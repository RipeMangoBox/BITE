---
title: "MLPA 跨领域机制迁移笔记"
created: 2026-05-20T00:00:00+08:00
updated: 2026-05-20T00:00:00+08:00
status: active
tags:
  - MLPA
  - mechanism_transfer
  - cross_domain
---

# MLPA 跨领域机制迁移笔记

## 目的

本文件把跨领域启发压成可实现机制。每条启发必须满足：

```text
source mechanism -> motion translation -> measurable gate
```

只写类比、不产生 operator 或 gate 的内容，不进入主路线。

## 1. 3DGS：稀疏锚点与局部细化

### 来源机制

3DGS 的有用启发不是“text-motion 也有几何投影”，而是：

1. 显式局部 anchor；
2. anchor 有 coverage / visibility / uncertainty；
3. 低质量区域可 densify；
4. 全局目标通过大量局部 residual 优化。

### Motion 转译

```text
Gaussian point -> event / body / contact pivot
visibility -> event cue observable in a motion window
densification -> split an ambiguous long window into local candidate windows
local residual -> part / contact / trajectory correction cue
```

### 算子

维护 pivot set：

```text
p_i = {text_unit, body_part, time_window, cue_type, confidence, uncertainty, null_mass}
```

对高 uncertainty 的 pivot 做局部 window split 或补充 body cue，而不是重算全序列。

### 关口

在 timestamping 中比较：

1. no densification；
2. uncertainty-driven window split；
3. oracle human window。

如果 2 不明显优于 1，3DGS-style densification 不进入主方法。

## 2. Triplane：因子化交互平面

### 来源机制

Triplane 的可迁移点是把高维场拆成几个低维平面查询，而不是照搬 radiance field。

### Motion 转译

构造三类 plane：

```text
P_time_body[t, b]       # 哪个身体部位在何时活跃
P_time_unit[t, k]       # 哪个 text unit 在何时可能发生
P_body_attribute[b, a]  # 哪个部位支持哪个属性 / 接触 / 方向 cue
```

### 算子

unit-to-motion score 不直接用全局 cosine，而用：

```text
score(unit_k, window_n)
= f(P_time_unit[n, k], max_b P_time_body[n, b], P_body_attribute[b, attr(k)])
```

### 关口

比较：

1. global text-motion score；
2. time-unit plane only；
3. time-body + time-unit；
4. all three planes。

如果 body / attribute plane 不能提升 part phrase localization，则不写 triplane 启发为贡献。

## 3. MLLM / A.I.R.：查询感知证据获取

### 来源机制

A.I.R.-style 启发是 query-aware 采样和局部验证：不是平均看所有 frame，而是围绕 query 找证据。

### Motion 转译

```text
text_unit -> candidate windows -> local evidence check -> window refinement -> monotonic aggregation
```

避免循环依赖：候选 window 不能来自“已知 unit 在哪里”。可用来源：

1. sliding windows；
2. root velocity / direction change；
3. foot contact / pose energy；
4. body-part activation；
5. coarse retrieval score。

### 算子

VLM / MLLM 只接收：

```text
text_unit
candidate_window_render
root/contact/pose cue summary
```

输出：

```text
evidence | uncertainty | contradiction | limitation
```

### 关口

比较：

1. full-video free caption；
2. fixed sliding window local check；
3. query-aware candidate + local check。

如果 3 不能提升 human agreement 或减少 ambiguity，MLLM route 降级为 visualization aid。

## 4. Bottleneck / Dependence / Span-Level Alignment

### 来源机制

global condition 容易形成 bottleneck；alignment signal 下沉到 token / span 层更稳；错误依赖可以通过 counterfactual probe 暴露。

### Motion 转译

定义 wrong correspondence：

```text
unit_k aligns to wrong window
unit_k aligns to wrong body part
drop / replace unit still receives high local score
shuffle keeps same monotonic path
```

### 算子

使用 counterfactual locality：

```text
locality_delta =
score(unit_k, true_window, full)
- score(unit_k, same_window, drop_or_replace)
```

同时记录 `null_mass`，允许文本单元在 motion 中找不到对应。

### 关口

1. `drop` 后 target unit 的 local score 应下降。
2. `replace` 后 wrong attribute / body cue 不应继续高分。
3. `shuffle` 后 monotonic path 应变化。
4. `null_mass` 应集中在 unsupported / invisible units，而不是随机分布。
