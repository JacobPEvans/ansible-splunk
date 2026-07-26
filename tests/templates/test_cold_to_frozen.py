#!/usr/bin/env python3
"""
Test the cold_to_frozen.py.j2 upload retry classification.

The freeze script must distinguish three outcomes, because Splunk deletes a
bucket only when the script exits 0:

  transport failure (URLError) -> retryable, bounded retry, then give up safely
  retryable HTTP (429/5xx)     -> retryable
  terminal HTTP (403 etc.)     -> fail immediately, no retry

Getting URLError wrong is the expensive case: a single connect/DNS/TLS blip
would abandon the bucket on a disk that is already tight, and the same bucket
fails again on the next pass.

Run from repo root:
  python3 tests/templates/test_cold_to_frozen.py
"""

import os
import sys
import tempfile
import types
import urllib.error
from email.message import Message
from pathlib import Path

try:
    from jinja2 import Environment, FileSystemLoader
except ImportError:
    print("ERROR: jinja2 not installed. Run: pip install jinja2")
    sys.exit(1)

TEMPLATE_DIR = Path(__file__).parent.parent.parent / "roles/splunk_docker/templates"
env = Environment(loader=FileSystemLoader(str(TEMPLATE_DIR)), keep_trailing_newline=True)

SETTING_KEYS = (
    "SPLUNK_FROZEN_S3_ENDPOINT",
    "SPLUNK_FROZEN_S3_BUCKET",
    "SPLUNK_FROZEN_S3_KEY_ID",
    "SPLUNK_FROZEN_S3_APP_KEY",
)

# The script reads its config from the environment at import time, so the
# values have to be in place before the module body executes.
CONFIG = {
    "SPLUNK_FROZEN_S3_ENDPOINT": "https://s3.us-east-005.example.invalid",
    "SPLUNK_FROZEN_S3_BUCKET": "test-bucket",
    "SPLUNK_FROZEN_S3_KEY_ID": "test-key-id",
    "SPLUNK_FROZEN_S3_APP_KEY": "test-app-key",
}


def load_module(env_vars=None, config_path=""):
    """Render and exec the template with a controlled env and config path.

    Splunkd's restricted environment is exactly what env_vars={} simulates:
    the module must then fall back to reading config_path. Every call clears
    the four settings from os.environ first so scenarios cannot leak into
    each other via process-wide state.
    """
    for key in SETTING_KEYS:
        os.environ.pop(key, None)
    for key, value in (env_vars or {}).items():
        os.environ[key] = value

    rendered = env.get_template("cold_to_frozen.py.j2").render(
        ansible_managed="test render",
        splunk_docker_frozen_config_path=config_path,
    )
    module = types.ModuleType("cold_to_frozen")
    module.__dict__["__name__"] = "cold_to_frozen"
    exec(compile(rendered, "cold_to_frozen.py", "exec"), module.__dict__)
    return module


mod = load_module(env_vars=CONFIG)

errors = []
calls = []


def fake_urlopen(raise_with):
    def _open(req, **_kwargs):
        calls.append(req.full_url)
        raise raise_with

    return _open


with tempfile.NamedTemporaryFile(suffix=".tsidx", delete=False) as handle:
    handle.write(b"bucket payload")
    PAYLOAD = handle.name


def run(raise_with, retry=False):
    """Call put_object (or put_object_with_retry) with urlopen stubbed out."""
    del calls[:]
    original = mod.urllib.request.urlopen
    mod.urllib.request.urlopen = fake_urlopen(raise_with)
    try:
        fn = mod.put_object_with_retry if retry else mod.put_object
        return fn(PAYLOAD, "prefix/index/bucket/file.tsidx")
    finally:
        mod.urllib.request.urlopen = original


HTTP_ERROR_503 = urllib.error.HTTPError(
    "https://example.invalid", 503, "Service Unavailable", Message(), None
)
HTTP_ERROR_403 = urllib.error.HTTPError(
    "https://example.invalid", 403, "Forbidden", Message(), None
)
URL_ERROR = urllib.error.URLError("connection refused")

# 1. A transport failure must be classified retryable.
result = run(URL_ERROR)
if not (result or "").startswith("retryable"):
    errors.append("URLError must be retryable, got: %r" % result)

# 2. HTTPError subclasses URLError. If the handlers are ordered wrongly the
#    URLError branch swallows every HTTP status and 403 becomes retryable.
result = run(HTTP_ERROR_403)
if (result or "").startswith("retryable"):
    errors.append("HTTP 403 must NOT be retryable (handler ordering), got: %r" % result)
if "403" not in (result or ""):
    errors.append("HTTP 403 error string must name the status, got: %r" % result)

# 3. Retryable HTTP statuses still classify as before.
result = run(HTTP_ERROR_503)
if not (result or "").startswith("retryable"):
    errors.append("HTTP 503 must be retryable, got: %r" % result)

# 4. The retry loop actually retries a URLError, and bounds itself.
result = run(URL_ERROR, retry=True)
if len(calls) != mod.MAX_ATTEMPTS:
    errors.append(
        "URLError should be attempted MAX_ATTEMPTS (%d) times, got %d"
        % (mod.MAX_ATTEMPTS, len(calls))
    )
if result is None:
    errors.append("exhausted retries must return an error, not success")

