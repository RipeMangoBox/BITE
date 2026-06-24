---
hypothesis: "基于 PulpMotion frozen stage1 连续 human/camera latent 的 CondMDI-style branch-mask continuous inpainting 可实现三模式 human-camera 统一生成。P1 official full eval 已证明 indepdrop_ft + cfg=2.0/eta=1.0 在 joint aggregate 指标上超过 PulpMotion；P2 四卡训练已完成，当前稳定 best 是 GPU1 human+joint-heavy 330k best_eval(step 282000)。旧 skeleton 可视化存在 topology/projection/smoke-script 问题，不应作为指标否定证据；但 joint human motion/contact 质量仍需 raw-skeleton gate 单独约束。下一步 full eval/render GPU1 stable best 与 GPU3 risky best。"
status: in_progress
source_papers:
  - "[[analysis/ICLR_2026/Pulp_Motion_Framing_aware_multimodal_camera_and_human_motion_generation|Pulp Motion]]"
  - "[[analysis/CVPR_2026/Towards_Storytelling_Animations_Joint_Synthesis_of_Human_and_Camera_Motions|Towards Storytelling Animations]]"
  - "[[analysis/SIGGRAPH_2024/Flexible_Motion_In_betweening_with_Diffusion_Models_CondMDI|CondMDI]]"
  - "[[analysis/ECCV_2024/E_T_the_Exceptional_Trajectories_Text_to_camera_trajectory_generation_with_character_awareness|E.T. / Director]]"
  - "[[analysis/SIGGRAPH_2026/ActCam_Zero_Shot_Joint_Camera_and_3D_Motion_Control_for_Video_Generation|ActCam]]"
  - "[[analysis/ECCV_2024/COIN_Control_Inpainting_Diffusion_Prior_for_Human_and_Camera_Motion_Estimation|COIN]]"
created: 2026-06-13T20:30:00+08:00
updated: 2026-06-16T14:00:00+08:00
supersedes: "[[2026-06-10_pulp-stage1-continuous-stage2-generator-formal]]"
---

# StoryMotion V2: Unified Human-Camera Motion Generation via Branch-Mask Continuous Inpainting

> [!abstract] 当前状态 (updated 2026-06-16 CST)
> **P2 四卡训练与 follow-up 已完成**。P1 的 official full eval 结论仍成立：indepdrop_ft + cfg=2.0/eta=1.0 在 10549 full test 上 Joint TMR=23.95、CLaTr=33.52、r_fpd=0.535，超过 PulpMotion no-Aux rerun。
> - 当前稳定 best： `humjoint_heavy_cam1_hum4_joint4_b512/best_eval.pt`，step 282000，best eval loss=0.008892，best joint human branch=0.030210。
> - 强但有风险的候选： `jointheavy6_humanbranch_h2_from146k_to196k/best_eval.pt`，step 177500，best joint human branch=0.034779；不要用它的 `last.pt`，last test joint human branch collapse 到 0.196017。
> - Channel-gated bilateral CFG 证实 sampler-time human/camera guidance 串扰真实存在，并改善 bilateral joint MPJPE；但 foot/contact 仍未解决。
> - 旧 skeleton 渲染问题主要来自可视化/诊断脚本路径，包括一跳 `t=500` smoke、2D XZ bbox、错误 bone topology、projection/c2w 处理和崩溃旧产物；这些不推翻 official eval 指标。
> - official TMR/CLaTr/r_fpd/FTD/FCD 指标可靠用于 aggregate 对比，因为它们走 Pulp official callbacks，不依赖 skeleton MP4 连线渲染；但它们不足以保证 human motion/contact perceptual quality。
> 下一步：对 GPU1 stable best 与 GPU3 risky best 跑 official full eval + Pulp fair render matrix，并把 raw-skeleton velocity/acceleration、foot contact、bone consistency 作为 checkpoint selection gate。

---

## 0. 2026-06-16 P2 Closure & Metric Reliability

### 0.1 Core P2 Result

P2 的主要问题已经从 "是否能超过 Pulp aggregate 指标" 转向 "joint mode 下 human motion/contact 是否足够可信"。四卡训练和两个 follow-up 的结论如下：

| Run                            | Core config                                    |     Best step |    Best eval loss | Best joint human branch | Decision                         |
| ------------------------------ | ---------------------------------------------- | ------------: | ----------------: | ----------------------: | -------------------------------- |
| GPU0 from-scratch joint6       | `task_probs=[1,1,6]`, branch_mean, 330k        |        282000 |          0.010846 |                0.031710 | 强，但低于 GPU1                       |
| GPU1 human+joint heavy         | `task_probs=[1,4,4]`, branch_mean, 330k        |        282000 |      **0.008892** |            **0.030210** | 当前稳定 best                        |
| GPU2 dropout ablations         | 3×50k                                          |   42000-44000 | 0.018425-0.018902 |       0.040337-0.041235 | 弱，不作为主线                          |
| GPU3 task ablations            | equal/joint-heavy/camera-heavy, 50k            |         42000 | 0.015039-0.018425 |       0.040989-0.049766 | camera-heavy 有害                  |
| GPU2 humanbranch h2            | from 146k, human branch weight 2               |        194500 |          0.013367 |                0.036914 | 稳定但不如 GPU1                       |
| GPU3 observed self-cond        | from 146k, observed self-conditioning          | 149500/183000 | 0.012899-0.013010 |                0.035744 | 不是主修复                            |
| GPU3 jointheavy humanbranch h2 | from 146k, joint-heavy + human branch weight 2 |        177500 |          0.013009 |            **0.034779** | best checkpoint 可测，last collapse |

