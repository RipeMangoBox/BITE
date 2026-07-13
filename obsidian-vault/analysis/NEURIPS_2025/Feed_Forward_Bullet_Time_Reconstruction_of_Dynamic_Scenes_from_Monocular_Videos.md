---
title: "Feed-Forward Bullet-Time Reconstruction of Dynamic Scenes from Monocular Videos"
type: paper
paper_level: A
venue: NeurIPS
year: 2025
pdf_ref: paperPDFs/NEURIPS_2025/Feed_Forward_Bullet_Time_Reconstruction_of_Dynamic_Scenes_from_Monocular_Videos.pdf
project_link: https://research.nvidia.com/labs/toronto-ai/bullet-timer/
code_link: null
aliases:
- BB
- FFBTRDSFMV
tags:
- NEURIPS_2025
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
core_operator: "向每个上下文帧中添加可共享的“子弹时间戳嵌入”（bullet-time embedding），将动态重建任务转化为从多帧上下文预测某一特定时间戳的完整3DGS表示，使得模型能够以统一方式处理静态和动态场景。"
primary_logic: "通过子弹时间公式将动态场景重建重新表述为一个时间条件生成问题，该公式天然兼容静态数据，从而能够利用大规模静态多视图数据集进行预训练，学习强有力的运动感知几何先验。"
claims:
- "BTimer是首个运动感知的前馈式动态场景重建与实时新视角合成模型。"
- "BTimer在NVIDIA Dynamic Scene数据集上以0.78s重建时间实现25.82 PSNR，速度比优化方法快数个数量级且质量有竞争力。"
- "课程学习（静态预训练+动态联合训练）对模型最终性能至关重要，移除静态预训练或联合训练会严重退化。"
- "DyCheck iPhone dataset 上 PSNR↑ / SSIM↑ / LPIPS↓ / Rec. Time = 16.52 / 0.570 / 0.338 / 0.98s"
---

# Feed-Forward Bullet-Time Reconstruction of Dynamic Scenes from Monocular Videos

