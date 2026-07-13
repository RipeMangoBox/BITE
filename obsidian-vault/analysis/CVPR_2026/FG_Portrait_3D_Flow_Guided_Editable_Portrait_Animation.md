---
title: "FG-Portrait: 3D Flow Guided Editable Portrait Animation"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/FG_Portrait_3D_Flow_Guided_Editable_Portrait_Animation.pdf
project_link: null
code_link: null
aliases:
- FP
- FG-Portrait
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/image_and_video_generation
- topic/vision_multimodal_applications/3d_rendering_reconstruction
core_operator: 3D流（3D Flow）：一种基于参数化3D头部模型FLAME的、无需学习的几何驱动运动对应关系，准确描述驱动→源的逐点3D位移。
primary_logic: 利用FLAME的顶点级语义一致性，直接通过驱动姿态与源形状组合的目标模型计算像素反投影后的3D位移；并提出深度引导采样将3D流编码为扩散模型条件，使网络获得精确的像素级运动引导，从而在保持身份的同时实现高保真运动传递。
claims:
- 3D流作为无需学习的几何对应，比预测的光流更鲁棒。
- 深度引导采样比均匀采样显著提升了运动传递指标（APD/AED）。
- 所提方法在自重建（self-reenactment）和跨重建（cross-reenactment）任务上均取得最佳APD/AED。
- VFHQ self-reenactment 上 APD↓ (Average Pose Distance) = 2.682
---

# FG-Portrait: 3D Flow Guided Editable Portrait Animation

> [!tip] 核心洞察
> 利用FLAME的顶点级语义一致性，直接通过驱动姿态与源形状组合的目标模型计算像素反投影后的3D位移；并提出深度引导采样将3D流编码为扩散模型条件，使网络获得精确的像素级运动引导，从而在保持身份的同时实现高保真运动传递。

| 字段 | 内容 |
|------|------|
| 中文题名 | FG-Portrait: 3D流引导的可编辑人像动画 |
| 英文题名 | FG-Portrait: 3D Flow Guided Editable Portrait Animation |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2603.23381) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/image_and_video_generation #topic/vision_multimodal_applications/3d_rendering_reconstruction |
| Method | FG-Portrait |
| Dataset | VFHQ self-reenactment, VFHQ cross-reenactment, FFHQ cross-reenactment |

> [!tip] 效果简介
> - VFHQ self-reenactment 上，APD↓ (Average Pose Distance) 2.682 vs 最佳基线 (见 Table 1) (最低)；AED↓ (Average Expression Distance) 0.327 vs 最佳基线 (见 Table 1) (最低)。
> - VFHQ cross-reenactment 上，APD↓ 7.764 vs 最佳基线 (见 Table 2) (最低)；AED↓ 0.652 vs 最佳基线 (见 Table 2) (最低)。
> - FFHQ cross-reenactment 上，FID↓ 99.4 vs 最佳基线 (见 Table 3) (最低)。

## 概要

人像动画（portrait animation）的目标是给定一张源图像和一段驱动视频（或单张驱动图像），生成一个保持源身份、同时精确复刻驱动者头部姿态与表情的目标人像。现有基于扩散模型的方法——如 **X-Portrait**（Xie et al., SIGGRAPH 2024）、**Face-Adapter**（Han et al., ECCV 2024）、**Follow-Your-Emoji**（Ma et al., SIGGRAPH Asia 2024）等——通常以驱动者的面部关键点（landmark）或驱动原图作为运动条件。这类条件缺乏源与驱动之间的显式运动对应关系：模型需要从二维信号中隐式推断三维运动，当源与驱动在视角或身份上差异较大时，学习歧义严重，导致运动传递次优，甚至出现直接复制驱动图像的现象。

本文的核心贡献在于提出了一种无需学习的、几何驱动的运动对应关系——**3D流（3D Flow）**，并将其编码为扩散模型的新型运动条件。3D流基于参数化三维头部模型 FLAME，通过组合源形状系数与驱动姿态/表情系数构建目标头部模型，再利用表面场（surface field）计算目标模型上每一点到源模型的精确三维位移向量。这一设计从根本上消除了运动歧义：模型获得的是像素级的、几何一致的逐点位移，而非需要网络自行猜测的二维投影。

为了将3D流有效注入扩散模型，作者进一步提出了**深度引导采样（depth-guided sampling）**策略：利用目标头部渲染的深度图，沿像素反投影射线在深度引导范围内采样3D点，使采样的3D流与二维像素运动精确对齐。最终，这些采样的3D流被堆叠为 $H \times W \times 3N$ 的张量，作为 ControlNet 的运动条件输入，与外观网络提取的源身份特征共同控制 U-Net 的生成过程。

