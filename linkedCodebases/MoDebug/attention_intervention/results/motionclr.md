# MotionCLR Attention Intervention 报告

## 状态

| 项目 | 值 |
|---|---|
| Baseline | MotionCLR |
| 架构 | 18 个 CLRBlock layer |
| 已完成 families | baseline, SA, CA, CFG_SA, CFG_CA |
| Formal run roots | `motionclr/formal_candidates/trace1_full_eval_*_20260605_*` |
| 已完成 manifests | 74 个 full evaluator results |
| 中位运行时间 | 单层约 7.2-7.4 min |
| 报告范围 | 仅使用 20260605 formal outputs |

旧的 20260604 full outputs 仍存在。最终聚合使用 20260605 roots，避免重复计入 layer。

## 审计证据

| 证据 | 状态 | 说明 |
|---|---:|---|
| `paper_level_status` | OK | 所有 20260605 layer manifests 均为 `full_evaluator_metrics_computed`。 |
| Metrics files | OK | `metrics_summary.json` 存在且非空。 |
| Provenance | OK | Manifests 包含 wrapper script、command script、checkpoint hashes、git head/status、evaluator path 和 layer mapping。 |
| Hook evidence | OK | Manifests 包含 `hook_call_counts` 和 `replacement_checks`。 |
| Family coverage | OK | baseline 加每个 intervention family 的 18 层均完成。 |

远程 roots：

```text
/data/public/ripemangobox/Motion/experiments/MoDebug/motionclr/formal_candidates/trace1_full_eval_ca_cfg_ca_ds_review_20260605_gpu0
/data/public/ripemangobox/Motion/experiments/MoDebug/motionclr/formal_candidates/trace1_full_eval_sa_cfg_sa_ds_review_20260605_gpu1
```

## 指标汇总

指标来自 MotionCLR official evaluator。同一 baseline 内，FID、Matching 越低越好；Top1/Top2/Top3、Diversity、MultiModality 通常越高越好。Top1/Top2/Top3 均来自原始 `metrics_summary.json`，不是事后估算。

| Family | N | FID mean | Best FID | Best FID layer | Top1 mean | Top2 mean | Top3 mean | Best Top1 | Best Top1 layer | Best Top2 | Best Top2 layer | Best Top3 | Best Top3 layer | Matching mean | Diversity mean | MultiModality mean | Median min |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| baseline | 2 | 0.1268 | 0.1268 | NA | 0.4437 | 0.6435 | 0.7562 | 0.4437 | NA | 0.6435 | NA | 0.7562 | NA | 3.4182 | 8.4674 | 2.3566 | 7.34 |
| SA | 18 | 0.2519 | 0.1134 | 2 | 0.4377 | 0.6400 | 0.7507 | 0.4450 | 5 | 0.6468 | 1 | 0.7616 | 11 | 3.4574 | 8.4290 | 2.3420 | 7.18 |
| CA | 18 | 0.1383 | 0.1085 | 13 | 0.4400 | 0.6416 | 0.7538 | 0.4496 | 1 | 0.6517 | 1 | 0.7582 | 11 | 3.4350 | 8.4662 | 2.3750 | 7.30 |
| CFG_SA | 18 | 0.1492 | 0.1114 | 3 | 0.4406 | 0.6424 | 0.7532 | 0.4446 | 1 | 0.6481 | 3 | 0.7578 | 5 | 3.4276 | 8.4758 | 2.3679 | 7.18 |
| CFG_CA | 18 | 0.7025 | 0.1198 | 5 | 0.3793 | 0.5619 | 0.6662 | 0.4442 | 6 | 0.6455 | 16 | 0.7567 | 17 | 4.0675 | 8.3083 | 3.0028 | 7.36 |

## 层趋势视图

![MotionCLR FID layer trend](../visualization/figures/motionclr_fid.svg)

![MotionCLR Top1 layer trend](../visualization/figures/motionclr_top1.svg)

![MotionCLR Top2 layer trend](../visualization/figures/motionclr_top2.svg)

![MotionCLR Top3 layer trend](../visualization/figures/motionclr_top3.svg)

FID trend，越低越好：

```text
SA     00:.622 01:.115 02:.113 03:.143 04:.128 05:.127 06:.127 07:.127 08:.126 09:.126 10:.129 11:.123 12:.175 13:.296 14:1.323 15:.480 16:.127 17:.127
CA     00:.177 01:.130 02:.117 03:.154 04:.129 05:.127 06:.127 07:.127 08:.126 09:.126 10:.130 11:.132 12:.163 13:.109 14:.168 15:.193 16:.127 17:.127
CFG_SA 00:.127 01:.163 02:.125 03:.111 04:.127 05:.127 06:.127 07:.127 08:.127 09:.126 10:.126 11:.120 12:.211 13:.194 14:.273 15:.223 16:.127 17:.126
CFG_CA 00:.248 01:.347 02:.200 03:.320 04:.120 05:.120 06:.126 07:.126 08:.125 09:.125 10:.130 11:.140 12:1.316 13:1.138 14:4.443 15:3.369 16:.127 17:.127
```

Top3 trend，越高越好：

```text
SA     00:.742 01:.749 02:.752 03:.753 04:.757 05:.756 06:.757 07:.756 08:.758 09:.757 10:.756 11:.762 12:.746 13:.739 14:.720 15:.740 16:.757 17:.757
CA     00:.756 01:.753 02:.754 03:.755 04:.758 05:.757 06:.757 07:.757 08:.756 09:.756 10:.755 11:.758 12:.740 13:.754 14:.742 15:.748 16:.756 17:.757
CFG_SA 00:.756 01:.752 02:.755 03:.756 04:.758 05:.758 06:.758 07:.757 08:.757 09:.756 10:.755 11:.755 12:.753 13:.737 14:.735 15:.748 16:.757 17:.757
CFG_CA 00:.742 01:.699 02:.738 03:.732 04:.756 05:.755 06:.756 07:.757 08:.756 09:.755 10:.754 11:.754 12:.628 13:.630 14:.169 15:.100 16:.755 17:.757
```

## 解读备注

- MotionCLR 是三套 baseline 中审计链路最完整的一个，因为每层都记录 provenance、hook evidence 和 metric hashes。
- CFG_CA 在 12-15 层出现严重退化，是 MotionCLR 中最清楚的层局部敏感模式。
- SA、CA、CFG_SA 大多数层接近 baseline；SA/CFG_SA 后段有少量 FID spike。
- Baseline 出现在两个 GPU split roots 中，应视为同一 baseline 条件的重复证据，而不是两个独立实验条件。
