---
title: "Any2Any 3D Diffusion Models with Knowledge Transfer: A Radiotherapy Planning Study"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/Any2Any_3D_Diffusion_Models_with_Knowledge_Transfer_A_Radiotherapy_Planning_Study.pdf
project_link: null
code_link: null
aliases:
- A3DMKTRPS
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
- topic/generative_models_diffusion
- topic/generative_models_diffusion/diffusion_image_video
core_operator: 将预训练视频扩散先验（Wan 2.1/MAISI）转移到剂量预测任务，并结合Any2Any条件化范式与基于临床评分卡的强化学习后训练，是突破性能瓶颈的核心操作杠杆。
primary_logic: 即使存在显著的域差异（从自然视频到医学剂量分布），利用大规模3D扩散先验、模态与角色感知的统一条件化（Any2Any），以及将临床评分卡转化为RL奖励信号的后训练，可以实现高效、稳健且临床相关的体素级剂量预测。
claims:
- DiffKT3D将体素级MAE从2.07 Gy降至1.93 Gy，超越GDP-HMM挑战赛冠军，且临床评分（Scorecard）从134.81提升至137.55。
- ScardNFT后训练在不损害体素保真度的前提下，持续提升临床对齐度，验证了RL引导的偏好优化是有效的。
- 在跨癌种知识迁移场景中（GDP-HMM→REQUITE前列腺），Any2Any扩散模型仅需少量微调即可快速收敛，MAE降至1.01 Gy，远超顶级回归基线。
- 消融实验表明，去除角色嵌入或使用因果注意力会显著降低性能，而4D RoPE和Any2Any统一训练范式是取得高性能的关键设计。
---

# Any2Any 3D Diffusion Models with Knowledge Transfer: A Radiotherapy Planning Study

> [!tip] 核心洞察
> 即使存在显著的域差异（从自然视频到医学剂量分布），利用大规模3D扩散先验、模态与角色感知的统一条件化（Any2Any），以及将临床评分卡转化为RL奖励信号的后训练，可以实现高效、稳健且临床相关的体素级剂量预测。

| 字段 | 内容 |
|------|------|
| 中文题名 | 面向放疗计划的任意到任意三维扩散模型与知识迁移 |
| 英文题名 | Any2Any 3D Diffusion Models with Knowledge Transfer: A Radiotherapy Planning Study |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2605.09622) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction #topic/generative_models_diffusion #topic/generative_models_diffusion/diffusion_image_video |
| Method | DiffKT3D |
| Dataset | GDP-HMM, REQUITE-Prostate |

> [!tip] 效果简介
> - GDP-HMM (test set) 上，MAE (Gy) 1.93 vs 2.07 (Challenge Top-1) (-0.14)；Scorecard (↑) 137.55 vs 134.81 (Challenge Top-1) (+2.74)；LPIPS (↓) 0.020 vs 0.033 (Challenge Top-1) (-0.013)。
> - REQUITE-Prostate 上，MAE (Gy) 1.01 / 0.97† vs 1.37 (best baseline) (-0.36 / -0.40)。

## 概要

放疗剂量预测是放射治疗计划中的关键步骤，其目标是根据患者的CT影像和靶区/危及器官勾画，生成满足临床处方要求的三维剂量分布。当前该领域面临两大核心瓶颈：**一是缺乏大规模预训练扩散先验的跨域迁移能力**，现有方法多依赖随机初始化或仅使用放疗数据训练，难以从海量自然视频或医学影像数据中汲取可迁移的表征；**二是模型输出难以对齐不同机构的临床偏好和指南要求**，单纯优化体素级回归损失（如MAE）无法保证生成的剂量分布在临床评分卡（Scorecard）上达到最优。

针对上述瓶颈，本文提出 **DiffKT3D**——一个统一的**任意到任意（Any2Any）三维扩散框架**，其核心操作杠杆包含三个关键设计：

1. **知识迁移**：将预训练视频扩散模型（Wan 2.1）或CT扩散模型（MAISI）的先验权重迁移至剂量预测任务，即使存在从自然视频到医学剂量分布的显著域差异，也能极大加速收敛并提升最终性能。
2. **Any2Any条件化范式**：引入模态与角色感知的统一条件化机制，通过可学习角色嵌入区分目标与条件令牌，结合4D RoPE位置编码增强跨模态自注意力，使单一模型能够以任意模态组合作为条件、预测任意目标模态。
3. **基于临床评分卡的强化学习后训练（ScardNFT）**：将临床评分卡转化为可微奖励信号，通过NFT损失对扩散得分场进行偏好优化，在不损害体素保真度的前提下持续提升临床对齐度。

在超过8,000例头颈和肺部放疗计划（GDP-HMM挑战赛）以及REQUITE前列腺数据集上的实验表明，DiffKT3D取得了当前最优性能：**体素级MAE从挑战赛冠军的2.07 Gy降至1.93 Gy，临床评分从134.81提升至137.55**。在跨癌种知识迁移场景中，仅需少量微调即可快速收敛，MAE降至1.01 Gy，远超顶级回归基线。消融实验进一步验证了角色嵌入、全注意力机制、v参数化以及预训练先验迁移等设计的关键贡献。



### 放疗剂量预测的临床瓶颈

