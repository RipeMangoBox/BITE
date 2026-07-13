---
title: "Light-X: Generative 4D Video Rendering with Camera and Illumination Control"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/Light_X_Generative_4D_Video_Rendering_with_Camera_and_Illumination_Control_d4dde8c331aa.pdf
project_link: "https://www.pexels.com"
code_link: "https://github.com/aigc-apps/"
aliases:
- LX
- Light-X
tags:
- ICLR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
- topic/generative_models_diffusion
core_operator: 显式解耦几何/运动与光照信号：通过动态点云投影提供细粒度几何线索，并将重光照帧投影到同一几何空间提供照明线索，从而独立或联合调控相机与光照。
primary_logic: 分别构建动态点云与重光照点云，沿用户相机轨迹投影获得几何对齐的渲染视图与可见性掩码，实现几何与光照的解耦条件注入；同时设计退化驱动的数据管道Light-Syn，利用逆几何映射从野外单目视频合成配对训练数据，解决了数据匮乏问题。
claims:
- Light-X 在联合相机-光照控制任务中显著优于所有基线方法，FID 降低至 101.06，Motion Pres. 降至 2.007，用户研究中各项指标均超过 85% 的偏好。
- 在真实野外视频的联合控制评估中，Light-X 取得最高 PSNR (13.96) 和最佳 FVD (45.91)，验证了其在复杂场景下的泛化能力。
- 文本条件下的视频重光照实验表明，Light-X 在 FID (83.65)、Motion Pres. (1.137) 和用户研究上均优于 Light-A-Video 等专用重光照方法。
- 对于背景图像驱动的重光照，Light-X 在 FID (61.75/56.60)、Aesthetic 和 Motion Pres. 上大幅超越 Light-A-Video 与 RelightVid。
---

# Light-X: Generative 4D Video Rendering with Camera and Illumination Control

> [!tip] 核心洞察
> 分别构建动态点云与重光照点云，沿用户相机轨迹投影获得几何对齐的渲染视图与可见性掩码，实现几何与光照的解耦条件注入；同时设计退化驱动的数据管道Light-Syn，利用逆几何映射从野外单目视频合成配对训练数据，解决了数据匮乏问题。

