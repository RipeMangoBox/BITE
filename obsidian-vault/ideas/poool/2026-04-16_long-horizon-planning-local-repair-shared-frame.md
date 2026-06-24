---
created: 2026-04-16
updated: 2026-04-16
tags:
  - paper-idea
  - shared-frame
  - Motion_Generation
  - long-horizon
  - planning
  - repair
---
# 2026-04-16 长时序动作规划与局部修复共享框架

> 这篇笔记抽离多篇“长时序 / 多事件 / 结构化规划 / 局部修复”笔记共享的母题，让各自主笔记只保留自己的独立主张。

## 1. 公共问题

- **多事件 prompt** 会导致 event omission、order drift、late-stage collapse。
- **长序列错误往往是局部的**，但很多方法仍然采用整段重采样。
- **transition inconsistency** 常常是边界问题，不一定是整段生成器失效。
- **评估目标正在从“像不像”转向“事件是否完成、后果是否正确”**。

## 2. 共享 pipeline

1. **结构化规划**：先把 prompt 变成 event chain、event graph、program 或 candidate set。
2. **分段生成**：按 event / segment / motion chunk 生成，而不是把全部复杂性压给一次解码。
3. **局部诊断或验证**：定位失败 span、比较候选后果、判断是否需要修补。
4. **选择性局部修复**：只修失败段或高风险边界，而不是整段重生成。
5. **全局一致性检查**：最后再看长程顺序、过渡、结果与副作用。

## 3. 共享评测轴

- **event completion**
- **order correctness**
- **boundary smoothness**
- **local repair vs whole regeneration**
- **outcome-aware success / risk**

## 4. 与现有笔记的分工

- [[2026-03-19_motion-repair-fine|2026-03-19_motion-gen-new-paradigm-fine]]：聚焦 diagnosis + local repair，把 reasoning 变成 test-time compute allocator。
- [[2026-04-05_eventgraph2motion-final-proposal|2026-04-05_eventgraph2motion-final-proposal]]：聚焦 event graph 作为生成中间表示。
- [[2026-04-05_motion-counterfactual-world-testing|2026-04-05_motion-counterfactual-world-testing]]：聚焦 world-model / verifier / outcome-aware selection。
- [[2026-04-06_structured-motion-understanding-from-motionpatch|2026-04-06_structured-motion-understanding-from-motionpatch]]：从理解侧补上 event / relation / evidence 的支撑表示。

## 5. 整理后的阅读顺序

1. 先读本文，统一“规划 → 生成 → 验证 / 修复”的公共骨架。
2. 再读 [[2026-04-05_eventgraph2motion-final-proposal|EventGraph2Motion]]，看中间表示如何设计。
3. 接着读 [[2026-03-19_motion-repair-fine|Reason-Plan-Repair]]，看局部修复闭环。
4. 如果想把“修不修”进一步升级为“验证后果再决策”，读 [[2026-04-05_motion-counterfactual-world-testing|Motion generation as counterfactual world testing]]。