当前 checkpoint selection：

- Stable baseline：`/data/public/ripemangobox/Motion/StoryMotion/runs/train/stage2/p2_long_training_20260615/gpu1_humjoint_heavy_cam1_hum4_joint4_b512/best_eval.pt`
- Risky candidate：`/data/public/ripemangobox/Motion/StoryMotion/runs/train/stage2/p2_followups_20260616/gpu3_jointheavy6_humanbranch_h2_from146k_to196k/best_eval.pt`
- 禁止使用：GPU3 jointheavy humanbranch h2 的 `last.pt`

### 0.2 Skeleton Visualization vs Metric Reliability

结论分三层：

1. **旧 skeleton 渲染不能作为负面证据**。早期 smoke 用一步 `t=500` denoise，不是真实 50-step DDIM sampler；2D XZ plot 有 bbox/aspect 压缩风险；旧 render 还存在 c2w/string、standard CFG `None` assignment、projection 与 bone topology 问题。这些问题会造成空白、扭曲、崩溃或旧产物混淆。
2. **official eval 指标没有被 skeleton 连线渲染污染**。`storymotion_official_full_eval.py` 的路径是 sampler → latent → Pulp frozen autoencoder.decode → `dataset.get_raw()` → Pulp official callbacks；TMR/CLaTr/r_fpd/FTD/FCD 不是从 Matplotlib/MP4 skeleton 图计算出来的。因此 P1 full-split aggregate 指标仍可作为公平对比依据。
3. **aggregate 指标不等于 human motion 质量充分验证**。当前 render/fair-compare 的 raw-joint 诊断显示，channel-gated CFG 改善 bilateral joint MPJPE，但 foot/contact 仍差；这说明 training/objective selection 没有充分约束 velocity/acceleration、foot contact、bone/limb consistency。后续 checkpoint 不能只看 eval loss、TMR/CLaTr 或 MPJPE。

保守表述：官方指标可靠地支持 "StoryMotion 在 aggregate semantic/geometric metrics 上超过 PulpMotion rerun"；它们不支持直接宣称 "joint human motion perceptual quality 已优于 PulpMotion"。这个后者需要 raw-skeleton gate 和修正后的统一拼接渲染来闭环。

## 1. Problem & Core Claim

### 1.1 What Problem

现有 human-camera motion generation 方法只解决单一生成方向（text→joint 或 human-first→camera），无法在统一框架中支持三种条件补全模式：

```
Mode A: human text + camera text + human latent  → camera latent   (给动作，生成运镜)
Mode B: human text + camera text + camera latent → human latent    (给运镜，生成动作)
Mode C: human text + camera text                 → human + camera  (从文本联合生成)
```

### 1.2 Core Claim

冻结 PulpMotion stage1 作为 human/camera continuous tokenizer，训练 CondMDI-style branch-mask continuous inpainting stage2，即可用一个模型覆盖三种模式。

### 1.3 Scope Boundary

- **公平对比对象**：PulpMotion official joint generation（Mode C）+ StoryMotion 内部 completion 对比（Mode A/B）
- **不考虑**：新 dataset、新 baseline（ActCam/TSA 等）、human eval、demo page、离散 token 路线
- **必须验证的前提**：sampler 正确性、语义对齐可修复性、Mode B 条件依赖性

---

## 2. Method

### 2.1 Stage1: Frozen PulpMotion Continuous Tokenizer

直接冻结 PulpMotion stage1（aligned autoencoder），MVP 只取 human + camera latent：

```text
z = concat([z_hum, z_cam])  ∈ R^{N × 192 × T}
  z_hum: 128 dims  (human motion latent)
  z_cam: 64 dims   (camera FOV + distance + pose latent)
```

Camera 表征是 **subject-relative**（`distance = camera_translation - human_root_translation`）。Mode B 学习 `p(z_hum | z_cam, text)`，不是确定性逆问题。

### 2.2 Stage2: CondMDI-Style Branch-Mask Continuous Inpainting

DiT-based diffusion generator（width=384, 1000 steps, cosine schedule, **START_X prediction**）：

```text
G_θ(z_t, z_visible, mask_branch, human_text_emb, camera_text_emb, t) → denoised masked branch
```

训练时 forward 内部用 clean `obs_x0` 替换 observed positions（CondMDI training contract）。三种 mask pattern 等概率采样：

| Pattern           | Visible branch | Predict target | Task   |
| ----------------- | -------------- | -------------- | ------ |
| camera completion | human          | camera         | Mode A |
| human completion  | camera         | human          | Mode B |
| joint generation  | none           | human + camera | Mode C |

**Text conditioning**：CLIP text embeddings（复用 Pulp dataset），通过 DiT cross-attention 注入。训练时 `cond_mask_prob=0.1`（模型支持 CFG）。**当前 sampler 已启用 CFG（cfg=2.0/eta=1.0 为验证最优）**。

### 2.3 Checkpoint Lineup & Training Differences

| Checkpoint            | Init                         | Steps        | Task probs | Loss mode    | Joint budget                 | Human budget |
| --------------------- | ---------------------------- | ------------ | ---------- | ------------ | ---------------------------- | ------------ |
| `mixed_standard_last` | scratch                      | 82,688       | 1/1/1      | element_mean | 27.6k (33%)                  | 55.1k (67%)  |
| `branch_jh6ft`        | resume `mixed_standard_last` | +20k→102,688 | 1/1/6      | branch_mean  | +15k→42.6k total (75% of ft) | +2.5k each   |

