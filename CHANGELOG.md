# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.24.1](https://github.com/dryvist/ansible-splunk/compare/v0.24.0...v0.24.1) (2026-07-05)


### Bug Fixes

* **playbooks:** align Splunk guest network with tofu inventory via guest agent ([#295](https://github.com/dryvist/ansible-splunk/issues/295)) ([5307125](https://github.com/dryvist/ansible-splunk/commit/5307125306623250b86b151eeb97093bb83f8477))

## [0.24.0](https://github.com/dryvist/ansible-splunk/compare/v0.23.0...v0.24.0) (2026-07-05)


### Features

* **alerts:** per-host LLM silence + LiteLLM router and model-eval alerts ([#294](https://github.com/dryvist/ansible-splunk/issues/294)) ([2dd80c4](https://github.com/dryvist/ansible-splunk/commit/2dd80c4ccafa72cb441b628ff2f87167151f787e))

## [0.23.0](https://github.com/dryvist/ansible-splunk/compare/v0.22.5...v0.23.0) (2026-07-03)


### Features

* add AI PR care caller (dep review + release highlights) ([#292](https://github.com/dryvist/ansible-splunk/issues/292)) ([60e647d](https://github.com/dryvist/ansible-splunk/commit/60e647ddfa0c4aa639a995771c2fc0eecbbf8045))

## [0.22.5](https://github.com/dryvist/ansible-splunk/compare/v0.22.4...v0.22.5) (2026-07-02)


### Bug Fixes

* **ci:** restore CI Fix auto-trigger as a thin cc-ci-fix wrapper ([ed61e6e](https://github.com/dryvist/ansible-splunk/commit/ed61e6e5b5aedb30301c2b417aa240f50d2fc948))

## [0.22.4](https://github.com/dryvist/ansible-splunk/compare/v0.22.3...v0.22.4) (2026-07-02)


### Bug Fixes

* point callers at renamed cc- reusable workflows ([5b9dd70](https://github.com/dryvist/ansible-splunk/commit/5b9dd701c01487e300138fac3ee813a7cfde9f6e))

## [0.22.3](https://github.com/dryvist/ansible-splunk/compare/v0.22.2...v0.22.3) (2026-06-22)


### Bug Fixes

* **splunk:** auto-reconcile admin password with SPLUNK_PASSWORD ([#282](https://github.com/dryvist/ansible-splunk/issues/282)) ([d3718b1](https://github.com/dryvist/ansible-splunk/commit/d3718b1eb039a10af1f4bc5db31c0a97bd2a5264))

## [0.22.2](https://github.com/dryvist/ansible-splunk/compare/v0.22.1...v0.22.2) (2026-06-22)


### Bug Fixes

* **ntp:** scope remote_tmp to chrony validate so site.yml deploys ([#274](https://github.com/dryvist/ansible-splunk/issues/274)) ([3196e35](https://github.com/dryvist/ansible-splunk/commit/3196e35a25ba8a9c2d0a53755080febddfcb3b65))

## [0.22.1](https://github.com/dryvist/ansible-splunk/compare/v0.22.0...v0.22.1) (2026-06-21)


### Bug Fixes

* **splunk:** repoint Splunkbase sync MinIO → object-storage (RustFS) ([#276](https://github.com/dryvist/ansible-splunk/issues/276)) ([b318baa](https://github.com/dryvist/ansible-splunk/commit/b318baa86045852065eade5c9bb823ad0d6616a0))

## [0.22.0](https://github.com/dryvist/ansible-splunk/compare/v0.21.0...v0.22.0) (2026-06-20)


### Features

* **ci:** re-validate inventory data contract on upstream release ([#275](https://github.com/dryvist/ansible-splunk/issues/275)) ([398b9f7](https://github.com/dryvist/ansible-splunk/commit/398b9f7a2b16b54bc4ea062e32952f54588907ba))

## [0.21.0](https://github.com/dryvist/ansible-splunk/compare/v0.20.0...v0.21.0) (2026-06-20)


### Features

* **splunk:** always-latest Splunkbase apps, air-gapped; fix install-once ([4096c02](https://github.com/dryvist/ansible-splunk/commit/4096c020f614e5122d64329a1ad82f8770636c77))

## [0.20.0](https://github.com/dryvist/ansible-splunk/compare/v0.19.3...v0.20.0) (2026-06-20)


### Features

* **inventory:** make S3 the sole live inventory source ([68492c2](https://github.com/dryvist/ansible-splunk/commit/68492c24868090d1f1cd9ea894604697c1fc9e47))

## [0.19.3](https://github.com/dryvist/ansible-splunk/compare/v0.19.2...v0.19.3) (2026-06-20)


### Bug Fixes

* **splunk:** rename metric index netmon -&gt; netmon_metrics ([#269](https://github.com/dryvist/ansible-splunk/issues/269)) ([1b110e0](https://github.com/dryvist/ansible-splunk/commit/1b110e0c4764b4d8dd7bf2e3b7bef2cef6d82859))

## [0.19.2](https://github.com/dryvist/ansible-splunk/compare/v0.19.1...v0.19.2) (2026-06-18)


### Bug Fixes

* **deps:** widen community.general ceiling to major (&lt;14.0.0) ([#265](https://github.com/dryvist/ansible-splunk/issues/265)) ([cde2389](https://github.com/dryvist/ansible-splunk/commit/cde2389d12800d78c6a2669515c720e3d5765dfd))

## [0.19.1](https://github.com/dryvist/ansible-splunk/compare/v0.19.0...v0.19.1) (2026-06-15)


### Bug Fixes

* **hec:** make per-index token activation work when HEC_NAMESPACE is set ([#260](https://github.com/dryvist/ansible-splunk/issues/260)) ([cee89e2](https://github.com/dryvist/ansible-splunk/commit/cee89e2045a93738eff98351198db2cbe04dbb52))

## [0.19.0](https://github.com/dryvist/ansible-splunk/compare/v0.18.0...v0.19.0) (2026-06-14)


### Features

* **hec:** decouple legacy token from namespace; use core to_uuid ([#256](https://github.com/dryvist/ansible-splunk/issues/256)) ([b80d1d4](https://github.com/dryvist/ansible-splunk/commit/b80d1d4560923579caa7e298ab62375d2b6537e6))
* **indexes:** add unifi_metrics + make unifi_metrics/netmon metric-datatype ([#255](https://github.com/dryvist/ansible-splunk/issues/255)) ([0f10945](https://github.com/dryvist/ansible-splunk/commit/0f109459fe1ade183f40fa67996034cef1baaa76))

## [0.18.0](https://github.com/dryvist/ansible-splunk/compare/v0.17.0...v0.18.0) (2026-06-14)


### Features

* **indexes:** add unifi_metrics index (90-day) for UniFi controller telemetry ([#253](https://github.com/dryvist/ansible-splunk/issues/253)) ([8d00e33](https://github.com/dryvist/ansible-splunk/commit/8d00e3340dd54fb59d7a22e9f65bb77aad21e933))

## [0.17.0](https://github.com/dryvist/ansible-splunk/compare/v0.16.0...v0.17.0) (2026-06-13)


### Features

* **splunk:** netflow index -&gt; 90-day retention + 50 GB cap ([#251](https://github.com/dryvist/ansible-splunk/issues/251)) ([65d14e7](https://github.com/dryvist/ansible-splunk/commit/65d14e7454c1d27be698ad9bef6eed6f06835011))

## [0.16.0](https://github.com/dryvist/ansible-splunk/compare/v0.15.0...v0.16.0) (2026-06-12)


### Features

* **indexes:** add llm index + pipeline-silence and manager-panic alerts ([#246](https://github.com/dryvist/ansible-splunk/issues/246)) ([3283b30](https://github.com/dryvist/ansible-splunk/commit/3283b30949e8a5d425a8f9193bf369addd45733e))
* **inventory:** resolve inventory S3-first via amazon.aws; DNS-first static fallback ([#249](https://github.com/dryvist/ansible-splunk/issues/249)) ([c3c26a8](https://github.com/dryvist/ansible-splunk/commit/c3c26a8caa56852eba7851739987ae5478405032))


### Bug Fixes

* **inventory:** remove dead cloud.terraform plugin enable; scrub deleted-script references ([#250](https://github.com/dryvist/ansible-splunk/issues/250)) ([24000b9](https://github.com/dryvist/ansible-splunk/commit/24000b96aeb2a6d34f12b6ba27ad12bd4f067c2d))

## [0.15.0](https://github.com/dryvist/ansible-splunk/compare/v0.14.4...v0.15.0) (2026-06-10)


### Features

* **indexes:** add netmon index with 90-day retention ([#244](https://github.com/dryvist/ansible-splunk/issues/244)) ([c44a1d8](https://github.com/dryvist/ansible-splunk/commit/c44a1d89cd224a911bccd726f9083d49dbe3c655))

## [0.14.4](https://github.com/dryvist/ansible-splunk/compare/v0.14.3...v0.14.4) (2026-06-03)


### Bug Fixes

* repoint retired-repo references to live canonical repos ([#239](https://github.com/dryvist/ansible-splunk/issues/239)) ([96f6a9f](https://github.com/dryvist/ansible-splunk/commit/96f6a9f16d9bc01d23732e7f9b9902ca84bf27f8))

## [0.14.3](https://github.com/dryvist/ansible-splunk/compare/v0.14.2...v0.14.3) (2026-06-03)


### Bug Fixes

* **release-please:** inherit dryvist/.github org-native caller ([#237](https://github.com/dryvist/ansible-splunk/issues/237)) ([06a70e0](https://github.com/dryvist/ansible-splunk/commit/06a70e06904725f721a1b68ed8b173d08e3c4796))

## [0.14.2](https://github.com/dryvist/ansible-splunk/compare/v0.14.1...v0.14.2) (2026-06-01)


### Bug Fixes

* **ci:** retarget reusable-workflow uses: refs to current org homes ([#230](https://github.com/dryvist/ansible-splunk/issues/230)) ([2ece34f](https://github.com/dryvist/ansible-splunk/commit/2ece34fb24bd40a3cc5dfecdd8f90186365c4afe))

## [0.14.1](https://github.com/JacobPEvans/ansible-splunk/compare/v0.14.0...v0.14.1) (2026-05-25)


### Bug Fixes

* **deps:** refresh gh-aw action SHA pins [aw:gh-aw-pin-refresh] ([#226](https://github.com/JacobPEvans/ansible-splunk/issues/226)) ([fdc79a5](https://github.com/JacobPEvans/ansible-splunk/commit/fdc79a538c1e2bf62b69804e975a2432f22df37e))

## [0.14.0](https://github.com/JacobPEvans/ansible-splunk/compare/v0.13.0...v0.14.0) (2026-05-24)


### Features

* **splunk:** add macOS Cribl Edge silence-detector saved search ([774cdf2](https://github.com/JacobPEvans/ansible-splunk/commit/774cdf2f857b4cce9521975f1b0f3e8b941e373f))

## [0.13.0](https://github.com/JacobPEvans/ansible-splunk/compare/v0.12.8...v0.13.0) (2026-05-24)


### Features

* **ntp:** vendor ntp role and configure Splunk VM client ([#203](https://github.com/JacobPEvans/ansible-splunk/issues/203)) ([4a464a3](https://github.com/JacobPEvans/ansible-splunk/commit/4a464a346ec449d99ace163286182eb6d56a7cb8)), closes [#200](https://github.com/JacobPEvans/ansible-splunk/issues/200)

## [0.12.8](https://github.com/JacobPEvans/ansible-splunk/compare/v0.12.7...v0.12.8) (2026-05-24)


### Bug Fixes

* **pre-commit:** exclude release-please CHANGELOG.md from markdownlint ([#220](https://github.com/JacobPEvans/ansible-splunk/issues/220)) ([a40f964](https://github.com/JacobPEvans/ansible-splunk/commit/a40f964d37be6a9e306f05a6b22363981ce8f695))

## [0.12.7](https://github.com/JacobPEvans/ansible-splunk/compare/v0.12.6...v0.12.7) (2026-05-22)


### Bug Fixes

* **deps:** refresh gh-aw action SHA pins ([#208](https://github.com/JacobPEvans/ansible-splunk/issues/208)) ([64dc073](https://github.com/JacobPEvans/ansible-splunk/commit/64dc073fd9a060e985bb6be9de980aa5670ed77b))

## [0.12.6](https://github.com/JacobPEvans/ansible-splunk/compare/v0.12.5...v0.12.6) (2026-05-18)


### Bug Fixes

* **deps:** refresh gh-aw action SHA pins ([#205](https://github.com/JacobPEvans/ansible-splunk/issues/205)) ([7a797bd](https://github.com/JacobPEvans/ansible-splunk/commit/7a797bd7b022f3cb27f5ad10cba99f674db67f57))

## [0.12.5](https://github.com/JacobPEvans/ansible-splunk/compare/v0.12.4...v0.12.5) (2026-05-14)


### Bug Fixes

* **deps:** refresh gh-aw action SHA pins ([#201](https://github.com/JacobPEvans/ansible-splunk/issues/201)) ([944454a](https://github.com/JacobPEvans/ansible-splunk/commit/944454a5377b87068c860da7595d7bf32496a039))

## [0.12.4](https://github.com/JacobPEvans/ansible-splunk/compare/v0.12.3...v0.12.4) (2026-05-11)


### Bug Fixes

* **deps:** refresh gh-aw action SHA pins ([#197](https://github.com/JacobPEvans/ansible-splunk/issues/197)) ([fe05bcd](https://github.com/JacobPEvans/ansible-splunk/commit/fe05bcd80f991b34df205b4a6004773b11f6cae2))

## [0.12.3](https://github.com/JacobPEvans/ansible-splunk/compare/v0.12.2...v0.12.3) (2026-05-07)


### Bug Fixes

* **deps:** refresh gh-aw action SHA pins ([#194](https://github.com/JacobPEvans/ansible-splunk/issues/194)) ([16a18fc](https://github.com/JacobPEvans/ansible-splunk/commit/16a18fcc6600b245ed530fc3d48c0ba911254e73))

## [0.12.2](https://github.com/JacobPEvans/ansible-splunk/compare/v0.12.1...v0.12.2) (2026-05-04)


### Bug Fixes

* **deps:** refresh gh-aw action SHA pins ([#191](https://github.com/JacobPEvans/ansible-splunk/issues/191)) ([c28e4d0](https://github.com/JacobPEvans/ansible-splunk/commit/c28e4d0e7e40e13a8f08906a9cb3878d615870b3))

## [0.12.1](https://github.com/JacobPEvans/ansible-splunk/compare/v0.12.0...v0.12.1) (2026-05-03)


### Bug Fixes

* **ci:** remove deprecated app-id secret passthrough ([6ef226f](https://github.com/JacobPEvans/ansible-splunk/commit/6ef226f39bf5ab3dbd2674034d240d496524a476))

## [0.12.0](https://github.com/JacobPEvans/ansible-splunk/compare/v0.11.9...v0.12.0) (2026-05-03)

### Features

* **splunk_docker:** add mac_perf index ([#184](https://github.com/JacobPEvans/ansible-splunk/issues/184)) ([6acc906](https://github.com/JacobPEvans/ansible-splunk/commit/6acc9069266771e24050f79f2eedb2e1aaa3303c))
* **splunk_docker:** wire TA-slack-add-on-for-splunk into addons registry ([#186](https://github.com/JacobPEvans/ansible-splunk/issues/186)) ([f93e5e0](https://github.com/JacobPEvans/ansible-splunk/commit/f93e5e01b8d2f1c763d1740c9454e61a0e7fa05b))

### Bug Fixes

* **deps:** refresh gh-aw action SHA pins ([#188](https://github.com/JacobPEvans/ansible-splunk/issues/188)) ([a884904](https://github.com/JacobPEvans/ansible-splunk/commit/a884904cd6cf006d5e8437b44fb65e7c2e8e65fa))

## [0.11.9](https://github.com/JacobPEvans/ansible-splunk/compare/v0.11.8...v0.11.9) (2026-04-29)

### Bug Fixes

* **splunk_docker:** create host splunk user/group matching container UID ([#182](https://github.com/JacobPEvans/ansible-splunk/issues/182)) ([446056d](https://github.com/JacobPEvans/ansible-splunk/commit/446056de2fe85387b338b8b799f1813a29e408dc))

## [0.11.8](https://github.com/JacobPEvans/ansible-splunk/compare/v0.11.7...v0.11.8) (2026-04-28)

### Bug Fixes

* **deps:** refresh gh-aw action SHA pins ([#179](https://github.com/JacobPEvans/ansible-splunk/issues/179)) ([9a3f9b8](https://github.com/JacobPEvans/ansible-splunk/commit/9a3f9b8221bcd00efd5da693f0e503b3aa3b428f))

## [0.11.7](https://github.com/JacobPEvans/ansible-splunk/compare/v0.11.6...v0.11.7) (2026-04-26)

### Bug Fixes

* **deps:** refresh gh-aw action SHA pins ([88c409b](https://github.com/JacobPEvans/ansible-splunk/commit/88c409b9c3286a4703f9d0f85ea064eb89f3ae8f))

## [0.11.6](https://github.com/JacobPEvans/ansible-splunk/compare/v0.11.5...v0.11.6) (2026-04-24)

### Bug Fixes

* update CI badge links to point to ci-gate.yml ([#166](https://github.com/JacobPEvans/ansible-splunk/issues/166)) ([6645415](https://github.com/JacobPEvans/ansible-splunk/commit/6645415a96fab58b366f1463ee33d38fc1c8801f))

## [0.11.5](https://github.com/JacobPEvans/ansible-splunk/compare/v0.11.4...v0.11.5) (2026-04-24)

### Bug Fixes

* **deps:** refresh gh-aw action SHA pins ([#170](https://github.com/JacobPEvans/ansible-splunk/issues/170)) ([8254d30](https://github.com/JacobPEvans/ansible-splunk/commit/8254d300770f62f5ae64a126b12cae2969eae708))

## [0.11.4](https://github.com/JacobPEvans/ansible-splunk/compare/v0.11.3...v0.11.4) (2026-04-21)

### Bug Fixes

* **ci:** add gh-aw-pin-refresh workflow and recompile lock files ([af66071](https://github.com/JacobPEvans/ansible-splunk/commit/af6607151e1b8516e23a0301336a408ab069005b))

## [0.11.3](https://github.com/JacobPEvans/ansible-splunk/compare/v0.11.2...v0.11.3) (2026-04-13)

### Bug Fixes

* add automation bots to AI Moderator skip-bots ([#152](https://github.com/JacobPEvans/ansible-splunk/issues/152)) ([7bbd048](https://github.com/JacobPEvans/ansible-splunk/commit/7bbd0482ab672e0efab0f6e1db14e09a579d2ffc))

## [0.11.2](https://github.com/JacobPEvans/ansible-splunk/compare/v0.11.1...v0.11.2) (2026-04-13)

### Bug Fixes

* **gh-aw:** recompile agentic workflow lock files with v0.68.1 ([d83f93c](https://github.com/JacobPEvans/ansible-splunk/commit/d83f93c7509937fa3ea53b308cfc7b8728601aae))

## [0.11.1](https://github.com/JacobPEvans/ansible-splunk/compare/v0.11.0...v0.11.1) (2026-04-13)

### Bug Fixes

* correct MCP Server config and restore per-index HEC tokens ([#140](https://github.com/JacobPEvans/ansible-splunk/issues/140)) ([24614d8](https://github.com/JacobPEvans/ansible-splunk/commit/24614d8159f31385ccb793bc27a26ebb8fe4bced))

## [0.11.0](https://github.com/JacobPEvans/ansible-splunk/compare/v0.10.0...v0.11.0) (2026-04-12)

## [0.10.0](https://github.com/JacobPEvans/ansible-splunk/compare/v0.9.0...v0.10.0) (2026-04-11)

### Features

* **splunk:** MinIO add-on registry + Splunkbase auto-sync ([7364448](https://github.com/JacobPEvans/ansible-splunk/commit/736444891f658d374e85329b5fecb47cc5612a9d))

## [0.9.0](https://github.com/JacobPEvans/ansible-splunk/compare/v0.8.1...v0.9.0) (2026-04-09)

### Features

* add MinIO artifact store + propagate terraform_data to all hosts ([#124](https://github.com/JacobPEvans/ansible-splunk/issues/124)) ([804eb55](https://github.com/JacobPEvans/ansible-splunk/commit/804eb55dc49aeea7561db51375c5c9efae4f6d6e))
* add MinIO artifact store for custom add-on downloads ([#118](https://github.com/JacobPEvans/ansible-splunk/issues/118)) ([20a1efe](https://github.com/JacobPEvans/ansible-splunk/commit/20a1efeae4e451eb8fc132a460a1883ca42b8d12))

## [0.8.1](https://github.com/JacobPEvans/ansible-splunk/compare/v0.8.0...v0.8.1) (2026-04-07)

### Bug Fixes

* restructure CLAUDE.md from wiki to rulebook ([#120](https://github.com/JacobPEvans/ansible-splunk/issues/120)) ([09c4b5b](https://github.com/JacobPEvans/ansible-splunk/commit/09c4b5b3312f6fc4202b29a7134cc9f29e911f80))

## [0.8.0](https://github.com/JacobPEvans/ansible-splunk/compare/v0.7.0...v0.8.0) (2026-04-07)

### Features

* add AI merge gate and Copilot setup steps ([#119](https://github.com/JacobPEvans/ansible-splunk/issues/119)) ([a6547da](https://github.com/JacobPEvans/ansible-splunk/commit/a6547da10c472819a05e3e0e4161960257f1c62c))

## [0.7.0](https://github.com/JacobPEvans/ansible-splunk/compare/v0.6.5...v0.7.0) (2026-04-04)

### Features

* add ai and claude Splunk indexes ([#24](https://github.com/JacobPEvans/ansible-splunk/issues/24)) ([a240deb](https://github.com/JacobPEvans/ansible-splunk/commit/a240deb625a5bdced46de42a30c0013ac63f0290))
* add daily repo health audit agentic workflow ([#91](https://github.com/JacobPEvans/ansible-splunk/issues/91)) ([d7e0880](https://github.com/JacobPEvans/ansible-splunk/commit/d7e08806a03481984477c529b8a1da68b9e80c88))
* add gemini, openai, and vscode splunk indexes ([#72](https://github.com/JacobPEvans/ansible-splunk/issues/72)) ([8a7116b](https://github.com/JacobPEvans/ansible-splunk/commit/8a7116b62f6566b357244a8800bda1ad9d92682f))
* add gh-aw agentic workflows for CI, security, and moderation ([#61](https://github.com/JacobPEvans/ansible-splunk/issues/61)) ([75ad4bc](https://github.com/JacobPEvans/ansible-splunk/commit/75ad4bcbf6d0e3733d93654e12429395c81727ee))
* add JRE-21 and Splunk DB Connect ([#30](https://github.com/JacobPEvans/ansible-splunk/issues/30)) ([b682eab](https://github.com/JacobPEvans/ansible-splunk/commit/b682eabf173da9663ad00ef82cd418dc77903b83))
* add MCP client config, best practices docs, and splunk.splunk role ([#51](https://github.com/JacobPEvans/ansible-splunk/issues/51)) ([2791192](https://github.com/JacobPEvans/ansible-splunk/commit/2791192419557a19b3b96560ba45bc0955a0e529))
* add PSC, MLTK, and DSDL validation checks ([#49](https://github.com/JacobPEvans/ansible-splunk/issues/49)) ([c9338d5](https://github.com/JacobPEvans/ansible-splunk/commit/c9338d57d489750a1d5d25103febaad9998d6d9d))
* add scheduled AI workflow callers ([#69](https://github.com/JacobPEvans/ansible-splunk/issues/69)) ([b04201e](https://github.com/JacobPEvans/ansible-splunk/commit/b04201e35b6d76ae63f1bdf3aad4915033659a83))
* add VisiCore AI Observability packages v1.0.0 ([#86](https://github.com/JacobPEvans/ansible-splunk/issues/86)) ([cd61bba](https://github.com/JacobPEvans/ansible-splunk/commit/cd61bbad03534d86920bbdd26783aa5bbdd49a7f))
* adopt conventional branch standard (feature/, bugfix/, chore/) ([#66](https://github.com/JacobPEvans/ansible-splunk/issues/66)) ([0702858](https://github.com/JacobPEvans/ansible-splunk/commit/0702858d7267d996ee33d36ba926357cff52d586))
* auto-configure DB Connect JAVA_HOME ([#52](https://github.com/JacobPEvans/ansible-splunk/issues/52)) ([e0fd0d5](https://github.com/JacobPEvans/ansible-splunk/commit/e0fd0d52d8ad5c10d5361fb7f7db0365ddde1327))
* Complete Splunk automation migration from terraform-proxmox ([#3](https://github.com/JacobPEvans/ansible-splunk/issues/3)) ([86f6ca0](https://github.com/JacobPEvans/ansible-splunk/commit/86f6ca06fc08d8c9ade01cb097f4068825545195))
* configure HEC token via inputs.conf template ([#31](https://github.com/JacobPEvans/ansible-splunk/issues/31)) ([74cc915](https://github.com/JacobPEvans/ansible-splunk/commit/74cc91569805c84beb10bcf2cdad0e1c9194ebd2))
* consolidate Splunk Docker deployment from ansible-proxmox-apps ([a1475a8](https://github.com/JacobPEvans/ansible-splunk/commit/a1475a8e3fb3cd23e97b67dfe1354fc7d0feba8e))
* deploy Splunk MCP Server for AI assistant integration ([#50](https://github.com/JacobPEvans/ansible-splunk/issues/50)) ([0ff84fa](https://github.com/JacobPEvans/ansible-splunk/commit/0ff84fa8ba8adfc21d703cd7778daaf17307e37c))
* disable automatic triggers on Claude-executing workflows ([b1f34ce](https://github.com/JacobPEvans/ansible-splunk/commit/b1f34ce0b06559ceaca650cc6ef7f0a9baf71d6f))
* download VisiCore add-ons from GitHub Releases automatically ([#89](https://github.com/JacobPEvans/ansible-splunk/issues/89)) ([81565a0](https://github.com/JacobPEvans/ansible-splunk/commit/81565a04e8f3ab5f05a69b3f1bfa7b1c201313ad))
* enforce required Splunk apps with fail-fast validation ([#90](https://github.com/JacobPEvans/ansible-splunk/issues/90)) ([c13e27d](https://github.com/JacobPEvans/ansible-splunk/commit/c13e27d24bf94f94122ac44f1785822a80f33cd7))
* **indexes:** add netflow index for NetFlow/IPFIX data ([#16](https://github.com/JacobPEvans/ansible-splunk/issues/16)) ([7b2435b](https://github.com/JacobPEvans/ansible-splunk/commit/7b2435b48aadb7c646bf33081215c133b256b2d2))
* per-index HEC tokens via UUID v5 derivation ([8baabc3](https://github.com/JacobPEvans/ansible-splunk/commit/8baabc3288fa4f3ebcdbf09b2d98a2a5e72cc702))
* pipeline sync - standardize env vars, fix HEC config ([#19](https://github.com/JacobPEvans/ansible-splunk/issues/19)) ([f54ed53](https://github.com/JacobPEvans/ansible-splunk/commit/f54ed53341ce3e13f4a63c0b5a91630a3560045b))
* refactor app management with Splunkbase registry and expose management port ([#48](https://github.com/JacobPEvans/ansible-splunk/issues/48)) ([9331708](https://github.com/JacobPEvans/ansible-splunk/commit/93317082f189579620c09a89d41032e0d701c24e))
* **renovate:** extend shared preset, remove duplicated rules ([7a21afb](https://github.com/JacobPEvans/ansible-splunk/commit/7a21afb124a8c96e1f7f3670dfedcdd349521560))

### Bug Fixes

* add Nix dev shell tool execution rule ([#106](https://github.com/JacobPEvans/ansible-splunk/issues/106)) ([3e3b08f](https://github.com/JacobPEvans/ansible-splunk/commit/3e3b08f8e3236db17e3a230e2dc7c4278531a74b))
* add Python 3.9 for Splunk compatibility ([1f31a00](https://github.com/JacobPEvans/ansible-splunk/commit/1f31a00839c9f0be7a22806eaf66e43869be2ddd))
* add python3-requests for community.docker modules ([fd53f27](https://github.com/JacobPEvans/ansible-splunk/commit/fd53f277831bce17f41e8cd485448ec78880a9c1))
* add systemd restart policy for Docker daemon ([#108](https://github.com/JacobPEvans/ansible-splunk/issues/108)) ([b7c1187](https://github.com/JacobPEvans/ansible-splunk/commit/b7c118756c14b795138deba6deaeef33d57d2b9b))
* address CI failures ([e29fd74](https://github.com/JacobPEvans/ansible-splunk/commit/e29fd745303d948f1947f93f6747b59c441ea037))
* address PR [#8](https://github.com/JacobPEvans/ansible-splunk/issues/8) review feedback on Splunk Docker deployment ([416833d](https://github.com/JacobPEvans/ansible-splunk/commit/416833db90c5a75bc47c65099f2eb5f155bef07a))
* allow all custom indexes in HEC token ([#32](https://github.com/JacobPEvans/ansible-splunk/issues/32)) ([70e538c](https://github.com/JacobPEvans/ansible-splunk/commit/70e538c9a13899061b1366be8f0e2df1ef64b958))
* automate Splunkbase app downloads via REST API ([#115](https://github.com/JacobPEvans/ansible-splunk/issues/115)) ([9129338](https://github.com/JacobPEvans/ansible-splunk/commit/9129338fea7c85d80bb0b2cabf072a2cc04fbb7b))
* **ci:** add pull-requests: write for release-please auto-approval ([#97](https://github.com/JacobPEvans/ansible-splunk/issues/97)) ([c2112c1](https://github.com/JacobPEvans/ansible-splunk/commit/c2112c1878dd6502c8fd029c5b0607334c13e135))
* **ci:** implement Merge Gatekeeper pattern with ci-gate ([#93](https://github.com/JacobPEvans/ansible-splunk/issues/93)) ([90a173b](https://github.com/JacobPEvans/ansible-splunk/commit/90a173b864aa175072e881a9fc6451bdc39eacaa))
* **ci:** use GitHub App token for release-please to trigger CI Gate ([#92](https://github.com/JacobPEvans/ansible-splunk/issues/92)) ([4ac143f](https://github.com/JacobPEvans/ansible-splunk/commit/4ac143f043c041d1640f3e1c190c9494ce043c21))
* complete pipeline sync - license, inventory paths, HEC config ([#20](https://github.com/JacobPEvans/ansible-splunk/issues/20)) ([ce3ed22](https://github.com/JacobPEvans/ansible-splunk/commit/ce3ed22b933e2885d3a17f4e1b190cebc57a7070))
* correct cloud.terraform version to 2.1.0 ([f01422e](https://github.com/JacobPEvans/ansible-splunk/commit/f01422ec2f45a6b138dfbdb21f5968907f9fed9a))
* correct HEC protocol documentation from HTTP to HTTPS ([#95](https://github.com/JacobPEvans/ansible-splunk/issues/95)) ([c91a757](https://github.com/JacobPEvans/ansible-splunk/commit/c91a757958ebe4f1bdf847e339f527ec2a23ced2))
* disable internet access checks for air-gapped Splunk VM ([#23](https://github.com/JacobPEvans/ansible-splunk/issues/23)) ([b37397e](https://github.com/JacobPEvans/ansible-splunk/commit/b37397e448af0f844557dadd07116609c75ad188))
* **firewall:** disable guest iptables in favor of Proxmox firewall ([#14](https://github.com/JacobPEvans/ansible-splunk/issues/14)) ([21a743e](https://github.com/JacobPEvans/ansible-splunk/commit/21a743e4e7b265dd9ca9e8822e00dbb9479b8520))
* grant contents: write for release-please workflow ([d5b6ec2](https://github.com/JacobPEvans/ansible-splunk/commit/d5b6ec25392427b202cbb92a37bb8218f3dad977))
* **inventory:** correct splunk_vm key path in load_terraform.yml ([#25](https://github.com/JacobPEvans/ansible-splunk/issues/25)) ([a747d47](https://github.com/JacobPEvans/ansible-splunk/commit/a747d472d9e9edef1cc3aedabb088f95f93c453c))
* make Molecule idempotence check deterministic ([#55](https://github.com/JacobPEvans/ansible-splunk/issues/55)) ([b8b9741](https://github.com/JacobPEvans/ansible-splunk/commit/b8b97413bf35934d6256ebc7e8d6e55dfcaf08aa))
* make Splunk Docker deployment idempotent and enable SSL ([f50eef3](https://github.com/JacobPEvans/ansible-splunk/commit/f50eef3f3dbb539038ca9339ca20a2ce8cef12fe))
* migrate release-please config to packages format ([4090064](https://github.com/JacobPEvans/ansible-splunk/commit/4090064b5895eafd967198f7979c9ec33be3d37a))
* pin ansible-core&gt;=2.16,&lt;2.18 for compatibility ([d4f90a9](https://github.com/JacobPEvans/ansible-splunk/commit/d4f90a933c3c361bbcb3f9f39ce136b13099658c))
* pin Docker SDK versions for Molecule CI compatibility ([897b5d4](https://github.com/JacobPEvans/ansible-splunk/commit/897b5d4e2fa506197b6321a88d4fe4348312e393))
* remove claude-review workflow ([#114](https://github.com/JacobPEvans/ansible-splunk/issues/114)) ([9d6f157](https://github.com/JacobPEvans/ansible-splunk/commit/9d6f157b4f6c9afd8d3ea19dcf46a52e8fce577b))
* remove Python 3.9, use syntax-only molecule test ([294357a](https://github.com/JacobPEvans/ansible-splunk/commit/294357a871870ad7217f33fdfadd88558978b4e5))
* remove quotes from inputs.conf values and add post-restart health check ([#34](https://github.com/JacobPEvans/ansible-splunk/issues/34)) ([65c3fd3](https://github.com/JacobPEvans/ansible-splunk/commit/65c3fd374cc7a3fa50a8f7ba7995d6a578682e9b))
* set ANSIBLE_COLLECTIONS_PATH for molecule tests ([d6a9288](https://github.com/JacobPEvans/ansible-splunk/commit/d6a9288fb50f4b4c6167cf4a20dd7582a928587e))
* support Python 3.9 and fix Docker-in-Docker storage ([0bed704](https://github.com/JacobPEvans/ansible-splunk/commit/0bed7047e788dfd7a55a7b03f4b2cfb426f89b3b))
* update SSH configuration and inventory for Splunk VM ([2ac5dde](https://github.com/JacobPEvans/ansible-splunk/commit/2ac5ddea3f34d3ceb0fde1aaedc41b503dc389c2))
* update stale nix-config references to nix-ai ([#105](https://github.com/JacobPEvans/ansible-splunk/issues/105)) ([a657710](https://github.com/JacobPEvans/ansible-splunk/commit/a657710ca9d6589333be699bf32a11b3919c1e1f))
* use ansible_facts dict to avoid INJECT_FACTS_AS_VARS deprecation ([#33](https://github.com/JacobPEvans/ansible-splunk/issues/33)) ([b3f3bb0](https://github.com/JacobPEvans/ansible-splunk/commit/b3f3bb06b232c4cea1b3edddd5199683096abbfa))
* use flexible community.docker version and verify collections ([1d3bbe1](https://github.com/JacobPEvans/ansible-splunk/commit/1d3bbe1e19774bb58fb010af8d2957cc8c0e0952))
* use include_role in post_tasks so role defaults are available ([#35](https://github.com/JacobPEvans/ansible-splunk/issues/35)) ([09c79ec](https://github.com/JacobPEvans/ansible-splunk/commit/09c79ec2a12040b972111398c902c6f8f0a7c5b5))
* use nix-devenv ansible-apps shell instead of local flake.nix ([#110](https://github.com/JacobPEvans/ansible-splunk/issues/110)) ([d18a3ca](https://github.com/JacobPEvans/ansible-splunk/commit/d18a3ca7e65f6fa028e3f36413ecba376b607323))
* use packages attr, add doppler, gitignore .direnv ([#78](https://github.com/JacobPEvans/ansible-splunk/issues/78)) ([2a05c4f](https://github.com/JacobPEvans/ansible-splunk/commit/2a05c4f0f8bf50281e9c2e9bb13774bebb7bea1c))
* use role-prefixed variable names for ansible-lint compliance ([d1f9887](https://github.com/JacobPEvans/ansible-splunk/commit/d1f98872f710e78372935ca7e2c36e4a5c23cbc0))
* use selectattr 'defined' test for github_repo filter ([#101](https://github.com/JacobPEvans/ansible-splunk/issues/101)) ([409cdea](https://github.com/JacobPEvans/ansible-splunk/commit/409cdeae623b2f2d7789289c98d3bc89c60435ca))

### Performance

* **ci:** cut Molecule runtime from ~30min to ~8min ([#56](https://github.com/JacobPEvans/ansible-splunk/issues/56)) ([ef179a4](https://github.com/JacobPEvans/ansible-splunk/commit/ef179a40513e328f3feb59cfb3d18e9f80a2901a))

## [0.6.5](https://github.com/JacobPEvans/ansible-splunk/compare/v0.6.4...v0.6.5) (2026-04-04)

### Bug Fixes

* remove claude-review workflow ([#114](https://github.com/JacobPEvans/ansible-splunk/issues/114)) ([9d6f157](https://github.com/JacobPEvans/ansible-splunk/commit/9d6f157b4f6c9afd8d3ea19dcf46a52e8fce577b))

## [0.6.4](https://github.com/JacobPEvans/ansible-splunk/compare/v0.6.3...v0.6.4) (2026-03-31)

### Bug Fixes

* use nix-devenv ansible-apps shell instead of local flake.nix ([#110](https://github.com/JacobPEvans/ansible-splunk/issues/110)) ([d18a3ca](https://github.com/JacobPEvans/ansible-splunk/commit/d18a3ca7e65f6fa028e3f36413ecba376b607323))

## [0.6.3](https://github.com/JacobPEvans/ansible-splunk/compare/v0.6.2...v0.6.3) (2026-03-26)

### Bug Fixes

* add systemd restart policy for Docker daemon ([#108](https://github.com/JacobPEvans/ansible-splunk/issues/108)) ([b7c1187](https://github.com/JacobPEvans/ansible-splunk/commit/b7c118756c14b795138deba6deaeef33d57d2b9b))

## [0.6.2](https://github.com/JacobPEvans/ansible-splunk/compare/v0.6.1...v0.6.2) (2026-03-25)

### Bug Fixes

* add Nix dev shell tool execution rule ([#106](https://github.com/JacobPEvans/ansible-splunk/issues/106)) ([3e3b08f](https://github.com/JacobPEvans/ansible-splunk/commit/3e3b08f8e3236db17e3a230e2dc7c4278531a74b))
* update stale nix-config references to nix-ai ([#105](https://github.com/JacobPEvans/ansible-splunk/issues/105)) ([a657710](https://github.com/JacobPEvans/ansible-splunk/commit/a657710ca9d6589333be699bf32a11b3919c1e1f))

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
