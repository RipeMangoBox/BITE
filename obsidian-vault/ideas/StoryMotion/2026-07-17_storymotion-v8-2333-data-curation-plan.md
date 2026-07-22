---
title: "StoryMotion v8.2333 Data Curation Contract"
status: automatic_screen_complete_candidate_only
hypothesis: |
  在冻结 C3-25 representation、owning decoder 与 Unified Stage2 实现后，
  只改变可逆、task-aware 的训练资格记录，可以检验物理异常与 Human
  caption-motion 错配是否损害生成；Camera 语义质量必须作为独立未解决轴。
tags:
  - StoryMotion
  - data-curation
  - stage2
  - status/active
aliases:
  - StoryMotion-v8.2333-Curation-Plan
source_notes:
  - "[[current]]"
  - "[[sft-data-prepare]]"
created: 2026-07-17T17:35:00+08:00
updated: 2026-07-22T14:30:00+08:00
---

# StoryMotion v8.2333 Data Curation Contract

> [!abstract] 当前裁决
> raw lock、Physical-v2、Human TMR-v4 与 loose/proposed/strict threshold grid 已闭合。当前输出仍是 `candidate_only`：`manual_labels=0`、threshold 未冻结、quarantine=`0`、正式 clean manifest 未生成、训练未授权。C3-25 是固定 representation owner；数据清洗不能与 Stage1、backbone 或 sampler 改动合并归因。

## 1. 数据单位

| 单位 | 数量 | 精确定义 |
| --- | ---: | --- |
| joint motion record | 162,760 | 一个同步的 Human motion、Camera trajectory 与文本文件的 clip；这是联合样本基数 |
| Human role row | 162,760 | `(motion_id, human, caption_index)` 的 Human caption-target 记录 |
| Camera role row | 163,384 | `(motion_id, camera, caption_index)` 的 Camera caption-trajectory 记录；107 个文件含多 caption |
| role-aware rows | 326,144 | 两种 role rows 之和；只用于文本 lineage 审计，不是 326,144 个 `<camera, motion>` 联合样本 |

raw artifact SHA256 为 `49d53029c42ad6ee275172fd9d3e5d56e98f1142ae9daf5dcc0988faa2a9c458`；ordered motion IDs SHA256 为 `a0981b6c…2c51dc9`；ordered role-row IDs SHA256 为 `182839ab…bbb8eb4`。

## 2. 已验证证据

| 证据 | 有效范围 | 状态 |
| --- | --- | --- |
| Physical-v2 | 162,760 joint records；Human 与 Camera dynamics | complete；SHA256 `ffd3f663…09b76` |
| Human TMR-v4 | 162,760 Human role rows；microbatch 1，replay 差值 0 | complete；SHA256 `766e4522…a4b0` |
| Camera semantic | Camera caption ↔ trajectory | unresolved；没有 verified scorer |
| LaMP | Human fine-grained alignment | unresolved；缺 verified code/checkpoint |

Physical 当前可用项包括 root/yaw/joint/bone/foot 与 Camera center/rotation dynamics。declared contact、calibrated ground、mesh 和 environment 输入不可得，保持 disabled，不能把“未计算”记为通过。

## 3. Threshold screen

Physical 只有在 length mismatch、bone extreme，或至少两个 dynamics family 同时进入 tail 且一个进入 extreme 时命中。TMR 要求分层内 cosine 进入低 tail 且 latent L2 进入高 tail。

| 分支 | 档位 | candidate | 保留量 |
| --- | --- | ---: | ---: |
| Physical | loose `p99 / p99.9` | 427 joint motions | 162,333 joint motions；325,290 role rows |
| Physical | proposed `p99.5 / p99.9` | 362 joint motions | 162,398 joint motions；325,420 role rows |
| Physical | strict `p99.9 / p99.95` | 128 joint motions | 162,632 joint motions；325,888 role rows |
| Human TMR | loose `p99` | 991 Human rows | 161,769 Human rows |
| Human TMR | proposed `p99.5` | 450 Human rows | 162,310 Human rows |
| Human TMR | strict `p99.9` | 87 Human rows | 162,673 Human rows |

| Physical | TMR | 异常交集 | 异常并集 | Human 保留 | role rows 保留 |
| --- | --- | ---: | ---: | ---: | ---: |
| loose | loose | 1 | 1,417 | 161,343 | 324,300 |
| loose | proposed | 0 | 877 | 161,883 | 324,840 |
| loose | strict | 0 | 514 | 162,246 | 325,203 |
| proposed | loose | 1 | 1,352 | 161,408 | 324,430 |
| proposed | proposed | 0 | 812 | 161,948 | 324,970 |
| proposed | strict | 0 | 449 | 162,311 | 325,333 |
| strict | loose | 1 | 1,118 | 161,642 | 324,898 |
| strict | proposed | 0 | 578 | 162,182 | 325,438 |
| strict | strict | 0 | 215 | 162,545 | 325,801 |

Physical 与 TMR 几乎不重叠，说明它们捕捉互补问题。clean 候选应排除异常并集；只删除异常交集会漏掉几乎所有候选。proposed/proposed 只是 operating-point candidate，不是正式阈值。

## 4. Task-aware 施加规则

| Stage2 task | 自动资格条件 | proposed 档预期基数 |
| --- | --- | ---: |
| Direct-H | Physical pass 且 Human TMR pass | 161,948 joint clips |
| Direct-C | Physical pass；Human-caption TMR 不适用 | 162,398 joint clips |
| joint | Physical pass 且 Human TMR pass；Camera semantic unresolved | 161,948 joint clips |

