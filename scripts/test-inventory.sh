#!/usr/bin/env bash
# Test inventory loading and OpenTofu output structure
#
# Usage:
#   ./scripts/test-inventory.sh          # Fixture-based tests only
#   ./scripts/test-inventory.sh --live   # Include live inventory validation
set -euo pipefail

# Color output helpers
readonly RED='\033[0;31m'
readonly GREEN='\033[0;32m'
readonly YELLOW='\033[1;33m'
readonly NC='\033[0m'

PASS=0
FAIL=0
SKIP=0
LIVE=false

# Parse args
for arg in "$@"; do
  case "$arg" in
    --live) LIVE=true ;;
  esac
done

# Get project root
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "${SCRIPT_DIR}")"

pass() { echo -e "${GREEN}  PASS${NC}: $1"; PASS=$((PASS + 1)); }
fail() { echo -e "${RED}  FAIL${NC}: $1"; FAIL=$((FAIL + 1)); }
skip() { echo -e "${YELLOW}  SKIP${NC}: $1"; SKIP=$((SKIP + 1)); }

# ============================================================
# Section 1: Example file structure
# ============================================================
echo ""
echo "=== Example File Structure ==="

EXAMPLE_FILE="${PROJECT_ROOT}/inventory/tofu_inventory.json.example"

if [[ -f "${EXAMPLE_FILE}" ]]; then
  # Validate splunk_vm is at root level (not nested under ansible_inventory)
  if python3 - "${EXAMPLE_FILE}" << 'PYEOF'
import json, sys
with open(sys.argv[1]) as f:
    data = json.load(f)
if 'splunk_vm' not in data:
    print("  splunk_vm key missing from root", file=sys.stderr)
    sys.exit(1)
if 'ansible_inventory' in data:
    print("  ansible_inventory wrapper found (should be flat)", file=sys.stderr)
    sys.exit(1)
sys.exit(0)
PYEOF
  then
    pass "Example file has splunk_vm at root level"
  else
    fail "Example file structure is incorrect"
  fi

  # Validate expected nested keys exist
  if python3 - "${EXAMPLE_FILE}" << 'PYEOF'
import json, sys
with open(sys.argv[1]) as f:
    data = json.load(f)
splunk = data.get('splunk_vm', {}).get('splunk', {})
for key in ('hostname', 'ip', 'vmid'):
    if key not in splunk:
        print(f"  Missing key: splunk_vm.splunk.{key}", file=sys.stderr)
        sys.exit(1)
sys.exit(0)
PYEOF
  then
    pass "Example file has required splunk_vm.splunk fields"
  else
    fail "Example file missing required fields"
  fi
else
  fail "Example file not found: ${EXAMPLE_FILE}"
fi

# ============================================================
# Section 2: Ansible load_tofu.yml syntax check
# ============================================================
echo ""
echo "=== Ansible Syntax Check ==="

LOAD_TOFU="${PROJECT_ROOT}/inventory/load_tofu.yml"

if command -v ansible-playbook &>/dev/null; then
  if [[ -f "${LOAD_TOFU}" ]]; then
    if ansible-playbook --syntax-check "${LOAD_TOFU}" &>/dev/null; then
      pass "load_tofu.yml passes syntax check"
    else
      fail "load_tofu.yml fails syntax check"
    fi
  else
    fail "load_tofu.yml not found"
  fi
else
  skip "ansible-playbook not in PATH"
fi

# ============================================================
# Section 3: splunk_vm fixture-shape parsing
# ============================================================
echo ""
echo "=== Sync Script Python Parsing ==="

# Create a temporary fixture matching real OpenTofu output structure
FIXTURE_JSON=$(mktemp)
trap 'rm -f "${FIXTURE_JSON}"' EXIT

cat > "${FIXTURE_JSON}" << 'JSON_EOF'
{
  "splunk_vm": {
    "splunk": {
      "hostname": "test-splunk",
      "ip": "192.168.0.200",
      "vmid": 200,
      "ansible_connection": "ssh",
      "node": "test-node"
    }
  },
  "containers": {},
  "docker_vms": {},
  "vms": {}
}
JSON_EOF

# Parse the splunk_vm entry the way inventory/load_tofu.yml consumes it
OUTPUT=$(python3 - "${FIXTURE_JSON}" << 'PYEOF'
import json, sys
with open(sys.argv[1]) as f:
    inventory = json.load(f)
splunk = inventory.get('splunk_vm', {})
splunk_vm_details = splunk.get('splunk')
if isinstance(splunk_vm_details, dict):
    print(f"hostname={splunk_vm_details.get('hostname', 'splunk')}")
    print(f"ip={splunk_vm_details.get('ip', 'N/A')}")
    print(f"vmid={splunk_vm_details.get('vmid', 'N/A')}")
else:
    print("ERROR: No splunk VM found", file=sys.stderr)
    sys.exit(1)
PYEOF
)

if echo "${OUTPUT}" | grep -q "hostname=test-splunk"; then
  pass "Fixture parses hostname correctly"
else
  fail "Fixture hostname parsing failed"
fi

if echo "${OUTPUT}" | grep -q "ip=192.168.0.200"; then
  pass "Fixture parses IP correctly"
else
  fail "Fixture IP parsing failed"
fi

if echo "${OUTPUT}" | grep -q "vmid=200"; then
  pass "Fixture parses vmid correctly"
else
  fail "Fixture vmid parsing failed"
fi

# ============================================================
# Section 4: Live inventory (--live only)
# ============================================================
echo ""
echo "=== Live Inventory Validation ==="

# There is no on-disk cache to validate any more — the published object is the
# only live source. Validate whatever TOFU_INVENTORY_PATH pins, which is the
# same tier-1 input a converge would use.
LIVE_FILE="${TOFU_INVENTORY_PATH:-}"

if [[ "${LIVE}" == "true" ]]; then
  if [[ -f "${LIVE_FILE}" ]]; then
    pass "Live inventory file exists"

    # Validate flat structure with splunk_vm at root
    if python3 - "${LIVE_FILE}" << 'PYEOF'
import json, sys
with open(sys.argv[1]) as f:
    data = json.load(f)
if 'splunk_vm' not in data:
    print("  splunk_vm missing from root", file=sys.stderr)
    sys.exit(1)
if 'ansible_inventory' in data:
    print("  Found ansible_inventory wrapper (should be flat)", file=sys.stderr)
    sys.exit(1)
splunk = data.get('splunk_vm', {}).get('splunk', {})
for key in ('hostname', 'ip', 'vmid'):
    if key not in splunk:
        print(f"  Missing key: splunk_vm.splunk.{key}", file=sys.stderr)
        sys.exit(1)
sys.exit(0)
PYEOF
    then
      pass "Live inventory has correct flat structure"
    else
      fail "Live inventory structure is incorrect"
    fi
  elif [[ -z "${LIVE_FILE}" ]]; then
    fail "--live needs TOFU_INVENTORY_PATH set to a copy fetched from the published object"
  else
    fail "Live inventory file not found: ${LIVE_FILE}"
  fi
else
  skip "Live inventory tests (pass --live to enable)"
fi

# ============================================================
# Summary
# ============================================================
echo ""
echo "================================"
echo -e "Results: ${GREEN}${PASS} passed${NC}, ${RED}${FAIL} failed${NC}, ${YELLOW}${SKIP} skipped${NC}"
if [[ ${FAIL} -gt 0 ]]; then
  exit 1
fi
