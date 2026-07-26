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
rendered = env.get_template("cold_to_frozen.py.j2").render(ansible_managed="test render")

# The script reads its config from the environment at import time, so the
# values have to be in place before the module body executes.
CONFIG = {
    "SPLUNK_FROZEN_S3_ENDPOINT": "https://s3.us-east-005.example.invalid",
    "SPLUNK_FROZEN_S3_BUCKET": "test-bucket",
    "SPLUNK_FROZEN_S3_KEY_ID": "test-key-id",
    "SPLUNK_FROZEN_S3_APP_KEY": "test-app-key",
}


def load_module():
    module = types.ModuleType("cold_to_frozen")
    module.__dict__["__name__"] = "cold_to_frozen"
    import os

    for key, value in CONFIG.items():
        os.environ[key] = value
    exec(compile(rendered, "cold_to_frozen.py", "exec"), module.__dict__)
    return module


mod = load_module()

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

if errors:
    print("FAIL")
    for error in errors:
        print("  - %s" % error)
    sys.exit(1)

print("PASS: cold_to_frozen retry classification")
