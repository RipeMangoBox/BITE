---
title: "StoryMotion Stage1 and Stage2 Loss Contract and Demanifold Diagnosis"
status: active
hypothesis: |
  StoryMotion Stage2 demanifold is caused by an interaction between local tokenizer geometry and a latent-only START_X MSE objective that does not constrain decoder-sensitive motion directions.
tags:
  - StoryMotion
  - Motion_Generation
  - loss
  - stage1
  - stage2
  - demanifold
  - status/active
aliases:
  - StoryMotion-Loss-Contract
source_notes:
  - "[[2026-07-11_storymotion-v7.14-corrected-results]]"
  - "[[2026-07-12_storymotion-v7.17-decoder-cache-contract-execution]]"
  - "[[2026-07-11_storymotion-latest-roadmap]]"
source_papers:
  - "[[analysis/CVPR_2025/MARDM_Rethinking_Diffusion_for_Text_Driven_Human_Motion_Generation|MARDM]]"
  - "[[analysis/arxiv_2026/What_Matters_for_Diffusion_Friendly_Latent_Manifold_Prior_Aligned_Autoencoders_for_Latent_Diffusion|PAE]]"
created: 2026-07-12T12:05:00+0800
updated: 2026-07-12T12:40:00+0800
---

# StoryMotion Stage1 and Stage2 Loss Contract and Demanifold Diagnosis

> [!abstract] Decision
> 当前 Stage1 在 decoded normalized human/camera feature space优化 reconstruction 与 temporal velocity；Stage2 则只在 z-normalized latent space优化 START_X MSE，训练时不经过 decoder，也没有 motion、velocity、joint或 framing loss。corrected v7.17 已证明 local latent MSE 下降时 decoded human manifold 可以同时崩溃。最可信的根因是 **latent-only loss 与 local latent correlated geometry / decoder-sensitive directions 的交互失配**，而不是“latent loss 在所有 tokenizer 上都错误”，因为 official AE 使用同一 Stage2 loss 能持续改善。

## 1. 当前数据空间

| layer | tensor | shape | space |
| --- | --- | --- | --- |
| Stage1 input / output human | `human` | `[B,T,199]` | PulpMotion normalized SMPL-RIFKE feature |
| Stage1 input / output camera | `camera` | `[B,T,14]` | FOV2 + relative distance3 + rotation6d + normalized velocity3 |
| Stage1 joint latent | `z` | `[B,192,75]` in Stage2 cache | human128 + camera64；cache 为 human-first order |
| Stage2 train latent | `z_norm` | `[B,192,75]` | train valid-frame per-channel z-normalized latent |
| raw evaluation | SMPL joints / camera matrices / projection | variable | owning decoder 后经 Pulp feature-to-raw contract 获得 |

“raw motion”需要区分两层：

- decoder 直接输出的 human199/camera14 是 normalized motion features，连续且可微；
- SMPL joints、camera matrix 和 projection 由 dataset `get_raw` 等转换获得，当前 eval 路径不是设计为训练时端到端反传。

因此可执行的 motion-space auxiliary 首先应放在 **decoded feature space**，而不是把 official raw evaluator 整体塞进训练循环。

## 2. Stage1 Loss

代码锚点：

- `storymotion/tokenizers/joint_human_camera.py::_branch_reconstruction_losses`
- `storymotion/tokenizers/base.py::masked_smooth_l1_loss`
- `storymotion/tokenizers/base.py::temporal_diff_loss`
- `scripts/train_storymotion_joint_tokenizer.py::apply_branch_loss_weights`

v7.14 corrected AE/VAE 都使用 non-causal encoder/decoder、human reconstruction weight `1`、camera reconstruction weight `1`、human/camera velocity weight `1`、acceleration weight `0`。

### 2.1 Joint AE

对有效帧：

```text
L_stage1_AE
  = SmoothL1(human_recon, human)
  + SmoothL1(camera_recon, camera)
  + MSE(Δ human_recon, Δ human)
  + MSE(Δ camera_recon, Δ camera)
  + commitment term
```

continuous joint AE 的 commitment term 为零值占位；量化 tokenizer 才使用非零 commitment。

### 2.2 Joint VAE

```text
L_stage1_VAE = L_stage1_recon_velocity + 1e-5 × KL(q(z|x) || N(0,I))
```

当前 `1e-5` KL 很弱。v7.17 full-cache stats 仍显示 local VAE channel std约 `1.19`，不能据此认为它已形成 diffusion-friendly isotropic Gaussian prior。

