---
title: "Tora: Trajectory-oriented Diffusion Transformer for Video Generation"
type: paper
paper_level: A
venue: CVPR
year: 2025
pdf_ref: paperPDFs/CVPR_2025/Tora_Trajectory_oriented_Diffusion_Transformer_for_Video_Generation.pdf
project_link: null
code_link: https://github.com/alibaba/Tora
aliases:
- Tora
tags:
- CVPR_2025
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/image_and_video_generation
- topic/vision_multimodal_applications/3d_rendering_reconstruction
- topic/generative_models_diffusion
core_operator: 通过Trajectory Extractor和Motion-guidance Fuser，将任意轨迹编码为时空运动块并自适应注入DiT块，使模型能够遵循用户指定的轨迹。
primary_logic: 利用3D运动VAE将轨迹压缩至与视频块共享的潜在空间，并与DiT的可扩展性无缝集成，首次实现了面向轨迹的DiT视频生成，显著提升了长视频的运动控制精度和视觉一致性。
claims:
- 在128帧生成设定下，Tora的轨迹误差（TrajError）仅为11.72，而最佳UNet基线MotionCtrl为38.39，精度提升约3.3倍；FVD为494，较MotionCtrl的731降低32.4%。
- 在128帧设定下，Tora相比OpenSora-based DragNUWA基线，TrajError从21.75降至11.72，FVD从565降至494，验证了所提运动模块与DiT架构的良好兼容性。
- 128-frame motion-controllable video generation 上 Trajectory Error (↓) = 11.72
- 128-frame motion-controllable video generation 上 FVD (↓) = 494
---

# Tora: Trajectory-oriented Diffusion Transformer for Video Generation

> [!tip] 核心洞察
> 利用3D运动VAE将轨迹压缩至与视频块共享的潜在空间，并与DiT的可扩展性无缝集成，首次实现了面向轨迹的DiT视频生成，显著提升了长视频的运动控制精度和视觉一致性。

