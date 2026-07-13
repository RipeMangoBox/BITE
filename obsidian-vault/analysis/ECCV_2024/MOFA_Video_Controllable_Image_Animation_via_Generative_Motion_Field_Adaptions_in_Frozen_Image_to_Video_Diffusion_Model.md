---
title: "MOFA-Video: Controllable Image Animation via Generative Motion Field Adaptions in Frozen Image-to-Video Diffusion Model"
type: paper
paper_level: A
venue: ECCV
year: 2024
pdf_ref: paperPDFs/ECCV_2024/MOFA_Video_Controllable_Image_Animation_via_Generative_Motion_Field_Adaptions_in_Frozen_Image_to_Video_Diffusion_Model.pdf
project_link: https://myniuuu.github.io/MOFA_Video/
code_link: null
aliases:
- MV
- MOFA-Video
tags:
- ECCV_2024
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: "通过设计 MOFA-Adapter（生成式运动场适配器），将用户提供的稀疏控制信号（如点轨迹、面部关键点）显式地转换为密集运动光流场，并利用该光流场对参考帧的多尺度特征进行扭曲（warp），从而为冻结的视频扩散模型（SVD）提供强有力的逐帧运动引导。"
primary_logic: "所有类型的动画均可统一建模为基于稀疏关键点（或关键轨迹）的运动传播问题，因此可以构建一个统一的网络结构（MOFA-Adapter），将不同模态的稀疏控制信号转换为密集运动场，并注入到预训练的视频扩散模型中，实现泛化且可控的图像动画。"
claims:
- "MOFA-Adapter通过稀疏到密集的运动生成网络从稀疏提示中生成密集运动场，并利用该场扭曲参考帧的多尺度特征以引导扩散生成。"
- "多个MOFA-Adapters可以针对不同的控制域（如手动轨迹、面部关键点）单独训练，并能在零样本下组合使用，实现多域联合控制。"
- "在轨迹动画任务上，所提方法在LPIPS (0.2274)、FID (16.82)、FVD (86.76) 和用户偏好上均优于DragNUWA。"
- "Trajectory-based Image Animation 上 LPIPS↓ = 0.2274"
---

# MOFA-Video: Controllable Image Animation via Generative Motion Field Adaptions in Frozen Image-to-Video Diffusion Model

