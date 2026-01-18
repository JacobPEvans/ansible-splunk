# Ansible Splunk Enterprise

Ansible automation for Splunk Enterprise deployment on Proxmox VMs with
persistent data storage and production-grade configuration.

## Dependencies

### Infrastructure

- **terraform-proxmox**: VM provisioning with 25GB boot disk, 200GB data disk
  on /dev/sdb. Splunk installation path: /opt/splunk
- **Doppler**: Secrets vault for SPLUNK_ADMIN_PASSWORD, SPLUNK_HEC_TOKEN

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
