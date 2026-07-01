---
title: "StoryMotion LLM 架构简报"
status: active
tags:
  - StoryMotion
  - Motion_Generation
  - architecture
  - experiment
  - status/active
aliases:
  - StoryMotion-LLM-Brief
hypothesis: |
  StoryMotion 的核心问题不是继续堆 Stage1 tokenizer 或照搬 CondMDI 随机 mask，而是要把 human-camera 的非对称条件关系、screen framing relation、observed branch source reliability 和 Stage1 official contract 分开处理。后续 LLM/agent 应基于证据定位病灶，再提出最小可验证修复。
source_papers:
  - "[[analysis/ICLR_2026/Pulp_Motion_Framing_aware_multimodal_camera_and_human_motion_generation]]"
  - "[[analysis/CVPR_2026/Towards_Storytelling_Animations_Joint_Synthesis_of_Human_and_Camera_Motions]]"
  - "[[analysis/SIGGRAPH_2024/Flexible_Motion_In_betweening_with_Diffusion_Models_CondMDI]]"
  - "[[analysis/ICCV_2025/MotionLab_Unified_Human_Motion_Generation_and_Editing_via_the_Motion_Condition_Motion_Paradigm]]"
  - "[[analysis/ICLR_2024/HUMAN_MOTION_DIFFUSION_AS_A_GENERATIVE_PRIOR]]"
  - "[[analysis/arxiv_2026/AnyMo_Scaling_Any-Modality_Conditional_Motion_Generation_with_Masked_Modeling]]"
created: 2026-07-01T22:10:00+0800
updated: 2026-07-01T22:10:00+0800
---
# StoryMotion LLM 架构简报

## 0. 给后续 LLM 的任务定义

你要解决的不是“让一个扩散模型同时输出 human 和 camera”这么宽泛的问题。StoryMotion 的目标是：

```text
给定 story/text，
生成或补全一段时间对齐的 human motion 与 camera motion，
使 human 动作语义成立，同时 camera 在屏幕空间中保持合理 framing，
并且当 human 条件来自 GT、noisy GT 或 generated human 时，camera 仍可靠。
```

这里的核心难点是 **human-camera 是耦合但不对称的**：

- human branch 承载动作、root、timing，是 camera 的结构条件。
- camera branch 承载 framing、视角、相机残差，应该读取 human，但不能盲信任何 human source。
- joint generation 的实际推理应是 `human prior -> camera conditioned on generated human`，而不是把 GT human completion 的 clean 指标当作真实 joint 能力。

因此，后续建议必须回答三个问题：

1. **Stage1 contract 是否可靠？** 如果 autoencoder decode 后进 official TMR/CLaTr/projection 已经弱，Stage2 再好也没用。
2. **Stage2 是否在 oracle observed branch 下过拟合？** clean GT human 条件强，不代表 generated/noisy human 条件强。
3. **architecture 是否把不该共享的信息共享了？** raw concat + shared TemporalObsUNet 会让 human/camera latent 互相串扰；camera text 也可能被 observed human shortcut 掩盖。

## 1. 当前系统架构

### 1.1 Stage1：Pulp-style human-camera latent contract

当前 StoryMotion 依赖 PulpMotion 风格的 Stage1 autoencoder / tokenizer，把原始 motion feature 压到 latent：

- human feature：Pulp SMPL/RIFKE 风格，约 `199D`。
- camera feature：camera trajectory / relative framing 相关特征。
- latent order：StoryMotion Stage2 cache 使用 `concat([z_hum,z_cam])`，常见维度为 human `128` + camera `64`。
- Pulp official ckpt 是当前 upper bound；self-trained tokenizer 必须通过 decoded official recon metric，不能只看 training loss。

