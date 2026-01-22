# Splunk Docker Role

Deploys Splunk Enterprise in a Docker container on a Proxmox VM.

## Overview

This role:

- Installs Docker and Docker Compose
- Deploys Splunk Enterprise container
- Configures custom indexes
- Installs Technology Add-ons (TAs)
- Applies firewall rules (optional)

## Requirements

- Debian-based target host
- Doppler secrets for SPLUNK_PASSWORD and SPLUNK_HEC_TOKEN
- VM provisioned by terraform-proxmox with appropriate disk space

## Role Variables

See `defaults/main.yml` for all variables. Key variables:

| Variable | Default | Description |
| -------- | ------- | ----------- |
| `splunk_docker_image` | `splunk/splunk:latest` | Splunk Docker image |
| `splunk_docker_web_port` | `8000` | Web UI port |
| `splunk_docker_hec_port` | `8088` | HEC port |
| `splunk_docker_user` | `41812` | Splunk container user UID |
| `splunk_docker_firewall_enabled` | `false` | Enable firewall rules |

## File Ownership

The Splunk container runs processes as UID 41812 (splunk user inside container).
All Splunk data directories and apps are owned by this UID to ensure proper
permissions inside the container.

## Technology Add-ons

TAs are placed in `files/` and configured in `splunk_docker_addons`:

```yaml
splunk_docker_addons:
  - name: TA-unifi-cloud
    filename: "TA-unifi-cloud-{{ splunk_docker_unifi_ta_version }}.tar"
    description: UniFi Cloud Add-on
```

## Example Playbook

```yaml
- hosts: splunk
  roles:
    - role: splunk_docker
      vars:
        splunk_docker_password: "{{ lookup('env', 'SPLUNK_PASSWORD') }}"
        splunk_docker_hec_token: "{{ lookup('env', 'SPLUNK_HEC_TOKEN') }}"
```

## Dependencies

- community.docker collection
- terraform-proxmox for VM provisioning
- Doppler for secrets management
