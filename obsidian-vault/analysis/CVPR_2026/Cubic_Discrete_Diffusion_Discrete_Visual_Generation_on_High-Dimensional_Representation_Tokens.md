---
title: "Cubic Discrete Diffusion: Discrete Visual Generation on High-Dimensional Representation Tokens"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/Cubic_Discrete_Diffusion_Discrete_Visual_Generation_on_High_Dimensional_Representation_Tokens.pdf
project_link: null
code_link: "https://github.com/YuqingWang1029/CubiD"
aliases:
- CDDC
- CDDDVGHDRT
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/generative_models_diffusion
- topic/representation_self_supervised_transfer
core_operator: 在 h×w×d 张量上执行元素级（per‑element）细粒度掩码与并行预测，打破空间位置和维度的刚性边界，使模型能够从部分观测中捕获多轴依赖关系，并将生成步数固定为 T (<< hwd)，实现与特征维度解耦的高效生成。
primary_logic: 将高维表示令牌视为统一的三维立方体，通过细粒度掩码扩散将不可行的顺序生成转化为固定的并行细化过程，既保留了语义完整性，又使高维离散生成在计算上可行。
claims:
- 元素级掩码 (gFID=5.33) 远优于按维度掩码 (gFID=120.03) 和按空间掩码 (gFID=22.22)，证明细粒度跨轴建模的必要性。
- 可学习掩码令牌 (gFID=5.33) 比随机掩码令牌 (gFID=56.38) 显著更优，验证了掩码表示的适应性设计。
- 逐维量化（DQ）在多模态理解基准上保持连续特征的性能（GQA 63.1 vs 63.2），而向量量化（VQ）显著下降（GQA 54.9），证明 DQ 是保留语义的关键离散化手段。
- 模型规模从 946M 扩展至 3.7B 时生成质量持续提升（gFID 从 5.25 降至 4.68），表明方法具有良好的可伸缩性。
---

# Cubic Discrete Diffusion: Discrete Visual Generation on High-Dimensional Representation Tokens

> [!tip] 核心洞察
> 将高维表示令牌视为统一的三维立方体，通过细粒度掩码扩散将不可行的顺序生成转化为固定的并行细化过程，既保留了语义完整性，又使高维离散生成在计算上可行。

