---
title: "DragAnything: Motion Control for Anything using Entity Representation"
type: paper
paper_level: A
venue: ECCV
year: 2024
pdf_ref: paperPDFs/ECCV_2024/DragAnything_Motion_Control_for_Anything_using_Entity_Representation.pdf
project_link: https://weijiawu.github.io/draganything_page/
code_link: null
aliases:
- DragAnything
tags:
- ECCV_2024
- topic/generative_models_diffusion
- topic/generative_models_diffusion/generative_models_and_autoencoders
core_operator: "用从去噪扩散模型中提取的实体掩码对应语义特征（实体表示）替代像素/区域表示，并结合2D高斯图来强调实体中心区域，从而直接操纵实体语义来驱动运动。"
primary_logic: "通过扩散模型第一帧的潜特征与实体掩码索引获得语义嵌入，并将其与2D高斯图融合后作为条件信号注入基础视频生成模型，实现了对任意实体的精确运动控制，分离了前景与背景运动。"
claims:
- "单点轨迹无法代表实体，拖拽像素区域不能精确控制目标运动。"
- "从扩散特征提取的实体表示能够实现真正的实体级运动控制。"
- "同时使用Entity和2D Gaussian Representation获得最佳运动控制精度(ObjMC 305.7)。"
- "DragAnything在人类投票中超越DragNUWA 26%，特别是在实体运动控制上。"
---

# DragAnything: Motion Control for Anything using Entity Representation

