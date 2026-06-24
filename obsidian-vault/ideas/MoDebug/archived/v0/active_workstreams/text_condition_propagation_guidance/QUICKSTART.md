---
title: "MoDebug text-condition propagation 快速命令"
created: 2026-05-28T16:40:00+08:00
updated: 2026-05-28T16:40:00+08:00
status: active
tags:
  - MoDebug
  - quickstart
  - text_condition_propagation
---

# MoDebug text-condition propagation 快速命令

## 工作目录

从 ResearchFlow 仓库根目录执行命令：

```bash
cd "/data/Life Me/ResearchWY Vault"
```

正文根目录：

```text
obsidian-vault/paperIDEAs/MoDebug/active/text_condition_propagation_guidance/
```

2026-05-27 实现快照：

```text
obsidian-vault/paperIDEAs/MoDebug/active/text_condition_propagation_guidance/_archive_20260527/
```

旧路径 `implementation_20260527/` 暂时是指向 `_archive_20260527/` 的兼容 symlink。新记录和新引用应使用 `_archive_20260527/` 或父目录正文入口。

## 结构检查

```bash
find "obsidian-vault/paperIDEAs/MoDebug/active/text_condition_propagation_guidance" -maxdepth 2 -type f | sort
ls -la "obsidian-vault/paperIDEAs/MoDebug/active/text_condition_propagation_guidance"
```

检查旧路径残留：

```bash
rg -n "implementation_20260527" "obsidian-vault/paperIDEAs/MoDebug/active/text_condition_propagation_guidance"
```

## 归档脚本

归档内现有工具：

```text
_archive_20260527/trace_adapters/
_archive_20260527/trace_metrics/
_archive_20260527/sync_index/
```

脚本运行前先看参数：

```bash
python "obsidian-vault/paperIDEAs/MoDebug/active/text_condition_propagation_guidance/_archive_20260527/trace_metrics/trace_contract_validator.py" --help
python "obsidian-vault/paperIDEAs/MoDebug/active/text_condition_propagation_guidance/_archive_20260527/sync_index/build_manifest_index.py" --help
```

## 可视化任务

8-case pilot 可视化产物：

```text
_archive_20260527/visualizations/case_cards.svg
_archive_20260527/visualizations/per_timestep_delta_l2.svg
_archive_20260527/visualizations/time_feature_delta_mass.svg
```

可视化脚本记录在 [[provenance|provenance]]。修复文字重叠时，优先修改生成脚本并重新导出，不直接手工修改 SVG。

## 记录要求

每次执行任务后更新 [[execution_log|execution_log]]，至少记录：

- date
- task
- command
- changed_files
- artifact_path
- result
- limitations
- next_action
