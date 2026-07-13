---
title: "CineScene: Implicit 3D as Effective Scene Representation for Cinematic Video Generation"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/CineScene_Implicit_3D_as_Effective_Scene_Representation_for_Cinematic_Video_Generation.pdf
project_link: null
code_link: null
aliases:
- CineScene
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/image_and_video_generation
- topic/vision_multimodal_applications/3d_rendering_reconstruction
- topic/generative_models_diffusion
core_operator: 将隐式3D场景表示以上下文条件（而非损失引导）的形式注入预训练T2V模型，使模型学习解耦静态场景与动态前景。
primary_logic: 通过VGGT从多视角静态场景图像中提取融合图像与相机信息的隐式3D特征，并利用上下文拼接机制将其与噪声视频潜变量一同送入扩散Transformer，从而赋予模型空间感知能力，在遵循大范围相机运动的同时保持场景一致性并生成新动态主体。
claims:
- "与2D上下文方法FramePack相比，CINESCENE在所有场景一致性指标上取得显著提升（Mat. Pix.: 4617.51 vs 4107.45，PSNR: 14.51 vs 11.89），表明隐式3D注入对保持大视角场景一致性至关重要。"
- 消融实验证实，同时使用图像特征和相机特征的隐式3D融合（Ours）在场景一致性上优于仅使用其中单一特征或完全无隐式3D的情况（Table 2），而随机打乱上下文图像（Shuffled）进一步提升了联合建模和相机准确性（Table 3）。
- Scene-Decoupled Video Dataset (held-out) 上 Mat. Pix.(K)↑ = 4617.51
- Scene-Decoupled Video Dataset 上 PSNR↑ = 14.5094
---

# CineScene: Implicit 3D as Effective Scene Representation for Cinematic Video Generation

> [!tip] 核心洞察
> 通过VGGT从多视角静态场景图像中提取融合图像与相机信息的隐式3D特征，并利用上下文拼接机制将其与噪声视频潜变量一同送入扩散Transformer，从而赋予模型空间感知能力，在遵循大范围相机运动的同时保持场景一致性并生成新动态主体。

| 字段 | 内容 |
|------|------|
| 中文题名 | CineScene：以隐式3D作为场景表示的电影级视频生成 |
| 英文题名 | CineScene: Implicit 3D as Effective Scene Representation for Cinematic Video Generation |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2602.06959) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/image_and_video_generation #topic/vision_multimodal_applications/3d_rendering_reconstruction #topic/generative_models_diffusion |
| Method | CINESCENE |
| Dataset | Scene-Decoupled Video Dataset, DiT360 OOD Test |

> [!tip] 效果简介
> - Scene-Decoupled Video Dataset (held-out) 上，Mat. Pix.(K)↑ 4617.51 vs 4107.45 (FramePack) (+510.06)。
> - Scene-Decoupled Video Dataset 上，PSNR↑ 14.5094 vs 11.8854 (FramePack) (+2.624)；RotErr↓ 2.6825 vs 2.7106 (CaM) (-0.0281)。
> - DiT360 OOD Test 上，Mat. Pix.(K)↑ 4726.57 vs 4025.98 (FramePack) (+700.59)。

## 概要

**问题瓶颈**：现有方法在生成大视角变化的视频时，难以同时保持场景一致性并容纳动态内容。2D上下文方法（如 **FramePack**，Zhang & Agrawala, arXiv 2025；**Context-as-Memory**，Yu et al., arXiv 2025）缺乏空间理解能力；显式3D方法（如 **Gen3C**，Zhang et al., CVPR 2025）依赖不完美的几何重建，且常限制动态生成。

**核心洞察**：将隐式3D场景表示以**上下文条件**（而非损失引导）的形式注入预训练文本到视频（T2V）扩散模型，使模型学习解耦静态场景与动态前景。

**方法定位**：CINESCENE 通过 VGGT 从多视角静态场景图像中提取融合图像与相机信息的隐式3D特征，并利用上下文拼接机制将其与噪声视频潜变量一同送入扩散 Transformer，从而赋予模型空间感知能力，在遵循大范围相机运动的同时保持场景一致性并生成新动态主体。