> [!tip] 核心洞察
> 通过扩散模型第一帧的潜特征与实体掩码索引获得语义嵌入，并将其与2D高斯图融合后作为条件信号注入基础视频生成模型，实现了对任意实体的精确运动控制，分离了前景与背景运动。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | DragAnything：基于实体表示的任意物体运动控制 |
| 英文题名 | DragAnything: Motion Control for Anything using Entity Representation |
| 会议/期刊 | ECCV 2024 |
| Links | [paper](https://arxiv.org/abs/2403.07420) · [Project](https://weijiawu.github.io/draganything_page/) |
| Topic | #topic/generative_models_diffusion #topic/generative_models_diffusion/generative_models_and_autoencoders |
| Method | DragAnything |
| Dataset | VIPSeg val 256x256, User Study |

> [!tip] 效果简介
> - VIPSeg val 256x256 上，FID 为 33.5，对比 39.8 (DragNUWA)，变化 -6.3。
> - VIPSeg val 256x256 上，FVD 为 494.8，对比 519.3 (DragNUWA)，变化 -24.5。
> - VIPSeg val 256x256 上，ObjMC 为 305.7，对比 324.6 (DragNUWA)，变化 -18.9。

## 概要

### 问题瓶颈

现有基于轨迹的运动控制方法（如 **DragNUWA**（Yin et al., arXiv 2023）、**MotionCtrl**（Wang et al., arXiv 2023））通过拖拽单个像素点或像素区域来控制物体运动。然而，这种像素级表示无法捕获实体的完整语义：单个轨迹点不能代表整个实体，而拖拽像素区域仅影响局部像素，无法实现精确的实体级运动控制（Figure 1、Figure 3）。当目标物体纹理复杂或与背景相似时，像素级控制容易导致外观变形、背景失控或错误的相机运动。

### 核心思路

DragAnything 提出**实体表示（Entity Representation）**来解决上述瓶颈。其核心因果机制是：从去噪扩散模型的第一帧潜特征中，利用实体掩码索引提取对应语义嵌入，作为该实体的运动控制信号；同时引入2D高斯图来强调实体中心区域权重。两者融合后注入基础视频生成模型，直接操纵实体语义来驱动运动，而非依赖像素坐标。这一设计使得前景实体运动与背景运动得以分离，实现了真正的实体级运动控制。

### 方法定位

DragAnything 以 **SVD（Stable Video Diffusion）** 为基础视频生成模型，在条件注入方式上采用类 ControlNet 的 3D UNet 架构。与 DragNUWA 等将轨迹坐标或光流直接编码为条件向量的方法不同，DragAnything 将实体表示和2D高斯图通过四层卷积编码器下采样后，与视频潜噪声相加，再注入去噪3D UNet 的解码器块。训练时引入掩码约束的 MSE 损失，使梯度仅反向传播于目标实体区域，减少对背景的干扰。

### 主要结果

在 VIPSeg 验证集（256×256）上，DragAnything 较 DragNUWA 取得显著提升：FID 从 39.8 降至 33.5，FVD 从 519.3 降至 494.8，物体运动控制精度 ObjMC 从 324.6 降至 305.7（Table 1）。用户研究中，DragAnything 在运动控制方面的人类投票偏好超越 DragNUWA 26%（Figure 8）。消融实验证实，实体表示与2D高斯图的组合是获得最优 ObjMC 的关键（Table 2），损失掩码进一步带来约5.4的 ObjMC 增益（Table 3）。需注意，当前定量比较仅针对 DragNUWA，因其他方法（如 MotionCtrl）未发布基于 SVD 的开源代码，公平性范围受限。

### 局限与开放问题

DragAnything 仍存在明显局限：大范围或快速运动下可能出现外观失真（Figure 10）；实体表示仅限于2D轨迹，无法处理深度旋转和3D姿态变化；依赖交互式分割模型 SAM 获取实体掩码，对遮挡严重或语义模糊的实体准确性下降。开放问题包括：如何将2D轨迹控制扩展到3D场景以支持物体姿态和深度控制；如何利用更强的视频生成基础模型（如 SORA）提升运动生成的鲁棒性；以及在多实体复杂交互场景下保持运动的一致性与独立性。



### 任务背景：轨迹驱动的视频运动控制

轨迹驱动的可控视频生成旨在通过用户指定的运动轨迹来操纵视频中物体的运动。给定一段参考视频的首帧、目标物体的掩码以及一条运动轨迹，系统需要生成一段视频，使目标物体按照轨迹移动，同时保持外观一致性和背景稳定性。该任务的核心挑战在于**如何精确地将稀疏的轨迹信号转化为对特定物体的运动控制**，而非对整个画面进行无差别的变换。

### 现有方法的瓶颈：像素级表示无法捕获实体语义

当前主流的轨迹运动控制方法，如 **DragNUWA**（Yin et al., arXiv 2023）和 **MotionCtrl**（Wang et al., arXiv 2023），均采用像素级或区域级的表示方式来驱动运动。具体而言，DragNUWA 将轨迹编码为密集光流条件，MotionCtrl 则使用轨迹坐标向量图。这些方法的共同缺陷在于：**它们将物体简化为若干像素点或像素区域，无法捕获物体的完整语义信息**。

这一缺陷带来了两个直接后果：

1. **拖拽点无法代表整个实体**：如图3（Insight 1）所示，物体上的单个轨迹点仅能影响其邻近的像素区域，无法驱动整个实体进行一致的移动。当用户拖拽物体上的某个点时，只有该点附近的局部区域发生位移，导致物体产生异常形变而非整体平移。

2. **控制精度随距离衰减**：如图3（Insight 2）所示，像素离拖拽点越近，受到的位移影响越大。这种空间衰减效应使得远离拖拽点的物体部分几乎不受控制，进一步加剧了运动的不一致性。

此外，**TrailBlazer**（Ma et al., arXiv 2024）尝试使用边界框来表示物体，但边界框同样是一种粗糙的区域级表示，无法区分前景物体与背景，也无法处理不规则形状的实体。

### 核心动机：从“拖拽像素”到“操纵实体语义”

上述分析揭示了一个根本性的瓶颈：**现有方法试图通过操纵像素坐标来间接控制物体运动，但像素坐标与物体语义之间不存在直接的映射关系**。一个物体由成百上千个像素组成，每个像素的语义归属取决于其在物体内部的相对位置和上下文关系，而非其绝对坐标。

DragAnything 的核心动机正是突破这一瓶颈——**直接操纵物体的语义表示来驱动运动，而非间接拖拽像素**。这一思路的关键洞察在于：如果能够从视频生成模型的内部特征中提取出目标实体的语义嵌入，并将其作为运动控制的条件信号，那么模型就能在语义层面理解“哪个物体需要移动”，从而实现真正的实体级运动控制。

### 技术路线的选择：基于扩散特征的条件注入

为实现上述目标，DragAnything 选择 **Stable Video Diffusion（SVD）** 作为基础视频生成模型。SVD 的去噪 U-Net 在生成过程中会产生丰富的潜在扩散特征，这些特征天然包含了物体的语义信息。通过利用首帧的实体掩码在扩散特征中进行索引，即可提取出对应实体的语义嵌入——即**实体表示（Entity Representation）**。

与像素点、轨迹图、边界框等传统表示相比，实体表示具有以下优势：

- **语义完整性**：实体表示编码了整个物体的外观和结构信息，而非孤立的坐标位置。
- **空间一致性**：实体表示在特征空间中自然保持了物体的内部结构关系，避免了像素级控制中的形变问题。
- **前景-背景分离**：通过掩码约束，实体表示仅关注目标物体区域，有效隔离了背景运动的干扰。

此外，DragAnything 还引入了 **2D 高斯图表示**，根据实体的中心坐标和半径生成高斯权重图，使模型更关注实体的中心区域，进一步增强了运动控制的精度和稳定性。这两种表示的融合构成了 DragAnything 运动控制信号的核心。



## 核心方法与创新机理

DragAnything 的核心创新在于用**实体语义表示**替代了现有方法中普遍使用的像素级或区域级轨迹表示，从根本上改变了运动控制的条件信号形态。这一转变解决了此前方法无法实现精确实体级运动控制的瓶颈问题。

### 从像素拖拽到实体表征

现有轨迹运动控制方法（如 **DragNUWA**，Yin et al., arXiv 2023；**MotionCtrl**，Wang et al., arXiv 2023）的基本范式是：将用户指定的轨迹点或轨迹向量图编码为条件信号，注入视频生成模型。然而，单个像素点或像素区域无法承载实体的完整语义——正如 Figure 1 和 Figure 2 所揭示的，轨迹点可能并不代表用户真正想要控制的实体，导致拖拽操作仅影响局部像素区域，而非整个目标实体。

DragAnything 的关键突破在于改变了条件信号的来源：**不再直接使用轨迹坐标作为条件，而是从去噪扩散模型的潜特征中提取实体对应的语义嵌入**。具体而言，给定第一帧的扩散特征 $\mathcal{F} = \epsilon_{\theta}(\mathbf{x}_t, t)$，利用实体掩码的坐标索引提取对应的语义特征作为实体表示。这种表示天然携带了实体的外观、结构等高层语义信息，使得模型能够“理解”被拖拽的是哪个实体，而非仅仅移动一组像素。

### 三个 Changed Slots 的因果链条

相对于基线方法，DragAnything 在三个关键设计槽位上做出了改变，三者构成一条因果链：

**1. 目标表示：从像素/区域到实体语义 + 2D 高斯**

基线方法使用轨迹点坐标、轨迹向量图或边界框作为实体表示（像素级或区域级），而 DragAnything 使用从扩散模型潜特征中提取的实体语义嵌入，并与 2D 高斯图融合。2D 高斯图的作用是强调实体中心区域——离中心越近的像素权重越大，这弥补了纯语义嵌入在空间定位上的不足。消融实验（Table 2）证实，仅使用实体表示或仅使用 2D 高斯图的物体运动控制精度（ObjMC）均劣于两者组合，组合方案取得最优 ObjMC 305.7。

**2. 条件注入方式：从直接编码到 ControlNet 式注入**

基线方法将轨迹坐标或光流直接编码为条件向量/图并叠加到视频生成过程。DragAnything 则将实体表示和 2D 高斯图通过一个四层卷积编码器 $\mathcal{E}$ 下采样至 1/8 分辨率后，与视频潜噪声相加，再注入到 ControlNet-like 的 3D UNet 解码器块中。这一设计使得条件信号能够以多尺度方式影响去噪过程，而非仅在输入端施加影响。

**3. 训练损失约束：引入实体掩码**

基线方法通常对整个帧计算损失，未区分前景实体与背景。DragAnything 引入掩码 $\mathbf{M}$，使 MSE 损失仅反向传播于目标实体区域：

$$\mathcal{L}_{\theta} = \sum_{i=1}^L \mathbf{M} \| \epsilon - \epsilon_{\theta}(\mathbf{x}_{t,i}, \mathcal{E}_{\theta}(\hat{\mathbf{E}}_i), \mathcal{E}_{\theta}(\mathbf{G}_i)) \|_2^2$$

这一设计迫使模型专注于学习目标实体的运动模式，减少对背景和非目标区域的干扰。消融实验（Table 3）表明，引入损失掩码将 ObjMC 从 311.1 降至 305.7（越低越好），带来约 5.4 的增益，FVD 和 FID 也有所改善。

### 创新效果的直接证据

Figure 3 的玩具实验直观展示了创新效果：DragNUWA 仅拖拽对应像素区域，导致非目标区域异常变形；而 DragAnything 的实体表示实现了精确的实体级运动控制，前景与背景运动得以分离。在 VIPSeg 验证集上，DragAnything 的 ObjMC 达到 305.7，显著优于 DragNUWA 的 324.6（Table 1）。用户研究中，DragAnything 在运动控制上的人类投票偏好超越 DragNUWA 26%（Figure 8），进一步验证了实体表示在感知质量上的优势。



![[assets/figures/papers/paper_list_l26_DragAnything_Motion_Control_for_Anything_using_Entity_Representation/figures/004_Figure_4.jpg]]
*Figure 4: DragAnything Framework. The architecture includes two parts: 1) Entity Semantic Representation Extraction. Latent features from the Diffusion Model are extracted based on entity mask indices to serve as corresponding entity representations. 2) Main Framework for DragAnything. Utilizing the corresponding entity representations and 2D Gaussian representations to control the motion of entities*

