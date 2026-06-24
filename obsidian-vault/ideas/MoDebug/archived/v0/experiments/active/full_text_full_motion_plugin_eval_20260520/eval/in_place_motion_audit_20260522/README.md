---
title: MoDebug P1 In-Place Motion Audit
created: 2026-05-22T23:15:00+08:00
updated: 2026-05-22T23:15:00+08:00
status: active
hypothesis: Human descriptions containing 原地/踏步 correspond to low root translation in source joints before unified rendering; treat them as generated-output phenomena unless later evidence shows a source export bug.
tags:
  - MoDebug
  - human_eval
  - diagnostic
  - motion_in_place
source_papers: []
related_docs:
  - "[[ideas/MoDebug/experiments/active/full_text_full_motion_plugin_eval_20260520/README]]"
  - "[[phase1_phase2_eval_data_split_contract]]"
---

# MoDebug P1 In-Place Motion Audit

> [!abstract] Decision
> 保留原始 human description，不直接覆盖为最终 caption。对“原地走路 / 原地踏步”另派生 `problem_tag`，并在后续 schema 中拆成 `visual_caption` 与 `problem_tag` 两列。

## Inputs

- Human eval CSV: `../p1_four_baseline_vis_problem_descriptions_20260522/human_problem_descriptions.csv`
- Geometry audit: `../../../../../../../../artifacts/remote4090/remote4090/modebug_p1_four_baseline_hml_render_20260522/geometry_audit.csv`
- Contact sheet: `contact_sheets/montage_labeled.jpg`
- Flagged table: `in_place_flagged_audit.csv`
- Run record: `run_record.json`

## Finding

7 个 baseline 条目的人类描述包含“原地 / 踏步 / 不位移”。这些条目在统一 HumanML3D renderer 之前的 `source_joints_path` 中，root planar span 已经很低：

| Count | Planar span range | Interpretation |
| --- | --- | --- |
| 7 | 0.065-0.457 | low global translation before rendering |

同类 walk prompt 的非 flagged 对照通常在约 1.5-5.6 的 root planar span 区间。当前证据因此更支持：这些条目是当前 source joints 中已有的 low-translation / in-place generation 现象，而不是 unified renderer 单独造成的位移消失。

## Policy

1. `problem_description` 保持人工原文，不自动改写。
2. 未来派生结构化列：
   - `visual_caption`: 人眼看到的动作描述，例如“a person steps in place with little global translation”。
   - `problem_tag`: 结构化诊断标签，例如 `motion_in_place`、`no_translation`、`weak_translation`。
3. 当前不要把 `motion_in_place` 写成模型机制根因。它只说明输出 joints 缺少 root translation，不说明原因来自训练数据、prompt parsing、condition propagation、motion decoder，或导出流程。
4. 若用于论文，只写 observation / diagnostic claim，不写 final evaluator claim。

## Suggested Tags

| Planar span | Suggested tag | Scope |
| --- | --- | --- |
| <= 0.1 | `no_translation` | prompt expects locomotion but root translation is almost zero |
| > 0.1 and <= 0.5 | `motion_in_place` | visible stepping or motion with very low translation |
| > 0.5 and < 1.0 | `weak_translation` | borderline, keep for review |
| >= 1.0 | `normal_translation` | not automatically clean; only clears this diagnostic |

## Claim Boundary

Safe:

- “Several walk-related outputs have low root planar span before rendering, matching human observations of in-place stepping.”
- “This audit helps separate renderer artifacts from generated-output geometry.”

Unsafe:

- “MoDebug proves the model mechanism fails to propagate walking semantics.”
- “The renderer caused / did not cause every possible locomotion artifact.”
- “`motion_in_place` is a final instruction-following evaluator.”

## Next Action

Add derived `problem_tag` and optional `visual_caption` columns in a future cleaned annotation table. Do not overwrite the current human-eval CSV unless the cleanup protocol is explicitly versioned.