在实验验证上，该方法在 VFHQ 和 FFHQ 数据集上进行了系统的自重建（self-reenactment）和跨重建（cross-reenactment）评估。以核心指标 APD（Average Pose Distance）和 AED（Average Expression Distance）衡量，所提方法在两项任务上均显著优于现有最佳基线：自重建任务上 S-APD 2.682、S-AED 0.327，跨重建任务上 C-APD 7.764、C-AED 0.652。消融实验进一步证实，3D流编码作为运动条件优于驱动 landmark 和预测光流，深度引导采样相比均匀采样能显著提升运动传递精度。此外，该方法支持在推理阶段通过直接编辑 FLAME 参数实现前馈式的表情与头部姿态编辑，展现出良好的可控性。

**方法定位**：FG-Portrait 属于“基于扩散模型的人像动画”方法簇，其核心改进在于将运动条件从二维信号升级为基于参数化头部模型的几何驱动3D流编码。在方法谱系上，它继承了 ControlNet 的条件注入范式，但在运动表征层面实现了从“隐式学习对应”到“显式几何对应”的范式跃迁。

人像动画（Portrait Animation）的目标是给定一张源图像与一段驱动视频（或单张驱动图像），生成一个目标人像视频，使其保持源人物的身份信息，同时准确复现驱动的头部姿态与表情。这一任务在虚拟数字人、视频会议、影视制作等场景中具有广泛的应用前景。

### 现有方法的缺口：运动对应关系的缺失

近年来，基于扩散模型（Diffusion Models）的方法在该任务上取得了显著进展，代表性工作包括 **X-Portrait**（Xie et al., SIGGRAPH 2024）、**Face-Adapter**（Han et al., ECCV 2024）、**EMOPortrait**（Drobyshev et al., CVPR 2024）以及 **HunyuanPortrait**（Xu et al., CVPR 2025）等。这些方法通常将驱动运动信息（如面部关键点landmark或驱动原图）作为条件注入扩散模型，以控制生成结果的运动模式。

然而，这一范式存在一个**核心瓶颈**：现有方法仅以驱动端的运动信号为条件，缺乏源与驱动之间**显式的运动对应关系**。具体而言，模型需要从驱动图像中“猜测”源人物应如何移动，而这一映射关系在训练数据中并非唯一确定——同一驱动姿态可能对应不同源人物的不同表现。这种模糊性导致模型在视角差异大、身份差异显著的跨重建（cross-reenactment）场景中，运动传递质量次优，甚至出现身份泄露或运动复制偏差。

### 本文动机：引入几何驱动的显式运动对应

针对上述问题，本文提出一个核心洞察：**利用参数化3D头部模型的顶点级语义一致性，可以为源与驱动之间建立精确的、无需学习的运动对应关系**。具体而言，本文引入 **3D流（3D Flow）** 作为源与驱动之间的显式运动桥梁——它描述了从目标姿态到源姿态的逐点3D位移向量，由参数化头部模型FLAME直接计算得出，不依赖任何学习过程，因而具有几何上的鲁棒性和跨身份泛化能力。

进一步地，本文提出**深度引导采样（Depth-Guided Sampling）** 机制，将3D流编码为扩散模型可理解的条件信号，使网络获得像素级的精确运动引导。这一设计从根本上解决了扩散模型“猜测”运动对应关系的歧义问题，在保持源身份的同时实现高保真的运动传递。

## 核心方法与创新机理

### 瓶颈：扩散模型缺乏显式运动对应

现有扩散式人像动画方法（如 **X-Portrait** (Xie et al., SIGGRAPH 2024)、**Face-Adapter** (Han et al., ECCV 2024)、**HunyuanPortrait** (Xu et al., CVPR 2025) 等）主要以驱动图像的 landmark 或原图作为运动条件。这类条件隐式地编码运动信息，但缺失源与驱动之间的显式运动对应关系。当源与驱动的视角、身份差异较大时，网络需要同时推断“往哪动”和“动多少”，导致学习歧义——模型可能倾向于直接复制驱动图像的外观，而非仅迁移其运动（Table 6 中 Dri-Img 条件的 S-APD 低至 1.060，近乎直接拷贝）。这一瓶颈在跨身份重建（cross-reenactment）场景中尤为突出。

### 关键机制：3D 流——无需学习的几何驱动运动对应

FG-Portrait 的核心创新在于引入 **3D 流（3D Flow）** 作为运动对应关系，从根本上改变了运动条件的表达形式。其因果链条如下：

1. **参数化 3D 头部模型 FLAME**：从源图像和驱动图像分别估计 FLAME 系数——形状 $\beta$、姿态 $\theta$、表情 $\psi$：
   $$M_{src} = M(\beta_{src}, \theta_{src}, \psi_{src}), \quad M_{dri} = M(\beta_{dri}, \theta_{dri}, \psi_{dri})$$

2. **目标 FLAME 构建**：组合源形状与驱动姿态/表情，生成“源身份 + 驱动运动”的目标 3D 头部：
   $$M_{tgt} = M(\beta_{src}, \theta_{dri}, \psi_{dri})$$

