#!/usr/bin/env python3
"""
Test the indexes.conf.j2 Jinja2 template rendering.

The template emits two [volume:*] stanzas (hot_warm, cold) followed by one
INI stanza per index with: homePath, coldPath, thawedPath,
maxTotalDataSizeMB, frozenTimePeriodInSecs.

Per-index `tier` (default "small") controls path placement:
  small (default) - homePath and coldPath both on volume:hot_warm.
  large           - homePath on volume:hot_warm with homePath.maxDataSizeMB,
                     coldPath on volume:cold.
thawedPath is always a literal $SPLUNK_DB path (Splunk rejects a volume:
reference there), regardless of tier.

Run from repo root:
  python3 tests/templates/test_indexes_conf.py
"""

import sys
from pathlib import Path

try:
    from jinja2 import Environment, FileSystemLoader
except ImportError:
    print("ERROR: jinja2 not installed. Run: pip install jinja2")
    sys.exit(1)

TEMPLATE_DIR = Path(__file__).parent.parent.parent / "roles/splunk_docker/templates"
env = Environment(loader=FileSystemLoader(str(TEMPLATE_DIR)), keep_trailing_newline=True)
template = env.get_template("indexes.conf.j2")

COMMON_VARS = {
    "splunk_docker_cold_dir": "/opt/splunk/cold",
    "splunk_docker_volume_hot_warm_max_mb": 409600,
    "splunk_docker_volume_cold_max_mb": 122880,
    "splunk_docker_frozen_archive_enabled": False,
    "splunk_docker_frozen_dir": "",
    "splunk_docker_frozen_script_path": "/opt/splunk/etc/system/local/cold_to_frozen.py",
}


def render(indexes, **overrides):
    variables = dict(COMMON_VARS)
    variables.update(overrides)
    return template.render(splunk_docker_indexes=indexes, **variables)


errors = []

# Shared fixture: representative subset of the pipeline indexes
INDEXES = [
    {"name": "unifi", "tier": "large", "home_max_size_mb": 15360, "max_size_mb": 61440,
     "frozen_time_secs": 31536000},
    {"name": "firewall", "tier": "large", "home_max_size_mb": 20480, "max_size_mb": 92160,
     "frozen_time_secs": 31536000},
    {"name": "netflow", "max_size_mb": 51200, "frozen_time_secs": 7776000},
    {"name": "dns", "max_size_mb": 10240, "frozen_time_secs": 31536000},
]

result = render(INDEXES)


def stanza_body(text, name, all_names):
    start = text.index(f"[{name}]")
    ends = [text.index(f"\n[{other}]", start + 1) for other in all_names if other != name
            if f"\n[{other}]" in text[start + 1:]]
    end = min(ends) if ends else len(text)
    return text[start:end]


# Test 1: both volume stanzas present with the right paths/caps
if "[volume:hot_warm]" not in result or "path = $SPLUNK_DB" not in result:
    errors.append("FAIL: volume:hot_warm stanza missing or wrong path")
elif f"maxVolumeDataSizeMB = {COMMON_VARS['splunk_docker_volume_hot_warm_max_mb']}" not in result:
    errors.append("FAIL: volume:hot_warm maxVolumeDataSizeMB wrong")
else:
    print("PASS: volume:hot_warm stanza rendered correctly")

if "[volume:cold]" not in result or f"path = {COMMON_VARS['splunk_docker_cold_dir']}" not in result:
    errors.append("FAIL: volume:cold stanza missing or wrong path")
elif f"maxVolumeDataSizeMB = {COMMON_VARS['splunk_docker_volume_cold_max_mb']}" not in result:
    errors.append("FAIL: volume:cold maxVolumeDataSizeMB wrong")
else:
    print("PASS: volume:cold stanza rendered correctly")

# Test 2: each index has its own INI stanza header
all_names = [idx["name"] for idx in INDEXES]
missing_stanzas = [n for n in all_names if f"[{n}]" not in result]
if missing_stanzas:
    errors.append(f"FAIL: missing stanza headers for: {missing_stanzas}")
else:
    print(f"PASS: all {len(INDEXES)} index stanza headers present")

# Test 3: small-tier indexes put both homePath and coldPath on volume:hot_warm
for idx in ("netflow", "dns"):
    body = stanza_body(result, idx, all_names)
    if f"homePath = volume:hot_warm/{idx}/db" not in body:
        errors.append(f"FAIL: small index '{idx}' homePath not on volume:hot_warm")
    if f"coldPath = volume:hot_warm/{idx}/colddb" not in body:
        errors.append(f"FAIL: small index '{idx}' coldPath not on volume:hot_warm")
    if "homePath.maxDataSizeMB" in body:
        errors.append(f"FAIL: small index '{idx}' should not emit homePath.maxDataSizeMB")
if not errors:
    print("PASS: small-tier indexes keep home+cold on volume:hot_warm")

# Test 4: large-tier indexes split home (hot_warm) from cold (cold volume)
for idx in INDEXES:
    if idx.get("tier") != "large":
        continue
    body = stanza_body(result, idx["name"], all_names)
    if f"homePath = volume:hot_warm/{idx['name']}/db" not in body:
        errors.append(f"FAIL: large index '{idx['name']}' homePath not on volume:hot_warm")
    if f"homePath.maxDataSizeMB = {idx['home_max_size_mb']}" not in body:
        errors.append(f"FAIL: large index '{idx['name']}' missing homePath.maxDataSizeMB")
    if f"coldPath = volume:cold/{idx['name']}/colddb" not in body:
        errors.append(f"FAIL: large index '{idx['name']}' coldPath not on volume:cold")
