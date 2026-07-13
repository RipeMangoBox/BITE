---
title: "From 2D Alignment to 3D Plausibility: Unifying Heterogeneous 2D Priors and Penetration-Free Diffusion for Occlusion-Robust Two-Hand Reconstruction"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/From_2D_Alignment_to_3D_Plausibility_Unifying_Heterogeneous_2D_Priors_and_Penetration_Free_Diffusion_for_Occlusion_Robust_Two_Hand_Reconstruction.pdf
project_link: "https://gaogehan.github.io/A2P/"
code_link: null
aliases:
- AF2A3P
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
- topic/generative_models_diffusion
- topic/representation_self_supervised_transfer
core_operator: 将问题解耦为2D结构先验对齐和3D空间交互精修，利用融合对齐编码器在训练时蒸馏异构先验，并在推理时通过带碰撞梯度引导的扩散模型实现免穿透生成。
primary_logic: 通过训练时统一关键点、分割和深度等异构2D先验知识并蒸馏到轻量编码器，结合双手免穿透扩散模型和碰撞梯度引导，使模型能够在无额外推理开销下实现物理合理的遮挡鲁棒双手重建。
claims:
- 将双手重建解耦为2D结构对齐和3D空间交互对齐两个阶段
- 首次统一异构2D先验（关键点、分割、深度）用于双手重建，并通过轻量融合对齐编码器在训练时蒸馏
- 引入双手免穿透扩散模型，学习从穿透姿态到无碰撞姿态的生成映射，并引入碰撞梯度引导
- 在InterHand2.6M上与最强基线相比，MPJPE从7.40mm降至5.36mm，MRRPE从24.58mm降至21.60mm
---

# From 2D Alignment to 3D Plausibility: Unifying Heterogeneous 2D Priors and Penetration-Free Diffusion for Occlusion-Robust Two-Hand Reconstruction

> [!tip] 核心洞察
> 通过训练时统一关键点、分割和深度等异构2D先验知识并蒸馏到轻量编码器，结合双手免穿透扩散模型和碰撞梯度引导，使模型能够在无额外推理开销下实现物理合理的遮挡鲁棒双手重建。

