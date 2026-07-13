---
title: "WorldSplat: Gaussian-Centric Feed-Forward 4D Scene Generation for Autonomous Driving"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/WorldSplat_Gaussian_Centric_Feed_Forward_4D_Scene_Generation_for_Autonomous_Driv_f29223160c30.pdf
project_link: "https://wm-research.github.io/worldsplat/"
code_link: null
aliases:
- WorldSplat
tags:
- ICLR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/image_and_video_generation
- topic/vision_multimodal_applications/3d_rendering_reconstruction
- topic/generative_models_diffusion
core_operator: 引入显式的4D高斯场景表示作为中间桥梁，使扩散模型生成包含RGB、深度和动态分割的多模态隐变量，并通过前馈解码器直接预测像素对齐的3D高斯并聚合成4D场景，从而同时实现生成灵活性与空间/时间一致性。
primary_logic: 通过4D感知的潜在扩散模型生成多模态隐变量（RGB、深度、动态掩码），经前馈Transformer解码器转化为显式4D高斯表示，并利用增强扩散模型对渲染视频进行质量优化，从而端到端生成高质量、时空一致的多轨迹新视角驾驶视频。
claims:
- 添加3D高斯显式场景表示使FVD从260.07降至75.26（−184.81），FID从41.40降至16.31（−25.09）
- 单帧3D高斯聚合为统一4D表示进一步将FVD从75.26降至50.73（−24.53），FID从16.31降至11.60（−4.71）
- 在±2m视角偏移下，WorldSplat的FVD为64.07，显著优于DiST-4D的105.29
- 几何一致性评估中，SSIM 0.912 远超 OmniScene 0.736，LPIPS 0.147 低于其 0.237
---

# WorldSplat: Gaussian-Centric Feed-Forward 4D Scene Generation for Autonomous Driving

> [!tip] 核心洞察
> 通过4D感知的潜在扩散模型生成多模态隐变量（RGB、深度、动态掩码），经前馈Transformer解码器转化为显式4D高斯表示，并利用增强扩散模型对渲染视频进行质量优化，从而端到端生成高质量、时空一致的多轨迹新视角驾驶视频。

