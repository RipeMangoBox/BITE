---
title: "MoDebug sample-level text-condition trace 运行报告"
created: 2026-05-28T14:20:00+08:00
updated: 2026-05-28T15:40:00+08:00
status: completed
tags:
  - MoDebug
  - sample_level_trace
  - f_signal
---

# MoDebug sample-level text-condition trace 运行报告

## 实验是什么

**目的**: 观测 text condition 在 motion generation 模型内部如何影响特征表示，从而理解为什么某些样本生成正确 (success)、某些失败 (failure)。

**方法**: 对每个 baseline 模型，选取 1 个 success sample 和 1 个 failure sample（由 human annotation 判定）。对每个 sample，用**完全相同的内部随机状态**运行两次 forward pass——一次带真实 text prompt (`text`)，一次不带 (`null_text`，用空字符串替换 text input)。两次 forward 的输出张量相减得到 delta，反映 text condition 在模型内部特征空间中产生的**净效应**。

**为什么不是直接比较 success vs failure sample**: success 和 failure 对应**不同的 prompt 和不同的 motion**，它们的基础特征分布不同。正确做法是在**同一个 sample 内部**比较 text vs null_text 的差异，然后对比 success sample 和 failure sample 各自内部的 delta 模式有何不同。

## 指标定义

### delta 张量

```
delta = forward(text_condition="text") − forward(text_condition="null_text")
```

对模型内部某一层 hook 的输出张量，在完全相同随机状态下，text 和 null_text 两次 forward 的逐元素差。

**含义**: delta 的每个元素表示 text embedding 对该特征维度的**偏转方向和幅度**。正值 = text condition 增强了该维度；负值 = text condition 抑制了该维度。

### relative_l2（全局指标）

```
relative_l2 = ||delta||_2 / ||forward(text)||_2
```

其中 `||·||_2` 是整个张量展平后的 L2 范数。

**含义**: text condition 造成的特征变化相对于原始特征幅度的比例。值越大表示 text 对内部状态的**总体影响越强**。没有绝对的"好"范围——关键在于影响是否落在正确的位置。

### per-timestep delta L2（时序指标）

```
per_timestep_l2[t] = sqrt(sum(delta[t, :]^2))
```

对 delta 张量的每个时间步，计算该步所有特征维度的 L2 范数。

**含义**: 反映 text condition 的影响**在时间上的分布**。early-peak 可能表示 text 早期就建立了方向引导；late-peak 可能表示引导来得太晚；均匀分布可能表示没有明确引导。

### time-feature delta mass（时空指标）

将 delta 张量的特征维度分成 N=32 个箱 (bins)，对每个 (时间步, 特征箱) 计算该箱内所有特征维度的 L2 范数。

**含义**: 同时看到 delta **在时间上和在特征空间中的分布**。某些 (时间, 特征区域) 的高 delta mass 可能对应 text 中特定语义信息被路由到的模型内部通道。

## 实验范围

4 baseline × 2 sample outcomes = 8 cases。每 case 有 text 和 null_text 两次 forward 读数和一次 delta 计算。

| Model | Hook 层 | f_space | 张量形状 | 模型族 |
|-------|---------|---------|----------|--------|
| MotionGPT | decoder prefix token logits | motion_vocab_logits | (1, 6, 514) | T5 motion-language |
| MoLingo | latent AR initial state | latent_transformer_z | (1, 49, 1024) | T5 latent-motion |
| MoMask original | base iter 00 codebook logits | vocab_logits | (1, 21-23, 512) | CLIP discrete |
| MoGenTS | grid iter 00 joint logits | time_joint_vocab_logits | (1, 23-38, 6, 256) | CLIP discrete |

**关键差异**: MotionGPT 只在 6 个 decoder step 上观察；MoLingo 的 hook 是 latent AR state 初始步（47-78% 的 latent token 在该步未激活，valid_mask < 1）；MoMask/MoGenTS 的 hook 是首次 mask iteration 的 codebook logits。

## Sample Cases

| Model | Outcome | sample_id | row | failure_factor | relative_l2 |
|-------|---------|-----------|-----|----------------|-------------|
| MotionGPT | success | `hml_orig100_train_003__full` | 2 | | 0.794 |
| MotionGPT | failure | `hml_orig100_train_037__full` | 36 | `missing_subaction` | 0.264 |
| MoLingo | success | `hml_orig100_train_003__full` | 2 | | 0.988 |
| MoLingo | failure | `hml_orig100_train_002__full` | 1 | `trajectory_error` | 1.260 |
| MoMask original | success | `hml_orig100_train_003__full` | 2 | | 1.084 |
| MoMask original | failure | `hml_orig100_train_001__full` | 0 | `artifact_sliding_or_drift` | 1.172 |
| MoGenTS | success | `hml_orig100_train_003__full` | 2 | | 0.849 |
| MoGenTS | failure | `hml_orig100_train_002__full` | 1 | `trajectory_error` | 1.383 |

