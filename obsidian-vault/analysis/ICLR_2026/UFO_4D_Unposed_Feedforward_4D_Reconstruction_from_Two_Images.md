---
title: "UFO-4D: Unposed Feedforward 4D Reconstruction from Two Images"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/UFO_4D_Unposed_Feedforward_4D_Reconstruction_from_Two_Images_f4891bdea6ab.pdf
project_link: "https://ufo-4d.github.io/"
code_link: null
aliases:
- U4
- UFO-4D
tags:
- ICLR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
core_operator: 采用动态3D高斯泼溅(D-3DGS)作为统一表示，通过可微分渲染同时输出图像、稠密点云和场景流，将多任务损失紧密耦合。
primary_logic: 核心洞察在于：从单一动态3D高斯表示可微分地渲染多种信号，能带来显著的训练优势（包括自监督光度损失和跨模态正则化）。
claims:
- UFO-4D在Stereo4D和KITTI上的场景流和几何精度超过最强基线3倍以上。
- 消融实验表明，移除光度损失梯度或移除渲染点云/运动损失均导致几何和运动精度大幅下降。
- 统一动态3D高斯表示在Stereo4D和KITTI上全面超越逐像素表示，证明了耦合表示的优势。
- 前馈位姿估计比PnP+RANSAC方案准确约16.6%，且几何质量也优于其他方法。
---

# UFO-4D: Unposed Feedforward 4D Reconstruction from Two Images

> [!tip] 核心洞察
> 核心洞察在于：从单一动态3D高斯表示可微分地渲染多种信号，能带来显著的训练优势（包括自监督光度损失和跨模态正则化）。

