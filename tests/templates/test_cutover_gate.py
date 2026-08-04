#!/usr/bin/env python3
"""
Guard the alerting cutover gate in savedsearches.conf.j2.

The app-namespace fix (tasks/main.yml) makes every scheduled search in this
template dispatchable for the first time ever. Re-enabling after months of
accumulated silent conditions is staged one detector at a time by a human, not
flipped on all at once by a converge. That means every scheduled stanza
(`enableSched = 1`) MUST render `disabled = 1` by default — this test fails
the moment any of them silently reverts to `disabled = 0` without someone
deliberately editing this test alongside it.

Run from repo root:
  python3 tests/templates/test_cutover_gate.py
"""

import re
import sys
from pathlib import Path

import yaml

try:
    from jinja2 import Environment, FileSystemLoader
except ImportError:
    print("ERROR: jinja2 not installed. Run: pip install jinja2")
    sys.exit(1)

ROOT = Path(__file__).parent.parent.parent
DEFAULTS = yaml.safe_load((ROOT / "roles/splunk_docker/defaults/main.yml").read_text())

env = Environment(
    loader=FileSystemLoader(str(ROOT / "roles/splunk_docker/templates")),
    keep_trailing_newline=True,
)
template = env.get_template("savedsearches.conf.j2")
rendered = template.render(
    splunk_docker_silence_detectors=DEFAULTS["splunk_docker_silence_detectors"],
    splunk_docker_silence_lookback_multiplier=DEFAULTS["splunk_docker_silence_lookback_multiplier"],
    splunk_docker_alert_ntfy_url=None,
    splunk_docker_alert_slack_webhook=None,
)

errors = []
for stanza in re.finditer(r"^\[(\S+)\]$(.*?)(?=^\[|\Z)", rendered, re.M | re.S):
    name, body = stanza.group(1), stanza.group(2)
    if re.search(r"^enableSched = 1$", body, re.M) and not re.search(r"^disabled = 1$", body, re.M):
        errors.append(f"FAIL: [{name}] is scheduled (enableSched = 1) but not disabled — "
                       "the cutover gate is off")

if errors:
    for err in errors:
        print(err)
    sys.exit(1)

print(f"PASS: every scheduled stanza in the rendered template is disabled (cutover gate holds)")
print("\nAll tests passed.")
