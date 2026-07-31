---
title: "StoryMotion Stage2 Backbone Redesign"
created: 2026-07-03T01:05:15+0800
updated: 2026-07-03T17:55:00+0800
status: active
hypothesis: "Stage2 不应继续沿用单体 joint denoiser 或 CondMDI 式局部修补，而应重构为 Motion-Condition-Motion 任务接口下的非对称 human-to-camera pipeline。"
tags:
  - StoryMotion
  - status/active
  - stage2
  - architecture
source_papers:
  - "[[analysis/ICCV_2025/MotionLab_Unified_Human_Motion_Generation_and_Editing_via_the_Motion_Condition_Motion_Paradigm|MotionLab]]"
  - "[[analysis/CVPR_2024/DanceCamera3D_3D_Camera_Movement_Synthesis_with_Music_and_Dance|DanceCamera3D]]"
  - "[[analysis/ICCV_2025/GenDoP_Auto_regressive_Camera_Trajectory_Generation_as_a_Director_of_Photography|GenDoP]]"
  - "[[analysis/ICLR_2026/Pulp_Motion_Framing_aware_multimodal_camera_and_human_motion_generation|Pulp Motion]]"
  - "[[analysis/CVPR_2026/Towards_Storytelling_Animations_Joint_Synthesis_of_Human_and_Camera_Motions|Towards Storytelling Animations]]"
  - "[[analysis/CVPR_2024/MCM_LDM_Arbitrary_Motion_Style_Transfer_with_Multi_condition_Motion_Latent_Diffusion_Model|MCM-LDM]]"
  - "[[analysis/SIGGRAPH_2024/Taming_Diffusion_Probabilistic_Models_for_Character_Control|CAMDM]]"
  - "[[analysis/ICCV_2025/MotionStreamer_Streaming_Motion_Generation_via_Diffusion_based_Autoregressive_Model_in_Causal_Latent_Space|MotionStreamer]]"
---

# StoryMotion Stage2 Backbone Redesign

> [!abstract] 结论
> Stage2 需要重构。当前 v7.2 / CP 实验说明，Clean-Preserving、TrustGate、TextRoleRouter 这类局部补丁无法解决 StoryMotion 的核心问题：生成链路没有稳定地学到“给定 human/source motion 后，如何生成可靠 camera/framing”的非对称条件关系。KB 证据支持把 Stage2 主干改成 **MotionLab 式 Motion-Condition-Motion 任务接口 + DanceCamera3D 式 camera completion 分支**，而不是继续强化单体 joint diffusion。

## 失败边界

当前实验的关键事实是：

- clean 下可以保持接近基线，但 noise0.15 下仍崩溃，说明小修补没有学到真正的 source corruption robustness。
- CP1 / CP2 保住 clean，却没有提升 noisy；CP3 改善 noisy 但明显伤 clean，说明当前结构在 clean fidelity 与 noisy robustness 之间是硬 trade-off。
- 现有 official eval sampler 没有传入 v7.2 的 `task` / `source_meta`，所以它能说明 checkpoint 在实际协议下无效，但不足以证明单个 routing 模块的因果失败。

因此 Stage2 的问题不应再表述为“还差一个更好的 gate / router / loss”，而应表述为：**Stage2 需要一个能把 source motion、condition、target camera 分层建模的数据与架构骨架。**

## Backbone 候选判断

### 首选：MotionLab 作为任务接口骨架

[[analysis/ICCV_2025/MotionLab_Unified_Human_Motion_Generation_and_Editing_via_the_Motion_Condition_Motion_Paradigm|MotionLab]] 的核心价值不是直接拿来生成 camera，而是它把任务统一为 **source motion / condition / target motion** 三元组，并用 Motion Curriculum Learning 处理多任务训练冲突。这个抽象与 Stage2 完全对齐：

- source motion：Stage1 human motion，包含 clean / corrupted / generated replay 三类来源。
- condition：camera text、story context、framing intent、可选 human text。
- target motion：camera trajectory 或 camera-relative framing sequence。

这比 CondMDI 风格的 mask/in-betweening 更适合 Stage2，因为 StoryMotion 不是单纯补全缺失片段，而是 source-conditioned camera synthesis。MotionLab 的 Aligned ROPE 和 task instruction modulation 也提示 Stage2 不应把不同任务混成一个无标签训练集。

