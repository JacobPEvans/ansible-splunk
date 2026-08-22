# Splunk-native HA cluster design (Phase 3)

Replaces the single all-in-one Splunk VM (docker AIO, tofu VM `200`) with a
Splunk-native highly-available cluster. No storage-level replication — all
redundancy is Splunk's own bucket replication and distributed search.

VMs are declared in tofu-proxmox (`deployment.json`, generic `vms` map;
companion PR `feature/splunk-cluster-vms`). This repo converges them with the
vendored `splunk.splunk` role (v2.1.6).

## Topology (bare minimum)

| Host | tofu VMID | Node | Splunk role(s) | Inventory groups |
| --- | --- | --- | --- | --- |
| `splunk-idx-10` | `421100` | proxmox-1 | Indexer cluster peer | `full,indexer,splunk_idx` |
| `splunk-idx-40` | `421110` | proxmox-4 | Indexer cluster peer | `full,indexer,splunk_idx` |
| `splunk-sh-10` | `421120` | proxmox-1 | Independent search head | `full,search,splunk_sh` |
| `splunk-sh-40` | `421130` | proxmox-4 | Independent search head | `full,search,splunk_sh` |
| `splunk-mgmt-40` | `421140` | proxmox-4 | CM + license master + monitoring console + 3rd SH | `full,clustermanager,licensemaster,dmc,search,splunk_mgmt` |

One indexer + one search head per node across proxmox-1 and proxmox-4; the
management VM on proxmox-4. The remaining nodes are hands-off or unused (a
third node is not required at this size).

### Why this shape

- **Indexer cluster: 2 peers, RF=2 / SF=2.** This is the supported minimum: an
  indexer cluster needs at least *replication factor* peer nodes, and RF=2
  requires 2 peers (Splunk docs, *The basics of indexer cluster architecture* →
  "replication factor").
  It is functional but has **no failure headroom** — with exactly RF peers, one
  peer down means the cluster can no longer maintain the replication factor
  until it returns. The upgrade path is a third peer.
- **Search tier: 2 independent search heads, not a search head cluster.** A
  search head cluster requires a **minimum of 3 members** (Splunk, *System
  requirements and other deployment considerations for search head clusters*).
  Only 2 dedicated search heads are affordable, so they attach to the indexer
  cluster as standalone search heads (`configure_idxc_sh`) with no SHC, no
  deployer, and no search-artifact/config replication between them. Knowledge
  objects are managed per search head (or later via a deployer + app git).
- **One management VM carries every singleton control role.** Cluster manager,
  license master, monitoring console, plus a third unclustered search head. The
  cluster manager cannot be a peer node (Splunk, *The basics of indexer cluster
  architecture*),
  so it lives here, not on an indexer. Co-locating a search head on the manager
  is discouraged for large deployments but is an accepted homelab compromise;
  watch this VM's load.

## Ports

Sourced from the tofu `pipeline_constants` and the Splunk defaults; opened
cluster-internally by the existing splunk firewall security group for any guest
tagged `splunk` (tofu-proxmox `modules/firewall/security_groups.tf`) — **no
firewall change is needed for this cluster.**

| Port | Purpose |
| --- | --- |
| 8000 | Splunk Web |
| 8088 | HEC (ingest) |
| 8089 | splunkd management / REST (cluster control plane) |
| 9997 | S2S receiving (forwarders → indexers) |
| 9887 | Indexer-cluster bucket replication (`splunk_idxc_rep_port`) |
| 8080 | Cluster replication (server-to-server) |

## Inventory wiring

`inventory/load_tofu.yml` resolves the tofu-published inventory
(`TOFU_INVENTORY_PATH` → RustFS artifact) and adds the cluster hosts from
`tofu_data.vms`, grouping each by its role tag (`splunk-idx` / `splunk-sh` /
`splunk-mgmt`) into the `splunk.splunk` role's canonical groups plus a friendly
`splunk_idx` / `splunk_sh` / `splunk_mgmt` group and the shared `splunk_cluster`
group. The legacy AIO `splunk` host is added by the same playbook and is
untouched.

