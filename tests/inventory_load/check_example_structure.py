#!/usr/bin/env python3
"""
Verify that terraform_inventory.json.example has the correct flat structure.

The terraform output is structured as:
  { "splunk_vm": { "splunk": { ... } }, "containers": {}, ... }

NOT the old incorrect structure:
  { "ansible_inventory": { "splunk_vm": { ... } } }

When loaded with `include_vars: name: terraform_data`, the correct access
path is terraform_data.splunk_vm.splunk, not terraform_data.ansible_inventory.splunk_vm.splunk.
"""

import json
import sys
from pathlib import Path

example_path = Path("inventory/terraform_inventory.json.example")

try:
    with open(example_path) as f:
        data = json.load(f)
except FileNotFoundError:
    print(f"ERROR: {example_path} not found")
    sys.exit(1)
except json.JSONDecodeError as e:
    print(f"ERROR: {example_path} is not valid JSON: {e}")
    sys.exit(1)

errors = []

if "ansible_inventory" in data:
    errors.append(
        "FAIL: 'ansible_inventory' key found at root — this is the OLD wrong structure. "
        "splunk_vm must be at the root level, not nested under ansible_inventory."
    )

if "splunk_vm" not in data:
    errors.append("FAIL: 'splunk_vm' not found at root level")
else:
    splunk_vm = data["splunk_vm"]
    if "splunk" not in splunk_vm:
        errors.append("FAIL: 'splunk' not found under splunk_vm")
    else:
        splunk = splunk_vm["splunk"]
        for field in ("ip", "hostname", "vmid", "ansible_connection"):
            if field not in splunk:
                errors.append(f"FAIL: '{field}' missing from splunk_vm.splunk")

if errors:
    for err in errors:
        print(err)
    sys.exit(1)

print("PASS: terraform_inventory.json.example has correct flat structure")
print(f"  splunk ip: {data['splunk_vm']['splunk']['ip']}")
print(f"  splunk hostname: {data['splunk_vm']['splunk']['hostname']}")
