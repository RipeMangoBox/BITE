---
title: "MemCam: Memory-augmented Camera Control for Video Generation"
type: paper
paper_level: A
venue: arXiv
year: 2026
pdf_ref: paperPDFs/arxiv_2026/MemCam_Memory_augmented_Camera_Control_for_Video_Generation.pdf
aliases:
- MemCam
tags:
- arxiv_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/image_and_video_generation
- topic/generative_models_diffusion
core_operator: 将历史生成帧作为外部记忆，并引入基于共视性的动态上下文检索与压缩模块，为模型提供长期且相关的场景信息。
primary_logic: 利用外部记忆和高效压缩，将历史帧转化为轻量上下文token，结合共视性选择保证相关性和覆盖均匀性，从而在维持计算效率的同时显著扩展有效上下文，解决长视距和大相机运动下的场景漂移问题。
claims:
- MemCam 将历史帧视为外部记忆，并利用共视性选择动态检索最相关的历史帧作为上下文条件。
- MemCam 在所有测试设置中均取得最佳 FVD，表明其具有优越的时序一致性和视觉质量，尤其是在长时间和大相机旋转场景下。
- 上下文压缩模块使模型在维持与未压缩长上下文相近质量的同时，推理速度提升约5倍。
- Context-as-Memory 90° Round-trip 上 FVD↓ = 215.71
---

# MemCam: Memory-augmented Camera Control for Video Generation

> [!tip] 核心洞察
> 利用外部记忆和高效压缩，将历史帧转化为轻量上下文token，结合共视性选择保证相关性和覆盖均匀性，从而在维持计算效率的同时显著扩展有效上下文，解决长视距和大相机运动下的场景漂移问题。

