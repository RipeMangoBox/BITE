---
title: "400-sample text-condition trace 分析方案设计"
created: 2026-05-28T15:30:00+08:00
updated: 2026-05-28T15:30:00+08:00
status: draft
tags:
  - MoDebug
  - analysis_plan
  - sample_level_trace
  - text_condition_propagation
---

# 400-sample text-condition trace 分析方案设计

## 目标

从 4 baseline × ~100 sample 的 text vs null_text delta trace 中，系统性地分析 text embedding 对 motion 生成过程的引导作用，识别成功/失败样本的 delta 模式差异，为进一步设计机制提高指令跟随能力提供依据。

## 1. 数据现状与扩展路径

### 当前状态（2026-05-28）

- 每 baseline 仅 1 success + 1 failure = 8 cases
- 数据链完整：`sample_id → human_annotation → motion_artifact → forward/delta manifest`
- delta 张量形状因模型而异：

| Model | f_name | delta shape | axis_names | valid_ratio |
|-------|--------|-------------|------------|-------------|
| MotionGPT | token_logits | (1, 6, 514) | [batch, decoder_step, motion_vocab] | 1.0 |
| MoLingo | hidden_state | (1, 49, 1024) | [batch, latent_token, hidden_dim] | 0.47–0.78 |
| MoMask | token_logits | (1, 21–23, 512) | [batch, token_time, codebook] | 1.0 |
| MoGenTS | token_logits | (1, 23–38, 6, 256) | [batch, token_time, joint_grid_slot, codebook] | 1.0 |

### 扩展到 400 samples 的前提条件

1. 需要跑通 4 baseline × 100 sample 的 batch trace（已有单样本 runner，需要 batch wrapper）
2. 需要所有 400 sample 的 human annotation（已有 Original100 标注数据，每 baseline 100 条）
3. 需要统一的 manifest index 和 quality validation（`trace_contract_validator.py` 和 `build_manifest_index.py` 可直接复用）

**关键风险**: MoLingo 的 valid_mask 只有 47–78%。这是因为 MoLingo 使用 full_mask AR state，部分 latent token 在初始步未被激活。批量分析时需要在所有统计中 propagate valid_mask，否则未激活位置的噪声会污染结论。

## 2. 分析维度体系

### 2.1 样本级描述维度（每 sample 一个标量或类别）

| 维度                           | 来源                       | 类型          | 说明                                                                         |       |                 |
| ---------------------------- | ------------------------ | ----------- | -------------------------------------------------------------------------- | ----- | --------------- |
| `outcome`                    | human_annotation         | binary      | success / failure                                                          |       |                 |
| `failure_factor`             | human_annotation         | categorical | missing_subaction, trajectory_error, artifact_sliding_or_drift, ...        |       |                 |
| `model_label`                | metadata                 | categorical | MotionGPT, MoLingo, MoMask, MoGenTS                                        |       |                 |
| `model_family`               | metadata                 | categorical | t5_motion_language, t5_latent_motion, clip_discrete                        |       |                 |
| `prompt_length`              | prompt text              | scalar      | 字符数 / token 数                                                              |       |                 |
| `prompt_n_sub_actions`       | prompt text (LLM parsed) | scalar      | 语义子动作数量                                                                    |       |                 |
| `prompt_temporal_complexity` | prompt text (LLM parsed) | ordinal     | 时序依赖复杂度（并行/串行/混合）                                                          |       |                 |
| `motion_length_frames`       | source_npy               | scalar      | 动作帧数                                                                       |       |                 |
| `overall_relative_l2`        | delta NPZ metric_value   | scalar      | text vs null 全局相对 L2                                                       |       |                 |
| `delta_abs_max`              | delta tensor             | scalar      | delta 张量绝对值最大值                                                             |       |                 |
| `delta_sparsity`             | delta tensor             | scalar      |                                                                            | delta | < threshold 的比例 |
| `temporal_concentration`     | delta tensor             | scalar      | 前 20% 时间步贡献的 delta 比例                                                      |       |                 |
| `delta_temporal_std`         | delta tensor             | scalar      | per-timestep L2 的标准差（时间分布均匀性）                                              |       |                 |
| `delta_mean_abs`             | delta tensor             | scalar      | delta 绝对值均值                                                                |       |                 |
| `delta_skewness`             | delta tensor             | scalar      | delta 分布偏度（正=text 整体增强，负=text 整体抑制）                                        |       |                 |
| `peak_time_step`             | delta tensor             | scalar      | delta L2 最大的时间步索引（归一化到 [0,1]）                                              |       |                 |
| `z_kind`                     | metadata                 | categorical | decoder_prefix, latent_ar_state, mask_iteration, time_joint_mask_iteration |       |                 |

