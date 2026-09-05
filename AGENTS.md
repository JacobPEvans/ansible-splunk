---
skill-groups: [core, review]
---
# ansible-splunk - AI Agent Documentation

Ansible automation for Splunk Enterprise deployment on a Proxmox VM.
**Single source of truth** for Splunk configuration in the dryvist
homelab.

## Container strategy: Docker (exception)

Splunk runs in Docker on a dedicated VM (VMID 200) — a deliberate
exception to the global LXC-first rule (see `~/git/CLAUDE.md` Container
Deployment Rules).

**Why Docker:** This repository standardizes on Splunk Enterprise via
the official `splunk/splunk` Docker image. Native Linux package and
tarball installs exist but are out of scope. The `splunk_docker` role
manages the container lifecycle via Docker Compose.

**Implication:** New features and integrations target Docker Compose
on the Splunk VM. Do not propose LXC migration or new Docker containers
for ancillary services — those belong in `ansible-proxmox-apps` as LXC.

## This repo owns

- Splunk Enterprise container deployment (Docker Compose on Proxmox VM)
- HEC (HTTP Event Collector) configuration
- Custom index creation and retention
- Technology Add-ons (TAs) and Splunkbase apps
- MCP Server integration (app 7931)

## Critical constraints

- **Firewall disabled**: Guest firewall is off
  (`splunk_docker_firewall_enabled: false`). Docker DNAT conflicts with
  iptables FORWARD chain. The Proxmox firewall is the sole network
  security (see `dryvist/tofu-proxmox` firewall modules).
- **HEC tokens**: Per-index tokens are derived via
  `uuidv5(HEC_NAMESPACE, "splunk-hec-<index_name>")`. `HEC_NAMESPACE` is
  required — a run without it is a hard fail (`playbooks/site.yml`),
  because silently falling back used to drop every per-index sender's
  token from `inputs.conf` and cause a live ingest outage on restart.
  `SPLUNK_HEC_TOKEN` is the separate shared legacy token, also required.
- **HEC transport**: HTTPS (Splunk Docker image default, SSL enabled).
- **Secrets**: Deployment inputs come from Doppler (`doppler run --`). The role
  publishes the shared Splunk MCP connection to OpenBao
  `secret/ai/mcp/splunk` when explicitly enabled.

## Dependencies

### Upstream

- **`dryvist/tofu-proxmox`**: provisions Splunk VM 200 through Terrakube and
  publishes the `ansible_inventory` output to homelab RustFS on every apply.
  `inventory/load_tofu.yml` resolves it: `TOFU_INVENTORY_PATH` (explicit
  pin) → RustFS artifact (native `amazon.aws`, credentials read directly from
  OpenBao `secret/platform/object-storage`; override:
  `TOFU_INVENTORY_S3_URI`) → static fallback (`SPLUNK_VM_HOST`, named
  explicitly — the VM's hostname is declared once in `deployment.json` and is
  never defaulted here). There is **no local-cache step** — see "Inventory
  freshness guarantee" below.

- **`dryvist/homelab-contracts`**: supplies the shared `inventory_resolve`
  role, pinned by commit in `requirements.yml`. Run
  `ansible-galaxy install -r requirements.yml` before the first converge in a
  fresh checkout. Use `install`, not `role install`: `requirements.yml` has both
  a `roles:` and a `collections:` section, and `role install -p roles` prints
  *"contains collections which will be ignored"* and installs none of them.
  Add `--force` if `roles/inventory_resolve`
  already exists — a plain install leaves an older copy in place, and the
  resolution order differs between versions, so a stale copy changes converge
  behavior while the pin still reads correct.

#### Inventory freshness guarantee (single-writer / readers-always-latest)

