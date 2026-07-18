---
title: "StoryMotion Latent Generatability and Stage2 Diagnostic Ladder"
status: proposed_non_promotion_diagnostic
hypothesis: |
  Stage1 reconstruction quality is necessary but insufficient for Stage2. Under
  an identical frozen representation, cache contract, Unified implementation,
  compute budget, and conditioning path, a representation whose decoded motion
  is stable under realistic denoiser residuals and whose Stage2 trajectory
  improves against the matched 30K control is more suitable for generation.
tags:
  - StoryMotion
  - stage1
  - stage2
  - representation
  - latent-diffusion
  - diagnostic
  - non-promotion
aliases:
  - StoryMotion-Latent-Generatability-Ladder
source_notes:
  - "[[version]]"
  - "[[history]]"
  - "[[StoryMotion-valid-metric-ledger]]"
  - "[[2026-07-17_storymotion-v8-yaw-quality-nonar-diffusion]]"
  - "[[2026-07-17_storymotion-v8-3-data-curation-plan]]"
source_papers:
  - "[[analysis/arxiv_2026/What_Matters_for_Diffusion_Friendly_Latent_Manifold_Prior_Aligned_Autoencoders_for_Latent_Diffusion]]"
  - "[[analysis/CVPR_2026/MoLingo_Motion_Language_Alignment_for_Text_to_Human_Motion_Generation]]"
  - "[[analysis/ICLR_2026/A_Study_of_Posterior_Stability_in_Time_Series_Latent_Diffusion]]"
created: 2026-07-18T14:44:45+08:00
updated: 2026-07-18T14:44:45+08:00
---

# StoryMotion Latent Generatability and Stage2 Diagnostic Ladder

> [!abstract] 先行裁决
> 不应无条件并行启动 v8.1A、v8.1B、v8.2 三条 `105K` Unified。v8.1A 是唯一可进入受控 Stage2 ladder 的候选：它保留 human199/camera14 与 v7.14 架构，只增加 geometry loss，且仅通过 amended non-promotion screen。v8.1B 和 v8.2 已有 severe Stage1 camera regression，先做短的 representation/camera root-cause diagnostic；它们的 `30K/105K` Unified 目前不会给出干净归因。所有 v8 cache/run 均为 `diagnostic_only`，不得成为 promotion-bearing cache。

## 1. 判断对象与术语边界

对冻结的编码器/解码器 `(E, D)`，需要区分：

- **可重建性**：`D(E(x))` 是否保留姿态、动力学、root/yaw、camera 与物理约束；它给出 Stage1 的上限。
- **可生成性**：在实际文本、任务路由、长度、条件 latent、噪声日程与采样器下，固定预算的 Stage2 是否能学习 `q_E(z | condition)`，并让近似 latent 经 `D` 后保持语义、几何与物理质量。

因此“重建好”是必要条件，不能单独推出“生成容易”。图像领域的 controlled tokenizer study 也观察到，局部连续性、空间结构和全局语义与下游生成比 reconstruction fidelity 更一致；这是一条可迁移的诊断动机，不是 Pulp 上已经成立的结论。[[analysis/arxiv_2026/What_Matters_for_Diffusion_Friendly_Latent_Manifold_Prior_Aligned_Autoencoders_for_Latent_Diffusion]]

若这里的 `NEP` 指 **next-embedding/next-latent prediction**，标准 VAE-LDM 不是严格 NEP：它在整个带噪 latent sequence 上预测 noise、velocity 或 `x0`，而不是按前缀预测下一个 latent。后续文档应使用 `non-AR diffusion`、`masked AR` 或 `next-latent` 的明确名称，不能把三者都写成 NEP。MoLingo 的语义对齐潜在空间是有价值的反例证据，但其生成器是 masked autoregressive rectified flow，不能直接证明 StoryMotion 的 non-AR DDPM 路径。[[analysis/CVPR_2026/MoLingo_Motion_Language_Alignment_for_Text_to_Human_Motion_Generation]]

