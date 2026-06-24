---
title: "MoDebug P1 1-3 Event MVP Provenance"
created: 2026-05-21T00:00:00+08:00
updated: 2026-05-22T15:20:17+08:00
type: provenance
tags:
  - MoDebug
  - P1
  - remote4090
---

# MoDebug P1 1-3 Event MVP Provenance

## Local Inputs

- `inputs/p1_1e3_mvp_sample_manifest.tsv`
- `inputs/p1_1e3_mvp_event_decomposition.tsv`
- `inputs/p1_1e3_mvp_prompt_manifest.tsv`
- `inputs/p1_1e3_mvp_prompts.txt`
- `inputs/p1_1e3_mvp_prompts_with_ids.tsv`

## Current Boundary

Existing P1 text-side embedding and propagation records are not enough to settle high/weak instruction-following sample characteristics. This MVP is a diagnostic generation bridge only.

Hard gate added after review: baseline comparisons must use original public baseline checkpoints. Runs using SOMA-trained checkpoints are invalid for original-ckpt baseline comparison, even if they are useful as engineering connectivity checks.

## Remote 4090 Logs

## Four Baseline Remote4090 Run

- date: 2026-05-21
- artifact_path: `/data/public/ripemangobox/Motion/EventT2M-codes/artifacts/remote4090/modebug_p1_1e3_four_baseline_20260521`
- local_evidence_root: `artifacts/remote4090/modebug_p1_1e3_four_baseline_20260521`
- evaluator: `modebug_p1_1e3_four_baseline_remote4090_summary`
- protocol: `paperIDEAs/MoDebug/experiments/active/full_text_full_motion_plugin_eval_20260520/protocols/p1_1e3_mvp_generation_protocol.md`
- motion_source: MotionGPT, MoLingo, MoMask, MoGenTS baseline generation on remote4090
- condition_pair: full/single_event
- n/evaluable: MotionGPT 18/18; MoLingo 18/18; MoMask 18/18; MoGenTS 18/18
- coverage: 18 prompts total, including 6 full prompts and 12 single-event prompts
- role: diagnostic
- used_for: observation
- limitations: Diagnostic custom-prompt MVP only; not held-out final evaluator evidence. MoGenTS used a custom direct-generation runner after code inspection showed native `eval_mask.py` ignores `text_path`. MoMask default checkpoint attempt failed, then the fixed SOMA checkpoint run succeeded.

Execution layout:

| GPU queue | serial baselines | status |
|---|---|---|
| GPU0 | MoLingo -> MoGenTS | completed |
| GPU1 | MotionGPT -> MoMask | completed |

Result records:

| model | evaluator | n/evaluable | local record |
|---|---|---:|---|
| MotionGPT | `motiongpt_official_demo_custom_prompt_mvp` | 18/18 | `artifacts/remote4090/modebug_p1_1e3_four_baseline_20260521_records_motiongpt/run_record.json` |
| MoLingo | `molingo_custom_prompt_mvp_runner` | 18/18 | `artifacts/remote4090/modebug_p1_1e3_four_baseline_20260521_records_molingo/run_record.json` |
| MoMask | `momask_native_gen_t2m_custom_text_path_fixed_soma_ckpt` | 18/18 | `artifacts/remote4090/modebug_p1_1e3_four_baseline_20260521_records_momask/run_record.json` |
| MoGenTS | `mogents_custom_prompt_runner_direct_generate` | 18/18 | `artifacts/remote4090/modebug_p1_1e3_four_baseline_20260521_records_mogents/run_record.json` |

Fetched evidence:

