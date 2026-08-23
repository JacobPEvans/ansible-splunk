#!/usr/bin/env python3
"""
Guard saved-search safety invariants in savedsearches.conf.j2.

Replaces test_cutover_gate.py, retired 2026-08-23 when the staged
disabled-by-default cutover gate it enforced was lifted (operator decision:
enable every detector at once and tune from real firing data instead of
staging one at a time). That test's invariant is gone by design -- deleting
it outright would have left this file enforcing NOTHING about these stanzas,
and the same audit that lifted the gate found several detectors pointed at
indexes with zero events ever. This test keeps the invariants that audit
actually verified true for all 33 detectors it touched:

1. Every scheduled stanza (enableSched = 1) throttles its own notification
   rate with `alert.suppress = 1` plus a non-empty `alert.suppress.period`.
   Without it, a detector on a `*/5 * * * *` cron over a noisy or
   structurally-empty index is a pager storm, not a signal -- see
   hardware_smart_failure (real disk, ~563 matches/7d) and the several
   detectors now firing "(no hosts reporting)" every cron cycle.
2. Every splunk_docker_silence_detectors list entry declares `disabled`
   explicitly rather than relying on the `| default(0)` in the template, so
   intent is never ambiguous from reading the list alone.

Run from repo root:
  python3 tests/templates/test_savedsearch_invariants.py
"""

import re
import sys
from pathlib import Path

from _defaults_loader import load_defaults

from _render_env import ansible_env

try:
    from jinja2 import Environment, FileSystemLoader
except ImportError:
    print("ERROR: jinja2 not installed. Run: pip install jinja2")
    sys.exit(1)

ROOT = Path(__file__).parent.parent.parent
DEFAULTS = load_defaults(ROOT)

# Same stanza-block extraction as the other savedsearches tests.
STANZA_RE = re.compile(r"^\[(\S+)\]$(.*?)(?=^\[|\Z)", re.M | re.S)
ENABLED_RE = re.compile(r"^enableSched\s*=\s*1\s*$", re.M)
SUPPRESS_ON_RE = re.compile(r"^alert\.suppress\s*=\s*1\s*$", re.M)
SUPPRESS_PERIOD_RE = re.compile(r"^alert\.suppress\.period\s*=\s*\S+\s*$", re.M)

env = ansible_env(ROOT / "roles/splunk_docker/templates")
template = env.get_template("savedsearches.conf.j2")
rendered = template.render(
    splunk_docker_silence_detectors=DEFAULTS["splunk_docker_silence_detectors"],
    splunk_docker_silence_lookback_multiplier=DEFAULTS["splunk_docker_silence_lookback_multiplier"],
    splunk_docker_alert_ntfy_url=None,
    splunk_docker_alert_slack_webhook=None,
)

errors = []

for name, body in ((m.group(1), m.group(2)) for m in STANZA_RE.finditer(rendered)):
    if not ENABLED_RE.search(body):
        continue
    if not SUPPRESS_ON_RE.search(body):
        errors.append(f"FAIL: [{name}] is scheduled but has no alert.suppress = 1")
    elif not SUPPRESS_PERIOD_RE.search(body):
        errors.append(f"FAIL: [{name}] has alert.suppress = 1 but no alert.suppress.period")

for det in DEFAULTS["splunk_docker_silence_detectors"]:
    if "disabled" not in det:
        errors.append(
            f"FAIL: splunk_docker_silence_detectors entry '{det.get('name', '?')}' has no "
            "explicit 'disabled' key (relies on the template's implicit default)"
        )

if errors:
    for err in errors:
        print(err)
    sys.exit(1)

print(
    "PASS: every scheduled stanza suppresses its own notification rate "
    "(alert.suppress = 1 with a period), and every silence-detector list "
    "entry declares 'disabled' explicitly"
)
print("\nAll tests passed.")
