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

Staging happens through INTENTIONALLY_ENABLED below: a named register of the
detectors a human has deliberately taken off the gate, one per wave. It is the
only way past this test, it is reviewed in the PR that adds each name, and an
entry naming a stanza that no longer renders fails too, so the register cannot
quietly accumulate holes.

The stanza set is derived entirely from the rendered output (every `[name]`
block found by regex), never from a hand-maintained list of known detectors —
a new stanza added anywhere in the template, by any author or macro, is
covered automatically. `ungated_stanzas()` is exercised twice: once against
the real render, once against a regression fixture with non-standard
`key=value` spacing, so a future stanza written without spaces around `=`
can't silently slip past the key/value regexes themselves.

Run from repo root:
  python3 tests/templates/test_cutover_gate.py
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

STANZA_RE = re.compile(r"^\[(\S+)\]$(.*?)(?=^\[|\Z)", re.M | re.S)
# \s*=\s* (not a literal " = ") so a stanza written with different spacing
# around the key/value separator is still recognized as scheduled/disabled.
ENABLED_RE = re.compile(r"^enableSched\s*=\s*1\s*$", re.M)
DISABLED_RE = re.compile(r"^disabled\s*=\s*1\s*$", re.M)


# Detectors deliberately staged live, one at a time. Each entry is a human
# decision reviewed in the PR that adds it — which is exactly the staging this
# gate exists to force. Adding a name here is the ONLY way past the gate; a
# converge cannot put one here, and every stanza not listed still has to render
# `disabled = 1`. Names are rendered stanza names ("<detector>_silence_detector"),
# not the `name:` key in splunk_docker_silence_detectors; a mismatch fails this
# test rather than silently exempting nothing.
INTENTIONALLY_ENABLED = {
    "otel_traces_silence_detector",  # staged 2026-08-06 to demonstrate fire + clear
}


def ungated_stanzas(rendered):
    """Names of every [stanza] in rendered text that is scheduled
    (enableSched = 1) but not gated disabled (disabled = 1)."""
    return [
        name
        for name, body in ((m.group(1), m.group(2)) for m in STANZA_RE.finditer(rendered))
        if ENABLED_RE.search(body) and not DISABLED_RE.search(body)
    ]


env = ansible_env(ROOT / "roles/splunk_docker/templates")
template = env.get_template("savedsearches.conf.j2")
rendered = template.render(
    splunk_docker_silence_detectors=DEFAULTS["splunk_docker_silence_detectors"],
    splunk_docker_silence_lookback_multiplier=DEFAULTS["splunk_docker_silence_lookback_multiplier"],
    splunk_docker_alert_ntfy_url=None,
    splunk_docker_alert_slack_webhook=None,
)

errors = [
    f"FAIL: [{name}] is scheduled (enableSched = 1) but not disabled — the cutover gate is off"
    for name in ungated_stanzas(rendered)
    if name not in INTENTIONALLY_ENABLED
]

# A staged name that matches no rendered stanza is a dead exemption: the
# detector was renamed or removed and the allowlist kept a hole open for a
# stanza that no longer exists. Fail on it rather than let the register rot.
all_stanzas = {m.group(1) for m in STANZA_RE.finditer(rendered)}
errors += [
    f"FAIL: INTENTIONALLY_ENABLED lists [{name}], which no rendered stanza matches — "
    "remove the entry or fix the name"
    for name in sorted(INTENTIONALLY_ENABLED - all_stanzas)
]

# Regression fixture: same bug shape, deliberately written with no spaces
# around '='. A regex anchored to the template's own " = " house style would
# silently pass this and miss a stanza formatted any other way.
fixture = "[fixture_stanza]\nenableSched=1\ndisabled=0\n"
if "fixture_stanza" not in ungated_stanzas(fixture):
    errors.append(
        "FAIL: regression case — a scheduled, ungated stanza written as "
        "'enableSched=1' / 'disabled=0' (no spaces around '=') was not caught"
    )

if errors:
    for err in errors:
        print(err)
    sys.exit(1)

print("PASS: every scheduled stanza in the rendered template is disabled (cutover gate holds); "
      "the gate also catches non-standard key=value spacing")
print("\nAll tests passed.")
