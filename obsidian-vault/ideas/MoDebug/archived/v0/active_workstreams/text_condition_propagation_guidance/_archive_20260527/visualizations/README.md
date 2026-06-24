# visualizations

所有图表和数据由 `scripts/` 下的两个脚本生成。

## 图表

| 文件 | 内容 | 生成脚本 |
|------|------|----------|
| [case_cards.svg](case_cards.svg) | 每 case 的 metadata card，作为 P3 证据索引 | `modebug_visualize_text_condition_sample_level.py` |
| [per_timestep_delta_l2.svg](per_timestep_delta_l2.svg) | 2x2 grid，每 baseline success vs failure 逐时间步 delta L2 柱状图 | `modebug_visualize_time_feature_delta_mass.py` |
| [time_feature_delta_mass.svg](time_feature_delta_mass.svg) | 4 行热力图，每行 success/failure 各一个 time × feature_bin delta mass heatmap | `modebug_visualize_time_feature_delta_mass.py` |

## 数据

| 文件 | 内容 |
|------|------|
| `trace_summary.csv` | 8 row，每 case 的 model/outcome/sample_id/metric_value/delta_shape |
| `frame_delta_l2.csv` | 每个时间步的 delta L2 值展开 |
| `delta_tensor_summary.json` | 每 case 的完整 delta 张量统计 (abs_max, mean, std, valid_ratio, axis_names ...) |
| `visualization_metadata.json` | 图表元信息 (source_root, role, limitations) |
