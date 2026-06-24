---
created: 2026-04-27T16:35
updated: 2026-04-27T16:35
title: MoDebug Plan B：Event-T2M Hard Negative Seed Pool v0
status: archived
tags:
  - MoDebug
  - plan-b
  - hard-negatives
  - EventT2M
  - HumanML3D-E
related_notes:
  - "[[2026-04-27_modebug-planb-ordering-omission-manifest]]"
---

# MoDebug Plan B：Event-T2M Hard Negative Seed Pool v0

## 0. 任务边界

这份 seed pool 只做一件事：

> 为 `Plan B` 准备第一批 **Event-T2M on-policy candidate negatives**，用于后续人工复核、reward 定义和最小 pilot。

关键约束已经遵守：

- backbone: `Event-T2M`
- dataset semantics: `HumanML3D-E`
- 不把 `HumanML3D-E-MP` 当作 Event-T2M 主数据源

## 1. 当前执行到哪一步

### 已完成

1. 确认真正可跑的生成入口是：
   - `EventT2M-codes-main/src/sample_motion.py`
2. 修通了最小生成链路：
   - 正确的 `data_dir` 应指向：
     - `/home/ripemangobox/Coding/Github/Motion/datasets/HumanML3D/HumanML3D`
   - 而不是上一级 `.../datasets/HumanML3D`
3. 生成了第一批 4 条多事件样本：
   - `planb_004965_0.npz`
   - `planb_008463_0.npz`
   - `planb_001969_0.npz`
   - `planb_003245_0.npz`

### 当前定义

这里的 `hard negative seed pool` 还不是“已经确认失败的负样本集”，而是：

> **最值得先人工复核的一批 on-policy 候选样本**

原因：

- 生成已经完成
- prompt 都是 `HumanML3D-E` 的真实多事件 case
- 每条都对 `ordering / omission` 很敏感
- 但是否真的失败，还需要人工看一眼或后续自动规则筛一轮

## 2. 当前生成产物

### 2.1 motion outputs

- `[[linkedCodebases/EventT2M-codes-main/logs/planb_seed_pool_20260427/gen_joints/generated/planb_004965_0.npz]]`
- `[[linkedCodebases/EventT2M-codes-main/logs/planb_seed_pool_20260427/gen_joints/generated/planb_008463_0.npz]]`
- `[[linkedCodebases/EventT2M-codes-main/logs/planb_seed_pool_20260427/gen_joints/generated/planb_001969_0.npz]]`
- `[[linkedCodebases/EventT2M-codes-main/logs/planb_seed_pool_20260427/gen_joints/generated/planb_003245_0.npz]]`

### 2.2 hydra logs

- `[[linkedCodebases/EventT2M-codes-main/logs/planb_seed_pool_20260427_hydra_004965]]`
- `[[linkedCodebases/EventT2M-codes-main/logs/planb_seed_pool_20260427_hydra_008463]]`
- `[[linkedCodebases/EventT2M-codes-main/logs/planb_seed_pool_20260427_hydra_001969]]`
- `[[linkedCodebases/EventT2M-codes-main/logs/planb_seed_pool_20260427_hydra_003245]]`

## 3. 第一批候选样本

| sample_id | 事件数 | 主要风险 | prompt |
| --- | ---: | --- | --- |
| `004965` | 4 | 中间事件 omission、末尾事件弱执行 | `walk forward -> pick up -> walk back -> shake` |
| `008463` | 4 | `pick up` omission、`stand back up` 弱执行 | `walk -> squat pick-up -> stand up -> resume walk` |
| `001969` | 5 | `turn around / faces back` 顺序错位 | `walk forward -> turn -> walk back -> face back -> stand still` |
| `003245` | 3 | 中间 contact 事件缺失 | `raise arms -> fingers touching -> lower arms` |

## 4. 为什么这 4 条适合做 seed pool

### 4.1 `004965`

适合测：

- `R_pres`: `pick something up` 是否出现
- `R_ord`: `walk back` 是否出现在 `pick up` 之后
- `R_dur`: `shake` 是否只是一闪而过

### 4.2 `008463`

适合测：

- `R_pres`: 中间 `pick up` 是否真的落地
- `R_ord`: `stand back up` 与 `resume walk` 的相对顺序
- 这是当前最值得保留的主样本之一

### 4.3 `001969`

适合测：

- `R_ord`: `turn around -> walk back -> face back -> stand still`
- 它的事件链更长，特别容易暴露顺序与 late-stage collapse

### 4.4 `003245`

适合测：

- `R_pres`: contact-like 子事件 `fingers touching`
- 这是最短链但最适合检查“中间细粒度事件是不是会直接丢”

## 5. 这批候选还差什么

当前还差两步，才能从 `seed pool` 升级成更硬的 negative pool：

1. **人工复核**
   - 每条样本看一遍渲染或 joints，标：
     - `clear omission`
     - `possible omission`
     - `clear ordering error`
     - `weak execution`
     - `looks fine`

2. **最小自动筛选**
   - 可用未来的轻量规则或 frozen reward backbone，对这 4 条先打第一轮粗分

## 6. 当前可直接复用的命令模式

本轮已经验证可跑的模式是：

1. 在 `EventT2M-codes-main/configs/` 根目录下写单独 config
2. 用：

```bash
python src/sample_motion.py --config-name planb_<sample_id>.yaml hydra.run.dir=...
```

3. `data_dir` 必须指向：

```bash
/home/ripemangobox/Coding/Github/Motion/datasets/HumanML3D/HumanML3D
```

而不是上级目录。

## 7. 一句话收口

当前 `hard negative seed pool v0` 的价值不是“已经证明这 4 条都失败”，而是：

> **先用真实 `HumanML3D-E` 多事件 prompt 跑出一小批 Event-T2M on-policy 样本，把最容易出 `ordering / omission` 问题的 case 收口成第一批人工复核池。**
