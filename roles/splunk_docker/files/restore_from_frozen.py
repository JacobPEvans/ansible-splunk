#!/usr/bin/env python3
"""Restore an archived Splunk bucket from S3-compatible object storage.

This is the other half of the freeze path. Archiving is only a backup if the
restore has been exercised, so this ships alongside the freeze script rather
than being left as prose in a runbook.

USAGE
    restore_from_frozen.py list [<index>]
    restore_from_frozen.py fetch <index> <bucket_id> <destination_dir>

AFTER FETCHING, to make the data searchable again:
    1. Move the bucket into the index's thawedPath.
    2. Run:  splunk rebuild <bucket_dir>
    3. Restart splunkd.
    Thawed data is exempt from the ageing scheme, so remove it by hand when
    you are done with it or it stays forever.

Credentials come from the same environment variables the freeze script uses.
Nothing is written to disk except the bucket files you asked for.
"""

import datetime
import hashlib
import hmac
import os
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request

# Object stores return transient 429/5xx under load. A restore that gives up on
# the first one leaves a half-written bucket, which is worse than not starting:
# the files look present but the bucket will not rebuild. Retry the retryable
# statuses and let anything else fail immediately.
RETRY_STATUSES = frozenset({429, 500, 502, 503, 504})
MAX_ATTEMPTS = 5

ENDPOINT = os.environ.get("SPLUNK_FROZEN_S3_ENDPOINT", "")
BUCKET = os.environ.get("SPLUNK_FROZEN_S3_BUCKET", "")
KEY_ID = os.environ.get("SPLUNK_FROZEN_S3_KEY_ID", "")
APP_KEY = os.environ.get("SPLUNK_FROZEN_S3_APP_KEY", "")


def _region_from_endpoint(endpoint):
    host = endpoint.split("://", 1)[-1].strip("/")
    parts = host.split(".")
    if len(parts) >= 3 and parts[0] == "s3":
        return parts[1]
    return ""


REGION = os.environ.get("SPLUNK_FROZEN_S3_REGION", "") or _region_from_endpoint(ENDPOINT)


def _sign(key, msg):
    return hmac.new(key, msg.encode("utf-8"), hashlib.sha256).digest()


def _request(method, path, query=""):
    """Signed request with bounded retry on transient failures."""
    last = None
    for attempt in range(MAX_ATTEMPTS):
        try:
            return _request_once(method, path, query)
        except urllib.error.HTTPError as exc:
            last = exc
            if exc.code not in RETRY_STATUSES:
                raise
        except urllib.error.URLError as exc:
            last = exc
        # Signing is time-based, so each attempt re-signs rather than replaying
        # a stale signature.
        time.sleep(2 ** attempt)
    raise last if last is not None else RuntimeError("request failed with no error recorded")


def _request_once(method, path, query=""):
    host = ENDPOINT.split("://", 1)[-1].rstrip("/")
    now = datetime.datetime.now(datetime.timezone.utc)
    amzdate = now.strftime("%Y%m%dT%H%M%SZ")
    datestamp = now.strftime("%Y%m%d")
    payload_hash = hashlib.sha256(b"").hexdigest()

    canonical_headers = (
        "host:%s\nx-amz-content-sha256:%s\nx-amz-date:%s\n" % (host, payload_hash, amzdate)
    )
    signed_headers = "host;x-amz-content-sha256;x-amz-date"
    canonical_request = "\n".join(
        [method, path, query, canonical_headers, signed_headers, payload_hash]
    )
    scope = "%s/%s/s3/aws4_request" % (datestamp, REGION)
    string_to_sign = "\n".join(
        [
            "AWS4-HMAC-SHA256",
            amzdate,
            scope,
            hashlib.sha256(canonical_request.encode("utf-8")).hexdigest(),
        ]
    )
    key = _sign(("AWS4" + APP_KEY).encode("utf-8"), datestamp)
    for part in (REGION, "s3", "aws4_request"):
        key = _sign(key, part)
    signature = hmac.new(key, string_to_sign.encode("utf-8"), hashlib.sha256).hexdigest()

    url = "%s%s" % (ENDPOINT.rstrip("/"), path)
    if query:
        url += "?" + query
    req = urllib.request.Request(url, method=method)
    req.add_header("Host", host)
    req.add_header("x-amz-date", amzdate)
    req.add_header("x-amz-content-sha256", payload_hash)
    req.add_header(
        "Authorization",
        "AWS4-HMAC-SHA256 Credential=%s/%s, SignedHeaders=%s, Signature=%s"
        % (KEY_ID, scope, signed_headers, signature),
    )
    return urllib.request.urlopen(req, timeout=300)


def list_keys(prefix):
    keys = []
    token = None
    while True:
        query = "list-type=2&prefix=" + urllib.parse.quote(prefix, safe="")
        if token:
            query += "&continuation-token=" + urllib.parse.quote(token, safe="")
        body = _request("GET", "/" + BUCKET, query).read().decode()
        keys.extend(re.findall(r"<Key>([^<]+)</Key>", body))
        truncated = "<IsTruncated>true</IsTruncated>" in body
        if not truncated:
            break
        match = re.search(r"<NextContinuationToken>([^<]+)</NextContinuationToken>", body)
        if not match:
            break
        token = match.group(1)
    return keys


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        return 2
    for name, value in (("endpoint", ENDPOINT), ("bucket", BUCKET), ("key id", KEY_ID)):
        if not value:
            print("missing config: %s" % name)
            return 1

    action = sys.argv[1]

    if action == "list":
        scope = (sys.argv[2] + "/") if len(sys.argv) > 2 else ""
        buckets = sorted({"/".join(k.split("/")[:2]) for k in list_keys(scope)})
        for entry in buckets:
            print(entry)
        print("\n%d archived bucket(s)" % len(buckets))
        return 0

    if action == "fetch":
        if len(sys.argv) < 5:
            print("usage: restore_from_frozen.py fetch <index> <bucket_id> <dest_dir>")
            return 2
        index, bucket_id, dest = sys.argv[2], sys.argv[3], sys.argv[4]
        scope = "%s/%s/" % (index, bucket_id)
        keys = list_keys(scope)
        if not keys:
            print("nothing archived under %s" % scope)
            return 1
        target = os.path.join(dest, bucket_id)
        os.makedirs(target, exist_ok=True)
        for key in keys:
            rel = key[len(scope):]
            out = os.path.join(target, rel)
            os.makedirs(os.path.dirname(out), exist_ok=True)
            data = _request("GET", "/%s/%s" % (BUCKET, key)).read()
            with open(out, "wb") as fh:
                fh.write(data)
            print("restored %s (%d bytes)" % (rel, len(data)))
        print(
            "\n%d file(s) into %s\nNow: move it under the index thawedPath, run "
            "'splunk rebuild <dir>', restart splunkd, and remember thawed data "
            "never ages out on its own." % (len(keys), target)
        )
        return 0

    print("unknown action: %s" % action)
    return 2


if __name__ == "__main__":
    sys.exit(main())
