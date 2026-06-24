---
title: "Full-Text / Full-Motion 插件评估实验骨架"
created: 2026-05-20T13:45:48+08:00
updated: 2026-05-23T15:53:56+08:00
type: experiment_scaffold
tags:
  - MoDebug
  - plugin_eval
  - full_text_full_motion
  - active_experiment
---

# Full-Text / Full-Motion 插件评估实验骨架

## 目标

这是 MoDebug 当前主线的后续实验入口。它只记录 full text / full motion 层面的 paired comparison：

```text
full text + baseline B -> full motion_B
full text + baseline B + MoDebug -> full motion_B+MoDebug
paired full-motion evaluation
```

当前目录已收录 P1 1-3 event MVP 的 diagnostic generation、skeleton visualization 和 MoGenTS native default split/eval cross-check。它们仍不是 `B+MoDebug` 优于 `B` 的 paired plugin evidence。

当前数据构造决策：下一轮不继续扩大 manual event-decomposition 样本，而是先构造 100 条 HumanML3D original text sample，作为 `failure_bank_v1`。目标配比为 80 条 train-source、20 条 test-source；第一轮只用 original full text，后续 decomposed text 仅在 full-text 结果需要归因时生成。完整方案见 [[2026-05-23_modebug_humanml3d_original100_diagnostic_expansion|HumanML3D Original100 Diagnostic Expansion]]。

## 当前已收录证据

- Four-baseline custom-prompt diagnostic generation: `artifacts/remote4090/modebug_p1_1e3_four_baseline_20260521`，MotionGPT / MoLingo / MoMask / MoGenTS 各 18/18。
- MoMask original-checkpoint correction: `artifacts/remote4090/modebug_p1_1e3_four_baseline_20260521_records_momask_original/run_record.json` supersedes the earlier SOMA-checkpoint MoMask diagnostic record for original-checkpoint baseline comparison.
- Skeleton visualization: `artifacts/remote4090/modebug_p1_1e3_four_baseline_20260521_vis/vis`，4 baselines x 18 prompts = 72/72 mp4，failures 0，role=`diagnostic`。
- MoGenTS corrected visualization: `artifacts/remote4090/remote4090/modebug_p1_mogents_corrected_20260522/records/run_record.json` supersedes the earlier MoGenTS custom direct-runner videos for human visual inspection. It uses official `demo_mogen.py` with `pretrain_mtrans` + `pretrain_rtrans` + `pretrain_vq`, length estimator, `time_steps=18`, and inverse normalization before `recover_from_ric`; coverage 18/18 mp4, role=`diagnostic`, used_for=`observation`.
- Four-baseline HumanML3D unified-renderer visualization: `artifacts/remote4090/remote4090/modebug_p1_four_baseline_hml_render_20260522/vis`，MotionGPT / MoLingo / MoMask original / MoGenTS corrected joints all rendered through MoGenTS/HumanML3D `plot_3d_motion` + `t2m_kinematic_chain`; 4 baselines x 18 prompts = 72/72 mp4，role=`diagnostic`, used_for=`observation`. This controls the renderer variable for visual inspection, but source generation lengths still differ by model.
- P1 HumanML3D GT visual reference: `artifacts/experiments/modebug/p1_humanml3d_gt_hml_render_20260522/vis/gt`，6 unique HumanML3D source motions are rendered from `new_joints` and mapped to all 18 P1 rows; 18/18 mp4，role=`diagnostic`, used_for=`observation`. These 18 rows are not all HumanML3D test-set text: 14 rows map to train source motions and 4 rows map to the single test source motion `003859/M003859`; single-event rows reuse the full source motion GT.
- Phase1 GT reprocessed human-eval bookkeeping: `eval/phase1_gt_reprocessed_20260522/run_record.json`，samples 18/18，items 90/90，baseline latest annotations 28/72，non-empty problem descriptions 12。It records train/test source split, native-vs-processed text provenance, text processing, GT paths, baseline videos, and cleaned latest human annotations; role=`diagnostic`, used_for=`human_eval_cleaning;split_analysis;event_embedding_analysis_prep`.
- MoGenTS native default split/eval cross-check: `artifacts/remote4090/modebug_mogents_default_split_eval_20260521_default_eval/modebug_mogents_default_split_eval_20260521`，evaluator=`mogents_native_eval_mask_default_humanml3d_test_split`，protocol=`MoGenTS native eval_mask.py default HumanML3D test split; no P1 custom text_path`，20 eval repeats completed，returncode 0。Final metrics: FID 2.839 conf 0.011; Diversity 9.478 conf 0.085; TOP1 0.236 conf 0.003; TOP2 0.386 conf 0.002; TOP3 0.487 conf 0.002; Matching 4.845 conf 0.004; Multimodality 0.917 conf 0.032. Role=`cross_check`, used_for=`observation`; do not mix these metrics with custom P1 visual diagnostics.

