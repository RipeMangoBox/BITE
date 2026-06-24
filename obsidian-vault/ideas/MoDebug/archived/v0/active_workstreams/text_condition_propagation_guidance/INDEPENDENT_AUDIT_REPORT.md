---
title: "MoDebug Independent Audit Report"
created: 2026-05-29
status: final
role: third-party-review
---

# MoDebug Independent Audit Report

## Verdict: **PARTIALLY VALID**

原始分析有真实信号，但多处统计口径、因果推断和机制优先级需要降级。Holm 校正后仅 1/16 检验显著；valid_ratio 问题的定性需要修正；3/5 机制当前仅为 diagnostic，不应进入模型改动。

---

## 1. Data Integrity

| 项目 | 值 |
|------|-----|
| Raw rows (`delta_tensor_summary.json`) | 408 |
| Unique (model, sample_id) | 400 |
| Duplicates | 8 rows — 每个 baseline 的 pilot case 在原始 `sample_level_cases_pilot_8.json` 和新 `sample_level_cases_full.json` 中各出现一次，相同 outcome |
| Old CSV (`/tmp/sample_features_387.csv`) | 387 rows, 缺失 21 MotionGPT success rows |
| Dedup 后每模型 | MotionGPT 100 (86S/14F), MoLingo 100 (88S/12F), MoMask 100 (77S/23F), MoGenTS 100 (79S/21F) |

**Critical Issue 1**: `/tmp/sample_features_387.csv` 不应再被使用。它漏掉 21 个 MotionGPT success rows，已有下游分析（outcome_classifier）建立在此口径上。

**Resolution**: 建立 canonical 表：`raw_408` + `dedup_400`。所有统计从 `dedup_400` 生成。

---

## 2. Statistical Re-analysis (Dedup N=400)

### 2.1 Per-model Success vs Failure: Mann-Whitney U + Holm Correction

16 tests (4 models × 4 metrics). Negative d = failure > success.

| Model | Metric | p_raw | p_holm | Cohen's d | Sig(Holm) |
|-------|--------|-------|--------|-----------|-----------|
| MotionGPT | metric_value | 0.3608 | 1.0000 | -0.165 | ns |
| MotionGPT | delta_abs_max | 0.3504 | 1.0000 | -0.236 | ns |
| MotionGPT | delta_std | 0.3660 | 1.0000 | -0.161 | ns |
| MotionGPT | delta_mean | 0.6335 | 1.0000 | +0.114 | ns |
| **MoLingo** | **metric_value** | **0.0020** | **0.0324** | **-1.129** | **SIG** |
| MoLingo | delta_abs_max | 0.0053 | 0.0791 | -0.970 | ns |
| MoLingo | delta_std | 0.0838 | 0.8382 | -0.564 | ns |
| MoLingo | delta_mean | 0.0106 | 0.1433 | -0.681 | ns |
| MoMask | metric_value | 0.1371 | 1.0000 | -0.456 | ns |
| MoMask | delta_abs_max | 0.8667 | 1.0000 | +0.015 | ns |
| MoMask | delta_std | 0.9771 | 1.0000 | +0.085 | ns |
| MoMask | delta_mean | 0.0102 | 0.1433 | -0.620 | ns |
| MoGenTS | metric_value | 0.2182 | 1.0000 | -0.098 | ns |
| MoGenTS | delta_abs_max | 0.0501 | 0.5552 | -0.389 | ns |
| MoGenTS | delta_std | 0.4904 | 1.0000 | -0.273 | ns |
| MoGenTS | delta_mean | 0.0463 | 0.5552 | -0.568 | ns |

**Critical Issue 2**: 原始报告声称"MoLingo 所有指标显著"、"MoMask delta_mean 显著"、"MoGenTS delta_mean 显著"。Holm 校正后，**仅 MoLingo metric_value 存活** (p_holm=0.0324)。其余 15/16 检验不显著。

**Robust finding**: MoLingo metric_value 区分 success/failure 是唯一经多重比较校正后仍成立的结论。

**Claims to downgrade**: 
- ~~"MoLingo 唯一强信号 across all metrics"~~ → 仅 metric_value 成立
- ~~"MoMask delta_mean 显著"~~ → Holm 校正后 ns
- ~~"MoGenTS delta_mean 显著"~~ → Holm 校正后 ns
- ~~"delta_mean 是跨模型最一致的信号"~~ → 仅 raw p 下成立，Holm 校正后无模型通过

### 2.2 Effect Sizes

即使不考虑显著性，效应量排名：
- MoLingo metric_value: d=-1.13 (large)
- MoLingo delta_abs_max: d=-0.97 (large, but ns after Holm)
- MoLingo delta_mean: d=-0.68 (medium)
- MoMask delta_mean: d=-0.62 (medium)
- MoGenTS delta_mean: d=-0.57 (medium)
- 其余: |d| < 0.46 (small or negligible)

