---
title: "StoryMotion Current: v10 Preparation"
status: v10_corrected_phase_b_long_training_human_teacher_evaluated
hypothesis: |
  v10 has a Phase-A-exact Human parent and a separately trained Human flow
  teacher. The prior Camera endpoint omitted framing backpropagation, so a
  corrected fresh Phase-B has passed its preregistered 30K smoke screen and is
  continuing to 210K; formal audit is still required before any cache or Stage2
  Camera work, and Direct-C and joint remain unevaluated.
tags:
  - StoryMotion
  - version/v9
  - version/v10
  - stage1
  - stage2
  - protected-human
  - status/active
aliases:
  - StoryMotion-Current
  - StoryMotion-v9-Redesign
source_notes:
  - "[[version_family]]"
  - "[[StoryMotion-valid-metric-ledger]]"
  - "[[Storymotion-exp-sha]]"
  - "[[StoryMotion-metric-computation-io]]"
  - "[[2026-07-27_storymotion-stage1-human-anchor-residual-control]]"
  - "[[2026-07-28_storymotion-v9-protected-h-three-stage-implementation-camera-diagnosis]]"
  - "[[2026-07-29_storymotion-v10-human-relative-camera-training-contract]]"
  - "[[2026-07-29_full_re]]"
created: 2026-07-12T14:30:00+08:00
updated: 2026-07-29T15:59:48+08:00
---

# StoryMotion Current: v10 Preparation

> [!abstract] 当前裁决
> v10 Human owner仍是Pulp-only Phase A `210K`，Human teacher `105K`结果仍有效。复核发现旧Camera Phase-B只反传relative reconstruction、relative temporal与rotation geodesic，漏掉了v9中合理的`0.1 framing`；旧`210K`及pure4,053审计因此只保留历史diagnostic，不再是cache候选。修正版以fixed-projective framing补齐loss，已从同一Phase-A父权重fresh启动并通过真实数据preflight与预注册`30K` smoke，当前从exact `30K` checkpoint接续至`210K`。v9与v10 teacher虽然同架构、同`105K`配方，但分别属于Phase-C `636K`与Phase-A `210K` latent owner，不能复用；CFG1／CFG3的matched fixed8六路Gradio与新增N=512诊断已闭合。当前尚无修正版Stage1 formal endpoint、v10 Camera flow、Direct-C、sequential joint、synchronous joint或Unified-3结果；v8.1C C3-25 seed17继续是mainline。

## 1. 当前系统与完成状态

| component / run | implementation | completed evidence | decision |
| --- | --- | --- | --- |
| v10 corrected Stage1 Phase B / v10_hrelcam_stage1_phasea210k_phaseb_framing_r2_seed17_4090g0_20260729 | exact Phase-A `E_h,D_h` frozen；fresh independent Human-relative Camera48 `E_c,D_c`；relative recon + temporal + `0.1` rotation + `0.1` fixed-projective framing；non-causal | contract、真实数据preflight、Camera-only gradient与Human exact regression通过；first-128 `30K` smoke逐项通过；同run续训至`210K`中 | 长训／pure4,053 formal未闭合前无v10 cache候选 |
| v10 old-3-loss Stage1 Phase B / v10_hrelcam_stage1_phasea210k_phaseb_camera48_210k_seed17_4090g0_20260729 | 同架构但没有framing backprop | completed `210K` pure4,053 canonical diagnostic；Human exact；fixed8 reconstruction visual | 历史数值与artifact保留；不得作为修正版endpoint、resume或cache parent |
| v10 Human teacher / v10_hrelcam_phasea210k_human_teacher105k_seed17_4090g1_20260729 | Phase-A Human128；`ViMoGenLightFlow` Human-text-only；EMA `105K`；因owner不同于v9而fresh训练 | first-512 Euler50 CFG1／CFG3 Direct-H、paired/no-reference diagnostics、fixed8 paired/blind及v9 matched六路visual | Human prerequisite available；CFG不是单调增益；diagnostic-only；没有 Camera 或 joint 证据 |
| Stage1 redesign Pulp-only / stage1_hanchor_pulp_only_matched_r3_636k_seed17_4090g0_20260726 | Pulp-only owning decoder；Human anchor + interaction residual；non-causal；Human128 + interaction16 + Camera48 | fresh 636K、Pulp pure4,053 true-length reconstruction 与 fixed8 visual 已闭合 | architecture/representation control；不替换 C3-25 |
| Stage2 Human teacher / v9_hanchor_protected_vimogen_u3_diag_seed17_4090g1_20260727 | ViMoGen-light CLIP Human text → Human；105K；bf16；Human EMA 在阶段边界物化并冻结 | N=512 Direct-H eval + paired/no-reference metrics + fixed8 paired/blind vis | completed；Human branch 质量较高 |
| Stage2 Camera/joint / same run | 独立 Camera64 Transformer；H→C cross-attention；Camera105K，分 Direct-C specialist、joint triangular、unified routing 三段 | global210K 三路 N=512；P0 snapshots、P1 CFG、P2 replay与P3 balanced screens均闭合 | completed diagnostic；P3 continuation gate fail |
| Promotion mainline | v8.1C C3-25 seed17 Stage1 + Unified-3 105K | pure4,053 formal Direct-H、Direct-C、joint parallel | 保持；v10 corrected Stage1尚未形成formal endpoint |

