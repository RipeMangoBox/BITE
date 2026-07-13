---
title: "Deformable Gaussian Occupancy: Decoupling Rigid and Nonrigid Motion with Factorized Distillation"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/Deformable_Gaussian_Occupancy_Decoupling_Rigid_and_Nonrigid_Motion_with_Factorized_Distillation.pdf
project_link: null
code_link: "https://github.com/vita-epfl/DeGO"
aliases:
- DDGO
- DGODRNMFD
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
core_operator: 引入可学习的刚性掩码，允许每个高斯自适应地在刚性偏移和非刚性变形之间切换，从而在保持刚体区域几何稳定的同时，精准建模人类中心的非刚性运动。配合从VGGT基础模型分解蒸馏获得的四维时空特征，为变形提供稳定先验。
primary_logic: 通过显式解耦刚性与非刚性运动，使高斯场能够分别优化刚性结构的稳定性和非刚性目标的灵活性，而分解式四维蒸馏将多视角和跨帧的时序一致性注入高斯特征，显著提升对动态场景的整体理解，尤其是人类实例的占用预测。
claims:
- 在Occ3D-NuScenes数据集上，DeGO相比先前最佳弱监督方法GaussianFlow*在mIoU上绝对提升1.78（相对提升10.9%），人体相关指标HCM提升13.5%。
- 消融实验表明，引入解耦变形模块使基线性能大幅提升43.4%，进一步结合VGGT蒸馏带来4.4%额外提升。
- 变形模块中尺度参数对性能影响最大，增加变形帧数至8可进一步提升。
- 分解蒸馏中的跨相机和跨帧注意力相互增强，共同贡献了4.4%总提升。
---

# Deformable Gaussian Occupancy: Decoupling Rigid and Nonrigid Motion with Factorized Distillation

> [!tip] 核心洞察
> 通过显式解耦刚性与非刚性运动，使高斯场能够分别优化刚性结构的稳定性和非刚性目标的灵活性，而分解式四维蒸馏将多视角和跨帧的时序一致性注入高斯特征，显著提升对动态场景的整体理解，尤其是人类实例的占用预测。

| 字段 | 内容 |
|------|------|
| 中文题名 | 可变形高斯占用：解耦刚性与非刚性运动与分解蒸馏 |
| 英文题名 | Deformable Gaussian Occupancy: Decoupling Rigid and Nonrigid Motion with Factorized Distillation |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://openaccess.thecvf.com/content/CVPR2026/html/Gao_Deformable_Gaussian_Occupancy_Decoupling_Rigid_and_Nonrigid_Motion_with_Factorized_CVPR_2026_paper.html) · [Code](https://github.com/vita-epfl/DeGO) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction |
| Method | DeGO (Deformable Gaussian Occupancy) |
| Dataset | Occ3D-NuScenes |

> [!tip] 效果简介
> - Occ3D-NuScenes 上，mIoU 18.05 vs 16.27 (GaussianFlow*) (+1.78 (+10.9%))；IoU 45.38 vs 40.39 (GaussianFlow*) (+4.99 (+12.4%))；HCM (Human-centric mIoU) 11.04 vs 9.73 (GaussianFlow*) (+1.31 (+13.5%))。

## 概要

**问题瓶颈**：现有弱监督三维占用预测方法普遍假设场景遵循刚体运动，仅通过简单的帧间平移偏移建模动态，无法捕捉行人等非刚性目标的细粒度变形。同时，高斯容量在静态背景上均匀分配，导致安全关键的人类实例表示严重不足，时序一致性差。

**核心思路**：本文提出 **DeGO (Deformable Gaussian Occupancy)**，通过显式解耦刚性与非刚性运动，使每个高斯原语自适应地在刚性偏移与非刚性变形之间切换——刚性区域保持几何稳定，非刚性目标（尤其是人类）获得灵活精准的运动建模。配合从 VGGT 基础模型中因子化蒸馏获得的四维时空特征，为变形提供跨相机、跨帧的稳定先验。

**方法定位**：DeGO 在弱监督三维占用预测任务中引入了两个关键改进槽位——将传统“每高斯刚性平移偏移”的运动模型替换为“可学习刚性掩码控制的解耦变形”，并将“逐帧二维教师蒸馏”升级为“因子化四维时空特征蒸馏”。训练时利用多帧增强时间一致性，推理时仅需单帧多视图图像，不增加额外推理成本。

**主要结果**：在 Occ3D-NuScenes 数据集上，DeGO 相比先前最佳弱监督方法 **GaussianFlow***（Boeder et al., arXiv 2025）在 mIoU 上绝对提升 1.78（相对提升 10.9%），IoU 提升 4.99（12.4%）。人体相关指标 HCM 提升 13.5%，实例 mIoU 提升 7.8%。消融实验表明，解耦变形模块单独贡献了 43.4% 的 mIoU 提升，因子化蒸馏在此基础上进一步带来 4.4% 增益，其中跨相机与跨帧注意力相互增强，共同驱动性能提升。