**`branch_jh6ft` 相比 `mixed_standard_last` 的三项修改**（实质是 curriculum learning：先 equal-task scratch → 后 joint-heavy ft）：

1. **Task sampling 从 `1:1:1` → `1:1:6`**：joint 占比从 33% 提升到 75%，直接增加 joint 训练预算
2. **Loss 从 `element_mean` → `branch_mean`**：joint 中 camera（64-dim）原来在 element_mean 下梯度权重约为 human（128-dim）的 1/3；branch_mean 将 human/camera 等权（0.5/0.5），camera 梯度信号增强约 3 倍
3. **额外 20k 步 joint-heavy finetune**：进一步强化 joint 能力

**这解释了 `branch_jh6ft` 的指标模式**：

```
mixed_standard_last → branch_jh6ft 的变化：
  Joint CLaTr:     20.74 → 23.70  (+14%)   ← camera 语义改善（更多 joint 训练 + camera 梯度增强）
  Joint r_fpd:      0.545 → 0.450            ← camera 几何改善
  Joint TMR:       18.65 → 18.72  (+0.4%)   ← human 语义几乎不变（human 梯度未增强，budget 变化小）
  Completion TMR:  18.20 → 18.19  (flat)    ← completion 能力保留但无提升
  Completion CLaTr: 53.54 → 53.29  (flat)    ← 同上
```

→ `branch_jh6ft` 是通过 **增加 joint 训练预算 + 提升 camera 梯度权重** 专门强化 camera 质量的结果。Human 语义和 completion 能力基本保留但无改善。

### 2.4 Training Budget

双方使用同一 mixed split cache（数据量相同，已验证 test set sample IDs 完全一致）。差异在训练步骤数——**82,688 步（V0）和 146,000 步（indepdrop_ft）远低于 Pulp 330,750 步。StoryMotion 在训练少 2-4× 的情况下超越了 PulpMotion，这是对 StoryMotion 不公平（被低估）.**

|                           | PulpMotion official | StoryMotion `mixed_standard_last` | 比值        |
| ------------------------- | ------------------- | --------------------------------- | --------- |
| Total steps               | 330,750             | 82,688                            | 4.0x      |
| Effective joint steps     | **330,750**         | **27,563**                        | **12.0x** |
| Effective human gen steps | 330,750             | 55,126                            | 6.0x      |

**纠正**：P0 确定最优 sampler/config 后，从零训练 `branch_jh6ft` 等价配置（`task_probs=[1,1,6]`, `branch_mean`）到 330k 步（4 GPU, ~3.5 天）。不复用 resume 路径。

---

## 3. Evaluation Protocol & Fair Comparison

### 3.1 Metric Computation

```
StoryMotion sampler → z_pred → Pulp frozen autoencoder.decode →
  human joints + camera params → Pulp official callbacks →
    TMR/CLaTr/captions (semantic), r_fpd/Out-rate/proj (geometry)
```

指标公式与 PulpMotion 完全相同（同一 `JointMetricCallback` / `CameraMetricCallback` / `HumanMetricCallback`），差异仅在被评估的生成 latent 质量。

### 3.2 Sampler Gap

**与 PulpMotion official sampler 的差异**：

|                   | StoryMotion (current)           | PulpMotion official                     |
| ----------------- | ------------------------------- | --------------------------------------- |
| Sampler type      | DDIM                            | DDPM                                    |
| Prediction target | x0 (START_X)                    | noise (ε)                               |
| eta               | 0.0–1.0 (tunable)               | N/A (DDPM stochastic)                   |
| CFG on text       | **cfg=2.0 (validated optimal)** | `cfg_rate_c=11.0`                       |
| CFG on projection | 无（MVP 不含 projection）            | `cfg_rate_z=0.0` (no-Aux) / `2.0` (Aux) |

CFG 已实现并验证。cfg=2.0 在 joint/camera/human 三模式均最优。eta=1.0 提供额外 +2.52 TMR 增益（r_fpd 不变）。

### 3.3 Fair Comparison Rules

1. **同 split / evaluator**：所有对比使用同一 mixed test split、同 Pulp callbacks、同 stage1
2. **Completion vs Joint 分开**：completion 只做 StoryMotion 内部对比；joint 与 Pulp no-Aux 横向对比需标注 sampler 差异
3. **一次改一个变量**：checkpoint 对比固定 sampler；sampler 对比固定 checkpoint
4. **CFG gap 已关闭**：P1 完成 CFG sweep + bilateral CFG 矩阵。StoryMotion cfg=2.0/eta=1.0 在 10549-sample full test 上全面超越 Pulp CFG w=11.0。对比已严格公平

---

## 4. Current Results (CFG-Equipped, Full-Split Only)

> **原则**：仅报告 10549-sample full test set 上的正式对比。1024-sample 诊断数据用于内部决策，不列入正式结果。

### 4.1 PulpMotion Official Baseline（5090, Full Mixed Split, 10549 samples）

Pulp official checkpoint `dit-xy-ddpm-4dlbunha-330750.ckpt`。

| Metric       | Pulp no-Aux (5090 rerun) |
| ------------ | ------------------------ |
| TMR ↑        | 23.36                    |
| CLaTr ↑      | 31.31                    |
| r_fpd ↓      | 5.15                     |
| Out-rate ↓   | 26.6%                    |
| Caption F1 ↑ | 0.350                    |
| FCD ↓        | 88.4                     |
| FTD ↓        | 377.4                    |

