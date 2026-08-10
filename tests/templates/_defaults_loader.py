"""Load the splunk_docker role's merged defaults, the way Ansible does.

WHY THIS MODULE EXISTS
-----------------------
roles/splunk_docker/defaults/main.yml used to be one file, loaded here with a
single `yaml.safe_load`. It is now `defaults/main/` — a directory of
topic-named files, because Ansible loads every file there and merges the
top-level keys, and a single flat file had grown past the point where the
section you want could be found by reading (the role itself takes advantage
of this: see roles/splunk_docker/defaults/main/09-custom-indexes-core.yml).

A test that still reads the old single path breaks the moment the split
lands. This loader reproduces Ansible's merge (later file wins on a key
collision, same as `include_vars: dir:`) so every test keeps seeing the same
merged dict it always did.

These tests run as standalone scripts, not under pytest, so this is a plain
sibling module rather than a conftest — same shape as _render_env.py.
"""

from pathlib import Path

import yaml


def load_defaults(root: Path) -> dict:
    """Merge every file in roles/splunk_docker/defaults/main/ into one dict."""
    defaults_dir = root / "roles/splunk_docker/defaults/main"
    merged: dict = {}
    for path in sorted(defaults_dir.glob("*.yml")):
        merged.update(yaml.safe_load(path.read_text()) or {})
    return merged
