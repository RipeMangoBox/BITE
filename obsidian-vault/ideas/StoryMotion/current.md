---
title: "StoryMotion Current"
status: active
hypothesis: |
  corrected v7.14 remains the Stage1 implementation mainline and v7.38 L0
  clean 105K remains the Stage2 formal mainline. The v8 family may replace
  them only after a prospective Stage1 geometry gate and a matched Stage2
  promotion path both close.
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
  - "[[2026-07-17_storymotion-v8-2333-data-curation-plan]]"
  - "[[2026-07-18_storymotion-latent-generatability-stage2-diagnostic-ladder]]"
source_papers:
  - "[[analysis/ECCV_2024/Motion_Mamba_Efficient_and_Long_Sequence_Motion_Generation]]"
  - "[[analysis/NEURIPS_2025/TransPhase_Deep_Compositional_Phase_Diffusion_for_Long_Motion_Sequence_Generation]]"
  - "[[analysis/ICCV_2025/MotionLab_Unified_Human_Motion_Generation_and_Editing_via_the_Motion_Condition_Motion_Paradigm]]"
created: 2026-07-12T14:30:00+08:00
updated: 2026-07-19T18:00:00+08:00
---

# StoryMotion Current

> [!abstract] 当前裁决
> corrected v7.14 camera14 joint AE 仍是 **Stage1 implementation mainline**，v7.38 L0 clean `105K` 仍是唯一 **Stage2 formal mainline**。目前最有希望的 v8 treatment 是 v8.1C C3-25，但它只完成了 Stage1：seed17/seed23 各自 fresh `636K / 81.38M` 和 pure4053 audit；seed17 只剩 Human global slope `26.302 > 20 mm/100f` 未过门，因此没有建 cache、没有 Stage2 `30K`、也没有 `105K`。完成过 Stage2 `30K` 的是父候选 v8.1A；它在 Direct-C 与 joint parallel Camera 上 broad regression 后按预注册停止，没有进入 `105K`。