现代放射治疗计划设计高度依赖精准的三维剂量分布预测，其核心目标是在保证靶区（PTV）处方剂量的同时，最大限度保护危及器官（OAR）。然而，当前剂量预测方法面临两大系统性瓶颈：

**瓶颈一：缺乏大规模预训练先验的跨域迁移能力。** 剂量预测本质上是一个高维、体素级的三维回归问题，但可用的放疗计划数据通常规模有限（单机构通常仅数百至数千例），难以支撑从零训练一个具备强泛化能力的深度生成模型。与此同时，自然视频和医学影像领域已积累了大规模预训练的扩散先验（如 Wan 2.1、MAISI），但这些先验与剂量分布之间存在显著的域差异——从 RGB 视频或 CT 影像到体素级剂量图，模态特性、动态范围和物理含义截然不同。如何弥合这一域鸿沟，将预训练先验有效迁移至剂量预测任务，是一个尚未被充分探索的关键问题。

**瓶颈二：模型输出难以对齐不同机构的临床偏好和指南要求。** 剂量预测的最终评判标准并非单纯的体素误差，而是临床可接受性——即预测剂量分布是否符合特定机构的处方指南、OAR 约束和治疗协议。传统方法仅依赖体素级回归损失（如 MAE、MSE），无法显式编码这些临床偏好，导致即使体素精度较高的预测，仍可能在关键剂量学指标（如 D95、V30）上偏离临床要求，需要大量人工修正。

### 现有方法的局限性

当前放疗剂量预测的主流范式可归纳为两类：

- **回归式方法**：以 GDP-HMM 挑战赛中的顶级方案为代表，如基于 MedNeXt 骨干的 Yasin、tyxiong123 等，以及基于 nnUNet 的 SKLSDE-BH。这些方法直接学习从 CT 和分割掩码到剂量分布的映射，训练高效、推理快速，但受限于确定性回归的固有局限——难以捕捉剂量分布的多模态性和不确定性，且缺乏对临床偏好的显式建模能力。

- **扩散式方法**：以 MedVision 的潜在扩散模型（LDM）为代表，尝试将扩散生成范式引入剂量预测。然而，现有扩散方案多采用简单的通道拼接式条件化（Conditional DiT Concat）或 3D ControlNet 风格的条件注入，未能充分利用放疗场景中多模态、多角色（条件 vs. 目标）的异构特性。此外，这些方法通常仅依赖扩散损失进行训练，缺乏将临床评分卡（Scorecard）直接纳入优化目标的机制。

### 本文的核心动机与研究问题

针对上述瓶颈，本文提出 **DiffKT3D**，一个统一的 Any2Any 三维扩散框架，旨在回答两个核心研究问题：

1. **跨域知识迁移**：能否将大规模预训练的三维扩散先验（来自自然视频或 CT 数据）有效迁移至剂量预测任务，即使存在显著的域差异？预训练先验能否加速收敛并提升最终性能上限？

2. **临床偏好对齐**：能否通过强化学习后训练，将基于临床指南的评分卡转化为可微奖励信号，在不损害体素保真度的前提下，使扩散生成结果对齐机构的规划偏好？

DiffKT3D 的设计围绕三个关键操作杠杆展开：**预训练扩散先验迁移**（从 Wan 2.1/MAISI 初始化 DiT 权重）、**Any2Any 条件化范式**（模态与角色感知的统一条件机制，含 4D RoPE 和可学习角色嵌入）、以及 **ScardNFT 强化学习后训练**（将临床评分卡转化为 NFT 损失中的偏好信号）。这一框架旨在实现高效、稳健且临床相关的体素级剂量预测，同时保持对任意模态组合的灵活适应能力。



## 核心方法与创新机理

DiffKT3D 的核心创新并非提出一个孤立的新模块，而是构建了一套系统性的“知识迁移 + 统一条件化 + 偏好对齐”三阶段范式，以此突破放疗剂量预测领域长期存在的两大瓶颈：**大规模预训练先验的跨域迁移困难**，以及**模型输出与多机构临床指南的对齐难题**。其创新点集中体现在三个关键的 changed slots 上。

### 创新一：从视频扩散到剂量预测的跨域先验迁移

传统放疗剂量预测模型（如挑战赛中基于 MedNeXt 或 nnUNet 的回归方法）通常采用随机初始化或仅在放疗数据上训练，这严重限制了模型在有限医学数据下的表征能力。DiffKT3D 的核心操作杠杆之一，是将在大规模自然视频数据上预训练的 3D 扩散模型（Wan 2.1）的权重直接迁移至剂量预测任务。

尽管源域（自然视频）与目标域（CT/剂量/结构掩膜）之间存在显著的域差异，这一迁移策略仍带来了决定性的性能增益。消融实验明确显示，引入预训练权重相比从头训练，不仅**大幅加速收敛**，更在最终性能上取得了**显著提升**（Table 4）。这证明了 3D 扩散模型从视频数据中习得的底层时空表征，对医学体素数据的生成具有可迁移的归纳偏置。值得注意的是，为弥合这一庞大的域差，主训练阶段必须对 DiT 块进行**全微调**，而 LoRA 仅在后训练阶段有效（Table 6）。

### 创新二：模态与角色感知的 Any2Any 统一条件化范式