### 主生成分支：DanceCamera3D 作为 H2C camera completion backbone

[[analysis/CVPR_2024/DanceCamera3D_3D_Camera_Movement_Synthesis_with_Music_and_Dance|DanceCamera3D]] 是最接近 Stage2 非对称设计的可靠证据：它不联合生成 human 和 camera，而是给定 3D pose / music 生成 camera。它的两个结论对 Stage2 尤其关键：

- body attention loss 显著降低人物出画，说明 projection/framing 约束必须进入训练或验证协议，而不是只看 camera MSE。
- strong-weak condition separation 说明不同条件权重不能共用一个 global CFG；human/source motion 应是强条件，text/style/story 是弱或中等条件。

这直接支持 Stage2 的非对称路线：**human branch 先稳定，camera branch 作为主要学习对象。**

### 备选相机表示：GenDoP 作为 camera tokenizer / AR prior

[[analysis/ICCV_2025/GenDoP_Auto_regressive_Camera_Trajectory_Generation_as_a_Director_of_Photography|GenDoP]] 不适合作为整个 StoryMotion Stage2 的唯一主干，因为它是 camera-only / scene-conditioned trajectory generation，不直接处理 human-camera coupling。但它对 Stage2 的 camera 表示非常有价值：

- 典型归一化对结果是决定性模块；移除后文本对齐和轨迹质量大幅恶化。
- camera trajectory 可以离散化为 token 并自回归生成，天然降低扩散轨迹抖动。
- Motion Caption / Directorial Caption 的数据拆分提示 Stage2 数据应同时保留低层运动描述和高层导演意图。

如果 Stage2 选择 camera token 路线，GenDoP 应作为 camera branch 的 representation/prior，而不是替代 H2C 条件建模。

## 不应作为主干的路线

### Pulp Motion：适合作为诊断和辅助引导，不适合作为新主干

[[analysis/ICLR_2026/Pulp_Motion_Framing_aware_multimodal_camera_and_human_motion_generation|Pulp Motion]] 证明 on-screen framing 是 human-camera 关系的关键辅助模态，也证明中等强度的 auxiliary guidance 可以改善出画率。但当前实验已经显示，仅在原有 joint generation 上做 sampling / gating / preserving，不足以解决 noisy source 崩溃。

Stage2 可以保留 Pulp 的 framing latent / out-rate / auxiliary guidance 作为评估与 refinement 工具，但不应继续把它当成核心架构。

### Towards Storytelling Animations：提供交互模块证据，但单体 joint diffusion 风险高

[[analysis/CVPR_2026/Towards_Storytelling_Animations_Joint_Synthesis_of_Human_and_Camera_Motions|Towards Storytelling Animations]] 的双向角色-相机交互模块和 Toric camera 表示很有参考价值，尤其证明显式 interaction 比简单拼接更强。但它的前提是 joint clean distribution，而 StoryMotion 当前失败点恰恰是 noisy / generated source 下的稳定条件化。

因此它适合提供 final joint refinement 或 pairwise interaction adapter 的设计证据，不适合作为 Stage2 首个重构 backbone。先做单体 joint diffusion，风险是继续复现 v7.2 的 clean/noisy trade-off。

### CondMDI / 局部补全：作为 baseline，不作为 Stage2 backbone

已有实验已经说明 CondMDI 式结构加 clean-preserving 补丁不能解决核心问题。Stage2 仍可保留它作为 interpolation/editing baseline，但不应再以它为架构中心。

## 推荐 Stage2 架构

推荐骨架：

```text
Stage1 / source human motion
  -> source quality tagging
     clean | synthetic corruption | generated replay
  -> relation feature process
     root trajectory, velocity, body bbox/projection, shot scale, visibility, screen center
  -> Stage2 H2C camera generator
     MotionLab-style source-condition-target interface
     DanceCamera3D-style camera completion
     optional GenDoP camera token / canonical normalization
  -> framing verifier / optional refiner
     Pulp-style framing latent, out-rate, projection loss, temporal smoothness
```

关键设计原则：

