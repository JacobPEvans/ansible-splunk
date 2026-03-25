# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.6.1](https://github.com/JacobPEvans/ansible-splunk/compare/v0.6.0...v0.6.1) (2026-03-20)

### Bug Fixes

* use selectattr 'defined' test for github_repo filter ([#101](https://github.com/JacobPEvans/ansible-splunk/issues/101)) ([409cdea](https://github.com/JacobPEvans/ansible-splunk/commit/409cdeae623b2f2d7789289c98d3bc89c60435ca))

## [0.6.0](https://github.com/JacobPEvans/ansible-splunk/compare/v0.5.0...v0.6.0) (2026-03-19)

### Features

* add daily repo health audit agentic workflow ([#91](https://github.com/JacobPEvans/ansible-splunk/issues/91)) ([d7e0880](https://github.com/JacobPEvans/ansible-splunk/commit/d7e08806a03481984477c529b8a1da68b9e80c88))
* add gemini, openai, and vscode splunk indexes ([#72](https://github.com/JacobPEvans/ansible-splunk/issues/72)) ([8a7116b](https://github.com/JacobPEvans/ansible-splunk/commit/8a7116b62f6566b357244a8800bda1ad9d92682f))
* add gh-aw agentic workflows for CI, security, and moderation ([#61](https://github.com/JacobPEvans/ansible-splunk/issues/61)) ([75ad4bc](https://github.com/JacobPEvans/ansible-splunk/commit/75ad4bcbf6d0e3733d93654e12429395c81727ee))
* add MCP client config, best practices docs, and splunk.splunk role ([#51](https://github.com/JacobPEvans/ansible-splunk/issues/51)) ([2791192](https://github.com/JacobPEvans/ansible-splunk/commit/2791192419557a19b3b96560ba45bc0955a0e529))
* add PSC, MLTK, and DSDL validation checks ([#49](https://github.com/JacobPEvans/ansible-splunk/issues/49)) ([c9338d5](https://github.com/JacobPEvans/ansible-splunk/commit/c9338d57d489750a1d5d25103febaad9998d6d9d))
* add scheduled AI workflow callers ([#69](https://github.com/JacobPEvans/ansible-splunk/issues/69)) ([b04201e](https://github.com/JacobPEvans/ansible-splunk/commit/b04201e35b6d76ae63f1bdf3aad4915033659a83))
* add VisiCore AI Observability packages v1.0.0 ([#86](https://github.com/JacobPEvans/ansible-splunk/issues/86)) ([cd61bba](https://github.com/JacobPEvans/ansible-splunk/commit/cd61bbad03534d86920bbdd26783aa5bbdd49a7f))
* adopt conventional branch standard (feature/, bugfix/, chore/) ([#66](https://github.com/JacobPEvans/ansible-splunk/issues/66)) ([0702858](https://github.com/JacobPEvans/ansible-splunk/commit/0702858d7267d996ee33d36ba926357cff52d586))
* auto-configure DB Connect JAVA_HOME ([#52](https://github.com/JacobPEvans/ansible-splunk/issues/52)) ([e0fd0d5](https://github.com/JacobPEvans/ansible-splunk/commit/e0fd0d52d8ad5c10d5361fb7f7db0365ddde1327))
* deploy Splunk MCP Server for AI assistant integration ([#50](https://github.com/JacobPEvans/ansible-splunk/issues/50)) ([0ff84fa](https://github.com/JacobPEvans/ansible-splunk/commit/0ff84fa8ba8adfc21d703cd7778daaf17307e37c))
* disable automatic triggers on Claude-executing workflows ([b1f34ce](https://github.com/JacobPEvans/ansible-splunk/commit/b1f34ce0b06559ceaca650cc6ef7f0a9baf71d6f))
* download VisiCore add-ons from GitHub Releases automatically ([#89](https://github.com/JacobPEvans/ansible-splunk/issues/89)) ([81565a0](https://github.com/JacobPEvans/ansible-splunk/commit/81565a04e8f3ab5f05a69b3f1bfa7b1c201313ad))
* enforce required Splunk apps with fail-fast validation ([#90](https://github.com/JacobPEvans/ansible-splunk/issues/90)) ([c13e27d](https://github.com/JacobPEvans/ansible-splunk/commit/c13e27d24bf94f94122ac44f1785822a80f33cd7))
* per-index HEC tokens via UUID v5 derivation ([8baabc3](https://github.com/JacobPEvans/ansible-splunk/commit/8baabc3288fa4f3ebcdbf09b2d98a2a5e72cc702))
* **renovate:** extend shared preset, remove duplicated rules ([7a21afb](https://github.com/JacobPEvans/ansible-splunk/commit/7a21afb124a8c96e1f7f3670dfedcdd349521560))

### Bug Fixes

* **ci:** add pull-requests: write for release-please auto-approval ([#97](https://github.com/JacobPEvans/ansible-splunk/issues/97)) ([c2112c1](https://github.com/JacobPEvans/ansible-splunk/commit/c2112c1878dd6502c8fd029c5b0607334c13e135))
* **ci:** implement Merge Gatekeeper pattern with ci-gate ([#93](https://github.com/JacobPEvans/ansible-splunk/issues/93)) ([90a173b](https://github.com/JacobPEvans/ansible-splunk/commit/90a173b864aa175072e881a9fc6451bdc39eacaa))
* **ci:** use GitHub App token for release-please to trigger CI Gate ([#92](https://github.com/JacobPEvans/ansible-splunk/issues/92)) ([4ac143f](https://github.com/JacobPEvans/ansible-splunk/commit/4ac143f043c041d1640f3e1c190c9494ce043c21))
* correct HEC protocol documentation from HTTP to HTTPS ([#95](https://github.com/JacobPEvans/ansible-splunk/issues/95)) ([c91a757](https://github.com/JacobPEvans/ansible-splunk/commit/c91a757958ebe4f1bdf847e339f527ec2a23ced2))
* grant contents: write for release-please workflow ([d5b6ec2](https://github.com/JacobPEvans/ansible-splunk/commit/d5b6ec25392427b202cbb92a37bb8218f3dad977))
* make Molecule idempotence check deterministic ([#55](https://github.com/JacobPEvans/ansible-splunk/issues/55)) ([b8b9741](https://github.com/JacobPEvans/ansible-splunk/commit/b8b97413bf35934d6256ebc7e8d6e55dfcaf08aa))
* migrate release-please config to packages format ([4090064](https://github.com/JacobPEvans/ansible-splunk/commit/4090064b5895eafd967198f7979c9ec33be3d37a))
* use packages attr, add doppler, gitignore .direnv ([#78](https://github.com/JacobPEvans/ansible-splunk/issues/78)) ([2a05c4f](https://github.com/JacobPEvans/ansible-splunk/commit/2a05c4f0f8bf50281e9c2e9bb13774bebb7bea1c))

### Performance

* **ci:** cut Molecule runtime from ~30min to ~8min ([#56](https://github.com/JacobPEvans/ansible-splunk/issues/56)) ([ef179a4](https://github.com/JacobPEvans/ansible-splunk/commit/ef179a40513e328f3feb59cfb3d18e9f80a2901a))

## [Unreleased]

## [0.5.0] - 2026-02-26

### Added

* Configure HEC token via inputs.conf template (#31)
* Add JRE-21 and Splunk DB Connect support (#30)
* Add `ai` and `claude` Splunk indexes (#24)
* Add `netflow` index for NetFlow/IPFIX data (#16)
* Pipeline sync: standardize env vars, fix HEC config (#19)

### Fixed

* Use `include_role` in post_tasks so role defaults are available (#35)
* Remove quotes from inputs.conf values and add post-restart health check (#34)
* Use `ansible_facts` dict to avoid `INJECT_FACTS_AS_VARS` deprecation (#33)
* Allow all custom indexes in HEC token (#32)
* Correct `splunk_vm` key path in `load_terraform.yml` (#25)
* Disable internet access checks for air-gapped Splunk VM (#23)
* Complete pipeline sync: license, inventory paths, HEC config (#20)
* Disable guest iptables in favor of Proxmox firewall (#14)

### Changed

* Rewrite README for accuracy and AI-agent readability (fixes role name,
  retention values, variable names, and missing indexes)
* Config standardization and CI dedup (#37)
* Consolidated to single `splunk_docker` role (previously multiple roles)
* All variable names prefixed with `splunk_docker_` for ansible-lint compliance

## [0.2.0] - 2026-01-18

### Fixed

* **BREAKING**: Fixed Doppler secret retrieval - now correctly uses
  `SPLUNK_PASSWORD` and `SPLUNK_HEC_TOKEN` environment variables instead
  of incorrectly using `DOPPLER_TOKEN` value as credentials
* Improved error message for missing environment variables with usage hint

### Added

* Dynamic Terraform inventory integration via `load_terraform.yml` playbook
* `scripts/sync-terraform-inventory.sh` script to export Terraform outputs
* Validation playbook (`playbooks/validate.yml`) for deployed Splunk instances
* Molecule test framework with Docker driver for automated testing
* GitHub Actions workflows for linting, molecule tests, and syntax validation
* CONTRIBUTING.md with development guidelines
* CHANGELOG.md for version tracking

### Changed

* `playbooks/site.yml` now imports dynamic inventory before deployment
* `inventory/hosts.yml` updated to support both static and dynamic inventory
* README.md enhanced with testing, CI/CD, and Doppler setup documentation

## [0.1.0] - 2026-01-17

Initial release with core Splunk Enterprise deployment automation.

**Features:**

* Splunk Enterprise 9.1.1 deployment automation
* Data disk mounting and formatting for persistent storage
* Index configuration (main, `_internal`, `_audit`)
* HTTP Event Collector (HEC) input setup
* Syslog input configuration on port 1514
* Systemd service management with boot-start
* Admin password and HEC token from Doppler
* Comprehensive README documentation
* Pre-commit hooks for YAML and markdown linting
* ansible-lint configuration
