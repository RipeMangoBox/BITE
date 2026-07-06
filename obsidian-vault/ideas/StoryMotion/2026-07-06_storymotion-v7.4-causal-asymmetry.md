---
title: "StoryMotion v7.4 Causal Asymmetry Diagnosis"
status: active
hypothesis: |
  StoryMotion v7.4 reframes the core Stage2 problem as a causal-direction mismatch: camera motion is represented relative to human root and should depend on human motion, but the current joint denoiser treats human and camera branches as symmetric peers. The current evidence supports a strong JOINT human dependency on raw camera latent state. The first minimal repair, asymmetric human-input shuffle, is rejected by full JOINT eval: it improves camera completion and roughly preserves human completion, but worsens JOINT human/camera metrics.
tags:
  - StoryMotion
  - Motion_Generation
  - architecture
  - causality
  - experiment
  - status/active
aliases:
  - StoryMotion-v7.4
source_notes:
  - "[[2026-07-03_storymotion-v7.3.1]]"
  - "[[2026-07-01_storymotion-v7.3.1-metric-data]]"
  - "[[archived/2026-06-23_storymotion-decoupled-coupling-qa-v5.1]]"
  - "[[archived/2026-06-16_storymotion-v3-formal]]"
created: 2026-07-06T00:00:00+0800
updated: 2026-07-06T16:02:00+0800
---

# StoryMotion v7.4 Causal Asymmetry Diagnosis

> [!abstract] 核心裁决
> v7.4 不把 v7.3.1 的 reliability schedule 当成主问题。更根本的问题是：StoryMotion 的物理依赖方向应接近 `H -> C`，但当前 Stage2 在 JOINT 中同步预测 `H` 和 `C`，等价于把本应单向的 camera-on-human 关系实现成对称耦合。2026-07-06 的 full JOINT intervention 显示，JOINT human 对 raw camera latent state 有强实例依赖；但第一版最小修法 `asym_human_input_shuffle_e3` 被 full JOINT eval 否决。它不能作为 v7.4 方法，只能作为机制诊断。

完整数值证据仍见 [[2026-07-01_storymotion-v7.3.1-metric-data]]；v7.3.1 路线裁决见 [[2026-07-03_storymotion-v7.3.1]]；早期 root / camera condition 诊断见 [[archived/2026-06-23_storymotion-decoupled-coupling-qa-v5.1]] 和 [[archived/2026-06-16_storymotion-v3-formal]]。

## 1. 最根本问题

表层问题是 v7.3.1 的 e3 `one-hot task + reliability schedule` 只带来局部改进，仍弱于旧 v6 clean unified baseline。更深一层的问题不是 schedule，而是 JOINT 的建模方向错了。

理论上，human motion 与 camera motion 的依赖应近似为：

```text
P(H, C | text, intent)
  = P(intent | text)
  · P(H | text_h, intent)
  · P(C | H, text_c, intent, framing)
```

其中：

- `H` 是 human root / body / action phase。
- `C` 是 camera trajectory / shot / framing。
- `intent` 是导演意图、staging、节奏、构图等高层变量。

这意味着 camera 可以依赖 human，但 raw camera trajectory 不应直接支配 human motion。当前 Stage2 的危险点是同步 denoising：

```text
concat([z_hum, z_cam]) -> shared joint denoiser -> [H_hat, C_hat]
```

如果 shared denoiser、cross-branch attention、loss 或 latent replacement 允许 `C` 的预测误差反向影响 `H`，则 JOINT 下 human 会被 camera 分支污染。clean human completion 好而 JOINT human 退化，正符合这个失配。

## 2. 已知证据与证据边界

| item | current status | meaning |
| --- | --- | --- |
| camera representation depends on human root | established | camera feature uses relative relation to human root, and decode adds human root back |
| current JOINT predicts human and camera together | established | simultaneous branch denoising can create root-level circular dependency |
| observed camera latent strongly affects human completion | established in archived intervention | camera latent is a strong condition; camera text half is weak in that setting |
| v7.3.1 reliability schedule improves JOINT locally | established | e3 improves over e2 on JOINT but still below v6 clean |
| JOINT human depends on camera latent state | established by 2026-07-06 full JOINT intervention | raw camera latent perturbation strongly degrades human-relevant TMR/CLaTr metrics |
| root-first / asymmetric factorization improves results | unproven | architecture candidate, not paper claim |
| capacity is not the cause | unproven | must be ruled out before strong causal-structure claim |

