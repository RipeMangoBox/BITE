---
title: A Unified Conditional Flow for Motion Generation, Editing, and Intra-Structural Retargeting
type: paper
paper_level: A
venue: arXiv
year: 2026
pdf_ref: paperPDFs/arxiv_2026/A_Unified_Conditional_Flow_for_Motion_Generation_Editing_and_Intra_Structural_Retargeting.pdf
project_link: null
code_link: null
aliases:
- UCFO
- UCFMGEISR
tags:
- arxiv_2026
- topic/vision_multimodal_applications
- topic/generative_models_diffusion
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: 通过调节条件信号（文本提示或目标骨骼结构）来切换任务，无需修改生成模型本身。
primary_logic: 基于联合文本和骨骼条件的流模型，编辑和重定向本质上是相同的条件传输任务，仅通过控制条件信号即可实现零样本操作。
claims:
- 模型在SnapMoGen文本生成任务上取得最佳R Precision Top1（0.917±0.001），显著超越所有基线。
- 移除关节自注意力导致FID从16.567升至17.205，表明关节级建模对生成质量至关重要。
- 运动重定向任务中，该模型FK重建误差（4.91×10⁻¹）远低于专用重定向网络R2ET（8.13×10⁻¹）。
- SnapMoGen Text-to-Motion 上 R Precision Top1 = 0.917 ± 0.001
---

# A Unified Conditional Flow for Motion Generation, Editing, and Intra-Structural Retargeting

> [!tip] 核心洞察
> 基于联合文本和骨骼条件的流模型，编辑和重定向本质上是相同的条件传输任务，仅通过控制条件信号即可实现零样本操作。