3. **3D 流计算**：利用 FLAME 的顶点级语义一致性，通过表面场（Surface Field）将目标模型上的点 $p_{tgt}$ 映射到源模型上的对应点 $p_{src}$，再计算逐点 3D 位移：
   $$f_{src \rightarrow tgt} = p_{src} - p_{tgt}$$
   该位移向量精确描述了“目标姿态下的每个 3D 点需要移动多少才能回到源姿态”。由于 FLAME 拓扑固定，这一对应关系是 **无需学习的（learning-free）**，天然具有几何一致性，避免了对预测光流等学习式方法的依赖。

### Changed Slot：运动条件从“隐式图像/Landmark”变为“显式 3D 流编码”

| 条件槽 | 基线方案 | FG-Portrait 方案 |
|--------|----------|------------------|
| 运动条件 | 驱动 landmark 或原图（如 X-Portrait 用 driving image） | 3D 流编码 + 深度引导采样 |

这一 changed slot 是整个方法的核心杠杆。具体实现包含两个紧密耦合的设计：

**深度引导采样（Depth-Guided Sampling）**：直接将 3D 流映射到 2D 像素空间时，若采用均匀深度采样，采样点可能落在远离实际头部表面的位置，导致 3D 流与 2D 运动失配（Fig. 4(a)）。FG-Portrait 通过渲染目标 FLAME 的深度图 $\tilde{D}_{tgt}$ 来约束采样范围，使每个像素沿反投影射线采样的深度点集中在实际头部表面附近：
$$\boldsymbol{p}_{tgt}^{n} = H \left[ d_{n} \left( K^{-1} q_{tgt} \right)^{\top}, 1 \right]^{\top}, \quad d_n \in [\tilde{D}_{tgt}(q_{tgt}) - \delta, \tilde{D}_{tgt}(q_{tgt}) + \delta]$$

消融实验证实，深度引导采样相比均匀采样显著提升运动传递质量（LPIPS 0.158 vs 0.163，S-APD 2.682 vs 3.254，Table 5）。

**3D 流编码**：将每个像素采样的 $N$ 个 3D 流向量堆叠为 $H \times W \times 3N$ 的张量 $F_{src \rightarrow tgt}$，作为 ControlNet 的运动条件输入。这一设计使扩散模型获得了像素级的精确运动引导，无需从图像中隐式推断运动。

### 证据强度

- **运动条件对比消融（Table 4）**：3D 流编码在自重建和跨重建任务的所有指标上均优于驱动 landmark 和预测光流（S-APD 2.682, S-AED 0.327, C-APD 7.764, C-AED 0.652），置信度 0.98。
- **深度引导采样消融（Table 5）**：深度引导在 APD 上带来约 17.6% 的相对提升（3.254 → 2.682），置信度 0.95。
- **与驱动原图条件的对比（Table 6, Fig. 9）**：使用驱动原图作为条件时，模型趋于直接复制（S-APD 1.060），而 3D 流编码能正确迁移运动，置信度 0.98。

### 辅助创新：推理阶段可编辑性

作为 3D 流框架的自然延伸，FG-Portrait 支持在推理时通过直接编辑 FLAME 系数实现前馈式表情和姿态控制：
$$\psi_{dri} \leftarrow \psi_{dri} + \Delta \psi_{usr}, \quad \theta_{dri} \leftarrow \theta_{dri} + \Delta \theta_{usr}$$
编辑后的系数重新驱动 3D 流计算，无需重新训练或微调，即可生成符合用户指定运动的目标图像（Fig. 8）。

FG-Portrait 的整体 pipeline 围绕一个核心设计展开：**将显式的3D运动对应关系编码为扩散模型的条件信号**，从而在保持源人物身份的同时，高保真地传递驱动运动的姿态与表情。框架由三个逻辑阶段串联构成：**3D头部建模与流计算**、**深度引导采样与3D流编码**、**条件扩散生成**。

### 输入输出流

系统接收两张输入图像——源图像 $I_{src}$ 和驱动图像 $I_{dri}$（或用户编辑的姿态/表情参数），输出一张合成图像 $I_{tgt}$，该图像具有 $I_{src}$ 的身份和背景，同时呈现 $I_{dri}$ 的头部姿态与面部表情。训练阶段，$I_{dri}$ 从与 $I_{src}$ 同一人的视频中采样，训练目标为重建 $I_{tgt}$ 使其等于 $I_{dri}$（Figure 3）。

![[assets/figures/papers/paper_list_l1021_https_arxiv_org_abs_2603_23381/figures/003_Figure_3.jpg]]
*Figure 3: Our Framework. We propose the 3D flow encoding*

### 阶段一：FLAME参数估计与目标头部构建

首先，利用预训练的FLAME参数估计器分别从 $I_{src}$ 和 $I_{dri}$ 中提取三组系数：形状系数 $\beta$、姿态系数 $\theta$ 和表情系数 $\psi$，得到各自的3D头部模型 $M_{src}$ 和 $M_{dri}$（Eqn. 2）。

