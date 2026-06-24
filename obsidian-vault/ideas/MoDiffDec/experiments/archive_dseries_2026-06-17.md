---
title: "MoDiffDec D-Series Archive 2026-06-17"
status: archived
hypothesis: "Old D-series runs are retained as failure evidence but no longer drive the roadmap because the RF auxiliary clean estimate was wrong."
created: 2026-06-17T23:10:00+08:00
updated: 2026-06-17T23:10:00+08:00
tags:
  - MoDiffDec
  - experiments
  - archived
source_papers:
  - "[[analysis/arxiv_2026/PiD_Fast_and_High-Resolution_Latent_Decoding_with_Pixel_Diffusion.md|PiD]]"
  - "[[analysis/CVPR_2026/MoLingo_Motion_Language_Alignment_for_Text_to_Human_Motion_Generation.md|MoLingo]]"
---

# MoDiffDec D-Series Archive 2026-06-17

## Archive Decision

The D-series runs are archived. They remain useful as evidence that the old route failed, but they should not be used to select new model sizes or schedules because the auxiliary clean-motion estimate in training was wrong.

Old training used:

```python
x0_pred = x_t - t.view(-1, 1, 1) * v_pred
```

Given the actual rectified-flow definition:

```python
x_t = t * motion_gt + (1 - t) * eps
v_target = motion_gt - eps
```

the clean estimate should be:

```python
x0_hat = x_t + (1 - t).view(-1, 1, 1) * v_pred
```

Therefore D-series auxiliary high-pass and velocity losses partially supervised a noise estimate as if it were motion.

## Archived Results

| Run | Status | Best known MPJPE | Conclusion |
|---|---|---:|---|
| CNN SAE decoder | Completed | about 10.0 mm | Reconstruction baseline. |
| D1 baseline | Completed | about 33.95 mm | Old from-scratch RF decoder failed. |
| D1 v6 | Completed | about 29.42 mm | Best old result, but trained with wrong auxiliary clean estimate. |
| D6 large | Stopped on 2026-06-17 around E230 | E200 about 30.18 mm | Larger model did not fix the gap before stop; no need to continue under old bug. |

## Remote State

- D6 session `traind6_gpu1` was stopped manually.
- GPUs were confirmed idle after stop.
- Checkpoints retained under:
  - `/data/public/ripemangobox/Motion/MoLingo/mogen/checkpoints/ms/modiffdec_D1_baseline/`
  - `/data/public/ripemangobox/Motion/MoLingo/mogen/checkpoints/ms/modiffdec_D1_v6/`
  - `/data/public/ripemangobox/Motion/MoLingo/mogen/checkpoints/ms/modiffdec_D6_large/`
- Temporary eval scripts retained:
  - `/tmp/eval_modiffdec.py`
  - `/tmp/eval_v6_d6.py`
  - `/tmp/modiffdec_eval_results.json`

## Next Runs

The replacement experiments are:

1. `T0_x0fix_d1v6`: correct clean estimate, no joint loss.
2. `T1_jointloss_raw`: same correction plus joint-space MPJPE and joint-velocity loss.

Both are diagnostic experiments; success or failure is judged by [[ideas/MoDiffDec/plan/diagnostic_matrix|diagnostic_matrix]].
