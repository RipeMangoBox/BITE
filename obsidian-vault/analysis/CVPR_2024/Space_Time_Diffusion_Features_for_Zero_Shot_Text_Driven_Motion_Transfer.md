---
title: "Space-Time Diffusion Features for Zero-Shot Text-Driven Motion Transfer"
type: paper
paper_level: A
venue: CVPR
year: 2024
pdf_ref: paperPDFs/CVPR_2024/Space_Time_Diffusion_Features_for_Zero_Shot_Text_Driven_Motion_Transfer.pdf
aliases:
- SBMTPM
- STDFZSTDMT
tags:
- CVPR_2024
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: "成对空间边缘均值（SMM）差异损失函数，通过引导生成过程使目标视频与输入视频在逐帧SMM特征差异上保持一致，从而在解耦外观和形状信息的同时，保持整体运动和场景布局。"
primary_logic: "预训练文本到视频扩散模型的中间层时空特征，其空间边缘均值（SMM）可作为一种鲁棒的每帧全局描述符，有效编码物体姿态、位置和场景语义布局，同时对像素级外观和形状变化不敏感；对该描述符进行成对差异优化，能够在不依赖显式姿态模型的条件下实现跨类别运动迁移。"
claims:
- "利用预训练且冻结的文本到视频扩散模型（ZeroScope），无需任何训练或微调即可完成运动迁移。"
- "提出的成对SMM差异损失引导生成过程，成功保留了输入视频的整体运动，同时允许大幅的外观和形状编辑。"
- "在涵盖多种场景和物体的实验中，与TokenFlow、Control-A-Video、Tune-A-Video等基线相比，本方法在用户偏好研究和定量平衡指标上均取得最优结果。"
- "空间边缘均值（SMM）特征能捕获物体的姿态和场景布局，同时对像素级变化鲁棒，并通过反演实验和最近邻检索得到验证。"
---

# Space-Time Diffusion Features for Zero-Shot Text-Driven Motion Transfer

> [!tip] 核心洞察
> 预训练文本到视频扩散模型的中间层时空特征，其空间边缘均值（SMM）可作为一种鲁棒的每帧全局描述符，有效编码物体姿态、位置和场景语义布局，同时对像素级外观和形状变化不敏感；对该描述符进行成对差异优化，能够在不依赖显式姿态模型的条件下实现跨类别运动迁移。

