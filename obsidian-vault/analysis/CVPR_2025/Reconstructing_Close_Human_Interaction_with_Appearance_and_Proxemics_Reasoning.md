---
title: Reconstructing Close Human Interaction with Appearance and Proxemics Reasoning
type: paper
paper_level: A
venue: CVPR
year: 2025
pdf_ref: paperPDFs/CVPR_2025/Reconstructing_Close_Human_Interaction_with_Appearance_and_Proxemics_Reasoning.pdf
project_link: null
code_link: null
aliases:
- CDBOF
- RCHIAPR
tags:
- CVPR_2025
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
core_operator: 利用RGB图像直接线索，通过重建人体外观（3D高斯泼溅）推断深度顺序关系，并结合学习到的空间行为先验（扩散模型）和物理约束进行优化。
primary_logic: 通过同时重建人体运动和外观，并将外观一致性、空间行为先验和物理合理性融入统一的优化框架，可以有效解决视觉模糊和严重遮挡问题，恢复野外视频中可信的近距离交互。
claims:
- 人类外观是防止错误深度排序和缓解视觉模糊的有效线索。
- 外观约束对于正确的深度顺序关系至关重要。
- 通过同时重建人体运动和外观，并将外观一致性、空间行为先验和物理合理性融入统一的优化框架，可以有效解决视觉模糊和严重遮挡问题，恢复野外视频中可信的近距离交互。
---

# Reconstructing Close Human Interaction with Appearance and Proxemics Reasoning

> [!tip] 核心洞察
> 通过同时重建人体运动和外观，并将外观一致性、空间行为先验和物理合理性融入统一的优化框架，可以有效解决视觉模糊和严重遮挡问题，恢复野外视频中可信的近距离交互。

