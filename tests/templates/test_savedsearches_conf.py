#!/usr/bin/env python3
"""
Test the hardware disk-failure alert contract in savedsearches.conf.j2.

The [hardware_smart_failure] search line is literal text in the template — no
Jinja substitution reaches it — so reading the file is equivalent to rendering
it, and needs none of the role vars the surrounding macros want.

What this guards: attributes 5 (reallocated sectors) and 197 (pending sectors)
are the counters that precede a disk dropping out of a pool, and their
NORMALIZED values sit at the ceiling long after the RAW counts start climbing.
Only the raw-value "<name> changed" lines report that transition. Drop those
phrases and the alert still exists, still runs on schedule, and still returns
zero results while sectors accumulate.

Run from repo root:
  python3 tests/templates/test_savedsearches_conf.py
"""

import re
import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent.parent
# [hardware_smart_failure] lives in the hardware-detectors fragment (see
# roles/splunk_docker/templates/savedsearches.conf.j2, which just includes it)
# since savedsearches.conf.j2 was split one-file-per-detector-group.
TEMPLATE = ROOT / "roles/splunk_docker/templates/savedsearches/09-hardware-detectors.j2"

# Phrase -> what its absence would stop detecting.
REQUIRED_PHRASES = {
    "Reallocated_Sector_Ct changed": "attribute 5 raw increase (new sectors reallocated)",
    "Current_Pending_Sector changed": "attribute 197 raw change (pending sectors)",
    "Offline_Uncorrectable changed": "attribute 198 raw change",
    "Failed SMART usage Attribute": "a tracked counter flagged critical",
    "FAILED SMART self-check": "a failed drive self-test",
    "FAILING_NOW": "an attribute crossing its failure threshold",
}

errors = []
body = TEMPLATE.read_text()

stanza = re.search(r"^\[hardware_smart_failure\]$(.*?)^\[", body, re.M | re.S)
if not stanza:
    print("FAIL: [hardware_smart_failure] stanza not found")
    sys.exit(1)

search_line = next(
    (ln for ln in stanza.group(1).splitlines() if ln.startswith("search = ")), ""
)
if not search_line:
    print("FAIL: [hardware_smart_failure] has no search line")
    sys.exit(1)

for phrase, why in REQUIRED_PHRASES.items():
    if phrase not in search_line:
        errors.append(f"FAIL: search lost {phrase!r} — stops detecting {why}")

# An alert that searches the wrong index returns zero results and reports
# success, which is indistinguishable from healthy hardware.
if "index=hardware" not in search_line:
    errors.append("FAIL: search is not scoped to index=hardware")

if errors:
    for err in errors:
        print(err)
    sys.exit(1)

print("PASS: hardware_smart_failure covers attributes 5 / 197 / 198 and self-test failure")
print("\nAll tests passed.")
