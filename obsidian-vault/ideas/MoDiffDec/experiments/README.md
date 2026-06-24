---
title: "MoDiffDec Experiments"
status: active
hypothesis: "Experiments are separated from design notes; legacy runs remain as evidence, while the next roadmap must separate PiD-style target-space RF from LDM-style latent RF."
created: 2026-06-17T23:20:00+08:00
updated: 2026-06-18T15:35:00+08:00
tags:
  - MoDiffDec
  - experiments
source_papers:
  - "[[analysis/arxiv_2026/PiD_Fast_and_High-Resolution_Latent_Decoding_with_Pixel_Diffusion.md|PiD]]"
  - "[[analysis/CVPR_2026/MoLingo_Motion_Language_Alignment_for_Text_to_Human_Motion_Generation.md|MoLingo]]"
---

# MoDiffDec Experiments

## Current Evidence

- [[evaluation_D1_vs_baseline|evaluation_D1_vs_baseline]]: full test evaluation for D1 baseline versus CNN decoder, plus sampling-step ablation.
- [[archive_dseries_2026-06-17|archive_dseries_2026-06-17]]: D-series archive decision after finding the RF auxiliary-target bug.
- [[T0_T1_launch_2026-06-17|T0_T1_launch_2026-06-17]]: dual-GPU launch record for corrected T0 and T1.
- [[progress_legacy|progress_legacy]]: original progress log before the revised diagnostic plan.
- [[experiment_plan_legacy|experiment_plan_legacy]]: original D1-D7 matrix, now archived as legacy planning context.

## Current Remote Runs

| Run | Remote session | Status | Current role |
|---|---|---|---|
| D6 large | `traind6_gpu1` | Stopped on 2026-06-17 around E230. E200 MPJPE around 30.2 mm. | Archived evidence only; not the main next step. |
| T0 x0 fix | `modiffdec_T0_x0fix_gpu0` | Completed and evaluated. Best observed MPJPE: 29.77 mm at E300. | Corrected RF clean estimate did not close the gap. |
| T1 joint loss | `modiffdec_T1_joint_gpu1` | Completed and evaluated. Best observed MPJPE: 26.14 mm at E300. | Joint loss helps but still fails the raw-space route threshold. |
| TensorBoard | `modiffdec_D1_baseline_tb_6008` | Running. | Monitor old runs and T0 if reused. |

## New Experiment Naming

Use the T-series names from [[ideas/MoDiffDec/plan/diagnostic_matrix|diagnostic_matrix]]:

- `T0_x0fix_d1v6`: correct clean estimate, otherwise D1_v6.
- `T1_jointloss_raw`: T0 plus joint-space supervision.
- `T2_sae_cond_raw_rf`: strict PiD-style diagnostic; 272D raw-motion RF conditioned on frozen SAE latent.
- `T3_uncond_raw_rf`: same RF without SAE/VAE latent condition, the control for T2.
- `T4_ldm_baseline`: old latent-space RF plus frozen CNN decoder, retained only as an LDM-style baseline.
- `T5_vae_cond_raw_rf`: matched VAE-conditioned raw RF after reporting VAE direct decoder baseline.
- `T6_raw_prior`: raw-space pretrained motion diffusion/RF prior test.

Each run note should record:

```text
goal:
source:
selection_rule:
budget:
output_target:
code_commit_or_remote_snapshot:
checkpoint:
metrics:
decision:
```
