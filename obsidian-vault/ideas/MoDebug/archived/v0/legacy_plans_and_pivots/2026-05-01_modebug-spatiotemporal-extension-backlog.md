---
created: 2026-05-06T16:40:26+08:00
updated: 2026-05-06T16:40:26+08:00
title: MoDebug Backlog：时间-空间并行控制
status: backlog
tags:
  - MoDebug
  - backlog
  - spatiotemporal
related_notes:
  - "[[2026-05-01_modebug-unified-ideas-progress]]"
---

# MoDebug Backlog：时间-空间并行控制

> [!warning] 当前定位
> 本笔记不是 S7-S11 的 active 执行计划。只有在 S8 产出与 joint-level attention / omission 相关的稳定机制证据后，它才重新进入主线评估。

## 1. 思路来源

多事件 motion 的时间并行实际上是身体不同 joint 动作的空间并行。例如"一边挥手一边走路"不只是两个 event 的时间拼接，而是上肢和下肢在同一时间段内执行不同动作。如果能精确控制不同 joint group 的动作，就能从空间维度切入，与纯时间级感知增强的众多工作（AToM、ReAlign、EasyTune、Motion-R1、MoRL）以及 streaming generation（MotionStreamer、KiMoD）形成差异化。

## 2. 可行性评估

| 维度 | 评估 |
| --- | --- |
| 方法价值 | **高**。时间-空间联合 reward 设计有新意，PAPO 等 RL 工作的 per-dimension reward 可启发设计 |
| 定位差异化 | **高**。从"temporal-only"升级为"spatio-temporal event control"，赛道更窄 |
| 数据支撑 | **不足**。HumanML3D-E 文本侧空间粒度不够（event 是动作级，不是 joint 级）；FineMotion 有时间标注和空间细粒度但没有 event 切分 |
| 实现复杂度 | **高**。需要 joint-level motion decomposition + joint-group-aware reward + 可能的 joint-level attention 机制 |

## 3. 当前决策

**当前滞后，不作为主线推进，也不作为 S7-S11 的默认任务。** 仅保留为 S8 后扩展方向。理由：

1. 数据侧瓶颈：HumanML3D-E 没有 joint-level event annotation，FineMotion 没有 event 切分。自建 joint-event 标注成本高且偏离核心。
2. 如果后续 failure attribution 发现 omission 的根因确实与 joint-level attention 分配相关，那么空间维度的方法设计才有实验支撑，可以在 S8 之后决定是否引入。
3. PAPO 的 per-dimension reward 设计可以作为 reward 架构的参考，但需要适配到 motion 的 joint-group 结构。

## 4. 若 S8 后重启，最小路径

1. 用 SMPL joint hierarchy 定义 5 个 joint group（torso / left-arm / right-arm / left-leg / right-leg）。
2. 在 EventT2M 的 cross-attention 中按 joint group 分析 attention 分布。
3. 如果发现 joint-group-level attention 与 event omission 有相关性，设计 joint-group-aware reward term。
4. 数据侧不自建标注，而是用 motion feature 的 joint-group 分解作为 weak supervision。
