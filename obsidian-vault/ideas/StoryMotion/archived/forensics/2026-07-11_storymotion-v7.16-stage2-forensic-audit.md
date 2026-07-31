---
title: "StoryMotion v7.16 Stage2 Forensic Audit"
status: completed
hypothesis: |
  The v7.15/v7.16 Stage2 collapse must be separated into evaluator-contract failure, denoiser learnability, sampler accumulation, and tokenizer latent geometry before topology or tokenizer suitability is judged.
tags:
  - StoryMotion
  - Motion_Generation
  - experiment
  - audit
  - stage2
  - status/completed
aliases:
  - StoryMotion-v7.16-Audit
source_notes:
  - "[[2026-07-11_storymotion-v7.14-corrected-results]]"
  - "[[2026-07-11_storymotion-v7.15-matched-stage2-results]]"
  - "[[2026-07-11_storymotion-latest-roadmap]]"
source_papers:
  - "[[analysis/ICLR_2026/Pulp_Motion_Framing_aware_multimodal_camera_and_human_motion_generation|Pulp Motion]]"
  - "[[analysis/CVPR_2025/MARDM_Rethinking_Diffusion_for_Text_Driven_Human_Motion_Generation|MARDM]]"
  - "[[analysis/arxiv_2026/What_Matters_for_Diffusion_Friendly_Latent_Manifold_Prior_Aligned_Autoencoders_for_Latent_Diffusion|PAE]]"
created: 2026-07-11T23:54:20+0800
updated: 2026-07-12T00:35:00+0800
---

# StoryMotion v7.16 Stage2 Forensic Audit

> [!abstract] Decision
> v7.15/v7.16 的灾难性 official 指标主要由 **local joint tokenizer latent 被送入 official Pulp decoder** 的 evaluator contract 错配造成，不能作为 Stage2 崩溃或 tokenizer 不适合扩散的证据。改用正确 local decoder 后，10k AE/VAE Stage2 仍明显弱于可用基线，且 held-out joint loss 已在 5k–10k 平台化。因此 10k 足够作为当前配置的 kill gate，但不足以否定 joint tokenizer 或证明增加训练步数永远无效。

> [!danger] 2026-07-12 superseding correction
> 旧 Stage2 cache builder 还忽略了 v7.14 checkpoint 的 `is_causal: false`，实际用 causal encoder 生成了 v7.15/v7.16 cache。旧 cache 与 owning non-causal encoder 的 latent RMS difference 达 AE `0.54–0.61`、VAE `0.69–0.82`。因此本页第 2–3 节旧 cache/10k 数值只保留作历史取证，不能判断修正版 latent 的 learnability。修复执行与新实验 gate 见 [[2026-07-12_storymotion-v7.17-decoder-cache-contract-execution]]。

## 1. 审计范围与锚点

训练与评估工件位于 4090：

- `runs/train/stage2/v7_16_znorm_calibration_20260711/`
- `runs/eval/stage2/v7_16_znorm_calibration_20260711/`
- `runs/train/stage2/v7_13_priority_20260710/exp1_symmetric_joint_width416_steps37500_seed17/`
- `runs/eval/stage2/v7_13_priority_20260710/exp1_symmetric_joint_mixed_full.json`

代码锚点：

- commit `816eb26`：恢复 Stage2 per-channel valid-frame z-normalization。
- `scripts/build_stage2_joint_tokenizer_latent_cache.py`：local cache 记录 tokenizer checkpoint、preset 与 `concat([z_hum,z_cam])`。
- `scripts/storymotion_official_bridge_smoke.py::build_pulp`：默认实例化 official Pulp autoencoder。
- `scripts/storymotion_official_bridge_smoke.py::decode_feature_and_raw`：把输入 latent 重排后交给该 official decoder。
- `scripts/storymotion_official_full_eval.py`：v7.15/v7.16 没有根据 cache metadata 切换到 local joint tokenizer decoder。

