#!/usr/bin/env bash
# Download required Splunkbase apps via REST API
# Requires SPLUNKBASE_USERNAME and SPLUNKBASE_PASSWORD (from Doppler)
# Usage: doppler run -- ./scripts/download-splunkbase-apps.sh
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
FILES_DIR="${SCRIPT_DIR}/../roles/splunk_docker/files"
APPS_YML="${SCRIPT_DIR}/../roles/splunk_docker/vars/splunkbase_apps.yml"

if [[ -z "${SPLUNKBASE_USERNAME:-}" ]] || [[ -z "${SPLUNKBASE_PASSWORD:-}" ]]; then
    echo "ERROR: SPLUNKBASE_USERNAME and SPLUNKBASE_PASSWORD must be set"
    echo "Run with: doppler run -- $0"
    exit 1
fi

echo "Authenticating to Splunkbase..."
AUTH_RESPONSE=$(curl -sS -X POST \
    "https://splunkbase.splunk.com/api/account:login/" \
    -d "username=${SPLUNKBASE_USERNAME}&password=${SPLUNKBASE_PASSWORD}")

TOKEN=$(echo "$AUTH_RESPONSE" | sed -n 's/.*<id>\([^<]*\)<\/id>.*/\1/p')
if [[ -z "$TOKEN" ]]; then
    echo "ERROR: Authentication failed"
    echo "$AUTH_RESPONSE"
    exit 1
fi
echo "Authenticated successfully"

_yaml_val() { echo "$1" | sed 's/^[^:]*: *//; s/^"//; s/"$//; s/ *$//'; }

DOWNLOAD_COUNT=0
SKIP_COUNT=0
FAIL_COUNT=0
APP_ID="" APP_VERSION="" APP_FILENAME="" APP_ENABLED="" APP_REQUIRED=""

while IFS= read -r line; do
    [[ "$line" =~ ^[[:space:]]*# ]] && continue
    [[ -z "${line// /}" ]] && continue
    case "$line" in
        *"splunkbase_id:"*)
            APP_ID=$(_yaml_val "$line")
            ;;
        *"version:"*)
            APP_VERSION=$(_yaml_val "$line")
            ;;
        *"filename:"*)
            APP_FILENAME=$(_yaml_val "$line")
            ;;
        *"enabled:"*)
            APP_ENABLED=$(_yaml_val "$line")
            ;;
        *"required:"*)
            APP_REQUIRED=$(_yaml_val "$line")

            if [[ "$APP_ENABLED" != "true" ]]; then
                echo "SKIP: ${APP_FILENAME} (disabled)"
                SKIP_COUNT=$((SKIP_COUNT + 1))
                continue
            fi

            TARGET="${FILES_DIR}/${APP_FILENAME}"
            if [[ -f "$TARGET" ]]; then
                echo "EXISTS: ${APP_FILENAME}"
                SKIP_COUNT=$((SKIP_COUNT + 1))
                continue
            fi

            echo -n "DOWNLOADING: ${APP_FILENAME} (Splunkbase #${APP_ID} v${APP_VERSION})... "
            HTTP_CODE=$(curl -sS -L \
                -H "X-Auth-Token: ${TOKEN}" \
                -o "${TARGET}" \
                -w "%{http_code}" \
                "https://splunkbase.splunk.com/app/${APP_ID}/release/${APP_VERSION}/download/" 2>&1)

            if [[ "$HTTP_CODE" == "200" ]] && [[ -s "$TARGET" ]]; then
                FILE_SIZE=$(du -h "$TARGET" | cut -f1)
                echo "OK (${FILE_SIZE})"
                DOWNLOAD_COUNT=$((DOWNLOAD_COUNT + 1))
            else
                echo "FAILED (HTTP ${HTTP_CODE})"
                rm -f "$TARGET"
                FAIL_COUNT=$((FAIL_COUNT + 1))
                if [[ "$APP_REQUIRED" == "true" ]]; then
                    echo "  ERROR: Required app failed to download"
                    echo "  Manual download: https://splunkbase.splunk.com/app/${APP_ID}"
                fi
            fi
            ;;
    esac
done < "$APPS_YML"

echo ""
echo "Summary: ${DOWNLOAD_COUNT} downloaded, ${SKIP_COUNT} skipped, ${FAIL_COUNT} failed"

if [[ $FAIL_COUNT -gt 0 ]]; then
    exit 1
fi