**主要结果**：
- 与2D上下文方法 **FramePack** 相比，CINESCENE 在所有场景一致性指标上取得显著提升（Mat. Pix.: 4617.51 vs 4107.45，PSNR: 14.51 vs 11.89），验证了隐式3D注入对保持大视角场景一致性的关键作用（Table 1）。
- 在域外测试集 DiT360 上，CINESCENE 同样表现优异（Mat. Pix.: 4726.57 vs FramePack 的 4025.98），展现出良好的泛化潜力（Table 4）。
- 消融实验证实：融合图像特征与相机特征的隐式3D表示、上下文条件注入机制（优于损失引导）、以及随机打乱上下文图像的训练策略，均为方法有效性的关键设计（Table 2, Table 3）。



### 问题背景：大视角变化下的电影级视频生成

电影级视频生成要求模型在动态镜头运动中同时保持场景的几何一致性和视觉连贯性。当相机执行大范围运动（如摇移、推拉、环绕）时，场景中的静态元素（墙壁、家具、远景）必须与相机位姿精确对齐，而动态主体（人物、车辆）则应自由运动。这一任务的本质困难在于：模型需要理解三维场景的空间结构，同时解耦静态背景与动态前景。

现有的文本到视频（T2V）生成模型在常规镜头下已能产出高质量片段，但当视角变化超过一定范围时，场景元素容易出现漂移、扭曲或消失。这暴露了当前方法的根本瓶颈：**缺乏对三维场景的有效空间感知能力**。

### 现有方法缺口

围绕这一问题，已有工作可大致分为三条技术路线，但各自存在关键局限：

**2D上下文方法**（如 **FramePack** (Zhang and Agrawala, arXiv 2025)、**Context-as-Memory (CaM)** (Yu et al., arXiv 2025)）将场景参考图像作为像素级条件注入扩散模型。这类方法完全在二维空间操作，缺乏对三维几何的理解。当相机视角大幅偏离参考图像时，模型无法推理遮挡关系和透视变化，导致场景一致性急剧下降。定量上，FramePack 在场景一致性指标 Mat. Pix. 上仅为 4107.45，PSNR 仅 11.89（见 Table 1），远不足以支撑电影级应用。

**显式3D引导方法**（如 **Gen3C** (Zhang et al., CVPR 2025)）尝试通过重建场景的显式三维几何（如点云、网格）来约束生成。然而，这一路线面临双重困境：其一，从稀疏视角重建完整场景几何本身是一个病态问题，重建误差会直接传导至生成结果；其二，显式3D约束本质上惩罚与静态场景的偏差，这恰恰抑制了动态内容的生成——场景越“一致”，动态主体越难以自然运动。

**相机控制方法**（如 **Traj-Attn**、**RecamMaster** (Bai et al., arXiv 2025)）专注于精确跟随用户指定的相机轨迹，但对场景内容的保持能力有限。它们可以拍出正确的镜头运动，却无法保证镜头中的场景与给定的参考环境一致。

### 核心动机：从“损失引导”到“上下文条件”

上述方法的共同症结在于：**场景信息要么以二维像素形式注入（缺乏空间理解），要么以显式三维约束施加（限制动态生成）**。本文的核心洞察是：场景表示不应作为对生成结果的惩罚信号，而应作为赋予模型空间感知能力的先验条件。

具体而言，CineScene 提出将**隐式3D场景表示**以**上下文条件**（context condition）的形式注入预训练 T2V 模型。这一设计的因果机制在于：

- **隐式3D表示**（通过 VGGT 从多视角场景图像中提取的融合图像特征与相机特征的联合表征）为模型提供了丰富的空间先验，使其能够理解场景的三维结构，而无需显式重建几何。
- **上下文条件机制**（将隐式3D特征与噪声视频潜变量沿帧维度拼接，共同送入扩散 Transformer）使场景信息成为生成过程的一部分，而非外部监督。这从根本上解耦了静态背景（条件）与动态前景（生成目标），使模型既能保持场景一致性，又能自由生成新的动态主体。

这一设计选择的关键优势在消融实验中得到了直接验证：与“损失引导”（loss-guided）的隐式3D注入方式相比，上下文条件机制能够生成无伪影的动态主体，且场景一致性更高（Mat. Pix.: 4617.51 vs 4509.46，见 Table 2 及 Figure 5）。损失引导方法因惩罚与静态场景的偏差，在生成动态内容时出现明显伪影；而上下文条件方法通过让模型“看见”场景而非“被约束于”场景，实现了静态保持与动态生成的统一。

### 本文目标

综上，CineScene 旨在解决大视角变化下的电影级视频生成问题，其核心贡献在于：**以隐式3D场景表示作为上下文条件，赋予预训练 T2V 模型空间感知能力，实现静态场景一致性保持与动态主体自由生成的解耦**。这一思路为后续将场景一致性扩展至更长视频、更大视角变化提供了新的技术基础。



