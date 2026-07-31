---
title: "StoryMotion++：三模式统一生成与分阶段 Human–Camera 关系引导"
status: archived_proposal
hypothesis: |
  将三种 human–camera 任务统一为结构化模态掩码条件生成，并在扩散早期强化全局构图关系、后期削弱冲突条件且保留分支细节，可在不牺牲单模态质量的前提下，同时实现 text-to-joint、human-to-camera、camera-to-human，以及不依赖文本的 zero-shot 关系编辑与迁移。
source_papers:
  - "[[analysis/SIGGRAPH_2026/ActCam_Zero_Shot_Joint_Camera_and_3D_Motion_Control_for_Video_Generation]]"
  - "[[analysis/ICLR_2026/Pulp_Motion_Framing_aware_multimodal_camera_and_human_motion_generation]]"
  - "[[analysis/CVPR_2026/Towards_Storytelling_Animations_Joint_Synthesis_of_Human_and_Camera_Motions]]"
  - "[[analysis/arxiv_2026/Auteur_Language-Driven_Cinematographic_Framing_for_Human-Centric_Video_Generation]]"
  - "[[analysis/SIGGRAPH_ASIA_2024/MaskedMimic_Unified_Physics_Based_Character_Control_Through_Masked_Motion_Inpainting]]"
  - "[[analysis/CVPR_2026/ProjFlow_Projection_Sampling_with_Flow_Matching_for_Zero_Shot_Exact_Spatial_Motion_Control]]"
  - "[[analysis/SIGGRAPH_ASIA_2024/Monkey_See_Monkey_Do_Harnessing_Self-attention_in_Motion_Diffusion_for_Zero-shot_Motion_Transfer]]"
  - "[[analysis/ICLR_2026/Time_to_Move_Training_Free_Motion_Controlled_Video_Generation_via_Dual_Clock_Denoising]]"
tags:
  - StoryMotion
  - StoryMotion++
  - human-camera
  - motion-generation
  - diffusion
  - zero-shot-editing
  - status/archived
created: 2026-07-13T21:40:00+0800
updated: 2026-07-18T15:20:00+08:00
archived_at: 2026-07-18T15:20:00+08:00
superseded_by:
  - "[[current]]"
---

# StoryMotion++：三模式统一生成与分阶段 Human–Camera 关系引导

> [!warning] Archived proposal
> 本页是 StoryMotion++ 的历史设计推演，不是当前实验队列。其 specialist、prompt attribution 与 phase-guidance 计划已经被后续 v7.42/v7.43 证据覆盖；当前主线和下一步只看 [[current]]。

> [!abstract] 直白结论
> ActCam 不能直接接到 StoryMotion 上：它依赖冻结视频生成器、RGB reference、depth 与 pose condition，而 StoryMotion 在 3D motion latent 中工作，没有等价的 depth/VACE 接口。但 ActCam 最有价值的机制可以迁移：**早期先确定全局 camera–human 几何关系，后期减少会过约束细节的条件**。对 StoryMotion 而言，这应升级为“结构化掩码统一三模式 + actor-relative camera state + phase-adaptive relational guidance + training-free constraint projection”。这条路线既能提升当前 StoryMotion，也足以形成 StoryMotion++ 的独立研究问题。

## 1. Research idea summary

### 1.1 当前已经解决与尚未解决的边界

Local Stage2 的灾难性 decoded collapse 已经完成闭环：修正后的 local joint AE latent 具有强烈通道相关性，逐通道 z-normalization 不能消除 off-diagonal covariance；blockwise full-covariance whitening 才把 latent 恢复到与扩散噪声更匹配的坐标系。v7.30 在 train seed `17/23/29` 的 official pure `4,053` 上分别得到 TMR `9.745/9.808/11.134`、HCov `30.8/31.6/35.2%`，三条都不再出现 v7.20 的 `TMR=0/HCov=0`。

v7.34 又把该修复推进到 prompt-global Unified-3：Balanced 与 joint-heavy `3:2:5` 的 text→joint pure `4,053` 均为有限指标，TMR 分别为 `10.852/10.864`、HCov 为 `29.6/30.2%`。因此“崩溃没有延续”已有跨 seed、跨任务配比证据，但不等于 StoryMotion 的质量目标全部完成：

- `3:2:5` 的 joint FDCLaTr/Out 为 `105.71/17.5%`，优于 Balanced 的 `134.17/26.6%`；joint-heavy sampling 对 joint 目标有效。
- camera completion 则由 Balanced 占优：FDCLaTr `91.36` 对 `118.38`、CLaTr `38.19` 对 `34.51`，说明不存在一个对三模式无条件最优的配比。
- observed-camera shuffle 会让两条 camera→human probe 的 TMR 从 `11.90/11.24` 降到 `0.29/0`，证明 human completion 不是空壳；human→camera 的依赖在 Balanced 上方向一致，在 `3:2:5` 上仍不稳定。
- 两条 v7.34 都开启了全局 CLIP task prompt，harness 默认仍为关闭；由于尚无同预算 prompt-off checkpoint，不能把收益单独归因于 task prompt。
- v7.33 camera14 separate AE/VAE 是另一条负结果：camera distribution 很强，但 HCov 仅 `12.7/20.4%`、Out 为 `71.6/72.0%`。这不等于 v7.34 Stage2 collapse 复发。

### 1.2 StoryMotion 与 StoryMotion++ 的分界

**当前 StoryMotion 主线**应先回答三个基础问题：

1. camera14 的 actor-relative/framing contract 是否优于 camera9，且比较是否同数据、同 seed、同更新次数；
2. 同一个 Stage2 checkpoint 是否能在三种任务上同时工作，而不是只在 joint-only 任务上工作；
3. human–camera 交互应随扩散时间怎样变化，能否替代当前“一直允许”或“一直阻断”的静态策略。

