---
title: "MoDebug 文本条件传播实验关口"
created: 2026-05-20T00:00:00+08:00
updated: 2026-05-20T00:00:00+08:00
status: active
tags:
  - MoDebug
  - experimental_gates
  - text_condition_propagation
---

# MoDebug 文本条件传播实验关口

## 关口 0：Full-Text / Full-Motion 插件评估

目标：在没有 motion-side event grounding 的条件下，先验证 MoDebug 能否增幅现有 baseline。

最小记录：

1. full text prompt；
2. baseline full motion artifact；
3. baseline+MoDebug full motion artifact；
4. seed / length / candidate budget；
5. paired human preference；
6. motion quality guardrail。

通过条件：`baseline+MoDebug` 在 paired full-motion comparison 中优于 baseline，且质量护栏没有明显下降。

## 关口 1：传播信号可导出

目标：确认至少两个 pretrained generator 能导出 text-condition propagation trace。

最小记录：

1. text embedding / condition embedding；
2. condition projection 或 cross-attention input；
3. hidden-state / attention / confidence / logits over generation steps；
4. decoded motion artifact for cross-check。

通过条件：每个保留模型至少有两层 trace，例如 `embedding_delta + logit_delta` 或 `projection_delta + confidence_delta`。

## 关口 2：扰动集合

目标：构造覆盖多粒度文本条件的 text perturbations。

扰动集合：

1. `drop_phrase`；
2. `replace_attribute`；
3. `shuffle_order`；
4. `compress_prompt`；
5. `expand_prompt`；
6. `paraphrase`。

通过条件：每个 sample 至少有 full prompt + 2 类 perturbation；每条 perturbation 记录 `text_unit_type` 和 `condition_pair`。

## 关口 3：传播 signature

目标：找到稳定的 propagation failure signature。

候选 signature：

| Signature | 含义 |
| --- | --- |
| `projection_collapse` | 文本侧可分，但 projection 后不可分 |
| `layer_decay` | 关键 phrase / attribute signal 随层深或步骤衰减 |
| `wrong_region_binding` | signal 进入错误 time / body / token region |
| `token_prior_override` | generator prior 无视 text perturbation |
| `prompt_packing_gain` | expanded / planner-normalized prompt 改善 propagation |

通过条件：至少一种 signature 在两个模型、两个 prompt buckets 或多个 seeds 中复现。

## 关口 4：引导目标

目标：把 signature 转成轻量 guidance。

候选 guidance：

1. phrase / attribute condition reweighting；
2. projection normalization / gating；
3. attention bias；
4. token-level rerank；
5. sampling or remask schedule adjustment；
6. prompt packing / planner-normalized prompt。

通过条件：guidance target 与 signature 一一对应，并能在 trace 上产生预期变化。

## 关口 5：输出交叉检查

目标：确认 guidance 改善 output，而不是只改 trace score。

交叉检查：

1. independent motion quality metric；
2. instruction-following human check；
3. VLM / PoseFix / geometry diagnostic where applicable；
4. diversity / naturalness guardrail。

通过条件：guided output 在 instruction-following 上改善，且不明显损害 motion quality。