### 2.2 时间序列维度（每 sample 一个向量）

| 维度 | 来源 | 类型 | 说明 |
|------|------|------|------|
| `per_timestep_l2` | delta → frame_l2 | vector[T] | 每个时间步的 delta L2 |
| `per_timestep_l2_norm` | per_timestep_l2 / overall_relative_l2 | vector[T] | 归一化到总 delta 的比例分布 |
| `temporal_diff_l2` | diff(per_timestep_l2) | vector[T-1] | delta 的时间变化率 |
| `cumulative_l2_curve` | cumsum(per_timestep_l2) | vector[T] | 累积 delta 曲线（用于 AUC 分析） |

### 2.3 特征空间维度（每 sample 一个矩阵或降维向量）

| 维度 | 来源 | 类型 | 说明 |
|------|------|------|------|
| `per_feature_bin_l2` | delta → feature_bin mass | vector[N_BINS] | 特征维度分 bin 后的 L2（时间平均） |
| `time_feature_mass` | delta → bin heatmap | matrix[T × N_BINS] | 完整的 time × feature_bin mass |
| `feature_PCA_projection` | delta → PCA | vector[K] | 对 time-feature mass 做 PCA 后的前 K 个主成分 |

### 2.4 跨模态对齐维度

| 维度 | 来源 | 类型 | 说明 |
|------|------|------|------|
| `prompt_delta_correlation` | prompt embeddings vs delta pattern | scalar | prompt CLIP/T5 embedding 与 delta 模式的相关性 |
| `sub_action_delta_alignment` | LLM-parsed sub-actions vs delta peaks | vector | 每个子动作对应时间段的 delta 激活强度 |

## 3. 分析流水线设计

### 核心闭环：统计发现 → sample 回查 → 机制设计

本方案的核心问题不是单纯找一个能区分 success/failure 的指标，而是建立一条可复查的研究链路：**aggregate 统计发现候选模式 → sample-level 证据回查确认模式含义 → 形成可反驳的机制假设 → 设计最小干预实验**。

执行要求：
- 每个统计发现都必须落到代表样本、异常样本或 borderline sample 上，回看 prompt、human annotation、motion MP4、forward/delta manifest 和可视化。
- 每个机制假设必须说明它来自哪些统计证据、哪些 sample 证据、预期改变哪个 delta pattern、预期改善哪类 motion failure。
- 若缺少 random text、semantic perturbation、partial text mask 或 held-out evaluator，只能写为 diagnostic hypothesis，不能写成最终因果结论。

### Phase 1: 批量 trace 运行与质控（工程阶段）

**目标**: 将 8 case 扩展到 400 sample，确保数据质量一致。

- 包装 `run_*_sample_trace.py` 为 batch runner，支持 per-model 并行
- 自动运行 `trace_contract_validator.py` 和 `build_manifest_index.py`
- 输出: 统一的 `batch_manifest_index.tsv`，400 row 全量索引
- 质控 check: valid_mask 覆盖检查、delta NaN/Inf 检查、manifest 完整性检查
- MoLingo 额外要求: delta、`relative_l2`、`per_timestep_l2`、`time_feature_mass` 均使用 text/null 有效 mask 交集；每个 sample 输出 `valid_ratio` 和 coverage，避免未激活 latent token 进入统计。

### Phase 2: 单变量描述统计（探索阶段）

