---
title: "MoDebug 主线：文本条件传播引导"
created: 2026-05-20T00:00:00+08:00
updated: 2026-05-28T16:40:00+08:00
status: active
hypothesis: "MoDebug 通过诊断和引导 text condition 在 pretrained motion generator 内部的传播，提高生成 motion 的质量和指令跟随。"
tags:
  - MoDebug
  - active_route
  - text_condition_propagation
  - guidance
---

# MoDebug 主线：文本条件传播引导

## 定位

本目录是 MoDebug 当前主线入口。

> [!note] 当前执行入口
> 2026-05-27 的实现快照已归档到 `_archive_20260527/`，旧路径 `implementation_20260527/` 暂时保留为兼容 symlink。后续任务、执行日志和快速命令以本目录为唯一正文根目录维护：[[TASK_BOARD|TASK_BOARD]]、[[execution_log|execution_log]]、[[QUICKSTART|QUICKSTART]]。

MoDebug 的方法对象是：

```text
text condition -> generator internal propagation -> motion output
```

核心目标：

```text
通过诊断并引导 text embedding / text condition 的传播，
提高 full motion 的 motion quality 与 instruction following。
```

## 当前核心科学问题

如何从 aggregate 统计和 sample-level 证据中进行合理的问题发现，并把问题发现转成可验证的机制设计？

当前验收口径：

1. aggregate 统计只用于提出候选 failure pattern，例如 delta 过低、delta 过高、晚期峰值、错误特征路由、时序波动大、prompt 类型困难。
2. 每个候选 pattern 必须回到 sample-level 证据链检查 prompt、human annotation、motion MP4、forward/delta manifest 和可视化。
3. 每个机制假设必须说明统计证据、sample 证据、预期 delta 改变、预期 motion-level 改善和失败判据。
4. trace delta 当前只能作为 diagnostic / side signal；若要升级为正式结论，需要 held-out evaluator、random/semantic perturbation 控制和 coverage 记录。

详见 [[analysis_plan_400_samples|400-sample text-condition trace 分析方案设计]]。

## 操作层级

MoDebug 可以操作以下任一层：

1. text encoder 输出；
2. phrase / attribute / prompt embedding；
3. condition projection；
4. cross-attention 或 conditioning gates；
5. motion-token logits / confidence；
6. denoising 或 remasking trajectory；
7. candidate rerank score。

语义步骤、短语、属性和 token span 都是可用文本单元；实验记录统一用 `text_unit_type` 标明来源。

## 核心假设

| 假设 | 含义 | 检查方式 |
| --- | --- | --- |
| H1 文本可分性 | prompt 的关键语义在 text embedding 中是否可分 | phrase / attribute perturbation distance |
| H2 投影瓶颈 | text signal 进入 generator 后是否被压扁 | condition projection delta |
| H3 传播衰减 | text signal 在层间或步骤间是否变弱 | layer / step response curve |
| H4 错误绑定 | text signal 是否影响错误 token、time 或 body region | token / body / time response localization |
| H5 引导有效 | 针对 signature 的轻量干预是否改善 output | guided vs original comparison |

## 第一批实验

1. 先跑 full-text / full-motion paired evaluation，比较 `B` 与 `B+MoDebug`。
2. 建立 trace availability table。
3. 为 full text prompts 生成 phrase / attribute perturbation battery。
4. 对 trace 可用模型导出 condition projection、layer delta、logits / confidence、token path 或 remask trajectory。
5. 从 propagation signature 中选择一个最稳定的 guidance target。
6. 做最小 guided generation / rerank 验证。

motion-side grounding 只作为并行资产路线。可靠性通过前，MoDebug 主线只使用 full text 与 full motion 的 paired comparison；若未来进入 grounding-based training，必须把 `text_unit`、`start_state`、`transition_context` 和 `core motion evidence` 分开建模。

## 相关文件

1. [[ideas/MoDebug/active/full_text_full_motion_plugin_eval/README|Full-Text / Full-Motion 插件式评估]]
2. [[propagation_schema|传播记录字段]]
3. [[experimental_gates|实验关口]]
4. [[2026-05-27_f_signal_parallel_implementation_plan|f-Signal 并行实现计划]]
5. [[TASK_BOARD|当前任务板]]
6. [[GPT_HANDOFF|2026-05-27 实现快照交接]]
7. [[ideas/MoDebug/active/motion_grounding_state_dependence/README|Motion-Side Grounding 并行路线]]
8. [[ideas/MoDebug/roadmap|MoDebug 当前路线图]]
