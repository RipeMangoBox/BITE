---
title: "MoDebug HumanML3D Original100 Four Baseline Generation Launch Plan"
created: 2026-05-24T20:08:32.620180+00:00
type: provenance
role: diagnostic
used_for: observation
---

# Original100 Four Baseline Generation

- Run root: `/data/public/ripemangobox/Motion/EventT2M-codes/artifacts/remote4090/modebug_hml_original100_four_baseline_20260524`
- Inputs: 100 HumanML3D native full-motion captions from `hml_original100_generation_manifest.tsv`.
- Length policy: `target_length = min(gt_frames, 196)`, floored to a multiple of 4 for VQ token compatibility.
- GPU0 serial queue: MoLingo -> MoGenTS.
- GPU1 serial queue: MotionGPT -> MoMask.
- This stage generates `npy/joints/features` and run records only. Unified MP4 rendering and Gradio review are downstream.
- Evidence role: diagnostic / observation only, not final evaluator evidence.
