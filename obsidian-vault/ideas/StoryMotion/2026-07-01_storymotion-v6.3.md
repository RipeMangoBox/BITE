---
title: "StoryMotion v6.3 聚焦问题与实验计划"
status: active
tags:
  - StoryMotion
  - Motion_Generation
  - experiment
  - plan
  - status/active
aliases:
  - StoryMotion-v6.3
hypothesis: |
  v6.3 不应继续横向堆 tokenizer，而应隔离两个问题：Pulp official Stage1 质量是否能被本地训练复现；在强 Stage1 条件下，StoryMotion Stage2 是否仍存在 generated/noisy observed branch coupling 和 sampler/reliability mismatch。
source_notes:
  - "[[2026-07-01_storymotion-v6.2-metric-data]]"
  - "[[2026-06-30_storymotion-experiment-metric-comparison]]"
  - "[[2026-06-29_storymotion-v6.2]]"
  - "[[2026-06-10_pulp-stage1-continuous-stage2-generator-formal]]"
created: 2026-07-01T14:08:43+0800
updated: 2026-07-01T17:48:00+0800
---
# Paper Design

# Abstract

Story-driven motion generation requires coordinating two coupled but asymmetric signals: the character motion that carries the action, and the camera motion that frames it. Existing pipelines often synthesize human and camera motion separately, or evaluate camera control with oracle human/root trajectories, which hides failures that emerge when both streams must be generated jointly. 
We 
+ introduce **StoryMotion**, a unified framework for joint human-camera motion generation and completion. StoryMotion is built on a simple principle: human and camera motion should share narrative structure while preserving modality-specific dynamics. 
	+ A shared latent generator captures cross-modal coordination in timing, viewpoint, distance, and framing, while source- and quality-aware conditioning distinguishes ground-truth, partially observed, and generated inputs. 
+ We further identify a key failure mode in coupled cinematic representations: camera completion can become overly dependent on the quality of the human branch, especially when camera latents encode root-relative quantities. 
	+ To address this, StoryMotion incorporates generated-human-aware training and camera-latent decoupling, improving robustness beyond clean-condition evaluation. 
Our results suggest that unified human-camera generation should be evaluated not only by motion realism, but also by whether camera and character remain coherent under incomplete, noisy, or generated observations.

**ICLR-facing contribution boundary**：可以写成 task / protocol / diagnosis / repair direction；不能写成已经解决 robust human-camera generation，也不能把 tokenizer 收敛写成 Stage2 质量提升。

## ICLR 标准审计

当前判断：**如果 StoryMotion 只停留在“统一 human-camera 框架 + joint 指标优势”，ICLR 风险偏高；如果 v6.3 能把 decoupled representation / Stage1 contract / generated-or-noisy reliability 三件事中的至少两件做实，它可以支撑 ICLR。** 真实工业级能力不是 ICLR 的硬性门槛，但“前人无法达到的能力或清晰机制洞察”是硬门槛。

更具体地说，StoryMotion 的 ICLR 论文不必证明自己是可直接落地的创作系统，但必须回答一个学习问题：

```text
When human motion and camera motion are generated or completed jointly,
what should be shared, what must be decoupled,
and how should reliability change when observed branches are generated/noisy rather than oracle?
```

这比“我们统一了任务”更像 ICLR 问题，因为它把贡献落在 representation、conditioning contract、robustness protocol 和 failure diagnosis 上。

### 当前 abstract 的过度前瞻风险

当前 abstract 中有三处必须谨慎：

1. **“shared latent generator captures cross-modal coordination”**：只有在 joint mode 或 completion mode 的指标、latent diagnostic 和 ablation 同时支持时才能这么写。否则应降级为 “is designed to capture” 或 “we study whether”。
2. **“source- and quality-aware conditioning distinguishes ground-truth, partially observed, and generated inputs”**：如果 P2b / generated-human-aware training 尚未显著改善 P2a noise slope 或 E.T. replay，就不能写成已解决，只能写成诊断协议和候选修复。
3. **“camera-latent decoupling improves robustness”**：这是 v6.3 最关键但尚未完成的实证点。没有新的数据表示或 decoupling ablation 前，这句话应保持为 hypothesis，而不是 result claim。

### 哪些是 ICLR 必须项

| 项目                       | ICLR 角色    | 当前状态  | 判据                                                                                                                 |
| ------------------------ | ---------- | ----- | ------------------------------------------------------------------------------------------------------------------ |
| 问题定义                     | 必须         | 基本成立  | human-camera joint generation/completion 不能只像 application；要形式化 oracle observed branch 与 generated/noisy branch 的差异 |
| 可靠性协议                    | 必须         | 已有雏形  | clean、P2a noise `0.15/0.30`、generated-human replay 必须成为主表或核心诊断                                                     |
| Stage1 contract 解释       | 必须         | 证据不闭环 | 需要 Pulp official Stage1 reproduction 或 controlled comparison，否则 tokenizer 相关结论不稳                                   |
| human-camera 适度 decouple | 基本必须       | 未完成   | 至少要证明某种 camera latent / representation / conditioning 改动能降低 branch coupling，而不是只保持 clean 指标                        |
| Stage1 新设计               | 视 claim 而定 | 未完成   | 如果论文声称方法创新在 tokenizer/representation，则必须有；如果论文主打 protocol+diagnosis+Stage2 reliability，可降为辅助                       |
| 可视化质量                    | 必须达标但非唯一贡献 | 目前不突出 | 至少要避免明显出画、跳变、构图失败；不必达到 SIGGRAPH demo 级，但不能和指标叙事冲突                                                                  |

因此，v6.3 的最低 ICLR 形态不是“工业级 StoryMotion”，而是：

- 一个清楚的 task/protocol：joint human-camera generation/completion under non-oracle observed branches。
- 一个清楚的 failure finding：clean oracle camera completion 会隐藏 generated/noisy human-root condition 下的 camera collapse。
- 一个清楚的 mechanism：relative/root-dependent camera latent 或 observed branch source mismatch 是关键原因之一。
- 一个清楚的 fix 或 partial fix：camera-latent decoupling、quality-aware conditioning、generated-human-aware training、sampler correction 中至少一个显著改善 reliability，而不是只改善 clean。

### 哪些是锦上添花

以下能力会显著增强说服力，但不是 ICLR 中稿的硬性条件：

