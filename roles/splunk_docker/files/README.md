# Splunk Add-on Files

This directory contains Splunk Technology Add-ons (TAs) and apps that are
deployed by the `splunk_docker` role. Due to their size, these files are
not stored in git.

## Required Files

The following files must be placed in this directory before running the
playbook:

| File | Description | Source |
| ---- | ----------- | ------ |
| `TA-unifi-cloud-{version}.tar` | UniFi Cloud Add-on | Internal build |
| `duck-yeah_{version}.tgz` | Duck Yeah Splunk app | Splunkbase |

## File Versions

Current expected versions (from `defaults/main.yml`):

- `TA-unifi-cloud-1.0.2+00b9ecb.tar`
- `duck-yeah_234.tgz`

## Obtaining Files

### TA-unifi-cloud

This is an internal add-on. Contact the infrastructure team for the file.

### Duck Yeah

Download from Splunkbase or internal artifact repository.

## Verification

After placing files, verify the playbook can find them:

```bash
ls -la roles/splunk_docker/files/
```

Expected output should show both `.tar` and `.tgz` files.
