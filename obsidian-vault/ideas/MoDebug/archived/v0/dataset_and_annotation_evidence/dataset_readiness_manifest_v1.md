---
title: "MoDebug P0 Dataset Readiness Manifest v1"
created: 2026-04-23T01:35
updated: 2026-04-26T02:31
status: archived
tags:
  - Motion_Generation
  - MoDebug
  - p0
  - dataset
related_exec:
  - '[[paperIDEAs/MoDebug/2026-04-22_modebug-exec-plan-alignment-first|MoDebug Exec]]'
---

# MoDebug P0 Dataset Readiness Manifest v1

## HumanML3D Family

- quant audit:
  - script: `scripts/modebug_audit_humanml3d_family.py`
  - json artifact: `paperIDEAs/MoDebug/humanml3d_family_audit_v1.json`

### HumanML3D

- status: `ready`
- evidence:
  - `[[linkedCodebases/datasets/HumanML3D/HumanML3D/texts]]`
  - `[[linkedCodebases/datasets/HumanML3D/HumanML3D/new_joint_vecs]]`
  - `[[linkedCodebases/datasets/HumanML3D/HumanML3D/new_joints]]`
- audit:
  - train: `23384` samples, frame mean / p50 / p90 = `140.84 / 149 / 199`, event coverage `22326 / 23384 = 95.48%`
  - val: `1460` samples, frame mean / p50 / p90 = `141.77 / 153 / 199`, event coverage `1400 / 1460 = 95.89%`
  - test: `4384` samples, frame mean / p50 / p90 = `140.74 / 148 / 199`, event coverage `4196 / 4384 = 95.71%`

### HumanML3D-E

- status: `ready`
- evidence:
  - `[[linkedCodebases/datasets/HumanML3D-E/data_train.npy]]`
  - `[[linkedCodebases/datasets/HumanML3D-E/data_val.npy]]`
  - `[[linkedCodebases/datasets/HumanML3D-E/data_test.npy]]`
  - event annotations:
    - `[[linkedCodebases/datasets/HumanML3D-E/.tamr_hml3de_gt_events_train.json]]`
    - `[[linkedCodebases/datasets/HumanML3D-E/.tamr_hml3de_gt_events_test.json]]`
    - `[[linkedCodebases/datasets/HumanML3D-E/.tamr_hml3de_gt_events_val.json]]`
- audit:
  - train: `24546` samples, frame mean / p50 / p90 = `142.75 / 150 / 199`, packaged event coverage `100%`
  - val: `1530` samples, frame mean / p50 / p90 = `144.94 / 158 / 199`, packaged event coverage `100%`
  - test: `4646` samples, frame mean / p50 / p90 = `143.13 / 150 / 199`, packaged event coverage `100%`

### HumanML3D-E-MP

- status: `ready`
- evidence:
  - `[[linkedCodebases/datasets/HumanML3D-E-MP/manifest.jsonl]]`
  - `[[linkedCodebases/datasets/HumanML3D-E-MP/captions.jsonl]]`
  - `[[linkedCodebases/datasets/HumanML3D-E-MP/train.txt]]`
  - `[[linkedCodebases/datasets/HumanML3D-E-MP/val.txt]]`
  - `[[linkedCodebases/datasets/HumanML3D-E-MP/test.txt]]`
  - `[[linkedCodebases/datasets/HumanML3D-E-MP/motion_formats/guo263]]`
  - `[[linkedCodebases/datasets/HumanML3D-E-MP/motion_format_stats]]`
- audit:
  - train: `24546` samples, frame mean / p50 / p90 = `142.75 / 150 / 199`, `num_decomposed_events > 0` coverage `100%`
  - val: `1530` samples, frame mean / p50 / p90 = `144.94 / 158 / 199`, `num_decomposed_events > 0` coverage `100%`
  - test: `4646` samples, frame mean / p50 / p90 = `143.13 / 150 / 199`, `num_decomposed_events > 0` coverage `100%`

### 272-dim-HumanML3D

- status: `partial`
- evidence:
  - `[[linkedCodebases/datasets/272-dim-HumanML3D/split]]`
  - `[[linkedCodebases/datasets/272-dim-HumanML3D/motion_data]]`
  - `[[linkedCodebases/datasets/272-dim-HumanML3D/texts]]`
- audit:
  - train: split ids `23384`, present motion files `21466`, missing motion files `1918`, frame mean / p50 / p90 over present files = `221.26 / 240 / 300`, inherited event coverage `22326 / 23384 = 95.48%`
  - val: `1338` samples, missing motion files `0`, frame mean / p50 / p90 = `225.36 / 252 / 300`, inherited event coverage `1322 / 1338 = 98.80%`
  - test: `4042` samples, missing motion files `0`, frame mean / p50 / p90 = `221.17 / 240 / 300`, inherited event coverage `3968 / 4042 = 98.17%`
