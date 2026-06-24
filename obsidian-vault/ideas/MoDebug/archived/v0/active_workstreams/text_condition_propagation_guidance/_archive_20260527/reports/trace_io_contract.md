---
title: "MoDebug Trace IO Contract 20260527"
created: 2026-05-27T00:00:00+08:00
updated: 2026-05-27T22:30:00+08:00
status: active
tags:
  - MoDebug
  - trace_schema
  - f_signal
---

# MoDebug Trace IO Contract 20260527

## 适用范围

本 contract 是 worker agents 的只读共享协议。变更请求写入各 agent 自己的 `change_requests.md`。

Reference plan:

[[2026-05-27_f_signal_parallel_implementation_plan|f-Signal 并行实现计划]]

当前 formal trace 使用该 contract 记录 `forward` 与 `delta` 内部特征张量。该 contract 不定义 final evaluator。

## Forward NPZ

Required keys:

```text
signal
valid_mask
meta_json
axis_names_json
```

`signal` 是模型内部 trace 张量，例如 `token_logits` 或 `hidden_state`。它不是人体关节位置、关节旋转或 motion trajectory。

`valid_mask` 可以与 `signal.shape` 完全相同，也可以是 `signal.shape[:-1]` 形式的 row mask，对最后一维 feature / vocabulary / embedding axis 做行级掩码。consumer 应在最后补一个 singleton axis 后再进行 broadcast。

Optional keys:

```text
logits
probabilities
hidden_states
attention_context
condition_projection
confidence
```

`meta_json` 是 UTF-8 JSON string，至少包含：

```json
{
  "run_id": "20260527_183000_agent_x_model_scope",
  "sample_id": "original100_000",
  "model": "momask_original",
  "model_family": "clip_discrete",
  "condition_id": "text",
  "condition_text": "...",
  "z_kind": "mask_iteration",
  "z_id": "iter_03",
  "f_name": "token_logits",
  "f_space": "vocab_logits",
  "role": "diagnostic",
  "limitations": "Internal trace only; not a final evaluator."
}
```

## Delta NPZ

Required keys:

```text
delta
metric_value
meta_json
```

`delta` array 是 `signal_text - signal_comparison`，计算前需要完成 shape validation 和可选 masking。`metric_value` 是标量，除非 `meta_json` 明确记录 localized metric。

注意：`delta` 是内部特征差值，不是 motion error、joint error 或 MPJPE。

## Manifest JSONL

Forward manifest required fields:

```text
run_id
sample_id
model
model_family
condition_id
condition_text
paired_condition_id
z_kind
z_id
f_name
f_space
forward_npz_path
motion_artifact_path
role
used_for
limitations
```

Delta manifest required fields:

```text
run_id
sample_id
model
condition_pair
z_kind
z_id
f_name
metric_name
metric_value
delta_npz_path
role
used_for
limitations
```

## Path Roots

Remote staging root:

```text
/data/public/ripemangobox/Motion/EventT2M-codes/artifacts/modebug/text_condition_propagation_20260527/
```

Local fetched root:

```text
/data/Life Me/ResearchWY Vault/artifacts/remote/4090/modebug_text_condition_propagation_20260527/
```

Formal artifact root:

```text
/data/Life Me/ResearchWY Vault/artifacts/remote/4090/modebug_text_condition_propagation_20260527/text_condition_propagation_20260527/
```

Run directory format:

```text
YYYYMMDD_HHMMSS_{agent}_{model_or_scope}
```

## Role Boundary

所有 trace outputs 默认都是 `diagnostic`，除非后续文档明确记录 evaluator、protocol、held-out split、coverage 和 limitations，并足以支持更强 role。

当前输出不是 final evaluator，不是 full benchmark，也不是 formal ordering evidence。`issue_rows=0` 只表示记录级校验通过，不表示 motion quality 或语义质量通过。
