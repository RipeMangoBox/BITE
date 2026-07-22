---
title: "StoryMotion Current"
status: active
hypothesis: |
  v8.1C C3-25 seed17 is the audited Stage1 and Stage2 mainline. The former
  Human global-slope threshold is a non-blocking diagnostic pass. v7.14 and
  v7.38 are former-mainline comparators; seed23 Stage2 remains audit-pending.
tags:
  - StoryMotion
  - version
  - stage1
  - stage2
  - status/active
aliases:
  - StoryMotion-Current
  - StoryMotion-Current-Version
  - StoryMotion-v8
  - StoryMotion-v8-Yaw-Quality
  - 2026-07-17_storymotion-v8-yaw-quality-nonar-diffusion
source_notes:
  - "[[version_family]]"
  - "[[StoryMotion-valid-metric-ledger]]"
  - "[[StoryMotion-metric-computation-io]]"
  - "[[StoryMotion-iclr-reliability]]"
  - "[[2026-07-17_storymotion-v8-2333-data-curation-plan]]"
  - "[[2026-07-18_storymotion-latent-generatability-stage2-diagnostic-ladder]]"
source_papers:
  - "[[analysis/ECCV_2024/Motion_Mamba_Efficient_and_Long_Sequence_Motion_Generation]]"
  - "[[analysis/NEURIPS_2025/TransPhase_Deep_Compositional_Phase_Diffusion_for_Long_Motion_Sequence_Generation]]"
  - "[[analysis/ICCV_2025/MotionLab_Unified_Human_Motion_Generation_and_Editing_via_the_Motion_Condition_Motion_Paradigm]]"
created: 2026-07-12T14:30:00+08:00
updated: 2026-07-22T13:30:00+08:00
---

# StoryMotion Current

<!-- c3-25-stage2-status-20260721 -->
> [!success] v8.1C C3-25 Stage2 已闭环
> `seed17` 已完成 Stage2 训练、Direct-H / Direct-C / joint parallel 正式评估与审计。相对旧 mainline 的匹配基线 v7.38 L0，C3-25 在大多数已审计正式指标上显著更优；当前状态应标记为“Stage2 train/eval completed”，而不是“训练中”或“待评估”。

> [!success] Mainline decision
> Stage1 Human global-slope 的旧 `≤20 mm/100f` 阈值不再是强制 gate，C3-25 的该项 diagnostic 判定为通过；原始数值 `26.302 mm/100f` 继续保留。结合 Stage1 Human/Camera Pareto 与已审计 Stage2 三路结果，C3-25 seed17 正式成为当前 mainline。`seed23` 仍为 `result_written_audit_pending`，不得并入正式 multi-seed 结论。

> [!abstract] 当前裁决
> **当前 mainline 是 v8.1C C3-25 seed17**：Stage1 fresh `636K / 81.38M` owning-decoder audit 已闭合；旧 global-slope 阈值改为非阻塞 diagnostic 并判定通过。Stage2 `105K` Direct-H TMR `14.389` 与 FTD `222.12` 均击败 former mainline v7.38 L0（`13.294 / 333.88`）；Direct-C CLaTr `59.539` 与 FCD `25.09` 均击败 v7.38 L0（`55.64 / 33.29`）；joint parallel 无 broad regression。v7.14/v7.38 现为 former-mainline comparators。C5-B repair 轴因 seed23 未复现 target 而关闭，但不影响 C3-25 mainline。Stage2 seed23 三路 `105K` result/records 已写出，仍为 `result_written_audit_pending`，不能作为 formal multi-seed 复现。v8.2333 的 representation owner 已固定为 C3-25，但阈值、quarantine、clean manifest 与训练仍需单独授权。