## 核心方法与创新机理

CINESCENE 的核心创新在于**将隐式3D场景表示以上下文条件的形式注入预训练T2V扩散模型**，从而从根本上解耦静态场景与动态前景的生成。这一设计解决了现有方法在大视角变化视频生成中的根本矛盾：2D上下文方法（如FramePack、Context-as-Memory）缺乏空间理解，难以在视角大幅变化时保持场景一致性；显式3D引导方法（如Gen3C）依赖不完美的几何重建，且其损失监督机制倾向于抑制动态内容的生成。

### 关键 changed slots

**Slot 1：场景表示条件注入机制**

- **基线做法**：无隐式3D条件（纯2D上下文），或以损失函数形式施加显式3D监督（如Gen3C的几何一致性损失）。
- **CINESCENE 做法**：通过上下文拼接（context concatenation）将来自VGGT的隐式3D场景特征 `F` 注入扩散Transformer。具体而言，从20张等距透视场景图像中提取图像特征 `F_i ∈ ℝ^(20×k×2048)`（包含深度图、点云和跟踪信息）和相机特征 `F_c ∈ ℝ^(20×1×2048)`（每视图一个姿态令牌），经逐元素相加融合为隐式3D表示 `F ∈ ℝ^(20×k×2048)`。该特征经空间分辨率对齐、分块投影后得到隐式3D令牌 `F_t`，与场景图像令牌 `I_t` 和噪声视频潜变量沿帧维度拼接，共同送入Transformer处理。

这一设计的因果机制在于：**条件注入使模型将静态场景视为“已知上下文”而非“需要复现的目标”**，从而允许生成全新的动态前景。与之相对，损失引导方式（Loss-Guided）将VGGT特征用于构造监督损失，惩罚生成视频与静态场景的偏差，这虽然有助于保持场景一致性，却会抑制动态主体生成并引入伪影（见Figure 5）。消融实验证实，上下文条件机制在场景一致性上优于损失引导（Mat. Pix.: 4617.51 vs 4509.46），且能生成无伪影的动态主体。

**Slot 2：上下文图像训练策略**

- **基线做法**：按固定顺序提供场景上下文图像，模型可能学习到依赖末张图像的“复制”捷径。
- **CINESCENE 做法**：训练时固定第一张场景图像的位置（对应起始视角），对其余场景图像进行随机打乱（shuffled）。这迫使模型不能依赖固定的空间顺序先验，而必须学习像素上下文与隐式3D表示之间的对齐关系。

消融实验（Table 3）表明，打乱策略在场景一致性（Mat. Pix. 4617.51 vs Ordered 4560.29）和相机准确性（RotErr 2.6825 vs Ordered 2.8226）上均优于有序输入和渐进训练策略。定性结果（Figure 6）进一步揭示，有序输入下模型倾向于复制末张上下文图像的内容，而打乱机制促使模型真正利用隐式3D表示进行联合建模。

### 与基线方法的本质差异

| 维度 | 2D上下文方法 | 显式3D引导方法 | CINESCENE |
|------|-------------|---------------|-----------|
| 场景理解 | 仅2D像素上下文 | 显式几何重建+损失监督 | 隐式3D特征+条件注入 |
| 动态生成 | 可生成，但一致性差 | 受损失约束抑制动态 | 解耦静态/动态，自由生成 |
| 空间感知 | 弱 | 依赖重建精度 | 通过VGGT特征隐式编码 |
| 训练信号 | 视频重建损失 | 重建损失+几何一致性损失 | 视频重建损失+上下文条件 |

综上，CINESCENE 通过两个关键的 changed slots——**隐式3D上下文条件注入**和**打乱上下文图像训练**——实现了对静态场景与动态前景的本质解耦，使得预训练T2V模型在不牺牲动态生成能力的前提下获得空间感知能力，从而在大视角变化下保持高场景一致性。



CINESCENE 的整体 pipeline 围绕一个核心设计展开：**将隐式3D场景表示以上下文条件的形式注入预训练的文生视频（T2V）扩散模型**，从而在遵循用户指定相机轨迹的同时保持静态场景的一致性，并自由生成动态前景主体。其输入输出定义如下：

给定一组解耦的静态场景图像 $I \in \mathbb{R}^{\times h \times w \times c}$、文本提示 $P$ 以及目标相机轨迹 $\bar{C} \in \mathbb{R}^{f \times 3 \times 4}$，模型生成一段包含动态主体、且相机运动严格遵循 $\bar{C}$ 的视频 $V \in \mathbb{R}^{f \times c \times h \times w}$，其中 $c$ 为通道数，$h$、$w$ 为高宽，$f$ 为帧数。

