---
title: "MoDebug 文本条件传播 canonical 审计 2026-05-29"
created: 2026-05-29
status: active
role: canonical-audit
tags:
  - MoDebug
  - text_condition_propagation
  - canonical_audit
---

# MoDebug 文本条件传播 canonical 审计 2026-05-29

## 审计结论

**部分有效，但 semantic-null 主结论被阻断。** 基于 `delta_tensor_summary.json` 重建 canonical trace 后，在 16 个预设的模型 × 指标 Mann-Whitney 检验中，只有 **MoLingo `metric_value`** 通过 Holm 校正。由于当前 `null_text` 是固定自然语言句子 `This is a null prompt with no semantic meaning.`，所有 text-vs-semantic-null delta 结果只能作为 `blocked / historical diagnostic only`，不能作为主结论、机制证据或训练/选择依据。所有机制 claim 都必须保持在诊断层，直到补齐 `standing` 与 `zero_text` null ablation，并完成与旧 semantic-null delta 的对比。

## 数据口径

| 字段 | 值 |
|-------|-------|
| date | 2026-05-29 |
| artifact_path | `canonical_20260529/` |
| protocol | text vs semantic-null forward trace；Mann-Whitney U 双侧检验；对 16 个模型 × 指标检验做 Holm 校正；当前口径为历史诊断 |
| motion_source | HumanML3D Original100 诊断子集，四个 baseline 输出 |
| condition_pair | `forward(text)` vs `forward(null_text)`，其中 `null_text="This is a null prompt with no semantic meaning."` |
| n/evaluable | 400 / 400 个唯一 `(model, sample_id)` |
| coverage | annotation join 400 / 400；trace/annotation outcome 一致 400 / 400；结构化 `failure_factor` 覆盖 70 / 70 个 failure 样本 |
| role | blocked for main claim；historical diagnostic only |
| used_for | observation |
| limitations | 不是 held-out final evaluation；semantic-null delta 不能作为主结论或机制证据；必须补 `standing` 与 `zero_text` null ablation 并与旧 semantic-null delta 对比；结构化 `failure_factor` 是 post-hoc 人工/agent 诊断分类；M2/M3 的 full time/slot tensors 目前只看到 pilot 导出；M4 的 post-hoc scaling 只能称为 simulation-only，除非实际 re-forward/regeneration |

## 数据概览

| 项目 | 值 |
|------|------:|
| 统计主表行数 | 400 |
| annotation join 覆盖 | 400 / 400 |
| annotation/trace outcome 一致 | 400 / 400 |
| 结构化 `failure_factor` 覆盖 | 70 / 70 个 failure 样本 |

## 指标与计算规则

### semantic-null 与 trace 条件

当前 `null_text` 的输入不是空字符串，也不是 pad-only embedding；它是固定自然语言句子：`This is a null prompt with no semantic meaning.`。因此本文所有 delta 都表示“真实文本相对这个固定 semantic-null prompt 的内部 trace 变化”，不是相对零向量、站立基线或绝对无条件模型的变化。这个旧 semantic-null 口径现在标为 `blocked / historical diagnostic only`：可保留统计事实和复核线索，但不能作为稳健主结论、跨 baseline 传播模式或机制证据。

| 模型 | null_text 输入 | 文本编码或条件入口 | 当前保存的表征 | 数值规则与限制 |
| --- | --- | --- | --- | --- |
| MotionGPT | `This is a null prompt with no semantic meaning.` | MotionGPT 的 tokenizer 和 language model；固定 decoder prefix | `token_logits`，空间为 `motion_vocab_logits_slice`，shape 为 `[batch, decoder_step, motion_vocab]` | null prompt 字符串与其他模型相同，但 tokenization、encoder 和输出空间不同；forward NPZ 未保存 text embedding 本体 |
| MoLingo | `This is a null prompt with no semantic meaning.` | MoLingo `forward_z`；T5-large local path；固定 masked latent state | `hidden_state`，空间为 `latent_transformer_z`，shape 为 `[batch, latent_token, hidden_dim]` | 只保存下游 hidden state，不保存 token embedding 或 pooled text embedding；不能和 MotionGPT 的 T5 系输出直接等同 |
| MoMask original | `This is a null prompt with no semantic meaning.` | MoMask transformer `encode_text`；`model_family=clip_discrete`；固定 full-mask state | `token_logits`，空间为 `vocab_logits`，shape 为 `[batch, token_time, codebook]` | 保存的是 post cond-scale logits，不是 CLIP text embedding；不能与 MoGenTS 直接比较尺度 |
| MoGenTS | `This is a null prompt with no semantic meaning.` | MoGenTS `encode_text`；CLIP ViT-B/32；固定 time-joint full-mask grid | `token_logits`，空间为 `time_joint_vocab_logits`，shape 为 `[batch, token_time, joint_grid_slot, codebook]` | `joint_grid_slot` 是内部 2D code grid slot，不是命名身体关节；不能直接解释为左手、右脚等物理部位 |