DragAnything 的整体架构围绕一个核心设计原则展开：**用实体的语义表示替代像素/区域表示，作为运动控制的条件信号**。这一设计直接回应了现有方法的瓶颈——单点轨迹或像素区域无法捕获实体的完整语义，导致拖拽操作仅影响局部像素，而非整个目标实体（见图3的玩具实验验证）。

### 架构总览

如图4所示，DragAnything 的 pipeline 由两条并行的条件信号提取路径和一个主生成框架组成：

1. **实体语义表示提取（Entity Semantic Representation Extraction）**：从第一帧的扩散特征中，依据实体掩码的坐标索引提取对应位置的语义嵌入，然后将这些嵌入按轨迹序列点插入到零矩阵中，形成实体表示 $\hat{\mathbf{E}}_i$。
2. **2D 高斯表示提取（2D Gaussian Representation Extraction）**：根据实体内切圆中心坐标 $(x, y)$ 和半径 $r$ 生成 2D 高斯分布图 $\mathbf{G}_i$，使靠近中心的像素获得更高权重，从而强调实体的核心区域。
3. **主生成框架**：将上述两种表示分别通过编码器 $\mathcal{E}$（四层卷积，下采样至 1/8 分辨率）编码后，与视频潜噪声 $\mathbf{Z}_i$ 相加，得到去噪 3D U-Net 的输入特征 $\mathbf{R}_i$。该 3D U-Net 采用 ControlNet 风格设计，将条件特征注入到基础模型 SVD 的去噪 3D U-Net 的解码器块中。