The key evidence boundary is strict: v7.4 may claim that current evidence exposes a raw camera-latent dependency / representation-intrusion risk in JOINT. It cannot yet claim that causal asymmetric factorization solves StoryMotion. Because zero / noise camera-state interventions make human metrics worse rather than better, the current problem is not “remove camera and human recovers”; the stricter claim is that JOINT human has learned an unsafe dependence on instance-level camera state, which may contain both useful and harmful information.

## 3. 理想表现

在物理 camera view 定义下，理想 JOINT 应满足：

- human branch primarily follows `text_h / action / intent` rather than raw camera prediction.
- camera branch follows `H` plus `text_c / shot / framing`.
- perturbing camera branch should not materially change human motion when the body remains visible and unoccluded.
- generated human should remain visually close to clean human completion quality under the same human text and seed.

这个不变量有边界：若 camera edit 改变 crop、occlusion、visibility 或 actor framing，使 body 不再完整可见，那么 human recovery 可能发生变化，这不是 causal leakage，而是任务定义改变。

## 4. 手动改 camera 的副作用定义

用户手动改 camera 后 human 是否应改变，取决于 camera 的语义层级。

| camera meaning | should human change? | v7.4 decision |
| --- | --- | --- |
| physical viewpoint / observer motion | no, except visibility/crop constraints | camera is downstream of human; use framing correction or camera optimization |
| director intent / staging / shot semantics | yes, but through high-level intent | raw camera latent should not directly drive human |
| generated camera from previous model | no direct trust | treat as unreliable condition with source quality metadata |

因此 v7.4 不把 “camera 改了 human 不变” 当成缺陷本身。真正的缺陷是：模型没有区分 physical camera、director intent 和 unreliable generated camera，而是让 raw camera branch 有机会直接影响 human branch。

## 5. 一票否决诊断

v7.4 的第一目标不是训练新大模型，而是把已经完成的相关 intervention 与尚未完成的真正 JOINT 因果干预分开。[[2026-07-01_storymotion-v7.3.1-metric-data]] 已经完成了若干强相关诊断，但它们不能直接等同于下面的 JOINT veto。

已完成的相关诊断：

| completed diagnostic | where | what it proves | what it does not prove |
| --- | --- | --- | --- |
| Mode B camera-latent causal gate | metric-data §6.3 | human completion 依赖 observed camera latent；zero / shuffle / noise camera latent 会显著改变 one-step human loss | 不等于 JOINT 生成中 camera branch 预测误差会污染 human branch |
| visible-branch reliance | metric-data §6.3 | completion 不是只靠 text shortcut，visible branch 被模型使用 | 没有定位 JOINT 下 `C -> H` leakage |
| camera text / noise probes | metric-data §8.1 | camera text 干预弱，observed-source noise 会暴露 H2C fragility | 主要是 H2C / camera-side reliability，不是 JOINT human 退化因果证据 |
| Stage2 joint qualitative visualization | metric-data §7 | 已有 JOINT / human completion / camera completion 可视化入口 | 不是系统的 paired render audit，也不是 camera-branch do-intervention |

因此，v7.4 中 “JOINT camera-branch intervention” 的准确含义是：在 JOINT sampling/eval 中固定 human text、human seed 和 visibility-safe case，只替换、清零或打乱 camera branch 条件 / intermediate latent / predicted camera path，并检查 human output 是否变化。2026-07-06 已完成 full JOINT latent-state intervention；它把假设从“可能有 camera 反向污染”推进到“human 对 raw camera latent state 有强实例依赖”。

