---
title: "MLPA 实验关口"
created: 2026-05-20T00:00:00+08:00
updated: 2026-05-26T00:00:00+08:00
status: active
tags:
  - MLPA
  - experiments
  - gates
  - timestamping
  - rerank
---

# MLPA 实验关口

## Scaffold 契约

**Verification scaffold** 用于关口 1-5，必须能回到 motion-side 证据：

```text
text unit
candidate time window
body-part group
root / contact / velocity cue
order constraint
null / ambiguity
confidence
evidence trace
```

**Generation scaffold** 只用于关口 6，必须由前置 verification scaffold 支撑：

```text
event windows
body-part activity map
root / contact cue map
duration and order constraints
null / low-confidence regions
optional transition slots
```

失败条件：把 LLM prompt expansion、普通 action plan、完整 RVQ token 或最终 motion latent 直接叫作 MLPA scaffold。

## 关口 0：数据契约

目标：确认输入不是幻想出来的同步监督。

| 项目 | 通过条件 |
| --- | --- |
| ordered text units | 存在可复查的文本单元列表 |
| full motion | 原始 motion path 存在 |
| motion-side timestamp | 可以缺失；这是 MLPA 要预测的目标 |
| body-part phrase | 可解析或标记为 absent |
| evaluator role | human / VLM / automatic scorer 的角色明确记录 |
| split role | official train/test、disposable cache、diagnostic data 必须分开记录 |

当前数据约束：

1. Kimodo / SEED-Timeline 是 event-time supervision 主线。
2. HumanML3D/HumanML3D-E 只作 baseline-rich diagnostic、failure bank 和窗口级 Qwen pseudo-label 流程验证。
3. 不使用非官方数据切分做正式实验、验证或 pilot；小规模调试只能使用 official train split 的 disposable cache。

失败条件：把没有 verified timestamp 的文本单元列表当成 ground truth motion span；把 VLM 输出当 final evaluator；把非官方 split 或 disposable cache 写成 official split。

## 关口 1：Unit-To-Chunk Retrieval

问题：

```text
text unit 是否比 full prompt global score 更能找到对应 motion chunk？
```

Baselines：

1. full prompt global text-motion score；
2. equal-duration split；
3. sliding window + global score；
4. MLPA unit-to-chunk local score。

Metrics：

1. Recall@K over candidate chunks；
2. AUC for unit-present vs unit-absent chunks；
3. human cross-check agreement；
4. `null_mass` on unsupported units。

通过条件：MLPA local score 在 hard multi-unit prompts 上优于 full prompt baseline，并且错误集中可解释。

## 关口 2：Body-Part Phrase Localization

问题：

```text
body phrase / attribute 是否真的定位到对应 body-part token，而不是只靠动作类别先验？
```

Counterfactuals：

1. swap left / right；
2. mask upper / lower body；
3. replace hand / foot action；
4. remove contact cue。

Metrics：

1. part F1；
2. wrong-body-group score gap；
3. counterfactual locality delta；
4. ambiguity / null rate。

通过条件：对应部位得分高于 wrong body group，并在 swap / mask 后局部得分变化。

## 关口 3：Timestamping

问题：

```text
MLPA 是否能给 ordered text units 补 motion-side candidate windows？
```

Baselines：

1. equal-duration split；
2. root-velocity-only heuristic；
3. VLM full-video free caption；
4. MLPA candidate window + local verification。

Metrics：

1. Span IoU if human window exists；
2. text unit order consistency；
3. coverage；
4. ambiguity rate；
5. evidence trace completeness。

通过条件：MLPA 的 window 与 human check 更一致，且比 free-caption VLM 更少产生无证据断言。

## 关口 4：Frozen Rerank

问题：

```text
local correspondence score 能否改善 generated motion candidate selection？
```

Baselines：

1. random candidate；
2. global text-motion scorer；
3. LLM prompt expansion / planning rerank；
4. MLPA local correspondence rerank。

Metrics：

1. human pairwise preference；
2. instruction satisfaction score；
3. late-unit realization；
4. independent scorer cross-check；
5. diversity / naturalness guardrail。

通过条件：MLPA 不只提升自己的 score，也提升 human / independent instruction satisfaction。

## 关口 5：Verifier / Guidance Readiness

只有关口 1-4 至少两个通过，才进入轻量 coupling。此处目标是验证 verification scaffold 能否支持局部判断和推理时控制，不是训练新 generator。

