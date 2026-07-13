---
title: Learning Video Generation for Robotic Manipulation with Collaborative Trajectory Control
type: paper
paper_level: A
venue: arXiv
year: 2025
pdf_ref: paperPDFs/arxiv_2025/Learning_Video_Generation_for_Robotic_Manipulation_with_Collaborative_Trajectory_Control.pdf
project_link: https://fuxiao0719.github.io/projects/robomaster/
code_link: https://github.com/1x-technologies/1xgpt
aliases:
- LVGRMCTC
tags:
- arxiv_2025
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/image_and_video_generation
- topic/generative_models_diffusion
- topic/benchmarks_datasets_evaluation
core_operator: 将交互过程分解为预交互、交互、后交互三个子阶段，并在每一阶段注入主导物体的掩码特征（圆形体积表示），形成统一的协同轨迹表示。
primary_logic: 通过分阶段交互建模与物体感知的掩码特征注入，消除重叠区域的特征歧义，使模型能够协同而非割裂地学习多物体动力学，从而在保证轨迹精度的同时显著提升视觉质量。
claims:
- 协同轨迹将目标物体轨迹误差从IRASim的34.39降至24.16，同时视觉指标FVD从Tora的152.28降至147.31。
- 移除因果嵌入(w/o Causal Embedding)导致FVD上升至151.62，轨迹误差提升至27.15。
- 将掩码表示替换为点表示(w/ Point Representation)使物体轨迹误差从24.16增至31.41。
- 在RLBench与SIMPLER基准上，RoboMaster的具身动作规划成功率在8/10任务上超越Tora。
---

# Learning Video Generation for Robotic Manipulation with Collaborative Trajectory Control

> [!tip] 核心洞察
> 通过分阶段交互建模与物体感知的掩码特征注入，消除重叠区域的特征歧义，使模型能够协同而非割裂地学习多物体动力学，从而在保证轨迹精度的同时显著提升视觉质量。

