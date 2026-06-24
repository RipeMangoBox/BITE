---
title: "SAM 3D: 3Dfy Anything in Images"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/SAM_3D_3Dfy_Anything_in_Images.pdf
aliases:
- S3
- S33AI
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
core_operator: 采用LLM式多阶段训练范式和人在回路数据引擎（MITL）：合成预训练→半合成中期训练→真实数据后训练对齐（SFT+DPO），并通过模型与人类标注协同迭代循环，持续提升数据质量和模型能力。
primary_logic: 借鉴人类视觉中的“熟悉物体”线索，将识别能力转化为3D重建能力，利用大规模合成数据训练基础形状词汇，再通过半合成与真实数据对齐实现域泛化，从而突破3D数据壁垒，在自然场景中实现精准的物体几何、纹理与布局预测。
claims:
- 合成预训练与真实世界对齐相结合的多阶段训练框架，打破了3D“数据壁垒”。
- 人类和模型在环的标注管线生成了前所未有的规模数据，包括近100万图像、～3.14M无纹理网格和～100K有纹理网格。
- "在真实图像人类偏好测试中，SAM 3D 取得至少 5:1 的胜率。"
- 在 SA-3DAO 基准上，F1@0.01 从最佳竞争方法的 0.1629（Hi3DGen）提升至 0.2344，相对提升43.7%。
---

# SAM 3D: 3Dfy Anything in Images

> [!tip] 核心洞察
> 借鉴人类视觉中的“熟悉物体”线索，将识别能力转化为3D重建能力，利用大规模合成数据训练基础形状词汇，再通过半合成与真实数据对齐实现域泛化，从而突破3D数据壁垒，在自然场景中实现精准的物体几何、纹理与布局预测。

