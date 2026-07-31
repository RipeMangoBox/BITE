---
title: "StoryMotion Latent Generatability and Stage2 Diagnostic Ladder — Closed Through Human-only"
status: archived_closed_through_human_only
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
  - mainline-selection
  - status/archived
source_notes:
  - "[[current]]"
  - "[[version_family]]"
  - "[[StoryMotion-valid-metric-ledger]]"
  - "[[2026-07-17_storymotion-v8-2333-data-curation-plan]]"
source_papers:
  - "[[analysis/SIGGRAPH_ASIA_2023/GeoLatent_A_Geometric_Approach_to_Latent_Space_Design_for_Deformable_Shape_Generators]]"
  - "[[analysis/arxiv_2026/What_Matters_for_Diffusion_Friendly_Latent_Manifold_Prior_Aligned_Autoencoders_for_Latent_Diffusion]]"
  - "[[analysis/CVPR_2026/MoLingo_Motion_Language_Alignment_for_Text_to_Human_Motion_Generation]]"
  - "[[analysis/ICLR_2026/A_Study_of_Posterior_Stability_in_Time_Series_Latent_Diffusion]]"
  - "[[analysis/ICLR_2025/REPA_Representation_Alignment_for_Generation_Training_Diffusion_Transformers_Is_Easier_Than_You_Think]]"
  - "[[analysis/CVPR_2026/SRA_2_Variational_Autoencoder_Self_Representation_Alignment_for_Efficient_Diffusion_Training]]"
  - "[[analysis/ICLR_2026/Unconditional_Human_Motion_and_Shape_Generation_via_Balanced_Score_Based_Diffusion]]"
  - "[[analysis/IEEE_TIP_2024/Multi_Condition_Latent_Diffusion_Network_for_Scene_Aware_Neural_Human_Motion_Prediction]]"
created: 2026-07-18T14:44:45+08:00
updated: 2026-07-24T12:10:00+08:00
archived: 2026-07-24
superseded_by: "[[2026-07-18_storymotion-latent-generatability-stage2-diagnostic-ladder]]"
---

# StoryMotion Latent Generatability and Stage2 Diagnostic Ladder

> [!abstract] 先行裁决
> v8.1A 的 G3 `30K` 已因 Direct-C 与 joint parallel Camera broad regression 停止。C3-25 seed17 则完成 Stage1 `636K` owning-decoder audit 与 exact-cache Stage2 continuous `0→105K`；`30K`、`105K` 的 Direct-H、Direct-C 与 joint parallel formal audit 均闭合。selection policy 已将 Human global-slope 改为非阻塞 diagnostic 并判定通过，因此 C3-25 正式成为当前 Stage1/Stage2 mainline。历史 run/cache 的 `diagnostic_only` 字段与 `diag` ID 保留为不可改写 provenance，不再代表当前 eligibility。pure4053 支持当前 selection，但 sealed set 仍用于论文级外推验证。

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
| D4 | cross-stage attribution | `D(E(x))`、`D(\hat z_0)`、Direct-H、Direct-C、joint parallel；当前 raw-residual arm 固定 Direct-C + GT-H | 错误位于 representation、denoiser、joint condition fusion，还是 sampler/decode | 单一因素的训练因果，除非另做 ablation |
| D5 | human-first condition-source matrix | 同一个 H2C sampler 分别消费 aligned GT、shuffled GT、aligned generated、shuffled generated human latent | cascade failure 是 H2C 本身、human latent quality/domain shift，还是 H2C 未使用/错误使用 human condition | v7.14 与 official-AE representation 的优劣，或任何 promotion 结论 |
| D6 | frozen H2C condition-radius probe | 同一 generated-human `Δz_h`、per-sample/per-channel RMS-matched IID residual、per-channel temporal-spectrum-matched phase-randomized residual | H2C failure 是误差量级本身、temporal support，还是 generated residual 的结构/方向 | Stage2 retraining 是否能修复，或任何 mainline/promotion 结论 |

所有 D1/D2 的统计只能用训练 split 估计；eval split 只用于冻结后的报告。D2 的 recent-neighbour 检查须提供同任务/同长度的 data baseline，不能凭二维可视化或 unstratified t-SNE 得出结论。

## 4. 候选优先级

| version / run | 进入的阶段 | 理由 | 当前禁止事项 |
| --- | --- | --- | --- |
| v8.1A / `v8_1a_joint_ae_yaw001_root003_seed17_4090g0_20260717` → `v8_1a_diag_unified3_30k_seed17_4090g0_20260718` | G3 `30K` 已闭合；不进入 G4 | 同 v7.14 human199/camera14 架构，仅 geometry loss；Direct-H 出现 signal，但 Direct-C 与 parallel/cascade camera 都是 broad regression | `105K` continuation、promotion cache、mainline rename、把单 seed 写为 promotion |
| v8.1C C3-25 / `v8_1c_c3_25_diag_unified3_105k_seed17_4090g0_20260719` | Stage1/Stage2 mainline；continuous `0→105K` completed | global-slope non-blocking diagnostic passed；exact parent/cache 的 `30K`/`105K` 三路 formal audit 闭合 | 用 v8.1A 30K artifact 代替 C3、在 30K 重启、把 cascade 改成 gate |
| v8.1C C5-B / two-seed matched short family | Stage1 short ladder 已闭合；不进入 full | C5-A 支持的 surrogate 在 seed17 有 signal，但 seed23 未通过同一两个 target | full/cache/Stage2、复用 short state、继续扩 dose、把 pure4053 当最终 promotion test |
| v8.1B / `v8_1b_residual_ae_yaw001_root003_seed17_4090g0_20260717` | D0 → D1/D2 与 Stage1 camera root-cause | residual/optimization 与 geometry loss纠缠，且 short-bin camera severe regression | `30K/105K` Unified；它只会混合已知 Stage1 camera failure 与 Stage2 效果 |
| v8.2 / `v8_2_human200_joint_ae_yaw001_root003_seed17_4090g1_20260717` | D0 → D1/D2 与 layout/stats/joint-opt root-cause | camera14 不变却出现各 bin center-translation regression，须先拆解 shared trade-off | `30K/105K` Unified；把 human200 改善误称为全系统收益 |
| v7.14 / v7.36 / v7.38 controls | D0–D4 control | v7.36 是 exact 30K parent，v7.38 L0 是 exact 105K former-mainline comparator | 用 `105K` L0 直接淘汰一个 `30K` candidate |
| v7.47 / `v7_47_official_ae_unified_matched_seed17_5090g0_20260717` | audited official-AE system control | 四个 pure4053 profile 的 JSON/records、contract 与 eval audit 已闭合；但其 Stage2 train-script SHA256 与 L0 不同，尚不是 strict representation-only comparison；它不是 corrected v7.14 local-AE 结果 | 把 control 结果重命名为 mainline、将其写成严格 representation isolation，或把 single-seed control 当 promotion |

## 5. Stage2 的可中止阶梯

### G0 — Diagnostic-only contract

每一条潜在 representation 在 cache 构建前必须通过 D0。diagnostic-only run 的 `representation` contract 与 cache metadata 都必须写入 `diagnostic_only=true`、`promotion_eligible=false` 和非空 purpose，并锁定 Stage1 checkpoint/owning decoder、train/eval ordered IDs、train-only z-normalization、latent order、non-causal assertion、Unified code revision、seed、batch sizes、sample exposures、sampler 与 active three-profile eval protocol（Direct-H、Direct-C、joint parallel）。非默认 representation control 还必须使用 contract 允许的 explicit control opt-out，并在所有 metric row 标为 control；它不放松 `is_causal=false`。任何缺项都停在 G0；不得用后写 JSON 补成正式账本。

### G1 — 无训练的 representation/decoder probe

先完成 D1 和 D2，再允许 v8.1A 训练 Stage2。D2 的 primary decoded metrics 是：human root-aligned/global MPJPE、root ADE/FDE、integrated yaw、velocity/acceleration/jerk、contact/skating；camera Cam-ADE/FDE/rotation、camera translation frequency response，以及 joint framing/Out。输出必须保存 perturbation source、noise level、valid mask、length bin、decoder hash 和 `E(D(z))` calibration，而不是只存一张曲线图。

若 v8.1A 在实际 denoiser-residual 量级下已出现显著 camera translation amplification，先修正 root cause，而不是让 `105K` 训练替代诊断。若 v8.1B/v8.2 D2 已复现 Stage1 camera failure，则它们停在这里，除非新的单变量 Stage1 ablation 关闭该问题。

### G2 — 10K structural and trajectory screen

v8.1A 从零训练与 v7.36/L0 相同的 Unified implementation，使用相同 seed、optimizer、task probabilities、batch/exposure accounting、condition paths、noise schedule、sampler 和 eval IDs；不同 representation 所必然不同的 cache/checkpoint/decoder/norm hash 必须显式列为差异。每个 `1K/5K/10K` checkpoint 记录：

- task- and timestep-banded denoising loss、`x0` residual 与 gradient norm；
- human 任务的 TMR coverage，camera 任务的 CLaTr coverage，joint parallel 的双 coverage 与 Out；不得对不适用任务把缺失 Out 当失败；
- N64 decoded D4 slices，当前固定为 GT-H Direct-C；cascade 不进入 active screen；
- audit/finite/identity checks。

G2 是 health gate，不是效果排名。任一 cache/decoder mismatch、NaN、任务适用指标缺失，或 high-noise `x0` 只产生无效 latent 时停止。通过 G2 只授权到 `30K`，不授权到 `105K`。

### G3 — 30K full matched screen

`30K` 的唯一 decision comparator 是 `v7_36_p0a_asym_unified3_joint30k_seed17_4090g0_20260714`：它是 v7.38 L0 的同 checkpoint/optimizer 直接父节点，且 active Direct-H、Direct-C、joint parallel 三个 profile 完整；历史 cascade 只作归因参考。`v7.38 L0 105K` 只能作为 trajectory ceiling/reference；把一个 `30K` candidate 直接称为“明显弱于 L0 105K”会混淆表征和训练成熟度。

G3 对未来 candidate 必须在同一 pure4053 ordered IDs 上完成 active 三个 profile，并写出 JSON、records、decoded geometry、四个时长 bin、checkpoint/cache/decoder/evaluator hashes。评测应保留 baseline 的 sampler protocol（DDIM50、CFG1、eta0），除非预注册的 matched protocol 同时改变两边。每个 profile 至少报告：

- human：FDTMR、TMR、HCov，root-aligned/global MPJPE、root ADE/FDE、yaw；
- camera：FDCLaTr、CLaTr、CCov、caption F1，Cam-ADE/FDE/rotation；
- joint parallel：上述任务适用项、Out 与 framing/projection；
- no-reference physical：foot contact/skating、acceleration/jerk、bone/root-path distribution，以及固定 blind-render protocol。

为防止“轻微单指标波动”与“广泛退化”混为一谈，G3 预定义 practical screen rule：对同 profile 的 primary semantic/distribution/coverage 集，distance-like metrics 向坏方向变化 `≥10%` 或 coverage/F1 向坏方向变化 `≥5 pp` 视为一项 practical regression；两个及以上 regression 且没有任一同集 practical improvement 即为该 profile 的 broad regression。decoded geometry 仅在它于两个相邻或最长 bins 同向恶化 `≥20%`、且没有对该候选假设相关的 semantic/physical improvement 时，作为 stop 的补充证据；自由生成 paired distance 不是单独 hard gate。

未来 candidate 只有在 Direct-H 与 Direct-C 都没有 broad regression、joint parallel 没有 broad regression 或 audit failure，并至少出现一个与假设一致、可复核的 Stage2 signal 时才继续。sample-paired bootstrap 可以报告方向稳定性，但不能替代第二训练 seed。v8.1B/v8.2 不进入 G3，直到其 Stage1 camera diagnosis 被一个前置、单变量实验关闭。v8.1A 的历史停止结论无需 cascade：Direct-C 与 joint parallel 已分别满足 broad camera regression。

### G3 result — v8.1A

`v8_1a_diag_unified3_30k_seed17_4090g0_20260718` 已以 same-step `v7_36_p0a_asym_unified3_joint30k_seed17_4090g0_20260714` 完成四个 pure4053 profile 的 formal audit。全量 evaluator 字段、decoded geometry、四个时长 bin、JSON/records/checkpoint/cache/decoder/evaluator hashes 的唯一 owner 是 [[StoryMotion-valid-metric-ledger]] §19；此处只保留 gate decision。

| version / run | Direct-H | Direct-C | joint parallel（active） / cascade（historical only） | G3 decision |
| --- | --- | --- | --- | --- |
| v8.1A / `v8_1a_diag_unified3_30k_seed17_4090g0_20260718` | FDTMR、TMR、HCov 与 global/root trajectory 均出现正向 signal | FDCLaTr 恶化，CLaTr、CCov、caption F1 同时下降 | 两种 schedule 都复现 camera semantic/distribution/caption regression，且 Out 上升；几何局部改善不能覆盖该失败 | `stop_30k_broad_camera_regression`；不启动 `105K`，不构建 promotion-bearing cache |

这个停止判断使用 G3 已声明的同预算 practical screen，不把自由生成 paired geometry 当作单独否决项，也不把 Direct-H 的改善外推为三模式生成改善。下一步是 C1 endpoint 与 camera latent/decoder/branch attribution 短测，而不是延长本 checkpoint。

### G3 result — v8.1C C3-25 seed17