---

## 3. Confound / Prompt Analysis

### 3.1 MoLingo valid_ratio

| Correlation | r | p |
|-------------|---|---|
| valid_ratio ~ outcome | +0.111 | 0.270 |
| valid_ratio ~ metric_value | +0.646 | <0.001 |
| metric_value ~ outcome | +0.283 | 0.003 |
| **partial r (metric_value ~ outcome \| valid_ratio)** | **+0.279** | — |

**Revised verdict**: valid_ratio 不是简单 confound（与 outcome 无显著相关），但与 metric_value 强相关 (r=0.646)。它是 **mediator/collider**：更长的 motion → 更多 valid tokens → 更大 surface area for delta → 更大 metric。Partial r 保持 0.279，说明 metric_value 携带独立于 valid_ratio 的信息。

**Critical Issue 3**: 原始报告从 "不是 confound" 跳到了 "可放心使用 metric_value"。正确表述应为：**metric_value 携带独立于 valid_ratio 的信号，但 valid_ratio 解释了 metric_value 41.7% 的方差 (r²=0.417)。metric_value 作为单一决策阈值时，必须显式控制 valid_ratio 的影响（如在 valid_ratio tertile 内分别设阈值）。**

### 3.2 Prompt-Delta

| Model | prompt_length ~ metric_value r | p |
|-------|-------------------------------|----|
| MotionGPT | -0.095 | 0.342 |
| **MoLingo** | **+0.453** | **<0.001** |
| **MoMask** | **+0.279** | **0.004** |
| MoGenTS | +0.162 | 0.104 |
| **POOLED** | **+0.109** | **0.029** |

**Robust finding**: Pooled 相关很弱 (r=0.109)，但 MoLingo (r=0.453) 和 MoMask (r=0.279) 内部有中等 prompt_length-delta 相关。Prompt complexity 预测 failure 的机制不是通过 delta 幅度：它是 **difficulty proxy**，而非 causal mechanism。

**Critical Issue 4**: 原始报告说 "failure 机制 ≠ delta 饱和 → attention collapse"。这是两跳推断：(1) prompt 复杂 → failure, (2) prompt 复杂 ≠ delta 大, (3) 所以 failure 来自 attention collapse。步骤 (3) 无直接证据。需要 cross-attention map 分析或其他机制证据才能支持。

---

## 4. Mechanism Status

| 机制 | 判定 | 理由 |
|------|------|------|
| M1: Event-level Injection | **diagnostic-targeted** | missing_subaction 是真实 failure mode，但当前 scalar delta 不能证明 event-level 分解有效。需先做 M1 targeted test (full vs event prompts vs recomposed)，比较 delta temporal concentration。P1。 |
| M2: Sparse Routing | **diagnostic-only** | 理论合理，但当前无 slot concentration / Gini / selectivity proxy 数据。必须先提取这些 proxy 才能进入实验。不能直接做模型改动。 |
| M3: Temporal Consistency | **diagnostic-only** | 同样缺 temporal_delta_std / temporal_diff 与 trajectory_error 的关系证据。必须先提取 proxy。 |
| M4: Length Normalization | **diagnostic-supported** | 有 MoLingo r=0.453、MoMask r=0.279 的 length-delta 诊断信号。但 **post-hoc rescaling 只能证明 delta 分布变化，不能证明 motion quality 改善**。必须重新 forward 并做 human eval。若仅 post-hoc rescale，必须标注 simulation-only。P0 作为诊断实验，P1 作为生成验证。 |
| M5: FlowEdit Refinement | **not-supported-yet** | 当前无任何直接证据。不应作为近期主线。P2。 |

---

## 5. Convergence Roadmap Review

提出的 Phase 0-3 路线总体合理，以下修改：

### Phase 0（立即）
- 废弃 `/tmp/sample_features_387.csv`
- 建立 canonical 表：`raw_408` + `dedup_400`
- 所有下游统计从 canonical 表重新生成
- annotation provenance 记录：标注来源 (`annotation_joined.jsonl`), `is_problem` 字段, `failure_factor` 覆盖率

### Phase 1（诊断层，不改模型）
- 复现本报告中的统计（Holm 校正 + dedup 口径）
- 提取 M2 proxy: per-slot delta concentration (Gini coefficient), MoGenTS joint_grid_slot 选择性
- 提取 M3 proxy: delta_temporal_std, delta_temporal_diff, 与 trajectory_error 的关系
- 提取 M1 evidence: full prompt vs event-level prompt 的 delta temporal distribution 差异（即使只做 diagnostic，不做模型改动）

### Phase 2（targeted tests，仅 2 个）
- **M4 test**: MoLingo/MoMask length-normalized text embedding ablation。重新 forward text/null，比较：
  - length-delta 相关性变化
  - per-length-quartile failure 率变化
  - 若仅 post-hoc rescale: **必须标注 simulation-only**，不能声称生成改善
