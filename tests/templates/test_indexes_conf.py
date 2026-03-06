#!/usr/bin/env python3
"""
Test the indexes.conf.j2 Jinja2 template rendering.

The template generates one INI stanza per index with five required fields:
  homePath, coldPath, thawedPath, maxTotalDataSizeMB, frozenTimePeriodInSecs

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

errors = []

# Shared fixture: representative subset of the pipeline indexes
INDEXES = [
    {"name": "unifi",    "max_size_mb": 102400, "frozen_time_secs": 31536000},
    {"name": "firewall", "max_size_mb": 102400, "frozen_time_secs": 31536000},
    {"name": "netflow",  "max_size_mb": 204800, "frozen_time_secs": 63072000},
]

result = template.render(splunk_docker_indexes=INDEXES)

# Test 1: Each index has its own INI stanza header
missing_stanzas = [idx["name"] for idx in INDEXES if f"[{idx['name']}]" not in result]
if missing_stanzas:
    errors.append(f"FAIL: missing stanza headers for: {missing_stanzas}")
else:
    print(f"PASS: all {len(INDEXES)} index stanza headers present")

# Test 2: Required path fields are rendered for every index
REQUIRED_SUFFIXES = ["/db", "/colddb", "/thaweddb"]
path_errors = []
for idx in INDEXES:
    for suffix in REQUIRED_SUFFIXES:
        expected = f"$SPLUNK_DB/{idx['name']}{suffix}"
        if expected not in result:
            path_errors.append(f"  missing '{expected}' for index '{idx['name']}'")
if path_errors:
    errors.append("FAIL: missing path fields:\n" + "\n".join(path_errors))
else:
    print("PASS: homePath/coldPath/thawedPath rendered for all indexes")

# Test 3: Size and retention values are rendered correctly
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

# Test 4: Stanzas are independent — each index path uses only that index's name
for idx in INDEXES:
    other_names = [i["name"] for i in INDEXES if i["name"] != idx["name"]]
    stanza_start = result.index(f"[{idx['name']}]")
    try:
        stanza_end = result.index("\n[", stanza_start + 1)
    except ValueError:
        stanza_end = len(result)
    stanza_body = result[stanza_start:stanza_end]
    for other in other_names:
        if f"/{other}/" in stanza_body:
            errors.append(
                f"FAIL: stanza for '{idx['name']}' contains path referencing '{other}'"
            )
            break
    else:
        continue
    break
else:
    print("PASS: each index stanza references only its own paths")

# Test 5: Empty index list produces no stanzas
result_empty = template.render(splunk_docker_indexes=[])
spurious = [line for line in result_empty.splitlines() if line.startswith("[")]
if spurious:
    errors.append(f"FAIL: stanzas rendered with empty index list: {spurious}")
else:
    print("PASS: empty index list produces no stanzas")

if errors:
    print()
    for err in errors:
        print(err)
    sys.exit(1)

print("\nAll tests passed.")
