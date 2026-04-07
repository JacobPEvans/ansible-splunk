# Splunk Docker Role

Deploys Splunk Enterprise in a Docker container on a Proxmox VM.

## Overview

This role:

- Installs Docker and Docker Compose
- Deploys Splunk Enterprise container
- Configures custom indexes
- Installs Technology Add-ons (TAs)
- Applies firewall rules (optional)

## Installation

```bash
ansible-galaxy collection install -r requirements.yml
```

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

## Usage

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

## HEC Token Setup

**1 index = 1 HEC token.** Tokens are derived deterministically via UUID v5:

```text
Token = uuidv5(HEC_NAMESPACE, "splunk-hec-<index_name>")
```

The `HEC_NAMESPACE` UUID is stored in Doppler. Any system with the namespace
can derive tokens locally — no cross-repo secret sharing needed.

### One-time Doppler Setup

```bash
# Generate a random namespace UUID (this is the ONE secret)
doppler secrets set HEC_NAMESPACE "$(uuidgen)"
```

### Adding a New Index + Token

1. Add the index to `splunk_docker_indexes` in `defaults/main.yml`
2. Run `doppler run -- ansible-playbook playbooks/site.yml` — token is auto-derived
3. Senders derive the same token locally:

```bash
python3 -c "import uuid; print(uuid.uuid5(uuid.UUID('$HEC_NAMESPACE'), 'splunk-hec-<name>'))"
```

## MCP Server Verification

The Splunk MCP Server (app 7931) enables AI agents to query Splunk directly
via the Model Context Protocol (MCP). Configure the MCP client in
`~/git/nix-ai/main/modules/mcp/default.nix`.

### Available MCP Tools

| Tool | Description |
| --- | --- |
| `run_splunk_query` | Execute SPL search queries |
| `get_indexes` | List all Splunk indexes |
| `get_sourcetypes` | List available sourcetypes |

### Verifying MCP Connection

```bash
# Check MCP Server app is installed and REST API responds
doppler run -- ansible-playbook playbooks/validate.yml

# Direct REST API test
curl -sk https://<SPLUNK_HOST_IP>:8089/services/apps/local/splunk-mcp-server \
  -u "admin:$SPLUNK_PASSWORD" | grep -o '"name">.*<'
```
