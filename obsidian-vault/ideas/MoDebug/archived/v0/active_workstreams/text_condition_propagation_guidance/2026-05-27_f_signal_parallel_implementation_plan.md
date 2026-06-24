---
title: "MoDebug f-Signal Parallel Implementation Plan"
created: 2026-05-27T00:00:00+08:00
updated: 2026-05-27T00:00:00+08:00
status: active
hypothesis: "在固定生成状态 z 时，比较 f(z, text) 与 f(z, null/random/counterfactual text) 可以定位 text condition 在 pretrained motion generator 内部的传播强度、语义特异性和绑定位置。"
tags:
  - MoDebug
  - text_condition_propagation
  - f_signal
  - parallel_agent_plan
source_papers:
  - "[[paperAnalysis/Motion_Generation/NeurIPS_2023/2023_MotionGPT_Human_Motion_as_Foreign_Language|MotionGPT]]"
  - "[[paperAnalysis/Motion_Generation/CVPR_2024/2024_MoMask_Generative_Masked_Modeling_of_3D_Human_Motions|MoMask]]"
  - "[[paperAnalysis/Motion_Generation/NeurIPS_2024/2024_MoGenTS_Motion_Generation_based_on_Spatial_Temporal_Joint_Modeling|MoGenTS]]"
  - "[[paperAnalysis/Motion_Generation/ICLR_2023/2023_MDM_Human_Motion_Diffusion_Model|MDM]]"
  - "[[paperAnalysis/Motion_Editing/SIGGRAPH_Asia_2024/2024_MotionFix_Text_Driven_3D_Human_Motion_Editing|MotionFix]]"
  - "[[paperAnalysis/Motion_Generation/CVPR_2023/2023_MLD_Executing_your_Commands_via_Motion_Diffusion_in_Latent_Space|MLD]]"
  - "[[paperAnalysis/Motion_Generation/ICCV_2025/2025_FineMotion_A_Dataset_and_Benchmark_with_both_Spatial_and_Temporal_Annotation_for_Fine_grained_Motion_Generation_and_Editing|FineMotion]]"
---

# MoDebug f-Signal Parallel Implementation Plan

## 目标

本计划把 `||f(z, text) - f(z, null/random text)||` 从概念定义落到可执行 trace 框架。

核心约束：

1. `f` 是模型内部可 hook 的 readout，不是最终视频或人工分数。
2. 比较时固定同一个生成状态 `z`，只替换文本条件。
3. `null`、`random`、`counterfactual` 分别回答不同问题：条件强度、语义特异性、因果敏感性。
4. 所有记录都是 diagnostic 或 cross_check，不是 held-out final evaluator。

## f 的实现定义

统一接口：

```text
signal = f(model, z, condition, f_name)
delta_null = distance(signal_text, signal_null)
delta_random = distance(signal_text, signal_random)
delta_counterfactual = distance(signal_text, signal_counterfactual)
```

`z` 按模型族定义：

| 模型族 | z 定义 | 首选 f | 首选距离 |
| --- | --- | --- | --- |
| MotionGPT / MoLingo T5-family | AR prefix、decoder step、layer state | next motion-token logits、cross-attention context、condition injection vector | JS/KL、cosine、relative L2 |
| MoMask CLIP-family | mask state、mask iteration、base/residual token layer | masked token logits、confidence、expected code embedding | JS/KL、entropy change、relative L2 |
| MoGenTS CLIP-family | time-joint mask grid、mask iteration、joint token cell | time-joint token logits、expected joint-code embedding | JS/KL、body/time localized mass |
| Diffusion-family fallback | noisy latent step `z_t`、denoise step `t` | `epsilon` prediction、`x0` prediction、latent `z0` prediction | relative L2、body/time localized norm |

`f_name` 允许值：

```text
token_logits
token_prob
expected_code_embedding
condition_projection
attention_context
hidden_state
denoiser_prediction
confidence
```

## 证据边界

