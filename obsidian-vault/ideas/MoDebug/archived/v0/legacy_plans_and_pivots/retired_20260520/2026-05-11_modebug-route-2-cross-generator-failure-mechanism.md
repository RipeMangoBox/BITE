---
created: 2026-05-07T13:01:26+08:00
updated: 2026-05-13T00:20:00+08:00
title: "Route-2: MoDebug 跨生成器失败机制"
status: active
route_id: route-2
tags:
  - MoDebug
  - route_2
  - EventProbe
  - PerceptGuide
  - cross-generator
  - pretrained-generators
  - failure-mechanism
  - mechanistic-diagnosis
related_notes:
  - "[[ideas/MoDebug/README]]"
  - "[[paperIDEAs/MoDebug/2026-05-11_modebug-route-overview]]"
  - "[[paperIDEAs/MoDebug/2026-05-11_modebug-route-3-failure-caption-negative-pair-training]]"
  - "[[paperIDEAs/MoDebug/2026-05-11_modebug-route-4-adaptive-failure-space-ants-style]]"
  - "[[paperIDEAs/MoDebug/2026-05-11_eventt2m-clean-4090-revalidation-log]]"
source_papers:
  - "[[paperAnalysis/Motion_Generation/NeurIPS_2023/2023_MotionGPT_Human_Motion_as_Foreign_Language]]"
  - "[[paperAnalysis/Motion_Generation/CVPR_2024/2024_MoMask_Generative_Masked_Modeling_of_3D_Human_Motions]]"
  - "[[paperAnalysis/Motion_Generation/NeurIPS_2024/2024_MoGenTS_Motion_Generation_based_on_Spatial_Temporal_Joint_Modeling]]"
  - "[[paperAnalysis/Motion_Generation/ICLR_2025/2025_DART_A_Diffusion_Based_Autoregressive_Motion_Model_for_Real_Time_Text_Driven_Motion_Control]]"
  - "[[paperAnalysis/Motion_Generation/ICLR_2025/2025_Language_Motion_Pretraining_for_Motion_Generation_Retrieval_and_Captioning]]"
  - "[[paperAnalysis/Motion_Generation/CVPR_2023/2023_MLD_Executing_your_Commands_via_Motion_Diffusion_in_Latent_Space]]"
  - "[[paperAnalysis/Motion_Generation/ICLR_2026/2026_Motion_R1_Enhancing_Motion_Generation_Decomposed_CoT_RL_Binding]]"
---

# Route-2: MoDebug 跨生成器失败机制

> [!abstract] 当前版本定位
> Route-2 仍然是 MoDebug 的主分析骨架，但它不再追求“大而全”的 cross-generator failure taxonomy。最新版本的完整叙事是：以 `EventT2M` 为关键 probe，写清楚 **event completion gap** 与 **metrics/usability mismatch**，再用其他 generators 和 streaming/planning 方法做对照与压力测试。

## 核心判断

当前最重要的事实不是“哪个 generator 在旧指标上更强”，而是：

1. `EventT2M` 在 event 粒度对齐上确实略优于其他三个 `full_text` 模型。
2. 例如复杂文本中的 `backward`，当前观察里有时只有它能做出来。
3. 但它经常**动作没做完**，靠后的 events 有时没有处理，或者明显弱化。
4. 即使如此，它的指标仍可能优于其他工作。

因此，当前主问题是：

```text
现有 metrics 会高估 event-aware generator 的实用性，
因为它们对 incomplete event realization 惩罚不够。
```

## 当前主论点

Route-2 当前要写的不是“我们找到了很多 failure family”，而是：

```text
一个模型可以在局部 event 对齐上优于 full-text baselines，
同时在整体可用性上仍明显失败；
而当前主指标无法可靠反映这个矛盾。
```

这比泛化的“多模型 failure catalog”更窄，但也更强。

## EventT2M 的当前角色

`EventT2M` 现在不是要被直接写成“最佳 backbone”，而是要被写成一个**关键 probe**：