| 字段 | 内容 |
|------|------|
| 中文题名 | 基于协同轨迹控制的机器人操作视频生成学习 |
| 英文题名 | Learning Video Generation for Robotic Manipulation with Collaborative Trajectory Control |
| 会议/期刊 | arXiv 2025 |
| Links | [paper](https://arxiv.org/abs/2506.01943) · [Project](https://fuxiao0719.github.io/projects/robomaster/) · [Code](https://github.com/1x-technologies/1xgpt) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/image_and_video_generation #topic/generative_models_diffusion #topic/benchmarks_datasets_evaluation |
| Method | RoboMaster |
| Dataset | Bridge Dataset |

> [!tip] 效果简介
> - Bridge Dataset 上，FVD↓ 147.31 vs 152.28 (Tora) (-4.97)；PSNR↑ 21.55 vs 21.24 (Tora) (+0.31)；SSIM↑ 0.803 vs 0.788 (Tora) (+0.015)。

## 概要

机器人操作视频生成的核心挑战在于同时控制机械臂与被操作物体的运动轨迹。现有方法（如 **Tora** (Zhang et al., CVPR 2025)）将多物体运动作为独立轨迹分别处理，但忽视了交互过程中物体间的耦合动力学——当机械臂与物体在空间上重叠时，独立轨迹会导致特征纠缠，造成视觉伪影（如物体缺失、形变）与轨迹精度下降。

**RoboMaster** 针对这一瓶颈，提出**协同轨迹控制**范式：将交互过程分解为预交互、交互、后交互三个子阶段，并在每一阶段注入主导物体的掩码特征（以圆形体积表示），形成统一的协同轨迹。其核心洞察在于：通过分阶段交互建模与物体感知的特征注入，消除重叠区域的特征歧义，使模型能够协同而非割裂地学习多物体动力学。

在整理后的 Bridge 数据集上，RoboMaster 在视频质量与轨迹精度上均超越现有轨迹控制方法：FVD 从 Tora 的 152.28 降至 **147.31**，物体轨迹误差从 26.43 降至 **24.16**，用户偏好率从 17.74% 提升至 **45.16%**。消融实验证实，移除因果嵌入或替换掩码表示为点表示均会导致性能显著退化。在 RLBench 与 SIMPLER 基准上，RoboMaster 的具身动作规划成功率在 8/10 任务上超越 Tora，验证了其在真实机器人任务中的有效性。

方法谱系上，RoboMaster 属于**轨迹条件视频生成**，以预训练视频扩散变换器（CogVideoX-5B）为骨干，通过掩码编码、协同轨迹分解与运动注入三个模块实现可控生成。相较于仅控制机械臂的 **IRASim**、使用点表示运动注入的 **MotionCtrl**、使用掩码但无交互分解的 **DragAnything**，以及 4D 世界模型 **TesserAct** (Zhen et al., ICCV 2025)，RoboMaster 首次在轨迹控制框架中显式建模交互阶段与物体身份一致性，填补了多物体交互视频生成的空白。

### 机器人操作视频生成的需求与挑战

具身智能的核心目标之一是使机器人能够在物理世界中执行复杂的操作任务。视频生成模型作为世界模拟器，为机器人提供了在“想象”中预演动作、评估后果的能力，从而大幅降低真实环境试错成本。然而，要让生成的视频真正服务于下游的具身动作规划，模型必须同时满足两个苛刻条件：**精确的轨迹控制**与**高保真的视觉质量**。

机器人操作场景的特殊之处在于，它天然涉及**多物体交互**——机械臂抓取、移动、放置物体，两者的运动轨迹在空间和时间上高度耦合。这种耦合在交互瞬间达到顶峰：机械臂的末端执行器与被操作物体在画面中高度重叠，形成密集的遮挡与接触区域。

### 现有方法的瓶颈：分离轨迹与特征纠缠

当前的轨迹控制视频生成方法，如 **Tora**（Zhang et al., CVPR 2025）、**MotionCtrl** 和 **DragAnything**，普遍采用**分离轨迹**的建模策略：将机械臂和物体的运动视为两条独立的轨迹，分别编码后注入生成模型。这种“分而治之”的思路在物体运动相互独立的场景下或许可行，但在机器人操作的交互重叠区域，它引发了一个根本性问题——**特征纠缠**。

当机械臂和物体的轨迹在重叠区域交叉时，分离轨迹表示无法区分“谁在动”以及“谁主导当前的视觉外观”。模型被迫从两条模糊的轨迹信号中猜测重叠像素的归属，导致生成结果中出现物体缺失、形状扭曲或运动不一致等严重伪影。如 Figure 2 所示，Tora 在抓取苹果的场景中，交互阶段的苹果完全消失——这正是分离轨迹在重叠区域特征融合失败的典型表现。

### 本文动机：从分离控制走向协同建模

上述瓶颈揭示了一个深层洞察：**多物体交互的本质不是多条独立轨迹的叠加，而是一个分阶段的、由主导物体驱动的协同过程。** 一个典型的“抓取-移动-放置”操作可以自然地分解为三个阶段：

1. **预交互阶段**：机械臂独立运动，接近目标物体；
2. **交互阶段**：机械臂与物体接触，两者作为一个整体协同运动；
3. **后交互阶段**：机械臂释放物体，物体保持最终状态或独立运动。

在每个阶段中，**主导物体**是明确的——预交互和后交互阶段由机械臂主导，交互阶段则由被操作物体的外观和运动主导。这一观察构成了本文的核心动机：**能否设计一种统一的轨迹表示，显式地编码这种分阶段的主导关系，从而在重叠区域消除特征歧义？**

本文提出的 **RoboMaster** 框架正是对这一问题的回答。它通过**协同轨迹**将多物体运动统一为单一表示，并在时间维度上分解为三个子阶段，每个阶段注入对应主导物体的掩码特征。这种设计使模型能够在重叠区域明确知道“当前该关注哪个物体”，从而在保证轨迹精度的同时，显著提升交互场景下的视觉保真度。

## 核心方法与创新机理

### 瓶颈诊断：重叠区域的特征纠缠

现有轨迹控制方法（如 **Tora**（Zhang et al., CVPR 2025）、**MotionCtrl**、**DragAnything**）将机器臂与被操作物体的运动建模为多条独立轨迹。当两者发生交互时，它们在空间上产生重叠区域，独立轨迹的特征在此处产生歧义与纠缠——模型无法区分“谁在动、谁被带动”，导致视觉保真度下降、物体变形甚至消失（如 Tora 生成中苹果的缺失，Figure 2）。这一瓶颈的因果本质是：**分离式轨迹表示破坏了多物体动力学的协同性**，使得扩散模型在重叠区域缺乏明确的特征归属信号。

### 核心创新：协同轨迹表示

RoboMaster 的核心创新在于将**对象分解**（decompose by objects）转变为**阶段分解**（decompose by interaction phases），提出统一的**协同轨迹**（Collaborative Trajectory）表示。具体而言，一条完整的操作轨迹被分解为三个子阶段：

1. **预交互阶段**（Pre-interaction）：仅机器臂运动，被操作物体静止；
2. **交互阶段**（Interaction）：机器臂抓取并移动物体，两者共同运动；
3. **后交互阶段**（Post-interaction）：机器臂释放，物体处于新位置。

在每个阶段，模型仅注入**主导物体**的掩码特征（圆形体积表示）——预交互和后交互阶段注入机器臂特征 $\mathbf{v}_d$，交互阶段同时注入机器臂与被操作物体特征 $\mathbf{v}_d, \mathbf{v}_s$。这一设计的因果机制是：**通过分阶段分配特征归属，消除重叠区域的多义性**，使扩散模型在每个时刻都明确“当前帧的视觉内容由谁主导”，从而协同而非割裂地学习多物体动力学。

### Changed Slots 详解

#### Slot 1：轨迹表示 —— 从分离轨迹到协同轨迹

| 维度 | 基线方法（Tora 等） | RoboMaster |
|------|---------------------|------------|
| 轨迹结构 | 多条独立轨迹，分别控制机器臂与物体 | 单一协同轨迹，按交互阶段分解 |
| 阶段划分 | 按对象分解（object-wise） | 按时序阶段分解（phase-wise） |
| 重叠区域处理 | 特征纠缠，归属模糊 | 阶段主导物体明确，特征无歧义 |

这一改变的直接证据来自 Table 2：协同轨迹将物体轨迹误差从 IRASim 的 34.39 降至 24.16，同时 FVD 从 Tora 的 152.28 降至 147.31。消融实验（Table 5）进一步证实，若使用分离轨迹（w/ Separate Trajectories），视觉质量与轨迹精度均显著下降。

#### Slot 2：物体特征编码 —— 从点坐标到掩码体积

基线方法（Tora、MotionCtrl）使用稀疏的**点坐标**表示物体位置，缺乏外观与形状信息。RoboMaster 提出**掩码驱动的外观-形状联合嵌入**：

- **外观提取**：利用 VAE 潜变量 $\tilde{\mathbf{z}}$ 与物体掩码 $\mathbf{m}$ 进行平均池化（Equation 3），得到物体外观特征 $\tilde{\mathbf{v}}$；
- **形状注入**：将外观特征扩展为**圆形空间体积**（Equation 4），半径 $r$ 与掩码面积成正比，使模型感知物体的空间尺度。

这一设计的因果逻辑是：**点表示仅提供位置信号，无法区分物体边界与外观；掩码体积表示将“物体是什么、在哪、多大”统一编码为空间特征**，使扩散模型在生成过程中保持物体身份一致性。Table 5 的消融直接验证了这一点：将掩码表示替换为点表示（w/ Point Representation），物体轨迹误差从 24.16 飙升至 31.41（+7.25）。

#### Slot 3：运动注入方式 —— 从交叉注意力到卷积注入

基线方法（如 DragAnything）通常使用**交叉注意力**将轨迹条件注入扩散主干。RoboMaster 采用**零初始化的 2D+1D 卷积运动注入器**，以加法方式融入 DiT 隐状态：

$$h = h + \text{norm}(\tilde{V}) + \tilde{V}, \quad \tilde{V} = \text{Conv1D}(\text{Conv2D}(\text{patchify}(V)))$$

零初始化确保训练初期模型行为与预训练主干一致，随后逐步学习轨迹到视觉的映射。Table 5 的消融表明，交叉注意力注入（w/ Cross Attention）导致性能下降，而卷积注入在保持轨迹精度的同时更充分地保留了预训练先验。

### 创新的系统性

上述三个 changed slots 并非孤立改进，而是构成一个**因果闭环**：

1. **协同轨迹分解**定义了“何时注入什么”的时序逻辑；
2. **掩码体积编码**提供了“注入什么”的内容信号；
3. **卷积运动注入**决定了“如何注入”的架构机制。

三者共同作用，使 RoboMaster 在轨迹精度（TrajError_obj 24.16 vs Tora 26.43）与视觉质量（FVD 147.31 vs Tora 152.28）两个维度同时超越基线，并在用户偏好测试中以 45.16% 的胜率大幅领先 Tora 的 17.74%（Table 2）。

RoboMaster 的整体 pipeline 围绕一个核心设计展开：将机器人操作视频生成建模为**以协同轨迹为条件的视频扩散过程**。给定初始帧 $\mathbf{I}$、文本提示 $\mathbf{c}$、用户指定的机械臂掩码 $\mathbf{M}_d$ 与被操作物体掩码 $\mathbf{M}_s$，以及一条协同轨迹 $\boldsymbol{\mathcal{C}}$，模型输出符合轨迹控制与语义约束的操作视频 $\mathbf{X}$。其形式化定义为：

$$f_{\theta}(\cdot): \mathbf{I} \in \mathbb{R}^{3 \times H \times W}, \mathbf{c} \in \mathcal{V}^{L}, \mathbf{M}_d, \mathbf{M}_s \in \{0,1\}^{H \times W}, \boldsymbol{\mathcal{C}} \in \mathbb{R}^{F \times 4} \mapsto \mathbf{X} \in \mathbb{R}^{F \times 3 \times H \times W}$$

框架由四个核心模块串联构成，如 Figure 3 所示：

![[assets/figures/papers/paper_list_l85_https_arxiv_org_abs_2506_01943/figures/004_Figure_3.jpg]]
*Figure 3: RoboMaster Framework. Given an input image I and a prompt c, it generates a desired robotic manipulation video X with the collaborative trajectory design. Specifically, it first encodes the object masks, including robotic arm*

**1. 3D VAE 编码器**  
将输入图像与视频帧压缩至潜空间，为后续特征提取与扩散生成提供紧凑表示。该模块继承自预训练视频扩散模型 CogVideoX-5B，在训练中保持冻结。

**2. 物体外观与形状嵌入（Subject Appearance & Shape Embedding）**  
从初始帧的掩码中提取每个物体的外观特征，并构造具有空间感知的圆形体积表示。具体而言，先将掩码下采样至 VAE 潜变量分辨率，再对有效像素区域的潜变量进行平均池化，得到物体特征向量 $\tilde{\mathbf{v}}_{d}, \tilde{\mathbf{v}}_{s}$。为增强空间定位能力，该向量被扩展为一个半径 $r$ 正比于掩码面积的圆形体积 $\mathbf{v}_{d,s}$（Figure 4），从而在保持跨帧身份一致性的同时，为后续轨迹控制提供物体感知的注入信号。

**3. 协同轨迹分解（Collaborative Trajectory Decomposition）**  
这是框架的核心创新。不同于现有方法将机械臂与物体轨迹作为独立信号处理，RoboMaster 将交互过程按时间轴分解为三个子阶段：**预交互**（$\mathcal{C}_1$，仅含机械臂轨迹）、**交互**（$\mathcal{C}_2$，仅含物体轨迹）和**后交互**（$\mathcal{C}_3$，仅含机械臂轨迹）。每个阶段注入对应主导物体的掩码特征，形成统一的协同轨迹潜变量 $\mathbf{V}$。这一分解策略从根源上消除了重叠区域的特征纠缠问题——当机械臂与物体在交互阶段空间重叠时，模型不再需要从多条独立轨迹中歧义地推断运动归属。

**4. 运动注入器（Motion Injector）**  
协同轨迹潜变量 $\mathbf{V}$ 经 patchify 操作后，依次通过零初始化的 2D 空间卷积层与 1D 时间卷积层编码，以加法方式融入视频 DiT 主干的隐状态：$h = h + \mathrm{norm}(\tilde{\mathbf{V}}) + \tilde{\mathbf{V}}$。零初始化确保训练初期轨迹控制信号不会破坏预训练主干的生成先验，随后逐步学习有效的运动注入。

整体训练目标为以掩码和协同轨迹为条件的扩散噪声预测损失：

$$\mathcal{L}(\pmb{\theta}) = \mathbb{E}_{\mathbf{x}, \mathbf{c}, \epsilon \sim \mathcal{N}(\mathbf{0}, \sigma_t^2 \mathbf{I}), \mathbf{I}, \mathbf{M}_d, \mathbf{M}_s, \boldsymbol{\mathcal{C}}, t} \left[ \| \epsilon - \hat{\epsilon}_{\pmb{\theta}_1}(\mathbf{x}_t, \mathbf{c}, \mathbf{M}_d, \mathbf{M}_s, \boldsymbol{\mathcal{C}}, t) \|_2^2 \right]$$

该损失同时优化 DiT 主干与运动注入器参数，使模型学会在协同轨迹引导下生成视觉连贯且运动精确的操作视频。

RoboMaster 的核心架构围绕三个关键设计展开：物体感知的掩码特征编码、协同轨迹分解，以及零初始化运动注入器。以下逐一剖析各模块的机理与关键公式。

### 物体外观与形状嵌入

传统轨迹控制方法（如 **Tora**, Zhang et al., CVPR 2025）使用点坐标或简单掩码表示物体，缺乏外观与形状信息。RoboMaster 通过耦合 VAE 潜空间的掩码平均池化与圆形体积扩展，构造物体感知的嵌入。

给定初始帧 $\mathbf{I}$，首先通过 3D VAE 编码器获得潜变量 $\tilde{\mathbf{z}} \in \mathbb{R}^{C \times T \times h \times w}$。将物体掩码 $\mathbf{M}$ 下采样至与 $\tilde{\mathbf{z}}$ 对齐的空间维度后，执行掩码平均池化提取外观特征：

$$\tilde{\mathbf{v}}_{d,s}[i]=\frac{1}{\sum_{i=1}^h\sum_{j=1}^w\mathbf{m}_{d,s}[i,j]}\sum_{i=1}^h\sum_{j=1}^w\tilde{\mathbf{z}}_{d,s}[i,x,y]$$

其中 $\tilde{\mathbf{v}}_{d,s}$ 分别表示机械臂（$d$）与被操作物体（$s$）的外观特征向量，$\mathbf{m}_{d,s}$ 为对应的二值掩码。这一操作将物体在潜空间中的有效像素聚合为紧凑的身份表征。

为增强空间感知能力，进一步将特征向量扩展为圆形体积：

$$\mathbf{v}_{d,s}[i,j,k]=\tilde{\mathbf{v}}_{d,s}[i] \quad \mathrm{if}\ (j-x)^2+(k-y)^2\le r_{d,s}^2$$

其中 $r_{d,s}$ 与掩码有效面积成正比。该设计使物体特征在潜空间中占据与真实物体尺寸相称的区域，而非孤立点，为后续协同轨迹注入提供空间上下文。

### 协同轨迹分解

现有方法将机械臂与被操作物体的运动视为多条独立轨迹分别控制，在交互导致的重叠区域产生特征纠缠。RoboMaster 将交互过程分解为三个子阶段，并统一为单一协同轨迹。

给定完整轨迹 $\boldsymbol{\mathcal{C}} = \{(\mathbf{p}_t^d, \mathbf{p}_t^s)\}_{t=1}^{F}$，按时间轴分解为：

- **预交互阶段** $\mathcal{C}_1 = \{\mathbf{p}_t^d\}_{t=1}^{F_1}$：仅机械臂运动，注入 $\mathbf{v}_d$；
- **交互阶段** $\mathcal{C}_2 = \{\mathbf{p}_t^s\}_{t=F_1+1}^{F_2}$：物体随机械臂移动，注入 $\mathbf{v}_d$ 与 $\mathbf{v}_s$；
- **后交互阶段** $\mathcal{C}_3 = \{\mathbf{p}_t^d\}_{t=F_2+1}^{F}$：机械臂撤离，注入 $\mathbf{v}_d$。

对应的条件分布分解为：

$$\underbrace{p_{\theta}(\mathbf{x}_1\mid\mathbf{I},\mathbf{c},\mathbf{v}_d,\mathcal{C}_1)}_{\mathrm{pre-interaction}}\underbrace{p_{\theta}(\mathbf{x}_2\mid\mathbf{I},\mathbf{c},\mathbf{v}_d,\mathbf{v}_s,\mathcal{C}_1,\mathcal{C}_2)}_{\mathrm{interaction}}\underbrace{p_{\theta}(\mathbf{x}_3\mid\mathbf{I},\mathbf{c},\mathbf{v}_d,\mathbf{v}_s,\mathcal{C}_1,\mathcal{C}_2,\mathcal{C}_3)}_{\mathrm{post-interaction}}$$

每个阶段仅注入该阶段主导物体的掩码特征，使模型明确感知“当前谁在运动”，从根本上消除重叠区域的特征歧义。

### 运动注入器与训练目标

协同轨迹潜变量 $\mathbf{V}$ 经 patchify 后，通过零初始化的 2D 空间卷积与 1D 时间卷积编码，以加法方式融入 DiT 隐状态：

$$\mathbf{h} = \mathbf{h} + \mathrm{norm}(\tilde{\mathbf{V}}) + \tilde{\mathbf{V}},\quad \tilde{\mathbf{V}} = \mathrm{Conv1D}(\mathrm{Conv2D}(\mathrm{patchify}(\mathbf{V})))$$

零初始化确保训练初期注入模块不干扰预训练 DiT 的生成能力，随后逐步学习轨迹条件。

整体训练目标为以掩码和协同轨迹为条件的扩散噪声预测损失：

$$\mathcal{L}(\pmb{\theta})=\mathbb{E}_{\mathbf{x},\mathbf{c},\epsilon\sim\mathcal{N}(\mathbf{0},\sigma_t^2\mathbf{I}),\mathbf{I},\mathbf{M}_d,\mathbf{M}_s,\boldsymbol{\mathcal{C}},t}\left[\|\epsilon-\hat{\epsilon}_{\pmb{\theta}_1}\left(\mathbf{x}_t,\mathbf{c},\mathbf{M}_d,\mathbf{M}_s,\boldsymbol{\mathcal{C}},t\right)\|_2^2\right]$$

该损失同时优化 DiT 主干与运动注入器参数，使模型学习在轨迹引导下生成视觉一致且物理合理的操作视频。

## 实验与关键发现

### 核心定量结果

RoboMaster 在 Bridge Dataset 上与多个轨迹控制基线进行全面对比，所有方法均基于相同的 CogVideoX-5B 骨干重新训练以保证公平性。如 Table 2 所示，RoboMaster 在视频质量与轨迹精度两个维度上均取得最优结果：

![[assets/figures/papers/paper_list_l85_https_arxiv_org_abs_2506_01943/figures/006_Table_2.jpg]]
*Table 2: Quantative Comparison. Note that all the baselines are retrained on our curated dataset*

- **视频质量**：FVD 降至 **147.31**，较 Tora 的 152.28 降低 4.97，较 DragAnything 的 158.42 降低 11.11。PSNR 达到 21.55，SSIM 达到 0.803，均优于所有对比方法。
- **轨迹精度**：机械臂轨迹误差（TrajError_robot）降至 **16.47**，物体轨迹误差（TrajError_obj）降至 **24.16**。相比 Tora 分别降低 1.67 和 2.27，相比仅控制机械臂的 IRASim 在物体轨迹误差上降低达 10.23（从 34.39 降至 24.16）。
- **用户偏好**：在用户研究中，RoboMaster 以 **45.16%** 的偏好率显著领先 Tora 的 17.74%，优势达 27.42 个百分点。

定性对比（Figure 5）进一步验证了 RoboMaster 在多种操作技能（移动、拾取、关闭、竖立等）上的视觉一致性优势，尤其在交互阶段被操作物体的外观保持方面明显优于 Tora 和 DragAnything。

![[assets/figures/papers/paper_list_l85_https_arxiv_org_abs_2506_01943/figures/007_Figure_5.jpg]]
*Figure 5: Qualitative Comparison. RoboMaster demonstrates superior performance across a range of manipulation skills (e.g., move, pick, close, upright, close), exhibiting improved visual consistency of the manipulated subject compared to prior baselines*

### 具身动作规划验证

为验证生成视频在下游具身任务中的实用性，作者在 RLBench 和 SIMPLER 两个基准上评估动作规划成功率。具体流程为：用 RoboMaster 生成视频后，通过逆动力学模型回归可执行动作标签。Table 4 显示，在 10 个评估任务中，RoboMaster 在 **8 个任务上超越 Tora**，例如在 "open drawer" 任务上达到 0.83 vs Tora 的 0.79，在 "meat off grill" 任务上达到 0.91 vs 0.89。同时，Table 3 表明逆动力学模型预测的动作所生成的视频与训练集动作生成的视频质量相当（PSNR 25.12 vs 25.48，FVD 127 vs 132），验证了该闭环流程的有效性。

### 消融实验：因果机制的严格验证

Table 5 的系统消融揭示了各设计选择对性能的因果贡献：

![[assets/figures/papers/paper_list_l85_https_arxiv_org_abs_2506_01943/figures/012_Table_5.jpg]]
*Table 5: Ablation Study on Bridge Full Benchmark*

1. **因果嵌入（Causal Embedding）**：移除因果嵌入后，FVD 从 147.31 升至 **151.62**，轨迹误差从 24.16 升至 **27.15**，证实分阶段交互建模对消除特征纠缠至关重要。

2. **掩码表示 vs 点表示**：将掩码表示替换为点表示（w/ Point Representation）导致物体轨迹误差从 24.16 飙升至 **31.41**（上升 7.25），FVD 升至 149.88。这验证了外观与形状信息嵌入对保持物体身份一致性的关键作用。

3. **协同轨迹 vs 分离轨迹**：使用分离轨迹（w/ Separate Trajectories）在重叠区域引入特征融合问题，FVD 升至 149.07，轨迹误差升至 25.43，直接证明了协同轨迹设计的必要性。

4. **运动注入方式**：将加法式卷积注入替换为交叉注意力注入（w/ Cross Attention）导致性能下降，FVD 升至 150.15，验证了零初始化卷积注入器在稳定训练中的优势。

### 鲁棒性分析

RoboMaster 对输入扰动表现出较强的鲁棒性：

- **掩码稀疏性**（Table 6）：当掩码稀疏度高达 60% 时，PSNR 仍可保持 **97.89%** 以上的水平，表明方法对不精确的掩码输入具有容忍度。
- **轨迹扰动**（Table 7）：轨迹扰动达 40% 时，PSNR 仍保持 **96.54%**，说明模型对轨迹标注误差不敏感。
- **不完美提示**（Table 8）：在提示信息不完整或存在偏差的情况下，生成质量下降有限，进一步验证了方法的实用性。

![[assets/figures/papers/paper_list_l85_https_arxiv_org_abs_2506_01943/figures/013_Table_7.jpg]]
*Table 7: Ablation on Trajectory Perturbation*

![[assets/figures/papers/paper_list_l85_https_arxiv_org_abs_2506_01943/figures/014_Table_8.jpg]]
*Table 8: Ablation on Imperfect Prompt Input*

### 失败模式与局限性

尽管 RoboMaster 在受控场景下表现优异，但分析揭示了以下失败模式：

1. **域外泛化退化**：对于训练分布外的物体外观或复杂场景，可能生成不完整或扭曲的物体，尤其在未见过的物体形状下身份一致性下降明显。
2. **3D 空间控制不足**：当前方法未显式整合深度线索，难以处理 3D 遮挡和复杂空间配置，在需要精确深度感知的操作中可能失效。
3. **新机器人形态泛化受限**：对训练期间未见过的机器人形态，直接生成质量下降，可能需要额外的预训练或轻量级适配（如 LoRA）。
4. **自动标注不可靠**：Grounded-SAM 在多物体或复杂场景下的自动分割成功率有限（Table R11），人工标注在数据构建中仍不可或缺，这限制了方法的大规模扩展能力。

## 定位与知识库关联

### 1. 与现有轨迹控制方法的谱系关系

RoboMaster 处于**轨迹控制视频生成**这一细分领域，其核心突破在于将交互建模的粒度从“物体分解”推进到“阶段分解”。表1系统对比了现有方法的交互粒度与物体感知维度，清晰标定了 RoboMaster 的方法学坐标。

**分离轨迹范式（Separated Trajectories）** 是此前的主流方案。**Tora**（Zhang et al., CVPR 2025）将机器臂与被操作物体作为独立运动实体，分别建模其轨迹；**MotionCtrl** 采用点表示的运动注入；**DragAnything** 虽使用掩码，但未对交互阶段进行分解。这一范式的根本瓶颈在于：当机器臂与物体在交互阶段发生空间重叠时，独立轨迹在重叠区域产生特征纠缠（feature entanglement），导致被操作物体在生成视频中缺失或扭曲（如 Figure 2 中 Tora 生成的“消失的苹果”）。

**仅控制机械臂的范式**以 **IRASim** 为代表，完全忽略被操作物体的运动，无法建模操作的核心语义——物体状态的改变。

RoboMaster 的方法学跃迁体现在三个维度：

1. **交互粒度**：从“物体分解”跃迁至“阶段分解”。协同轨迹将联合分布因式分解为预交互（pre-interaction）、交互（interaction）、后交互（post-interaction）三个子阶段的条件分布（Equation 5），各阶段注入对应主导物体的掩码特征——预交互和后交互阶段以机械臂为主导，交互阶段以被操作物体为主导。这一设计从因果结构上消除了重叠区域的多物体特征歧义。

2. **物体感知维度**：从“点坐标/简单掩码”跃迁至“外观+形状编码”。RoboMaster 通过 VAE 潜变量的掩码平均池化（Equation 3）提取物体外观特征，再以圆形体积扩展（Equation 4）赋予空间范围，使模型获得物体形状感知能力。消融实验证实，将掩码表示替换为点表示（w/ Point Representation）使物体轨迹误差从 24.16 升至 31.41（Table 5），验证了形状感知对精确定位的关键作用。

3. **运动注入机制**：从“交叉注意力”跃迁至“零初始化卷积注入”。RoboMaster 采用 2D+1D 卷积的运动注入器，以加法方式融入 DiT 隐状态，避免了交叉注意力（w/ Cross Attention）带来的性能下降（Table 5）。

### 2. 与世界模型和机器人策略的接口关系

RoboMaster 在具身智能栈中占据**视觉生成层**的位置，向上可为世界模型和策略学习提供高质量的视频预测。

**4D 基世界模型**如 **TesserAct**（Zhen et al., ICCV 2025）需要从视频中学习动力学先验。RoboMaster 生成的视频在轨迹精度（TrajError_obj 24.16 vs Tora 26.43）和视觉保真度（FVD 147.31 vs Tora 152.28）上均优于现有方法（Table 2），意味着其输出可作为更可靠的世界模型训练数据。

**机器人策略基线**如 **OpenVLA**（Kim et al., 2024）依赖视觉输入进行动作决策。RoboMaster 的具身动作规划验证（Table 4）表明：在 RLBench 与 SIMPLER 基准的 10 个任务中，基于 RoboMaster 生成视频的逆向动力学模型在 8 个任务上超越了 Tora 的成功率，证明其视频质量提升可直接转化为下游策略的性能增益。

### 3. 适用边界与局限性

尽管 RoboMaster 在 Bridge 数据集上展现了显著优势，其适用边界受以下因素制约：

1. **域外泛化的视觉退化**：对于训练分布外的物体外观和场景（Figure 6 的“Pick up the bee”等示例），模型可能生成不完整或扭曲的物体。当前方法未显式整合深度或 3D 线索，难以处理复杂的空间遮挡和三维配置关系。

2. **机器人形态的泛化局限**：模型对未见过的机器人形态（如不同自由度、不同外观的机械臂）泛化能力有限，可能需要额外的预训练数据或测试时适配机制（如 LoRA）。

3. **多主体交互的未验证边界**：当前协同轨迹分解策略针对双臂-单物体（两个主体）场景设计，在超过两个主体的复杂交互场景下的有效性尚未验证。

4. **标注依赖**：自动分割模型（如 Grounded-SAM）在多物体或复杂场景下的可靠性低（Table R11），高质量训练数据仍依赖人工标注的三阶段轨迹和掩码。

### 4. 开放问题

1. **3D 空间控制的深化**：如何将深度线索或 3D 表征有效融入协同轨迹框架，实现更精准的三维交互控制，是提升操作精度的关键方向。

2. **跨形态泛化机制**：能否通过更丰富的预训练数据或轻量级适配机制（如少样本微调），使模型泛化到训练期间未见的新型机器人形态？

3. **自动标注的鲁棒性提升**：能否通过更强的视觉基础模型或半监督策略，提高交互阶段自动分割的鲁棒性，减少对人工修正的依赖？

4. **多主体扩展**：在更复杂的多物体交互场景（如多臂协作、多物体同时操作）下，协同轨迹的阶段分解策略是否依然有效？是否需要引入图结构或注意力机制来建模多主体间的动态关系？

### 5. 方法谱系定位总结

RoboMaster 的核心贡献在于**以因果结构驱动轨迹表示的重设计**：通过将交互过程分解为因果上有序的三个子阶段，并在各阶段注入对应主导物体的感知特征，从根本上解决了分离轨迹范式中重叠区域的特征纠缠问题。这一思路在方法学上可追溯至因果表示学习中的“解耦”（disentanglement）思想，但在轨迹控制视频生成领域是首次系统性应用。其技术方案（掩码池化 + 圆形体积 + 零初始化卷积注入）为后续研究提供了可复用的模块化设计范式。

## 原文 PDF

![[paperPDFs/arxiv_2025/Learning_Video_Generation_for_Robotic_Manipulation_with_Collaborative_Trajectory_Control.pdf]]