- Blender / Unreal / asset export。
- artist/user study。
- 长视频多镜头 authoring demo。
- reference-camera interface。
- ego / exo / cinematic camera 统一。
- 接入视频生成模型得到更好视觉成片。

这些更像 CVPR/SIGGRAPH 或下一篇 human-camera-video 工作的价值。如果把它们硬塞进当前 StoryMotion，反而可能稀释 v6.3 的核心问题。

### 当前最危险的写法

- “StoryMotion solves robust human-camera generation”：不安全。目前最多是发现并尝试修复 reliability mismatch。
- “joint framework itself is the contribution”：不够。已有 [Towards Storytelling Animations(CVPR_2026)](../../analysis/CVPR_2026/Towards_Storytelling_Animations_Joint_Synthesis_of_Human_and_Camera_Motions.md) 和 [Pulp Motion(ICLR_2026)](../../analysis/ICLR_2026/Pulp_Motion_Framing_aware_multimodal_camera_and_human_motion_generation.md) 会让“统一生成”不再新。
- “better joint metric proves method works”：不够。必须解释 camera completion 相比 E.T. 没有显著优势、human completion 仍待 MoLingo 完成、generated/noisy condition 退化这些负面事实。
- “new tokenizer solves Stage2”：除非通过 official reconstruction metric 和 Stage2 transfer gate，否则不能这么写。

### 更稳的 ICLR 论文定位

更稳的定位是：

```text
StoryMotion is a diagnostic and modeling framework for robust human-camera motion generation:
it exposes the gap between oracle-conditioned completion and generated/noisy-conditioned use,
then studies which representation and conditioning contracts reduce this gap.
```

如果 v6.3 后续实验达成预期，abstract 应从“前瞻式系统宣言”改成“问题-诊断-机制-修复”：

1. 现有 human-camera 方法依赖 oracle human/root condition，低估真实 joint generation 难度。
2. StoryMotion 建立统一任务和 reliability protocol，显示 clean completion 与 generated/noisy condition 存在明显差距。
3. 诊断发现 root-relative camera latent 与 observed branch source mismatch 会放大 camera failure。
4. 通过 decoupled camera representation / quality-aware conditioning / generated-human-aware training，降低 noise slope 和 replay collapse，同时保持 clean quality。

在这个定位下，“更真实的工业能力”是强加分项，但不是当前 ICLR 的必要前提；**必要前提是把上述机制链证明完整**。




---

## 0. 当前裁决

v6.2 数据不能支持“问题只在 Stage1”或“问题只在 Stage2”任一单因果结论。更稳妥的读法是两个 bottleneck 同时存在：

1. **Stage1 contract bottleneck 成立**：Pulp official Stage1 reconstruction 在 pure/mixed 三模式都强；多组自训练 separate / joint / VAE / GRFSQ tokenizer 即使 loss 或 feature MSE 收敛，也没有稳定传递到 Stage2 official metrics。
2. **Stage2 branch coupling bottleneck 成立**：使用 Pulp official Stage1 的 StoryMotion v6 clean completion 可以很强，但 camera completion 在 noisy/generated human/root condition 下明显退化；latent diagnostics 也显示 completion 使用 visible branch，不是 text-only shortcut。
3. **尚未证明的点**：本地是否能完整复现 Pulp official Stage1 ckpt 效果还没有闭环。用户提出的怀疑是合理的，应作为 v6.3 第一优先级，而不是继续从当前失败 tokenizer 上推断架构结论。

## 1. Stage1 指标为什么与 loss 脱钩

### 1.1 Pulp official Stage1 是当前 upper bound

| tokenizer | split | task | samples | FDTMR↓ | TMR↑ | HCov↑ | FDCLaTr↓ | CLaTr↑ | CCov↑ | F1↑ | Out↓ | readout |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| Pulp official Stage1 recon | mixed | human | 10549 | 124.46 | 18.17 | 85.4% | - | - | - | - | - | human upper bound strong |
| Pulp official Stage1 recon | mixed | camera | 10549 | - | - | - | 15.51 | 58.10 | 87.2% | 0.670 | - | camera upper bound strong |
| Pulp official Stage1 recon | mixed | joint | 10549 | 124.46 | 18.17 | 85.4% | 15.51 | 58.10 | 87.2% | 0.670 | 4.6% | official AE remains strong in three modes |
| Pulp official Stage1 recon | pure | joint | 4053 | 109.34 | 15.94 | 92.4% | 17.66 | 60.53 | 84.5% | 0.776 | 3.5% | pure upper bound strong |

这组数据说明：Pulp official Stage1 ckpt 的 decoded reconstruction 进入 TMR/CLaTr/projection metric 后仍强。v6.3 必须先验证“我自己训练是否能复现这个 Stage1 upper bound”，否则无法把后续失败归因到 joint/separate、VAE/GRFSQ 或 Stage2。

### 1.2 自训练 tokenizer 的关键负例

| tokenizer | split | Stage1 readout | Stage2 readout | implication |
| --- | --- | --- | --- | --- |
| separate AE no-z | mixed-subset / mixed full | feature MSE `0.002174`; official recon camera FDCLaTr `2.71`, CLaTr `66.26`, F1 `0.878` | full mixed joint FDTMR `2157.12`, FDCLaTr `662.84`, Out `95.5%` | deterministic separate AE 的 reconstruction upper bound 强，但 Stage2 transfer 失败 |
| separate VAE with-z | mixed-subset / mixed full | official recon joint FDTMR `1364.23`, FDCLaTr `4.75`, F1 `0.842` | full mixed joint FDTMR `1863.90`, FDCLaTr `885.36`, Out `99.0%` | native z 和 VAE 不足以保证 Stage2 |
| corrected joint VAE with-z | mixed full | feature total `0.003617`, human MSE `0.001752`, camera MSE `0.005145` | full mixed joint FDTMR `2250.73`, FDCLaTr `989.53`, Out `100.0%` | joint + VAE 的 feature recon 可用，但 Stage2 仍坍塌 |
| corrected joint GRFSQ with-z | mixed full | camera MSE `0.292299`, joint MSE `0.148231` | full mixed joint FDTMR `1648.84`, FDCLaTr `663.60`, Out `99.6%` | mixed camera branch recon 本身弱，Stage2 也弱 |
| corrected joint VAE with-z | pure | feature total `0.001932`, camera MSE `0.000338` | pure Stage2 未完成同口径闭环 | pure Stage1 clean，不可直接外推 mixed |
| corrected joint GRFSQ with-z | pure | feature total `0.003852`, camera MSE `0.002418` | pure Stage2 未完成同口径闭环 | pure Stage1 clean，不可直接外推 mixed |

