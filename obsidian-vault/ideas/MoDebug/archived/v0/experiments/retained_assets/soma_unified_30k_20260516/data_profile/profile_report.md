---
title: "SOMA Unified 30k 数据画像报告"
created: 2026-05-16T23:48:36
updated: 2026-05-17T16:36:06+08:00
type: dataset_profile
---

# SOMA Unified 30k 数据画像报告

## 目标

统计 SOMA/KIMODO/SEED metadata 经过筛选后的数量、分布和 split，为后续 MoMask/MoGenTS 训练前置检查提供依据。

## 数据对象

- metadata rows: `142220`
- temporal rows: `142220`
- eligible rows: `58281`
- selected rows: `30000`

## 计算方式

筛选条件：original、text-present、temporal-label-present、40<=estimated_20fps_frames<200、SOMA uniform path present。split 使用 80/10/10，并按 source identity 去重防泄漏。

## 统计结果

- split_counts: `{'test': 3000, 'train': 24000, 'val': 3000}`
- selected_event_count_distribution: `{'1': 7846, '2': 11057, '3': 8363, '4': 2214, '5': 431, '6': 73, '7': 12, '8': 2, '9': 2}`
- selected_duration_20fps_quantiles: `{'0': 40.0, '0.1': 58.0, '0.25': 75.0, '0.5': 102.0, '0.75': 135.0, '0.9': 166.0, '1': 199.0}`
- selected_caption_word_count_quantiles: `{'0': 5.0, '0.1': 7.0, '0.25': 8.0, '0.5': 10.0, '0.75': 14.0, '0.9': 17.0, '1': 30.0}`

## 结论

当前已获得 30k caption-motion pair manifest 和 split。该结果只证明 metadata selection 完成，不证明特征转换、loader 可用或模型训练完成。

## 元数据

- date: `2026-05-17`
- experiment_path: `paperIDEAs/MoDebug/experiments/soma_unified_30k_20260516`
- evaluator: `modebug_build_soma_unified_30k_manifest`
- protocol: `metadata-only KIMODO/SEED profile and DS-reviewed 30k caption-motion pair selection`
- data_source: KIMODO/SEED metadata、temporal labels、SOMA uniform path
- condition_pair: `not_applicable`
- n/evaluable: `30000/30000`
- coverage: metadata selection and split
- role: `diagnostic`
- used_for: `selection`
- limitations: metadata-selected manifest only；未验证 MoMask/MoGenTS feature conversion 和 loader smoke。
