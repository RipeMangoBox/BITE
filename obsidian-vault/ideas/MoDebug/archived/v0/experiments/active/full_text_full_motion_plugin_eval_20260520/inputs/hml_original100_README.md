---
title: "HML Original100 Inputs"
created: 2026-05-24T23:09:04+08:00
updated: 2026-05-24T23:09:04+08:00
type: experiment_input_record
tags:
  - MoDebug
  - HumanML3D
  - Original100
  - diagnostic
---

# HML Original100 Inputs

> [!abstract] 资产定位
> 这批输入是 MoDebug 的 `failure_bank_v1` 诊断扩展：100 条 HumanML3D original full-motion captions，其中 80 条来自 train source split，20 条来自 test source split。它不是 benchmark、不是 final test set，也不是数据集贡献。

## 文件

- `hml_original100_sample_manifest.tsv`：主 manifest，100 行，含 split、caption provenance、GT motion path、bucket、role、limitations。
- `hml_original100_prompts_with_ids.tsv`：baseline generation 用 prompt 表，保留 `prompt_id` 和 `sample_id`。
- `hml_original100_prompts.txt`：纯 prompt 列表，供只接受文本列表的 runner 使用。
- [[hml_original100_selection_run_record.json|hml_original100_selection_run_record.json]]：选择策略、筛选条件、hash 和限制。

生成脚本：

- `scripts/modebug_build_hml_original100_inputs.py`

## 选择规则

使用 `bucket_quota_hash_v1`：

1. 数据根：`linkedCodebases/datasets/HumanML3D/HumanML3D`。
2. 只选 HumanML3D text 文件中 `f_tag=0.0` 且 `to_tag=0.0` 的 full-motion caption。
3. 不重写文本，不生成 decomposed text。
4. 每条样本要求存在 `texts/{id}.txt`、`new_joints/{id}.npy` 和 `new_joint_vecs/{id}.npy`。
5. `motion_id` 不重复。
6. 10 个语义 bucket 各 10 条：train 中每 bucket 8 条，test 中每 bucket 2 条。
7. bucket 内按固定 seed 的 SHA256 排序，保证可复现。

## 校验结果

| 项 | 结果 |
| --- | --- |
| total rows | 100 |
| train/test | 80 / 20 |
| unique sample_id | 100 |
| unique motion_id | 100 |
| full caption tags | 100 rows with `0.0 / 0.0` |
| prompt rows | 100 |
| prompt txt lines | 100 |
| GT frame range | 10 to 213 |
| missing assets | 0 |
| bucket coverage | 10 buckets x 10 rows |

## 使用边界

允许用途：

1. baseline full-motion generation；
2. failure family selection；
3. good / bad comparator construction；
4. trace hypothesis preparation；
5. 后续按 full-text 结果触发 decomposed text 归因。

禁止用途：

1. 报告总体 failure rate；
2. 宣称 held-out generalization；
3. 把 train-source rows 当作 final evaluator；
4. 在 full-text 结果出来前预生成 decomposed text；
5. 把这 100 条写成数据集贡献。