- `artifacts/remote4090/modebug_p1_1e3_four_baseline_20260521/four_baseline_summary.json`
- `artifacts/remote4090/modebug_p1_1e3_four_baseline_20260521/four_baseline_summary.md`
- `artifacts/remote4090/modebug_p1_1e3_four_baseline_20260521/result_sha256.txt`
- `artifacts/remote4090/modebug_p1_1e3_four_baseline_20260521/input_sha256.txt`
- `artifacts/remote4090/modebug_p1_1e3_four_baseline_20260521/input_line_counts.txt`
- `artifacts/remote4090/modebug_p1_1e3_four_baseline_20260521/modebug_p1_1e3_gpu0_molingo_mogents_20260521.log`
- `artifacts/remote4090/modebug_p1_1e3_four_baseline_20260521/modebug_p1_1e3_gpu1_motiongpt_momask_20260521.log`
- `artifacts/remote4090/modebug_p1_1e3_four_baseline_20260521/modebug_p1_1e3_momask_fixed_g1_20260521.log`
- `artifacts/remote4090/modebug_p1_1e3_four_baseline_20260521/modebug_p1_1e3_mogents_custom_g0_20260521.log`
- `artifacts/remote4090/modebug_p1_1e3_four_baseline_20260521/modebug_p1_1e3_four_summary_20260521.log`

Drift note:

`initial plan: MoGenTS native eval_mask.py --text_path` -> `actual run: MoGenTS custom direct-generate runner` -> evidence: code inspection and stopped native attempt showed `eval_mask.py` ignores `text_path` and uses the HumanML3D test loader -> affected_docs: `artifacts/remote4090/modebug_p1_1e3_four_baseline_20260521/launch_plan.md`, `artifacts/remote4090/modebug_p1_1e3_four_baseline_20260521/four_baseline_summary.json` -> next_action: treat the MoGenTS output as diagnostic custom-runner evidence only, not native eval evidence.

2026-05-22 correction drift:

`MoGenTS custom direct-generate runner videos` -> `MoGenTS official demo_mogen.py corrected visualization` -> evidence: visual review showed obvious instruction-following concerns; code review plus DeepSeek cross-check found the old runner did not use `pretrain_rtrans`, forced every prompt to 196 frames, and its own saved joints path bypassed the official demo inverse-normalization visualization path -> affected_docs: this provenance note, `README.md`, `MoDebug_p1_four_baseline_vis_gradio.sh`, `scripts/modebug_p1_four_baseline_vis_review_app.py` -> next_action: use the corrected MoGenTS videos for human visual re-evaluation; keep the older MoGenTS direct-runner output only as superseded diagnostic provenance.

2026-05-22 renderer-control drift:

`mixed baseline visualization renderers` -> `single HumanML3D/MoGenTS renderer for all four baselines` -> evidence: user requested removing the rendering-style variable after MoGenTS was switched to HumanML3D rendering; new artifact renders MotionGPT, MoLingo, MoMask original, and corrected MoGenTS joints through the same `plot_3d_motion` + `t2m_kinematic_chain` path -> affected_docs: this provenance note, `README.md`, `MoDebug_p1_four_baseline_vis_gradio.sh`, `scripts/modebug_p1_four_baseline_vis_review_app.py` -> next_action: use the unified-renderer videos for human visual inspection; keep source-generation length differences as an explicit limitation.

2026-05-22 GT-reference drift:

`baseline-only visual review` -> `leftmost HumanML3D source GT reference plus four baselines` -> evidence: the older local `linkedCodebases/datasets/HumanML3D/HumanML3D/animations` directory did not contain the six P1 source motion ids as same-name mp4 files; a new explicit GT artifact renders P1 source `new_joints` and maps them to all 18 rows -> affected_docs: this provenance note, `README.md`, `MoDebug_p1_four_baseline_vis_gradio.sh`, `scripts/modebug_p1_four_baseline_vis_review_app.py` -> next_action: use the GT column only as visual reference; do not describe the P1 18 rows as a HumanML3D test-set benchmark.

2026-05-22 phase1 split-bookkeeping drift:

`ad hoc P1 human-eval rows` -> `phase1 GT split/text-provenance manifests` -> evidence: current plan requires train/test, native-vs-processed text, processing method, GT mapping, and human-eval cleaning before analysis -> affected_docs: this provenance note, `README.md`, `protocols/phase1_phase2_eval_data_split_contract.md`, `eval/phase1_gt_reprocessed_20260522/` -> next_action: use the reprocessed phase1 tables for all first-stage analysis; do not join directly against old annotation events except for audit.

