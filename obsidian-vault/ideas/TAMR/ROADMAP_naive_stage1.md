---
created: 2026-04-20
updated: 2026-04-20
status: active
title: "TAMR Stage 1 — Naive Structured Rerank 策略"
parent: ROADMAP.md
---
# Stage 1: Naive Structured Rerank 策略

> 指标释义与公式见 `METRICS.md`。

> 对应 ROADMAP Phase 1 "R1 核心方法验证"。目标：验证 **structured matching > global matching** 假设。
>
> ⚠️ Training-time event alignment 路线（D1/D2a/D2b/P2a）已证伪。本方案为推理时 rerank，不改训练 loss。
>
> 策略：先在 TMR 上验证（代码和 checkpoint 都在），通过后再迁移到 MotionPatches。

## 1. 核心思路

```
Inference pipeline:
  1) Global retrieval: text_emb × motion_emb → cosine sim → top-K candidates
  2) Structured rerank: 对 top-K 中每个 candidate 计算 structured_score
  3) Final score: λ_g · global_score + λ_s · structured_score → 重排序
```

Structured score 计算：
- Text 侧：caption → event decomposition → 逐 event 编码 → `[K_events, D]`
- Motion 侧：14×5 patch tokens → 沿 body-group 池化 → 14 segment tokens `[14, D]`
- 相似度矩阵：`sim[i,j] = cosine(event_i, segment_j)`，shape `[K_events, 14]`
- Monotonic DP：在 sim 矩阵上找最优单调递增路径 → 归一化得分
- Fusion：仅在 query 的 global top-K 候选集内做 score normalization，再做 `global + structured` 融合；最终只重排 top-K 内部顺序，不改变 top-K 集合本身

当前实现约束：
- `K=1`：直接 global fallback，不做 rerank
- `K>=2`：默认按 **ordered monotonic** 处理
- 只有显式 overlap cue（`while/simultaneously/...`）才走 unordered matching

## 2. 步骤化验证（Gate 链）

> 使用蛀牙思维（逐层验证）+ 逆推思维（从目标倒推子能力）。每一步是前一步的 gate，不过就停下分析原因。

### R1-S0: TMR temporal tokens 时序区分度验证

**目的**：确认 TMR motion encoder 的中间表征包含时序信息。

**方法**：
- 加载 TMR 500ep checkpoint（`models/tmr_humanml3d_guoh3dfeats/last_weights`）
- 对 val set 中的长 motion（T > 100 帧），取不同起始位置的滑动窗口（窗口大小 = T/2）
- 用 motion encoder 编码每个窗口，得到 latent
- 计算相邻窗口 vs 远距窗口的 latent 余弦相似度

**Gate**：相邻窗口相似度显著高于远距窗口（p < 0.05）

**预计耗时**：2h

### R1-S1: Event embeddings 语义验证

**目的**：确认 TMR text encoder 编码的 event embedding 与对应 motion 片段有意义的对齐。

**方法**：
- 用 TMR text encoder 分别编码：(a) 完整 caption (b) 每个 decomposed event
- 对 K≥2 样本，将 motion 按 event 数量等分为 segments
- 计算 event_i 与 segment_i 的余弦相似度（对角线）vs event_i 与 segment_j (i≠j) 的相似度（非对角线）

**Gate**：对角线平均相似度 > 非对角线平均相似度

**预计耗时**：2h

### R1-S2: Top-K ceiling 诊断

**目的**：确认 global retrieval 的 top-K 候选集中包含正确答案。

**方法**：
- 在 TMR val set 上计算 global sim matrix
- 对 K≥2 子集，统计正确 motion 在 top-K 内的比例

**Gate**：ceiling@100 > 80%

**预计耗时**：1h

### R1-S3: Reverse-order sanity 诊断

**目的**：确认 monotonic DP 能区分正确顺序和错误顺序。

**方法**：
- 对 K≥2 且非 overlap 的 query
- 计算 `dp_score(events, motion)` vs `dp_score(reverse(events), motion)`

**Gate**：正序 > 反序的比例 > 60%

**预计耗时**：2h

