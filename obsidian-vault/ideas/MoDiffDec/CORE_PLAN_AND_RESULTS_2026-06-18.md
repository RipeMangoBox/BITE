---
title: "MoDiffDec Core Plan and Results 2026-06-18"
status: active
hypothesis: "T0 and T1 show that correcting the RF clean estimate and adding raw joint-space supervision do not close the MoLingo CNN decoder gap; strict PiD adaptation should be latent-conditioned raw-motion RF, while latent-space RF plus a frozen CNN decoder is only an LDM-style baseline."
created: 2026-06-18T13:25:46+08:00
updated: 2026-06-18T15:35:00+08:00
tags:
  - MoDiffDec
  - research_plan
  - experiments
  - diagnostic
source_papers:
  - "[[analysis/arxiv_2026/PiD_Fast_and_High-Resolution_Latent_Decoding_with_Pixel_Diffusion.md|PiD]]"
  - "[[analysis/CVPR_2026/MoLingo_Motion_Language_Alignment_for_Text_to_Human_Motion_Generation.md|MoLingo]]"
  - "[[analysis/ICLR_2026/COME_Advancing_Representation_Learning_and_Generative_Modeling_for_High_Quality_Text_to_Motion_Generation.md|COME]]"
---

# MoDiffDec Core Plan and Results 2026-06-18

> [!abstract] 结论
> T0/T1 已完成训练和 full test MPJPE 评估。T0 几乎没有优于 D1_v6；T1 的 joint-space loss 带来约 3.6 mm 改善，但最佳仍为 26.14 mm，距离 MoLingo SAE CNN decoder 的 10.03 mm 很远，也没有达到 T1 的 14 mm 成功阈值。进一步复核 PiD 后，旧版“latent-space RF + frozen CNN decoder”应降级为 LDM baseline；严格 PiD-to-motion 主线应是以 SAE/VAE latent 为条件、在 272D motion target space 做 RF 解码。

## Links

- 总入口：[[ideas/MoDiffDec/README]]
- 诊断矩阵：[[ideas/MoDiffDec/plan/diagnostic_matrix]]
- 修订方案：[[ideas/MoDiffDec/plan/revised_plan_2026-06-17]]
- PiD/LDM 术语纠偏：[[ideas/MoDiffDec/plan/deepseek_pid_correction_2026-06-18]]
- T0/T1 启动记录：[[ideas/MoDiffDec/experiments/T0_T1_launch_2026-06-17]]
- D-series archive：[[ideas/MoDiffDec/experiments/archive_dseries_2026-06-17]]
- 实验索引：[[ideas/MoDiffDec/experiments/README]]

## Evaluation Setup

- Remote root: `/data/public/ripemangobox/Motion/MoLingo`
- Eval script: `/tmp/eval_t0_t1_mpjpe.py`
- Eval result JSON: `/tmp/modiffdec_T0_T1_eval_results.json`
- Eval log: `/data/public/ripemangobox/Motion/logs/remote4090/modiffdec_eval_T0_T1_mpjpe.log`
- Data: `HumanML3D_272` test split through `Text2MotionDatasetMS`
- Dataset items in this eval: `4404` samples, `276` batches
- Metric: root-aligned MPJPE in mm
- Sampling: 16-step Euler from clean SAE latent condition, same quick-eval口径 as D1_v6/D6 diagnosis

## Results

| Run | Checkpoint | Epoch | MPJPE ↓ | Delta vs CNN | Verdict |
|---|---|---:|---:|---:|---|
| CNN SAE decoder | direct decoder | - | 10.03 ± 8.37 | 0.00 | Reconstruction baseline. |
| D1_v6 | best_l1 | 270 | 29.67 ± 25.90 | +19.64 | Old best reference. |
| T0 x0 fix | best_l1 | 300 | 29.84 ± 30.88 | +19.81 | Fails T0 threshold. |
| T0 x0 fix | best_flow | 280 | 54.29 ± 43.34 | +44.26 | Flow-val checkpoint is unsafe for MPJPE. |
| T0 x0 fix | E200 | 200 | 32.26 ± 37.81 | +22.23 | Worse than E300. |
| T0 x0 fix | E300 | 300 | 29.77 ± 27.76 | +19.73 | Best T0, still fails. |
| T1 joint raw | best_l1 | 300 | 26.19 ± 33.15 | +16.16 | Partial gain, still fails T1 threshold. |
| T1 joint raw | best_flow | 280 | 26.56 ± 33.13 | +16.53 | Similar to best_l1. |
| T1 joint raw | E200 | 200 | 27.38 ± 32.67 | +17.34 | Worse than E300. |
| T1 joint raw | E300 | 300 | 26.14 ± 31.62 | +16.11 | Best observed corrected raw RF. |

