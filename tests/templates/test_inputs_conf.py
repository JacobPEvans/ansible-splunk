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

# Test 3: Empty string token → stanza is skipped entirely
partial_tokens = dict(TOKENS)
partial_tokens["claude"] = ""  # empty → must be skipped
result_partial = template.render(
    splunk_docker_indexes=INDEXES, splunk_docker_hec_token_values=partial_tokens
)
if "[http://claude]" in result_partial:
    errors.append("FAIL: stanza '[http://claude]' rendered despite empty token (should be skipped)")
else:
    print("PASS: empty token → stanza is skipped")

# Test 4: No 'legacy' key → no [http://legacy] stanza
if "[http://legacy]" in result:
    errors.append("FAIL: legacy stanza rendered when 'legacy' key is absent from token dict")
else:
    print("PASS: no legacy stanza when 'legacy' token is absent")

# Test 5: Legacy token present → legacy stanza includes 'main' and all index names
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

# Test 6: No token values at all → no per-index stanzas, global [http] still present
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

# Test 7: extra_hec_indexes widens the token's allowed-index list but not its
# default index; indexes without the key keep the single-index allowlist.
extra_indexes = [
    {"name": "ai"},
    {"name": "unifi", "extra_hec_indexes": ["firewall"]},
]
extra_tokens = {
    "ai":    "aaaaaaaa-0000-5000-8000-000000000001",
    "unifi": "ffffffff-0000-5000-8000-000000000006",
}
result_extra = template.render(
    splunk_docker_indexes=extra_indexes, splunk_docker_hec_token_values=extra_tokens
)
extra_errors = []
if "indexes = unifi,firewall" not in result_extra:
    extra_errors.append("  'indexes = unifi,firewall' not rendered for extra_hec_indexes entry")
if "index = unifi" not in result_extra:
    extra_errors.append("  default 'index = unifi' missing from extra_hec_indexes stanza")
if "indexes = ai\n" not in result_extra:
    extra_errors.append("  index without extra_hec_indexes lost its single-index allowlist")
if extra_errors:
    errors.append("FAIL: extra_hec_indexes rendering errors:\n" + "\n".join(extra_errors))
else:
    print("PASS: extra_hec_indexes widens 'indexes =' while 'index =' stays the token's own")

# Test 8: explicit null and empty-list extra_hec_indexes degrade to the plain
# single-index allowlist (default([], true) must swallow None, not just undefined).
degenerate_indexes = [
    {"name": "ai", "extra_hec_indexes": None},
    {"name": "unifi", "extra_hec_indexes": []},
]
result_degenerate = template.render(
    splunk_docker_indexes=degenerate_indexes, splunk_docker_hec_token_values=extra_tokens
)
degenerate_errors = []
if "indexes = ai\n" not in result_degenerate:
    degenerate_errors.append("  null extra_hec_indexes did not degrade to 'indexes = ai'")
if "indexes = unifi\n" not in result_degenerate:
    degenerate_errors.append("  empty extra_hec_indexes did not degrade to 'indexes = unifi'")
if degenerate_errors:
    errors.append("FAIL: degenerate extra_hec_indexes handling:\n" + "\n".join(degenerate_errors))
else:
    print("PASS: null and empty extra_hec_indexes both degrade to the single-index allowlist")

if errors:
    print()
    for err in errors:
        print(err)
    sys.exit(1)

print("\nAll tests passed.")
