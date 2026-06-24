---
## created: 2026-04-06
updated: 2026-04-09T18:40
source:
  - /home/ripemangobox/Coding/Github/Motion/EventT2M-codes-main/paperIDEAs/TAMR/2026-04-05_tamr-motionpatches-harness-design.md
  - /home/ripemangobox/Coding/Github/Motion/MotionPatches-main/checkpoints/pretrained/HumanML3D/contrastive_metrics/TMR-normal.yaml
  - /home/ripemangobox/Coding/Github/Motion/MotionPatches-main/checkpoints/pretrained/HumanML3D/contrastive_metrics/TMR-nsim.yaml
  - /home/ripemangobox/Coding/Github/Motion/MotionPatches-main/checkpoints/pretrained/HumanML3D/contrastive_metrics/EVT-normal.yaml
  - /home/ripemangobox/Coding/Github/Motion/MotionPatches-main/checkpoints/pretrained/HumanML3D/contrastive_metrics/EVT-nsim.yaml
  - /home/ripemangobox/Coding/Github/Motion/MotionPatches-main/checkpoints/pretrained/HumanML3D/generation_metrics/EVT-native_normal.yaml
  - /home/ripemangobox/Coding/Github/Motion/MotionPatches-main/checkpoints/stage1_mp_rule/HumanML3D/contrastive_metrics/TMR-normal.yaml
  - /home/ripemangobox/Coding/Github/Motion/MotionPatches-main/checkpoints/stage1_mp_rule/HumanML3D/contrastive_metrics/TMR-nsim.yaml
  - /home/ripemangobox/Coding/Github/Motion/MotionPatches-main/checkpoints/stage1_mp_rule/HumanML3D/contrastive_metrics/EVT-normal.yaml
  - /home/ripemangobox/Coding/Github/Motion/MotionPatches-main/checkpoints/stage1_mp_rule/HumanML3D/contrastive_metrics/EVT-nsim.yaml
  - /home/ripemangobox/Coding/Github/Motion/MotionPatches-main/checkpoints/stage1_mp_rule/HumanML3D/generation_metrics/EVT-native_normal.yaml
  - /home/ripemangobox/Coding/Github/Motion/MotionPatches-main/checkpoints/stage1_mp_gt/HumanML3D/contrastive_metrics/TMR-normal.yaml
  - /home/ripemangobox/Coding/Github/Motion/MotionPatches-main/checkpoints/stage1_mp_gt/HumanML3D/contrastive_metrics/TMR-nsim.yaml
  - /home/ripemangobox/Coding/Github/Motion/MotionPatches-main/checkpoints/stage1_mp_gt/HumanML3D/contrastive_metrics/EVT-normal.yaml
  - /home/ripemangobox/Coding/Github/Motion/MotionPatches-main/checkpoints/stage1_mp_gt/HumanML3D/contrastive_metrics/EVT-nsim.yaml
  - /home/ripemangobox/Coding/Github/Motion/MotionPatches-main/checkpoints/stage1_mp_gt/HumanML3D/generation_metrics/EVT-native_normal.yaml
  - /home/ripemangobox/Coding/Github/Motion/MotionPatches-main/temporal_utils.py
  - /home/ripemangobox/Coding/Github/Motion/MotionPatches-main/scripts/train.py
tags:
  - tamr
  - motionpatches
  - stage1
  - closure
status: summary
title: "TAMR MotionPatches Stage-1 Closure: Baseline vs Rule vs GT"

# TAMR MotionPatches Stage-1 Closure: Baseline vs Rule vs GT

## 1. Executive Summary

本轮闭环回答四个问题：

1. `MP baseline / MP + rule / MP + GT` 三组在统一口径下分别表现如何；
2. generation proxy 的过滤统计是否同口径；
3. event 集成相对原始 MotionPatches 是正向还是方向性作用；
4. 是否达到 canonical design 中 `Stage 0 / Stage 1` 的目标，以及是否进入 `Stage 2`。

结论先写在前面：

- **Stage 0 已达成**：baseline、strict fair retrieval、temporal eval、generation proxy export 都已跑通并固定输出。
- **Stage 1 部分达成**：event 集成对 temporal retrieval 是明确正向；但对标准 retrieval 与 generation proxy 仍是 trade-off，`MP + GT` 也还没有稳定压过 `MP + rule`。
- **是否进入 Stage 2**：可以，而且当前建议直接固定沿 `HumanML3D-E-only` GT event 主线推进 event-aware retrieval 与评测/回归支架验证。

