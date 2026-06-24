---
created: 2026-04-27T22:40
updated: 2026-04-27T23:20
title: MoDebug Plan B：PRCO -> Motion Bridge
status: archived
tags:
  - MoDebug
  - plan-b
  - PRCO
  - motion-bridge
  - observer-solver
  - evidence
source_papers:
  - "[[paperAnalysis/Vision_Language_Reasoning/arXiv_2026/2026_Seeing_with_You_Perception_Reasoning_Coevolution_for_Multimodal_Reasoning|PRCO]]"
related_notes:
  - "[[archive_manifest]]"
  - "[[2026-04-25_modebug-pivot-implicit-event-repair]]"
  - "[[2026-04-27_modebug-planb-finemotion-weak-supervision-audit]]"
---

# MoDebug Plan B：PRCO -> Motion Bridge

## 0. 一句话结论

`PRCO` 对 MoDebug 最值得迁移的不是双角色训练全套，而是：

> **先产出中间证据，再用下游成功率反推这份证据值不值钱。**

它更适合 **第二阶段 sidecar**，不是当前 MVP 主线。

## 1. PRCO 的最小可迁移单元

本地实现里最重要的是三件事：

1. **Observer**
   - 只提取与问题有关的证据
   - 不给最终答案
2. **Solver**
   - 优先依赖 caption / evidence
3. **Utility reward**
   - 用下游是否成功，反向评价中间证据

所以 PRCO 的最小机制核是：

> **“有用但不泄露答案”的中间表征。**

## 2. Motion 侧最自然的对应物

在 motion 域里最自然的映射应写成：

1. Observer 输入
   - `(motion, prompt, event decomposition)`
2. Observer 输出
   - event-level evidence caption
   - 例如：
     - 哪个事件明显出现
     - 哪个事件可能缺失
     - 哪段可能顺序错位
3. Evaluator / Solver 输入
   - `(prompt, evidence caption, optional motion)`
4. 输出
   - 更稳的事件评分
   - 或更强的 error analysis

也就是说：

> 在 MoDebug 里，PRCO 更像 **evidence-producing scorer**，不是另一个生成 backbone。

## 3. 当前不该怎么用

当前不建议：

1. 立刻做完整 Observer/Solver 训练框架
2. 把 Plan B 改造成 interleaved correction pipeline
3. 在 MVP 阶段引入两个大模型互相调用

因为这会把主线从：

- inference-time event reward guidance

拉回到：

- 生成-评估-修正 agent pipeline

这和当前主线不一致。

## 4. 当前最合理的最小迁移版本

如果要先落一个最小单元，唯一值得先试的是：

> **Observer-only sidecar**

也就是：

1. 给 motion + prompt
2. 输出 event-level evidence text
3. 不做修正
4. 只做：
   - qualitative error analysis
   - reward diagnosis
   - sidecar supervision

## 5. 当前阶段的判断

- **能直接开工吗**
  - 能，但只建议做 Observer-only sidecar 设计
- **需要先造数据吗**
  - 不需要新数据集就能先做 qualitative sidecar
  - 若真要训练 utility reward，则后面仍需要中间证据数据
- **现在不该做什么**
  - 不该把 PRCO 直接变成当前 MVP 主框架

## 6. 一句话收口

`PRCO` 当前对 MoDebug 的正确角色是：

> **Observer-style evidence sidecar，用来增强解释力，不是当前 Event reward MVP 的起点。**