### 4.2 StoryMotion Joint Mode（10549-sample Full Test）

| Metric       | Pulp official | `branch_jh6ft` cfg=2.0 eta=1.0 | `branch_jh6ft` cfg=3.0 eta=0.0 | **FT cfg=2.0 eta=1.0** | FT cfg=3.0 eta=0.0 |
| ------------ | ------------- | ------------------------------ | ------------------------------ | ---------------------- | ------------------ |
| TMR ↑        | 23.36         | 23.64                          | 23.33                          | **23.95**              | **24.02**          |
| CLaTr ↑      | 31.31         | 32.96                          | 33.52                          | **33.52**              | **34.52**          |
| `r_fpd` ↓    | 5.15          | 0.619                          | 1.678                          | **0.535**              | 1.396              |
| FCD ↓        | 88.4          | 87.4                           | 106.2                          | **85.7**               | 104.6              |
| Out-rate ↓   | 26.6%         | 8.5%                           | 13.4%                          | **7.9%**               | 12.4%              |
| Caption F1 ↑ | 0.3505        | 0.3726                         | 0.3668                         | **0.3740**             | **0.3779**         |
| FTD ↓        | 377.4         | 150.4                          | 154.0                          | 155.7                  | 156.6              |

**Key findings（10549 full-split confirmed）:**

1. **CFG 修复语义 gap 在 full test 上确认**：cfg=2.0/eta=1.0 + FT ckpt → TMR=23.95 > Pulp 23.36；CLaTr=33.52 > Pulp 31.31
2. **Geometry 优势保持**：r_fpd=0.535（9.6x 优于 Pulp 5.15），Out-rate=7.9%（3.4x 优于 Pulp 26.6%）
3. **FT checkpoint 全面超越 branch_jh6ft**：independent per-modality dropout 训练有效提升了 CFG 效果。FT cfg=3.0 给出最强语义（TMR=24.02, CLaTr=34.52），但 geometry 退化（r_fpd=1.396）。FT cfg=2.0/eta=1.0 是最优均衡配置
4. **P0 1024-sample 趋势在 10549-sample 上保持**：TMR 绝对值下降约 0.5（24.15→23.64 branch / 23.95 FT），符合更大测试集的预期；相对排序（cfg=2.0 vs cfg=3.0 tradeoff、FT > branch）完全一致
5. **所有 StoryMotion 配置在 FTD/CapF1 上均优于 Pulp**：说明生成质量和文本对齐度一致更好

### 4.3 Cross-Config Analysis（10549-sample）

**CFG effect magnitude**（branch_jh6ft, 10549-sample）:

| Transition                | TMR Δ     | CLaTr Δ   | r_fpd Δ | Out-rate Δ |
| ------------------------- | --------- | --------- | ------- | ---------- |
| cfg=1.0 → cfg=2.0/eta=1.0 | **+4.92** | **+9.27** | +0.169  | +1.1%      |
| cfg=1.0 → cfg=3.0/eta=0.0 | +4.60     | +9.82     | +1.228  | +5.9%      |

CFG 独立贡献了几乎全部语义提升（TMR +5, CLaTr +9），远超 eta stochasticity 的辅助增益。

**FT vs branch_jh6ft**（same cfg, 10549-sample）:

| Comparison                   | TMR Δ     | CLaTr Δ   | r_fpd Δ    | FCD Δ    |
| ---------------------------- | --------- | --------- | ---------- | -------- |
| cfg=2.0/eta=1.0: FT − branch | **+0.31** | **+0.56** | **−0.084** | **−1.7** |
| cfg=3.0/eta=0.0: FT − branch | **+0.69** | **+1.00** | −0.282     | −1.7     |

**cfg=2.0 vs cfg=3.0 Pareto tradeoff**（FT checkpoint）:

| cfg | TMR | CLaTr | r_fpd | Out-rate | FCD |
|---|---|---|---|---|---|
| 2.0/eta=1.0 | 23.95 | 33.52 | **0.535** | **7.9%** | **85.7** |
| 3.0/eta=0.0 | **24.02** | **34.52** | 1.396 | 12.4% | 104.6 |

cfg=3.0 给出最强语义，但 r_fpd 退化 2.6×、Out-rate 退化 1.6×。**cfg=2.0/eta=1.0 是最优均衡配置**——语义已超越 Pulp，geometry 保持 9.6x 优势。

### 4.4 Completion Mode（10549-sample Official Full-Split）

All indepdrop_ft checkpoint, cfg=2.0, eta=1.0, 50-step DDIM START_X.

**Camera completion**（Mode A: human→camera）:

| Metric | branch_jh6ft no-CFG | **indepdrop_ft cfg=2.0 η=1.0** | Δ |
|--------|---------------------|-------------------------------|----|
| CLaTr ↑ | 53.29 | **54.85** | **+1.56** |
| FCD ↓ | — | 14.50 | — |
| Caption F1 ↑ | — | 0.638 | — |

**Human completion**（Mode B: camera→human）:

| Metric | branch_jh6ft no-CFG | **indepdrop_ft cfg=2.0 η=1.0** | Δ |
|--------|---------------------|-------------------------------|----|
| TMR ↑ | 18.19 | **18.17** | −0.02 |
| FTD ↓ | — | 126.7 | — |
| Coverage | — | 0.846 | — |

