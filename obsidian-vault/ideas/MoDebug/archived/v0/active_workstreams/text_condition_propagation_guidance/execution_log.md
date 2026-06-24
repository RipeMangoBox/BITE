---
title: "MoDebug text-condition propagation 执行日志"
created: 2026-05-28T16:40:00+08:00
updated: 2026-05-28T16:40:00+08:00
status: active
tags:
  - MoDebug
  - execution_log
  - text_condition_propagation
---

# MoDebug text-condition propagation 执行日志

## 2026-05-28 — 目录整合与任务入口统一

**task**: 整合 `text_condition_propagation_guidance/` 与 `implementation_20260527/` 的双入口问题。

**decision**: 采用 DeepSeek max 多轮审查后的阶段一方案：父目录作为唯一正文根目录，2026-05-27 实现目录归档为 `_archive_20260527/`，暂留 `implementation_20260527 -> _archive_20260527` symlink 兼容旧路径。不移动 Python 代码、reports 或 visualizations，避免破坏导入和相对路径。

**changed_files**:
- `README.md`
- `TASK_BOARD.md`
- `QUICKSTART.md`
- `execution_log.md`
- `_archive_20260527/README_ARCHIVED.md`

**artifact_path**:
- `_archive_20260527/`
- `implementation_20260527` symlink

**result**:
- 已建立统一正文入口和任务板。
- 已把核心科学问题写入 README 与 TASK_BOARD：从 aggregate 统计到 sample-level 证据回查，再到可反驳机制假设和最小干预实验。
- 已把 MoLingo mask 与可视化文字重叠列为明确任务。

**limitations**:
- 当前仍保留兼容 symlink，因此 `rg implementation_20260527` 可能出现历史计划和兼容说明；这些需要人工区分是否为真实死链。
- 代码物理整合尚未执行，需待脚本导入和输出路径检查后再决定。

**next_action**: 已完成。见后续条目。

## 2026-05-28 — 可视化路径修复与文字重叠验证

**task**: 修复可视化脚本输出路径，重新生成全部 SVG，验证文字重叠已解决。

**changed_files**:
- `scripts/modebug_visualize_time_feature_delta_mass.py`: OUT_DIR 改为 `_archive_20260527/visualizations`
- `scripts/modebug_visualize_text_condition_sample_level.py`: OUT_DIR 已在之前改为 `_archive_20260527/visualizations`
- 重新生成全部 SVG 到 `_archive_20260527/visualizations/`

**result**:
- 两个脚本均成功运行，输出到归档路径。
- `case_cards.svg` 已使用 `text_lines`/`middle_shorten` 实现多行文本换行和路径截断，长 prompt (如 "a person does a quick wheel-like spin kick...") 正确换行，motion path 使用中间省略。
- `per_timestep_delta_l2.svg` 和 `time_feature_delta_mass.svg` 文字间距已在上一轮修复。

**limitations**:
- `modebug_visualize_text_condition_sample_level.py` 仍会生成旧的 `sample_level_*` 前缀文件（mogents_time_grid_mass, time_delta_curves, success_failure_delta_bar），这些是冗余产物但归档无害。

**next_action**:
- MoLingo mask 在可视化中的处理（见下一节）。

## 2026-05-28 — MoLingo valid_mask 审计

**task**: 追踪 MoLingo valid_mask 在全链路中的写出和消费。

**method**: Explore agent 审计了 runner、validator、visualization 三处的 mask 逻辑。

**findings**:

1. **写出** (`run_molingo_sample_trace.py` + `sample_trace_utils.py`): `valid_mask = ~key_padding_mask`。MoLingo 用固定 49 token 的 latent sequence，仅前 `floor(frame_length/unit_length)` 个 token 有效，其余为 padding。mask 正确写入 forward NPZ。

2. **delta 计算** (`trace_contract_validator.py`): 正确使用 text/null 两个 forward mask 的交集，`delta[~valid_mask] = 0.0`。scalar metric 只在 valid positions 上计算——正确。

