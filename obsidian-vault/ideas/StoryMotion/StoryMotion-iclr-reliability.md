---
title: "StoryMotion ICLR Reliability and Contribution Positioning"
hypothesis: |
  StoryMotion 最稳健的 ICLR 定位不是单项 SOTA，而是一个可审计的非因果
  asymmetric Unified-3 system：在一个 checkpoint 内统一 Direct-H、Direct-C
  与 joint parallel，并把 human-camera joint representation 的跨 Stage
  可靠性问题转化为可验证的 geometry、condition 与 provenance gates。
status: in_progress
tags:
  - StoryMotion
  - reliability
  - contribution
  - ICLR
  - status/active
source_notes:
  - "[[current]]"
  - "[[version_family]]"
  - "[[StoryMotion-valid-metric-ledger]]"
  - "[[StoryMotion-metric-computation-io]]"
  - "[[2026-07-18_storymotion-latent-generatability-stage2-diagnostic-ladder]]"
  - "[[2026-07-17_storymotion-v8-2333-data-curation-plan]]"
source_papers:
  - "[[analysis/ICCV_2025/MotionLab_Unified_Human_Motion_Generation_and_Editing_via_the_Motion_Condition_Motion_Paradigm]]"
  - "[[analysis/ECCV_2024/Motion_Mamba_Efficient_and_Long_Sequence_Motion_Generation]]"
  - "[[analysis/NEURIPS_2025/TransPhase_Deep_Compositional_Phase_Diffusion_for_Long_Motion_Sequence_Generation]]"
created: 2026-06-18T00:00:00+08:00
updated: 2026-07-21T15:42:04+08:00
supersedes: "[[2026-06-16_storymotion-v3-formal]]"
---

# StoryMotion ICLR Reliability and Contribution Positioning

<!-- c3-25-reliability-evidence-status-20260721 -->
> [!important] 当前证据状态
> v8.1C C3-25 的 `seed17` 已完成 Stage2 训练和 Direct-H / Direct-C / joint parallel 正式评估审计；相对匹配的旧 mainline v7.38 L0，其大多数正式指标显著改善。这一结果应作为“表征到生成器的可用性已被 Stage2 验证”的正证据，而不是继续表述为待完成实验。
>
> selection policy 已修订：Stage1 global-slope 是非阻塞 diagnostic，C3-25 的该项判定为通过，原始 `26.302 mm/100f` 数值继续保留。C3-25 seed17 现为正式 mainline；这不等于全面 SOTA。`seed23` 结果已写出但审计未闭环，只能作为复现实验进行中。

> [!abstract] 当前定位
> StoryMotion 的论文主线应是 **reliable asymmetric unified human-camera motion generation**，不是“所有指标全面 SOTA”。当前 mainline 证据是：同一个 C3-25 Unified-3 `105K` checkpoint 支持 human text → H、GT/observed H + camera text → C、text → H+C 三个 active profile；Direct-H 与 Direct-C 多数语义/分布指标改善 former mainline v7.38 L0，joint parallel 未出现 broad regression。当前限制是 pure4053 已成为 development set，no-reference physical、blind render、sealed audit 与 seed23 audit 尚未闭合；这些限制约束外推强度，不撤销当前 mainline decision。

精确数值和 hashes 只由 [[StoryMotion-valid-metric-ledger]] 所有；本页只负责贡献定位、claim 边界和核心验证顺序。

## 1. 当前系统与任务合同

### 1.1 表征与生成

```text
Stage1 non-causal joint tokenizer
  normalized human199 -> human latent 128
  official camera14   -> camera latent 64
  concat order        -> human128 + camera64

Stage2 Unified-3 checkpoint
  Direct-H       : human text -> H
  Direct-C       : GT/observed H + camera text -> C
  joint parallel : text -> H + C in one trajectory
```

当前 Stage1/Stage2 mainline 是 v8.1C C3-25 seed17 及其 Unified-3 `105K` endpoint。它使用自己的 exact Stage1 checkpoint、owning decoder、cache 与 train-only full-cov normalization；v7.14/v7.38 是 former-mainline comparators。历史 run contract 中的 `diagnostic_only=true`、`promotion_eligible=false` 只描述执行时授权，不回写，也不代表当前 selection status。

> [!warning] 旧文档中的错误合同
> Human completion 不是 `camera latent + text → H`。active Direct-H 是 **human-text-only**。Camera completion 才消费 complete GT/observed Human latent 与 camera text。Cascade 已退出 active reporting，不得与 joint parallel 并列为必报 gate。

### 1.2 当前 sampler 与证据范围