Cluster-wide vars live in `inventory/group_vars/splunk_cluster.yml`; per-role
license settings in `splunk_idx.yml` / `splunk_sh.yml` / `splunk_mgmt.yml`. All
secrets are read with `lookup('env', ...)` — injection-agnostic (no
Doppler/SOPS/OpenBao baked into the role).

## Converge

`playbooks/deploy-cluster.yml` runs the role once per tier, setting
`deployment_task` per play in the order the role documents:

1. `check_splunk.yml` on `splunk_cluster` — install Splunk Enterprise.
2. `configure_license.yml` on `licensemaster`.
3. `configure_idxc_manager.yml` on `clustermanager`.
4. `configure_idxc_member.yml` on `indexer` — peers join the cluster.
5. `configure_idxc_sh.yml` on `search` — search heads attach to the cluster.
6. `configure_dmc.yml` on `dmc` — monitoring console.

```bash
doppler run -- ansible-playbook -i inventory/hosts.yml playbooks/deploy-cluster.yml
```

Required env: `SPLUNK_PASSWORD`, `SPLUNK_PACKAGE_URL_FULL`,
`SPLUNK_IDXC_PASS4SYMMKEY`, `SPLUNK_GENERAL_PASS4SYMMKEY`, `PROXMOX_DOMAIN`,
`PROXMOX_SSH_KEY_PATH` (optional `SPLUNK_LICENSE_FILE`). The two pass4SymmKeys
are new shared secrets generated at the source; once set, rotating them requires
re-syncing the cluster.

## Data migration from the AIO (Splunk-native)

The AIO (VM `200`) is **disable-never-delete**. There is also a live-only,
stopped `splunk-aio-data-holder` (VM `8200`) outside IaC — do not delete it.

**Primary path (lowest risk, no bucket surgery):**

1. Stand the empty cluster up.
2. Repoint ingest: Cribl HEC output → the cluster HEC, load-balanced across the
   indexer peers via the existing `splunk-hec` Traefik route (repointing that
   route's backend from the AIO to the two indexers is a small tofu ingress
   change — tracked as a **follow-up**, not in the VM-declaration PR). New events
   land in the cluster.
3. Keep the AIO online as a **distributed search peer** added to the search
   heads (`splunk add search-server`), so historical data stays searchable
   across old and new with no data movement.
4. Let the AIO's data age out per retention. Once aged/empty, remove it as a
   search peer and stop the AIO (disable-never-delete).

**Alternative (immediate consolidation):** offline bucket copy — `splunk offline`
the AIO, copy its warm/cold buckets into a peer's `colddb`/`thaweddb`, restart,
and let the cluster manager rebalance. Higher risk (manual bucket/GUID
handling); only if historical data must physically live inside the cluster.

## Rollback

The cluster is purely additive and the AIO is never modified. Rollback =
repoint Cribl/HEC senders back to the AIO route and stop the cluster VMs. No
data loss.

## Residual risks / open questions

1. **2-peer RF=2 has zero failure headroom** — one peer down = RF not
   maintainable until it returns. Upgrade: add a third peer.
2. **2 independent SHs, no SHC** — no config/artifact sync between search heads;
   knowledge objects managed per-SH. Upgrade: a 3rd SH + SHC.
3. **Search head co-located on the cluster manager** — accepted homelab
   compromise; watch mgmt VM load.
4. **License** — a Splunk *Free* license cannot run indexer clustering,
   distributed search, or auth. An **Enterprise or developer license is
   required** on the license master. *Open: which license, and where is the
   file?*
5. **proxmox-4 not commissioned** — 3 of 5 VMs land there; it must be
   commissioned and powered on before the tofu apply (flagged in
   `deployment.json.example`).
6. **HEC/S2S cutover** — repointing the `splunk-hec` Traefik route and forwarder
   S2S targets to the indexer peers is a separate follow-up tofu change.

## References

- Companion tofu PR: `dryvist/tofu-proxmox` `feature/splunk-cluster-vms`.
- Vendored role: `splunk.splunk` v2.1.6 (`requirements.yml`), from
  [splunk/ansible-role-for-splunk](https://github.com/splunk/ansible-role-for-splunk).
- Storage tiers (fast-splunk/bulk-splunk) target the AIO module and are already
  merged in tofu develop; cluster indexers use generic `additional_disks`.