**目标**: 建立每个维度的分布基线，识别粗粒度模式。

**数值工具:**
- `descriptive_stats.py`: 对 2.1 中所有标量维度计算 per-model × per-outcome 的 mean/std/median/IQR
- `distribution_test.py`: Mann-Whitney U test 检验 success vs failure 在每个维度上是否有显著差异
- `effect_size.py`: Cohen's d 量化每个维度的 success/failure 区分能力

**可视化:**
- Per-model violin plot: `overall_relative_l2` 分布，按 outcome 分组
- Per-model scatter matrix: 关键标量维度的 pairwise scatter（prompt_length, delta_sparsity, temporal_concentration, peak_time_step）
- Per-model CDF overlay: success vs failure 的 cumulative L2 curve 叠加对比

**分析要点:**
- 是否存在一个 "delta 甜区" (relative_l2 既不太低也不太高时 success 率最高)?
- 不同 model_family 的 delta 分布形态是否有系统性差异?
- MoLingo 的低 valid_ratio 是否与 failure 率相关?

### Phase 3: 聚类与模式发现（核心分析阶段）

**目标**: 不以 outcome 为先验，从 delta 模式本身发现自然分组。

#### 3.1 基于 time-feature mass 的聚类

**输入**: 每个 sample 的 `time_feature_mass` 展平为向量（需要对齐时间维度: pad/interpolate 到统一长度）。

**方法:**
- PCA 降维 → 保留 95% 方差的成分
- K-means (K=3..8) + silhouette score 选最优 K
- t-SNE/UMAP 可视化 + 标注 outcome 和 failure_factor

**可视化:**
- t-SNE scatter plot: 每个点是一个 sample，颜色 = cluster，形状 = outcome
- 每个 cluster 的 "代表样本" heatmap（质心最近的实际样本）
- Per-cluster outcome 分布条形图

**分析问题:**
- 自然聚类的簇是否与 outcome 或 failure_factor 一致?
- 是否存在 "hard samples" 簇（failure 集中但 delta 模式相似的样本）?
- 跨模型的聚类是否比 per-model 聚类更有信息量?

#### 3.2 基于时序模式的聚类

**输入**: `per_timestep_l2_norm`（归一化后的时间分布）。

**方法:**
- DTW (Dynamic Time Warping) 距离 + 层次聚类
- 识别典型时序模式: early-peak, late-peak, uniform, bimodal

**可视化:**
- Per-cluster mean temporal profile with std band
- 每个时序模式对应的典型 prompt（文本分析）

**分析问题:**
- Success case 是否倾向于 early-peak（text 早期就引导了方向）?
- Failure case 是否表现为 delta 分布均匀（text 没有明确的引导信号）?
- 不同 model_family 是否有不同的 "健康时序模式"?

#### 3.3 基于 prompt 特征的聚类

**输入**: prompt text → sentence embedding (all-MiniLM-L6-v2 或 T5-XXL)

**方法:**
- Sentence embedding → UMAP + HDBSCAN 聚类
- Per-cluster 的 outcome 分布和 delta 统计量

**可视化:**
- UMAP scatter with prompt keywords overlay
- Per-cluster success rate bar chart

**分析问题:**
- 是否存在 "hard prompts"（长文本、多子动作、时序复杂）导致低 success rate?
- 不同模型对 prompt 类型的鲁棒性是否有差异?

### Phase 4: Success/Failure 判别分析（因果探索阶段）

**目标**: 不声称 causal，但识别与 success 最相关的 delta 特征。

#### 4.1 特征重要性

**方法:**
- Random Forest classifier: predict outcome from scalar delta features + prompt features
- SHAP values: 量化每个特征的贡献
- 分别 per-model 和跨模型训练

**输出:**
- SHAP summary plot (bar + beeswarm)
- Per-model top-5 区分特征

#### 4.2 决策边界分析

**方法:**
- Logistic regression on top-3 features → 可视化决策边界
- 识别 "borderline samples"（接近决策边界的样本）→ 这些是机制改进的最优 target