随后，框架执行一个关键的“参数重组”操作：**组合源图像的形状系数与驱动图像的姿态/表情系数**，构建一个目标3D头部模型 $M_{tgt}$（Eqn. 3）。这一设计的直觉在于：$M_{tgt}$ 在几何形状上与源人物一致，但在姿态和表情上完全对齐驱动信号，从而为后续的3D流计算提供了精确的几何锚点。

### 阶段二：3D流计算与深度引导采样

在获得 $M_{src}$ 和 $M_{tgt}$ 后，框架利用FLAME模型的顶点级语义一致性，通过表面场（Surface Field）查找，建立 $M_{tgt}$ 上每个顶点到 $M_{src}$ 上对应顶点的映射关系（Eqn. 4）。**3D流**定义为从目标顶点指向源顶点的3D位移向量（Eqn. 5），它精确描述了驱动运动所需的逐点空间变化（Figure 2）。

要将3D流作为扩散模型的条件，需要将其映射到2D图像平面上。框架对目标图像的每个像素 $q_{tgt}$，沿其反投影射线在深度方向上采样 $N$ 个点，对每个采样点查询其3D流，最终将每个像素的 $N$ 个3D位移向量堆叠为一个 $H \times W \times 3N$ 的张量——即**3D流编码** $F_{src \rightarrow tgt}$（Eqn. 6）。

这里的一个关键设计是**深度引导采样**：通过渲染 $M_{tgt}$ 的深度图 $\tilde{D}_{tgt}$（Eqn. 7），将采样范围约束在目标头部表面附近，而非在整条射线上均匀采样。这使得采样点更接近像素的实际3D位置，从而查询到的3D流能更准确地反映2D运动（Figure 4）。

### 阶段三：条件扩散生成

生成模块基于Stable Diffusion架构，由两个核心组件构成：

- **ControlNet $G$**：接收3D流编码 $F_{src \rightarrow tgt}$ 作为运动条件，控制U-Net的去噪过程，确保生成图像的运动模式与驱动信号对齐。
- **外观网络（Appearance Network）**：从源图像 $I_{src}$ 中提取身份和背景特征，注入U-Net的自注意力层，维持生成图像中源人物的身份一致性。

训练损失为标准扩散噪声预测损失（Eqn. 1），条件 $c$ 同时包含外观特征和3D流编码。

### 推理时的可编辑性

在推理阶段，框架支持**前馈式姿态和表情编辑**：用户可以直接在FLAME参数空间中指定姿态编辑量 $\Delta \theta_{usr}$ 和表情编辑量 $\Delta \psi_{usr}$，将其叠加到驱动系数上（Eqn. 8），然后重新计算 $M_{tgt}$ 和3D流编码，即可生成编辑后的动画结果，无需任何额外的训练或优化。

### 方法谱系与知识库定位

FG-Portrait 在肖像动画领域的方法谱系中占据一个独特位置。与基于landmark的扩散方法（如 **X-Portrait** (Xie et al., SIGGRAPH 2024)、**Follow-Your-Emoji** (Ma et al., SIGGRAPH Asia 2024)）和基于隐式条件控制的方法（如 **HunyuanPortrait** (Xu et al., CVPR 2025)）不同，FG-Portrait 的运动条件来自**无需学习的几何对应关系**，而非从数据中隐式习得。与基于光流的运动模型（如 **FOMM** (Siarohin et al., NeurIPS 2019)）相比，3D流避免了光流预测网络在视角/身份差异大时的歧义性问题。在身份保持方面，FG-Portrait 采用外观特征注入策略，与 **Face-Adapter** (Han et al., ECCV 2024) 和 **MagicPose** (Chang et al., arXiv 2023) 等工作的思路相近，但其运动条件的设计从根本上降低了“运动传递”与“身份保持”之间的学习冲突。

**核心瓶颈与因果机制**：现有扩散方法以驱动landmark或原图作为运动条件时，网络需要同时隐式推断运动对应关系和生成目标图像，这在源-驱动视角或身份差异较大时导致学习歧义。FG-Portrait 通过引入3D流编码，将运动对应关系**外化**为一个显式的、几何精确的信号，使生成网络只需专注于“如何渲染”，而无需猜测“应该移动到哪里”。深度引导采样进一步确保了这一几何信号在投影到2D时与像素运动精确对齐。

**证据强度**：定量消融（Table 4）直接验证了3D流编码相对于驱动landmark和预测光流的优越性——在所有APD/AED指标上均取得最佳。深度引导采样的消融（Table 5）显示，相比均匀采样，APD从3.254降至2.682，LPIPS从0.163降至0.158，证实了其有效性。跨重建任务上的领先表现（Table 2: C-APD 7.764, C-AED 0.652）进一步证明该方法对身份变化的鲁棒性。

