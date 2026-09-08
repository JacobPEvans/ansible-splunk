# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.70.3](https://github.com/dryvist/ansible-splunk/compare/v0.70.2...v0.70.3) (2026-09-08)


### Bug Fixes

* **splunk:** give the agent identity search, not administration ([#543](https://github.com/dryvist/ansible-splunk/issues/543)) ([5a9cf71](https://github.com/dryvist/ansible-splunk/commit/5a9cf718bf2f8770001d05ad98fe80db6b3c8867))

## [0.70.2](https://github.com/dryvist/ansible-splunk/compare/v0.70.1...v0.70.2) (2026-09-08)


### Bug Fixes

* **splunk_docker:** reconcile the Enterprise license, and refuse an expired one ([#541](https://github.com/dryvist/ansible-splunk/issues/541)) ([685716f](https://github.com/dryvist/ansible-splunk/commit/685716f1288ce0c96c2f0ca0b8a2ac5e5b0d2651))

## [0.70.1](https://github.com/dryvist/ansible-splunk/compare/v0.70.0...v0.70.1) (2026-09-05)


### Bug Fixes

* **agents:** restore the trailing newline on AGENTS.md ([#538](https://github.com/dryvist/ansible-splunk/issues/538)) ([941b912](https://github.com/dryvist/ansible-splunk/commit/941b91264d0ccae6f8e6c23aa110129bfdcc6dbb))

## [0.70.0](https://github.com/dryvist/ansible-splunk/compare/v0.69.1...v0.70.0) (2026-09-05)


### Features

* **splunk_docker:** declare the clickhouse and phoenix indexes ([#535](https://github.com/dryvist/ansible-splunk/issues/535)) ([af96b8b](https://github.com/dryvist/ansible-splunk/commit/af96b8bb2c1c6c51c218586e5c9acfc5201d93c5))

## [0.69.1](https://github.com/dryvist/ansible-splunk/compare/v0.69.0...v0.69.1) (2026-09-04)


### Bug Fixes

* **splunk_docker:** fall back to dig for object-storage DNS on macOS ([1d50f96](https://github.com/dryvist/ansible-splunk/commit/1d50f96702960208ff963f62b735b6746831e72f))
* **splunk_docker:** MCP 2.0 ACCEPTED assert and guest S3 DNS ([f0082df](https://github.com/dryvist/ansible-splunk/commit/f0082dfa8ba00ea68ae7060d317610fca9fac6f4))
* **splunk_docker:** MCP 2.0 ACCEPTED assert, resolve S3 DNS for guests ([a3c6d8f](https://github.com/dryvist/ansible-splunk/commit/a3c6d8fb883f06bc64a4601ad1e7a774a5c55df8))
* **splunk_docker:** set pipefail in object-storage DNS lookup ([291c3d2](https://github.com/dryvist/ansible-splunk/commit/291c3d28662dba40e0efafe77d22e9375099d6bb))

## [0.69.0](https://github.com/dryvist/ansible-splunk/compare/v0.68.7...v0.69.0) (2026-09-04)


### Features

* **splunk_docker:** register Splunkbase Add-on Builder app 2962 ([6114ebd](https://github.com/dryvist/ansible-splunk/commit/6114ebd33387e2f214b5a545ce3f654e4b49248b))
* **splunk_docker:** track Splunk Add-on Builder (2962) ([76634a7](https://github.com/dryvist/ansible-splunk/commit/76634a74924ef3067c298a17e6295000b14ca012))
* **splunk_docker:** track Splunk Add-on Builder (2962) and ignore .worktrees ([c5927eb](https://github.com/dryvist/ansible-splunk/commit/c5927eb81426ab6714e8e072a2c593bd45a950a5))

## [0.68.7](https://github.com/dryvist/ansible-splunk/compare/v0.68.6...v0.68.7) (2026-09-04)


### Bug Fixes

* **sync-splunkbase:** harden review feedback on empty S3 JSON and schema ([fc9f1e4](https://github.com/dryvist/ansible-splunk/commit/fc9f1e4de9f74a441ee68bc2c8a4498ddbd30891))

## [0.68.6](https://github.com/dryvist/ansible-splunk/compare/v0.68.5...v0.68.6) (2026-09-03)


### Bug Fixes

* **validate:** use playbook_dir in defaults include_vars path ([#526](https://github.com/dryvist/ansible-splunk/issues/526)) ([ee2ec67](https://github.com/dryvist/ansible-splunk/commit/ee2ec6709c6111ab02bde1195fb81ab8dbf12b65))

## [0.68.5](https://github.com/dryvist/ansible-splunk/compare/v0.68.4...v0.68.5) (2026-09-03)


### Bug Fixes

* **splunk_docker:** install the official Slack Notification Alert app ([0e83ae8](https://github.com/dryvist/ansible-splunk/commit/0e83ae8c874d6fc0474c77764ab08b82c759e01f))
* **splunk_docker:** install the official Slack Notification Alert app ([9443270](https://github.com/dryvist/ansible-splunk/commit/94432705025dc9b6281e8ea0535da5d095231530))

## [0.68.4](https://github.com/dryvist/ansible-splunk/compare/v0.68.3...v0.68.4) (2026-09-03)


### Bug Fixes

* **splunk_docker:** deliver Slack alerts via the built-in webhook action ([b497bce](https://github.com/dryvist/ansible-splunk/commit/b497bcefb05c1b9eb675db2365d7feed9660f14d))
* **splunk_docker:** deliver Slack alerts via the built-in webhook action ([6b1367c](https://github.com/dryvist/ansible-splunk/commit/6b1367cd09bb190f6d82acb583c1e47e8ae7d2c6))
* **splunk_docker:** make the Zammad delivery gate loud, not aspirational ([f5788a9](https://github.com/dryvist/ansible-splunk/commit/f5788a9da44a3d4b5e8542403e9e3efadaa501b2))

## [0.68.3](https://github.com/dryvist/ansible-splunk/compare/v0.68.2...v0.68.3) (2026-09-03)


### Bug Fixes

* **splunk_docker:** use live time, not a stale gathered fact, for token eligibility ([e14688c](https://github.com/dryvist/ansible-splunk/commit/e14688c51e37d8af31c72faa3c6526557d086e48))
* **splunk_docker:** use live time, not a stale gathered fact, for token eligibility ([966641f](https://github.com/dryvist/ansible-splunk/commit/966641f6337469fc1d094092b2c8b01f0e9fe43a))

## [0.68.2](https://github.com/dryvist/ansible-splunk/compare/v0.68.1...v0.68.2) (2026-09-02)


### Bug Fixes

* **splunk_docker:** fail the converge on an unset alert gate or a missing detector index ([62b3a43](https://github.com/dryvist/ansible-splunk/commit/62b3a43a68ddb2174a88d58e6a909975c8681e85))

## [0.68.1](https://github.com/dryvist/ansible-splunk/compare/v0.68.0...v0.68.1) (2026-09-02)


### Bug Fixes

* **splunk_docker:** dedupe voter-health silence detection, fix total-silence blind spot ([9680553](https://github.com/dryvist/ansible-splunk/commit/9680553b93dc1b2f864f73c922e0d0e06c8581ac))
* **splunk_docker:** dedupe voter-health silence detection, fix total-silence blind spot ([9357680](https://github.com/dryvist/ansible-splunk/commit/93576805a9f98064b1e2cfdea3d219fe2d34035b))

## [0.68.0](https://github.com/dryvist/ansible-splunk/compare/v0.67.1...v0.68.0) (2026-09-02)


### Features

* **alerts:** OpenBao privileged-use, audit/snapshot/voter silence, and raft quorum alerts ([93e0201](https://github.com/dryvist/ansible-splunk/commit/93e02013a76eb680dcc41bbca26e9d5196a69c4f))
* **alerts:** OpenBao privileged-use, snapshot silence, and raft quorum alerts ([520e74e](https://github.com/dryvist/ansible-splunk/commit/520e74eee67346256e78c380c8046b08e237a33d))

## [0.67.1](https://github.com/dryvist/ansible-splunk/compare/v0.67.0...v0.67.1) (2026-09-02)


### Bug Fixes

* **splunk:** let the audit-trail silence detector see a real outage ([#510](https://github.com/dryvist/ansible-splunk/issues/510)) ([aed1eaf](https://github.com/dryvist/ansible-splunk/commit/aed1eaf8e1ae9457fa49dfd21eb35381967018a8))

## [0.67.0](https://github.com/dryvist/ansible-splunk/compare/v0.66.0...v0.67.0) (2026-09-02)


### Features

* **indexes:** add the ai_usage index for agent OTLP log records ([#508](https://github.com/dryvist/ansible-splunk/issues/508)) ([84c248a](https://github.com/dryvist/ansible-splunk/commit/84c248a2d18419c650f7f36883c336040cb792b1))

## [0.66.0](https://github.com/dryvist/ansible-splunk/compare/v0.65.0...v0.66.0) (2026-09-01)


### Features

* **cluster:** apply the Splunk Enterprise license on every converge ([#506](https://github.com/dryvist/ansible-splunk/issues/506)) ([6d373cb](https://github.com/dryvist/ansible-splunk/commit/6d373cb46a15515288ac78ed49c20bc11a75a03c))

## [0.65.0](https://github.com/dryvist/ansible-splunk/compare/v0.64.2...v0.65.0) (2026-09-01)


### Features

* **splunk_docker:** add semaphore Splunk index ([#503](https://github.com/dryvist/ansible-splunk/issues/503)) ([84eca0c](https://github.com/dryvist/ansible-splunk/commit/84eca0c400a1381969149ee5d586cabf7fb2e9b6))

## [0.64.2](https://github.com/dryvist/ansible-splunk/compare/v0.64.1...v0.64.2) (2026-08-25)


### Bug Fixes

* **splunk_docker:** bind every index to a Splunk volume ([#500](https://github.com/dryvist/ansible-splunk/issues/500)) ([25c7011](https://github.com/dryvist/ansible-splunk/commit/25c7011c2f3b91774a34c20f7edc5c465d950ad4))

## [0.64.1](https://github.com/dryvist/ansible-splunk/compare/v0.64.0...v0.64.1) (2026-08-23)


### Bug Fixes

* **splunk_docker:** point the Mac detectors at sourcetypes that exist ([#495](https://github.com/dryvist/ansible-splunk/issues/495)) ([5c005ec](https://github.com/dryvist/ansible-splunk/commit/5c005ec821ea771bc4993d0dd6a580f91e53035c))

## [0.64.0](https://github.com/dryvist/ansible-splunk/compare/v0.63.0...v0.64.0) (2026-08-23)


### ⚠ BREAKING CHANGES

* **splunk_docker:** savedsearches/00-macros.j2 and alert_deliver() are removed. A fragment still calling the macro fails to render.

### Features

* **splunk_docker:** default every saved search to Slack + Zammad ([#489](https://github.com/dryvist/ansible-splunk/issues/489)) ([17420eb](https://github.com/dryvist/ansible-splunk/commit/17420ebdf04700a7c19bc5bd319734a3a5889c18))

## [0.63.0](https://github.com/dryvist/ansible-splunk/compare/v0.62.0...v0.63.0) (2026-08-23)


### Features

* **splunk:** add Mac-health detectors ([#490](https://github.com/dryvist/ansible-splunk/issues/490)) ([352dbbd](https://github.com/dryvist/ansible-splunk/commit/352dbbdf9850470b4b1040fed6665b3435f6729f))

## [0.62.0](https://github.com/dryvist/ansible-splunk/compare/v0.61.3...v0.62.0) (2026-08-23)


### Features

* **splunk_docker:** lift the alerting cutover gate, enable all detectors ([#491](https://github.com/dryvist/ansible-splunk/issues/491)) ([14fb22d](https://github.com/dryvist/ansible-splunk/commit/14fb22d7f31987e1e4062e1a27fa656e879b39c9))

## [0.61.3](https://github.com/dryvist/ansible-splunk/compare/v0.61.2...v0.61.3) (2026-08-17)


### Bug Fixes

* **splunk_docker:** fail fast on a failed HEC query, avoid unsafe dot access ([a3bb678](https://github.com/dryvist/ansible-splunk/commit/a3bb678bdbd51cbea5ea1c2dd23d31b7c41f365e))
* **splunk_docker:** repair pre-role index-combine reference, add HEC stanza completeness check ([b3a46b7](https://github.com/dryvist/ansible-splunk/commit/b3a46b7b918aaf76d2d4a0d62f6ff5a9c65c12fe))
* **splunk_docker:** repair pre-role index-combine reference, add HEC stanza completeness check ([#484](https://github.com/dryvist/ansible-splunk/issues/484)) ([51de9e3](https://github.com/dryvist/ansible-splunk/commit/51de9e3a9874f8ecf76fa82c6d4585d6fb15bbd8))
* **splunk_docker:** satisfy ansible-lint on the completeness check ([3d452f0](https://github.com/dryvist/ansible-splunk/commit/3d452f0396591d0646716f0386ec181ecef4011b))

## [0.61.2](https://github.com/dryvist/ansible-splunk/compare/v0.61.1...v0.61.2) (2026-08-16)


### Bug Fixes

* **splunk_docker:** make HEC_NAMESPACE required, not silently optional ([#482](https://github.com/dryvist/ansible-splunk/issues/482)) ([a408c41](https://github.com/dryvist/ansible-splunk/commit/a408c412202c501dec3a68c52f2ea78426a2c48d))

## [0.61.1](https://github.com/dryvist/ansible-splunk/compare/v0.61.0...v0.61.1) (2026-08-07)


### Bug Fixes

* **splunk:** keep the newline after the search line so detectors can parse ([#479](https://github.com/dryvist/ansible-splunk/issues/479)) ([202c85a](https://github.com/dryvist/ansible-splunk/commit/202c85aa493d57617bb4835462a5c6773bf374e1))

## [0.61.0](https://github.com/dryvist/ansible-splunk/compare/v0.60.0...v0.61.0) (2026-08-07)


### ⚠ BREAKING CHANGES

* **sync-splunkbase:** the controller now needs `aws` on PATH instead of the previous object-storage client.

### Features

* add ai and claude Splunk indexes ([#24](https://github.com/dryvist/ansible-splunk/issues/24)) ([a240deb](https://github.com/dryvist/ansible-splunk/commit/a240deb625a5bdced46de42a30c0013ac63f0290))
* add AI merge gate and Copilot setup steps ([#119](https://github.com/dryvist/ansible-splunk/issues/119)) ([a6547da](https://github.com/dryvist/ansible-splunk/commit/a6547da10c472819a05e3e0e4161960257f1c62c))
* add AI PR care caller (dep review + release highlights) ([#292](https://github.com/dryvist/ansible-splunk/issues/292)) ([60e647d](https://github.com/dryvist/ansible-splunk/commit/60e647ddfa0c4aa639a995771c2fc0eecbbf8045))
* add daily repo health audit agentic workflow ([#91](https://github.com/dryvist/ansible-splunk/issues/91)) ([d7e0880](https://github.com/dryvist/ansible-splunk/commit/d7e08806a03481984477c529b8a1da68b9e80c88))
* add gemini, openai, and vscode splunk indexes ([#72](https://github.com/dryvist/ansible-splunk/issues/72)) ([8a7116b](https://github.com/dryvist/ansible-splunk/commit/8a7116b62f6566b357244a8800bda1ad9d92682f))
* add gh-aw agentic workflows for CI, security, and moderation ([#61](https://github.com/dryvist/ansible-splunk/issues/61)) ([75ad4bc](https://github.com/dryvist/ansible-splunk/commit/75ad4bcbf6d0e3733d93654e12429395c81727ee))
* add JRE-21 and Splunk DB Connect ([#30](https://github.com/dryvist/ansible-splunk/issues/30)) ([b682eab](https://github.com/dryvist/ansible-splunk/commit/b682eabf173da9663ad00ef82cd418dc77903b83))
* add MCP client config, best practices docs, and splunk.splunk role ([#51](https://github.com/dryvist/ansible-splunk/issues/51)) ([2791192](https://github.com/dryvist/ansible-splunk/commit/2791192419557a19b3b96560ba45bc0955a0e529))
* add MinIO artifact store + propagate terraform_data to all hosts ([#124](https://github.com/dryvist/ansible-splunk/issues/124)) ([804eb55](https://github.com/dryvist/ansible-splunk/commit/804eb55dc49aeea7561db51375c5c9efae4f6d6e))
* add MinIO artifact store for custom add-on downloads ([#118](https://github.com/dryvist/ansible-splunk/issues/118)) ([20a1efe](https://github.com/dryvist/ansible-splunk/commit/20a1efeae4e451eb8fc132a460a1883ca42b8d12))
* add PSC, MLTK, and DSDL validation checks ([#49](https://github.com/dryvist/ansible-splunk/issues/49)) ([c9338d5](https://github.com/dryvist/ansible-splunk/commit/c9338d57d489750a1d5d25103febaad9998d6d9d))
* add scheduled AI workflow callers ([#69](https://github.com/dryvist/ansible-splunk/issues/69)) ([b04201e](https://github.com/dryvist/ansible-splunk/commit/b04201e35b6d76ae63f1bdf3aad4915033659a83))
* add VisiCore AI Observability packages v1.0.0 ([#86](https://github.com/dryvist/ansible-splunk/issues/86)) ([cd61bba](https://github.com/dryvist/ansible-splunk/commit/cd61bbad03534d86920bbdd26783aa5bbdd49a7f))
* adopt conventional branch standard (feature/, bugfix/, chore/) ([#66](https://github.com/dryvist/ansible-splunk/issues/66)) ([0702858](https://github.com/dryvist/ansible-splunk/commit/0702858d7267d996ee33d36ba926357cff52d586))
* **alerts:** add data-driven per-index silence detectors ([#304](https://github.com/dryvist/ansible-splunk/issues/304)) ([1991880](https://github.com/dryvist/ansible-splunk/commit/199188037aba5ecc3a2edb5d835b68d4b052978e))
* **alerts:** ntfy + Slack delivery, repoint LLM router alerts at live data ([#342](https://github.com/dryvist/ansible-splunk/issues/342)) ([0f10cbb](https://github.com/dryvist/ansible-splunk/commit/0f10cbb784a882fd43709bdca4365f1c61acfbd5))
* **alerts:** per-host LLM silence + LiteLLM router and model-eval alerts ([#294](https://github.com/dryvist/ansible-splunk/issues/294)) ([2dd80c4](https://github.com/dryvist/ansible-splunk/commit/2dd80c4ccafa72cb441b628ff2f87167151f787e))
* auto-configure DB Connect JAVA_HOME ([#52](https://github.com/dryvist/ansible-splunk/issues/52)) ([e0fd0d5](https://github.com/dryvist/ansible-splunk/commit/e0fd0d52d8ad5c10d5361fb7f7db0365ddde1327))
* **ci:** re-validate inventory data contract on upstream release ([#275](https://github.com/dryvist/ansible-splunk/issues/275)) ([398b9f7](https://github.com/dryvist/ansible-splunk/commit/398b9f7a2b16b54bc4ea062e32952f54588907ba))
* **cluster:** Splunk-native HA cluster topology and converge ([#376](https://github.com/dryvist/ansible-splunk/issues/376)) ([b33ef94](https://github.com/dryvist/ansible-splunk/commit/b33ef94eeef9d1d03870cb383b077169cc0667d2))
* Complete Splunk automation migration from terraform-proxmox ([#3](https://github.com/dryvist/ansible-splunk/issues/3)) ([86f6ca0](https://github.com/dryvist/ansible-splunk/commit/86f6ca06fc08d8c9ade01cb097f4068825545195))
* configure HEC token via inputs.conf template ([#31](https://github.com/dryvist/ansible-splunk/issues/31)) ([74cc915](https://github.com/dryvist/ansible-splunk/commit/74cc91569805c84beb10bcf2cdad0e1c9194ebd2))
* consolidate Splunk Docker deployment from ansible-proxmox-apps ([a1475a8](https://github.com/dryvist/ansible-splunk/commit/a1475a8e3fb3cd23e97b67dfe1354fc7d0feba8e))
* **cspell:** migrate to shared org-wide dictionary hierarchy ([6c639c0](https://github.com/dryvist/ansible-splunk/commit/6c639c0210f5c0ff7f88d3553c1e54b9e758f02b))
* deploy Splunk MCP Server for AI assistant integration ([#50](https://github.com/dryvist/ansible-splunk/issues/50)) ([0ff84fa](https://github.com/dryvist/ansible-splunk/commit/0ff84fa8ba8adfc21d703cd7778daaf17307e37c))
* disable automatic triggers on Claude-executing workflows ([b1f34ce](https://github.com/dryvist/ansible-splunk/commit/b1f34ce0b06559ceaca650cc6ef7f0a9baf71d6f))
* download VisiCore add-ons from GitHub Releases automatically ([#89](https://github.com/dryvist/ansible-splunk/issues/89)) ([81565a0](https://github.com/dryvist/ansible-splunk/commit/81565a04e8f3ab5f05a69b3f1bfa7b1c201313ad))
* enforce required Splunk apps with fail-fast validation ([#90](https://github.com/dryvist/ansible-splunk/issues/90)) ([c13e27d](https://github.com/dryvist/ansible-splunk/commit/c13e27d24bf94f94122ac44f1785822a80f33cd7))
* **hec:** allow per-token extra target indexes via extra_hec_indexes ([#302](https://github.com/dryvist/ansible-splunk/issues/302)) ([3193361](https://github.com/dryvist/ansible-splunk/commit/31933615be8556425e47c803df864aa4d884f61a))
* **hec:** decouple legacy token from namespace; use core to_uuid ([#256](https://github.com/dryvist/ansible-splunk/issues/256)) ([b80d1d4](https://github.com/dryvist/ansible-splunk/commit/b80d1d4560923579caa7e298ab62375d2b6537e6))
* **indexes:** add llm index + pipeline-silence and manager-panic alerts ([#246](https://github.com/dryvist/ansible-splunk/issues/246)) ([3283b30](https://github.com/dryvist/ansible-splunk/commit/3283b30949e8a5d425a8f9193bf369addd45733e))
* **indexes:** add monitoring-program indexes and dedupe unifi_metrics ([#301](https://github.com/dryvist/ansible-splunk/issues/301)) ([f2959a9](https://github.com/dryvist/ansible-splunk/commit/f2959a92151e2aeca9a61e073cbe311bcd0a7aae))
* **indexes:** add netflow index for NetFlow/IPFIX data ([#16](https://github.com/dryvist/ansible-splunk/issues/16)) ([7b2435b](https://github.com/dryvist/ansible-splunk/commit/7b2435b48aadb7c646bf33081215c133b256b2d2))
* **indexes:** add netmon index with 90-day retention ([#244](https://github.com/dryvist/ansible-splunk/issues/244)) ([c44a1d8](https://github.com/dryvist/ansible-splunk/commit/c44a1d89cd224a911bccd726f9083d49dbe3c655))
* **indexes:** add unifi_metrics + make unifi_metrics/netmon metric-datatype ([#255](https://github.com/dryvist/ansible-splunk/issues/255)) ([0f10945](https://github.com/dryvist/ansible-splunk/commit/0f109459fe1ade183f40fa67996034cef1baaa76))
* **indexes:** add unifi_metrics index (90-day) for UniFi controller telemetry ([#253](https://github.com/dryvist/ansible-splunk/issues/253)) ([8d00e33](https://github.com/dryvist/ansible-splunk/commit/8d00e3340dd54fb59d7a22e9f65bb77aad21e933))
* **inventory:** make S3 the sole live inventory source ([68492c2](https://github.com/dryvist/ansible-splunk/commit/68492c24868090d1f1cd9ea894604697c1fc9e47))
* **inventory:** resolve inventory S3-first via amazon.aws; DNS-first static fallback ([#249](https://github.com/dryvist/ansible-splunk/issues/249)) ([c3c26a8](https://github.com/dryvist/ansible-splunk/commit/c3c26a8caa56852eba7851739987ae5478405032))
* **ntp:** vendor ntp role and configure Splunk VM client ([#203](https://github.com/dryvist/ansible-splunk/issues/203)) ([4a464a3](https://github.com/dryvist/ansible-splunk/commit/4a464a346ec449d99ace163286182eb6d56a7cb8)), closes [#200](https://github.com/dryvist/ansible-splunk/issues/200)
* per-index HEC tokens via UUID v5 derivation ([8baabc3](https://github.com/dryvist/ansible-splunk/commit/8baabc3288fa4f3ebcdbf09b2d98a2a5e72cc702))
* pipeline sync - standardize env vars, fix HEC config ([#19](https://github.com/dryvist/ansible-splunk/issues/19)) ([f54ed53](https://github.com/dryvist/ansible-splunk/commit/f54ed53341ce3e13f4a63c0b5a91630a3560045b))
* refactor app management with Splunkbase registry and expose management port ([#48](https://github.com/dryvist/ansible-splunk/issues/48)) ([9331708](https://github.com/dryvist/ansible-splunk/commit/93317082f189579620c09a89d41032e0d701c24e))
* **renovate:** extend shared preset, remove duplicated rules ([7a21afb](https://github.com/dryvist/ansible-splunk/commit/7a21afb124a8c96e1f7f3670dfedcdd349521560))
* **scripts:** mint short-lived SSH certificates from the OpenBao CA in run-ansible.sh ([#349](https://github.com/dryvist/ansible-splunk/issues/349)) ([6a40a0a](https://github.com/dryvist/ansible-splunk/commit/6a40a0a912fe1abbcff8cc4c62a9ac850e7bec06))
* **splunk_docker:** add dedicated hermes index ([#357](https://github.com/dryvist/ansible-splunk/issues/357)) ([8baf82a](https://github.com/dryvist/ansible-splunk/commit/8baf82a03ad50167ba02ecbf281ab62912f0f4e5))
* **splunk_docker:** add LLM surface silence detectors and a freshness report ([#468](https://github.com/dryvist/ansible-splunk/issues/468)) ([857ed47](https://github.com/dryvist/ansible-splunk/commit/857ed471bfe3e33599b0c418d8451293f035c880))
* **splunk_docker:** add mac_perf index ([#184](https://github.com/dryvist/ansible-splunk/issues/184)) ([6acc906](https://github.com/dryvist/ansible-splunk/commit/6acc9069266771e24050f79f2eedb2e1aaa3303c))
* **splunk_docker:** add os_proxmox and os_ai to decompose the os catch-all ([#390](https://github.com/dryvist/ansible-splunk/issues/390)) ([c3e28a2](https://github.com/dryvist/ansible-splunk/commit/c3e28a2ac338e656f72900cb4c6771311f75c8aa))
* **splunk_docker:** add otel_traces index for OTLP trace spans ([#379](https://github.com/dryvist/ansible-splunk/issues/379)) ([4f8a618](https://github.com/dryvist/ansible-splunk/commit/4f8a61872606d9b0308b28f13cec1c09109fc8fa))
* **splunk_docker:** archive frozen buckets instead of deleting them ([#386](https://github.com/dryvist/ansible-splunk/issues/386)) ([7a1deca](https://github.com/dryvist/ansible-splunk/commit/7a1decaeb39bdc36c36941f7863b16f12ad032cd))
* **splunk_docker:** dedicated index per AI Docker service (7 new indexes) ([#473](https://github.com/dryvist/ansible-splunk/issues/473)) ([d327353](https://github.com/dryvist/ansible-splunk/commit/d3273537256875b5cf4991e79a037b896385f8c1))
* **splunk_docker:** Hermes delivery SLO alert (INC-17088) ([#355](https://github.com/dryvist/ansible-splunk/issues/355)) ([7c30d37](https://github.com/dryvist/ansible-splunk/commit/7c30d372fcf5cb7aa9a91730661a28c57d6d7f20))
* **splunk_docker:** hot_warm/cold volume tiering with a capacity preflight ([#384](https://github.com/dryvist/ansible-splunk/issues/384)) ([8eee970](https://github.com/dryvist/ansible-splunk/commit/8eee970f776bbe22777b2e62344d1ad0077a578f))
* **splunk_docker:** raise firewall and unifi index caps to round values ([#417](https://github.com/dryvist/ansible-splunk/issues/417)) ([7cc2595](https://github.com/dryvist/ansible-splunk/commit/7cc2595cf8d4dd7741e188d26f11a3029bad4af5))
* **splunk_docker:** tag the alerting tasks so a converge can scope to them ([#470](https://github.com/dryvist/ansible-splunk/issues/470)) ([dabfa0e](https://github.com/dryvist/ansible-splunk/commit/dabfa0eabc6ba8949ecd7f4383664062e1703ee7))
* **splunk_docker:** wire TA-slack-add-on-for-splunk into addons registry ([#186](https://github.com/dryvist/ansible-splunk/issues/186)) ([f93e5e0](https://github.com/dryvist/ansible-splunk/commit/f93e5e01b8d2f1c763d1740c9454e61a0e7fa05b))
* **splunk:** add hardware telemetry index + disk-failure alerts ([#374](https://github.com/dryvist/ansible-splunk/issues/374)) ([e88d206](https://github.com/dryvist/ansible-splunk/commit/e88d2066197de97b02e8859ea5db84d6cb2807ab))
* **splunk:** add macOS Cribl Edge silence-detector saved search ([774cdf2](https://github.com/dryvist/ansible-splunk/commit/774cdf2f857b4cce9521975f1b0f3e8b941e373f))
* **splunk:** add os_metrics metric index for host OS telemetry ([#363](https://github.com/dryvist/ansible-splunk/issues/363)) ([a3b311d](https://github.com/dryvist/ansible-splunk/commit/a3b311df9c1abdcd65c2c1235c2221a00cc00862))
* **splunk:** add Splunkbase 8278 registry entry ([#298](https://github.com/dryvist/ansible-splunk/issues/298)) ([3667421](https://github.com/dryvist/ansible-splunk/commit/3667421415fde94c55b6e8b8146fda6c5e6f41a5))
* **splunk:** add TA Studio splunkbase app ([#331](https://github.com/dryvist/ansible-splunk/issues/331)) ([891ddae](https://github.com/dryvist/ansible-splunk/commit/891ddaebab78b26011fb0c92a634ac9e90dd5294))
* **splunk:** add Traefik Splunkbase app ([#324](https://github.com/dryvist/ansible-splunk/issues/324)) ([df3ee3b](https://github.com/dryvist/ansible-splunk/commit/df3ee3bcb2a8a74a19b9530831a6c7f77ae8eb55))
* **splunk:** add workstation index ([#448](https://github.com/dryvist/ansible-splunk/issues/448)) ([50017b8](https://github.com/dryvist/ansible-splunk/commit/50017b88ccf8667339188ea8581a899bdd120463))
* **splunk:** alert on raw sector-counter movement, not just standing counts ([#453](https://github.com/dryvist/ansible-splunk/issues/453)) ([0f1bc4d](https://github.com/dryvist/ansible-splunk/commit/0f1bc4dbb58a52cb8ded73480c68bf2d19318f06))
* **splunk:** always-latest Splunkbase apps, air-gapped; fix install-once ([4096c02](https://github.com/dryvist/ansible-splunk/commit/4096c020f614e5122d64329a1ad82f8770636c77))
* **splunk:** archive Splunkbase release history ([#422](https://github.com/dryvist/ansible-splunk/issues/422)) ([9d6fec3](https://github.com/dryvist/ansible-splunk/commit/9d6fec30377b40a0b5cb363d4c770d1cfbf43f24))
* **splunk:** bench verdict-maturity + score-trend reports from mlx:bench feed ([#333](https://github.com/dryvist/ansible-splunk/issues/333)) ([23a3069](https://github.com/dryvist/ansible-splunk/commit/23a306977b152795f5ebcdf3aa1a58cb27d32a7a))
* **splunk:** cap the index volumes now the archive is proven ([#430](https://github.com/dryvist/ansible-splunk/issues/430)) ([7f9b513](https://github.com/dryvist/ansible-splunk/commit/7f9b513cfb48ef873a2a90cc3139fb310a719602))
* **splunk:** create the ansible index and deploy pipeline-staleness alerts ([#456](https://github.com/dryvist/ansible-splunk/issues/456)) ([f88eac1](https://github.com/dryvist/ansible-splunk/commit/f88eac1251fb0fb90c17d973f6c6caa292be805a))
* **splunk:** enable Splunk MCP token publish to OpenBao ([#345](https://github.com/dryvist/ansible-splunk/issues/345)) ([9850503](https://github.com/dryvist/ansible-splunk/commit/9850503b7d5d0473d44405227dae92b353ba02ff))
* **splunk:** enable the frozen-bucket archive ([#391](https://github.com/dryvist/ansible-splunk/issues/391)) ([381acec](https://github.com/dryvist/ansible-splunk/commit/381acecff58833ff14a1e851745d011f7d99dd5b))
* **splunk:** MinIO add-on registry + Splunkbase auto-sync ([7364448](https://github.com/dryvist/ansible-splunk/commit/736444891f658d374e85329b5fecb47cc5612a9d))
* **splunk:** mint per-user auth tokens for MCP service accounts ([#309](https://github.com/dryvist/ansible-splunk/issues/309)) ([74f68cb](https://github.com/dryvist/ansible-splunk/commit/74f68cb35ed1856a9808fbd467397388fa7a4d69))
* **splunk:** netflow index -&gt; 90-day retention + 50 GB cap ([#251](https://github.com/dryvist/ansible-splunk/issues/251)) ([65d14e7](https://github.com/dryvist/ansible-splunk/commit/65d14e7454c1d27be698ad9bef6eed6f06835011))
* **splunk:** night-cluster rank-error + idle-cluster saved searches ([5fedef0](https://github.com/dryvist/ansible-splunk/commit/5fedef0015664e8f9012209dab8efaaba46a4fd8))
* **splunk:** publish MCP credentials to OpenBao ([#341](https://github.com/dryvist/ansible-splunk/issues/341)) ([2550bbc](https://github.com/dryvist/ansible-splunk/commit/2550bbcd18e5e4ace7ce8f74a398b0f579f8e9ce))
* **splunk:** serving memory-headroom + Metal ceiling alerts ([#326](https://github.com/dryvist/ansible-splunk/issues/326)) ([bafb66e](https://github.com/dryvist/ansible-splunk/commit/bafb66eae47feae5ea22d20f08ada9eb307874f4))
* **splunk:** stage the otel_traces silence detector off the cutover gate ([#472](https://github.com/dryvist/ansible-splunk/issues/472)) ([456753a](https://github.com/dryvist/ansible-splunk/commit/456753a8da1ba4ee96b91ce1659930942ac30a6b))
* use shared OpenBao inventory resolver ([#339](https://github.com/dryvist/ansible-splunk/issues/339)) ([90f54e5](https://github.com/dryvist/ansible-splunk/commit/90f54e52f3ca586822f7efe509a1d0c516430104))


### Bug Fixes

* add automation bots to AI Moderator skip-bots ([#152](https://github.com/dryvist/ansible-splunk/issues/152)) ([7bbd048](https://github.com/dryvist/ansible-splunk/commit/7bbd0482ab672e0efab0f6e1db14e09a579d2ffc))
* add Nix dev shell tool execution rule ([#106](https://github.com/dryvist/ansible-splunk/issues/106)) ([3e3b08f](https://github.com/dryvist/ansible-splunk/commit/3e3b08f8e3236db17e3a230e2dc7c4278531a74b))
* add Python 3.9 for Splunk compatibility ([1f31a00](https://github.com/dryvist/ansible-splunk/commit/1f31a00839c9f0be7a22806eaf66e43869be2ddd))
* add python3-requests for community.docker modules ([fd53f27](https://github.com/dryvist/ansible-splunk/commit/fd53f277831bce17f41e8cd485448ec78880a9c1))
* add systemd restart policy for Docker daemon ([#108](https://github.com/dryvist/ansible-splunk/issues/108)) ([b7c1187](https://github.com/dryvist/ansible-splunk/commit/b7c118756c14b795138deba6deaeef33d57d2b9b))
* address CI failures ([e29fd74](https://github.com/dryvist/ansible-splunk/commit/e29fd745303d948f1947f93f6747b59c441ea037))
* address PR [#8](https://github.com/dryvist/ansible-splunk/issues/8) review feedback on Splunk Docker deployment ([416833d](https://github.com/dryvist/ansible-splunk/commit/416833db90c5a75bc47c65099f2eb5f155bef07a))
* allow all custom indexes in HEC token ([#32](https://github.com/dryvist/ansible-splunk/issues/32)) ([70e538c](https://github.com/dryvist/ansible-splunk/commit/70e538c9a13899061b1366be8f0e2df1ef64b958))
* **apps:** fail-soft guest-side add-on installs so config handlers still flush ([#308](https://github.com/dryvist/ansible-splunk/issues/308)) ([5935a27](https://github.com/dryvist/ansible-splunk/commit/5935a27faf223576e2e9aee95f19f3eb13aa8955))
* automate Splunkbase app downloads via REST API ([#115](https://github.com/dryvist/ansible-splunk/issues/115)) ([9129338](https://github.com/dryvist/ansible-splunk/commit/9129338fea7c85d80bb0b2cabf072a2cc04fbb7b))
* **ci:** add gh-aw-pin-refresh workflow and recompile lock files ([af66071](https://github.com/dryvist/ansible-splunk/commit/af6607151e1b8516e23a0301336a408ab069005b))
* **ci:** add pull-requests: write for release-please auto-approval ([#97](https://github.com/dryvist/ansible-splunk/issues/97)) ([c2112c1](https://github.com/dryvist/ansible-splunk/commit/c2112c1878dd6502c8fd029c5b0607334c13e135))
* **ci:** drop unused id-token: write from ci-fix.yml ([#450](https://github.com/dryvist/ansible-splunk/issues/450)) ([ae3a270](https://github.com/dryvist/ansible-splunk/commit/ae3a270655414a4d0e5076fa7805f247d5364b9d))
* **ci:** implement Merge Gatekeeper pattern with ci-gate ([#93](https://github.com/dryvist/ansible-splunk/issues/93)) ([90a173b](https://github.com/dryvist/ansible-splunk/commit/90a173b864aa175072e881a9fc6451bdc39eacaa))
* **ci:** install both requirements sections in the syntax-check job ([#427](https://github.com/dryvist/ansible-splunk/issues/427)) ([3c592da](https://github.com/dryvist/ansible-splunk/commit/3c592dab9da1811c66d7a31dafc80d02250fec96))
* **ci:** remove deprecated app-id secret passthrough ([6ef226f](https://github.com/dryvist/ansible-splunk/commit/6ef226f39bf5ab3dbd2674034d240d496524a476))
* **ci:** restore CI Fix auto-trigger as a thin cc-ci-fix wrapper ([ed61e6e](https://github.com/dryvist/ansible-splunk/commit/ed61e6e5b5aedb30301c2b417aa240f50d2fc948))
* **ci:** retarget reusable-workflow uses: refs to current org homes ([#230](https://github.com/dryvist/ansible-splunk/issues/230)) ([2ece34f](https://github.com/dryvist/ansible-splunk/commit/2ece34fb24bd40a3cc5dfecdd8f90186365c4afe))
* **ci:** use GitHub App token for release-please to trigger CI Gate ([#92](https://github.com/dryvist/ansible-splunk/issues/92)) ([4ac143f](https://github.com/dryvist/ansible-splunk/commit/4ac143f043c041d1640f3e1c190c9494ce043c21))
* complete pipeline sync - license, inventory paths, HEC config ([#20](https://github.com/dryvist/ansible-splunk/issues/20)) ([ce3ed22](https://github.com/dryvist/ansible-splunk/commit/ce3ed22b933e2885d3a17f4e1b190cebc57a7070))
* correct cloud.terraform version to 2.1.0 ([f01422e](https://github.com/dryvist/ansible-splunk/commit/f01422ec2f45a6b138dfbdb21f5968907f9fed9a))
* correct HEC protocol documentation from HTTP to HTTPS ([#95](https://github.com/dryvist/ansible-splunk/issues/95)) ([c91a757](https://github.com/dryvist/ansible-splunk/commit/c91a757958ebe4f1bdf847e339f527ec2a23ced2))
* correct MCP Server config and restore per-index HEC tokens ([#140](https://github.com/dryvist/ansible-splunk/issues/140)) ([24614d8](https://github.com/dryvist/ansible-splunk/commit/24614d8159f31385ccb793bc27a26ebb8fe4bced))
* **deps:** install both requirements sections, and ignore what they fetch ([#420](https://github.com/dryvist/ansible-splunk/issues/420)) ([6eaaff4](https://github.com/dryvist/ansible-splunk/commit/6eaaff40a9467c74cb946af6db9c3ba335380062))
* **deps:** refresh gh-aw action SHA pins ([88c409b](https://github.com/dryvist/ansible-splunk/commit/88c409b9c3286a4703f9d0f85ea064eb89f3ae8f))
* **deps:** refresh gh-aw action SHA pins ([#170](https://github.com/dryvist/ansible-splunk/issues/170)) ([8254d30](https://github.com/dryvist/ansible-splunk/commit/8254d300770f62f5ae64a126b12cae2969eae708))
* **deps:** refresh gh-aw action SHA pins ([#179](https://github.com/dryvist/ansible-splunk/issues/179)) ([9a3f9b8](https://github.com/dryvist/ansible-splunk/commit/9a3f9b8221bcd00efd5da693f0e503b3aa3b428f))
* **deps:** refresh gh-aw action SHA pins ([#188](https://github.com/dryvist/ansible-splunk/issues/188)) ([a884904](https://github.com/dryvist/ansible-splunk/commit/a884904cd6cf006d5e8437b44fb65e7c2e8e65fa))
* **deps:** refresh gh-aw action SHA pins ([#191](https://github.com/dryvist/ansible-splunk/issues/191)) ([c28e4d0](https://github.com/dryvist/ansible-splunk/commit/c28e4d0e7e40e13a8f08906a9cb3878d615870b3))
* **deps:** refresh gh-aw action SHA pins ([#194](https://github.com/dryvist/ansible-splunk/issues/194)) ([16a18fc](https://github.com/dryvist/ansible-splunk/commit/16a18fcc6600b245ed530fc3d48c0ba911254e73))
* **deps:** refresh gh-aw action SHA pins ([#197](https://github.com/dryvist/ansible-splunk/issues/197)) ([fe05bcd](https://github.com/dryvist/ansible-splunk/commit/fe05bcd80f991b34df205b4a6004773b11f6cae2))
* **deps:** refresh gh-aw action SHA pins ([#201](https://github.com/dryvist/ansible-splunk/issues/201)) ([944454a](https://github.com/dryvist/ansible-splunk/commit/944454a5377b87068c860da7595d7bf32496a039))
* **deps:** refresh gh-aw action SHA pins ([#205](https://github.com/dryvist/ansible-splunk/issues/205)) ([7a797bd](https://github.com/dryvist/ansible-splunk/commit/7a797bd7b022f3cb27f5ad10cba99f674db67f57))
* **deps:** refresh gh-aw action SHA pins ([#208](https://github.com/dryvist/ansible-splunk/issues/208)) ([64dc073](https://github.com/dryvist/ansible-splunk/commit/64dc073fd9a060e985bb6be9de980aa5670ed77b))
* **deps:** refresh gh-aw action SHA pins [aw:gh-aw-pin-refresh] ([#226](https://github.com/dryvist/ansible-splunk/issues/226)) ([fdc79a5](https://github.com/dryvist/ansible-splunk/commit/fdc79a538c1e2bf62b69804e975a2432f22df37e))
* **deps:** widen community.general ceiling to major (&lt;14.0.0) ([#265](https://github.com/dryvist/ansible-splunk/issues/265)) ([cde2389](https://github.com/dryvist/ansible-splunk/commit/cde2389d12800d78c6a2669515c720e3d5765dfd))
* disable internet access checks for air-gapped Splunk VM ([#23](https://github.com/dryvist/ansible-splunk/issues/23)) ([b37397e](https://github.com/dryvist/ansible-splunk/commit/b37397e448af0f844557dadd07116609c75ad188))
* **firewall:** disable guest iptables in favor of Proxmox firewall ([#14](https://github.com/dryvist/ansible-splunk/issues/14)) ([21a743e](https://github.com/dryvist/ansible-splunk/commit/21a743e4e7b265dd9ca9e8822e00dbb9479b8520))
* **gh-aw:** recompile agentic workflow lock files with v0.68.1 ([d83f93c](https://github.com/dryvist/ansible-splunk/commit/d83f93c7509937fa3ea53b308cfc7b8728601aae))
* grant contents: write for release-please workflow ([d5b6ec2](https://github.com/dryvist/ansible-splunk/commit/d5b6ec25392427b202cbb92a37bb8218f3dad977))
* **hec:** make per-index token activation work when HEC_NAMESPACE is set ([#260](https://github.com/dryvist/ansible-splunk/issues/260)) ([cee89e2](https://github.com/dryvist/ansible-splunk/commit/cee89e2045a93738eff98351198db2cbe04dbb52))
* **inventory:** correct splunk_vm key path in load_terraform.yml ([#25](https://github.com/dryvist/ansible-splunk/issues/25)) ([a747d47](https://github.com/dryvist/ansible-splunk/commit/a747d472d9e9edef1cc3aedabb088f95f93c453c))
* **inventory:** remove dead cloud.terraform plugin enable; scrub deleted-script references ([#250](https://github.com/dryvist/ansible-splunk/issues/250)) ([24000b9](https://github.com/dryvist/ansible-splunk/commit/24000b96aeb2a6d34f12b6ba27ad12bd4f067c2d))
* **inventory:** repoint containers['object-storage'] lookups to renamed key 's3' ([#317](https://github.com/dryvist/ansible-splunk/issues/317)) ([d277c06](https://github.com/dryvist/ansible-splunk/commit/d277c06d573caea119ddb93d009eb0936c6610f3))
* **inventory:** stop restating the Splunk VM hostname outside deployment.json ([#418](https://github.com/dryvist/ansible-splunk/issues/418)) ([67895b1](https://github.com/dryvist/ansible-splunk/commit/67895b13c4cc1fa11729bf3edad0edca085066d4))
* make Molecule idempotence check deterministic ([#55](https://github.com/dryvist/ansible-splunk/issues/55)) ([b8b9741](https://github.com/dryvist/ansible-splunk/commit/b8b97413bf35934d6256ebc7e8d6e55dfcaf08aa))
* make Splunk Docker deployment idempotent and enable SSL ([f50eef3](https://github.com/dryvist/ansible-splunk/commit/f50eef3f3dbb539038ca9339ca20a2ce8cef12fe))
* migrate release-please config to packages format ([4090064](https://github.com/dryvist/ansible-splunk/commit/4090064b5895eafd967198f7979c9ec33be3d37a))
* **ntp:** scope remote_tmp to chrony validate so site.yml deploys ([#274](https://github.com/dryvist/ansible-splunk/issues/274)) ([3196e35](https://github.com/dryvist/ansible-splunk/commit/3196e35a25ba8a9c2d0a53755080febddfcb3b65))
* pin ansible-core&gt;=2.16,&lt;2.18 for compatibility ([d4f90a9](https://github.com/dryvist/ansible-splunk/commit/d4f90a933c3c361bbcb3f9f39ce136b13099658c))
* pin Docker SDK versions for Molecule CI compatibility ([897b5d4](https://github.com/dryvist/ansible-splunk/commit/897b5d4e2fa506197b6321a88d4fe4348312e393))
* **playbooks:** align Splunk guest network with tofu inventory via guest agent ([#295](https://github.com/dryvist/ansible-splunk/issues/295)) ([5307125](https://github.com/dryvist/ansible-splunk/commit/5307125306623250b86b151eeb97093bb83f8477))
* **playbooks:** stop play vars_files clobbering group_vars overrides ([#312](https://github.com/dryvist/ansible-splunk/issues/312)) ([4ec0cd8](https://github.com/dryvist/ansible-splunk/commit/4ec0cd8e7a370126496ac6937921196c2aa878dd))
* point callers at renamed cc- reusable workflows ([5b9dd70](https://github.com/dryvist/ansible-splunk/commit/5b9dd701c01487e300138fac3ee813a7cfde9f6e))
* **pre-commit:** exclude release-please CHANGELOG.md from markdownlint ([#220](https://github.com/dryvist/ansible-splunk/issues/220)) ([a40f964](https://github.com/dryvist/ansible-splunk/commit/a40f964d37be6a9e306f05a6b22363981ce8f695))
* **release-please:** inherit dryvist/.github org-native caller ([#237](https://github.com/dryvist/ansible-splunk/issues/237)) ([06a70e0](https://github.com/dryvist/ansible-splunk/commit/06a70e06904725f721a1b68ed8b173d08e3c4796))
* remove claude-review workflow ([#114](https://github.com/dryvist/ansible-splunk/issues/114)) ([9d6f157](https://github.com/dryvist/ansible-splunk/commit/9d6f157b4f6c9afd8d3ea19dcf46a52e8fce577b))
* remove Python 3.9, use syntax-only molecule test ([294357a](https://github.com/dryvist/ansible-splunk/commit/294357a871870ad7217f33fdfadd88558978b4e5))
* remove quotes from inputs.conf values and add post-restart health check ([#34](https://github.com/dryvist/ansible-splunk/issues/34)) ([65c3fd3](https://github.com/dryvist/ansible-splunk/commit/65c3fd374cc7a3fa50a8f7ba7995d6a578682e9b))
* repoint retired-repo references to live canonical repos ([#239](https://github.com/dryvist/ansible-splunk/issues/239)) ([96f6a9f](https://github.com/dryvist/ansible-splunk/commit/96f6a9f16d9bc01d23732e7f9b9902ca84bf27f8))
* restructure CLAUDE.md from wiki to rulebook ([#120](https://github.com/dryvist/ansible-splunk/issues/120)) ([09c4b5b](https://github.com/dryvist/ansible-splunk/commit/09c4b5b3312f6fc4202b29a7134cc9f29e911f80))
* **runner:** keep OpenBao token out of argv ([866d811](https://github.com/dryvist/ansible-splunk/commit/866d811a78eb5ff55e8cccbd2fc34a2fc8327d33))
* **runner:** pass OpenBao token to Ansible ([a742638](https://github.com/dryvist/ansible-splunk/commit/a74263889321c0e733587ab393aff41b0fb8a9b9))
* set ANSIBLE_COLLECTIONS_PATH for molecule tests ([d6a9288](https://github.com/dryvist/ansible-splunk/commit/d6a9288fb50f4b4c6167cf4a20dd7582a928587e))
* **splunk_docker:** add openbao voter-health silence detector ([#445](https://github.com/dryvist/ansible-splunk/issues/445)) ([f6c2927](https://github.com/dryvist/ansible-splunk/commit/f6c2927ad9d0e50137b2a94be079ac7a3b6c571b))
* **splunk_docker:** alarm on index-volume headroom and freeze failures ([#412](https://github.com/dryvist/ansible-splunk/issues/412)) ([e594f78](https://github.com/dryvist/ansible-splunk/commit/e594f78f287b749c97d93590bf197edf4020ce29))
* **splunk_docker:** assert the MCP 202 patch actually landed ([#414](https://github.com/dryvist/ansible-splunk/issues/414)) ([0821479](https://github.com/dryvist/ansible-splunk/commit/0821479be0abbf23ddbb87b2929122fd6d0b1a20))
* **splunk_docker:** bring Splunk's own indexes inside the volume cap ([#440](https://github.com/dryvist/ansible-splunk/issues/440)) ([6adf9e3](https://github.com/dryvist/ansible-splunk/commit/6adf9e3af1caa48b41a1ff7ffa22a22b04e8cb25))
* **splunk_docker:** cap firewall and unifi by size for a week of headroom ([#401](https://github.com/dryvist/ansible-splunk/issues/401)) ([992a38e](https://github.com/dryvist/ansible-splunk/commit/992a38eea0daff2eb85e4abf86cbf2e2909c8dd1))
* **splunk_docker:** create host splunk user/group matching container UID ([#182](https://github.com/dryvist/ansible-splunk/issues/182)) ([446056d](https://github.com/dryvist/ansible-splunk/commit/446056de2fe85387b338b8b799f1813a29e408dc))
* **splunk_docker:** cut unifi retention to 90d to reclaim disk ([#399](https://github.com/dryvist/ansible-splunk/issues/399)) ([72a97e2](https://github.com/dryvist/ansible-splunk/commit/72a97e2be311d1ab56880e3523fa2fbc65e99e26))
* **splunk_docker:** deploy alerts to an app namespace so they dispatch ([#455](https://github.com/dryvist/ansible-splunk/issues/455)) ([aef95f8](https://github.com/dryvist/ansible-splunk/commit/aef95f8deb7f6f658ffe5542709555163399e6b1))
* **splunk_docker:** derive silence-detector lookback and threshold, not a flat constant ([#457](https://github.com/dryvist/ansible-splunk/issues/457)) ([446bc2a](https://github.com/dryvist/ansible-splunk/commit/446bc2a968376d4022fc6e2c7833aa15709c8d95))
* **splunk_docker:** fall back to a config file for frozen-archive creds ([#403](https://github.com/dryvist/ansible-splunk/issues/403)) ([75950fa](https://github.com/dryvist/ansible-splunk/commit/75950faf492d314129b9afe2a3408bfa535ecc04))
* **splunk_docker:** guard tstats zero-row blind spot in silence detectors ([#460](https://github.com/dryvist/ansible-splunk/issues/460)) ([389dbcc](https://github.com/dryvist/ansible-splunk/commit/389dbcc8a0d445f7e90ba5133f344d6e2daab1a0))
* **splunk_docker:** install the extractor the archive unpack needs ([#437](https://github.com/dryvist/ansible-splunk/issues/437)) ([d167401](https://github.com/dryvist/ansible-splunk/commit/d167401cdf201675db11e227a6dfa23384292247))
* **splunk_docker:** make volume caps opt-in so the guard cannot block itself ([#388](https://github.com/dryvist/ansible-splunk/issues/388)) ([f2c068d](https://github.com/dryvist/ansible-splunk/commit/f2c068d75f9cad6b60eec267b0e5c2caa0c0bed5))
* **splunk_docker:** match grouped-stats BY keyword case-insensitively ([#465](https://github.com/dryvist/ansible-splunk/issues/465)) ([0e4034f](https://github.com/dryvist/ansible-splunk/commit/0e4034f4ed02a7fca2c2741cc696b0685e9ccf6e))
* **splunk_docker:** move frozen archive to a dedicated B2 bucket ([#405](https://github.com/dryvist/ansible-splunk/issues/405)) ([1fa0ead](https://github.com/dryvist/ansible-splunk/commit/1fa0ead8cb29c83d928ad2dcfa6eedbb79a55793))
* **splunk_docker:** order the archive before compose, and make dry runs work ([#393](https://github.com/dryvist/ansible-splunk/issues/393)) ([7a7d1c4](https://github.com/dryvist/ansible-splunk/commit/7a7d1c4ea3da8d813720695e065be84f451c0c55))
* **splunk_docker:** publish the Traefik-fronted MCP URL, not the raw mgmt endpoint ([#351](https://github.com/dryvist/ansible-splunk/issues/351)) ([ddbab68](https://github.com/dryvist/ansible-splunk/commit/ddbab6862f0d48c98bb272e95b285b2e3b74ebb9))
* **splunk_docker:** reclaim index-volume capacity hidden by fs reserve ([#381](https://github.com/dryvist/ansible-splunk/issues/381)) ([a5eab6e](https://github.com/dryvist/ansible-splunk/commit/a5eab6ecb870a032219a237b1d27482a40b22c95))
* **splunk_docker:** repoint router silence/spike detectors to index=os_ai ([#462](https://github.com/dryvist/ansible-splunk/issues/462)) ([bd7481e](https://github.com/dryvist/ansible-splunk/commit/bd7481e5e863e9b012067c98b67a4cd75e72d3c1))
* **splunk_docker:** retry transport failures in the freeze upload ([#396](https://github.com/dryvist/ansible-splunk/issues/396)) ([fd061a6](https://github.com/dryvist/ansible-splunk/commit/fd061a6c913f5db6e723c486113aebd2c6434fa1))
* **splunk_docker:** return HTTP 202 for notifications/initialized ([#335](https://github.com/dryvist/ansible-splunk/issues/335)) ([3a65d1a](https://github.com/dryvist/ansible-splunk/commit/3a65d1a4b1df3e414c3df9feceed31f71a091057))
* **splunk_docker:** shorten cold_to_frozen upload timeout to 60s ([#407](https://github.com/dryvist/ansible-splunk/issues/407)) ([bc0d5b3](https://github.com/dryvist/ansible-splunk/commit/bc0d5b3f13b56b547e70ac584feb54c5b75608dd))
* **splunk_docker:** stop the archive probing for a bucket it cannot create ([#441](https://github.com/dryvist/ansible-splunk/issues/441)) ([3a0b94c](https://github.com/dryvist/ansible-splunk/commit/3a0b94c0b0cd3db0d38bb734a33f25ba21e55ada))
* **splunk_docker:** stream frozen-bucket uploads and make restore usable ([#416](https://github.com/dryvist/ansible-splunk/issues/416)) ([e5c72cf](https://github.com/dryvist/ansible-splunk/commit/e5c72cf140e1bf230211a18dde982ccb0ddf9130))
* **splunk:** auto-reconcile admin password with SPLUNK_PASSWORD ([#282](https://github.com/dryvist/ansible-splunk/issues/282)) ([d3718b1](https://github.com/dryvist/ansible-splunk/commit/d3718b1eb039a10af1f4bc5db31c0a97bd2a5264))
* **splunkbase:** fail on a missing object-storage client, not on storage ([#429](https://github.com/dryvist/ansible-splunk/issues/429)) ([156b907](https://github.com/dryvist/ansible-splunk/commit/156b907e4ec400e20a6d5fae76870bdbbb5a7cce))
* **splunk:** drop the orphaned otel index ([#471](https://github.com/dryvist/ansible-splunk/issues/471)) ([b857df8](https://github.com/dryvist/ansible-splunk/commit/b857df81642d3dcc6597f884a8d5ada483f91bc4))
* **splunk:** keep OpenBao publishing controller-local ([d8a7c2a](https://github.com/dryvist/ansible-splunk/commit/d8a7c2a645d7c2ad260c0cf41e5d91c7c5f33170))
* **splunk:** mint MCP tokens via the app mcp_token endpoint (aud=mcp) ([#313](https://github.com/dryvist/ansible-splunk/issues/313)) ([4487d18](https://github.com/dryvist/ansible-splunk/commit/4487d183e6c69c78eb0e272c55dc5e225ddbd55a))
* **splunk:** rename metric index netmon -&gt; netmon_metrics ([#269](https://github.com/dryvist/ansible-splunk/issues/269)) ([1b110e0](https://github.com/dryvist/ansible-splunk/commit/1b110e0c4764b4d8dd7bf2e3b7bef2cef6d82859))
* **splunk:** repoint Splunkbase sync MinIO → object-storage (RustFS) ([#276](https://github.com/dryvist/ansible-splunk/issues/276)) ([b318baa](https://github.com/dryvist/ansible-splunk/commit/b318baa86045852065eade5c9bb823ad0d6616a0))
* **splunk:** restore the freshness report's search, welded away by a comment ([#477](https://github.com/dryvist/ansible-splunk/issues/477)) ([a28e380](https://github.com/dryvist/ansible-splunk/commit/a28e3807ba8a457bd129476bb987d4f152d7a39b))
* **splunk:** rotate managed MCP token safely ([#366](https://github.com/dryvist/ansible-splunk/issues/366)) ([6296b4a](https://github.com/dryvist/ansible-splunk/commit/6296b4a6ae8e61cc78b393ac342b25b9a222cc72))
* **splunk:** secure OpenBao-backed token publication ([93b0cb4](https://github.com/dryvist/ansible-splunk/commit/93b0cb4680ef21a98e1da013ce42a6d2a8af3f90))
* **splunk:** size the frozen-upload timeout as a stall detector ([#426](https://github.com/dryvist/ansible-splunk/issues/426)) ([bc9653c](https://github.com/dryvist/ansible-splunk/commit/bc9653c8ec8cd8a9a705f1f021fd94576575a5aa))
* **splunk:** validate MCP tokens the way Splunk actually issues them ([#434](https://github.com/dryvist/ansible-splunk/issues/434)) ([66d8ac9](https://github.com/dryvist/ansible-splunk/commit/66d8ac9f42b19628c791639e4746fcd916e22bf9))
* support Python 3.9 and fix Docker-in-Docker storage ([0bed704](https://github.com/dryvist/ansible-splunk/commit/0bed7047e788dfd7a55a7b03f4b2cfb426f89b3b))
* update CI badge links to point to ci-gate.yml ([#166](https://github.com/dryvist/ansible-splunk/issues/166)) ([6645415](https://github.com/dryvist/ansible-splunk/commit/6645415a96fab58b366f1463ee33d38fc1c8801f))
* update SSH configuration and inventory for Splunk VM ([2ac5dde](https://github.com/dryvist/ansible-splunk/commit/2ac5ddea3f34d3ceb0fde1aaedc41b503dc389c2))
* update stale nix-config references to nix-ai ([#105](https://github.com/dryvist/ansible-splunk/issues/105)) ([a657710](https://github.com/dryvist/ansible-splunk/commit/a657710ca9d6589333be699bf32a11b3919c1e1f))
* use ansible_facts dict to avoid INJECT_FACTS_AS_VARS deprecation ([#33](https://github.com/dryvist/ansible-splunk/issues/33)) ([b3f3bb0](https://github.com/dryvist/ansible-splunk/commit/b3f3bb06b232c4cea1b3edddd5199683096abbfa))
* use flexible community.docker version and verify collections ([1d3bbe1](https://github.com/dryvist/ansible-splunk/commit/1d3bbe1e19774bb58fb010af8d2957cc8c0e0952))
* use include_role in post_tasks so role defaults are available ([#35](https://github.com/dryvist/ansible-splunk/issues/35)) ([09c79ec](https://github.com/dryvist/ansible-splunk/commit/09c79ec2a12040b972111398c902c6f8f0a7c5b5))
* use nix-devenv ansible-apps shell instead of local flake.nix ([#110](https://github.com/dryvist/ansible-splunk/issues/110)) ([d18a3ca](https://github.com/dryvist/ansible-splunk/commit/d18a3ca7e65f6fa028e3f36413ecba376b607323))
* use packages attr, add doppler, gitignore .direnv ([#78](https://github.com/dryvist/ansible-splunk/issues/78)) ([2a05c4f](https://github.com/dryvist/ansible-splunk/commit/2a05c4f0f8bf50281e9c2e9bb13774bebb7bea1c))
* use role-prefixed variable names for ansible-lint compliance ([d1f9887](https://github.com/dryvist/ansible-splunk/commit/d1f98872f710e78372935ca7e2c36e4a5c23cbc0))
* use selectattr 'defined' test for github_repo filter ([#101](https://github.com/dryvist/ansible-splunk/issues/101)) ([409cdea](https://github.com/dryvist/ansible-splunk/commit/409cdeae623b2f2d7789289c98d3bc89c60435ca))


### Performance

* **ci:** cut Molecule runtime from ~30min to ~8min ([#56](https://github.com/dryvist/ansible-splunk/issues/56)) ([ef179a4](https://github.com/dryvist/ansible-splunk/commit/ef179a40513e328f3feb59cfb3d18e9f80a2901a))


### Refactoring

* **sync-splunkbase:** use the AWS CLI for object storage ([#438](https://github.com/dryvist/ansible-splunk/issues/438)) ([e82faa2](https://github.com/dryvist/ansible-splunk/commit/e82faa294a99665116167509e5843af00b2f7a94))

## [0.60.0](https://github.com/dryvist/ansible-splunk/compare/v0.59.0...v0.60.0) (2026-08-07)


### Features

* **splunk:** stage the otel_traces silence detector off the cutover gate ([#472](https://github.com/dryvist/ansible-splunk/issues/472)) ([456753a](https://github.com/dryvist/ansible-splunk/commit/456753a8da1ba4ee96b91ce1659930942ac30a6b))

## [0.59.0](https://github.com/dryvist/ansible-splunk/compare/v0.58.0...v0.59.0) (2026-08-07)


### Features

* **splunk_docker:** tag the alerting tasks so a converge can scope to them ([#470](https://github.com/dryvist/ansible-splunk/issues/470)) ([dabfa0e](https://github.com/dryvist/ansible-splunk/commit/dabfa0eabc6ba8949ecd7f4383664062e1703ee7))

## [0.58.0](https://github.com/dryvist/ansible-splunk/compare/v0.57.0...v0.58.0) (2026-08-07)


### Features

* **splunk_docker:** dedicated index per AI Docker service (7 new indexes) ([#473](https://github.com/dryvist/ansible-splunk/issues/473)) ([d327353](https://github.com/dryvist/ansible-splunk/commit/d3273537256875b5cf4991e79a037b896385f8c1))

## [0.57.0](https://github.com/dryvist/ansible-splunk/compare/v0.56.0...v0.57.0) (2026-08-05)


### Features

* **splunk_docker:** add LLM surface silence detectors and a freshness report ([#468](https://github.com/dryvist/ansible-splunk/issues/468)) ([857ed47](https://github.com/dryvist/ansible-splunk/commit/857ed471bfe3e33599b0c418d8451293f035c880))

## [0.56.0](https://github.com/dryvist/ansible-splunk/compare/v0.55.5...v0.56.0) (2026-08-04)


### Features

* **splunk:** create the ansible index and deploy pipeline-staleness alerts ([#456](https://github.com/dryvist/ansible-splunk/issues/456)) ([f88eac1](https://github.com/dryvist/ansible-splunk/commit/f88eac1251fb0fb90c17d973f6c6caa292be805a))

## [0.55.5](https://github.com/dryvist/ansible-splunk/compare/v0.55.4...v0.55.5) (2026-08-04)


### Bug Fixes

* **splunk_docker:** match grouped-stats BY keyword case-insensitively ([#465](https://github.com/dryvist/ansible-splunk/issues/465)) ([0e4034f](https://github.com/dryvist/ansible-splunk/commit/0e4034f4ed02a7fca2c2741cc696b0685e9ccf6e))

## [0.55.4](https://github.com/dryvist/ansible-splunk/compare/v0.55.3...v0.55.4) (2026-08-04)


### Bug Fixes

* **splunk_docker:** repoint router silence/spike detectors to index=os_ai ([#462](https://github.com/dryvist/ansible-splunk/issues/462)) ([bd7481e](https://github.com/dryvist/ansible-splunk/commit/bd7481e5e863e9b012067c98b67a4cd75e72d3c1))

## [0.55.3](https://github.com/dryvist/ansible-splunk/compare/v0.55.2...v0.55.3) (2026-08-04)


### Bug Fixes

* **splunk_docker:** guard tstats zero-row blind spot in silence detectors ([#460](https://github.com/dryvist/ansible-splunk/issues/460)) ([389dbcc](https://github.com/dryvist/ansible-splunk/commit/389dbcc8a0d445f7e90ba5133f344d6e2daab1a0))

## [0.55.2](https://github.com/dryvist/ansible-splunk/compare/v0.55.1...v0.55.2) (2026-08-04)


### Bug Fixes

* **splunk_docker:** derive silence-detector lookback and threshold, not a flat constant ([#457](https://github.com/dryvist/ansible-splunk/issues/457)) ([446bc2a](https://github.com/dryvist/ansible-splunk/commit/446bc2a968376d4022fc6e2c7833aa15709c8d95))

## [0.55.1](https://github.com/dryvist/ansible-splunk/compare/v0.55.0...v0.55.1) (2026-08-04)


### Bug Fixes

* **splunk_docker:** deploy alerts to an app namespace so they dispatch ([#455](https://github.com/dryvist/ansible-splunk/issues/455)) ([aef95f8](https://github.com/dryvist/ansible-splunk/commit/aef95f8deb7f6f658ffe5542709555163399e6b1))

## [0.55.0](https://github.com/dryvist/ansible-splunk/compare/v0.54.1...v0.55.0) (2026-08-04)


### Features

* **splunk:** alert on raw sector-counter movement, not just standing counts ([#453](https://github.com/dryvist/ansible-splunk/issues/453)) ([0f1bc4d](https://github.com/dryvist/ansible-splunk/commit/0f1bc4dbb58a52cb8ded73480c68bf2d19318f06))

## [0.54.1](https://github.com/dryvist/ansible-splunk/compare/v0.54.0...v0.54.1) (2026-08-02)


### Bug Fixes

* **ci:** drop unused id-token: write from ci-fix.yml ([#450](https://github.com/dryvist/ansible-splunk/issues/450)) ([ae3a270](https://github.com/dryvist/ansible-splunk/commit/ae3a270655414a4d0e5076fa7805f247d5364b9d))

## [0.54.0](https://github.com/dryvist/ansible-splunk/compare/v0.53.2...v0.54.0) (2026-08-02)


### Features

* **splunk:** add workstation index ([#448](https://github.com/dryvist/ansible-splunk/issues/448)) ([50017b8](https://github.com/dryvist/ansible-splunk/commit/50017b88ccf8667339188ea8581a899bdd120463))


### Bug Fixes

* **splunk_docker:** add openbao voter-health silence detector ([#445](https://github.com/dryvist/ansible-splunk/issues/445)) ([f6c2927](https://github.com/dryvist/ansible-splunk/commit/f6c2927ad9d0e50137b2a94be079ac7a3b6c571b))

## [0.53.2](https://github.com/dryvist/ansible-splunk/compare/v0.53.1...v0.53.2) (2026-07-31)


### Bug Fixes

* **splunk_docker:** stop the archive probing for a bucket it cannot create ([#441](https://github.com/dryvist/ansible-splunk/issues/441)) ([3a0b94c](https://github.com/dryvist/ansible-splunk/commit/3a0b94c0b0cd3db0d38bb734a33f25ba21e55ada))

## [0.53.1](https://github.com/dryvist/ansible-splunk/compare/v0.53.0...v0.53.1) (2026-07-31)


### Bug Fixes

* **splunk_docker:** bring Splunk's own indexes inside the volume cap ([#440](https://github.com/dryvist/ansible-splunk/issues/440)) ([6adf9e3](https://github.com/dryvist/ansible-splunk/commit/6adf9e3af1caa48b41a1ff7ffa22a22b04e8cb25))

## [0.53.0](https://github.com/dryvist/ansible-splunk/compare/v0.52.2...v0.53.0) (2026-07-31)


### ⚠ BREAKING CHANGES

* **sync-splunkbase:** the controller now needs `aws` on PATH instead of the previous object-storage client.

### Refactoring

* **sync-splunkbase:** use the AWS CLI for object storage ([#438](https://github.com/dryvist/ansible-splunk/issues/438)) ([e82faa2](https://github.com/dryvist/ansible-splunk/commit/e82faa294a99665116167509e5843af00b2f7a94))

## [0.52.2](https://github.com/dryvist/ansible-splunk/compare/v0.52.1...v0.52.2) (2026-07-31)


### Bug Fixes

* **splunk_docker:** install the extractor the archive unpack needs ([#437](https://github.com/dryvist/ansible-splunk/issues/437)) ([d167401](https://github.com/dryvist/ansible-splunk/commit/d167401cdf201675db11e227a6dfa23384292247))

## [0.52.1](https://github.com/dryvist/ansible-splunk/compare/v0.52.0...v0.52.1) (2026-07-31)


### Bug Fixes

* **splunk:** validate MCP tokens the way Splunk actually issues them ([#434](https://github.com/dryvist/ansible-splunk/issues/434)) ([66d8ac9](https://github.com/dryvist/ansible-splunk/commit/66d8ac9f42b19628c791639e4746fcd916e22bf9))

## [0.52.0](https://github.com/dryvist/ansible-splunk/compare/v0.51.3...v0.52.0) (2026-07-31)


### Features

* **splunk:** cap the index volumes now the archive is proven ([#430](https://github.com/dryvist/ansible-splunk/issues/430)) ([7f9b513](https://github.com/dryvist/ansible-splunk/commit/7f9b513cfb48ef873a2a90cc3139fb310a719602))


### Bug Fixes

* **splunkbase:** fail on a missing object-storage client, not on storage ([#429](https://github.com/dryvist/ansible-splunk/issues/429)) ([156b907](https://github.com/dryvist/ansible-splunk/commit/156b907e4ec400e20a6d5fae76870bdbbb5a7cce))

## [0.51.3](https://github.com/dryvist/ansible-splunk/compare/v0.51.2...v0.51.3) (2026-07-31)


### Bug Fixes

* **ci:** install both requirements sections in the syntax-check job ([#427](https://github.com/dryvist/ansible-splunk/issues/427)) ([3c592da](https://github.com/dryvist/ansible-splunk/commit/3c592dab9da1811c66d7a31dafc80d02250fec96))

## [0.51.2](https://github.com/dryvist/ansible-splunk/compare/v0.51.1...v0.51.2) (2026-07-31)


### Bug Fixes

* **splunk:** size the frozen-upload timeout as a stall detector ([#426](https://github.com/dryvist/ansible-splunk/issues/426)) ([bc9653c](https://github.com/dryvist/ansible-splunk/commit/bc9653c8ec8cd8a9a705f1f021fd94576575a5aa))

## [0.51.1](https://github.com/dryvist/ansible-splunk/compare/v0.51.0...v0.51.1) (2026-07-31)


### Bug Fixes

* **deps:** install both requirements sections, and ignore what they fetch ([#420](https://github.com/dryvist/ansible-splunk/issues/420)) ([6eaaff4](https://github.com/dryvist/ansible-splunk/commit/6eaaff40a9467c74cb946af6db9c3ba335380062))

## [0.51.0](https://github.com/dryvist/ansible-splunk/compare/v0.50.0...v0.51.0) (2026-07-31)


### Features

* **splunk_docker:** raise firewall and unifi index caps to round values ([#417](https://github.com/dryvist/ansible-splunk/issues/417)) ([7cc2595](https://github.com/dryvist/ansible-splunk/commit/7cc2595cf8d4dd7741e188d26f11a3029bad4af5))


### Bug Fixes

* **splunk_docker:** stream frozen-bucket uploads and make restore usable ([#416](https://github.com/dryvist/ansible-splunk/issues/416)) ([e5c72cf](https://github.com/dryvist/ansible-splunk/commit/e5c72cf140e1bf230211a18dde982ccb0ddf9130))

## [0.50.0](https://github.com/dryvist/ansible-splunk/compare/v0.49.10...v0.50.0) (2026-07-31)


### Features

* **splunk:** archive Splunkbase release history ([#422](https://github.com/dryvist/ansible-splunk/issues/422)) ([9d6fec3](https://github.com/dryvist/ansible-splunk/commit/9d6fec30377b40a0b5cb363d4c770d1cfbf43f24))

## [Unreleased]

### Added

* Archive every exposed Splunkbase release under an immutable RustFS key with a SHA-256 catalog, while keeping archive-only references out of the Splunk VM manifest.

## [0.49.10](https://github.com/dryvist/ansible-splunk/compare/v0.49.9...v0.49.10) (2026-07-31)


### Bug Fixes

* **inventory:** stop restating the Splunk VM hostname outside deployment.json ([#418](https://github.com/dryvist/ansible-splunk/issues/418)) ([67895b1](https://github.com/dryvist/ansible-splunk/commit/67895b13c4cc1fa11729bf3edad0edca085066d4))

## [0.49.9](https://github.com/dryvist/ansible-splunk/compare/v0.49.8...v0.49.9) (2026-07-29)


### Bug Fixes

* **splunk_docker:** assert the MCP 202 patch actually landed ([#414](https://github.com/dryvist/ansible-splunk/issues/414)) ([0821479](https://github.com/dryvist/ansible-splunk/commit/0821479be0abbf23ddbb87b2929122fd6d0b1a20))

## [0.49.8](https://github.com/dryvist/ansible-splunk/compare/v0.49.7...v0.49.8) (2026-07-27)


### Bug Fixes

* **splunk_docker:** alarm on index-volume headroom and freeze failures ([#412](https://github.com/dryvist/ansible-splunk/issues/412)) ([e594f78](https://github.com/dryvist/ansible-splunk/commit/e594f78f287b749c97d93590bf197edf4020ce29))

## [0.49.7](https://github.com/dryvist/ansible-splunk/compare/v0.49.6...v0.49.7) (2026-07-27)


### Bug Fixes

* **splunk_docker:** shorten cold_to_frozen upload timeout to 60s ([#407](https://github.com/dryvist/ansible-splunk/issues/407)) ([bc0d5b3](https://github.com/dryvist/ansible-splunk/commit/bc0d5b3f13b56b547e70ac584feb54c5b75608dd))

## [0.49.6](https://github.com/dryvist/ansible-splunk/compare/v0.49.5...v0.49.6) (2026-07-26)


### Bug Fixes

* **splunk_docker:** move frozen archive to a dedicated B2 bucket ([#405](https://github.com/dryvist/ansible-splunk/issues/405)) ([1fa0ead](https://github.com/dryvist/ansible-splunk/commit/1fa0ead8cb29c83d928ad2dcfa6eedbb79a55793))

## [0.49.5](https://github.com/dryvist/ansible-splunk/compare/v0.49.4...v0.49.5) (2026-07-26)


### Bug Fixes

* **splunk_docker:** fall back to a config file for frozen-archive creds ([#403](https://github.com/dryvist/ansible-splunk/issues/403)) ([75950fa](https://github.com/dryvist/ansible-splunk/commit/75950faf492d314129b9afe2a3408bfa535ecc04))

## [0.49.4](https://github.com/dryvist/ansible-splunk/compare/v0.49.3...v0.49.4) (2026-07-26)


### Bug Fixes

* **splunk_docker:** cap firewall and unifi by size for a week of headroom ([#401](https://github.com/dryvist/ansible-splunk/issues/401)) ([992a38e](https://github.com/dryvist/ansible-splunk/commit/992a38eea0daff2eb85e4abf86cbf2e2909c8dd1))

## [0.49.3](https://github.com/dryvist/ansible-splunk/compare/v0.49.2...v0.49.3) (2026-07-26)


### Bug Fixes

* **splunk_docker:** cut unifi retention to 90d to reclaim disk ([#399](https://github.com/dryvist/ansible-splunk/issues/399)) ([72a97e2](https://github.com/dryvist/ansible-splunk/commit/72a97e2be311d1ab56880e3523fa2fbc65e99e26))

## [0.49.2](https://github.com/dryvist/ansible-splunk/compare/v0.49.1...v0.49.2) (2026-07-26)


### Bug Fixes

* **splunk_docker:** retry transport failures in the freeze upload ([#396](https://github.com/dryvist/ansible-splunk/issues/396)) ([fd061a6](https://github.com/dryvist/ansible-splunk/commit/fd061a6c913f5db6e723c486113aebd2c6434fa1))

## [0.49.1](https://github.com/dryvist/ansible-splunk/compare/v0.49.0...v0.49.1) (2026-07-26)


### Bug Fixes

* **splunk_docker:** order the archive before compose, and make dry runs work ([#393](https://github.com/dryvist/ansible-splunk/issues/393)) ([7a7d1c4](https://github.com/dryvist/ansible-splunk/commit/7a7d1c4ea3da8d813720695e065be84f451c0c55))

## [0.49.0](https://github.com/dryvist/ansible-splunk/compare/v0.48.0...v0.49.0) (2026-07-26)


### Features

* **splunk_docker:** add os_proxmox and os_ai to decompose the os catch-all ([#390](https://github.com/dryvist/ansible-splunk/issues/390)) ([c3e28a2](https://github.com/dryvist/ansible-splunk/commit/c3e28a2ac338e656f72900cb4c6771311f75c8aa))

## [0.48.0](https://github.com/dryvist/ansible-splunk/compare/v0.47.1...v0.48.0) (2026-07-26)


### Features

* **splunk:** enable the frozen-bucket archive ([#391](https://github.com/dryvist/ansible-splunk/issues/391)) ([381acec](https://github.com/dryvist/ansible-splunk/commit/381acecff58833ff14a1e851745d011f7d99dd5b))

## [0.47.1](https://github.com/dryvist/ansible-splunk/compare/v0.47.0...v0.47.1) (2026-07-26)


### Bug Fixes

* **splunk_docker:** make volume caps opt-in so the guard cannot block itself ([#388](https://github.com/dryvist/ansible-splunk/issues/388)) ([f2c068d](https://github.com/dryvist/ansible-splunk/commit/f2c068d75f9cad6b60eec267b0e5c2caa0c0bed5))

## [0.47.0](https://github.com/dryvist/ansible-splunk/compare/v0.46.0...v0.47.0) (2026-07-26)


### Features

* **splunk_docker:** archive frozen buckets instead of deleting them ([#386](https://github.com/dryvist/ansible-splunk/issues/386)) ([7a1deca](https://github.com/dryvist/ansible-splunk/commit/7a1decaeb39bdc36c36941f7863b16f12ad032cd))

## [0.46.0](https://github.com/dryvist/ansible-splunk/compare/v0.45.1...v0.46.0) (2026-07-26)


### Features

* **splunk_docker:** hot_warm/cold volume tiering with a capacity preflight ([#384](https://github.com/dryvist/ansible-splunk/issues/384)) ([8eee970](https://github.com/dryvist/ansible-splunk/commit/8eee970f776bbe22777b2e62344d1ad0077a578f))

## [0.45.1](https://github.com/dryvist/ansible-splunk/compare/v0.45.0...v0.45.1) (2026-07-26)


### Bug Fixes

* **splunk_docker:** reclaim index-volume capacity hidden by fs reserve ([#381](https://github.com/dryvist/ansible-splunk/issues/381)) ([a5eab6e](https://github.com/dryvist/ansible-splunk/commit/a5eab6ecb870a032219a237b1d27482a40b22c95))

## [0.45.0](https://github.com/dryvist/ansible-splunk/compare/v0.44.0...v0.45.0) (2026-07-25)


### Features

* **splunk_docker:** add otel_traces index for OTLP trace spans ([#379](https://github.com/dryvist/ansible-splunk/issues/379)) ([4f8a618](https://github.com/dryvist/ansible-splunk/commit/4f8a61872606d9b0308b28f13cec1c09109fc8fa))

## [0.44.0](https://github.com/dryvist/ansible-splunk/compare/v0.43.0...v0.44.0) (2026-07-24)


### Features

* **cluster:** Splunk-native HA cluster topology and converge ([#376](https://github.com/dryvist/ansible-splunk/issues/376)) ([b33ef94](https://github.com/dryvist/ansible-splunk/commit/b33ef94eeef9d1d03870cb383b077169cc0667d2))

## [0.43.0](https://github.com/dryvist/ansible-splunk/compare/v0.42.2...v0.43.0) (2026-07-23)


### Features

* **splunk:** add hardware telemetry index + disk-failure alerts ([#374](https://github.com/dryvist/ansible-splunk/issues/374)) ([e88d206](https://github.com/dryvist/ansible-splunk/commit/e88d2066197de97b02e8859ea5db84d6cb2807ab))

## [0.42.2](https://github.com/dryvist/ansible-splunk/compare/v0.42.1...v0.42.2) (2026-07-22)


### Bug Fixes

* **runner:** keep OpenBao token out of argv ([866d811](https://github.com/dryvist/ansible-splunk/commit/866d811a78eb5ff55e8cccbd2fc34a2fc8327d33))
* **runner:** pass OpenBao token to Ansible ([a742638](https://github.com/dryvist/ansible-splunk/commit/a74263889321c0e733587ab393aff41b0fb8a9b9))
* **splunk:** keep OpenBao publishing controller-local ([d8a7c2a](https://github.com/dryvist/ansible-splunk/commit/d8a7c2a645d7c2ad260c0cf41e5d91c7c5f33170))
* **splunk:** secure OpenBao-backed token publication ([93b0cb4](https://github.com/dryvist/ansible-splunk/commit/93b0cb4680ef21a98e1da013ce42a6d2a8af3f90))

## [0.42.1](https://github.com/dryvist/ansible-splunk/compare/v0.42.0...v0.42.1) (2026-07-22)


### Bug Fixes

* **splunk:** rotate managed MCP token safely ([#366](https://github.com/dryvist/ansible-splunk/issues/366)) ([6296b4a](https://github.com/dryvist/ansible-splunk/commit/6296b4a6ae8e61cc78b393ac342b25b9a222cc72))

## [0.42.0](https://github.com/dryvist/ansible-splunk/compare/v0.41.0...v0.42.0) (2026-07-21)


### Features

* **splunk:** add os_metrics metric index for host OS telemetry ([#363](https://github.com/dryvist/ansible-splunk/issues/363)) ([a3b311d](https://github.com/dryvist/ansible-splunk/commit/a3b311df9c1abdcd65c2c1235c2221a00cc00862))

## [0.41.0](https://github.com/dryvist/ansible-splunk/compare/v0.40.0...v0.41.0) (2026-07-20)


### Features

* **splunk_docker:** add dedicated hermes index ([#357](https://github.com/dryvist/ansible-splunk/issues/357)) ([8baf82a](https://github.com/dryvist/ansible-splunk/commit/8baf82a03ad50167ba02ecbf281ab62912f0f4e5))

## [0.40.0](https://github.com/dryvist/ansible-splunk/compare/v0.39.1...v0.40.0) (2026-07-19)


### Features

* **splunk_docker:** Hermes delivery SLO alert (INC-17088) ([#355](https://github.com/dryvist/ansible-splunk/issues/355)) ([7c30d37](https://github.com/dryvist/ansible-splunk/commit/7c30d372fcf5cb7aa9a91730661a28c57d6d7f20))

## [0.39.1](https://github.com/dryvist/ansible-splunk/compare/v0.39.0...v0.39.1) (2026-07-18)


### Bug Fixes

* **splunk_docker:** publish the Traefik-fronted MCP URL, not the raw mgmt endpoint ([#351](https://github.com/dryvist/ansible-splunk/issues/351)) ([ddbab68](https://github.com/dryvist/ansible-splunk/commit/ddbab6862f0d48c98bb272e95b285b2e3b74ebb9))

## [0.39.0](https://github.com/dryvist/ansible-splunk/compare/v0.38.0...v0.39.0) (2026-07-16)


### Features

* **scripts:** mint short-lived SSH certificates from the OpenBao CA in run-ansible.sh ([#349](https://github.com/dryvist/ansible-splunk/issues/349)) ([6a40a0a](https://github.com/dryvist/ansible-splunk/commit/6a40a0a912fe1abbcff8cc4c62a9ac850e7bec06))

## [0.38.0](https://github.com/dryvist/ansible-splunk/compare/v0.37.0...v0.38.0) (2026-07-16)


### Features

* **splunk:** enable Splunk MCP token publish to OpenBao ([#345](https://github.com/dryvist/ansible-splunk/issues/345)) ([9850503](https://github.com/dryvist/ansible-splunk/commit/9850503b7d5d0473d44405227dae92b353ba02ff))

## [0.37.0](https://github.com/dryvist/ansible-splunk/compare/v0.36.0...v0.37.0) (2026-07-16)


### Features

* **alerts:** ntfy + Slack delivery, repoint LLM router alerts at live data ([#342](https://github.com/dryvist/ansible-splunk/issues/342)) ([0f10cbb](https://github.com/dryvist/ansible-splunk/commit/0f10cbb784a882fd43709bdca4365f1c61acfbd5))

## [0.36.0](https://github.com/dryvist/ansible-splunk/compare/v0.35.0...v0.36.0) (2026-07-16)


### Features

* **splunk:** publish MCP credentials to OpenBao ([#341](https://github.com/dryvist/ansible-splunk/issues/341)) ([2550bbc](https://github.com/dryvist/ansible-splunk/commit/2550bbcd18e5e4ace7ce8f74a398b0f579f8e9ce))

## [0.35.0](https://github.com/dryvist/ansible-splunk/compare/v0.34.1...v0.35.0) (2026-07-13)


### Features

* use shared OpenBao inventory resolver ([#339](https://github.com/dryvist/ansible-splunk/issues/339)) ([90f54e5](https://github.com/dryvist/ansible-splunk/commit/90f54e52f3ca586822f7efe509a1d0c516430104))

## [0.34.1](https://github.com/dryvist/ansible-splunk/compare/v0.34.0...v0.34.1) (2026-07-10)


### Bug Fixes

* **splunk_docker:** return HTTP 202 for notifications/initialized ([#335](https://github.com/dryvist/ansible-splunk/issues/335)) ([3a65d1a](https://github.com/dryvist/ansible-splunk/commit/3a65d1a4b1df3e414c3df9feceed31f71a091057))

## [0.34.0](https://github.com/dryvist/ansible-splunk/compare/v0.33.0...v0.34.0) (2026-07-10)


### Features

* **splunk:** bench verdict-maturity + score-trend reports from mlx:bench feed ([#333](https://github.com/dryvist/ansible-splunk/issues/333)) ([23a3069](https://github.com/dryvist/ansible-splunk/commit/23a306977b152795f5ebcdf3aa1a58cb27d32a7a))

## [0.33.0](https://github.com/dryvist/ansible-splunk/compare/v0.32.0...v0.33.0) (2026-07-10)


### Features

* **splunk:** add TA Studio splunkbase app ([#331](https://github.com/dryvist/ansible-splunk/issues/331)) ([891ddae](https://github.com/dryvist/ansible-splunk/commit/891ddaebab78b26011fb0c92a634ac9e90dd5294))

## [0.32.0](https://github.com/dryvist/ansible-splunk/compare/v0.31.0...v0.32.0) (2026-07-10)


### Features

* **splunk:** night-cluster rank-error + idle-cluster saved searches ([5fedef0](https://github.com/dryvist/ansible-splunk/commit/5fedef0015664e8f9012209dab8efaaba46a4fd8))

## [0.31.0](https://github.com/dryvist/ansible-splunk/compare/v0.30.0...v0.31.0) (2026-07-10)


### Features

* **splunk:** add Traefik Splunkbase app ([#324](https://github.com/dryvist/ansible-splunk/issues/324)) ([df3ee3b](https://github.com/dryvist/ansible-splunk/commit/df3ee3bcb2a8a74a19b9530831a6c7f77ae8eb55))

## [0.30.0](https://github.com/dryvist/ansible-splunk/compare/v0.29.3...v0.30.0) (2026-07-09)


### Features

* **splunk:** serving memory-headroom + Metal ceiling alerts ([#326](https://github.com/dryvist/ansible-splunk/issues/326)) ([bafb66e](https://github.com/dryvist/ansible-splunk/commit/bafb66eae47feae5ea22d20f08ada9eb307874f4))

## [0.29.3](https://github.com/dryvist/ansible-splunk/compare/v0.29.2...v0.29.3) (2026-07-08)


### Bug Fixes

* **inventory:** repoint containers['object-storage'] lookups to renamed key 's3' ([#317](https://github.com/dryvist/ansible-splunk/issues/317)) ([d277c06](https://github.com/dryvist/ansible-splunk/commit/d277c06d573caea119ddb93d009eb0936c6610f3))

## [0.29.2](https://github.com/dryvist/ansible-splunk/compare/v0.29.1...v0.29.2) (2026-07-08)


### Bug Fixes

* **playbooks:** stop play vars_files clobbering group_vars overrides ([#312](https://github.com/dryvist/ansible-splunk/issues/312)) ([4ec0cd8](https://github.com/dryvist/ansible-splunk/commit/4ec0cd8e7a370126496ac6937921196c2aa878dd))

## [0.29.1](https://github.com/dryvist/ansible-splunk/compare/v0.29.0...v0.29.1) (2026-07-08)


### Bug Fixes

* **splunk:** mint MCP tokens via the app mcp_token endpoint (aud=mcp) ([#313](https://github.com/dryvist/ansible-splunk/issues/313)) ([4487d18](https://github.com/dryvist/ansible-splunk/commit/4487d183e6c69c78eb0e272c55dc5e225ddbd55a))

## [0.29.0](https://github.com/dryvist/ansible-splunk/compare/v0.28.1...v0.29.0) (2026-07-08)


### Features

* **splunk:** mint per-user auth tokens for MCP service accounts ([#309](https://github.com/dryvist/ansible-splunk/issues/309)) ([74f68cb](https://github.com/dryvist/ansible-splunk/commit/74f68cb35ed1856a9808fbd467397388fa7a4d69))

## [0.28.1](https://github.com/dryvist/ansible-splunk/compare/v0.28.0...v0.28.1) (2026-07-07)


### Bug Fixes

* **apps:** fail-soft guest-side add-on installs so config handlers still flush ([#308](https://github.com/dryvist/ansible-splunk/issues/308)) ([5935a27](https://github.com/dryvist/ansible-splunk/commit/5935a27faf223576e2e9aee95f19f3eb13aa8955))

## [0.28.0](https://github.com/dryvist/ansible-splunk/compare/v0.27.0...v0.28.0) (2026-07-07)


### Features

* **alerts:** add data-driven per-index silence detectors ([#304](https://github.com/dryvist/ansible-splunk/issues/304)) ([1991880](https://github.com/dryvist/ansible-splunk/commit/199188037aba5ecc3a2edb5d835b68d4b052978e))

## [0.27.0](https://github.com/dryvist/ansible-splunk/compare/v0.26.0...v0.27.0) (2026-07-07)


### Features

* **hec:** allow per-token extra target indexes via extra_hec_indexes ([#302](https://github.com/dryvist/ansible-splunk/issues/302)) ([3193361](https://github.com/dryvist/ansible-splunk/commit/31933615be8556425e47c803df864aa4d884f61a))

## [0.26.0](https://github.com/dryvist/ansible-splunk/compare/v0.25.0...v0.26.0) (2026-07-07)


### Features

* **indexes:** add monitoring-program indexes and dedupe unifi_metrics ([#301](https://github.com/dryvist/ansible-splunk/issues/301)) ([f2959a9](https://github.com/dryvist/ansible-splunk/commit/f2959a92151e2aeca9a61e073cbe311bcd0a7aae))

## [0.25.0](https://github.com/dryvist/ansible-splunk/compare/v0.24.1...v0.25.0) (2026-07-07)


### Features

* **splunk:** add Splunkbase 8278 registry entry ([#298](https://github.com/dryvist/ansible-splunk/issues/298)) ([3667421](https://github.com/dryvist/ansible-splunk/commit/3667421415fde94c55b6e8b8146fda6c5e6f41a5))

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

* **splunk:** repoint Splunkbase sync to object-storage (RustFS) ([#276](https://github.com/dryvist/ansible-splunk/issues/276)) ([b318baa](https://github.com/dryvist/ansible-splunk/commit/b318baa86045852065eade5c9bb823ad0d6616a0))

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

* **splunk:** object-storage add-on registry + Splunkbase auto-sync ([7364448](https://github.com/JacobPEvans/ansible-splunk/commit/736444891f658d374e85329b5fecb47cc5612a9d))

## [0.9.0](https://github.com/JacobPEvans/ansible-splunk/compare/v0.8.1...v0.9.0) (2026-04-09)

### Features

* add object-storage artifact store + propagate terraform_data to all hosts ([#124](https://github.com/JacobPEvans/ansible-splunk/issues/124)) ([804eb55](https://github.com/JacobPEvans/ansible-splunk/commit/804eb55dc49aeea7561db51375c5c9efae4f6d6e))
* add object-storage artifact store for custom add-on downloads ([#118](https://github.com/JacobPEvans/ansible-splunk/issues/118)) ([20a1efe](https://github.com/JacobPEvans/ansible-splunk/commit/20a1efeae4e451eb8fc132a460a1883ca42b8d12))

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