## 成功标准

一条结果进入 `results/` 前必须同时记录：

1. same prompt；
2. same seed 或 same candidate pool；
3. same length / token budget；
4. same sampling budget；
5. baseline provenance；
6. MoDebug intervention 描述；
7. full-motion paired preference 或 checklist；
8. quality guardrail；
9. limitations。

## 目录约定

| 路径 | 内容 | 当前状态 |
|---|---|---|
| `inputs/` | prompt set、baseline list、seed/candidate budget | 待填 |
| `protocols/` | paired evaluation protocol、human review rubric、quality guardrail | 待填 |
| `provenance/` | git commit、checkpoint、command、tmux/log、artifact path | 待填 |
| `eval/` | paired preference、checklist、quality guardrail、side signals | 待填 |
| `results/` | 中文 summary、表格、结论和限制 | 待填 |
| `vis/` | paired render、case card、failure examples | 待填 |
| `logs/` | 运行日志副本 | 待填 |

## Original100 数据扩展约定

计划新增：

| artifact | 内容 | role |
| --- | --- | --- |
| `inputs/hml_original100_sample_manifest.tsv` | 100 条 HumanML3D original caption 样本，含 80 train-source 与 20 test-source | diagnostic |
| `eval/original100_human_review_*/` | visual caption、problem、enrichment、ambiguity 标注 | anchor |
| `results/original100_failure_family_summary.md` | failure family、good/bad pair、decomposed 触发清单 | diagnostic_summary |

每条样本必须记录：

1. `phase=phase1_original100_gt`；
2. `split_bucket=original100_train_gt` 或 `original100_test_gt`；
3. `source_split=train/test`；
4. `text_origin=humanml3d_caption`；
5. `text_processing=native_original_caption`；
6. `motion_id`、`caption_idx`、GT motion path 和 text file path；
7. `role=diagnostic`；
8. `used_for=failure_bank_construction;baseline_artifact_observation;failure_family_selection;trace_hypothesis_prep`。

decomposed text 不作为默认输入。只有当 original full text 生成结果暴露 event omission、event misbinding、order mismatch、方向/步数冲突或组合失真时，才为对应样本生成 `inputs/hml_original100_decomposed_triggered.tsv`。

## 证据角色

| 证据 | role | used_for | 边界 |
|---|---|---|---|
| paired full-motion preference | `primary_plugin_evidence` | `selection` 或 `observation` | 需要 blind / paired protocol |
| instruction-following checklist | `cross_check` | `observation` | 不替代人工偏好 |
| FID / diversity / foot sliding / pose validity | `quality_guardrail` | `safety` | 只防止质量下降 |
| trace signal delta | `mechanistic_diagnostic` | `observation` | 解释插件影响，不单独证明提升 |
| VLM / PoseFix / retrieval score | `side_signal` | `cross_check` | 不能写成 final evaluator |
| Original100 failure bank | `diagnostic_expansion` | `failure_family_selection` | 不写成 benchmark、final test set 或总体 failure rate |

## 禁止事项

1. 不把 P1 text embedding diagnostic 写成插件提升。
2. 不把旧 M0 proxy 或 retained assets 合并进本目录结果。
3. 不在没有 paired full-motion evidence 时写 `B+MoDebug` 优于 `B`。
4. 不把同一 scorer/protocol 同时作为 dev scorer 和 final evaluator。

## 下一步填充顺序

1. `inputs/prompt_set.tsv`：先放最小 prompt set，不需要 motion-side event grounding。
2. `inputs/hml_original100_sample_manifest.tsv`：构造 80 train-source + 20 test-source 的 original caption diagnostic set。
3. `inputs/baseline_queue.tsv`：记录可运行 baseline 和插件形态。
4. `protocols/paired_eval_contract.md`：定义 blind pairwise、quality guardrail 和 side signal。
5. `provenance/run_manifest.jsonl`：每个 run 一行，记录命令、checkpoint、seed、length budget 和 artifact path。
6. `results/original100_failure_family_summary.md`：只总结 failure family、good/bad pair 和 decomposed 触发条件，不写总体 failure rate。
7. `results/plugin_eval_summary.md`：只有真实 paired evidence 后再创建。