**StoryMotion++**再增加两项训练外能力：

1. 给定任意部分 human、camera 或 framing observation，进行 zero-shot completion/editing；
2. 在没有文本时，把一个样本的人体动作、镜头关系或构图风格迁移到另一个样本，同时保持硬约束与多样性。

建议的论文级表述是：

> **StoryMotion++: Unified Human–Camera Generation, Completion, and Zero-Shot Relational Editing**

核心不是再增加一种 tokenizer，而是把 human 与 camera 视为可观察、可生成、可编辑的两个关系分支，并让同一生成先验在不同任务和约束密度下复用。

## 2. Mechanism decomposition

### 2.1 三模式统一为 structured masked generation

当前代码中的三种核心任务已经可以写成统一掩码：

| 模式 | 已观察分支 | 生成分支 | 语义 |
| --- | --- | --- | --- |
| human→camera | human | camera | 根据人体运动与 camera 描述生成镜头 |
| camera→human | camera | human | 根据镜头轨迹与 human 描述生成人体 |
| text→joint | 无 motion observation | human + camera | 根据文本联合生成两者 |

第一步不是增加新网络，而是用同一个 denoiser、task embedding、`obs_x0/obs_mask` 和 loss mask 训练三种任务。进一步可把 branch-level mask 扩展到 temporal sparse mask，使完整条件、局部关键帧、片段补全与完全无条件生成成为同一接口。这与 [[analysis/SIGGRAPH_ASIA_2024/MaskedMimic_Unified_Physics_Based_Character_Control_Through_Masked_Motion_Inpainting]] 的启发一致：统一能力来自结构化缺失模式，而不是简单把多个任务名称放进一个模型。

公平比较必须使用以下预算口径：

- Unified checkpoint 训练总计 `3N` 次 task exposure，三种任务期望各 `N` 次；
- 三个 specialist checkpoint 各训练 `N` 次，总训练开销同样为 `3N`；
- 同时报告每个任务的实际采样数，不能只比较 epoch 或 wall-clock；
- Stage1 checkpoint、latent cache、train/test sample IDs、seed、sampler 与评测样本完全固定。

这样可同时回答“统一模型是否优于等总计算的三模型 ensemble”与“统一训练是否产生 negative transfer”。

StoryMotion Stage2 不是 causal LLM，因此 task prompt 不应复制为额外 token 序列。当前 `TemporalObsUNet` 已具备适合该架构的全局条件路径：先离线编码每个任务的简短 instruction，再投影到 denoiser width，与 timestep 和原始 camera/human 文本条件相加：

```text
e_task = CLIP(prompt_task)
c = MLP_time(t) + MLP_text(e_camera, e_human) + λ_task MLP_task(e_task)
(scale_l, shift_l) = Linear_l(c)
h_l = Norm(Conv_l(h_l)) * (1 + scale_l) + shift_l
```

同一个 `c` 被送到所有 down/mid/up residual blocks，因此 task instruction 是全局 FiLM 条件，而不是局部 token 或 Qwen 式 causal attention。若没有外部 prompt embedding，现有 `--v72-text-role-router` 会退化为 learned task-ID embedding；提供 `--task-instruction-embeddings` 后则使用 frozen semantic embedding + trainable projection，两条路径互斥，避免重复注入 task ID。

当前三条 StoryMotion instruction 经 normalized CLIP ViT-B/32 编码后的两两 cosine similarity 为 `0.9700–0.9767`，语义向量并不天然正交。可训练 MLP 能放大其差异，但不能预设 semantic prompt 一定优于 learned task ID；正式结论需要同预算 prompt-vs-ID 消融，并用 task-shuffle/zero counterfactual 验证模型确实使用该全局条件。

### 2.2 camera9 与 camera14 的角色

camera9 是绝对 translation `3D` + rotation `6D`。它不包含 FOV，也不显式包含 velocity，更不是 actor-relative representation。PulpMotion camera14 是：

| 分量 | 维度 | 实际处理 |
| --- | ---: | --- |
| FOV | 2 | 原始弧度；没有逐维数据集 z-score |
| human-relative distance | 3 | 使用训练集 mean/std 做 z-score |
| rotation 6D | 6 | 来自旋转矩阵，具有几何尺度约束；没有训练集 mean/std z-score |
| translation velocity | 3 | 使用训练集 mean/std 做 z-score |

因此，“只有 distance 和 rotation 做 norm”并不准确：**affine z-score 的是 distance 和 velocity；rotation 是几何规范化表示；FOV 保持原始弧度。** Human199 则按通道使用官方 mean/std 做 z-score。

已对 2,048 条 train clips、242,128 帧做确定性抽样：FOV 两维的跨序列标准差约为 `0.139` 与 `0.229` rad，序列间变化显著；camera9 完全无法表达这种内参变化。故：

- camera9 可以保留为 fixed-intrinsics/extrinsics ablation；
- camera14 才能作为 PulpMotion 与 StoryMotion 主线的公平表示；
- camera9 与 camera14 的最终指标不能直接宣称方法优劣，必须同时给出各自 contract；
- 对 camera9，FOV reconstruction 应标记为 `N/A`，不能用隐式默认 FOV 后的投影分数冒充同任务结果。

当前 Stage1 train manifest 含 `162,760` 个唯一 clip，即约 **16.3 万**，不是 `1.6 万`。batch size `128` 时每 epoch 为 `1,272` steps，500 epochs 为 `636,000` optimizer updates 和 `81,380,000` sample exposures。camera9 与 camera14 对照必须固定这些量。

### 2.3 data z-normalization、diagonal normalization 与 covariance whitening

三者的数学关系可以统一理解为“选择扩散或表示学习工作的坐标系”：