**局限与展望**：当前方法仅在训练时利用短时序（最多 8 帧），推理时依赖单帧，可能难以捕捉更长时序依赖；性能依赖于外部模型（Grounded-SAM、Metric3D、VGGT）生成的伪标签和特征质量。未来可探索更长序列、多模态输入及大规模预训练以提升四维泛化能力。



三维占用预测旨在从多视角图像中恢复场景的完整三维几何与语义表示，是自动驾驶感知系统的核心任务之一。该任务要求模型对三维空间中的每个体素同时预测其是否被占据以及所属语义类别，为下游的规划与控制提供稠密的环境理解。

### 现有方法的瓶颈

近年来，弱监督三维占用预测方法取得了显著进展。这类方法利用二维视觉基础模型（如Grounded-SAM生成语义伪标签、Metric3D生成深度伪标签）来规避昂贵的三维标注需求。代表性工作包括**SelfOcc**（Huang et al., CVPR 2024）、**GaussianOcc**（Gan et al., ICCV 2025）、**OccNeRF**（Zhang et al., TIP 2025）、**DistillNeRF**（Wang et al., NeurIPS 2024）、**GaussTR**（Jiang et al., CVPR 2025）、**VEON**（Zheng et al., ECCV 2024）以及**GaussianFlowOcc**（Boeder et al., arXiv 2025）等。然而，现有方法普遍存在两个关键缺陷：

**刚体运动假设的局限。** 当前方法几乎无一例外地假设场景中的所有物体均遵循刚体运动，仅通过简单的帧间平移偏移来建模动态。这一假设在建模行人、骑行者等非刚性目标时严重失效——这些安全关键的人类实例涉及复杂的关节变形和姿态变化，刚性偏移无法捕捉其细粒度的时空演变，导致人体类别的占用预测精度显著不足。

**高斯容量的均匀分配。** 基于三维高斯溅射的方法在表示静态场景时具有高效性，但将高斯原语均匀分布于整个场景会导致大量表示容量被浪费在静态背景区域，而安全关键的人类实例却得不到足够的表示资源。这种分配失衡直接损害了时序一致性，使得动态目标的占用预测在帧间出现抖动和断裂。

### 核心动机与解决思路

针对上述瓶颈，本文提出**可变形高斯占用（DeGO）**框架，其核心动机在于：**显式解耦刚性与非刚性运动，使高斯场能够分别优化刚性结构的稳定性和非刚性目标的灵活性**。

具体而言，DeGO引入两个关键创新：

1. **解耦高斯变形（Decoupled Gaussian Deformation, DGD）**：为每个高斯原语分配一个可学习的刚性掩码，使其自适应地在刚性偏移和非刚性变形之间切换。刚性高斯仅通过平移偏移更新，保持静态几何的稳定性；非刚性高斯则同时调整位置、旋转、尺度和不透明度，精准捕捉人类中心的细粒度运动。

2. **因子化四维特征蒸馏（Factorized Feature Distillation, FFD）**：从VGGT基础模型中分解蒸馏跨相机和跨帧的时空特征，将多视角一致性和时序连续性注入高斯特征空间，为变形提供稳定的先验引导。

通过上述设计，DeGO在不增加推理成本的前提下（推理时仅需单帧多视图图像），在Occ3D-NuScenes数据集上实现了弱监督设定下的最优性能：相比先前最佳方法**GaussianFlowOcc**，整体mIoU绝对提升1.78（相对提升10.9%），人体相关指标HCM提升13.5%。



## 核心方法与创新机理

DeGO 的核心创新在于**显式解耦刚性与非刚性运动**，并辅以**因子化的四维基础模型蒸馏**，从而在弱监督三维占用预测中同时提升全局几何精度与安全关键的人类实例建模能力。相较于现有方法普遍采用的每高斯刚性平移假设，DeGO 在两个关键维度上实现了突破。

### 解耦高斯变形：从统一刚体假设到自适应运动建模

现有弱监督占用预测方法（如 **GaussianFlowOcc**（Boeder et al., arXiv 2025）、**SelfOcc**（Huang et al., CVPR 2024））将动态场景的运动统一建模为每个高斯的刚性平移偏移。这一假设在车辆等刚体目标上尚可成立，但对行人等非刚性目标则完全失效——人体的肢体摆动、姿态变化无法用单一的平移向量描述，导致时序一致性差，人体占用预测成为性能瓶颈。

DeGO 的核心调控变量是一个**可学习的刚性掩码**（rigid-body mask）$m_i \in [0,1]$，为每个高斯原语分配一个介于 0 和 1 之间的刚性程度值。该掩码控制高斯在时序演化中采用何种运动模式：

- **刚性路径**（$m_i \to 0$）：高斯仅通过帧间偏移 $\Delta G_i^{\mathrm{rig}}(t)$ 更新位置，保留其旋转、尺度和不透明度不变，适用于静态背景和刚体车辆。
- **非刚性路径**（$m_i \to 1$）：高斯同时经历位置、旋转、尺度和不透明度的全参数变形 $\Delta G_i^{\mathrm{def}}(t)$，能够捕捉人体的细粒度非刚性运动。

两条路径通过掩码加权融合，形成最终的运动更新：