精确指标见 [[StoryMotion-valid-metric-ledger]]；全部 checkpoint、cache 与 artifact 身份见 [[Storymotion-exp-sha]]。
提供给外部Web GPT的非canonical transport prompt见[[2026-07-29_storymotion-v10-human-relative-camera-training-contract#9. Web GPT外部评审Prompt（2026-07-29）]]。

## 2. v9 三阶段训练实现

### 2.1 Human teacher：global 1–105K

- 训练对象仅为 Human ViMoGen-light flow branch；Camera tokens、Camera text 与 Camera modules 不进入 Direct-H 调用。
- micro/effective batch 都是 128，bf16，AdamW，初始 LR 2e-4，warmup 2K，80K 后衰减到 0.1 倍。
- 以 shifted-sigma flow objective 训练 Human text → Human128；每 5K 做 fixed held-out loss、TensorBoard 与 resume checkpoint。
- step105K 将 Human EMA 写入 teacher endpoint，随后冻结 Human；Camera 训练期间 Direct-H 只做 exact-regression monitor，不重复优化。

### 2.2 Direct-C specialist：Camera phase 1–35K，global 105001–140K

- 输入是 observed/GT Human latent + Camera text，输出 Camera64；Human context stop-gradient，trust 固定为 1。
- Camera branch 为 12-layer、width512、8-head full Transformer，使用 H→C cross-attention。
- 本阶段只训练 Direct-C，目的是先建立 Camera completion，再进入 generated-H joint context。
- 这不是 joint generation；其 projective 指标只属于 observed-Human Camera completion。

### 2.3 Joint triangular 与 unified routing：Camera phase 35K–105K

- Camera phase 35,001–70,000：strict joint triangular。训练时从 noisy GT-Human 调用一次冻结 teacher 的 conditional forward，Camera 消费 stop-gradient predicted-clean Human，context trust 随 sigma 调节；这不是完整 Human 自由生成轨迹。
- Camera phase 70,001–105,000：Direct-C 与 joint 交替；奇数 step 为 observed-H Direct-C，偶数 step 为 joint。
- 最终 checkpoint 同时提供 Direct-H、Direct-C 与 joint parallel；Human branch 参数与 teacher 逐位一致。
- Camera phase 的 immutable run contract 是 micro/effective batch `128/128`、gradient accumulation `1`、bf16、AdamW、105K optimizer steps、每5K eval/checkpoint。Human phase 的 micro/effective batch 也都是 `128`；总训练量为 `210K × 128 = 26.88M` sample exposures，其中 Human 与 Camera各 `13.44M`。旧 base template 的 `32 × accumulation 4` 不是实际执行配置。

正式joint inference才从Human noise沿完整Euler trajectory生成predicted-clean context，并使用Human CFG3；它与上述noisy-GT、单步、conditional-scale1的HC train context不同。换言之，v9 Camera训练没有使用“完整CFG1 Human generation”：Direct-C读取GT Human，HC读取单步估计；Camera阶段唯一完整`generate_human`调用是CFG3 exact-regression monitor，不进入Camera loss。

## 3. v9 已闭合证据

| version / run | mode | N | primary result | geometry / framing | status |
| --- | --- | ---: | --- | --- | --- |
| v9 redesign protected-H ViMoGen / Human teacher105K and Unified210K | Direct-H | 512 | FDTMR 156.576；TMR 19.097；HCov 0.8317 | global MPJPE 0.8615 m；root-aligned 0.2373 m；root ADE/FDE 0.7729 / 1.2616 m | completed diagnostic；teacher/final exact |
| v9 redesign protected-H ViMoGen / Unified210K | Direct-C observed-H | 512 | FDCLaTr 232.175；CLaTr 36.430；CCov 0.5819；F1 0.4103 | Cam ADE/FDE 2.625 / 2.911 m；rotation 57.564°；Out 50.0% | completed；Camera fail |
| v9 redesign protected-H ViMoGen / Unified210K | joint parallel | 512 | H 与 Direct-H exact；Camera FDCLaTr 181.666；CLaTr 48.619；CCov 0.6735；F1 0.4965 | Cam ADE/FDE 3.312 / 3.416 m；rotation 69.886°；Out 31.57% | completed；Camera fail |

> [!warning] Evidence boundary
> 三路都是 first-512、Euler50、CFG3、seed17、同一 redesign owning decoder 的诊断结果。它们可用于定位该系统的 Human/Camera 差异，但不能替代 C3-25 pure4,053 formal evidence，也不能触发 representation promotion。

## 4. v9 Camera blocker 与根因假设

当前证据把问题收窄到 Camera 生成与适配，而不是 Human 污染：

- Human teacher 在 Camera 训练前后保持 exact，joint Human 指标也与 Direct-H 一致；因此 Camera 差不能归因于 Camera 更新破坏 Human。
- Direct-C 已在 observed Human 条件下明显失败，说明问题先于 joint generated-H exposure 存在；joint context shift 会放大问题，但不是唯一根因。
- v9 HC训练的单步conditional-scale1 context与CFG3完整joint rollout之间存在exposure mismatch；它可以解释部分joint额外退化，却不能解释只读GT Human也失败的Direct-C，因此不是Camera三模式冲突的充分根因。
- redesign Stage1 Camera latent 是 interaction16 + Camera48，而 Stage2 Camera route、objective 和文本适配来自 ViMoGen-light Human 路径的扩展。Camera 表征 owner 与 denoiser inductive bias 未形成像 Human 那样的原生匹配。
- Camera 文本使用固定 caption index 0，禁用了训练期多 caption 增广；这会削弱语义覆盖，但不能单独解释大幅轨迹/旋转误差。
- 当前 objective 只对 Camera latent 做统一 flow matching，没有 DC3D 式 raw projective geometry sidecar、framing loss 或轨迹/旋转专用约束；这与 vis 中的漂移和不稳定方向一致，但仍需 matched ablation 验证。

final210K 不是最佳 Camera endpoint。P0确认 sequential route absence造成遗忘；P2否定“持续负 route-gradient cosine”并把历史 moments限定为失稳放大器；P3进一步证明 same-step aggregation可消除短程爆炸，却没有在 `10K` 内恢复两路健康 fixed-loss或 decoded Camera能力。这些过程数值由 run artifacts与[[2026-07-28_storymotion-v9-protected-h-three-stage-implementation-camera-diagnosis]]拥有，本页只保留当前决策。

## 5. 当前 stop 与下一授权边界

v10 当前边界：

1. Stage1 corrected-framing Phase-B的`30K` smoke已通过；当前先完成同run的`30K→210K`长训，再做pure4,053 formal。旧三项loss `step_210000.pt`和旧`207K`都没有当前cache决策权。不得回退到旧`636K`、interaction16、Camera64或旧normalization。
2. Human teacher `105K` 可以按 `strict=True` 转入未来 v10 Unified-3 的同实现 Human branch，但本次 Direct-H 只关闭 Human 前置条件，不代表完整 v10 通过。
3. 当前离线generated／rollout Human context cache与eval默认都是CFG1。Camera contract启动前必须固定为CFG1-only，或按durable contract改为离散CFG1／CFG3双cache；禁止用CFG1 cache训练后静默切到CFG3 sequential inference。首个双CFG诊断不采用连续随机区间，也不同时增加CFG embedding。
4. 只有corrected Stage1 endpoint闭合且上述CFG support写入immutable contract后，下一独立实验轴才是其Camera48 cache、四route Camera flow与预注册LR screen；完成Camera训练后才运行GT-H Direct-C、sequential joint、synchronous joint的matched A/B/C。当前这些实验均未启动，不能提前判断成功或失败。

v9 已闭合边界：

1. P3 两条 `10K` screen停止在既有 artifacts；不从 short contract续训，也不自动创建 `105K` full run。
2. 两臂共 `20` 个 paired-gradient probes全部为正，不满足 PCGrad／CAGrad或 mode-specific adapter的触发条件。
3. `1e-4` 终点仍明显高于 P0 健康 fixed-loss且到 `10K` 仍在下降；decoded错误尚不能与 latent underfit分离，因此暂不触发 interaction16／camera48 oracle、conditional-manifold或 geometry auxiliary。
4. 若继续 v9，需把“更长 same-step balanced 是否进入健康区”作为新的单一 causal axis重新预注册；仍从 protected `teacher.pt`边界开始，Human exact与 non-causal约束不变。

## 6. Claim boundary

可以写：

- “v10 Phase-A-exact Human owner与独立Human teacher105K的first-512 Direct-H诊断已闭合；corrected-framing Stage1 Phase-B已通过preflight与30K smoke，并在同run续训至210K。”
- “旧三项loss `210K`与旧`207K` artifact仍保留provenance和历史数值，但都不是修正版endpoint或cache候选。”
- “v9与v10 Human teacher使用同一flow实现／训练配方，但latent owner、cache与train-only statistics不等价，所以v10需要fresh训练。”
- “v9 Camera训练没有消费完整CFG1 Human rollout；Direct-C使用GT Human，HC使用noisy-GT上的conditional-only单步predicted-clean。它与CFG3 joint inference存在exposure mismatch，但不能解释Direct-C失败。”
- “v10 teacher的CFG3改善部分semantic／retrieval与运动幅度，同时回退FDTMR、coverage及paired geometry；CFG不是单调修复。”
- “v10 Human teacher未塌缩且 semantic/distribution signal可用，但 fixed8仍有速度、加速度或单帧尖峰，strict physical-quality gate未闭合。”
- “v9 redesign protected-H Unified-3 已完整训练并评估；Human branch 较强且被严格保护，Camera branch 在 Direct-C 与 joint 中仍不稳定。”
- “Direct-C 在 observed Human 条件下已经失败，因此 joint generated-H context 不是 Camera 问题的充分原因。”
- “same-step balanced objective通过 `10K` 稳定性 screen，但未通过 healthy-loss与 decoded continuation gate。”

不能写：

- “v10 Camera 或 joint 已训练／失败／通过”，或“Human teacher结果等价于 v10 Unified-3 三模式结果”。
- “旧三项loss `210K`就是修正版Stage1 endpoint”或“可以从它直接构建v10 Stage2 cache”。
- “Stage1 reconstruction visual 是 Stage2 Camera generation visual”。
- “redesign 已替换 C3-25 mainline”或“该 N=512 诊断具有 promotion 资格”。
- “joint Camera 差完全由 Human 质量导致”。
- “缺少 DC3D sidecar 已经被证明是唯一根因”。
- “balanced `10K` 稳定等于 Camera能力已修复”或“已授权 full `105K`”。
- “root-aligned MPJPE 是 local-pose error”；它仍保留 heading error。

## 7. Canonical owners

- 当前主线、blocker、允许行动：本页。
- 审计数值与公平对比：[[StoryMotion-valid-metric-ledger]]。
- checkpoint、cache、artifact 与 records 身份：[[Storymotion-exp-sha]]。
- metric/evaluator/decoder 语义：[[StoryMotion-metric-computation-io]]。
- 版本事件与失效来源：[[version_family]]。
- 三阶段完整实现、Camera 训练曲线与根因分析：[[2026-07-28_storymotion-v9-protected-h-three-stage-implementation-camera-diagnosis]]。
- v10 architecture、训练合同与A/B/C gate：[[2026-07-29_storymotion-v10-human-relative-camera-training-contract]]；原任务书与执行快照见 [[2026-07-29_full_re]]。