### 模块关系与数据流

整个框架由四个关键模块串联构成，数据流从场景图像输入到最终视频生成呈线性推进：

1. **3D感知场景表示提取**
   输入20张从全景图经等距透视投影生成的场景图像，通过预训练的 VGGT 网络同时提取图像特征 $F_i \in \mathbb{R}^{20 \times k \times 2048}$（包含深度图、点云和跟踪信息）和相机姿态特征 $F_c \in \mathbb{R}^{20 \times 1 \times 2048}$。将 $F_c$ 空间扩展后与 $F_i$ 逐元素相加，得到融合了内容信息与视角信息的隐式3D特征 $F \in \mathbb{R}^{20 \times k \times 2048}$。

2. **场景上下文图像条件注入**
   将20张场景图像分别编码为潜变量并分块，沿帧维度拼接为上下文令牌 $I_t$，作为视频扩散模型的附加条件。这一设计与隐式3D条件协同工作，为模型提供直接的像素级场景参考。

3. **隐式3D场景表示条件注入**
   将隐式3D特征 $F$ 对齐空间分辨率、分块投影后得到隐式3D令牌 $F_t$。$F_t$ 与 $I_t$ 以及噪声视频潜变量沿帧维度拼接，共同输入扩散 Transformer 进行去噪。这一上下文拼接机制是 CINESCENE 区别于损失引导方法的核心——它将静态场景作为条件而非监督信号，从架构层面解耦了静态背景与动态前景的生成。

4. **相机轨迹与文本提示注入**
   目标相机参数 $\bar{C}$ 通过可学习编码器投影后注入视频令牌，同时在交叉注意力层注入文本提示 $P$，实现相机控制和语义对齐。

### 关键训练策略

在训练阶段，CINESCENE 采用**随机打乱上下文图像**的策略：固定第一张场景图像的位置（对应起始视角），其余19张图像顺序随机打乱。这一设计迫使模型学习像素上下文与隐式3D表示之间的真实对齐关系，而非依赖固定的位置先验。消融实验表明，该策略在场景一致性和相机准确性上均显著优于有序输入和渐进训练方案。

### 与损失引导方法的本质区别

Figure 3 明确对比了两种隐式3D注入范式。损失引导方法将 VGGT 特征用于构造监督损失，惩罚生成结果与静态场景的偏差——这天然抑制动态内容的产生，导致动态主体区域出现伪影。CINESCENE 的上下文条件机制则将隐式3D信息作为生成条件而非约束，使模型在“理解”场景空间结构的前提下自由生成动态前景，从机制上避免了两者的冲突。

![[assets/figures/papers/paper_list_l2449_https_arxiv_org_abs_2602_06959/figures/003_Figure_3.jpg]]
*Figure 3: Overview of CINESCENE. Left: Our method, CINESCENE, injects implicit 3D information as a context condition. Features from VGGT are encoded as tokens (Ft) and concatenated with the scene images (It) and the noisy video latents. This architecture fundamentally decouples the static background (the condition) from the dynamic foreground (the generation target). Right: In contrast, loss-guided approaches use the VGGT features to form a supervisory loss, which penalizes deviations from the static scene and thus discourages dynamic content generation. We omit the text prompt for simplicity*



### 问题形式化

CINESCENE的目标可形式化为：给定一组解耦的场景图像 $I \in \mathbb{R}^{\times h \times w \times c}$、文本提示 $P$ 以及目标相机轨迹 $\bar{C} \in \mathbb{R}^{f \times 3 \times 4}$，生成一段 $f$ 帧的视频 $V \in \mathbb{R}^{f \times c \times h \times w}$。其中 $c$ 为通道数，$h$、$w$ 为帧的高和宽，$f$ 为帧数。核心约束是：生成的视频需在遵循指定相机运动的同时，保持静态场景的一致性，并能容纳动态前景主体。

### 核心模块拆解

CINESCENE的架构围绕一个关键设计展开：将隐式3D场景表示作为上下文条件注入预训练的文生视频（T2V）扩散模型，而非作为损失监督信号。这一设计在根本上将静态背景（条件）与动态前景（生成目标）解耦。以下为四个核心模块：

#### 1. 3D感知场景表示提取（VGGT编码器）

该模块负责从多视角静态场景图像中提取融合了内容信息与空间视角信息的隐式3D特征。