| 问题 | 当前结论 | 后续若要回答需要新增的记录 |
| --- | --- | --- |
| null text 具体输入是什么 | 固定句子 `This is a null prompt with no semantic meaning.`；该旧 semantic-null 结果为 blocked / historical diagnostic only | 必须补 `standing` 与 `zero_text` null ablation，并与旧 semantic-null delta 对比；可同时记录 empty string、pad-only、random text、shuffled text 等对照，检查 null 选择是否影响结论 |
| null text 对应的 text embedding 是什么 | 当前正式 artifact 未落盘 embedding 本体；只保存 text/null forward 后的下游 `signal` | 保存 token ids、attention mask、encoder hidden states、pooled condition vector、conditioning scale 前后的 cond_vector |
| 不同模型的 null embedding 是否一致 | 字符串一致；embedding 不能认为一致。不同 tokenizer、encoder、conditioning wrapper、读出层和信号空间都会改变向量含义 | 同一 prompt 在各模型中分别导出 text encoder 输出，并做模型内归一化；跨模型只比较归一化趋势，不比较 raw magnitude |
| delta 指标的计算意义 | 衡量同一模型、同一生成状态、同一 trace 位置上，真实文本相对旧 semantic-null prompt 改变内部信号的强度、方向和分布 | 必须先做 `standing` 与 `zero_text` ablation，并加入 random/semantic perturbation/event prompt/re-forward 生成结果，才能讨论机制或可干预效果 |

### Trace、prompt 与标签指标