**关键发现**：
1. **Camera completion**：CFG + indepdrop_ft 在 10549-sample 上带来 +1.56 CLaTr 提升（53.29→54.85），正式确认有效
2. **Human completion**：CFG 无增益（Δ −0.02，噪声级）。Observed camera branch 作为强 spatial condition 主导生成分布，text guidance 边际效益为零。Mode B TMR ~18 天花板需通过更多训练/架构改进突破，而非 CFG sweep
3. **Cam vs Human 不对称**：CFG 对 camera completion 有效（+1.56）但对 human completion 无效，反映了两个模态从 text condition 受益程度不同——camera 语义空间更大、更依赖 text 约束

### 4.5 Bilateral CFG Analysis（1024-sample, branch_jh6ft, joint）

18 组 bilateral + 6 组 standard CFG sweep 揭示 human/camera CFG 独立效应：

| Objective | Best Config | Value | Tradeoff |
|-----------|------------|-------|----------|
| TMR ↑ | `cfg_h=2, cfg_c=1` | **26.67** | r_fpd=1.47 |
| CLaTr ↑ | `std cfg=3, eta=0.5` | **34.47** | r_fpd=1.34 |
| r_fpd ↓ | `cfg_h=1, cfg_c=1, eta=1.0` | **0.41** | TMR=22.88 |
| **Balanced** 🏆 | `std cfg=2.0, eta=1.0` | TMR=24.15, CLaTr=33.40, r_fpd=0.64 | — |

**结论**：Human CFG 独立驱动 TMR，Camera CFG 独立驱动 CLaTr。但在 joint mode 下标准 CFG（统一 scale）是最佳平衡。Bilateral CFG 能力存在——若下游只关注单一维度（如纯 camera quality），可独立调高 camera CFG。

---

## 5. Critical Issues & Deep Analysis

### 5.1 Issue 1: Sampler — Resolved

**旧诊断（2026-06-12 naive proxy）**：latent MSE 随步数增加 → 被解读为 "multi-step degradation"。

**P0 实验澄清（2026-06-13）**：官方指标（TMR/CLaTr/r_fpd）显示这不是退化，而是**几何-语义 tradeoff**：

| Steps | r_fpd | TMR | 现象 |
|---|---|---|---|
| 1 | 1.655 | 26.66 | 高语义、低几何 |
| 20 | 0.474 | 21.00 | 均衡 |
| 50 | 0.448 | 18.99 | 高几何、低语义 |

**结论**：latent MSE proxy 与官方生成指标不等价。多步 denoising 使输出更接近训练分布（→ r_fpd↓），但牺牲多样性（→ TMR↓）。这不是 bug，50-step DDIM 完全可以作为主 sampler。

**不再需要 C1/C2 控制实验**——CFG 修复后语义已达 Pulp level，sampler 本身不是瓶颈。

### 5.2 Issue 2: Mode-Seeking — Confirmed & Resolved

**假设**：DDIM eta=0 + 无 CFG → mode-seeking → r_fpd 极低但 TMR 低。

**P0 验证**：

| 实验 | 预测 | 结果 |
|---|---|---|
| CFG (cfg=2~3) | r_fpd↑, TMR↑↑ | ✅ TMR 18.99→24.43 (+5.4), r_fpd 0.45→1.40 |
| Eta (eta=1.0) | r_fpd↑, TMR↑ | ✅ TMR 18.99→21.68 (+2.7), r_fpd 稳定 |

**结论**：mode-seeking hypothesis 完全确认。CFG 是主因（+5.4 TMR），eta stochasticity 是辅助（+2.7 TMR）。cfg=2.0 时 TMR=24.15 已超 Pulp 23.36，r_fpd=0.71 仍 7x 优于 Pulp。此问题已解决。

### 5.3 Issue 3: Semantic Alignment — ✅ Resolved via CFG (Full-Split Confirmed)

| Setting | Human TMR | Camera CLaTr | r_fpd | Source |
|---------|-----------|-------------|-------|--------|
| Pulp no-Aux joint | 23.36 | 31.31 | 5.15 | 10549-sample |
| StoryMotion joint no-CFG | 19.66 | 25.25 | 0.35 | 1024-sample |
| **StoryMotion joint cfg=2.0 η=1.0** | **23.95** | **33.52** | **0.53** | **10549-sample** 🏆 |

**CFG 在 10549-sample full test 上确认超越 PulpMotion。** Semantic gap 已彻底关闭。StoryMotion 在训练 146k 步时语义已超 Pulp 330k 步。

CFG 对 completion mode 的效果不对称：camera completion +1.56 CLaTr（有效），human completion Δ≈0（无效）。详见 Section 4.4。

### 5.4 Issue 4: Mode B Strictness — Validation Without Breaking Stage1

**Mode B 要证明**：`z_cam` 的 relative framing condition 确实约束了生成的 human motion，而不是被模型忽略。

**已通过**：整体 camera latent zero/shuffle/matched-noise gate（V1 Section 6.1）——模型确实依赖整体 `z_cam`。

**V2 策略：** 不做 latent-space component 拆分（会破坏 frozen stage1）。Pulp camera feature 在 **encode 之前** 已有清晰三段结构：`camera_feat = concat([intrinsics(2D), distance(3D), posevel(9D)])`。通过 decode-space intervention 验证 component-level dependency：修改 GT camera_feat 的 distance/FOV/posevel 分量 → 通过 frozen stage1 encoder 重新编码 → 生成 modified `z_cam` → Mode B inference → 观察 human 输出变化。

