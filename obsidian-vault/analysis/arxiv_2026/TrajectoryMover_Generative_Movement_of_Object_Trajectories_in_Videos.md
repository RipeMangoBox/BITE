---
title: "TrajectoryMover: Generative Movement of Object Trajectories in Videos"
type: paper
paper_level: A
venue: arXiv
year: 2026
pdf_ref: paperPDFs/arxiv_2026/TrajectoryMover_Generative_Movement_of_Object_Trajectories_in_Videos.pdf
aliases:
- TrajectoryMover
tags:
- arxiv_2026
- topic/vision_multimodal_applications
- topic/generative_models_diffusion
- topic/benchmarks_datasets_evaluation
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: TrajectoryAtlas 合成数据生成管道，通过物理模拟和在线场景修改自动创建大规模、多样化且具有场景交互的轨迹移动视频对。
primary_logic: 将轨迹移动重新定义为视频到视频的生成任务，利用合成配对数据微调扩散模型，并采用交替训练策略保存原始生成先验，从而仅通过简单的边界框控制即可实现保持物体身份和场景合理性的轨迹平移。
claims:
- TrajectoryMover 在背景保留 (SSIM_bg 0.92)、前景身份 (DINO_fg 0.45)、轨迹遵循度 (IoU_traj 0.27) 以及用户合理性研究 (Bradley‑Terry strength 1.25) 上全面优于现有基线，例如轨迹遵循度比 SFM 提高 +0.04，用户合理性比 ATI 提高 +1.52。
- TrajectoryAtlas test set (40 videos) 上 IoU_traj ↑ (轨迹遵循度) = 0.27
- TrajectoryAtlas test set user study 上 Bradley‑Terry plausibility strength u_m ↑ = 1.25
- 将轨迹移动重新定义为视频到视频的生成任务，利用合成配对数据微调扩散模型，并采用交替训练策略保存原始生成先验，从而仅通过简单的边界框控制即可实现保持物体身份和场景合理性的轨迹平移。
---

# TrajectoryMover: Generative Movement of Object Trajectories in Videos

> [!tip] 核心洞察
> 将轨迹移动重新定义为视频到视频的生成任务，利用合成配对数据微调扩散模型，并采用交替训练策略保存原始生成先验，从而仅通过简单的边界框控制即可实现保持物体身份和场景合理性的轨迹平移。

