# Splunk App Files

This directory contains Splunk Technology Add-ons (TAs) and apps deployed
by the `splunk_docker` role. Files are gitignored due to size and licensing.

## Installation

Place app archives in this directory before running the playbook. Add-ons with
a `github_repo` in `vars/custom_addons.yml` are **downloaded automatically** from
GitHub Releases — no manual placement needed for those.

### Splunkbase Apps (`vars/splunkbase_apps.yml`)

Download from Splunkbase and place in this directory.

| File | App | Splunkbase ID | Enabled |
| ---- | --- | ------------- | ------- |
| `splunk-mcp-server_101.tgz` | Splunk MCP Server | [7931](https://splunkbase.splunk.com/app/7931) | Yes |
| `python-for-scientific-computing-for-linux-64-bit_430.tgz` | Python for Scientific Computing | [2882](https://splunkbase.splunk.com/app/2882) | Yes |
| `splunk-machine-learning-toolkit_550.tgz` | Machine Learning Toolkit | [2890](https://splunkbase.splunk.com/app/2890) | Yes |
| `splunk-app-for-data-science-and-deep-learning_510.tgz` | Deep Learning Toolkit (DSDL) | [4607](https://splunkbase.splunk.com/app/4607) | Yes |
| `local-ai-assistant_100.tgz` | Local AI Assistant | [8374](https://splunkbase.splunk.com/app/8374) | No |
| `ta-ollama_100.tgz` | TA-Ollama | [8024](https://splunkbase.splunk.com/app/8024) | No |
| `cimplicity-ai_100.tgz` | CIMPlicity AI | [7945](https://splunkbase.splunk.com/app/7945) | No |

To enable or disable a Splunkbase app, edit `roles/splunk_docker/vars/splunkbase_apps.yml`
and set `enabled: true` or `enabled: false` for the relevant entry.

Disabled apps are skipped at install time but remain documented in the registry.

The Deep Learning Toolkit (DSDL) is deployed **without Docker features**:

- Jupyter Lab notebooks and the core framework work normally
- TensorFlow/PyTorch container-based workloads are **not available**
- Enabling container workloads requires Docker-in-Docker on the VM (deferred)

### Custom Add-ons (`vars/custom_addons.yml`)

Internal or third-party TAs not managed via the Splunkbase app registry.

| File | Description | Source | Auto-download |
| ---- | ----------- | ------ | ------------- |
| `TA-unifi-cloud-{version}.tar` | UniFi Cloud syslog parsing | Internal build | No — place manually |
| `duck-yeah_{version}.tgz` | Splunk app packaging utilities | Internal | No — place manually |
| `splunk-db-connect_{version}.tar` | Database connectivity | Splunkbase [#2686](https://splunkbase.splunk.com/app/2686) | No — place manually |
| `VisiCore_TA_AI_Observability.spl` | VisiCore TA for AI Observability | GitHub Releases (latest) | Yes |
| `VisiCore_App_for_AI_Observability.spl` | VisiCore App for AI Observability | GitHub Releases (latest) | Yes |

Manual files (from `defaults/main.yml`):

- `TA-unifi-cloud-1.0.2+00b9ecb.tar`
- `duck-yeah_234.tgz`
- `splunk-db-connect_421.tar`

## Usage

After running the playbook, verify all archives are present:

```bash
ls -la roles/splunk_docker/files/*.{tar,tar.gz,tgz,spl} 2>/dev/null
```
