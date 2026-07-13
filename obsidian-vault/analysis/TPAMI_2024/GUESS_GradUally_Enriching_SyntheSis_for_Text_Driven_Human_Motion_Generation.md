---
title: GUESS GradUally Enriching SyntheSis for Text Driven Human Motion Generation
type: paper
paper_level: A
venue: TPAMI
year: 2024
pdf_ref: paperPDFs/TPAMI_2024/GUESS_GradUally_Enriching_SyntheSis_for_Text_Driven_Human_Motion_Generation.pdf
project_link: null
code_link: https://github.com/Xuehao-Gao/GUESS
aliases:
- GGESTDHMG
tags:
- TPAMI_2024
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
- topic/generative_models_diffusion
core_operator: 多尺度身体姿态表示与由粗到精的级联潜在扩散生成策略。
primary_logic: 仿照人类从粗到细想象动作的过程，将人体动作抽象为多级骨骼图，先合成粗粒度的稳定运动提示，再逐步注入文本条件和粗运动提示丰富细节，从而降低每一步的跨模态映射难度。
claims:
- 级联渐进生成策略显著缓解了单阶段生成中的身体关节抖动问题，并提高了生成质量。
- GUESS在HumanML3D上的FID达到0.109，相比第二好的T2M-GPT（0.141）和MLD（0.473）大幅领先，且R-Precision、MM Dist和Diversity均取得最优。
- 消融实验显示使用两级及以上尺度（S1+S2）的FID较仅使用S1有显著提升（如Table 4中0.334 vs 0.109），且动态多条件融合模块进一步提升了R-Precision和FID。
- HumanML3D 上 R-Precision Top-1 ↑ = 0.503 ± .003
---

# GUESS GradUally Enriching SyntheSis for Text Driven Human Motion Generation

> [!tip] 核心洞察
> 仿照人类从粗到细想象动作的过程，将人体动作抽象为多级骨骼图，先合成粗粒度的稳定运动提示，再逐步注入文本条件和粗运动提示丰富细节，从而降低每一步的跨模态映射难度。

