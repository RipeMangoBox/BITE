---
title: "Move-in-2D: 2D-Conditioned Human Motion Generation"
type: paper
paper_level: A
venue: CVPR
year: 2025
pdf_ref: paperPDFs/CVPR_2025/Move_in_2D_2D_Conditioned_Human_Motion_Generation.pdf
aliases:
- M2
- Move-in-2D
tags:
- CVPR_2025
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
- topic/generative_models_diffusion
core_operator: 引入二维场景图像作为附加条件，并与文本提示共同送入基于Transformer的扩散模型，通过上下文条件化（in-context conditioning）将两种模态对齐到共享标记空间。
primary_logic: 利用类似大语言模型中的上下文学习策略，将场景图像（经DINO编码）和文本（经CLIP编码）统一为一组条件标记，直接注入扩散Transformer的生成过程，使模型学会生成既符合文本描述又能在二维图像平面自然投影的运动序列，从而绕开三维重建。
claims:
- 所提方法在HiC-Motion测试集上取得最低FID 44.639和最高精度0.661，并较仅含场景条件的变体精度提升37%。
- 在VLM自动评估中，本方法在场景对齐（3.55）、文本对齐（2.70）和姿态质量（2.85）方面均优于所有基线。
- 消融实验证实，对文本和场景使用In-Context条件化、对时间步使用AdaLN的组合可实现最佳性能。
- HiC-Motion测试集 (957样本) 上 Accuracy (运动分类精度) = 0.661 (Ours)
---

# Move-in-2D: 2D-Conditioned Human Motion Generation

> [!tip] 核心洞察
> 利用类似大语言模型中的上下文学习策略，将场景图像（经DINO编码）和文本（经CLIP编码）统一为一组条件标记，直接注入扩散Transformer的生成过程，使模型学会生成既符合文本描述又能在二维图像平面自然投影的运动序列，从而绕开三维重建。

