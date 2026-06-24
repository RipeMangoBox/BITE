---
title: "MoDiffDec GPT Handoff"
status: active
hypothesis: "Continue only through the diagnostic matrix; do not expand old D-series experiments before fixing the RF auxiliary target."
created: 2026-06-17T23:20:00+08:00
updated: 2026-06-17T23:20:00+08:00
tags:
  - MoDiffDec
  - handoff
source_papers:
  - "[[analysis/arxiv_2026/PiD_Fast_and_High-Resolution_Latent_Decoding_with_Pixel_Diffusion.md|PiD]]"
  - "[[analysis/CVPR_2026/MoLingo_Motion_Language_Alignment_for_Text_to_Human_Motion_Generation.md|MoLingo]]"
---

# MoDiffDec GPT Handoff

## Status

MoDiffDec is in diagnostic mode. The old D1-D7 expansion plan is paused.

> [!warning] Superseded by 2026-06-18 correction
> This handoff predates the PiD/LDM terminology correction in [[ideas/MoDiffDec/plan/deepseek_pid_correction_2026-06-18|deepseek_pid_correction_2026-06-18]]. Mentions of “T2 latent-space RF” are historical and should now be read as `T4-LDM-baseline`, not as the PiD mainline.

Current best reported metric:

| Model | MPJPE |
|---|---:|
| MoLingo SAE CNN decoder | about 10.0 mm |
| D1_v6 MoDiffDec | about 29.4 mm |
| D6 E200 MoDiffDec | about 30.2 mm |

D6 is still running remotely in `traind6_gpu1`; E200 already suggests model size is not the main fix.

## Critical New Finding

Current auxiliary high-pass and velocity losses use the wrong clean-motion estimate.

Given:

```python
x_t = t * motion_gt + (1 - t) * eps
v_target = motion_gt - eps
```

Correct clean estimate:

```python
x0_hat = x_t + (1 - t).view(-1, 1, 1) * v_pred
```

Current code used:

```python
x0_pred = x_t - t.view(-1, 1, 1) * v_pred
```

If `v_pred` is correct, the current expression estimates `eps`, not `x0`. This makes auxiliary frequency/velocity losses supervise noise as if it were motion.

## Updated Root-Cause View

1. P0: wrong `x0_pred` auxiliary target.
2. P1: feature-space flow loss does not directly optimize joint-space MPJPE.
3. P1: no target-space pretrained motion diffusion prior, so current work is not faithful PiD adaptation.
4. P2: raw 272D RF may be harder than latent-space RF.
5. P3: SAE vs VAE and text condition are secondary until reconstruction improves.

SAE motion-text alignment cannot explain the current Stage 1 reconstruction gap because the current decoder receives no text condition and the CNN baseline uses the same latent.

## Next Action

Run T0 from [[ideas/MoDiffDec/plan/diagnostic_matrix|diagnostic_matrix]]:

1. Patch remote `mogen/models/motion_diff_decoder/decoder_trainer.py`.
2. Replace auxiliary clean estimate with `x_t + (1-t)*v_pred`.
3. Rerun D1_v6 settings as `T0_x0fix_d1v6`.
4. Full test MPJPE:
   - ≤ 20 mm: bug was a major cause; proceed T1/T2.
   - > 20 mm: use fixed baseline but expect joint loss / prior to be necessary.

## Important Files

Local docs:

- [[ideas/MoDiffDec/README|README]]
- [[ideas/MoDiffDec/plan/revised_plan_2026-06-17|revised_plan_2026-06-17]]
- [[ideas/MoDiffDec/plan/diagnostic_matrix|diagnostic_matrix]]
- [[ideas/MoDiffDec/plan/deepseek_review_2026-06-17|deepseek_review_2026-06-17]]
- [[ideas/MoDiffDec/experiments/README|experiments]]

Remote code:

- `/data/public/ripemangobox/Motion/MoLingo/mogen/models/motion_diff_decoder/decoder_trainer.py`
- `/data/public/ripemangobox/Motion/MoLingo/mogen/models/motion_diff_decoder/motion_diff_decoder.py`
- `/data/public/ripemangobox/Motion/MoLingo/mogen/train_diff_decoder.py`

Remote eval:

- `/tmp/eval_v6_d6.py`
- `/tmp/eval_modiffdec.py`
- `/tmp/modiffdec_eval_results.json`

## Archived Context

The previous flat files were reorganized:

- Old handoff: [[ideas/MoDiffDec/handoff/GPT_HANDOFF_2026-06-17|GPT_HANDOFF_2026-06-17]]
- Old architecture: [[ideas/MoDiffDec/archive/legacy/architecture_initial|architecture_initial]]
- Old implementation: [[ideas/MoDiffDec/archive/legacy/implementation_initial|implementation_initial]]
- Old D-series plan: [[ideas/MoDiffDec/experiments/experiment_plan_legacy|experiment_plan_legacy]]
- Old progress: [[ideas/MoDiffDec/experiments/progress_legacy|progress_legacy]]
