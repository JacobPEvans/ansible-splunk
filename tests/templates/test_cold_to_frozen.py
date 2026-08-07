#!/usr/bin/env python3
"""
Test the cold_to_frozen.py.j2 freeze contract.

Splunk deletes a bucket only when this script exits 0, so the properties worth
guarding are the ones that decide whether data survives:

  - every failure path exits non-zero, so the bucket stays on disk
  - the completion marker is written last, and never when anything failed
  - credentials reach rclone through the environment, never on a command line
  - transfers are actually concurrent, which is what makes the archive keep up

The upload itself is rclone's job now; these tests check how it is invoked
rather than re-testing S3.

Run from repo root:
  python3 tests/templates/test_cold_to_frozen.py
"""

import os
import sys
import tempfile
import types
from pathlib import Path

from _render_env import ansible_env

try:
    from jinja2 import Environment, FileSystemLoader
except ImportError:
    print("ERROR: jinja2 not installed. Run: pip install jinja2")
    sys.exit(1)

TEMPLATE_DIR = Path(__file__).parent.parent.parent / "roles/splunk_docker/templates"
env = ansible_env(TEMPLATE_DIR)

SETTING_KEYS = (
    "SPLUNK_FROZEN_S3_ENDPOINT",
    "SPLUNK_FROZEN_S3_BUCKET",
    "SPLUNK_FROZEN_S3_KEY_ID",
    "SPLUNK_FROZEN_S3_APP_KEY",
)

# The script reads its config at import time, so the values have to be in place
# before the module body executes.
CONFIG = {
    "SPLUNK_FROZEN_S3_ENDPOINT": "https://s3.us-east-005.example.invalid",
    "SPLUNK_FROZEN_S3_BUCKET": "test-bucket",
    "SPLUNK_FROZEN_S3_KEY_ID": "test-key-id",
    "SPLUNK_FROZEN_S3_APP_KEY": "test-app-key",
}

RCLONE_PATH = "/opt/splunk/etc/system/local/bin/rclone"
CONCURRENCY = 8


def load_module(env_vars=None, config_path=""):
    """Render and exec the template with a controlled env and config path.

    Each call produces an independent module, so cases cannot leak into each
    other via process-wide state.
    """
    for key in SETTING_KEYS:
        os.environ.pop(key, None)
    for key, value in (env_vars or {}).items():
        os.environ[key] = value

    rendered = env.get_template("cold_to_frozen.py.j2").render(
        ansible_managed="test render",
        splunk_docker_frozen_config_path=config_path,
        splunk_docker_frozen_rclone_path=RCLONE_PATH,
        splunk_docker_frozen_upload_timeout_seconds=900,
        splunk_docker_frozen_upload_concurrency=CONCURRENCY,
    )
    module = types.ModuleType("cold_to_frozen")
    module.__dict__["__name__"] = "cold_to_frozen"
    exec(compile(rendered, "cold_to_frozen.py", "exec"), module.__dict__)
    return module


def make_bucket(root, name="db_1_1_0", index="main", files=("Hosts.data",)):
    bucket_dir = os.path.join(root, index, "db", name)
    os.makedirs(bucket_dir)
    for filename in files:
        Path(bucket_dir, filename).write_bytes(b"x")
    return bucket_dir


def run_main(module, bucket_dir):
    original_argv = sys.argv[:]
    sys.argv[1:] = [bucket_dir]
    try:
        return module.main()
    finally:
        sys.argv[:] = original_argv


def record_calls(module, fail_on=None):
    """Replace run_rclone with a recorder. fail_on matches the rclone verb."""
    calls = []

    def _run(args, stdin_data=None):
        calls.append(args)
        if fail_on and args and args[0] == fail_on:
            return "rclone exited 1: simulated"
        return None

    setattr(module, "run_rclone", _run)
    setattr(module, "log", lambda _msg: None)
    return calls


errors = []

# --- The happy path: copy, then marker, in that order ----------------------
mod = load_module(env_vars=CONFIG)
calls = record_calls(mod)
with tempfile.TemporaryDirectory() as root:
    bucket_dir = make_bucket(root)
    rc = run_main(mod, bucket_dir)

if rc != 0:
    errors.append("a successful archive must exit 0, got %r" % rc)
verbs = [call[0] for call in calls]
if verbs != ["copy", "rcat"]:
    errors.append("expected a copy then a marker rcat, got: %r" % verbs)
if calls and not calls[0][2].endswith("main/db_1_1_0"):
    # Keys land at the bucket root as <index>/<bucket>/<relpath>, with no extra
    # prefix - restore and every runbook path assume that layout.
    errors.append("copy destination must be <bucket>/<index>/<id>, got: %r" % calls[0][2])
if calls and mod.ARCHIVE_MARKER_NAME not in calls[-1][1]:
    errors.append("the last call must write the completion marker, got: %r" % calls[-1])

# --- A failed copy must abort before any marker is written -----------------
#
# This is the expensive one to get wrong: a marker on an incomplete prefix makes
# restore trust a bucket that is missing files.
fail_mod = load_module(env_vars=CONFIG)
fail_calls = record_calls(fail_mod, fail_on="copy")
with tempfile.TemporaryDirectory() as root:
    bucket_dir = make_bucket(root, name="db_2_2_0")
    fail_rc = run_main(fail_mod, bucket_dir)

if fail_rc != 1:
    errors.append("a failed copy must exit non-zero so Splunk keeps the bucket, got %r" % fail_rc)
