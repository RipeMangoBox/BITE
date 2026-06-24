---
created: 2026-05-11T20:58:00+08:00
updated: 2026-05-13T00:20:00+08:00
title: "Route-3: MoDebug 基于 Failure-Caption Negative-Pair 的训练"
status: route_candidate
route_id: route-3
tags:
  - MoDebug
  - route_3
  - route_candidate
  - negative_pairs
  - failure_caption
  - training
  - contrastive_learning
related_notes:
  - "[[ideas/MoDebug/README]]"
  - "[[paperIDEAs/MoDebug/2026-05-11_modebug-route-overview]]"
---

# Route-3: MoDebug 基于 Failure-Caption Negative-Pair 的训练

> [!abstract] 当前版本定位
> Route-3 不再作为当前主线，而是保留为一个训练型备选支线。它当前最有意义的用途，不是泛化地学习所有 failure，而是当 `event completion gap` 被写稳之后，针对“后半段 event 没做完”这一类 failure 构造更密集的负监督。

## 当前角色

在最新 `gradio` 观察下，Route-3 的角色已经收缩：

1. 它不是当前第一主线。
2. 它不再承担“泛化 failure-caption training 方法论文”的主叙事。
3. 它只在一个前提下值得恢复：`event completion gap` 已经被正式定义，并且我们确实需要训练型 intervention 来减少后半段 unfinished / late-event drop。

## 核心对象

如果未来恢复，这条 Route 处理的对象应当更具体：

```yaml
instruction_text: "complex multi-event prompt"
generated_motion: "front events mostly correct, later events incomplete"
label: failure
negative_caption: "realizes the early event but fails to complete the later event"
missing_constraint: "late-event completion"
failure_type: incomplete_event_realization
positive_sibling: "candidate or reference motion that completes the full sequence"
```

也就是说，当前版本下，`Route-3` 的训练对象应优先围绕 **incomplete event realization**，而不是泛化到所有 possible failures。

## 为什么它暂时降级

因为当前最强的新事实不是“failure captions 很有潜力”，而是：

1. `EventT2M` 在局部 event 对齐上略优；
2. 但它经常没把后续 events 做完；
3. 当前 metrics 又对这种 failure 不够敏感。

在这个阶段，先把评价缺口和 usability 错位写清楚，比直接扩展训练型方法更重要。

## 如果恢复，这条线的合理用途

Route-3 未来恢复时，最合理的用途是：

1. 将 unfinished / late-event drop 样本构造成 structured negatives。
2. 训练一个 completion-aware scorer、reranker 或轻量 reward head。
3. 验证这种监督是否能在不破坏前半段对齐优势的情况下，提高后半段 completion。

## 当前不再保留的旧叙事

当前版本不再保留以下叙事作为主内容：

1. 将 failure-caption negative pairs 写成与当前主线并列的主故事。
2. 过早扩展到所有 failure families。
3. 在 `event completion gap` 还没正式写稳前，就把 Route-3 作为主要训练路线。

## 重新启用的条件

只有在以下条件满足后，Route-3 才值得恢复：

1. `event completion gap` 已被正式量化。
2. 旧指标与人审之间的错位已被写清楚。
3. 我们明确需要一个训练型 intervention，而不仅仅是评价协议或轻量 test-time 修补。

## 当前结论

Route-3 保留，但不是当前主线。它现在最好的定义是：

```text
completion-aware training branch, activated only after the event-completion gap is established.
```
