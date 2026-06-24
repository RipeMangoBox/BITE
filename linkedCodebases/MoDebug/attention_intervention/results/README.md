# Results

| 文件 | 内容 |
|---|---|
| [summary.md](summary.md) | 综合完成矩阵、审计矩阵、运行时间对比、主要发现、跨模型 late CFG_CA 结论。 |
| [motionclr.md](motionclr.md) | MotionCLR 的状态、审计证据、指标汇总和层趋势。 |
| [motiongpt.md](motiongpt.md) | MotionGPT 的状态、SA/CA 结果和 CFG unsupported 说明。 |
| [molingo.md](molingo.md) | MoLingo 旧结果作废原因、official-setting 代表层完整结果和 `CFG_CA/layer_15` 退化。 |
| [ldo_dso.md](ldo_dso.md) | LDO/DSO formal 诊断状态、MotionCLR DSO formation curve、MoLingo LDO proxy。 |
| [data_analysis_and_mechanism_discussion_20260609.md](data_analysis_and_mechanism_discussion_20260609.md) | 数据解释边界、证据等级和机制设计建议。 |

MoLingo 20260609 official rerun 已完成。关键结论是 MotionCLR 与 MoLingo 均出现 late `CFG_CA` 退化；机制成因仍需 cond/uncond 诊断验证。
