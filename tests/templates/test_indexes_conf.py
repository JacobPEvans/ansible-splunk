#!/usr/bin/env python3
"""
Test the indexes.conf.j2 Jinja2 template rendering.

Verifies that all pipeline indexes (including otel) are rendered with
correct configuration keys and values.

Run from repo root:
  python3 tests/templates/test_indexes_conf.py
"""

import sys
from pathlib import Path

try:
    from jinja2 import Environment, FileSystemLoader
except ImportError:
    print("ERROR: jinja2 is required (pip install jinja2)")
    sys.exit(1)

TEMPLATE_DIR = Path(__file__).parent.parent.parent / "roles" / "splunk_docker" / "templates"

env = Environment(loader=FileSystemLoader(str(TEMPLATE_DIR)))
template = env.get_template("indexes.conf.j2")

# Mirror defaults from roles/splunk_docker/defaults/main.yml
DEFAULT_MAX_SIZE_MB = 102400
DEFAULT_FROZEN_SECS = 31536000

PIPELINE_INDEXES = [
    "ai",
    "claude",
    "firewall",
    "netflow",
    "network",
    "otel",
    "os",
    "unifi",
]

indexes = [
    {
        "name": name,
        "max_size_mb": DEFAULT_MAX_SIZE_MB,
        "frozen_time_secs": DEFAULT_FROZEN_SECS,
    }
    for name in PIPELINE_INDEXES
]

rendered = template.render(splunk_docker_indexes=indexes)

errors = []

# Test 1: All pipeline indexes have a stanza header
for idx in PIPELINE_INDEXES:
    if f"[{idx}]" not in rendered:
        errors.append(f"FAIL: index stanza '[{idx}]' not found in indexes.conf output")
    else:
        print(f"PASS: stanza '[{idx}]' present")

# Test 2: Each index has the required configuration keys
required_keys = [
    "homePath",
    "coldPath",
    "thawedPath",
    "maxTotalDataSizeMB",
    "frozenTimePeriodInSecs",
]
for key in required_keys:
    if key not in rendered:
        errors.append(f"FAIL: required key '{key}' not found in any stanza")
    else:
        print(f"PASS: key '{key}' present in output")

# Test 3: otel index is specifically present (gap in molecule/default/verify.yml)
if "[otel]" not in rendered:
    errors.append("FAIL: otel index stanza missing — not covered by molecule verify")
else:
    print("PASS: otel index rendered (not checked in molecule verify)")

# Test 4: Size and retention values match defaults
if str(DEFAULT_MAX_SIZE_MB) not in rendered:
    errors.append(f"FAIL: expected maxTotalDataSizeMB={DEFAULT_MAX_SIZE_MB} not found")
else:
    print(f"PASS: maxTotalDataSizeMB={DEFAULT_MAX_SIZE_MB} present")

if str(DEFAULT_FROZEN_SECS) not in rendered:
    errors.append(f"FAIL: expected frozenTimePeriodInSecs={DEFAULT_FROZEN_SECS} not found")
else:
    print(f"PASS: frozenTimePeriodInSecs={DEFAULT_FROZEN_SECS} present")

# Test 5: Each index has its own homePath with the index name
for idx in PIPELINE_INDEXES:
    if f"$SPLUNK_DB/{idx}/db" not in rendered:
        errors.append(f"FAIL: homePath for '{idx}' not found")

if not any("homePath" in err for err in errors):
    print(f"PASS: all {len(PIPELINE_INDEXES)} indexes have correct homePath")

# Test 6: No extra/unexpected indexes from empty input
empty_rendered = template.render(splunk_docker_indexes=[])
if "[" in empty_rendered.strip():
    errors.append("FAIL: empty indexes list produced unexpected stanza headers")
else:
    print("PASS: empty indexes list produces no stanza headers")

if errors:
    print()
    for err in errors:
        print(err)
    sys.exit(1)

print("\nAll tests passed.")