1. **Data/feature z-normalization**：在 Stage1 输入空间按特征维度做 `(x-μ)/σ`，主要解决不同物理量量纲差异。
2. **Latent diagonal normalization**：在 Stage2 latent 空间按通道做 `(z-μ_z)/σ_z`，令每个通道边际方差接近 1。
3. **Full-covariance whitening**：使用 `Σ^{-1/2}(z-μ_z)`，同时消除通道间线性相关，使整体 covariance 接近单位阵。

Diagonal normalization **不是任何时候都错误**。若 latent covariance 接近对角、条件数良好，或 denoiser 已能稳定吸收相关性，它是简单且可靠的默认方法。它在本次 local joint AE 上失败，是因为强 off-diagonal correlation 仍被保留，而扩散过程继续注入各向同性噪声，导致信号与噪声几何严重不匹配。

Full-covariance 也不是无条件更优：样本不足、高维 covariance 估计不稳时可能放大小特征值方向的噪声。因此当前合理实现是 human/camera blockwise whitening，并加入 shrinkage/ridge；不能把所有维度未经正则化地一次性求逆。

PulpMotion 与 StoryMotion 的历史边界需要明确：

- **PulpMotion Stage1** 使用上述 human199/camera14 feature contract，autoencoder 配置没有额外的 latent normalization 层。
- **PulpMotion Stage2** 将 Stage1 latent 直接送入 diffusion/DiT；目前代码证据中没有 StoryMotion 式逐通道 latent z-normalization，也没有 full-covariance whitening。代码里的 `z_scale` 是时间下采样比例，不是 latent 数值缩放。
- **StoryMotion Stage1** 历史 camera9 是 raw absolute camera；后续 local camera14 支持 raw/official-normalized 等多个 contract。
- **StoryMotion Stage2** 历史版本引入了逐通道 latent z-normalization；本次 local joint AE collapse 正是该方法不足以处理相关 latent，而不是“所有 diagonal normalization 都错”。

### 2.4 从 ActCam 迁移 two-phase condition guidance

[[analysis/SIGGRAPH_2026/ActCam_Zero_Shot_Joint_Camera_and_3D_Motion_Control_for_Video_Generation]] 的关键不是 depth 本身，而是条件在时间上的职责分工：

- 高噪声早期使用 depth+pose，先锁定 global geometry、camera motion 与人物布局；
- 低噪声后期只保留 pose，避免 depth 持续过约束背景和高频动作；
- `N_D=0` 时 camera 与 human motion 容易歧义，`N_D=1` 时背景趋于静态，约 `20%` 的早期强几何条件取得较好折中。

StoryMotion 没有 depth，但存在三个可替代的关系条件：actor-relative camera14、framing/projection constraint，以及 human/camera 的 observed branch。对应的 phase-adaptive 机制可以定义为：

```text
高噪声阶段：joint relational view
  human ↔ camera + actor-relative framing
  目标：先确定谁相对谁移动、人物处于画面何处、镜头全局趋势

低噪声阶段：asymmetric/detail view
  human detail branch: 降低无必要的 camera→human 泄漏
  camera branch: 保留 human→camera 与 framing guidance
  目标：恢复人体动态细节，同时继续满足构图
```

这比当前固定 `c_to_h_blocked` 更一般：joint task 可以早期允许关系协商、后期阻断有害泄漏；camera→human task 因 camera 本来就是 observation，则始终保留该条件，不受 joint-only 阻断策略误伤。

### 2.5 Training-free editing and transfer

StoryMotion++ 可把已训练的三模式 prior 变成编辑器，而不是重新为每种控制训练模型：

- **Exact branch projection**：每个去噪/流步骤先预测 clean endpoint，再把已知 human/camera 帧投影回约束集合。[[analysis/CVPR_2026/ProjFlow_Projection_Sampling_with_Flow_Matching_for_Zero_Shot_Exact_Spatial_Motion_Control]] 说明，投影必须使用与运动学一致的 metric；直接欧氏投影可能满足约束却严重破坏生成质量。
- **Reference transfer**：通过 inversion 获得源样本轨迹，在中间层选择性共享或替换 human/camera relation feature。[[analysis/SIGGRAPH_ASIA_2024/Monkey_See_Monkey_Do_Harnessing_Self-attention_in_Motion_Diffusion_for_Zero-shot_Motion_Transfer]] 表明冻结 motion diffusion 的 attention feature 可承载 zero-shot motion transfer，但 StoryMotion 需要先验证 U-Net/DiT 中是否存在可分离的 relation carrier，不能直接假定 Q/K/V 对应关系成立。
- **Dual-clock refinement**：对已满足约束的分支少更新，对冲突或弱响应区域多更新。[[analysis/ICLR_2026/Time_to_Move_Training_Free_Motion_Controlled_Video_Generation_via_Dual_Clock_Denoising]] 提供了 training-free 非均匀 denoising 的先例。
- **No-text mode**：用 null text、source motion branch 与 structured mask 作为唯一条件。该能力目前尚未验证；训练时至少需要 text dropout/null-condition exposure，或在推理时使用可靠 inversion，不能仅把 text tensor 置零后直接宣称 zero-shot。

## 3. Related evidence from the local knowledge base

### 3.1 ActCam：阶段化条件用于解决 camera–human 歧义

[[analysis/SIGGRAPH_2026/ActCam_Zero_Shot_Joint_Camera_and_3D_Motion_Control_for_Video_Generation]] 在冻结生成器上以 camera-aligned depth+pose 处理全局几何，再切换到 pose-only 恢复细节。其最直接启发是：human 与 camera 的耦合并非常数，应随噪声阶段变化。局限是其性能依赖 depth、pose 与 VACE 双条件能力，不能作为 StoryMotion latent 模型的直接 plug-in。