| 指标 | 计算规则 | 计算目的 | 数值规则与大小含义 | 限制 |
| --- | --- | --- | --- | --- |
| `delta` | 同一随机状态和同一 trace 位置下的 `forward(text) - forward(null_text)`；无效 mask 位置在保存 delta 中置为 0 | 表示文本条件对内部信号的逐元素影响 | 正值表示 text 方向的该元素大于 null；负值表示小于 null；局部符号只在同一模型同一信号空间内有意义 | 不是 motion error；不同模型的 delta 空间不可直接比较 |
| `metric_value` | 当前 `metric_name=relative_l2`；在 valid entries 上计算 `L2(forward(text)-forward(null_text)) / L2(forward(null_text))` | 给每个样本一个旧 semantic-null text sensitivity 标量 | 越大表示该 readout 对 text 条件相对 semantic-null 的整体变化越强；本文只能在模型内做历史诊断比较 | blocked / historical diagnostic only；不是 final evaluator；不表示语义正确；受 MoLingo `valid_ratio`、prompt length 和 null denominator 影响 |
| `delta_abs_max` | `max(abs(delta))` | 捕捉最强单点变化 | 越大表示某个元素出现更大的局部变化 | 容易受 outlier 和 logit 尺度影响；Holm 后未形成稳健结论 |
| `delta_mean` | `mean(delta)` | 观察整体 signed shift | 正值表示 text 相对 null 的平均方向为正；负值表示平均方向为负 | 正负号依赖 logit或hidden-state坐标定义，跨模型不能解释；Holm 后不支持主结论 |
| `delta_std` | `np.std(delta)`，`ddof=0` | 观察 delta 在张量内的离散程度 | 越大表示变化更分散或幅度更不均匀 | 不告诉变化是否落在语义相关 token、time 或 slot |
| `valid_ratio` | 有 `valid_mask` 时取 `mean(valid_mask)`；无 mask 时记为 `1.0` | MoLingo-only mask/valid diagnostic，衡量 MoLingo 有多少 fixed latent token 位置参与有效计算 | 在 MoLingo 中值越大，参与 L2 的位置越多；其他 baseline 当前基本为常数或不可解释 | 不是跨 baseline confound/mediator，不是 final evaluator，也不能解释为语义质量或机制变量 |
| `delta_numel` | `delta_shape` 各维度乘积 | 记录 delta 张量规模 | 越大表示 trace 元素更多 | 只作 schema 说明，不作机制证据 |
| `delta_ndim` | `delta_shape` 的维度数 | 记录 trace 张量阶数 | 3D/4D 代表不同读出结构 | 不同 ndim 不代表机制强弱 |
| `outcome_bin` | `failure=1`，`success=0` | 供相关和回归使用 | 正相关表示指标随 failure 增大 | 标签来自 trace outcome，不是连续质量分数 |
| `prompt_length` | prompt 字符数 | 检查长度与 delta 或 failure 的关系 | 越大表示文本更长 | 长度是难度 proxy，不等于语义复杂度 |
| `prompt_word_count` | 按空格切分词数 | 粗略文本长度特征 | 越大表示词数更多 | 不处理短语、复合词或语义角色 |
| `n_sub_actions` | 预定义动作关键词出现次数 | 粗略估计动作数量 | 越大表示启发式动作词更多 | 不是人工事件分解；不能直接作为事件标签 |
| `temporal_complexity` | `0=simple`，`1=包含 then`，`2=包含 while`；同时出现时按 2 | 粗略估计时序结构 | 2 表示并行提示，1 表示顺序提示，0 表示未显式触发 | 只是规则特征，不等于真实时序复杂度 |
| `failure_factor count` | 70 个 failure 样本中每个一级标签的计数 | 识别 failure description 的主要诊断簇 | count 越大表示该错误类型出现越多 | post-hoc taxonomy，不是机制因果证据 |
| `failure_factor percent` | `count / 70` | 给出一级标签占比 | 越大表示该错误类型在 failure 中占比更高 | 分母只包含 failure，不代表总体失败率 |

### 统计检验与效应量