### 输入输出与数据流

**输入条件信号 $c$** 包含三类信息（Section 3.1）：
- 轨迹点序列：定义实体的运动路径
- 视频第一帧：提供实体的外观和空间上下文
- 第一帧的实体掩码：标识目标实体的空间范围

**数据流**：
1. 将第一帧输入去噪扩散模型，提取潜在扩散特征 $\mathcal{F} = \epsilon_\theta(\mathbf{x}_t, t)$（Eq. 1）。
2. 利用实体掩码的坐标索引从 $\mathcal{F}$ 中提取实体语义嵌入，并沿轨迹点位置插入，得到 $\hat{\mathbf{E}}_i$。
3. 同时生成 2D 高斯图 $\mathbf{G}_i$。
4. 两者经编码器 $\mathcal{E}$ 编码后与潜噪声 $\mathbf{Z}_i$ 融合：$\{\mathbf{R}_i\}_{i=1}^L = \mathcal{E}(\{\hat{\mathbf{E}}_i\}_{i=1}^L) + \mathcal{E}(\{\mathbf{G}_i\}_{i=1}^L) + \{\mathbf{Z}_i\}_{i=1}^L$（Eq. 2）。
5. $\mathbf{R}_i$ 作为条件输入到 SVD 的去噪 3D U-Net 中，引导视频生成。