## Original-Checkpoint Correction

- date: 2026-05-21
- artifact_path: `/data/public/ripemangobox/Motion/EventT2M-codes/artifacts/remote4090/modebug_p1_1e3_four_baseline_20260521/results/momask_original`
- local_evidence_root: `artifacts/remote4090/modebug_p1_1e3_four_baseline_20260521_records_momask_original`
- evaluator: `momask_native_gen_t2m_custom_text_path_original_humanml3d_ckpt`
- protocol: `paperIDEAs/MoDebug/experiments/active/full_text_full_motion_plugin_eval_20260520/protocols/p1_1e3_mvp_generation_protocol.md`
- motion_source: MoMask official HumanML3D original checkpoints on remote4090 GPU1 via `mogents-gpu1` env
- condition_pair: full/single_event
- n/evaluable: 18/18
- coverage: 18 custom prompt lines in MoMask `text_path` format `prompt#196#196`
- role: diagnostic
- used_for: observation
- limitations: Original HumanML3D MoMask checkpoint; custom prompt MVP only; `MODEBUG_TRACE_SKIP_VIS=1`, so npy joints only, not rendered videos; not held-out final evaluator evidence.

MoMask checkpoint correction:

| record | checkpoint source | status for original-ckpt baseline |
|---|---|---|
| `artifacts/remote4090/modebug_p1_1e3_four_baseline_20260521_records_momask/run_record.json` | SOMA checkpoint | invalid / superseded |
| `artifacts/remote4090/modebug_p1_1e3_four_baseline_20260521_records_momask_original/run_record.json` | official HumanML3D original checkpoint | valid diagnostic record |

Original MoMask checkpoint provenance:

- downloaded official HumanML3D checkpoint archive from MoMask official script source: Google Drive file id `1vXS7SHJBgWPt59wupQ5UUzhFObrnGkQ0`
- local archive: `artifacts/remote4090/momask_original_ckpt_download_20260521/t2m.tar.gz`
- local archive sha256: `3ed737fe352c4cdc671b0c133d6c0090690468d58832bd883686188d5f333ec7`
- uploaded original directories to remote MoMask repo:
  - `checkpoints/t2m/t2m_nlayer8_nhead6_ld384_ff1024_cdp0.1_rvq6ns`
  - `checkpoints/t2m/rvq_nq6_dc512_nc512_noshare_qdp0.2`
  - `checkpoints/t2m/tres_nlayer8_ld384_ff1024_rvq6ns_cdp0.2_sw`
  - `checkpoints/t2m/length_estimator`

Current original-ckpt diagnostic set:

| model | evaluator | n/evaluable | checkpoint status | comparison role |
|---|---|---:|---|---|
| MotionGPT | `motiongpt_official_demo_custom_prompt_mvp` | 18/18 | original public checkpoint as loaded by MotionGPT demo config | diagnostic connectivity |
| MoLingo | `molingo_custom_prompt_mvp_runner` | 18/18 | original/public pretrained `pretrained_model_263` as loaded by MoLingo runner | diagnostic connectivity |
| MoMask | `momask_native_gen_t2m_custom_text_path_original_humanml3d_ckpt` | 18/18 | official HumanML3D original checkpoint | diagnostic connectivity |
| MoGenTS | `mogents_custom_prompt_runner_direct_generate` | 18/18 | HumanML3D `pretrain_mtrans/pretrain_vq` checkpoint | diagnostic connectivity with fairness caveat |

MoGenTS fairness caveat:

- The checkpoint source is not SOMA; the loaded opts are `logs/humanml3d/pretrain_mtrans/opt.txt` and `logs/humanml3d/pretrain_vq/opt.txt`.
- The native `eval_mask.py` path is not suitable for custom prompts because it ignores `text_path` and loads the HumanML3D `test` dataloader.
- The recorded MoGenTS run uses a direct custom-prompt runner with fixed 196-frame lengths for all prompts. This avoids test-split leakage for the P1 prompts, but it also bypasses the native dataloader length distribution and native metric protocol.
- Therefore MoGenTS is acceptable as an original-checkpoint diagnostic generation artifact, but not as formal fair comparison evidence against other baselines unless all baselines are rerun under an explicitly matched custom-prompt protocol and evaluator.