| priority | experiment | success / failure criterion | decision impact |
| --- | --- | --- | --- |
| P0 done | JOINT camera latent-state intervention | fixed e3 JOINT baseline, perturb camera latent state by zero / shuffle / noise-matched during sampling | confirms strong raw camera-state dependency; does not prove simple removal helps |
| P0 done / rejected | asymmetric human-input shuffle training | JOINT camera loss uses normal forward; JOINT human loss uses second forward with shuffled camera input channels | camera completion improves, human completion roughly holds, but JOINT worsens; minimal shared-backbone gating is not the fix |
| P0 done | clean human completion numeric baseline | same e3 checkpoint, human task eval, 1024 samples first | quantifies the “clean human completion looks better” reference instead of relying only on visual impression |
| P0 pending | clean human completion vs JOINT paired render audit | same human text / seed, compare body quality, foot contact, action phase, jitter, limb artifacts | turns user-observed visual degradation into auditable evidence |
| P0 pending | visibility boundary split | separate normal full-body cases from crop / outscreen / occlusion cases | prevents invalid “human should be camera-invariant” claims |
| P1 | root-first diagnostic | predict human root first, then camera relation; compare against simultaneous JOINT | tests whether root-level parent variable fixes circular dependency |
| P1 | capacity competition control | add branch-specific capacity or separate lightweight adapters without changing causal direction | only after the core asymmetry experiment; do not spend cards before the causal path is tested |

If asymmetric human-input shuffle does not improve JOINT human and camera remains stable, the bottleneck is likely deeper than this minimal gating. If human and camera both degrade, the shared backbone cannot reconcile the two objectives and the next candidate should be stronger branch separation, not more capacity.

## 5.1 JOINT Intervention Result 2026-07-06

Baseline is e3 JOINT full eval, 10549 samples. All intervention rows use the same e3 checkpoint and JOINT sampler, changing only the stated camera-side variable.

| condition | captions F | CLaTr FCD | CLaTr cov | Out | TMR FTD | TMR cov | interpretation |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| baseline JOINT | 0.2528 | 126.91 | 0.5752 | 0.0903 | 195.85 | 0.3158 | reference e3 JOINT |
| camera latent zero | 0.1589 | 347.79 | 0.1898 | 0.1865 | 413.95 | 0.1131 | removing camera state causes severe human/joint metric collapse |
| camera latent shuffle | 0.1945 | 253.72 | 0.2703 | 0.1134 | 419.87 | 0.1100 | instance-mismatched camera state also collapses human-relevant metrics |
| camera latent noise-matched | 0.1494 | 404.65 | 0.1574 | 0.1981 | 440.67 | 0.1044 | distribution-shaped noise is worst; not just text semantics |
| camera text shuffle | 0.1625 | 132.83 | 0.5585 | 0.1001 | 198.76 | 0.3127 | human metrics stay close to baseline; high-level camera text is not the main culprit |

Decision: the strongest supported claim is **JOINT human is strongly dependent on raw camera latent state**. The evidence does not support a naive fix of zeroing camera state at inference, because zero / noise / shuffle all degrade human. The actionable mechanism to test is training-time decoupling of instance-level camera state from the human-loss path while preserving `H -> C` learning for camera.

## 5.2 Core Deployment Result

Approved by DS max after the 2026-07-06 review: run one main experiment first, not a bundle of capacity or auxiliary long trainings.

| run | machine / GPU | path | status | purpose |
| --- | --- | --- | --- | --- |
| `asym_human_input_shuffle_e3` | 5090 GPU0 | `runs/train/stage2/v7_4_core_20260706/asym_human_input_shuffle_e3` | done / rejected | main core test: JOINT human loss sees shuffled camera input; JOINT camera loss stays normal |
| `e3_human_completion_1024` | 4090 GPU1 | `runs/eval/stage2/v7_4/asym_human_input_20260706/baselines/e3_human_completion_1024.json` | done | clean human completion numeric reference |

Implementation contract:

- New CLI: `--joint-human-camera-input-mode {normal,zero,shuffle,noise_matched}`.
- Training: only JOINT human-loss channels use the second camera-perturbed forward; JOINT camera-loss channels use the normal forward.
- Eval/render: JOINT camera prediction comes from the normal forward; JOINT human prediction comes from the camera-perturbed forward; channels are merged before decoding.
- Current main run uses `shuffle`, because it preserves camera-state distribution while breaking instance-level camera-human pairing.