$$\Delta G_i(t) = (1 - m_i)\Delta G_i^{\mathrm{rig}}(t) + m_i\Delta G_i^{\mathrm{def}}(t)$$

这一设计的因果机制在于：**刚性掩码使高斯场能够自适应地分配建模容量**。静态背景中的高斯自然趋向于 $m_i \to 0$，仅消耗少量刚性偏移参数；而人体区域的高斯则获得更大的 $m_i$ 值，激活全参数变形能力。消融实验（Table 2）表明，仅引入解耦变形模块（DGD）即可使基线性能提升 **43.4%** 的 mIoU，验证了运动解耦本身是性能跃升的主要驱动力。

在变形模块的参数消融（Table 4）中，**尺度参数**对性能影响最大，其次为旋转参数，这表明非刚性目标的尺度变化（如人体靠近或远离相机）是动态占用预测中最关键的变形维度。此外，增加变形帧数从 4 帧到 8 帧可进一步提升 mIoU 至 18.05（Table 3），说明更长的时序上下文为变形预测提供了更丰富的运动先验。

### 因子化四维蒸馏：从二维逐帧蒸馏到时空联合知识迁移

现有弱监督方法（如 **GaussianOcc**（Gan et al., ICCV 2025）、**GaussTR**（Jiang et al., CVPR 2025））通常使用 DINO 或 CLIP 等二维基础模型进行逐帧特征蒸馏，仅提供单帧空间语义监督，完全忽略了跨帧时序一致性。

DeGO 提出的**因子化特征蒸馏（FFD）** 从 VGGT 基础模型中提取四维时空特征作为监督信号。VGGT 的 Transformer 块采用**交替式注意力**设计：先在多相机视图间执行跨相机（空间）注意力，再在时间维度上执行跨帧（时序）注意力。DeGO 将这种因子化的时空特征蒸馏到学生高斯场的渲染特征中，使高斯特征同时对齐多视角几何一致性和跨帧运动一致性。

蒸馏损失在参考帧 $t=0$ 上计算学生特征 $\mathbf{S}_0'$ 与教师特征 $\mathbf{T}_0'^{(\ell)}$ 的余弦相似度：

$$\mathcal{L}_{\mathrm{distil}} = \frac{1}{|\mathcal{V}||\Omega|} \sum_{v \in \mathcal{V}} \sum_{u \in \Omega} \Big(1 - \cos\big(\mathbf{T}_{0}^{\prime(\ell)}(v)[u], \mathbf{S}_{0}^{\prime}(v)[u]\big)\Big)$$

消融实验（Table 5）揭示了跨相机与跨帧蒸馏的**相互增强效应**：单独使用跨相机蒸馏或跨帧蒸馏均能带来提升，但两者联合使用贡献了完整的 4.4% 额外 mIoU 提升，表明空间一致性和时序一致性在四维场景理解中互为补充。

蒸馏策略的另一个关键设计选择是**特征对齐的目标模块**：将蒸馏应用于高斯 Transformer（而非图像编码器）效果最佳（Table 6），且教师-学生对齐模块的投影维度设为 32 为最优（Table 7），这在高斯特征空间的信息保持与计算效率之间取得了平衡。

### 训练-推理解耦的时序设计

DeGO 的第三个关键设计在于**训练与推理的时序不对称性**：训练时利用多帧（最多 8 帧）历史信息进行变形预测和蒸馏，充分学习时序运动模式；推理时仅需单帧多视图图像，不引入额外的时间输入或计算开销。这一设计使 DeGO 在推理效率上与纯单帧方法持平，却在性能上显著超越了同样使用单帧推理的 **GaussianFlowOcc**（mIoU 18.05 vs. 16.27），证明了训练阶段的时序监督能够有效蒸馏为单帧推理能力。

### 创新点的协同效应

解耦变形与因子化蒸馏并非独立运作，而是形成正向反馈循环：VGGT 蒸馏提供的四维时空特征为变形模块提供了稳定的运动先验，使刚性掩码能够更准确地判断每个高斯应采用的运动模式；反过来，准确的运动解耦使蒸馏特征的对齐更加精准，减少了静态背景中的噪声干扰。Table 2 的消融实验完整展示了这一协同效应：基线 → +DGD（+43.4%）→ +FFD（+4.4%），两个模块的叠加带来了远超各自独立贡献的总体性能提升。

在主实验（Table 1）中，DeGO 在 Occ3D-NuScenes 上达到 **18.05 mIoU**，相比先前最佳弱监督方法 GaussianFlow* 绝对提升 **1.78**（相对提升 10.9%），在人体相关指标 HCM 上更是取得 **13.5%** 的相对提升，验证了运动解耦与四维蒸馏在安全关键场景中的实际价值。



DeGO 构建了一个统一的**可变形高斯占用预测框架**，其核心设计在于将动态三维场景的建模分解为两个协同模块：**解耦高斯变形**（Decoupled Gaussian Deformation，DGD）与**因子化特征蒸馏**（Factorized Feature Distillation，FFD）。整个 pipeline 的输入输出流如图2所示（Figure 2）。