- **输入**：20张等距透视投影的场景图像，由全景图经等距柱状投影到透视投影转换生成。
- **处理流程**：将20张场景图像送入预训练的VGGT网络，分别提取：
  - **图像特征** $F_i \in \mathbb{R}^{20 \times k \times 2048}$：包含深度图、点云和跟踪信息的视觉特征，$k$ 为与空间分辨率相关的令牌数。
  - **相机特征** $F_c \in \mathbb{R}^{20 \times 1 \times 2048}$：每个视图对应的相机姿态特征，每个视图仅一个令牌。
- **融合策略**：将 $F_c$ 沿令牌维度扩展至与 $F_i$ 相同的 $k$ 维度，然后通过**逐元素相加**得到最终的隐式3D场景表示 $F \in \mathbb{R}^{20 \times k \times 2048}$。消融实验证实，逐元素加法优于直接将 $F_i$ 和 $F_c$ 拼接。

#### 2. 场景上下文图像条件注入

将20张场景图像分别通过VAE编码为潜变量，并进行分块（patchify）处理，沿帧维度拼接为上下文令牌 $I_t$。这些令牌作为视频扩散模型的附加条件输入，为模型提供像素级的场景外观参考。

#### 3. 隐式3D场景表示条件注入

将隐式3D特征 $F$ 进行空间分辨率对齐和分块投影后，得到隐式3D令牌 $F_t$。$F_t$ 与场景图像上下文令牌 $I_t$ 以及噪声视频潜变量令牌沿**帧维度拼接**，共同输入扩散Transformer。消融实验表明，帧维度拼接优于通道维度或视图维度拼接。

#### 4. 相机轨迹与文本提示注入

目标相机参数 $C$ 通过可学习的编码器投影后注入视频令牌中；文本提示 $P$ 则通过交叉注意力层注入Transformer。这一设计使模型能够同时响应相机控制信号和语义内容指令。

### 关键训练策略：打乱上下文图像对齐

为防止模型依赖场景图像的固定顺序先验（例如直接复制最后一张图像内容），CINESCENE在训练时采用随机打乱策略：

- **固定第一张场景图像的位置**，使其始终对应生成视频的起始视角。
- **随机打乱其余19张场景图像的顺序**。

这一策略迫使模型学习像素上下文与隐式3D表示之间的真正对齐，而非利用位置捷径。消融实验（Table 3）证实，打乱策略在场景一致性和相机准确性上均优于有序输入和渐进训练。

### 与损失引导方法的本质区别

CINESCENE将隐式3D信息作为**上下文条件**注入，而损失引导方法则将VGGT特征用于构造监督损失，惩罚生成结果与静态场景的偏差。前者在架构层面解耦了静态背景与动态前景，能够生成无伪影的动态主体；后者因损失约束倾向于抑制前景变化，导致动态内容生成时出现伪影（Figure 5）。定量对比显示，上下文条件机制在场景一致性指标上优于损失引导方式（Mat. Pix.: 4617.51 vs 4509.46，Table 2）。

![[assets/figures/papers/paper_list_l2449_https_arxiv_org_abs_2602_06959/figures/006_Figure_5.jpg]]
*Figure 5: Qualitative ablation study on injecting implicit 3D methods. Loss-guided method shows artifacts when generating dynamic subject*

### 补充图表

![[assets/figures/papers/paper_list_l2449_https_arxiv_org_abs_2602_06959/figures/011_Figure_6.jpg]]
*Figure 6: Qualitative ablation study on shuffled context images. The shuffled mechanism leads to better joint modeling and learning in scene consistency, while the ordered ones are tend to copy content from last provided image*



## 实验与关键发现

### 核心瓶颈与验证逻辑

现有方法在生成大视角变化的视频时面临一个根本性矛盾：**2D上下文方法**（如FramePack）缺乏空间理解能力，无法在视角大幅变化时保持场景一致性；**显式3D引导方法**（如Gen3C）虽引入几何信息，却依赖不完美的重建结果，且其损失监督机制倾向于抑制动态内容的生成。CINESCENE的因果调节变量在于：将隐式3D场景表示作为**上下文条件**而非损失信号注入预训练T2V扩散模型，使模型能够解耦静态场景与动态前景。实验设计围绕两条主线展开：一是验证隐式3D条件注入对场景一致性的提升幅度，二是检验上下文条件机制相比损失引导方式的优越性。

### 主实验结果

