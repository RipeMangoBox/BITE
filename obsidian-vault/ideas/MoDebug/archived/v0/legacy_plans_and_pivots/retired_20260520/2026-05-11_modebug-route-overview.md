---
created: 2026-05-11T20:58:00+08:00
updated: 2026-05-13T00:20:00+08:00
title: MoDebug Route 概览
status: active
route_id: route-overview
tags:
  - MoDebug
  - route_overview
  - route_comparison
  - research_strategy
  - ICLR
related_notes:
  - "[[ideas/MoDebug/README]]"
  - "[[paperIDEAs/MoDebug/2026-05-11_modebug-route-1-local-motion-semantic-artifact-debug-non-mllm]]"
  - "[[paperIDEAs/MoDebug/2026-05-11_modebug-route-2-cross-generator-failure-mechanism]]"
  - "[[paperIDEAs/MoDebug/2026-05-11_modebug-route-3-failure-caption-negative-pair-training]]"
  - "[[paperIDEAs/MoDebug/2026-05-11_modebug-route-4-adaptive-failure-space-ants-style]]"
  - "[[paperIDEAs/MoDebug/2026-05-11_eventt2m-clean-4090-revalidation-log]]"
---

# MoDebug Route 概览

> [!abstract] 当前主判断
> MoDebug 当前不再把四条 Route 当作并列主线推进。最新版本的完整叙事是：先用 `EventT2M` 暴露并量化 **event completion gap** 与 **metrics/usability mismatch**，再决定是否恢复更宽的方法线。换句话说，当前最重要的问题不是“谁的旧指标更高”，而是“哪些模型虽然局部 event 对齐更好，但仍然没有把整句动作做完，而现有 metrics 又看不见这个缺口”。

## 最新 gradio 观察

当前需要正式写进总叙事的观察是：

1. `EventT2M` 在 event 粒度对齐上确实略优于其他三个 `full_text` 模型，例如复杂文本中的 `backward` 有时只有它能实现。
2. 但它经常**动作没做完**，靠后的 events 会丢失、缩短，或退化成弱动作。
3. 即使如此，它在当前主指标上仍可能优于其他工作，这说明现有 metrics 与真实可用性错位。
4. `MotionStreamer` 一类 streaming / local generation 方法提供了另一条思路：一次只处理小段文本，再平滑拼接。但它们也有自己的代价，包括片段衔接、局部最优、以及训练时单段文本复杂度与推理时单段复杂度不匹配。
5. `Kimodo` 一类更强基座提醒我们：单纯讲“更高质量、更大规模的时间片切分数据”并不是一个足够新的故事。

## 当前路线图

| Route                             | 当前一句话定位                                                                          | 当前角色          |
| --------------------------------- | -------------------------------------------------------------------------------- | ------------- |
| Route-1 local artifact non-MLLM   | 处理局部几何/接触/局部语义 artifact 的支持线                                                     | support only  |
| Route-2 cross-generator mechanism | 当前主线，收缩为 `EventT2M` 驱动的 `event completion gap` 与 `metrics/usability mismatch` 诊断 | primary       |
| Route-3 negative-pair training    | 若后续需要训练型 intervention，可作为 `completion-aware` 支线恢复                                | secondary     |
| Route-4 adaptive failure space    | 若后续需要 training-free reranking / local selection，可作为未来支线恢复                        | future branch |

## 当前聚焦点

### 1. 主线

主线是：

```text
EventT2M 这类 event-aware generator 可能在局部 event 对齐上更强，
但仍然因为后续 event 没做完而距离真实可用性很远，
而当前主指标对这种失败惩罚不够。
```

### 2. 次线

只保留一个最小 `completion-aware intervention` 作为 proof-of-concept。

它的作用不是把项目升级成“新 generator”，而是证明这个 gap 不是纯诊断幻觉，而是一个可被部分修复的 failure mode。

### 3. 暂时降级的内容

以下内容保留，但不再是当前主叙事：

1. 大而全的 cross-generator failure taxonomy。
2. 泛化的 failure-caption training 主线。
3. ANTS-style adaptive failure-space 主线。
4. 局部 artifact 修复主线。

## 对 streaming / planning / stronger-data 路线的当前定位

| 工作               | 当前定位          | 用途                                                                                          |
| ---------------- | ------------- | ------------------------------------------------------------------------------------------- |
| `ActionPlan`     | pressure test | 检查 future-aware planning 是否也会在旧 metrics 下掩盖 completion 问题                                   |
| `MotionStreamer` | pressure test | 检查 strict causal streaming 是否更容易出现后半段掉链子，同时旧指标仍不够敏感                                         |
| `DART`           | ablation axis | 检查“分段 primitive / local generation”是否真的改善 completion，而不是只改变错误形态                             |
| `Kimodo`         | pressure test | 说明 stronger segmented data / better foundation model 可能抬高旧指标，但不自动让“event completion”成为已解决问题 |

## 当前论文形态

当前最安全的论文形态不是“又一个更强的 motion generator”，而是：

```text
现有 text-to-motion metrics 会系统性忽略 complex text 下的 incomplete event realization。
我们用 EventT2M 作为关键 probe，将这一 blind spot 显式化，并给出最小 completion-aware proof-of-concept。
```

## 当前执行顺序

1. 固化复杂长文本 battery 中的 `event completion` 失败证据。
2. 将人审、`gradio` 观察和旧指标结果并排，形成 `metrics/usability mismatch` 的正式证据。
3. 引入 `ActionPlan / MotionStreamer / DART / Kimodo` 作为压力测试或对照，而不是新的主线替代方向。
4. 仅在这一步写稳之后，测试最小 `completion-aware intervention`。

## 当前决定

当前不再把四条 Route 合并成一篇“大而全”的方法论文。最新完整版本的路线是：

1. `Route-2` 为主。
2. `Route-3` 和 `Route-4` 暂时降为备选方法支线。
3. `Route-1` 保留为局部支持线。

如果后续要恢复更宽的方法线，也必须建立在 `event completion gap` 已经被正式写清楚的前提上。