- active Stage2 formal：pure4053、DDIM `50`、CFG `1`、eta `0`、seed `17`。
- active profiles：Direct-H、Direct-C、joint parallel。
- paired geometry 是 mandatory diagnostic，但 free generation 存在 one-to-many；单一 GT 的 MPJPE/Cam-ADE 不能独立成为生成质量硬门槛。
- Top-5 是明确标注的 best-case paired-geometry slice；必须与随机样本、失败样本和 blind review 分开解释。
- pure4053 已参与多轮开发和 candidate selection；当前 mainline decision 已闭合，但论文级跨分布泛化 claim 仍需要训练前冻结新的 sealed audit set。

## 2. ICLR 贡献定位

### 2.1 Contribution 1：Asymmetric Unified-3

**候选表述**：一个 non-causal、branch-masked continuous latent model，在同一 checkpoint 和同一 human-camera latent basis 中统一 Direct-H、Direct-C 与 joint parallel，同时保持每个 profile 的条件合同可审计。

这个贡献的重点不是“有三个按钮”，而是三种模式共享参数、cache、normalization 与 decoder，同时保留不对称条件语义：

- Direct-H 不读取 camera condition，避免把 paired camera 泄漏为虚假控制能力。
- Direct-C 显式读取 observed Human latent，回答“给定动作如何补相机”。
- joint parallel 同步生成两分支，不依赖 cascade 的二阶段误差传播。
- specialist 只能是同一 branch implementation 的 task-sliced diagnostic，不能用独立专家替 Unified-3 过 gate。

**当前成熟度：较强，但仍需 sealed multi-seed confirmation。** 单 checkpoint 三路 formal 已闭合；C3-25 seed17 的 matched `105K` 显示三路可共同训练而不产生 broad joint regression。最终论文还需要新 sealed set 与 Stage2 seed repeat。

### 2.2 Contribution 2：Representation-to-generation reliability loop

**候选表述**：针对 human-camera joint representation，建立从 Stage1 decoded geometry 到 Stage2 generatability 的闭环诊断，并用低 dose Camera-center supervision 展示“重建更好”与“更可生成”必须同时验证。

可迁移的核心不是 C3-25 这个内部版本号，而是以下 routine：

1. Stage1 用 owning decoder 在 valid-length bins 审计 Human root/yaw/global 与 Camera center/rotation。
2. Stage2 绑定 exact checkpoint、decoder、cache、normalization、IDs 与 sampler。
3. Direct-H、Direct-C 与 joint parallel 分开判断 representation-generatability。
4. 用 low-noise decoder-direction sensitivity 与 condition-reliance probe 区分 condition neglect、objective mismatch 和 decoder amplification。
5. mainline selection 由 audited Stage1 Human/Camera Pareto 与 matched Stage2 active-profile evidence 共同决定；global-slope 是非阻塞 diagnostic。sealed audit 用于补强外推 claim，而不是追溯否定当前 C3-25 selection。

**当前成熟度：mainline selection 已闭合，完整算法 claim 仍需补强。** C3-25 seed17 证明低 dose 区间存在，C3-50 证明更大 dose 会伤害 Human horizon；C5-B seed23 否定了当前 multi-horizon surrogate 的稳定修复。global-slope diagnostic 按修订政策通过，但原始长程误差仍是可报告限制；安全说法是“audited loop selected a better cross-stage Pareto mainline”，不是“所有 representation conflict 均已解决”。

### 2.3 Contribution 3：Auditable evaluation protocol

**候选表述**：一个面向 asymmetric human-camera generation 的 reliability protocol，联合报告 provenance、语义/分布、decoded geometry、projection、physical diagnostics 与 blind visual evidence。

协议必须包含：

- checkpoint、owning decoder、cache、train-only normalization、ordered IDs、seed、batch、sampler 与 code/hash provenance；
- Direct-H、Direct-C、joint parallel 三个 profile，且条件源写清；
- TMR/CLaTr/coverage 与 decoded Human/Camera geometry；
- joint projection/framing、no-reference foot/contact/acceleration/jerk/bone/root-path diagnostics；
- condition shuffle/zero/noise sensitivity；
- random、failure、best-case 三类可视切片与 blind review。

**当前成熟度：协议已成形，证据未全部填满。** 精确 provenance 与 formal semantic/distribution 已较完整；C3-25 Direct-H/Direct-C decoded geometry、no-reference physical、blind review 和 sealed audit 仍是缺口。只有在这些项闭合并对外发布 evaluator/contract 后，才能把它写成独立贡献，而不是内部实验纪律。

## 3. Claim-evidence 矩阵