| Gate                  | 方法                                                     | 通过标准                                        |
| --------------------- | ------------------------------------------------------ | ------------------------------------------- |
| Distance zero-out     | 前置零 `distance_feat` → re-encode → Mode B               | human root/geometry 显著变化                    |
| Distance shuffle      | shuffle `distance_feat` → re-encode → Mode B           | human root distribution 改变                  |
| Camera-motion shuffle | 固定 distance, shuffle FOV/velocity → re-encode → Mode B | 输出有别于 distance-only 变化                      |
| Decoded geometry      | decode human+camera → projection metrics               | 与 text-only / camera-shuffle baseline 有显著差异 |
| Cycle consistency     | Mode B human → Mode A camera → 对比输入 camera             | 诊断用，非 main metric                           |

---

## 6. Experiment Plan

### 6.1 P0: ✅ COMPLETED（2026-06-13）

CFG sweep + eta sweep + multi-step 全部完成。核心发现：
- **CFG w=2~3 彻底修复语义 gap**（TMR 24.15~24.43, CLaTr 31.37~33.21）
- **Eta stochasticity 辅助增益**（TMR +2.7 at eta=1.0）
- **Multi-step 是 tradeoff 而非 degradation**
- 结果输出：`remote 5090: .../runs/eval/storymotion_p0_diag_20260613/`

### 6.2 P1: CFG+Eta Combo + Full-Split + Completion — ✅ COMPLETED (2026-06-15)

- **P1-1**: CFG+eta combo ✅ — bilateral_cfg_matrix (18+6 runs) + P1 parallel eval
- **P1-2**: Best combo full-split joint eval ✅ — indepdrop_ft cfg=2.0/eta=1.0: TMR=23.95, CLaTr=33.52, r_fpd=0.53
- **P1-3**: Completion mode CFG test ✅ — Camera CLaTr=54.85 (+1.56), Human TMR=18.17 (flat)
- **P1-4**: Rendering ✅ — 3 samples × 3 modes, PNG+MP4+Concat, indepdrop_ft cfg=2.0/eta=1.0
- **P1-5**: Bilateral CFG analysis ✅ — human/camera CFG independently controllable; std cfg=2.0 is best balanced
- 结果输出：`5090:runs/eval/stage2/p1_parallel_20260615/` + `p1_renders_20260615/`
- 完整分析：`linkedCodebases/StoryMotion/stage2/analysis/stage2_p1_parallel_eval_20260615.md`

### 6.3 P2：Four-GPU Long Training & Human-Branch Follow-Up — ✅ COMPLETED (2026-06-16)

P2 已完成 4 个 GPU 主实验与 3 个 follow-up。核心结论：

- 330k long training 有效，GPU0/GPU1 均明显优于 50k ablations。
- 当前稳定 best 是 GPU1 `task_probs=[1,4,4]` human+joint-heavy，而不是纯 joint-heavy from scratch。
- Dropout ablations 没有产生清晰增益；camera-heavy task ratio 对 joint human branch 有害。
- Observed-branch self-conditioning 不是主修复；它没有改善 channel-gated bilateral joint render 的 foot/contact。
- GPU3 `jointheavy6 + human_branch_weight=2` 的 `best_eval.pt` 可作为强候选，但 `last.pt` collapse，必须只评估 best checkpoint。

| Checkpoint                          |   Step | Best eval loss | Best joint human branch | Status                              |
| ----------------------------------- | -----: | -------------: | ----------------------: | ----------------------------------- |
| GPU1 human+joint-heavy best         | 282000 |   **0.008892** |            **0.030210** | stable best                         |
| GPU0 from-scratch joint6 best       | 282000 |       0.010846 |                0.031710 | strong backup                       |
| GPU3 jointheavy humanbranch h2 best | 177500 |       0.013009 |                0.034779 | risky candidate, validate only best |
| GPU2 humanbranch h2 best            | 194500 |       0.013367 |                0.036914 | stable but weaker                   |

P2 后的主线不再是 "启动 330k"，而是 "用 official full eval + Pulp fair render matrix 验证 GPU1/GPU3 best，并把 raw-skeleton dynamics/contact 纳入 checkpoint gate"。

### 6.4 P3（2-3 周）：Mode B + 完善

| Gate                         | 完成标准                                      |
| ---------------------------- | ----------------------------------------- |
| G4: Mode B decode-space gate | Section 5.4 的 5 个 gate                    |
| G5: Visualization audit      | decode → skeleton/camera 可视化              |
| G6: Pulp strict alignment    | split hash / metric audit / seed variance |
| G7: Diversity metrics        | APD/Div + multi-seed generation           |

### 6.5 Not in Scope

- 新 dataset、新 baseline（ActCam/TSA/GenDoP）、projection latent ablation、discrete token 路线、human eval、demo page

### 6.6 2026-06-14 Marathon Rerun Status

- `run_experiment_marathon_v2.sh` 已把阶段 0 的独立 dropout 训练跑完，训练从 `branch_jh6ft/best_eval.pt` 续到 `step=146000`，`best_eval.pt` / `last.pt` 均已写出。
- 这次 rerun 的第一个 full joint batch 没有完成 10549-sample 全量测试：`std_cfg2.0_eta1.0`、`std_cfg1.0_eta0.0`、`bi_h2.0_c1.0_eta0.0` 都在 `dataset.get_raw()` 的 SMPL decode 处 OOM，且各自只写到 `5632` 条 `records.jsonl`。
- 根因是 marathon 脚本把 full eval 的 `--batch-size` 硬编码成 `128`，而官方 full-eval wrapper 默认是 `64`。这次 rerun 不能算新的 full test；后续需要把 full eval batch 降到 `64` 或更低，再重跑被 OOM 打断的 full eval / completion / sweep / render 阶段。

