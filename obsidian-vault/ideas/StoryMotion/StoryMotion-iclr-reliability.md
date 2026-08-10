---
title: "StoryMotion ICLR Reliability and Closure Contract"
status: in_progress
hypothesis: |
  StoryMotion检验在冻结Human prior及其输出路径时，非对称Human–Camera扩展能否支持
  Direct-H、Direct-C与sequential composition。NoInt-HREL／C1REL Stage1表示审计已闭合；
  C0-LAT是后续唯一operational mainline。C1REL-w/o-Interaction16 matched Stage2与
  exact HREL-vs-C1REL Stage2 comparison已完成formal评测；结论为mixed Pareto。
tags:
  - StoryMotion
  - reliability
  - submission-closure
  - status/active
aliases:
  - StoryMotion-ICLR-Reliability
source_notes:
  - "[[StoryMotion/current]]"
  - "[[StoryMotion/version_family]]"
  - "[[StoryMotion-valid-metric-ledger]]"
  - "[[StoryMotion-metric-computation-io]]"
  - "[[StoryMotion/paper-boundary]]"
  - "[[analysis/CVPR_2025/Dynamic_Motion_Blending_for_Versatile_Motion_Editing]]"
created: 2026-06-18T00:00:00+08:00
updated: 2026-08-10T21:26:13+08:00
---

# StoryMotion ICLR Reliability and Closure Contract

> [!important] 唯一live范围
> 本页只拥有StoryMotion的claim–evidence gap、投稿实验优先级、停止条件和降级措辞。
> 正式数字与hash只见[[StoryMotion-valid-metric-ledger]]；DIRECT状态只见
> [[DIRECT/current]]。拆分前完整方案已归档，不再授权Rect、HumanML3D跨配对、program
> solver、Actor–Director数据、ViGen utility、editing长训或joint-parallel训练。组合式composition／editing
> 只是secondary utility extension；具体operator、数据与训练顺序由§4.5的gates约束。
> 当前不授权composition／editing长训，必须先通过data与Stage1 support gates；它不改变
> mainline或核心claim。§2.3a的symmetric root-cause controls已单独授权。

## 0. Storymotion Contribution

见[[StoryMotion-Contributions]]。

## 1. 已冻结的方法与已有证据

$$
p(H,C\mid T_H,T_C)=p_H(H\mid T_H)p_C(C\mid H,T_C).
$$

StoryMotion只报告：

1. Direct-H：$T_H\rightarrow H$；
2. Direct-C：observed $H+T_C\rightarrow C$；
3. sequential composition：先生成并固定$H$，再由同一个Camera branch生成$C$。

当前训练主线已经闭合。v11 C0-LAT与C0-GEO共享exact v9 Pulp-only non-causal Stage1、
owning decoder／cache／train-only stats及冻结v9 Human `105K` teacher，仅Camera objective不同。
seed17与seed23四个Camera endpoint均完成`105K`、Pulp pure4,053三接口、official metrics、
decoded geometry／physical diagnostics和10,000次paired bootstrap。24个Camera geometry差异的
95% CI全部跨零，因此统计结论仍是“没有稳健单一objective胜者”，不能写LAT／GEO等价。
2026-08-04作者基于主表指标优先级与更简洁的latent-flow objective，将C0-LAT指定为后续唯一
operational mainline；C0-GEO保留为audited alternate。该选择不是显著性结论。

## 2. `0803-2024`表示因果矩阵

> [!important] 当前优先级
> NoInt-HREL／C1REL Stage1已闭合，C0-LAT仍是默认mainline。作者已根据现有formal
> artifact将NoInt-HREL matched Stage2标记为未完成，并单独授权C1REL Stage2及
> `C1REL-w/o-Interaction16` Stage1。strict no-I16的广泛退化被作者裁决为Interaction16
> simple-and-effective的正向Stage1 ablation；其matched Stage2已完成formal评测。WORLD不因本次
> 授权进入执行。旧 Matched Symmetric run 仅保留为 misconfigured/invalid provenance：
> `human_frozen_after_teacher=true`、strict triangular MVP 的 `camera_to_human=none`、
> `joint_context=stop-gradient predicted-clean Human`，不能回答Camera loss影响Human的symmetric
> causal question；其Direct-H尝试停止且无有效results/manifest。真实P2 fresh run
> `sm_p2_matched_symmetric_joint_fresh_h105k_joint105k_seed17_4090g1_20260809` 已按正确合同通过
> contract/generic audit、GPU preflight与step20双边finite nonzero-gradient gate，并完成`105K`
> symmetric-joint endpoint及pure4,053三接口formal。结果是mixed Pareto：Direct-H与sequential
> geometry改善，但Direct-C Camera以及sequential semantic／framing明显退化。P1 HREL只提供同
> evaluator/protocol secondary comparison；因其Human初始化与P2不同，严格factorization因果估计仍需
> 已部署的C0-LAT同一evaluator/noise reference rerun完成并审计。正式数字只见ledger §3.19。

此前的Independent Conditional Camera64与Fully-Separate-Native来自`0803-1647`，不回答本轮
表示问题。前者在审计前已完成`210K`，只保留off-plan HREL-Camera64 diagnostic；后者在约Human
phase `55K`安全停止并保留checkpoint。二者都不进入`0803-2024`主矩阵，也不据此启动Stage2。

| arm | Stage1所有权 | latent／Human接口 | Camera positive | 参数／计算匹配 | 预声明结论 |
| --- | --- | --- | --- | --- | --- |
| A · StoryMotion-HREL | exact v9 Pulp-only owner；owning `D_h/D_c/D_f` | H128＋I16＋C48；official Camera14 relation path | factual GT-H199＋GT-C14 | reference `636K`、batch128、seed17 | current reference；不预设I16必要 |
| B · HREL-w/o-Interaction16 | fresh Stage1；同v9数据、三阶段schedule、loss与exposure | H128＋C48；conditioner／`D_c`／`D_f`输入192→176；Camera48仍读取v9 HREL Camera14 | factual GT-H199＋GT-C14 | `1,273,657`参数；同`636K`、batch128、seed17 | 只回答“显式I16是否必要”；不回答Camera是否依赖Human |
| C · StoryMotion-C1REL | fresh Stage1；同v9数据、三阶段schedule、loss与exposure | H128＋I16＋C48；I16继续读取Human-relative framing，C48输入完整$T_{C1}^{-1}T_{Ct}$；owning decoder恢复首帧锚点 | factual GT-H199＋GT-C14 | `1,480,521`参数，与A exact；同`636K`、batch128、seed17 | 只回答Camera-native motion／Human-relative relation分开表示是否形成稳定Pareto |
| D · C1REL-w/o-Interaction16 | fresh Stage1；相对C只删除I16 | H128＋native C1REL-C48；owning `D_c/D_f`输入192→176 | factual GT-H199＋GT-C14 | `1,273,657`参数；同`636K`、batch128、seed17 | Stage1已支持I16有效性；后续matched Stage2检验generation贡献 |

### 2.1 表示与锚点所有权

- B是从当前结构删除I16的matched ablation；Camera conditioner和owning Camera／framing decoder
  仍读取H128＋C48。历史v10虽然也是176D，但其Human owner是Phase-A `210K`，与v9 Phase-C
  `636K`不等价，不能替代B。
