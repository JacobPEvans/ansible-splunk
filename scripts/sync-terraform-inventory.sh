#!/usr/bin/env bash
# Sync Terraform inventory to Ansible
#
# This script exports the Terraform-defined Splunk VM infrastructure
# to a JSON file that Ansible can dynamically load via load_terraform.yml
#
# Usage:
#   ./scripts/sync-terraform-inventory.sh
#   TERRAFORM_DIR=/custom/path ./scripts/sync-terraform-inventory.sh
#
# This should be run after 'terragrunt apply' in terraform-proxmox to ensure
# Ansible has the latest Splunk VM configuration.

set -euo pipefail

# Color output helpers
readonly RED='\033[0;31m'
readonly GREEN='\033[0;32m'
readonly YELLOW='\033[1;33m'
readonly NC='\033[0m' # No Color

# Get the directory where this script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Navigate to project root (parent of scripts directory)
PROJECT_ROOT="$(dirname "${SCRIPT_DIR}")"

# Path to Terraform infrastructure (configurable via environment variable)
TERRAFORM_DIR="${TERRAFORM_DIR:-${HOME}/git/terraform-proxmox/main}"

# Path to Ansible inventory file
INVENTORY_FILE="${PROJECT_ROOT}/inventory/terraform_inventory.json"

# Ensure terraform directory exists
if [[ ! -d "${TERRAFORM_DIR}" ]]; then
  echo -e "${RED}ERROR: Terraform directory not found at ${TERRAFORM_DIR}${NC}" >&2
  exit 1
fi

# Ensure Ansible project directory exists
if [[ ! -d "${PROJECT_ROOT}" ]]; then
  echo -e "${RED}ERROR: Ansible project directory not found at ${PROJECT_ROOT}${NC}" >&2
  exit 1
fi

echo -e "${YELLOW}Exporting Terraform inventory...${NC}"
echo "  Terraform dir: ${TERRAFORM_DIR}"
echo "  Output file:   ${INVENTORY_FILE}"

# Change to Terraform directory and export inventory
if cd "${TERRAFORM_DIR}" && terragrunt output -json ansible_inventory > "${INVENTORY_FILE}"; then
  echo -e "${GREEN}Inventory exported successfully${NC}"

  # Show summary of exported infrastructure
  echo -e "\n${YELLOW}Infrastructure Summary:${NC}"

  # Use Python to parse and display the JSON in a readable format
  python3 "${INVENTORY_FILE}" << 'PYTHON_EOF'
import json
import sys

try:
    with open(sys.argv[1]) as f:
        inventory = json.load(f)

        splunk = inventory.get('ansible_inventory', {}).get('splunk_vm', {})
        splunk_vm_details = splunk.get('splunk')
        if isinstance(splunk_vm_details, dict):
            print(f"  Splunk VM:")
            print(f"    - hostname: {splunk_vm_details.get('hostname', 'splunk')}")
            print(f"    - ip:       {splunk_vm_details.get('ip', 'N/A')}")
            print(f"    - vmid:     {splunk_vm_details.get('vmid', 'N/A')}")
        else:
            print("  No Splunk VM found in Terraform outputs")
            print("  Ensure terraform-proxmox has splunk_vm in ansible_inventory output")

except Exception as e:
    print(f"  (Could not parse inventory: {e})", file=sys.stderr)
PYTHON_EOF

  echo -e "\n${GREEN}Ansible can now use this inventory via 'load_terraform.yml'${NC}"
else
  echo -e "${RED}ERROR: Failed to export Terraform inventory${NC}" >&2
  exit 1
fi
