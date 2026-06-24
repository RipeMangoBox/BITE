---
created: 2026-05-11T20:58:00+08:00
updated: 2026-05-13T00:20:00+08:00
title: "Route-1: 不依赖 MLLM 的 MoDebug 局部 motion semantic artifact 调试"
status: route_candidate
route_id: route-1
tags:
  - MoDebug
  - route_1
  - route_candidate
  - local_artifact
  - non_mllm
  - motion_semantics
related_notes:
  - "[[ideas/MoDebug/README]]"
  - "[[paperIDEAs/MoDebug/2026-05-11_modebug-route-overview]]"
---

# Route-1: 不依赖 MLLM 的 MoDebug 局部 motion semantic artifact 调试

> [!abstract] 当前版本定位
> Route-1 研究 **local motion semantic artifacts**：检测生成 motion 在哪里违反了局部语义或物理约束，将失败归因到某个 motion segment / body part / event unit，然后施加有针对性的 non-MLLM repair 或 selection operator。当前版本中，它不是主线，而是一个局部支持分支。

## 当前角色

在最新的 `gradio` 观察下，MoDebug 的主问题已经收缩到：

```text
event-aware generator 也可能因为后续 event 没做完而不可用，
而当前 metrics 对这种 failure 不敏感。
```

因此，Route-1 当前不承担主叙事。它的价值只在于：

1. 当主线开始做 `completion-aware intervention` 时，帮助清理明显的局部几何、接触或局部执行 artifact。
2. 防止局部 artifact 污染对 `event completion` 的判断。
3. 在后续如果 completion 问题被写稳之后，再作为可恢复的局部修复支线。

## 核心论断

如果未来重新启用，Route-1 的可写 claim 应该是：

```text
local failure localization -> targeted non-MLLM correction -> measurable reduction of the same failure family
```

也就是说，它必须真正减少某类局部 failure，而不是只做看起来更平滑的 post-hoc cosmetic repair。

## 范围内

1. 被定位到某个 time segment 或 event unit 的 event omission 局部表现。
2. 错误的局部 body-part execution、contact error、foot sliding、jitter、penetration，或 implausible speed。
3. Counterfactual prompt pairs 只用于识别局部 failure，而不是作为 final evaluator。
4. 不依赖 MLLM captions 的 deterministic rules、geometry metrics、retrieval/reranking，或 model-internal trace signals。

## 范围外

1. 将 MLLM sidecar judging 作为 primary detector。
2. 将 manual local motion editing 作为证据。
3. 将它写成当前 MoDebug 的主线。
4. 将其扩写成新的 generator 故事。

## 为什么当前降级

最新观察说明，当前最值得优先写清楚的问题不是局部 artifact，而是：

1. `EventT2M` 在 event 粒度上略优；
2. 但它经常没把后续 events 做完；
3. 而旧指标看不见这个 gap。

所以，在这个阶段把精力投到局部 artifact taxonomy 上，优先级明显低于 `event completion gap`。

## 何时恢复这条线

只有在以下条件成立时，Route-1 才值得恢复为更强支线：

1. `event completion gap` 已经被正式写清楚。
2. 需要局部修复来配合 completion-aware intervention。
3. 可以证明某类局部 correction 不会破坏整体 event correctness。

## 下一步

当前不单独推进这条线。它只保留为 support note，后续如需恢复，应围绕“补全主线的局部修复需求”而不是独立扩张。
