---
title: MoDebug Text Propagation Reality Check
created: 2026-05-31T00:00:00+08:00
updated: 2026-05-31T00:00:00+08:00
status: active
hypothesis: 原始的失败案例特征传递路径挖掘还不足以支撑 ICLR 方法论文；可救路线是收窄为可复现局部传播 signature 与推理期因果干预。
tags:
  - MoDebug
  - text_condition_propagation
  - reviewer_risk
  - diagnostic
  - inference_guidance
source_papers: []
related_docs:
  - "[[ideas/MoDebug/README]]"
  - "[[core_idea]]"
  - "[[ideas/MoDebug/roadmap]]"
  - "[[2026-05-22_modebug_risk_boundary_and_claim_control]]"
---

# MoDebug Text Propagation Reality Check

> [!abstract] 决策
> 按“从失败案例无监督寻找文本特征传递路径数据模式，然后直接设计训练机制”原样推进，当前应判为 **Borderline Reject / Reject**。MoDebug 仍可保留，但必须改成一个小闭环：先证明一个局部语义错误簇存在可复现 propagation signature，再用不改参数的 signature-targeted inference intervention 做因果修复。

## 当前证据边界

本记录整合 2026-05-31 的 null-ablation 结果、Agent1 诊断、三路子代理复核和 DeepSeek reviewer 复核。证据角色均为 `diagnostic` / `observation`，不能升级成 final evaluator。

- date: 2026-05-31
- artifact_path: `artifacts/modebug/agent_reports/agent1_null_ablation_text_guidance_diagnostic_20260531.md`
- data_source_zero_text: `artifacts/remote4090/modebug_nullablation_20260531_resume2_zero_text_20260529/text_condition_null_ablation`
- data_source_standing: `artifacts/remote4090/modebug_nullablation_20260531_resume2_standing_20260529/text_condition_null_ablation`
- evaluator: Agent1 local diagnostic aggregation, subagent review, DeepSeek reviewer consultation
- protocol: Original100 failure bank, four baseline sample-level null/standing trace, relative_l2 diagnostic aggregation
- condition_pair: `text_vs_zero_text`, `text_vs_standing`
- n/evaluable: standing 400/400 ok; zero_text 300/400 ok plus MoLingo 100/100 skipped
- role: diagnostic
- used_for: observation
- limitations: small probe set; no held-out final evaluator; MoLingo zero_text not executed; `relative_l2` is internal trace delta, not semantic correctness

## Zero Text / MoLingo Integrity Clarification

`Data Integrity Checks` 中：

```text
condition=zero_text
baseline=molingo
rows=100
status=skipped 100
metric_guard=unsupported_pending_patch 100
numeric rows=0
```

这不是 MoLingo zero_text 运行失败，也不是数据完整性错误。根因是 launcher 明确把 MoLingo `zero_text` 设为 skipped：现有 `force_mask=True` 被记录为 dummy prompt，不是可信的 true zero text / no-condition patch。

可复查路径：

- `scripts/modebug_launch_text_condition_sample_level_remote.py` 中 zero_text 条件说明为 `model_specific_zero_condition_interface_or_skipped_pending_patch`。
- `artifacts/remote4090/modebug_nullablation_20260531_resume2_zero_text_20260529/text_condition_null_ablation/runners/run_molingo_sample_trace.py` 在 `condition_id == "zero_text"` 时写 `skipped_forward_manifest`。
- `artifacts/remote4090/modebug_nullablation_20260531_resume2_zero_text_20260529/text_condition_null_ablation/runners/sample_trace_utils.py` 写入 `status=skipped` 与 `skip_reason=unsupported_pending_patch`。
- `obsidian-vault/paperIDEAs/MoDebug/active/text_condition_propagation_guidance/_archive_20260527/sync_index/build_manifest_index.py` 将 `ok` 和 `skipped` 定义为 non-issue statuses。

因此：

```text
MoLingo text forward trace: 可用
MoLingo zero_text forward trace: 未执行，设计性 skipped
Data integrity issue: 否
MoLingo zero_text ablation result: 不可用，等待 true source patch
```