if any(call[0] == "rcat" for call in fail_calls):
    errors.append("no completion marker may be written when the copy failed")

# --- A failed marker write must also fail the bucket -----------------------
#
# Every file is stored at that point, but nothing can prove it, and restore
# refuses an unmarked bucket. Reporting success would strand the data.
marker_mod = load_module(env_vars=CONFIG)
record_calls(marker_mod, fail_on="rcat")
with tempfile.TemporaryDirectory() as root:
    bucket_dir = make_bucket(root, name="db_3_3_0")
    marker_rc = run_main(marker_mod, bucket_dir)

if marker_rc != 1:
    errors.append("a failed marker write must exit non-zero, got %r" % marker_rc)

# --- An empty bucket directory is never reported as archived ---------------
empty_mod = load_module(env_vars=CONFIG)
record_calls(empty_mod)
with tempfile.TemporaryDirectory() as root:
    empty_dir = os.path.join(root, "main", "db", "db_4_4_0")
    os.makedirs(empty_dir)
    empty_rc = run_main(empty_mod, empty_dir)

if empty_rc != 1:
    errors.append("an empty bucket must not be reported as archived, got %r" % empty_rc)

# --- Credentials go through the environment, never a command line ----------
#
# A command line is visible to every other process on the host, and rclone
# accepts credentials either way - so this is a real choice that must not
# silently regress.
cred_mod = load_module(env_vars=CONFIG)
rclone_env = cred_mod.rclone_env()
if rclone_env.get("RCLONE_CONFIG_ARCHIVE_SECRET_ACCESS_KEY") != CONFIG["SPLUNK_FROZEN_S3_APP_KEY"]:
    errors.append("the app key must be passed to rclone through the environment")
if rclone_env.get("RCLONE_CONFIG_ARCHIVE_ENDPOINT") != CONFIG["SPLUNK_FROZEN_S3_ENDPOINT"]:
    errors.append("the endpoint must be passed to rclone through the environment")

argv_calls = []


def _capture_argv(cmd, **kwargs):
    argv_calls.append(cmd)

    class _Result(object):
        returncode = 0
        stdout = b""
        stderr = b""

    return _Result()


setattr(cred_mod, "subprocess", types.SimpleNamespace(run=_capture_argv, PIPE=-1))
cred_mod.run_rclone(["copy", "/tmp/x", "archive:b/i/d"])
flat = " ".join(argv_calls[0])
for secret in (CONFIG["SPLUNK_FROZEN_S3_APP_KEY"], CONFIG["SPLUNK_FROZEN_S3_KEY_ID"]):
    if secret in flat:
        errors.append("a credential appeared on the rclone command line")

# --- Concurrency and config isolation are load-bearing flags ---------------
#
# Single-stream upload is what made archiving slower than data arrived: the
# endpoint throttles per connection. And a stray on-disk rclone config must not
# be able to redirect the archive somewhere else.
if CONCURRENCY < 2 or "--transfers" not in flat or "--s3-upload-concurrency" not in flat:
    errors.append("uploads must run concurrently, got: %r" % flat)
if "--config" not in flat or os.devnull not in flat:
    errors.append("rclone must be pinned to no on-disk config, got: %r" % flat)

# The destination bucket must never be probed for or created. rclone ensures a
# bucket exists before writing unless told not to, and that needs a create
# permission the archive credential deliberately lacks — it is scoped to one
# existing bucket. Observed live: the endpoint answered the probe 403 and
# rclone treated it as fatal, so every upload failed before a byte moved,
# while the bucket it was asking about already existed.
if "--s3-no-check-bucket" not in flat:
    errors.append("rclone must not probe for or create the bucket; a scoped "
                  "credential cannot create one and the probe fails the "
                  "upload, got: %r" % flat)

# --- Config resolution: environment vs credential file ---------------------
#
# splunkd invokes the script with a restricted environment, so the file is the
# path that matters in production; the environment must still win so a manual
# canary run behaves the same way.
with tempfile.NamedTemporaryFile("w", suffix=".conf", delete=False) as fh:
    for key, value in CONFIG.items():
        fh.write("%s=%s\n" % (key, value))
    file_config_path = fh.name

try:
    file_mod = load_module(env_vars={}, config_path=file_config_path)
    if file_mod.BUCKET != CONFIG["SPLUNK_FROZEN_S3_BUCKET"]:
        errors.append("with no environment, settings must resolve from the credential file")

    override = dict(CONFIG, SPLUNK_FROZEN_S3_BUCKET="from-environment")
    both_mod = load_module(env_vars=override, config_path=file_config_path)
    if both_mod.BUCKET != "from-environment":
        errors.append("the environment must win over the credential file")
finally:
    os.unlink(file_config_path)

# Missing in both places must refuse rather than proceed: the alternative is
# letting Splunk delete an unarchived bucket.
missing_mod = load_module(env_vars={}, config_path="/nonexistent/cold_to_frozen.conf")
record_calls(missing_mod)
with tempfile.TemporaryDirectory() as root:
    bucket_dir = make_bucket(root, name="db_5_5_0")
    missing_rc = run_main(missing_mod, bucket_dir)

if missing_rc != 1:
    errors.append("missing credentials must refuse the freeze, got %r" % missing_rc)

if errors:
    print("FAIL:")
    for error in errors:
        print("  - %s" % error)
    sys.exit(1)

print("PASS: cold_to_frozen freeze contract, credential handling, and rclone invocation")