### 3.2 PulpMotion：framing 是关系约束，不只是 camera reconstruction

[[analysis/ICLR_2026/Pulp_Motion_Framing_aware_multimodal_camera_and_human_motion_generation]] 的 auxiliary sampling 把镜头引导投影到 framing 子空间，mixed DiT 的 out-rate 从 `25.98` 降到 `16.76`、framing distance 从 `4.90` 降到 `3.37`。这支持 StoryMotion 在 sampling 期增加关系引导，但过大的 guidance weight 会损伤质量，因此应与 phase schedule 联合消融。

### 3.3 actor-relative representation：降低绝对坐标学习负担

[[analysis/arxiv_2026/Auteur_Language-Driven_Cinematographic_Framing_for_Human-Centric_Video_Generation]] 使用 actor-relative 语义 camera axes；[[analysis/CVPR_2026/Towards_Storytelling_Animations_Joint_Synthesis_of_Human_and_Camera_Motions]] 使用 Toric/pairwise interaction 建模人物与镜头。这两条证据共同表明，camera 应首先表示“相对人物如何构图”，再表示世界坐标中的绝对轨迹。camera14 是必要的近期修复，但仍可进一步加入可解释的 framing relation state。

### 3.4 structured masks：三模式统一的最小机制

[[analysis/SIGGRAPH_ASIA_2024/MaskedMimic_Unified_Physics_Based_Character_Control_Through_Masked_Motion_Inpainting]] 把多种控制任务统一为 masked motion inpainting。这比单纯 task token 更适合 StoryMotion：task token 说明意图，mask 精确说明哪些 branch/frame 已知、哪些必须生成。两者结合才能支持训练分布外的稀疏编辑。

### 3.5 projection 与 feature reuse：通向 zero-shot editing

[[analysis/CVPR_2026/ProjFlow_Projection_Sampling_with_Flow_Matching_for_Zero_Shot_Exact_Spatial_Motion_Control]]、[[analysis/SIGGRAPH_ASIA_2024/Monkey_See_Monkey_Do_Harnessing_Self-attention_in_Motion_Diffusion_for_Zero-shot_Motion_Transfer]] 与 [[analysis/ICLR_2026/Time_to_Move_Training_Free_Motion_Controlled_Video_Generation_via_Dual_Clock_Denoising]] 分别提供 hard projection、attention reuse 与非均匀去噪三个互补算子。StoryMotion++ 可先实现最稳健的 branch projection，再决定是否值得做 attention transfer；不应一开始同时修改训练、网络与 sampler。

### 3.6 ArtLLM：任务比例与 prompt routing 的可迁移边界

[[paperPDFs/CVPR_2026/ArtLLM_Generating_Articulated_Assets_via_3D_LLM.pdf|ArtLLM]] 把 articulation SFT 分成三项：Task 1 仅从点云预测 part boxes；Task 2 在点云和 GT part layout 条件下预测 joints；Task 3 从点云端到端预测 boxes 与 joints。Stage 1 只训练 Task 1，Stage 2 联合三项；补充材料明确给出 Stage 2 数据混合比 `3:2:5`，对应的简短 prompts 分别是 `Detect part boxes.`、`Given part boxes, detect joints.`、`Detect part boxes and joints.`。

论文训练样例使用 ShareGPT human message：先放 `<point_cloud>`，再放 task prompt 与输出 schema；补充材料说明训练时 point-cloud placeholder 会替换成 point encoder 产生的 tokens。结合其 Qwen3-0.6B autoregressive backbone，可合理推断 task 文本、schema、GT layout（Task 2）与 point tokens 位于同一 causal context，输出 token 通过 self-attention 使用这些前缀条件。但论文没有显式给出 `Z_chat/Z_pc/Z_task/Z_schema` 的拼接公式，因此该公式应标为架构解释，而不是原文公式。

可迁移到 StoryMotion 的是“显式任务说明 + ratio sensitivity”，不是 token 拼接本身。ArtLLM 的 layout/kinematic/end-to-end 难度结构与 StoryMotion 的 human→camera、camera→human、text→joint 不同，所以 `3:2:5` 只能作为 joint-heavy 配比消融，balanced `[1,1,1,0]` 仍是 Unified-3 的主注册设置。

## 4. Candidate experiments

### 4.1 P0：camera9 vs camera14 Stage1 公平对照

目的：回答 FOV/velocity/actor-relative distance 是否改善 Stage1 reconstruction 与后续 Stage2 条件质量。

固定项：

- 同一 `162,760` train clips 与 `4,053` pure-test clips；
- seed `17`、batch `128`、500 epochs、`636,000` optimizer updates；
- non-causal、human/camera latent `128/64`、hidden `256`、downsample `4`；
- AE 对 AE、VAE 对 VAE，checkpoint update 数完全一致；
- 相同 Stage2 cache/eval 协议，硬件差异只影响 wall-clock，不影响 exposure budget。

变量：

- camera9：absolute translation3 + rotation6D6；
- camera14：FOV2 + relative distance3 + rotation6D6 + velocity3。

Stage1 指标除整体 MSE 外，必须按 FOV、distance、rotation、velocity 分块报告，并增加 decoded projection/outscreen。camera9 的 FOV 项标为 `N/A`。若 camera14 只改善 FOV reconstruction、却不改善 joint Stage2，则说明 Stage2 没有有效使用内参，不能归咎于 Stage1。

完成状态（2026-07-14）：camera9 与 camera14 的 separate AE/VAE 均完成 `636,000` updates、strict postflight、official pure `4,053` eval。四条结果均使用 last checkpoint、seed17 和同一 pure IDs；camera9 缺少 FOV 与 actor-relative 字段，因此这里只比较 decoded official aggregate，不能把差异归因到某一个新增字段。