- **非对称**：human 是强条件和误差来源，camera 是主生成目标；不要一开始就让 human 与 camera 在同一个 denoiser 里同权竞争。
- **pipeline 优先**：先稳定 human source representation，再生成 camera，再做轻量 joint refinement。
- **data process 优先于模块补丁**：必须显式构建 clean / corrupted / generated replay 三类 source，而不是只加高斯噪声。
- **condition priority**：参考 MCM-LDM / CAMDM，把条件分成主条件和辅条件，避免 camera text、human source、style/story 在一个 embedding 里互相淹没。
- **framing 进入训练闭环**：至少加入 projection-derived metrics；更进一步可加入 DanceCamera3D 式 visibility/body attention loss。

## 数据流程要求

Stage2 数据不应只保存 `(human, camera, text)` 三元组，而应扩展为：

```text
source_human_type:
  gt_clean | gt_corrupted | generated_replay

source_human:
  normalized joint/root representation

relation_features:
  root trajectory, root velocity, heading, body bbox, projected joints,
  in-frame ratio, shot scale, screen center, camera-human distance

conditions:
  camera text, story/directorial text, optional human action text

target_camera:
  canonical relative pose or tokenized camera sequence
```

这里最重要的是 `generated_replay`。现有 noise0.15 失败说明高斯噪声不是 Stage1 错误分布的充分替代。Stage2 需要看见真实 Stage1 生成误差，否则 clean/noisy trade-off 会继续存在。

## 最小可验证 Stage2

第一版不应从完整大模型开始。最小可验证版本只需要证明 H2C 非对称 backbone 是否成立：

1. 固定 human source，不更新 human。
2. 用 clean / corrupted / generated replay 三类 source 训练 camera generator。
3. camera 表示先用 canonical relative pose；若抖动严重，再切 GenDoP-style camera token。
4. 评估同时报告 clean 与 noisy/replay：
   - camera FID / ADE
   - out-rate / in-frame joint ratio
   - shot scale stability
   - text-camera alignment
   - clean retention gap

如果这个 H2C 版本无法在 noisy/replay source 上稳定提升，同时保持 clean 不崩，则 StoryMotion 的 Stage2 问题不在 joint modeling，而在数据分布或评估定义；反之，再考虑加 Towards Storytelling Animations 式 pairwise interaction adapter 做 final joint refinement。

## 当前决策

Stage2 backbone 建议定为：

> **MotionLab-style MCM task backbone + DanceCamera3D-style H2C camera completion, with GenDoP-style camera representation as optional upgrade.**

Pulp Motion / Towards Storytelling Animations / MCM-LDM / CAMDM / MotionStreamer 的角色分别是：

- Pulp Motion：framing latent、out-rate、auxiliary guidance 与 eval protocol。
- Towards Storytelling Animations：后续 joint refinement 的 pairwise interaction adapter 参考。
- MCM-LDM：条件优先级与主辅条件注入参考。
- CAMDM：分离条件 tokenization、past-motion CFG、source influence control 参考。
- MotionStreamer：generated replay / autoregressive exposure bias 的训练启发。

这一路线比继续修补 v7.2 更必要，因为它改变的是 Stage2 的问题定义：从“联合生成 human-camera”改为“在可靠 source process 上生成 camera/framing，再做可控 refinement”。

## DeepSeek 审查与落地 2026-07-03

DeepSeek 严格审查后给出保留意见：仅把 Stage2 改成非对称 H2C 并不能自动解释 noisy source robustness，必须证明新 contract 与旧 H2C / CP 路线在因果上不同。采纳后的工程判据是：先实现最小 H2C trainer/evaluator，跑通 clean/noise latent eval 和 official camera eval，再启动长训；official full conclusion 只能在长训后按 kill criteria 判定。

本次新增实现：

- `linkedCodebases/StoryMotion/scripts/train_stage2_h2c_minimal.py`
- 模型：固定 human latent 作为 observed condition，只预测 camera latent。
- 数据：复用 `runs/train/stage2/pulp_official_full_mixed_20260611/cache_mixed_full_nw0_20260611_2110`。
- 评估：`eval-latent` 支持 clean / noisy 0.05 / 0.10 / 0.15 / 0.20；`eval-official-camera` 支持 Pulp official camera metrics。

已完成 smoke：

