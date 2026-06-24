---
title: "MoDebug 模型与资产角色登记"
created: 2026-05-20T00:00:00+08:00
updated: 2026-05-20T00:00:00+08:00
status: active
tags:
  - MoDebug
  - baselines
  - role_registry
---

# MoDebug 模型与资产角色登记

## 进入原则

每个模型或资产必须先能服务 full-text / full-motion paired plugin evaluation。能导出 trace 的模型优先，但 trace 不是等待 motion-side grounding 的理由；当前主线先比较 `B` 与 `B+MoDebug`。

| 模型 / 资产 | 当前角色 | 是否进入当前队列 | 边界 |
| --- | --- | --- | --- |
| T2M-GPT | 最小离散 motion token 生成器 | full-motion paired eval 可运行时进入 | trace 可增强解释，但不是 grounding 依赖 |
| MotionGPT | motion-language token 机制探针 | 进入 | T5 / LM-style 信号不和 CLIP-family embedding 做公平排序 |
| Motion-Agent / MotionLLM | planner 改写与 single-call 对照 | 视复现路径进入 | 适合 prompt packing / planner-normalized 插件 |
| MoMask | masked-token 生成器对照 | 进入 | paired eval 必须记录 target length 与 remask schedule |
| MoGenTS | time-joint 结构化 token 对照 | 进入 | trace schema 与 1D token family 分开写 |
| DART / MLD / ReAlign-MLD | diffusion / reward / adapter 参照 | paired eval 可运行时进入 | 不混入 token-prior 主表 |
| SALAD / MotionCLR / SimMotionEdit | attention 与编辑性参考 | 只作 diagnostic reference | 不承担主结果 |
| MotionLab | runtime readiness reference | 只作资产可运行性记录 | smoke 不等于 quality evidence |
| SOMA / Kimodo-like assets | 数据扩展与生成资产参考 | 不进入主实验 | 只服务后续样本池或压力测试 |
| MoLingo | MLPA alignment reference | 不进入 MoDebug 主实验 | 更适合 correspondence layer 路线 |

## 进入当前队列的条件

模型至少满足以下一项：

1. 能运行 `B` vs `B+MoDebug` 的 full-text / full-motion paired evaluation；
2. 能承载一种插件形态，例如 prompt packing、condition rescaling、rerank 或 sampling adjustment；
3. 能运行统一 text perturbation battery；
4. 能导出 token-level、confidence、attention、hidden-state 或 denoising trajectory；
5. 能做 decoded full-motion quality guardrail。

不满足这些条件的对象只登记，不继续扩实验。
