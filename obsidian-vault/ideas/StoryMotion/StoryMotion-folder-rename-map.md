---
title: "StoryMotion folder rename mapping (4090 pre-rename)"
status: migration-in-progress
hypothesis: |
  A deterministic legacy-to-sm namespace migration can simplify the StoryMotion
  workspace while old run IDs, paths, manifests, artifacts, and hashes remain
  recoverable. This note is the single pre-rename mapping owner.
tags:
  - StoryMotion
  - provenance
  - rename
  - status/draft
aliases:
  - StoryMotion-folder-rename-map
source_notes:
  - "[[StoryMotion-valid-metric-ledger]]"
  - "[[StoryMotion/current]]"
created: 2026-08-10T16:48:00+08:00
updated: 2026-08-10T17:52:00+08:00
rename_executed: partial
source_namespace_rename_executed: true
historical_artifact_rename_executed: false
host_4090_status: source-renamed-artifacts-held
host_5090_status: symmetric-source-synced-other-source-renames-pending
---

# StoryMotion folder rename mapping

> [!warning] Pre-rename canonical record
> 本页已先于任何远端 rename 存在。当前记录 4090 的只读清点和已授权的
> `paperA_* → sm_*` folder/ID 映射。4090的Git-managed source namespace已在两个受审计
> commit中改名；历史artifact未改名。5090已同步本轮symmetric control source，其他source
> namespace仍待同commit同步。
> 本页是旧前缀唯一允许保留的Markdown owner；它不替代
> `experiment_contract.json`、`manifest.json` 或result/records中的provenance。

## Scope and naming rule

The proposed display/path rule is deterministic:

```text
paperA_<suffix>       → sm_<suffix>
stage1_paperA_<suffix> → stage1_sm_<suffix>
stage2_paperA_<suffix> → stage2_sm_<suffix>
```

The `sm_` target is the canonical StoryMotion namespace for new runs and regular
Markdown. The user authorized a one-time rename, but the read-only inventory
invalidated the assumption that all affected folders are few: 4090 contains
three source experiment namespaces and roughly 145 generated/history folders.
Therefore the small Git-managed source rename may proceed, while historical
artifacts remain held until an allowlisted migration can preserve every old
path, embedded run ID and content hash in this note and a machine-readable
migration manifest.

## 4090 inventory captured before rename

| field | value |
| --- | --- |
| host | `4090` (`172.23.148.106`, SSH alias) |
| repository root | `/data/public/ripemangobox/Motion/StoryMotion` |
| repository HEAD | `cf5cb278cae6630088df2c939a0ee5f596c3eef0` |
| matching directories | `149` total: `145` under `runs/`, `3` under `experiments/`, `1` worktree |
| sorted matching-directory inventory SHA-256 | `23abefa46d07937abf8166e74d0da01f38db716a47afb2d327395ba53081149b` |
| remote rename executed | `false` |
| remote scan writes | none intended; this note records only the read-only inventory |

The inventory was based on directory basenames matching `*paperA_*`. The
family counts below include the umbrella directory where present and the one
hidden preparation directory under the Camera-recaption artifact namespace.
They cover all `149` matching directories without expanding every record file.

## Old → new path-family mapping

The `new path` column is the canonical `sm_` target. `preserve ID` means that a
regular note uses the mapped alias while the old embedded `run_id` and content
hashes stay recoverable here until that physical artifact family is migrated.

