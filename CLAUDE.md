# Ansible Splunk Enterprise

Deploy and configure Splunk Enterprise (Docker) on Proxmox VM.

## This Repo Owns

- Splunk Enterprise container deployment
- HEC (HTTP Event Collector) configuration
- Custom index creation and retention
- Technology Add-ons (TAs)

## Pipeline Role

This repo is the **destination** for the syslog pipeline:

```text
Cribl Edge (ansible-proxmox-apps) -> Splunk HEC :8088
                                      |
                                  Splunk indexes:
                                    unifi, firewall,
                                    network, os, netflow
```

HEC runs on **HTTP** (not HTTPS). This role does not manage HEC SSL
settings; we rely on the Splunk Docker image's default HTTP behavior.
Cribl Edge is configured to send to `http://splunk:8088`.

## Custom Indexes

| Index | Purpose | Size | Retention |
| --- | --- | --- | --- |
| unifi | UniFi syslog | 100GB | 365 days |
| firewall | Palo Alto/Cisco | 100GB | 365 days |
| network | Network devices | 100GB | 365 days |
| os | Linux/Windows | 100GB | 365 days |
| netflow | NetFlow/IPFIX | 100GB | 365 days |

## Inventory

Loaded from `terraform_inventory.json` via
`inventory/load_terraform.yml`. Falls back to
`SPLUNK_VM_HOST` env var if JSON is missing.

### Required Environment Variables

| Variable | Purpose |
| --- | --- |
| `SPLUNK_PASSWORD` | Splunk admin password |
| `SPLUNK_HEC_TOKEN` | HTTP Event Collector token |
| `PROXMOX_SSH_KEY_PATH` | SSH key for VM access |

All secrets managed via Doppler (`doppler run --`).

## Commands

```bash
# Full deployment
doppler run -- pipx run ansible-playbook \
  playbooks/site.yml

# Validate deployment
doppler run -- pipx run ansible-playbook \
  playbooks/validate.yml

# Lint
pipx run ansible-lint
```

## Firewall

Guest firewall is **disabled**
(`splunk_docker_firewall_enabled: false`).
Proxmox firewall manages all network security
(see `terraform-proxmox/modules/firewall/`).
Docker's DNAT conflicts with guest iptables FORWARD
chain rules.

## Related Repositories

| Repo | Relationship |
| --- | --- |
| terraform-proxmox | Upstream: provisions Splunk VM |
| ansible-proxmox-apps | Peer: owns Cribl (sends to HEC) |
| ansible-proxmox | Peer: Proxmox host config |
