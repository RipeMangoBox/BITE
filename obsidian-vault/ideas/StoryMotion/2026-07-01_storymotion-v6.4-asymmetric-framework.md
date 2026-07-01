---
title: "StoryMotion v6.4 非对称 Stage2 框架"
status: active
tags:
  - StoryMotion
  - Motion_Generation
  - experiment
  - status/active
aliases:
  - StoryMotion-v6.4-asym
hypothesis: |
  StoryMotion Stage2 不应继续套用 CondMDI 式对称随机 mask。更合适的框架是 human-first、camera-conditioned、source/reliability-aware 的非对称生成：human branch 提供动作与 root 条件，camera branch 生成 framing / camera residual，并显式区分 GT、noisy、generated 与 missing human source。
source_papers:
  - "[[analysis/ICLR_2026/Pulp_Motion_Framing_aware_multimodal_camera_and_human_motion_generation]]"
  - "[[analysis/CVPR_2026/Towards_Storytelling_Animations_Joint_Synthesis_of_Human_and_Camera_Motions]]"
  - "[[analysis/SIGGRAPH_2024/Flexible_Motion_In_betweening_with_Diffusion_Models_CondMDI]]"
  - "[[analysis/ICCV_2025/MotionLab_Unified_Human_Motion_Generation_and_Editing_via_the_Motion_Condition_Motion_Paradigm]]"
created: 2026-07-01T17:58:00+0800
updated: 2026-07-01T17:58:00+0800
---
# StoryMotion v6.4 非对称 Stage2 框架

## 0. 裁决

当前 Stage2 的问题不是“mask 还不够随机”，而是任务结构被错误对称化。

CondMDI 的合理前提是：同一个人体 motion 序列中任意关节 / 任意关键帧都可能被观测，目标是从对称 partial observation 中补全同一类 motion。StoryMotion 的真实结构不同：

```text
story / text -> human action / root / timing -> camera framing / camera residual
```

camera 依赖 human 是建模事实，不是污染；真正需要避免的是 camera 噪声反向污染 human，以及把 GT human、noisy human、generated human 当作同一种 clean observed branch。

因此 v6.4 不再把 `TASK_CAMERA`、`TASK_HUMAN`、`TASK_JOINT` 当作同权三模式随机训练。最低可验证框架改为：

```text
human prior: text -> human
camera specialist: camera text + human source + reliability tag -> camera
joint generation: human prior first, then camera specialist
```

## 1. 设计依据

[Pulp Motion(ICLR_2026)](../../analysis/ICLR_2026/Pulp_Motion_Framing_aware_multimodal_camera_and_human_motion_generation.md) 说明 human-camera 的关键不是 raw latent share-all，而是 on-screen framing relation subspace。其 `W` row-space / auxiliary sampling 提示我们应该显式建模 framing control 面。

[Towards Storytelling Animations(CVPR_2026)](../../analysis/CVPR_2026/Towards_Storytelling_Animations_Joint_Synthesis_of_Human_and_Camera_Motions.md) 把 character 与 camera 视为独立实体，并显式建模 pairwise interaction。这支持 entity / relation routing，而不是把 human 与 camera 拼成一个普通 latent 后完全共享 UNet 通道。

[CondMDI(SIGGRAPH_2024)](../../analysis/SIGGRAPH_2024/Flexible_Motion_In_betweening_with_Diffusion_Models_CondMDI.md) 的核心是训练时随机 keyframe / joint mask。这个思路可以解释 observed mask 输入的来源，但不能直接迁移到 StoryMotion 的语义分支级不对称任务。

[MotionLab(ICCV_2025)](../../analysis/ICCV_2025/MotionLab_Unified_Human_Motion_Generation_and_Editing_via_the_Motion_Condition_Motion_Paradigm.md) 的重要启发不是立刻换 RF，而是多任务统一需要 task instruction / curriculum；直接混训复杂任务会出现冲突。

## 2. 框架定义

### 2.1 变量契约

- `H`: human latent，包含动作、root、timing，是 camera 的主要结构条件。
- `C`: camera latent，包含 camera trajectory / relative distance / framing residual。
- `R`: relation / framing control 面，第一阶段可以用 Pulp `W` row-space 或 screen projection surrogate 近似。
- `S`: source/reliability tag，区分 `gt`、`noisy_gt`、`generated`、`missing`。

