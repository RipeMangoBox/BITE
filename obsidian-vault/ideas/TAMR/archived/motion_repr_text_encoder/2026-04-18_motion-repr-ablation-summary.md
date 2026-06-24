# 2026-04-18 Motion Representation Ablation Summary

> ⚠️ **Setting 说明（非 MotionPatches 原生架构）**：本实验基于 `MotionReprBaseline`（2 层轻量 Transformer，D=256），checkpoint 约 9MB，不含 ViT-B/16 主干。结论不可直接迁移到 MotionPatches `ClipModel`。

## Run Status

- 本地串行 run 已完成，5 个 schema 均完成训练、best checkpoint 选择、以及 test set eval。
- MotionPatches 运行根目录：
  `/home/ripemangobox/Coding/Github/Motion/MotionPatches-main/checkpoints/motion_repr_ablation_local_2026-04-18_serial`
- 自动汇总文件：
  - `summary.md`
  - `summary.json`

## Important Note

- `scripts/run_motion_repr_ablation.py` 在训练结束后会自动：
  1. 按 val R@1 选择 best checkpoint
  2. 加载 best checkpoint
  3. 在 test set 上计算 retrieval metrics
- 因此这次不需要再额外跑一次独立 eval；当前 `metrics.json` 已经是最终 test 结果。

## Ranking

| Rank | Schema | Dim | BestEpoch | ValR1 | Primary | t2m/R1 | m2t/R1 | t2m/R5 | m2t/R5 | t2m/MedR | m2t/MedR |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 1 | kimodo_like_261 | 261 | 49 | 13.95 | 14.16 | 5.34 | 7.66 | 21.09 | 22.56 | 23.00 | 23.50 |
| 2 | pos66 | 66 | 46 | 12.48 | 14.05 | 5.96 | 8.24 | 20.06 | 21.95 | 26.00 | 27.50 |
| 3 | guo263 | 263 | 35 | 13.59 | 13.37 | 5.32 | 7.45 | 19.44 | 21.27 | 25.00 | 24.00 |
| 4 | hy201_recon | 201 | 38 | 13.46 | 13.03 | 4.95 | 7.06 | 19.05 | 21.07 | 27.00 | 26.00 |
| 5 | smpl_d135_recon | 135 | 25 | 12.71 | 11.84 | 4.58 | 6.56 | 17.76 | 18.45 | 30.00 | 30.00 |

## Main Takeaway

- 当前单次本地 run 的最佳 schema 是 `kimodo_like_261`。
- 但它和 `pos66` 的差距非常小：
  - `kimodo_like_261`: `PrimaryScore = 14.16`
  - `pos66`: `PrimaryScore = 14.05`
  - gap = `0.11`
- 因此如果要把 Step 0 结果写进后续正式实验设置，建议不要只凭这一次单 seed 就完全拍板。

## Interpretation

- `kimodo_like_261` 在当前 run 中总体最优，说明 richer motion representation 并不一定比 raw joint position 差。
- `pos66` 非常接近最优，且实现/解释最简单，这使它成为一个很强的 practical baseline 候选。
- `guo263` 没有赢过前两者，说明直接沿用传统 HumanML3D packaged feature 在这个 global contrastive setup 下并不占优。
- `smpl_d135_recon` 明显最差，说明只保留旋转主导信息、弱化位置/速度几何后，对当前 retrieval baseline 不利。

## Current Recommendation

- 不建议立刻只凭这一个 run 就正式固定 schema。
- 建议下一步优先做二选一确认：
  1. `kimodo_like_261`
  2. `pos66`

比较稳妥的决策方式：

- 方案 A：先做 2-3 个 seed 的复现实验，只重跑 `kimodo_like_261` 和 `pos66`
- 方案 B：如果时间更紧，就先固定 `kimodo_like_261`，同时在文档里注明它只比 `pos66` 略优

## Existing Artifacts

- 总汇总：
  `/home/ripemangobox/Coding/Github/Motion/MotionPatches-main/checkpoints/motion_repr_ablation_local_2026-04-18_serial/summary.md`
- 逐 schema 结果：
  - `.../guo263/guo263/metrics.json`
  - `.../pos66/pos66/metrics.json`
  - `.../smpl_d135_recon/smpl_d135_recon/metrics.json`
  - `.../hy201_recon/hy201_recon/metrics.json`
  - `.../kimodo_like_261/kimodo_like_261/metrics.json`

## Implementation Notes

- 当前输出目录有一层重复嵌套：`<run_root>/<schema>/<schema>/metrics.json`
- 这不影响结果正确性，但后续可以顺手修掉。
- 当前 run 只是一轮单卡本地串行实验，不是多 seed 正式结论。