| version / run | feature contract / tokenizer | FDTMR↓ | TMR↑ | HCov↑ | FDCLaTr↓ | CLaTr↑ | CCov↑ | F1↑ | Out↓ |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| v7.32 / `v7_32_separate_local_ae_500ep_seed17_5090_20260713` | camera9 separate AE | 268.92 | 12.503 | 67.3% | 22.81 | 61.035 | 83.6% | 0.931 | 14.5% |
| v7.32 / `v7_32_separate_local_vae_500ep_seed17_5090_20260713` | camera9 separate VAE | 208.39 | 14.673 | 79.7% | 15.01 | 63.650 | 89.6% | 0.927 | 13.4% |
| v7.33 / `v7_33_separate_official14_ae_500ep_seed17_4090_20260713` | camera14 separate AE | 788.72 | 7.287 | 12.7% | **0.56** | **70.116** | **99.8%** | 0.938 | 71.6% |
| v7.33 / `v7_33_separate_official14_vae_500ep_seed17_4090_20260713` | camera14 separate VAE | 671.98 | 6.944 | 20.4% | 0.67 | 69.998 | 99.8% | **0.939** | 72.0% |

camera14 的 camera distribution reconstruction 明显增强，但 human distribution 与 joint projection 同时恶化；因此本轮 P0 不支持把 camera14 separate tokenizer 提升为 Stage1 主线。这个结果也说明 FDCLaTr/CCov 单独很好不能代表 human–camera 关系健康，必须与 HCov 和 Out 一起看。camera14 的 8-sample GT/AE/VAE 三视图与统一 Gradio audit 作为定性核查补齐，操作入口见 [[StoryMotion_Gradio_Render]]。

证据路径：

- camera9 AE/VAE：`runs/stage1/v7_32_separate_local_{ae,vae}_500ep_seed17_5090_20260713/eval/official_pure4053_last.json`
- camera14 AE/VAE：`runs/stage1/v7_33_separate_official14_{ae,vae}_500ep_seed17_4090_20260713/eval/official_pure4053_last.json`
- camera14 vis：`runs/stage1/v7_33_separate_official14_ae_500ep_seed17_4090_20260713/vis/pure8_camera14_last_ae_vae/summary.json`

### 4.2 P0：三模式统一 checkpoint vs 等总预算 specialists

最小实验矩阵：

| 组别 | task sampling | 总 task exposures | 用途 |
| --- | --- | ---: | --- |
| Joint-only control | `[0,0,1,0]` | `N` | 复现当前 v7.30，不作为三模式模型 |
| Unified-3 prompt-balanced | `[1,1,1,0]` | `3N` | 主注册设置；每种任务期望 `N` 次 |
| Unified-3 prompt-3:2:5 | `[3,2,5,0]` | `3N` | ArtLLM-inspired ratio sensitivity；不得作为直接任务映射 |
| Specialist ensemble | 三个独立 one-hot | `3N` | 每模型 `N` 次，总计算匹配 Unified-3 |
| Unified-3 + structured temporal masks | balanced + mask curriculum | `3N` | 测试 sparse completion 泛化 |

完成状态（2026-07-14）：两条 run 均完成 `30,000` updates、batch `512`、seed17、width416、同一 corrected camera14 cache、blockwise full-covariance stats 和 strict pre/postflight。两项均使用 normalized CLIP ViT-B/32 task prompt，经 trainable MLP 加到全局 denoiser condition；CLI 未提供 embedding path 时默认关闭。

| run | camera exposures | human exposures | joint exposures | total exposures | final eval loss |
| --- | ---: | ---: | ---: | ---: | ---: |
| Balanced `1:1:1` | 5,120,574 | 5,121,250 | 5,118,176 | 15,360,000 | 0.2864 |
| ArtLLM-inspired `3:2:5` | 4,611,015 | 3,072,088 | 7,676,897 | 15,360,000 | 0.2732 |

Official pure `4,053`、last checkpoint、DDIM50、`eta=0`、CFG1 的 generated-target 指标如下。completion 行只报告生成分支；另一分支是 observed GT。

| run | task | target | FDTMR↓ | TMR↑ | HCov↑ | FDCLaTr↓ | CLaTr↑ | CCov↑ | F1↑ | Out↓ |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Balanced | joint | human + camera | 439.79 | 10.852 | 29.6% | 134.17 | 28.762 | 42.8% | 0.273 | 26.6% |
| `3:2:5` | joint | human + camera | **423.56** | **10.864** | **30.2%** | **105.71** | **34.568** | **51.3%** | **0.422** | **17.5%** |
| Balanced | camera | camera | — | — | — | **91.36** | **38.190** | **57.9%** | **0.452** | — |
| `3:2:5` | camera | camera | — | — | — | 118.38 | 34.505 | 56.1% | 0.431 | — |
| Balanced | human | human | **279.99** | **10.682** | **58.7%** | — | — | — | — | — |
| `3:2:5` | human | human | 313.53 | 9.639 | 52.9% | — | — | — | — | — |

配比形成明确 Pareto：`3:2:5` 改善 joint，Balanced 改善 camera 与 human completion。不能只看较低的 aggregate eval loss，也不能把 `3:2:5` 写成三模式统一的无条件 winner。

Observed-branch pure-256 shuffle probes 进一步给出依赖性边界：

