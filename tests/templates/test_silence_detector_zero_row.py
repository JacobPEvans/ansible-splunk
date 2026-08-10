#!/usr/bin/env python3
"""
Guard the tstats/stats zero-row blind spot in savedsearches.conf.j2.

tstats is a GENERATING command: over a lookback window with no matching
events at all, it returns ZERO result rows -- not one row with a null
last_seen -- whether or not it groups `by host`. `stats ... by <field>`
shares the same blind spot when grouped: zero input rows means zero groups,
so it also emits nothing. (An UNGROUPED `stats` aggregate like `stats count`
is exempt -- it always emits exactly one row, even over zero input rows.)
Verified live: index=llm from the router hosts and llm_pipeline emitters was
fully empty for 18 days, and both llm_router_silence_detector (which already
had coalesce(last_seen, 0)) and llm_pipeline_silence_detector never fired.
coalesce() cannot help because there is no row for eval to run it on -- the
downstream `eval minutes_silent = ... | where minutes_silent > N` guard
simply never executes.

The fix is the appendpipe sentinel-row pattern: `appendpipe [ stats count as
_rows | where _rows == 0 | eval last_seen = 0 | fields - _rows ]`. An
ungrouped `stats count` always emits exactly one result row, even over zero
input rows -- so this branch fires precisely when (and only when) the main
result set is empty, synthesizing the missing "everything is silent" row.

Coverage note: this test used to check a hardcoded list of stanza names (the
three named detectors plus the generic per-index loop's non-by_host branch),
so a new stanza with the same defect -- or the loop's by_host branch -- would
not be caught. It now DERIVES the set of checked searches from the rendered
template (see `silence_stanzas()`), the same approach test_cutover_gate.py
uses for the disabled-by-default gate.

Inclusion rule: a stanza qualifies as a silence/staleness detector -- and
therefore must survive its own aggregation returning zero rows -- when its
search performs a grouped aggregation (`tstats`, by-clause or not; or
`stats ... by`) AND computes elapsed time since a last-seen event
(`now() - coalesce(...)`). The second half excludes a spike/content-match
search (nothing to fire on when healthy is correct) and a *data-value*
threshold over a grouped aggregate, e.g. llm_serving_memory_headroom's
`stats avg(...) by host | where ... > 85` -- zero rows there means no host is
over the memory ceiling, the correct silent-when-healthy behavior, not a
blind spot.

Run from repo root:
  python3 tests/templates/test_silence_detector_zero_row.py
"""

import re
import sys
import time
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

# Same stanza-block extraction as test_cutover_gate.py's STANZA_RE.
STANZA_RE = re.compile(r"^\[(\S+)\]$(.*?)(?=^\[|\Z)", re.M | re.S)
SEARCH_RE = re.compile(r"^search = (.*)$", re.M)
# SPL command keywords are case-insensitive (`stats ... BY host` and
# `stats ... by host` are identical to Splunk's parser), so this must match
# regardless of case -- a case-sensitive version silently missed every
# grouped-stats search written in the `BY`-uppercase style.
GROUPED_AGG_RE = re.compile(r"\btstats\b|\bstats\b[^|]*\bby\b", re.I)
# Any reference to now() -- elapsed-time subtraction (now() - coalesce(...)),
# or a recency comparison (relative_time(now(), ...)) -- is this codebase's
# tell for "this search's condition is time/recency, not a data value". Kept
# broad (not anchored to the one `now() - coalesce(` idiom PR #460 happened to
# use) so a differently-worded staleness check -- e.g. `now() - last_seen`
# with no coalesce() wrapper -- is still recognized.
SILENCE_SIGNATURE_RE = re.compile(r"now\(\)")

# Real, currently-guarded stanzas that must always be swept in -- a floor so
# a selector regression that stops matching anything still fails loudly
# instead of passing vacuously with zero detectors checked.
EXPECTED_INCLUDED = {
    "macos_edge_silence_detector",
    "llm_pipeline_silence_detector",
    "llm_router_silence_detector",
}
# Real grouped-aggregation stanzas that are NOT silence detectors (a
# data-value threshold or a run-count/score comparison, not elapsed time
# since a last-seen event) -- must never be swept in.
EXPECTED_EXCLUDED = {
    "model_eval_regression",
    "llm_serving_memory_headroom",
    "bench_verdict_maturity",
}


def is_silence_detector(search):
    return bool(GROUPED_AGG_RE.search(search)) and bool(SILENCE_SIGNATURE_RE.search(search))


def silence_stanzas(rendered):
    """Name -> search for every stanza whose search matches the
    grouped-aggregation-over-empty-input blind spot (see module docstring),
    derived entirely from the render -- never a maintained list."""
    found = {}
    for m in STANZA_RE.finditer(rendered):
        sm = SEARCH_RE.search(m.group(2))
        if sm and is_silence_detector(sm.group(1)):
            found[m.group(1)] = sm.group(1)
    return found


# --- minimal SPL simulator, scoped to exactly what these searches use ------
#
# A "table" is a list of dict rows. Only the operators these specific search
# strings contain are implemented: the grouped aggregation under test (as the
# zero-events ground truth), appendpipe [ stats count | where _rows == 0 |
# eval ... | fields - _rows ], eval minutes_silent = (now() - coalesce(field,
# 0)) / 60, and where minutes_silent > <threshold>. This is not a general SPL
# interpreter.


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
        row[field.strip()] = 0 if value.strip() == "0" else value.strip().strip('"')
    return table + [row]