**Table 1** 报告了在Scene-Decoupled Video Dataset保留测试集上的全面对比。CINESCENE在场景一致性上全面超越上下文基线FramePack：Mat. Pix.从4107.45提升至**4617.51**（+12.4%），PSNR从11.89提升至**14.51**（+2.62 dB），SSIM从0.38提升至**0.41**。与显式3D方法Gen3C相比，CINESCENE在场景一致性和相机准确性上均取得更优结果（RotErr: 2.68 vs 2.93, TransErr: 5.15 vs 5.82），且无需依赖不完美的几何重建。在相机准确性上，CINESCENE的RotErr（2.68）与专用相机控制方法Traj-Attn（2.66）和RecamMaster（2.67）相当，CamMC（6.88）甚至优于两者（7.12和7.16），表明隐式3D条件在保持场景一致性的同时有效传递了相机信息。

**Table 4** 的域外（OOD）泛化测试进一步验证了方法的鲁棒性。在DiT360测试集上，CINESCENE相对FramePack的优势进一步扩大：Mat. Pix.从4025.98提升至**4726.57**（+17.4%），PSNR从9.99提升至**12.02**（+2.03 dB）。这一结果表明，隐式3D表示赋予模型的场景理解能力具有跨数据分布的泛化性。

### 消融实验

**隐式3D表示成分消融**（Table 2）揭示了内容信息与视角信息联合建模的必要性。仅使用图像特征（Image Feature Only）或仅使用相机特征（Camera Feature Only）时，场景一致性指标均显著下降（Mat. Pix.分别为4520.26和4547.95，vs Ours的4617.51）。完全无隐式3D条件（w/o Implicit 3D）时性能最低（Mat. Pix. 4496.88），证实了隐式3D信息对场景一致性的因果贡献。关键对比来自损失引导方式（Loss-Guided）：其Mat. Pix.为4509.46，低于上下文条件机制（4617.51），且**Figure 5**的定性结果显示损失引导方法在生成动态主体时产生明显伪影——这是因为损失函数惩罚与静态场景的偏离，本质上抑制了前景运动。

**上下文图像打乱策略消融**（Table 3, Figure 6）验证了训练策略的设计合理性。随机打乱（Shuffled）在场景一致性（Mat. Pix. 4617.51）和相机准确性（RotErr 2.68）上均优于有序输入（Ordered, Mat. Pix. 4559.91, RotErr 2.96）和渐进训练（Progressive, Mat. Pix. 4549.17, RotErr 2.79）。Figure 6的定性结果表明，有序输入倾向于“复制”最后一张上下文图像的内容，而非真正理解场景的3D结构；打乱策略迫使模型学习像素上下文与隐式3D表示之间的对齐，从而增强了对隐式3D信息的依赖。

**场景上下文图像数量消融**（Table 5）显示，随着视图数从4增加到20，场景一致性（Mat. Pix.从4466.11升至4617.51）和相机精度（RotErr从3.80降至2.68）持续改善，20张视图取得最佳结果。这验证了多视角信息对构建完整场景表示的重要性。

**特征融合策略消融**（Table 8）表明，帧维度拼接（frame-dim concatenation）优于通道维度或视图维度拼接；图像特征与相机特征的融合方式上，元素级加法优于直接拼接Fi和Fc。这些设计选择均经过定量验证。

### 失败模式与局限

论文明确指出的局限包括：（1）当前仅生成77帧、最大视角变化75度的短视频片段，扩展至更长视频和更大视角变化仍是开放问题；（2）假设第一张场景图像与生成视频的首帧共享同一视角，限制了从任意相机位姿开始生成的灵活性；（3）受限于预训练T2V模型的能力，大幅运动下的人物细节可能出现失真；（4）训练数据虽多样化但均为合成渲染数据，对极端真实场景的泛化能力有待进一步检验。

### 公平性说明

所有上下文基线方法（FramePack, CaM）均在同一基础T2V模型和Scene-Decoupled Video Dataset上以相同训练设置重新实现；相机控制方法（RecamMaster, Traj-Attn）使用官方代码默认参数；Gen3C使用其默认推理配置。评估涵盖场景一致性、相机准确性、文本对齐和视频质量四个维度，并在域内和域外数据上进行测试，比较框架具有充分公平性。

### 补充图表

![[assets/figures/papers/paper_list_l2449_https_arxiv_org_abs_2602_06959/figures/004_Table_1.jpg]]
*Table 1: Quantitative comparision with previous methods. We compare CINESCENE with FramePack [71] on scene consistency, Context-as-Memory [68] and Gen3C [45] on both scene consistency and camera accuracy, Traj-Attn [63] and RecamMaster [2] on camera accuracy. We follow [64] to evaluate video quality on VBench*

