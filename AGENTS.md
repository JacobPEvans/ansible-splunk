# Ansible Splunk - AI Agent Documentation

Ansible automation for Splunk Enterprise deployment on Proxmox VMs.

## Purpose

Deploy and configure Splunk Enterprise using either:

- **Docker-based**: `splunk_docker` role (containerized, recommended)
- **Direct install**: `splunk_enterprise` role (bare metal)

This repository is the **single source of truth** for Splunk configuration.
Splunk-related code was consolidated here from `ansible-proxmox-apps`.

## Dependencies

### Upstream

- **terraform-proxmox**: VM provisioning (VM 200)
  - Exports `ansible_inventory` output for dynamic inventory
  - Creates VM with appropriate disk space

### External Services

- **Doppler**: Secrets for SPLUNK_PASSWORD, SPLUNK_HEC_TOKEN

## Key Files

| Path | Purpose |
| ---- | ------- |
| `roles/splunk_docker/` | Docker-based Splunk deployment |
| `roles/splunk_enterprise/` | Direct Splunk installation |
| `playbooks/deploy_docker.yml` | Main Docker deployment playbook |
| `inventory/load_terraform.yml` | Dynamic inventory loader |
| `inventory/terraform.yml` | Terraform inventory plugin config |

## Agent Tasks

### Deployment

1. Sync Terraform inventory: `./scripts/sync-terraform-inventory.sh`
2. Deploy Splunk: `doppler run -- uv run ansible-playbook playbooks/deploy_docker.yml`

### Troubleshooting

- **Health check fails**: Check container logs with `docker logs splunk`
- **Apps not visible**: Verify ownership is UID 41812
- **HEC not working**: Confirm SPLUNK_HEC_TOKEN in Doppler

### Adding Technology Add-ons

1. Place `.tar` or `.tgz` files in `roles/splunk_docker/files/`
2. Update `splunk_docker_addons` in `defaults/main.yml`
3. Re-run playbook

## Secrets Management

All secrets are retrieved from Doppler at runtime:

```bash
doppler run -- uv run ansible-playbook playbooks/deploy_docker.yml
```

Never store secrets in git. Required Doppler secrets:

- `SPLUNK_PASSWORD`: Admin password
- `SPLUNK_HEC_TOKEN`: HTTP Event Collector token

## Related Repositories

- **terraform-proxmox**: VM provisioning and networking
- **ansible-proxmox-apps**: Other Proxmox applications (Cribl, HAProxy)