Do not run width-512 capacity, relation-surrogate, or human-protect long trainings before this result is evaluated. They are secondary controls, not the current core experiment.

Clean human completion 1024-sample reference:

| task | samples | TMR R1 | TMR R3 | TMR FTD | TMR cov | TMR precision | TMR recall | note |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| human completion e3 | 1024 | 0.0938 | 0.2158 | 176.75 | 0.9033 | 0.8662 | 0.9609 | TMR-only callback; not directly a full 10549 JOINT eval |

This supports the user-observed quality gap mainly through TMR coverage: clean human completion is much broader / less collapsed than e3 JOINT baseline coverage 0.3158, while FTD is only moderately better than JOINT baseline 195.85. Full interpretation still requires paired render audit.

Full `asym_human_input_shuffle_e3` eval, 10549 samples:

| task | run | FDTMR↓ | TMR↑ | HCov↑ | FDCLaTr↓ | CLaTr↑ | CCov↑ | F1↑ | Out↓ | readout |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| camera | e3 baseline | - | - | - | 34.62 | 44.97 | 78.2% | 0.512 | - | v7.3.1 reference |
| camera | asym shuffle | - | - | - | 23.74 | 47.35 | 78.9% | 0.556 | - | camera completion improves |
| human | e3 baseline | 147.60 | 18.15 | 76.2% | - | - | - | - | - | v7.3.1 reference |
| human | asym shuffle | 148.18 | 18.83 | 74.5% | - | - | - | - | - | human completion roughly holds, coverage slightly worse |
| joint | e3 baseline | 195.85 | 17.96 | 31.6% | 126.91 | 21.08 | 57.5% | 0.253 | 9.0% | v7.3.1 reference |
| joint | asym shuffle | 204.07 | 17.28 | 25.2% | 143.70 | 17.25 | 45.5% | 0.221 | 10.2% | JOINT worsens; repair rejected |

Important execution note: the first JOINT eval attempt with batch size `64` OOMed at `8960/10549` during SMPL decode and did not produce a final JSON. The accepted JOINT row is the complete batch size `32` rerun with `PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True`.

## 5.3 Veto Criteria

Full eval compared e3 JOINT baseline, clean human completion baseline, and `asym_human_input_shuffle_e3`.

- Human veto: TMR coverage improves less than 30% over e3 JOINT baseline, or TMR FTD reduces less than 25%, or CLaTr FCD is more than 10% worse than e3 JOINT.
- Camera veto: camera/framing quality collapses, operationalized first by Out rising above 0.135 on comparable JOINT eval, plus paired visual audit for camera jumps or broken framing.
- Training veto: by mid-training, if human and camera validation losses both fail to descend or oscillate worse than e3, stop this minimal shared-backbone fix and move to stronger branch separation.

Actual readout: the human veto triggers. JOINT TMR coverage decreases from `0.3158` to `0.2521`, TMR FTD worsens from `195.85` to `204.07`, and CLaTr FCD worsens from `126.91` to `143.70` (>10% worse). Camera Out increases from `9.0%` to `10.2%`, below the hard Out veto threshold, but the overall JOINT row is worse. Therefore `asym_human_input_shuffle_e3` is rejected as a repair.

Mechanistic implication: simply forcing the human-loss forward pass to ignore instance-matched camera state does not make the shared denoiser learn the desired `H -> C` causal factorization. The next serious fix should use stronger structural separation, such as human-first / root-first generation or branch-separated denoisers with explicit `H -> C` conditioning, rather than more shared-backbone capacity or auxiliary loss tuning.

## 5.4 Stronger Asymmetry Implementation Gate

After `asym_human_input_shuffle_e3` was rejected, v7.4 moves from shared-backbone gating to explicit factorization:

```text
H = P(H | human_text)
C = P(C | H, camera_text, source_quality)
JOINT output = concat([H, C])
```