- C的C1REL使用完整首帧相对平移向量、旋转、相对速度及FOV，不使用标量distance。缓存／生成的
  C48严格等于$E_C(\mathrm{C1REL}_{14})$，发生在任何Human／I16 conditioning之前；逐元素单测为
  exact `rtol=0, atol=0`。I16仍从paired Human199＋v9 Camera14获得人物相对构图信息，conditioner
  只作为owning decoder侧的首帧锚点adapter，不进入Stage2的C48 target。
- C1REL train-only statistics来自exact 162,760条Pulp train、19,336,827个有效帧；artifact
  SHA256=`7ca04cba4ff6efe573060eea8382e4dc097a9d17b1ab874c32c998661ad13564`。
- 所有新实验默认并显式使用seed17、`is_causal=false`、batch128。不得构造generated-H＋原GT-C
  positive；generated-H只在formal sequential推理时使用。

v9 Stage1已把Human–Camera关系写入Camera14、Interaction16、Camera48及owning `D_c/D_f`；因此
组合式Human不能直接复用任意旧Camera或旧latent。任何composition utility必须先证明冻结Stage1
仍能支持新的pair-side输入，再决定是否调整表示或进入Stage2。

### 2.2 训练与评测gate

1. B／C均固定v9的Pulp-only A `210K`＋B `210K`＋C `216K` schedule、source cycle、optimizer、
   LR、loss、sample exposure与checkpoint schedule；fresh初始化，不复用旧optimizer或模型权重。
2. optimizer前必须通过implementation／data／stats hash、non-causal、Human latent对Camera扰动
   exact invariance、4-sample finite backward、32-sample deterministic replay及500-step one-batch
   overfit；long-run model在preflight后仍为0 step。
3. Stage1先做pure4,053 owning-decoder reconstruction、world／relative geometry与framing audit。
   严重退化可按预声明降低对应Stage2优先级，但不能用中间train loss作论文结论。
4. C1REL Stage1与v9难分上下，且其坐标表示避免了Human-relative relation path。作者因此授权
   C1REL Stage2与D的strict Stage1；这不是C1REL升级事件。D的formal广泛退化支持I16在Stage1
   simple and effective，作者随后授权并启动matched Stage2。
   只有在同时改善Camera-native adherence并守住Human-relative
   projection／framing时，才可讨论替换HREL表示。
5. 现有 Matched Symmetric run 不是有效 causal control：contract 固定
   `human_frozen_after_teacher=true`，strict triangular MVP 中 `implementation.camera_to_human=none`，
   `joint_context=stop-gradient predicted-clean Human`，且仅有 exact Direct-H replay；Direct-H
   attempt 在 `3744/4053` 停止、max_abs=`2.08e-03`，没有 results/manifest，因此不产生任何metric row。
   它只保留为invalid provenance。真实P2 fresh run已允许Camera loss影响Human，并完成正确的
   Stage2 contract/preflight、step20双边finite nonzero-gradient gate、`105K` joint endpoint及三接口
   pure4,053 formal。与P1 HREL的paired CI只作evaluator-matched secondary evidence；P1不同的Human
   初始化使它不能替代同初始化C0-LAT reference。

### 2.3 Durable evidence identities

- HREL reference and HREL-w/o-Interaction16 Stage1
  `sm_hrel_nointeraction16_stage1_636k_seed17_4090g0_r2_20260803` are formal true-length
  `N=4,053` audits. The ablation retains Human quality but degrades Camera/framing; it supports
  an I16 Stage1 reconstruction/framing contribution only.
- C1REL Stage1
  `sm_c1rel_stage1_636k_seed17_4090g1_r2_20260803` is formal true-length `N=4,053`;
  it preserves Human behavior but does not establish a stable Pareto over HREL.
- C1REL Stage2
  `sm_c1rel_rawt0_lat_h105k_c105k_seed17_4090g0_20260804` is formal at Human `105K` plus
  Camera `105K`, with `joint_parallel=false` and Direct-H, Direct-C, and sequential modes. The
  artifact supports the three-interface and generated-H→Camera claims.
- C1REL-w/o-Interaction16 Stage1 and matched Stage2 use
  `sm_c1rel_nointeraction16_stage1_636k_seed17_4090g1_20260804` and
  `sm_c1rel_nointeraction16_rawt0_lat_h105k_c105k_seed17_4090g1_20260806`. Both are formal;
  the matched Stage2 result supports an Interaction16 Camera-generation component effect under the
  seed17 matched protocol, not universal necessity.
- Native PulpMotion Stage1
  `sm_pulpmotion_repro162760_stage1_original_seed17_4090g0_r9_20260806` is a formal external
  system boundary with `413,075` steps and joint reconstruction evidence. Native Stage2
  `sm_pulpmotion_repro162760_stage2_original_matched210k_seed17_5090g3_r2_20260809` is also
  formal on the matched available-data cohort, but its weak native-joint result is a system-boundary
  negative result rather than a StoryMotion three-mode row.
- Superseded Stage1 attempts are provenance-only: the earlier C1REL implementation reconditioned
  Camera48 through the Human/I16 path, so no checkpoint or optimizer state is reused.

