---

## created: 2026-05-06T23:54:45+08:00
updated: 2026-05-07T13:01:26+08:00
archived_at: 2026-05-07T13:01:26+08:00
title: "MoDebug Backbone Comparison Archive"
status: archived
tags:
  - MoDebug
  - backbone
  - evaluator
  - EventProbe
  - PerceptGuide
  - archived
related_notes:
  - '[[ideas/MoDebug/README]]'
  - '[[ideas/MoDebug/blocked/README]]'
  - '[[paperIDEAs/MoDebug/2026-05-11_modebug-route-2-cross-generator-failure-mechanism]]'

# MoDebug Backbone Comparison Archive

> [!note] Archive Boundary
> This note preserves the 2026-05-07 backbone comparison and selection reasoning, including MotionGPT, MoGenTS, LaMP, DART, MoMask, TMR, ChronAccRet, and MotionPatches roles. It is no longer the active execution route.
>
> Current active route: [[paperIDEAs/MoDebug/2026-05-11_modebug-route-2-cross-generator-failure-mechanism]].

> [!warning] Current Decision
> EventT2M is not an active evaluator candidate and not an active backbone candidate. EventT2M-era notes live in [[ideas/MoDebug/blocked/README]] as blocked provenance only.
>
> The new route keeps the MoDebug idea but rebuilds the executable stack around event / temporal relevance plus a complete `training + inference + eval` loop. Generic T2M completeness is necessary for runnable baselines, but not sufficient for core candidacy.

## 1. Active Scope

MoDebug still targets event-level semantic failure in multi-event motion generation.

```text
counterfactual text -> internal representation comparison -> root-cause diagnosis -> process-time correction
```

The current route avoids making explicit motion slicing and local artifact recognition the main dependency. Those operations require high-quality temporal labels and reliable generated-motion localizations, which are exactly the weak points this project is trying to diagnose. Instead, EventProbe should first compare correct / failed counterfactual generations inside the model: text tokenization, generated motion tokens, decoder attention, hidden states, logits, entropy, and failure-condition deltas.

This plan answers three questions:


| Question                              | Current answer                                                                                                                                                      |
| ------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| What is the generation backbone pool? | Only repos with complete training, inference, eval and a credible event / temporal link                                                                             |
| What is the evaluator stack?          | TMR for semantic side signal, ChronAccRet for chronology side signal, MotionPatches/TAMR-style sidecar for representation audit, human calibration for final anchor |
| What is excluded?                     | EventT2M as active eval/backbone; incomplete repos as backbone; generic T2M methods as core event-aware claims                                                      |


## 1.1 Backbone Role Update: 2026-05-07

DS's recommendation to move from post-hoc repair to in-process diagnosis is directionally correct. The backbone conclusion needs one guardrail: MotionGPT should be the target final diagnostic backbone only after mechanism gates pass, not an unconditional final backbone yet.

Accepted points:

1. MotionGPT is the strongest current target for EventProbe because the local code uses a T5 conditional generator over text and motion tokens, plus VAE decoding to joints. This gives a practical route to text-token / motion-token / hidden-state probing.
2. MoGenTS remains valuable as a structural temporal baseline and fallback, especially because the first geometry and training-entry smoke passed.
3. TMR should stay in the evaluator stack as a semantic side signal. It is not a generator, and using it as both judge and player would contaminate claims.

Guardrail:

1. MotionGPT's current local generation path does not directly export attention / hidden-state traces. M1 must instrument HuggingFace T5 generation or hooks before any paper claim says attention evidence is available.
2. AToM preference fine-tuning assets are not yet complete locally, so MotionGPT base is the immediate mechanism-probe target; AToM-style alignment is a later method layer.

## 2. Eligibility Gate

Backbone hard gate:

1. `training_entry`: documented training code for the generator / tokenizer stack.
2. `inference_entry`: documented text-to-motion generation, composition, or control inference.
3. `eval_entry`: documented generation evaluation, not visualization only.
4. `local_asset`: local checkpoint or already produced local runnable outputs.
5. `output_bridge`: output can be audited as `(T,22,3)` joints or has a tested bridge to evaluator space.
6. `event_temporal_fit`: the method has an explicit event, action-plan, ordering, streaming, temporal-control, or spatial-temporal representation hook.

If the first three entries are missing, the repo is not a backbone candidate. If only the sixth entry is weak, the repo can be a runnable baseline but not a core event-aware candidate.

Evaluator hard gate:

1. clear scoring input and output;
2. explicit condition pair, such as `full_text vs drop_text` or `full_text vs shuffle_text`;
3. reported coverage, event bucket, evaluable `n`, checkpoint/source, protocol, role, and limitations;
4. no reuse of the same scorer/protocol as both reward scorer and final evaluator for the same claim.