Implemented code path:

- `train_stage2_condmdi_pulp.py` adds `TASK_HUMAN_TEXT = 3`.
- `human_text` has no observed latent branch; loss covers only human latent channels `[0,HUM_DIM)`.
- camera latent channels are neither observed nor trained in `human_text`, so raw camera latent cannot enter the human generator through CondMDI replacement.
- `storymotion_official_full_eval.py` adds composed JOINT eval: `--run-dir` loads the human generator, `--joint-compose-camera-run-dir` loads an asymmetric H2C camera generator, then official JOINT metrics evaluate the concatenated `[H,C]`.
- composed eval also supports `--joint-compose-human-source gt` for pipeline sanity: use GT human as H2C source before testing generated human.
- `--task human_text` runs the human-text sampler through the official human metric callback, so the human generator can be judged before JOINT composition.

DS max review: **conditional pass only**. The design is more faithful to causal asymmetry than shuffle gating, but long training is blocked until the following veto checks pass.

| gate | required check | veto condition |
| --- | --- | --- |
| implementation | `train_stage2_condmdi_pulp.py check` with four-task `--task-probs` | `human_text` observes any latent branch, trains camera channels, or breaks old task masks |
| old-checkpoint compatibility | load old three-task e3 checkpoint under new code | checkpoint load or old task sampling fails |
| human quality | short human-text smoke checkpoint evaluated with `--task human_text` | human metric is unusably collapsed; do not proceed to JOINT long eval |
| H2C pipeline sanity | composed JOINT with `--joint-compose-human-source gt` and H2C source clean | decode / metric / concat path fails, or H2C on GT human is far below known H2C camera-completion quality |
| generated-source stress | composed JOINT with generated human and H2C source replay | camera collapses so severely that generated-H source mismatch dominates before human-text quality can be assessed |

Only after these gates pass should v7.4 run long training. The first long-training target is not another shared JOINT denoiser; it is `human_text` text-to-human, followed by H2C training or fine-tuning on generated human replay if the generated-source stress test exposes a source shift.

### 5.5 Stronger Asymmetry Closed-Loop Smoke

2026-07-06 code and smoke status:

| gate | machine | artifact | result | readout |
| --- | --- | --- | --- | --- |
| four-task implementation check | 5090 GPU0, 4090 GPU0 | `train_stage2_condmdi_pulp.py check --task-probs 0 0 0 1` | pass | `human_text` trains only human channels and observes no latent branch |
| old checkpoint compatibility | 5090, 4090 | `e3_bridge_smoke_compat_5090.json`, `e3_bridge_smoke_compat_4090.json` | pass | old three-task e3 checkpoint samples camera / human / joint only; no task-id overflow |
| human-text smoke train | 5090 GPU0 | `runs/train/stage2/v7_4_core_20260706/human_text_smoke_20step` | pass | training loop and four-task checkpoint metadata work; not quality evidence |
| human-text official metric | 5090 GPU0 | `human_text_smoke32.json` | pass | official human callback accepts `human_text`; 32 samples avoid PRDC k failure |
| composed JOINT with GT human | 5090 GPU0 | `composed_gt_human_h2c_clean_smoke32.json` | pass | concat `[H_gt, C_h2c]` path, decode path, and official JOINT metric all run |
| composed JOINT with generated human | 5090 GPU0 | `composed_generated_human_h2c_replay_smoke32.json` | pass as execution, quality failed as expected | generated-source path runs, but 20-step human generator causes severe metric collapse |

Key smoke metrics, 32 samples:

| condition | TMR FTD↓ | TMR cov↑ | TMR score↑ | CLaTr FCD↓ | CLaTr cov↑ | F1↑ | Out↓ | interpretation |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| `human_text` smoke | 2266.95 | 0.0% | 3.44 | - | - | - | - | official human metric path works, but 20-step model is not usable quality |
| composed GT human + H2C clean | 439.83 | 100.0% | 15.71 | 110.77 | 97.1% | 0.557 | 6.0% | H2C compose / decode / metric path is valid under GT human |
| composed generated human + H2C replay | 2266.28 | 0.0% | 3.55 | 1024.98 | 0.0% | 0.017 | 15.4% | source-shift and weak 20-step human generator dominate; not a method-quality result |