## MoGenTS Corrected P1 Visualization

- date: 2026-05-22
- artifact_path: `/data/public/ripemangobox/Motion/EventT2M-codes/artifacts/remote4090/modebug_p1_mogents_corrected_20260522`
- local_evidence_root: `artifacts/remote4090/remote4090/modebug_p1_mogents_corrected_20260522`
- evaluator: `mogents_official_demo_mogen_corrected_custom_prompt_runner`
- protocol: `paperIDEAs/MoDebug/experiments/active/full_text_full_motion_plugin_eval_20260520/protocols/p1_1e3_mvp_generation_protocol.md`
- motion_source: MoGenTS official `demo_mogen.py` with HumanML3D `pretrain_mtrans`, `pretrain_rtrans`, `pretrain_vq`, and length estimator on remote4090 GPU0
- condition_pair: full/single_event
- n/evaluable: 18/18
- coverage: 18 P1 prompts; prompt-only `text_path` triggers `demo_mogen.py` length estimator; official residual transformer refinement enabled; videos copied to the local corrected `vis/mogents` root.
- role: diagnostic
- used_for: observation
- limitations: Corrected qualitative visualization generation only; single seed `20260522`; MoGenTS lengths are estimated by its own length estimator and are not length-matched to the other three baseline videos; not a held-out final evaluator.

Corrected settings:

| setting | value |
|---|---|
| seed | 20260522 |
| time_steps | 18 |
| cond_scale | 4 |
| temperature | 1.0 |
| topkr | 0.9 |
| gumbel_sample | false |
| text_length_mode | `length_estimator` |
| mtrans_name | `pretrain_mtrans` |
| rtrans_name | `pretrain_rtrans` |
| vq_name | `pretrain_vq` |

Corrected verification:

- `records/run_record.json`: `mp4_count=18`, `joints_npy_count=18`, `feature_npy_count=18`.
- `geometry_audit.csv`: 18 rows, all `status=ok`, `joints_finite_rate=1.0`, frame range 36-196.
- `logs/demo_mogen_corrected_stdout.log`: confirms `pretrain_rtrans`, `pretrain_mtrans`, `pretrain_vq`, length estimator, `time_steps=18`, and estimated per-sample lengths.
- DeepSeek implementation cross-check: corrected path fixes the old missing residual transformer, fixed 196-frame length, and inverse-normalization/recover path issues; no additional model rerun required before human re-evaluation.

## Four Baseline HumanML3D Unified Renderer Visualization

- date: 2026-05-22
- artifact_path: `/data/public/ripemangobox/Motion/EventT2M-codes/artifacts/remote4090/modebug_p1_four_baseline_hml_render_20260522`
- local_evidence_root: `artifacts/remote4090/remote4090/modebug_p1_four_baseline_hml_render_20260522`
- evaluator: `p1_four_baseline_humanml3d_renderer_unified_visualization`
- protocol: Render all four P1 baseline 22-joint outputs with the same MoGenTS/HumanML3D `t2m_kinematic_chain` + `plot_3d_motion` renderer.
- motion_source: MotionGPT, MoLingo, MoMask original, and MoGenTS corrected P1 joints on remote4090
- condition_pair: full/single_event
- n/evaluable: 72/72
- coverage: 4 baselines x 18 P1 prompts; renderer variable controlled; MoGenTS source is corrected official `demo_mogen.py` output.
- role: diagnostic
- used_for: observation
- limitations: Unified renderer for visual inspection only; source generation lengths still differ by model; not a held-out final evaluator.

Renderer settings:

| setting | value |
|---|---|
| renderer | `mogents/utils/plot_script.py::plot_3d_motion` |
| kinematic_chain | `t2m_kinematic_chain` |
| fps | 20 |
| radius | 4 |
| mp4_count | 72 |
| failures | 0 |

Local verification:

