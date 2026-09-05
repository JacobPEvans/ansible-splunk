# Splunk Docker Role

Deploys Splunk Enterprise in a Docker container on a Proxmox VM.

## Overview

This role:

- Installs Docker and Docker Compose
- Deploys Splunk Enterprise container
- Configures custom indexes
- Installs Technology Add-ons (TAs)
- Applies firewall rules (optional)

## Installation

```bash
ansible-galaxy install -r requirements.yml
```

`install` covers both sections of `requirements.yml`. The `collection`
subcommand reads only `collections:` and silently skips `roles:`, so the
Splunk role would be missing and the play would fail on an unrelated error.

## Requirements

- Debian-based target host
- Doppler secrets for SPLUNK_PASSWORD and SPLUNK_HEC_TOKEN
- VM provisioned by tofu-proxmox with appropriate disk space

## Role Variables

See `defaults/main/` for all variables (one topic per file). Key variables:

| Variable | Default | Description |
| -------- | ------- | ----------- |
| `splunk_docker_image` | `splunk/splunk:10.4.3` | Splunk Docker image (pinned; Renovate-tracked) |
| `splunk_docker_web_port` | `8000` | Web UI port |
| `splunk_docker_hec_port` | `8088` | HEC port |
| `splunk_docker_user` | `41812` | Splunk container user UID |
| `splunk_docker_firewall_enabled` | `false` | Enable firewall rules |

## File Ownership

The Splunk container runs processes as UID 41812 (splunk user inside container).
All Splunk data directories and apps are owned by this UID to ensure proper
permissions inside the container.

## Technology Add-ons

TAs are placed in `files/` and configured in `splunk_docker_addons`:

```yaml
splunk_docker_addons:
  - name: TA-unifi-cloud
    filename: "TA-unifi-cloud-{{ splunk_docker_unifi_ta_version }}.tar"
    description: UniFi Cloud Add-on
```

## Usage

```yaml
- hosts: splunk
  roles:
    - role: splunk_docker
      vars:
        splunk_docker_password: "{{ lookup('env', 'SPLUNK_PASSWORD') }}"
        splunk_docker_hec_token: "{{ lookup('env', 'SPLUNK_HEC_TOKEN') }}"
```

## Dependencies

- community.docker collection
- tofu-proxmox for VM provisioning
- Doppler for secrets management

## HEC Token Setup

**Per-index tokens** are derived deterministically via UUID v5:

```text
Token = uuidv5(HEC_NAMESPACE, "splunk-hec-<index_name>")
```

The `HEC_NAMESPACE` UUID is stored in Doppler. Any system with access to that
namespace can derive tokens locally. `SPLUNK_HEC_TOKEN` is the shared legacy
fallback that grants access to all indexes.

### One-time Doppler Setup

```bash
# Generate a random namespace UUID (enables per-index tokens)
doppler secrets set HEC_NAMESPACE "$(uuidgen)"

# Set the shared legacy token (always required)
doppler secrets set SPLUNK_HEC_TOKEN "$(uuidgen)"
```

### Adding a New Index + Token

1. Add the index to `splunk_docker_indexes_core` or `splunk_docker_indexes_extra`
   in `defaults/main/09-custom-indexes-core.yml` / `10-custom-indexes-extra.yml`
2. Run `doppler run -- ansible-playbook playbooks/site.yml` — token is auto-derived
3. Senders derive the same token locally:

```bash
python3 -c "import uuid; print(uuid.uuid5(uuid.UUID('$HEC_NAMESPACE'), 'splunk-hec-<index_name>'))"
```

## MCP Server Verification

The Splunk MCP Server (app 7931) enables AI agents to query Splunk directly
via the Model Context Protocol (MCP). The MCP JSON-RPC endpoint clients connect
to is `<mgmt-base>/services/mcp` (for example,
`SPLUNK_MCP_URL=https://<host>:8089/services/mcp`).
Tokens are minted via the app's `/services/mcp_token` endpoint. Configure the MCP client in
`~/git/nix-ai/main/modules/mcp/default.nix`.

When OpenBao publication is enabled, the role writes the shared connection as
`SPLUNK_MCP_URL` and `SPLUNK_MCP_TOKEN` at `secret/ai/mcp/splunk`. The KV-v2
write preserves sibling fields and uses metadata-based compare-and-set, including
when the latest secret version was soft-deleted. The publisher AppRole needs
KV-v2 data read/write, metadata read, and undelete access for this exact path.
Every converge validates the published JWT's subject, audience, validity window,
and token ID against Splunk; inventory presence alone never suppresses repair of
a missing or invalid canonical credential, and duplicate live tokens trigger
replacement so a failed cleanup is recovered by the next default converge.

For an operator-initiated rotation, run one converge with
`splunk_docker_token_force_rotate: true`. Publication must also be enabled. The
role mints exactly one replacement per user, publishes it with KV-v2 compare-and-set,
then re-enumerates Splunk and revokes every other eligible token for that user
and audience, including tokens minted concurrently after the initial snapshot.
A final read proves the published token is the sole eligible token. Disabled or
expired tokens, and tokens whose not-before time is still in the future, do not
count as live. If publication fails, the role attempts to revoke the unpublished
replacement and leaves the old snapshot untouched; if final revocation fails,
both old and new tokens remain usable. Leave the option at its default `false`
for ordinary converges; default mode still repairs an undelivered token.

### Available MCP Tools

| Tool | Description |
| --- | --- |
| `run_splunk_query` | Execute SPL search queries |
| `get_indexes` | List all Splunk indexes |
| `get_sourcetypes` | List available sourcetypes |

### Verifying MCP Connection

```bash
# Check MCP Server app is installed and REST API responds
doppler run -- ansible-playbook playbooks/validate.yml

# Direct REST API test
curl -sk https://<SPLUNK_HOST_IP>:8089/services/apps/local/splunk-mcp-server \
  -u "admin:$SPLUNK_PASSWORD" | grep -o '"name">.*<'
```