> [!tip] 核心洞察
> 所有类型的动画均可统一建模为基于稀疏关键点（或关键轨迹）的运动传播问题，因此可以构建一个统一的网络结构（MOFA-Adapter），将不同模态的稀疏控制信号转换为密集运动场，并注入到预训练的视频扩散模型中，实现泛化且可控的图像动画。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | MOFA-Video：通过冻结图像到视频扩散模型中的生成式运动场适应实现可控图像动画 |
| 英文题名 | MOFA-Video: Controllable Image Animation via Generative Motion Field Adaptions in Frozen Image-to-Video Diffusion Model |
| 会议/期刊 | ECCV 2024 |
| Links | [paper](https://arxiv.org/abs/2405.20222) · [Project](https://myniuuu.github.io/MOFA_Video/) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/image_and_video_generation |
| Method | MOFA-Video |
| Dataset | Trajectory-based Image Animation |

> [!tip] 效果简介
> - Trajectory-based Image Animation 上，LPIPS↓ 为 0.2274，对比 0.2705 (DragNUWA)，变化 -0.0431。
> - Trajectory-based Image Animation 上，FID↓ 为 16.82，对比 19.66 (DragNUWA)，变化 -2.84。
> - Trajectory-based Image Animation 上，FVD↓ 为 86.76，对比 91.38 (DragNUWA)，变化 -4.62。

## 概要

**问题瓶颈**：现有的图像到视频（I2V）扩散模型在通用图像上缺乏跨多个运动域（物体轨迹、人脸表情、相机运动）的细粒度、显式运动控制能力；特定领域的动画方法则难以泛化至开放场景。

**核心思路**：MOFA-Video 在冻结的 Stable Video Diffusion（SVD）主干上引入生成式运动场适配器（MOFA-Adapter），将用户提供的稀疏控制信号（如点轨迹、面部关键点）显式转换为密集运动光流场，并利用该光流场对参考帧的多尺度特征进行扭曲（warp），从而为扩散生成过程提供逐帧运动引导。

**因果机制**：所有类型的动画均可统一建模为基于稀疏关键点（或关键轨迹）的运动传播问题。MOFA-Adapter 通过稀疏到密集（S2D）运动生成网络，将不同模态的稀疏控制信号统一转换为密集运动场，再注入冻结的 SVD 模型，实现泛化的可控图像动画。

**方法定位**：MOFA-Video 属于基于预训练视频扩散模型的适配器方法，类似于 ControlNet 的思想——冻结主干网络参数，仅训练轻量级适配器来增加新的控制能力。不同的是，MOFA-Adapter 的核心在于显式运动场的生成与特征扭曲，而非直接将控制信号作为条件输入。

**主要结果**：
- 在轨迹驱动动画任务上，MOFA-Video 在 LPIPS（0.2274）、FID（16.82）、FVD（86.76）及用户偏好上均显著优于 DragNUWA（Yin et al., arXiv 2023）。
- 在人像动画任务上，CPBD（0.4075）和身份保持度 ID（0.9293）优于 SadTalker（Zhang et al., CVPR 2023）和 StyleHEAT（Yin et al., ECCV 2022）。
- 多个 MOFA-Adapter 可在零样本下组合使用，实现多域联合控制（如同时控制轨迹与人脸表情），无需重新训练。

**局限与开放问题**：在大范围或剧烈运动引导下可能产生结构丢失或模糊等视觉伪影；尚未解决生成与参考图像内容差异较大的新运动或新视图的问题。



### 核心瓶颈

图像到视频（I2V）扩散模型在通用图像动画生成上面临一个关键矛盾：一方面，现有模型缺乏跨运动域的细粒度、显式运动控制能力——用户无法精确指定物体轨迹、人脸表情或相机运动；另一方面，特定领域的动画方法（如音频驱动的人脸动画）虽然在各自领域内表现良好，却无法泛化到开放场景。这一瓶颈的根源在于，不同运动模态的控制信号形态差异巨大（稀疏轨迹点、面部关键点序列、相机参数等），而统一的、可泛化的运动注入机制尚未建立。

### 现有方法的缺口

在轨迹驱动的图像动画任务上，**DragNUWA**（Yin et al., arXiv 2023）等基线方法尝试将稀疏运动提示直接作为条件信号输入网络，但缺乏从稀疏控制到密集运动场的显式建模，导致对复杂非线性运动的控制精度不足。在人脸动画领域，**SadTalker**（Zhang et al., CVPR 2023）和**StyleHEAT**（Yin et al., ECCV 2022）等方法依赖特定的人脸先验和3D关键点提取器，无法迁移到通用物体或场景的动画任务中。商业模型如**Gen-2**虽然支持一定程度的运动控制，但采用掩码加方向的粗粒度方式，难以处理复杂运动（如眨眼等非线性控制）。在相机运动控制方面，**MotionCtrl**（Wang et al., arXiv 2023）提供了相机参数的注入方式，但其控制域与其他运动模态相互独立，无法在同一框架内联合使用。

### 本文动机

上述缺口的共同本质在于：**缺乏一种将不同模态的稀疏控制信号统一转化为密集运动引导的通用机制**。本文的核心洞察是：所有类型的图像动画均可统一建模为基于稀疏关键点（或关键轨迹）的运动传播问题——无论是用户绘制的物体运动轨迹、音频驱动的人脸关键点位移，还是相机运动模式，都可以被表达为帧间的稀疏运动向量。基于此，MOFA-Video提出在冻结的图像到视频扩散模型（Stable Video Diffusion）之上，设计生成式运动场适配器（MOFA-Adapter），将各类稀疏控制信号显式地转换为密集光流场，并通过特征扭曲（warping）机制将运动信息注入生成过程，从而实现跨域、可组合的通用图像动画控制。



## 核心方法与创新机理

MOFA-Video 的核心创新在于提出了一种**统一的运动场适配器（MOFA-Adapter）**，将不同模态、不同领域的稀疏运动控制信号转化为密集光流场，并以此为桥梁，向冻结的图像到视频扩散模型（Stable Video Diffusion, SVD）注入显式的、细粒度的逐帧运动引导。这一设计从根本上改变了现有 I2V 模型“仅依赖文本条件”或“为每个运动域单独建模”的范式。

### 1. 从稀疏控制到密集运动场的统一生成

现有方法（如 **DragNUWA**, Yin et al., arXiv 2023）通常直接将稀疏运动提示（如点轨迹）作为条件信号输入网络，缺乏对中间运动场的显式建模。MOFA-Video 的关键改变在于引入了一个**稀疏到密集运动生成网络（S2D Network）**，先将用户提供的稀疏控制信号（手绘轨迹、面部关键点序列、相机运动参数等）显式地转化为密集的帧间光流场，再基于该光流场对参考帧的多尺度特征进行扭曲（warp），最终将扭曲后的特征作为条件注入扩散生成过程。

这一“生成-扭曲-注入”的三段式管线带来了两个直接优势：
- **控制精度提升**：密集运动场提供了像素级的运动先验，使生成视频中的物体位移与用户意图高度一致。消融实验（Fig. 10, Table 3）证实，去除扭曲操作的“稀疏条件模型（Sparse-conditioning）”和去除 S2D 网络的“稀疏扭曲模型（Sparse-warping）”在可控性和合成质量上均显著劣于完整模型。
- **运动域统一**：不同来源的稀疏控制信号（轨迹点、人脸关键点、相机运动）均被抽象为“稀疏运动向量”，由同一 S2D 网络结构处理。这使得 MOFA-Adapter 成为一个跨域通用的运动注入模块，而非针对单一任务的专用设计。

### 2. 冻结主干网络下的多域适配器架构

MOFA-Video 的另一个关键设计选择是**完全冻结预训练的视频扩散模型（SVD）参数**，仅训练轻量的 MOFA-Adapter。这借鉴了 ControlNet 的思路，但在视频生成领域实现了多运动域的扩展：

- **独立训练，零样本组合**：针对手动轨迹、面部关键点、相机运动等不同控制域，可分别训练独立的 MOFA-Adapter。由于 SVD 主干保持冻结，多个适配器可以在推理时直接组合使用，通过掩码感知策略（mask-aware strategy）定义各适配器的控制区域，实现多域联合控制（如同时控制人物面部表情和身体运动轨迹），无需重新训练。
- **与基线方法的本质差异**：**SadTalker** (Zhang et al., CVPR 2023) 和 **StyleHEAT** (Yin et al., ECCV 2022) 等特定领域方法需要为音频驱动的人脸动画设计专用架构；**MotionCtrl** (Wang et al., arXiv 2023) 则专注于相机运动控制。MOFA-Video 通过统一的 MOFA-Adapter 结构覆盖了这些分散的能力，且各适配器可灵活组合。

### 3. 运动信息利用方式的根本转变

与直接将稀疏提示作为条件的基线方法相比，MOFA-Video 的**特征扭曲机制**是性能提升的核心因果节点。具体而言：

- **基线做法**（Sparse-conditioning）：稀疏运动提示被直接编码并拼接到噪声潜变量中，网络需要隐式地学习从稀疏点到密集运动的映射，这增加了学习难度，且容易导致控制不精确。
- **MOFA-Video 做法**：S2D 网络显式生成密集运动场，随后利用该场对参考帧的**多尺度特征**进行扭曲。扭曲后的特征已经包含了运动后的空间结构信息，扩散模型只需在此基础上补充纹理和细节，大幅降低了生成任务的难度。

定量结果验证了这一转变的有效性：在轨迹驱动的图像动画任务上，MOFA-Video 在 LPIPS（0.2274 vs. 0.2705）、FID（16.82 vs. 19.66）和 FVD（86.76 vs. 91.38）上均显著优于 DragNUWA，用户偏好评分也更优（Table 1）。

### 4. 长视频生成的周期性采样策略

SVD 原生支持固定帧数（14 帧）的生成。为突破这一限制，MOFA-Video 提出了**周期性采样策略（Periodic Sampling）**：将长视频划分为重叠 7 帧的 14 帧片段组，在潜空间中对重叠帧进行逐帧平均融合。消融实验（Fig. 11）表明，该策略有效避免了“动态条件法”导致的过曝问题和“零条件法”导致的片段间突变，实现了平滑的长视频生成。这一策略本身是推理阶段的工程创新，但其有效性依赖于 MOFA-Adapter 提供的稳定帧间运动引导。

---

**证据强度说明**：上述核心创新点均有明确的论文原文锚点（Sec. 3.1, Fig. 2, Fig. 3, Fig. 10, Table 1, Table 3）和消融实验支持，置信度较高。关于两阶段训练策略（先训练光流重建，再微调 S2D 网络）对最终性能的必要性，论文在实现细节中提及但未提供独立的消融验证，该点置信度相对较低（约 0.8），需读者注意。



![[assets/figures/papers/paper_list_l5_MOFA_Video_Controllable_Image_Animation_via_Generative_Motion_Field_Adap/figures/002_Figure_2.jpg]]
*Figure 2: Overview of MOFA-Video. We design MOFA-Adadpters for adapting the motions from different domains with a unified structure on the frozen Video Diffusion Model. It generates the video from a single image and the corresponding sparse motion hints. For training, we generate the sparse motion hints through sparse motion sampling and then train different MOFA-Adapters to generate video via pre-trained SVD [7]*

MOFA-Video 的整体 pipeline 围绕一个核心设计展开：**在冻结的预训练视频扩散模型（Stable Video Diffusion, SVD）之上，通过轻量的 MOFA-Adapter 注入显式的运动控制能力**。其关键思路是将不同模态的稀疏运动控制信号（手动轨迹、面部关键点序列、相机运动模式等）统一转换为密集运动光流场，并利用该光流场对参考帧的多尺度特征进行扭曲（warp），从而为扩散生成过程提供逐帧的运动引导。

### 模块组成与数据流

系统由四个核心模块构成，数据流如图 2 所示：

1. **Reference Encoder（参考编码器）**  
   一个多尺度卷积特征编码器，负责从输入的参考图像 $I$ 中提取多尺度特征。这些特征将在后续步骤中被密集运动场扭曲，作为条件信号注入生成过程。

2. **Sparse-to-Dense (S2D) Motion Generator（稀疏到密集运动生成网络）**  
   这是 MOFA-Adapter 的核心组件。它接收稀疏运动提示 $\boldsymbol{F}^s$（如采样点处的光流向量或关键点位移），输出完整的密集运动光流场。该网络本质上执行一个运动传播任务：从少量控制点的运动信息推断全图所有像素的运动。

3. **Fusion Encoder（融合编码器）**  
   架构与 SVD Encoder 完全一致，但权重可训练。它将经密集运动场扭曲后的参考特征与时间步 $t$、噪声潜变量 $\mathcal{V}_t$ 融合，生成空间-时间条件特征，注入冻结的 SVD 编码器-解码器结构。详细特征融合架构见 Fig. 13。

4. **Frozen Stable Video Diffusion (SVD) Model（冻结的 SVD 主干网络）**  
   作为图像到视频的去噪扩散生成主干，参数完全冻结。SVD 接收融合后的条件特征，在潜空间执行去噪过程，最终解码为视频帧序列。

### 训练与推理流程

**训练阶段**，系统从视频数据中自动构建稀疏运动提示。对于通用视频，采用分水岭采样策略在密集光流场上采样 $n$ 个空间点，仅保留采样点处的运动向量（Eq. 1），其余位置置零；对于人脸视频，则将面部关键点的帧间位移作为点状稀疏运动流（Eq. 2）。MOFA-Adapter 的优化目标是最小化重建视频潜变量与原始视频潜变量之间的均方误差（Eq. 3），迫使网络学会从稀疏提示中恢复密集运动信息。

**推理阶段**，用户提供参考图像和稀疏控制信号。对于手动轨迹，系统通过插值将轨迹点分配到各帧，并计算每帧轨迹点相对于起始点的位移作为稀疏运动提示（Eq. 4）；对于人脸动画，则从音频驱动的面部关键点序列中提取位移。S2D 网络据此生成密集运动场，驱动参考特征的扭曲与融合，最终由 SVD 生成受控视频。

### 多域控制与长视频生成

该框架的一个关键特性是**多 MOFA-Adapter 的零样本组合**。由于 SVD 参数冻结，不同运动域（轨迹、人脸、相机）的 MOFA-Adapter 可以独立训练，并在推理时通过掩码感知策略（mask-aware strategy）指定各适配器的控制区域，实现多域联合控制（如同时控制物体移动和人脸表情），无需重新训练。这一设计类似于 ControlNet 的多条件组合范式。

对于长视频生成，框架采用**周期性采样策略（Periodic Sampling）**：以 14 帧为一组进行去噪，相邻组之间重叠 7 帧，在潜空间对重叠帧进行逐帧平均融合。该方法有效缓解了简单分段推理导致的误差累积（过曝）和片段间突变问题（Fig. 11）。

### 关键设计决策

消融实验（Fig. 10, Table 3）揭示了两个决定性设计选择：
- **S2D 网络 + 特征扭曲的完整结构**在可控性和合成质量上均显著优于仅使用稀疏条件注入（Sparse-conditioning，无 warping）或仅对稀疏点进行扭曲（Sparse-warping，无 S2D 网络）的变体。
- **域感知的适配器训练**是必要的：直接使用轨迹域训练的 MOFA-Adapter 处理人脸动画会导致质量下降（Fig. 12），验证了为不同运动域训练专门适配器的合理性。



### 关键模块架构

MOFA-Video 的核心由**冻结的 Stable Video Diffusion (SVD)** 主干网络和若干个可训练的 **MOFA-Adapter** 组成。每个 MOFA-Adapter 内部包含三个子模块（Fig. 3）：

1. **Reference Encoder（参考帧编码器）**：一个多尺度卷积特征编码器，从输入的参考图像 $I$ 中提取多尺度特征，供后续运动扭曲使用。
2. **Sparse-to-Dense (S2D) Motion Generator（稀疏到密集运动生成网络）**：接收稀疏运动控制信号（如点轨迹、面部关键点），生成与视频帧数对应的密集运动光流场。
3. **Fusion Encoder（融合编码器）**：架构与 SVD 编码器完全一致，权重从其初始化。它将经密集运动场扭曲后的参考特征与时间步、噪声潜变量融合，注入冻结的 SVD 编解码流程中。

多个 MOFA-Adapter 可针对不同运动域（手动轨迹、人脸关键点、相机运动）独立训练，并在推理时通过掩码感知策略零样本组合，实现多域联合控制（Fig. 7）。

### 核心公式推导

**稀疏运动向量的统一表示** 是方法的基础。论文将不同模态的运动控制信号统一建模为稀疏运动向量 $F^s$。

**从密集光流采样稀疏运动向量**（Eq. 1）。给定视频的密集光流 $F$ 和通过分水岭采样策略得到的稀疏掩膜 $M^s$，稀疏运动向量定义为仅在采样点保留运动信息：

$$F_{:,:,i,j}^{s} = \left\{ \begin{array}{ll} F_{:,:,i,j} & \mathrm{if~} M_{i,j}^{s} = 1, \\ 0 & \mathrm{if~} M_{i,j}^{s} = 0. \end{array} \right.$$

其中 $i,j$ 为空间坐标，$M^s_{i,j}=1$ 表示该位置被采样。

**从结构化人脸关键点构建稀疏运动向量**（Eq. 2）。对于人脸动画，将视频帧中人脸关键点位置 $P[l,k,:]$ 与参考帧关键点 $\hat{P}[k,:]$ 的位移差作为稀疏运动流：

$$F^{s}[l-1,:,\hat{P}[k,0],\hat{P}[k,1]] = P[l,k,:] - \hat{P}[k,:]$$

其中 $l$ 为帧索引，$k$ 为关键点索引。

**用户手绘轨迹的稀疏运动提示计算**（Eq. 4）。对于用户绘制的轨迹，先插值得到序列 $\hat{\mathcal{T}}$，然后计算每一点相对起始点的位移：

$$F^{s}[l-1,:,\hat{\mathcal{T}}[0,0],\hat{\mathcal{T}}[0,1]] = \hat{\mathcal{T}}[l,:] - \hat{\mathcal{T}}[0,:]$$

**训练目标函数**（Eq. 3）。MOFA-Adapter 的优化目标是利用含噪潜变量 $\mathcal{V}_t$、时间步 $t$、参考图像 $I$ 和稀疏运动提示 $\boldsymbol{F}^s$，通过冻结的 SVD 去噪函数 $\mathcal{S}$ 重建原始视频潜变量 $\mathcal{V}$：

$$\mathcal{L} = || \mathcal{S}(\mathcal{V}_t, t, \mathcal{M}(\mathcal{V}_t, t, I, \boldsymbol{F}^s; \theta_{\mathcal{M}})) - \mathcal{V} ||^2$$

其中 $\mathcal{M}$ 为 MOFA-Adapter，$\theta_{\mathcal{M}}$ 为其可训练参数。该均方误差损失驱动 S2D 网络学会从稀疏提示生成准确的密集运动场，并指导特征扭曲的有效性。

### 长视频生成的周期性采样

为突破 SVD 固定帧数限制，MOFA-Video 采用周期性采样策略（Fig. 6）：每次以 14 帧为一组进行去噪，相邻组之间重叠 7 帧，在潜空间中对重叠帧进行逐帧平均以平滑过渡。该策略有效避免了动态条件法导致的过曝和零条件法导致的片段间突变（Fig. 11）。



## 实验与关键发现

### 主实验结果

MOFA-Video 在两个核心任务上进行了定量评估：基于轨迹的图像动画和基于音频驱动的肖像动画。所有实验均与当前领域最优方法进行了公平对比，其中轨迹动画任务的基线方法 **DragNUWA**（Yin et al., arXiv 2023）在与本文相同的 WebVid-10M 数据子集上进行了复现与重新训练。

**轨迹驱动图像动画**

在轨迹驱动任务上，MOFA-Video 在所有自动评估指标和用户偏好上均显著优于 DragNUWA。具体而言：

- **感知质量（LPIPS↓）**：0.2274 vs. 0.2705，降低了 0.0431，表明生成帧与参考图像在感知特征空间中更为一致。
- **图像质量（FID↓）**：16.82 vs. 19.66，降低了 2.84，生成帧的分布更接近真实图像。
- **视频质量（FVD↓）**：86.76 vs. 91.38，降低了 4.62，视频整体的时序一致性更强。
- **帧一致性（Fra.Con.↑）**：0.9390 vs. 0.9302，提升了 0.0088，相邻帧之间的连贯性更好。

用户研究进一步验证了上述结论：在控制精度（Ctrl.Pre.）上，MOFA-Video 获得 3.58 分，远高于 DragNUWA 的 2.76 分；在视觉质量（Vis.Qua.）上，MOFA-Video 获得 3.42 分，同样优于 DragNUWA 的 3.18 分。这表明用户明显更偏好 MOFA-Video 对运动轨迹的精确响应和生成结果的视觉保真度。

**肖像动画**

在音频驱动的肖像动画任务上，MOFA-Video 与 **SadTalker**（Zhang et al., CVPR 2023）和 **StyleHEAT**（Yin et al., ECCV 2022）进行了对比。定量结果如下：

- **清晰度（CPBD↑）**：0.4075，显著高于 SadTalker 的 0.3218 和 StyleHEAT 的 0.3534，表明生成的人脸区域更清晰。
- **身份保持（ID↑）**：0.9293，优于 SadTalker 的 0.9188 和 StyleHEAT 的 0.9119，说明生成的人脸更好地保留了原始身份特征。
- **感知质量（LPIPS↓）**：0.2099，低于 SadTalker 的 0.2308，进一步证实了感知质量的提升。

用户研究同样显示 MOFA-Video 在保真度（Fide.）、自然度（Natur.）和视觉质量（Vis.Qua.）上均获得最高评分。

**相机运动控制与多域组合**

轨迹域 MOFA-Adapter 还可用于相机运动控制——通过输入固定的密集光流模式（如平移、缩放、旋转），实现对全局视角变化的精确引导，在定性对比中优于 **MotionCtrl**（Wang et al., arXiv 2023）。此外，多个 MOFA-Adapter 可在零样本下组合使用，同时控制物体轨迹和人脸表情，实现复杂的多域动画，而无需重新训练。

### 消融实验

消融实验围绕网络设计、长视频推理策略和域感知适配器三个方面展开，验证了 MOFA-Video 各核心组件的必要性。

**网络设计消融**

将完整模型与三个变体进行对比：
1. **Sparse-conditioning（无扭曲）**：移除特征扭曲操作，直接将稀疏运动提示作为条件信号输入网络。
2. **Sparse-warping（无 S2D 网络）**：移除稀疏到密集运动生成网络，仅使用稀疏运动场进行特征扭曲。
3. **Non-tuning（无微调）**：完全不进行适配器训练，仅使用冻结的 SVD 模型。

结果表明，完整模型在可控性和合成质量上均达到最优。去除扭曲操作会导致运动控制精度显著下降；去除 S2D 网络则使运动场过于稀疏，无法提供足够的引导信号；不进行微调则完全丧失运动控制能力。定量结果（Table 3）进一步确认了完整模型在所有指标上的最佳平衡。


![[assets/figures/papers/paper_list_l5_MOFA_Video_Controllable_Image_Animation_via_Generative_Motion_Field_Adap/figures/015_Table_3.jpg]]
*Table 3: Quantitative comparison results for ablation study on trajectory-based image animation*

**长视频推理策略消融**

针对 SVD 固定帧数限制，论文对比了三种长视频生成策略：
- **Dynamic-conditional Naive Separation**：将前一段的最后一帧作为下一段的条件帧，会导致误差累积和过曝现象。
- **Zero-conditional Naive Separation**：始终以原始输入帧为条件，但片段间无重叠，会导致片段间突变。
- **Periodic Sampling（本文提出）**：以 14 帧为一组，组间重叠 7 帧，在潜空间中进行逐帧平均融合。

实验显示，周期性采样策略成功解决了前两种方法的过曝和时序不连续问题，能够生成平滑的长视频序列。

**域感知适配器消融**

直接使用轨迹域训练的 MOFA-Adapter 处理人脸动画任务，结果质量不佳，出现明显的结构失真和运动不自然。这证实了为不同运动域训练专门适配器的必要性——尽管适配器共享统一的 S2D 网络结构，但不同域的稀疏控制信号分布差异较大，需要独立的参数学习。

### 失败模式与局限性

尽管 MOFA-Video 在多个任务上表现优异，但仍存在以下已知局限：

1. **大范围运动下的视觉伪影**：当运动引导幅度较大或剧烈时，生成的视频可能出现结构丢失或模糊等视觉伪影。这一问题在极端轨迹或大幅度面部运动场景中尤为明显。
2. **内容生成能力受限**：MOFA-Video 的核心机制是基于参考帧特征的扭曲，因此无法生成与给定参考图像内容差异显著的新运动或新视图。该方法本质上是对现有像素的重排与变形，而非创造全新的视觉内容。

### 补充图表

![[assets/figures/papers/paper_list_l5_MOFA_Video_Controllable_Image_Animation_via_Generative_Motion_Field_Adap/figures/009_Table_1.jpg]]
*Table 1: Quantitative comparison and user study results for trajectory-based image animation. Table 2: Quantitative comparison and user study results for portrait image animation*




## 定位与知识库关联

### 与现有基线的关系

MOFA-Video 的核心贡献在于为冻结的图像到视频扩散模型（Stable Video Diffusion, SVD）赋予跨运动域的显式控制能力，其设计思路直接对标并改进了以下基线方法：

**轨迹驱动动画方面**，与 **DragNUWA**（Yin et al., arXiv 2023）形成最直接的对比。DragNUWA 将稀疏运动提示直接作为条件信号输入网络，而 MOFA-Video 通过 Sparse-to-Dense（S2D）运动生成网络先将稀疏轨迹转换为密集光流场，再利用该光流场对参考帧的多尺度特征进行扭曲（warp），从而为扩散模型提供更强的逐帧运动引导。在相同 WebVid-10M 数据子集上复现并重新训练 DragNUWA 的公平对比中，MOFA-Video 在 LPIPS（0.2274 vs. 0.2705）、FID（16.82 vs. 19.66）、FVD（86.76 vs. 91.38）以及用户控制精度偏好上均取得显著优势（Table 1）。此外，MOFA-Video 还能通过运动画笔（motion brushes）实现 DragNUWA 难以处理的非线性精细控制（如眨眼），相比之下商业模型 **Gen-2** 的“掩码+方向”范式在复杂运动管理上同样存在局限（Fig. 19）。

**相机运动控制方面**，与 **MotionCtrl**（Wang et al., arXiv 2023）形成对照。MOFA-Video 的轨迹域 MOFA-Adapter 可直接通过固定光流模式实现平移、缩放、旋转等相机运动控制（Fig. 15），展示了统一架构对不同运动类型的泛化能力。

**人像动画方面**，与 **SadTalker**（Zhang et al., CVPR 2023）和 **StyleHEAT**（Yin et al., ECCV 2022）形成对比。MOFA-Video 的人脸 MOFA-Adapter 利用 SadTalker 从音频生成的面部关键点序列作为稀疏控制信号，在清晰度（CPBD: 0.4075 vs. SadTalker 0.3218 / StyleHEAT 0.3534）、身份保持（ID: 0.9293 vs. 0.9188 / 0.9119）及用户偏好的自然度和视觉质量上均显著优于两者（Table 2），且 LPIPS 指标同样占优（0.2099 vs. SadTalker 0.2308）。

**架构设计层面**，MOFA-Video 借鉴了 **ControlNet** 的“冻结主干+可训练适配器”范式。但与 ControlNet 在图像域添加空间条件不同，MOFA-Adapter 的核心创新在于通过生成式运动场适配器将稀疏控制信号显式转换为密集运动流，并以特征扭曲的方式注入时序信息。多个 MOFA-Adapter 可独立训练并零样本组合（类似 Multi-ControlNet），实现轨迹与人脸关键点的联合控制（Fig. 7），而无需重新训练。

### 适用边界与局限

**适用场景**：MOFA-Video 适用于需要从单张参考图像出发、通过显式稀疏控制信号（手绘轨迹、面部关键点序列、固定光流模式）生成可控视频的任务。其统一架构覆盖了物体运动轨迹控制、音频驱动人像动画、相机运动控制等多个运动域，并支持多适配器零样本组合以实现更复杂的联合控制。

**已知局限**：
1. **大范围运动的视觉伪影**：在大范围或剧烈的运动引导下，生成的视频可能出现结构丢失或模糊等视觉伪影（Fig. 21）。这表明 S2D 网络生成的密集运动场在极端位移下的准确性仍有提升空间，扭曲操作可能引入不可逆的特征畸变。
2. **内容变化幅度受限**：该方法本质上是对参考帧特征的运动驱动扭曲，无法生成与给定参考图像内容差异较大的新运动或新视图。这意味着 MOFA-Video 不适用于需要大幅改变场景内容或生成全新视角的任务。
3. **域间适配器不可互换**：消融实验表明，直接使用未针对人像动画微调的轨迹域 MOFA-Adapter 处理人脸动画会导致质量不佳（Fig. 12），验证了为不同运动域训练专门适配器的必要性，也说明当前架构尚未实现完全的域无关运动控制。

### 开放问题

1. **如何生成与参考图像内容差异巨大的新运动或新场景？** 当前方法受限于“扭曲参考特征”的范式，本质上是对已有内容的运动重排。突破这一限制可能需要引入生成式先验来补充被遮挡区域或合成全新内容，而非仅依赖光流扭曲。
2. **如何进一步缓解大范围运动下的视觉伪影？** 现有 S2D 网络和特征扭曲机制在极端运动下表现不足，可能的改进方向包括：引入多帧参考信息以覆盖更大位移、设计更鲁棒的运动场正则化策略、或在扭曲后增加修复网络以补偿失真。
3. **能否实现完全域无关的统一运动控制器？** 当前仍需为不同运动域训练独立适配器。探索更通用的稀疏运动表征（如统一的关键点抽象）和跨域迁移学习策略，可能减少对域特定微调的依赖。
4. **长视频生成的时序一致性与误差累积问题**：虽然周期性采样策略缓解了片段间突变和过曝问题（Fig. 11），但长序列生成中的误差累积和运动漂移仍然是开放挑战，需要更有效的时序一致性约束机制。



## 原文 PDF

![[paperPDFs/ECCV_2024/MOFA_Video_Controllable_Image_Animation_via_Generative_Motion_Field_Adaptions_in_Frozen_Image_to_Video_Diffusion_Model.pdf]]