## 3. Generation Candidate Matrix


| Candidate            | Event / temporal fit                                                                                                              | Complete loop status                                                                               | Current role                                          | Decision                                                                                     |
| -------------------- | --------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------- | ----------------------------------------------------- | -------------------------------------------------------------------------------------------- |
| MotionGPT base       | strongest diagnostic fit: text-token / motion-token generation can support event-level internal probes                            | local repo exposes train / demo / test and a local pretrained checkpoint                           | target final diagnostic backbone, pending M0-M3 gates | run MotionGPT mechanism gate before locking final backbone                                   |
| AToM alignment layer | event-level alignment is conceptually relevant to later correction / reward design                                                | preference / finetune assets need repair before retrain validation                                 | later method layer                                    | repair only after MotionGPT base passes mechanism gate                                       |
| LaMP                 | language-motion pretraining may help semantic grounding and event phrasing                                                        | local repo has training / generation / evaluation scripts but current asset paths are inconsistent | blocked until path/assets are repaired                | do not occupy GPU in current round                                                           |
| DART                 | temporal / streaming / action-timeline control is highly relevant                                                                 | training, rollout, and evaluation scripts exist locally, but representation bridge is heavy        | later temporal-control candidate                      | defer until 22j/evaluator bridge cost is explicit                                            |
| ActionPlan           | frame-level action plan is highly relevant to multi-event temporal planning                                                       | current release is not a complete training/eval loop                                               | concept reference                                     | exclude as current backbone                                                                  |
| MoGenTS              | spatial-temporal joint modeling and 22j output are useful, but CLIP global text conditioning limits token-level event attribution | complete local training / inference / eval and HumanML3D assets                                    | validated structural temporal baseline / fallback     | use for smoke sanity and cross-backbone comparison, not as the main mechanism-probe backbone |
| MoMask               | mature HumanML3D 22j generation baseline; weak event/temporal mechanism                                                           | complete local training / inference / eval and pretrained assets                                   | runnable generic sanity baseline                      | use as baseline only                                                                         |
| ReAlign              | reward-guided alignment is relevant to PerceptGuide comparison                                                                    | local readiness is partial                                                                         | method comparison reference                           | exclude from first backbone round                                                            |


## 4. Evaluator / Scorer Matrix


| Evaluator / sidecar                       | Best use                                                                                                          | Boundary                                                                                             | Decision                                             |
| ----------------------------------------- | ----------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------- | ---------------------------------------------------- |
| TMR                                       | global semantic compatibility; omission and replacement paired diagnostics; cross-check against chronology scorer | not event-aware, not ordering-reliable, not final judge                                              | include as semantic side signal                      |
| ChronAccRet                               | chronology-sensitive `full_text vs shuffle_text` / CAR evidence                                                   | not full event correctness; no standalone duration/frequency guarantee; not held-out final evaluator | include as temporal side signal with coverage report |
| MotionPatches / TAMR-style representation | representation audit, possible local body-part / patch evidence, semantic retrieval sidecar                       | not a generation backbone; no verified event-order protocol by default                               | audit as sidecar, not main evaluator                 |
| AToM-style GPT-4V judge                   | expensive event-level external sidecar or human-calibration proxy                                                 | not current automatic main evaluator; cost and reproducibility risk                                  | optional calibration aid                             |
| Human calibration                         | final anchor for sampled cases                                                                                    | not reward scorer                                                                                    | required before final failure-rate claims            |


Short TMR rule:

```text
TMR: semantic scorer + diagnostic baseline; not an event-aware evaluator, not a final judge.
```

There is no current evaluator that is a complete, dimension-reliable, event-aware strict upper bound over TMR, ChronAccRet, MotionPatches, and human review. The plan is a role-separated evaluator stack, not a single automatic replacement.

## 5. Revised Experiment Plan

### B1: Evaluator Readiness

**Status**: next.
**Goal**: define reusable automatic side signals before trusting any new generated motions.
**Scope**: no full test split.

Protocol:

1. Confirm TMR input format for GT and generated motion candidates.
2. Confirm ChronAccRet event-text adapter coverage, event bucket, and `full_text vs shuffle_text` protocol.
3. Audit MotionPatches/TAMR-style local readiness as a representation sidecar.
4. Record checkpoint/source, protocol, motion format, role, limitations, and artifact path.

Pass condition: each retained scorer has a documented role and cannot be mistaken for final evaluator.

### B2: Backbone Smoke Gate

**Status**: started on 2026-05-07 with event/temporal battery.
**Scope**: no full test split. First launch used six paired event/temporal prompts under `artifacts/modebug_backbone_audit/prompts/event_temporal_battery.tsv` and candidate-specific prompt files.