这也意味着：

- 当前 canonical 口径已经更正为：后续实验固定沿 `HumanML3D-E` GT event 主线推进；
- Stage-1 的结论已经足以固定这条 GT event 主线。

---
## 2. Unified Comparison Tables

### 2.1 Retrieval: `TMR-normal`


| Setting  | R@1  | R@5   | MedR |
| -------- | ---- | ----- | ---- |
| baseline | 7.30 | 25.75 | 19   |
| rule     | 7.62 | 25.41 | 18   |
| gt       | 6.93 | 26.80 | 18   |


相对 baseline：

- rule: `R@1 +0.32`, `R@5 -0.34`, `MedR -1`
- gt: `R@1 -0.37`, `R@5 +1.05`, `MedR -1`

### 2.2 Retrieval: `TMR-nsim`


| Setting  | R@1   | R@5   | MedR |
| -------- | ----- | ----- | ---- |
| baseline | 51.00 | 87.00 | 1    |
| rule     | 48.00 | 86.00 | 2    |
| gt       | 55.00 | 86.00 | 1    |


相对 baseline：

- rule: `R@1 -3.00`, `R@5 -1.00`, `MedR +1`
- gt: `R@1 +4.00`, `R@5 -1.00`, `MedR 0`

### 2.3 Temporal: `EVT-normal`


| Setting  | CAR@1 | CAR@5 | CAR@10 | TAR@1 | TAR@5 | TAR@10 |
| -------- | ----- | ----- | ------ | ----- | ----- | ------ |
| baseline | 7.06  | 22.85 | 31.74  | 3.19  | 10.72 | 15.37  |
| rule     | 9.50  | 30.11 | 43.02  | 5.27  | 16.86 | 25.05  |
| gt       | 8.16  | 30.72 | 42.45  | 4.74  | 17.77 | 24.98  |


相对 baseline：

- rule: `CAR@1 +2.44`, `TAR@5 +6.14`, `TAR@10 +9.68`
- gt: `CAR@1 +1.10`, `TAR@5 +7.05`, `TAR@10 +9.61`

### 2.4 Temporal: `EVT-nsim`


| Setting  | CAR@1 | CAR@5 | CAR@10 | TAR@1 | TAR@5 | TAR@10 |
| -------- | ----- | ----- | ------ | ----- | ----- | ------ |
| baseline | 45.83 | 75.00 | 75.00  | 17.00 | 31.00 | 32.00  |
| rule     | 54.17 | 91.67 | 93.75  | 27.00 | 48.00 | 51.00  |
| gt       | 62.50 | 89.58 | 93.75  | 36.00 | 50.00 | 51.00  |


相对 baseline：

- rule: `CAR@1 +8.34`, `TAR@5 +17.00`, `TAR@10 +19.00`
- gt: `CAR@1 +16.67`, `TAR@5 +19.00`, `TAR@10 +19.00`

### 2.5 Generation Proxy: `EVT-native_normal`

说明：

- `Matching_score` 越低越好；
- `R_precision_top_k` 越高越好；
- `FID` 越低越好；
- `Diversity` 只做分布参考；
- 当前仍是 retrieval-top1 proxy，不是 diffusion generator。


| Setting  | Matching | R@1    | R@2    | R@3    | FID    | Diversity | num_eval_queries |
| -------- | -------- | ------ | ------ | ------ | ------ | --------- | ---------------- |
| baseline | 2.8623   | 0.5458 | 0.7355 | 0.8278 | 0.0508 | 9.5927    | 4146             |
| rule     | 2.7907   | 0.5439 | 0.7373 | 0.8274 | 0.0609 | 9.4977    | 4110             |
| gt       | 2.8916   | 0.5291 | 0.7202 | 0.8125 | 0.0470 | 9.6323    | 4126             |


相对 baseline：

- rule: `Matching -0.0716`，`R@1 -0.0018`，`FID +0.0101`
- gt: `Matching +0.0293`，`R@1 -0.0167`，`FID -0.0038`

对两条新分支的直接对比：

- rule 优于 gt：`Matching`、`R@1/R@2/R@3`
- gt 优于 rule：`FID`

---
## 3. Generation Proxy Filtering Statistics

过滤统计按 `scripts/test.py::compute_eventt2m_generation_metrics` 的真实顺序复放：

1. 先检查 `new_joint_vecs/<keyid>.npy` 是否存在且维度合法；
2. 再检查 `eval_len >= min_motion_length(40)`；
3. 最后检查 caption tokens 是否为空。