### 2.2 非对称信息流

```text
human branch:
  text_human -> H
  不读取 camera latent 作为主条件

camera branch:
  text_camera + H + S -> C
  允许读取 human/root/framing feature
  不把 H 当作永远 clean 的 hard replacement

joint inference:
  H_hat = human_prior(text_human)
  C_hat = camera_specialist(text_camera, H_hat, source=generated, quality=q)
```

这意味着 `human completion from camera` 不再是主任务的镜像版本。它可以保留为 diagnostic，但不应和 `camera completion from human` 一起混成三模式训练主目标。

## 3. 第一版可跑实验

为避免先做大改架构，v6.4 第一版直接使用已有 Stage2 代码中的 P2b reliability path，训练 camera specialist：

| item | setting |
| --- | --- |
| remote | 4090 server |
| GPU | `CUDA_VISIBLE_DEVICES=1` |
| tmux | `v64_asym_cam_p2b_gpu1_20260701` |
| cache | `runs/train/stage2/pulp_official_full_mixed_20260611/cache_mixed_full_nw0_20260611_2110` |
| output | `runs/train/stage2/v6_4_asym_human_to_camera_p2b_20260701/camera_p2b_b512_gpu1` |
| task probs | `[1, 0, 0]` camera-only |
| text dropout | global `0.1`, camera half `0.1`, human half `1.0` |
| reliability | P2b enabled, prob `0.7`, noise `0/0.05/0.10/0.15/0.30`, missing `0.1` |
| steps | `50000`, batch `512`, EMA `0.999` |

启动命令摘要：

```bash
CUDA_VISIBLE_DEVICES=1 python scripts/train_stage2_condmdi_pulp.py train \
  --cache-dir runs/train/stage2/pulp_official_full_mixed_20260611/cache_mixed_full_nw0_20260611_2110 \
  --output-dir runs/train/stage2/v6_4_asym_human_to_camera_p2b_20260701/camera_p2b_b512_gpu1 \
  --task-probs 1 0 0 \
  --cond-mask-prob 0.1 --cond-mask-prob-cam 0.1 --cond-mask-prob-hum 1.0 \
  --p2b-enable --p2b-prob 0.7 --p2b-noise-levels 0.0 0.05 0.10 0.15 0.30 \
  --p2b-missing-prob 0.1 --ema-decay 0.999
```

Step 1 sanity:

- GPU1 memory about `9.5GB`.
- train `loss_camera = 0.6921`.
- `p2b_selected_frac = 0.7090`.
- `p2b_noisy_frac = 0.6348`.
- `p2b_missing_frac = 0.0742`.

## 4. 成功判据

第一版不看 human / joint 的 teacher loss，因为它们不是训练目标。必须用 camera reliability protocol 判定：

| gate | target |
| --- | --- |
| clean camera completion | 不显著劣于 v6.2 clean `FDCLaTr 14.50 / F1 0.638` |
| P2a noise `0.15` | 明显低于旧 `FDCLaTr 96.87` |
| P2a noise `0.30` | 明显低于旧 `FDCLaTr 216.79` |
| generated-human replay | 不再接近 E.T. replay collapse `FDCLaTr 92.24 / F1 0.375` |
| text dependence | camera text drop / shuffle 不应继续接近无影响 |

若 clean 掉得很厉害，说明 reliability corruption 太强或 human text 全 drop 不合理；下一版先降低 `p2b_prob` 或保留部分 human text，而不是回到三模式随机训练。

## 5. 下一版架构改动

若 camera-only P2b 有效，再做真正的 architecture ablation：

1. `camera root residual split`：camera = text-only global prior + human-conditioned root/framing residual。
2. `relation token`：加入 `R` token，承载 Pulp `W` row-space 或 screen framing surrogate。
3. `task adapter/head`：保留共享浅层时序编码，但 human / camera 输出 head 分离。
4. `stop-gradient human condition`：camera 可读 human feature；human path 不从 camera residual 接梯度。
5. `two-pass joint sampler`：human prior -> camera specialist -> optional relation refinement。

只有当这些 ablation 同时改善 clean、P2a 和 replay，才能把 v6.4 写成 StoryMotion 的新 Stage2 方法；否则它只是一个可靠性诊断实验。
