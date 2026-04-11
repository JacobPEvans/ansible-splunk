# Splunk App Files (gitignored, runtime-only)

This directory is gitignored. The `splunk_docker` role does **not** stage
archives here — every add-on is pulled by the Splunk VM directly from MinIO
(or GitHub Releases) via `ansible.builtin.unarchive` with `remote_src: true`.

## Installation

No manual installation is required — add-ons are installed by running the
`splunk_docker` role:

```bash
doppler run -- ansible-playbook playbooks/site.yml
```

The role reads `../vars/addons.yml` and, for each entry, issues an
`ansible.builtin.unarchive` against the target Splunk VM. The VM downloads
the archive directly from MinIO (or GitHub) and extracts it into
`/opt/splunk/etc/apps/`. The `creates:` guard skips any app whose target
directory already exists.

## Usage

### Registry

Every installed add-on is listed in `../vars/addons.yml`. Each entry has:

- `filename` — archive name in the MinIO `splunk-addons` bucket or GitHub release asset
- `app_dir` — extracted directory name under `/opt/splunk/etc/apps/` (used by `creates:` for idempotency and by `validate.yml` to assert installation)
- `github_repo` — optional. If set, download from `github.com/<repo>/releases/latest`; otherwise download from MinIO.

### Adding / rotating an add-on

```bash
# Upload with a version-free filename
mc cp ~/Downloads/splunk-db-connect_425.tar homelab/splunk-addons/splunk-db-connect.tar

# Tag with the version (and any other metadata you want searchable)
mc tag set homelab/splunk-addons/splunk-db-connect.tar "version=4.2.5"

# If this is a new add-on, also add an entry to vars/addons.yml.
# Nothing else. The Splunk VM pulls from MinIO on the next playbook run.
```

To force re-extraction after rotating a file with the same name, delete the
target `app_dir` (`ssh splunk "rm -rf /opt/splunk/etc/apps/<app_dir>"`) so
the `creates:` guard lets `unarchive` run again.

### Bulk upload

```bash
for f in ~/Downloads/*.tar; do
  base=$(basename "$f")
  # strip _NNN or -X.Y.Z version suffix before the extension
  stripped=$(echo "$base" | sed -E 's/([_-][0-9]+([.+][0-9a-z]+)*)(\.(tar|tgz|spl))$/\3/')
  mc cp "$f" "homelab/splunk-addons/$stripped"
done
```