#### 4.3 Counterfactual 模拟（如果数据支持）

**局限**: 当前只有 text vs null_text，没有 random text 或部分 mask 条件。

**如果后期添加这些控制条件，可以做的:**
- 渐进式 text masking (mask 10%, 30%, 50%, 100% of text tokens) → delta 的 dose-response curve
- Random text embedding → delta 的 specificity test
- Semantic perturbation (swap 同义/反义词) → delta 的 sensitivity test

### Phase 5: 机制推断与改进方向

#### 5.1 从 delta 模式到干预策略

根据 Phase 2-4 的发现，推断机制分类:

| Delta 模式                  | 推断                     | 可能的干预                                        |
| ------------------------- | ---------------------- | -------------------------------------------- |
| delta 过低（failure 常见）      | text embedding 没有有效注入  | 增强 cross-attention / 增加 text conditioning 强度 |
| delta 过高 + failure        | text 过度压制 motion prior | 引入 text-motion balance gate                  |
| delta 晚期峰值 + failure      | text 引导来得太晚            | 在早期 decoding step 注入更强的 text bias            |
| delta 集中在错误特征区域 + failure | text 被路由到无关的 motion 维度 | 学习 sparse text-to-motion feature mapping     |
| delta 时序波动大 + failure     | text 引导不稳定             | 引入 temporal smoothing / consistency loss     |

#### 5.2 Per-model 改进优先级

- **MotionGPT (T5 decoder prefix)**: delta 仅在 6 个 decoder step 上生效。如果 failure case 的 delta 过低，检查 T5 encoder 的 text embedding 质量。
- **MoLingo (latent AR state)**: valid_ratio 仅 47-78%，大量 latent token 未激活。这是天然的 sparsity bottleneck —— 可以设计 sparse text injection 只针对已激活 token。
- **MoMask (discrete mask iter)**: delta on codebook logits。可以分析哪些 codebook entry 对 text 最敏感，设计 codebook-level text conditioning。
- **MoGenTS (joint grid mask iter)**: 已有 2D grid 结构（time × joints）。可以将 delta 按 joint 维度可视化（已有 time-grid mass），进一步推断 text 对 body part 的选择性引导。

## 4. 可视化 vs 数值工具分工

### 可视化分析（人类模式识别）

| 任务                           | 工具                  | 产出                 |
| ---------------------------- | ------------------- | ------------------ |
| Per-model delta mass heatmap | SVG (已有)            | 发现跨时间/特征的 delta 结构 |
| t-SNE/UMAP sample embedding  | Plotly/Altair HTML  | 交互式样本空间探索          |
| Per-cluster temporal profile | Matplotlib/SVG      | 识别典型时序模式           |
| SHAP feature importance      | SHAP plot           | 关键区分特征可视化          |
| Prompt-delta 联合空间            | Plotly linked views | 连接文本特征和 delta 模式   |

### 数值工具（统计推断 + 自动化）

| 任务          | 工具                            | 产出                              |
| ----------- | ----------------------------- | ------------------------------- |
| 描述统计        | `descriptive_stats.py`        | CSV 表格                          |
| 分布差异检验      | `distribution_test.py`        | p-values + effect sizes         |
| 聚类 + 指标     | `cluster_analysis.py`         | cluster labels + silhouette/DBI |
| 分类器 + SHAP  | `outcome_classifier.py`       | feature importance + AUC        |
| Delta 模式分类器 | `delta_pattern_classifier.py` | 自动标注 delta pattern type         |
| 跨模态相关性      | `cross_modal_correlation.py`  | prompt-delta 相关矩阵               |

## 5. 多 Agent 协作分析架构

将分析拆分为独立 agent，每个负责一个维度，最后汇总。

