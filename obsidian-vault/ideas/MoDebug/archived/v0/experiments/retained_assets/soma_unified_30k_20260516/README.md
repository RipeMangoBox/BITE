---
title: "SOMA Unified 30k 实验总览"
created: 2026-05-16T23:48:36
updated: 2026-05-19T15:25:31+08:00
type: experiment_readme
tags:
  - MoDebug
  - SOMA
  - KIMODO
  - dataset
---

# SOMA Unified 30k 实验总览

## 目标

从 SOMA/KIMODO/SEED 相关 metadata 中构造约 3 万条 text-motion 数据 manifest，并记录 MoMask/MoGenTS 训练前置条件。当前目标是数据构造和 provenance，不声称训练效果。

## 数据对象

- 单位：`caption-motion pair`，不是 event-level pair。
- 输入来源：KIMODO/SEED metadata、temporal labels、SOMA uniform BVH path。
- 选择结果：`30000` 条 selected rows。
- split：train/val/test = `{'test': 3000, 'train': 24000, 'val': 3000}`。

## 计算方式

- 过滤 original、text-present、temporal-label-present、40<=estimated_20fps_frames<200、SOMA uniform path present 的 metadata rows。
- 固定 seed `20260516`，按 source identity 分组 split，避免同源 motion 跨 split 泄漏。
- 记录 manifest/split hash、DS review、remote4090 preflight、4090 raw BVH text-motion 构造结果和 training blockers。

## 当前结论

- 已生成 `selected_30k_manifest.tsv/jsonl` 和 train/val/test split。
- event_count 分布：`{'1': 7846, '2': 11057, '3': 8363, '4': 2214, '5': 431, '6': 73, '7': 12, '8': 2, '9': 2}`。
- 20fps frame quantiles：`{'0': 40.0, '0.1': 58.0, '0.25': 75.0, '0.5': 102.0, '0.75': 135.0, '0.9': 166.0, '1': 199.0}`。
- caption word count quantiles：`{'0': 5.0, '0.1': 7.0, '0.25': 8.0, '0.5': 10.0, '0.75': 14.0, '0.9': 17.0, '1': 30.0}`。
- 4090 已按本地 split 构造 raw BVH + full text 数据集：`30000/30000` motion symlinks，`30000/30000` text files，missing motion 为 `0`。
- KIMODO/HumanML3D 转换 smoke 已通过：`6/6` 条 SOMA BVH 使用 KIMODO 官方 `convert_motion_files` 转为 Kimodo NPZ，再映射生成 HumanML3D 263D `new_joint_vecs`，loader smoke 为 `pass`。
- 20fps gate 已通过：`6/6` 20fps smoke 与 `12/12` 20fps regression 均通过，最终帧数回到 HumanML3D/MoMask/MoGenTS loader 使用的 20fps 长度范围。
- 全量 30k 20fps HumanML3D-263 转换已在 4090 完成：`29998/30000` rows converted；2 条 train 样本因 `Non-finite feature or recovered joint value` 失败。
- 原始 full conversion 目录的 loader smoke 未通过：7 条 train 样本为 `(39, 263)`，低于 MoGenTS/HumanML3D loader 的 `min_motion_len=40` 门槛。
- 已创建 clean_min40 训练视图：`29991` 条 finite samples，train/val/test = `23991/3000/3000`，Mean/Std 在 clean train split 上重算。
- MoGenTS VQ 训练已在 4090 GPU0 启动：tmux `soma30k_mogents_vq_gpu0_20260518`，实验名 `soma30k_clean_min40_rvq6_bs128_20260518`，训练循环已进入 `ep/it: 0-*`。
- MoMask masked/residual transformer 已完成训练，并已在 SOMA test 与 official HumanML3D test 上完成 20-repeat 官方 eval；结果见 `eval/momask_soma_hml3d_eval_summary_20260519.md`。

> [!warning] 训练边界
> MoGenTS VQ 训练只说明 clean_min40 数据视图已通过启动门槛，不是模型效果结论。MoMask 已完成 VQ、masked transformer、residual transformer 训练并完成 SOMA/HumanML3D official eval；MoGenTS transformer 训练仍需等待 VQ checkpoint 产出后再接。

## 阅读入口

| 文件 | 作用 |
|---|---|
| `data_profile/profile_report.md` | 数据筛选统计和分布。 |
| `manifests/dataset_card.md` | 数据卡、split、hash。 |
| `provenance/ds_review.md` | DS 对筛选和训练 gate 的审查。 |
| `provenance/training_status.md` | 4090 训练前置状态和 blocker。 |
| `eval/momask_soma_hml3d_eval_summary_20260519.md` | MoMask SOMA/HumanML3D test eval 与 KIMODO/MoMask paper 对照。 |
| `remote4090_build/README.md` | 4090 raw BVH text-motion 数据集构造结果，本地未覆盖原始 split。 |
| `../../../../artifacts/remote4090/remote4090_soma30k_clean_train_20260518/soma30k_clean_train_20260518/clean_min40_report.json` | clean_min40 训练视图报告和 Mean/Std hash。 |
| `../../../../artifacts/remote4090/remote4090_soma30k_clean_train_20260518/soma30k_clean_train_20260518/soma30k_mogents_vq_gpu0_20260518.log` | MoGenTS VQ 启动与训练日志副本。 |
| `humanml3d_smoke_20260517/reports/smoke_report.md` | KIMODO/HumanML3D 转换闭环 smoke 报告。 |
| `humanml3d_smoke_20fps_20260517/reports/smoke_report.md` | 20fps gate smoke 报告。 |
| `humanml3d_smoke_20260517/vis/` | recover 后的 22 关节静态可视化面板。 |
| `remote4090_build/manifests/selected_30k_text_motion_manifest.tsv` | 带远程 text/BVH 路径的 30k manifest。 |
| `manifests/selected_30k_manifest.tsv` | 选中的 30k manifest。 |
| `split/train.tsv`, `split/val.tsv`, `split/test.tsv` | 数据划分。 |

## 限制

- 原始 full conversion 目录保留不改；可训版本是过滤 7 条 too-short train samples 后的 clean_min40 视图。
- 2 条原始 selected rows 未能转换为 HumanML3D-263；7 条转换成功但长度为 39，未纳入 clean_min40 训练视图。
- MoMask 已通过临时同步的 remote repo 完成 VQ、masked transformer、residual transformer 训练；当前 eval 使用 masked `latest.tar` 与 residual `net_best_fid.tar`，详见 eval summary。
- 当前 MoGenTS VQ 是训练进行中状态，不是完成状态；日志中的 Ep 0/FID/Top-k 只作为启动期诊断，不作为正式效果指标。