Decision: the stronger-asymmetry code path is ready for the first real long training target, `human_text` text-to-human. It is not yet evidence that v7.4 solves JOINT. The next veto will be the full `human_text` checkpoint quality; generated-source H2C fine-tuning should wait until that checkpoint exists, otherwise the H2C source-shift experiment is confounded by a deliberately undertrained human generator.

DS max post-smoke audit: **PASS for `human_text` long training only**. It explicitly does not approve generated-source H2C long training before a full human generator checkpoint exists.

Required long-training gates:

| gate | check | action |
| --- | --- | --- |
| startup | no OOM / NaN; `grad_norm` finite; `human_text_loss` logged | continue |
| 10k official human-text eval | FTD below `2000`, coverage at least `5%`, TMR score at least `4.0` | if missed, mark weak signal but continue to 30k unless training is unstable |
| 30k official human-text eval | FTD below `1500`, coverage at least `20%` | if missed, stop and re-check configuration |
| 50k hard collapse | coverage still `0%` | stop; do not launch H2C replay training |
| generated-source H2C | only after `human_text` full checkpoint has usable official human metrics | then test / train H2C on generated-human replay |

Current long training:

| run | machine / GPU | path | status | note |
| --- | --- | --- | --- | --- |
| `human_text_full_e3like_82688` | 5090 GPU0 | `runs/train/stage2/v7_4_core_20260706/human_text_full_e3like_82688` | running from 2026-07-06 16:00 +0800 | e3-like capacity; `--task-probs 0 0 0 1`; selection metric `human_text_loss` |

## 6. Candidate Fixes, Not Claims

v7.4 keeps architecture proposals behind diagnostics.

| candidate | core idea | when to try | risk |
| --- | --- | --- | --- |
| human-first / root-first factorization | generate `H_root` or `H` before `C`; camera depends on human | after intervention confirms `C -> H` leakage | serial error propagation |
| asymmetric attention | permit `H -> C`, restrict `C -> H` except through intent / visibility metadata | after leakage is localized to attention or feature mixing | over-restricting useful geometric information |
| branch-specific heads / adapters | reduce capacity competition while preserving shared backbone | before claiming structural causality | may hide the same leakage in a bigger model |
| intent / staging layer | let camera edits affect human only via high-level intent, not raw trajectory | when interactive camera edit is part of task definition | intent labels may be underspecified |
| post-generation camera optimization | keep human fixed, optimize camera for framing / Out / shot scale | for physical-camera edit and camera completion | does not solve director-intent edits |

The stronger paper claim should only be made after diagnostics:

```text
Human-camera motion is not a symmetric joint variable pair.
Camera is a downstream view / framing process conditioned on human and intent.
StoryMotion should model this causal asymmetry explicitly.
```

## 7. Relation to v7.3.1

v7.3.1 remains useful, but only as a lower-level evidence layer:

- e3 proves reliability schedule has a real but local JOINT / framing signal.
- e2 proves clean H2C is not a sufficient proxy for JOINT.
- e0/e1 prove naive CLIP task instruction is not a reliable task-control fix.
- RF / MoLingo evidence shows process or backbone swaps alone do not solve JOINT.

v7.4 changes the center of gravity:

```text
v7.3.1 question:
  Which task/source schedule is least bad under current symmetric Stage2?

v7.4 question:
  Why does symmetric Stage2 let camera prediction degrade human in JOINT,
  despite the physical dependency being H -> C?
```

## 8. DS Audit Integrated

DeepSeek max review agreed that v7.4 is deeper than v7.3.1, but required three constraints:

- Do not write v7.4 as a solved architecture. It is a diagnostic roadmap.
- Define the human-invariance boundary: it applies only when camera changes do not imply crop, occlusion, or visibility loss.
- Rule out capacity competition before claiming causal-structure leakage as the dominant root cause.

These constraints are now part of the P0 gate above.