所有 failure case 满足 `gt_problem=false` 且 `model_problem=true`，排除源 motion/text 质量问题。

### 初步观察

- **MotionGPT failure 的 relative_l2 (0.264) 远低于 success (0.794)**: text condition 几乎没改变 failure sample 的 decoder 输出。text embedding 可能没有有效注入 decoder prefix。
- **MoLingo/ MoMask/ MoGenTS failure 的 relative_l2 均高于或接近 success**: 在这些模型中，failure 不是"text 没起作用"，而是"text 起了作用但引导方向不对"。
- **MoLingo valid_mask = 47-78%**: 约一半 latent token 在初始步未激活，delta 只在这些位置上被观测到。这是一种结构性稀疏，不是错误。

## 可视化

图表位于 `_archive_20260527/visualizations/`。

### Case Cards

![[case_cards.svg]]

每张卡汇总一个 case 的 metadata：模型、outcome、sample_id、prompt、human 标注、failure_factor、relative_l2、motion artifact 路径、manifest 路径。作为 P3 证据索引使用。

### Per-timestep delta L2

![[per_timestep_delta_l2.svg]]

**每张子图**: 同一 baseline 的 success (绿) 和 failure (红) 样本各自的逐时间步 delta L2 柱状图。

**读法**: x 轴 = 模型内部时间步（不同模型含义不同: decoder step / latent token / mask iteration）。y 轴 = 该时间步上 delta 向量的 L2 范数。柱越高 = text condition 在该步产生的特征变化越强。

**例子**: MotionGPT success (绿柱) 在 decoder step 0-2 有明显 delta 峰值，而 failure (红柱) 全程低平——text embedding 没有对 failure 样本的 decoding 产生有效引导。

### Time-feature delta mass 热力图

![[time_feature_delta_mass.svg]]

**每行 = 一个 baseline，左 = success，右 = failure。** x 轴 = 时间步，y 轴 = 特征维度分箱（每组约 D/32 维），颜色 = 该 (时间, 特征箱) 内 delta 的 L2 范数。

**读法**: 红色 = text condition 在该 (时间, 特征区域) 产生了正向偏转；蓝色 = text 产生了负向偏转（null_text 更强）。分布的**结构化程度**比绝对值大小更重要——高度结构化的 pattern（如特定时间步集中在特定特征箱）说明 text 有明确的引导路径；均匀散乱的 pattern 说明 text 的引导没有明确方向。

**跨模型警告**: 不同模型的 f_space 不同（logits vs hidden_state），色标绝对值和空间结构不可直接比较。

## P3 证据链

每个 case 的完整证据链在 artifact 的 `index_outputs/sample_case_index.tsv` 中:

```
sample_id → prompt → human_description → failure_factor
         → motion_artifact_path (MP4)
         → forward_manifest_path → text/npz, null/npz
         → delta_manifest_path → delta/npz
```

`motion_artifact_path` 指向 Original100 的 rendered MP4，可直接打开验证生成质量。

## 验证结果

```
远端: manifest_files=16 manifest_rows=24 ok_rows=24 issue_rows=0
本地: manifest rows=24 ok=24 bad=0
      sample_case_index rows=8
      blank motion_artifact_path=0
      blank prompt=0
```

## 局限

**当前不能声称的结论**:

- **语义特异性**: 没有 random text embedding / semantic perturbation 控制，不能证明 delta 是 text 语义特定的而不是任意 text 都会产生的 general perturbation
- **因果敏感性**: text vs null_text 是最强对比，不能证明 delta 对 text 变化敏感
- **模型排序**: 不同模型 f_space 不同，relative_l2 值不能跨模型比较
- **不是 final evaluator**: delta 是内部诊断信号，不能替代 human evaluation

如果下一步要支持这些结论，需要增加 counterfactual/random 控制、明确 semantic-step temporal boundaries、并引入 held-out evaluator。

## 相关文档

- [实验溯源与脚本路径](provenance.md) — 远端路径、启动脚本、可视化脚本、关键索引
- [400-sample 扩展分析方案](analysis_plan_400_samples.md) — 大规模分析的维度和流水线设计
- [Trace IO Contract](trace_io_contract.md) — forward/delta NPZ 格式规范