此前的条件扩散模型多采用通道拼接（Conditional DiT）或 ControlNet 式级联，这些策略在异构放疗模态（CT、多结构掩膜、剂量、射束板）场景下要么难以灵活组合条件，要么性能显著下降（3D ControlNet 的 MAE 高达 2.42 Gy）。DiffKT3D 引入了三个紧密耦合的设计，构成其条件化机制的核心创新：

1.  **Any2Any 门控与统一训练**：训练时随机将任意模态指定为目标或条件，使单一模型能够处理“任意模态作为条件、任意模态作为目标”的生成任务。从条件扩散过渡到 Any2Any 范式本身就能进一步提升性能（Table 4 消融），验证了联合建模多模态依赖的优势。

2.  **可学习角色嵌入（Role Embedding）**：通过一个二值嵌入区分目标令牌与条件令牌，并与时间步嵌入相加后注入共享的 AdaLayerNorm 调制器，驱动 FiLM 式缩放与偏移。消融实验表明，**移除角色嵌入会清楚损害体素精度和临床评分**（Table 4），证明显式建模“条件-目标”身份对跨模态注意力至关重要。

3.  **4D RoPE 位置编码**：将标准 3D RoPE 扩展至包含“槽位轴”（Slot Axis）的 4D 版本，通过公式 $d = d_S + d_H + d_W + d_D$ 分割注意力头维度，使模型能同时编码模态身份和三维空间坐标。这一设计使自注意力机制能够感知不同模态令牌的来源，是 Any2Any 框架高效运行的关键。

### 创新三：基于临床评分卡的强化学习后训练（ScardNFT）

体素级回归损失（MAE/MSE）无法直接反映临床计划的接受度——一个 MAE 较低的预测可能仍在关键危及器官的剂量约束上违反指南。DiffKT3D 的第三个核心创新是将临床评分卡转化为可微的强化学习奖励信号，通过**ScardNFT** 后训练实现偏好对齐。

具体而言，评分卡将剂量-体积直方图（DVH）统计量（如 D95、V30）映射为结构级评分，经加权求和得到原始奖励 $r^{\mathrm{raw}}$，再通过指数变换与裁剪归一化为最优性概率 $r \in [0,1]$。NFT 损失利用高奖励样本对扩散得分场进行正向引导，对低奖励样本施加反向惩罚，最终与扩散损失联合优化：
$$\mathcal{L}(\theta) = \mathcal{L}_{\mathrm{NFT}}(\theta) + \lambda \mathcal{L}_{\mathrm{diff}}(\theta)$$

决定性证据表明，ScardNFT 在不损害体素保真度的前提下，将临床评分从 134.81 提升至 137.55（Table 1），且在逐结构评分对比中，RL 增强模型在多个关键结构上显著优于未对齐的扩散模型和挑战赛冠军基线（Figure 4）。这验证了**将临床知识作为奖励信号注入生成过程**的有效性，使模型输出从“统计上接近参考剂量”进化为“临床上更可接受”。

---

**创新总结**：DiffKT3D 的三个 changed slots 形成了因果闭环——预训练先验提供了强大的生成基础，Any2Any 条件化实现了对异构模态的高效利用，而 ScardNFT 则将临床偏好直接编码进训练目标。三者协同，使得模型在体素精度（MAE 1.93 Gy）、感知质量（LPIPS 0.020）和临床对齐度（Scorecard 137.55）三个维度上全面超越了 GDP-HMM 挑战赛冠军。



DiffKT3D 的整体框架围绕三个核心阶段构建：**大规模扩散先验迁移**、**Any2Any 统一条件化训练**，以及**基于临床评分卡的强化学习后训练**。这三个阶段形成一条从通用生成能力到临床偏好对齐的完整流水线，如 Figure 1 所示。

![[assets/figures/papers/paper_list_l2185_https_arxiv_org_abs_2605_09622/figures/001_Figure_1.jpg]]
*Figure 1: Illustration of the proposed DiffKT3D. We first transfer priors from diffusion models pretrained on large-scale public video or CT data, despite a substantial domain gap to radiotherapy dose prediction. These backbones are then adapted to heterogeneous RT modalities with relatively limited data, followed by RL posttraining driven by guideline-derived clinical Scorecards to better align predictions with institutional planning preferences*

### 三阶段流水线

**第一阶段：先验迁移。** 将在大规模自然视频（Wan 2.1）或 CT 数据（MAISI）上预训练的 3D 扩散模型权重迁移至剂量预测任务。尽管源域（自然视频/医学影像）与目标域（体素级剂量分布）存在显著的域差异，预训练 DiT 骨干仍为后续微调提供了强大的生成先验。消融实验表明，引入预训练相比从头训练能极大加速收敛并显著提升最终性能。

**第二阶段：Any2Any 条件化训练。** 在相对有限的放疗数据上，以统一的 Any2Any 范式对 DiT 块进行全微调。该阶段的核心是模态与角色感知的条件化机制：每次训练随机将各模态（CT、结构掩码、射束板、剂量等）分配为条件或目标，目标模态经正向扩散加噪后与清洁条件令牌一同送入 DiT 进行联合自注意力，预测 v 参数化输出。

**第三阶段：ScardNFT 后训练。** 将机构特定的临床评分卡（Scorecard）转化为可微奖励信号，通过 NFT（Noise Fine-Tuning）损失对扩散得分场进行偏好优化。该阶段仅需轻量级 LoRA 微调，在不损害体素级保真度的前提下持续提升临床对齐度——验证集评分卡从 134.81 提升至 137.55。

