# REF00 Extended Eval Summary

Date: 2026-04-15

Updated: 2026-04-17 (fair-baseline audit note)

> Historical note (2026-04-17): this summary should now be treated as a legacy
> strict-split reference, not the current fair baseline summary. Although the
> strict retrieval preset is `humanml3de`, the retrieval gallery in these runs
> still comes from `MotionPatches-main/data/HumanML3D` (`TMR-normal len=4196`),
> not the newer packaged-root `HumanML3D-E-MP` fair eval (`TMR-normal len=4646`).
> See `eval_summary/2026-04-17_tamr-fair-baseline-eval-summary.md`.

Evaluated runs:
- `/home/ripemangobox/Coding/Github/Motion/TMR/MotionPatches-main/checkpoints/ref00_s42_70/HumanML3D`
- `/home/ripemangobox/Coding/Github/Motion/TMR/MotionPatches-main/checkpoints/ref00_s43/HumanML3D`
- `/home/ripemangobox/Coding/Github/Motion/TMR/MotionPatches-main/checkpoints/ref00_s44/HumanML3D`

Reference runs:
- `/home/ripemangobox/Coding/Github/Motion/TMR/MotionPatches-main/checkpoints/ref00_s41/HumanML3D`
- `/home/ripemangobox/Coding/Github/Motion/TMR/MotionPatches-main/checkpoints/ref00_s42/HumanML3D`

Shared eval protocol:
- strict retrieval preset: `humanml3de`
- retrieval gallery root: `MotionPatches-main/data/HumanML3D` (historical)
- temporal GT source: `HumanML3D-E-MP`
- offline evaluation mode for HuggingFace assets
## PrimaryScore Table

PrimaryScore definition:

`mean(TMR-normal R@1/R@5 + TMR-nsim R@1/R@5 over t2m+m2t)`

| Run | PrimaryScore | TMR-normal t2m R@1 | TMR-normal m2t R@1 | TMR-normal t2m R@5 | TMR-normal m2t R@5 | TMR-nsim t2m R@1 | TMR-nsim m2t R@1 | TMR-nsim t2m R@5 | TMR-nsim m2t R@5 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| ref00_s41 | **45.3625** | 7.39 | 11.34 | 26.74 | 27.74 | 54.64 | 54.64 | 90.72 | 89.69 |
| ref00_s42 | **43.9825** | 7.34 | 10.92 | 24.81 | 27.34 | 55.67 | 53.61 | 87.63 | 84.54 |
| ref00_s42_70 | **44.5962** | 7.24 | 11.03 | 25.71 | 27.22 | 59.79 | 58.76 | 83.51 | 83.51 |
| ref00_s43 | **45.5012** | 7.44 | 10.68 | 25.24 | 27.86 | 61.86 | 55.67 | 87.63 | 87.63 |
| ref00_s44 | **44.1462** | 7.44 | 11.49 | 26.38 | 28.48 | 53.61 | 56.70 | 86.60 | 82.47 |

## Temporal Diagnostics Snapshot

| Run | EVT-normal t2m CAR@1 | EVT-normal t2m TAR@5 | EVT-nsim t2m CAR@1 | EVT-nsim t2m TAR@5 |
|---|---:|---:|---:|---:|
| ref00_s41 | 9.44 | 16.78 | 60.42 | 47.42 |
| ref00_s42 | 9.07 | 15.90 | 64.58 | 40.21 |
| ref00_s42_70 | 8.86 | 17.68 | 75.00 | 43.30 |
| ref00_s43 | 9.03 | 16.90 | 68.75 | 43.30 |
| ref00_s44 | 9.03 | 16.44 | 64.58 | 52.58 |

## Aggregates

Four-seed baseline view (`s41`, `s42`, `s43`, `s44` only):
- mean = **44.7481**
- std = **0.7944**
- min/max = **43.9825 / 45.5012**

Two-seed extension view (`s42` vs `s42_70`):
- `ref00_s42`: **43.9825**
- `ref00_s42_70`: **44.5962**
- delta = **+0.6137**

## Interpretation

### 1. `s43` / `s44` confirm that seed variance remains high