- MDM 和 MotionFix 的 CFG 公式直接使用 conditional 与 unconditional predictor 的差分，因此 diffusion-family 的 `f=epsilon/x0/score predictor` 有最强采样机制证据。
- MLD 支持把 `f` 放在 latent diffusion 的 denoised latent 或 predicted clean latent 上。
- MoMask 和 MoGenTS 是 token / mask / VQ-style generator，主 `f` 应放在 token logits、confidence、expected code embedding，而不是 diffusion score。
- MotionGPT 使用 T5-style motion language modeling，主 `f` 应放在 next motion-token logits、decoder hidden state、cross-attention context。
- FineMotion 支持 long fine-grained motion text 中 T5-family text encoder 相对 CLIP-family 更适合细粒度语义保持的假设，但当前计划只把它作为机制假设来源，不直接当结果证据。

## 本地与远端路径

计划与实现根目录：

```text
obsidian-vault/paperIDEAs/MoDebug/active/text_condition_propagation_guidance/_archive_20260527/
```

实验记录根目录：

```text
obsidian-vault/paperIDEAs/MoDebug/experiments/active/text_condition_propagation_trace_20260527/
```

4090 远端 staging 根目录，保持在 remote4090 MCP 默认 repo 内：

```text
/data/public/ripemangobox/Motion/EventT2M-codes/artifacts/modebug/text_condition_propagation_20260527/
```

本地拉回根目录：

```text
/data/Life Me/ResearchWY Vault/artifacts/remote/4090/modebug_text_condition_propagation_20260527/
```

每次运行必须使用日期命名子目录：

```text
YYYYMMDD_HHMMSS_{agent}_{model_or_scope}
```

示例：

```text
20260527_183000_agent_b_momask_trace_smoke
20260527_190500_agent_d_directory_sanity
```

## 并行 agent 写集

每个 agent 只能写自己的目录。需要修改共享 schema 时，先在自己的 `change_requests.md` 记录请求，由 coordinator 合并。

| Agent   | 责任                                                               | 本地可写目录                                           | 远端可写目录                                                                         |
| ------- | ---------------------------------------------------------------- | ------------------------------------------------ | ------------------------------------------------------------------------------ |
| A T5    | MotionGPT / MoLingo 的 hook map、T5-family trace adapter、smoke 验证  | `_archive_20260527/agent_a_t5/`            | `artifacts/modebug/text_condition_propagation_20260527/agent_a_t5/`            |
| B CLIP  | MoMask / MoGenTS 的 hook map、CLIP/discrete trace adapter、smoke 验证 | `_archive_20260527/agent_b_clip_discrete/` | `artifacts/modebug/text_condition_propagation_20260527/agent_b_clip_discrete/` |
| C Trace | 公共 NPZ/JSONL schema、delta 计算、dummy test、summary TSV              | `_archive_20260527/agent_c_trace_metrics/` | `artifacts/modebug/text_condition_propagation_20260527/agent_c_trace_metrics/` |
| D Sync  | 4090 拉回、目录 sanity、manifest 汇总、Gradio/inspection 索引准备             | `_archive_20260527/agent_d_sync_eval/`     | `artifacts/modebug/text_condition_propagation_20260527/agent_d_sync_eval/`     |

Coordinator 保留写权限：

```text
_archive_20260527/shared/
_archive_20260527/coordinator_status.md
```

## 共享文件格式

数组使用 `.npz`，元数据使用 `.jsonl`，阅读汇总使用 `.tsv` 或 `.md`。

Forward NPZ 必填 key：

```text
signal
valid_mask
meta_json
axis_names_json
```

`meta_json` 至少包含：

```json
{
  "run_id": "20260527_183000_agent_x_model_scope",
  "sample_id": "original100_000",
  "model": "momask_original",
  "model_family": "clip_discrete",
  "condition_id": "text",
  "condition_text": "...",
  "z_kind": "mask_iteration",
  "z_id": "iter_03",
  "f_name": "token_logits",
  "f_space": "vocab_logits",
  "role": "diagnostic",
  "limitations": "Internal trace only; not a final evaluator."
}
```

