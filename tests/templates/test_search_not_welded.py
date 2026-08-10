#!/usr/bin/env python3
"""No rendered stanza may carry a comment welded into a directive value.

THE DEFECT THIS EXISTS TO CATCH
-------------------------------
Rendered under Ansible's settings (trim_blocks=True), the `search =` line in
savedsearches.conf.j2 ended in `{% endif %}`, whose trailing newline Ansible
strips. The `#` comment block on the following line was therefore appended to
the search value, producing:

    ... | where minutes_silent > 30# Lookback derives from this detector's ...

Splunk stored that happily. It scheduled the search, dispatched it every 10
minutes, and failed it every time with a FATAL parse error. 17 detectors were
live in exactly that state while the test suite stayed green.

WHY THE EXISTING TESTS MISSED IT, TWICE OVER
--------------------------------------------
1. They built bare `jinja2.Environment(...)`, which defaults trim_blocks=False.
   The weld does not occur under that setting, so the rendered text under test
   was not the text Ansible ships. Fixed by `_render_env.ansible_env`.
2. The earlier weld guard (added after a comment swallowed a whole search)
   checked two specific symptoms: a stanza with NO `search` key, and a key
   whose value had absorbed another `key = value` pair. This defect is neither
   — the `search` key is present, non-empty, and absorbed a comment rather than
   a directive. Guarding two known symptoms is not guarding the class.

So this test asserts the general property instead: SPL has no `#` comment
syntax, therefore a `#` inside a rendered `search` value is always a .conf
comment that lost its newline.

FALSIFIABILITY
--------------
A test that cannot fail proves nothing, and this suite has already shipped one
that could not. `check_welded` is therefore run against a fixture that MUST be
flagged and one that must NOT be, before it is run against the real template.
"""

import re
import sys
from pathlib import Path

from _defaults_loader import load_defaults

from _render_env import ansible_env

ROOT = Path(__file__).parent.parent.parent
TEMPLATES = ROOT / "roles/splunk_docker/templates"
DEFAULTS = load_defaults(ROOT)

# Directives whose values are executable and must never absorb a comment.
# `description` is excluded deliberately: it is free prose and a '#' in it is
# legitimate.
EXECUTABLE_KEYS = ("search",)


def check_welded(text):
    """Return [(stanza, key, offending_value)] for values containing '#'."""
    found = []
    for m in re.finditer(r"^\[(\S+)\]$(.*?)(?=^\[|\Z)", text, re.M | re.S):
        stanza, body = m.group(1), m.group(2)
        for line in body.splitlines():
            for key in EXECUTABLE_KEYS:
                prefix = f"{key} = "
                if line.startswith(prefix) and "#" in line:
                    found.append((stanza, key, line[len(prefix) :]))
    return found


# --- prove the check can fail before trusting it to pass -------------------

FIXTURE_WELDED = """[some_detector]
search = | tstats count WHERE index=x | where minutes_silent > 30# a comment
dispatch.latest_time = now
"""

FIXTURE_CLEAN = """[some_detector]
description = counts things # this hash is fine, prose is not executable
search = | tstats count WHERE index=x | where minutes_silent > 30
dispatch.latest_time = now
"""

_welded = check_welded(FIXTURE_WELDED)
assert _welded, "check_welded failed to flag a known-welded fixture; the check is broken"
assert _welded[0][0] == "some_detector"

_clean = check_welded(FIXTURE_CLEAN)
assert not _clean, f"check_welded flagged a clean fixture: {_clean}"

# --- the real template, rendered the way Ansible renders it ----------------

rendered = ansible_env(TEMPLATES).get_template("savedsearches.conf.j2").render(
    splunk_docker_silence_detectors=DEFAULTS["splunk_docker_silence_detectors"],
    splunk_docker_silence_lookback_multiplier=DEFAULTS[
        "splunk_docker_silence_lookback_multiplier"
    ],
    splunk_docker_alert_ntfy_url=None,
    splunk_docker_alert_slack_webhook=None,
)

welded = check_welded(rendered)
if welded:
    print(f"FAIL: {len(welded)} stanza(s) have a comment welded into an executable value.")
    print("Under Ansible these are stored, scheduled, and fail to parse on every run.")
    for stanza, key, value in welded:
        print(f"  [{stanza}] {key} = ...{value[-80:]}")
    sys.exit(1)

stanza_count = len(re.findall(r"^\[(\S+)\]$", rendered, re.M))
print(f"PASS: no welded comments in executable values across {stanza_count} stanzas")