![[assets/figures/papers/paper_list_l2_https_openaccess_thecvf_com_content_CVPR2026_html_Gao_Deformable_Gaussia/figures/002_Figure_2.jpg]]
*Figure 2: Overview of the proposed DeGO framework. It unifies the Decoupled Gaussian Deformation (DGD) and Factorized Feature Distillation (FFD). The spatialtemporal features from VGGT teacher guides Gaussian rendering through feature alignment, producing foundation-aligned 4D features that drive decoupled motion prediction for nonrigid classes and rigid classes*

### 输入与输出

框架的输入为多视角图像序列，输出为目标时刻的三维语义占用场。具体而言，给定一组多相机视图 $\mathcal{V}$ 和时间窗口 $t \in [-T, 0]$，模型学习一个映射：

$$f_{\theta} : (\mathbf{x}, t) \mapsto (p_{\mathrm{occ}}, p_{\mathrm{sem}}), \quad \mathbf{x} \in \mathbb{R}^{3}, \ t \in [-T, 0]$$

其中 $p_{\mathrm{occ}}$ 为占用概率，$p_{\mathrm{sem}}$ 为语义类别分布（Eq. 1）。

### 模块关系与数据流

**1. 图像编码与规范高斯生成**

首先，图像编码器从多视角输入中提取特征，高斯解码器据此在参考帧 $t=0$ 生成一组**规范三维高斯原语**。每个高斯原语 $G_i$ 包含位置 $\mu_i$、旋转 $r_i$、尺度 $s_i$、不透明度 $\alpha_i$ 以及高维特征向量 $\mathbf{f}_i$。

**2. 因子化特征蒸馏（FFD）**

该模块将 VGGT 基础模型作为教师网络，从中提取四维时空特征作为监督信号。VGGT 的 Transformer 块交替执行**跨相机（空间）注意力**和**跨帧（时间）注意力**，产生富含时空一致性的特征表示。蒸馏过程将教师特征 $\mathbf{T}_{0}^{\prime(\ell)}(v)$ 与学生渲染特征 $\mathbf{S}_{0}^{\prime}(v)$ 在参考帧进行余弦相似度对齐：

$$\mathcal{L}_{\mathrm{distil}} = \frac{1}{|\mathcal{V}||\Omega|} \sum_{v \in \mathcal{V}} \sum_{u \in \Omega} \Big(1 - \cos\big(\mathbf{T}_{0}^{\prime(\ell)}(v)[u], \mathbf{S}_{0}^{\prime}(v)[u]\big)\Big)$$

蒸馏后的高斯特征同时蕴含了空间多视角一致性和时间运动线索，为后续变形预测提供稳定先验。

**3. 解耦高斯变形（DGD）**

DGD 模块接收规范高斯及其蒸馏特征，预测每个高斯在目标时刻的运动更新。其关键创新在于引入一个可学习的**刚性掩码** $m_i \in [0, 1]$，自适应地控制每个高斯的运动类型：

$$\Delta G_{i}(t) = (1 - m_{i})\Delta G_{i}^{\mathrm{rig}}(t) + m_{i}\Delta G_{i}^{\mathrm{def}}(t)$$

- 当 $m_i \to 0$ 时，高斯仅执行刚性平移偏移，适用于静态背景或刚体运动；
- 当 $m_i \to 1$ 时，高斯同时进行位置、旋转、尺度和不透明度的非刚性变形，专为人体等可变形目标设计。

变形预测通过 MLP 实现，其输入为高斯位置的空间编码 $\gamma_{p}(\pmb\mu)$ 和时间编码 $\gamma_{t}(t)$ 的拼接，输出各参数的时序增量。

**4. 可微渲染与占用预测**

变形后的高斯场被投影到各相机视图，通过可微高斯光栅化渲染语义图和深度图。渲染的语义与伪真值标签（由 Grounded-SAM 生成）计算交叉熵损失，深度与 Metric3D 生成的伪深度计算 L1 损失。最终，一个轻量级预测头从体素特征中输出占用概率和语义分布：

$$p_{\mathrm{occ}}(\mathbf{x}, t) = \sigma(\mathbf{w}_{\mathrm{occ}} \mathbf{f}_{x,t}), \quad p_{\mathrm{sem}}(\mathbf{x}, t) = \mathrm{softmax}(\mathbf{w}_{\mathrm{sem}} \mathbf{f}_{x,t})$$

### 训练与推理解耦

训练阶段利用多帧（最多 8 帧）增强时间一致性，而推理时仅需单帧多视图图像，不引入额外时间输入，保证了与现有弱监督方法同等的推理效率。总损失函数组合了语义损失、深度损失、蒸馏损失和变形正则化损失（含 L2 正则项 $\mathcal{L}_{\mathrm{reg}}$ 与掩码二值化项 $\mathcal{L}_{\mathrm{mask}}$），实现端到端的弱监督优化。

> **注意**：蒸馏应用于高斯 Transformer 层（而非图像编码器）效果最佳，投影维度 32 为最优配置（Table 6, Table 7）。跨相机与跨帧注意力在蒸馏中相互增强，共同贡献了 4.4% 的 mIoU 提升（Table 5）。