| 字段 | 内容 |
|------|------|
| 中文题名 | Cubic离散扩散：面向高维表示令牌的离散视觉生成 |
| 英文题名 | Cubic Discrete Diffusion: Discrete Visual Generation on High-Dimensional Representation Tokens |
| 会议/期刊 | CVPR 2026 (Highlight) |
| Links | [paper](https://openaccess.thecvf.com/content/CVPR2026/html/Wang_Cubic_Discrete_Diffusion_Discrete_Visual_Generation_on_High-Dimensional_Representation_Tokens_CVPR_2026_paper.html) · [Code](https://github.com/YuqingWang1029/CubiD) |
| Topic | #topic/vision_multimodal_applications #topic/generative_models_diffusion #topic/representation_self_supervised_transfer |
| Method | Cubic Discrete Diffusion (CubiD) |
| Dataset | ImageNet 256×256 class‑conditional generation |

> [!tip] 效果简介
> - ImageNet 256×256 class‑conditional generation 上，gFID (with classifier‑free guidance) 1.88 (CubiD‑XXL) vs 1.95 (VFM‑Tok‑XXL) (-0.07)；gFID (without guidance) 2.02 (CubiD‑XXL) vs 2.04 (CubiD‑XL / VFM‑Tok‑3B) (-0.02)。

## 概要

### 问题背景

离散视觉生成方法近年来取得了显著进展，但其适用范围长期受限于**低维潜在令牌**（通常 8–32 维）。这类低维表示通过向量量化（VQ）将连续特征压缩为紧凑的离散码本，虽利于建模，却不可避免地牺牲了视觉理解和生成所需的语义丰富性。另一方面，现代视觉基础模型（如 DINOv2、SigLIP2）所提取的**高维表示**（768–1024 维）展现出卓越的语义保真度，但将其离散化并直接用于生成面临根本性困难：高维张量 $h \times w \times d$ 产生的令牌空间呈指数级膨胀，自回归建模需要 $O(hwd)$ 步，计算上不可行；而标准离散扩散仅按空间位置掩码，无法捕获维度内部的复杂依赖关系（图 1）。

### 核心方法

本文提出 **Cubic Discrete Diffusion（CubiD）**，一种面向高维离散表示的统一掩码扩散框架。其核心思想是将 $h \times w \times d$ 张量视为一个**三维立方体**，在元素级别执行细粒度掩码与并行预测——任意空间位置的任意维度均可被独立掩码，模型从部分观测中学习跨空间和跨维度的联合依赖。这一设计将不可行的顺序生成转化为**固定 $T$ 步的并行细化过程**，使生成步数与特征维度 $d$ 解耦，首次实现了高维离散令牌（768 维）的原生高效生成。

方法的关键技术环节包括：
- **逐维量化（Dimension-wise Quantization）**：独立处理每一维度，将连续值量化为 $L$ 级离散令牌，在保留语义质量的同时避免向量量化的信息损失（Table 3: SigLIP2-DQ GQA 63.1 vs. VQ 54.9）。
- **元素级掩码**：在 $h \times w \times d$ 张量上随机独立掩码任意元素，打破空间与维度的刚性边界。
- **可学习掩码令牌**：以可训练的 [MASK] 嵌入替代固定或随机噪声，为上下文推理提供适应性表示。
- **截断高斯掩码比率**：从 $\text{TruncNorm}(\mu=1.0, \sigma, [0,1])$ 中采样，偏向高掩码率以强化模型从稀疏观测中重建的能力。

### 主要结果

在 ImageNet 256×256 类条件生成任务上，CubiD 取得了离散生成方法的领先性能：CubiD-XXL（3.7B 参数）在无分类器引导下达到 gFID 2.02，使用引导后降至 **gFID 1.88**，优于同期高维令牌生成方法 VFM-Tok-XXL（gFID 1.95）。消融实验系统验证了设计的有效性：元素级掩码（gFID 5.33）远优于按维度掩码（120.03）和按空间掩码（22.22）；可学习掩码令牌（5.33）显著优于随机掩码（56.38）；模型从 946M 扩展至 3.7B 时生成质量持续提升（gFID 5.25 → 4.68），展现出良好的可伸缩性。

### 方法定位

CubiD 处于**离散扩散生成**与**高维表示学习**的交叉地带。与经典离散扩散方法 **MaskGIT**（Chang et al., CVPR 2022）按空间位置掩码不同，CubiD 将掩码粒度下沉至元素级别；与自回归方法 **VAR**（Tian et al., arXiv 2024）的逐尺度预测不同，CubiD 以固定步数的并行细化替代了顺序生成。相较于 VFM-Tok 等需要重组压缩的高维令牌生成基线，CubiD 是首个**直接以原生高维表示令牌（768d）进行离散生成**的方法，无需降维或空间压缩（Table 5）。



### 离散视觉生成的两条路径

视觉生成模型的核心挑战在于如何将高维、连续的图像信号转化为可建模的离散序列。当前主流范式可归结为两条技术路线：

**低维令牌生成**（Figure 1a）是现有工作的主战场。图像先被压缩为少量空间令牌（通常 $h \times w$ 个），每个令牌由一个低维向量（8–32 维）表示，再通过向量量化（VQ）映射到离散码本。在此设定下，自回归方法（如 VAR, Tian et al., arXiv 2024）沿空间维度逐位置生成，需 $O(hw)$ 步；而离散扩散方法（如 **MaskGIT**, Chang et al., CVPR 2022）通过并行掩码与预测将步数降至 $T < hw$。然而，低维令牌的语义容量受限于其压缩比——压缩越激进，理解与生成所需的细粒度信息丢失越严重。

**高维令牌生成**（Figure 1b）则试图保留预训练编码器（如 DINOv2、SigLIP2）的原生表示能力。这些编码器直接输出 $h \times w \times d$ 的特征张量，其中 $d$ 可达 768–1024 维。问题在于：若将其离散化后沿空间位置逐位置生成，自回归需 $O(hwd)$ 步，计算上不可行；而标准离散扩散仅在空间维度上执行掩码与预测，完全忽略了同一空间位置内部各维度间的依赖关系，导致生成质量严重退化。

### 核心瓶颈：维度灾难与依赖断裂

上述困境的根源在于一个双重瓶颈：

1. **离散化的语义损失**：现有方法普遍采用向量量化（VQ），将整个 $d$ 维向量联合映射到单一码字。当 $d$ 较高时，码本必须覆盖指数级增长的向量空间，导致量化误差急剧上升。实验表明，SigLIP2 特征经 VQ 后在 GQA 基准上从 63.2 骤降至 54.9（Table 3），语义理解能力严重受损。

2. **建模粒度的刚性边界**：低维令牌方法将空间位置视为不可分割的原子单元，掩码与预测仅发生在空间网格上。这一设计在 $d$ 较小时可接受，但当 $d$ 升至数百维时，同一位置的不同维度承载着互补的语义信息，空间级掩码无法捕获维度间的细粒度依赖，导致生成图像出现局部不一致和模糊（Figure 5，中行）。

### CubiD 的核心洞见

CubiD 的出发点是一个直接的观察：**高维表示令牌本质上是一个三维张量，而非二维网格上的向量集合**。将 $h \times w \times d$ 张量视为统一的立方体，允许在任意空间位置、任意维度上进行独立的掩码与预测，就能打破空间与维度的刚性边界。

这一设计带来了三个关键突破：

- **语义保真**：采用逐维量化（Dimension-wise Quantization, DQ），每个维度独立量化为 $L$ 级离散值，避免了 VQ 的联合量化误差。实验证实，SigLIP2-DQ 在多模态理解任务上几乎与连续特征持平（GQA 63.1 vs 63.2，Table 3）。
- **高效生成**：通过细粒度掩码扩散，将不可行的 $O(hwd)$ 顺序生成转化为固定的 $T$ 步并行细化过程（$T \ll hwd$），生成步数与特征维度解耦。
- **跨轴依赖捕获**：元素级掩码迫使模型从部分观测中同时推断空间邻域和维度间的关系，消融实验验证了其决定性作用——元素级掩码的 gFID 为 5.33，而按维度掩码和按空间掩码分别高达 120.03 和 22.22（Table 4b）。

### 与现有工作的定位

CubiD 是首个直接在高维原生表示令牌（768d）上进行离散生成的方法。与此相对，现有离散方法（如 MaskGIT、VAR）均工作在压缩后的低维空间（通常 $\leq 32$ 维），而 VFM-Tok 虽涉及高维令牌但需额外重组压缩步骤。CubiD 在 ImageNet 256×256 上以 768 维离散令牌取得 1.88 gFID（Table 5），证明了高维离散生成在计算和语义上均可行。



## 核心方法与创新机理

CubiD 的核心创新在于将高维表示令牌重新定义为一个统一的 **h×w×d 三维建模空间**，并通过细粒度掩码扩散打破了传统离散生成方法中空间位置与特征维度的刚性边界。以下从瓶颈突破、关键机制和设计决策三个层面展开。

### 1. 瓶颈突破：从低维压缩到高维原生建模

现有离散生成方法（如 **MaskGIT** (Chang et al., CVPR 2022)、**VAR** (Tian et al., arXiv 2024)）普遍依赖向量量化（VQ）将连续特征压缩至 8–32 维的离散令牌，这一过程不可避免地牺牲了语义丰富性——Table 3 显示，VQ 在多模态理解任务上导致 GQA 从 63.2 骤降至 54.9。然而，直接对 768–1024 维的原生高维令牌进行离散建模面临维度灾难：h×w×d 张量产生的令牌空间呈指数级膨胀，自回归需要 O(hwd) 步，标准离散扩散又无法捕获维度内部的复杂依赖（Figure 1b）。

CubiD 的突破在于**直接对高维表示令牌进行生成建模，无需降维压缩**，从而在保留语义完整性的同时使高维离散生成在计算上可行。

### 2. 关键机制：元素级掩码与并行预测

CubiD 的核心操作是将 h×w×d 张量中的**每个元素独立视为可掩码与可预测的基本单元**。这一设计与传统方法的对比体现在三个 changed slots 上：

**掩码粒度的根本转变**（Table 4b）：
- 按维度掩码（per-dim）：掩码某一维度的所有空间位置，gFID = 120.03，几乎完全失败；
- 按空间掩码（per-spatial）：掩码某一位置的所有维度，gFID = 22.22，存在显著局部不一致；
- 元素级掩码（per-element）：独立掩码张量中任意元素，gFID = 5.33，性能跃升一个数量级。

这一消融实验直接验证了论文的核心洞察：高维令牌的空间依赖和维度内依赖必须被**同时、细粒度地建模**。元素级掩码迫使模型从部分观测中学习跨轴上下文推理，而非将空间和维度视为可分离的建模维度。

**掩码令牌表示的可学习性**（Table 4c）：可学习的 [MASK] 嵌入（gFID=5.33）显著优于随机掩码令牌（gFID=56.38），说明掩码位置的表示本身需要适应性地编码“待预测”这一语义，而非简单的零值填充或噪声注入。

**生成步数与维度解耦**：推理从全掩码张量出发，按 cosine schedule 在固定 T 步内逐步解掩码。Table 4d 显示 T=512 时性能趋于饱和（gFID=5.25），这意味着生成复杂度与特征维度 d 无关——这是自回归方法（步数 ∝ hwd）无法实现的效率特性。

### 3. 离散化策略的配套创新：逐维量化

高维原生建模的前提是离散化过程不能破坏语义质量。CubiD 采用**逐维量化（Dimension-wise Quantization, DQ）**替代传统的向量量化：

$$
q_{x,y,i} = \mathrm{Quantize}(z_{x,y,i}; L)
$$

每个维度独立量化为 L 个离散等级。Table 2 表明 DINOv2 在 L=8、SigLIP2 在 L=16 时即可达到与连续特征几乎一致的 rFID。Table 3 进一步验证了 DQ 在多模态理解上的保真度：SigLIP2-DQ 在 GQA 上取得 63.1（连续特征为 63.2），而 SigLIP2-VQ 仅为 54.9。DQ 是使高维离散生成不牺牲语义质量的必要前提。

### 4. 掩码比率分布的设计

掩码比率从截断高斯分布中采样：

$$
r \sim \mathrm{TruncNorm}(\mu = 1.0, \sigma, [0, 1.0])
$$

该分布偏向高掩码率（μ=1.0），迫使模型在极度稀疏的可见上下文中进行推理。Table 4a 显示 σ=0.10 为最优（gFID=5.33），过小（σ=0.01, gFID=5.47）导致训练分布过于集中，过大（σ=0.25, gFID=5.75）则引入过多低掩码率的简单样本，削弱了上下文推理能力的训练强度。

### 5. 规模扩展性

Table 4e 显示模型从 946M 扩展至 3.7B 参数时 gFID 从 5.25 持续降至 4.68，且 Table 4f 表明该方法对编码器选择（DINOv2 vs SigLIP2）具有通用性。这一可伸缩性验证了元素级掩码扩散作为高维离散生成范式的结构合理性。

**局限提示**：当前实验仅覆盖 256×256 分辨率的 class-conditional 生成，更高分辨率或文本到图像场景下的元素级掩码计算开销是否可控，仍需进一步验证。



CubiD 的整体 pipeline 围绕“高维连续表示 → 逐维离散化 → 三维掩码扩散建模 → 迭代解码”这一核心流程构建，旨在打破低维令牌生成对语义丰富性的瓶颈，同时避免高维空间下自回归建模的指数级步数灾难。

### 1. 表示提取：冻结的连续编码器

流程起点是一个**冻结的预训练表示编码器**（Representation Encoder），例如 DINOv2‑B 或 SigLIP2‑B。给定输入图像，编码器输出连续特征图 $z \in \mathbb{R}^{h \times w \times d}$，典型配置为 $h \times w = 16 \times 16$，$d=768$。该编码器在整个训练和推理过程中保持冻结，仅作为语义丰富的特征提取器，使得后续模块能够专注于学习离散令牌的生成分布，而不必从像素端到端地重建语义。

### 2. 离散化：逐维量化（Dimension‑wise Quantization）

连续特征图 $z$ 无法直接用于离散扩散模型，因此 CubiD 引入**逐维量化**（DQ）将其转换为离散令牌。与传统的向量量化（VQ）不同，DQ 独立地处理每个特征维度：对于空间位置 $(x, y)$ 的第 $i$ 个维度，其连续值 $z_{x,y,i}$ 被独立量化为 $L$ 个离散等级之一：

$$q_{x,y,i} = \mathrm{Quantize}(z_{x,y,i}; L)$$

由此得到离散令牌张量 $q \in \{1, 2, \dots, L\}^{h \times w \times d}$。这一设计的因果逻辑在于：VQ 对整个向量联合量化，会严重破坏预训练特征的语义结构，导致多模态理解性能急剧下降（如 SigLIP2‑VQ 在 GQA 上仅 54.9，而连续特征为 63.2）；而 DQ 通过逐维独立量化，几乎完整保留了连续特征的语义质量（SigLIP2‑DQ 在 GQA 上 63.1，与连续特征 63.2 几乎持平），这是后续生成模型能够产出高质量图像的前提（**Table 3**）。

### 3. 掩码扩散建模：三维细粒度掩码与双向 Transformer

这是 CubiD 的核心创新模块。传统离散扩散方法（如 **MaskGIT**，Chang et al., CVPR 2022）仅在空间位置级进行掩码，无法建模高维令牌内部的维度间依赖；而自回归方法（如 **VAR**，Tian et al., arXiv 2024）需要 $O(hwd)$ 步，在高维空间下不可行。CubiD 将 $h \times w \times d$ 张量视为统一的**三维立方体**，执行**元素级（per‑element）掩码**：训练时，每个元素独立且随机地被掩码，掩码比率 $r$ 从截断高斯分布中采样：

$$r \sim \mathrm{TruncNorm}(\mu = 1.0, \sigma, [0, 1.0])$$

该分布偏向高掩码率（$\mu=1.0$），迫使模型从极度稀疏的可见上下文中学习强推理能力。被掩码的位置由**可学习的 [MASK] 嵌入**替代，而非固定零值或随机噪声——消融实验表明，可学习掩码令牌（gFID=5.33）远优于随机掩码令牌（gFID=56.38），验证了掩码表示适应性设计的必要性（**Table 4c**）。

掩码后的张量被展平为 $h \times w$ 个位置序列，每个位置包含 $d$ 维令牌，送入**双向 Transformer** 进行建模。Transformer 通过双向自注意力捕获所有可见令牌之间的空间与维度依赖，其输出通过一个 MLP 头**并行预测所有被掩码位置的全部 $d$ 维令牌类别**。训练目标为交叉熵损失：

$$\mathcal{L} = -\mathbb{E}_{\mathbf{q}, \mathbf{M}} \left[ \sum_{i \in \mathbf{M}} \log p(q_i | \mathbf{q}_{\bar{\mathbf{M}}}) \right]$$

其中 $\mathbf{M}$ 为掩码集合，$\mathbf{q}_{\bar{\mathbf{M}}}$ 为可见令牌。这一设计的关键在于：模型在一次前向传播中同时建模空间位置间的依赖和同一位置内各维度间的依赖，打破了“空间掩码”和“维度掩码”的刚性边界。

### 4. 迭代推理：从全掩码到完整图像的渐进式解掩码

推理过程从**全掩码张量**开始（掩码率 100%），按照 **cosine schedule** 逐步解掩码令牌。每步迭代中，模型并行预测所有当前被掩码位置的令牌值，然后随机选取一个子集进行解掩码，其余位置保持掩码状态进入下一步。这一过程实现了 **coarse‑to‑fine** 的生成：早期步骤建立整体结构，后期步骤细化细节（**Figure 4**）。推理步数固定为 $T$（通常 512 步），与特征维度 $d$ 无关，使得高维离散生成在计算上可行——这从根本上解决了自回归方法 $O(hwd)$ 步的不可行性。

### 5. 模块间的因果依赖与数据流

整个 pipeline 的因果链路可以概括为：**冻结编码器的语义保真度 → 逐维量化的信息保留 → 元素级掩码的跨轴依赖捕获 → 双向 Transformer 的并行预测能力 → 固定步数迭代的生成效率**。其中，逐维量化和元素级掩码是两个最关键的因果节点：前者确保了离散化不丢失语义（**Table 3** 的强证据），后者使得模型能够从部分观测中同时捕获空间和维度的复杂依赖（**Table 4b**：元素级掩码 gFID=5.33，而按维度掩码 gFID=120.03，按空间掩码 gFID=22.22）。两者缺一不可，共同支撑了 CubiD 在高维离散生成任务上的有效性。

### 补充图表

![[assets/figures/papers/cubid_cvpr2026_20260622/figures/003_Figure.jpg]]
*Figure: Figur 3.OverviewofCubicDiscreteDiffusion.(a)HighdimensionalTokenDiscretizationGivenaninputimage,afrozenrepresentationecoderextractscontiuoustokens,whicaretendiscretizedthroughdimension-wisequantizationintoh××ddiscretetoks. (b)TrainngviaDimension-wiseMaskModeling.Duringtraining,werandomlymasktokensacrosbothspatialanddimensioalaxes ofthe ensor(white:maskedtokens,pnk:visiblegroundtruthtokensothercolors:predictedtokens).Theransformerleastopredict these masked tokens fromthe unmaskedcontext,capturing thecomplexdependencies acrossboth spatialand dimensionalaxes*

![[assets/figures/papers/cubid_cvpr2026_20260622/figures/001_Figure_1.jpg]]
*Figure 1: Comparison of discrete visual generation approaches.(a) Low-dimensional token generation:Both methods operate at the spatial level—autoregressive requires h × w sequential steps,while discrete diffusion achieves parallel generation in T\<h ×w iterations.(b)High-dimensional token generation:Autoregressive becomes intractable (h X w X d steps),and standard discrete diffusion cannot model intra-position dependencies. Our Cubic Discrete Diffusion performs fine-grained masking across the entire 3D tensor—any dimension at any position can be masked and predicted independently-enabling effcient generation in T\< h ×w ×d iterations while capturing both spatial and dimensional correlations*



CubiD 将高维表示令牌生成建模为三维张量上的细粒度掩码扩散过程。其核心由三个紧密耦合的模块构成：**逐维量化**将连续特征转化为离散令牌，**三维掩码采样器**在 h×w×d 张量上施加元素级掩码，**双向 Transformer** 从部分观测中并行预测所有被掩码位置。

---

### 3.1 逐维量化（Dimension-wise Quantization）

给定冻结的预训练编码器 E（如 DINOv2-B 或 SigLIP2-B）提取的连续特征图 $z \in \mathbb{R}^{h \times w \times d}$，逐维量化对每个维度独立执行均匀离散化：

$$q_{x,y,i} = \mathrm{Quantize}(z_{x,y,i}; L)$$

其中 $q_{x,y,i} \in \{1, 2, \dots, L\}$ 表示空间位置 $(x, y)$ 处第 $i$ 维的离散令牌，$L$ 为量化级数。与向量量化（VQ）将整个 $d$ 维向量映射到码本中单一索引不同，DQ 在每个维度上独立决策，避免了码本坍塌和语义退化。Table 3 的消融实验证实了这一设计的必要性：SigLIP2-DQ 在多模态理解基准上几乎无损地保持连续特征性能（GQA 63.1 vs 63.2），而 SigLIP2-VQ 出现显著下降（GQA 54.9）。Table 2 进一步表明，DINOv2-B 在 $L=8$、SigLIP2-B 在 $L=16$ 时即可达到与连续特征相当的 rFID 重建质量。

![[assets/figures/papers/cubid_cvpr2026_20260622/figures/011_Table_3.jpg]]
*Table 3: Understanding performance onLLaVA benchmarks with different quantization methods.Evaluation using SigLIP2 features.VQ:vector quantization,DQ:dimension-wise quantization．DQ maintains continuous-level performance while VQ shows significant degradation*

![[assets/figures/papers/cubid_cvpr2026_20260622/figures/008_Table_2.jpg]]
*Table 2: Effect of quantization levels on reconstruction quality. Both encoders achieve continuous-level performance with appropriate quantization levels (L=8 for DINOv2,L=16 for SigLIP2)*

---

### 3.2 三维掩码采样与训练目标

CubiD 的核心操作空间是完整的 $h \times w \times d$ 张量。训练时，采样一个二进制掩码 $\mathbf{M} \in \{0, 1\}^{h \times w \times d}$，其中每个元素独立且随机地被掩码。掩码比率 $r$ 从一个偏向激进掩码的截断高斯分布中采样：

$$r \sim \mathrm{TruncNorm}(\mu = 1.0, \sigma, [0, 1.0])$$

$\mu=1.0$ 意味着分布中心位于全掩码状态，强制模型在极端信息缺失条件下学习强上下文推理能力。Table 4a 的系统消融表明，标准差 $\sigma=0.10$ 达到最优 gFID=5.33：过小的 $\sigma$（0.01，gFID=5.47）导致掩码比率变化不足，过大的 $\sigma$（0.25，gFID=5.75）则使训练分布过于分散。

被掩码位置替换为可学习的 $[\mathrm{MASK}]$ 嵌入。Table 4c 显示，可学习掩码令牌（gFID=5.33）显著优于随机噪声（gFID=56.38），也略优于固定零值（gFID=5.52），验证了自适应掩码表示对上下文建模的关键作用。

训练目标为标准交叉熵损失，模型从可见令牌 $\mathbf{q}_{\overline{\mathbf{M}}}$ 预测被掩码位置 $i \in \mathbf{M}$ 的真实离散类别：

$$\mathcal{L} = -\mathbb{E}_{\mathbf{q}, \mathbf{M}} \left[ \sum_{i \in \mathbf{M}} \log p(q_i | \mathbf{q}_{\overline{\mathbf{M}}}) \right]$$

该损失在 $h \times w \times d$ 个元素上联合优化，迫使 Transformer 同时捕获空间位置间的长程依赖和维度内的跨通道关联。

---

### 3.3 双向 Transformer 架构与并行预测

模型以 $h \times w$ 个空间位置为序列单元，每个位置接收一个 $d$ 维令牌向量。双向自注意力在空间轴上全局建模，使得任意位置的预测可以聚合来自所有其他位置的上下文信息。与自回归方法需要 $O(hwd)$ 步顺序生成不同，CubiD 的 Transformer 通过一个 MLP 头在每一层同时输出所有 $d$ 个维度的类别预测，将生成步数与特征维度解耦。

推理过程从全掩码张量开始，按照 cosine schedule 逐步解掩码。每步迭代中，模型并行预测所有当前被掩码位置的令牌，随后根据置信度随机选择一部分进行解掩码，未被选中的令牌在下一轮继续参与预测。这一 coarse-to-fine 过程在固定的 $T$ 步内完成（典型值 $T=512$），与张量总元素数 $hwd$ 无关。Table 4d 表明，$T=512$ 时性能趋于饱和（gFID=5.25），继续增至 $T=1024$ 仅带来 0.01 的边际收益。

---

### 3.4 掩码粒度的决定性作用

Table 4b 的消融实验揭示了掩码粒度的核心地位。按维度掩码（per-dim：掩码某一维度的所有空间位置）几乎完全失效（gFID=120.03），因为模型无法从其他维度推断被掩码维度的值，维度间依赖完全断裂。按空间掩码（per-spatial：掩码某一位置的所有维度，类似 MaskGIT 的策略）表现稍好但仍不理想（gFID=22.22），因为它忽略了维度内不同通道间的结构关联。只有元素级掩码（per-element：独立掩码 $h \times w \times d$ 中的任意元素）实现了 gFID=5.33，证明高维离散生成必须同时跨空间轴和维度轴进行细粒度建模。Figure 5 的定性对比直观展示了这一差异：per-dim 产生严重纹理伪影，per-spatial 存在局部不一致和模糊，而 per-element 生成清晰连贯的图像。

![[assets/figures/papers/cubid_cvpr2026_20260622/figures/012_Figure_5.jpg]]
*Figure 5: Qualitative comparison of different masking strategies.Top row:Per-dim masking completely fails,producing severe texture-like artifacts.Middle row:Per-spatial masking generates images with significant local inconsistencies and blurry details.Bottom row: Our per-element masking produces clear, coherent images with fine details.The dramatic quality difference validates that high-dimensional tokens require fine-grained masking across both spatial and dimensional axes*

### 补充图表

![[assets/figures/papers/cubid_cvpr2026_20260622/figures/004_Figure_4.jpg]]
*Figure 4: InferenceprocessofCubiD.Toprowshowsthelatenttokenstate(white:masked,pink:unmasked),botomrowshows correspondingdecodedimages.uringgeneration,CubiDstartsfromafullyasedtensor(O%)andprogressvelyunmasktkensuntil reachingacompleteimage(O0%).Atachiteration,themodelpredictsallmaskedtokensinparalelandrandomlyunmasksasubset. The percentagesshowtheprogessthroughgenerationsteps.Generationtakeshundredsofterationsregardlessoffeaturedimensioality makingigh-dmensioaletegneratiomputatioallfeasibl.Thsualizatidemostratesacoarse-tfnegeeratiooces, where early iterations establish overall structure and later iterations refine details*



## 实验与关键发现

### 核心瓶颈验证：高维离散化的语义保持

CubiD 的核心前提是：高维表示令牌（768–1024 维）能够保留连续特征的语义丰富性，而传统低维令牌（8–32 维）在生成和理解之间存在根本性权衡。这一前提通过两个关键实验得到验证。

**逐维量化 vs. 向量量化的语义保持**（Table 3）：以 SigLIP2 编码器为基础，逐维量化（DQ）在多模态理解基准上几乎完全保持了连续特征的性能——GQA 得分 63.1 vs 63.2，TextVQA 得分 59.8 vs 59.6。相比之下，向量量化（VQ）导致显著退化，GQA 降至 54.9，TextVQA 降至 54.1。这一差距揭示了 VQ 的瓶颈：联合量化整个向量会破坏维度间的细粒度语义结构，而逐维独立量化则保留了每个维度的判别信息。

**量化层级的选择**（Table 2）：DINOv2 编码器在量化层级 L=8 时达到重建质量饱和（rFID=0.57），SigLIP2 在 L=16 时达到最优（rFID=0.69）。过低的量化层级（如 L=4）信息损失显著，而过高的层级（如 L=32）收益递减，表明高维令牌的每个维度本身携带的信息量有限，适度的离散化足以捕获其表达能力。

### 消融实验：设计选择的因果链条

Table 4 的消融实验揭示了 CubiD 成功的关键因果机制，每一项都直接关联到方法的核心创新。

![[assets/figures/papers/cubid_cvpr2026_20260622/figures/006_Table_4.jpg]]
*Table 4: Ablation studies on CubiD design choices.Gray rows indicate best results*

**掩码粒度：跨轴依赖的必要性**（Table 4b）。这是最具决定性的消融结果。按维度掩码（per-dim）完全失败，gFID 高达 120.03，生成的图像呈现严重的纹理状伪影（Figure 5 顶行）；按空间掩码（per-spatial）有所改善但仍不理想，gFID=22.22，图像存在局部不一致和模糊细节（Figure 5 中行）；而元素级掩码（per-element）将 gFID 降至 5.33，生成清晰连贯的图像（Figure 5 底行）。这一巨大差距证明了高维令牌生成的根本挑战：空间位置和特征维度之间存在交织的依赖关系，任一维度的独立掩码都会破坏这种跨轴结构。元素级掩码通过在三维张量上随机掩码任意元素，迫使模型从部分观测中同时捕获空间上下文和维度内相关性。

**掩码比率分布：学习信号的强度控制**（Table 4a）。掩码比率 r 从截断高斯分布 TruncNorm(μ=1.0, σ, [0,1]) 中采样，标准差 σ 控制训练时掩码的激进程度。σ=0.10 实现最优 gFID=5.33，σ 过小（0.01，gFID=5.47）导致掩码比率过于集中在 1.0 附近，模型几乎总是面对高度掩码的输入，缺乏足够的可见上下文；σ 过大（0.25，gFID=5.75）则使掩码比率分布过于分散，模型训练信号变弱。这一结果验证了截断高斯分布的设计合理性：偏向高掩码率迫使模型学习强上下文推理，同时保留适度的方差以提供多样化的训练难度。

**掩码令牌表示：可学习嵌入的适应性**（Table 4c）。可学习掩码令牌（gFID=5.33）优于固定零值（gFID=5.52），并大幅领先随机掩码令牌（gFID=56.38）。随机掩码令牌的失败表明，掩码位置的表示不能是任意噪声——它需要与可见令牌形成有意义的对比，使模型能够区分“待预测”和“已知”状态。可学习嵌入通过训练适应了这一角色，为模型提供了稳定的缺失值语义。

**推理步数的饱和效应**（Table 4d）。推理步数 T 从 64 增至 512 时，gFID 持续改善（5.88→5.25），但 T=1024 时仅微降至 5.24，性能趋于饱和。这表明 cosine schedule 驱动的迭代解掩码过程在约 500 步时已基本完成 coarse-to-fine 的生成过程，继续增加步数带来的细粒度修正极为有限。这一特性使 CubiD 在固定数百步内完成生成，与特征维度 d 无关（Figure 1b），实现了计算可行性的核心承诺。

**模型规模的扩展行为**（Table 4e）。从 CubiD-L（946M，gFID=5.25）到 CubiD-XL（1.4B，gFID=4.91）再到 CubiD-XXL（3.7B，gFID=4.68），生成质量持续提升，未出现明显的规模收益递减。这表明元素级掩码提供的稠密学习信号能够有效驱动大规模模型的训练，方法具有良好的可伸缩性。

**编码器的通用性**（Table 4f）。DINOv2-B 和 SigLIP2-B 编码器均可训练出高质量生成模型（gFID 5.25 vs 5.87），表明 CubiD 的细粒度掩码策略对不同预训练表示具有通用适应能力。DINOv2 略优的性能可能源于其更强的空间结构保持能力，但差距不大，说明方法的核心优势在于掩码策略本身而非特定编码器。

### 主结果：高维离散生成的基准对比

Table 5 汇总了 ImageNet 256×256 类别条件生成的主要结果。CubiD-XXL 在无引导条件下达到 gFID=2.02，使用分类器自由引导（cfg）后降至 1.88。与现有离散生成方法相比，CubiD 是唯一直接使用原生高维表示令牌（768d）的方法，而所有其他方法均使用压缩或低维令牌（大多低于 32 维）。

![[assets/figures/papers/cubid_cvpr2026_20260622/figures/013_Table_5.jpg]]
*Table 5: Discrete generationmethodsonImageNet[8256x256.LatentDimdenotes theoriginaldimensionalityofthelatentspace (featureseforevectorquantizationforlow-dimensionalmethods,beforeandafterdimension-wiseuantizationforCubiD).Resultsith superscript"redenoterejectionsampling.CubiDisthefirstandonlydiscretemethodtodirectlygeneratewithnativehigh-dimensional representation tokens (768d),while allother methods use compressed or low-dimensional tokens (mostly below 32)*

具体而言，VFM-Tok-XXL 报告了 1.95 gFID（cfg），但需注意该方法对高维令牌进行了重组压缩，并非直接在高维空间建模。MaskGIT（Chang et al., CVPR 2022）使用低维 VQ 令牌，gFID 为 6.18；VAR（Tian et al., arXiv 2024）采用下一尺度自回归预测，gFID 为 1.73，但其潜在维度仅为 32。CubiD 在保持 768 维语义丰富性的同时，实现了与这些低维方法竞争甚至更优的生成质量，证明了高维离散生成在保真度上不逊于低维方案。

### 失败模式与局限性

消融实验揭示了明确的失败模式：当掩码粒度退化为 per-dim 或 per-spatial 时，模型完全无法生成有意义图像（gFID>22），表现为纹理崩溃和结构混乱（Figure 5）。这表明元素级掩码不是可选的优化，而是高维离散生成的必要条件——任何粗粒度的掩码策略都无法同时捕获空间和维度依赖。

当前实验的局限性也需注意：所有结果仅限于 256×256 分辨率的类别条件生成，尚未验证在更高分辨率或文本到图像场景下的有效性。逐维量化虽保持了连续特征性能，但量化层级有限（L=8 或 16），在极端细节需求下可能存在信息瓶颈。此外，推理仍需数百步迭代，实时应用场景面临延迟挑战。这些限制指向了未来的改进方向：分层掩码策略以处理更高分辨率，以及更高效的推理调度以降低步数需求。

### 补充图表

![[assets/figures/papers/cubid_cvpr2026_20260622/figures/005_Table_1.jpg]]
*Table 1: Model sizes and architecture configurations of CubiD*

![[assets/figures/papers/cubid_cvpr2026_20260622/figures/009_Table.jpg]]
*Table: (d) Inference steps.Effect of inference steps T. (f) Representation encoder. DI-NOv2 vs. SigLIP2*

![[assets/figures/papers/cubid_cvpr2026_20260622/figures/010_Table.jpg]]
*Table: (c)Mask value.Fixed,random, or learned mask token*

![[assets/figures/papers/cubid_cvpr2026_20260622/figures/002_Figure.jpg]]
*Figure: Figur2.Generatedsamples fromCubiD.Clas-conditioal generatioresultsonImageNet256×256usinghigh-dimensionalrepresentation tokens from DINOv2-B encoder,demonstrating fine details and textures across diverse categories*



## 定位与知识库关联

### 1. 问题定位：高维离散生成的核心瓶颈

CubiD 所解决的核心问题根植于离散视觉生成领域长期存在的一个结构性矛盾：**低维令牌的语义贫瘠性与高维令牌的建模不可行性**。

现有离散生成方法——包括自回归模型和离散扩散模型——几乎全部建立在低维潜在令牌（通常 8–32 维）之上。这些低维令牌通过向量量化（VQ）将连续表示压缩至极低维度，其根本原因在于：若直接在原生高维表示（如 DINOv2 的 768 维或 SigLIP2 的 1024 维特征）上执行离散建模，会遭遇维度灾难——一个 $h \times w \times d$ 的张量产生指数级庞大的令牌空间，自回归生成需要 $O(hwd)$ 步，在计算上完全不可行；而标准离散扩散仅在空间位置层面操作，无法捕获同一位置内各维度之间的复杂依赖关系（Figure 1）。

这一瓶颈的实质是：**低维令牌牺牲了预训练编码器所提取的语义丰富性，而高维令牌的离散化又缺乏有效的生成范式**。CubiD 正是在这一夹缝中找到了突破口。

### 2. 与现有方法的谱系关系

#### 2.1 离散扩散谱系：从 MaskGIT 到 CubiD

CubiD 直接继承并扩展了掩码扩散（masked diffusion）的范式。其最直接的方法论前驱是 **MaskGIT**（Chang et al., CVPR 2022），后者首次将双向 Transformer 与迭代解掩码策略引入图像生成，证明了离散扩散在视觉合成中的可行性。然而，MaskGIT 的操作空间仅限于低维 VQ 令牌的空间位置级别——它在 $h \times w$ 的二维网格上执行掩码与预测，每个位置对应一个已被 VQ 压缩至 8–32 维的离散码。

CubiD 将这一范式从二维空间网格**升维至三维张量空间**（$h \times w \times d$），其核心改造体现在三个层面：

| 设计维度 | MaskGIT 及同类方法 | CubiD |
|---------|-------------------|-------|
| **令牌维度** | 低维（8–32d），经 VQ 压缩 | 高维（768–1024d），保留原生语义 |
| **掩码粒度** | 空间位置级（per-spatial） | 元素级（per-element），独立掩码任意维度 |
| **建模空间** | $h \times w$ 二维网格 | $h \times w \times d$ 三维立方体 |
| **生成步数** | $T < hw$ | $T \ll hwd$，与 $d$ 无关 |

这一升维并非简单的维度扩展。Table 4b 的消融实验揭示了其关键性：在相同架构下，按维度掩码（per-dim）导致 gFID 飙升至 120.03，按空间掩码（per-spatial）为 22.22，而元素级掩码（per-element）则达到 5.33。这一巨大差距说明，**高维令牌的生成必须同时捕获空间跨位置依赖和维度内跨特征依赖**，任何单一轴向上的掩码策略都会破坏这种双重依赖结构。

#### 2.2 自回归谱系：与 VAR 的对比

**VAR**（Tian et al., arXiv 2024）代表了自回归生成在离散空间中的最新进展，其采用“下一尺度预测”（next-scale prediction）策略，通过多尺度自回归逐步生成令牌。VAR 的核心优势在于将自回归步数从 $O(hw)$ 降至 $O(\log(hw))$，显著提升了生成效率。

然而，VAR 与 CubiD 的根本分歧在于**对令牌维度的处理方式**：VAR 仍然依赖 VQ 将令牌压缩至低维（通常 ≤32 维），其自回归策略的加速并未解决高维令牌的建模难题。事实上，若将 VAR 直接应用于 768 维令牌，其自回归步数将变为 $O(hwd)$，完全失去效率优势。CubiD 的固定步数迭代策略（cosine schedule，$T$ 步）则从根本上与特征维度 $d$ 解耦，使得高维生成的计算复杂度不再随维度增长。

#### 2.3 高维令牌生成谱系：与 VFM-Tok 的关系

**VFM-Tok** 是已知唯一直接处理高维表示令牌的离散生成方法，但其策略与 CubiD 截然不同：VFM-Tok 需要对高维令牌进行重组压缩（reshaping and compression），实质上是将高维问题重新转化为低维问题。CubiD 则首次实现了**在原生高维令牌上的直接生成**，无需任何降维或重组操作。

Table 5 的主实验结果量化了这一差异：CubiD-XXL 在 ImageNet 256×256 上以 768 维原生令牌达到 1.88 gFID（含 classifier-free guidance），而 VFM-Tok-XXL 在同基准上报告 1.95 gFID。尽管差距仅为 0.07，但考虑到 CubiD 处理的是未经压缩的完整 768 维表示，这一结果表明**保留语义完整性可以在不牺牲生成质量的前提下实现**。

### 3. 离散化策略的谱系定位：DQ vs. VQ

CubiD 的另一关键设计选择——逐维量化（Dimension-wise Quantization, DQ）——同样需要在离散化方法的谱系中加以定位。

向量量化（VQ）长期以来是离散表示学习的标准范式，从 VQ-VAE 到 VQGAN，其核心操作是将整个向量联合映射到码本中的最近邻。VQ 的优势在于信息压缩率高，但代价是语义信息的显著损失。Table 3 的结果清晰地展示了这一代价：在 SigLIP2 特征上，VQ 导致 GQA 从连续特征的 63.2 降至 54.9（下降 8.3 点），TextVQA 从 59.6 降至 54.1（下降 5.5 点）。

CubiD 的逐维量化则采取正交策略：独立处理每一维度，将连续值 $z_{x,y,i}$ 量化为 $L$ 个离散等级：

$$q_{x,y,i} = \mathrm{Quantize}(z_{x,y,i}; L)$$

这一设计的核心洞察在于：**预训练编码器的各维度已经过充分解耦，独立量化不会破坏维度间的语义结构**。Table 3 证实了这一点——SigLIP2-DQ 在 GQA 上达到 63.1（与连续特征的 63.2 几乎一致），TextVQA 达到 59.8（与连续特征的 59.6 持平）。Table 2 进一步表明，仅需 8 个量化等级（DINOv2）或 16 个等级（SigLIP2）即可实现与连续特征相当的 reconstruction 质量（rFID 分别为 0.57 和 0.69）。

### 4. 适用边界与局限

尽管 CubiD 在高维离散生成上取得了突破，其方法存在明确的适用边界：

**（1）分辨率限制。** 当前所有实验均在 ImageNet 256×256 分辨率上进行。元素级掩码的计算开销随 $h \times w \times d$ 线性增长，在更高分辨率（如 512² 或 1024²）下，张量规模可能达到数千万元素，训练和推理的内存需求将显著增加。虽然方法本身与分辨率无关，但实际可扩展性尚未验证。

**（2）对预训练编码器的强依赖。** Table 4f 显示，使用 DINOv2-B 编码器时 gFID 为 5.25，而 SigLIP2-B 为 5.87，差距约 0.6。这表明 CubiD 的生成质量高度依赖编码器表示的特性——不同编码器的特征分布、维度间相关性、语义组织方式都会影响离散化质量和掩码建模的难度。该方法并非“编码器无关”，而是需要针对具体编码器进行适配。

**（3）量化精度的固有限制。** 逐维量化虽保留了连续特征的大部分语义，但 $L=8$ 或 $L=16$ 的离散化本质上引入了不可逆的信息损失。在需要极高精度特征重建的场景（如医学图像、科学可视化），这种损失可能变得显著。Table 2 中 rFID 未能降至零即反映了这一残余损失。

**（4）推理效率的实践挑战。** 虽然 CubiD 的推理步数与特征维度 $d$ 无关，但 Table 4d 表明仍需 $T=512$ 步才能达到性能饱和（gFID 5.25），$T=256$ 步时 gFID 升至 5.56。数百步的迭代推理在实时应用中仍构成挑战，尤其是与单步生成方法（如 GAN）或少数步扩散方法相比。

**（5）任务范围的局限性。** 当前工作仅限于 class-conditional 图像生成。CubiD 尚未在文本到图像生成、图像编辑、视频生成等更广泛的条件生成任务上进行验证。元素级掩码策略是否能自然地融入跨模态条件信号（如文本嵌入），以及是否能在时序维度上扩展至视频，仍是开放问题。

### 5. 开放问题与未来方向

CubiD 的提出不仅解决了一个具体的技术问题，更开启了一系列值得探索的方向：

**（1）细粒度掩码与连续扩散的融合。** CubiD 证明了在离散空间中进行元素级掩码建模的有效性。一个自然的问题是：能否将这一细粒度掩码策略引入连续扩散模型？例如，在 latent diffusion 的高维潜在空间中对特定维度或通道进行选择性噪声注入，可能进一步提升连续扩散模型在高维表示上的生成保真度。

**（2）统一理解与生成的离散令牌。** Table 3 表明 DQ 令牌在理解任务上几乎无损。这暗示了一个诱人的可能性：同一组高维离散令牌能否同时服务于视觉理解（作为 MLLM 的输入）和视觉生成（作为 CubiD 的生成目标）？若能实现端到端的统一训练，将朝着真正的多模态基础模型迈出重要一步。

**（3）高分辨率下的可扩展掩码策略。** 在 $h \times w \times d$ 张量上进行全元素级掩码在高分辨率下可能变得低效。是否需要设计分层的（hierarchical）或稀疏的（sparse）掩码策略，仅在关键位置或关键维度上执行细粒度掩码，而在其他区域采用粗粒度掩码？这种混合策略可能在高分辨率场景下实现效率与质量的平衡。

**（4）文本到图像及视频生成的扩展。** CubiD 的掩码扩散框架在理论上支持任意条件信号——只需将条件嵌入注入双向 Transformer 的注意力层。验证该方法在文本到图像生成上的有效性，以及将 $h \times w \times d$ 张量扩展为 $t \times h \times w \times d$ 用于视频生成，是直接且重要的下一步。

**（5）量化策略的理论分析。** 逐维量化的成功依赖于“预训练特征维度已充分解耦”这一经验假设。对这一假设进行更深入的理论分析——例如研究不同编码器的维度间互信息、量化误差的传播特性——可能指导更优的离散化策略设计，甚至催生专门为逐维量化优化的编码器架构。



## 原文 PDF

![[paperPDFs/CVPR_2026/Cubic_Discrete_Diffusion_Discrete_Visual_Generation_on_High_Dimensional_Representation_Tokens.pdf]]