Forward manifest JSONL 每行字段：

```text
run_id
sample_id
model
model_family
condition_id
condition_text
paired_condition_id
z_kind
z_id
f_name
f_space
forward_npz_path
motion_artifact_path
role
used_for
limitations
```

Delta NPZ 必填 key：

```text
delta
metric_value
meta_json
```

Delta manifest JSONL 每行字段：

```text
run_id
sample_id
model
condition_pair
z_kind
z_id
f_name
metric_name
metric_value
delta_npz_path
role
used_for
limitations
```

## 距离与可视化口径

默认距离：

1. logits / prob：`JS divergence`、`KL`、entropy change、logit margin shift；
2. embedding / hidden / context：cosine distance、relative L2；
3. diffusion predictor：relative L2、body/time localized norm；
4. time-joint grid：按 left arm、right arm、left leg、right leg、root、torso 聚合 influence mass；
5. stage following：按 prompt semantic step 聚合 time-region influence curve。

输出图只服务 qualitative inspection 和 mechanism diagnosis，不写成最终评价器。

## DS Max 审查记录

每个 agent 必须在自己的目录保存：

```text
ds_max_rounds.md
review_log.md
verify_log.txt
change_requests.md
```

`ds_max_rounds.md` 必须包含：

1. 给 DS Max 的 prompt；
2. DS Max 指出的风险；
3. 接受或拒绝的修改；
4. 拒绝理由；
5. 本轮 verify 结果。

最小要求：每个 agent 至少完成两轮 DS Max 迭代，第二轮必须是对已实现文件的审查，而不是只审计划。

## 验证关口

P0 本地 dummy：

```text
Agent C 能用 synthetic forward NPZ 生成 delta NPZ 和 delta manifest。
```

P1 hook smoke：

```text
Agent A/B 各选择 1 个 sample、1 个 seed、1 个 condition_pair，导出 forward NPZ。
```

P2 远端/本地结构：

```text
Agent D 能把 4090 staging run 拉回 artifacts/remote/4090/modebug_text_condition_propagation_20260527/，并生成 file_tree.md 与 manifest_index.tsv。
```

P3 解释连接：

```text
至少一个 success sample 与一个 failure sample 具备 forward manifest、delta manifest、motion artifact path 和 description/human annotation link。
```

## 执行顺序

1. Coordinator 写入本计划并创建 `_archive_20260527/shared/`。
2. Agent C 先实现公共 NPZ/JSONL validator 与 dummy delta。
3. Agent A/B 并行实现各自 baseline hook map 与最小 forward adapter。
4. Agent D 并行实现目录 sanity 和拉回索引，不等待 A/B 真实 trace。
5. Coordinator 汇总四个 agent 输出，只合并 manifest/schema，不合并私有 helper。
6. 4090 执行前用 `r4090_git_archive` 记录远端 provenance；长任务必须用 tmux/log。
7. 拉回后统一检查本地目录树和 manifest 覆盖率。

## 禁止声明

1. 不把 trace delta 当 final evaluator。
2. 不把 attention heatmap 单独解释成因果证据。
3. 不在多个 agent 之间共享可写文件。
4. 不改写用户已有 manual annotation。
5. 不把 MoLingo custom direct runner 的旧 metadata 当新 trace 证据。
6. 不把 random text baseline 混同于 null baseline；random 只表示语义特异性对照。

## 当前任务完成定义

本轮完成不是要求跑完四个 baseline 的 full trace，而是完成：

1. 计划写入；
2. 四个 agent 并行启动；
3. 每个 agent 有 disjoint write-set；
4. 每个 agent 与 DS Max 迭代并留下审查记录；
5. 4090 与本地拉回目录结构被写入并由 Agent D 检查。