- **M1 test**: full prompt vs event prompts vs recomposed condition。targeted evaluation on missing_subaction cases:
  - 对比三种条件的 delta temporal concentration
  - 仅在 delta 分布有结构化变化时，才进入模型改动

### Phase 3（gate）
- 仅 Phase 2 明确支持时进入模型改动
- 否则停在诊断结论
- 模型改动前需要 independent replication on held-out samples

---

## 6. Final Output

### Verdict: PARTIALLY VALID

MoLingo metric_value 的 success/failure 区分是真实信号（Holm 后 p=0.032, d=-1.13）。但其余 15/16 检验不显著；valid_ratio 的定性需要修正；3/5 机制当前仅 diagnostic。

### Critical Issues (by severity)

1. **多重比较未校正** (HIGH): 原始报告声称多个显著结果，Holm 校正后仅 1/16 存活。所有多模型多指标的 claims 必须标注校正状态。
2. **387 CSV 口径错误** (HIGH): 已有分析建立在此口径上，需全部用 dedup_400 重跑。
3. **valid_ratio 定性不准** (MEDIUM): 不是 "不是 confound"，而是 mediator/collider。metric_value 作为阈值时必须控制 valid_ratio。
4. **"attention collapse" 因果跳跃** (MEDIUM): 从 prompt-delta 不相关推断 attention collapse 无直接证据。需 cross-attention map 或 mechanism-specific 证据。
5. **MotionGPT 零信号被低估** (MEDIUM): 这是重要发现——delta 分析对此模型完全无效——但原始报告未充分强调其 implications。
6. **M2/M3/M5 缺乏诊断 proxy** (LOW): 当前不能进入实验。

### Robust Findings

1. MoLingo metric_value 区分 success/failure: Holm p=0.032, d=-1.13 (唯一校正后显著的结论)
2. MotionGPT 四个 delta 指标均无区分能力 (all p>0.35, |d|<0.24): delta 分析对此模型无效
3. MoLingo/MoMask prompt_length 与 delta 正相关 (r=0.453/0.279)，但 pooled 相关弱 (r=0.109): **必须 per-model 分析**
4. valid_ratio 与 metric_value 强相关 (r=0.646)，与 outcome 弱相关 (r=0.111): mediator, not confound
5. Failure 方差 < Success 方差 (MoLingo, MoGenTS): 推翻 naive noise hypothesis，但不等价于 attention collapse

### Claims To Downgrade/Delete

- DELETE: "MoLingo 所有指标 success/failure 差异显著" → 仅 metric_value 成立
- DELETE: "delta_mean 是跨模型最一致的信号" → Holm 校正后无模型通过
- DOWNGRADE: "valid_ratio 不是 confound" → "valid_ratio 是 mediator; metric_value 携带独立信号但必须控制 valid_ratio"
- DOWNGRADE: "failure 来自 attention collapse" → "failure 机制不明; attention collapse 是一个 hypothesis 但无直接证据"
- DOWNGRADE: M2/M3 从 "机制设计" → "diagnostic proxy 待提取"

### Mechanism Priority Table (Revised)

| 优先级 | 机制 | 判定 | 前提条件 |
|--------|------|------|----------|
| P0 diagnostic | M4: Length-Normalized Injection | diagnostic-supported | post-hoc rescale → simulation-only; 重新 forward → 可升级 |
| P1 diagnostic | M1: Event-level Injection | diagnostic-targeted | 先做 full vs event prompt delta 对比 |
| P2 diagnostic | M2: Sparse Routing | diagnostic-only | 先提取 Gini/slot selectivity proxy |
| P2 diagnostic | M3: Temporal Consistency | diagnostic-only | 先提取 temporal_delta_std vs trajectory_error |
| P3 (hold) | M5: FlowEdit Refinement | not-supported-yet | 无直接证据，等 M1-M4 结果 |

### Minimal Next Experiments

1. **Canonical data**: 废弃 387 CSV, 建立 raw_408 + dedup_400 canonical 表
2. **M4 post-hoc**: MoLingo/MoMask length-normalized rescale → 重新计算 delta (simulation-only)
3. **M1 diagnostic**: full vs event prompt delta temporal distribution
4. **M2/M3 proxy extraction**: Gini, temporal_delta_std, trajectory_error correlation

### Reproducibility Checklist

- [x] Data: dedup_400 from delta_tensor_summary.json
- [x] Tests: Mann-Whitney U, two-tailed, normal approximation
- [x] Correction: Holm-Bonferroni on 16 tests
- [x] Effect size: Cohen's d
- [x] Confound: partial correlation controlling for valid_ratio
- [x] Prompt: per-model Pearson r, not just pooled
- [ ] Old 387 CSV: needs deprecation
- [ ] Annotation provenance: needs `annotation_joined.jsonl` traceability doc
- [ ] Failure factor coverage: needs per-factor N and distribution report