## 2. 已确认的 evaluator decoder 错配

v7.16 JSON 同时记录了以下互相冲突的 contract：

- cache source：`storymotion_joint_tokenizer`；
- cache tokenizer：v7.14 local joint AE/VAE checkpoint；
- eval `model_dir`：`/data/public/ripemangobox/Motion/PulpMotion_official_eval/pulpmotion-models`。

维度与通道顺序相同不能保证 latent basis 相同。将 **真实 local cache latent** 绕过 Stage2、直接送入错误的 official decoder，已经几乎复现 v7.16 的所谓崩溃。

### 2.1 AE：错误 decoder 本身复现灾难指标

| 路径 | FDTMR ↓ | TMR ↑ | HCov ↑ | FDCLaTr ↓ | CLaTr ↑ | CCov ↑ | F1 ↑ | Out ↓ |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| local AE cache → wrong official decoder，256 | 1787.38 | 0.00 | 0.00% | 580.17 | 4.99 | 14.52% | 0.0535 | 79.55% |
| v7.16 AE Stage2 → wrong official decoder，256 | 1815.54 | 0.00 | 0.00% | 590.34 | 4.59 | 15.67% | 0.0507 | 79.74% |
| v7.16 AE Stage2 → correct local AE decoder，256 | 1171.30 | 6.35 | 3.91% | 284.32 | 15.04 | 57.50% | 0.1673 | 54.27% |

### 2.2 VAE：同样由错误 decoder 主导

| 路径 | FDTMR ↓ | TMR ↑ | HCov ↑ | FDCLaTr ↓ | CLaTr ↑ | CCov ↑ | F1 ↑ | Out ↓ |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| local VAE cache → wrong official decoder，256 | 1441.74 | 0.00 | 1.15% | 650.20 | 5.28 | 4.71% | 0.0545 | 96.56% |
| v7.16 VAE Stage2 → wrong official decoder，256 | 1542.95 | 0.00 | 0.00% | 671.04 | 7.56 | 3.53% | 0.0327 | 97.37% |
| v7.16 VAE Stage2 → correct local VAE decoder，256 | 993.72 | 7.63 | 5.51% | 283.58 | 14.22 | 57.85% | 0.1533 | 66.43% |

正确 decoder 明显改善结果，但 10k 两组仍不可用。这个剩余缺口才是 Stage2 需要解释的真实问题。

## 3. 同 step 训练曲线

三条 symmetric joint-only run 使用相同 width `416`、batch `512`、seed `17`、cosine diffusion、`START_X` 与学习率 `1e-4`。official latent run 是当前最接近“正常 latent contract”的代码内对照。

| latent | step 1k joint eval loss | step 5k joint eval loss | step 10k train loss | step 10k joint eval loss | step 10k joint test loss |
| --- | ---: | ---: | ---: | ---: | ---: |
| official Pulp AE latent | 0.0810 | 0.0547 | 0.0541 | 0.0596 | 0.0496 |
| local joint AE + z-norm | 0.2614 | 0.1789 | 0.1298 | 0.1902 | 0.1839 |
| local joint VAE + z-norm | 0.2556 | 0.1656 | 0.1210 | 0.1750 | 0.1654 |

判断：

1. local AE/VAE 在 step 1k 已比 official latent 难学约三倍；不是到 10k 才突然崩溃。
2. local held-out joint loss 在 5k→10k 没有继续下降，AE 从 `0.1789` 到 `0.1902`，VAE 从 `0.1656` 到 `0.1750`；同时 train loss 继续下降，已经出现泛化平台而非单纯欠训练曲线。
3. step 10k 的 joint test loss 仍是 official 对照的 `3.71×`（AE）和 `3.34×`（VAE）。
4. batch `512` 下 10k steps 约产生 `5.12M` sample presentations；相对 `162760` 个训练样本约为 `31.5` 次名义遍历。它不是“只看了很少数据”，但比 Pulp Motion 公布的 pure `92950` steps 和 mixed `330750` steps 明显短。

