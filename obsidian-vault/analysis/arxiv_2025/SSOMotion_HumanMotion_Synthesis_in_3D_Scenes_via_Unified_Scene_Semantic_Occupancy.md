---
title: SSOMotion HumanMotion Synthesis in 3D Scenes via Unified Scene Semantic Occupancy
type: paper
paper_level: A
venue: arXiv
year: 2025
pdf_ref: paperPDFs/arxiv_2025/SSOMotion_HumanMotion_Synthesis_in_3D_Scenes_via_Unified_Scene_Semantic_Occupancy.pdf
project_link: null
code_link: https://github.com/jingyugong/SSOMotion
aliases:
- SHS3SUSSO
tags:
- arxiv_2025
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
core_operator: 采用统一场景语义占用（SSO）表示，通过双向三平面分解将体素信息压缩为轻量级特征图，并利用CLIP文本编码加共享线性降维实现跨数据集的统一语义表达。
primary_logic: 双向三平面分解与统一语义映射相结合，能以极低计算成本为运动合成提供细粒度、跨数据集的语义结构提示，从而显著提升动作自然度和指令达成率。
claims:
- 在移动和交互任务上，SSOMotion 在目标距离、穿透等指标上显著优于 DIMOS
- 双向三平面分解与语义降维使场景感知和运动-场景关联的计算量从 20783 GFLOPs 降至 0.49 GFLOPs
- 空间语义信息能帮助模型更准确地识别可交互区域（如坐下位置）
- Cluttered scenes with ShapeNet furniture (Locomotion) 上 avg. dist (m), loco. pene., time (s) = 0.02, 0.95, 3.60
---

# SSOMotion HumanMotion Synthesis in 3D Scenes via Unified Scene Semantic Occupancy

> [!tip] 核心洞察
> 双向三平面分解与统一语义映射相结合，能以极低计算成本为运动合成提供细粒度、跨数据集的语义结构提示，从而显著提升动作自然度和指令达成率。

