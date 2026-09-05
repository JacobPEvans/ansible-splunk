# Ansible Splunk Enterprise

[![CI][ci-badge]][ci-url]

[ci-badge]: https://github.com/dryvist/ansible-splunk/actions/workflows/ci-gate.yml/badge.svg
[ci-url]: https://github.com/dryvist/ansible-splunk/actions/workflows/ci-gate.yml

Deploy and configure Splunk Enterprise (Docker) on a Proxmox VM.

## Quick Facts

| Property | Value |
| --- | --- |
| **Type** | Ansible role + playbooks |
| **Target** | Splunk VM (VMID 200) — addressed from the tofu inventory, or by an explicit `SPLUNK_VM_HOST` |
| **Role** | `roles/splunk_docker` |
| **Entry point** | `playbooks/site.yml` |
| **Secrets** | Doppler |
| **Version** | See `VERSION` |

## Pipeline Architecture

```text
Cribl Edge (181/182) ──HEC :8088──> Splunk (200)
                                      │
                                  Splunk indexes:
                                    ai, claude, firewall, gemini,
                                    mac_perf, netflow, netmon_metrics, network,
                                    openai, os, os_metrics, otel_traces, unifi,
                                    unifi_metrics, vscode
```

## Installation

This repo provides a [Nix dev shell][nix-develop] with all tools
(`ansible-playbook`, `ansible-lint`, `molecule`, etc.). Activate it once per worktree
with `direnv allow` — the committed `.envrc` wires up the shell automatically.

## Usage

Converges run through Semaphore, the execution plane. Its template wrapper
loads the run environment from OpenBao before the playbook starts. Playbooks
read plain environment variables and are independent of the secrets manager:
`.env`, Doppler, OpenBao or any other injector behaves identically.
`scripts/run-ansible.sh` remains the runner the wrapper calls and the
break-glass path from a workstation.

The commands below are that break-glass path, plus local development and
testing.

```bash
# 1. Deploy Splunk
doppler run -- ansible-playbook playbooks/site.yml

# 2. Validate deployment
doppler run -- ansible-playbook playbooks/validate.yml
```

## Custom Indexes

Per-index size caps and retention are set in
`roles/splunk_docker/defaults/main/09-custom-indexes-core.yml` and
`10-custom-indexes-extra.yml` (`splunk_docker_indexes`); most
indexes use the 365-day/10 GiB defaults, but `netflow`, `host_metrics`,
`llm_metrics`, `netmon_metrics`, `os_metrics`, and `unifi_metrics` use
90-day retention, and `netflow` caps at 50 GiB rather than the default. Two
indexes — `firewall` and `unifi` — are tiered: their hot data stays on fast
storage (`$SPLUNK_DB`) and their cold data rolls out to a separate
`splunk_docker_cold_dir` volume; every other index keeps both hot and cold
data on fast storage.

| Index | Purpose |
| --- | --- |
| `ai` | AI assistant activity and tool calls |
| `claude` | Claude-specific events |
| `firewall` | Palo Alto / Cisco firewall logs |
| `gemini` | Gemini-specific events |
| `mac_perf` | macOS performance metrics |
| `netflow` | NetFlow / IPFIX flow data |
| `netmon_metrics` | Per-WAN network-diagnosis probe telemetry, metric index (90-day retention) |
| `network` | Network device syslog |
| `openai` | OpenAI-specific events |
| `os` | Linux / Windows system logs |
| `os_metrics` | Per-host OS metric series (CPU/mem/disk/net, incl. per-process), metric index (90-day retention) |
| `otel_traces` | OpenTelemetry trace spans (sole trace index) |
| `unifi` | UniFi network syslog |
| `unifi_metrics` | UniFi controller device/port/client/WAN metrics (unpoller+Telegraf via Cribl, 90-day retention) |
| `vscode` | VS Code / Copilot events |

## Technology Add-ons

Archives must be placed in `roles/splunk_docker/files/` before running (gitignored).
See [`roles/splunk_docker/files/README.md`](roles/splunk_docker/files/README.md) for download instructions.