“语义/细节分层”也不是可单独声称的新颖点。它只有在一个冻结其他变量的 control 中改善可生成性，且不牺牲 camera/root/physical 指标时，才是 StoryMotion 的有效设计选择。

## 2. 对四层框架的批判性收敛

| 层级 | 能回答什么 | 必须修正 | 在本计划中的地位 |
| --- | --- | --- | --- |
| Stage1 reconstruction | `D(E(x))` 的上限和 branch-level 失真 | 不把 reconstruction FID、MPJPE 或 feature loss 当作 Stage2 quality proxy；human/camera 的 root、yaw、velocity、acceleration、contact/skating、频带都要分开 | 必要条件与 root-cause evidence，不是晋级充分条件 |
| latent statistics | cache 是否有 dead channels、尺度失衡、低有效秩或异常 temporal/branch correlation | 协方差谱依赖坐标系；必须同时报告 raw `z` 与 contract 中 exact train-only normalization 后的 `z`，且按 human/camera、length、time-frequency 分开。不能用“更白”替代生成更好 | 低成本风险筛查，不是 hard gate |
| neighbourhood / interpolation / perturbation | decoder 是否在真实 latent 附近稳定；潜在空间是否有明显空洞 | 欧氏邻居必须 match length、task、phase/root 状态和 normalized metric；线性插值离开流形本身不等于失败；随机 IID noise 要以真实 denoiser residual 校准，而非任意 sigma | decoder-sensitivity diagnostic，解释 Stage2 error 被放大的位置 |
| latent cycle | `E(D(z))` 是否把 real、扰动、插值和 generated latent 映回一致区域 | encoder 非双射会产生基线 cycle error；只看相对 real-latent calibration，不能把大 cycle 当作唯一 OOD 判据 | OOD/decoder-consistency auxiliary |
| fixed-budget Stage2 probe | 同一 generator 在不同 frozen representations 上的真实学习难度 | 必须同时匹配参数、token length/维度带来的 compute、条件路径、exposures、sampler 和 cache protocol；单一 seed 的 bootstrap 只量化 sampled outputs，不量化 training-seed variance | 唯一能决定继续到 `105K` 的证据 |

局部噪声与 decoder sensitivity 是本轮最有价值的短测，但应以 diffusion 的实际误差为标尺：从同任务、同 timestep band 的 denoiser `x0` residual 采样扰动，再解码比较，而不是只做 isotropic Gaussian 扫描。近期 time-series latent-diffusion 工作也把 decoder 对 latent 的依赖性视为一项可测风险；其具体后验崩塌机制不应直接外推到 StoryMotion 的非自回归 decoder。[[analysis/ICLR_2026/A_Study_of_Posterior_Stability_in_Time_Series_Latent_Diffusion]]

## 3. 最小诊断集：先定位，再耗费训练预算

| ID | 实验 | 固定项与输出 | 回答的问题 | 不能回答的问题 |
| --- | --- | --- | --- | --- |
| D0 | contract/cache preflight | checkpoint、owning decoder、ordered IDs、train-only z-norm、split、sampler、task routing、cache hash 全部 audit | 比较是否可归因 | 表征或生成质量 |
| D1 | cache geometry audit | raw/normalized per-channel mean/std、dead-channel fraction、effective rank、temporal spectrum、H-C cross-correlation，按 length bin 保存 | 是否存在尺度/容量/分支统计异常 | 异常是否必然造成差生成 |
| D2 | decoder robustness | real `E(x)`、matched neighbour、插值、以及由 denoiser residual 校准的扰动；decode 后测 human/camera geometry、velocity/acceleration/jerk、contact/skating、root/yaw | 哪些 latent 误差会被 decode 放大，是否集中在 camera translation 或长 root/yaw | denoiser 能否学会避免这些误差 |
| D3 | 10K Stage2 trajectory | per-timestep denoising/x0 loss、gradient norm、finite checks、N64 task-applicable screen、decoded residual profile | 训练是否从高噪声端取得全局导航信号，而非只会局部修复 | 30K/105K final quality |
| D4 | cross-stage attribution | `D(E(x))`、`D(\hat z_0)`、Direct-H、Direct-C、parallel、human-first cascade；camera 使用 GT-H 与 generated-H 条件分别记录 | 错误位于 representation、denoiser、human→camera propagation，还是 sampler/decode | 单一因素的训练因果，除非另做 ablation |

