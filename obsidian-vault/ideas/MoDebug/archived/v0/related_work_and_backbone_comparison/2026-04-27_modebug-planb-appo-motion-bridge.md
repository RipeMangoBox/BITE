---
created: 2026-04-27T22:40
updated: 2026-04-27T23:20
title: MoDebug Plan B：APPO -> Motion Bridge
status: archived
tags:
  - MoDebug
  - plan-b
  - APPO
  - motion-bridge
  - attention
  - interval-mining
source_papers:
  - "[[paperAnalysis/Vision_Language_Reasoning/CVPR_2026/2026_APPO_Attention_guided_Perception_Policy_Optimization_for_Video_Reasoning|APPO]]"
related_notes:
  - "[[archive_manifest]]"
  - "[[2026-04-27_modebug-planb-ordering-omission-manifest]]"
---

# MoDebug Plan B：APPO -> Motion Bridge

## 0. 一句话结论

`APPO` 对 MoDebug 最值得迁移的不是视频 RL，而是：

> **用 attention 找关键局部，再把 reward / diagnosis 聚焦到这些区间。**

当前它首先是 **interval miner**，不是主 reward 定义器。

## 1. APPO 的最小可迁移单元

本地代码里最关键的是：

1. `compute_token_weights_from_kl()`
   - 用 attention 先找关键帧
   - 再找关键 token
2. `loss_type == arpo_kl`
   - 用这些 token weights 放大局部优化信号

抽象成 motion 语言就是：

> 先找“模型真正盯住的局部”，再决定哪里值得重点更新或重点检查。

## 2. Motion 侧的对应物

当前最自然的 attention 来源不是 MotionPatches，而是 `Event-T2M` 内部已有的：

1. motion token
2. decomposed event token
3. event-conditioned cross-attention

因此最自然的 APPO-style 抽取点是：

> **motion token 对 event token 的 cross-attention 分布。**

## 3. 它和三路 reward 的关系

- 不直接定义 `R_pres / R_ord / R_dur`
- 它回答的是：
  - **哪些时间区间最关键**

当前最直接服务：

1. `R_ord`
   - 找顺序错位最敏感的时间区间
2. `R_pres`
   - 找可能被弱执行或跳过的事件区间
3. `R_dur`
   - 有潜力，但当前不是第一优先级

## 4. 当前该挂在哪

当前不建议先把 APPO 挂到：

1. 独立 reward training 主线
2. MotionPatches 训练主链
3. 新的多模块 RL 系统

当前最合理的挂点是：

> **diagnostic / interval mining sidecar**

也就是：

1. 先不改最终 loss
2. 先把它当关键区间发现器
3. 再决定这些区间是否用于：
   - reward weighting
   - gradient gating
   - error analysis

## 5. 当前最小 MVP

当前最合理的 APPO-lite MVP：

1. 固定 backbone 为 `Event-T2M`
2. 固定数据为 `HumanML3D-E`
3. 对同一 prompt 采样多条 rollout
4. 用粗分信号把样本分成好/坏两组
5. 导出 event cross-attention
6. 比较两组 attention 在时间维上的差异

只看两个输出：

1. top suspicious intervals
2. top suspicious events

## 6. 当前阶段的判断

- **能直接开工吗**
  - 能，前提是先导出 Event-T2M attention
- **需要先造数据吗**
  - 不需要新数据集
  - 但需要 on-policy sample bank 和 attention dump
- **现在不该做什么**
  - 不该直接把 APPO 升级成新的训练主线

## 7. 一句话收口

`APPO` 当前对 MoDebug 的正确角色是：

> **ordering / omission 的关键区间发现器。**
