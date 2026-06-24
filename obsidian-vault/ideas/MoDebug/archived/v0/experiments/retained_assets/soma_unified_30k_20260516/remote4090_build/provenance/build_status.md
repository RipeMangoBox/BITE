---
title: "SOMA 30k 4090 文本动作数据集构造状态"
created: 2026-05-17T16:47:14+08:00
updated: 2026-05-17T16:47:14+08:00
type: dataset_build_status
---

# SOMA 30k 4090 文本动作数据集构造状态

## 目标

按照本地 30k manifest/split，在 4090 上构造 raw BVH + full text 的 text-motion 数据集。

## 数据对象

- manifest rows: `30000`
- split_counts: `{'test': 3000, 'train': 24000, 'val': 3000}`
- source_soma_root: `/data/public/ripemangobox/Motion/datasets/soma_uniform`
- output_dataset_root: `/data/public/ripemangobox/Motion/datasets/soma_unified_30k_20260516/text_motion_dataset`

## 计算方式

读取上传到 4090 的 `selected_30k_manifest.tsv` 和 train/val/test split，逐条生成文本文件，并把 remote SOMA BVH 以 symlink 方式挂到 `motions_bvh/`。同时生成 split list、带远程路径的 text-motion manifest、缺失运动报告和 hash。

## 结论

- n/evaluable: `30000/30000 motion symlinks; 30000/30000 text files`
- missing_motion_rows: `0`
- symlink_status: `{'ok_symlink_created': 30000}`
- input_hash_check_ok: `True`
- leakage_overlap: `none`

## 限制

这是 raw BVH text-motion 数据集，不是 HumanML3D-263 feature 数据集。后续训练前仍需 BVH-to-HumanML3D 转换、skeleton/fps/normalization 记录、loader smoke 和小训练 smoke。