| old path family on 4090 | planned new path family | object type | matching dirs | host | reference/manifest update scope | status |
| --- | --- | --- | ---: | --- | --- | --- |
| `experiments/paperA_camera_recaption` | `experiments/sm_camera_recaption` | source experiment namespace | 1 | 4090 | imports, scripts, contracts that point to this source namespace | completed in `0cf5f91` |
| `experiments/stage1_paperA_representation_controls` | `experiments/stage1_sm_representation_controls` | source experiment namespace | 1 | 4090 | imports, scripts, Stage1 control contracts | completed in `0cf5f91` |
| `experiments/stage2_paperA_c1rel` | `experiments/stage2_sm_c1rel` | source experiment namespace | 1 | 4090 | imports, scripts, Stage2 control contracts | completed in `0cf5f91` |
| `experiments/stage2_paperA_true_p2` | `experiments/stage2_sm_symmetric_route_controls` | independent-worktree source namespace | — | 4090 + 5090 | imports, contract/preflight/evaluator code and tests | outside the 149-dir root inventory; completed in `350777b`, route fixes through `47b29fa` |
| `.git/worktrees/paperA_true_p2_20260809` | `.git/worktrees/sm_true_p2_20260809` | Git worktree metadata | 1 | 4090 | `.git/worktrees/*`, worktree `gitdir`/`commondir`; do not hand-rename | hold; Git-managed |
| `runs/artifacts/paperA_camera_recaption` and children `paperA_*` | `runs/artifacts/sm_camera_recaption` and children `sm_*` | generated artifact namespace | 45 | 4090 | artifact manifests, `path`/`run_root` fields, ledger hash references | preserve immutable artifacts |
| `runs/artifacts/paperA_representation_controls` and children `paperA_*` | `runs/artifacts/sm_representation_controls` and children `sm_*` | generated artifact namespace | 4 | 4090 | paired-audit manifests and ledger hash references | preserve immutable artifacts |
| `runs/legacy/train/stage1/paperA_*` | `runs/legacy/train/stage1/sm_*` | legacy Stage1 run roots | 15 | 4090 | contracts, manifests, checkpoint/decoder/cache paths | preserve exact run IDs |
| `runs/legacy/train/stage2/paperA_*` | `runs/legacy/train/stage2/sm_*` | legacy Stage2 run roots | 16 | 4090 | contracts, manifests, checkpoint/cache/evaluator paths | preserve exact run IDs |
| `runs/legacy/train/eval/stage2/paperA_*` | `runs/legacy/train/eval/stage2/sm_*` | legacy misplaced eval root | 1 | 4090 | evaluation contract/result/records paths | preserve exact run ID |
| `runs/legacy/eval/stage1/paperA_*` | `runs/legacy/eval/stage1/sm_*` | legacy Stage1 eval roots | 15 | 4090 | evaluation contracts, result/records paths | preserve exact run IDs |
| `runs/legacy/eval/stage2/paperA_*` | `runs/legacy/eval/stage2/sm_*` | legacy Stage2 eval roots | 19 | 4090 | evaluation contracts, result/records/manifest paths | preserve exact run IDs |
| `runs/legacy/vis/stage1/paperA_*` | `runs/legacy/vis/stage1/sm_*` | legacy visualization roots | 5 | 4090 | render manifests and source run references | preserve exact run IDs |
| `runs/vis/stage1/paperA_*` | `runs/vis/stage1/sm_*` | visualization roots | 10 | 4090 | render manifests and source run references | preserve exact run IDs |
| `runs/vis/stage2/paperA_*` | `runs/vis/stage2/sm_*` | visualization roots | 15 | 4090 | render manifests and source run references | preserve exact run IDs |

The family rows sum to `149`. The planned `sm_*` spelling is therefore an
explicit old→new mapping, not permission to apply a glob rename. In particular,
the 145 `runs/` directories are historical evidence and must not be silently
renamed merely to make Markdown shorter.

## Known exact ID mappings

These are the exact Paper-A-prefixed IDs already present in the active ledger or
StoryMotion notes. They illustrate the deterministic target spelling; all other
matching basenames are covered by the path-family rule above.