| 指标 | 计算规则 | 计算目的 | 数值规则与大小含义 | 限制 |
| --- | --- | --- | --- | --- |
| `n_success` / `n_failure` | 每个模型内部 success / failure 样本数 | 给统计检验分母 | 数量越小，估计越不稳定 | 不同模型失败数不同，解读 effect size 时需同时看 n |
| `mean_success` / `mean_failure` | 每个模型内部、每个指标在 success / failure 组的均值 | 描述组间中心差异 | failure 均值更大不自动代表更差，只说明该 trace 指标更大 | 均值受 outlier 影响 |
| `var_success` / `var_failure` | 每组样本方差，`ddof=1` | 描述组内离散程度 | 值越大表示同组样本差异越大 | 方差差异不等于 failure 噪声因果机制 |
| `Cohen's d（成功-失败）` | pooled-SD effect size；`d=(mean_success-mean_failure)/s_pooled` | 量化 success/failure 差异大小 | `d < 0` 表示 failure 组指标更大；绝对值越大，标准化差异越大 | 不是显著性；需配合 p 值和多重校正 |
| `Mann-Whitney p` | 每个模型内部 success vs failure 的 Mann-Whitney U 双侧检验；SciPy `method=auto` | 主检验 raw p | 越小表示两组分布差异越难由零假设解释 | 本报告有 16 个主检验，不能只看 raw p |
| `Welch p` | success vs failure 的 Welch t-test 双侧 p | 辅助检查均值差异 | 越小表示均值差异更强 | 不属于 primary Holm family |
| `Levene p` | Levene 方差检验，`center=median` | 辅助检查方差差异 | 越小表示两组方差更可能不同 | 不属于 primary Holm family |
| `Holm p（16 次检验）` | 对 4 个模型乘 4 个 trace 指标的 16 个 Mann-Whitney p 做 Holm-Bonferroni；排序后用 `(16-i+1)*p_(i)` 并取前缀最大、截断到 1 | 控制 family-wise error | `< 0.05` 才作为本报告主显著结果 | 当前只有 MoLingo `metric_value` 存活 |
| `BH-FDR p（16 次检验）` | 对同一 16 个 Mann-Whitney p 做 Benjamini-Hochberg；排序后用 `16/i*p_(i)` 并取后缀最小、截断到 1 | 辅助观察 FDR 口径 | 越小表示在 FDR 控制下越强 | 本报告主结论仍以 Holm 为准 |
| `Pearson r` / `p` | Pearson 线性相关及双侧 p；failure 相关使用 `outcome_bin` | 检查线性相关方向 | `r > 0` 正相关，`r < 0` 负相关；绝对值越大线性关系越强 | 相关不是因果；对非线性不敏感 |
| `partial r` / `partial p` | 分别用 `intercept + valid_ratio` 回归 `metric_value` 与 `outcome_bin`，再对残差做 Pearson 相关 | 检查控制 `valid_ratio` 后的残差关联 | 绝对值越大表示控制后线性残差关联越强 | 只控制一个协变量；不能证明 confound 或 mediator 身份 |
| `OLS 失败-成功系数` | 线性模型 `metric_value ~ 1 + outcome_bin + covariates` 中 `outcome_bin` 的系数 | 诊断协变量敏感性 | 正值表示控制后 failure 组 `metric_value` 更大；负值相反 | 线性模型；受共线性和 overcontrol 影响 |
| `OLS outcome p` | 上述 OLS outcome 系数的双侧 t 检验 p | 辅助判断控制后关联 | 越小表示系数更稳定 | 不属于 primary Holm family |
| `残差 Mann-Whitney p` | 先用协变量回归 `metric_value` 并取残差，再对 success/failure 残差做 Mann-Whitney U 双侧检验 | 非参数残差敏感性检查 | 越小表示控制协变量后的残差分布差异越强 | 探索性检查，不是主显著性判据 |
| `残差 d（成功-失败）` | 残差上的 pooled-SD Cohen's d | 描述控制后的效应大小 | `d < 0` 表示 failure 残差更大 | 不能单独作为机制证据 |
| `annotation join 覆盖` | `annotation_found=True` 行数除以 400 | 检查人工描述连接完整性 | 越接近 1 越完整 | 只说明 join 覆盖，不说明标签正确性 |
| `annotation/trace outcome 一致` | `annotation_is_problem` 与 `outcome=="failure"` 一致的行数除以 400 | 检查 outcome 口径一致性 | 越接近 1 越一致 | 不代表 failure_factor taxonomy 是因果机制 |

## failure_factor 结构化结果

结构化 `failure_factor` 只用于 post-hoc 诊断分类；不允许把类别分布升级为机制因果证据。

### 一级标签分布

| failure_factor | 数量 | 占比 |
| --- | --- | --- |
| wrong_limb_or_side | 27 | 0.3857 |
| missing_subaction | 13 | 0.1857 |
| wrong_trajectory_or_path | 11 | 0.1571 |
| timing_or_duration_error | 6 | 0.08571 |
| pose_or_contact_artifact | 5 | 0.07143 |
| overgeneration_or_extra_motion | 3 | 0.04286 |
| orientation_or_facing_error | 2 | 0.02857 |
| wrong_action | 2 | 0.02857 |
| semantic_mismatch | 1 | 0.01429 |


## 统计检验

主检验为 Mann-Whitney U 双侧检验，并对 16 个模型 × 指标组合做 Holm 校正。`Cohen's d（成功-失败）< 0` 表示 failure 组的指标值更大。

