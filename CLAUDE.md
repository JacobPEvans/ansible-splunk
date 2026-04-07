# Ansible Splunk Enterprise

Deploy and configure Splunk Enterprise on a Proxmox VM.

## Container Strategy: Docker (Exception)

Splunk runs in Docker on a dedicated VM (VMID 200) — this is a deliberate
exception to the global LXC-first rule (see `~/git/CLAUDE.md` Container
Deployment Rules).

**Why Docker:** This repository standardizes on Splunk Enterprise via the
official `splunk/splunk` Docker image. Native Linux package and tarball
installs exist, but they are out of scope here. The `splunk_docker` role
manages the container lifecycle via Docker Compose.

**Implication:** New features and integrations target Docker Compose on
the Splunk VM. Do not propose LXC migration or new Docker containers
for ancillary services — those belong in `ansible-proxmox-apps` as LXC.

## This Repo Owns

- Splunk Enterprise container deployment (Docker Compose on Proxmox VM)
- HEC (HTTP Event Collector) configuration
- Custom index creation and retention
- Technology Add-ons (TAs) and Splunkbase apps
- MCP Server integration (app 7931)

## Critical Constraints

- **Firewall disabled**: Guest firewall is off
  (`splunk_docker_firewall_enabled: false`). Docker DNAT conflicts with
  iptables FORWARD chain. Proxmox firewall is sole network security
  (see `~/git/terraform-proxmox/main/modules/firewall/`).
- **HEC tokens**: Deterministic via
  `uuidv5(HEC_NAMESPACE, "splunk-hec-<index_name>")`.
  One index = one token. Namespace UUID stored in Doppler.
- **HEC transport**: HTTPS (Splunk Docker image default, SSL enabled).
- **Secrets**: All via Doppler (`doppler run --`).

## Sources of Truth

| What | Where |
| --- | --- |
| Index definitions | `roles/splunk_docker/defaults/main.yml` |
| Splunkbase apps | `roles/splunk_docker/vars/splunkbase_apps.yml` |
| Custom add-ons | `roles/splunk_docker/vars/custom_addons.yml` |
| Inventory | `inventory/load_terraform.yml` |
| Pipeline architecture | `~/git/CLAUDE.md` |
| App files and downloads | `roles/splunk_docker/files/README.md` |
| HEC setup and MCP verification | `roles/splunk_docker/README.md` |

## Commands

```bash
# Full deployment
doppler run -- ansible-playbook playbooks/site.yml

# Validate deployment
doppler run -- ansible-playbook playbooks/validate.yml

# Lint
ansible-lint
```

## Artifact Store (MinIO)

Custom add-ons that cannot be downloaded from Splunkbase or GitHub
are served from a self-hosted MinIO instance (LXC VMID 107, `10.0.1.107:9000`).

- Bucket: `splunk-addons` (anonymous read on internal network)
- Add-ons with `artifact_store: true` in `vars/custom_addons.yml` auto-download
- Upload new versions via `mc cp` — filenames are version-free, versions tracked via MinIO object tags
- See `roles/splunk_docker/files/README.md` for upload instructions

## Related Repositories

| Repo | Relationship |
| --- | --- |
| terraform-proxmox | Upstream: provisions Splunk VM + MinIO LXC |
| ansible-proxmox-apps | Peer: owns Cribl (sends to HEC), deploys MinIO |
| ansible-proxmox | Peer: Proxmox host config |