| 字段 | 内容 |
|------|------|
| 中文题名 | 通过外观和人际空间推理重建近距离人类交互 |
| 英文题名 | Reconstructing Close Human Interaction with Appearance and Proxemics Reasoning |
| 会议/期刊 | CVPR 2025 |
| Links |  [paper](https://arxiv.org/abs/2507.02565)|
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction |
| Method | CloseApp (Dual-branch Optimization Framework) |
| Dataset |  |

> [!tip] 效果简介
> 本笔记的既有实验指标、对比结果与适用边界见“实验与关键发现”；本轮仅统一结构，不改写证据。

## 概要

从单目野外视频中重建近距离人类交互面临一个核心瓶颈：**视觉模糊与人与人之间的严重遮挡**。当两人身体紧密接触时，即使是当前最先进的视觉基础模型（如 SAM、ViTPose++）也难以准确区分各自的人体语义，导致深度排序混乱和姿态估计失败（Figure 1）。

本文提出 **CloseApp**，一个**双分支优化框架**，通过同时利用**人体外观、空间行为先验和物理约束**来解决上述问题。其核心洞察在于：人体外观本身是一种有效且被以往方法忽视的深度线索——即使仅使用粗糙纹理，渲染图像与原始图像的差异也能可靠地推断遮挡关系（Figure 2）。

方法层面，CloseApp 做出了四项关键改变：
- **优化目标**：从仅依赖 2D 关键点重投影，扩展为联合外观渲染损失、重投影损失、物理穿透损失及运动正则化。
- **运动先验**：引入基于扩散模型学习的空间行为先验，能从噪声和部分观测中生成合理的交互姿态。
- **外观约束**：通过可优化 UV 高斯图与 3D 高斯泼溅技术对人体外观建模，利用渲染差异反向驱动姿态优化。
- **物理约束**：采用基于可微分距离场的精确穿透惩罚，替代以往粗略的碰撞避免。

实验结果表明，外观约束对深度顺序关系的正确恢复至关重要：移除该约束后，MPJPE 从 59.06 上升至 60.68；进一步移除空间先验后，误差增至 61.52。物理约束的移除虽使 MPJPE 略微改善至 57.01，但平均穿透距离从 0.81 显著恶化至 1.30。

**方法定位**：CloseApp 属于基于优化的交互重建范式，与 **BUDDI**（Muller et al., CVPR 2024）和 **CloseInt**（Huang et al., CVPR 2024）等同期工作相比，其核心差异在于将外观一致性与学习到的空间行为先验统一纳入优化循环。当前框架仅支持双人交互，且要求输入视频中存在部分无接触帧以可靠约束外观分支；优化耗时约 3–5 分钟（128 帧），尚不适用于实时场景。

### 近距离交互重建的核心瓶颈

从单目视频中重建多人三维姿态与运动是计算机视觉的核心任务之一，但在**近距离交互**场景下，现有方法面临根本性困难。当两人身体紧密接触时，肢体相互遮挡导致图像中出现严重的**视觉模糊**：同一像素区域可能同时对应多个人的身体部位，使得基于外观的语义分割和关键点检测无法可靠地区分个体归属。即使是最先进的视觉基础模型，如 **ViTPose++** 和时序 **SAM**，在近距离交互案例中也难以清晰分辨人体语义（Figure 1）。这种底层语义的混淆直接导致上层姿态估计方法失效——深度排序错误、肢体互换、穿透等问题频繁出现。

从因果机制来看，核心瓶颈在于：**现有方法缺乏有效的线索来打破由视觉模糊和人与人遮挡造成的深度歧义**。仅依赖2D关键点或分割掩码的优化框架，在遮挡区域缺乏足够的约束来推断正确的三维空间关系。

### 现有方法的缺口

当前主流的交互重建方法大致分为两类：

- **基于优化的方法**（如 **BUDDI**，Müller et al., CVPR 2024）：通过拟合检测到的2D关键点并施加空间先验来优化人体模型参数。这类方法在严重遮挡时，关键点检测本身已不可靠，优化缺乏正确的目标引导。
- **基于回归的方法**（如 **CloseInt**，Huang et al., CVPR 2024）：直接从图像回归运动参数，结合邻近空间和物理适应。尽管速度更快，但回归模型在训练数据覆盖不足的复杂交互模式下泛化能力有限。

两类方法的共同缺口在于：**均未利用RGB图像中蕴含的人体外观线索来主动推理深度顺序关系**。此外，现有方法的物理约束通常较为粗糙（如简单的碰撞避免），缺乏精确的可微分穿透惩罚；运动先验也多为通用的人体姿态正则化，未针对交互行为中的空间关系（proxemics）进行专门建模。

### 本文动机与核心思路

本文的核心洞察是：**人体外观可以成为缓解视觉模糊和人与人遮挡的有效线索**。即使使用粗糙的纹理重建，渲染图像与原始RGB之间的外观差异也能为深度排序提供强约束——正确的深度顺序应产生与观测一致的渲染结果，而错误的顺序则会导致明显的渲染偏差（Figure 2）。

基于此，本文提出 **CloseApp**，一个**双分支优化框架**，将以下三种互补的约束统一纳入优化：

1. **外观约束**：通过3D高斯泼溅重建人体外观，利用渲染损失直接指导姿态优化，从像素级一致性推断深度顺序关系。
2. **空间行为先验**：使用扩散模型学习交互中的邻近空间行为，从噪声和部分观测中生成合理的交互姿态，作为优化的初始估计和正则化。
3. **物理约束**：基于可微分距离场精确惩罚身体穿透，确保重建结果的物理合理性。

该方法的关键优势在于：外观、空间先验和物理约束三者协同作用，在优化过程中相互校正——外观约束解决深度歧义，空间先验提供行为合理性，物理约束保证接触真实性，从而在野外视频中恢复可信的近距离交互。

## 核心方法与创新机理

本文提出 **CloseApp**，一个基于外观、人际空间和物理约束的双分支优化框架，以解决现有方法在近距离交互重建中的根本瓶颈：**视觉模糊与人与人之间的严重遮挡**导致基础视觉模型（如 SAM、ViTPose++）无法可靠区分人体语义，进而使深度排序和姿态估计失败。其核心创新体现在以下四个维度的“changed slots”上。

### 1. 优化目标：从单一重投影到多模态联合约束

现有优化类方法（如 **BUDDI**, Müller et al., CVPR 2024）主要依赖检测到的 2D 关键点或分割掩码的重投影损失来驱动姿态拟合，在严重遮挡下极易陷入局部最优。CloseApp 将优化目标扩展为五项联合损失（Eq. 10）：

$$
\operatorname*{argmin}_{\pi_m,\pi_a}\mathcal{L} = \mathcal{L}_{\mathrm{app}} + \mathcal{L}_{\mathrm{reproj}} + \mathcal{L}_{\mathrm{pen}} + \mathcal{L}_{\mathrm{smooth}} + \mathcal{L}_{\mathrm{reg}}
$$

这一设计的关键在于引入**外观渲染损失**（Eq. 6）和**物理穿透损失**（Eq. 7），使优化过程同时受 RGB 像素级外观一致性、3D 关键点投影、物理合理性及时间平滑性的联合驱动，从根本上突破了仅依赖稀疏关键点监督的局限。

### 2. 运动先验：从简单正则化到学习型空间行为先验

基线方法通常仅使用简单的姿态先验（如高斯混合模型）或粗略的正则化项，缺乏对交互行为本身的结构化建模。CloseApp 提出基于**扩散模型的邻近空间先验**（Proxemics Prior, Section 3.2），在大量交互运动数据上学习条件去噪过程：

$$
q(\mathbf{x}_{t-1} \mid \mathbf{x}_t, c) = \mathcal{N}(\mathbf{x}_{t-1}; \mu_\alpha(\mathbf{x}_t, c), \tilde{\gamma}_t \mathrm{I})
$$

该先验以 RGB 图像和 2D 关键点为条件，能够从纯噪声或部分观测中生成包含合理空间关系和身体接触的交互运动，为后续优化提供强先验初始化和正则化锚点。消融实验表明，仅使用扩散模型初始预测而不进行优化的 MPJPE 高达 65.23，大幅落后于全模型，验证了“先验+优化”的协同必要性。

### 3. 外观约束：从无到可优化的 3D 高斯外观建模

这是 CloseApp 最具区分度的创新——首次将**人体外观重建**引入交互姿态优化回路。通过可优化的 UV 高斯图与 3D 高斯泼溅技术，框架能够同时估计人体粗糙纹理并渲染至图像平面，利用渲染图像与原始 RGB 之间的差异（L1 + SSIM + LPIPS）反向驱动姿态修正。消融实验证实，移除外观约束后 MPJPE 从 59.06 增至 60.68，且深度顺序关系显著恶化（Fig. 5），直接证明了“外观是防止错误深度排序的有效线索”这一核心洞察。

### 4. 物理约束：从粗略碰撞避免到可微分穿透惩罚

相较于以往方法仅使用简单的碰撞检测或忽略穿透问题，CloseApp 采用基于**可微分符号距离场**的精确穿透损失（Eq. 7），对交互双方三角面片之间的相互穿透进行逐面片惩罚。消融显示，移除物理约束后 MPJPE 虽略微改善至 57.01，但平均穿透距离（A-PD）从 0.81 恶化至 1.30，表明物理约束的核心价值在于保证重建结果的物理合理性而非单纯的关节精度。

### 创新总结

CloseApp 的方法论创新并非孤立组件的堆砌，而是通过**外观-空间-物理**三者的因果联动实现突破：外观约束解决视觉模糊和深度歧义，空间先验提供行为合理性边界，物理约束保证接触可信度，三者共同构成一个自洽的优化闭环。这一设计使得框架能够在野外单目视频中恢复出具有正确深度顺序和自然接触的可信交互运动。

CloseApp 提出一个**双分支优化框架**（Dual-branch Optimization Framework），从单目野外视频中重建近距离双人交互。其核心设计思路是：将人体外观、空间行为先验与物理合理性统一纳入优化目标，以解决因视觉模糊和严重遮挡导致的深度排序与姿态估计失败问题。

### 框架总览

整体流程如 Figure 3 所示，包含两个并行分支——**运动分支**（Motion Branch）与**外观分支**（Appearance Branch）——它们共享约束信号并联合优化。

![[assets/figures/papers/paper_list_l1746_Reconstructing_Close_Human_Interaction_with_Appearance_and_Proxemics_Rea/figures/003_Figure_3.jpg]]
*Figure 3: Overview of our framework. We propose a dual-branch optimization framework to reconstruct close human interactions from a monocular in-the-wild video. By optimizing the proxemics prior, U-Net backbone, and two optimizable tensors, the framework simultaneously predicts interactive motions and coarse appearances. With the constraints from 2D observations, physics, and prior knowledge, the framework can finally output 3D interactions with plausible body poses, natural proxemic relationships and accurate physical contacts*

**运动分支** 负责预测双人的 3D 运动序列。它以预训练的邻近空间扩散模型（Proxemics Prior）为基础，该扩散模型学习从 RGB 图像和 2D 关键点生成合理的交互姿态与空间关系。在优化阶段，运动分支通过微调扩散模型的网络参数 $ \pi_m $，直接输出 SMPL 参数序列（姿态 $ \theta $、体型 $ \beta $、平移 $ \tau $）。

**外观分支** 负责重建人体外观，为深度排序提供关键线索。它由 U-Net 骨干和两个可优化隐式张量组成，解码出 UV 高斯属性图；随后通过 UV 坐标映射将 2D 高斯提升到 3D 空间，再利用 3D 高斯泼溅（3D Gaussian Splatting）将人体渲染到图像平面。

### 输入输出流

框架的输入为单目 RGB 视频序列及其检测到的 2D 关键点。扩散先验首先从这些观测中生成初始运动估计，作为优化的起点。运动分支输出 SMPL 参数，驱动人体网格变形；外观分支输出 UV 高斯图，经高斯泼溅渲染器生成可微渲染图像。

优化过程由五项损失联合驱动（Eq. 10）：

$$
\operatorname*{argmin}_{\pi_m,\pi_a}\mathcal{L} = \mathcal{L}_{\mathrm{app}} + \mathcal{L}_{\mathrm{reproj}} + \mathcal{L}_{\mathrm{pen}} + \mathcal{L}_{\mathrm{smooth}} + \mathcal{L}_{\mathrm{reg}}
$$

其中：
- **$ \mathcal{L}_{\mathrm{app}} $**（外观损失）：渲染图像与原始 RGB 之间的 L1、SSIM 和 LPIPS 差异，用于推断深度顺序关系；
- **$ \mathcal{L}_{\mathrm{reproj}} $**（重投影损失）：3D 关节透视投影与 2D 关键点之间的 L2 误差；
- **$ \mathcal{L}_{\mathrm{pen}} $**（穿透损失）：基于可微分距离场惩罚两角色三角面片之间的相互穿透；
- **$ \mathcal{L}_{\mathrm{smooth}} $**（平滑损失）：相邻帧间 3D 关节位置的时间一致性；
- **$ \mathcal{L}_{\mathrm{reg}} $**（正则化损失）：约束运动参数和外观高斯参数保持在扩散先验初始预测附近，防止优化发散。

### 关键机制：外观驱动的深度推理

Figure 2 揭示了外观分支如何解决深度歧义。UV 高斯图映射到 3D 空间后，渲染图像与原始 RGB 的差异直接反映深度排序和图像-模型对齐的质量。由于高斯泼溅在不同帧间应保持外观一致性（尤其在无遮挡帧），优化过程会调整姿态参数以寻找最优解，从而在交互帧中恢复正确的深度排序。这一机制是 CloseApp 区别于仅依赖 2D 关键点方法的根本创新。

### 优化特性

双分支优化在约 3-5 分钟内完成 128 帧的处理，不适用于实时应用。框架假设输入视频中存在至少部分无接触或接触较少的帧，以便可靠地约束外观分支；若全程紧密接触，外观约束的有效性将下降。当前设计仅支持双人交互，尚未扩展至三人及以上场景。

### 3.1 运动表征与问题形式化

给定一段包含两人交互的野外单目视频，目标是从 $N$ 帧序列中同时恢复两人的3D运动与外观。对于个体 $a$ 和 $b$，重建的运动序列定义为：

$$\mathbf{x}^{1:N} = \{\mathbf{x}^{a,1:N}, \mathbf{x}^{b,1:N}\}$$

其中每帧的个体运动 $\mathbf{x}^{a,i} = \{\theta^i, \beta^i, \tau^i\}$ 包含SMPL模型的姿态参数 $\theta$、体型参数 $\beta$ 和平移参数 $\tau$。该表征构成了后续扩散先验和双分支优化的核心变量空间。

### 3.2 邻近空间先验：扩散模型

#### 动机与训练

现有方法缺乏对交互行为的显式先验建模，导致在视觉模糊区域产生不合理的姿态与空间关系。为此，方法首先训练一个扩散模型以学习人体姿态和邻近空间行为的先验知识。该模型以真实交互运动数据 $\hat{\mathbf{x}}_0$ 为目标，通过前向扩散过程将其逐步噪声化：

$$q(\mathbf{x}_t \mid \hat{\mathbf{x}}_0) = \sqrt{\hat{\alpha}_t} \hat{\mathbf{x}}_0 + \sqrt{1 - \hat{\alpha}_t} \epsilon, \quad \epsilon \sim \mathcal{N}(0, \mathrm{I}) \tag{1}$$

反向去噪过程则从高斯噪声出发，在条件信号 $c$（从RGB图像和2D关键点提取的特征）的引导下逐步恢复运动序列：

$$q(\mathbf{x}_{t-1} \mid \mathbf{x}_t, c) = \mathcal{N}(\mathbf{x}_{t-1}; \mu_\alpha(\mathbf{x}_t, c), \tilde{\gamma}_t \mathrm{I}) \tag{2}$$

#### 训练损失

扩散模型的训练损失由五项联合构成，确保预测的运动序列在多个维度上与真实值一致：

$$\mathcal{L} = \mathcal{L}_{\mathrm{reproj}} + \mathcal{L}_{\mathrm{smpl}} + \mathcal{L}_{\mathrm{joint}} + \mathcal{L}_{\mathrm{vel}} + \mathcal{L}_{\mathrm{int}} \tag{3}$$

- **重投影损失** $\mathcal{L}_{\mathrm{reproj}}$：将预测的3D关节通过透视相机投影到图像平面，与检测到的2D关键点计算L2差异：

$$\mathcal{L}_{\mathrm{reproj}} = \| \Pi(J_{3D} + \tau) - \hat{J}_{2D} \|_2^2 \tag{4}$$

- **SMPL损失** $\mathcal{L}_{\mathrm{smpl}}$：约束预测的SMPL参数与真实值一致。
- **关节损失** $\mathcal{L}_{\mathrm{joint}}$：直接约束3D关节位置的准确性。
- **速度损失** $\mathcal{L}_{\mathrm{vel}}$：保证运动的时间连续性。
- **交互损失** $\mathcal{L}_{\mathrm{int}}$：惩罚两人之间相对距离的偏差，确保空间关系合理：

$$\mathcal{L}_{\mathrm{int}} = \| |J_{3D}^a - J_{3D}^b| - |\hat{J}_{3D}^a - \hat{J}_{3D}^b| \|_2^2 \tag{5}$$

训练完成后，该扩散模型可从RGB图像和2D关键点预测初步的交互运动，作为后续双分支优化的初始估计和正则化锚点。

### 3.3 双分支优化框架

扩散模型的初始预测在严重遮挡和视觉模糊区域仍存在较大误差。为此，方法设计了一个双分支优化框架，同时优化运动分支和外观分支，利用外观一致性、物理约束和先验正则化联合精炼结果。

#### 外观分支与渲染损失

外观分支通过一个U-Net骨干网络和两个可优化隐式编码张量，为每个人体预测UV高斯属性图。这些3D高斯通过UV坐标映射到人体表面，再经由高斯泼溅渲染器投影到图像平面，生成可微渲染图像。渲染图像与原始RGB图像之间的差异构成外观损失：

$$\mathcal{L}_{\mathrm{app}} = \mathcal{L}_{\mathrm{rgb}} + \mathcal{L}_{\mathrm{ssim}} + \mathcal{L}_{\mathrm{lpips}} \tag{6}$$

该损失同时包含像素级L1损失、结构相似性损失（SSIM）和感知损失（LPIPS），从多粒度衡量渲染质量。外观损失的核心作用在于：通过比较渲染与真实图像的差异，推断两人的深度顺序关系——错误的深度排序会导致渲染图像与原始图像在遮挡边界处产生显著不一致，从而驱动姿态优化向正确方向收敛。

#### 物理穿透损失

为防止重建结果中出现人体相互穿透的物理不合理现象，方法引入基于可微分距离场的穿透惩罚。对于两个个体的三角面片集合 $\mathcal{C}$ 中的每一对面片 $(f_a, f_b)$，计算面片顶点在对方距离场中的穿透程度：

$$\mathcal{L}_{\mathrm{pen}} = \sum_{(f_a, f_b) \in \mathcal{C}} \left\{ \sum_{v_a \in f_a} \| -\Psi_{f_b}(v_a) n_a \|_2^2 + \sum_{v_b \in f_b} \| -\Psi_{f_a}(v_b) n_b \|_2^2 \right\} \tag{7}$$

其中 $\Psi_{f}(\cdot)$ 为面片 $f$ 的可微分距离场，$n$ 为法向量。该损失仅在顶点位于对方体内时产生非零惩罚，精确约束物理接触的合理性。

#### 运动正则化

为保证优化的稳定性和时序一致性，方法施加两项正则化：

- **平滑损失** $\mathcal{L}_{\mathrm{smooth}}$：约束相邻帧之间3D关节位置的变化幅度：

$$\mathcal{L}_{\mathrm{smooth}} = \sum_{i=1}^{N-1} \| J_{3D}^{i+1} - J_{3D}^i \|_2^2 \tag{8}$$

- **先验正则化损失** $\mathcal{L}_{\mathrm{reg}}$：将运动参数（姿态 $\theta$、平移 $\tau$、体型 $\beta$）和外观高斯参数约束在扩散先验的初始预测附近，防止优化偏离合理空间：

$$\mathcal{L}_{\mathrm{reg}} = \| \theta - \theta' \|_2^2 + \| \tau - \tau' \|_2^2 + \| \beta - \beta' \|_2^2 + \mathcal{L}_{\mathrm{offset}} + \mathcal{L}_{\mathrm{scale}} \tag{9}$$

其中 $\theta'$, $\tau'$, $\beta'$ 为扩散模型的初始预测值，$\mathcal{L}_{\mathrm{offset}}$ 和 $\mathcal{L}_{\mathrm{scale}}$ 约束外观高斯的位置偏移和尺度变化。

#### 总优化目标

最终，双分支优化框架联合优化运动分支参数 $\pi_m$ 和外观分支参数 $\pi_a$（包含U-Net网络权重和可优化张量），最小化以下总损失：

$$\operatorname*{argmin}_{\pi_m,\pi_a} \mathcal{L} = \mathcal{L}_{\mathrm{app}} + \mathcal{L}_{\mathrm{reproj}} + \mathcal{L}_{\mathrm{pen}} + \mathcal{L}_{\mathrm{smooth}} + \mathcal{L}_{\mathrm{reg}} \tag{10}$$

该目标函数的五项约束形成互补机制：外观损失提供深度排序线索，重投影损失锚定2D观测，穿透损失保证物理合理性，平滑损失和正则化损失维护时序一致性与先验可信度。消融实验（Table 3）证实，移除任一组件均会导致性能下降——外观约束的移除使MPJPE从59.06增至60.68，邻近空间先验的移除进一步增至61.52，而物理约束的移除虽使MPJPE略微改善至57.01，但平均穿透距离从0.81恶化至1.30，验证了各模块的必要性。

![[assets/figures/papers/paper_list_l1746_Reconstructing_Close_Human_Interaction_with_Appearance_and_Proxemics_Rea/figures/002_Figure_2.jpg]]
*Figure 2: With predicted UV Gaussian maps, we can map the Gaussians to 3D space with a UV coordinate map and splat them to the image plane. We can then reason the depth ordinal relationship and image-model alignment with the rendered and original images. Since the Gaussians should also be consistent across non-occluded frames, the optimization adjusts poses to find an optimal solution in interactive frames, thereby producing accurate depth ordering and poses*

## 实验与关键发现

### 核心瓶颈与实验设计逻辑

现有方法在近距离人类交互场景中面临的根本瓶颈是**视觉模糊与互遮挡**：即使是最先进的视觉基础模型（如 ViTPose++、temporal SAM）也无法可靠地区分交互个体的语义归属，导致深度排序混乱和姿态估计失败（Figure 1）。本方法的核心假设是：**人类外观线索可以有效防止错误的深度排序，缓解视觉模糊**（Section 5.4）。实验设计围绕这一假设展开，通过定量对比、消融实验和定性分析，系统验证外观约束、空间行为先验和物理约束三者协同优化的必要性。

![[assets/figures/papers/paper_list_l1746_Reconstructing_Close_Human_Interaction_with_Appearance_and_Proxemics_Rea/figures/001_Figure_1.jpg]]
*Figure 1: Due to the visual ambiguity, even state-of-the-art vision foundation models (e.g., ViTPose++ [63] and temporal SAM [25, 37]) cannot clearly distinguish human semantics in close interactive cases. Consequently, human pose estimation methods based these basic human semantics tend to fail. In comparison, our dual-branch optimization framework that leverages human appearance, proxemics, and physics is capable of alleviating visual ambiguity to give better results*

---

### 主实验结果

#### 定量对比

在 Hi4D 和 3DPW 两个基准数据集上，本方法（CloseApp）与多个代表性方法进行了对比，包括基于优化的 **BUDDI**（Muller et al., CVPR 2024）、基于回归的 **CloseInt**（Huang et al., CVPR 2024）、单人多帧方法 **Human4D**（Goel et al., ICCV 2023）、单帧方法 **CLIFF**（Li et al., ECCV 2022）以及物理感知方法 **MultiPhys**（Ugrinovic et al., CVPR 2024）。主要评价指标为 MPJPE（Mean Per-Joint Position Error）和 PA-MPJPE（Procrustes-Aligned MPJPE）。

**Table 2** 展示了定量对比结果（Figure 4 合并呈现）：
- 在 Hi4D 数据集上，本方法取得了 **MPJPE 59.1 mm** 和 **PA-MPJPE 44.3 mm** 的最优性能。
- 在 3DPW 数据集上，本方法取得了 **MPJPE 64.5 mm** 和 **PA-MPJPE 45.6 mm** 的最优性能。
- 本方法在室内（Hi4D）和室外（3DPW）场景下均达到 state-of-the-art 水平，验证了框架的泛化能力。

#### 定性对比

**Figure 4** 提供了与 BUDDI 和 CloseInt 的定性可视化对比。在视觉模糊严重的帧中，BUDDI 和 CloseInt 容易出现肢体错位、深度顺序错误或穿透问题，而本方法通过联合优化外观和空间先验，能够恢复更可信的交互姿态和深度关系。

---

### 消融实验

消融实验（**Table 3** 和 **Figure 5**）系统拆解了各组件对性能的贡献，核心发现如下：

![[assets/figures/papers/paper_list_l1746_Reconstructing_Close_Human_Interaction_with_Appearance_and_Proxemics_Rea/figures/008_Figure_5.jpg]]
*Figure 5: Ablation study. The initial prediction is severely affected by visual ambiguity and cannot reconstruct accurate interaction. With the proposed optimization, the body pose can be improved with the additional constraints. In addition, we find that appearance constraint is important for the depth ordinal relationships*

| 配置 | MPJPE ↓ | A-PD ↓ | 关键结论 |
|------|---------|--------|----------|
| 全模型（Ours） | **59.06** | **0.81** | 所有组件协同工作，取得最优综合性能 |
| 仅初始预测（无优化） | 65.23 | — | 扩散先验单独预测严重受视觉模糊影响，性能大幅落后 |
| 移除外观约束 | 60.68 | — | 深度顺序关系变差，验证外观线索对深度排序的关键作用 |
| 移除邻近空间先验 | 61.52 | — | 性能进一步恶化，说明空间行为先验对姿态合理性至关重要 |
| 移除物理约束（穿透损失） | 57.01 | 1.30 | MPJPE 略微改善，但平均穿透距离显著增加，说明物理约束以微小姿态精度代价换取了物理合理性 |

**逐项分析：**

1. **初始预测 vs. 全模型**：仅使用预训练扩散模型直接预测（不经过优化），MPJPE 高达 65.23 mm，比全模型差约 6.2 mm。这证明双分支优化框架对于纠正视觉模糊引起的初始误差是必不可少的。

2. **外观约束的关键性**：移除外观约束后，MPJPE 从 59.06 增加到 60.68。**Figure 5** 的可视化进一步证实，外观约束对于恢复正确的深度顺序关系至关重要——即使外观分支仅提供粗糙纹理，渲染差异仍能有效指导姿态优化（Section 5.4）。

3. **空间行为先验的作用**：移除邻近空间先验后，MPJPE 进一步增加到 61.52。这表明学习到的空间行为先验（扩散模型）为优化提供了合理的初始化和正则化，防止姿态偏离自然交互模式。

4. **物理约束的权衡**：移除穿透损失后，MPJPE 略微改善至 57.01，但平均穿透距离（A-PD）从 0.81 增加至 1.30。这揭示了物理合理性与姿态精度之间的经典权衡：物理约束强制避免穿透，可能在某些帧中略微牺牲关键点拟合精度，但大幅提升了交互的物理可信度。

---

### 失败模式与局限性

根据实验观察和方法设计假设，本方法存在以下已知失败模式：

1. **全程紧密接触场景**：方法假设输入视频中存在部分无接触或接触较少的帧，以可靠地约束外观分支。若视频全程紧密接触，外观约束的有效性将下降（Section 3.3 设计假设）。

2. **剧烈光照变化与严重遮挡**：在光照变化剧烈或部分严重遮挡的情况下，无法重建高质量完整人体纹理，外观分支仅能提供粗糙的外观约束（limitations）。但实验表明，即使粗纹理仍能提供有效的深度线索（Section 5.4）。

3. **多人场景未覆盖**：当前框架仅针对双人交互设计，未涉及三人及以上场景，公平性比较局限于二人基准。

4. **计算效率**：优化过程约需 3-5 分钟（128 帧），不适用于实时在线应用，但不影响离线重建的定性结果。

---

### 关键图表结论

- **Figure 1**：动机展示——视觉基础模型在近距离交互中无法区分人体语义，本方法通过外观、空间和物理约束缓解了这一问题。
- **Figure 4 / Table 2**：定量与定性对比——本方法在 Hi4D 和 3DPW 上均超越现有方法，对视觉模糊更鲁棒。
- **Figure 5 / Table 3**：消融研究——外观约束对深度顺序关系至关重要，空间先验和物理约束分别提升姿态合理性和物理可信度。

![[assets/figures/papers/paper_list_l1746_Reconstructing_Close_Human_Interaction_with_Appearance_and_Proxemics_Rea/figures/006_Figure_4.jpg]]
*Figure 4: Qualitative comparison with BUDDI [40] and CloseInt [16]. Our method is more robust to visual ambiguity*

![[assets/figures/papers/paper_list_l1746_Reconstructing_Close_Human_Interaction_with_Appearance_and_Proxemics_Rea/figures/004_Table_1.jpg]]
*Table 1: Comparisons of existing human-human interaction datasets*

## 定位与知识库关联

### 1. 问题定位：视觉模糊与深度歧义

本工作聚焦单目野外视频中**近距离双人交互**的3D运动与外观联合重建。核心瓶颈在于：当两人肢体紧密接触或相互遮挡时，RGB图像中的人体语义边界高度模糊，即使是最先进的视觉基础模型（如ViTPose++、时序SAM）也无法可靠地区分个体语义，导致下游姿态估计与深度排序失败（Figure 1）。现有方法通常依赖2D关键点/分割的重投影损失进行优化，在视觉歧义严重的帧中缺乏有效约束来纠正错误的深度顺序关系。

### 2. 方法谱系

**CloseApp**（本文提出的双分支优化框架）位于“基于优化的交互重建”谱系中，与以下代表性工作形成对比与继承关系：

| 方法 | 范式 | 核心约束 | 关键差异 |
|------|------|----------|----------|
| **BUDDI** (Müller et al., CVPR 2024) | 优化 | 空间先验拟合2D关键点 | 无外观约束与物理穿透惩罚，深度排序依赖2D证据 |
| **CloseInt** (Huang et al., CVPR 2024) | 回归+适应 | 邻近空间先验 + 物理适应 | 回归范式，未使用可微渲染与外观一致性约束 |
| **Human4D** (Goel et al., ICCV 2023) | 单人多帧优化 | 时序姿态与形状先验 | 仅处理单人，无交互建模 |
| **CLIFF** (Li et al., ECCV 2022) | 单帧回归 | 透视相机模型 | 单帧单人，无交互与外观推理 |
| **MultiPhys** (Ugrinovic et al., CVPR 2024) | 物理感知优化 | 多人物理约束 | 侧重物理合理性，未引入外观渲染损失与邻近空间先验 |

**CloseApp的增量创新**体现在四个关键维度：

1. **外观约束**：引入3D高斯泼溅对人体外观进行显式建模，通过渲染差异（L1 + SSIM + LPIPS）驱动姿态优化，利用“同一人体外观在非遮挡帧中应一致”的跨帧约束来破解深度歧义。这是本工作区别于所有前述方法的核心创新。

2. **邻近空间先验**：预训练扩散模型学习双人交互的空间行为分布（姿态、相对距离、接触模式），为优化提供强先验初始化和正则化，避免陷入由视觉模糊导致的局部最优。

3. **物理穿透惩罚**：基于可微分距离场的精确穿透损失（Eq. 7），惩罚三角面片间的相互穿透，补充外观约束无法覆盖的不可见接触区域。

4. **统一优化框架**：将外观渲染损失、重投影损失、物理穿透损失、时序平滑损失及先验正则化整合为单一目标函数（Eq. 10），联合优化运动分支与外观分支参数。

### 3. 知识库定位

**CloseApp**在人体重建知识库中占据“外观感知交互重建”这一新兴节点，连接以下知识域：

- **3D高斯泼溅（3D Gaussian Splatting）**：将静态场景表示技术迁移至动态人体外观建模，通过UV高斯图实现可优化的人体纹理表示。
- **扩散模型运动先验**：将扩散模型从运动生成领域引入交互运动先验学习，条件信号为RGB图像与2D关键点。
- **可微渲染**：利用高斯泼溅的可微性，将图像空间的外观差异反向传播至SMPL姿态参数，建立“像素→姿态”的直接优化通路。
- **物理仿真约束**：借鉴物理感知运动估计中的穿透惩罚思想，将其与外观优化结合，形成互补约束体系。

### 4. 适用边界与局限

**适用条件**：
- 输入为单目野外RGB视频，包含两人近距离交互（如拥抱、握手、舞蹈）。
- 视频需包含至少部分无明显接触的帧，以便外观分支可靠地学习个体纹理特征。
- 当前仅支持双人场景，未扩展至三人及以上群体交互。

**已知局限**（来自消融实验与论文声明）：
- **外观分支退化风险**：若视频全程紧密接触，外观分支无法获得清晰的个体纹理观测，外观约束的有效性将显著下降。
- **纹理重建质量受限**：在光照剧烈变化或严重遮挡下，仅能恢复粗糙纹理（但消融实验表明粗纹理仍可提供有效的深度排序线索）。
- **计算开销**：128帧视频的优化耗时约3-5分钟，不适用于实时在线应用。
- **物理约束的权衡**：消融实验（Table 3）显示，移除穿透损失后MPJPE从59.06略微改善至57.01，但平均穿透距离（A-PD）从0.81增加至1.30，表明物理约束与姿态精度之间存在权衡——强制避免穿透可能略微牺牲关节位置精度以换取物理合理性。

### 5. 开放问题

1. **群体交互扩展**：如何将外观约束与邻近空间先验从双人推广至三人及以上场景？这需要新的多人交互数据集与可扩展的外观建模策略（如个体外观解耦）。

2. **连续严重遮挡下的鲁棒性**：当视频全程存在严重遮挡时，外观分支无法获得可靠的非遮挡帧，是否可以利用长期运动模式、场景上下文或外部人体先验（如着装模板）来弥补？

3. **多模态辅助**：能否引入深度相机、多视角或时序运动线索来降低对外观分支“无接触帧”的依赖，使框架适用于全程紧密接触的视频？

4. **跨域泛化**：当前框架在Hi4D（室内）和3DPW（室外）上验证，如何推广至手-物交互、人-物交互等更复杂的交互类型？这需要重新定义“邻近空间先验”的语义范畴。

5. **外观与运动的解耦程度**：当前框架中外观分支与运动分支通过联合优化隐式耦合，是否存在更显式的解耦策略（如先独立优化外观再固定外观优化运动），以提升优化稳定性和效率？

## 原文 PDF

![[paperPDFs/CVPR_2025/Reconstructing_Close_Human_Interaction_with_Appearance_and_Proxemics_Reasoning.pdf]]
