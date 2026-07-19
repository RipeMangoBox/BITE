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
updated: 2026-07-19T20:55:00+08:00
---

# StoryMotion Latent Generatability and Stage2 Diagnostic Ladder

> [!abstract] 先行裁决
> 不应无条件并行启动 v8.1A、v8.1B、v8.2 三条 `105K` Unified。v8.1A 的 G3 `30K` 已因 Direct-C 与 joint parallel Camera broad regression 停止。Stage1 C3-25 seed17 目前只剩 Human global slope blocker，是当前最有希望的 v8 Stage1 candidate；用户于 `2026-07-19` 明确授权它以独立 exact cache 单进程训练 Stage2 `0→105K`，在 immutable `30K` checkpoint 上并行完成 Direct-H、Direct-C 与 joint parallel full eval，训练不因 30K quality screen 自动停止。该授权是 exposure/generatability diagnostic override，不改写 Stage1 gate；pure4053 已参与候选选择，最终 promotion 仍需新的 sealed audit set。所有 v8 cache/run 均为 `diagnostic_only`，不得成为 promotion-bearing cache。

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
| v8.1C C3-25 / `v8_1c_c3_25_diag_unified3_105k_seed17_4090g0_20260719` | Stage1 selected candidate；Stage2 continuous `0→105K` diagnostic active | Stage1 只剩 global slope blocker；用户授权 exact parent/cache 的长预算 generatability diagnostic | promotion claim、用 v8.1A 30K artifact 代替 C3、30K quality-stop、cascade gate |
| v8.1C C5-B / two-seed matched short family | Stage1 short ladder 已闭合；不进入 full | C5-A 支持的 surrogate 在 seed17 有 signal，但 seed23 未通过同一两个 target | full/cache/Stage2、复用 short state、继续扩 dose、把 pure4053 当最终 promotion test |
| v8.1B / `v8_1b_residual_ae_yaw001_root003_seed17_4090g0_20260717` | D0 → D1/D2 与 Stage1 camera root-cause | residual/optimization 与 geometry loss纠缠，且 short-bin camera severe regression | `30K/105K` Unified；它只会混合已知 Stage1 camera failure 与 Stage2 效果 |
| v8.2 / `v8_2_human200_joint_ae_yaw001_root003_seed17_4090g1_20260717` | D0 → D1/D2 与 layout/stats/joint-opt root-cause | camera14 不变却出现各 bin center-translation regression，须先拆解 shared trade-off | `30K/105K` Unified；把 human200 改善误称为全系统收益 |
| v7.14 / v7.36 / v7.38 controls | D0–D4 control | v7.36 是 exact 30K parent，v7.38 L0 是 exact 105K mainline | 用 `105K` L0 直接淘汰一个 `30K` candidate |
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

### G4 — 105K continuation and formal comparison

本 gate 是条件规则，不是当前队列。若某个未来 candidate 通过 G3，必须从同一 `30K` checkpoint 和 optimizer/RNG state 续训至 `105K`，不得重启、换 best checkpoint 或改 cache，再以完整 active three-profile protocol 与 v7.38 L0 的 `105K` formal 比较。v8.1A 已在 G3 失败并写入 `stop_30k_broad_camera_regression`，因此它没有 G4、不得续训。即使未来 candidate 的 G4 表现良好，它仍是 non-promotion diagnostic：原始 Stage1 promotion gate 没有被重写，不能据此替换 v7.14/v7.38 或启动 v8.2333。

#### C3-25 seed17 用户授权的连续 `105K` 诊断

`v8_1c_c3_25_diag_unified3_105k_seed17_4090g0_20260719` 是上述默认 G3→G4 quality gate 的显式协议修订，而不是给 v8.1A 续命。预注册问题是：C3-25 的 Stage1 Pareto 改善能否转化为 Stage2 generatability，以及其 `30K→105K` 轨迹是否显示“训练成熟度不足”还是稳定的 Camera/Joint failure。

