---
title: "A1 Original100 posthoc actual-text and GT review summary"
created: 2026-05-27T00:41:23
updated: 2026-05-27T00:41:23
tags:
  - MoDebug
  - Original100
  - HumanML3D
  - status/completed
type: posthoc_summary
---

## 范围

本次仅处理 `annotation_joined.jsonl` 中 `human_description` 非空的条目；按用户约定，非空即问题行。未把空 description 计入问题。

输出文件：
- [[a1_actual_text_error_causes.tsv]]
- [[a1_gt_humanml3d_review_queue.tsv]]
- 当前笔记 `a1_actual_text_error_causes.md`

## 统计概览

- 问题行总数：`76`
- 涉及唯一 prompt 数：`42`
- GT 问题行：`6`
- `needs_followup=yes`：`52`
- `needs_followup=no`：`24`

按 baseline 分布：
- `mogents`: 21
- `momask_original`: 23
- `motiongpt`: 14
- `molingo`: 12
- `gt`: 6

按错误类型分布：
- `left_right_error`: 26
- `trajectory_error`: 9
- `hand_usage_error`: 6
- `missing_subaction`: 6
- `speed_duration_error`: 5
- `action_semantic_mismatch`: 4
- `artifact_sliding_or_drift`: 4
- `limb_count_error`: 3
- `count_repetition_error`: 2
- `action_type_error`: 2
- `kinematic_artifact`: 2
- `orientation_facing_error`: 2
- `source_text_ambiguity`: 1
- `source_text_typo_or_caption_issue`: 1
- `sample_or_prompt_contamination`: 1
- `action_progression_failure`: 1
- `viewer_direction_error`: 1

## A1 标注原则

- `actual_observed_text` 只复述 human description 已能支持的内容，不自行想象视频细节。
- 当人工描述不足以完整恢复整段动作时，统一写成“从标注可确定：...；未能确定：...”。
- 这里的结果是 `Original100` 的人工诊断整理，用于复查与错误归因，不是 final evaluator。

## GT 复查重点

- `M002542` / `hml_orig100_test_007__full`: `ambiguity_type=text_ambiguous`；`review_priority=high`。弱。同一 motion 的另外两条文本分别写“右侧拾起、左侧放下”和“左侧拿起、右侧放下”，与当前 caption 互相冲突，只能说明该 motion 存在系统性左右歧义，不能自动给出唯一纠正。
- `M014557` / `hml_orig100_test_009__full`: `ambiguity_type=none`；`review_priority=medium`。强。同一 motion 的另外两条文本都稳定指向“跑步后跳起/继续跑”，可用于把当前 caption 中的拼写问题和不自然措辞修正为 run-forward-and-jump 家族。
- `009629` / `hml_orig100_train_031__full`: `ambiguity_type=actor/body-centric`；`review_priority=high`。弱。其余文本只说明 kneeling 和右臂支撑，没有写 first kneeling leg，无法自动纠正“先跪哪条腿”。
- `002812` / `hml_orig100_train_033__full`: `ambiguity_type=actor/body-centric`；`review_priority=high`。负向。同一 text 文件中另外两条是 pacing/waiting，与踢地动作语义完全不一致，提示该 motion 的文本对齐本身就值得复查，不能拿来自动纠正左/右脚。
- `013083` / `hml_orig100_train_035__full`: `ambiguity_type=actor/body-centric`；`review_priority=high`。强。同一 motion 的前两条文本都明确写 right leg/right leg high kick，可用于把当前“left leg” caption 纠正回右腿踢。
- `M000778` / `hml_orig100_train_062__full`: `ambiguity_type=none`；`review_priority=medium`。弱。同一 motion 的三条文本都属于 forward-walk 家族，但其中两条仍写 slowly，因此只能确认动作族，不足以单独修正速度词。

## 结论

- GT 里至少有三类需要人工复查的源问题：
  - 左右侧别可能错标但语义本身清楚：`009629`、`002812`、`013083`
  - 左右参照系本身不清楚：`M002542`
  - 文本措辞/拼写质量问题：`M014557`
- 非 GT baseline 的问题主要集中在：轨迹不符、左右手/脚错误、子动作缺失，以及滑步/漂移等运动学伪影。
- `002812` 的同一 text 文件中存在与踢地动作无关的 pacing 文本；这不是普通 left/right 小问题，更像 HumanML3D 文本对齐异常，建议优先复查。