## Diagnostic Decisions

### T0: clean-estimate bug is real but not the main MPJPE bottleneck

The code bug was real: under the actual RF definition,

```python
x_t = t * motion_gt + (1 - t) * eps
v_target = motion_gt - eps
```

the clean estimate must be:

```python
x0_hat = x_t + (1 - t) * v_pred
```

However, fixing it did not improve test MPJPE. T0 E300 is 29.77 mm, essentially tied with D1_v6 best_l1 at 29.67 mm. This rejects the hypothesis that the auxiliary `x0_pred` bug was the dominant cause of the 10 mm to 30 mm gap.

### T1: joint loss helps, but raw-space RF still fails

T1 E300 reaches 26.14 mm, about 3.6 mm better than T0 E300. This supports the loss/eval mismatch hypothesis: joint-space supervision does help. But the result is still 16.11 mm worse than CNN baseline and far above the T1 success criterion of 14 mm. This is not a near miss; it is still a qualitatively different reconstruction regime.

### Checkpoint selection must move to joint-space validation

For T0, `best_flow` gives 54.29 mm, much worse than E300. This means validation `flow_loss` is not a safe checkpoint selector for geometric reconstruction. Future runs must log and select by validation MPJPE or at least a differentiable joint-space proxy.

### PiD framing remains unsupported

The current implementation is a from-scratch conditional RF decoder in normalized 272D motion feature space. It is structurally closer to PiD than a latent-space RF route because PiD predicts the target-space velocity field conditioned on latent codes. However, it is still not faithful enough to support a PiD claim: it lacks a pretrained target-space motion diffusion prior and it did not yet establish that the SAE/VAE latent condition is the decisive variable.

Do not call `SAE latent-space RF + frozen CNN decoder` the next PiD experiment. That route is an LDM-style baseline: diffusion happens in latent space and the original CNN decoder remains the final decoder. PiD instead replaces/enhances deterministic decoding with target-space conditional diffusion/RF.

## Reconstruction Visualization

GPU0 visualization was generated after evaluation:

- Remote artifact dir: `/data/public/ripemangobox/Motion/MoLingo/artifacts/modiffdec_recon_viz_20260618`
- Local fetched summary: `/data/Life Me/ResearchWY Vault/artifacts/remote4090_motion/modiffdec_recon_viz_20260618/SUMMARY.md`
- Format: GIF via Matplotlib PillowWriter because `ffmpeg` is unavailable on remote PATH.
- Methods: GT, SAE direct, VAE direct, T1 joint raw RF E300.

| Sample | SAE MPJPE | VAE MPJPE | T1 MPJPE | Evidence |
|---:|---:|---:|---:|---|
| 0 | 10.04 | 11.14 | 19.45 | `sample_0000/compare_gt_sae_vae_t1.gif` |
| 1 | 9.27 | 9.18 | 30.62 | `sample_0001/compare_gt_sae_vae_t1.gif` |
| 2 | 16.35 | 17.50 | 30.33 | `sample_0002/compare_gt_sae_vae_t1.gif` |

The visualized samples match the aggregate diagnosis: direct SAE/VAE decoding is close to GT, while T1 remains visibly and numerically worse.

## Updated Hypotheses