**局限与待验证点**：深度引导采样依赖FLAME的准确拟合，极端姿态或遮挡下FLAME估计误差可能传播至3D流质量；当前方法未显式建模头发、服装等非面部区域的运动，这些区域的运动传递精度可能不足。对于卡通肖像的泛化能力有限（Figure 11），需要额外的数据增强或域适应策略。

FG-Portrait 的核心创新在于用**无需学习的几何驱动3D流**替代传统扩散模型中的隐式运动条件，并通过**深度引导采样**将其编码为 ControlNet 的显式运动先验。以下按管线顺序阐述关键模块及其公式。

### 3.1 预备：扩散训练目标

方法基于 Stable Diffusion 的 U-Net 架构，训练目标为标准噪声预测损失：

$$\mathcal{L} = \mathbb{E}_{z_0, c, \epsilon, t} \left[ \left\| \epsilon - U(z_t, t, c) \right\|_2^2 \right] \tag{1}$$

其中 $z_t$ 为加噪潜变量，$c$ 为条件信号（本文中包括外观条件与运动条件），$U$ 为 U-Net 去噪网络。

### 3.2 FLAME 参数估计与目标头部构建

从源图像 $I_{src}$ 和驱动图像 $I_{dri}$ 分别估计参数化 3D 头部模型 FLAME 的系数：

$$M_{src} = M(\beta_{src}, \theta_{src}, \psi_{src}) \quad M_{dri} = M(\beta_{dri}, \theta_{dri}, \psi_{dri}) \tag{2}$$

其中 $\beta$ 为形状系数，$\theta$ 为姿态系数，$\psi$ 为表情系数。

为获得描述“源身份 + 驱动运动”的动画目标姿态，构建**目标 FLAME 模型**：

$$M_{tgt} = M(\beta_{src}, \theta_{dri}, \psi_{dri}) \tag{3}$$

即组合源的形状与驱动的姿态/表情，使 $M_{tgt}$ 在 3D 几何上代表期望的动画输出。

### 3.3 3D 流计算（核心运动对应）

利用 FLAME 的顶点级语义一致性，通过**表面场（Surface Field）** 建立 $M_{tgt}$ 到 $M_{src}$ 的逐点对应：

$$p_{src} = \mathrm{SF}(p_{tgt}; M_{tgt}, M_{src}) \tag{4}$$

其中 $p_{tgt}$ 为目标模型上的 3D 点，$p_{src}$ 为源模型上的对应点。由此定义**3D 流**——描述驱动运动到源状态的逐点 3D 位移：

$$f_{src \rightarrow tgt} = p_{src} - p_{tgt} \tag{5}$$

该流向量为学习无关的几何对应，准确刻画了从目标姿态“回到”源姿态所需的 3D 运动。

### 3.4 深度引导采样与 3D 流编码

为将 3D 流注入扩散模型，需将 2D 像素与 3D 空间关联。对目标图像平面上的像素齐次坐标 $q_{tgt}$，沿反投影射线在深度 $d_n$ 处采样 3D 点：

$$\boldsymbol{p}_{tgt}^{n} = H \left[ d_{n} \left( K^{-1} q_{tgt} \right)^{\top}, 1 \right]^{\top} \tag{6}$$

其中 $K$ 为相机内参，$H$ 为齐次坐标归一化。

**深度引导采样**的关键在于采样深度范围的确定：先渲染 $M_{tgt}$ 的深度图 $\tilde{D}_{tgt}$：

$$\tilde{D}_{tgt} = \mathrm{Render}\left( M_{tgt}; H, K \right) \tag{7}$$

以渲染深度 $\tilde{D}_{tgt}$ 为中心、$\delta$ 为搜索半径确定采样区间 $[d_{near}, d_{far}]$，使采样点集中在实际头部表面附近。相比均匀采样（在整个深度区间等距采样），深度引导采样确保采到的 3D 点更贴近像素的真实 3D 位置，从而使对应的 3D 流更准确地反映 2D 运动（见 Figure 4）。

对每个像素采样 $N$ 个深度点，分别计算对应的 3D 流向量，堆叠为 $H \times W \times 3N$ 的**3D 流编码** $F_{src \rightarrow tgt}$，作为 ControlNet 的运动条件输入。

### 3.5 推理时的可编辑运动控制

推理阶段，用户可通过直接编辑 FLAME 系数实现前馈式表情与姿态控制：

$$\psi_{dri} \leftarrow \psi_{dri} + \Delta \psi_{usr}, \quad \theta_{dri} \leftarrow \theta_{dri} + \Delta \theta_{usr} \tag{8}$$

其中 $\Delta \psi_{usr} \in \mathbb{R}^{100}$ 和 $\Delta \theta_{usr} \in \mathbb{R}^{12}$ 为用户指定的编辑增量。修改后的系数重新参与式 (3) 构建 $M_{tgt}$ 及后续 3D 流计算，无需重新训练即可实现表情幅度调整、头部转动等编辑效果。

