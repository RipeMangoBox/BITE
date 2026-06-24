---
created: 2026-05-12T23:58:00+08:00
updated: 2026-05-12T23:58:00+08:00
title: MoDebug 聚焦更新：event completion gap 与 metrics/usability mismatch
status: active
tags:
  - MoDebug
  - event_completion
  - metrics_mismatch
  - EventT2M
  - gradio_review
related_notes:
  - "[[ideas/MoDebug/README]]"
  - "[[paperIDEAs/MoDebug/2026-05-11_modebug-route-overview]]"
  - "[[paperIDEAs/MoDebug/2026-05-11_modebug-route-2-cross-generator-failure-mechanism]]"
  - "[[paperIDEAs/MoDebug/2026-05-11_eventt2m-clean-4090-revalidation-log]]"
source_notes:
  - "[[paperIDEAs/MoDebug/modebug_m0_gt_paired_fixed_repeat_human_annotations_20260511/human_annotations]]"
  - "[[paperIDEAs/MoDebug/modebug_gt_paired_human_annotations_20260510/human_annotations]]"
---

# MoDebug 聚焦更新：event completion gap 与 metrics/usability mismatch

> [!abstract] 当前主判断
> MoDebug 的第一主线不再是并列推进多条 debug / training 路线，而是先把 **event completion gap** 写清楚：一个模型即使在 event presence/omission 粒度上优于 `full_text` baselines、甚至在旧 metrics 上拿高分，仍然可能因为**后续 events 没做完**而距离真实可用性很远。

## 1. 触发这次聚焦更新的观察

最新 `gradio/manual review` 指向了一个更强、也更窄的事实：

1. `EventT2M` 在 event 粒度对齐上确实有局部优势。
2. 但它经常**动作没做完**，靠后的 events 会丢失、缩短，或退化成原地踏步。
3. 即使如此，它仍可能在当前主指标上优于其他模型。

这说明当前主问题不是“谁更会生成 motion”，而是：

```text
现有 metrics 对 event completion 与真实可用性不敏感
```

## 2. 本地证据链

最强本地证据来自以下几类材料：

1. `EventT2M` 论文和 revalidation 记录支持它在 event presence / omission 条件上确实更敏感。
2. `gradio` 人审 CSV 则直接显示：复杂长文本下，它会出现 `six steps -> only two steps`、后半段退化为原地踏步等 incomplete realization。
3. 历史 evaluation policy note 已经明确写过：

```text
high full-level score -/-> high event-level correctness
```

所以更稳的主结论是：

```text
EventT2M 在 event presence/omission 上更敏感，
但复杂文本下仍会 unfinished / late-event drop，
而当前主指标对这种 failure 惩罚不够。
```

## 3. 新的主聚焦

### 3.1 主线

**主线**：以 `EventT2M` 为关键 probe，暴露并量化 `event completion gap` 与 `metrics/usability mismatch`。

这条主线的 paper-safe 表述是：

```text
current text-to-motion metrics can over-reward models
that partially realize event structure but fail to complete the motion
```

### 3.2 次线

只保留一个轻量 `completion-aware intervention` 作为 proof-of-concept：

1. 它的作用不是把项目升级成新 generator。
2. 它的作用只是证明：这个 gap 不是纯评审偏见，而是一个可诊断、可部分修复的 failure mode。

## 4. 旧路线如何降级

### 4.1 暂时非主线

以下路线保留，但都不再是当前主叙事：

1. `Route-1 local artifact`
2. `Route-3 failure-caption negative-pair training`
3. `Route-4 ANTS-style adaptive failure space`
4. 泛化的 cross-generator failure taxonomy

### 4.2 为什么降级

因为当前最强观察不是局部 artifact、也不是 failure caption supervision，而是：

```text
event-aware model 也可能在真实使用上明显没做完
```

如果这个缺口都还没正式写清楚，就不适合继续把主精力分散到更宽的 debug story 上。

## 5. 对 streaming / segmented work 的新定位

在这次聚焦更新之后：

1. `ActionPlan`：pressure test
2. `MotionStreamer`：pressure test
3. `DART`：ablation axis
4. `Kimodo`：pressure test

它们当前的作用不是替代主线，而是帮助回答三个问题：

1. 问题是不是 `EventT2M` 架构私有的？
2. 把长文本拆段之后，是否真能缓解 completion 问题？
3. 更强数据 / segmentation / planning 是否只是继续抬高旧指标，而不真正解决 completion？

## 6. 当前最值得优先补的 evaluation redesign

优先级最高的是围绕 `event completion` 的评估补充，而不是继续堆旧指标。

建议优先补：

1. 每个 textual event 是否被实际实现。
2. 后半段 events 的覆盖率。
3. 人审中的“是否把整句做完”这一维度。
4. 明确把旧指标降为 side evidence，而不是 headline claim。

## 7. 一个月内的路线

### 7.1 前两周

1. 固化复杂长文本 battery。
2. 把 `gradio/manual review` 中关于 unfinished / late-event drop 的现象写成结构化 evidence。
3. 形成 `event completion gap` 的最小评价协议。

### 7.2 后两周

1. 做一个最小 `completion-aware intervention`。
2. 检查它是否能在不破坏已有 event alignment 优势的前提下，减少后半段未完成。
3. 用 `ActionPlan / MotionStreamer / DART / Kimodo` 做压力测试或对照，不把它们拉成新的主线。

## 8. Stop-Doing List

1. 暂停把 `FID / R-Precision` 当作主结果讲述。
2. 暂停把 `Route-3` 和 `Route-4` 当作当前主方法线。
3. 暂停泛化的 cross-generator catalog 式 failure 收集。
4. 暂停把“更强 segmented data”讲成新贡献。
5. 暂停任何“MoDebug 会变成更强 generator”的叙述。

## 9. 一句话版本

当前最值得写的不是“我们又提出了一个 motion debugging method”，而是：

```text
我们找到了一个会被当前指标系统性忽略的关键 usability defect：
复杂文本下的 event completion failure
```