![[assets/figures/papers/paper_list_l2449_https_arxiv_org_abs_2602_06959/figures/005_Figure_4.jpg]]
*Figure 4: Qualitative comparison of CINESCENE and previous context-based, explicit 3D guidance, camera-controlled methods. We present dynamic scenes, static scenes compared with FramePack [71], CaM [68], and Gen3C [45], camera-control with Traj-Attn [63] and RecamMaster [2]. We provide scene ground truth (gt) for comparison. We only show 4 scene context images for illustration*

![[assets/figures/papers/paper_list_l2449_https_arxiv_org_abs_2602_06959/figures/007_Table_2.jpg]]
*Table 2: Ablation on scene implicit 3D representation*

![[assets/figures/papers/paper_list_l2449_https_arxiv_org_abs_2602_06959/figures/009_Table_3.jpg]]
*Table 3: Ablation on shuffled context images*

![[assets/figures/papers/paper_list_l2449_https_arxiv_org_abs_2602_06959/figures/012_Table_4.jpg]]
*Table 4: Quantitative comparision with previous methods on OOD test set. We compare CINESCENE with FramePack [71] on scene consistency, Context-as-Memory [68] and Gen3C [45] on both scene consistency and camera accuracy, Traj-Attn [63] and RecamMaster [2] on camera accuracy. We follow [64] to evaluate video quality on VBench*

![[assets/figures/papers/paper_list_l2449_https_arxiv_org_abs_2602_06959/figures/013_Table_5.jpg]]
*Table 5: Ablation study on number of scene context images*

![[assets/figures/papers/paper_list_l2449_https_arxiv_org_abs_2602_06959/figures/016_Table_8.jpg]]
*Table 8: Ablation study on different feature fusion strategies*

![[assets/figures/papers/paper_list_l2449_https_arxiv_org_abs_2602_06959/figures/010_Figure_8.jpg]]
*Figure 8: Qualitative results of CINESCENE with diverse scenes, dynamic subjects, and camera trajectories. Our method shows promising application of virtual stage and cinematic language in cinematic video generation*

![[assets/figures/papers/paper_list_l2449_https_arxiv_org_abs_2602_06959/figures/017_Table_9.jpg]]
*Table 9: Ablation on camera control condition. Supplement to Table 2*



## 定位与知识库关联

### 任务定位与核心差异

CINESCENE 解决的是**大视角变化下的场景一致性视频生成**问题，其核心矛盾在于：生成模型需要同时保持静态场景的3D几何一致性，又能自由生成动态前景内容。这一需求将现有方法划分为两条技术路线：

- **2D上下文方法**：如 **FramePack** (Zhang and Agrawala, arXiv 2025) 和 **Context-as-Memory (CaM)** (Yu et al., arXiv 2025)，将场景图像作为像素级上下文条件注入视频扩散模型。这类方法缺乏对场景3D结构的显式理解，在大视角变化时难以维持几何一致性——Table 1显示，FramePack在场景一致性指标Mat. Pix.上仅为4107.45，远低于CINESCENE的4617.51。
- **显式3D引导方法**：如 **Gen3C** (Zhang et al., CVPR 2025)，依赖显式3D重建（如点云或深度图）来约束生成过程。然而，不完美的几何重建会引入伪影，且显式约束往往限制动态内容的生成自由度。

CINESCENE 的关键创新在于将**隐式3D场景表示以上下文条件（而非损失引导）的形式注入预训练T2V模型**，从而解耦静态场景与动态前景。这一设计选择从根本上区别于上述两类方法：既不依赖2D像素对应，也不受显式几何重建精度的制约。

### 与相机控制方法的关系

在相机轨迹遵循能力上，CINESCENE 与专门的相机控制方法形成互补而非替代关系。**Traj-Attn** 和 **RecamMaster** (Bai et al., arXiv 2025) 专注于通过注意力机制或条件编码实现精确的相机运动控制，但通常不解决场景内容的一致性问题。Table 1显示，CINESCENE在相机准确性指标RotErr（2.6825）上已达到与RecamMaster（2.7106）相当甚至更优的水平，同时额外提供了场景一致性保证。这表明隐式3D场景表示天然蕴含了相机-场景的耦合信息，使模型在生成过程中隐式地学习到正确的多视图几何关系。

### 条件注入 vs. 损失引导：架构设计的根本分歧

