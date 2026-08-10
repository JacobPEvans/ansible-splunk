#!/usr/bin/env python3
"""
Guard the two generic silence-detector bugs fixed here:

1. Lookback bug: dispatch.earliest_time was a flat -7d shared by every
   detector regardless of its threshold_minutes. A host silent longer than
   the window has no row for tstats to return at all, so a host silent
   longer than 7 days was invisible to its own detector — exactly the case
   it exists to catch. Fixed by deriving the lookback from each detector's
   own threshold_minutes (guards against it silently reverting to any flat
   constant, not just the old one).

2. Flat-threshold bug: a by_host detector applied ONE threshold_minutes to
   every host on the index regardless of that host's normal logging cadence,
   so a naturally-quiet host fires continuously. Fixed by deriving each
   host's effective threshold from its own observed average inter-event gap
   (floored at threshold_minutes), with a host_overrides escape hatch.

Run from repo root:
  python3 tests/templates/test_silence_detector_cadence.py
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
DETECTORS = DEFAULTS["splunk_docker_silence_detectors"]
MULTIPLIER = DEFAULTS["splunk_docker_silence_lookback_multiplier"]

env = ansible_env(ROOT / "roles/splunk_docker/templates")
rendered = env.get_template("savedsearches.conf.j2").render(
    splunk_docker_silence_detectors=DETECTORS,
    splunk_docker_silence_lookback_multiplier=MULTIPLIER,
    splunk_docker_alert_ntfy_url=None,
    splunk_docker_alert_slack_webhook=None,
)

errors = []
by_name = {}
for stanza in re.finditer(r"^\[(\S+)\]$(.*?)(?=^\[|\Z)", rendered, re.M | re.S):
    by_name[stanza.group(1)] = stanza.group(2)

for det in DETECTORS:
    name = f"{det['name']}_silence_detector"
    body = by_name.get(name)
    if body is None:
        errors.append(f"FAIL: [{name}] not found in rendered output")
        continue

    # 1. Lookback must derive from THIS detector's own threshold, not a flat
    # constant. Assert the exact expected value so a regression to any other
    # hardcoded number (old or new) is caught, not just the specific one fixed.
    expected_lookback = f"-{det['threshold_minutes'] * MULTIPLIER}m"
    m = re.search(r"^dispatch\.earliest_time = (\S+)$", body, re.M)
    if not m or m.group(1) != expected_lookback:
        errors.append(
            f"FAIL: [{name}] dispatch.earliest_time = {m.group(1) if m else 'MISSING'}, "
            f"expected {expected_lookback} (threshold_minutes x lookback multiplier)"
        )

    # 2. by_host detectors must compare against a computed per-host threshold,
    # not the flat threshold_minutes directly.
    if det.get("by_host"):
        if "where minutes_silent > host_threshold_minutes" not in body:
            errors.append(f"FAIL: [{name}] is by_host but does not gate on host_threshold_minutes")
        if "avg_gap_minutes" not in body:
            errors.append(f"FAIL: [{name}] is by_host but computes no per-host cadence baseline")
    else:
        # Non-by_host detectors are untouched: still the flat threshold.
        expected = f"where minutes_silent > {det['threshold_minutes']}"
        if expected not in body:
            errors.append(f"FAIL: [{name}] is not by_host but lost its flat threshold comparison")

if errors:
    for err in errors:
        print(err)
    sys.exit(1)

print(f"PASS: all {len(DETECTORS)} silence detectors have a threshold-derived lookback; "
      f"by_host detectors gate on a cadence-derived per-host threshold")
print("\nAll tests passed.")