所有 D1/D2 的统计只能用训练 split 估计；eval split 只用于冻结后的报告。D2 的 recent-neighbour 检查须提供同任务/同长度的 data baseline，不能凭二维可视化或 unstratified t-SNE 得出结论。

## 4. 候选优先级

| version / run | 进入的阶段 | 理由 | 当前禁止事项 |
| --- | --- | --- | --- |
| v8.1A / `v8_1a_joint_ae_yaw001_root003_seed17_4090g0_20260717` | D0 → D1/D2 → D3 → `30K` → 条件性 `105K` | 同 v7.14 human199/camera14 架构，仅 geometry loss；human 改善且 camera 退化未达 severe 边界 | promotion cache、mainline rename、把单 seed 写为 promotion |
| v8.1B / `v8_1b_residual_ae_yaw001_root003_seed17_4090g0_20260717` | D0 → D1/D2 与 Stage1 camera root-cause | residual/optimization 与 geometry loss纠缠，且 short-bin camera severe regression | `30K/105K` Unified；它只会混合已知 Stage1 camera failure 与 Stage2 效果 |
| v8.2 / `v8_2_human200_joint_ae_yaw001_root003_seed17_4090g1_20260717` | D0 → D1/D2 与 layout/stats/joint-opt root-cause | camera14 不变却出现各 bin center-translation regression，须先拆解 shared trade-off | `30K/105K` Unified；把 human200 改善误称为全系统收益 |
| v7.14 / v7.36 / v7.38 controls | D0–D4 control | v7.36 是 exact 30K parent，v7.38 L0 是 exact 105K mainline | 用 `105K` L0 直接淘汰一个 `30K` candidate |
| v7.47 / `v7_47_official_ae_unified_matched_seed17_5090g0_20260717` | audited representation-isolation control | 四个 pure4053 profile 的 JSON/records、contract 与 eval audit 已闭合；它仍是 frozen official-AE control，不是 corrected v7.14 local-AE 结果 | 把 control 结果重命名为 mainline，或把 single-seed control 当 promotion |

## 5. Stage2 的可中止阶梯

### G0 — Diagnostic-only contract

每一条潜在 representation 在 cache 构建前必须通过 D0。diagnostic-only run 的 `representation` contract 与 cache metadata 都必须写入 `diagnostic_only=true`、`promotion_eligible=false` 和非空 purpose，并锁定 Stage1 checkpoint/owning decoder、train/eval ordered IDs、train-only z-normalization、latent order、non-causal assertion、Unified code revision、seed、batch sizes、sample exposures、sampler 与 four-profile eval protocol。非默认 representation control 还必须使用 contract 允许的 explicit control opt-out，并在所有 metric row 标为 control；它不放松 `is_causal=false`。任何缺项都停在 G0；不得用后写 JSON 补成正式账本。

### G1 — 无训练的 representation/decoder probe

先完成 D1 和 D2，再允许 v8.1A 训练 Stage2。D2 的 primary decoded metrics 是：human root-aligned/global MPJPE、root ADE/FDE、integrated yaw、velocity/acceleration/jerk、contact/skating；camera Cam-ADE/FDE/rotation、camera translation frequency response，以及 joint framing/Out。输出必须保存 perturbation source、noise level、valid mask、length bin、decoder hash 和 `E(D(z))` calibration，而不是只存一张曲线图。