点对点拆分：

- **joint vs separate**：当前数据不能简单支持“joint 必然好”或“separate 必然差”。Pulp official joint AE 强；但 corrected joint VAE / GRFSQ Stage2 仍失败。separate AE no-z Stage1 official upper bound 很强，但 Stage2 transfer 更差。真正差异更可能是 Stage1 latent contract 是否与 Stage2 generator 的训练/采样分布兼容。
- **AE vs VAE/GRFSQ**：VAE 的 KL 和 sampling-friendly latent 没有自动改善 Stage2。GRFSQ pure Stage1 可用，但 mixed camera MSE 明显偏高；quantization 在 mixed camera branch 上目前是弱点。deterministic AE no-z 去掉 KL 后仍失败，说明问题不只在 KL。
- **loss vs metric**：feature loss/MSE 是 normalized representation space 的误差；official metric 是 decoded human/camera 后的 TMR/CLaTr/projection/caption score。separate AE no-z 同时有低 MSE 和强 official reconstruction upper bound，但 Stage2 full mixed collapse，因此 loss 收敛最多说明 Stage1 可重建，不说明 Stage2 可生成。
- **训练策略**：旧 mixed-subset 不是 eval 少跑，而是训练 cache 本身只有 `29779/3279`；full manifest 已补到 `94050/10549` 后，MoLingo、separate AE、separate VAE、joint VAE、joint GRFSQ 仍为负面。

## 2. Stage2 分支耦合证据

### 2.1 Clean condition 强，不代表 generated/noisy condition 强

| model | condition | samples | FDCLaTr↓ | CLaTr↑ | CCov↑ | F1↑ | RootFrame↑ | MPJPE↓ | readout |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| StoryMotion v6 unified camera | clean GT human/root | 10549 | 14.50 | 54.85 | 87.1% | 0.638 | - | 0.085 | clean completion strong |
| E.T./DIRECTOR root-only | clean GT/root | 10549 | 14.51 | 54.84 | 87.0% | 0.638 | 81.5% | 0.085 | external camera baseline strong under clean condition |
| E.T./DIRECTOR replay | generated-human condition | 10549 | 92.24 | 33.31 | 62.8% | 0.375 | 27.3% | 0.194 | generated-human condition collapses |
| StoryMotion v6 unified joint | no observed branch | 10549 | 85.70 | 33.52 | 62.8% | 0.374 | - | 0.194 | joint weaker than clean camera |

这说明 Stage2 的 camera branch 至少在 observed branch source 改变时存在可靠性问题。即使 Pulp official Stage1 upper bound 强，StoryMotion Stage2 仍没有证明能在 generated/noisy human/root condition 下保持 clean completion 质量。

### 2.2 P2a 噪声斜率是最直接的 branch coupling 数据

| observed human/root noise std | camera FDCLaTr↓ | camera CLaTr↑ | camera CCov↑ | camera F1↑ |
| ----------------------------: | --------------: | ------------: | -----------: | ---------: |
|                          0.00 |           14.50 |         54.85 |        87.1% |      0.638 |
|                          0.05 |           22.02 |         53.15 |        85.6% |      0.625 |
|                          0.10 |           51.89 |         48.66 |        80.2% |      0.573 |
|                          0.15 |           96.87 |         43.54 |        70.1% |      0.503 |
|                          0.30 |          216.79 |         32.96 |        46.7% |      0.360 |
|                          0.50 |          303.00 |         25.68 |        31.0% |      0.278 |

`0.15` noise 已经把 camera FDCLaTr 从 `14.50` 拉到 `96.87`。这不是 Stage1 reconstruction loss 能解释的现象，而是 Stage2 conditioning/reliability 与 camera relative-distance contract 的组合风险。

### 2.3 Latent diagnostics 支持“模型确实使用 visible branch”

| diagnostic                | key numbers                                                                    | what it proves                                     | what it does not prove            |
| ------------------------- | ------------------------------------------------------------------------------ | -------------------------------------------------- | --------------------------------- |
| visible shuffle           | camera delta `+1.1016`; human delta `+1.3672`                                  | completion 不是只靠 text shortcut                      | 不等于 official generated quality    |
| Mode B camera latent gate | base `0.003662`; zero `0.216638`; shuffle `0.314891`; matched-noise `0.774336` | human completion 依赖 camera latent                  | 还未分解 distance / camera-motion 子切片 |
| joint sampler re-eval     | teacher `0.016472`; 1-step `0.292046`; 20-step `0.617884`; 50-step `0.740053`  | one-step x0 objective 与 recursive sampler mismatch | 不是 official metric                |

## 3. 用户疑问的当前回答

### 3.1 会不会只是 PulpMotion official Stage1 ckpt 好，我自己训练无法复现？

这是目前最应该优先验证的假设。已有数据只能说明 official ckpt 是强 upper bound；不能证明本地训练 pipeline 已能复现它。v6.3 第一优先级应是用 4090 上的 Pulp 官方仓库、官方训练设置复现 Pulp official Stage1，而不是继续比较当前失败 tokenizer。该复现任务由另一个 agent 负责；本轮不触碰其 tmux、repo 或 checkpoint。

复现实验的判据应使用 official reconstruction metric，而不是训练 loss：

| target       | mixed success band                                  | pure success band                                   | fail interpretation                                   |
| ------------ | --------------------------------------------------- | --------------------------------------------------- | ----------------------------------------------------- |
| human recon  | close to FDTMR `124.46`, TMR `18.17`, HCov `85.4%`  | close to FDTMR `109.34`, TMR `15.94`, HCov `92.4%`  | 本地 Stage1 训练或数据/normalization/ckpt selection 不复现 Pulp |
| camera recon | close to FDCLaTr `15.51`, CLaTr `58.10`, F1 `0.670` | close to FDCLaTr `17.66`, CLaTr `60.53`, F1 `0.776` | camera AE contract 未复现                                |
| joint recon  | Out close to `4.6%` mixed / `3.5%` pure             | same                                                | projection/camera-root contract 未复现                   |

### 3.2 Stage2 耦合来自 Stage1 严重约束，还是 Stage2 新增劣势？

当前证据支持“两者都可能贡献”，但优先级不同：

