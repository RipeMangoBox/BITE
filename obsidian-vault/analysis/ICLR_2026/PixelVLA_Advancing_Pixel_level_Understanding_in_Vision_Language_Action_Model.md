---
title: "PixelVLA: Advancing Pixel-level Understanding in Vision-Language-Action Model"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/PixelVLA_Advancing_Pixel_level_Understanding_in_Vision_Language_Action_Model.pdf
project_link: https://wenqiliang.github.io/PixelVLA/
code_link: null
openreview_forum_id: 7M6ryCABIc
aliases:
- PixelVLA
tags:
- ICLR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/robotics
core_operator: "在VLA架构中注入像素级理解模块（多尺度像素感知编码器）并引入多模态视觉提示处理能力，配合专门构建的大规模像素标注数据集和两阶段视觉-运动指令微调框架，显著提升空间精准度和操控成功率。"
primary_logic: "通过两阶段自动标注流水线从现有机架数据中生成包含像素级掩码和视觉提示的大规模数据集（Pixel-160K），并设计多尺度像素感知编码器与轻量视觉提示编码器，使VLA能够同时理解像素级空间信息与多类型视觉提示，从而在保持高效率微调的前提下大幅提高操控策略的精度与泛化性。"
claims:
- "PixelVLA在SimplerEnv Google Robot基准上的Visual Matching平均成功率（65.0）较OpenVLA（27.7）提升37.3个百分点，较TraceVLA（42.0）提升23个百分点。"
- "在LIBERO四个任务套件上，PixelVLA微调后平均成功率达到86.7%，位列所有对比方法第一，尤其在Spatial和Long任务套件排名第1。"
- "消融实验中，引入像素级理解增强（+FT+PUE）相比基线提升8.0%，且最终PixelVLA整合所有模块后达到最佳平均分50.1（VA）。"
- "PixelVLA的训练成本仅为OpenVLA预训练成本的1.5%，即可实现显著性能提升。"
---

# PixelVLA: Advancing Pixel-level Understanding in Vision-Language-Action Model

