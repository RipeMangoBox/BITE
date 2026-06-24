---
title: "MoDebug 主线：Full-Text / Full-Motion 插件式评估"
created: 2026-05-20T00:00:00+08:00
updated: 2026-05-20T00:00:00+08:00
status: active
hypothesis: "MoDebug 的当前可行验证可以只依赖 full text 与 full generated motion，通过 paired baseline vs baseline+MoDebug 证明插件式增幅；motion-side event grounding 作为并行资产路线推进。"
tags:
  - MoDebug
  - plugin_eval
  - full_text_full_motion
  - baseline_independent
---

# MoDebug 主线：Full-Text / Full-Motion 插件式评估

## 定位

MoDebug 当前 MVP 不依赖 motion-side event grounding。它先把 MoDebug 写成一类预训练 text-to-motion baseline 的插件：

```text
full text prompt + pretrained generator
-> original motion

full text prompt + pretrained generator + MoDebug
-> guided motion
```

核心比较是同一 baseline、同一 prompt、同一 seed / length / candidate budget 下：

```text
original baseline vs baseline + MoDebug
```

这条路线回答的是：MoDebug 是否能在完整文本和完整 motion 输出层面提升动作质量与指令跟随。

## 为什么可行

MoDebug 的主对象是文本条件传播，而不是 motion event 边界。只要 baseline 能接收 full text 并生成 full motion，就可以测试：

1. 文本条件在 generator 内部是否有可观测响应；
2. MoDebug 是否能改变该响应；
3. 改变后的 full motion 是否更符合 full text；
4. 这种增幅是否能跨多个 baseline 复现。

motion-side grounding 可用于后续解释更细的局部错配，但不是插件有效性的前置条件。

## 最小实验协议

### 输入

1. full text prompts；
2. 每个 prompt 的 baseline generated full motion；
3. 可选：baseline trace signal，如 condition projection、attention、hidden state、logits、confidence 或 denoising trajectory；
4. 可选：多候选 motion，用于 rerank 型 MoDebug。

### 条件对

| 条件 | 含义 |
| --- | --- |
| `B` | 原始 pretrained baseline |
| `B+MoDebug` | 同一 baseline 加 MoDebug guidance / rerank / condition repair |
| `same_seed` | 两个条件使用相同 seed，适合 process-time guidance |
| `same_candidate_pool` | 两个条件使用同一候选池，适合 rerank |
| `same_length_budget` | 两个条件使用相同长度或 token budget |

### 可用插件形态

| 插件形态 | 依赖 | 适合场景 |
| --- | --- | --- |
| prompt packing / planner-normalized prompt | full text | baseline 没有开放内部 hook |
| text-condition rescaling | condition embedding | 文本条件被弱化 |
| projection normalization / gating | condition projection | projection 后信号坍缩 |
| attention bias | attention map | text-to-motion attention 可访问 |
| token-level rerank | logits 或 candidate pool | 多候选生成或可重采样 |
| sampling / remask schedule adjustment | confidence / trajectory | masked 或 denoising 生成器 |

## 评价

### 主评价

使用完整文本和完整 motion 做 paired comparison：

1. blind human pairwise preference：`B+MoDebug` 是否更符合 full text；
2. instruction-following checklist：方向、计数、顺序、身体部位、物体交互、速度等由文本自动解析成检查项，但不需要 motion event boundary；
3. standard quality guardrail：FID、diversity、foot sliding、pose validity、naturalness；
4. independent scorer cross-check：TMR / retrieval score / VLM 只作为 side signal。

### 机制评价

机制证据来自 full text 条件下的传播变化：

1. `trace_signal(B+MoDebug) - trace_signal(B)` 是否朝预期方向变化；
2. 该变化是否与 full-motion paired preference 同向；
3. 相同 signature 是否能跨 prompt bucket 或 baseline 复现。

### Prompt bucket

不需要 motion event grounding，也可以只从文本侧建立 bucket：

1. direction / path；
2. count / duration；
3. order / transition words；
4. body part；
5. object interaction；
6. speed / style；
7. long compositional prompt。

这些 bucket 用于分层报告，不等价于 motion-side event 标注。

## 成功标准

最小成功标准：

1. 至少一个 baseline 上，`B+MoDebug` 在 blind human pairwise preference 中显著优于 `B`；
2. 基本 motion quality guardrail 没有明显下降；
3. 有至少一个 trace signature 能解释 MoDebug 的干预位置。

更强论文标准：

1. 至少两个不同生成机制的 baseline 上复现增幅；
2. 使用同一套 full-text / full-motion protocol；
3. 每个 baseline 都报告 compute、seed、length budget 和 candidate budget；
4. motion-side grounding 结果只作为附加解释，不参与主 claim 的成立。

## 与 Motion-Side Grounding 的并行关系

当前主线：

```text
full text -> baseline full motion
full text -> baseline+MoDebug full motion
paired full-motion evaluation
```

并行资产路线：

```text
full motion -> candidate grounding
VLM / PoseFix / geometry cross-check
grounding reliability audit
future fine-grained training or diagnosis
```

并行路线通过后，可以补充解释 MoDebug 改善了哪些局部 text unit；通过前，不影响 full-text / full-motion 插件评估。