- `records/run_record.json`: `n/evaluable=72/72`, `mp4_count=72`, `failures=[]`.
- `vis/vis_manifest.tsv`: 72 rows plus header; model counts are MotionGPT 18, MoLingo 18, MoMask original 18, MoGenTS 18.
- `geometry_audit.csv`: 72 rows plus header; each rendered joint file passed finite-coordinate geometry audit.
- fetched logs: `artifacts/remote4090/remote4090/modebug_p1_hml_render_20260522.log`, `artifacts/remote4090/remote4090/modebug_p1_hml_render_check_1442.log`.

## P1 HumanML3D GT Visual Reference

- date: 2026-05-22
- artifact_path: `/data/Life Me/ResearchWY Vault/artifacts/experiments/modebug/p1_humanml3d_gt_hml_render_20260522`
- local_evidence_root: `artifacts/experiments/modebug/p1_humanml3d_gt_hml_render_20260522`
- evaluator: `p1_humanml3d_gt_hml_renderer_visual_reference`
- protocol: Render the six HumanML3D source motions used by P1 prompts from `new_joints` with a HumanML3D-style `t2m_kinematic_chain` renderer, then map them to all 18 P1 rows.
- motion_source: HumanML3D `new_joints` for P1 source motion ids
- condition_pair: full/single_event
- n/evaluable: 18/18
- coverage: 6 unique HumanML3D source motions mapped to 18 P1 prompt rows; single-event prompt rows reuse their full source motion GT.
- role: diagnostic
- used_for: observation
- limitations: GT video is a full source motion reference, not a per-single-event GT clip. The P1 rows are not all HumanML3D test-set text: 14 rows map to train source motions, and 4 rows map to the single test source motion `003859/M003859`.

Source split check:

| motion_id | source_split | row_count |
|---|---|---:|
| `007969` | train | 2 |
| `M011433` | train | 2 |
| `M013270` | train | 3 |
| `001985` | train | 3 |
| `M003558` | train | 4 |
| `003859` | test | 4 |

Local verification:

- `gt_manifest.tsv`: 18 rows plus header; all `status=rendered`.
- `vis/gt`: 18 mp4 files; first sample is 1000x1000, 20fps, 88 frames; last sample is 1000x1000, 20fps, 131 frames.
- Existing local `linkedCodebases/datasets/HumanML3D/HumanML3D/animations` did not contain same-name mp4 files for the six P1 source ids, so the new explicit GT artifact is the active reference for the P1 Gradio column.

## Phase1 GT Reprocessed Human-Eval Bookkeeping

- date: 2026-05-22
- artifact_path: `/data/Life Me/ResearchWY Vault/paperIDEAs/MoDebug/experiments/active/full_text_full_motion_plugin_eval_20260520/eval/phase1_gt_reprocessed_20260522`
- local_evidence_root: `eval/phase1_gt_reprocessed_20260522`
- evaluator: `phase1_gt_reprocessed_human_eval_manifest_builder`
- protocol: `protocols/phase1_phase2_eval_data_split_contract.md`
- motion_source: HumanML3D source GT plus MotionGPT, MoLingo, MoMask original, and MoGenTS baseline videos
- condition_pair: full/single_event
- n/evaluable: samples 18/18; items 90/90; baseline annotations 28/72
- coverage: 18 P1 rows; each has 1 GT visual reference and 4 baseline visual items.
- role: diagnostic
- used_for: human_eval_cleaning; split_analysis; event_embedding_analysis_prep
- limitations: Phase1 GT diagnostic bookkeeping only. Train/test is HumanML3D source split; single-event texts are manually processed and reuse full source GT motion.

Outputs:

- `phase1_gt_sample_manifest.tsv`: one row per P1 text row, including split bucket, source split, text origin, text processing, GT paths, and event-decomposition status.
- `phase1_gt_item_manifest.tsv`: one row per displayed item, including GT reference and four baseline videos per sample.
- `phase1_clean_human_annotations.tsv`: latest human annotation join for 72 baseline rows; raw annotation JSONL remains audit-only.
- `run_record.json`: summary counts and provenance.

