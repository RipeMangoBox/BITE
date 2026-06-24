---
title: "MoDebug Phase1/Phase2 Evaluation Data Split Contract"
created: 2026-05-22T15:20:17+08:00
updated: 2026-05-23T15:53:56+08:00
type: experiment_protocol
tags:
  - MoDebug
  - data_split
  - human_eval
  - diagnostic
---

# MoDebug Phase1/Phase2 Evaluation Data Split Contract

## Scope

This contract defines how current and future human-eval samples must be marked before analysis.

Each row must make the following explicit:

- `phase`: `phase1_gt` or `phase2_no_gt`
- `split_bucket`: for phase 1, `phase1_train_gt` or `phase1_test_gt`; for phase 2, a no-GT discovery bucket
- `source_split`: dataset split of the source motion when available
- `text_origin`: whether the text is a native dataset caption or processed text
- `text_processing`: what was changed, generated, split, normalized, or manually derived
- `has_gt_motion`: whether a GT motion/video is available for this exact source sample
- `event_decomposition_status`: native, manual, automatic, cleaned, or pending
- `role` and `used_for`: diagnostic bookkeeping only unless a later held-out evaluator is created

## Phase 1: With GT

Phase 1 is for samples with an identifiable HumanML3D source motion and renderable GT reference.

### Train Source Split

Purpose:

- Sanity-check whether released baselines behave reasonably on motions/texts from their training distribution.
- Treat strong results as expected connectivity, not as evidence of generalization.

Required marking:

- `split_bucket=phase1_train_gt`
- `source_split=train`
- `has_gt_motion=yes`
- `role=diagnostic`
- `used_for=human_eval_cleaning;split_analysis;event_embedding_analysis_prep`

Interpretation:

- Models should plausibly perform well here.
- Failures here are useful for debugging baseline setup, rendering, prompt formatting, or obvious instruction-following gaps.
- Success here must not be reported as held-out performance.

### Test Source Split

Purpose:

- Conventional GT-backed evaluation reference.
- Still diagnostic unless the evaluator protocol is held out and predefined.

Required marking:

- `split_bucket=phase1_test_gt`
- `source_split=test`
- `has_gt_motion=yes`
- `role=diagnostic` or a stricter role only after a separate held-out protocol is defined
- `used_for=human_eval_cleaning;split_analysis;event_embedding_analysis_prep`

Interpretation:

- Test-source rows can support stronger sanity claims than train-source rows.
- They do not become final evaluator evidence unless sample selection, metric, scorer, and annotation cleaning are locked before evaluation.

## Phase 1b: Original100 With GT

Phase 1b expands the current GT-backed diagnostic pool to 100 HumanML3D original text samples.

Target composition:

| bucket | count | source_split | phase |
|---|---:|---|---|
| `original100_train_gt` | 80 | train | `phase1_original100_gt` |
| `original100_test_gt` | 20 | test | `phase1_original100_gt` |

Purpose:

- Build a diagnostic failure bank over native HumanML3D captions.
- Select failure families for trace analysis and targeted intervention.
- Keep train-source and test-source provenance explicit before any summary.
- Decide which samples need decomposed text for attribution.

Required marking:

- `phase=phase1_original100_gt`
- `split_bucket=original100_train_gt` or `original100_test_gt`
- `source_split=train` or `test`
- `has_gt_motion=yes`
- `text_origin=humanml3d_caption`
- `text_processing=native_original_caption`
- `role=diagnostic`
- `used_for=failure_bank_construction;baseline_artifact_observation;failure_family_selection;trace_hypothesis_prep`

Interpretation:

- Train-source rows are useful for baseline setup, artifact discovery, and good/bad comparator construction.
- Test-source rows are stronger sanity checks, but still do not become final evaluator evidence unless sample selection, scorer, annotation protocol, and held-out evaluator are predefined.
- Original100 must not be reported as a new benchmark, final test set, or general model failure-rate estimate.
- The primary output is a failure-family and trace-hypothesis queue, not a dataset contribution.

### Decomposed Text Trigger

