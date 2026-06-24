---
title: "Motion Inversion for Video Customization"
type: paper
paper_level: A
venue: SIGGRAPH
year: 2025
pdf_ref: paperPDFs/SIGGRAPH_2025/Motion_Inversion_for_Video_Customization.pdf
aliases:
- MIVC
tags:
- SIGGRAPH_2025
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: "通过可学习的运动查询-键嵌入和运动值嵌入调制时间变压器的自注意力计算，直接控制跨帧的时序关系。"
primary_logic: "设计排除空间维度的1D运动查询-键嵌入以捕获全局时序关系，同时引入带差分运算的2D运动值嵌入以捕获局部动态并消除静态外观偏差。"
claims:
- "运动查询-键嵌入排除空间维度（H和W），避免捕获外观信息。"
- "对运动值嵌入应用差分运算可去除静态外观，保留动态运动。"
- "定量评估显示，本文方法在文本相似度、运动保真度、FID和用户偏好方面均优于所有基线方法。"
- "Video evaluation set (DAVIS, WebVID, online sources) 上 Motion Fidelity = 0.9552"
---

# Motion Inversion for Video Customization

> [!tip] 核心洞察
> 设计排除空间维度的1D运动查询-键嵌入以捕获全局时序关系，同时引入带差分运算的2D运动值嵌入以捕获局部动态并消除静态外观偏差。上述设计构成了本文消除外观纠缠的双重机制（对应 Figure 3）：
1. **查询-键去空间维度**：将 $\mathbf{m}_i^{QK}$ 的 $H$ 和 $W$ 维度压缩为 1，使其在计算注意力图时无法携带物体的形状、纹理等空间外观信息，仅编码“哪些帧之间应产生关联”的时序关系。
2. **值嵌入差分运算**：虽然 $\mathbf{m}_i^{V}$ 保留了空间维度以捕获局部运动模式，但推理时的差分处理剥离了静态背景和物体外观，仅传递帧间变化信号。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 面向视频定制的运动反演 |
| 英文题名 | Motion Inversion for Video Customization |
| 会议/期刊 | SIGGRAPH 2025 |
| Links | [paper](https://arxiv.org/abs/2403.20193); [Project](https://wileewang.github.io/MotionInversion/) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/image_and_video_generation |
| Method | Motion Inversion |
| Dataset | DAVIS, WebVID, 在线视频（Video evaluation set） |

> [!tip] 效果简介
> - Video evaluation set (DAVIS, WebVID, online sources) 上，Motion Fidelity 为 0.9552，变化 best result among compared methods。
> - Video evaluation set (DAVIS, WebVID, online sources) 上，Text Similarity 为 0.3113，变化 best result among compared methods。
> - Video evaluation set (DAVIS, WebVID, online sources) 上，FID 为 550.38，变化 lowest (best) among compared methods。

## 概述

视频定制生成的核心挑战在于从参考视频中提取运动模式并将其可靠地迁移至不同外观的生成对象上。现有方法的根本瓶颈在于缺乏显式且时序解耦的运动表示——运动与外观特征在模型内部高度纠缠，导致跨类别运动迁移时出现外观泄露或运动失真。

本文提出**Motion Inversion**框架，通过可学习的**运动嵌入**直接调制视频扩散模型中时间变压器的自注意力计算，实现对跨帧时序关系的显式控制。其核心洞察是双通道去偏设计：运动查询-键嵌入排除空间维度以捕获全局时序关系，运动值嵌入在推理时通过帧间差分运算消除静态外观偏差，仅保留动态运动信息。这一设计使得运动表示与外观特征在结构层面解耦，从而支持可靠的运动迁移。

在方法谱系中，Motion Inversion属于基于预训练文本到视频扩散模型的运动定制方法，与**DMT**（Yatim et al., CVPR 2024）、**VMC**（Jeong et al., CVPR 2024）及Motion Director等近期工作形成对比。区别于这些方法，本文的关键改动在于将运动控制信号直接注入时间注意力机制，并通过查询-键去空间维度和值嵌入差分两种策略主动消除外观纠缠。

实验结果表明，该方法在运动保真度、文本相似度、FID和用户偏好四项指标上均优于所有对比基线，验证了时序解耦运动表示在视频定制任务中的有效性。

## 背景与动机

视频生成模型的快速发展使得从文本描述生成逼真视频成为可能，但如何在保持生成内容多样性的同时精确控制视频中的运动模式，仍是一个尚未解决的核心挑战。现有方法面临一个根本性瓶颈：**缺乏显式且时序解耦的运动表示**。在标准文本到视频（T2V）扩散模型中，运动信息隐式地编码在时间注意力模块的跨帧交互中，与外观特征深度纠缠。这种耦合导致两个直接后果：其一，从参考视频中提取的运动特征不可避免地携带了源对象的形状、纹理等静态外观信息；其二，将提取到的运动模式迁移至不同对象类别时，外观残留会污染生成结果，导致运动迁移的可靠性显著下降。

现有运动定制方法试图通过不同策略解决这一问题，但各自存在局限。**DMT**（Yatim et al., CVPR 2024）和**VMC**（Jeong et al., CVPR 2024）分别从扩散轨迹匹配和时空特征解耦的角度出发，但均未在运动表示层面建立显式的时序建模机制。**Motion Director**则依赖外部运动信号引导，缺乏对参考视频中运动模式的端到端学习能力。这些方法的共同缺口在于：未能设计一种既充分捕获跨帧时序动态、又系统性地消除外观偏差的运动表示。

本文的核心动机源于一个关键洞察：**时间变压器模块中的自注意力计算天然具备建模帧间关系的能力，但需要一种精心设计的调制信号来引导其聚焦于运动而非外观**。具体而言，影响注意力图的查询-键（Query-Key）交互决定了哪些帧之间建立强关联，而值（Value）聚合则决定了传递到输出特征的具体信息内容。通过在这两个环节分别注入结构化的运动嵌入，可以从机制层面实现对运动模式的解耦控制。

## 核心创新

本文的核心创新在于提出了一种**显式、时序解耦的运动表示**，并配套设计了**双重外观去偏机制**，从而解决了现有视频定制方法中运动与外观特征纠缠的瓶颈问题。

### 1. 可学习的运动嵌入

与现有方法（如 **DMT** (Yatim et al., CVPR 2024)、**VMC** (Jeong et al., CVPR 2024)）直接对模型参数或潜变量进行优化的策略不同，本文引入了一组专门的可学习参数——**运动嵌入 (Motion Embeddings)** $\mathcal{M}$，并将其作为运动信息的唯一载体。这些嵌入被直接注入到预训练文本到视频 (T2V) 扩散模型的时间变压器模块中，通过调制自注意力计算来控制跨帧时序关系，而无需修改预训练模型本身的权重。

运动嵌入由两类互补的组件构成：

- **运动查询-键嵌入 (Motion Query-Key Embedding)** $\mathcal{M}^{QK}$：负责捕获帧间的全局时序关系。
- **运动值嵌入 (Motion Value Embedding)** $\mathcal{M}^{\mathcal{V}}$：负责捕获局部的动态细节。

在训练阶段，给定一段参考视频，这些嵌入从零初始化，仅通过扩散损失反向传播梯度进行更新，优化目标为：

$$\mathcal{M}_* = \arg\min_{\mathcal{M}} \mathbb{E}_{t,\epsilon}\left[\left\|\epsilon_t^{1:N} - \epsilon_\theta(x_t^{1:N}, t, \mathcal{M})\right\|_2^2\right]$$

学习到的嵌入随后在推理阶段被用于生成具有相同运动模式但外观不同的视频。

### 2. 双重外观去偏机制

运动嵌入面临的核心挑战是：直接从视频中学习到的表示不可避免地会编码参考视频中的静态外观信息（如物体形状、纹理），导致运动迁移失败。本文设计了两种针对性策略来消除这一偏差：

**策略一：查询-键嵌入去空间维度。** 运动查询-键嵌入 $\mathbf{m}_i^{QK} \in \mathbb{R}^{1 \times N \times C}$ 的维度设计显式排除了空间维度（$H$ 和 $W$），仅保留时序维度 $N$。由于该嵌入直接影响时间注意力图的计算，排除空间维度意味着注意力图无法捕获帧间物体的形状信息，从而从结构上切断了外观信息进入全局时序关系建模的路径。

**策略二：值嵌入差分运算。** 运动值嵌入 $\mathbf{m}_i^{V} \in \mathbb{R}^{(H \times W) \times N \times C}$ 保留了空间维度以捕获局部运动，但这也使其容易编码静态外观。受光流原理启发，在推理阶段对优化后的运动值嵌入应用帧间差分操作：

$$\tilde{\mathbf{m}}_i^V[:, j, :] = \begin{cases} \mathbf{m}_i^V[:, j, :], & j=1 \\ \mathbf{m}_i^V[:, j, :] - \mathbf{m}_i^V[:, j-1, :], & j>1 \end{cases}$$

当前帧的值嵌入减去前一帧的值嵌入，静态外观分量被抵消，仅保留帧间的动态变化，从而实现了运动与外观的有效解耦。

### 3. 与基线方法的关键差异

| 设计维度 | 基线方法 | 本文方法 |
|:---|:---|:---|
| **时间注意力计算** | 标准自注意力，无运动嵌入 | 通过向 Query/Key 和 Value 添加运动嵌入进行调制 |
| **运动查询-键嵌入维度** | 可能包含空间维度 (2D) | 仅含时序维度 ($1 \times N \times C$)，显式排除 $H$ 和 $W$ |
| **推理时值嵌入处理** | 直接使用学习到的值嵌入 | 应用帧间差分运算，当前帧减去前一帧 |
| **外观偏差消除** | 无显式去偏策略 | 双重策略：查询-键去空间 + 值嵌入差分 |

这两种策略协同工作：查询-键嵌入从注意力机制层面阻止外观信息进入全局关系建模，值嵌入差分则从特征层面消除局部运动表示中的静态外观残留。消融实验证实，同时使用两类嵌入并配合差分运算，才能获得最佳的文本-视频相似度和运动保真度。

## 整体框架

![[assets/figures/papers/paper_list_l22_Motion_Inversion_for_Video_Customization/figures/001_Figure_1.jpg]]
*Figure 1: Applications of the proposed Motion Embeddings for customized video generation. Our method supports a wide range of motion types, including various camera movements and object motions. In each example, the first row shows the source video, while the second row shows the output. Please refer to the supplementary videos for clearer visualization*

Motion Inversion 的整体框架围绕一个核心思想展开：将参考视频的运动模式压缩为一组显式的、时序连贯的运动嵌入（Motion Embeddings），并将其注入到预训练文本到视频（T2V）扩散模型的时间变压器模块中，从而在生成过程中调制跨帧的自注意力计算。

### 工作流程

框架分为训练和推理两个阶段，如 Figure 2 所示。

**训练阶段**的目标是从给定的参考视频 $x_0^{1:N}$ 中学习运动嵌入 $\mathcal{M}$。具体而言，运动嵌入被零初始化，并集成到扩散模型的时间变压器模块中。通过标准的扩散损失反向传播梯度，仅更新运动嵌入参数，而预训练模型权重保持冻结。优化目标为最小化噪声预测误差：

$$\mathcal{M}_* = \arg\min_{\mathcal{M}} \mathbb{E}_{t,\epsilon}\left[\left\|\epsilon_t^{1:N} - \epsilon_\theta(x_t^{1:N}, t, \mathcal{M})\right\|_2^2\right]$$

**推理阶段**则利用学习到的运动嵌入来引导生成过程。给定一个描述目标外观的文本提示，运动嵌入被注入到时间变压器中，调制自注意力计算，使生成的视频序列在保留参考运动模式的同时，响应文本描述的外观内容。

### 核心模块与数据流

整个 pipeline 由四个关键模块串联构成：

1. **运动嵌入训练模块**：接收参考视频，通过扩散损失反向传播梯度，学习运动嵌入 $\mathcal{M}$。这是框架的入口，输出一组可复用的运动参数。

2. **运动嵌入注入模块**：将学习到的运动查询-键嵌入 $\mathbf{m}_i^{QK}$ 和运动值嵌入 $\mathbf{m}_i^{V}$ 添加至时间变压器模块的时空特征张量 $\mathbf{F}$ 上，直接调制 Query/Key 和 Value 的计算路径。

3. **时间变压器模块**：作为运动嵌入的作用载体，其标准自注意力计算被修改为：

$$\mathrm{TA}_i(\mathbf{F}) = \mathrm{softmax}\left(\frac{(\mathbf{W}_\mathbf{q}(\mathbf{F} + \mathbf{m}_i^{QK}))(\mathbf{W}_\mathbf{k}(\mathbf{F} + \mathbf{m}_i^{QK}))^T}{\sqrt{d_k}}\right)(\mathbf{W}_\mathbf{v}(\mathbf{F} + \mathbf{m}_i^{V}))$$

该模块是运动控制的实际执行者，通过调制注意力图（Query-Key）和输出特征（Value）来实现跨帧时序关系的显式控制。

4. **推理去偏模块**：在推理阶段对运动值嵌入应用帧间差分运算，以消除训练过程中可能混入的静态外观信息：

$$\tilde{\mathbf{m}}_i^V[:, j, :] = \begin{cases} \mathbf{m}_i^V[:, j, :], & j=1 \\ \mathbf{m}_i^V[:, j, :] - \mathbf{m}_i^V[:, j-1, :], & j>1 \end{cases}$$

运动查询-键嵌入本身已通过排除空间维度（$1 \times N \times C$，不含 $H$ 和 $W$）来避免捕获外观信息，因此无需额外去偏处理。

### 输入输出规范

- **输入**：一段参考视频（提供运动模式）和一个文本提示（指定目标外观）。
- **输出**：一段定制化视频，其运动轨迹与参考视频一致，视觉内容与文本描述对齐。
- **可复用产物**：训练得到的运动嵌入 $\mathcal{M}$ 可作为“运动资产”保存，后续可搭配任意文本提示进行推理，无需重新训练。

### 关键设计决策

框架的性能瓶颈在于运动与外观的纠缠问题。两个设计决策构成了因果调节的枢纽：其一，运动查询-键嵌入显式排除空间维度（$H$ 和 $W$），使其仅能捕获全局时序关系，从根本上阻断了外观信息的注入路径（Figure 3 左）；其二，运动值嵌入虽保留空间维度以捕获局部动态，但通过推理阶段的差分运算去除静态外观，仅保留帧间变化量（Figure 3 右）。这两个策略协同工作，实现了运动与外观的时序解耦，是方法能够跨对象类别进行可靠运动迁移的核心机制。

## 核心模块与公式推导

### 时间变压器中的自注意力基础

本文方法的核心操作点位于预训练文本到视频（T2V）扩散模型的时间变压器模块。该模块负责建模视频序列的帧间时序关系，其标准自注意力计算为：

$$\mathrm{TA}(\mathbf{F}) = \mathrm{softmax}\left(\frac{\mathbf{Q}\mathbf{K}^{\mathbf{T}}}{\sqrt{d_k}}\right)\mathbf{V}$$

其中 $\mathbf{F} \in \mathbb{R}^{(H \times W) \times N \times C}$ 是输入的特征张量，$H$、$W$ 为空间维度，$N$ 为帧数，$C$ 为通道数。$\mathbf{Q}$、$\mathbf{K}$、$\mathbf{V}$ 分别由 $\mathbf{F}$ 经线性投影得到。此公式定义了帧间注意力权重的计算方式，也是后续运动嵌入注入的基础。

### 运动嵌入的定义与注入

为解决运动与外观特征纠缠的问题，本文引入两类可学习的运动嵌入，统称为 $\mathcal{M}$：

$$\mathcal{M} = \{\mathcal{M}^{QK}, \mathcal{M}^{\mathcal{V}}\}, \quad \mathcal{M}^{QK} = \{\mathbf{m}_1^{QK}, \mathbf{m}_2^{QK}, ..., \mathbf{m}_L^{QK}\}, \quad \mathcal{M}^{\mathcal{V}} = \{\mathbf{m}_1^{V}, \mathbf{m}_2^{V}, ..., \mathbf{m}_L^{V}\}$$

两类嵌入的关键区别在于维度设计：
- **运动查询-键嵌入** $\mathbf{m}_i^{QK} \in \mathbb{R}^{1 \times N \times C}$：显式排除空间维度（$H$ 和 $W$），仅保留时序维度 $N$ 和通道维度 $C$。这一设计使其只能捕获全局时序关系，而无法编码任何空间外观信息。
- **运动值嵌入** $\mathbf{m}_i^{V} \in \mathbb{R}^{(H \times W) \times N \times C}$：保留完整的空间维度，以捕获局部动态细节。

这些嵌入被注入到时间变压器的自注意力计算中，调制后的注意力公式为：

$$\mathrm{TA}_i(\mathbf{F}) = \mathrm{softmax}\left(\frac{(\mathbf{W}_\mathbf{q}(\mathbf{F} + \mathbf{m}_i^{QK}))(\mathbf{W}_\mathbf{k}(\mathbf{F} + \mathbf{m}_i^{QK}))^T}{\sqrt{d_k}}\right)(\mathbf{W}_\mathbf{v}(\mathbf{F} + \mathbf{m}_i^{V}))$$

其中 $\mathbf{W}_\mathbf{q}$、$\mathbf{W}_\mathbf{k}$、$\mathbf{W}_\mathbf{v}$ 为投影矩阵。运动查询-键嵌入同时加在 Query 和 Key 特征上，影响注意力图的生成；运动值嵌入加在 Value 特征上，调制输出特征的时序动态。下标 $i$ 表示第 $i$ 个时间变压器层，每层拥有独立的学习嵌入。

### 训练目标与推理去偏

**训练阶段**，给定一段参考视频 $x_0^{1:N}$，运动嵌入从零初始化，通过标准的扩散损失反向传播梯度进行优化：

$$\mathcal{M}_* = \arg\min_{\mathcal{M}} \mathbb{E}_{t,\epsilon}\left[\left\|\epsilon_t^{1:N} - \epsilon_\theta(x_t^{1:N}, t, \mathcal{M})\right\|_2^2\right]$$

其中 $\epsilon_\theta$ 为噪声预测网络，$t$ 为扩散时间步。梯度仅流向运动嵌入参数，预训练模型权重保持冻结。

**推理阶段**，运动查询-键嵌入因本身已排除空间维度，可直接使用。但运动值嵌入包含空间信息，可能残留静态外观偏差。为此，对优化后的运动值嵌入施加帧间差分运算：

$$\tilde{\mathbf{m}}_i^V[:, j, :] = \begin{cases} \mathbf{m}_i^V[:, j, :], & j=1 \\ \mathbf{m}_i^V[:, j, :] - \mathbf{m}_i^V[:, j-1, :], & j>1 \end{cases}$$

该操作借鉴光流的思想：当前帧减去前一帧的运动值嵌入，静态外观分量被抵消，仅保留帧间的动态变化。第一帧保持不变，作为运动的初始参考。

### 外观去偏的双重设计原理

上述设计构成了本文消除外观纠缠的双重机制（对应 Figure 3）：
1. **查询-键去空间维度**：将 $\mathbf{m}_i^{QK}$ 的 $H$ 和 $W$ 维度压缩为 1，使其在计算注意力图时无法携带物体的形状、纹理等空间外观信息，仅编码“哪些帧之间应产生关联”的时序关系。
2. **值嵌入差分运算**：虽然 $\mathbf{m}_i^{V}$ 保留了空间维度以捕获局部运动模式，但推理时的差分处理剥离了静态背景和物体外观，仅传递帧间变化信号。

消融实验（Figure 6、Figure 7）验证了这一双重设计的必要性：单独使用任一类嵌入均导致文本-视频相似度和运动保真度下降，而去除差分运算同样显著损害生成质量。

## 实验与分析

### 定量评估

本文在包含DAVIS、WebVID及在线来源的视频评估集上，与**DMT**（Yatim et al., CVPR 2024）、**VMC**（Jeong et al., CVPR 2024）及**Motion Director**等基线方法进行了定量比较。所有方法均基于相同的预训练文本到视频模型ZeroScope进行集成与评估，确保实验公平性。

Table 1展示了四项核心指标的对比结果：


![[assets/figures/papers/paper_list_l22_Motion_Inversion_for_Video_Customization/figures/006_Table_1.jpg]]
*Table 1: Quantitatve comparisons with existing methods*

- **运动保真度（Motion Fidelity）**：本文方法达到0.9552，在所有对比方法中取得最优结果。该指标利用轨迹相关性衡量输入与输出视频间的运动一致性，计算公式为：

$$\frac { 1 } { m } \sum _ { \widetilde { \tau } \in \widetilde { \mathcal { T } } } \operatorname* { m a x } _ { \tau \in \mathcal { T } } \mathrm { c o r r } ( \tau , \widetilde { \tau } ) + \frac { 1 } { n } \sum _ { \tau \in \mathcal { T } } \operatorname* { m a x } _ { \widetilde { \tau } \in \widetilde { \mathcal { T } } } \mathrm { c o r r } ( \tau , \widetilde { \tau } )$$

- **文本相似度（Text Similarity）**：本文方法达到0.3113，同样优于所有基线方法，表明生成视频在视觉特征上与文本描述具有更高的对齐度。

- **FID**：本文方法取得550.38的最低值，反映生成视频的视觉质量与分布匹配度最优。

- **用户偏好（User Preference）**：本文方法获得39.35%的最高偏好率，进一步验证了方法的实际感知优势。

定性对比（Figure 5）显示，相较于DMT、VMC和Motion Director，本文方法不仅能更准确地保留原始视频的运动轨迹和物体姿态，还能生成与文本描述高度一致的视觉特征。

### 消融研究

消融实验从两个关键维度验证了设计选择的有效性：

**运动嵌入设计消融**（Figure 6及Figure 7左）：同时使用运动查询-键嵌入（$\mathcal{M}^{QK}$）和运动值嵌入（$\mathcal{M}^V$）可获得最佳的文本-视频相似度和运动保真度。单独使用任一嵌入均导致性能下降，证实两类嵌入在捕获全局时序关系和局部动态信息方面具有互补作用。


![[assets/figures/papers/paper_list_l22_Motion_Inversion_for_Video_Customization/figures/007_Figure_7.jpg]]
*Figure 7: Visual Result of the Ablation Study. Left: Ablation of motion embedding design; Right: Ablation of inference strategy. For better visualization, refer to the videos in the supplementary files*

**推理策略消融**（Figure 6右及Figure 7右）：推理阶段对运动值嵌入应用差分运算显著提升了文本-视频相似度。该操作通过当前帧减去前一帧的运动值嵌入，有效去除了静态外观偏差，仅保留动态运动信息：

$$\tilde{\mathbf{m}}_i^V[:, j, :] = \begin{cases} \mathbf{m}_i^V[:, j, :], & j=1 \\ \mathbf{m}_i^V[:, j, :] - \mathbf{m}_i^V[:, j-1, :], & j>1 \end{cases}$$

消融结果验证了去偏外观设计（1D查询-键嵌入排除空间维度 + 2D值嵌入差分运算）是运动表示纯净性的核心保障。

### 局限性

尽管本文方法在整体运动迁移上表现优异，仍存在以下已知失败模式：

- **实例级运动隔离困难**：当场景中包含多个对象且运动相互干扰时，方法难以完全分离各实例的独立运动，可能导致运动迁移的串扰。

- **模型依赖性**：运动表示高度依赖所使用的基础T2V模型，对模型内部参数的改动较为敏感，跨模型泛化能力有待验证。

以上局限表明，进一步分离实例级运动并降低对特定模型的依赖是未来改进的潜在方向。
## 方法谱系与知识库定位

### 与现有运动定制方法的异同

本文提出的 **Motion Inversion** 方法属于视频扩散模型中基于嵌入学习的运动定制范式，与三类代表性基线方法形成直接对比：

- **DMT** (Yatim et al., CVPR 2024) 和 **VMC** (Jeong et al., CVPR 2024) 同样试图从参考视频中提取运动信息并迁移至文本驱动的视频生成，但两者均未显式设计时序解耦的运动表示。DMT 和 VMC 在运动迁移过程中，运动特征与外观特征存在纠缠，导致跨对象类别迁移时目标对象的视觉属性易被源视频的外观污染。
- **Motion Director**（Zhao et al., 2023）采用不同的运动控制策略，但同样缺乏对运动与外观的解耦机制。

本文的核心差异化在于**显式定义了两种运动嵌入**——运动查询-键嵌入（$\mathcal{M}^{QK}$）和运动值嵌入（$\mathcal{M}^\mathcal{V}$）——并通过结构设计和推理策略主动消除外观偏差。具体而言：

1. **运动查询-键嵌入**的张量形状为 $1 \times N \times C$，显式排除了空间维度（$H$ 和 $W$），使其仅捕获跨帧的全局时序关系，避免编码对象的空间形状信息（Section 3.3, Figure 3 左）。
2. **运动值嵌入**虽保留空间维度（$(H \times W) \times N \times C$）以捕获局部动态，但在推理阶段通过帧间差分运算（Equation 5）减去前一帧的值嵌入，从而去除静态外观分量，仅保留动态运动信息（Section 3.2, Figure 3 右）。

这种“结构去偏 + 运算去偏”的双重设计，使得运动嵌入在训练过程中自然解耦于外观，是区别于所有基线方法的关键因果机制。

### 方法适用边界

**适用场景**：
- 单对象或主导对象的运动定制，包括摄像机运动和物体运动（Figure 1）。
- 运动迁移至不同外观的文本描述对象，生成视觉特征与文本对齐的视频（Figure 4, Figure 5）。
- 可集成至不同的文本到视频（T2V）扩散模型，如 ZeroScope 和 AnimateDiff（Figure 4）。

**不适用或受限场景**：
- **多对象运动干扰**：当前方法难以完全隔离实例级运动，在处理多个对象且运动相互干扰的场景时存在局限性（Section 4.4 Limitations）。
- **模型依赖性**：运动表示高度依赖所使用的基础 T2V 模型，对模型内部参数的改动较为敏感，限制了跨模型的即插即用能力（Section 4.4）。

### 局限与开放问题

**已知局限**：
1. 实例级运动隔离不足，多对象场景下的运动解耦仍是未解决问题。
2. 运动嵌入与特定 T2V 模型绑定，泛化至其他模型架构需重新训练。

**开放问题**：
1. 如何进一步分离实例级运动，以处理多个对象的复杂运动交互？
2. 能否将运动嵌入推广至更广泛的运动类型或更长时序的生成任务？
3. 如何降低运动嵌入对特定 T2V 模型的依赖，实现跨模型的运动迁移？

### 在知识库中的定位

Motion Inversion 在视频生成知识库中的定位可概括为：

- **问题域**：视频运动定制（Video Motion Customization）——从参考视频中提取运动模式并迁移至文本驱动的视频生成。
- **技术路线**：基于预训练 T2V 扩散模型的时间注意力调制，通过可学习的运动嵌入实现时序关系的显式控制。
- **核心贡献**：首次提出通过结构设计（去空间维度）和运算策略（帧间差分）主动消除运动表示中的外观偏差，为运动与外观的解耦提供了可验证的技术方案。
- **证据强度**：定量实验（Table 1）显示，该方法在文本相似度（0.3113）、运动保真度（0.9552）、FID（550.38）和用户偏好（39.35%）四项指标上均优于所有对比基线；消融实验（Figure 6, Figure 7）进一步验证了双重去偏设计的必要性。

## 原文 PDF

![[paperPDFs/SIGGRAPH_2025/Motion_Inversion_for_Video_Customization.pdf]]