### 补充图表

![[assets/figures/papers/paper_list_l2_https_openaccess_thecvf_com_content_CVPR2026_html_Gao_Deformable_Gaussia/figures/001_Figure_1.jpg]]
*Figure 1: Overview of our deformable Gaussian occupancy framework. We enable Gaussians to adaptively model rigid and nonrigid motion. Deformable Gaussians evolve through both nonrigid deformation and offsets, while rigid Gaussians use only offset updates. Foundation-model distillation provides cross-camera and cross-frame guidance, yielding more accurate occupancy prediction via temporal consistency*



### 问题形式化

DeGO 将三维占用预测形式化为一个四维映射问题。给定世界坐标 $\mathbf{x} \in \mathbb{R}^3$ 和时间步 $t \in [-T, 0]$，模型学习一个函数：

$$f_{\theta} : (\mathbf{x}, t) \mapsto (p_{\mathrm{occ}}, p_{\mathrm{sem}})$$

该函数将时空坐标映射到占用概率 $p_{\mathrm{occ}}$ 和语义分布 $p_{\mathrm{sem}}$。占用预测通过线性投影和 sigmoid 激活从体素特征 $\mathbf{f}_{x,t}$ 获得：

$$p_{\mathrm{occ}}(\mathbf{x}, t) = \sigma(\mathbf{w}_{\mathrm{occ}} \mathbf{f}_{x,t})$$

语义预测则通过线性投影和 softmax 获得类别分布：

$$p_{\mathrm{sem}}(\mathbf{x}, t) = \mathrm{softmax}(\mathbf{w}_{\mathrm{sem}} \mathbf{f}_{x,t})$$

### 解耦高斯变形（DGD）

DGD 模块的核心创新在于为每个高斯原语引入可学习的刚性掩码 $m_i \in [0,1]$，该掩码隐式地控制高斯仅执行刚性偏移，还是同时进行偏移和非刚性变形。给定规范空间（参考帧 $t=0$）中的高斯，DGD 预测其在 $T$ 个目标时间步上的位置、旋转、尺度和不透明度演化。

**时空编码**：为捕捉平滑的时序变化，模块使用正弦余弦编码分别对空间坐标和时序进行编码：

$$\gamma_{p}(\pmb\mu) = \left[ \pmb\mu, \sin(2^{k}\pmb\mu), \cos(2^{k}\pmb\mu) \right]_{k=0}^{L_{p}-1}$$

$$\gamma_{t}(t) = \left[ t, \sin(2^{k}t), \cos(2^{k}t) \right]_{k=0}^{L_{t}-1}$$

**运动组合**：刚性掩码通过加权融合实现运动解耦，最终的参数更新为：

$$\Delta G_{i}(t) = (1 - m_{i})\Delta G_{i}^{\mathrm{rig}}(t) + m_{i}\Delta G_{i}^{\mathrm{def}}(t)$$

其中 $\Delta G_{i}^{\mathrm{rig}}(t)$ 为刚性偏移更新，$\Delta G_{i}^{\mathrm{def}}(t)$ 为非刚性变形更新。当 $m_i \to 0$ 时，高斯退化为纯刚性运动；当 $m_i \to 1$ 时，高斯允许完整的非刚性变形。

**变形正则化**：为约束变形行为并促进掩码二值化，引入变形损失：

$$\mathcal{L}_{\mathrm{def}} = \lambda_{\mathrm{reg}}\mathcal{L}_{\mathrm{reg}} + \lambda_{\mathrm{mask}}\mathcal{L}_{\mathrm{mask}}$$

其中正则化项对各高斯参数的变形偏移量施加 L2 惩罚：

$$\mathcal{L}_{\mathrm{reg}} = \sum_{p \in \{\mu, r, s, \alpha\}} \lambda_{p} \| \Delta p_{i}(t) \|_{2}^{2}$$

掩码损失鼓励二值化：

$$\mathcal{L}_{\mathrm{mask}} = [m_i(1 - m_i)]$$

### 因子化特征蒸馏（FFD）

FFD 模块从 VGGT 基础模型中提取四维时空特征作为监督信号。VGGT 的 Transformer 块交替执行跨相机（空间）注意力和跨帧（时间）注意力，产生蕴含多视角几何一致性和时序运动信息的特征表示。

蒸馏在参考帧 $t=0$ 上进行，通过最小化学生渲染特征 $\mathbf{S}_{0}^{\prime}(v)$ 与教师特征 $\mathbf{T}_{0}^{\prime(\ell)}(v)$ 之间的余弦距离实现：

$$\mathcal{L}_{\mathrm{distil}} = \frac{1}{|\mathcal{V}||\Omega|} \sum_{v \in \mathcal{V}} \sum_{u \in \Omega} \Big(1 - \cos\big(\mathbf{T}_{0}^{\prime(\ell)}(v)[u], \mathbf{S}_{0}^{\prime}(v)[u]\big)\Big)$$