若 v8.1A 在实际 denoiser-residual 量级下已出现显著 camera translation amplification，先修正 root cause，而不是让 `105K` 训练替代诊断。若 v8.1B/v8.2 D2 已复现 Stage1 camera failure，则它们停在这里，除非新的单变量 Stage1 ablation 关闭该问题。

### G2 — 10K structural and trajectory screen

v8.1A 从零训练与 v7.36/L0 相同的 Unified implementation，使用相同 seed、optimizer、task probabilities、batch/exposure accounting、condition paths、noise schedule、sampler 和 eval IDs；不同 representation 所必然不同的 cache/checkpoint/decoder/norm hash 必须显式列为差异。每个 `1K/5K/10K` checkpoint 记录：

- task- and timestep-banded denoising loss、`x0` residual 与 gradient norm；
- human 任务的 TMR coverage，camera 任务的 CLaTr coverage，joint parallel/cascade 的双 coverage 与 Out；不得对不适用任务把缺失 Out 当失败；
- N64 decoded D4 slices，含 GT-H camera completion 与 generated-H cascade；
- audit/finite/identity checks。

G2 是 health gate，不是效果排名。任一 cache/decoder mismatch、NaN、任务适用指标缺失，或 high-noise `x0` 只产生无效 latent 时停止。通过 G2 只授权到 `30K`，不授权到 `105K`。

### G3 — 30K full matched screen

`30K` 的唯一 decision comparator 是 `v7_36_p0a_asym_unified3_joint30k_seed17_4090g0_20260714`：它是 v7.38 L0 的同 checkpoint/optimizer 直接父节点，且已有 human、camera、parallel、human-first cascade 四个完整 profile。`v7.38 L0 105K` 只能作为 trajectory ceiling/reference；把一个 `30K` candidate 直接称为“明显弱于 L0 105K”会混淆表征和训练成熟度。

G3 对 v8.1A 必须在同一 pure4053 ordered IDs 上完成四个 profile，并写出 JSON、records、decoded geometry、四个时长 bin、checkpoint/cache/decoder/evaluator hashes。评测应保留 baseline 的 sampler protocol（DDIM50、CFG1、eta0），除非预注册的 matched protocol 同时改变两边。每个 profile 至少报告：

- human：FDTMR、TMR、HCov，root-aligned/global MPJPE、root ADE/FDE、yaw；
- camera：FDCLaTr、CLaTr、CCov、caption F1，Cam-ADE/FDE/rotation；
- parallel/cascade：上述任务适用项、Out、framing/projection、human→camera propagation；
- no-reference physical：foot contact/skating、acceleration/jerk、bone/root-path distribution，以及固定 blind-render protocol。

为防止“轻微单指标波动”与“广泛退化”混为一谈，G3 预定义 practical screen rule：对同 profile 的 primary semantic/distribution/coverage 集，distance-like metrics 向坏方向变化 `≥10%` 或 coverage/F1 向坏方向变化 `≥5 pp` 视为一项 practical regression；两个及以上 regression 且没有任一同集 practical improvement 即为该 profile 的 broad regression。decoded geometry 仅在它于两个相邻或最长 bins 同向恶化 `≥20%`、且没有对该候选假设相关的 semantic/physical improvement 时，作为 stop 的补充证据；自由生成 paired distance 不是单独 hard gate。

v8.1A 只有在 Direct-H 与 Direct-C 都没有 broad regression，parallel/cascade 没有 audit failure，并至少出现一个与假设一致、可复核的 Stage2 signal 时才继续。sample-paired bootstrap 可以报告方向稳定性，但不能替代第二训练 seed。v8.1B/v8.2 不进入 G3，直到其 Stage1 camera diagnosis 被一个前置、单变量实验关闭。

### G4 — 105K continuation and formal comparison

G3 通过的 v8.1A 必须从同一 `30K` checkpoint 和 optimizer/RNG state 续训至 `105K`，不得重启、换 best checkpoint 或改 cache。然后以完整四 profile 与 v7.38 L0 的 `105K` formal 比较。即使 G4 表现良好，它仍是 non-promotion diagnostic：原始 Stage1 promotion gate 没有被重写，不能据此替换 v7.14/v7.38 或启动 v8.3。

