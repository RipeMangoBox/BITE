---
title: "StoryMotion Metric Computation IO"
status: active
tags:
  - StoryMotion
  - Motion_Generation
  - metric
  - evaluation
  - status/active
aliases:
  - StoryMotion-Metric-IO
source_notes:
  - "[[StoryMotion/current]]"
  - "[[version_family]]"
  - "[[StoryMotion-valid-metric-ledger]]"
  - "[[StoryMotion-iclr-reliability]]"
created: 2026-07-09T12:20:00+0800
updated: 2026-08-10T18:00:00+0800
---

# StoryMotion Metric Computation IO

> [!abstract] Current contract
> 本页只定义当前 StoryMotion v11 C0-LAT operational mainline 的输入、解码、指标和 loss 语义。活动 Stage2 只有 Direct-H、Direct-C 和 sequential Human→Camera 三种 mode；旧 joint-parallel／evolving-H solver、odd-even route schedule 与 joint-training HC 只属于历史 provenance，不在本页定义。正式数值与 artifact hash 只见 [[StoryMotion-valid-metric-ledger]]。

## 1. Active system boundary

StoryMotion 的研究对象是 **Human motion generation capability-preserving H–C generation**：先由 Human text 生成 Human motion，Camera branch 在 observed 或 generated Human latent 上生成 Camera trajectory。它与 Auteur 的问题不同：Auteur 从 Human trajectory／actor program 锚定 Camera trajectory，服务下游 ViGen；StoryMotion 的核心是 Human motion generation 及其能力保持下的 Human–Camera generation。

### 1.1 Shared v9 Stage1 owner

v11 C0-LAT 与 C0-GEO 共用完全相同的 v9 Pulp-only、non-causal Stage1 owner；只改变 Camera Stage2 objective。

| component | active contract | consequence |
| --- | --- | --- |
| Human input | normalized Pulp Human199 | train-only Pulp statistics；true-length mask |
| Camera input | official Camera14 | FOV、Human-relative center/distance、c2w rotation 6D、translation velocity |
| latent order | `Human128 + Interaction16 + Camera48` | `H128` 由 Human decoder 读取；`I16+C48` 参与 Camera/framing decode |
| tokenizer / decoder | exact v9 owner and owning `D_h/D_c/D_f` | Stage2 cache、checkpoint、statistics、decoder 必须 hash-match |
| causality | `is_causal=false` | 所有 StoryMotion Stage1/Stage2 constructor、load、eval 均 fail-closed |

Stage1 reconstruction 是 deterministic exact-valid-length round trip，不是 text-conditioned generation。normalized feature loss 只属于训练诊断；正式 ranking 使用 owning decoder 输出的 raw Human、Camera、projection 与 physical records。

### 1.2 Active Stage2 modes

| mode | Human source | Camera condition | official interpretation |
| --- | --- | --- | --- |
| Direct-H | Human text only | not sampled | free Human generation capability |
| Direct-C | observed Human latent | Camera text | Camera completion with observed Human |
| sequential Human→Camera | generated final Human from Direct-H | Camera text + frozen generated Human | v11 formal joint system; Human finishes before Camera sampling |

Human completion is Human-text-only. Camera completion consumes Human latent plus Camera text. C0-LAT does not train, evaluate, or gate on joint-parallel/evolving-H generation. A historical artifact may retain those names for provenance, but it is not an active v11 result.

## 2. Evaluation data and decoder IO

### 2.1 Full-cohort rule

Formal Stage2 rows use the complete Pulp pure-test cohort `N=4,053` and the complete materializable StoryMotion train cohort `162,760`; the ordered sample-ID hash, cache hashes, train-only statistics, Stage1 checkpoint and owning decoder are recorded per run in [[StoryMotion-valid-metric-ledger]]. Ordinary `N=512`, first-512 and short-screen generation rows are not active evidence. A swap, intervention, calibration or fixed-cohort mechanism probe may use a smaller cohort only when it is explicitly labeled `special diagnostic` and is not used for ranking.

### 2.2 Active code entry points

```text
linkedCodebases/StoryMotion/scripts/storymotion_official_full_eval.py
linkedCodebases/StoryMotion/experiments/stage2_v11_fixed_h_camera/model.py
linkedCodebases/StoryMotion/experiments/stage2_v11_fixed_h_camera/evaluate_pure4053.py
linkedCodebases/StoryMotion/experiments/stage2_protected_h_vimogen/model.py
linkedCodebases/StoryMotion/storymotion/per_sample_quality.py
```

Official callback implementations remain in the Pulp bridge:

```text
linked/PulpMotion/src/callbacks/human_metrics.py
linked/PulpMotion/src/callbacks/camera_metrics.py
linked/PulpMotion/src/callbacks/joint_metrics.py
linked/PulpMotion/src/metrics/*.py
```

