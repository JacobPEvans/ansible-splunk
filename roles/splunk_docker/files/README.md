# Splunk App Files

This directory contains Splunk Technology Add-ons (TAs) and apps deployed
by the `splunk_docker` role. Files are gitignored due to size and licensing.

## Installation

This role uses artifacts from three sources:

1. **Splunkbase apps** — downloaded in advance by `scripts/download-splunkbase-apps.sh` (run before playbook)
2. **MinIO artifact store** — downloaded during playbook run from self-hosted MinIO (`artifact_store: true`)
3. **GitHub Releases** — downloaded during playbook run from GitHub (`github_repo` field)

Only custom add-ons without either `artifact_store` or `github_repo` need manual placement.

### Splunkbase Apps (`vars/splunkbase_apps.yml`)

Downloaded automatically by `scripts/download-splunkbase-apps.sh`:

```bash
doppler run -- ./scripts/download-splunkbase-apps.sh
```

Requires `SPLUNKBASE_USERNAME` and `SPLUNKBASE_PASSWORD` from Doppler.

**Required apps** (marked `required: true`) cause deployment to fail if their archive is missing.
Verify the exact filename from Splunkbase at download time — naming conventions vary between apps.

| File | App | Splunkbase ID | Required | Enabled |
| ---- | --- | ------------- | -------- | ------- |
| `splunk-mcp-server_110.tgz` | Splunk MCP Server | [7931](https://splunkbase.splunk.com/app/7931) | Yes | Yes |
| `splunk-common-information-model-cim_850.tgz` | Common Information Model (CIM) | [1621](https://splunkbase.splunk.com/app/1621) | Yes | Yes |
| `splunk-ai-assistant-for-spl_151.tgz` | Splunk AI Assistant for SPL | [7245](https://splunkbase.splunk.com/app/7245) | Yes | Yes |
| `alerts-for-splunk-admins_407.tgz` | Alerts for Splunk Admins (SplunkAdmins) | [3796](https://splunkbase.splunk.com/app/3796) | Yes | Yes |
| `ta-alerts-for-splunkadmins_108.tgz` | TA for Splunk Admins (TA-SplunkAdmins) | [6518](https://splunkbase.splunk.com/app/6518) | Yes | Yes |
| `python-for-scientific-computing-for-linux-64-bit_431.tgz` | Python for Scientific Computing | [2882](https://splunkbase.splunk.com/app/2882) | Yes | Yes |
| `splunk-ai-toolkit_572.tgz` | Splunk AI Toolkit | [2890](https://splunkbase.splunk.com/app/2890) | Yes | Yes |
| `splunk-app-for-data-science-and-deep-learning_523.tgz` | Deep Learning Toolkit (DSDL) | [4607](https://splunkbase.splunk.com/app/4607) | Yes | Yes |
| `local-ai-assistant_100.tgz` | Local AI Assistant | [8374](https://splunkbase.splunk.com/app/8374) | No | No |
| `ta-ollama_100.tgz` | TA-Ollama | [8024](https://splunkbase.splunk.com/app/8024) | No | No |
| `cimplicity-ai_100.tgz` | CIMPlicity AI | [7945](https://splunkbase.splunk.com/app/7945) | No | No |

To enable or disable a Splunkbase app, edit `roles/splunk_docker/vars/splunkbase_apps.yml`
and set `enabled: true` or `enabled: false` for the relevant entry.

Required apps (`required: true`) cannot be disabled — deployment will fail with an actionable
error if the archive is missing or the app is disabled. Optional apps are skipped with a
warning if their archive is not present.

The Deep Learning Toolkit (DSDL) is deployed **without Docker features**:

- Jupyter Lab notebooks and the core framework work normally
- TensorFlow/PyTorch container-based workloads are **not available**
- Enabling container workloads requires Docker-in-Docker on the VM (deferred)

### Custom Add-ons (`vars/custom_addons.yml`)

Internal or third-party TAs not managed via the Splunkbase app registry.

| File | Description | Source | Auto-download |
| ---- | ----------- | ------ | ------------- |
| `TA-unifi-cloud.tar` | UniFi Cloud syslog parsing | [Splunkbase #7494](https://splunkbase.splunk.com/app/7494) | Yes — MinIO |
| `duck-yeah.tar` | Splunk app packaging utilities | [Splunkbase #7015](https://splunkbase.splunk.com/app/7015) | Yes — MinIO |
| `splunk-db-connect.tar` | Database connectivity | [Splunkbase #2686](https://splunkbase.splunk.com/app/2686) | Yes — MinIO |
| `Splunk_TA_H3_Unifi.tar` | UniFi network device TA | [Splunkbase #7935](https://splunkbase.splunk.com/app/7935) | Yes — MinIO |
| `ubiquiti-add-on-for-splunk.tar` | Ubiquiti monitoring add-on | [Splunkbase #4107](https://splunkbase.splunk.com/app/4107) | Yes — MinIO |
| `VisiCore_TA_AI_Observability.spl` | VisiCore TA for AI Observability | GitHub Releases (latest) | Yes — GitHub |
| `VisiCore_App_for_AI_Observability.spl` | VisiCore App for AI Observability | GitHub Releases (latest) | Yes — GitHub |

### MinIO Artifact Store

Custom add-ons marked `artifact_store: true` are served from a self-hosted MinIO
instance (LXC container `minio`, port 9000). The URL is constructed from the
terraform inventory at runtime. The bucket has anonymous read on the internal
network — no authentication is needed for downloads.

Filenames are **version-free** — the same name is reused across all versions.
MinIO bucket versioning retains old versions automatically on re-upload.
Object tags track `version` and `splunkbase_id` for auditability.

**Uploading a new or updated add-on:**

```bash
# One-time: configure mc CLI alias (use the MinIO host's FQDN or IP from inventory)
mc alias set homelab http://minio.<domain>:9000 $MINIO_ROOT_USER $MINIO_ROOT_PASSWORD

# Upload (strip version from filename, use the canonical object name)
mc cp ~/Downloads/splunk-db-connect_425.tar homelab/splunk-addons/splunk-db-connect.tar
mc tag set homelab/splunk-addons/splunk-db-connect.tar "version=4.2.5&splunkbase_id=2686"

# No Ansible changes needed — next playbook run gets the new version
```

## Usage

After running the playbook, verify all archives are present:

```bash
ls -la roles/splunk_docker/files/*.{tar,tgz,spl} 2>/dev/null
```
