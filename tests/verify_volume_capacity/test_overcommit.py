#!/usr/bin/env python3
"""
Test the nominal-index-cap-overcommit Jinja expressions in
verify_volume_capacity.yml ("Sum nominal index caps per volume").

Renders the two `set_fact` expressions verbatim out of the task file (not a
reimplementation) against fixture index lists, so a change to the real
expression is what this test exercises.

Run from repo root:
  python3 tests/verify_volume_capacity/test_overcommit.py
"""

import sys
from pathlib import Path

try:
    import yaml
    from jinja2 import Environment
except ImportError:
    print("ERROR: pyyaml/jinja2 not installed. Run: pip install pyyaml jinja2")
    sys.exit(1)

TASK_FILE = (
    Path(__file__).parent.parent.parent
    / "roles/splunk_docker/tasks/verify_volume_capacity.yml"
)

# Ansible task files carry Jinja inside YAML scalars, which safe_load parses
# fine without evaluating the Jinja — only the "Sum nominal index caps per
# volume" task's two set_fact expressions are pulled out and rendered here.
tasks = yaml.safe_load(TASK_FILE.read_text())
sum_task = next(t for t in tasks if t.get("name") == "Sum nominal index caps per volume")
set_fact = sum_task["ansible.builtin.set_fact"]
HOT_WARM_EXPR = set_fact["splunk_docker_hot_warm_nominal_mb"]
COLD_EXPR = set_fact["splunk_docker_cold_nominal_mb"]

env = Environment()


def render_totals(system_indexes, indexes):
    hot_warm = env.from_string(HOT_WARM_EXPR).render(
        splunk_docker_system_indexes=system_indexes, splunk_docker_indexes=indexes
    )
    cold = env.from_string(COLD_EXPR).render(splunk_docker_indexes=indexes)
    return int(hot_warm.strip()), int(cold.strip())


errors = []

# --- under-committed: sums stay under both volume caps -----------------
SYSTEM_INDEXES = [{"name": "_internal", "max_size_mb": 20480}]
UNDER_INDEXES = [
    {"name": "qdrant", "max_size_mb": 2500},
    {"name": "dify", "max_size_mb": 12000},
    {"name": "firewall", "tier": "large", "home_max_size_mb": 20480, "max_size_mb": 102400},
]
hot_warm, cold = render_totals(SYSTEM_INDEXES, UNDER_INDEXES)
expected_hot_warm = 20480 + 2500 + 12000 + 20480  # system + small-tier + large-tier HOME slice
expected_cold = 102400 - 20480  # large-tier remainder only
if hot_warm != expected_hot_warm:
    errors.append(f"FAIL: hot_warm nominal {hot_warm} != expected {expected_hot_warm}")
elif cold != expected_cold:
    errors.append(f"FAIL: cold nominal {cold} != expected {expected_cold}")
else:
    print(f"PASS: under-committed fixture sums correctly (hot_warm={hot_warm}, cold={cold})")

HOT_WARM_CAP = 150000
if hot_warm > HOT_WARM_CAP:
    errors.append(f"FAIL: under-committed fixture ({hot_warm}) unexpectedly exceeds the {HOT_WARM_CAP} MB test cap")
else:
    print(f"PASS: under-committed fixture ({hot_warm} MB) fits the {HOT_WARM_CAP} MB test cap — no warning expected")

# --- over-committed: sum exceeds the hot_warm cap -----------------------
OVER_INDEXES = [{"name": f"svc{i}", "max_size_mb": 20000} for i in range(10)]  # 200000 MB
hot_warm_over, _ = render_totals([], OVER_INDEXES)
if hot_warm_over != 200000:
    errors.append(f"FAIL: over-committed fixture hot_warm nominal {hot_warm_over} != expected 200000")
elif hot_warm_over <= HOT_WARM_CAP:
    errors.append(f"FAIL: over-committed fixture ({hot_warm_over}) should exceed the {HOT_WARM_CAP} MB test cap")
else:
    print(f"PASS: over-committed fixture ({hot_warm_over} MB) exceeds the {HOT_WARM_CAP} MB test cap — warning expected")

# --- empty lists render to 0, not an error ------------------------------
hot_warm_empty, cold_empty = render_totals([], [])
if (hot_warm_empty, cold_empty) != (0, 0):
    errors.append(f"FAIL: empty index lists should sum to (0, 0), got ({hot_warm_empty}, {cold_empty})")
else:
    print("PASS: empty index lists sum to 0 on both volumes")

if errors:
    print()
    for err in errors:
        print(err)
    sys.exit(1)

print("\nAll tests passed.")