The evaluator consumes `outputs["raw_input"]` as the reference and `outputs["raw_output"]` as the decoded prediction. `padding_mask` excludes padded frames. Human captions feed TMR; Camera captions and segment labels feed CLaTr and camera-caption callbacks; `proj_joints` is the official 2-D reference projection.

### 2.3 Feature and decode boundary

Camera14 translation velocity is cumulatively integrated after de-normalization. Its first-frame zero is a convention, not an absolute origin. Camera14 relative center is anchored to the decoded Human root; therefore Human root/yaw and Camera decode errors can couple in raw world-space metrics. `g_fpd`, projection PRDC fields and projection error are disabled by the current callback when emitted as zero and must not be interpreted as evidence.

## 3. Human metrics

Human raw output is transformed to the official Guo motion feature convention, normalized with the TMR train statistics, and encoded by the TMR motion/text encoder.

| display | machine key | computation | direction |
| --- | --- | --- | --- |
| FDTMR | `test/tmr/ftd` | Frechet distance between generated and reference TMR motion embeddings | lower |
| TMR | `test/tmr/tmr_score` | matched generated-motion/text cosine similarity, scaled by 100 and clamped at zero | higher |
| coverage / density / precision / recall | `test/tmr/{coverage,density,precision,recall}` | PRDC in TMR motion space | higher |
| R1/R2/R3 | `test/tmr/R1`, `R2`, `R3` | text-to-motion retrieval rank | higher |
| MM distance | `test/tmr/mm_distance` | matched text-motion distance | lower |

Paired Human geometry is a diagnostic, not a one-to-many hard gate. `human_global_mpjpe` is world joint error; `human_root_aligned_mpjpe` removes root translation but not heading; root ADE/FDE are pelvis trajectory errors. Integrated yaw is obtained by de-normalizing Human199 dim 3, cumulative summation and wrapped/unwrapped angle error.

## 4. Camera and framing metrics

Camera raw poses are converted to the official CLaTr coordinate convention, represented by rotation 6D plus normalized translation, and encoded with CLaTr motion/text features.

| display | machine key | computation | direction |
| --- | --- | --- | --- |
| FDCLaTr | `test/clatr/fcd` | Frechet distance between generated and reference CLaTr trajectory embeddings | lower |
| CLaTr | `test/clatr/clatr_score` | matched Camera trajectory/text cosine similarity, scaled by 100 | higher |
| CLaTr coverage / density / precision / recall | `test/clatr/{coverage,density,precision,recall}` | PRDC in CLaTr space | higher |
| Camera R1/R2/R3 | `test/clatr/R1`, `R2`, `R3` | text-to-camera retrieval rank | higher |
| caption P/R/F1 | `test/captions/{precision,recall,fscore}` | weighted Camera movement-segment classification after 25-fps segmentation/smoothing | higher |
| Camera ADE/FDE | records field | paired Camera center trajectory error | lower |
| rotation | records field | paired Camera rotation geodesic error | lower |
| r-FPD | `test/proj/r_fpd` | Frechet distance between generated-by-reprojection and reference 2-D joint projection features | lower |
| Out | `test/proj/outscreen` | valid-frame fraction with zero selected joints inside normalized screen bounds | lower |

`Out` is a generated-system zero-visible rate. It is not the Stage1 raw joint-out occupancy and not the paired Stage1 Out error; these fields must never be mixed.

## 5. Current Stage1 objective IO

The active v9 Stage1 owner uses masked exact-length reductions. Human reconstruction is normalized SmoothL1 plus temporal difference, decoded cumulative-yaw and root terms. Camera reconstruction is normalized Camera14 SmoothL1 plus temporal difference and framing target; `I16` energy is a Stage1 regularizer only. The active Stage1 phase schedule is owned by its run contract and is not a Stage2 generation metric.

The decoder receives `z_h[128]`, `z_hc[16]`, `z_c[48]` in the fixed order above. `D_h` cannot read Camera latent. `D_c` and `D_f` read the complete latent. Directly splicing Human/Camera latent chunks is invalid when the Interaction16 representation was produced from the complete pair.

## 6. Current v11 C0-LAT Stage2 objective IO

### 6.1 Human teacher

The Human flow is trained from Human text only to the frozen v9 Human `105K` teacher boundary. C0-LAT and C0-GEO never update this Human owner during Camera training. Direct-H and the Human part of sequential therefore share the exact Human output and the same Human metrics.

### 6.2 Camera-only shifted flow

C0-LAT is the operational **Camera-only latent-flow objective**. The Camera branch predicts a velocity for whitened Camera48+Interaction16-derived Camera64 representation while consuming a fixed Human latent and Camera text. It does not back-propagate into Human, does not use an old joint-training HC objective, and has no odd/even route alternation.

For Camera latent `C_0`, sample `u ~ Uniform(0,1)`, use the fixed shifted schedule
`sigma = 5u/(1+4u)`, draw Gaussian `epsilon`, and form:

```text
C_sigma = (1 - sigma) C_0 + sigma epsilon
v_star  = epsilon - C_0
L_LAT   = masked_mean((v_pred - v_star)^2)
```

