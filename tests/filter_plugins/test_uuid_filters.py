#!/usr/bin/env python3
"""
Test the uuidv5 Jinja2 filter plugin.

The filter derives deterministic HEC tokens per index:
  Token = uuidv5(HEC_NAMESPACE, "splunk-hec-<index_name>")

Run from repo root:
  python3 tests/filter_plugins/test_uuid_filters.py
"""

import re
import sys
import uuid
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from filter_plugins.uuid_filters import FilterModule  # noqa: E402

errors = []

# Test 1: FilterModule.filters() exposes the uuidv5 filter
filters = FilterModule().filters()
if "uuidv5" not in filters:
    errors.append("FAIL: 'uuidv5' not found in FilterModule.filters()")
else:
    print("PASS: FilterModule.filters() contains 'uuidv5'")

# Test 2: Deterministic — same inputs always produce the same UUID
NAMESPACE = "12345678-1234-5678-1234-567812345678"
NAME = "splunk-hec-test"

result_a = FilterModule._uuidv5(NAME, NAMESPACE)
result_b = FilterModule._uuidv5(NAME, NAMESPACE)
if result_a != result_b:
    errors.append(f"FAIL: uuidv5 is not deterministic: {result_a!r} != {result_b!r}")
else:
    print(f"PASS: uuidv5 is deterministic: {result_a}")

# Test 3: Output matches stdlib uuid.uuid5 directly
expected = str(uuid.uuid5(uuid.UUID(NAMESPACE), NAME))
if result_a != expected:
    errors.append(f"FAIL: uuidv5 result {result_a!r} != expected {expected!r}")
else:
    print(f"PASS: uuidv5 matches stdlib uuid.uuid5: {expected}")

# Test 4: Different index names produce different tokens
result_unifi = FilterModule._uuidv5("splunk-hec-unifi", NAMESPACE)
result_firewall = FilterModule._uuidv5("splunk-hec-firewall", NAMESPACE)
if result_unifi == result_firewall:
    errors.append(
        f"FAIL: different index names produced the same UUID: {result_unifi!r}"
    )
else:
    print("PASS: different index names produce different tokens")
    print(f"  unifi:    {result_unifi}")
    print(f"  firewall: {result_firewall}")

# Test 5: Output is a valid UUID v5 string (version bit = 5, variant = 8/9/a/b)
uuid_v5_pattern = re.compile(
    r"^[0-9a-f]{8}-[0-9a-f]{4}-5[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$"
)
if not uuid_v5_pattern.match(result_a):
    errors.append(f"FAIL: output {result_a!r} is not a valid UUID v5 string")
else:
    print(f"PASS: output is a valid UUID v5 string")

# Test 6: All pipeline indexes produce unique tokens (no collisions)
pipeline_indexes = ["ai", "claude", "firewall", "netflow", "network", "otel", "os", "unifi"]
tokens = {}
for idx in pipeline_indexes:
    token = FilterModule._uuidv5(f"splunk-hec-{idx}", NAMESPACE)
    if token in tokens.values():
        existing = [k for k, v in tokens.items() if v == token]
        errors.append(
            f"FAIL: collision — '{idx}' produced same token as {existing}: {token}"
        )
    tokens[idx] = token

if not any("collision" in e for e in errors):
    print(f"PASS: all {len(pipeline_indexes)} pipeline indexes produce unique tokens")

# Test 7: Invalid namespace UUID raises ValueError
try:
    FilterModule._uuidv5("splunk-hec-test", "not-a-valid-uuid")
    errors.append("FAIL: expected ValueError for invalid namespace, but none raised")
except ValueError:
    print("PASS: invalid namespace raises ValueError")

if errors:
    print()
    for err in errors:
        print(err)
    sys.exit(1)

print("\nAll tests passed.")
