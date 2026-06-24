---
title: "Original100 posthoc multi-agent index"
created: 2026-05-27T00:50:00+08:00
updated: 2026-05-27T00:50:00+08:00
type: diagnostic_index
status: complete
tags:
  - MoDebug
  - Original100
  - HumanML3D
  - multi-agent
  - status/completed
role: diagnostic
used_for:
  - failure_bank_construction
  - baseline_artifact_observation
  - failure_family_selection
  - trace_hypothesis_prep
limitations: |
  Original100 is a diagnostic sample set, not a benchmark or held-out final evaluator.
  Empty human description means accepted/correct for this pass; non-empty human description means problem.
---

# Original100 Posthoc 20260527

## Scope

- Source annotation: `../original100_four_baseline_vis_review_20260525/human_problem_descriptions.csv`
- Rows: `500` = `gt + 4 baselines` x `100`
- Problem rows: `76`
- GT problem rows: `6`
- Generated-model prompt outcomes: `61` all-good, `36` partial, `3` all-bad

## Inputs

- `annotation_joined.jsonl`: joined annotation, sample metadata, render paths.
- `per_prompt_problem_matrix.tsv`: prompt-level correctness matrix.
- `coordinator_basic_stats.json`: coordinator cross-check statistics.
- `coordinator_prompt_groups.tsv`: prompt grouping by all-good / partial / all-bad.

## Agent Outputs

### a1 Actual Text And Error Causes

- `a1_actual_text_error_causes.tsv`: `76` non-empty-description problem rows.
- `a1_gt_humanml3d_review_queue.tsv`: `6` GT review candidates.
- `a1_actual_text_error_causes.md`: Chinese summary.

Key results:

- Dominant error type: `left_right_error` (`26` rows).
- GT review cases include left/right actor-centric issues, text ambiguity, typo/caption quality, and speed wording.
- `002812` is high priority because sibling HumanML3D captions mix a kick action with unrelated pacing/waiting captions.

### a2 Motion Text Ambiguity

- `a2_motion_text_ambiguity.tsv`: `17` high-value motion-text ambiguity candidates from all `100/100` Original100 motions.
- `a2_motion_text_ambiguity.md`: Chinese summary.

Key results:

- Direct replace candidates: `7`.
- Supplement/self-rewrite candidates: `4`.
- Keep/block automatic replacement candidates: `6`.
- Main ambiguity families: sibling left/right conflicts, selected caption too short for path/facing/turn, and viewer-centric phrasing.

### a3 Model Sample Capability

- `a3_model_sample_capability_summary.md`: main capability report.
- `a3_model_sample_capability_tables.tsv`: grouped statistics.
- `a3_metric_visualization_proposals.tsv`: candidate metrics and visualization processes.
- `a3_deepseek_closure.md`: 3-round DeepSeek closure summary.

Key results:

- Model problem counts on this diagnostic set: `MoLingo 12`, `MotionGPT 14`, `MoGenTS 21`, `MoMask original 23`.
- Four-model all-bad prompts: `test_003`, `test_020`, `train_050`.
- Strongest composite difficulty: `left/right + sequential + long_text`.
- P0 metrics proposed:
  - `LRGA`: left/right grounding accuracy.
  - `SCS`: stage coverage score.
- Root trajectory shape is useful for qualitative visualization, but should not be promoted to a main metric yet.

## Cross-Check Notes

- a1 problem rows match coordinator count: `76`.
- a1 GT queue matches GT problem count: `6`.
- a2 scanned all `100` motions and emitted only suspicious/high-value candidates.
- a3 follows the required DeepSeek loop and keeps Original100 as diagnostic evidence only.

## Recommended Next Actions

1. Build a VLM/manual review sheet for the `6` GT candidates in `a1_gt_humanml3d_review_queue.tsv`.
2. Split `a2_motion_text_ambiguity.tsv` into direct replacement, supplement, and blocklist files before any text self-optimization.
3. Implement a small LRGA annotation protocol first; use the `49` side-token samples as the initial pool.
4. Implement SCS on explicit multi-stage samples; start with the all-bad and partial cases before expanding.
5. Keep foot sliding / physics artifacts as secondary tags for this batch; the primary failure axis is instruction following.
