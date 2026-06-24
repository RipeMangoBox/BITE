---
title: "MoDebug 机制设计与实验方案"
created: 2026-05-28T19:00:00+08:00
status: draft
tags: [MoDebug, mechanism_design, experiment_plan, text_condition_propagation]
---

# MoDebug 机制设计与实验方案

基于 400-sample trace 分析 + 论文知识库检索的综合输出。

## 核心发现摘要

### 数据事实 (408 cases, N=4 models × ~102 each)

| 发现 | 证据 | 来源 |
|------|------|------|
| MoLingo 唯一强信号: 所有 delta 指标 success/failure 差异显著 (d=-0.56~-0.97) | Cohen's d + Mann-Whitney U, p<.001 | deep_analysis |
| MotionGPT 零区分能力: metric_value 与 outcome 无统计差异 (p=0.920) | 成功案例可承受 delta_abs_max=149.94 | deep_analysis |
| **valid_ratio 不是 confound**: 偏相关 r=-0.302 ≈ 原始 r=-0.303 | Partial correlation controlling for valid_ratio | deep_analysis |
| Failure 方差 LOWER than success 方差 (MoLingo p=.006, MoGenTS p=.048) | Levene test — 推翻 "noise causes failure" 假说 | deep_analysis |
| MoMask 双峰 failure 模式 (U-shaped): 中段 vs 高端两种 failure | Decile analysis, top decile 50% failure | deep_analysis |
| Prompt 复杂度预测 failure 但不影响 delta 幅度 | failure prompt_length=103.5 vs success=68.2 (p<.0001) | prompt-delta |
| 并行 prompt 最困难：MoMask 67% failure | parallel vs simple: 3.5× gap | prompt-delta |
| delta_mean 是跨模型最一致的信号 (3/4 models significant) | 点二列相关 ranking, Cohen's d | deep_analysis + outcome_classifier |

### 关键洞察

**Failure 机制 ≠ delta 饱和**。Prompt 复杂度高 → 更高失败率，但 delta 幅度不随 prompt 复杂度增加。这说明 failure 来自 **attention collapse** 或 **cross-modal interference**（text embedding 未能有效路由到正确的 motion 维度），而不是 text condition 强度不足。

## 机制设计（5 个候选方向）

### M1: Event-level Text Injection（事件级文本注入）

**问题**: 长 prompt 含多个子动作时，单一 global text embedding 压缩所有语义 → 子动作遗漏。

**机制**: 借鉴 Event-T2M 的 event-level cross-attention。将 prompt 分解为子动作短语，每个短语独立编码为 event embedding，通过 per-event cross-attention 注入 motion decoder 的不同时间步。

**参考论文**: Event-T2M (ICLR 2026), Fg-T2M++ (IJCV 2025)

**预期效果**: 子动作遗漏率下降；delta 时间分布从均匀变为 per-event 峰值。

**最小实验**:
1. 用 LLM 将 100 prompts 解析为子动作序列（已有人工 semantic_steps）
2. 在 MotionGPT decoder 的每步注入对应 event embedding（而非全局 text embedding）
3. 对比 delta trace 的 temporal concentration 变化
4. 评估指标: per-event delta peak alignment, missing_subaction 率

### M2: Sparse Text-to-Feature Routing（稀疏文本-特征路由）

**问题**: Text embedding 均匀影响所有特征维度 → 文本信号被稀释，特定 body part 的引导不精确 → artifact_sliding_or_drift。

**机制**: 在 cross-attention 层后加可学习的 routing gate，将 text features 稀疏路由到相关的 motion feature 子空间（如 MoGenTS 的 joint_grid_slot）。

**参考论文**: LMM/TOMATO part-aware attention (ECCV 2024), PartMotionEdit per-part modulation (arXiv 2025), Hidden Semantic Bottleneck — 条件嵌入 66% 维度可剪枝 (ICLR 2026)

**预期效果**: delta 集中在相关特征子空间；artifact 率下降。

**最小实验**:
1. 对 MoGenTS 的 time-feature delta mass 按 joint_grid_slot 维度聚合，观察当前 text 对各 slot 的选择性
2. 添加 top-K sparse gate（K=2-3 slots），只让 text 影响 delta mass 最大的 slot
3. 对比 full text vs sparse text 的 motion quality 和 delta 分布
4. 评估指标: delta concentration (Gini), artifact_sliding_or_drift 率