> [!tip] 核心洞察
> 通过子弹时间公式将动态场景重建重新表述为一个时间条件生成问题，该公式天然兼容静态数据，从而能够利用大规模静态多视图数据集进行预训练，学习强有力的运动感知几何先验。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 基于单目视频的前馈式动感场景子弹时间重建 |
| 英文题名 | Feed-Forward Bullet-Time Reconstruction of Dynamic Scenes from Monocular Videos |
| 会议/期刊 | NeurIPS 2025 |
| Links | [paper](https://arxiv.org/abs/2412.03526) · [Project](https://research.nvidia.com/labs/toronto-ai/bullet-timer/) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction |
| Method | BTimer (BulletTimer) |
| Dataset | DyCheck iPhone dataset, NVIDIA Dynamic Scene dataset, RE10K (static scene benchmark), Tanks & Temples (OOD static benchmark) |

> [!tip] 效果简介
> - DyCheck iPhone dataset 上，PSNR↑ / SSIM↑ / LPIPS↓ / Rec. Time 为 16.52 / 0.570 / 0.338 / 0.98s，对比 HyperNeRF: 16.81 / 0.569 / 0.332 / 72h，变化 PSNR -0.29, 但速度快 264,000 倍。
> - NVIDIA Dynamic Scene dataset 上，PSNR↑ / LPIPS↓ / Render FPS / Rec. Time 为 25.82 / 0.086 / 115 / 0.78s，对比 Casual-FVS: 24.57 / 0.081 / 48 / 0.25h，变化 +1.25 dB PSNR, 速度提升约 1150 倍。
> - RE10K (static scene benchmark) 上，LPIPS↓ 为 0.070 (Ours-Static)，对比 GS-LRM: 0.114; MVSplat: 0.128，变化 LPIPS 相对最佳基线降低 39%。

## 概要

### 问题背景

从单目视频中重建动态场景并实现自由视点渲染是计算机视觉领域的长期挑战。传统方法通常依赖逐场景的优化过程（如动态NeRF），虽然能产生高质量结果，但重建时间动辄数小时甚至数天，难以满足实时应用需求。近年来兴起的前馈式场景重建模型（如pixelSplat、MVSplat等）虽能在亚秒级时间内从多视图图像直接预测3D高斯泼溅（3DGS）表示，但这些方法**仅适用于静态场景**，无法泛化到包含复杂运动的动态场景——其核心瓶颈在于缺乏有效处理4D时空信息的能力。

### 核心方法

本文提出**BTimer**，首个运动感知的前馈式动态场景重建模型。其核心创新在于**子弹时间公式**：向每个上下文帧中添加可共享的子弹时间戳嵌入，将动态重建任务重新表述为一个时间条件生成问题——给定一段单目视频的若干上下文帧及其相机姿态，直接预测某一指定时间戳下的完整3DGS场景表示。这一公式天然兼容静态数据，使模型能够利用大规模静态多视图数据集进行预训练，从而学习强有力的运动感知几何先验。

为处理输入帧集合中不存在的时间戳，BTimer引入了**Novel Time Enhancer（NTE）模块**，通过先预测目标时间戳的RGB帧再送入主模型进行3DGS重建，有效缓解了快速或复杂运动场景中的重影伪影。训练采用三阶段课程学习策略：低分辨率到高分辨率的静态场景预训练 → 动态数据联合训练 → 长上下文窗口微调。

### 主要结果

BTimer在动态场景基准上展现出**速度与质量的显著突破**：
- 在NVIDIA Dynamic Scene数据集上，以**0.78秒**重建时间达到25.82 PSNR，比优化方法Casual-FVS快约1150倍且质量更优（+1.25 dB）；
- 在DyCheck iPhone数据集上，以**0.98秒**重建时间达到16.52 PSNR，速度比优化方法HyperNeRF快约264,000倍，质量仅差0.29 dB；
- 在静态场景基准RE10K上，LPIPS达到0.070，较最佳前馈基线GS-LRM降低39%，展现出强大的泛化能力。

消融实验证实，课程学习中的静态预训练和动态联合训练对模型性能至关重要，移除任一阶段均会导致几何退化和细节丢失。

### 动态场景重建的核心矛盾：质量与速度的取舍

从单目视频中重建完整的动态3D场景并支持自由视点渲染，是计算机视觉与图形学中长期存在的挑战。这一任务要求模型同时理解场景的几何结构、外观属性以及随时间演化的运动模式，其核心困难在于4D时空信息的复杂性——模型必须在稀疏的观测视角和时间点上，推断出任意新视角和新时刻的完整场景表示。

近年来，以NeRF（Neural Radiance Fields）和3D高斯泼溅（3D Gaussian Splatting, 3DGS）为代表的神经渲染技术，在静态场景重建上取得了显著进展。然而，当这些方法被扩展到动态场景时，一个根本性的矛盾浮现出来：**优化类方法**（如**HyperNeRF** (Park et al., CVPR 2021)、**DynNeRF** (Gao et al., ICCV 2021)、**4D-GS** (Wu et al., CVPR 2024) 等）通过对每个场景进行长时间的逐场景优化，能够获得较高的渲染质量，但重建时间通常以小时甚至天计，完全无法满足实时应用的需求。相反，**前馈式方法**（feed-forward models）通过在大规模数据上预训练，仅需单次前向传播即可完成重建，速度极快（毫秒级），但其能力长期局限于静态场景——现有前馈模型无法泛化到包含复杂运动的动态场景，缺乏有效处理4D时空信息的能力。

这一缺口在Figure 1的速度-质量对比中得到了直观呈现：优化方法聚集在高PSNR区域但速度极慢，而BTimer以0.78秒的重建时间达到了25.82 PSNR，在保持竞争性质量的同时实现了数量级的速度飞跃。

### 现有动态场景方法的瓶颈

当前动态场景重建方法可大致分为三类，各自存在显著局限：

1. **逐场景优化的动态NeRF/3DGS方法**：以**TiNeuVox** (Fang et al., SIGGRAPH Asia 2022)、**NSFF** (Li et al., CVPR 2022)、**RoDynRF** (Liu et al., CVPR 2023) 等为代表。这些方法通过引入时间维度的变形场或时空特征网格来建模运动，但需要针对每个视频序列进行数小时的重建优化，计算代价高昂。**HyperNeRF**在DyCheck iPhone数据集上达到16.81 PSNR，但重建耗时72小时——这种速度在实际应用中几乎不可用。

2. **前馈式静态重建方法**：如PixelSplat、MVSplat、GS-LRM等，通过Transformer直接从多视图图像回归3DGS参数，实现了毫秒级重建。然而，这些模型的设计假设场景是静态的，当输入包含运动物体或动态变化时，模型无法区分不同时刻的观测差异，导致几何混乱和重影伪影。**核心瓶颈在于：这些模型没有时间感知能力，无法将不同时间戳的观测信息正确地融合到统一的场景表示中。**

3. **混合方法**：**Casual-FVS** (Lee et al., 2023) 通过深度估计和变形实现较快的动态视图合成（约0.25小时），但仍远未达到实时；**PGDVS** (Zhao et al., ICLR 2024) 依赖视频一致的深度估计作为额外输入，增加了系统复杂度和误差传播风险。

上述方法的共同缺陷揭示了动态场景前馈重建的根本难题：**如何设计一个统一的时间条件机制，使模型能够以计算高效的方式处理任意时间戳的场景状态，同时保持对静态场景的兼容性？**

### 本文动机：子弹时间公式与运动感知先验

BTimer的核心洞察在于将动态场景重建重新表述为一个**时间条件生成问题**。给定一段单目视频及其相机姿态和时间戳，模型的目标是预测任意指定“子弹时间戳”（bullet timestamp）下的完整3DGS场景表示。这一形式化带来了两个关键优势：

1. **天然兼容静态数据**：当所有输入帧共享同一时间戳时（即静态场景），子弹时间公式退化为标准的多视图重建问题。这意味着模型可以利用大规模静态多视图数据集（如RE10K、DL3DV等）进行预训练，从中学习强有力的运动感知几何先验——这是纯动态数据集无法提供的。

2. **统一处理静态与动态**：通过在上下文帧中注入可共享的**子弹时间戳嵌入**（bullet-time embedding），模型学会根据目标时间戳聚合来自不同时刻的观测信息。这一机制将动态重建从“如何建模运动”转化为“如何从多时刻观测中预测特定时刻的完整场景”，避免了显式运动估计的复杂性。

基于这一公式，BTimer成为**首个运动感知的前馈式动态场景重建模型**，能够在150ms内（12帧256×256分辨率）完成子弹时间重建，同时保持与优化方法可竞争的质量。这种速度优势源于其纯前馈的设计——重建过程仅需一次Transformer前向传播和后续的3DGS光栅化渲染，无需任何逐场景的迭代优化。

## 核心方法与创新机理

BTimer的核心创新在于将动态场景的前馈式重建重新定义为一个**时间条件生成问题**，并通过三个关键设计（changed slots）突破现有前馈模型无法处理复杂运动的瓶颈。

### 1. 子弹时间戳嵌入：从多视图几何到时空感知

现有前馈式场景重建模型（如MVSplat、GS-LRM等）仅依赖多视图几何线索，缺乏处理时态信息的能力。BTimer的关键创新是向每个上下文帧注入**可共享的子弹时间戳嵌入（bullet-time embedding）**。

具体而言，模型接收两个时间信号：上下文帧自身的时间戳 $t_i$ 和目标“子弹”时间戳 $t_b$。两者均通过正弦位置编码（PE）及两层线性层分别编码为 $f_i^{ctx}$ 和 $f_i^{bullet}$，然后相加形成最终的时间特征 $f_i^{time} = f_i^{ctx} + f_i^{bullet}$。该时间特征与RGB patch嵌入和Plücker相机射线嵌入相加后送入ViT骨干网络（Section 3.1）。

这一设计的因果机制在于：**子弹时间戳嵌入将动态重建任务转化为“给定多帧上下文，预测某一特定时刻的完整3DGS表示”的统一范式**。模型在训练中学习将不同时间戳的观测信息聚合到目标时刻，从而隐式地建模场景运动。由于该公式天然兼容静态场景（所有帧共享同一时间戳），BTimer得以利用大规模静态多视图数据集进行预训练，学习强有力的几何先验——这是后续动态泛化的基础。

### 2. Novel Time Enhancer：中间时刻的运动插值

当目标子弹时间戳 $t_b$ 不在输入上下文帧的时间戳集合 $\mathcal{T}$ 中时，直接由主模型预测未观测时刻的3DGS易产生重影伪影（ghosting artifacts）。BTimer引入**Novel Time Enhancer (NTE)** 模块来解决这一问题。

NTE复用BTimer的ViT架构，但存在两个关键差异：
- 输入上下文token的时间特征仅编码其自身时间戳（即 $f_i^{time} = f_i^{ctx}$）；
- 额外拼接目标token，其包含目标时间戳嵌入和线性插值得到的目标姿态 $\mathbf{P}_b$。

NTE直接预测目标时刻的RGB图像 $\mathbf{I}_b$，该预测帧随后作为“子弹帧”输入主BTimer模型进行3DGS重建（Section 3.2）。消融实验证实，NTE模块显著减少了快速或复杂运动场景中的重影伪影（Section 4.4, Figure 8b）。该设计将困难的时间插值问题分解为“RGB预测 + 3DGS重建”两步，降低了主模型的学习难度。

### 3. 三阶段课程学习：静态预训练驱动的运动感知先验

BTimer的训练策略是其性能的关键使能因素。模型采用三阶段课程学习（Section 3.3）：

1. **Stage 1（静态预训练）**：在混合大规模静态数据集（RE10K、DL3DV等）上以低分辨率到高分辨率的渐进方式进行预训练，学习通用3D几何先验。
2. **Stage 2（动态联合训练）**：在动态数据集上训练的同时继续联合训练静态数据，防止灾难性遗忘。
3. **Stage 3（长上下文微调）**：扩展上下文窗口进行微调，提升对长视频序列的建模能力。

消融实验提供了决定性证据：**移除Stage 1的静态预训练会导致模型产生不正确的几何和模糊细节**；**即使在Stage 2中，若不同时联合训练静态数据，模型也会出现细节丢失和几何退化**（Section 4.4, Figure 6）。这表明静态数据预训练所获得的几何先验是动态场景重建质量的必要条件，而联合训练策略则防止了模型在适应动态数据时遗忘这些先验。

### 创新总结

上述三个changed slots形成了一条因果链：子弹时间戳嵌入提供了处理时态信息的统一框架，使静态数据预训练成为可能；课程学习策略将静态预训练获得的几何先验有效迁移到动态场景；NTE模块则弥补了主模型在未观测时刻的预测能力缺口。三者协同使得BTimer成为首个能够在亚秒级时间内完成动态场景重建与实时新视角合成的前馈式模型。

BTimer 的整体流水线围绕一个核心思想展开：**将动态场景重建重新表述为时间条件生成问题**。给定一段单目视频 $\mathcal{I} = \{ \mathbf{I}_i \in \mathbb{R}^{H \times W \times 3} \}_{i=1}^{N}$、对应的已知相机位姿 $\mathcal{P} = \{ \mathbf{P}_i \in \mathbb{SE}(3) \}_{i=1}^{N}$ 以及时间戳 $\mathcal{T} = \{ t_i \in \mathbb{R} \}_{i=1}^{N}$，模型的目标是从多帧上下文直接预测在任意指定“子弹时间戳” $t_b$ 处的完整 3D 高斯泼溅（3DGS）表示。这一前馈过程仅需单次推理，无需逐场景优化。

### 输入预处理与嵌入

模型首先将每帧上下文图像 $\mathbf{I}_i$ 划分为 $8 \times 8$ 的 patch，并通过线性嵌入层投影为 RGB 特征 $\{f_{ij}^{\text{rgb}}\}$。同时，每帧的相机位姿 $\mathbf{P}_i$ 被编码为 Plücker 坐标嵌入，与 patch 特征相加，使网络获得显式的多视图几何先验。

**时间信息编码**是 BTimer 区别于静态前馈模型的关键设计。对于每个上下文帧，模型分别编码两个时间信号：
- **上下文时间戳** $t_i$：表示该帧在视频中的原始时刻；
- **子弹时间戳** $t_b$：表示期望输出的目标时刻。

两者均通过正弦位置编码（Positional Encoding）后经两层线性层处理，分别得到 $f_i^{\text{ctx}}$ 和 $f_i^{\text{bullet}}$，最终相加形成统一的时间嵌入 $f_i^{\text{time}} = f_i^{\text{ctx}} + f_i^{\text{bullet}}$。这一可共享的“子弹时间戳嵌入”使得模型能够以统一方式处理静态和动态场景——当 $t_b = t_i$ 时，模型退化为标准的多视图重建任务。

### 主干网络与 3DGS 解码

BTimer 采用基于 ViT 的主干网络，包含 24 层自注意力模块，首尾均应用 LayerNorm。每个上下文帧的所有 patch token 被拼接后送入 Transformer，通过自注意力机制在帧内与帧间聚合时空信息。

每个输出 token $f_{ij}^{\text{out}}$ 通过单层线性层解码为 $8 \times 8$ 区域的 12 通道 3DGS 参数 $\mathbf{G}_{ij} \in \mathbb{R}^{8 \times 8 \times 12}$。所有区域的参数合并后即构成目标时刻的完整 3DGS 场景表示，可直接用于可微光栅化渲染。

### Novel Time Enhancer（NTE）模块

当子弹时间戳 $t_b$ 不在输入时间戳集合 $\mathcal{T}$ 中时，直接由主模型预测未观察时刻的 3DGS 容易产生重影伪影。为此，BTimer 引入 NTE 模块（见图 3）作为中间帧合成器。

NTE 复制了 BTimer 的 ViT 架构，但存在两处关键差异：
1. 输入上下文 token 的时间特征仅编码其自身的上下文时间戳（即 $f_i^{\text{time}} = f_i^{\text{ctx}}$）；
2. 额外拼接目标 token，其嵌入由目标子弹时间戳和线性插值得到的目标位姿 $\mathbf{P}_b$ 共同编码。

NTE 直接预测目标时刻的 RGB 图像 $\mathbf{I}_b$，该合成帧随后被送入主 BTimer 模型作为子弹帧，用于重建 $t_b$ 时刻的 3DGS。这一设计显著缓解了快速或复杂运动场景中的重影问题（消融证据见 §4.4）。

### 推理流程

完整视频的子弹时间重建可通过迭代方式高效完成：将 $t_b$ 依次设为视频中的每个时间戳，所有时刻的推理可并行执行。对于 12 帧 $256^2$ 分辨率的输入，单次前馈推理仅需 150 ms；$512^2$ 分辨率下为 1.55 s。整个过程在单张 NVIDIA A100 GPU 上的显存占用低于 10 GB。

### 训练课程

BTimer 采用三阶段课程学习策略（详见 §3.3）：
1. **静态预训练**：在大规模混合静态多视图数据集上进行低分辨率到高分辨率的渐进训练，学习强几何先验；
2. **动态联合训练**：在静态与动态数据上共同训练，使模型适应运动场景；
3. **长上下文微调**：扩展输入帧数窗口，提升对长视频的重建完整性。

消融实验（§4.4）表明，移除静态预训练会导致不正确的几何和模糊细节；在第二阶段中不共同训练静态数据则会造成细节丢失和几何退化。

### 子弹时间重建模型（BTimer）

BTimer 是一个基于 ViT 的前馈式动态场景重建模型，其核心任务是将单目视频的上下文帧集合映射为指定“子弹时间戳”处的完整 3DGS 场景表示。模型由以下关键模块构成：

**ViT 骨干网络**：采用 24 层自注意力 Transformer 作为主干，输入输出两端均施加 LayerNorm。该骨干负责在全部上下文帧的 patch token 之间进行全局信息聚合，使每个输出 token 融合了多帧、多视角的时空特征。

**Patch 与位姿嵌入**：每帧输入图像 $\mathbf{I}_i \in \mathbb{R}^{H \times W \times 3}$ 被划分为 $8 \times 8$ 的 patch，经线性投影得到 RGB 特征 $\{f_{ij}^{\text{rgb}}\}$。同时，每帧的相机位姿 $\mathbf{P}_i \in \mathbb{SE}(3)$ 被编码为 Plücker 坐标嵌入，与 RGB 特征相加，为模型提供显式的多视图几何约束。

**子弹时间戳嵌入**：这是 BTimer 的核心创新。给定上下文帧时间戳 $t_i$ 和目标子弹时间戳 $t_b$，两者分别通过正弦位置编码（PE）和两层线性层得到时间特征 $f_i^{\text{ctx}}$ 与 $f_i^{\text{bullet}}$，最终相加形成统一的时间嵌入 $f_i^{\text{time}}$：

$$f_i^{\text{time}} = f_i^{\text{ctx}} + f_i^{\text{bullet}}$$

该嵌入被叠加到每个上下文帧的 patch 特征上，使得模型在聚合多帧信息时能够明确感知目标输出时间戳，从而将动态重建转化为一个时间条件生成问题。这一设计的因果机制在于：子弹时间公式天然兼容静态场景（此时所有帧的时间戳相同，嵌入退化为常量），使得模型可以无缝利用大规模静态多视图数据集进行预训练，学习运动感知的几何先验。

**3DGS 解码器**：每个输出 token $f_{ij}^{\text{out}}$ 通过单层线性层解码为 $8 \times 8 \times 12$ 的 3D 高斯参数 $G_{ij}$，包含位置、协方差、颜色和不透明度。所有 patch 的高斯参数拼接即构成目标时间戳处的完整场景表示。

### 损失函数

BTimer 的训练采用渲染 RGB 与真实值之间的复合损失：

$$\mathcal{L}_{\text{RGB}} = \mathcal{L}_{\text{MSE}} + \lambda \mathcal{L}_{\text{LPIPS}}, \quad \lambda = 0.5$$

其中 $\mathcal{L}_{\text{MSE}}$ 为逐像素均方误差，$\mathcal{L}_{\text{LPIPS}}$ 为感知损失，权重 $\lambda = 0.5$ 平衡像素级精度与感知相似度。该损失同时施加于目标时间戳渲染和中间时间戳插值渲染，后者作为正则化手段防止模型将 3DGS 放置在相机近处产生白色边缘伪影。

### Novel Time Enhancer（NTE）模块

当目标子弹时间戳 $t_b \notin \mathcal{T}$（即不在输入帧的时间戳集合中）时，直接由主模型预测容易产生重影。NTE 模块专门解决此问题：

NTE 复制 BTimer 的 ViT 架构，但有两个关键差异：其一，输入上下文 token 的时间特征仅编码各自的上下文时间戳（即 $f_i^{\text{time}} = f_i^{\text{ctx}}$）；其二，额外拼接目标 token，其嵌入包含目标时间戳 $t_b$ 和目标位姿 $\mathbf{P}_b$（由邻近帧位姿线性插值得到）。NTE 直接预测 $t_b$ 时刻的 RGB 图像 $\mathbf{I}_b$，该预测帧随后作为“子弹帧”输入主 BTimer 模型进行 3DGS 重建。

NTE 的因果机制在于：将困难的时间插值问题分解为“图像域预测 + 3D 重建”两步，其中图像域预测可利用相邻帧的像素级对应关系，比直接从隐空间预测 3D 高斯更稳定，从而显著减少快速或复杂运动场景中的重影伪影。

### 三阶段课程学习策略

训练策略本身虽非网络模块，但其对模型最终性能具有决定性作用，消融实验证实移除任一部分均会导致严重退化：

- **Stage 1（静态预训练）**：在混合大规模静态多视图数据集上进行低分辨率到高分辨率的渐进式预训练，建立强有力的多视图几何先验。
- **Stage 2（动态联合训练）**：引入动态场景数据，与静态数据共同训练，使模型在保持几何质量的同时学习运动信息。若此阶段移除静态联合训练，会导致细节丢失和几何退化。
- **Stage 3（长上下文微调）**：使用更长的上下文窗口进行微调，提升模型对长序列时空信息的建模能力。

## 实验与关键发现

BTimer在动态与静态场景数据集上均展现出速度与质量的显著优势，其核心实验结论可概括为：**以优化方法数万分之一的重建时间，取得有竞争力的渲染质量；通过课程学习策略和NTE模块，有效解决动态场景中的几何退化和运动重影问题。**

### 主实验结果

#### 动态场景重建

在NVIDIA Dynamic Scene数据集上，BTimer以**0.78秒**的单场景重建时间取得**25.82 PSNR / 0.086 LPIPS**，渲染帧率达**115 FPS**。相比Casual-FVS（24.57 PSNR / 0.25小时重建），PSNR提升1.25 dB，重建速度加快约**1150倍**。值得注意的是，Casual-FVS需要视频一致的深度估计作为额外输入，而BTimer仅使用彩色图像。与4D-GS等显式3DGS基线相比，BTimer在PSNR上领先约5%。

在DyCheck iPhone数据集上，BTimer取得**16.52 PSNR / 0.570 SSIM / 0.338 LPIPS**，重建时间**0.98秒**。虽然PSNR略低于优化方法HyperNeRF（16.81 PSNR），但重建速度快约**264,000倍**（0.98秒 vs. 72小时）。这一速度-质量权衡关系在Figure 1的散点图中清晰呈现：BTimer位于帕累托前沿，在保持竞争性质量的同时实现了数量级的速度跨越。

#### 静态场景泛化能力

BTimer的子弹时间公式天然兼容静态场景，使其能够利用大规模静态多视图数据预训练。在RE10K静态基准上，BTimer-Static取得**0.070 LPIPS**，相比最佳基线GS-LRM（0.114 LPIPS）降低39%，较MVSplat（0.128 LPIPS）降低45%。在分布外Tanks & Temples基准上，混合数据集训练的BTimer-Full取得**0.093 LPIPS**，而仅在单一数据集上训练的基线模型LPIPS范围为0.278-0.668，BTimer将LPIPS降低了**67%-86%**，充分验证了课程学习策略对泛化能力的关键作用。

### 消融实验

消融实验揭示了BTimer中三个关键设计的作用机制：

**课程学习策略**（Figure 6右侧）：移除静态预训练（Stage 1）导致模型产生不正确的几何结构和模糊细节，说明静态数据预训练为模型提供了基础的几何先验。即使在第二阶段联合训练中不共同训练静态数据，也会导致细节丢失和几何退化，表明静态场景的持续监督对维持几何质量至关重要。

**插值监督**：移除插值损失后，模型倾向于在相机附近生成低深度值的3DGS，产生白色边缘伪影。插值监督通过约束模型在未见时间戳上的RGB预测，有效防止了这种深度退化。

**NTE模块**（Figure 8(b)）：对于快速或复杂运动场景，NTE模块显著减少了中间时间戳渲染中的重影伪影。该模块通过先预测中间帧RGB再送入主模型，将运动插值从3DGS生成中解耦，使主模型能够专注于几何重建。

![[assets/figures/papers/paper_list_l3_https_arxiv_org_abs_2412_03526/figures/009_Figure_8.jpg]]
*Figure 8: (a) Illustration of bullet-time reconstruction from multiple context frames. Increased number of frame predictions leads to progressively more complete scene reconstruction on target views. (b) Ablation on the NTE module. The middle frame is in between the $1 ^ { \mathrm { s t } }$ frame and the $\bar { 2 } ^ { \mathrm { n d } }$ frame. Results are rendered from the view of the $1 ^ { \mathrm { s t } }$ frame

### 推理效率

BTimer的推理效率随输入帧数和分辨率灵活缩放：4帧256²分辨率重建仅需**20毫秒**，12帧256²需**150毫秒**，12帧512²需**1.55秒**。模型在单张NVIDIA A100 GPU上显存占用低于10 GB，可部署于消费级显卡。

### 失败模式与局限性

尽管BTimer在整体性能上表现优异，实验揭示了以下失败模式：

1. **远视角合成退化**：模型在渲染远离输入相机轨迹的新视角时质量明显下降，这是前馈式方法的共性挑战，源于训练数据中视角覆盖的有限性。
2. **极快/高度非刚性运动模糊**：虽然NTE模块缓解了复杂运动的重影问题，但对于极快或高度非刚性的运动仍可能产生模糊伪影。
3. **几何精度不足**：渲染的深度图存在漂移或人为结构，几何质量不如专门的深度估计方法精确，这限制了模型在需要精确几何的应用场景中的使用。

这些失败模式指向了未来工作的方向：提升深度图精度以改善远视角合成、显式恢复运动向量以支持可编辑重建，以及降低对大规模标注静态数据的依赖。

![[assets/figures/papers/paper_list_l3_https_arxiv_org_abs_2412_03526/figures/004_Table_1.jpg]]
*Table 1: Quantitative comparisons on dynamic datasets. (a) DyCheck iPhone dataset [64] comparison. (b) NVIDIA Dynamic Scene dataset [1] comparison. The results are rendered on 4 8 0 $\times$ 2 7 0 resolution. ‘Rec. Time’ is per-scene reconstruction time. †: Video-consistent depth estimation step included. We highlight the best , second best , and third best results*

![[assets/figures/papers/paper_list_l3_https_arxiv_org_abs_2412_03526/figures/008_Figure_7.jpg]]
*Figure 7: Quantitative comparisons on static datasets. (a) results on the RE10K benchmark [50]; (b) results on the Tanks and Temples benchmark [69]. We highlight the best , second best , and third best models. ∗: Our reproduced results*

## 定位与知识库关联

### 1. 问题定位与核心瓶颈

BTimer 瞄准的核心瓶颈是：**现有前馈式场景重建模型无法泛化到包含复杂运动的动态场景**。此前的前馈方法（如 pixelSplat、MVSplat、GS-LRM 等）在静态多视图重建上取得了显著进展，但它们缺乏有效处理 4D 时空信息的能力——当场景中存在物体运动、非刚性变形或遮挡关系随时间变化时，这些模型要么完全无法工作，要么产生严重的重影和几何崩溃。另一方面，基于优化的动态重建方法（如 HyperNeRF、4D-GS 等）虽然能处理运动，但每个场景需要数小时到数天的逐场景优化，无法满足实时应用需求。**速度与泛化能力之间的鸿沟**构成了本工作的直接动机。

### 2. 方法在知识库中的位置

BTimer 处于**前馈式 3D 重建**与**动态场景新视角合成**两条研究脉络的交汇点。从技术架构来看，它继承了前馈式 3DGS 预测的范式——用 ViT 编码多视图上下文，直接回归 3D 高斯参数——但其关键创新在于将时间维度显式建模为可条件化的生成变量。

#### 2.1 与前馈式静态重建方法的关系

BTimer 的静态版本（Ours-Static）直接对标以下前馈式 3DGS 方法：

- **pixelSplat** (Charatan et al., CVPR 2024)：基于 epipolar transformer 的 3DGS 预测。
- **MVSplat** (Chen et al., ECCV 2024)：引入代价体构建的多视图 3DGS 预测。
- **GS-LRM** (Zhang et al., 2024)：大规模 transformer 直接回归 3DGS 参数。
- **GPNR** (Szymanowicz et al., CVPR 2024)：基于像素对齐高斯的可泛化重建。

在 RE10K 静态基准上，BTimer-Static 以 **LPIPS 0.070** 显著优于上述所有方法（最佳基线 GS-LRM 为 0.114，MVSplat 为 0.128），证明了其架构在静态场景上的竞争力。更重要的是，BTimer 的子弹时间公式天然兼容静态数据（静态场景可视为所有时间戳相同的特例），这使得它能够利用大规模静态多视图数据集进行预训练，学习强有力的运动感知几何先验——这是纯动态方法无法获得的优势。

#### 2.2 与动态场景重建方法的关系

在动态场景领域，BTimer 与以下方法形成对比：

**基于优化的方法：**
- **HyperNeRF** (Park et al., CVPR 2021)：用高维空间建模拓扑变化的可变形 NeRF，逐场景优化需约 72 小时。
- **Nerfies** (Park et al., ICCV 2021)：基于 SE(3) 场变形的可变形 NeRF。
- **TiNeuVox** (Fang et al., SIGGRAPH Asia 2022)：基于体素网格的时间插值 NeRF。
- **4D-GS** (Wu et al., CVPR 2024)：将 3DGS 扩展到时间维度的优化方法。
- **RoDynRF** (Liu et al., CVPR 2023)：鲁棒动态辐射场，处理相机位姿噪声。

BTimer 与这些方法的本质区别在于**前馈式推理 vs. 逐场景优化**。在 NVIDIA Dynamic Scene 数据集上，BTimer 以 **0.78s 重建时间**达到 **25.82 PSNR**，而 4D-GS 需要更长的优化时间，Casual-FVS 需 0.25 小时达到 24.57 PSNR。在 DyCheck iPhone 数据集上，BTimer 的 PSNR（16.52）略低于 HyperNeRF（16.81），但**速度快约 264,000 倍**（0.98s vs. 72h）。这种速度-质量权衡使 BTimer 定位于需要实时或近实时重建的应用场景。

**前馈式动态方法：**
- **Casual-FVS** (Lee et al., 2023)：快速动态视图合成，但需要深度估计预处理步骤，重建时间约 0.25 小时。
- **PGDVS** (Zhao et al., ICLR 2024)：前馈动态视图合成，但依赖视频一致性深度估计（†标注）。

BTimer 是首个**纯 RGB 输入、无需深度估计**的前馈式动态 3DGS 重建模型。相比 Casual-FVS，BTimer 在 NVIDIA 数据集上 PSNR 提升 1.25 dB，重建速度提升约 1150 倍。

#### 2.3 核心机制创新：子弹时间嵌入与 NTE 模块

BTimer 的方法论贡献体现在三个可替换的"槽位"上：

| 槽位 | 基线做法 | BTimer 做法 |
|------|---------|------------|
| **时态信息编码** | 无时间编码（仅多视图几何） | 引入基于正弦位置编码的子弹时间戳嵌入（bullet-time embedding），与上下文帧及 Plücker 嵌入相加 |
| **训练策略** | 仅在单一数据集上从头训练 | 三阶段课程学习：大规模混合静态数据集预训练 → 动态数据联合训练 → 长上下文微调 |
| **中间时间戳处理** | 直接由主模型预测未观察时间戳，易产生重影 | 新增 Novel Time Enhancer (NTE) 模块，先预测中间帧 RGB，再送入主模型进行 3DGS 重建 |

子弹时间嵌入的核心洞察在于：**将动态重建重新表述为时间条件生成问题**。给定上下文帧 $\{\mathbf{I}_i\}$ 及其时间戳 $\{t_i\}$，模型被训练为预测目标"子弹时间戳" $t_b$ 处的完整 3DGS 表示。这一公式天然兼容静态数据（$t_b = t_i$ 对所有 $i$），从而解锁了大规模静态数据预训练的可能性。

NTE 模块（Figure 3）解决了一个关键失败模式：当目标时间戳 $t_b \notin \mathcal{T}$ 时，主模型直接从相邻帧的时间特征进行外推，在快速或复杂运动场景中会产生重影。NTE 通过先预测 $t_b$ 处的 RGB 图像（使用线性插值的目标位姿和最近邻上下文帧），再将预测帧作为额外的"子弹帧"输入主模型，显著缓解了这一问题。

### 3. 适用边界与局限

基于论文报告的实验证据和分析，BTimer 的适用边界可归纳如下：

1. **远视角合成能力有限**：模型在渲染远离输入相机轨迹的新视角时，重建质量会明显下降。这是前馈式方法的共性局限——模型缺乏显式的 3D 几何推理，依赖多视图线索进行隐式三角测量，当目标视角与输入视角基线过大时，深度估计的不确定性急剧增加。

2. **极快或高度非刚性运动的模糊**：虽然 NTE 模块缓解了复杂运动的重影问题，但对于极快运动或高度非刚性变形（如流体、烟雾），中间帧的 RGB 预测本身可能不准确，导致级联误差。

3. **几何精度不足**：生成的深度图存在漂移和人为结构（见 Figure 4 的深度图可视化）。这是因为模型仅通过 RGB 渲染损失间接监督几何，缺乏显式的深度或法线约束。

4. **输入依赖**：目前仅支持单目视频输入，且**需要已知相机位姿**，不具备位姿估计的端到端能力。这限制了其在无约束视频上的直接应用。

5. **材质建模受限**：论文未展示对非朗伯表面、透明物体或复杂光照效果的处理能力。

### 4. 开放问题与后续方向

1. **几何精度提升**：如何显式监督或正则化深度图，从而改善远视角合成质量？可能的路径包括引入单目深度估计先验或多视图立体匹配的几何约束。

2. **运动显式恢复**：当前模型隐式编码运动信息，能否在不增加后处理的情况下显式恢复场景的运动向量或几何变形场，以支持可编辑的动态重建？

3. **数据效率**：三阶段课程学习依赖大规模带标注的静态多视图数据（如 RE10K），如何降低对大规模数据集的依赖，或利用自监督/半监督信号进行训练？

4. **材质与光照扩展**：BTimer 框架是否可以扩展到非朗伯表面、透明物体、镜面反射等更复杂的材质建模？这可能需要修改 3DGS 的渲染管线或其参数化方式。

5. **端到端位姿估计**：将相机位姿估计集成到前馈框架中，实现从原始视频到动态 3D 场景的全自动重建流水线。

### 5. 知识库定位总结

BTimer 在动态场景重建领域的定位可概括为：**首个运动感知的前馈式 3DGS 重建模型**，通过子弹时间公式桥接了静态预训练与动态泛化之间的鸿沟。它在速度上比优化方法快数个数量级，在质量上接近甚至超越部分优化方法，同时保持了前馈方法的泛化能力。其核心贡献——时间条件化生成与课程学习策略——为后续将前馈式重建推向更复杂的 4D 场景理解任务提供了可复用的方法论框架。

## 原文 PDF

![[paperPDFs/NEURIPS_2025/Feed_Forward_Bullet_Time_Reconstruction_of_Dynamic_Scenes_from_Monocular_Videos.pdf]]