| old immutable ID | planned `sm_` display/path ID | object type | host/status |
| --- | --- | --- | --- |
| `paperA_v11_c0_lat_30to105k_seed23_4090g0_r2_20260803` | `sm_v11_c0_lat_30to105k_seed23_4090g0_r2_20260803` | Stage2 run | 4090; preserve old ID |
| `paperA_v11_c0_geo_30to105k_seed23_4090g1_r2_20260803` | `sm_v11_c0_geo_30to105k_seed23_4090g1_r2_20260803` | Stage2 run | 4090; preserve old ID |
| `paperA_c1rel_lat_h105k_c105k_seed23_4090g0_20260809` | `sm_c1rel_lat_h105k_c105k_seed23_4090g0_20260809` | Stage2 run | 4090; preserve old ID |
| `paperA_c1rel_noi16_lat_h105k_c105k_seed23_4090g0_20260810` | `sm_c1rel_noi16_lat_h105k_c105k_seed23_4090g0_20260810` | Stage2 run | 4090; preserve old ID |
| `paperA_c1rel_rawt0_lat_h105k_c105k_seed17_4090g0_20260804` | `sm_c1rel_rawt0_lat_h105k_c105k_seed17_4090g0_20260804` | Stage2 run | 4090; preserve old ID |
| `paperA_c1rel_nointeraction16_rawt0_lat_h105k_c105k_seed17_4090g1_20260806` | `sm_c1rel_nointeraction16_rawt0_lat_h105k_c105k_seed17_4090g1_20260806` | Stage2 run | 4090; preserve old ID |
| `paperA_c1rel_stage1_636k_seed17_4090g1_r2_20260803` | `sm_c1rel_stage1_636k_seed17_4090g1_r2_20260803` | Stage1 run | 4090; preserve old ID |
| `paperA_hrel_nointeraction16_stage1_636k_seed17_4090g0_r2_20260803` | `sm_hrel_nointeraction16_stage1_636k_seed17_4090g0_r2_20260803` | Stage1 run | 4090; preserve old ID |
| `paperA_p1_hrel_matched_lat_h105k_c105k_seed17_4090g1_20260809` | `sm_p1_hrel_matched_lat_h105k_c105k_seed17_4090g1_20260809` | Stage2 run | 4090; preserve old ID |
| `paperA_p2_1_matched_symmetric_joint_h105k_c105k_seed17_4090g0_20260808` | `sm_p2_1_matched_symmetric_joint_h105k_c105k_seed17_4090g0_20260808` | invalid historical Stage2 run | 4090; preserve invalid provenance |
| `paperA_p2_matched_symmetric_joint_fresh_h105k_joint105k_seed17_4090g1_20260809` | `sm_p2_matched_symmetric_joint_fresh_h105k_joint105k_seed17_4090g1_20260809` | formal Stage2 run | 4090; preserve old ID |
| `paperA_pulpmotion_repro162760_stage2_original_matched210k_seed17_5090g3_r2_20260809` | `sm_pulpmotion_repro162760_stage2_original_matched210k_seed17_5090g3_r2_20260809` | native Stage2 baseline | 4090 path inventory; preserve native provenance |
| `paperA_ht_condition_attribution_pure4053_20260810_r2` | `sm_ht_condition_attribution_pure4053_20260810_r2` | attribution eval namespace | 4090; preserve result/records hashes |
| `paperA_independent_conditional_camera64_stage1_210k_seed17_4090g1_20260803` | `sm_independent_conditional_camera64_stage1_210k_seed17_4090g1_20260803` | Stage1 diagnostic | 4090; preserve diagnostic status |
| `paperA_fully_separate_native_lat_h105k_c105k_seed17_4090g0_r2_20260803` | `sm_fully_separate_native_lat_h105k_c105k_seed17_4090g0_r2_20260803` | Stage2 diagnostic | 4090; preserve historical status |

The `5090` token embedded in the native baseline ID is an experiment-host
provenance field, not evidence that this 4090 inventory scanned host 5090.

## Local vault reference inventory

The pre-migration read-only search covered `obsidian-vault/ideas/StoryMotion/`
and `obsidian-vault/ideas/DIRECT/`: 20 Markdown files and 41 unique legacy
tokens. The sorted path, token, and matching-line fingerprints were:

