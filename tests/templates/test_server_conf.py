#!/usr/bin/env python3
"""
Test the server.conf.j2 Jinja2 template rendering.

The template generates a Splunk server.conf with one conditional block:
  - When splunk_docker_allow_internet_access=false: an [applicationsManagement]
    stanza that disables Splunkbase browsing and clears DNS-timeout-causing URLs.
  - When splunk_docker_allow_internet_access=true: the stanza is omitted entirely.

Run from repo root:
  python3 tests/templates/test_server_conf.py
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
template = env.get_template("server.conf.j2")

errors = []

# Test 1: Internet access blocked → [applicationsManagement] stanza is rendered
result_blocked = template.render(splunk_docker_allow_internet_access=False)
if "[applicationsManagement]" not in result_blocked:
    errors.append("FAIL: [applicationsManagement] stanza missing when internet access is blocked")
else:
    print("PASS: [applicationsManagement] stanza present when internet access is blocked")

# Test 2: Internet access blocked → allowInternetAccess = false is set
if "allowInternetAccess = false" not in result_blocked:
    errors.append("FAIL: 'allowInternetAccess = false' missing when internet access is blocked")
else:
    print("PASS: allowInternetAccess = false rendered correctly")

# Test 3: Internet access blocked → DNS-timeout URL overrides are present (empty values)
DNS_FIELDS = ["splunkbaseAppsDumpUrl", "archivedSplunkbaseAppsDumpUrl", "updateHost"]
missing_fields = [f for f in DNS_FIELDS if f not in result_blocked]
if missing_fields:
    errors.append(f"FAIL: DNS override fields missing when blocked: {missing_fields}")
else:
    print("PASS: DNS timeout override fields present when internet access is blocked")

# Test 4: Internet access allowed → [applicationsManagement] stanza is absent
result_allowed = template.render(splunk_docker_allow_internet_access=True)
if "[applicationsManagement]" in result_allowed:
    errors.append("FAIL: [applicationsManagement] stanza rendered when internet access is allowed")
else:
    print("PASS: [applicationsManagement] stanza absent when internet access is allowed")

# Test 5: Internet access allowed → output is effectively empty (no config content)
non_empty_lines = [
    ln for ln in result_allowed.splitlines()
    if ln.strip() and not ln.strip().startswith("#")
]
if non_empty_lines:
    errors.append(
        f"FAIL: unexpected config content when internet access is allowed: {non_empty_lines}"
    )
else:
    print("PASS: no config content rendered when internet access is allowed")

if errors:
    print()
    for err in errors:
        print(err)
    sys.exit(1)

print("\nAll tests passed.")