| Hypothesis | Status | Evidence |
|---|---|---|
| Auxiliary `x0_pred` bug explains most of the gap. | Rejected as main cause. | T0 fixed the bug but stayed around 29.8 mm. |
| Feature-space loss and MPJPE are misaligned. | Supported. | T1 joint loss improves about 3.6 mm; `best_flow` can be very bad. |
| Raw 272D from-scratch RF without a target-space prior is the main obstacle. | Likely. | T0/T1 remain far from CNN despite same SAE latent and correct RF estimate. |
| SAE text alignment causes reconstruction failure. | Not supported for Stage 1. | Stage 1 has no text condition; CNN baseline uses the same SAE latent and reaches 10.03 mm. |
| VAE may be a better condition latent than SAE. | Unresolved. | Needs matched SAE/VAE decoder baselines and matched conditioned RF runs. |
| Missing target-space pretrained prior is decisive for PiD-style quality. | Plausible and still open. | Current route lacks this; larger/raw RF did not close the gap. |

## Core Plan

### P0: freeze raw-space from-scratch scaling

Do not continue D6/D7-style scaling or scheduler tuning as the main route. T0/T1 show that the corrected raw-space decoder remains far from the CNN baseline. More sampling steps were already ineffective, and more epochs did not change the regime.

### P1: rename old T2 to LDM baseline

The old T2 proposal is no longer the PiD mainline:

- Output space: SAE latent space, not 272D raw motion features.
- Decoder to motion: frozen MoLingo SAE CNN decoder.
- First loss: latent MSE only.
- Eval: same root-aligned MPJPE after frozen CNN decode.

This is useful only as an LDM-style comparison. It answers whether latent-space denoising is easier, but it does not test PiD's core claim because the deterministic CNN decoder remains the actual decoder. Keep it out of the main PiD evidence chain unless the project deliberately pivots to latent diffusion.

### P2: run T2-SAE, the strict PiD-style diagnostic

The next core experiment should keep the target variable in raw motion space:

- Target/output space: normalized 272D motion features.
- Condition: frozen MoLingo SAE latent `z`, including the existing noise-latent conditioning and sigma-aware gate.
- Decoder: RF model itself is the generative decoder; the SAE CNN decoder is not used during RF inference except as a reconstruction baseline.
- Loss: corrected RF loss first; add validation MPJPE and checkpoint by validation MPJPE before new long training.
- Success threshold: MPJPE ≤ 16 mm, or at minimum a clear >5 mm gain over the unconditioned raw RF baseline.

Purpose: isolate whether the MoLingo latent condition can make target-space RF competitive. This is the closest current analogue of PiD without importing an external pretrained motion prior.

### P3: run T3-unconditioned with the same raw RF

Use the same architecture, optimizer, loss, schedule, validation MPJPE, and sampling setup, but remove the SAE/VAE latent condition. This is the control for PiD's latent conditioning. If T2-SAE does not improve this baseline meaningfully, the latent condition is not carrying enough usable information into the RF decoder.

### P4: SAE vs VAE only as matched conditioned RF

Run VAE only after the SAE-conditioned and unconditioned baselines are clean:

- Measure matched VAE direct decoder baseline first.
- Run matched VAE-conditioned raw RF with the same architecture and validation protocol.
- Claim VAE helps only if it improves matched SAE-conditioned RF by more than 5 mm while preserving an acceptable direct decoder baseline.

### P5: PiD-style claim requires a motion prior

If the goal remains "PiD for motion", find or build a target-space pretrained motion diffusion prior:

- Candidate source: raw-motion or joint-space pretrained diffusion/flow model.
- Required adaptation: replace or augment text condition with MoLingo SAE/VAE latent condition.
- Without this, describe the work as a conditional RF motion decoder, not a faithful PiD adaptation.

## Stop Rule

T0 and T1 have failed the diagnostic thresholds. If T2-SAE and the matched unconditioned RF control both stay far above 16 mm MPJPE, stop the current from-scratch route. At that point the practical path is to improve or distill the MoLingo CNN decoder, or to restart only with a real target-space pretrained motion prior.

## Immediate Action Items

1. Add validation MPJPE logging and checkpoint selection before any new training.
2. Implement T2-SAE as latent-conditioned raw-motion RF, not latent-space RF.
3. Archive T0/T1 as corrected raw-space RF evidence, not as a mainline architecture.
4. Keep old latent-space RF only as `LDM-baseline`.
5. Do not add text condition, DMD/LCM distillation, or larger raw transformer until T2-SAE and the unconditioned control change the conclusion.
