---
title: "StoryMotion Repository Valid Metric Ledger"
status: active
hypothesis: |
  The single StoryMotion repository has one numeric owner. Active evidence
  starts with the v9 usable owner and requires complete pure4053 formal data
  unless an explicitly labeled special diagnostic is being audited.
tags:
  - StoryMotion
  - DIRECT
  - Motion_Generation
  - metric
  - evidence
  - status/active
aliases:
  - StoryMotion-Valid-Metrics
source_notes:
  - "[[StoryMotion/current]]"
  - "[[DIRECT/current]]"
  - "[[version_family]]"
  - "[[Storymotion-exp-sha]]"
  - "[[StoryMotion-metric-computation-io]]"
  - "[[paper-boundary]]"
created: 2026-07-12T12:15:00+08:00
updated: 2026-08-13T02:12:50+08:00
---

# StoryMotion Repository Valid Metric Ledger

> [!abstract] Canonical numeric owner
> 本页是 StoryMotion／DIRECT 共用的唯一正式 numeric owner。活动证据从第一个可用的 v9 Pulp-only owner 开始；旧 v7/v8、C3-25 完整证据由 [[archived/metrics/2026-07-24_StoryMotion-valid-metric-ledger_pre-human-first-orthogonalization]] 拥有，普通 N512/first-512 generation rows 由 [[archived/metrics/2026-08-10_StoryMotion-valid-metric-ledger_pre-v9-and-nonfull]] 索引。artifact、checkpoint、contract、result、records 与 audit hash 仍保持 immutable provenance，完整 identity 见 [[Storymotion-exp-sha]]。

> [!important] 读表原则
> Formal generation rows 必须是完整 Pulp pure-test `N=4,053`，并在每行标出 `version / run`、mode、representation／decoder boundary 与 sampler。普通 N512、first-512、N64/N128 和中间训练 snapshot 不属于当前 ranking；其 provenance index 见 [[archived/metrics/2026-08-10_StoryMotion-valid-metric-ledger_pre-v9-and-nonfull]]。swap、intervention、calibration、locality 与 fixed-cohort mechanism 可保留为 `special diagnostic`，但不得伪装为 full-cohort evidence。

## 1. Active evidence contract

- StoryMotion Stage1/Stage2 active paths require `is_causal=false`.
- Active v11 modes are Direct-H, Direct-C and sequential Human→Camera. `joint_parallel=false`; evolving-H solver is closed.
- Direct-H is Human-text-only. Direct-C is observed Human latent plus Camera text. Sequential first samples final Human, then samples Camera with that frozen Human.
- v11 C0-LAT is the operational Camera-only latent-flow mainline at Camera optimizer `105K`; C0-GEO shares exact v9 Stage1/Human owner and adds decoded Camera/framing geometry objective as an audited alternate.
- HREL, C1REL, true-P2 and the observed-Human G-on/G-off route controls are v9+ full-cohort system/ablation evidence. A row may compare systems, but different representation, decoder, objective, initialization, runtime or mode prevents a single-variable causal claim.
- Formal data boundary is complete materializable train/eval IDs `162,760/4,053`; PulpMotion's “matched available-data cohort” is the same ID set, not a smaller StoryMotion subset.
- Loss/TensorBoard values, training progress and deployment logs remain in run artifacts; this page owns decoded metric results and audit boundaries only.

## 2. Canonical metric schema

| branch | metrics | interpretation |
| --- | --- | --- |
| Human semantic | FDTMR↓, TMR↑, coverage/density/precision/recall↑, R1/R2/R3↑, MM distance↓ | text-motion/distribution space |
| Human paired | global/root-aligned MPJPE↓, root ADE/FDE↓, integrated yaw↓ | paired diagnostic; root-aligned removes translation but not heading |
| Camera semantic | FDCLaTr↓, CLaTr↑, coverage/density/precision/recall↑, R1/R2/R3↑, MM distance↓ | text-camera/distribution space |
| Camera caption | caption P / R / F1 ↑ | weighted Camera movement segment classification |
| Camera geometry | Camera center ADE/FDE↓, rotation↓ | decoded paired trajectory error |
| projection | projective joint UV L2↓, r-FPD↓, zero-visible Out↓ | generated Human reprojected through generated Camera |
| physical | bone CV ↓, speed/acceleration/jerk ↔ reference, contact heuristic ↔ reference, skate heuristic ↓ | no-reference decoded diagnostics; arrows are reporting conventions, not calibrated physical validity |

Definitions and callback keys are canonical in [[StoryMotion-metric-computation-io]]. Disabled zero-valued projection PRDC/error fields are excluded from all conclusions. For no-reference physical/kinematic fields, `↔ reference` means compare the same-cohort distribution rather than optimize monotonically; static collapse and contact inflation are not improvements.

## 3. Active full-cohort Stage1 owner

The active Stage1 owner is the v9 Pulp-only non-causal representation:
`normalized Human199 + official Camera14 → Human128 + Interaction16 + Camera48`, exact owning `D_h/D_c/D_f`, train-only normalization and true-length decoding. Complete audited fields, run identities and hashes are retained under [[#4B. v9+ Stage1 audited detail tables]].

HumanML3D `N=1,460` root/local reconstruction is a cross-domain special diagnostic and is not an active full-cohort row.

## 4. Active Stage2 full-cohort evidence

The active Stage2 headline is v11 C0-LAT at Camera optimizer `105K`; C0-GEO, HT-FILM/HX/DR, HREL, C1REL, C1REL-noI16, seed23 repeat, Pulp native, True-P2 and the observed-Human G-on/G-off route controls remain auditable controls. Complete pure4053 fields, hashes and exception boundaries are retained under [[#4A. v9+ Stage2 audited detail tables]].

### 4.1 C0-LAT competition snapshot (pure4053 formal)

This compact reviewer-facing snapshot uses only complete pure4,053 formal rows already owned by this ledger. Every non-`—` cell in a row comes from the same run; the columns show the corresponding inference mode rather than a cross-mode composite. Direct-C Human fields are observed-H diagnostics. `FDTMR/TMR`, `FDCLaTr/CLaTr`, and `ADE/FDE` follow the metric directions in §2.

| display ID / canonical run alias | cohort / protocol | Direct-H Human FDTMR ↓ / TMR ↑ | Direct-C Camera FDCLaTr ↓ / CLaTr ↑ | Direct-C Cam ADE / FDE ↓ m / rotation ↓ deg | sequential Camera FDCLaTr ↓ / CLaTr ↑ | sequential caption F1 ↑ | sequential Cam ADE / FDE ↓ m / rotation ↓ deg | comparison boundary |
| --- | --- | --- | --- | --- | --- | ---: | --- | --- |
| v11 C0-LAT / `v11_c0_lat_fixedh_35to105k_seed17_5090g2_r2_20260730` | pure4,053; v9 owner; three active modes | 99.391 / 17.608 | 21.171 / 56.933 | 1.4125 / 1.4985 / 29.922 | 28.754 / 55.579 | 0.6935 | 2.9428 / 3.0422 / 71.435 | operational mainline |
| v11 C0-LAT no-source / `sm_c0_lat_nosource_c105k_seed17_4090g0_20260812` | pure4,053; exact v9 owner; source embedding absent; three active modes | 99.391 / 17.608 | 20.912 / 56.984 | 1.4213 / 1.5068 / 29.631 | 31.987 / 55.185 | 0.6864 | 2.9092 / 3.0103 / 70.860 | audited implementation-clean candidate; aggregate mixed, so no automatic metric-mainline replacement |
| Independent dual-EncDec / `sm_independent_dual_encdec_lat_h105k_c105k_seed17_4090g1_20260811` | pure4,053; independent H128/C64 owners, decoders, cache and normalizers; three active modes | 132.930 / 15.668 | 11.740 / 64.482 | 1.6213 / 1.6956 / 34.039 | 24.941 / 63.908 | 0.8016 | 2.9843 / 3.0763 / 71.470 | secondary native-system boundary; mixed, promotion-ineligible |
| v11 C0-GEO / `v11_c0_geo_fixedh_35to105k_seed17_5090g3_r2_20260730` | pure4,053; same v9 owner; objective alternate | 99.391 / 17.608 | 20.540 / 57.574 | 1.3860 / 1.4711 / 29.800 | 29.505 / 56.103 | 0.7007 | 2.9368 / 3.0395 / 71.507 | audited objective alternate; no single-winner claim |
| v11 HT-DR / `v11_ht_dr_fresh105k_seed17_4090g0_r2_20260801` | pure4,053; C0-GEO-matched Human-text Camera control | 99.391 / 17.608 | 17.586 / 58.840 | 1.4141 / 1.5014 / 29.572 | 24.564 / 58.145 | 0.7436 | 2.9460 / 3.0473 / 71.162 | semantic/caption-leading control; not a global winner |
| HREL / `sm_p1_hrel_matched_lat_h105k_c105k_seed17_4090g1_20260809` | pure4,053; HREL owner; three active modes | 100.254402 / 17.354467 | 22.199497 / 57.238335 | 1.424767 / 1.510033 / 30.037865 | 30.147327 / 55.586891 | 0.701713 | 2.893823 / 3.000069 / 71.159801 | representation/decoder control; mixed-Pareto comparison |
| C1REL / `sm_c1rel_rawt0_lat_h105k_c105k_seed17_4090g0_20260804` | pure4,053; C1REL owner; three-interface formal | 104.331841 / 17.276762 | 18.183035 / 61.985516 | 1.709340 / 1.785491 / 35.901068 | 17.322052 / 61.360668 | — | 2.990472 / 3.093771 / 71.352258 | representation control; no semantic paired-unit significance claim |
| C1REL-noI16 / `sm_c1rel_nointeraction16_rawt0_lat_h105k_c105k_seed17_4090g1_20260806` | pure4,053; Interaction16 removed; three-interface formal | 92.033676 / 17.619104 | 65.427673 / 43.920853 | 1.665444 / 1.777655 / 41.145027 | 89.051743 / 41.235523 | — | 2.646307 / 2.745572 / 67.081549 | matched component ablation; not a universal necessity claim |
| True-P2 / `sm_p2_matched_symmetric_joint_fresh_h105k_joint105k_seed17_4090g1_20260809` | pure4,053; symmetric-joint diagnostic; three active modes | 97.553619 / 18.013281 | 131.628693 / 37.851692 | 2.025185 / 2.145800 / 49.877689 | 104.280891 / 40.078587 | 0.499214 | 2.476393 / 2.583847 / 64.814241 | fresh symmetric joint; diagnostic-only, not causal rank |
| observed=true, G=on / `sm_p2_obstrue_coupled_cont105k_seed17_4090g0_20260810` | pure4,053; source row1; 4090 runtime; three active modes | 102.445770 / 17.845230 | 33.146400 / 54.313377 | 2.388501 / 2.498247 / 56.352396 | 23.822430 / 58.139671 | 0.741294 | 2.918527 / 3.029785 / 70.852242 | route-control diagnostic; mixed Pareto, not a promoted system |
| observed=true, G=off / `sm_p2_obstrue_detach_cont105k_seed17_5090g3_20260810` | pure4,053; source row1; 5090 runtime; three active modes | 96.372887 / 18.613176 | 29.300417 / 55.365463 | 2.501148 / 2.616128 / 58.310559 | 25.601322 / 57.573360 | 0.743736 | 2.980856 / 3.099442 / 70.781130 | detached route control; host/runtime is an explicit covariate |
| PulpMotion native / `sm_pulpmotion_repro162760_stage2_original_matched210k_seed17_5090g3_r2_20260809` | pure4,053; native-joint only | — | — | — | — | — | — | native-joint TMR/FDTMR=`15.332323 / 375.383148`; CLaTr/FDCLaTr=`14.281564 / 275.958374`; no direct StoryMotion ranking |

The table is a protocol-aware snapshot, not a single leaderboard: representation, owning decoder, objective, initialization, and native-joint versus asymmetric mode differences remain explicit. Exact fields, artifact identities, hashes, and uncertainty boundaries are retained in the detailed Stage2 sections below.

No scalar aggregate or preregistered utility weighting defines “overall best.” HT-DR leads the listed
Camera semantic/caption fields, but its six Camera geometry CIs against C0-GEO cross zero and its
Direct-C r-FPD/Out regress; it is therefore a conditional semantic/caption winner rather than an
unqualified replacement for C0-LAT.

#### C0-LAT／C0-GEO／HT-DR comprehensive comparison

下列三表只比较这三个有力竞争者，均为pure-test `N=4,053`、seed17、Euler50与同一个
v9 Stage1／冻结Human owner。HT-DR与C0-GEO共享GEO objective、初始化、batch／noise trace
和Camera `105K`预算；C0-LAT的Camera objective不同，因此HT-DR−C0-LAT不是单变量消融。
所有数值来自本页后续正式artifact；不是跨表挑选或重新聚合。

| display ID / canonical run alias | Camera training setting | comparison role |
| --- | --- | --- |
| C0-LAT / `v11_c0_lat_fixedh_35to105k_seed17_5090g2_r2_20260730` | latent-flow Camera objective；无Human-text Camera注入 | operational mainline |
| C0-GEO / `v11_c0_geo_fixedh_35to105k_seed17_5090g3_r2_20260730` | latent flow＋decoded Camera／framing geometry objective；无Human-text Camera注入 | exact no-Human-text parent for HT-DR |
| HT-DR / `v11_ht_dr_fresh105k_seed17_4090g0_r2_20260801` | C0-GEO-matched fresh Camera；Human observation驱动Camera-velocity residual | Human-text／Human-observation mechanism control |

| version / run | mode | FDTMR ↓ / TMR ↑ | FDCLaTr ↓ / CLaTr ↑ | coverage / density / precision / recall ↑ | caption P / R / F1 ↑ | r-FPD / Out ↓ | Human geometry ↓ m | Camera ADE / FDE ↓ m / rotation ↓ deg |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| C0-LAT / `v11_c0_lat_fixedh_35to105k_seed17_5090g2_r2_20260730` | Direct-C observed-H | — | 21.171 / 56.933 | 0.8303 / 1.0932 / 0.9156 / 0.5566 | 0.7857 / 0.7000 / 0.7372 | 0.8465 / 0.1052 | observed-H global/root-aligned MPJPE `0.125466 / 0.048796` | 1.412472 / 1.498528 / 29.922 |
| C0-GEO / `v11_c0_geo_fixedh_35to105k_seed17_5090g3_r2_20260730` | Direct-C observed-H | — | 20.540 / 57.574 | 0.8236 / 1.0604 / 0.9062 / 0.5589 | 0.7900 / 0.7075 / 0.7442 | 0.8514 / 0.1017 | observed-H global/root-aligned MPJPE `0.125466 / 0.048796` | 1.385987 / 1.471145 / 29.800 |
| HT-DR / `v11_ht_dr_fresh105k_seed17_4090g0_r2_20260801` | Direct-C observed-H | — | 17.586 / 58.840 | 0.8377 / 1.0986 / 0.9084 / 0.5754 | 0.8177 / 0.7339 / 0.7711 | 0.8699 / 0.1075 | observed-H global/root-aligned MPJPE `0.125455 / 0.048795` | 1.414115 / 1.501362 / 29.572 |
| C0-LAT / `v11_c0_lat_fixedh_35to105k_seed17_5090g2_r2_20260730` | sequential Human→Camera | 99.391 / 17.608 | 28.754 / 55.579 | 0.7735 / 1.0100 / 0.8949 / 0.5241 | — / — / 0.6935 | 0.5082 / 0.0773 | global/root-aligned MPJPE `0.842760 / 0.228751` | 2.942785 / 3.042185 / 71.435 |
| C0-GEO / `v11_c0_geo_fixedh_35to105k_seed17_5090g3_r2_20260730` | sequential Human→Camera | 99.391 / 17.608 | 29.505 / 56.103 | 0.7626 / 1.0042 / 0.8939 / 0.5164 | — / — / 0.7007 | 0.5098 / 0.0768 | global/root-aligned MPJPE `0.842760 / 0.228751` | 2.936792 / 3.039527 / 71.507 |
| HT-DR / `v11_ht_dr_fresh105k_seed17_4090g0_r2_20260801` | sequential Human→Camera | 99.391 / 17.608 | 24.564 / 58.145 | 0.7804 / 0.9968 / 0.8774 / 0.5512 | — / — / 0.7436 | 0.4943 / 0.0781 | global/root-aligned MPJPE `0.842762 / 0.228751` | 2.945997 / 3.047307 / 71.162 |

Direct-H与decoded-Human physical/kinematic可合并，因为三份独立run使用同一冻结Human
owner并通过replay gate；这里的一行表示**三份run的相同来源输出**，不是均值、ensemble或
一个联合实验。跨5090／4090的末位差仅为已审计GPU roundoff，精确逐run值保留在§4A的
Human-text formal表。

| version / run membership | applicable modes | Direct-H FDTMR ↓ / TMR ↑ | global / root-aligned MPJPE ↓ m | root ADE / FDE ↓ m | bone CV ↓ | joint speed / accel / jerk ↔ reference | root speed / accel / jerk ↔ reference | contact ↔ reference / skate ↓ |
| --- | --- | --- | --- | --- | ---: | --- | --- | --- |
| C0-LAT；C0-GEO；HT-DR（3份run，共享冻结Human owner） | Direct-H = sequential Human | 99.391 / 17.608 | 0.842760 / 0.228751 | 0.758772 / 1.283039 | 2.280e−7 | 0.025358 / 0.023125 / 0.036800 | 0.017803 / 0.011937 / 0.016892 | 0.59616 / 0.030608 |

Direct-C的physical row同样只是observed-H经同一Stage1 owner的重建；三份run均约为
`bone CV=2.467e−7`、`joint speed/accel/jerk=0.037159/0.030219/0.046381`、
`root speed/accel/jerk=0.030292/0.019720/0.027753`、`contact/skate=0.49199/0.041857`。
因此这些字段验证Human路径未被Camera设计改变，不用于给三种Camera方案排序。

### 4.2 Interface-specific external baselines

本节把已经重新核验的外部／operator baselines迁回当前投稿比较。`v9+`限制适用于
StoryMotion自身版本排名，不排除在同一pure-test `N=4,053`上完成正式评测的外部系统。
这些行共享Pulp test identity，但representation、owning decoder、sampler与训练预算并不都匹配；
因此只能作system-level comparison，不能解释为StoryMotion组件的单变量消融。

#### Direct-H: Human text → Human motion

| version / run | role and training boundary | N | FDTMR ↓ | TMR ↑ | HCov ↑ | root-aligned / global MPJPE ↓ mm | root ADE / FDE ↓ mm | comparison boundary |
| --- | --- | ---: | ---: | ---: | ---: | --- | --- | --- |
| v11 C0-LAT / `v11_c0_lat_fixedh_35to105k_seed17_5090g2_r2_20260730` | frozen canonical Human `105K` teacher；v9 H128 owning decoder；Euler50/CFG4 | 4,053 | 99.391 | 17.608 | 71.58% | 228.751 / 842.760 | 758.772 / 1,283.039 | StoryMotion operational mainline；system-level reference |
| MotionLab-MFT / `baseline_motionlab_mft_v714_human_seed17_4090g0_20260716` | MotionLab MFT operator adapted to Pulp v7.14 latent/decoder；human-only；RF50/CFG2.5；`30K×512=15.36M` exposures | 4,053 | 156.350 | 18.172 | 59.19% | 250.782 / 951.380 | 857.640 / 1,436.396 | formal representation-matched operator peer；不是未经修改的官方MotionLab |
| MoMask-Pulp native / `momask_pulp_human_native_seed17_5090g3_stage1matched_20260716` | native non-causal RVQ-VAE `159K`＋Mask/Residual Transformer各`240K`；native owning decoder | 4,053 | 219.553 | 27.347 | 45.50% | 316.113 / 1,160.494 | 998.888 / 1,610.472 | formal native-system peer；第二次4,053-record replay byte-exact |

MoLingo-derived v7.45暂不进入上面的formal comparison。其完整4,053 screen为
`FDTMR=149.163↓`、`TMR=17.729↑`、`HCov=49.86%↑`、root-aligned/global
`MPJPE=242.502/1,249.134 mm↓`、root `ADE/FDE=1,164.249/2,007.279 mm↓`；但result自身仍为
`metric_status=run`并写明promotion需要contract audit，缺独立audit artifact，且现存训练源码
SHA与result记录不一致。它只能称为“MoLingo-derived provisional operator screen”，不能称为
官方MoLingo或audited formal baseline。

MotionStreamer-Pulp当前只有native causal TAE的Stage1 pure4,053 reconstruction，尚无
text→motion Stage2 generation result，故不填入Direct-H数值表。其Stage1 overall
root-aligned/global MPJPE为`79.937 / 281.524 mm`，只能作为owning-tokenizer reconstruction
diagnostic；owner checkpoint SHA256为
`825b15e3946bc511fa560ae9f7b34a76d1d19458d01aad0ec36be15a1b57016d`。native Stage2必须
继续使用MotionStreamer的causal tokenizer与decoder，并保持在StoryMotion Stage1/Stage2合同
之外。当前4090副本缺官方loader与Pulp199 sequence-level latent exporter，故本轮没有创建
Stage2 run，不能把“尚未实现”写成失败结果。

#### Direct-C: observed Human + Camera text → Camera motion

| version / run | role and observed-H boundary | N | FDCLaTr ↓ | CLaTr ↑ | CCov ↑ | caption P / R / F1 ↑ | Camera R1 / R2 / R3 ↑ | precision / recall / density ↑ | MM distance ↓ | comparison boundary |
| --- | --- | ---: | ---: | ---: | ---: | --- | --- | --- | ---: | --- |
| v11 C0-LAT / `v11_c0_lat_fixedh_35to105k_seed17_5090g2_r2_20260730` | v9 observed-H latent＋Camera text；C0-LAT Camera64；Euler50 | 4,053 | 21.171379 | 56.933498 | 83.0257% | 0.785682 / 0.700022 / 0.737150 | 0.234888 / 0.395756 / 0.509252 | 0.915614 / 0.556641 / 1.093173 | 23.4027 | StoryMotion operational mainline；decoded geometry见§4A |
| Director-C native / `director_c_pure_matched_seed17_5090g3_20260716` | corrected E.T./DIRECTOR endpoint；GT pelvis trajectory＋raw Camera text；native direct 9D C2W、EDM10/CFG1.4 | 4,053 | 32.436531 | 52.661713 | 81.4944% | 0.752748 / 0.647030 / 0.688359 | 0.128053 / 0.229213 / 0.310141 | 0.899821 / 0.569958 / 1.050549 | 24.2063 | valid native external baseline；不存在StoryMotion tokenizer／decoder；decoded Camera geometry未审计 |
| CCD-Pulp / `ccd_pulp_camera_completion_v714_seed17_4090g1_20260716` | Cinematographic Camera Diffusion adapter；GT-H v7.14 latent＋Camera text；DDIM50/CFG2 | 4,053 | 101.026993 | 33.094883 | 59.9061% | — / — / 0.441915 | 0.222304 / 0.364915 / 0.472736 | 0.828761 / 0.393054 / 0.866654 | — | contract-complete task peer；fixed 60K endpoint、完整IDs与records可核验，但无独立audit artifact；非v11表示且无decoded geometry |

Director-C训练集为162,760条、94 epochs／239,136 optimizer steps，实际exposure为
15,299,440（epoch rounding导致不是名义15.36M）；checkpoint不是test selection。CCD-Pulp为
`60K×256=15.36M` exposures。两者均只在已有semantic/distribution字段比较；缺失的decoded
Camera center／rotation geometry保持空白。

#### Native joint: Human–Camera joint generation

| version / run | native mode | N | Human FDTMR ↓ / TMR ↑ / coverage ↑ | Camera FDCLaTr ↓ / CLaTr ↑ / coverage ↑ | caption F1 ↑ | outscreen ↓ / projection error ↓ / r-FPD ↓ | comparison boundary |
| --- | --- | ---: | --- | --- | ---: | --- | --- |
| v11 C0-LAT / `v11_c0_lat_fixedh_35to105k_seed17_5090g2_r2_20260730` | asymmetric sequential Human→Camera | 4,053 | 99.391 / 17.608 / 71.58% | 28.754 / 55.579 / 77.35% | 0.6935 | 7.73% / — / 0.5082 | StoryMotion sequential reference；与native joint任务不等价，不作单变量胜负 |
| PulpMotion native / `sm_pulpmotion_repro162760_stage2_original_matched210k_seed17_5090g3_r2_20260809` | native joint only；fresh `210K`；matched available-data cohort | 4,053 | 375.383148 / 15.332323 / 21.2433% | 275.958374 / 14.281564 / 31.8780% | 0.174287 | 54.2279% / 1.893503 / 11.336928 | valid negative system boundary；不是Direct-H、Direct-C或sequential；无decoded StoryMotion geometry |

| version / run | checkpoint SHA-256 | contract SHA-256 | result SHA-256 | records / audit SHA-256 |
| --- | --- | --- | --- | --- |
| MoLingo-derived provisional / `v7_45_molingo_offline_masked_ar_human240k_seed17_4090g0_20260717` | `4669a56fb6c9a4adafc2cfedef39b27c060cd00949a7407c86c68cc9fa30200d` | `34544e1588a5af63614a1b04c50e2481c6f73ed97e21cfc3ab93ba657a2d163a` | `445695958ba86c11831cbc8f931939c71f72135453b21ca6b6d5e2f170b6f685` | records `6edb7d5f9e54a61540b175028cad6911d5b573d4290e7dc95edc7e6fce122a9c`; no independent audit |
| MotionLab-MFT / `baseline_motionlab_mft_v714_human_seed17_4090g0_20260716` | `45477134830f25c58b6db2ea54cfdce4cadd8f0e84c0e9312f1ead73bce468dd` | `a2f4d063bad486075084d9a66d06084a430f012d28356f42a4b161f8eaef8002` | semantic `bd8eba338960f3be71bf6f97d269e3c85183766ae1a2c93f83b7f4cd80633bcb`; geometry re-audit `f1a45654d740d8937152c96b75f88a53a765bc37977719d6628ccef6c36d79ba` | records `2b6d42544e75ad330e01091e4a3a294a67e02f2fe0db17ba14fc12e5afdca765` |
| MoMask-Pulp native / `momask_pulp_human_native_seed17_5090g3_stage1matched_20260716` | VQ `e21d42684e4441b67782b8951e1a5e6c9e5c25bbd1bc460aa7fda138ea348664`; Mask `037871329eaf980e320961445f5492c7a79ad85d60e9e2b79640678dfabeff3c`; Residual `89faab30ffb62d185a789a814ae7c061ed5f5375f9ce5128dc4764756c43e0b1` | `94a217f900e26212e523dd1f0444fbbba5e6392a7c424e0441bab19c02238901` | `3a133b834bfac8203a9bfb92cea55e0127f50369bc51c68a53bb3b0d877baf70` | records `6545ab1a4e17bc13b73663aafd983b439ccae664b016251640dcc22a0e067ed8`; audit `71bd4b1d31409a8e70e991715ee7a09ee1706384df39831ea575e9f4a2ff3232` |
| Director-C native / `director_c_pure_matched_seed17_5090g3_20260716` | `ad27564052465ff11f5264c5606473f2daacaaf74abbf45adc7b563328b5e823` | `3a3635be17fa1c6cc155fa8e5ad7339d46e446c55195ec9ca1b350390addcaa1` | `f9693592d62780dd2a4ed330dc2b102b88b775a839e459c6adefc6eb2bd97b15` | records `e0734d76e316dc5f66149214e2daf7cbdd42adaeec17c796a1897e88dfaf2e4a` |
| CCD-Pulp / `ccd_pulp_camera_completion_v714_seed17_4090g1_20260716` | `8014b120c218a7ce8bd7d6f6c3e381cc009939950926da847c4dc2597f6603da` | `bb1818fb9703035d34bc691bdbffe82a3c9447c9c68a3b6010cd3387e5b93039` | `f016ba46250c1bb4895aed14b447088852658c9ca025f2118244b0ff9a144e5b` | records `19354e7949d004af4057269f432b47b6f33392a8ceb1da376b1e2a05c64ba9c0` |
| PulpMotion native / `sm_pulpmotion_repro162760_stage2_original_matched210k_seed17_5090g3_r2_20260809` | final `877c6b1a6fc78c6bcb20d936aaddde30a1c7a2d8b9729135c3d1cdd7573a4bd0`; halfway `c03f1f5dd12e72db9969f18fd6f7bb853cf77e4f41888db4396c23c018a66d47` | train `d6af214b7c5bf396ee30ce0f84909ef95b6c8127a4e008125b2ca4a1b91d941c`; eval `b47f75f4fdefb46658a4d5ea961bc64dfd6640d73b19f109fff0c47c9fd6142c` | `8da8d60e1faf3bf02c5a2e969893dbd4c3f295f04f558b00d0fd69e77772618a` | audit `5e2b629d330192650c2f09f46631935b46a78fd0a4f4e6f437d50598861c7d8a` |

## 4A. v9+ Stage2 audited detail tables

Original §§3.11–3.19 are retained below with complete pure4053 numeric fields, run identities, artifact hashes and protocol exception boundaries. Tables use short display IDs plus canonical `sm_` aliases. For migrated historical runs, the pre-migration embedded ID/path is retained only in [[StoryMotion-folder-rename-map]] together with its old→new mapping and hash boundary. Direct-C observed-H fields are explicitly labeled and are not free-Human generation.

### Audited detail — original §3.11 v11 four-arm `105K` pure4,053 formal audit

| display ID | canonical sm_ run alias | setting | goal |
| --- | --- | --- | --- |
| C0-LAT | `v11_c0_lat_fixedh_35to105k_seed17_5090g2_r2_20260730` | v9 owner; Camera latent objective; Human frozen at `105K` | operational asymmetric mainline |
| C0-GEO | `v11_c0_geo_fixedh_35to105k_seed17_5090g3_r2_20260730` | same v9 owner and frozen Human; decoded Camera/framing geometry objective | audited objective alternate |
| C1-LAT | `v11_c1_lat_fixedh_gt64_tf64_35to105k_seed17_4090g0_r2_20260730` | C1 representation; Camera latent objective | representation/objective control |
| C1-GEO | `v11_c1_geo_fixedh_gt64_tf64_35to105k_seed17_4090g1_r2_20260730` | C1 representation; decoded Camera/framing geometry objective | representation/objective control |

每一行对应一个 experiment arm；后续 metric rows 的 display ID 与 canonical run alias 保持一一对应；alias不是平均或ensemble。

正式cross-arm audit root位于4090：

`/data/public/ripemangobox/Motion/StoryMotion/runs/legacy/eval/stage2/v11_four_arm_105k_pure4053_audit_20260730/`

四臂均评测完整Pulp pure-test `N=4,053`，ordered-ID SHA-256为`a0d7627ee827e36a229d33f9975f8417ae78b504cd5a6db1edf62cb1a9266b93`，official-input SHA-256为`6d75cbf5d22b4a9f0a39d79fa8cfb900708a4095725b7ff62e7bf11ca4d2b80f`。统一使用EMA Camera step `105K`、seed17、eval batch32、shifted-sigma explicit Euler50、Human CFG1、无Camera CFG；模式为Direct-H、Direct-C与formal sequential Human→Camera，`joint_parallel=false`。implementation composite SHA-256为`33eef1048cc19335fc25e6b8025eadc40fc5a12af88b95d62ed581bf00d83552`；evaluator SHA-256为`a14f1bc1e1257e6e1967bef44d0974f5bf037aafb6326f2043c55bacf1cd39fd`。

cross-arm `matrix_audit.json` SHA-256为`96464d35fbb69dc6befa5121153543e64b29f399d5feeb0c7a5c90d30c9927fb`；audit implementation SHA-256为`858bcdb4148d0efcf96beefd5a54b93bf33d8f3f1bf06b730a48b5a32e7f121d`。审计逐臂验证contract、non-causal、checkpoint／cache／stats／decoder、4,053个唯一ID、official input、三模式字段和artifact hash，并对全部paired geometry与decoded-Human physical字段执行10,000次matched-sample bootstrap。跨主机Direct-H replay使用显式unit-specific单样本最大值与cohort均值双阈值；同5090的C0-LAT／GEO逐字段exact，5090↔4090的最大yaw差`0.2259°`、最大root FDE差`0.00555 m`及孤立contact阈值翻转均通过相应均值守卫。

| version / run | EMA `105K` SHA-256 | pure contract SHA-256 | result SHA-256 | records SHA-256 |
| --- | --- | --- | --- | --- |
| v11 / `v11_c0_lat_fixedh_35to105k_seed17_5090g2_r2_20260730` | `b7759ea686ddc8bd9abc2db2b3a6f74421bf3f6033274863d715f58b0d66b96a` | `390d1cda9e1636460ff6cc641cb67cf08e530448b04748adab4c7b3dc4e5d832` | `d7cd9fc63139fea2c716de279e11ee009d6775da37ff49604eefa3bc3eca22da` | `00fdb6e4538b8a8864827f0237d824c6fde3e859862d6513564396c8ad064b8f` |
| v11 / `v11_c0_geo_fixedh_35to105k_seed17_5090g3_r2_20260730` | `3cd135b0105e32cab9da877926a16d712ed480648176f909ac9044c51e7670c7` | `b4a96b57a11751113a76ad2b28345c103ba7a42ad63337ef124faaef59edd24c` | `85d26a1705f0bb96af83b679ac7e7921c94115cbc22e603350deabc62e5f1ba1` | `1e08feb85f8c0e61dc0ebdf6d39b68af27e69cb5889da6b0677929710980475e` |
| v11 / `v11_c1_lat_fixedh_gt64_tf64_35to105k_seed17_4090g0_r2_20260730` | `2fcd0092348cb8aa0403f28b0e0af3f4f62c07569c68806d62ac141f45b385e8` | `1a5d8e9b6efe4da47c28c1f8cf6ffd18e36dcfdf4d3f0b10d4ee82db9f8e6044` | `adc0c95639484fd41ee6abcc29960eded70655b4191bdc0203a476eb4a8f89e3` | `a9b38100c025407f6d13bdc7666e505fb30c9f6851511975bdfa904f3ff8ec92` |
| v11 / `v11_c1_geo_fixedh_gt64_tf64_35to105k_seed17_4090g1_r2_20260730` | `1cef5404de4a334021034372358dd946a1e91b0728ddf8340888e4cfaeff236a` | `99503b531c1e4b90d0ac587d7a18a62c26ac396eb8bc70985504c79b7dd2cb3c` | `f0dddfde464719e92d9dc096c03bfa6daab4e1323cfd34420374299791ea8f5d` | `3954af44654c471c8852553197dd742e9ecb7938b911a72d2290e92d9ecfdae4` |

#### Direct-H complete semantic and paired geometry

四臂使用同一冻结Human teacher；5090两臂逐字段exact，跨4090只有受审计约束的GPU roundoff。root-aligned MPJPE只去除root translation，仍保留heading error。

| display ID / canonical run alias | N | FDTMR ↓ | TMR ↑ | HCov / density / precision / recall ↑ | R1 / R2 / R3 ↑ | global / root-aligned MPJPE ↓ m | root ADE / FDE ↓ m | yaw mean / final / unwrapped final ↓ deg |
| --- | ---: | ---: | ---: | --- | --- | --- | --- | --- |
| v11 C0-LAT / `v11_c0_lat_fixedh_35to105k_seed17_5090g2_r2_20260730` | 4,053 | 99.391 | 17.608 | 0.7158 / 0.8079 / 0.8283 / 0.6531 | 0.1559 / 0.2556 / 0.3388 | 0.842760 / 0.228751 | 0.758772 / 1.283039 | 47.239 / 66.123 / 239.357 |
| v11 C0-GEO / `v11_c0_geo_fixedh_35to105k_seed17_5090g3_r2_20260730` | 4,053 | 99.391 | 17.608 | 0.7158 / 0.8079 / 0.8283 / 0.6531 | 0.1559 / 0.2556 / 0.3388 | 0.842760 / 0.228751 | 0.758772 / 1.283039 | 47.239 / 66.123 / 239.357 |
| v11 C1-LAT / `v11_c1_lat_fixedh_gt64_tf64_35to105k_seed17_4090g0_r2_20260730` | 4,053 | 99.391 | 17.608 | 0.7158 / 0.8079 / 0.8283 / 0.6528 | 0.1562 / 0.2559 / 0.3388 | 0.842762 / 0.228751 | 0.758774 / 1.283042 | 47.239 / 66.123 / 239.356 |
| v11 C1-GEO / `v11_c1_geo_fixedh_gt64_tf64_35to105k_seed17_4090g1_r2_20260730` | 4,053 | 99.391 | 17.608 | 0.7158 / 0.8079 / 0.8283 / 0.6528 | 0.1562 / 0.2559 / 0.3388 | 0.842762 / 0.228751 | 0.758774 / 1.283042 | 47.239 / 66.123 / 239.356 |

#### Direct-C complete Camera and observed-Human geometry

Direct-C的Human列是GT-H经v9 owning decoder的重建诊断，不是自由Human生成。

| display ID / canonical run alias | FDCLaTr ↓ | CLaTr ↑ | CCov / density / precision / recall ↑ | caption P / R / F1 ↑ | Cam ADE / FDE ↓ m | rotation ↓ deg | r-FPD / Out ↓ | observed-H global / root-aligned MPJPE ↓ m |
| --- | ---: | ---: | --- | --- | --- | ---: | --- | --- |
| v11 C0-LAT / `v11_c0_lat_fixedh_35to105k_seed17_5090g2_r2_20260730` | 21.171 | 56.933 | 0.8303 / 1.0932 / 0.9156 / 0.5566 | 0.7857 / 0.7000 / 0.7372 | 1.4125 / 1.4985 | 29.922 | 0.8465 / 0.1052 | 0.125466 / 0.048796 |
| v11 C0-GEO / `v11_c0_geo_fixedh_35to105k_seed17_5090g3_r2_20260730` | 20.540 | 57.574 | 0.8236 / 1.0604 / 0.9062 / 0.5589 | 0.7900 / 0.7075 / 0.7442 | 1.3860 / 1.4711 | 29.800 | 0.8514 / 0.1017 | 0.125466 / 0.048796 |
| v11 C1-LAT / `v11_c1_lat_fixedh_gt64_tf64_35to105k_seed17_4090g0_r2_20260730` | 22.461 | 56.689 | 0.8209 / 1.0991 / 0.9127 / 0.5453 | 0.7770 / 0.6941 / 0.7293 | 1.6756 / 1.7706 | 35.250 | 1.1141 / 0.1245 | 0.125455 / 0.048795 |
| v11 C1-GEO / `v11_c1_geo_fixedh_gt64_tf64_35to105k_seed17_4090g1_r2_20260730` | 23.863 | 56.687 | 0.8083 / 1.0625 / 0.9080 / 0.5401 | 0.7782 / 0.6959 / 0.7306 | 1.6176 / 1.7137 | 33.777 | 1.1380 / 0.1243 | 0.125455 / 0.048795 |

#### Formal sequential Human→Camera complete joint system

| display ID / canonical run alias | Camera FDCLaTr ↓ / CLaTr ↑ | Camera coverage / density / precision / recall ↑ | caption F1 ↑ | r-FPD / Out ↓ | H global / root-aligned MPJPE ↓ m | Cam ADE / FDE ↓ m | Cam rotation ↓ deg |
| --- | --- | --- | ---: | --- | --- | --- | ---: |
| v11 C0-LAT / `v11_c0_lat_fixedh_35to105k_seed17_5090g2_r2_20260730` | 28.754 / 55.579 | 0.7735 / 1.0100 / 0.8949 / 0.5241 | 0.6935 | 0.5082 / 0.0773 | 0.842760 / 0.228751 | 2.9428 / 3.0422 | 71.435 |
| v11 C0-GEO / `v11_c0_geo_fixedh_35to105k_seed17_5090g3_r2_20260730` | 29.505 / 56.103 | 0.7626 / 1.0042 / 0.8939 / 0.5164 | 0.7007 | 0.5098 / 0.0768 | 0.842760 / 0.228751 | 2.9368 / 3.0395 | 71.507 |
| v11 C1-LAT / `v11_c1_lat_fixedh_gt64_tf64_35to105k_seed17_4090g0_r2_20260730` | 35.242 / 53.235 | 0.7464 / 1.0124 / 0.8863 / 0.4880 | 0.6779 | 1.2577 / 0.1384 | 0.842762 / 0.228751 | 3.0448 / 3.1537 | 72.838 |
| v11 C1-GEO / `v11_c1_geo_fixedh_gt64_tf64_35to105k_seed17_4090g1_r2_20260730` | 37.466 / 53.405 | 0.7311 / 0.9650 / 0.8732 / 0.4863 | 0.6839 | 1.2113 / 0.1349 | 0.842762 / 0.228751 | 3.0497 / 3.1511 | 72.398 |

#### Complete decoded-Human physical/kinematic diagnostics

每个cell是`mean / median / p90`。单位与[[StoryMotion-metric-computation-io]]一致；bone CV无量纲，dynamics为decoded coordinate / frameⁿ，contact为fraction。它们是no-reference heuristic diagnostics，不是calibrated physical-validity或ground penetration／floating指标。Direct-H与sequential共享同一冻结Human输出；Direct-C是observed-H reconstruction。

| display ID / canonical run alias | mode | N | bone CV ↓ | joint speed ↔ reference | joint acceleration ↔ reference | joint jerk ↔ reference |
| --- | --- | ---: | ---: | ---: | ---: | ---: |
| Dataset reference / v11 pure4053 | reference | 4,053 | 2.414e-7 / 2.194e-7 / 3.085e-7 | 0.035336 / 0.021716 / 0.080298 | 0.026611 / 0.015280 / 0.060480 | 0.041110 / 0.023375 / 0.093897 |
| v11 C0-LAT / `v11_c0_lat_fixedh_35to105k_seed17_5090g2_r2_20260730` | Direct-H = sequential Human | 4,053 | 2.280e-7 / 2.220e-7 / 2.622e-7 | 0.025358 / 0.017674 / 0.053936 | 0.023125 / 0.016563 / 0.048184 | 0.036800 / 0.026027 / 0.076142 |
| v11 C0-GEO / `v11_c0_geo_fixedh_35to105k_seed17_5090g3_r2_20260730` | Direct-H = sequential Human | 4,053 | 2.280e-7 / 2.220e-7 / 2.622e-7 | 0.025358 / 0.017674 / 0.053936 | 0.023125 / 0.016563 / 0.048184 | 0.036800 / 0.026027 / 0.076142 |
| v11 C1-LAT / `v11_c1_lat_fixedh_gt64_tf64_35to105k_seed17_4090g0_r2_20260730` | Direct-H = sequential Human | 4,053 | 2.279e-7 / 2.220e-7 / 2.626e-7 | 0.025358 / 0.017675 / 0.053936 | 0.023125 / 0.016568 / 0.048186 | 0.036800 / 0.026036 / 0.076142 |
| v11 C1-GEO / `v11_c1_geo_fixedh_gt64_tf64_35to105k_seed17_4090g1_r2_20260730` | Direct-H = sequential Human | 4,053 | 2.279e-7 / 2.220e-7 / 2.626e-7 | 0.025358 / 0.017675 / 0.053936 | 0.023125 / 0.016568 / 0.048186 | 0.036800 / 0.026036 / 0.076142 |
| v11 C0-LAT / `v11_c0_lat_fixedh_35to105k_seed17_5090g2_r2_20260730` | Direct-C observed-H reconstruction | 4,053 | 2.468e-7 / 2.253e-7 / 3.127e-7 | 0.037159 / 0.023331 / 0.083145 | 0.030219 / 0.018391 / 0.066288 | 0.046381 / 0.027816 / 0.099293 |
| v11 C0-GEO / `v11_c0_geo_fixedh_35to105k_seed17_5090g3_r2_20260730` | Direct-C observed-H reconstruction | 4,053 | 2.468e-7 / 2.253e-7 / 3.127e-7 | 0.037159 / 0.023331 / 0.083145 | 0.030219 / 0.018391 / 0.066288 | 0.046381 / 0.027816 / 0.099293 |
| v11 C1-LAT / `v11_c1_lat_fixedh_gt64_tf64_35to105k_seed17_4090g0_r2_20260730` | Direct-C observed-H reconstruction | 4,053 | 2.467e-7 / 2.250e-7 / 3.131e-7 | 0.037159 / 0.023330 / 0.083141 | 0.030219 / 0.018382 / 0.066291 | 0.046381 / 0.027812 / 0.099302 |
| v11 C1-GEO / `v11_c1_geo_fixedh_gt64_tf64_35to105k_seed17_4090g1_r2_20260730` | Direct-C observed-H reconstruction | 4,053 | 2.467e-7 / 2.250e-7 / 3.131e-7 | 0.037159 / 0.023330 / 0.083141 | 0.030219 / 0.018382 / 0.066291 | 0.046381 / 0.027812 / 0.099302 |

| display ID / canonical run alias | mode | N | root speed ↔ reference | root acceleration ↔ reference | root jerk ↔ reference | contact heuristic ↔ reference | foot skate heuristic ↓ |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Dataset reference / v11 pure4053 | reference | 4,053 | 0.029456 / 0.016709 / 0.067934 | 0.017055 / 0.009513 / 0.039636 | 0.023314 / 0.013070 / 0.053262 | 0.489381 / 0.425000 / 1.000000 | 0.039985 / 0.021858 / 0.080741 |
| v11 C0-LAT / `v11_c0_lat_fixedh_35to105k_seed17_5090g2_r2_20260730` | Direct-H = sequential Human | 4,053 | 0.017803 / 0.010156 / 0.041565 | 0.011937 / 0.007418 / 0.026801 | 0.016892 / 0.010376 / 0.037602 | 0.596160 / 0.595745 / 1.000000 | 0.030608 / 0.019470 / 0.063224 |
| v11 C0-GEO / `v11_c0_geo_fixedh_35to105k_seed17_5090g3_r2_20260730` | Direct-H = sequential Human | 4,053 | 0.017803 / 0.010156 / 0.041565 | 0.011937 / 0.007418 / 0.026801 | 0.016892 / 0.010376 / 0.037602 | 0.596160 / 0.595745 / 1.000000 | 0.030608 / 0.019470 / 0.063224 |
| v11 C1-LAT / `v11_c1_lat_fixedh_gt64_tf64_35to105k_seed17_4090g0_r2_20260730` | Direct-H = sequential Human | 4,053 | 0.017803 / 0.010157 / 0.041564 | 0.011937 / 0.007417 / 0.026799 | 0.016892 / 0.010380 / 0.037599 | 0.596170 / 0.595745 / 1.000000 | 0.030611 / 0.019465 / 0.063216 |
| v11 C1-GEO / `v11_c1_geo_fixedh_gt64_tf64_35to105k_seed17_4090g1_r2_20260730` | Direct-H = sequential Human | 4,053 | 0.017803 / 0.010157 / 0.041564 | 0.011937 / 0.007417 / 0.026799 | 0.016892 / 0.010380 / 0.037599 | 0.596170 / 0.595745 / 1.000000 | 0.030611 / 0.019465 / 0.063216 |
| v11 C0-LAT / `v11_c0_lat_fixedh_35to105k_seed17_5090g2_r2_20260730` | Direct-C observed-H reconstruction | 4,053 | 0.030292 / 0.017515 / 0.069143 | 0.019720 / 0.011575 / 0.043850 | 0.027753 / 0.016435 / 0.061084 | 0.491982 / 0.437500 / 1.000000 | 0.041858 / 0.024370 / 0.085571 |
| v11 C0-GEO / `v11_c0_geo_fixedh_35to105k_seed17_5090g3_r2_20260730` | Direct-C observed-H reconstruction | 4,053 | 0.030292 / 0.017515 / 0.069143 | 0.019720 / 0.011575 / 0.043850 | 0.027753 / 0.016435 / 0.061084 | 0.491982 / 0.437500 / 1.000000 | 0.041858 / 0.024370 / 0.085571 |
| v11 C1-LAT / `v11_c1_lat_fixedh_gt64_tf64_35to105k_seed17_4090g0_r2_20260730` | Direct-C observed-H reconstruction | 4,053 | 0.030292 / 0.017515 / 0.069143 | 0.019720 / 0.011576 / 0.043855 | 0.027753 / 0.016443 / 0.061077 | 0.491997 / 0.437500 / 1.000000 | 0.041857 / 0.024370 / 0.085574 |
| v11 C1-GEO / `v11_c1_geo_fixedh_gt64_tf64_35to105k_seed17_4090g1_r2_20260730` | Direct-C observed-H reconstruction | 4,053 | 0.030292 / 0.017515 / 0.069143 | 0.019720 / 0.011576 / 0.043855 | 0.027753 / 0.016443 / 0.061077 | 0.491997 / 0.437500 / 1.000000 | 0.041857 / 0.024370 / 0.085574 |

#### Four-arm paired geometry bootstrap

10,000次resample，seed `260730`，unit为matched sample；差值均为前者减后者。

| version / comparison | mode | Δ Camera ADE ↓ m（95% CI; A−B） | Δ Camera FDE ↓ m（95% CI; A−B） | Δ Camera rotation ↓ deg（95% CI; A−B） |
| --- | --- | --- | --- | --- |
| v11 / `v11_c0_geo_fixedh_35to105k_seed17_5090g3_r2_20260730` − `v11_c0_lat_fixedh_35to105k_seed17_5090g2_r2_20260730` | Direct-C | -0.0265 [-0.0651, 0.0121] | -0.0274 [-0.0667, 0.0113] | -0.1218 [-1.0660, 0.8289] |
| v11 / `v11_c0_geo_fixedh_35to105k_seed17_5090g3_r2_20260730` − `v11_c0_lat_fixedh_35to105k_seed17_5090g2_r2_20260730` | sequential | -0.0060 [-0.0362, 0.0231] | -0.0027 [-0.0333, 0.0271] | +0.0725 [-0.9431, 1.0655] |
| v11 / `v11_c1_geo_fixedh_gt64_tf64_35to105k_seed17_4090g1_r2_20260730` − `v11_c1_lat_fixedh_gt64_tf64_35to105k_seed17_4090g0_r2_20260730` | Direct-C | -0.0580 [-0.0965, -0.0203] | -0.0569 [-0.0960, -0.0189] | -1.4732 [-2.3643, -0.5822] |
| v11 / `v11_c1_geo_fixedh_gt64_tf64_35to105k_seed17_4090g1_r2_20260730` − `v11_c1_lat_fixedh_gt64_tf64_35to105k_seed17_4090g0_r2_20260730` | sequential | +0.0049 [-0.0244, 0.0347] | -0.0026 [-0.0328, 0.0280] | -0.4395 [-1.2353, 0.3416] |
| v11 / `v11_c1_lat_fixedh_gt64_tf64_35to105k_seed17_4090g0_r2_20260730` − `v11_c0_lat_fixedh_35to105k_seed17_5090g2_r2_20260730` | Direct-C | +0.2631 [0.2208, 0.3054] | +0.2721 [0.2285, 0.3156] | +5.3279 [4.2681, 6.3547] |
| v11 / `v11_c1_lat_fixedh_gt64_tf64_35to105k_seed17_4090g0_r2_20260730` − `v11_c0_lat_fixedh_35to105k_seed17_5090g2_r2_20260730` | sequential | +0.1020 [0.0433, 0.1618] | +0.1115 [0.0522, 0.1718] | +1.4030 [-0.2920, 3.0632] |
| v11 / `v11_c1_geo_fixedh_gt64_tf64_35to105k_seed17_4090g1_r2_20260730` − `v11_c0_geo_fixedh_35to105k_seed17_5090g3_r2_20260730` | Direct-C | +0.2316 [0.1936, 0.2705] | +0.2426 [0.2037, 0.2823] | +3.9765 [2.9520, 4.9841] |
| v11 / `v11_c1_geo_fixedh_gt64_tf64_35to105k_seed17_4090g1_r2_20260730` − `v11_c0_geo_fixedh_35to105k_seed17_5090g3_r2_20260730` | sequential | +0.1129 [0.0552, 0.1713] | +0.1116 [0.0534, 0.1709] | +0.8910 [-0.7611, 2.5541] |

#### Four-arm distributional／semantic and decoded-Human delta supplement

下表中的 distributional／semantic 项是对应 official `results.json` 的 cohort arithmetic
delta（前者减后者），没有 per-sample semantic unit，故不提供 semantic CI。physical 项来自
同一 matrix audit 的 nested decoded-Human records；`↔` 是 no-reference diagnostic，不能按
正负号宣称优劣。geometry CI 与 hash/provenance 仍以上表及其 audit artifact 为准。

| comparison | mode | distributional／semantic aggregate Δ (A−B; no CI) | decoded-Human physical／kinematic mean Δ [95% CI] (diagnostic-only) |
| --- | --- | --- | --- |
| C0-GEO − C0-LAT | Direct-C | `CLaTr↑ +0.640221; FDCLaTr↓ −0.631561; cov↑ −0.006660; dens↑ −0.032725; prec↑ −0.009371; rec↑ +0.002231; R1↑ +0.001480; R2↑ +0.006415; R3↑ +0.010116; MM↓ −0.160486; caption P/R/F1↑ +0.004275/+0.007459/+0.007017; r-FPD↓ +0.004919; Out↓ −0.003503` | all 9 fields `0 [0, 0]` |
| C0-GEO − C0-LAT | sequential Human→Camera | `CLaTr↑ +0.524597; FDCLaTr↓ +0.751535; cov↑ −0.010863; dens↑ −0.005778; prec↑ −0.001002; rec↑ −0.007658; R1↑ −0.001727; R2↑ +0.001974; R3↑ +0.001974; MM↓ −0.131036; caption P/R/F1↑ +0.009501/+0.006522/+0.007161; r-FPD↓ +0.001553; Out↓ −0.000490` | all 9 fields `0 [0, 0]` |
| C1-GEO − C1-LAT | Direct-C | `CLaTr↑ −0.002304; FDCLaTr↓ +1.401524; cov↑ −0.012598; dens↑ −0.036601; prec↑ −0.004678; rec↑ −0.005178; R1↑ +0.003208; R2↑ −0.003454; R3↑ −0.001727; MM↓ −0.004053; caption P/R/F1↑ +0.001231/+0.001800/+0.001265; r-FPD↓ +0.023953; Out↓ −0.000225` | all 9 fields `0 [0, 0]` |
| C1-GEO − C1-LAT | sequential Human→Camera | `CLaTr↑ +0.170410; FDCLaTr↓ +2.224155; cov↑ −0.015303; dens↑ −0.047447; prec↑ −0.013078; rec↑ −0.001736; R1↑ −0.004194; R2↑ +0.003701; R3↑ +0.009623; MM↓ −0.039469; caption P/R/F1↑ +0.004385/+0.005548/+0.006042; r-FPD↓ −0.046390; Out↓ −0.003498` | all 9 fields `0 [0, 0]` |
| C1-LAT − C0-LAT | Direct-C | `CLaTr↑ −0.244499; FDCLaTr↓ +1.290079; cov↑ −0.009372; dens↑ +0.005914; prec↑ −0.002963; rec↑ −0.011346; R1↑ −0.006908; R2↑ −0.004194; R3↑ −0.001974; MM↓ +0.100048; caption P/R/F1↑ −0.008665/−0.005910/−0.007823; r-FPD↓ +0.267546; Out↓ +0.019362` | `bone-CV↔ −1.789e−10 [−4.562e−10,+9.314e−11]; joint speed↔ −2.451e−08 [−9.450e−08,+4.512e−08]; joint accel↔ −9.693e−08 [−2.635e−07,+6.411e−08]; joint jerk↔ −1.304e−07 [−4.676e−07,+2.052e−07]; root speed↔ −1.049e−08 [−5.878e−08,+3.820e−08]; root accel↔ −2.086e−08 [−1.582e−07,+1.185e−07]; root jerk↔ −6.423e−08 [−3.781e−07,+2.505e−07]; contact↔ +1.486e−05 [−2.097e−05,+5.957e−05]; skate↔ −1.049e−06 [−3.555e−06,+1.364e−06]` |
| C1-LAT − C0-LAT | sequential Human→Camera | `TMR↑ −0.000055; FDTMR↓ +0.000023; H cov↑ +0.000001; H dens↑ +0.000082; H prec↑ 0; H rec↑ −0.000247; H R1↑ +0.000247; H R2↑ +0.000247; H R3↑ 0; H MM↓ +0.000062; CLaTr↑ −2.344086; FDCLaTr↓ +6.488459; C cov↑ −0.027138; C dens↑ +0.002447; C prec↑ −0.008647; C rec↑ −0.036032; C R1↑ +0.005428; C R2↑ −0.008636; C R3↑ −0.016531; C MM↓ +0.668083; caption P/R/F1↑ −0.006386/−0.031101/−0.015616; r-FPD↓ +0.749500; Out↓ +0.061146` | `bone-CV↔ −1.138e−10 [−3.498e−10,+1.248e−10]; joint speed↔ +4.834e−09 [−5.261e−08,+6.170e−08]; joint accel↔ +5.698e−08 [−7.109e−08,+1.829e−07]; joint jerk↔ +6.747e−08 [−2.055e−07,+3.377e−07]; root speed↔ +1.216e−08 [−3.668e−08,+5.949e−08]; root accel↔ +5.811e−08 [−7.430e−08,+1.863e−07]; root jerk↔ +6.324e−08 [−2.362e−07,+3.578e−07]; contact↔ +9.939e−06 [−1.270e−05,+3.320e−05]; skate↔ +2.837e−06 [−3.949e−07,+6.334e−06]` |
| C1-GEO − C0-GEO | Direct-C | `CLaTr↑ −0.887024; FDCLaTr↓ +3.323164; cov↑ −0.015310; dens↑ +0.002038; prec↑ +0.001729; rec↑ −0.018755; R1↑ −0.005181; R2↑ −0.014064; R3↑ −0.013817; MM↓ +0.256481; caption P/R/F1↑ −0.011710/−0.011569/−0.013575; r-FPD↓ +0.286581; Out↓ +0.022640` | `bone-CV↔ −1.789e−10 [−4.571e−10,+1.028e−10]; joint speed↔ −2.451e−08 [−9.506e−08,+4.601e−08]; joint accel↔ −9.693e−08 [−2.645e−07,+6.862e−08]; joint jerk↔ −1.304e−07 [−4.702e−07,+2.097e−07]; root speed↔ −1.049e−08 [−6.027e−08,+3.836e−08]; root accel↔ −2.086e−08 [−1.649e−07,+1.176e−07]; root jerk↔ −6.423e−08 [−3.808e−07,+2.475e−07]; contact↔ +1.486e−05 [−2.129e−05,+5.921e−05]; skate↔ −1.049e−06 [−3.583e−06,+1.353e−06]` |
| C1-GEO − C0-GEO | sequential Human→Camera | `TMR↑ −0.000055; FDTMR↓ +0.000023; H cov↑ +0.000001; H dens↑ +0.000082; H prec↑ 0; H rec↑ −0.000247; H R1↑ +0.000247; H R2↑ +0.000247; H R3↑ 0; H MM↓ +0.000062; CLaTr↑ −2.698273; FDCLaTr↓ +7.961079; C cov↑ −0.031578; C dens↑ −0.039222; C prec↑ −0.020722; C rec↑ −0.030111; C R1↑ +0.002961; C R2↑ −0.006908; C R3↑ −0.008882; C MM↓ +0.759650; caption P/R/F1↑ −0.011502/−0.032075/−0.016735; r-FPD↓ +0.701558; Out↓ +0.058138` | `bone-CV↔ −1.138e−10 [−3.500e−10,+1.276e−10]; joint speed↔ +4.834e−09 [−5.163e−08,+5.973e−08]; joint accel↔ +5.698e−08 [−6.999e−08,+1.848e−07]; joint jerk↔ +6.747e−08 [−2.049e−07,+3.361e−07]; root speed↔ +1.216e−08 [−3.607e−08,+6.047e−08]; root accel↔ +5.811e−08 [−7.411e−08,+1.919e−07]; root jerk↔ +6.324e−08 [−2.341e−07,+3.620e−07]; contact↔ +9.939e−06 [−1.277e−05,+3.302e−05]; skate↔ +2.837e−06 [−3.390e−07,+6.413e−06]` |

#### Mainline competition boundary

C0-LAT/C0-GEO, HT controls and representation/factorization controls are compared only within their declared pure4053 protocol. The former C3-25 and v9 short-cohort rows are not active numeric evidence; their complete pre-v9 or non-full provenance is routed by the archive index above. Cross-system capability/protocol slots are defined in [[StoryMotion-metric-computation-io#7. Competition protocol slots]].

### Audited detail — original §3.13 v11 Human-text Camera fresh `105K` pure4,053 formal audit

| display ID | canonical sm_ run alias | setting | goal |
| --- | --- | --- | --- |
| C0-LAT | `v11_c0_lat_fixedh_35to105k_seed17_5090g2_r2_20260730` | frozen Human; latent Camera objective | operational mainline context |
| C0-GEO | `v11_c0_geo_fixedh_35to105k_seed17_5090g3_r2_20260730` | frozen Human; decoded Camera/framing geometry objective | matched no-Human-text parent |
| HT-FILM | `v11_ht_film_fresh105k_seed17_4090g0q_r2_20260801` | pooled scale/shift Human observation injected into Camera | test pooled Human-text conditioning |
| HT-HX | `v11_ht_hx_fresh105k_seed17_4090g1_r2_20260801` | temporal Human-token cross-attention | test token-level Human-text conditioning |
| HT-DR | `v11_ht_dr_fresh105k_seed17_4090g0_r2_20260801` | direct Camera-velocity residual from Human observation | test velocity-residual conditioning |

每一行是一个独立 experiment arm；C0-LAT/C0-GEO 是上下文或 parent，不与三个 HT arm 合并成一行。

本节比较exact matched C0-GEO与三种Human-text Camera注入设计。三条处理臂都从与
C0-GEO相同的Camera初始状态fresh训练完整Camera分支与对应Human-text模块到optimizer
step `105K`；四臂共享Pulp factual训练流、batch顺序、噪声／dropout trace、GEO目标、
Stage1、owning decoder、冻结Human teacher、seed17与EMA合同。正式评测统一使用
pure-test `N=4,053`、ordered-ID SHA256
`a0d7627ee827e36a229d33f9975f8417ae78b504cd5a6db1edf62cb1a9266b93`、official-input
SHA256 `6d75cbf5d22b4a9f0a39d79fa8cfb900708a4095725b7ff62e7bf11ca4d2b80f`与Euler50；
模式为Direct-H、Direct-C与formal sequential Human→Camera，`joint_parallel=false`。

| version / run | role | EMA `105K` SHA256 | result SHA256 | records SHA256 |
| --- | --- | --- | --- | --- |
| v11 / `v11_c0_lat_fixedh_35to105k_seed17_5090g2_r2_20260730` | operational mainline context；非GEO-objective matched baseline | `b7759ea686ddc8bd9abc2db2b3a6f74421bf3f6033274863d715f58b0d66b96a` | `d7cd9fc63139fea2c716de279e11ee009d6775da37ff49604eefa3bc3eca22da` | `00fdb6e4538b8a8864827f0237d824c6fde3e859862d6513564396c8ad064b8f` |
| v11 / `v11_c0_geo_fixedh_35to105k_seed17_5090g3_r2_20260730` | exact无Human-text baseline | `3cd135b0105e32cab9da877926a16d712ed480648176f909ac9044c51e7670c7` | `85d26a1705f0bb96af83b679ac7e7921c94115cbc22e603350deabc62e5f1ba1` | `1e08feb85f8c0e61dc0ebdf6d39b68af27e69cb5889da6b0677929710980475e` |
| v11 / `v11_ht_film_fresh105k_seed17_4090g0q_r2_20260801` | pooled scale／shift Human observation | `750c8f394a8e8eedd363691ee588d4c203fcb58ee0b8ac5704fd6cc52395f4bf` | `697a9930d6f784c74e36e5ea2547e289e72be48eb7cc94cb2365ff8d1a0e5bb8` | `3faec2c4b722baa1980a6541c45dc204790df8dae6e71ff53d63b7ccf4a9706a` |
| v11 / `v11_ht_hx_fresh105k_seed17_4090g1_r2_20260801` | temporal Human-token cross-attention | `efc44816b31fe497128c3418d6f742925ce31e5ce09b488f46a5d165f3126489` | `5a6d933ce6768c7116b356275471bc5fc0062f41642018b1bb3f9ecc1cbf7f14` | `2b69b44510f160fc3069e0d3c10e0b3849ae3f6d96c2bfc128e7346713e680dc` |
| v11 / `v11_ht_dr_fresh105k_seed17_4090g0_r2_20260801` | direct Camera-velocity residual | `d817b5cb5a635972054405f1bb6ae8dfe15ae1b4036ed9a8536d57ed2c585a77` | `3416b84c064116775b782402f3cf1d5544bf0fb55384fa23bf80d42aeb64852f` | `57dee6f9362037034aa8d361a03e2d85fefa77b2d73960c4829371d87caef9f9` |

#### Direct-H frozen-owner replay

| display ID / canonical run alias | FDTMR ↓ | TMR ↑ | coverage ↑ | root-aligned MPJPE ↓ m | global MPJPE ↓ m | root ADE / FDE ↓ m | yaw mean ↓ deg |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| v11 / `v11_c0_lat_fixedh_35to105k_seed17_5090g2_r2_20260730` | 99.391 | 17.608 | 0.7158 | 0.228751 | 0.842760 | 0.758772 / 1.283039 | 47.239 |
| v11 / `v11_c0_geo_fixedh_35to105k_seed17_5090g3_r2_20260730` | 99.391 | 17.608 | 0.7158 | 0.228751 | 0.842760 | 0.758772 / 1.283039 | 47.239 |
| v11 / `v11_ht_film_fresh105k_seed17_4090g0q_r2_20260801` | 99.391 | 17.608 | 0.7158 | 0.228751 | 0.842762 | 0.758774 / 1.283042 | 47.239 |
| v11 / `v11_ht_hx_fresh105k_seed17_4090g1_r2_20260801` | 99.391 | 17.608 | 0.7158 | 0.228751 | 0.842762 | 0.758774 / 1.283042 | 47.239 |
| v11 / `v11_ht_dr_fresh105k_seed17_4090g0_r2_20260801` | 99.391 | 17.608 | 0.7158 | 0.228751 | 0.842762 | 0.758774 / 1.283042 | 47.239 |

三条处理臂的Direct-H逐样本replay都通过预注册的unit-specific tolerance；差异只来自
跨主机GPU kernel roundoff与少量contact阈值翻转。root-aligned MPJPE仅移除root
translation而保留heading，不能解释成local-pose error。

#### Direct-C observed-Human Camera

| display ID / canonical run alias | FDCLaTr ↓ | CLaTr ↑ | coverage ↑ | caption F1 ↑ | r-FPD ↓ | Out ↓ | Camera ADE / FDE ↓ m | rotation ↓ deg |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| v11 / `v11_c0_lat_fixedh_35to105k_seed17_5090g2_r2_20260730` | 21.171 | 56.933 | 0.8303 | 0.7372 | 0.8465 | 0.1052 | 1.412472 / 1.498528 | 29.922 |
| v11 / `v11_c0_geo_fixedh_35to105k_seed17_5090g3_r2_20260730` | 20.540 | 57.574 | 0.8236 | 0.7442 | 0.8514 | 0.1017 | 1.385987 / 1.471145 | 29.800 |
| v11 / `v11_ht_film_fresh105k_seed17_4090g0q_r2_20260801` | 19.353 | 57.252 | 0.8275 | 0.7514 | 0.7930 | 0.1000 | 1.354679 / 1.446069 | 28.489 |
| v11 / `v11_ht_hx_fresh105k_seed17_4090g1_r2_20260801` | 19.399 | 57.419 | 0.8372 | 0.7468 | 0.7846 | 0.0988 | 1.346459 / 1.438749 | 28.014 |
| v11 / `v11_ht_dr_fresh105k_seed17_4090g0_r2_20260801` | 17.586 | 58.840 | 0.8377 | 0.7711 | 0.8699 | 0.1075 | 1.414115 / 1.501362 | 29.572 |

#### Formal sequential Human→Camera

| display ID / canonical run alias | FDCLaTr ↓ | CLaTr ↑ | caption F1 ↑ | FDTMR ↓ / TMR ↑ | r-FPD ↓ / Out ↓ | Human global / root ADE ↓ m | Camera ADE / FDE ↓ m | rotation ↓ deg |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| v11 / `v11_c0_lat_fixedh_35to105k_seed17_5090g2_r2_20260730` | 28.754 | 55.579 | 0.6935 | 99.391 / 17.608 | 0.5082 / 0.0773 | 0.842760 / 0.758772 | 2.942785 / 3.042185 | 71.435 |
| v11 / `v11_c0_geo_fixedh_35to105k_seed17_5090g3_r2_20260730` | 29.505 | 56.103 | 0.7007 | 99.391 / 17.608 | 0.5098 / 0.0768 | 0.842760 / 0.758772 | 2.936792 / 3.039527 | 71.507 |
| v11 / `v11_ht_film_fresh105k_seed17_4090g0q_r2_20260801` | 32.106 | 56.089 | 0.7128 | 99.391 / 17.608 | 0.4794 / 0.0729 | 0.842762 / 0.758774 | 2.774063 / 2.874111 | 69.890 |
| v11 / `v11_ht_hx_fresh105k_seed17_4090g1_r2_20260801` | 43.644 | 54.055 | 0.6810 | 99.391 / 17.608 | 0.5129 / 0.0725 | 0.842762 / 0.758774 | 2.704729 / 2.805182 | 70.217 |
| v11 / `v11_ht_dr_fresh105k_seed17_4090g0_r2_20260801` | 24.564 | 58.145 | 0.7436 | 99.391 / 17.608 | 0.4943 / 0.0781 | 0.842762 / 0.758774 | 2.945997 / 3.047307 | 71.162 |

#### Decoded-Human physical and kinematic diagnostics

| mode | display ID / canonical run alias | Bone CV ↓ | Joint speed ↔ reference | Joint accel ↔ reference | Joint jerk ↔ reference | Root speed ↔ reference | Root accel ↔ reference | Root jerk ↔ reference | Contact† ↔ reference | Skate† ↓ |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Direct-H | v11 / `v11_c0_lat_fixedh_35to105k_seed17_5090g2_r2_20260730` | 2.28027e-07 | 0.025358 | 0.0231249 | 0.0368002 | 0.0178026 | 0.0119371 | 0.0168918 | 0.59616 | 0.030608 |
| Direct-H | v11 / `v11_c0_geo_fixedh_35to105k_seed17_5090g3_r2_20260730` | 2.28027e-07 | 0.025358 | 0.0231249 | 0.0368002 | 0.0178026 | 0.0119371 | 0.0168918 | 0.59616 | 0.030608 |
| Direct-H | v11 / `v11_ht_film_fresh105k_seed17_4090g0q_r2_20260801` | 2.27913e-07 | 0.025358 | 0.0231250 | 0.0368003 | 0.0178026 | 0.0119372 | 0.0168918 | 0.59617 | 0.0306109 |
| Direct-H | v11 / `v11_ht_hx_fresh105k_seed17_4090g1_r2_20260801` | 2.27913e-07 | 0.025358 | 0.0231250 | 0.0368003 | 0.0178026 | 0.0119372 | 0.0168918 | 0.59617 | 0.0306109 |
| Direct-H | v11 / `v11_ht_dr_fresh105k_seed17_4090g0_r2_20260801` | 2.27913e-07 | 0.025358 | 0.0231250 | 0.0368003 | 0.0178026 | 0.0119372 | 0.0168918 | 0.59617 | 0.0306109 |
| Direct-C | v11 / `v11_c0_lat_fixedh_35to105k_seed17_5090g2_r2_20260730` | 2.46848e-07 | 0.0371589 | 0.0302190 | 0.0463807 | 0.0302918 | 0.0197196 | 0.0277530 | 0.491982 | 0.0418580 |
| Direct-C | v11 / `v11_c0_geo_fixedh_35to105k_seed17_5090g3_r2_20260730` | 2.46848e-07 | 0.0371589 | 0.0302190 | 0.0463807 | 0.0302918 | 0.0197196 | 0.0277530 | 0.491982 | 0.0418580 |
| Direct-C | v11 / `v11_ht_film_fresh105k_seed17_4090g0q_r2_20260801` | 2.46669e-07 | 0.0371589 | 0.0302189 | 0.0463805 | 0.0302918 | 0.0197196 | 0.0277529 | 0.491997 | 0.0418569 |
| Direct-C | v11 / `v11_ht_hx_fresh105k_seed17_4090g1_r2_20260801` | 2.46669e-07 | 0.0371589 | 0.0302189 | 0.0463805 | 0.0302918 | 0.0197196 | 0.0277529 | 0.491997 | 0.0418569 |
| Direct-C | v11 / `v11_ht_dr_fresh105k_seed17_4090g0_r2_20260801` | 2.46669e-07 | 0.0371589 | 0.0302189 | 0.0463805 | 0.0302918 | 0.0197196 | 0.0277529 | 0.491997 | 0.0418569 |
| Sequential | v11 / `v11_c0_lat_fixedh_35to105k_seed17_5090g2_r2_20260730` | 2.28027e-07 | 0.025358 | 0.0231249 | 0.0368002 | 0.0178026 | 0.0119371 | 0.0168918 | 0.59616 | 0.030608 |
| Sequential | v11 / `v11_c0_geo_fixedh_35to105k_seed17_5090g3_r2_20260730` | 2.28027e-07 | 0.025358 | 0.0231249 | 0.0368002 | 0.0178026 | 0.0119371 | 0.0168918 | 0.59616 | 0.030608 |
| Sequential | v11 / `v11_ht_film_fresh105k_seed17_4090g0q_r2_20260801` | 2.27913e-07 | 0.025358 | 0.0231250 | 0.0368003 | 0.0178026 | 0.0119372 | 0.0168918 | 0.59617 | 0.0306109 |
| Sequential | v11 / `v11_ht_hx_fresh105k_seed17_4090g1_r2_20260801` | 2.27913e-07 | 0.025358 | 0.0231250 | 0.0368003 | 0.0178026 | 0.0119372 | 0.0168918 | 0.59617 | 0.0306109 |
| Sequential | v11 / `v11_ht_dr_fresh105k_seed17_4090g0_r2_20260801` | 2.27913e-07 | 0.025358 | 0.0231250 | 0.0368003 | 0.0178026 | 0.0119372 | 0.0168918 | 0.59617 | 0.0306109 |
| factual reference | Pulp / pure-test-4,053 | 2.41667e-07 | 0.0353356 | 0.0266111 | 0.0411097 | 0.0294563 | 0.0170548 | 0.0233141 | 0.489381 | 0.0399853 |

† Contact与skate是未校准heuristic，不是physical-validity pass。四臂的Human来源相同，
因此本表只验证冻结Human owner与解码链没有被Camera设计改变，不用于给Human-text设计排名。

#### Matched Camera geometry bootstrap against C0-GEO

下表是处理臂减C0-GEO，单位依次为米／米／度；负值表示误差降低。每个cell给出
`mean delta [95% CI]`，重采样单位为相同sample，seed `260802`，共`10,000`次。

| version / run comparison | mode | Camera ADE ↓ delta (A−B) | Camera FDE ↓ delta (A−B) | rotation ↓ delta (A−B) |
| --- | --- | ---: | ---: | ---: |
| v11 / `v11_c0_lat_fixedh_35to105k_seed17_5090g2_r2_20260730` − `v11_c0_geo_fixedh_35to105k_seed17_5090g3_r2_20260730` | Direct-C | +0.02648 [-0.01245, +0.06529] | +0.02738 [-0.01240, +0.06681] | +0.12178 [-0.80951, +1.08853] |
| v11 / `v11_c0_lat_fixedh_35to105k_seed17_5090g2_r2_20260730` − `v11_c0_geo_fixedh_35to105k_seed17_5090g3_r2_20260730` | sequential | +0.00600 [-0.02330, +0.03600] | +0.00266 [-0.02676, +0.03219] | -0.07250 [-1.08543, +0.91249] |
| v11 / `v11_ht_film_fresh105k_seed17_4090g0q_r2_20260801` − `v11_c0_geo_fixedh_35to105k_seed17_5090g3_r2_20260730` | Direct-C | -0.03131 [-0.06971, +0.00596] | -0.02508 [-0.06355, +0.01295] | -1.31122 [-2.26411, -0.37093] |
| v11 / `v11_ht_film_fresh105k_seed17_4090g0q_r2_20260801` − `v11_c0_geo_fixedh_35to105k_seed17_5090g3_r2_20260730` | sequential | -0.16273 [-0.19543, -0.13000] | -0.16542 [-0.19839, -0.13229] | -1.61680 [-2.64821, -0.59007] |
| v11 / `v11_ht_hx_fresh105k_seed17_4090g1_r2_20260801` − `v11_c0_geo_fixedh_35to105k_seed17_5090g3_r2_20260730` | Direct-C | -0.03953 [-0.07561, -0.00189] | -0.03240 [-0.06981, +0.00569] | -1.78586 [-2.73627, -0.81166] |
| v11 / `v11_ht_hx_fresh105k_seed17_4090g1_r2_20260801` − `v11_c0_geo_fixedh_35to105k_seed17_5090g3_r2_20260730` | sequential | -0.23206 [-0.26523, -0.19831] | -0.23435 [-0.26847, -0.19979] | -1.28961 [-2.39623, -0.18125] |
| v11 / `v11_ht_dr_fresh105k_seed17_4090g0_r2_20260801` − `v11_c0_geo_fixedh_35to105k_seed17_5090g3_r2_20260730` | Direct-C | +0.02813 [-0.00824, +0.06345] | +0.03022 [-0.00732, +0.06676] | -0.22866 [-1.16223, +0.68281] |
| v11 / `v11_ht_dr_fresh105k_seed17_4090g0_r2_20260801` − `v11_c0_geo_fixedh_35to105k_seed17_5090g3_r2_20260730` | sequential | +0.00920 [-0.02168, +0.03949] | +0.00778 [-0.02402, +0.03946] | -0.34554 [-1.34676, +0.62894] |

审计SHA256为`3f410e70f870dc9b0c012bcc8e69a09f9c0823b3606f0d5e1776e129f87e12be`；
audit implementation为`a43b51ce7c322e0076a34b2aff7abf579d60b3cb3a0d9faef0a2811f2a2010bf`；
fresh evaluator为`306e5d3e503195d9273521a26b29fec41ca553fa95645bcf48d77d8cf816c632`。
固定8例覆盖两种Camera模式与Pulp／C0-GEO／三个处理臂共`80`个cell，visual manifest
SHA256为`eeeff66c6e91d998e88213e582778a9e2c0a2a8125b2cf3dad67f0a997914edc`。C0-LAT只补入
同协议numeric context与现有paired bootstrap，不冒充该GEO-parent visual panel成员。

#### HT − C0-GEO distributional／semantic and decoded-Human delta supplement

distributional／semantic 项为 official aggregate 的算术差值（处理臂减 C0-GEO），没有
per-sample semantic/framing unit，故 CI unavailable。physical 项来自同一 `matrix_audit.json`
的逐样本 decoded-Human records，给出 matched bootstrap CI；`↔` 仍是 no-reference diagnostic，
不赋予单调质量方向。

| comparison | mode | distributional／semantic aggregate Δ (A−B; no CI) | decoded-Human physical／kinematic mean Δ [95% CI] (diagnostic-only) |
| --- | --- | --- | --- |
| HT-FILM − C0-GEO | Direct-C | `CLaTr↑ −0.321911; FDCLaTr↓ −1.186733; cov↑ +0.003945; dens↑ +0.035354; prec↑ +0.002464; rec↑ +0.011588; R1↑ −0.009622; R2↑ −0.010363; R3↑ −0.009376; MM↓ +0.057609; caption P/R/F1↑ +0.005518/+0.008076/+0.007228; r-FPD↓ −0.058473; Out↓ −0.001639` | `bone-CV↔ −1.789e−10 [−4.563e−10,+9.295e−11]; joint speed↔ −2.451e−08 [−9.694e−08,+4.608e−08]; joint accel↔ −9.693e−08 [−2.653e−07,+6.699e−08]; joint jerk↔ −1.304e−07 [−4.784e−07,+2.088e−07]; root speed↔ −1.049e−08 [−6.006e−08,+3.851e−08]; root accel↔ −2.086e−08 [−1.620e−07,+1.179e−07]; root jerk↔ −6.423e−08 [−3.829e−07,+2.523e−07]; contact↔ +1.486e−05 [−2.227e−05,+5.975e−05]; skate↔ −1.049e−06 [−3.549e−06,+1.388e−06]` |
| HT-FILM − C0-GEO | sequential Human→Camera | `TMR↑ −0.000055; FDTMR↓ +0.000023; CLaTr↑ −0.014519; FDCLaTr↓ +2.601112; cov↑ −0.014321; dens↑ −0.016919; prec↑ −0.015533; rec↑ +0.010116; R1↑ +0.002714; R2↑ +0.003701; R3↑ +0.000493; MM↓ −0.007414; caption P/R/F1↑ +0.008291/+0.012156/+0.012105; r-FPD↓ −0.030315; Out↓ −0.003886` | `bone-CV↔ −1.138e−10 [−3.490e−10,+1.276e−10]; joint speed↔ +4.834e−09 [−5.088e−08,+5.972e−08]; joint accel↔ +5.698e−08 [−6.507e−08,+1.855e−07]; joint jerk↔ +6.747e−08 [−1.942e−07,+3.392e−07]; root speed↔ +1.216e−08 [−3.556e−08,+5.975e−08]; root accel↔ +5.811e−08 [−7.354e−08,+1.900e−07]; root jerk↔ +6.324e−08 [−2.322e−07,+3.562e−07]; contact↔ +9.939e−06 [−1.292e−05,+3.275e−05]; skate↔ +2.837e−06 [−3.123e−07,+6.276e−06]` |
| HT-HX − C0-GEO | Direct-C | `CLaTr↑ −0.154949; FDCLaTr↓ −1.140621; cov↑ +0.013567; dens↑ +0.011911; prec↑ −0.001240; rec↑ +0.007151; R1↑ −0.004441; R2↑ −0.009129; R3↑ −0.010856; MM↓ +0.009440; caption P/R/F1↑ +0.003323/+0.001405/+0.002585; r-FPD↓ −0.066864; Out↓ −0.002903` | `bone-CV↔ −1.789e−10 [−4.545e−10,+1.001e−10]; joint speed↔ −2.451e−08 [−9.482e−08,+4.508e−08]; joint accel↔ −9.693e−08 [−2.602e−07,+6.501e−08]; joint jerk↔ −1.304e−07 [−4.653e−07,+2.020e−07]; root speed↔ −1.049e−08 [−5.881e−08,+3.906e−08]; root accel↔ −2.086e−08 [−1.589e−07,+1.202e−07]; root jerk↔ −6.423e−08 [−3.856e−07,+2.499e−07]; contact↔ +1.486e−05 [−2.211e−05,+5.913e−05]; skate↔ −1.049e−06 [−3.518e−06,+1.344e−06]` |
| HT-HX − C0-GEO | sequential Human→Camera | `TMR↑ −0.000055; FDTMR↓ +0.000023; CLaTr↑ −2.048119; FDCLaTr↓ +14.139170; cov↑ −0.053779; dens↑ −0.046634; prec↑ −0.031332; rec↑ +0.012352; R1↑ −0.007649; R2↑ −0.021959; R3↑ −0.028621; MM↓ +0.573638; caption P/R/F1↑ −0.012225/−0.014458/−0.019696; r-FPD↓ +0.003128; Out↓ −0.004245` | `bone-CV↔ −1.138e−10 [−3.473e−10,+1.232e−10]; joint speed↔ +4.834e−09 [−5.098e−08,+6.082e−08]; joint accel↔ +5.698e−08 [−6.693e−08,+1.834e−07]; joint jerk↔ +6.747e−08 [−1.983e−07,+3.399e−07]; root speed↔ +1.216e−08 [−3.494e−08,+5.986e−08]; root accel↔ +5.811e−08 [−7.135e−08,+1.877e−07]; root jerk↔ +6.324e−08 [−2.221e−07,+3.596e−07]; contact↔ +9.939e−06 [−1.262e−05,+3.347e−05]; skate↔ +2.837e−06 [−3.690e−07,+6.278e−06]` |
| HT-DR − C0-GEO | Direct-C | `CLaTr↑ +1.266689; FDCLaTr↓ −2.954306; cov↑ +0.014065; dens↑ +0.038160; prec↑ +0.002220; rec↑ +0.016525; R1↑ −0.001234; R2↑ 0; R3↑ +0.005181; MM↓ −0.356856; caption P/R/F1↑ +0.027717/+0.026395/+0.026949; r-FPD↓ +0.018412; Out↓ +0.005787` | `bone-CV↔ −1.789e−10 [−4.551e−10,+8.968e−11]; joint speed↔ −2.451e−08 [−9.547e−08,+4.512e−08]; joint accel↔ −9.693e−08 [−2.666e−07,+6.434e−08]; joint jerk↔ −1.304e−07 [−4.743e−07,+2.020e−07]; root speed↔ −1.049e−08 [−5.941e−08,+3.831e−08]; root accel↔ −2.086e−08 [−1.586e−07,+1.203e−07]; root jerk↔ −6.423e−08 [−3.748e−07,+2.504e−07]; contact↔ +1.486e−05 [−2.150e−05,+6.023e−05]; skate↔ −1.049e−06 [−3.617e−06,+1.358e−06]` |
| HT-DR − C0-GEO | sequential Human→Camera | `TMR↑ −0.000055; FDTMR↓ +0.000023; CLaTr↑ +2.041756; FDCLaTr↓ −4.940895; cov↑ +0.017767; dens↑ −0.007403; prec↑ −0.016521; rec↑ +0.034790; R1↑ +0.016778; R2↑ +0.014557; R3↑ +0.012583; MM↓ −0.585448; caption P/R/F1↑ +0.039473/+0.041072/+0.042893; r-FPD↓ −0.015463; Out↓ +0.001277` | `bone-CV↔ −1.138e−10 [−3.519e−10,+1.276e−10]; joint speed↔ +4.834e−09 [−5.120e−08,+6.040e−08]; joint accel↔ +5.698e−08 [−6.838e−08,+1.829e−07]; joint jerk↔ +6.747e−08 [−2.034e−07,+3.334e−07]; root speed↔ +1.216e−08 [−3.492e−08,+5.858e−08]; root accel↔ +5.811e−08 [−7.492e−08,+1.910e−07]; root jerk↔ +6.324e−08 [−2.331e−07,+3.548e−07]; contact↔ +9.939e−06 [−1.263e−05,+3.302e−05]; skate↔ +2.837e−06 [−3.975e−07,+6.281e−06]` |

审计裁决：三臂形成明确Pareto。HT-HX的Camera geometry最强，但sequential语义与
caption明显回退；HT-DR的Direct-C与sequential Camera semantic／caption最强，但相对
C0-GEO的六项Camera geometry CI全跨零，且Direct-C r-FPD／Out回退；HT-FILM在
sequential geometry、caption与projective framing上较均衡，但FDCLaTr不占优。因此不选
单一全胜设计，也不替换C0-LAT operational mainline。该formal只评测matching Human text；
没有同endpoint的HT0／HTS完整cohort，故不能把全部增益归因于正确Human语义，更不能外推
为multi-pair Director、event grounding或Rect证据。


### Audited detail — original §3.14 v11 C0 seed23 `105K` pure4,053 matched repeat

| display ID | canonical sm_ run alias | setting | goal |
| --- | --- | --- | --- |
| C0-LAT-seed23 | `sm_v11_c0_lat_30to105k_seed23_4090g0_r2_20260803` | fresh seed23 continuation; C0-LAT objective; frozen v9 Human owner | cross-seed repeatability of the latent objective |
| C0-GEO-seed23 | `sm_v11_c0_geo_30to105k_seed23_4090g1_r2_20260803` | fresh seed23 continuation; C0-GEO objective; frozen v9 Human owner | cross-seed repeatability of the geometry objective |

每一行是一个 experiment arm；seed17 C0-LAT/C0-GEO 仅作为已审计 reference，不与 seed23 arm 合并。

两臂均以训练seed `23`从零启动，在各自fresh parent的full-state `30K`边界恢复并连续训练
至Camera optimizer step `105K`；恢复包含model、optimizer、scheduler与RNG state，不是
只载入权重。两臂共享exact v9 Pulp-only non-causal Stage1 owner、冻结Human teacher、
cache／stats／sample identities与训练exposure，唯一臂间变量为Camera objective。正式评测
固定使用eval seed `17`、EMA `105K`、pure-test `N=4,053`、ordered-ID SHA256
`a0d7627ee827e36a229d33f9975f8417ae78b504cd5a6db1edf62cb1a9266b93`、official-input
SHA256 `6d75cbf5d22b4a9f0a39d79fa8cfb900708a4095725b7ff62e7bf11ca4d2b80f`、batch `32`与
shifted-sigma Euler50；模式为Direct-H、Direct-C与formal sequential Human→Camera，
`joint_parallel=false`。

正式repeat audit位于
`/data/public/ripemangobox/Motion/StoryMotion/runs/eval/stage2/v11_c0_seed17_seed23_repeat_audit_20260803/`。
`seed_repeat_audit.json` SHA256为
`b87872ef96af20afaf385c54cae5ea5c754208c405b6dd2328de86730d4fb2a4`；audit implementation
SHA256为`846a5b4d19f76697d58a22fdd8dd300cbd1f9b18cb27427a84e61da93414e05f`。
审计逐臂验证training contract、Stage1 owner、non-causal边界、checkpoint／cache／stats／
decoder、ordered IDs、sampler、evaluator与artifact hash，并执行10,000次matched-sample
bootstrap。LAT／GEO的`fixed_samples.pt` SHA256分别为
`36dfe34cd13a752c3ba2590d0a335b20856e5ea07b1b48944455d54c8f47d9ca`与
`256778c38332c00af84a08c493d44bb9f8a9467b86251fc0c3d95504e55868d5`。

| version / run | EMA `105K` SHA256 | input contract SHA256 | evaluation contract SHA256 | result SHA256 | records SHA256 |
| --- | --- | --- | --- | --- | --- |
| v11 / `sm_v11_c0_lat_30to105k_seed23_4090g0_r2_20260803` | `076dad8276da2283086ace6701f93433e541fa7e6d72ebef54a16d0b082c8d24` | `51f16a54220064d22a16489a59ccc2401b09bc09a1900fa0e358b9bfdaabd67d` | `eed9fef9316fddc8c2114b886f38b2f433d5c0d472bd7d8861c359503dc2b39f` | `d13109ebc2e157d3acf8ac4ce8c60148d7a71236a13ade0fed8f97414eeb4ab1` | `510beb24b148ab2f15ba4ee7f9c95a2f20cb76f414e085abf439b30f3571fdd0` |
| v11 / `sm_v11_c0_geo_30to105k_seed23_4090g1_r2_20260803` | `ded0e06947bf5dd9b100c485acce59e7e14eb4995023cd0f5bc250627d5740379` | `7be6d444cb9fe14b819b925a4fb326a2e9561995023cd0f5bc250627d5740379` | `08e8516d05e6145e9f59d34a305fcb0a2d2c13d90fa98cb579d623e00a339b8a` | `8bf54167a73fa8e38dc304ae0de576c94cbb48ad1f8571a9380fdd6761544ddd` | `fad420b9bd910e894b964f332c31398d9044c3985bfd2674c9c32410d38b5641` |

#### Direct-H frozen-owner replay

两臂的Direct-H official metrics与paired geometry逐字段一致，并与seed17 owner replay通过
预注册的逐样本／cohort守卫。root-aligned MPJPE只移除root translation，仍保留heading。

| display ID / canonical run alias | N | FDTMR ↓ / TMR ↑ | coverage / density / precision / recall ↑ | R1 / R2 / R3 ↑ | MM distance ↓ | global / root-aligned MPJPE ↓ m | root ADE / FDE ↓ m | yaw mean / final / unwrapped final ↓ deg |
| --- | ---: | --- | --- | --- | ---: | --- | --- | --- |
| v11 C0-LAT-seed23 / `sm_v11_c0_lat_30to105k_seed23_4090g0_r2_20260803` | 4,053 | 99.391 / 17.608 | 0.7158 / 0.8079 / 0.8283 / 0.6528 | 0.1562 / 0.2559 / 0.3388 | 49.705 | 0.842762 / 0.228751 | 0.758774 / 1.283042 | 47.239 / 66.123 / 239.356 |
| v11 C0-GEO-seed23 / `sm_v11_c0_geo_30to105k_seed23_4090g1_r2_20260803` | 4,053 | 99.391 / 17.608 | 0.7158 / 0.8079 / 0.8283 / 0.6528 | 0.1562 / 0.2559 / 0.3388 | 49.705 | 0.842762 / 0.228751 | 0.758774 / 1.283042 | 47.239 / 66.123 / 239.356 |

#### Direct-C observed-Human Camera

| display ID / canonical run alias | FDCLaTr ↓ / CLaTr ↑ | coverage / density / precision / recall ↑ | R1 / R2 / R3 ↑ | MM distance ↓ | caption P / R / F1 ↑ | r-FPD ↓ / Out ↓ | Camera ADE / FDE ↓ m | rotation ↓ deg | observed-H global / root-aligned MPJPE ↓ m |
| --- | --- | --- | --- | ---: | --- | --- | --- | ---: | --- |
| v11 C0-LAT seed23 / `sm_v11_c0_lat_30to105k_seed23_4090g0_r2_20260803` | 20.852 / 56.931 | 0.8278 / 1.0895 / 0.9134 / 0.5581 | 0.2297 / 0.3943 / 0.5105 | 23.409 | 0.7801 / 0.6984 / 0.7339 | 0.8139 / 0.1010 | 1.398343 / 1.489706 | 29.922 | 0.125455 / 0.048795 |
| v11 C0-GEO seed23 / `sm_v11_c0_geo_30to105k_seed23_4090g1_r2_20260803` | 20.303 / 58.058 | 0.8362 / 1.0620 / 0.9050 / 0.5690 | 0.2388 / 0.3997 / 0.5191 | 23.085 | 0.7952 / 0.7151 / 0.7509 | 0.8586 / 0.1035 | 1.384952 / 1.471736 | 29.255 | 0.125455 / 0.048795 |

#### Formal sequential Human→Camera

| display ID / canonical run alias | FDCLaTr ↓ / CLaTr ↑ | coverage / density / precision / recall ↑ | R1 / R2 / R3 ↑ | MM distance ↓ | caption P / R / F1 ↑ | r-FPD ↓ / Out ↓ | H FDTMR ↓ / TMR ↑ | H global / root-aligned MPJPE ↓ m | Camera ADE / FDE ↓ m | rotation ↓ deg |
| --- | --- | --- | --- | ---: | --- | --- | --- | --- | --- | ---: |
| v11 C0-LAT seed23 / `sm_v11_c0_lat_30to105k_seed23_4090g0_r2_20260803` | 28.333 / 56.174 | 0.7752 / 0.9994 / 0.8868 / 0.5283 | 0.2189 / 0.3795 / 0.4999 | 23.636 | 0.7618 / 0.6783 / 0.7074 | 0.5130 / 0.0773 | 99.391 / 17.608 | 0.842762 / 0.228751 | 2.929020 / 3.029515 | 71.339 |
| v11 C0-GEO seed23 / `sm_v11_c0_geo_30to105k_seed23_4090g1_r2_20260803` | 27.449 / 57.057 | 0.7804 / 0.9928 / 0.8934 / 0.5260 | 0.2226 / 0.3847 / 0.5078 | 23.378 | 0.7712 / 0.6877 / 0.7170 | 0.4826 / 0.0758 | 99.391 / 17.608 | 0.842762 / 0.228751 | 2.934441 / 3.035767 | 71.202 |

#### Complete decoded-Human physical／kinematic diagnostics

每个cell是`mean / median / p90`。这些字段是decoded-Human no-reference heuristics，不是
Camera physical metric，也不能解释成ground penetration／floating等calibrated validity。
Direct-H与sequential共享同一冻结Human输出；Direct-C是observed-H reconstruction。两条
Camera objective的Human物理字段逐字段一致。

| display ID / canonical run alias | mode | bone CV ↓ | joint speed ↔ reference | joint acceleration ↔ reference | joint jerk ↔ reference |
| --- | --- | --- | --- | --- | --- |
| v11 C0-LAT-seed23 / `sm_v11_c0_lat_30to105k_seed23_4090g0_r2_20260803` | Direct-H = sequential Human | 2.279e-7 / 2.220e-7 / 2.626e-7 | 0.025358 / 0.017675 / 0.053936 | 0.023125 / 0.016568 / 0.048186 | 0.036800 / 0.026036 / 0.076142 |
| v11 C0-GEO-seed23 / `sm_v11_c0_geo_30to105k_seed23_4090g1_r2_20260803` | Direct-H = sequential Human | 2.279e-7 / 2.220e-7 / 2.626e-7 | 0.025358 / 0.017675 / 0.053936 | 0.023125 / 0.016568 / 0.048186 | 0.036800 / 0.026036 / 0.076142 |
| v11 C0-LAT-seed23 / `sm_v11_c0_lat_30to105k_seed23_4090g0_r2_20260803` | Direct-C observed-H reconstruction | 2.467e-7 / 2.250e-7 / 3.131e-7 | 0.037159 / 0.023330 / 0.083141 | 0.030219 / 0.018382 / 0.066291 | 0.046381 / 0.027812 / 0.099302 |
| v11 C0-GEO-seed23 / `sm_v11_c0_geo_30to105k_seed23_4090g1_r2_20260803` | Direct-C observed-H reconstruction | 2.467e-7 / 2.250e-7 / 3.131e-7 | 0.037159 / 0.023330 / 0.083141 | 0.030219 / 0.018382 / 0.066291 | 0.046381 / 0.027812 / 0.099302 |

| display ID / canonical run alias | mode | root speed ↔ reference | root acceleration ↔ reference | root jerk ↔ reference | contact heuristic ↔ reference | foot skate heuristic ↓ |
| --- | --- | --- | --- | --- | --- | --- |
| v11 C0-LAT-seed23 / `sm_v11_c0_lat_30to105k_seed23_4090g0_r2_20260803` | Direct-H = sequential Human | 0.017803 / 0.010157 / 0.041564 | 0.011937 / 0.007417 / 0.026799 | 0.016892 / 0.010380 / 0.037599 | 0.596170 / 0.595745 / 1.000000 | 0.030611 / 0.019465 / 0.063216 |
| v11 C0-GEO-seed23 / `sm_v11_c0_geo_30to105k_seed23_4090g1_r2_20260803` | Direct-H = sequential Human | 0.017803 / 0.010157 / 0.041564 | 0.011937 / 0.007417 / 0.026799 | 0.016892 / 0.010380 / 0.037599 | 0.596170 / 0.595745 / 1.000000 | 0.030611 / 0.019465 / 0.063216 |
| v11 C0-LAT-seed23 / `sm_v11_c0_lat_30to105k_seed23_4090g0_r2_20260803` | Direct-C observed-H reconstruction | 0.030292 / 0.017515 / 0.069143 | 0.019720 / 0.011576 / 0.043855 | 0.027753 / 0.016443 / 0.061077 | 0.491997 / 0.437500 / 1.000000 | 0.041857 / 0.024370 / 0.085574 |
| v11 C0-GEO-seed23 / `sm_v11_c0_geo_30to105k_seed23_4090g1_r2_20260803` | Direct-C observed-H reconstruction | 0.030292 / 0.017515 / 0.069143 | 0.019720 / 0.011576 / 0.043855 | 0.027753 / 0.016443 / 0.061077 | 0.491997 / 0.437500 / 1.000000 | 0.041857 / 0.024370 / 0.085574 |

#### Two-seed matched Camera geometry bootstrap

下表差值均为前者减后者；每个cell为`mean delta [95% CI]`，使用相同sample执行10,000次
paired resample。八个mode-level comparison共24个Camera geometry CI，全部跨零。

| version / comparison | mode | Δ Camera ADE ↓ m（95% CI; A−B） | Δ Camera FDE ↓ m（95% CI; A−B） | Δ Camera rotation ↓ deg（95% CI; A−B） |
| --- | --- | --- | --- | --- |
| v11 / `v11_c0_geo_fixedh_35to105k_seed17_5090g3_r2_20260730` − `v11_c0_lat_fixedh_35to105k_seed17_5090g2_r2_20260730` | Direct-C | -0.02648 [-0.06529, +0.01245] | -0.02738 [-0.06681, +0.01240] | -0.12178 [-1.08853, +0.80951] |
| v11 / `v11_c0_geo_fixedh_35to105k_seed17_5090g3_r2_20260730` − `v11_c0_lat_fixedh_35to105k_seed17_5090g2_r2_20260730` | sequential | -0.00600 [-0.03600, +0.02330] | -0.00266 [-0.03219, +0.02676] | +0.07250 [-0.91249, +1.08543] |
| v11 / `sm_v11_c0_geo_30to105k_seed23_4090g1_r2_20260803` − `sm_v11_c0_lat_30to105k_seed23_4090g0_r2_20260803` | Direct-C | -0.01339 [-0.04775, +0.02179] | -0.01797 [-0.05326, +0.01793] | -0.66706 [-1.55837, +0.26073] |
| v11 / `sm_v11_c0_geo_30to105k_seed23_4090g1_r2_20260803` − `sm_v11_c0_lat_30to105k_seed23_4090g0_r2_20260803` | sequential | +0.00542 [-0.02912, +0.04100] | +0.00625 [-0.02959, +0.04338] | -0.13707 [-1.15967, +0.90620] |
| v11 / `sm_v11_c0_lat_30to105k_seed23_4090g0_r2_20260803` − `v11_c0_lat_fixedh_35to105k_seed17_5090g2_r2_20260730` | Direct-C | -0.01413 [-0.05520, +0.02500] | -0.00882 [-0.05031, +0.03073] | -0.00046 [-0.94181, +0.95590] |
| v11 / `sm_v11_c0_lat_30to105k_seed23_4090g0_r2_20260803` − `v11_c0_lat_fixedh_35to105k_seed17_5090g2_r2_20260730` | sequential | -0.01378 [-0.04625, +0.01881] | -0.01267 [-0.04572, +0.01995] | -0.09554 [-1.07293, +0.90480] |
| v11 / `sm_v11_c0_geo_30to105k_seed23_4090g1_r2_20260803` − `v11_c0_geo_fixedh_35to105k_seed17_5090g3_r2_20260730` | Direct-C | -0.00104 [-0.03533, +0.03391] | +0.00059 [-0.03497, +0.03697] | -0.54573 [-1.43111, +0.35788] |
| v11 / `sm_v11_c0_geo_30to105k_seed23_4090g1_r2_20260803` − `v11_c0_geo_fixedh_35to105k_seed17_5090g3_r2_20260730` | sequential | -0.00235 [-0.03332, +0.02887] | -0.00376 [-0.03487, +0.02825] | -0.30511 [-1.29920, +0.67211] |

审计裁决：seed23重现了冻结Human owner的逐样本保持，并未产生稳健Camera geometry
objective胜者。seed23的GEO在两种Camera模式的多数raw semantic／caption均值上高于LAT，
但seed17是混合Pareto，且当前official semantic evaluator没有对应的逐样本bootstrap单位；
因此只作描述，不把raw均值趋势升级为显著性结论。2026-08-04将C0-LAT指定为后续operational
mainline是作者侧主表优先级与优化简洁性决策；它不由本bootstrap证明单一objective稳健胜出。
C0-GEO保留为audited alternate。本轮关闭独立训练seed缺口，但不替代后续sealed audit、视觉失败
分层或matched cascade。


### Audited detail — original §3.15 C1REL／C1REL-noI16 matched Stage2 pure4,053 three-interface formal

| display ID | canonical sm_ run alias | setting | goal |
| --- | --- | --- | --- |
| C1REL-rawT0 | `sm_c1rel_rawt0_lat_h105k_c105k_seed17_4090g0_20260804` | C1REL-C48 with raw-T0 Camera text; I16 retained; three-interface formal, `joint_parallel=false` | evaluate the C1REL representation/control interface |
| C1REL-noI16-rawT0 | `sm_c1rel_nointeraction16_rawt0_lat_h105k_c105k_seed17_4090g1_20260806` | same raw-T0 C1REL-C48; Interaction16 removed; three-interface formal, `joint_parallel=false` | isolate the Interaction16 ablation |

每一行是一个 experiment arm；同目录中的 historical `joint_parallel` artifact 仅保留 provenance，不属于本组 formal 指标。

本节回填两条已经存在的 Stage2 formal artifact，不启动新训练或 evaluator。两条 run 的正式报告
包含 Direct-H、Direct-C observed-H 与 sequential Human→Camera 接口，N=`4,053`，ordered-ID
SHA-256 为`a0d7627ee827e36a229d33f9975f8417ae78b504cd5a6db1edf62cb1a9266b93`，且合同明确
`joint_parallel=false`。同目录下的 `joint_parallel` 结果保留为历史 provenance；它们不属于本节
formal 接口，也没有被改名。

| version / run | mode | N | evaluation contract SHA-256 | result SHA-256 | records SHA-256 | fixed samples SHA-256 | manifest SHA-256 |
| --- | --- | ---: | --- | --- | --- | --- | --- |
| C1REL / `sm_c1rel_rawt0_lat_h105k_c105k_seed17_4090g0_20260804` | sequential | 4,053 | `36da153fd9cdb55b996b8a82d3a874fa1c7cbb5503585407360b10c3ec180422` | `48dbce1de422d271e6536075cc692ed87b32c91ca5b78920ec061bd445cdf041` | `48b4eb275ac44de91972c1971bf3eff601c30ad65d7b725b5a86505b3cd2f08b` | `393f0594c26cf8d288113f841de4d83cf220a83c68461c41c1f49723f3f0bd4e` | `a6d24148baf6a5bbdca70f11b8eca571410a753eb843902858b3741d7b9c221f` |
| C1REL-noI16 / `sm_c1rel_nointeraction16_rawt0_lat_h105k_c105k_seed17_4090g1_20260806` | sequential | 4,053 | `8a9c4b761a79752e0828e62db6832216d234e84a0b1c5a8e91f5a9e1ed3ce4ae` | `2cc342abf5fae9536db04dcaffacba80d4f46ff33baf10909caf17bb7f5642f0` | `17dbcfad14dc9415231ebf96fbbabf7eb937013c16181f9873cbc9e356460034` | `e4a66d648aa22dbcbbc40e5ae7149f45eb8f9a4fa41aed04db168909172bdd90` | `dd705440635b6b07f3dbbd963d400f281f9789fcd32375e92d2518e61c6448fd` |

#### Semantic and framing aggregates

这些是各接口原始 `results.json` 的 aggregate；`r-FPD` 与 `Out` 使用 Stage2 official
projection callback 语义。Direct-C 的 Human 数值是 observed-H 子指标，不能与 Direct-H
自由 Human 结果混为一项。

| display ID / canonical run alias | mode | Human TMR ↑ | Human FDTMR ↓ | Camera CLaTr ↑ | Camera FDCLaTr ↓ | observed-H TMR ↑ / FDTMR ↓ | r-FPD ↓ / Out ↓ |
| --- | --- | ---: | ---: | ---: | ---: | --- | --- |
| C1REL / `sm_c1rel_rawt0_lat_h105k_c105k_seed17_4090g0_20260804` | Direct-H | 17.276762 | 104.331841 | — | — | — | — |
| C1REL / `sm_c1rel_rawt0_lat_h105k_c105k_seed17_4090g0_20260804` | Direct-C observed-H | — | — | 61.985516 | 18.183035 | 15.653248 / 7.931718 | 1.259693 / 0.131841 |
| C1REL / `sm_c1rel_rawt0_lat_h105k_c105k_seed17_4090g0_20260804` | sequential | 17.276762 | 104.331841 | 61.360668 | 17.322052 | — | 0.687697 / 0.091884 |
| C1REL-noI16 / `sm_c1rel_nointeraction16_rawt0_lat_h105k_c105k_seed17_4090g1_20260806` | Direct-H | 17.619104 | 92.033676 | — | — | — | — |
| C1REL-noI16 / `sm_c1rel_nointeraction16_rawt0_lat_h105k_c105k_seed17_4090g1_20260806` | Direct-C observed-H | — | — | 43.920853 | 65.427673 | 15.575075 / 9.833646 | 8.372213 / 0.444066 |
| C1REL-noI16 / `sm_c1rel_nointeraction16_rawt0_lat_h105k_c105k_seed17_4090g1_20260806` | sequential | 17.619104 | 92.033676 | 41.235523 | 89.051743 | — | 8.624285 / 0.443064 |

#### Paired geometry aggregates

Stage2 generation artifacts expose the paired geometry subset below. It is not a replacement for
the complete Stage1 schema in §6.1–§6.4 (which additionally contains integrated yaw, FOV and the
full projective fields). Stage1 full-field rows for HREL, NoInt-HREL, C1REL and C1REL-noI16 remain
the canonical entries in §6.2–§6.4; no rerun is needed.

| display ID / canonical run alias | mode | Human global / root-aligned MPJPE ↓ m | Human root ADE / FDE ↓ m | Camera center ADE / FDE ↓ m | Camera rotation ↓ deg |
| --- | --- | --- | --- | --- | ---: |
| C1REL / `sm_c1rel_rawt0_lat_h105k_c105k_seed17_4090g0_20260804` | Direct-H | 0.844060 / 0.232308 | 0.757307 / 1.266741 | — | — |
| C1REL / `sm_c1rel_rawt0_lat_h105k_c105k_seed17_4090g0_20260804` | Direct-C observed-H | — | — | 1.709340 / 1.785491 | 35.901068 |
| C1REL / `sm_c1rel_rawt0_lat_h105k_c105k_seed17_4090g0_20260804` | sequential | 0.844060 / 0.232308 | 0.757307 / 1.266741 | 2.990472 / 3.093771 | 71.352258 |
| C1REL-noI16 / `sm_c1rel_nointeraction16_rawt0_lat_h105k_c105k_seed17_4090g1_20260806` | Direct-H | 0.846452 / 0.228077 | 0.762097 / 1.282781 | — | — |
| C1REL-noI16 / `sm_c1rel_nointeraction16_rawt0_lat_h105k_c105k_seed17_4090g1_20260806` | Direct-C observed-H | — | — | 1.665444 / 1.777655 | 41.145027 |
| C1REL-noI16 / `sm_c1rel_nointeraction16_rawt0_lat_h105k_c105k_seed17_4090g1_20260806` | sequential | 0.846452 / 0.228077 | 0.762097 / 1.282781 | 2.646307 / 2.745572 | 67.081549 |

#### Decoded-Human physical／kinematic aggregate

每个 cell 为 `mean / median / p90`；这些是 no-reference decoded-Human heuristics，不是
calibrated physical-validity 分数。两条 sequential 与各自 Direct-H 共享同一 Human 输出。

| display ID / canonical run alias | mode | bone CV ↓ | joint speed ↔ reference | joint acceleration ↔ reference | joint jerk ↔ reference | root speed ↔ reference | root acceleration ↔ reference | root jerk ↔ reference | contact ↔ reference | skate ↓ |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| C1REL / `sm_c1rel_rawt0_lat_h105k_c105k_seed17_4090g0_20260804` | sequential | 2.284e-7 / 2.214e-7 / 2.605e-7 | 0.025801 / 0.017677 / 0.054646 | 0.023425 / 0.016651 / 0.048673 | 0.037175 / 0.026313 / 0.077194 | 0.018116 / 0.010321 / 0.042993 | 0.012080 / 0.007464 / 0.026990 | 0.017046 / 0.010386 / 0.038141 | 0.599366 / 0.600917 / 1.000000 | 0.030448 / 0.018859 / 0.063656 |
| C1REL-noI16 / `sm_c1rel_nointeraction16_rawt0_lat_h105k_c105k_seed17_4090g1_20260806` | sequential | 2.285e-7 / 2.216e-7 / 2.621e-7 | 0.025357 / 0.017363 / 0.054974 | 0.022670 / 0.016144 / 0.047586 | 0.035787 / 0.025314 / 0.074766 | 0.018010 / 0.010190 / 0.042527 | 0.011954 / 0.007312 / 0.027177 | 0.016846 / 0.010189 / 0.038298 | 0.594181 / 0.592369 / 1.000000 | 0.030316 / 0.018301 / 0.063004 |

历史 `joint_parallel/results.json` 的数字仍可在对应 run 目录按其原始 hash 复核，但不能覆盖或
改名本节的 sequential artifact。PulpMotion-Repro r9 仍是外部 native Stage1 baseline；其
原生 evaluator 没有 StoryMotion paired-geometry／physical artifact，因此不以缺失字段补造
canonical Stage1 数字。


### Audited detail — original §3.16 HREL matched Stage2 pure4,053 formal

| display ID | canonical sm_ run alias | setting | goal |
| --- | --- | --- | --- |
| HREL | `sm_p1_hrel_matched_lat_h105k_c105k_seed17_4090g1_20260809` | HREL representation owner; frozen Human teacher; three active asymmetric modes | test the matched HREL Stage2 owner under the actual `128/1` evaluator protocol |
| C1REL-rawT0 reference | `sm_c1rel_rawt0_lat_h105k_c105k_seed17_4090g0_20260804` | C1REL representation/control from §3.15; same ordered-ID comparison boundary | paired reference for field-wise HREL-minus-C1REL audit |

每一行是一个 named arm/reference；HREL 的 canonical run alias 保留在 provenance 列中，短 display ID 用于正文。

本节登记 HREL matched Stage2 的唯一正式三模式结果。run
`sm_p1_hrel_matched_lat_h105k_c105k_seed17_4090g1_20260809` 使用 exact v9
Pulp-only HREL representation owner、owning decoder、原始 Pulp captions 与 frozen
Human teacher；`is_causal=false`，`joint_parallel=false`，模式为 Direct-H、Direct-C 与
sequential Human→Camera。三接口均为 pure-test `N=4,053`，ordered-ID SHA-256 为
`a0d7627ee827e36a229d33f9975f8417ae78b504cd5a6db1edf62cb1a9266b93`，sampler 为
shifted-sigma explicit Euler50、`eta=0`、CFG=1、seed17。

Training contract 声明 `eval.batch_size=128`、`decode_batch_size=64`；immutable evaluator
实际要求 true-length decode batch `1`，且 accepted C1REL formal reference 也使用 `128/1`。
因此本节明确绑定 actual evaluation protocol `128/1`，不宣称与 HREL training contract 的
decode64 完全匹配。protocol exception artifact 为
canonical alias `sm_p1_hrel_matched_lat_h105k_c105k_seed17_4090g1_20260809/protocol_exception.json`（exact immutable path见[[StoryMotion-folder-rename-map]]），
SHA-256=`6ae08ecda6c3a8ce6adf14fd5b2113799f5ba4e7e240562dcae58dae3ac6a454`；training
contract SHA-256=`08dc0362a45d5a79f7aac4913a815cafe750e02a7160cccf74b1588ff70e3b90`。

#### Formal artifact identity

三行均为 `status=evaluated`、`samples=4,053`，records 全部 finite；checkpoint SHA-256 为
`ec0bc54fede329d74faac53c6ae6ea9165734db5c3412851040502c3c7c74ca4`，owning decoder
SHA-256 为`51233f6a032c779e66b6eed4bb22b7f61c41d9b4a5a0a1ffc7dade7d3d86d4df`。

| version / run | mode | evaluation contract SHA-256 | fixed samples SHA-256 | result SHA-256 | records SHA-256 | manifest SHA-256 |
| --- | --- | --- | --- | --- | --- | --- |
| HREL / `sm_p1_hrel_matched_lat_h105k_c105k_seed17_4090g1_20260809` | Direct-H | `040965e1ec792cba0b97582d837c3e9f14b028c887a98b5a1a3b34d9bbba9cd9` | `e06ef5454de05c12ad68fa96515fab0aba3656cceba585e3df088e1d119624a0` | `393af19a3124aee9478cc9e94eb9cc7eaafed5839c8d77ff4cd586ce6e80abf9` | `1971a08f39503889ff675c82ecafd48bec42e53451248480f64a156c523518fd` | `eb9327d7c1cec1861c6023775dd82618d3b4cd8258d11b0dcf4920e64edc5cff` |
| HREL / `sm_p1_hrel_matched_lat_h105k_c105k_seed17_4090g1_20260809` | Direct-C | `ec390274f66547ffd94918903ea50b7a6d164c4d7648b3c4c77451f00994b259` | `8b0a7eb0715d2d1ed482af46989385a9a20c95f456691f637fe2203a65448872` | `5433a1304668bf767d72fa65b7e676619e54eec06d9eb515a2ff46f826f1debe` | `1b5147ce64cc7315fc81f513b3e084ffdca52af3bff9b8a1050ea02c3c65273e` | `ceb231aad6524116def3808b7a1d444409f3a57f2f3d06b947f74900783b34fc` |
| HREL / `sm_p1_hrel_matched_lat_h105k_c105k_seed17_4090g1_20260809` | sequential | `7b9fd7ab3bb39a90eacf7f8cfd66dba053f0386bbb7ca81db8209f1c1fc0f05b` | `146eac209ba228fce0b7ac1ecd0c33f0b4ea12dd210342d38e49d66f77115480` | `37e1b8744eabdf6245775c0b3dd5d8859fa9a74355d00a78a8323c806239c555` | `45bd6dbd0c8609edf861730256d5bf46dc408294ceb436ae17fbc61357a720ec` | `b140a69cf9fe3787a71c82c66ad3d47d0293ccb753ae310b8dd746968d067bf7` |

#### Semantic and framing aggregates

每行均来自该 mode 的 `results.json` aggregate。Direct-C 的 observed-H Human 指标与 Direct-H
自由 Human 指标不是同一 completion condition；projection callback 的恒零字段仍保留为
原始 aggregate，不解释为额外质量证据。

| display ID / canonical run alias | mode | Human TMR ↑ / FDTMR ↓ | Camera CLaTr ↑ / FDCLaTr ↓ | observed-H TMR ↑ / FDTMR ↓ | caption P / R / F1 ↑ | r-FPD ↓ / Out ↓ |
| --- | --- | --- | --- | --- | --- | --- |
| HREL / `sm_p1_hrel_matched_lat_h105k_c105k_seed17_4090g1_20260809` | Direct-H | `17.354467 / 100.254402` | — | — | — | — |
| HREL / `sm_p1_hrel_matched_lat_h105k_c105k_seed17_4090g1_20260809` | Direct-C observed-H | — | `57.238335 / 22.199497` | `15.659584 / 7.944044` | `0.792642 / 0.698820 / 0.740582` | `0.889080 / 0.104959` |
| HREL / `sm_p1_hrel_matched_lat_h105k_c105k_seed17_4090g1_20260809` | sequential Human→Camera | `17.354467 / 100.254402` | `55.586891 / 30.147327` | — | `0.757394 / 0.670500 / 0.701713` | `0.506346 / 0.076670` |

Direct-H Human retrieval为`R1/R2/R3=0.063163/0.097952/0.136442`、coverage/density/precision/recall
为`0.701195/0.825495/0.845053/0.650871`、MM distance=`49.808089`。Direct-C Camera retrieval
为`R1/R2/R3=0.081421/0.152233/0.217863`、coverage/density/precision/recall
为`0.827529/1.090277/0.910687/0.547020`、MM distance=`23.331600`；observed-H joint
retrieval为`R1/R2/R3=0.046879/0.086109/0.120651`、coverage/density/precision/recall
为`0.999260/1.117705/0.999753/0.996546`、MM distance=`50.265059`。Sequential Camera
retrieval为`R1/R2/R3=0.077227/0.142857/0.196891`、coverage/density/precision/recall
为`0.760179/1.022130/0.896127/0.517658`、MM distance=`23.799211`；Human retrieval与
Direct-H相同。Direct-C projection aggregate 的其余字段 `coverage/density/error/g-FPD/precision/recall`
均为`0`；sequential相同字段也均为`0`，仅`r-FPD`与`Out`如表所示。

#### Paired geometry aggregates

| display ID / canonical run alias | mode | Human global / root-aligned MPJPE ↓ m | Human root ADE / FDE ↓ m | Camera center ADE / FDE ↓ m | Camera rotation ↓ deg |
| --- | --- | --- | --- | --- | ---: |
| HREL / `sm_p1_hrel_matched_lat_h105k_c105k_seed17_4090g1_20260809` | Direct-H | `0.848565 / 0.230946` | `0.762336 / 1.278247` | — | — |
| HREL / `sm_p1_hrel_matched_lat_h105k_c105k_seed17_4090g1_20260809` | Direct-C observed-H | — | — | `1.424767 / 1.510033` | `30.037865` |
| HREL / `sm_p1_hrel_matched_lat_h105k_c105k_seed17_4090g1_20260809` | sequential Human→Camera | `0.848565 / 0.230946` | `0.762336 / 1.278247` | `2.893823 / 3.000069` | `71.159801` |

Direct-H exact teacher regression max-abs=`6.7711e-05`，通过 frozen-owner gate；sequential Human
branch复用同一生成Human，因此Human geometry相同。

#### Decoded-Human physical／kinematic diagnostics

每个 cell 为 `mean / median / p90`；这些是 no-reference decoded-Human diagnostics，不是 calibrated
physical-validity 分数。Direct-H与sequential Human共享同一输出；Direct-C没有单独的
decoded-Human physical aggregate（`null`）。

| display ID / canonical run alias | mode | bone CV ↓ | joint speed ↔ reference | joint acceleration ↔ reference | joint jerk ↔ reference | root speed ↔ reference | root acceleration ↔ reference | root jerk ↔ reference | contact ↔ reference | skate ↓ |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| HREL / `sm_p1_hrel_matched_lat_h105k_c105k_seed17_4090g1_20260809` | dataset reference | `2.414e-7 / 2.195e-7 / 3.080e-7` | `0.035336 / 0.021716 / 0.080298` | `0.026611 / 0.015280 / 0.060480` | `0.041110 / 0.023375 / 0.093897` | `0.029456 / 0.016709 / 0.067934` | `0.017055 / 0.009513 / 0.039636` | `0.023314 / 0.013070 / 0.053262` | `0.489381 / 0.425000 / 1.000000` | `0.039985 / 0.021858 / 0.080741` |
| HREL / `sm_p1_hrel_matched_lat_h105k_c105k_seed17_4090g1_20260809` | Direct-H = sequential Human | `2.290e-7 / 2.214e-7 / 2.629e-7` | `0.025784 / 0.017563 / 0.055609` | `0.023378 / 0.016493 / 0.048864` | `0.037092 / 0.025973 / 0.076024` | `0.018118 / 0.010202 / 0.042848` | `0.012078 / 0.007469 / 0.027795` | `0.017053 / 0.010474 / 0.038711` | `0.601517 / 0.602649 / 1.000000` | `0.030490 / 0.018605 / 0.063476` |

#### HREL minus C1REL exact ordered paired bootstrap

配对审计 artifact 为
canonical alias `sm_p1_hrel_matched_lat_h105k_c105k_seed17_4090g1_20260809/paired_bootstrap_hrel_minus_c1rel_seed17.json`（exact immutable path见[[StoryMotion-folder-rename-map]]），
SHA-256=`5b48a7c3a0f460323b2d2c8bb122dfc71fb9f93b89a8264e8cc7babcff56327e`。审计使用相同
ordered IDs、10,000 resamples、seed=`260730`；差值定义为`HREL − C1REL`，仅对 records 中实际
存在的逐样本 geometry 计算。C1REL reference为 §3.15 的
`sm_c1rel_rawt0_lat_h105k_c105k_seed17_4090g0_20260804`。

| version / run | mode | metric (direction) | mean delta (A−B) | 95% CI |
| --- | --- | --- | ---: | --- |
| HREL − C1REL / `sm_p1_hrel_matched_lat_h105k_c105k_seed17_4090g1_20260809` vs `sm_c1rel_rawt0_lat_h105k_c105k_seed17_4090g0_20260804` | Direct-H | global MPJPE ↓ | `+0.004504` | `[-0.002439, +0.011316]` |
| HREL − C1REL / `sm_p1_hrel_matched_lat_h105k_c105k_seed17_4090g1_20260809` vs `sm_c1rel_rawt0_lat_h105k_c105k_seed17_4090g0_20260804` | Direct-H | root ADE ↓ | `+0.005029` | `[-0.001792, +0.011706]` |
| HREL − C1REL / `sm_p1_hrel_matched_lat_h105k_c105k_seed17_4090g1_20260809` vs `sm_c1rel_rawt0_lat_h105k_c105k_seed17_4090g0_20260804` | Direct-H | root-aligned MPJPE ↓ | `-0.001362` | `[-0.002883, +0.000143]` |
| HREL − C1REL / `sm_p1_hrel_matched_lat_h105k_c105k_seed17_4090g1_20260809` vs `sm_c1rel_rawt0_lat_h105k_c105k_seed17_4090g0_20260804` | Direct-H | root FDE ↓ | `+0.011506` | `[-0.004050, +0.026671]` |
| HREL − C1REL / `sm_p1_hrel_matched_lat_h105k_c105k_seed17_4090g1_20260809` vs `sm_c1rel_rawt0_lat_h105k_c105k_seed17_4090g0_20260804` | Direct-C | Camera ADE ↓ | `-0.284573` | `[-0.333422, -0.236861]` |
| HREL − C1REL / `sm_p1_hrel_matched_lat_h105k_c105k_seed17_4090g1_20260809` vs `sm_c1rel_rawt0_lat_h105k_c105k_seed17_4090g0_20260804` | Direct-C | Camera FDE ↓ | `-0.275457` | `[-0.325246, -0.226620]` |
| HREL − C1REL / `sm_p1_hrel_matched_lat_h105k_c105k_seed17_4090g1_20260809` vs `sm_c1rel_rawt0_lat_h105k_c105k_seed17_4090g0_20260804` | Direct-C | Camera rotation ↓ | `-5.863202` | `[-7.021823, -4.698981]` |
| HREL − C1REL / `sm_p1_hrel_matched_lat_h105k_c105k_seed17_4090g1_20260809` vs `sm_c1rel_rawt0_lat_h105k_c105k_seed17_4090g0_20260804` | sequential | Camera ADE ↓ | `-0.096648` | `[-0.142145, -0.052241]` |
| HREL − C1REL / `sm_p1_hrel_matched_lat_h105k_c105k_seed17_4090g1_20260809` vs `sm_c1rel_rawt0_lat_h105k_c105k_seed17_4090g0_20260804` | sequential | Camera FDE ↓ | `-0.093702` | `[-0.140213, -0.047547]` |
| HREL − C1REL / `sm_p1_hrel_matched_lat_h105k_c105k_seed17_4090g1_20260809` vs `sm_c1rel_rawt0_lat_h105k_c105k_seed17_4090g0_20260804` | sequential | Camera rotation ↓ | `-0.192457` | `[-1.510332, +1.083402]` |

Direct-C 三项 Camera geometry 的 CI 均不跨零；sequential 的 ADE/FDE CI 不跨零而 rotation
CI 跨零；Human 四项 geometry CI 均跨零。`records.jsonl` 没有逐样本 semantic/framing 字段，
而 `results.json` 只保留 cohort-level aggregate，因此 semantic/framing 的 exact paired
bootstrap 标记为 blocked，不能声称显著性。C1REL 的 Camera semantic aggregate 高于 HREL，
但没有逐样本 semantic/framing paired unit，故不能把该 aggregate 趋势升级为单边 superiority。

#### HREL − C1REL distributional／semantic and decoded-Human delta supplement

下表补齐同一 `results.json` cohort aggregate 的算术差值，均为前者减后者；指标箭头只表示
单项指标的预注册方向，不把 aggregate delta 当作显著性。`records.jsonl` 仅含 geometry，故
distributional／semantic 与 decoded-Human physical／kinematic 均为 `CI unavailable`；后者的
`↔` 字段明确不赋予“更优”方向。

| comparison | mode | distributional／semantic aggregate Δ (A−B; no CI) | decoded-Human physical／kinematic aggregate Δ (A−B; mean / median / p90; no CI) |
| --- | --- | --- | --- |
| HREL − C1REL | Direct-H | `TMR↑ +0.077705; FDTMR↓ −4.077438; cov↑ −0.008399; dens↑ −0.005040; prec↑ +0.006149; rec↑ +0.007150; R1↑ +0.003207; R2↑ −0.002714; R3↑ 0; MM↓ −0.022152` | `bone-CV↔ +5.497e−10/+1.977e−11/+2.467e−09; joint speed↔ −1.716e−05/−1.141e−04/+9.628e−04; joint accel↔ −4.666e−05/−1.582e−04/+1.912e−04; joint jerk↔ −8.318e−05/−3.392e−04/−1.170e−03; root speed↔ +1.706e−06/−1.194e−04/−1.448e−04; root accel↔ −1.618e−06/+4.994e−06/+8.051e−04; root jerk↔ +6.996e−06/+8.793e−05/+5.699e−04; contact↔ +0.002151/+0.001732/0; skate↔ +4.154e−05/−2.536e−04/−1.798e−04` |
| HREL − C1REL | Direct-C observed-H | `CLaTr↑ −4.747181; FDCLaTr↓ +4.016462; cov↑ −0.004686; dens↑ +0.054950; prec↑ +0.013087; rec↑ −0.050831; R1↑ −0.004935; R2↑ −0.007895; R3↑ −0.011103; MM↓ +1.317759; caption P/R/F1↑ −0.030678/−0.050919/−0.035253; r-FPD↓ −0.370613; Out↓ −0.026882` | `—` (`decoded_human_physical=null` in both Direct-C results) |
| HREL − C1REL | sequential Human→Camera | `TMR↑ +0.077705; FDTMR↓ −4.077438; cov↑ −0.008399; dens↑ −0.005040; prec↑ +0.006149; rec↑ +0.007150; R1↑ +0.003207; R2↑ −0.002714; R3↑ 0; MM↓ −0.022152; CLaTr↑ −5.773777; FDCLaTr↓ +12.825280; cov↑ −0.019238; dens↑ +0.046574; prec↑ +0.012089; rec↑ −0.046376; R1↑ −0.002961; R2↑ −0.012090; R3↑ −0.015791; MM↓ +1.576873; caption P/R/F1↑ −0.039857/−0.067448/−0.060786; r-FPD↓ −0.181351; Out↓ −0.015214` | `bone-CV↔ +5.497e−10/+1.977e−11/+2.467e−09; joint speed↔ −1.716e−05/−1.141e−04/+9.628e−04; joint accel↔ −4.666e−05/−1.582e−04/+1.912e−04; joint jerk↔ −8.318e−05/−3.392e−04/−1.170e−03; root speed↔ +1.706e−06/−1.194e−04/−1.448e−04; root accel↔ −1.618e−06/+4.994e−06/+8.051e−04; root jerk↔ +6.996e−06/+8.793e−05/+5.699e−04; contact↔ +0.002151/+0.001732/0; skate↔ +4.154e−05/−2.536e−04/−1.798e−04` |

#### Claim boundary

HREL 继续作为当前 StoryMotion representation owner；本节支持的是 actual `128/1` formal protocol
下的 matched Stage2 mixed-Pareto comparison：HREL 在 Direct-C geometry 以及 sequential
Camera ADE/FDE 上显著更强，C1REL 的 Camera semantic aggregate 更高，Human geometry 没有明确差异。
不把 C1REL 升格为 owner，不把 actual eval `128/1` 写成 training decode64 matched，也不把
semantic aggregate 或 no-reference physical diagnostics写成 calibrated validity。


### Audited detail — original §3.17 C1REL seed23 raw-T0 Stage2 repeat audit

| display ID | canonical sm_ run alias | setting | goal |
| --- | --- | --- | --- |
| C1REL-rawT0-seed23 | `sm_c1rel_lat_h105k_c105k_seed23_4090g0_20260809` | fresh seed23 C1REL endpoint; raw-T0 Camera text; same evaluator boundary as seed17 | cross-seed repeatability only |
| C1REL-rawT0-seed17 reference | `sm_c1rel_rawt0_lat_h105k_c105k_seed17_4090g0_20260804` | seed17 formal reference from §3.15 | paired reference; not a new arm in this repeat |

每一行是一个 named run/reference；本节的结论是 repeatability evidence，不是方法干预的因果排名。

`sm_c1rel_lat_h105k_c105k_seed23_4090g0_20260809`完成 fresh Stage2 `210K` endpoint 后，
在同一 pure-test `N=4,053`、ordered-ID SHA-256
`a0d7627ee827e36a229d33f9975f8417ae78b504cd5a6db1edf62cb1a9266b93`、eval seed17、
shifted-sigma explicit Euler50、CFG=1、`batch=128 / decode_batch=1`协议下完成 Direct-H、
Direct-C 与 sequential Human→Camera。三模式均 `is_causal=false`；目录中没有
`joint_parallel` artifact。该 run 与 seed17 reference 的 Stage2 checkpoint 不同，因此本节是
cross-seed repeat audit，不是两个方法干预的因果比较。

两次评测共享 ordered IDs、split、sample count、sampler、eval/decode batch、owning decoder，
并逐项通过 manifest artifact hash、records provenance、fixed-sample metadata、finite 数值及
checkpoint／decoder host SHA 检查。审计与 paired geometry bootstrap JSON 为
canonical alias `sm_c1rel_lat_h105k_c105k_seed23_4090g0_20260809/seed17_paired_audit_bootstrap_r2.json`（exact immutable path见[[StoryMotion-folder-rename-map]]），
SHA-256=`89246b01674a3e8682d74eaa0c38356f47d70e937d2df934e8a6888c2c46b0a5`；使用相同 sample ID
做 10,000 次 paired resample，seed=`260810`，差值定义为`seed23 − seed17`。

| version / run | mode | N | evaluation contract SHA-256 | fixed samples SHA-256 | records SHA-256 | results SHA-256 | manifest SHA-256 |
| --- | --- | ---: | --- | --- | --- | --- | --- |
| C1REL / `sm_c1rel_lat_h105k_c105k_seed23_4090g0_20260809` | Direct-H | 4,053 | `61f539ab51fd8841cf70d4f659abda017ff5385f7cc7b26aec5ec00ffb29e10d` | `865f42598096a197cf0eb5ee846dd6c697fb92767737deacb261d303b1b3190c` | `c7246844d9aa38ea16b40f94f4ce77f01007435b7963e992dee4fb2e20cd7b74` | `6a27c8682877ebf07599bdbea1d8098476977ae787e4129e6a2f468331a82564` | `ecce6e02729d1c2ffe1e23abf3cf254a3c31cb02236c2769ea85788b4baef251` |
| C1REL / `sm_c1rel_lat_h105k_c105k_seed23_4090g0_20260809` | Direct-C | 4,053 | `f9d32a269e28980133fb4c39b3dad9a283d5afa5d028bc3caadfa15aefd26efd` | `a498915537e3e0ddd73a4698db16d14785551e395c44a8611598947ad007eafc` | `2453bfb0cb39c575b6a934d844f7201fec5505b6daf1019118136f90cf881438` | `dffafd4a41307791f0b1704c2ef5e4c7b1ce3d62a8655a67543fe1830845c633` | `13f5d7a8e8079aa01f007d482bdaf777ed6e3655cf490856590c80d4b1d7cb6c` |
| C1REL / `sm_c1rel_lat_h105k_c105k_seed23_4090g0_20260809` | sequential | 4,053 | `63f8be317c33ba6704ff2685af0bb5c5730d5c9be9866ae1f64c1d12473750c4` | `7e378f915dc7131bce7a404c56b17ee3d7873f14895ccb0cc35e5c840dd9414d` | `c1a73a36392d47c964ffe8d2c1034bd6939136b0d485930724dc5494a3585bf0` | `2981ce3caddd41aa80d10971d91838579d1343b91308b4dc60868d09ead3272a` | `7e5bad5871c67a1b96a2d55c7a95d690560b76ff08efefa3ae55ab7914294977` |

#### Aggregate metrics

这些数值直接来自三种 mode 的 `results.json`；seed17 数值仍由 §3.15 作为 reference 保存。它们
不是 semantic significance test，且 raw Pulp Camera captions 保持为 T0 boundary。

| display ID / canonical run alias | mode | Human TMR ↑ / FDTMR ↓ | Camera CLaTr ↑ / FDCLaTr ↓ | observed-H TMR ↑ / FDTMR ↓ | caption F1 ↑ | r-FPD ↓ / Out ↓ |
| --- | --- | --- | --- | --- | ---: | --- |
| C1REL / `sm_c1rel_lat_h105k_c105k_seed23_4090g0_20260809` | Direct-H | `17.455219 / 102.077736` | — | — | — | — |
| C1REL / `sm_c1rel_lat_h105k_c105k_seed23_4090g0_20260809` | Direct-C observed-H | — | `61.610401 / 20.361712` | `15.653248 / 7.931718` | `0.772358` | — |
| C1REL / `sm_c1rel_lat_h105k_c105k_seed23_4090g0_20260809` | sequential Human→Camera | `17.455219 / 102.077736` | `60.909504 / 18.602613` | — | `0.766348` | `0.670877 / 0.092575` |

#### Paired geometry aggregates and cross-seed uncertainty

| display ID / canonical run alias | mode | Human global / root-aligned MPJPE ↓ m | Human root ADE / FDE ↓ m | Camera center ADE / FDE ↓ m | Camera rotation ↓ deg |
| --- | --- | --- | --- | --- | ---: |
| C1REL / `sm_c1rel_lat_h105k_c105k_seed23_4090g0_20260809` | Direct-H | `0.851383 / 0.231334` | `0.764674 / 1.278857` | — | — |
| C1REL / `sm_c1rel_lat_h105k_c105k_seed23_4090g0_20260809` | Direct-C observed-H | — | — | `1.680650 / 1.750830` | `35.489959` |
| C1REL / `sm_c1rel_lat_h105k_c105k_seed23_4090g0_20260809` | sequential Human→Camera | `0.851383 / 0.231334` | `0.764674 / 1.278857` | `2.988533 / 3.088894` | `71.501466` |

| comparison | mode | metric (direction) | seed23 − seed17 mean delta (A−B) | 95% CI |
| --- | --- | --- | ---: | --- |
| C1REL / `sm_c1rel_lat_h105k_c105k_seed23_4090g0_20260809` − `C1REL / sm_c1rel_rawt0_lat_h105k_c105k_seed17_4090g0_20260804` | Direct-H | global MPJPE ↓ | `+0.007323` | `[-0.002722, +0.017260]` |
| C1REL / `sm_c1rel_lat_h105k_c105k_seed23_4090g0_20260809` − `C1REL / sm_c1rel_rawt0_lat_h105k_c105k_seed17_4090g0_20260804` | Direct-H | root ADE ↓ | `+0.007367` | `[-0.002356, +0.017262]` |
| C1REL / `sm_c1rel_lat_h105k_c105k_seed23_4090g0_20260809` − `C1REL / sm_c1rel_rawt0_lat_h105k_c105k_seed17_4090g0_20260804` | Direct-H | root-aligned MPJPE ↓ | `-0.000974` | `[-0.002982, +0.000998]` |
| C1REL / `sm_c1rel_lat_h105k_c105k_seed23_4090g0_20260809` − `C1REL / sm_c1rel_rawt0_lat_h105k_c105k_seed17_4090g0_20260804` | Direct-H | root FDE ↓ | `+0.012117` | `[-0.008465, +0.033353]` |
| C1REL / `sm_c1rel_lat_h105k_c105k_seed23_4090g0_20260809` − `C1REL / sm_c1rel_rawt0_lat_h105k_c105k_seed17_4090g0_20260804` | Direct-C | Camera ADE ↓ | `-0.028690` | `[-0.066201, +0.007895]` |
| C1REL / `sm_c1rel_lat_h105k_c105k_seed23_4090g0_20260809` − `C1REL / sm_c1rel_rawt0_lat_h105k_c105k_seed17_4090g0_20260804` | Direct-C | Camera FDE ↓ | `-0.034661` | `[-0.073829, +0.003691]` |
| C1REL / `sm_c1rel_lat_h105k_c105k_seed23_4090g0_20260809` − `C1REL / sm_c1rel_rawt0_lat_h105k_c105k_seed17_4090g0_20260804` | Direct-C | Camera rotation ↓ | `-0.411108` | `[-1.374512, +0.537709]` |
| C1REL / `sm_c1rel_lat_h105k_c105k_seed23_4090g0_20260809` − `C1REL / sm_c1rel_rawt0_lat_h105k_c105k_seed17_4090g0_20260804` | sequential | Human global MPJPE ↓ | `+0.007323` | `[-0.002544, +0.017585]` |
| C1REL / `sm_c1rel_lat_h105k_c105k_seed23_4090g0_20260809` − `C1REL / sm_c1rel_rawt0_lat_h105k_c105k_seed17_4090g0_20260804` | sequential | Human root ADE ↓ | `+0.007367` | `[-0.002262, +0.017228]` |
| C1REL / `sm_c1rel_lat_h105k_c105k_seed23_4090g0_20260809` − `C1REL / sm_c1rel_rawt0_lat_h105k_c105k_seed17_4090g0_20260804` | sequential | Human root-aligned MPJPE ↓ | `-0.000974` | `[-0.002958, +0.000970]` |
| C1REL / `sm_c1rel_lat_h105k_c105k_seed23_4090g0_20260809` − `C1REL / sm_c1rel_rawt0_lat_h105k_c105k_seed17_4090g0_20260804` | sequential | Human root FDE ↓ | `+0.012117` | `[-0.008529, +0.032887]` |
| C1REL / `sm_c1rel_lat_h105k_c105k_seed23_4090g0_20260809` − `C1REL / sm_c1rel_rawt0_lat_h105k_c105k_seed17_4090g0_20260804` | sequential | Camera ADE ↓ | `-0.001939` | `[-0.042527, +0.038016]` |
| C1REL / `sm_c1rel_lat_h105k_c105k_seed23_4090g0_20260809` − `C1REL / sm_c1rel_rawt0_lat_h105k_c105k_seed17_4090g0_20260804` | sequential | Camera FDE ↓ | `-0.004877` | `[-0.046033, +0.035224]` |
| C1REL / `sm_c1rel_lat_h105k_c105k_seed23_4090g0_20260809` − `C1REL / sm_c1rel_rawt0_lat_h105k_c105k_seed17_4090g0_20260804` | sequential | Camera rotation ↓ | `+0.149207` | `[-0.994513, +1.282847]` |

#### C1REL seed23 − seed17 distributional／semantic and decoded-Human delta supplement

这些是 `results.json` cohort aggregate 的算术差值（前者减后者），不是 semantic significance
test。seed-repeat `records.jsonl` 仅有 geometry 字段；因此所有 distributional／semantic 与
decoded-Human physical／kinematic 的 CI 均 unavailable，不能把 raw delta 升级为显著性或质量排名。

| comparison | mode | distributional／semantic aggregate Δ (A−B; no CI) | decoded-Human physical／kinematic aggregate Δ (A−B; mean / median / p90; no CI) |
| --- | --- | --- | --- |
| seed23 − seed17 | Direct-H | `TMR↑ +0.178457; FDTMR↓ −2.254105; cov↑ −0.011344; dens↑ −0.033663; prec↑ −0.009138; rec↑ +0.003945; R1↑ +0.000247; R2↑ +0.000987; R3↑ −0.004194; MM↓ −0.042379` | `bone-CV↔ +3.983e−10/−4.361e−11/+9.155e−10; joint speed↔ −1.882e−04/+5.933e−05/−4.063e−04; joint accel↔ −2.528e−04/−1.309e−04/+1.143e−04; joint jerk↔ −4.903e−04/−4.566e−04/−6.750e−04; root speed↔ −1.042e−04/−1.611e−04/+5.930e−04; root accel↔ −7.510e−05/−1.392e−04/+4.647e−04; root jerk↔ −1.343e−04/−1.448e−04/+3.131e−04; contact↔ +0.005235/+0.020578/0; skate↔ +4.215e−04/−1.534e−04/−1.219e−04` |
| seed23 − seed17 | Direct-C observed-H | `CLaTr↑ −0.375114; FDCLaTr↓ +2.178677; cov↑ −0.000002; dens↑ +0.009643; prec↑ −0.005922; rec↑ +0.000237; R1↑ −0.003454; R2↑ −0.001974; R3↑ −0.004688; MM↓ +0.108103; caption P/R/F1↑ +0.003062/−0.004659/−0.003476` | `—` (seed-repeat records do not contain decoded-Human physical fields) |
| seed23 − seed17 | sequential Human→Camera | `TMR↑ +0.178457; FDTMR↓ −2.254105; cov↑ −0.011344; dens↑ −0.033663; prec↑ −0.009138; rec↑ +0.003945; R1↑ +0.000247; R2↑ +0.000987; R3↑ −0.004194; MM↓ −0.042379; CLaTr↑ −0.451164; FDCLaTr↓ +1.280561; cov↑ +0.008897; dens↑ +0.033458; prec↑ −0.000501; rec↑ −0.006158; R1↑ +0.001480; R2↑ −0.003208; R3↑ +0.004688; MM↓ +0.149190; caption P/R/F1↑ +0.006958/+0.002385/+0.003849; r-FPD↓ −0.016820; Out↓ +0.000691` | `bone-CV↔ +3.983e−10/−4.361e−11/+9.155e−10; joint speed↔ −1.882e−04/+5.933e−05/−4.063e−04; joint accel↔ −2.528e−04/−1.309e−04/+1.143e−04; joint jerk↔ −4.903e−04/−4.566e−04/−6.750e−04; root speed↔ −1.042e−04/−1.611e−04/+5.930e−04; root accel↔ −7.510e−05/−1.392e−04/+4.647e−04; root jerk↔ −1.343e−04/−1.448e−04/+3.131e−04; contact↔ +0.005235/+0.020578/0; skate↔ +4.215e−04/−1.534e−04/−1.219e−04` |

审计裁决：三种 mode 的 cross-seed geometry CI 全部跨零，seed23 只提供 repeatability evidence，
不支持单 seed 的稳定 superiority。两次 run 都保持 `diagnostic_only=true`、
`promotion_eligible=false`，因为 canonical C1REL-derived Camera captions 仍暂停；因此本节
不能替代最终 caption-matched retraining，也不把 aggregate semantic 差异升级为显著性。


### Audited detail — original §3.18 PulpMotion native Stage2 matched available-data cohort

| display ID | canonical sm_ run alias | setting | goal |
| --- | --- | --- | --- |
| Pulp-native-210K | `sm_pulpmotion_repro162760_stage2_original_matched210k_seed17_5090g3_r2_20260809` | native PulpMotion joint path; matched available-data cohort `162,760/4,053`; `210K` steps | external system-boundary comparator, not a StoryMotion mode-equivalent arm |
| Pulp-native-step92,950 | `dit-xy-ddpm-p2ee3dj7 step92,950` | historical native Pulp checkpoint and official decoder | protocol-sanity provenance only |

每一行对应一个 native checkpoint boundary；Pulp 的 joint callback 不拆写成 StoryMotion Direct-H/Direct-C/sequential。

`sm_pulpmotion_repro162760_stage2_original_matched210k_seed17_5090g3_r2_20260809`
是外部 PulpMotion native-system boundary，不是 StoryMotion 组件消融。Pulp native pipeline 与
StoryMotion Stage2 的训练／评测 sample-ID 集分别 exact 匹配为 `162,760 / 4,053`，排序后集合差异
均为 `0`；这里的 `162,760` 是原始 `ae_train_split.txt` 173,912 条中能够同时物化必要文件的全部
样本，11,152 条因必要文件缺失被过滤。它不是 StoryMotion 训练集的更小子集，后续统一称
**matched available-data cohort**。Pulp 使用 native `config_dit_xyz`、online Stage1 encode 与
`camera64+projection64+human128` owner；StoryMotion 使用冻结 v9 cache 与
`human128+interaction16+camera48` owner，因此本节只能作同 cohort 的外部系统比较。

训练从 step 0 完成 `210,000` optimizer steps，effective batch=`128`，总 exposure=
`26,880,000`。在 exact `105,000` 与 `210,000` 边界原子保存并 reload-verify full-state checkpoint；
两者均包含 model、optimizer、scheduler、EMA、RNG、sampler 与 provenance。正式评测固定 physical
GPU3、seed17、batch128、50-step native sampler、`cfg_c=11 / cfg_z=0` 与显式 4,053 ordered IDs。
源 loader 的 `full_split_samples=4,054` 来自 split 文件末尾一个空行；正式 ID 唯一数与实际评测数
均为 4,053，空 ID 没有进入评测。

| version / run | native mode | N | train contract SHA-256 | eval contract SHA-256 | final checkpoint SHA-256 | output SHA-256 | report / audit SHA-256 |
| --- | --- | ---: | --- | --- | --- | --- | --- |
| PulpMotion native / `sm_pulpmotion_repro162760_stage2_original_matched210k_seed17_5090g3_r2_20260809` | joint generation only | 4,053 | `d6af214b7c5bf396ee30ce0f84909ef95b6c8127a4e008125b2ca4a1b91d941c` | `b47f75f4fdefb46658a4d5ea961bc64dfd6640d73b19f109fff0c47c9fd6142c` | `877c6b1a6fc78c6bcb20d936aaddde30a1c7a2d8b9729135c3d1cdd7573a4bd0` | `8da8d60e1faf3bf02c5a2e969893dbd4c3f295f04f558b00d0fd69e77772618a` | `d828082276cb61a5371b7f7bdbc3461f92253bc32c4f2053878a756cfc1ce973` / `5e2b629d330192650c2f09f46631935b46a78fd0a4f4e6f437d50598861c7d8a` |

Halfway checkpoint SHA-256 为
`c03f1f5dd12e72db9969f18fd6f7bb853cf77e4f41888db4396c23c018a66d47`；显式 ID JSONL SHA-256
为`e2c00e8f407b16785714ffd851c7994b778d303166d7ba0802600c13215dfb03`，formal order SHA-256
为`a6414865d9ab330fd559f6cf8a62bab7dc1ce4e4ba0dc4f301194c2c71f0eb21`。

| display ID / canonical run alias | TMR ↑ / FDTMR ↓ | CLaTr ↑ / FDCLaTr ↓ | caption F1 ↑ | r-FPD ↓ / Out ↓ | projection error ↓ / g-FPD ↓ |
| --- | --- | --- | ---: | --- | --- |
| PulpMotion native / `sm_pulpmotion_repro162760_stage2_original_matched210k_seed17_5090g3_r2_20260809` | `15.332323 / 375.383148` | `14.281564 / 275.958374` | `0.174287` | `11.336928 / 0.542279` | `1.893503 / 3.540139` |

同一 evaluator、SSD root、4,053 ordered IDs、`config_dit_xyz`、CFG、seed、batch 与 steps 上，官方
step `92,950` checkpoint＋其 owning official decoder 完成 protocol-sanity control：TMR／FDTMR=
`20.720825 / 403.221893`，CLaTr／FDCLaTr=`33.251812 / 90.779678`，caption F1=`0.468188`，
r-FPD／Out=`10.024635 / 0.467802`。control output SHA-256=
`5ef25d18ea91e76d748dde0ea30efb92b00e77204ffabbf34256d1be58b6e04f`。该 control 只排除
evaluator／data／cohort／config 路径失效，不用于 CFG 或 checkpoint 选择；因为 checkpoint 与 owning
decoder 同时不同，不能把差异因果归于训练权重或 decoder 中的任一方。

审计裁决：本次 `210K` native checkpoint 的弱指标是有效负结果，没有发现 checkpoint load、样本集、
顺序、配置或 evaluator mismatch。Pulp 只有一个 native joint generation path；Human／Camera callback
是同一 joint output 的 task slice，不是 StoryMotion Direct-H／Direct-C／sequential，也没有兼容的
StoryMotion decoded geometry artifact。因此只允许作显式标注 representation／decoder／mode 差异的
system-boundary comparison，不支持把 StoryMotion 三模式与该行写成单变量 superiority。


#### Historical full-cohort Pulp native sanity comparator (not StoryMotion mode-equivalent)

The original §3.11 boundary also recorded this full-cohort native PulpMotion checkpoint. It is retained for provenance and is not a StoryMotion Direct-H/Direct-C/sequential ranking row.

| display ID / canonical run alias | mode | N | F-distance ↓ / alignment ↑ | coverage / precision / recall ↑ | caption F1 ↑ | H global / root-aligned MPJPE ↓ m | Cam ADE / FDE ↓ m | Cam rotation ↓ deg | r-FPD ↓ / Out ↓ |
| --- | --- | ---: | --- | --- | ---: | --- | --- | ---: | --- |
| PulpMotion official / `dit-xy-ddpm-p2ee3dj7 step92,950` | native joint no-aux | 4,053 | 94.842 / 35.691 | 0.4833 / 0.6740 / 0.4431 | 0.4905 | — | — | — | 7.4040 / 0.3954 |
| PulpMotion official / `dit-xy-ddpm-p2ee3dj7 step92,950` | native joint aux | 4,053 | 93.269 / 37.777 | 0.4481 / 0.6442 / 0.4752 | 0.5127 | — | — | — | 5.8933 / 0.2847 |

The original render summary SHA-256 is `44dfa0a9a18fdc6eed492dc220cfae9606bc9f31832462699c3453ccb7e3bc57`; representation, decoder and native joint semantics remain different from StoryMotion.

### Audited detail — original §3.19 True-P2 matched symmetric Stage2 pure4,053 formal

| display ID | canonical sm_ run alias | setting | goal |
| --- | --- | --- | --- |
| True-P2-symmetric | `sm_p2_matched_symmetric_joint_fresh_h105k_joint105k_seed17_4090g1_20260809` | start from canonical Human teacher `105K` plus C0-LAT Camera initialization; jointly update Human+Camera for an additional `105K` steps | diagnostic factorization control; test whether relaxing Human freeze changes the Human/Camera trade-off |
| HREL-secondary-reference | `sm_p1_hrel_matched_lat_h105k_c105k_seed17_4090g1_20260809` | evaluator-matched HREL reference on the same ordered IDs | secondary field-wise reference only; not an exact initialization match |

每一行是一个 named run/reference；True-P2 remains `diagnostic_only` and `promotion_eligible=false`。

`sm_p2_matched_symmetric_joint_fresh_h105k_joint105k_seed17_4090g1_20260809`
是允许Camera loss更新Human参数的fresh symmetric-joint factorization control。它从与C0-LAT相同的
canonical Human `105K` teacher、Camera initialization、v9 non-causal Stage1 owner、cache、text、
model config和train/eval IDs出发，再共同更新Human与Camera `105,000` optimizer steps；endpoint
checkpoint同时拥有Human与Camera EMA，`human_frozen_after_teacher=false`。本节只报告预注册的
Direct-H、Direct-C和sequential；`joint_parallel=false`、`is_causal=false`、
`diagnostic_only=true`、`promotion_eligible=false`。

这里的 `symmetric` 指两条独立的 Human／Camera denoising flow 共同优化
`L_H + L_C^HC`，不是把 `h latent、c latent、I latent` concat 后交给一个 joint denoiser，
也没有重新开放 `joint_parallel`。训练时 HC Camera-loss route 只接收 predicted-clean Human；
formal Camera generation 却设置 `observed_human=true`，因此训练与评测 route 并不完全相同。
step-20 的 Camera-only gradient probe 为 `||∇_H L_C||₂=0.002785`、
`||∇_C L_C||₂=0.485446`，只能证明 Camera loss 可达两组参数，不能证明发生了 gradient stealing；
teacher under-convergence、梯度竞争等具体原因目前均未被该 probe 单独证实。

训练contract SHA-256=`b57ef7103a23aca806a61f9ea50d4ff585a117e46b32278000e8e0950a59aa51`，
GPU preflight SHA-256=`e55731e20eb2ac27f0e79e32035f1f13f7f724765245ce06c819f85c2cef3f9f`，
final full-state checkpoint SHA-256=`8f8d50fd3b1cbf6e665537cfa616b4677d9ee00bf020c6fab92efb5e63e80b6b`，
train manifest SHA-256=`c64e2e3dd351a72abc87d1d8886a2e38941cf36e387cabcbfddc3a4a01ac98ec`。
三接口使用pure-test `N=4,053`、ordered-ID SHA-256=
`a0d7627ee827e36a229d33f9975f8417ae78b504cd5a6db1edf62cb1a9266b93`、seed17、
eval/decode batch=`128/1`、shifted-sigma explicit Euler50、CFG=1、eta=0和同一owning decoder
SHA-256=`51233f6a032c779e66b6eed4bb22b7f61c41d9b4a5a0a1ffc7dade7d3d86d4df`。

| version / run | mode | evaluation contract SHA-256 | fixed samples SHA-256 | records SHA-256 | results SHA-256 | manifest SHA-256 |
| --- | --- | --- | --- | --- | --- | --- |
| True-P2 / `sm_p2_matched_symmetric_joint_fresh_h105k_joint105k_seed17_4090g1_20260809` | Direct-H | `abda49bef92d00569113f4cec4966875a06c79445c8c897edd48d80f7f8ccf7d` | `20fd7b62968136d6353786cc745700f970241678468fbacbdf2a3c3b32f1832e` | `ff310656f1b3b53ffa3c875e60129886b052efe249f880e0c0d8f7b255731471` | `58d0f4a7edd00c90341b95cccc4bd50dfa400ab474253d4685197c938c420bcf` | `548fb67776aa5a4b306fceefe2ee20fc59d8cd4cc260f55054eaf75aef525df6` |
| True-P2 / `sm_p2_matched_symmetric_joint_fresh_h105k_joint105k_seed17_4090g1_20260809` | Direct-C observed-H | `100938caf49c48d6b4e905746ca921787a44a9a1cc93987d0bda5b1c2d803a65` | `5cd9f859e9299d6268c6ac2ab39b1c72a734088cb5bf22eef24590dbffb269ba` | `8f1c4132ccdf1042e147e7bf2be93f39811c7a90de5fc6e92805db19a703ec9b` | `009dc102d05e4b624008ab488769941c8e89a19f448fe30e2f761a19d91b874d` | `42d64dfd3a3864ea73417acfcad6f1e6b165408a67cf8580735d24b31872fd30` |
| True-P2 / `sm_p2_matched_symmetric_joint_fresh_h105k_joint105k_seed17_4090g1_20260809` | sequential Human→Camera | `675f63080d6a43f6ab35ab0e20f0940a7a0dac3fea4373f421c535aab43c860a` | `ed0070b0d3c344bac9716717bbfb5a22a23c2bbb0b843c8fe62ca53ca2662c48` | `f32596d585e144420ff6ae58a24db2f2ed3ef1645461006624225aa0bf578d78` | `692eaf106db47dcf7fffab40d7058bf8e30ae08e5c6e0eb28520d15e1115d58b` | `89fff412bbb9e927d4dad5e40b5074b1fa8ca1e866679c65a6e93a679e88d577` |

#### Aggregate metrics

| display ID / canonical run alias | mode | Human TMR ↑ / FDTMR ↓ | Camera CLaTr ↑ / FDCLaTr ↓ | caption F1 ↑ | r-FPD ↓ / Out ↓ |
| --- | --- | --- | --- | ---: | --- |
| True-P2 / `sm_p2_matched_symmetric_joint_fresh_h105k_joint105k_seed17_4090g1_20260809` | Direct-H | `18.013281 / 97.553619` | — | — | — |
| True-P2 / `sm_p2_matched_symmetric_joint_fresh_h105k_joint105k_seed17_4090g1_20260809` | Direct-C observed-H | observed-H `15.659584 / 7.944044` | `37.851692 / 131.628693` | `0.451288` | `3.188230 / 0.225102` |
| True-P2 / `sm_p2_matched_symmetric_joint_fresh_h105k_joint105k_seed17_4090g1_20260809` | sequential Human→Camera | `18.013281 / 97.553619` | `40.078587 / 104.280891` | `0.499214` | `2.024074 / 0.157821` |

#### Paired geometry and decoded-Human diagnostics

| display ID / canonical run alias | mode | Human global / root-aligned MPJPE ↓ m | Human root ADE / FDE ↓ m | Camera center ADE / FDE ↓ m | Camera rotation ↓ deg |
| --- | --- | --- | --- | --- | ---: |
| True-P2 / `sm_p2_matched_symmetric_joint_fresh_h105k_joint105k_seed17_4090g1_20260809` | Direct-H | `0.827778 / 0.222009` | `0.746442 / 1.252167` | — | — |
| True-P2 / `sm_p2_matched_symmetric_joint_fresh_h105k_joint105k_seed17_4090g1_20260809` | Direct-C observed-H | — | — | `2.025185 / 2.145800` | `49.877689` |
| True-P2 / `sm_p2_matched_symmetric_joint_fresh_h105k_joint105k_seed17_4090g1_20260809` | sequential Human→Camera | `0.827778 / 0.222009` | `0.746442 / 1.252167` | `2.476393 / 2.583847` | `64.814241` |

Direct-H与sequential复用同一Human output。decoded-Human generated mean为root jerk=`0.016280`、
foot skate=`0.027705`、joint jerk=`0.033140`、contact=`0.596234`；这些是no-reference
kinematic heuristics，不是calibrated physical-validity分数。

#### Evaluator-matched P1 secondary bootstrap and causal boundary

审计还以P1 HREL `sm_p1_hrel_matched_lat_h105k_c105k_seed17_4090g1_20260809`作为
同ordered IDs、evaluator、batch、sampler、cache、text、Stage1 owner和model-config的secondary
reference，对逐样本geometry做10,000次paired bootstrap，差值定义为`P2 − P1`。
审计JSON路径为
canonical alias `sm_p2_matched_symmetric_joint_fresh_h105k_joint105k_seed17_4090g1_20260809/pure4053_formal_20260810/audit_true_p2_vs_hrel_seed17.json`（exact immutable path见[[StoryMotion-folder-rename-map]]），
SHA-256=`01cfc929e8c06416d94e68bb2c7d68800fee37ec4000ac95520d3e23ee7a4af1`；审计实现
SHA-256=`f0962f69397b6bc1690b6b52b1e2dc7ce1d2f8941807cb00fb61ad3c810665bd`。

| version / comparison | mode | metric (direction) | mean delta (A−B) | 95% CI |
| --- | --- | --- | ---: | --- |
| True-P2 / `sm_p2_matched_symmetric_joint_fresh_h105k_joint105k_seed17_4090g1_20260809` − P1 HREL / `sm_p1_hrel_matched_lat_h105k_c105k_seed17_4090g1_20260809` | Direct-H | global MPJPE ↓ | `-0.020787` | `[-0.031423, -0.010182]` |
| True-P2 / `sm_p2_matched_symmetric_joint_fresh_h105k_joint105k_seed17_4090g1_20260809` − P1 HREL / `sm_p1_hrel_matched_lat_h105k_c105k_seed17_4090g1_20260809` | Direct-H | root ADE ↓ | `-0.015894` | `[-0.026291, -0.005231]` |
| True-P2 / `sm_p2_matched_symmetric_joint_fresh_h105k_joint105k_seed17_4090g1_20260809` − P1 HREL / `sm_p1_hrel_matched_lat_h105k_c105k_seed17_4090g1_20260809` | Direct-H | root-aligned MPJPE ↓ | `-0.008937` | `[-0.010776, -0.007107]` |
| True-P2 / `sm_p2_matched_symmetric_joint_fresh_h105k_joint105k_seed17_4090g1_20260809` − P1 HREL / `sm_p1_hrel_matched_lat_h105k_c105k_seed17_4090g1_20260809` | Direct-H | root FDE ↓ | `-0.026080` | `[-0.048353, -0.003876]` |
| True-P2 / `sm_p2_matched_symmetric_joint_fresh_h105k_joint105k_seed17_4090g1_20260809` − P1 HREL / `sm_p1_hrel_matched_lat_h105k_c105k_seed17_4090g1_20260809` | Direct-C | Camera ADE ↓ | `+0.600418` | `[+0.546570, +0.653915]` |
| True-P2 / `sm_p2_matched_symmetric_joint_fresh_h105k_joint105k_seed17_4090g1_20260809` − P1 HREL / `sm_p1_hrel_matched_lat_h105k_c105k_seed17_4090g1_20260809` | Direct-C | Camera FDE ↓ | `+0.635766` | `[+0.577747, +0.693091]` |
| True-P2 / `sm_p2_matched_symmetric_joint_fresh_h105k_joint105k_seed17_4090g1_20260809` − P1 HREL / `sm_p1_hrel_matched_lat_h105k_c105k_seed17_4090g1_20260809` | Direct-C | Camera rotation ↓ | `+19.839824` | `[+18.439271, +21.248590]` |
| True-P2 / `sm_p2_matched_symmetric_joint_fresh_h105k_joint105k_seed17_4090g1_20260809` − P1 HREL / `sm_p1_hrel_matched_lat_h105k_c105k_seed17_4090g1_20260809` | sequential | Camera ADE ↓ | `-0.417430` | `[-0.461591, -0.373619]` |
| True-P2 / `sm_p2_matched_symmetric_joint_fresh_h105k_joint105k_seed17_4090g1_20260809` − P1 HREL / `sm_p1_hrel_matched_lat_h105k_c105k_seed17_4090g1_20260809` | sequential | Camera FDE ↓ | `-0.416222` | `[-0.462050, -0.371399]` |
| True-P2 / `sm_p2_matched_symmetric_joint_fresh_h105k_joint105k_seed17_4090g1_20260809` − P1 HREL / `sm_p1_hrel_matched_lat_h105k_c105k_seed17_4090g1_20260809` | sequential | Camera rotation ↓ | `-6.345560` | `[-7.741426, -4.946408]` |

#### True-P2 − P1 HREL distributional／semantic and decoded-Human delta supplement

这些是两份 `results.json` 的 cohort aggregate 算术差值（P2 − P1），不是 paired semantic test。
P1/P2 audit records 仅有 geometry，故 distributional／semantic 与 decoded-Human physical／kinematic
均标为 `CI unavailable`；physical／contact／skate 的 `↔` 仅表示 no-reference diagnostic，
不表示更优方向。

| comparison | mode | distributional／semantic aggregate Δ (A−B; no CI) | decoded-Human physical／kinematic aggregate Δ (A−B; mean / median / p90; no CI) |
| --- | --- | --- | --- |
| True-P2 − P1 HREL | Direct-H | `TMR↑ +0.658814; FDTMR↓ −2.700783; cov↑ +0.019254; dens↑ +0.001386; prec↑ −0.010858; rec↑ −0.001965; R1↑ −0.004935; R2↑ 0; R3↑ −0.003208; MM↓ −0.189736` | `bone-CV↔ −1.093e−09/+5.621e−10/−3.468e−09; joint speed↔ −0.001764/−0.000492/−0.004523; joint accel↔ −0.002335/−0.001295/−0.006576; joint jerk↔ −0.003952/−0.002102/−0.009715; root speed↔ −0.000811/+0.000176/−0.002399; root accel↔ −0.000591/−0.000098/−0.002095; root jerk↔ −0.000773/−0.000099/−0.002281; contact↔ −0.005283/−0.008054/0; skate↔ −0.002785/−0.000929/−0.006704` |
| True-P2 − P1 HREL | Direct-C observed-H | `CLaTr↑ −19.386640; FDCLaTr↓ +109.429200; cov↑ −0.294076; dens↑ −0.250741; prec↑ −0.081655; rec↑ −0.169995; R1↑ −0.023439; R2↑ −0.049593; R3↑ −0.070812; MM↓ +5.317184; caption P/R/F1↑ −0.197904/−0.278120/−0.289294; r-FPD↓ +2.299150; Out↓ +0.120143` | `—` (`decoded_human_physical=null` for Direct-C) |
| True-P2 − P1 HREL | sequential Human→Camera | `TMR↑ +0.658814; FDTMR↓ −2.700783; cov↑ +0.019254; dens↑ +0.001386; prec↑ −0.010858; rec↑ −0.001965; R1↑ −0.004935; R2↑ 0; R3↑ −0.003208; MM↓ −0.189736; CLaTr↑ −15.508300; FDCLaTr↓ +74.133560; cov↑ −0.202545; dens↑ −0.203207; prec↑ −0.068328; rec↑ −0.154705; R1↑ −0.022946; R2↑ −0.039230; R3↑ −0.053294; MM↓ +4.290628; caption P/R/F1↑ −0.163090/−0.210109/−0.202499; r-FPD↓ +1.517728; Out↓ +0.081151` | `bone-CV↔ −1.093e−09/+5.621e−10/−3.468e−09; joint speed↔ −0.001764/−0.000492/−0.004523; joint accel↔ −0.002335/−0.001295/−0.006576; joint jerk↔ −0.003952/−0.002102/−0.009715; root speed↔ −0.000811/+0.000176/−0.002399; root accel↔ −0.000591/−0.000098/−0.002095; root jerk↔ −0.000773/−0.000099/−0.002281; contact↔ −0.005283/−0.008054/0; skate↔ −0.002785/−0.000929/−0.006704` |

P1 HREL使用不同的Human teacher／Stage2 checkpoint初始化，因此以上paired CI只说明在同一评测器
与采样协议下的field-wise差异，**不是**严格的factorization因果效应。与P2 exact初始化相同的
C0-LAT现已通过同一`128/1` evaluator/noise合同并完成paired audit，见§3.21：结论仍是mixed
Pareto，P2的Human与sequential Camera geometry更低，但Direct-C Camera geometry更高，且两种
Camera接口的semantic／framing cohort aggregate回退。§3.21的source-row replay同时证明C0
sequential依赖训练未覆盖且会改变全部样本Camera输出的row1；因此historical P2−C0 sequential
对照需披露这一C1-derived实现covariate。它不对应StoryMotion的双来源能力主张；不能写“protected
asymmetry逐字段全面优于symmetric joint”的原因是metric本身为mixed Pareto，而不是row1造成核心claim缺口。


### Audited detail — original §3.20 C1REL-noI16 seed23 full-cohort repeat

| display ID | canonical sm_ run alias | setting | goal |
| --- | --- | --- | --- |
| C1REL-noI16-seed23 | `sm_c1rel_noi16_lat_h105k_c105k_seed23_4090g0_20260810` | fresh training seed23；C1REL-C48 owner with Interaction16 removed；raw Pulp Camera captions；three active asymmetric modes | independently repeat the Interaction16 component arm |
| full-C1REL-seed23 reference | `sm_c1rel_lat_h105k_c105k_seed23_4090g0_20260809` | sealed full-C1REL seed23 result from §3.17 | same-seed component reference |

每行是一个named arm/reference。noI16 seed23完成Human `105K`＋Camera `105K`，final
global step=`210K`；checkpoint tensor audit确认Camera input/output为`48D`、source embedding为
`[2,512]`、Human为`128D`且`is_causal=false`。正式评测只含Direct-H、Direct-C与sequential，
`joint_parallel=false`；pure-test `N=4,053`，ordered-ID SHA-256=
`a0d7627ee827e36a229d33f9975f8417ae78b504cd5a6db1edf62cb1a9266b93`，
eval/decode batch=`128/1`，shifted-sigma explicit Euler50、eta=0、CFG=1、固定evaluation seed17。
训练seed仍为23；固定evaluation seed用于与既有reference共享noise，不改写run identity。

noI16 seed23 checkpoint SHA-256=
`6f1ac203689c9df4af956eb5b78fe97a1669688c4d87a86908cc8198d20c5f3b`，Human teacher
SHA-256=`8603339b3e4526d003c2b1aa740e969664ee9d0a79f29eeaa94ea7a184f1497d`，owning
decoder SHA-256=`b8b572d5562f0946896ac9fc6af866d9ea636c9460e461628b81bb2d2329be0b`，
training contract SHA-256=`66eaa2ae328de6870f0e84e6925c904ac673a1b21e94468d2c03ca1e2b015442`。
sealed audit canonical alias为
`sm_c1rel_noi16_lat_h105k_c105k_seed23_4090g0_20260810_formal_pure4053_r1/sealed_audit_noi16_seed23.json`
（exact immutable path见[[StoryMotion-folder-rename-map]]），SHA-256=
`67485dc4ddb30669a3e4272745bb2d33bdbd940556715ff2599489f43e567840`。

#### Formal artifact identity

| version / run | mode | evaluation contract SHA-256 | fixed samples SHA-256 | records SHA-256 | results SHA-256 | manifest SHA-256 |
| --- | --- | --- | --- | --- | --- | --- |
| C1REL-noI16-seed23 / `sm_c1rel_noi16_lat_h105k_c105k_seed23_4090g0_20260810` | Direct-H | `fbdb923e1f85944aad89ca273e3b07f2335fd471d708015acf56852d32c1d089` | `dc2c522cf745e1439a8731989e8092e6492cec58bffa86e89344c411e58848f4` | `2b02d782980d6dab68082466d4b95d06865e7b4af0835a310b2a67f3a806abe3` | `cf1b7ae0125586775bdf052cc909f7763dca85873660a74db859aa970d6aa716` | `89f4338d1461bcdf2d66ede731a1a8c95baa52136a2a0fb35b38e03bbf126b66` |
| C1REL-noI16-seed23 / `sm_c1rel_noi16_lat_h105k_c105k_seed23_4090g0_20260810` | Direct-C observed-H | `2613be6b0cb5c3446128c7d9e7a2e1e1a7114cb3d82421a4eef7e9128e6a0339` | `61da766498135baa21e8ca03a6b775d6a923612e2c9ad5b560fb95b88fb5cb6c` | `8f4fae7e02281c51afe4bfaee703891105a187e3d3de99723726b4339898a2b5` | `49b9924a9b5c09b70042a76a1894f0db8684f5ebe76419858a89486d0a11bed9` | `0680f0ff5afbd9f1a8312539f05ec54b103ed9e800db08feade6b951f056e596` |
| C1REL-noI16-seed23 / `sm_c1rel_noi16_lat_h105k_c105k_seed23_4090g0_20260810` | sequential Human→Camera | `9ea1f830a9560d48de0679019808aab92f6d96b1e89a974607b8ec3505727a24` | `a389de5b9fa5ba2624d76f7ae7f4a98990a4c9899af071cf80598b90146cc0eb` | `d060ff384e63db19cce6976994f4665ff72ae3a7d14bdd37e1436e5575b151e9` | `52c456c4b4cd3b2159c3cd2a63d880ac3b21e45776194d39e29eafeb0669651c` | `909ab0b5be4eed2cd9892bccff635d19617fee70cab935d08991a560df137033` |

#### Aggregate metrics and paired geometry

| version / run | mode | Human TMR ↑ / FDTMR ↓ | Camera CLaTr ↑ / FDCLaTr ↓ | observed-H TMR ↑ / FDTMR ↓ | caption F1 ↑ | r-FPD ↓ / Out ↓ |
| --- | --- | --- | --- | --- | ---: | --- |
| C1REL-noI16-seed23 / `sm_c1rel_noi16_lat_h105k_c105k_seed23_4090g0_20260810` | Direct-H | `17.800165 / 93.129906` | — | — | — | — |
| C1REL-noI16-seed23 / `sm_c1rel_noi16_lat_h105k_c105k_seed23_4090g0_20260810` | Direct-C observed-H | — | `43.644409 / 66.523109` | `15.575075 / 9.833646` | `0.541792` | `8.256357 / 0.440641` |
| C1REL-noI16-seed23 / `sm_c1rel_noi16_lat_h105k_c105k_seed23_4090g0_20260810` | sequential Human→Camera | `17.800165 / 93.129906` | `40.343426 / 92.991791` | — | `0.492550` | `8.533516 / 0.438627` |

| version / run | mode | Human global / root-aligned MPJPE ↓ m | Human root ADE / FDE ↓ m | Camera center ADE / FDE ↓ m | Camera rotation ↓ deg |
| --- | --- | --- | --- | --- | ---: |
| C1REL-noI16-seed23 / `sm_c1rel_noi16_lat_h105k_c105k_seed23_4090g0_20260810` | Direct-H | `0.850149 / 0.229023` | `0.764463 / 1.274428` | — | — |
| C1REL-noI16-seed23 / `sm_c1rel_noi16_lat_h105k_c105k_seed23_4090g0_20260810` | Direct-C observed-H | — | — | `1.664651 / 1.775128` | `41.231200` |
| C1REL-noI16-seed23 / `sm_c1rel_noi16_lat_h105k_c105k_seed23_4090g0_20260810` | sequential Human→Camera | `0.850149 / 0.229023` | `0.764463 / 1.274428` | `2.627770 / 2.727306` | `66.708058` |

Direct-H与sequential共享同一Human输出；teacher regression max-abs=`4.1008e-05`。上述semantic／
framing字段是cohort aggregate，没有逐样本semantic bootstrap单位。

#### Same-seed component comparison and repeat boundary

相对§3.17的sealed full-C1REL seed23，删除Interaction16后，Direct-C的CLaTr／FDCLaTr差值为
`-17.965992 / +46.161398`，sequential为`-20.566078 / +74.389177`；caption F1分别变化
`-0.230566 / -0.273797`，r-FPD分别变化`+6.929227 / +7.862639`。四个预声明方向
（两模式CLaTr下降、FDCLaTr上升）全部通过，但这些仍是aggregate direction gate，不是semantic显著性检验。

下表差值均为`noI16 seed23 − full-C1REL seed23`；每个cell为
`mean delta [95% CI]`，使用exact ordered sample执行10,000次paired bootstrap。

| version / comparison | mode | metric group（均↓） | mean delta [95% CI] |
| --- | --- | --- | --- |
| C1REL-noI16-seed23 / `sm_c1rel_noi16_lat_h105k_c105k_seed23_4090g0_20260810` − full-C1REL-seed23 / `sm_c1rel_lat_h105k_c105k_seed23_4090g0_20260809` | Direct-H | Human global MPJPE；root ADE；root-aligned MPJPE；root FDE | `-0.001234 [-0.012370, +0.009972]`; `-0.000211 [-0.011291, +0.010428]`; `-0.002311 [-0.004270, -0.000336]`; `-0.004430 [-0.027025, +0.017701]` |
| C1REL-noI16-seed23 / `sm_c1rel_noi16_lat_h105k_c105k_seed23_4090g0_20260810` − full-C1REL-seed23 / `sm_c1rel_lat_h105k_c105k_seed23_4090g0_20260809` | Direct-C observed-H | Camera ADE；Camera FDE；Camera rotation | `-0.015999 [-0.064162, +0.033819]`; `+0.024299 [-0.025927, +0.074107]`; `+5.741240 [+4.555008, +6.938256]` |
| C1REL-noI16-seed23 / `sm_c1rel_noi16_lat_h105k_c105k_seed23_4090g0_20260810` − full-C1REL-seed23 / `sm_c1rel_lat_h105k_c105k_seed23_4090g0_20260809` | sequential Human | Human global MPJPE；root ADE；root-aligned MPJPE；root FDE | `-0.001234 [-0.012323, +0.009520]`; `-0.000211 [-0.011255, +0.010696]`; `-0.002311 [-0.004272, -0.000339]`; `-0.004430 [-0.026642, +0.017403]` |
| C1REL-noI16-seed23 / `sm_c1rel_noi16_lat_h105k_c105k_seed23_4090g0_20260810` − full-C1REL-seed23 / `sm_c1rel_lat_h105k_c105k_seed23_4090g0_20260809` | sequential Camera | Camera ADE；Camera FDE；Camera rotation | `-0.360764 [-0.410682, -0.312155]`; `-0.361588 [-0.411744, -0.312594]`; `-4.793408 [-6.088850, -3.485564]` |

裁决是**semantic／framing collapse复现，但geometry为mixed Pareto**：Direct-C rotation显著更高，
sequential三项Camera geometry反而显著更低；Human除小幅root-aligned项外没有稳定差异。因此结果支持
Interaction16在两seed的matched component protocol中具有可重复的Camera semantic／framing贡献，
不支持“所有字段都退化”或普遍必要性。full-C1REL与noI16会按声明的组件干预一起改变Stage1
representation owner、owning decoder、Camera width和参数量；该比较不是Stage2-only单变量消融。

noI16 seed23相对seed17的全部paired geometry CI跨零，但seed17 evaluation contract绑定的旧training-contract
SHA=`32f39697f55d3bdc71cd8ecec54be771805547d2d19a6ce42da2e55f83478dd9`在同一路径已变为
`6edca8b2d99ffa4807a0c9186291f13d43d8bd39ffc618dc361cf6abd3b4daf8`，run root中没有旧bytes；故该
cross-seed结果只作provenance-limited secondary repeat，不称fully hash-matched。这个例外不影响上述
same-seed noI16 seed23 vs sealed full-C1REL seed23 primary gate。另有三个保留的执行例外：训练合同预测
decode batch=`64`而正式执行为`1`；run-local `meta.json`遗留C64架构标签而contract／checkpoint tensor
均为Camera48；训练seed23使用固定evaluation seed17。所有原bytes均不回写。


### Audited detail — original §3.21 exact-initialization C0-LAT reference and source-row diagnostic

| display ID | canonical sm_ run alias | setting | evidence role |
| --- | --- | --- | --- |
| exact-init C0-LAT reference | `sm_c0_lat_true_p2_reference_seed17_4090g1_20260810` | exact legacy C0-LAT Camera `105K` EMA and canonical frozen Human teacher; True-P2 data/evaluator/sampler boundary | full-cohort formal-protocol reference; diagnostic-only and promotion-ineligible |
| source-row replay | `sm_c0_lat_true_p2_reference_seed17_4090g1_20260810/diagnostic_source_row01` | fixed sequential samples/noise; only Camera `source_id` changes from untrained row1 to trained row0 | full-cohort sensitivity diagnostic; not a formal fourth mode |

三种正式模式均使用pure-test `N=4,053`、ordered-ID SHA-256=
`a0d7627ee827e36a229d33f9975f8417ae78b504cd5a6db1edf62cb1a9266b93`、
eval/decode batch=`128/1`、shifted-sigma explicit Euler50、eta=0、CFG=1和相同逐分支确定性
noise。`is_causal=false`、`joint_parallel=false`，不存在evolving-H或第四种formal mode。
checkpoint SHA-256=`b7759ea686ddc8bd9abc2db2b3a6f74421bf3f6033274863d715f58b0d66b96a`，
canonical Human teacher SHA-256=`3efd59481f8052b401889fce6559e31f96cb88f51dfb6c466464cf05ec6c2c50`，
owning decoder SHA-256=`51233f6a032c779e66b6eed4bb22b7f61c41d9b4a5a0a1ffc7dade7d3d86d4df`。
正式实现绑定clean commit `989693955ecbfc3c4cfe6f7c326d981e5f3366d4`；legacy C0 identity contract
SHA-256=`1d05bef03cf10b839bb75018cd6ca0efff8d0a4696f6cafcbbafb028fb69e326`，
True-P2 contract SHA-256=`b57ef7103a23aca806a61f9ea50d4ff585a117e46b32278000e8e0950a59aa51`
在这里仅拥有data／evaluator／sampler boundary，不改写C0训练语义。

#### Formal artifact identity

| version / run | mode | evaluation contract SHA-256 | fixed samples SHA-256 | records SHA-256 | results SHA-256 | manifest SHA-256 |
| --- | --- | --- | --- | --- | --- | --- |
| exact-init C0-LAT / `sm_c0_lat_true_p2_reference_seed17_4090g1_20260810` | Direct-H | `93e2062cbe715136887024d9b7078dabdb4b6832a4199d6498e4cf495b11ee9b` | `ec467d6931fb9fc3391e0b0bfda8f6fc2e431a1f3d4f9b2c029d82aa9a26636e` | `8b8123ff1770b19c1b5efde4135193a88d702e5c5614e4b6f4ade796f3eb5e1d` | `b932d966031af331de497989654ec837aa88deae3dcf1d02fb80e9d81ecfbf2a` | `dd63e5ce90b8941faae513b6518152a3e49e25f5834e40c45067d60ba5a856d5` |
| exact-init C0-LAT / `sm_c0_lat_true_p2_reference_seed17_4090g1_20260810` | Direct-C observed-H, source row0 | `701a089024c30a5e00c990aec891a53d98bc186140d7108ab3e5e41346ed5ad4` | `7e295949a939db06ea5ed0d6d9bf1091f9f085121e4457799500009b8c89a0fe` | `6a3150c2d8d54dda1777977f1bf72a40406408904e447c632969a4da43d90125` | `bf85dd04c423c33262bbe8fea61b22f14d0f3bdfa4c1ad3cff31cf936c56c6a6` | `c37b057cf1ce7c7a134a5cc22e4e4152235c03a564b59f6905b4dba00028a1da` |
| exact-init C0-LAT / `sm_c0_lat_true_p2_reference_seed17_4090g1_20260810` | sequential Human→Camera, source row1 | `1ff617dc0b1c328dfd913a9d87b15391121466668e245e8020864579d88fb6d3` | `d1e7059f360861cfc6dd09b6fc0a81c25909440176467a2d6f57ea0374400f3c` | `6375b261fc4d972de02cc62f869a3f70a17ebeb26a465d14f4c8c55ed4b0b808` | `fe6670ff41644c86084a680210ca821493b9854dac4aa16897534f1ce5165fe1` | `f575f14cb432d0d8b67b294d9c6baa943c4d53e592ae6efbb1109d62b9f9f674` |

#### Formal metrics

| version / run | mode | Human TMR ↑ / FDTMR ↓ | Camera CLaTr ↑ / FDCLaTr ↓ | caption F1 ↑ | r-FPD ↓ / Out ↓ |
| --- | --- | --- | --- | ---: | --- |
| exact-init C0-LAT / `sm_c0_lat_true_p2_reference_seed17_4090g1_20260810` | Direct-H | `17.354467 / 100.254402` | — | — | — |
| exact-init C0-LAT / `sm_c0_lat_true_p2_reference_seed17_4090g1_20260810` | Direct-C observed-H, source row0 | observed-H `15.659584 / 7.944044` | `56.586727 / 22.163630` | `0.731021` | `0.799310 / 0.100393` |
| exact-init C0-LAT / `sm_c0_lat_true_p2_reference_seed17_4090g1_20260810` | sequential Human→Camera, source row1 | `17.354467 / 100.254402` | `55.393429 / 29.761435` | `0.685826` | `0.507365 / 0.078331` |

| version / run | mode | Human global / root-aligned MPJPE ↓ m | Human root ADE / FDE ↓ m | Camera center ADE / FDE ↓ m | Camera rotation ↓ deg |
| --- | --- | --- | --- | --- | ---: |
| exact-init C0-LAT / `sm_c0_lat_true_p2_reference_seed17_4090g1_20260810` | Direct-H | `0.848565 / 0.230946` | `0.762336 / 1.278247` | — | — |
| exact-init C0-LAT / `sm_c0_lat_true_p2_reference_seed17_4090g1_20260810` | Direct-C observed-H, source row0 | — | — | `1.404148 / 1.487332` | `30.184385` |
| exact-init C0-LAT / `sm_c0_lat_true_p2_reference_seed17_4090g1_20260810` | sequential Human→Camera, source row1 | `0.848565 / 0.230946` | `0.762336 / 1.278247` | `2.896272 / 2.993438` | `70.880520` |

Direct-H与sequential Human逐元素exact，max-abs=`0`。

#### True-P2 minus exact-init C0-LAT paired audit

下表为`True-P2 − exact-init C0-LAT`的`mean delta [95% percentile CI]`；均使用同一4,053个
ordered IDs、10,000次matched-index bootstrap、seed=`260812`。列内metric均为↓。

| version / comparison | mode | metric group | mean delta [95% CI] |
| --- | --- | --- | --- |
| True-P2 / `sm_p2_matched_symmetric_joint_fresh_h105k_joint105k_seed17_4090g1_20260809` − exact-init C0-LAT / `sm_c0_lat_true_p2_reference_seed17_4090g1_20260810` | Direct-H | Human global MPJPE; root ADE; root-aligned MPJPE; root FDE | `-0.020787 [-0.031666, -0.010184]`; `-0.015894 [-0.026625, -0.005393]`; `-0.008937 [-0.010747, -0.007137]`; `-0.026080 [-0.048386, -0.004738]` |
| True-P2 / `sm_p2_matched_symmetric_joint_fresh_h105k_joint105k_seed17_4090g1_20260809` − exact-init C0-LAT / `sm_c0_lat_true_p2_reference_seed17_4090g1_20260810` | Direct-C observed-H | Camera ADE; Camera FDE; Camera rotation | `+0.621037 [+0.567702, +0.674284]`; `+0.658468 [+0.601490, +0.715619]`; `+19.693304 [+18.281702, +21.124427]` |
| True-P2 / `sm_p2_matched_symmetric_joint_fresh_h105k_joint105k_seed17_4090g1_20260809` − exact-init C0-LAT / `sm_c0_lat_true_p2_reference_seed17_4090g1_20260810` | sequential Human | Human global MPJPE; root ADE; root-aligned MPJPE; root FDE | `-0.020787 [-0.031421, -0.010356]`; `-0.015894 [-0.026467, -0.005252]`; `-0.008937 [-0.010755, -0.007113]`; `-0.026080 [-0.048255, -0.003953]` |
| True-P2 / `sm_p2_matched_symmetric_joint_fresh_h105k_joint105k_seed17_4090g1_20260809` − exact-init C0-LAT / `sm_c0_lat_true_p2_reference_seed17_4090g1_20260810` | sequential Camera | Camera ADE; Camera FDE; Camera rotation | `-0.419879 [-0.464221, -0.376540]`; `-0.409590 [-0.455058, -0.364457]`; `-6.066279 [-7.409024, -4.671518]` |

全部14项geometry CI不跨零，但方向构成mixed Pareto。P2相对C0的aggregate差值为：Direct-H
`TMR +0.658814 / FDTMR -2.700783`；Direct-C
`CLaTr -18.735035 / FDCLaTr +109.465063 / caption F1 -0.279733 / r-FPD +2.388920 / Out +0.124709`；
sequential `CLaTr -15.314842 / FDCLaTr +74.519457 / caption F1 -0.186612 / r-FPD +1.516708 / Out +0.079490`。
semantic／framing字段仍是cohort aggregate，没有逐样本paired CI。因此严格初始化reference支持的结论是：
P2改善Human及sequential Camera geometry，同时显著损害Direct-C geometry与两种Camera接口的
semantic／framing；不存在逐字段全局支配。但这不表示两者“总体相当”：按投稿预先采用的
Camera／系统质量优先级，C0-LAT在Direct-C geometry及Direct-C／sequential semantic／framing上
明确占优；True-P2的优势限于Human geometry与sequential Camera geometry。

#### Historical source-row sensitivity and implementation-cleanup boundary

C0-LAT训练只使用Camera source row0（observed/GT）；formal Direct-C也使用row0，而formal sequential
使用训练未触达的row1（generated/teacher-final）。checkpoint的`camera.source_embedding.weight`
shape=`[2,512]`：row0 L2=`0.376517`、SHA-256=`defff3ad66d7a3a0a05c0279d7e951a100d9bea0796cacadcaab907c48fa34b1`；
row1为exact zero、SHA-256=`e5a00aa9991ac8a5ee3109844d84a55583bd20572ad3ffcd42792f3c36b183ad`；
row0−row1 L2=`0.376517`、max-abs=`0.045465`。

固定formal sequential的Human、Camera text、ordered IDs与noise，只将row1重放为row0后，Human在全部样本
逐元素exact；4,053/4,053样本的Camera latent及decoded Camera均发生非零变化。每样本Camera-latent L2
mean/median/P90/P99/max=`3.059385 / 2.153666 / 5.005076 / 24.109246 / 87.388237`；
decoded-Camera L2=`1.017175 / 0.507861 / 1.586884 / 14.615968 / 67.628067`。
diagnostic contract／records／summary／manifest SHA-256依次为
`7a07c35c877fd8a598f08b25c73b1df86a10147273073dc53684cfd11c4a8138`、
`cbe5a58db3eae7b54d0cc8e6cedaef5368cf54548c570c73d6c6016c7094da30`、
`f056193bc8dc2dc6015f24468b012db50e6e9cf5606030eaeb69e52a95af6977`、
`1d55ebccff752c7f891872dfef6e00ddb2b4041319045bcb02f3a48f39189477`；诊断实现commit=
`7ae3b08c0a5552f18cbbf4a8b395b026f9c3db99`。

sealed audit为
`sm_c0_lat_true_p2_reference_seed17_4090g1_20260810/sealed_audit_c0_reference_source_row01.json`
（exact immutable path见[[StoryMotion-folder-rename-map]]），SHA-256=
`1d823b05b996a910253c5fecbb3db3d2be4ca82ca14ad441e83d6bb848253215`。
裁决：两行source embedding来自共享C0／C1四臂实现；C1的GT-H与teacher-final-H mixture需要区分
conditioning route，但StoryMotion从未提出“双来源匹配”能力，C0的核心条件分布也只要求Camera读取
给定Human latent与Camera text。因而本诊断证明的是historical C0多带了一个output-sensitive、训练未覆盖的
实现变量，不是StoryMotion核心claim失败，也不把既有三模式formal artifact作废。2026-08-12作者另行
授权只移除C0 source identity并fresh训练Camera Stage2 `105K`；exact v9 Stage1、owning decoder／cache／
stats与frozen Human teacher保持不变。该run只作实现清理，在endpoint／full-state与同evaluator三模式
formal audit前不替换operational C0-LAT；本节不提前登记任何新metric。

### Audited detail — original §3.22 observed=true symmetric route controls pure4,053 formal

| display ID | canonical sm_ run alias | training route | role |
| --- | --- | --- | --- |
| observed=true, G=on | `sm_p2_obstrue_coupled_cont105k_seed17_4090g0_20260810` | `observed_human=true`；Camera loss reaches Human；Human loss continues；source row1 | coupled route control |
| observed=true, G=off | `sm_p2_obstrue_detach_cont105k_seed17_5090g3_20260810` | `observed_human=true`；Camera loss detached from Human；Human loss continues；source row1 | detached route control |
| historical True-P2 | `sm_p2_matched_symmetric_joint_fresh_h105k_joint105k_seed17_4090g1_20260809` | `observed_human=false`；G=on；U=on；source row1 | route reference from §3.19 |
| exact-init C0-LAT | `sm_c0_lat_true_p2_reference_seed17_4090g1_20260810` | frozen Human；Direct-C row0、sequential untrained row1 | operational reference from §3.21 |

两条新臂均完成Camera／joint optimizer `105K`。endpoint audit确认model与EMA同时包含完整Human／
Camera state，optimizer、scheduler、RNG、sampler、embedded contract、implementation boundary与
checkpoint reload均闭合。预声明的step `20/100/1K/5K/21K/42K/63K/84K/105K`九次gradient
audit全部通过：G=on的Camera→Human梯度finite nonzero，G=off对应梯度exact zero，其余Human／Camera
梯度finite。两臂正式评测均为Direct-H、Direct-C与sequential，`joint_parallel=false`、
`is_causal=false`、shifted-sigma Euler50、CFG=1、eval/decode batch=`128/1`，ordered pure-test
`N=4,053`及ID SHA-256=
`a0d7627ee827e36a229d33f9975f8417ae78b504cd5a6db1edf62cb1a9266b93`。

公共owning decoder SHA-256=
`51233f6a032c779e66b6eed4bb22b7f61c41d9b4a5a0a1ffc7dade7d3d86d4df`，canonical Human teacher
SHA-256=`3efd59481f8052b401889fce6559e31f96cb88f51dfb6c466464cf05ec6c2c50`。
G=on checkpoint／training contract／endpoint audit SHA-256依次为
`d2921293dd0e6115d59490e0cc311188a3ee2e4605426031ed9a29e32a8638c0`、
`3ac108c3b2aeb7937409ee69b871115f5d17797aa66a8b251a1b0e094bdcb591`、
`c2c8c6f1f3fc826c8416c0cc132e248bd3d9f5b3dc9c45ce4611c46022bea2a0`；G=off对应为
`3535ac9e45ab920db4275524c1239edf2eed0586824f4928c410e1817eff7069`、
`81b7987752ed7663f54e80fde08a32ba203bde15d0a1ecb6e1e41f9b953a6f44`、
`b33b7fd5066e808e2cf7f1d3fee914106d5e8499f81e7d43274fff18d70f021f`。

#### Formal artifact identity

| version / run | mode | evaluation contract SHA-256 | fixed samples SHA-256 | records SHA-256 | results SHA-256 | manifest SHA-256 |
| --- | --- | --- | --- | --- | --- | --- |
| observed=true, G=on / `sm_p2_obstrue_coupled_cont105k_seed17_4090g0_20260810` | Direct-H | `ce6a48f3fa37dedf269eeb1a5108681fa4dc6445479c315228b42776b185813e` | `92cd859ef0418bdef50b945d4023217b0dcc6a067d6f27f43968282dd7d20f99` | `5832829a90e91588cd52b5800a4bc8d15bad6e7aa031e058375fee1e5c1b3741` | `d8d47d1c3585497f159020385c6fdfd0bd5deb977c285aaadc4a382ce87192da` | `b6b410e6372f640e5a57f1de3e4f6c3a13a0754f2a72d27cd1cc6125cf6fad3f` |
| observed=true, G=on / `sm_p2_obstrue_coupled_cont105k_seed17_4090g0_20260810` | Direct-C observed-H | `c04df3185bbb5278a0733b4714d1a07faba09da826f3db71b59c8b05725dbdc1` | `7beb46ebb500e8abf52ff88350eab1552d457e3ee311ec91f8cc470dc0fe8c94` | `340a1554085e7c6adf635aca3acf404aba1459cee5d623bf22f33ae1e27fc6d8` | `05d8b8655c555a245360a734c5f77e68a3a679156f5217e8d9cfa3009a8d27d6` | `170fc5bfd64055c9a9f1b58d7e52165d4dfd8f92383918a16c5127537f255799` |
| observed=true, G=on / `sm_p2_obstrue_coupled_cont105k_seed17_4090g0_20260810` | sequential Human→Camera | `e62e01ca85a7cad5db8d526f2f0f57063ab6d4f3e267ec244014f1a6939c787f` | `dc9fd3b78bef3eaaad9c3bf258151334ed4d7abce9c18b8c019534140c036491` | `3d301ff6147c5b45f27736af3db2e2c66932e6f1871a1c2b2d075b3b4f5873f1` | `754a20cf484028b604a5312e2ee179fdebae8377aa451ef473a30628b38fb1b9` | `0c986dcfda01e4db52c8428aa3ca0360d5382c5950598bf10fd152c6f163dcb6` |
| observed=true, G=off / `sm_p2_obstrue_detach_cont105k_seed17_5090g3_20260810` | Direct-H | `2140f745e3495cb7d4283d616da01689cbdc8f2079c7ed544ffa3c84975ba67d` | `6a7cf0de0a43389d0bfda5ea52f5f90fe19b25b4adee455cefecfdf875db0efe` | `52fbd91cdd9a5a85a0065620d45418de0d800e422bda10f4d0c36543075bd6b0` | `55ed8c86a4bad1306d51c2486a86a0b6458db62a6cc30781a7fc593f88bab7df` | `ed19c64ce66a884239b9172556e4eda7dfebfb2cf13428e42dfa0ae4d308c376` |
| observed=true, G=off / `sm_p2_obstrue_detach_cont105k_seed17_5090g3_20260810` | Direct-C observed-H | `831bb0e31e717180ed567e6bacec1ab180014e13c9a30f1aa199d1e979610b3a` | `2a486bfdeced682484337661c605b594d8ed1bb9a1fc3a926799b1f2b887c071` | `4679ed6369e15f5677067cb063027762a62d810a6dab1902c5bbde75028212eb` | `e8769db9c908ee9701eba5eb33df892723ccededc332172ce1abfe7a086c7326` | `312fa3775f7f7fb61814f36aca882468c00218a9bf3df679a3ef195b8cfe5820` |
| observed=true, G=off / `sm_p2_obstrue_detach_cont105k_seed17_5090g3_20260810` | sequential Human→Camera | `e5169097434a543d10fb71c04ca4624e92f501a5213c874084beaa7e894a2e51` | `94e6f3624ba9776ae8292b044c2210170422a8a3ebd59a118af748faa2035e93` | `659849e09ddf844d0aa00235bcf5c91c092357f26dbe7846b138a532e1283869` | `2cf7b98913929de85da6e1ff0d9942fb3a7a8ea9f69216491ced0d7c24d03da9` | `d1b5e4b053d0c80b8edc9cabe5d287c08b76d9188db3d53ea6f6e2b46258885f` |

G=on／G=off sealed eval audit SHA-256分别为
`c38c506dd88ebb06903f43166c62f7f7186ccb6ca61a2b8f50b684b83d2326dc`／
`4d2bd81853f9591a1eecfd5fccf2994a37909b0c2be1d9d8f5d49dcc93994805`。
G=off正式bytes以只读comparison input保存在G=on eval root下的
`comparison_inputs/detached_5090/pure4053/`；seal重新核验每个manifest与artifact hash，比较读取这些
5090原始bytes，不是在4090重跑detached evaluator。5090 runtime metadata仍由artifact保留，不能因staging
而消除cross-host covariate。

#### Aggregate metrics

| version / run | mode | Human TMR ↑ / FDTMR ↓ | Camera CLaTr ↑ / FDCLaTr ↓ | caption F1 ↑ | r-FPD ↓ / Out ↓ |
| --- | --- | --- | --- | ---: | --- |
| observed=true, G=on / `sm_p2_obstrue_coupled_cont105k_seed17_4090g0_20260810` | Direct-H | `17.845230 / 102.445770` | — | — | — |
| observed=true, G=on / `sm_p2_obstrue_coupled_cont105k_seed17_4090g0_20260810` | Direct-C observed-H | — | `54.313377 / 33.146400` | `0.713573` | `1.812493 / 0.167663` |
| observed=true, G=on / `sm_p2_obstrue_coupled_cont105k_seed17_4090g0_20260810` | sequential Human→Camera | `17.845230 / 102.445770` | `58.139671 / 23.822430` | `0.741294` | `1.014779 / 0.116215` |
| observed=true, G=off / `sm_p2_obstrue_detach_cont105k_seed17_5090g3_20260810` | Direct-H | `18.613176 / 96.372887` | — | — | — |
| observed=true, G=off / `sm_p2_obstrue_detach_cont105k_seed17_5090g3_20260810` | Direct-C observed-H | — | `55.365463 / 29.300417` | `0.733114` | `1.886545 / 0.171948` |
| observed=true, G=off / `sm_p2_obstrue_detach_cont105k_seed17_5090g3_20260810` | sequential Human→Camera | `18.613176 / 96.372887` | `57.573360 / 25.601322` | `0.743736` | `0.989905 / 0.115524` |
| exact-init C0-LAT / `sm_c0_lat_true_p2_reference_seed17_4090g1_20260810` | Direct-H | `17.354467 / 100.254402` | — | — | — |
| exact-init C0-LAT / `sm_c0_lat_true_p2_reference_seed17_4090g1_20260810` | Direct-C observed-H | — | `56.586727 / 22.163630` | `0.731021` | `0.799310 / 0.100393` |
| exact-init C0-LAT / `sm_c0_lat_true_p2_reference_seed17_4090g1_20260810` | sequential Human→Camera | `17.354467 / 100.254402` | `55.393429 / 29.761435` | `0.685826` | `0.507365 / 0.078331` |

| version / run | mode | Human global / root-aligned MPJPE ↓ m | Human root ADE / FDE ↓ m | Camera center ADE / FDE ↓ m | Camera rotation ↓ deg |
| --- | --- | --- | --- | --- | ---: |
| observed=true, G=on / `sm_p2_obstrue_coupled_cont105k_seed17_4090g0_20260810` | Direct-H | `0.828285 / 0.223819` | `0.746462 / 1.254861` | — | — |
| observed=true, G=on / `sm_p2_obstrue_coupled_cont105k_seed17_4090g0_20260810` | Direct-C observed-H | — | — | `2.388501 / 2.498247` | `56.352396` |
| observed=true, G=on / `sm_p2_obstrue_coupled_cont105k_seed17_4090g0_20260810` | sequential Human→Camera | `0.828285 / 0.223819` | `0.746462 / 1.254861` | `2.918527 / 3.029785` | `70.852242` |
| observed=true, G=off / `sm_p2_obstrue_detach_cont105k_seed17_5090g3_20260810` | Direct-H | `0.829283 / 0.221986` | `0.747588 / 1.249277` | — | — |
| observed=true, G=off / `sm_p2_obstrue_detach_cont105k_seed17_5090g3_20260810` | Direct-C observed-H | — | — | `2.501148 / 2.616128` | `58.310559` |
| observed=true, G=off / `sm_p2_obstrue_detach_cont105k_seed17_5090g3_20260810` | sequential Human→Camera | `0.829283 / 0.221986` | `0.747588 / 1.249277` | `2.980856 / 3.099442` | `70.781130` |
| exact-init C0-LAT / `sm_c0_lat_true_p2_reference_seed17_4090g1_20260810` | Direct-H | `0.848565 / 0.230946` | `0.762336 / 1.278247` | — | — |
| exact-init C0-LAT / `sm_c0_lat_true_p2_reference_seed17_4090g1_20260810` | Direct-C observed-H | — | — | `1.404148 / 1.487332` | `30.184385` |
| exact-init C0-LAT / `sm_c0_lat_true_p2_reference_seed17_4090g1_20260810` | sequential Human→Camera | `0.848565 / 0.230946` | `0.762336 / 1.278247` | `2.896272 / 2.993438` | `70.880520` |

#### Paired route-control audit and causal boundary

下表为`left − right`的mean delta与95% percentile CI；lower-is-better geometry按同一4,053个
ordered IDs做10,000次matched-index bootstrap。semantic／framing只有cohort aggregate，不附造
paired CI。

| version / comparison | mode | metric group | mean delta [95% CI] |
| --- | --- | --- | --- |
| G=on − G=off | Direct-H | Human global MPJPE；root ADE；root-aligned MPJPE；root FDE | `-0.000998 [-0.016342, 0.013772]`；`-0.001126 [-0.016764, 0.014216]`；`+0.001832 [-0.000618, 0.004252]`；`+0.005584 [-0.023057, 0.033504]` |
| G=on − G=off | Direct-C | Camera ADE；FDE；rotation | `-0.112647 [-0.166972, -0.058112]`；`-0.117881 [-0.176609, -0.060989]`；`-1.958163 [-3.447080, -0.528759]` |
| G=on − G=off | sequential Camera | Camera ADE；FDE；rotation | `-0.062329 [-0.119977, -0.005823]`；`-0.069657 [-0.127882, -0.010750]`；`+0.071113 [-1.523275, 1.675527]` |
| G=on − historical True-P2 | Direct-C | Camera ADE；FDE；rotation | `+0.363317 [+0.320545, +0.406139]`；`+0.352447 [+0.305621, +0.398184]`；`+6.474707 [+5.281071, +7.661443]` |
| G=on − historical True-P2 | sequential Camera | Camera ADE；FDE；rotation | `+0.442134 [+0.402287, +0.482851]`；`+0.445938 [+0.404240, +0.488569]`；`+6.038001 [+4.905851, +7.160045]` |
| G=on − exact-init C0-LAT | Direct-H | Human global MPJPE；root ADE；root-aligned MPJPE；root FDE | `-0.020280 [-0.029381, -0.011242]`；`-0.015874 [-0.024598, -0.007182]`；`-0.007128 [-0.008950, -0.005288]`；`-0.023386 [-0.041084, -0.005427]` |
| G=on − exact-init C0-LAT | Direct-C | Camera ADE；FDE；rotation | `+0.984354 [+0.925758, +1.043899]`；`+1.010915 [+0.950138, +1.072369]`；`+26.168011 [+24.692029, +27.630983]` |
| G=on − exact-init C0-LAT | sequential Camera | Camera ADE；FDE；rotation | `+0.022255 [-0.027944, 0.071142]`；`+0.036347 [-0.014966, 0.088674]`；`-0.028278 [-1.468793, 1.447926]` |

相对G=off，G=on不改变任何有显著CI的Human geometry，却显著改善Direct-C三项与sequential
ADE/FDE；sequential rotation CI跨零。对应aggregate为mixed Pareto：Direct-C的
`CLaTr/FDCLaTr/F1=-1.052086/+3.845984/-0.019541`，但`r-FPD/Out=-0.074052/-0.004285`；
sequential为`+0.566311/-1.778893/-0.002442`，但`r-FPD/Out=+0.024874/+0.000691`。
因此G-on只获得“在该matched observed route下Camera geometry更强”的局部支持，不能写成整体支配。

相对historical `observed_human=false`，G=on在Direct-C／sequential的aggregate Camera语义与framing
大幅修复：CLaTr分别`+16.461685/+18.061085`、FDCLaTr `-98.482292/-80.458462`、caption F1
`+0.262285/+0.242080`、r-FPD `-1.375736/-1.009295`、Out `-0.057439/-0.041606`；代价是上述
六项Camera geometry均显著回退。它支持“训练route错位是历史semantic／framing collapse的重要根因”，
但仍是trade-off，不是全面修复。

相对exact-init C0-LAT，G=on显著改善Human geometry，Direct-C Camera geometry和semantic／framing
均回退；sequential Camera geometry CI全跨零，CLaTr／FDCLaTr／caption F1改善，但r-FPD／Out回退。
本组关闭observed-route与gradient root-cause execution；§3.21的untrained source-row1只作为
historical C0 sequential实现provenance，StoryMotion不提出source matching claim。结果仍不支持
protected-asymmetry逐字段全面优越。

sealed paired comparison artifact SHA-256=
`7c0c5f77545f46052f5e26812c02ed9fe003baaa26fe562992e9c211a9eab490`；comparison audit script
SHA-256=`ae0c821a67e0d2e5a9cd35cd6fb07d25d130336561602207a8b1c4dc967a81cf`；exact audit helper
bytes只读保存在对应train/eval run的`audit_code/`。
4090运行时为Python `3.10.14`、Torch `2.3.1+cu121`、CUDA `12.1`、cuDNN `8902`、driver
`580.119.02`；5090为Python `3.10.20`、Torch `2.8.0+cu128`、CUDA `12.8`、cuDNN `91002`、
driver `580.95.05`。因此G=on−G=off保留host/runtime covariate，不能升格为无条件单变量估计。

### Audited detail — original §3.23 C0-LAT no-source implementation cleanup pure4,053 formal

`sm_c0_lat_nosource_c105k_seed17_4090g0_20260812`只删除C0 Camera Stage2的
two-row `source_embedding`；exact v9 Pulp-only non-causal Stage1、owning decoder、train/eval cache、
train-only stats、frozen Human `105K` teacher、Camera LAT objective与`105K` optimizer budget均不变。
endpoint audit确认full-resume／latest checkpoint一致，283个AdamW state全部在`105K`，
model／EMA／optimizer strict reload通过，Human state与teacher exact；Camera梯度finite nonzero，
Human无梯度，审计未执行optimizer step。`source_embedding_absent=true`，endpoint audit
SHA-256=`406bedd39454a6d0e724085e1009387e5975fdbbf4a0db0120c1706df5fe7788`。

formal评测使用ordered pure `N=4,053`，ID SHA-256=
`a0d7627ee827e36a229d33f9975f8417ae78b504cd5a6db1edf62cb1a9266b93`，
Direct-H、Direct-C与sequential三模式在同一runner内完成；`joint_parallel=false`、
Euler `50`、CFG=`1`、eval batch=`32`、decoder batch=`1`。Direct-H与sequential的Human
fixed samples与四个geometry fields在本run内全部tensor-exact，证明Camera路径没有改写Human输出。

| version / run | mode | Human TMR ↑ / FDTMR ↓ | Camera CLaTr ↑ / FDCLaTr ↓ | caption F1 ↑ | r-FPD ↓ / Out ↓ |
| --- | --- | --- | --- | ---: | --- |
| v11 C0-LAT no-source / `sm_c0_lat_nosource_c105k_seed17_4090g0_20260812` | Direct-H | `17.608391 / 99.390533` | — | — | — |
| v11 C0-LAT no-source / `sm_c0_lat_nosource_c105k_seed17_4090g0_20260812` | Direct-C observed-H | — | `56.983715 / 20.911659` | `0.734108` | `0.809388 / 0.101137` |
| v11 C0-LAT no-source / `sm_c0_lat_nosource_c105k_seed17_4090g0_20260812` | sequential Human→Camera | `17.608391 / 99.390533` | `55.184547 / 31.986971` | `0.686440` | `0.484429 / 0.074622` |

| version / run | mode | Human global / root-aligned MPJPE ↓ m | Human root ADE / FDE ↓ m | Camera center ADE / FDE ↓ m | Camera rotation ↓ deg |
| --- | --- | --- | --- | --- | ---: |
| v11 C0-LAT no-source / `sm_c0_lat_nosource_c105k_seed17_4090g0_20260812` | Direct-H | `0.842762 / 0.228751` | `0.758774 / 1.283042` | — | — |
| v11 C0-LAT no-source / `sm_c0_lat_nosource_c105k_seed17_4090g0_20260812` | Direct-C observed-H | — | — | `1.421300 / 1.506828` | `29.630605` |
| v11 C0-LAT no-source / `sm_c0_lat_nosource_c105k_seed17_4090g0_20260812` | sequential Human→Camera | `0.842762 / 0.228751` | `0.758774 / 1.283042` | `2.909155 / 3.010297` | `70.859733` |

#### Formal artifact identity

| version / run | training contract SHA-256 | endpoint Camera EMA SHA-256 | decoder / teacher / stats / train-cache SHA-256 | eval contract / fixed samples / records / results / manifest SHA-256 |
| --- | --- | --- | --- | --- |
| v11 C0-LAT no-source / `sm_c0_lat_nosource_c105k_seed17_4090g0_20260812` | `a5a4da1a41a0a51c1afc2595444f46306c26f11e5f5b4f23748d2f6389a41da0` | `37c60b343663b84a2eb886061304f8fccfa0fb94232665c3ee7eb503c43647f0` | `51233f6a032c779e66b6eed4bb22b7f61c41d9b4a5a0a1ffc7dade7d3d86d4df` / `3efd59481f8052b401889fce6559e31f96cb88f51dfb6c466464cf05ec6c2c50` / `117d51a1d2ed1ae57541723b85c732118172634c57b2665f00b246c36e218558` / `04add8e553af334e4724f08c7076a0be24f171470b938920120ef64fc7b01576` | `782a9fb5bbc782d85dff663086b6dc48984423fea570c51145a6e3c2cb6279da` / `5ae6a2b5afa5f4464692a95cf82fc5e97e6839122ead3cd64102953265ad0f51` / `0ecc46687a59e40b9249705c36108386ce19542bee5f4a0382decb4489b14f99` / `0c1ac94fdfdb950247e9986860211b669192c34e0c61d4a2efc03fb1a670157f` / `542de87751e98781620b9f576bb51fca4a8d9c4da0bf3af64ff728d94017e25b` |

#### Paired comparison and decision boundary

下表为`no-source − reference`的mean delta与95% percentile CI，lower-is-better geometry在
4,053个ordered matched samples上做10,000次bootstrap。aggregate semantic／framing无per-sample
paired unit，只报告差值而不伪造CI。

| comparison | mode | Camera ADE∆ / FDE∆ / rotation∆ | Human global / root ADE / root-aligned / root FDE∆ |
| --- | --- | --- | --- |
| no-source − exact-init C0-LAT / `sm_c0_lat_true_p2_reference_seed17_4090g1_20260810` | Direct-C | `+0.017152 [-0.021907, +0.056599]` / `+0.019496 [-0.020881, +0.059500]` / `-0.553780 [-1.449410, +0.335224]` | — |
| no-source − exact-init C0-LAT / `sm_c0_lat_true_p2_reference_seed17_4090g1_20260810` | sequential Camera | `+0.012883 [-0.048784, +0.074766]` / `+0.016859 [-0.045824, +0.080534]` / `-0.020787 [-1.833349, +1.758312]` | — |
| no-source − exact-init C0-LAT / `sm_c0_lat_true_p2_reference_seed17_4090g1_20260810` | Direct-H | — | `-0.005803 [-0.024647, +0.012229]` / `-0.003562 [-0.022416, +0.014612]` / `-0.002195 [-0.004817, +0.000396]` / `+0.004795 [-0.028658, +0.037730]` |
| no-source − operational C0-LAT / `v11_c0_lat_fixedh_35to105k_seed17_5090g2_r2_20260730` | Direct-C | `+0.008828 [-0.025003, +0.044350]` / `+0.008300 [-0.026382, +0.044274]` / `-0.291445 [-1.121281, +0.522102]` | — |
| no-source − operational C0-LAT / `v11_c0_lat_fixedh_35to105k_seed17_5090g2_r2_20260730` | sequential Camera | `-0.033641 [-0.059759, -0.008065]` / `-0.031893 [-0.058728, -0.005570]` / `-0.574822 [-1.509105, +0.350793]` | — |

相对exact-init C0-LAT，全部paired geometry CI跨零；相对operational C0-LAT，只有
sequential Camera ADE／FDE小幅显著改善，Direct-C三项与sequential rotation CI跨零。
operational aggregate差值为mixed：Direct-C的FDCLaTr／r-FPD／Out改善
`-0.259720 / -0.037139 / -0.004041`，CLaTr `+0.050217`，但caption F1 `-0.003043`；
sequential的FDCLaTr／CLaTr／caption F1回退`+3.233345 / -0.394196 / -0.007078`，
r-FPD／Out改善`-0.023776 / -0.002643`。因此该run证明source identity可从C0实现中
移除而不造成paired geometry退化，但不形成逐字段winner，也不单凭该结果自动替换
operational metric mainline。它是claim-neutral implementation-clean candidate，不新增“双来源匹配”
贡献，也不改变§3.21历史artifact的provenance价值。

sealed audit SHA-256=
`f72d6ff099d3962503b67fed8f86f6d9828335903fdaf6b58dcea6ed22a59632`；audit helper
commit=`4f0ea990f1cee5bf6949340f9b67c9671c25bead`，script SHA-256=
`ea4b173f46cbefb5b1181b2df7246779a3c0ecac8c22bace3ddd5a1bf3fc95c6`。当前runner与
operational C0均为eval batch `32`，但wrapper SHA不同；exact-init reference为batch `128`。
三者共用official Pulp callbacks、ordered IDs、decoder、teacher、Euler50与CFG=1，
wrapper／batch／runtime仍保留为covariates。

### Audited detail — original §3.24 fully independent dual-EncDec Stage2 pure4,053 formal

`sm_independent_dual_encdec_lat_h105k_c105k_seed17_4090g1_20260811`冻结§6.9已经审计的
independent Human199→H128与absolute-C2W14→C64 Stage1 owning checkpoints、branch-local
train-only normalizers、完整`162,760/4,053` cache和各自owning decoder；Human Stage2先fresh训练
`105K`并冻结，Camera Stage2再以GT-H-only训练`105K`。Camera使用同一个已训练source row服务
Direct-C与sequential，不构造generated-H positive；`joint_parallel=false`、`is_causal=false`。
该系统同时改变representation、decoder、normalizer/cache、参数化与Stage2接口，因此从预注册开始就只
是secondary native-system boundary，不是protected-asymmetry、latent-interface或cascade的单变量消融。

endpoint R2确认`210K` checkpoint与last payload exact，Human endpoint state与`105K` teacher tensor-exact，
284个Camera optimizer state全部到`105K`，strict model／EMA／optimizer reload通过；gradient audit有
284个finite nonzero Camera-gradient tensors、Human-gradient tensors为0，且backward后Human state exact。
checkpoint SHA-256=`0f396930ed71a6d348932f2a6e914bb3f511c364727db2e63a91448c355f01cf`，
teacher SHA-256=`a6c29c14131b644aeff3d2ccf0a15348372182f89b3db32999c22d4c4f6466ed`，
owning-decoder SHA-256=`6f22ba0bb85f782795263500e1feb4bf27cd6c88c9387524c63d0c54b1014f4b`。
endpoint audit SHA-256=`d68624ca6d24a42c6cbb6b72912b50e324579fcdd31de7d730108168b529a972`。

formal evaluator在ordered pure `N=4,053`、ID SHA-256=
`a0d7627ee827e36a229d33f9975f8417ae78b504cd5a6db1edf62cb1a9266b93`上完成Direct-H、
Direct-C与sequential；Euler `50`、CFG=`1`、eval batch=`128`、decoder batch=`1`。Direct-H与
sequential Human输出在本run内相同；相对teacher的CUDA runtime max-abs=`5.3883e-5`，低于预声明
`5e-4` gate，endpoint state仍为tensor-exact。

| version / run | mode | Human TMR ↑ / FDTMR ↓ | Camera CLaTr ↑ / FDCLaTr ↓ | caption F1 ↑ | r-FPD ↓ / Out ↓ |
| --- | --- | --- | --- | ---: | --- |
| Independent dual-EncDec / `sm_independent_dual_encdec_lat_h105k_c105k_seed17_4090g1_20260811` | Direct-H | `15.667656 / 132.930176` | — | — | — |
| Independent dual-EncDec / `sm_independent_dual_encdec_lat_h105k_c105k_seed17_4090g1_20260811` | Direct-C observed-H | — | `64.481987 / 11.739902` | `0.836639` | `1.197567 / 0.132438` |
| Independent dual-EncDec / `sm_independent_dual_encdec_lat_h105k_c105k_seed17_4090g1_20260811` | sequential Human→Camera | `15.667656 / 132.930176` | `63.908108 / 24.940548` | `0.801576` | `0.582880 / 0.084257` |

| version / run | mode | Human global / root-aligned MPJPE ↓ m | Human root ADE / FDE ↓ m | Camera center ADE / FDE ↓ m | Camera rotation ↓ deg |
| --- | --- | --- | --- | --- | ---: |
| Independent dual-EncDec / `sm_independent_dual_encdec_lat_h105k_c105k_seed17_4090g1_20260811` | Direct-H | `0.852898 / 0.238061` | `0.765001 / 1.284139` | — | — |
| Independent dual-EncDec / `sm_independent_dual_encdec_lat_h105k_c105k_seed17_4090g1_20260811` | Direct-C observed-H | — | — | `1.621345 / 1.695579` | `34.039265` |
| Independent dual-EncDec / `sm_independent_dual_encdec_lat_h105k_c105k_seed17_4090g1_20260811` | sequential Human→Camera | `0.852898 / 0.238061` | `0.765001 / 1.284139` | `2.984307 / 3.076258` | `71.470072` |

#### Formal artifact identity

training contract SHA-256=`f9e4c1239858019b2a3b38439c6111388d45f0050a5598ab714d4bc6b66daad3`；
training manifest SHA-256=`f042d0179f8e68b7d8991541893fb22df75f350a75387b4c8b44c87e6e142f0e`。

| version / run | mode | eval contract SHA-256 | fixed / records / results / manifest SHA-256 |
| --- | --- | --- | --- |
| Independent dual-EncDec / `sm_independent_dual_encdec_lat_h105k_c105k_seed17_4090g1_20260811` | Direct-H | `027693ea0e467e5496a1c989919e90de55d38d2c8c3b03e2dddd7cba985e5e08` | `a98320f38d57009fd95eba8dbaa435e84591c131440129090cf16e0eb1dc3a38` / `6df96d28ef6a0e8d34a239efda9f36be2ea5141c20d780e9aa39a7815c6a073d` / `424409e3d910ce367b6c34e5c13885a74631c3b71fd5c95a6e60f79314efd369` / `5c928b21dbc0f492415d60dfa2043004006968eaa5a14f3b7b63f76e17fa129e` |
| Independent dual-EncDec / `sm_independent_dual_encdec_lat_h105k_c105k_seed17_4090g1_20260811` | Direct-C observed-H | `ace6f71729cc824503dcb9715bd2c500efe3292cf3cf1b157d9269f43f769e70` | `2e2f7be2e048e5c3ed9cbe5da0037a4e0329764c7a96599ba67567df715abb72` / `45762b74531d7b0beaaf7f00307271e894687f50d003409e80b90437732d3cac` / `fdc94242322392b306d4cdb4ec5f44d918b589806124cc39a0854dbec6058cbf` / `605c2a3a4ecc669d65af087266c71a0e76a296f779fc9f8640e1a30b4880555e` |
| Independent dual-EncDec / `sm_independent_dual_encdec_lat_h105k_c105k_seed17_4090g1_20260811` | sequential Human→Camera | `c2f524d7e2bfb6531fa1d9c5c9172bfa28a36cff54877e084ee2434ecaee1cab` | `0deb655999a791333864cb758e035c37043bae37f5ca9bd693d101c5c71ab93d` / `aeba57bfa347b01b23772b2464cbdd9ac24f23c416b019c626c1d9a172a2e613` / `6abc1c0294e86c291ae35c7eeb370eb40b13bffbf4c599322b3cdb1d2653d38d` / `57aef35eff655731a0bba281bf26d491b36e4a513fcef8abd14f0712c0310235` |

#### Exact-init C0 comparison and decision boundary

下表为`independent − exact-init C0-LAT`的mean delta与95% percentile CI；lower-is-better geometry按
相同ordered 4,053样本做10,000次matched bootstrap。aggregate semantic／framing没有逐样本paired
unit，只报告方向，不附造CI。

| comparison | mode | Camera ADE∆ / FDE∆ / rotation∆ | Human global / root ADE / root-aligned / root FDE∆ |
| --- | --- | --- | --- |
| Independent dual-EncDec − exact-init C0-LAT / `sm_c0_lat_true_p2_reference_seed17_4090g1_20260810` | Direct-C | `+0.217198 [+0.170072, +0.263038]` / `+0.208247 [+0.160600, +0.255563]` / `+3.854879 [+2.699325, +5.035567]` | — |
| Independent dual-EncDec − exact-init C0-LAT / `sm_c0_lat_true_p2_reference_seed17_4090g1_20260810` | sequential Camera | `+0.088035 [+0.024336, +0.151992]` / `+0.082820 [+0.018455, +0.147441]` / `+0.589552 [-1.280910, +2.418639]` | — |
| Independent dual-EncDec − exact-init C0-LAT / `sm_c0_lat_true_p2_reference_seed17_4090g1_20260810` | Direct-H / sequential Human | — | `+0.004334 [-0.015058, +0.023676]` / `+0.002665 [-0.016994, +0.022131]` / `+0.007115 [+0.004514, +0.009638]` / `+0.005892 [-0.028197, +0.039528]` |

相对exact-init C0，independent系统的Direct-C三项Camera geometry与sequential ADE／FDE显著回退，
sequential rotation CI跨零；Human只有root-aligned MPJPE显著回退，其余三项CI跨零。aggregate同样是
mixed：Direct-C的CLaTr／FDCLaTr／caption F1改善`+7.895260 / -10.423728 / +0.105618`，但
r-FPD／Out回退`+0.398257 / +0.032046`；sequential的CLaTr／FDCLaTr／caption F1改善
`+8.514679 / -4.820887 / +0.115751`，但r-FPD／Out回退`+0.075515 / +0.005927`；Human
TMR／FDTMR回退`-1.686811 / +32.675774`。因此该run只证明完整独立H/C native chain在公平
exposure边界下可训练、可三模式生成，并形成semantic-vs-geometry／framing trade-off；它不支持
独立representation、latent interface、cascade或protected asymmetry superiority，也不替换v9+C0-LAT。

H／C Stage1各为`210K` optimizer steps、batch128，即各`26.88M` exposure，合计`53.76M`
branch-samples；低于v9 Stage1三phase合计`81.408M` exposure，不是v9双倍sample exposure。
sealed audit SHA-256=`2ea912380ff3b66bbde854a4018f0b3e820922b7c7e7a96a0501a123d77cf25c`；
audit helper commit=`51388d144b5aa2e8d2acf5640e22324030d96d2a`，script SHA-256=
`8fb1827b8d57eec80662824b93826b2bdcc3eab5be46af8d92cb2ecf2c8e418c`。本次4090 runtime为
Python `3.10.20`、Torch `2.8.0+cu128`、CUDA `12.8`；与历史4090 evaluator runtime不同，
system comparison继续保留runtime covariate。

### Audited detail — original §3.25 Human-text Camera condition-attribution pure4,053 diagnostic

`sm_ht_condition_attribution_pure4053_20260810_r2`复用HT-FILM／HT-HX／HT-DR的matching
pure4,053结果，并在每个design的Direct-C与sequential接口分别执行Human-text `absent`和
fixed-point-free cyclic-shift-1 `shuffled`。12条intervention arm均为evaluator-only：固定Camera
text、Human context／output、sample IDs、initial noise、Stage2 EMA、v9 owning decoder及cache；
`optimizer_constructed=false`、`is_causal=false`、`joint_parallel=false`。三种condition均为
`N=4,053`且ordered IDs SHA-256=
`a0d7627ee827e36a229d33f9975f8417ae78b504cd5a6db1edf62cb1a9266b93`。

| version / run | design | mode | Human-text condition | CLaTr ↑ | FDCLaTr ↓ | caption F1 ↑ | r-FPD ↓ | Out ↓ |
| --- | --- | --- | --- | ---: | ---: | ---: | ---: | ---: |
| v11 / `v11_ht_film_fresh105k_seed17_4090g0q_r2_20260801` | HT-FILM | Direct-C observed-H | matching | 57.251808 | 19.353085 | 0.751396 | 0.792972 | 0.100036 |
| v11 / `sm_ht_film_direct_c_absent_pure4053_20260810_r2` | HT-FILM | Direct-C observed-H | absent | 39.671360 | 143.347702 | 0.411247 | 5.325312 | 0.315492 |
| v11 / `sm_ht_film_direct_c_shuffled_pure4053_20260810_r2` | HT-FILM | Direct-C observed-H | shuffled | 57.312496 | 19.886114 | 0.749121 | 0.794079 | 0.101793 |
| v11 / `v11_ht_film_fresh105k_seed17_4090g0q_r2_20260801` | HT-FILM | sequential Human→Camera | matching | 56.088821 | 32.106274 | 0.712784 | 0.479443 | 0.072889 |
| v11 / `sm_ht_film_sequential_absent_pure4053_20260810_r2` | HT-FILM | sequential Human→Camera | absent | 42.743332 | 94.277359 | 0.421725 | 1.965306 | 0.166811 |
| v11 / `sm_ht_film_sequential_shuffled_pure4053_20260810_r2` | HT-FILM | sequential Human→Camera | shuffled | 56.092674 | 31.152216 | 0.714548 | 0.508565 | 0.074930 |
| v11 / `v11_ht_hx_fresh105k_seed17_4090g1_r2_20260801` | HT-HX | Direct-C observed-H | matching | 57.418770 | 19.399197 | 0.746752 | 0.784582 | 0.098772 |
| v11 / `sm_ht_hx_direct_c_absent_pure4053_20260810_r2` | HT-HX | Direct-C observed-H | absent | 34.236355 | 210.436203 | 0.387534 | 8.278432 | 0.379763 |
| v11 / `sm_ht_hx_direct_c_shuffled_pure4053_20260810_r2` | HT-HX | Direct-C observed-H | shuffled | 57.289715 | 19.582769 | 0.749549 | 0.769506 | 0.099013 |
| v11 / `v11_ht_hx_fresh105k_seed17_4090g1_r2_20260801` | HT-HX | sequential Human→Camera | matching | 54.055222 | 43.644333 | 0.680983 | 0.512886 | 0.072530 |
| v11 / `sm_ht_hx_sequential_absent_pure4053_20260810_r2` | HT-HX | sequential Human→Camera | absent | 35.841499 | 171.067245 | 0.355524 | 3.178044 | 0.199020 |
| v11 / `sm_ht_hx_sequential_shuffled_pure4053_20260810_r2` | HT-HX | sequential Human→Camera | shuffled | 53.957172 | 42.881405 | 0.682746 | 0.501131 | 0.071708 |
| v11 / `v11_ht_dr_fresh105k_seed17_4090g0_r2_20260801` | HT-DR | Direct-C observed-H | matching | 58.840408 | 17.585512 | 0.771117 | 0.869858 | 0.107463 |
| v11 / `sm_ht_dr_direct_c_absent_pure4053_20260810_r2` | HT-DR | Direct-C observed-H | absent | 54.731720 | 32.306683 | 0.686334 | 0.949724 | 0.114605 |
| v11 / `sm_ht_dr_direct_c_shuffled_pure4053_20260810_r2` | HT-DR | Direct-C observed-H | shuffled | 58.678585 | 17.938782 | 0.768544 | 0.861534 | 0.106606 |
| v11 / `v11_ht_dr_fresh105k_seed17_4090g0_r2_20260801` | HT-DR | sequential Human→Camera | matching | 58.145096 | 24.564266 | 0.743572 | 0.494295 | 0.078052 |
| v11 / `sm_ht_dr_sequential_absent_pure4053_20260810_r2` | HT-DR | sequential Human→Camera | absent | 54.845802 | 30.395502 | 0.675149 | 0.616057 | 0.088435 |
| v11 / `sm_ht_dr_sequential_shuffled_pure4053_20260810_r2` | HT-DR | sequential Human→Camera | shuffled | 58.031605 | 24.315554 | 0.739245 | 0.495391 | 0.077543 |

matching相对absent在`3 designs × 2 modes × 5 fields=30`个方向性aggregate cell全部改善，
支持三个可选HT分支确实依赖**非空Human-text通道**。但matching相对shuffled的差值很小且
方向混合：例如FILM Direct-C的CLaTr为`−0.060688`、FDCLaTr为`−0.533030`，HX Direct-C
分别为`+0.129055/−0.183573`，DR sequential分别为`+0.113491/+0.248713`。因此本矩阵
不支持“Camera使用了样本匹配的正确Human语义”；aggregate semantic／framing metric没有逐样本
paired unit，不能把近似重合写成统计等价。该结论只关闭optional Human-text mechanism diagnostic，
不提升HT分支、不改变C0-LAT mainline，也不替代C0-LAT的Camera-text ownership intervention。

#### Model, evaluator and artifact identity

三条design共享v9 parent／owning decoder SHA-256=
`51233f6a032c779e66b6eed4bb22b7f61c41d9b4a5a0a1ffc7dade7d3d86d4df`、frozen Human teacher
SHA-256=`3efd59481f8052b401889fce6559e31f96cb88f51dfb6c466464cf05ec6c2c50`、stats
SHA-256=`117d51a1d2ed1ae57541723b85c732118172634c57b2665f00b246c36e218558`；
eval／Human-text／teacher-final cache SHA-256依次为
`cd10a02a09bbb716dcdd1796bc0b11cac4451ff3f18496535c68464e0d88a603`／
`21915073284992f5c6f8f4f545e0be38f7384acb0fe971789f23ab9664829913`／
`4bd299cc990ad5cabfefa1670afa4d06e525840deb52caf59440bd53fd02642d`。

| version / run | Stage2 EMA SHA-256 | training contract SHA-256 |
| --- | --- | --- |
| HT-FILM / `v11_ht_film_fresh105k_seed17_4090g0q_r2_20260801` | `750c8f394a8e8eedd363691ee588d4c203fcb58ee0b8ac5704fd6cc52395f4bf` | `83f96937f8aa798361b5c5527839ac6b6b22e7e47aaca0919d8df02b58a887c8` |
| HT-HX / `v11_ht_hx_fresh105k_seed17_4090g1_r2_20260801` | `efc44816b31fe497128c3418d6f742925ce31e5ce09b488f46a5d165f3126489` | `4fa04fd795e1b631eafb778061d88ebf7f39cc316c5e92b9969c6efd0ebcd64f` |
| HT-DR / `v11_ht_dr_fresh105k_seed17_4090g0_r2_20260801` | `d817b5cb5a635972054405f1bb6ae8dfe15ae1b4036ed9a8536d57ed2c585a77` | `7fcd78a77dfe3286f907878b7f5d051d77ef54b4b5fcefd7024acc78f422cdb9` |

下表每格依次为attribution contract／evaluation contract／fixed samples／records／results／manifest
SHA-256。regular Markdown使用`sm_` alias；4090 immutable artifact内的`paperA_` run ID与路径不改名。

| version / run | artifact SHA-256 sequence |
| --- | --- |
| HT-FILM / `sm_ht_film_direct_c_absent_pure4053_20260810_r2` | `83d61ea5b2826077fe3cbf82b190ec9c8702c61306a1f01fd18acdbd0a7c4521` / `30df9649561d7e597427a15cbec81c45c8377dabb3f65a569a1c400417fe542f` / `67b514547f878bbe9f496b50c1a85a3084b0db974d952e9dc1c43d40c8617718` / `ef80c25e132f520ae3f00ce979c92ec7ef2b7eae6d741e10ee7ac4e2ea61ae12` / `6eb9c7018e93358da1a663776a3158e92b175595118d6c6c101617e29d66d45e` / `2c09c343f59ca416970654493ce5dbaadbbe5ab3f13d39126c7d1a931bf4401f` |
| HT-FILM / `sm_ht_film_direct_c_shuffled_pure4053_20260810_r2` | `dcadb158eb4375d9fe227f08da47eb7cd324037b74b05ea6cab6f02497b55428` / `5ec86dfbdaf1502c20f43e525aea931d339ab6705615566c9e12253e81639336` / `9d3bd29823716d2e330a9d9032e3e2525cb29f742366a40decca7f1f870a9a8a` / `e8caed72794da3228f0e4f7a9e1499bb74502f8ea7a51395777e59660e8442be` / `f1220ea4f7db67e388ecb861dd8d3211dd4e9450a413b897220f487797e653e5` / `9bc6a79a321f41315ed68bb358a4020af3db8a40b1725b8f7fa2012694f16cf9` |
| HT-FILM / `sm_ht_film_sequential_absent_pure4053_20260810_r2` | `84ac208f0e4a5ccf36264d920c65ea7770c1efde7e99367668bd30cfbeef70c5` / `8ab2fcbf382b3405d9e4de0afb9cb2a4137d553d20c4ab5533b09365d4c541e5` / `0a3b8de4b7bd06cb06a3886642d8bb8262713b6d0e57d9816109cb74cd79df72` / `11993932e36ca0b6179b6fdb07cbc561adc9a063a4d53ee80a41c5984dd06d86` / `c7c18bafe54dbe7ae7d3ae1d2d8eb93a501d86edffd329903b87fe70cfb7f7c9` / `d0b23381cba028b438e7638cff8b531d0028c8e009c265038d1bc53895d0122e` |
| HT-FILM / `sm_ht_film_sequential_shuffled_pure4053_20260810_r2` | `f04aae1a9d6b5c575f41babf05a38c40ccb615c76dbdac0d2be3c129ede188dc` / `1a17c2da7470390419bd32dbb63cdba121ea0042115bf62c17be4f8337ea5749` / `2cf934832b66fe2b7e3d31e77725e852f4d98e77a6e202c5a88800716715b2f4` / `24ad78ab7b731dd80dcaae77ab13951aa4129d811e0463bd4f9cb897c2f260cb` / `c22f36cfceac1070c1e6a79e0ddbf451107809aace07b3e4ba46a99dcd9f7363` / `468ba91cc7e4fe881437d7261e12f4095b4ad86abb612df1407f47fb544980b7` |
| HT-HX / `sm_ht_hx_direct_c_absent_pure4053_20260810_r2` | `cca3779bd777103ed6c156f03c0206fb00587167f547d0e5e92f989a1c05dbd8` / `728cea195df426273a8950e4aa3b89725f85d89ea591606262d4b8b661a182ce` / `301b3d72191e2e80ebcceb4cd275b1fb7bd30fc91991dfc03ad4806cb9f5ef69` / `3805a669bc8fdc26ee46aa17a8a2acbac0fb7b5571d364929ce16779b04dd5e4` / `421b580a7c491d7acdeecfce6d86337ed5f649d2f2de4bd8fa18a3903f24654f` / `6e04ef889fb3044319a60228963603ed69e3f52de25f94d89b59a22976a2d71d` |
| HT-HX / `sm_ht_hx_direct_c_shuffled_pure4053_20260810_r2` | `38d08b0b2bc10c34bddf56df7e2e4628f054fa3010a4113d4a7ac54b3c3fb706` / `a5153bd7b390683114d054bc890caf34e545ec4cedd8bb36ad87971f0c562c83` / `743133beddece70c5cb3949b934ae49c9c00acd5c72681602abc38ef46b8a2c2` / `fccf7af574a558e32750c4f1f63df7e46d37d2d54ca089dc93e7333761e997bc` / `8747e9d63967b15fb8f325a7dc4658c460d2450466b1abbcab97e604b8e48e52` / `d382eaf38cc933fe520c6d8076d51e84b032144a446ad1cc70271bdc7e7aef56` |
| HT-HX / `sm_ht_hx_sequential_absent_pure4053_20260810_r2` | `bba77edba39e0fbcdea1335f9a714bc0bf5f3a3e13697b6966112cdda97782c4` / `ab561a61d247f49b4dca3e291c0254e3fdcaada7fcaeb10ed0311214666b294c` / `73f8153c2b3a183f66d26829f433409369e2325023e95a42543d442b25665cc4` / `b0666d6fe1e6e37d8f63a83465e9c10d8213091f6806770af83ad5887b30a21a` / `cd62ff4279421924dbf6f801df34aa92b218c2b0b1c0feecc5432e29713c9d40` / `9da7c4228bd255321105d27f89d8a29700705f0f7b56c4345c6b664f9ee7769e` |
| HT-HX / `sm_ht_hx_sequential_shuffled_pure4053_20260810_r2` | `89a16755ff9b8ff5dd149a450d627882760d62fe1e05ad85a369d8875601ef99` / `411890da683ce112231fe9e0e84ee27276c344e2a8cb46adb76f70cf99b91c33` / `6e9631586f8c8ee062c21b8bb835e825fd297b1bc2f72cdc59c47ce3b7e7e3be` / `88cccdd238eeda540de202b2fb844d85ea7147b0254b5d0bf870c7acb717c1d4` / `e227a70bd6ae5b6a76c6b4752a070bd0737caeb4bfaf7a3d5eecdba111508032` / `4d9cd8b33aac31da8be5ab13271c1e895e765dd66330078d29b661a5439ee5af` |
| HT-DR / `sm_ht_dr_direct_c_absent_pure4053_20260810_r2` | `c7d9484dd912efb283d906c5dc7d19442c961ee50206446b6feba43b32ed3c4e` / `cf91dddc5ae1007cc550a02027850adc8bedc9e732e6f02fdc89dab4b6d338a0` / `e8324687c7e5f90ea9e885d87c251f5ed83044a64891560090227935796d267d` / `6173062b86db82d972632666c4a06a0547019c9a1cc370ac5d6534247b0eca1e` / `93c02735c721ae33c376bb4a4d8d25501038ba6fa273ecad2302b5c7ef5f0b72` / `989bc02061ce465218dc8e36accb5f0e05ff647ced4a99744fc7bf4d36e58a8d` |
| HT-DR / `sm_ht_dr_direct_c_shuffled_pure4053_20260810_r2` | `ee42b6341599fb6192757f6d65e787d1505d28bf62ac5a7cde0a3cf2ba0eec45` / `4bbad8ae1ed6aa22446764d7c48502db11305bcdf0a9c4fc1561c0f621921257` / `86f5c579b8502cad0811eecf5883b2fa0d0b8594386e3102ea7b793485cf1c28` / `d2e5cd6c83f833c349ae57df5c1ff74ed3ece990cf6f04141ef204a17f9cb688` / `bbbb4e0ebb58b0ef739caf4aa62f1bbcaf812f12c3e7bb431217dcef575219de` / `e7d75ca78ddbebf70d9233ce26385ca5643f5d3eea95178e8d1a17f2a3c824bd` |
| HT-DR / `sm_ht_dr_sequential_absent_pure4053_20260810_r2` | `79234e5ba6e71c074ec29597524a93d74cedbc5cffd7366fe14f59dc80f666dc` / `e0688a2d5c5b3fb4ed34bfd5b5c26ef4211e1c83cac016b5720350524a5d5d05` / `5b8dd4da2430978dd7df5e39220841193067512a93d7c5c07b4241c59e3de398` / `09aa3c1527a8c4a24d0a7f9d1ec104caa5956c283e7a7282fef216df298ade84` / `67379ee71197695ace33b48b43f5a57e58f33c4e8760c994e061a494717e1f86` / `37b4d737373d171de268cd1b2136ff317443d52a5c7297e3c597a8e3ec746374` |
| HT-DR / `sm_ht_dr_sequential_shuffled_pure4053_20260810_r2` | `0e24b6eadabdacd27f3710ef94237a428968aee18050eb663c80ed6f5d6f0eb6` / `9087b19c392bb8d6b8623ad24735a6dd4a15a73b8da62ea6ea942142bac21eaa` / `61f8d7d3a29b05e37327c6cade84565e9c415b67252a68c8c4f2d510c157aa75` / `b5185ccd98e1d5a5efc82127d20e349503955ef06810fe47557de15b7c54a949` / `585af4e679622c690e0d304357f77db1dfefe7cee4b3337f40cf019c0be33d29` / `60b3882808918dfb41dd87dc02e7166f723b27bfa69061139d3ac5739fb9f2de` |

matching reference的evaluation contract／fixed samples／pure4053 contract／records／results／manifest
SHA-256为：

| version / run | artifact SHA-256 sequence |
| --- | --- |
| HT-FILM / `v11_ht_film_fresh105k_seed17_4090g0q_r2_20260801` | `8a7acac34a20ca7ad8b32080a3d1e69da3df97df4301b7856f4622eca68820f6` / `6b35d63bf4cb6ba8dc71c1590607289035adf06ea6a9b0e953b4d1141ff3315a` / `fe941be4ade5611c34610fe0a998c670261cc65d390498618e93068f4c4bb137` / `3faec2c4b722baa1980a6541c45dc204790df8dae6e71ff53d63b7ccf4a9706a` / `697a9930d6f784c74e36e5ea2547e289e72be48eb7cc94cb2365ff8d1a0e5bb8` / `81f79a460f30ac24223fa1f973f96844dc53f56564190c7b2ebb30d5e9d4c957` |
| HT-HX / `v11_ht_hx_fresh105k_seed17_4090g1_r2_20260801` | `16609b0b866ce19dba1367879bf1abda2bff1033df0d054f2d01e5b4396a97bd` / `0e45f9399bf360152b156dc9fddb0a6feb7ebeecaa008bf189fed3bbc676b037` / `015c0ae20c264d4f11fb8a80b3f9e069fe2b1146df1420e3a0040d19076a2c80` / `2b69b44510f160fc3069e0d3c10e0b3849ae3f6d96c2bfc128e7346713e680dc` / `5a6d933ce6768c7116b356275471bc5fc0062f41642018b1bb3f9ecc1cbf7f14` / `4202b14fd8ed1e03277e87d893cf4589316f549475c13487e7aff10ddfe0a6d4` |
| HT-DR / `v11_ht_dr_fresh105k_seed17_4090g0_r2_20260801` | `260d8a0d28ef20bbbb718a773738090c7b36a4d5bb1077760e0d67d1ad9d4211` / `a57418b75500a8a1bdf84a612d6939d738e6dea1505a35119d925696f0ac82be` / `6534e5cdad57a6cd6a8e79d1b6ef90b5c25988a4313c4bf78273f81d60258164` / `57dee6f9362037034aa8d361a03e2d85fefa77b2d73960c4829371d87caef9f9` / `3416b84c064116775b782402f3cf1d5544bf0fb55384fa23bf80d42aeb64852f` / `154e120e108b81dd9d31255a22b5b0c3d25ab04156a4e9882b47b856f7cf5534` |

formal R2 seal SHA-256=
`818ac91cba809db73c179509745c5d0d277226b8f32287eb570bd706f2e70d40`；audit helper
SHA-256=`cb9e48f6fc8fc254e41915f91088f3ead62c27e57eb46e156db4fd261a65ef63`；
evaluator commit／SHA-256=`c3dcdff`／
`50d52c28781dd7f548f90268014b0848e5e2bb8dcbe4743f93c1a8d76509471a`。R2 seal重做了
EMA bytes、training contract、Stage1／decoder／teacher／stats／cache identity检查；较早的partial
audit `ebb92a99fc122b760adafa47cbeafc134b3aabb004fbcac89440cbe085dc895e`被R2明确supersede，
不作为canonical seal。

### Audited detail — §3.26 matched Camera-text dropout pure4,053 formal

两条no-source C0-LAT arm在同一5090 SSD worktree从零完成Camera `105K`，每臂
`13.44M` exposures；exact parent、v9 Stage1／owning decoder、frozen Human teacher、cache／
train-only stats、seed17、batch order、noise、runtime与evaluation protocol均匹配，唯一训练差异是
Camera-text dropout=`0.10`或`0.00`。由于训练前没有绑定独立validation split／cache，全部
`162,760`个可物化train IDs又已用于训练，两臂在首次pure-test access前共同冻结neutral scale
`1.0`与single-open pure4,053合同。这里的证据类别严格是**matched Camera-text-dropout training
ablation**；`cfg_guidance_enabled=false`，不产生CFG scale或controllability promotion证据。

formal评测覆盖同一ordered pure `N=4,053`，ID SHA-256=
`a0d7627ee827e36a229d33f9975f8417ae78b504cd5a6db1edf62cb1a9266b93`；Direct-H、
Direct-C与sequential均使用Euler50，`joint_parallel=false`、`is_causal=false`。Direct-H的fixed
samples与四项paired Human geometry在两臂间tensor-exact。

| version / run | mode | Human TMR ↑ / FDTMR ↓ | Camera CLaTr ↑ / FDCLaTr ↓ | caption F1 ↑ | r-FPD ↓ / Out ↓ |
| --- | --- | --- | --- | ---: | --- |
| v11 C0-LAT no-source drop0.10 / `sm_c0_lat_nosource_camtextdrop010_c105k_seed17_5090g2_r2_20260812` | Direct-H | `17.608446 / 99.390511` | — | — | — |
| v11 C0-LAT no-source drop0.10 / `sm_c0_lat_nosource_camtextdrop010_c105k_seed17_5090g2_r2_20260812` | Direct-C observed-H | — | `55.066975 / 22.295156` | `0.710181` | `0.875055 / 0.110521` |
| v11 C0-LAT no-source drop0.10 / `sm_c0_lat_nosource_camtextdrop010_c105k_seed17_5090g2_r2_20260812` | sequential Human→Camera | `17.608446 / 99.390511` | `52.678387 / 38.197651` | `0.642800` | `0.505727 / 0.078213` |
| v11 C0-LAT no-source drop0.00 / `sm_c0_lat_nosource_nodrop_c105k_seed17_5090g3_r2_20260812` | Direct-H | `17.608446 / 99.390511` | — | — | — |
| v11 C0-LAT no-source drop0.00 / `sm_c0_lat_nosource_nodrop_c105k_seed17_5090g3_r2_20260812` | Direct-C observed-H | — | `57.242012 / 19.488703` | `0.733595` | `0.862023 / 0.105909` |
| v11 C0-LAT no-source drop0.00 / `sm_c0_lat_nosource_nodrop_c105k_seed17_5090g3_r2_20260812` | sequential Human→Camera | `17.608446 / 99.390511` | `54.940334 / 31.276964` | `0.685531` | `0.495212 / 0.077305` |

| version / run | mode | Human global / root-aligned MPJPE ↓ m | Human root ADE / FDE ↓ m | Camera center ADE / FDE ↓ m | Camera rotation ↓ deg |
| --- | --- | --- | --- | --- | ---: |
| v11 C0-LAT no-source drop0.10 / `sm_c0_lat_nosource_camtextdrop010_c105k_seed17_5090g2_r2_20260812` | Direct-H | `0.842760 / 0.228751` | `0.758772 / 1.283039` | — | — |
| v11 C0-LAT no-source drop0.10 / `sm_c0_lat_nosource_camtextdrop010_c105k_seed17_5090g2_r2_20260812` | Direct-C observed-H | — | — | `1.423981 / 1.516389` | `29.851310` |
| v11 C0-LAT no-source drop0.10 / `sm_c0_lat_nosource_camtextdrop010_c105k_seed17_5090g2_r2_20260812` | sequential Human→Camera | `0.842760 / 0.228751` | `0.758772 / 1.283039` | `2.905080 / 3.004177` | `71.022073` |
| v11 C0-LAT no-source drop0.00 / `sm_c0_lat_nosource_nodrop_c105k_seed17_5090g3_r2_20260812` | Direct-H | `0.842760 / 0.228751` | `0.758772 / 1.283039` | — | — |
| v11 C0-LAT no-source drop0.00 / `sm_c0_lat_nosource_nodrop_c105k_seed17_5090g3_r2_20260812` | Direct-C observed-H | — | — | `1.401442 / 1.487820` | `29.332004` |
| v11 C0-LAT no-source drop0.00 / `sm_c0_lat_nosource_nodrop_c105k_seed17_5090g3_r2_20260812` | sequential Human→Camera | `0.842760 / 0.228751` | `0.758772 / 1.283039` | `2.905820 / 3.004678` | `70.530631` |

#### Matched dropout comparison and decision boundary

下表为`drop0.10 − drop0.00`的mean delta与95% percentile CI；lower-is-better Camera geometry
按4,053个ordered matched samples做10,000次bootstrap。aggregate semantic／framing没有逐样本
paired unit，只报告完整差值，不附造CI。

| comparison | mode | Camera ADE∆ / FDE∆ / rotation∆ | aggregate CLaTr∆ / FDCLaTr∆ / caption F1∆ / r-FPD∆ / Out∆ |
| --- | --- | --- | --- |
| drop0.10 − drop0.00 / matched no-source pair | Direct-C observed-H | `+0.022539 [-0.014427, +0.062036]` / `+0.028569 [-0.009663, +0.068672]` / `+0.519307 [-0.362747, +1.430821]` | `-2.175037 / +2.806454 / -0.023414 / +0.013033 / +0.004612` |
| drop0.10 − drop0.00 / matched no-source pair | sequential Human→Camera | `-0.000740 [-0.030354, +0.028779]` / `-0.000501 [-0.030967, +0.029494]` / `+0.491442 [-0.448575, +1.466452]` | `-2.261948 / +6.920687 / -0.042731 / +0.010515 / +0.000908` |

六项Camera geometry CI全部跨零；dropout `0.10`在Direct-C与sequential的CLaTr、FDCLaTr、caption
F1、r-FPD与Out这十个方向性aggregate字段上全部回退。故本次matched treatment被拒绝，保留
no-drop实现；不把dropout arm放入主表、不替换operational C0-LAT，也不声称统计显著的geometry退化。
该formal没有执行caption intervention，因而既不是Camera-text ownership证据，也不能关闭C3；CFG
guidance／controllability promotion永久不具资格。

#### Formal artifact identity

| version / run | training contract / Camera EMA SHA-256 | pure4053 / eval / fixed / records / results / manifest SHA-256 |
| --- | --- | --- |
| v11 C0-LAT no-source drop0.10 / `sm_c0_lat_nosource_camtextdrop010_c105k_seed17_5090g2_r2_20260812` | `dc9e3d9bd32b7a4f8d7836a0d57c8ffb153a73e36858930cd6c0dd00332ba3ac` / `0e2290d1972af311a7a09cc110a93d5a166857eff8482199001ee1c852ecafea` | `6396debcd81237dec755c04ca972353c0854ab45f8dd52c0f642e501ef4adc35` / `a723322f68dba1718565990a35cd2c0818b0f156297d78e776d0d1259e061295` / `f73b01e232b643c5525197bc6b9e1a355e8394f707f77c6adfe1c84e24fbb261` / `bf3663099a3d382910fa744d21889d8ca8e8c5b0e190082f8fecb56f55eb8b50` / `7401fd7b7e7edf8266bb473d222c0fdfc404827725cbdd26a76832bee36bbcf7` / `e098a3e9cdae891140e6393410cea321032274ee4a8e0f3f5a2a55c8c79402ef` |
| v11 C0-LAT no-source drop0.00 / `sm_c0_lat_nosource_nodrop_c105k_seed17_5090g3_r2_20260812` | `492ac6c5f1954abbafcef6ee3037e9bf28770b215c2e450e4da8d17396cd44a2` / `2f9092a789394a826fd3535fad1fd40c7bc3f29df95b1d109999476e32ac3c5d` | `3c427f033be286ba58713849695317dde2bbd6de6099bb4ff2ec8ef85ab2b744` / `e41ff9c43a1725afcd1bb222c186284bc8cdf55ab6d362d1b01368e0ce4fea10` / `3c3c18279bd58a9ecc8227e6e40404b9dfcc3701f958a974285fef9b1b3648c6` / `2fc2ae7484e8b0bb52d3429a792307b5c431a7c9f8140cb1234d9ebceced07c8` / `82115745294830dc9a44f3d9e3c10c1e9fee6723a5cb400df61f6b536a3326e3` / `781ead0399893651b0d2ee0ce43f6b667634bf093f9f51d4fbce4f8f72428c5d` |

两臂共享decoder／teacher／stats／train-cache SHA-256=
`51233f6a032c779e66b6eed4bb22b7f61c41d9b4a5a0a1ffc7dade7d3d86d4df`／
`3efd59481f8052b401889fce6559e31f96cb88f51dfb6c466464cf05ec6c2c50`／
`117d51a1d2ed1ae57541723b85c732118172634c57b2665f00b246c36e218558`／
`04add8e553af334e4724f08c7076a0be24f171470b938920120ef64fc7b01576`。paired audit
SHA-256=`9b63b9e952f8efb3e46da233f9e8d48ee747d259b1a537618f25687fd3caf923`；
audit commit=`6f3a8277fe7d307e960debcd02a28ef0e6330cbc`，script SHA-256=
`776664efe97e54d18c737a8a8dee9439a8ab4e7a3a441c8fefcf0e353974314c`。


## 4B. v9+ Stage1 audited detail tables

Original §§6.2–6.4 and §6.8 are retained below with complete v9+ pure4053 fields, projective diagnostics and matched audit hashes. Pre-v9 C3 rows are excluded and remain owned by the pre-v9 archive.

### Audited detail — original §6 Stage1 true-length paired reconstruction

| display ID | immutable provenance ID(s) | setting | goal |
| --- | --- | --- | --- |
| Pulp-only-v9 | owner `stage1_hanchor_pulp_only_matched_r3_636k_seed17_4090g0_20260726`; formal eval artifact `stage1_hanchor_pulp_only_matched_r3_636k_eval_r4_true4053_seed17_4090g0_20260727` | v9 Pulp-only non-causal owner; `H128+I16+C48`; exact-length round trip | canonical full-cohort Stage1 owner |
| NoInt-HREL | `sm_hrel_nointeraction16_stage1_636k_seed17_4090g0_r2_20260803` | HREL-derived owner with Interaction16 removed; `H128+C48` | test the interaction-token ablation |
| C1REL-Stage1 | `sm_c1rel_stage1_636k_seed17_4090g1_r2_20260803` | C1REL-C48 with `H128+I16`; world Camera14 decoder bridge | test the C1REL representation interface |
| C1REL-noI16-Stage1 | `sm_c1rel_nointeraction16_stage1_636k_seed17_4090g1_20260804` | C1REL-C48 with I16 removed | isolate the C1REL interaction-token ablation |
| HREL-C-old3loss | `v10_hrelcam_stage1_phasea210k_phaseb_camera48_210k_seed17_4090g0_20260729` | frozen Phase-A Human plus independent relative Camera48; historical `210K` | retain old Camera-only diagnostic boundary |
| HML+Pulp-v9 | `stage1_hanchor_hmlrootlocal_pulpfull_packedio_r3_636k_eval_r4_true4053_seed17_5090g2_20260727` | joint Pulp paired reconstruction with HML root/local branch | cross-domain/architecture diagnostic, not owner |
| Pulp-only-HML-val | `stage1_hanchor_pulp_only_matched_r3_636k_eval_r2_true_hmlval1460_seed17_5090g2_20260727` | HumanML3D `N=1,460` root/local Human-only round trip | cross-domain Human reconstruction diagnostic |
| HML+Pulp-HML-val | `stage1_hanchor_hmlrootlocal_pulpfull_packedio_r3_636k_eval_r2_true_hmlval1460_seed17_5090g2_20260727` | HumanML3D `N=1,460` root/local branch under Pulp normalization | cross-domain architecture diagnostic |

每一行是一个 distinct Stage1 run；HML3D rows 与 Pulp pure4,053 rows 的 cohort 和 reference distribution 不可互排名。

`Pulp-only-v9` 的 formal eval artifact就是C0-LAT／C0-GEO共同Stage1 owner的 deterministic
reconstruction floor。C0-LAT和C0-GEO只改变Stage2 Camera objective，不产生新的Stage1 checkpoint
或owning decoder，因此§6.2–§6.4不会再列一条“C0-LAT Stage1”。它与前述Stage2章节共享owner
provenance，但回答的是representation round-trip误差，而不是text-conditioned generation质量。

本节是 Stage1 deterministic encoder–decoder round trip，**不是** text-conditioned generation。所有样本先裁到自身 exact valid length，再进入 non-causal tokenizer；不存在固定首 `64` 帧裁切，也不让 future batch padding 进入 encoder。Pulp 与 HumanML3D 使用不同 cohort、观测字段和 reference distribution，禁止跨表排名。

#### Audited detail — original §6.1 Schema and protocol

| family | machine-readable keys | unit | direction / boundary |
| --- | --- | --- | --- |
| paired Human geometry | `human_global_mpjpe_m`, `human_root_aligned_mpjpe_m`, `human_root_ade_m`, `human_root_fde_m` | meter | ↓；root-aligned 仍保留 heading error |
| integrated heading | `human_wrapped_yaw_mean_deg`, `human_wrapped_yaw_final_deg`, `human_unwrapped_yaw_final_error_deg` | degree | ↓ |
| Camera trajectory | `camera_joint_center_ade_m`, `camera_joint_center_fde_m`, `camera_gt_human_anchor_center_ade_m`, `camera_gt_human_anchor_center_fde_m`, `camera_rotation_mean_deg`, `camera_fov_h_mean_abs_deg`, `camera_fov_w_mean_abs_deg` | meter / degree | ↓；GT-H anchor 行隔离 Human-root decode coupling |
| Human–Camera projective | `projective_joint_uv_l2_mean`, `projective_center_l2_mean`, `projective_log_scale_abs_mean`, `projective_out_ratio_abs_mean`, visible-joint fraction与 zero-visible frame rate | normalized screen / fraction | error、out、zero-visible ↓；visible fraction与 reference 对照 |
| decoded physical/kinematic | bone CV、joint/root speed/acceleration/jerk、foot contact/skate heuristic | decoded coordinate / frameⁿ / fraction | 每项均报告 `mean / median / p90`；只与同 cohort reference 对照 |

| version / run | mode | N / ordered IDs | sampler | evaluator | representation / owning decoder |
| --- | --- | --- | --- | --- | --- |
| Redesign Pulp-only / `stage1_hanchor_pulp_only_matched_r3_636k_eval_r4_true4053_seed17_4090g0_20260727` | joint paired reconstruction | 4,053 / [[Storymotion-exp-sha]] | deterministic exact-length owning encoder–decoder round trip；decode batch1 | redesign Pulp [[Storymotion-exp-sha]] | `human_anchor_interaction_residual_199_14_128_16_48_v1`；owning decoder [[Storymotion-exp-sha]] |
| NoInt-HREL / `sm_hrel_nointeraction16_stage1_636k_seed17_4090g0_r2_20260803` | matched joint paired reconstruction | 4,053 / ordered SHA `a0d7627e…6b93` | deterministic exact-length owning encoder–decoder round trip；decode batch1 | StoryMotion representation evaluator SHA `e6c8fb08…5eb0` | H128＋C48；显式I16删除；owning `D_h/D_c/D_f`；non-causal |
| C1REL / `sm_c1rel_stage1_636k_seed17_4090g1_r2_20260803` | matched joint paired reconstruction | 4,053 / ordered SHA `a0d7627e…6b93` | deterministic exact-length owning encoder–decoder round trip；decode batch1 | StoryMotion representation evaluator SHA `e6c8fb08…5eb0` | H128＋I16＋C1REL-C48；owning `D_h/D_c/D_f`恢复world Camera14；non-causal |
| C1REL-noI16 / `sm_c1rel_nointeraction16_stage1_636k_seed17_4090g1_20260804` | matched joint paired reconstruction | 4,053 / ordered SHA `a0d7627e…6b93` | deterministic exact-length owning encoder–decoder round trip；decode batch1 | StoryMotion representation evaluator SHA `cd4a4054…0218` | H128＋C1REL-C48；只删除I16；owning `D_h/D_c/D_f`；non-causal |
| v10 Human-relative Camera old-3-loss Phase B / `v10_hrelcam_stage1_phasea210k_phaseb_camera48_210k_seed17_4090g0_20260729` | historical `210K` Camera-only paired reconstruction diagnostic | 4,053 / [[Storymotion-exp-sha]] | deterministic exact-length owning encoder–decoder round trip；GT Human supplies inverse-relative reference | v10 native + canonical historical Stage1 endpoint evaluator [[Storymotion-exp-sha]] | frozen Phase-A Human128 owner + independent relative-Camera48 encoder/decoder；missing framing backprop；non-causal [[Storymotion-exp-sha]] |
| Redesign HML+Pulp / `stage1_hanchor_hmlrootlocal_pulpfull_packedio_r3_636k_eval_r4_true4053_seed17_5090g2_20260727` | joint paired reconstruction | 4,053 / [[Storymotion-exp-sha]] | deterministic exact-length owning encoder–decoder round trip；decode batch1 | redesign Pulp [[Storymotion-exp-sha]] | same redesigned architecture；owning decoder [[Storymotion-exp-sha]] |
| Redesign Pulp-only / `stage1_hanchor_pulp_only_matched_r3_636k_eval_r2_true_hmlval1460_seed17_5090g2_20260727` | HumanML3D Human-only root/local paired reconstruction diagnostic | 1,460 / [[Storymotion-exp-sha]] | deterministic exact-length owning Human encoder–decoder round trip；decode batch1 | redesign HumanML [[Storymotion-exp-sha]] | converted HML root/local under Pulp normalization；rot6D `4:136` prohibited mean-imputed/unobserved；decoder [[Storymotion-exp-sha]] |
| Redesign HML+Pulp / `stage1_hanchor_hmlrootlocal_pulpfull_packedio_r3_636k_eval_r2_true_hmlval1460_seed17_5090g2_20260727` | HumanML3D Human-only root/local paired reconstruction diagnostic | 1,460 / [[Storymotion-exp-sha]] | deterministic exact-length owning Human encoder–decoder round trip；decode batch1 | redesign HumanML [[Storymotion-exp-sha]] | converted HML root/local under Pulp normalization；rot6D `4:136` prohibited mean-imputed/unobserved；decoder [[Storymotion-exp-sha]] |

以上八条 contract 与 checkpoint 均显式 `is_causal=false`。历史 machine field `pose6d_policy` 是旧命名，实际指 Human199 channels `4:136` 的 joint rot6D；本页统一使用 **rot6D**。2026-07-27 的 policy correction 判定无显式 missingness 的 Pulp-mean填充为禁止的伪观测：上表 HML rows只保留已解码 root/local diagnostic 数值，mixed checkpoint不得进入正式 Stage2。


#### Audited detail — original §6.2 Pulp pure4,053 complete Human reconstruction

| display ID / canonical run alias | mode | N | global MPJPE ↓ m | root-aligned MPJPE ↓ m | root ADE ↓ m | root FDE ↓ m | wrapped yaw mean ↓ deg | wrapped yaw final ↓ deg | unwrapped yaw final ↓ deg |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Redesign Pulp-only / `stage1_hanchor_pulp_only_matched_r3_636k_eval_r4_true4053_seed17_4090g0_20260727` | joint paired reconstruction | 4,053 | 0.120708 | 0.042136 | 0.100757 | 0.248722 | 10.434 | 18.751 | 20.757 |
| NoInt-HREL / `sm_hrel_nointeraction16_stage1_636k_seed17_4090g0_r2_20260803` | matched joint paired reconstruction | 4,053 | 0.120919 | 0.042175 | 0.100965 | 0.249442 | 10.447 | 18.775 | 20.786 |
| C1REL / `sm_c1rel_stage1_636k_seed17_4090g1_r2_20260803` | matched joint paired reconstruction | 4,053 | 0.120705 | 0.042187 | 0.100737 | 0.248654 | 10.452 | 18.877 | 20.897 |
| C1REL-noI16 / `sm_c1rel_nointeraction16_stage1_636k_seed17_4090g1_20260804` | matched joint paired reconstruction | 4,053 | 0.129549 | 0.044328 | 0.109197 | 0.262747 | 11.529 | 20.634 | 22.739 |
| v10 HREL-C old-3-loss Phase-B / `v10_hrelcam_stage1_phasea210k_phaseb_camera48_210k_seed17_4090g0_20260729` | frozen-Human + Camera-only paired reconstruction | 4,053 | 0.133869 | 0.044779 | 0.112616 | 0.279547 | 11.897 | 21.218 | 23.622 |
| Redesign HML+Pulp / `stage1_hanchor_hmlrootlocal_pulpfull_packedio_r3_636k_eval_r4_true4053_seed17_5090g2_20260727` | joint paired reconstruction | 4,053 | 0.718084 | 0.212668 | 0.614757 | 1.136651 | 82.011 | 91.159 | 418.094 |


#### Audited detail — original §6.3 Pulp pure4,053 complete Camera and projective reconstruction

| display ID / canonical run alias | mode | N | joint Cam ADE ↓ m | joint Cam FDE ↓ m | GT-H Cam ADE ↓ m | GT-H Cam FDE ↓ m | rotation ↓ deg | FOV-H ↓ deg | FOV-W ↓ deg |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Redesign Pulp-only / `stage1_hanchor_pulp_only_matched_r3_636k_eval_r4_true4053_seed17_4090g0_20260727` | joint paired reconstruction | 4,053 | 0.037654 | 0.043840 | 0.026146 | 0.033668 | 0.575890 | 0.204003 | 0.262347 |
| NoInt-HREL / `sm_hrel_nointeraction16_stage1_636k_seed17_4090g0_r2_20260803` | matched joint paired reconstruction | 4,053 | 0.047452 | 0.067396 | 0.037331 | 0.059294 | 0.736642 | 0.230362 | 0.294394 |
| C1REL / `sm_c1rel_stage1_636k_seed17_4090g1_r2_20260803` | matched joint paired reconstruction | 4,053 | 0.044945 | 0.057538 | 0.035511 | 0.049641 | 0.820222 | 0.186437 | 0.307167 |
| C1REL-noI16 / `sm_c1rel_nointeraction16_stage1_636k_seed17_4090g1_20260804` | matched joint paired reconstruction | 4,053 | 1.501675 | 1.583464 | 1.500885 | 1.582966 | 38.977528 | 1.167162 | 1.834105 |
| v10 HREL-C old-3-loss Phase-B / `v10_hrelcam_stage1_phasea210k_phaseb_camera48_210k_seed17_4090g0_20260729` | frozen-Human + Camera-only paired reconstruction | 4,053 | 0.121757 | 0.377332 | 0.021567 | 0.173423 | 0.617630 | 2.265990 | 1.462458 |
| Redesign HML+Pulp / `stage1_hanchor_hmlrootlocal_pulpfull_packedio_r3_636k_eval_r4_true4053_seed17_5090g2_20260727` | joint paired reconstruction | 4,053 | 0.052681 | 0.058489 | 0.026317 | 0.034576 | 0.598872 | 0.197493 | 0.269706 |

| display ID / canonical run alias | mode | N | joint UV L2 ↓ | center L2 ↓ | log-scale abs ↓ | out-ratio abs ↓ | visible recon / ref ↔ reference | zero-visible recon / ref ↓ |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Redesign Pulp-only / `stage1_hanchor_pulp_only_matched_r3_636k_eval_r4_true4053_seed17_4090g0_20260727` | joint paired reconstruction | 4,053 | 0.160790 | 0.096190 | 0.029678 | 0.039550 | 0.484065 / 0.497732 | 0.023921 / 0.007547 |
| NoInt-HREL / `sm_hrel_nointeraction16_stage1_636k_seed17_4090g0_r2_20260803` | matched joint paired reconstruction | 4,053 | 0.180547 | 0.101843 | 0.031005 | 0.041164 | 0.484226 / 0.497732 | 0.023734 / 0.007547 |
| C1REL / `sm_c1rel_stage1_636k_seed17_4090g1_r2_20260803` | matched joint paired reconstruction | 4,053 | 0.157706 | 0.101260 | 0.029883 | 0.040497 | 0.485306 / 0.497732 | 0.024223 / 0.007547 |
| C1REL-noI16 / `sm_c1rel_nointeraction16_stage1_636k_seed17_4090g1_20260804` | matched joint paired reconstruction | 4,053 | 4.741876 | 1.157589 | 0.360707 | 0.306611 | 0.227098 / 0.497732 | 0.393948 / 0.007547 |
| v10 HREL-C old-3-loss Phase-B / `v10_hrelcam_stage1_phasea210k_phaseb_camera48_210k_seed17_4090g0_20260729` | frozen-Human + Camera-only paired reconstruction | 4,053 | 0.353564 | 0.107943 | 0.066030 | 0.041602 | 0.497488 / 0.497732 | 0.012102 / 0.007547 |
| Redesign HML+Pulp / `stage1_hanchor_hmlrootlocal_pulpfull_packedio_r3_636k_eval_r4_true4053_seed17_5090g2_20260727` | joint paired reconstruction | 4,053 | 0.848923 | 0.343268 | 0.132111 | 0.122139 | 0.435095 / 0.497732 | 0.118101 / 0.007547 |

#### Audited detail — original §6.4 Pulp pure4,053 complete decoded physical/kinematic summary


每个 cell 是 `mean / median / p90`。这些是 reconstruction output，不是 free generation；contact/skate 使用 own-motion floor heuristic，不是 calibrated ground metric。

| display ID / canonical run alias | mode | N | bone CV ↓ | joint speed ↔ reference | joint acceleration ↔ reference | joint jerk ↔ reference |
| --- | --- | ---: | ---: | ---: | ---: | ---: |
| Pulp dataset reference / pure4053 | reference | 4,053 | 2.677e-7 / 2.376e-7 / 3.423e-7 | 0.034022 / 0.020797 / 0.078097 | 0.024906 / 0.014389 / 0.056310 | 0.038199 / 0.021969 / 0.087722 |
| Redesign Pulp-only / `stage1_hanchor_pulp_only_matched_r3_636k_eval_r4_true4053_seed17_4090g0_20260727` | joint paired reconstruction | 4,053 | 0.026000 / 0.020484 / 0.050117 | 0.035668 / 0.022309 / 0.079710 | 0.028277 / 0.017335 / 0.062101 | 0.043172 / 0.026360 / 0.094611 |
| NoInt-HREL / `sm_hrel_nointeraction16_stage1_636k_seed17_4090g0_r2_20260803` | matched joint paired reconstruction | 4,053 | 0.026001 / 0.020474 / 0.050088 | 0.035671 / 0.022296 / 0.079721 | 0.028280 / 0.017332 / 0.062071 | 0.043178 / 0.026340 / 0.094728 |
| C1REL / `sm_c1rel_stage1_636k_seed17_4090g1_r2_20260803` | matched joint paired reconstruction | 4,053 | 0.026002 / 0.020492 / 0.050089 | 0.035668 / 0.022325 / 0.079727 | 0.028276 / 0.017322 / 0.062056 | 0.043168 / 0.026369 / 0.094644 |
| C1REL-noI16 / `sm_c1rel_nointeraction16_stage1_636k_seed17_4090g1_20260804` | matched joint paired reconstruction | 4,053 | 0.024529 / 0.019159 / 0.046883 | 0.035715 / 0.022362 / 0.079895 | 0.028261 / 0.017301 / 0.062335 | 0.043168 / 0.026352 / 0.094779 |
| v10 HREL-C old-3-loss Phase-B / `v10_hrelcam_stage1_phasea210k_phaseb_camera48_210k_seed17_4090g0_20260729` | frozen-Human + Camera-only paired reconstruction | 4,053 | 0.021380 / 0.016591 / 0.041141 | 0.035518 / 0.022162 / 0.079693 | 0.027760 / 0.016814 / 0.061350 | 0.042220 / 0.025519 / 0.093351 |
| Redesign HML+Pulp / `stage1_hanchor_hmlrootlocal_pulpfull_packedio_r3_636k_eval_r4_true4053_seed17_5090g2_20260727` | joint paired reconstruction | 4,053 | 0.037738 / 0.030727 / 0.069701 | 0.052227 / 0.038916 / 0.104918 | 0.037689 / 0.025133 / 0.080011 | 0.052494 / 0.034237 / 0.111604 |

| display ID / canonical run alias | mode | N | root speed ↔ reference | root acceleration ↔ reference | root jerk ↔ reference | contact heuristic ↔ reference | foot skate heuristic ↓ |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Pulp dataset reference / pure4053 | reference | 4,053 | 0.029456 / 0.016709 / 0.067934 | 0.017055 / 0.009513 / 0.039636 | 0.023314 / 0.013070 / 0.053262 | 0.492193 / 0.428571 / 1.000000 | 0.039121 / 0.021590 / 0.079352 |
| Redesign Pulp-only / `stage1_hanchor_pulp_only_matched_r3_636k_eval_r4_true4053_seed17_4090g0_20260727` | joint paired reconstruction | 4,053 | 0.030292 / 0.017515 / 0.069146 | 0.019719 / 0.011587 / 0.043854 | 0.027753 / 0.016438 / 0.061139 | 0.484022 / 0.421053 / 0.999598 | 0.039454 / 0.023312 / 0.082005 |
| NoInt-HREL / `sm_hrel_nointeraction16_stage1_636k_seed17_4090g0_r2_20260803` | matched joint paired reconstruction | 4,053 | 0.030293 / 0.017522 / 0.069152 | 0.019722 / 0.011590 / 0.043833 | 0.027757 / 0.016450 / 0.061155 | 0.483933 / 0.421429 / 0.999598 | 0.039482 / 0.023321 / 0.081861 |
| C1REL / `sm_c1rel_stage1_636k_seed17_4090g1_r2_20260803` | matched joint paired reconstruction | 4,053 | 0.030291 / 0.017520 / 0.069149 | 0.019718 / 0.011575 / 0.043866 | 0.027746 / 0.016434 / 0.061189 | 0.483900 / 0.420455 / 0.999598 | 0.039503 / 0.023321 / 0.081758 |
| C1REL-noI16 / `sm_c1rel_nointeraction16_stage1_636k_seed17_4090g1_20260804` | matched joint paired reconstruction | 4,053 | 0.030311 / 0.017568 / 0.069343 | 0.019653 / 0.011535 / 0.043463 | 0.027627 / 0.016403 / 0.060805 | 0.485326 / 0.424242 / 0.996774 | 0.039549 / 0.023427 / 0.082139 |
| v10 HREL-C old-3-loss Phase-B / `v10_hrelcam_stage1_phasea210k_phaseb_camera48_210k_seed17_4090g0_20260729` | frozen-Human + Camera-only paired reconstruction | 4,053 | 0.030211 / 0.017454 / 0.069245 | 0.019525 / 0.011400 / 0.043384 | 0.027378 / 0.016122 / 0.060866 | 0.496643 / 0.443182 / 1.000000 | 0.039378 / 0.023089 / 0.082767 |
| Redesign HML+Pulp / `stage1_hanchor_hmlrootlocal_pulpfull_packedio_r3_636k_eval_r4_true4053_seed17_5090g2_20260727` | joint paired reconstruction | 4,053 | 0.030462 / 0.017899 / 0.069392 | 0.021257 / 0.012494 / 0.046893 | 0.029491 / 0.017673 / 0.063758 | 0.480031 / 0.415730 / 0.986771 | 0.061342 / 0.042012 / 0.127044 |


#### Audited detail — §6.5 Phase-C gradient／update protection controls

本节登记同一 v9 Phase-B `420K` parent 上的 Phase-C `216K` matched causal audit。A0 是现有
Pulp-only v9 owner 的原始 Phase-C；A1 只关闭 Camera loss 到 Human encoder 的梯度，仍用 Human
loss 更新 Human encoder／decoder；A2 在相同 `G=off` 边界进一步关闭 Phase-C Human 更新。三臂
使用相同 non-causal `H128+I16+C48` 拓扑、parent checkpoint SHA-256
`0bc677c173eae3330757de62418059ed1176d7359221fe648c10eef3d6f048d8`、seed17、重建后的同一
batch order、`162,760/4,053` train／eval IDs 和 `216,000 × 128 = 27,648,000` Phase-C exposures。

| version / run | Camera→Human `G` | Phase-C Human update `U` | endpoint update boundary | endpoint checkpoint SHA-256 | training contract SHA-256 |
| --- | --- | --- | --- | --- | --- |
| A0 current owner / `stage1_hanchor_pulp_only_matched_r3_636k_seed17_4090g0_20260726` | on | on | `216,000 / 216,000` | `51233f6a032c779e66b6eed4bb22b7f61c41d9b4a5a0a1ffc7dade7d3d86d4df` | `96552a68699bb6c9dd694a19e8a4147d6ddf2f2c997c53aed93532e461f6cc28` |
| A1 G-off, U-on / `sm_stage1_phasec_g0_u1_seed17_4090g0_20260812` | off | on | `216,000 / 216,000` | `626acf50e65a552a0e34442d5c223182ff21d556d300501f7d8424b55c339193` | `6bdefebf8c781a1d00a40fb1cd61806a42d23424eb51b1e60d29a7f29c7292b5` |
| A2 G-off, U-off / `sm_stage1_phasec_g0_u0_seed17_4090g1_20260812` | off | off | `151,200 parameter updates / 64,800 intentional no-update anchor boundaries` | `94407e46ee7eac7681a925cd31e83f6510bea602f5df953939826b7a7782e569` | `157a71f244a7e7cb9580d616aa8440b5cfe554e8186ab03f8455923c3ee59563` |

A1／A2 midpoint与endpoint均 atomic-save、reload-verified；endpoint全状态含 model、optimizer、RNG、sampler、
scheduler、contract／code／host／device provenance。A1／A2 training revision为`0e0b15c2`。preflight 分别验证
Camera loss 对 Human encoder／decoder exact-zero gradient、A1 Human loss 对两者非零 gradient，以及 A2
frozen Human parameter hash 不变。

##### Formal artifact identity

三臂 formal 均使用相同 evaluator SHA-256
`66f64cc8add76ea941a972d8a197cab380a85dadd1913fcedb0e0da312458b3a`、pure-test `N=4,053`、ordered-ID
SHA-256 `a0d7627ee827e36a229d33f9975f8417ae78b504cd5a6db1edf62cb1a9266b93`、batch `128`、
true-length decode batch `1` 和 exact owning decoder。A0 artifact identity已在§6.1–§6.4登记；下表只新增
A1／A2 bytes，避免重复登记 A0 数字。

| version / run | evaluation contract SHA-256 | fixed samples SHA-256 | result SHA-256 | records SHA-256 | eval manifest SHA-256 |
| --- | --- | --- | --- | --- | --- |
| A1 G-off, U-on / `sm_stage1_phasec_g0_u1_seed17_4090g0_20260812` | `58c23ecbee64a3b14329f493336b2568667c14f1d899a998a6fcfabe50ccb769` | `b4bb1255c2ed5219b67c5bdd61a6dcce61bf06a428ff8c6f95e05d37e6c12680` | `2ee476643efc31e781c76838c15bfd990bd8827f84322d00eb2227beabd22615` | `5c8681fec7a6cb025f647af1aca0277b635a1c6690a32e2c1fb9bdccc6c28ca2` | `89b79850ea05872d09a95a9d84d96d74f8594a0f01da5115ec1d276b146a16cc` |
| A2 G-off, U-off / `sm_stage1_phasec_g0_u0_seed17_4090g1_20260812` | `bb63c60d9f39d0f43f1774dc8b5a82118a1b8bed09ab9a41c93b433231fd3452` | `d84fd3718c3a958a5ad5c2ab1f0c6c0c4c675ecbb975dba6e0e9b7e43f7ab219` | `da06172b8e28d873e56072de1af7b7900d050e1a77137dea92ce5ebdec8ec43a` | `dd6c996a62de99265b218d9ee7b0c91ec061715961862db4aae625996cee3a51` | `d665ac6a2d3bfc65a67b10cb7d80911dd5a4db8ad065b54718fe4c78f01aee07` |

##### Formal reconstruction aggregates

以下是 deterministic Stage1 reconstruction，不是 text-conditioned generation。Human root-aligned MPJPE
移除 root translation，但仍保留 heading error。

| version / run | N | global / root-aligned MPJPE ↓ m | root ADE / FDE ↓ m | yaw mean / final / unwrapped final ↓ deg |
| --- | ---: | --- | --- | --- |
| A1 G-off, U-on / `sm_stage1_phasec_g0_u1_seed17_4090g0_20260812` | 4,053 | `0.120762 / 0.042260` | `0.100764 / 0.248305` | `10.4740 / 18.9520 / 20.9692` |
| A2 G-off, U-off / `sm_stage1_phasec_g0_u0_seed17_4090g1_20260812` | 4,053 | `0.133869 / 0.044779` | `0.112616 / 0.279547` | `11.8966 / 21.2175 / 23.6222` |

| version / run | joint Cam ADE / FDE ↓ m | GT-H Cam ADE / FDE ↓ m | rotation ↓ deg | FOV-H / FOV-W ↓ deg |
| --- | --- | --- | ---: | --- |
| A1 G-off, U-on / `sm_stage1_phasec_g0_u1_seed17_4090g0_20260812` | `0.037729 / 0.043980` | `0.026170 / 0.033787` | 0.575230 | `0.203853 / 0.262149` |
| A2 G-off, U-off / `sm_stage1_phasec_g0_u0_seed17_4090g1_20260812` | `0.035537 / 0.041679` | `0.024328 / 0.031843` | 0.556322 | `0.192442 / 0.247522` |

| version / run | joint UV / center L2 ↓ | log-scale / out-ratio abs ↓ | visible recon / reference ↔ | zero-visible recon / reference ↓ |
| --- | --- | --- | --- | --- |
| A1 G-off, U-on / `sm_stage1_phasec_g0_u1_seed17_4090g0_20260812` | `0.161031 / 0.096820` | `0.029860 / 0.039690` | `0.483917 / 0.497732` | `0.024163 / 0.007547` |
| A2 G-off, U-off / `sm_stage1_phasec_g0_u0_seed17_4090g1_20260812` | `0.164988 / 0.100944` | `0.030390 / 0.041214` | `0.481314 / 0.497732` | `0.026834 / 0.007547` |

两条 result artifact 均另含相同 `1-64/65-128/129-192/193+` bins，样本数分别为
`1,805/1,411/456/381`；length `min/median/p90/max=9/71/188/251`。完整逐 bin 字段由上表
`results.json` hash 唯一拥有。

##### Decoded-Human physical／kinematic diagnostics

每个 cell 为 `mean / median / p90`；仍是 reconstruction heuristic，不是 calibrated physical-validity。

| version / run | bone CV ↓ | joint speed | joint acceleration | joint jerk |
| --- | --- | --- | --- | --- |
| A1 G-off, U-on / `sm_stage1_phasec_g0_u1_seed17_4090g0_20260812` | `0.026013 / 0.020494 / 0.050116` | `0.035670 / 0.022322 / 0.079735` | `0.028279 / 0.017334 / 0.062094` | `0.043176 / 0.026409 / 0.094687` |
| A2 G-off, U-off / `sm_stage1_phasec_g0_u0_seed17_4090g1_20260812` | `0.021380 / 0.016591 / 0.041141` | `0.035518 / 0.022162 / 0.079693` | `0.027760 / 0.016814 / 0.061350` | `0.042220 / 0.025519 / 0.093351` |

| version / run | root speed | root acceleration | root jerk | contact | foot skate ↓ |
| --- | --- | --- | --- | --- | --- |
| A1 G-off, U-on / `sm_stage1_phasec_g0_u1_seed17_4090g0_20260812` | `0.030291 / 0.017516 / 0.069141` | `0.019718 / 0.011582 / 0.043867` | `0.027752 / 0.016471 / 0.061080` | `0.484014 / 0.420455 / 0.999598` | `0.039462 / 0.023296 / 0.081835` |
| A2 G-off, U-off / `sm_stage1_phasec_g0_u0_seed17_4090g1_20260812` | `0.030211 / 0.017454 / 0.069245` | `0.019525 / 0.011400 / 0.043384` | `0.027378 / 0.016122 / 0.060866` | `0.496643 / 0.443182 / 1.000000` | `0.039378 / 0.023089 / 0.082767` |

##### Paired causal audit and decision boundary

10,000-draw sample-paired bootstrap使用seed17。comparison／manifest SHA-256分别为
`a8893f4e6511576da4dd238a051969c22512511dc2625c75a31850c6414000c1`／
`d97cd613abb67e4f621fd77a748041b6edab2113257ce7120a792e6f2c51932a`；comparator SHA-256为
`edc8652452350a5f99413619edcb8347941a83d379ccdb5a1d480cdf31a184c0`，revision=`5901ace7`。
每个 cell 是 `arm − reference [95% CI]`，误差项正值表示回退。

| comparison | global / root-aligned MPJPE Δ m | root ADE / FDE Δ m | yaw mean / final / unwrapped final Δ deg |
| --- | --- | --- | --- |
| A1−A0：在 `U=on` 时关闭 `G` | `+0.000054 [-0.001067, +0.001026]` / `+0.000124 [-0.000030, +0.000278]` | `+0.000007 [-0.001088, +0.000962]` / `-0.000417 [-0.003704, +0.002525]` | `+0.0401 [-0.0066, +0.0873]` / `+0.2009 [+0.0938, +0.3072]` / `+0.2118 [+0.1046, +0.3184]` |
| A2−A1：在 `G=off` 时关闭 `U` | `+0.013106 [+0.008677, +0.018214]` / `+0.002519 [+0.001552, +0.003460]` | `+0.011853 [+0.007513, +0.016892]` / `+0.031242 [+0.019684, +0.044226]` | `+1.4226 [+1.1778, +1.6658]` / `+2.2656 [+1.7820, +2.7673]` / `+2.6531 [+2.0845, +3.2424]` |

| comparison | joint Cam ADE / FDE Δ m | GT-H Cam ADE / FDE Δ m | rotation Δ deg | projective center / out / zero-visible Δ |
| --- | --- | --- | --- | --- |
| A1−A0：在 `U=on` 时关闭 `G` | `+0.000076 [+0.000035, +0.000118]` / `+0.000139 [+0.000073, +0.000210]` | `+0.000025 [-0.000029, +0.000080]` / `+0.000119 [+0.000037, +0.000204]` | `-0.000661 [-0.001056, -0.000298]` | `+0.000629 [+0.000130, +0.001119]` / `+0.000139 [-0.000103, +0.000364]` / `+0.000242 [-0.000165, +0.000650]` |
| A2−A1：在 `G=off` 时关闭 `U` | `-0.002193 [-0.002430, -0.001973]` / `-0.002301 [-0.002602, -0.002021]` | `-0.001843 [-0.002048, -0.001642]` / `-0.001944 [-0.002232, -0.001663]` | `-0.018908 [-0.020836, -0.016988]` | `+0.004124 [+0.001671, +0.006760]` / `+0.001524 [+0.000652, +0.002459]` / `+0.002671 [+0.001168, +0.004222]` |

审计裁决：A1−A0 的大多数 Human 项跨零，但两个 final-yaw 字段、微小 Camera／projective 字段形成
mixed effect；它不支持“Camera gradient 普遍有害”，也不能在结果后把近零均值改写成预注册
non-inferiority。A2−A1 的全部 Human geometry／yaw CI 均在零上，同时 Camera trajectory／rotation
改善而 projective center、out-ratio、visible fraction与zero-visible回退，证明关闭 Phase-C Human更新
不是免费的 protection，而是明确的 Human–Camera Pareto trade-off。

计划要求 endpoint 前封存 numeric non-inferiority margin，但没有找到已封存的数值 margin；comparison
因此 fail closed 为`stage2_authorized=false`、`stage1_owner_replacement_authorized=false`。不选择 protected
arm、不建新 cache／stats／Stage2；保留现有 A0 Stage1 owner。paper 只能写 finalized Stage1 后的 frozen-Human
保证，并把“Stage1 Phase-C 仍需要 Human-loss更新；Camera→Human gradient的效果很小且mixed”作为审计边界。


#### Audited detail — original §6.8 NoInt-HREL／C1REL／C1REL-noI16 matched Stage1 audit

reference、NoInt-HREL、C1REL与C1REL-noI16使用相同Pulp pure4,053 ordered IDs、
真实有效长度、seed17、non-causal边界、deterministic owning encoder–decoder round trip和canonical
Camera14 raw bridge。paired bootstrap以sample为单位做10,000次重采样，seed `17`；下表cell均为
`arm − HREL reference [95% CI]`。误差项正值表示回退。

| version / run | global MPJPE ↓ m | root-aligned MPJPE ↓ m | root ADE ↓ m | root FDE ↓ m |
| --- | ---: | ---: | ---: | ---: |
| NoInt-HREL / `sm_hrel_nointeraction16_stage1_636k_seed17_4090g0_r2_20260803` | 0.000211 [-0.000072, 0.000513] | 0.000039 [-0.000010, 0.000086] | 0.000208 [-0.000077, 0.000506] | 0.000720 [0.000005, 0.001454] |
| C1REL / `sm_c1rel_stage1_636k_seed17_4090g1_r2_20260803` | -0.000002 [-0.000886, 0.000759] | 0.000052 [-0.000072, 0.000170] | -0.000020 [-0.000896, 0.000733] | -0.000069 [-0.002813, 0.002382] |
| C1REL-noI16 / `sm_c1rel_nointeraction16_stage1_636k_seed17_4090g1_20260804` | 0.008842 [0.005645, 0.012002] | 0.002192 [0.001501, 0.002885] | 0.008440 [0.005288, 0.011559] | 0.014025 [0.005111, 0.022876] |

| version / run | joint Cam ADE ↓ m | joint Cam FDE ↓ m | GT-H Cam ADE ↓ m | GT-H Cam FDE ↓ m | rotation ↓ deg |
| --- | ---: | ---: | ---: | ---: | ---: |
| NoInt-HREL / `sm_hrel_nointeraction16_stage1_636k_seed17_4090g0_r2_20260803` | 0.009798 [0.008764, 0.010824] | 0.023556 [0.021871, 0.025231] | 0.011186 [0.010050, 0.012295] | 0.025626 [0.023850, 0.027372] | 0.160751 [0.134838, 0.196613] |
| C1REL / `sm_c1rel_stage1_636k_seed17_4090g1_r2_20260803` | 0.007291 [0.006396, 0.008184] | 0.013697 [0.012359, 0.015063] | 0.009365 [0.008420, 0.010329] | 0.015973 [0.014574, 0.017384] | 0.244332 [0.182620, 0.326526] |
| C1REL-noI16 / `sm_c1rel_nointeraction16_stage1_636k_seed17_4090g1_20260804` | 1.464021 [1.410848, 1.517311] | 1.539623 [1.483981, 1.594844] | 1.474739 [1.421337, 1.527961] | 1.549298 [1.493371, 1.604674] | 38.401637 [37.393106, 39.404047] |

| version / run | joint UV L2 ↓ | center L2 ↓ | log-scale abs ↓ | paired Out error ↓ |
| --- | ---: | ---: | ---: | ---: |
| NoInt-HREL / `sm_hrel_nointeraction16_stage1_636k_seed17_4090g0_r2_20260803` | 0.019756 [0.001759, 0.041305] | 0.005653 [0.003732, 0.007953] | 0.001327 [0.000812, 0.001889] | 0.001613 [0.000936, 0.002308] |
| C1REL / `sm_c1rel_stage1_636k_seed17_4090g1_r2_20260803` | -0.003085 [-0.025255, 0.018458] | 0.005069 [0.003204, 0.007278] | 0.000205 [-0.000615, 0.000989] | 0.000947 [0.000379, 0.001525] |
| C1REL-noI16 / `sm_c1rel_nointeraction16_stage1_636k_seed17_4090g1_20260804` | 4.581085 [4.209556, 4.992013] | 1.061399 [1.034197, 1.089261] | 0.331029 [0.321917, 0.340305] | 0.267061 [0.260354, 0.273892] |

严格组件问题的主比较是`C1REL-noI16 − C1REL`，因为它只删除I16。该比较的Human
global／root-aligned MPJPE、root ADE／FDE与wrapped-yaw mean，Camera joint／GT-H
ADE／FDE、rotation、FOV-H／FOV-W，以及四项projective error共16项95% CI全部在零上方。
其中joint Cam ADE差为`1.456730 [1.403823, 1.509794] m`，rotation差为
`38.157305 [37.161044, 39.148231]°`，joint UV差为
`4.584170 [4.214516, 4.995502]`。因此D在Stage1形成广泛且量级显著的退化。这是有效的正向
ablation evidence：在仅删除I16的strict C1REL合同下，简单的Interaction16对owning
reconstruction／framing有效且不可直接删除。该结果仍不外推为free-generation中的单组件必要性；
作者已单独决定后续补充matched Stage2，在该结果产生前只写Stage1有效性。

NoInt-HREL的Human均值基本保持，只有root FDE出现极小的正差；五项Camera geometry和四项projective
error的CI均在零上方。因此本Stage1证据支持“删除显式I16会损害owning reconstruction／framing”，
但不单独证明Stage2 generation中的I16必要，更不能扩写为Camera不依赖Human。C1REL同样守住Human，
但五项Camera geometry均回退，projective center／Out也回退，joint UV与scale没有稳健差异；它没有
形成可晋升的稳定Pareto。Stage1不消费Camera text，不能从本artifact声称C1REL text adherence改善。

预声明只写了“严重退化可降级”，没有冻结数值阈值；因此formal artifact本身不事后发明binary
severe gate，也不把C1REL直接判为最终失败。2026-08-05作者在看到完整formal结果后另行授权未来
C1REL-noI16 matched Stage2；这是新的决策层事件，不回写Stage1 artifact，也不预先宣称generation
结论。HREL继续保持当前representation owner。

NoInt-HREL checkpoint／training contract／evaluation contract／result／records／fixed-samples／eval-manifest
SHA256依次为`968133147d7e1b1202e5bf9ff5e046ae8ff0c592573361821804a1823562ef75`、
`599faf76f1b019d9d64160cab6e6d3c292a4befb5e1165d4bb54e35979877f66`、
`368f4dd1c8641766dcc8ff952af25881b316aee4218992f0e9e44cb145175078`、
`f946e0f29246143258d2bc5d0359b7a8950c9c2509584fb6fb604c2fcb542045`、
`56256318aff641496ddf0d699595c13b92ece7b641f5085fca14aa44c38036c9`、
`bad0e437eeeb8d2ed967d014cd164113592233c231d07efa7475a96164a14150`、
`7f5502be47864471f3ef92de803521f64a6fcb92831efd061fc38c59aa64eb2e`。

C1REL对应SHA256依次为`5af7317fcaea0694b457cecf7a106b5ecd26e8acdfbe47a7bd6571cebc0017f0`、
`745ff16cc853ce20de6c86690dcc8a9569c2cf4a9a1ce8cb8ab12f959fd0e9c2`、
`e5679b14d9e997bdafc28638796a19ce9c5ba98a8661ea3f43558b44503f50dd`、
`dd3c0ac1cea438659a2071679275e4225ba7bde96aa92bbc3c8cd3841f92b267`、
`b5685a7ee650e248c7da05893e6f73b5c39fba65487463478e454c1ab1cc71d0`、
`c36afd833e5823cea22e179027763ed0b641af0c738aeca518dcafb089c01e69`、
`cecf75f6f527cfb39907df7f5d02e1d2e60daebaa7f471af3cab9d5f2d2453b1`。

C1REL-noI16对应SHA256依次为`b8b572d5562f0946896ac9fc6af866d9ea636c9460e461628b81bb2d2329be0b`、
`fa0a2d1192a9e11e390bd57997031b58bddafafda84c9c68878ee820b799f588`、
`320580ac1bf0eb5e0cf7593ee3a42459652b66d04b0423d4d7650ae82fe92907`、
`6113bee975fb7a1e205afc5b497bc23a0a55112be90d4f6cd345493181267823`、
`5b5555573fc77c84bd47e67b21da11f7e7f4e2c37c1edebda4643dd0bfffc851`、
`712b9089fd06041f9fd69cf60fbb002422a2172376d9bd0543fa107c8e4c9c37`、
`563b8fc47c821592e7b1597ccb81373bd355afe4de61c21bde2f4f819331243e`。
三路paired comparison artifact／manifest SHA256分别为
`ce21952d67b5f2b5532fdf4be494dcdf9f40d97aa8dd92f3816beb6107792bac`／
`09a5e8ca807643f4a7a375582024f3197e1b5b99954408c186e62ee598c4cc51`；后者由run root
`sm_c1rel_nointeraction16_formal_paired4053_bootstrap10000_seed17_4090cpu_20260805`
拥有。该artifact只提供Stage1证据；未来Stage2授权与结果必须由独立run contract拥有。
cross-arm comparison／manifest SHA256为
`b6fe50d255cd574385f8dcb75bc1eb7692371f8c770bb780674cb84b3afc2bed`／
`dd89f88bb4fb08dc4cb0bb2dd8d2b126025e33117c983d6e7a20557c9700d254`；formal evaluator与
comparison evaluator SHA256为`e6c8fb08f830b24dd2d36bedd4a3942065e807029149d073a67e14fb5e625eb0`／
`c577b1d81d00200cdc24964994c15e7c1a62c53f49a43bf2dbbdfbc273c83e95`。

### Audited detail — original §6.9 fully independent Human／Camera Stage1 native-system audit

| display ID | canonical sm_ run alias | owner boundary | role |
| --- | --- | --- | --- |
| independent-H | `sm_independent_encdec_h199_h128_210k_seed17_4090g1_20260811` | Human199→H128；独立encoder、decoder、optimizer、checkpoint与branch-specific normalizer fields | secondary native Human Stage1 system |
| independent-C | `sm_independent_encdec_c2w14_c64_210k_seed17_4090g1_20260811` | world-C2W14→C64；独立encoder、decoder、optimizer、checkpoint与branch-specific normalizer fields；learned path不读Human | secondary native Camera Stage1 system |

两条fresh non-causal Stage1 run使用exact Pulp train/eval ordered cohorts=`162,760/4,053`、seed17和
train-only statistics；各自完成`210K` optimizer steps并原子保存／reload验证`105K`与`210K`
full-state checkpoint。两branch没有共享learned parameter、optimizer、checkpoint或decoder；Camera
cache只在materialization时用factual paired Human把HREL distance还原为absolute C2W center，训练consumer
与learned Camera model不再读取Human。train/eval cache index SHA-256分别为
`af8825ee56c0268c7b5dcd89a4034c29a46ad66f8737c2e53a040e0aff94fea6`／
`f586ce46bd307ee5e2a737c5e933614d0e39f039c5b27e8008e7f8ad11381abf`。共同的只读
`normalizer_stats.pt`容器分别保存train-only Human199与C2W14 mean/std；两consumer只加载各自字段，
没有跨branch normalization。该artifact SHA-256=
`073e52ad4a7ca7794463bc750f102ffc3dd16316ff776e0d7cf058997545e71a`。

#### Formal artifact identity

| version / run | endpoint | checkpoint / model-state SHA-256 | evaluation contract SHA-256 | fixed samples SHA-256 | records / results SHA-256 | manifest / endpoint seal SHA-256 |
| --- | ---: | --- | --- | --- | --- | --- |
| independent-H / `sm_independent_encdec_h199_h128_210k_seed17_4090g1_20260811` | 105K | `9689eef98b7df83a228fd91968164b3d84f5a36be9ce44126f52a975be1cca84` / `e881627b8633149827796473eb6e0d227dc897daaea35bb312e20021a2a981f4` | `744592b436c2fdde73f919153212cb891f820270a3ccce58821a5ec01527255b` | `ffad8d5e822ce3f8fa083d522192feb91f578d899e002d6c8c921d707f3af8ff` | `712df2ec210e40f343540397fce585911bbfadcd334d2f5d81ea6d6e8f09a61e` / `2b84a7736f4f7b6c7f6879d5e5db23f6e1f8238e93082427666a5ca309f6fef2` | `31d560f4cdaac6fa6b89ffa769dc9cbbf0a930764f4734dd66c7dc402c1bad7c` / `460e359afa802cda743e35b8dbe9c0eb777e11bc1e4b39867610d1ecb29d55ae` |
| independent-H / `sm_independent_encdec_h199_h128_210k_seed17_4090g1_20260811` | 210K | `9b46896520431bb22f866c159700e0557439cab17464567fe3a5b592c96d24e9` / `fb84e4eac399f289ba5a2d195777b1145dc2877ee8f021ec9ff27fd2faed0277` | `09259c7b7cb042cb3eba47f2637e136965265131a2a0f127881e8d330d8ed582` | `61e852c0476feec6ef4454aced02cde50b3499c2f0ec96a4ac389448249e1b02` | `c321698d85d7eb8083de34d841ec511abc99d6fca2e7c9051b26d8f591fc7da2` / `11a9455c5aab8889df7100449b0d6cfcb8ec914465cc67112f1232ed48d99398` | `54b53ec182b48fc62f9d8d643a0b639804d86253d315daf6c9156a70c59a9083` / `0e22f5c003b63b8d74a00b4aea59aa520430d9e04770f8ac61bbb581986c9bcf` |
| independent-C / `sm_independent_encdec_c2w14_c64_210k_seed17_4090g1_20260811` | 105K | `3d190b130d082362d8c5471807c3c9380c49b8f65a0e5b38525954859ebe61ee` / `81b88fe9d00ede260e53cc7851ab04c159fbb9ff6ca11998cab167013abc3367` | `d5bf36f28980018ecfd7156122d06a2ec98332a4bbbf34b6fa2e27c28cdf10cf` | `cf1fc2be15223012f65b71071d57253f6bb5197b2e54633aa7c2c353ac52d7a0` | `e303c5421c1b9c1d5e62b3ca49ea9dac4bb857758db87011415d46adc89c4fae` / `a61531792f44ad1965de5e20cff2243c1260e319c3d280af919860a49a781bc4` | `6caf42bd67e19f2580151bf584738d8edbd33d9f998f1db1343c9d5547901e44` / `1eb331be18323a0f68787b1e0723462738e5392b10f506c982ce6f2a9f01cc3a` |
| independent-C / `sm_independent_encdec_c2w14_c64_210k_seed17_4090g1_20260811` | 210K | `979681044340fd41ee4c6edd063ee8d4d6e102188cd52fbc6112c6219b8715e8` / `f1f22bef06056815f2026b6d4d08c21dee8a9ea917340651ee08d230951e1abd` | `30a9c0206c91787b662951bfd34bde88a4369bbe8c0f9e45a83ebf79660b42b0` | `10a2556e9af940af7514c961dea6745309dd437ddb1b1bcc96dcf2dd0c0d4874` | `f95c46a301654d9b65a74b480dee0090da47c4c724b0e6caa58ca3a84bcc1147` / `1e5f82452b5c2e432d5d17bfcb4727e0e518c8c98690d19c67116c98e6f800ac` | `b8e9600662fc443f36c016a1ef0a9bffc5373795180fb9f25da2617712dbdb76` / `53a79262e0130078781afd83810e1158e6d7f062edd291c13c37f59a2421644e` |

Human training contract／manifest／log／endpoint summary SHA-256为
`ea085bf62e5bf31178aff9379e667a6d9604010e917a8a70b8c5446447e76fcc`／
`a52f9624640c5d4759ab1b1581dcecc13871386cbb92908d8abdabc9be018ffc`／
`ce12bf0ec9b36897189a0700c53ea78edfcdf3d7efb043effd2a142012ed37e7`／
`be0ca643fe8fbbf909749b09b529a15b9f2149c3c70958e98381b15ea7660c1d`；Camera对应为
`9510fe1a9d1a495c0c87a61e33026ab2a840e9db8d3e3477be941e8779fb5df8`／
`b4b1b882c7e49c327e0886294fc7406fd085b055619aca10fc16262d57bc25c5`／
`c7c153f93cf9d53cece7afc80452e26558a2f51a043206c733ef966c2d5a4a6a`／
`084960716e2ec01e23152b2c200c010bda6e6a5934ba791dced6e365c1f65c6f`。

#### Human and Camera reconstruction

| version / run | endpoint | global / root-aligned MPJPE ↓ m | root ADE / FDE ↓ m | wrapped yaw mean / final ↓ deg | velocity / acceleration / jerk error ↓ m | latent active channels / effective rank |
| --- | ---: | --- | --- | --- | --- | --- |
| independent-H / `sm_independent_encdec_h199_h128_210k_seed17_4090g1_20260811` | 105K | `0.622276 / 0.192610` | `0.529873 / 1.060024` | `72.463502 / 89.867299` | `0.044848 / 0.033377 / 0.051026` | `128/128 / 42.929` |
| independent-H / `sm_independent_encdec_h199_h128_210k_seed17_4090g1_20260811` | 210K | `0.167870 / 0.057315` | `0.145091 / 0.345824` | `16.059308 / 28.526968` | `0.017880 / 0.019987 / 0.032172` | `128/128 / 43.114` |

| version / run | endpoint | Camera ADE / FDE ↓ m | rotation ↓ deg | FOV-H / FOV-W ↓ deg | velocity / acceleration / jerk error ↓ m | projective UV / center / scale / Out ↓ | latent active channels / effective rank |
| --- | ---: | --- | ---: | --- | --- | --- | --- |
| independent-C / `sm_independent_encdec_c2w14_c64_210k_seed17_4090g1_20260811` | 105K | `0.021462 / 0.106367` | `0.311567` | `0.061200 / 0.101091` | `0.015458 / 0.023026 / 0.038907` | `0.036435 / 0.024218 / 0.006623 / 0.008246` | `64/64 / 15.426` |
| independent-C / `sm_independent_encdec_c2w14_c64_210k_seed17_4090g1_20260811` | 210K | `0.017597 / 0.084248` | `0.261007` | `0.054026 / 0.083821` | `0.012773 / 0.019168 / 0.032525` | `0.029197 / 0.020189 / 0.005448 / 0.006644` | `64/64 / 14.431` |

Human `210K−105K`的十项误差95% CI全部低于零；代表性差值为global MPJPE
`-0.454406 [-0.480980, -0.429073]`、root-aligned MPJPE
`-0.135295 [-0.137954, -0.132586]`、root ADE
`-0.384781 [-0.410850, -0.358752]`、root FDE
`-0.714200 [-0.763931, -0.664825]`、wrapped-yaw mean
`-56.404195 [-57.368950, -55.408399]`。Camera `210K−105K`的十三项error CI同样全部低于零；
代表性差值为ADE `-0.003864 [-0.004091, -0.003646]`、FDE
`-0.022119 [-0.023566, -0.020738]`、rotation
`-0.050560 [-0.053767, -0.047486]`、projective UV
`-0.007238 [-0.010473, -0.004463]`。均使用4,053个matched IDs、10,000次bootstrap。

Human 210K decoded physical mean／median／P90为：bone CV
`0.024896/0.018748/0.049165`、joint speed `0.035763/0.022525/0.079537`、
acceleration `0.027898/0.017351/0.061306`、jerk `0.042581/0.026549/0.091710`、
root speed `0.030591/0.017947/0.069521`、contact heuristic
`0.494966/0.436508/0.992331`、skate `0.038348/0.023838/0.079905`。这些是未校准的
physical diagnostics，不提供单调优越性结论。

#### Native-system boundary

210K明确优于各自105K，且所有latent channel active、无collapse；但它不替代StoryMotion v9 owner。
independent-H 210K仍弱于v9 joint owner的Human aggregate（global/root-aligned MPJPE=
`0.120708/0.042136`，root ADE/FDE=`0.100757/0.248722`，wrapped-yaw mean=`10.434°`）。
independent-C相对v9 joint/GT-H owner在ADE、rotation与projective部分字段更低，但FDE更高；且它使用
world-C2W14→C64的不同representation、decoder、normalization、参数量与interface，不能写成单变量优势。

cross audit artifact为
`sm_independent_dual_encdec_105k_210k_pure4053_audit_20260811/sealed_audit.json`，SHA-256=
`9acc6b0f95610d60f77fd16fe678902093aa26bd1e6fb0097d30804ff5f1c020`；audit script SHA-256=
`9a4d2aa13d549dc2b2684d51383a1b707fe9bef2bd5cfb0e4f01ca3dc0373760`；exact helper bytes只读保存在
该audit root的`audit_code/`。implementation／evaluator
revisions为`88c6a17f25e789af0716c07336bc3b512f505bc5`／
`9ef42f84897c36773a018bd369eb8aeb4ce74919`，evaluator SHA-256=
`e865f1e1f3568e0a5e6ad09e6cbc9d9fd93456efc74670c9558961ac082060f2`。
本证据分类固定为secondary native-system Stage1 comparison；`stage2_authorized=false`，不自动授权
独立双Stage2 cascade，也不进入protected-asymmetry核心消融。


## 4C. Special full-cohort diagnostic detail

The original §3.12 framing-control run is retained as a special diagnostic, not a current endpoint or ranking row. It preserves its full-cohort target, fixed-cohort swap diagnostics, fields, hashes and explicit non-promotion boundary.

### Audited diagnostic — original §3.12 v11 explicit framing-control `30K` pure4,053 formal

| display ID | canonical sm_ run alias | setting | goal |
| --- | --- | --- | --- |
| C0-LAT-reference | `v11_c0_lat_fixedh_35to105k_seed17_5090g2_r2_20260730` | operational mainline context; not the CF-4 training parent | same-protocol system-quality reference |
| C0-GEO-CF4-parent | `v11_c0_geo_fixedh_35to105k_seed17_5090g3_r2_20260730` | frozen-Camera parent for the CF-4 adapter | exact parent and absent-control boundary |
| CF4-screen2K | `v11_f_cf4_framing_screen2k_seed17_4090g1_20260731` | zero-init CF-4 framing adapter, N64 screen | small-cohort adherence screen |
| CF4-30K | `v11_f_cf4_framing_long30k_seed17_4090g0_20260731` | zero-init CF-4 framing adapter trained for `30K`; target and swap diagnostics | formal full-cohort framing-control diagnostic; no promotion |

每一行是一个 distinct run boundary；`CF4-screen2K` 只属于 N64 screen，`CF4-30K` 才有 formal `N=4,053` rows。

本节只比较 exact C0-GEO parent 与其 frozen-Camera 上的 zero-init CF-4 framing
adapter。两行使用相同 pure-test `N=4,053` ordered IDs、official inputs、Euler50、
seed17、eval batch `32`、noise schedule、non-causal Stage1／decoder／stats 与
Human owner；唯一变化是 framing adapter。Direct-H exact 继承 parent，未重复生成；
`joint_parallel=false`。N64 screen 的 batch `8` 不用于 formal 数值。

| display ID / canonical run alias | role | N / identity | formal modes | claim boundary |
| --- | --- | --- | --- | --- |
| v11 / `v11_c0_lat_fixedh_35to105k_seed17_5090g2_r2_20260730` | C0-LAT operational mainline reference | 4,053 / `a0d7627e…6b93` | Direct-C；sequential H→C | 不是CF-4训练parent；只补同协议system-quality上下文 |
| v11 / `v11_c0_geo_fixedh_35to105k_seed17_5090g3_r2_20260730` | exact C0-GEO CF-4 parent；audited alternate | 4,053 / `a0d7627e…6b93` | Direct-C；sequential H→C | 无 explicit numeric framing condition |
| v11 framing-30K / `v11_f_cf4_framing_long30k_seed17_4090g0_20260731` | explicit-control diagnostic | 4,053 / `a0d7627e…6b93` | target Direct-C；target sequential H→C；swapped Direct-C diagnostic | swap 不以原 GT 计算官方语义指标；不得晋升 |

#### Formal system quality

| display ID / canonical run alias | mode | N | FDCLaTr ↓ | CLaTr ↑ | coverage ↑ | caption F1 ↑ | Cam ADE / FDE ↓ m | rotation ↓ deg | r-FPD ↓ / Out ↓ |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| v11 / `v11_c0_lat_fixedh_35to105k_seed17_5090g2_r2_20260730` | Direct-C mainline reference | 4,053 | 21.171 | 56.933 | 0.8303 | 0.7372 | 1.4125 / 1.4985 | 29.922 | 0.8465 / 0.1052 |
| v11 / `v11_c0_geo_fixedh_35to105k_seed17_5090g3_r2_20260730` | Direct-C parent | 4,053 | 20.540 | 57.574 | 0.8236 | 0.7442 | 1.3860 / 1.4711 | 29.800 | 0.8514 / 0.1017 |
| v11 framing-30K / `v11_f_cf4_framing_long30k_seed17_4090g0_20260731` | Direct-C target | 4,053 | 36.615 | 52.910 | 0.7693 | 0.6781 | 1.4318 / 1.5194 | 28.939 | 1.6116 / 0.1575 |
| v11 / `v11_c0_lat_fixedh_35to105k_seed17_5090g2_r2_20260730` | sequential H→C mainline reference | 4,053 | 28.754 | 55.579 | 0.7735 | 0.6935 | 2.9428 / 3.0422 | 71.435 | 0.5082 / 0.0773 |
| v11 / `v11_c0_geo_fixedh_35to105k_seed17_5090g3_r2_20260730` | sequential H→C parent | 4,053 | 29.505 | 56.103 | 0.7626 | 0.7007 | 2.9368 / 3.0395 | 71.507 | 0.5098 / 0.0768 |
| v11 framing-30K / `v11_f_cf4_framing_long30k_seed17_4090g0_20260731` | sequential H→C target | 4,053 | 42.732 | 51.487 | 0.6992 | 0.6424 | 2.8785 / 2.9857 | 68.084 | 1.1446 / 0.1313 |
| v11 framing-30K / `v11_f_cf4_framing_long30k_seed17_4090g0_20260731` | Direct-C swapped diagnostic | 4,053 | — | — | — | — | 1.6752 / 1.7503 | 32.631 | — |

#### Explicit-control adherence

下表的字段是 decoded true-length sequence-mean framing4 MAE。N64 只用于同机制
endpoint screen；N4,053 才是完整 cohort。swapped rows 是控制响应诊断，不是对原 GT
的语义质量排名。

| display ID / canonical run alias | evidence role | N | screen-x ↓ | screen-y ↓ | log-scale ↓ | out-of-frame ↓ |
| --- | --- | ---: | ---: | ---: | ---: | ---: |
| v11 / `v11_c0_lat_fixedh_35to105k_seed17_5090g2_r2_20260730` | C0-LAT未进入冻结的GEO-parent CF-4 adherence合同 | — | — | — | — | — |
| v11 / `v11_c0_geo_fixedh_35to105k_seed17_5090g3_r2_20260730` | parent → own target | 64 | 0.2630 | 0.3548 | 0.1092 | 0.0631 |
| v11 framing-screen2K / `v11_f_cf4_framing_screen2k_seed17_4090g1_20260731` | 2K target condition | 64 | 0.1854 | 0.2492 | 0.0780 | 0.0490 |
| v11 framing-30K / `v11_f_cf4_framing_long30k_seed17_4090g0_20260731` | 30K target condition | 64 | 0.2021 | 0.2354 | 0.0769 | 0.0505 |
| v11 / `v11_c0_geo_fixedh_35to105k_seed17_5090g3_r2_20260730` | parent → swapped target | 64 | 0.4612 | 1.2159 | 0.4355 | 0.2785 |
| v11 framing-screen2K / `v11_f_cf4_framing_screen2k_seed17_4090g1_20260731` | 2K swapped condition | 64 | 0.2110 | 0.5168 | 0.2140 | 0.1385 |
| v11 framing-30K / `v11_f_cf4_framing_long30k_seed17_4090g0_20260731` | 30K swapped condition | 64 | 0.2224 | 0.3914 | 0.1860 | 0.1177 |
| v11 framing-30K / `v11_f_cf4_framing_long30k_seed17_4090g0_20260731` | formal target Direct-C | 4,053 | 0.2149 | 0.2723 | 0.0867 | 0.0595 |
| v11 framing-30K / `v11_f_cf4_framing_long30k_seed17_4090g0_20260731` | formal target sequential H→C | 4,053 | 0.2142 | 0.3466 | 0.1280 | 0.0877 |
| v11 framing-30K / `v11_f_cf4_framing_long30k_seed17_4090g0_20260731` | formal swapped Direct-C diagnostic | 4,053 | 0.2315 | 0.4634 | 0.1794 | 0.1113 |

C0-LAT的standard pure4,053 system-quality已在上一表补齐；但CF-4的N64 target／swap只为exact
C0-GEO parent预注册并生成，故本表的`—`表示**未评测**，不是零误差。若需要数值LAT adherence，
必须另建no-training、同64 IDs／noise／decoder的replay合同，不能从`r-FPD/Out`换名补造。

`30K` N64 gate 为 target `4/4`、swap `4/4`、direction `4/4`；absent-control
Euler50 sampler max-abs 为 `0.0`。这证明 adapter 可控且没有破坏 absent path，但不
抵消 formal system quality 的多字段回退。

#### Artifact and visual identity

| version / run | artifact | SHA256 |
| --- | --- | --- |
| v11 framing-30K / `v11_f_cf4_framing_long30k_seed17_4090g0_20260731` | adapter weights | `b403794ed105974e0bb84ea68cf9f1b61790dce80e6afb4acab51d2efc010bbc` |
| v11 framing-30K / `v11_f_cf4_framing_long30k_seed17_4090g0_20260731` | owning decoder | `51233f6a032c779e66b6eed4bb22b7f61c41d9b4a5a0a1ffc7dade7d3d86d4df` |
| v11 framing-30K / `v11_f_cf4_framing_long30k_seed17_4090g0_20260731` | evaluator | `eecb9222b6a46c59d4275cbc87e223bacf780b941a366d90e5572cbb00a2a6eb` |
| v11 framing-30K / `v11_f_cf4_framing_long30k_seed17_4090g0_20260731` | formal results / records / fixed8 source | `46972fc3eabe870afb20035c61bad2c2c0380c9e6d32fd7ff9ebe05e2c7ca60d` / `cd22cf47a70281e97130246f8f83238808f2e38f35b7c20106134c12c3242e5b` / `c1ca00bfc43afdc493e2b794b559e715e124762403beaacce8f8c60344f78ab7` |
| v11 framing-30K / `v11_f_cf4_framing_long30k_seed17_4090g0_20260731` | visual manifest / renderer / base renderer / contact sheet | `f4659c6c64247c49a6e535158b249f392a276cb287b0745c75a246dc3bea76ef` / `7359708f940fbfb725e7f9dbef9230ea8ac3845bb0503ec70792b2b30e337441` / `b1dd9cc3c20fbe281e1b293bce529875a92c6b04e24b19c5b66ee5c0a8ab5635` / `01dbf4914585af263e83039da42d1d956a45c4a446db69378cab50179933ea99` |

formal official-input SHA256 为
`6d75cbf5d22b4a9f0a39d79fa8cfb900708a4095725b7ff62e7bf11ca4d2b80f`；
ordered-ID SHA256 为
`a0d7627ee827e36a229d33f9975f8417ae78b504cd5a6db1edf62cb1a9266b93`。
fixed8 与 parent 的 8 个 sample IDs 完全一致；8 个展示视频均为 H.264
`1800×736@30fps`，右侧顺序固定为 GT／target Direct-C／swapped Direct-C／target
sequential H→C。

审计裁决：显式 condition adherence 成立，且 Direct-C rotation、sequential
ADE／FDE／rotation 的 raw mean 局部改善；但 Direct-C 与 sequential 的
FDCLaTr、CLaTr、coverage、caption F1、r-FPD 与 Out 均回退。该多字段系统质量
退化触发 endpoint rejection；不晋升、不追加 seed。该结论不改变C0-LAT operational
mainline；C0-GEO继续只作为本轴exact parent与audited alternate。


## 5. Optional Human-text injection controls

HT-FILM, HT-HX and HT-DR are completed pure4053, 105K optional adapters over frozen C0-GEO. They are retained as mechanism controls, not as C0-LAT mainline evidence. The complete exact tables and hashes are on this page in [[StoryMotion-valid-metric-ledger#Audited detail — original §3.13 v11 Human-text Camera fresh `105K` pure4,053 formal audit|§4A / original §3.13]]. No control is a global winner: HT-HX/HT-FILM improve selected geometry/framing fields, while HT-DR has stronger semantic fields.

## 6. Special diagnostics retained outside ranking

| diagnostic | allowed cohort | status | interpretation |
| --- | --- | --- | --- |
| Human/Camera swap or intervention | fixed small cohort | special diagnostic | mechanism attribution only; no population ranking |
| temporal locality / endpoint oracle | N64/N8 | special diagnostic | decoder/editability boundary; no free-edit claim |
| caption recaption QC | first20K / matched5324 | special diagnostic | data quality, not generation metric |
| calibrated/paired bootstrap | full4053 or declared fixed cohort | special diagnostic | uncertainty or mechanism audit; report its unit and cohort |

All ordinary non-pure4053 generation rows, including first-512, N512, N64 and intermediate 30K snapshots, are excluded from active evidence and indexed in [[archived/metrics/2026-08-10_StoryMotion-valid-metric-ledger_pre-v9-and-nonfull]].

### 5.6 v9／v10 Human teacher owner非等价审计

| display ID | canonical sm_ run alias | setting | goal |
| --- | --- | --- | --- |
| v9-PhaseC636K ↔ v10-PhaseA210K | `phase_a210k_vs_phase_c636k_human` | paired owner-identity audit of the Phase-C `636K` and Phase-A `210K` Human-teacher endpoints | establish whether same-shaped Human latents are interchangeable |

每一行是一个 teacher-owner boundary；comparison artifact 只出现一次，本表审计 latent identity，不提供 generation-performance ranking。

这是明确的fixed-cohort owner-identity special diagnostic，不是generation ranking。两条teacher的
`ViMoGenLightFlow`拓扑、71,870,080参数规模、shifted-flow objective、batch128、AdamW、LR
schedule、EMA与`105K`预算相同；本表只审计它们是否拥有同一个Human latent坐标系。cohort为相同
ordered pure-test first128，比较raw Human128有效元素。

| display ID / canonical run alias | N | Human state changed tensors | fixed latent exact | nonzero / valid elements | mean abs | max abs | decision |
| --- | ---: | ---: | --- | ---: | ---: | ---: | --- |
| v9 Phase-C636K ↔ v10 Phase-A210K / `phase_a210k_vs_phase_c636k_human` | 128 | 10 / 10 | false | 371,712 / 371,712 | 0.216329 | 2.286326 | raw cache与train-only statistics不等价；v10 teacher必须fresh训练 |

这证明“同为Human128”只代表shape相同。v9 teacher属于Phase-C `636K` owner；v10属于exact
Phase-A `210K` owner。flow权重在各自whitened坐标中训练，禁止跨owner复用；checkpoint、cache与
statistics身份见 [[Storymotion-exp-sha]]。

## 6A. Pulp Camera recaption first-20K quality audit

| display ID | canonical sm_ run alias | setting | goal |
| --- | --- | --- | --- |
| v1p0-Qwen-raw | `v1p0` | Qwen raw short/long captions on the earliest first20K records | screen geometry/event-marker coverage before any canonical write-back |
| legacy-caption | `legacy` | old short/long captions on the same matched5324 records | matched old/new data-QC comparator |
| v1p0-selected | `v1p0-selected` | fallback-selected short/long captions | verify why selected-text remains blocked |

每一行是一个 caption/data-QC condition；这些 proxy 结果不属于 generation metric 或 Camera text 最终质量 claim。

本节是noncanonical data-QC，不是模型生成指标或Camera text最终质量claim。cohort固定为两个v1p0
run按`created_at`排序的最早20,000条，范围`2026-08-05T02:43:22+0800`至
`2026-08-05T13:23:27+0800`；与旧512／30K／40K exact sample交集为5,324条。新旧文本统一对照
同一rotvec H1 event plan。自动分数只计算count-aware primitive-direction实例与relation marker，
不替代人工对具体event interval、语言自然度和训练可用性的裁决。

### Full first-20K architecture screen

| display ID / canonical run alias | text role | geometry recall ↑ | geometry precision ↑ | geometry pass ↑ | temporal-marker proxy pass ↑ | training-ready proxy ↑ |
| --- | --- | ---: | ---: | ---: | ---: | ---: |
| v1p0 / first20K | Qwen raw short | 0.910140 | 0.994794 | 76.20% | 54.30% | 53.31% |
| v1p0 / first20K | Qwen raw long | 0.758818 | 0.775319 | 43.77% | 95.04% | 42.11% |
| v1p0 / first20K | selected short after fallback | 0.577014 | 1.000000 | 50.84% | 50.84% | 50.84% |
| v1p0 / first20K | selected long after fallback | 0.999944 | 0.986751 | 97.22% | 47.90% | 44.40% |

### Exact 5,324 matched old／new comparison

| display ID / canonical run alias | text role | geometry recall ↑ | geometry precision ↑ | geometry pass ↑ | temporal-marker proxy pass ↑ | training-ready proxy ↑ |
| --- | --- | ---: | ---: | ---: | ---: | ---: |
| v1p0 / matched5324 | Qwen raw short | 0.907289 | 0.993802 | 76.31% | 53.96% | 52.82% |
| legacy / matched5324 | old short | 0.276899 | 0.443889 | 11.04% | 43.26% | 10.99% |
| v1p0 / matched5324 | Qwen raw long | 0.762345 | 0.772331 | 43.82% | 94.83% | 41.90% |
| legacy / matched5324 | old long | 0.652011 | 0.374399 | 10.86% | 45.32% | 10.84% |

| version / run | caption | new-only ready | old-only ready | both ready | neither ready |
| --- | --- | ---: | ---: | ---: | ---: |
| v1p0 raw Qwen vs legacy / matched5324 | short | 2,227 | 0 | 585 | 2,512 |
| v1p0 raw Qwen vs legacy / matched5324 | long | 1,654 | 0 | 577 | 3,093 |

新版raw Qwen相对旧版在同一几何参照上形成明显的mechanical improvement，但这不能挽救当前
`selected_text`合同。20K中11,256条deterministic short存在`rightthen`类粘连，7,698条required
sequence含重复primitive-direction；set-based parser无法表达其multiplicity。最终40,000个
short／long selected captions中20,952个未通过本次count-aware training-ready proxy。

| version / run | all events | required events | relevant relations |
| --- | ---: | ---: | ---: |
| v1p0 / first20K mean | 8.4233 | 6.5104 | 17.5741 |
| v1p0 / first20K median | 6 | 3 | 2 |
| v1p0 / first20K P90 | 21 | 19 | 57 |
| v1p0 / first20K P99 | 42 | 40 | 153 |
| v1p0 / first20K max | 78 | 75 | 329 |

因此停止100K扩写是architecture stop，不是“新版语言不如旧版”的结论。raw Qwen输出逐条保留，
允许修复后离线reparse；现有fallback／selected fields禁止canonical写回。cohort contract SHA256=
`a3a4a78eb53ca0c4d9b367f9b039f09bf70259e6d5c0443d503e302374ea133b`；QC contract／summary／
per-sample SHA256=`03aecfba2aa8a58fb5dfbb3c47861f44fe6985a4a38608e78ab8546b91514f2d`／
`3b325cf10a421b7ac1a159232cccef9cb141585cb7182a09a99c45bcac3b8e03`／
`bbd19ec821c7b0b962f7ce52ba08ed69e48fc9ea9696bff9fa99498a7104ed87`。implementation revision=
`fa6361c1`。

## 7. Uncertainty and claim boundary

- C0-LAT/C0-GEO geometry CIs cross zero; retain both endpoint identities and do not describe LAT as statistically dominant.
- HREL/C1REL/P2 rows have differing representation, initialization or factorization; use field-wise language and state the boundary next to any mixed table.
- Root-aligned MPJPE is not yaw-aligned local-pose error.
- Physical/contact/skate values are heuristics. Calibrated ground penetration/floating and independent Camera velocity/acceleration distributions remain unimplemented.
- Direct-C observed-Human fields are not free-Human generation. Sequential Human fields reuse the Direct-H Human output.
- Auteur, PulpMotion and other external systems require capability/protocol slot descriptions before numeric ranking; task/decoder/cohort mismatch is not an ablation.

## 8. Artifact identity routing

The run contract owns mutable configuration and provenance. The immutable run directory owns checkpoints, logs, manifests, fixed samples, records and raw results. [[Storymotion-exp-sha]] indexes hashes and visual artifacts. This ledger owns only audited numeric rows and their interpretation. Historical pre-v9 and non-full data remain recoverable from the archive note and source snapshot; they are not deleted from provenance.

## 9. Retired anchor index

The following headings are compatibility anchors for older live notes. They intentionally contain no numbers or competing conclusions; each routes to the active section or to the read-only archive.

### 3.10 v11 four-arm 105K first-512 audited confirmation

Retired ordinary first-512 screen. See [[archived/metrics/2026-08-10_StoryMotion-valid-metric-ledger_pre-v9-and-nonfull]].

### 3.11 v11 four-arm `105K` pure4,053 formal audit

Current endpoint summary: [[#Audited detail — original §3.11 v11 four-arm `105K` pure4,053 formal audit]].

### 3.12 v11 explicit framing-control 30K pure4,053 formal

Special diagnostic only: [[#Audited diagnostic — original §3.12 v11 explicit framing-control `30K` pure4,053 formal]].

### 3.13 v11 Human-text Camera fresh 105K pure4,053 formal audit

Optional control summary: [[#Audited detail — original §3.13 v11 Human-text Camera fresh `105K` pure4,053 formal audit]].

### 3.14 v11 C0 seed23 `105K` pure4,053 matched repeat

Repeatability summary: [[#Audited detail — original §3.14 v11 C0 seed23 `105K` pure4,053 matched repeat]].

### 3.15 C1REL／C1REL-noI16 matched Stage2 pure4,053 three-interface formal

Current representation-control summary: [[#Audited detail — original §3.15 C1REL／C1REL-noI16 matched Stage2 pure4,053 three-interface formal]].

### 3.16 HREL matched Stage2 pure4,053 formal

Current representation-control summary: [[#Audited detail — original §3.16 HREL matched Stage2 pure4,053 formal]].

### 3.17 C1REL seed23 raw-T0 Stage2 repeat audit

Repeatability summary: [[#Audited detail — original §3.17 C1REL seed23 raw-T0 Stage2 repeat audit]].

### 3.18 PulpMotion native Stage2 matched available-data cohort

Native boundary summary: [[#Audited detail — original §3.18 PulpMotion native Stage2 matched available-data cohort]].

### 3.19 True-P2 matched symmetric Stage2 pure4,053 formal

Symmetric-control summary: [[#Audited detail — original §3.19 True-P2 matched symmetric Stage2 pure4,053 formal]].

### 3.20 C1REL-noI16 seed23 full-cohort repeat

Repeatability summary: [[#Audited detail — original §3.20 C1REL-noI16 seed23 full-cohort repeat]].

### 3.21 exact-initialization C0-LAT reference and source-row diagnostic

Exact-initialization and source-row boundary: [[#Audited detail — original §3.21 exact-initialization C0-LAT reference and source-row diagnostic]].

### 3.22 observed=true symmetric route controls pure4,053 formal

Route-control closure: [[#Audited detail — original §3.22 observed=true symmetric route controls pure4,053 formal]].

### 3.23 C0-LAT no-source implementation cleanup pure4,053 formal

Source-free implementation closure: [[#Audited detail — original §3.23 C0-LAT no-source implementation cleanup pure4,053 formal]].

### 3.24 fully independent dual-EncDec Stage2 pure4,053 formal

Secondary native-system closure: [[#Audited detail — original §3.24 fully independent dual-EncDec Stage2 pure4,053 formal]].

### 3.25 Human-text Camera condition-attribution pure4,053 diagnostic

Optional mechanism closure: [[#Audited detail — original §3.25 Human-text Camera condition-attribution pure4,053 diagnostic]].

### 5.6 compatibility route — v9／v10 Human teacher owner非等价审计

Canonical fixed-cohort owner-identity diagnostic: [[#5.6 v9／v10 Human teacher owner非等价审计]]. It is not a generation ranking row.

### 6.2 Pulp pure4,053 complete Human reconstruction

Current Stage1 detail: [[#Audited detail — original §6.2 Pulp pure4,053 complete Human reconstruction]].

### 6.4 Pulp pure4,053 complete decoded physical/kinematic summary

Current Stage1 detail: [[#Audited detail — original §6.4 Pulp pure4,053 complete decoded physical/kinematic summary]].

### 6.8 NoInt-HREL／C1REL／C1REL-noI16 matched Stage1 audit

Current Stage1 detail: [[#Audited detail — original §6.8 NoInt-HREL／C1REL／C1REL-noI16 matched Stage1 audit]].

### 6.9 fully independent Human／Camera Stage1 native-system audit

Secondary native-system detail: [[#Audited detail — original §6.9 fully independent Human／Camera Stage1 native-system audit]].

### 6A compatibility route — Pulp Camera recaption first-20K quality audit

Canonical noncanonical data-QC evidence: [[#6A. Pulp Camera recaption first-20K quality audit]]. It is not a generation ranking row.

### C3-25 completion → joint 条件暴露归因（2026-07-21）

Historical mechanism evidence: [[archived/metrics/2026-08-10_StoryMotion-valid-metric-ledger_pre-v9-and-nonfull]].