### 2.3 Stage1 Loss 能保证什么

它直接约束：

- on-manifold reconstruction；
- normalized feature逐帧误差；
-一阶 temporal velocity；
- owning decoder 对 encoder 输出的闭环。

它不直接约束：

- latent marginal是否 Gaussian；
-跨 channel covariance与条件数；
- encoder manifold周围的 decoder Jacobian；
-随机方向或 denoiser error方向的 decoder稳定性；
-文本语义在 latent空间中的可预测性。

## 3. Stage2 Loss

代码锚点：

- `storymotion/stage2/processes.py::CondMDIDiffusionProcess`
- `scripts/train_stage2_condmdi_pulp.py::diffusion_loss`
- `scripts/train_stage2_condmdi_pulp.py::masked_target_mse`

当前 diffusion process 是 cosine schedule、`1000` timesteps、prediction type `START_X`：

```text
z_t = sqrt(alpha_bar_t) × z_0 + sqrt(1-alpha_bar_t) × epsilon
target = z_0
L_stage2 = masked MSE(predicted_z0, z0)
```

实际 `z0` 是 per-channel normalized latent。loss 只覆盖 task 的 target branch 与 valid latent frames。v7.17 joint-only 使用 `element_mean`，因此 128维 human branch 与64维 camera branch按元素数自然形成 `2:1` 权重。

训练循环中：

- 不加载 Stage1 decoder；
- 不计算 decoded human199/camera14 reconstruction；
- 不计算 decoded velocity/acceleration；
- 不计算 SMPL joint、root path、framing或 Out；
- 不约束 prediction 是否仍位于 encoder latent manifold。

## 4. Loss 与 Demanifold 的直接证据

corrected v7.17 使用 same-manifest official AE、joint AE和joint VAE。三条 held-out latent loss 都在约5k最低，但 external decoded human metrics 的方向不同。

| latent | eval loss 1k → 5k | HCov 1k → 5k | FDTMR 1k → 5k |
| --- | ---: | ---: | ---: |
| official AE | `0.1891 → 0.1552` | `59.1% → 67.1%` | `350 → 339` |
| joint AE | `0.2740 → 0.1840` | `51.3% → 2.7%` | `524 → 1203` |
| joint VAE | `0.2529 → 0.1636` | `18.4% → 2.0%` | `928 → 1335` |

step-5k single-step predicted `z₀` 在低噪声 `t=100` 已显示首个 decisive failure：

| latent | HCov ↑ | FDTMR ↓ |
| --- | ---: | ---: |
| official AE | 98.8% | 173 |
| joint AE | 55.8% | 646 |
| joint VAE | 39.0% | 775 |

因此：

1. failure 在 full sampler 之前已经发生；
2. sampler 继续放大，但不是唯一原因；
3. per-channel z-normalization 修复了尺度，没有修复 covariance或 decoder-sensitive directions；
4. latent MSE 对 official AE有效，所以不能归纳为“START_X永远错误”；
5. 当前核心是 local representation与 objective 的组合不适配。

## 5. Stage2 应该对 Latent 还是 Motion 作 Loss

### 5.1 不建议 raw-only

纯 decoded-motion loss 的问题：

- decoder 可能存在多对一方向，raw loss不能唯一约束 latent；
-每步 decode 增加显存与计算；
-高噪声 timestep早期 prediction很差，raw gradient可能不稳定；
- official raw conversion与指标 callback不适合作为训练图的一部分；
-会削弱 diffusion target的概率建模含义。

### 5.2 推荐 hybrid loss

保留 latent diffusion主损失，加入 frozen owning decoder consistency：

```text
z0_hat = prediction_to_x0(model_output, z_t, t)
x_teacher = stopgrad(D(z0))
x_hat = D(z0_hat)

L = L_latent
  + lambda_feat(t) × SmoothL1(x_hat, x_teacher)
  + lambda_vel(t) × MSE(Δx_hat, Δx_teacher)
```

关键设计：

- target优先用 `D(z0)`，不是原始 `x`，避免要求 Stage2修补 Stage1固有重建误差；
- human/camera branch分别报告，不把 human199维与camera14维混成无解释平均；
- decoder参数冻结，但保留 `z0_hat → D(z0_hat)` 梯度；
-先在部分 batch或选定 timestep使用，控制计算量；
-所有 promotion仍由 owning-decoder external metrics决定。