### 3.1 过滤结果


| Setting  | total_strict_queries | kept | filtered_total | filtered_length | filtered_missing_tokens | filtered_missing_file | filtered_invalid_shape |
| -------- | -------------------- | ---- | -------------- | --------------- | ----------------------- | --------------------- | ---------------------- |
| baseline | 4384                 | 4146 | 238            | 238             | 0                       | 0                     | 0                      |
| rule     | 4384                 | 4110 | 274            | 274             | 0                       | 0                     | 0                      |
| gt       | 4384                 | 4126 | 258            | 258             | 0                       | 0                     | 0                      |


### 3.2 过滤口径判断

结论：

- **过滤规则完全同口径**；
- **rule 与 gt 的差异不是缺文件、缺 token 或 shape 错误造成的**；
- 两者唯一差异来自 **retrieval top1 不同，进而导致 `min(gt_len, pred_len, 196)` 在部分 query 上低于 `40`**；
- gt 比 rule 多保留了 `16` 个 query，因此 generation proxy 的对比不应被解读为“数据脏导致的假差异”，而应视为 **模型检索结果带来的有效评测子集差异**。

这也意味着：

- 当前 trade-off 不是 I/O 问题；
- 是 stage-1 event integration 本身对 retrieval target selection 的真实影响。

---
## 4. What Changed Relative to Original MotionPatches

### 4.1 Retrieval

相对原始 MotionPatches baseline：

- **rule branch**
  - `TMR-normal R@1` 小幅提升；
  - `TMR-nsim R@1` 明显下降；
  - temporal 指标大幅提升。
- **gt branch**
  - `TMR-normal R@1` 小幅下降，但 `R@5` 更高；
  - `TMR-nsim R@1` 明显提升；
  - temporal 指标同样大幅提升，且在 `nsim` 上通常优于 rule。

因此：

- 从 **temporal-aware retrieval** 角度看，event 集成是明显正向；
- 从 **标准 semantic retrieval** 角度看，event 集成是方向性重分配，不是无条件增益。

### 4.2 Generation Proxy

相对原始 MotionPatches baseline：

- baseline 实际上保住了最稳的 `R_precision_top_1`；
- rule 主要把指标推向更好的 `Matching_score`，但 `FID` 变差；
- gt 主要把指标推向更好的 `FID`，但 `Matching/R_precision` 变差。

因此：

- event 集成对 generation proxy **不是单调正向**；
- 它更像是把系统推向了两种不同偏好：
  - rule: 更偏 text-motion matching
  - gt: 更偏 distribution/FID

---
## 5. Is Event Integration Positive or Directional?

如果用一句话总结：

> event integration 对 MotionPatches 的主效应是“显著增强 temporal following”，而不是“全面提升所有 retrieval/generation 指标”。

更细一点：

- **对 temporal retrieval**：明确正向。
- **对 strict retrieval**：方向性，有 protocol trade-off。
- **对 generation proxy**：方向性，有 `Matching/R_precision` 与 `FID` trade-off。

所以本轮最稳妥的判断不是“event 集成已经全面成功”，而是：

> event 集成已经证明自己是 TAMR 的有效时序注入方向，但它还没有把所有下游指标一起推高。

---
## 6. Stage-0 / Stage-1 Goal Check Against Canonical Design

### 6.1 Stage 0

canonical 要求：

1. 保留 MotionPatches 原生指标；
2. 保留 strict TMR-aligned fair comparison；
3. 固定 temporal eval 评测支架。

本地状态：

- MP baseline 已稳定复现；
- `TMR-`* retrieval 输出已固定；
- `EVT-*` temporal 输出已固定；
- `EVT-native_normal` generation proxy 已接入并可导出。

结论：

> **Stage 0 已达成。**

### 6.2 Stage 1

canonical 要求：

1. 不显著伤害标准 retrieval；
2. temporal retrieval 优于 `MP baseline`；
3. `MP + GT events` 至少应优于 `MP + rule events`。

本地状态：

- 条件 1：**基本达成**
  - normal retrieval 没有灾难性下降；
  - nsim 上出现 rule/gt 分化，但仍属于可分析范围，而不是训练失控。
- 条件 2：**明确达成**
  - rule 与 gt 在 `EVT-normal`、`EVT-nsim` 上都显著优于 baseline。
- 条件 3：**尚未达成**
  - gt 在 `TMR-nsim`、`EVT-nsim`、`FID` 更强；