| 模型 | 指标 | 成功数 | 失败数 | Cohen's d（成功-失败） | Mann-Whitney p | Holm p（16 次检验） | BH-FDR p（16 次检验） | Holm 0.05 显著 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| MoGenTS | metric_value | 79 | 21 | -0.08427 | 0.2198 | 1 | 0.3907 | 否 |
| MoGenTS | delta_abs_max | 79 | 21 | -0.3809 | 0.0506 | 0.5608 | 0.1349 | 否 |
| MoGenTS | delta_std | 79 | 21 | -0.2971 | 0.493 | 1 | 0.6068 | 否 |
| MoGenTS | delta_mean | 79 | 21 | -0.6053 | 0.04673 | 0.5608 | 0.1349 | 否 |
| MoLingo | metric_value | 88 | 12 | -0.9006 | 0.00206 | 0.03297 | 0.03297 | 是 |
| MoLingo | delta_abs_max | 88 | 12 | -0.9428 | 0.005363 | 0.08045 | 0.04291 | 否 |
| MoLingo | delta_std | 88 | 12 | -0.5311 | 0.08477 | 0.8477 | 0.1938 | 否 |
| MoLingo | delta_mean | 88 | 12 | -0.7556 | 0.01074 | 0.145 | 0.04296 | 否 |
| MoMask original | metric_value | 77 | 23 | -0.4872 | 0.1382 | 1 | 0.2764 | 否 |
| MoMask original | delta_abs_max | 77 | 23 | 0.01393 | 0.8699 | 1 | 0.9279 | 否 |
| MoMask original | delta_std | 77 | 23 | 0.08368 | 0.9804 | 1 | 0.9804 | 否 |
| MoMask original | delta_mean | 77 | 23 | -0.6647 | 0.01036 | 0.145 | 0.04296 | 否 |
| MotionGPT | metric_value | 86 | 14 | -0.1601 | 0.3634 | 1 | 0.4915 | 否 |
| MotionGPT | delta_abs_max | 86 | 14 | -0.2341 | 0.353 | 1 | 0.4915 | 否 |
| MotionGPT | delta_std | 86 | 14 | -0.1606 | 0.3686 | 1 | 0.4915 | 否 |
| MotionGPT | delta_mean | 86 | 14 | 0.1134 | 0.637 | 1 | 0.728 | 否 |

### Holm 后存活项

| 模型 | 指标 | Cohen's d（成功-失败） | Mann-Whitney p | Holm p（16 次检验） |
| --- | --- | --- | --- | --- |
| MoLingo | metric_value | -0.9006 | 0.00206 | 0.03297 |

Effect size 口径：`Cohen's d（成功-失败）` 是在每个模型内部、基于去重 400 行表计算的 pooled-SD Cohen's d。MoLingo `metric_value` 的存活项如下：

| 模型 | 指标 | 成功数 | 失败数 | 成功均值 | 失败均值 | Cohen's d（成功-失败） |
| --- | --- | --- | --- | --- | --- | --- |
| MoLingo | metric_value | 88 | 12 | 1.11 | 1.216 | -0.9006 |

## 协变量敏感性

`valid_ratio` 只能作为 MoLingo-only mask/valid diagnostic。当前可 defend 的说法更窄：在 MoLingo 中，`valid_ratio` 与 `metric_value` 强相关，但它与 outcome 的直接相关在当前样本中不显著；它不能被写成跨 baseline confound/mediator、机制变量或 final evaluator。

| 模型 | 样本数 | valid_ratio 唯一值数 | r(valid_ratio, failure) | p(valid_ratio, failure) | r(metric_value, failure) | p(metric_value, failure) | r(metric_value, valid_ratio) | p(metric_value, valid_ratio) | partial r(metric_value, failure; control valid_ratio) | partial p |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| MoGenTS | 100 | 1 | 不适用 | 不适用 | 不适用 | 不适用 | 不适用 | 不适用 | 不适用 | 不适用 |
| MoLingo | 100 | 34 | 0.1107 | 0.2727 | 0.2835 | 0.00426 | 0.6461 | 3.892e-13 | 0.2794 | 0.004873 |
| MoMask original | 100 | 1 | 不适用 | 不适用 | 不适用 | 不适用 | 不适用 | 不适用 | 不适用 | 不适用 |
| MotionGPT | 100 | 1 | 不适用 | 不适用 | 不适用 | 不适用 | 不适用 | 不适用 | 不适用 | 不适用 |

