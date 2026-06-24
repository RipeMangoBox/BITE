---
title: "MoDebug text-condition propagation 当前任务板"
created: 2026-05-28T16:40:00+08:00
updated: 2026-05-28T16:40:00+08:00
status: active
tags:
  - MoDebug
  - task_board
  - text_condition_propagation
---

# MoDebug text-condition propagation 当前任务板

## 任务原则

本任务板是当前唯一执行入口。历史实现快照在 `_archive_20260527/`；旧路径 `implementation_20260527/` 仅作为兼容 symlink 暂留。

所有任务必须服务于核心闭环：

```text
aggregate 统计发现候选问题
  -> sample-level 证据回查
  -> 可反驳的机制假设
  -> 最小干预实验
```

trace delta 默认是 diagnostic / side signal，不是 final evaluator。

## P0 — 目录整合与执行口径

- [x] 以父目录 `text_condition_propagation_guidance/` 作为唯一正文根目录。
- [x] 将 2026-05-27 实现目录归档为 `_archive_20260527/`，不删除任何内容。
- [x] 暂留 `implementation_20260527 -> _archive_20260527` symlink，兼容旧路径。
- [x] 建立 `TASK_BOARD.md`、`QUICKSTART.md`、`execution_log.md`。
- [x] 全类型搜索 `implementation_20260527`，确认残留引用均为历史说明或兼容说明。
- [x] 修复 3 个 Python 脚本中的旧路径引用（`scripts/`），替换为 `_archive_20260527/`。
- [x] 从父目录运行两个可视化脚本的验证命令，确认输出到归档路径。

## P1 — 可视化文字重叠修复

- [x] 定位 `case_cards.svg`、`per_timestep_delta_l2.svg`、`time_feature_delta_mass.svg` 的生成脚本。
- [x] 优先修改生成脚本，不手工改 SVG。
- [x] 长路径、manifest、说明文本采用换行、截断或中间省略（`text_lines`/`middle_shorten` 已生效）。
- [x] 重新导出 SVG，并检查 Obsidian 阅读视图中标题、legend、说明、长文本不重叠。
- [x] 图中明确标注 sample-level diagnostic、不是 final evaluator；跨模型不可直接比较绝对值。

## P2 — MoLingo mask 问题处理

- [x] 定位 MoLingo forward/delta NPZ 的 `valid_mask` 写出与读取逻辑（已完成全链路审计）。
- [x] 明确 text/null 两个 forward 的有效 mask 交集作为 delta 统计 mask（`trace_contract_validator.py` 已正确实现）。
- [x] 修复 `modebug_visualize_time_feature_delta_mass.py`: `compute_time_feature_mass()` 和 `write_bar_charts()` 接受 valid_mask，仅对 valid timesteps 计算。
- [x] 所有 MoLingo 可视化输出同时标注 `valid_ratio` 和 coverage（SVG 中红色 valid_ratio=X.XX 标注）。
- [ ] 检查 `valid_ratio` 与 outcome / failure_factor 是否相关（需 400 sample 数据后执行）。
- [ ] 在机制假设中区分结构性稀疏 bottleneck 与真正的 text routing failure（需分析结果后执行）。

## P3 — 400 sample 批量扩展

- [x] 写 batch wrapper (`scripts/modebug_batch_sample_trace.py`)。
- [x] 在 4090 上实际运行 4 baseline × 100 sample 的批量 trace（GPU1, 144s 完成）。
- [x] 运行 `build_manifest_index.py`（1294 rows, 0 issues）。
- [x] Fetch 387/400 delta NPZ 回本地（13 MotionGPT cases rsync 遗漏，已补充）。
- [x] 汇总: 387 cases, 8 groups, 0 NaN/Inf, 0 shape mismatch。

## P4 — 分析闭环

- [x] Agent A: `modebug_descriptive_stats.py` 实测 387 cases, 8 groups CSV。
- [x] Agent D: `modebug_prompt_analysis.py` 实测 100 unique prompts, mean_length=74.5, mean_sub_actions=1.25。
- [x] Agent B: `modebug_cluster_analysis.py` 骨架就绪，需 conda python + full NPZ 数据。
- [x] Agent C: `modebug_outcome_classifier.py` 实测 387 samples, top feature = delta_mean (score=0.116)。
- [ ] sample-level case audit: 回看统计异常点、cluster 代表样本和 borderline samples。

## P5 — 机制设计与干预实验

- [ ] 根据统计和 sample audit 形成机制假设。
- [ ] 为每个机制假设记录最小干预、预期 delta 变化、预期 motion-level 改善和失败判据。
- [ ] 候选方向：text-motion balance gate、sparse text-to-feature routing、temporal consistency loss、early-decoding text bias injection、MoLingo valid-token sparse text injection。
- [ ] 增加 random text、semantic perturbation、partial text mask 控制条件后，再讨论语义特异性和因果敏感性。

## 关键文档

- [[ideas/MoDebug/active/text_condition_propagation_guidance/README|主线入口]]
- [[QUICKSTART|快速命令]]
- [[execution_log|执行日志]]
- [[GPT_HANDOFF|2026-05-27 实现快照交接]]
- [[analysis_plan_400_samples|400-sample 分析方案]]
- [[sample_level_trace_run_report|8-case pilot 运行报告]]