| run | generated target | clean observed condition | shuffled observed condition | 判定 |
| --- | --- | --- | --- | --- |
| Balanced | human | TMR `11.90` / HCov `72.9%` / FDTMR `400.36` | `0.29` / `61.7%` / `473.40` | 强 camera→human dependence |
| `3:2:5` | human | TMR `11.24` / HCov `70.2%` / FDTMR `412.67` | `0` / `55.9%` / `489.12` | 强 camera→human dependence |
| Balanced | camera | CLaTr `38.17` / CCov `79.8%` / FDCLaTr `115.67` | `37.85` / `71.9%` / `123.81` | 弱但方向一致的 human→camera dependence |
| `3:2:5` | camera | CLaTr `34.61` / CCov `78.9%` / FDCLaTr `135.50` | `36.80` / `74.5%` / `131.38` | 指标方向混合；依赖性未稳健通过 |

两条 run 都完成 bridge-smoke、三模式 full eval 与 8-sample single-asset render。global task prompt 的直接贡献仍需同预算 prompt-off 或 prompt intervention 对照；当前 probe 验证的是 observed motion condition，不是 prompt 因果效应。

每个模式分别报告 semantic quality、human/camera distribution、condition adherence、diversity 和 outscreen；再报告三模式宏平均，禁止只用 joint 指标掩盖 completion task 的失败。

决策门：

- Unified-3 任一模式相对对应 specialist 退化超过预注册容忍度，则先处理 negative transfer，不进入 StoryMotion++；
- Unified-3 三模式均有效且总预算不劣于 ensemble，才可以宣称 unified generation；
- 未见过的 temporal sparse masks 若显著失败，则下一步是 mask curriculum，而不是增加网络深度。

### 4.3 P1：phase-adaptive relational guidance

固定同一 Unified-3 checkpoint，仅改变 inference schedule，避免把训练收益与 sampler 收益混在一起。

建议网格：

- early relational/framing fraction `ρ ∈ {0, 0.1, 0.2, 0.4, 1.0}`；
- joint C→H policy：`always allow`、`early allow → late block`、`always block`；
- framing guidance weight 使用 PulpMotion 合理范围的小网格，并固定 DDIM steps/seed；
- camera→human task 始终保留 observed-camera condition，schedule 只调 relation guidance 强度。

主要判据：

- 早期允许、后期阻断是否同时提高 joint framing 与 human TMR/HCov；
- `ρ=1` 是否出现 ActCam 类过约束，即动作细节下降或 camera 背景趋静；
- `ρ=0` 是否出现 camera/human 归因歧义；
- `ρ≈0.2` 的优势是否跨 seed、sampler steps 与 camera contract 稳定，而不是直接照搬 ActCam 的数值。

### 4.4 P1：counterfactual coupling gate

对三种模式分别构造 zero/shuffle/noise-matched counterfactual：

- text→joint：替换 camera latent 不应无边界改变 human branch，但应允许合理的构图协商；
- human→camera：替换 human observation 必须显著改变 camera，否则模型没有使用条件；
- camera→human：替换 camera observation 必须显著改变 human，否则该模式名存实亡；
- text shuffle：应主要影响与对应语义相关的分支，记录 branch-specific delta。

v7.34 observed-branch shuffle 已证明两条 camera→human 路径具有强依赖，并只让 Balanced 的 human→camera 路径方向一致通过；`3:2:5` 的 human→camera 仍需修复。text/task-prompt shuffle 尚未执行，不能由 observed-latent probe 代替。

### 4.5 P2：zero-shot relational editing

按风险从低到高执行：

1. 已知完整 human、生成 camera；已知完整 camera、生成 human，逐步 hard replace observation branch；
2. 只给稀疏关键帧或片段，使用 clean-endpoint projection；
3. null-text 条件下，把 source human motion 与 target camera/framing 组合；
4. 做 inversion + relation feature transfer，比较 attention replacement 的层与时间窗口；
5. 最后才加入 actor-relative cinematic DSL 或多角色 Toric extension。

基础对照必须包含：普通 masked sampling、每步欧氏 hard replacement、kinematics-aware projection、phase-adaptive projection。若 exact constraint error 降为零但 FTD/TMR 显著变差，应判定 projection metric 错误，而不是成功。

## 5. Risks, decision gates, and next steps

### 5.1 最高优先级排序

本节是讨论后的排程，**尚未启动新增训练**。

| 优先级 | 实验 | 训练数 | 最小公平预算 | 晋级条件 |
| ---: | --- | ---: | --- | --- |
| P0-a | v7.33 normalized-human heading/decode audit；v7.34 camera projection render 已完成 | 0 | 复用现有 checkpoint；8-sample 与 pure-256 | 区分 contract/loss 问题、真实生成问题与展示缺失 |
| P0-b | frozen-checkpoint phase/framing guidance | 0 | Balanced 与 `3:2:5`、同 pure-256、同 seed/steps | generated-target 指标与 Out 同时改善，不接受只把轨迹拉近 GT |
| P0-c | prompt-off / task-ID-only Unified-3 | 2 | Balanced 与 `3:2:5` 各 `30k`，完全匹配 v7.34 | 分离 global CLIP prompt 的因果贡献 |
| P0-d | one-hot specialists | 3 | camera/human/joint 三条；使用 snapshots 同时匹配两种 ratio | 给出 compute-normalized unified-vs-specialist gap |
| P1 | projection-relation auxiliary | 1 candidate | 只在 P0-b 有正向信号后做一条 Balanced `30k` | 修复 human→camera 与 joint framing，不牺牲 human completion |
| P2 | task-specific FiLM/adapter 或 gradient balancing | 待定 | 只有 specialists 显著优于 Unified-3 才进入 | 处理已被证实的 negative transfer |

三组 specialist 足够，不需要为两种 ratio 各训练三组：camera specialist 保存 `9k/10k`，human 保存 `6k/10k`，joint 保存 `10k/15k`。Balanced 对比使用三个 `10k` snapshots，总暴露为 `3N`；`3:2:5` 对比使用 `9k/6k/15k` snapshots，总暴露同样为 `3N`。因此是 **3 次训练、6 个评测 checkpoint**，不是 6 次训练。

