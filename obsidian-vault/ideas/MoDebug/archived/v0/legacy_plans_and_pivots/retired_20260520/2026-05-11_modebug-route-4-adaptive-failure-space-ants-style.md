---
created: 2026-05-11T20:58:00+08:00
updated: 2026-05-13T00:20:00+08:00
title: "Route-4: 受 ANTS 启发的 MoDebug Adaptive Failure Space"
status: route_candidate
route_id: route-4
tags:
  - MoDebug
  - route_4
  - route_candidate
  - ANTS
  - adaptive_failure_space
  - OOD_detection
  - training_free
related_notes:
  - "[[ideas/MoDebug/README]]"
  - "[[paperIDEAs/MoDebug/2026-05-11_modebug-route-overview]]"
  - "[[paperIDEAs/MoDebug/2026-05-12_ants-to-modebug-transfer-review-ds-kimi]]"
source_pdfs:
  - /home/ripemangobox/Downloads/ANTS.pdf
---

# Route-4: 受 ANTS 启发的 MoDebug Adaptive Failure Space

> [!abstract] 当前版本定位
> Route-4 保留为一个未来可能恢复的 training-free 分支。它的价值在于：如果后续需要在不训练主模型的前提下，对 complex text candidates 做局部 reranking、segment selection 或 failure-aware selection，它可以提供一个结构化的 failure-space 框架。但在当前阶段，它不是主线。

## 当前角色

在最新 `gradio` 观察下，Route-4 暂时降级，原因不是它错误，而是优先级变化了：

1. 当前最强的新事实是 `EventT2M` 在 event 粒度上略优，但经常没把后续 events 做完。
2. 这个问题首先要求我们写清楚 `event completion gap` 与 `metrics/usability mismatch`。
3. 相比之下，Route-4 这种更抽象的 failure-space 叙事，当前还不是最值得优先推进的中心。

## 这条线目前还能提供什么

如果未来恢复，Route-4 最有价值的地方不是泛化理论，而是更具体的 training-free 用途：

1. 在 complex text 下，对多个局部 candidates 做 completion-aware reranking。
2. 在 segment / chunk 级别选择更可能完成后续 event 的候选。
3. 与 `MotionStreamer` 一类 local generation 路线结合，做局部选择而不是直接大训练。

也就是说，这条线如果要回来，最合理的版本不是“统一 failure space 大理论”，而是：

```text
complex-text completion-aware training-free selection branch
```

## 为什么当前降级

因为现在已经有更强的主问题：

1. `EventT2M` 局部 event 对齐略好；
2. 但动作经常没做完；
3. 旧 metrics 又可能继续给高分。

在这种情况下，先写评价缺口，再决定是否需要更复杂的 training-free reranking，优先级更合理。

## 与 streaming / stronger-data 路线的关系

当前这条 Route 需要放在新的背景里理解：

1. `MotionStreamer` 提示了 local generation 的可能性，但也带来 stitching 与局部视野问题。
2. `ActionPlan` 提示了 future-aware planning 的价值。
3. `Kimodo` 提示我们：更强的 segmented data 和更强基座可能提高旧指标，但不自动解决 completion gap。

因此，如果 Route-4 将来恢复，它的角色更像是：

```text
在已有 planning / streaming / stronger-data 路线之间，
增加一个 failure-aware training-free selection layer
```

而不是独立承担当前 MoDebug 的主叙事。

## 当前可保留的核心句

当前最安全的 Route-4 说法是：

```text
If MoDebug later needs a training-free branch,
Route-4 is the place for completion-aware failure-space scoring and candidate selection.
```

## 当前结论

Route-4 保留，但只作为未来支线。当前阶段，它不再与 `Route-2` 并列主推；主线优先级已经转移到 `event completion gap` 与 `metrics/usability mismatch`。