### 模块关系与数据流

Figure 2 详细描绘了 DiffKT3D 的训练机制，Figure 6 给出了 VAE–DiT 混合架构的完整结构。数据流经以下模块依次处理：

1. **Frozen Wan VAE Encoder**  
   多模态 3D 体数据（CT、结构掩码、剂量、射束板等）首先通过冻结的 3D VAE 编码器压缩至共享潜空间，获得紧凑的潜在表示。VAE 在视频数据上预训练后保持冻结，仅 DiT 块参与微调（Table 8 消融证实冻结 VAE 为最优策略）。

![[assets/figures/papers/paper_list_l2185_https_arxiv_org_abs_2605_09622/figures/015_Table_8.jpg]]
*Table 8: Effect of VAE adaptation on GDP–HMM (validation). All variants use the same Any2Any DiT with v-pred and 10-step sampling*

2. **Modality-specific Patch Embedding (PEₘ)**  
   每个模态拥有独立的轻量级 3D 卷积补丁嵌入层，将潜在网格（或带噪目标潜在）映射为统一维度 D 的令牌序列。该设计使各模态在共享 DiT 骨干中保持模态特异性表示。

3. **Slot-aware 4D RoPE**  
   在标准 3D RoPE 基础上引入额外的槽位轴（slot axis），将注意力头维度 d 分割为四个子维度：
   $$d = d_S + d_H + d_W + d_D$$
   其中 S 轴编码模态身份，H/W/D 轴编码三维空间坐标。4D RoPE 使自注意力机制能够同时感知令牌的模态来源与空间位置，增强跨模态依赖建模。

4. **Role Embedding + AdaLayerNorm**  
   可学习的二值角色嵌入（role embedding）区分目标令牌与条件令牌，通过与时步嵌入相加后注入共享的 AdaLayerNorm 调制器，以 FiLM 式（Scale, Shift）操作驱动各 DiT 块的自适应归一化。消融实验表明，移除角色嵌入会清楚损害体素精度和临床评分。

5. **Fine-tuned DiT Blocks**  
   DiT 块对清洁条件令牌与带噪目标令牌执行联合全注意力（full attention），预测目标模态的 v 参数化输出 $v_\theta$。与因果注意力相比，全注意力能更有效地捕获跨模态依赖关系。原始 Wan DiT 中的交叉注意力层被移除，因为 DiffKT3D 不使用语言令牌。

6. **Frozen Wan VAE Decoder**  
   预测的潜在代码经 VAE 解码器恢复至原始体素空间，得到最终剂量分布。

7. **ScardNFT RL Post-training**  
   在监督训练收敛后，引入基于评分卡的 RL 后训练模块。将临床评分卡的逐结构加权得分作为原始奖励 $r^{\mathrm{raw}}$，经指数变换与裁剪归一化为 $[0,1]$ 区间的最优性概率，再通过 NFT 损失对高奖励样本正向引导、低奖励样本反向惩罚，实现扩散生成与机构偏好的对齐。

### 输入输出规范

- **输入**：多模态放疗数据，包括 CT 影像、靶区/危及器官结构掩码、射束板信息等。训练时随机选择目标模态 $\tau$ 和条件子集 $S \subseteq M \setminus \{\tau\}$。
- **输出**：目标模态的体素级预测，以剂量分布为主要任务，同时支持任意模态的单模态预测（Table 5 验证了 remaining-1 设定下的跨模态生成能力）。
- **推理**：采用 10 步 DDIM 采样，单病例推理时间约 16 秒（H100 GPU），显存消耗约 8.70 GB，远低于 2D 切片扩散的 32.40 GB（Table 6）。

![[assets/figures/papers/paper_list_l2185_https_arxiv_org_abs_2605_09622/figures/009_Table_5.jpg]]
*Table 5: Single-modality prediction under the remaining-1 (predictone) setting. What this table shows: each modality is predicted from all the others. CT uses FID; segmentation-like modalities use Dice; Dose and Beam Plate use MAE only*



### 3.1 潜空间扩散与Any2Any条件化范式

DiffKT3D的生成过程完全在共享的VAE潜空间内进行。多模态体数据（CT、结构掩膜、剂量分布等）首先通过**冻结的Wan VAE编码器**压缩为紧凑的潜表示，随后由**模态特定的轻量级补丁嵌入**（PEₘ）将潜网格映射为统一维度D的令牌序列。

**Any2Any门控机制**是框架的核心设计：在每个训练步，从模态集合M中均匀采样一个目标模态τ，并从剩余模态中按课程策略抽取条件子集S。条件模态的干净潜令牌与目标模态的带噪潜令牌被拼接后送入DiT，实现“任意模态作为条件、任意模态作为目标”的统一训练。

**角色嵌入**（Role Embedding）通过一个可学习的二值嵌入区分目标令牌与条件令牌。该嵌入与时步嵌入相加后，通过共享的**AdaLayerNorm**调制器注入DiT的每一层，以FiLM式（缩放、偏移）操作驱动条件化。

### 3.2 4D旋转位置编码

为编码令牌的模态身份与三维空间位置，DiffKT3D在标准3D RoPE基础上扩展了一个**槽位轴**（slot axis），形成4D RoPE。注意力头维度d被分割为四个子维度：