1. 它证明了 event-level conditioning 的确能带来局部语义优势。
2. 它也暴露了一个更尖锐的问题：局部 event 对齐更好，不等于整句动作完成得更好。
3. 它因此成为当前最好的 `metrics/usability mismatch` 诊断对象。

当前最安全的定位是：

```text
EventT2M is the key probe, not yet the trusted final backbone.
```

## 其他模型与工作的当前角色

### 1. `MotionGPT / MoMask / MoGenTS`

这三者当前主要作为 `full_text` 对照组存在：

1. 用来证明 `EventT2M` 的 event 粒度优势并非幻觉。
2. 用来比较“局部对齐稍强”与“整体没做完”之间的错位。
3. 不再要求它们承载更宽的 failure taxonomy 主叙事。

### 2. `ActionPlan / MotionStreamer / DART / Kimodo`

它们当前都不作为新主线，而是服务于主问题：

| 工作               | 当前定位          | 当前用途                                                                           |
| ---------------- | ------------- | ------------------------------------------------------------------------------ |
| `ActionPlan`     | pressure test | 检查 future-aware planning 是否也会在旧 metrics 下掩盖 completion 问题                      |
| `MotionStreamer` | pressure test | 检查 strict causal streaming 是否更容易在后半段掉链子，同时旧指标是否仍不够敏感                           |
| `DART`           | ablation axis | 检查 local generation / primitive 分段是否真的缓解 completion 问题                         |
| `Kimodo`         | pressure test | 说明更强的 segmented data / stronger foundation model 可能抬高旧指标，但不自动解决 completion gap |

其中最重要的对照逻辑是：

1. `MotionStreamer` 代表纯 streaming/local generation 路线；
2. `ActionPlan` 代表 future-aware planning + streaming execution；
3. `DART` 代表 segment / primitive 级局部生成；
4. `Kimodo` 代表更强数据和更强基座。

它们帮助回答的问题是：当前问题到底是 `EventT2M` 架构私有的，还是更普遍的 evaluation blind spot。

## 当前不再保留的旧叙事

以下内容不再作为这份 route 文档的主叙事：

1. 详细的多轮 `Drift Note`。
2. 冗长的 checkpoint / repo / asset 迁移历史。
3. 大范围的 generator candidate 迭代史。
4. “先做跨生成器完整 failure taxonomy，再做方法”的旧节奏。

这些历史如果需要，应回看：

- [[paperIDEAs/MoDebug/2026-05-11_eventt2m-clean-4090-revalidation-log]]
- `archived/` 下的历史文档

但它们不再属于当前版本的主叙事。

## 当前评价重点

当前优先补的不是新的大方法，而是新的评价视角：

1. 每个 textual event 是否真的被实现。
2. 后半段 events 是否被丢失、截断或弱化。
3. 人审中的“是否把整句动作做完”这一维度。
4. 旧指标只能作为 side evidence，而不能继续当 headline claim。

当前最安全的表述是：

```text
full-level metrics are not enough for complex multi-event usability.
```

## 当前可写 claim

在不夸张的前提下，当前 Route-2 最强的 paper-safe claim 是：

```text
Current text-to-motion metrics can over-reward models
that partially realize event structure
while failing to complete later events in complex text.
```

它可以再加一句方法侧的弱 claim：

```text
We use EventT2M as a key probe and retain a minimal completion-aware intervention
only to show that the gap is actionable rather than purely anecdotal.
```

## 当前执行顺序

1. 固化复杂长文本 battery 中关于 unfinished / late-event drop 的直接证据。
2. 将人审、`gradio` 观察与旧指标并排，正式写出 `metrics/usability mismatch`。
3. 用 `MotionGPT / MoMask / MoGenTS` 做 `full_text` 对照，用 `ActionPlan / MotionStreamer / DART / Kimodo` 做压力测试或 ablation。
4. 只在这一步完成后，测试一个最小 `completion-aware intervention`。

## 当前结论

Route-2 仍然是主线，但它已经从“广义跨生成器 failure mechanism”收缩为：

```text
EventT2M-driven diagnosis of event completion gap
and the evaluation mismatch behind it.
```

当前阶段，这就是最完整、最值得保留的最新版本叙事。