else:
    print("PASS: large-tier indexes split home (hot_warm) / cold (cold volume)")

# Test 5: thawedPath is always a literal $SPLUNK_DB path, regardless of tier
for name in all_names:
    body = stanza_body(result, name, all_names)
    if f"thawedPath = $SPLUNK_DB/{name}/thaweddb" not in body:
        errors.append(f"FAIL: thawedPath not a literal $SPLUNK_DB path for '{name}'")
else:
    print("PASS: thawedPath stays a literal $SPLUNK_DB path for every tier")

# Test 6: size and retention values are rendered correctly
value_errors = []
for idx in INDEXES:
    if f"maxTotalDataSizeMB = {idx['max_size_mb']}" not in result:
        value_errors.append(f"  maxTotalDataSizeMB wrong for '{idx['name']}'")
    if f"frozenTimePeriodInSecs = {idx['frozen_time_secs']}" not in result:
        value_errors.append(f"  frozenTimePeriodInSecs wrong for '{idx['name']}'")
if value_errors:
    errors.append("FAIL: size/retention value errors:\n" + "\n".join(value_errors))
else:
    print("PASS: maxTotalDataSizeMB and frozenTimePeriodInSecs rendered with correct values")

# Test 7: stanzas are independent — each index path uses only that index's name
for idx in all_names:
    other_names = [n for n in all_names if n != idx]
    body = stanza_body(result, idx, all_names)
    for other in other_names:
        if f"/{other}/" in body:
            errors.append(f"FAIL: stanza for '{idx}' contains path referencing '{other}'")
            break
    else:
        continue
    break
else:
    print("PASS: each index stanza references only its own paths")

# Test 8: empty index list produces no index stanzas (volume stanzas still render)
result_empty = render([])
spurious = [line for line in result_empty.splitlines()
            if line.startswith("[") and not line.startswith("[volume:")]
if spurious:
    errors.append(f"FAIL: index stanzas rendered with empty index list: {spurious}")
else:
    print("PASS: empty index list produces no index stanzas")

# Test 9: datatype = metric only for indexes flagged datatype: metric
DATATYPE_INDEXES = [
    {"name": "events_idx", "max_size_mb": 102400, "frozen_time_secs": 31536000},
    {"name": "metric_idx", "max_size_mb": 102400, "frozen_time_secs": 7776000, "datatype": "metric"},
]
result_dt = render(DATATYPE_INDEXES)
metric_stanza = result_dt[result_dt.index("[metric_idx]"):]
events_stanza = result_dt[result_dt.index("[events_idx]"):result_dt.index("[metric_idx]")]
if "datatype = metric" not in metric_stanza.split("[metric_idx]")[1].split("\n[")[0]:
    errors.append("FAIL: metric index missing 'datatype = metric'")
elif "datatype = metric" in events_stanza:
    errors.append("FAIL: event index wrongly emitted 'datatype = metric'")
else:
    print("PASS: datatype = metric emitted only for metric indexes")

# --- frozen archive -------------------------------------------------------
# coldToFrozenDir and coldToFrozenScript are mutually exclusive in Splunk, and
# when both are present Splunk silently honours the Dir and ignores the script.
# The failure mode is therefore invisible: buckets stop being uploaded and
# nothing reports an error. These cases pin the template to exactly one.
FROZEN_INDEXES = [
    {"name": "idx_a", "max_size_mb": 10240, "frozen_time_secs": 31536000},
]

frozen_off = render(FROZEN_INDEXES)
if "coldToFrozen" in frozen_off:
    errors.append("FAIL: frozen settings emitted while the archive is disabled")
else:
    print("PASS: no coldToFrozen* emitted when archive disabled and no dir set")

frozen_on = render(FROZEN_INDEXES, splunk_docker_frozen_archive_enabled=True)
if "coldToFrozenScript" not in frozen_on:
    errors.append("FAIL: coldToFrozenScript missing when the archive is enabled")
elif "coldToFrozenDir" in frozen_on:
    errors.append("FAIL: coldToFrozenDir emitted alongside coldToFrozenScript")
else:
    print("PASS: archive enabled emits coldToFrozenScript alone")

# The dangerous combination: archive on AND a dir configured. The script must
# win, because the dir would silently disable the upload.
frozen_both = render(
    FROZEN_INDEXES,
    splunk_docker_frozen_archive_enabled=True,
    splunk_docker_frozen_dir="/opt/splunk/frozen",
)
if "coldToFrozenDir" in frozen_both:
    errors.append(
        "FAIL: coldToFrozenDir emitted with the archive enabled - Splunk would "
        "prefer it and silently stop uploading"
    )
else:
    print("PASS: a configured dir cannot override the archive script")

frozen_dir_only = render(FROZEN_INDEXES, splunk_docker_frozen_dir="/opt/splunk/frozen")
if "coldToFrozenDir = /opt/splunk/frozen" not in frozen_dir_only:
    errors.append("FAIL: coldToFrozenDir not emitted when set with archive disabled")
elif "coldToFrozenScript" in frozen_dir_only:
    errors.append("FAIL: coldToFrozenScript emitted while the archive is disabled")
else:
    print("PASS: dir-only configuration emits coldToFrozenDir alone")

if errors:
    print()
    for err in errors:
        print(err)
    sys.exit(1)

print("\nAll tests passed.")
