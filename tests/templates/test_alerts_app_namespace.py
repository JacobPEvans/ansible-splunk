#!/usr/bin/env python3
"""
Guard the deployment path of savedsearches.conf.

Splunk's scheduler dispatches saved searches per app context and never walks
the system namespace. A scheduled search in etc/system/local/savedsearches.conf
is accepted without complaint: the REST API reports enableSched=1 and a valid
cron, the UI shows it enabled, and it is never run. next_scheduled_time stays
empty and no row for it ever reaches index=_internal sourcetype=scheduler. That
failure is silent in every direction, which is why it went unnoticed until an
audit compared next_scheduled_time across namespaces.

So the path is the contract, not an implementation detail. Move savedsearches
back under system/local and every alert in this repo goes quiet again with no
error anywhere.

Run from repo root:
  python3 tests/templates/test_alerts_app_namespace.py
"""

import re
import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent.parent
TASKS = ROOT / "roles/splunk_docker/tasks/main.yml"

APP_DEST = "apps/homelab_alerts/local/savedsearches.conf"

errors = []
body = TASKS.read_text()

# Every dest:/path: line naming savedsearches.conf, whatever task it belongs to.
# The value is templated ("{{ splunk_docker_etc_dir }}/..."), so it contains
# spaces — match to end of line, not to the next whitespace.
written = re.findall(r"^\s*dest:\s*\"?(.*savedsearches\.conf)\"?\s*$", body, re.M)
removed = re.findall(r"^\s*path:\s*\"?(.*savedsearches\.conf)\"?\s*$", body, re.M)

if not written:
    print("FAIL: no task deploys savedsearches.conf at all")
    sys.exit(1)

if not any(d.endswith(APP_DEST) for d in written):
    errors.append(f"FAIL: savedsearches.conf is not deployed to {APP_DEST} (found: {written})")

for d in written:
    if "system/local" in d:
        errors.append(
            f"FAIL: savedsearches.conf deployed to {d} — the system namespace "
            "receives no scheduled dispatch, so every alert would run never"
        )

if not any("system/local" in d for d in removed):
    errors.append("FAIL: no task targets the old system/local/savedsearches.conf for removal")

# The app is inert without its manifest: Splunk skips a directory under
# etc/apps that carries no app.conf, taking the saved searches with it.
if "apps/homelab_alerts/default/app.conf" not in body:
    errors.append("FAIL: no app.conf deployed for homelab_alerts — Splunk ignores the app dir")

# The pre-fix file must be actively removed, not merely stopped being written:
# a converge that only changes the destination leaves the old stanzas behind as
# a permanently-dead duplicate of every alert name.
if not re.search(r"system/local/savedsearches\.conf\"\s*\n\s*state:\s*absent", body):
    errors.append("FAIL: the old system/local/savedsearches.conf is never removed")

if errors:
    for err in errors:
        print(err)
    sys.exit(1)

print(f"PASS: savedsearches.conf deploys to {APP_DEST}, with app.conf, and the "
      "system-namespace copy is removed")
