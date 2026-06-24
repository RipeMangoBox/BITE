---
title: "MoDebug P1 事件传递样本选择说明"
created: 2026-05-16T21:45:00+08:00
updated: 2026-05-17T16:36:06+08:00
tags:
  - MoDebug
  - P1
  - selection
---

# MoDebug P1 事件传递样本选择说明

## 目标

说明 P1 输入集为何从旧的“control”表述切换为 sample + decomposed event + single-event prompt。

## 数据对象

- sample：一条完整多事件 prompt。
- decomposed event：从 full prompt 中拆出的单个事件诊断单元。
- single-event prompt：针对每个 decomposed event 写出的独立 prompt。

## 选择策略

1. 覆盖 event_count 1、2、3、4、5。
2. 每个 event_count 尽量保留 2 条 sample。
3. 同一 event_count 内尽量覆盖不同 target_dimension。
4. 所有结果只作为 diagnostic/cross_check。
5. 新结果写在当前 experiment 目录，不写入 `artifacts/`。

## 计算方式

按 event_count 分层选样，每档优先保留 2 条 sample；再把完整 prompt 人工分解为 decomposed event，并为每个 event 写 single-event prompt。该步骤只定义诊断输入，不计算模型质量分数。

## 计划漂移记录

`旧计划：P1-v1 18-case set 补 1/2-event controls` -> `新计划：P1 event-transfer set 覆盖 event_count 1-5` -> `证据：用户明确正式单位是 sample、decomposed event、single-event prompt` -> `影响文档：本实验目录和 MoDebug 相关计划` -> `下一步：继续补 P1 generator/motion 侧真实输出，不用 M0 代理填补`。

## 结论

“5 controls”不是当前实验的正式单位。当前正式单位是 sample、decomposed event 和 single-event prompt。