The mask is the exact valid latent-frame mask. Per-sample valid-frame/channel normalization precedes batch averaging. The Camera text dropout and Human-context dropout in v11 are both zero; the sampler is therefore a fully conditional Camera velocity field. C0-GEO uses the same flow term and adds a frozen-owning-decoder decoded Camera14/framing auxiliary geometry term; C0-GEO is an audited alternate, not the operational parent.

The active v11 optimizer boundary is one Camera branch, one optimizer/EMA state, and Camera optimizer step `105K`; the historical HC/odd-even schedule is not part of this contract. Progress and loss scalars remain in run manifests/TensorBoard; only decoded formal metrics enter the ledger.

### 6.3 Optional Human-text embedding injection control

Human-text injection is an optional Stage2 control, not part of C0-LAT. HT-FILM, HT-HX and HT-DR add a zero-initialized adapter to a frozen C0-GEO Camera endpoint and inject the factual Human text embedding. The controls use the same pure-test contract and are not arbitrary Human/Camera editing.

The exact Direct-C and sequential metrics, complete fields, run identities and artifact/audit hashes are owned only by [[StoryMotion-valid-metric-ledger#Audited detail — original §3.13 v11 Human-text Camera fresh 105K pure4,053 formal audit]]. This page records the mechanism and interpretation only: the controls form a mixed Pareto, so none is promoted to C0-LAT.

## 7. Competition protocol slots

Run-specific numeric results are owned only by the [[StoryMotion-valid-metric-ledger#4.1 C0-LAT competition snapshot (pure4053 formal)]] and its detailed Stage2 tables in [[StoryMotion-valid-metric-ledger#4A. v9+ Stage2 audited detail tables]]. Numeric values live only in the ledger; this page deliberately records the capability and protocol boundary needed to interpret them, not a second leaderboard.

| system | dataset / cohort contract | mode | representation | owning decoder | numeric owner / comparability |
| --- | --- | --- | --- | --- | --- |
| StoryMotion v11 C0-LAT | complete Pulp pure-test contract | Direct-H, Direct-C, sequential Human→Camera | v9 Pulp-only non-causal Human128 + Interaction16 + Camera48 | exact v9 D_h/D_c/D_f | ledger pure4053 rows; current operational mainline |
| StoryMotion C0-GEO / HT controls | complete Pulp pure-test contract | Direct-C, sequential Human→Camera | same v9 owner; objective or optional Human-text adapter differs | exact v9 owning decoder | ledger pure4053 control rows; not single-variable superiority |
| PulpMotion native | same complete materializable available-data IDs | native joint | native paired representation and online Stage1 | native PulpMotion decoder | native-system boundary; no StoryMotion mode-equivalent ranking |
| Auteur | method-specific data and actor-program contract | Human trajectory / actor program → Camera trajectory for downstream ViGen | Auteur-native | Auteur-native | no matched numeric owner in this ledger; capability/protocol mismatch |
| CVPR26 Joint Synthesis / external baseline | method-specific dataset and cohort | method-native joint or pair synthesis | method-native | method-native | add numbers only after an exact full-cohort contract is audited |

Auteur anchors Camera trajectory from Human trajectory／actor program for downstream ViGen; StoryMotion generates Human motion and preserves the Human capability while generating Human–Camera motion. Different input, task and decoder contracts prohibit direct metric ranking.

## 8. Special diagnostics and exclusions

- `swap`, intervention, calibration, locality and fixed-cohort mechanism probes may retain smaller cohorts only under an explicit `special diagnostic` label. They do not enter the numeric competition table.
- Ordinary `N=512`, first-512, `N=64`, `N=128`, intermediate 30K snapshots and non-pure4053 generation screens are archived and do not support current ranking.
- Historical joint-parallel/evolving-H, old odd-even route, and old joint-training HC descriptions are archived implementation provenance. They are not current C0-LAT behavior.
- Human physical/kinematic fields are decoded diagnostics; contact/skate use an uncalibrated own-motion floor and are not ground-penetration validity scores.
- `g_fpd`, projection PRDC zero fields and disabled callback outputs are excluded from evidence.

## 9. JSON output layout

```json
{
  "task": "human | camera | sequential",
  "mode": "direct_h | direct_c | sequential",
  "run": {"checkpoint": "...", "checkpoint_sha256": "...", "is_causal": false},
  "data": {"split": "pure-test", "sample_count": 4053, "sample_ids_sha256": "..."},
  "sampler": {"name": "shifted-sigma-euler", "num_steps": 50, "seed": 17},
  "metrics": {"test/tmr/ftd": "...", "test/clatr/fcd": "..."},
  "paired_geometry": {"overall_mean": {}, "records": []},
  "decoded_human_physical": {"generated": {}, "dataset_reference": {}, "records": []}
}
```

The run contract remains the source of mutable provenance; the run directory owns logs, checkpoints and manifests; this page owns only reusable metric and IO semantics.