| 字段 | 内容 |
|------|------|
| 中文题名 | TrajectoryMover：视频中物体轨迹的生成式移动 |
| 英文题名 | TrajectoryMover: Generative Movement of Object Trajectories in Videos |
| 会议/期刊 | arXiv 2026 |
| Links | [paper](https://arxiv.org/abs/2603.29092) |
| Topic | #topic/vision_multimodal_applications #topic/generative_models_diffusion #topic/benchmarks_datasets_evaluation #topic/vision_multimodal_applications/image_and_video_generation |
| Method | TrajectoryMover |
| Dataset | TrajectoryAtlas test set, TrajectoryAtlas test set user study |

> [!tip] 效果简介
> - TrajectoryAtlas test set (40 videos) 上，IoU_traj ↑ (轨迹遵循度) 0.27 vs 0.23 (SFM) / 0.18 (ATI) (+0.04 / +0.09)。
> - TrajectoryAtlas test set user study 上，Bradley‑Terry plausibility strength u_m ↑ 1.25 vs 0.10 (SFM) / -0.27 (ATI) (+1.15 / +1.52)。

## 概述

**问题瓶颈**：视频中移动物体轨迹是一项直观且高频的编辑需求，但现有方法面临根本性障碍——缺乏用于物体轨迹移动任务的成对训练数据，难以直接生成保持原始相对运动但改变起始位置的配对视频。传统方案要么依赖用户手工指定完整的 2D/3D 轨迹控制信号，要么通过外部深度估计间接转换轨迹，过程繁琐且难以保证场景交互的物理合理性。

**核心思路**：本文提出 **TrajectoryMover**，将轨迹移动重新定义为视频到视频（V2V）的生成任务。其关键创新在于两点：一是 **TrajectoryAtlas** 合成数据生成管道，通过物理模拟和在线场景修改自动创建大规模、多样化且具有场景交互的轨迹移动视频对，从根本上解决训练数据缺失问题；二是仅需用户提供两个简单的边界框（源物体首帧位置与目标首帧位置）作为控制信号，大幅降低使用门槛。模型基于预训练扩散模型微调，采用交替训练策略（V2V 与 T2V 任务比例约 7:3）以保留原始生成先验。

**主要结果**：在 TrajectoryAtlas 测试集（40 段视频）上，TrajectoryMover 在背景保留（SSIM_bg 0.92）、前景身份保持（DINO_fg 0.45）、轨迹遵循度（IoU_traj 0.27）以及用户合理性研究（Bradley‑Terry strength 1.25）上全面优于现有基线。轨迹遵循度比 SFM 提高 +0.04，用户合理性比 ATI 提高 +1.52。消融实验证实，多样物体库、混合在线场景修改策略以及完整轨迹类型组合对最终性能至关重要。

**方法定位**：TrajectoryMover 属于基于扩散模型的视频编辑方法，与 **ATI**（Wang et al., arXiv 2025，基于 2D 轨迹控制的图像到视频生成）、**SFM**（基于 3D 代理网格的运动编辑）、**DaS**（基于 3D 点轨迹的视频编辑）、**VACE**（支持边界框轨迹参考的对象移动编辑）及 **I2VEdit**（首帧编辑传播）等方案形成对比。其独特之处在于通过合成数据驱动的方式，将复杂的轨迹控制简化为双边界框输入，并在统一的 V2V 框架内同时处理物体身份保持与场景交互合理性。

## 背景与动机

### 视频编辑中的轨迹移动需求

视频编辑领域长期存在一个核心需求：**将视频中物体的完整运动轨迹平移到新的起始位置，同时保持运动的相对模式、物体身份以及场景合理性**。例如，用户可能希望将一段视频中从桌面左侧滚落的球移动到桌面右侧，使其从新的位置开始相同的滚动与弹跳过程。这类操作在电影特效、内容创作和物理模拟可视化中具有广泛的应用价值。

然而，这一看似直观的操作在技术上极具挑战性。其根本困难在于，物体在视频中的运动并非孤立的像素位移，而是与三维场景深度耦合的物理过程——物体可能与地面碰撞、被障碍物阻挡、或沿曲面滑动。简单地对物体区域进行二维平移或复制粘贴会破坏这种场景交互，产生穿模、悬浮或不自然的运动伪影。

### 现有方法的局限

当前可用于轨迹移动的方法大致可分为两类，但均存在显著缺陷：

**第一类方法基于显式三维重建与代理几何体**，如 **SFM** 使用 3D 代理网格进行精准运动编辑。这类方法需要从单目视频中估计深度、重建三维场景并提取物体运动轨迹，然后将轨迹重新锚定到目标位置。然而，深度估计和三维重建在复杂场景中本身就不稳定，累积误差会严重破坏最终视频的视觉质量。更重要的是，这类方法无法处理因轨迹移动而产生的新场景交互——例如，当物体轨迹从桌面移至地面时，原本不存在的碰撞和反弹行为需要被“凭空”生成。

**第二类方法基于生成模型**，如 **ATI**（Wang et al., arXiv 2025）通过投影 3D 轨迹实现图像到视频的物体移动控制，**VACE** 支持边界框轨迹参考的对象移动编辑，**I2VEdit** 则通过首帧编辑传播实现视频编辑。这些方法虽然能生成视觉上更连贯的结果，但面临一个根本性瓶颈：**缺乏用于轨迹移动任务的成对训练数据**。在真实世界中，几乎不可能获取同一场景下物体从不同起始位置执行相同相对运动的配对视频。因此，现有方法要么依赖手动设计的代理控制信号（如投影轨迹、深度估计），要么将任务拆解为“首帧编辑 + 运动传播”的两阶段过程，无法端到端地学习轨迹移动所需的场景感知生成能力。

### 核心瓶颈与本文动机

上述分析揭示了一个清晰的因果瓶颈：**成对训练数据的缺失直接限制了模型学习轨迹移动映射的能力**。没有成对的“源视频-目标视频”监督信号，模型只能通过间接的、不完整的控制信号来猜测目标输出，导致以下典型失败模式：

- **背景失真**：生成过程破坏了源视频中不应改变的背景区域。
- **物体身份丢失**：移动后的物体外观、纹理或几何形状发生改变。
- **轨迹偏离**：生成的运动路径与用户指定的目标起始位置不符。
- **场景交互不合理**：物体在新路径上缺乏应有的碰撞、遮挡或物理响应。

针对这一瓶颈，**TrajectoryMover** 提出了两条关键思路：

1. **构建合成配对数据管道 TrajectoryAtlas**：通过物理模拟和在线场景修改，自动创建大规模、多样化且具有场景交互的轨迹移动视频对，为模型提供直接的监督信号。
2. **将轨迹移动重新定义为视频到视频的生成任务**：利用合成配对数据微调扩散模型，并采用交替训练策略保存原始生成先验，使用户仅需提供两个简单的边界框（源物体首帧位置与目标首帧位置）即可实现保持物体身份和场景合理性的轨迹平移。

这种设计从根本上规避了真实配对数据缺失的问题，同时将复杂的 3D 轨迹推理隐式地交由生成模型在合成数据上学习，从而在控制简洁性与生成质量之间取得了平衡。

## 核心创新

TrajectoryMover 的核心创新在于将视频中物体轨迹移动重新定义为**视频到视频（V2V）的生成任务**，并通过三个关键设计突破现有方法的瓶颈。

### 1. 任务重定义：从轨迹控制到视频生成

现有方法（如 **ATI**（Wang et al., arXiv 2025）、**SFM**）通常将轨迹移动视为基于显式轨迹信号（2D/3D 轨迹、深度估计、代理网格）的视频编辑问题。用户需要提供完整的运动路径，方法则通过深度估计、轨迹投影或代理网格变形来驱动物体移动。这种范式面临两个根本性困难：一是缺乏用于轨迹移动的成对训练数据，二是控制信号的获取与转换过程复杂且易引入误差。

TrajectoryMover 将问题重新定义为：给定源视频和简单的边界框控制信号（源物体首帧位置 + 目标首帧位置），直接生成物体轨迹已被平移的目标视频。这一重定义将控制信号从“完整轨迹”简化为“首帧位移”，用户仅需提供两个边界框即可指定移动意图（见 Fig. 1）。同时，V2V 生成框架使模型能够端到端地学习从源视频到目标视频的映射，隐式地处理物体身份保持、背景保留和场景交互合理性。

### 2. 数据瓶颈突破：TrajectoryAtlas 合成管道

轨迹移动任务的核心瓶颈在于**缺乏成对训练数据**——不存在源视频与“同一物体沿偏移轨迹运动”的目标视频配对。现有方法只能通过手动设计代理控制信号或拆解-重建策略间接实现移动，无法直接学习轨迹平移的映射。

TrajectoryAtlas 数据生成管道（Fig. 2）通过物理模拟和在线场景修改自动创建大规模配对视频：
- **物理合理的轨迹生成**：使用 Bullet 刚体物理引擎模拟 throw、drop、roll、drag 四类运动轨迹，确保物体与场景几何发生真实的碰撞、弹跳、滚动等交互。
- **在线场景修改**：在目标视频的轨迹走廊中移除或调整非结构性障碍物，使偏移后的轨迹在物理上可行，同时保持场景主体结构不变。
- **多样化资产与场景**：从 Objaverse 资产库采样前景物体，结合程序化场景布局，生成覆盖丰富物体种类和场景类型的配对数据。
- **自动掩码与渲染**：通过 Blender 渲染规范的 RGB 视频和二值分割掩码，提供精确的前景/背景监督信号。

该管道将轨迹移动从“无监督/弱监督编辑问题”转化为“有监督 V2V 生成问题”，为扩散模型微调提供了关键的地面真值监督。

### 3. 训练策略创新：交替训练与参数高效微调

直接在合成数据上微调预训练视频扩散模型可能导致生成先验的灾难性遗忘。TrajectoryMover 采用两项关键训练策略：

- **交替训练（7:3 比例）**：训练过程中交替执行 TrajectoryMover 的 V2V 任务（合成配对数据）和标准 T2V 任务（大规模视频语料），比例约为 7:3。这使模型在学会轨迹移动的同时保留原有的无条件视频生成能力，避免生成质量退化。
- **参数高效微调**：仅微调自注意力层和投影层，冻结网络的其余部分。这进一步降低了过拟合风险，同时使模型能够高效地适应轨迹移动任务。

### 4. 架构设计：三流潜变量拼接

TrajectoryMover 基于 Wan2.1-T2V-1.3B 扩散模型构建，通过三流潜变量拼接实现条件控制（Fig. 3）：将轨迹控制信号的潜变量 $z_{trj}$、源视频潜变量 $z_{src}$ 和边界框控制图像潜变量 $z_{bb}$ 在去噪前拼接，使模型能够同时感知源视频内容、物体身份和移动目标位置。控制图像中红色框标记源物体位置，绿色框标记目标位置，提供简洁直观的空间约束。

**创新总结**：TrajectoryMover 通过“合成数据管道 + V2V 任务重定义 + 交替训练策略”的组合，将轨迹移动从缺乏监督的编辑问题转化为可学习的生成问题，仅需简单的边界框控制即可实现保持物体身份和场景合理性的轨迹平移。

## 整体框架

TrajectoryMover 将视频中物体轨迹的移动重新定义为**视频到视频（V2V）的生成任务**。其整体框架由两个核心模块串联构成：**TrajectoryAtlas 数据生成管道**和**TrajectoryMover 视频生成器**。前者负责自动合成大规模、物理合理的配对训练数据，后者利用这些数据微调扩散模型，实现从源视频到目标视频的轨迹平移。

### 输入与输出流

系统的输入与输出设计简洁直观。用户仅需提供：
- **源视频**：包含待移动物体的原始视频片段。
- **控制信号**：两个边界框——第一个框在首帧中选中待移动物体，第二个框指定该物体在首帧中的目标位置。

系统输出为**目标视频**，其中物体的 3D 运动轨迹从原始起始位置平移到目标起始位置，同时保持物体身份、场景背景以及与新环境之间的物理交互合理性（如碰撞、落地等）。

### 模块关系与数据流

两个模块之间的关系是典型的**数据驱动训练范式**：TrajectoryAtlas 生成合成配对视频作为监督信号，TrajectoryMover 在此数据上进行 V2V 任务的微调。

**TrajectoryAtlas 数据生成管道**（详见 Fig. 2）负责创建源视频 A 和目标视频 B 的配对。其核心机制是：在 3D 场景中放置物体，通过物理模拟生成原始轨迹 $X = (x_i)_{i=1}^{N_F}$，然后对轨迹施加常数偏移 $\delta$ 得到目标轨迹 $Y$：

$$y_i = x_i + \delta$$

管道包含五个阶段：资产缓存准备、预飞行验证、碰撞感知采样与缩放、任务模拟、以及规范渲染与运行时元数据生成。其中，在线场景修改（online scene modification）是一个关键设计——在轨迹走廊中移除非结构性障碍物，使物体在新路径上能够产生合理的场景交互（如穿过洞口而非直接撞击地面）。管道同时输出 RGB 视频和物体分割掩码，为后续训练提供完整监督。

**TrajectoryMover 视频生成器**（详见 Fig. 3）基于预训练的文本到视频扩散模型 Wan2.1‑T2V‑1.3B 构建。它将源视频 $V_{\mathrm{src}}$ 与目标视频 $V_{\mathrm{trg}}$ 的映射条件化于边界框控制信号 $I_{\mathrm{bb}}$。架构上采用**三流潜变量拼接**策略：将轨迹控制信号的潜变量 $z_{\mathrm{trj}}$、源视频潜变量 $z_{\mathrm{src}}$ 以及边界框控制信号的潜变量 $z_{\mathrm{bb}}$ 在去噪前拼接，使模型能够同时感知源视频内容、物体身份以及目标位置约束。

### 训练策略

训练采用**参数高效微调**，仅更新自注意力和投影层，冻结其余网络参数以保留预训练生成先验。更重要的是，采用**交替训练**方案：TrajectoryMover 的 V2V 任务与标准 T2V 任务以约 7:3 的比例交替进行，防止模型在合成数据上过拟合而遗忘开放域视频生成能力。总训练步数为 3,200 步，在 8 张 H100 GPU 上进行，总批次大小为 16。

这一整体框架的核心优势在于：通过合成数据管道解决了轨迹移动任务缺乏成对训练数据的瓶颈，同时以交替训练策略在任务特化与生成先验保留之间取得平衡，使得模型仅需简单的边界框控制即可实现物理合理的轨迹平移。

### 补充图表

![[assets/figures/papers/paper_list_l65_https_arxiv_org_abs_2603_29092/figures/001_Figure_1.jpg]]
*Figure 1: TrajectoryMover enables intuitive video editing by allowing users to translate an object’s 3D motion path to a new starting location using simple bounding box controls across diverse and complex scenarios, including drop, roll, and drag motions. Our model successfully aligns the generated trajectory with the target initial location. Furthermore, the model dynamically adapts the motion to the new path to ensure physical plausibility, seamlessly handling novel scene interactions such as realistic collisions with the environment*

## 核心模块与公式推导

### 问题形式化

TrajectoryMover 将物体轨迹移动任务形式化为视频到视频的生成问题。给定源视频 $\dot{V}_{\mathrm{src}} \in \mathbb{R}^{F \times C \times H \times W}$（$F$ 帧，$C$ 通道，高 $H$，宽 $W$），目标是生成目标视频 $V_{\mathrm{trg}}$，其中物体的 3D 运动轨迹从 $X = (x_i)_{i=1}^{N_F}$ 平移至 $Y = (y_i)_{i=1}^{N_F}$。

轨迹偏移的核心公式为：

$$y_i = x_i + \delta$$

其中 $\delta$ 为常数偏移量。该公式定义了理想情况下的简单平移关系，但在实际场景中，物体移动后可能与新环境产生碰撞、遮挡等交互，因此生成模型需要学会在保持偏移语义的同时适应新的物理约束。

### 控制信号编码

用户控制信号极其简洁：仅需在首帧中提供两个边界框——红色框标记源物体位置，绿色框标记目标起始位置。该控制信号被编码为控制图像 $I_{\mathrm{bb}}$，作为额外的输入帧拼接到源视频中，形成三流潜变量拼接结构：

- $z_{\mathrm{src}}$：源视频的潜变量表示
- $z_{\mathrm{trj}}$：轨迹相关的潜变量表示
- $z_{\mathrm{bb}}$：边界框控制信号的潜变量表示

三者在去噪前被拼接，共同输入扩散模型进行条件生成。

### TrajectoryAtlas 数据生成管道

TrajectoryAtlas 是本文的核心贡献之一，解决了轨迹移动任务缺乏成对训练数据的瓶颈。管道包含五个阶段：

1. **资产缓存准备（Asset Cache Preparation）**：将相机、3D 场景、光照材质、Objaverse 物体或几何基元转换为可复用的碰撞缓存。
2. **预飞行验证（Preflight Validation）**：通过跳过渲染的预飞行检查筛选有效帧。
3. **碰撞感知采样与缩放（Collision Aware Sampling and Scaling）**：生成共享缩放的配对 A/B 放置方案，通过可见性、支撑面法线和穿透间隙过滤无效配置；可选的无碰撞处理仅移除非结构性障碍物。
4. **任务模拟（Task Simulation）**：使用 Bullet 刚体物理引擎模拟投掷（throw）、掉落（drop）、滚动（roll）和拖拽（drag）四类轨迹，生成物理合理的运动序列。
5. **规范渲染与运行时元数据（Canonical Rendering with Runtime Metadata）**：使用 Blender 将模拟结果渲染为标准 RGB 视频和二元分割掩码视频。

管道的关键设计在于**在线场景修改**：在轨迹走廊中动态移除非结构性障碍物，使物体能够通过原本不可通行的区域（如穿过地面上的洞），从而生成具有新颖场景交互的配对数据。

### 视频生成器架构

TrajectoryMover 基于 Wan2.1-T2V-1.3B 扩散模型构建，采用参数高效微调策略：仅训练自注意力层和投影层，冻结其余网络参数。训练采用交替策略，将 TrajectoryMover 的视频到视频（V2V）任务与标准文本到视频（T2V）任务以约 7:3 的比例交替进行，在 8 张 H100 GPU 上以总批次大小 16 训练 3200 步。该策略旨在保留预训练模型的通用视频生成先验，同时使模型适应轨迹移动的特定任务。

### Bradley-Terry 用户偏好模型

用户研究中采用 Bradley-Terry 模型量化方法间的相对偏好：

$$P(i \succ j) = \frac{e^{u_i}}{e^{u_i} + e^{u_j}}$$

其中 $P(i \succ j)$ 表示方法 $i$ 在成对比较中优于方法 $j$ 的概率，$u_i$ 和 $u_j$ 分别为两方法的效用强度。TrajectoryMover 的效用强度 $u_m = 1.25$，显著高于 SFM 的 0.10 和 ATI 的 -0.27，表明用户对其生成结果的运动合理性有强烈偏好。

### 补充图表

![[assets/figures/papers/paper_list_l65_https_arxiv_org_abs_2603_29092/figures/002_Figure_2.jpg]]
*Figure 2: TrajectoryAtlas data generation pipeline. The pipeline has five stages, Asset Cache Preparation, Preflight Validation, Collision Aware Sampling and Scaling, Task Simulation, and Canonical Rendering with Runtime Metadata. Inputs including camera, 3D scene, lights and materials, and Objaverse or primitive assets are converted to reusable collision caches, then skip render preflight selects valid frames. Paired A/B placements with shared scale are filtered by visibility, support normal, and penetration clearance, and optional no hit processing removes only non structural obstacles in the trajectory corridor. Throw, drop, roll, and drag trajectories are simulated with Bullet and rendered with B...*

![[assets/figures/papers/paper_list_l65_https_arxiv_org_abs_2603_29092/figures/003_Figure.jpg]]

![[assets/figures/papers/paper_list_l65_https_arxiv_org_abs_2603_29092/figures/009_Figure.jpg]]
*Figure: Fig. B.2. Drag trajectory variants. We visualize the three planar drag references used in our simulator: spiral (left), circular (middle), and S-shaped (right), rendered from the scene camera as 3D trajectories. Each curve shows directed start-to-goal progression and highlights the motion templates used for drag supervision*

## 实验与分析

### 主结果：与基线方法的全面对比

TrajectoryMover 在四个互补维度上全面超越现有基线方法，验证了将轨迹移动重新定义为视频到视频生成任务并通过合成配对数据训练的有效性。Table 1 报告了在 TrajectoryAtlas 测试集（40 个视频）上的定量结果。

![[assets/figures/papers/paper_list_l65_https_arxiv_org_abs_2603_29092/figures/004_Table_1.jpg]]
*Table 1: Comparison to Baselines. We compare background preservation*

**背景保留（SSIM_bg ↑）**：TrajectoryMover 达到 0.92，相比 ATI（0.71）提升 +0.21，相比 SFM（0.56）提升 +0.36。这一显著优势源于三流潜变量拼接架构将源视频作为条件直接注入去噪过程，而非依赖外部深度估计或代理网格重建，从而最大程度保留了源视频的背景结构。

**前景身份保留（DINO_fg ↑）**：TrajectoryMover 达到 0.45，相比 ATI（0.39）提升 +0.06，相比 SFM（0.29）提升 +0.16。合成数据中的多样物体库（Objaverse 资产）和在线场景修改策略共同保障了模型对物体外观的稳定编码能力。

**轨迹遵循度（IoU_traj ↑）**：TrajectoryMover 达到 0.27，相比最优基线 SFM（0.23）提升 +0.04，相比 ATI（0.18）提升 +0.09。仅需两个边界框的简洁控制信号在引导目标轨迹方面展现出竞争力，尽管绝对数值表明精确映射仍具挑战。

**用户合理性研究（Bradley-Terry strength u_m ↑）**：TrajectoryMover 达到 1.25，相比 SFM（0.10）提升 +1.15，相比 ATI（-0.27）提升 +1.52。用户研究采用盲审、随机匿名与 Bradley-Terry 模型（$P(i \succ j) = \frac{e^{u_i}}{e^{u_i} + e^{u_j}}$），确保了评估的公平性。TrajectoryMover 在运动稳定性、物体一致性和场景交互合理性方面获得了用户的显著偏好。

Fig. 4 的定性对比进一步印证了定量发现：SFM 在背景保留上表现较差（粉色框标注区域出现明显伪影），ATI 的轨迹遵循度不足，而 TrajectoryMover 在四个代表性运动场景（drop、roll、drag 等）中均能一致地遵循目标运动路径，同时保持物体外观和场景身份（青色框标注成功区域）。

![[assets/figures/papers/paper_list_l65_https_arxiv_org_abs_2603_29092/figures/005_Figure_4.jpg]]
*Figure 4: Qualitative comparison with baselines. We compare TrajectoryMover with SFM, ATI, DaS, VACE, and I2VEdit on four representative motion scenarios. Red boxes indicate the source object location in the input video, green boxes indicate the target location at frame 0, pink boxes highlight regions of failure, and cyan boxes highlight regions of success. TrajectoryMover follows the intended motion most consistently while preserving object appearance and scene identity. Please zoom in for details*

### 消融实验：关键设计选择的影响

Table 2 和 Fig. 5 系统消融了 TrajectoryAtlas 数据生成管道和训练策略中的四项关键设计。

![[assets/figures/papers/paper_list_l65_https_arxiv_org_abs_2603_29092/figures/006_Figure_5.jpg]]
*Figure 5: Qualitative ablation analysis. We compare the full model with ablations using only primitives, only scene modification, without scene modification, and droponly motion training. Red boxes indicate source object location, green boxes indicate target frame-0 location, and pink boxes mark representative regions of failure while cyan boxes highlight region of success results. The full model gives the best balance of trajectory fidelity, object identity preservation, and scene-aware motion plausibility. Please zoom in for details*

![[assets/figures/papers/paper_list_l65_https_arxiv_org_abs_2603_29092/figures/007_Table_2.jpg]]
*Table 2: Ablation. We ablate several key design choices in our pipeline: only using primitives as foreground objects, performing online scene modifications for all videos, or for none of the videos, and using only a single object trajectory type*

**物体多样性（primitives only）**：仅使用简单几何体替代多样物体库时，前景身份 DINO_fg 从 0.45 骤降至 0.15，轨迹遵循度 IoU_traj 也从 0.27 降至 0.17。这表明多样化的 Objaverse 资产对于训练模型保持物体身份至关重要，简单几何体无法提供足够的外观变化来学习鲁棒的身份编码。

**在线场景修改策略**：完全移除在线场景修改（w/o scene mod.）导致 IoU_traj 降至 0.17；全部使用场景修改（only scene mod.）则进一步降至 0.16。混合模式（即部分视频进行场景修改）对最佳性能是必要的——它使模型既能学习轨迹偏移与场景交互的因果关系，又不会过拟合到修改后的场景分布上。

**轨迹类型多样性（Drop-only）**：仅使用单一 Drop 轨迹训练时，IoU_traj 为 0.21，而完整的多样化轨迹组合（drop、roll、drag 等）将指标提升至 0.27。这验证了多种运动类型对模型泛化能力的贡献，单一轨迹类型限制了模型对不同运动模式的适应。

### 失败模式与局限性

尽管 TrajectoryMover 在各项指标上全面领先，实验揭示了以下关键局限：

1. **轨迹遵循精度上限**：绝对 IoU_traj 仅 0.27，意味着模型生成的物体运动轨迹与目标路径之间仍存在显著偏差。当轨迹变化较复杂（如大范围空间偏移或多方向复合运动）时，模型难以精确地将物体映射到目标位置。

2. **合成域泛化未验证**：所有训练和测试均在 TrajectoryAtlas 合成场景上进行，模型在任意真实视频数据集上的泛化能力尚未验证。合成数据中的物体种类和场景布局与真实世界存在域差异，可能限制模型处理开放域物体和复杂环境时的表现。

3. **场景交互的边界情况**：尽管在线场景修改策略提升了物理合理性，但在某些极端交互场景（如物体穿过狭窄缝隙或多物体碰撞）中，模型仍可能产生不符合物理规律的生成结果。这一点在用户研究中虽有改善，但未完全解决。

### 公平性保障

所有基线方法均按照统一流程重新部署：使用相同的深度估计器（Video-Depth-Anything）提取轨迹，统一输出分辨率与帧率，并采用相同的评估协议（SAM3 分割、SSIM_bg/DINO_fg/IoU_traj）。Fig. B.1 展示了统一的基线赋能管道，确保对比结果不受实现差异影响。

### 补充图表

![[assets/figures/papers/paper_list_l65_https_arxiv_org_abs_2603_29092/figures/008_Figure.jpg]]
*Figure: (IV) Compute offset E Fig. B.1. Common baseline repurposing pipeline. We convert each source-target case into method specific controls. We estimate source depth, extract source and target frame 0 masks, lift source object motion to a 3D trajectory proxy, compute the frame 0 displacement E, and re-anchor the trajectory to the target start. Red indicates source localization, green indicates target localization, and trajectory overlays visualize source and re-anchored motion elements used for downstream baseline control conversion*

![[assets/figures/papers/paper_list_l65_https_arxiv_org_abs_2603_29092/figures/010_Figure.jpg]]
*Figure: Fig. C.1. User study interface. Participants compare two anonymized videos (A/B) from the same source-target setup and select the one with more natural and coherent object motion. The guidance text standardizes the evaluation criteria (motion stability, object consistency, trajectory reasonableness, and scene interaction plausibility). The same interface format is used for all user study experiments in this project*

## 方法谱系与知识库定位

### 任务定位与问题边界

TrajectoryMover 将物体轨迹移动重新定义为一种**视频到视频（V2V）的生成任务**：给定源视频和用户指定的两个边界框（首帧中物体的源位置与目标位置），模型需要生成一段新视频，其中被选中物体从目标位置出发，沿与源轨迹保持相同相对运动的路径移动，同时保持物体身份、背景完整性和场景交互的物理合理性。这一任务设定区别于现有视频编辑方法的两个核心约束是：（1）仅需极简的边界框控制信号，而非完整的 2D/3D 轨迹标注；（2）要求模型自动适应新路径上的场景交互变化（如碰撞、遮挡），而非简单地对轨迹进行几何平移。

### 与现有方法的关系

现有视频物体运动编辑方法可大致分为以下几类，TrajectoryMover 在控制信号简洁性、场景交互合理性和生成质量三个维度上与它们形成差异化定位。

**基于 2D/3D 轨迹控制的生成方法**：**ATI**（Wang et al., arXiv 2025）通过投影 3D 轨迹实现图像到视频的物体移动生成，但需要用户提供完整的 2D 轨迹作为控制信号，且依赖外部深度估计将 2D 轨迹提升为 3D 代理。实验表明，ATI 在背景保留（SSIM_bg 0.71 vs. TrajectoryMover 0.92）和轨迹遵循度（IoU_traj 0.18 vs. 0.27）上均显著弱于 TrajectoryMover，其根本原因在于缺乏成对的轨迹移动训练数据，导致模型难以在移动物体的同时保持场景一致性。

**基于 3D 代理网格的精准运动编辑**：**SFM** 通过 3D 代理网格实现精准的运动编辑，在轨迹遵循度上表现相对较好（IoU_traj 0.23），但该方法需要完整的 3D 轨迹输入，且背景保留（SSIM_bg 0.56）和前景身份保持（DINO_fg 0.29）严重退化。这表明仅关注运动精度而忽略生成质量会导致整体编辑效果不可用。

**基于点轨迹的视频编辑**：**DaS** 使用 3D 点轨迹进行视频编辑，但在轨迹移动任务中面临与 SFM 类似的生成质量瓶颈。**VACE** 和 **I2VEdit** 分别通过边界框轨迹参考和首帧编辑传播实现物体移动，但这些方法同样缺乏针对轨迹移动任务的专门训练数据，在复杂场景交互（如物体与场景的碰撞适应）上表现不足。

TrajectoryMover 的关键突破在于：通过 **TrajectoryAtlas 合成数据生成管道**自动创建大规模、多样化且具有物理合理场景交互的轨迹移动视频对，从而首次为该任务提供了可直接用于监督训练的成对数据。这使得模型能够学习从源视频到目标视频的端到端映射，而非依赖拆解-重建的代理策略。

### 方法谱系中的关键设计选择

TrajectoryMover 在以下几个设计维度上做出了区别于基线的选择：

1. **训练数据来源**：基线方法依赖手动设计的代理控制信号或外部模型（如深度估计）进行轨迹转换，而 TrajectoryMover 使用 TrajectoryAtlas 自动合成的配对视频，包含物理模拟（Bullet）生成的轨迹和 Blender 渲染的 RGB 与分割掩码。这一数据管道的核心创新在于**在线场景修改**机制——在轨迹走廊中移除非结构性障碍物，使物体在新路径上产生物理合理的碰撞与交互，而非简单的几何平移。

2. **控制信号设计**：将控制信号简化为两个边界框（源与目标首帧位置），编码为额外的视频帧输入。这一设计使非专业用户也能直观地指定编辑意图，无需理解 3D 轨迹或深度信息。

3. **训练策略**：采用**交替训练**方案，在 TrajectoryMover 的 V2V 任务与标准 T2V 任务之间以约 7:3 的比例切换，仅微调自注意力和投影层。这一策略的关键作用是保留预训练扩散模型的生成先验，防止模型在合成数据上过拟合而丧失泛化能力。

### 适用边界与局限

尽管 TrajectoryMover 在合成测试集上全面优于现有基线，其适用边界仍存在以下限制：

1. **绝对轨迹精度有限**：IoU_traj 仅达到 0.27，表明模型在精确映射物体到目标路径上仍有较大提升空间。当轨迹变化较为复杂（如大幅度的方向改变或多物体交互）时，模型可能无法完全遵循期望的运动路径。

2. **合成域到真实域的泛化未验证**：TrajectoryAtlas 生成的训练和测试数据均为合成场景（使用 Objaverse 物体库和程序化场景），模型在任意真实视频上的轨迹移动能力尚未得到验证。合成数据中的物体种类、场景布局和光照条件与真实世界存在域差异，可能限制模型处理开放域物体和复杂真实环境时的表现。

3. **单物体移动假设**：当前方法假设视频中仅有一个物体需要移动，且该物体在首帧中可通过单个边界框选中。对于多物体交互或需要同时移动多个物体的场景，方法需要扩展。

4. **静态摄像机假设**：TrajectoryAtlas 数据生成使用固定摄像机，模型未针对动态摄像机运动进行训练。在真实视频中，摄像机运动与物体运动的耦合可能引入额外的挑战。

### 开放问题

基于上述分析，以下开放问题值得后续研究关注：

1. **轨迹映射精度的进一步提升**：如何在保持物体身份稳定和场景合理性的前提下，将 IoU_traj 提升至实用水平（例如 >0.5）？可能的路径包括引入更精细的轨迹条件机制（如逐帧点轨迹监督）或改进损失函数中对轨迹遵循度的显式建模。

2. **域适应与真实视频泛化**：能否通过域适应技术（如域随机化、对抗训练或少量真实视频微调）将模型推广到真实视频中的轨迹移动任务？这需要构建或利用现有的真实视频物体运动数据集，并设计合适的域间对齐策略。

3. **多物体与动态场景扩展**：如何利用更丰富多样的数据（例如多物体交互、动态摄像机、非刚性物体）扩展模型的适用范围？这要求 TrajectoryAtlas 数据管道支持更复杂的物理模拟和场景配置。

4. **控制信号的表达力与简洁性平衡**：当前两个边界框的控制方式极为简洁，但可能不足以表达复杂的运动意图（如轨迹形状修改、速度变化）。如何在保持用户友好的前提下增强控制信号的表达力，是实用化的关键问题。

## 原文 PDF

![[paperPDFs/arxiv_2026/TrajectoryMover_Generative_Movement_of_Object_Trajectories_in_Videos.pdf]]