下面是 MoLingo `metric_value` 的诊断性控制检查。`OLS 失败-成功系数 > 0` 表示控制所列协变量后 failure 组的 `metric_value` 更大。残差 Mann-Whitney 检验只是探索性检查，不属于 16-test primary Holm family。

| 模型 | 指标 | 控制变量 | 成功数 | 失败数 | OLS 失败-成功系数 | OLS outcome p | 残差 Mann-Whitney p | 残差 d（成功-失败） |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| MoLingo | metric_value | prompt_length | 88 | 12 | 0.04868 | 0.187 | 0.3701 | -0.3793 |
| MoLingo | metric_value | valid_ratio | 88 | 12 | 0.08093 | 0.005097 | 0.006726 | -0.8806 |
| MoLingo | metric_value | valid_ratio+prompt_length | 88 | 12 | 0.05552 | 0.06492 | 0.1762 | -0.5346 |

解释：只控制 MoLingo `valid_ratio` 不会移除 MoLingo `metric_value` 与 outcome 的关联；但 prompt-length-only 和 `valid_ratio + prompt_length` 联合调整后，残差 Mann-Whitney 关联不再保留。这不能说明 prompt length 是唯一 confounder，也不能把 `valid_ratio` 升级成跨 baseline confound/mediator。更安全的表述是：Holm 后存活的结果对现有协变量调整不稳健，只能作为 historical diagnostic，不能作为稳定因果机制。

### Prompt length 相关性

`prompt_length` 与 `metric_value` 的关系必须 per-model 阅读；合并相关较弱，不应作为主结论。

| 范围 | 样本数 | Pearson r | p |
| --- | --- | --- | --- |
| 合并 | 400 | 0.1091 | 0.02912 |
| MoGenTS | 100 | 0.1622 | 0.1069 |
| MoLingo | 100 | 0.4527 | 2.252e-06 |
| MoMask original | 100 | 0.2792 | 0.004901 |
| MotionGPT | 100 | -0.09547 | 0.3447 |

## 可保留与必须降级的 claims

可保留：

- `canonical_trace_dedup_400.csv` 是唯一统计主表，包含 400 个唯一 `(model, sample_id)`。
- 结构化 `failure_factor` 已覆盖 70 / 70 个 failure 样本；只能作为人工诊断 taxonomy，不是机制证据。
- 16 个模型 × 指标 Mann-Whitney 检验经 Holm 校正后，只有 MoLingo `metric_value` 存活。
- MoLingo `metric_value` 只能称为旧 semantic-null historical diagnostic marker，且对现有 MoLingo `valid_ratio` 与 prompt length 协变量调整不稳健。
- MotionGPT 四项指标均未通过 Holm 校正，可作为无稳健信号的负结果报告。
- 跨 baseline shared propagation pattern 不成立；当前只有单模型 MoLingo `metric_value` 历史诊断信号，不能写成跨模型共享传播规律。

必须删除或降级：

- 删除：“MoLingo 所有 delta 指标显著。”Holm 校正后只有 `metric_value` 存活。
- 删除：“`delta_mean` 是跨模型最一致信号。”没有任何 `delta_mean` 结果通过 Holm 校正。
- 删除：“跨 baseline 存在 shared propagation pattern。”当前统计不支持；MotionGPT 无稳健信号，其他 baseline 未通过 Holm。
- 降级任何把旧 semantic-null delta 当作稳健主结论或机制证据的表述。应改为：旧 semantic-null delta 是 `blocked / historical diagnostic only`，必须补 `standing` 与 `zero_text` ablation 后才能重审。
- 降级：“`valid_ratio` 不是 confound。”应改为：`valid_ratio` 只是 MoLingo-only mask/valid diagnostic，当前数据不能确立 confound 或 mediator 身份，更不能跨 baseline 解释。
- 降级：“MoLingo `metric_value` 对协变量稳健。”应改为：MoLingo `metric_value` 是唯一 Holm 后存活的诊断 marker，但对现有 `valid_ratio` 和 prompt length 协变量调整不稳健。
- 降级：“failure 来自 attention collapse。”应改为：attention collapse 只是未验证的机制假设。
- 降级：M2/M3 不能进入机制实现，必须先做 proxy extraction。