## Reviewer Verdict

当前主张若写成：

```text
We discover text-feature propagation patterns from failure cases and train a mechanism to improve text-to-motion instruction following.
```

大概率会被拒。最强 reject rationale：

1. `relative_l2` 与人工 success/failure 不稳定相关，无法证明存在可复现的文本传播瓶颈。
2. 当前 trace 主要是 sample-level/global scalar，不能定位 token/span 到 time/body/latent region 的局部错绑。
3. MoLingo zero_text 缺失，旧 semantic-null 又不是 true null；null choice 对结论影响过大。
4. 失败标签是输出症状，不是机制标签；`left_right_error`、`missing_subaction`、`trajectory_error` 不能自动映射为某个传播路径失败。

DeepSeek 的更严格判断是：原始方向按现在证据应视为 `Reject`，除非放弃寻找通用传递模式，改成反事实文本下的局部失败可预测性和推理期处理。

## 为什么当前找不到稳定模式

根因不是“baseline 还不够多”，而是对象混层。

1. **指标层级错位**：`relative_l2` 衡量内部张量整体扰动，不衡量左右、部位、子动作、路径等局部语义是否正确。
2. **null 条件不稳**：semantic null、standing、zero_text 分别有不同语义含义；MoLingo true zero_text 又未实现。
3. **全局标量抹掉路径**：文本传播问题应是 `token/span -> layer/step -> time/body/latent region`，不是单个 sample-level scalar。
4. **模型异质性强**：MoGenTS / MoMask 有弱 margin 趋势，MotionGPT 不支持同一趋势，MoLingo zero_text 缺失。
5. **failure label 不是机制标签**：人工错误类型描述输出，不描述内部路径失效类型。
6. **缺少可逆性测试**：还没有证明增强某个 token/span 或调整某个 guidance 后，目标错误能被独立 evaluator 纠正。

## 可救重定义

安全主张应收窄为：

```text
MoDebug identifies reproducible local text-condition propagation signatures inside pretrained T2M generators and applies minimal inference-time interventions targeted to those signatures.
```

更保守版本：

```text
MoDebug tests whether counterfactual text edits produce localized, predictable changes in motion-generation traces, then uses that predictability to trigger text simplification, token emphasis, candidate reranking, or rejection.
```

当前不应 claim：

```text
MoDebug has discovered a general failure pattern of text-feature transmission.
MoDebug has enough evidence to design a training objective.
```

## 最小 Trace Schema

每条 trace 需要保留以下字段，避免再次落回全局 `relative_l2`：

- `sample_id`, `model`, `seed`, `prompt`, `source_split`, `bucket`, `failure_factor`, `error_type`
- `condition_pair`: `text_vs_zero_text`, `text_vs_standing`, `text_vs_drop_span`, `text_vs_replace_attribute`, `text_vs_counterfactual`
- text side: token ids, attention mask, token/span boundaries, phrase/event spans, attribute spans
- encoder side: token hidden states, pooled condition vector, condition norm
- injection side: projection output, condition scale before/after, cross-attention input
- generator side: per-layer hidden delta, attention mass, logits/confidence, remask/denoising trajectory
- localization side: per-time delta, per-slot/body proxy delta, token-region attribution
- output side: motion path, rendered video, evaluator, protocol, blind label, quality guardrail
- provenance: artifact path, evaluator, n/evaluable, role, used_for, limitations

## Metrics To Pre-Register

设同一样本、同模型、同随机状态下内部 trace 为 `z_c`，其中 `c` 是条件。

Global response:

```text
R_global = ||z_text - z_base||_2 / (||z_base||_2 + eps)
```

Span response:

```text
R_span(s) = ||z_text - z_drop(s)||_2 / (||z_text||_2 + eps)
```

Time concentration:

```text
Delta_t = ||z_t_text - z_t_base||_2
C_t = max_t Delta_t / (sum_t Delta_t + eps)
```

Body or slot selectivity:

```text
TopKShare = sum_{k in TopK} Delta_k / (sum_k Delta_k + eps)
```

