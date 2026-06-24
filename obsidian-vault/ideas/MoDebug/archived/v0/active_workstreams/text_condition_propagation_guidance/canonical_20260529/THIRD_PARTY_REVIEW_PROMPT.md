# 第三方复核 Prompt — MoDebug canonical 审计 2026-05-29

请作为独立统计与机制设计复核 agent，复核 MoDebug 文本条件传播 canonical audit。目标不是扩写方案，而是找出 overclaim、统计错误、数据口径错误、failure case 结构化错误和下一步实验优先级问题，尤其要检查旧 semantic-null 结果是否仍被误写为稳健主结论。请用中文输出。

## 需要复核的文件

- 报告：`/data/Life Me/ResearchWY Vault/obsidian-vault/paperIDEAs/MoDebug/active/text_condition_propagation_guidance/canonical_20260529/canonical_audit_report.md`
- 统计主表：`/data/Life Me/ResearchWY Vault/obsidian-vault/paperIDEAs/MoDebug/active/text_condition_propagation_guidance/canonical_20260529/canonical_trace_dedup_400.csv`
- Holm 表：`/data/Life Me/ResearchWY Vault/obsidian-vault/paperIDEAs/MoDebug/active/text_condition_propagation_guidance/canonical_20260529/dedup_400_mannwhitney_holm.csv`
- 协变量敏感性：`/data/Life Me/ResearchWY Vault/obsidian-vault/paperIDEAs/MoDebug/active/text_condition_propagation_guidance/canonical_20260529/covariate_sensitivity.csv`
- `valid_ratio` 相关性：`/data/Life Me/ResearchWY Vault/obsidian-vault/paperIDEAs/MoDebug/active/text_condition_propagation_guidance/canonical_20260529/valid_ratio_partial_corr.csv`
- prompt 相关性：`/data/Life Me/ResearchWY Vault/obsidian-vault/paperIDEAs/MoDebug/active/text_condition_propagation_guidance/canonical_20260529/prompt_delta_correlations.csv`
- annotation join 质量：`/data/Life Me/ResearchWY Vault/obsidian-vault/paperIDEAs/MoDebug/active/text_condition_propagation_guidance/canonical_20260529/annotation_join_quality.csv`
- 结构化 failure factor：`/data/Life Me/ResearchWY Vault/obsidian-vault/paperIDEAs/MoDebug/active/text_condition_propagation_guidance/canonical_20260529/failure_factor_structured_70.csv`
- failure factor 分布：`/data/Life Me/ResearchWY Vault/obsidian-vault/paperIDEAs/MoDebug/active/text_condition_propagation_guidance/canonical_20260529/failure_factor_distribution.csv`、`/data/Life Me/ResearchWY Vault/obsidian-vault/paperIDEAs/MoDebug/active/text_condition_propagation_guidance/canonical_20260529/failure_factor_by_model.csv`

报告中的 `指标与计算规则` 小节是所有统计复核的口径来源。若复算结果与报告不一致，请先指出具体指标、公式或实现差异。

## 当前可疑但待复核的 claims

1. `canonical_trace_dedup_400.csv` 是唯一统计主表，包含 400 个唯一 `(model, sample_id)`。
2. annotation join 完整：400 / 400 joined；trace outcome 与 annotation `is_problem` 一致 400 / 400。
3. 结构化 `failure_factor` 覆盖为 70 / 70。它只能作为 post-hoc 诊断 taxonomy，不能作为机制因果证据。
4. 16 个预设模型 × 指标 Mann-Whitney 检验中，只有 MoLingo `metric_value` 通过 Holm 校正：raw p=0.002060，Holm p=0.032968。
5. MoLingo `metric_value` effect size 报告为 dedup 400 表上的 pooled-SD Cohen's d(success-minus-failure)=-0.9006。
6. MoLingo `metric_value` 只能称为旧 semantic-null historical diagnostic marker；它对包含 MoLingo-only `valid_ratio` 和 prompt length 的现有协变量调整不稳健，不能作为因果、机制证据、final evaluator 或训练/选择依据。
7. 机制设计全部降级：M1 先做 full-vs-event prompt delta；M4 只有 re-forward/regeneration 后才能超出 simulation-only；M2/M3 在 full slot/time tensors 抽取前只是 proxy-only；M5 暂不进入近期主线。
8. 当前 `null_text` 是固定自然语言句子 `This is a null prompt with no semantic meaning.`，不是空字符串、`zero_text`、`standing` 或 pad-only；各模型 null prompt 字符串一致，但 tokenizer/encoder/readout 不同，不能声称 null embedding 一致。
9. 旧 semantic-null delta 结果必须标为 `blocked / historical diagnostic only`，不能作为主结论、机制证据或跨 baseline shared propagation pattern。
10. MotionGPT 四项指标均未通过 Holm 校正，应作为无稳健信号的负结果报告；跨 baseline shared propagation pattern 不成立。

## 必查项

1. 从 `canonical_trace_dedup_400.csv` 重新计算 16 个 Mann-Whitney p 值和 Holm 校正。
2. 用均值、方差和样本数重算 MoLingo `metric_value` 的 pooled-SD Cohen's d。
3. 检查任何未通过 Holm 的结果是否被误写为显著；如果只是 nominal/exploratory，请明确指出。
4. 检查 `covariate_sensitivity.csv` 中 `valid_ratio` 与 prompt length 控制模型，标出 overcontrol、collinearity 或解释错误。
5. 检查文档是否把 `valid_ratio` 写成已证明的 confound、mediator、跨 baseline 解释变量或 final evaluator；若有，要求降级为 MoLingo-only mask/valid diagnostic。
6. 检查 `failure_factor_structured_70.csv` 是否 70 个唯一 case、受控词表合法、`evidence_quote` 来自 `problem_description`、无 `nan`/占位符、`needs_adjudication` 口径一致。
7. 检查所有 M1-M5 机制表述是否都停留在 diagnostic / proxy-only / simulation-only，直到定向实验完成。
8. 检查 `指标与计算规则` 中每个指标是否都有计算规则、计算目的、数值大小含义和限制；若存在跨模型误读风险，请指出。
9. 检查 `机制闭环路线` 是否真正满足“诊断问题 -> 路径数值 -> 判断准则 -> 机制 gate”，是否仍有从相关性直接跳到机制实现的 overclaim。
10. 检查是否明确要求下一步补 `standing` 与 `zero_text` null ablation，并与旧 semantic-null delta 对比；若缺失，视为阻断问题。

## 输出格式

请严格按以下结构输出，不要省略任何小节。若某节没有问题，也要写“无”并给出一句理由。

```text
结论: 有效 / 部分有效 / 无效

阻断问题:
- 无，或列出具体文件、行号、问题、为什么阻断。

非阻断问题:
- 无，或列出具体文件、行号、问题、建议修正。

允许保留的 claims:
- 列出每条 claim，并说明对应证据文件和统计口径。

必须删除或降级的 claims:
- 列出每条 claim，并说明应改成什么保守表述。

下一步实验优先级:
1. 第一优先级实验，包含输入、输出、成功/失败判据。
2. 第二优先级实验，包含输入、输出、成功/失败判据。
3. 第三优先级实验，包含输入、输出、成功/失败判据。
```
