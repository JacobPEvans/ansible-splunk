# splunk_enterprise

Ansible role for Splunk Enterprise installation and configuration on
Proxmox VMs.

## Purpose

This role automates:

- Splunk Enterprise package installation
- Boot-start configuration via systemd
- Default index creation and configuration
- HTTP Event Collector (HEC) setup
- Syslog input configuration
- Admin password configuration
- Persistent data storage on mounted disk

## Role Variables

### Service Configuration

- `splunk_admin_user`: Admin username (default: admin)
- `splunk_service_state`: Systemd state started/stopped (default: started)
- `splunk_service_enabled`: Enable on boot (default: true)

### Data Disk Configuration

- `splunk_data_disk_device`: Device path (default: /dev/sdb1)
- `splunk_data_disk_mount_path`: Mount point (default:
  /opt/splunk/var/lib/splunk)

### Index Configuration

- `splunk_indexes`: List of indexes to create with path and retention
  settings

### HEC Configuration

- `splunk_hec_port`: HEC service port (default: 8088)
- `splunk_hec_enable_ssl`: Enable SSL (default: false)
- `splunk_hec_token`: HEC authentication token (no default - required)
- `splunk_hec_default_index`: Default index for HEC (default: main)
- `splunk_hec_default_sourcetype`: Default sourcetype (default: _json)

### Syslog Configuration

- `splunk_syslog_port`: Syslog service port (default: 1514)
- `splunk_syslog_default_index`: Default index for syslog (default: main)

### Admin Password

- `splunk_admin_password`: Admin account password (no default - required)

## Dependencies

- Proxmox VM with 25GB boot disk, 200GB data disk
- Debian/Ubuntu system
- Python 3.x interpreter

## Example Playbook

```yaml
- name: Deploy Splunk Enterprise
  hosts: splunk
  roles:
    - role: splunk_enterprise
      vars:
        splunk_admin_password: "{{ admin_pass }}"
        splunk_hec_token: "{{ hec_token }}"
```

## Tasks

### install.yml

- Install Splunk Enterprise package
- Initialize Splunk binaries
- Verify installation

### configure.yml

- Enable and start systemd service
- Set admin password
- Configure boot-start

### indexes.yml

- Create default indexes
- Configure persistent storage paths
- Set retention policies

### inputs.yml

- Configure HEC input
- Configure syslog input
- Enable input services

## Handlers

### restart-splunk

Restart Splunk Enterprise service via systemd.

## Templates

### server.conf.j2

Splunk server configuration with admin user setup.

### indexes.conf.j2

Index definitions with persistent storage paths.

### inputs.conf.j2

HEC and syslog input configurations.

### web.conf.j2

Web UI configuration settings.
