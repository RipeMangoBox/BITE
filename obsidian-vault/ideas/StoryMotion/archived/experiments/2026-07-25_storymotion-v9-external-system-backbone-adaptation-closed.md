---
title: "StoryMotion v9 External System and Backbone Adaptation — Closed Plan"
status: archived
hypothesis: |
  The failed Human128 topology screen supports a mismatch among Stage2
  architecture, inductive bias, objective, and C3 latent topology, but does not
  isolate parameter capacity. External full-system controls and fixed-C3
  matched-backbone arms must be separated before any joint extension.
tags:
  - StoryMotion
  - stage2
  - external-system
  - backbone
  - human-first
  - camera-completion
  - diagnostic
  - version/v9
  - status/archived
aliases:
  - StoryMotion-External-Backbone-Adaptation
source_notes:
  - "[[current]]"
  - "[[2026-07-18_storymotion-latent-generatability-stage2-diagnostic-ladder]]"
  - "[[StoryMotion-valid-metric-ledger]]"
  - "[[StoryMotion-metric-computation-io]]"
created: 2026-07-24T21:00:00+08:00
updated: 2026-07-25
archived: 2026-07-25
superseded_by: "[[current]]"
---

# StoryMotion v9 External System and Backbone Adaptation — Closed Plan

> [!warning] 已归档
> 本页保留 E1–E4 的 interface、variable matrix、preflight、observability 与 stop/continue preregistration。其早期“无长训/E3 未实现”执行状态已由后续用户授权与 fresh `105K` runs 取代；当前裁决见 [[current]]，正式数值与 hashes 只见 [[StoryMotion-valid-metric-ledger]]，完成事件见 [[version_family]]。