Decomposed text is generated only after original full-text generation exposes an attribution question.

Trigger conditions:

- a full motion omits an event from the original caption;
- an event is present but bound to the wrong direction, count, body part, order, or manner;
- multiple events appear to compete, collapse, or be overwritten by a dominant prior;
- human review cannot tell whether the model lacks the atomic event ability or loses the event only under full-text composition.

Required marking for decomposed rows:

- `text_origin=manual_event_decomposition` or `automatic_pending_review`
- `text_processing=triggered_decomposition_from_original100`
- `parent_sample_id`
- `event_idx`
- `event_text`
- `event_relation_to_full`: `literal_span`, `paraphrase`, or `implicit_completion`
- `boundary_confidence`
- `role=diagnostic`
- `used_for=full_vs_decomposed_attribution`

Interpretation:

- If full text fails but decomposed event succeeds, the case supports a compositional propagation-loss hypothesis.
- If both full text and decomposed event fail, the case is more likely atomic event capability failure, data ambiguity, or baseline setup weakness.
- If decomposed text introduces ambiguity, it must be recorded as an analysis limitation rather than treated as a cleaner label.

## Text Provenance

Use these values:

| value | meaning |
|---|---|
| `humanml3d_caption` | Native caption selected from a HumanML3D text file by `caption_idx`. |
| `manual_event_decomposition` | Text manually derived from a full caption for event-level probing. |
| `model_or_llm_processed` | Text generated or rewritten by a model; must include prompt/procedure provenance. |
| `human_cleaned` | Human-edited text; must keep original text and edit rationale. |
| `unknown` | Temporary only; must be resolved before analysis. |

For processed text, preserve:

- original text
- processed text
- processing method
- processor or annotator
- date
- limitations

Manual event prompts are not native HumanML3D captions and are not temporal GT boundary labels.

## Phase 2: No GT

Phase 2 is for samples without GT motion reference.

### Discovery

Goal:

- Find instruction-following and non-following samples.
- Split text into events for further visualization and human eval.

Required marking:

- `phase=phase2_no_gt`
- `has_gt_motion=no`
- `event_decomposition_status=manual_pending`, `manual_cleaned`, or `automatic_pending_review`
- `role=diagnostic`
- `used_for=sample_discovery;human_eval;event_embedding_analysis`

### Text-Embedding Analysis

For every sample, compute:

- full-text embedding
- event-text embeddings
- similarity between each event embedding and full-text embedding
- aggregate similarity statistics
- text-embedding propagation traces

The propagation trace definition is not finalized. Candidate trace fields:

- layer or block index
- token or event span
- event-to-full similarity over layers
- attention mass from generated motion tokens to event tokens
- conditioning residual or cross-attention norm over time
- temporal stability of the dominant event alignment

The trace schema must be fixed before using it for comparisons.

### Human Eval Join

Before analysis:

- deduplicate repeated annotation events
- use a current latest-annotation table as the main source
- keep raw annotation events as audit log
- keep empty descriptions as missing/neutral, not positive evidence
- record annotator, date, protocol, and limitations

## Current Phase 1 Reprocessed Artifact

Current active artifact:

- `eval/phase1_gt_reprocessed_20260522/phase1_gt_sample_manifest.tsv`
- `eval/phase1_gt_reprocessed_20260522/phase1_gt_item_manifest.tsv`
- `eval/phase1_gt_reprocessed_20260522/phase1_clean_human_annotations.tsv`
- `eval/phase1_gt_reprocessed_20260522/run_record.json`

Current counts:

| bucket | count |
|---|---:|
| `phase1_train_gt` | 14 |
| `phase1_test_gt` | 4 |
| `humanml3d_caption` | 6 |
| `manual_event_decomposition` | 12 |
| baseline annotation rows | 72 |
| latest annotated baseline rows | 28 |
| non-empty problem descriptions | 12 |

Limitations:

- Train/test refers to HumanML3D source motion split.
- Single-event rows reuse the full source GT motion for visual reference.
- The current tables support diagnostic cleanup and analysis preparation, not final held-out evaluation claims.