| 字段 | 内容 |
|------|------|
| 中文题名 | 基于统一场景语义占用的3D场景人体运动合成 |
| 英文题名 | SSOMotion HumanMotion Synthesis in 3D Scenes via Unified Scene Semantic Occupancy |
| 会议/期刊 | arXiv 2025 |
| Links | [Code](https://github.com/jingyugong/SSOMotion) · [paper](https://arxiv.org/abs/2511.07819) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction |
| Method | SSOMotion |
| Dataset | Cluttered scenes with ShapeNet furniture, HUMANISE |

> [!tip] 效果简介
> - Cluttered scenes with ShapeNet furniture (Locomotion) 上，avg. dist (m), loco. pene., time (s) 0.02, 0.95, 3.60。
> - Cluttered scenes with ShapeNet furniture (Interaction) 上，sit time (s), pene. mean, pene. max / lie time (s), pene. mean, pene. max sit: 3.45, 1.83, 6.78; lie: 3.69, 5.74, 40.48。
> - HUMANISE (Motion Prediction) 上，MPJPE (m), MPVPE (m), Goal Dist. (m) 0.095, 0.118, 0.045。

## 概要

3D 场景中的人体运动合成要求模型同时理解空间结构与语义可供性，以生成符合物理规律且满足任务指令的自然动作。现有方法（如 **DIMOS**, Zhao et al., ICCV 2023）主要依赖场景的空间结构信息进行碰撞避免，却忽略了语义信息对行为理解的关键作用，导致模型无法正确识别可交互区域（如可坐的椅子与不可坐的桌子）。此外，高维语义特征提取带来的冗余计算严重制约了实际部署效率。

针对上述瓶颈，本文提出 **SSOMotion**，其核心思路是构建 **统一场景语义占用（Scene Semantic Occupancy, SSO）** 表示，并通过 **双向三平面分解** 与 **统一语义映射** 两项关键设计，实现轻量且语义丰富的场景感知。具体而言：双向三平面分解将体素化的场景语义占用沿 ±x、±y、z 轴投影为多视角的语义-深度-颜色图，将体素信息压缩为紧凑的特征图；统一语义映射则借助 CLIP 文本编码器提取类别特征，再通过共享线性层降维，实现跨数据集的统一语义表达。在此基础上，目标导向的人-场景关联模块以帧级交叉注意力将方向指令与场景语义特征注入运动扩散模型，驱动指令感知的运动生成。

实验结果表明，SSOMotion 在移动与交互任务上均显著优于 DIMOS：目标距离更小、穿透更少，且用户研究在自然度、指令达成率等维度上获得一致偏好。尤为关键的是，双向三平面分解与语义降维将单样本场景感知及运动-场景关联的计算量从 **20783 GFLOPs 骤降至 0.49 GFLOPs**，降幅达四个数量级。消融实验进一步证实，去除空间语义信息后模型无法正确识别坐下区域，验证了语义信息对行为理解的决定性作用。

当前方法仍存在两点局限：其一，基于网格的语义占用表示与原始场景网格存在偏差，可能导致约 4 cm 的轻微碰撞或悬空；其二，框架仅支持单人运动合成，尚未扩展至多人交互或群体运动生成场景。

### 问题背景：3D 场景中的人体运动合成

生成在复杂 3D 室内场景中自然移动并与物体交互的人体运动序列，是计算机视觉与图形学中的一个基础且具有挑战性的问题。该任务的核心难点在于，合成的人体不仅需要保持运动本身的物理合理性与自然度，还必须与周围 3D 环境的几何约束和语义属性保持精确一致——例如，人物应走到沙发前而非穿入其中，坐下时应选择可坐的表面而非桌子边缘。

近年来，基于扩散模型（Diffusion Models）的运动生成方法在无条件及文本条件的人体运动合成上取得了显著进展。然而，当将这些方法扩展到 3D 场景条件下时，一个关键瓶颈浮现：**如何高效且准确地让模型理解 3D 场景的“可供性”（affordance）**——即场景中哪些区域是可通行的、哪些物体是可交互的、以及以何种方式交互。

### 现有方法的缺口

现有场景感知运动合成方法主要存在两个结构性缺陷：

**1. 重结构、轻语义的场景表征**

以 **DIMOS**（Zhao et al., ICCV 2023）为代表的现有方法，通常采用基于网格的占位传感器（occupancy grid）或点云来编码场景信息。这类表征仅捕获了场景的几何结构（如障碍物的空间位置），却完全忽略了**语义信息**——模型知道“这里有一个立方体形状的物体”，但不知道“这是一个沙发”还是“一个书架”。缺乏语义理解直接导致模型无法正确推理场景可供性：它无法区分可坐的表面与不可坐的表面，无法识别可交互物体与背景障碍物。实验证据表明，当移除空间语义信息后，模型无法正确识别坐下区域（Figure 10），这直接验证了语义信息对行为理解的关键作用。

**2. 高维语义特征带来的计算冗余**

若试图将语义信息引入场景表征，直接使用高维语义特征（如 CLIP 文本嵌入的原始维度）会带来巨大的计算开销。在不做任何优化的前提下，单样本的场景感知与运动-场景关联计算量可达 **20783 GFLOPs**（Table 3），这使得实时或大规模应用变得不切实际。此外，不同数据集（如 PROX、Replica、HUMANISE）往往使用各自独立的语义标签体系，缺乏统一的语义空间，导致模型难以跨数据集泛化。

### 本文动机与核心思路

针对上述缺口，本文的核心动机是：**设计一种同时编码几何结构与语义信息的轻量级统一场景表征，使运动合成模型能够以极低的计算成本理解场景可供性，并支持跨数据集的语义一致性。**

为实现这一目标，本文提出了 **SSOMotion** 框架，其核心设计包含两个相互配合的技术组件：

- **统一场景语义占用（Scene Semantic Occupancy, SSO）与双向三平面分解**：在人体周围构建体素化的场景语义占用网格，同时记录每个体素的语义标签、深度和颜色信息。随后，通过沿 ±x、±y、z 五个方向进行正交投影，将三维体素信息压缩为多视角的二维 RGB-DS（颜色-深度-语义）特征图。这一分解将场景理解的计算量从体素级的三维运算降至二维卷积可处理的范围。

- **CLIP 文本编码 + 共享线性降维的统一语义映射**：利用 CLIP 文本编码器提取各语义类别的文本特征，再通过一个共享的线性层将高维特征降维至统一的低维语义空间。这不仅解决了不同数据集语义标签不兼容的问题，还通过降维大幅削减了后续计算开销——结合双向三平面分解后，单样本计算量从 20783 GFLOPs 骤降至 **0.49 GFLOPs**（Table 3），降幅超过四个数量级。

基于这一轻量级统一场景表征，SSOMotion 进一步通过**目标导向的人-场景关联模块**，以帧级交叉注意力机制将方向指令提示与场景语义特征共同注入扩散模型的运动控制分支，实现指令感知的 3D 场景人体运动合成。

## 核心方法与创新机理

SSOMotion 的核心创新在于将**场景语义占用（Scene Semantic Occupancy, SSO）**引入 3D 场景人体运动合成，并通过三项关键设计（changed slots）解决了现有方法的两大瓶颈：**（1）仅关注空间结构而忽略语义信息，导致无法正确理解场景可供性；（2）高维语义特征提取存在大量冗余计算**。

### 创新一：统一场景语义占用与双向三平面分解

**问题**：现有方法（如 DIMOS, Zhao et al., ICCV 2023）采用基于网格的占位传感器或点云表示场景，仅捕获几何结构信息，缺乏对“椅子可坐、床可躺”等语义可供性的理解。

**方案**：SSOMotion 提出将场景语义占用（SSO）作为统一表示，同时编码语义、几何和颜色信息。为消除高维体素带来的计算冗余，进一步引入**双向三平面分解**：将体素化场景沿 ±x、±y、z 轴投影，生成多视角的语义-深度-颜色图（Figure 2(a)）。这一分解将 3D 体素信息压缩为轻量级 2D 特征图，在保留细粒度空间语义的同时大幅降低计算量。

**关键因果机制**：三平面分解的本质是将 $O(N^3)$ 的体素查询转化为 $O(N^2)$ 的投影图查询，使场景感知的计算成本从 20783 GFLOPs 骤降至 0.49 GFLOPs（Table 3），降幅超过四个数量级。这是 SSOMotion 能够实现高效推理的基础。

### 创新二：跨数据集统一语义映射

**问题**：不同数据集的语义标签体系互不兼容（如 PROX 与 Replica 的类别定义不同），传统独热编码无法跨数据集泛化，且高维语义特征（如 CLIP 的 512 维嵌入）直接使用会引入额外计算负担。

**方案**：SSOMotion 使用 **CLIP 文本编码器** 提取类别名称的语义特征，再通过一个**共享线性层**将高维嵌入降维到统一的低维语义空间（Figure 2(b)）。降维后的特征被散射回语义图中，形成跨数据集一致的轻量语义表示。

**关键因果机制**：CLIP 编码器提供了语言监督下的通用语义先验，共享线性层则强制不同数据集的语义特征映射到同一空间。这使得模型在 PROX 上训练的语义理解能力可直接迁移到 Replica 等新场景，无需重新训练语义分支。消融实验（Figure 10）证实，移除空间语义信息后，模型无法正确识别可交互区域（如坐下位置），直接验证了统一语义映射对行为理解的决定性作用。

### 创新三：目标导向的人-场景关联建模

**问题**：现有方法将场景特征仅用于碰撞避免，缺乏指令（如“走向椅子并坐下”）与场景语义的显式关联建模。

**方案**：SSOMotion 设计了**目标导向的人-场景关联模块**（Figure 3(b)），通过帧级交叉注意力机制实现双重关联：
- **目标-运动关联**（Eq. 8）：将归一化的方向提示 $\mathbf{d}_n$ 作为查询，与运动特征进行交叉注意力，使运动生成受目标方向约束；
- **场景-运动关联**（Eq. 9）：将场景融合特征 $f_{scene}$（拼接语义、几何、纹理，Eq. 6）作为键值对，与运动查询进行交叉注意力，使每一步运动都感知周围场景的语义结构。

关联后的特征通过**零初始化线性层**注入主扩散模型的运动控制分支，确保训练初期不破坏预训练运动先验。

**关键因果机制**：双重交叉注意力形成了一个“指令→目标方向→场景语义→运动生成”的因果链。方向提示约束运动的宏观走向，场景语义约束微观的落脚点和交互姿态。Table 1 和 Table 2 显示，该设计使移动任务的目标距离低至 0.02m，交互任务的穿透均值控制在 1.83（坐）和 5.74（躺），显著优于仅依赖结构特征的基线方法。

### 创新总结

三项创新形成闭环：**SSO 三平面分解**提供轻量级多模态场景表示，**统一语义映射**赋予其跨数据集泛化能力，**目标导向关联**则将语义信息有效注入运动生成过程。这一组合以极低的计算代价（0.49 GFLOPs/样本）实现了对场景可供性的细粒度理解，是 SSOMotion 在移动精度和交互自然度上超越 DIMOS 的根本原因。

SSOMotion 的整体框架围绕三个核心设计展开：**统一场景语义占用（SSO）感知**、**目标导向的人-场景关联建模**，以及**基于扩散模型的运动控制生成**。系统输入为历史人体运动序列与自然语言指令，输出为未来帧的 SMPL-X 参数（全局平移、全局朝向、关节旋转）。

### 流水线概览

如 Figure 1 所示，框架首先将指令通过人体先验知识转化为目标姿态或位置（Hassan et al., 2021b; Zhao et al., 2022）。随后，以人体为中心部署网格传感器，在体中心坐标系下感知局部场景的语义、几何与颜色信息，构建紧凑的场景语义占用表示。该占用体素通过**双向三平面分解**（沿 ±x、±y、z 五个方向投影）被压缩为多视角的语义-深度-颜色特征图，同时利用 CLIP 文本编码器与共享线性层将不同数据集的语义标签映射到统一的低维特征空间（Figure 2）。

在运动生成端，系统采用基于扩散模型的架构：历史运动帧经加噪后，与时间步、掩码关节、动作编码共同构成动作意图提示（Figure 3a）。目标导向的人-场景关联模块（Figure 3b）通过帧级交叉注意力机制，分别建模方向提示与运动特征的关联（Eq. 8）以及场景特征与运动特征的关联（Eq. 9），最终将融合后的控制信号通过零初始化线性层注入主扩散模型，引导去噪过程生成符合指令且场景兼容的运动序列。

### 模块关系与数据流

1. **场景感知模块**：接收当前人体位姿，在体中心坐标系采样网格传感器，经坐标变换（Eq. 4）获取世界坐标系下的语义、深度、颜色信息，通过高斯深度激活（Eq. 5）突出近处几何结构，最终拼接为统一场景特征 $f_{scene}$（Eq. 6）。

2. **运动控制模块**：以加噪运动序列 $x_t$、扩散时间步 $t$、掩码关节信息及动作编码为输入，在 Transformer 解码器层中插入两组交叉注意力——一组以方向提示为键值对生成目标导向运动特征 $f_{mot}^g$，另一组以场景特征为键值对生成场景感知运动特征 $f_{mot}^{gs}$。

3. **损失监督**：训练时直接预测原始运动 $\hat{x}_0^\phi$（Eq. 2），总损失由关节旋转重建损失（Eq. 11）、平移重建损失（Eq. 12）和速度损失（Eq. 14）加权求和构成（Eq. 10），其中速度损失从第二帧开始计算以保证运动平滑性。

### 关键设计决策

- **双向三平面分解**替代直接处理三维体素，将单样本场景感知与运动-场景关联的总计算量从 20783 GFLOPs 压缩至 0.49 GFLOPs（Table 3），这是框架实现高效推理的瓶颈突破点。
- **统一语义映射**通过 CLIP 文本编码器提取类别特征后经共享线性层降维，解决了不同数据集语义标签空间不兼容的问题，使模型能够在 HUMANISE、PROX、Replica 等多数据集上联合训练。
- **长序列合成**采用滑动窗口策略（历史帧 $H$ 与生成帧 $S$ 重叠），以历史运动约束保证帧间过渡的连续性。

### 问题形式化与扩散基础

SSOMotion 将指令感知的 3D 场景人体运动合成建模为一个条件生成问题。人体姿态采用 SMPL-X 参数化表示，主要包含全局平移 $\tau \in \mathbb{R}^3$、全局朝向 $\gamma \in \mathbb{R}^6$ 以及身体关节旋转 $\theta \in \mathbb{R}^{32 \times 6}$。场景则以紧凑的场景语义占用（Scene Semantic Occupancy, SSO）表示，记为 $\mathcal{S} \in \mathbb{R}^{N \times 4}$，其中每个体素存储语义标签和占用状态。

运动生成基于扩散模型框架。前向扩散过程逐步向原始运动 $x_0$ 添加高斯噪声：

$$q(x_t | x_{t-1}) = \mathcal{N}(\sqrt{\alpha_t} x_{t-1}, (1-\alpha_t) \mathbf{I}) \quad \text{(Eq. 1)}$$

其中 $\alpha_t$ 为噪声调度参数。网络 $\phi$ 从噪声运动 $x_t$ 直接预测原始运动 $\hat{x}_0^\phi$：

$$\hat{x}_0^\phi = \phi(x_t, t, c) \quad \text{(Eq. 2)}$$

$c$ 为条件信号（场景特征与方向提示），$t$ 为扩散时间步。推理时的逆向去噪步骤为：

$$P(x_{t-1}|x_t) = \mathcal{N}(\mu_t(\hat{x}_0^\phi(x_t), x_t), \tilde{\beta}_t \mathbf{I}) \quad \text{(Eq. 3)}$$

### 场景语义占用（SSO）感知管线

SSO 感知管线是本文的核心创新，其目标是以极低计算成本提取富含语义-几何-纹理信息的场景表征。该管线包含三个紧密耦合的子模块：

**（1）双向三平面分解**

以人体为中心放置网格传感器，将传感器坐标变换到世界坐标系：

$$\mathcal{T}_g = R(\theta_z^{\mathcal{I}}) \mathcal{T}_l + \tau^{\mathcal{I}} \quad \text{(Eq. 4)}$$

其中 $\mathcal{T}_l$ 为体中心传感器坐标，$R(\theta_z^{\mathcal{I}})$ 为人体绕 z 轴旋转矩阵，$\tau^{\mathcal{I}}$ 为人体平移向量。随后沿 $\pm x$、$\pm y$、$z$ 五个方向对体素化场景语义占用进行投影，生成多视角的语义图、深度图和颜色图。这一分解将三维体素信息压缩为二维特征图，大幅降低了后续处理的计算量。

**（2）深度高斯激活**

对深度图应用高斯核激活，以突出近处物体的几何信息：

$$\mathcal{O}_{ij}^{da} = \frac{1}{\sigma \sqrt{2\pi}} e^{-(\mathcal{O}_{ij}^{d})^2/(2\sigma^2)} \quad \text{(Eq. 5)}$$

其中 $\sigma$ 控制激活的敏感范围，$\mathcal{O}_{ij}^{d}$ 为像素 $(i,j)$ 处的深度值。

**（3）统一语义映射**

为解决不同数据集中语义标签不一致的问题，采用 CLIP 文本编码器提取类别名称的语义特征，再通过一个共享线性层将高维 CLIP 特征降维至统一的低维语义空间。降维后的语义特征被散射回语义图中对应类别区域。最终，场景特征由三部分拼接而成：

$$f_{scene} = f_{sem} \oplus f_{geo} \oplus f_{tex} \quad \text{(Eq. 6)}$$

其中 $f_{sem}$ 为统一语义特征，$f_{geo}$ 为深度几何特征，$f_{tex}$ 为颜色纹理特征。

### 目标导向的人-场景关联与运动控制

运动控制器通过帧级交叉注意力机制，将方向提示与场景特征注入扩散模型的去噪过程。

**方向提示归一化**：将目标方向向量 $\mathbf{d}$ 的范数裁剪至 $[0,1]$ 范围：

$$\mathbf{d}_n = \frac{\min(||\mathbf{d}||, 1) + \epsilon}{||\mathbf{d}|| + \epsilon} \mathbf{d} \quad \text{(Eq. 7)}$$

**目标导向的人-运动交叉注意力**：以运动特征作为查询 $Q_{d,i}$，方向提示作为键 $K_{d,i}$ 和值 $V_{d,i}$，计算交叉注意力并融合：

$$f_{mot}^{g} = \mathrm{concat}(\mathrm{softmax}(\frac{Q_{d,i} K_{d,i}^{T}}{\sqrt{d_d}}) V_{d,i}) W_{o,d} \quad \text{(Eq. 8)}$$

**目标导向的人-场景交叉注意力**：进一步以运动特征为查询 $Q_{s,j}$，场景特征为键 $K_{s,j}$ 和值 $V_{s,j}$，建模人-场景关联：

$$f_{mot}^{gs} = \underset{j}{\mathrm{concat}}(\mathrm{softmax}(\frac{Q_{s,j} K_{s,j}^{T}}{\sqrt{d_s}}) V_{s,j}) W_{o,s} \quad \text{(Eq. 9)}$$

融合后的特征 $f_{mot}^{gs}$ 通过零初始化线性层注入主扩散模型的控制分支，确保训练初期控制信号不干扰基础运动生成能力。

### 训练损失

总损失由旋转重建、平移重建和速度一致性三部分构成：

$$\mathcal{L}_{total} = \mathcal{L}_{rot} + \mathcal{L}_{trans} + \mathcal{L}_{vel} \quad \text{(Eq. 10)}$$

$$\mathcal{L}_{rot} = M \cdot ||\hat{x}_0^{rot} - x_0^{rot}||^2 \quad \text{(Eq. 11)}$$

$$\mathcal{L}_{trans} = M \cdot ||\hat{x}_0^{trans} - x_0^{trans}||^2 \quad \text{(Eq. 12)}$$

其中 $M$ 为掩码矩阵，用于仅对有效关节计算损失。速度损失基于连续帧关节位置差计算：

$$v = ||\mathcal{I}[1:S] - \mathcal{I}[0:S-1]||_2 \times \nu \quad \text{(Eq. 13)}$$

$$\mathcal{L}_{vel} = M_{1:} \cdot ||\hat{v} - v||^2 \quad \text{(Eq. 14)}$$

$\nu$ 为帧率缩放因子，$M_{1:}$ 从第二帧开始掩码以对齐速度计算的时间偏移。

![[assets/figures/papers/paper_list_l1695_SSOMotion_HumanMotion_Synthesis_in_3D_Scenes_via_Unified_Scene_Semantic/figures/002_Figure_2.jpg]]
*Figure 2: Pipeline of the Scene Semantic Occupancy perception (SSO). (a) presents the Bi-directional Tri-plane Decomposition of the SSO, where scene color, semantics and depth are perceived in body-centered coordinate. In (b), we map the semantic labels into a unified semantic space via the CLIP textual encoder and a shared linear layer. Then, the unified low-dimension semantic features will be scattered into the semantic map. (c) indicates the normalization functions for distance and color space*

## 实验与关键发现

### 核心定量结果

SSOMotion 在移动和交互两类任务上均展现出相对于基线方法 **DIMOS** (Zhao et al., ICCV 2023) 的显著优势。

**移动任务** (Table 1)：在由 ShapeNet 家具构成的杂乱场景中，SSOMotion 的平均目标距离仅 0.02 m，移动穿透率 0.95，平均到达时间 3.60 s。与 DIMOS 相比，SSOMotion 在目标达成精度与路径安全性的权衡上取得了更优的平衡——更低的穿透率意味着合成的人体运动更少穿透场景物体，而更短的目标距离则表明动作对指令的响应更精确。

**交互任务** (Table 2)：坐下动作的穿透均值仅 1.83、最大穿透值 6.78，躺下动作的穿透均值 5.74、最大穿透值 40.48。值得注意的是，交互任务的穿透指标绝对值高于移动任务，这反映了坐下/躺下等行为天然需要与物体表面发生接触，因此精确建模场景语义可供性（affordance）的难度更大。SSOMotion 在此类任务上的穿透控制能力，直接受益于其统一场景语义占用（SSO）对可交互区域的细粒度语义理解。

**运动预测任务** (Table 4)：在 HUMANISE 数据集上，SSOMotion 的 MPJPE 为 0.095 m，MPVPE 为 0.118 m，目标距离误差仅 0.045 m，验证了该方法在给定历史运动与目标指令条件下的未来运动预测能力。

### 计算效率与消融分析

SSOMotion 的核心效率突破体现在场景感知与运动-场景关联两个阶段的计算量压缩。消融实验 (Table 3) 揭示了一条清晰的因果链：

![[assets/figures/papers/paper_list_l1695_SSOMotion_HumanMotion_Synthesis_in_3D_Scenes_via_Unified_Scene_Semantic/figures/012_Table_3.jpg]]
*Table 3: Computational Cost of the Scene Comprehension and Motion Scene Correlation for only 1 sample*

1. **双向三平面分解**：将体素化的场景语义占用沿 ±x、±y、z 轴投影为多视角的特征图，避免了在密集 3D 体素空间中进行高维卷积操作。
2. **统一语义降维**：使用 CLIP 文本编码器提取类别特征后，通过共享线性层将高维语义嵌入压缩至低维统一空间，消除了不同数据集间语义维度不一致带来的冗余。

两者叠加使单样本计算量从 20783 GFLOPs 骤降至 0.49 GFLOPs，降幅超过四个数量级。这一结果并非简单的工程优化，而是源于“双向三平面分解 + 统一语义映射”的组合设计：前者解决了空间维度的冗余，后者解决了语义维度的冗余。

语义信息的必要性在定性消融 (Figure 10) 中得到进一步验证：移除空间语义信息后，模型无法正确识别坐下区域，合成的人体倾向于在不可坐的物体表面执行坐下动作。这直接证明了 SSO 提供的语义可供性信号是交互行为理解的关键因果变量，而非仅靠几何碰撞避免即可替代。

![[assets/figures/papers/paper_list_l1695_SSOMotion_HumanMotion_Synthesis_in_3D_Scenes_via_Unified_Scene_Semantic/figures/014_Figure_10.jpg]]
*Figure 10: Visual comparison of the proposed method with-/without spatial semantic information*

### 可视化与定性分析

在移动合成可视化对比 (Figure 4) 中，DIMOS 生成的路径存在明显穿透家具的现象，而 SSOMotion 的路径更贴近场景中的可行走区域。坐下动作对比 (Figure 5) 显示 DIMOS 合成的人体常出现悬空或穿透椅面的情况，SSOMotion 则能准确定位椅面并生成自然的坐下姿态。躺下动作 (Figure 6) 的对比进一步印证了这一趋势：SSOMotion 能正确识别床/沙发等可躺卧表面，而 DIMOS 的合成结果存在人体与场景物体严重穿插的问题。

![[assets/figures/papers/paper_list_l1695_SSOMotion_HumanMotion_Synthesis_in_3D_Scenes_via_Unified_Scene_Semantic/figures/007_Figure_4.jpg]]
*Figure 4: Visual comparison of locomotion synthesis between DIMOS and the proposed method*

![[assets/figures/papers/paper_list_l1695_SSOMotion_HumanMotion_Synthesis_in_3D_Scenes_via_Unified_Scene_Semantic/figures/008_Figure_5.jpg]]
*Figure 5: Visual results given by DIMOS and the proposed method for sitting action*

![[assets/figures/papers/paper_list_l1695_SSOMotion_HumanMotion_Synthesis_in_3D_Scenes_via_Unified_Scene_Semantic/figures/004_Figure_6.jpg]]
*Figure 6: Visualization of lying motions synthesized by DI-MOS and the proposed method*

在 PROX (Figure 8) 和 Replica (Figure 9) 数据集上的跨场景泛化结果表明，SSOMotion 的统一语义映射机制使其能够在不同场景布局和语义标签体系下保持稳定的合成质量，无需针对特定数据集重新训练语义嵌入层。

### 失败模式与边界条件

尽管 SSOMotion 在主要指标上表现优异，但其基于网格的场景语义占用表示引入了与原始场景网格的偏差。这一偏差导致合成的人体运动可能出现约 4 cm 量级的轻微碰撞和悬空现象。该问题的根源在于体素化过程本身的信息损失——网格到占用的离散化不可避免地丢失了细粒度的表面几何细节。

此外，当前框架仅针对单人运动合成设计，未扩展到多人/群体运动生成场景。在多人场景中，人体间碰撞避免、社交距离维持等约束需要额外的交互建模模块，而现有的目标导向交叉注意力机制仅建模了单人与场景之间的关联。

### 用户研究

用户研究 (Figure 7) 从自然度、指令达成率、场景合理性等多个维度对竞争方法进行了主观评分，SSOMotion 在所有维度上均取得最高分，与定量指标的趋势一致。

## 定位与知识库关联

### 1. 与基线方法的关系与差异

SSOMotion 的核心对比基线是 **DIMOS** (Zhao et al., ICCV 2023)，该方法代表了当前3D场景人体运动合成的主流范式。两者在以下关键维度上存在本质差异：

**场景表示的代际跃迁。** DIMOS 等基线方法主要依赖基于网格的占位传感器或点云，仅提取场景的空间结构信息（如障碍物位置），而完全忽略了语义层面的可供性（affordance）——例如，一个平面区域是“地板”还是“床”对“坐下”动作的选择至关重要。SSOMotion 提出的统一场景语义占用（SSO）将语义、几何和颜色信息同时编码，并通过双向三平面分解将体素信息压缩为多视角的轻量级特征图，从根本上弥补了语义缺失的短板。

**语义嵌入的统一性。** 现有方法通常采用数据集相关的独热编码或缺乏跨场景泛化能力的语义表示，导致模型在不同数据集间迁移时语义空间断裂。SSOMotion 引入 CLIP 文本编码器提取类别特征，并通过共享线性层实现降维与跨数据集统一映射，使不同来源的语义标签（如 PROX 和 Replica 的家具类别）收敛到同一低维空间，这是实现跨场景泛化的关键因果机制。

**运动-场景关联的精细化。** DIMOS 等基线仅利用结构特征进行碰撞避免，是一种被动的约束策略。SSOMotion 则通过目标导向的帧级交叉注意力机制，将指令方向提示与场景语义特征共同注入运动控制分支，使模型主动理解“在哪里执行什么动作”，而非仅仅“避开障碍物”。

### 2. 适用边界与约束条件

**输入假设。** SSOMotion 假设场景以语义占用形式提供，且指令可转化为目标姿态或位置（通过人体先验分布）。对于缺乏语义标注的原始点云或网格场景，需要额外的语义分割预处理。指令的翻译依赖于预定义的动作类别和目标位置，尚未支持自由形式的自然语言指令。

**运动表示。** 模型采用 SMPL-X 参数化人体模型，输出全局平移、全局朝向和关节旋转。这意味着生成的运动质量受限于 SMPL-X 的表达能力，对于与物体精细交互（如手指操作）的场景不适用。

**场景表示偏差。** 由于采用基于网格的场景语义占用表示，与原始场景网格存在离散化偏差，可能导致轻微碰撞和悬空（约4cm）。这一偏差在需要高精度接触的任务（如倚靠、抓握）中可能更为显著。

**单人假设。** 当前框架仅针对单人运动合成设计，未扩展到多人/群体运动生成场景。多人场景中的社交交互、空间协调等问题不在当前方法的处理范围内。

### 3. 已知局限与失效模式

**网格偏差导致的穿透与浮空。** 消融实验和定性分析表明，去除空间语义信息后，模型无法正确识别坐下区域（Figure 10），但即使保留语义信息，基于网格的表示仍与真实几何存在偏差，导致约4cm量级的穿透和悬空。这是方法固有的表示精度瓶颈，而非训练不足。

**长序列合成的误差累积。** 模型采用滑动窗口策略生成长序列运动，历史帧与未来帧之间有 H 帧重叠以保证连续性。然而，随着序列增长，预测误差可能逐步累积，导致后期动作偏离预期目标。论文未提供超长序列（如数分钟）的定量评估。

**对场景语义质量的依赖。** 统一语义映射依赖 CLIP 文本编码器提取类别特征，若场景中存在 CLIP 训练分布外的物体类别（如特殊医疗器械、工业设备），语义嵌入质量可能下降，进而影响动作合成的合理性。

### 4. 开放问题与后续方向

**如何进一步减小网格偏差？** 当前约4cm的穿透/悬空偏差源于体素化的固有精度损失。可能的改进方向包括：引入自适应分辨率的多尺度体素表示、在推理阶段结合隐式神经表示进行精细碰撞校正，或采用混合表示（体素+网格）以保留关键接触区域的几何精度。

**如何扩展至多人/群体运动生成？** 多人场景引入了个体间的空间协调、社交规范（如个人空间、对话朝向）和时序同步等新挑战。将 SSO 表示扩展为多人共享的场景语义场，并引入个体间的注意力交互建模，是自然的扩展方向。但如何保持计算效率（当前单样本仅0.49 GFLOPs）是核心约束。

**如何支持更自由的指令形式？** 当前指令需转化为目标姿态或位置，限制了交互的自然性。将指令端扩展为自然语言输入，并建立语言-场景-动作的联合推理，是提升系统实用性的关键方向。这需要在统一语义空间的基础上，进一步建立语言描述与场景可供性的细粒度对齐。

**实时性与交互式应用。** 虽然双向三平面分解将场景感知计算量从20783 GFLOPs 降至0.49 GFLOPs（Table 3），但整体推理延迟是否满足实时交互需求（如VR/AR场景中的即时响应）仍需进一步验证和优化。

## 原文 PDF

![[paperPDFs/arxiv_2025/SSOMotion_HumanMotion_Synthesis_in_3D_Scenes_via_Unified_Scene_Semantic_Occupancy.pdf]]