| 字段 | 内容 |
|------|------|
| 中文题名 | Tora：面向轨迹的扩散Transformer视频生成 |
| 英文题名 | Tora: Trajectory-oriented Diffusion Transformer for Video Generation |
| 会议/期刊 | CVPR 2025 |
| Links | [paper](https://arxiv.org/abs/2407.21705) · [Code](https://github.com/alibaba/Tora) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/image_and_video_generation #topic/vision_multimodal_applications/3d_rendering_reconstruction #topic/generative_models_diffusion |
| Method | Tora |
| Dataset | 128-frame motion-controllable video generation |

> [!tip] 效果简介
> - 128-frame motion-controllable video generation 上，Trajectory Error (↓) 11.72 vs 38.39 (MotionCtrl) (-26.67)；FVD (↓) 494 vs 565 (OpenSora-based DragNUWA) (-71)。

## 概要

**问题瓶颈**：基于UNet的视频扩散模型在生成超过16帧的长视频时，运动控制能力显著退化——轨迹误差随帧数增加急剧上升，且DiT架构虽在可扩展性上优于UNet，但缺乏有效的运动引导机制，导致生成的运动随机、失真，无法遵循用户指定的物体轨迹。

**核心思路**：Tora通过两个关键模块将任意轨迹控制引入DiT视频生成框架——**Trajectory Extractor (TE)** 利用3D运动VAE将稀疏轨迹点编码为与视频块共享潜在空间的时空运动块（motion patches），**Motion-guidance Fuser (MGF)** 则通过自适应归一化层将多级运动特征注入ST-DiT的各个块中，使去噪过程始终遵循指定轨迹。该设计首次实现了面向轨迹的DiT视频生成，无需修改基础DiT架构即可无缝集成其可扩展性优势。

**方法定位**：Tora属于扩散Transformer（DiT）视频生成框架下的运动可控生成方法。与UNet路线的运动控制工作（如**VideoComposer** (Wang et al., NeurIPS 2023)、**DragNUWA** (Yin et al., arXiv 2023)、**MotionCtrl** (Wang et al., SIGGRAPH 2024)）不同，Tora直接在DiT架构（基于OpenSora）上构建运动模块，避免了UNet在长视频生成中因顺序推理引入的累积误差。相较于将DragNUWA的运动控制方式简单迁移到DiT的基线（OpenSora-based DragNUWA），Tora的3D VAE压缩与自适应融合策略显著提升了轨迹遵循精度。

**主要结果**：在128帧生成设定下，Tora的轨迹误差（TrajError）仅为11.72，相较最佳UNet基线MotionCtrl的38.39降低约3.3倍；FVD为494，较MotionCtrl的731降低32.4%。与DiT基线OpenSora-based DragNUWA相比，TrajError从21.75降至11.72，FVD从565降至494，验证了所提运动模块与DiT架构的良好兼容性。消融实验进一步证实了3D运动VAE压缩、自适应归一化融合和两阶段训练策略各自的关键贡献。

### 视频生成范式的演进与运动控制瓶颈

扩散模型在文本到视频（T2V）生成领域取得了显著进展，其核心架构经历了从基于UNet的3D变体到扩散Transformer（DiT）的演进。早期工作如**VideoComposer**（Wang et al., NeurIPS 2023）和**DragNUWA**（Yin et al., arXiv 2023）在UNet框架下探索了运动控制机制，但这些方法在生成长视频时面临根本性限制：UNet架构通过顺序推理扩展帧数，这一过程会引入累积误差，导致运动精度随帧数增加而急剧下降。

DiT架构的引入为视频生成带来了可扩展性优势，**OpenSora**（Zheng et al., arXiv 2024）等基础模型展示了DiT在文本到视频生成中的潜力。然而，这些DiT基础模型缺乏运动引导机制，生成的视频运动呈现随机性，无法满足用户对精确运动控制的需求。核心瓶颈在于：**如何将任意轨迹条件有效地注入DiT架构，使其既能保持DiT的可扩展性，又能实现精确的运动遵循**。

### 现有运动控制方法的局限

现有运动可控视频生成方法主要可分为以下几类，但各自存在明显不足：

- **基于UNet的轨迹控制方法**：如**MotionCtrl**（Wang et al., SIGGRAPH 2024）通过额外通道注入摄像机/物体运动条件，**DragNUWA**利用稀疏轨迹引导运动，**TrailBlazer**（Kurt Ma et al., SIGGRAPH Asia 2024）采用边界框轨迹控制。这些方法受限于UNet架构，在128帧设定下轨迹误差（TrajError）高达38.39，且视觉质量指标FVD达到731，难以满足长视频生成需求。

- **基于UNet的运动掩码方法**：如**AnimateAnything**（Dai et al., arXiv 2023）通过运动掩码控制运动区域，但缺乏对精确轨迹的细粒度控制能力。

- **DiT架构的初步尝试**：将DragNUWA的运动控制机制直接迁移到OpenSora DiT架构上（即OpenSora-based DragNUWA），虽然利用了DiT的可扩展性，但由于运动特征提取与注入方式与DiT的patch化输入不兼容，其TrajError仍高达21.75，FVD为565，说明简单的架构迁移无法充分发挥DiT的潜力。

### 运动条件表示与注入的根本性挑战

现有方法在运动条件处理上面临两个深层技术挑战：

1. **运动条件表示的不兼容性**：传统方法使用帧间位移偏移量（$u(x_i, y_i) = x_{i+1} - x_i; v(x_i, y_i) = y_{i+1} - y_i$）或稠密光流直接编码运动条件，这种表示方式与DiT的patch化输入机制存在根本性冲突。DiT将视频分解为时空patch进行处理，而逐点的位移向量缺乏空间结构信息，难以被patch化操作有效利用。

2. **运动条件注入方式的次优性**：现有DiT运动控制基线（OpenSora-based DragNUWA）采用额外通道拼接或线性投影方式注入运动条件，这种简单的注入策略无法在DiT的多层Transformer块中有效传递运动信息，导致运动控制精度不足。

### Tora的核心动机

针对上述瓶颈，Tora的动机聚焦于三个关键突破方向：

- **设计专用于DiT的运动条件表示**：将任意轨迹编码为与视频patch共享潜在空间的时空运动块，使运动条件与DiT的patch化处理机制自然兼容。

- **构建自适应运动融合机制**：通过自适应归一化层将多级运动特征注入DiT块，确保运动条件在生成过程中得到有效利用，而非简单的条件拼接。

- **充分利用DiT的可扩展性**：使运动控制能力随模型规模和生成长度同步提升，突破UNet架构在长视频生成中的性能衰减问题，实现128帧乃至更长视频的精确运动控制。

## 核心方法与创新机理

Tora 的核心创新在于首次将面向轨迹的运动控制能力引入基于 Diffusion Transformer（DiT）的视频生成框架，解决了现有 UNet 基模型在长视频运动控制上精度不足、以及 DiT 基模型缺乏有效运动引导机制的双重瓶颈。其关键创新体现在三个“changed slots”上：

### 1. 运动条件表示：从位移偏移量到时空运动块

传统方法（如 TrailBlazer、MotionCtrl）将轨迹编码为帧间位移偏移量 $u(x_i, y_i), v(x_i, y_i)$ 或稠密光流，直接作为条件输入。Tora 提出了一种全新的运动条件表示——**时空运动块（motion patches）**，通过 **Trajectory Extractor (TE)** 中的 3D 运动 VAE 实现。

具体而言，TE 先将原始轨迹点序列转化为流可视化图像，再利用 3D 运动 VAE 将其压缩至与视频块相同的潜在空间（Section 3.2）。这一设计使得运动条件能够与 DiT 的 patch 化输入在空间和时间维度上自然对齐，保留了跨帧的运动上下文信息。消融实验（Table 2）证实，该 3D VAE 压缩方法在 TrajError 和 FVD 上均显著优于关键帧采样和平均池化方案，验证了定制化 VAE 的必要性。

### 2. 运动条件注入方式：从通道拼接到自适应归一化融合

现有 DiT 基线（如 OpenSora-based DragNUWA）通常采用额外通道拼接或线性投影的方式注入运动条件，但这种方式难以充分利用 DiT 的表示能力。Tora 设计了 **Motion-guidance Fuser (MGF)**，通过自适应归一化层（Adaptive Norm）将多级运动特征注入 DiT 块。

MGF 首先通过堆叠的卷积层从运动潜在块中提取层次化特征 $f_i$（$f_i = \mathrm{Conv}^i(f_{i-1}) + f_{i-1}$），随后利用线性投影将 $f_i$ 转化为缩放参数 $\gamma_i$ 和偏移参数 $\beta_i$，以残差方式调制 DiT 块的隐藏状态：$h_i = \gamma_i \cdot h_{i-1} + \beta_i + h_{i-1}$。Table 3 的消融表明，这种自适应归一化融合在 TrajError 和 FVD 上均优于额外通道拼接和交叉注意力（$h_i = \mathrm{CrossAttn}([h_{i-1}, f_i]) + h_{i-1}$）方案。

### 3. 训练策略：从单阶段到两阶段稠密+稀疏混合训练

现有方法多采用单阶段训练，仅使用稠密光流或稀疏轨迹。Tora 提出了**两阶段训练策略**：第一阶段使用稠密光流训练，使模型学习稳定的运动先验；第二阶段引入随机数量的稀疏轨迹（1～N 条），增强模型对任意轨迹输入的泛化能力。Table 4 的消融显示，这种“Hybrid”策略相比单独使用稠密光流或稀疏轨迹，在 TrajError 上实现了大幅降低，验证了混合训练对运动控制精度的关键作用。

### 创新集成效果

上述三个创新槽位协同作用，使 Tora 在 128 帧生成设定下实现了轨迹误差（TrajError）仅 11.72，较最佳 UNet 基线 MotionCtrl 的 38.39 降低约 3.3 倍；FVD 为 494，较 MotionCtrl 的 731 降低 32.4%（Table 1）。与 OpenSora-based DragNUWA 这一 DiT 基线相比，TrajError 从 21.75 降至 11.72，FVD 从 565 降至 494，充分验证了所提运动模块与 DiT 架构的良好兼容性。

Tora 的整体架构围绕三个核心组件构建：**轨迹提取器**（Trajectory Extractor, TE）、**时空 DiT**（Spatial-Temporal DiT, ST-DiT）和**运动引导融合器**（Motion-guidance Fuser, MGF）。其设计目标是将任意用户指定的轨迹条件无缝注入扩散Transformer的去噪过程，使生成的视频在保持高视觉质量的同时精确遵循给定运动路径。

### 数据流与模块关系

整个生成pipeline的输入输出流如图3所示。系统接收三类条件输入：文本提示、参考图像（可选）以及用户定义的轨迹序列。轨迹首先进入**轨迹提取器**，经过流可视化转换和3D运动VAE压缩，被编码为与视频潜在块共享同一潜在空间的时空运动块（motion patches）。随后，通过堆叠的卷积层提取多级层次化运动特征。

这些多尺度运动特征被送入**运动引导融合器**，以自适应归一化层的形式注入**时空DiT**的各个DiT块中。ST-DiT由空间DiT块（S-DiT-B）和时间DiT块（T-DiT-B）交替堆叠而成，负责在潜在空间中进行视频去噪。最终，去噪后的潜在表示经**视频VAE**解码器恢复为像素空间的视频帧。

### 核心设计动机

传统基于UNet的视频扩散模型（如**VideoComposer**（Wang et al., NeurIPS 2023）、**DragNUWA**（Yin et al., arXiv 2023）、**MotionCtrl**（Wang et al., SIGGRAPH 2024））在处理长视频生成时，运动控制能力随帧数增加而显著退化。其根本瓶颈在于：UNet架构缺乏原生的大规模可扩展性，且运动条件通常以帧间位移偏移量或稠密光流的形式通过额外通道拼接注入，这种方式难以在长时序上保持运动一致性。

Tora 的关键洞察在于：利用3D运动VAE将轨迹压缩至与视频块共享的潜在空间，使得运动条件与视频内容在统一的表示空间中对齐，从而能够利用DiT的可扩展性实现长视频的精确运动控制。这是首次将面向轨迹的运动控制与DiT架构深度集成的尝试。

### 轨迹提取器（TE）

轨迹提取器负责将原始轨迹坐标序列转化为适合DiT块处理的运动条件表示。其处理流程分为三步：

1. **流可视化转换**：将轨迹点序列 $\{(x_i, y_i)\}$ 转换为类似光流的可视化表示，而非直接使用传统的帧间位移偏移量 $u(x_i, y_i)=x_{i+1}-x_i, v(x_i, y_i)=y_{i+1}-y_i$。论文指出，这种逐帧偏移表示不适合DiT的patch化输入机制（Equation 4）。

2. **3D运动VAE压缩**：将流可视化后的轨迹图像序列通过3D运动VAE压缩到与视频VAE潜在空间维度一致的潜在表示。这一设计使得运动条件与视频内容在相同的潜在空间中操作，为后续融合奠定基础。消融实验（Table 2）证实，该压缩方法在轨迹误差（TrajError）和FVD上均显著优于关键帧采样和平均池化等替代方案。

3. **多级特征提取**：通过带有跳跃连接的堆叠卷积层从运动潜在块中提取层次化特征：
   $$f_i = \mathrm{Conv}^i(f_{i-1}) + f_{i-1}$$
   其中 $f_i$ 为第 $i$ 级运动特征，用于注入对应层次的DiT块（Equation 5）。

### 运动引导融合器（MGF）

MGF负责将轨迹提取器输出的多级运动特征注入ST-DiT的去噪过程。论文对比了三种融合设计（Figure 4），最终采用**自适应归一化**（Adaptive Norm）方案：

$$h_i = \gamma_i \cdot h_{i-1} + \beta_i + h_{i-1}$$

其中 $h_{i-1}$ 为前一层的隐藏状态，$\gamma_i$ 和 $\beta_i$ 由运动特征 $f_i$ 通过线性投影生成的缩放和偏移参数（Equation 7）。这种融合方式以残差形式将运动条件平滑注入，既保留了原始DiT的表达能力，又引入了精确的运动引导。

消融实验（Table 3）表明，自适应归一化在TrajError和FVD上均优于额外通道拼接和交叉注意力（$h_i = \mathrm{CrossAttn}([h_{i-1}, f_i]) + h_{i-1}$，Equation 8）等替代方案。

### 训练策略

Tora采用两阶段训练策略（Table 4消融验证其有效性）：

1. **第一阶段**：使用稠密光流作为运动条件进行训练，使模型学习基本的运动遵循能力。
2. **第二阶段**：引入随机稀疏轨迹（1至N条），使模型泛化到用户提供的任意稀疏轨迹输入。

这种“稠密+稀疏”的混合训练策略使TrajError大幅降低，优于单独使用稠密光流或稀疏轨迹的训练方案。

Tora 的整体架构由三个核心组件构成：轨迹提取器（Trajectory Extractor, TE）、时空 DiT（Spatial-Temporal DiT, ST-DiT）以及运动引导融合器（Motion-guidance Fuser, MGF）。其设计目标是将任意用户指定的轨迹编码为与视频块共享潜在空间的时空运动特征，并自适应地注入 DiT 的去噪过程，从而实现对生成视频中物体运动的精确控制。

### 3.1 基础扩散框架

Tora 建立在潜在视频扩散模型（LVDM）之上。给定一个视频的潜在表示 $z_0$，前向扩散过程逐步向其添加高斯噪声，得到噪声潜在状态 $z_t$：

$$z_t = \sqrt{\bar{\alpha}_t} z_0 + \sqrt{1 - \bar{\alpha}_t} \epsilon, \quad \epsilon \sim \mathcal{N}(0, I)$$

模型的训练目标是最小化噪声预测损失：

$$l_{\epsilon} = ||\epsilon - \epsilon_{\theta}(z_t, t, c)||_2^2$$

其中，$\epsilon_{\theta}$ 为去噪网络（在 Tora 中为 ST-DiT）预测的噪声，$c$ 为条件信息（包括文本、图像以及本文引入的轨迹条件）。

### 3.2 时空 DiT（ST-DiT）

Tora 采用时空 DiT 作为基础去噪网络，其结构由空间 DiT 块（S-DiT-B）和时间 DiT 块（T-DiT-B）交替堆叠而成。每个块内部使用标准的自注意力机制，对归一化后的输入令牌 $I_{\mathrm{norm}}$ 进行变换：

$$Q = W_Q \cdot I_{\mathrm{norm}}; \quad K = W_K \cdot I_{\mathrm{norm}}; \quad V = W_V \cdot I_{\mathrm{norm}}$$

这种解耦的时空注意力设计使模型能够分别建模单帧内的空间结构和跨帧的时间动态，为后续运动条件的注入提供了结构基础。

### 3.3 轨迹提取器（TE）

轨迹提取器负责将原始的轨迹坐标序列转化为适合 DiT 处理的时空运动块。传统方法通常直接使用帧间位移偏移量：

$$u(x_i, y_i) = x_{i+1} - x_i; \quad v(x_i, y_i) = y_{i+1} - y_i$$

然而，这种逐点偏移表示缺乏全局时空上下文，且与 DiT 的 patch 化输入模式不兼容。Tora 的解决方案是首先将轨迹渲染为流可视化图像序列，然后通过一个专门设计的 3D 运动 VAE 将其压缩到与视频块相同的潜在空间。该 VAE 能够捕获连续轨迹区间的全局上下文，生成紧凑的运动潜在块。

在此基础上，堆叠的卷积层通过跳跃连接提取多级运动特征：

$$f_i = \mathrm{Conv}^i(f_{i-1}) + f_{i-1}$$

其中 $f_i$ 为第 $i$ 层的运动特征，将被送入对应层级的 MGF 模块。

### 3.4 运动引导融合器（MGF）

MGF 负责将 TE 提取的多级运动特征注入 ST-DiT 的对应块中。Tora 探索了三种融合机制（Figure 4），最终采用性能最优的自适应归一化（Adaptive Norm）方案：

![[assets/figures/papers/paper_list_l5_https_arxiv_org_abs_2407_21705/figures/004_Figure_4.jpg]]
*Figure 4: Different designs of the Motion-guidance Fuser for incorporating trajectory conditioning. Adaptive Norm demonstrates the best performance*

$$h_i = \gamma_i \cdot h_{i-1} + \beta_i + h_{i-1}$$

其中，$h_{i-1}$ 为 DiT 块的隐藏状态，缩放参数 $\gamma_i$ 和偏移参数 $\beta_i$ 由运动特征 $f_i$ 通过线性投影得到。这种融合方式本质上是将轨迹条件转化为对特征通道的仿射变换，使运动引导平滑地调制去噪过程。

作为对比，交叉注意力融合方案将运动特征作为额外的键和值：

$$h_i = \mathrm{CrossAttn}([h_{i-1}, f_i]) + h_{i-1}$$

消融实验（Table 3）表明，自适应归一化在轨迹误差和视频质量（FVD）上均优于通道拼接和交叉注意力方案，验证了仿射变换式融合在运动控制任务中的有效性。

## 实验与关键发现

### 主要定量结果

Tora在128帧运动可控视频生成任务上建立了显著的性能优势，其核心优势体现在运动控制精度与视觉质量两个维度。如Table 1所示，在轨迹误差（Trajectory Error）指标上，Tora仅需11.72，而UNet架构中表现最佳的**MotionCtrl**（Wang et al., SIGGRAPH 2024）为38.39，精度提升约3.3倍（Δ=-26.67）。这一差距在更长帧数下进一步扩大：在128帧设定下，Tora的FVD为494，较MotionCtrl的731降低32.4%，同时较OpenSora-based DragNUWA基线（FVD 565）降低12.6%。

与DiT架构基线的对比揭示了运动模块设计的决定性作用。OpenSora本身不具备运动控制能力，其轨迹误差高达373.17；经DragNUWA方案适配后（OpenSora-based DragNUWA），轨迹误差降至21.75，但仍为Tora（11.72）的近两倍。这表明Tora提出的Trajectory Extractor与Motion-guidance Fuser能够更充分地利用DiT的可扩展性，而非简单地将UNet控制方案迁移至DiT架构。

Table 5的用户研究进一步验证了Tora的感知质量：在指令遵循（Instruction Following）维度上，Tora对CogVideoX、Vidu、Kling的胜率分别为67%、71%、55%；在感官质量（Sensory Quality）上对三者的胜率分别为52%、67%、56%。但需注意，在物理仿真（Physics Simulation）维度上，Tora对Kling的胜率仅为45%，表明在复杂动态模拟上仍有提升空间。

### 消融实验

**轨迹压缩方法（Table 2）**：对比了三种轨迹编码策略——关键帧采样（Key Frame Sampling）、平均池化（Average Pooling）与3D运动VAE。3D VAE在FVD（513）、CLIPSIM（0.2358）和TrajError（14.25）三项指标上均取得最优，验证了定制化压缩网络对保持帧间运动一致性的必要性。关键帧采样因丢失连续运动信息导致轨迹误差显著升高，平均池化则因过度平滑而损害运动精度。

**运动融合模块设计（Table 3）**：在Motion-guidance Fuser中比较了额外通道拼接（Extra Channel Concatenation）、交叉注意力（Cross-Attention）与自适应归一化（Adaptive Norm）三种融合机制。Adaptive Norm在FVD（513）和TrajError（14.25）上均优于其余方案，其设计通过将运动条件转化为缩放参数$\gamma_i$与偏移参数$\beta_i$，以线性投影方式注入DiT块的隐藏状态（公式$h_i = \gamma_i \cdot h_{i-1} + \beta_i + h_{i-1}$），实现了运动引导与内容生成的解耦融合。

**训练策略（Table 4）**：两阶段训练（先稠密光流后随机稀疏轨迹，记为“Hybrid”）在TrajError上显著优于单独使用稠密光流或稀疏轨迹。稠密光流训练为模型提供了精细的运动先验，而稀疏轨迹训练（1~N条随机轨迹）使模型泛化至推理时的任意轨迹输入，二者互补是Tora能够处理多样化轨迹条件的关键。

### 失败模式与局限性

1. **物理仿真差距**：用户研究中Tora对Kling在物理仿真维度的胜率（45%）低于50%，说明在复杂物理交互（如碰撞、弹性形变）的模拟上，Tora仍不及部分商业级视频生成模型。这可能与训练数据中运动场景的多样性有关——自建评估集主要来自视频物体分割数据并经过摄像机运动过滤，偏向于运动较平稳的场景。

2. **光流依赖瓶颈**：轨迹提取和训练高度依赖光流估计精度。在遮挡、快速运动或透明物体等光流失效场景下，轨迹编码可能引入误差，进而影响生成视频的运动控制质量。这一系统性局限在当前框架内尚未得到根本解决。

3. **长视频生成上限**：当前最大生成长度为204帧（约8秒），对于更长时间跨度的视频，模型性能尚未充分验证。随着帧数增加，轨迹误差的累积效应可能加剧，需要额外的架构适应或记忆机制。

### 关键图表结论

- **Figure 5** 展示了Tora在不同分辨率与时长下的轨迹误差变化：Tora在各设定下均保持较低的轨迹误差，且随帧数增加的误差增长斜率明显低于UNet基线，验证了DiT架构在长视频生成中的可扩展性优势。
- **Figure 6** 的定性对比显示，在自行车骑行场景中，Tora准确捕捉了踩踏动作的物理规律，而其他方法出现腿部姿态不自然的问题；在灯笼场景中，DragNUWA导致物体严重变形，MotionCtrl未能正确呈现两个灯笼的数量，Tora则在遵循轨迹的同时保持了物体的结构完整性。
- **Table 3** 与 **Table 2** 共同揭示了Tora设计的两个关键因果节点：自适应归一化融合机制与3D运动VAE压缩，二者分别解决了运动条件“如何注入”与“如何表示”的核心问题，是Tora性能优势的主要来源。

![[assets/figures/papers/paper_list_l5_https_arxiv_org_abs_2407_21705/figures/006_Table_3.jpg]]
*Table 3: Different variants of motion fusion blocks employed in MGF. Adaptive Norm works best*

![[assets/figures/papers/paper_list_l5_https_arxiv_org_abs_2407_21705/figures/007_Figure_5.jpg]]
*Figure 5: Comparison of Trajectory Error across various resolutions and durations*

![[assets/figures/papers/paper_list_l5_https_arxiv_org_abs_2407_21705/figures/008_Table_2.jpg]]
*Table 2: Evaluation of the impact of different trajectory compression methods*

![[assets/figures/papers/paper_list_l5_https_arxiv_org_abs_2407_21705/figures/010_Figure_6.jpg]]
*Figure 6: Qualitative Comparisons on Trajectory Control. In the bicycle scenario, Tora realistically captures pedaling motions, while other methods show legs in an unnatural, nearly horizontal position. In another case, DragNUWA causes significant deformation of the lanterns, and MotionCtrl fails to accurately depict two lanterns. Overall, Tora not only adheres precisely to the specified trajectory but also produces smoother movement that conforms to the physical world*

![[assets/figures/papers/paper_list_l5_https_arxiv_org_abs_2407_21705/figures/005_Table_1.jpg]]
*Table 1: Quantitative comparisons with motion-controllable video generation models. As the number of generated frames increases, Tora’s performance advantage over UNet-based methods becomes more pronounced. Specifically, Tora not only enhances motion fidelity but also improves the visual quality of the foundational model. Comparisons with OpenSora-based DragNUWA highlight the strengths of our proposed motion modules, which integrate seamlessly with DiT’s architecture*

## 定位与知识库关联

### 问题瓶颈：从UNet到DiT的运动控制鸿沟

基于UNet架构的视频扩散模型长期主导可控视频生成，但在运动控制任务上存在结构性瓶颈。**VideoComposer**（Wang et al., NeurIPS 2023）、**DragNUWA**（Yin et al., arXiv 2023）、**AnimateAnything**（Dai et al., arXiv 2023）、**TrailBlazer**（Kurt Ma et al., SIGGRAPH Asia 2024）和**MotionCtrl**（Wang et al., SIGGRAPH 2024）等代表性工作均构建于UNet之上，其运动条件通常以帧间位移偏移量或稠密光流形式直接编码，通过额外通道拼接或线性投影注入去噪网络。然而，UNet在生成长视频时依赖顺序推理逐段扩展帧数，这导致两个致命弱点：一是运动误差随帧数累积放大，二是架构本身缺乏对长时间运动一致性的全局建模能力。

与此同时，扩散Transformer（DiT）凭借可扩展性和长程建模优势，正在取代UNet成为视频生成的新基石。**OpenSora**（Zheng et al., arXiv 2024）作为DiT-based的文本到视频生成模型，验证了DiT架构在视频生成上的潜力，但其原生设计中缺乏运动引导机制，无法支持用户指定的轨迹控制。这一空白构成了Tora工作的核心动机：**如何将精确的运动控制能力无缝嵌入DiT的可扩展架构，使长视频生成既能遵循任意轨迹，又能保持视觉一致性？**

### 方法定位：首个面向轨迹的DiT运动控制框架

Tora是首个将轨迹导向的运动控制引入DiT视频生成范式的工作。其方法定位可从三个关键维度界定：

**1. 架构基座：Spatial-Temporal DiT（ST-DiT）**

Tora继承了DiT的patch化输入和可扩展去噪架构，采用空间DiT块（S-DiT-B）和时间DiT块（T-DiT-B）交替排列的设计。这一基座使Tora天然具备处理长视频帧序列的能力，避免了UNet基线的顺序推理累积误差问题。与OpenSora-based DragNUWA（由本文作者自行适配的DiT运动控制基线）相比，Tora并非简单地将DragNUWA的运动注入方式移植到DiT，而是从运动条件表示到融合机制进行了系统重构。

**2. 运动条件表示：从像素偏移到时空运动块**

传统UNet方法（如MotionCtrl、DragNUWA）将轨迹转化为帧间位移偏移量 $u(x_i, y_i) = x_{i+1} - x_i$ 和 $v(x_i, y_i) = y_{i+1} - y_i$，或通过稠密光流直接编码运动信息。Tora指出这种表示不适合DiT的patch化输入，转而提出**Trajectory Extractor（TE）**，其核心创新在于：

- 将轨迹点序列通过流可视化转换为轨迹图像；
- 使用**3D运动VAE**将轨迹图像压缩到与视频块相同的潜在空间，形成时空运动块（motion patches）；
- 通过堆叠卷积层提取多级运动特征 $f_i = \mathrm{Conv}^i(f_{i-1}) + f_{i-1}$（跳跃连接设计）。

这一设计的本质是将轨迹运动信息“翻译”为DiT去噪网络能够直接理解的时空patch语言，从而在潜在空间中实现运动条件与视频内容的对齐。

**3. 运动条件注入：自适应归一化融合**

传统方法多采用额外通道拼接（如VideoComposer）或交叉注意力（如DragNUWA的部分设计）注入运动条件。Tora提出**Motion-guidance Fuser（MGF）**，通过自适应归一化层将运动特征转化为缩放参数 $\gamma_i$ 和偏移参数 $\beta_i$，与DiT块的隐藏状态融合：$h_i = \gamma_i \cdot h_{i-1} + \beta_i + h_{i-1}$。消融实验（Table 3）证实，这种自适应归一化方案在TrajError和FVD上均优于额外通道拼接和交叉注意力方案，表明运动条件以“调制”而非“拼接”方式注入更契合DiT的归一化层设计范式。

### 训练策略与适用边界

Tora采用**两阶段训练策略**：第一阶段使用稠密光流训练，让模型学习精确的运动-像素对应关系；第二阶段引入随机稀疏轨迹（1至N条），增强模型对任意用户输入轨迹的泛化能力。消融实验（Table 4）表明，这种“稠密+稀疏”的混合训练策略相比单独使用稠密光流或稀疏轨迹，使TrajError大幅降低，验证了分阶段引入运动先验的有效性。

**适用边界**方面，需注意以下约束：

- **训练数据依赖光流精度**：轨迹提取和训练高度依赖光流估计的精度，在遮挡、快速运动或透明物体等场景下，光流误差可能传导至运动控制质量，导致轨迹遵循偏差。
- **运动平稳性偏好**：评估数据集主要来自视频物体分割数据并经过摄像机运动过滤，可能偏向于运动较平稳的场景，对剧烈运动或复杂动态的泛化性能需进一步验证。
- **生成长度上限**：当前最大生成长度为204帧（约8秒），对于更长的视频，其性能尚未充分验证，可能需要额外的架构适应或记忆机制。

### 局限与开放问题

尽管Tora在轨迹控制精度上建立了显著优势（128帧设定下TrajError 11.72 vs MotionCtrl 38.39，FVD 494 vs 731），但仍存在值得关注的局限和开放问题：

**1. 感知质量与物理仿真的权衡**

用户研究（Table 5）显示，Tora在物理仿真方面的胜率低于Kling（45%），表明在感知质量或复杂动态模拟上仍有差距。这暗示当前的轨迹控制机制可能在某些场景下过度约束运动，牺牲了物理真实感。如何在精确轨迹遵循与物理合理性之间取得更优平衡，是后续改进的重要方向。

**2. 极端运动场景的鲁棒性**

遮挡、快速运动、透明物体等场景下光流估计的精度下降，直接影响轨迹提取质量。这一问题并非Tora独有，而是整个基于光流的运动控制范式的共性挑战。可能的解决路径包括引入自监督运动表征或物理模拟器辅助的轨迹标注。

**3. 运动控制维度的扩展**

当前Tora聚焦于2D物体轨迹控制，尚未涉足3D空间轨迹或摄像机轨迹。将轨迹控制扩展至3D空间，或支持物体轨迹与摄像机运动的联合控制，可以显著提升视频制作的灵活性，但需要解决3D运动表征与DiT潜在空间的适配问题。

**4. 数据效率与标注成本**

两阶段训练策略虽然有效，但第一阶段对稠密光流标注的依赖增加了数据准备成本。如何降低对精细光流标注的依赖——例如通过弱监督或自监督运动表征学习——同时保持运动控制效果，是推动方法实用化的关键开放问题。

## 原文 PDF

![[paperPDFs/CVPR_2025/Tora_Trajectory_oriented_Diffusion_Transformer_for_Video_Generation.pdf]]