其中 $\mathcal{V}$ 为相机视图集合，$\Omega$ 为像素坐标集合，$\ell$ 为教师网络层索引。蒸馏目标是将 VGGT 的跨相机空间一致性和跨帧时序一致性注入高斯特征空间，为 DGD 模块提供稳定的运动先验。

### 总体优化目标

训练时的总损失由语义分割损失、深度损失、蒸馏损失和变形正则化损失组成。语义损失使用 Grounded-SAM 生成的伪标签进行交叉熵监督：

$$\mathcal{L}_{\mathrm{seg}} = \frac{1}{|\mathcal{V}||\Omega|} \sum_{v \in \mathcal{V}} \sum_{u \in \Omega} \mathrm{CE}\big(\hat{y}_v(u), y_v^{\mathrm{pseudo}}(u)\big)$$

深度损失使用 Metric3D 生成的伪深度标签。值得注意的是，蒸馏损失应用于高斯 Transformer 特征而非图像编码器特征时效果最佳，投影维度 32 为最优配置（Table 6, Table 7）。



## 实验与关键发现

### 实验设置与基准

所有实验在Occ3D-NuScenes数据集上进行，遵循弱监督设定：语义标签由Grounded-SAM生成，深度标签由Metric3D生成，确保与先前弱监督方法的公平比较。推理时所有方法均仅使用单帧多视图图像，不引入额外时间输入。对比基线包括**SelfOcc**（Huang et al., CVPR 2024）、**GaussianOcc**（Gan et al., ICCV 2025）、**OccNeRF**（Zhang et al., TIP 2025）、**DistillNeRF**（Wang et al., NeurIPS 2024）、**GaussTR**（Jiang et al., CVPR 2025）以及最直接的弱监督基线**GaussianFlow**（Boeder et al., arXiv 2025，标记*表示从官方代码复现）。评估指标涵盖整体IoU、mIoU、实例mIoU（InsM）、场景mIoU（ScnM）以及本文提出的人体中心mIoU（HCM），后者聚焦安全关键的人体类别。

### 主要结果

Table 1展示了Occ3D-NuScenes上的弱监督方法定量对比。DeGO在所有指标上均取得最优：

- **整体IoU**：45.38，相比GaussianFlow*的40.39绝对提升4.99（相对提升12.4%）。
- **mIoU**：18.05，相比GaussianFlow*的16.27绝对提升1.78（相对提升10.9%）。
- **人体中心指标HCM**：11.04，相比GaussianFlow*的9.73绝对提升1.31（相对提升13.5%），验证了解耦变形对人类非刚性目标的针对性建模优势。
- **实例mIoU（InsM）**：10.34，相比GaussianFlow*的9.59提升7.8%。

从逐类细分看，DeGO在“行人”（pedestrian）、“自行车”（bicycle）等非刚性类别上优势尤为突出，同时在“可驾驶路面”（driving surface）等静态背景类别上也保持领先，表明刚性掩码有效防止了静态区域的容量浪费。定性可视化（Figure 3）进一步印证：DeGO在人体姿态变化场景中产生更连贯、更准确的占用预测，而基线方法常出现肢体断裂或缺失。

![[assets/figures/papers/paper_list_l2_https_openaccess_thecvf_com_content_CVPR2026_html_Gao_Deformable_Gaussia/figures/010_Figure_3.jpg]]
*Figure 3: Qualitative comparison with the state-of-the-art method. The upper three scenes focus on Human-centric nonrigid classes, and the lower two scenes focus on static context*

### 消融实验

#### 变形模块与蒸馏的贡献分解

Table 2的消融揭示了各组件的因果链路：

- **无变形无蒸馏的基线**：仅使用刚性高斯偏移，性能极低（mIoU约2.5级别，具体数值需参考原文Table 2）。
- **引入解耦高斯变形（DGD）**：mIoU相比基线大幅提升43.4%，这是整个框架中**最关键的单一提升**。刚性掩码使高斯能够自适应地在刚性与非刚性运动间切换，将建模容量集中分配给需要变形的区域。
- **进一步加入VGGT因子化特征蒸馏（FFD）**：在DGD基础上额外带来4.4%的mIoU提升，证明四维时空蒸馏为变形提供了稳定的先验引导。
- **替换蒸馏源为DINOv2**：提升幅度低于VGGT蒸馏，表明VGGT的分解式时空注意力结构对动态场景理解具有独特优势。

#### 变形帧数的影响

Table 3显示，变形帧数从4增至8时mIoU进一步提升至18.05，表明更长的时序窗口有助于捕捉非刚性运动的演化规律。但帧数继续增加是否持续获益，原文未给出超过8帧的实验，需进一步验证。

#### 变形参数的消融

Table 4考察了变形模块中不同高斯参数（位置μ、旋转r、尺度s）的贡献：

- **尺度参数**对性能影响最大，移除尺度变形导致性能下降最为显著。
- **旋转参数**次之，移除旋转变形也带来明显退化。
- 三者联合建模取得最佳效果，说明非刚性目标的变形在位置、朝向和形状尺度上均需灵活调整。

#### 蒸馏策略的消融

