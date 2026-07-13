---
title: "TexFusion: Synthesizing 3D Textures with Text-Guided Image Diffusion Models"
type: paper
paper_level: A
venue: ICCV
year: 2023
pdf_ref: paperPDFs/ICCV_2023/TexFusion_Synthesizing_3D_Textures_with_Text_Guided_Image_Diffusion_Models.pdf
project_link: https://research.nvidia.com/labs/toronto-ai/texfusion/
code_link: null
aliases:
- TTD
- TexFusion
tags:
- ICCV_2023
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
core_operator: "使用顺序交错多视图采样器（SIMS）在扩散去噪过程中交错聚合多视图潜在纹理，替代了SDS的蒸馏优化和纯自回归采样。"
primary_logic: "在扩散模型的每个去噪步骤之间交错执行视图聚合和噪声对齐，可以在所有视图上同步生成3D一致的纹理，这比完全去噪后聚合或顺序自回归采样更好地维持了全局一致性，并避免了SDS导致的过饱和与缓慢优化。"
claims:
- "TexFusion在用户研究中在自然颜色（75.58% vs 24.42%）、更少伪影（68.60% vs 31.40%）和提示对齐（56.98% vs 43.02%）方面均显著优于TEXTure。"
- "TexFusion的FID得分为59.78，远低于TEXTure的79.47，表明生成纹理与真实图像分布更接近。"
- "TexFusion采样时间为2.2-6.2分钟，比SDS方法（stable-dreamfusion 39分钟，Latent-Painter 22分钟）快10-18倍，且质量更高。"
- "TexFusion的SIMS通过在每个去噪步交错聚合不同视图，避免了TEXTure中早期视图错误导致的不可调和伪影（如图3所示）。"
---

# TexFusion: Synthesizing 3D Textures with Text-Guided Image Diffusion Models