# 5. A terminal status must not burn retries.
result = run(HTTP_ERROR_403, retry=True)
if len(calls) != 1:
    errors.append("HTTP 403 should be attempted once, got %d" % len(calls))

Path(PAYLOAD).unlink()

# --- Config resolution: environment vs. credential file -------------------
#
# splunkd invokes coldToFrozenScript with a restricted environment, so the
# compose-injected env vars a manual `docker exec` sees are absent on the
# real path. The script must fall back to reading CONFIG_PATH, and the
# environment must still win when both are present (preserves the existing
# manual/canary invocation).

with tempfile.NamedTemporaryFile(
    mode="w", suffix=".conf", delete=False
) as handle:
    handle.write(
        "# comment line, ignored\n"
        "\n"
        "SPLUNK_FROZEN_S3_ENDPOINT=https://s3.us-east-005.file.invalid\n"
        "SPLUNK_FROZEN_S3_BUCKET=file-bucket\n"
        "SPLUNK_FROZEN_S3_KEY_ID=file-key-id\n"
        "SPLUNK_FROZEN_S3_APP_KEY=file-app-key\n"
    )
    CONFIG_FILE = handle.name

# 6. No environment at all (splunkd's real invocation) -> resolved from file.
file_mod = load_module(env_vars={}, config_path=CONFIG_FILE)
if file_mod.ENDPOINT != "https://s3.us-east-005.file.invalid":
    errors.append("ENDPOINT should resolve from the config file, got: %r" % file_mod.ENDPOINT)
if file_mod.BUCKET != "file-bucket":
    errors.append("BUCKET should resolve from the config file, got: %r" % file_mod.BUCKET)
if file_mod.KEY_ID != "file-key-id":
    errors.append("KEY_ID should resolve from the config file, got: %r" % file_mod.KEY_ID)
if file_mod.APP_KEY != "file-app-key":
    errors.append("APP_KEY should resolve from the config file, got: %r" % file_mod.APP_KEY)

# 7. Both present -> the environment wins (the manual/canary path is unchanged).
both_mod = load_module(env_vars=CONFIG, config_path=CONFIG_FILE)
if both_mod.ENDPOINT != CONFIG["SPLUNK_FROZEN_S3_ENDPOINT"]:
    errors.append(
        "environment must win over the config file, got ENDPOINT=%r" % both_mod.ENDPOINT
    )
if both_mod.BUCKET != CONFIG["SPLUNK_FROZEN_S3_BUCKET"]:
    errors.append(
        "environment must win over the config file, got BUCKET=%r" % both_mod.BUCKET
    )

# 8. Missing in both -> still refuses, and the message still names the
#    missing keys (main() re-reads the module-level globals it already
#    resolved at import time, so this exercises the same missing-config path
#    that runs when neither source is populated).
missing_mod = load_module(env_vars={}, config_path="/nonexistent/cold_to_frozen_creds.conf")
log_lines = []
missing_mod.log = lambda msg: log_lines.append(msg)
with tempfile.TemporaryDirectory() as bucket_dir:
    Path(bucket_dir, "file.tsidx").write_bytes(b"x")
    original_argv = sys.argv[:]
    sys.argv[1:] = [bucket_dir]
    try:
        rc = missing_mod.main()
    finally:
        sys.argv[:] = original_argv
if rc != 1:
    errors.append("missing config in both env and file should refuse (exit 1), got %r" % rc)
if not any("refusing to freeze" in line and "endpoint" in line for line in log_lines):
    errors.append("missing-config message should name 'endpoint', got: %r" % log_lines)
if not any("key id" in line and "app key" in line for line in log_lines):
    errors.append("missing-config message should name 'key id' and 'app key', got: %r" % log_lines)

Path(CONFIG_FILE).unlink()

# --- Object key layout: no prefix, bucket-root <index>/<bucket>/<relpath> --
#
# The archive now lives in its own dedicated bucket, so the old
# "<prefix>/<index>/<bucket>/<file>" layout is redundant - the operator wants
# objects written directly at the bucket root as "<index>/<bucket>/<file>".

key_mod = load_module(env_vars=CONFIG)
captured_keys = []


def fake_put_object_with_retry(_local_path, object_key):
    captured_keys.append(object_key)
    return None


key_mod.put_object_with_retry = fake_put_object_with_retry

with tempfile.TemporaryDirectory() as splunk_db:
    bucket_dir = os.path.join(splunk_db, "main", "db", "db_1_1_0")
    os.makedirs(bucket_dir)
    Path(bucket_dir, "Hosts.data").write_bytes(b"x")
    original_argv = sys.argv[:]
    sys.argv[1:] = [bucket_dir]
    try:
        rc = key_mod.main()
    finally:
        sys.argv[:] = original_argv

if rc != 0:
    errors.append("main() with a stubbed uploader should succeed, got rc=%r" % rc)
if captured_keys != ["main/db_1_1_0/Hosts.data"]:
    errors.append(
        "object key should be exactly '<index>/<bucket>/<relpath>' with no "
        "prefix, got: %r" % captured_keys
    )

if errors:
    print("FAIL")
    for error in errors:
        print("  - %s" % error)
    sys.exit(1)

print("PASS: cold_to_frozen retry classification and config resolution")
