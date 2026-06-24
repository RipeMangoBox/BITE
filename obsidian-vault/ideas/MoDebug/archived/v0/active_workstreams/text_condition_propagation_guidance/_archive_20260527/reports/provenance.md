---
title: "Trace 实验溯源"
created: 2026-05-28T15:40:00+08:00
status: reference
---

# Trace 实验溯源

## 远端

```text
4090:/data/public/ripemangobox/Motion/EventT2M-codes/artifacts/modebug/text_condition_sample_level_20260528/
```

## 本地 artifact

```text
artifacts/remote/4090/modebug_text_condition_sample_level_20260528/text_condition_sample_level_20260528/
```

## 启动脚本

```text
scripts/modebug_launch_text_condition_sample_level_remote.py
```

## 可视化脚本

```text
scripts/modebug_visualize_text_condition_sample_level.py  # case cards + summary CSV
scripts/modebug_visualize_time_feature_delta_mass.py       # heatmaps + bar charts
```

## 关键索引

```text
index_outputs/sample_case_index.tsv    # 8 row, 完整 P3 证据链
index_outputs/sample_case_index.jsonl  # 同上, JSONL
index_outputs/manifest_index.tsv       # 24 row, forward/delta manifest
logs/validate_sample_level_traces.log  # 远端验证输出
```

## 协议摘要

- date: `2026-05-28`
- evaluator: `trace_contract_validator.py` + `build_manifest_index.py`
- protocol: per-baseline success/failure case, paired text vs null_text forward, 固定内部随机状态
- motion_source: Original100 four-baseline rendered MP4 + human diagnostic annotations
- condition_pair: `text_vs_null`
- coverage: 8 cases = 4 baseline × 2 outcomes; 16 forward NPZ; 8 delta NPZ
- role: `diagnostic`, used_for: `observation`