| candidate claim | 已有证据 | 当前状态 | 论文安全表述 | 下一 gate |
| --- | --- | --- | --- | --- |
| 一个 checkpoint 统一三种 active profile | C3-25 seed17 Direct-H、Direct-C、joint parallel formal artifacts | supported on development set | unified asymmetric generation under one audited checkpoint | sealed set + Stage2 seed repeat |
| C3-25 比 v7.38 更可生成 | matched `105K` Direct-H/Direct-C 改善，joint 无 broad regression | supported mainline evidence | improves matched Direct-H/Direct-C generatability over L0 | decoded geometry + physical + blind render |
| 解决了 Stage1 joint representation conflict | C3-25 成为 mainline；C3-50/C5-B 仍暴露 trade-off | partially supported | selects a low-dose Pareto mainline while retaining long-horizon limitations | prospective slope analysis across seeds |
| 三模式 SOTA | native peers 在部分 TMR/CLaTr/FCD 指标更强 | not supported | competitive/Pareto evidence, not universal SOTA | fair per-task baseline matrix on sealed set |
| joint mode 全面超过 PulpMotion | sampler、AE、budget 与 evaluator boundary 不同，语义指标非全胜 | not supported as controlled ablation | favorable metrics under explicit native-system boundaries | same claim scope or matched system control |
| flexible inpainting/editing | architecture capability 尚无 masked-region formal test | unverified | omit from main contribution | preregistered temporal mask/inbetween protocol |
| 物理+语义数据清洗提升生成 | v8.2333 仍在 score/distribution，未冻结 clean manifest 或训练 | unverified separate axis | future work / ongoing ablation | calibrated thresholds + immutable manifest + SFT |

## 4. 当前数值能支持什么

### 4.1 C3-25 seed17 与 v7.38 L0

以下只列 current decision 所需的 matched `105K` 摘要；完整表与 hashes 见 [[StoryMotion-valid-metric-ledger]]。

| version / run | profile | primary distribution ↓ | primary semantic ↑ | 当前结论 |
| --- | --- | ---: | ---: | --- |
| C3-25 / `v8_1c_c3_25_diag_unified3_105k_seed17_4090g0_20260719` | Direct-H | FDTMR `222.120` | TMR `14.389` | 两项均优于 v7.38 L0 |
| v7.38 L0 / `v7_38_l0_clean_lr3em5_105k_purefull_seed17_4090g0_20260715` | Direct-H | FDTMR `333.880` | TMR `13.294` | matched former-mainline comparator |
| C3-25 / `v8_1c_c3_25_diag_unified3_105k_seed17_4090g0_20260719` | Direct-C | FDCLaTr `25.091` | CLaTr `59.539` | 两项均优于 v7.38 L0 |
| v7.38 L0 / `v7_38_l0_clean_lr3em5_105k_purefull_seed17_4090g0_20260715` | Direct-C | FDCLaTr `33.290` | CLaTr `55.640` | matched former-mainline comparator |

这些结果与 Stage1 Human/Camera Pareto 共同支持 C3-25 mainline selection。Stage1 global slope 原始值仍为 `26.302 mm/100f`，但旧 `20 mm/100f` 阈值已降为非阻塞 diagnostic 并判定通过。run contract 的 non-promotion 字段作为历史 provenance 保留，不代表当前 status。

### 4.2 Native baseline 边界

| baseline | 可回答的问题 | 不能回答的问题 |
| --- | --- | --- |
| v7.38 L0 | 同 Unified implementation、预算与 sampler 下的 matched StoryMotion baseline | 最终跨系统 SOTA |
| v7.47 official-AE Unified | released AE system 在 Unified-3 中的 system control | strict representation-only ablation |
| MoMask-Pulp | native Direct-H system quality | C3 Stage1 或 Unified branch 的单变量收益 |
| Director-C | native Direct-C camera semantic/distribution | owning-decoder Camera geometry，直到 decoded re-eval 完成 |
| CCD-Pulp | v7.14 latent Direct-C system peer | C3 representation 的 matched control |
| PulpMotion official DiT | native joint-generation system comparison | StoryMotion loss/architecture 的单变量归因 |

因此 Gradio 的 completion baseline 固定为 matched v7.38 L0。MoMask、Director-C、CCD-Pulp 和 PulpMotion 在没有同 sample render 与完整 decoded geometry 前只保留 aggregate system rows，不能用占位视频制造“公平可视比较”。

## 5. 核心 TODO 与停止条件

### P0：论文结论前必须完成