def run_eval_minutes_silent(table):
    now_minutes = time.time() / 60
    for row in table:
        last_seen = row.get("last_seen")
        last_seen = last_seen if isinstance(last_seen, (int, float)) else 0
        row["minutes_silent"] = now_minutes - last_seen / 60
    return table


def run_where_threshold(table, search):
    m = re.search(r"where minutes_silent > (\S+)", search)
    try:
        threshold = float(m.group(1)) if m else 0.0
    except ValueError:
        # Symbolic threshold (e.g. host_threshold_minutes, derived via a
        # case() expression bounded by a real detector's threshold_minutes).
        # A sentinel row's last_seen is always 0, so minutes_silent is
        # ~now()/60 -- tens of millions of minutes -- which dwarfs any
        # realistic bounded threshold this codebase would ever configure.
        threshold = 0.0
    return [row for row in table if row["minutes_silent"] > threshold]


def simulate(search):
    """Run a search against a fully-silent data source (a grouped
    aggregation over zero matching input rows returns zero result rows) and
    return the surviving rows -- what the alert would fire on."""
    table = run_appendpipe_zero_guard([], search)
    table = run_eval_minutes_silent(table)
    return run_where_threshold(table, search)


env = ansible_env(ROOT / "roles/splunk_docker/templates")
rendered = env.get_template("savedsearches.conf.j2").render(
    splunk_docker_silence_detectors=DEFAULTS["splunk_docker_silence_detectors"],
    splunk_docker_silence_lookback_multiplier=DEFAULTS["splunk_docker_silence_lookback_multiplier"],
    splunk_docker_alert_ntfy_url=None,
    splunk_docker_alert_slack_webhook=None,
)

detectors = silence_stanzas(rendered)
errors = []

missing_floor = EXPECTED_INCLUDED - detectors.keys()
if missing_floor:
    errors.append(
        f"FAIL: the inclusion rule stopped matching known silence detectors: "
        f"{sorted(missing_floor)} -- selector regression, this test would now pass vacuously"
    )

overreach = EXPECTED_EXCLUDED & detectors.keys()
if overreach:
    errors.append(
        f"FAIL: the inclusion rule swept in non-silence stanzas that legitimately "
        f"return nothing when healthy: {sorted(overreach)}"
    )

for name, search in detectors.items():
    if not simulate(search):
        errors.append(
            f"FAIL: [{name}] produced no result row over a fully-silent data "
            f"source -- the alert would stay quiet through total silence"
        )

# --- regression fixtures: prove the derivation catches a reintroduced bug,
# and doesn't flag a correctly-guarded search, without touching the real
# template (same technique as test_cutover_gate.py's fixture). ---
BROKEN = (
    "| tstats latest(_time) as last_seen WHERE index=fixture by host "
    "| eval minutes_silent = (now() - coalesce(last_seen, 0)) / 60 "
    "| where minutes_silent > 15"
)
FIXED = (
    "| tstats latest(_time) as last_seen WHERE index=fixture by host "
    "| appendpipe [ stats count as _rows | where _rows == 0 | eval last_seen = 0 | fields - _rows ] "
    "| eval minutes_silent = (now() - coalesce(last_seen, 0)) / 60 "
    "| where minutes_silent > 15"
)

if not is_silence_detector(BROKEN):
    errors.append("FAIL: regression fixture -- inclusion rule failed to recognize a real silence-detector shape")
elif simulate(BROKEN):
    errors.append("FAIL: regression fixture -- simulator did not catch a search missing the appendpipe guard")

if not is_silence_detector(FIXED):
    errors.append("FAIL: regression fixture -- inclusion rule rejected a properly-guarded silence detector")
elif not simulate(FIXED):
    errors.append("FAIL: regression fixture -- simulator rejected a correctly-guarded search")

# Uppercase BY regression: SPL command keywords are case-insensitive
# (`stats ... BY host` and `stats ... by host` are identical to Splunk's
# parser), so a case-sensitive GROUPED_AGG_RE silently missed every grouped
# search written in the `BY`-uppercase style -- this caught two real
# detectors (ansible_stale_converge, ansible_orphan_host) before it was
# fixed.
UPPERCASE_BY = (
    "index=fixture | stats latest(_time) as last_seen BY host "
    "| appendpipe [ stats count as _rows | where _rows == 0 | eval last_seen = 0 | fields - _rows ] "
    "| eval minutes_silent = (now() - coalesce(last_seen, 0)) / 60 "
    "| where minutes_silent > 15"
)
if not is_silence_detector(UPPERCASE_BY):
    errors.append("FAIL: regression fixture -- inclusion rule is case-sensitive to the BY keyword")

if errors:
    for err in errors:
        print(err)
    sys.exit(1)

print(
    f"PASS: all {len(detectors)} silence/staleness detectors derived from the render "
    f"({', '.join(sorted(detectors))}) produce a firing result row when their source "
    f"data is fully silent; the inclusion rule excludes non-silence grouped aggregations "
    f"and catches both a reintroduced missing-guard bug and its fix in fixtures"
)
print("\nAll tests passed.")