> [!abstract] 归档的预长训裁决
> [[2026-07-18_storymotion-latent-generatability-stage2-diagnostic-ladder#4.2 P0-H128-S2 stop/continue screen|P0-H128-S2]] 已按 N=512 hard gate 停止；E1 G-SYS-H 与 E2 D-SYS-C 的 N=512 short screen 也分别触发 stop。没有 E1/E2 长训授权，也没有获准的 E3/E4 实现或训练；早于本轮存在的 E4 草稿骨架保持隔离，不能作为 contract、run 或 evidence。现有证据仍只支持 Stage2 architecture、inductive bias、objective 与 latent topology 的组合不匹配；没有资格宣称参数容量或“Stage2 backbone 能力上限不足”已被单独证明。C3-25 seed17 105K Unified-3 保持 mainline。

外部来源固定为 [GestureLSM repository](https://github.com/andypinxinliu/GestureLSM)、[GestureLSM paper](https://arxiv.org/abs/2501.18898)、[DanceCamera3D repository](https://github.com/Carmenw1203/DanceCamera3D-Official) 与 [DanceCamera3D paper](https://openaccess.thecvf.com/content/CVPR2024/html/Wang_DanceCamera3D_3D_Camera_Movement_Synthesis_with_Music_and_Dance_CVPR_2024_paper.html)。

## 1. External provenance and license boundary

| external source | exact code revision | code license | dependency baseline | data/license boundary |
| --- | --- | --- | --- | --- |
| GestureLSM | `main` at `f52ac2f53dd1b99beb74bbcdbdf1a98118a36a70` | MIT | README: Python 3.12, PyTorch 2.1.2, torchvision and torchaudio 0.16.2, CUDA 11.8; requirements additionally include diffusers 0.32.0 and NumPy 1.26.2 | Code license does not license BEAT2, SMPL-X, speech, transcript, or other upstream data/assets |
| DanceCamera3D-Official | `master` at `9159b4b9e1195edaeed04d2ee9f28f29e61df123` | MIT | README: Python 3.7+, PyTorch 1.12.1; validated stack lists Python 3.7.12, PyTorch 1.13.1, CUDA 11.6 | DCM dataset is academic-use-only under a separate EULA and upstream provider rules; it is not covered by the MIT code license |
| PulpMotion code/data adapter | local code at `b81c7d95d5d9d58c6a8b76775c658eecfba74262` | code MIT; public data repository declares MIT | existing Pulp official evaluator environment remains isolated from both external environments | SMPL, SMPLify, SMPL-X and separately downloaded model assets retain their own registration/license terms |

Fresh clones live outside the StoryMotion worktree under `StoryMotion-external-controls/20260724/`. Adapter code enters StoryMotion only through `experiments/stage2_backbone_upper_bound/`; no external default trainer is edited and no StoryMotion mainline trainer default changes.

## 2. Four-arm interface map

| arm | causal question | input and condition | prediction | representation and decoder | evidence class |
| --- | --- | --- | --- | --- | --- |
| E1 G-SYS-H | Can a GestureLSM-style complete Human system establish a higher Pulp Human upper bound? | Pulp Human text replaces the transcript/text semantic branch; speech waveform, onset and amplitude are absent and explicitly masked/zeroed, not synthesized | upper, hands and lower Human regions, then unified Human motion | new part-wise RVQ-VAE plus GestureLSM Stage2; final decode must map to Human199/raw skeleton evaluator | system-level control |
| E2 D-SYS-C | Can a DanceCamera3D-style complete system improve observed-Human Camera completion/framing? | observed raw Human199 or decoded Human plus Camera text; music is removed, and Camera text is a separate condition rather than relabeled music | raw camera14-compatible Camera trajectory | DC3D-style raw Camera system; canonical camera14 conversion and evaluator | system-level Direct-C control |
| E3 C3-D-DC | Does a DC3D transformer topology improve Direct-C with the C3 representation and objective fixed? | observed normalized Human128 plus Camera text512 | normalized Camera64 | frozen C3-25 Stage1/cache/stats/owning decoder | matched-backbone Direct-C arm |
| E4 C3-G-DH | Does a GestureLSM temporal topology improve Direct-H with the C3 representation and objective fixed? | Human text512 only | normalized Human128 | frozen C3-25 Stage1/cache/stats/Human decoder | matched-backbone Direct-H arm |

E1 changes tokenizer, region topology, condition contract, objective implementation and backbone together. E2 changes raw representation, condition contract, objective implementation and backbone together. Neither is single-variable backbone evidence. E2 and E3 consume observed Human and therefore are Camera completion, not joint generation.

## 3. Variable and attribution matrix

| arm | Stage1/tokenizer | latent or raw representation | condition | first-screen objective and schedule | backbone | evaluator |
| --- | --- | --- | --- | --- | --- | --- |
| E1 G-SYS-H | changed to three part-wise RVQ-VAEs | changed to upper, hands and lower discrete latents | changed from speech/audio/transcript to Pulp Human text with missing-acoustic mask | native system objective; exact selected GestureLSM mode must be named and flow, shortcut, reflow and DDIM must not be mixed | GestureLSM spatial-temporal system | fixed Human199/raw skeleton output contract |
| E2 D-SYS-C | no C3 tokenizer contract | raw Human plus raw camera14-compatible output | observed Human plus Camera text; music removed | native DC3D x0 diffusion system control | DC3D transformer and body conditioning | fixed canonical camera14 evaluator |
| E3 C3-D-DC | fixed C3-25 | fixed H128 input and C64 target | fixed observed Human128 plus Camera text512 | fixed StoryMotion START_X, cosine schedule, time sampling, sample exposure and DDIM50 | only DC3D-style transformer topology changes | fixed Direct-C camera14 evaluator |
| E4 C3-G-DH | fixed C3-25 | fixed H128 target | fixed Human text512 only | fixed StoryMotion START_X, cosine schedule, time sampling, loss normalization, sample exposure and DDIM50 | only GestureLSM-style temporal topology changes in the first screen | fixed Direct-H Human199/raw skeleton evaluator |

DC3D velocity, acceleration and body-attention losses are excluded from E3 first screen. GestureLSM flow matching, latent shortcut, reflow, MeanFlow and a new RVQ tokenizer are excluded from E4 first screen. Adding any of these creates a separately named second axis.

## 4. Dense Human128 to GestureLSM token contract

E4 first screen uses one dense Human token per latent frame. This preserves the frozen C3 Human128 cache and adds only input/output projections required by the selected temporal block. With one token, GestureLSM spatial attention degenerates to an identity-sized spatial set; therefore a failed E4 first screen cannot reject GestureLSM's original body-part inductive bias.

An optional later `E4-TOK` intervention may learn three explicit upper/hands/lower projections from Human128 and a matched inverse merge to Human128. It must record projection dimensions, parameters, initialization, token order and inverse mapping. `E4-TOK` is a new topology intervention, not the E4 backbone-only result, because C3 latent channels have no established anatomical partition.

## 5. Native system condition adaptations

For E1, the Pulp Human caption is encoded through the GestureLSM transcript/text semantic path. Acoustic waveform, onset and amplitude are represented by an explicit missing-condition mask and zero tensors with fixed shapes. No text-to-speech audio is synthesized. Stage1 reports reconstruction floors separately for upper, hands and lower before any Stage2 claim.

For E2, observed Human199 is the motion condition. Camera text is encoded as its own condition branch. The music/Jukebox branch is removed for the first system control; zeroing a live music branch is not treated as equivalent unless its effect is separately audited. Output is converted to canonical camera14 before scoring. Given observed Human, the result is Direct-C/framing only.

## 6. Pre-optimizer contract and tests

Every arm receives a unique `experiment_contract.json` before optimizer construction. It records the single causal question; fixed and changed variables; external commit, branch, code license and adapter SHA256; Stage1/checkpoint/decoder/cache/normalization hashes; raw and latent shapes; condition sources and missing-condition behavior; objective, prediction target, time/noise sampling and sampler; trainable parameters and reproducible compute estimate; batch and branch sample exposure; ordered IDs, seed, eval batch and sample count; short checkpoint and stop/continue gate; run root, host, physical GPU and environment path.

All four arms also have a fail-closed observability contract:

- TensorBoard is enabled under the immutable run root at `tensorboard/`; training loss components, learning rate, gradient norm and branch/sample exposure are logged with global step. E1 additionally separates Stage1 part reconstruction and Stage2 generation losses; E2/E3 separate reconstruction, velocity, acceleration and framing terms when those terms exist; E4 separates the fixed StoryMotion prediction loss from any later, separately contracted axis.
- Required checkpoint milestones are `ceil(0.2 × total_steps)`, `ceil(0.4 × total_steps)`, `ceil(0.6 × total_steps)`, `ceil(0.8 × total_steps)` and `total_steps`. Thus a 5K screen saves 1K/2K/3K/4K/5K, and a 105K run saves 21K/42K/63K/84K/105K. Extra diagnostic checkpoints are allowed but cannot replace these milestones.
- CLI snapshot steps and `compute.checkpoint_steps` must both contain every required milestone; `compute.tensorboard.enabled` must be true and `compute.tensorboard.log_dir` must be exactly `tensorboard`. Validation runs before optimizer construction.
- Existing E1/E2 5K screen roots predate this requirement and contain neither a complete run-local TensorBoard history nor all 20% milestones. They remain immutable historical screen evidence and are not retroactively declared compliant. Any new short or long run must use a fresh root and pass the new audit.

The isolated E1 deployment currently resolves PyTorch `2.1.0+cu118` and TensorBoard `2.20.0`; the isolated E2 repair deployment resolves PyTorch `2.8.0+cu128` and TensorBoard `2.20.0`. Both completed a real event-file scalar round-trip in their owning environment. These deployed versions are recorded separately from the native repository README baselines and do not modify the StoryMotion main environment.

The launch sequence is fixed:

1. import plus forward/backward unit test;
2. explicit Stage1 and Stage2 `is_causal is False` assertion where StoryMotion components are used;
3. one-batch overfit;
4. owning-decoder round-trip;
5. deterministic 32-sample generation smoke;
6. metric I/O contract audit;
7. optimizer-free run-contract audit.

No 105K or full external-system run is authorized by these preflights. The first optimizer run is a preregistered short screen in a fresh immutable run root.

## 7. Stop/continue contracts

| arm | short-screen stop | short-screen continue |
| --- | --- | --- |
| E1 G-SYS-H | any part reconstruction floor is worse than its declared control; unified Human199 mapping is invalid; decoded Human semantic, coverage or physical diagnostics collapse | all three part floors are auditable, unified mapping passes, and decoded Human is credible enough to justify the preregistered Stage2 system screen |
| E2 D-SYS-C | camera14 conversion or observed-Human contract fails; FDCLaTr, CLaTr, coverage, framing, trajectory or joint geometry broadly regress | Direct-C/framing forms a camera Pareto improvement without changing the observed-Human boundary |
| E3 C3-D-DC | matched variables differ; Direct-C camera metrics or framing broadly regress | fixed-C3 Direct-C passes the canonical Camera gate, authorizing a separately contracted H128+C64 joint-output design |
| E4 C3-G-DH | matched variables differ; FDTMR, TMR, HCov, pose, heading, global/root or physical quality broadly regress | Direct-H forms a Human Pareto improvement or strict non-inferiority and passes fixed/blind physical review, authorizing a separately contracted joint extension |

E1 pass plus E4 fail attributes any advantage to the tokenizer/objective/condition/backbone system, not the backbone alone. E4 pass under fixed C3 and fixed objective supports architecture/inductive bias as a major factor. E4 pass only after flow or RVQ changes supports a system interaction, not a pure-backbone explanation. E2 or E3 pass proves Camera completion only. A joint-only pass without Direct-H does not resolve the Human blocker.

### 7.1 Closed short-screen decisions

- E1 Stage1 produced auditable lower/torso/arms reconstruction floors, but its Stage2 5K N=512 screen failed Human semantic/coverage, latent-to-decoded agreement and fixed/blind physical-quality gates. Decision: stop; no 105K.
- E2 original, bounded-FOV and no-framing variants all failed the canonical observed-Human Camera completion gate. The final repair improved some geometric axes but collapsed Camera-language alignment and left a majority out of frame. Decision: stop; no 105K.
- These are system-control failures. They neither prove nor disprove a fixed-C3 backbone-only intervention. Exact screen values and hashes are owned by [[StoryMotion-valid-metric-ledger]].

## 8. Resource schedule and compute accounting

| physical slot | current assignment | next authorized assignment | concurrency guard |
| --- | --- | --- | --- |
| 5090 GPU2 | released after E2 repair screen | none under the closed E1/E2 gates | at most one StoryMotion train or eval process |
| 4090 GPU0 | released after E1 screen | none under the closed E1/E2 gates | at most one training process |
| 4090 GPU1 | released after E2 formal eval | none under the closed E1/E2 gates | at most one training process |

E1 and E2 environments are separate from each other and from StoryMotion. Native paper-scale compute is not a launch budget: GestureLSM reports single-A100 training, while DanceCamera3D reports a six-3090 validation stack and 52.7M native transformer. Each adapter must instrument its actual parameter count and either FLOPs or a reproducible forward/backward compute proxy before optimizer creation.

Per the execution boundary agreed with the user, E3/E4 implementation is deferred until a successful long run first justifies drafting their detailed pipeline modification plan and flowchart, followed by explicit user confirmation. Because both current system-control screens stopped before long training, that trigger has not fired. A pre-existing E4 draft directory is quarantined as an unauthorized skeleton: it must not construct an optimizer, launch a run or be cited as E4 evidence, and any later approved implementation must be reviewed against the newly agreed design rather than silently reusing it. Idle hardware does not override a failed causal gate.

## 9. Claim boundary

Current eligibility is:

- qualified: “The current C3 Human128 single-branch topology failed its matched short gate, strengthening a broader Stage2 architecture/inductive-bias/objective/latent-topology mismatch hypothesis.”
- not qualified: “Stage2 parameter capacity is the root cause” or “the current backbone has reached a proven capability ceiling.”
- not qualified: any three-mode claim from E1, E2, E3, E4 or a joint-only exploratory checkpoint.
- future three-mode evidence: one checkpoint evaluated in Direct-H, Direct-C and joint parallel; cascade remains optional attribution only.

Joint-only arms remain deferred until E3 or E4 passes its direct gate. If launched earlier by explicit user override, they are named exploratory multi-axis joint diagnostics and cannot promote a backbone, capacity or three-mode conclusion.

## 10. v9 closure

后续用户明确授权了 fresh long runs；该授权 supersede 本页第 8 节的旧 queue state，但不改变 interface、因果边界或 gate：

- E1 Stage1 pure4,053 part-wise RVQ reconstruction floor 通过；E1 Stage2 `105K` Human generation 因 semantic/coverage broad regression 停止。
- E2 使用正确 train-only MinMax 完成 `105K` observed-Human Camera completion；相对 5K 可学习性恢复，但相对 C3 Direct-C 仍 broad regress，停止。
- E3 fixed-C3 `105K` Direct-C 改善 trajectory/rotation，却牺牲 semantic/coverage，按 matched gate 停止。
- E4 未评估；joint extension 未授权；C3-25 Unified-3 `105K` 保持 mainline。

正式数值与 hashes 只见 [[StoryMotion-valid-metric-ledger#4.10 v9 external long-run N=512 screens]]，当前 claim boundary 只见 [[current]]。
