#!/usr/bin/env bash
# Ansible runner — mints a short-lived SSH certificate from the OpenBao CA
# (ssh-certificate-authority ADR) and runs the playbook under it, falling back
# to the static break-glass key ONLY when no certificate environment is present
# at all (never when a mint fails; see the fail-loud guard below).
#
# It also exports the AppRole login token as BAO_TOKEN, which is what lets the
# playbooks read their own credentials from OpenBao instead of expecting them
# as ambient environment variables. That is the whole reason an unattended run
# needs no secrets of its own.
#
# Two identities, selected automatically and never mixed:
#   OPENBAO_APPROLE_SEMAPHORE_*  -> signs as automation-semaphore (unattended)
#   OPENBAO_APPROLE_ANSIBLE_*    -> signs as automation-ansible   (interactive)
#
#   scripts/run-ansible.sh playbooks/site.yml [args...]
#
# An interactive run still needs BAO_ADDR and one AppRole pair in the
# environment; a secrets-manager wrapper is the usual way to get them.
set -euo pipefail

usage() {
  echo "Usage: $0 <playbook> [ansible-playbook args...]"
  echo "Example: $0 playbooks/site.yml --limit vms"
  exit 1
}

[[ $# -lt 1 ]] && usage

PLAYBOOK="$1"
shift

CERT_DIR=""
RUNNER_BAO_TOKEN=""
BAO_TOKEN_WAS_SET=${BAO_TOKEN+x}

revoke_runner_token() {
  [[ -z $RUNNER_BAO_TOKEN ]] && return 0
  { set +x; } 2>/dev/null
  if curl -fsSL --max-time 10 --request POST \
    -H @<(printf 'X-Vault-Token: %s\n' "$RUNNER_BAO_TOKEN") \
    --output /dev/null \
    "$BAO_ADDR/v1/auth/token/revoke-self"; then
    RUNNER_BAO_TOKEN=""
    return 0
  fi
  return 1
}

cleanup() {
  local status=$? revoke_status=0
  revoke_runner_token || revoke_status=$?
  [[ -n $CERT_DIR ]] && rm -rf "$CERT_DIR"
  if (( revoke_status != 0 )); then
    echo "ERROR: failed to revoke the runner-owned OpenBao token." >&2
  fi
  if (( status != 0 )); then
    exit "$status"
  fi
  if (( revoke_status != 0 )); then
    exit "$revoke_status"
  fi
}
trap cleanup EXIT

# WHICH IDENTITY THIS RUN USES.
# The unattended execution plane has its own AppRole and its own CA signing
# role; a laptop run has the shared ansible-converge one. The two travel
# TOGETHER — an identity signed under the other's principal would authenticate
# while misreporting who ran the converge — so a single choice here selects
# both, rather than letting the caller set them independently and mismatch them.
CERT_ROLE=""
if [[ -n ${OPENBAO_APPROLE_SEMAPHORE_ROLE_ID:-} && -n ${OPENBAO_APPROLE_SEMAPHORE_SECRET_ID:-} ]]; then
  APPROLE_ROLE_ID="$OPENBAO_APPROLE_SEMAPHORE_ROLE_ID"
  APPROLE_SECRET_ID="$OPENBAO_APPROLE_SEMAPHORE_SECRET_ID"
  CERT_ROLE="automation-semaphore"
elif [[ -n ${OPENBAO_APPROLE_ANSIBLE_ROLE_ID:-} && -n ${OPENBAO_APPROLE_ANSIBLE_SECRET_ID:-} ]]; then
  APPROLE_ROLE_ID="$OPENBAO_APPROLE_ANSIBLE_ROLE_ID"
  APPROLE_SECRET_ID="$OPENBAO_APPROLE_ANSIBLE_SECRET_ID"
  CERT_ROLE="automation-ansible"
fi

# Mint an ephemeral ed25519 keypair signed by ssh-client-ca/sign/<role>, using
# the identity chosen above. OpenSSH pairs id + id-cert.pub automatically via
# PROXMOX_SSH_KEY_PATH. No secret material on any command line.
mint_ssh_cert() {
  local mount=${SSH_CA_MOUNT:-ssh-client-ca} login token signed
  CERT_DIR=$(mktemp -d "${TMPDIR:-/tmp}/ansible-sshcert.XXXXXX") || return 1
  chmod 700 "$CERT_DIR"
  (umask 077 && ssh-keygen -q -t ed25519 -N '' -C "$CERT_ROLE" -f "$CERT_DIR/id") || return 1
  { set +x; } 2>/dev/null
  login=$(jq -nc --arg r "$APPROLE_ROLE_ID" --arg s "$APPROLE_SECRET_ID" \
    '{role_id: $r, secret_id: $s}' \
    | curl -fsSL --max-time 10 -H 'Content-Type: application/json' --data @- \
      "$BAO_ADDR/v1/auth/approle/login") || return 1
  token=$(printf '%s' "$login" | jq -er '.auth.client_token') || return 1
  RUNNER_BAO_TOKEN="$token"
  # 2h, not 1h. A full converge outlived its own certificate once and every
  # host remaining after the expiry failed to connect — which reads as a fleet
  # of unreachable hosts rather than as one expired credential.
  signed=$(jq -nc --rawfile pub "$CERT_DIR/id.pub" --arg ttl "${SSH_CERT_TTL:-2h}" \
    '{public_key: $pub, ttl: $ttl}' \
    | curl -fsSL --max-time 10 \
      -H @<(printf 'X-Vault-Token: %s\n' "$RUNNER_BAO_TOKEN") --data @- \
      "$BAO_ADDR/v1/$mount/sign/$CERT_ROLE" \
    | jq -er '.data.signed_key') || return 1
  printf '%s\n' "$signed" > "$CERT_DIR/id-cert.pub"
  # Controller-side OpenBao reads share this short-lived token; cleanup revokes
  # it when the run ends. Exported under BOTH names on purpose: roles here read
  # BAO_*, while community.hashi_vault (how the playbooks read their own
  # credentials) takes VAULT_ADDR / VAULT_TOKEN. Same value, two consumers, so
  # neither needs a bespoke shim.
  if [[ -z $BAO_TOKEN_WAS_SET ]]; then
    export BAO_TOKEN="$token"
  fi
  export VAULT_ADDR="$BAO_ADDR"
  export VAULT_TOKEN="$token"
  export PROXMOX_SSH_KEY_PATH="$CERT_DIR/id"
}

# FAIL LOUD. This used to read `[[ cert env present ]] && mint_ssh_cert`, so a
# FAILED mint short-circuited to the static-key branch and the run continued on
# the break-glass key without saying so — the certificate path could be dead
# for weeks while every converge reported success. When the cert environment is
# present a mint failure is an error, never a silent downgrade.
if [[ -n ${BAO_ADDR:-} && -n $CERT_ROLE ]]; then
  if ! mint_ssh_cert; then
    echo "ERROR: OpenBao SSH certificate mint FAILED for role '$CERT_ROLE' and the" >&2
    echo "       cert environment is present — refusing to fall back to the static key." >&2
    exit 1
  fi
  echo "Using a short-lived SSH certificate from the OpenBao CA ($CERT_ROLE)."
elif [[ -z ${PROXMOX_SSH_KEY_PATH:-} ]]; then
  echo "ERROR: no SSH auth available — set BAO_ADDR plus either" >&2
  echo "       OPENBAO_APPROLE_SEMAPHORE_* or OPENBAO_APPROLE_ANSIBLE_* for cert" >&2
  echo "       minting, or PROXMOX_SSH_KEY_PATH for the static break-glass key." >&2
  exit 1
fi

ansible-playbook "$PLAYBOOK" "$@"