Priority after 2026-05-07 closure:

1. MotionGPT base: immediate target for M0/M1 event/temporal generation and mechanism-trace gate.
2. MoGenTS: launched and passed pretrained geometry + training-entry launch smoke; keep as structural temporal baseline / fallback.
3. AToM alignment layer: conceptually relevant, but finetune/retrain assets are incomplete; do not use as retrain-validation GPU yet.
4. LaMP: blocked by hard-coded paths / missing expected local model tar / missing local dataset link; repair before launch.
5. MoMask and DART: excluded from this round because they were already reliability-validated outside this audit.

Protocol:

1. Generate one motion per prompt.
2. Export static skeleton or canonical joint representation.
3. Report `joints_abs_mean`, min, max, finite rate, length, seed, checkpoint, prompt adapter, motion format, and output path.
4. Save static skeleton plots for every pass/fail sample.

Pass condition: generated joints are in the same order of magnitude as HumanML3D-E GT and visually non-degenerate on static skeleton plots.

### B2 Result: MoGenTS 2026-05-07

**Status**: first gate passed.

Artifacts:


| Artifact               | Path                                                                                  |
| ---------------------- | ------------------------------------------------------------------------------------- |
| launch manifest        | `artifacts/modebug_backbone_audit/launch_manifest_20260507.md`                        |
| MoGenTS result summary | `artifacts/modebug_backbone_audit/mogents/result_summary_20260507.md`                 |
| geometry audit CSV     | `artifacts/modebug_backbone_audit/mogents/geometry_audit_20260507/geometry_audit.csv` |
| static plots           | `artifacts/modebug_backbone_audit/mogents/geometry_audit_20260507/static_plots/`      |


Non-IK geometry summary:


| Field           | Range                        |
| --------------- | ---------------------------- |
| shape           | `196x22x3` for all 6 samples |
| finite_rate     | `1.0` for all 6 samples      |
| joints_abs_mean | `0.493075` to `1.105252`     |
| min             | `-2.489685` to `-0.255091`   |
| max             | `1.619924` to `3.311733`     |
| mean_joint_step | `0.009274` to `0.047006`     |
| max_joint_step  | `0.141135` to `0.488947`     |


Retrain smoke:


| Evidence                                            | Status      |
| --------------------------------------------------- | ----------- |
| VQ training command launches in `mogents` conda env | passed      |
| opt/log/code snapshot written                       | passed      |
| cuda selected                                       | passed      |
| evaluator loaded                                    | passed      |
| model instantiated                                  | passed      |
| dataset reached                                     | passed      |
| full epoch/convergence                              | not claimed |


Interpretation: MoGenTS is reliable enough to keep as the first active generated-motion candidate. This is not yet an event-ordering success claim; event/temporal behavior must be judged by visual inspection plus side-signal evaluators in B4.

### M0/M1: MotionGPT Mechanism Gate

**Status**: next.
**Goal**: decide whether MotionGPT can be locked as the final MoDebug diagnostic backbone rather than only a runnable baseline.

Why MotionGPT is prioritized:

1. The local MotionGPT repo has documented training, demo, and test entries, plus a local pretrained `motiongpt_s3_h3d.tar` checkpoint.
2. The implementation uses T5 conditional generation with added motion tokens, then decodes motion tokens through the motion VAE. This is a better fit for text-token / motion-token diagnosis than global text-vector conditioning.
3. MotionGPT supports generation tasks beyond plain T2M, including prediction and in-between paths, which keeps temporal conditioning within the same architecture family.

What must be verified before locking it:


| Gate                         | Required evidence                                                                                                                                            | Pass condition                                                                                                          |
| ---------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------ | ----------------------------------------------------------------------------------------------------------------------- |
| M0 pretrained geometry       | run the six-prompt event/temporal battery with fixed seed and save `(T,22,3)` or equivalent joint output plus static skeletons                               | finite joints, HumanML3D-scale ranges, no EventT2M-style skeleton explosion                                             |
| M1 trace export              | instrument generation to save input text tokens, generated motion token IDs, decoder attention or hidden states, logits, entropy, and sampled token sequence | traces are reproducible and can be aligned to `full_text / drop_text / shuffle_text / replace_text` conditions          |
| M2 counterfactual contrast   | run paired prompts under identical config and compare trace deltas before relying on output-level scores                                                     | omission / wrong-event / order-failure cases show inspectable internal differences                                      |
| M3 retrain or finetune smoke | launch MotionGPT stage training or a repaired AToM-style finetune path                                                                                       | training entry reaches dataset/model/evaluator without missing-asset failure; convergence is not claimed at smoke stage |


