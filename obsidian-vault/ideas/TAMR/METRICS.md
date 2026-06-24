# TAMR Metrics

> TAMR 相关指标的统一释义与计算方法概述。
> 目标是统一 `ROADMAP / EXPERIMENTS / 验证记录 / archived eval` 的口径。

## 1. 标准 Retrieval 指标

### `t2m` / `m2t`

- `t2m`：text-to-motion。给定文本 query，在 motion gallery 中检索正确 motion。
- `m2t`：motion-to-text。给定 motion query，在 text gallery 中检索正确文本。

### `R@K`

- 定义：正确样本的 rank `< K` 的 query 比例。
- 公式：

```text
R@K = (# {q | rank(q) < K}) / N_queries
```

- 常见的 `K`：`1 / 2 / 3 / 5 / 10`
- 越高越好。

### `MedR`

- 定义：所有 query 的正确样本排名（1-based）的中位数。
- 公式：

```text
MedR = median(rank(q) + 1)
```

- 越低越好。

### rank 的含义

- `rank=0` 表示第一名就是 GT。
- 在本仓库里：
  - 标准 `retrieval.py` 用 `src/model/metrics.py`
  - 我们补充的 ceiling / subset 统计使用 average tie-breaking 的自定义 rank
- 两者在无大量 tie 的情况下通常应接近。

## 2. Retrieval 协议

### `normal`

- full-gallery strict retrieval。
- 每个样本只取一条标准 caption，与整个 test gallery 做检索。
- 是最主要的 retrieval 对比协议。

### `nsim`

- non-similar / harder split。
- 只在较难、语义相近更高的子集上评估。
- 用于检测 harder retrieval 下的判别能力。

### `threshold_0.95`

- 在文本自相似度高于阈值的情况下做 GT 合并或过滤。
- 目的是减轻“多个文本本来就几乎等价”造成的评测噪声。

### `guo`

- Guo-style batched matching / R-Precision 口径。
- 本质是小批量候选中的匹配，不等价于 full-gallery retrieval。
- 不能把 `guo` 的数值直接和 `normal/nsim` 横比。

## 3. `PrimaryScore`

- 当前 TAMR 文档中的 `PrimaryScore`，通常指：

```text
PrimaryScore = mean(
  normal t2m R@1,
  normal m2t R@1,
  nsim   t2m R@1,
  nsim   m2t R@1,
  normal t2m R@5,
  normal m2t R@5,
  nsim   t2m R@5,
  nsim   m2t R@5
)
```

- 即 8 个值的平均。
- 用途：压缩成一个主检索分数，便于 same-regime scoreboard。
- 风险：会掩盖 `normal` 和 `nsim` 的结构性差异，因此任何提升都必须回看明细。

## 4. Phase 1 / R1 指标

### `R1-S0` temporal token 时序区分度

- 目标：验证 temporal tokens 是否带有时间敏感性。
- 当前实现：
  - 取同一 motion 的 3 个窗口
  - 比较邻近窗口与远距窗口的 pooled temporal embedding cosine
- 主要统计：
  - `mean_adjacent_cosine`
  - `mean_far_cosine`
  - `adjacent_gt_far_ratio`
  - `sign_test_p_one_sided`

### `R1-S1` event-motion 对角线优势

- 目标：验证 event embedding 是否更偏向对应 segment。
- 当前统计：

```text
diag_mean = mean(sim[event_i, segment_i])
offdiag_mean = mean(sim[event_i, segment_j], i != j)
```

- 主要指标：
  - `mean_diag_cosine`
  - `mean_offdiag_cosine`
  - `mean_margin = diag - offdiag`
  - `diag_gt_off_ratio`

### `R1-S2` `ceiling@K`

- 定义：GT 是否已经在 global retrieval 的 top-K 候选集中。
- 公式：

```text
ceiling@K = (# {q | gt_rank(q) < K}) / N_queries
```

- 这是 rerank 的前提上限，不是 rerank 后性能。
- 若 `ceiling@100` 太低，则 structured rerank 理论上也很难提升。

### `R1-S3` reverse-order sanity

- 定义：比较

```text
score(events, motion) vs score(reverse(events), motion)
```

- 主要指标：
  - `mean_forward_score`
  - `mean_reverse_score`
  - `forward_gt_reverse_ratio`

- 用途：检查 structured score 是否真的编码了顺序。

### `R1-S4` structured rerank gain

- 定义：在 global top-K 候选内，用 structured score 融合后重新排序。
- 主要关注：
  - `baseline K>=2 R@1`
  - `best lambda_s`
  - `best_gain_r1_pp`

- 这里的 `pp` 指百分点（percentage points）。

## 5. `ceiling` 与最终性能的区别

- `ceiling@K` 是候选集上限：
  - 问“GT 在不在 top-K 里”
- `R@K` 是最终排序性能：
  - 问“GT 最终有没有排到前 K”

因此：

- `ceiling@100` 高但 `R@1` 低，说明 rerank 或 score 设计还有改进空间
- `ceiling@100` 本身低，说明问题更可能在 global retrieval 阶段

## 6. HumanML3D 上的 `temporal_cue_proxy_subset`

- 原始 HumanML3D annotations 没有 HumanML3D-E 式的显式 decomposed events
- 因此不能把 HumanML3D 原始 test 直接当作 `K>=2` 子集来跑 `S3`
- 当前补充统计里定义了一个 proxy 子集：

```text
caption contains one of
{then, before, after, while, simultaneously, at the same time, meanwhile}
```

- 这个子集仅用于观察“更可能带时序关系的自然语言 query”在 full gallery 上的 ceiling / retrieval 情况
- 它 **不是** HumanML3D-E 的 `K>=2` 等价物

## 7. `CAR / TAR`

### `CAR@K`

- Chronologically-Accurate Retrieval
- 更偏“顺序是否正确”的 retrieval 指标

### `TAR@K`

- Temporal-Aware Retrieval
- 更偏“所有时序约束是否满足”的 retrieval 指标

### 使用边界

- `CAR/TAR` 很适合做 temporal capability diagnosis
- 但它们目前不是 motion-text retrieval 社区的通用主表指标
- 所以它们更适合作为：
  - 机制诊断
  - 能力分层分析
  - 辅助证据

而不是唯一主表分数

## 8. 当前最重要的口径提醒

1. `guo` 协议不是 full-gallery retrieval，不要和 `normal/nsim` 混看。
2. `ceiling@K` 不是最终 R@K，它只是 rerank 上限。
3. HumanML3D 原始集没有 HumanML3D-E 式 event decomposition，因此不能强行照搬 `S3`。
4. `PrimaryScore` 是聚合指标，任何结论都必须回到明细指标看结构。