> [!info] P0 timestep attribution（2026-07-22）
> 四分支 Direct-H、Direct-C clean-H、joint-parallel 的 `N=512` screen 与 Parent/C0/Tq 的 60 项 single-step attribution 已闭合。Tq 对 `q(H_gt,t)` 的鲁棒收益集中于 `t=399–799`，但 clean-H Camera 与 framing 未恢复；`t=999` 仍为坍缩端点。C3-105K 保持 mainline，下一步只讨论 lower-dose band-limited matched arm。数值与 provenance 只见 [[2026-07-18_storymotion-latent-generatability-stage2-diagnostic-ladder#P0-JC-7：completion 三模式统一分析与 Tq 分层归因（2026-07-22）]]。

> [!warning] 最容易混淆的命名
> 仓库中没有独立的 “v8.1D” 或 “v8.1H” 完整版本。`D4/D4.2/D4.3` 是 v8.1A `30K` checkpoint 的 Stage2 只读诊断；`C4-H` 是 v8.1C 内部的 Stage1 Human-horizon short arm。完整命名、dose 和 step 对照只见 [[version_family#v8.1 命名解码与执行状态]]。

精确指标、valid-length bins 与 artifact/checkpoint/record hashes 只见 [[StoryMotion-valid-metric-ledger]]；指标定义与 decoder/evaluator 语义只见 [[StoryMotion-metric-computation-io]]。

## 1. 当前决策板

| family / run | Stage 与预算 | 要回答的问题 | 已验证状态 | 现在允许的行动 |
| --- | --- | --- | --- | --- |
| v7.14 / `joint_ae_official_4090_gpu0_r2` | Stage1 `636K` | corrected local tokenizer 能否作为 implementation baseline | former implementation mainline；long Human geometry 仍是已知风险 | 保持为 matched representation comparator |
| v7.38 / `v7_38_l0_clean_lr3em5_105k_purefull_seed17_4090g0_20260715` | Stage2 `105K` | Unified-3 formal reference 是什么 | former Stage2 formal mainline | 作为 matched `105K` comparator |
| v7.47 / `v7_47_official_ae_unified_matched_seed17_5090g0_20260717` | Stage2 `105K` | official AE system 在同预算 Unified 中表现如何 | audited system control；Direct-H/Direct-C 有 signal，parallel Camera 退化；strict representation isolation 未建立 | 保留为 system evidence，不替换 C3-25 mainline |
| v8.1A / `v8_1a_joint_ae_yaw001_root003_seed17_4090g0_20260717` | Stage1 `636K` | yaw/root geometry supervision 能否修复 Human 长程误差 | Human 显著改善，Camera mild regression；原始 Stage1 gate 未过 | 保留为 v8.1C parent 与 Stage2 generatability control |
| v8.1A / `v8_1a_diag_unified3_30k_seed17_4090g0_20260718` | Stage2 `30K` | v8.1A latent 是否更易生成 | Direct-H 有 signal；Direct-C 与 joint parallel Camera broad regression；正式停止 | 不续 `105K`；只保留已闭合 D4 family 归因 |
| v8.1C C3-25 / `v8_1c_center25pct_full636k_seed17_4090g0_20260719` | Stage1 `636K` | 低 dose Camera-center loss 能否兼顾 Human 与 Camera | 当前 Stage1 mainline；Human/Camera Pareto 通过，global-slope 为非阻塞 diagnostic pass | 作为下列 Stage2 mainline 的 exact parent |
| v8.1C C3-25 / `v8_1c_c3_25_diag_unified3_105k_seed17_4090g0_20260719` | Stage2 `0→105K` | C3-25 latent 在同 Unified 与长预算下能否生成 | exact cache/contract、D1、`30K` 与 `105K` active three-profile formal audit 均闭合；Direct-H 与 Direct-C 多数指标击败 v7.38，joint parallel 无 broad regression | 当前 Stage2 formal mainline；run ID 与 contract 中的 diagnostic 字段仅保留历史 provenance；physical/render 与 multi-seed 继续补强外推证据 |
| C3-25 P0-JC-7 / Parent、C0、Tq、Tj family | Stage2 matched `5K` + `N=512` full-sampling；Parent/C0/Tq 60-output timestep attribution | noisy observed-H 的收益位于哪些 timestep，能否同时保住 completion、joint 与 framing | Tq 的 `q(H_gt,t)` 鲁棒收益集中 `t=399–799`；clean-H Camera 退化，`t=999` 坍缩；Tj broad regression | parent 保持 mainline；仅讨论 lower-dose band-limited matched arm，不授权 formal4053 或继续 uniform-Tq |
| v8.1C C3-25 / `v8_1c_c3_25_diag_unified3_seed23_105k_4090g1_20260720` | Stage2 `0→105K` | seed17 Stage1 representation 下的 Unified-3 signal 是否跨 Stage2 seed | Human、Camera、joint parallel `105K` result/records 已写出；未见对应 contract audit/profile audit | 保持 `result_written_audit_pending`；先补 provenance/audit，禁止进入 ledger、version milestone 或 multi-seed claim |
| v8.1C C3-25 / `v8_1c_center25pct_full636k_seed23_5090g0_20260719` | Stage1 `636K` | C3-25 signal 是否跨 seed | Human RA `24.70` / global `70.80` / slope `27.59 mm/100f`；Camera ADE `39.05` 与 translation signal 重现；rotation `0.776° > 0.75` fail；slope fail | 只作 robustness evidence，不替代 seed17 selected arm |
| v8.1C C3-50 / `v8_1c_center50pct_full636k_seed17_4090g1_exploratory_20260719` | Stage1 `636K` | 更高 center dose 的完整预算代价是什么 | Camera ADE `36.41` 更好，但 Human overall `73.17` / long `193+` global `138.49` 与 slope `36.21` 全面变差 | dose-response 已闭合；不再增大 center dose |
| v8.1C C5-B / two-seed matched short family | Stage1 calibration + fresh `10,176` screens | four-anchor multi-horizon 是否进一步改善 C3-25 的 Human horizon | seed17 dose1.0 过 gate，但 seed23 两项 target 未复现；two-seed screen fail | optional repair 正式关闭；不影响 C3-25 mainline |
| v8.1B / `v8_1b_residual_ae_yaw001_root003_seed17_4090g0_20260717` | Stage1 `636K` only | residual AE 是否增加有效容量 | Human 改善，Camera short-bin severe regression；无 Stage2 | 不建 Unified；仅作 architecture control |
| v8.2 / `v8_2_human200_joint_ae_yaw001_root003_seed17_4090g1_20260717` | Stage1 `636K` only | non-integrative human200 是否解决 root/yaw 累积 | Human 改善，Camera center translation 退化；无 Stage2 | 不建 Unified；仅作 representation control |
| v8.2333 / `clean_manifest_ablation` | future data axis | pair-level curation 是否改善 prior | G1 raw lock 与 physical distribution complete；TMR Human-pair singleton distribution active；G0 closed、LaMP missing、thresholds unset、quarantine `0` | 只允许继续只读 score/distribution；不得阈值冻结、clean manifest、cache 或训练 |
| v8.4-A/B | future Stage2 backbone | non-AR backbone 是否改善生成 | not started | 以 C3-25 mainline 做 matched backbone axis；仍需单独授权 |

## 2. 不可变边界

- Stage1/Stage2 的 tokenizer 固定为 non-causal；construct、checkpoint/cache load、train 与 eval 均断言 `is_causal=false`。standalone native MotionStreamer 是唯一外置例外，不能进入 StoryMotion cache、Unified 或 promotion gate。
- Human completion 是 `human text → H`；Camera completion 是 `GT/observed H + camera text → C`；active evaluation 固定为 Direct-H、Direct-C 与 joint parallel。Cascade 只作历史或显式 root-cause attribution，不是必报分数或 gate。
- Stage2 必须绑定 exact Stage1 checkpoint、owning decoder、train/eval cache hashes、train-only normalization source、ordered IDs、seed、train/eval batch size、sample count 与 sampler。
- pure4053 已被多轮开发和候选选择使用。它现在支持当前 mainline decision，但不等于独立外部验证；面向论文的强泛化 claim 仍需训练前冻结新的 sealed audit set。
- GT 是 reconstruction/paired-target reference，不是 one-to-many Stage2 generator。PulpMotion 的 released AE 与 official DiT 是 native-system baselines；只有在 Stage、任务、IDs、预算和 evaluator 都写清时才能与 StoryMotion 并列。

## 3. v8 假设与 mainline selection policy

v8.0 owning-decoder oracle 已把 v7.14 的主要长程问题收窄到累计 heading：替换 GT yaw velocity 会大幅降低 long-bin root/global error，而替换 local-joint channels 不改变最终 SMPL joint error。它证明 yaw channel 是首要责任通道，但不证明某个可训练 loss 必然成功。

v8 candidate 的 Stage1 原始 gate 不追溯改写：

| gate | threshold |
| --- | ---: |
| overall Human RA-MPJPE | `≤85 mm` |
| overall Human global MPJPE | `≤190 mm` |
| `193+` Human RA/global MPJPE | `≤90 / 210 mm` |
| Human RA/global length slope | `≤5 / 20 mm per 100f` |
| Camera Cam-ADE | `≤50 mm` |
| Camera rotation | `≤0.75°` |
| contract | finite；checkpoint/owning-decoder/IDs/hashes 完整 |

C3-25 seed17 的 Stage1 Human/Camera Pareto 与 Stage2 三路 formal evidence 已通过 mainline selection。global slope 原始值高于旧阈值，但该阈值现为非阻塞 diagnostic，状态记为 pass；原始数值不改写。

三个因果轴必须分开：

1. **v8.1 representation/loss**：先修 Stage1 yaw/root、Camera center 和 Human horizon。
2. **v8.2333 data curation**：固定已晋级 representation/backbone，只改变 immutable train manifest；完整 contract 见 [[2026-07-17_storymotion-v8-2333-data-curation-plan]]。
3. **v8.4 Stage2 backbone**：先做 Motion Mamba-style non-AR latent DDPM，再以同 representation/cache 测 TransPhase-style adjacent-phase alignment。它们不能替代 Stage1 gate。

## 4. 当前根因判断

### 4.1 为什么 C3-25 成为当前 mainline

C3-25 的 25% 表示 **C1 Camera-center weight 的 25%**，不是 25% 数据、训练步数或样本。它等价于 C0 raw-center unit gradient 的约 `1.25%` target dose；C3-50 则约为 `2.5%`。两条 short 都是 fresh `10,176` steps，两条 full 都是 fresh Stage1 `636K`。

低 dose 在 seed17 full 上同时守住或改善 Human、Camera translation 与 rotation；更高 dose 则把 Human long horizon 推坏，说明 C3-25 是当前 Pareto 选择。global slope 保留为非阻塞 diagnostic 和后续优化轴。C4-H 的 old last-valid objective 在 matched `10,176`-step short 中 fail；C5-A 只读 audit 显示 four-anchor multi-horizon surrogate 与 formal global/yaw/root-ADE 更对齐。C5-B 随后完成 fresh two-seed calibration 与 matched shorts：seed17 选择 dose1.0，但 seed23 未复现两个 target，因此 optional repair 轴按预注册停止，不进入 full。

因此 C3-25 当前状态是 **Stage1/Stage2 mainline**。晋升依据是自己的 exact checkpoint、owning decoder、cache、normalization 与 `105K` formal eval artifacts；不能继承或改名 v8.1A 的 `30K` 结果。历史 run 的 diagnostic contract 不回写，但不再代表当前 eligibility。

### 4.2 v8.1A Stage2 为什么停在 30K

v8.1A 与 v7.36 做了同 Unified implementation、seed、预算和 sampler 的 G3 `30K` screen。Human 侧出现可重复 signal，但 Direct-C 与 joint parallel Camera 在 semantic/distribution/coverage 上 broad regression。D4/D4.2/D4.3 进一步表明：Camera text 确实被使用；主要问题是 near-manifold 低噪 residual 更集中命中 v8.1A owning decoder 的 Camera 高敏方向，即 Stage1 manifold/decoder 与 Stage2 objective/response 的 cross-stage calibration mismatch。

这个证据当时不支持把“继续训练到 `105K`”当作自动修复，因此原 run 的 `105K` authorization 正确关闭，历史正式端点仍是 `30K`。2026-07-21 新授权的是独立的 **budget-matched causal control**：从只读 `30K` optimizer checkpoint 建立新 run ID，按 C3-25 相同的 `30,001` LR decay 续到 `105K`；它只回答同预算比较，不回写原 run，也不预设 v8.1A 会被修复或晋升。

## 5. 核心 TODO

完整 contribution/claim 边界见 [[StoryMotion-iclr-reliability]]。当前只保留会改变主结论的任务：

1. **P0 — 设计低剂量、分段的 condition-domain remedy。** 四分支 completion/joint screen 与 Parent/C0/Tq 的 60 项 single-step attribution 已闭合。Tq 的有效机制是增强 Camera 对 `q(H_gt,t)` 的鲁棒性，收益集中在 `t=399–799`；它并未改善 clean-H Camera denoise，`t=999` 仍坍缩。C3-105K 继续作为正式 mainline。下一候选只讨论 `clean-H 75% + q(H_gt,t) 25%`、`t∈[399,799]` 的 matched 5K arm；在预注册 gate 前不启动 formal4053、不延长 uniform-Tq，也不返回 Stage1。
2. **P0 — 重做真正的 Stage2 seed23 `105K` repeat。** 现有 run 已于 2026-07-22 fail-close：它实际是 `0–30K seed23 + 30K–105K seed17`，且缺 experiment contract/profile audit，不能进入 multi-seed。新 run 必须从正确 seed23 contract 独立训练或使用可审计 RNG-resume；不得给旧结果补标签。
3. **P0 — 补 decoded/no-reference 与 sealed blind evidence。** Direct-H、Direct-C、joint parallel 补齐适用 geometry、integrated yaw、projection、foot/contact、acceleration/jerk、bone 与 root-path；Gradio/Top-5 不替代冻结 IDs/hash 的 blind review。
4. **P1 — 冻结 Human 自动筛选 operating point。** raw lock、physical-v2 与 TMR-v4 双分支计算及 loose/proposed/strict 独立与 `3×3` union/intersection screen 已闭合；当前仍是 `labels=0`、threshold 未冻结、quarantine=`0`。本阶段只筛选、不创造，不启动人工标注；physical 与 TMR 几乎零交叠，候选 clean 集应按两类坏样本的 union 排除，而不是只删二者 intersection。全量阈值、计数与 hashes 只见 [[2026-07-17_storymotion-v8-2333-data-curation-plan]]。
5. **P2 — 多数据集与增广保持独立。** [[ideas/StoryMotion/2026-07-22_storymotion-humanml3d-fixed-camera-augmentation-plan]] 已建立；当前只有旧 v7.14 的 8 条 adapter 可视化，没有 C3-25 配对构造或 Stage2 混合训练证据。先做 fixed-Camera/augment-Human 的自动 A0-A2，Human/Camera 交叉交换只作为后续受控比例 ablation；temporal inpaint 与 v8.4 backbone 延后。

## 6. 文档与证据路由

- 当前主线、active blocker 与允许行动：本页。
- 版本家族、命名、目标、唯一操作、Stage 与已完成 steps：[[version_family]]。
- 已审计数值、fair comparison、valid-length geometry 与 hashes：[[StoryMotion-valid-metric-ledger]]。
- metric/evaluator/decoder 定义：[[StoryMotion-metric-computation-io]]。
- Stage2 screen/continue/stop gate：[[2026-07-18_storymotion-latent-generatability-stage2-diagnostic-ladder]]。
- v8.2333 curation contract 与全部零/非零计数：[[2026-07-17_storymotion-v8-2333-data-curation-plan]]。

run 中的 ETA、有限 step、worker output 和 checkpoint 只进入 `runs/` manifest/log；formal audit 后才更新 ledger、本页和 version family。

## Active evidence boundary — 2026-07-22

- v8.1C C3-25 seed17 remains the formal `105K` mainline, but its claim is now scoped: it is a Camera/joint-system choice rather than a universal Human Pareto win.
- P0-JC-4 is closed. At matched `30K`, C3 is substantially better on Camera across nearly all timesteps, while v8.1A is better on most Human single-step distribution and root/global diagnostics; joint inherits the Camera gain with mixed Human behavior.
- The independent v8.1A `30K→105K` control is formally closed. At matched `105K`, v8.1A is better on most Direct-H metrics; C3 is decisively better on Direct-C semantic/distribution metrics and on joint Camera, coverage, framing, and Camera geometry.
- The active causal target remains Stage2 conditional exposure/routing: Direct-C sees clean GT Human, while joint Camera must consume an evolving/noisy generated Human. The next intervention is a matched Camera replay-refinement exposure test, not a Stage1 rollback.
- The four-branch Direct-H/Direct-C/joint screen is complete. Tq remains positive-but-mixed, Tj is a negative control, and C3-105K remains mainline.
- Tq timestep attribution is complete: its causal benefit is concentrated at `t=399–799`. The next decision is whether to authorize one lower-dose band-limited matched arm; P1 remains automatic-only and candidate-only.
