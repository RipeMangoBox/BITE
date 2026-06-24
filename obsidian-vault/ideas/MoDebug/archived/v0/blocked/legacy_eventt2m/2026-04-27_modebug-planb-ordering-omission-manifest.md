---
created: 2026-04-27T16:35
updated: 2026-04-27T23:59
title: "MoDebug Plan B：Ordering/Omission Manifest（Event-T2M -> HumanML3D-E）"
status: archived
tags:
  - MoDebug
  - plan-b
  - manifest
  - EventT2M
  - HumanML3D-E
---

# MoDebug Plan B：Ordering/Omission Manifest（Event-T2M -> HumanML3D-E）

## 0. 边界写死

这份 manifest 只服务当前正式主线：

1. generation backbone：`Event-T2M`
2. 主数据源：`HumanML3D-E`
3. 主 symptom：`ordering / omission`
4. reward family：`R_pres / R_ord / R_dur`

同时明确：

- `HumanML3D-E-MP` 不作为这份 manifest 的主 benchmark 来源
- 当前没有第二个与 `HumanML3D-E` 同型、同样适合直接做 ordered-event reward 的开放替代 benchmark
- `FineMotion` 之类资产只能当 sidecar，不替代主数据源

## 1. 当前直接可用的数据结构

### 1.1 主 cache

当前 `HumanML3D-E` 已有可直接消费的 event cache：

- `linkedCodebases/datasets/HumanML3D-E/.tamr_hml3de_gt_events_train.json`
- `linkedCodebases/datasets/HumanML3D-E/.tamr_hml3de_gt_events_val.json`
- `linkedCodebases/datasets/HumanML3D-E/.tamr_hml3de_gt_events_test.json`

最小结构：

```yaml
sample_id:
  prompt_text:
    - event_1
    - event_2
    - event_3
```

这已经足够支撑：

- `R_pres` 的事件存在单元
- `R_ord` 的有序事件对
- `R_dur` 的后续候选接口

### 1.2 split 统计

| Split | 有事件样本数 | 至少 2 个事件 | 事件数 p50 | 事件数 p90 | 最大事件数 |
| --- | ---: | ---: | ---: | ---: | ---: |
| train | 22326 | 10763 | 1 | 3 | 9 |
| val | 1400 | 664 | 1 | 3 | 6 |
| test | 4196 | 2408 | 2 | 3 | 8 |

直接结论：

1. `test` split 已足够作为当前 `ordering / omission` 主切片
2. 第一批优先抽 `>=3 events` 样本
3. `pause / stand still / holds` 这类 case 先保留为 `R_dur` 后续 sidecar，不抢当前主切片

## 2. 推荐 manifest 字段

当前最小推荐 schema：

```yaml
sample_id: "004965"
split: "test"
prompt: "a person walks forward to the left, picks something up and walks back and then shakes what is in the hand"
events:
  - "a person walks forward to the left."
  - "a person picks something up."
  - "a person walks back."
  - "a person shakes what is in the hand."
event_count: 4
candidate_slice:
  - ordering
  - omission
order_pairs:
  - [0, 1]
  - [1, 2]
  - [2, 3]
primary_risk:
  - middle-event omission
  - late-event swap
reward_use:
  - R_pres
  - R_ord
generated_npz: ""
hydra_log: ""
human_review: pending
```

建议追加两个执行字段：

- `generated_npz`
  - 记录 on-policy generation 产物路径
- `human_review`
  - 先只允许 `pending / clear_omission / clear_ordering / weak_execution / looks_fine`

## 3. 第一批正式样本 bank

当前优先保留这批 test 样本：

| sample_id | 事件数 | 推荐用途 | 主要风险 |
| --- | ---: | --- | --- |
| `004965` | 4 | ordering + omission | 中间 `pick up` 缺失，末尾 `shake` 弱执行 |
| `008463` | 4 | ordering + omission | `pick up` 缺失，`stand back up` 弱执行 |
| `001969` | 5 | ordering-heavy | `turn -> walk back -> face back` 错位 |
| `003245` | 3 | ordering + contact event | 中间 contact 事件被直接吞掉 |
| `002246` | 3 | ordering-heavy | `up stairs -> turn left -> back down` |
| `007767` | 3 | omission-heavy | 中间 kick 事件丢失 |
| `011997` | 3 | ordering-heavy | `up stairs -> turn -> down stairs` |
| `006652` | 3 | duration sidecar | `starjumps -> stops -> starts` |

## 4. 已经生成的 seed pool

当前已经有 4 条 `Event-T2M` on-policy 候选样本完成生成，可直接接入 manifest：

- `004965`
- `008463`
- `001969`
- `003245`

对应产物位于：

- `linkedCodebases/EventT2M-codes-main/logs/planb_seed_pool_20260427/gen_joints/generated/`
- `linkedCodebases/EventT2M-codes-main/logs/planb_seed_pool_20260427_hydra_*`

这 4 条当前的角色是：

> 第一批人工复核池，而不是已经确认失败的 hard negatives。

## 5. 当前最小执行建议

1. 从 `HumanML3D-E` test split 先抽 `40-80` 个 `>=3 events` 样本
2. 其中先固定 `10-20` 个 ordering-sensitive 样本
3. 再固定 `10-20` 个 omission-sensitive 样本
4. 先对第一批 on-policy 结果做人审，再决定哪部分进入 reward diagnostic

生成侧的已验证注意事项：

1. 当前可跑入口是 `EventT2M-codes-main/src/sample_motion.py`
2. `data_dir` 需要指向 `datasets/HumanML3D/HumanML3D`
3. 先保留单样本 config + hydra log 的记录方式，便于后续回放与对照

## 6. 一句话收口

当前 MoDebug Plan B 的 manifest 起点应固定为：

> **直接使用 `HumanML3D-E` 的 ordered-event cache，在 test split 的 `>=3 events` 多事件样本上建立 `ordering / omission` 主切片，并把已生成的 4 条 Event-T2M on-policy 样本作为第一批人工复核池。**