| 字段 | 内容 |
|------|------|
| 中文题名 | MemCam: 记忆增强的相机控制视频生成 |
| 英文题名 | MemCam: Memory-augmented Camera Control for Video Generation |
| 会议/期刊 | arXiv 2026 |
| Links | [paper](https://arxiv.org/abs/2603.26193) · [Code](https://github.com/) · [Project](https://oasis-model.github.io) · [arXiv](https://arxiv.org/abs/1505.04597) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/image_and_video_generation #topic/generative_models_diffusion |
| Method | MemCam |
| Dataset | Context-as-Memory 90° Round-trip, Context-as-Memory 360° Round-trip, RealEstate10K 90° Round-trip, RealEstate10K 360° Round-trip |

> [!tip] 效果简介
> - Context-as-Memory 90° Round-trip 上，FVD↓ 215.71 vs 557.66 (GF) (-341.95)。
> - Context-as-Memory 360° Round-trip 上，FVD↓ 167.87 vs 852.05 (GF) (-684.18)。
> - RealEstate10K 90° Round-trip 上，FVD↓ 269.82 vs 519.78 (GF) (-249.96)。

## 概述

现有交互式视频生成方法在长时序列和大视角旋转场景下，普遍因缺乏有效的历史帧记忆机制而出现严重的场景遗忘与内容不一致问题。**MemCam** 针对这一瓶颈，提出将先前生成帧视为外部记忆，并通过基于共视性的动态上下文检索与压缩，为模型注入长期且相关的场景信息，从而在维持计算效率的同时显著扩展有效上下文。

核心思路是：维护一个包含历史帧及其相机参数的外部记忆库，对每一待预测帧，利用蒙特卡洛采样近似计算相机视锥的共视性交并比（IoU），动态选取最相关的历史帧作为上下文条件。这些上下文帧经 **3D VAE** 编码后，由专用的 **Context Compressor**（卷积网络替代基础 patchify 层，空间 2× 压缩）转化为紧凑表示，与噪声预测序列拼接后送入 **DiT Block** 进行双向注意力计算；同时，每个 DiT 块内部通过单层 MLP 的 **Camera Encoder** 将相机姿态信息以元素加和方式注入主特征：

$$\mathbf{F}_{\mathrm{out}} = \mathbf{F}_{\mathrm{in}} + \mathrm{CameraEncoder}(\mathrm{cam})$$

实验表明，MemCam 在 Context‑as‑Memory 和 RealEstate10K 两个数据集的 90° 与 360° 往返基准上，FVD 均显著优于 **GF**（Geometry‑Forcing）等基线（如 360° Context‑as‑Memory 上 FVD 从 852.05 降至 167.87）。消融研究进一步证实：基于共视性的动态选择策略远优于简单的“最近帧”策略（后者 FVD 恶化至 915.41）；上下文压缩模块在保持与未压缩长上下文相近质量的同时，推理速度提升约 5 倍（76 帧上下文从 22.15 秒/帧降至 4.47 秒/帧），且在同时间成本下优于短上下文未压缩方案。

## 背景与动机

可控视频生成旨在根据用户提供的条件信号（如文本、图像、相机轨迹）合成高质量视频，其在电影制作、虚拟现实和具身智能等领域具有广泛应用前景。其中，相机可控的视频生成任务要求模型在用户实时交互指定的相机姿态下，持续生成场景内容一致的视频帧。这一设定与传统的离线视频生成有本质区别：模型必须在生成过程中动态响应新的相机指令，同时保持对已生成场景内容的长期记忆。

当前方法在这一任务上面临一个核心瓶颈：**长时交互下的场景遗忘与内容漂移**。具体而言，现有方案大致可分为两类。一类是仅以首帧为条件的图像到视频（I2V）方法，其上下文窗口局限于单帧，无法在大角度旋转或长序列生成中维持场景一致性。另一类方法如 **DFoT**（Song et al., arXiv 2025）采用固定长度的上下文窗口，仅保留最近的若干历史帧作为条件；**GF**（Wu et al., arXiv 2025）则通过3D显式重建施加几何约束以增强多视图一致性。然而，这些方法均缺乏对历史帧信息的有效记忆与检索机制——当相机旋转超过180°或序列长度显著增长时，模型会“遗忘”先前生成的场景内容，导致新生成帧中出现不一致的几何结构和纹理。

这一瓶颈的因果根源在于：**历史帧信息未被显式维护为可检索的外部记忆，且上下文选择策略未能兼顾相关性与覆盖均匀性**。固定窗口方法仅保留最近帧，当相机回望已离开的区域时，相关历史信息已从窗口中滑出；而简单的全量拼接则带来计算开销的急剧膨胀，难以在交互场景中实时应用。

针对上述缺口，**MemCam** 提出将历史生成帧视为外部记忆，并设计了一套基于共视性的动态上下文检索与压缩机制。其核心思路是：为每一待预测帧，从历史记忆中检索与其相机视场最相关的帧子集，经高效压缩后作为条件注入扩散Transformer。这一设计在维持计算效率的同时，显著扩展了有效上下文范围，从而从根本上缓解长视距和大相机运动下的场景漂移问题。

## 核心创新

MemCam 的核心创新在于将视频生成中的上下文建模从“被动遗忘”转变为“主动记忆”，其关键因果操作为：**将历史生成帧构建为外部记忆，并通过基于共视性的动态检索与压缩，为模型提供长期、相关且计算高效的场景上下文**。这一设计直接针对长时交互视频生成中，因缺乏有效历史帧记忆而导致的大视角旋转与长序列场景内容不一致的瓶颈。

### 方法谱系与知识库定位

与现有方法相比，MemCam 在三个关键维度上引入了根本性改变：

1.  **上下文记忆机制**：从无记忆或固定窗口到**显式外部记忆 + 动态检索**。
    *   **I2V 基线**仅使用第一帧作为上下文，完全不具备长时记忆能力。
    *   **DFoT** (Song et al., arXiv 2025) 基于固定长度的上下文窗口进行扩散强迫训练，其记忆范围受窗口大小刚性限制。
    *   **GF** (Wu et al., arXiv 2025) 通过 3D 显式重建施加几何约束，但未建立显式的历史帧记忆机制。
    MemCam 则维护一个包含相机信息的历史帧序列，并**为每一预测帧动态计算其与所有历史帧的共视性（Co-visibility）**，选择最相关的帧作为上下文条件，从而在长序列和大旋转下仍能检索到关键场景信息。

2.  **上下文特征处理**：从直接拼接原始帧到**高效压缩编码**。
    基线方法通常直接拼接原始帧作为上下文 token，导致序列长度随记忆帧数线性增长，计算开销巨大。MemCam 提出**上下文压缩模块（Context Compressor）**，使用卷积网络替代基础模型的 patchify 层，对上下文帧进行空间维度 2 倍压缩，将 token 长度降至原始的 1/4，在保留时间维度的同时大幅降低计算负担。

3.  **相机控制方式**：从无控制或复杂机制到**轻量即插即用注入**。
    MemCam 采用了一种极简的相机控制方案：在每个 DiT 块中添加一个**单层 MLP 相机编码器（Camera Encoder）**，将相机参数（R|t）映射后以元素加和的方式注入主特征流，如公式所示：
    $$\mathbf{F}_{\mathrm{out}} = \mathbf{F}_{\mathrm{in}} + \mathrm{CameraEncoder}(\mathrm{cam})$$
    这种设计使其能灵活地作为即插即用模块集成到现有 DiT 架构中。

### 关键设计决策与因果机制

MemCam 的优越性能源于两个核心设计之间的协同效应：

*   **共视性驱动的动态选择**：该策略是保证记忆“相关性”与“覆盖均匀性”的关键。通过蒙特卡洛采样（N=10⁴ 个 3D 点）估算两个相机视锥的可见点集交并比（IoU）来定义共视性：
    $$\operatorname{IoU}({\mathcal{C}_1},{\mathcal{C}_2}) = \frac{\sum_{i=1}^{N} {\mathcal{V}_1}(\mathbf{x}_i) \wedge {\mathcal{V}_2}(\mathbf{x}_i)}{\sum_{i=1}^{N} {\mathcal{V}_1}(\mathbf{x}_i) \vee {\mathcal{V}_2}(\mathbf{x}_i)} \in [0,1]$$
    消融实验证实，简单的“最近帧”选择策略在 360° 往返基准上会导致性能急剧下降（FVD 飙升至 915.41），而 MemCam 的共视性动态选择达到了最佳 FVD 167.87，证明了仅靠时间邻近性远不足以保证场景内容的相关性。

*   **上下文压缩模块**：该模块解决了长记忆带来的计算瓶颈。实验表明，使用完整 76 帧上下文但不压缩（None-76）虽然质量接近，但推理速度极慢（22.15 秒/帧）；而 MemCam 的压缩方案（Ours-76）在维持几乎相同生成质量的同时，推理速度提升近 5 倍（4.47 秒/帧）。更重要的是，在相仿的时间成本下，Ours-76 的质量显著优于使用 19 帧未压缩上下文的 None-19（PSNR 14.81 vs. 14.69），证明了压缩模块实现了更高效的信息利用。

### 局限性

当前方法的主要局限在于推理速度仍较慢，这主要源于 DiT 块中双向注意力的计算开销。未来的改进方向包括通过扩散蒸馏技术加速推理，以及扩大训练数据规模以进一步提升生成质量。

## 整体框架

MemCam 的整体流程围绕一个核心思想展开：将**已生成的历史帧视为外部记忆**，并通过**共视性驱动的动态检索与压缩**，为当前预测帧提供长期且相关的场景上下文。整个 pipeline 由五个关键模块串联构成，形成“记忆存取—条件注入—扩散生成”的闭环。

### 推理流程概览

在推理阶段，系统采用**分段生成**策略。对于待预测的每一帧，流水线依次执行以下步骤：

1. **共视性选择**：从历史帧记忆库中，基于当前预测帧的相机姿态，动态检索最相关的上下文帧。
2. **上下文压缩**：选中的历史帧首先经 3D VAE 编码为潜在表示，再通过 Context Compressor 进行空间压缩，转化为轻量上下文 token。
3. **相机条件注入**：当前预测帧的相机参数（旋转 R | 平移 t）经 Camera Encoder 编码后，以元素相加的方式注入 DiT Block 的主特征。
4. **双向注意力扩散**：压缩后的上下文 token 与带噪预测序列拼接，送入 DiT Block 进行时空联合注意力计算，最终由 3D VAE 解码器重建出视频帧。

### 模块关系与数据流

下图（Fig. 2）直观展示了各模块间的连接关系：历史帧记忆库经 Co-visibility Selector 筛选后，输入 Context Compressor 进行编码压缩；压缩后的上下文 token 与当前噪声序列在通道维度拼接，共同进入 DiT Block；Camera Encoder 则并行地将相机信息注入每个 DiT Block 的特征空间。

![[assets/figures/papers/paper_list_l13_https_arxiv_org_abs_2603_26193/figures/002_Figure_2.jpg]]
*Figure 2: Methodology. (Left) Overview of MemCam: the Context Compressor encodes historical frames selected via co-visibility into compact representations, which are concatenated with the noisy prediction sequence and fed into the DiT Block. (Right) Illustration of co-visibility computation between predicted and historical camera FOVs*

**数据流的关键节点**：
- **输入**：历史帧序列及其对应相机参数、当前预测帧的噪声潜在表示及目标相机参数。
- **记忆存取**：Co-visibility Selector 通过蒙特卡洛采样计算视锥重叠 IoU（见公式 Eq. 2），为每帧独立选择上下文，保证相关性与覆盖均匀性。
- **特征压缩**：Context Compressor 以卷积网络替代基础模型的 patchify 层，空间维度压缩比为 2，使 token 长度降至原始的 1/4。
- **条件融合**：Camera Encoder 为单层 MLP，其输出经重复扩展后与 DiT Block 输入特征按元素相加（见公式 Eq. 1）。
- **输出**：3D VAE 解码器从 DiT Block 输出的去噪潜在表示中重建视频帧，该帧随后被加入历史记忆库，用于后续帧的生成。

### 训练与推理的差异

训练时，上下文帧同样基于共视性从同一视频片段内选取，并以 10% 概率将所选上下文全部置零，以支持图像到视频（I2V）生成场景。推理时则从已生成的历史帧中，为每帧选择共视性得分最高的上下文帧，确保信息最相关。

> **需手动验证**：论文未详细说明 Context Compressor 的具体卷积架构细节（如层数、卷积核大小），仅提及空间压缩比为 2。若需精确复现，建议查阅官方代码仓库。

## 核心模块与公式推导

MemCam 整体框架由五个关键模块构成（图2），其核心设计围绕“历史帧记忆化”与“高效上下文注入”展开。本节聚焦各模块的机理与关键公式，不涉及训练/推理流程细节。

### 3D VAE 与上下文压缩器

基座模型使用 **3D VAE** 将原始帧编码至潜在空间。在此基础上，MemCam 设计了 **上下文压缩器（Context Compressor）**，以卷积网络替代基座模型原有的 patchify 层，对上下文帧进行空间压缩。压缩比在空间长宽维度均设为 2，使得每帧上下文 token 长度降至原来的 1/4。该模块输出的紧凑潜在表示随后与噪声预测序列拼接，送入 DiT 块进行双向注意力计算。

### 相机编码器

相机控制通过在每个 DiT 块中插入一个单层 MLP 实现，称为 **相机编码器（Camera Encoder）**。给定相机参数 $\mathrm{cam}$（包含旋转 $\mathbf{R}$ 和平移 $\mathbf{t}$），其注入方式为逐元素加法：

$$\mathbf{F}_{\mathrm{out}} = \mathbf{F}_{\mathrm{in}} + \mathrm{CameraEncoder}(\mathrm{cam})$$

其中 $\mathbf{F}_{\mathrm{in}}$ 为 DiT 块的输入特征，$\mathrm{CameraEncoder}(\cdot)$ 将相机信息映射至与主特征相同的通道维度，经空间重复扩展后逐元素相加。此设计使模型能感知每帧对应的相机姿态，从而在生成过程中维持空间一致性。

### 共视性选择器

**共视性选择器（Co-visibility Selector）** 是 MemCam 记忆机制的核心。其目标是从历史帧外部记忆中，为每一待预测帧动态检索最相关的上下文帧。共视性度量基于两个相机视锥的可见 3D 点集交并比（IoU）定义。

具体而言，通过蒙特卡洛采样在场景空间中随机采样 $N = 10^4$ 个 3D 点 $\mathbf{x}_i$，对每个相机 $k$ 定义可见性指示函数 $\mathcal{V}_k(\mathbf{x}_i) \in \{0, 1\}$，表示点 $\mathbf{x}_i$ 是否落在相机 $k$ 的视锥内。两个相机 $\mathcal{C}_1, \mathcal{C}_2$ 的共视性 IoU 定义为：

$$\operatorname{IoU}(\mathcal{C}_1, \mathcal{C}_2) = \frac{\sum_{i=1}^{N} \mathcal{V}_1(\mathbf{x}_i) \wedge \mathcal{V}_2(\mathbf{x}_i)}{\sum_{i=1}^{N} \mathcal{V}_1(\mathbf{x}_i) \vee \mathcal{V}_2(\mathbf{x}_i)} \in [0,1]$$

其中 $\wedge$ 和 $\vee$ 分别表示逻辑与、逻辑或。该值越接近 1，表明两个相机视场重叠越多，历史帧与当前预测帧的场景相关性越强。

基于此度量，选择器为每帧动态选取共视性最高的历史帧作为上下文条件，既保证了信息的相关性，又通过逐帧独立选择实现了对历史记忆的均匀覆盖，避免因固定窗口或“最近帧”策略导致的场景遗忘问题。

### DiT 块与双向注意力

压缩后的上下文 token 与噪声预测序列拼接后，送入标准的 **DiT 块（含双向注意力）** 进行时空联合建模。双向注意力机制使每一预测帧能够同时关注所有上下文帧，从而有效利用长期记忆信息。这也是推理速度的主要瓶颈所在——上下文长度增加时，注意力计算开销显著上升，而上下文压缩模块正是为解决此问题而设计。

## 实验与分析

### 主实验结果

MemCam 在两个数据集（Context-as-Memory 和 RealEstate10K）的 90° 和 360° 往返基准上全面验证。表 I 汇总了与 I2V 基线、**DFoT**（Song et al., arXiv 2025）和 **GF**（Wu et al., arXiv 2025）的定量对比。

核心发现：MemCam 在所有设置下均取得最佳 FVD，尤其在长时大角度旋转场景中优势显著。在 Context-as-Memory 360° 往返基准上，MemCam 的 FVD 为 167.87，GF 为 852.05，降幅达 684.18；在 90° 基准上，MemCam 为 215.71，GF 为 557.66，降幅 341.95。RealEstate10K 上趋势一致：360° 场景 FVD 131.96（GF 419.60），90° 场景 269.82（GF 519.78）。

这一结果直接印证了核心因果机制：外部记忆与共视性检索有效解决了长序列下的场景漂移问题。GF 依赖 3D 显式重建施加几何约束，在 360° 大旋转下因累积误差导致场景一致性崩溃；I2V 仅用第一帧作为上下文，完全无法应对视角大幅变化；DFoT 的固定窗口上下文在长序列中同样丢失早期场景信息。MemCam 通过动态检索相关历史帧，在维持计算可行性的同时显著扩展了有效上下文窗口。

在图像质量指标（PSNR、SSIM、LPIPS）上，MemCam 同样领先。Context-as-Memory 360° 场景下 PSNR 14.81、SSIM 0.423、LPIPS 0.504；RealEstate10K 360° 场景下 PSNR 16.52、SSIM 0.550、LPIPS 0.400。这些指标与 FVD 的协同改善表明，记忆机制不仅提升了时序一致性，也直接贡献于逐帧重建质量。

定性结果（图 3）进一步佐证：MemCam 在 360° 往返和单方向旋转中始终保持场景内容一致，而基线方法出现不同程度的场景遗忘或扭曲，尤其在相机旋转超过 180° 后差异更为明显。

### 消融实验

**上下文选择策略。** 表 II 对比了三种策略：仅用第一帧（First）、选择最近帧（Recent）、以及 MemCam 的逐帧共视性动态选择（Ours）。在 360° 往返基准上，Recent 策略的 FVD 急剧恶化至 915.41，甚至远差于仅用第一帧的 711.63。这表明在长序列大旋转下，最近帧与当前帧的视域重叠可能极低，提供的是噪声而非有效上下文。Ours 的 FVD 为 167.87，验证了共视性选择同时保证相关性和覆盖均匀性的关键作用。

**上下文压缩模块。** 表 III 消融了压缩策略与上下文长度。None-76（完整 76 帧无压缩）虽质量接近 Ours-76，但推理速度慢至 22.15 秒/帧；Ours-76 仅需 4.47 秒/帧，速度提升约 5 倍，且 PSNR 14.81 与 None-76 的 14.82 几乎持平。更关键的是，在相近时间成本下，Ours-76（4.47 秒/帧）优于 None-19（4.45 秒/帧，PSNR 14.69），证明压缩模块使模型能在相同计算预算内利用更长的上下文历史，而非简单牺牲上下文换取速度。

### 失败模式与局限

当前方法的主要瓶颈在于推理速度。尽管压缩模块将上下文 token 数降至 1/4，双向注意力机制仍带来显著计算开销（Ours-76 仍需 4.47 秒/帧）。论文指出未来可借助扩散蒸馏进一步加速。

此外，共视性选择基于蒙特卡洛采样的 FOV 重叠 IoU 计算，在复杂遮挡场景下的鲁棒性尚未充分验证。当前评估集中于室内和室外建筑场景，对多物体密集遮挡环境的可扩展性仍是开放问题。

### 图表结论要点

- **图 3**：定性对比显示 MemCam 在 360° 旋转中始终保持场景记忆，基线方法随旋转角度增大出现明显内容漂移。
- **表 I**：MemCam 在所有基准的 FVD 上大幅领先，360° 场景优势尤为突出。
- **表 II**：共视性动态选择是性能关键，最近帧策略在 360° 场景下完全失效。
- **表 III**：上下文压缩在几乎不损失质量的前提下实现约 5 倍加速，使长上下文在计算上可行。

### 补充图表

![[assets/figures/papers/paper_list_l13_https_arxiv_org_abs_2603_26193/figures/004_Table.jpg]]
*Table: I: Quantitative Comparison Results. We evaluate on two datasets with 90° and 360° round-trip benchmarks. ↑ means higher is better, ↓ means lower is better. Best results are in bold, second best are underlined. TABLE II: Ablation on Context Selection Strategy. TABLE III: Ablation on Context Compression Module*

![[assets/figures/papers/paper_list_l13_https_arxiv_org_abs_2603_26193/figures/003_Figure_3.jpg]]
*Figure 3: Qualitative Comparison Results. (a) and (b) are evaluated on the Context-as-Memory dataset, and (c) and (d) on RealEstate10K. MemCam achieves superior performance in scene memory retention and overall generation quality. In contrast, other methods exhibit varying degrees of scene inconsistency due to insufficient utilization of contextual information*

![[assets/figures/papers/paper_list_l13_https_arxiv_org_abs_2603_26193/figures/001_Figure_1.jpg]]
*Figure 1: MemCam generates videos with high scene consistency over long time horizons and under large camera rotations. Rows 1-2 show results on the test split of our dataset, including 360° round-trip and 360° single-direction rotation. Row 3 presents open-domain real-world scenes, demonstrating that MemCam maintains long-term scene consistency across varied scenes*

## 方法谱系与知识库定位

### 核心问题与基线对比

MemCam 聚焦于长时交互视频生成中的**场景一致性漂移**问题：当相机经历大视角旋转或长序列生成时，现有方法因缺乏有效的历史帧记忆机制，会逐渐“遗忘”先前生成的场景内容，导致前后帧不一致。围绕这一问题，MemCam 与三类代表性基线形成了清晰的对比：

- **I2V（Image-to-Video 基线）**：仅使用第一帧作为上下文条件，完全不具备历史记忆能力。该基线在相同基模型和训练配置下实现，确保了直接可比性。其性能在长时间和大旋转场景下急剧退化，直接验证了“无记忆”策略的根本性缺陷。

- **DFoT（Diffusion Forcing Transformer，Song et al., arXiv 2025）**：采用固定长度上下文窗口的扩散强迫训练方法，可视为一种“滑动窗口记忆”。但其上下文仅覆盖最近的若干帧，当相机旋转超出窗口覆盖范围时，早期场景信息永久丢失，无法应对 360° 往返等极端场景。

- **GF（Geometry-Forcing，Wu et al., arXiv 2025）**：通过 3D 显式重建施加几何约束以增强多视图一致性。该方法引入了显式的几何先验，但在长序列下仍缺乏对历史生成内容的直接记忆，导致几何约束本身无法弥补内容遗忘。

MemCam 的关键突破在于将问题从“如何更好地利用最近帧”重新定义为“如何从完整历史中动态检索最相关的信息”。这一思路与检索增强生成（RAG）在语言模型中的应用有精神上的相似性，但在视频生成领域，MemCam 首次将外部记忆、共视性检索和压缩编码系统性地结合。

### 方法谱系中的定位

从技术组件角度看，MemCam 处于以下几条方法线的交汇点：

1. **扩散 Transformer（DiT）视频生成线**：MemCam 基于 DiT 架构构建，继承了时空联合注意力的生成范式。其双向注意力机制允许噪声预测序列与上下文 token 之间的充分交互，这是实现条件生成的基础。

2. **相机可控视频生成线**：与无条件生成或文本条件生成不同，MemCam 引入了显式的相机姿态控制。其 Camera Encoder（单层 MLP，将相机参数 $R|t$ 映射并注入每个 DiT 块）的设计简洁而有效，控制信号通过元素加法融入特征流：
   $$\mathbf{F}_{\mathrm{out}} = \mathbf{F}_{\mathrm{in}} + \mathrm{CameraEncoder}(\mathrm{cam})$$
   这种轻量设计避免了复杂的交叉注意力或条件归一化，同时保持了相机控制的精确性。

3. **外部记忆与上下文压缩线**：这是 MemCam 最具区分度的贡献。Context Compressor 以卷积网络替代基础 patchify 层，对上下文帧进行空间 2× 压缩，将 token 长度减少至 1/4。这一设计使得模型可以在几乎不损失质量的前提下，将有效上下文长度从 19 帧扩展到 76 帧，同时推理速度提升约 5 倍（22.15 s/frame → 4.47 s/frame）。

4. **共视性驱动的动态检索线**：Co-visibility Selector 通过蒙特卡洛采样（$N=10^4$ 个 3D 点）计算两个相机视锥的可见点集交并比：
   $$\operatorname{IoU}(\mathcal{C}_1, \mathcal{C}_2) = \frac{\sum_{i=1}^{N} \mathcal{V}_1(\mathbf{x}_i) \wedge \mathcal{V}_2(\mathbf{x}_i)}{\sum_{i=1}^{N} \mathcal{V}_1(\mathbf{x}_i) \vee \mathcal{V}_2(\mathbf{x}_i)} \in [0,1]$$
   基于此度量为每一预测帧动态选择最相关的历史帧。消融实验表明，简单的“最近帧”策略在 360° 往返场景下 FVD 飙升至 915.41，而共视性选择达到 167.87，这揭示了**相关性**和**覆盖均匀性**在记忆检索中的同等重要性。

### 适用边界与局限

MemCam 的优势场景明确：**需要长时间场景记忆且相机运动幅度大的交互式视频生成**，如 360° 场景漫游、大角度旋转拍摄等。在两个基准数据集（Context-as-Memory 和 RealEstate10K）的 90° 和 360° 往返测试中，MemCam 在所有设置下均取得最佳 FVD，且在大旋转场景下的优势更为显著（360° 场景下 FVD 相对 GF 降低 287–684 点）。

然而，方法存在以下已知局限：

- **推理速度瓶颈**：尽管压缩模块大幅降低了上下文 token 数量，双向注意力的计算开销仍是推理速度的主要制约。论文明确指出未来拟通过扩散蒸馏加速推理，这一方向与当前视频扩散模型的加速研究趋势一致。

- **训练数据与泛化边界**：当前模型在室内场景数据集上训练，虽然在开放域真实场景（Figure 1 Row 3）中展示了初步泛化能力，但论文未提供大规模开放域评估的定量结果，跨域泛化的上限尚不明确。

### 开放问题

1. **复杂遮挡下的共视性选择可靠性**：当前的共视性计算基于视锥内 3D 点的可见性，并未显式建模场景中的遮挡关系。在多物体遮挡场景下，两个相机即使有高 IoU 共视区域，实际可见的场景内容可能因遮挡而截然不同。共视性度量是否会在遮挡密集的场景中失效，需要进一步验证。

2. **压缩模块与双向注意力的联合优化空间**：当前压缩模块仅作用于空间维度，时间维度的信息冗余未被利用。是否可以通过时序压缩或稀疏注意力机制进一步降低双向注意力的开销，是一个值得探索的方向。

3. **记忆更新与遗忘策略**：MemCam 当前维护完整的历史帧记忆，未引入主动的遗忘或记忆整合机制。在极长序列（如数千帧）下，记忆库的线性增长将带来检索效率和质量的双重挑战。如何设计自适应的记忆管理策略，是迈向真正无限长视频生成的关键问题。

4. **与 3D 重建方法的深度融合**：GF 的几何约束与 MemCam 的记忆机制在原理上互补——前者提供显式的空间一致性先验，后者提供内容级别的长期记忆。两者的有效结合可能进一步提升大旋转场景下的生成质量，但如何在训练和推理中统一这两种异构信号仍是一个开放挑战。

## 原文 PDF

![[paperPDFs/arxiv_2026/MemCam_Memory_augmented_Camera_Control_for_Video_Generation.pdf]]