1. **审计 seed23 Stage2 `105K` 输出。** 当前 Human/Camera/joint JSON 已写出，但 eval bundle 未见 contract audit 与 profile audit；在 checkpoint/cache/IDs/sampler/records hashes 闭合前只称 `result_written_audit_pending`。
2. **补 C3-25 decoded geometry。** Direct-H 报 RA/global/root ADE/FDE/yaw；Direct-C 报 Cam-ADE/FDE/rotation；joint 报两分支 geometry 与 projection。缺失字段不能解释为 pass。
3. **完成 no-reference physical + blind render。** 固定同 IDs，报告 foot contact/skating、acceleration/jerk、bone consistency、root speed/path，并由不知道版本标签的 reviewer 做 blind preference/failure coding。
4. **冻结新 sealed audit set。** 在训练和 candidate selection 前锁定 IDs/hash；pure4053 只保留 development evidence。
5. **建立 Stage2 multi-seed。** 固定 C3-25 seed17 Stage1 checkpoint/cache，只改变 Unified-3 seed；若 seed23 audit 不满足 exact matched contract，则重做而不是补标签。

### P1：决定最终方法 claim

1. **把 Human global-slope 作为非阻塞优化轴。** 下一项仍应是 prospective、two-seed、单变量 Stage1 intervention；原始数值不改写，结果不作为 C3-25 mainline 的追溯否决。
2. **补 condition reliance。** Direct-C 做 aligned/shuffled/zero/noise Human 与 camera-text probe；Direct-H 验证没有 camera leakage；joint 做 branch intervention。
3. **完成 baseline 矩阵。** 同任务、同 split/IDs、明确 representation/decoder/sampler；不可能匹配的 native baseline 必须标 system comparison。
4. **将 reliability protocol 产品化。** 对外整理 contract schema、evaluator、failure taxonomy 与最小复现实例，否则 Contribution 3 降级为实验设置。

### P2：不阻塞主论文

1. temporal inpaint/inbetweening 只有在 masked-region geometry 与 semantics formal 通过后再写入 contribution。
2. v8.2333 data curation 保持独立因果轴；阈值、quarantine、clean manifest 与 SFT 未闭合前不进入主 claim。
3. v8.4 non-AR backbone 现在可把 C3-25 作为固定 representation owner 做 matched axis；仍需单独授权，且不能用 backbone change 掩盖 long-horizon limitation。

### 停止条件

- sealed set 上任一 active profile broad regress：停止“统一且可靠”的强 claim，回到 profile-specific attribution。
- Stage2 seed repeat 不复现 Direct-H/Direct-C signal：记录跨 seed 泛化限制并重新审议后续 claim，不追溯抹除 seed17 的 audited mainline evidence。
- physical/blind render 与 aggregate semantics 方向冲突：论文以 trade-off 和 failure analysis 为主，不挑选支持性视频覆盖冲突。
- Stage1 slope 跨 seed 仍高于旧阈值：记录为 mainline limitation 与优化优先级，不再触发自动降级。

## 6. Gradio 可视证据合同

当前展示只服务三类问题：

1. Human completion：`GT / C3-25 Direct-H / v7.38 L0 Direct-H`，固定 world-skeleton view。
2. Camera completion：`GT / C3-25 Direct-C / v7.38 L0 Direct-C`，固定同一 GT Human 的 camera projection。
3. Joint Top-5：C3-25 paired Human RA-MPJPE 与 Camera ADE 的 mean-rank 前五；`2×3` 同屏展示 projection 与 world skeleton 的 `GT / C3-25 / L0`。
4. C3-25 single-step：`q(z_gt,t) → one pred_x0`，只作局部 denoising diagnostic。

> [!warning] 可视化不能承担的结论
> Top-5 是 best-case slice，不是总体质量；single-step 不是 full reverse generation；L0 是 matched StoryMotion baseline，不代表 native-system SOTA；任何 qualitative preference 都必须由 random/failure slice 与 blind review 补齐。

## 7. 推荐论文表述

### 安全表述

> We present an asymmetric Unified-3 model that supports human-text generation, human-conditioned camera completion, and parallel human-camera generation within one audited non-causal latent system. A representation-to-generation diagnostic loop identifies a low-dose camera-geometry regime that improves matched Direct-H and Direct-C generatability without broad joint regression, while exposing a remaining long-horizon human-geometry limitation.

### 当前不安全表述

- “StoryMotion achieves SOTA on all three tasks.”
- “C3-25 solves the human-camera representation conflict.”
- “Human completion is camera-conditioned.”
- “Top-5 videos demonstrate general perceptual superiority.”
- “Data cleaning or temporal editing is a validated contribution.”
- “C3-25 在所有指标、所有 seed 与所有外部分布上全面优于旧主线。”

## 8. 当前裁决

StoryMotion 已从“多模式功能集合”推进到“有 matched evidence 的 unified reliability candidate”，但离强会闭环仍差三个硬证据：**sealed multi-seed、decoded/physical completeness、blind qualitative audit**。论文应围绕 Unified-3 + cross-stage reliability loop 展开；SOTA、inpainting 与 data curation 只在各自 gate 真正闭合后再进入贡献列表。