$$d = d_S + d_H + d_W + d_D$$

其中d_S对应槽位轴（区分不同模态），d_H、d_W、d_D分别对应高度、宽度、深度三个空间轴。各轴独立计算正弦频率：

$$\mathrm{freqs}_a(i) = \theta_a^{-2i/d_a}$$

这使得自注意力机制能够同时感知令牌的模态来源和空间坐标，增强跨模态依赖建模。

### 3.3 正向扩散与v参数化

对于选定的目标模态τ，正向扩散过程遵循标准保方差噪声调度：

$$x_t^{(\tau)} = \alpha_t x_0^{(\tau)} + \sigma_t \varepsilon, \quad \varepsilon \sim \mathcal{N}(0, \mathbf{I}), \quad t \sim \mathcal{U}(0,1)$$

其中α_t和σ_t为时间步t的噪声调度系数。

DiffKT3D采用**v参数化**作为预测目标，定义为：

$$v(x_0, \varepsilon, t) = \alpha_t \varepsilon - \sigma_t x_0$$

该参数化在跨时间步上产生更优的梯度条件。从预测的v可解析恢复原始数据x₀和噪声ε：

$$x_0 = \alpha_t x_t - \sigma_t v, \qquad \varepsilon = \sigma_t x_t + \alpha_t v$$

扩散训练损失为v参数化下的均方误差，对目标模态τ、条件子集S和时间步t求期望：

$$\mathcal{L}_{\mathrm{diff}} = \mathbb{E}_{t,\varepsilon,\tau,S} \left[ \| v_{\theta}(x_t^{(\tau)}, C, t) - v(x_0^{(\tau)}, \varepsilon, t) \|_2^2 \right]$$

### 3.4 临床评分卡驱动的RL后训练（ScardNFT）

为对齐不同机构的临床偏好，DiffKT3D引入**ScardNFT**后训练阶段。首先，基于剂量-体积直方图（DVH）统计量定义原始评分卡奖励：

$$r^{\mathrm{raw}}(y,C) = \sum_{s \in \mathcal{S}} w_s \mathrm{score}_s (\phi_s(y;C))$$

其中φ_s提取结构s的DVH指标（如D95、V30），score_s根据临床指南赋分，w_s为结构权重。

原始奖励经指数变换后裁剪至[0,1]，归一化为最优性概率：

$$r = \frac{1}{2} + \frac{1}{2} \exp\left( \frac{r^{\mathrm{raw}} - \mathbb{E}_{y\sim\pi_{\mathrm{old}}}[r^{\mathrm{raw}}]}{Z_C}, -1, 1\right)$$

该概率驱动**NFT损失函数**，通过对高奖励样本正向引导、低奖励样本反向惩罚来重缩放扩散得分场：

$$\mathcal{L}_{\mathrm{NFT}} = \mathbb{E} \left[ r \| \tilde{v}_{\theta}^{+} - v \|_2^2 + (1-r) \| \tilde{v}_{\theta}^{-} - v \|_2^2 \right]$$

最终训练目标平衡临床偏好对齐与体素级保真度：

$$\mathcal{L}(\theta) = \mathcal{L}_{\mathrm{NFT}}(\theta) + \lambda \mathcal{L}_{\mathrm{diff}}(\theta)$$

其中λ控制RL更新的强度。该设计使模型在不损害体素精度的前提下，持续提升与临床指南的对齐度。

### 补充图表

![[assets/figures/papers/paper_list_l2185_https_arxiv_org_abs_2605_09622/figures/002_Figure_2.jpg]]
*Figure 2: Training mechanism for DiffKT3D. The multi-modal data first pass through the VAE encoder to obtain latent features. With the Any2Any gating mechanism, each modality is randomly assigned as either a condition or a target. Conditional modalities are independently encoded into patch tokens, while target modalities are combined with latent noise*

![[assets/figures/papers/paper_list_l2185_https_arxiv_org_abs_2605_09622/figures/011_Figure_6.jpg]]
*Figure 6: Architecture of the proposed VAE–DiT-based conditional diffusion model DiffKT3D. Left: multi-branch VAE–DiT pipeline for CT*



## 实验与关键发现

### 主实验结果

DiffKT3D在GDP-HMM挑战赛测试集上建立了新的最先进水平。如Table 1所示，该方法将体素级MAE从挑战赛冠军方案的2.07 Gy降至**1.93 Gy**，降幅达0.14 Gy；同时临床评分卡（Scorecard）从134.81提升至**137.55**，感知质量指标LPIPS从0.033降至**0.020**。这表明模型不仅在体素精度上超越了顶级回归基线（包括基于MedNeXt的Yasin、tyxiong123等方案），更在临床可接受性上实现了显著增益。

引入ScardNFT后训练（Ours+ScardNFT）在不损害体素保真度的前提下，持续提升临床对齐度——验证集和测试集的Scorecard均获得一致性改善。这一结果证实，将临床评分卡转化为可微奖励信号并嵌入RL后训练框架，能够有效引导扩散生成朝向机构偏好方向优化。

### 消融实验

Table 4的系统性消融揭示了各设计组件的独立贡献：