| Add-on | Source | Notes |
| --- | --- | --- |
| TA-unifi-cloud | Internal build | UniFi syslog parsing |
| Duck Yeah | Splunkbase | App packaging utilities |
| Splunk DB Connect | Splunkbase [#2686](https://splunkbase.splunk.com/app/2686) | DB connectivity |

## Playbooks

| Playbook | Purpose |
| --- | --- |
| `site.yml` | Full deployment: loads inventory, runs `splunk_docker` role |
| `deploy.yml` | Bare deployment (no inventory load) |
| `deploy_docker.yml` | Deploys Splunk container, assuming Docker is pre-installed |
| `validate.yml` | Post-deploy validation: ports, HEC, web UI |
| `configure_indexes.yml` | Index configuration only (idempotent) |
| `sync-splunkbase.yml` | Mirrors current Splunkbase releases at stable artifact keys and publishes the deployment manifest |

`sync-splunkbase.yml` stores each app at one version-free key. Native S3 bucket
versioning retains prior object versions, while current objects carry
`channel=latest`, `version`, and `splunkbase_id` tags. Run the priority vendor
AI scope with `-e splunkbase_update_scope=official_ai`; it updates Python for
Scientific Computing, Splunk AI Toolkit, MLTK Container, and Splunk AI Assistant
without replacing unrelated manifest entries.

## Role Structure

```text
roles/splunk_docker/
├── defaults/main/          # Core Docker + Splunk configuration (one file per topic)
├── tasks/
│   ├── main.yml            # Orchestrates all tasks
│   ├── java.yml            # Optional JRE-21 for DB Connect
│   └── wait_for_splunk.yml # Health check loop after container start
├── templates/
│   ├── docker-compose.yml.j2
│   ├── indexes.conf.j2
│   ├── inputs.conf.j2      # HEC token configuration
│   ├── web.conf.j2
│   ├── server.conf.j2
│   └── firewall.sh.j2
├── handlers/main.yml       # Restart Splunk container
└── files/                  # TA archives (gitignored)
```

## Configuration Variables

Key defaults in `roles/splunk_docker/defaults/main/`:

| Variable | Default | Description |
| --- | --- | --- |
| `splunk_docker_image` | `splunk/splunk:latest` | Docker image. Pin to a specific version for production. |
| `splunk_docker_web_port` | `8000` | Splunk Web UI port |
| `splunk_docker_hec_port` | `8088` | HEC ingestion port |
| `splunk_docker_data_dir` | `/opt/splunk` | Data volume mount path |
| `splunk_docker_web_ssl` | `true` | Enable Splunk Web SSL |
| `splunk_docker_java_enabled` | `false` | Enable JRE for DB Connect |
| `splunk_docker_firewall_enabled` | `false` | Guest iptables (disabled; use Proxmox firewall) |
| `splunk_docker_allow_internet_access` | `false` | Disables Splunkbase app browsing, update checks, and telemetry to prevent DNS timeouts on air-gapped VMs. |
| `splunk_docker_index_default_max_size_mb` | `102400` | 100 GiB per index |
| `splunk_docker_index_default_frozen_time_secs` | `31536000` | 365-day retention |

## Secrets

The playbooks read these as plain environment variables. Semaphore loads them
from OpenBao; from a workstation any injector supplies them.

| Environment variable | Ansible Variable | Purpose |
| --- | --- | --- |
| `SPLUNK_PASSWORD` | `splunk_docker_password` | Splunk admin password |
| `HEC_NAMESPACE` | `splunk_docker_hec_namespace` | UUID namespace for per-index HEC token derivation (required) |
| `SPLUNK_HEC_TOKEN` | `splunk_docker_hec_token_values.legacy` | Shared legacy HEC token (always required) |
| `SPLUNK_MCP_TOKEN` | — | MCP Server Bearer token (client-side). Minted per managed user by the role — see [Managed service users](#managed-service-users) |
| `PROXMOX_SSH_KEY_PATH` | — | SSH key for VM access |

```bash
# Run any playbook with secrets injected
doppler run -- ansible-playbook playbooks/site.yml
```

> **Rotating `SPLUNK_PASSWORD`:** the splunk/splunk image seeds the admin password
> from `SPLUNK_PASSWORD` only on the container's first boot, when
> `/opt/splunk/etc/passwd` is absent. Because `etc/` is a persistent disk mount,
> changing `SPLUNK_PASSWORD` afterward does **not** update the running admin — the
> entrypoint's Ansible then loops on a "Get existing HEC token" 401. After any
> rotation you must reset the container admin via the standard
> [user-seed.conf](https://docs.splunk.com/Documentation/Splunk/latest/Admin/User-seedconf)
> procedure on the persistent `etc/` mount.

## Managed service users

Service accounts (AI agents, MCP clients) get their own scoped Splunk identity
instead of sharing the admin password. Set `splunk_docker_manage_users: true`
and list them in `splunk_docker_users`:

```yaml
splunk_docker_users:
  - name: hermes
    roles: [admin]   # narrow to a custom read/search role once known
```

After the REST API is up, the role (`tasks/manage_users.yml`) idempotently:

1. **Enables token authentication** deployment-wide.
2. **Creates each user** with its roles (password is random, set once at
   creation — never rotated here, since the token is the real credential).
3. **Validates the canonical authorization token** (JWT) from OpenBao and mints
   a replacement when it is missing, invalid, outside its validity window, or
   duplicated in Splunk, and when explicitly rotated.

The minted JWT is the client-side `SPLUNK_MCP_TOKEN` the Splunk MCP Server
(Splunkbase 7931) accepts as a Bearer token — a Splunk token inherits its
owner's roles, so searches run with the user's capabilities. Because Splunk
returns a token's value **only once at creation**, minting is gated on a
delivery path: set `splunk_docker_token_publish_openbao: true` and provide a
write-capable OpenBao AppRole (`BAO_ADDR` / `BAO_TOKEN`) so the role merges the
canonical `SPLUNK_MCP_URL` and `SPLUNK_MCP_TOKEN` fields into
`secret/ai/mcp/splunk` without clobbering sibling keys. The AppRole needs KV-v2
data read/write, metadata read, and undelete access for that exact path so a
soft-deleted current version can be recovered before a compare-and-set write.
The role validates the published JWT's subject, audience, validity window, and
token ID against Splunk on every converge; merely finding a token in Splunk
never suppresses recovery when the canonical key is missing or invalid.
To rotate that token, run one converge with
`splunk_docker_token_force_rotate: true`. The role identifies one new token,
publishes it through a version-checked OpenBao merge, then re-enumerates Splunk
and revokes every other eligible token, including tokens minted concurrently
after the initial snapshot. A final read proves the published token is the sole
eligible token. Disabled, expired, and not-yet-valid tokens never count as live.
A publish failure removes the unpublished replacement when possible and never
revokes the old snapshot. Forced rotation requires publication to be enabled
and returns to its default-off state on the next normal converge. Until
publication is wired, users and roles are still reconciled; only token delivery
is deferred. The URL uses the
inventory-derived Splunk FQDN when available and can be overridden with
`splunk_docker_mcp_url`.

## Testing

```bash
# Lint
ansible-lint

# Syntax check
doppler run -- ansible-playbook playbooks/site.yml --syntax-check

# Molecule (syntax-only CI test)
molecule test

# Post-deploy validation
doppler run -- ansible-playbook playbooks/validate.yml
```

## Dependencies

### Ansible Collections (`requirements.yml`)

| Collection | Version |
| --- | --- |
| `ansible.posix` | `>=2.1.0,<3.0.0` |
| `community.general` | `>=12.4.0,<13.0.0` |
| `community.docker` | `>=5.0.6,<6.0.0` |
| `amazon.aws` | `>=9.0.0` |

```bash
ansible-galaxy install -r requirements.yml
```

### External Services

- **Splunk VM (VMID 200)** — provisioned externally; this repo configures it
- **Doppler** — secrets management
- **Proxmox firewall** — network access control (no guest iptables)

## Links

- [Changelog](CHANGELOG.md)
- [Contributing](CONTRIBUTING.md)
- [Splunk Docker image](https://hub.docker.com/r/splunk/splunk)

[nix-develop]: https://nixos.org/manual/nix/stable/command-ref/new-cli/nix3-develop.html

---

> Part of a [larger ecosystem of ~40 repos](https://docs.jacobpevans.com) — see how it all fits together.