### 训练策略

训练数据从视频分割基准（VIPSeg）中自动构建（Figure 5）：对每个实体计算其掩码的内切圆，获取中心坐标和半径，再用 Co-Tracker 预测中心点的运动轨迹作为真实轨迹。训练损失采用掩码约束的 MSE 损失（Eq. 3），**仅对目标实体区域进行反向传播**，避免背景和非目标区域的干扰：

$$\mathcal{L}_{\theta} = \sum_{i=1}^L \mathbf{M} \| \epsilon - \epsilon_{\theta}(\mathbf{x}_{t,i}, \mathcal{E}_{\theta}(\hat{\mathbf{E}}_i), \mathcal{E}_{\theta}(\mathbf{G}_i)) \|_2^2$$

消融实验证实（Table 3），引入损失掩码 $\mathbf{M}$ 使 ObjMC 从 311.1 降至 305.7，带来了约 5.4 的增益。

### 模块间的因果机制

实体表示与 2D 高斯表示之间存在明确的互补关系：实体表示提供**语义层面的身份信息**（“这是什么物体”），而 2D 高斯图提供**空间注意力引导**（“物体的核心在哪里”）。消融实验（Table 2）表明，单独使用任一种表示均不如两者组合——组合方案取得了最优 ObjMC 305.7。这一结果验证了语义定位与空间聚焦协同作用的必要性。



### 1. 任务形式化

DragAnything 将运动控制视频生成建模为条件去噪过程。核心目标是学习一个条件去噪自编码器 $\epsilon_{\theta}(z, c)$，其中条件信号 $c$ 包含三类信息：轨迹点序列、视频首帧、以及首帧的实体掩码。给定这些条件，模型从纯噪声出发逐步去噪，生成符合指定运动轨迹的视频帧序列。

### 2. 实体语义表示提取

这是 DragAnything 区别于现有方法的核心模块。现有方法（如 DragNUWA、MotionCtrl）使用单个像素坐标或像素区域来表示被控制的目标，但如图 3 的玩具实验所示，物体上的单个点无法代表整个实体的语义，导致拖拽仅影响局部像素区域，产生异常形变。

DragAnything 的解决方案是直接从去噪扩散模型的潜特征中提取实体的语义嵌入：

**步骤一：扩散特征提取**
给定首帧的噪声潜变量 $\mathbf{x}_t$ 和时间步 $t$，通过去噪 U-Net 提取中间层潜特征：
$$\mathcal{F} = \epsilon_{\theta}(\mathbf{x}_t, t)$$
其中 $\mathcal{F} \in \mathbb{R}^{H \times W \times C}$ 是包含丰富语义信息的扩散特征图。

**步骤二：实体嵌入索引**
利用首帧实体掩码的坐标索引，从 $\mathcal{F}$ 中提取对应位置的语义特征，得到实体嵌入向量。这些嵌入向量捕获了实体的完整语义表征，而非孤立的像素信息。

**步骤三：轨迹序列插入**
初始化一个全零矩阵 $\mathbf{E} \in \mathbb{R}^{H \times W \times C}$，然后根据轨迹序列点将实体嵌入插入到对应位置，形成沿轨迹分布的实体表示序列 $\{\hat{\mathbf{E}}_i\}_{i=1}^L$，其中 $L$ 为视频帧数。

### 3. 2D 高斯图表示

为弥补实体表示对中心区域关注不足的问题，DragAnything 同时引入 2D 高斯图表示。具体做法是：根据实体内切圆中心坐标 $(x, y)$ 和半径 $r$，沿轨迹生成 2D 高斯分布图序列 $\{\mathbf{G}_i\}_{i=1}^L$。高斯图中越靠近中心的像素权重越大，从而强化对实体核心区域的注意力。

消融实验（Table 2）证实：单独使用实体表示或单独使用 2D 高斯图，其物体运动控制精度（ObjMC）均不如两者组合——组合方案取得了最优 ObjMC 305.7。

### 4. 条件注入与特征融合