**角色嵌入与注意力机制。** 移除角色嵌入（role embedding）会清楚损害体素精度和临床评分，证明在联合自注意力中显式区分目标令牌与条件令牌至关重要。将全注意力替换为因果注意力同样导致性能下降，因为因果掩码削弱了模型捕获跨模态依赖的能力——剂量预测需要目标区域充分感知所有条件模态的全局上下文。

**Any2Any训练范式。** 从条件扩散过渡到统一的Any2Any训练范式可进一步提升性能。该范式通过随机分配任意模态作为目标，迫使模型学习更鲁棒的跨模态映射，而非仅固定剂量作为预测目标。

**v参数化与采样步数。** Table 2和Table 7显示，v参数化（v-prediction）在单步和十步采样下均显著优于x₀预测和噪声预测（ϵ-pred），被选为默认设置。其优势源于v参数化在扩散时间步上提供更好条件的梯度。多步迭代细化（从1步到10步）持续改善剂量质量，确认扩散细化对峰值剂量学性能的必要性。

**预训练知识迁移。** Figure 3（左）的收敛曲线表明，引入Wan 2.1预训练大幅加速收敛，并达到远优于从头训练（from scratch）的最终性能。Table 9进一步验证了知识迁移的通用性：即使使用医学CT预训练的MAISI扩散先验，在合适的参数化下同样能获得有竞争力的结果。但需注意，当源域与目标域差距极大时（如MAISI的噪声预测模式可能导致动态范围漂移），性能可能崩溃，需额外适配设计。

**微调策略。** 主训练阶段全微调DiT块是必要的，因为自然视频与医学剂量分布间存在庞大域差，LoRA等轻量适配不足以弥合。然而，LoRA在轻量的ScardNFT后训练阶段被证明有效（Table 4），可在保持体素精度的同时高效对齐临床偏好。Table 8的VAE消融表明，冻结VAE解码器即可获得满意性能，微调VAE带来的增益有限。

**条件化策略对比。** Table 6的扩展对比显示，3D ControlNet在此异构RT模态场景下表现不佳（MAE 2.42 Gy），因其设计初衷是处理同模态的图像到图像翻译，难以适配多模态条件。2D切片扩散存在层间不一致问题，且显存消耗高达32.40 GB（vs. DiffKT3D的8.70 GB），不适用于临床部署。

### 跨癌种知识迁移

Table 3展示了从GDP-HMM（头颈/肺）到REQUITE前列腺数据集的迁移能力。所有方法均从GDP-HMM检查点初始化并采用相同微调策略。Any2Any扩散模型仅需少量微调即可快速收敛，MAE降至**1.01 Gy**（best-of-n为0.97 Gy），远超最佳回归基线（1.37 Gy）。Figure 3（中）的微调曲线进一步验证了扩散先验的迁移效率——模型在极少迭代内即超越收敛后的回归基线。

![[assets/figures/papers/paper_list_l2185_https_arxiv_org_abs_2605_09622/figures/004_Figure_3.jpg]]
*Figure 3: MAE vs. training epochs / inference steps. The single figure contains three subplots: (left) pretrain vs. from-scratch across epochs, (middle) model-transfer finetuning curve, and (right) testtime scaling (single vs. best-of-n)*

### 单模态预测与框架灵活性

Table 5展示了Any2Any框架的灵活性：在remaining-1设定下（每次预测一种模态，其余作为条件），模型不仅能预测剂量，还能生成CT、分割掩码等模态。CT使用FID评估，分割类模态使用Dice，剂量和射束板使用MAE。这一能力源于Any2Any门控机制与统一令牌空间的设计，使单一模型覆盖多种预测任务。

### 定性分析

Figure 5和Figure 7提供了头颈、肺、前列腺病例的定性对比。DiffKT3D在靶区适形度上展现明显优势，剂量分布更贴近参考计划，DVH曲线与真实值高度吻合。Figure 4的逐结构评分卡对比揭示，RL后训练（Ours+ScardNFT）对特定OAR的保护能力优于纯扩散模型和挑战赛冠军方案，说明评分卡奖励信号成功编码了机构特定的临床优先级。

### 推理效率与局限

10步采样下DiffKT3D的单病例推理时间约16秒（Table 6），虽在临床计划优化的离线场景中可接受，但相比回归模型的毫秒级推理仍有差距。显存占用（8.70 GB）显著优于2D切片扩散方案。Figure 3（右）的测试时扩展曲线表明，best-of-n策略可进一步压榨性能，但以线性增长的推理成本为代价。

![[assets/figures/papers/paper_list_l2185_https_arxiv_org_abs_2605_09622/figures/013_Table_6.jpg]]
*Table 6: Extended comparison on GDP–HMM (validation set). All diffusion models use 10-step sampling. Inference time and peak GPU memory are measured per case on a single H100 GPU. Data loading time is included*

**需注意的失败模式：** 当前扩散训练未直接将DVH等剂量学指标作为可微损失嵌入，而是依赖后训练阶段对齐，端到端的DVH感知扩散损失值得探索。预训练先验迁移高度依赖源域模型质量，MAISI噪声预测模式下的动态范围漂移问题（Table 9）提示跨域适配需谨慎选择参数化策略。模型仅在历史回顾性数据上验证，前瞻性临床部署的鲁棒性尚待评估。

### 补充图表