CINESCENE 在方法谱系中一个重要的定位锚点是**条件机制的选择**。Figure 3明确对比了两种隐式3D注入范式：

- **上下文条件注入（CINESCENE采用）**：将VGGT提取的隐式3D特征$F \in \mathbb{R}^{20 \times k \times 2048}$编码为令牌$F_t$，与场景图像令牌$I_t$和噪声视频潜变量沿帧维度拼接，共同输入扩散Transformer。这种设计使模型将静态场景视为“已知上下文”，将动态前景视为“生成目标”，天然解耦两者。
- **损失引导方式**：利用VGGT特征构建监督损失，惩罚生成视频与静态场景的偏差。Table 2的消融实验表明，损失引导方法在场景一致性上（Mat. Pix.: 4509.46）弱于上下文条件注入（4617.51），且Figure 5显示其在生成动态主体时出现明显伪影。根本原因在于：损失引导强制约束生成内容与静态场景的相似性，反而抑制了动态内容的合理生成。

这一发现对后续研究具有方法论意义——当任务需要同时保持场景约束和生成自由度时，条件注入比损失监督更适合作为3D先验的传递机制。

### 训练策略的关键作用：打乱上下文图像

CINESCENE 的另一重要设计是**随机打乱场景上下文图像的训练策略**（固定首张图像对应起始视角）。Table 3的消融实验证实，打乱策略（Shuffled）在场景一致性和相机准确性上均显著优于有序输入（Ordered）和渐进训练（Progressive）。Figure 6的定性结果表明，有序输入容易导致模型复制末张图像的内容，而非真正学习隐式3D表示。这一发现揭示了上下文条件生成中的一个普遍陷阱：模型可能依赖输入顺序的位置先验，而非学习底层的空间结构。打乱策略通过打破这种虚假相关性，迫使模型学习像素上下文与隐式3D表示之间的真正对齐。

### 适用边界与局限

基于论文提供的证据，CINESCENE 的适用边界可归纳如下：

1. **时序与视角范围**：当前仅支持生成77帧、最大视角变化75度的短视频片段。这是预训练T2V模型和训练数据规模的直接限制，而非方法本身的根本瓶颈。扩展至更长视频和360°以上连续大视角变化需要解决注意力机制的扩展性和长程一致性维持问题。

2. **起始视角假设**：方法假设第一张场景图像与生成视频的首帧共享同一视角。这一简化假设降低了问题复杂度，但也限制了从任意相机位姿开始生成的灵活性。未来需支持自动对齐机制。

3. **人物运动质量**：受限于预训练T2V模型的能力上限，生成的人物大幅运动可能出现失真。这是基座模型的固有限制，而非场景表示方法的缺陷。

4. **数据依赖性**：训练数据虽多样化（35个高质量3D环境，46K视频-场景图像对），但均为合成渲染数据。Table 4的域外测试（DiT360 OOD Test）显示方法具有一定泛化潜力（Mat. Pix.: 4726.57），但对极端真实场景的泛化能力仍需进一步检验。

### 开放问题与后续方向

从CINESCENE的局限出发，可识别以下开放问题：

- **长视频场景一致性**：如何将隐式3D场景表示扩展至数分钟级长视频，并支持360°以上的连续大视角变化？这可能需要层次化的场景表示或动态更新的隐式3D特征。
- **任意起始位姿对齐**：当场景图像与起始视频视角不一致时，如何自动对齐并保持一致性？这涉及视角插值或场景表示的旋转不变性设计。
- **动态人物生成质量**：如何解耦并改善大幅运动下的人物细节生成？可能需要额外的运动先验或人物特定的微调策略。
- **真实数据适配**：如何利用少量真实数据微调以减少对合成数据的依赖，同时保持泛化能力？少样本领域自适应和域随机化可能是可行路径。

### 知识库定位总结

CINESCENE 在视频生成方法谱系中占据了一个独特位置：它桥接了2D上下文生成与3D感知生成之间的鸿沟，通过隐式3D场景表示的条件注入，在不牺牲动态生成自由度的前提下实现了大视角场景一致性。其核心贡献——上下文条件注入优于损失引导、打乱训练策略打破位置先验——为后续研究提供了可复用的设计原则。该方法当前适用于中等长度、中等视角变化的电影级视频生成场景（如虚拟舞台应用，Figure 8），向更长时序和更大视角的扩展是明确的演进方向。



## 原文 PDF

![[paperPDFs/CVPR_2026/CineScene_Implicit_3D_as_Effective_Scene_Representation_for_Cinematic_Video_Generation.pdf]]
