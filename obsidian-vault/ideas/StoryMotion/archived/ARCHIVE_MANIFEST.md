---
title: "StoryMotion Archive Manifest"
status: active
tags:
  - StoryMotion
  - archive
  - provenance
  - status/active
created: 2026-07-12T12:35:00+0800
updated: 2026-08-10T15:00:00+08:00
---

# StoryMotion Archive Manifest

> [!abstract] Scope
> archive 中的内容用于历史追溯，不作为当前默认结论。当前入口见 [[StoryMotion/current]]，有效指标见 [[StoryMotion-valid-metric-ledger]]。

> [!info] Paper B archive
> DIRECT专属历史已迁移到[[DIRECT/archived/ARCHIVE_MANIFEST|DIRECT Archive Manifest]]，
> 本页不再拥有Actor–Director、HumanML3D fixed-Camera或co-design历史。

整理前完整快照：

`_private/backups/storymotion-ideas-pre-reorg-20260712.tar.zst`

## Archived From Root

| original filename | archived category | evidence status | reason |
| --- | --- | --- | --- |
| 2026-07-01_storymotion-v6.2-metric-data.md | metrics | partially valid | official-cache v6 rows保留；local-tokenizer rows受后续contract纠错影响 |
| 2026-07-01_storymotion-v7-stage2-architecture.md | superseded-design | superseded | 旧Stage2架构设计，当前roadmap替代 |
| 2026-07-02_storymotion-v7.2-stage2.md | superseded-design | superseded | 与archive既有同basename版本冲突，改名为active-draft |
| 2026-07-03_storymotion-v7.3.1.md | superseded-design | historical | 旧architecture与实验裁决 |
| 2026-07-06_storymotion-v7.4-causal-asymmetry.md | superseded-design | historical | topology假设仍可追溯，但当前被loss/geometry gate后置 |
| 2026-07-09_storymotion-v7.12-clean-data-and-human-reconstruction.md | invalidated | superseded | 混有旧feature/decode contract证据 |
| 2026-07-09_storymotion-v7.12-metric-data.md | invalidated | superseded ledger | 混有被否决local rows；有效行已进入canonical ledger |
| 2026-07-11_storymotion-v7.15-matched-stage2-results.md | invalidated | invalid | wrong owning decoder |
| 2026-07-11_storymotion-v7.16-stage2-forensic-audit.md | forensics | superseded forensic | 又被wrong causal cache发现二次修正；v7.17吸收最终结论 |
| ae_train_split.txt | artifacts | generated artifact | 非idea note，移出根目录 |

## Archived From Root: Evidence Reorganization

| original filename | archived path | evidence status | reason |
| --- | --- | --- | --- |
| 2026-07-11_storymotion-latest-roadmap.md | evidence/2026-07-11_storymotion-latest-roadmap.md | superseded evidence | priority absorbed by `current.md` |
| 2026-07-11_storymotion-v7.14-corrected-results.md | evidence/2026-07-11_storymotion-v7.14-corrected-results.md | retained evidence | pure corrected Stage1 evidence; no longer a separate version narrative |
| 2026-07-12_storymotion-stage1-stage2-loss-and-demanifold.md | evidence/2026-07-12_storymotion-stage1-stage2-loss-and-demanifold.md | retained evidence | loss diagnosis absorbed by `current.md` |
| 2026-07-12_storymotion-v7.17-decoder-cache-contract-execution.md | evidence/2026-07-12_storymotion-v7.17-decoder-cache-contract-execution.md | retained evidence | contract execution and matched diagnostic details |
| 2026-07-13_storymotion-plusplus-phase-adaptive-relational-guidance.md | proposals/2026-07-13_storymotion-plusplus-phase-adaptive-relational-guidance.md | archived proposal | superseded design exploration; not a current experiment queue |
| 2026-07-17_storymotion-stage1-length-condmdi-causal-priority.md | evidence/2026-07-17_storymotion-stage1-length-condmdi-causal-priority.md | retained evidence | length/CondMDI/causality forensic evidence moved out of current decision surface |
| 2026-07-17_storymotion-fixed300-offline-ar-motionstreamer-v746-deployment.md | operations/2026-07-17_storymotion-fixed300-offline-ar-motionstreamer-v746-deployment.md | archived operation | closed deployment snapshot; live status moved to run artifacts, version, and history |
| sft-data-prepare.md | superseded-design/2026-07-22_storymotion-sft-data-prepare-premerge.md | superseded design | 质量维度、分档结果、nested pools 与训练分配已合并到 canonical v8.2333 curation contract |
| current.md v8 pre-v9 snapshot | progress/2026-07-25_storymotion-current_v8_pre-v9-external-long-eval.md | superseded decision surface | v9 保留 v8 mainline core，并由三个 105K external/matched eval 更新当前 claim boundary |
| 2026-07-24_storymotion-external-system-backbone-adaptation-plan.md | experiments/2026-07-25_storymotion-v9-external-system-backbone-adaptation-closed.md | closed preregistration | E1/E2/E3 long eval 已闭合；interface、observability 与 stop/continue contract 保留，live conclusion 归 `current.md` |