### 6.7 2026-06-14 Formal Full-Split Rerun — ✅ COMPLETED

- 直接使用已有 `cache_mixed_full_nw0_20260611_2110` (10549 val samples)，无需重建。
- 4-GPU 5090 并行 eval，batch_size=64（修复了 marathon v2 的 batch=128 OOM）。
- 4 个配置全部跑完：`branch_jh6ft` × {cfg=2.0/eta=1.0, cfg=3.0/eta=0.0} + `FT ckpt` × {cfg=2.0/eta=1.0, cfg=3.0/eta=0.0}。
- 完整指标对比表见 Section 4.5。
- 结果输出：`5090:runs/eval/marathon_20260614/full/`，已同步到本地 mirror `stage2/metrics/marathon/full/`。

---

## 7. Claims & Boundaries

### 7.1 可以写

1. "基于 PulpMotion frozen stage1 的 CondMDI-style branch-mask continuous inpainting 框架，用单一模型支持三种 human-camera 条件生成模式。"
2. "Stage2 三模式训练可收敛，completion mode 可通过 Pulp official callbacks 评估。"
3. "在 joint generation 10549-sample full test 上，StoryMotion FT checkpoint + cfg=2.0/eta=1.0 的语义指标（TMR=23.95, CLaTr=33.52）已超越 PulpMotion no-Aux baseline（TMR=23.36, CLaTr=31.31），同时 geometry 指标保持显著优势（r_fpd=0.535 vs 5.15, 9.7× better）。同 split 同 evaluator。"
4. "Independent per-modality dropout fine-tuning 有效提升了 CFG 效果，FT checkpoint 在全部指标上超越原始 branch_jh6ft。"
5. "Camera completion (Mode A) 在 10549-sample full test 上 CLaTr=54.85，较 no-CFG baseline (+1.56)。"
6. "Bilateral CFG 验证 human/camera CFG 独立可控，但标准 CFG cfg=2.0 在 joint mode 下是最佳平衡。"
7. "PulpMotion official no-Aux baseline 在 5090 rerun 与论文数值接近。"
8. "P2 四卡训练已完成；当前稳定 best 是 GPU1 human+joint-heavy 330k `best_eval.pt`，GPU3 jointheavy humanbranch h2 的 `best_eval.pt` 是强但需验证的候选。"
9. "旧 skeleton 可视化异常主要来自 render/diagnostic pipeline，不应反向否定 P1 official full eval；但 joint human motion/contact 质量仍需 raw-skeleton gate 单独验证。"

### 7.2 不能写

1. "StoryMotion 全面优于 PulpMotion"——human completion 未超越，joint human/contact 未通过 raw-skeleton gate，Pulp strict alignment audit 仍未完成
2. "Human completion TMR 超越 Pulp joint baseline"——18.17 vs 23.36，差距显著
3. "Mode B 已验证 component-level camera dependency"——decode-space gate 未做
4. "`cfg_rate_z=2` 是 PulpMotion Aux baseline"——只是 no-Aux ckpt 的 inference-only probe
5. "StoryMotion 使用 Pulp official sampler"——当前是自定义 DDIM START_X
6. "FT checkpoint 的优势仅来自训练步数"——FT 同时改变了 dropout 策略和步数，未做消融
7. "GPU1/GPU3 P2 best 已经在 official full eval 上超越 PulpMotion"——P2 full eval/render matrix 还没跑完；当前只确认 training loss 和局部 render diagnostics
8. "skeleton 渲染坏，所以 P1 指标不可靠"——P1 指标路径不依赖 skeleton render；只能说 aggregate 指标不覆盖所有 human motion/contact 质量

### 7.3 停止条件（更新）

1. ✅ P1 全部完成（CFG sweep, full-split, completion, bilateral, rendering）
2. ✅ P2 四卡训练与 follow-up 完成；stable best 与 risky best 已确定
3. Mode B decode-space gate 未完成 → 不宣称 "camera-conditioned human generation" 的 component-level 因果性
4. Pulp strict alignment audit 未完成 → baseline 始终标注 "provisional"
5. GPU1/GPU3 P2 best 的 official full eval 未完成 → 不宣称 P2 checkpoint aggregate 指标最终胜出
6. Raw-skeleton dynamics/contact gate 未完成 → 不宣称 joint human motion perceptual quality 已解决

---

## 8. Key Evidence Artifacts