3. **可视化** (`modebug_visualize_time_feature_delta_mass.py`): **完全忽略 valid_mask**。`compute_time_feature_mass()` 和 `write_bar_charts()` 均未接受或使用 mask 参数。后果：
   - padded tokens (26/49 for success, 11/49 for failure) 在 heatmap 中显示为零值列，与真实低 delta 区域不可区分
   - per-timestep L2 bar chart 的 y 轴被零值 bar 压缩，稀释真实信号

4. **valid_ratio confound**: MoLingo success valid_ratio=0.469 (23 valid), failure valid_ratio=0.776 (38 valid)。Failure 有更多有效 token → 更大的 metric 可能仅因为更多 token 参与了 metric 计算，而非每个 token 上的 text effect 更强。

**required_changes**: 已完成。见下一节。

## 2026-05-28 — MoLingo mask 可视化修复 (P2 完成)

**task**: 在 `modebug_visualize_time_feature_delta_mass.py` 中实现 mask-aware 计算。

**changed_files**:
- `scripts/modebug_visualize_time_feature_delta_mass.py`: `compute_time_feature_mass()` 和 `write_bar_charts()` 均已接受 valid_mask，对 3D/4D 张量自动处理 mask 降维，仅对 valid timesteps 计算。MoLingo panel 标题中红色 `valid_ratio=X.XX` 标注已生效。

**result**:
- 脚本重新生成 confirmed 通过。MoLingo heatmap 和 bar chart 不再包含 padding token 的零值列。
- 其他模型（valid_ratio=1.0）不受影响。

**limitations**:
- mask-aware 计算依赖 `trace_contract_validator.py` 已将 delta[~valid_mask] 置零。可视化脚本显式使用 mask 而非依赖 zeroing，已解耦。
- valid_ratio confound（failure 0.78 vs success 0.47）仍需在 400-sample 数据上进一步验证。

## 2026-05-28 — Batch wrapper + analysis stubs (P3+P4 骨架完成)

**task**: 创建 batch trace orchestrator 和 4 个 analysis pipeline skeleton。

**changed_files** (5 new scripts under `scripts/`):
- `modebug_batch_sample_trace.py` — 读取 sample CSV，生成 per-sample JSON config + batch manifest
- `modebug_descriptive_stats.py` — 读取 delta_tensor_summary.json，输出 per-model×outcome 描述统计 CSV（已用 8-case pilot 测试通过）
- `modebug_cluster_analysis.py` — PCA + k-means 聚类骨架（需 conda python + numpy）
- `modebug_outcome_classifier.py` — RF/SHAP 分类器骨架（支持 sklearn fallback）
- `modebug_prompt_analysis.py` — prompt NLP 特征提取（已测试：正确识别 while→parallel, then→sequential）

**result**:
- 全部 5 个脚本 `--help` 正常，已用 pilot 数据测试 `descriptive_stats` 和 `prompt_analysis` 通过。
- 400-sample 数据到位后可直接填充 placeholder 计算逻辑。

**artifact_path**: `scripts/modebug_batch_sample_trace.py` 等

**next_action**: 在 4090 上运行批量 trace；400-sample 数据到位后填充 analysis skeleton。

## 2026-05-28 — Gradio human eval 定位

**task**: 用户提到 400 sample human eval 已有 Gradio app，需找到而非重建。

**finding**: 
- 现有 app: `scripts/modebug_original100_four_baseline_vis_review_app.py`
- 启动脚本: `MoDebug_original100_four_baseline_vis_gradio.sh`（端口 7865）
- 数据源: `obsidian-vault/paperIDEAs/MoDebug/experiments/active/full_text_full_motion_plugin_eval_20260520/`
- 已有 human annotation 输出: `eval/original100_four_baseline_vis_review_20260525/`

**decision**: 不创建新的 Gradio app。现有 app 已产出当前 8-case pilot 使用的 human annotation。
- `write_bar_charts()`: 使用 valid_mask 截断 delta 数据，只绘制 valid timesteps
- 两个函数应显式接受 mask 而非依赖 validator 的 zeroing（解耦）

**decision**: MoLingo mask 修复列为 P2，需改 `modebug_visualize_time_feature_delta_mass.py`。

**next_action**:
- 实现 mask-aware 可视化
- 在 heatmap 标题中标注 `valid_ratio`
- 全类型路径引用搜索完成后再统一更新执行日志