实体表示和 2D 高斯图通过一个编码器 $\mathcal{E}$（由四个卷积块组成，将特征下采样至 1/8 分辨率）编码后，与视频潜噪声 $\{\mathbf{Z}_i\}_{i=1}^L$ 相加，得到去噪 3D U-Net 的输入特征：
$$\{\mathbf{R}_i\}_{i=1}^L = \mathcal{E}(\{\hat{\mathbf{E}}_i\}_{i=1}^L) + \mathcal{E}(\{\mathbf{G}_i\}_{i=1}^L) + \{\mathbf{Z}_i\}_{i=1}^L$$

其中 $\mathbf{R}_i$ 作为条件信号注入到 Stable Video Diffusion（SVD）基础模型的去噪 3D U-Net 解码器块中，采用类似 ControlNet 的注入方式。

### 5. 掩码损失函数

为减少对背景和非目标区域的干扰，DragAnything 引入掩码 $\mathbf{M}$ 约束 MSE 损失的反向传播范围：
$$\mathcal{L}_{\theta} = \sum_{i=1}^L \mathbf{M} \left\| \epsilon - \epsilon_{\theta}\left(\mathbf{x}_{t,i}, \mathcal{E}_{\theta}(\hat{\mathbf{E}}_i), \mathcal{E}_{\theta}(\mathbf{G}_i)\right) \right\|_2^2$$

其中 $\mathbf{M}$ 为目标实体区域的二值掩码，使得损失仅在实体区域进行优化。消融实验（Table 3）表明，引入损失掩码将 ObjMC 从 311.1 降至 305.7（降低约 5.4），FVD 和 FID 也有相应改善。



## 实验与关键发现

### 评估协议与基准

DragAnything 在 **VIPSeg** 视频分割验证集上评估，所有视频统一缩放至 **256×256** 分辨率、采样 **14 帧**。评估指标涵盖视频质量与运动控制精度两个维度：

- **FID**（Fréchet Inception Distance）：衡量单帧图像质量。
- **FVD**（Fréchet Video Distance）：衡量视频时序连贯性。
- **ObjMC**（Object Motion Control）：以欧氏距离定量衡量目标实体实际运动轨迹与给定轨迹之间的偏差，值越低表示运动控制越精确。

用户研究则通过人类投票评估运动控制精度与视频质量，参与者从给定轨迹与生成视频的匹配程度和视觉质量两个维度进行偏好选择。

### 主实验结果

与 DragNUWA（Yin et al., arXiv 2023）的定量对比结果见 Table 1。由于 MotionCtrl（Wang et al., arXiv 2023）等同期工作未发布基于 Stable Video Diffusion（SVD）的开源代码，公平比较仅限 DragNUWA，所有方法使用相同的轨迹输入与评估协议。

![[assets/figures/papers/paper_list_l26_DragAnything_Motion_Control_for_Anything_using_Entity_Representation/figures/007_Table_1.jpg]]
*Table 1: Performance Comparison on VIPSeg val 256 × 256 [30]. We only compared against DragNUWA, as other relevant works (e.g., Motionctrl [42]) did not release source code based on SVD [3]. Fig. 7. Visualization Comparison with DragNUWA. DragNUWA leads to distortion of appearance (first row), out-of-control sky and ship (third row), incorrect camera motion (fifth row), while DragAnything enables precise control of motion*

**Table 1 核心结论**：DragAnything 在所有指标上均显著优于 DragNUWA。

| 指标 | DragNUWA | DragAnything | 提升 |
|------|----------|-------------|------|
| FID ↓ | 39.8 | **33.5** | -6.3 |
| FVD ↓ | 519.3 | **494.8** | -24.5 |
| ObjMC ↓ | 324.6 | **305.7** | -18.9 |

- **视频质量**：FID 降低 6.3，表明单帧生成质量明显更优；FVD 降低 24.5，反映时序一致性显著改善。
- **运动控制精度**：ObjMC 降低 18.9，证实实体表示能更精确地驱动目标运动，减少对背景和非目标区域的误扰。

定性对比（Figure 7）进一步揭示了 DragNUWA 的典型失效模式：第一行出现外观失真，第三行天空与船只运动失控，第五行产生错误的相机运动。DragAnything 则在这些场景下实现了精确的实体级运动控制。

