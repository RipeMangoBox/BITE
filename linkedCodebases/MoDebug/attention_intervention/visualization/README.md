# Visualization

本目录用零依赖 Python 脚本把有效结果转成 CSV 和 SVG 图。Attention official evaluator 与 LDO/DSO 诊断分开生成，避免混淆性能指标和 diagnostic proxy。

## 生成命令

```bash
python3 linkedCodebases/MoDebug/attention_intervention/visualization/build_attention_visualizations.py
python3 linkedCodebases/MoDebug/attention_intervention/visualization/build_ldo_dso_visualizations.py
```

## 输入数据

| 路径 | 内容 |
|---|---|
| `data/source_metrics_20260605.json` | MotionCLR/MotionGPT 20260605 formal roots 导出的有效 attention intervention 数据。 |
| `data/source_metrics_20260609_molingo.json` | MoLingo 20260609 official-setting representative metrics，含 `CFG_CA/layer_15`。 |
| `data/source_ldo_dso_20260608.json` | Formal LDO/DSO 状态、MotionCLR DSO metrics、MoLingo LDO decoded-array proxy。 |

## 输出

| 路径 | 内容 |
|---|---|
| `data/family_summary.csv` | 每个 baseline/family 的 attention 汇总指标，含 Top1/Top2/Top3 和状态。 |
| `data/layer_metrics.csv` | 每个 baseline/family/layer 的 FID/FID_TMR 与 Top1/Top2/Top3。 |
| `data/ldo_dso_status.csv` | 三个 baseline 的 LDO/DSO formal 状态矩阵。 |
| `data/motionclr_dso_metrics.csv` | MotionCLR DSO endpoint metrics。 |
| `data/molingo_ldo_metrics.csv` | MoLingo LDO seed/block endpoint diagnostic metrics。 |
| `data/molingo_ldo_block_summary.csv` | MoLingo LDO 按 block 聚合的诊断指标。 |
| `figures/family_runtime_median.svg` | 各 baseline/family 单层中位运行时间。 |
| `figures/*_fid*.svg` | 各 baseline 的 layer FID/FID_TMR 趋势。 |
| `figures/*_top1.svg` / `*_top2.svg` / `*_top3.svg` | 各 baseline 的 layer R-Precision 趋势。 |
| `figures/motionclr_dso_*.svg` | MotionCLR DSO formation curves。 |
| `figures/molingo_ldo_*.svg` | MoLingo LDO diagnostic endpoint difference plots。 |

## 图像

这些 SVG 同时嵌入在 `../results/summary.md` 和各报告中。

![Runtime median](figures/family_runtime_median.svg)

![MotionCLR FID](figures/motionclr_fid.svg)

![MotionGPT FID](figures/motiongpt_fid.svg)

![MoLingo FID_TMR](figures/molingo_fid_tmr.svg)

![MotionCLR DSO FID](figures/motionclr_dso_fid.svg)

![MoLingo LDO L2](figures/molingo_ldo_l2_vs_baseline.svg)

MoLingo `CFG_CA/layer_15` 已包含在 `data/source_metrics_20260609_molingo.json`。源数据变化后重跑两个生成命令即可刷新 CSV/SVG。
