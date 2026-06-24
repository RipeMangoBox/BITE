# GPT Review Handoff — MoDebug 400-sample 分析复核

将此文档交给 GPT 进行独立复核。GPT 应审查数据分析方法、统计结论的有效性、机制设计的逻辑链、以及实验设计的可行性。

## 1. 项目背景

**目标**: 研究 text-to-motion 模型中 text embedding 如何传播并引导动作生成，识别 success/failure 样本的 delta 模式差异，设计机制提高指令跟随能力。

**方法**: 对 4 个 baseline 模型（MotionGPT, MoLingo, MoMask, MoGenTS），用相同随机状态分别跑 text 和 null_text（空字符串）的 forward pass，计算 delta = forward(text) - forward(null_text)。delta 反映 text condition 在模型内部特征空间的净效应。

**数据规模**: 400 samples = 4 baselines × 100 samples（来自 HumanML3D Original100 子集），每 sample 有人工标注（success/failure + failure_factor）。

## 2. 原始数据位置

所有路径均为绝对路径。

```
delta_tensor_summary.json → /data/Life Me/ResearchWY Vault/obsidian-vault/paperIDEAs/MoDebug/active/text_condition_propagation_guidance/_archive_20260527/visualizations/delta_tensor_summary.json
prompt_features.csv → /tmp/prompt_features_full.csv
descriptive_stats.csv → /tmp/descriptive_stats_400.csv
feature_importance.csv → /tmp/feature_importance_387.csv
prompt-delta correlation → /tmp/prompt_delta_correlation.md
deep analysis → /tmp/deep_analysis_report.md
mechanism plan → /data/Life Me/ResearchWY Vault/obsidian-vault/paperIDEAs/MoDebug/active/text_condition_propagation_guidance/mechanism_design_plan.md
GPT handoff → /data/Life Me/ResearchWY Vault/obsidian-vault/paperIDEAs/MoDebug/active/text_condition_propagation_guidance/GPT_REVIEW_HANDOFF.md
```

每 case 字段: model, outcome, sample_id, metric_value (relative_l2), delta_abs_max, delta_mean, delta_std, valid_ratio, delta_shape, f_name, f_space

## 3. 四项指标定义

- **metric_value (relative_l2)**: ||delta|| / ||forward(text)|| — text 对特征的总影响强度
- **delta_abs_max**: delta 张量中绝对值最大的元素
- **delta_mean**: delta 张量的均值（正=text 整体增强，负=text 整体抑制）
- **delta_std**: delta 张量的标准差（反映 delta 的空间分布均匀性）
- **valid_ratio** (MoLingo only): latent token 中非 padding 的比例（MoLingo 使用 49-token 固定序列，仅前 N 个有效）

## 4. 分析结果（待复核）

### 4.1 描述统计

4 baseline × 2 outcome = 8 groups。MotionGPT 81 cases (66S/15F), MoLingo 102 (89S/13F), MoMask 102 (78S/24F), MoGenTS 102 (80S/22F)。

### 4.2 统计显著性（Cohen's d, success vs failure）

| Metric | MoLingo | MoGenTS | MoMask | MotionGPT |
|--------|---------|---------|--------|-----------|
| metric_value | **-0.944***** | -0.116 | -0.482 | -0.029 |
| delta_abs_max | **-0.968**** | -0.370 | -0.054 | -0.167 |
| delta_std | **-0.556*** | -0.285 | +0.054 | -0.014 |
| delta_mean | **-0.876**** | -0.545* | **-0.680*** | +0.051 |

负值 = failure > success。* = p<.05, ** = p<.01, *** = p<.001。

**关键断言**: MoLingo 唯一强信号。MotionGPT 零区分 (p=0.920)。MotionGPT 成功案例可承受 delta_abs_max=149.94。

### 4.3 valid_ratio confound 分析（需重点复核）

**原始担忧**: MoLingo failure 的 valid_ratio 均值 0.80 > success 的 0.70。更多有效 token → 更大 metric 可能仅因更多 token 参与计算。

**分析结论**: valid_ratio 与 outcome 无显著相关 (r=-0.115, p=.249)。控制 valid_ratio 后的偏相关 r=-0.302 ≈ 原始 r=-0.303。结论: **valid_ratio 不是 confound**。

**复核要点**: 偏相关计算是否正确？tertile 分层 d 值 (-0.39 to -1.74) 是否一致？