```
                    ┌─────────────────────┐
                    │  Agent O: 协调器     │
                    │  (任务分发 + 汇总)    │
                    └──────┬──────────────┘
           ┌───────────────┼───────────────┬───────────────┐
           │               │               │               │
    ┌──────▼──────┐ ┌──────▼──────┐ ┌──────▼──────┐ ┌──────▼──────┐
    │ Agent A:    │ │ Agent B:    │ │ Agent C:    │ │ Agent D:    │
    │ 描述统计    │ │ 聚类分析    │ │ 判别分析    │ │ Prompt分析  │
    │             │ │             │ │             │ │             │
    │ 单变量分布  │ │ PCA+t-SNE   │ │ RF+SHAP     │ │ NLP特征     │
    │ 差异检验    │ │ K-means+    │ │ 决策边界    │ │ Prompt嵌入  │
    │ Effect size │ │ DTW cluster │ │ Top features│ │ 子动作解析  │
    └──────┬──────┘ └──────┬──────┘ └──────┬──────┘ └──────┬──────┘
           │               │               │               │
           └───────────────┼───────────────┼───────────────┘
                           │               │
                    ┌──────▼───────────────▼──────┐
                    │ Agent E: 综合报告 + 假设生成 │
                    │                              │
                    │ 跨agent发现整合               │
                    │ 机制推断 + 改进建议           │
                    │ 下一步实验设计               │
                    └──────────────────────────────┘
```

### Agent 定义

**Agent A — 描述统计**
- 输入: `batch_manifest_index.tsv` + 所有 delta NPZ
- 产出: per-model × per-outcome 的完整统计表，所有维度的 M-W 检验和 Cohen's d
- 关键检查: MoLingo valid_mask 处理、跨模型可比性声明

**Agent B — 聚类分析**
- 输入: agent A 产出的 time_feature_mass 矩阵
- 产出: cluster labels, t-SNE coordinates, per-cluster 画像
- 方法: PCA → K-means → silhouette; DTW + 层次聚类
- 可视化: t-SNE plot + per-cluster heatmap 代表

**Agent C — 判别分析**
- 输入: agent A 产出的标量特征表 + outcome labels
- 产出: SHAP importance ranking, decision boundary, borderline samples
- 方法: Random Forest + SHAP, Logistic Regression

**Agent D — Prompt 分析**
- 输入: prompt text + LLM
- 产出: n_sub_actions, temporal_complexity, prompt embedding, sub-action boundaries
- 方法: LLM parsing + sentence-transformers embedding

**Agent E — 综合报告**
- 输入: agent A/B/C/D 产出
- 产出: 综合分析报告 + 机制推断 + 下一步实验设计
- 关键: 不做出超出数据支持的因果声明

## 6. 实施路径与优先级

### 立即（本周）
1. 批量 trace runner（扩展到 400 sample）
2. Agent A: 描述统计 + 差异检验 → 先看全局信号

### 短期（1-2 周）
3. Agent D: Prompt 分析 → 识别 hard prompt 类型
4. Agent B: 聚类分析 → 发现自然 delta 模式分组
5. Agent C: SHAP 判别分析 → 确认区分 success/failure 的关键 delta 特征

### 中期（2-4 周）
6. Agent E: 综合报告 + 机制推断
7. 根据 agent E 的建议设计干预实验（增加 counterfactual/random 控制条件）
8. 在 MoGenTS 的 joint grid 上验证 text-to-body-part 选择性引导假说

## 7. 局限与注意事项

1. **当前只有 text/null 条件**，不能分离语义特异性、因果方向、或排除 general perturbation effect。干预实验需要 random text embedding / semantic perturbation 控制。
2. **MoLingo 的 valid_mask < 100%** 是一种结构性稀疏，不是 bug。分析时必须只统计 valid positions，否则噪声会主导信号。
3. **跨模型 delta 值不可直接比较**: 不同 f_space (logits vs hidden_state) 的量纲和动态范围不同。跨模型分析只能用 ranking 或 per-model 归一化后的模式相似度。
4. **8 → 400 的扩展假设**: 当前 8 case 的模式可能不能代表 400 sample 的分布。Phase 2 的初步统计如果与当前 pilot 发现矛盾，需要重新审视 pilot 代表性。
5. **不是 final evaluator**: delta trace 是内部诊断信号，不能替代 human evaluation 或 downstream motion quality metrics。