| 字段      | 内容                                                                                                                                        |
| ------- | ----------------------------------------------------------------------------------------------------------------------------------------- |
| 中文题名    | 面向运动生成、编辑与结构内重定向的统一条件流模型                                                                                                                  |
| 英文题名    | A Unified Conditional Flow for Motion Generation, Editing, and Intra-Structural Retargeting                                               |
| 会议/期刊   | arXiv 2026                                                                                                                                |
| Links   | [paper](https://arxiv.org/abs/2604.13427)                                                                                                 |
| Topic   | #topic/vision_multimodal_applications #topic/generative_models_diffusion #topic/vision_multimodal_applications/image_and_video_generation |
| Method  | Unified Conditional Flow (Ours)                                                                                                           |
| Dataset | SnapMoGen Text-to-Motion, Mixamo Retargeting, SnapMoGen Text-based Editing                                                                |

> [!tip] 效果简介
> - SnapMoGen Text-to-Motion 上，R Precision Top1 0.917 ± 0.001 vs 0.802 ± 0.001 (MoMask++) (+0.115)；FID 16.567 ± 0.045 vs 15.060 ± 0.065 (MoMask++) (+1.507)。
> - Mixamo Retargeting 上，Error (×10)↓ 4.91 (FK reconstruction) vs 8.13 (R2ET) (-3.22)。
> - SnapMoGen Text-based Editing (User Study) 上，Average Preference Rate 70% vs ~30% (vs. combined baselines) (+40%)。

## 概要

### 问题瓶颈

文本驱动的运动生成、编辑与骨骼重定向通常被视作三个独立任务，需要不同的输入格式、模型架构和训练目标。这种分离导致流程不兼容，无法在统一框架中灵活切换。核心瓶颈在于：**编辑和重定向本质上都是“保留运动语义、改变条件信号”的条件传输任务，但现有方法未能将二者统一为同一生成范式**。

### 核心思路

本文提出一种统一视角：将文本驱动的运动编辑和骨骼内重定向视为**相同的条件生成任务**，仅通过调节条件信号（文本提示或目标骨骼结构）来切换操作模式，无需修改生成模型本身。基于这一洞察，作者设计了一个**联合文本与骨骼条件的整流流（rectified flow）模型**，在单一预训练模型上实现运动生成、零样本编辑和零样本重定向。

### 方法定位

该方法在三个维度上区别于现有工作：

1. **表示层面**：采用逐关节令牌（per-joint token）替代传统的逐帧令牌，通过关节自注意力显式建模骨骼内依赖关系，使模型具备身体部位级别的生成能力。
2. **条件层面**：将目标T-pose骨骼向量作为与文本提示并列的条件信号，使重定向从几何优化问题转化为条件生成问题。
3. **推理层面**：引入统一的FlowEdit推理方案，通过计算不同条件下速度场的差异实现编辑和重定向，无需逆过程或掩码修复。

### 主要结果

- **文本生成**：在SnapMoGen基准上，R Precision Top1达到0.917±0.001，显著超越所有基线方法（次优MoMask++为0.802±0.001）。
- **运动重定向**：FK重建误差（4.91×10⁻¹）远低于专用重定向网络R2ET（8.13×10⁻¹），且模型能隐式学习目标骨骼的长度约束。
- **运动编辑**：用户研究中，该方法在源运动保留、编辑准确性和整体质量三个维度上均获得约70%的偏好率，远超对比基线（约30%）。
- **消融验证**：移除关节自注意力导致FID从16.567升至17.205，证实关节级关系建模对生成质量的关键作用；参数量相近的宽基线（90M参数，FID=17.111）仍不及含关节注意力的模型（88M参数，FID=16.567），表明增益来自结构归纳偏置而非容量增加。



### 问题背景

人类运动生成是计算机视觉与图形学的核心任务之一，其应用涵盖动画制作、虚拟现实和人机交互。近年来，基于扩散模型（diffusion models）和流匹配（flow matching）的生成方法在文本到运动（text-to-motion）任务上取得了显著进展，能够根据自然语言描述合成逼真的三维人体运动序列。然而，实际创作流程远不止从零生成——动画师通常需要**编辑已有运动**（如将“走路”改为“疲惫地走路”）或将**同一运动迁移到不同骨骼结构的角色**上（即运动重定向，motion retargeting）。

### 现有方法的碎片化困境

当前方法在处理这三个核心任务时呈现出明显的碎片化特征：

**文本到运动生成**方面，主流方法包括基于扩散的**MDM**（Tevet et al., ICLR 2023）、基于VQ-VAE的**T2M-GPT**（Zhang et al., CVPR 2023）和**MoMask**（Guo et al., CVPR 2024），以及基于流匹配的**StableMoFusion**（Huang et al., arXiv 2024）等。这些模型仅接受文本条件，无法处理骨骼结构变化。

**运动编辑**通常采用两类策略：一是基于掩码的扩散修复方法（如MDM的编辑模式），在指定时间窗口内替换运动片段，但容易在掩码边界引入僵硬感；二是重新生成方法（如**MoMask++**，Guo et al., arXiv 2025），根据编辑后的文本重新合成运动，但往往偏离源运动的语义结构。

**运动重定向**则长期被视为几何优化问题，代表性工作包括**SAN**（Aberman et al., ACM TOG 2020）、**SAME**（Lee et al., SIGGRAPH Asia 2023）和**R2ET**（Zhang et al., CVPR 2023）。这些专用网络需要成对的源-目标运动数据进行监督训练，且与生成、编辑流程完全不兼容。

### 核心瓶颈

上述碎片化格局揭示了一个深层瓶颈：**文本驱动的运动编辑和结构内骨骼重定向通常采用分离的、不兼容的流程，不同任务需要不同的输入、目标和表示，导致无法在统一模型中灵活处理**。具体表现为：

1. **表示不统一**：生成模型使用全局运动特征，重定向网络依赖关节级几何约束，编辑方法则关注时间局部性。
2. **条件空间割裂**：文本条件与骨骼条件从未在同一生成框架中被联合建模。
3. **推理范式互斥**：生成需要从噪声采样，编辑需要部分保留源运动，重定向需要几何适配——三者缺乏共享的推理机制。

### 本文动机

本文提出一个统一视角：**基于联合文本和骨骼条件的流模型，编辑和重定向本质上是相同的条件传输任务，仅通过控制条件信号即可实现零样本操作**。具体而言：

- 将运动重定向重新定义为**条件生成问题**，而非几何优化——目标骨骼（由骨骼长度和T-pose定义）作为“风格”或“域”条件，运动语义作为“内容”。
- 设计单一矫正流（rectified flow）模型，联合接受**文本提示**和**目标角色T-pose**作为条件，通过调节条件信号（文本提示或目标骨骼结构）来切换任务，无需修改生成模型本身。
- 引入统一的**FlowEdit推理方案**，无需显式反演步骤，通过组合不同条件下的速度场预测实现编辑和重定向。

这种方法论转变使得一个预训练模型即可覆盖生成、编辑和重定向三个任务，消除了传统流水线中的任务专用模块和手工几何约束。



## 核心方法与创新机理

### 问题瓶颈：多任务的流程割裂

文本驱动的运动生成、编辑与骨骼重定向通常被视为三个独立任务，各自依赖不同的输入格式、优化目标和表示空间。例如，生成模型仅以文本为条件，编辑方法需额外指定掩码或源运动，而重定向则依赖成对骨骼数据与几何约束。这种**流程割裂**导致三个根本性问题：其一，不同任务间无法共享模型能力，每项任务均需独立训练专用网络；其二，编辑与重定向往往需要显式逆映射或掩码修补，引入额外的误差累积；其三，缺乏统一的表征使得“改变条件即可切换任务”的零样本操作难以实现。

### 核心洞察：条件传输的统一视角

本文的核心洞察在于：**文本驱动的运动编辑和骨骼结构内重定向本质上是同一类条件传输任务**——它们都旨在将源运动分布传输到由新条件（修改后的文本或目标骨骼）指定的目标分布，区别仅在于被调制的条件信号不同。基于这一视角，编辑和重定向不再需要分离的任务模块，而可以通过**控制条件信号（文本提示或目标骨骼结构）来切换任务，无需修改生成模型本身**。

### 关键设计：三个Changed Slots

为实现上述统一，本文在基线方法的基础上进行了三项关键改动，构成方法的核心创新：

**1. 令牌表示：从逐帧令牌到逐关节令牌**

基线方法（如MDM、T2M-GPT等）通常将每帧运动特征编码为单个令牌，关节间的依赖关系被隐式混合在帧级表示中。本文改为**逐关节令牌（per-joint token）**表示：每帧特征被投影并重塑为 $J$ 个关节令牌，每个令牌维度为 $d = D_h / J$（参见Eq. (3)）。在此基础上，引入**关节自注意力（Joint Self-Attention）**在同一帧内显式建模骨骼内关节间的依赖关系（Eq. (4)）。消融实验（Table 2）证实，移除关节自注意力导致FID从16.567升至17.205，验证了关节级关系建模对运动自然度的关键作用。值得注意的是，即使将基线参数量扩大至90M（宽基线hidden dim 576），其FID（17.111）仍不及含关节注意力的88M模型（16.567），表明性能增益来自**结构归纳偏置**而非单纯容量提升。

**2. 条件输入：从单一文本到文本-骨骼联合条件**

现有文本到运动生成模型仅以文本提示为条件。本文在条件空间中引入**目标T-pose骨骼向量**作为第二条件信号（Sec. 3.1），与扩散时间嵌入融合为统一条件向量 $\mathbf{c}$（Eq. (5)），通过AdaLN调制注入Transformer的每一层。骨骼向量编码了目标角色的骨骼长度与静止姿态信息，使模型在训练阶段即学会将“骨骼”视为一种可切换的风格条件。这一设计使得推理时仅需更换骨骼条件即可实现零样本重定向，无需任何额外微调。

**3. 编辑方法：从任务专用模块到统一FlowEdit**

基线编辑方法（如MDM的掩码修补、MoMask++的再生式编辑）依赖任务特定的推理流程。本文采用**统一FlowEdit集成**：编辑被形式化为沿共享噪声路径积分两个条件下的速度差异（Eq. (13)）。具体而言，给定源运动 $\mathbf{x}$ 和源条件 $c_s$，目标条件 $c_t$ 下的编辑运动 $\mathbf{y}$ 通过求解ODE获得，其速度场为目标条件速度与源条件速度之差。该方法**无需显式逆映射或掩码**，编辑与重定向共享完全相同的推理框架——仅需将 $c_t$ 替换为修改后的文本或目标骨骼即可。用户研究（Figure 4）显示，该方法在三项感知指标上均获得约70%的平均偏好率，显著优于MDM和MoMask++的编辑模式。

### 方法谱系与知识库定位

本工作处于**条件运动生成**与**整流流模型**的交叉点。在生成架构上，继承了DiT式Transformer骨干与扩散/流匹配范式，与**MDM**（Tevet et al., ICLR 2023）、**T2M-GPT**（Zhang et al., CVPR 2023）、**MoMask**（Guo et al., CVPR 2024）等基于VQ-VAE或扩散的文本到运动方法共享技术脉络，但通过逐关节令牌与骨骼条件实现了对骨骼结构的显式建模。在流模型层面，采用**整流流匹配**（rectified flow matching），以线性插值路径 $\mathbf{x}_\tau = (1-\tau)\mathbf{x}_0 + \tau\mathbf{x}_1$ 替代传统扩散的随机微分方程，训练目标为预测干净数据 $\hat{\mathbf{x}}_1$（Eq. (9)-(10)）。在编辑机制上，FlowEdit（Kulikov et al., 2025）提供了无需逆映射的条件传输框架，本文将其首次应用于运动域，并扩展至骨骼条件的切换。

与专用重定向网络（如**SAN**（Aberman et al., ACM TOG 2020）、**SAME**（Lee et al., SIGGRAPH Asia 2023）、**R2ET**（Zhang et al., CVPR 2023））相比，本文方法将重定向重新定义为条件生成问题，而非几何优化或成对数据学习问题，从而在统一的生成框架内实现了零样本重定向。Table 3显示，该方法FK重建误差（$4.91 \times 10^{-1}$）显著低于专用重定向网络R2ET（$8.13 \times 10^{-1}$），验证了条件生成视角的有效性。



本文提出一种统一条件流模型，将运动生成、文本驱动编辑和结构内骨骼重定向三个任务收敛到单一框架中。其核心思想是：**编辑和重定向本质上是相同的条件传输问题**——区别仅在于调节哪个条件信号（文本提示或目标骨骼结构），而生成模型本身无需修改。基于这一视角，系统由三个协同组件构成：双条件 Transformer 骨干网络、条件整流流训练策略，以及统一的 FlowEdit 推理方案。

### 数据流与特征空间

模型在拼接特征空间中运行。每一运动帧被表示为一个联合向量：

$$\mathbf{x}_t = [\mathbf{x}_t^{\mathrm{gen}}; \mathbf{x}_t^{\mathrm{ret}}], \quad \mathbf{x}_t^{\mathrm{gen}} \in \mathbb{R}^{D_{\mathrm{gen}}}, \mathbf{x}_t^{\mathrm{ret}} \in \mathbb{R}^{D_{\mathrm{ret}}}$$

其中 $\mathbf{x}_t^{\mathrm{gen}}$ 为生成特征（用于标准评估指标），$\mathbf{x}_t^{\mathrm{ret}}$ 为重定向特征，后者包含每关节的根相对位置、6D旋转和速度：

$$\mathbf{x}_{t,j}^{\mathrm{ret}} = [\mathbf{p}_{t,j}; \mathbf{r}_{t,j}^{6\mathrm{D}}; \mathbf{v}_{t,j}] \in \mathbb{R}^{12}$$

这种双块设计使模型同时学习语义运动质量（生成块）和几何约束（重定向块），为后续统一推理奠定基础。

### 骨干网络：逐关节令牌的 Transformer

模型采用 DiT 风格的 Transformer 骨干，同时接受文本和骨骼两个条件信号。其关键设计在于**将每帧特征投影为逐关节令牌**，显式建模骨骼内部的关节级依赖关系。具体流程为：

1. **输入投影**：将输入状态 $\mathbf{X}_t$ 通过线性层投影并重塑为 $J$ 个关节令牌，每个维度为 $d = D_h / J$：
   $$\mathbf{H}_t = \mathrm{reshape}(\mathbf{W}_{\mathrm{in}} \mathbf{X}_t + \mathbf{b}_{\mathrm{in}}) \in \mathbb{R}^{J \times d}$$

2. **关节自注意力**：在同一帧内对关节令牌执行自注意力，使用 AdaLN 进行条件化调制，并施加残差门控 $g_{\mathrm{jnt}}(\mathbf{c})$：
   $$\mathbf{H}_{t,\cdot} \gets \mathbf{H}_{t,\cdot} + g_{\mathrm{jnt}}(\mathbf{c}) \cdot \mathrm{Attn}_{\mathrm{jnt}}(\mathrm{AdaLN}(\mathbf{H}_{t,\cdot}, \mathbf{c}))$$

3. **跨注意力与帧注意力**：在关节分辨率上通过交叉注意力注入文本特征；随后在时间维度对帧令牌执行自注意力，并再次通过帧级交叉注意力注入文本。

4. **骨骼与时间注入**：扩散时间步和骨骼嵌入通过 AdaLN 调制注入网络：
   $$\mathbf{c} = \phi(\mathbf{c}_\tau + \mathbf{c}_s) \in \mathbb{R}^{D_h}$$

5. **输出投影**：将归一化后的关节令牌投影回运动特征维度：
   $$\hat{\mathbf{x}}_1 = \mathbf{W}_{\mathrm{out}} \mathrm{reshape}(\mathrm{Norm}(\mathbf{H})) + \mathbf{b}_{\mathrm{out}}$$

消融实验验证了关节自注意力的关键作用：移除该模块后，FID 从 16.567 升至 17.205（Table 2），证明关节级关系建模对运动自然度至关重要。此外，参数量相近的宽基线（90M 参数，FID 17.111）仍不及含关节注意力的模型（88M 参数，FID 16.567），表明增益来自结构归纳偏置而非容量增加。

### 训练：条件整流流匹配

训练采用整流流匹配，定义从噪声到数据的线性插值路径：

$$\mathbf{x}_\tau = (1 - \tau) \mathbf{x}_0 + \tau \mathbf{x}_1$$

其真实速度为 $\mathbf{u}^\star = \mathbf{x}_1 - \mathbf{x}_0$。模型学习预测干净目标 $\hat{\mathbf{x}}_1$，并通过以下公式转换为速度场用于推理：

$$\mathbf{v}_\theta(\mathbf{x}_\tau, \tau; P, S) = \frac{\hat{\mathbf{x}}_1 - \mathbf{x}_\tau}{1 - \tau}$$

损失函数在生成块和重定向块上分别计算 MSE：

$$\mathcal{L}_{\mathrm{simple}} = \lambda_{\mathrm{gen}} \mathbb{E} \big[ \| \mathbf{f}_\theta^{\mathrm{gen}} - \mathbf{x}_1^{\mathrm{gen}} \|^2 \big] + \lambda_{\mathrm{ret}} \mathbb{E} \big[ \| \mathbf{f}_\theta^{\mathrm{ret}} - \mathbf{x}_1^{\mathrm{ret}} \|^2 \big]$$

### 统一推理：FlowEdit 方案

推理时，三个任务共享同一预训练模型，仅通过切换条件信号实现零样本操作：

- **生成**：给定文本 $P$ 和骨骼 $S$，从噪声出发沿整流流路径积分。
- **编辑**：保持骨骼不变，仅将文本条件从 $c_s$ 切换为 $c_t$。
- **重定向**：保持文本不变，仅将骨骼条件切换为目标骨骼。

编辑和重定向均采用 FlowEdit 方案，无需显式反演。定义共享噪声轨迹：

$$\tilde{\mathbf{x}}_\tau = (1 - \tau)\boldsymbol{\epsilon}_\tau + \tau\mathbf{x}, \quad \boldsymbol{\epsilon}_\tau \sim N(0,\mathbf{I})$$

编辑通过积分目标条件与源条件下的速度差实现：

$$\frac{d\mathbf{y}_\tau}{d\tau} = \mathbf{v}_{\mathrm{CFG}}(\mathbf{y}_\tau + \tilde{\mathbf{x}}_\tau - \mathbf{x}, \tau; c_t) - \mathbf{v}_{\mathrm{CFG}}(\tilde{\mathbf{x}}_\tau, \tau; c_s)$$

多条件分类器无关引导用于组合无条件速度与各条件速度：

$$\mathbf{v}_{\mathrm{CFG}} = \mathbf{v}_u + \sum_k w_k (\mathbf{v}_k - \mathbf{v}_u)$$

这一统一推理方案使模型在三个任务上均展现出竞争力：文本生成任务中 R Precision Top1 达到 0.917（Table 1），重定向任务中 FK 重建误差（$4.91 \times 10^{-1}$）显著低于专用重定向网络 R2ET（$8.13 \times 10^{-1}$，Table 3），用户研究中编辑偏好率达 70%（Figure 4）。

### 补充图表

![[assets/figures/papers/paper_list_l43_https_arxiv_org_abs_2604_13427/figures/001_Figure_1.jpg]]
*Figure 1: One rectified-flow model unifies motion generation, editing, and intra-structural retargeting. Conditioned on text and skeleton, it enables (left) generation, (middle) zero-shot editing by changing only the text condition, and (right) zero-shot retargeting by changing only the skeleton condition*

![[assets/figures/papers/paper_list_l43_https_arxiv_org_abs_2604_13427/figures/002_Figure_2.jpg]]
*Figure 2: Model Architecture. Input frame tokens are reshaped into per-joint tokens for processing. Time and skeleton conditions are injected via AdaLN, while text embeddings are integrated through cross-attention*



### 3.1 统一条件流模型概述

该方法的核心思想是将文本驱动的运动编辑和骨骼重定向统一为同一条件生成任务——区别仅在于调节哪个条件信号（文本提示或目标骨骼T-pose），而无需修改生成模型本身。整个框架由三个集成组件构成：**双条件Transformer骨干网络**、**条件整流流训练策略**、以及**统一FlowEdit推理方案**（见 Figure 2 和 Figure 3）。

![[assets/figures/papers/paper_list_l43_https_arxiv_org_abs_2604_13427/figures/003_Figure_3.jpg]]
*Figure 3: Applications of our unified inference scheme. Left: text-based editing by changing the text condition. Right: intra-structural retargeting by changing only the skeleton condition. Both use the same pre-trained model and an inversion-free update rule, where the edit velocity is obtained by combining velocity predictions under different conditions*

模型操作于一个拼接特征空间，将每个运动帧表示为生成特征和重定向特征的拼接：

$$
\mathbf{x}_t = [\mathbf{x}_t^{\mathrm{gen}}; \mathbf{x}_t^{\mathrm{ret}}], \quad \mathbf{x}_t^{\mathrm{gen}} \in \mathbb{R}^{D_{\mathrm{gen}}}, \mathbf{x}_t^{\mathrm{ret}} \in \mathbb{R}^{D_{\mathrm{ret}}}
$$

其中生成特征 $\mathbf{x}_t^{\mathrm{gen}}$ 用于标准评估指标，重定向特征 $\mathbf{x}_t^{\mathrm{ret}}$ 提供逐关节的几何控制信息。重定向特征定义为：

$$
\mathbf{x}_{t,j}^{\mathrm{ret}} = [\mathbf{p}_{t,j}; \mathbf{r}_{t,j}^{6\mathrm{D}}; \mathbf{v}_{t,j}] \in \mathbb{R}^{12}
$$

每个关节 $j$ 的特征包含：根相对关节位置 $\mathbf{p}_{t,j}$、6D旋转表示 $\mathbf{r}_{t,j}^{6\mathrm{D}}$ 和速度 $\mathbf{v}_{t,j}$。这种设计使模型在统一表示下同时掌握运动语义和骨骼几何约束。

### 3.2 双条件Transformer骨干网络

骨干网络采用DiT风格的Transformer架构，同时接受文本和骨骼条件。关键创新在于**逐关节令牌（per-joint token）**机制，将每帧特征显式分解为关节级表示，以鼓励身体部位级别的生成。

**输入投影**：将输入状态 $\mathbf{X}_t$ 投影并重塑为 $J$ 个关节令牌，每个维度为 $d$：

$$
\mathbf{H}_t = \mathrm{reshape}(\mathbf{W}_{\mathrm{in}} \mathbf{X}_t + \mathbf{b}_{\mathrm{in}}) \in \mathbb{R}^{J \times d}, \quad d = \frac{D_h}{J}
$$

**关节自注意力**：在同一帧内对关节令牌执行自注意力，显式建模骨骼内依赖关系，并使用AdaLN条件化和残差门控：

$$
\mathbf{H}_{t,\cdot} \gets \mathbf{H}_{t,\cdot} + g_{\mathrm{jnt}}(\mathbf{c}) \cdot \mathrm{Attn}_{\mathrm{jnt}}(\mathrm{AdaLN}(\mathbf{H}_{t,\cdot}, \mathbf{c}))
$$

其中条件向量 $\mathbf{c}$ 融合了扩散时间嵌入和骨骼嵌入：

$$
\mathbf{c} = \phi(\mathbf{c}_\tau + \mathbf{c}_s) \in \mathbb{R}^{D_h}
$$

**文本注入**：通过关节-文本交叉注意力和帧-文本交叉注意力两个层次注入文本特征，分别在关节分辨率和帧级实现语义对齐。

**输出投影**：处理后的关节令牌经归一化后投影回运动特征维度：

$$
\hat{\mathbf{x}}_1 = \mathbf{W}_{\mathrm{out}} \mathrm{reshape}(\mathrm{Norm}(\mathbf{H})) + \mathbf{b}_{\mathrm{out}}
$$

### 3.3 条件整流流训练

训练采用整流流匹配（rectified flow matching），定义从噪声到数据的线性插值路径：

$$
\mathbf{x}_\tau = (1 - \tau) \mathbf{x}_0 + \tau \mathbf{x}_1
$$

其真实速度为路径导数：

$$
{\mathbf{u}}^\star = \frac{d \mathbf{x}_\tau}{d \tau} = \mathbf{x}_1 - \mathbf{x}_0
$$

推理时，将模型预测的干净目标转换为速度场：

$$
\mathbf{v}_\theta(\mathbf{x}_\tau, \tau; P, S) = \frac{\hat{\mathbf{x}}_1 - \mathbf{x}_\tau}{1 - \tau}
$$

训练损失在生成和重定向两个特征块上分别计算MSE：

$$
\mathcal{L}_{\mathrm{simple}} = \lambda_{\mathrm{gen}} \mathbb{E} \big[ \| \mathbf{f}_\theta^{\mathrm{gen}} - \mathbf{x}_1^{\mathrm{gen}} \|^2 \big] + \lambda_{\mathrm{ret}} \mathbb{E} \big[ \| \mathbf{f}_\theta^{\mathrm{ret}} - \mathbf{x}_1^{\mathrm{ret}} \|^2 \big]
$$

多条件分类器无关引导（multi-condition CFG）组合无条件速度与多个条件速度：

$$
\mathbf{v}_{\mathrm{CFG}} = \mathbf{v}_u + \sum_k w_k (\mathbf{v}_k - \mathbf{v}_u)
$$

### 3.4 统一FlowEdit推理

FlowEdit的核心思想是构造源条件分布与目标条件分布之间的直接传输ODE，无需显式反演或经过纯噪声的往返过程。编辑通过沿共享噪声路径积分两个条件下的速度差异实现。

**共享噪声轨迹**定义：

$$
\tilde{\mathbf{x}}_\tau = (1 - \tau)\boldsymbol{\epsilon}_\tau + \tau\mathbf{x}, \quad \boldsymbol{\epsilon}_\tau \sim N(0,\mathbf{I})
$$

**FlowEdit更新规则**：积分目标条件与源条件下的速度差异，实现编辑或重定向：

$$
\frac{d\mathbf{y}_\tau}{d\tau} = \mathbf{v}_{\mathrm{CFG}}(\mathbf{y}_\tau + \tilde{\mathbf{x}}_\tau - \mathbf{x}, \tau; c_t) - \mathbf{v}_{\mathrm{CFG}}(\tilde{\mathbf{x}}_\tau, \tau; c_s)
$$

该公式的关键在于：**仅需切换条件信号**（$c_t$ 为目标条件，$c_s$ 为源条件），同一预训练模型即可在零样本设定下完成文本编辑（改变文本条件）或骨骼重定向（改变骨骼条件），无需任何任务特定的微调或架构修改。



## 实验与关键发现

### 文本驱动运动生成主结果

在SnapMoGen测试集上，所提统一条件流模型在语义对齐指标上取得全面领先。**Table 1** 显示，R Precision Top1 达到 **0.917±0.001**，较第二名 **MoMask++**（Guo et al., arXiv 2025）的 0.802±0.001 提升 **+0.115**，Top2（0.973±0.001）和 Top3（0.991±0.001）同样最优。这表明联合文本-骨骼条件与逐关节令牌设计有效捕获了细粒度语义。

![[assets/figures/papers/paper_list_l43_https_arxiv_org_abs_2604_13427/figures/004_Table_1.jpg]]
*Table 1: Text-to-motion generation quantitative evaluation on the SnapMoGen test split. Baseline numbers are taken from SnapMoGen (mean ± 95% CI). Bold and underlined numbers indicate the best and second-best results, respectively*

FID 方面，模型取得 16.567±0.045，略逊于 MoMask++ 的 15.060±0.065（差距 +1.507）。这一差距可归因于方法目标不同：MoMask++ 专精于生成质量优化，而本模型在统一框架下同时承担生成、编辑与重定向任务，FID 的轻微折衷是任务泛化性的合理代价。多样性（Diversity）和 multimodality 指标上，模型均处于健康区间，未出现模式坍塌。

对比基线覆盖扩散模型（**MDM**, Tevet et al., ICLR 2023）、自回归模型（**T2M-GPT**, Zhang et al., CVPR 2023）、流匹配模型（**StableMoFusion**, Huang et al., arXiv 2024; **MARDM**, Meng et al., arXiv 2024）及掩码模型（**MoMask**, Guo et al., CVPR 2024），评估遵循 SnapMoGen 统一协议，基线数值直接引用原论文报告的均值与95%置信区间，确保公平性。

### 消融实验

**Table 2** 的消融实验揭示了两个关键设计的作用。

**关节自注意力的核心贡献。** 移除关节自注意力（w/o jnt attn）导致 FID 从 16.567 升至 17.205，R Precision Top1 从 0.917 降至 0.911。这一退化验证了关节级关系建模对运动自然度的因果作用——同一帧内不同关节的依赖关系（如手臂与躯干的协调）无法被帧级注意力充分捕获。

**容量与结构偏置的分离。** 为排除参数量增加的混淆效应，实验构建了隐藏维度 576 的宽基线（90M 参数，无关节注意力），其 FID 为 17.111，仍不及含关节注意力的标准模型（88M 参数，FID 16.567）。这证明性能增益来自关节级建模的结构归纳偏置，而非单纯的容量扩展。

### 运动重定向评估

在 Mixamo 测试集上，模型展现出强大的零样本重定向能力。**Table 3** 显示，基于 FK 重建的误差仅为 **4.91×10⁻¹**，显著低于专用重定向网络 **R2ET**（Zhang et al., CVPR 2023）的 8.13×10⁻¹（降低 39.6%），也优于几何优化方法 **SAN**（Aberman et al., ACM TOG 2020）和 **SAME**（Lee et al., SIGGRAPH Asia 2023）。

![[assets/figures/papers/paper_list_l43_https_arxiv_org_abs_2604_13427/figures/005_Table_3.jpg]]
*Table 3: Retargeting evaluation on the Mixamo test split*

值得关注的是，即使采用直接位置预测而不使用 FK 重建，模型仍达到较低误差（5.24×10⁻¹），表明其已隐式学会目标骨骼的骨骼长度约束——这是统一条件建模带来的涌现能力，而非显式几何约束的结果。

### 文本驱动运动编辑用户研究

**Figure 4** 的感知用户研究从源运动保留（Pres.）、编辑准确性（Edit）和整体质量（Over.）三个维度评估。与 **MDM**（Tevet et al., ICLR 2023）比较时，偏好率分别为 65%/78%/77%；与 **MoMask++** 比较时为 75%/75%/72%；与掩码消融基线比较时为 46%/70%/63%。平均偏好率约 **70%**，显著高于组合基线约 30% 的水平。

定性结果（**Figure 7**）进一步显示，掩码方法（MDM）在掩码边界处易引入僵硬伪影，再生式基线（MoMask++）常偏离源运动语义，而本方法通过 FlowEdit 的差分速度积分机制，在保持叙事结构的同时实现准确编辑。

### 失败模式与局限

尽管整体性能优异，模型在以下场景存在已知局限：

1. **极端形态变化：** 当前实现假设关节顺序一致且每个目标角色需提供定义良好的 T-pose。对于非人形角色或骨骼拓扑差异过大的情况，统一的关节令牌表示可能失效。
2. **分布外运动：** 高度分布外运动（如攀爬、翻滚）在重定向时可能产生不自然的关节扭转或拉伸，这与训练数据覆盖范围直接相关。
3. **长文本编辑显著性不足：** 过长的文本提示在编辑时可能引入微小的速度差异，导致编辑效果不明显——这是 FlowEdit 框架在条件差异较小时的固有挑战，需通过调整 CFG 引导强度或引入迭代编辑策略改善。

这些局限指向了框架的扩展方向：跨拓扑重定向、无 T-pose 条件下的推理、以及更精细的编辑控制机制。

### 补充图表

![[assets/figures/papers/paper_list_l43_https_arxiv_org_abs_2604_13427/figures/006_Table_2.jpg]]
*Table 2: Ablation study of the generation task on the SnapMoGen test split*

![[assets/figures/papers/paper_list_l43_https_arxiv_org_abs_2604_13427/figures/007_Figure_4.jpg]]
*Figure 4: Perceptual user study. Pairwise preferences (Ours/Equal/Baseline) for Source Preservation (Pres.), Edit Accuracy (Edit), and Overall Quality (Over.). Ours is preferred across all three criteria vs. MDM [Tevet et al. 2023] (65/78/77%), MoMask++ [Guo et al. 2025] (75/75/72%), and the mask-based ablation (46/70/63%) (Pres./Edit/Over.)*

![[assets/figures/papers/paper_list_l43_https_arxiv_org_abs_2604_13427/figures/008_Figure_5.jpg]]
*Figure 5: Qualitative comparison on text-to-motion generation. For visualization, motions with little or no root translation are manually time-shifted. Prompt words in red denote actions, while words in green indicate motion modifiers. Our model successfully synthesizes coherent full-body motions that faithfully reflect fine-grained textual details over long time spans. This temporal coherence is critical for our downstream editing tasks, where the model must preserve the narrative structure of the source motion*

![[assets/figures/papers/paper_list_l43_https_arxiv_org_abs_2604_13427/figures/011_Figure_6.jpg]]
*Figure 6: Qualitative retargeting comparison. We compare against SAN [Aberman et al. 2020], SAME [Lee et al. 2023], and R2ET [Zhang et al. 2023a]. The proposed method better preserves fine-grained local motion and adapts to varying skeleton proportions. As highlighted in the zoomed-in regions, baseline methods often introduce artifacts such as unnatural twisting or over-stretching when adapting to different skeletons. In contrast, our method preserves delicate local details (e.g., leg bending scale, hand facing direction) while naturally adapting the global motion to fit the new body shape*



## 定位与知识库关联

### 核心问题与范式转换

文本驱动的运动生成、编辑与骨骼重定向长期处于分离的技术路线：生成模型以文本为条件合成运动序列，编辑方法依赖掩码修复或重生成策略，重定向则被建模为几何优化问题。这些任务的输入、目标与表示互不兼容，导致无法在统一框架内灵活切换。本文提出一个根本性的范式转换——将文本编辑与骨骼重定向统一视为**条件传输任务**，二者仅在调节的条件信号（文本提示或目标骨骼结构）上存在差异，生成模型本身无需任何修改。

这一视角的技术基础是**校正流（Rectified Flow）**框架：模型学习从噪声到数据的线性速度场，推理时沿直线路径积分。当需要切换任务时，只需改变条件信号并利用**FlowEdit**机制——通过积分目标条件与源条件下的速度差异，构建直接传输ODE，无需显式反演或穿越纯噪声空间。这种“一次训练，零样本多任务”的设计，从根本上消除了任务特定模块的需求。

### 与生成基线的结构差异

主流文本-运动生成模型可分为扩散模型与自回归模型两条路线。**MDM**（Tevet et al., ICLR 2023）采用逐帧令牌的扩散架构，隐式混合所有关节信息；**T2M-GPT**（Zhang et al., CVPR 2023）和**MoMask**（Guo et al., CVPR 2024）则基于VQ-VAE的离散令牌自回归生成。这些方法的核心局限在于：令牌表示层面缺乏对骨骼内部结构的显式建模，且条件空间仅包含文本，无法自然扩展至重定向任务。

本文方法的关键改造体现在三个层面：

1. **令牌表示**：从逐帧令牌切换为**逐关节令牌**，每帧的 $J$ 个关节独立编码为 $d$ 维令牌（$\mathbf{H}_t \in \mathbb{R}^{J \times d}$，Eq. 3），使模型能够显式建模同一帧内不同关节间的依赖关系。

2. **注意力架构**：引入**关节自注意力**（Joint Self-Attention，Eq. 4），在同一帧内对关节令牌执行自注意力，辅以AdaLN条件化注入骨骼和时间信息。这一设计为模型提供了骨骼拓扑的归纳偏置，使其能感知关节间的运动学约束。

3. **条件空间**：将条件从单一文本提示扩展为**文本+目标T-pose骨骼向量**的联合条件（Eq. 5），使同一模型能响应文本语义和骨骼结构两类信号。

消融实验（Table 2）直接验证了关节自注意力的因果效应：移除该模块后，FID从16.567升至17.205，生成质量显著下降。更重要的是，参数量相近的宽基线（hidden dim 576，90M参数，FID 17.111）仍不及含关节注意力的模型（88M参数，FID 16.567），证明性能增益来自结构归纳偏置而非单纯容量增加。

### 与编辑/重定向基线的对比

**运动编辑**领域，现有方法主要依赖两类策略：掩码修复（如MDM的编辑模式，在指定时间区间内修复运动）或重生成（如MoMask++，Guo et al., arXiv 2025，基于编辑文本重新生成完整序列）。掩码修复方法在掩码边界常引入僵硬感，重生成方法则容易偏离源运动的语义结构。本文的FlowEdit方案通过速度差异积分（Eq. 13）实现编辑，无需掩码或重生成，用户研究（Figure 4）显示该方法在源运动保留（65% vs. MDM）、编辑准确性（78% vs. MDM）和整体质量（77% vs. MDM）三个维度上均获显著偏好。

**运动重定向**领域，专用方法如**SAN**（Aberman et al., ACM TOG 2020）、**SAME**（Lee et al., SIGGRAPH Asia 2023）和**R2ET**（Zhang et al., CVPR 2023）将重定向建模为几何优化或专用网络映射问题。本文方法以FK重建误差（$4.91 \times 10^{-1}$）显著优于R2ET（$8.13 \times 10^{-1}$），且即使采用直接位置预测而非FK重建（误差$5.24 \times 10^{-1}$），仍保持较低误差，表明模型已隐式学会目标骨骼的长度约束。定性对比（Figure 6）进一步揭示，基线方法在适应不同骨骼比例时常引入非自然扭曲或过度拉伸等伪影，而本文方法能保留精细局部细节（如腿部弯曲幅度、手掌朝向）的同时自然适配新体型。

### 适用边界与局限

当前实现的适用性建立在三个前提之上：关节顺序在源与目标骨骼间保持一致；每个目标角色需提供定义良好的T-pose作为骨骼代理；运动数据以标准的人形骨骼拓扑为基础。这些假设在以下场景中可能失效：

- **极端形态变化**：非人形角色（如四足动物、多足生物）的骨骼拓扑与训练分布差异过大，模型难以泛化。
- **高度分布外运动**：如攀爬、翻滚等与常见运动模式显著偏离的动作，生成质量和重定向精度可能下降。
- **长文本编辑的显著性**：过长的文本提示在编辑时可能引入微小的速度差异，导致编辑效果不明显，需进一步研究如何增强长文本条件下的编辑可控性。

### 开放问题与潜在延伸

1. **跨拓扑重定向**：当前方法假设关节顺序一致，能否扩展至不同骨骼图结构（如不同关节数量、不同连接关系）的跨拓扑重定向？这可能需要引入图神经网络或注意力掩码机制来处理可变拓扑。

2. **部分骨骼信息处理**：当目标角色仅提供部分骨骼信息或无T-pose时，如何利用可用的部分约束完成重定向？这涉及缺失条件下的条件生成问题。

3. **物理合理性增强**：能否融合mesh信息或物理模拟约束，以改善重定向结果的物理合理性（如避免穿透、保持接触约束）？当前方法仅依赖运动学特征，未显式建模动力学约束。

4. **编辑显著性与可控性**：如何提升长文本编辑的显著性和精细度控制？可能需要引入层次化条件注入或编辑强度调节机制。

5. **多模态条件扩展**：框架的条件空间可进一步扩展至音频、场景几何等多模态信号，实现更丰富的运动控制。



## 原文 PDF

![[paperPDFs/arxiv_2026/A_Unified_Conditional_Flow_for_Motion_Generation_Editing_and_Intra_Structural_Retargeting.pdf]]