### 3.6 外观网络

除运动条件外，外观网络从 $I_{src}$ 提取身份与背景特征，注入 U-Net 的自注意力层，以保持源人物身份一致性。该模块与 X-Portrait 等工作的外观注入机制类似，非本文核心创新点，故不展开详述。

![[assets/figures/papers/paper_list_l1021_https_arxiv_org_abs_2603_23381/figures/002_Figure_2.jpg]]
*Figure 2: Visualization of 3D flows. Target portrait is the animated image with the source identity and driving motion. Target 3D head is the head model of target portrait, which is pre-computed by assembling source shape and driving motion parameters. We select some corresponding points both in the 2D and 3D, with red denoting the source and green denoting the target position. The 3D flows (black lines) correctly reflect the displacement from the target to the source position for each point. The yellow circles mark one example of a pair of points and the corresponding 3D flow*

## 实验与关键发现

### 核心实验设置

实验基于 **VFHQ** 和 **FFHQ** 两个数据集，分别在 **自重建（self-reenactment）** 和 **跨重建（cross-reenactment）** 两种任务设定下评估。自重建任务中，源图像和驱动图像来自同一人的不同帧；跨重建任务中，源和驱动来自不同身份。所有对比方法均使用官方代码和预训练权重，在相同的测试集上以统一帧采样策略评估。主要指标包括：

- **APD**（Average Pose Distance，↓）：平均姿态距离，数值越低表示运动传递越准确。
- **AED**（Average Expression Distance，↓）：平均表情距离，数值越低表示表情传递越准确。
- **FID**（↓）：生成图像质量与分布匹配度。
- **CSIM**（↑）：源身份余弦相似度。
- **LPIPS**（↓）：感知图像相似度。

### 主实验结果

#### 自重建任务（VFHQ）

在自重建设定下，FG-Portrait 在所有运动传递指标上均取得最优。如 **Table 1** 所示，APD 达到 **2.682**，AED 达到 **0.327**，均显著低于所有基线方法。这表明所提 3D 流编码能够精确地将驱动运动传递到源身份上，即使源与驱动帧之间存在姿态和表情差异。

![[assets/figures/papers/paper_list_l1021_https_arxiv_org_abs_2603_23381/figures/005_Table_1.jpg]]
*Table 1: Comparison on the self-reenactment task on VFHQ at*

#### 跨重建任务（VFHQ）

跨重建任务更具挑战性，因为源和驱动来自不同身份，模型需要同时保持源身份并准确传递驱动运动。如 **Table 2** 所示，FG-Portrait 的 APD 为 **7.764**，AED 为 **0.652**，在所有对比方法中均为最低。相比之下，基于 landmark 或驱动原图作为条件的方法在跨身份场景下运动传递明显退化。

![[assets/figures/papers/paper_list_l1021_https_arxiv_org_abs_2603_23381/figures/006_Table_2.jpg]]
*Table 2: Comparison on the cross-reenactment task on VFHQ at 5122. ↓ means lower the better and ↑ is the opposite. APD is scaled by 100. Best results are marked bold*

#### 跨数据集泛化（FFHQ）

为验证泛化能力，在 FFHQ 数据集上进行跨重建评估。如 **Table 3** 所示，FG-Portrait 的 FID 达到 **99.4**（最低），CSIM 达到 **0.558**（较高），表明方法在未见数据上仍能保持较好的身份一致性和运动传递质量。

![[assets/figures/papers/paper_list_l1021_https_arxiv_org_abs_2603_23381/figures/008_Table_3.jpg]]
*Table 3: Comparison on the cross-reenactment task on FFHQ at 5122. ↓ means lower the better and ↑ is the opposite. APD is scaled by 100. Best results are marked bold*

### 消融实验

#### 运动条件对比

**Table 4** 系统比较了三种运动条件：驱动 landmark、预测光流（predicted flow）和所提 3D 流。结果表明，3D 流在自重建和跨重建的所有指标上均最优（S-APD 2.682, S-AED 0.327, C-APD 7.764, C-AED 0.652）。预测光流虽然能捕捉 2D 运动，但缺乏几何一致性，在视角变化大时产生歧义；驱动 landmark 则丢失了密集的运动对应信息。

#### 深度引导采样

**Table 5** 消融了深度引导采样（depth-guided sampling）的效果。使用均匀采样替代深度引导采样后，APD 从 **2.682** 退化到 **3.254**，LPIPS 从 **0.158** 增加到 **0.163**。这验证了深度引导采样能更准确地捕捉与 2D 运动对应的 3D 流，从而提升运动传递精度。

#### 驱动原图作为条件