> [!warning] 最容易混淆的命名
> 仓库中没有独立的 “v8.1D” 或 “v8.1H” 完整版本。`D4/D4.2/D4.3` 是 v8.1A `30K` checkpoint 的 Stage2 只读诊断；`C4-H` 是 v8.1C 内部的 Stage1 Human-horizon short arm。完整命名、dose 和 step 对照只见 [[version_family#v8.1 命名解码与执行状态]]。

精确指标、valid-length bins 与 artifact/checkpoint/record hashes 只见 [[StoryMotion-valid-metric-ledger]]；指标定义与 decoder/evaluator 语义只见 [[StoryMotion-metric-computation-io]]。

## 1. 当前决策板

| family / run | Stage 与预算 | 要回答的问题 | 已验证状态 | 现在允许的行动 |
| --- | --- | --- | --- | --- |
| v7.14 / `joint_ae_official_4090_gpu0_r2` | Stage1 `636K` | corrected local tokenizer 能否作为 implementation baseline | implementation mainline；long Human geometry 仍是已知风险 | 保持为所有 representation control 的基线 |
| v7.38 / `v7_38_l0_clean_lr3em5_105k_purefull_seed17_4090g0_20260715` | Stage2 `105K` | Unified-3 formal reference 是什么 | 唯一 Stage2 formal mainline | 作为 matched `105K` comparator |
| v7.47 / `v7_47_official_ae_unified_matched_seed17_5090g0_20260717` | Stage2 `105K` | official AE system 在同预算 Unified 中表现如何 | audited system control；Direct-H/Direct-C 有 signal，parallel Camera 退化；strict representation isolation 未建立 | 保留为 system evidence，不替换主线 |
| v8.1A / `v8_1a_joint_ae_yaw001_root003_seed17_4090g0_20260717` | Stage1 `636K` | yaw/root geometry supervision 能否修复 Human 长程误差 | Human 显著改善，Camera mild regression；原始 Stage1 gate 未过 | 保留为 v8.1C parent 与 Stage2 generatability control |
| v8.1A / `v8_1a_diag_unified3_30k_seed17_4090g0_20260718` | Stage2 `30K` | v8.1A latent 是否更易生成 | Direct-H 有 signal；Direct-C 与 joint parallel Camera broad regression；正式停止 | 不续 `105K`；只保留已闭合 D4 family 归因 |
| v8.1C C3-25 / `v8_1c_center25pct_full636k_seed17_4090g0_20260719` | Stage1 `636K` | 低 dose Camera-center loss 能否兼顾 Human 与 Camera | 当前最佳 Stage1 candidate；除 global slope 外原始 gate 全过 | 不建 cache；下一训练必须是 fresh、预注册的 multi-horizon short screen |
| v8.1C C3-25 / `v8_1c_center25pct_full636k_seed23_5090g0_20260719` | Stage1 `636K` | C3-25 signal 是否跨 seed | Human 与 Camera translation signal 重现；slope 与 rotation 未全过 | 只作 robustness evidence，不替代 seed17 selected arm |
| v8.1C C3-50 / `v8_1c_center50pct_full636k_seed17_4090g1_exploratory_20260719` | Stage1 `636K` | 更高 center dose 的完整预算代价是什么 | Camera translation 更好，但 Human overall 与 long horizon 全面变差 | dose-response 已关闭；不再增大 center dose |
| v8.1B / `v8_1b_residual_ae_yaw001_root003_seed17_4090g0_20260717` | Stage1 `636K` only | residual AE 是否增加有效容量 | Human 改善，Camera short-bin severe regression；无 Stage2 | 不建 Unified；仅作 architecture control |
| v8.2 / `v8_2_human200_joint_ae_yaw001_root003_seed17_4090g1_20260717` | Stage1 `636K` only | non-integrative human200 是否解决 root/yaw 累积 | Human 改善，Camera center translation 退化；无 Stage2 | 不建 Unified；仅作 representation control |
| v8.2333 / `clean_manifest_ablation` | future data axis | pair-level curation 是否改善 prior | preregistered、not started；所有计数为 `0` | 等 prospective representation promotion 后再开 gate |
| v8.4-A/B | future Stage2 backbone | non-AR backbone 是否改善生成 | not started | 只在 representation promotion 后做 matched backbone axis |

## 2. 不可变边界

- Stage1/Stage2 的 tokenizer 固定为 non-causal；construct、checkpoint/cache load、train 与 eval 均断言 `is_causal=false`。standalone native MotionStreamer 是唯一外置例外，不能进入 StoryMotion cache、Unified 或 promotion gate。
- Human completion 是 `human text → H`；Camera completion 是 `GT/observed H + camera text → C`；active evaluation 固定为 Direct-H、Direct-C 与 joint parallel。Cascade 只作历史或显式 root-cause attribution，不是必报分数或 gate。
- Stage2 必须绑定 exact Stage1 checkpoint、owning decoder、train/eval cache hashes、train-only normalization source、ordered IDs、seed、train/eval batch size、sample count 与 sampler。
- pure4053 已被多轮开发和候选选择使用。它现在是 development evidence；任何最终 promotion 都必须在训练前冻结新的 sealed audit set。
- GT 是 reconstruction/paired-target reference，不是 one-to-many Stage2 generator。PulpMotion 的 released AE 与 official DiT 是 native-system baselines；只有在 Stage、任务、IDs、预算和 evaluator 都写清时才能与 StoryMotion 并列。

## 3. v8 假设与 promotion gate

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

C3-25 seed17 已通过其中所有项，唯一例外是 global slope。后验 amended screen 只能帮助选择 diagnostic，不产生 promotion status。

三个因果轴必须分开：

1. **v8.1 representation/loss**：先修 Stage1 yaw/root、Camera center 和 Human horizon。
2. **v8.2333 data curation**：固定已晋级 representation/backbone，只改变 immutable train manifest；完整 contract 见 [[2026-07-17_storymotion-v8-2333-data-curation-plan]]。
3. **v8.4 Stage2 backbone**：先做 Motion Mamba-style non-AR latent DDPM，再以同 representation/cache 测 TransPhase-style adjacent-phase alignment。它们不能替代 Stage1 gate。

## 4. 当前根因判断

### 4.1 为什么 C3-25 最有希望但还不能进入 Stage2

C3-25 的 25% 表示 **C1 Camera-center weight 的 25%**，不是 25% 数据、训练步数或样本。它等价于 C0 raw-center unit gradient 的约 `1.25%` target dose；C3-50 则约为 `2.5%`。两条 short 都是 fresh `10,176` steps，两条 full 都是 fresh Stage1 `636K`。

低 dose 在 seed17 full 上同时守住或改善 Human、Camera translation 与 rotation；更高 dose 则把 Human long horizon 推坏。这说明可用区间存在，但剩余 blocker 已从 Camera 收窄为 Human global slope。C4-H 的 old last-valid objective 在 matched `10,176`-step short 中 fail；C5-A 只读 audit 显示 four-anchor multi-horizon surrogate 与 formal global/yaw/root-ADE 更对齐，但它没有训练结果，也没有冻结 fresh-init dose。

因此 C3-25 当前状态是 **Stage1 candidate, no cache, no Stage2**。不能把 v8.1A 的 `30K` Stage2 结果继承或改名给 C3-25。

### 4.2 v8.1A Stage2 为什么停在 30K

v8.1A 与 v7.36 做了同 Unified implementation、seed、预算和 sampler 的 G3 `30K` screen。Human 侧出现可重复 signal，但 Direct-C 与 joint parallel Camera 在 semantic/distribution/coverage 上 broad regression。D4/D4.2/D4.3 进一步表明：Camera text 确实被使用；主要问题是 near-manifold 低噪 residual 更集中命中 v8.1A owning decoder 的 Camera 高敏方向，即 Stage1 manifold/decoder 与 Stage2 objective/response 的 cross-stage calibration mismatch。

这个证据不支持“只要多训到 `105K`”“condition 没接上”或“总曝光不足”。`105K` authorization 已明确关闭。

## 5. 下一轮执行顺序

1. 先冻结新的 sealed audit policy、两个 training seeds、matched comparator、同一 short gate，以及 4090/5090/本地三卡分工；当前没有 active GPU experiment。
2. 若要继续 C5，先在 fresh initialization 与 train distribution 上重新校准 multi-horizon dose，再做两 seed、fresh `10,176`-step screen。不得复用 C4-H checkpoint/optimizer/RNG，也不得直接采用 C5-A trained-endpoint weight。
3. 只有 short gate 通过才允许 fresh Stage1 `636K`；只有 full endpoint 再通过原始 gate和 sealed audit，才允许建 exact cache。
4. Stage2 首个新 control 只能是 Direct-C decoder-sensitive objective/calibration 的短阶梯；Direct-C 通过后才处理 joint parallel fusion，inference 最后。
5. v8.2333 curation 与 v8.4 backbone 继续 blocked；不得与 representation repair 混训。

## 6. 文档与证据路由

- 当前主线、active blocker 与允许行动：本页。
- 版本家族、命名、目标、唯一操作、Stage 与已完成 steps：[[version_family]]。
- 已审计数值、fair comparison、valid-length geometry 与 hashes：[[StoryMotion-valid-metric-ledger]]。
- metric/evaluator/decoder 定义：[[StoryMotion-metric-computation-io]]。
- Stage2 screen/continue/stop gate：[[2026-07-18_storymotion-latent-generatability-stage2-diagnostic-ladder]]。
- v8.2333 curation contract 与全部零/非零计数：[[2026-07-17_storymotion-v8-2333-data-curation-plan]]。

run 中的 ETA、有限 step、worker output 和 checkpoint 只进入 `runs/` manifest/log；formal audit 后才更新 ledger、本页和 version family。