Caveat: DS's attention argument is usable as a research direction, not yet as recorded evidence. Current code calls HuggingFace T5 generation but does not directly write attention / hidden-state artifacts. The first MotionGPT implementation task is therefore instrumentation, not metric reporting.

### B3: Event-Counterfactual Adapter

**Status**: pending B1/B2/M0/M1.

MVP text conditions:


| Condition      | Definition                                                    |
| -------------- | ------------------------------------------------------------- |
| `full_text`    | original caption or concatenated event list in original order |
| `drop_text`    | same event list with one target event removed                 |
| `shuffle_text` | same event list with order shuffled                           |
| `replace_text` | optional diagnostic until replacement policy is fixed         |


Adapter must not depend on EventT2M decomposed input or EventT2M-specific runtime code.

### B4: S7 Replacement-Min

**Status**: pending B3.

Metrics:


| Metric family                   | Evaluator                        | Role                                                                |
| ------------------------------- | -------------------------------- | ------------------------------------------------------------------- |
| semantic omission / replacement | TMR                              | side signal                                                         |
| temporal ordering               | ChronAccRet                      | side signal / formal ordering evidence only if coverage is reported |
| representation sanity           | MotionPatches/TAMR-style sidecar | cross-check                                                         |
| static skeleton scale           | local geometry audit             | backbone sanity                                                     |
| human calibration               | human or explicit external judge | final anchor for small sampled set                                  |


Boundary: automatic evaluator outputs remain side signals until calibrated. Do not write final failure rates from B4 alone.

### B5: S8 Attribution and PerceptGuide Gate

**Status**: pending S7 replacement-min.

Rules:

1. First compare cross-backbone failure patterns.
2. Only instrument repo-specific internals if the failure pattern is stable and the hooks are cheap.
3. Upgrade PerceptGuide from reward-side asset to method only if S8 gives a mechanism-driven correction target.
4. Keep reward metric gains separate from final generation improvement claims.

## 6. Decision Matrix


| Route                              | Keep as active backbone?                                                       | Keep as evaluator?                     | Immediate action                                                          |
| ---------------------------------- | ------------------------------------------------------------------------------ | -------------------------------------- | ------------------------------------------------------------------------- |
| MotionGPT base                     | target final diagnostic backbone if M0-M3 pass                                 | no                                     | run M0/M1 event/temporal generation plus internal-trace instrumentation   |
| AToM alignment layer               | later method layer, pending missing preference assets                          | AToM-style judge optional sidecar only | repair assets only after MotionGPT base passes mechanism gate             |
| DART                               | later                                                                          | no                                     | defer until bridge cost is justified                                      |
| ActionPlan                         | no                                                                             | no                                     | concept reference only                                                    |
| LaMP                               | no, currently blocked                                                          | no                                     | repair hard-coded paths / expected model tar / dataset link before launch |
| MoGenTS                            | yes as structural temporal baseline / fallback, not primary mechanism backbone | no                                     | keep MoGenTS outputs for cross-backbone comparison after MotionGPT M0/M1  |
| MoMask                             | excluded from current round                                                    | no                                     | already reliability-validated; keep as external baseline                  |
| TMR                                | no                                                                             | semantic side signal                   | include in B1                                                             |
| ChronAccRet                        | no                                                                             | temporal ordering side signal          | include in B1                                                             |
| MotionPatches / TAMR-style sidecar | no                                                                             | representation / retrieval sidecar     | audit in B1                                                               |


## 7. Drift Note

old_plan -> replacement backbone selection was biased toward complete HumanML3D T2M loops and still documented EventT2M as failed rows inside the active decision matrix

new_plan -> EventT2M is removed from active eval/backbone consideration; candidates are separated into generation routes and evaluator/sidecar roles; event / temporal relevance is a hard ranking criterion after complete-loop eligibility

evidence -> EventT2M-era generated-motion scale audit and historical notes are retained in `blocked/`; current plan does not reuse those generated motions or EventT2M runtime as active evidence

affected_docs -> README, blocked index, archived index, migration plan, directory layout

2026-05-07 refinement -> old_plan: post-hoc repair route depended on explicit generated-motion slicing and local artifact recognition; new_plan: prioritize in-process mechanistic probing under counterfactual text conditions; evidence: MotionGPT's T5 + motion-token architecture is instrumentable but not yet traced, while MoGenTS is reliable but text-global; affected_docs: README and migration plan; next_action: MotionGPT M0/M1 gate before final backbone lock

next_action -> MotionGPT M0/M1 mechanism gate, B1 evaluator readiness, and MoGenTS baseline cross-check after MotionGPT outputs exist