- Stage1 约束确实存在：Pulp camera latent 是 relative-distance contract，camera decode 依赖 human/root；self-trained source tokenizers 没有稳定复现官方 Stage1 upper bound 到 Stage2 transfer。
- Stage2 劣势也确实存在：在 Pulp official Stage1 支持下，clean camera completion 强，但 generated/noisy observed branch 下退化；joint mode 无 observed branch 时也弱于 clean completion。
- 因此 v6.3 的关键不是再问“Stage1 或 Stage2 哪个单独负责”，而是隔离：在复现 Pulp Stage1 后，用同一个 Stage2 config 比较 official ckpt / reproduced ckpt / controlled architecture ckpt；同时用 P2a/E.T. replay 测 Stage2 reliability。

### 3.3 KB/Web 增强后的耦合根源假设

这轮检索使用了本地 `papers-query-knowledge-base` 和 web 证据。核心外部锚点如下：

- [Pulp Motion GitHub](https://github.com/robincourant/pulp-motion) 与本地 4090 repo `/home/ripemangobox/Coding/Github/Motion/PulpMotion` 均已确认存在；README 给出 `src/train.py --config-name=CONFIG_NAME` 和 `src/evaluate.py` 的官方入口，官方模型仓库中包含 generation ckpt 与 `pulpmotion-models/autoencoder/aemmardm-xgmj0yjj-325.ckpt`。Pulp 明确把 human/camera joint latent 通过线性变换映射到 on-screen framing latent，并在采样时用辅助方向引导 coherence。
- [Towards Storytelling Animations CVF](https://openaccess.thecvf.com/content/CVPR2026/html/Cheng_Towards_Storytelling_Animations_Joint_Synthesis_of_Human_and_Camera_Motions_CVPR_2026_paper.html)：该工作把角色和相机作为独立且同等重要实体，并显式建模 pairwise interactions，而不是只做 raw latent concat。
- [MARDM arXiv](https://arxiv.org/abs/2411.16575)：其主张表示分布、预测目标和评估器失配会系统性放大扩散生成误差，支持我们不要只看 Stage1 feature MSE。
- [Robust Learning of Diffusion Models with Extremely Noisy Conditions](https://arxiv.org/html/2510.10149v1)：条件扩散依赖高质量条件；条件噪声会降低 controllability，因此需要显式估计或修正条件可靠性。

因此，当前最可能的耦合根源不是单一“Stage1 不好”，而是以下四个机制叠加：

1. **root-relative camera contract 的误差直通**：Pulp camera raw feature 显式包含 `camera_translation - human_root_translation`，decode 时再把 human root 加回 camera translation。这个 contract 对 GT human/root 是合理的，但当 observed human 来自生成器或带噪时，human root 误差会直接变成 camera world-space 误差。
2. **hard observed injection 导致条件盲信**：当前 completion 训练和采样把 observed branch 当作 clean truth。P2a 说明 `0.15` noise 就足以把 camera FDCLaTr 从 `14.50` 拉到 `96.87`；这更像 reliability modeling failure，而不是单纯生成能力不足。
3. **raw concat shared denoise 缺少关系控制面**：StoryMotion 当前把 human/camera latent 拼接后一起去噪，跨分支影响只能隐式发生；Pulp 的 `W` 行空间和 Storytelling Animations 的 pairwise interaction 都提示，应把“关系/构图”作为单独控制面，而不是让所有通道自由串扰。
4. **one-step objective 与 recursive sampler mismatch**：已有 joint sampler re-eval 显示 teacher `0.016472`，1-step `0.292046`，20-step `0.617884`，50-step `0.740053`。这与 MARDM 对预测目标/扩散误差放大的诊断一致：Stage2 不能只看 teacher-forced latent MSE。

直接结论：**Pulp Stage1 复现仍是必要 gate，但不应阻塞所有 Stage2 工作。所有只依赖 pretrained official Stage1 的 Stage2 decoupling 实验可以立即并行，因为它们回答的是条件可靠性、关系子空间、采样目标和 branch routing，而不是重新训练 Stage1。**

### 3.4 2026-07-01 三模式统一架构冲突诊断

代码事实：

- 当前 Stage2 主干不是 Transformer attention，而是共享通道 `TemporalObsUNet`。输入先执行 `torch.where(obs_mask, obs_x0, x_t)`，再拼接 `obs_mask`，因此 completion 模式会把 observed branch 硬注入为 clean condition。
- `TASK_CAMERA` 观察 human latent、预测 camera latent；`TASK_HUMAN` 观察 camera latent、预测 human latent；`TASK_JOINT` 不观察任何 latent，预测 human + camera。
- 文本约定为 1024 维：前 512 是 camera text，后 512 是 human text。`model.eval()` 时训练期随机 half-dropout 不再生效。
- 因此 joint 与 completion 的条件结构确实不对称：joint 是 text + noisy latent joint denoise；completion 是 observed branch 单向条件 + text。human/camera latent 在 joint 中通过共享 UNet 通道互相影响，在 completion 中影响方向由 observed mask 决定。

新增 v6.3 诊断脚本 `scripts/storymotion_v63_coupling_eval.py` 经 DeepSeek max 复查后修正了四个关键混杂：显式 device、文本样本内 half shuffle、joint `x_t` 按 diffusion 噪声尺度重采样、prediction shift 只在 target mask 上统计。1024 samples、5 timesteps 的 Phase 1 结果：

| run | camera completion drop camera text | camera completion shuffle camera text | human completion drop human text | joint drop camera text on camera | joint drop human text on human | joint human `x_t` noise → camera | joint camera `x_t` noise → human | camera obs zero | human obs zero |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| joint GRFSQ | +4.15% | +8.02% | +6.56% | +2.59% | +7.38% | +389.04% | +81.20% | +5096.56% | +351.76% |
| joint VAE | +0.76% | +1.12% | +0.54% | +0.11% | +6.18% | +3478.16% | +2014.50% | +134613.38% | +12223.94% |
| separate AE no-z | +1.51% | +3.09% | +6.27% | +0.62% | +5.82% | +481.35% | +21.50% | +3293.62% | +17.04% |
| separate VAE | +2.76% | +4.13% | +6.89% | +2.08% | +6.90% | +87.94% | +47.64% | +2913.39% | +51.15% |

读法：

- camera completion 对 camera text 的依赖偏弱，尤其 joint VAE 几乎只涨 `0.76% / 1.12%`；这支持“camera completion 被 observed human latent 支配，而不是公平使用 camera text”的怀疑。
- observed branch 破坏导致 camera branch 损失上升几十到上千倍，是当前最强信号；completion 模式确实是单向 observed-dominant。
- joint 模式中 human/camera latent 通过共享 UNet 强互扰，joint VAE 尤其严重；这条很可能是 coupling 根源之一，但它不是 Transformer attention，而是共享卷积通道 + concat denoise 的结果。

立即启动的 Phase 2 对照均使用同一个 `v6_2_joint_vae_wz_seed17_fullcache_20260701/mixed_full`、同 seed/steps/batch/lr，只改变任务分布和文本半区可见性：

| run | GPU | task distribution | text setting | purpose | ETA |
| --- | ---: | --- | --- | --- | --- |
| `cam_text_only_jointvae_full_b512` | 5090 GPU0 | camera only `[1,0,0]` | global CFG `0.1`，camera half drop `0.1`，human half always dropped `1.0` | 公平验证 camera-text-only camera completion 是否可学 | 2026-07-01 20:50-21:50 CST |
| `cam_full_text_jointvae_full_b512` | 5090 GPU1 | camera only `[1,0,0]` | global/camera/human half drop all `0.1` | 与 camera-text-only 对照，隔离 human text 是否造成 shortcut | 2026-07-01 20:50-21:50 CST |
| `joint_only_jointvae_full_b512` | 5090 GPU2 | joint only `[0,0,1]` | global/camera/human half drop all `0.1` | 判断三模式混训是否污染 joint text-only 生成 | 2026-07-01 20:50-21:50 CST |
| `completion_only_jointvae_full_b512` | 5090 GPU3 | completion only `[1,1,0]` | global/camera/human half drop all `0.1` | 判断 joint task 是否与 completion task 条件结构冲突 | 2026-07-01 20:50-21:50 CST |

这些训练完成后必须统一跑：

1. 同一 `storymotion_v63_coupling_eval.py` text / joint / observed diagnostics。
2. clean camera / human / joint official eval。
3. P2a noise `0.15/0.30` 和 generated-human replay。只有同时改善 text-dependence 与 reliability，才能写成 architecture fix；否则只能写成 failure diagnosis。

## 4. v6.3 实验优先级

| priority | experiment                                                                 | exact purpose                                          | metric gate                                    | decision                                                  |
| -------: | -------------------------------------------------------------------------- | ------------------------------------------------------ | ---------------------------------------------- | --------------------------------------------------------- |
|        1 | 4090 Pulp 官方仓库复现 Pulp official Stage1 AE                                   | 验证官方训练设置能否达到 official Stage1 upper bound；当前由本轮直接接管并已启动 | mixed/pure 三模式 official recon 接近 Pulp official | 若失败，先修 Stage1 train/data/normalization，不继续 Stage2 推断      |
|        2 | reproduced Stage1 + original Stage2 config                                 | 判断复现 ckpt 是否能传递到 Stage2                                | Stage2 mixed human/camera/joint official rows  | 若 Stage1 复现但 Stage2 仍弱，聚焦 Stage2 transfer                 |
|        3 | official Pulp Stage1 vs reproduced Stage1 vs self-trained source tokenizer | 同 Stage2 seed/config 的 controlled comparison           | full mixed official + P2a reliability          | 隔离 ckpt 质量与 architecture 差异                               |
|        4 | generated-human-aware training / quality-aware observed branch             | 修复 camera 对 generated/noisy human/root 的盲信             | P2a noise slope、E.T. replay、joint metric       | clean 不掉太多且 noise/replay 明显改善才保留                          |
|        5 | camera latent decoupling ablation                                          | 验证 relative-distance / human-camera concat 是否是硬瓶颈      | clean camera、joint、P2a、replay                  | 若 global/root-independent camera 同时改善 joint 与 replay，升级主线 |
|        6 | sampler/text-conditioning audit                                            | 解释 teacher-forced 好但 multi-step/joint 弱                | text shuffle、sampler grid、caption/TMR/CLaTr    | 若语义弱主要来自 sampler/text，则先修 Stage2 inference/training       |

## 4.1 可并行的 pretrained Stage1 Stage2 核心实验

这些实验全部使用 Pulp official pretrained Stage1，不等待 4090 Stage1 复现完成。它们的目标是定位并修复 decouple 问题，而不是证明新 tokenizer。

| priority | experiment                                     | change                                                                                                                                 | coupling root tested                        | metric gate                                                                              |
| -------: | ---------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------- | ---------------------------------------------------------------------------------------- |
|     S2-1 | Pulp `W` row-space auxiliary sampling retrofit | 在 StoryMotion joint / completion sampler 中加入 Pulp official `W_proj` / `P_parallel` 引导，扫 `w_z`                                          | raw concat 缺少 framing relation control      | clean 不显著下降；P2a `0.15/0.30` 和 generated-human replay 的 FDCLaTr / Out / F1 改善             |
|     S2-2 | reliability-aware observed branch              | 训练时随机注入 generated/noisy observed branch，并加入 source tag、noise sigma 或 trust scalar；推理时替代 hard observed injection                        | observed branch 盲信                          | P2a slope 降低；E.T. replay 不再接近 joint collapse；clean camera 允许小幅下降但不能失守                    |
|     S2-3 | pairwise relation adapter                      | 保留 pretrained Stage1 latent，不改 AE；在 Stage2 中用 human token、camera token、relation token 三路，增加 human-camera pairwise interaction residual | branch routing 隐式、跨通道串扰                     | visible shuffle 敏感性保留，但 noise/shuffle observed branch 退化下降；joint metric 优于 raw concat    |
|     S2-4 | relation-subspace two-pass refinement          | 第一次生成 independent/base human-camera，第二次只在 `W` 行空间或 relation residual 上 refinement                                                      | 一步 joint denoise 同时承担单模态质量和关系修复             | human/camera 单模态 metric 不掉，framing / Out-rate / P2a 明显改善                                 |
|     S2-5 | camera root residual split                     | camera branch 分成 text-only global camera prior 和 human-conditioned root/framing residual；残差支路加 stop-gradient 或 trust gate              | root-relative camera contract 误差直通          | generated-human condition 下 RootFrame、FDCLaTr、MPJPE 同时改善；clean camera 不劣于 E.T. root-only |
|     S2-6 | Stage2 prediction target / sampler audit       | 在同一 pretrained Stage1 latent 上比较 x0、epsilon、v-pred、DDIM step 数和 schedule distillation                                                  | teacher-forced 与 recursive sampler mismatch | teacher / 1-step / 20-step / 50-step gap 收缩；official joint 不再随采样步数恶化                     |

优先级建议：

1. **先跑 S2-1**：成本最低，直接复用 Pulp 的数学结构；如果有效，说明 relation subspace 是缺失控制面。
2. **并行跑 S2-2**：当前最直接对应 P2a 和 replay collapse；如果有效，论文主线可以从“decoupled representation”收缩为“source/reliability-aware coupling contract”。
3. **S2-3 / S2-4 二选一先做轻量版**：如果 S2-1 有效，做 relation-subspace refinement；如果 S2-1 无效，做 pairwise adapter，测试架构级 routing。
4. **S2-6 作为审计后台跑**：它不一定直接修 decouple，但能解释为什么 teacher loss 不传递到 50-step official metric。

## 4.2 KB/Web 相关工作：不对称多任务不是 raw concat

本节使用 `papers-query-knowledge-base` 的本地分析 note 作为主证据，并用 web/官方 repo 校验项目链接与开源状态。涉及的本地 note 包括 [Pulp Motion(ICLR_2026)](../../analysis/ICLR_2026/Pulp_Motion_Framing_aware_multimodal_camera_and_human_motion_generation.md)、[Towards Storytelling Animations(CVPR_2026)](../../analysis/CVPR_2026/Towards_Storytelling_Animations_Joint_Synthesis_of_Human_and_Camera_Motions.md)、[CondMDI(SIGGRAPH_2024)](../../analysis/SIGGRAPH_2024/Flexible_Motion_In_betweening_with_Diffusion_Models_CondMDI.md)、[PriorMDM(ICLR_2024)](../../analysis/ICLR_2024/HUMAN_MOTION_DIFFUSION_AS_A_GENERATIVE_PRIOR.md)、[OmniControl(ICLR_2024)](../../analysis/ICLR_2024/OmniControl_Control_Any_Joint_at_Any_Time_for_Human_Motion_Generation.md)、[MoReact(TMLR_2025)](../../analysis/TMLR_2025/MoReact_Generating_Reactive_Motion_from_Textual_Descriptions.md)、[MotionLab(ICCV_2025)](../../analysis/ICCV_2025/MotionLab_Unified_Human_Motion_Generation_and_Editing_via_the_Motion_Condition_Motion_Paradigm.md)、[MoLingo(CVPR_2026)](../../analysis/CVPR_2026/MoLingo_Motion_Language_Alignment_for_Text_to_Human_Motion_Generation.md)、[AnyMo(arxiv_2026)](../../analysis/arxiv_2026/AnyMo_Scaling_Any-Modality_Conditional_Motion_Generation_with_Masked_Modeling.md)、[Lance(arxiv_2026)](../../analysis/arxiv_2026/Lance_Unified_Multimodal_Modeling_by_Multi-Task_Synergy.md)、[UniMo(arxiv_2026)](../../analysis/arxiv_2026/UniMo_Unified_Motion_Generation_and_Understanding_with_Chain_of_Thought.md) 与 [UniMuMo(AAAI_2025)](../../analysis/AAAI_2025/Unified_Text_Music_and_Motion_Generation.md)。

| work                            | task shape                           | how asymmetry/multitask is handled                                       | implication for StoryMotion                                                     |
| ------------------------------- | ------------------------------------ | ------------------------------------------------------------------------ | ------------------------------------------------------------------------------- |
| Pulp Motion                     | human-camera joint generation        | 用 on-screen framing latent 作为关系控制面，采样时在 W row-space 做 auxiliary guidance | camera 依赖 human/framing 是事实；缺的是显式 relation subspace                             |
| Towards Storytelling Animations | human/camera storytelling animation  | character 与 camera 是独立实体，并显式建模 character-camera pairwise interaction     | 不应只拼 latent；应有 entity/relationship routing                                      |
| CondMDI                         | arbitrary motion in-betweening       | 随机 keyframe/joint masks 训练对称 partial observation                         | 当前 StoryMotion 是语义分支级不对称 mask，直接套 hard replacement 有盲信风险                        |
| PriorMDM / ComMDM               | composition / multi-person / control | 冻结 prior，加入小通信模块或 specialist blending                                    | 统一不等于 share-all；可以 separate priors + lightweight communication                  |
| MoReact                         | reactive motion                      | 明确 trajectory -> local/reaction 的两阶段依赖                                   | 不对称依赖应被排序建模，不能假装 camera 与 human 对等独立                                            |
| OmniControl                     | spatially controlled motion          | 内部相对表示 + 输出/全局空间 guidance 与 realism guidance                             | 若内部 latent 难控，可在 output/framing space 加约束面                                      |
| MotionLab                       | generation/editing unified motion    | Motion-Condition-Motion + task instruction + curriculum + rectified flow | RF 只是统一范式的一部分，关键还有 task instruction 与 condition design                          |
| MoLingo                         | text-to-human motion                 | semantic latent + T5 multi-token CrossAttn + masked AR rectified flow    | 可借鉴 semantic latent / CrossAttn / masked modeling；不能直接照搬到 human-camera coupling |
| AnyMo / UniMuMo / Lance         | unified multimodal / omni modeling   | modality-specific paths、experts、tokens、curriculum 或 masked modeling      | 高影响 unified 工作通常保留模态/任务专用容量，不是完全共享 raw concat                                   |

统一结论：**camera 依赖 human 是建模事实，而不是需要消除的“污染”。真正需要 decouple 的是错误的信息流与可靠性假设：human 作为条件应进入 camera，但 camera 噪声不应反向污染 human；GT human 与 generated/noisy human 应有不同 source/reliability contract；human-camera relation/framing 应有显式控制面。**

## 4.3 Backbone / RF / Causal 裁决【低优先级，优先解决couple问题】

DeepSeek max 复核 session `7042eeacd6d7` 已关闭，核心裁决如下。

### 4.3.1 Stage2 是否 CondMDI / UNet，是否换 backbone

当前 Stage2 是 **CondMDI-style TemporalObsUNet**：它继承了 observed mask + observed x0 拼接的思想，并使用 temporal Conv1D UNet；但它不是 CondMDI 原论文的完整随机 keyframe/joint mask 训练范式。更关键的是，CondMDI 的 mask 是对称任意部分观测，而 StoryMotion 的 camera/human completion 是语义分支级不对称任务。

当前不应把“换 Transformer/DiT”作为第一修复。证据上，clean oracle camera completion 已经强，说明 UNet 容量不是最先暴露的瓶颈；P2a 和 replay collapse 指向的是 hard observed injection 与 generated/noisy source mismatch；Phase1 diagnostics 指向的是 share-all 通道互扰和 camera text 依赖弱。换 backbone 会重置对照体系，却不能自动解决条件盲信。

更合理的最小改法是：

- 保留 pretrained Pulp official Stage1 和当前 Stage2 对照口径。
- 在 Stage2 引入 task adapter / branch-specific head。
- human denoise 不读取 camera latent；camera denoise 可单向读取 human feature 或 human x0，并对 human path stop-gradient。
- 用 relation/framing token 或 Pulp `W` row-space 作为显式控制面，而不是让 raw latent concat 自由串扰。

### 4.3.2 DDPM/DDIM vs Rectified Flow

当前代码是 DDPM q_sample + x0 prediction，official eval 使用 DDIM sampler，不是 rectified flow。MoLingo 与 MotionLab 说明 RF 在高效采样、统一编辑/生成和连续 latent 生成上有价值；但 StoryMotion 当前最大负例是 **clean condition 强、noisy/generated observed branch 崩**。这不是 RF 天然能解决的问题。

因此 RF 的位置应是后置消融，而不是主线修复：

- 如果 routing/reliability 修复后仍有 teacher-forced 与 multi-step sampler gap，再比较 x0 / epsilon / v-pred / RF。
- 若直接改 RF，同时保留 hard observed injection 和 share-all channel，极可能只是换了采样路径，coupling 仍在。
- 论文中不能写“采用 MoLingo-style rectified flow”或“RF 解决 camera coupling”，除非真的完成同口径实现和 ablation。

### 4.3.3 Causal Modeling

当前没有 causal modeling。对离线 cinematic camera generation 来说，逐帧 temporal causal mask 不一定合理，因为 camera 往往需要看见未来 human action 才能提前构图。真正有意义的是 **结构因果 / directed dependency**：

```text
story/text -> human intent/root/motion -> camera framing/residual
```

这不要求绑定成 raw joint 模型。相反，separate 或 shared-backbone-with-adapters 更合理：human prior 先生成或去噪，camera branch 单向查询 human feature / relation token；joint 输出应被视为 human-first + camera-conditioned composition，而不是 human/camera 同权双向去噪。

只有在目标变成在线/streaming camera control 时，temporal causal 才是必要设计；当前 v6.3 不应把 causal 当增点主线。

## 4.4 下一批实验排序与预计完成时间

这批实验均可基于 Pulp official pretrained Stage1 先跑，不等待 4090 Pulp Stage1 复现完成；4090 复现仍是 Stage1 contract gate，但不阻塞 Stage2 coupling 诊断。

| priority | code name | experiment | purpose | cost / ETA |
| ---: | --- | --- | --- | --- |
| 1 | PULP_ROBUST | 用 Pulp official latent / framing relation 做 clean vs noisy human camera 探针，扫 sigma `0/0.15/0.30` | 判断 Pulp-style framing relation 是否比 StoryMotion hard obs 更抗噪 | \<1 GPU-hour；当天完成 |
| 2 | TWO_STAGE_INFERENCE | 现有模型先 human，再用 generated human 做 camera completion，不重训 | 低成本测 single joint vs sequential dependency 的差距 | \<1 GPU-hour；当天完成 |
| 3 | INJECT_NOISE_AUG | Stage2 TASK_CAMERA 训练时对 observed human latent 注入随机 sigma `0-0.3` 与 source tag/trust scalar | 验证 P2a collapse 是否来自 hard observed train/test mismatch | 8-12 GPU-hours；1 天内 |
| 4 | JOINT_STOPGRAD | joint 模式中 camera 可读 human feature，但 human path stop-gradient / 不读 camera | 直接验证对称 share-all 是否是 joint 劣化根因 | 4-8 GPU-hours；1 天内 |
| 5 | TASK_ADAPTERS | shared UNet + task embedding / FiLM-AdaLN / branch-specific output head / camera->human 禁止 | 轻量验证不拆 backbone 的 routing 修复 | 16-24 GPU-hours；2-3 天 |
| 6 | PULP_FRAMING_HEAD | 在 StoryMotion Stage2 camera 分支加 Pulp-like on-screen framing auxiliary head | 若 PULP_ROBUST 有效，验证 relation head 能否内化 | 12-24 GPU-hours；2-3 天 |
| 7 | ASYMMETRIC_TWOSTREAM | 重训 asymmetric dual-stream：human 独立，camera 单向 conditioned on human | 最终架构候选，不作为第一轮盲投 | 40+ GPU-hours；3-5 天 |
| 8 | RF_ABLATION | 在 routing/reliability 已修后再切 RF | 仅评估采样范式的纯贡献 | 40+ GPU-hours；后置 |

预计完成时间口径：

- 已在跑的四个 mode-conflict 对照预计仍按 `2026-07-01 20:50-21:50 CST` 完成首轮训练，随后统一跑 diagnostics / clean / P2a / replay。
- 新增 PULP_ROBUST 与 TWO_STAGE_INFERENCE 可在当天补齐，优先占用空闲 4090/5090。
- INJECT_NOISE_AUG 与 JOINT_STOPGRAD 可并行排队，若 4 卡可用，首轮关键结论应在 24 小时内得到。
- TASK_ADAPTERS / PULP_FRAMING_HEAD 是 P0 结论后的 2-3 天窗口。
- ASYMMETRIC_TWOSTREAM 与 RF_ABLATION 不应抢占第一批资源，除非 P0/P1 证据明确支持。

## 4.5 实验池污染审计

实验池只允许 active / comparable run 进入主表。旧实验可以保留为历史证据，但必须在 registry 或汇总脚本中显式排除。

| scope                                     | path pattern                                                                                                  | reason                                                                     | action                                                                                              |
| ----------------------------------------- | ------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------- |
| old mixed camera manifests                | `agent2_pulpmotion_camera_mixed_*_manifest_full_20260621.jsonl`                                               | 只有 `29779/3279` paired rows，会把 train/cache/eval 限制成 mixed-subset           | keep for provenance; exclude from new train/eval                                                    |
| corrected full mixed manifests            | `agent2_pulpmotion_camera_mixed_*_manifest_full_20260630.jsonl`                                               | `94050/10549` paired rows，是当前 full mixed 口径                                | keep active                                                                                         |
| deleted old mixed joint Stage1            | `joint_vae_wz_mixed_bs128_seed17_500ep_gpu1_20260630`, `gpu*_joint_*_mixed_500ep` under `v5_pulp192_20260621` | 旧 mixed 训练不满足 full manifest 判据；上一轮已删除 4090/5090 mixed 目录                   | delete completed; do not restore                                                                    |
| remaining `v5_pulp192_20260621` pure dirs | `runs/train/stage1/joint/v5_pulp192_20260621/gpu*_pure_500ep`                                                 | pure 不受 mixed camera manifest 缺失影响，但仍是旧命名和旧代码时期产物                          | keep as legacy pure only; exclude from mixed claims                                                 |
| corrected joint full dirs                 | `runs/train/stage1/joint/joint_*_wz_mixed_full_*_20260630` and `runs/train/stage2/v6_2_joint_*_20260701`      | 使用 full mixed manifest 和 current source-tokenizer-aware Stage2 cache/train | keep active, but metrics are negative diagnostic                                                    |
| old v5 / 20260621-20260629 Stage2 sweeps  | `runs/train/stage2/v5_*`, `v6_2_*_20260629`, P2 followups                                                     | 多数是 subset、smoke、ablation 或旧 reliability 诊断，不同口径混在主池会污染结论                  | keep archived/provenance; exclude from primary comparison unless table explicitly labels diagnostic |
| old visualization manifests               | `runs/visualizations/archived/**`                                                                             | 已被 2026-07-01 active rerun superseded                                      | keep archived; Gradio registry must exclude                                                         |

2026-07-01 执行结果：

- 4090/5090 上旧 mixed-subset manifests、旧 v5 Stage1/Stage2、smoke、archived visualization、`_accidental_sync_20260701` 已删除；删除日志分别见 4090/5090 delete log。
- 5090 上残留的旧 `sm_v5_pure_joint_eval` tmux 命令已终止，避免继续指向已删除污染指标路径。
- 4090/5090 目标目录按 `20260621`、`v5_*`、`*_smoke*`、`archived`、`_accidental_sync_20260701` 复查无污染残留。少量 native/pure/full manifest 保留为非污染 provenance，不进入新实验主表。

## 5. 暂停或降级的方向

- 不继续把 VAE/GRFSQ/HFSQ tokenizer 当主线扩展，除非先通过 Pulp official Stage1 reproduction gate。
- 不把 Stage1 training loss 当主指标；每个 Stage1 都必须进入 decoded official recon metric。
- 不把 clean camera completion 写成 robust camera generation；必须同时报告 generated/noisy observed branch。
- 不把 E.T./DIRECTOR replay 当 full external joint baseline；它是 camera condition reliability 诊断。
- 不把 P2b v1/v2 写成已解决方案；v1 clean drop 过大，v2 仍未回到 P0 clean。

## 6. v6.3 最小闭环

最小可交付不是更多表，而是一个因果隔离闭环：

1. Pulp official Stage1 复现：same split、same official recon metric、pure/mixed 三模式。
2. Stage2 transfer：official ckpt / reproduced ckpt / current source tokenizer 使用同一 Stage2 config 和 seed17。
3. Reliability：每个候选必须同时跑 clean、P2a noise `0.15/0.30`、generated-human replay。
4. 结论只按 evidence 写：如果 Stage1 复现失败，先修 Stage1；如果 Stage1 复现成功但 Stage2 仍退化，v6.3 主问题就是 Stage2 reliability / sampler / observed branch source mismatch。

## 7. Evidence Paths

- metric data page: [[2026-07-01_storymotion-v6.2-metric-data]]
- Pulp Stage1 official recon: `/data/public/ripemangobox/Motion/StoryMotion/runs/eval/pulpmotion_core_bs64_20260625/stage1`
- Pulp Stage1 official reproduction tmux: `pulp_stage1_official_repro_g0_20260701`
- Pulp Stage1 official reproduction log: `/data/public/ripemangobox/Motion/PulpMotion/results/stage1_official_repro_20260701/train.log`
- Pulp Stage1 official reproduction metrics: `/data/public/ripemangobox/Motion/PulpMotion/results/stage1_official_repro_20260701/metrics.jsonl`
- Pulp Stage1 official reproduction script: `/data/public/ripemangobox/Motion/PulpMotion/artifacts/repro/stage1_official_20260701/train_stage1_autoencoder_official.py`
- StoryMotion v6 native baseline: `/data/public/ripemangobox/Motion/StoryMotion/stage2/metrics/v6_p0_native_20260625`
- E.T./DIRECTOR seed17 eval: `/data/public/ripemangobox/Motion/StoryMotion/stage2/metrics/v6_2_seed17_eval_20260630`
- full mixed v6.2 eval: `/data/public/ripemangobox/Motion/StoryMotion/stage2/metrics/v6_2_fulltrain_eval_20260701`
- joint full mixed eval: `/data/public/ripemangobox/Motion/StoryMotion/stage2/metrics/v6_2_joint_fulltrain_eval_20260701`
- Stage1 posthoc eval: `/data/public/ripemangobox/Motion/StoryMotion/stage2/metrics/v6_2_joint_stage1_recon_eval_20260701`
- P2a matched noise: `/data/public/ripemangobox/Motion/StoryMotion/stage2/metrics/v6_p2a_matched_noise_20260625`
- P2b reliability: `/data/public/ripemangobox/Motion/StoryMotion/stage2/metrics/v6_p2b_robustness_20260628`
- latent diagnostics: `/data/public/ripemangobox/Motion/StoryMotion/runs/eval/stage2_gated_diag_20260613`
- pollution deletion log 4090: `/data/public/ripemangobox/Motion/StoryMotion/artifacts_delete_pollution_20260701_4090.log`
- pollution deletion log 5090: `/data/public/ripemangobox/Motion/StoryMotion/artifacts_delete_pollution_20260701_5090.log`
- v6.3 coupling diagnostic script: `/data/public/ripemangobox/Motion/StoryMotion/scripts/storymotion_v63_coupling_eval.py`
- v6.3 coupling diagnostics: `/data/public/ripemangobox/Motion/StoryMotion/stage2/metrics/v6_3_coupling_20260701`
- v6.3 mode-conflict training runs: `/data/public/ripemangobox/Motion/StoryMotion/runs/train/stage2/v6_3_mode_conflict_20260701`
