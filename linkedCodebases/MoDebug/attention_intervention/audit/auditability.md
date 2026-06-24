# Attention Intervention 可审计性说明

## 审计口径

本文件只描述证据质量，不重算指标。正式数值位于 [../results/summary.md](../results/summary.md) 和各 baseline 独立报告。

| Baseline | Manifest 状态 | Provenance | Hook 证据 | Unsupported/blocked 处理 | 结论 |
|---|---:|---:|---:|---:|---|
| MotionCLR | 强 | 强 | 强 | LDO blocked 合理 | 审计链路最完整。 |
| MotionGPT | 强 | 强 | 良好 | CFG/LDO 均明确处理 | CFG_SA/CFG_CA 是显式 unsupported，不是漏跑。 |
| MoLingo | 强 | 强 | 强 | 旧 eval invalidated | 20260609 official-setting representative rerun 可作为正式结果。 |

## 证据组织

| 类别 | 应检查内容 |
|---|---|
| 运行状态 | `paper_level_status` 是否为 `full_evaluator_metrics_computed`，unsupported/blocked family 是否 fail-fast。 |
| 指标文件 | `metrics_summary.json` 是否存在且非空，是否来自 official evaluator。 |
| Provenance | command script、wrapper script、checkpoint hash、git head/status、dataset/evaluator path、layer mapping。 |
| Hook 证据 | `hook_call_counts`、replacement checks、CFG cond/uncond branch 处理路径。 |
| 架构阻断 | 无 CA 模块、无 paired CFG branch、或 hidden state 不能合法解码时，必须记录为 unsupported/blocked，而不是空缺指标。 |

## Baseline 备注

- MotionCLR：20260605 formal roots 完整，包含 hook call counts 和 replacement checks。20260604 outputs 不纳入最终聚合。
- MotionGPT：SA/CA 完成；CFG_SA/CFG_CA 已由 wrapper fail-fast 标记 unsupported。
- MoLingo：20260603/20260605 results 已 invalidated，原因是 `unit_length`、`cfg/acc` 与 official setting 不一致且缺少 hook/replacement 运行时证据。20260609 official-setting rerun 记录 `unit_length=2`、`cfg=5.5`、`acc=3` 和 hook/replacement checks。
- LDO/DSO：MotionCLR DSO 是 full evaluator diagnostic；MoLingo LDO 是 decoded-array proxy；MotionCLR/MotionGPT LDO blocked 属于正确的接口保护。

## 关键审计点

- MoLingo `CFG_CA/layer_15` manifest 为 `full_evaluator_metrics_computed`，hook/replacement counts 均为 6850，`missed_replacement=0`，`shape_mismatch=0`。
- MotionGPT CFG unsupported 不进入缺失统计。
- LDO/DSO 诊断结果不与 official attention evaluator 指标混合排名。