```text
remote: 4090 /data/public/ripemangobox/Motion/StoryMotion
check: pass
20-step train smoke: pass
latent eval 128 samples: pass
official camera clean 64 samples: pass
official camera noisy:0.15 64 samples: pass
```

Smoke 结果只证明 pipeline 可运行，不证明方案有效。20 step checkpoint 的 official FCD 仍在 500+，不可用于论文结论。

已完成 H2C minimal 长训：

```text
run_dir: runs/train/stage2/stage2_h2c_minimal_clean_20260703
train_source: clean
steps: 60000
selection_metric: clean_camera_mse

run_dir: runs/train/stage2/stage2_h2c_minimal_noisy015_20260703
train_source: noisy
train_noise_std: 0.15
steps: 60000
selection_metric: noisy_0.15_camera_mse
```

full official eval 结果见 [[2026-07-01_storymotion-v7.2-metric-data#9. Stage2 H2C / MoLingo FullRF Official Eval 2026-07-03|StoryMotion Metric Data §9]]。关键读数：

| model | eval source | FDCLaTr↓ | F1↑ | readout |
| --- | --- | ---: | ---: | --- |
| H2C minimal clean | clean | 15.20 | 0.665 | matched clean strong |
| H2C minimal clean | noisy `0.15` | 824.33 | 0.048 | noisy source collapse |
| H2C minimal noisy015 | clean | 1022.65 | 0.055 | clean source collapse |
| H2C minimal noisy015 | noisy `0.15` | 26.71 | 0.587 | matched noisy strong |

结论：H2C 非对称 contract 可以在 matched source distribution 下工作，但 clean 与 noisy `0.15` 训练出现强分布分裂。只把任务改成 H2C 不能解决 robust source conditioning。

## MoLingo FullRF 复核 2026-07-03

按用户要求，4090 与 5090 双向同步了关键代码与配置；5090 上完成的 MoLingo FullRF ckpt 已 scp 到 4090，并在 4090 上按 full official protocol 评估。5090 曾短暂启动 eval，但已停止，最终有效记录全部来自 4090：

```text
protocol:
  split: full mixed test
  samples: 10549
  batch_size: 64
  seed: 17
  callback: Pulp/StoryMotion official camera metrics

runs:
  stage2_molingo_fullrf_h2c_clean_20260703
  stage2_molingo_fullrf_h2c_noisy015_20260703
  stage2_molingo_fullrf_h2c_v64_p2b_20260703
```

| model | eval source | FDCLaTr↓ | F1↑ | readout |
| --- | --- | ---: | ---: | --- |
| MoLingo FullRF clean | clean | 18.59 | 0.651 | clean strong |
| MoLingo FullRF clean | noisy `0.15` | 625.57 | 0.124 | noisy collapse remains |
| MoLingo FullRF noisy015 | clean | 611.09 | 0.101 | clean collapse remains |
| MoLingo FullRF noisy015 | noisy `0.15` | 31.05 | 0.490 | matched noisy works |
| MoLingo FullRF p2b | clean | 22.67 | 0.590 | best clean/noisy compromise |
| MoLingo FullRF p2b | noisy `0.15` | 40.41 | 0.452 | robust but not clean-anchor quality |

当前裁决：

- MoLingo-style FullRF backbone 不是单独的解决方案；clean/noisy 分裂仍存在。
- `stage2_molingo_fullrf_h2c_v64_p2b_20260703` 是当前最好的 clean/noisy Pareto checkpoint，可以作为下一轮 ablation/qualitative 候选。
- 不能宣称 robust generated-source camera control 已解决，因为当前仍是 Gaussian noisy source，而不是真实 Stage1 generated replay。
- 下一步最短证据链应补 `generated_replay` 输入与固定 replay cache；如果 p2b 在 replay 上也保住 clean/noisy，才考虑把 FullRF+p2b 升为主线。

## CondMDI / MoLingo 适配裁决 2026-07-03

需要区分两层：

1. **扩散 / Rectified Flow 训练目标与 sampler 层**可以做成可替换模块。CondMDI 当前使用 DDPM/DDIM 风格 `START_X` 预测与 beta schedule；MoLingo FullRF 使用线性插值和速度场预测。它们共享的接口应是：给定 `model(x_t, t, condition)`，返回目标参数化，然后由 process 模块负责 `loss()` 与 `sample()`。
2. **Stage2 非对称任务 contract 层**不能只靠替换 backbone 自动迁移。H2C、JOINT、C2H 的 observed branch、mask/clamp、source metadata、generated replay schedule、relation/projection feature 都会改变模型输入语义。CondMDI 与 MoLingo/RF 应各自落实这个 contract，而不是把 MoLingo 当作 CondMDI 的无脑 drop-in。

因此工程路线是：

- 先把 `diffusion` / `rf` process 抽成可替换模块，保证 clean CondMDI Stage2 能在同一训练脚本里切到 RF loss/sampler。
- 再分别实现 CondMDI-asymmetric 与 MoLingo-asymmetric 的 source-condition-target contract；二者可以复用数据、eval、metadata、replay cache，但不能假设一个 checkpoint 或一套输入拼接能直接兼容另一套 backbone。
- 下一轮 clean `condmdi stage2 + rf` 训练只应验证“RF process 是否可替换且不破坏 clean anchor”，不能直接等价为“非对称架构已完成”。

### Modularization Implementation Status

已完成本地实现：

- `linkedCodebases/StoryMotion/storymotion/stage2/processes.py`
  - `CondMDIDiffusionProcess`: 保持旧 CondMDI/DDIM `START_X` 训练目标与 beta schedule。
  - `RectifiedFlowProcess`: 使用线性插值 `x_t = (1-t) noise + t x0` 与 velocity target `x0 - noise`。
  - `build_stage2_process`: 统一 process factory。
- `linkedCodebases/StoryMotion/scripts/train_stage2_condmdi_pulp.py`
  - 新增 `--generative-process diffusion|rectified_flow`，默认 `diffusion`，旧 checkpoint/eval 默认不变。
  - `diffusion_loss` / `evaluate` 通过 process 接口选择 `q_sample`、`model_t`、training target。
- `linkedCodebases/StoryMotion/scripts/storymotion_official_full_eval.py`
  - 旧 diffusion checkpoint 仍走原 DDIM START_X sampler。
  - RF checkpoint 走独立 Euler velocity sampler，并在 output JSON 写入 `stage2_process`。
- `linkedCodebases/StoryMotion/scripts/storymotion_official_bridge_smoke.py`
  - 从 `meta.args.generative_process` 或 `meta.stage2_process.generative_process` 恢复 process。

本地验证：

- `python3 -m py_compile` 通过：process module、train script、bridge smoke、official full eval、Gradio render script。
- fake model 语义 smoke 通过：`diffusion_loss:diffusion`、`diffusion_loss:rectified_flow`、`sample_rectified_flow`。

限制：

- DeepSeek MCP 按 `deepseek-reasoner` / `deepseek-chat`、`reasoning_effort=max` 连续三次返回空响应；本轮没有得到可引用的 DeepSeek 审查内容。该事实不能写成“DeepSeek 已确认正确”。
- 4090 v7.2 joint fair-bs64 eval 因 OOM 停止，partial / bs32 无效文件已清理；有效 v7.2 E2/E3/E4/E6 joint evidence 改用 5090 已完成的 fair-bs64 JSON。

### Clean CondMDI Stage2 + RF Training Status

远端：`5090:/data/public/ripemangobox/Motion/StoryMotion`

```text
run_dir: runs/train/stage2/condmdi_stage2_rf_clean_20260703
log: logs/train_rf_20260703/condmdi_stage2_rf_clean_20260703.log
gpu: 5090 GPU0
cache: runs/train/stage2/pulp_official_full_mixed_20260611/cache_mixed_full_nw0_20260611_2110
steps: 82688
batch_size: 512
task_probs: 1 / 1 / 1
generative_process: rectified_flow
prediction_type: VELOCITY
```

启动前检查：

- `py_compile` passed for modular process, train script, bridge smoke, and full eval scripts on 5090.
- RF `check` passed on real cache: finite loss and output shape `[4, 192, 75]`.

启动后健康：

- process alive on 5090 GPU0.
- GPU0 memory about `9.2GB / 32.6GB`, utilization about `91%`.
- `step=1` train/eval/test records written; `step=100` train record written.