![[assets/figures/papers/paper_list_l2185_https_arxiv_org_abs_2605_09622/figures/003_Table_1.jpg]]
*Table 1: Main results on GDP-HMM (validation & test). Metrics: MAE (Gy; ↓), clinical Scorecard (Score) (↑), PSNR (dB; ↑), SSIM (↑), and LPIPS (↓). The main table spans both columns; bold indicates the best in its block*

![[assets/figures/papers/paper_list_l2185_https_arxiv_org_abs_2605_09622/figures/008_Table_4.jpg]]
*Table 4: Component ablations on validation set*

![[assets/figures/papers/paper_list_l2185_https_arxiv_org_abs_2605_09622/figures/006_Figure_4.jpg]]
*Figure 4: Per-structure scorecard value comparison of head-andneck plans. The plot contrasts reference, the challenge Top-1 baseline, our diffusion model, and our RL-enhanced variant (Ours+ScardNFT), showing how reinforcement learning can improve alignment with institutional planning objectives*

![[assets/figures/papers/paper_list_l2185_https_arxiv_org_abs_2605_09622/figures/007_Table_3.jpg]]
*Table 3: Comparisons on REQUITE-Prostate. We report MAE (Gy; ↓), PSNR (dB; ↑), SSIM (↑), and LPIPS (↓). Both ours and baselines are pretrained with GDP-HMM and fine-tuned on prostate data. † denotes best-of-n*

![[assets/figures/papers/paper_list_l2185_https_arxiv_org_abs_2605_09622/figures/016_Table_9.jpg]]
*Table 9: GDP–HMM head-and-neck results on the MAISI backbone with different output parameterizations. MAE is reported in Gy. Infer time is only reported on deep learning backbone forward without data loading*



## 定位与知识库关联

### 1. 方法谱系：从条件扩散到Any2Any统一生成

**DiffKT3D** 在放疗剂量预测领域的定位，可以沿两条技术谱系理解：一是**扩散生成模型在医学影像中的应用**，二是**跨模态条件化机制**的演进。

#### 1.1 扩散模型在剂量预测中的演进

剂量预测任务长期由回归模型主导。GDP-HMM Grand Challenge 的顶级方案普遍采用卷积骨干网络直接回归体素级剂量分布，例如基于 **MedNeXt** 的 **Yasin**（挑战赛冠军）、**tyxiong123**、**rcgao**、**PVmed** 等方案，以及基于 **nnUNet** 的 **SKLSDE-BH** 方案。这些方法以体素级 MAE/MSE 为优化目标，取得了可观的精度（冠军方案 MAE 2.07 Gy），但本质上缺乏对剂量分布整体结构和临床偏好的显式建模。

扩散模型在剂量预测中的尝试尚处早期。挑战赛中 **MedVision** 团队采用了**潜在扩散模型（LDM）**，代表了将生成式方法引入该任务的初步探索。DiffKT3D 在此基础上实现了三个关键跃迁：

1. **从条件扩散到Any2Any统一范式**：传统条件扩散（如通道拼接式 Conditional DiT、3D ControlNet）固定条件与目标模态的角色，限制了跨模态信息的灵活利用。DiffKT3D 的 Any2Any 门控机制随机分配各模态为条件或目标，使单一模型能够处理任意模态组合的生成任务。
2. **从随机初始化到大规模预训练先验迁移**：将 **Wan 2.1**（大规模视频扩散模型）或 **MAISI**（CT预训练扩散模型）的 DiT 权重迁移至剂量预测任务，即使源域（自然视频）与目标域（医学剂量分布）存在显著差异。
3. **从纯体素损失到临床偏好对齐**：引入基于临床评分卡的强化学习后训练（ScardNFT），将机构规划指南转化为可微奖励信号，在不损害体素保真度的前提下提升临床可接受性。

#### 1.2 Any2Any条件化范式的设计谱系

在条件化机制上，DiffKT3D 的 Any2Any 方案与现有方法形成清晰对比：

| 条件化策略 | 代表方法 | 核心机制 | 在RT剂量预测中的局限 |
|-----------|---------|---------|-------------------|
| 通道拼接 | Conditional DiT (Concat) | 将条件图像沿通道维度与目标拼接 | 无法区分多模态条件的异质性角色 |
| 交叉注意力 | 3D ControlNet | 通过额外编码器提取条件特征，经交叉注意力注入生成过程 | 在异构RT模态下表现显著恶化（MAE 2.42 Gy），计算开销大 |
| 切片级2D扩散 | 2D Slice-wise Diffusion | 逐切片进行2D扩散生成 | 层间不一致性严重，显存消耗高（32.40 GB vs. 8.70 GB） |
| **Any2Any门控+角色嵌入** | **DiffKT3D** | 可学习角色嵌入区分目标/条件令牌，4D RoPE编码模态身份与空间位置，统一自注意力建模跨模态依赖 | — |

消融实验（Table 4）明确验证了关键设计的必要性：移除角色嵌入会清楚损害体素精度和临床评分；将全注意力替换为因果注意力则削弱了跨模态依赖建模能力，性能下降。这表明**区分目标与条件令牌的角色感知设计**和**全注意力机制**是 Any2Any 范式取得高性能的基石。

#### 1.3 与具体基线工作的关系