### R1-S4: Structured rerank 端到端验证

**目的**：验证 structured rerank 能在 K≥2 子集上提升 retrieval 指标。

**方法**：
- 实现 monotonic DP rerank（复用 R1-S3 的 DP 代码）
- global top-100 → structured rerank
- 扫描 λ_s ∈ [0.0, 0.1, 0.3, 0.5, 0.7, 1.0]

**Gate**：K≥2 子集 R@1 提升 > +2pp

**预计耗时**：4h

---
## 3. 分步实验设计（R1-S4 通过后的细化实验）

### Exp 0: 先做诊断，不先扫 λ（已合并到 R1-S2/S3）

> 以下 Exp 0 的诊断已合并到上方 R1-S2（Top-K ceiling）和 R1-S3（Reverse-order sanity）。保留原文供参考。

**目的**：先确认 structured score 有信息，再做大规模 sweep。

**诊断 1：Top-K ceiling**
- 统计正确 motion 是否已经在 global top-K 内
- 报告 `ceiling@10/20/50/100`
- 重点看 `K>=2` 子集 ceiling

**诊断 2：Reverse-order sanity**
- 对每个 `K>=2` 且非 overlap 的 query
- 计算 diagonal correct pair 上的：
  - `score(events, motion)`
  - `score(reverse(events), motion)`
- 目标：原始顺序得分显著高于反序

如果这两个诊断不过，不进入 λ / top-K sweep。

### Exp 1.1: Strict Monotonic Rerank（最小可行）

**目的**：验证 monotonic DP structured score 是否能在 K≥2 样本上提升 CAR/TAR。

**配置**：
- 基线 checkpoint：`plain00`（pos66 + DistilBERT，无 event/temporal 训练）
- Motion tokens：冻结 backbone，直接取 14 time tokens（mean pool over body-group）
- Text events：HumanML3D-E GT decomposed events
- Event 编码：优先 `context`，保留完整 caption + event context + 当前 focus event
- DP 路径：默认 `strict`
- Rerank：global top-100 → structured rerank
- Score fusion：先在 top-K 候选集内做 query-wise normalization，再做 `final = λ_g · global + λ_s · structured`；最终将 fused 排序映射回原始 global score 域
- λ_s 扫描：`[0.0, 0.1, 0.3, 0.5, 0.7, 1.0]`（λ_g = 1 - λ_s）

**开关**：`eval.structured_rerank.enable=true eval.structured_rerank.top_k=100 eval.structured_rerank.lambda_s=0.3`

**Smoke gate**：
- `K>=2` 子集的 chronology-sensitive 指标先出现稳定正增益
- `reverse-order` diagnostic 明显优于随机
- 全局 PrimaryScore 不允许出现明显回退（例如 `< -0.3pp`）

### Exp 1.2: Strict vs Skip vs Relaxed

**目的**：对比严格单调 vs 允许跳跃的 DP 变体。

**配置**：在 Exp 1.1 最优 λ_s 基础上：
- `strict`：event_i 必须映射到更晚的 segment
- `skip`：仍要求严格递增，但最多跳过 2 个中间 segment（等价于相邻 event index 差值 ≤ 3）
- `relaxed`：允许相邻 event 映射到同一 segment，作为最宽松对照

**开关**：`--dp-mode {strict,relaxed,skip}`

### Exp 1.3: Rerank Top-K 敏感性

**目的**：确定最优 rerank 候选数量。

**配置**：固定 Exp 1.1/1.2 最优参数，扫描 top-K：
- K ∈ `[10, 20, 50, 100, 200]`

**开关**：`--rerank-top-k {10,20,50,100,200}`

### Exp 1.4: Event 编码策略对比

**目的**：对比不同 event 文本编码方式。

**配置**：
- `independent`：每个 event 独立过 text encoder（默认）
- `prefix`：每个 event 前拼接 "Event i of N: "
- `context`：完整 caption + 全 event context + 当前 focus event

**开关**：`--event-encode-mode {independent,prefix,context}`

## 4. 关键实现模块

> Phase 1 先在 TMR 上实现验证，通过后再迁移到 MotionPatches。