- exact parent 固定为 C3-25 seed17 fresh `636K` endpoint；不得继承 v8.1A cache、normalization、checkpoint 或结果。
- Unified implementation、human-first routing、seed `17`、batch `512`、task probabilities `1:1:1:0`、full-cov train-only normalization、DDIM50/CFG1/eta0 与 v8.1A matched diagnostic 保持一致。
- 单进程从 step `0` 连续到 `105K`；step `30001` 起 LR 从 `1e-4` 降至 `3e-5`。保存 `1K/5K/10K/30K/105K` immutable checkpoints，不在 `30K` 重启 optimizer。
- `step_30000.pt` 单独计算 SHA256 并以冻结 contract snapshot 做 pure4053 Direct-H、Direct-C、joint parallel full eval；cascade 不运行。主训练同时继续，30K quality 结论不自动杀死 `105K`。
- 唯一自动停止条件是 operational failure、non-finite state、contract/hash/identity/non-causal audit failure。无论 30K 或 105K 结果如何，该 run 都保持 `diagnostic_only=true`、`promotion_eligible=false`。

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

1. C3 的 `1.25%/2.5%` raw-gradient camera-center dose 都已在 fresh matched screen 中保住 v8.1A Human core 并改善 Camera translation；按预注册规则选择较小 `1.25%` dose。seed23 C3-25 已完成 full endpoint，证明低 dose signal 能扩展到完整预算，但仍以 Human global slope `27.594 mm/100f` 与 Camera rotation `0.776°` 未过原始 gate。seed17 selected endpoint 用于判断这一边界是否重现；任何 endpoint 过 gate 前都不能建 cache 或进入 Stage2。
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
| Stage1 camera C3 seed23 robustness full | `v8_1c_center25pct_full636k_seed23_5090g0_20260719` | completed `636K / 81.38M` and pure4053 owning-decoder audit; Human held and Camera translation improved, but global-slope/rotation gate failed | full robustness evidence only; no promotion cache or Stage2; 5090 path text `nvme` is legacy naming over a SATA SSD replica |
| Stage1 camera C3 selected full | `v8_1c_center25pct_full636k_seed17_4090g0_20260719` | completed fresh `636K / 81.38M` and pure4053 owning-decoder audit；Human/Camera Pareto holds，rotation=`0.705°` passes，only global slope=`26.302 mm/100f` misses the original gate | exact diagnostic-only Stage2 cache/run has since been authorized；the failed original Stage1 gate still forbids promotion |
| Stage2 C3 continuous diagnostic | `v8_1c_c3_25_diag_unified3_105k_seed17_4090g0_20260719` | exact parent/decoder/cache/train-only full-cov stats、non-causal contract 与 hash audit 均通过；单一进程 `0→105K` 已部署，30K/105K 各固化 checkpoint 并执行 active three-profile eval | user-authorized generatability/exposure diagnostic only；30K 不重启或 quality-stop 主训练，任何结果都不追溯改写 Stage1 gate |
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
5. 用户已授权 C3-25 seed17 的连续 Stage2 `105K` 非晋级诊断；4090 GPU0 专用于该长训，30K full eval 使用 immutable checkpoint 且不阻断主训练。
6. C5-B calibration、seed17 matched selection 与 seed23 confirmation 已全部闭合；预注册 gate fail，不扩展其他 dose/full。5090 GPU1 已按短测边界使用并释放；4090 GPU1 释放给 C3 30K full eval。
7. 除这条用户显式授权的 C3 diagnostic override 外，新的 Stage2 candidate 仍需等待 Stage1 gate；顺序固定为 Direct-C camera-sensitive objective → joint-condition fusion → inference。D6/H2C 与 cascade 不再参与 active priority；v8.1B/v8.2 不进入 `30K/105K` Unified。

新 run 的 mutable state 只写入 remote run contract/log/manifest；G2/G3 的结论更新本页的一行 decision，formal audited metrics 只进入 [[StoryMotion-valid-metric-ledger]]，当前状态只摘要到 [[current]]，最终事件只追加到 [[version_family]]。该路由由仓库根 `AGENTS.md` 约束。