因此：

> [!warning] 10k 的结论边界
> 10k 足够否定“norm 修好后已经恢复正常，只需直接晋级 asymmetric/full run”；不足以否定“更长训练可继续改善”，更不足以否定 joint tokenizer。最终判断需要正确 decoder、同 pure IDs、同 step 的 official/local 外部指标曲线。

## 4. Stage2 失败原因分层

### 4.1 已确认代码问题

1. **Evaluator decoder contract 错配**：解释 v7.15/v7.16 大部分灾难性 official 指标；这些旧指标作废。
2. **v7.15 缺少 per-channel z-normalization**：commit `816eb26` 已修复；v7.16 stats/hash/roundtrip 生效，因此它是历史回归，但不是 v7.16 剩余差距的解释。
3. **joint-only checkpoint 选择错误**：`evaluate()` 固定遍历 camera、human、joint、human-text 四个任务，而 `selection_metric=loss` 汇总了未训练任务。结果 AE `best_eval.pt` 停在 step `3000`，VAE 停在 step `2000`，不是最优 joint checkpoint。当前 256 重评使用 `last.pt`，所以该问题不造成本文 10k 结果，但会污染后续 best-checkpoint 选择。
4. **human-text 训练存在 camera-channel leakage**：`TASK_HUMAN_TEXT` 只屏蔽 camera loss，却仍把成对的 noisy camera latent 放进 `x_t`。推理 human-first 时 camera channels 来自随机噪声，形成 train–inference mismatch。它直接威胁 asymmetric human generator，但不能解释 v7.16 joint-only symmetric 的全部差距。

### 4.2 仍待验证

- local latent 的局部连续性、语义组织或 branch-conditioned density 是否比 official latent 更难由当前 denoiser学习；
- `START_X` 单步误差是否在 50-step DDIM 中累积；
- local tokenizer decoder 对标准化 latent 邻域扰动是否敏感；
- 10k 是否只是过短，或更长训练只会继续过拟合；
- 当前 U-Net/CondMDI 宽度与 local latent geometry 是否失配。

## 5. Stage1 Ckpt 能排除什么

### 5.1 已能排除的上游问题

正确 local decoder 的 pure-4053 Stage1 指标为：

| tokenizer | FDTMR ↓ | HCov ↑ | FDCLaTr ↓ | CCov ↑ | F1 ↑ | Out ↓ |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| joint AE | 31.10 | 97.9% | 0.48 | 99.5% | 0.927 | 5.1% |
| joint VAE | 69.61 | 93.1% | 2.28 | 97.7% | 0.914 | 7.9% |

这些结果与 cache metadata/hash 可以排除：

- local Stage1 输入 human199/camera14 feature contract 错误；
- paired sample IDs、有效长度和 native latent reorder 在 Stage1 on-manifold reconstruction 路径中整体错位；
- local decoder 无法解码自身 encoder 输出；
- “VAE checkpoint 本身完全坍塌”。

它们不能排除 off-manifold continuity、diffusion learnability、文本条件语义组织或 sampler 误差累积。

### 5.2 Joint latent 是否适合 human-first 解耦

使用 224 个等长 paired samples，对 Stage1 encoder 输入做 modality shuffle，并按 train per-channel std 标准化 latent 变化：

| tokenizer | camera shuffle → human latent RMS | human shuffle → human latent RMS | 比值 | human shuffle → camera latent RMS | camera shuffle → camera latent RMS | 比值 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| joint AE | 0.0397 | 1.4964 | 2.65% | 0.7101 | 1.3233 | 53.7% |
| joint VAE | 0.0542 | 1.5013 | 3.61% | 0.9889 | 1.2015 | 82.3% |

证据支持的解释是：