```text
paths: 07fefbfb1972915304611a7fe15ef9a82b89ac1c463b25b1aafce60cb33267e1
tokens: 859d8a6d877f20bbf06c314eff83dfed5d8ad08279153d3b2b20b4b118fc158b
lines:  5629373490a45859f9e9cb9a70c707120e8d7dde64cc232f73ef45582f5419f0
```

Those fingerprints intentionally describe the pre-migration state. Regular
StoryMotion/DIRECT Markdown has since moved to the `sm_` aliases by a one-time
allowlisted replacement; only this map retains the old spelling. The affected
files were grouped by update priority:

- canonical active owners: [[StoryMotion/current]],
  [[StoryMotion-valid-metric-ledger]],
  [[StoryMotion/version_family]], [[StoryMotion-iclr-reliability]],
  and [[DIRECT/current]];
- durable contracts and implementation maps:
  [[StoryMotion/paper-boundary]], [[StoryMotion/Pulp-camera-recaption-contract]],
  [[StoryMotion-codebase-deconstruction]], and
  [[StoryMotion_Gradio_Render]];
- archived or historical context: [[StoryMotion/archived/ARCHIVE_MANIFEST]],
  [[StoryMotion/archived/paper-scope/2026-08-03_paper-boundary-condensed-superseded]],
  [[StoryMotion/archived/paper-scope/2026-08-03_storymotion-iclr-reliability-pre-closure-refactor]],
  [[StoryMotion/dont_read/0805-0017]], [[StoryMotion/dont_read/0805-0137]],
  [[StoryMotion/dont_read/0805-2009]], [[StoryMotion/dont_read/0805-2334]],
  [[StoryMotion/dont_read/0806-1551]], [[StoryMotion/dont_read/blackboard]],
  [[StoryMotion/prompts/0803-1647]], and [[StoryMotion/prompts/0803-2024]].

The full vault search found 32 matching Markdown files; 12 files outside the
StoryMotion/DIRECT scope contain unrelated historical “Paper A” wording and are
not part of this mapping.

## Reference, manifest, and hash strategy for a future migration

1. Freeze the sorted old/new path inventory and record its SHA-256 before any
   move. Record the host, repository HEAD, migration tool version, and an
   append-only migration manifest.
2. For every affected run, verify the existing contract-declared hashes before
   moving: `experiment_contract.json`, `manifest.json`, checkpoint, owning
   decoder, train/eval cache, normalization source, result, records, fixed
   samples, and render manifests when present. Directory names are not identity.
3. If a folder-only move is approved, update only explicit path fields and
   allowlisted source imports. Keep `run_id`, `version / run`, split, sample
   IDs, checkpoint/cache/decoder hashes, result hashes, and historical status
   unchanged. Do not rewrite the ledger's immutable exact IDs.
4. After the move, rehash the same content and rerun contract/eval/doc audits.
   Require old-path → new-path entries and a successful old/new content-hash
   comparison before marking a row migrated.
5. Apply the same map to 5090 only after its own read-only inventory and hash
   comparison. Host 5090 is `pending_sync`; this note authorizes neither SSH
   writes nor a cross-host copy.

## Current decision

- 4090 source experiment namespaces: renamed and tested. The symmetric package
  is on `agent/symmetric-route-controls-20260810` at `47b29fa`; the other three
  namespaces are on `agent/sm-namespace-migration-20260810` at `0cf5f91`.
- 4090 historical run/eval/vis/artifact folders: held after inventory showed the
  scope is about 145 directories, not a small manual rename. No destructive or
  hash-breaking bulk move is authorized by this note.
- 5090: the symmetric source commit `47b29fa` is synchronized through an
  auditable Git bundle into SSD worktree
  `/home/ripemangobox/StoryMotion_worktrees/sm_symmetric_route_controls_20260810`;
  commit `0cf5f91` remains pending. Historical artifact paths are not inferred
  from 4090.
- Regular Markdown: migrated to `sm_`; old IDs remain only in this map.