- `ref00_s43` reaches **45.50**, slightly above `s41`.
- `ref00_s44` drops to **44.15**, still above `s42` but well below `s41/s43`.
- Four-seed std remains high at **0.79**.

This means `REF00` is now better characterized than before, but it is **still not a low-variance baseline**. Any future architecture gain smaller than ~`0.8` should be treated cautiously.

### 2. Extending `s42` from 50 → 70 epochs helps, but does not fully solve stability

- `s42_70` improves over `s42` by **+0.61 PrimaryScore**.
- However, `s42_70` still does not clearly exceed the better 50-epoch seeds (`s41`, `s43`).
- The 70-epoch result also trades off some `nsim R@5` while improving `nsim R@1`.

So the evidence supports:
- **50 epochs may be slightly short for some seeds**
- but **epoch extension alone is not enough to stabilize the baseline**

### 3. Practical recommendation

- Use the four-seed summary (`s41/s42/s43/s44`) only as a historical variance / training-length reference.
- If compute is limited, do **not** immediately re-run all seeds at 70 epochs.
- If you want to probe training length further, do it as a **targeted epoch-length ablation**, not as a blanket baseline replacement.
- Do **not** use this file alone to freeze the current fair baseline; packaged-root fair re-eval is the new source of truth.

## Recommendation

Current status:
- `REF00` here is usable only as a **historical rerun / variance reference**
- it is **not** the current fair paper baseline summary

Suggested next step priority:
1. Finish packaged-root fair re-eval before freezing any `REF00` baseline.
2. Only run a clean `50 vs 70 epoch` comparison if later architecture gains are in the same range as the observed seed variance.
3. Avoid over-interpreting sub-`+0.8` gains without bootstrap CI or additional seeds.

## Artifact References

- `/home/ripemangobox/Coding/Github/Motion/TMR/MotionPatches-main/checkpoints/ref00_s42_70/HumanML3D/contrastive_metrics/TMR-normal.yaml`
- `/home/ripemangobox/Coding/Github/Motion/TMR/MotionPatches-main/checkpoints/ref00_s42_70/HumanML3D/contrastive_metrics/TMR-nsim.yaml`
- `/home/ripemangobox/Coding/Github/Motion/TMR/MotionPatches-main/checkpoints/ref00_s42_70/HumanML3D/contrastive_metrics/EVT-normal.yaml`
- `/home/ripemangobox/Coding/Github/Motion/TMR/MotionPatches-main/checkpoints/ref00_s42_70/HumanML3D/contrastive_metrics/EVT-nsim.yaml`
- `/home/ripemangobox/Coding/Github/Motion/TMR/MotionPatches-main/checkpoints/ref00_s43/HumanML3D/contrastive_metrics/TMR-normal.yaml`
- `/home/ripemangobox/Coding/Github/Motion/TMR/MotionPatches-main/checkpoints/ref00_s43/HumanML3D/contrastive_metrics/TMR-nsim.yaml`
- `/home/ripemangobox/Coding/Github/Motion/TMR/MotionPatches-main/checkpoints/ref00_s43/HumanML3D/contrastive_metrics/EVT-normal.yaml`
- `/home/ripemangobox/Coding/Github/Motion/TMR/MotionPatches-main/checkpoints/ref00_s43/HumanML3D/contrastive_metrics/EVT-nsim.yaml`
- `/home/ripemangobox/Coding/Github/Motion/TMR/MotionPatches-main/checkpoints/ref00_s44/HumanML3D/contrastive_metrics/TMR-normal.yaml`
- `/home/ripemangobox/Coding/Github/Motion/TMR/MotionPatches-main/checkpoints/ref00_s44/HumanML3D/contrastive_metrics/TMR-nsim.yaml`
- `/home/ripemangobox/Coding/Github/Motion/TMR/MotionPatches-main/checkpoints/ref00_s44/HumanML3D/contrastive_metrics/EVT-normal.yaml`
- `/home/ripemangobox/Coding/Github/Motion/TMR/MotionPatches-main/checkpoints/ref00_s44/HumanML3D/contrastive_metrics/EVT-nsim.yaml`