### M3: Temporal Consistency Regularization（时序一致性正则）

**问题**: Delta 时序波动大 → text 引导不稳定 → trajectory_error。

**机制**: 在 text condition 注入后添加 temporal smoothing loss，约束相邻时间步的 delta L2 变化率。

**参考论文**: KinemaDiff joint-adaptive noise + structure alignment (ICLR 2026), MotionStream joint text-motion guidance balance (ICLR 2026)

**预期效果**: delta_temporal_std 下降；trajectory_error 率下降。

**最小实验**:
1. 计算当前 400 cases 的 delta_temporal_std 与 trajectory_error 的相关性
2. 在 MotionGPT decoder 输出添加 temporal smoothness loss (λ * ||delta[t] - delta[t-1]||²)
3. 对比有无 regularization 的 delta 时序曲线
4. 评估指标: delta_temporal_std, trajectory_error 率

### M4: Length-Normalized Text Injection（长度归一化文本注入）

**问题**: MoLingo/MoMask 的 delta 幅度与 prompt 长度正相关 → 长 prompt 系统性地过度扰动内部状态。

**机制**: 在 text embedding 注入前进行 L2 归一化，或按 prompt token 数缩放注入强度。

**参考论文**: Hidden Semantic Bottleneck — 条件嵌入极度稀疏，有效维度仅 1-2% (ICLR 2026)

**预期效果**: MoLingo/MoMask 的 prompt_length-delta 相关性降至 ~0；跨 prompt 长度的 failure 率更均匀。

**最小实验**:
1. 对 MoLingo 的 text embedding 按 `1/sqrt(n_tokens)` 缩放
2. 重新计算 100 cases 的 delta，对比归一化前后的 length-delta 相关性
3. 评估指标: prompt_length-delta r 值, per-length-quartile failure 率

### M5: Post-hoc Motion Refinement via FlowEdit（后处理运动修正）

**问题**: 某些 failure 模式（artifact_sliding_or_drift, trajectory_error）可在不重新生成的情况下修正。

**机制**: 使用 FlowEdit ODE 在推理时修改 text condition → 局部修正 motion 的问题区域，保留正确部分。

**参考论文**: Unified Conditional Flow (arXiv 2026), ExpertEdit skill-critical phase masking (arXiv 2026), Iterative Motion Editing MEO operators (SIGGRAPH 2024)

**预期效果**: artifact 和 trajectory error 通过后处理可修正。

**最小实验**:
1. 选取 10 个已知 artifact_sliding_or_drift 的 failure case
2. 对问题时间段的 motion tokens 施加更强的 text guidance（提高该段的 CFG scale）
3. 对比修正前后的 human eval 评分
4. 评估指标: human preference rate, artifact 可见度

## 实验优先级

| 优先级 | 机制 | 理由 | 风险 |
|--------|------|------|------|
| P0 | M4: Length-Normalized Injection | 最简单，一行代码改动，立即可验证 | 可能降低短 prompt 的引导强度 |
| P0 | M2: Sparse Routing | 直接针对 artifact 问题，MoGenTS 已有时空 grid 结构 | routing gate 需要训练或精心设计 |
| P1 | M1: Event-level Injection | 针对最核心的 missing_subaction 问题 | 需要 event temporal boundary（当前无 GT） |
| P1 | M3: Temporal Consistency | 针对 trajectory_error，已有 delta_temporal_std 度量 | 可能使 motion 过于平滑、丧失多样性 |
| P2 | M5: Post-hoc Refinement | 可作为 safety net | 依赖 M1-M4 的效果，增加推理成本 |

## 验证协议

每个机制的验证必须包含:
1. delta trace 对比（before vs after）
2. motion-level human eval（使用现有 Gradio app 做 A/B test）
3. 跨 baseline 泛化性检查（至少 2 个 baseline）
4. 失败判据: 如果 delta 分布无显著变化 + human eval 无改善 → 机制不成立

## 局限

- 所有机制设计基于 387-case analysis，样本量有限
- 当前只有 text/null 控制，机制验证需要 random/semantic perturbation 控制条件
- 跨 baseline 的机制效果不可假设——每个 baseline 的 text injection 路径不同（decoder prefix, latent AR, mask iter）
