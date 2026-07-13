---
title: "HOP: Heterogeneous Topology-based Multimodal Entanglement for Co-Speech Gesture Generation"
type: paper
paper_level: A
venue: CVPR
year: 2025
pdf_ref: paperPDFs/CVPR_2025/HOP_Heterogeneous_Topology_based_Multimodal_Entanglement_for_Co_Speech_Gesture_Generation.pdf
project_link: https://star-uu-wang.github.io/HOP/
code_link: null
aliases:
- HOP
tags:
- CVPR_2025
- topic/generative_models_diffusion
- topic/benchmarks_datasets_evaluation
- topic/generative_models_diffusion/diffusion_image_video
core_operator: 以音频节奏为桥梁，显式构建文本-音频-动作的拓扑纠缠关系，使各模态相互适应并驱动协调的手势生成。
primary_logic: 音频信号天然编码了手势的节奏特征和文本的语义信息，可作为跨模态对齐的核心中介；通过重编程（reprogramming）和时空图建模，能够有效捕获异构多模态之间的深层次纠缠，从而生成更自然、富有表现力的协同语音手势。
claims:
- HOP在TED Gesture和TED Expressive数据集上的FGD、BC、Diversity均达到最优性能（Table 1）。
- 用户研究表明HOP在自然性、流畅性、语义一致性和同步性四个方面获得最高MOS评分（Table 2）。
- 去除时空图编码器或重编程层均导致所有指标明显下降（Table 5），验证了拓扑纠缠设计的有效性。
- HOP在不同训练数据比例下始终优于Trimodal基线，且性能下降更平缓（Table 3），表明模型具备更好的数据效率和鲁棒性。
---

# HOP: Heterogeneous Topology-based Multimodal Entanglement for Co-Speech Gesture Generation

> [!tip] 核心洞察
> 音频信号天然编码了手势的节奏特征和文本的语义信息，可作为跨模态对齐的核心中介；通过重编程（reprogramming）和时空图建模，能够有效捕获异构多模态之间的深层次纠缠，从而生成更自然、富有表现力的协同语音手势。