- human latent 对 camera 输入近似不变，适合作为 human-first 的上游变量；
- camera latent 强依赖 human 输入，符合 framing-aware `H → C` 表示需求；
- 当前没有证据说明 joint tokenizer 天生不适合 Stage2 解耦；相反，它的方向性与 human-first 假设一致。

仍需用正确 decoder 的扰动/生成实验确认该局部结构是否足够 diffusion-friendly。不能从 reconstruction 或 shuffle sensitivity 直接推出生成成功。

## 6. 更新后的三个核心实验

### P0-1 修复并锁定 Decoder/Evaluator Contract

目标：先保证指标测的是正确模型。

- evaluator 根据 cache `source`、`tokenizer_checkpoint`、`tokenizer_preset` 选择 decoder；
- local cache 禁止静默回退到 official decoder；
- 加入 raw cache latent → owning decoder 的 256 identity gate，并与 Stage1 reconstruction 对齐；
- joint-only run 用 `joint_loss` 选择 checkpoint，保存 step `1k/3k/5k/10k` snapshots；
- 用正确 decoder 重评 v7.15/v7.16，旧 JSON 标记 invalidated。

成功标准：on-manifold cache identity 指标复现对应 Stage1 结果；decoder checkpoint/hash 写入 eval JSON。

### P0-2 无长训练的 Tokenizer/Denoiser/Sampler 三段审计

目标：用现有 Stage1/Stage2 ckpt 定位剩余差距。

1. local AE、local VAE、official AE latent 分别做 normalized perturbation `σ ∈ {0, 0.01, 0.02, 0.05, 0.1}`，必须用各自 decoder；
2. 在固定 `t` 网格上做 `z₀ → q(z_t) → predicted z₀ → decode`，与 oracle `z₀` decode 对比；
3. 对比单步 predicted `z₀` 与完整 50-step sampler，判断误差来自 denoiser 还是迭代累积；
4. 对 human-text 模型做 camera-channel normal/zero/shuffle/matched-noise 干预，量化 leakage。

分流规则：

- `σ` 很小时 local decoder 已崩：优先 Stage1 manifold continuity regularization；
- 单步 decode 好、full sampler 差：优先修 sampler/target calibration；
- 单步已差：优先 latent learnability或条件训练；
- human-text 对 camera noise 高敏感：先修任务 mask，再谈 asymmetric。

### P0-3 严格 Matched 10k Learnability Curve

目标：回答 10k 是否只是预算不足。

- official Pulp AE latent、local joint AE + z-norm、local joint VAE + z-norm；
- 相同 pure train/eval IDs、width、batch、seed、optimizer、task、sampler和正确 owning decoder；
- 在 step `1k/3k/5k/10k` 同时记录 joint held-out loss、official 256 metrics 和固定 renders；
- 10k 后只延长仍持续改善且通过正确 decoder gate 的分支。

只有胜出 tokenizer 的 symmetric baseline 恢复后，才继续到约 `50k/93k`，再比较 symmetric/asymmetric。separate tokenizer、replay 与 editing 均低于这个共享 contract gate。

## 7. 论文证据的适用边界

本地知识库提供三条方法学约束：

- [[analysis/ICLR_2026/Pulp_Motion_Framing_aware_multimodal_camera_and_human_motion_generation|Pulp Motion]] 证明统一 human-camera latent 与扩散可以工作，因此不能仅凭 joint 表示形式判死刑。
- [[analysis/CVPR_2025/MARDM_Rethinking_Diffusion_for_Text_Driven_Human_Motion_Generation|MARDM]] 表明确定性 AE 也能服务运动扩散，且表示尺度/冗余与预测目标会显著影响学习。
- [[analysis/arxiv_2026/What_Matters_for_Diffusion_Friendly_Latent_Manifold_Prior_Aligned_Autoencoders_for_Latent_Diffusion|PAE]] 明确指出 reconstruction quality 不等于 generation quality，局部连续性应单独测量。

这些论文支持 P0-2 的审计设计，但不能替代 StoryMotion 自身的正确-decoder对照。