Physical 是 clip-level 证据，命中后关闭三任务资格。Human TMR 是 Human caption-motion 证据，只关闭 Direct-H 与 joint 的该 Human condition，不能误删 Direct-C。Camera 多 caption 只增加 condition rows，不增加 joint motion 基数。

candidate manifest 必须保留 raw parent hash、motion order、role pair IDs、reason codes、三任务 eligibility 与 `camera_semantic_status=unresolved_no_verified_scorer`；不得命名为 quarantine 或 clean。

## 5. 未解决问题

- Camera caption ↔ trajectory 没有 verified semantic scorer。
- LaMP 不可用；TMR 只能产生 Human semantic candidate。
- proposed threshold 未经 matched training ablation，不能冻结。
- `capture_source_proxy` 使用年份代理，仍需检查 source/年份偏差。
- 1 条 Human/Camera valid-length mismatch，最大差 13 帧。
- contact/ground/mesh/environment 规则缺输入。
- 8K/16K/32K/64K 子集缺 Camera semantic、rarity、complexity 与 coverage features。

本阶段不做人工标记。未来若引入人工，必须另行授权，不回写本轮 automatic-only contract。

## 6. 下一 gate

1. 物化 proposed/proposed 的 task-aware `candidate_only` eligibility。
2. 建立 Camera semantic 与 coverage features，再做 Pareto + stratified nested subset。
3. 固定 C3-25 做 raw continuation、random-size control 与 task-aware SFT。
4. 只有 matched ablation 支持后，才冻结 threshold 并生成可逆 quarantine/clean manifest。

SFT 合同见 [[sft-data-prepare]]。HumanML3D 属于数据增广轴，不属于本清洗合同。

## 7. Artifact registry

- evidence root：`runs/data_curation/storymotion_v8_2333_data_curation_20260717/`
- threshold screen：`threshold_screens/roleaware_grid_v1_20260722/`
- threshold contract SHA256：`e8cd8afc868d2c8e7395b650cb9b9d443615fd7be8feab131a755ba455a0b2e9`
- summary SHA256：`93693ca866be852de37bbcc8345f27ea9755994b19480d892b7a6c8ee2cf18b8`
- artifact manifest SHA256：`93f059e12bc20c7493ad879edf7c004a41b1fc627ea8e0de6afd20c10ecefc90`
- current state：raw locked；candidate screens complete；quarantine 0；formal clean 0


## 已实现：task-aware SFT candidate v1（2026-07-22）

> [!important] 计数单位更正
> `326,144` 不是 `<camera trajectory, human motion>` joint pair 数。原始联合数据只有 `162,760` 个 motion/clip records；`326,144 = 162,760 Human role rows + 163,384 Camera role rows`，计数单位是 `(motion_id, caption_role, caption_index)` 文本目标行。Camera 比 motion 多 `624` 行，是因为 `107` 个 Camera caption 文件含多 caption。joint 训练的基础单位仍约 `16.3 万` 个 motion；多 caption 展开后的 Human×Camera condition combinations 需另行报告。

已生成 candidate-only、不可直接训练的 task-aware manifest：

| 项目 | 数量 |
| --- | ---: |
| raw joint motions | 162,760 |
| raw Human role rows | 162,760 |
| raw Camera role rows | 163,384 |
| proposed Physical candidates | 362 motions |
| proposed TMR candidates | 450 Human rows |
| eligible Direct-H motions/rows | 161,948 |
| eligible Direct-C motions | 162,398 |
| eligible Direct-C Camera-condition rows | 163,022 |
| eligible joint motions | 161,948 |
| eligible joint Human×Camera combinations | 162,560 |
| retained role rows（audit only） | 324,970 |
| manual labels | 0 |

任务门控保持分离：

- Direct-H 排除 proposed Physical 与 Human-TMR candidates。
- Direct-C 不因 Human-TMR 低分删除 Camera target；当前只排除 proposed Physical candidates。
- joint 同时要求 Human target 与 observed-H condition 合格，因此取两类候选的 motion-level 并集。
- `retained role rows` 只用于审计，不得再次称为 joint pair 或训练样本数。
- Camera semantic scorer、LaMP、最终阈值与 coverage gate 尚未闭合，因此 `training_authorized=false`。

产物：

- `runs/data_curation/storymotion_v8_2333_data_curation_20260717/sft_candidates/task_aware_sft_candidate_v1_20260722/`
- raw manifest SHA256：`49d53029c42ad6ee275172fd9d3e5d56e98f1142ae9daf5dcc0988faa2a9c458`
- Physical candidates SHA256：`a2c31b4890f64d22e91df0247f648ce02e1500f97006828995cf9b8653194ef5`
- TMR candidates SHA256：`ae7f03242943970f5359978fe0a93a5187dcd6d6d90097634e6f3e4bc961c4c6`
- `eligibility.jsonl` SHA256：`9de1264495ec70a36efdc4e9628e45cbe5bd6eb42a77b3a05084c8b4d1ac853f`
- `direct_h.jsonl` SHA256：`ac855a7228efc49724c1efe98209ab09429879874957c1261ad987bda563f375`
- `direct_c.jsonl` SHA256：`bcf89f9a6528dad7615ce9808ce2a86e63e9f990635cc196ed2e3ec15edf80cb`
- `joint.jsonl` SHA256：`cce4f29392c0d9caf13e8dcfd67b5d3bb6ee8093ae7341177a877b0c604fcce1`