> [!tip] 核心洞察
> 在扩散模型的每个去噪步骤之间交错执行视图聚合和噪声对齐，可以在所有视图上同步生成3D一致的纹理，这比完全去噪后聚合或顺序自回归采样更好地维持了全局一致性，并避免了SDS导致的过饱和与缓慢优化。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | TexFusion: 基于文本引导图像扩散模型的3D纹理合成 |
| 英文题名 | TexFusion: Synthesizing 3D Textures with Text-Guided Image Diffusion Models |
| 会议/期刊 | ICCV 2023 |
| Links | [paper](https://arxiv.org/abs/2310.13772) · [Project](https://research.nvidia.com/labs/toronto-ai/texfusion/) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction |
| Method | TexFusion (Texture Diffusion) |
| Dataset | 自建35个网格×约86提示组合的纹理生成, 用户研究（Amazon Mechanical Turk）, 用户研究 |

> [!tip] 效果简介
> - 自建35个网格×约86提示组合的纹理生成 上，FID (相对SD2-depth生成的图像) 为 59.78，对比 79.47 (TEXTure)，变化 -19.69。
> - 用户研究（Amazon Mechanical Turk） 上，自然色彩偏好率 为 75.58%，对比 24.42% (TEXTure)，变化 +51.16%。
> - 用户研究 上，较少伪影偏好率 为 68.60%，对比 31.40% (TEXTure)，变化 +37.20%。

## 概要

**问题瓶颈：** 现有基于Score Distillation Sampling（SDS）的3D纹理生成方法（如stable-dreamfusion、Latent-Painter）需要极高的分类器自由引导权重（通常>100），导致纹理过饱和、色彩失真且多样性低，单样本生成耗时约30分钟。另一方面，自回归视图生成方法TEXTure因按视图顺序逐步采样，早期视图的错误会不可调和地传播至后续视图，造成严重的视图不一致伪影（Figure 3）。

**核心方法：** TexFusion提出**顺序交错多视图采样器（Sequential Interlaced Multiview Sampler, SIMS）**，在扩散模型的每个去噪步骤之间交错执行多视图渲染、聚合与去噪。具体而言，SIMS将共享的潜在纹理图渲染至不同相机视图，经扩散模型去噪后，依据屏幕空间导数测量的视图质量，将最优视角的纹理区域投影回共享潜在纹理图，从而在所有视图上同步生成3D一致的纹理。该方法以粗到细两阶段策略运行：粗阶段使用全景相机生成低分辨率纹理，细阶段使用窄视角相机进行高分辨率细化。

**关键结论：**

- **质量显著提升：** 在用户研究中，TexFusion在自然色彩（75.58% vs 24.42%）、更少伪影（68.60% vs 31.40%）和提示对齐度（56.98% vs 43.02%）三个维度上均显著优于TEXTure（Table 1）。FID得分（59.78）远低于TEXTure（79.47），表明生成纹理更接近扩散模型训练数据的分布。
- **速度数量级提升：** TexFusion的单样本生成时间仅需2.2–6.2分钟（取决于相机数量），比stable-dreamfusion（39分钟）快约18倍，比Latent-Painter（22分钟）快约10倍（Table 2）。
- **方法定位：** TexFusion完全避免了SDS蒸馏优化，转而利用扩散模型的标准采样过程，通过SIMS在去噪轨迹中实现3D一致性聚合。该方法可灵活替换扩散骨干（如集成ControlNet进行更精确的几何控制），并支持非随机DDIM采样以增强材质细节。

**局限与开放问题：** 当前方法生成的纹理仅为漫反射颜色，未建模光照与PBR材质属性；纹理分辨率受限于潜在扩散模型的潜在空间尺寸；极端几何形状需要定制相机配置。未来方向包括集成更快的扩散采样器以实现实时生成，以及扩展至PBR材质合成。

### 问题背景：文本驱动的3D纹理合成

将文本描述自动转化为覆盖在给定三维网格上的高质量纹理，是连接语言与视觉世界的关键任务。这一能力对游戏开发、影视制作和虚拟现实内容创作具有直接价值——它允许创作者通过自然语言快速为任意形状的物体赋予外观，而无需手工绘制复杂的UV贴图。然而，实现这一目标面临双重挑战：纹理必须在所有可能的观察角度下保持视觉一致，同时又要忠实反映文本提示中的语义和风格。

近年来，文本到图像扩散模型（如Stable Diffusion）在二维图像生成领域取得了突破性进展，能够根据任意文本描述合成高度逼真且多样化的图像。这自然引出一个问题：能否将这种强大的二维生成能力“迁移”到三维表面，从而为任意网格生成纹理？

### 现有方法的两条路径及其瓶颈

当前基于扩散模型的纹理合成方法主要沿两条技术路线发展，但各自存在根本性局限。

**路径一：基于分数蒸馏采样（SDS）的优化方法。** 这类方法以DreamFusion为代表，通过将扩散模型作为可微分的“批评者”，在参数空间（如神经辐射场或纹理图）中进行迭代优化。在纹理合成领域，**Latent-Painter**（Metzer et al., 2022）和社区实现的**stable-dreamfusion**（Tang et al., 2023）均采用此范式。

SDS方法的核心瓶颈在于：为了获得可接受的纹理质量，通常需要极高的分类器自由引导权重（classifier-free guidance weight，常超过100）。这一数值远超标准图像生成中常用的7.5-15范围，导致两个严重后果：**纹理过饱和**——色彩浓重不自然，缺乏细腻的色调层次；**多样性低**——不同随机种子生成的纹理高度相似，丧失了扩散模型本应具备的创造性。此外，SDS优化过程缓慢，典型单样本生成时间在22-39分钟之间（Table 2），难以满足实际应用中的迭代需求。

**路径二：自回归视图采样方法。** 以**TEXTure**（Richardson et al., 2023）为代表的并发工作采用截然不同的策略：从一个初始视图开始，逐步将纹理“绘制”到网格表面，每个新视图的生成以前序视图的已有纹理为条件进行修补。

这种顺序生成模式引入了一个不可调和的矛盾——**早期视图的错误无法被后续视图纠正**。如Figure 3所示，当第一个视角下生成的纹理区域在几何上并不正确（例如，一个在正面视角看起来自然的图案，从侧面观察时却与网格表面严重错位），后续视图的去噪过程会将这些错误“固化”到纹理中，而非修复它们。这是因为自回归采样缺乏全局协调机制：每个视图只看到局部的、已生成的纹理片段，无法感知整个三维表面的一致性需求。

### 核心洞察与本文动机

上述两条路径的失败揭示了同一个深层问题：**纹理合成本质上是一个多视图联合生成任务，而非单视图生成或逐视图修补的简单组合**。SDS方法试图通过全局优化来协调视图，但蒸馏过程本身扭曲了扩散模型的采样动态，导致质量退化；TEXTure的自回归采样保持了原生扩散质量，却因顺序依赖而牺牲了全局一致性。

TexFusion的核心洞察在于：**在扩散模型的每个去噪步骤之间交错执行视图聚合和噪声对齐，可以在所有视图上同步生成3D一致的纹理**。这一策略既避免了SDS的蒸馏优化带来的过饱和与缓慢收敛，又克服了纯自回归采样的视图间不可调和错误。直觉上，如果每个去噪步都能让所有视图“看到”彼此的生成进度并相互协调，那么整个纹理将从高噪声状态同步收敛到一个全局一致的低噪声结果——这比完全去噪后再聚合，或顺序逐个视图去噪，都更能维持跨视图的语义和几何一致性。

基于这一洞察，TexFusion提出了**顺序交错多视图采样器（Sequential Interlaced Multiview Sampler, SIMS）**，将多视图纹理生成重新表述为在共享潜在纹理图上进行的交错扩散过程，从根本上改变了纹理合成的问题建模方式。

## 核心方法与创新机理

TexFusion 的核心创新在于用**顺序交错多视图采样器（SIMS）** 替代了现有纹理合成方法中的两类主导范式：基于分数蒸馏采样（SDS）的优化和纯自回归的视图采样。这一替换在三个维度上带来了根本性变化：

**1. 生成机制：从“去噪后聚合”到“去噪中交错”**

现有方法要么在完全去噪后聚合视图（如 TEXTure 的自回归采样），要么通过 SDS 在全局范围内做蒸馏优化（如 Latent-Painter）。TexFusion 的 SIMS 在每个扩散去噪步之间交错执行视图渲染、聚合和去噪——将多视图去噪过程分解为条件概率的连乘积（式 3），使得所有视图的潜在纹理在去噪轨迹中同步演化。这避免了 TEXTure 中早期视图错误导致的不可调和伪影（Figure 3 所示），也绕过了 SDS 需要极高分类器自由引导权重（通常 >100）引发的纹理过饱和和多样性低的问题。

**2. 聚合策略：从简单混合到视图质量驱动**

TexFusion 引入基于屏幕空间导数（负雅可比行列式，式 6）的视图质量度量，在聚合时按 texel 选择最优视角的纹理区域进行更新，而非简单的重叠区域混合。这一设计确保高保真覆盖，同时抑制了低质量视角引入的模糊或错误。

**3. 纹理烘焙：从直接解码到神经颜色场蒸馏**

Latent-Painter 直接解码潜在纹理图会导致 UV 边界伪影（Figure 4 右所示）。TexFusion 改为将 SIMS 生成的多视图潜在图像解码为 RGB 后，再优化一个哈希编码+MLP 的神经颜色场，最终烘焙出高分辨率 RGB 纹理图。这一间接路径有效消除了不同视图间的解码不一致性。

上述三个 changed slots 共同构成了 TexFusion 的方法瓶颈突破：在保持 3D 一致性的前提下，将纹理生成时间从 22-39 分钟压缩至 2.2-6.2 分钟（Table 2），同时显著提升纹理的自然度和提示对齐度（Table 1）。

TexFusion 的整体流程以**文本提示**和**给定的3D网格几何体**为输入，输出一张与提示语义对齐且跨视图一致的UV参数化纹理图。其核心创新在于用**顺序交错多视图采样器（Sequential Interlaced Multiview Sampler, SIMS）**替代了此前方法中普遍采用的SDS蒸馏优化或纯自回归采样范式，从而在生成速度、色彩自然度和视图一致性上取得显著提升。

### 输入输出与模块划分

整个pipeline可划分为四个功能模块，它们以级联方式协作：

1.  **潜在纹理图初始化**
    流程起始于为SIMS准备一张高维高斯噪声的潜在纹理图 $\mathbf{z}_T$。该纹理图位于Stable Diffusion 2的潜在空间中，作为后续多视图扩散过程的共享状态载体。

2.  **顺序交错多视图采样器（SIMS）—— 核心模块**
    SIMS是整个框架的核心。它在50个DDIM去噪时间步中，对多个预设相机视图的潜在图像进行**交错渲染、聚合与去噪**。关键机制在于：每个去噪步之后，不同视图的扩散轨迹会通过一张共享的潜在纹理图进行聚合，而非在各视图独立去噪完成后再做融合。这确保了所有视图的纹理生成过程是同步协调的，从根本上避免了自回归方法（如TEXTure）中早期视图错误在后续视图中被放大且无法修正的问题（Figure 3）。SIMS最终输出一组3D一致的潜在图像。

3.  **多分辨率纹理生成（粗到细策略）**
    为平衡生成速度与细节质量，TexFusion采用两阶段策略：
    -   **粗阶段**：使用全景相机（大视场角）生成低分辨率纹理，快速建立全局语义和色彩布局。
    -   **细阶段**：切换至更窄视角的相机配置，对纹理进行高分辨率细化，同时避免因直接在高分辨率下生成而导致的内容漂移。

4.  **神经颜色场蒸馏与纹理烘焙**
    SIMS生成的潜在多视图图像首先通过Stable Diffusion的解码器转换为RGB图像。然而，直接解码会导致UV边界附近出现不一致的伪影（Figure 4）。为解决此问题，TexFusion引入一个中间表示——**神经颜色场**（一个基于哈希编码和MLP的网络）。该网络以多视图RGB图像为监督信号进行优化，学习一个视角一致的连续颜色场，最终从该颜色场中烘焙出高分辨率、无接缝的UV纹理图。

### 数据流与控制流

流程的控制流可概括为：

1.  **初始化**：生成噪声潜在纹理图 $\mathbf{z}_T$。
2.  **SIMS循环**（时间步 $i$ 从 $T$ 递减至 $1$）：
    -   **视图遍历**（视图 $n$ 从 $1$ 至 $N$）：
        -   **噪声对齐**：将共享潜在纹理图 $\mathbf{z}_i$ 中已被先前视图覆盖的区域添加噪声，使其噪声水平与当前扩散步 $i$ 匹配。
        -   **渲染**：将噪声对齐后的潜在纹理图通过可微光栅化渲染到当前相机 $C_n$ 视角，得到潜在图像 $\mathbf{x}_{i,n}'$。
        -   **去噪**：将 $\mathbf{x}_{i,n}'$ 与深度条件图一并送入扩散模型进行单步DDIM去噪，得到 $\mathbf{x}_{i-1,n}$。
        -   **聚合**：基于视图质量（由屏幕空间UV导数的负雅可比行列式衡量），将去噪后的图像最优区域反向投影并更新至共享潜在纹理图 $\mathbf{z}_{i-1,n}$。
3.  **后处理**：将SIMS输出的潜在图像解码为RGB，通过神经颜色场融合为最终纹理图。

该框架将扩散模型的生成能力与3D几何约束深度融合，通过在每个去噪步交错执行视图聚合，实现了生成速度与多视图一致性的联合优化。

### 3.1 扩散模型基础

TexFusion 建立在潜在扩散模型（Latent Diffusion Model）的去噪得分匹配框架之上。给定条件 $\mathbf{c}$，扩散模型的训练目标为最小化噪声预测误差：

$$ \mathbb{E}_{\mathbf{x}\sim p_{\mathrm{data}}, t\sim p_t, \epsilon\sim\mathcal{N}(\mathbf{0},I)}\left[\lVert\epsilon-\epsilon_\theta(\mathbf{x}_t;\mathbf{c},t)\rVert_2^2\right] \tag{1} $$

其中 $\mathbf{x}_t$ 为加噪后的数据，$\epsilon_\theta$ 为噪声预测网络，$t$ 为扩散时间步。

在推理阶段，采用 DDIM（Denoising Diffusion Implicit Models）反向采样逐步还原数据。单步 DDIM 采样公式为：

$$ \pmb{x}_{i-1} = \sqrt{\alpha_{i-1}}\left(\frac{\pmb{x}_i - \sqrt{1-\alpha_i}\pmb{\epsilon}_\theta^{(t_i)}(\pmb{x}_i)}{\sqrt{\alpha_i}}\right) + \sqrt{1-\alpha_{i-1}-\sigma_{t_i}^2}\cdot\pmb{\epsilon}_\theta^{(t_i)}(\pmb{x}_i) + \sigma_{t_i}\pmb{\epsilon}_{t_i} \tag{2} $$

其中 $\alpha_i$ 为噪声调度参数，$\sigma_{t_i}$ 控制采样的随机性（$\sigma_{t_i}=0$ 时为确定性采样），$\pmb{\epsilon}_{t_i} \sim \mathcal{N}(\mathbf{0}, \mathbf{I})$ 为标准高斯噪声。

---

### 3.2 顺序交错多视图采样器（SIMS）

SIMS 是 TexFusion 的核心创新模块，其关键洞察在于：**在扩散模型的每个去噪步骤之间交错执行视图聚合和噪声对齐**，从而在所有视图上同步生成 3D 一致的纹理。这与 TEXTure 的自回归视图采样和 SDS 的蒸馏优化形成根本性区别。

#### 3.2.1 联合分布分解

设 $\mathbf{z}_i$ 为扩散时间步 $t_i$ 时的共享潜在纹理图，$\{C_j\}_{j=1}^N$ 为 $N$ 个相机视图。SIMS 将多视图去噪过程的联合分布分解为条件概率的连乘积：

$$ p_\theta(\{\mathbf{x}_{i-1,j}\}_{j=1}^N|\mathbf{z}_i)=p_\theta(\mathbf{x}_{i-1,1}|\mathbf{z}_i)\times\prod_{n=2}^N p_\theta(\mathbf{x}_{i-1,n}|\{\mathbf{x}_{i-1,j}\}_{j=1}^{n-1},\mathbf{z}_i) \tag{3} $$

**变量含义**：
- $\mathbf{x}_{i-1,j}$：第 $j$ 个视图在时间步 $t_{i-1}$ 的去噪图像
- $\mathbf{z}_i$：当前时间步的共享潜在纹理图
- $p_\theta(\mathbf{x}_{i-1,1}|\mathbf{z}_i)$：第一个视图的去噪分布，仅依赖于当前潜在纹理
- $p_\theta(\mathbf{x}_{i-1,n}|\{\mathbf{x}_{i-1,j}\}_{j=1}^{n-1},\mathbf{z}_i)$：第 $n$ 个视图的去噪分布，条件于前 $n-1$ 个视图的去噪结果

这一分解使得每个视图的去噪过程能够感知先前视图已生成的纹理内容，从而在采样顺序中逐步建立视图间一致性。

#### 3.2.2 首个视图采样

对于第一个相机视图 $C_1$，SIMS 通过渲染函数 $\mathcal{R}$ 将当前潜在纹理图 $\mathbf{z}_i$ 映射到图像空间，然后执行一次 DDIM 去噪：

$$ \mathbf{x}_{i-1,1} \sim f_\theta^{(t_i)}(\mathbf{x}_{i-1,1} | \mathbf{x}_{i,1}' = \mathcal{R}(\mathbf{z}_i; C_1)) \tag{4} $$

其中 $\mathcal{R}(\mathbf{z}_i; C_1)$ 表示使用相机 $C_1$ 渲染潜在纹理图 $\mathbf{z}_i$ 得到的潜在图像，$f_\theta^{(t_i)}$ 为扩散模型在时间步 $t_i$ 的去噪函数。

#### 3.2.3 视图采样与噪声匹配

对于后续视图 $n \geq 2$，SIMS 的关键操作是**噪声匹配**——对已访问区域添加适量噪声，使其噪声水平与当前扩散步保持一致，然后再进行去噪：

$$ \mathbf{z}_{i,n} = M_{i,n} \odot \left( \sqrt{ \frac{\alpha_{i-1}}{\alpha_i} } \mathbf{z}_{i-1,n-1} + \sigma_i \epsilon_i \right) + (\mathbf{1} - M_{i,n}) \odot \mathbf{z}_i \tag{5a} $$

$$ \mathbf{x}_{i-1,n} \sim f_\theta^{(t_i)}(\mathbf{x}_{i-1,n} | \mathbf{x}_{i,n}' = \mathcal{R}(\mathbf{z}_{i,n}; C_n)) \tag{5b} $$

**变量含义**：
- $M_{i,n}$：二值掩码，标记相机 $C_n$ 可见的纹理区域
- $\sqrt{\frac{\alpha_{i-1}}{\alpha_i}}$：噪声缩放因子，将 $t_{i-1}$ 的噪声水平调整至 $t_i$
- $\sigma_i \epsilon_i$：添加的新噪声项
- $\mathbf{z}_{i,n}$：经噪声匹配后的混合潜在纹理图
- $\odot$：逐元素乘法

该机制确保每个视图在去噪时，其输入图像中的已生成区域和未生成区域具有一致的噪声统计特性，避免因噪声不匹配导致的伪影。

#### 3.2.4 基于视图质量的聚合规则

每次视图去噪后，SIMS 通过逆渲染 $\mathcal{R}^{-1}$ 将去噪图像投影回 UV 纹理空间，并根据视图质量选择性地更新潜在纹理图。视图质量 $Q_{i,n}$ 由屏幕空间导数（负雅可比行列式）衡量：

$$ Q_{i,n}(u,v) = -\left| \frac{\partial u}{\partial p} \cdot \frac{\partial v}{\partial q} - \frac{\partial u}{\partial q} \cdot \frac{\partial v}{\partial p} \right| $$

该度量反映了 UV 坐标在屏幕空间的变化率：值越大（越接近 0），表示该视角下该纹理区域的采样密度越高，纹理质量越好。

聚合更新规则为：

$$ \mathbf{z}_{i-1,n}(u,v) = \begin{cases} \frac{\mathbf{z}_{i-1,n}'(u,v)}{M_{i,n}(u,v)} & M_{i,n}(u,v)>0 \text{ and } Q_{i,n}(u,v)>Q_i(u,v) \\ \mathbf{z}_{i-1,n-1}(u,v) & \text{otherwise} \end{cases} \tag{6} $$

**变量含义**：
- $\mathbf{z}_{i-1,n}'(u,v)$：当前视图去噪后投影回 UV 空间的纹理值
- $M_{i,n}(u,v)$：当前视图在 $(u,v)$ 处的可见性掩码
- $Q_i(u,v)$：已累积的最佳视图质量
- 除以 $M_{i,n}(u,v)$ 用于归一化多次投影的累积效应

该规则确保每个纹理像素始终保留来自最佳视角（最高采样密度）的去噪结果，从而实现高保真的纹理覆盖。

---

### 3.3 神经颜色场蒸馏

SIMS 生成的是多视图一致的潜在图像集合，需进一步转换为 RGB 纹理图。直接使用 Stable Diffusion 解码器解码潜在纹理图会导致 UV 边界伪影和视图间外观不一致（如 Figure 4 所示）。TexFusion 采用**神经颜色场蒸馏**解决此问题：

1. 使用 SD 解码器将 SIMS 输出的多视图潜在图像解码为 RGB 图像
2. 优化一个基于哈希编码的 MLP 神经颜色场，以多视图 RGB 图像为监督信号
3. 将训练好的颜色场烘焙为高分辨率 UV 纹理图

该模块将多视图 RGB 信息融合为全局一致的纹理表示，避免了直接潜在空间操作带来的解码不一致性问题。

---

### 3.4 多分辨率纹理生成

TexFusion 采用粗到细的两阶段策略：

- **粗阶段**：使用全景相机（大视场角）生成低分辨率纹理，建立全局语义和颜色分布
- **细阶段**：使用更窄视角的相机进行高分辨率细化，在保持全局一致性的前提下增强局部细节

这种策略有效避免了单阶段高分辨率生成中常见的内容漂移问题。

---

### 3.5 条件引导配置

TexFusion 使用 Stable Diffusion 2-depth 作为扩散骨干，联合深度和文本条件进行分类器自由引导：

$$ \epsilon_\theta^{\prime t_i}(\mathbf{x}_{i,n}; d_n, \text{text}) = (1-w_{joint})\epsilon_\theta^{t_i}(\mathbf{x}_{i,n}) + w_{joint}\epsilon_\theta^{t_i}(\mathbf{x}_{i,n}; d_n, \mathbf{text}) $$

其中 $d_n$ 为相机 $C_n$ 渲染的深度图，$w_{joint}$ 为联合引导权重。深度条件确保生成纹理与输入网格的几何结构对齐，文本条件控制语义内容。

## 实验与关键发现

### 主实验结果

TexFusion在35个网格与约86个提示组合的纹理生成任务上与**TEXTure**（Richardson et al., 2023）进行了全面对比。Table 1汇总了定量与定性评估结果。

**FID分布距离**：以Stable Diffusion 2-depth自身生成的图像集为参考分布，TexFusion的FID得分为59.78，远低于TEXTure的79.47（Δ=-19.69）。这表明TexFusion生成的纹理在分布层面与扩散模型的生成域更接近，视觉质量更高。

**用户偏好研究**：通过Amazon Mechanical Turk进行的用户研究（每个提示3名评估者）显示，TexFusion在三个维度上均显著优于TEXTure：
- 自然色彩偏好率：75.58% vs 24.42%（Δ=+51.16%）
- 较少伪影偏好率：68.60% vs 31.40%（Δ=+37.20%）
- 提示文本对齐度偏好率：56.98% vs 43.02%（Δ=+13.96%）

**生成效率**：Table 2给出了单样本端到端运行时间对比（NVIDIA RTX A6000）。TexFusion使用9相机配置仅需2.2分钟，24相机配置需6.2分钟。相比之下，基于SDS的**stable-dreamfusion**（Tang et al., 2023）需约39分钟，**Latent-Painter**（Metzer et al., 2022）需约22分钟，TexFusion实现了10-18倍的加速。

**与SDS方法的定性对比**：Figure 11展示了TexFusion与stable-dreamfusion、Latent-Painter的可视化对比。需要指出的是，该对比仅选取了stable-dreamfusion成功收敛几何体的样本（如Figure 12所示，该方法在几何生成上经常失败），因此可能高估了SDS方法的实际纹理质量。即便如此，TexFusion仍展现出更自然的色彩饱和度和更少的视图不一致伪影。

### 消融实验

**非随机DDIM采样的影响**：将SIMS中的随机DDIM采样（η=1）替换为非随机DDIM（τ=0，即σ_{t_i}=0）可显著增强材质细节表现。Figure 7展示了皮革纹理和木瓦屋顶纹理在非随机模式下获得了更丰富的微观细节。然而，这一设置在低多边形或光滑网格上可能导致块状伪影（Figure 9左），因为确定性去噪过程对几何离散化更为敏感。

**ControlNet骨干替换**：TexFusion的SIMS框架可直接将扩散骨干从SD2-depth替换为ControlNet，无需修改流程。Figure 8和Figure 13展示了两种模式的效果：
- **正常模式（normal mode）**：提供更稳定的几何控制，纹理与网格表面法线高度一致。
- **猜测模式（guess mode）**：允许更自由的纹理创作，但容易发生语义漂移，特别是在缺乏明确深度提示的区域（Figure 9右）。

![[assets/figures/papers/paper_list_l34_https_arxiv_org_abs_2310_13772/figures/006_Figure.jpg]]

![[assets/figures/papers/paper_list_l34_https_arxiv_org_abs_2310_13772/figures/014_Figure.jpg]]

![[assets/figures/papers/paper_list_l34_https_arxiv_org_abs_2310_13772/figures/015_Figure.jpg]]

![[assets/figures/papers/paper_list_l34_https_arxiv_org_abs_2310_13772/figures/016_Figure.jpg]]

![[assets/figures/papers/paper_list_l34_https_arxiv_org_abs_2310_13772/figures/017_Figure.jpg]]

**相机配置数量**：Table 2的运行时数据同时反映了相机数量的影响。9相机配置可在2.2分钟内获得合理结果，24相机配置能改善纹理覆盖度，但时间增至6.2分钟。这表明相机数量在覆盖度与效率之间存在直接权衡。

### 失败模式分析

TexFusion的主要失败模式集中在以下场景（Figure 9）：

1. **非随机DDIM + 低多边形网格**：确定性采样对网格离散化误差敏感，在光滑或低多边形网格上产生明显的块状伪影。
2. **ControlNet猜测模式漂移**：当几何体缺乏明确深度提示时，猜测模式可能生成与几何形状不一致的纹理语义，例如将平面区域误解为不同材质。
3. **极端几何形状**：长细棒状或具有极端曲率的几何体需要专门定制的相机配置，默认的均匀采样策略可能无法充分覆盖所有表面区域。
4. **纹理分辨率瓶颈**：受限于潜在扩散模型的潜在空间尺寸和UV参数化分辨率，TexFusion难以生成超高分辨率细节。当前方法未建模光照和材质属性（如金属度、粗糙度），生成的纹理仅为漫反射颜色。

### 实验公平性说明

以下因素可能影响实验结论的普适性：
- 与stable-dreamfusion的对比仅选取了其成功收敛的示例，可能高估了该方法的实际纹理质量。
- 用户研究样本量较小（每个提示3人），可能不足以达到统计显著性。
- FID计算参考集为SD2-depth自身生成的图像而非真实照片，可能偏向于生成类似扩散模型训练数据风格的纹理，而非评估照片真实感。
- 实验使用的35个网格和约86个提示组合（详见Table 3和Table 4）为自建数据集，其在更广泛几何类别上的泛化性尚需验证。

![[assets/figures/papers/paper_list_l34_https_arxiv_org_abs_2310_13772/figures/007_Figure_6.jpg]]
*Figure 6: Visual comparison of textures generated by TEXTure [62] and TexFusion. Table 1: Quantitative and qualitative comparisons between TEX-Ture and TexFusion . FID is computed w.r.t. a set of images synthesized by SD2-depth*

## 定位与知识库关联

### 方法谱系与核心区别

TexFusion 处于文本到3D纹理生成的方法谱系中，其核心定位是**在扩散模型的去噪过程中进行多视图一致性采样**，而非后处理式的纹理优化或纯自回归视图生成。

与TexFusion最直接相关的并发工作是 **TEXTure**（Richardson et al., 2023），两者均以3D网格和文本提示为输入，利用预训练的2D扩散模型生成UV纹理。然而，两者的生成机制存在根本差异：

- **TEXTure** 采用自回归视图采样策略，依次从不同相机视角生成纹理，每个新视图基于先前视图的已生成区域进行修复（inpainting）。这种顺序依赖导致了一个关键缺陷：早期视图中的错误会不可调和地传播到后续视图，产生无法修正的伪影（见Figure 3）。TexFusion通过在每个去噪步骤中交错聚合所有视图的潜在纹理，从根本上避免了这一问题。

- **Latent-Painter**（Metzer et al., 2022）和 **stable-dreamfusion**（Tang et al., 2023）属于基于分数蒸馏采样（Score Distillation Sampling, SDS）的方法族。这类方法将扩散模型作为可微分的损失函数，通过反向传播优化纹理参数。其瓶颈在于：需要极高的分类器自由引导权重（通常>100）才能产生可辨识的纹理，这导致纹理过饱和、多样性低，且优化过程缓慢（约22-39分钟）。TexFusion完全避开了SDS范式，改用标准的扩散模型采样过程，在2.2-6.2分钟内即可生成纹理，速度提升10-18倍，同时避免了SDS固有的色彩过饱和问题。

### 核心机制差异总结

| 维度 | TEXTure | Latent-Painter / SDS族 | TexFusion |
|------|---------|----------------------|-----------|
| 生成机制 | 自回归视图采样 | SDS蒸馏优化 | 顺序交错多视图采样（SIMS） |
| 视图一致性 | 弱（顺序依赖导致错误累积） | 中（全局优化但收敛慢） | 强（每步去噪后交错聚合） |
| 色彩自然度 | 一般 | 差（过饱和） | 优（用户偏好率75.58%） |
| 采样时间 | ~分钟级 | 22-39分钟 | 2.2-6.2分钟 |
| 扩散模型使用方式 | 自回归修复 | 分数蒸馏损失 | 标准去噪采样 |

### 适用边界与局限

尽管TexFusion在纹理质量、一致性和效率上展现出显著优势，其适用性仍受以下边界条件约束：

1. **网格质量依赖**：在低多边形或光滑网格上使用非随机DDIM采样（$\sigma_{t_i}=0$）时，可能出现块状伪影（Figure 9左）。这是因为确定性采样放大了纹理参数化在几何不连续处的采样不足问题。

2. **语义漂移风险**：当集成ControlNet的猜测模式（guess mode）时，纹理语义可能偏离提示文本，尤其是在几何体缺乏明确深度线索的区域（Figure 9右）。正常模式（normal mode）提供更稳定的几何控制，但可能限制纹理的创作自由度。

3. **分辨率瓶颈**：纹理分辨率受限于潜在扩散模型的潜在空间尺寸和UV参数化分辨率。当前方法未集成超分辨率模块，难以生成超高分辨率的纹理细节。

4. **材质建模缺失**：TexFusion仅生成漫反射颜色纹理，未建模光照、金属度、粗糙度等PBR材质属性。生成的纹理在改变光照条件时无法正确响应。

5. **极端几何适应性**：对于长细棒状等极端几何形状，默认的相机配置可能无法提供充分的视图覆盖，需要针对性地设计相机采样策略。

### 开放问题

1. **实时生成**：能否集成更快的扩散采样器（如减少DDIM步数或渐进式蒸馏）将纹理生成时间压缩至秒级，以支持交互式应用？

2. **PBR材质扩展**：如何将方法从漫反射颜色扩展至完整的PBR材质（法线贴图、粗糙度、金属度等）的联合生成？这需要扩散模型具备多通道材质输出的能力。

3. **分辨率突破**：是否可以将TexFusion与高分辨率扩散模型或超分辨率模块级联，突破当前潜在空间尺寸对纹理分辨率的限制？

4. **自适应相机配置**：如何根据输入网格的几何特性自动确定最优的相机视图数量和分布，以在生成质量与计算开销之间取得最佳平衡？当前的9相机和24相机配置均为经验性选择。

5. **光照解耦**：当前纹理生成隐式地将光照信息烘焙到漫反射颜色中。如何实现纹理与光照的解耦生成，使得纹理可以在任意光照条件下正确渲染？

## 原文 PDF

![[paperPDFs/ICCV_2023/TexFusion_Synthesizing_3D_Textures_with_Text_Guided_Image_Diffusion_Models.pdf]]
