# Ansible Splunk Enterprise

[![Lint](https://github.com/JacobPEvans/ansible-splunk/actions/workflows/lint.yml/badge.svg)](https://github.com/JacobPEvans/ansible-splunk/actions/workflows/lint.yml)
[![Molecule](https://github.com/JacobPEvans/ansible-splunk/actions/workflows/molecule.yml/badge.svg)](https://github.com/JacobPEvans/ansible-splunk/actions/workflows/molecule.yml)
[![Validate](https://github.com/JacobPEvans/ansible-splunk/actions/workflows/validate.yml/badge.svg)](https://github.com/JacobPEvans/ansible-splunk/actions/workflows/validate.yml)

Comprehensive Ansible automation for Splunk Enterprise deployment and
configuration on Proxmox VMs.

## Purpose and Scope

This repository provides production-grade Ansible playbooks and roles to
deploy Splunk Enterprise across Proxmox virtual machines. It automates:

- Splunk Enterprise installation and initialization
- Index configuration with persistent data storage
- HTTP Event Collector (HEC) configuration for log ingestion
- Syslog input configuration (backup ingestion path)
- Admin account setup with Doppler secrets
- Systemd boot-start service enablement
- Cold storage configuration on dedicated data disk

## Dependencies

### External Services

- **terraform-proxmox**: VMs must be provisioned via
  [terraform-proxmox](https://github.com/user/terraform-proxmox) with 25GB
  boot disk and 200GB data disk
- **Doppler**: Secrets stored in Doppler vault with `SPLUNK_PASSWORD`
  and `SPLUNK_HEC_TOKEN`

### Ansible Collections

```yaml
ansible.builtin:     Core Ansible functionality
ansible.posix:       POSIX system modules
community.general:   General utilities
```

Install dependencies:

```bash
uv run ansible-galaxy collection install -r requirements.yml
```

## Quick Start

### Option A: Dynamic Inventory (Recommended)

Use Terraform outputs for automatic inventory management:

1. **Sync Terraform inventory:**

   ```bash
   ./scripts/sync-terraform-inventory.sh
   ```

2. **Deploy with Doppler secrets:**

   ```bash
   doppler run -- uv run ansible-playbook playbooks/site.yml
   ```

3. **Configure indexes:**

   ```bash
   doppler run -- uv run ansible-playbook playbooks/configure_indexes.yml
   ```

4. **Validate deployment:**

   ```bash
   doppler run -- uv run ansible-playbook playbooks/validate.yml
   ```

### Option B: Static Inventory (Fallback)

For manual inventory configuration:

1. **Set environment variables:**

   ```bash
   export SPLUNK_VM_HOST="splunk.example.com"
   ```

2. **Deploy with Doppler secrets:**

   ```bash
   doppler run -- uv run ansible-playbook playbooks/deploy.yml
   doppler run -- uv run ansible-playbook playbooks/configure_indexes.yml
   ```

## Doppler Secrets Setup

This project uses Doppler for secrets management. The following secrets must
be configured in your Doppler project:

| Secret Name              | Description                      |
|--------------------------|----------------------------------|
| `SPLUNK_PASSWORD`        | Splunk admin account password    |
| `SPLUNK_HEC_TOKEN`       | HTTP Event Collector token UUID  |

### Setting Up Secrets

```bash
# Set Splunk admin password
doppler secrets set SPLUNK_PASSWORD "your-secure-password"

# Set HEC token (generate a UUID)
doppler secrets set SPLUNK_HEC_TOKEN "$(uuidgen)"
```

### Running Playbooks

Always run playbooks with `doppler run --` to inject secrets:

```bash
doppler run -- uv run ansible-playbook playbooks/deploy.yml
```

## Testing

### Syntax Validation

```bash
uv run ansible-playbook playbooks/deploy.yml --syntax-check
uv run ansible-playbook playbooks/validate.yml --syntax-check
```

### Linting

```bash
uv run yamllint .
uv run ansible-lint playbooks/ roles/
```

### Molecule Tests

Run the full test suite:

```bash
uv run molecule test
```

Run individual stages:

```bash
uv run molecule converge  # Create and configure test container
uv run molecule verify    # Run verification tests
uv run molecule destroy   # Clean up
```

### Deployment Validation

After deploying to a real VM, validate the deployment:

```bash
doppler run -- uv run ansible-playbook playbooks/validate.yml
```

## Disk Layout

### Boot Disk (25GB at /dev/sda)

```text
/dev/sda1 → /               (root filesystem)
            ├── /opt        (Splunk app files)
            ├── /etc        (Splunk configuration)
            └── /var/log    (System logs)
```

### Data Disk (200GB at /dev/sdb)

```text
/dev/sdb1 → /opt/splunk/var/lib/splunk
            ├── main/
            │   ├── db/        (hot data)
            │   ├── colddb/    (cold data)
            │   └── thaweddb/  (thawed data)
            ├── _internal/
            │   ├── db/
            │   ├── colddb/
            │   └── thaweddb/
            ├── _audit/
            │   ├── db/
            │   ├── colddb/
            │   └── thaweddb/
            └── [other indexes...]
```

## Index Retention Policy

All indexes configured with:

- **Maximum data size**: auto_high_volume for main index (rollover on size)
- **Frozen time period**: 7776000 seconds (90 days)
- **Home path**: `/opt/splunk/var/lib/splunk/<index>/db`
- **Cold path**: `/opt/splunk/var/lib/splunk/<index>/colddb`
- **Thawed path**: `/opt/splunk/var/lib/splunk/<index>/thaweddb`

Data retention timeline:

1. **Hot**: Actively written to (newest data)
2. **Warm**: Recently closed buckets
3. **Cold**: Buckets after 90-day threshold
4. **Frozen**: Deleted after retention period

## Default Indexes

Splunk Enterprise is configured with these standard indexes:

- **main**: Primary index for general purpose logs
- **_internal**: Splunk internal operations and metrics
- **_audit**: Authorization, configuration change audits
- **_telemetry**: Performance telemetry (if enabled)

## HEC Input Configuration

HTTP Event Collector is configured on:

- **Port**: 8088
- **Token**: Retrieved from Doppler (`SPLUNK_HEC_TOKEN`)
- **SSL**: Disabled (internal network, Cribl Edge handles encryption)
- **Default index**: main
- **Sourcetype**: _json (recommended for Cribl Edge)

## Syslog Input Configuration

Backup syslog input configured on:

- **Port**: 1514
- **Protocol**: UDP
- **Default index**: main
- **Sourcetype**: syslog

Use this input if Cribl Edge connection fails. Configure log forwarders:

```text
[tcpout:default]
server = splunk-host:1514
```

## Playbook Directory

### playbooks/site.yml

Main site playbook that orchestrates all deployment plays. Automatically loads
dynamic inventory from Terraform outputs.

### playbooks/deploy.yml

Core deployment playbook:

- Install Splunk Enterprise 9.x
- Configure boot-start via systemd
- Mount data disk at /opt/splunk/var/lib/splunk
- Set admin password from Doppler
- Enable HEC and syslog inputs

### playbooks/configure_indexes.yml

Index configuration playbook:

- Create default indexes with persistent storage
- Configure retention policies
- Set cold storage paths
- Validate index configuration

### playbooks/validate.yml

Validation playbook to verify deployment:

- Check Splunk service is running
- Verify boot-start is enabled
- Confirm data disk is mounted
- Test HEC and syslog ports are listening
- Check web interface accessibility

## Role Structure

### roles/splunk_enterprise

Main Splunk Enterprise role with modular tasks:

- **tasks/install.yml**: Package installation and initialization
- **tasks/configure.yml**: Service and boot configuration
- **tasks/indexes.yml**: Index creation and configuration
- **tasks/inputs.yml**: HEC and syslog input setup
- **templates/**: Jinja2 configuration templates
- **handlers/**: Service restart handlers

## Playbook Variables

Override defaults in `group_vars/splunk.yml`:

```yaml
# Service configuration
splunk_admin_user: admin
splunk_service_state: started
splunk_service_enabled: true

# Index configuration
splunk_indexes:
  - name: main
    data_disk_path: /opt/splunk/var/lib/splunk/main
    max_data_size: auto_high_volume
    frozen_time_secs: 7776000

# HEC configuration
splunk_hec_port: 8088
splunk_hec_enable_ssl: false
splunk_hec_default_sourcetype: _json
splunk_hec_default_index: main

# Syslog configuration
splunk_syslog_port: 1514
splunk_syslog_default_index: main
```

## Troubleshooting

### Splunk Service Not Starting

Check systemd status:

```bash
systemctl status Splunkd
journalctl -u Splunkd -n 50
```

### Missing Environment Variables

If you see "SPLUNK_PASSWORD and SPLUNK_HEC_TOKEN environment variables
must be set", ensure you're running with Doppler:

```bash
doppler run -- uv run ansible-playbook playbooks/deploy.yml
```

### HEC Token Not Working

Verify the token is set in Doppler:

```bash
doppler secrets get SPLUNK_HEC_TOKEN
```

Reload Splunk after configuration changes:

```bash
/opt/splunk/bin/splunk restart
```

### Data Disk Not Mounted

Check mount status:

```bash
mount | grep /opt/splunk/var/lib/splunk
df -h /opt/splunk/var/lib/splunk
```

Format and mount manually:

```bash
mkfs.ext4 /dev/sdb1
mkdir -p /opt/splunk/var/lib/splunk
mount /dev/sdb1 /opt/splunk/var/lib/splunk
```

### Terraform Inventory Not Found

If dynamic inventory fails, ensure you've synced from Terraform:

```bash
./scripts/sync-terraform-inventory.sh
```

Check the inventory file exists:

```bash
cat inventory/terraform_inventory.json
```

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for development setup, testing
guidelines, and contribution workflow.

## Changelog

See [CHANGELOG.md](CHANGELOG.md) for version history and release notes.

## License

This playbook set is licensed under the MIT License.
