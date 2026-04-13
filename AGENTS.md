# Ansible Splunk - AI Agent Documentation

Ansible automation for Splunk Enterprise deployment on Proxmox VMs.

## Purpose

Deploy and configure Splunk using the `splunk_docker` role.

This repository is the **single source of truth** for Splunk configuration.

## Dependencies

### Upstream

- **terraform-proxmox**: VM provisioning (VM 200)
  - Exports `ansible_inventory` output for dynamic inventory
  - Creates VM with appropriate disk space

### External Services

- **Doppler**: Secrets for `SPLUNK_PASSWORD`, `SPLUNK_HEC_TOKEN`, `SPLUNK_MCP_TOKEN`

## Key Files

| Path | Purpose |
| --- | --- |
| `roles/splunk_docker/` | Splunk deployment role |
| `roles/splunk_docker/vars/splunkbase_apps.yml` | Splunkbase app registry |
| `roles/splunk_docker/vars/custom_addons.yml` | Custom TA definitions |
| `roles/splunk_docker/vars/mcp.yml` | MCP Server configuration |
| `roles/splunk_docker/files/` | App archives (gitignored) |
| `playbooks/site.yml` | Full deployment playbook |
| `playbooks/validate.yml` | Post-deploy validation |
| `inventory/load_terraform.yml` | Dynamic inventory loader |

## Agent Tasks

### Deployment

```bash
# Full deployment
doppler run -- ansible-playbook playbooks/site.yml

# Post-deploy validation
doppler run -- ansible-playbook playbooks/validate.yml
```

### Troubleshooting

- **Health check fails**: Check container logs with `docker logs splunk`
- **Apps not visible**: Verify ownership is UID 41812
- **HEC not working**: Confirm `SPLUNK_HEC_TOKEN` in Doppler
- **MCP Server not responding**: Create token via Splunk MCP Server config page (Settings > MCP Server), check port 8089 is accessible

### Adding Splunkbase Apps

1. Edit `roles/splunk_docker/vars/splunkbase_apps.yml` - add entry or set `enabled: true`
2. Download archive from Splunkbase and place in `roles/splunk_docker/files/`
3. Re-run `doppler run -- ansible-playbook playbooks/site.yml`

### Adding Custom Add-ons

1. Place `.tar` or `.tgz` in `roles/splunk_docker/files/`
2. Add entry to `roles/splunk_docker/vars/custom_addons.yml`
3. Re-run `doppler run -- ansible-playbook playbooks/site.yml`

## MCP Server Tools

The Splunk MCP Server provides these tools for AI agents after deployment:

| Tool | Description | Example |
| --- | --- | --- |
| `run_splunk_query` | Execute SPL searches | `` `\| makeresults \| eval test="ok"` `` |
| `get_indexes` | List all indexes | Returns 11 custom + system indexes |
| `get_sourcetypes` | List sourcetypes | Returns ingested sourcetypes |

Configure the MCP client in `~/git/nix-ai/main/modules/mcp/default.nix`.

## Secrets Management

All secrets retrieved from Doppler at runtime. Required secrets:

| Secret | Purpose |
| --- | --- |
| `SPLUNK_PASSWORD` | Admin password |
| `SPLUNK_HEC_TOKEN` | HEC token UUID (shared across all indexes) |
| `SPLUNK_MCP_TOKEN` | MCP Server Bearer token (client-side, created via Splunk UI) |
| `PROXMOX_SSH_KEY_PATH` | SSH key for VM access |

```bash
doppler run -- ansible-playbook playbooks/site.yml
```

## Related Repositories

- **terraform-proxmox**: VM provisioning and networking
- **ansible-proxmox-apps**: Other Proxmox applications (Cribl, HAProxy)
- **nix-ai**: MCP client configuration (`modules/mcp/`)