| 字段 | 内容 |
|------|------|
| 中文题名 | Light-X：具有相机和照明控制的生成式4D视频渲染 |
| 英文题名 | Light-X: Generative 4D Video Rendering with Camera and Illumination Control |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=VBew6vESGL) · [Code](https://github.com/aigc-apps/) · [Project](https://www.pexels.com) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction #topic/generative_models_diffusion |
| Method | Light-X |
| Dataset | Joint Camera-Illumination Control, Video Relighting, Foreground Video Relighting |

> [!tip] 效果简介
> - Joint Camera-Illumination Control 上，FID ↓ 101.06 vs 122.73 (TL-Free) (-21.67)；Motion Pres. ↓ 2.007 vs 3.356 (TL-Free) (-1.349)。
> - Joint Camera-Illumination Control (Real Videos) 上，PSNR ↑ 13.96 vs 13.49 (TL-Free) (+0.47)。
> - Video Relighting (Text-conditioned) 上，FID ↓ 83.65 vs 112.45 (LAV) (-28.80)。

## 概要

**Light-X** 是首个从单目视频中实现对相机轨迹与光照进行联合控制的生成式框架。其核心动机源于现有视频重光照方法面临的根本性瓶颈：**光照保真度与时间一致性之间存在难以调和的权衡**，且缺乏对相机运动的联合操控能力。更深层的障碍在于，配对的多视角、多光照视频数据极度匮乏，严重制约了学习解纠缠表征的可能性。

Light-X 的关键洞察在于**显式解耦几何/运动信号与光照信号**。具体而言，它从输入视频估计深度并构建动态点云，沿用户指定的相机轨迹投影，获得几何对齐的渲染视图与可见性掩码，以此提供细粒度的几何线索；同时，利用图像重光照先验（IC-Light）对单帧进行重光照，再将重光照帧通过相同的深度投影至目标视角，获得几何对齐的光照线索。这种设计使得相机与光照能够独立或联合调控，从机制上绕开了传统方法的耦合困境。

为突破数据瓶颈，本文提出了 **Light-Syn**——一种退化驱动的数据管道。该管道以野外单目视频为真值，通过逆几何映射合成退化输入及其对应的几何对齐条件，构建了覆盖静态、动态和 AI 生成场景的大规模配对训练集，从而无需依赖稀缺的真实配对数据或图形学合成的重光照样本。

在联合相机-光照控制任务上，Light-X 显著优于所有组合基线方法，FID 降至 **101.06**，运动保持性（Motion Pres.）降至 **2.007**，用户研究中各项指标均获得超过 85% 的偏好率。在文本条件和背景图像驱动的视频重光照任务中，该方法同样以明显优势超越了专用重光照方法（如 **Light-A-Video** 和 **RelightVid**），并在真实野外视频上展现出更强的泛化能力。消融实验系统性地验证了 Light-Syn 三类训练数据、细粒度光照线索、全局照明控制模块以及软掩码域指示器等设计的关键贡献。

### 问题背景：可控制视频生成的新挑战

近年来，视频生成领域取得了显著进展，但大多数方法仍局限于“从文本到视频”或“从图像到视频”的单一生成范式，缺乏对生成过程进行精细空间与物理条件控制的能力。在实际应用中，用户往往不仅希望生成一段视频，更希望**同时控制相机的运动轨迹和场景的照明条件**——例如，在电影预演中调整镜头角度并改变光照氛围，或在虚拟现实中以特定视角观察不同光照下的动态场景。

这一任务——即从单目视频输入出发，实现**联合相机轨迹与照明控制的4D视频渲染**——面临两个根本性挑战：

1. **光照保真度与时间一致性的权衡**：现有视频重光照方法在改变场景光照时，难以同时保持帧间的平滑过渡和几何结构的一致性。当相机视角也发生变化时，这种张力被进一步放大，因为模型需要在新的视角下合成未见过的内容，同时维持光照的自然感。

2. **配对训练数据的极度匮乏**：学习解纠缠的几何与光照表征需要大量“同一场景、不同视角、不同光照”的配对视频数据。然而，在真实世界中获取此类数据几乎不可能，严重制约了监督学习方法的发展。

### 现有方法缺口

当前相关工作可大致分为三类，但均无法有效解决上述联合控制问题：

- **相机控制方法**（如 **TrajectoryCrafter**（YU et al., 2025）、**ReCamMaster**（Bai et al., 2025）、**Free4D**（Liu et al., 2025a））专注于沿用户指定轨迹重定向视频，但完全忽略光照编辑能力。它们通常依赖隐式的相机参数嵌入或逐场景优化，缺乏对场景照明的显式建模。

- **视频重光照方法**（如 **Light-A-Video**（Zhou et al., 2025）、**IC-Light**（Zhang et al., 2025b）、**RelightVid**（Fang et al., 2025））能够根据文本提示或背景图像改变视频的光照，但假设相机视角固定不变。它们在面对视角变化时无法生成几何一致的新视图内容，且光照编辑与运动控制相互耦合。

- **通用视频编辑方法**（如 **AnyV2V**（Ku et al., 2024））提供了一定程度的灵活性，但缺乏对相机和光照的专门化控制机制，在联合控制任务上表现不佳。

**核心瓶颈**在于：现有方法将几何/运动信号与光照信号混合处理，缺乏一种**显式解耦**的机制来分别建模并联合调控这两个维度。同时，由于缺乏配对的多视角、多光照视频数据，学习这种解耦表征变得异常困难。

### 本文动机与核心思路

针对上述缺口，本文提出 **Light-X**——首个从单目视频出发，实现**联合相机轨迹与照明控制的生成式4D视频渲染框架**。

Light-X 的核心洞察是：**分别构建动态点云与重光照点云，沿用户相机轨迹投影获得几何对齐的渲染视图与可见性掩码，从而实现几何与光照的解耦条件注入**。具体而言：

- **几何与运动信号**通过从源视频估计深度并反投影构建动态点云来捕获，随后沿用户指定的相机轨迹投影，生成几何对齐的渲染视图和可见性掩码，为模型提供细粒度的几何线索。
- **光照信号**通过将重光照帧投影到同一几何空间获得对齐的照明线索，确保光照编辑与场景几何保持一致。
- **数据困境**通过 **Light-Syn** 退化驱动管道解决：以野外单目视频为真值，利用逆几何映射合成退化输入及其条件，构建包含静态、动态和AI生成场景的配对训练数据集。

这一解耦设计使得 Light-X 能够独立或联合调控相机运动与照明条件，突破了现有方法在光照保真度与时间一致性之间的根本性权衡，为可控制4D视频生成开辟了新路径。

## 核心方法与创新机理

Light-X 的核心创新在于对几何/运动信号与光照信号进行**显式解耦**，从而首次实现联合相机轨迹与照明的可控视频生成。与现有方法将相机参数嵌入或光照特征简单拼接不同，Light-X 通过以下关键设计突破瓶颈。

### 几何与光照的解耦条件注入

现有视频重光照方法面临光照保真度与时间一致性之间的根本性权衡，且缺乏联合控制能力。Light-X 的解决方案是分别构建两类动态点云，并沿用户相机轨迹投影为几何对齐的条件信号：

- **几何与运动条件**：从源视频估计深度图，通过反投影构建动态点云 $P_i = \Phi^{-1}(I_i^s, D_i^s; K)$。沿用户指定的相机轨迹 $C$ 投影，生成几何对齐的渲染视图 $I_i^p$ 与可见性掩码 $M_i^p$，为模型提供细粒度的几何线索。相比 **TrajectoryCrafter**（Yu et al., 2025）等无显式 3D 条件的方法，这一设计直接编码了视角变换的几何约束。

- **光照条件**：选取源视频的某一帧，通过 **IC-Light**（Zhang et al., 2025b）进行单帧重光照，构建稀疏重光照视频 $\hat{V}^s$。利用相同的深度图将其反投影为重光照点云 $\hat{P}_i = \Phi^{-1}(\hat{I}_i^s, D_i^s; K)$，再投影到目标视角获得几何对齐的重光照渲染视图 $\hat{I}_i^p$ 与掩码 $\hat{M}_i^p$。这确保了光照线索与源视频在几何空间中对齐，避免了 **Light-A-Video**（Zhou et al., 2025）等方法中光照信息与几何脱节的问题。

### 全局照明一致性的维持

仅依赖帧级局部条件容易导致照明衰减或突变。Light-X 引入 **Light-DiT 层**与 **Q-Former** 结构：Q-Former 从重光照帧中提取全局照明 token $\mathcal{T}_{\mathrm{illum}}$，通过交叉注意力注入 DiT 块的视觉 token 中：

$$\mathcal{T}_{\mathrm{vision}}' = \mathrm{CrossAttn}(Q=\mathcal{T}_{\mathrm{vision}}, K=V=\mathcal{T}_{\mathrm{illum}})$$

消融实验证实，禁用该全局控制模块会导致性能恶化（Table 6, b.ii），验证了其对于维持长序列照明一致性的关键作用。

### 退化驱动的数据管道 Light-Syn

配对的多视角、多光照视频数据极度稀缺，严重制约了学习解纠缠表征的能力。Light-X 提出 **Light-Syn**，一种退化驱动的数据构建管道：以野外单目视频为真值 $V^t$，通过逆几何映射合成退化输入 $V^s$ 及其条件（渲染视图、掩码、重光照对应项），构建包含静态场景、动态场景和 AI 生成场景的配对训练数据集。消融实验表明，删除任意一种数据（静态/动态/AI 生成）均会导致 FID 显著上升（Table 6, a.i–a.iii），证明了数据多样性的必要性。

### 多照明模态的统一适配

为支持 HDR 环境图、参考图像和文本等多种照明条件，Light-X 采用软加权掩码作为域指示器：

$$(\hat{V}^p, \hat{V}^m) = (V_k, \alpha_k \mathbf{1}), \quad k \in \{\mathrm{ref}, \mathrm{hdr}\}$$

其中 $\alpha_{\mathrm{ref}}=0.25$，$\alpha_{\mathrm{hdr}}=0.50$。这一设计使单一模型能够泛化到不同照明模态，移除该软掩码设计会导致性能下降（Table 6, c.iii），证实了其有效性。

### 创新总结

| 改进槽位 | 基线方法 | Light-X 方案 |
|---------|---------|-------------|
| 几何条件 | 无显式 3D 几何，或相机参数嵌入 | 动态点云投影的几何对齐视图与可见性掩码 |
| 光照条件 | 文本特征拼接，或未对齐的重光照帧 | 重光照帧通过深度投影至目标视角，获得几何对齐的光照线索 |
| 全局照明一致性 | 无全局约束，或仅依赖局部帧级条件 | Light-DiT + Q-Former 提取全局照明 token，交叉注意力注入 |
| 训练数据 | 依赖合成重光照或缺乏配对数据 | Light-Syn 退化驱动管道，合成静态/动态/AI 场景的配对数据 |
| 多照明模态 | 硬掩码或单一模态 | 软加权掩码作为域指示器，统一支持 HDR/参考图像/文本 |

这些创新共同构成了 Light-X 在联合相机-光照控制任务中显著优于所有基线方法（FID 101.06 vs. 122.73，Table 1）的技术基础。

Light-X 的核心设计理念是**显式解耦几何/运动信号与光照信号**，从而实现对相机轨迹和光照条件的独立或联合控制。整个框架以单目视频为输入，通过动态点云构建、几何对齐投影、条件注入与扩散模型去噪四个关键阶段，生成符合目标相机轨迹和光照条件的 4D 视频。

### 输入输出定义

设源视频为 $V^s = \{I_i^s\}_{i=1}^f$，目标视频为 $V^t = \{I_i^t\}_{i=1}^f$，两者描述同一动态场景，但 $V^t$ 需遵循用户指定的相机轨迹 $\mathcal{C}$ 和目标光照条件（文本提示、参考图像或 HDR 环境图）。框架的任务是建模条件分布：

$$x \sim p(x \mid V^s, \hat{V}^s, V^p, \hat{V}^p, V^m, \hat{V}^m)$$

其中 $V^p, V^m$ 为源视频的几何对齐投影视图与可见性掩码，$\hat{V}^s$ 为稀疏重光照视频，$\hat{V}^p, \hat{V}^m$ 为对应的重光照投影视图与掩码。

### 模块关系与数据流

**1. 动态点云构建（Dynamic Point Cloud Construction）**

首先对源视频 $V^s$ 逐帧估计深度图 $D_i^s$（使用 Hu et al., 2024 的深度估计器），结合相机内参 $K$ 将每帧反投影到 3D 空间，构建动态点云 $P_i$：

$$P_i = \Phi^{-1}(I_i^s, D_i^s; K)$$

**2. 稀疏重光照视频生成**

选取源视频中的某一帧（通常为第一帧），利用 **IC-Light**（Zhang et al., 2025b）在目标光照条件下对该帧进行重光照，得到重光照图像。将该图像与原始深度图 $D_i^s$ 结合，形成稀疏重光照视频 $\hat{V}^s$，其中仅参考帧包含重光照信息，其余帧保持原始内容。

**3. 几何对齐投影（Geometry-aligned Projection）**

将源点云和重光照点云分别沿用户指定的相机轨迹 $\mathcal{C}$ 投影到目标视角，生成几何对齐的渲染视图与可见性掩码：

- 源点云投影：$I_i^p, M_i^p = \Phi(R_i P_i + t_i; K)$
- 重光照点云投影：$\hat{I}_i^p, \hat{M}_i^p = \Phi(R_i \hat{P}_i + t_i; K)$

其中 $R_i, t_i$ 为目标相机位姿。重光照点云 $\hat{P}_i$ 通过将稀疏重光照帧以原始深度反投影得到，确保与源视频的几何对齐：

$$\hat{P}_i = \Phi^{-1}(\hat{I}_i^s, D_i^s; K)$$

这一双重投影机制是 Light-X 实现**几何与光照解耦**的关键：源点云投影提供细粒度几何线索（告知模型“场景在目标视角下应该长什么样”），重光照点云投影提供细粒度光照线索（告知模型“场景在目标光照下应该呈现何种外观”），而可见性掩码则指示投影中的有效区域与空洞区域。

**4. VAE 编码与 Patchification**

将源视频帧、投影视图和掩码分别通过 VAE 编码器映射到潜在空间，并进行分块（patchification）处理，转化为视觉 token 序列 $\mathcal{T}_{\text{vision}}$。文本条件则通过 CLIP 编码为文本 token，与视觉 token 融合。

**5. Light-DiT 与全局照明控制**

为抑制长序列中的光照衰减和突变，Light-X 引入 **Light-DiT** 层与 **Q-Former** 模块。Q-Former 从重光照帧中提取紧凑的全局照明 token $\mathcal{T}_{\text{illum}}$，通过交叉注意力注入视觉 token：

$$\mathcal{T}_{\text{vision}}' = \text{CrossAttn}(Q=\mathcal{T}_{\text{vision}}, K=V=\mathcal{T}_{\text{illum}})$$

这一设计使模型在逐帧去噪过程中始终感知全局照明上下文，保持长视频序列的光照一致性。

**6. DiT 与 Ref-DiT 去噪**

框架保留了 **TrajectoryCrafter**（YU et al., 2025）中的原始 DiT 和 Ref-DiT 模块：DiT 聚合文本-视觉信息进行去噪，Ref-DiT 通过参考源视频维持 4D 一致性（包括内容、运动和身份保持）。最终，VAE 解码器将去噪后的潜在表示重建为目标视频 $V^t$。

### 多照明模态适配

为支持文本、参考图像和 HDR 环境图等多种照明条件，Light-X 采用**软加权掩码**作为域指示器：

$$(\hat{V}^p, \hat{V}^m) = (V_k, \alpha_k \mathbf{1}), \quad k \in \{\text{ref}, \text{hdr}\}$$

其中 $\alpha_{\text{ref}} = 0.25$，$\alpha_{\text{hdr}} = 0.50$。这一设计使单一模型能够泛化到不同的照明模态，而无需为每种模态训练独立模型。

### 数据管道：Light-Syn

训练数据的匮乏是制约联合控制的核心瓶颈。Light-X 提出了**退化驱动的数据管道 Light-Syn**（详见 Figure 3）：以野外单目视频 $V^t$ 为真值，通过逆几何映射合成退化输入 $V^s$ 及其对应的几何对齐条件（$V^p, V^m, \hat{V}^p, \hat{V}^m$）。该管道覆盖静态场景、动态场景和 AI 生成场景三种类型，分别采用不同的退化策略（如相机抖动、局部遮挡、光照扰动等），构建了大规模配对训练数据。消融实验证实，删除任意一种类型的数据均会导致性能显著下降（Table 6）。

### 训练设置

模型在 $384 \times 672$ 分辨率、49 帧的视频上训练，共 16,000 次迭代，学习率为 $2 \times 10^{-5}$，batch size 为 8，使用 8 块 H100 GPU。推理阶段，生成一段 49 帧视频约需 1.83 分钟。

Light-X 的核心设计围绕一个根本性洞察展开：**将几何/运动信号与光照信号显式解耦**，分别通过动态点云投影提供细粒度几何线索，通过重光照点云投影提供对齐的照明线索，从而实现相机运动与光照的独立或联合调控。以下按模块拆解其关键机制。

### 动态点云构建与几何对齐投影

给定源视频 $V^s = \{I_i^s\}_{i=1}^f$，首先利用深度估计方法（Hu et al., 2024）逐帧估计深度图 $D_i^s$，然后通过逆透视投影将每帧反投影到 3D 空间，构建动态点云：

$$P_i = \Phi^{-1}(I_i^s, D_i^s; K)$$

其中 $K$ 为相机内参（经验设定），$\Phi^{-1}$ 表示从像素空间到相机坐标系的逆映射。对于用户指定的目标相机轨迹 $C = \{(R_i, t_i)\}_{i=1}^f$，将动态点云投影到各目标视角，获得几何对齐的渲染视图 $I_i^p$ 与可见性掩码 $M_i^p$：

$$I_i^p, M_i^p = \Phi(R_i P_i + t_i; K)$$

此步骤提供了**细粒度的几何线索**：渲染视图编码了目标视角下的场景结构，可见性掩码则指示了哪些区域在目标视角中可见，有效引导模型合成新视角内容。

### 重光照点云与照明线索注入

照明控制的核心是构建几何对齐的重光照条件。首先，对源视频的某一帧（通常为首帧）应用 IC-Light（Zhang et al., 2025b）进行图像级重光照，生成稀疏重光照视频 $\hat{V}^s$。利用与源视频相同的深度图，将重光照帧反投影为**重光照点云**：

$$\hat{P}_i = \Phi^{-1}(\hat{I}_i^s, D_i^s; K)$$

随后，将重光照点云沿相同的用户相机轨迹投影到目标视角：

$$\hat{I}_i^p, \hat{M}_i^p = \Phi(R_i \hat{P}_i + t_i; K)$$

这一设计的精妙之处在于：重光照帧与源视频共享深度图，确保了重光照点云与动态点云的**几何严格对齐**。投影后的 $\hat{I}_i^p$ 提供了目标视角下的照明参考，而 $\hat{M}_i^p$ 标记了重光照信息的有效区域（稀疏性掩码）。

### 条件编码与全局照明控制

将上述条件视图（源视频 $V^s$、稀疏重光照视频 $\hat{V}^s$、几何渲染视图 $V^p$、重光照渲染视图 $\hat{V}^p$ 及其掩码 $V^m$、$\hat{V}^m$）通过 VAE 编码为潜在空间并分块为视觉 token。目标视频的生成分布建模为：

$$x \sim p(x \mid V^s, \hat{V}^s, V^p, \hat{V}^p, V^m, \hat{V}^m)$$

为解决长序列中照明衰减或突变的问题，引入 **Light-DiT 层**与 **Q-Former** 实现全局照明控制。Q-Former 从重光照帧中提取全局照明 token $\mathcal{T}_{\text{illum}}$，随后在 Light-DiT 层中通过交叉注意力注入视觉 token：

$$\mathcal{T}_{\text{vision}}' = \text{CrossAttn}(Q=\mathcal{T}_{\text{vision}}, K=V=\mathcal{T}_{\text{illum}})$$

该机制使模型在去噪过程中持续感知全局照明状态，有效抑制了逐帧独立处理导致的照明不一致。同时，框架保留了原 DiT 与 Ref-DiT 模块（继承自 TrajectoryCrafter，YU et al., 2025），分别聚合文本-视觉信息并维持与源视频的 4D 一致性。

### 多照明模态的软掩码适配

为支持 HDR 环境图、参考图像和文本等多种照明条件，Light-X 采用软加权掩码作为域指示器：

$$(\hat{V}^p, \hat{V}^m) = (V_k, \alpha_k \mathbf{1}), \quad k \in \{\text{ref}, \text{hdr}\}$$

其中 $\alpha_{\text{ref}} = 0.25$，$\alpha_{\text{hdr}} = 0.50$。对于文本条件，重光照帧由 IC-Light 直接生成；对于参考图像和 HDR 环境图，则通过专门的数据构建管道（Figure 4）生成对应的 $\hat{V}^p$ 和软掩码。这一设计使单一模型能灵活适配不同照明模态，无需为每种条件训练独立模型。

![[assets/figures/papers/paper_list_l2_https_openreview_net_forum_id_VBew6vESGL/figures/004_Figure_4.jpg]]
*Figure 4: Left: Data curation pipelines for reference-image and HDR-map conditioned video generation. Right: Conditioning cues with soft masks used for model training*

### Light-Syn 数据管道

训练数据的匮乏是制约解耦表征学习的核心瓶颈。Light-Syn 采用**退化驱动**策略：以野外单目视频为真值 $V^t$，通过逆几何映射合成退化输入 $V^s$ 及其条件。针对静态、动态和 AI 生成场景分别设计退化策略（Figure 3），从 $V^s$ 出发计算 $V^p$、$V^m$，并利用 IC-Light 生成重光照对应项 $\hat{V}^p$、$\hat{V}^m$，构建完整的配对训练数据。消融实验（Table 6）证实，删除任意一种数据（静态/动态/AI生成）均导致 FID 显著上升，验证了多源数据对模型鲁棒性的关键作用。

![[assets/figures/papers/paper_list_l2_https_openreview_net_forum_id_VBew6vESGL/figures/003_Figure_3.jpg]]
*Figure 3: Overview of Light-Syn. From an in-the-wild video*

## 实验与关键发现

### 核心瓶颈与因果机制

现有视频重光照方法在光照保真度与时间一致性之间存在根本性权衡，且缺乏对相机运动与光照的联合控制能力。Light-X 通过显式解耦几何/运动与光照信号来解决这一问题：利用动态点云投影提供细粒度几何线索，同时将重光照帧投影到同一几何空间以提供照明线索，实现独立或联合调控。为突破配对数据匮乏的瓶颈，方法引入退化驱动的数据管道 Light-Syn，通过逆几何映射从野外单目视频合成配对训练数据。

### 实验设置

模型在 384×672 分辨率、49 帧的视频上训练，共 16,000 次迭代，学习率 $2 \times 10^{-5}$，batch size 为 8，使用 8 张 H100 GPU。视频深度由 Hu et al., 2024 估计以构建动态点云，相机内参根据经验设定。所有对比方法均使用公开的官方实现或默认超参数；联合相机-光照控制基线由现有相机控制方法和重光照方法组合而成。评估指标涵盖图像质量（FID、Aesthetic、PSNR、SSIM、LPIPS）、视频平滑度（Motion Pres.、CLIP similarity）以及用户研究（57 名参与者，从重光照质量、视频平滑度、ID 保持和 4D 一致性四个维度评估）。

### 联合相机-光照控制

Table 1 展示了联合相机-光照控制任务的定量结果。Light-X 取得 FID 101.06，显著优于最佳基线 TL-Free 的 122.73（降低 21.67）；Motion Pres. 降至 2.007（TL-Free 为 3.356），表明时间一致性大幅提升。用户研究中，Light-X 在各项指标上均获得超过 85% 的偏好率。值得注意的是，Light-X 的推理时间为 1.83 分钟，虽高于训练自由方法但远低于需要逐场景优化的 Free4D（Liu et al., 2025a）。

![[assets/figures/papers/paper_list_l2_https_openreview_net_forum_id_VBew6vESGL/figures/006_Table_1.jpg]]
*Table 1: Quantitative results for the joint camera-illumination control task. User preference indicates the percentage of participants who selected our method*

Table 2 使用真实野外视频作为参照进行评估。Light-X 取得最高 PSNR (13.96) 和最佳 FVD (45.91)，验证了其在复杂真实场景下的泛化能力。Figure 5 的定性对比进一步显示，Light-X 在重光照质量、时间一致性和新视图内容生成方面均优于基线方法。

### 视频重光照

文本条件下的视频重光照实验（Table 3）表明，Light-X 在 FID (83.65) 和 Motion Pres. (1.137) 上均优于专用重光照方法 Light-A-Video（Zhou et al., 2025）的 112.45 和 1.677，FID 降幅达 28.80。在真实野外视频评估中（Table 4），Light-X 取得最低 LPIPS (0.369)，优于 IC-Light（Zhang et al., 2025b）的 0.422。

![[assets/figures/papers/paper_list_l2_https_openreview_net_forum_id_VBew6vESGL/figures/008_Table_3.jpg]]
*Table 3: Quantitative results for video relighting. * indicates evaluation on the first 16 frames*

背景图像驱动的前景视频重光照任务（Table 5）中，Light-X 在 FID (61.75/56.60) 上大幅超越 Light-A-Video (76.05) 和 RelightVid（Fang et al., 2025），同时在 Aesthetic 和 Motion Pres. 指标上保持领先。

![[assets/figures/papers/paper_list_l2_https_openreview_net_forum_id_VBew6vESGL/figures/011_Table_5.jpg]]
*Table 5: Quantitative results for background image-conditioned foreground video relighting. Methods marked with * are evaluated on the first 16 frames*

### 消融实验

Table 6 系统消融了训练数据、架构设计和训练策略的影响：

![[assets/figures/papers/paper_list_l2_https_openreview_net_forum_id_VBew6vESGL/figures/012_Table_6.jpg]]
*Table 6: Qualitative ablation results for the joint camera-illumination control across different components: (a) training data, (b) architecture and lighting conditions, (c) training and conditioning strategy*

**训练数据消融（a 组）：**
- 移除静态数据导致 FID 上升至 123.35，削弱了未见视角的合成能力；
- 排除动态数据使 FID 变为 108.70 并引入运动伪影；
- 去除 AI 生成的数据降低对稀有光照（如霓虹灯）的鲁棒性，FID 为 102.09。

**架构与条件消融（b 组）：**
- 跳过细粒度光照线索限制了 IC-Light 先验的使用，重光照质量下降；
- 禁用全局照明控制（Light-DiT + Q-Former）导致光照衰减或不连续变化；
- 用文本-光照拼接替代几何对齐的条件输入无法利用细粒度照明先验，表现更差。

**训练策略消融（c 组）：**
- 将算法生成的输出作为真值会损害保真度和一致性；
- 重光照所有帧而非单帧虽改善 FID，但增加了计算成本并降低了时间连贯性；
- 移除软掩码设计（$\alpha_{\text{ref}}=0.25$, $\alpha_{\text{hdr}}=0.50$）导致性能下降，证实其对多照明模态泛化的重要性。

### 失败模式与局限性

1. **IC-Light 先验依赖**：方法依赖 IC-Light 作为重光照先验，其在非郎伯表面处理上的不完美会直接影响最终视频质量。
2. **大角度相机运动**：在超过 60° 的相机运动下性能逐渐下降，对完整 360° 场景支持不足。
3. **深度估计敏感性**：动态点云投影依赖深度估计精度；极端深度误差会导致几何错位和伪影，尽管方法对中等噪声具有鲁棒性（见 Table H）。
4. **光照分布偏差**：训练数据虽经 Light-Syn 扩展，但分布仍偏向常见光照和场景类型，对某些稀有或极端照明条件的泛化可能受限。
5. **计算开销**：推理需要多步去噪和点云投影计算，成本高于训练自由或轻量级基线。
6. **自训练边际收益**：使用 Light-X 自身生成的重光照数据微调仅带来边际收益（Table J），表明自训练策略尚未充分挖掘。

### 关键图表结论

- **Figure 6**：文本条件重光照的定性对比证实 Light-X 在重光照质量和时间一致性上均优于基线。
- **Figure J**：FID 随与参考帧时间距离的增加而上升，但在两种设置下均保持相对稳定，验证了全局照明控制模块的有效性。
- **Figure K / Table H**：深度噪声注入实验表明，方法在中等高斯噪声下仍能保持连贯的照明和运动一致性。
- **Table D**：重光照前后点云的 Chamfer Distance 评估证实方法能够保持几何一致性。

## 定位与知识库关联

### 1. 与现有工作的关系

Light-X 的核心贡献在于首次将**相机轨迹控制**与**视频重光照**统一到一个生成框架中，填补了这两个独立研究线之间的空白。在它之前，这两个方向分别由不同的方法主导。

在相机控制方面，**TrajectoryCrafter** (YU et al., 2025) 和 **ReCamMaster** (Bai et al., 2025) 代表了基于扩散模型的新视角合成范式，它们能够根据用户指定的相机轨迹从单目视频生成新视图。然而，这些方法完全不支持光照编辑——它们只能忠实地复现源视频的光照条件。**Free4D** (Liu et al., 2025a) 虽然也支持相机控制，但需要逐场景优化，无法像 Light-X 那样实现前馈式推理。

在视频重光照方面，**Light-A-Video** (Zhou et al., 2025) 和 **RelightVid** (Fang et al., 2025) 分别针对文本条件和背景图像条件做了专门设计。**IC-Light** (Zhang et al., 2025b) 在图像级别的重光照上表现出色，但其视频扩展面临时间一致性的根本挑战。Light-X 巧妙地利用 IC-Light 作为稀疏重光照先验（仅对一帧操作），然后通过几何对齐的点云投影将光照信息传播到整个视频序列，从而绕过了逐帧独立重光照导致的时间闪烁问题。

**TC-Light** (Liu et al., 2025b) 和 **DiffusionRenderer** (Liang et al., 2025) 也尝试了将照明控制引入视频生成，但它们缺乏显式的 3D 几何约束，导致光照与场景几何的耦合不够紧密。Light-X 通过动态点云投影提供的细粒度几何线索，从根本上改善了这一问题。

在数据层面，Light-X 的 **Light-Syn** 管道借鉴了退化驱动训练的思想，但与以往工作不同的是，它通过**逆几何映射**从野外单目视频合成配对的训练数据，同时覆盖静态、动态和 AI 生成三种场景类型。这种数据构建策略使得模型能够学习到几何与光照的解耦表征，而不需要昂贵的多视角、多光照采集设备。

### 2. 适用边界

Light-X 的适用边界由其设计中的几个关键依赖所定义：

**深度估计依赖**：动态点云构建依赖于单目深度估计的精度。虽然实验表明方法对中等程度的高斯噪声具有鲁棒性（Table H），但在深度估计完全失效的场景（如透明物体、镜面反射、极端动态模糊）中，几何对齐的投影将引入显著的错位伪影。这是所有基于深度投影的方法共有的边界。

**重光照先验瓶颈**：Light-X 使用 IC-Light 作为重光照的初始信号源，因此 IC-Light 在图像级别的局限性——特别是对非 Lambertian 表面（如金属、丝绸）的处理不完美——会直接传递到最终视频中。Figure G 展示了在非 Lambertian 物体上的结果，但整体质量仍受限于该先验的能力上限。

**相机运动范围**：实验表明，当相机运动角度超过约 60° 时，性能开始逐渐下降。对于完整的 360° 环绕场景，动态点云中不可避免的遮挡区域会导致投影视图出现大面积空洞，而当前的补全机制尚不能完美处理这种情况。

**光照分布偏向**：尽管 Light-Syn 通过引入 AI 生成数据扩展了光照多样性，训练数据的分布仍然偏向常见的光照类型（日光、室内灯光等）。对于极端或罕见的光照条件（如强烈逆光、多色点光源混合），模型的泛化能力可能受限。

### 3. 局限与开放问题

**已确认的局限**：

1. **IC-Light 先验的传递性缺陷**：如方法本身所承认，IC-Light 在非 Lambertian 表面上的重光照质量不完美，这一缺陷会通过稀疏重光照帧传递到整个视频序列。目前没有机制能在视频层面修正这些图像级别的误差。

2. **大角度相机运动的退化**：当用户指定的相机轨迹偏离源视角超过约 60° 时，点云投影的覆盖范围不足，导致生成质量下降。这是动态点云表示本身的信息瓶颈——它只能提供源视角附近的可信几何信息。

3. **极端深度误差的脆弱性**：虽然对中等深度噪声具有鲁棒性，但当深度估计出现系统性偏差（如前景/背景深度反转）时，几何对齐的条件注入会失效。目前的噪声注入实验（Section D.13）仅测试了高斯噪声，未覆盖结构化深度误差。

4. **计算开销**：推理过程需要多步扩散去噪和点云投影计算，单次推理约需 1.83 分钟（Table 1），远高于训练自由的基线方法（如 IC-Light 的逐帧处理），限制了交互式应用场景。

5. **自训练策略未充分挖掘**：使用 Light-X 自身生成的重光照数据进行微调仅带来边际收益（Table J），表明当前的自提升策略尚未形成有效的正向反馈循环。

**开放问题**：

1. **全向 360° 控制的拓展**：能否通过引入更强的 3D 表示（如 3D Gaussian Splatting 或 NeRF 类的隐式场）来替代动态点云，从而支持任意角度的相机运动同时保持一致的照明？这需要解决新表示与扩散模型的集成问题。

2. **重光照先验的迭代提升**：是否可以通过多轮自提升策略——用 Light-X 的输出作为新的重光照先验，再次输入模型——来突破 IC-Light 的质量瓶颈？当前的自训练实验仅做了一轮微调，迭代潜力尚未被探索。

3. **合成重光照数据的域差距**：Table K 显示引入图形引擎合成的重光照数据对性能影响有限。如何生成更真实、更多样的合成数据，使其与真实视频的域差距足够小，从而有效增强训练？这涉及到渲染真实感与数据多样性的权衡。

4. **推理效率优化**：能否通过蒸馏、步数压缩或缓存点云投影结果来降低 1.83 分钟的推理延迟？特别是对于相机轨迹固定但光照变化的场景，点云投影可以预计算。

5. **物理条件的全面解耦**：Light-X 成功解耦了相机与光照，但场景的其他物理属性——材质反射率、表面粗糙度、环境遮挡——仍然耦合在源视频的内容表示中。能否将解耦的思路推广到这些维度，实现更全面的 4D 视频编辑？

6. **无深度估计的几何先验**：在深度估计不可靠的动态场景（如快速运动、复杂遮挡）中，是否可以通过光流一致性或可微渲染来隐式地提供几何约束，而不依赖显式的深度估计？这将从根本上消除方法对深度精度的依赖。

## 原文 PDF

![[paperPDFs/ICLR_2026/Light_X_Generative_4D_Video_Rendering_with_Camera_and_Illumination_Control_d4dde8c331aa.pdf]]