### 4.4 Failure 方差分析（需重点复核）

**断言**: MoLingo failure 方差 < success 方差 (Levene p=.006)。MoGenTS 同样 (p=.048)。

**推论**: Failure 集中在高 metric 区域，而非随机散布 → 推翻 "noise causes failure" 假说。

### 4.5 Prompt-Delta 关系

**断言**: Prompt 复杂度（length, word_count, n_sub_actions）与 failure 强相关 (p<.001)，但与 delta 幅度无显著线性相关 (|r| < .05)。

**推论**: Failure 机制 ≠ delta 饱和。可能是 attention collapse 或 cross-modal interference。

### 4.6 非线性和模型特异性

- **MoLingo**: 单调 — decile 1-4 零 failure, top decile 33%
- **MoMask**: U 形 — 中段和高端两种 failure 模式
- **MoGenTS**: 倒 U — 中段 peak 50%, 两端低
- **MotionGPT**: 平噪声 — 所有 decile 无差异

## 5. 机制设计（待复核）

### M1: Event-level Text Injection
- **问题**: global text embedding 压缩多子动作语义 → missing_subaction
- **方案**: 分解 prompt 为子动作 event embedding，per-event cross-attention 注入
- **参考**: Event-T2M (ICLR 2026)
- **实验**: LLM 解析子动作 → 替换 MotionGPT global embedding → 对比 delta temporal concentration 和 missing_subaction 率

### M2: Sparse Text-to-Feature Routing
- **问题**: text 均匀影响所有特征维度 → 信号稀释 → artifact
- **方案**: top-K sparse gate 将 text 路由到相关 feature subspace
- **参考**: LMM/TOMATO (ECCV 2024), Hidden Semantic Bottleneck (ICLR 2026)
- **实验**: MoGenTS grid_slot 选择性分析 → K=2-3 gate → 对比 full vs sparse

### M3: Temporal Consistency Regularization
- **问题**: delta 时序波动大 → trajectory_error
- **方案**: temporal smoothness loss 约束相邻时间步 delta L2 变化率
- **参考**: KinemaDiff (ICLR 2026), MotionStream (ICLR 2026)
- **实验**: 相关性验证 → 添加 smoothness loss → 对比 delta_temporal_std

### M4: Length-Normalized Text Injection
- **问题**: MoLingo/MoMask delta 幅度与 prompt 长度正相关
- **方案**: text embedding 按 1/sqrt(n_tokens) 缩放
- **实验**: 一行代码改动 → 对比 length-delta r 值

### M5: Post-hoc FlowEdit Refinement
- **问题**: artifact/trajectory error 可后处理修正
- **方案**: FlowEdit ODE 推理时修改 text condition 局部修正
- **参考**: Unified Conditional Flow (arXiv 2026), ExpertEdit (arXiv 2026)

### 优先级

| 级别 | 机制 | 理由 |
|------|------|------|
| P0 | M4 | 最简单，一行代码 |
| P0 | M2 | 直接针对 artifact |
| P1 | M1 | 针对核心 missing_subaction |
| P1 | M3 | 针对 trajectory_error |
| P2 | M5 | 安全网，依赖前几个效果 |

## 6. 复核检查清单

请 GPT 重点审查以下问题:

**统计方法**:
- [ ] Cohen's d 和 Mann-Whitney U 的用法是否正确？（小样本，非正态分布）
- [ ] valid_ratio 偏相关分析是否正确？是否应使用更严格的因果推断方法？
- [ ] Levene test 对 failure 方差 < success 方差的结论是否稳健？
- [ ] 多重比较是否做了校正（4 models × 4 metrics = 16 tests）？

**逻辑链**:
- [ ] "failure 方差低 → 不是 noise → attention collapse" 的推断是否有跳跃？
- [ ] "prompt 复杂度 ≠ delta 幅度 → failure 来自 attention collapse" 是否有替代解释？
- [ ] MoMask U-shaped failure 的两种模式是否被正确识别？

**机制设计**:
- [ ] M1-M5 的逻辑是否与数据分析发现一致？
- [ ] 是否有遗漏的机制方向？
- [ ] 实验设计是否可证伪？失败判据是否明确？

**实验优先级**:
- [ ] P0-P2 排序是否合理？
- [ ] 是否有依赖关系被忽略（如 M2 需要 M4 作为前提）？
