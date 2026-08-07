#!/usr/bin/env python3
"""
Guard against a stanza rendering with no `search` at all.

This is not hypothetical. A Jinja comment written with whitespace control on
both sides (`{#- ... -#}`) strips the newline BEFORE and AFTER itself. Placed
between two keys it welds them together, so:

    description = ...missing row.
    {#- explanatory comment -#}
    search = | makeresults ...

rendered as a single `description = ...missing row.search = | makeresults ...`
line. Splunk accepted the file, the stanza appeared in savedsearches.conf, the
report was dispatchable, and `| savedsearch llm_surface_freshness` returned
HTTP 200 with ZERO ROWS. Nothing errored anywhere: not the render, not the
converge, not the search. It reached the live instance and was only caught by
reading the deployed value back.

That is why this test asserts on the RENDERED text rather than the template
source, and why it checks for a missing key rather than for the specific
comment syntax — the next instance of this will be some other construct that
eats a newline, and a check pinned to `{#- -#}` would miss it.

Every check below is exercised against a fixture that must FAIL it, because a
check that cannot fail is indistinguishable from one that passes.

Run from repo root:
  python3 tests/templates/test_savedsearches_render.py
"""

import re
import sys
from pathlib import Path

import yaml

from _render_env import ansible_env

try:
    from jinja2 import Environment, FileSystemLoader
except ImportError:
    print("ERROR: jinja2 not installed. Run: pip install jinja2")
    sys.exit(1)

ROOT = Path(__file__).parent.parent.parent
DEFAULTS = yaml.safe_load((ROOT / "roles/splunk_docker/defaults/main.yml").read_text())

STANZA_RE = re.compile(r"^\[(\S+)\]$(.*?)(?=^\[|\Z)", re.M | re.S)
# A key line, allowing any spacing around '='. Continuation lines (previous
# line ends in a backslash) are values, not keys, and are skipped below.
KEY_RE = re.compile(r"^([A-Za-z_][\w.]*)\s*=\s*(.*)$")

# Stanzas that legitimately carry no `search` key. Empty today; an entry here
# is a deliberate, reviewed exemption, same contract as the cutover gate's
# register.
NO_SEARCH_EXPECTED: set = set()


def stanza_keys(body):
    """Map key -> value for one stanza body, honouring backslash continuations.

    A continuation line belongs to the previous key's value; treating it as a
    key line would invent keys out of search fragments such as `| eval x=...`.
    """
    keys, pending = {}, None
    for line in body.splitlines():
        if pending is not None:
            keys[pending] += "\n" + line
            pending = pending if line.rstrip().endswith("\\") else None
            continue
        m = KEY_RE.match(line)
        if m:
            keys[m.group(1)] = m.group(2)
            if m.group(2).rstrip().endswith("\\"):
                pending = m.group(1)
    return keys


def missing_search(text):
    """Names of stanzas with no `search` key, or one whose value is empty."""
    out = []
    for m in STANZA_RE.finditer(text):
        name, keys = m.group(1), stanza_keys(m.group(2))
        if name in NO_SEARCH_EXPECTED:
            continue
        if not keys.get("search", "").strip():
            out.append(name)
    return out


def swallowed_keys(text):
    """Stanzas where a key's VALUE contains what looks like another key.

    Catches the weld even when the swallowed key is not `search`: a legitimate
    value never contains a bare `\\nsomekey = ` at line start, and the welded
    form puts the second key inline in the first key's value.
    """
    out = []
    for m in STANZA_RE.finditer(text):
        name, keys = m.group(1), stanza_keys(m.group(2))
        for key, value in keys.items():
            for suspect in ("search =", "enableSched =", "cron_schedule =", "disabled ="):
                # Mid-value, not at the start of a continuation line: a welded
                # key sits inline right after the previous value's last char.
                if suspect in value.replace("\n", " ") and not value.lstrip().startswith(suspect):
                    out.append(f"{name}.{key} contains {suspect!r}")
    return out


env = ansible_env(ROOT / "roles/splunk_docker/templates")
rendered = env.get_template("savedsearches.conf.j2").render(
    splunk_docker_silence_detectors=DEFAULTS["splunk_docker_silence_detectors"],
    splunk_docker_silence_lookback_multiplier=DEFAULTS["splunk_docker_silence_lookback_multiplier"],
    splunk_docker_llm_freshness_indexes=DEFAULTS["splunk_docker_llm_freshness_indexes"],
    splunk_docker_alert_ntfy_url=None,
    splunk_docker_alert_slack_webhook=None,
)

errors = [
    f"FAIL: [{name}] renders with no usable `search` — Splunk will run it to "
    "HTTP 200 with zero rows rather than erroring"
    for name in missing_search(rendered)
]
errors += [f"FAIL: welded keys — {hit}" for hit in swallowed_keys(rendered)]

# The roster must be non-empty, or the freshness report renders a valid search
# over nothing and returns zero rows for a second, unrelated reason.
if not DEFAULTS.get("splunk_docker_llm_freshness_indexes"):
    errors.append("FAIL: splunk_docker_llm_freshness_indexes is empty")

# --- prove each check can fail -------------------------------------------
# The exact welded shape that shipped, reduced to two keys.
welded = (
    "[fixture_welded]\n"
    "description = ends here.search = | makeresults | eval x=1\n"
    "enableSched = 0\n"
)
if "fixture_welded" not in missing_search(welded):
    errors.append(
        "FAIL: regression case — the welded description/search shape that "
        "reached production was not reported as missing a search"
    )
if not swallowed_keys(welded):
    errors.append(
        "FAIL: regression case — the welded description/search shape was not "
        "reported as containing an inline key"
    )
# A stanza with `search =` and nothing after it is equally dead.
if "fixture_blank" not in missing_search("[fixture_blank]\nsearch =\n"):
    errors.append("FAIL: regression case — an empty `search =` value was not caught")
# And a healthy stanza must NOT be flagged, or the check is just noise.
healthy = "[fixture_ok]\nsearch = | makeresults | eval x=1 \\\n  | table x\ndisabled = 1\n"
if missing_search(healthy) or swallowed_keys(healthy):
    errors.append("FAIL: false positive — a well-formed multi-line stanza was flagged")

if errors:
    for err in errors:
        print(err)
    sys.exit(1)

print("PASS: every rendered stanza defines a non-empty `search`, no keys are welded "
      "together by whitespace-stripping comments, and the freshness roster is non-empty")
print("\nAll tests passed.")
