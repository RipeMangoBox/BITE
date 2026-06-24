---
title: "SOMA Unified 30k 4090 构造结果"
created: 2026-05-17T16:55:00+08:00
updated: 2026-05-17T16:55:00+08:00
type: remote_dataset_build_readme
tags:
  - MoDebug
  - SOMA
  - remote4090
---

# SOMA Unified 30k 4090 构造结果

## 目标

记录 4090 上按本地 30k manifest/split 构造 raw BVH + full text 数据集的结果，并说明本地拉回文件如何使用。

## 数据对象

- 本地输入：`manifests/selected_30k_manifest.tsv`、`split/train.tsv`、`split/val.tsv`、`split/test.tsv`。
- 远程 SOMA 根目录：`/data/public/ripemangobox/Motion/datasets/soma_uniform`。
- 远程输出数据集：`/data/public/ripemangobox/Motion/datasets/soma_unified_30k_20260516/text_motion_dataset`。
- 本地拉回目录：`paperIDEAs/MoDebug/experiments/soma_unified_30k_20260516/remote4090_build/`。

## 计算方式

远程脚本读取上传后的 manifest/split，逐条生成 full text 文件，并把 SOMA BVH 以 symlink 方式挂到 `motions_bvh/`。本地只拉回 manifest、split list、hash、status 和日志，不复制 3 万个 BVH/text 文件本体，也不覆盖本地已有 `manifests/` 和 `split/`。

## 结论

- n/evaluable: `30000/30000 motion symlinks; 30000/30000 text files`
- missing_motion_rows: `0`
- split_counts: `train=24000, val=3000, test=3000`
- source_identity leakage_overlap: `none`
- input_hash_check_ok: `true`

## 文件说明

| 文件夹 | 作用 |
|---|---|
| `manifests/` | 带远程 text/BVH 路径的 30k text-motion manifest 和 train/val/test 子 manifest。 |
| `splits/` | 远程数据集使用的 sample_id split list。 |
| `provenance/` | build summary、input hash check、output hashes、build status。 |
| `logs/` | remote4090 tmux 运行日志。 |

## 限制

这是 raw BVH text-motion 数据集，不是 HumanML3D-263 feature 数据集。MoMask/MoGenTS 真正训练前仍需完成 BVH-to-HumanML3D 转换、skeleton/fps/normalization 记录、mean/std、loader smoke 和小训练 smoke。