Table 5验证了跨相机注意力与跨帧注意力的协同效应：

- 仅使用跨相机蒸馏或仅使用跨帧蒸馏时，各自带来约2%级别的提升（具体数值需参考原文Table 5）。
- 两者联合使用时，总提升达到4.4%，**超过单独贡献之和**，表明空间一致性与时序一致性相互增强——跨帧信息帮助跨相机特征对齐，反之亦然。

Table 6和Table 7进一步优化蒸馏配置：

- 蒸馏应用于**高斯变换器**（而非图像编码器）效果最佳，说明在高斯特征空间进行对齐更直接地影响占用预测质量。
- 教师网络中间层（而非最后层）的特征蒸馏效果最优。
- 对齐模块的投影维度取32时达到最佳精度-效率平衡。

### 失败模式与局限性分析

尽管DeGO取得了显著提升，仍存在以下局限：

1. **长时序依赖不足**：当前方法仅在训练时利用最多8帧的短时序窗口，推理时完全依赖单帧。对于持续时间超过8帧的缓慢变形（如行人持续下蹲），模型可能无法充分捕捉运动趋势。扩展至更长序列或引入递归结构是潜在改进方向。

2. **外部模型依赖链**：性能受制于Grounded-SAM（语义伪标签）、Metric3D（深度伪标签）和VGGT（蒸馏特征）三个外部模型的准确性。任一环节的误差会通过伪标签监督和特征蒸馏两条路径传播，在遮挡严重或光照极端的场景下风险加剧。

3. **非刚性类别的绝对性能仍低**：尽管HCM相对提升13.5%，其绝对值（11.04）仍远低于整体mIoU（18.05）和场景mIoU（33.46），说明人体等非刚性目标的占用预测仍是开放难题，变形模型的表达能力尚有提升空间。

4. **泛化性未验证**：实验仅基于NuScenes的单模态（相机）设定，未在雷达融合、大规模预训练或跨数据集迁移场景下评估，方法的通用性有待进一步检验。

### 关键图表结论速览

- **Table 1**：DeGO在全部指标上超越所有弱监督基线，人体中心指标HCM提升13.5%最为突出。
- **Table 2**：解耦变形模块贡献43.4%的巨幅提升，VGGT蒸馏额外贡献4.4%，两者缺一不可。
- **Table 3**：变形帧数8优于4，时序窗口长度与性能正相关。
- **Table 4**：尺度是变形模块中最重要的参数，其次为旋转。
- **Table 5**：跨相机与跨帧蒸馏相互增强，联合效果大于单独之和。
- **Table 6-7**：蒸馏作用于高斯变换器、取中间层特征、投影维度32为最优配置。

![[assets/figures/papers/paper_list_l2_https_openaccess_thecvf_com_content_CVPR2026_html_Gao_Deformable_Gaussia/figures/003_Table_1.jpg]]
*Table 1: Quantitative comparison of weakly supervised methods on the Occ3D-NuScenes [3, 35] benchmark. We report the overall IoU and mIoU, as well as Instance mIoU (InsM), Scene mIoU (ScnM), and the proposed Human-centric mIoU (HCM) that focuses on safety-critical human classes. * indicates reproduced results from official code. ‘cons. veh.’ is short for construction vehicle, and ‘drive. surf.’ indicates driving surface. Best number for each class is in bold, and the second best is underlined*

![[assets/figures/papers/paper_list_l2_https_openaccess_thecvf_com_content_CVPR2026_html_Gao_Deformable_Gaussia/figures/004_Table_2.jpg]]
*Table 2: Ablation of the deformation module and different foundation-model distillation settings*

![[assets/figures/papers/paper_list_l2_https_openaccess_thecvf_com_content_CVPR2026_html_Gao_Deformable_Gaussia/figures/005_Table_3.jpg]]
*Table 3: Impact of the number of deformed frames*

![[assets/figures/papers/paper_list_l2_https_openaccess_thecvf_com_content_CVPR2026_html_Gao_Deformable_Gaussia/figures/006_Table_6.jpg]]
*Table 6: Impact of different teacher layers on distillation*

![[assets/figures/papers/paper_list_l2_https_openaccess_thecvf_com_content_CVPR2026_html_Gao_Deformable_Gaussia/figures/007_Table_4.jpg]]
*Table 4: Ablation on different parameters in deformation module*

![[assets/figures/papers/paper_list_l2_https_openaccess_thecvf_com_content_CVPR2026_html_Gao_Deformable_Gaussia/figures/009_Table_5.jpg]]
*Table 5: Ablation on cross-camera and cross-frame distillation*

### 补充图表

![[assets/figures/papers/paper_list_l2_https_openaccess_thecvf_com_content_CVPR2026_html_Gao_Deformable_Gaussia/figures/008_Table_7.jpg]]
*Table 7: Ablation on the projection dimension in the teacherstudent alignment module*



## 定位与知识库关联

### 任务定位与基线关系

DeGO 面向**弱监督三维占用预测**（weakly-supervised 3D occupancy prediction），其核心设定与以下工作处于同一比较体系：

