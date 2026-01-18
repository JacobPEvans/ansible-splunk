# Ansible Splunk Enterprise

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
- **Doppler**: Secrets stored in Doppler vault with SPLUNK_ADMIN_PASSWORD
  and SPLUNK_HEC_TOKEN

### Ansible Collections

```yaml
ansible.builtin:     Core Ansible functionality
ansible.posix:       POSIX system modules
community.general:   General utilities
```

Install dependencies:

```bash
cd ansible
uv run ansible-galaxy collection install -r requirements.yml
```

## Quick Start

### 1. Set Doppler Authentication

```bash
export DOPPLER_TOKEN="your-doppler-token"
```

### 2. Configure Target Host

```bash
export SPLUNK_VM_HOST="splunk.example.com"
```

### 3. Update Inventory

Edit `inventory/hosts.yml` to set the target VM hostname:

```yaml
splunk:
  hosts:
    splunk-01:
      ansible_host: "{{ lookup('env', 'SPLUNK_VM_HOST') }}"
      ansible_user: root
```

### 4. Deploy Splunk Enterprise

```bash
cd ansible
uv run ansible-playbook playbooks/deploy.yml
```

### 5. Configure Default Indexes

```bash
uv run ansible-playbook playbooks/configure_indexes.yml
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
- **Token**: Retrieved from Doppler (SPLUNK_HEC_TOKEN)
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

Main site playbook that orchestrates all deployment plays.

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
systemctl status splunk
journalctl -u splunk -n 50
```

### HEC Token Not Working

Verify token from Doppler:

```bash
echo $DOPPLER_TOKEN
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

## License

This playbook set is licensed under the MIT License.