## 修正后的机制状态

| 机制 | 当前状态 | 下一道 gate |
|-----------|--------|-----------|
| M4 length-normalized injection | 历史诊断线索，主结论阻断 | 先补 `standing` 与 `zero_text` null ablation；post-hoc rescaling 只能标注为 simulation-only；真实 claim 需要 re-forward 或 regeneration |
| M1 event-level conditioning | 诊断目标 | 模型改动前先做 full prompt vs event prompt delta 对比 |
| M2 sparse routing | proxy-only | 先提取 slot concentration / Gini / selectivity |
| M3 temporal consistency | proxy-only | 先提取 per-case temporal delta std/diff，并 join trajectory_error 标签 |
| M5 FlowEdit refinement | 尚无支持 | 不进入近期主线 |

## 机制闭环路线

当前证据的正确用法是“发现可验证的诊断规律”，而不是直接推出机制。闭环顺序固定为：`failure description 分簇 -> 路径数值采集 -> 模型内统计判据 -> 小规模可干预机制 -> re-forward/regeneration 验证`。

| failure 簇或目标 | 当前事实 | 需要进一步发现的规律 | 需要采集的路径数值 | 希望看到的数值特性 | 判断准则 | 可能机制 | 当前 gate |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `wrong_limb_or_side` | 27 / 70，是最大 failure 簇 | 侧别、左右肢体或身体部位词是否在生成路径中被弱化、混淆或路由到错误位置 | text token ids；body-part token span；encoder hidden states；cross-attention 或 conditioning-to-token attribution；time/slot delta mass；左右肢体轨迹或接触 proxy | 成功样本应在对应肢体词和相关时间段出现更集中、更稳定的 attribution；失败样本若出现侧别翻转，应表现为左右相关 proxy 的反向或低选择性 | 在同一模型内，相关 proxy 对该 failure 簇 vs 其他 failure/成功有可重复差异；优先要求 Holm 或预注册 family 内校正后保留 | M1 event-level conditioning；后续可接 M2 sparse routing | 先导出 token-level attribution 和左右 proxy；不能只用全局 `metric_value` |
| `missing_subaction` | 13 / 70 | 多子动作 prompt 是否发生尾部动作遗忘或动作覆盖 | 人工/LLM 子动作 span；span order；per-span attribution；每个时间段的 delta mass；生成 motion 的事件边界或动作片段 proxy | 成功样本应出现 span-to-time 的多峰覆盖；失败样本若缺子动作，应在缺失 span 上 attribution 或对应 time mass 明显不足 | 缺失子动作对应 span 的 attribution/time mass 低于成功或非缺失样本，并能定位到具体 span | M1 event-level conditioning；M4 length-normalized injection；必要时 M2 sparse routing | 先完成 full prompt vs event prompt delta 对比；没有 event span 不进入模型改动 |
| `wrong_trajectory_or_path` | 11 / 70 | 方向、路径、转身等空间词是否在时间维上持续传播 | direction/path token span；root trajectory；heading/yaw；per-time delta L2；trajectory-error 标签 | 成功样本应在路径相关时间段有持续 delta 或稳定 heading/root proxy；失败样本可能出现 delta 高但轨迹 proxy 错，或 delta 在关键时间段断裂 | path proxy 与对应 failure_factor 的相关在模型内成立，并能区分 direction/path failure 与其他 failure | M3 temporal consistency；event-level path conditioning | 先补全 full per-case time tensors 和 trajectory proxy |
| `timing_or_duration_error` | 6 / 70 | slowly/quickly/while/then 等时序词是否影响速度和动作顺序 | temporal token span；frame velocity；acceleration；event order；per-time delta variance | 成功样本的速度、持续时间或顺序 proxy 应与时序词一致；失败样本出现速度方差异常或事件顺序错位 | timing proxy 与 timing failure 在模型内有方向一致的差异；样本量不足时只作 pilot | M3 temporal consistency | 当前 n 小，先作为诊断补充，不作为主线 |
| 全局 text sensitivity | 只有 MoLingo `metric_value` Holm 后存活，但属于旧 semantic-null historical diagnostic，且对 `valid_ratio` 和 prompt length 不稳健 | 全局 text-vs-null 强度是否只是长度/有效 token 数或 semantic-null 选择导致，还是包含 failure-specific 信息 | MoLingo `valid_ratio`；prompt features；null denominator norm；`standing` delta；`zero_text` delta；random text delta；semantic perturbation delta；event prompt delta | 合理机制目标应在控制长度、valid tokens 和 null denominator 后仍保留 failure-specific 方向，并且不依赖旧 semantic-null | 预注册控制后仍保留，且在 `standing` 与 `zero_text` 对照下方向可复核 | M4 或重新设计指标 | 先补 `standing` 与 `zero_text` null ablation，并与旧 semantic-null delta 对比；不把现有 `metric_value` 当训练目标 |

