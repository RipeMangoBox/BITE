# REF00 Two-Seed Eval Summary

Date: 2026-04-15

Updated: 2026-04-17 (fair-baseline audit note)

> Historical note (2026-04-17): this two-seed summary is now a legacy
> strict-split reference. These runs use `humanml3de` strict split, but the
> retrieval gallery still comes from `MotionPatches-main/data/HumanML3D`
> (`TMR-normal len=4196`), not the newer packaged-root `HumanML3D-E-MP` fair
> eval (`TMR-normal len=4646`). See
> `eval_summary/2026-04-17_tamr-fair-baseline-eval-summary.md`.

Runs:
- `/home/ripemangobox/Coding/Github/Motion/TMR/MotionPatches-main/checkpoints/ref00_s41/HumanML3D`
- `/home/ripemangobox/Coding/Github/Motion/TMR/MotionPatches-main/checkpoints/ref00_s42/HumanML3D`

Eval protocol:
- strict retrieval preset: `humanml3de`
- retrieval gallery root: `MotionPatches-main/data/HumanML3D` (historical)
- temporal GT source: `HumanML3D-E-MP`
- offline evaluation mode for HuggingFace assets
## PrimaryScore

PrimaryScore definition:

`mean(TMR-normal R@1/R@5 + TMR-nsim R@1/R@5 over t2m+m2t)`

| Run | PrimaryScore | TMR-normal t2m R@1 | TMR-normal m2t R@1 | TMR-normal t2m R@5 | TMR-normal m2t R@5 | TMR-nsim t2m R@1 | TMR-nsim m2t R@1 | TMR-nsim t2m R@5 | TMR-nsim m2t R@5 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| ref00_s41 | **45.3625** | 7.39 | 11.34 | 26.74 | 27.74 | 54.64 | 54.64 | 90.72 | 89.69 |
| ref00_s42 | **43.9825** | 7.34 | 10.92 | 24.81 | 27.34 | 55.67 | 53.61 | 87.63 | 84.54 |

Aggregate:
- mean = **44.6725**
- std = **0.9758**
- min/max = **43.9825 / 45.3625**

## Temporal Diagnostics

| Run | EVT-normal t2m CAR@1 | EVT-normal t2m TAR@5 | EVT-nsim t2m CAR@1 | EVT-nsim t2m TAR@5 |
|---|---:|---:|---:|---:|
| ref00_s41 | 9.44 | 16.78 | 60.42 | 47.42 |
| ref00_s42 | 9.07 | 15.90 | 64.58 | 40.21 |

## Interpretation

- Two-seed mean (**44.67**) is close to the earlier single-seed `S2E-v2` reference range, but variance is still large (`std ≈ 0.98`).
- `ref00_s41` is clearly above 45.3, while `ref00_s42` falls below 44.0. This spread is too wide to treat the current two-seed result as a stable final baseline.
- The result is useful as a **historical preliminary reference signal**, but not strong enough for final go/no-go. A third seed is still recommended before freezing `REF00` as the paper baseline, and packaged-root fair re-eval is now mandatory.

## Artifact References

- `/home/ripemangobox/Coding/Github/Motion/TMR/MotionPatches-main/checkpoints/ref00_s41/HumanML3D/contrastive_metrics/TMR-normal.yaml`
- `/home/ripemangobox/Coding/Github/Motion/TMR/MotionPatches-main/checkpoints/ref00_s41/HumanML3D/contrastive_metrics/TMR-nsim.yaml`
- `/home/ripemangobox/Coding/Github/Motion/TMR/MotionPatches-main/checkpoints/ref00_s41/HumanML3D/contrastive_metrics/EVT-normal.yaml`
- `/home/ripemangobox/Coding/Github/Motion/TMR/MotionPatches-main/checkpoints/ref00_s41/HumanML3D/contrastive_metrics/EVT-nsim.yaml`
- `/home/ripemangobox/Coding/Github/Motion/TMR/MotionPatches-main/checkpoints/ref00_s42/HumanML3D/contrastive_metrics/TMR-normal.yaml`
- `/home/ripemangobox/Coding/Github/Motion/TMR/MotionPatches-main/checkpoints/ref00_s42/HumanML3D/contrastive_metrics/TMR-nsim.yaml`
- `/home/ripemangobox/Coding/Github/Motion/TMR/MotionPatches-main/checkpoints/ref00_s42/HumanML3D/contrastive_metrics/EVT-normal.yaml`
- `/home/ripemangobox/Coding/Github/Motion/TMR/MotionPatches-main/checkpoints/ref00_s42/HumanML3D/contrastive_metrics/EVT-nsim.yaml`
