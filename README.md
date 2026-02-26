# Ansible Splunk Enterprise

[![Lint](https://github.com/JacobPEvans/ansible-splunk/actions/workflows/lint.yml/badge.svg)](https://github.com/JacobPEvans/ansible-splunk/actions/workflows/lint.yml)
[![Molecule](https://github.com/JacobPEvans/ansible-splunk/actions/workflows/molecule.yml/badge.svg)](https://github.com/JacobPEvans/ansible-splunk/actions/workflows/molecule.yml)
[![Validate](https://github.com/JacobPEvans/ansible-splunk/actions/workflows/validate.yml/badge.svg)](https://github.com/JacobPEvans/ansible-splunk/actions/workflows/validate.yml)

Deploy and configure Splunk Enterprise (Docker) on a Proxmox VM.

## Quick Facts

| Property | Value |
| --- | --- |
| **Type** | Ansible role + playbooks |
| **Target** | Proxmox VM `10.0.1.200` (VMID 200) |
| **Role** | `roles/splunk_docker` |
| **Entry point** | `playbooks/site.yml` |
| **Secrets** | Doppler (`iac-conf-mgmt` / `prd`) |
| **Version** | See `VERSION` |

## Pipeline Architecture

```text
Cribl Edge (181/182) ──HEC :8088──> Splunk (200)
                                      │
                                  Splunk indexes:
                                    ai, claude, firewall,
                                    netflow, network, os, unifi
```

## Quick Start

```bash
# 1. Deploy Splunk
doppler run -- pipx run ansible-playbook playbooks/site.yml

# 2. Validate deployment
doppler run -- pipx run ansible-playbook playbooks/validate.yml
```

## Custom Indexes

All indexes: 100 GiB max size, 365-day retention, stored at `/opt/splunk/<index>/`.

| Index | Purpose |
| --- | --- |
| `ai` | AI assistant activity and tool calls |
| `claude` | Claude-specific events |
| `firewall` | Palo Alto / Cisco firewall logs |
| `netflow` | NetFlow / IPFIX flow data |
| `network` | Network device syslog |
| `os` | Linux / Windows system logs |
| `unifi` | UniFi network syslog |

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

## Role Structure

```text
roles/splunk_docker/
├── defaults/main.yml       # Core Docker + Splunk configuration
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

Key defaults in `roles/splunk_docker/defaults/main.yml`:

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

All secrets via Doppler (`iac-conf-mgmt` / `prd`):

| Doppler Secret | Ansible Variable | Purpose |
| --- | --- | --- |
| `SPLUNK_PASSWORD` | `splunk_docker_password` | Splunk admin password |
| `SPLUNK_HEC_TOKEN` | `splunk_docker_hec_token` | HEC token UUID |
| `PROXMOX_SSH_KEY_PATH` | — | SSH key for VM access |

```bash
# Run any playbook with secrets injected
doppler run -- pipx run ansible-playbook playbooks/site.yml
```

## Testing

```bash
# Lint
pipx run ansible-lint

# Syntax check
doppler run -- pipx run ansible-playbook playbooks/site.yml --syntax-check

# Molecule (syntax-only CI test)
pipx run molecule test

# Post-deploy validation
doppler run -- pipx run ansible-playbook playbooks/validate.yml
```

## Dependencies

### Ansible Collections (`requirements.yml`)

| Collection | Version |
| --- | --- |
| `ansible.posix` | `>=2.1.0,<3.0.0` |
| `community.general` | `>=12.4.0,<13.0.0` |
| `community.docker` | `>=5.0.6,<6.0.0` |
| `cloud.terraform` | `>=4.0.0,<5.0.0` |

```bash
pipx run ansible-galaxy collection install -r requirements.yml
```

### External Services

- **terraform-proxmox** — provisions Splunk VM (VMID 200)
- **Doppler** — secrets management
- **Proxmox firewall** — network access control (no guest iptables)

## Links

- [Changelog](CHANGELOG.md)
- [Contributing](CONTRIBUTING.md)
- [Splunk Docker image](https://hub.docker.com/r/splunk/splunk)
- [ansible-proxmox-apps](https://github.com/JacobPEvans/ansible-proxmox-apps) — Cribl Edge (upstream sender)