允许的轻量形式：

1. candidate rerank；
2. inference-time guidance；
3. low-confidence chunk resampling；
4. small adapter；
5. masked cross-attention gating。

暂不允许：

1. 从零训练新 generator；
2. 把 VLM reward 当 final metric；
3. 在没有 timestamping 证据的情况下加 alignment loss；
4. 把 LLM prompt expansion 当作 scaffold 贡献。

MoLingo TPA-SAE 可以并行做 short-run ablation，但它不替代关口 1-4。其内部 cosine、TPA loss、PoseFix sidecar 分数只能记为 `diagnostic` 或 `side_signal`，不能作为 MLPA final evaluator。

## 关口 6：Pivot-First Generation

问题：

```text
先生成 pivot-level motion scaffold，再生成 fine-grained event / body-part motion，
是否比 single-stage text-to-motion 或 prompt expansion 更可靠？
```

前置条件：

1. 关口 1 或关口 3 证明 event-to-chunk localization 有正信号；
2. 关口 4 证明 MLPA local score 能改善 candidate selection；
3. 关口 5 证明 verifier / guidance 对 human 或 independent evaluator 有正信号；
4. 至少一个 body-part / contact cue probe 不是随机或全局动作类别先验。

Allowed forms：

1. pivot scaffold rerank；
2. pivot-conditioned local resampling；
3. masked chunk refinement；
4. residual / rectified-flow detail refiner；
5. small adapter over an existing generator。

Baselines：

1. single-stage text-to-motion；
2. LLM prompt expansion；
3. Event-T2M-style event conditioning without explicit correspondence verification；
4. MoMask-style motion-token coarse-to-fine without semantic pivot scaffold；
5. ActionPlan-style frame action plan if runnable / comparable。

Metrics：

1. event coverage and order correctness；
2. body-part locality score；
3. scaffold-final consistency；
4. human / independent instruction satisfaction；
5. naturalness / FID / diversity guardrail；
6. low-confidence chunk resampling gain。

通过条件：pivot-first generation 不只提升 MLPA 自己的 score，也提升 human / independent instruction satisfaction，并且 naturalness 与 diversity 不显著退化。

## 旁路关口：MoLingo TPA-SAE Ablation

问题：

```text
在不改 generator 的前提下，SAE latent 加入 Temporal-Phrase Alignment，
是否能带来可复查的 text-following 或 generation-side 正信号？
```

阶段：

1. 原始 SAE dry-run，记录 batch size、显存、iter time、loss finite。
2. Stage 1 clean proof：恢复 BABEL raw segment text / time，构造 oracle phrase/event anchors。
3. 跑四个 loss mode：`SL` 单 anchor、`WM` MoLingo 原始 token-local window mean、`MWM` 多 phrase 加权混合、`TPA-select` 选择式 phrase anchor。
4. Stage 2 extension：只有 `TPA-select > WM/MWM` 后，才试 T5 embedding-change pseudo segments、HumanML3D-E 或 PoseFix sidecar。
5. `TPA-PE` 只作为后续 PE 消融；使用 fixed sine PE，不使用 flow denoising timestep embedding。

Metrics：

1. Semantic Attribution Accuracy：latent token 是否归属到其中心帧所在 phrase/event segment；
2. Semantic Purity：top-1 vs top-2 phrase anchor margin、in-segment vs wrong-segment gap；
3. Traceability table：phrase/event coverage、null/background token、最常混淆 phrase pair；
4. Reconstruction guardrail：MPJPE / reconstruction loss / velocity loss；
5. downstream R-Precision / matching score 只作后续 side signal，不作为 Stage 1 主证据。

通过条件：`TPA-select` 不能只降低自身训练 loss；必须在 SAA、Semantic Purity 和 wrong-segment gap 上优于 `WM` 与 `MWM`，且 reconstruction guardrail 不显著退化。

失败条件：`TPA-select` 只赢 `SL` 但不赢 `WM/MWM`；raw BABEL segment 无法可靠恢复；phrase anchors 噪声导致 reconstruction 退化；PoseFix sidecar 被误用为动态 event GT。

## 共享元数据

每个关口记录：

```text
date
artifact_path
evaluator
protocol
motion_source
condition_pair
n/evaluable
coverage
role
used_for
limitations
```