- **GaussianFlowOcc**（Boeder et al., arXiv 2025）：当前弱监督占用预测的最强基线，同样采用高斯原语表示场景，但仅通过每高斯的刚性平移偏移建模动态。DeGO 在其基础上引入解耦变形和分解蒸馏，在 Occ3D-NuScenes 上实现 mIoU 绝对提升 1.78（相对提升 10.9%），人体相关指标 HCM 提升 13.5%（Table 1）。
- **SelfOcc**（Huang et al., CVPR 2024）、**GaussianOcc**（Gan et al., ICCV 2025）、**OccNeRF**（Zhang et al., TIP 2025）、**DistillNeRF**（Wang et al., NeurIPS 2024）、**GaussTR**（Jiang et al., CVPR 2025）、**VEON**（Zheng et al., ECCV 2024）、**LangOcc**（Boeder et al., arXiv 2024）：这些方法均在弱监督或自监督设定下进行占用预测，但普遍假设刚体运动或仅依赖逐帧二维教师模型（如 DINO/CLIP）的特征蒸馏。DeGO 的关键差异化在于**显式解耦刚性与非刚性运动**，以及从 VGGT 基础模型进行**因子化四维时空特征蒸馏**。

### 方法谱系中的关键改进槽位

DeGO 在现有高斯占用框架上改动了三个核心槽位：

| 槽位 | 基线做法 | DeGO 做法 | 证据锚点 |
|------|----------|-----------|----------|
| **运动模型** | 每高斯刚性平移偏移 | 可学习刚性掩码控制每高斯自适应选择刚性偏移和/或非刚性变形（位置、旋转、尺度、不透明度） | Sec. 4.1 |
| **蒸馏策略** | 逐帧二维教师模型蒸馏（DINO/CLIP） | 因子化四维特征蒸馏，从 VGGT 同时蒸馏跨相机空间注意力和跨帧时间注意力 | Sec. 4.2 |
| **时序建模** | 邻近帧预测偏移，训练与推理可能解耦不足 | 训练时多帧（最多 8 帧）增强时间一致性，推理时仅用单帧，不增加推理成本 | Sec. 4.3 |

消融实验（Table 2）定量揭示了各改进的贡献：引入解耦变形模块（DGD）使基线性能大幅提升 43.4%，在此基础上加入 VGGT 蒸馏（FFD）进一步带来 4.4% 的额外提升。在蒸馏内部，跨相机和跨帧注意力相互增强，共同贡献这 4.4% 的总提升（Table 5）。

### 适用边界与局限

1. **时序依赖长度有限**：当前方法仅在训练时利用短时序信息（最多 8 帧，Table 3 显示帧数从 4 增至 8 可提升 mIoU 至 18.05），推理时仅依赖单帧。对于需要更长时序运动依赖的场景（如缓慢的行人意图变化、长时遮挡恢复），模型可能无法充分捕捉。

2. **对外部模型的依赖链**：DeGO 的性能建立在多个外部模型生成的伪标签和特征之上——Grounded-SAM 提供语义伪标签，Metric3D 提供深度伪标签，VGGT 提供蒸馏特征。这些上游模型的误差会沿依赖链传播，且当前论文未系统评估各外部模型失效时的性能退化程度。

3. **泛化验证范围有限**：目前仅在 Occ3D-NuScenes 单一基准上验证，尚未在更大规模预训练、多模态输入（如雷达、激光雷达）或跨数据集迁移场景下评估泛化能力。

4. **变形模块的参数敏感性**：消融实验（Table 4）表明尺度参数对变形性能影响最大，其次为旋转。这意味着在实际部署中，变形模块的超参数（各属性的正则化权重）可能需要针对不同场景进行调优，增加了工程适配成本。

### 开放问题

1. **长时序与多模态扩展**：如何将解耦变形框架扩展至更长的视频序列或多模态输入（如融合雷达点云），以进一步提升对复杂动态场景的建模能力？这涉及高斯原语在长时序下的累积误差控制和跨模态特征对齐。

2. **大规模预训练的潜力**：当前 VGGT 蒸馏仅作用于高斯变换器层（Table 6 显示应用于高斯变换器而非图像编码器效果最佳，投影维度 32 为最优，Table 7），若将整个框架纳入大规模 4D 预训练，能否进一步提升时空表征的泛化性？

3. **在线学习与教师解耦**：蒸馏过程依赖 VGGT 教师的离线推理，计算开销较大。如何避免教师模型的计算瓶颈，实现轻量化的在线蒸馏或自蒸馏，是将方法推向实时自动驾驶系统的关键挑战。

4. **刚性掩码的可解释性**：当前刚性掩码通过二值化损失约束趋近 0/1，但其学习到的刚性与非刚性区域划分是否与人类语义一致（例如，是否真正将行人归为非刚性、车辆归为刚性），尚未进行定性分析。这一可解释性问题对于安全关键应用尤为重要。



## 原文 PDF

![[paperPDFs/CVPR_2026/Deformable_Gaussian_Occupancy_Decoupling_Rigid_and_Nonrigid_Motion_with_Factorized_Distillation.pdf]]