Pulp Motion 的核心证据见 [[analysis/ICLR_2026/Pulp_Motion_Framing_aware_multimodal_camera_and_human_motion_generation]]。它不是简单 raw concat，而是学习 human-camera latent 到 screen framing latent 的线性桥 `W`，并在采样时用 `W` row-space 做 auxiliary guidance。官方开源入口：[Pulp Motion GitHub](https://github.com/robincourant/pulp-motion)，项目页和数据也公开。

### 1.2 Stage2：CondMDI-style branch-mask diffusion

当前 Stage2 主干是 `TemporalObsUNet`，不是 Transformer attention。关键训练/推理 contract：

```python
x = torch.where(obs_mask.bool(), obs_x0, x_t)
input = concat(x, obs_mask, text, t)
target_loss = MSE(pred_x0, target_x0) only on target branch
```

三种任务：

- `TASK_CAMERA`：观察 human latent，预测 camera latent。
- `TASK_HUMAN`：观察 camera latent，预测 human latent。
- `TASK_JOINT`：不观察 latent，同时预测 human + camera。

文本约定：

- 1024 维 text embedding。
- 前 `512` 维是 camera text。
- 后 `512` 维是 human text。

这个设计借鉴了 CondMDI 的 mask-conditioned diffusion，但 CondMDI 的前提是**同一种人体 motion 中任意 keyframe / joint 观测都可随机缺失**。CondMDI 的官方代码与项目证明了随机 mask 对单人体补间有效：[CondMDI GitHub](https://github.com/setarehc/diffusion-motion-inbetweening)，本地分析见 [[analysis/SIGGRAPH_2024/Flexible_Motion_In_betweening_with_Diffusion_Models_CondMDI]]。

StoryMotion 不满足 CondMDI 的对称前提。human 与 camera 是语义分支，不是同一模态里的任意维度；camera 读 human 是合理的，但 human/camera 双向 share-all 与 hard observed replacement 会导致错误耦合。

## 2. 已知实验事实

### 2.1 Pulp official Stage1 是 upper bound

| checkpoint | split | samples | FDTMR↓ | TMR↑ | HCov↑ | FDCLaTr↓ | CLaTr↑ | CCov↑ | F1↑ | Out↓ |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Pulp official Stage1 recon | mixed | 10549 | 124.46 | 18.17 | 85.4% | 15.51 | 58.10 | 87.2% | 0.670 | 4.6% |
| Pulp official Stage1 recon | pure | 4053 | 109.34 | 15.94 | 92.4% | 17.66 | 60.53 | 84.5% | 0.776 | 3.5% |

这说明 official AE decoded reconstruction 进入 TMR/CLaTr/projection metric 后仍强，可以作为 Stage1 contract 目标。

### 2.2 本地 Pulp Stage1 复现失败

4090 GPU0 完成 mixed official recon；5090 GPU0 完成 pure official recon。结果：

| checkpoint | split | samples | FDTMR↓ | TMR↑ | HCov↑ | FDCLaTr↓ | CLaTr↑ | CCov↑ | F1↑ | Out↓ |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| reproduced Stage1 latest | mixed | 10549 | 423.10 | 8.74 | 34.1% | 76.97 | 35.86 | 68.2% | 0.373 | 28.6% |
| reproduced Stage1 latest | pure | 4053 | 438.99 | 7.88 | 41.4% | 99.98 | 38.27 | 67.1% | 0.453 | 23.3% |

结论：本地训练的 `stage1_official_repro_20260701` 没有复现 Pulp official ckpt。任何基于这个 reproduced Stage1 的 Stage2 正结论都应暂停。

Evidence:

- mixed eval: `/data/public/ripemangobox/Motion/StoryMotion/stage2/metrics/v6_3_stage1_repro_official_eval_20260701/stage1_repro_latest_mixed_official_recon.json`
- pure eval: `/data/public/ripemangobox/Motion/StoryMotion/stage2/metrics/v6_3_stage1_repro_official_eval_5090_pure_20260701/stage1_repro_latest_pure_official_recon.json`

### 2.3 v6.3 三模式拆分不能绕过 self-trained latent failure

v6.3 把三模式拆开训练：camera-only、completion-only、joint-only。所有 runs 都到 `50000` step，但 first-wave clean official eval 已经失败：

| run | task | samples | FDTMR↓ | FDCLaTr↓ | CLaTr↑ | F1↑ | Out↓ | readout |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| `cam_text_only_jointvae_full_b512` | camera | 10549 | - | 957.83 | 3.13 | 0.060 | - | clean camera collapses |
| `cam_full_text_jointvae_full_b512` | camera | 10549 | - | 957.45 | 3.10 | 0.060 | - | human text does not rescue |
| `completion_only_jointvae_full_b512` | camera | 10549 | - | 955.99 | 3.18 | 0.060 | - | completion-only also collapses |
| `joint_only_jointvae_full_b512` | joint | 10549 | 2228.68 | 967.49 | 3.31 | 0.063 | 100.0% | joint collapses |

结论：在 self-trained joint VAE source tokenizer 上，拆任务不能解决 Stage2 transfer。这个负例不能证明非对称框架无效，只能证明当前 Stage1 latent contract 不可用。

Evidence:

- `/data/public/ripemangobox/Motion/StoryMotion/stage2/metrics/v6_3_mode_conflict_eval_20260701`
- `/data/public/ripemangobox/Motion/StoryMotion/runs/train/stage2/v6_3_mode_conflict_20260701`

### 2.4 v6.4 GPU1：clean 通过，但 noise 与 text-dependence 失败

v6.4 GPU1 是一个 camera-only specialist：

```text
task_probs = [1, 0, 0]
observed branch = human latent
target branch = camera latent
Stage1 cache = Pulp official full mixed cache
P2b reliability augmentation = enabled
```

Official eval:

| eval | observed human condition | camera text intervention | FDCLaTr↓ | CLaTr↑ | CCov↑ | F1↑ | readout |
| --- | --- | --- | ---: | ---: | ---: | ---: | --- |
| clean camera | GT | none | 15.00 | 54.87 | 84.9% | 0.629 | clean oracle completion strong |
| noise `0.15` | matched latent noise | none | 530.27 | 9.46 | 4.0% | 0.103 | noisy observed branch collapses |
| noise `0.30` | matched latent noise | none | 493.82 | 10.24 | 6.0% | 0.110 | noisy observed branch collapses |
| text shuffle | GT | shuffle camera half | 15.63 | 53.89 | 84.5% | 0.618 | camera text weak |
| text zero | GT | zero camera half | 14.16 | 53.29 | 84.0% | 0.609 | camera text not decisive |

Evidence:

- train run: `/data/public/ripemangobox/Motion/StoryMotion/runs/train/stage2/v6_4_asym_human_to_camera_p2b_20260701/camera_p2b_b512_gpu1`
- eval output: `/data/public/ripemangobox/Motion/StoryMotion/stage2/metrics/v6_4_asym_camera_p2b_eval_5090_20260701`

## 3. v6.4 clean / noise 到底代表什么

### 3.1 Clean

`clean camera` 的意思是：camera branch 观察到的 human latent 是 **GT human latent**，没有扰动、没有生成误差。

```text
input condition: H_gt
target: C_gt
model predicts: C_hat = camera_specialist(camera_text, H_gt)
```

它回答的是：

- 模型在 oracle human 条件下有没有 camera completion 能力？
- Stage2 sampler、official metric bridge、Pulp official Stage1 cache 是否正常？
- v6.4 camera-only specialist 是否至少没有破坏 clean quality？

clean 通过说明：capacity 和 basic camera completion 没问题。v6.4 clean `FDCLaTr 15.00 / F1 0.629` 接近旧 v6 clean `14.50 / 0.638`。

### 3.2 Noise

`noise015_camera` / `noise030_camera` 的意思是：仍然做 camera completion，但把 observed human latent 加入 matched latent noise。

```text
input condition: H_noisy = H_gt + sigma * matched_latent_noise
target: C_gt
model predicts: C_hat = camera_specialist(camera_text, H_noisy)
```

它不是在测试 camera 采样噪声，而是在测试 **camera 对 human condition 质量的鲁棒性**。

为什么必要：真实 joint inference 不会给 camera `H_gt`，而是给一个 human prior 生成的 `H_hat`。`H_hat` 一定带有分布偏差、root 误差和 latent noise。若模型只在 `H_gt` 下强，而在 `H_noisy` 下崩，则它只是 oracle completion，不是 robust StoryMotion。

### 3.3 它如何帮助定位 coupling 问题

clean/noise 形成一个因果隔离：

```text
clean pass + noise fail
=> 模型不是没有 camera 生成能力
=> failure 不是 official metric bridge 或 Stage1 official cache 本身
=> failure 集中在 observed human branch 的可靠性假设
```

v6.4 GPU1 正是这个形态：

- clean pass：`FDCLaTr 15.00 / F1 0.629`
- noise fail：`0.15` 噪声下 `FDCLaTr 530.27 / F1 0.103`
- text weak：camera text shuffle / zero 几乎不破坏 clean output

这说明当前 camera specialist 大概率仍在用 hard observed human/root shortcut，而不是稳定融合 camera text 与 relation/framing control。对架构的直接启发是：

- 不能继续只加随机 mask。
- 不能把 `H` 当作永远可信的 clean observed branch。
- 必须把 `H` 的 source / trust / noise sigma 显式进入模型或 sampler。
- camera branch 应分成 text-driven global camera prior 与 human-conditioned residual/framing branch。

## 4. 外部工作证据链：哪些能借，哪些不能硬套

### 4.1 Pulp Motion：需要显式 relation/framing control 面

Pulp Motion 证明 human-camera joint generation 的关键不是 raw latent share-all，而是 screen-space framing 关系。它通过 `W` 把 human/camera latent 映射到 framing latent，并用 auxiliary sampling 改善构图。混合子集上，Pulp 分析 note 记录 DiT + Aux 将 `FD_framing` 从 `4.90` 降至 `3.37`，Out-rate 从 `25.98%` 降至 `16.76%`。

对 StoryMotion 的启发：

- 加 `relation token` 或 Pulp `W` row-space guidance。
- camera 不应只回归 raw trajectory；应显式约束 screen framing。
- root-relative camera error 需要被拆出来，不应通过 raw concat 传播。

### 4.2 Towards Storytelling Animations：实体交互不是 raw concat

[[analysis/CVPR_2026/Towards_Storytelling_Animations_Joint_Synthesis_of_Human_and_Camera_Motions]] 把 character 与 camera 作为独立实体，并显式建模 character-camera pairwise interaction。其消融显示交互模块对角色和相机质量及协调性关键。

对 StoryMotion 的启发：

- human / camera 应保留 branch-specific path。
- relation interaction 应是模块化的，而不是让共享 UNet 通道自由串扰。
- 如果要 joint model，也应是 entity/relation routing，不是单纯 `[z_hum,z_cam]` concat。

### 4.3 CondMDI：随机 mask 有效，但前提不同

CondMDI 在单人体 motion in-betweening 中通过随机 keyframe / joint mask 获得灵活补全能力。它适合“同一 motion 表示内的任意部分观测”。

对 StoryMotion 的边界：

- 可以借鉴 `mask + observed x0` 输入形式。
- 不能直接把 human/camera 分支当作对称随机 mask，因为 camera 与 human 语义、误差传播和可靠性不同。
- StoryMotion 的 bug 不是 mask 数量不够，而是 source reliability 与 branch routing 不对。

### 4.4 MotionLab / AnyMo：统一模型需要 task instruction、curriculum、modality-specific capacity

MotionLab 使用 Motion-Condition-Motion、task instruction modulation 与 curriculum learning；消融显示去掉 curriculum 会让文本生成 FID 从 `0.167` 恶化到 `1.956`。AnyMo 使用大规模多模态数据、R-FSQ、并行掩码建模和分阶段课程训练支持任意模态组合。

对 StoryMotion 的启发：

- 统一任务不是把所有模式同权混在一起。
- 要有明确 task/source instruction，例如 `gt_human`、`noisy_human`、`generated_human`、`missing_human`。
- 训练顺序应 human prior -> camera specialist -> relation refinement，而不是一开始三模式随机混训。

MotionLab 官方实现：[GitHub](https://github.com/Diouo/MotionLab)。AnyMo 论文与数据说明见 [arXiv](https://arxiv.org/abs/2605.29488) 与本地 [[analysis/arxiv_2026/AnyMo_Scaling_Any-Modality_Conditional_Motion_Generation_with_Masked_Modeling]]。

### 4.5 PriorMDM / MDM：优先复用强 prior 与轻量协调

PriorMDM 的核心是把 MDM 作为冻结或轻微微调的 motion prior，再用 handshake、communication block 或 model blending 做组合泛化。官方代码见 [PriorMDM GitHub](https://github.com/priorMDM/priorMDM)，MDM 官方代码见 [MDM GitHub](https://github.com/GuyTevet/motion-diffusion-model)。

对 StoryMotion 的启发：

- 不要每次从零重训整个 human-camera generator。
- 可以先固定强 human prior，再训练 camera specialist。
- 需要轻量 communication / relation block，而不是 share-all backbone。

## 5. 对阵下药：后续 LLM 应该怎么提方案

### 5.1 先过 Stage1 gate

必须修清楚：

- official training config 是否完全一致。
- normalizer / feature scaling 是否一致。
- checkpoint 是否应该用 EMA / best epoch / averaged ckpt，而不是 latest。
- official model dir symlink 是否完全匹配。
- pure/mixed split 与 data loader 是否和 Pulp official eval 一致。

成功判据：

```text
mixed close to official: FDTMR 124.46, FDCLaTr 15.51, Out 4.6%
pure close to official: FDTMR 109.34, FDCLaTr 17.66, Out 3.5%
```

### 5.2 Stage2 不要再盲目三模式对称训练

推荐最小架构：

```text
human prior:
  text_human -> H_hat

camera specialist:
  camera_text + H_condition + source_tag + trust_scalar + relation_token -> C_hat

joint inference:
  H_hat = human_prior(text_human)
  C_hat = camera_specialist(camera_text, H_hat, source=generated, trust=q)
```

必要改动：

1. `trust-gated observed human`：不要用 hard `torch.where(obs_mask, obs_x0, x_t)` 盲写 noisy/generated human；让模型知道 source 和 sigma。
2. `camera root residual split`：拆成 text-only global camera prior 与 human-conditioned residual/framing branch。
3. `relation token / W row-space`：加入 screen framing relation 控制面。
4. `branch-specific heads/adapters`：保留共享低层时序能力，但 human/camera 输出头和条件路由分离。
5. `external human replay eval`：camera specialist 的 generated-human replay 必须接外部 human prior，不能用 camera-only checkpoint 自己先生成 human。

### 5.3 每个候选必须过的 eval

任何新方案都必须同时报告：

| gate | why |
| --- | --- |
| Stage1 official recon | 防止 tokenizer/reconstruction 假阳性 |
| clean camera completion | 保证基础 camera capacity 不掉 |
| P2a noise `0.15/0.30` | 测 noisy/generative human condition robustness |
| generated-human replay | 测真实 joint inference condition shift |
| camera text shuffle / zero | 测 camera text 是否真的控制 output |
| relation/framing metrics | 测 screen-space coherence，而不是只看 latent MSE |

### 5.4 禁止误判

- 不要把 clean GT-human camera completion 写成 robust joint generation。
- 不要把 training loss / feature MSE 写成 Stage1 成功。
- 不要继续把 CondMDI 的对称随机 mask 原样套到 human-camera 三模式。
- 不要在 self-trained Stage1 gate 失败时比较 Stage2 架构正负。
- 不要把 `generated-human replay` 用 camera-only checkpoint 自己生成 human；这不是有效 replay。

## 6. 当前最短行动清单

1. 修 Stage1 reproduction：先复现 official AE，不进入 Stage2 主表。
2. 在 Pulp official Stage1 cache 上做 `trust-gated observed human` ablation。
3. 给 v6.4 camera specialist 接一个合法 human prior，跑 generated-human replay。
4. 加 `camera root residual split` 与 `relation token` 的最小代码版本。
5. 每个版本只看 official clean/noise/replay/text gates，不再用 teacher loss 做结论。