Current counts:

| field | count |
|---|---:|
| `phase1_train_gt` samples | 14 |
| `phase1_test_gt` samples | 4 |
| native HumanML3D-caption rows | 6 |
| manual event-decomposition rows | 12 |
| baseline item rows | 72 |
| latest annotated baseline rows | 28 |
| non-empty problem descriptions | 12 |

## Skeleton Visualization Record

- date: 2026-05-21
- artifact_path: `/data/public/ripemangobox/Motion/EventT2M-codes/artifacts/remote4090/modebug_p1_1e3_four_baseline_20260521/vis`
- local_evidence_root: `artifacts/remote4090/modebug_p1_1e3_four_baseline_20260521_vis/vis`
- evaluator: `p1_four_baseline_skeleton_video_visualization`
- protocol: Render one lightweight skeleton mp4 per baseline per P1 prompt from original-checkpoint diagnostic generation outputs.
- motion_source: MotionGPT, MoLingo, MoMask original, MoGenTS original-checkpoint custom P1 generations
- condition_pair: full/single_event
- n/evaluable: 72/72
- coverage: 4 baselines x 18 P1 prompts; MoGenTS visualization uses inverse-normalized features with checkpoint meta mean/std before `recover_from_ric`.
- role: diagnostic
- used_for: observation
- limitations: Skeleton visualization for qualitative inspection only; not a held-out final evaluator; videos are derived from diagnostic custom-prompt generations and should not be used as metric evidence.

Local verification:

- `vis_record.json` exists with `failures=[]`.
- mp4 count: MotionGPT 18, MoLingo 18, MoMask original 18, MoGenTS 18.
- fetched logs: `artifacts/remote4090/modebug_p1_1e3_four_baseline_20260521_vis/vis/render.log`, `render_fix.log`, `render_fix2.log`.

## MoGenTS Native Default Split/Eval Cross-Check

- date: 2026-05-21
- artifact_path: `/data/public/ripemangobox/Motion/EventT2M-codes/artifacts/remote4090/modebug_mogents_default_split_eval_20260521`
- local_evidence_root: `artifacts/remote4090/modebug_mogents_default_split_eval_20260521_default_eval/modebug_mogents_default_split_eval_20260521`
- evaluator: `mogents_native_eval_mask_default_humanml3d_test_split`
- protocol: `MoGenTS native eval_mask.py default HumanML3D test split; no P1 custom text_path`
- motion_source: MoGenTS official/default HumanML3D `pretrain_mtrans` / `pretrain_vq` checkpoint on remote4090 GPU0
- condition_pair: native_humanml3d_test_split
- n/evaluable: native `eval_mask.py` test dataloader; 20 eval repeats completed; see `native_eval_log.txt` and `mogents_default_eval_stdout.log`.
- coverage: MoGenTS default HumanML3D test split loaded by `get_dataset_motion_loader(..., test)`; custom P1 prompts not used.
- role: cross_check
- used_for: observation
- limitations: Native default split/eval for protocol fairness reference only, not the P1 18-prompt generation set. Metrics must not be mixed with custom P1 visual diagnostics or treated as plugin-pair evidence.

Final MoGenTS native default split metrics:

| metric | value | confidence |
|---|---:|---:|
| FID | 2.839 | 0.011 |
| Diversity | 9.478 | 0.085 |
| TOP1 | 0.236 | 0.003 |
| TOP2 | 0.386 | 0.002 |
| TOP3 | 0.487 | 0.002 |
| Matching | 4.845 | 0.004 |
| Multimodality | 0.917 | 0.032 |

Local verification:

- `run_record.json` exists with `returncode=0`.
- `mogents_default_eval_stdout.log` contains `Eval. Repeat 0` through `Eval. Repeat 19`.
- fetched logs: `artifacts/remote4090/modebug_mogents_default_split_eval_20260521_logs/modebug_mogents_default_eval_g0_20260521.log`, `modebug_mogents_default_eval_probe_20260521.log`, `modebug_mogents_default_eval_liveness_20260521.log`.