| 字段 | 内容 |
|------|------|
| 中文题名 | HOP：基于异构拓扑的多模态纠缠用于协同语音手势生成 |
| 英文题名 | HOP: Heterogeneous Topology-based Multimodal Entanglement for Co-Speech Gesture Generation |
| 会议/期刊 | CVPR 2025 |
| Links | [Project](https://star-uu-wang.github.io/HOP/) |
| Topic | #topic/generative_models_diffusion #topic/benchmarks_datasets_evaluation #topic/generative_models_diffusion/diffusion_image_video |
| Method | HOP |
| Dataset | TED Gesture, TED Expressive, User Study |

> [!tip] 效果简介
> - TED Gesture 上，FGD 1.406 vs SOTA (Trimodal ≈ 3.73) (显著降低)；BC 0.762 vs SOTA (提升)；Diversity 108.176 vs SOTA (提升)。
> - TED Expressive 上，FGD 1.815 vs SOTA (显著降低)；BC 0.738 vs SOTA (提升)；Diversity 183.332 vs SOTA (提升)。
> - User Study 上，MOS Naturalness 3.92 vs N/A (N/A)。

## 概要

协同语音手势生成（Co-Speech Gesture Generation）旨在根据说话人的语音和文本内容，自动合成与之同步、语义一致且自然流畅的肢体动作。该任务的核心挑战在于：文本、音频、动作三种模态之间存在显著的异构性——文本承载语义，音频编码节奏与韵律，动作则表现为连续的人体关节运动。现有方法大多假设这些模态相互独立，采用先独立编码再简单融合（如拼接或加和）的策略，缺乏对跨模态交互的显式建模，导致生成手势的多样性和连贯性不足。

针对上述瓶颈，本文提出 **HOP**（**H**eterogeneous T**op**ology-based Multimodal Entanglement），一种基于异构拓扑的多模态纠缠框架。其核心洞察在于：**音频信号天然编码了手势的节奏特征和文本的语义信息，可作为跨模态对齐的核心中介**。HOP 以音频为桥梁，显式构建文本-音频-动作三者之间的拓扑纠缠关系：通过**重编程（Reprogramming）** 机制将音频节奏信息注入预训练语言模型的输入空间，实现音频与文本语义的对齐；通过**时空图网络（Graph-WaveNet）** 捕获音频节奏与肢体运动之间的时空依赖。这种“拓扑纠缠”设计使各模态相互适应，共同驱动协调、富有表现力的手势生成。

在 TED Gesture 和 TED Expressive 两个公开基准数据集上，HOP 在 Fréchet Gesture Distance（FGD）、Beat Consistency（BC）和 Diversity 三项核心指标上均达到最优性能（Table 1）。用户研究进一步表明，HOP 生成的手势在自然性（MOS 3.92）、流畅性（MOS 3.77）、语义一致性（MOS 4.01）和同步性（MOS 3.86）四个维度上均获得最高主观评分（Table 2）。消融实验证实，移除时空图编码器或重编程层均会导致所有指标的显著退化（Table 5），验证了拓扑纠缠设计的有效性。此外，渐进学习实验显示 HOP 在训练数据减半时仍保持较强的学习能力，且始终优于 **Trimodal Context**（Yoon et al., ACM TOG 2020）等基线方法，表明其具备更好的数据效率和鲁棒性（Table 3）。

协同语音手势（co-speech gesture）是人类交流中自然伴随言语的肢体动作，承载着语义强调、情感表达和节奏同步等关键交际功能。在虚拟人、具身智能体等应用中，生成与语音自然匹配的手势序列对于提升交互沉浸感至关重要。

### 现有方法及其瓶颈

当前主流的手势生成方法通常将文本、音频和说话人身份等多模态输入视为彼此独立的信号源，各模态经独立编码后通过简单拼接或加和进行融合，例如 **Trimodal Context**（Yoon et al., ACM TOG 2020）和 **DiffuseStyleGesture**（Yang et al., 2023）。这类范式隐含了一个强假设：多模态信息是相互独立的，融合仅需在特征层面做浅层组合。

然而，这一假设忽略了跨模态之间深层的交互与对齐关系。文本语义、音频节奏和肢体动作之间存在天然的耦合——例如，语音的重音往往伴随手势的节拍性运动，而语义焦点常驱动手势的空间指向。现有方法缺乏对这种跨模态交互的显式建模，导致生成的手势在多样性和时序连贯性上存在明显不足。

### 核心洞察：音频作为跨模态桥梁

HOP 的核心洞察在于：**音频信号天然编码了手势的节奏特征和文本的语义信息，可作为跨模态对齐的中介桥梁**。具体而言：

- 音频的韵律特征（重音、语调、停顿）直接决定了手势的节拍结构（beat gesture）；
- 音频中的语义内容与文本共享词汇信息，为文本-动作的语义对齐提供了纽带；
- 文本与动作之间存在显著的异质性（离散符号 vs. 连续运动），而音频的连续频谱表示恰好可以弥合这一鸿沟。

基于此，HOP 提出以音频节奏为枢纽，显式构建文本-音频-动作三者之间的**拓扑纠缠（topological entanglement）**关系，使各模态在特征空间中相互适应，而非简单堆叠。这一设计通过两个关键机制实现：**重编程（reprogramming）**将音频特征对齐到语言模型的词汇嵌入空间，实现音频-文本的跨模态适应；**时空图网络（Graph-WaveNet）**将动作与音频表示为时空图，通过自适应图卷积和膨胀因果卷积捕获肢体运动与音频节奏的深层耦合。

### 方法定位

HOP 属于显式跨模态对齐驱动的生成式方法，区别于传统的独立编码-简单融合范式。其核心贡献不在于引入全新的生成架构（手势生成器仍基于 GAN），而在于重新设计了多模态特征的交互方式——从“拼接”转向“纠缠”，从而在保持生成质量的同时显著提升了手势的多样性、语义一致性和节奏同步性。

## 核心方法与创新机理

HOP 的核心创新在于**显式建模文本、音频、动作三种异构模态之间的拓扑纠缠关系**，突破了现有方法将多模态输入视为相互独立、仅做简单融合的范式。其关键洞察是：音频信号天然编码了手势的节奏特征和文本的语义信息，可作为跨模态对齐的中介桥梁（Figure 3）。基于此，HOP 引入两项关键机制——**音频-文本重编程**和**音频-动作时空图编码**——使各模态相互适应，驱动协调的手势生成。

### 从独立融合到拓扑纠缠

主流协同语音手势生成方法，如 **Trimodal Context**（Yoon et al., ACM TOG 2020），将文本、音频和说话人身份分别编码后进行拼接或加和融合。这种“独立编码-简单融合”的范式忽略了模态间的深层交互：文本语义与手势动作之间存在显著的异构鸿沟，直接融合难以有效捕获二者之间的对应关系。

HOP 将这一范式转变为**以音频为枢纽的跨模态适应**（cross-modality adaptation）。具体而言，音频表示被用于自适应地调整文本和动作表示：

$$h_{t-aud} = g_{t}(h_{t}, h_{aud}), \quad h_{act-aud} = g_{act}(h_{act}, h_{aud})$$

其中 $h_{t}$、$h_{aud}$、$h_{act}$ 分别为文本、音频、动作的编码表示，$g_t$ 和 $g_{act}$ 为跨模态适应函数（Eq. (2), Sec. 3.1）。适应后的表示 $h_{t-aud}$ 和 $h_{act-aud}$ 与原始音频表示 $h_{aud}$ 共同融合为统一的拓扑纠缠特征 $h_{tme}$（Eq. (3), Sec. 3.1）。这一设计使音频的节奏信息深度嵌入文本语义和动作表示中，实现了三模态的协调纠缠。

### 关键机制一：音频-文本重编程（Reprogramming）

与基线方法使用时序卷积网络（TCN）提取文本特征不同，HOP 采用预训练语言模型 BERT 作为文本编码器，并通过**重编程模块**将音频梅尔频谱映射到语言模型的词汇嵌入空间。这一设计的动机在于：预训练语言模型蕴含丰富的语义先验，但音频与文本属于不同模态空间，直接输入不可行。重编程模块通过多头交叉注意力计算，将时间序列补丁的音频特征对齐到词汇嵌入空间：

$$\hat{w}_{1:T} = \text{Linear}\left(\operatorname{Softmax}\left(\frac{\mathbf{Q}\mathbf{K}^{\top}}{\sqrt{d}}\right)\mathbf{V}\right)$$

$$\mathbf{Z}_{(w,r)}^{(1:T)} = E_{a}(\hat{w}_{1:T}, w_{1:T})$$

其中 $\hat{w}_{1:T}$ 为重编程后的音频特征，$w_{1:T}$ 为原始词汇嵌入（Eq. (4)-(5), Sec. 3.2）。消融实验（Table 5）表明，移除重编程层导致 FGD 从 1.406 升至 1.721，BC 从 0.762 降至 0.755，验证了该模块对音频-文本对齐的关键作用。特征可视化（Figure 4）进一步显示，随着训练推进，重编程后的音频特征与文本特征的相关性逐步增强，呈现明显的对齐趋势。

### 关键机制二：音频-动作时空图编码

对于音频与动作的融合，HOP 采用 **Graph-WaveNet** 风格的时空图编码器。将动作和音频分别表示为时空图，通过自适应图卷积捕获肢体运动的空间依赖，同时利用膨胀因果卷积提取音频中的长程节奏模式。自适应邻接矩阵从可学习的节点嵌入生成：

$$\mathbf{A}_{\text{adapted}} = \operatorname{SoftMax}\left(\operatorname{ReLU}\left(\mathbf{E}_1 \odot \mathbf{E}_2^{\top}\right)\right)$$

图卷积层结合前向、后向转移矩阵和自适应邻接矩阵，融合动作图与音频图的时空信息（Eq. (6)-(7), Sec. 3.3）。膨胀因果卷积以指数级增大感受野，高效捕获音频中的节奏模式（Eq. (8), Sec. 3.3）。消融实验（Table 5）显示，移除时空图编码器导致 FGD 升至 2.026，BC 降至 0.650，Diversity 降至 103.311，严重损害生成质量，表明该模块对于捕获音频-动作的时空纠缠至关重要。

### 创新总结

| 维度 | 基线方法（Trimodal Context 等） | HOP |
|------|-------------------------------|-----|
| 跨模态交互机制 | 各模态独立编码后简单融合（拼接/加和） | 以音频为枢纽的拓扑纠缠：音频-文本通过重编程对齐，音频-动作通过时空图网络融合 |
| 文本特征提取 | 时序卷积网络（TCN） | 预训练语言模型（BERT）+ 重编程模块，将音频信息融入语言模型的输入空间 |
| 核心设计理念 | 模态独立假设 | 异构拓扑纠缠：显式建模跨模态适应关系 |

这两项 changed slots 共同构成了 HOP 的方法论核心，使其在 TED Gesture 和 TED Expressive 数据集上均取得最优的 FGD、BC 和 Diversity 指标（Table 1），并在用户研究中获得最高的自然性、流畅性、语义一致性和同步性评分（Table 2）。

HOP的整体pipeline围绕“音频作为跨模态桥梁”这一核心思想构建。如Figure 2所示，模型接收三种异构输入——文本（$X_t$）、音频（$X_{aud}$）和动作（$X_{act}$）——并分别通过各自的编码器将其映射到隐层表示（Eq. 1）：

$$h_t = f_t(X_t), \quad h_{aud} = f_{aud}(X_{aud}), \quad h_{act} = f_{act}(X_{act})$$

与现有方法（如**Trimodal Context**，Yoon et al., ACM TOG 2020）将三模态独立编码后直接拼接或加和的策略不同，HOP引入了一个显式的跨模态适应阶段。该阶段的核心逻辑是：文本和动作之间存在显著的异构性，但音频天然编码了语音的节奏特征和文本的语义信息，可以作为连接两者的直接媒介（Figure 3）。因此，模型利用音频表示 $h_{aud}$ 分别对文本和动作进行自适应调整（Eq. 2）：

$$h_{t-aud} = g_t(h_t, h_{aud}), \quad h_{act-aud} = g_{act}(h_{act}, h_{aud})$$

经过适应后的文本表示 $h_{t-aud}$ 和动作表示 $h_{act-aud}$ 与原始音频表示 $h_{aud}$ 一同送入拓扑融合模块，形成统一的拓扑纠缠特征 $h_{tme}$（Eq. 3）：

$$h_{tme} = f_{tme}(h_{t-aud}, h_{act-aud}, h_{aud})$$

最终，融合后的多模态特征被输入到基于GAN的手势生成器中，映射为连续的协同语音手势序列。

整个pipeline包含四个关键处理模块：

1. **梅尔频谱提取**：从原始音频中提取梅尔频谱特征，捕获节奏和频率动态，为后续的跨模态对齐提供音频基础表示。

2. **音频-文本重编程模块**：利用多头交叉注意力，将音频梅尔频谱的时间序列补丁“重编程”到预训练语言模型（BERT）的词汇嵌入空间中。具体而言，通过计算重编程后的音频特征 $\hat{w}_{1:T}$（Eq. 5），使其与文本的词汇表示对齐，从而让语言模型能够同时感知音频节奏和文本语义。这一设计解决了音频与文本在特征空间上的异构性，使得语义提取过程能够融入韵律信息。

3. **音频-动作时空图编码器**：将动作和音频分别构建为时空图，采用Graph-WaveNet架构进行融合。该模块通过自适应图卷积（Eq. 7）捕获肢体关节之间的空间依赖关系，同时利用膨胀因果卷积（Eq. 8）以指数级增大的感受野捕获音频中的长程节奏模式。自适应邻接矩阵（Eq. 6）从可学习的节点嵌入中动态生成，无需预定义的人体骨架拓扑，使模型能够自动发现动作数据中的潜在结构特征（Figure 6）。

4. **手势生成器**：基于GAN架构，将拓扑纠缠特征映射为连续手势序列。训练目标（Eq. 9）联合优化四项损失——Huber损失（生成手势与真值的逐帧差异）、风格损失（保持说话人身份一致性）、KL散度（隐空间正则化）和对抗损失——以兼顾生成质量、多样性和身份保真度。

整个框架的信息流可以概括为：音频作为桥梁，通过重编程连接文本语义，通过时空图连接动作节奏，最终在拓扑融合层实现三模态的深度纠缠，驱动协调、富有表现力的手势生成。

![[assets/figures/papers/paper_list_l1859_HOP_Heterogeneous_Topology_based_Multimodal_Entanglement_for_Co_Speech_G/figures/002_Figure_2.jpg]]
*Figure 2: Overview of the proposed framework for multimodal gesture generation with heterogeneous topology entanglement. Given the input text of speech and the Mel-Spectrum obtained through audio preprocessing, we treat audio sequences as a bridge, linking text sequences and action sequences with distinct topologies. For the connection between text and audio, we apply a reprogramming layer to align data from these different modalities, utilizing a language model to extract embedded semantic information. To link action and audio, we employ the Graph-WaveNet approach to separately extract action and audio features. The entangled multimodal representations are then fed into the gesture generator through...*

HOP的整体框架围绕“以音频为桥梁的异构多模态拓扑纠缠”这一核心思想构建。如图2所示，系统接收语音文本与经音频预处理得到的梅尔频谱（Mel-Spectrogram），通过两条并行的跨模态适应路径——音频-文本重编程（Audio-Text Reprogramming）与音频-动作时空图编码（Audio-Action Spatio-Temporal Graph Encoder）——分别实现音频与文本语义、音频与肢体运动节奏的对齐，最终经拓扑融合（Topological Fusion）输入手势生成器（Gesture Generator）。

### 3.1 模态编码与拓扑纠缠框架

HOP显式建模文本、音频、动作三种异构模态之间的拓扑关系。首先，各模态经独立编码器映射至隐空间：

$$h_{t} = f_{t}(X_{t}), \quad h_{aud} = f_{aud}(X_{aud}), \quad h_{act} = f_{act}(X_{act}) \tag{1}$$

其中 $X_t$、$X_{aud}$、$X_{act}$ 分别为文本、音频、动作的原始输入，$h_t$、$h_{aud}$、$h_{act}$ 为对应的隐层表示。随后，以音频表示 $h_{aud}$ 为调节信号，对文本和动作表示进行跨模态适应（cross-modality adaptation）：

$$h_{t-aud} = g_{t}(h_{t}, h_{aud}), \quad h_{act-aud} = g_{act}(h_{act}, h_{aud}) \tag{2}$$

适应后的文本表示 $h_{t-aud}$ 和动作表示 $h_{act-aud}$ 与原始音频表示 $h_{aud}$ 共同进入拓扑融合模块，形成统一的拓扑纠缠特征：

$$h_{tme} = f_{tme}(h_{t-aud}, h_{act-aud}, h_{aud}) \tag{3}$$

这一设计的核心洞察在于：文本与动作之间存在显著的异构性（分别编码语义和运动学信息），而音频天然地同时承载了语义的韵律表达和手势的节奏线索，因此可作为跨模态对齐的中介桥梁（图3）。

### 3.2 音频-文本重编程模块

音频-文本跨模态适应采用“重编程”（Reprogramming）策略，将音频的梅尔频谱特征映射到预训练语言模型（BERT）的词汇嵌入空间，使语言模型能够感知音频中的韵律和节奏信息，从而提取与语音节奏相协调的语义表示。

具体而言，对时间序列补丁（time-series patches），重编程操作定义为：

$$\mathbf{Z}_{(w,r)}^{(1:T)} = E_{a}(\hat{w}_{1:T}, w_{1:T}) \tag{4}$$

其中 $\hat{w}_{1:T}$ 为经多头交叉注意力计算得到的重编程音频特征：

$$\hat{w}_{1:T} = \text{Linear}\left(\operatorname{Softmax}\left(\frac{\mathbf{Q}\mathbf{K}^{\top}}{\sqrt{d}}\right)\mathbf{V}\right) \tag{5}$$

$\mathbf{Q}$ 来自文本词汇嵌入的查询映射，$\mathbf{K}$、$\mathbf{V}$ 来自音频梅尔频谱特征的键值映射，通过缩放点积注意力实现音频到文本空间的软对齐。重编程后的特征与原始词汇嵌入 $w_{1:T}$ 共同进入BERT编码器，输出融合了音频节奏线索的语义表示。

图4的可视化验证了这一机制的有效性：训练前，音频特征相比文本特征噪声较大；经过重编程层后，随着训练推进，音频与文本特征之间的相关性逐渐增强，呈现明显的对齐趋势。

### 3.3 音频-动作时空图编码器

音频-动作跨模态适应采用基于Graph-WaveNet的时空图编码器，将人体姿态序列和音频节奏特征联合建模为时空图结构，以捕获肢体运动的协调模式与音频节拍之间的对应关系。

**自适应邻接矩阵**：为建模人体关节之间非预定义的依赖关系，引入可学习的节点嵌入 $\mathbf{E}_1$、$\mathbf{E}_2$，通过内积与激活函数生成自适应邻接矩阵：

$$\mathbf{A}_{\text{adapted}} = \operatorname{SoftMax}\left(\operatorname{ReLU}\left(\mathbf{E}_1 \odot \mathbf{E}_2^{\top}\right)\right) \tag{6}$$

该矩阵能够从数据中自动发现关节间的潜在关联（如图6所示，某些关节对其他节点表现出强影响力），弥补了预定义骨架拓扑的不足。

**图卷积层**：将动作图 $\mathbf{G}$ 和音频图 $\mathbf{R}$ 拼接后，通过结合前向转移矩阵 $\mathbf{Q}_f^j$、后向转移矩阵 $\mathbf{Q}_b^j$ 和自适应邻接矩阵 $\mathbf{A}_{\text{adapted}}^j$ 的多阶图卷积进行时空特征提取：

$$\mathbf{Z}_{(r,g)}^{(1:T)} = \sum_{j=0}^{J} \mathbf{Q}_{f}^{j} [\mathbf{G},\mathbf{R}]^{(1:T)} \mathbf{W}_{j1} + \mathbf{Q}_{b}^{j} [\mathbf{G},\mathbf{R}]^{(1:T)} \mathbf{W}_{j2} + \mathbf{A}_{\text{adapted}}^{j} [\mathbf{G},\mathbf{R}]^{(1:T)} \mathbf{W}_{j3} \tag{7}$$

其中 $J$ 为图卷积的阶数，$\mathbf{W}_{j1}$、$\mathbf{W}_{j2}$、$\mathbf{W}_{j3}$ 为可学习的权重矩阵。前向和后向转移矩阵分别捕获信息在图中的单向传播模式，自适应邻接矩阵则捕获全局的隐式依赖。

**膨胀因果卷积**：为高效捕获音频中的长程节奏模式，在时域采用膨胀因果卷积：

$$y_{t} = \sum_{i=0}^{K-1} f_{i} \, x_{t-d \cdot i} \tag{8}$$

其中 $d$ 为膨胀因子，$K$ 为卷积核大小。膨胀因果卷积以指数级增大感受野，同时保证时序因果性（不依赖未来信息），使模型能够感知跨越数秒的节奏模式。

### 3.4 手势生成器与训练目标

拓扑融合后的多模态特征 $h_{tme}$ 输入基于生成对抗网络（GAN）的手势生成器，输出连续的手势序列。训练目标由四项损失的加权组合构成：

$$\mathcal{L}_{\text{gesture}} = \alpha \cdot \mathcal{L}_{\text{Huber}}(\mathbf{g}, \hat{\mathbf{g}}) + \beta \cdot \mathcal{L}_{\text{style}}(\mathbf{g}_{id}, \hat{\mathbf{g}}_{id'}) + \gamma \cdot \mathcal{L}_{\text{KLD}} + \lambda \cdot \mathcal{L}_{\text{GAN}} \tag{9}$$

- **$\mathcal{L}_{\text{Huber}}$**：Huber损失，约束生成手势 $\hat{\mathbf{g}}$ 与真实手势 $\mathbf{g}$ 的逐帧一致性，对异常值具有鲁棒性。
- **$\mathcal{L}_{\text{style}}$**：风格损失，通过比较说话人身份 $id$ 对应的真实手势风格与生成手势风格，保持个体运动特质。
- **$\mathcal{L}_{\text{KLD}}$**：KL散度损失，对隐空间分布施加正则化，促进生成多样性。
- **$\mathcal{L}_{\text{GAN}}$**：对抗损失，采用与基线方法一致的对抗训练策略，提升生成手势的真实感。

其中 $\alpha$、$\beta$、$\gamma$、$\lambda$ 为平衡各项损失的超参数。

![[assets/figures/papers/paper_list_l1859_HOP_Heterogeneous_Topology_based_Multimodal_Entanglement_for_Co_Speech_G/figures/011_Figure_6.jpg]]
*Figure 6: The visualization of adaptive adjacency matrix*

## 实验与关键发现

### 主实验结果

HOP在两个公开基准数据集上进行了全面评估：**TED Gesture** 和 **TED Expressive**。评估指标包括Frechet Gesture Distance (FGD，越低越好)、Beat Consistency (BC，越高越好) 和 Diversity（越高越好）。如 Table 1 所示，HOP在所有指标上均达到了最优性能：

![[assets/figures/papers/paper_list_l1859_HOP_Heterogeneous_Topology_based_Multimodal_Entanglement_for_Co_Speech_G/figures/006_Table_1.jpg]]
*Table 1: The Quantitative Results on TED Gesture [49, 50] and TED Expressive [22]. We compare the proposed method [1, 9, 22, 49, 50, 54] based on topological fusion of heterogeneous multimodal learning with recent sota methods and ground truth. Lower FGD is better, higher BC and diversity are better*

- **TED Gesture 数据集**：FGD 达到 1.406，BC 达到 0.762，Diversity 达到 108.176，显著优于 Trimodal 基线（FGD ≈ 3.73）及其他现有方法。
- **TED Expressive 数据集**：FGD 达到 1.815，BC 达到 0.738，Diversity 达到 183.332，同样全面领先。

这些结果表明，基于异构拓扑纠缠的多模态融合策略能够有效提升生成手势的质量和多样性。Figure 8 的定性对比进一步显示，HOP生成的手势在语义对齐和节奏同步方面明显优于基线方法，尤其在手势多样性上表现出显著优势（红色框标注了基线方法中手势数量不足的情况）。

![[assets/figures/papers/paper_list_l1859_HOP_Heterogeneous_Topology_based_Multimodal_Entanglement_for_Co_Speech_G/figures/013_Figure_8.jpg]]
*Figure 8: Visualization of generated gestures. We compared the gesture visualization results on these two datasets with those generated by BASELINE [1, 9, 22, 49, 50, 54]. Additionally, we present the visualization results of gesture diversity on the TED dataset, which clearly demonstrate that our approach significantly outperforms other methods in gesture diversity. Results with an insufficient number of gestures are highlighted with a red box*

### 用户研究

为评估生成手势的感知质量，论文进行了用户研究，从四个维度进行 MOS（1-5分）评分（Table 2）：

| 评估维度 | MOS 评分 |
|---------|---------|
| 自然性 (Naturalness) | 3.92 |
| 流畅性 (Smoothness) | 3.77 |
| 语义一致性 (Semantic) | 4.01 |
| 同步性 (Synchrony) | 3.86 |

HOP在所有四个维度上均获得最高评分，其中语义一致性得分最高（4.01），表明音频-文本重编程模块有效促进了手势与语音语义的对齐。需要注意的是，用户研究的参与规模未在文中公开，MOS评分可能受主观偏差影响，仍需更大规模感知评估进一步验证。

### 消融实验

为验证各核心模块的有效性，论文进行了系统的消融实验：

**文本编码器选择（Table 4）**：对比了不使用语言模型、使用 GPT-2 和使用 BERT 三种配置。结果显示，BERT 作为文本编码器在所有指标上均取得最佳性能（FGD 1.406, BC 0.762, Diversity 108.176），验证了预训练语言模型在提取语义信息方面的优势。

**核心模块消融（Table 5）**：
- **移除时空图编码器（Graph Encoder）**：FGD 上升至 2.026，BC 降至 0.650，Diversity 降至 103.311，性能严重退化。这表明音频-动作的时空图建模对于捕获肢体运动特征和音频节奏特征至关重要。
- **移除重编程层（Reprogramming Layer）**：FGD 升至 1.721，BC 降至 0.755，Diversity 降至 105.360。这验证了音频-文本跨模态适应模块在语义对齐中的关键作用。

两个模块的移除均导致所有指标明显下降，充分证明了拓扑纠缠设计的有效性。

### 数据效率分析

渐进学习实验（Table 3）以10%为步长逐步减少训练数据，观察模型性能变化。结果显示：
- HOP 在不同训练数据比例下始终优于 Trimodal 基线，且性能下降更为平缓。
- 即使仅使用 50% 的训练数据，HOP 仍保持较强的学习效果（FGD 2.709 vs Trimodal 7.364）。

这表明拓扑纠缠设计具有更好的数据效率和鲁棒性，在低资源场景下仍能维持可接受的生成质量。

### 可视化分析

- **重编程效果（Figure 4）**：特征可视化显示，训练前音频特征相比文本特征噪声更大；经过重编程层后，随着训练推进，音频与文本特征的相关性逐渐增加，呈现对齐趋势，验证了跨模态适应的有效性。
- **生成手势可视化（Figure 5）**：HOP生成的手势能更有效地捕捉文本中的语义信息，在高亮区域展现出更大的运动节奏幅度，直观体现了语义与节奏的协同表达。
- **自适应邻接矩阵（Figure 6）**：可视化揭示了动作数据中某些关节对其他节点的强影响，表明模型能够自主学习人体骨骼的潜在结构特征。

![[assets/figures/papers/paper_list_l1859_HOP_Heterogeneous_Topology_based_Multimodal_Entanglement_for_Co_Speech_G/figures/005_Figure_5.jpg]]
*Figure 5: Visualization of generated gestures. The gestures generated by our method more effectively capture the semantic information in the text, exhibiting a greater range of movement rhythm in the highlighted sections. We highlight the text and its corresponding gesture actions using red and yellow shading, respectively*

### 局限性与未验证问题

论文未在正文中明确讨论方法的局限性。从实验设置推断，存在以下待验证问题：
- **场景泛化性**：实验仅基于英文 TED 演讲数据，模型在其它语言（如中文、日语）或不同场景（日常对话、戏剧表演）上的表现尚未验证。
- **计算效率**：重编程和时空图编码器增加了模型复杂度，可能对实时推理造成挑战，但文中未提供推理速度或计算开销的分析。
- **长时间序列一致性**：模型在整场演讲等长时间序列生成中是否存在动作漂移或崩溃现象，仍需进一步研究。

![[assets/figures/papers/paper_list_l1859_HOP_Heterogeneous_Topology_based_Multimodal_Entanglement_for_Co_Speech_G/figures/009_Table_4.jpg]]
*Table 4: Ablation study results of text decoder. We investigate the performance of the proposed method without using a language model, as well as with different language models (including GPT-2 and BERT) as text encoders*

## 定位与知识库关联

### 1. 问题定位：从模态独立到拓扑纠缠

协同语音手势生成（Co-Speech Gesture Generation）的核心挑战在于如何将文本语义、音频节奏和说话人身份等多模态信号融合为自然、连贯的肢体动作序列。现有主流方法存在一个根本性瓶颈：**假设文本、音频、动作等模态相互独立**，各模态经独立编码后仅通过简单的拼接或加和进行融合。这种“浅层融合”范式缺乏对跨模态交互的显式建模，导致生成手势的多样性不足、语义-动作对齐松散、节奏一致性差。

HOP 的切入点正是打破这一假设。其核心洞察在于：**音频信号天然编码了手势的节奏特征和文本的语义信息**（韵律边界、重音、情感强度等），可作为跨模态对齐的天然桥梁。基于此，HOP 提出以音频为中介，显式构建文本-音频-动作三者之间的**拓扑纠缠关系**（topological entanglement），使各模态相互适应而非简单叠加，从而驱动协调的手势生成。

### 2. 与基线方法的关系

#### 2.1 Trimodal Context（Yoon et al., ACM TOG 2020）

**Trimodal Context** 是协同语音手势生成领域的主流三模态融合基线，将文本、音频和说话人身份分别编码后融合。其融合策略本质上是模态拼接或加和，未显式建模模态间的非对称依赖关系。HOP 直接以其为对比对象：在渐进学习实验（Table 3）中，HOP 在不同训练数据比例下始终优于 Trimodal 基线，且性能下降曲线更平缓——当训练数据减至 50% 时，Trimodal 的 FGD 从约 3.73 恶化至 7.36，而 HOP 仅从 1.41 升至 2.71，表明拓扑纠缠设计具备更好的数据效率和鲁棒性。

#### 2.2 DiffuseStyleGesture（Yang et al., arXiv:2305.04919, 2023）

**DiffuseStyleGesture** 代表基于扩散模型的语音驱动手势生成路线。HOP 在 Table 1 中将其列为对比方法之一，在 TED Gesture 和 TED Expressive 两个数据集上的 FGD、BC、Diversity 三项指标均实现超越。值得注意的是，HOP 本身采用 GAN 而非扩散模型作为生成器，这表明其性能优势主要来自前端的跨模态纠缠设计，而非生成范式的差异。

#### 2.3 方法谱系中的位置

从方法演进脉络看，HOP 处于两条技术路线的交汇点：

- **多模态融合路线**：从早期单模态（仅音频）到 Trimodal Context 的三模态拼接，再到 HOP 的非对称拓扑融合，体现了从“模态聚合”到“模态纠缠”的范式升级。
- **时序建模路线**：HOP 的音频-动作跨模态适应模块采用了 **Graph-WaveNet** 架构，将自适应图卷积（空间依赖）与膨胀因果卷积（长程时序依赖）结合。这一选择继承了时空图网络在交通预测、骨架动作识别等领域的成功经验，并将其迁移至音频-手势的跨模态对齐场景。

### 3. 核心设计决策与适用边界

#### 3.1 关键设计决策

| 设计维度 | 基线做法 | HOP 做法 | 效果证据 |
|---------|---------|---------|---------|
| 文本编码器 | 时序卷积网络（TCN） | 预训练 BERT + 音频重编程对齐 | Table 4：BERT 优于 GPT-2 和无语言模型 |
| 跨模态交互 | 拼接/加和 | 音频-文本重编程 + 音频-动作时空图 | Table 5：移除任一模块均显著损害性能 |
| 音频特征 | 原始波形或 MFCC | 梅尔频谱图（Mel-Spectrogram） | 保留节奏和频率动态信息 |

其中最具创新性的是**音频-文本重编程模块**（Reprogramming Module）。该模块通过多头交叉注意力将音频梅尔频谱“重编程”到预训练语言模型（BERT）的词汇嵌入空间，使语言模型能够感知音频的韵律信息（节奏、重音、停顿），从而提取出与语音节奏对齐的语义表示。Figure 4 的特征可视化显示，经过重编程后，音频与文本特征的相关性随训练逐步增强，呈现明显的对齐趋势。

#### 3.2 适用边界

HOP 的设计隐含以下适用前提：

1. **语言-音频-手势的强耦合场景**：适用于演讲、授课等语音、文本和手势高度协同的场景。对于弱耦合场景（如日常闲聊中手势的随意性较高），拓扑纠缠的收益可能减弱。
2. **英文语音环境**：实验仅在 TED 英文演讲数据集上验证，重编程模块依赖的 BERT 为英文预训练模型。多语种场景需重新验证跨语言的重编程有效性。
3. **上半身手势生成**：当前模型聚焦于手臂和手部动作，未涵盖面部表情和躯干运动。

### 4. 局限性与开放问题

#### 4.1 已知局限

1. **泛化能力未验证**：仅在 TED 和 TED-Expressive 两个英文演讲数据集上评测，模型在其它语言（如中文、日语）、其它领域（如日常对话、戏剧表演、采访）上的表现尚不明确。
2. **计算复杂度未分析**：重编程模块（涉及 BERT 前向传播和交叉注意力）和时空图编码器显著增加了模型复杂度，但论文未提供推理速度、参数量或计算开销的定量分析，对实时应用（如虚拟人实时驱动）的可行性存疑。
3. **用户研究规模有限**：MOS 评估参与人数未公开，主观评分可能受样本量限制，仍需更大规模的感知评估以确认人体验层面的优势。
4. **长时间序列一致性未讨论**：模型是否会在长序列生成中出现动作漂移或模式崩溃，论文未涉及。

#### 4.2 开放问题

1. **全身体态扩展**：如何将拓扑纠缠框架从上半身手势扩展到包含面部表情、身体躯干运动的全身体态生成？不同身体部位的动作拓扑结构差异显著，统一建模面临挑战。
2. **跨语言泛化**：重编程模块依赖语言模型的嵌入空间，在多语种、低资源语言上的对齐效果如何？是否需要语言特定的重编程策略？
3. **任务迁移潜力**：音频-文本重编程模块本质上是一种通用的跨模态对齐机制，是否可迁移到其它需要音频-文本对齐的任务（如语音驱动的面部动画生成、音频到表情映射、歌声驱动的舞蹈生成）？
4. **实时推理优化**：能否通过模型蒸馏、重编程层的轻量化设计或图卷积的近似计算，在保持纠缠效果的前提下满足实时推理需求？
5. **生成可控性**：当前模型未提供对生成手势风格（如手势幅度、速度、情感倾向）的显式控制接口，如何在不破坏拓扑纠缠的前提下引入可控性，是走向实际应用的关键一步。

## 原文 PDF

![[paperPDFs/CVPR_2025/HOP_Heterogeneous_Topology_based_Multimodal_Entanglement_for_Co_Speech_Gesture_Generation.pdf]]