camera projection 已在这些 control 之前补齐：camera completion 的 world skeleton 本来就是 observed GT human，无法显示生成 camera 的好坏；joint 的动作也不应按逐帧 GT 重建误判。当前 Gradio qualitative gate 同时展示世界骨架、GT/generated camera projection 和轨迹诊断 PNG。

camera14 separate 对照与 Unified-3 screening 已关闭；继续只在 joint-only 上细调、盲目加长 `3:2:5`，或立即照搬 ActCam 的 depth 条件，都不会回答当前最关键的 prompt attribution 与 camera condition dependence。

### 5.2 主要风险

- **Full-covariance 统计泄漏或不稳定**：stats 只能来自 train cache；使用 blockwise shrinkage/ridge，并记录 sha256。
- **camera14 改善来自更多维度而非更好关系表示**：报告 parameter count，并增加 camera14 去 FOV/去 velocity 消融。
- **三模式 negative transfer**：task exposure、loss scale 和 branch frequency 不平衡会让宏平均掩盖单模式退化。
- **分阶段 guidance 过拟合 sampler**：必须跨 DDIM step 数、seed 与 noise schedule 复测。
- **No-text 声明过早**：null text 不是自动具备 zero-shot editing；必须测 condition adherence 与 inversion error。
- **硬投影破坏运动流形**：exact constraint satisfaction 与生成质量必须同时过 gate。
- **actor-relative 表示丢失世界轨迹信息**：保留可逆的 world transform 或双表示，不把 cinematic relation 当作完整 camera state。

### 5.3 Promotion gates

StoryMotion 主线进入 StoryMotion++ 前应同时满足：

- camera14 AE/VAE checkpoint 通过 dataset、feature contract、causal flag、dims 与 tokenizer fail-closed harness；
- one-step、DDIM1 与 DDIM5–50 全路径 finite，且 collapse reversal 在至少三个 seed 上成立；
- Unified-3 的三个模式均有非退化 condition dependence，宏平均不以牺牲某一模式换取；
- phase schedule 相对静态 blocking 在 human quality 与 framing/camera quality 上形成稳定 Pareto 改善；
- zero-shot completion 至少在一种 sparse mask setting 下同时满足约束误差与分布质量 gate。

camera14 separate 已因 human/projection 退化停止 promotion，当前 Stage2 继续使用 v7.14 corrected joint AE。Unified-3 已证明单 checkpoint 三模式均可生成，但 ratio Pareto 与 human→camera 依赖缺口仍在；若 prompt-off/specialist 公平对照确认 negative transfer，再考虑 shared backbone + task-specific lightweight heads，而不是立刻扩大模型。

## 6. StoryMotion++：独立方法章节

> [!tip] 一句话定位
> StoryMotion++ 不是 StoryMotion 增加更多 condition 的版本，而是把 human 与 camera 统一为可观察、可生成、可补全、可迁移的关系变量，并用同一生成先验支持三模式生成和不依赖文本的 zero-shot relational editing。

### 6.1 研究问题与范围

StoryMotion++ 试图回答三个比“联合生成一对 human-camera motion”更强的问题：

1. **统一性**：同一个 checkpoint 能否在 human→camera、camera→human、text→joint 三种模式间切换，而不依赖独立模型？
2. **关系可控性**：模型能否区分必要条件依赖与有害跨分支泄漏，并让耦合强度随扩散阶段变化？
3. **迁移性**：在不重新训练、甚至不给文本时，能否把 source motion、target camera 或 framing relation 重新组合？

当前范围只处理单人、单镜头、短时 3D motion。多角色、长序列、RGB video rendering 和 cinematic language DSL 是后续扩展，不应混入第一版主张。

### 6.2 方法总览

建议把方法组织为四个相互独立、可逐项消融的模块：

#### A. Unified Modality-Masked Prior

- 使用统一 `obs_x0/obs_mask/target_mask` 表达三种任务，而不是为任务各建一条网络。
- Branch mask 表示整条 human/camera 是否可见；temporal mask 表示关键帧、片段或稀疏 observation。
- Task embedding 说明生成意图，mask 说明实际可见信息；两者不可互相替代。
- 训练时记录每种 mask/task 的实际 exposure，避免“名义 balanced、实际不平衡”。

这一模块主要承接 [[analysis/SIGGRAPH_ASIA_2024/MaskedMimic_Unified_Physics_Based_Character_Control_Through_Masked_Motion_Inpainting]] 的 structured masked generation 思路，但目标从物理角色控制扩展到 human-camera relational prior。

#### B. Actor-Relative Relational State

- Camera 主状态使用 official camera14：FOV、human-relative distance、rotation6D 与 velocity。
- 保留可逆 world transform 或 world-space residual，避免 actor-relative 表示丢失全局轨迹。
- 从 human 与 camera 解码结果构造 framing state，例如 screen-space actor center、scale、visibility 与 outscreen margin。
- Framing state 首先作为 inference guidance/metric；只有证明有效后才考虑加入训练条件。

该模块结合 [[analysis/ICLR_2026/Pulp_Motion_Framing_aware_multimodal_camera_and_human_motion_generation]] 的 framing subspace、[[analysis/arxiv_2026/Auteur_Language-Driven_Cinematographic_Framing_for_Human-Centric_Video_Generation]] 的 actor-relative camera control，以及 [[analysis/CVPR_2026/Towards_Storytelling_Animations_Joint_Synthesis_of_Human_and_Camera_Motions]] 的 pairwise/Toric 关系建模。

#### C. Phase-Adaptive Relational Guidance

定义随归一化去噪进度 `s∈[0,1]` 变化的关系门控 `g(s)`：