RustFS is the single source of truth; this repo is a **read-only consumer** and
holds no authoritative local inventory. The producer-side ACID contract is
documented once at
[Deployment state contract](https://docs.jacobpevans.com/infrastructure/deployment-state-contract).

- **Single writer**: Terrakube serializes each `tofu-proxmox` apply with its
  native workspace lock and republishes the artifact with a single atomic PUT, so two applies
  cannot both publish. This lock lives in the producer — a consumer repo cannot
  (and must not) reimplement it. (Lock mechanics: see the contract above.)
- **Readers always get the latest**: S3-compatible strong read-after-write consistency —
  every GET returns the most recent PUT; concurrent reads need no lock. The S3
  fetch retries transient blips before degrading.
- **No staleness hole**: there is deliberately no on-disk inventory cache. The
  only non-RustFS source is the DNS-first static fallback, and that A-record is
  itself continuously reconciled from this same inventory (Technitium) — a live
  source for the Splunk VM address, not a frozen copy.

### External services

- **Doppler**: Secrets for `SPLUNK_PASSWORD`, `HEC_NAMESPACE`,
  `SPLUNK_HEC_TOKEN`, `PROXMOX_SSH_KEY_PATH`,
  `OBJECT_STORAGE_ROOT_USER`, `OBJECT_STORAGE_ROOT_PASSWORD`.

## Sources of truth

| What | Where |
| --- | --- |
| Index definitions | `roles/splunk_docker/defaults/main/` |
| Add-on registry | `roles/splunk_docker/vars/addons.yml` |
| MCP Server configuration | `roles/splunk_docker/vars/mcp.yml` |
| Inventory | `inventory/load_tofu.yml` |
| Pipeline architecture | `~/git/CLAUDE.md` |
| HEC setup and MCP verification | `roles/splunk_docker/README.md` |

## Key files

| Path | Purpose |
| --- | --- |
| `roles/splunk_docker/` | Splunk deployment role |
| `roles/splunk_docker/files/` | App archives (gitignored) |
| `playbooks/site.yml` | Full deployment playbook |
| `playbooks/sync-splunkbase.yml` | Splunkbase → object-storage (RustFS) sync |
| `playbooks/validate.yml` | Post-deploy validation |
| `inventory/load_tofu.yml` | Dynamic inventory loader |

## Commands

`doppler run` supplies `BAO_ADDR` but **not** `BAO_TOKEN`. Without a token the
loader cannot read the object-storage credential, so it cannot fetch the
published inventory. It does not stop. It falls back to the static host entry
in `hosts.yml`, and the run dies later on `'tofu_data' is undefined` — after it
has already written config. There is no prompt and no warning.

Mint a read token in the same invocation. Reads are pre-authorized, so this
needs no approval. Never write the token to a file:

```bash
export BAO_TOKEN=$(doppler run -- bash -c 'curl -sS -X POST \
  -d "{\"role_id\":\"$OPENBAO_APPROLE_ANSIBLE_ROLE_ID\",\"secret_id\":\"$OPENBAO_APPROLE_ANSIBLE_SECRET_ID\"}" \
  "$BAO_ADDR/v1/auth/approle/login"' \
  | python3 -c 'import sys,json;print(json.load(sys.stdin)["auth"]["client_token"])')
```

To tell which path a run took, read the host name in the play output: the
dynamic path yields the real inventory name, the static fallback yields the
placeholder from `hosts.yml`.

This is a *read* credential. It is unrelated to the elevated token that writing
the desired-state object needs — that path is `flow-lock`, and no converge
should ever take that lease.

Converges run through Semaphore, the execution plane. Its template wrapper
loads the run environment from OpenBao before the playbook starts. Playbooks
read plain environment variables and are independent of the secrets manager:
`.env`, Doppler, OpenBao or any other injector behaves identically.
`scripts/run-ansible.sh` remains the runner the wrapper calls and the
break-glass path from a workstation.

```bash
# Full deployment (object storage → Splunk VM, direct target-side pull)
doppler run -- ansible-playbook playbooks/site.yml

# Sync Splunkbase → object storage (run before site.yml when versions bumped)
doppler run -- ansible-playbook playbooks/sync-splunkbase.yml

# Validate deployment
doppler run -- ansible-playbook playbooks/validate.yml

# Lint
ansible-lint
```

### Execution Performance & Optimization

Ansible runs in this repo are generally fast since it targets a single VM.
However, if running larger-scale validation or checking/deploying across
multiple endpoints, keep these speed options in mind:

1. **Parallel Execution (`--forks` or `ANSIBLE_FORKS`)**: Concurrency default is
   5 hosts. Specifying a higher value (e.g. `--forks 25`) runs parallel checks
   faster.
2. **Targeted Runs (`--limit`)**: Restrict playbook runs to specific target
   hosts (e.g., `--limit splunk-vm`).
3. **Disable Fact Gathering**: If host facts aren't needed, setting
   `gather_facts: false` bypasses the slow setup step.

## Agent tasks

### Troubleshooting

- **Health check fails**: Check container logs with `docker logs splunk`.
- **Apps not visible**: Verify ownership is UID 41812.
- **HEC not working**: Confirm `SPLUNK_HEC_TOKEN` in Doppler; set
  `HEC_NAMESPACE` for per-index tokens.
- **MCP Server not responding**: Verify token minting via the app's
  `/services/mcp_token` endpoint; confirm port 8089 is accessible and
  `SPLUNK_MCP_URL` points to the `<mgmt-base>/services/mcp` path.

### Adding Splunkbase apps

1. Add the app entry to `roles/splunk_docker/vars/addons.yml` under `splunk_docker_addons` with its `filename`, `app_dir`, and `splunkbase_id`.
2. Sync the app to object storage: `doppler run -- ansible-playbook playbooks/sync-splunkbase.yml`.
3. Re-run `doppler run -- ansible-playbook playbooks/site.yml`.

### Adding custom add-ons

1. Package the custom add-on as a version-free `.tar` archive.
2. Upload the archive to object storage (e.g. using `aws s3 cp`) and tag it with `version=X.Y.Z`.
3. Add the entry to `roles/splunk_docker/vars/addons.yml` without a `splunkbase_id`.
4. Re-run `doppler run -- ansible-playbook playbooks/site.yml`.

## Artifact store (object-storage / RustFS)

Custom add-ons and current Splunkbase packages that the air-gapped Splunk VM
pulls over the LAN are served from a self-hosted S3-compatible object-storage
instance (RustFS LXC). Endpoint and port come from the
OpenTofu inventory (`tofu_data.constants.service_ports.object_storage_s3`);
bucket-write auth is `OBJECT_STORAGE_ROOT_USER` / `OBJECT_STORAGE_ROOT_PASSWORD`
from Doppler.

- Bucket: `splunk-addons` (anonymous read on internal network).
- Add-ons with `artifact_store: true` in `vars/custom_addons.yml`
  auto-download.
- Upload new versions via `aws s3 cp` — filenames are version-free,
  versions tracked via object tags (`aws s3api put-object-tagging`).
- S3 bucket versioning is required. Prior uploads are native object versions;
  no application-managed archive path is used.
- Current Splunkbase objects carry `channel=latest`, `version`, and
  `splunkbase_id` tags.
- Run `doppler run -- ansible-playbook playbooks/sync-splunkbase.yml -e
  splunkbase_update_scope=official_ai` to update the priority official AI scope
  without removing unrelated manifest entries.
- See `roles/splunk_docker/files/README.md` for upload instructions.

## MCP Server tools

The Splunk MCP Server provides these tools for AI agents after deployment:

| Tool | Description | Example |
| --- | --- | --- |
| `run_splunk_query` | Execute SPL searches | `\| makeresults \| eval test="ok"` |
| `get_indexes` | List all indexes | Returns 11 custom + system indexes |
| `get_sourcetypes` | List sourcetypes | Returns ingested sourcetypes |

Configure the MCP client in `dryvist/nix-ai` (`modules/mcp/`).

## Secrets management

Deployment secrets are retrieved from Doppler at runtime. The Splunk MCP
connection is an output published to OpenBao when explicitly enabled:

| Secret | Purpose |
| --- | --- |
| `SPLUNK_PASSWORD` | Admin password |
| `HEC_NAMESPACE` | UUID namespace for per-index HEC token derivation (required) |
| `SPLUNK_HEC_TOKEN` | Shared legacy HEC token (always required) |
| `SPLUNK_MCP_TOKEN` | Client-side MCP Bearer token minted per managed user and published with `SPLUNK_MCP_URL` to OpenBao `secret/ai/mcp/splunk` |
| `PROXMOX_SSH_KEY_PATH` | SSH key for VM access |
| `SPLUNK_LICENSE` | Raw `.lic` XML for the cluster license master; required — clustering needs Enterprise. Re-applied on every converge |

## Tooling baseline (inherited from dryvist/.github)

- **Markdown lint:** `markdownlint-cli2` with the canonical
  `.markdownlint-cli2.yaml` synced from
  [`dryvist/.github`](https://github.com/dryvist/.github).
  `MD013 line_length: 160`; no 80-char heading/code restrictions.
  `CHANGELOG.md`, `.github/workflows/*.md`, `.github/aw/**`, and
  `.claude/**` are ignored. `MD024` strict-by-default everywhere
  actually linted — never disabled across the board.
- **Pre-commit hooks** (this is NOT a Nix-flake-based repo so we keep
  `.pre-commit-config.yaml`):
  `pre-commit/pre-commit-hooks@v6.0.0` meta-pack,
  `DavidAnson/markdownlint-cli2@v0.22.0`, `gitleaks/gitleaks@v8.30.1`,
  `adrienverge/yamllint`, local `ansible-lint`.

Do NOT commit local copies of `.markdownlint-cli2.{jsonc,yaml}` that
drift from the dryvist canonical, and do NOT re-introduce leniency
rules to work around stale tooling.

## Related repositories

| Repo | Relationship |
| --- | --- |
| `dryvist/tofu-proxmox` | Upstream: provisions Splunk VM + object-storage (RustFS) LXC |
| `dryvist/ansible-proxmox-apps` | Peer: owns Cribl (sends to HEC), deploys the object storage (RustFS) |
| `dryvist/ansible-proxmox` | Peer: Proxmox host config |
| `dryvist/nix-ai` | MCP client configuration (`modules/mcp/`) |