**用户研究**（Figure 8）显示，DragAnything 在运动控制精度上的人类投票偏好超越 DragNUWA **26%**，在视频质量维度同样取得优势，与定量指标相互印证。

![[assets/figures/papers/paper_list_l26_DragAnything_Motion_Control_for_Anything_using_Entity_Representation/figures/008_Figure_8.jpg]]
*Figure 8: User Study for Motion Control and Video Quality. DragAnything achieved superior performance in terms of motion control and video quality*

### 消融实验

**实体表示与 2D 高斯图的组合效应**（Table 2）

![[assets/figures/papers/paper_list_l26_DragAnything_Motion_Control_for_Anything_using_Entity_Representation/figures/009_Table_2.jpg]]
*Table 2: Ablation for Entity and 2D Gaussian Representation. The combination of the both yields the greatest benefit. Table 3. Ablation Study for Loss Mask M. Loss mask can bring certain gains, especially for the ObjMC metric*

| 配置 | ObjMC ↓ |
|------|---------|
| 仅实体表示 | 高于 305.7 |
| 仅 2D 高斯图 | 高于 305.7 |
| 实体表示 + 2D 高斯图 | **305.7** |

单独使用实体表示或 2D 高斯图均无法达到最优运动控制精度，两者组合产生最大增益。因果机制在于：实体表示提供完整语义特征以区分目标与背景，2D 高斯图则通过中心加权强化实体核心区域的响应，抑制边缘噪声。

**损失掩码 M 的效应**（Table 3）

| 配置 | ObjMC ↓ | FVD ↓ | FID ↓ |
|------|---------|-------|-------|
| 无掩码 | 311.1 | — | — |
| 有掩码 M | **305.7** | 改善 | 改善 |

引入损失掩码 M 使 ObjMC 降低约 5.4，FVD 和 FID 也同步改善。掩码将 MSE 损失的反向传播限制在目标实体区域，避免背景和非目标区域对运动控制信号的干扰，从而提升控制精度与生成质量。

### 失败模式分析

尽管 DragAnything 在实体级运动控制上表现优异，仍存在以下失效场景（Figure 10）：

- **大范围运动控制**：当轨迹跨度较大或运动速度较快时，生成视频可能出现外观失真，目标实体形状和纹理无法保持稳定。
- **深度旋转与 3D 姿态变化**：当前实体表示仅支持 2D 轨迹，无法处理身体旋转等涉及深度维度的运动，限制了在复杂 3D 场景中的应用。
- **遮挡与语义模糊**：实体掩码依赖交互式分割模型 SAM 获取，对于严重遮挡或语义边界模糊的实体，掩码质量下降会直接影响实体表示提取的准确性。

### 多类型运动控制能力

Figure 9 展示了 DragAnything 支持多样化的运动控制模式，包括前景物体运动、背景运动以及相机运动，表明实体表示框架具备良好的泛化性，不局限于单一运动类型。

### 补充图表

![[assets/figures/papers/paper_list_l26_DragAnything_Motion_Control_for_Anything_using_Entity_Representation/figures/003_Figure_3.jpg]]
*Figure 3: (a) Insight 1: The points on the object cannot represent the entity (b) Insight 2: Pixels closer to the drag point receive a greater influence Fig. 3. Toy experiment for the motivation of Entity Representation. Existing methods (DragNUWA [49] and MotionCtrl [42]) directly drag pixels, which cannot precisely control object targets, whereas our method employs entity representation to achieve precise control*

![[assets/figures/papers/paper_list_l26_DragAnything_Motion_Control_for_Anything_using_Entity_Representation/figures/011_Figure.jpg]]
*Figure: demonstrate that our DragAnything achieves SOTA performance for User Study, surpassing the previous state of the art (DragNUWA) by 26% in human voting*



## 定位与知识库关联

### 问题定位：从像素拖拽到实体语义控制

现有基于轨迹的运动控制方法，如 **DragNUWA**（Yin et al., arXiv 2023）和 **MotionCtrl**（Wang et al., arXiv 2023），其核心瓶颈在于**目标表示粒度不足**：它们使用单个轨迹点、轨迹向量图或边界框来表示被控物体，本质上仍是像素级或区域级的操作。这种表示无法捕获实体的完整语义，导致拖拽仅影响局部像素区域，而非整个目标实体——例如拖拽汽车的一个角点时，只有该角点附近的像素发生移动，车身其余部分可能静止或产生异常形变（图3玩具实验验证了这一现象）。