| 字段 | 内容 |
|------|------|
| 中文题名 | Move-in-2D：基于二维场景条件的人体运动生成 |
| 英文题名 | Move-in-2D: 2D-Conditioned Human Motion Generation |
| 会议/期刊 | CVPR 2025 |
| Links | [Project](https://hhsinping.github.io/Move-in-2D) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction #topic/generative_models_diffusion |
| Method | Move-in-2D |
| Dataset | HiC-Motion测试集 |

> [!tip] 效果简介
> - HiC-Motion测试集 (957样本) 上，Accuracy (运动分类精度) 0.661 (Ours) vs 0.482 (Ours-scene, 估算) (+37%相对提升)。
> - HiC-Motion测试集 上，FID 44.639 (Ours) vs MDM+ (具体值未列出，但本方法最低) (最佳 (lowest))；VLM总分 (0-15) 9.10 vs 其余方法均更低 (HUMANISE等) (最高 (highest))。

## 概述

**核心问题**：现有的人体运动生成方法要么仅依赖文本提示而缺乏场景感知，要么需要昂贵的三维场景重建，无法直接根据常见的二维背景图像生成与之空间兼容的运动序列。

**核心方案**：Move-in-2D 提出将二维场景图像与文本提示共同作为条件，注入基于 Transformer 的扩散模型。其关键创新在于采用**上下文条件化**策略——受大语言模型中上下文学习的启发，将 DINO 编码的场景视觉标记与 CLIP 编码的文本标记统一到共享的标记空间中，使模型无需三维重建即可学会生成既符合文本描述、又能在二维图像平面上自然投影的人体运动。

**方法定位**：该方法在条件模态上区别于仅用文本的 **MDM**（Tevet et al., ICLR 2023）和 **MLD**（Chen et al., CVPR 2023），在场景表征上区别于依赖三维点云的 **SceneDiff**（Huang et al., CVPR 2023）和 **HUMANISE**（Wang et al., NeurIPS 2022）。它额外预测相机平移参数 $\pi \in \mathbb{R}^3$ 以支持从 SMPL 空间到图像平面的透视投影，并采用文本与场景的联合分类器自由引导来增强条件对齐。

**主要结果**：在 HiC-Motion 测试集上，Move-in-2D 取得最低 FID 44.639 和最高运动分类精度 0.661，较仅含场景条件的变体精度相对提升 37%；在 VLM 自动评估中，场景对齐（3.55）、文本对齐（2.70）和姿态质量（2.85）均优于所有基线。

**局限与开放问题**：框架未控制生成运动中的相机运动，两阶段视频生成流程尚未端到端联合优化，且仅支持单人运动。未来方向包括引入相机运动控制、端到端联合训练、多人场景扩展，以及在更开放的场景-文本组合下验证泛化边界。

## 背景与动机

人体运动生成是计算机视觉与图形学领域的核心问题之一，其目标是根据给定的控制信号合成自然、多样的人体动作序列。近年来，随着扩散模型在生成任务中的突破性进展，文本条件运动生成取得了显著进步——用户仅需提供自然语言描述，即可获得对应的三维人体运动。然而，**现有方法面临一个关键瓶颈：它们要么仅依赖文本提示，缺乏对物理场景的感知能力；要么需要完整的三维场景重建作为条件输入，而三维重建本身获取成本高昂且易引入误差**。这使得现有方法无法直接根据日常随处可见的二维背景图像生成与之兼容的运动序列。

具体而言，当前主流范式可分为两类。一类是以 **MDM**（Tevet et al., ICLR 2023）和 **MLD**（Chen et al., CVPR 2023）为代表的纯文本条件方法，它们能够生成语义丰富的运动，但完全忽略场景约束——生成的动作可能与实际场景发生穿透、悬空或尺度失配。另一类是以 **SceneDiff**（Huang et al., CVPR 2023）和 **HUMANISE**（Wang et al., NeurIPS 2022）为代表的场景感知方法，它们将三维点云或三维场景表示作为附加条件，使运动生成具备场景意识，但前提是需要预先获取场景的三维几何信息。在实际应用中，三维重建不仅计算开销大，而且对输入图像质量、视角覆盖和深度估计精度都有较高要求，这严重限制了场景感知运动生成的实用性和可扩展性。

这一缺口催生了一个自然的问题：**能否绕过三维重建，直接从单张二维场景图像出发，生成既符合文本语义、又能在该二维平面上自然投影的运动序列？** 这构成了 Move-in-2D 工作的核心动机。其核心洞察在于：借鉴大语言模型中的上下文学习策略，将场景图像和文本提示统一编码为一组共享的条件标记，直接注入基于 Transformer 的扩散模型，使模型学会在二维图像约束下生成语义一致的运动——从而以极低的输入成本实现场景感知运动生成。

## 核心创新

Move-in-2D 的核心创新在于**将二维场景图像作为附加条件引入人体运动生成**，从而绕开了现有方法对三维场景重建的依赖。这一设计直接回应了一个现实瓶颈：文本条件方法（如 **MDM** (Tevet et al., ICLR 2023)、**MLD** (Chen et al., CVPR 2023)）缺乏场景感知，而场景感知方法（如 **SceneDiff** (Huang et al., CVPR 2023)、**HUMANISE** (Wang et al., NeurIPS 2022)）需要三维点云输入，获取成本高昂。Move-in-2D 仅需单张二维背景图像和文本提示，即可生成在图像平面上投影自然、且语义匹配的运动序列。

为实现这一目标，方法在三个关键“槽位”上做出了改变：

**1. 条件模态：从“文本/三维点云”到“文本 + 二维场景图像”**

现有基线要么仅依赖文本，要么需要文本与三维点云的组合。Move-in-2D 将条件扩展为文本提示 $p$ 与二维场景图像 $s$ 的联合输入。场景图像经 DINO-B 编码为 240 个视觉标记，文本经 CLIP-B 编码为单个全局标记，二者共同构成条件信号。这一改变使模型能够直接从日常的二维图像中理解场景的可供性（affordance），而无需进行显式的深度估计或三维重建。

**2. 条件注入方式：从“交叉注意力/FiLM”到“In-Context Conditioning + AdaLN”**

这是方法层面的关键设计。传统条件扩散模型通常采用交叉注意力或 FiLM 来注入条件信号。Move-in-2D 借鉴大语言模型中的上下文学习策略，将文本标记与场景图像标记统一排列为共享标记空间中的条件序列，直接作为 Transformer 的上下文输入（In-Context Conditioning）。与此同时，扩散时间步 $t$ 则通过 AdaLN 层注入。消融实验（Table 4）证实，这一组合——In-Context 处理文本和场景条件、AdaLN 处理时间步——在 FID（44.639）和 Accuracy（0.661）上均达到最优，优于其他注入方式的排列。

**3. 输出参数：从“仅姿态与朝向”到“额外预测相机平移 $\pi \in \mathbb{R}^3$”**

为支持运动序列在二维图像平面上的自然投影，模型在输出 SMPL 姿态参数和全局朝向之外，额外预测一个相机平移参数 $\pi \in \mathbb{R}^3$。该参数假设透视相机具有固定焦距和内参，用于将 SMPL 空间中的三维点投影到图像平面。这一设计使生成的运动能够适配输入场景图像的视角，而非仅仅在抽象三维空间中生成运动。

**4. 联合分类器自由引导**

在采样阶段，Move-in-2D 对文本和场景条件施加联合分类器自由引导（CFG）：

$$\mathcal{M}_{\mathrm{cfg}} = \mathcal{M}(\mathbf{x}_t | t) + g (\mathcal{M}(\mathbf{x}_t | t, p, s) - \mathcal{M}(\mathbf{x}_t | t))$$

这一公式将无条件输出与文本-场景联合条件输出相结合，引导生成的运动同时对齐文本语义和场景几何约束。训练时以概率 $q=0.1$ 随机丢弃文本和场景条件，以支持 CFG 采样。

**5. 两阶段训练策略**

为解耦相机运动并增强大动态运动生成能力，Move-in-2D 采用两阶段训练：第一阶段在全量 300k 视频数据上训练 600k 迭代；第二阶段在混合数据集（60% 大运动视频 + 40% 固定背景视频，共 150k）上微调 600k 迭代。这一策略有效缓解了原始视频中残余相机移动对运动生成的干扰。

综合来看，Move-in-2D 的创新并非单一技术点的突破，而是通过**条件模态扩展、注入机制重构、输出参数补全和训练策略适配**四个维度的协同改变，首次实现了仅依赖二维场景图像的高质量场景感知运动生成。

## 整体框架

Move-in-2D 的生成管线以一张二维场景图像和一条文本动作描述为输入，输出一段与场景布局兼容、且语义上符合文本指令的三维人体运动序列。该框架的核心设计在于**绕过显式的三维场景重建**，通过将图像与文本统一到共享的标记空间中，使扩散模型直接学习二维投影约束下的运动先验。

### 输入与输出定义

输入由两部分组成：
- **场景图像** $s$：一张包含目标背景的 RGB 图像，作为空间约束的来源。
- **文本提示** $p$：描述期望动作的自然语言短语（如 “a person walking towards the chair”）。

输出为一段长度为 $N=256$ 帧的人体运动序列，每帧包含 SMPL 姿态参数、全局朝向，以及一个额外预测的**相机平移参数** $\pi \in \mathbb{R}^3$。该相机参数假定透视相机具有固定焦距和内参，用于将 SMPL 空间中的三维关节点投影到输入图像的二维平面上，从而建立运动与场景之间的几何对应关系（见 Sec. 4.2）。

### 核心模块与数据流

整个框架由四个关键模块串联构成，数据流向如图 Figure 2 所示：

![[assets/figures/papers/paper_list_l1855_Move_in_2D_2D_Conditioned_Human_Motion_Generation/figures/003_Figure_2.jpg]]
*Figure 2: Overview. The text prompt and background scene image are encoded by the CLIP and DINO encoders, and incorporated into the model via in-context conditioning. The AdaLN layer receives the diffusion timestep as input. Our multi-conditional transformer model then generates a human motion sequence through a diffusion denoising process, aligning the generated motion with both input conditions*

1. **场景图像编码器（DINO-B）**  
   将输入的场景图像（分辨率 $168 \times 280$）编码为 240 个视觉标记，捕获场景的语义与空间布局信息。选择 DINO 而非其他视觉骨干的原因在于其自监督预训练特征对场景结构和物体边界具有良好的保持能力。

2. **文本编码器（CLIP-B）**  
   将文本提示编码为单个全局标记，提供动作语义的高层指导。CLIP 的图文对齐预训练使得该标记天然与视觉概念处于相近的语义空间。

3. **多条件扩散 Transformer**  
   这是生成过程的核心引擎。它由 8 个 Transformer 块构成（隐藏单元 512，前馈层维度 2048，注意力头数 4），接收三个条件信号：
   - **文本标记与场景标记**：通过 **In-Context Conditioning** 策略注入。具体而言，将 CLIP 文本标记与 DINO 场景标记拼接为一组条件标记，直接作为 Transformer 输入序列的一部分，使模型以类似大语言模型上下文学习的方式同时关注两种模态。这种设计避免了交叉注意力或 FiLM 等传统条件注入方式可能引入的模态冲突。
   - **扩散时间步**：通过 **AdaLN（自适应层归一化）** 注入每个 Transformer 块，调节去噪过程的进度。

   模型在扩散去噪过程中逐步从纯噪声恢复出运动序列，同时预测相机平移参数 $\pi$。

4. **两阶段训练策略**  
   为解耦原始视频中的相机运动并增强大动态运动的生成能力，训练分为两个阶段：
   - **第一阶段**：在全量 300k 视频数据上训练 600k 次迭代，建立基础的运动—场景—文本关联。
   - **第二阶段**：在混合数据集（150k 视频，60% 大运动视频 + 40% 固定背景视频）上微调 600k 次迭代。大运动视频中人体在场景内有显著位移，固定背景视频则提供稳定的场景参照，二者混合促使模型区分人体运动与相机运动。

训练采用 Adam 优化器，学习率 $0.0002$，批次大小 128，共 1.2M 次迭代；扩散过程使用 1000 步余弦噪声调度。训练期间以概率 $q=0.1$ 随机丢弃文本和场景条件，以支持采样时的无分类器引导。

### 采样与条件引导

采样阶段应用**联合无分类器引导**，同时对文本条件 $p$ 和场景条件 $s$ 施加引导：

$$\mathcal{M}_{\mathrm{cfg}} = \mathcal{M}(\mathbf{x}_t \mid t) + g \big( \mathcal{M}(\mathbf{x}_t \mid t, p, s) - \mathcal{M}(\mathbf{x}_t \mid t) \big)$$

其中 $\mathcal{M}$ 为去噪网络，$g$ 为引导强度。该公式将无条件输出与双条件输出进行线性外推，增强生成运动与两个输入条件的对齐度（公式 (1)，Sec. 4.2）。

### 与基线方法的差异定位

相较于现有方法，Move-in-2D 在以下关键环节做出了差异化设计：

| 差异维度 | 基线方法 | Move-in-2D |
|---------|---------|------------|
| 条件模态 | 仅文本（**MDM**, Tevet et al., ICLR 2023；**MLD**, Chen et al., CVPR 2023）或文本+三维点云（**SceneDiff**, Huang et al., CVPR 2023；**HUMANISE**, Wang et al., NeurIPS 2022） | 文本提示 + 二维场景图像 |
| 条件注入方式 | 交叉注意力或 FiLM | In-Context Conditioning 统一标记空间 + AdaLN 注入时间步 |
| 输出参数 | 仅 SMPL 姿态与全局朝向 | 额外预测相机平移 $\pi \in \mathbb{R}^3$，支持二维投影 |

这一框架的核心洞察在于：通过将场景图像和文本统一为上下文标记，模型无需昂贵的三维重建即可学习二维平面上的运动兼容性，从而在保持较低获取成本的同时实现场景感知的运动生成。

### 补充图表

![[assets/figures/papers/paper_list_l1855_Move_in_2D_2D_Conditioned_Human_Motion_Generation/figures/001_Figure_1.jpg]]
*Figure 1: 2D-conditioned human motion generation. Given an image representing the target scene and a text prompt describing the desired motion, we generate a motion sequence that aligns with the text description and projects naturally onto the scene image. This generated motion then serves as the control signal for the subsequent video generation tasks*

## 核心模块与公式推导

### 条件编码器

**场景图像编码器**：采用预训练的 DINO-B 模型，将输入场景图像（168×280）编码为 240 个视觉标记。DINO 的自监督预训练特性使其能够捕获场景的语义结构与几何布局，为后续运动-场景对齐提供丰富的视觉上下文。

**文本编码器**：采用 CLIP-B 模型，将文本提示编码为单个全局标记，提取动作语义信息。

两种编码器的输出被统一为一组条件标记（condition tokens），直接注入扩散 Transformer 的生成过程，形成“上下文条件化”（in-context conditioning）机制。

### 多条件扩散 Transformer

模型核心是一个由 8 个 Transformer 块组成的扩散去噪网络，每块包含 512 个隐藏单元、前馈层维度 2048、4 个注意力头。条件注入采用双路径设计：

- **上下文条件化（In-Context Conditioning）**：文本标记与场景视觉标记共享同一标记空间，作为上下文前缀直接拼接到运动序列标记中，通过自注意力机制实现跨模态融合。这借鉴了大语言模型中的上下文学习策略，使模型隐式地学习文本语义与场景几何之间的关联。
- **自适应层归一化（AdaLN）**：扩散时间步 $t$ 通过 AdaLN 层注入，调节各 Transformer 块的归一化参数，使模型感知当前去噪阶段。

消融实验（Table 4）证实，对文本和场景条件使用 In-Context 条件化、对时间步使用 AdaLN 的组合，在 FID（44.639）和运动分类精度（0.661）上均达到最优。

![[assets/figures/papers/paper_list_l1855_Move_in_2D_2D_Conditioned_Human_Motion_Generation/figures/010_Table_4.jpg]]
*Table 4: Ablation study. We study different transformer block designs, and choose AdaLN for timestep conditioning and In-Context for text and scene conditions as our main configuration*

### 输出参数化

模型输出运动序列长度 $N = 256$，特征维度 $D = 147$，包含 SMPL 姿态参数与全局朝向。与仅预测姿态的基线不同，Move-in-2D 额外预测一个相机平移参数 $\pi \in \mathbb{R}^3$，在假定透视相机（固定焦距与内参）的前提下，将 SMPL 空间中的三维人体点投影到二维图像平面，从而支持生成的运动在输入场景图像上的自然投影。

### 联合分类器自由引导

在采样阶段，对文本提示 $p$ 和场景图像 $s$ 进行联合分类器自由引导（Classifier-Free Guidance, CFG），以增强生成运动与输入条件的对齐度：

$$\mathcal{M}_{\mathrm{cfg}} = \mathcal{M}(\mathbf{x}_t \mid t) + g \left( \mathcal{M}(\mathbf{x}_t \mid t, p, s) - \mathcal{M}(\mathbf{x}_t \mid t) \right)$$

其中：
- $\mathcal{M}(\mathbf{x}_t \mid t)$ 为无条件扩散模型输出；
- $\mathcal{M}(\mathbf{x}_t \mid t, p, s)$ 为同时条件化于文本和场景的模型输出；
- $g$ 为引导尺度，控制条件对齐的强度。

训练时以概率 $q = 0.1$ 随机丢弃文本和场景条件，使模型同时学习条件与无条件分布，以支持采样时的 CFG 推断。

### 两阶段训练策略

为解耦原始视频中的相机运动并增强大动态运动生成能力，模型采用两阶段训练：

1. **第一阶段**：在全量 300K 视频数据上训练 600K 迭代，使模型初步建立场景-运动映射。
2. **第二阶段**：在 150K 混合数据（60% 大动态运动视频 + 40% 固定背景视频）上微调 600K 迭代，抑制残余相机运动，同时提升大位移动作的生成质量。

训练使用 Adam 优化器，学习率 $1 \times 10^{-4}$（原文为 0.0002，需手动核实），批次大小 128，扩散步数 1000 并采用余弦噪声调度。

## 实验与分析

### 评估设置

实验在HiC-Motion测试集上进行，该测试集从100个高频动词短语中采样，每个短语选取10个视频，每段视频抽取一帧并移除人体作为场景图像，共构成957个测试样本。评估指标包含四个维度：

- **FID**：基于自定义STGCN运动分类器计算，衡量生成运动与真实运动分布的距离；
- **Accuracy**：同一分类器的分类精度，反映运动语义的可辨识性；
- **Diversity**与**Multimodality**：衡量生成结果的多样性与多模态覆盖度。

所有运动序列统一为长度N=256、特征维度D=147（包含21个SMPL关节的6D旋转表示及根节点位移等参数）。由于目前尚无评估二维场景图像与运动序列兼容性的成熟指标，本文额外引入基于VLM的自动评估（见下文）。

### 主实验结果

**定量对比**（Table 2）。Move-in-2D在HiC-Motion测试集上取得FID 44.639（所有方法中最低）和Accuracy 0.661（最高），同时Diversity达到26.027。与仅使用场景条件的消融变体Ours-scene相比，完整模型的精度提升约37%，证明文本提示对运动语义对齐的贡献至关重要。三维场景条件基线（SceneDiff、HUMANISE等）需借助Depth Anything将二维图像反投影为点云，可能引入深度估计误差；即便如此，所提方法仍全面领先。

**VLM自动评估**（Table 3）。采用GPT-4作为评判器，从场景对齐（0-5）、文本对齐（0-5）和姿态质量（0-5）三个维度评分，总分15。Move-in-2D获得场景对齐3.55、文本对齐2.70、姿态质量2.85，总分9.10，在所有基线中均最高。需注意，VLM评分标准可能与人类评判存在系统性偏差，但作为相对排序指标仍具参考价值。

**定性对比**（Figure 5）。MDM和SceneDiff生成不合理的姿态；MLD产生与场景不匹配的运动；HUMANISE倾向于生成静态姿势。Move-in-2D则能生成与场景和文本均一致的连贯运动，如在山崖边站立、与狗互动等场景感知行为（Figure 3），以及打网球等大动态运动（Figure 4）。

### 消融实验

Table 4系统消融了条件注入方式的设计选择：

- **条件注入策略**：对比了In-Context conditioning与Cross-Attention两种方案，结果表明对文本和场景条件使用In-Context conditioning（共享标记空间）可获得更优的FID和Accuracy。
- **时间步注入方式**：对比了AdaLN与In-Context两种方案，AdaLN在扩散时间步条件化上表现更好。
- **最优组合**：文本/场景使用In-Context conditioning + 时间步使用AdaLN的组合在FID（44.639）和Accuracy（0.661）上均达到最佳，被选为最终配置。

### 失败模式与局限性

尽管Move-in-2D在定量和定性评估中表现优异，仍存在以下已知局限：

1. **相机运动不可控**：模型未对生成的相机平移参数$\pi \in \mathbb{R}^3$施加显式约束，运动序列可能包含来自原始视频的残余相机移动，在固定相机场景下会产生不自然的投影偏移。
2. **两阶段流程未端到端优化**：当前运动生成与下游视频生成（如Figure 6所示）是分离的，尚未在HiC-Motion数据集上进行联合训练，限制了端到端的质量提升空间。
3. **仅支持单人运动**：测试数据均经过单人过滤，模型无法处理多人交互或人群场景。
4. **测试集覆盖范围**：测试文本提示基于高频动词短语，可能未充分反映长尾或组合动作的泛化能力。

### 关键图表结论汇总

| 图表 | 核心结论 |
|------|----------|
| Table 1 | HiC-Motion是当前最大的包含运动、文本和多样化室内外场景的数据集 |
| Table 2 | Move-in-2D在FID、Accuracy上全面优于文本条件、场景条件和多模态运动生成基线 |
| Table 3 | VLM自动评估中，本方法在场景对齐、文本对齐和姿态质量三个维度均领先 |
| Table 4 | In-Context conditioning（文本/场景）+ AdaLN（时间步）的组合达到最优性能 |
| Figure 3 | 模型能生成场景感知的运动，如站立悬崖边、抚摸狗等复杂人-场景交互 |
| Figure 4 | 支持大动态运动生成，如打网球，且运动在场景中位置准确 |
| Figure 5 | 定性对比显示，本方法在运动合理性和场景-文本一致性上显著优于MDM、MLD、SceneDiff和HUMANISE |

![[assets/figures/papers/paper_list_l1855_Move_in_2D_2D_Conditioned_Human_Motion_Generation/figures/008_Table_2.jpg]]
*Table 2: Quantitative results. Our method achieves better quality and diversity scores compared to state-of-the-art text-conditioned, scene-conditioned, and multimodal motion generation models*

![[assets/figures/papers/paper_list_l1855_Move_in_2D_2D_Conditioned_Human_Motion_Generation/figures/007_Table_3.jpg]]
*Table 3: Automated evaluation. We report average VLM scores (0-5) for generated motions, assessing alignment with scene, text, and pose quality. Our method outperforms all evaluated baselines*

![[assets/figures/papers/paper_list_l1855_Move_in_2D_2D_Conditioned_Human_Motion_Generation/figures/002_Table_1.jpg]]
*Table 1: Dataset statistics. HiC-Motion is the largest dataset comprising motions, text, and diverse indoor and outdoor scenes*

![[assets/figures/papers/paper_list_l1855_Move_in_2D_2D_Conditioned_Human_Motion_Generation/figures/005_Figure_3.jpg]]
*Figure 3: Affordance-aware human generation. Our model generates human poses consistent with both text prompts and scene context, such as standing on a cliff. It also supports complex human-scene interactions, including activities like petting a dog*

![[assets/figures/papers/paper_list_l1855_Move_in_2D_2D_Conditioned_Human_Motion_Generation/figures/006_Figure_5.jpg]]
*Figure 5: Comparison to state-of-the-art. MDM and SceneDiff produces implausible poses, MLD generates mismatched motion with the scene, and HUMANISE generates static poses. Our method generates coherent motion aligned with both the scene and text prompts*

### 补充图表

![[assets/figures/papers/paper_list_l1855_Move_in_2D_2D_Conditioned_Human_Motion_Generation/figures/009_Figure_6.jpg]]
*Figure 6: Motion-guided human video generation. Our approach generates scene-compatible motion sequences from a scene image and text prompt, which are then used to animate a reference human using Champ [60] or Gen-3 [11]. The generated motion ensures accurate human shapes and smooth motion in the resulting videos, outperforming SVD [5] in preserving human geometry and motion consistency*

## 方法谱系与知识库定位

### 1. 与现有基线的结构性差异

Move‑in‑2D 的核心突破在于**将场景条件从三维显式重建降维为二维图像隐式编码**，并采用**上下文条件化（In‑Context Conditioning）**统一多模态条件注入。这一设计使其与现有方法在三个关键维度上形成结构性区分：

| 维度 | 文本条件运动生成 | 三维场景条件运动生成 | **Move‑in‑2D（本方法）** |
|------|------------------|----------------------|--------------------------|
| 条件模态 | 仅文本 | 文本 + 三维点云/网格 | **文本 + 二维场景图像** |
| 场景获取成本 | 无 | 高（需深度传感器或多视图重建） | **低（单张RGB图像即可）** |
| 条件注入方式 | 交叉注意力或FiLM | 交叉注意力或拼接 | **In‑Context Conditioning（共享标记空间） + AdaLN（时间步）** |
| 输出空间 | SMPL姿态 + 全局朝向 | SMPL姿态 + 全局朝向 | **SMPL姿态 + 全局朝向 + 相机平移参数 π∈ℝ³** |

**具体基线对比：**

- **MDM**（Tevet et al., ICLR 2023）与 **MLD**（Chen et al., CVPR 2023）：纯文本条件扩散模型，缺乏场景感知能力。在HiC‑Motion测试集上，MDM+（使用HiC‑Motion数据训练的MDM增强版）生成的姿态常出现物理不合理性（Figure 5），MLD则产生与场景平面不匹配的运动投影。Move‑in‑2D通过引入场景图像条件，使生成的运动序列能够自然投影到二维场景平面，解决了纯文本模型“悬浮运动”的问题。

- **SceneDiff**（Huang et al., CVPR 2023）与 **HUMANISE**（Wang et al., NeurIPS 2022）：两者均依赖三维点云作为场景条件。SceneDiff生成的运动姿态存在物理不合理性，HUMANISE则倾向于生成静态姿态，缺乏动态运动（Figure 5）。Move‑in‑2D绕开了三维重建瓶颈，直接利用二维图像中的场景布局信息（如地面平面、障碍物边界），通过DINO编码器提取的视觉标记隐式学习场景可供性（affordance），在VLM评估中场景对齐得分达3.55（Table 3），显著优于HUMANISE等三维条件基线。

- **Ours‑scene（消融变体）**：仅使用场景图像条件、移除文本提示时，运动分类精度下降37%（Table 2），表明文本提示对运动语义对齐具有不可替代的因果作用。这验证了双条件设计的必要性。

### 2. 条件注入策略的消融证据

Table 4的消融实验系统比较了四种条件注入组合，揭示了**In‑Context Conditioning + AdaLN**的最优性：

- **时间步条件**：AdaLN（自适应层归一化） vs. In‑Context。AdaLN在FID和精度上均优于将时间步也作为上下文标记的方案，说明扩散时间步作为全局调制信号比作为序列标记更有效。
- **文本与场景条件**：In‑Context vs. 交叉注意力。将文本和场景编码为统一标记空间中的上下文标记（In‑Context），在FID（44.639）和精度（0.661）上均达到最佳。交叉注意力方案可能因查询‑键对齐的灵活性不足而降低条件融合效率。

这一发现的方法论意义在于：**借鉴大语言模型中的上下文学习范式，将异质条件（图像、文本）统一为共享标记空间中的前缀标记，可以避免为每种模态设计独立的条件注入机制**，简化了多条件扩散模型的设计空间。

### 3. 适用边界与局限

Move‑in‑2D的适用边界由以下设计选择决定：

**适用场景：**
- 单人运动生成，场景为静态二维背景图像
- 运动类型覆盖常见交互动作（站立、行走、坐下、抚摸动物等）和大动态运动（打网球等）
- 下游任务可作为视频生成的控制信号（Figure 6，配合Champ或Gen‑3）

**关键局限：**

1. **相机运动不可控**：模型预测的相机平移参数 π 来自原始视频的残余相机运动，无法按需指定相机轨迹。这导致生成的二维投影可能包含非预期的视角变化，影响与静态场景图像的一致性。论文明确指出“框架未对生成的相机运动进行控制”。

2. **单人限制**：模型仅处理单人运动，测试数据经过单人过滤。无法生成多人交互或人群场景中的协调运动。

3. **两阶段流程未端到端优化**：运动生成与视频生成（Champ/Gen‑3）分阶段进行，未在HiC‑Motion数据集上联合训练。这限制了最终视频中人体几何一致性和运动平滑度的上限。

4. **VLM评估的可靠性**：由于缺乏评估二维运动‑场景兼容性的标准指标，论文采用GPT‑4（OpenAI, 2024）进行自动评分。该评估可能存在与人类评判的系统性偏差，且评分标准（0‑5分制）的粒度可能不足以捕捉细微的场景穿透或物理不合理性。

5. **泛化边界未知**：测试集文本提示基于100个高频动词短语构建，可能偏向常见动作。模型在开放词汇、长尾动作或未见场景类型（如极端透视、非自然场景）下的泛化能力尚未验证。

### 4. 开放问题与后续方向

从当前局限出发，可识别以下开放问题：

- **相机运动解耦与控制**：如何引入显式的相机运动控制机制（如条件化相机轨迹参数），使生成的运动能适配任意指定的二维投影视角？这可能需要修改训练策略，在第二阶段微调时显式建模相机运动与人体运动的独立性。

- **端到端联合优化**：能否将运动扩散模型与视频生成模型（如SVD、Champ）进行端到端联合训练，使运动序列的生成直接以最终视频质量为优化目标？这需要解决两个扩散模型之间的梯度传递和训练稳定性问题。

- **多人场景扩展**：如何将上下文条件化框架扩展至多人场景，同时保持个体‑场景、个体‑个体之间的合理交互？可能的路径包括引入交互图网络或顺序生成策略，但需要相应的多人运动‑场景配对数据集支持。

- **评估体系完善**：如何建立更可靠的二维运动‑场景兼容性评估指标？可能的方案包括基于投影穿透率的物理度量、基于渲染的感知评估，或引入人类评判的基准数据集。

- **泛化能力验证**：在更开放、未见过的场景图像和文本组合下，模型的场景可供性理解能力是否仍然鲁棒？是否需要更丰富的场景‑运动对齐标注（如接触点、支撑面标注）来提升泛化性？

### 5. 在知识库中的定位

Move‑in‑2D 处于**二维条件运动生成**这一新兴交叉点，连接了三个研究方向：

- **上游**：继承自文本条件运动扩散模型（MDM、MLD）的扩散框架和SMPL参数化表示，以及三维场景条件方法（SceneDiff、HUMANISE）的场景感知运动生成目标。
- **核心创新**：通过**二维图像条件 + In‑Context Conditioning**将场景感知运动生成的门槛从三维重建降低到单张RGB图像，同时引入**相机平移预测**以支持二维投影对齐。
- **下游**：为运动引导的视频生成（Figure 6）提供场景兼容的运动控制信号，可作为现有视频扩散模型（Champ、Gen‑3）的即插即用运动先验。

该方法的方法论贡献——**利用上下文学习范式统一多模态条件注入**——对后续多条件生成模型设计具有参考价值，但其当前的单人、静态场景、不可控相机的限制，也为后续工作留下了明确的研究空间。

## 原文 PDF

![[paperPDFs/CVPR_2025/Move_in_2D_2D_Conditioned_Human_Motion_Generation.pdf]]