Span-to-time alignment:

```text
A(s,t) = sum_{layer,head} Attention_{layer,head}(motion_t, text_span_s)
```

Counterfactual movement:

```text
JSD_attn = JSD(A_text(s, t), A_counterfactual(s, t))
LocalMotionDelta = ||motion_region_text - motion_region_counterfactual||_2
```

Failure-family metrics:

- left/right: `SideMargin = Response(correct_side) - Response(opposite_side)`
- missing subaction: `Coverage(s) = max_t A(s,t)`
- trajectory: `PathAlign = sim(delta_heading_or_root_path, direction_cue)`

统计要求：per-model 预注册；报告 effect size、bootstrap CI、Holm/BH 校正；所有这些仍是 diagnostic，不是 final evaluator。

## Training vs Inference Decision Rule

当前应先做推理机制，不应直接训练。

优先推理机制，当满足：

- 文本条件响应存在，但 failure 的 response margin 较弱或不稳定。
- 错误集中在可通过 token weighting、guidance scale、candidate rerank、text simplification 改变的语义 cue。
- 证据来自小 probe set，尚不足以改 loss 或架构。
- guidance scan 可低成本测试错误是否可逆。

转训练机制，只在满足以下条件后：

- guidance scale、token reweighting、rerank、text rewrite 都无法纠正目标错误。
- token/span/time/body trace 显示相关语义从 projection 或中间层开始系统性不可分。
- 同一 failure signature 在 held-out prompts、多个 seed、至少两个 baseline 或两个 bucket 中复现。
- 有独立 final evaluator，且 dev scorer 不与 final evaluator 重合。
- 训练目标不依赖旧 semantic-null artifact。

## 最小实验闭环

1. 选 3 个 failure family：`wrong_limb_or_side`、`missing_subaction`、`wrong_trajectory_or_path`。
2. 每类选 failure + 同 bucket success comparator；保留 test-source sanity set。
3. 对每个 prompt 构造 full、drop phrase、replace attribute、counterfactual attribute、standing、zero 或 random text 条件。
4. 导出 token/span/time/body trace，而不是只导出 `relative_l2`。
5. 预注册 2-3 个 signature：
   - side cue 低选择性或反向绑定；
   - missing span 的 span-to-time coverage 低；
   - trajectory cue 的 time response 断裂或 heading proxy 错向。
6. 做 inference scan：guidance scale、direction token emphasis、event/span rerank、candidate rerank、text simplification/rewrite。
7. 用 blind human / targeted geometry / quality guardrail 判断 `B` vs `B+MoDebug`。
8. 通过门槛：目标错误率绝对下降至少 30 个百分点，success comparator 不明显退化，至少一个 held-out slice 或第二 baseline 复现。
9. 若失败，再决定是否训练 adapter / contrastive loss / event-level conditioning。

## Stop / Pivot Gates

立即停止原始“泛化传播模式挖掘”路线，如果：

- 新 50 条独立 probe 上，局部反事实 trace 对人工局部跟随标签的 AUROC < 0.70；
- `JSD_attn` 或局部 trace movement 与人工评分 Spearman rho < 0.25；
- guidance scan 只改变全局 motion style，不定向修复目标语义；
- 修复依赖事后挑样本、事后调阈值，不能在 held-out prompt 上复现；
- final evaluator 与 dev scorer 重合，导致无法证明真实质量提升。

如果上述 stop gate 触发，MoDebug 应 pivot 成诊断 benchmark / failure bank / evaluation protocol，而不是继续包装成 ICLR 方法论文。

## Next Action

下一步只做一个小闭环，不再扩散：

1. 选 `left_right_error`、`missing_subaction`、`trajectory_error` 各 10-20 个样本。
2. 为每个样本构造反事实文本和 drop-span 对照。
3. 导出 token/span/time/body trace。
4. 先做 inference-time semantic guidance 或 candidate rerank。
5. 用盲评和几何 guardrail 判断是否达成定向修复。

只有这个闭环成立，才讨论训练机制。
