"""One Jinja2 Environment, configured the way Ansible configures it.

WHY THIS MODULE EXISTS
----------------------
Every template test here used to build its own bare `jinja2.Environment(...)`.
A bare Environment defaults `trim_blocks=False`. Ansible's `template` module
defaults it to **True**. That one flag makes the tests render a different
document than production ships.

It is not a theoretical difference. `trim_blocks=True` removes the newline
immediately following a `{% ... %}` block tag. In savedsearches.conf.j2 the
`search =` line ends in `{% endif %}`, so under Ansible — and only under
Ansible — the comment block on the next line was welded onto the end of the
search value. Splunk accepted the stanza, scheduled it, dispatched it on cron,
and failed it with a FATAL parse error every run:

    Error in 'where' command: The operator at '# Lookback derives from this
    detector's own threshold (not a flat constant' is invalid.

17 silence detectors were live in that state. The test suite was green
throughout, because with `trim_blocks=False` the weld does not happen and the
tests never saw it. A detector that cannot parse looks exactly like a detector
with nothing to report: both are silent.

So: tests must render with Ansible's settings, or they are testing a document
that does not exist. Import `ansible_env` here rather than constructing an
Environment inline — a second definition is a second chance to drift.

These tests run as standalone scripts (`python3 tests/templates/test_x.py`),
not under pytest, so this is a plain sibling module rather than a conftest.
"""

import sys

try:
    from jinja2 import Environment, FileSystemLoader
except ImportError:
    print("ERROR: jinja2 not installed. Run: pip install jinja2")
    sys.exit(1)

# Mirrors ansible.builtin.template's defaults. If Ansible's defaults ever
# change, change them here, in one place, and every test follows.
ANSIBLE_TEMPLATE_DEFAULTS = {
    "trim_blocks": True,
    "lstrip_blocks": False,
    "keep_trailing_newline": True,
}


def ansible_env(template_dir, **overrides):
    """An Environment matching how Ansible will render these templates.

    template_dir: path to the directory holding the .j2 files.
    overrides:    only for a test that deliberately renders the OTHER way to
                  prove a difference exists. Production-shaped rendering is
                  the default and should stay that way.
    """
    return Environment(
        loader=FileSystemLoader(str(template_dir)),
        **{**ANSIBLE_TEMPLATE_DEFAULTS, **overrides},
    )