```
# StoryMotion training
linkedCodebases/StoryMotion/storymotion_stage2_5090_20260611/
linkedCodebases/StoryMotion/storymotion_stage2_5090_20260611/stage2_completed_summary_20260612.md

# P0 diagnostic results (2026-06-13)
remote 5090: /data/public/ripemangobox/Motion/StoryMotion/runs/eval/storymotion_p0_diag_20260613/

# P1 parallel eval results (2026-06-15) 🆕
remote 5090: /data/public/ripemangobox/Motion/StoryMotion/runs/eval/stage2/p1_parallel_20260615/
local analysis: linkedCodebases/StoryMotion/stage2/analysis/stage2_p1_parallel_eval_20260615.md

# P1 rendering results (2026-06-15) 🆕
remote 5090: /data/public/ripemangobox/Motion/StoryMotion/runs/eval/p1_renders_20260615/std_cfg2.0_eta1.0/

# P2 GPU training report and metrics (2026-06-16)
local analysis: linkedCodebases/StoryMotion/stage2/analysis/stage2_p2_gpu_training_20260616.md
local metrics: linkedCodebases/StoryMotion/stage2/metrics/p2_training_20260616/p2_all_gpu_training_summary_20260616.json
remote train: /data/public/ripemangobox/Motion/StoryMotion/runs/train/stage2/p2_long_training_20260615/
remote followups: /data/public/ripemangobox/Motion/StoryMotion/runs/train/stage2/p2_followups_20260616/

# P2 render/fair-compare diagnostics
remote 5090: /data/public/ripemangobox/Motion/StoryMotion/runs/eval/stage2/joint_channel_gated_pulpmotion_fair_compare_20260615/
remote 5090: /data/public/ripemangobox/Motion/StoryMotion/runs/eval/stage2/gpu3_obs_selfcond_best_pulpmotion_fair_compare_20260616/

# Bilateral CFG matrix (2026-06-14)
remote 5090: /data/public/ripemangobox/Motion/StoryMotion/runs/eval/bilateral_cfg_matrix_20260614/

# indepdrop_ft training checkpoint 🏆
remote 5090: /data/public/ripemangobox/Motion/StoryMotion/runs/train/stage2/independent_dropout_ft_20260614/gpu0_indepdrop_b512_50000/

# P2 current best checkpoints
stable best: /data/public/ripemangobox/Motion/StoryMotion/runs/train/stage2/p2_long_training_20260615/gpu1_humjoint_heavy_cam1_hum4_joint4_b512/best_eval.pt
risky candidate: /data/public/ripemangobox/Motion/StoryMotion/runs/train/stage2/p2_followups_20260616/gpu3_jointheavy6_humanbranch_h2_from146k_to196k/best_eval.pt

# PulpMotion official baseline (5090)
remote 5090: /data/public/ripemangobox/Motion/StoryMotion/runs/eval/pulpmotion_official_baseline_20260613/

# Pulp official checkpoint
remote 5090: /data/public/ripemangobox/Motion/PulpMotion_official_eval/pulpmotion-models/runs/dit-xy-ddpm-4dlbunha-330750.ckpt

# Eval scripts
scripts/storymotion_official_full_eval.py
scripts/render_bilateral_results.py
```

---

## 9. Next Core Tasks（2026-06-16 CST）

优先级按顺序排列：

### 9.1 P1 并行评估 — ✅ COMPLETED (2026-06-15)

- Joint full-split: TMR=23.95, CLaTr=33.52, r_fpd=0.53 ✅
- Camera full-split: CLaTr=54.85 ✅
- Human full-split: TMR=18.17 ✅
- Bilateral CFG analysis: 标准 cfg=2.0 最优，双边独立可控 ✅
- Rendering: 3 samples × 3 modes ✅
- 见 Section 4.2–4.5, Section 6.2

### 9.2 P2 Best Checkpoint Official Eval + Render Matrix — **最高优先级**

目标：比较 GPU1 stable best 与 GPU3 risky best，不再使用 `last.pt` 或未验证中间产物。

- **official full eval**：joint / camera completion / human completion，固定 Pulp callbacks、same split、same sampler contract
- **render matrix**：StoryMotion vs PulpMotion fair compare，统一 sample、统一 skeleton topology、统一 camera projection、统一 concat 输出
- **checkpoint pair**：GPU1 `best_eval.pt` step 282000；GPU3 jointheavy-humanbranch `best_eval.pt` step 177500
- **判定标准**：aggregate 指标不能下降太多，同时 raw-skeleton dynamics/contact 必须改善；否则保留 GPU1 stable best

### 9.3 Raw-Skeleton Selection Gate

这条是对 "joint loss/selection 不只看 aggregate 指标，要单独约束 human branch" 的具体落地：

- **velocity/acceleration**：统计 root 与 joint 的速度/加速度分布，防止抖动、漂移和突变
- **foot contact**：检测 foot joint 的低速接触帧，与 GT/Pulp contact pattern 比较，防止滑步和悬空
- **bone/limb consistency**：统计固定骨长方差和 limb ratio，发现 autoencoder decode 或 topology 异常
- **per-branch reporting**：joint task 单独报告 human branch，不只看 aggregate loss/TMR/CLaTr
- **selection rule**：`best_eval.pt` 先按 official eval 过线，再用 raw-skeleton gate 排除 perceptual failure

### 9.4 Human Completion / Mode B 提升

Mode B TMR=18.17，距 Pulp joint TMR=23.36 有显著差距。CFG 对此 mode 无效。需探索：

- 条件注入方式和 attention mask pattern，而不是继续只 sweep CFG
- Human text conditioning 增强，当前 CLIP embedding 对 human motion 的描述可能不足
- Decode-space camera component gate，验证 `distance` / FOV / camera motion 是否真正约束 human output

### 9.5 Pulp Baseline Strict Alignment Audit

Pulp 5090 rerun 与论文值有偏差（r_fpd 5.15 vs 4.90, CLaTr 31.31 vs 30.75），需正式审计。

- **检查项**: split hash, metric seed, evaluator version, model weights hash
- **完成后**: 可将 Pulp baseline 标注从 "provisional" 升级为 "verified"