**Table 6** 对比了使用驱动原图（Dri-Img）作为运动条件的情况。结果显示，Dri-Img 在自重建任务上 APD 仅为 **1.060**（接近 1，意味着几乎直接复制驱动图像），而 FG-Portrait 的 APD 为 **2.682**，说明所提方法正确地迁移了运动而非简单复制。定性结果（**Figure 9**）进一步证实，Dri-Img 条件导致模型直接输出驱动图像，而 FG-Portrait 能保持源身份并准确传递驱动姿态和表情。

#### 采样点数 N

**Table 7** 消融了 3D 流编码中每像素采样点数 N 的影响。N=20（默认设置）取得最佳运动指标；N=10 时 APD 轻微退化至 **2.724**，表明足够的采样密度对精确运动编码是必要的。

#### 深度搜索范围 δ

**Table 8** 消融了深度搜索范围 δ 的影响。δ=0.01m 为最佳设置；δ 过小（0.005m）或过大（0.05m）均导致 APD 轻微退化，说明合理的深度搜索范围对准确捕获 3D 流至关重要。

### 时间一致性分析

**Table 9** 给出了自重建任务上的时间一致性评估（FVD）。FG-Portrait 排名第二，表明所提方法在保持运动传递精度的同时，也具有较好的时序稳定性。时间一致性受益于 3D 流编码提供的帧间几何一致性，但未显式建模时序依赖，因此略逊于专门优化时序的方法。

### 失败模式与局限性

1. **卡通肖像泛化有限**：模型仅在真实人像数据上训练，对卡通肖像的泛化不足，可能出现眼睑闭合等瑕疵（**Figure 11**）。
2. **FLAME 拟合依赖**：深度引导采样依赖 FLAME 的准确拟合，极端姿态或严重遮挡下 FLAME 估计误差可能影响 3D 流质量，进而降低运动传递精度。
3. **非面部区域运动**：当前方法未显式建模头发、服装等非面部区域的运动，这些区域的运动传递可能不够精确，在复杂发型或配饰场景下可能出现伪影（**Figure 10**）。

### 关键图表结论汇总

| 图表 | 核心结论 |
|------|----------|
| **Table 1** | 自重建任务上 APD/AED 最优，运动传递精度显著优于基线 |
| **Table 2** | 跨重建任务上 APD/AED 最优，跨身份运动传递鲁棒 |
| **Table 3** | FFHQ 跨重建 FID 最低，泛化能力强 |
| **Table 4** | 3D 流作为运动条件优于 landmark 和预测光流 |
| **Table 5** | 深度引导采样显著提升运动传递指标 |
| **Table 6** | 驱动原图条件导致直接复制，所提方法正确迁移运动 |
| **Figure 9** | 定性对比证实 Dri-Img 的复制问题与 FG-Portrait 的正确迁移 |
| **Figure 10** | 复杂场景下仍保持较好的身份一致性和运动传递 |
| **Figure 11** | 卡通肖像场景存在眼睑闭合等瑕疵，需进一步改进 |

![[assets/figures/papers/paper_list_l1021_https_arxiv_org_abs_2603_23381/figures/011_Table_5.jpg]]
*Table 5: Ablation study of depth-guided sampling on the selfreenactment task*

## 定位与知识库关联

### 1. 与现有工作的关系

FG-Portrait 处于基于扩散模型的人像动画这一活跃研究脉络中，其核心推进在于**运动条件的几何化**。

#### 1.1 相对于扩散人像动画方法

现有扩散人像动画方法普遍以驱动信号直接作为运动条件，但缺乏源与驱动之间的显式运动对应关系，导致模型学习歧义。典型基线包括：

- **X-Portrait** (Xie et al., SIGGRAPH 2024)：采用层级运动注意力机制，以驱动图像或landmark为条件。该方法隐式地让网络学习运动迁移，在视角或身份差异较大时运动传递可能出现偏差。
- **Face-Adapter** (Han et al., ECCV 2024)：引入细粒度身份和属性控制，但运动条件仍依赖驱动图像，未显式建模3D运动对应。
- **HunyuanPortrait** (Xu et al., CVPR 2025)：采用隐式条件控制，运动传递能力受限于条件设计的表达能力。
- **Follow-Your-Emoji** (Ma et al., SIGGRAPH Asia 2024)：结合landmark和外观信息进行自由风格动画，但landmark作为2D稀疏点缺乏3D几何一致性。
- **EMOPortrait** (Drobyshev et al., CVPR 2024) 与 **MagicPose** (Chang et al., arXiv 2023)：分别聚焦情感增强和姿态重定向，运动条件仍以2D或隐式表达为主。

FG-Portrait 的关键差异在于：**将运动条件从“驱动信号”替换为“3D流编码”**——一种无需学习的、基于参数化3D头部模型FLAME的几何驱动运动对应关系。该设计使网络获得精确的像素级运动引导，从根本上消除了“从驱动图像推断运动”这一歧义学习过程。

#### 1.2 相对于基于流的动画方法