`step_30000.pt` 的 pure4053 Direct-H、Direct-C 与 joint parallel contract/identity/non-causal/result audit 全部通过。相对唯一 matched `30K` comparator v7.36 A30：Direct-H 有 practical semantic/coverage signal且几何不退化；Direct-C 的 FDCLaTr 改善并无 broad regression；joint parallel 的 Camera semantic/distribution 与 Out 改善，几何保持同量级。正式数值与 hashes 只见 [[StoryMotion-valid-metric-ledger#4. Stage2 30K matched generatability screen]]。

历史 G3 decision=`pass_30k_active_profiles_continue_105k`；同一进程随后完成 `105K`，三路 formal audit 闭合。当前 selection decision 将该 endpoint 晋升为 mainline。run contract 中的 `diagnostic_only=true`、`promotion_eligible=false` 不回写，仅保留执行 provenance。由于 Direct-C 没有 broad regression，按已冻结的 D4.3 matched-attribution 分支不启动 decoded-Camera/decoder-aware auxiliary short。

### G4 — 105K continuation and formal comparison

本 gate 是条件规则，不是当前队列。若某个未来 candidate 通过 G3，必须从同一 `30K` checkpoint 和 optimizer/RNG state 续训至 `105K`，不得重启、换 best checkpoint 或改 cache，再以完整 active three-profile protocol 与当前 C3-25 mainline 及 former-mainline v7.38 L0 比较。v8.1A 已在 G3 失败并写入 `stop_30k_broad_camera_regression`，因此它没有 G4、不得续训。未来 candidate 只有在 audited Stage1 Pareto、G4 与明确 selection decision 闭合后才能替换 mainline；global-slope 保持非阻塞 diagnostic。

#### C3-25 seed17 连续 `105K` mainline evidence run

`v8_1c_c3_25_diag_unified3_105k_seed17_4090g0_20260719` 是上述默认 G3→G4 quality gate 的显式协议修订，而不是给 v8.1A 续命。预注册问题是：C3-25 的 Stage1 Pareto 改善能否转化为 Stage2 generatability，以及其 `30K→105K` 轨迹是否显示“训练成熟度不足”还是稳定的 Camera/Joint failure。

- exact parent 固定为 C3-25 seed17 fresh `636K` endpoint；不得继承 v8.1A cache、normalization、checkpoint 或结果。
- Unified implementation、human-first routing、seed `17`、batch `512`、task probabilities `1:1:1:0`、full-cov train-only normalization、DDIM50/CFG1/eta0 与 v8.1A matched diagnostic 保持一致。
- 单进程从 step `0` 连续到 `105K`；step `30001` 起 LR 从 `1e-4` 降至 `3e-5`。保存 `1K/5K/10K/30K/105K` immutable checkpoints，不在 `30K` 重启 optimizer。
- `step_30000.pt` 单独计算 SHA256 并以冻结 contract snapshot 做 pure4053 Direct-H、Direct-C、joint parallel full eval；cascade 不运行。主训练同时继续，30K quality 结论不自动杀死 `105K`。
- 唯一自动停止条件是 operational failure、non-finite state、contract/hash/identity/non-causal audit failure。该 run 按执行时 contract 保留 `diagnostic_only=true`、`promotion_eligible=false`；2026-07-21 的审计后 selection decision 独立记录其当前 mainline status。

执行状态：`step_30000.pt` 与三路 formal audit 已闭合，decision 为 `pass_30k_active_profiles_continue_105k`；continuous trainer 未在 `30K` 重启，`105K` endpoint/formal 仍待完成。

#### C3-25 `30K` D4.3 matched attribution

`step_30000.pt` formal eval 开始后，5090 GPU0 只读复用 D4.3 的同一 r3 implementation，将 C3-25 与 v7.36 matched `30K` control 比较。两臂固定 pure4053 前 `64` 个 ordered IDs、Direct-C + observed GT-H、seed `17`、`t=50/500/950`、batch `16`、decode batch `8` 与各自 owning decoder/cache/train-only full-cov stats；C3 checkpoint、cache、stats、decoder 和冻结 contract 从 4090 复制后逐文件验 SHA。跨主机只允许沿用已经在读取 C3 结果前冻结的 RTX 4090 → RTX 5090 replay envelope；该 probe 不训练、不写 cache、不修改主 contract，也不占用 4090 GPU1 的 formal eval。

分支判据预先固定：

1. 若 C3 `30K` Direct-C 没有 broad regression，不启动 decoder-aware loss；若只剩 joint parallel Camera 失败，下一项转为 joint branch/fusion 单变量 screen。
2. 若 Direct-C broad regression，且 C3 相对 v7.36 在 `t=50` 或 `t=500` 的 Camera-center 或 rotation actual-direction median gain `≥1.10×`，同时 C3 actual/random median gain `≥1.20×`，才允许进入同主机、同初始化、同 C3 cache 的 decoded-Camera auxiliary matched short；该 short 仍须另行冻结 dose、预算和 stop gate。
3. 若 Direct-C broad regression 但 D4.3 不支持上述局部方向放大，不启动 decoder-aware loss；优先定位 multi-step rollout 或 camera-text semantic calibration。无论哪个分支，本 probe 都不授权 full、第二条 `105K`、v8.2333、v8.4 或 promotion。

**Decision — closed, no auxiliary short.** C3 相对 v7.36 只有 `t=50` Camera-center 命中局部规则（candidate/baseline=`1.131×`、candidate actual/random=`2.197×`），rotation 与其他 timestep 未命中；同时 C3 `30K` Direct-C formal 没有 broad regression。故按上面的先验分支保留 sensitivity attribution，但不启动 decoder-aware loss，也不把局部 JVP/VJP 结果外推成 full-generation failure。

## 6. Stage1 camera 根因：比再训三条 Unified 更优先的短测

| 问题 | 先做的短测 | 预期可区分的假设 | 若仍不确定 |
| --- | --- | --- | --- |
| v8.1B short-bin camera regression | frozen endpoint 的 per-frame/per-bin camera feature、decoded translation/rotation、valid-mask/padding/boundary profile；human/camera/shared-encoder gradient norm 与 cosine | residual decoder boundary artifact、camera loss-scale 竞争、shared-branch gradient conflict | 仅在结论明确后，补一个预注册 factor-complete residual control；不能把 B 的 Stage2 当作该 ablation |
| v8.2 all-bin camera translation regression | 比较 v7.14、v8.1A、v8.2 的 camera branch feature scale、z-norm、latent temporal spectrum、decoder sensitivity 与 shared gradient；保持 camera14 input/output 常量 | human200 layout、train-only stats、joint optimization 三者中的哪一项最可疑 | 缺少的最小 factor 为 `human200 + baseline geometry weights` endpoint；它是 Stage1 设计实验，不是短 10K Stage2 substitute |
| L0 与 v8.1A 的 camera generation regression | v7.36 A30 与 v8.1A A30 同 pure4053 前 `64` IDs 的 Direct-C teacher-forced `x0` screen，固定 `t=50/500/950`，记录 raw camera-latent residual 与 decoded geometry | candidate latent residual 更大：camera denoiser/cache prior；latent residual相近而 decoded camera更差：camera14 integration/decoder amplification；两者均相近但 formal Direct-C 仍差：多步收敛、task loss/exposure或semantic alignment | N64 只有 finite、identity、checkpoint 与 sampler audit 都通过且签名一致时才决定下一个 matched ablation；否则停止，不启动任何105K |

不做未经 contract 支持的 latent swap 或“看起来合理”的 decoder 替换：它们会破坏 owning decoder 语义，所得图像/几何不能解释为 representation evidence。

这条 D4 是无训练、无 cache 写入的 `diagnostic_only` 配对 screen。每个 arm 使用自己的 source `last.pt`、owning decoder 与 cache，只比较同一 `30K` 预算下的结果；输出须同时保留 evaluator JSON、records、前 `64` ordered-ID hash、source checkpoint SHA256、source cache hashes 与单步 sampler metadata。它不能产生 promotion 结论，也不能代替未来 candidate 的 formal active three-profile eval；v8.1A 已存在的第四条 cascade 只保留为历史 artifact。

**D4 decision — closed.** 初始 decoded screen 与后续只读 raw-residual recorder 都通过了 matched-identity、checkpoint、cache、owning-decoder、non-causal 与 finite audit；完整数值及 artifact hashes 只见 [[StoryMotion-valid-metric-ledger#5.1 D4 residual propagation]]。Direct-C 已给定 GT/observed human latent，因此排除了“只由 generated-human cascade propagation 导致”的解释。raw recorder 的实际签名是 mixed：v8.1A 的 whitened camera residual 仅轻度升高，inverse-whitening 后在特定 camera channel/direction 上放大，低噪 decoded geometry 又进一步恶化；高噪端没有同样的 decoder-amplification signature。故不扩 N256、不恢复 cascade、不开 `105K`，也不能把责任单独归给 Stage1 或 Stage2。

### D4.1 — Stage1→Stage2 camera amplification causal map

这里的“放大”必须拆成两个现象。v8.1A 的 formal Direct-C camera semantic/distribution/coverage 广泛退化，但 paired Cam-ADE 只轻度变差；joint parallel 的 paired camera geometry 甚至改善。因此不能写成“Stage2 把所有 camera geometry 都显著放大”。当前被明显放大的是 **camera semantic/distribution generatability gap**，另有低/中噪声单步 decoded error；二者可能共享原因，但不是同一个指标。

现有结构给出一个明确的 Stage1 风险面：joint AE 的 encoder 读取 concatenated human199+camera14，并通过共享 trunk 同时产生 human128 与 camera64；两个 decoder 才是 branch-specific。v8.1A 新增的 human yaw/root auxiliary 虽不直接训练 camera decoder，梯度仍会改变共享 encoder 和 camera latent 的条件拓扑。Stage2 的 full-cov whitening只在 human/camera branch 内分别校准一、二阶边际统计，不保持 `p(z_c | z_h, text)` 的 cross-branch structure、higher-order topology、decoder Jacobian 或 caption-sensitive directions。

第 19.4 节还给出两个不能合并的 Stage2 故障面：Direct-C 的 candidate camera x0 eval loss 已低于 baseline，但 formal semantic结果更差，说明“平均 whitened MSE 收敛”与“camera 可生成性”失配；joint camera-branch x0 loss 则明显更高，说明 parallel 另有真实的 branch/fusion optimization 缺口。v7.47 的 Direct-C 很强而 joint parallel camera 失败也支持这一拆分：当前 Unified 并非完全不会生成 camera，但 joint fusion 仍不稳；v8.1A 又额外存在 representation-specific Direct-C 问题。

只读 recorder 已命中下表前两种 signature 的组合，而不是第三种：Stage2 在 whitened space 确有轻度、timestep/channel-dependent residual；Stage1 inverse map/decoder 又把其中一部分高敏感方向放大。下一轮不得把两者重新压成“训练没收敛”一个解释。

| matched raw-residual signature | 支持的首要解释 | 下一步；只执行一项最小可归因检查 |
| --- | --- | --- |
| candidate 在 whitened 与 owning-decoder-input camera residual 都更大，decoded error 同向 | denoiser 未正确拟合 candidate camera target；平均日志 loss 掩盖 timestep/channel/direction 差异 | 先做 frozen camera-text shuffle/aligned advantage 与 per-channel/timestep audit；若 text reliance 正常，再做 Direct-C camera-sensitive objective 短 ablation |
| whitened residual相近，但 decoder-input residual或 decoded geometry明显更差 | inverse normalization或 owning decoder 对特定 latent direction更敏感；属于 representation/decoder robustness | 对 D4 residual directions 做 decoder local-sensitivity/Jacobian probe；Stage1 优先保留 C3 低 dose，并禁止用延长 Stage2 代替修复 |
| 两个 latent space与单步 decoded error都相近，但 formal semantic仍差 | 多步 rollout、camera-text semantic alignment或 higher-order latent distribution问题 | 固定 checkpoint 做 camera-text shuffle、逐步 rollout divergence；不先改数据或开 `105K` |
| Direct-C 恢复、joint camera仍差，且 joint camera-branch loss高 | joint element-mean/fusion/condition path 对 camera 不足；这是第二故障面 | 只在 Direct-C 先通过后，比较 joint branch-mean/camera balance或 camera-specific condition injection；保持 Human 不退化 |

对“保持 human 优化同时提高 camera”的 Stage1 顺序也据此冻结：

1. C3 的 `1.25%/2.5%` raw-gradient camera-center dose 都已在 fresh matched screen 中保住 v8.1A Human core并改善 Camera translation；按预注册规则选择较小 `1.25%` dose。seed23 C3-25 full endpoint 证明低 dose signal 能扩展到完整预算；Human global slope `27.594 mm/100f` 作为非阻塞 diagnostic 通过，Camera rotation `0.776°` 保留为 robustness limitation。seed17 endpoint 的完整 Stage1/Stage2 audit 支持当前 mainline selection。
2. “两个 dose 都失败则停止 center-only sweep”的 failure branch未触发，但 seed23 已表明继续只扫 center weight不会直接解决 rotation/global-slope。下一条 Stage1 诊断应先测 human geometry auxiliary、camera base/velocity、camera center 与 camera rotation 在 shared encoder 的 per-layer gradient norm/cosine，再把 decoded Camera rotation 与 Human long-horizon yaw/root 拆成两个单变量 short screens；首轮不得同时修改两项。
3. 只有确认 shared-gradient conflict 后，才在 balanced SE(3) camera auxiliary、shared-trunk gradient projection或更小的 branch-specific encoder改动中选择一个单变量 control。数据样本/manifest 与 inference 不是当前首要嫌疑，因为 v7.14/v8.1A 使用同一 ordered IDs，而单步 GT-H 已复现差异。

对 Stage2 的修改顺序固定为 **Direct-C representation handling → joint parallel fusion → inference**。camera task 曝光不足不是当前首要假设：两条 run 的 camera exposure 都约 `5.12M`，v8.1A Direct-C latent loss还更低；简单增加 steps/task probability可能继续优化错误代理。优先候选是让 objective 对 owning-decoder-sensitive camera directions或 clean camera representation进行校准，并以 frozen text-condition probe确认语义路径；只有 Direct-C 短 gate 通过后，才处理 joint camera branch balance。REPA/SRA2、balanced diffusion与动态多条件融合的本地论文证据只提供机制设计线索，不替代上述 StoryMotion matched artifacts。

### D4.2 — Direct-C camera-text reliance screen

**Decision — closed.** v7.36 与 v8.1A 使用同 N64 IDs、GT-H、noise、`x_t` 和 `t=50/500/950`；唯一 intervention 是把 camera-text embedding 前半按 ordered ID 循环错位，human-text 后半保持 bit-exact。aligned path 对 D4 raw/geometry 的 formal reproduction delta 为 `0`，两边的 checkpoint/cache/decoder/non-causal 与 child-contract audit 都通过；未运行 blank、cascade、N256、训练或 cache write。完整数字和 hashes 只见 [[StoryMotion-valid-metric-ledger#5.2 D4.2 Camera-text reliance]]。

v8.1A 在三个 timestep 上都有正的平均 shuffled-minus-aligned residual advantage，camera-text condition effect 也没有一致弱于 v7.36。因此排除“Stage2 没接上或简单忽略 camera text”作为首要解释。该 N64 one-step probe 不计算 CLaTr，也不证明 semantic mapping 已正确；允许的结论仅是 condition 被使用，但其响应仍可能与 v8 camera manifold 的高增益方向或 reverse-process calibration 失配。后续 Direct-C 单变量实验应测试 decoder-sensitive objective/calibration，而不是先增加 condition injection；joint fusion 仍必须等 Direct-C 通过。

### D4.3 — owning-decoder residual-direction sensitivity

**Pre-registered and authorized, read-only.** 用户已确认按 D4.3 → seed17 Stage1 endpoints → C4-R/C4-H 的顺序执行。D4.3 复用 D4 的 v7.36/v8.1A 两条 frozen `30K` source checkpoint、各自 cache/train-only inverse stats/owning decoder、前 `64` 个 pure4053 ordered IDs、GT-H Direct-C、seed `17` 与 `t=50/500/950`；不训练、不写 cache、不运行 cascade/full reverse，也不修改任何 legacy artifact。新 child run 使用 functional `runs/train|eval|vis/stage2/<run_id>` layout。

对每个 sample/timestep，先在 owning-decoder input space 取实际 Camera residual `prediction-target`，按 valid latent element 归一到 RMS=`1`；再生成一个确定性 Gaussian control，投影到与实际 residual 正交并做同样 RMS 匹配。JVP 在 target/prediction midpoint 测 decoded Camera center ADE/RMS/FDE gain、rotation tangent angular gain 与 rotation-matrix Frobenius gain；VJP 在 prediction 点测 decoded Camera center ADE/FDE 与 rotation geodesic 对 latent 的 gradient RMS、方向导数及其与实际 residual 的 cosine。这里只计算实际 residual 与一个 per-sample isotropic control，不构造 full Jacobian。

首次 v7.36 child `v7_36_d43_decoder_sensitivity_n64_seed17_5090g0_20260719` 在第一个 formal record 写出前被 replay gate 拒绝，未生成 `decoder_sensitivity` artifact：它把跨主机重放误设成近同栈容差。随后先完成只读 v7.36 N64 cross-host replay；checkpoint/cache/owning-decoder/四份实现代码 hash 全部与 4090 parent 相同，唯一执行栈差异是 RTX 4090 `torch 2.3.1+cu121` 对 RTX 5090 `torch 2.8.0+cu128`。三时刻的最大绝对 replay delta 为 latent residual RMS `1.998e-4`、Camera center `3.558e-3 m`、rotation `4.186e-2°`。在查看 v8.1A candidate sensitivity 前，据此冻结 r2 replay envelope 为 `3e-4 / 5e-3 m / 5e-2°`；该 envelope 只判断旧 D4 路径是否在跨栈数值漂移内重现，不参与 candidate/baseline gain 决策。正式 child 改用带 `_r2` 的新 run ID，保留 r1 failure 与 replay artifact，不覆盖任何证据。

r2 v7.36 artifact 完整写出；r2 v8.1A 又在加载阶段、任何 candidate JVP/VJP 前被 stats file hash gate 拒绝。审计定位为 parent contract 保留的 pre-resume serialization SHA256=`605049fa…71feb` 与 step-10K resume 后当前文件 SHA256=`94805397…5adc4` 不同：当前文件在 4090 原目录与 5090 最小搬运包完全同 hash，embedded source-cache SHA256=`3b55223d…bd22`、`created_at=2026-07-18T15:13:06+0800` 及 latent summary 与 D4 raw evidence 一致；文件 mtime `17:02` 紧随 step-10K checkpoint `17:01`，而 trainer 的 full-cov path 会在 resume 时重新 `torch.save` 已加载 stats。缺失的旧 serialization 已无法做 tensor-by-tensor byte audit，因此不修改 parent contract，也不把该项升级为 promotion evidence。r3 child 会把当前实际 file hash、旧 expected hash 与此不确定性同时写入 contract，并强制校验 embedded source-cache hash、D4 summary 与实际 file hash；两边用同一 r3 implementation 重跑后才允许比较。

预注册支持条件不变：在 `t=50` 或 `t=500`，Camera center 或 rotation 的 candidate/baseline actual-direction median gain `≥1.10×`，且 candidate actual/random median gain `≥1.20×`。满足时才允许把“owning-decoder-sensitive direction calibration”作为后续 Direct-C objective 的依据；否则不得从 D4.3 推出 sensitivity-weighted Stage2 loss，应保留 finite-path nonlinearity 或 inverse-normalization 解释。无论结果如何，D4.3 都不是 Stage1/Stage2 单独归因、promotion、full-generation quality 或扩大 N256/105K 的授权。

**Decision — closed, local alignment supported.** r3 两边均完成 N64 JVP/VJP 与 contract/artifact audit。`t=50` 的 actual-direction center gain 为 v7.36 `2.73995`、v8.1A `3.41669`，candidate/baseline=`1.24699×`，candidate actual/random=`2.47033×`；rotation 分别为 `46.6517/52.5040 deg per RMS`，candidate/baseline=`1.12545×`，candidate actual/random=`2.36034×`，两个 objective 都命中预注册条件。`t=500` 与 `t=950` 未出现同样的 candidate/baseline 放大，因而结论是 **低噪、方向选择性的局部 owning-decoder amplification**，不是全 timestep 或全方向敏感。comparison SHA256=`ff0df9c541f351827ae234700b25cf5f9f355ec369b0c9f7c8525de0ab7ef7ae`；完整矩阵、VJP 与 r1/r2 provenance 只见 [[StoryMotion-valid-metric-ledger#5.3 D4.3 owning-decoder direction sensitivity]]。允许后续在 Stage1 gate 之后做 Direct-C decoder-sensitive objective 单变量 control；不授权 N256、cascade、`105K` 或 promotion。

### D5 — v7.47 human-first condition-source screen

这是针对已审计 `v7.47` official-AE system control 的已闭合历史 attribution screen，而不是新的 Stage2 candidate或当前评估标准。它固定同一 `last.pt`、owning official Pulp decoder、val cache、train-only z-normalization、first `64` pure4053 ordered IDs、seed `17`、DDIM `50`、CFG `1`、eta `0`、batch `32`、decode batch `16` 与 `human_text` first-pass task；仅改变 human source：`gt`、`shuffled_gt`、`generated`、`shuffled_generated`。四臂均走同一 human-first H2C evaluator path；`h2c_source=replay` 沿用 formal cascade metadata，但该 CondMDI checkpoint 的 second pass 仍是同一个 diffusion completion，不能误报为额外的 clean/noisy factor。

预注册解释为：aligned GT 明显优于 aligned generated，且 shuffled GT 明显差于 aligned GT，支持 generated-H domain shift 或 H2C 对其误差不稳健；aligned GT 也差则定位为 H2C/task-routing 本身，不能归因给 human generator；shuffled GT 与 aligned GT 接近则说明 H2C 没有有效利用 human condition。只比较四臂间同 ID 的 camera semantic/coverage、human semantic、Out 和 decoded geometry方向；N64 不作正式排名、主线替换或 promotion evidence。原始 JSON、records、diagnostic contract 与 audit 留在 v7.47 run 下；screen 闭合后本页只记录一条 decision。

**D5 screen decision — closed.** 四臂 records 在 amendment audit 下通过：初始 contract 的 ID digest 误把字面 `\\n` 当分隔符，保留原 failed audit 后以 StoryMotion canonical newline-byte digest `dedf57927569e1dcb6ed86ca5336686224b7d20301083b17d79a998ea3963911` 作了只增量的 amendment；没有重跑或改动任何模型 artifact。amendment audit SHA256=`3f4c3cafebee327f098ed350264519c32d31b4006e23f17261c12ea70c5e28e5`。

Human-source quality：

| version / run | n | H FDTMR ↓ | H TMR ↑ | HCov ↑ | H RA-MPJPE / m ↓ | H global MPJPE / m ↓ |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| v7.47 D5 / aligned GT-H | 64 | 303.090 | 16.853 | 100.00% | 0.069 | 0.173 |
| v7.47 D5 / shuffled GT-H | 64 | 481.130 | 0.000 | 93.72% | 0.239 | 0.907 |
| v7.47 D5 / aligned generated-H | 64 | 2053.114 | 1.896 | 1.54% | 0.313 | 1.112 |
| v7.47 D5 / shuffled generated-H | 64 | 1791.797 | 0.000 | 0.00% | 0.288 | 1.011 |

同一 frozen H2C 对 camera 的响应：

| version / run | n | C FDCLaTr ↓ | CLaTr ↑ | CCov ↑ | Caption F1 ↑ | Out ↓ | Cam-ADE / m ↓ | Cam-FDE / m ↓ | rotation / deg ↓ |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| v7.47 D5 / aligned GT-H | 64 | 52.284 | 63.122 | 100.00% | 0.769 | 2.49% | 0.130 | 0.223 | 2.097 |
| v7.47 D5 / shuffled GT-H | 64 | 124.530 | 23.094 | 98.46% | 0.262 | 9.32% | 3.772 | 3.802 | 76.932 |
| v7.47 D5 / aligned generated-H | 64 | 658.183 | 10.637 | 27.95% | 0.052 | 84.58% | 3.012 | 3.730 | 80.863 |
| v7.47 D5 / shuffled generated-H | 64 | 588.288 | 11.859 | 40.38% | 0.195 | 82.65% | 2.912 | 3.241 | 77.180 |

aligned GT-H 的 camera geometry/semantic 均恢复到良好范围，shuffled GT-H 随即出现近 cascade 量级的 geometry/semantic collapse，故 H2C 实际依赖 human condition；aligned generated-H 则复现 collapse，且 shuffled generated-H 并未一致地更差。N64 的 coverage/density 对样本数敏感，尤其 shuffled GT-H 的高 CCov 不能覆盖 CLaTr、F1 与米级 geometry 的同步恶化。D5 排除“H2C 完全忽略 human”与“官方 AE decoder 本身不能支撑 H2C”的解释，支持 generated-H conditional-support shift 或结构化误差是 cascade 主故障面。它尚不能区分误差幅度、时间结构、cross-channel direction 与 H2C training exposure；下一步若需要，会以冻结 v7.47 的 actual-`Δz_h` / magnitude-matched / temporal-matched H2C radius probe 处理，不直接重训 Unified。

### D6 — v7.47 frozen H2C condition-radius probe

该 probe 的预注册定义仅作为历史设计记录；自 `2026-07-19` 起 cascade 不再属于 active evaluation/gate，因此 D6 状态改为 `retired_not_run`，不实现 runner、不占用 GPU，也不据此启动 H2C retraining。若未来用户重新打开 cascade root-cause 轴，必须作为新的显式授权重新审查。原设计使用 D5 的同一 `v7.47` checkpoint、official Pulp owning decoder、val cache、train-only z-normalization、pure4053 前 `64` ordered IDs、`seed=17`、DDIM `50`、CFG `1`、eta `0`、`B=32`、decode batch `16`、`human_text` first pass 与 H2C replay path；下表仅保留当时的四臂定义。

| arm | human latent supplied to H2C | 保留的因素 | 刻意打破的因素 |
| --- | --- | --- | --- |
| `gt` | `z_h^gt` | clean condition | generated error |
| `actual_delta` | `z_h^gt + Δz_h = z_h^gen` | 真实幅度、mean、channel/time correlation、semantic direction | 无 |
| `rms_iid` | `z_h^gt + ε`；每 sample/channel match `Δz_h` 的 valid-frame mean 和 centered RMS | error scale、per-channel DC/variance | 时间相关、cross-channel/semantic direction |
| `spectrum_phase` | `z_h^gt + ε_spec`；每 sample/channel exact match `Δz_h` 的 temporal Fourier magnitude、randomize interior phase | error scale、每 channel temporal power spectrum | phase、cross-channel/semantic direction |

预先固定的解释规则：若 `rms_iid` 与 `spectrum_phase` 都接近 `actual_delta` 的 camera collapse，**误差量级已足够**解释 H2C failure；若 `rms_iid` 明显好而 `spectrum_phase` 仍坏，temporal spectrum/support 是充分风险因素；若两个 matched control 都明显好而仅 `actual_delta` 坏，则 real generated residual 的方向、cross-channel structure 或 text-conditioned support shift 才是主要剩余解释。若 `gt` 也失败、任一 arm 的 identity/sampler/decoder audit 失败，或 human first-pass 不是同一 deterministic latent，D6 无效且不据此继续任何训练。该 N64 screen 仅决定是否值得做 H2C training-exposure ablation；它不能比较 v7.47 与 L0、不能授权 Stage2 continuation，也不能解释为 v8 promotion evidence。

### 6.1 当前 v8 execution snapshot

| stage | run / artifact | status | boundary |
| --- | --- | --- | --- |
| D0 cache / contract | `v8_1a_diag_unified3_30k_seed17_4090g0_20260718` | completed; diagnostic-only train/val cache SHA256=`3b55223d…bd22` / `1050748f…541d` and final contract audit passed | cache remains non-promotion; no cache/checkpoint substitution is permitted |
| G2/D3 health path | same run | completed only as a launch/health path to G3; no standalone D1/D2 or 10K performance claim is used for the G3 conclusion | the formal conclusion comes only from four-profile 30K audit |
| G3 `30K` | same run | completed; four pure4053 profile audits passed, then `stop_30k_broad_camera_regression` was written to the contract | no G4 `105K` continuation, retrain, or mainline/promotion action |
| D4 Direct-C N64 | `v8_1a_d4_directc_n64_seed17_4090g1_20260718` and matched v7.36 artifacts | completed and audited, including the read-only `raw_residual_20260719` recorder; actual signature is Stage2 residual × Stage1 direction-sensitive amplification | no N256/cascade/105K expansion; use the signature to order Stage1 C3 and a later Direct-C camera-sensitive objective/Jacobian control |
| D4.2 camera-text reliance | same matched D4 pair, `camera_text_reliance_20260719` | completed and audited; aligned camera text helps v8.1A on average and condition effect is not consistently weaker than v7.36 | simple condition neglect excluded; no broad condition-path rewrite; next Direct-C control targets sensitive-direction calibration |
| D4.3 decoder sensitivity | `v8_1a_d43_decoder_sensitivity_n64_seed17_5090g0_20260719_r3` and matched v7.36 r3 | completed and audited；`t=50` center/rotation both pass the predeclared candidate-vs-baseline and actual-vs-random rule | supports low-noise direction-selective owning-decoder calibration only；no N256/cascade/105K expansion |
| D5 v7.47 H-source | frozen v7.47 four-arm N64 screen | completed; aligned GT-H recovers camera while aligned generated-H collapses | supports conditional-support shift; does not by itself distinguish magnitude, temporal structure or channel direction |
| D6 H2C radius | historical preregistration only | `retired_not_run`；no runner, preflight or artifact exists | cascade 已退出 active standard；不实现、不占用 GPU |
| Stage1 camera C1/C2 | `v8_1c_joint_ae_yaw001_root003_cctr004067_full636k_seed17_5090g0_20260718` | completed and Stage1-specific audited; center translation improves, but rotation/global-slope boundary fails | only C3 center-weight dose screens; no cache, Unified or v8.1A G4 reopening |
| Stage1 camera C3 first deployment | `v8_1c_center25pct_screen10176_seed17_4090g1_20260718` + `v8_1c_center50pct_screen10176_seed17_4090g0_20260718` | both aborted at optimizer step `214` after about `520 s` (`0.412 step/s`) because two random-small-file loaders contended on one 4090 HDD; no endpoint or eval exists | partial weights/optimizer state are invalid; any retry needs new run IDs, fresh initialization and a prevalidated per-host local-data I/O plan |
| Stage1 camera C3 fresh screens | `v8_1c_center25pct_screen10176_seed17_4090g0_20260719` + `v8_1c_center50pct_screen10176_seed17_4090g1_20260719` | both completed pure4053 and passed contract/non-causal/decoder/gate audit on 4090 local NVMe | predeclared selection chooses the smaller 25% dose; screen weights remain non-promotion and cannot be resumed |
| Stage1 camera C3 seed23 robustness full | `v8_1c_center25pct_full636k_seed23_5090g0_20260719` | completed `636K / 81.38M` and pure4053 owning-decoder audit；Human held and Camera translation improved；global-slope diagnostic passes under non-blocking policy，rotation remains a robustness limitation | robustness evidence；does not replace seed17 owner；5090 path text `nvme` is legacy naming over a SATA SSD replica |
| Stage1 camera C3 selected full | `v8_1c_center25pct_full636k_seed17_4090g0_20260719` | completed fresh `636K / 81.38M` and pure4053 owning-decoder audit；Human/Camera Pareto holds，rotation=`0.705°` passes，global slope raw value=`26.302 mm/100f` | global-slope non-blocking diagnostic pass；current Stage1 mainline and exact Stage2 parent |
| C3 D1 cache geometry | same Stage2 run；full train estimate + frozen eval report | completed and audited；train/eval IDs、cache/stats/contract hashes 与 non-causal boundary 全部匹配；H/C 均无 dead channel，whitened marginal 无 collapse，raw Camera effective rank 明显较低 | low-cost cache-health evidence only；不预测生成质量，不替代 D2 或 30K/105K full eval |
| C3 `10K` three-profile screen | same Stage2 run；immutable `step_10000.pt` first-64 Direct-H/Direct-C/joint parallel | completed；三路 records、ordered first-64 IDs、checkpoint/cache/non-causal/sampler 与 finite audit 全过 | D3 health slice only；N64 数值不进入 formal ranking，也不改变 30K/105K 训练与评测计划 |
| Stage2 C3 mainline evidence run | `v8_1c_c3_25_diag_unified3_105k_seed17_4090g0_20260719` | exact parent/decoder/cache/train-only full-cov stats、non-causal contract 与 hash audit 均通过；D1、`10K` health slice、`30K` 与 `105K` active three-profile formal 均闭合 | current Stage2 mainline；历史 run ID/contract flags 保留 provenance |
| Stage1 camera C3-50 exploratory full | `v8_1c_center50pct_full636k_seed17_4090g1_exploratory_20260719` | completed fresh `636K / 81.38M` and pure4053 audit；more Camera translation improvement but all Human overall metrics and long-bin/slope regress versus C3-25 | dose-response attribution only；confirms higher center dose harms Human horizon and cannot replace selected C3-25 |
| Stage1 C4 gradient calibration | `v8_1c_c4_gradient_calibration_seed17_5090g0_20260719` | completed read-only on 8 real seed17-ordered batches；rotation and horizon are near-orthogonal in the shared encoder；independent `1.25%` doses frozen | quality-neutral scale evidence only；selected endpoint triggers C4-H after C3-50 attribution closes，while C4-R remains blocked because selected rotation already passes |
| Stage1 C4-H screen | `v8_1c_c4h_horizon_screen10176_seed17_4090g0_20260719` | completed fresh `8 epochs / 10,176 steps` and audited；all Pareto guards pass，but both required slope/`193+` targets fail | non-promotion screen closed；no resume and no 5090 fresh full；C5-A read-only follow-up has since closed |
| Stage1 C5-A objective alignment | `v8_1c_c5a_objective_alignment_seed17_4090g0_20260719` | completed read-only and formally audited；all/`193+` primary alignment and both Camera-gradient guards pass；same-set/different-order attempt was retained and fixed only by explicit sample-ID mapping | only justified the separately preregistered C5-B calibration/screen；C5-A itself froze no dose or trained state |
| Stage1 C5-B calibration | `v8_1c_c5b_fresh_gradient_calibration_seed17_23_5090g1_20260719` | seed17/23 fresh train-distribution calibration completed；cross-seed ratio=`1.021≤2`，base=`0.041302533967803944` and `0.5×/1.0×` doses frozen before training | scale evidence only；authorized the preregistered short screens, not full/cache/Stage2 |
| Stage1 C5-B seed17 screen | matched control + dose0.5 + dose1.0 fresh `10,176` runs | control and both treatments completed pure4053；only dose1.0 passed both Human slope/`193+` targets and all eight guards | only dose1.0 advances to fresh seed23 short confirmation；still no full or promotion action |
| Stage1 C5-B seed23 confirmation | matched control + dose1.0 fresh `10,176` runs | both completed pure4053；all eight guards pass but neither Human slope nor `193+` target reaches its threshold | `stop_seed23_confirmation_failed`；two-seed screen closed，无 full/cache/Stage2 |
| six-way recon vis | `v8_1_sixway_recon_20260718` | complete; eight ordered IDs rendered as GT/Pulp/v7.14/v8.1A/v8.1B/v8.2 and served by the separate Stage1 Gradio | visual evidence is diagnostic, not a promotion endpoint |

### 6.2 C5-B fresh-init multi-horizon dose 与两 seed short gate

用户于 `2026-07-19` 授权其余短任务照常执行。C5-B 只处理 Stage1 Human multi-horizon objective，不与上面的 C3 Stage2 `105K` 混成一个 intervention：

1. 先在 5090 GPU1 用 seed `17/23` 分别 fresh 初始化，同一 train-distribution 前 `8×8` ordered samples、fixed max `250`、无 checkpoint/optimizer，计算 unit four-anchor multi-horizon shared-encoder gradient。每个 seed 独立标到 C3-25 parent gradient的 `1.25%`；在读取结果前冻结 base weight 为两条 recommendation 的几何均值。若 max/min `>2` 或任一非 finite/zero，停止，不训练。
2. 第一轮在同一 5090 host、seed17、fresh `10,176` steps 上比较 C3-25 control、`0.5×` base 与 `1.0×` base。三者固定相同 IDs、架构、optimizer、batch、C3 Camera-center/yaw/root weights 与 evaluator，唯一差异是 `human_multi_horizon_weight`；不得加载 C4-H/C5-A state。
3. 每个 dose 相对 control 必须同时满足：fixed-max Human global slope 改善 `≥5%`、`193+` Human global MPJPE 改善 `≥2%`，且 overall Human RA/global/root ADE/FDE/yaw 与 Camera ADE/FDE/rotation 八项各自回退 `≤2%`。两 dose 都过则选 `0.5×`，只过一个则选该 dose，都不过则停止。
4. selected dose 再以 seed23 做一组 fresh control/treatment matched `10,176`-step confirmation，使用同一 gate。只有 seed17/23 都过才允许讨论 full；本轮 pure4053 仍是 development screen，未冻结 sealed audit，因此即使双过也不自动启动 full、cache 或 Stage2。
5. 资源顺序：校准与 seed17 `0.5×` 使用 5090 GPU1 且总占用控制在 `2h` 内；5090 GPU0 顺序执行 seed17 control/`1.0×`；4090 GPU1 可承担不改变 gate 的复核短臂，但必须在 C3 `30K` full eval 前让卡。所有 finite step/ETA 只写 run logs。

> [!info] 已闭合的 screen 决策
> fresh calibration 已通过稳定性 guard。seed17 matched screen 中 dose0.5 未过两个 target，dose1.0 同时通过两个 target 与八项 guard；seed23 confirmation 的八项 guard 仍全过，但两个 target 都未达到门槛。因此 two-seed screen fail 并停止，精确数值与 hashes 只见 [[StoryMotion-valid-metric-ledger#C5-B fresh multi-horizon matched screen]]。

这里的 **fresh screen** 指短预算、从零开始的诊断 run：使用新 run ID，不加载旧 model、optimizer、scheduler、scaler 或 RNG state；model 权重由声明的 seed 重新初始化，optimizer 的 moment 等状态为空而不是“随机初始化”。RNG 是 Python、NumPy、PyTorch CPU/CUDA 以及 DataLoader worker 等伪随机数发生器的状态，控制权重初始化、shuffle、dropout、diffusion noise 或 augmentation 等实际使用的随机过程。matched 两臂固定同一 seed、数据、架构、optimizer、batch、训练步数与 evaluator，使初始化和随机流尽量对齐，唯一 intervention 是该 arm 声明的 auxiliary weight；CUDA/worker 调度仍不承诺 bit-exact determinism。

因此 fresh same-seed screen 的目的，是排除 warm-start 与旧 optimizer state 污染并回答 treatment 的短预算方向，不是单独证明跨 seed 稳定性；独立 seed 重复才提供 robustness evidence。C3-25/C3-50 中的 `25%/50%` 也不是训练进度或数据比例，而是相对 C1 校准权重的 loss dose：`0.0010166945703219975/0.002033389140643995`，分别约占 C0 raw-center 梯度的 `1.25%/2.5%`。两臂都完整训练 `8 epochs / 10,176 steps`。A10 只是 v8.1A 的 matched `10K`-class Stage1 comparator 名称，不是完整 v8.1A endpoint 的别名，更不是 Stage2。

## 7. 执行次序与记录

1. v7.47 formal 与 D5 已闭合；保留 audited system-control/historical attribution evidence。cascade 已退出 active standard，D6 标记为 `retired_not_run`，不进入当前队列。
2. v8.1A 的 G3 已闭合并停止；不能用新筛选 checkpoint 或更长训练重开 G4。
3. C3 fresh 25%/50% screens 已在 4090 本机 NVMe 双 loader 下闭合且都过 gate，证明旧 step-214 问题只是 I/O deployment failure。seed23/seed17 C3-25 full 与 seed17 C3-50 exploratory 也都完成；C3-50 的额外 translation 收益伴随全面 Human horizon 回退，因此不改变 selected C3-25。任何 screen/aborted checkpoint 都不得恢复。
4. D4/D4.2/D4.3 已共同闭合：camera text 被使用，但 v8.1A 的低噪实际 residual 更集中命中 owning decoder 的高增益方向。C4 calibration/C4-H、C5-A 与 C5-B 均已闭合；C5-B seed23 未复现 seed17 target，two-seed screen 停止。pure4053 仍是 development set。
5. C3-25 seed17 的连续 Stage2 `105K` 已完成；D1、`10K` first-64 health slice、immutable `30K` 与 `105K` three-profile formal 均闭合。该 endpoint 已晋升为 mainline；no-reference/render 与 seed23 audit 继续补强外推证据。
6. C5-B calibration、seed17 matched selection 与 seed23 confirmation 已全部闭合；预注册 gate fail，不扩展其他 dose/full。MoMask-Pulp native Direct-H pure4053 baseline 也已在独立 contract 下闭合；它只进入 C-tier ledger，不改变 C3 ladder。
7. 当前没有无条件新增的核心长训：先闭合 C3 `105K` active three-profile，再做 no-reference physical 与 blind render。只有 Direct-C 在 endpoint broad regress 才重开 rollout/semantic calibration；只有 joint Camera 单独失败才做 joint-condition fusion 单变量 screen。两者都通过后，才把 fixed-representation Stage2 seed23 repeat 放入低优先级队列。D6/H2C 与 cascade 不再参与 active priority；v8.1B/v8.2 不进入 `30K/105K` Unified。

新 run 的 mutable state 只写入 remote run contract/log/manifest；G2/G3 的结论更新本页的一行 decision，formal audited metrics 只进入 [[StoryMotion-valid-metric-ledger]]，当前状态只摘要到 [[current]]，最终事件只追加到 [[version_family]]。该路由由仓库根 `AGENTS.md` 约束。

## P0-JC：completion → joint 转化归因（2026-07-21 预注册）

**冻结问题**：C3-25 的 Direct-H / Direct-C 优势为什么没有按相同幅度转化为 joint-parallel 优势；teacher-forced single-step 是否掩盖了 rollout exposure gap。

| ID | 对照 | 唯一回答的问题 | 预注册判据 | 证据等级 |
| --- | --- | --- | --- | --- |
| P0-JC-1 | v8.1A-30K vs C3-25-30K | Stage1 representation 在相同 Stage2 budget 下是否改变 generatability | 仅使用相同 split、4053 IDs、seed17、DDIM50、CFG1、eta0 的正式 artifact | formal matched |
| P0-JC-2 | C3-25 Direct-C(GT H) vs Direct-H → Direct-C(generated H replay) | Camera completion 优势是否依赖 clean Human 条件 | generated-H composition 若在 Camera semantic/distribution 与 paired geometry 上系统性退化，则支持 H→C condition exposure gap | root-cause attribution；非 gate |
| P0-JC-3 | C3-25 generated-H composition vs joint-parallel | 剩余差距是否来自 joint task embedding / coupled rollout，而非 Human 条件质量本身 | composition 恢复而 parallel 仍差，才进入 joint task/coupling；二者都差则先修 H→C exposure | root-cause attribution；非 gate |
| P0-JC-4 | v8.1A 与 C3-25 matched single-step | GT 邻域的局部去噪差异是否已存在 | 只报告 teacher-forced 局部诊断，不外推自由 rollout | diagnostic |
| P0-JC-5 | 新 v8.1A-105K-control vs C3-25-105K | 105K 下的预算对齐结论 | continuation 必须新 run ID、保留 30K optimizer、使用与 C3 相同的 30001 LR decay；不得改写历史 30K run | formal matched after audit |

**停止规则**：P0-JC-2 已确认 exposure gap 时，不先改 Stage1；先设计 Stage2 的 generated/noised-H conditioning 或 joint rollout curriculum。只有 P0-JC-1 与 P0-JC-5 均显示 representation 局限，且 P0-JC-2 不支持 exposure gap，才返回 Stage1。数据清洗和多数据集增广保持独立轴，不用于解释本轮差异。

**运行记录位置**：有限步进度、PID、日志和中间 artifact 只写入对应 `runs/train|eval/stage2/<run_id>/`；本页只在 screen/formal decision 时更新判定行。

### P0-JC screen/formal decision（2026-07-21）

| ID | 状态 | 决策 |
| --- | --- | --- |
| P0-JC-1 | closed from existing matched formal artifacts | A30 ↔ C30 只回答 representation；不与 C105 混写。 |
| P0-JC-2 | passed / hypothesis supported | full-4053 GT-H、generated-H 与 shuffled-H replay 均通过 source-contract audit；支持 H→C condition exposure gap。 |
| P0-JC-3 | passed / second gap supported | generated-H replay 明显优于 joint-parallel，确认 parallel evolving-H / joint-task 的附加损失；下一步进入最小 Stage2 exposure remedy。 |
| P0-JC-4 | completed | A30 与 C3-30 corrected single-step 均完成 full-4053、五 timestep、三模式 audit；结论为 C3 Camera 优势、v8.1A Human 优势、joint Human mixed。 |
| P0-JC-5 | completed | 独立 v8.1A 30K → 105K control 与 C3-25 105K 三模式 matched audit 已闭合；C3 的正式优势集中在 Direct-C 与 joint Camera/system，不包含 Direct-H 全面领先。 |

## 2026-07-22 P0-JC-4 corrected audit boundary

- v8.1A `30K` side is complete and formally audited on `4053` samples for Direct-H, Direct-C, and joint-parallel at `t∈{199,399,599,799,999}`.
- The corrected run explicitly uses `eval_source=single_step`; the earlier mislabeled source-cache run remains invalid provenance.
- The v8.1C C3-25 `30K` runner is reported complete on 5090 GPU1, but its artifact directory is currently unreachable and was not mirrored to 4090. Therefore P0-JC-4 remains open as a matched comparison rather than being promoted from a one-sided audit.
- A-side evidence already shows that the joint gap is present within one denoising diagnostic, especially on Camera: at `t=399`, FCD changes from `28.432` in Direct-C to `47.807` in joint; at `t=999`, from `75.184` to `413.863`. Multi-step rollout accumulation is therefore not the sole cause, although the missing C3 side prevents a representation-level A/C conclusion.

## 2026-07-22 P0-JC-4/5 final decision

- P0-JC-4 is closed with both corrected `30K` halves. C3-25 is easier to denoise on Camera; v8.1A is easier on most Human diagnostics; joint Human is mixed.
- P0-JC-5 is closed with a new independent v8.1A `105K` endpoint and three passed profile audits. The old comparison against v8.1A `30K` was maturity-confounded and must not support a universal completion claim.
- C3-25 remains mainline for the coupled system because it is stronger on Direct-C and joint Camera/system outcomes. The next causal experiment targets Camera exposure to generated/noisy Human from the same C3-105K parent.

## 2026-07-22 P0-JC-6 matched `105K→110K` condition-exposure screen

> [!warning] Screen-only evidence
> 本节是同一 C3-25 parent 上的 `N=512` first-ID screen，不是 pure4053 formal evidence，不进入 [[StoryMotion-valid-metric-ledger]]。四个 checkpoint 均由同一 evaluator 在 `seed=17`、DDIM50、`eta=0`、CFG1 下重新评估 Direct-H、Direct-C clean-H 与 joint parallel；不能拼接旧评估结果。

### 训练臂与闭合 provenance

三臂均从 `v8_1c_c3_25_diag_unified3_105k_seed17_4090g0_20260719` 的 exact `105K` checkpoint/optimizer 继续到 `110K`：

| version / run | Direct-C 的 observed-H treatment | 设备 | 实测壁钟 | `110K last.pt` SHA256 | 合同状态 |
| --- | --- | --- | ---: | --- | --- |
| C0 / `p0_c3_25_105_110k_c0_clean_seed17_4090g0_20260722` | 仅 clean GT-H；matched continuation control | 4090 GPU0 | `41m56s` | `9d168f2e...390989` | passed；screen pending 后闭合 |
| Tq / `p0_c3_25_105_110k_tq_forwardq_seed17_4090g1_20260722` | 对 50% Direct-C 样本使用同 timestep 的 `q(H_gt,t)` | 4090 GPU1 | `41m34s` | `eec094d2...36e93` | passed；screen pending 后闭合 |
| Tj / `p0_c3_25_105_110k_tj_jointpred_seed17_5090g2_20260722` | 对 50% Direct-C 样本使用当前模型 same-timestep detached joint-pred-H Two-Forward；不是完整 DDIM replay | 5090 GPU2 | `34m51s` | `494076da...3399` | passed；screen pending 后闭合 |

初次 post-train audit 因 driver 将完整 test split 基数 `4053` 写入 `data.eval_samples`、同时将本次 `eval.sample_count` 写为 `512` 而一致 fail-closed。修复提交 `b0a3bb0e0e41e0d6dd67c687bd306910a9a74ed2` 仅令二者都为本次实际样本数 `512`；三个 `110K` checkpoint 未修改、未重训。恢复后的 manifest 保留原失败时间和原因，正式 harness audit 与原 `verify_training` 均通过。评估器提交为 `df16b1e79ef8006148ff5f6d1605c9d9f1c63796`。

C0 与 Tq 在 4090 同一步的 task exposure 完全一致。Tj 使用相同 seed、batch、task ratio 与总 exposure，但跨 5090/PyTorch 环境不保证逐样本 RNG bitwise identity；因此 Tj 的负向 screen 可用于停止该实现，不得写成严格 paired effect size。

### 四 checkpoint × 三 profile 结果

Direct-H：

| version / run | FDTMR↓ | TMR↑ | HCov↑ | global MPJPE↓ |
| --- | ---: | ---: | ---: | ---: |
| C3-105K / `v8_1c_c3_25_diag_unified3_105k_seed17_4090g0_20260719` | 293.735 | 15.293 | 0.6486 | 0.7941 |
| C0-110K / `p0_c3_25_105_110k_c0_clean_seed17_4090g0_20260722` | 324.255 | 14.247 | 0.6229 | 0.8074 |
| Tq-110K / `p0_c3_25_105_110k_tq_forwardq_seed17_4090g1_20260722` | 303.547 | 14.846 | 0.6760 | 0.8050 |
| Tj-110K / `p0_c3_25_105_110k_tj_jointpred_seed17_5090g2_20260722` | 346.757 | 13.635 | 0.6094 | 0.8639 |

Direct-C clean-H：

| version / run | FDCLaTr↓ | CLaTr↑ | CCov↑ | caption F1↑ | Cam-ADE↓ |
| --- | ---: | ---: | ---: | ---: | ---: |
| C3-105K / `v8_1c_c3_25_diag_unified3_105k_seed17_4090g0_20260719` | 34.076 | 60.278 | 0.8989 | 0.7658 | 1.592 |
| C0-110K / `p0_c3_25_105_110k_c0_clean_seed17_4090g0_20260722` | 57.650 | 54.257 | 0.8494 | 0.7344 | 1.507 |
| Tq-110K / `p0_c3_25_105_110k_tq_forwardq_seed17_4090g1_20260722` | 47.735 | 55.597 | 0.8984 | 0.7235 | 1.699 |
| Tj-110K / `p0_c3_25_105_110k_tj_jointpred_seed17_5090g2_20260722` | 47.943 | 55.208 | 0.8884 | 0.7287 | 1.628 |

joint parallel：

| version / run | H FDTMR↓ | H TMR↑ | C FDCLaTr↓ | C CLaTr↑ | CCov↑ | F1↑ | Out↓ | H global↓ | Cam-ADE↓ |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| C3-105K / `v8_1c_c3_25_diag_unified3_105k_seed17_4090g0_20260719` | 305.243 | 14.045 | 75.215 | 48.185 | 0.7754 | 0.6184 | 0.1874 | 0.8034 | 2.872 |
| C0-110K / `p0_c3_25_105_110k_c0_clean_seed17_4090g0_20260722` | 291.989 | 14.778 | 74.671 | 47.724 | 0.8047 | 0.6129 | 0.2199 | 0.8215 | 2.785 |
| Tq-110K / `p0_c3_25_105_110k_tq_forwardq_seed17_4090g1_20260722` | 263.539 | 15.343 | 70.596 | 47.309 | 0.8121 | 0.5679 | 0.2179 | 0.8149 | 2.848 |
| Tj-110K / `p0_c3_25_105_110k_tj_jointpred_seed17_5090g2_20260722` | 295.138 | 12.674 | 90.246 | 44.193 | 0.7340 | 0.5635 | 0.2627 | 0.8896 | 2.933 |

全部原始 JSON/records、per-sample joint quality 与 `screen_manifest.json` 位于各 run 的 `runs/eval/stage2/<run_id>/condition_robustness_standard_n512_20260722/`，状态均为 `complete_screen_only`。

### 因果解释与决策

1. **C0 相对 parent 不是“多训 5K 必然更好”。** clean-only continuation 令 Direct-H 与 Direct-C semantic/distribution 整体退化，却改善 joint Human FDTMR/TMR/coverage 以及部分 joint Camera coverage/geometry。completion 与 joint 的梯度/条件域可以相反移动，因此不能再用 completion endpoint 单独预测 joint。
2. **Tq 是正向但 mixed 的机制信号。** 相对 matched C0，Tq 将 Direct-H FDTMR 从 `324.255` 降至 `303.547`、TMR 从 `14.247` 升至 `14.846`，将 joint H FDTMR 从 `291.989` 降至 `263.539`、TMR 从 `14.778` 升至 `15.343`，并改善 joint Camera FDCLaTr 与 CCov。它仍未恢复 parent 的 clean completion，且 joint caption F1/Out 明显不如 parent，所以只支持“同 timestep noisy-H exposure 能缓解部分 joint domain gap”，不支持晋升。
3. **Tj 当前实现停止。** same-timestep current-model joint-pred-H Two-Forward 在 Direct-H、joint Human、joint Camera、F1、Out 与 paired geometry 上均没有形成可接受的 trade-off；不继续加预算，也不将它外推为“所有 generated-H replay 都失败”。
4. **当前 mainline 不变。** C3-105K 保持正式 mainline；C0 仅为 continuation control，Tj=`stop_current_two_forward_arm`，Tq=`continue_secondary_attribution_only`。Tq 在任何 pure4053 formal eval 或继续训练前，先做预注册的 `q(H_gt,t)` 分层鲁棒性曲线，并把低/中/高 timestep 对 Direct-C 与 joint 的作用拆开；不得盲目把 5K 扩到更长预算。

这轮回答了“为什么 completion 优势未自动体现在 joint”：Direct-C 训练只消费 clean GT-H，而 joint Camera 在采样时消费随 timestep 演化的 Human；同时 shared Unified 的额外训练会产生任务间漂移。Tq 的局部修复支持 condition-domain gap，但 F1/Out 未恢复说明它不是唯一根因，joint task routing/caption-framing objective 仍需单独定位。

## P0-JC-7：completion 三模式统一分析与 Tq 分层归因（2026-07-22）

> [!important] 证据级别
> 本节全部为固定首批 test IDs、`N=512`、seed17 的 screen-only 证据，不进入正式 metric ledger，也不改变 C3-105K 的 mainline 身份。四分支 full-sampling screen 已覆盖 Direct-H、Direct-C clean-H 与 joint-parallel；single-step 分层只保留 Parent、C0、Tq，因为 Tj 已在 matched screen 中形成广泛负向控制结论。

### 四分支的三模式联合判读

- **C0-110K**：相对 Parent，Direct-H 与 Direct-C 的语义/分布指标整体退化，但 joint Human 与部分 joint Camera 指标改善。额外 5K 的 joint 训练发生了 mode-specific drift，completion 不能替代 joint gate。
- **Tq-110K**：相对 C0，Direct-H 的 FTD/TMR/HCov 与 Direct-C 的 FCD/CLaTr/CCov 均有恢复；joint 获得最佳 Human FTD/TMR，并改善 Camera FCD/coverage。相对 Parent，它仍未恢复 Direct-C caption F1，joint 的 F1/Out 也未形成优势，因此只能解释机制，不能 promotion。
- **Tj-110K**：相对 C0，Direct-H、joint Human、joint Camera 与 framing 指标广泛退化；当前 Two-Forward 实现停止。该结论不外推到所有 generated-H replay。
- **统一结论**：Tq 修复的是 noisy observed-H 条件域，而不是所有三模式共享的生成质量。Human denoising、Camera semantic alignment、framing/Out 必须继续并列报告，不能用任一 completion 或 joint 单项代替三模式证据。

### standard single-step：收益与代价所在的 timestep

Direct-H 中，Tq 的 TMR/coverage 改善主要出现在 `t≤599`，在 `t=799` 仅部分挽回 C0，`t=999` 三分支均坍缩。joint 的 Human 收益主要出现在 `t=199/599/799`，但 Camera/F1 经常同步退化。这与 full sampling 中“joint Human 强、framing 未恢复”的结果一致。

Direct-C clean-H 则随 timestep 一致退化：

| `t` | C0→Tq FCD ↓ | C0→Tq CLaTr ↑ |
| ---: | ---: | ---: |
| 199 | 4.797→5.549 | 69.482→69.044 |
| 399 | 7.103→8.946 | 69.075→68.182 |
| 599 | 9.868→13.600 | 68.469→66.707 |
| 799 | 11.906→19.526 | 67.384→65.101 |
| 999 | 26.956→52.183 | 62.318→56.854 |

这排除了“Tq 只是让 clean-H Camera denoiser 更强”的解释。

### exact `q(H_gt,t)` intervention：因果定位

下表只改变 Camera 模型实际接收的 observed Human 条件：使用与目标 `q(z_gt,t)` 相同 timestep、相同确定性噪声的 `q(H_gt,t)`；最终 observed 分支与监督目标仍为 clean GT。

| `t` | C0→Tq FCD ↓ | C0→Tq CLaTr ↑ | C0→Tq CCov ↑ | C0→Tq F1 ↑ | C0→Tq CamADE ↓ |
| ---: | ---: | ---: | ---: | ---: | ---: |
| 199 | 6.147→5.747 | 68.747→68.956 | .9863→.9863 | .8901→.8937 | .296→.282 |
| 399 | 24.579→9.128 | 63.884→67.830 | .9473→.9688 | .8421→.8650 | .541→.394 |
| 599 | 95.460→15.928 | 51.956→65.781 | .7791→.9647 | .6688→.8435 | 1.248→.550 |
| 799 | 325.825→29.359 | 35.010→62.176 | .3397→.9083 | .3506→.7900 | 3.016→.910 |
| 999 | 548.842→376.413 | 20.561→36.332 | .1173→.1664 | .1257→.2671 | 4.186→2.375 |

- 有效带明确落在 `t=399–799`；`t=199` 差异很小。
- `t=999` 虽相对 C0 有改善，但绝对质量仍坍缩，不能计为有效训练收益。
- `t=999` 的 Human TMR 数值会在 FTD 约 970–999、HCov 约 .04–.05 时异常升高；这是 near-static/collapsed endpoint 的度量病理，不是语义质量提升。
- uniform `t∈[0,999]`、probability `0.5` 的 Tq 暴露过强：它获得 noisy-H 鲁棒性，却损害 clean-H Camera 与 framing。
- 唯一值得预注册的后续候选是 lower-dose band-limited mix，例如 `clean-H 75% + q(H_gt,t) 25%` 且 `t∈[399,799]`。该参数目前只是由 screen 导出的候选，不是已授权实验。

### 产物与可复现性

- code commit：`aed514788f3e8bc6ad76193b105baa4a8c714399`
- standard：3 branches × 5 timesteps × 3 profiles = 45 outputs
- exact forward-q Camera：3 branches × 5 timesteps = 15 outputs
- 总计：60 outputs；所有 driver manifest 均为 `complete_screen_only`
- 路径：`runs/eval/stage2/<run>/tq_timestep_attribution_standard_n512_20260722/`
- 路径：`runs/eval/stage2/<run>/tq_timestep_attribution_forwardq_camera_n512_20260722/`

## P0-JC-8：Tb25-band lower-dose condition exposure（2026-07-22 预注册）

> [!warning] Screen-only contract
> 本 arm 是 C3-105K 同 parent 的 condition-exposure 与 completion/joint 冲突诊断，不是 promotion run。训练结束后的 `N=512` 三模式结果只进入本页与 run artifacts，不进入 [[StoryMotion-valid-metric-ledger]]；C3-105K 在正式证据层继续保持 mainline。

### 冻结训练边界

| 字段 | 冻结值 |
| --- | --- |
| version / run | Tb25-band / `p0_c3_25_105_110k_tb25_band399_799_seed17_5090g2_r4_20260722` |
| exact parent | `v8_1c_c3_25_diag_unified3_105k_seed17_4090g0_20260719`，`105K→110K` matched continuation，共 `5K` steps |
| task probability | `[camera,human,joint]=[1,1,1]`；Human-text-only 槽为 `0` |
| treatment scope | 仅 Direct-C；其中 25% 样本把 observed Human 替换为同 timestep 的 `q(H_gt,t)` |
| timestep | treated Direct-C 均匀采样闭区间 `[399,799]`，Camera target 与 `q(H_gt,t)` 共用该 timestep |
| untouched samples | 其余 75% Direct-C、全部 Direct-H 与全部 joint 保持原 timestep 分布 |
| expected exposure | Direct-C 条件比例约 `25%`；全部训练样本 overall qH exposure 约 `1/3 × 25% = 8.3%` |
| RNG | treatment 使用 seed `170105` 的 dedicated generator，不推进 data/task/timestep/noise RNG；check 使用独立同 seed generator |
| normalization | immutable byte SHA `7decc3dd213d5af79176eeb3d95d1ba2561994bce0cf04fffa7cbd40b38742af`；semantic SHA `2f9946a411fe33091e52962bea689aa0bbc35601edd8e879b35c20581d92fe5f` |
| code | driver SHA `85f1e82272a64ecfe5e9325cc91e24966a61c3c6bb5939ae9262819aaece5e5b`；train-script SHA `b02451cc1f33735467845cd0b51e1721e3b2bf8e1d485e1c72fbc72cf619a7f7` |

执行状态、有限 step、ETA 与 GPU worker 信息的唯一 owner 是该 run 的 `manifest.json`、`preflight.log`、`launcher.log` 与 `train_log.jsonl`，本页不复制运行日志。

### 冻结 `N=512` screen 问题

同一 first-512 IDs、seed17、DDIM50、CFG1、`eta=0` 下重跑 Direct-H、Direct-C clean-H 与 joint parallel，并把 Tb25-band 与 Parent C3-105K、C0-110K、uniform Tq-110K 比较；Tj-110K 只保留 negative control 身份。

1. Tb25-band 是否相对 uniform Tq 恢复 Direct-C clean-H 的 FCD、CLaTr、caption F1 与 Cam-ADE。
2. Tb25-band 是否保留 uniform Tq 在 joint Human FTD/TMR 与 joint Camera FCD/CCov 上的收益。
3. joint caption F1 与 Out 是否恢复，而不是只改善 noisy-H robustness。
4. Direct-H 是否出现 broad regression；任何 Camera 收益都不能通过牺牲 Human 取得。

### 后续冲突归因边界

本轮训练不加入 gradient instrumentation。若三模式 screen 仍显示 completion/joint 互相拉扯，下一步只做同 checkpoint、同 IDs、同 timestep band 的 no-update attribution：分别计算 `L_DC_clean`、`L_DC_qH`、`L_joint_H` 与 `L_joint_C`，报告 shared trunk、task/source router、Human path、Camera path 与 output head 的 gradient cosine 和 norm ratio，不执行 optimizer step。

只有该 attribution 确认 Camera-related 冲突后，才讨论 source-conditioned Camera residual adapter 或 Camera-loss 范围内的 PCGrad/CAGrad。shared Human path 与 Direct-H 保持保护边界；不能通过降低 Human loss、修改 Stage1 或先对全模型应用 gradient surgery 来“修复” Camera。

### 训练闭合与实际 exposure

preflight 通过后，r4 从 exact C3-105K parent 完成到 `110K`，训练 owner manifest 的终态保持 `trained_110k_screen_eval_pending`。endpoint checkpoint SHA256 为 `153c5c61a350ccffca9601908bac5211b31e5caaaed51dc07147605f02ff641a`；immutable normalization artifact 在训练前后均为只读 `0444`，byte SHA256 仍为 `7decc3dd213d5af79176eeb3d95d1ba2561994bce0cf04fffa7cbd40b38742af`。

最终 task exposure 为 Camera `853,721`、Human `853,382`、joint `852,897`，总计 `2,560,000` samples。50 个记录点上的 overall qH exposure 均值为 `0.081836`，Direct-C conditional treatment 均值为 `0.246401`；treated timestep 实测覆盖 `399–799`，均值 `598.966`。这与预注册的约 `8.3%` overall、`25%` Direct-C 和闭区间 band 一致。

### `N=512` 三模式 screen 结果

五个版本使用同一 ordered first-512 IDs、seed17、DDIM50、CFG1、`eta=0`；ordered-ID SHA256 均为 `6b9c92a533d2d0aff76cce6c7ad23361733fb38d3157128bf7eee56cdc33d8df`。所有行都是 `screen`，不是 formal evidence。

Direct-H：

| version / run | FDTMR↓ | TMR↑ | HCov↑ | global MPJPE↓ |
| --- | ---: | ---: | ---: | ---: |
| Parent C3-105K / `v8_1c_c3_25_diag_unified3_105k_seed17_4090g0_20260719` | 293.735 | 15.293 | 0.6486 | 0.7941 |
| C0-110K / `p0_c3_25_105_110k_c0_clean_seed17_4090g0_20260722` | 324.255 | 14.247 | 0.6229 | 0.8074 |
| Tq uniform-110K / `p0_c3_25_105_110k_tq_forwardq_seed17_4090g1_20260722` | 303.547 | 14.846 | 0.6760 | 0.8050 |
| Tb25-band-110K / `p0_c3_25_105_110k_tb25_band399_799_seed17_5090g2_r4_20260722` | 328.041 | 14.133 | 0.5954 | 0.8479 |
| Tj-110K negative control / `p0_c3_25_105_110k_tj_jointpred_seed17_5090g2_20260722` | 346.757 | 13.635 | 0.6094 | 0.8639 |

Direct-C clean-H：

| version / run | FDCLaTr↓ | CLaTr↑ | CCov↑ | caption F1↑ | Cam-ADE↓ |
| --- | ---: | ---: | ---: | ---: | ---: |
| Parent C3-105K / `v8_1c_c3_25_diag_unified3_105k_seed17_4090g0_20260719` | 34.076 | 60.278 | 0.8989 | 0.7658 | 1.592 |
| C0-110K / `p0_c3_25_105_110k_c0_clean_seed17_4090g0_20260722` | 57.650 | 54.257 | 0.8494 | 0.7344 | 1.507 |
| Tq uniform-110K / `p0_c3_25_105_110k_tq_forwardq_seed17_4090g1_20260722` | 47.735 | 55.597 | 0.8984 | 0.7235 | 1.699 |
| Tb25-band-110K / `p0_c3_25_105_110k_tb25_band399_799_seed17_5090g2_r4_20260722` | 72.422 | 53.437 | 0.8124 | 0.7144 | 1.513 |
| Tj-110K negative control / `p0_c3_25_105_110k_tj_jointpred_seed17_5090g2_20260722` | 47.943 | 55.208 | 0.8884 | 0.7287 | 1.628 |

joint parallel：

| version / run | H FDTMR↓ | H TMR↑ | C FDCLaTr↓ | C CLaTr↑ | CCov↑ | F1↑ | Out↓ | H global↓ | Cam-ADE↓ |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Parent C3-105K / `v8_1c_c3_25_diag_unified3_105k_seed17_4090g0_20260719` | 305.243 | 14.045 | 75.215 | 48.185 | 0.7754 | 0.6184 | 0.1874 | 0.8034 | 2.872 |
| C0-110K / `p0_c3_25_105_110k_c0_clean_seed17_4090g0_20260722` | 291.989 | 14.778 | 74.671 | 47.724 | 0.8047 | 0.6129 | 0.2199 | 0.8215 | 2.785 |
| Tq uniform-110K / `p0_c3_25_105_110k_tq_forwardq_seed17_4090g1_20260722` | 263.539 | 15.343 | 70.596 | 47.309 | 0.8121 | 0.5679 | 0.2179 | 0.8149 | 2.848 |
| Tb25-band-110K / `p0_c3_25_105_110k_tb25_band399_799_seed17_5090g2_r4_20260722` | 279.316 | 13.432 | 96.945 | 46.192 | 0.7286 | 0.5857 | 0.2258 | 0.8850 | 2.899 |
| Tj-110K negative control / `p0_c3_25_105_110k_tj_jointpred_seed17_5090g2_20260722` | 295.138 | 12.674 | 90.246 | 44.193 | 0.7340 | 0.5635 | 0.2627 | 0.8896 | 2.933 |

r4 screen artifact root 为 `runs/eval/stage2/p0_c3_25_105_110k_tb25_band399_799_seed17_5090g2_r4_20260722/condition_robustness_standard_n512_20260722/`，manifest SHA256 为 `73f729dd981b0f66c95861899490d10139ec8c8434c321dec6b33a020c560823`。Direct-H result/records SHA256 为 `d27708816cf4ff82c60b6377e3e9c68974981fab3bb6bf46107be9edc17b3587 / 9ee88c0f23a019d1da646f2da6526672b9e91d7d2a68954b2d98dc90a333dee6`；Direct-C 为 `e6a0b612515f3a03ac704532b5f654bbf74e2f8b99c38400bee220dbdba4a3c0 / 05289c828a33fae615e1bc5db6c1b83b0b13604fb6d0e5dc9f472d1fefc11255`；joint 为 `5e5f006d90fd5919b49a2f0ded8907f8fecd2abe9522f286af69ae5f02cd2f54 / ad2ada3c87e361622a1c7266e33105335ea18f77f03d4863adef08c03cb0ea97`。screen driver SHA256 为 `a1bb83dcbf5dc85ed86af1fb9c4dd50338c2a59a90702d26c29d6226fbd3e347`，evaluator SHA256 为 `8cfa0eb9a725bd8d4da87be95cce0af9b51989c47c6ab8ba89bff0a8029d9de5`。

### screen 裁决

1. **Tb25-band 未恢复 Direct-C clean-H。** 相对 Tq，Tb25 的 FDCLaTr `47.735→72.422`、CLaTr `55.597→53.437`、CCov `0.8984→0.8124`、F1 `0.7235→0.7144` 均变差；Cam-ADE `1.699→1.513` 单项改善不足以抵消 semantic/distribution/framing regression。相对 C0 也没有形成可接受 trade-off。
2. **Tb25-band 未保留 Tq 的 joint 收益。** joint Camera FDCLaTr `70.596→96.945`、CCov `0.8121→0.7286`，joint Human TMR `15.343→13.432`；F1 虽从 `0.5679` 部分回升到 `0.5857`，仍低于 Parent/C0，且 Out 与 Human global 同时变差。
3. **Direct-H 出现 broad regression。** Tb25 的 FDTMR、TMR、HCov 与 global MPJPE 均差于 Parent 和 Tq。它只在 joint Human FDTMR 上保留相对 Parent/C0 的局部信号，不能据此继续。
4. **停止当前 arm。** Tb25-band 是 `stop_screen_broad_regression`，不是 promotion candidate；C3-105K 保持正式 mainline。该 screen 不进入 metric ledger。

### evaluator 标准路径等价性

r4 使用 evaluator SHA256 `8cfa0eb9a725bd8d4da87be95cce0af9b51989c47c6ab8ba89bff0a8029d9de5`，历史 comparators 使用 `3ada6fd2c81ed8a6122a837968a3da82b596dfba66c9fbc573dc873e08531fa2`。为排除代码版本混合，Parent 在新 evaluator 上用同 IDs/seed/sampler 完整复跑三模式：三个 metric dictionaries 逐值完全相同，三份 records JSONL 也分别逐字节相同，SHA256 为 `69bab021d2ced1292eafbfc02348a67440ac0f50b6b969c99e1b36ea5b8d245e`、`51e6800b836cc2bffff85e8c1d7ab6f115f8aee8bd650b2ff8b4c34a0e44e529`、`d55f2192a12e850d2943c060a6c459244be7ac23c855ca3fda3796fe50f87123`。因此本轮标准 full-sampling comparison 不受新增 single-step intervention 路径影响。

### no-update gradient attribution

由于 screen 触发预注册条件，在 r4 endpoint 上用相同 512 IDs、seed17、同一 deterministic noise 与均匀闭区间 `t∈[399,799]` 计算 `L_DC_clean`、`L_DC_qH`、`L_joint_H`、`L_joint_C`。模型为 eval/full-condition，joint 使用 active screen 的 `coupling_scale=0`、`c_to_h_blocked`。每个 objective 先在四个等大的 128-sample shards 上分别求 batch-mean loss 的 `torch.autograd.grad`，再等权平均成 N=512 gradient；最后在每个 parameter view 上计算 `cos(g_a,g_b)=dot(g_a,g_b)/(||g_a||·||g_b||)` 与 `||g_a||/||g_b||`。描述性标签固定为 cosine `<-0.1` negative、`[-0.1,0.1]` near-orthogonal、`>0.1` aligned；这不是显著性检验。没有构造 optimizer，没有 optimizer step，所有 parameter `.grad` 保持空；checkpoint 前后 SHA256 均为 `153c5c61a350ccffca9601908bac5211b31e5caaaed51dc07147605f02ff641a`。

下表每格为 `cosine / first-to-second norm ratio`。Human/Camera path 是 modality-sliced input projection 加对应 output rows；output head 与两者有意重叠，其余主体参数归入 shared trunk。

| parameter block | DC-clean vs DC-qH | DC-clean vs joint-C | DC-qH vs joint-C | joint-H vs joint-C |
| --- | ---: | ---: | ---: | ---: |
| shared trunk | `0.262 / 0.700` | `0.604 / 1.241` | `0.323 / 1.774` | `0.136 / 0.541` |
| task/source router | `-0.184 / 1.053` | `0.000 / 1.612` | `0.000 / 1.531` | `-0.014 / 0.303` |
| Human path | `0.056 / 0.908` | `0.526 / 2.670` | `0.218 / 2.941` | `0.158 / 1.547` |
| Camera path | `0.481 / 0.785` | `0.715 / 1.192` | `0.515 / 1.519` | `undefined / 0.000` |
| output head | `0.588 / 0.940` | `0.719 / 1.253` | `0.654 / 1.334` | `0.000 / 0.741` |

这里需要拆开两种结论。对真正回答 completion/joint 冲突的两组比较，`DC-clean vs joint-C` 与 `DC-qH vs joint-C` 在 shared trunk 分别为 `0.604/0.323`、Camera path 为 `0.715/0.515`、output head 为 `0.719/0.654`，都属于正向 aligned；Human I/O path 也为正。**这些块不是“结构性正交”。** 结构性正交只出现在跨 task 的 router 比较为精确 `0`，因为 Camera task 与 joint task 更新 `task_embed.weight` 的不同 rows；以及 joint-H/joint-C 在 output head 为 `0`，因为两者更新不相交的 Human/Camera output rows。Camera path 的 joint-H gradient 为零也由切片定义直接造成。output head 又与 Human/Camera path 有意重叠，不能把它们当作三份统计独立证据。

因此本实验支持的窄结论是：**在 r4 final checkpoint、这 512 个 IDs 和这一 timestep band 上，未观察到 Direct-C 与 joint-C 在所定义共享主体/Camera I/O 参数上的负平均梯度夹角。** 它不证明整个训练轨迹不存在冲突，也不覆盖其他 checkpoint、timestep、数据切片或 batch-level cancellation；4 个 128-sample shard 只能作为方向稳定性补充，不能把局部 no-update attribution 升格为无冲突定理。当前证据不足以启用 PCGrad/CAGrad。

唯一重复出现的局部反向信号是 `DC-clean vs DC-qH` 在 `task_embed.weight` 上 aggregate cosine `-0.184`，4 个 shard 为 `-0.468 / -0.569 / -0.553 / 0.258`，即 3/4 为负、并非全 shard 稳定。本 checkpoint 的 router block 只有 `task_embed.weight`；source router 未启用，跨 Camera-task/joint-task 的 router cosine 为 `0` 是不同 embedding rows 的结构性正交，不是功能解耦证明。该结果支持“clean-H 与 qH 暴露缺少 source-conditioned parameterization”这一窄假设，但不足以证明它单独造成三模式 broad regression。

因此当前裁决是：不做全模型 gradient surgery，不降低 Human loss，不修改 Stage1。若后续另行授权，只允许先设计 Camera-only、source-conditioned residual/router 的 matched feasibility contract：noisy-H/joint Camera 激活，shared Human path 与 Direct-H 无 adapter，clean-H Camera 保留 parent consistency/distillation；在任何训练前先冻结参数 ownership 与 Human no-regression gate。

### attribution artifacts

- root：`runs/eval/stage2/p0_c3_25_105_110k_tb25_band399_799_seed17_5090g2_r4_20260722/no_update_gradient_attribution_band399_799_n512_20260722/`
- attribution script SHA256：`95ee55a269ae5004923bad945c0a75294038376ef5328731a77173f975b789d2`
- `gradient_attribution.json` SHA256：`5a92033465f69edabcc5cc11e73eb710b739eada99944920c303caf7674dc468`
- `manifest.json` SHA256：`1b4b9257fbcc81b93c2ca247ac5a764098b3bff2433ab024d3e191552421474d`
- 两个 artifact 均为只读 `0444`；ordered-ID SHA256 为 `6b9c92a533d2d0aff76cce6c7ad23361733fb38d3157128bf7eee56cdc33d8df`。

## P0-JC-9：architecture-view consistency 2×2（2026-07-22 预注册）

### 因果问题

Tb25 和 no-update gradient attribution 没有确认 shared Camera parameters 的负平均夹角，但 mainline 仍有两个直接可见的 view mismatch：Human 侧是 Direct-H full noisy latent + Human-only text 对 joint-H isolated Camera latent/text；Camera 侧是 Direct-C clean observed Human + Camera-only text 对 joint-C noisy Human + dual text。当前诊断只改变这些 view，不改变 task ID、default learned task embedding、loss mask、Stage1、cache、normalization、task probability 或训练预算。

### 四个独立 arm

| arm | run ID | Human view | Camera view | 预注册问题 |
| --- | --- | --- | --- | --- |
| H-FULL | `p0_c3_25_unified3_hview_full_0_105k_seed17_4090g0_20260722` | Direct-H/joint-H 均为 full latent + dual text | mainline Direct-C/joint-C 不变 | Human 是否受益于两处都保留 Camera context |
| H-ISOLATED | `p0_c3_25_unified3_hview_isolated_0_105k_seed17_4090g1_20260722` | Direct-H/joint-H 均为 isolated Camera latent/text | mainline Direct-C/joint-C 不变 | Human 是否受益于两处都执行严格 `C→H` 阻断 |
| C-JOINT | `p0_c3_25_unified3_cview_joint_0_105k_seed17_4090g0_20260723` | mainline mixed Human views 不变 | Direct-C/joint-C 均为 full noisy latent + dual text | 只消除 `H_0↔H_t`、显式 obs-mask role 与 Human-text routing 的 Camera mismatch 是否足够 |
| ALL-JOINT | `p0_c3_25_unified3_all_joint_view_0_105k_seed17_4090g1_20260723` | Direct-H/joint-H 均为 full | Direct-C/joint-C 均为 full | 四个 slice 共用 view 后，剩余 task/loss 差异是否仍产生 direct/joint gap |

四组都是 C3-25 seed17 fresh continuous `0→105K` diagnostics，不是 C3-105K continuation，也不是 promotion runs。失败的首次 C-JOINT/ALL-JOINT preflight root 原样保留为 0-step provenance；4090 execution 使用全新 run root，不复用任何 5090 planned/failed ID。精确代码 SHA、normalization byte/semantic SHA、host/GPU 与实时状态只读各自 `experiment_contract.json`、`manifest.json` 和日志，本页不复制 mutable step/ETA。

### 固定合同与判定顺序

1. 四组保持 `[camera,human,joint,human_text]=[1,1,1,0]`、seed17、batch512、105K、相同 snapshots/LR schedule、C3-25 Stage1/cache 与只读 normalization artifact。
2. C-JOINT/ALL-JOINT 在 Direct-C 的内部 model view 清除 observed-H mask，使 latent 真正成为 `[H_t,C_t]`；同时把 `source_meta.mask_ratio` 对齐为 0 并保留 `[e_C,e_H]`。task 仍为 Camera-0，loss 仍只监督 Camera-64。
3. H-FULL 对 H-ISOLATED 是 Human Camera-context 端点比较；C-JOINT 对 mainline 是 Camera 单轴比较；ALL-JOINT 对 H-FULL/C-JOINT 才回答两轴 interaction。不能从任一单行结果直接归因 task embedding。
4. 完成后使用同一 ordered IDs、seed17、sampler、CFG 与 owning decoder 做 Direct-H、Direct-C、joint parallel screen。首先检查 Direct-H broad regression，再检查 Direct-C/joint Camera distribution、semantics、framing/geometry，最后看 direct/joint gap 是否收窄。
5. ALL-JOINT 即使改善指标，也因 Direct-C 不再内部观察 clean Human 而只作 root-cause evidence；恢复正式 Camera-completion 语义需要另立 source-conditioned Camera-only contract。`N=512` screen 可进入 metric ledger 的显式 diagnostic 区，但不能进入 formal ranking/promotion table。

### 停止与下一步 gate

- 任一 arm 出现 Direct-H broad regression：不得作为后续 architecture owner。
- C-JOINT 只改善 joint 而损害 Direct-C：说明简单 view tying 不是可用 completion contract，不继续加 task/loss 干预。
- H-FULL 与 H-ISOLATED 均不能改善 Human consistency：不再把 Camera nuisance state 视为主要 Human gap。
- ALL-JOINT 没有超过两个单轴 arm 的共同边界：不支持双轴 interaction，优先回到 Camera-only source-conditioned routing。
- 只有 view 对齐在 Human hard boundary 下产生稳定三模式收益，才授权下一轮将同一 view policy 与正式 completion semantics 重新组合；PCGrad/CAGrad、降低 Human loss与 Stage1 修改仍不授权。

### H-axis 两端点 N=512 screen（2026-07-23）

H-FULL 与 H-ISOLATED 均完成 fresh continuous `0→105K` 训练及 matched
Direct-H、Direct-C clean-H、joint parallel screen。审计后的数值、协议与 artifact
hashes 统一由
[[StoryMotion-valid-metric-ledger#5.4 Architecture-view consistency 四臂 N=512 screen]]
持有；本节只保留该 screen 的预注册裁决。

#### H-axis 裁决

1. **严格隔离 Camera nuisance 对 Human distribution/semantics 有明确正信号。** H-ISOLATED 相对 Parent 同时改善 Direct-H FDTMR、TMR、HCov，以及 joint-H FDTMR、TMR、HCov；它也整体优于 H-FULL 的 Human endpoint。H-FULL 只在 FDTMR/coverage 上改善，Direct-H TMR 略降。
2. **这不是 Human Pareto win。** H-FULL 与 H-ISOLATED 的 Direct-H global MPJPE 均从 Parent 的 `0.7941` 退到 `0.8103/0.8120`，joint global 也退化。因此 H-ISOLATED 是 Human semantic/distribution candidate，不满足无代价的 Human no-regression。
3. **两种一致化都引起 Camera broad regression。** H-FULL 与 H-ISOLATED 没有改变 Direct-C 的 `[H_0,C_t]+[e_C,0]` view 或 Camera-only loss，却都使 Direct-C FDCLaTr/CLaTr/CCov/F1 及 joint Camera 的主要 semantic/distribution/F1 指标差于 Parent。少数 geometry/framing 单项改善不能抵消这一结果。
4. **因果解释收窄为 shared-training trade-off。** Human view mismatch 确实影响 Human generatability，但把两个 Human slice 绑到同一端点会通过 shared network 改变 Camera endpoint；现有 direct/joint gap 不能归结为单一 Human 输入不一致，也不能通过直接选择 H-FULL 或 H-ISOLATED 解决。
5. **两条 arm 均不成为 architecture owner，Parent C3-105K 保持 mainline。**
   P0-JC-9 的 Human 轴裁决由下述 Camera 轴结果补全。当前仍不授权
   PCGrad/CAGrad、降低 Human loss或无归因的 Stage1 修改。

### C-axis 与 ALL-JOINT N=512 screen（2026-07-24）

C-JOINT 与 ALL-JOINT 均完成 fresh continuous `0→105K` 和 exact-wrapper r3
三模式 screen。审计数值、same-host Parent backfill 与 artifact hashes 统一由
[[StoryMotion-valid-metric-ledger#5.4 Architecture-view consistency 四臂 N=512 screen]]
持有；本节只记录预注册问题的答案。

1. **C-JOINT 没有把 Camera mismatch 转化为收益。** 它在 Camera task 中把
   `[H_0,C_t]+[e_C,0]` 直接改成 `[H_t,C_t]+[e_C,e_H]` 后，Direct-H、
   arm-effective Camera task 与 joint 的主要 distribution/semantic endpoint
   均 broad regress。故 clean/noisy Human source、obs-role 与 dual-text mismatch
   是真实接口差异，但“全部直接绑成 joint view”不是充分修复。
2. **ALL-JOINT 没有出现双轴协同。** 四个 slice 使用同类 full latent/dual-text
   view 后，Human 与 Camera 仍全面退化，且没有超过 H/C 单轴 arm 的共同边界。
   这关闭了朴素 view equality 的 `105K` 路线。
3. **Camera-task 行不是 clean-H completion。** C-JOINT/ALL-JOINT 的 wrapper
   清除了 observed-H mask；这些结果只回答 root-cause view tying，不拥有正式
   Camera-completion 语义。
4. **Parent C3-105K 继续持有 mainline。** 四条 architecture-view arm 均停止，
   不再追加相同 view 组合的 `105K` 训练。结果不能归因 task embedding，因为
   task row 保持默认且尚未做 T1 override。
5. **VACE 启发被收窄而非推翻。** 结果否定“用同一个 numeric view 消除差异”，
   但没有检验将 condition value、preserve/generate role、source reliability、
   text presence 与 loss mask 分离的 control plane。该接口重构降为 Human
   objective/manifold 归因后的候选，不立即训练 adapter。

## P0-JC-10：task-row、context-role 与 loss-dose no-update attribution

### 预注册顺序

1. **T0 view-equivalence。** 在 ALL-JOINT 固定同一 ID、`z_0`、`ε`、`t` 与 text，
   assert Direct/joint 对应 branch 的 numeric state、obs-mask、routed text 和
   source-meta 完全一致；full joint 的两次 shared-weight forward 也应数值等价。
2. **T1 task-embedding-row efficacy。** semantic/routing task 保持不变，只用 hook
   比较 `own/zero/wrong-row`。Primary 是 ALL-JOINT，Parent 是 native-view sanity；
   先跑 ordered `N=512` latent-only，不创建 optimizer，不修改 checkpoint。
3. **T2 context-role mask。** 固定 numeric `[H_t,C_t]`、dual text、task row 与
   Camera-only target，只比较 mask0 与“Human role mask=1 但 `obs_x0=H_t`”；随后才
   单独比较 `H_0↔H_t`。这样把 value 与显式 mask channel 拆开。
4. **T3 loss geometry。** 在 ALL view 且强制 shared task row 后，分别求
   `L_DH/L_JH`、`L_DC/L_JC` 的 no-update gradients，再单独组合当前
   `2/3 Human + 1/3 Camera` joint dose。

T1 只有在 own row 相对 zero/wrong row 对 branch MSE 形成跨 timestep/shard 的稳定
practical gain 时才称 useful。T2/T3 未命中前不重构接口；任一项命中后也只能各自
开启一个 matched short arm，不能把 task row、mask role 与 loss dose 合并成一次训练。

T1 的 no-update implementation 已准备：固定 semantic task 与 effective
latent/text/obs-mask/source-meta，只覆盖 `task_embed` 输出；使用
`t=[199,399,599,799,999]`、4×128 shards，并同时记录 input/prediction SHA、
checkpoint before/after SHA 与空 `.grad` 断言。脚本为
`scripts/storymotion_c3_25_task_embedding_probe.py`，当前 SHA256
`d80c3237737ff0fd034d9b419889ff58d2bf95657314d548dbf00d460bc16f5c`。
probe 必须显式绑定 immutable normalization manifest 的 byte/semantic/source-cache
SHA；Parent contract 的历史 `0c97…` byte 仅作 provenance 记录，不被重写，也不声称
由 semantic-equivalent artifact 找回。
它尚未产生 result；ALL-JOINT 的 exact-wrapper `105K` endpoint 已封存，因此
T0/T1 具备只读运行条件，Parent sanity 使用同一 ordered IDs。由于 ALL-JOINT
已 broad fail，T1/T2 现在只回答“task row/context role 是否有效”，不能自动授权
新架构训练；执行优先级低于 P0-HUM-1 后续的 Human heading/manifold attribution。
任何运行状态只写对应 output manifest。

## P0-HUM-1：C3-25 原生 Direct-H 单任务学习曲线（2026-07-23 预注册）

### 因果问题

当前 Direct-H 与 joint-H 的 Human 自由生成质量均不充分，但 C3-25 没有使用当前
Unified-3 branch implementation 的 Human-only Stage2。旧 v7.14 specialist、
MoLingo、MotionLab 或 MoMask 的结果不能区分：

1. C3-25 Unified 三任务共享优化是否干扰 Human；
2. `1:1:1` task allocation 下 Human supervision dose 是否不足；
3. 当前 Stage2 Human branch 的单任务能力上限是否不足；
4. C3-25 Stage1 latent/owning decoder 是否限制 Human generatability。

本实验先回答前三项。它不是 promotion run，也不以 unrelated specialist 替代
Unified gate。

### 固定训练合同

- exact Stage1 owner：
  `v8_1c_center25pct_full636k_seed17_4090g0_20260719`；
- exact C3-25 train/eval cache、ordered IDs 与 immutable full-cov normalization；
- fresh Stage2 `0→105K`，seed17、batch512、START_X、cosine diffusion、
  AdamW/LR milestone 与 Parent 完全相同；
- `task_probs=[camera,human,joint,human_text]=[0,1,0,0]`；
- 保持 Parent 的原生 Direct-H view：
  `[H_t,C_t]+[0,e_H]`、task row 1、`obs_mask=(0,0)`、Human-only loss；
- `human_view_mode=mixed`、`task_routing=human_first`；
- 不加入 Camera context ablation、task-row覆盖、decoded auxiliary、SNR weighting、
  数据清洗或增广；
- Camera/joint output 因无训练目标而不评估、不排名。

Parent `105K` 的实际 exposure ledger 为：

- Direct-H assignments：`17,922,917` samples；
- joint assignments：`17,919,830` samples；
- batch size：`512`；
- joint `element_mean` 的 Human channel coefficient：`128/192=2/3`。

因此 Human-only run 必须保存以下 immutable snapshots：

| snapshot | Parent-matched 含义 | 推导 |
| ---: | --- | --- |
| `35,006` | Direct-H assignment dose | `round(17,922,917 / 512)` |
| `58,339` | Human element-weighted loss dose | `round((17,922,917 + 2/3 × 17,919,830) / 512)` |
| `70,005` | 全部 Human-target assignment dose | `round((17,922,917 + 17,919,830) / 512)` |
| `105,000` | Human-only per-model compute ceiling | 与 Parent 总 optimizer steps 相同 |

这些 milestone 是三种不同的 matching boundary，不得挑一个事后改称“完全公平”。
`35,006` 只匹配 Direct-H 样本，`58,339` 匹配当前 loss geometry，
`70,005` 忽略 joint Human view 与 task row 差异，`105K` 则增加了 Human dose。

### 评估与 gate

四个 snapshots 首先使用同一 first-512 ordered IDs、seed17、DDIM50、CFG1、
`eta=0`、eval/decode batch 与 C3-25 owning decoder，只评 Direct-H：

- primary：FDTMR、TMR、HCov；
- mandatory geometry：global/root-aligned MPJPE、root ADE/FDE、integrated yaw；
- mandatory stratification：valid length、net yaw、yaw total variation、
  turn reversal；
- no-reference Human physical fields若 evaluator 输入可用则同时报告，缺失时标
  unresolved。

只有某个 snapshot 同时形成 stable semantic/distribution signal 且 Human
global/root geometry不 broad regress，才对该 snapshot 做 pure4053 formal。

判定顺序固定为：

1. `35,006/58,339` 已 broad 优于 Parent：支持 strong shared-training interference；
2. 只在 `70,005/105K` 改善：优先解释为 Human dose/成熟度，不先声称负梯度冲突；
3. `105K` 仍无 broad 改善：三模式混训不是主要瓶颈，转向 Stage2 Human
   objective/backbone 与 Stage1 latent 条件数；
4. semantic/distribution 改善但 geometry 不改善：启动 P0-HDG-1 与
   Stage1 ceiling-transfer attribution，不直接加更多 Human steps；
5. Human-only 的任何优势都不自动晋升 Unified；只有随后 matched no-update
   parameter-block attribution 确认冲突，才讨论 Camera-only adapter 或局部
   gradient surgery。

训练中的 step、ETA、host/GPU 与 checkpoint 只进入 run manifest/log；本节不复制
运行状态，也不以中途 loss 修改预注册判定。

### N=512 screen 结果与裁决（2026-07-24）

四个 immutable snapshots 已按同一 ordered IDs、seed17、DDIM50、owning decoder
完成 Direct-H-only screen。数值与 hashes 只见
[[StoryMotion-valid-metric-ledger#5.5 C3-25 原生 Direct-H Human-only 学习曲线 N=512 screen]]。

1. 四个 exposure/compute boundary 的 FDTMR、TMR、HCov 均未超过 Parent；
   FDTMR 与 coverage 是 broad regression，不存在可送入 pure4,053 的 snapshot。
2. paired global/root trajectory 有改善，但 root-aligned pose 与 wrapped
   integrated-yaw 没有形成 Pareto win，不能覆盖 semantic/distribution collapse。
3. 结果命中预注册 gate 3：仅移除 Camera/joint assignments 并把 Human dose
   增加到完整 `105K`，仍不能修复原生 Direct-H。因此 Unified 三任务混训不是
   当前 Human 质量的首要瓶颈，Direct-H 样本剂量也不是充分解释。
4. 该结果不证明 Stage1 已是容量瓶颈，也不证明 Human 单任务的普遍能力上限；
   它只关闭当前 192D native view、当前 START_X objective/backbone 下的
   Human-only 方案。下一步先做 heading、near-zero identity、decoder/manifold
   no-update attribution，再授权一个单变量 Human objective/backbone short arm。
5. 不运行 Human-only pure4,053 formal，不评 Camera/joint，不晋升 specialist；
   Parent C3-105K 保持 Unified mainline。

## P0-HDG-1：高噪 heading attribution

用户在 Parent/H-axis 的固定 8-ID renders 上观察到 `t=799` heading 异常；结合
Stage1 yaw oracle，这是高优先级风险。Parent、C-JOINT、ALL-JOINT 与 Human-only
现在已有 N=512 full-DDIM integrated-yaw 诊断；C/ALL view tying 没有消除该问题，
Human-only 也没有形成 wrapped-yaw Pareto win。但这些值不是固定 `t=799`
teacher-forced attribution，且 full4,053 仍未运行，不能预先写成全臂机制结论。

Human199 dim-3 必须先按训练统计反归一化，再从 frame 0 `cumsum`；owning decoder
所得 yaw 同时旋转 root local-XY velocity 与 skeleton。Camera14 只用
`distance+Human-root` 的 temporal `[0]` 作为 Camera velocity trajectory 原点，因此
Human yaw drift 不会机械地逐帧平移 Camera center；其直接风险是相对姿态、投影与
framing，Camera center 回归仍需单独归因。历史 `[136:199]` local-XYZ oracle 对
official SMPL joints 几乎无效也不代表 local articulation 无误，必须增加真正驱动
body model 的 pose6d `[4:136]` oracle。

Phase A 的 primary 改为 Parent 与 Human-only `105K` 的 Direct-H；ALL-JOINT
只作已封存的 architecture negative control，并补 Parent/ALL-JOINT 的 joint-H。
使用 ordered `N=512`、相同 `z_0/ε/ID/seed`，跑
`t=[0,49,99,199,399,599,799,999]`。每个 sample 同时保留 raw GT、
`x_id=Dec(z_gt)` 与 `x_pred=Dec(pred_x0)`，分别报告：

1. wrapped yaw mean/final、unwrapped final drift、p50/p90/p95；
2. official length、GT net-yaw、yaw total variation、turn-reversal strata；
3. RA-MPJPE 与 per-frame root+heading-aligned MPJPE 的 paired delta/bootstrap CI；
4. `x_id→raw GT`、`x_pred→raw GT`、`x_pred→x_id`，不把 paired excess 当严格误差分解。

Phase B 先只在 `t=799` 扩展五臂：分别做 yaw `[3:4]`、root-height、root-XY、
root-all `[0:4]`、pose6d `[4:136]`、RIFKE XYZ `[136:199]`、nonroot
`[4:199]` oracle；invalid tail 比较 current q-noise、zero、independent noise、
deterministic shuffle，并把 fixed-75 U-Net leakage 与 true-length decoder boundary
分开。最后比较 sequence-rigid/framewise H+C SE(2) 共同校正和 Human-only heading
oracle；共同变换必须保持 H-C projection/framing，作为 sanity invariant。

只有 Phase A/B attribution 命中后才扩展五臂全 grid，并选择 heading anchor、
valid-length conditioning、joint SE(2) augmentation 或 representation
factorization；teacher-forced `t=799` 不替代最终 DDIM50，也不进入 formal metric
ranking。
