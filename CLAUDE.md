# Ansible Splunk Enterprise

Ansible automation for Splunk Enterprise deployment on Proxmox VMs with
persistent data storage and production-grade configuration.

## Dependencies

### Infrastructure

- **terraform-proxmox**: VM provisioning with 25GB boot disk, 200GB data disk
  on /dev/sdb. Splunk installation path: /opt/splunk
- **Doppler**: Secrets vault for SPLUNK_PASSWORD, SPLUNK_HEC_TOKEN

### Disk Requirements

**Boot Disk** (25GB /dev/sda):

```text
/dev/sda → Linux boot partition
├── / (25GB) → Root filesystem for OS + Splunk binaries
```

**Data Disk** (200GB /dev/sdb):

```text
/dev/sdb → Linux filesystem
├── /opt/splunk/var/lib/splunk (200GB) → Hot/cold/thawed indexes
```

## Default Indexes

Splunk is configured with these standard indexes:

| Index | Purpose | Retention |
| --- | --- | --- |
| main | General purpose logs | 90 days |
| _internal | Splunk operations | 60 days |
| _audit | Authorization audits | 90 days |

## Deployment Commands

```bash
# Deploy Splunk Enterprise
cd ansible
uv run ansible-playbook playbooks/deploy.yml

# Configure default indexes
uv run ansible-playbook playbooks/configure_indexes.yml

# Full site deployment
uv run ansible-playbook playbooks/site.yml
```

## Required Environment Variables

- `DOPPLER_TOKEN`: Doppler service token for secrets
- `SPLUNK_VM_HOST`: Target VM hostname (inventory override)

## Architecture Notes

- Data disk mounted at /opt/splunk/var/lib/splunk via role
- HEC token stored in Doppler, retrieved via lookup
- Admin password stored in Doppler, set during deployment
- Systemd service for boot-start auto-enablement
- Index configuration is idempotent (supports rerun)

## Firewall Configuration (2026-01-22)

**Guest firewall is DISABLED** (`splunk_docker_firewall_enabled: false`)

Network security is managed by Proxmox firewall (`terraform-proxmox/modules/firewall/`).

### Why Not Guest Firewall?

Guest iptables rules conflict with Docker's networking:

1. Docker uses DNAT to forward ports (8000, 8088) to container (172.18.0.x)
2. DNATed traffic goes to iptables FORWARD chain, not INPUT
3. The old `firewall.sh` set FORWARD policy to DROP without Docker rules
4. Result: SSH worked but all Docker ports failed

### Current State

- **Guest iptables**: No Ansible-managed rules
  (`splunk_docker_firewall_enabled: false`)
- **Proxmox firewall**: Manages all inbound/outbound security
- **Docker**: Manages its own FORWARD rules for container networking

### To Re-enable Guest Firewall (NOT RECOMMENDED)

If guest firewall is needed, the template must include Docker-aware rules:

```bash
# Allow FORWARD for Docker networks.
# NOTE: The 172.18.0.0/16 subnet is an example. You may need to find the correct
# subnet for your Docker network using `docker network inspect <network_name>`.
iptables -I FORWARD -d 172.18.0.0/16 -j ACCEPT
iptables -I FORWARD -s 172.18.0.0/16 -j ACCEPT
```
