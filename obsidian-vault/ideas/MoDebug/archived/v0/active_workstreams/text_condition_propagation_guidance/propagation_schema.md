---
title: "MoDebug 文本条件传播记录字段"
created: 2026-05-20T00:00:00+08:00
updated: 2026-05-20T00:00:00+08:00
status: active
tags:
  - MoDebug
  - propagation_schema
  - text_condition_propagation
---

# MoDebug 文本条件传播记录字段

## 分析单元

MoDebug 允许多种 text unit：

| 文本单元 | 示例 | 是否必需 |
| --- | --- | --- |
| full prompt | full caption 或 instruction | 是 |
| phrase | verb phrase、body phrase、object phrase | 可选 |
| attribute | direction、count、speed、style、body part | 可选 |
| token span | text token range | 可选 |
| semantic step | 可独立解释的动作步骤 | 可选 |
| planner step | LLM-normalized sub-instruction | 可选 |

所有实验记录使用通用字段 `text_unit_type`，并在 `text_unit` 中保存具体内容。

## 必填字段

```text
sample_id
model
condition_id
text_unit_type
text_unit
perturbation_type
condition_pair
trace_signal
trace_layer_or_step
motion_artifact_path
role
used_for
limitations
```

## 插件式评估字段

full-text / full-motion paired evaluation 需要记录：

```text
prompt_id
baseline_model
baseline_condition
modebug_condition
seed
length_budget
candidate_budget
baseline_motion_path
modebug_motion_path
paired_evaluator
paired_protocol
paired_preference
quality_guardrail
role
limitations
```

其中 `baseline_condition` 通常是 `B`，`modebug_condition` 通常是 `B+MoDebug`。如果是 rerank 型插件，`candidate_budget` 与 candidate pool provenance 必须记录。

## Motion-Side Grounding 扩展字段

只有在并行 motion-side grounding 路线通过可靠性审计，并用于训练或监督 cross-check 时才需要这些字段：

```text
segment_start
segment_end
core_start
core_end
transition_before
transition_after
start_state_summary
end_state_summary
prefix_context_path
grounding_evaluator
grounding_confidence
```

其中 `segment_*` 表示候选片段范围，`core_*` 表示高置信文本单元证据范围，transition 字段表示过渡或不确定区域。训练时应对 transition 与核心动作使用不同监督权重。

## 传播信号

| 信号 | 含义 | 适用模型 |
| --- | --- | --- |
| `embedding_delta` | 文本侧可分性 | 全部 |
| `projection_delta` | 条件投影响应 | 有 condition projection 的模型 |
| `attention_delta` | 文本到 motion 或 condition attention 响应 | attention-based generators |
| `hidden_delta` | 层间传播变化 | transformer generators |
| `logit_delta` | motion-token 分布变化 | token generators |
| `confidence_delta` | mask 或 token confidence 变化 | masked generators |
| `trajectory_delta` | denoising / remasking path 变化 | diffusion 或 masked generators |
| `rerank_score` | candidate-level diagnostic score | 有候选输出的模型 |

## 扰动类型

| 扰动 | 用途 |
| --- | --- |
| `drop_phrase` | omission sensitivity |
| `replace_attribute` | direction / count / body / style binding |
| `shuffle_order` | chronology sensitivity |
| `compress_prompt` | global prompt bottleneck |
| `expand_prompt` | prompt packing / planner effect |
| `paraphrase` | lexical robustness |
| `negative_prompt` | contrastive separation |

## Motion 侧标签

Decoded motion label 是交叉检查，不是主分析单元。

允许标签：

```text
visible
weak_visible
absent
ambiguous
quality_degraded
not_judged
```

每条标签都要记录 evaluator、protocol、artifact_path、role 与 limitations。
