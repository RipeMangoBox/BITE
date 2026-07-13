---
title: "PhysGM: Large Physical Gaussian Model for Feed-Forward 4D Synthesis"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/PhysGM_Large_Physical_Gaussian_Model_for_Feed_Forward_4D_Synthesis.pdf
project_link: "https://hihixiaolv.github.io/PhysGM.github.io/"
code_link: null
aliases:
- PhysGM
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
core_operator: 通过前馈方式联合预测3D高斯表示和物理属性，并利用直接偏好优化（DPO）进行偏好对齐，无需可微模拟器或逐场景迭代，从而根本性地消除优化瓶颈。
primary_logic: 将物理基础的4D生成重构为前馈推理问题：在大规模数据集上预训练一个 Transformer 模型，一次性输出完整的几何、外观和物理参数，再通过 MPM 模拟生成动态序列；引入 DPO 根据视频真实感偏好微调物理属性分布，显著提升感知质量而不引入计算开销。
claims:
- PhysGM 首次实现从单张图像出发，在单次前馈过程中直接预测3D高斯和物理属性，无需任何逐场景优化。
- 两阶段训练策略（监督预训练 + DPO 微调）使模型学习物理先验并与视觉质量对齐，完全消除了对可微物理引擎的需求。
- 实验证明 PhysGM 在多种材料上均大幅超越基于 SDS 的优化方法，在生成速度（<1分钟）和视觉真实感（CLIP_sim, UPR）上均具有显著优势。
- PhysAssets 数据集（5种材料） 上 CLIP_sim / UPR = 0.2748 / 42.8%
---

# PhysGM: Large Physical Gaussian Model for Feed-Forward 4D Synthesis

> [!tip] 核心洞察
> 将物理基础的4D生成重构为前馈推理问题：在大规模数据集上预训练一个 Transformer 模型，一次性输出完整的几何、外观和物理参数，再通过 MPM 模拟生成动态序列；引入 DPO 根据视频真实感偏好微调物理属性分布，显著提升感知质量而不引入计算开销。