| 字段 | 内容 |
|------|------|
| 中文题名 | WorldSplat：以高斯为中心的自动驾驶前馈式 4D 场景生成 |
| 英文题名 | WorldSplat: Gaussian-Centric Feed-Forward 4D Scene Generation for Autonomous Driving |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=KWeX6tYno6) · [Project](https://wm-research.github.io/worldsplat/) · [paper](https://arxiv.org/abs/2302.05543) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/image_and_video_generation #topic/vision_multimodal_applications/3d_rendering_reconstruction #topic/generative_models_diffusion |
| Method | WorldSplat |
| Dataset | nuScenes validation set video generation, nuScenes novel-view synthesis ±2m viewpoint shift, nuScenes novel-view geometric consistency |

> [!tip] 效果简介
> - nuScenes validation set video generation (no first-frame guidance) 上，FVD_multi 74.13 vs 232.85 (MagicDrive) (-158.72)。
> - nuScenes novel-view synthesis ±2m viewpoint shift 上，FVD 64.07 vs 105.29 (DiST-4D) (-41.22)。
> - nuScenes novel-view geometric consistency (OmniScene protocol) 上，SSIM 0.912 vs 0.736 (OmniScene) (+0.176)。

## 概要

### 问题瓶颈

现有驾驶场景生成方法面临一个根本性困境：视频生成模型（如 **MagicDrive** (Gao et al., 2023)、**Panacea** (Wen et al., 2024)）虽能产生多样化的驾驶画面，但缺乏显式的3D几何约束，导致生成结果在不同视角间缺乏一致性，无法自由控制新视角；而重建方法（如 **OmniScene** (Wei et al., 2024)、**OmniRe** (Chen et al., 2024c)）虽然能保证3D一致性，却局限于对已有观测的拟合，不具备生成未曾捕获场景的能力。这一“生成灵活性”与“空间/时间一致性”之间的鸿沟，构成了驾驶世界模型的核心瓶颈。

### 核心思路

**WorldSplat** 提出以**显式4D高斯场景表示**作为中间桥梁，将扩散模型的生成能力与几何一致性统一在一个端到端框架中。其核心洞察是：让扩散模型生成包含RGB、深度和动态分割信息的**多模态隐变量**，再通过一个**前馈Transformer解码器**将这些隐变量直接映射为像素对齐的3D高斯，并聚合为时空一致的4D高斯表示，从而在保持生成多样性的同时，天然具备新视角可控性。最后，引入一个**增强扩散模型**对渲染视频进行质量优化，填补未观测区域并锐化快速运动帧。

### 方法定位

WorldSplat 在方法谱系中位于**视频生成、3D重建与前馈高斯预测**的交叉点：

| 对比维度 | 视频生成方法（MagicDrive/Panacea） | 重建方法（OmniScene/OmniRe） | **WorldSplat（本文）** |
|---------|--------------------------------|---------------------------|----------------------|
| 场景表示 | 2D视频潜变量（隐式3D） | 逐场景优化的3D/4D高斯 | **前馈预测的显式4D高斯** |
| 3D一致性 | 弱（缺乏显式几何约束） | 强（但仅限已观测场景） | **强（生成场景也具备）** |
| 新视角可控性 | 无 | 有限（依赖已有观测） | **有（支持±4m轨迹偏移）** |
| 生成灵活性 | 高 | 无（仅重建） | **高（从条件直接生成）** |
| 扩散采样效率 | DDPM多步（>30步） | — | **Rectified Flow仅8步** |

与最相关的前馈重建方法 **OmniScene** 相比，WorldSplat 的关键差异在于：（1）不依赖真实RGB输入，从条件信号直接生成；（2）生成的是4D动态场景而非静态3D；（3）输出为显式高斯表示，可自由渲染新视角。

### 主要结果

在 nuScenes 验证集上，WorldSplat 在多项核心指标上取得显著提升：

- **视频生成质量**：FVD 降至 **74.13**，较 MagicDrive 的 232.85 降低 158.72（↓68.2%），无需首帧引导即可生成高质量多视角驾驶视频。
- **新视角合成**：在 ±2m 视角偏移下，FVD 为 **64.07**，显著优于 **DiST-4D** (Guo et al., 2025) 的 105.29（↓39.1%）。
- **几何一致性**：遵循 OmniScene 评估协议，SSIM 达 **0.912**，远超 OmniScene 的 0.736（+23.9%）；LPIPS 降至 **0.147**，低于其 0.237（↓38.0%）。

消融实验揭示了各模块的因果贡献：引入3D高斯显式表示使 FVD 从 260.07 骤降至 75.26（−184.81）；聚合为统一4D表示进一步降至 50.73（−24.53）；增强扩散模型与条件重投影各自带来额外增益。这些结果表明，显式4D高斯表示是弥合生成与几何一致性鸿沟的关键因果杠杆。

### 局限与开放问题

尽管整体性能优异，WorldSplat 仍存在以下局限：（1）对于严重未观测区域和大视角偏移，增强扩散模型虽能部分修复，渲染质量仍可能下降；（2）当前框架依赖布局、3D框等结构化条件，尚未探索纯文本驱动的4D场景生成；（3）当自车轨迹进入完全未访问区域（如建筑内部）时，模型的泛化能力有待验证。

自动驾驶世界模型的终极目标是生成时空一致、多视角可控的驾驶场景视频，以支持感知模型的训练与闭环仿真。然而，现有方法在该目标上陷入一种结构性两难：**生成方法**具有想象力和灵活性，却缺乏三维几何一致性；**重建方法**天然保持几何一致，却只能复现已观测场景，无法生成未见过的驾驶情境。

具体而言，以 **MagicDrive**（Gao et al., 2023）和 **Panacea**（Wen et al., 2024）为代表的视频生成模型，将场景隐式编码为 2D 潜在变量，通过扩散模型生成多帧视频。这类方法能够根据布局、文本等条件“想象”出多样化的驾驶画面，但由于缺乏显式的三维场景表示，生成结果在不同视角之间缺乏几何一致性，新视角合成能力极为有限——当自车轨迹发生横向偏移时，渲染质量急剧下降。

另一条技术路线以 **OmniRe**（Chen et al., 2024c）和 **OmniScene**（Wei et al., 2024）为典型，采用基于高斯泼溅（3D Gaussian Splatting）的显式场景重建，能够从多视角输入中恢复出高保真、几何一致的三维场景表示。然而，这类重建方法本质上是“后向”的——它们只能拟合已捕获的传感器数据，无法生成从未观测过的场景内容，不具备生成模型的想象能力。

这种**生成灵活性与三维一致性之间的根本矛盾**，构成了当前驾驶世界模型的核心瓶颈：视频生成模型能“想象”但不懂几何，重建方法懂几何但不会“想象”。现有工作试图通过“先生成视频、再重建场景”的两阶段流程弥合这一鸿沟，但这种串行方案不仅效率低下，且两阶段之间的误差累积难以避免，无法实现端到端的联合优化。

**WorldSplat** 的动机正是打破这一两难困境。其核心洞察是：如果在生成过程中引入**显式的 4D 高斯场景表示**作为中间桥梁，就有可能让扩散模型在保持生成灵活性的同时，获得三维几何的硬约束。具体而言，该方法让扩散模型直接生成包含 RGB、深度和动态分割信息的**多模态潜在变量**，再通过一个前馈 Transformer 解码器将其转化为像素对齐的 3D 高斯，并聚合成统一的 4D 时空场景表示。这一设计使生成过程天然具备三维一致性，同时保留了扩散模型的想象能力，从而在单一框架内同时实现“生成”与“几何一致”这两个曾被视为此消彼长的目标。

## 核心方法与创新机理

WorldSplat 的核心创新在于通过**显式 4D 高斯场景表示**作为中间桥梁，从根本上统一了驾驶场景的生成灵活性与时空一致性。传统方法面临两难困境：视频生成模型（如 MagicDrive、Panacea）虽能想象新场景，但缺乏 3D 一致性和新视角可控性；而重建方法（如 OmniRe、OmniScene）虽保证几何一致性，却无法生成未曾捕获的场景。WorldSplat 通过以下五个关键设计突破这一瓶颈：

### 1. 显式 4D 高斯场景表示

这是最根本的架构创新。不同于以往方法在 2D 视频潜变量空间中隐式建模场景，WorldSplat 引入显式的 4D 高斯表示作为生成与渲染之间的中间层。消融实验（Table 3）提供了决定性证据：引入单帧 3D 高斯表示使 FVD 从 260.07 骤降至 75.26（−184.81），FID 从 41.40 降至 16.31（−25.09）；进一步将多帧 3D 高斯聚合为统一的 4D 表示，FVD 再降至 50.73（−24.53），FID 降至 11.60（−4.71）。这一因果链条清晰表明，显式 4D 表示是性能飞跃的核心驱动因素。

### 2. 端到端统一生成框架

传统方法采用“先视频生成、后重建”的两阶段流程，生成与 3D 一致性相互割裂。WorldSplat 将二者统一为端到端框架：4D 感知的潜在扩散模型直接生成包含 RGB、深度和动态分割信息的**多模态隐变量**，经前馈 Transformer 解码器转化为像素对齐的 3D 高斯，再通过动静分离聚合成 4D 场景。多模态隐变量的通道拼接形式为：

$$\mathbf{L} = concat\{\mathbf{L}_{\mathrm{img}}, \mathbf{L}_{\mathrm{depth}}, \mathbf{L}_{\mathrm{seg}}\}$$

解码器的映射关系为：

$$D_{\phi} : (\mathbf{L}_{\mathrm{img}}, \mathbf{L}_{\mathrm{depth}}, \mathbf{L}_{\mathrm{seg}}, \mathbf{P}) \mapsto \{ (\mathbf{G}_t, \mathbf{M}_t) \in \mathbb{R}^{V \times H \times W \times (14, 1)} \}_{t=1}^T$$

其中 $\mathbf{P}$ 为 Plücker 射线坐标，$\mathbf{G}_t$ 为高斯参数，$\mathbf{M}_t$ 为动态掩码。

### 3. 多模态条件与条件重投影

WorldSplat 的条件输入从传统 2D 信号（文本、布局、边界框）扩展为多模态条件组合：道路草图、文本描述、3D 边界框和自车轨迹。在推理阶段，**条件重投影**（Condition Reprojection）机制将草图和边界框重投影到新视角，施加显式的 3D 几何约束，进一步提升了新视角合成的质量（Table 3 消融实验证实该模块带来额外增益）。

### 4. Rectified Flow 高效采样

将传统 DDPM 的多步采样（>30 步）替换为 **Rectified Flow**，仅需 8 步即可完成采样。其核心公式为：

$$z(s) = (1 - s) \epsilon + s x$$

训练损失为：

$$\mathcal{L}(\psi) = \mathbb{E}_{\mathbf{x}, \epsilon, s} \Big| \Big| g_{\psi}(z(s), s, \mathcal{C}) - (\mathbf{x} - \epsilon) \Big| \Big|_2^2$$

推理时采用离散反向步进：

$$z(s_{k-1}) = z(s_k) - \frac{1}{N} g_{\psi}(z(s_k), s_k, \mathcal{C})$$

这一设计显著降低了推理延迟，使 WorldSplat 在效率对比（Table 7）中展现出明显优势。

### 5. 增强扩散模型后处理

高斯渲染的新视角视频可能存在未观察区域的缺失内容和高速运动下的模糊帧。WorldSplat 引入**增强扩散模型**（Enhanced Diffusion Model）对渲染视频进行修复和细节增强（Figure 3 展示了该模块对缺失区域的修复和快速运动帧的锐化效果）。消融实验中的“Mixed Aug”策略通过混合不同质量的渲染结果训练增强模型，进一步提升了其鲁棒性。

WorldSplat 构建了一个端到端的生成式 4D 驾驶场景框架，其核心瓶颈在于打破现有方法中“生成灵活性”与“3D 时空一致性”之间的对立——视频生成模型缺乏新视角可控性，而重建方法则无法想象未曾捕获的场景。该框架通过引入**显式 4D 高斯场景表示**作为中间桥梁，使扩散模型生成包含 RGB、深度和动态分割信息的**多模态隐变量**，再经由前馈解码器直接预测像素对齐的 3D 高斯并聚合成 4D 场景，从而同时实现生成多样性与空间/时间一致性。

### 整体流程

框架由四个核心模块串联构成（图 2），形成“生成—解码—聚合—增强”的完整管线：

1. **4D 感知潜在扩散模型 (4D-Aware Latent Diffusion Model)**  
   根据多模态条件（道路草图、文本、3D 边界框、自车轨迹）生成包含 RGB、深度和动态分割信息的时空一致潜在表示。该模块采用基于 Rectified Flow 的扩散 Transformer，仅需 8 步采样即可完成去噪，显著提升推理效率。

2. **潜在 4D 高斯解码器 (Latent 4D Gaussian Decoder)**  
   从前一步生成的多模态潜在向量中，通过前馈 Transformer 解码器直接预测像素对齐的 3D 高斯参数，并输出动态掩码以区分静态背景与动态物体。解码器输入为通道拼接的多模态隐变量 $\mathbf{L} = \text{concat}\{\mathbf{L}_{\text{img}}, \mathbf{L}_{\text{depth}}, \mathbf{L}_{\text{seg}}\}$ 与 Plücker 射线坐标 $\mathbf{P}$，输出为每帧的高斯参数和动态掩码：
   $$D_{\phi} : (\mathbf{L}_{\text{img}}, \mathbf{L}_{\text{depth}}, \mathbf{L}_{\text{seg}}, \mathbf{P}) \mapsto \{ (\mathbf{G}_t, \mathbf{M}_t) \}_{t=1}^T$$

3. **4D 高斯聚合 (4D Gaussians Aggregation)**  
   将各帧的 3D 高斯通过动静分离策略融合为统一的时空表示：当前帧的动态高斯与所有帧的静态高斯合并，形成可渲染任意新视角的 4D 场景：
   $$\mathcal{G}_{4D} = \big\{ \big( \mathbf{G}_t \odot \mathbf{M}_t \big) \cup \bigcup_{i=1}^T \big( \mathbf{G}_i \odot (1 - \mathbf{M}_i) \big) \big\}_{t=1}^T$$

4. **增强扩散模型 (Enhanced Diffusion Model)**  
   对 4D 高斯渲染的新视角视频进行质量增强，修复因视角偏移导致的未观察区域缺失和高速运动模糊等退化问题（图 3）。该模块以原始条件输入和渲染视频为条件，对输出视频进行细节增强和时序一致性优化。

### 推理时的条件重投影

在推理阶段，框架引入**条件重投影 (Condition Reprojection)** 机制：将草图与边界框等 2D 条件根据目标视角重投影，施加显式 3D 几何约束，进一步提升新视角合成的几何一致性。消融实验证实该机制能有效增强性能（Table 3）。

### 训练目标

解码器的训练损失为多任务加权和，包含重建损失、感知损失 (LPIPS)、深度损失和分割损失：
$$\mathcal{L} = \mathcal{L}_{\text{recon}} + \lambda_{1} \mathcal{L}_{\text{lpips}} + \lambda_{2} \mathcal{L}_{\text{depth}} + \lambda_{3} \mathcal{L}_{\text{seg}}$$

整体框架实现了从条件输入到高质量多轨迹新视角驾驶视频的端到端生成，无需首帧 RGB 引导即可完成场景想象与时空一致渲染。

![[assets/figures/papers/paper_list_l11_https_openreview_net_forum_id_KWeX6tYno6/figures/002_Figure_2.jpg]]
*Figure 2: The overview of our framework. (1) Employing a 4D-aware diffusion model to generate a multi-modal latent containing RGB, depth, and dynamic information. (2) Predicting pixel-aligned 3D Gaussians from the denoised latent using our feed-forward latent decoder. (3) Aggregating the 3D Gaussians with dynamic-static decomposition to form 4D Gaussians and rendering novel-view videos. (4) Improving the spatial resolution and temporal consistency of the rendered videos with an enhanced diffusion model. "E" and "D" denote the VAE encoder and decoder, respectively. The ↑ arrow and the ↑ ones denote the train-only and inference*

WorldSplat 框架由三个关键模块串联构成：**4D 感知潜在扩散模型**、**潜在 4D 高斯解码器**和**增强扩散模型**（Figure 2）。前两个模块完成从条件信号到显式 4D 场景表示的生成，第三个模块对渲染视频进行质量后处理。

### 4D 感知潜在扩散模型

该模块以多模态条件 $\mathcal{C}$（道路草图、文本、3D 框、自车轨迹）为输入，生成包含 RGB、深度和动态分割信息的时空一致潜在变量。模型基于 OpenSora-VAE-1.2 预训练主干，扩展为**双分支扩散 Transformer**：主 DiT 流处理时空视频潜在变量 $\mathbf{L}$，多块 ControlNet 分支处理条件 $\mathcal{C}$。为确保多视角一致性，标准自注意力被替换为**跨视角注意力**。

采样过程采用 **Rectified Flow** 替代传统 DDPM，推理仅需 8 步。其核心公式为：

**插值状态定义**：
$$z(s) = (1 - s) \epsilon + s x$$
其中 $\epsilon \sim \mathcal{N}(0, I)$ 为噪声，$x$ 为干净潜在变量，$s \in [0, 1]$ 为混合参数。

**训练损失**：
$$\mathcal{L}(\psi) = \mathbb{E}_{\mathbf{x}, \epsilon, s} \Big| \Big| g_{\psi}(z(s), s, \mathcal{C}) - (\mathbf{x} - \epsilon) \Big| \Big|_2^2$$
神经网络 $g_{\psi}$ 学习预测目标向量 $x - \epsilon$，即从噪声指向干净样本的方向。

**推理步进**：
$$z(s_{k-1}) = z(s_k) - \frac{1}{N} g_{\psi}(z(s_k), s_k, \mathcal{C})$$
其中 $N$ 为总步数（8），$s_k = k/N$ 为离散时间步。此公式定义了从噪声逐步逼近干净潜在变量的反向采样过程。

生成的多模态潜在变量通过通道拼接形成解码器输入：
$$\mathbf{L} = concat\{\mathbf{L}_{\mathrm{img}}, \mathbf{L}_{\mathrm{depth}}, \mathbf{L}_{\mathrm{seg}}\}$$

### 潜在 4D 高斯解码器

解码器 $D_{\phi}$ 将多模态潜在变量 $\mathbf{L}$ 和 Plücker 射线坐标 $\mathbf{P}$ 映射为逐帧的像素对齐 3D 高斯参数及动态掩码：
$$D_{\phi} : (\mathbf{L}_{\mathrm{img}}, \mathbf{L}_{\mathrm{depth}}, \mathbf{L}_{\mathrm{seg}}, \mathbf{P}) \mapsto \{ (\mathbf{G}_t, \mathbf{M}_t) \in \mathbb{R}^{V \times H \times W \times (14, 1)} \}_{t=1}^T$$
其中 $\mathbf{G}_t$ 为第 $t$ 帧的 14 维高斯参数（位置、协方差、颜色、不透明度等），$\mathbf{M}_t$ 为单通道动态掩码，$V$ 为视角数，$T$ 为帧数。

解码器架构包含**跨视角注意力**和**时序注意力**模块（Figure 2），以捕获 4D 场景的时空动态。

### 4D 高斯聚合

各帧 3D 高斯通过动静分解融合为统一 4D 表示：
$$\mathcal{G}_{4D} = \big\{ \big( \mathbf{G}_t \odot \mathbf{M}_t \big) \cup \bigcup_{i=1}^T \big( \mathbf{G}_i \odot (1 - \mathbf{M}_i) \big) \big\}_{t=1}^T$$
该公式将当前帧动态高斯（$\mathbf{G}_t \odot \mathbf{M}_t$）与所有帧的静态高斯（$\bigcup_{i=1}^T \mathbf{G}_i \odot (1 - \mathbf{M}_i)$）融合。动态物体在各帧独立建模，静态背景则跨帧共享，从而在变换自车轨迹时保持场景几何一致性。

### 解码器训练损失

解码器训练目标为多项损失的加权和：
$$\mathcal{L} = \mathcal{L}_{\mathrm{recon}} + \lambda_{1} \mathcal{L}_{\mathrm{lpips}} + \lambda_{2} \mathcal{L}_{\mathrm{depth}} + \lambda_{3} \mathcal{L}_{\mathrm{seg}}$$
其中 $\mathcal{L}_{\mathrm{recon}}$ 为像素级重建损失，$\mathcal{L}_{\mathrm{lpips}}$ 为感知损失，$\mathcal{L}_{\mathrm{depth}}$ 和 $\mathcal{L}_{\mathrm{seg}}$ 分别为深度和动态分割的监督损失。

### 增强扩散模型

高斯渲染的新视角视频可能存在未观察区域的缺失内容和快速运动导致的模糊（Figure 3）。增强扩散模型以原始条件 $\mathcal{C}$ 和渲染视频为输入，对渲染结果进行修复和细节增强。消融实验（Table 3）中 **Mixed Aug** 策略通过混合不同质量的渲染样本训练该模型，提升了其鲁棒性。

![[assets/figures/papers/paper_list_l11_https_openreview_net_forum_id_KWeX6tYno6/figures/014_Figure_7.jpg]]
*Figure 7: Visualizations of our Gaussians representation*

## 实验与关键发现

### 实验设置

实验基于 **nuScenes** 数据集，包含 1000 个驾驶场景，其中 700 个用于训练，150 个用于验证。评估指标采用 **FVD**（Fréchet Video Distance）和 **FID**（Fréchet Inception Distance）衡量生成质量，同时使用 **SSIM** 和 **LPIPS** 评估几何一致性与多视角连贯性。模型以预训练的 OpenSora-VAE-1.2 为骨干，仅对扩散 Transformer 中的跨视角注意力模块进行微调。扩散采样采用 Rectified Flow，推理仅需 **8 步**，大幅提升了效率。

### 视频生成主结果

Table 1 展示了在 nuScenes 验证集上的视频生成对比。在不使用首帧引导的条件下，WorldSplat 取得了 **FVD_multi 74.13** 和 **FID_multi 8.78**，显著优于 **MagicDrive**（Gao et al., 2023）的 232.85 和 **Panacea**（Wen et al., 2024）的 139.26。在首帧引导设置下，性能进一步提升至 **FVD 16.57** 和 **FID 4.14**。定性对比（Figure 4）显示，WorldSplat 在细节保真度和时序一致性上均有明显优势，尤其在红框标注的关键区域改善最为显著。

![[assets/figures/papers/paper_list_l11_https_openreview_net_forum_id_KWeX6tYno6/figures/004_Table_1.jpg]]
*Table 1: Video generation comparison on the nuScenes (Caesar et al., 2020) validation set, with green and blue highlighting the best and second-best values, respectively*

![[assets/figures/papers/paper_list_l11_https_openreview_net_forum_id_KWeX6tYno6/figures/005_Figure_4.jpg]]
*Figure 4: Comparison with MagicDrive (Gao et al., 2023) and Panacea (Wen et al., 2024). The top row shows real frames, the second row the corresponding sketches and bounding-box controls. Red boxes highlight areas where our method achieves the most notable improvements*

### 新视角合成主结果

Table 2 报告了在不同视角偏移下的新视角合成性能。在 ±2m 偏移下，WorldSplat 的 **FVD 为 64.07**，显著优于 **DiST-4D**（Guo et al., 2025）的 105.29（Δ = −41.22）。在几何一致性评估中（Table 6），遵循 **OmniScene**（Wei et al., 2024）协议，WorldSplat 取得了 **SSIM 0.912** 对比 OmniScene 的 0.736（Δ = +0.176），**LPIPS 0.147** 对比 0.237（Δ = −0.090），表明其生成的新视角在结构保真度和感知质量上均大幅领先。Figure 5 的定性对比进一步验证了 WorldSplat 在处理大视角偏移时对细节和几何结构的保持能力。

![[assets/figures/papers/paper_list_l11_https_openreview_net_forum_id_KWeX6tYno6/figures/006_Table_2.jpg]]
*Table 2: Quantitative results of novel-view synthesis, reporting FID and FVD under viewpoint shifts of ±1, ±2, and ±4 meters. Baseline metrics are taken from DiST-4D (Guo et al., 2025)*

![[assets/figures/papers/paper_list_l11_https_openreview_net_forum_id_KWeX6tYno6/figures/012_Table_6.jpg]]
*Table 6: Geometric consistency and multi-view coherence evaluation. We follow OmniScene’s protocol for novel-view synthesis evaluation*

### 消融实验

Table 3 系统消融了各组件的贡献，揭示了清晰的因果链条：

1. **引入 3D 高斯显式场景表示**：将 FVD 从 260.07 降至 75.26（−184.81），FID 从 41.40 降至 16.31（−25.09），证明了显式 3D 表示对时空一致性的核心作用。
2. **聚合为统一 4D 高斯**：将单帧 3D 高斯融合为 4D 表示后，FVD 进一步从 75.26 降至 50.73（−24.53），FID 从 16.31 降至 11.60（−4.71），验证了多帧信息融合对时序建模的增益。
3. **混合增强策略**：在训练增强扩散模型时混合不同质量的渲染结果，提升了模型的鲁棒性。
4. **条件重投影**：在推理时施加显式 3D 几何约束，进一步提升了生成质量。

最终完整版本（Version F）达到 **FVD 47.41**，相比无任何增强的基线（Version A 的 260.07）提升了 **−212.66**。

### 下游任务验证

Table 4 展示了生成数据在下游感知任务中的有效性。(a) 使用预训练 BEVFormer 评估生成数据的域差距，结果表明生成数据与真实数据的分布高度一致；(b) 将生成数据加入 StreamPETR 训练后，感知性能获得稳定提升，验证了 WorldSplat 生成的数据可作为有效的训练增强资源。

### 推理效率

Table 7 对比了不同方法的推理效率。WorldSplat 在单张 GPU 上完成新场景生成，显存占用和推理时间均优于 **MagicDrive-V2**（Gao et al., 2025）和 **Cosmos-transfer1**（Alhaija et al., 2025）等方案，体现了前馈式架构的效率优势。

### 失败模式与局限性

尽管增强扩散模型能修复部分渲染伪影，对于**严重未观察区域**和**大视角偏移**（如 ±4m），渲染质量仍可能下降。Figure 3 展示了增强扩散模型在填补缺失内容和锐化快速运动帧方面的效果，但当自车轨迹进入完全未访问区域时，模型缺乏足够的先验信息进行合理补全。此外，当前框架依赖布局和 3D 框等条件输入，尚未支持纯文本驱动的 4D 场景生成。

## 定位与知识库关联

### 1. 核心瓶颈与动机

现有驾驶场景生成方法面临一个根本性困境：**视频生成模型**（如 **MagicDrive** (Gao et al., 2023)、**Panacea** (Wen et al., 2024)）虽能产生多样化的视觉内容，但缺乏显式3D几何约束，导致生成结果在新视角下缺乏空间一致性和可控性；而**场景重建方法**（如 **OmniRe** (Chen et al., 2024c)、**OmniScene** (Wei et al., 2024)）虽能保证3D一致性，却无法“想象”未曾捕获的场景，不具备生成能力。WorldSplat 的核心动机正是打破这一僵局，构建一个同时具备生成灵活性与时空一致性的统一框架。

### 2. 方法谱系定位

WorldSplat 的方法设计可视为对以下三条技术路线的交叉融合与改进：

| 技术维度 | 基准方法 | WorldSplat 的改进 |
|---------|---------|------------------|
| **场景表示** | 2D视频潜变量（隐式3D），如 MagicDrive、Panacea | 显式4D高斯表示，通过前馈解码器从多模态潜变量直接预测像素对齐的3D高斯 |
| **生成与3D一致性结合** | 先视频生成后重建的两阶段流程 | 端到端统一框架：扩散模型直接生成多模态潜变量并解码为4D高斯 |
| **条件类型** | 仅2D信号（文本、布局、框） | 多模态条件（道路草图、文本、3D框、自车轨迹），并引入条件重投影施加显式3D几何约束 |
| **扩散模型采样** | DDPM多步采样（>30步） | Rectified Flow仅需8步采样，大幅提升推理效率 |
| **渲染后处理** | 直接使用高斯渲染输出 | 增强扩散模型对渲染视频进行修复和细节增强 |

**具体对比分析：**

- **相对于 MagicDrive / Panacea（视频生成线）**：WorldSplat 的核心突破在于用显式4D高斯替代隐式潜变量作为场景表示。消融实验（Table 3）提供了决定性证据：引入3D高斯使FVD从260.07骤降至75.26（−184.81），FID从41.40降至16.31（−25.09）；进一步聚合为4D表示后，FVD再降至50.73（−24.53），FID降至11.60（−4.71）。这表明显式场景表示是性能飞跃的关键因果杠杆。

- **相对于 DiST-4D（新视角合成线）**：在±2m视角偏移下，WorldSplat的FVD为64.07，显著优于DiST-4D的105.29（Table 2），展现了前馈式4D高斯生成在可控新视角合成上的优势。

- **相对于 OmniScene（前馈3D重建线）**：在几何一致性评估中，WorldSplat的SSIM达0.912，远超OmniScene的0.736；LPIPS为0.147，低于其0.237（Table 6），验证了生成框架在保持3D几何精度上的有效性。

### 3. 关键创新与知识库贡献

WorldSplat 向知识库贡献了以下可复用的设计模式：

1. **多模态潜变量桥接**：扩散模型生成的潜变量同时编码RGB、深度和动态分割信息（$\mathbf{L} = concat\{\mathbf{L}_{\mathrm{img}}, \mathbf{L}_{\mathrm{depth}}, \mathbf{L}_{\mathrm{seg}}\}$），为前馈解码器提供丰富的3D感知先验。这一设计将2D扩散模型的生成能力与3D重建的几何约束解耦又耦合。

2. **动静分离的4D高斯聚合**：通过动态掩码$\mathbf{M}_t$将每帧高斯分解为动态前景与静态背景，再跨帧融合（Eq. 5: $\mathcal{G}_{4D} = \{ (\mathbf{G}_t \odot \mathbf{M}_t) \cup \bigcup_{i=1}^T (\mathbf{G}_i \odot (1 - \mathbf{M}_i)) \}_{t=1}^T$），既保留了动态物体的时间连续性，又避免了静态区域的冗余复制。

3. **增强扩散模型作为后处理**：针对高斯渲染在未观察区域和快速运动场景中的退化问题，引入条件增强扩散模型进行修复和锐化（Figure 3），形成“生成-渲染-增强”的级联优化管线。

4. **条件重投影机制**：推理时将草图/边界框重投影以施加显式3D几何约束，进一步提升了新视角合成的几何一致性。

### 4. 适用边界与局限

尽管WorldSplat在nuScenes数据集上展现了显著优势，其方法存在以下适用边界：

- **严重未观察区域的退化**：当自车轨迹偏移较大或进入完全未访问区域（如建筑内部）时，高斯渲染仍可能产生缺失内容和伪影。增强扩散模型虽能部分修复，但无法从根本上解决信息缺失问题。
- **条件依赖**：当前框架依赖道路草图、3D框等结构化条件进行控制，尚未验证在纯粹文本驱动下的4D场景生成能力。
- **场景泛化性**：所有实验均在nuScenes数据集上进行（700场景训练，150场景验证），对跨数据集、跨城市、跨天气条件的泛化能力尚待验证。
- **实时性限制**：尽管采用了8步Rectified Flow采样，整体管线包含扩散生成、高斯解码、渲染和增强四个阶段，推理效率对比（Table 7）显示其仍慢于纯视频生成方法，需进一步优化以满足在线应用需求。

### 5. 开放问题

1. **纯文本驱动的4D场景生成**：如何在不依赖布局/框条件下，仅通过自然语言描述生成时空一致的4D驾驶场景？
2. **极端视角偏移的几何补全**：当自车轨迹进入完全未观察区域时，如何利用语义先验或世界模型进行合理的几何与外观外推？
3. **跨域泛化与规模化**：该方法能否扩展到更大规模、更多样化的驾驶数据集？对传感器配置和天气变化的鲁棒性如何？
4. **闭环仿真中的物理合理性**：生成的4D高斯表示是否能直接用于物理引擎中的碰撞检测和动力学仿真？动静分离的精度是否满足安全关键应用的需求？

**注意**：以上开放问题基于论文自身讨论的局限性和方法设计边界推导，部分结论（如跨域泛化性）需通过后续实验进行验证。

## 原文 PDF

![[paperPDFs/ICLR_2026/WorldSplat_Gaussian_Centric_Feed_Forward_4D_Scene_Generation_for_Autonomous_Driv_f29223160c30.pdf]]