| 字段 | 内容 |
|------|------|
| 中文题名 | UFO-4D：基于双图的无姿态前馈4D重建 |
| 英文题名 | UFO-4D: Unposed Feedforward 4D Reconstruction from Two Images |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=8gDDWqO59H) · [Project](https://ufo-4d.github.io/) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction |
| Method | UFO-4D |
| Dataset | Stereo4D, KITTI, Bonn |

> [!tip] 效果简介
> - Stereo4D 上，Pointmap EPE (↓) 0.659 vs 0.811 (DynaDUSt3R) (-0.152)；Scene flow EPE3D forward (↓) 0.049 vs 0.175 (DynaDUSt3R) (-0.126)；ATE (↓) 0.0101 vs 0.0458 (MonST3R) (-0.0357)。
> - KITTI 上，Scene flow EPE3D forward (↓) 0.137 vs 0.463 (DynaDUSt3R) (-0.326)。
> - Bonn 上，Pointmap EPE (↓) 0.162 vs 0.181 (St4RTrack) (-0.019)。

## 概要

从两帧无姿态图像中重建完整的4D（3D几何+运动）动态场景是计算机视觉的核心难题。现有方法面临三大瓶颈：**缺乏统一的显式4D表示**——逐像素的点云和运动向量彼此解耦，无法利用多模态信号间的正正则化；**训练数据稀疏且标注不完整**——真实世界的动态标注数据稀缺且含噪（如Stereo4D数据集中静态区域存在非零运动标注，Figure D）；**相机位姿依赖后处理**——基于PnP+RANSAC的方案对噪声敏感，且无法与重建网络端到端联合优化。

**UFO-4D** 提出了一种统一的前馈框架，核心洞察在于：**从单一动态3D高斯泼溅（Dynamic 3DGS）表示出发，通过可微分渲染同时输出图像、稠密点云和场景流，将多任务损失紧密耦合**。这一设计将原本孤立的几何、运动和位姿估计统一为同一个显式4D表示的学习问题，带来两方面的训练优势：（1）自监督光度损失通过可微渲染提供稠密的像素级监督信号，弥补稀疏标注的不足；（2）渲染的点云和运动损失构成跨模态正则化，迫使高斯属性在几何和运动上保持一致性。

方法层面，UFO-4D以两帧图像和相机内参为输入，通过共享权重的ViT编码器和含交叉注意力的ViT解码器，前馈预测每个像素对应的动态3D高斯参数（中心、速度、旋转、尺度、球谐系数、不透明度）以及相对相机位姿。可微4D光栅化器将这些高斯渲染为任意时刻的图像、点云和场景流（Figure 3），使整个系统端到端可训练。相机位姿由网络直接预测，相比PnP+RANSAC方案准确率提升约16.6%（Table G）。

实验表明，UFO-4D在Stereo4D和KITTI数据集上的场景流和几何精度**超过最强基线3倍以上**：Stereo4D上场景流EPE从0.175降至0.049，KITTI上从0.463降至0.137（Table 2）；点云EPE从0.811降至0.659（Table 1）。消融实验证实，移除光度损失梯度或移除渲染点云/运动损失均导致精度大幅下降（Table 4），验证了统一渲染框架的关键作用。

**方法谱系与知识库定位**：UFO-4D继承了两条技术路线——基于高斯泼溅的可微分渲染（3DGS, Kerbl et al., SIGGRAPH 2023）和基于ViT的前馈3D重建（**MASt3R**, Leroy et al., 2024）。相较于逐像素表示的动态重建基线**DynaDUSt3R**（Jin et al., 2025）和**MonST3R**（Zhang et al., 2025a），UFO-4D首次将动态3DGS引入前馈框架，实现了几何、运动和位姿的联合估计。与多帧场景流方法**ZeroMSF**（Liang et al., 2025b）和同时跟踪重建方法**St4RTrack**（Feng et al., 2025）相比，UFO-4D仅需两帧即可输出显式4D表示，且运动边界更清晰、静态区域残差运动更少（Figure 4, Figure A-C）。

当前方法仍存在局限：仅支持双帧输入，扩展到长序列面临线性内存增长问题；假设线性运动，难以处理非线性动态；在Bonn等纹理缺乏区域因高斯重叠导致精度略低于逐像素表示（Table 1, Figure F）。这些方向值得后续探索。

从二维图像恢复三维世界是计算机视觉的核心目标。近年来，基于前馈网络（feedforward）的静态场景重建取得了显著进展，仅需少量无姿态图像即可直接输出三维几何。然而，现实世界是动态的——物体在运动、相机在移动，将这些方法扩展到**动态4D场景**（3D几何 + 3D运动）仍面临根本性挑战。

### 现有方法的缺口

当前主流的动态场景重建方法存在三类结构性缺陷：

**1. 缺乏统一的显式4D表示。** 现有方法多采用**逐像素的点云和运动向量**作为输出（如 **DynaDUSt3R**（Jin et al., 2025）、**MonST3R**（Zhang et al., 2025a）），每个像素独立估计几何和运动，缺乏显式的表面连接。这种碎片化表示难以在训练中引入跨模态的正则化，也无法自然地支持新视角、新时刻的稠密渲染。相比之下，**动态3D高斯泼溅（Dynamic 3DGS）** 提供了连续、可微的4D场景表示，但此前未被用于前馈式的无姿态4D重建任务。

**2. 监督信号稀疏且标注不完整。** 动态场景的真实标注数据（如稠密点云和场景流）获取成本极高。以 **Stereo4D**（Jin et al., 2025）为例，虽是目前最大规模的动态标注数据集，其标注仍存在噪声——例如静态区域被错误地赋予非零运动（见Figure D）。现有方法仅依赖这些稀疏标注进行监督，缺乏利用原始图像信号进行自监督的能力。

**3. 相机位姿估计依赖后处理。** 无姿态重建方法通常需要先估计点云，再通过 **PnP+RANSAC** 等迭代求解器计算相机位姿。这种后处理方案对点云噪声敏感，且与重建网络解耦，无法端到端优化，限制了整体精度。

### 核心动机与洞察

本文的核心洞察在于：**从单一的动态3D高斯表示出发，通过可微分渲染同时输出图像、稠密点云和场景流，能够将多任务损失紧密耦合，带来显著的训练优势。** 具体而言：

- **自监督光度损失**：渲染的图像与原始输入之间的光度误差，为几何和运动估计提供稠密的像素级监督信号，弥补稀疏标注的不足。
- **跨模态正则化**：点云和场景流的渲染损失迫使高斯属性（位置、速度）与图像重建目标保持一致，形成多任务协同优化的正反馈回路。
- **端到端位姿估计**：在位姿与表示联合优化的框架下，网络可以直接预测相对相机位姿，替代噪声敏感的后处理方案。

基于这一洞察，**UFO-4D** 提出了一种统一的**无姿态前馈4D重建方法**：输入两张无姿态图像，直接输出动态3D高斯集合和相对相机位姿。该显式4D表示可同时支撑三维几何（点云、深度）、三维运动（场景流、光流）以及任意时刻/视角的图像渲染（Figure 1），并通过对渲染信号的自监督训练，在标注稀缺的条件下实现高精度重建。

## 核心方法与创新机理

UFO-4D的核心创新在于将动态3D高斯泼溅（Dynamic 3DGS）确立为统一的显式4D场景表示，并围绕该表示构建了一个端到端的前馈重建框架。相较于现有方法，这一选择在三个关键维度上形成了根本性的变革：

### 1. 从逐像素表示到统一动态高斯表示

现有方法普遍采用逐像素的点云和运动向量表示（如 **DynaDUSt3R** (Jin et al., 2025)、**MonST3R** (Zhang et al., 2025a)），每个像素独立估计其3D坐标和运动，缺乏显式的表面连接和空间连续性约束。UFO-4D转而采用动态3D高斯泼溅作为统一表示，每个高斯原语携带中心位置 $\boldsymbol{\mu}$、速度 $\mathbf{v}$、旋转 $\mathbf{r}$、尺度 $\mathbf{s}$、球谐系数 $\mathbf{h}$ 和不透明度 $o$ 等属性，天然具备空间连续性和尺度感知能力。

这一表示切换带来了因果性的性能提升：统一的高斯表示使得模型可以通过可微分渲染同时输出图像、稠密点云和场景流三种信号，从而将多任务损失紧密耦合。消融实验（Table 5）证实，在相同训练协议下，动态3D高斯表示在Stereo4D和KITTI上全面超越逐像素表示，仅在Bonn数据集上因纹理缺乏区域的高斯重叠问题而略逊一筹。

### 2. 从纯稀疏监督到半监督渲染框架

现有方法（如 **DynaDUSt3R**、**ZeroMSF** (Liang et al., 2025b)）的监督信号主要依赖稀疏标注的几何和运动真值，受限于标注数据的稀缺性和噪声（如Stereo4D数据集中静态区域存在非零运动标注噪声，见Figure D）。UFO-4D的核心洞察在于：从单一动态3D高斯表示可微分地渲染多种信号，能带来显著的训练优势。

具体而言，UFO-4D引入了自监督光度损失 $\mathcal{L}_{\mathrm{photo}}$ 和边缘感知平滑损失 $\mathcal{L}_{\mathrm{smooth}}$，通过可微4D光栅化器将渲染图像与输入图像进行对比，形成稠密的像素级监督信号。损失消融（Table 4）揭示了这一设计的决定性作用：移除光度损失梯度（即禁用图像合成损失对高斯参数的反向传播）导致点云EPE从0.827升至0.903，运动EPE从0.069升至0.072；而完全移除渲染点云和运动损失则造成灾难性退化，运动光栅化EPE从0.064飙升至0.9以上，图像PSNR从23.929骤降至20.675。

### 3. 从后处理位姿求解到前馈位姿估计

现有方法（如 **MonST3R**、**St4RTrack** (Feng et al., 2025)）普遍采用PnP+RANSAC后处理步骤从估计的点云中求解相机位姿，这一过程不仅引入额外的计算开销，还对点云噪声高度敏感。UFO-4D在网络中直接集成了前馈位姿预测头，通过可学习的位姿token与图像特征进行交叉注意力交互，直接输出相对相机位姿 $\mathbf{P}$。

实验表明（Table G），前馈位姿估计比PnP+RANSAC方案准确约16.6%，且几何质量也优于其他方法。注意力可视化（Figure G）进一步揭示了其工作机制：位姿token在特定解码器层（第8、11、12层）倾向于关注静态区域的图像token，自动学习忽略运动物体以获取可靠的位姿估计线索。

UFO-4D 是一个从**两帧无姿态图像**中直接进行前馈式4D重建的统一框架。其核心设计在于：将整个重建过程建模为一个从图像对到**动态3D高斯泼溅（Dynamic 3DGS）**和**相对相机位姿**的端到端映射，而非分步处理几何、运动与位姿。

### 输入输出定义

给定时间相邻的两帧图像 $\mathbf{I}_t$ 和 $\mathbf{I}_{t+1}$ 及其已知相机内参 $\mathbf{K}$，模型直接输出：

$$
f_{\theta}(\mathbf{I}_t, \mathbf{I}_{t+1}) \mapsto (\mathcal{G}, \mathbf{P})
$$

其中 $\mathcal{G}$ 是定义在规范空间中的动态3D高斯集合，每个高斯由中心位置 $\boldsymbol{\mu}$、速度向量 $\mathbf{v}$、旋转四元数 $\mathbf{r}$、各向异性尺度 $\mathbf{s}$、球谐系数 $\mathbf{h}$ 和不透明度 $o$ 组成；$\mathbf{P}$ 是两帧之间的相对相机位姿。高斯来源于两帧图像的所有像素，即 $\mathbf{p} \in \mathcal{D}(\mathbf{I}_t) \cup \mathcal{D}(\mathbf{I}_{t+1})$。

### 流水线模块

整个前馈流水线由四个关键模块串联构成（图2）：

1. **共享权重ViT编码器**：对两帧输入图像分别提取特征token，独立处理以保留各自的空间信息。

2. **ViT解码器（含交叉注意力）**：融合两帧特征，同时接收相机内参token和可学习的位姿token。交叉注意力机制使两帧信息在解码过程中充分交互，位姿token在此阶段逐步聚合可靠的静态区域线索用于位姿估计。

3. **属性预测头**：从解码特征中并行预测每个像素对应的高斯参数（中心、速度、旋转、尺度、球谐系数、不透明度）以及相对相机位姿。位姿头直接输出位姿参数，无需PnP+RANSAC等后处理步骤。

4. **可微4D光栅化器**：这是框架的核心创新环节。给定任意时刻 $t'$，先将高斯沿速度方向平移得到 $\mathcal{G}(t')$：

   $$
   \mathcal{G}(t') = \{ (\boldsymbol{\mu} + \Delta t \cdot \mathbf{v}, \mathbf{v}, \mathbf{r}, \mathbf{s}, \mathbf{h}, \mathbf{c}, o)_{\mathbf{p}} \}
   $$

   然后通过统一的α混合光栅化，**同时渲染**出三种输出信号（图3b）：
   - **RGB图像**：标准颜色渲染 $\hat{\mathbf{I}}_{t'}(\mathbf{p}) = \sum_{i} \mathbf{c}_i o_i \prod_{j=1}^{i-1} (1 - o_j)$
   - **稠密3D点云**：以高斯中心替代颜色作为属性渲染 $\mathbf{X}_{t'}(\mathbf{p}) = \sum_{i} \boldsymbol{\mu}_i o_i \prod_{j=1}^{i-1} (1 - o_j)$
   - **稠密3D场景流**：以高斯速度替代颜色作为属性渲染 $\mathbf{V}_{t'}(\mathbf{p}) = \sum_{i} \mathbf{v}_i o_i \prod_{j=1}^{i-1} (1 - o_j)$

### 设计动机与因果机制

框架的核心洞察在于：**从单一动态3D高斯表示可微分地渲染多种信号，能带来显著的训练优势**。传统方法（如**DynaDUSt3R**，Jin et al., 2025）采用逐像素点云表示，各像素独立预测，缺乏显式的表面连接，监督信号也仅限于稀疏标注的几何和运动损失。UFO-4D通过统一的显式表示，实现了两个关键的因果耦合：

- **跨模态正则化**：渲染的点云和场景流必须与渲染的图像在几何上一致，这种隐式约束迫使高斯的位置和速度预测更加准确。
- **自监督光度损失**：渲染图像与输入图像的差异通过可微光栅化反向传播梯度到高斯参数，提供了稠密的像素级监督信号，有效缓解了标注数据稀疏的问题。

总损失函数将监督损失和自监督损失紧密结合：

$$
\mathcal{L}_{\mathrm{total}} = \mathcal{L}_{\mathrm{sup}} + \mathcal{L}_{\mathrm{self}}
$$

其中 $\mathcal{L}_{\mathrm{sup}} = L_{\mathrm{motion}} + w_{\mathrm{point}} L_{\mathrm{point}} + w_{\mathrm{pose}} L_{\mathrm{pose}}$ 利用稀疏标注监督运动、点云和位姿；$\mathcal{L}_{\mathrm{self}} = L_{\mathrm{photo}} + w_{\mathrm{smooth}} L_{\mathrm{smooth}}$ 通过渲染图像的光度一致性和边缘感知平滑损失提供自监督信号。

### 与基线方法的关键差异

| 维度 | 基线方法 | UFO-4D |
|------|---------|--------|
| 场景表示 | 逐像素点云和运动向量（无明确表面连接） | 统一动态3D高斯泼溅（显式表面表示） |
| 监督信号 | 仅稀疏标注的几何和运动损失 | 半监督：稀疏标注损失 + 自监督光度损失及平滑损失 |
| 位姿估计 | PnP+RANSAC后处理 | 网络直接前馈预测 |

消融实验（Table 4）证实了这一设计的有效性：移除光度损失梯度导致点云和运动精度显著下降；移除渲染点云和运动损失则使所有任务严重退化，运动边界模糊。架构对比（Table 5）进一步表明，动态3D高斯表示在Stereo4D和KITTI上全面超越逐像素表示，验证了耦合表示的优势。

### 不透明度作为可学习置信度

框架中一个值得注意的机制是不透明度的双重作用：除了参与α混合渲染外，不透明度还充当了**可学习的置信度**。在（去）遮挡场景中（图5），模型学会对去遮挡区域分配高不透明度（高置信度），而对两帧共视区域只选择来自某一帧的对应高斯，从而构建出高效紧凑的4D表示。这一机制使得模型能够自动处理遮挡歧义，无需显式的遮挡推理模块。

UFO-4D 的核心设计是将双图输入映射为一个统一的显式4D表示——动态3D高斯泼溅（Dynamic 3DGS），并通过可微渲染同时输出多模态信号，实现端到端的联合优化。整个pipeline由四个关键模块串联构成。

### 1. 共享权重ViT编码器与交叉注意力解码器

网络架构如 Figure 2 所示。两张输入图像 $\mathbf{I}_t$ 和 $\mathbf{I}_{t+1}$ 首先分别经过**共享权重的ViT编码器**，独立提取各自的图像特征token。随后，**ViT解码器**通过交叉注意力机制融合两帧信息，同时处理相机内参token和可学习的位姿token，为后续的多任务预测提供统一的特征表示。

![[assets/figures/papers/paper_list_l32_https_openreview_net_forum_id_8gDDWqO59H/figures/002_Figure_2.jpg]]
*Figure 2: Network architecture. Given a pair of input images*

### 2. 属性预测头：从像素到动态高斯的映射

解码器输出的特征被送入四个并行的**属性预测头**，为每个像素 $\mathbf{p}$ 预测其对应的动态3D高斯参数。模型的整体映射关系为：

$$f_{\theta}(\mathbf{I}_t, \mathbf{I}_{t+1}) \mapsto (\mathcal{G}, \mathbf{P}), \text{ with } \mathcal{G} = \{ (\boldsymbol{\mu}, \mathbf{v}, \mathbf{r}, \mathbf{s}, \mathbf{h}, o)_{\mathbf{p}} \mid \mathbf{p} \in \mathcal{D}(\mathbf{I}_t) \cup \mathcal{D}(\mathbf{I}_{t+1}) \}$$

其中 $\mathcal{G}$ 为动态高斯集合，每个高斯由以下属性定义：
- $\boldsymbol{\mu}$：高斯中心（3D位置）
- $\mathbf{v}$：速度向量（3D运动）
- $\mathbf{r}$：旋转四元数
- $\mathbf{s}$：各向异性缩放因子
- $\mathbf{h}$：球谐系数（编码视角相关的颜色）
- $o$：不透明度（同时作为可学习的置信度）

$\mathbf{P}$ 为网络直接预测的相对相机位姿（前馈位姿头输出），避免了PnP+RANSAC等后处理步骤。

### 3. 时间演化：线性运动插值

为实现连续时间的4D表示，每个高斯沿其速度方向进行线性平移。在任意时刻 $t' = t + \Delta t$，高斯集合更新为：

$$\mathcal{G}(t') = \{ (\mu + \Delta t \cdot \mathbf{v}, \mathbf{v}, \mathbf{r}, \mathbf{s}, \mathbf{h}, \mathbf{c}, o)_{\mathbf{p}} \}$$

这一过程如 Figure 3a 所示，使得模型能够在任意中间时刻插值出场景状态，支持新视角和新时刻的渲染。

### 4. 可微4D光栅化器：多信号统一渲染

可微光栅化器（Figure 3b）是连接表示与监督的关键模块。对于时刻 $t'$ 上的每个像素 $\mathbf{p}$，沿射线方向对深度排序后的高斯进行 $\alpha$ 混合：

**图像渲染：**
$$\hat{\mathbf{I}}_{t'}(\mathbf{p}) = \sum_{i \in \mathcal{N}_{\mathbf{p}}^{t'}} \mathbf{c}_i o_i \prod_{j=1}^{i-1} (1 - o_j)$$

**稠密点云渲染：**
$$\mathbf{X}_{t'}(\mathbf{p}) = \sum_{i \in \mathcal{N}_{\mathbf{p}}^{t'}} \pmb{\mu}_i o_i \prod_{j=1}^{i-1} (1 - o_j)$$

**稠密场景流渲染：**
$$\mathbf{V}_{t'}(\mathbf{p}) = \sum_{i \in \mathcal{N}_{\mathbf{p}}^{t'}} \mathbf{v}_i o_i \prod_{j=1}^{i-1} (1 - o_j)$$

其核心洞察在于：将高斯属性中的颜色 $\mathbf{c}$ 替换为中心 $\pmb{\mu}$ 或速度 $\mathbf{v}$，使用完全相同的 $\alpha$ 混合权重，即可渲染出稠密的3D点云和3D场景流。这一统一渲染机制是完全可微的，使得自监督光度损失和跨模态正则化的梯度能够反向传播到高斯参数。

### 5. 损失函数：半监督耦合优化

总损失由监督损失和自监督损失两部分组成：

$$\mathcal{L}_{\mathrm{total}} = \mathcal{L}_{\mathrm{sup}} + \mathcal{L}_{\mathrm{self}}$$

**监督损失**利用稀疏标注数据：

$$L_{\mathrm{sup}} = L_{\mathrm{motion}} + w_{\mathrm{point}} L_{\mathrm{point}} + w_{\mathrm{pose}} L_{\mathrm{pose}}$$

**自监督损失**通过可微渲染引入稠密监督：

$$L_{\mathrm{self}} = L_{\mathrm{photo}} + w_{\mathrm{smooth}} L_{\mathrm{smooth}}$$

其中 $L_{\mathrm{photo}}$ 为渲染图像与原始输入之间的光度一致性损失，$L_{\mathrm{smooth}}$ 为边缘感知的平滑正则项。这种半监督框架有效缓解了4D标注数据稀疏的问题——消融实验（Table 4）表明，移除光度损失梯度会导致点云和运动精度显著下降，而移除渲染点云/运动损失则会使所有任务严重退化。

## 实验与关键发现

### 核心定量结果

UFO-4D 在几何估计、运动估计和相机位姿估计三个维度上均取得了显著领先。

**几何估计。** 在 Stereo4D 测试集上，UFO-4D 的点云终点误差（Pointmap EPE）为 0.659，较 **DynaDUSt3R**（Jin et al., 2025）的 0.811 降低了约 18.7%。在 Bonn 数据集上，UFO-4D 的点云 EPE 为 0.162，略优于 **St4RTrack**（Feng et al., 2025）的 0.181（Table 1）。在深度估计指标上，UFO-4D 在所有评测基准上均取得最优的绝对相对误差（Abs. Rel.）和 δ<1.25 准确率，表明其几何重建在全局尺度和局部结构上均具有高保真度。需注意，所有对比方法均采用每张图像的中值尺度对齐协议进行评估，确保了比较的公平性。

**运动估计。** 场景流精度是 UFO-4D 最突出的优势维度。在 Stereo4D 上，UFO-4D 的前向场景流 EPE3D 仅为 0.049，而 **DynaDUSt3R** 为 0.175，降幅超过 3.5 倍；在 KITTI Scene Flow 2015 训练集上，UFO-4D 的前向 EPE3D 为 0.137，**DynaDUSt3R** 为 0.463，降幅超过 3.3 倍（Table 2）。这一结果直接验证了论文的核心主张——“超过最强基线 3 倍以上的 EPE 降低”。**ZeroMSF**（Liang et al., 2025b）和 **St4RTrack** 在运动边界处频繁出现残差运动和模糊估计，而 UFO-4D 展现出清晰的前景/背景运动分离（Figure 4, Figure B）。

**相机位姿估计。** UFO-4D 采用前馈位姿头直接预测相对位姿，无需 PnP+RANSAC 后处理。在 Stereo4D 上，其绝对轨迹误差（ATE）为 0.0101，远优于 **MonST3R**（Zhang et al., 2025a）的 0.0458（Table 3）。与自身使用 PnP+RANSAC 的变体相比，前馈估计器精度提升约 16.6%（Table G），证明端到端学习的位姿头对噪声更具鲁棒性。

### 消融实验：因果机制的实证验证

消融实验系统性地验证了 UFO-4D 两大核心设计——可微渲染多信号和统一动态 3D 高斯表示——的因果作用。

**光度损失梯度的必要性。** Table 4 的损失消融揭示了自监督信号的因果链：(a) 完整模型 vs (b) 移除光度损失梯度（即禁用图像合成损失对高斯参数的反向传播）。移除后，高斯中心点 EPE 从 0.827 升至 0.903，渲染运动 EPE 从 0.069 升至 0.072。这表明光度损失提供的稠密像素级梯度是几何和运动精度的重要驱动力，尤其是在标注稀疏的场景下。

**渲染点云和运动损失的关键性。** 从完整模型 (a) 移除渲染点云和运动损失（只保留逐高斯属性监督）得到配置 (c)，导致图像 PSNR 从 23.929 骤降至 20.675，渲染运动 EPE 从 0.064 恶化至 0.9 以上。这一极端退化说明：仅靠稀疏的逐高斯监督无法约束动态场景的复杂几何和运动，而可微渲染的稠密输出损失是实现高精度的必要条件。定性对比（Figure 6）进一步显示，移除这些损失后运动边界和物体边缘出现明显的模糊和错误。

**统一动态 3D 高斯表示的优势。** Table 5 将 UFO-4D 的动态 3D 高斯表示与逐像素点云表示在相同训练协议下进行了公平对比。结果显示，UFO-4D 在 Stereo4D 和 KITTI 上的点云和运动 EPE 全面优于逐像素表示，仅在 Bonn 上略逊。进一步分析（Table F, Figure H）表明，这一优势来源于两个相互增强的机制：(1) 前馈位姿头提供了更准确的相机位姿估计；(2) 光度损失通过可微渲染为高斯表示提供了稠密的像素级监督，尤其改善了平面区域（如路面）的几何精度。在 Bonn 上的劣势则与纹理缺乏区域的高斯重叠混合误差有关——高斯尺度越大，深度精度越低（Table E）。

**不透明度作为可学习置信度。** Figure 5 可视化了模型在遮挡/去遮挡场景下的不透明度分布：模型学会对去遮挡区域赋予高不透明度（高置信度），而对两帧共视区域仅从某一帧选择对应高斯，从而实现紧凑高效的 4D 表示。这一机制是 UFO-4D 处理遮挡的核心策略。

### 失败模式与局限性

尽管整体性能领先，UFO-4D 存在以下已知失败模式：

1. **纹理缺乏区域的几何退化。** 在 Bonn 数据集的墙壁等纹理缺乏区域，UFO-4D 的几何精度略低于逐像素表示（Table 5, Figure F）。分析表明，纹理缺乏导致模型预测较大尺度的高斯来覆盖大面积均匀区域，但大尺度高斯在深度方向的重叠混合会引入误差（Table E）。这是 3D 高斯表示在无纹理场景下的固有问题。

![[assets/figures/papers/paper_list_l32_https_openreview_net_forum_id_8gDDWqO59H/figures/012_Table_5.jpg]]
*Table 5: Architecture comparison. For apples-to-apples comparison, we train other methods with different output representation on our training protocol. Our method achieves the best accuracy except for Bonn on both point and motion end-point errors (lower the better)*

2. **线性运动假设的局限。** 模型的时间演化公式 $\mathcal{G}(t') = \{ (\mu + \Delta t \cdot \mathbf{v}, \mathbf{v}, \mathbf{r}, \mathbf{s}, \mathbf{h}, \mathbf{c}, o)_{\mathbf{p}} \}$ 假设高斯做匀速直线运动，无法建模非线性运动或加速度变化。在包含快速旋转或非刚性形变的场景中，这一假设可能导致运动估计偏差。

3. **两帧输入的限制。** 当前方法仅处理两帧输入，扩展到长序列时面临线性内存增长和时序一致性问题。这是前馈方法向视频级 4D 重建扩展的核心瓶颈。

4. **遮挡场景的局部错误。** 在强遮挡或极端视角变化时，不透明度置信度机制有时会选择错误的对应高斯，导致局部几何或运动错误。这一失败模式在论文的局限性讨论中被明确指出。

### 训练与评估协议

UFO-4D 采用混合数据集训练：Stereo4D（采样概率 60%）、PointOdyssey（20%）和 Virtual KITTI 2（20%）。网络使用 **NoPoSplat**（Ye et al., 2025）的权重初始化高斯预测头，使用 **MASt3R**（Leroy et al., 2024）的权重初始化其余部分，位姿头从头训练。训练在 4×A100 40GB GPU 上约需 3 天。数据集消融（Table C）显示，仅使用 Stereo4D 训练可在 Stereo4D 测试集上获得最佳精度，添加 Virtual KITTI 2 可改善 KITTI 上的运动精度但损害 Bonn 的点云精度，添加 PointOdyssey 则相反——这揭示了不同合成/真实数据集之间存在精度权衡。初始化方案消融（Table D）表明，从 MASt3R 初始化整体精度更优，而从 MonST3R 初始化则在 KITTI 和 Bonn 的点云精度上略有提升。

![[assets/figures/papers/paper_list_l32_https_openreview_net_forum_id_8gDDWqO59H/figures/005_Table_1.jpg]]
*Table 1: Geometry estimation: We report end-point error (EPE) for pointmap accuracy and absolute relative error (Abs. Rel.) and δ\<1.25 for depth accuracy. Lower is better for EPE and Abs. Rel., and higher is better for δ\<1.25*

![[assets/figures/papers/paper_list_l32_https_openreview_net_forum_id_8gDDWqO59H/figures/007_Figure_4.jpg]]
*Figure 4: Qualitative comparison of depth and projected 2D optical flow on Stereo4D, Bonn, and KITTI. For motion on KITTI, it visualizes motion relative to the camera, as GT is defined. Unlike DynaDUSt3R, ZeroMSF and St4RTrack, which suffers from residual motions in static region and inaccurate motion on object boundaries, UFO-4D exhibits clear motion boundaries and separation between moving objects and background. More qualitative results are in Section A.1*

![[assets/figures/papers/paper_list_l32_https_openreview_net_forum_id_8gDDWqO59H/figures/010_Table_4.jpg]]
*Table 4: Loss ablation. We report image reconstruction in PSNR and accuracy of Gaussian center (Point), rasterized point (Point rast.), Gaussian velocity (Motion), and rasterized motion (Motion rast.) in end-point error (EPE). Integrating the photometric loss gradient (Eq. (7c)) with all heads boosts overall performance. Losses on rendered motion (Eq. (6b)) and point map (Eq. (6c)) are crucial for achieving high accuracy*

![[assets/figures/papers/paper_list_l32_https_openreview_net_forum_id_8gDDWqO59H/figures/011_Figure_6.jpg]]
*Figure 6: Qualitative comparison on loss ablation. Gradient backpropagation from the image synthesis loss and rendering losses on point and motion helps UFO-4D improve motion and point estimates, especially on object and motion boundaries*

## 定位与知识库关联

### 1. 方法定位与核心差异

UFO-4D 处于**无姿态前馈4D重建**这一新兴技术路线的交叉点：它同时输出显式3D几何、3D运动场和相机位姿，而现有方法通常只覆盖其中部分子任务。与最具可比性的基线相比，UFO-4D 在三个关键维度上做出了系统性改变：

| 维度 | 现有范式 | UFO-4D 的改变 |
|------|----------|---------------|
| **场景表示** | 逐像素点云 + 运动向量（无显式表面连接） | 统一动态3D高斯泼溅（D-3DGS），通过可微渲染同时输出图像、稠密点云和场景流 |
| **监督信号** | 仅稀疏标注的几何/运动损失 | 半监督框架：稀疏标注损失 + 自监督光度损失 + 边缘感知平滑损失 |
| **位姿估计** | 后处理PnP+RANSAC | 网络直接前馈预测相对位姿 |

**核心洞察**在于：从单一动态3D高斯表示可微分地渲染多种信号（RGB图像、点云、场景流），能带来显著的训练优势——包括自监督光度损失提供的稠密梯度，以及渲染点云/运动损失施加的跨模态正正则化。这一洞察在 Table 4 的消融实验中得到直接验证：移除光度损失梯度（a→b）导致点云和运动精度下降；移除渲染点云/运动损失（a→c）则造成所有任务严重退化，运动边界模糊。

### 2. 与具体基线的关系

#### 2.1 动态场景重建基线

**DynaDUSt3R**（Jin et al., 2025）是最直接的对比对象，同样从双图估计几何和运动，但采用逐像素点云表示。Table 1 显示 UFO-4D 在 Stereo4D 上的点云 EPE 为 0.659，优于 DynaDUSt3R 的 0.811；Table 2 中场景流 EPE3D（forward）为 0.049 vs. 0.175，提升超过 3 倍。Table 5 的架构消融进一步表明，在相同训练协议下，动态3D高斯表示在 Stereo4D 和 KITTI 上全面超越逐像素表示，主要收益来自更准确的位姿估计和光度损失提供的稠密监督。但在 Bonn 数据集上，UFO-4D 略逊于 St4RTrack（点云 EPE 0.162 vs. 0.181），原因在于纹理缺乏区域高斯重叠导致的混合误差——Table E 显示深度精度随高斯尺度增大而下降。

**MonST3R**（Zhang et al., 2025a）是单目动态重建基线，Table 3 中 UFO-4D 的 ATE 为 0.0101，远优于 MonST3R 的 0.0458，体现了前馈位姿估计相对于 PnP+RANSAC 后处理的鲁棒性优势。

#### 2.2 场景流基线

**ZeroMSF**（Liang et al., 2025b）和 **St4RTrack**（Feng et al., 2025）是多帧场景流和同时跟踪重建方法。在 KITTI 上，UFO-4D 的场景流 EPE3D 为 0.137，而 DynaDUSt3R 为 0.463，ZeroMSF 和 St4RTrack 同样差距显著。定性结果（Figure 4, Figure A-C）表明，ZeroMSF 和 St4RTrack 在静态区域存在残余运动伪影，物体边界运动模糊，而 UFO-4D 展现出清晰的运动边界和动静分离能力。

#### 2.3 静态重建与位姿估计基线

**MASt3R**（Leroy et al., 2024）作为静态场景重建基线，其预训练权重被用于 UFO-4D 网络初始化（除相机头外）。Table G 显示，即使在 UFO-4D 的输出上使用 PnP+RANSAC 后处理，其位姿精度仍优于直接竞争者，验证了 UFO-4D 估计的几何质量更高。进一步地，UFO-4D 的前馈位姿头比 PnP+RANSAC 方案准确约 16.6%，证明直接预测比噪声敏感的迭代求解器更鲁棒。

### 3. 适用边界与局限

1. **仅支持双帧输入**：当前方法严格限定于两帧，扩展到长序列面临线性内存增长和一致性问题。论文未讨论时序融合或滑动窗口机制。

2. **线性运动假设**：时间演化公式 $\mathcal{G}(t') = \{ (\mu + \Delta t \cdot \mathbf{v}, \mathbf{v}, \mathbf{r}, \mathbf{s}, \mathbf{h}, \mathbf{c}, o)_{\mathbf{p}} \}$ 假设恒速直线运动，无法处理加速度变化或非线性轨迹。这一假设在 Stereo4D 和 KITTI 的短时帧间隔下尚可维持，但在长间隔或复杂运动中可能失效。

3. **纹理缺乏区域的退化**：在 Bonn 等纹理缺乏场景，高斯重叠导致混合误差，精度略低于逐像素表示（Table 5, Figure F）。Table E 定量显示深度精度随高斯尺度增大而下降，本质原因是缺乏纹理约束时大高斯覆盖了多个深度层的信号。

4. **计算与数据开销**：训练需 4×A100 40GB 约 3 天，且仅使用 10% 的 Stereo4D 数据以降低存储。全数据集潜力未被充分探索，可能限制性能上限。

5. **遮挡与极端视角**：不透明度置信度机制（Figure 5）在遮挡/去遮挡场景中表现良好，但在强遮挡或极端视角变化时，模型有时会选择错误的对应高斯，导致局部错误。

### 4. 开放问题

1. **长序列扩展**：如何将双帧前馈范式扩展到长序列而不导致内存线性增长？可能的路径包括循环架构、关键帧选择或时序高斯合并策略。

2. **非线性运动建模**：引入时变高斯属性或高阶运动模型（如加速度、旋转分量）来处理复杂动态场景，同时保持可微渲染的效率。

3. **渲染信号作为额外监督**：是否可以利用渲染图像、几何和运动作为新视角/新时刻的额外监督信号，形成闭环自训练来进一步提高精度？论文的半监督框架已为此提供了基础。

4. **纹理缺乏区域的改进**：如何更好地处理纹理缺乏区域以减少高斯重叠带来的误差？可能的方案包括自适应高斯尺度约束或引入结构先验（如平面假设）。

5. **训练数据效率**：Table C 的数据集消融显示不同数据集之间存在 trade-off（Stereo4D 单独训练在该数据集上最优，但加入 Virtual KITTI 2 或 PointOdyssey 会改善对应测试集的性能而损害其他），如何设计更优的数据混合策略或域适应方法？

## 原文 PDF

![[paperPDFs/ICLR_2026/UFO_4D_Unposed_Feedforward_4D_Reconstruction_from_Two_Images_f4891bdea6ab.pdf]]
