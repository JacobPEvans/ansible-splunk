#!/usr/bin/env python3
"""
Test the inputs.conf.j2 Jinja2 template rendering.

The template generates:
  - A global [http] stanza enabling HEC
  - One [http://<index>] stanza per index that has a non-empty token
  - An optional [http://legacy] stanza when a 'legacy' token is present

Run from repo root:
  python3 tests/templates/test_inputs_conf.py
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
template = env.get_template("inputs.conf.j2")

errors = []

# Shared fixture: a representative subset of the pipeline indexes
INDEXES = [
    {"name": "ai"},
    {"name": "claude"},
    {"name": "firewall"},
    {"name": "netflow"},
]
TOKENS = {
    "ai":       "aaaaaaaa-0000-5000-8000-000000000001",
    "claude":   "bbbbbbbb-0000-5000-8000-000000000002",
    "firewall": "cccccccc-0000-5000-8000-000000000003",
    "netflow":  "dddddddd-0000-5000-8000-000000000004",
}

result = template.render(splunk_docker_indexes=INDEXES, splunk_docker_hec_token_values=TOKENS)

# Test 1: Global [http] stanza always present and enabled
if "[http]" not in result or "disabled = 0" not in result:
    errors.append("FAIL: global [http] stanza missing or not enabled")
else:
    print("PASS: global [http] stanza is present and enabled")

# Test 2: Indexes with tokens render per-index stanzas with correct token values
stanza_errors = []
for idx_name, token in TOKENS.items():
    stanza_header = f"[http://{idx_name}]"
    if stanza_header not in result:
        stanza_errors.append(f"  stanza '{stanza_header}' not rendered when token is set")
    elif f"token = {token}" not in result:
        stanza_errors.append(f"  token value missing for {idx_name}")
if stanza_errors:
    errors.append("FAIL: per-index stanza rendering errors:\n" + "\n".join(stanza_errors))
else:
    print(f"PASS: all {len(TOKENS)} per-index stanzas rendered with correct tokens")

# Test 3: Each per-index stanza routes to the correct index
routing_errors = []
for idx_name in TOKENS:
    if f"index = {idx_name}" not in result:
        routing_errors.append(f"  'index = {idx_name}' routing not found")
if routing_errors:
    errors.append("FAIL: per-index routing errors:\n" + "\n".join(routing_errors))
else:
    print(f"PASS: all {len(TOKENS)} per-index stanzas have correct index routing")

# Test 4: Empty string token → stanza is skipped entirely
partial_tokens = dict(TOKENS)
partial_tokens["claude"] = ""  # empty → must be skipped
result_partial = template.render(
    splunk_docker_indexes=INDEXES, splunk_docker_hec_token_values=partial_tokens
)
if "[http://claude]" in result_partial:
    errors.append("FAIL: stanza '[http://claude]' rendered despite empty token (should be skipped)")
else:
    print("PASS: empty token → stanza is skipped")

# Test 5: No 'legacy' key → no [http://legacy] stanza
if "[http://legacy]" in result:
    errors.append("FAIL: legacy stanza rendered when 'legacy' key is absent from token dict")
else:
    print("PASS: no legacy stanza when 'legacy' token is absent")

# Test 6: Legacy token present → legacy stanza includes 'main' and all index names
legacy_token = "eeeeeeee-0000-5000-8000-000000000005"
tokens_with_legacy = dict(TOKENS)
tokens_with_legacy["legacy"] = legacy_token
result_legacy = template.render(
    splunk_docker_indexes=INDEXES, splunk_docker_hec_token_values=tokens_with_legacy
)
if "[http://legacy]" not in result_legacy:
    errors.append("FAIL: legacy stanza not rendered when legacy token is set")
elif f"token = {legacy_token}" not in result_legacy:
    errors.append("FAIL: legacy token value not rendered in legacy stanza")
else:
    indexes_lines = [ln for ln in result_legacy.splitlines() if ln.startswith("indexes = ")]
    if not indexes_lines:
        errors.append("FAIL: no 'indexes = ' line found in legacy stanza")
    else:
        indexes_line = indexes_lines[-1]  # legacy stanza is rendered last
        missing_names = [idx["name"] for idx in INDEXES if idx["name"] not in indexes_line]
        if "main" not in indexes_line:
            errors.append(f"FAIL: 'main' missing from legacy indexes line: {indexes_line!r}")
        elif missing_names:
            errors.append(
                f"FAIL: legacy indexes line missing index names: {missing_names}\n"
                f"  Got: {indexes_line!r}"
            )
        else:
            print("PASS: legacy stanza rendered with 'main' and all index names in indexes line")

# Test 7: No token values at all → no per-index stanzas, global [http] still present
result_empty = template.render(
    splunk_docker_indexes=INDEXES, splunk_docker_hec_token_values={}
)
spurious = [idx["name"] for idx in INDEXES if f"[http://{idx['name']}]" in result_empty]
if spurious:
    errors.append(f"FAIL: per-index stanzas rendered with empty token dict: {spurious}")
elif "[http]" not in result_empty:
    errors.append("FAIL: global [http] stanza missing when token dict is empty")
else:
    print("PASS: no per-index stanzas when token dict is empty; global [http] still present")

if errors:
    print()
    for err in errors:
        print(err)
    sys.exit(1)

print("\nAll tests passed.")
