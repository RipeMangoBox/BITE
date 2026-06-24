---
created: 2026-04-27T23:30
updated: 2026-04-27T23:30
title: "MoDebug Plan B：Event-T2M Local Evidence Audit"
status: archived
tags:
  - MoDebug
  - plan-b
  - EventT2M
  - reproduction
  - audit
related_notes:
  - '[[paperIDEAs/MoDebug/archived/readiness/smoke_logs_v1]]'
  - '[[paperAnalysis/Motion_Generation/ICLR_2026/2026_Event_T2M_Event_Level_Conditioning_Complex_Text_to_Motion_Synthesis|Event-T2M]]'
---

# MoDebug Plan B：Event-T2M Local Evidence Audit

## 0. 一句话结论

本地**有证据**支持三件事：

1. 官方预训练 `hml3d.ckpt` 的本地 eval 与 paper 之间存在**轻度差距**
2. 官方预训练 `hml3d.ckpt` 接到 `HumanML3D-E` 后**没有出现巨大劣化**
3. 你本地的 `exp7` 重训结果与 paper / official pretrained 相比是**明显失真且远差**

但当前证据更支持：

> **先怀疑重训流程/配置，而不是先判死 Event-T2M 这个 backbone。**

## 1. 官方预训练 ckpt 的本地证据

证据来源：

- `linkedCodebases/EventT2M-codes-main/logs/eval/runs/2026-04-04_19-06-00/eval.log`
- `linkedCodebases/EventT2M-codes-main/logs/eval/runs/2026-04-04_19-06-00/metrics.json`
- `linkedCodebases/EventT2M-codes-main/checkpoints/pretrained/HumanML3D/eval/native_normal.yaml`

这次 run 明确使用：

- `ckpt_path = checkpoints/pretrained/HumanML3D/hml3d.ckpt`

本地结果：

- native FID = `0.049953`
- native R_precision_top_3 = `0.846983`
- diversity = `9.3633`

与当前 paper note 中写的标准集结果相比：

- paper summary: `FID 0.040`, `R-Top3 0.818`, `MM-Dist 2.923`

当前能稳说的只有：

- **FID 本地略差于 paper**

不宜直接硬比的部分：

- `R-Top3`
- `MM-Dist`

原因：

- 当前本地导出的 metric 命名和 paper summary 里的面板未完全同口径对齐

因此，这一层证据说明的是：

> 官方预训练 ckpt 的本地复评**不是 paper-perfect**，但差距还没有大到足以单独判 backbone 不可用。

## 2. 本地重训 `exp7` 的证据

证据来源：

- `linkedCodebases/EventT2M-codes-main/checkpoints/pretrained/HumanML3D/exp7/hml3d/event.log`
- `linkedCodebases/EventT2M-codes-main/logs/eval/runs/2026-04-04_19-15-43/metrics.json`
- `linkedCodebases/EventT2M-codes-main/logs/eval/runs/2026-04-04_20-43-20/metrics.json`
- `linkedCodebases/EventT2M-codes-main/checkpoints/pretrained/HumanML3D/exp7/hml3d/checkpoints/eval/native_normal.yaml`

最关键事实：

- `event.log` 显示这次训练 **`max_epochs=1`**

也就是说，这不是一个可信的 paper-grade retrain。

本地 `exp7` eval 结果：

- run `2026-04-04_19-15-43`
  - FID = `30.0708`
  - R_precision_top_3 = `0.1030`
- run `2026-04-04_20-43-20`
  - FID = `30.3509`
  - R_precision_top_3 = `0.1002`

这是一个**数量级上的崩坏**，而不是轻微波动。

因此当前更可信的判断是：

> 本地“重训不如 paper”这件事是成立的，但它更像是 **训练流程未闭合**，而不是 backbone 本身无效。

## 3. 官方预训练 ckpt 在 `HumanML3D-E` 上的本地证据

本轮为了直接验证 `HumanML3D-E`，我临时构造了最小数据壳：

- `data_test.npy` 或 `data_test_condition3.npy` 来自 `HumanML3D-E`
- `Mean.npy / Std.npy` 借自原始 `HumanML3D`

注意：

- 当前仓库自带的 retrieval export 仍然会走标准 `HumanML3D` 检索协议
- 因此本轮只把 **native metrics** 当作 `HumanML3D-E` 的有效证据

### 3.1 overall `HumanML3D-E`

证据来源：

- `/tmp/modebug_eventt2m_hml3de_all_eval/metrics.json`

本地结果：

- FID = `0.049708`
- R_precision_top_3 = `0.836638`
- Diversity = `9.7172`

直接结论：

- 从标准 `HumanML3D` 官方 ckpt 本地复评的 `FID ≈ 0.04995`
- 到 overall `HumanML3D-E` 的 `FID ≈ 0.04971`

**没有出现巨大变化**。

### 3.2 `HumanML3D-E condition3`

证据来源：

- `/tmp/modebug_eventt2m_hml3de_cond3_eval/metrics.json`

本地结果：

- FID = `0.136729`
- R_precision_top_3 = `0.791295`
- Diversity = `8.9073`

直接结论：

- 3-event 子集确实比 overall 更难
- 但数值仍处于**正常量级**
- 没有出现你本地 `exp7` 那种 `FID ~ 30` 的崩坏

### 3.3 对 Plan B 的含义

当前更可信的判断是：

> 官方 `hml3d.ckpt` 接到 `HumanML3D-E` 是可以正常工作的，因此当前完全可以把它当作 Plan B 的 MVP executor 继续做集成验证。

## 4. 对 backbone 决策的直接含义

### 4.1 现在不能据此直接换 backbone

原因：

1. official pretrained 本地 eval 仍然是可用的
2. 真正崩的是 `exp7` 这类本地重训
3. `exp7` 当前连训练轮数都明显不对

所以现阶段更合理的解释顺序应该是：

1. 训练配置/流程问题
2. eval protocol /资产路径问题
3. 最后才是 backbone 问题

### 4.2 当前最稳的做法

对 Plan B MVP，当前最稳的选择仍然是：

1. **用官方 pretrained `hml3d.ckpt` 做集成验证**
2. **不要把本地 `exp7` 当可靠 backbone 证据**
3. **先验证 plug-in 假设，再决定要不要重训 backbone**

## 5. 是否需要换 dataset

当前也**没有足够证据**支持立刻换 dataset。

原因：

1. Plan B 当前主任务天然依赖 `HumanML3D-E`
2. `Event-T2M` 与 `HumanML3D-E` 的 event schema 是天然对齐的
3. 当前问题首先出在本地重训质量不可信，而不是数据主线先天错位

所以当前更合理的 dataset 判断是：

- **MVP 阶段不换主数据**
- 继续用 `HumanML3D-E`
- 只为 diagnostic 轻量构造：
  - corrupted prompts
  - sample manifests
  - attention dumps

## 6. 当前建议

1. 把 `official pretrained hml3d.ckpt` 视为当前唯一可信的 Event-T2M 执行底座
2. 用它先做 attention observation / event corruption sensitivity 的最小验证
3. 若后续必须训练新 reward/backbone，再单独开 reproduction audit
4. 在 reproduction 没闭合前，不建议因为 `exp7` 崩坏而直接换 backbone 或换主数据

## 7. 一句话收口

当前本地证据支持：

> **你本地的 Event-T2M 重训结果确实远差于 paper，但官方 pretrained ckpt 接到 `HumanML3D-E` 后并没有出现巨大劣化，因此现阶段仍不足以直接否定 Event-T2M 作为 Plan B 的 MVP backbone。**