> [!tip] 核心洞察
> 通过两阶段自动标注流水线从现有机架数据中生成包含像素级掩码和视觉提示的大规模数据集（Pixel-160K），并设计多尺度像素感知编码器与轻量视觉提示编码器，使VLA能够同时理解像素级空间信息与多类型视觉提示，从而在保持高效率微调的前提下大幅提高操控策略的精度与泛化性。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | PixelVLA：推进视觉-语言-动作模型中的像素级理解 |
| 英文题名 | PixelVLA: Advancing Pixel-level Understanding in Vision-Language-Action Model |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=7M6ryCABIc) · [Project](https://wenqiliang.github.io/PixelVLA/) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/robotics |
| Method | PixelVLA |
| Dataset | SimplerEnv - Google Robot (VM), SimplerEnv - Google Robot (VA), LIBERO (平均), SimplerEnv - WidowX |

> [!tip] 效果简介
> - SimplerEnv - Google Robot (VM) 上，平均成功率 为 65.0，对比 27.7 (OpenVLA)，变化 +37.3。
> - SimplerEnv - Google Robot (VA) 上，平均成功率 为 52.6，对比 39.8 (OpenVLA)，变化 +12.8。
> - LIBERO (平均) 上，成功率 为 86.7，对比 77.3 (SpatialVLA) / 79.5 (OpenVLA fine-tuned)，变化 +9.4 / +7.2。

## 概要

当前视觉-语言-动作模型（VLAs）在机器人操控中面临一个关键瓶颈：它们仅依赖图像级视觉理解，缺乏对像素级细节的精确感知与空间推理能力，且指令形式局限于纯文本，无法利用更丰富的视觉提示。这严重制约了模型在复杂环境中的泛化性和操控精度。

PixelVLA 针对上述瓶颈提出了一个系统性的解决方案。其核心思路是在 VLA 架构中注入像素级理解能力，并引入多模态视觉提示处理机制。具体而言，PixelVLA 设计了三个关键组件：**多尺度像素感知编码器**，从多级视觉特征和像素掩膜中提取像素级空间嵌入；**视觉提示感知编码器**，将用户提供的点、线、区域、掩膜等视觉提示编码为连续的位置感知嵌入；以及**连续动作解码器**，直接预测 7D 连续动作以降低离散化损失。配合这些模块，作者构建了一个两阶段自动标注流水线，从现有机架数据中生成包含像素掩膜和视觉提示的大规模数据集 **Pixel-160K**（160K episodes / 6.5M 三元组），并通过连续动作训练与像素级理解增强的两阶段微调框架完成训练。

实验结果表明，PixelVLA 在多个基准上取得了显著提升。在 **SimplerEnv Google Robot** 基准上，PixelVLA 的 Visual Matching 平均成功率达到 **65.0**，较 OpenVLA（27.7）提升 **37.3 个百分点**，较 TraceVLA（42.0）提升 23 个百分点。在 **LIBERO** 四个任务套件上，PixelVLA 微调后平均成功率达到 **86.7%**，位列所有对比方法第一，尤其在 Spatial 和 Long 任务套件排名首位。消融实验进一步验证，引入像素级理解增强（PUE）相比基线带来 **8.0%** 的提升，且最终整合所有模块后达到最佳平均分 50.1（VA）。值得注意的是，PixelVLA 的训练成本仅为 OpenVLA 预训练成本的 **1.5%**，即可实现上述性能增益。

当前方法的局限在于仅支持 2D 视觉提示，尚未引入 3D 感知或深度信息，视觉提示类型也限于点、线、区域、掩膜等基本形式。所有验证均在仿真环境中完成，真实机器人部署的效果有待进一步检验。

视觉-语言-动作模型（Vision-Language-Action, VLA）已成为机器人操控策略学习的主流范式。这类模型将视觉观测与语言指令映射为机器人动作，在多种任务中展现出令人瞩目的泛化能力。然而，现有VLA方法存在一个根本性瓶颈：**它们仅依赖图像级（image-level）的全局视觉理解，缺乏对像素级细节的精确感知与空间推理能力**。具体而言，当前VLA模型将整幅图像编码为统一的特征表示，无法区分场景中关键物体、机械臂末端执行器与背景区域的细粒度空间关系。这导致两个直接后果：其一，在需要精密操控的场景中（如抓取特定位置的小物体、避开障碍物），模型的空间定位精度不足；其二，当环境发生视觉扰动（光照变化、背景替换、干扰物引入）时，图像级特征容易受到全局偏移的影响，策略鲁棒性显著下降。

与此同时，现有VLA模型的人机交互方式受限于**纯文本指令**。用户只能通过自然语言描述操控意图，无法利用点、线、区域框、掩膜等更丰富、更直观的视觉提示来精确传达空间目标。这种单一模态的交互范式在复杂场景中尤为受限——例如，当用户需要指定“抓取蓝色杯子右侧的红色方块”时，纯文本描述既冗长又容易产生歧义，而一个简单的视觉标记即可精确传达意图。

针对上述缺口，**PixelVLA**提出了一个核心因果调节变量：在VLA架构中注入像素级理解能力，并赋予模型处理多模态视觉提示的能力。这一设计选择的逻辑链条清晰：像素级空间感知直接提升操控策略的定位精度，而视觉提示支持则大幅扩展人机交互的表达带宽。二者协同作用，使模型在保持高效微调的前提下，显著提升操控成功率与跨环境泛化性。

从证据强度来看，这一动机假设获得了充分的实验支撑。在SimplerEnv Google Robot基准上，PixelVLA的Visual Matching平均成功率达到65.0，较OpenVLA的27.7提升了37.3个百分点（Table 5）；在LIBERO四个任务套件上，PixelVLA微调后平均成功率达86.7%，位列所有对比方法第一（Table 3）。更值得注意的是，PixelVLA的总训练成本仅为OpenVLA预训练成本的1.5%，却实现了如此显著的性能跃升，表明像素级理解模块的引入并非依靠堆砌算力，而是精准地击中了现有VLA架构的能力短板。

综上，PixelVLA的动机根植于一个清晰的因果洞察：**当前VLA模型的性能瓶颈不在于视觉编码器的容量或语言理解的深度，而在于空间感知粒度的缺失与交互模态的单一化**。通过系统性地解决这两个问题，PixelVLA为VLA模型向像素级精确操控的演进提供了可行路径。

## 核心方法与创新机理

PixelVLA 相对于现有 VLA 模型的核心创新在于**三个关键架构槽位的改变**，以及支撑这些改变的**专用数据集与训练框架**。这些改变共同解决了当前 VLA 模型“仅有图像级理解、仅支持文本指令”的根本瓶颈。

### 1. 从图像级特征到像素级空间理解

现有 VLA（如 OpenVLA）仅依赖视觉编码器输出的全局图像特征，缺乏对像素级空间细节的感知能力。PixelVLA 引入了**多尺度像素感知编码器（Multiscale Pixel-aware Encoder）**，该模块接收像素掩膜 $\mathbf{p}^0 \in \mathbb{R}^{H \times W}$ 作为输入，利用多级视觉特征 $\mathbf{f}_p^{0,i}$ 通过加权平均计算像素感知嵌入：

$$\mathbf{E}_p^0 = \mathrm{MLP}\left(\sum_{i=1}^{L} \Gamma^i(\mathbf{f}_p^{0,i})\right), \quad \mathbf{f}_p^{0,i} = \frac{\mathbf{p}^0 \cdot \mathbf{f}_v^{0,i}}{|\mathbf{p}^0|}$$

其中 $\Gamma^i$ 为线性投影层，权重由像素掩膜确定，使得模型能够精确聚焦于操作相关的空间区域。这一设计将像素级空间信息直接注入到 LLM 的 token 嵌入序列中，实现了从“看图”到“看像素”的质变。

### 2. 从纯文本指令到多模态视觉提示

传统 VLA 仅接受文本语言指令 $\mathbf{L}$，限制了人机交互的表达能力和空间指引精度。PixelVLA 新增了**视觉提示感知编码器（Visual Prompt-aware Encoder）**，能够处理点、线、区域、掩膜等多种视觉提示 $\mathbf{V}^0$。该编码器将用户提供的视觉提示转换为连续的位置感知嵌入，并与可学习的提示类型嵌入结合，使模型能够同时理解文本指令和视觉指引。这使得动作似然从 $p(\mathbf{A} | \mathbf{X}, \mathbf{L})$ 扩展为：

$$p(\mathbf{A} | \mathbf{X}, \mathbf{P}, \mathbf{L}, \mathbf{V}) = \prod_{t=1}^{T} p_\theta(\mathbf{a}^t | \mathbf{x}^t, \mathbf{p}^t, \mathbf{L}, \mathbf{V})$$

其中 $\mathbf{P}$ 为像素掩膜序列，$\mathbf{V}$ 为视觉提示。这一改变从根本上拓展了 VLA 的交互范式。

### 3. 从离散动作预测到连续动作解码

现有 VLA 通常将动作离散化为 bins 进行自回归预测，这不可避免地引入离散化损失，损害精细操控精度。PixelVLA 采用**连续动作解码器（Continuous Action Decoder）**，直接基于 LLM 最后一层的隐藏状态，通过线性投影、$N_r$ 个 ResNet 块和 MLP 输出连续的 7 维动作序列。训练使用 L1 回归损失：

$$\mathcal{L}_{\text{PixelVLA}} = \sum_{i=1}^{B} \|\mathbf{a}^i - \mathcal{C}(\mathcal{H}(\mathbf{E}_v^i, \mathbf{E}_l^i, \mathbf{E}_p^i, \mathbf{E}_s^i))\|_1$$

其中 $\mathcal{H}$ 为 LLM 处理函数，$\mathcal{C}$ 为连续动作解码器。这一设计保留了预训练 VLM 的像素级理解能力，同时消除了离散化带来的精度损失。

### 4. 支撑创新的数据与训练基础设施

上述架构创新依赖于两个关键支撑：

- **Pixel-160K 数据集**：通过两阶段自动标注流水线（夹爪感知区域提议 + 多模态物体分割）从现有机架数据中生成，包含 160K 个操作 episode、6.5M 个图像-文本-动作三元组，每个三元组均带有像素掩膜和视觉提示标注。这为像素级监督提供了此前不存在的大规模训练数据。

- **两阶段视觉-运动指令微调框架**：第一阶段（Continuous Action Training）使用 Fractal 和 Bridge v2 数据集的真实机器人演示学习连续动作映射；第二阶段（Pixel-level Understanding Enhancement）在 Pixel-160K 上通过 LoRA 高效微调 LLM 骨干，同时联合训练视觉提示感知编码器和多尺度像素感知编码器。整个训练成本仅为 OpenVLA 预训练成本的 1.5%。

消融实验（Table 4）直接验证了这些创新的因果贡献：仅增加连续动作训练（+CAT）相比基线提升 3.8%（VA），而引入像素级理解增强（+PUE）带来 8.0% 的提升，表明像素级模块是性能增益的主要来源。最终 PixelVLA 全集（CAT+PUE）在 VA 评估中达到 50.1 的平均分，验证了各组件的协同效应。

![[assets/figures/papers/iclr26_0009_7M6ryCABIc_PixelVLA_Advancing_Pixel-level_Understanding_in/figures/002_Figure_2.jpg]]
*Figure 2: Overview of the PixelVLA architecture. The model integrates three novel components: (1) a visual prompt-aware encoder for processing input diverse visual prompts; (2) a multiscale pixelaware encoder that injects pixel-level information into token embeddings; and (3) a continuous action decoder to predict 7D robot actions. PixelVLA enhances fine-grained pixel-level spatial understanding and multimodal prompt responsiveness, enabling more precise manipulation policies in visually complex scenarios*

PixelVLA 的整体设计围绕一个核心瓶颈展开：现有 VLA 模型仅依赖图像级视觉特征和纯文本指令，缺乏对像素级空间细节的感知能力，导致在复杂操控场景中泛化性和精度不足。为解决这一问题，PixelVLA 在标准 VLA 架构中注入了两个关键能力——**像素级理解**和**多模态视觉提示处理**，并通过专门构建的 Pixel-160K 数据集和两阶段微调框架实现高效训练。

### 架构总览

PixelVLA 的架构由五个核心模块串联构成，形成从视觉感知到动作输出的完整流水线：

1. **视觉编码器 (Vision Encoder)**：采用预训练的 DinoV2 和 SigLIP 双骨干网络提取图像特征，经两层 MLP 投影器将视觉嵌入映射到 LLM 的输入空间。
2. **多尺度像素感知编码器 (Multiscale Pixel-aware Encoder)**：接收像素掩膜 $\mathbf{p}^0 \in \mathbb{R}^{H \times W}$ 作为输入，从视觉编码器的多级特征 $\mathbf{F}_{\eta}^{0}$ 中提取像素级信息，通过掩膜加权平均和 MLP 生成像素感知嵌入 $\mathbf{E}_{p}^{0}$。
3. **视觉提示感知编码器 (Visual Prompt-aware Encoder)**：将用户提供的视觉提示（点、线、区域、掩膜）编码为连续的位置感知嵌入，与可学习的提示类型嵌入结合后注入模型。
4. **LLM 骨干 (LLM Backbone)**：基于 Llama 2-7B 的 Prismatic-7B VLM，处理融合了视觉、语言、像素和提示信息的多模态序列，生成隐藏状态。
5. **连续动作解码器 (Continuous Action Decoder)**：从 LLM 最后一层的隐藏状态出发，经过线性投影、$N_r$ 个 ResNet 块和 MLP，直接预测连续的 7 维动作序列，避免了离散化带来的精度损失。

整个前向过程可概括为：视觉特征和像素掩膜经多尺度像素感知编码器生成像素感知嵌入，视觉提示经提示编码器生成位置嵌入，二者与语言指令嵌入共同输入 LLM，最后由连续动作解码器输出动作序列。

### 输入输出流

模型的输入由四部分组成：
- **图像观测** $\mathbf{X}$：来自机器人视角的 RGB 图像序列
- **像素掩膜** $\mathbf{P}$：标注的像素级空间信息
- **语言指令** $\mathbf{L}$：任务描述文本
- **视觉提示** $\mathbf{V}$：用户提供的点、线、区域或掩膜提示

模型输出为连续的 7 维动作序列 $\mathbf{A}$，其条件似然定义为：

$$p ( \mathbf { A } | \mathbf { X } , \mathbf { P } , \mathbf { L } , \mathbf { V } ) = \prod _ { t = 1 } ^ { T } p _ { \theta } ( \mathbf { a } ^ { t } | \mathbf { x } ^ { t } , \mathbf { p } ^ { t } , \mathbf { L } , \mathbf { V } )$$

相比标准 VLA 仅依赖图像和语言的条件似然 $p ( \mathbf { A } | \mathbf { X } , \mathbf { L } )$，PixelVLA 显式引入了像素掩膜 $\mathbf{P}$ 和视觉提示 $\mathbf{V}$ 作为额外条件，这是实现像素级理解和多模态交互的理论基础。

### 训练流水线

PixelVLA 的训练分为两个阶段：

**阶段一：连续动作训练 (Continuous Action Training, CAT)**。在 Fractal 和 Bridge v2 真实机器人数据集上进行，目标是让模型学会从视觉和语言输入直接预测连续动作值。训练使用 L1 回归损失：

$$\mathcal{L}_{PixelVLA} = \sum_{i=1}^{B} \| \mathbf{a}^{i} - \mathcal{C}( \mathcal{H}( \mathbf{E}_{v}^{i}, \mathbf{E}_{l}^{i}, \mathbf{E}_{p}^{i}, \mathbf{E}_{s}^{i} ) ) \|_{1}$$

其中 $\mathcal{H}$ 表示 LLM 的隐藏状态计算，$\mathcal{C}$ 表示连续动作解码器的映射。

**阶段二：像素级理解增强 (Pixel-level Understanding Enhancement, PUE)**。在 Pixel-160K 数据集上使用 LoRA 高效微调 LLM 骨干，同时联合训练视觉提示感知编码器和多尺度像素感知编码器。这一阶段赋予模型像素级空间推理能力和视觉提示响应能力。

### 数据支撑：Pixel-160K 数据集

Pixel-160K 通过两阶段自动标注流水线从现有机架数据生成：
1. **夹爪感知区域提议**：利用 SAM 2 在夹爪闭合帧上生成夹爪掩膜，扩展为边界框作为视觉提示
2. **多模态物体分割**：结合 LLM、Grounding DINO 和 SAM 对操作物体进行分割，生成物体掩膜和视觉提示

最终数据集包含 160K 个操作片段、6.5M 个图像-文本-动作三元组，每个三元组均带有像素掩膜和视觉提示标注。

### 问题形式化

标准VLA将机器人操控建模为给定图像观测序列 $\mathbf{X}$ 和语言指令 $\mathbf{L}$ 下动作序列 $\mathbf{A}$ 的条件生成问题，其似然形式为：

$$p ( \mathbf { A } | \mathbf { X } , \mathbf { L } ) = \prod _ { t = 1 } ^ { T } p _ { \theta } ( \mathbf { a } ^ { t } | \mathbf { x } ^ { t } , \mathbf { L } )$$

其中 $\mathbf{x}^t$ 为第 $t$ 步的RGB图像观测，$\mathbf{a}^t$ 为对应的7自由度末端执行器动作（位置、旋转、夹爪开合），$\theta$ 为模型参数。该范式仅依赖图像级特征，缺乏对像素级空间细节的显式建模。

PixelVLA将像素掩膜 $\mathbf{P}$ 和视觉提示 $\mathbf{V}$ 引入条件生成，扩展后的动作似然为：

$$p ( \mathbf { A } | \mathbf { X } , \mathbf { P } , \mathbf { L } , \mathbf { V } ) = \prod _ { t = 1 } ^ { T } p _ { \theta } ( \mathbf { a } ^ { t } | \mathbf { x } ^ { t } , \mathbf { p } ^ { t } , \mathbf { L } , \mathbf { V } )$$

其中 $\mathbf{p}^t$ 为第 $t$ 步的像素感知掩膜，$\mathbf{V}$ 包含用户提供的点、线、区域、掩膜等多种视觉提示。这一扩展使模型能够同时利用像素级空间信息和多模态提示进行动作预测。

### 多尺度像素感知编码器

多尺度像素感知编码器是PixelVLA的核心创新模块，负责将像素级掩膜转化为可注入LLM的感知嵌入。其计算过程如下：

设视觉编码器（DinoV2 + SigLIP）提取的多级特征图为 $\mathbf{f}_v^{0,i}$（$i=1,\dots,L$，$L$ 为特征层级数），输入的像素感知掩膜为 $\mathbf{p}^0 \in \mathbb{R}^{H \times W}$。首先通过掩膜引导的特征聚合计算各层级的像素感知特征：

$$\mathbf { f } _ { p } ^ { 0 , i } = \frac { \mathbf { p } ^ { 0 } \cdot \mathbf { f } _ { v } ^ { 0 , i } } { | \mathbf { p } ^ { 0 } | }$$

其中 $|\mathbf{p}^0|$ 为掩膜区域面积，用于归一化。该操作实质上是掩膜区域内的空间平均池化，使模型聚焦于操控目标区域的特征。

随后，各层级特征经过独立的线性投影 $\Gamma^i$ 映射到统一维度，求和后由MLP生成最终的像素感知嵌入 $\mathbf{E}_p^0$：

$$\mathbf { E } _ { p } ^ { 0 } = \mathrm { M L P } ( \sum _ { i = 1 } ^ { L } \Gamma ^ { i } ( \mathbf { f } _ { p } ^ { 0 , i } ) )$$

多尺度设计的因果机制在于：浅层特征保留精细的空间定位信息，深层特征编码语义理解，通过掩膜引导的跨层融合，$\mathbf{E}_p^0$ 同时具备“在哪里”和“是什么”的像素级理解能力。

### 视觉提示感知编码器

视觉提示感知编码器采用轻量设计（类似SAM的提示编码器），将用户提供的多样化视觉提示 $\mathbf{V}^0 \in \overline{\mathbb{R}}^{H \times W}$ 转化为连续的位置感知嵌入。具体流程：首先根据提示在图像中的归一化坐标生成连续位置编码，然后与可学习的提示类型嵌入（区分点、线、区域、掩膜等类型）相加，得到最终的视觉提示嵌入 $\mathbf{E}_s^0$。该模块使PixelVLA能够响应比纯文本指令更细粒度的人机交互方式。

### 连续动作解码器

传统VLA通常将动作空间离散化为bin并采用自回归分类预测，这不可避免地引入离散化误差。PixelVLA的连续动作解码器直接以LLM最后一层的隐藏状态为输入，通过线性投影、$N_r$ 个ResNet块和MLP输出连续的7D动作序列。训练采用L1回归损失：

$$\mathcal{L}_{PixelVLA} = \sum_{i=1}^{B} \| \mathbf{a}^{i} - \mathcal{C}( \mathcal{H}( \mathbf{E}_{v}^{i}, \mathbf{E}_{l}^{i}, \mathbf{E}_{p}^{i}, \mathbf{E}_{s}^{i} ) ) \|_{1}$$

其中 $\mathcal{H}$ 表示LLM骨干对视觉嵌入 $\mathbf{E}_v$、语言嵌入 $\mathbf{E}_l$、像素感知嵌入 $\mathbf{E}_p$ 和视觉提示嵌入 $\mathbf{E}_s$ 的融合处理，$\mathcal{C}$ 为连续动作解码器，$\mathbf{a}^i$ 为真值动作，$B$ 为批次大小。该设计保留了预训练VLM的像素级理解能力，同时避免了离散化带来的精细动作细节损失。

### 两阶段视觉-运动指令微调

PixelVLA的训练分为两个阶段：（1）**连续动作训练阶段**（CAT），在Fractal和Bridge v2等真实机器人数据集上使用L1回归学习连续动作映射；（2）**像素级理解增强阶段**（PUE），在Pixel-160K数据集上通过LoRA高效微调LLM骨干，同时联合训练视觉提示感知编码器和多尺度像素感知编码器。消融实验表明，PUE阶段贡献了8.0%的VA平均分提升（相较仅CAT的3.8%提升），验证了像素级模块的主导作用。

## 实验与关键发现

### 瓶颈与核心验证

当前视觉-语言-动作模型（VLA）的根本瓶颈在于图像级视觉处理与纯文本指令的耦合：模型缺乏对像素级细节的精确感知与空间推理能力，无法利用更丰富的视觉提示（点、线、区域、掩膜），这直接制约了在复杂环境中的泛化性和操控精度。PixelVLA 通过三个因果性架构改动——多尺度像素感知编码器、视觉提示感知编码器和连续动作解码器——同时配合大规模像素标注数据集 Pixel-160K 与两阶段视觉-运动指令微调框架，系统性地打破了这一瓶颈。

决定性证据来自三个基准上的跨方法对比：在 SimplerEnv Google Robot 基准上，PixelVLA 的 Visual Matching（VM）平均成功率达到 65.0，较 OpenVLA（27.7）提升 37.3 个百分点，较 TraceVLA（42.0）提升 23 个百分点（Table 5）；在 LIBERO 四个任务套件上，PixelVLA 微调后平均成功率达 86.7%，位列所有对比方法第一，尤其在 Spatial 和 Long 套件排名第 1（Table 3）；消融实验中，引入像素级理解增强（+FT+PUE）相比基线提升 8.0%，最终 PixelVLA 整合所有模块后达到最佳 VA 平均分 50.1（Table 4）。上述提升仅消耗 OpenVLA 预训练成本的 1.5%，验证了架构注入的高效性。

![[assets/figures/papers/iclr26_0009_7M6ryCABIc_PixelVLA_Advancing_Pixel-level_Understanding_in/figures/015_Table_5.jpg]]
*Table 5: SimplerEnv (Li et al. (2024c)) simulation evaluation results in terms of the average success rate for the Google Robot setup. VM denotes Visual Matching and VA is Variant Aggregation. denotes tuning-based methods applied to the pretrained weights of OpenVLA*

![[assets/figures/papers/iclr26_0009_7M6ryCABIc_PixelVLA_Advancing_Pixel-level_Understanding_in/figures/008_Table_3.jpg]]
*Table 3: LIBERO Simulation Benchmark Results. We report the success rates of each method across four task suites. Models including Octo, OpenVLA, TraceVLA, Dita, SpatialVLA and PixelVLA are adapted through fine-tuning. R. represents the success rate ranking in each task suite*

![[assets/figures/papers/iclr26_0009_7M6ryCABIc_PixelVLA_Advancing_Pixel-level_Understanding_in/figures/011_Table_4.jpg]]
*Table 4: Quantitative ablation studies on Variant Aggregation for the Google Robot setup, evaluated in the SimplerEnv simulation environment (Li et al. (2024c))*

### 主结果分析

#### SimplerEnv Google Robot 基准

Table 5 报告了 12 种方法在 Visual Matching 和 Variant Aggregation 两种评估协议下的平均成功率。PixelVLA（基于 OpenVLA 权重微调）在 VM 下取得 65.0，在 VA 下取得 52.6，分别超出 OpenVLA 37.3 和 12.8 个百分点。值得注意的是，PixelVLA-π0（基于 π0 骨干）在 VM 下达到 63.3，验证了像素级理解模块对不同 VLA 骨干的普适性。VA 协议下的消融分析（Table 4）进一步揭示了各模块的独立贡献：仅增加连续动作训练（+FT+CAT）带来 3.8% 的提升，而加入像素级理解增强（+FT+PUE）带来 8.0% 的提升，表明像素感知编码器是性能增益的主要驱动因素。最终 PixelVLA 全集（CAT+PUE）取得 50.1，验证了组件的协同作用。

#### SimplerEnv WidowX 机器人基准

Table 2 展示了 WidowX 机器人上 11 种方法的抓手成功率（Gra.）与任务完成率（Suc.）。PixelVLA-π0 取得平均抓手成功率 55.1、任务完成率 33.8，较 π0 基线的 39.5 和 7.3 分别提升 15.6 和 26.5 个百分点。在 Put Spoon 任务上，PixelVLA 的抓手成功率达到 81.7。这一跨机器人平台的增益表明，像素级理解模块并非对特定硬件的过拟合，而是提供了可迁移的空间精度提升。

![[assets/figures/papers/iclr26_0009_7M6ryCABIc_PixelVLA_Advancing_Pixel-level_Understanding_in/figures/007_Table_2.jpg]]
*Table 2: Evaluation results from the SimplerEnv simulation for the WidowX robot. Gra. denotes the average grasp success rate, and Suc. is the overall task completion success rate*

#### LIBERO 仿真基准

Table 3 对比了 8 种方法在 LIBERO 四个任务套件（Spatial、Object、Goal、Long）上的成功率。PixelVLA 以 86.7 的平均成功率排名第一，在 Spatial 和 Long 套件均位列第 1，在 Goal 套件排名第 2。相比 OpenVLA 微调版（79.5）和 SpatialVLA（77.3），PixelVLA 分别提升 7.2 和 9.4 个百分点。Long 套件对长时序空间记忆要求极高，PixelVLA 在此套件的领先优势直接归因于多尺度像素感知编码器提供的细粒度空间锚定能力。

### 环境鲁棒性

Figure 4 展示了 OpenVLA、TraceVLA 和 PixelVLA 在五种环境变化下的性能对比：相机朝向、光照、背景、干扰物和桌面纹理。PixelVLA 在所有变化条件下均保持显著优势，尤其在引入干扰物和改变桌面纹理时，其成功率下降幅度远小于基线方法。这一鲁棒性来源于两阶段自动标注流水线生成的 Pixel-160K 数据集——该数据集覆盖了多样的视觉场景，使模型在像素级理解增强阶段学习到了对视觉干扰的不变性。

### 消融实验的关键因果链路

Table 4 的消融设计揭示了清晰的因果链路：基线（Baseline）→ 连续动作训练（+FT+CAT）→ 像素级理解增强（+FT+PUE）→ 完整 PixelVLA（+FT+CAT+PUE）。CAT 阶段通过 L1 回归直接预测连续 7D 动作，避免了离散化损失，贡献 3.8% 的 VA 提升；PUE 阶段在 Pixel-160K 上通过 LoRA 微调 LLM 骨干并联合训练视觉提示编码器与多尺度像素感知编码器，贡献 8.0% 的提升。后者的增益约是前者的 2.1 倍，证明像素级空间理解是性能瓶颈的核心解除点。

### 失败模式与局限

尽管 PixelVLA 在仿真基准上表现优异，以下局限需要关注：
- **2D 感知限制**：当前版本仅支持 2D 视觉提示，未引入深度信息或 3D 空间几何推理，在需要精确深度判断的任务中可能存在系统性能上限。
- **视觉提示类型有限**：支持的提示类型限于点、线、区域、掩膜，未扩展至轨迹引导、参考图像提示或位姿条件提示等更复杂形式，限制了人机交互的表达能力。
- **仿真验证缺口**：所有系统验证均在 SimplerEnv 和 LIBERO 仿真环境中完成，尚未在真实机器人上部署验证，sim-to-real 迁移的性能衰减程度需要手动验证。
- **数据多样性依赖**：Pixel-160K 的生成依赖现有开源机器人数据集（Fractal、Bridge v2），其场景多样性受限于源数据分布，可能无法覆盖极端边缘情况。

![[assets/figures/papers/iclr26_0009_7M6ryCABIc_PixelVLA_Advancing_Pixel-level_Understanding_in/figures/013_Figure_6.jpg]]
*Figure 6: The proposed automated annotation pipeline for generating visual prompts and mask annotations at scale for a given robot dataset, consisting of a gripper-aware region proposal stage and a multimodal object segmentation stage*

## 定位与知识库关联

### 1. 方法谱系：从图像级VLA到像素级VLA的演进

PixelVLA的定位是在现有VLA范式上完成一次“感知粒度升级”——将视觉理解从图像级特征推向像素级空间推理。其直接基线与对比对象构成一个清晰的方法谱系：

**直接基线：OpenVLA。** PixelVLA以OpenVLA为架构基础（共享Prismatic-7B VLM骨干与Llama 2-7B LLM），但对其三个关键槽位进行了替换：引入多尺度像素感知编码器替代纯图像级特征输入、引入视觉提示感知编码器替代纯文本指令接口、引入连续动作解码器替代自回归离散动作预测。这种“继承骨干、替换感知与输出模块”的策略使得PixelVLA仅需OpenVLA预训练成本的1.5%即可完成微调，却在SimplerEnv Google Robot基准上实现Visual Matching平均成功率从27.7到65.0的跃升（+37.3个百分点）。

**视觉提示VLA对照：TraceVLA。** TraceVLA代表了另一条技术路线——通过视觉追踪实现空间感知。PixelVLA与之的核心差异在于：TraceVLA关注“物体在哪里移动”，而PixelVLA关注“像素级空间关系是什么”。这一差异在性能上体现为PixelVLA在SimplerEnv Google Robot的VM指标上领先TraceVLA 23个百分点（65.0 vs 42.0），表明像素级掩膜理解比纯追踪信号提供了更丰富的空间约束。

**空间感知VLA对照：SpatialVLA。** SpatialVLA引入了空间感知能力，但在LIBERO基准上平均成功率（77.3）落后PixelVLA（86.7）近9.4个百分点。这表明通用的空间感知增强不足以替代显式的像素级监督信号。

**跨骨干验证：π0。** PixelVLA的架构设计并非仅适用于OpenVLA骨干。论文将像素级理解模块迁移至π0骨干（形成PixelVLA-π0），在SimplerEnv WidowX基准上取得55.1的抓手成功率和33.8的任务成功率，相较π0基线分别提升15.6和26.5个百分点。这一跨骨干验证表明，像素感知编码器+视觉提示编码器+连续动作解码器的组合作为“即插即用”模块具有架构普适性。

**经典基线：RT-1-X与Octo。** 作为机器人策略领域的经典方法，RT-1-X和Octo在LIBERO基准上分别取得65.3和43.7的平均成功率，远低于PixelVLA的86.7。这进一步确认了大规模VLA预训练+像素级微调范式的优势。

### 2. 适用边界与条件约束

PixelVLA的性能增益建立在一系列前提条件之上，脱离这些条件时效果可能显著衰减：

**数据依赖性：Pixel-160K数据集的质量与覆盖范围。** PixelVLA的像素级理解能力完全依赖于Pixel-160K数据集（160K episodes, 6.5M三元组）中的掩膜标注和视觉提示。该数据集通过两阶段自动标注流水线（Gripper-aware Region Proposal + Multimodal Object Segmentation）从开源机器人数据（Fractal、Bridge v2等）生成，因此其场景多样性受限于源数据集的覆盖范围。若目标场景的物体类别、机械臂形态或操作模式与源数据集差异较大，自动标注的质量和像素级理解的迁移效果需要重新验证。

**2D感知的固有局限。** 当前版本仅支持2D视觉提示（点、线、区域、掩膜），不包含深度信息或3D空间几何推理。在需要精确深度估计或多视图融合的任务中（如堆叠、插入等接触密集型操作），2D像素级理解可能不足以提供完整的空间约束。论文明确将此列为限制条件。

**视觉提示类型的覆盖范围。** 尽管PixelVLA支持多种视觉提示类型，但仍限于空间标注类提示（点、线、框、掩膜），未引入轨迹引导、参考图像提示、位姿条件提示等更复杂的提示形式。这限制了其在需要动态路径规划或视觉示例引导的场景中的应用。

**仿真验证的迁移鸿沟。** 所有系统验证均在仿真环境（SimplerEnv、LIBERO）中完成，尚未在真实机器人上部署验证。仿真到真实的迁移（sim-to-real gap）在像素级感知层面可能表现为：真实场景中掩膜分割的噪声、光照变化对视觉提示编码的影响、以及机械臂动力学差异对连续动作解码器输出的扰动。

**计算效率与实时性。** 虽然PixelVLA的训练成本仅为OpenVLA的1.5%，但推理阶段需要额外运行多尺度像素感知编码器和视觉提示编码器，增加了前向传播的计算开销。论文未提供推理延迟数据，在需要高频控制的实时场景中，这一开销可能成为瓶颈。

### 3. 局限性与失效模式分析

基于论文披露的消融实验和限制声明，可识别以下关键失效模式：

**像素级模块的独立贡献与协同依赖。** 消融实验（Table 4）显示，单独引入连续动作训练（CAT）仅提升3.8% VA平均分，而单独引入像素级理解增强（PUE）提升8.0%。最终PixelVLA全集（CAT+PUE）达到50.1的最佳VA平均分。这表明像素级模块是性能提升的主要驱动力，但连续动作解码器与之存在协同效应——若移除连续动作解码而保留像素级编码器，离散化损失可能部分抵消像素级理解带来的精度增益。

**环境扰动下的鲁棒性梯度。** 论文在SimplerEnv Google Robot设置下测试了多种环境变化（相机朝向、光照、背景、干扰物、桌面纹理），但未提供各扰动条件下的定量消融数据。从Figure 4的定性对比可推断，像素级理解对纹理和背景变化的鲁棒性可能优于对光照和相机朝向变化的鲁棒性——因为掩膜生成依赖视觉特征的一致性，而光照剧变可能破坏特征提取的稳定性。

**多任务场景中的注意力分散。** LIBERO的Long任务套件涉及长序列多步骤操作，PixelVLA在该套件排名第1，表明像素级理解有助于维持空间记忆。但若任务涉及大量无关物体（密集场景），像素级编码器可能产生冗余的掩膜嵌入，分散LLM的注意力。论文未测试极端密集场景下的性能退化曲线。

**视觉提示歧义性。** 当用户提供的视觉提示存在歧义（如点击点位于物体边界附近、框选区域包含多个物体）时，轻量视觉提示编码器可能产生模糊的位置嵌入，导致动作解码器输出不稳定的抓取位姿。论文未报告此类边缘案例的失效率。

### 4. 开放问题与未来方向

**3D扩展与多视图融合。** 如何将像素级理解从2D平面扩展至3D空间是多模态VLA的自然演进方向。可能的技术路径包括：引入深度估计分支与像素感知编码器联合训练、利用多视图掩膜一致性约束构建3D感知嵌入、或将神经辐射场（NeRF）类表示集成到VLA框架中。

**更丰富的视觉提示生态。** 当前提示类型可扩展至：轨迹提示（示意运动路径）、参考图像提示（目标状态示例）、力/触觉提示（接触点标注）、以及自然语言+视觉提示的复合指令。这需要构建更大规模、更多样的像素标注数据集，并设计通用的提示融合机制。

**真实世界验证与闭环学习。** 在真实机器人上部署PixelVLA需要解决：实时掩膜生成（可能需要轻量化的SAM变体）、在线视觉提示交互界面、以及基于执行结果的策略修正机制。闭环学习框架（如基于成功/失败信号的在线微调）可能进一步提升真实场景中的鲁棒性。

**大规模预训练的潜力。** PixelVLA目前仅在相对小规模的Pixel-160K上进行微调。若能构建更大规模（百万级episodes）的像素标注机器人数据集，并在多机器人、多任务设定下进行预训练，像素级VLA可能享受到类似于VLM领域的规模化增益。这需要解决跨具身数据对齐和高效标注流水线的工程挑战。

**与基础模型的深度整合。** 当前PixelVLA将像素感知作为“外挂”模块注入冻结的VLM骨干。未来可探索在VLM预训练阶段即引入像素级理解目标（如联合训练掩膜预测与指令跟随），使像素级空间推理成为VLA的原生能力而非微调附加。

## 原文 PDF

![[paperPDFs/ICLR_2026/PixelVLA_Advancing_Pixel_level_Understanding_in_Vision_Language_Action_Model.pdf]]