可以追加的 manifold term包括 predicted residual在 train latent covariance下的 Mahalanobis penalty，或 encoder-cycle consistency；但应在 residual audit证明确切失配后再加，不能一次堆叠多个新 loss。

## 6. Loss 是否是核心原因

> [!warning] Causal boundary
> 现有实验已经证明 latent loss与 decoded quality发生系统性解耦，并把首次失败定位到 learned single-step prediction。它强烈支持“loss/geometry interaction是核心机制”。但尚未通过改变 loss并恢复指标的干预实验，因此不能写成已完成的因果证明。

当前可信度排序：

| mechanism | evidence | status |
| --- | --- | --- |
| wrong decoder / wrong causal cache | 已通过 identity与重建 cache修复 | 历史 bug，非当前剩余原因 |
|训练步数不足 | 5k后 held-out loss平台，external local更差 | 已基本排除 |
| sampler-only failure | `t=100` single-step已 demanifold | 已排除为单一原因 |
| local latent geometry × START_X MSE | official/local同 loss反向表现；single-step先坏 | 当前最强机制假设 |
|所有 joint tokenizer天生不适合 | Stage1 identity、方向性与small-noise gate通过 | 无证据支持 |

## 7. 最小因果实验

### P0-A Decoded-Feature Auxiliary

固定 joint AE cache、architecture、seed与schedule：

- control：当前 latent START_X MSE；
- treatment：latent MSE + frozen decoder feature/velocity auxiliary；
-只跑1k/3k snapshots；
-每个step比较latent loss、single-step HCov/FDTMR和50-step external metrics。

若 treatment 阻止1k→3k HCov collapse，同时 latent loss相近，才可把 decoded-space constraint视为修复证据。

### P0-B Prediction Target

在同一 cache 上比较 START_X与 epsilon/v-style target。必须复用同一 sampler语义和 external gate，不能只比较训练 loss数值。

### P0-C Geometry Control

对 human/camera latent分别做 covariance whitening或低秩 prior alignment，并在 decode前精确逆变换。该实验回答 per-channel normalization是否遗漏关键相关结构。

## 8. 当前路线裁决

-不延长当前 local AE/VAE到50k/93k；
-不先做 asymmetric、human-text leakage、replay或 editing；
-保留 official AE Stage2作为可学习 control；
-local候选只保留 joint AE，VAE降级；
-先用1k/3k hybrid-loss、target与geometry controls形成因果证据；
-只有其中至少一项恢复 decoded human manifold，才重训正式 Stage2。

## 9. v6 与 Demanifold 引入时间

### 9.1 保留的 v6 clean unified

有效 v6 anchor 使用 official Pulp AE cache：

`runs/train/stage2/independent_dropout_ft_20260614/gpu0_indepdrop_b512_50000/last.pt`

它存在普通后期过拟合信号：

| curve | earlier | best | late |
| --- | ---: | ---: | ---: |
| eval loss | step98k `0.01700` | step114k `0.01234` | step146k `0.01478` |
| eval joint | step98k `0.04542` | step114k `0.03186` | step146k `0.04029` |

但 step146k full external metrics仍健康：

| split / task | FDTMR ↓ | HCov ↑ | Out ↓ |
| --- | ---: | ---: | ---: |
| mixed human | 126.71 | 84.6% | - |
| mixed joint | 155.73 | 36.4% | 7.9% |
| pure human | 111.14 | 91.9% | - |
| pure joint | 137.12 | 46.4% | 6.9% |

因此 v6 clean unified 有常见的loss平台/过拟合，不存在 v7.17 local latent那种 HCov随训练降到约0的已证实灾难性 demanifold。

### 9.2 v6 的另一条 train/held-out分裂

`runs/train/stage2/condmdi_pulp_no_proj_20260611/gpu1_main` 的 train loss最终约 `0.00076`，eval loss从step4k最低 `0.05885` 增至step330.5k `0.28340`，属于明显过拟合。由于没有逐checkpoint decoded external metrics，不能把它直接称为已证明 demanifold。

### 9.3 当前可证明的最早引入点

v5–v7.16 的 local-tokenizer external rows受到 feature contract、owning decoder或causal cache错误影响，不能用于可靠定年。当前最早无混杂证据是 v7.17：

```text
corrected local cache identity healthy
  → Stage2 step1k degraded
  → step3k/5k HCov collapse while latent loss improves
```

同代码下 official AE latent持续改善，因此这不像近期引入的通用 Stage2代码回归；它是 corrected local latent与当前loss/geometry contract组合暴露出的representation-specific failure。
