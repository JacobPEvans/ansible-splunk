# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.5.0] - 2026-02-26

### Added

- Configure HEC token via inputs.conf template (#31)
- Add JRE-21 and Splunk DB Connect support (#30)
- Add `ai` and `claude` Splunk indexes (#24)
- Add `netflow` index for NetFlow/IPFIX data (#16)
- Pipeline sync: standardize env vars, fix HEC config (#19)

### Fixed

- Use `include_role` in post_tasks so role defaults are available (#35)
- Remove quotes from inputs.conf values and add post-restart health check (#34)
- Use `ansible_facts` dict to avoid `INJECT_FACTS_AS_VARS` deprecation (#33)
- Allow all custom indexes in HEC token (#32)
- Correct `splunk_vm` key path in `load_terraform.yml` (#25)
- Disable internet access checks for air-gapped Splunk VM (#23)
- Complete pipeline sync: license, inventory paths, HEC config (#20)
- Disable guest iptables in favor of Proxmox firewall (#14)

### Changed

- Rewrite README for accuracy and AI-agent readability (fixes role name,
  retention values, variable names, and missing indexes)
- Config standardization and CI dedup (#37)
- Consolidated to single `splunk_docker` role (previously multiple roles)
- All variable names prefixed with `splunk_docker_` for ansible-lint compliance

## [0.2.0] - 2026-01-18

### Fixed

- **BREAKING**: Fixed Doppler secret retrieval - now correctly uses
  `SPLUNK_PASSWORD` and `SPLUNK_HEC_TOKEN` environment variables instead
  of incorrectly using `DOPPLER_TOKEN` value as credentials
- Improved error message for missing environment variables with usage hint

### Added

- Dynamic Terraform inventory integration via `load_terraform.yml` playbook
- `scripts/sync-terraform-inventory.sh` script to export Terraform outputs
- Validation playbook (`playbooks/validate.yml`) for deployed Splunk instances
- Molecule test framework with Docker driver for automated testing
- GitHub Actions workflows for linting, molecule tests, and syntax validation
- CONTRIBUTING.md with development guidelines
- CHANGELOG.md for version tracking

### Changed

- `playbooks/site.yml` now imports dynamic inventory before deployment
- `inventory/hosts.yml` updated to support both static and dynamic inventory
- README.md enhanced with testing, CI/CD, and Doppler setup documentation

## [0.1.0] - 2026-01-17

Initial release with core Splunk Enterprise deployment automation.

**Features:**

- Splunk Enterprise 9.1.1 deployment automation
- Data disk mounting and formatting for persistent storage
- Index configuration (main, `_internal`, `_audit`)
- HTTP Event Collector (HEC) input setup
- Syslog input configuration on port 1514
- Systemd service management with boot-start
- Admin password and HEC token from Doppler
- Comprehensive README documentation
- Pre-commit hooks for YAML and markdown linting
- ansible-lint configuration
