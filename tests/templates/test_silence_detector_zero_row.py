#!/usr/bin/env python3
"""
Guard the tstats zero-row blind spot in savedsearches.conf.j2.

tstats is a GENERATING command: over a lookback window with no matching
events at all, it returns ZERO result rows -- not one row with a null
last_seen. Verified live: index=llm from the router hosts and llm_pipeline
emitters was fully empty for 18 days, and both llm_router_silence_detector
(which already had coalesce(last_seen, 0)) and llm_pipeline_silence_detector
never fired. coalesce() cannot help because there is no row for eval to run
it on -- the downstream `eval minutes_silent = ... | where minutes_silent >
N` guard simply never executes.

The fix is the appendpipe sentinel-row pattern: `appendpipe [ stats count as
_rows | where _rows == 0 | eval last_seen = 0 | fields - _rows ]`. Unlike
tstats, stats is non-generating -- an ungrouped aggregate like `count`
always emits exactly one result row, even over zero input rows -- so this
branch fires precisely when (and only when) the main tstats result set is
empty, synthesizing the missing "everything is silent" row.

A test that only greps the SPL string for "coalesce" would have passed on
the original, broken llm_router_silence_detector (it already had coalesce)
and given false confidence. This test instead simulates the two SPL
primitives the bug hinges on -- tstats-returns-zero-rows-on-no-match, and
stats-always-returns-a-row -- and asserts each fixed detector actually
produces a surviving result row when its source data is fully silent.

Run from repo root:
  python3 tests/templates/test_silence_detector_zero_row.py
"""

import re
import sys
import time
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
rendered = env.get_template("savedsearches.conf.j2").render(
    splunk_docker_silence_detectors=DEFAULTS["splunk_docker_silence_detectors"],
    splunk_docker_silence_lookback_multiplier=DEFAULTS["splunk_docker_silence_lookback_multiplier"],
    splunk_docker_alert_ntfy_url=None,
    splunk_docker_alert_slack_webhook=None,
)


def stanza_search(text, name):
    m = re.search(rf"^\[{re.escape(name)}\]$(.*?)^\[", text, re.M | re.S)
    if not m:
        raise AssertionError(f"[{name}] stanza not found")
    line = next(ln for ln in m.group(1).splitlines() if ln.startswith("search = "))
    return line[len("search = ") :]


# --- minimal SPL simulator, scoped to exactly what these searches use ------
#
# A "table" is a list of dict rows. Only the operators these specific search
# strings contain are implemented: tstats (as the zero-events ground truth
# under test), appendpipe [ stats count | where _rows == 0 | eval ... |
# fields - _rows ], eval minutes_silent = (now() - coalesce(field, 0)) / 60,
# and where minutes_silent > N. This is not a general SPL interpreter.


def run_tstats_over_empty_data():
    # Ground truth verified live (see module docstring): tstats over a
    # window with zero matching events returns zero rows, by_host or not.
    return []


def run_appendpipe_zero_guard(table, search):
    guard = re.search(
        r"appendpipe \[ stats count as _rows \| where _rows == 0 \| eval (.+?) \| fields - _rows \]",
        search,
    )
    if not guard:
        return table  # no guard present -- nothing appended (the bug)
    if len(table) != 0:
        return table  # stats count as _rows > 0 here, so `where _rows == 0` drops it
    # stats on zero input rows still emits exactly one row (ungrouped count).
    row = {}
    for assignment in guard.group(1).split(", "):
        field, _, value = assignment.partition(" = ")
        row[field] = 0 if value == "0" else value.strip('"')
    return table + [row]


def run_eval_minutes_silent(table):
    now_minutes = time.time() / 60
    for row in table:
        last_seen = row.get("last_seen")
        last_seen = last_seen if isinstance(last_seen, (int, float)) else 0
        row["minutes_silent"] = now_minutes - last_seen / 60
    return table


def run_where_minutes_silent(table, threshold):
    return [row for row in table if row["minutes_silent"] > threshold]


def simulate(search, threshold):
    """Run the fixed search shape against a fully-silent data source and
    return the surviving rows -- what the alert would fire on."""
    table = run_tstats_over_empty_data()
    table = run_appendpipe_zero_guard(table, search)
    table = run_eval_minutes_silent(table)
    return run_where_minutes_silent(table, threshold)


errors = []

# 1. The two detectors named in the bug report, plus macos_edge (identical
# fixed-lookback tstats shape, sharing the same defect).
for name, threshold in [
    ("llm_router_silence_detector", 15),
    ("llm_pipeline_silence_detector", 30),
    ("macos_edge_silence_detector", 15),
]:
    search = stanza_search(rendered, name)
    result = simulate(search, threshold)
    if not result:
        errors.append(
            f"FAIL: [{name}] produced no result row over a fully-silent data "
            f"source -- the alert would stay quiet through total silence"
        )

# 2. The generic per-index loop's non-by_host branch shares the exact same
# defect (confirmed structurally identical to llm_router_silence_detector
# before this fix): 9 of its defaults entries (unifi, claude, dns, proxy,
# firewall, netflow, openbao_audit, openbao_voter_health, honeypot) render
# through it. Spot-check every non-by_host entry.
for det in DEFAULTS["splunk_docker_silence_detectors"]:
    if det.get("by_host"):
        continue
    name = f"{det['name']}_silence_detector"
    search = stanza_search(rendered, name)
    result = simulate(search, det["threshold_minutes"])
    if not result:
        errors.append(
            f"FAIL: [{name}] (generic loop, non-by_host) produced no result "
            f"row over a fully-silent index"
        )

if errors:
    for err in errors:
        print(err)
    sys.exit(1)

print(
    "PASS: llm_router_silence_detector, llm_pipeline_silence_detector, "
    "macos_edge_silence_detector, and every non-by_host generic silence "
    "detector all produce a firing result row when their source data is "
    "fully silent"
)
print("\nAll tests passed.")