```text
early / high noise:
  g(s) high
  human ↔ camera + framing
  establish global motion attribution and composition

late / low noise:
  reduce unnecessary camera → human interaction in joint generation
  retain human → camera and framing guidance
  recover human detail without losing composition
```

最小版本不新增网络参数，只在 sampling forward 中调度现有 coupling view。`c_to_h_blocked` 是 `g(s)=0` 的静态端点；StoryMotion++ 要验证的是 `early allow → late block` 是否形成更好的 Pareto 前沿。

这一设计迁移自 [[analysis/SIGGRAPH_2026/ActCam_Zero_Shot_Joint_Camera_and_3D_Motion_Control_for_Video_Generation]] 的 two-phase condition guidance，但不照搬 depth/VACE 条件，也不预设 ActCam 的 `20%` 切换点可直接泛化到 motion latent。

#### D. Zero-Shot Relational Operators

- **Branch completion**：每步恢复已观察 human/camera branch，只生成缺失分支。
- **Sparse completion**：只固定关键帧或片段，在 clean endpoint 上投影回约束集合。
- **Relation transfer**：source 提供 human motion，target 提供 camera/framing；text 可置空。
- **Style transfer**：通过 inversion 和选择性中间特征复用迁移 camera rhythm 或 human motion pattern。

第一版优先实现 kinematics-aware projection。只有 projection 同时满足 exact constraint 与生成质量 gate 后，才进入 attention feature transfer。依据分别来自 [[analysis/CVPR_2026/ProjFlow_Projection_Sampling_with_Flow_Matching_for_Zero_Shot_Exact_Spatial_Motion_Control]]、[[analysis/SIGGRAPH_ASIA_2024/Monkey_See_Monkey_Do_Harnessing_Self-attention_in_Motion_Diffusion_for_Zero-shot_Motion_Transfer]] 与 [[analysis/ICLR_2026/Time_to_Move_Training_Free_Motion_Controlled_Video_Generation_via_Dual_Clock_Denoising]]。

### 6.3 训练与推理流程

```text
camera14 Stage1 tokenizer
  ↓ fixed, contract-checked latent cache
Unified-3 Stage2 prior
  ├─ human observation → camera
  ├─ camera observation → human
  └─ no motion observation → joint human + camera
  ↓
phase-adaptive relational sampler
  ↓ optional
clean-endpoint projection / inversion / relation transfer
```

训练阶段只要求完成 Unified-3 与 structured masks；phase schedule 和 zero-shot operators 应先作为冻结 checkpoint 上的 inference-only 实验。这样能区分“prior 学到了什么”与“sampler 强制了什么”。

### 6.4 可主张贡献与明确非主张

若实验通过，StoryMotion++ 可以主张：

1. 单 checkpoint 的三模式 human-camera generation/completion；
2. 随扩散阶段变化的非对称关系引导，兼顾构图和人体细节；
3. 不重新训练的 sparse completion 与 no-text relational transfer。

第一版不能提前主张：

- 任意视频生成器上的 zero-shot camera control；
- 未见角色、超长序列或多角色的一般化；
- 仅凭 null text 推理就实现语义无损迁移；
- exact constraint error 为零等价于自然运动质量更好。

### 6.5 核心实验矩阵

| 研究问题 | 主实验 | 必要对照 | 通过条件 |
| --- | --- | --- | --- |
| 三模式能否统一 | Unified-3 vs three specialists | joint-only、equal-total-exposure ensemble | 三模式均非退化，宏平均不掩盖单模式失败 |
| camera14 是否必要 | camera9 vs camera14 matched Stage1/2 | camera14 去 FOV、去 velocity | framing/projection 改善且不是单纯维度收益 |
| phase schedule 是否有效 | early fraction 与 C→H policy 网格 | always allow、always block | human 与 camera/framing 形成稳定 Pareto 改善 |
| sparse control 是否泛化 | unseen temporal/branch masks | train-seen masks、hard replacement | adherence 提升且 FTD/TMR 不显著崩坏 |
| no-text transfer 是否成立 | source human + target camera/framing | text condition、zero text、shuffle source | 使用目标关系且保留 source motion identity |

所有表格只比较同一 dataset/split、Stage1、cache、updates、seed 与 sampler budget。不同 camera contract 的结果单独报告，不强行合并为单一排名。

### 6.6 最小实现路线与停止条件

1. **M0 — Unified-3**：只改 task sampling 和 exposure ledger。失败则停止 StoryMotion++，先处理 negative transfer。
2. **M1 — Phase schedule**：固定 M0 checkpoint，加入 inference-only `g(s)`。没有 Pareto 改善则保留静态 directed blocking。
3. **M2 — Sparse projection**：加入 temporal mask 与 clean-endpoint projection。exact constraint 与分布质量必须同时通过。
4. **M3 — No-text transfer**：先做完整 branch recombination，再做 inversion/feature transfer。
5. **M4 — Multi-character/long-form**：只有 M0–M3 形成稳定方法链后才进入。

停止条件应写进实验计划：若 Unified-3 相对 specialists 在任一核心模式持续显著退化，StoryMotion++ 不再坚持 fully shared checkpoint，而转向 shared backbone + lightweight task heads；若 phase guidance 只在单 seed 或单 sampler 有效，则不能作为方法贡献。

### 6.7 论文叙事建议

论文主线应从“生成更多模态”改写为“解决 relational ambiguity”：相同的画面变化可以由 human motion、camera motion 或二者共同造成；静态对称耦合容易把这种歧义变成跨分支泄漏。StoryMotion++ 先用 structured observations 定义谁是条件、谁是目标，再用 actor-relative state 描述关系，最后用 phase-adaptive guidance 在全局布局与局部细节间分配条件职责。Zero-shot editing 是这一统一关系先验的推论，而不是孤立附加功能。