### 4.1 `scripts/tmr_structured_rerank.py`（新文件，TMR 版本）

核心函数：
- `get_tmr_temporal_tokens(model, motion_batch)` → `[B, T, D]` temporal tokens
- `segment_temporal_tokens(tokens, n_segments)` → `[B, n_seg, D]` 等分 segments
- `encode_events(model, event_texts)` → `[K_events, D]` event embeddings
- `monotonic_dp_score(sim_matrix, mode="strict")` → float
- `structured_rerank(global_sim, temporal_tokens, event_embs_list, cfg)` → reranked_sim
- `compute_topk_ceiling(sim_matrix, k_list)` → ceiling metrics
- `compute_reverse_order_diag(event_embs, segment_tokens)` → sanity metrics

### 4.2 MotionPatches 版本（R1-S4 通过后迁移）

原 `MotionPatches-main/structured_rerank.py` 方案保留，待 TMR 验证通过后实现：
- `ClipModel.encode_motion_time_tokens()` → L2-normalized time tokens `[B, 14, D]`
- `test.py` 评估路径扩展

## 5. 样本分类处理

| 样本类型 | 判定条件 | 处理方式 |
|---------|---------|---------|
| single (K=1) | GT events 数量 = 1 | 走 global fallback，structured_score = global_score |
| ordered-default (K≥2) | GT events 数量 ≥ 2 且**没有显式 overlap cue** | monotonic DP |
| explicit-overlap (K≥2) | 含 `while/simultaneously/...` 等显式重叠词 | unordered matching（exact assignment） |

K=1 占比 ~50.7%，因此全局指标涨幅预期有限，需分层报告 `K>=2`、condition2/3/4，以及 reverse-order diagnostics。

## 6. 实验脚本

评测脚本：

```
scripts/run_stage1_structured_rerank.sh
```

正式训练脚本：

```
MotionPatches-main/scripts/run_mp_s2e_v2_stage1_rerank_train.sh
```

说明：
- 训练 recipe 仍沿用 `stage5_s2e_v2` 对比基线
- `batch_size=64`、`epoch=50` 保持不变
- structured rerank 只影响训练后的 eval 闭环，不改训练 loss

## 7. 预期时间线

| 步骤 | 预计耗时 |
|------|---------|
| R1-S0 temporal tokens 时序区分度 | 2h |
| R1-S1 event embeddings 语义验证 | 2h |
| R1-S2 top-K ceiling 诊断 | 1h |
| R1-S3 reverse-order sanity | 2h |
| R1-S4 structured rerank 端到端 | 4h |
| Exp 1.1 λ_s 扫描（R1-S4 通过后） | ~2h |
| Exp 1.2 DP mode 对比 | ~1h |
| Exp 1.3 Top-K 敏感性 | ~1h |
| Exp 1.4 Event 编码策略 | ~2h |

R1-S0 到 R1-S4 为串行 gate 链，总计 ~11h（~1.5 天）。Exp 1.1-1.4 为 R1-S4 通过后的细化实验，额外 ~1 天。

## 8. 风险与缓解

0. **Training-time event alignment 已证伪** → 本方案完全基于推理时 rerank，不改训练 loss，风险隔离
1. **Top-K ceiling 太低** → R1-S2 gate，不满足就不做后续
2. **TMR temporal tokens 无时序区分度** → R1-S0 gate，不满足说明 TMR backbone 本身不编码时序，需要换 backbone 或加 temporal positional encoding
3. **14-bin 固定切分 vs 语义边界不对齐** → `strict/skip/relaxed` 对比，只把 `relaxed` 当对照
4. **text encoder 未见过 sub-event 文本** → `context` 作为默认主线，Exp 1.4 做编码策略对比
5. **structured score 与 global score 分布不一致** → 候选集内 query-wise normalization，再线性融合
6. **K=1 样本无法受益** → 分层报告，关注 `K>=2` / condition2/3/4 / reverse-order diagnostics
7. **context 文本可能被 tokenizer 截断** → 每次 rerank eval 自动记录 token 长度 / truncation / focus event 可见性统计