| 字段 | 内容 |
|------|------|
| 中文题名 | SAM 3D: 图像中的万物三维化 |
| 英文题名 | SAM 3D: 3Dfy Anything in Images |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2511.16624) · [Code](https://github.com/facebookresearch/sam-3d-objects) · [arXiv](http://arxiv.org/abs/1311.2524) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction |
| Method | SAM 3D |
| Dataset | SA-3DAO, ISO3D, Aria Digital Twin, Human Preference |

> [!tip] 效果简介
> - SA-3DAO (Artist Ground-Truth Shape) 上，F1@0.01 (↑) 0.2344 vs 0.1629 (Hi3DGen) (+0.0715)。
> - SA-3DAO 上，Chamfer (↓) 0.0400 vs 0.0937 (Hi3DGen) (-0.0537)。
> - ISO3D (Perceptual Similarity) 上，ULIP (↑) 0.1488 vs 0.1529 (TripoSG) (接近（-0.0041）)。

## 概述

从单张自然图像重建场景中每个物体的三维几何、纹理和空间布局，是通向视觉世界模型的关键一步。然而，该任务长期受困于一个根本瓶颈：真实图像与高质量3D标注的配对数据极度稀缺——标注物体的精确形状、姿态和纹理需要专业3D艺术家，成本高昂、规模受限，导致现有方法难以在遮挡、杂乱的真实场景中实现视觉标定的三维重建。

SAM 3D 的核心洞察在于借鉴人类视觉中的“熟悉物体”线索——将识别能力转化为3D重建能力。方法上，它借鉴大语言模型的多阶段训练范式，构建了一条从大规模合成数据到真实世界对齐的递进路径：首先在合成数据上预训练基础形状词汇，再通过半合成数据完成中期训练，最后利用真实数据后训练（SFT + DPO）实现域泛化，从而突破3D“数据壁垒”。与之配套的是一套人在回路/模型在回路的数据引擎（MITL），通过人类标注者与模型协同迭代，生成了近100万张图像、约314万个无纹理网格和约10万个有纹理网格的标注数据，规模前所未有。

在架构上，SAM 3D 采用两阶段设计：Geometry Model（基于 Mixture-of-Transformers 的1.2B参数流变换器）联合预测物体的粗略体素形状（$64^3$ 分辨率）与6D姿态/缩放参数；Texture & Refinement Model（600M参数稀疏潜在流变换器）则以粗略形状为条件，进一步细化几何细节并合成纹理。两阶段共享一个深度感知VAE的潜在空间，可统一解码为网格或3D高斯泼溅。

实验结果表明，在艺术家标注的真实几何基准 SA-3DAO 上，SAM 3D 的 F1@0.01 达到 0.2344，较此前最佳方法 **Hi3DGen**（Ye et al., 2025）的 0.1629 相对提升 43.7%；Chamfer 距离从 0.0937 降至 0.0400。在 Aria Digital Twin 的布局评测中，联合预测的 ADD-S@0.1 达到 0.7673，显著优于两阶段管线方法（0.5992）。在真实图像的人类偏好测试中，SAM 3D 在场景级和物体级重建上均取得至少 5:1 的胜率。消融实验进一步证实，多阶段训练的每个环节——MITL-3DO SFT/DPO、Art-3DO SFT/DPO——均为性能提升贡献了不可替代的增益。

## 背景与动机

### 核心瓶颈：自然图像的3D数据壁垒

从单张自然图像重建物体的三维几何、纹理与空间布局，是计算机视觉迈向场景理解的关键一步。然而，这一方向长期受困于一个根本性矛盾：**监督3D重建需要精确的形状、姿态与纹理标注，而这类标注只能由专业3D艺术家完成，成本极高、规模极小**。合成数据虽能提供无限量标注，但其渲染域与真实图像的分布鸿沟——光照、材质、遮挡、杂乱背景——使得纯合成训练的模型在真实场景中性能骤降。

这一“3D数据壁垒”构成了本工作的核心瓶颈：自然图像与3D真实标注配对的数据极度稀缺，导致模型难以在遮挡、杂乱的真实场景中实现视觉标定的三维重建。

### 现有方法的缺口

当前图像到3D重建方法可大致分为两类，各有结构性不足：

- **纯合成数据驱动的方法**（如 **Trellis** (Xiang et al., 2025)、**Hunyuan3D-2.1** (Hunyuan3D et al., 2025)、**TripoSG** (Li et al., 2025)、**Hi3DGen** (Ye et al., 2025)）在合成基准上表现亮眼，但面对真实图像时，形状精度和纹理一致性显著退化。它们缺乏对真实世界光照、遮挡和杂乱场景的建模能力。
- **两阶段pipeline方法**（如 MegaPose/FoundationPose + 形状模型）将形状重建与姿态估计解耦，但割裂了二者在物理世界中的内在耦合关系，导致布局预测精度受限。

更重要的是，这些方法普遍采用**单阶段、单一数据源**的训练范式，无法系统性地弥合合成域与真实域之间的鸿沟。

### 核心洞察与动机

本工作提出一个关键认知转向：**借鉴人类视觉中的“熟悉物体”线索，将识别能力转化为3D重建能力**。人类能够从单张照片推断物体的三维结构，并非因为大脑存储了所有物体的精确CAD模型，而是因为我们在大量视觉经验中习得了“形状词汇”——对常见物体类别的几何先验。

SAM 3D 的核心洞察在于：**利用大规模合成数据训练基础形状词汇，再通过半合成与真实数据对齐实现域泛化**。这一思路直接借鉴了大语言模型（LLM）的成功范式——合成预训练建立基础能力，真实数据后训练实现对齐——将其迁移至3D感知领域，从而突破数据壁垒，在自然场景中实现精准的物体几何、纹理与布局预测。

### 本文目标

基于上述洞察，SAM 3D 旨在构建一个从单张自然图像到可组合3D场景的端到端系统，其设计目标包括：

1. **打破3D数据壁垒**：通过人在回路数据引擎（MITL）生成前所未有的真实图像3D标注规模——近100万图像、约314万无纹理网格、约10万有纹理网格。
2. **多阶段训练范式**：采用合成预训练（Iso-3DO）→ 半合成中期训练（RP-3DO）→ 真实数据后训练对齐（MITL-3DO SFT + DPO）的递进策略。
3. **联合预测形状与布局**：两阶段架构先联合预测粗略形状和6D姿态/缩放，再细化几何细节并合成纹理，实现视觉标定的三维重建。

后续章节将依次展开模型架构、数据引擎、训练范式与实验验证，展示SAM 3D如何在真实图像人类偏好测试中取得至少5:1的胜率，并在SA-3DAO基准上将形状F1@0.01从最佳竞争方法的0.1629提升至0.2344（相对提升43.7%）。

## 核心创新

SAM 3D 的核心创新在于系统性地打破了自然图像三维重建的“数据壁垒”，通过借鉴大语言模型的多阶段训练范式，将大规模合成预训练与真实世界对齐有机结合。具体而言，其关键创新体现在三个相互耦合的维度上。

### 1. 从合成到真实的多阶段训练范式

传统图像到3D方法通常局限于单一数据域训练——要么完全依赖合成数据导致真实场景泛化不足，要么受限于稀缺的真实3D标注而难以规模化。SAM 3D 引入了递进式的三阶段训练策略（Figure 4），逐步将模型暴露于复杂度递增的数据与模态中：

- **阶段1：合成预训练（Iso-3DO）**：在孤立物体合成数据上建立基础形状词汇，学习从单张图像到3D形状、姿态的通用映射能力。
- **阶段1.5：半合成中期训练（RP-3DO）**：引入包含飞越遮挡（Flying Occlusion）、物体交换（Object Swap）等增强的半合成数据，弥合孤立物体与真实场景之间的域差距。
- **阶段2：真实数据后训练对齐**：依次在人在回路标注数据（MITL-3DO）和3D艺术家精标数据（Art-3DO）上进行监督微调（SFT），并通过直接偏好优化（DPO）实现人类偏好对齐。

这一范式的有效性在消融实验中得到严格验证：逐步添加各训练阶段后，形状 F1@0.01 从仅合成预训练的 0.1349 单调提升至完整管线的 0.2344（Table 4）。剔除任一真实数据阶段（MITL-3DO、Art-3DO）或 DPO 对齐步骤均导致形状指标显著下降（Table 7），证明各阶段贡献不可替代。

### 2. 人在回路与模型在回路的数据引擎

SAM 3D 突破了传统依赖3D艺术家直接创建网格的标注瓶颈，设计了人在回路（Human-in-the-Loop）与模型在回路（Model-in-the-Loop）协同的数据采集管线（Figure 5），将标注任务分解为三个子任务：

- **阶段1**：标注者选择图像中的目标物体。
- **阶段2**：模型集成生成 N=8 个候选3D形状，人类标注者从中选择最优匹配并评分；未达质量阈值 α 的候选成为负样本，用于后续偏好对齐。
- **阶段3**：标注者在2.5D场景中调整选定模型的6D姿态，困难案例路由给专业3D艺术家。

该引擎的核心洞察在于：普通标注者无法直接创建3D真值，但能够可靠地判别和筛选模型生成的候选结果。这一设计使数据采集规模达到前所未有的水平——近100万张图像、约314万个无纹理网格和约10万个有纹理网格。数据引擎的迭代运行持续提升模型能力：历史Elo评分呈近线性增长，400点Elo差距对应10:1的偏好胜率（Figure 10）。

### 3. 联合形状-姿态预测与两阶段细化架构

与主流方法将形状重建和姿态估计分离处理的策略不同，SAM 3D 采用两阶段联合架构（Figure 2）：

- **Geometry Model**（1.2B参数，Mixture-of-Transformers架构）：基于条件流匹配（CFM）在 $64^3$ 体素空间直接建模联合分布 $p(O, R, t, s \mid I, M)$，同时去噪输出粗略形状 $O$、6D旋转 $R$、平移 $t$ 和缩放 $s$。这一联合预测设计使模型能够利用形状与姿态之间的互信息，在 Aria Digital Twin 布局基准上将 ADD-S@0.1 从最佳管线方法的 0.5992 提升至 0.7673（Table 3），相对增益达28%。
- **Texture & Refinement Model**（600M参数稀疏流变换器）：以粗略形状 $O$ 为条件，建模 $p(S, T \mid I, M, O)$，从图像线索中细化几何细节并合成纹理。两阶段设计使模型先建立全局结构约束，再聚焦局部细节生成。

架构层面的关键消融包括：标准化6D连续旋转参数化相比四元数将ICP旋转误差从17.96°降至14.59°（Table 10）；深度感知VAE（Depth-VAE）相比无深度VAE显著提升PSNR、SSIM和LPIPS（Table 11）；快捷蒸馏将25步推理压缩至4步而不显著损失质量。

### 方法对比定位

相较于同期前沿方法，SAM 3D 的差异化优势体现在：

| 维度 | 主流方法 | SAM 3D |
|------|---------|--------|
| 训练数据 | 合成数据为主，真实数据有限 | 合成→半合成→真实三阶段递进，人在回路数据引擎 |
| 标注范式 | 3D艺术家直接创建或纯模型生成 | 人类筛选+模型生成协同，困难样本路由专家 |
| 架构设计 | 单阶段形状生成，布局分离处理 | 两阶段联合形状-姿态预测+纹理细化 |
| 对齐策略 | 无偏好对齐或仅SFT | SFT+DPO完整偏好对齐管线 |

在真实图像人类偏好测试中，SAM 3D 以至少5:1的胜率显著优于 **Trellis**（Xiang et al., 2025）、**Hunyuan3D-2.1**（Hunyuan3D et al., 2025）和 **MIDI**（Huang et al., 2025）（Figure 8）。在 SA-3DAO 基准上，F1@0.01 从最佳竞争方法 **Hi3DGen**（Ye et al., 2025）的 0.1629 提升至 0.2344，相对提升43.7%（Table 2）。

## 整体框架

SAM 3D 的目标是将单张 RGB 自然图像中的物体转化为可组合的三维场景——对每个目标物体同时预测其几何形状、表面纹理以及在世界坐标系中的六自由度布局（旋转、平移、缩放），从而实现完整的场景重建（Figure 1）。

![[assets/figures/papers/paper_list_l2_https_arxiv_org_abs_2511_16624/figures/001_Figure_1.jpg]]
*Figure 1: SAM 3D converts a single image into a composable 3D scene made of individual objects. Our method predicts per-object geometry, texture, and layout, enabling full scene reconstruction. Bottom: high-quality 3D assets recovered for each object*

为实现这一目标，SAM 3D 采用**两阶段级联架构**（Figure 2）。第一阶段由 **Geometry Model** 负责，它接收输入图像 $I$ 和目标掩码 $M$，通过条件流匹配建模联合分布 $p(O, R, t, s \mid I, M)$，在 $64^3$ 体素空间中生成粗略形状 $O$，并直接去噪输出 6D 旋转 $R$、平移 $t$ 和缩放 $s$。第二阶段由 **Texture & Refinement Model** 承接，它以第一阶段输出的粗略形状 $O$ 为条件，学习分布 $p(S, T \mid I, M, O)$，融合图像线索对几何细节进行细化，并合成纹理 $T$，最终输出精细形状 $S$ 与纹理。

![[assets/figures/papers/paper_list_l2_https_arxiv_org_abs_2511_16624/figures/002_Figure_2.jpg]]
*Figure 2: SAM 3D architecture. (top) SAM 3D first predicts coarse shape and layout with the Geometry model; (right) the mixture of transformers architecture apply a two-stream approach with information sharing in the multi-modal self-attention layer. (bottom) The voxels predicted by the Geometry model are passed to the Texture & Refinement model, which adds higher resolution detail and textures*

两个模型共享一个基于 DINOv2 的视觉编码器，该编码器同时提取裁剪目标区域和全图的特征，为模型提供局部细节与全局上下文。Geometry Model 采用 **1.2B 参数的混合变换器（Mixture-of-Transformers, MoT）** 架构，通过双流设计在多模态自注意力层中实现信息共享；Texture & Refinement Model 则使用 **600M 参数的稀疏潜在流变换器**，在共享的 VAE 潜在空间中操作。最终的潜在表示可通过分别训练的网格解码器 $D_m$ 或 3D 高斯泼溅解码器 $D_g$ 转换为不同下游任务所需的表示形式。

整个系统的训练遵循**LLM 式的多阶段递进范式**（Figure 4），从大规模合成数据预训练起步，逐步引入半合成数据中训练，最终在真实数据上进行后训练对齐（SFT + DPO）。这一范式的核心在于打破 3D 的“数据壁垒”：自然图像与 3D 真实标注配对的数据极度稀缺，而 SAM 3D 通过**人在回路/模型在回路（MITL）的数据引擎**（Figure 5）持续生成高质量标注——标注者从模型生成的多个候选（N=8）中选择最优网格并标注姿态，困难案例则路由给专业 3D 艺术家处理。该引擎以迭代方式运行：当前最优模型 $q(S, T, R, t, s \mid I, M)$ 作为 API 输出候选，人类反馈产生正样本 $D^+$ 和偏好信号，进而驱动模型的 SFT 与 DPO 更新，形成数据质量与模型能力的正向循环。

![[assets/figures/papers/paper_list_l2_https_arxiv_org_abs_2511_16624/figures/004_Figure_4.jpg]]
*Figure 4: SAM 3D training paradigm. We employ a multi-stage pipeline incrementally exposing the model to increasingly complex data and modalities*

这一设计使得 SAM 3D 能够将识别能力转化为 3D 重建能力：合成预训练阶段建立基础形状词汇，半合成与真实数据对齐阶段实现域泛化，最终在遮挡、杂乱的真实场景中实现视觉标定的三维重建。

### 补充图表

![[assets/figures/papers/paper_list_l2_https_arxiv_org_abs_2511_16624/figures/020_Figure_15.jpg]]
*Figure 15: Reward model data recovery pipeline. The diagram shows how we use reward mdoels to increase N in best-of-N search to improve the chance of a successful annotation on challenging tail inputs. We use both a VLM and also DPO implicit reward as reward models*

## 核心模块与公式推导

SAM 3D 采用两阶段生成架构，将单张图像重建为可组合的3D场景。第一阶段由 **Geometry Model** 联合预测物体的粗略形状与6D布局参数；第二阶段由 **Texture & Refinement Model** 在粗略形状基础上细化几何细节并合成纹理。两个阶段共享 **DINOv2** 编码器提取的视觉特征，并通过共享潜在空间的 **3D VAE 解码器** 输出网格或3D高斯泼溅。

### 2.1 视觉编码器

模型使用 DINOv2 作为骨干编码器，从两组图像对中提取特征：**裁剪目标区域** 提供局部细节，**全图** 提供全局上下文。这种双视角编码策略使模型既能感知物体的精细结构，又能理解其在场景中的空间关系，为后续的形状与布局联合预测奠定基础。

### 2.2 Geometry Model

Geometry Model 建模条件分布 $p(O, R, t, s \mid I, M)$，其中 $O \in \mathbb{R}^{64^3}$ 为粗略形状体素，$R \in \mathbb{R}^6$ 为标准化6D连续旋转参数化，$t \in \mathbb{R}^3$ 为平移向量，$s \in \mathbb{R}$ 为缩放因子，$I$ 为输入图像，$M$ 为目标分割掩码。

该模型采用 **混合变换器（Mixture-of-Transformers, MoT）** 架构，参数量为1.2B。MoT 通过双流设计处理多模态信息：一条流处理形状体素，另一条流处理布局参数，在 **多模态自注意力层** 中实现信息共享。这种设计使形状预测与姿态估计能够相互引导——形状的对称性等几何属性可为旋转估计提供约束，而姿态信息则可帮助消除形状预测中的歧义。

训练采用 **条件流匹配（Conditional Flow Matching, CFM）** 框架，对四个模态分别建模速度场。CFM 损失函数为：

$$\mathcal{L}_{\mathrm{CFM}} = \sum_{m \in \mathcal{M}} \lambda_m \mathbb{E} \left[ \| \mathbf{v}^m - \mathbf{v}_\theta^m(\mathbf{x}_\tau^m, c, \tau) \|^2 \right]$$

其中 $\mathcal{M} = \{O, R, t, s\}$ 为四个模态的集合，$\mathbf{v}^m$ 为模态 $m$ 的真实速度场，$\mathbf{v}_\theta^m$ 为模型预测的速度场，$\mathbf{x}_\tau^m$ 为时间步 $\tau$ 的噪声化样本，$c$ 为条件信息（图像特征与掩码），$\lambda_m$ 为各模态的权重系数。该目标函数驱动模型学习从噪声分布到目标分布的最优传输路径。

### 2.3 Texture & Refinement Model

Texture & Refinement Model 建模条件分布 $p(S, T \mid I, M, O)$，其中 $S$ 为细化后的形状，$T$ 为纹理信息。该模型以 Geometry Model 输出的粗略形状 $O$ 为条件，通过 **600M参数的稀疏潜在流变换器** 在共享的 VAE 潜在空间中操作：首先将粗略形状编码为潜在表示，再通过流匹配过程逐步去噪，同时整合图像中的纹理线索，最终解码为高保真的带纹理网格。

### 2.4 3D 解码器

两个模型共享同一 VAE 编码器，因此共享结构化的潜在空间。该潜在表示可通过分别训练的解码器 $D_m$（网格解码器）和 $D_g$（高斯泼溅解码器）灵活转换为不同下游表示，支持渲染、仿真等多样的应用需求。

### 2.5 偏好对齐：Flow Matching DPO

在真实数据后训练阶段，SAM 3D 引入 **直接偏好优化（DPO）** 将人类偏好信号注入流匹配框架。给定优选样本 $w$ 和次选样本 $l$，DPO 损失函数为：

$$\mathcal{L}_{\mathrm{DPO}} = -\mathbb{E} \left[ \log \sigma \left( -\beta T w(\tau) \cdot \Delta \right) \right]$$

其中 $\sigma$ 为 sigmoid 函数，$\beta$ 控制偏好强度，$T$ 为总时间步数，$w(\tau)$ 为时间步权重。核心信号 $\Delta$ 定义为当前策略 $\theta$ 与参考策略 $\mathrm{ref}$ 在优选和次选样本上的速度场预测误差之差：

$$\Delta = \| \mathbf{v}^w - \mathbf{v}_\theta(x_\tau^w, c, \tau) \|_2^2 - \| \mathbf{v}^w - \mathbf{v}_{\mathrm{ref}}(x_\tau^w, c, \tau) \|_2^2 - \left( \| \mathbf{v}^l - \mathbf{v}_\theta(x_\tau^l, c, \tau) \|_2^2 - \| \mathbf{v}^l - \mathbf{v}_{\mathrm{ref}}(x_\tau^l, c, \tau) \|_2^2 \right)$$

直观上，当模型对优选样本的预测优于参考模型、且对次选样本的预测劣于参考模型时，$\Delta$ 为负，损失降低，模型被鼓励向人类偏好方向更新。

### 2.6 快捷蒸馏

为加速推理，SAM 3D 采用快捷蒸馏将25步采样压缩至4步。蒸馏损失 $\mathcal{L}_S(\theta)$ 同时包含标准流匹配项和一致性项：

$$\mathcal{L}_S(\theta) = \mathbb{E}_{\mathbf{x}_0 \sim \mathsf{N}(0,I), \tau \downarrow \sim p(x,d)} \Big[ \| \mathbf{v} - \mathbf{v}_\theta(x_\tau, c, \tau, d=0) \|^2 + \| \mathbf{v}_{\mathrm{consistency}} - \mathbf{v}_\theta(x_\tau, c, \tau, 2d) \|^2 \Big]$$

第一项为标准流匹配目标（$d=0$），第二项为一致性目标（步长为 $2d$），强制模型在更大步长下仍保持预测一致性，从而实现少步高质量的生成。

### 补充图表

![[assets/figures/papers/paper_list_l2_https_arxiv_org_abs_2511_16624/figures/006_Figure_5.jpg]]
*Figure 5: Life of an example going through the data collection pipeline. We streamline annotation by breaking it into subtasks: annotators first choose target objects (Stage 1); rank and select 3D model candidates (Stage 2); then pose these models within a 2.5D scene (Stage 3). Stages 2 and 3 use model-in-the-loop*

## 实验与分析

### 核心定量结果：形状重建

SAM 3D 在 SA-3DAO 基准（由 3D 艺术家标注的真实几何形状）上取得了显著领先的形状重建精度。如表 2 所示，其 F1@0.01 达到 0.2344，相比此前最佳方法 **Hi3DGen**（Ye et al., 2025）的 0.1629 提升了 43.7%（+0.0715）；Chamfer 距离降至 0.0400，相比 Hi3DGen 的 0.0937 降低了 57.3%。这表明 SAM 3D 生成的形状与艺术家级真实标注的吻合度远高于现有方法。

在无几何真实标注的 ISO3D 基准上，SAM 3D 在 ULIP 感知相似度指标上达到 0.1488，与 **TripoSG**（Li et al., 2025）的 0.1529 基本持平（-0.0041），证明其在孤立物体图像上的重建质量与现有前沿方法相当。

定性对比（图 6）进一步印证了上述结论：相比 **Trellis**（Xiang et al., 2025）、**Hunyuan3D-2.1**（Hunyuan3D et al., 2025）、**Direct3D-S2**（Wu et al., 2025a）和 Hi3DGen，SAM 3D 在真实场景中恢复的物体形状更贴近艺术家创建的真实网格，尤其在遮挡和杂乱背景下优势明显。

### 核心定量结果：布局预测

SAM 3D 联合预测物体形状与 6D 布局（旋转、平移、缩放），在场景级重建任务中展现出压倒性优势。如表 3 所示，在 Aria Digital Twin 数据集上，SAM 3D 的 ADD-S @ 0.1 达到 0.7673，相比两阶段 pipeline 方法（HY3D-2.0 + FoundationPose）的 0.5992 提升了 28.1%（+0.1681），相比联合生成模型 **MIDI**（Huang et al., 2025）的 0.3701 更是提升超过一倍。这一结果表明，端到端联合预测形状与布局的策略显著优于“先形状后姿态”的分步方案。

在 SA-3DAO 布局子集上，SAM 3D 同样以 0.7232 的 ADD-S @ 0.1 大幅领先 pipeline 方法（0.5562）和 MIDI（0.3891）。

### 核心定性结果：人类偏好测试

在真实图像的人类偏好评估中（图 8），SAM 3D 在场景级和物体级重建上均取得了至少 5:1 的头对头胜率，显著优于 Trellis、Hunyuan3D-2.1 和 MIDI。这意味着人类评估者在绝大多数情况下认为 SAM 3D 的重建结果更符合真实场景的几何、纹理和空间布局。

纹理偏好测试（图 9）采用了公平对比设计：所有方法均使用 SAM 3D 生成的几何形状作为输入，仅比较纹理生成能力。在此设定下，SAM 3D 的纹理质量仍显著优于 Trellis、Hunyuan3D-2.1 和 **Unitex**（Liang et al., 2025b），证明其纹理模型独立具备竞争力。

### 多阶段训练的累积贡献

表 4 的消融实验揭示了多阶段训练范式中每个环节的累积增益。从合成预训练（Iso-3DO）基线开始，逐步添加中训练（RP-3DO）、MITL-3DO SFT、MITL-3DO DPO、Art-3DO SFT 和 Art-3DO DPO，形状 F1@0.01 从 0.1349 单调提升至 0.2344，总增幅达 73.8%。纹理质量同样随阶段增加而持续改善，各阶段间的胜率（WR）均为正值。

训练阶段剔除实验（表 7）进一步证实了各真实数据阶段的不可替代性：单独移除 MITL-3DO、Art-3DO 或 DPO 训练阶段均导致形状指标的明显下降，说明合成数据预训练虽奠定基础，但真实世界的泛化能力依赖于人在回路数据（MITL-3DO）和艺术家数据（Art-3DO）的联合对齐。

### 数据引擎的迭代增益

图 10 展示了数据引擎持续运行的效果。模型 Elo 评分随引擎迭代周期（约每 3 周一个检查点）近乎线性增长，400 点 Elo 差异对应 10:1 的偏好胜率。扩展 MITL-3DO 数据规模（图 10b）虽呈现边际递减趋势，但整体仍带来正向增益，验证了人在回路数据引擎的长期价值。

### 纹理与细化模型的关键设计

图 17 的消融表明，光照增强、RP-3DO 半合成数据、后训练数据（MITL 和 AES 偏好数据）以及 DPO 对齐均对纹理质量有显著正面贡献。去除任一组件的模型在人类偏好测试中均被完整模型显著击败，偏好率差距明确。

### 旋转表示与 VAE 设计

旋转表示的消融（表 10）显示，标准化 6D 连续参数化相比四元数和未归一化 6D 旋转，将 ICP 旋转误差从 17.96° 降至 14.59°，验证了该表示在流匹配框架中的有效性。

深度感知 VAE（Depth-VAE）的消融（表 11）表明，相比无深度特征的 VAE，Depth-VAE 在 PSNR、SSIM 和 LPIPS 上均有提升；进一步扩大训练数据则显著增强了重建质量，说明深度线索的引入和规模化训练是提升几何细节的关键。

### 失败模式与限制

尽管取得了显著性能提升，SAM 3D 仍存在若干已知限制。首先，形状分辨率受限于 64³ 体素网格，对于手部、面部等精细结构可能产生感知伪影，未来需通过更高分辨率、超分或隐式表示突破这一瓶颈。其次，当前模型仅能逐个预测物体，缺乏对多物体间物理交互（接触、稳定性、穿透、共面）的推理能力，场景级重建的全局一致性仍有提升空间。此外，纹理预测未考虑姿态信息，对于具有旋转对称性的物体可能产生方向错误的纹理。在复杂多物体场景中，布局对齐精度目前依赖后处理优化，端到端的联合推理是下一步方向。

### 奖励模型与尾部类别提升

使用奖励模型扩展 best-of-N 搜索（N=50）恢复的 SFT 数据（表 12），有效提升了尾部类别和挑战性数据集（如 Epic Kitchens）上的 Chamfer 距离和 F1 指标，表明通过模型自身筛选高质量伪标签可以进一步挖掘数据引擎的潜力，尤其对长尾分布场景具有实用价值。

### 补充图表

![[assets/figures/papers/paper_list_l2_https_arxiv_org_abs_2511_16624/figures/009_Table_2.jpg]]
*Table 2: 3D shape quantitative comparison to competing image-to-3D methods, including Trellis (Xiang et al., 2025), HY3D-2.1 (Hunyuan3D et al., 2025), HY3D-2.0 (Team, 2025), Direct3D-S2 (Wu et al., 2025a), TripoSG (Li et al., 2025), Hi3DGen (Ye et al., 2025). SA-3DAO shows metrics that measure accuracy against GT geometry; ISO3D (Ebert, 2025) has no geometric GT and so we show perceptual similarities between 3D and input images (ULIP (Xue et al., 2023) and Uni3D (Zhou et al., 2023)). TripoSG uses a significantly higher mesh resolution, which is rewarded in perceptual metrics*

![[assets/figures/papers/paper_list_l2_https_arxiv_org_abs_2511_16624/figures/010_Figure_8.jpg]]
*Figure 8: Preference comparison on scene-level and object-level reconstruction. Numbers indicate human preference rates. Objects comparisons are done on textured meshes. SAM 3D is significantly preferred over others on all fronts*

![[assets/figures/papers/paper_list_l2_https_arxiv_org_abs_2511_16624/figures/011_Table_3.jpg]]
*Table 3: 3D layout quantitative comparison to competing layout prediction methods on SA-3DAO and Aria Digital Twin (Pan et al., 2023). SAM 3D significantly outperforms both pipeline approaches used in robotics (Labbé et al., 2022; Wen et al., 2024) and joint generative models (MIDI (Huang et al., 2025)). Most SA-3DAO scenes only contain one object so we do not show MIDI results that require multi-object alignment. The metrics measure bounding box overlap, rotation error, and chamfer-like distances normalized by object diameter*

![[assets/figures/papers/paper_list_l2_https_arxiv_org_abs_2511_16624/figures/013_Table_4.jpg]]
*Table 4: Cascading improvements from multi-stage training on 3D shape and texture. For texture, we report win rates (WR) between each row and the row above it*

![[assets/figures/papers/paper_list_l2_https_arxiv_org_abs_2511_16624/figures/024_Table_7.jpg]]
*Table 7: Training stage knockout. The impact of training on MITL and 3D artist-generated data*

![[assets/figures/papers/paper_list_l2_https_arxiv_org_abs_2511_16624/figures/014_Figure_10.jpg]]
*Figure 10: Data engine with additional iterations. The plots show Elo scores of different models; a 400 point Elo difference corresponds to 10:1 odds in a preference test. Models were (a) checkpoints around 3 weeks apart, indicating cumulative improvements as we scale and add different stages and (b) post-trained (SFT) using expanded training data*

![[assets/figures/papers/paper_list_l2_https_arxiv_org_abs_2511_16624/figures/028_Table_10.jpg]]
*Table 10: Rotation representation. Ablation on the representation used during pretraining. We report Chamfer distances and ICP rotation error*

## 方法谱系与知识库定位

### 1. 方法谱系：从单阶段生成到两阶段联合推理

SAM 3D 在图像到三维重建的演进脉络中占据了一个独特位置，其核心贡献在于将**布局预测（6D姿态与缩放）与形状生成深度融合**，打破了此前“先形状后姿态”的两阶段工程管线与“仅生成形状”的单阶段模型之间的方法论鸿沟。

**与单阶段形状生成方法的对比。** 当前主流的图像到三维资产生成方法——如 **Trellis**（Xiang et al., 2025）、**Hunyuan3D-2.1**（Hunyuan3D et al., 2025）、**Direct3D-S2**（Wu et al., 2025a）、**TripoSG**（Li et al., 2025）和 **Hi3DGen**（Ye et al., 2025）——均聚焦于从单张图像生成独立的物体三维形状与纹理，但**不显式预测物体在场景中的空间布局**。这些方法在孤立物体图像（如ISO3D基准）上表现优异，TripoSG在ULIP感知相似度指标上甚至略优于SAM 3D（0.1529 vs. 0.1488）。然而，当面对自然场景中的多物体图像时，这些方法缺乏对物体间空间关系的建模能力，无法直接输出可组合的三维场景。

**与两阶段工程管线的对比。** 机器人领域常用的方案是将前沿形状生成模型（如Hunyuan3D-2.0）与姿态估计器（如**MegaPose**或**FoundationPose**）串联，形成“先重建形状，再估计姿态”的级联系统。SAM 3D 在Aria Digital Twin布局基准上的联合预测结果（ADD-S@0.1 = 0.7673）显著优于该管线方案（HY3D-2.0 + FoundationPose = 0.5992），相对提升达28.1%。这一差距揭示了级联方案的瓶颈：形状生成阶段的误差会不可逆地传播到姿态估计阶段，而联合建模允许两个子任务共享视觉特征并相互约束。

**与场景重建方法的对比。** **MIDI**（Huang et al., 2025）是少数同时预测形状与布局的生成式方法，但其布局精度在SA-3DAO上（ADD-S@0.1 = 0.3370）远低于SAM 3D（0.7232）。这表明，SAM 3D通过大规模合成预训练习得的形状先验，为其布局预测提供了更强的几何约束。

### 2. 知识库定位：LLM训练范式的三维迁移

SAM 3D的方法论创新并非孤立产生，而是**将大语言模型（LLM）的多阶段训练与人在回路对齐范式系统性地迁移到三维视觉领域**。这一迁移体现在三个层面：

**数据策略的范式迁移。** SAM 3D的四阶段训练策略——合成预训练（Iso-3DO）→ 半合成中期训练（RP-3DO）→ 真实数据监督微调（MITL-3DO, Art-3DO SFT）→ 偏好对齐（DPO）——直接对应了LLM训练中的预训练→中期训练→SFT→RLHF/DPO的经典配方。这一策略的核心洞察在于：合成数据提供了**基础的形状词汇**（shape vocabulary），使得模型在接触真实数据之前已经习得了三维几何的基本结构；而真实数据后训练则通过**视觉标定**（visually grounded annotation）将这些词汇与自然图像中的物体实例对齐，实现域泛化。

**人在回路数据引擎。** SAM 3D的MITL（Model-in-the-Loop）标注管线借鉴了LLM领域通过人类偏好数据迭代提升模型能力的思路。其核心设计——从模型生成的N=8个候选形状中由人类标注者选择最佳匹配并标注姿态——本质上是一种**best-of-N搜索与人类反馈的结合**。这一设计解决了三维标注的根本性困难：普通标注者无法从零创建三维网格，但可以在模型生成的候选中进行视觉判断。困难案例则路由给专业三维艺术家，形成了“模型生成→众包筛选→专家兜底”的分级标注体系。该引擎产出了前所未有的数据规模：近100万张图像、约314万个无纹理网格和约10万个有纹理网格。

**偏好对齐的几何化。** SAM 3D将DPO（Direct Preference Optimization）从文本生成领域适配到三维流匹配框架中，其损失函数形式为：

$$\mathcal{L}_{\mathrm{DPO}} = -\mathbb{E} \left[ \log \sigma \left( -\beta T w(\tau) \cdot \Delta \right) \right]$$

其中Δ为当前策略与参考策略对优选/次选样本的速度场预测误差之差。这一适配使得模型能够直接从人类偏好比较中学习，而非仅依赖绝对真值监督。

### 3. 适用边界与局限

尽管SAM 3D在自然场景三维重建上取得了显著突破，其方法仍存在若干明确的适用边界：

**分辨率瓶颈。** 几何模型在$64^3$的体素空间中进行流匹配生成，这一分辨率对于手部、面部等精细结构可能产生感知伪影。虽然纹理与细化模型在此基础上增加了高频细节，但基础体素网格的表达能力上限构成了几何精度的硬约束。未来可通过更高分辨率、超分网络或隐式表示（如NeRF、3D Gaussian Splatting的潜在编码）来突破这一瓶颈。

**物理交互缺失。** 当前模型逐个预测物体，缺乏对多物体间物理交互（接触、稳定性、穿透、共面）的推理能力。在SA-3DAO和Aria Digital Twin的评估中，布局指标衡量的是单物体姿态精度，而非场景级物理一致性。多物体联合预测与物理感知的损失函数设计是下一步方向。

**纹理的方向歧义。** 纹理预测模块未显式考虑物体姿态信息，对于具有旋转对称性的物体（如球、圆柱体），可能产生方向错误的纹理映射。这一问题源于纹理生成与姿态预测的解耦设计。

**复杂场景的对齐精度。** 在密集多物体场景中，布局对齐精度仍有提升空间，当前依赖后处理优化步骤。严重遮挡或极小物体区域的失败模式尚未被系统性地表征和分析。

### 4. 开放问题

1. **新物体类别的泛化边界。** 模型在合成预训练和真实数据后训练中均未出现的新物体类别上表现如何？其泛化能力是否依赖于合成数据中形状词汇的覆盖度，还是可以通过视觉特征的迁移实现零样本重建？

2. **遮挡与极小物体的鲁棒性。** 在严重遮挡或目标仅占图像极小区域的场景中，模型的失败模式有哪些？是否可以通过数据增强（如Flying Occlusion）或注意力机制的改进来提升鲁棒性？

3. **人在回路引擎的自动化。** 质量阈值α的课程如何自动设置？能否通过奖励模型进一步放大专家策略的增益，减少对三维艺术家的依赖？使用奖励模型扩展best-of-N搜索（N=50）的初步实验已显示出对尾部类别和挑战性数据集的正面影响，但这一方向的潜力远未穷尽。

4. **分辨率与效率的权衡。** 可否通过部件式生成或隐式表示来突破$64^3$体素的分辨率瓶颈，同时保持流匹配的推理速度？快捷蒸馏（Shortcut Distillation）已将推理步数从25步压缩至4步，但其损失函数：

   $$\mathcal{L}_S(\theta) = \mathbb{E}_{\mathbf{x}_0 \sim \mathsf{N}(0,I), \tau \downarrow \sim p(x,d)} \Big[ \| \mathbf{v} - \mathbf{v}_\theta(x_\tau, c, \tau, d=0) \|^2 + \| \mathbf{v}_{\mathrm{consistency}} - \mathbf{v}_\theta(x_\tau, c, \tau, 2d) \|^2 \Big]$$

   在高分辨率下的保真度仍需验证。

5. **多物体物理一致性。** 多物体场景的联合推理应如何设计以避免穿模并保持全局物理一致性？是否需要引入物理仿真器作为可微分损失组件？

6. **视频数据的自监督扩展。** 是否可以利用大规模视频数据进一步自监督预训练，增强模型对时序一致性和遮挡关系的理解？视频中的多视角信息天然提供了三维几何的监督信号，这可能成为突破当前数据瓶颈的下一个杠杆点。

## 原文 PDF

![[paperPDFs/CVPR_2026/SAM_3D_3Dfy_Anything_in_Images.pdf]]