**FOMM** (Siarohin et al., NeurIPS 2019) 是早期基于预测光流的图像动画方法，通过关键点检测和稠密运动估计实现运动迁移。然而，预测光流依赖网络学习，在跨身份、大姿态场景下鲁棒性不足。FG-Portrait 的3D流与之形成鲜明对比：

- **学习依赖性**：FOMM需学习光流预测网络；FG-Portrait的3D流通过FLAME模型的顶点级语义一致性直接计算，是纯几何的、无需学习的对应关系。
- **几何一致性**：3D流基于3D头部模型的表面场（surface field）计算逐顶点位移，天然保证几何一致性；预测光流在遮挡、大位移区域容易产生伪影。
- **证据支持**：消融实验（Table 4）直接对比了预测光流与3D流作为运动条件的效果，3D流在所有APD/AED指标上均显著优于预测光流。

#### 1.3 方法谱系定位

从条件设计的视角，FG-Portrait 可被定位为**“几何驱动运动条件”**范式的开创性工作。其核心组件——3D流编码与深度引导采样——形成了一条新的技术路径：

- **上游依赖**：FLAME参数估计（形状、姿态、表情系数）提供3D先验，表面场提供顶点级对应。
- **下游可扩展**：3D流编码作为ControlNet的输入条件，与Stable Diffusion的U-Net架构解耦，理论上可替换为更强的骨干网络（如DiT架构），或扩展至其他可参数化的对象类别。

### 2. 适用边界与前提假设

FG-Portrait 的有效性建立在以下前提之上，这些前提也划定了其适用边界：

1. **FLAME拟合质量**：3D流的计算完全依赖FLAME模型对源图像和驱动图像的准确拟合。在极端姿态（如超大侧脸）、严重遮挡或非典型面部外观下，FLAME参数估计误差会直接传导至3D流质量，进而影响生成结果。这是该方法的一个结构性脆弱点。

2. **真实人像域训练**：模型仅在真实人像数据（VFHQ）上训练，对卡通肖像等非真实域的泛化有限。论文自身指出（Fig. 11），在卡通肖像上可能出现眼睑闭合等瑕疵。

3. **面部区域的运动建模**：3D流仅覆盖FLAME网格顶点所描述的面部区域，未显式建模头发、服装、颈部等非面部区域的运动。这些区域的运动传递依赖于扩散模型的先验知识，精度可能不足。

4. **单帧条件假设**：当前方法以单张源图像和单帧驱动图像为输入，未利用视频时序信息。时间一致性（Table 9显示FVD排名第二）主要依赖生成模型的帧间稳定性，而非显式时序建模。

### 3. 局限性与开放问题

#### 3.1 已知局限

- **跨域泛化**：卡通肖像等非真实域的性能下降（Fig. 11），表明3D流所依赖的FLAME先验在非真实面部几何下失效。
- **非面部区域**：头发、配饰、身体等区域的运动传递缺乏几何引导，可能产生不自然的变形。
- **极端场景鲁棒性**：大角度侧脸、严重遮挡下FLAME估计的退化风险未在论文中得到充分压力测试。

#### 3.2 开放问题

1. **极端姿态与遮挡的鲁棒性**：3D流编码对于大角度侧脸或严重遮挡场景的鲁棒性如何？是否需要额外的视角增强训练策略或更鲁棒的3D人脸重建模块？

2. **骨干网络升级**：当前方法基于ControlNet + Stable Diffusion U-Net。能否将3D流引入基于DiT（Diffusion Transformer）的更强骨干网络（如HunyuanPortrait所用架构），以进一步提升生成质量和运动精度？

3. **扩展至全身动画**：3D流的几何对应思想能否扩展至全身动画或手部动画？这需要相应的参数化模型（如SMPL-X）和表面场对应机制。

4. **合成数据利用**：训练策略上是否可以利用合成数据（如Portrait4D）来覆盖更极端的运动变化和更丰富的身份多样性，从而缓解真实数据的覆盖不足？

5. **显式时序建模**：当前方法逐帧独立生成，引入时序一致性模块（如时序注意力或光流约束）是否能进一步改善视频生成的流畅度？Table 9中FVD指标排名第二表明存在改进空间。

6. **非面部区域的几何引导**：能否将3D流的思想扩展至头发、服装等区域？例如，结合发丝几何模型或服装物理模拟，为这些区域提供类似的几何驱动运动条件。

---

**证据强度说明**：以上分析中，关于FLAME依赖、卡通域泛化局限、非面部区域建模不足等判断直接来自论文自身的局限性讨论（Fig. 11 及 Sec. C）。开放问题部分基于方法设计逻辑的合理推演，其中“极端姿态鲁棒性”和“非面部区域扩展”属于论文未充分探索的方向，需后续工作验证。

## 原文 PDF

![[paperPDFs/CVPR_2026/FG_Portrait_3D_Flow_Guided_Editable_Portrait_Animation.pdf]]