- implication:
  - 当前不能再把 `272-dim-HumanML3D` 视作完全 ready；至少 train split 仍有 `1918` 个 motion 缺口。

### HumanML3D-272-self

- status: `ready`
- evidence:
  - `[[linkedCodebases/datasets/HumanML3D-272-self/split]]`
  - `[[linkedCodebases/datasets/HumanML3D-272-self/motion_data]]`
  - `[[linkedCodebases/datasets/HumanML3D-272-self/texts]]`
- audit:
  - train: `23384` samples, frame mean / p50 / p90 = `140.84 / 149 / 199`, inherited event coverage `22326 / 23384 = 95.48%`
  - val: `1460` samples, frame mean / p50 / p90 = `141.77 / 153 / 199`, inherited event coverage `1400 / 1460 = 95.89%`
  - test: `4384` samples, frame mean / p50 / p90 = `140.74 / 148 / 199`, inherited event coverage `4196 / 4384 = 95.71%`

## 缺失数据集

### BABEL

- status: `missing`
- expected path:
  - `linkedCodebases/datasets/BABEL`

### TEACH

- status: `missing`
- expected path:
  - `linkedCodebases/datasets/TEACH`
- note:
  - `[[linkedCodebases/teach]]` repo 已在位，但 README 要求的数据链路仍包括：
    - AMASS / BABEL 原始数据
    - TEACH website 登录后下载的 processed data
    - SMPLH male body model
  - 因此当前仍不能把 `TEACH` 记作本地 ready dataset root

### FineMotion

- status: `ready`
- evidence:
  - `[[linkedCodebases/datasets/FineMotion/BPMP_auto.json]]`
  - `[[linkedCodebases/datasets/FineMotion/BPMP_human.json]]`
  - `[[linkedCodebases/datasets/FineMotion/BPMSD_auto.json]]`
  - `[[linkedCodebases/datasets/FineMotion/BPMSD_human.json]]`
  - source release repo:
    - `[[linkedCodebases/FineMotion_release]]`
- audit:
  - `BPMP_auto.json`: `29226` motions, split coverage `train 23382 / val 1460 / test 4384`, median `3` non-empty intervals per sample
  - `BPMSD_auto.json`: `29230` motions, split coverage `train 23382 / val 1460 / test 4384`, median `12` non-empty intervals per sample, and `4` extra ids not in `all.txt`
  - `BPMP_human.json`: `1500` motions, split coverage `train 1212 / val 86 / test 202`, median `3` non-empty intervals per sample
  - `BPMSD_human.json`: `1500` motions, split coverage `train 1212 / val 86 / test 202`, median `12` non-empty intervals per sample
- body-part labelability:
  - 这 4 个 json 都是 `motion_id -> list[str]`，没有显式 `body_part` 字段
  - interval 级严格 regex 单标签统计里，`BPMSD_human.json` 只有 `31.9%` 是 clean single-label interval，`60.3%` 仍是 multi-part mixed 描述
  - 弱标注可见度仍足够：
    - `BPMSD_human.json` 中放宽到“显式提及即可”后，`LOWER_BODY 11946`、`LEFT_ARM 8346`、`RIGHT_ARM 8346`、`UPPER_BODY 8204`
- implication:
  - standalone textual dataset root 已 materialize；作为 weak-supervision MVP 替代源：`够`
  - 作为 clean body-part single-label ground truth：`不够`
  - 底层 motion sequences 仍继承自 `HumanML3D`，不构成独立 motion tensor source
  - 当前最合适的优先顺序是 `BPMSD_human.json` 主用，`BPMSD_auto.json` 补覆盖，`BPMP_*` 只做辅助/回退

## Body Models

- status: `ready`
- evidence:
  - `[[linkedCodebases/datasets/body_models/smpl]]`
  - `[[linkedCodebases/datasets/body_models/smplh]]`
  - `[[linkedCodebases/datasets/body_models/dmpls]]`

## 当前判断

- `HumanML3D` family 已足够支撑 `Event-T2M` 与一部分 `ActionPlan / ReAlign-MLD` 检查。
- `272-dim-HumanML3D` train split 仍缺 `1918` 个 motion 文件，因此它目前更适合作为 partial 而不是 fully ready 资产。
- `BABEL / TEACH` 缺失意味着 `duration / transition` 主切片当前仍不能进入 runnable P2 主测试。
- `FineMotion` standalone 文本标注根已补齐；它已足够支撑 weak-supervision MVP feasibility，但仍不能替代 clean body-part single-label 真值集。