Full numeric fields, uncertainty, artifact identities, and hashes remain in the single metric ledger:
[[StoryMotion-valid-metric-ledger#4B. v9+ Stage1 audited detail tables]],
[[StoryMotion-valid-metric-ledger#4A. v9+ Stage2 audited detail tables]], and
[[StoryMotion-valid-metric-ledger#5. Optional Human-text injection controls]].

### 2.3a Symmetric多重反转的root-cause controls

`observed_human`不是“是否向Camera提供Human”。它控制Camera对Human context的trust缩放：
`false`对context乘以随噪声变化的$(1-\sigma)^{\gamma}$，`true`使用完整context。正式Direct-C与
sequential evaluator都调用`generate_camera(..., observed_human=true)`。原fresh symmetric训练
则把predicted-clean Human送入Camera但使用`observed_human=false`；因此其评测接口没有错，错位发生
在训练route与正式sequential接口之间。该错位足以成为Direct-C、semantic／framing回退的候选根因，
但不能在matched controls完成前当作已证实解释。

| control | Camera train route R | Camera→Human gradient G | Human loss continuation U | host / GPU | state | causal contrast |
| --- | --- | --- | --- | --- | --- | --- |
| existing fresh symmetric | `observed_human=false` | on | on | completed historical arm | formal complete | R-control reference; the remaining-contract match must be verified |
| `sm_p2_obstrue_coupled_cont105k_seed17_4090g0_20260810` | `true` | on | on | 4090 / GPU0 | active long train | coupled minus historical fresh isolates R, conditional on the remaining-contract match |
| `sm_p2_obstrue_detach_cont105k_seed17_5090g3_20260810` | `true` | off | on | 5090 / GPU3 | active long train | coupled minus detached isolates G under the same observed route |

两条新臂共享exact v9 HREL Stage1 owner、Human `105K` teacher、C0-LAT Camera初始化、数据／cache、
seed17、105K exposure与三接口formal evaluator。二者都保留$L_H$，所以不能把结果解释成Human-loss
continuation的消融；若仍需隔离U，必须另行授权`R=true, G=off, U=off`第四臂。它们是当前唯一
仍在进行的核心长训；不重复部署4090 GPU1长训，也不启动independent Encodec-H/C或H199／cascade，
因为这些路线同时改变representation、decoder、参数量与Stage2 interface。训练期间预声明记录
$L_H$、$L_{C\mid H}$、$L_C^{HC}$、$\|\nabla_HL_H\|$、
$\|\nabla_HL_C\|$、$\|\nabla_CL_C\|$、两组gradient cosine、$\sigma$与trust统计。
首个live gradient audit固定在step20而非step1，因为Camera的级联zero-init会令step1的
$\nabla_HL_C$结构性为零；step20、100、1K、5K、21K、42K、63K、84K、105K持续审计。
任何主机／物理GPU／route flag不匹配都必须fail closed；detached臂formal结果不得被封装成
`camera_loss_reaches_human=true`。4090 GPU1可在两臂长训期间并行运行exact-initialization C0-LAT同evaluator
的三模式formal eval与paired `source_id` row0／row1 diagnostic，不产生新的训练证据；其factorization
解释与paired closure待两臂完成并通过artifact audit。本文将detached臂作为本轮P1 matched arm；它不同于历史的P1 HREL
`sm_p1_hrel_matched_lat_h105k_c105k_seed17_4090g1_20260809`，后者仍只是evaluator-matched secondary control。

### 2.4 Evidence completion and gap matrix

The matrix below records only causal status and the claim boundary needed for ICLR review; it
does not duplicate the metric ledger.

| causal question | evidence identity | status | ICLR conclusion or remaining gate |
| --- | --- | --- | --- |
| C0-LAT vs C0-GEO Camera objective | `v11_c0_lat_fixedh_35to105k_seed17_5090g2_r2_20260730`; `v11_c0_geo_fixedh_35to105k_seed17_5090g3_r2_20260730` | formal complete | All 24 Camera-geometry CIs cross zero; no single objective winner; C0-LAT remains the operational mainline by author decision |
| v8.1C C3-25 system baseline | `v8_1c_c3_25_diag_unified3_105k_seed17_4090g0_20260719` | formal complete | Former-mainline system boundary; its historical joint-parallel mode is not v11 sequential |
| HREL vs C1REL Stage1 representation | HREL reference; `sm_c1rel_stage1_636k_seed17_4090g1_r2_20260803` | formal complete | Mixed Human/Camera/projective evidence; no stable Pareto promotion |
| Interaction16 Stage1 ablation | `sm_hrel_nointeraction16_stage1_636k_seed17_4090g0_r2_20260803`; `sm_c1rel_nointeraction16_stage1_636k_seed17_4090g1_20260804` | formal complete | Supports Stage1 reconstruction/framing contribution; does not establish generation necessity |
| C1REL Stage2 three interfaces | `sm_c1rel_rawt0_lat_h105k_c105k_seed17_4090g0_20260804` | formal complete | Supports Direct-H, Direct-C, and sequential generated-H→Camera artifact claims under the frozen protocol |
| C1REL-w/o-Interaction16 matched Stage2 | `sm_c1rel_nointeraction16_rawt0_lat_h105k_c105k_seed17_4090g1_20260806` | formal complete | Supports a seed17 matched Camera-generation component effect; no universal necessity claim |
| HREL vs C1REL matched Stage2 | `sm_p1_hrel_matched_lat_h105k_c105k_seed17_4090g1_20260809` | formal complete; mixed Pareto | HREL geometry stronger, C1REL semantic aggregate higher, Human geometry unresolved; no single-winner claim |
| PulpMotion native Stage2 comparison | `sm_pulpmotion_repro162760_stage2_original_matched210k_seed17_5090g3_r2_20260809` | formal complete; valid weak native-joint result | Train/eval IDs exactly match StoryMotion at `162,760/4,053`, but representation, decoder and formal mode differ. Keep as a system boundary; no single-variable three-mode superiority claim |
| Protected asymmetry vs symmetric joint | Old `sm_p2_1_matched_symmetric_joint_h105k_c105k_seed17_4090g0_20260808` is invalid; historical fresh `sm_p2_matched_symmetric_joint_fresh_h105k_joint105k_seed17_4090g1_20260809`; active controls `sm_p2_obstrue_coupled_cont105k_seed17_4090g0_20260810` / `sm_p2_obstrue_detach_cont105k_seed17_5090g3_20260810` | historical fresh formal complete; observed=true G-on/G-off matched pair in training | Historical P2 has stronger Human/sequential geometry but much weaker Direct-C and sequential semantic/framing than the evaluator-matched P1 HREL secondary control. The active pair tests route/gradient root cause under observed=true; it is not yet metric evidence. Exact-initialization C0-LAT same-evaluator reference remains the causal gate |
| C1REL seed robustness | `sm_c1rel_lat_h105k_c105k_seed23_4090g0_20260809` | formal complete; diagnostic-only raw-caption repeat | Three interfaces and hashes are sealed; all paired geometry seed23−seed17 CIs cross zero. Semantic aggregates have no paired bootstrap unit, so robustness wording remains field-specific |
| C1REL-noI16 seed robustness | `sm_c1rel_noi16_lat_h105k_c105k_seed23_4090g0_20260810` | `210K` training complete; pure4,053 Direct-H/Direct-C/sequential evaluation deployed, audit pending | Do not upgrade the seed17 Interaction16 effect until this independent repeat has complete artifacts, hashes and field-wise uncertainty |
| Human-text Camera attribution | `sm_ht_condition_attribution_pure4053_20260810_r2` | full4,053 evaluator-only matrix deployed; HT-FILM/HX/DR × absent/shuffled × Direct-C/sequential; results pending | Matching-text gains cannot be attributed to correct Human semantics until each arm is compared against these frozen-context interventions; diagnostic only, no C0-LAT promotion |
| Visual credibility | `sm_sealed_final_blind_audit_run_id_pending` | incomplete | No visual-superiority or failure-rate claim before a sealed blind audit; H199 and independent dual-codec/cascade comparisons are out of scope because the paper makes no latent-interface superiority claim |
| v8.4 backbone and adjacent-phase controls | `sm_v8_4_a_non_ar_latent_ddpm_run_id_pending`; `sm_v8_4_b_adjacent_phase_control_run_id_pending` | not authorized | Not required for the current capability-preserving factorization claim; do not create runs merely to fill a table |
## 3. 投稿闭环矩阵

本页只记录 claim gate；正式数字、hash 与逐字段不确定性由
[[StoryMotion-valid-metric-ledger]]唯一拥有。

| 闭环单元 | evidence state | 最小剩余 gate | 关闭后的 claim |
| --- | --- | --- | --- |
| HREL vs C1REL representation | Stage1 与 matched Stage2 均已 formal；结论为 mixed Pareto（ledger §§3.16、6.8） | 保留 HREL 为 representation owner；不得写单边 superiority | 只支持审计到的表示差异与 mixed-Pareto 边界 |
| Interaction16 component | HREL/C1REL 两条 Stage1 deletion 与 C1REL matched Stage2 已 formal（ledger §§3.15、6.8） | 将结论限定为 seed17 matched Camera-generation component effect | 不宣称 Interaction16 在所有 seed、数据或实现下普遍必要 |
| Protected asymmetric factorization | 旧 `sm_p2_1_matched_symmetric_joint_h105k_c105k_seed17_4090g0_20260808` 是 invalid provenance-only；fresh `sm_p2_matched_symmetric_joint_fresh_h105k_joint105k_seed17_4090g1_20260809` 已完成三接口 formal，结论为 mixed Pareto（ledger §3.19） | 完成与P2 exact初始化匹配的C0-LAT同evaluator reference及paired audit；旧 artifact 不产生 metric row | 当前只支持“对称joint牺牲Camera controllability／framing而未损害Human质量”的诊断，不支持全局 asymmetric superiority |
| Native PulpMotion Stage2 boundary | Stage1 r9 与 Stage2 `sm_pulpmotion_repro162760_stage2_original_matched210k_seed17_5090g3_r2_20260809` 均已 formal；Stage2 是有效弱 native-joint result（ledger §3.18） | 保留 representation／decoder／mode 差异和 system-boundary 标签；不以 protocol-sanity control 选模 | 可报告同 cohort 外部系统边界，不能写成 StoryMotion 三模式的单变量 superiority |
| C1REL seed robustness | `sm_c1rel_lat_h105k_c105k_seed23_4090g0_20260809` 三接口 pure `N=4,053` 与 hash 已 formal | 保留 raw-caption、diagnostic-only 与 semantic aggregate 无 paired unit 的边界 | 支持 paired geometry 未见 seed 差异；不扩写成所有指标的统计稳健性 |
| C1REL-noI16 repeat | seed23已完成`210K`训练，三接口pure4,053 formal eval已部署 | 完成artifact/hash与field-wise audit后再判断seed17组件效应是否复现 | 当前仍只支持seed17 matched component effect |
| Optional Human-text attribution | HT-FILM/HX/DR matching formal已完成；absent/shuffled × Direct-C/sequential full4,053矩阵已部署 | 固定Camera text、Human context、IDs、noise与checkpoint，完成12项artifact audit；semantic aggregate不伪装paired CI | 只归因正确Human语义是否被Camera分支使用，不改变C0-LAT mainline |
| Human preservation | seed17/23 Direct-H 共享冻结 Human owner；正式 artifact 与 replay 归 ledger | 公开包固化 checkpoint/output identity check | Camera 扩展不改变 Human owner 与输出路径 |
| Perceptual / reproducibility closure | 当前 visual blind audit、failure taxonomy 与论文复现/成本包未闭合 | 冻结 evaluator/cohort，完成 random/best/worst blind slices、环境与成本记录 | 不作 visual superiority、failure-rate 或 production claim |

### 3.1 Baseline边界

- C3-25已有 Pulp pure4,053 formal row，不重复训练；PulpMotion native Stage2 与 StoryMotion
  representation 保持 system-boundary 分离。三条接口的当前投稿覆盖如下；正式数值与hash只见
  [[StoryMotion-valid-metric-ledger#4.2 Interface-specific external baselines]]。

| target interface | audited baseline coverage | fairness verdict | remaining gate |
| --- | --- | --- | --- |
| Direct-H | MoMask-Pulp native；MotionLab-MFT v7.14 adaptation | 两者均为pure4,053 formal system/operator peers；MoMask保留native owner，MotionLab-MFT明确是representation-matched adaptation而非官方原样实现 | MoLingo-derived v7.45仅为provisional screen，缺audit与历史训练源码SHA；MotionStreamer只有causal TAE reconstruction，无Stage2 generator |
| Direct-C | corrected Director-C／E.T. native；CCD-Pulp | Director是pure4,053 native formal；CCD的fixed endpoint、合同、IDs与records完整，但缺独立audit artifact；两者condition/decoder不同且均缺decoded Cam-ADE/FDE/rotation | 现有semantic/distribution可以报告；CCD标注较低assurance，几何只在接入相同callback后比较 |
| sequential Human→Camera | 无mode-equivalent外部baseline；PulpMotion native joint `210K` | matched `162,760/4,053` cohort但representation、decoder与概率分解不同 | 只作native-joint system boundary，不把joint task slices改名为Direct-H／Direct-C／sequential |

- v9是首个可用Stage1 owner；其普通first-512 Stage2 screens已退出活动证据，不能伪装成
  pure4,053 matched row或参与排名。
- TSA／Auteur 只有在输入、输出、数据和指标可对齐且存在可执行 artifact 时进入 formal 表；
  否则只进入 related-work 任务边界。
- Uni3C、ActCam 与 ViGen utility 不属于 StoryMotion 实验门槛。
## 4. Claim冻结表

### 4.1 初稿现在可以写死

- 方法是能力保持式非对称扩展，不是对称joint generator。
- Direct-H复用冻结Human prior；Direct-C与sequential复用同一Camera branch。
- Composition是两个条件分布的顺序组合，`joint_parallel=false`。
- seed17／23不支持稳健的单一LAT／GEO geometry胜者；C0-LAT是后续operational mainline，
  C0-GEO作为audited alternate完整报告。
- StoryMotion mainline训练只使用Pulp factual Human–Camera pairs；不构造generated-H与原GT Camera
  positive。组合式H–C pair construction是secondary utility extension，不回写mainline训练manifest，
  也不在未通过data／Stage1／Human-retention gates前授权长训。

### 4.2 必须等实验再决定

- 显式interaction16是否对free generation必要：**seed17 matched evidence已闭合，但普遍性未闭合**。
  C1REL-noI16 Stage2 Direct-C CLaTr=43.92
  相对C1REL 61.99下降18.07点、FCD恶化47.25点，同一冻结Human teacher下Direct-H几乎不变
  （TMR 17.62 vs 17.28）。这是整个消融矩阵中最大的单一效应量，支持Interaction16对Camera
  free generation的component effect，但不构成普遍必要性证明。
- HREL还是C1REL作为StoryMotion主表示；C1REL必须在sequential模式下同时改善Camera control
  并守住人物构图。
- protected asymmetric factorization是否整体优于matched symmetric joint；历史fresh P2 formal为mixed
  Pareto，证明简单的全局superiority措辞不成立。当前observed=true G-on／G-off matched pair仍在长训，
  只用于拆解route／Camera→Human gradient根因；P1 HREL仍只作同evaluator secondary control，且需要
  与P2 exact初始化匹配的C0-LAT reference rerun才能给出factorization paired estimate；该reference已与
  两臂长训并行部署，paired closure仍等待评测链与active pair审计。
- 是否优于公开baseline、是否有主观优势；由同协议主表、sealed audit与盲评决定。

### 4.3 已关闭的非核心轴

- H199 interface audit与完全独立Encodec-H／Encodec-C或双Stage2 cascade已从投稿队列删除。
  本文不声称latent接口优于显式Human API；完全独立Stage1还同时改变representation、decoder、
  参数量和Stage2接口，无法作为protected asymmetry的单变量核心消融。
- `C1REL-w/o-Interaction16`的Stage1＋Stage2审计已形成完整组件证据链：Stage1 reconstruction
  degradation → Stage2 Camera generation collapse（CLaTr −18.07）。这支持seed17 matched
  protocol下的Interaction16 component effect，但不外推为普遍必要性。
- 若正文需要更多relation机制归因，再补zero／shuffle／route检查；NoInt目前只支持I16的
  Stage1 reconstruction／framing贡献。

### 4.4 当前禁止写入摘要或contribution

- “latent直连优于普通cascade”——本文已删除该主张，且不安排相应实验。
- “interaction16对generation普遍必要”——**仍不应写入**。C1REL-noI16 matched Stage2 formal
  已完成，Camera CLaTr −18.07／FCD ＋47.25支持该seed17 matched protocol下的component effect；
  C1REL seed23只复验full C1REL，不是noI16的第二seed组件消融。
- “C1REL优于HREL”——Stage1没有形成稳定Pareto且不读取文本；仍需Camera-native adherence／
  Human-relative framing联合证据。
- “protected asymmetry全面优于symmetric joint”——fresh P2已经产生mixed-Pareto formal result；即使
  exact C0-LAT reference闭合，也必须按Human、Direct-C和sequential各字段报告，不得压成单一胜负。
- “LAT与GEO等价”或“GEO优于LAT”。
- “Stage1每个部件都必要”、全面SOTA、calibrated physical validity或production-ready。
- 同步joint generation、任意Human／Camera自由编辑、Rect、program transfer或ViGen utility。

### 4.5 Compositional utility边界

编辑不是StoryMotion的第二主问题。核心仍是capability-preserving human-motion generation与
sequential Human→Camera；composition/editing只作为secondary utility extension，失败就留作future work。
[[analysis/CVPR_2025/Dynamic_Motion_Blending_for_Versatile_Motion_Editing|MotionRemix／MotionCutMix]]
提供的是raw Human composition operator。借用它的目的不是上／下半身Human增广本身，而是构造组合式
H–C训练pairs、打破原始一对一Human–Camera pair correlation。

新pair必须在raw motion层完整构造。对composite Human，Camera program／trajectory必须独立
retarget或re-solve到该Human；随后重新生成Camera14、projection、framing与pair-dependent
Interaction16／Camera48，并按kinematic、seam、view-space与framing一致性过滤。不得直接保留已经
不再对应composite Human的$C_A$，也不得拼接旧latent，因为I16／C48与完整H–C pair相关。

数据合同必须支持many-to-many：每个Human对应多个Camera program，每个program对应多个Human。
manifest至少记录source IDs、composition operator与参数、retarget／re-solve solver、filter reason、
parent lineage和split；eval按composition-disjoint split，不能把同一source pair或同一组合泄漏到评测。

由于v9 Stage1已在Camera14、I16、C48及owning$D_c/D_f$处耦合H–C，训练顺序固定为：

1. 先做frozen Stage1 support audit，确认新pair能通过输入／重建／framing与Human-retention检查；
2. 若可支持，优先冻结$E_H/D_H$，只finetune pair-side encoder／decoder／framing，并混合factual replay；
3. 若support失败，才单独授权fresh Stage1全训，生成新的checkpoint、cache、train-only stats与owning decoder，
   并完整复验Human prior后再决定是否继续；
4. 只有Stage1 support与Human-retention gate通过后，才可授权Camera Stage2。当前不直接部署任何长训。

没有paired target Camera的组合只作unpaired diagnostic，不报告paired ADE／FDE，也不声称任意Human／Camera
自由替换。通过全部gate最多支持“受控组合式H–C下的Camera-preserving sequential generation”；若data、
Stage1 support或Human retention任一gate失败，composition/editing留作future work。

## 5. 投稿闭环顺序

方法、问题定义、数据边界、现有 seed17/23 结果与限制可以成文；data contribution 与 baseline
superiority 仍保留为条件性 claim。

1. C0-LAT 保持 operational mainline；NoInt-HREL matched Stage2 不进入当前预算。
2. C1REL Stage2 三接口与 C1REL-w/o-Interaction16 matched Stage2 已 formal；结论与完整结果分别
   由 ledger §3.15 约束。
3. HREL-vs-C1REL matched Stage2 已 formal，结论为 mixed Pareto；不把 C1REL 升格为 representation
   owner。
4. Protected-asymmetry只认fresh P2合同；旧symmetric artifact不产生metric row。历史fresh P2 formal已闭合，
   observed=true G-on／G-off matched pair是当前唯一剩余核心长训；4090 GPU1已并行部署
   exact-initialization C0-LAT同evaluator三模式formal eval与paired `source_id` row0／row1 diagnostic，
   不增加训练臂；paired closure与解释仍等待两臂完成并审计。
   P1 HREL仍只是evaluator-matched secondary control，严格因果闭环仍等待同初始化C0-LAT reference结果。
5. Native PulpMotion Stage2 已形成 matched available-data cohort 的 formal system-boundary negative
   result；保留 representation／decoder／mode 差异，不与 Pulp Stage1 reconstruction 混比。
6. 完成适用的 sealed visual audit、failure taxonomy、复现与成本包。

当前不进入 StoryMotion 核心 claim 的轴包括旧 Independent/Fully-Separate specialist Stage2、v10、
WORLD、editing长训、Camera MAE、Human locality short screen 与 DIRECT。组合式H–C utility是条件性
secondary extension，必须先完成data／Stage1 support／Human-retention gates；未通过即留future work。
v11 mainline 禁用
`joint_parallel`；所有执行日志与进度归 `runs/`，本页只记录 evidence state 与 claim gate。
## 6. 历史材料

重构前的完整reliability页与拆分前Actor–Director附录保留在
[[StoryMotion/archived/paper-scope/2026-08-03_storymotion-iclr-reliability-pre-closure-refactor]]。
它只作provenance，不是当前StoryMotion训练授权。

## 7. Formal evidence follow-up

已有 formal artifact 的共同协议是 pure `N=4,053`、`is_causal=false`，并将 v11 第三模式定义为
sequential Human→Camera。旧 `joint_parallel` artifact 保留为 provenance，不改写为 sequential。

| priority | causal experiment / run | evidence state | claim gate |
| --- | --- | --- | --- |
| P0 | Sequential protocol; C1REL `sm_c1rel_rawt0_lat_h105k_c105k_seed17_4090g0_20260804`; C1REL-noI16 `sm_c1rel_nointeraction16_rawt0_lat_h105k_c105k_seed17_4090g1_20260806` | formal complete | Supports the three-interface and matched component-effect artifacts; exact fields in ledger §3.15 |
| P1 | HREL-vs-C1REL matched comparison `sm_p1_hrel_matched_lat_h105k_c105k_seed17_4090g1_20260809` | formal complete; mixed Pareto | Keep geometry/semantic conclusions separated; no single-winner representation claim; ledger §3.16 |
| closed | C1REL seed23 repeat `sm_c1rel_lat_h105k_c105k_seed23_4090g0_20260809` | formal complete; ledger §3.17 | Report the paired-geometry all-CI-cross-zero result with the raw-caption and unpaired-semantic boundaries |
| P1 | Stage2 geometry/physical extraction | complete from existing sequential artifacts | No new training; retain no-reference diagnostic boundary |
| P2 | Historical fresh matched symmetric joint `sm_p2_matched_symmetric_joint_fresh_h105k_joint105k_seed17_4090g1_20260809`; active observed=true controls `sm_p2_obstrue_coupled_cont105k_seed17_4090g0_20260810` / `sm_p2_obstrue_detach_cont105k_seed17_5090g3_20260810` | Historical `105K` endpoint and pure4,053 three-mode formal complete; mixed Pareto. The G-on/G-off pair is still training and is not yet metric evidence; exact-init C0 reference chain is deployed | Complete and audit the C0 reference and both controls before interpreting paired/factorization closure; old invalid run remains excluded |
| P2 | Native PulpMotion Stage2 `sm_pulpmotion_repro162760_stage2_original_matched210k_seed17_5090g3_r2_20260809` | formal complete；有效弱 native-joint result | 只作 matched available-data cohort 的 system-boundary comparison；不伪装为 StoryMotion 三模式单变量对照 |
| Conditional | C1REL cfg sensitivity | not required for current claim | Only run under a frozen, predeclared evaluator contract; never use post-hoc selection |

## 8. 2026-08-09 Reviewer stress test

> [!warning] Overall risk verdict
> 模拟严格 ICLR reviewer 的当前 verdict 仍为 **Borderline / Weak Reject**。研究问题与工程证据链有价值，
> 但 acceptance 仍被 claim–evidence 间的可见缺口压住：历史true-P2本身已formal，observed=true G-on／G-off
> matched pair仍在长训；与exact-initialization
> C0-LAT的同evaluator paired audit及sealed final visual blind audit尚未完成。C1REL seed23已闭合为field-bounded repeat；
> PulpMotion native Stage2 也已闭合，但结果很弱且只能作
> system-boundary comparison。exact
> HREL-vs-C1REL Stage2 已关闭，但结论为 mixed Pareto，不能替代这些缺口。**Novelty confidence limited**：本页已依据本地 KB 挂载
> Pulp Motion、CVPR 2026 Joint Synthesis 与 Auteur，但论文仍需在 related-work 中给出逐 slot 的明确差异，
> 不能只依赖“Human–Camera joint generation”这一宽泛表述。

本节只使用当前 ledger 与本地 KB 的可核验事实；缺少的结果被标为未完成，不把“尚未测量”写成已经反驳。
P0 sequential artifact 的 run 名仍含 `rawt0`，但该命名是 immutable provenance；实际合同使用冻结的原始
Pulp captions，recaption 不是当前证据门槛。`diagnostic_only` 与 `promotion_eligible=false` 也保留为执行
授权 provenance，不否定 `N=4,053` artifact；promotion 仍是单独的作者决策层事件。

### 8.1 Evidence closure matrix

| version / run | evidence state | formal cohort / mode | current claim boundary | minimum condition for closure |
| --- | --- | --- | --- | --- |
| C1REL / `sm_c1rel_rawt0_lat_h105k_c105k_seed17_4090g0_20260804` | 完成 | `N=4,053` pure_test；Direct-H、Direct-C、sequential | 可支持当前 C1REL 三接口与 sequential artifact claim；Camera semantic aggregate高于HREL，但不可单独支持整体优于HREL/PulpMotion | ledger §3.15 已有 semantic、geometry、physical 与 hash；保持mixed-Pareto wording |
| C1REL-noI16 / `sm_c1rel_nointeraction16_rawt0_lat_h105k_c105k_seed17_4090g1_20260806` | 完成 | `N=4,053` pure_test；Direct-H、Direct-C、sequential | 支持 Interaction16 matched component ablation；仍是 seed17 evidence | 保持原始 Pulp caption 与同 protocol 的证据限定 |
| Matched Symmetric Joint / historical `sm_p2_matched_symmetric_joint_fresh_h105k_joint105k_seed17_4090g1_20260809`; active controls `sm_p2_obstrue_coupled_cont105k_seed17_4090g0_20260810` / `sm_p2_obstrue_detach_cont105k_seed17_5090g3_20260810` | Historical fresh pure4,053三接口formal完成；旧P2-1 invalid provenance-only；observed=true G-on/G-off pair仍在训练 | Historical P2 Direct-H与sequential geometry较P1 HREL secondary control改善，Direct-C及sequential semantic／framing显著回退；active pair尚无metric row，仅用于route／gradient root-cause gate | 不能将P1 paired CI写成factorization因果效应，因为其Human初始化不同；也不能支持global asymmetric superiority | 并行部署同初始化C0-LAT同evaluator reference；完成并审计active pair后再解释paired/factorization closure；永久排除旧P2-1 |
| HREL matched Stage2 / `sm_p1_hrel_matched_lat_h105k_c105k_seed17_4090g1_20260809` | formal完成；mixed Pareto | `N=4,053` pure_test；Direct-H、Direct-C、sequential；exact ordered HREL−C1REL geometry bootstrap | HREL Camera geometry更强，C1REL Camera semantic aggregate更高，Human geometry无明确差异；semantic/framing paired blocked | ledger §3.16 已有完整 semantic、geometry、physical、exception 与 hash；不写成单边 superiority |
| PulpMotion Stage2 matched available-data cohort / `sm_pulpmotion_repro162760_stage2_original_matched210k_seed17_5090g3_r2_20260809` | formal完成；有效弱 native-joint result | 210K／105K full-state checkpoint、4,053 IDs、contract、output与audit hashes闭合；同协议官方checkpoint sanity通过 | 不能把native joint task slices写成StoryMotion Direct-H／Direct-C／sequential，也不能分解checkpoint与decoder贡献 | 以ledger §3.18的system-boundary标签报告；不做事后CFG或checkpoint选择 |
| C1REL seed23 / `sm_c1rel_lat_h105k_c105k_seed23_4090g0_20260809` | formal完成；diagnostic-only | 三接口 pure `N=4,053`、artifact/hash与exact ordered comparison已闭合；所有paired geometry CI跨零 | 支持paired geometry未见seed差异；semantic aggregate没有逐样本paired unit，且raw-caption合同不具promotion资格 | ledger §3.17；不再列作执行缺口 |
| Sealed final blind audit / `sm_sealed_final_blind_audit_run_id_pending` | 未完成 | 当前 blind 目录是旧/diagnostic artifact | 不支持 selection-leakage、视觉可信度或 failure-rate claim | 冻结模型、prompt taxonomy、排序规则与 evaluator 后一次性封存并盲评 |

### 8.2 Nearest-work gap check

近邻依据为本地分析笔记：[[analysis/ICLR_2026/Pulp_Motion_Framing_aware_multimodal_camera_and_human_motion_generation|Pulp Motion]]、
[[analysis/CVPR_2026/Towards_Storytelling_Animations_Joint_Synthesis_of_Human_and_Camera_Motions|Towards Storytelling Animations]]、
[[analysis/arxiv_2026/Auteur_Language-Driven_Cinematographic_Framing_for_Human-Centric_Video_Generation|Auteur]]。

| nearest work / version | evidence-backed changed slot | StoryMotion distinction that can be defended now | gap a reviewer can still raise |
| --- | --- | --- | --- |
| Pulp Motion / ICLR 2026 | Pulp uses a shared human-camera latent plus framing-aware auxiliary sampling and projection at inference; it is the dataset/system boundary used here | StoryMotion tests a non-causal asymmetric factorization, freezes the Human owner, and routes generated-H into the same Camera branch; the C1REL-noI16 matched Stage2 degradation is direct evidence for the Interaction16 component | Native Pulp Stage2 is now formal on exactly the same `162,760/4,053` IDs, but representation, decoder and native-joint mode remain different; it closes execution, not a single-variable superiority test |
| Towards Storytelling Animations / CVPR 2026 | Three-instance joint diffusion, Toric camera coordinates, and bidirectional pairwise character-camera interaction | StoryMotion is a single-human capability-preserving factorization with observed-H and sequential interfaces, not a two-character synchronous joint generator | Both papers claim coordinated human-camera generation; without an explicit changed-slot table and exact task/data boundary, novelty can look incremental |
| Auteur / arXiv 2026 | Auteur uses Human trajectory to anchor Camera trajectory for downstream ViGen | StoryMotion works on Human motion generation and capability-preserving Human–Camera generation; it does not claim Auteur's downstream ViGen planning | State the input/output and downstream boundary explicitly; do not describe StoryMotion as a cinematographic DSL or ViGen controller |

### 8.3 Major concerns and repair paths

| # | version / run | reviewer concern | evidence-backed assessment | minimum repair or honest downgrade |
| --- | --- | --- | --- | --- |
| M1 | Cross-paper / `Pulp Motion`, `Towards Storytelling Animations`, `Auteur` | Novelty may be only “another human-camera joint model” | The KB shows prior work already covers framing-aware auxiliary sampling, synchronous entity interaction, and actor-relative cinematographic control | Add a changed-slot table: ownership/factorization, latent target, solver mode, representation, data, and claim. If not added, narrow novelty to the audited asymmetric capability-preservation result and mark confidence limited |
| M2 | C1REL / `sm_c1rel_rawt0_lat_h105k_c105k_seed17_4090g0_20260804` vs native Pulp Stage2 / `sm_pulpmotion_repro162760_stage2_original_matched210k_seed17_5090g3_r2_20260809` | Is C1REL better than PulpMotion? | Train/eval IDs now match exactly, but representation, owning decoder and generation mode differ; Pulp emits one native joint path, while StoryMotion reports three interfaces | Report the Pulp row as a system boundary and remove any single-variable superiority wording; same cohort alone does not make the methods matched |
| M3 | HREL reference / `stage1_hanchor_pulp_only_matched_r3_636k_seed17_4090g0_20260726` vs C1REL / `sm_c1rel_stage1_636k_seed17_4090g1_r2_20260803` | Does the new representation actually improve the reference? | Exact matched Stage2 is now formal: HREL geometry is stronger, C1REL Camera semantic aggregate is higher, Human geometry CI crosses zero; semantic/framing paired unit is unavailable | Withdraw single-winner wording; report mixed Pareto and keep HREL as representation owner |
| M4 | Matched Symmetric Joint / historical `sm_p2_matched_symmetric_joint_fresh_h105k_joint105k_seed17_4090g1_20260809`; active G-on/G-off controls | Is protected asymmetry causally better than symmetric joint, and does observed route or Camera→Human gradient explain the reversal? | Historical fresh P2 is formal and mixed: Human/sequential geometry can improve while Direct-C and semantic/framing regress. The active controls are not yet metrics; the existing paired P1 reference matches evaluator/protocol but not initialization | Run the exact-initialization C0-LAT endpoint through the same evaluator/noise contract in parallel; complete/audit the active pair before interpreting the paired/factorization closure, report field-wise trade-offs, and withdraw any global superiority claim |
| M5 | C1REL seed17/23 / `sm_c1rel_rawt0_lat_h105k_c105k_seed17_4090g0_20260804`; `sm_c1rel_lat_h105k_c105k_seed23_4090g0_20260809` | Is the result robust or seed-selected? | The three-interface seed23 repeat is sealed and every paired-geometry CI crosses zero; semantic/framing aggregates lack a paired unit and the repeat is raw-caption diagnostic-only | State robustness only for the audited paired-geometry fields; do not convert absence of a detected seed difference into universal equivalence |
| M6 | Sealed final blind audit / `sm_sealed_final_blind_audit_run_id_pending` | Are visual examples cherry-picked and are failure rates credible? | Existing blind artifacts are legacy/diagnostic; no sealed current final study exists | Freeze evaluator and sampling first, then blind random/best/worst slices and failure taxonomy. Until then make no visual superiority or failure-rate claim |

### 8.4 Minor concerns

| # | version / run | concern | repair |
| --- | --- | --- | --- |
| m1 | C1REL / `sm_c1rel_rawt0_lat_h105k_c105k_seed17_4090g0_20260804` | `rawt0` in the canonical alias can be misread as a non-final caption protocol | State once that original Pulp captions are authoritative and preserve the pre-migration identity through [[StoryMotion-folder-rename-map]] |
| m2 | C1REL sequential / `sm_c1rel_rawt0_lat_h105k_c105k_seed17_4090g0_20260804` | Historical `joint_parallel` rows sit beside current sequential rows | Keep the mode column and label old rows historical; never relabel them as sequential |
| m3 | Stage1 four arms / `HREL`, `HREL-noI16`, `C1REL`, `C1REL-noI16` | Stage1 metrics are complete but headline tables can hide the full field boundary | Keep four-arm full headline in this note and leave detailed numeric ownership in ledger §6.2–§6.4 |
| m4 | Stage2 geometry / `C1REL` and `C1REL-noI16` sequential | Paired geometry and physical fields are diagnostics, not calibrated physical validity | Preserve the no-reference warning and avoid “physical validity passed” wording |
| m5 | All formal rows / `StoryMotion-valid-metric-ledger` | Mixed versions can be mistaken for matched ablations | Require non-empty version/run on every row and state protocol differences next to every mixed table |

### 8.5 Evidence-backed QA / simulated rebuttal

| reviewer question | evidence-backed answer | limitation that must be conceded | rebuttal/repair wording |
| --- | --- | --- | --- |
| Why is this not just PulpMotion or a joint-diffusion reimplementation? | Pulp Motion uses framing-aware auxiliary sampling; CVPR 2026 Joint Synthesis uses synchronous three-instance Toric/bidirectional interaction; Auteur uses Human trajectory to anchor Camera trajectory for downstream ViGen. StoryMotion works on Human motion generation and capability-preserving Human–Camera generation, with frozen-Human ownership and one Camera branch supporting observed-H and generated-H sequential inference | Nearest-work novelty is not fully closed by current experiments | “We do not claim to be the first human-camera generator. Our narrower claim is an auditable capability-preserving asymmetric factorization with a generated-H→Camera interface; a slot-level comparison is provided.” |
| Is the sequential result a real formal result? | Both C1REL component runs have pure-test `N=4,053`, `mode=sequential`, `is_causal=false`, status evaluated and exact hashes in ledger §3.15; the full-C1REL seed23 repeat is sealed in §3.17 | Promotion flags remain immutable provenance; seed23 is raw-caption diagnostic-only | “The artifacts are formal4053 evidence; promotion is a separate author decision. We retain the historical flags and do not use them to rewrite provenance.” |
| Does Interaction16 matter beyond reconstruction? | Same seed17 matched Stage2 artifacts show a large Camera semantic/framing degradation when Interaction16 is removed while the frozen Human path remains close; see ledger §3.15 for the audited fields | This is one completed component-ablation seed; noI16 seed23 training is complete but its pure4,053 evaluation is not yet audited | “The result supports an Interaction16 Camera-generation ablation under the seed17 matched protocol, not a universal component-necessity theorem. We will report seed23 only after its independent full-cohort audit.” |
| Does C1REL beat HREL? | Exact ordered pure4,053 HREL-vs-C1REL Stage2 comparison is formal in ledger §3.16: HREL has stronger Camera geometry, C1REL higher Camera semantic aggregates, Human geometry CI crosses zero | Semantic/framing records lack a per-sample paired unit, so semantic significance is blocked; conclusion is mixed Pareto | “We withdraw a single-winner claim: HREL remains the representation owner, C1REL is retained as a tested control, and the comparison is reported as mixed Pareto.” |
| Does protected asymmetry beat a symmetric joint model? | Fresh true-P2 completed pure4,053 Direct-H、Direct-C与sequential. Against the evaluator-matched P1 secondary reference, P2 improves Human and sequential geometry but sharply degrades Direct-C and sequential semantic/framing | P1 uses a different Human initialization, so its paired CI is not the strict factorization estimate; the exact-initialization C0-LAT same-evaluator three-mode chain is deployed but not yet audited | “The evidence rejects a one-number winner: symmetric joint updates do not necessarily damage Human quality, but they weaken the usable Camera interface. We report this mixed Pareto and reserve causal factorization wording until the deployed exact C0 reference is paired.” |
| Where are the Direct-H baselines? | MoMask-Pulp native and MotionLab-MFT both have human-text-only pure4,053 formal artifacts; MoMask also has a byte-exact replay, while MotionLab-MFT is explicitly a Pulp-latent adaptation | MoLingo-derived v7.45 is only a provisional screen because its result requests promotion audit and its recorded training-source SHA is unrecoverable; MotionStreamer has no Stage2 generator | “We report MoMask as a native-system peer and MotionLab-MFT as an adapted operator peer. We disclose the MoLingo screen outside formal ranking and do not turn MotionStreamer reconstruction into generation evidence.” |
| Where are the Direct-C baselines? | Corrected Director-C／E.T. has a native pure4,053 formal endpoint; CCD-Pulp has a fixed 60K endpoint, sealed IDs, contract and complete records | Director consumes GT pelvis trajectory and emits native 9D C2W; CCD uses a v7.14 latent/decoder and has no independent audit artifact. Neither has matched decoded Cam-ADE/FDE/rotation | “We report their semantic/distribution rows with condition/decoder and assurance boundaries, mark CCD accordingly, and leave unmatched geometry blank rather than borrowing StoryMotion values.” |
| Is C1REL better than PulpMotion? | Native Pulp Stage2 is now formal on the exact same `162,760/4,053` ID sets, and its weak result passed evaluator-path sanity | Pulp uses a different representation, owning decoder and native-joint mode, so this remains a system comparison rather than a single-variable ablation | “We report the matched-cohort Pulp result transparently but do not claim that cohort matching isolates architecture; mode and decoder boundaries remain explicit.” |
| Does one seed support robustness? | Full C1REL now has a sealed seed23 three-interface repeat; all seed23−seed17 paired-geometry CIs cross zero | This does not repeat the noI16 component arm, semantic aggregates lack a paired unit, and the sealed blind audit is separate | “We report field-specific paired-geometry robustness for full C1REL; the Interaction16 component effect remains seed17 evidence, and we make no universal equivalence claim.” |
| Are the visual examples trustworthy? | Current artifacts support formal metrics and fixed-sample provenance | No sealed final blind study or failure taxonomy exists | “We will freeze sampling and report random/best/worst blind slices; until then visual superiority is not claimed.” |
| Is the physical story solid? | Stage1 and sequential artifacts expose paired geometry and decoded-Human physical aggregates | These are paired/no-reference diagnostics, not calibrated physical validity; Stage2 CI is not yet a sealed result | “We report them as diagnostics, retain units and caveats, and do not claim physical-validity certification.” |

### 8.6 Repair paths and re-review checklist

1. **Positioning repair:** add the three-work changed-slot table and explicitly narrow the novelty statement to
   capability-preserving asymmetric factorization, frozen-Human ownership, and the matched Interaction16
   Camera-generation ablation. Do not claim first joint human-camera generation or latent superiority.
2. **Fair baseline repair:** report the audited MoMask-Pulp native and MotionLab-MFT adapted Direct-H
   rows; keep MoLingo-derived v7.45 outside formal ranking until its audit/source provenance closes.
   Report corrected Director-C／E.T. and the explicitly lower-assurance CCD-Pulp Direct-C row, plus the
   PulpMotion native-joint `210K` boundary, with representation／decoder／condition fields. MotionStreamer
   cannot enter the generation table until its native text→motion Stage2 is complete.
3. **Representation repair:** the exact HREL-vs-C1REL matched Stage2 has now been completed under the
   same original Pulp captions, ordered pure4,053 cohort and `is_causal=false`; report its mixed-Pareto
   result and downgrade any single-winner wording.
4. **Factorization/robustness repair:** historical fresh P2 train/eval is complete and yields a mixed Pareto;
   the observed=true G-on／G-off matched controls are the only remaining core long trains and must be
   completed/audited before interpreting the factorization result. The exact-initialization C0-LAT
   same-evaluator reference is deployed in parallel; its paired closure is gated by that chain and active-pair audit. The full-C1REL seed23 repeat is sealed; noI16 seed23 is a separate full-cohort evaluation now
   in progress and must not be inferred from that full-C1REL repeat.
5. **Visual repair:** latent-interface superiority and its H199/cascade experiment queue have been
   removed from scope. Freeze a sealed blind audit with random/best/worst slices, failure taxonomy and
   no post-hoc model selection.
6. **Documentation repair:** keep detailed numeric values and hashes only in
   [[StoryMotion-valid-metric-ledger]]；reliability owns decisions and gaps，`runs/` owns execution
   logs and progress.

Re-review should be requested only after every applicable item below is true:

- [ ] related-work changed-slot table covers Pulp Motion, CVPR 2026 Joint Synthesis and Auteur;
- [x] PulpMotion Stage2 matched available-data cohort has a complete contract, audit and explicit system-boundary label;
- [x] exact HREL-vs-C1REL Stage2 comparison is formal `N=4,053` and recorded as mixed Pareto in ledger §3.16;
- [x] C1REL seed23 three-interface formal result is sealed with field-specific uncertainty boundaries;
- [ ] sealed visual blind audit and failure taxonomy are complete;
- [x] latent-interface superiority is deleted; no H199 or independent dual-codec/cascade experiment is queued;
- [ ] every mixed metric table has non-empty version/run and points to the single ledger owner;
- [ ] original Pulp captions are stated as authoritative, with no active recaption gate;
- [ ] no claim says C1REL > HREL/PulpMotion, protected asymmetry globally > symmetric joint, or calibrated physical validity without the corresponding evidence.

## 9. Durable submission queue

本页只保留投稿门槛、证据状态、关闭条件及其所约束的 claim；运行步骤与 worker output 归
`runs/`，不在此重复。

| priority | version / run | evidence state | close condition | claim gated |
| --- | --- | --- | --- | --- |
| closed | PulpMotion Stage2 matched available-data cohort / `sm_pulpmotion_repro162760_stage2_original_matched210k_seed17_5090g3_r2_20260809` | formal complete；valid weak native-joint result；ledger §3.18 | —；永久保留representation／decoder／mode差异 | 仅支持external system-boundary reporting，不支持单变量 superiority |
| Q1 | True Matched Symmetric historical / `sm_p2_matched_symmetric_joint_fresh_h105k_joint105k_seed17_4090g1_20260809`; active observed=true G-on/G-off controls | 历史pure4,053三接口formal完成；mixed Pareto；ledger §3.19；active pair仍在长训；旧 `sm_p2_1_matched_symmetric_joint_h105k_c105k_seed17_4090g0_20260808` invalid | 并行部署exact-initialization C0-LAT同evaluator/noise reference；完成并审计两条active control后再做paired/factorization closure | protected asymmetry vs symmetric joint的field-wise边界 |
| closed | C1REL seed23 / `sm_c1rel_lat_h105k_c105k_seed23_4090g0_20260809` | 三接口 pure `N=4,053` 与 hash formal闭合；ledger §3.17 | —；保留raw-caption、diagnostic-only与unpaired-semantic边界 | 只支持audited paired-geometry field robustness |
| closed | Matched HREL Stage2 / `sm_p1_hrel_matched_lat_h105k_c105k_seed17_4090g1_20260809` | ledger §3.16 formal closed；mixed Pareto | — | HREL vs C1REL representation choice |
| Q2 | Sealed visual audit / `sm_sealed_final_blind_audit_run_id_pending` | incomplete | Freeze evaluator/cohort and complete random/best/worst blind study plus failure taxonomy | visual credibility and selection-leakage rebuttal |
| future / conditional | Composite H–C utility data and Stage1 support audit / no run authorized | not started; no long train authorized | Construct retargeted/re-solved many-to-many pairs, recompute Camera14/projection/framing/I16/C48, filter, seal composition-disjoint eval, then pass frozen-Stage1 support and Human-retention gates before any pair-side finetune or Stage2 | secondary utility only; no free-editing claim |