| 字段 | 内容 |
| ------- | -------------------------------------------------------------------------------------------------------- |
| 中文题名 | 时空扩散特征驱动的零样本文本运动迁移 |
| 英文题名 | Space-Time Diffusion Features for Zero-Shot Text-Driven Motion Transfer |
| 会议/期刊 | CVPR 2024 |
| Links | [paper](https://arxiv.org/abs/2311.17009); [Project](https://diffusion-motion-transfer.github.io/) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/image_and_video_generation |
| Method | SMM-Based Motion Transfer (Proposed Method) |
| Dataset | User Study (2AFC), Custom dataset (54 video-edit pairs, 21 videos) |

> [!tip] 效果简介
> - User Study (2AFC) 上，Human preference for our method 为 72.57%，对比 TokenFlow (50% chance)，变化 +22.57%。
> - User Study (2AFC) 上，Human preference for our method 为 84.50%，对比 Control-A-Video (50% chance)，变化 +34.50%。
> - User Study (2AFC) 上，Human preference for our method 为 77.80%，对比 Tune-A-Video (50% chance)，变化 +27.80%。

## 概述

**核心问题**：现有文本驱动的视频编辑与运动迁移方法存在两个关键瓶颈：（1）大多要求源对象与目标对象属于相同或相近类别，难以在保持细粒度运动特性的同时实现大幅的形状和外观变化；（2）缺乏可直接利用的通用时空运动先验，导致跨类别编辑时运动保真度低或编辑效果受限。

**核心方案**：本文提出一种零样本的文本驱动运动迁移方法。其核心洞察是：预训练文本到视频扩散模型（ZeroScope）中间层时空特征的空间边缘均值（Spatial Marginal Mean, SMM）可作为一种鲁棒的每帧全局描述符——它能有效编码物体姿态、位置和场景语义布局，同时对像素级的外观和形状变化不敏感。基于此，方法通过一个**成对SMM差异损失函数**引导生成过程，使目标视频与输入视频在逐帧SMM特征的成对差异上保持一致，从而在解耦外观和形状信息的同时保持整体运动和场景布局。整个过程**无需任何训练或微调**，完全依赖冻结的预训练扩散模型。

**方法定位**：本方法属于基于预训练扩散模型特征的零样本视频编辑范式，与 TokenFlow（Geyer et al., 2023）、Tune-A-Video（Wu et al., 2022）、Control-A-Video（Chen et al., 2023）等方法相比，其关键区别在于：（1）使用文本到视频（T2V）模型的时空特征而非2D图像扩散特征；（2）通过SMM描述符的成对差异而非全特征重建来保持运动，从而允许更大的形状编辑自由度；（3）采用低频滤波的DDIM逆噪声初始化，在保留场景布局的同时引入生成多样性。

**主要结果**：
- 在用户偏好研究（2AFC）中，本方法相对于 TokenFlow 获得 72.57% 的偏好票，相对于 Control-A-Video 获得 84.50%，相对于 Tune-A-Video 获得 77.80%（Table 1）。
- 在 CLIP 文本相似度与运动保真度的平衡评估中，本方法展现出优于各基线的综合表现（Figure 8）。
- 消融实验证实：全时空特征重建会阻止外观变化；仅优化SMM特征（非成对差异）仍保留过多原始外观信息；随机噪声初始化会导致运动保真度显著下降（Figure 7）。

**局限性**：当输入运动与目标物体的组合对于T2V模型是分布外（out-of-distribution）时，方法难以维持原视频的运动特征；推理时间较长（DDIM反演约10分钟，优化采样7-15分钟），离实时应用仍有距离。

## 背景与动机

### 文本驱动的视频编辑：从外观编辑到运动迁移

近年来，文本驱动的视频编辑技术取得了显著进展。以 **Tune-A-Video**（Wu et al., 2022）为代表的方法通过在单视频上微调图像扩散模型实现风格转换，**Control-A-Video**（Chen et al., 2023）则将可控图像生成扩展至视频领域以保持逐帧布局，而 **TokenFlow**（Geyer et al., 2023）利用扩散特征的时空一致性实现零样本编辑。这些方法在保持视频外观一致性方面表现优异，但其共同局限在于：它们主要面向**相同或相近物体类别**的编辑场景，例如将一只奔跑的狗转换为另一品种的狗，或改变视频的整体风格。

然而，更具挑战性的任务——**跨类别运动迁移**——要求将输入视频中的运动模式（如姿态变化、运动轨迹、时序节奏）迁移至外观和形状截然不同的目标物体上。例如，将一辆汽车的3D旋转姿态迁移至一辆自行车，同时保持自行车的结构特征。现有方法在这一场景下面临双重困境：要么因过度约束像素级外观而无法实现大幅形状变化，要么因缺乏有效的运动保持机制而导致运动保真度严重下降。

### 核心瓶颈：通用时空运动先验的缺失

现有方法的根本瓶颈在于**缺少可直接利用的通用时空运动先验**。具体而言：

1. **运动与外观的纠缠**：传统方法通常直接操作像素空间或浅层特征，难以将物体的运动特性（姿态、位置、时序变化）与其外观属性（纹理、颜色、形状细节）有效解耦。当编辑目标要求大幅改变外观时，运动信息往往随之丢失。

2. **对显式姿态模型的依赖**：部分运动迁移方法依赖显式的姿态估计器（如人体骨骼关键点检测），这限制了其适用范围——无法处理非人体对象、非刚性运动或缺乏预定义姿态模型的物体类别。

3. **跨类别泛化能力不足**：现有视频编辑方法在训练或设计阶段隐含假设源对象与目标对象属于相同或相近类别，当面对“汽车→自行车”或“狗→骆驼”等跨类别迁移任务时，其运动保持机制往往失效。

### 本文动机：从预训练视频扩散模型中挖掘运动先验

预训练的文本到视频扩散模型（Text-to-Video, T2V）在海量视频数据上学习到了丰富的时空生成先验，其内部特征隐式编码了物体的运动模式、场景布局和时序一致性。本文的核心动机是：**能否在不进行任何训练或微调的前提下，直接从冻结的T2V模型中提取一种通用的运动描述符，用以引导跨类别的运动迁移？**

这一思路面临两个关键挑战：（1）如何从扩散模型的中间层特征中提取对像素级外观变化不敏感、但对运动姿态和场景布局保持高保真度的表示；（2）如何设计优化目标，使得在保持运动特征的同时，允许目标对象在形状和外观上发生充分变化以匹配编辑文本。

本文的解决方案围绕**空间边缘均值（Spatial Marginal Mean, SMM）** 这一核心概念展开。SMM通过对T2V模型中间层时空特征的空间维度取均值，生成每帧的全局描述符。实验表明，该描述符能有效捕获物体的姿态、位置和场景语义布局，同时对像素级的外观和形状变化具有鲁棒性（见Figure 2）。在此基础上，本文进一步提出**成对SMM差异损失**，通过保持帧间SMM特征的相对变化而非绝对值，实现了运动保持与外观编辑自由度之间的关键平衡。

## 核心创新

本方法的核心创新在于提出了一种**无需训练或微调的零样本文本驱动运动迁移框架**，其关键突破可归纳为三个紧密耦合的“changed slots”：特征描述符、损失函数和初始化策略。

### 1. 特征描述符：空间边缘均值（SMM）

传统方法通常依赖预训练2D扩散模型的空间特征（如DIFT），或直接使用全时空特征进行重建。本方法首次从**预训练且冻结的文本到视频（T2V）扩散模型**（ZeroScope）的中间层提取时空特征 $\mathbf{f}(\mathbf{x}_t) \in \mathbb{R}^{F \times M \times N \times D}$，并对其空间维度取均值，构造出**空间边缘均值（Spatial Marginal Mean, SMM）** 描述符：

$$\mathrm{SMM}[\mathbf{f}(\mathbf{x}_t)] = \frac{1}{M \cdot N} \sum_{i=1}^{M} \sum_{j=1}^{N} \mathbf{f}(\mathbf{x}_t)_{i,j}$$

该描述符的因果作用体现在两个层面：
- **信息保留**：SMM作为一种每帧全局描述符，能有效编码物体的姿态、位置和场景语义布局（Figure 2(c) 反演实验证实，SMM引导的重建可恢复正确姿态与位置）。
- **外观解耦**：SMM对像素级外观和形状变化具有鲁棒性（Figure 2(d) 最近邻检索显示，在显著外观和视角变化下仍能匹配相同姿态的帧），这为跨类别编辑提供了关键的解耦能力。

### 2. 损失函数：成对SMM差异损失

这是本方法最关键的因果调节旋钮。基线方法若直接使用全时空特征重建作为损失（如特征反演中的标准做法），会强制保留像素级外观和形状，**阻止跨类别编辑所需的结构变化**（Figure 7(b) 消融证实）。若仅优化SMM特征绝对值，虽增加一定灵活性，但仍保留过多原始外观信息，无法充分匹配编辑文本（Figure 7(c)）。

本方法转而优化**成对SMM差异**：先计算驱动视频与生成视频中各帧SMM特征的成对差值：

$$\Delta_{(i,j)}^{t} = \phi_i^{t} - \phi_j^{t}, \quad \tilde{\Delta}_{(i,j)}^{t} = \tilde{\phi}_i^{t} - \tilde{\phi}_j^{t}$$

再最小化二者之间的L2距离：

$$\mathcal{L}\big(\mathrm{SMM}(\mathbf{f}(\mathbf{x}_t)), \mathrm{SMM}(\mathbf{f}(\tilde{\mathbf{x}}_t))\big) = \sum_{i} \sum_{j} \lVert \Delta_{(i,j)}^{t} - \tilde{\Delta}_{(i,j)}^{t} \rVert_2^2$$

该设计的核心洞察在于：**成对差异保留了帧间相对运动变化，同时丢弃了绝对外观信息**。这使得生成过程能够保持输入视频的整体运动和时序动态，同时允许目标物体的形状和外观发生大幅变化（Figure 7(f) 完整方法效果最优）。

### 3. 初始化策略：低频滤波初始化

从纯随机噪声初始化会导致运动保真度显著下降（Figure 7(e)），而直接使用DDIM逆噪声则限制编辑多样性。本方法采用**低频滤波初始化**：

$$\tilde{\mathbf{x}}_T = LF_\xi(\mathbf{x}_T) + (\epsilon_0 - LF_\xi(\epsilon_0))$$

该策略将DDIM逆噪声 $\mathbf{x}_T$ 的低频分量（保留场景布局和物体位置信息）与随机噪声 $\epsilon_0$ 的高频分量（提供编辑多样性）相结合。消融实验（Figure 7(d-f)）表明，低频滤波初始化与成对SMM差异损失协同作用，是实现最佳运动保持与编辑逼真度平衡的必要条件。

### 创新总结

上述三个changed slots构成了一个完整的因果链条：**SMM描述符**从冻结的T2V模型中提取外观解耦的运动表示，**成对SMM差异损失**将运动保持问题转化为帧间相对关系的保持，**低频滤波初始化**在布局保持与编辑多样性之间取得平衡。三者协同，使得本方法在不依赖显式姿态模型、无需任何训练或微调的条件下，首次实现了跨类别物体的零样本运动迁移。

## 整体框架

![[assets/figures/papers/paper_list_l3_Space_Time_Diffusion_Features_for_Zero_Shot_Text_Driven_Motion_Transfer/figures/003_Figure_3.jpg]]
*Figure 3: Pipeline. (a) Given an input video, we apply DDIM inversion and extract space-time features $\pmb { f } \in \mathbb { R } ^ { F \times M \times N \times D }$ from intermediate layer activations. We obtain our Spatial Marginal Mean (SMM) feature SMM [ $\dot { \pmb f } ] \in \mathbb { R } ^ { F \times D }$ by computing the mean over the spatial dimensions, and compute the pairwise differences between each pair of SMM features. (b) For editing, we guide the generation at each denoising step with our Pairwise SMM differences objective (b). See Sec. 4 for more details

![[assets/figures/papers/paper_list_l3_Space_Time_Diffusion_Features_for_Zero_Shot_Text_Driven_Motion_Transfer/figures/009_Figure_9.jpg]]
*Figure 9: Limitations. Our method struggles to preserve the original motion since the combination of the original motion and the edit prompt may be out of distribution for the T2V model*

![[assets/figures/papers/paper_list_l3_Space_Time_Diffusion_Features_for_Zero_Shot_Text_Driven_Motion_Transfer/figures/001_Figure_1.jpg]]
*Figure 1: Given an input video and a text prompt describing the target objects and scene, our method generates a new video in which the overall motion and scene layout of the input video are preserved, while allowing for notable structural and appearance changes*

本方法的核心思想是：利用一个预训练且冻结的文本到视频（T2V）扩散模型（ZeroScope），在不进行任何训练或微调的情况下，通过一个新颖的优化目标函数引导生成过程，实现零样本的跨类别运动迁移。整个框架的流程如图3所示，可分为两条并行的处理路径——驱动视频的特征提取路径与生成视频的引导去噪路径——二者通过**成对SMM差异损失**实现耦合。

**驱动视频的特征提取路径**由以下模块串联构成：

1. **DDIM反演**：给定输入视频 $V$，使用空文本提示进行DDIM反演，获得一系列潜变量 $[\mathbf{x}_1, \dots, \mathbf{x}_T]$。这些潜变量作为后续特征提取的载体。
2. **时空特征提取**：将每个时间步的潜变量 $\mathbf{x}_t$ 输入预训练T2V UNet，从中间层激活中提取时空特征 $\mathbf{f}(\mathbf{x}_t) \in \mathbb{R}^{F \times M \times N \times D}$，其中 $F$ 为帧数，$M \times N$ 为空间分辨率，$D$ 为特征通道数。
3. **SMM描述符计算**：对每帧的时空特征在空间维度上取均值，得到空间边缘均值（Spatial Marginal Mean, SMM）特征：
   $$\mathrm{SMM}[\mathbf{f}(\mathbf{x}_t)] = \frac{1}{M \cdot N} \sum_{i=1}^{M} \sum_{j=1}^{N} \mathbf{f}(\mathbf{x}_t)_{i,j}$$
   该操作将每帧的高维时空特征压缩为一个 $D$ 维全局描述符 $\phi^t \in \mathbb{R}^{D}$，编码了物体的姿态、位置和场景语义布局，同时对像素级外观变化具有鲁棒性。
4. **成对差异计算**：计算驱动视频各帧SMM特征之间的成对差异 $\Delta_{(i,j)}^{t} = \phi_i^{t} - \phi_j^{t}$，作为运动时序结构的紧凑表示。

**生成视频的引导去噪路径**由以下模块构成：

1. **低频滤波初始化**：不同于从随机噪声开始去噪，本方法将DDIM反演噪声 $\mathbf{x}_T$ 的低频分量与随机噪声 $\epsilon_0$ 的高频分量进行混合，得到初始潜变量：
   $$\tilde{\mathbf{x}}_T = LF_\xi(\mathbf{x}_T) + (\epsilon_0 - LF_\xi(\epsilon_0))$$
   其中 $LF_\xi$ 为截止频率 $\xi$ 的低通滤波操作。这一设计保留了驱动视频的粗略场景布局和物体位置信息，同时为外观和形状的编辑提供了足够的多样性空间。
2. **引导去噪**：在每一去噪步 $t$，从生成潜变量 $\tilde{\mathbf{x}}_t$ 中提取时空特征并计算其SMM描述符 $\tilde{\phi}^t$，进而得到成对差异 $\tilde{\Delta}_{(i,j)}^{t} = \tilde{\phi}_i^{t} - \tilde{\phi}_j^{t}$。然后通过最小化成对SMM差异损失来引导生成：
   $$\mathcal{L}\big(\mathrm{SMM}(\mathbf{f}(\mathbf{x}_t)), \mathrm{SMM}(\mathbf{f}(\tilde{\mathbf{x}}_t))\big) = \sum_{i} \sum_{j} \lVert \Delta_{(i,j)}^{t} - \tilde{\Delta}_{(i,j)}^{t} \rVert_2^2$$
   该损失函数通过梯度下降更新 $\tilde{\mathbf{x}}_t$，使生成视频的帧间运动模式与驱动视频保持一致。完整的优化-采样流程总结于Algorithm 1。

**输入输出流**：系统接收一个驱动视频和一个目标文本提示（描述期望的目标物体和场景），输出一个保留驱动视频整体运动和场景布局、同时呈现目标物体外观和形状的新视频。整个过程无需配对训练数据，也无需对预训练T2V模型进行任何参数更新。

> **证据强度说明**：上述pipeline描述基于论文Section 4.1-4.2的方法阐述及Figure 3的流程可视化，置信度较高。关于SMM特征对姿态和布局的编码能力，有Figure 2(c,d)的特征反演实验和最近邻检索实验作为实证支撑。低频滤波初始化的有效性在Figure 7(d-f)的消融实验中得到验证。

## 核心模块与公式推导

本方法的核心在于从预训练文本到视频扩散模型中提取时空特征，并构建一种对像素级变化鲁棒的全局运动描述符，进而通过成对差异优化实现运动迁移。整个框架无需任何训练或微调，仅依赖冻结的ZeroScope模型。

### 空间边缘均值描述符

给定输入视频，首先通过DDIM反演获得潜变量序列，并将其送入T2V UNet的中间层，提取时空特征 $\mathbf{f}(\mathbf{x}_t) \in \mathbb{R}^{F \times M \times N \times D}$，其中 $F$ 为帧数，$M \times N$ 为空间分辨率，$D$ 为特征通道数。

直接使用完整时空特征进行重建会严格约束像素级外观和形状，阻碍跨类别编辑。为此，提出**空间边缘均值**（Spatial Marginal Mean, SMM）描述符，对空间维度取均值，将每帧的高维特征压缩为一个全局向量：

$$\mathrm{SMM}[\mathbf{f}(\mathbf{x}_t)] = \frac{1}{M \cdot N} \sum_{i=1}^{M} \sum_{j=1}^{N} \mathbf{f}(\mathbf{x}_t)_{i,j}$$

该操作产生 $\mathbb{R}^{F \times D}$ 的每帧描述符。反演实验（Figure 2）证实：SMM描述符能够捕获物体的姿态、位置和场景语义布局，同时对像素级外观和形状变化保持鲁棒——使用SMM引导生成的反演视频呈现出正确的姿态和位置，但允许较大的结构和外观变化；基于SMM的最近邻检索也能在显著外观和视角变化下匹配到相同姿态的帧。

### 成对SMM差异损失

仅优化SMM特征的绝对值仍会保留部分原始外观信息，不足以充分匹配编辑文本。关键的因果调控旋钮是**成对SMM差异损失**：不直接对齐每帧的SMM值，而是保持驱动视频与生成视频中任意两帧之间SMM特征的相对变化关系。

对于驱动视频在去噪步 $t$ 的SMM特征 $\phi_i^t$，计算成对差异：

$$\Delta_{(i,j)}^{t} = \phi_i^{t} - \phi_j^{t}$$

同理，生成视频的成对差异记为 $\tilde{\Delta}_{(i,j)}^{t}$。损失函数最小化两者的L2距离：

$$\mathcal{L}\big(\mathrm{SMM}(\mathbf{f}(\mathbf{x}_t)), \mathrm{SMM}(\mathbf{f}(\tilde{\mathbf{x}}_t))\big) = \sum_{i} \sum_{j} \lVert \Delta_{(i,j)}^{t} - \tilde{\Delta}_{(i,j)}^{t} \rVert_2^2$$

这一设计的核心洞察在于：成对差异编码了帧间运动的相对变化模式，同时丢弃了绝对外观信息，从而在解耦外观和形状的同时保持整体运动特性。消融实验（Figure 7b-c）验证：使用完整时空特征重建会阻止外观和形状的任何偏离；仅优化SMM绝对值虽增加灵活性，但仍保留原始外观；而成对差异损失实现了最佳的运动保持与编辑自由度。

### 低频滤波初始化

去噪过程的初始潜变量直接影响生成结果的布局与多样性。方法采用**低频滤波初始化**，结合DDIM反演噪声的低频分量与随机噪声的高频分量：

$$\tilde{\mathbf{x}}_T = LF_\xi(\mathbf{x}_T) + (\epsilon_0 - LF_\xi(\epsilon_0))$$

其中 $LF_\xi$ 为低通滤波操作，$\mathbf{x}_T$ 为DDIM反演得到的噪声，$\epsilon_0$ 为随机采样的高斯噪声。低频分量保留输入视频的粗略场景布局和物体位置，高频随机分量则引入生成多样性。消融实验（Figure 7d-f）表明：去除优化步骤仅能从初始潜变量保留粗略布局；从纯随机噪声初始化会导致运动保真度显著下降；低频滤波与成对SMM差异损失的结合实现了最优的运动保持和编辑逼真度。

### 引导去噪流程

完整的生成过程在Algorithm 1中总结。在每个去噪步 $t$，计算当前生成潜变量 $\tilde{\mathbf{x}}_t$ 与驱动视频潜变量 $\mathbf{x}_t$ 的成对SMM差异损失，通过梯度下降更新 $\tilde{\mathbf{x}}_t$，随后执行一步DDIM去噪。该迭代优化在保持运动的同时，使生成结果逐步符合目标文本描述。

## 实验与分析

### 定量评估与用户研究

为评估运动迁移质量，本文设计了一个基于Chamfer距离的运动保真度指标（Motion-Fidelity Score，Eq. 5），该指标通过在输入和输出视频中提取轨迹集（tracklets），计算轨迹间位移向量的平均余弦相似度，从而量化运动保持程度。同时，采用CLIP文本相似度衡量生成视频与目标文本提示的编辑一致性。

在包含21个视频、54个视频-编辑对的测试集上，本方法与**TokenFlow**（Geyer et al., 2023）、**Tune-A-Video**（Wu et al., 2022）和**Control-A-Video**（Chen et al., 2023）三个基线进行了对比。如Figure 8所示，本方法在CLIP文本相似度与运动保真度之间取得了更优的平衡：在相近的CLIP得分下，本方法的运动保真度明显高于所有基线，表明成对SMM差异损失能有效解耦运动保持与外观编辑。

用户研究采用标准两两比较（2AFC）范式，共收集了来自150名参与者的7000次判断。结果如Table 1所示，本方法在所有对比中均获得显著偏好：

| 对比基线 | 用户偏好本方法比例 |
|:---|:---|
| TokenFlow | 72.57% |
| Tune-A-Video | 77.80% |
| Control-A-Video | 84.50% |

> **Table 1** 用户研究结果：报告本方法相对于各基线获得偏好投票的百分比。所有比较均在统计上显著，验证了成对SMM差异损失引导的生成过程在感知质量上的优势。

![[assets/figures/papers/paper_list_l3_Space_Time_Diffusion_Features_for_Zero_Shot_Text_Driven_Motion_Transfer/figures/010_Table_1.jpg]]
*Table 1: User Study. We report the percentage of judgments in our favour w.r.t. each baseline*

需注意，Gen-1（Esser et al., 2023）因输出视频长度不一致且部分帧重复，仅参与可视化比较（Figure 6），未纳入定量评估或用户研究。所有基线均使用官方代码运行，并尽力调整参数以获取最佳效果，确保比较公平性。

### 消融实验

Figure 7系统消融了损失函数和初始化策略两大核心设计选择，揭示了以下因果机制：

**损失函数消融（Figure 7 b-c）**：
- **全空间-时间特征重建**（Figure 7b）：直接使用完整的时空特征作为重建目标，导致生成视频几乎完全复制输入视频的外观和形状，无法实现跨类别编辑。这验证了SMM描述符对像素级信息解耦的关键作用。
- **SMM特征直接优化**（Figure 7c）：仅优化SMM特征的绝对值（而非成对差异），虽相比全特征重建增加了灵活性，但仍保留较多原始外观信息，无法充分匹配目标文本的编辑要求。这表明成对差异形式通过仅约束帧间相对变化，为外观编辑释放了更大的自由度。

**初始化策略消融（Figure 7 d-f）**：
- **无优化直接采样**（Figure 7d）：从DDIM逆噪声直接采样而不施加任何引导，仅能保留粗略的场景布局，无法维持精确的运动轨迹。
- **随机噪声初始化**（Figure 7e）：去除低频滤波（Eq. 4），从纯随机噪声开始优化，导致运动保真度显著下降。这证明DDIM逆噪声的低频分量携带了场景布局和物体初始位置的关键信息。
- **完整方法**（Figure 7f）：成对SMM差异损失与低频滤波初始化结合，实现了最佳的运动保持与编辑逼真度平衡。

消融实验的因果链条清晰：低频滤波初始化提供场景布局先验，成对SMM差异损失在去噪过程中约束帧间运动关系，二者协同实现了无需显式姿态模型的跨类别运动迁移。

### 定性比较

Figure 6展示了本方法与四个基线的定性对比。在“汽车漂移→摩托车”等跨类别场景中，TokenFlow倾向于保留原始物体的外观特征，Control-A-Video和Tune-A-Video虽能改变物体类别，但运动轨迹出现明显偏差或时序不一致。本方法在保持输入视频整体运动轨迹的同时，成功将物体替换为目标类别，并维持了细粒度的姿态变化（如摩托车的倾斜角度与输入汽车的漂移姿态一致）。

与**SA-NLA**（Loeschcke et al., 2022）的对比（Figure 5）进一步凸显了本方法的优势：SA-NLA依赖神经分层图集进行局部编辑，在处理大幅形状变化时图集分解容易失效，导致运动伪影；而本方法通过全局SMM描述符约束，天然支持整体物体的替换。

### 失败模式与局限性

Figure 9揭示了本方法的主要失败模式：当输入运动与编辑提示的目标物体组合对预训练T2V模型（ZeroScope）构成分布外（out-of-distribution）情况时，模型的生成先验无法有效将运动模式与目标物体结合，导致运动保真度下降。例如，将蛇的蜿蜒运动迁移到熊时，T2V模型缺乏“熊以蛇的方式移动”的生成先验，导致输出视频中熊的运动偏离输入模式。

此外，推理时间较长是实际部署的瓶颈：DDIM反演约需10分钟，带优化的采样根据配置需7-15分钟（Appendix B），离实时应用仍有显著距离。方法的零样本特性目前仅在ZeroScope上验证，对不同基座T2V模型的泛化能力尚未探索。

### 补充图表

![[assets/figures/papers/paper_list_l3_Space_Time_Diffusion_Features_for_Zero_Shot_Text_Driven_Motion_Transfer/figures/002_Figure_2.jpg]]
*Figure 2: Diffusion feature inversion via guided feature reconstruction. We extract space-time features f from an input video (a) and steer the generation process of a random sample to produce the same feature f , using feature reconstruction as guidance (b); the synthesized videos closely resemble the original video content in terms of appearance, shape, and pose. Replacing the full space-time features with their spatial marginal mean feature SMM[f ] allows for more flexibility (c); the SMM feature inversion results capture the original object pose, general position, and scene layout yet are not restricted to the original content at the pixel-level. This is also demonstrated in the nearest neighbor...*

## 方法谱系与知识库定位

### 1. 方法谱系：与基线的结构性差异

本节从“特征描述符—损失函数—初始化策略”三个核心设计槽位出发，定位本方法在零样本文本驱动运动迁移任务中的技术坐标。

#### 1.1 特征描述符：从全空间-时间特征到空间边缘均值（SMM）

现有基于扩散特征的视频编辑方法普遍依赖原始空间-时间特征的直接重建，或使用二维扩散模型的空间DIFT特征。**TokenFlow**（Geyer et al., 2023）通过联合编辑关键帧并传播一致性特征实现零样本视频编辑，但其特征表示缺乏对运动时序的显式建模。**Tune-A-Video**（Wu et al., 2022）在单视频上微调图像扩散模型的空间注意力，本质上仍以逐帧外观保真度为核心约束。**Control-A-Video**（Chen et al., 2023）将可控图像生成扩展至视频，通过深度图等条件保持每帧布局，但对跨类别运动迁移的灵活性不足。

本方法的关键差异在于提出**空间边缘均值（Spatial Marginal Mean, SMM）**作为每帧全局描述符：

$$\mathrm{SMM}[\mathbf{f}(\mathbf{x}_t)] = \frac{1}{M \cdot N} \sum_{i=1}^{M} \sum_{j=1}^{N} \mathbf{f}(\mathbf{x}_t)_{i,j}$$

该描述符通过对预训练文本到视频扩散模型中间层时空特征的空间维度取均值，保留了物体姿态、位置和场景语义布局等全局信息，同时对像素级外观和形状变化具有鲁棒性。反演实验（Figure 2c）和最近邻检索（Figure 2d）验证了SMM特征的这一性质：SMM反演结果能传达正确的姿态和位置，但允许较大的结构和外观变化；基于SMM的最近邻检索可找到姿态相同但外观和视角显著不同的帧。

#### 1.2 损失函数：从特征重建到成对SMM差异

损失函数的设计决定了运动保持与编辑灵活性之间的权衡。消融实验（Figure 7b）表明，使用全空间-时间特征重建作为损失函数会完全阻止外观和形状的偏离，无法实现有效的跨类别编辑。仅优化SMM特征本身（Figure 7c）虽增加了灵活性，但仍保留较多原始外观信息，难以充分匹配编辑文本。

本方法的核心创新是**成对SMM差异损失**：

$$\mathcal{L}\big(\mathrm{SMM}(\mathbf{f}(\mathbf{x}_t)), \mathrm{SMM}(\mathbf{f}(\tilde{\mathbf{x}}_t))\big) = \sum_{i} \sum_{j} \lVert \Delta_{(i,j)}^{t} - \tilde{\Delta}_{(i,j)}^{t} \rVert_2^2$$

其中 $\Delta_{(i,j)}^{t} = \phi_i^{t} - \phi_j^{t}$ 和 $\tilde{\Delta}_{(i,j)}^{t} = \tilde{\phi}_i^{t} - \tilde{\phi}_j^{t}$ 分别表示驱动视频和生成视频中各帧SMM特征的成对差异。该损失通过保持特征在时间维度上的相对变化模式，而非绝对值，实现了外观和形状信息的有效解耦，同时维持了整体运动的时序结构。

#### 1.3 初始化策略：低频滤波与随机高斯的混合

初始化策略直接影响生成结果的运动保真度和编辑多样性。消融实验（Figure 7d-e）表明：直接从初始潜变量采样而不进行优化，仅能保留粗略布局；从随机噪声初始化则导致运动保真度显著下降。

本方法采用**低频滤波初始化**：

$$\tilde{\mathbf{x}}_T = LF_\xi(\mathbf{x}_T) + (\epsilon_0 - LF_\xi(\epsilon_0))$$

该策略提取DDIM逆噪声的低频分量以保留物体位置和场景布局，同时用随机噪声的高频分量提供编辑多样性。与成对SMM差异损失结合时，实现了最佳的运动保持和编辑逼真度（Figure 7f）。

#### 1.4 与SA-NLA和Gen-1的定位关系

**SA-NLA**（Loeschcke et al., 2022）利用神经分层图集进行分层视频编辑，支持局部结构变化，但其运动迁移能力受限于图集表示的刚性约束。**Gen-1**（Esser et al., 2023）是基于结构/外观条件的视频生成模型，需要显式的条件输入，且输出视频长度不一致（部分帧重复），因此未纳入定量评估。本方法在零样本设定下，无需任何训练或微调，仅通过预训练且冻结的文本到视频扩散模型（ZeroScope）即可完成运动迁移，在灵活性上具有显著优势。

### 2. 适用边界与局限

#### 2.1 分布外（OOD）问题

当输入视频的运动与编辑提示的目标物体组合对于T2V模型是分布外时，方法难以维持原视频的运动特征（Figure 9）。例如，将“人跑步”的运动迁移到“鱼游动”时，T2V模型的生成先验可能无法有效结合该运动模式与目标物体，导致运动保真度下降。这一局限源于方法对预训练模型生成先验的依赖，而非优化框架本身。

#### 2.2 推理效率

当前方法的推理时间较长：DDIM反演约需10分钟，带优化的采样根据配置需7-15分钟（Appendix B），离实时应用仍有显著距离。这限制了其在交互式编辑场景中的实用性。

#### 2.3 模型依赖性

方法基于特定的预训练T2V模型（ZeroScope），在不同基座模型上的泛化能力未经验证。若更换底层模型，SMM特征的性质和损失函数的有效性可能需要重新评估。

#### 2.4 多对象与复杂遮挡

当前方法主要关注单个主要运动对象，对于多交互对象及复杂遮挡下的运动迁移尚未探索。在涉及多个独立运动实体的场景中，SMM作为全局描述符可能无法区分不同对象的运动模式。

### 3. 开放问题

1. **分布外鲁棒性**：如何设计机制使T2V模型的生成先验能更好地适应运动-目标组合的分布外情况？可能的思路包括引入额外的运动-外观解耦约束，或在推理时动态调整引导强度。

2. **跨模型泛化**：如何将框架推广到其他基础T2V模型（如ModelScope、VideoCrafter等），同时保持零样本特性？SMM特征的有效性是否依赖于特定模型架构或训练数据分布？

3. **推理加速**：能否通过模型蒸馏、更高效的优化策略（如少步采样、隐式梯度近似）或特征预计算显著降低推理时间？当前约20分钟的总推理时间限制了方法的规模化应用。

4. **多对象运动解耦**：如何将SMM描述符扩展为对象级或区域级的表示，以处理多交互对象及复杂遮挡下的运动迁移？这可能需要引入无监督的运动分割或注意力引导机制。

5. **长视频支持**：当前方法处理的是固定长度的短视频片段，如何扩展到更长视频，同时保持时序一致性和运动保真度，仍是一个待解决的问题。

## 原文 PDF

![[paperPDFs/CVPR_2024/Space_Time_Diffusion_Features_for_Zero_Shot_Text_Driven_Motion_Transfer.pdf]]