| 字段 | 内容 |
|------|------|
| 中文题名 | GUESS：逐渐丰富合成的文本驱动人体动作生成 |
| 英文题名 | GUESS GradUally Enriching SyntheSis for Text Driven Human Motion Generation |
| 会议/期刊 | TPAMI 2024 |
| Links | [Code](https://github.com/Xuehao) · [Code](https://github.com/Xuehao-Gao/GUESS) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction #topic/generative_models_diffusion |
| Method | GUESS |
| Dataset | HumanML3D, KIT-ML, UESTC |

> [!tip] 效果简介
> - HumanML3D 上，R-Precision Top-1 ↑ 0.503 ± .003 vs 0.492 ± .003 (T2M-GPT) (+0.011)；FID ↓ 0.109 ± .007 vs 0.141 ± .005 (T2M-GPT) (-0.032)；Diversity ↑ 9.826 ± .104 vs 9.724 ± .082 (MLD) (+0.102)。
> - KIT-ML 上，R-Precision Top-1 ↑ 0.425 ± .005 vs 0.419 ± .005 (T2M-GPT) (+0.006)；FID ↓ 0.371 ± .020 vs 0.384 ± .027 (T2M-GPT) (-0.013)。
> - UESTC 上，FID_train ↓ 8.01 vs 10.21 (MLD) (-2.20)。

## 概要

文本驱动的人体动作生成旨在从自然语言描述中合成逼真的三维骨骼运动序列。该任务的核心瓶颈在于**文本模态与人体运动模态之间存在巨大的语义—几何鸿沟**：直接从文本一步到位地生成包含数十个骨骼关节的精细运动序列，极易导致关节抖动、语义错位与不自然的动作片段。

GUESS（**Grad**Ually **E**nriching **S**ynthe**s**is）提出了一种仿照人类“由粗到细”想象过程的解决方案。其核心洞察是：将人体动作抽象为多级骨骼图——从最粗的整体躯干节点（S4）到最细的22个骨骼关节（S1）——先合成粗粒度的稳定运动提示，再逐步注入文本条件和粗运动提示来丰富细节，从而**将困难的单步跨模态映射分解为多个渐进的、难度递减的子任务**。

在方法层面，GUESS采用**级联潜在扩散模型**（cascaded latent diffusion model）作为生成框架，配合两个关键设计：
- **多尺度VAE运动编码**：在每个姿态尺度上训练一个基于Transformer的变分自编码器，将运动序列压缩到低维潜在空间，使扩散过程在更紧凑的表示上进行。
- **动态多条件融合模块**：在每一级去噪过程中，通过通道注意力重标定和跨模态注意力，自适应地融合文本嵌入与上一级粗运动嵌入，生成样本专属、去噪步专属的联合条件。

实验结果表明，GUESS在HumanML3D数据集上取得了**FID 0.109**的当时最优结果，相比第二好的方法T2M-GPT（FID 0.141）和MLD（FID 0.473）大幅领先，同时在R-Precision、MM Dist和Diversity三项指标上均达到最优。消融实验进一步证实，多尺度渐进生成（两级及以上尺度相比仅用S1，FID从0.334降至0.109）和动态多条件融合是性能提升的关键因素。定性可视化显示，级联生成策略显著缓解了单阶段生成中常见的身体关节抖动问题。



文本驱动的人体动作生成旨在根据自然语言描述合成逼真的三维人体运动序列，在虚拟人、游戏、影视、人机交互等领域具有广泛应用前景。该任务的核心挑战在于**文本模态与人体运动模态之间存在巨大的语义和结构鸿沟**：文本是高度抽象、语义压缩的离散符号序列，而人体运动则是高维连续时空信号，包含数十个骨骼关节的精细旋转与位置变化。直接从文本描述一步生成完整运动序列极易导致关节抖动、语义不一致以及运动不自然等问题。

早期方法主要采用循环神经网络（RNN）或Transformer构建文本到动作的序列到序列映射，如 **Seq2Seq**（Lin et al., NeurIPS 2018）、**Language2Pose**（Ahuja et al., 3DV 2019）、**Hier**（Ghosh et al., ICCV 2021）等。这些方法通常直接回归关节旋转或位置，缺乏对运动分布的有效建模，生成质量有限。随后，基于生成对抗网络（GAN）的方法如 **MoCoGAN**（Tulyakov et al., CVPR 2018）尝试将动作分解为内容与运动分支，但训练不稳定且多样性不足。

近年来，扩散模型在图像和视频生成领域取得突破性进展，并迅速被引入人体动作生成。**MDM**（Tevet et al., ICLR 2023）首次将去噪扩散概率模型应用于原始运动序列的直接生成，**MLD**（Chen et al., CVPR 2023）进一步将扩散过程迁移到潜在空间以提高效率，**T2M-GPT**（Zhang et al., CVPR 2023）则将生成建模为离散码本的序列预测。这些方法在生成质量上取得了显著进步，但它们普遍采用**单阶段生成范式**：一次性从噪声和文本条件合成所有关节的完整细粒度运动。这种“一步到位”的策略忽视了人体运动天然的层次化结构——躯干、四肢、末端关节的运动在空间精度和语义粒度上存在明显差异，单阶段生成难以同时兼顾全局稳定性和局部细节。

GUESS的核心动机正源于此：**仿照人类从粗到细想象动作的认知过程**——当读到“一个人向前走并挥手”时，大脑首先勾勒出身体整体的移动轨迹和姿态轮廓，再逐步丰富手臂摆动、手指动作等细节。GUESS将这一直觉转化为**多尺度身体姿态表示与由粗到精的级联潜在扩散生成策略**，将人体动作抽象为从单节点躯干到22关节全身的多级骨骼图，先合成最粗粒度的稳定运动提示，再逐步注入文本条件和粗运动提示丰富细节，从而降低每一步的跨模态映射难度，缓解单阶段生成中的关节抖动与语义漂移问题。



## 核心方法与创新机理

GUESS 的核心创新在于将文本驱动人体动作生成这一高难度跨模态映射问题，分解为**由粗到细的多阶段渐进生成过程**。这一设计并非简单的工程堆叠，而是针对单阶段生成中普遍存在的**身体关节抖动（body-joint jittering）**和语义不一致问题，从生成框架、条件融合机制和运动表示三个维度进行了系统性重构。

### 1. 核心瓶颈与因果杠杆

文本到人体动作生成的本质困难在于**文本模态与精细骨骼运动模态之间存在巨大语义鸿沟**。现有单阶段方法（如 **MDM**（Tevet et al., ICLR 2023）和 **MLD**（Chen et al., CVPR 2023））试图直接从文本条件一次性合成全部 22 个骨骼关节的三维运动序列，这迫使模型在极高维度空间中完成跨模态对齐，极易产生关节抖动和语义漂移。

GUESS 识别出的**因果杠杆**是**多尺度身体姿态表示与级联潜在扩散策略**：通过将人体骨骼抽象为从 22 个关节（S1）→ 11 个身体部件（S2）→ 5 个部件（S3）→ 1 个根节点（S4）的四级层次结构（Fig. 3），将生成任务分解为先在极低维度空间合成粗粒度运动提示，再逐步注入文本条件和粗运动先验以丰富细节。这一策略的直观动机来源于人类认知过程——人在想象动作时，总是先构想躯干和主要肢体的宏观运动，再逐步填充手指、头部等精细关节的细节（Fig. 1）。

### 2. 关键 changed slots

相较于主流 baseline，GUESS 在以下三个关键维度上做出了实质性改变：

#### 2.1 生成框架：从单阶段直接生成到多级联渐进生成

| 维度 | Baseline 做法 | GUESS 做法 |
|------|-------------|-----------|
| 生成策略 | 单阶段直接从噪声+文本条件合成所有关节的细粒度运动序列（如 MDM、MLD） | 四级联潜在扩散模型：R4 基于文本嵌入 $c$ 生成最粗尺度 $z_4$，随后 R3→R1 依次结合 $c$ 和上一级粗运动嵌入 $z_{i+1}$ 生成 $z_3$→$z_1$ |
| 证据强度 | — | 消融实验（TABLE 4）显示，仅使用 S1 的单阶段生成 FID 为 0.334，而引入 S2 后 FID 降至 0.109，降幅达 67%；Fig. 9 的定性对比中，单阶段生成的红色圆圈区域存在明显关节抖动，而四阶段级联生成则显著平滑 |

这一改变的核心机制在于：每一阶段仅需完成有限幅度的跨模态映射（从粗到细的增量丰富），而非一次性跨越文本到精细运动的全部距离。最粗尺度 $z_4$ 的生成仅依赖文本条件 $c$，其去噪步骤为：

$$z_4^{t-1} = \frac{1}{\sqrt{\alpha_t}} z_4^t - \sqrt{\frac{1}{\alpha_t} - 1} \mathcal{R}_4(z_4^t, t, c)$$

后续较细尺度的去噪则同时依赖文本条件和上一级粗运动嵌入：

$$z_3^{t-1} = \mathcal{R}_3(z_3^t, t, c, z_4) = \frac{1}{\sqrt{\alpha_t}} z_3^t - \sqrt{\frac{1}{\alpha_t} - 1} \mathcal{T}_3(j_t, z_3^t)$$

其中 $j_t$ 为动态融合后的联合条件（见下文）。

#### 2.2 条件融合方式：从简单拼接到动态多条件融合

| 维度 | Baseline 做法 | GUESS 做法 |
|------|-------------|-----------|
| 融合机制 | 仅使用文本嵌入作为条件，或简单拼接文本与运动条件 | 动态多条件融合模块（Dynamic Multi-Condition Fusion）：通过对去噪时刻 $t$ 编码、通道注意力加权、跨模态注意力动态生成文本条件权重 $w_c$ 和运动条件权重 $w_z$，逐样本、逐去噪步自适应融合 |
| 证据强度 | — | 消融实验（TABLE 7）显示，使用动态融合较不使用融合或不使用文本条件，在 R-Precision Top-1 和 FID 上均有显著提升 |

该模块的核心操作分为三步：
1. **通道注意力重标定**：对加入时间嵌入的运动表示 $\widetilde{z_4}$ 和文本表示 $\widetilde{c}$ 分别进行通道注意力加权，得到精炼嵌入 $\widehat{z_4}$ 和 $\widehat{c}$；
2. **跨模态注意力融合**：通过一个可学习的小型网络，从 $\widehat{z_4} + \widehat{c}$ 中动态推断融合权重 $[w_z, w_c]$；
3. **联合条件生成**：$j_t = w_z \hat{z_4} + w_c \hat{c}$。

这一设计的精妙之处在于，权重 $w_z$ 和 $w_c$ 是**去噪时刻 $t$ 的函数**：在去噪早期（$t$ 较大），模型可能更依赖粗运动嵌入提供的结构先验；而在去噪后期（$t$ 较小），文本条件的细粒度语义约束可能更为重要。Fig. 11 的可视化证实了不同去噪器和去噪步中文本/运动跨模态注意力权重的动态变化。

#### 2.3 运动表示：从原始运动序列到潜在空间扩散

| 维度 | Baseline 做法 | GUESS 做法 |
|------|-------------|-----------|
| 表示空间 | 直接在原始运动序列空间（如旋转、位置、速度）执行扩散或生成 | 在每个尺度上训练一个 Transformer-based VAE，将运动编码到低维潜在空间，然后在潜在空间中执行扩散过程 |
| 证据强度 | — | TABLE 5 的 VAE 评估显示，各尺度的重建 MPJPE 和 FID 均处于较低水平，验证了潜在表示的有效性 |

VAE 的训练损失结合了运动重建 L2 损失和 KL 散度正则项：

$$\mathcal{L}_{\mathcal{V}} = \lambda_{mr}\sum_{i=1}^{4} \| \pmb{S}_i - \mathcal{D}_i(\mathcal{E}_i(\pmb{S}_i)) \|_2 + \lambda_{kl}\sum_{i=1}^{4} KL(\mathcal{N}(\mu_i,\sigma_i^2)\|\mathcal{N}(0,1))$$

在潜在空间中执行扩散过程（前向加噪 $q(z_i^t \| z_i^{t-1}) = \mathcal{N}(\sqrt{\alpha^t} z_i^{t-1}, \sqrt{1-\alpha^t} I)$）具有双重优势：一是降低了扩散模型需要建模的维度，使训练更稳定；二是潜在空间天然具有更好的语义连续性，有利于跨模态条件的注入。

### 3. 创新点的协同效应

上述三个 changed slots 并非孤立存在，而是形成了**结构性的协同效应**：多尺度姿态表示为级联生成提供了天然的层次化目标空间；潜在运动编码使每个尺度的扩散过程在低维语义空间中高效运行；动态多条件融合则确保了在每个去噪步骤中，文本语义约束和粗运动结构先验能够以最优比例协同作用。消融实验中，采用 8 层 Transformer 去噪器并同时输入 $c + z_2 + z_3 + z_4$ 的配置获得最佳性能（TABLE 6，Top-1 0.503, FID 0.109），验证了多尺度条件协同的有效性。

### 4. 当前局限

需要指出的是，GUESS 的渐进生成策略目前存在两个固有限制：一是对所有输入文本采用**固定的四个尺度和四个推理阶段**，无法根据文本描述的复杂度（如“一个人走路” vs “一个人一边走路一边挥手并转头”）自适应调整阶段数；二是渐进生成仅从**空间维度**（姿态由粗到细）展开，尚未探索时间维度的渐进式生成（如先合成低帧率关键帧再补全高帧率细节）。这些方向构成了后续研究的重要开放问题。



GUESS 的整体设计遵循一个核心理念：**将文本到人体运动的跨模态生成问题分解为多个抽象层次，通过由粗到精的级联潜在扩散过程逐步合成目标运动**。这一设计直接回应了文本模态与精细骨骼关节运动之间存在的巨大语义鸿沟——单阶段方法试图一步跨越这一鸿沟，往往导致关节抖动和语义不一致。

### 三组件架构

GUESS 包含三个基本组件（见 Figure 2）：

![[assets/figures/papers/paper_list_l1930_GUESS_GradUally_Enriching_SyntheSis_for_Text_Driven_Human_Motion_Generat/figures/002_Figure_2.jpg]]
*Figure 2: The Framework of GUESS. In the training phase, we first represent a human motion input with multiple pose scales*

1. **多尺度姿态表示（Multi-Scale Pose Representation）**：将人体骨骼抽象为四个空间尺度（S₁→S₄），从 22 个身体关节逐步聚合为 11、5、1 个身体部件节点。这一聚合基于人体先验知识，将空间上相近的关节位置取平均，生成新的粗粒度特征。
2. **运动编码模块（Motion Encoding Module）**：在每个姿态尺度上部署一个基于 Transformer 的变分自编码器（VAE），学习该尺度的低维潜在运动表示 z₁~z₄。这些潜在嵌入是后续扩散过程的生成目标。
3. **运动推理模块（Motion Inference Module）**：由一个级联的潜在扩散模型构成，包含四个去噪器 R₄→R₁。推理过程从最粗尺度开始，逐步向最细尺度推进。

### 级联推理流程

推理过程严格遵循“由粗到精”的顺序：

- **阶段一（最粗尺度 S₄）**：去噪器 R₄ 仅以文本嵌入 c 为条件，从纯噪声中合成最粗粒度的运动潜在嵌入 z₄。
- **阶段二至四（S₃→S₁）**：每个后续去噪器 Rᵢ 同时接收文本条件 c 和上一级已合成的粗运动嵌入 z_{i+1} 作为条件，通过动态多条件融合模块生成联合条件 j_t，逐步丰富运动细节，最终生成最细粒度的 z₁。

### 动态多条件融合机制

在每个去噪步骤 t，动态多条件融合模块（Dynamic Multi-Condition Fusion）自适应地平衡文本与粗运动嵌入的贡献。具体而言：

1. 对文本嵌入 c 和粗运动嵌入 z_{i+1} 分别施加时间步编码，并通过通道注意力进行特征重标定，得到精炼的文本嵌入 ĉ 和运动嵌入 ẑ。
2. 通过跨模态注意力动态计算融合权重 [w_z, w_c]，生成联合条件 j_t = w_z · ẑ + w_c · ĉ。

这一机制使得模型能够根据输入样本的特性和当前去噪阶段，灵活调整文本语义与粗运动提示的相对重要性（见 Figure 11 的注意力权重可视化）。

### 训练与推理的分离

- **训练阶段**：先独立训练四个尺度的 VAE（损失函数为运动重建 L2 损失与 KL 散度的加权和），再固定 VAE 参数，训练级联扩散模型（损失函数为各尺度去噪器预测噪声的均方误差之和）。
- **推理阶段**：从高斯噪声出发，依次通过 R₄→R₁ 去噪，最后将潜在嵌入 z₁ 解码为完整的运动序列 S₁。

### 框架的关键设计选择

| 设计维度 | 选择 | 依据 |
|---------|------|------|
| 尺度数量 | 固定 4 个 | 消融实验（TABLE 4）显示两级及以上（S₁+S₂）的 FID 从 0.334 降至 0.109，四级达到最优 |
| 去噪步数 | T=250 | TABLE 8 显示从 100 增至 250 大幅提升性能，增至 1000 提升有限 |
| 条件融合 | 动态多条件融合 | TABLE 7 显示相比不使用融合或简单拼接，R-Precision 和 FID 均有提升 |
| 去噪器架构 | 8 层 Transformer | TABLE 6 显示该配置在 Top-1（0.503）和 FID（0.109）上取得最佳性能 |

### 局限与开放问题

当前框架对所有输入文本采用固定的四级推理，尚未根据文本复杂度自适应调整阶段数。此外，渐进生成目前仅从空间维度展开（姿态由粗到细），时间维度的渐进生成（如先合成低帧率序列再补全细节）仍有待探索。



GUESS 的核心架构由三个基本组件构成：多尺度姿态表示、运动编码模块和运动推理模块。其核心思想是将文本驱动的人体动作生成问题分解为多个抽象层次，通过级联潜在扩散模型逐步从粗到细丰富运动细节。

### 运动编码模块（Motion Encoding）

运动编码模块的核心任务是在每个姿态尺度上学习低维潜在运动表示。具体而言，对四个尺度 $S_1$ 至 $S_4$ 分别部署基于 Transformer 的变分自编码器（VAE），将高维运动序列压缩到紧凑的潜在空间，便于后续扩散模型处理。

VAE 的训练损失函数为：

$$\mathcal{L}_{\mathcal{V}} = \lambda_{mr}\sum_{i=1}^{4} \| \pmb{S}_i - \mathcal{D}_i(\mathcal{E}_i(\pmb{S}_i)) \|_2 + \lambda_{kl}\sum_{i=1}^{4} KL(\mathcal{N}(\mu_i,\sigma_i^2)||\mathcal{N}(0,1))$$

其中 $\mathcal{E}_i$ 和 $\mathcal{D}_i$ 分别为第 $i$ 尺度的编码器和解码器，$\pmb{S}_i$ 为原始运动表示。第一项为运动重建的 L2 损失，保证编码-解码后的运动序列与原始序列一致；第二项为 KL 散度正则项，约束潜在分布 $\mathcal{N}(\mu_i,\sigma_i^2)$ 逼近标准正态分布 $\mathcal{N}(0,1)$，确保潜在空间的连续性和可采样性。$\lambda_{mr}$ 和 $\lambda_{kl}$ 为两项损失的平衡权重。

### 运动推理模块（Motion Inference）

运动推理模块采用级联潜在扩散模型，由四个去噪器 $\mathcal{R}_4 \rightarrow \mathcal{R}_1$ 组成，从最粗尺度到最细尺度逐步生成目标运动表示。

**前向扩散过程**在潜在空间中对运动嵌入进行马尔可夫噪声注入：

$$q(z_i^t | z_i^{t-1}) = \mathcal{N}(\sqrt{\alpha^t} z_i^{t-1}, \sqrt{1-\alpha^t} I)$$

其中 $z_i^t$ 为第 $i$ 尺度在第 $t$ 步的噪声化潜在运动嵌入，$\alpha^t$ 为噪声调度系数，控制每一步的信噪比衰减。

**反向去噪过程**从纯噪声出发逐步重建运动嵌入。在最粗尺度 $S_4$，去噪器 $\mathcal{R}_4$ 仅依赖文本嵌入 $c$ 和时间步 $t$ 预测并去除噪声：

$$z_4^{t-1} = \frac{1}{\sqrt{\alpha_t}} z_4^t - \sqrt{\frac{1}{\alpha_t} - 1} \mathcal{R}_4(z_4^t, t, c)$$

该式表明，每一步去噪通过当前噪声嵌入 $z_4^t$ 减去去噪器预测的噪声分量，再经系数缩放得到更纯净的 $z_4^{t-1}$。

### 动态多条件融合模块（Dynamic Multi-Condition Fusion）

在较细尺度（$S_3$、$S_2$、$S_1$），去噪器需要同时利用文本条件 $c$ 和上一级生成的粗运动嵌入 $z_{i+1}$。动态多条件融合模块通过通道注意力和跨模态注意力自适应地生成融合条件。

首先，对加入时间嵌入后的粗运动表示 $\widetilde{z_4}$ 和文本表示 $\widetilde{c}$ 分别进行通道注意力重标定：

$$\widehat{z_4} = \widetilde{z_4} \otimes \mathrm{SoftMax}(\theta_z^2(\sigma(\theta_z^1(\widetilde{z_4}))))$$

$$\widehat{c} = \widetilde{c} \otimes \mathrm{SoftMax}(\theta_c^2(\sigma(\theta_c^1(\widetilde{c}))))$$

其中 $\sigma$ 为激活函数，$\theta_z^1$、$\theta_z^2$ 和 $\theta_c^1$、$\theta_c^2$ 为可学习的全连接层参数，$\otimes$ 表示逐元素乘法。该操作通过通道维度的自注意力机制增强关键特征、抑制冗余信息。

随后，通过跨模态注意力动态计算文本和运动嵌入的融合权重，生成联合条件 $j_t$：

$$j_t = w_z \hat{z_4} + w_c \hat{c}, \quad [w_z, w_c] = \mathrm{SoftMax}(\theta_j^2(\sigma(\theta_j^1(\hat{z_4} + \hat{c}))))$$

这里 $\theta_j^1$ 和 $\theta_j^2$ 学习从拼接的文本和运动特征中推断每个模态的重要性权重 $w_c$ 和 $w_z$，实现逐样本、逐去噪步的自适应融合。这种机制使得模型能够在不同生成阶段灵活调整文本语义引导和粗运动结构约束的相对贡献。

### 细尺度去噪与整体训练

获得联合条件 $j_t$ 后，细尺度去噪器 $\mathcal{R}_i$（以 $i=3$ 为例）通过 Transformer $\mathcal{T}_3$ 预测噪声并执行去噪：

$$z_3^{t-1} = \mathcal{R}_3(z_3^t, t, c, z_4) = \frac{1}{\sqrt{\alpha_t}} z_3^t - \sqrt{\frac{1}{\alpha_t} - 1} \mathcal{T}_3(j_t, z_3^t)$$

整个运动推理模块的训练损失为四个尺度去噪损失的加权和：

$$\mathcal{L}_{MI} = \mathbb{E}[\|\epsilon - \mathcal{R}_4(z_4^t, t, c)\|_2^2] + \sum_{i=1}^{3} \mathbb{E}[\|\epsilon - \mathcal{R}_i(z_i^t, t, c, z_{i+1})\|_2^2]$$

其中 $\epsilon$ 为前向过程中实际添加的噪声，去噪器的目标是精确预测该噪声。第一项对应最粗尺度的无条件（仅文本）去噪，后三项对应细尺度在粗运动引导下的去噪。通过联合优化四个尺度的噪声预测均方误差，模型学习到从文本到完整精细运动的渐进式映射。



## 实验与关键发现

### 主实验结果

GUESS在三个基准数据集上进行了全面评测，覆盖文本到动作生成（HumanML3D、KIT-ML）和动作标签到动作生成（UESTC、HumanAct12）两类任务。

**HumanML3D数据集**（Table 1）：GUESS在所有六项指标上均取得最优。FID降至**0.109 ± .007**，相比第二名的**T2M-GPT**（Zhang et al., CVPR 2023）的0.141降低了22.7%，相比**MLD**（Chen et al., CVPR 2023）的0.473降低了77.0%。R-Precision Top-1达到**0.503 ± .003**，较T2M-GPT的0.492提升0.011。Diversity达到**9.826 ± .104**，MM Dist降至**2.974 ± .036**，均优于所有对比方法。这一结果直接验证了级联渐进生成策略在缩小文本-运动跨模态差距方面的有效性——粗尺度运动提示为细尺度生成提供了稳定的结构先验，显著缓解了单阶段方法中常见的关节抖动和语义漂移问题。

**KIT-ML数据集**（Table 2）：GUESS在FID（**0.371 ± .020**）和R-Precision Top-1（**0.425 ± .005**）上均取得最优，但优势幅度小于HumanML3D。这与KIT-ML数据集规模较小（仅3,911个运动序列）有关，级联模型的多阶段训练对数据量更为敏感。

**UESTC数据集**（Table 3）：在动作到动作生成任务上，GUESS的FID_train降至**8.01**，显著优于MLD的10.21和**MoCoGAN**（Tulyakov et al., CVPR 2018）的24.06，证明多尺度渐进生成策略不仅适用于文本条件，对离散动作标签条件同样有效。

### 消融实验

**多尺度配置的贡献**（Table 4）：仅使用单一最细尺度S1时FID为0.334，加入粗尺度S2后FID骤降至0.109，降幅达67.4%。继续增加S3和S4后性能基本饱和（FID分别为0.113和0.109），说明两级粗细搭配已能捕获主要的结构约束，更多尺度主要提升Diversity（从9.474升至9.826）。值得注意的是，四尺度配置的平均推理时间为每句0.286秒，相比两尺度的0.217秒仅增加31.8%，效率代价可控。

**动态多条件融合模块**（Table 7）：移除融合模块（仅用文本条件）时FID升至0.183，R-Precision Top-1降至0.481。采用简单拼接替代动态加权时FID为0.121，Top-1为0.496。完整动态融合方案将Top-1提升至0.503，FID降至0.109，验证了逐样本、逐去噪步自适应平衡文本条件与粗运动条件权重的必要性。

**去噪器深度与条件输入**（Table 6）：8层Transformer配合完整条件（c+z2+z3+z4）取得最优Top-1（0.503）和FID（0.109）。减少层数至4层时FID升至0.121，减少条件输入（仅c+z4）时Top-1降至0.498。

**去噪步数**（Table 8）：去噪步数从100增至250时FID从0.221降至0.109，性能大幅提升；继续增至1000时FID仅微降至0.106，收益递减显著。作者选择T=250作为效率与质量的平衡点。

**VAE重建质量**（Table 5）：四尺度VAE在S1尺度上MPJPE为44.3mm，PAMPJPE为31.8mm，表明潜在空间压缩在保持重建精度的同时有效降低了扩散模型的生成难度。

### 定性分析与用户研究

**关节抖动改善**（Fig. 9）：单阶段生成（S1-only）的骨架序列在相邻帧间存在明显的关节位置跳变（红色圆圈标注），而级联四阶段生成的骨架运动平滑自然。这直接归因于粗尺度运动嵌入为细尺度去噪提供了全局结构约束，抑制了高维关节空间中无约束采样的高频噪声。

**多样性展示**（Fig. 7）：同一文本描述可生成风格迥异但语义一致的运动序列，验证了扩散模型在潜在空间中的随机采样能力。

**用户偏好研究**（Fig. 8）：在人类评估中，GUESS生成的动作在自然度和文本匹配度上均显著优于对比方法。

### 失败模式与局限

1. **固定阶段数**：当前方法对所有输入文本统一使用四个推理阶段。对于简单动作（如“站立”），粗尺度信息已足够，后续阶段可能引入冗余计算甚至噪声；对于复杂长描述，四个阶段可能仍不足以充分细化。作者指出未来需设计自适应阶段数的动态机制。

2. **仅空间维度渐进**：渐进生成目前仅从空间维度（姿态由粗到细）展开，尚未探索时间维度的渐进式生成（先合成低帧率运动序列再补全细节）。对于长时序动作，时间维度的由粗到细可能带来额外的效率和质量收益。

3. **数据集规模敏感性**：KIT-ML上的性能优势小于HumanML3D，暗示级联多阶段训练对小数据集可能存在过拟合风险，需要进一步验证。

4. **跨模态注意力可视化**（Fig. 11）：不同去噪步中文本与运动嵌入的注意力权重存在波动，表明动态融合机制虽有效，但权重的可解释性和稳定性仍有提升空间。

### 公平性说明

所有对比实验均采用统一的评估协议（20次重复，95%置信区间），统一使用CLIP-ViT-L-14作为文本编码器，训练/测试数据划分与基准方法一致，结果具有可比性。

### 补充图表

![[assets/figures/papers/paper_list_l1930_GUESS_GradUally_Enriching_SyntheSis_for_Text_Driven_Human_Motion_Generat/figures/006_Table_1.jpg]]

![[assets/figures/papers/paper_list_l1930_GUESS_GradUally_Enriching_SyntheSis_for_Text_Driven_Human_Motion_Generat/figures/007_Table_2.jpg]]

![[assets/figures/papers/paper_list_l1930_GUESS_GradUally_Enriching_SyntheSis_for_Text_Driven_Human_Motion_Generat/figures/008_Table_3.jpg]]

![[assets/figures/papers/paper_list_l1930_GUESS_GradUally_Enriching_SyntheSis_for_Text_Driven_Human_Motion_Generat/figures/012_Table_4.jpg]]

![[assets/figures/papers/paper_list_l1930_GUESS_GradUally_Enriching_SyntheSis_for_Text_Driven_Human_Motion_Generat/figures/013_Figure_9.jpg]]
*Figure 9: Visual comparison between*

![[assets/figures/papers/paper_list_l1930_GUESS_GradUally_Enriching_SyntheSis_for_Text_Driven_Human_Motion_Generat/figures/015_Table_7.jpg]]

![[assets/figures/papers/paper_list_l1930_GUESS_GradUally_Enriching_SyntheSis_for_Text_Driven_Human_Motion_Generat/figures/018_Table_6.jpg]]

![[assets/figures/papers/paper_list_l1930_GUESS_GradUally_Enriching_SyntheSis_for_Text_Driven_Human_Motion_Generat/figures/019_Table_8.jpg]]

![[assets/figures/papers/paper_list_l1930_GUESS_GradUally_Enriching_SyntheSis_for_Text_Driven_Human_Motion_Generat/figures/011_Figure_8.jpg]]
*Figure 8: User Study. Each bar indicates the preference rate of GUESS over other methods. The red line indicates the 50%*

![[assets/figures/papers/paper_list_l1930_GUESS_GradUally_Enriching_SyntheSis_for_Text_Driven_Human_Motion_Generat/figures/003_Figure_3.jpg]]
*Figure 3: Four body scales on HumanML3D dataset. In the initial scale*

![[assets/figures/papers/paper_list_l1930_GUESS_GradUally_Enriching_SyntheSis_for_Text_Driven_Human_Motion_Generat/figures/010_Figure_7.jpg]]
*Figure 7: Diverse synthesized motion samples. We visualize two human motion generation results for each textual description. These qualitative evaluations indicate that GUESS generates realistic and diverse motions*



## 定位与知识库关联

### 1. 问题定位：跨模态鸿沟与单阶段生成的困境

文本驱动的人体动作生成面临的核心瓶颈在于**文本模态与人体运动模态之间存在巨大差距**——从自然语言描述直接映射到包含数十个骨骼关节的精细三维运动序列，其映射空间高度复杂且多解。早期方法如 **Seq2Seq**（Lin et al., NeurIPS 2018）、**Language2Pose**（Ahuja et al., 3DV 2019）和 **Hier**（Ghosh et al., ICCV 2021）采用循环或图卷积网络进行序列到序列的回归，但受限于确定性映射的表达能力，生成的动作往往趋于平均化、缺乏多样性。

近期基于扩散模型的方法如 **MDM**（Tevet et al., ICLR 2023）和 **MLD**（Chen et al., CVPR 2023）将扩散过程引入运动生成，显著提升了生成质量与多样性。然而，这些方法均采用**单阶段生成策略**——直接从噪声和文本条件一次性合成所有关节的完整运动序列。这种策略的根本缺陷在于：去噪网络必须在每个时间步同时处理所有关节的精细协调关系，导致优化困难，具体表现为**身体关节抖动**（body-joint jittering）和**语义错位**。如原文 Fig. 9 所示，单阶段生成结果在红色标注处出现明显的不自然抖动，而级联生成则有效缓解了这一问题。

基于离散 token 的自回归方法 **T2M-GPT**（Zhang et al., CVPR 2023）通过将运动量化为离散编码并逐帧预测，在 HumanML3D 上取得了当时最优的 FID（0.141），但其逐帧自回归的本质限制了长程时序一致性的建模能力，且推理速度受序列长度制约。

### 2. GUESS 的核心机制：级联潜在扩散与由粗到精生成

GUESS 的核心洞察在于**仿照人类从粗到细想象动作的认知过程**：当人脑理解“一个人向前走并挥手”时，会先勾勒出身体整体的移动轨迹和躯干姿态（粗粒度），再逐步填充手臂摆幅、步态节奏等细节（细粒度）。GUESS 将这一认知策略工程化为三个相互耦合的机制：

**（1）多尺度姿态表示。** GUESS 将人体骨骼抽象为四个层级：S1（22 个关节节点，原始精度）、S2（11 个身体部件节点）、S3（5 个核心部件节点）、S4（1 个全局根节点）。这种抽象并非简单的下采样，而是基于人体语义邻近性将空间相近的关节分组并替换为单一身体部件节点，从而在每个尺度上保留有意义的运动语义。

**（2）级联潜在扩散模型。** 与 MDM/MLD 的单阶段扩散不同，GUESS 采用四个级联的去噪器 $\mathcal{R}_4 \rightarrow \mathcal{R}_1$，从最粗尺度开始逐步生成：
- $\mathcal{R}_4$ 仅基于文本嵌入 $c$ 生成最粗尺度潜在运动 $z_4$（全局轨迹和身体朝向）；
- $\mathcal{R}_3$ 结合 $c$ 和已生成的粗运动嵌入 $z_4$，生成更细的 $z_3$；
- 依此类推，直至 $\mathcal{R}_1$ 生成最精细的 $z_1$。

这种级联策略将原本的单步跨模态映射分解为多个递进子任务，每一步只需在上一级粗粒度运动提示的基础上进行局部细化，大幅降低了每个去噪器的优化难度。

**（3）动态多条件融合模块。** 在细尺度去噪器（$\mathcal{R}_3$ 至 $\mathcal{R}_1$）中，文本条件 $c$ 和粗运动条件 $z_{i+1}$ 并非简单拼接，而是通过一个动态融合机制自适应地加权。具体而言，该模块对去噪时刻 $t$ 编码后，分别对文本嵌入和运动嵌入施加通道注意力重标定，再通过跨模态注意力动态生成融合权重 $w_c$ 和 $w_z$，得到联合条件 $j_t$：

$$j_t = w_z \hat{z}_{i+1} + w_c \hat{c}, \quad [w_z, w_c] = \mathrm{SoftMax}(\theta_j^2(\sigma(\theta_j^1(\hat{z}_{i+1} + \hat{c}))))$$

这一设计的精妙之处在于：权重是**逐样本、逐去噪步**动态推断的，而非全局固定。原文 Fig. 11 的可视化表明，在去噪早期（高噪声阶段），模型更依赖文本语义进行全局布局；而在去噪后期（低噪声阶段），模型更依赖粗运动嵌入进行细节细化。

### 3. 在文本驱动动作生成谱系中的定位

GUESS 的定位可以从以下几个维度理解：

| 维度 | 代表性方法 | GUESS 的位置 |
|------|-----------|-------------|
| 生成范式 | Seq2Seq (确定性回归) → T2M-GPT (自回归离散) → MDM/MLD (单阶段扩散) | **级联多阶段扩散** |
| 运动表示 | 原始关节序列 (MDM) / 离散 token (T2M-GPT) / 潜在嵌入 (MLD) | **多尺度潜在嵌入**（每尺度独立 VAE） |
| 条件融合 | 简单拼接或交叉注意力 (MDM/MLD) | **逐步动态加权融合** |
| 生成粒度 | 一次性生成全部关节 | **S4→S3→S2→S1 渐进细化** |

GUESS 与 **MLD**（Chen et al., CVPR 2023）共享“在潜在空间执行扩散”的思路，但 MLD 仅使用单一尺度的 VAE 和单阶段去噪，而 GUESS 将这一思路扩展为多尺度级联框架。与 **T2M-GPT**（Zhang et al., CVPR 2023）相比，GUESS 的级联生成在空间维度上由粗到细，而 T2M-GPT 的自回归生成在时间维度上逐帧展开——两者分别从空间和时间角度探索了“分而治之”的生成策略，但尚未在统一框架中结合。

### 4. 适用边界与局限

尽管 GUESS 在 HumanML3D、KIT-ML 和 UESTC 三个基准上均取得了最优结果，其设计仍存在明确的适用边界：

**（1）固定阶段数的刚性。** 当前方法对所有输入文本均采用固定的四个尺度和四个推理阶段，无论文本描述是简单的“一个人走路”还是复杂的“一个人先慢走然后突然转身跑起来并挥手”。对于简单描述，部分粗尺度阶段可能是冗余的，增加了不必要的计算开销；对于极复杂描述，四个阶段可能仍不足以充分解耦映射难度。

**（2）仅空间维度的渐进生成。** GUESS 的“由粗到细”目前仅在空间维度展开（从粗粒度身体部件到精细关节），尚未探索时间维度的渐进式生成。例如，先生成低帧率的关键姿态序列，再通过时间超分辨率补全中间帧——这种时空联合的级联策略可能进一步降低单步生成难度。

**（3）多尺度 VAE 的训练独立性。** 四个尺度的 VAE 是独立训练的，尺度间的潜在空间缺乏显式对齐约束。这可能导致粗尺度潜在嵌入 $z_4$ 中编码的运动信息与细尺度 $z_1$ 所需的条件信息之间存在语义间隙，级联去噪器需要额外学习这种隐式映射。

**（4）对极端姿态的泛化能力未充分验证。** 现有评估集中在 HumanML3D 和 KIT-ML 等相对规范的日常动作数据集，对于杂技、舞蹈等极端姿态或与训练分布差异较大的动作类型，多尺度抽象的语义保真度可能下降——粗尺度节点可能无法有效表征这些动作的关键特征。

### 5. 开放问题与后续方向

基于 GUESS 的设计逻辑和现存局限，以下几个开放问题值得关注：

1. **自适应阶段数机制。** 如何设计一个门控网络或难度评估器，使模型能根据输入文本的描述粒度和复杂度自动选择合适的推理阶段数量？这类似于“早退”机制在分类网络中的应用，但需要解决生成任务中阶段数与生成质量的非单调关系。

2. **时空联合渐进生成。** 能否将空间上的“由粗到细”扩展至时空域？例如，先生成低时间分辨率（如 5 fps）的粗粒度运动序列，再通过级联的时间超分辨率模块生成高帧率（如 20 fps）的精细运动。这需要解决时间下采样带来的运动模糊和关键帧选择问题。

3. **无分类器引导与多尺度提示的结合。** GUESS 目前未采用无分类器引导（classifier-free guidance），而该技术在文本到图像生成中已被证明能显著提升文本-图像对齐质量。如何在多尺度级联框架中设计高效的引导策略——例如在不同尺度施加不同强度的引导——是一个值得探索的方向。

4. **跨尺度潜在空间的对齐学习。** 通过对比学习或知识蒸馏，在 VAE 训练阶段显式对齐不同尺度的潜在空间，可能减少级联去噪器学习隐式映射的负担，进一步提升生成质量。

5. **更广泛的动作类型验证。** 在舞蹈、体育动作、手语等具有高度结构化或文化特定性的动作类型上验证多尺度抽象的有效性，并探索是否需要针对特定动作类型设计定制化的骨骼抽象层级。



## 原文 PDF

![[paperPDFs/TPAMI_2024/GUESS_GradUally_Enriching_SyntheSis_for_Text_Driven_Human_Motion_Generation.pdf]]
