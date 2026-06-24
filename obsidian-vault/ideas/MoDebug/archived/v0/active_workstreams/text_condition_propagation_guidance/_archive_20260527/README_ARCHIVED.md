# 2026-05-27 实现快照（已归档）

> [!warning] 归档说明
> 本目录是 2026-05-27 text-condition propagation trace 的实现快照。后续正文入口、任务推进和执行记录统一在父目录 [[ideas/MoDebug/active/text_condition_propagation_guidance/README|text_condition_propagation_guidance]] 中维护。本目录内容暂时保留原位，避免破坏脚本导入、报告引用和历史复现路径。

# implementation_20260527 — text-condition propagation trace

对 4 个 motion generation baseline 做 sample-level text vs null_text forward trace，
观测 text embedding 在模型内部特征空间的传播效应。

## 目录

| 目录                | 职责                                                 |
| ----------------- | -------------------------------------------------- |
| `trace_adapters/` | 模型特定的 forward trace adapter，负责 hook 模型内部层并写出标准 NPZ |
| `trace_metrics/`  | delta 计算（text vs null_text 差值）和 contract 校验        |
| `sync_index/`     | manifest 索引构建和远端/本都同步校验                            |
| `reports/`        | 运行报告、分析方案、IO contract                              |
| `visualizations/` | 所有 SVG 图表和底层数据 CSV/JSON                            |

## 数据流

```
trace_adapters (hook model → forward NPZ)
    ↓
trace_metrics (pair text/null → delta NPZ → validate)
    ↓
sync_index (build manifest index → validate integrity)
    ↓
reports + visualizations (generate SVG + CSV → human review)
```
