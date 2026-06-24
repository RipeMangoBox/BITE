---
title: "SOMA Unified 30k 数据卡"
created: 2026-05-16T23:48:36
updated: 2026-05-17T16:36:06+08:00
type: dataset_card
---

# SOMA Unified 30k 数据卡

## 目标

记录 selected 30k manifest 的单位、split、hash 和使用边界。

## 数据对象

- unit: `caption-motion pair`
- selected_rows: `30000`
- split_counts: `{'test': 3000, 'train': 24000, 'val': 3000}`
- mirror_policy: `exclude`
- leakage_key: `take_date|take_name|take_actor|base_filename_without__M`

## 计算方式

从 eligible metadata rows 中抽取 30k 条，保留 full text + full motion sequence path，按 source identity 分组做 80/10/10 split，并计算 sha256。

## 哈希

```json
{
  "selected_30k_manifest.tsv": "e07963cde7e86b2db43a264237ef533954e6e703f659a82eda88d5e7393c57ac",
  "selected_30k_manifest.jsonl": "f294a98950c3868112498878fe977df56259be085e0001df219675eec5fba74c",
  "split_manifest.tsv": "e07963cde7e86b2db43a264237ef533954e6e703f659a82eda88d5e7393c57ac",
  "train.tsv": "287ef7a24a55166be3caf86ec8c0a2f91653f13fa26536616589abc826bfd519",
  "val.tsv": "6f3c1d0995fc17caedf00f960ed009f83c3190c332feceeac2ce806814a56a0d",
  "test.tsv": "bea225d3619e5d2e28a00ab31ad01086cd4f99e94d774c963b97b36a7f00f23f",
  "profile_stats.json": "aec0de3b22a73b03f1c2230792732cc274327c597a1feff9fb817d4897aa5ad7"
}
```

## 结论

manifest/split 已可复查，但训练前仍需要 HumanML3D-263 feature conversion、mean/std provenance、loader smoke 和小训练 smoke。

## 元数据

- date: `2026-05-17`
- experiment_path: `paperIDEAs/MoDebug/experiments/soma_unified_30k_20260516`
- evaluator: `modebug_build_soma_unified_30k_manifest`
- protocol: `DS-reviewed metadata selection for full text + full motion sequence`
- data_source: `KIMODO/SEED metadata + temporal labels + SOMA uniform BVH paths`
- condition_pair: `not_applicable`
- n/evaluable: `30000/30000`
- coverage: selected metadata and split
- role: `diagnostic`
- used_for: `selection`
- limitations: 数据卡不是训练结果，也不是 final evaluator。
