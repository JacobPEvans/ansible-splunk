# Splunk App Files

This directory contains Splunk Technology Add-ons (TAs) and apps deployed
by the `splunk_docker` role. Files are gitignored due to size and licensing.

## Installation

There are three download sources, all handled automatically:

1. **Splunkbase apps** — downloaded by `scripts/download-splunkbase-apps.sh` (run before playbook)
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
| `TA-unifi-cloud-{version}.tar` | UniFi Cloud syslog parsing | Internal build | Yes — MinIO |
| `duck-yeah_{version}.tar` | Splunk app packaging utilities | Internal | Yes — MinIO |
| `splunk-db-connect_{version}.tar` | Database connectivity | Splunkbase [#2686](https://splunkbase.splunk.com/app/2686) | Yes — MinIO |
| `Splunk_TA_H3_Unifi.tar` | UniFi network device TA | Third-party | Yes — MinIO |
| `ubiquiti-add-on-for-splunk_{version}.tar` | Ubiquiti monitoring add-on | Splunkbase [#3504](https://splunkbase.splunk.com/app/3504) | Yes — MinIO |
| `VisiCore_TA_AI_Observability.spl` | VisiCore TA for AI Observability | GitHub Releases (latest) | Yes — GitHub |
| `VisiCore_App_for_AI_Observability.spl` | VisiCore App for AI Observability | GitHub Releases (latest) | Yes — GitHub |

### MinIO Artifact Store

Custom add-ons marked `artifact_store: true` are served from a self-hosted MinIO
instance at `http://10.0.1.107:9000/splunk-addons/`. The bucket has anonymous read
on the internal network — no authentication is needed for downloads.

**Uploading a new add-on or version:**

```bash
# One-time: configure mc CLI alias
mc alias set homelab http://10.0.1.107:9000 $MINIO_ROOT_USER $MINIO_ROOT_PASSWORD

# Upload
mc cp ~/Downloads/splunk-db-connect_425.tar homelab/splunk-addons/

# Then update the version pin in defaults/main.yml
```

## Usage

After running the playbook, verify all archives are present:

```bash
ls -la roles/splunk_docker/files/*.{tar,tgz,spl} 2>/dev/null
```