### 机制优先级与采集路线

| 优先级 | 机制 | 为什么排这个位置 | 先采集什么 | 通过 gate 后才允许的实现 |
| --- | --- | --- | --- | --- |
| P1 | M1 event-level conditioning | 最大 failure 簇集中在 side/limb 和 missing_subaction；二者都需要把全局 prompt 拆成可定位事件或部位条件 | event/body-part span；span-level text embedding；span-to-time attribution；full vs event prompt delta | 在 MoLingo/MoMask/MoGenTS 至少一个模型内证明 event/span proxy 能区分相关 failure 后，再做 event-level 条件注入 |
| P2 | M4 length-normalized injection | MoLingo `metric_value` 与 MoLingo-only `valid_ratio`/prompt length 敏感；且旧 semantic-null 口径已阻断主结论，只能先当归一化或鲁棒性问题 | `standing` 与 `zero_text` null ablation；旧 semantic-null delta 对比；empty/null/random/semantic perturbation 对照；null denominator norm；控制 prompt_length 和 valid_ratio 后的 residual delta | 若在 `standing` 和 `zero_text` 对照下 failure-specific signal 仍保留，可做 re-forward；若只在旧 semantic-null 下存在，则说明原 metric 主要是 null-choice artifact |
| P3 | M2 sparse routing | 需要 token/slot 选择性证据；目前只有全局标量，不足以实现 | slot concentration；Gini；top-k token attribution；time-slot selectivity | 只有当 failure 簇对应低选择性或错误路由时，才设计 sparse routing |
| P4 | M3 temporal consistency | trajectory/timing 类 failure 有意义，但当前 full time tensor 不全，样本簇较小 | per-time delta L2；frame velocity；root path；heading；event boundary | 只有 time proxy 和 trajectory/timing failure 对齐后，才做 temporal constraint |
| P5 | M5 FlowEdit refinement | 可作为后处理，但当前没有 latent edit direction 和成功判据 | 局部编辑方向；pre/post edit motion metrics；side/path/timing targeted evaluator | 只有已有明确错误方向和可自动评价器时进入，不作为近期主线 |

## 最小下一步

1. 每次引用 MoLingo `metric_value` 诊断关联时，都必须标为旧 semantic-null `blocked / historical diagnostic only`，同时报告 MoLingo `valid_ratio` 与 prompt length 敏感性。
2. 重新实验时必须补 `standing` 与 `zero_text` null ablation，并与旧 semantic-null delta 对比；可额外加入 empty string、pad-only、random text、semantic perturbation，所有结果必须报告 null 选择敏感性。
3. 保存 text embedding 路径：token ids、attention mask、encoder hidden states、pooled condition vector、cond-scale 前后向量；否则不能回答 embedding 一致性或 token 传播问题。
4. 在实现 event-level conditioning 前，先跑 M1 full prompt vs event prompt delta 对比，并把 event span 与 failure_factor join。
5. 只有拿到 full per-case time/slot delta tensors 后，才提取 M2/M3 proxies；当前 per-timestep CSV 只覆盖 pilot 8 cases。
6. M4 只能二选一：标注为 simulation-only 的 post-hoc rescaling，或实际 re-forward/regeneration；两者不能混写。