- **Yasin (MedNeXt)**：作为 GDP-HMM 挑战赛冠军，代表回归方法的性能上限（MAE 2.07 Gy, Scorecard 134.81）。DiffKT3D 在相同数据划分和评估协议下将 MAE 降至 1.93 Gy，Scorecard 提升至 137.55，验证了扩散生成范式对纯回归方法的超越。
- **MedVision (LDM)**：作为扩散基线，验证了扩散模型在该任务上的可行性，但其性能受限于条件化策略和预训练先验的缺失。
- **3D ControlNet**：作为 ControlNet 风格条件策略的对比基线，在 RT 异构模态场景下表现不佳（MAE 2.42），凸显了 Any2Any 统一自注意力方案在跨模态建模上的优势。
- **2D Slice-wise Diffusion**：切片级方法在层间一致性和显存效率上均存在明显劣势，反衬出 3D 全注意力扩散的必要性。

### 2. 知识库定位：预训练先验的跨域迁移

DiffKT3D 的核心知识杠杆在于**大规模预训练扩散先验的跨域迁移**。这一策略的成功依赖于以下发现：

#### 2.1 预训练先验的关键作用

即使源域（Wan 2.1 的自然视频）与目标域（放疗剂量分布）存在实质性域差异，预训练 DiT 权重的迁移仍能**极大加速收敛并提升最终性能**。Figure 3（左）显示，从头训练的模型在相同训练预算下远不及预训练迁移版本。这表明大规模扩散模型习得的**通用生成能力**（如空间结构建模、多尺度特征提取）具有跨域可迁移性。

#### 2.2 全微调的必要性与LoRA的适用边界

消融实验揭示了一个重要的适配策略分层：
- **主训练阶段**：必须对 DiT 块进行**全微调**，以弥合自然视频与医学剂量分布间的庞大域差。LoRA 在此阶段不足以完成如此剧烈的域适配。
- **后训练阶段**：ScardNFT 的轻量 RL 微调中，**LoRA 被证明有效**，可在不引入过多参数的前提下实现临床偏好对齐。

#### 2.3 预训练源域的选择与失败模式

MAISI 扩散先验的对比实验（Table 9）揭示了预训练源域选择的敏感性。当 MAISI 采用噪声预测模式（ϵ-pred）时，由于动态范围漂移，性能出现显著退化。这提示**预训练模型的输出参数化方式**与目标任务的适配性至关重要，不能简单假设任何预训练扩散先验都能带来正向迁移。

### 3. 适用边界与局限

#### 3.1 已验证的适用场景

- **多癌种剂量预测**：在头颈部（GDP-HMM）和前列腺（REQUITE）数据集上均取得最优性能，跨癌种迁移仅需少量微调即可快速收敛（MAE 从 1.37 Gy 降至 1.01 Gy）。
- **多模态生成**：Any2Any 框架支持从任意条件子集预测任意目标模态（Table 5），展示了统一模型处理异构 RT 模态的灵活性。
- **临床偏好对齐**：ScardNFT 后训练在不损害体素保真度的前提下持续提升临床评分（Figure 4），验证了 RL 引导的偏好优化在剂量预测中的有效性。

#### 3.2 明确局限

1. **推理时间**：10 步采样约需 16 秒/例，虽在临床计划优化场景中可接受，但显著高于回归模型的单次前向推理。模型蒸馏或 CUDA 部署优化是可行的加速路径，但尚未在本文中探索。
2. **回顾性验证局限**：所有实验均基于历史计划数据，尚未在真实前瞻性临床环境中评估部署鲁棒性和临床可接受性。
3. **DVH 感知训练的缺失**：当前扩散训练未直接将 DVH 等剂量特定指标作为可微损失引入，而是依赖后训练阶段对齐。端到端的 DVH 感知扩散损失值得探索。
4. **预训练先验依赖性**：迁移效果高度依赖源域模型质量。当源域与目标域的差距极大时（如 MAISI 噪声预测模式下的动态范围漂移），可能导致性能崩溃，需要额外的适配设计。

### 4. 开放问题

1. **推理效率的极致优化**：能否通过更轻量的骨干网络、结构化注意力或渐进式蒸馏，在保持生成质量的同时将推理时间压缩至秒级，以满足实时临床交互需求？
2. **端到端剂量学感知训练**：如何将 DVH 驱动的剂量学损失函数（如目标剂量约束、OAR 惩罚）直接、可微地嵌入扩散训练流程，实现一体化优化，而非两阶段的后训练补偿？
3. **多癌种与多治疗模式的泛化**：DiffKT3D 在其他癌症部位（如乳腺、食管）以及不同治疗模式（如 IMRT、质子治疗）上的泛化能力和迁移效率如何？Any2Any 框架是否能统一处理这些异构场景？
4. **多机构动态适配**：在真实多机构、多协议环境下，RL 后训练能否动态适应不同医院的评分卡，并持续保持性能？这需要验证 ScardNFT 对评分卡变化的鲁棒性和泛化性。
5. **预训练源域的最优选择**：预训练扩散模型的选择（视频、CT、自然图像）如何影响跨域迁移的效率与上限？是否存在更优的预训练任务和域（如医学影像特定预训练），能进一步缩小域差异并提升迁移效率？



## 原文 PDF

![[paperPDFs/CVPR_2026/Any2Any_3D_Diffusion_Models_with_Knowledge_Transfer_A_Radiotherapy_Planning_Study.pdf]]