DragAnything 的因果调节变量是将**目标表示**从像素/区域级升级为**实体语义嵌入**：从去噪扩散模型（SVD）第一帧的潜特征中，利用实体掩码索引提取对应语义特征，并将其与2D高斯图融合后作为条件信号注入基础视频生成模型。这一设计使得运动控制信号直接作用于实体的语义表征，从而实现了前景与背景运动的解耦和精确的实体级运动控制。

### 方法谱系中的位置

在可控视频生成的运动控制子领域中，DragAnything 处于**基于轨迹的扩散条件控制**这一技术路线，其与相关工作的关系如下：

- **上游基础模型**：DragAnything 直接继承 **Stable Video Diffusion（SVD）** 的架构与预训练权重，利用其强大的视频先验来保证生成质量。这与 DragNUWA 基于 SVD 的路线一致，但 MotionCtrl 当时未发布基于 SVD 的代码，因此无法直接定量比较。

- **同级方法对比**：
  - **DragNUWA** 使用轨迹点生成密集光流作为条件，本质是像素级运动场控制。DragAnything 将其替换为实体语义嵌入，在 VIPSeg 验证集上 FID 从 39.8 降至 33.5，FVD 从 519.3 降至 494.8，物体运动控制精度 ObjMC 从 324.6 降至 305.7（数值越低越好）。
  - **MotionCtrl** 使用轨迹坐标向量图，同样受限于像素级表示。
  - **TrailBlazer**（Ma et al., arXiv 2024）使用边界框表示，虽然比单点更丰富，但仍无法捕获实体内部语义。

- **技术组件来源**：实体掩码通过交互式分割模型 SAM 获取，运动轨迹通过 Co-Tracker 预测，条件注入方式沿用了 ControlNet 的设计范式（将编码后的条件特征注入去噪 3D U-Net 的解码器块）。

### 关键设计消融与证据强度

| 消融项 | ObjMC 变化 | 证据强度 |
|--------|-----------|---------|
| 仅实体表示 vs. 实体+2D高斯 | 组合获得最优 ObjMC 305.7 | 高（Table 2） |
| 无损失掩码 M vs. 有损失掩码 M | ObjMC 从 311.1 降至 305.7（提升约 5.4） | 高（Table 3） |

实体表示与2D高斯图的组合是性能最优的关键：实体表示提供语义完整性，2D高斯图则通过中心加权强化对实体核心区域的关注，避免边缘噪声干扰。损失掩码 M 进一步将 MSE 损失约束在目标实体区域，减少对背景和非目标区域的误优化。

### 适用边界与局限

1. **大范围/快速运动失稳**：当运动幅度较大或速度较快时，生成视频可能出现外观失真（图10失败案例），这是当前 SVD 基础模型能力的上限。

2. **仅支持2D轨迹控制**：实体表示目前仅限于二维平面轨迹，无法处理深度旋转和3D物体姿态变化（如身体旋转、物体翻转）。这是从2D视频生成模型继承的固有局限。

3. **依赖外部分割模型**：实体掩码的质量依赖于 SAM 的分割精度，对于遮挡严重或语义模糊的实体，掩码误差会直接传导至实体表示提取环节。

4. **定量比较范围有限**：由于其他方法（如 MotionCtrl）未发布基于 SVD 的代码，定量评估仅与 DragNUWA 进行了对比，跨方法泛化性结论需要更多基线验证。

### 开放问题

1. **从2D到3D的轨迹扩展**：如何将深度信息融入二维轨迹，使其扩展为三维轨迹，以支持3D空间中的物体姿态和旋转控制？

2. **更强基础模型的适配**：当更强的视频生成基础模型（如 SORA）可用时，如何迁移实体表示机制以支持更大范围、更鲁棒的运动生成？

3. **多实体交互的一致性**：在多实体复杂交互场景下，如何保持各实体运动的一致性与独立性，避免实体间运动信号的相互干扰？



## 原文 PDF

![[paperPDFs/ECCV_2024/DragAnything_Motion_Control_for_Anything_using_Entity_Representation.pdf]]