| 字段 | 内容 |
|------|------|
| 中文题名 | PhysGM：面向前馈4D合成的大规模物理高斯模型 |
| 英文题名 | PhysGM: Large Physical Gaussian Model for Feed-Forward 4D Synthesis |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2508.13911) · [Project](https://hihixiaolv.github.io/PhysGM.github.io/) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction |
| Method | PhysGM |
| Dataset | PhysAssets 数据集（5种材料）, GSO 数据集（多视图合成）, 与SOTA方法的效率对比 |

> [!tip] 效果简介
> - PhysAssets 数据集（5种材料） 上，CLIP_sim / UPR 0.2748 / 42.8% vs OmniPhysGS: 0.2091 / 10% ; DreamPhysics: 0.2291 / 17.2% (CLIP_sim +0.0657 (vs Omni), UPR +32.8% (vs Omni))。
> - GSO 数据集（多视图合成） 上，PSNR / SSIM / LPIPS (分辨率 512) 28.95 / 0.953 / 0.039 vs GS-LRM: 30.52 / 0.952 / 0.050 ; LGM: 21.44 / 0.832 / 0.122 (256) (PSNR -1.57 vs GS-LRM ; SSIM +0.001 ; LPIPS -0.011)。
> - 与SOTA方法的效率对比 上，推理时间 / CLIP_sim <1 min / 0.2748 vs OmniPhysGS: >12 h / 0.2091 ; DreamPhysics: >0.5 h / 0.2291 (推理时间缩短几十到几百倍，CLIP_sim 更高)。

## 概要

**问题瓶颈**：现有物理感知4D内容生成方法（如 **OmniPhysGS** (Lin et al., arXiv 2025) 和 **DreamPhysics** (Huang et al., AAAI 2025)）依赖两个关键前提：① 需要多视图图像经逐场景优化获得预重建的3D高斯表示；② 物理属性需手动指定或通过基于分数蒸馏采样（SDS）的迭代优化从视频扩散模型中蒸馏。这导致计算成本极高（单场景需数小时）、生成速度慢，且难以泛化到新物体。

**核心思路**：PhysGM 将物理基础的4D生成重新定义为**前馈推理问题**——从单张（或多视图）图像出发，通过一次前向传播直接预测完整的3D高斯几何外观参数和物理属性分布，再以质点法（MPM）模拟器驱动动态序列生成，全程无需逐场景优化或可微物理引擎。

**方法定位**：PhysGM 采用两阶段训练范式。第一阶段在 PhysAssets 数据集上进行监督预训练，使 Transformer 模型同时学习几何重建与物理属性预测的联合先验；第二阶段引入直接偏好优化（DPO），通过自动构建的偏好对（利用 SAM-2 分割和 CoTracker-3 轨迹提取对候选模拟排序）微调物理属性预测分布，使其与人类感知真实感对齐。这一设计从根本上消除了对可微模拟器和逐场景迭代的依赖。

**主要结果**：在 PhysAssets 数据集的5种材料上，PhysGM（含 DPO）平均 CLIP_sim 达 0.2748，用户偏好率（UPR）达 42.8%，显著超越 OmniPhysGS（0.2091 / 10%）和 DreamPhysics（0.2291 / 17.2%）。更重要的是，PhysGM 的端到端推理时间小于1分钟，相比基于优化的基线方法（>12小时 / >0.5小时）实现了数十至数百倍的加速，同时保持更高的视觉真实感。

### 问题背景

从单张图像生成物理真实的4D动态内容——即随时间演化的三维场景——是计算机视觉与图形学交叉领域的核心挑战。这一能力在游戏开发、影视特效、机器人仿真和数字孪生等应用中具有广泛需求。传统上，构建此类4D资产需要专业艺术家手工建模、设定材质参数并反复调试物理模拟参数，整个过程耗时数小时甚至数天，且高度依赖领域经验。

近年来，3D高斯泼溅（3D Gaussian Splatting, 3DGS）的兴起为高质量、实时的新视角合成提供了有力工具。与此同时，基于物理的模拟方法（如质点法，Material Point Method, MPM）能够产生符合真实世界力学规律的形变与运动。然而，将两者有效结合，从单张图像直接生成可模拟的4D内容，仍然是一个开放性问题。

### 现有方法的瓶颈

当前物理感知的4D合成方法主要分为两类，均存在根本性的效率和质量瓶颈：

**1. 基于逐场景优化的方法。** 以 **OmniPhysGS**（Lin et al., arXiv 2025）和 **DreamPhysics**（Huang et al., AAAI 2025）为代表，这些方法依赖预重建的3D高斯表示，而3DGS的重建本身就需要多视图图像和逐场景的迭代优化。在此基础上，物理属性的获取要么依赖人工手动指定，要么通过基于评分的蒸馏采样（Score Distillation Sampling, SDS）从预训练视频模型中蒸馏得到。SDS优化的核心问题在于：它需要在每个场景上反复查询视频扩散模型并计算梯度，计算成本极高（OmniPhysGS 单场景推理超过12小时），且优化过程不稳定，生成的物理参数往往偏离真实材质属性。

**2. 对可微模拟器的依赖。** 部分方法尝试将物理模拟器嵌入优化循环，利用可微物理引擎端到端地学习材质参数。然而，可微MPM模拟器的实现复杂、内存消耗巨大，且梯度回传的数值稳定性难以保证，限制了其在大规模场景中的部署。

上述方法的共同缺陷可归纳为三个关键维度：**计算成本极高**（逐场景优化，单场景需数小时至半天以上）、**泛化能力弱**（每个新场景需从头优化，无法复用已学知识）、**物理真实感与视觉真实感难以兼得**（SDS优化倾向于产生视觉上“看起来像”但物理上不合理的运动）。

### 本文动机

本文的核心洞察在于：**将物理基础的4D生成重新定义为一个前馈推理问题**。如果能够在大规模数据集上预训练一个模型，使其学会从图像中一次性推断出完整的几何、外观和物理属性，那么推理时仅需一次前馈计算即可获得所有必要参数，彻底消除逐场景优化的需求。

这一思路面临两个关键挑战：（1）如何设计一个统一的模型架构，能够同时预测3D高斯参数和物理属性；（2）如何在无需可微模拟器的情况下，使模型输出的物理参数能够产生视觉上真实且物理上合理的动态序列。针对后者，本文引入直接偏好优化（Direct Preference Optimization, DPO），通过生成候选模拟结果并依据视频真实感进行排序，以偏好对齐的方式微调物理属性预测分布，在不增加推理计算开销的前提下显著提升感知质量。

基于以上动机，本文提出 **PhysGM**——一个面向前馈4D合成的大规模物理高斯模型，首次实现了从单张图像到物理真实4D动画的端到端前馈生成，推理时间控制在1分钟以内。

## 核心方法与创新机理

PhysGM 的核心创新在于将物理感知的 4D 内容生成**重新定义为前馈推理问题**，从而根本性地消除了现有方法对逐场景优化、预重建 3D 表示和可微物理模拟器的依赖。这一范式转变通过三个关键机制实现：

### 1. 联合预测 3D 高斯与物理属性（前馈式生成）

现有物理感知 4D 合成方法（如 **OmniPhysGS** (Lin et al., arXiv 2025)、**DreamPhysics** (Huang et al., AAAI 2025)）遵循“先重建、后优化”的范式：需要从多视图图像预重建 3D 高斯表示，再通过 SDS 损失从视频扩散模型中蒸馏物理属性，整个过程需要数小时甚至更长的逐场景迭代优化。

PhysGM 打破了这一瓶颈：通过预训练的 Transformer 模型，在**单次前馈**过程中直接从输入图像联合预测完整的 3D 高斯参数 $\boldsymbol{\psi}$ 和物理属性分布 $P(\pmb{\theta} | I)$。物理属性包括材料类别、杨氏模量和泊松比的概率分布，模型输出的是分布参数（均值和方差），而非确定性值，这为后续的偏好优化提供了必要的随机性基础。

### 2. 两阶段训练策略：监督预训练 + DPO 微调

PhysGM 的训练策略是其另一核心创新。第一阶段在大规模数据集上进行**监督预训练**，使模型学习联合预测 3D 高斯表示和物理属性的生成先验。第二阶段引入**直接偏好优化（Direct Preference Optimization, DPO）**，无需可微物理引擎即可将物理属性分布与视觉真实感对齐。

DPO 的关键在于偏好对的构建：通过 SAM-2 进行前景分割，利用 CoTracker-3 在真实视频和模拟视频之间提取点轨迹，以轨迹保真度作为偏好排序的依据（参见 Figure 3）。DPO 损失函数为：

$$L_{\mathrm{DPO}}(\pi_{\omega}, \pi_{\mathrm{ref}}) = -\mathbb{E}_{(\mathbf{z},\phi_w,\phi_l)\sim D} [ \log \sigma(p_1 - p_2) ]$$

其中 $p_1$ 和 $p_2$ 分别是“获胜”和“失败”物理参数在策略模型与参考模型下的对数概率比。这一设计使得模型能够从不可微的 MPM 模拟器的反馈中学习，而无需修改模拟器本身。

### 3. 与基线方法的本质差异

| 关键维度 | OmniPhysGS / DreamPhysics | PhysGM |
|---------|--------------------------|--------|
| 3D 高斯获取 | 预重建（需多视图 + 逐场景优化） | 前馈式直接从单图/多视图预测 |
| 物理属性获取 | 手动指定或 SDS 蒸馏 | 与高斯参数联合预测，输出属性分布 |
| 优化方式 | 逐场景迭代优化（SDS 等） | 一次前馈推理 + DPO 微调（无需可微模拟器） |
| 推理时间 | >12 小时 / >0.5 小时 | <1 分钟 |

这一创新使得 PhysGM 首次实现了从单张图像出发、在 1 分钟内完成从 3D 重建到物理模拟的全流程，推理速度提升数十至数百倍，同时在 CLIP_sim 和用户偏好率（UPR）上均显著超越基于优化的基线方法。

PhysGM 的核心设计理念是将物理驱动的 4D 动态合成重构为一个**前馈推理问题**，从根本上消除传统方法对逐场景优化和可微模拟器的依赖。其整体框架可概括为一条端到端的生成流水线：从稀疏视角图像输入出发，经过多模态标记化与 Transformer 特征编码，由两个并行头部联合预测 3D 高斯表示和物理属性分布，随后以采样得到的参数初始化 MPM 模拟器，直接生成物理合理的 4D 动态序列。整个推理过程无需任何迭代优化，单次前馈即可在 **1 分钟内**完成从单张图像到高保真 4D 动画的全流程生成（Figure 1）。

![[assets/figures/papers/paper_list_l2567_https_arxiv_org_abs_2508_13911/figures/001_Figure_1.jpg]]
*Figure 1: Overview of PhysGM. Given a single image, PhysGM performs a single feed-forward pass to directly predict 3D Gaussian Splatting (3DGS) representation and its associated physical properties (e.g., stiffness, mass). This prediction is optimization-free and completes in under one second. The generated parameters then initialize a Material Point Method (MPM) simulator, producing the final, physically plausible 4D animation*

### 输入与标记化

框架接受一张或多张带相机位姿的 RGB 图像作为输入。在标记化阶段，系统采用 **DINOv3** 作为图像编码器提取视觉特征，同时利用 **Plücker 射线坐标**对每个像素的主射线进行编码以注入相机几何信息。图像特征与相机特征沿通道维度拼接，形成各视图的局部标记 $\mathbf{t}_i$。此外，在序列前端额外添加三个可学习的**全局标记** $\mathbf{g}_1, \mathbf{g}_2, \mathbf{g}_3$，用于聚合场景级信息并驱动后续物理属性的预测。完整的输入标记序列为：

$$\mathcal{T}_{\mathrm{in}} = (\mathbf{t}_i)_{i=1}^N \cup \mathbf{g}_k, \quad k=1,2,3$$

### Transformer 主干与双头解码

标记序列被送入一个 **24 层的 Transformer** 主干网络，通过自注意力机制学习上下文化的多尺度表示。输出端分为两个并行的解码头部：

1. **DPT 头部（3DGS 预测）**：基于密集预测 Transformer（Dense Prediction Transformer）架构，对多尺度特征逐步上采样，为每个视图输出逐像素的 3D 高斯参数图，包括位置、旋转四元数、各向异性缩放、不透明度和球谐颜色系数。多视图预测结果经聚合形成完整的初始 3D 高斯场景表示 $\boldsymbol{\psi}$。

2. **物理头部（Physics Head）**：从三个全局标记出发，通过一个分类头 $f_{\text{material}}$ 预测材料类别分布，以及两个回归头 $f_{\text{phys}}$ 分别预测杨氏模量 $E$ 和泊松比 $\nu$ 的高斯分布参数（均值与方差）。物理属性 $\pmb{\theta}$ 的条件分布形式为：

$$P(\pmb{\theta} | I) = \mathcal{N}(\pmb{\theta} | \pmb{\mu}_{\theta}, \mathrm{diag}(\pmb{\sigma}_{\theta}^2))$$

推理时从该分布中采样即可获得具体的物理参数 $\theta_{\text{sampled}}$。

### MPM 模拟与 4D 生成

获取 3D 高斯表示和物理属性后，框架通过**质点法（Material Point Method, MPM）** 驱动动态模拟。系统在 3D 高斯与 MPM 材料点之间建立**一一对应关系**：每个高斯原语对应一个材料点，其初始位置由高斯中心 $\pmb{\mu}_i$ 初始化。在模拟过程中，MPM 通过标准的粒子到网格（P2G）质量/动量映射、网格速度更新、以及网格到粒子（G2P）的速度与变形梯度回传，计算每个时间步的材料点形变。变形梯度 $\mathbf{F}_p$ 直接决定对应高斯的各向异性形状和朝向——通过 Neo-Hookean 本构模型将形变映射为协方差矩阵的更新：

$$\boldsymbol{\Sigma} = \mathbf{R}_{\mathrm{mat}} \mathbf{S} \mathbf{S}^T \mathbf{R}_{\mathrm{mat}}^T$$

最终渲染得到物理上合理的 4D 动态视频。

### 两阶段训练策略

PhysGM 的训练分为两个阶段以解决物理模拟不可微带来的优化难题：

- **阶段一：监督预训练**。在大规模合成数据集上，以 3D 高斯参数和物理属性的真实值作为监督信号，联合训练 DPT 头部和物理头部，使模型建立从图像到几何与物理属性的生成先验。
- **阶段二：DPO 微调**。引入**直接偏好优化（Direct Preference Optimization）**，无需可微模拟器。具体而言，从预测的物理分布中采样多组候选参数，分别进行 MPM 模拟生成视频；利用 SAM-2 和 CoTracker-3 提取真实视频与各候选视频的点轨迹，据此对候选结果排序形成偏好对 $(\phi_w, \phi_l)$；然后通过 DPO 损失微调物理头部，使模型增大生成“获胜”参数的概率、降低“失败”参数的概率：

$$L_{\mathrm{DPO}}(\pi_{\omega}, \pi_{\mathrm{ref}}) = -\mathbb{E}_{(\mathbf{z},\phi_w,\phi_l)\sim D} [ \log \sigma(p_1 - p_2) ]$$

其中 $p_1$、$p_2$ 分别为获胜和失败参数在策略模型与参考模型下的对数概率比。这一阶段使物理属性预测与视觉真实感对齐，显著提升生成质量而不增加推理开销。

### 框架的关键优势

这一整体设计带来了三个核心优势：**（1）消除优化瓶颈**——单次前馈替代了传统方法中耗时数小时的逐场景 SDS 迭代；**（2）联合预测的物理先验**——几何与物理属性的协同学习使两者相互促进，避免了分离式流水线的误差累积；**（3）偏好驱动的质量对齐**——DPO 微调在不依赖可微模拟器的前提下，有效弥合了仿真参数与感知真实度之间的鸿沟。

PhysGM 的核心架构由一个 Transformer 主干和两个并行解码头部构成，辅以 MPM 物理模拟器，实现从图像到 4D 动画的单次前馈推理。

### 多模态标记化

输入图像通过 DINOv3 编码器提取特征，相机参数采用 Plücker 射线坐标编码。对于第 $i$ 个视图，图像特征与相机特征拼接形成视图标记：

$$\mathbf{t}_i = \mathrm{concat}(E_{\mathrm{img}}(I_i), E_{\mathrm{cam}}(C_i))$$

此外，在序列前端添加三个可学习的全局标记 $\mathbf{g}_1, \mathbf{g}_2, \mathbf{g}_3$，形成完整的输入标记序列：

$$\mathcal{T}_{\mathrm{in}} = (\mathbf{t}_i)_{i=1}^N \cup \mathbf{g}_k,\quad k=1,2,3$$

该序列被送入 24 层 Transformer 主干，学习上下文表示并输出多尺度特征。

### DPT 头部：3D 高斯预测

采用 Dense Prediction Transformer（DPT）头部逐步上采样多尺度特征，输出每个视图的逐像素高斯参数图。完整的高斯参数集合为：

$$\boldsymbol{\psi} = \{(\pmb{\mu}_i, \mathbf{q}_i, \mathbf{s}_i, \alpha_i, \mathbf{c}_i)\}_{i=1}^N$$

其中 $\pmb{\mu}_i$ 为位置，$\mathbf{q}_i$ 为旋转四元数，$\mathbf{s}_i$ 为缩放因子，$\alpha_i$ 为不透明度，$\mathbf{c}_i$ 为颜色。各视图预测结果聚合形成完整场景。3D 高斯的协方差矩阵由旋转矩阵 $\mathbf{R}_{\mathrm{mat}}$ 和对角缩放矩阵 $\mathbf{S}$ 计算：

$$\boldsymbol{\Sigma} = \mathbf{R}_{\mathrm{mat}} \mathbf{S} \mathbf{S}^T \mathbf{R}_{\mathrm{mat}}^T$$

### 物理头部：物理属性分布预测

物理头部从三个全局标记出发，预测物体的物理属性分布。具体包含三个输出分支：
- **材料分类头** $f_{\mathrm{material}}$：预测材料类别 $C$ 的离散分布；
- **物理回归头** $f_{\mathrm{phys}}$：预测杨氏模量 $E$ 和泊松比 $\nu$ 的连续分布。

给定输入图像 $I$，物理属性 $\pmb{\theta}$ 的条件分布建模为对角高斯：

$$P(\pmb{\theta} | I) = \mathcal{N}(\pmb{\theta} | \pmb{\mu}_{\theta}, \mathrm{diag}(\pmb{\sigma}_{\theta}^2))$$

推理时从该分布采样获得场景参数：$\theta_{\mathrm{sampled}} \sim P(\pmb{\theta} | I)$。

### MPM 模拟器：物理动态生成

采用质点法（MPM）驱动物理模拟，在每个高斯原语与材料点之间建立一一对应关系。模拟的核心步骤包括：

**粒子到网格（P2G）质量传递：**

$$m_i = \sum_p m_p N(\mathbf{x}_i - \mathbf{x}_p)$$

**粒子到网格（P2G）动量传递：**

$$\mathbf{p}_i = \sum_p m_p \left( \mathbf{v}_p + \mathbf{C}_p (\mathbf{x}_i - \mathbf{x}_p) \right) N(\mathbf{x}_i - \mathbf{x}_p)$$

其中 $m_p$ 为粒子质量，$\mathbf{v}_p$ 为粒子速度，$\mathbf{C}_p$ 为仿射速度矩阵，$N(\cdot)$ 为插值核函数。

**网格到粒子（G2P）速度更新：**

$$\mathbf{v}_p^{n+1} = \sum_i \frac{\mathbf{p}_i^{n+1}}{m_i} N(\mathbf{x}_i - \mathbf{x}_p)$$

**网格到粒子（G2P）变形梯度更新：**

$$\mathbf{F}_p^{n+1} = \left( \mathbf{I} + \Delta t \sum_i \frac{\mathbf{p}_i^{n+1}}{m_i} \nabla N(\mathbf{x}_i - \mathbf{x}_p)^T \right) \mathbf{F}_p^n$$

变形梯度 $\mathbf{F}_p$ 直接决定高斯的各向异性形状和朝向。材料应力-应变关系采用可压缩 Neo-Hookean 模型，其 Kirchhoff 应力为：

$$\boldsymbol{\tau} = \mu \cdot J^{-2/3} \cdot \mathrm{dev}(\mathbf{B}) + \frac{\lambda}{2} \cdot (J^2 - 1) \cdot \mathbf{I}$$

其中 $\mu$ 和 $\lambda$ 为 Lamé 常数，由预测的 $E$ 和 $\nu$ 导出，$J = \det(\mathbf{F})$，$\mathbf{B} = \mathbf{F}\mathbf{F}^T$。

### DPO 微调阶段

第二阶段采用直接偏好优化（DPO），在无需可微模拟器的条件下微调物理属性预测分布。DPO 损失函数为：

$$L_{\mathrm{DPO}}(\pi_{\omega}; \pi_{\mathrm{ref}}) = -\mathbb{E}_{(\mathbf{z},\phi_w,\phi_l)\sim D}[\log \sigma(p_1 - p_2)]$$

其中 $p_1$ 和 $p_2$ 分别为获胜参数 $\phi_w$ 和失败参数 $\phi_l$ 的对数概率比：

$$p_1 = \beta \log \frac{\pi_{\omega}(\phi_w|\mathbf{z})}{\pi_{\mathrm{ref}}(\phi_w|\mathbf{z})},\quad p_2 = \beta \log \frac{\pi_{\omega}(\phi_l|\mathbf{z})}{\pi_{\mathrm{ref}}(\phi_l|\mathbf{z})}$$

该目标直接增加模型生成“获胜”参数的可能性，同时降低“失败”参数的可能性，使物理属性分布与感知真实感对齐。偏好对通过 SAM-2 分割和 CoTracker-3 轨迹提取自动构建，量化各候选模拟与真值视频的保真度。

## 实验与关键发现

### 主实验结果

PhysGM 在物理感知 4D 合成任务上展现出对现有方法的显著优势。Table 1 报告了在 PhysAssets 数据集的 5 种材料类别上的定量对比。PhysGM（含 DPO 微调）在 CLIP_sim 指标上达到 0.2748，用户偏好率（UPR）达到 42.8%，远超基于 SDS 优化的基线方法 OmniPhysGS（CLIP_sim 0.2091，UPR 10%）和 DreamPhysics（CLIP_sim 0.2291，UPR 17.2%）。这一结果验证了前馈式联合预测 3D 高斯与物理属性的策略，在视觉真实感和物理合理性两个维度上均取得了突破性提升。

![[assets/figures/papers/paper_list_l2567_https_arxiv_org_abs_2508_13911/figures/006_Table_1.jpg]]
*Table 1: Quantitative comparisons. We evaluate our method and baseline models on 5 different material types. Evaluation is based on the*

在效率维度上，Table 3 的系统性对比揭示了 PhysGM 的核心竞争力：推理时间小于 1 分钟，而 OmniPhysGS 需要超过 12 小时的逐场景优化，DreamPhysics 也需要超过 0.5 小时。PhysGM 在将推理速度提升数十至数百倍的同时，CLIP_sim 仍保持领先，表明前馈范式从根本上消除了优化瓶颈，而非以牺牲质量为代价。

![[assets/figures/papers/paper_list_l2567_https_arxiv_org_abs_2508_13911/figures/008_Table_3.jpg]]
*Table 3: Comparison with state-of-the-art methods. It can be observed that DPO achieves superior performance in generalization, inference time, and simulation quality*

多视图合成能力方面，Table 2 展示了 PhysGM 在 GSO 数据集上与 GS-LRM 和 LGM 的对比。在 512 分辨率下，PhysGM 取得 PSNR 28.95、SSIM 0.953、LPIPS 0.039 的成绩，与 GS-LRM（PSNR 30.52，SSIM 0.952，LPIPS 0.050）相比，PSNR 略低 1.57，但 SSIM 和 LPIPS 均更优。值得注意的是，PhysGM 仅使用了 GS-LRM 10% 的训练数据即达到该水平，证明了联合物理属性预测并未损害 3D 重建质量，反而通过多任务学习增强了表征能力。

![[assets/figures/papers/paper_list_l2567_https_arxiv_org_abs_2508_13911/figures/009_Table_2.jpg]]
*Table 2: Quantitative comparisons for multi-view synthesis on GSO dataset. We matched the baseline settings by comparing with LGM and GS-LRM, We achieve better results while using only 10% of the data compared to the GS-LRM*

定性结果（Figure 4、Figure 5）进一步印证了上述结论。PhysGM 能够从单张图像出发，生成涵盖弹性、塑性、流体等多种材料行为的物理合理动画，并展现出对拉伸、扭转等复杂形变的泛化能力。Figure 6 的定性对比显示，PhysGM 生成的动态序列在形变自然度和材料真实感上明显优于 OmniPhysGS 和 DreamPhysics。

![[assets/figures/papers/paper_list_l2567_https_arxiv_org_abs_2508_13911/figures/004_Figure_4.jpg]]
*Figure 4: Qualitative results by PhysGM. For different objects, we show the single input image (left), keyframes from the resulting physically-plausible simulation (middle), and the physical properties predicted by our model (right). Our method generates these highfidelity 4D sequences in under one minute from a single view, without any per-scene optimization*

### 消融实验

DPO 微调阶段是 PhysGM 性能的关键贡献因素。Table 1 中 PhysGM（w/o DPO）的平均 UPR 仅为 30%，而加入 DPO 后提升至 42.8%，相对提升 42.7%。在所有 5 种材料类别上，DPO 均带来一致的 CLIP_sim 和 UPR 提升，表明偏好对齐策略对各类材料行为具有普适的改善效果。

Figure 7 的消融可视化揭示了 DPO 的作用机制：经过两阶段训练后，模型预测的物理属性分布更接近真实值，生成的 4D 视频在物理逼真度上显著提高。这一结果验证了 DPO 的核心设计——通过偏好排序信号引导物理属性预测分布向感知真实方向偏移，而无需可微物理引擎或逐场景迭代。

![[assets/figures/papers/paper_list_l2567_https_arxiv_org_abs_2508_13911/figures/010_Figure_7.jpg]]
*Figure 7: Ablation results of DPO. The results indicate that after the two-stage DPO training, the model predicts physical attributes with greater accuracy, enabling the generation of 4D videos that exhibit higher physical fidelity*

### 方法独特性分析

Table 4 将 PhysGM 与现有物理参数预测方法进行了多维度对比。PhysGM 是首个同时消除“预优化 3D 高斯”和“预定义物理参数”双重依赖的方法。现有方法要么需要多视图图像和逐场景优化来获取 3D 高斯（如 OmniPhysGS），要么依赖手动指定的物理参数或 SDS 蒸馏（如 DreamPhysics），而 PhysGM 通过单次前馈推理直接从图像预测所有必要参数，推理时间控制在 30 秒以内，在泛化能力和效率上均建立了新的基准。

### 局限性

尽管 PhysGM 取得了显著进展，仍存在若干值得关注的局限性。首先，当前模型预测的是整个物体的单一物理属性向量，无法处理空间变化的材质属性（如局部刚度差异），这限制了在非均匀材质物体上的表现。其次，MPM 模拟器虽然提供了高保真的物理仿真，但其计算开销仍然较大，阻碍了实时交互应用的落地。此外，在高度可变形或铰接物体的泛化上可能存在不足，需要进一步扩充数据集和开展域适应研究。数据集构建中使用的 Qwen3-VL 自动标注流程，其准确性受限于视觉语言模型的能力边界，可能引入标注噪声。

### 开放问题

PhysGM 的开源方向指向若干关键问题：如何扩展架构以预测空间变化的物理属性，实现更精细的局部变形控制？如何进一步加速 MPM 模拟或采用更高效的物理引擎以降低端到端生成时延？如何缩小仿真到真实的 gap，提升在真实世界场景中的部署鲁棒性？DPO 训练中基于点轨迹的自动化偏好标注方法是否总是与人类感知一致，需要进一步的人因验证。

## 定位与知识库关联

### 问题定位：物理感知4D合成的范式跃迁

PhysGM 所解决的核心问题——从稀疏图像输入生成物理合理的动态3D内容——处于生成式AI、物理模拟与3D视觉的交叉地带。现有方法在此问题上的技术路线可划分为两个代际：**基于优化的物理感知生成**和**前馈式物理重建**。

**第一代：优化驱动范式。** 以 **OmniPhysGS**（Lin et al., arXiv 2025）和 **DreamPhysics**（Huang et al., AAAI 2025）为代表的方法遵循“先重建、后优化”的流水线。它们依赖预重建的3D高斯表示（需要多视图图像和逐场景优化），随后通过 Score Distillation Sampling（SDS）从视频扩散模型中蒸馏物理属性，或手动指定材料参数。这一范式的根本瓶颈在于：**计算成本极高**（单场景优化需数小时至半天）、**泛化能力弱**（每个新物体需重新优化），且需要可微物理模拟器或复杂的梯度近似策略。

**PhysGM 的代际跃迁。** PhysGM 将物理感知4D生成重构为**前馈推理问题**，从根本上消除了逐场景优化的需求。其核心创新在于三个层面的联合设计：（1）**联合预测**——通过单个 Transformer 模型一次性输出完整的3D高斯参数和物理属性分布；（2）**两阶段训练**——监督预训练建立生成先验，DPO 微调实现感知质量对齐；（3）**模拟器解耦**——利用 MPM 模拟器作为不可微的后处理模块，通过偏好优化间接学习物理参数，完全避免了对可微物理引擎的依赖。

这一范式跃迁的直接后果是效率与质量的同步提升：推理时间从数小时压缩至1分钟以内，同时 CLIP_sim 和用户偏好率（UPR）均显著超越优化基线（Table 1, Table 3）。

### 知识库定位：技术组件溯源与创新边界

PhysGM 的架构设计融合了多个成熟技术线，但其组合方式构成了独特的创新点。以下从三个关键技术维度进行定位。

#### 3D生成：从LRM系列到物理感知扩展

PhysGM 的 Transformer 主干和 DPT 头部直接继承了大规模3D重建模型的设计范式，特别是 **GS-LRM** 和 **LGM** 等前馈式3D高斯预测方法。在 GSO 数据集上的多视图合成对比（Table 2）表明，PhysGM 在仅使用 GS-LRM 10% 训练数据的情况下，取得了可比的 PSNR（28.95 vs 30.52）和更优的 LPIPS（0.039 vs 0.050），验证了其几何重建能力的竞争力。

**创新边界：** 与传统 LRM 类方法仅预测几何和外观不同，PhysGM 引入了**物理头部**，从全局标记预测材料类别、杨氏模量和泊松比的概率分布。这一扩展使得模型从“静态3D生成”跃迁至“物理可驱动的4D资产生成”。值得注意的是，物理属性的预测并非简单的回归任务——模型输出的是**条件高斯分布** $P(\pmb{\theta} | I) = \mathcal{N}(\pmb{\theta} | \pmb{\mu}_{\theta}, \mathrm{diag}(\pmb{\sigma}_{\theta}^2))$，这为后续的 DPO 采样和对齐提供了概率基础。

#### 物理模拟：MPM与高斯的紧耦合

PhysGM 采用 Material Point Method（MPM）作为物理引擎，这一选择具有明确的动机：MPM 天然适合处理大变形和拓扑变化，且其粒子-网格表示与3D高斯的点基元表示高度兼容。PhysGM 的创新在于**建立了材料点与高斯基元的一一对应关系**，使得变形梯度 $\mathbf{F}_p$ 直接驱动高斯的各向异性形状和朝向更新。

**与替代方案的对比：** 基于网格的有限元方法（FEM）虽精度更高，但难以处理大变形和断裂；基于位置的动力学（PBD）速度快但物理准确性不足。MPM 在精度与效率之间取得了平衡，但与纯渲染管线相比，其计算开销仍是主要瓶颈（当前单场景模拟需数十秒）。

#### 偏好对齐：DPO在物理参数空间的应用

DPO 最初由 Rafailov et al.（NeurIPS 2023）提出，用于大语言模型的偏好对齐。PhysGM 首次将其引入物理参数预测任务，具有两个关键适配：（1）**偏好数据构建**——使用 SAM-2 进行前景分割，CoTracker-3 提取运动轨迹，通过比较模拟视频与真实视频的点轨迹相似度自动生成偏好排序（Figure 3）；（2）**参数空间对齐**——DPO 损失直接作用于物理属性的概率分布，而非生成内容本身，从而在不增加推理开销的前提下提升感知质量。

消融实验（Figure 7）证实，DPO 微调阶段对物理真实感至关重要：仅监督预训练的模型（w/o DPO）在 UPR 上仅为 30%，而 DPO 微调后提升至 42.8%。

### 适用边界与局限

**当前适用边界：**
- **输入模态：** 单张或四张带位姿的RGB图像，通过 MVAdapter 可自动生成多视图。
- **材料范围：** 覆盖 PhysAssets 数据集中14种主要材料类别（占97%），包括弹性、塑性、脆性等多种本构模型。
- **交互类型：** 支持自由落体、碰撞、拉伸、扭转等典型物理交互（Figure 5），以及多物体场景。
- **输出形式：** 50帧的4D动态序列，分辨率512×512。

**明确局限：**

1. **空间均匀的物理属性假设。** 当前模型预测的是整个物体的单一物理属性向量 $(\text{material class}, E, \nu)$，无法表示空间变化的材质（如复合材料、局部硬度差异）。这是架构层面的根本限制——物理头部仅从三个全局标记预测属性分布，缺乏空间分辨能力。

2. **MPM 模拟器的计算瓶颈。** 尽管前馈推理在1秒内完成，但 MPM 模拟仍需数十秒（总时间<1分钟），限制了实时交互应用。论文未提供模拟时间的精确分解，但这一开销主要来自粒子-网格映射的迭代计算。

3. **高度可变形和铰接物体的泛化不足。** PhysAssets 数据集以刚体和有限变形物体为主，对于布料、流体、铰接机构等复杂物理系统，当前模型的泛化能力尚未验证。论文在开放问题中明确提到需要“进一步扩充数据集和域适应研究”。

4. **数据集标注的自动化偏差。** PhysAssets 使用 Qwen3-VL 进行物理属性自动标注，标注准确性受限于视觉语言模型的能力。这可能在稀有材料类别上引入系统性偏差，但论文未对此进行定量评估。

5. **偏好标注的感知一致性。** DPO 训练依赖基于点轨迹的自动偏好排序，但轨迹相似度是否总是与人类对“物理真实感”的判断一致，仍是一个开放问题。论文未进行人类偏好与自动标注的相关性分析。

### 开放问题与后续方向

**短期可推进方向：**

- **空间变化物理属性预测。** 将物理头部从全局预测扩展为逐像素或逐区域预测，可能需要引入物理属性的空间先验（如对称性、接触约束）。这需要相应的数据集支持（带空间标注的物理属性）。

- **模拟加速。** 探索更高效的物理引擎（如基于神经网络的代理模拟器）或 MPM 的 GPU 优化实现，将端到端时延压缩至秒级。

**中长期挑战：**

- **Sim-to-Real 鸿沟。** 当前模型在合成数据上训练，模拟器使用的本构模型（如 Neo-Hookean 应力 $\boldsymbol{\tau} = \mu * J^{-2/3} * \mathrm{dev}(\mathbf{B}) + (\lambda / 2) * (J^2 - 1) * \mathbf{I}$）是对真实物理的简化。如何将模型部署到真实世界场景（如机器人操作、AR交互）需要解决材质识别、光照一致性和物理参数校准等复合问题。

- **多模态物理交互。** 扩展到流体-固体耦合、断裂传播、热力耦合等更复杂的物理现象，需要更丰富的物理表示和更大规模的多样化训练数据。

- **可控生成。** 当前模型从单图自动推断物理属性，缺乏用户控制接口（如指定材质、调整弹性）。引入条件生成机制（如文本描述、物理参数滑块）将显著提升实用性。

### 方法谱系总结

PhysGM 在物理感知4D生成领域建立了**前馈推理+偏好对齐**的新范式，其核心贡献不在于单一技术组件的原创性，而在于将前馈3D重建、概率物理预测、MPM模拟和DPO对齐整合为端到端可训练系统的架构创新。与基于优化的基线相比，PhysGM 在效率上实现了数量级提升，在质量上取得了显著超越，但其空间均匀物理属性和模拟计算开销的局限，为后续研究指明了明确的改进方向。

## 原文 PDF

![[paperPDFs/CVPR_2026/PhysGM_Large_Physical_Gaussian_Model_for_Feed_Forward_4D_Synthesis.pdf]]