| 字段 | 内容 |
|------|------|
| 中文题名 | 从2D对齐到3D合理性：统一异构2D先验与免穿透扩散的遮挡鲁棒双手重建 |
| 英文题名 | From 2D Alignment to 3D Plausibility: Unifying Heterogeneous 2D Priors and Penetration-Free Diffusion for Occlusion-Robust Two-Hand Reconstruction |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2503.17788) · [Project](https://gaogehan.github.io/A2P/) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction #topic/generative_models_diffusion #topic/representation_self_supervised_transfer |
| Method | A2P (From 2D Alignment to 3D Plausibility) |
| Dataset | InterHand2.6M |

> [!tip] 效果简介
> - InterHand2.6M (5fps) 上，MRRPE (mm) 21.60 vs 24.58 (4DHands) (-2.98)；MPJPE (mm) 5.36 vs 7.40 (4DHands) (-2.04)；MPVPE (mm) 5.58 vs 7.78 (InterHandGen) (-2.20)。
> - InterHand2.6M 上，PenVol (穿透体积) 0.11 vs 0.76 (InterHandGen) (-0.65)；PenDist (穿透距离) 0.01 vs 0.04 (InterHandGen) (-0.03)；ProxRatio (接近比例) 0.99 vs 0.97 (InterHandGen) (+0.02)。

## 概要

从单目图像中恢复交互双手的3D姿态与形状是计算机视觉中的一个核心难题，其瓶颈在于**遮挡导致的2D-3D对应模糊**以及**双手之间的物理穿透**。遮挡破坏了视觉线索的连续性，使得仅依赖图像特征的方法难以准确推断手部关节的深度与相对位置；而穿透问题则使重建结果违背物理常识，导致交互不协调与空间错位。

针对上述瓶颈，本文提出 **A2P（From 2D Alignment to 3D Plausibility）**，将双手重建解耦为两个互补的对齐阶段：**2D结构对齐**与**3D空间交互对齐**。核心洞察在于：通过在训练时统一关键点、分割和深度等异构2D先验知识，并将其蒸馏到一个轻量级的融合对齐编码器中，模型能够在不增加推理开销的前提下获得更强的结构感知能力；同时，引入一个双手免穿透扩散模型，以穿透姿态为条件学习到无碰撞姿态的生成映射，并结合碰撞梯度引导，在推理时迭代消除穿透，最终输出物理合理的双手姿态。

在方法定位上，A2P区别于现有工作的关键设计包括：
- **多模态先验的统一与蒸馏**：首次将视觉基础模型（如Sapiens）产生的关键点、分割、深度三种异构2D结构先验统一用于双手重建，并通过轻量融合对齐编码器（FAE）在训练时以MSE蒸馏，推理时移除重编码器，保持高效。
- **免穿透扩散精修**：提出双手免穿透扩散模型，仅在检测到双手穿透（IoU>0）时激活，以DDIM采样配合碰撞梯度引导，将穿透姿态映射为无碰撞姿态，显著优于InterHandGen等扩散正则化方法。

实验结果表明，A2P在InterHand2.6M 5fps基准上取得了领先性能：与最强基线4DHands相比，MPJPE从7.40mm降至5.36mm，MRRPE从24.58mm降至21.60mm；穿透指标大幅改善，PenVol从InterHandGen的0.76降至0.11。消融实验进一步验证了逐步融合多模态先验和引入扩散精修模块的有效性。

**局限性**：极端运动模糊会导致2D参考信息不可靠，影响重建质量。未来工作可探索时序融合以缓解该问题。



### 问题背景

从单目图像中恢复交互双手的3D姿态与形状，是计算机视觉中一个基础而困难的问题。与单手重建相比，双手交互场景引入了两个核心挑战：**严重遮挡**和**物理穿透**。当一只手被另一只手或物体遮挡时，2D图像中的可见信息急剧减少，导致2D-3D对应关系高度模糊，重建结果容易出现空间错位和姿态失真。同时，独立预测两只手往往会产生相互穿透的网格，破坏物理合理性，使得重建结果无法直接用于下游应用。

### 现有方法缺口

当前双手重建方法大致可分为两类。一类方法通过设计精巧的网络架构来建模双手交互，如**IntagHand**（Li et al., CVPR 2022）引入图注意力机制捕获手间关系，**ACR**（Yu et al., CVPR 2023）采用中心-部件注意力，**InterWild**（Moon, CVPR 2023）利用域对齐与几何特征，**4DHands**（Lin et al., arXiv 2024）则借助Transformer和时空交互。这些方法在可见区域表现良好，但在严重遮挡下仍缺乏足够的2D结构参考信息来纠正错位。

另一类方法尝试引入先验知识来约束重建空间。**Zuo et al.**（ICCV 2023）使用VAE学习交互先验，**InterHandGen**（Lee et al., CVPR 2024）利用扩散模型作为生成先验进行正则化。然而，这些先验通常是单一模态的（如仅使用关键点或仅使用3D姿态先验），未能充分挖掘视觉基础模型中蕴含的丰富2D结构信息。更关键的是，现有方法的物理穿透抑制能力有限——InterHandGen虽然引入了扩散先验，但其穿透体积（PenVol）仍高达0.76，表明生成先验本身不足以保证无碰撞的双手配置。

### 核心瓶颈与解决思路

上述分析揭示了一个根本瓶颈：**遮挡导致的2D-3D对应模糊与双手穿透构成了一对耦合难题**——缺乏可靠的2D结构参考使得遮挡下的姿态估计不可靠，而不可靠的姿态估计又加剧了穿透问题。

本文的核心洞察是：**将这一耦合问题解耦为两个互补的对齐阶段**——2D结构对齐和3D空间交互对齐，并为每个阶段设计专门的解决方案。具体而言：

1. **2D结构对齐阶段**：首次统一关键点、分割和深度等多种异构2D先验，通过视觉基础模型（Sapiens）提取这些先验知识，并在训练时将其蒸馏到一个轻量级的融合对齐编码器（Fusion Alignment Encoder, FAE）中。推理时仅保留轻量编码器，在不增加额外开销的前提下为遮挡区域提供丰富的2D结构参考。

2. **3D空间交互对齐阶段**：引入双手免穿透扩散模型，学习从穿透姿态到无碰撞物理合理姿态的生成映射。在去噪过程中进一步融入碰撞梯度引导，通过反向传播碰撞损失的负梯度来主动推开穿透顶点，实现更彻底的穿透消除。

这种“训练时蒸馏异构先验、推理时扩散去穿透”的两阶段设计，使得模型能够在无额外推理开销的条件下，同时实现遮挡鲁棒的精确对齐和物理合理的双手交互。



## 核心方法与创新机理

A2P 的核心创新在于将遮挡鲁棒的双手重建解耦为**2D结构对齐**与**3D空间交互对齐**两个互补阶段，并通过三个关键的 changed slots 实现性能跃升。

**1. 异构2D先验的统一融合与蒸馏（输入特征与训练辅助任务的联合改造）**

这是该方法最根本的差异化设计。传统双手重建方法仅依赖视觉主干提取的单一图像特征，而 A2P 首次将来自视觉基础模型（Sapiens）的**关键点、分割、深度**三种异构2D结构先验统一纳入重建流程。具体而言，方法引入一个轻量级**融合对齐编码器（Fusion Alignment Encoder, FAE）**，在训练阶段通过可学习投影层将三类先验特征融合为 $\mathbf{F}_p = Proj(\mathbf{F}_k, \mathbf{F}_s, \mathbf{F}_d)$，再经 Transformer 编码器与图像特征整合为集成特征 $\mathbf{F} = TransEnc(<\mathbf{F}_i, \mathbf{F}_p>)[0:l]$，供手部回归器预测 MANO 参数。

这一设计的精巧之处在于训练-推理的非对称性：FAE 通过 MSE 损失 $\mathcal{L}_{prior}(\mathbf{F}_p, \mathbf{F}_{fa})$ 蒸馏基础模型的先验知识，使得推理时**完全移除重型基础模型编码器**，仅保留轻量 FAE，从而在不增加推理开销的前提下获得多模态先验的增益。消融实验证实，逐步融合关键点、分割、深度先验均能持续改善 MPJPE/MPVPE——其中关键点与分割显著提升 XY 平面精度，深度先验则进一步改善 Z 轴和 MRRPE 指标。

**2. 免穿透扩散模型与碰撞梯度引导（后处理/精修阶段的改造）**

现有方法对双手穿透问题缺乏专门的处理机制，或仅依赖扩散正则化输出（如 **InterHandGen** (Lee et al., CVPR 2024)），穿透抑制能力有限。A2P 引入一个**双手免穿透扩散模型**，学习从穿透姿态到无碰撞姿态的生成映射。该模型以穿透双手 $\mathbf{X}_c$ 为条件，通过 DDIM 采样迭代去噪，其扩散损失为 $\mathcal{L}_{diffusion} = \| \mathbf{X}_0 - \mathcal{D}(\mathbf{X}_t, \mathbf{X}_c) \|_2$。

更关键的是，方法在去噪过程中嵌入了**碰撞梯度引导**：基于 GMoF 的鲁棒碰撞损失 $\mathcal{L}_{collision}$ 惩罚穿透顶点对，并通过负梯度更新 $\hat{\mathbf{X}_0} = \hat{\mathbf{X}_0} - \lambda (\delta_i \mathcal{L}_{collision})$ 主动将预测推向无碰撞配置。这一机制使 PenVol 从 InterHandGen 的 0.76 骤降至 **0.11**，PenDist 从 0.04 降至 **0.01**，ProxRatio 提升至 **0.99**，在物理合理性上实现了质的飞跃。

**3. 按需触发的扩散推理策略**

为平衡精度与效率，扩散模型仅在双手 IoU > 0（即存在穿透）时激活，避免了对大多数正常帧的冗余计算。这一条件触发机制使扩散精修的计算代价仅在必要时产生，配合 FAE 的推理轻量化设计，整体方法在参数量与推理时间上保持了实用竞争力。



A2P 将单目遮挡鲁棒的双手重建解耦为两个互补的对齐阶段：**2D 结构对齐**与**3D 空间交互对齐**。这一解耦设计的核心动机在于：遮挡导致 2D-3D 对应模糊，而双手穿透则造成交互不协调与空间错位。通过分别处理这两类问题，A2P 在训练时蒸馏异构 2D 先验知识，在推理时以扩散模型实现免穿透生成。

整体流程如 Figure 2 所示，包含以下关键模块：

![[assets/figures/papers/paper_list_l2254_https_arxiv_org_abs_2503_17788/figures/002_Figure_2.jpg]]
*Figure 2: The overall pipeline of our proposed method. “Feat.”, “Proj.”, “Enc.”, “FA”, “Key.”, “Seg.”, “Pen.” and “RelTrans” are abbreviations for “Feature”, “Projection”, “Encoder”, “Fusion Alignment”, “key points”, “Segmentation”, “Penetration” and “Relative Translation”, respectively. c denotes the condition of penetrated two hands. The purple arrow path will be activated during inference, while the yellow arrow path will be activated when the Intersection over Union (IoU) of both hands is greater than 0*

1. **图像编码器（Image Encoder）**：以 ResNet-50 为视觉主干，从单目 RGB 图像中提取图像特征 $\mathbf{F}_i$。

2. **融合对齐编码器（Fusion Alignment Encoder, FAE）**：在训练阶段，FAE 通过 MSE 损失蒸馏视觉基础模型（Sapiens）的多模态先验特征，生成融合先验特征 $\mathbf{F}_{fa}$。这些先验涵盖关键点、分割和深度三种异构 2D 结构信息，经可学习投影层融合为 $\mathbf{F}_p = Proj(\mathbf{F}_k, \mathbf{F}_s, \mathbf{F}_d)$。推理时 FAE 直接替代重型基础模型编码器，不增加额外推理开销。

3. **Transformer 编码器**：将图像特征 $\mathbf{F}_i$ 与融合先验特征 $\mathbf{F}_p$ 拼接后送入 Transformer，输出集成特征 $\mathbf{F} = TransEnc(\langle\mathbf{F}_i, \mathbf{F}_p\rangle)[0:l]$，取前 $l$ 通道用于下游回归。

4. **手部回归器（Hand Regressor）**：从集成特征 $\mathbf{F}$ 预测 MANO 参数、3D/2.5D 关节坐标及双手相对平移。训练阶段以总损失 $\mathcal{L}_{total} = \mathcal{L}_{hand} + \mathcal{L}_{prior}(\mathbf{F}_p, \mathbf{F}_{fa})$ 端到端优化，其中 $\mathcal{L}_{hand}$ 为 L1 回归损失，$\mathcal{L}_{prior}$ 为 FAE 的 MSE 蒸馏损失。

5. **双手免穿透扩散模型（Two-Hand Penetration-Free Diffusion Model）**：构成 Stage 2 的交互精修环节。推理时，仅当双手 IoU > 0（即存在穿透）时才激活该模块。扩散模型以穿透双手 $\mathbf{X}_c$ 为条件，通过 DDIM 采样逐步去噪，并在每一步去噪中引入碰撞梯度引导：以基于 GMoF 的鲁棒碰撞损失 $\mathcal{L}_{collision}$ 计算负梯度，按 $\hat{\mathbf{X}_0} = \hat{\mathbf{X}_0} - \lambda (\delta_i \mathcal{L}_{collision})$ 更新预测的干净双手参数，从而将穿透姿态映射为物理合理的无碰撞配置。

**数据流与触发逻辑**：训练时，黄色路径（FAE 蒸馏基础模型）始终激活；推理时，紫色路径（FAE 直接输出先验特征）替代基础模型。扩散模型仅在 IoU > 0 时触发，避免不必要的推理开销。这一条件触发策略将计算资源集中于真正需要去穿透的困难样本，在保证精度的同时兼顾效率。



A2P 的整体管线由五个核心模块串联构成，按功能可划分为两个阶段：**2D 结构对齐**（图像编码器、融合对齐编码器、Transformer 编码器、手部回归器）与 **3D 空间交互精修**（双手免穿透扩散模型）。以下逐一剖析各模块的设计逻辑与关键公式。

### 图像编码器（Image Encoder）

采用 **ResNet-50** 作为视觉主干，从单目 RGB 图像中提取图像特征 $\mathbf{F}_i$。该模块为后续所有模块提供基础的视觉表征，不引入额外结构修改。

### 融合对齐编码器（Fusion Alignment Encoder, FAE）

这是 A2P 在训练阶段的核心创新。其设计目标是：**将视觉基础模型（Sapiens）提取的异构 2D 先验知识蒸馏到一个轻量编码器中，使推理时无需运行重型基础模型即可获得等价的多模态先验特征**。

具体流程为：训练时，Sapiens 基础模型分别提取 2D 关键点特征 $\mathbf{F}_k$、分割特征 $\mathbf{F}_s$ 和深度特征 $\mathbf{F}_d$，三者通过可学习投影层融合为统一的先验特征：

$$\mathbf{F}_p = Proj(\mathbf{F}_k, \mathbf{F}_s, \mathbf{F}_d)$$

同时，轻量 FAE 直接从图像学习生成融合先验特征 $\mathbf{F}_{fa}$，并通过 MSE 损失 $\mathcal{L}_{prior}(\mathbf{F}_p, \mathbf{F}_{fa})$ 与基础模型的输出对齐。这一蒸馏机制使得推理时 FAE 可独立替代 Sapiens，参数量和推理时间大幅降低（详见 Table 4），而精度保持接近直接使用基础模型的效果。

### Transformer 编码器（Transformer Encoder）

将图像特征 $\mathbf{F}_i$ 与融合先验特征 $\mathbf{F}_p$ 拼接后送入 Transformer 编码器，取前 $l$ 通道作为集成特征：

$$\mathbf{F} = TransEnc(<\mathbf{F}_i, \mathbf{F}_p>)[0:l]$$

该模块的核心作用是**实现图像证据与 2D 结构先验的跨模态融合**，使下游回归器能同时利用外观信息和几何先验来消解遮挡带来的歧义。

### 手部回归器（Hand Regressor）

从集成特征 $\mathbf{F}$ 预测双手的 MANO 参数、3D/2.5D 关节坐标以及 3D 相对平移。训练时采用端到端优化，总损失为：

$$\mathcal{L}_{total} = \mathcal{L}_{hand} + \mathcal{L}_{prior}(\mathbf{F}_p, \mathbf{F}_{fa})$$

其中 $\mathcal{L}_{hand}$ 为预测值与真值之间在 MANO 参数、3D/2.5D 关节和相对平移上的 L1 距离。该模块完成 2D 结构对齐阶段的核心输出，但此时双手之间可能存在穿透。

### 双手免穿透扩散模型（Two-Hand Penetration-Free Diffusion Model）

这是 A2P 在 3D 空间交互精修阶段的核心创新。其因果机制为：**学习从穿透双手姿态到无碰撞双手姿态的生成映射，并在去噪过程中引入碰撞梯度引导以增强去穿透能力**。

扩散模型以穿透双手 $\mathbf{X}_c$ 为条件，对加噪后的干净双手 $\mathbf{X}_t$ 进行去噪，训练损失为 L2 距离：

$$\mathcal{L}_{diffusion} = \| \mathbf{X}_0 - \mathcal{D}(\mathbf{X}_t, \mathbf{X}_c) \|_2$$

推理时，采用 DDIM 采样逐步去噪。在每一步去噪后，对预测的干净双手 $\hat{\mathbf{X}}_0$ 施加碰撞梯度引导。碰撞损失采用基于 GMoF（Generalized Mean of Fractions）的鲁棒排斥项，惩罚穿透顶点对：

$$\mathcal{L}_{collision} = \sum_i \sum_j \left( \frac{\|\mathbf{V}_{t-1}^i - \mathbf{V}_c^j\|^2}{\|\mathbf{V}_{t-1}^i - \mathbf{V}_c^j\|^2 - \rho} \right)$$

随后通过反向传播碰撞损失的负梯度更新预测的干净双手参数：

$$\hat{\mathbf{X}_0} = \hat{\mathbf{X}_0} - \lambda (\delta_i \mathcal{L}_{collision})$$

该梯度引导机制使扩散模型在生成过程中显式感知并修正穿透，最终输出物理合理的无碰撞双手姿态。值得注意的是，扩散模型仅在双手 IoU > 0 时激活，避免了对大多数无穿透帧的冗余推理开销。

### 模块间的因果链

整个管线的因果链可概括为：**FAE 蒸馏异构 2D 先验 → Transformer 跨模态融合 → 回归器输出初步双手参数 → 扩散模型以碰撞梯度引导消除穿透**。消融实验（Table 3）证实了这一链条中每个环节的独立贡献：逐步融合关键点、分割、深度先验均能提升 MPJPE/MPVPE；加入扩散模型后，XY 与 Z 维度误差进一步下降，表明扩散精修有效消除了穿透带来的空间错位。



## 实验与关键发现

### 1. 主实验定量结果

A2P 在双手重建的核心基准上全面超越现有方法。在 **InterHand2.6M 5fps** 测试集上（Table 1），A2P 的 MRRPE 达到 **21.60 mm**，相较此前最优的 **4DHands**（Lin et al., arXiv 2024）的 24.58 mm 降低 2.98 mm（相对提升 12.1%）；MPJPE 从 4DHands 的 7.40 mm 降至 **5.36 mm**（降低 2.04 mm），MPVPE 从 **InterHandGen**（Lee et al., CVPR 2024）的 7.78 mm 降至 **5.58 mm**（降低 2.20 mm）。这表明 A2P 在双手整体姿态精度和顶点级重建精度上均取得显著增益。

![[assets/figures/papers/paper_list_l2254_https_arxiv_org_abs_2503_17788/figures/003_Table_1.jpg]]
*Table 1: Comparison with state-of-the-art methods on InterHand2.6M[16] 5fps test dataset. The results that are bolded and underlined represent the best result, while the bolded results represent the second-best result*

在 **HIC 数据集**上（Table 2），A2P 同样表现最优，MRRPE 为 **22.24 mm**，优于 4DHands 等基线，验证了方法在真实交互场景下的泛化能力。

![[assets/figures/papers/paper_list_l2254_https_arxiv_org_abs_2503_17788/figures/004_Table_2.jpg]]
*Table 2: Comparison with state-of-the-art methods on HIC dataset [25]*

穿透指标方面（Table 5），A2P 的 PenVol 仅为 **0.11**，而 InterHandGen 为 0.76，穿透体积降低约 85%；PenDist 从 0.04 降至 **0.01**，ProxRatio 从 0.97 提升至 **0.99**。这组数据直接证明了双手免穿透扩散模型在消除物理不合理穿透上的有效性。

![[assets/figures/papers/paper_list_l2254_https_arxiv_org_abs_2503_17788/figures/008_Table_5.jpg]]
*Table 5: Comparison on penetration metrics. We provide penetration metrics following [9]: PenVol, PenDist, and ProxRatio stand for penetration volume, penetration distance, and proximity ratio, respectively*

### 2. 消融实验

消融实验（Table 3）系统验证了各模块的因果贡献：

![[assets/figures/papers/paper_list_l2254_https_arxiv_org_abs_2503_17788/figures/006_Table_3.jpg]]
*Table 3: Ablation studies on InterHand2.6M [16]*

**异构先验的逐步融合**：仅使用图像特征（无先验）时性能最低；逐步加入关键点先验、分割先验后，MPJPE 和 MPVPE 在 XY 维度上持续改善，表明 2D 结构先验有效缓解了遮挡导致的定位模糊。进一步融合深度先验后，Z 轴误差和 MRRPE 显著下降，说明深度先验对恢复双手相对空间关系具有关键作用。三者联合使用达到第一阶段最优。

**扩散模型的增益**：在融合全部先验的基础上，加入双手免穿透扩散模型后，MRRPE、MPJPE 和 MPVPE 在 XY 与 Z 维度均进一步提升。这验证了扩散精修不仅消除穿透，还通过物理合理性约束反向修正了回归阶段的姿态误差。

**效率设计**（Table 4）：推理时移除基础模型编码器（仅保留轻量 FAE），参数量和推理时间大幅降低，而精度保持接近直接使用基础模型的效果。这证明 FAE 的 MSE 蒸馏策略在无额外推理开销的前提下成功保留了多模态先验知识。

### 3. 定性分析

Figure 1 展示了 A2P 在 InterHand2.6M、Re:InterHand 和 In-the-Wild 场景下的重建结果，双手姿态自然、交互协调，即使在严重遮挡下也未出现明显穿透或错位。Figure 4 对比了扩散精修前后的效果：精修前双手存在穿透区域，精修后穿透消除且姿态保持合理。与 InterHandGen 相比，A2P 的扩散模型在去穿透的同时更好地保留了手部姿态的准确性。

![[assets/figures/papers/paper_list_l2254_https_arxiv_org_abs_2503_17788/figures/009_Figure_4.jpg]]
*Figure 4: Qualitative two-hand recovery results compared with InterHandGen [9], Ours (before diffusion) and Ours (after diffusion) on InterHand2.6M [16]*

![[assets/figures/papers/paper_list_l2254_https_arxiv_org_abs_2503_17788/figures/001_Figure_1.jpg]]
*Figure 1: Two-hand recovery on InterHand2.6M (1st, 3rd columns), Re:InterHand (4th, 5th columns), and In-the-Wild (2nd, 6th columns)*

Figure 3 展示了网络来源真实场景的定性结果，A2P 在非受控环境下仍能恢复合理的双手姿态，但部分极端视角或运动模糊场景（红色圆圈标注）出现了估计失真或精度下降。

![[assets/figures/papers/paper_list_l2254_https_arxiv_org_abs_2503_17788/figures/005_Figure_3.jpg]]
*Figure 3: Qualitative two-hand recovery results in real scenes. The images are all sourced from the internet. The red circle indicates distortion or inaccurate estimation*

### 4. 失败模式与局限性

论文明确指出，**极端运动模糊**会导致 2D 参考信息不可靠，进而影响重建质量。从定性结果（Figure 3 红圈标注）可观察到，在快速运动或低质量输入下，A2P 可能出现手部姿态扭曲或空间定位偏差。此外，扩散模型的触发条件为 IoU > 0，这意味着仅在双手存在交集时才激活去穿透过程；对于未触发但存在轻微空间不协调的情况，模型可能无法进行精修。这一触发策略是否为最优尚待进一步研究。

### 5. 关键图表结论汇总

- **Table 1**：A2P 在 InterHand2.6M 5fps 上以 MRRPE 21.60 mm、MPJPE 5.36 mm、MPVPE 5.58 mm 全面领先现有方法。
- **Table 2**：在 HIC 数据集上 MRRPE 22.24 mm，验证跨数据集泛化能力。
- **Table 3**：异构先验逐步融合持续提升精度，扩散模型进一步优化空间交互。
- **Table 4**：FAE 蒸馏策略在保持精度的同时大幅降低推理开销。
- **Table 5**：PenVol 0.11 相较 InterHandGen 降低 85%，穿透抑制效果显著。
- **Figure 4**：扩散精修可有效消除穿透，且姿态保持优于 InterHandGen。

![[assets/figures/papers/paper_list_l2254_https_arxiv_org_abs_2503_17788/figures/007_Table_4.jpg]]
*Table 4: Comparison in model parameters and inference time. ⋆ represents with fusion alignment encoder & without two-hand diffusion. ⋆⋆ represents with fusion alignment encoder & two-hand diffusion. · denotes using foundation model encoder [8] without diffusion model for inference*



## 定位与知识库关联

**核心定位**：A2P 属于“单目遮挡鲁棒双手重建”这一细分方向，其技术路线可归纳为 **“训练时多模态先验蒸馏 + 推理时条件扩散精修”** 的双阶段范式。与现有工作相比，A2P 的关键差异在于将问题明确解耦为 2D 结构对齐和 3D 空间交互对齐两个互补阶段，并通过可学习投影层首次统一了关键点、分割和深度三种异构 2D 先验。

**与基线方法的关系**：

- **4DHands**（Lin et al., arXiv 2024）和 **ACR**（Yu et al., CVPR 2023）代表了当前双手重建的强基线，分别通过 Transformer 时空交互和中心-部件注意力机制提升重建精度。A2P 在 InterHand2.6M 5fps 上相较 4DHands 将 MRRPE 从 24.58mm 降至 21.60mm（-2.98mm），MPJPE 从约 7.40mm 降至 5.36mm（-2.04mm），表明多模态先验蒸馏带来的 2D 结构对齐能力显著超越了纯视觉特征方案。

- **InterHandGen**（Lee et al., CVPR 2024）将扩散模型引入双手生成，作为正则化先验约束重建输出。A2P 的双手免穿透扩散模型在动机上与之相近，但在机制上存在本质差异：InterHandGen 的扩散模型作用于重建管线的输出端进行全局正则化，而 A2P 仅在双手 IoU > 0 时激活扩散精修，并引入碰撞梯度引导（$\hat{\mathbf{X}_0} = \hat{\mathbf{X}_0} - \lambda (\delta_i \mathcal{L}_{collision})$）实现定向去穿透。这一设计使 A2P 在穿透指标上大幅优于 InterHandGen：PenVol 从 0.76 降至 0.11，PenDist 从 0.04 降至 0.01。

- **IntagHand**（Li et al., CVPR 2022）和 **Zuo et al.**（Zuo et al., ICCV 2023）分别通过图注意力交互和 VAE 交互先验建模双手关系。A2P 的扩散精修阶段可视为对这些显式交互建模方法的补充——在 2D 对齐阶段产生穿透时，通过生成式映射恢复物理合理性，而非依赖单一前馈网络同时解决对齐和交互问题。

**知识库贡献**：

1. **异构先验统一**：首次证明关键点、分割、深度三种 2D 结构先验在双手重建中具有互补性。消融实验（Table 3）显示，逐步融合关键点与分割显著改善 MPJPE/MPVPE 的 XY 维度，融合深度进一步改善 Z 轴和 MRRPE，验证了不同先验在空间维度上的分工特性。

2. **训练-推理解耦的蒸馏范式**：FAE 在训练时通过 MSE 蒸馏视觉基础模型（Sapiens）的多模态先验特征，推理时仅保留轻量编码器，使参数量和推理时间大幅降低（Table 4），精度接近直接使用基础模型的效果。这为“大模型知识注入小模型”在 3D 重建领域提供了可复用的范式。

3. **条件扩散与碰撞梯度引导**：将去穿透建模为从穿透姿态到无碰撞姿态的条件生成映射，并通过 GMoF 鲁棒碰撞损失（$\mathcal{L}_{collision} = \sum_i \sum_j \left( \frac{||\mathbf{V}_{t-1}^i - \mathbf{V}_c^j||^2}{||\mathbf{V}_{t-1}^i - \mathbf{V}_c^j||^2 - \rho} \right)$）的负梯度更新预测姿态，实现了物理约束与扩散先验的有机结合。

**适用边界与局限**：

- **极端运动模糊**：论文明确指出，极端运动模糊会导致 2D 参考信息不可靠，影响重建质量。这是所有依赖 2D 先验方法的共性瓶颈，A2P 的 FAE 蒸馏范式无法从根本上解决输入退化问题。
- **扩散触发条件**：当前以 IoU > 0 作为扩散精修的硬阈值触发条件，其最优性未经验证。是否存在边界情况（如 IoU 接近 0 但存在轻微穿透）需要手动核实。
- **数据集依赖**：主要实验在 InterHand2.6M 和 HIC 受控环境下进行，真实场景（Figure 3）的定性结果虽展示了一定泛化能力，但缺乏大规模 in-the-wild 定量评估。

**开放问题**：

1. 如何处理极端运动模糊？时序融合是否能缓解该问题？
2. 扩散模型的触发条件（IoU > 0）是否为最优？能否端到端学习触发策略？
3. 异构先验的融合权重是否可自适应学习，而非固定投影？不同场景下先验的可靠性可能存在差异。



## 原文 PDF

![[paperPDFs/CVPR_2026/From_2D_Alignment_to_3D_Plausibility_Unifying_Heterogeneous_2D_Priors_and_Penetration_Free_Diffusion_for_Occlusion_Robust_Two_Hand_Reconstruction.pdf]]