## Current Canonical Notes

- [[StoryMotion/current]]
- [[version_family]]
- [[paper-boundary]]
- [[StoryMotion-iclr-reliability]]
- [[StoryMotion-valid-metric-ledger]]
- [[StoryMotion-metric-computation-io]]
- [[Storymotion-exp-sha]]
- [[StoryMotion_Gradio_Render]]

## 2026-08-10 metric-ledger evidence split

| source | archived path | evidence status | reason |
| --- | --- | --- | --- |
| pre-v9 formal ledger | `metrics/2026-07-24_StoryMotion-valid-metric-ledger_pre-human-first-orthogonalization.md` | immutable pre-v9 numeric owner | StoryMotion active ledger starts from the v9 owner |
| ordinary non-full generation rows | `metrics/2026-08-10_StoryMotion-valid-metric-ledger_pre-v9-and-nonfull.md` | provenance index only | first-512/N512 and intermediate generation screens no longer participate in active ranking; allowed special diagnostics remain explicitly labeled |

## 2026-08-03 Paper A root-surface cleanup

| original root note | archived path | evidence status | reason |
| --- | --- | --- | --- |
| 2026-07-17 v8.2333 data curation | `data/` | retained historical contract | 未授权训练；不再占用Paper A live surface |
| 2026-07-18 generatability ladder | `diagnostics/` | closed diagnostic | 结论已被current／ledger吸收 |
| 2026-07-25 dual-expert design | `superseded-design/` | superseded | joint-parallel与DC3D不属于当前Paper A |
| 2026-07-27 Stage1 H-anchor control | `invalidated/` | invalid for Stage2 | HumanML3D rot6D伪观测边界已关闭 |
| 2026-07-28 v9 Camera diagnosis | `diagnostics/` | retained provenance | v11已替代其live执行状态 |
| 2026-07-29 runtime plan | `operations/` | retained implementation history | 长期执行合同已由代码仓库文档接管 |
| 2026-07-29 v10 contract | `versions/v10/` | closed by scope | 不再执行 |
| 2026-07-29 v11 rescue contract | `versions/v11/` | completed | 正式结果已进入ledger，版本事件已进入version family |
| 2026-07-31 Camera／framing／Human locality controls | `experiments/` | stopped／closed／future work | 不进入当前投稿queue |
| 2026-08-02 two-paper positioning | restored as `../paper-boundary.md` | active canonical | 完整双论文定义与两张内嵌SVG恢复到一级长期owner |
| 2026-08-03 condensed paper boundary | `paper-scope/2026-08-03_paper-boundary-condensed-superseded.md` | superseded condensed | 精简替代页保留；不得取代完整图文owner |
| StoryMotion Checkmate | `diagnostics/` | stale-mainline snapshot | 仍以C3为current，不再是长期owner |
| blackboard | `progress/` | working-note archive | 只保留历史问题与接力记录 |
| pre-refactor ICLR reliability | `paper-scope/` | retained full snapshot | 拆分前附录不再混入Paper A live closure |

## Interpretation Rule

Archive note中的数字仅在其原始contract范围内保留。若与canonical ledger冲突，以canonical ledger、owning-decoder JSON、cache hash和explicit checkpoint结果为准。