## 6. Stage1 camera 根因：比再训三条 Unified 更优先的短测

| 问题 | 先做的短测 | 预期可区分的假设 | 若仍不确定 |
| --- | --- | --- | --- |
| v8.1B short-bin camera regression | frozen endpoint 的 per-frame/per-bin camera feature、decoded translation/rotation、valid-mask/padding/boundary profile；human/camera/shared-encoder gradient norm 与 cosine | residual decoder boundary artifact、camera loss-scale 竞争、shared-branch gradient conflict | 仅在结论明确后，补一个预注册 factor-complete residual control；不能把 B 的 Stage2 当作该 ablation |
| v8.2 all-bin camera translation regression | 比较 v7.14、v8.1A、v8.2 的 camera branch feature scale、z-norm、latent temporal spectrum、decoder sensitivity 与 shared gradient；保持 camera14 input/output 常量 | human200 layout、train-only stats、joint optimization 三者中的哪一项最可疑 | 缺少的最小 factor 为 `human200 + baseline geometry weights` endpoint；它是 Stage1 设计实验，不是短 10K Stage2 substitute |
| L0 米级 camera generation error | Direct-C 的 GT-H condition、parallel、cascade 逐级 D4 对照；分析 `D(E(x))` 到 `D(\hat z_0)` 的增长 | representation upper bound、camera denoiser、human→camera propagation、sampler/decode 何者主导 | 仅对主导环节改一项，再重跑 matched screen |

不做未经 contract 支持的 latent swap 或“看起来合理”的 decoder 替换：它们会破坏 owning decoder 语义，所得图像/几何不能解释为 representation evidence。

### 6.1 当前 v8.1A execution snapshot

| stage | run / artifact | status | boundary |
| --- | --- | --- | --- |
| D0 cache | `v8_1a_diag_unified3_30k_seed17_4090g0_20260718` | initial cache built on 4090 GPU0; train/val SHA256 were `346d3b2d...c7a2` / `c99a0fa7...ee99` | cache is diagnostic-only and must be rebuilt with its explicit marker before any train checkpoint is accepted |
| D1 preflight | same run | running on 4090 GPU0; computes train-only full-cov z-norm and verifies human-first Unified masks | no Stage2 training starts until the marked cache and contract audit both pass |
| Stage1 camera C1 | `v8_1c_joint_ae_yaw001_root003_cctr004067_screen10k_seed17_4090g1_20260718` | running on 4090 GPU1 after C0 calibrated `camera_center_weight=0.00406677828128799` | C1 outcome can authorize only its own C2 decision; it does not alter v8.1A's Stage2 diagnostic status |
| six-way recon vis | `v8_1_sixway_recon_20260718` | complete; eight ordered IDs rendered as GT/Pulp/v7.14/v8.1A/v8.1B/v8.2 and served by the separate Stage1 Gradio | visual evidence is diagnostic, not a promotion endpoint |

## 7. 执行次序与记录

1. 先恢复 v7.47 raw artifacts 并审计；它是已有 `105K` representation control，成本最低。
2. 对 v8.1A 做 D0–D2；若通过，再做 G2 和 G3。空闲 5090/4090 可用于这条单一因果链，而不是预占三条 `105K`。
3. 并行做 v8.1B/v8.2 的 D1/D2 与 camera root-cause short test；它们不占完整 Unified budget。
4. 仅在 G3 的预注册条件满足后，再让 v8.1A 从相同 state 续训 G4。

新 run 的 mutable state 只写入 remote run contract/log/manifest；G2/G3 的结论更新本页的一行 decision，formal audited metrics 只进入 [[StoryMotion-valid-metric-ledger]]，当前状态只摘要到 [[version]]，最终事件只追加到 [[history]]。该路由由仓库根 `AGENTS.md` 约束。
