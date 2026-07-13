---
title: KMM Key Frame Mask Mamba for Extended Motion Generation
type: paper
paper_level: A
venue: arXiv
year: 2024
pdf_ref: paperPDFs/arxiv_2024/KMM_Key_Frame_Mask_Mamba_for_Extended_Motion_Generation.pdf
project_link: https://steve-zeyu-zhang.github.io/KMM
code_link: null
aliases:
- KFMMK
- KKFMMEMG
tags:
- arxiv_2024
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
- topic/generative_models_diffusion
core_operator: 核心干预手段为：1）基于局部密度和最小距离到更高密度点的关键帧掩码策略，使曼巴的记忆集中于关键动作；2）可学习对比损失显式对齐文本和运动特征。
primary_logic: 利用运动令牌的密度分布识别关键帧并进行掩码，强化Mamba隐状态对关键动态的建模；同时，通过对比学习拉近文本和运动潜在空间，提升跨模态对齐，从而生成更准确、连贯的长运动序列。
claims:
- KMM在BABEL子序列上的FID达到0.34，显著优于先前最佳方法（如TEACH的1.12）。
- 在包含方向性指令的BABEL-D数据集上，KMM的R-precision和FID均大幅领先，验证了文本-运动对齐能力的提升。
- 消融实验表明，基于密度的关键帧掩码相比随机掩码带来显著性能提升，对比学习进一步降低FID。
- 用户研究显示92%的参与者认为KMM在方向性指令上的运动对齐优于其他方法。
---

# KMM Key Frame Mask Mamba for Extended Motion Generation

> [!tip] 核心洞察
> 利用运动令牌的密度分布识别关键帧并进行掩码，强化Mamba隐状态对关键动态的建模；同时，通过对比学习拉近文本和运动潜在空间，提升跨模态对齐，从而生成更准确、连贯的长运动序列。

| 字段 | 内容 |
|------|------|
| 中文题名 | KMM：面向扩展运动生成的关键帧掩码曼巴网络 |
| 英文题名 | KMM Key Frame Mask Mamba for Extended Motion Generation |
| 会议/期刊 | arXiv 2024 |
| Links | [Project](https://steve-zeyu-zhang.github.io/KMM) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction #topic/generative_models_diffusion |
| Method | Key Frame Mask Mamba (KMM) |
| Dataset | BABEL, BABEL-D, HumanML3D |

> [!tip] 效果简介
> - BABEL (Subsequence) 上，FID 0.34 ± 0.01 vs 1.12 ± 0.00 (TEACH) (-0.78)。
> - BABEL (Transition) 上，FID 1.37 ± 0.04 vs 7.93 ± 0.00 (TEACH) (-6.56)。
> - BABEL-D 上，R-precision 0.538 ± 0.004 vs 0.459 ± 0.004 (FlowMDM) (+0.079)。

## 概要

### 问题背景

长时序人体运动生成（extended motion generation）面临两个核心瓶颈。其一，基于Mamba的序列模型在处理长运动序列时，其隐式记忆容量有限，难以有效捕捉全部关键动作帧，导致生成动作的连贯性和准确性下降。其二，Mamba的序列化架构在多模态对齐方面存在天然劣势——文本与运动特征之间缺乏显式的跨模态约束，使得模型在处理包含方向性指令（如“向左走”、“右手抬起”）的复杂文本查询时，常常产生错误的运动方向或动作类型。

### 核心方法定位

针对上述瓶颈，KMM（Key Frame Mask Mamba）提出了两项关键干预手段，形成“记忆聚焦—模态对齐”的双重改进路径。

**记忆聚焦层面**，KMM设计了一种基于密度感知的关键帧掩码策略（Key Frame Mask Modeling）。该策略通过计算运动令牌在潜在空间中的局部密度和到更高密度点的最小距离，自动识别携带关键动态信息的动作帧，并对这些关键帧进行掩码。这一设计迫使Mamba的隐状态在序列建模过程中集中“记忆”关键动作的上下文信息，从而缓解长序列下的记忆稀释问题。

**模态对齐层面**，KMM引入了可学习温度的文本-运动对比损失，显式地将文本潜在表征与运动潜在表征拉近。与以往依赖冻结CLIP编码器、缺乏显式对齐信号的方法不同，该对比学习范式使模型能够动态学习文本编码，显著提升了对方向性指令和复杂语义的理解能力。

在架构层面，KMM采用VQ-VAE将运动序列压缩至离散潜在空间，并以掩码双向Mamba（Mask Bi-Mamba）作为自回归生成主干，将关键帧掩码与对比对齐统一于同一训练框架。

### 主要结果

KMM在扩展运动生成任务上取得了显著的性能优势，同时保持了极高的计算效率。

在BABEL数据集上，KMM的子序列FID达到0.34，相比先前最佳方法TEACH（FID为1.12）降低了约70%；在过渡段（Transition）上，FID从7.93降至1.37，降幅更为显著。在专门评估方向性指令理解能力的BABEL-D基准上，KMM的R-precision达到0.538，大幅领先FlowMDM的0.459，验证了对比学习对文本-运动对齐的实质性提升。在HumanML3D数据集上，KMM同样取得了有竞争力的FID（0.15），与MoMask持平或略优。

值得注意的是，KMM在实现上述性能的同时，参数量减少了55%，计算量（GFLOPs）降低了70%，展现出“轻量高效”的实用价值。用户研究进一步佐证了方法的有效性：92%的参与者认为KMM在方向性指令上的运动对齐优于其他方法，78%的参与者认为其生成的运动更加鲁棒和真实。

### 开放问题

尽管KMM在现有基准上表现突出，仍存在若干值得探索的方向：该方法能否扩展至超出BABEL时长限制的超长序列生成；基于密度的关键帧选择策略是否适用于其他Mamba变体或Transformer架构；对比学习中的温度参数和掩码比例是否可以在推理过程中动态调整；以及该方法在实时生成场景中的可行性尚待验证。



### 长时运动生成的核心困境

人体运动生成旨在根据文本描述合成真实、多样的人体动作序列。随着应用场景从短视频向电影、游戏、虚拟人等长时内容扩展，**扩展运动生成**（extended motion generation）成为该领域的关键挑战。与标准运动生成不同，扩展运动生成要求模型在长达数十秒甚至数分钟的时间跨度内，持续生成语义连贯、动作自然且与文本指令精确对齐的运动序列。

该任务面临两个相互交织的瓶颈：

**瓶颈一：长序列记忆容量不足。** 以Mamba为代表的状态空间模型在序列建模中展现出线性复杂度和长程依赖捕捉能力，但其隐式记忆容量仍然有限。当运动序列长度显著增加时，模型难以在隐状态中完整保留所有关键动作信息，导致生成的运动在语义上出现漂移或丢失关键动作节点。

**瓶颈二：文本-运动跨模态对齐薄弱。** 现有扩展运动生成方法通常依赖冻结的CLIP文本编码器提取文本特征，缺乏显式的跨模态对齐机制。这一缺陷在涉及方向性指令（如“向左走”“向右转”）时尤为突出——模型频繁生成方向错误或语义矛盾的运动，暴露出对空间语义理解的深层不足。

### 现有方法的缺口

当前扩展运动生成的主流范式可归为两类：

- **基于扩散模型的方法**：如**PriorMDM**和**FlowMDM**（Barquero et al., CVPR 2024），通过在时间维度上拼接或插值运动片段实现序列扩展。这类方法虽然能生成平滑的过渡动作，但对长序列的全局语义一致性控制较弱，且推理过程计算开销大。

- **基于自回归/掩码建模的方法**：如**TEACH**及其变体、**MoMask**（Guo et al., CVPR 2024）、**MMM**（Pinyoanuntapong et al., CVPR 2024）和**BAMM**（Pinyoanuntapong et al., 2024），通过离散化运动令牌并利用Transformer或Mamba进行序列生成。这类方法在短序列上表现优异，但在长序列生成中仍受限于两个根本问题：一是掩码策略通常采用随机掩码，未能引导模型关注关键动作帧；二是文本编码与运动解码之间缺乏显式对齐，导致复杂语义指令的理解偏差。

值得注意的是，**Motion Mamba**（Zhang et al., ECCV 2024）和**InfiniMotion**（Zhang et al., 2024）已将Mamba架构引入运动生成，验证了状态空间模型在该任务上的潜力。然而，它们同样未解决Mamba隐状态对关键动作的选择性记忆问题，也未建立有效的文本-运动对齐机制。

### 本文的核心动机

针对上述缺口，本文提出**KMM（Key Frame Mask Mamba）**，核心动机可概括为两个层面：

1. **让Mamba“记住该记住的”**：运动序列中存在天然的信息密度差异——关键动作帧承载了绝大部分语义信息，而过渡帧的信息量相对较低。通过识别并掩码这些高密度关键帧，迫使Mamba的隐状态主动学习关键动作的表征，从而在有限记忆容量下最大化语义保留。

2. **让文本与运动“真正对齐”**：放弃对冻结文本编码器的依赖，引入可学习的对比损失，将文本潜在空间与运动潜在空间显式拉近。这一设计使得模型能够动态学习文本编码，而非被动接受固定的语义表示，从而显著提升对方向性指令和复杂文本查询的理解精度。

这两个动机在方法论上互为补充：关键帧掩码强化了运动侧的语义建模，对比对齐则弥合了文本侧与运动侧之间的语义鸿沟，共同构成了KMM应对长时扩展运动生成挑战的技术基础。



## 核心方法与创新机理

KMM 的核心创新围绕两个因果扭结（causal knobs）展开：**基于密度感知的关键帧掩码策略**与**可学习对比损失驱动的跨模态对齐**。二者共同解决了 Mamba 架构在扩展运动生成中的两个根本瓶颈——隐式记忆容量有限导致的长程关键动作丢失，以及序列化架构在多模态对齐上的先天弱势。

### 创新点一：密度感知的关键帧掩码建模

传统掩码策略（如随机掩码或无关键帧选择）对运动令牌一视同仁，导致 Mamba 的隐状态难以聚焦于决定运动语义的关键动作帧。KMM 提出了一种**基于局部密度和最小距离的关键帧选择与掩码机制**，其核心逻辑如下：

1. **局部密度计算**：对运动潜在空间中的每个令牌 $\mathbf{x}_i$，计算其高斯核局部密度 $\mathbf{d}_i = \sum_j \exp(-||\mathbf{x}_i - \mathbf{x}_j||_2^2)$（Equation 4）。密度高的令牌对应运动序列中的关键姿态节点。

2. **最小距离到更高密度点**：定义 $\mathbf{S}_i = \min_{j: \mathbf{d}_j > \mathbf{d}_i} ||\mathbf{x}_i - \mathbf{x}_j||_2$（Equation 9），衡量令牌 $i$ 到任意密度更高令牌的最小欧氏距离。该值大的令牌孤立性更强，更可能是独立的语义关键帧。

3. **密度参数与关键帧选择**：定义密度参数 $\Gamma_i = \mathbf{d}_i \cdot \mathbf{S}_i$（Equation 10），取 $\mathbf{K} = \underset{i}{\mathrm{argmax}}\ \Gamma_i$（Equation 11）作为关键帧索引。该策略确保选出的帧同时具备高局部密度和高语义独立性。

选定关键帧后，KMM 在 Mamba 的序列架构上施加**单向掩码与填充掩码**（Section 3.2），迫使模型在恢复被掩码关键帧的过程中强化对关键动态的表征学习。消融实验（Table 4）直接验证了这一设计的因果效应：**密度关键帧掩码将 BABEL 子序列上的 FID 从随机掩码的 0.40 降至 0.34**，证明了“掩码什么”比“掩码多少”更关键。

### 创新点二：可学习温度的文本-运动对比对齐

Mamba 的序列化架构天然缺乏 Transformer 的全局交叉注意力机制，导致文本条件与运动序列之间的跨模态对齐较弱，尤其体现在方向性指令（如“向左走”与“向右走”）的理解错误上（Figure 2）。KMM 通过**显式对比学习**干预这一瓶颈：

- 计算文本潜在张量 $\mathbf{T}_i$ 与运动潜在张量 $\mathbf{M}_j$ 的缩放相似度 $\mathrm{sim}_{ij} = \frac{\mathbf{T}_i^\top \mathbf{M}_j}{\tau}$（Equation 13），其中 $\tau$ 为可学习温度参数。
- 施加对称交叉熵对比损失 $\mathcal{L}_{\text{contrast}} = \lambda (\text{CrossEntropy}(\mathrm{sim}, \mathbf{y}) + \text{CrossEntropy}(\mathrm{sim}^\top, \mathbf{y}))$（Equation 14），$\lambda=0.5$。

该设计改变了基线方法依赖冻结 CLIP 文本编码器、无显式对齐损失的做法（changed slot），使文本编码能够动态适应运动空间的分布。消融实验（Table 4）表明，**加入对比学习后，BABEL 子序列 FID 进一步从 0.40 降至 0.34，且 R-precision 同步提升**。在专门构造的 BABEL-D 方向性指令基准上，KMM 的 R-precision 达到 0.538，显著领先 FlowMDM 的 0.459（Table 2），用户研究中有 92% 的参与者认为 KMM 在方向性指令上的对齐优于其他方法（Figure 6）。

### 创新点三：掩码双向 Mamba 架构的整体重构

上述两个 changed slots 嵌入在统一的**掩码双向 Mamba 自回归框架**中（Figure 3b）。相较于标准 Transformer 或扩散模型的基线方案，KMM 的架构重构体现在：

- **VQ-VAE 压缩**：将运动序列映射到离散潜在空间，降低序列长度与计算开销。
- **四层 Mask Bi-Mamba**：对掩码后的运动令牌与文本嵌入进行双向序列建模，恢复被掩码的关键帧。
- **效率优势**：相比先前 SOTA，KMM 参数量减少 55%，GFLOPs 降低 70%（Figure 1 右），同时 FID 降低超过 0.24。

需要指出的是，部分对比方法的计算量是否在同等硬件条件下重新测量尚不明确（fairness notes），但 KMM 在 BABEL 子序列（FID 0.34 vs TEACH 1.12）和过渡段（FID 1.37 vs TEACH 7.93）上的大幅领先（Table 1），为架构重构的有效性提供了强证据。



KMM的整体架构是一个面向长序列运动生成的自回归模型，其核心设计遵循“压缩-掩码-重建-对齐”的四阶段流水线。给定一段文本描述和期望的运动时长，系统首先将原始运动序列压缩到离散潜在空间，随后通过基于密度的关键帧选择策略对潜在令牌进行选择性掩码，再由掩码双向Mamba骨干网络结合文本条件恢复被掩码的关键帧，最终通过对比学习显式对齐文本与运动的潜在表示。

### 阶段一：运动压缩与离散化

输入的运动序列首先经过一个VQ-VAE编码器，被压缩到低维潜在空间，并通过一个可学习的码本（codebook）将连续潜在向量量化为离散的运动令牌。该VQ-VAE采用6层量化结构，以256的批次大小进行训练。这一步将连续的高维运动数据转化为离散的令牌序列，为后续的掩码语言建模范式提供基础。

### 阶段二：基于密度的关键帧掩码

这是KMM区别于现有方法的**核心创新模块**。系统对VQ-VAE输出的每个运动令牌$\mathbf{x}_i$计算其局部密度$\mathbf{d}_i$：

$$\mathbf{d}_i = \sum_j \exp(-||\mathbf{x}_i - \mathbf{x}_j||_2^2)$$

随后计算每个令牌到局部密度更高的令牌的最小欧氏距离$\mathbf{S}_i$：

$$\mathbf{S}_i = \min_{j: \mathbf{d}_j > \mathbf{d}_i} ||\mathbf{x}_i - \mathbf{x}_j||_2$$

将两者相乘得到密度参数$\Gamma_i = \mathbf{d}_i \cdot \mathbf{S}_i$，并通过$\mathbf{K} = \underset{i}{\mathrm{argmax}}\ \Gamma_i$选取密度参数最大的令牌索引作为关键帧。这一策略的直觉在于：高密度区域中的令牌代表运动序列中的核心姿态，而较大的最小距离则确保所选关键帧在语义上具有区分度。选定关键帧后，系统对这些令牌施加掩码，迫使后续的Mamba骨干网络聚焦于关键动作的建模。

### 阶段三：掩码双向Mamba序列建模

掩码后的运动令牌序列与文本嵌入拼接后，输入一个4层的掩码双向Mamba（Mask Bi-Mamba）骨干网络。Mamba的状态空间模型天然适合长序列建模，但其隐式记忆容量有限；关键帧掩码策略通过强制模型恢复被掩码的关键动作，将Mamba的隐状态容量集中于运动序列中信息密度最高的部分。该骨干网络以64的批次大小进行训练，负责从被部分掩码的序列和文本条件中重建完整的运动令牌序列。

### 阶段四：文本-运动对比对齐

传统方法通常依赖冻结的CLIP文本编码器提取文本特征，缺乏对文本-运动跨模态对齐的显式优化。KMM引入了一个可学习温度的对比学习模块：将文本潜在表示$\mathbf{T}_i$与运动潜在表示$\mathbf{M}_j$的缩放相似度定义为：

$$\mathrm{sim}_{ij} = \frac{\mathbf{T}_i^\top \mathbf{M}_j}{\tau}$$

其中$\tau$为可学习温度参数。在此基础上施加对称交叉熵对比损失：

$$\mathcal{L}_{\text{contrast}} = \lambda (\text{CrossEntropy}(\mathrm{sim}, \mathbf{y}) + \text{CrossEntropy}(\mathrm{sim}^\top, \mathbf{y}))$$

其中$\lambda=0.5$。该损失显式地将匹配的文本-运动对拉近，将不匹配的对推开，从而在潜在空间中实现跨模态对齐。这一设计直接回应了现有方法在处理方向性指令（如“向左走”与“向右走”）时频繁出错的瓶颈。

### 数据流与模块关系

整体数据流可概括为：**文本描述 → 文本编码器 → 文本潜在表示**；**运动序列 → VQ-VAE编码器 → 码本量化 → 运动令牌 → 密度计算与关键帧选择 → 掩码运动令牌**；**掩码运动令牌 + 文本嵌入 → Mask Bi-Mamba → 重建运动令牌 → VQ-VAE解码器 → 生成运动序列**。对比损失作用于文本潜在表示与重建后的运动潜在表示之间，在训练过程中同时优化跨模态对齐和运动重建质量。

各模块间的关系呈串行-并行混合结构：VQ-VAE的压缩与码本量化为后续掩码提供离散令牌基础；关键帧掩码策略直接决定了Mamba骨干网络的学习重点；对比对齐模块则独立于重建路径，从表示层面约束文本与运动的一致性。三者协同作用，使得KMM在BABEL子序列上实现了0.34的FID（相比TEACH的1.12降低0.78），同时参数量减少55%、计算量降低70%。

### 补充图表

![[assets/figures/papers/paper_list_l1830_KMM_Key_Frame_Mask_Mamba_for_Extended_Motion_Generation/figures/003_Figure_3.jpg]]
*Figure 3: The figure demonstrates our novel method from three different perspectives: (a) illustrates the key frame masking strategy based on local density and minimum distance to higher density calculation. (b) showcases the overall architecture of the masked bidirectional Mamba. (c) demonstrates the text-to-motion alignment, highlighting the process before and after alignment*



KMM 的核心架构由四个关键模块构成：VQ-VAE 运动压缩、基于密度-距离的关键帧选择与掩码、掩码双向 Mamba 序列建模，以及文本-运动对比对齐。以下逐一展开其机理与关键公式。

### 运动压缩：VQ-VAE 与码本量化

原始运动序列首先通过 VQ-VAE 压缩到离散潜在空间。该模块采用 6 层量化层，将连续运动帧映射为码本中的离散令牌，从而将长序列转化为紧凑的令牌序列，为后续 Mamba 建模提供高效表示（Section 3.1）。这一压缩步骤是整个流程的基础，直接决定了后续掩码建模的输入质量。

### 关键帧掩码建模：密度-距离双指标选择

这是 KMM 的核心创新。传统掩码策略（如随机掩码）无法区分运动序列中信息量不同的帧，导致模型注意力分散。KMM 提出基于局部密度与最小距离的双指标关键帧选择策略，其因果机制如下：

**步骤一：局部密度计算。** 对 VQ-VAE 编码后的每个运动令牌 $\mathbf{x}_i$，计算其在高斯核下的局部密度：

$$\mathbf{d}_i = \sum_j \exp(-||\mathbf{x}_i - \mathbf{x}_j||_2^2)$$

其中 $\mathbf{d}_i$ 衡量第 $i$ 个令牌周围令牌的聚集程度。密度高的令牌通常对应运动序列中的关键姿态或动作转折点。

**步骤二：最小距离到更高密度点。** 为区分密度相近但语义不同的令牌，引入到更高密度令牌的最小欧氏距离：

$$\mathbf{S}_i = \min_{j: \mathbf{d}_j > \mathbf{d}_i} ||\mathbf{x}_i - \mathbf{x}_j||_2$$

$\mathbf{S}_i$ 越大，说明该令牌在特征空间中越“孤立”，即使其绝对密度不是最高，也可能承载独特的关键信息。

**步骤三：密度参数合成与关键帧选取。** 将两个指标相乘得到综合密度参数：

$$\Gamma_i = \mathbf{d}_i \cdot \mathbf{S}_i$$

最后通过 argmax 选取 $\Gamma_i$ 最大的令牌索引作为关键帧：

$$\mathbf{K} = \underset{i}{\mathrm{argmax}}\ \Gamma_i$$

这一策略的因果逻辑是：高密度且远离更高密度簇的令牌，最可能对应运动序列中不可替代的关键动作帧。选定关键帧 $\mathbf{K}$ 后，对这些帧施加掩码，迫使 Mamba 的隐状态在重建过程中聚焦于关键动态的建模。消融实验（Table 4）证实，该密度掩码策略相比随机掩码将 BABEL 子序列上的 FID 从 0.40 降至 0.34，验证了其因果有效性。

### 掩码双向 Mamba 序列建模

掩码后的运动令牌与文本嵌入拼接，送入 4 层掩码双向 Mamba（Mask Bi-Mamba）进行序列建模（Figure 3b）。Mamba 的选择性状态空间机制天然适合长序列，但其隐式记忆容量有限——这正是关键帧掩码要解决的瓶颈。通过将 Mamba 的注意力强制集中在被掩码的关键帧上，模型隐状态被迫学习捕捉长程运动依赖中的关键动态，而非均匀处理所有帧。

### 文本-运动对比对齐

Mamba 的序列化架构在多模态对齐方面天然弱于 Transformer，表现为方向性指令理解错误（Figure 2）。KMM 引入可学习温度的对比损失来弥合这一差距。

**相似度计算。** 文本潜在表示 $\mathbf{T}_i$ 与运动潜在表示 $\mathbf{M}_j$ 的点积相似度由可学习温度 $\tau$ 缩放：

$$\mathrm{sim}_{ij} = \frac{\mathbf{T}_i^\top \mathbf{M}_j}{\tau}$$

**对比损失。** 采用对称交叉熵形式，系数 $\lambda=0.5$：

$$\mathcal{L}_{\text{contrast}} = \lambda \left( \text{CrossEntropy}(\mathrm{sim}, \mathbf{y}) + \text{CrossEntropy}(\mathrm{sim}^\top, \mathbf{y}) \right)$$

该损失显式拉近匹配的文本-运动对，推远不匹配对，使得原本依赖冻结 CLIP 编码器的文本表示能够动态适应运动空间。消融实验（Table 4）表明，加入对比学习后 FID 进一步从 0.40 降至 0.34，且 R-precision 提升，验证了该模块对跨模态对齐的因果贡献。

### 模块间因果联动

上述四个模块形成因果闭环：VQ-VAE 提供紧凑令牌表示 → 密度-距离指标识别关键帧 → 掩码迫使 Mamba 隐状态聚焦关键动态 → 对比损失确保文本指令与运动语义的对齐。这一联动机制直接回应了 Mamba 架构在长运动生成中的两大瓶颈——记忆容量有限与跨模态对齐弱。



## 实验与关键发现

### 主实验结果

KMM在两个核心基准上均展现出显著优势。在BABEL数据集上，KMM在子序列生成任务中取得了**0.34**的FID（Table 1），相比此前最优方法TEACH的1.12降低了0.78，提升幅度超过69%。在更具挑战性的过渡（Transition）生成任务上，KMM的FID为**1.37**，而TEACH为7.93，差距扩大至6.56，表明KMM在长距离运动连贯性建模上的核心优势。同时，KMM的MM-Dist在子序列上达到**3.11**，为所有对比方法中最优，进一步验证了生成运动与文本描述在语义层面的高度一致。

![[assets/figures/papers/paper_list_l1830_KMM_Key_Frame_Mask_Mamba_for_Extended_Motion_Generation/figures/005_Table_1.jpg]]
*Table 1: Comparison on BABEL [30]. The right arrow → indicates that closer values to real motion are better. Bold and underline highlight the best and second-best results, respectively. Additionally, ∗ denotes results reproduced by FlowMDM. SLI denotes spherical linear interpolation. For results with ±0.000 or ±0.00, the corresponding paper does not provide error bars*

在专门评估方向性指令理解能力的BABEL-D基准上（Table 2），KMM的R-precision达到**0.538**，显著领先于FlowMDM（Barquero et al., CVPR 2024）的0.459，FID亦从FlowMDM的0.87降至**0.62**。这直接印证了对比学习模块对文本-运动对齐的实质改善。在HumanML3D数据集上（Table 3），KMM的FID为**0.15**，略优于MoMask（Guo et al., CVPR 2024）的0.18，表明该方法在常规长度运动生成任务上同样具备竞争力。

![[assets/figures/papers/paper_list_l1830_KMM_Key_Frame_Mask_Mamba_for_Extended_Motion_Generation/figures/006_Table_2.jpg]]
*Table 2: Comparison on BABEL-D. The right arrow → indicates that closer values to real motion are better. Bold and underline highlight the best and second-best results, respectively*

值得注意的效率指标：KMM在参数量上比此前最优方法减少**55%**，GFLOPs降低**70%**（Figure 1），实现了性能与效率的双重突破。

![[assets/figures/papers/paper_list_l1830_KMM_Key_Frame_Mask_Mamba_for_Extended_Motion_Generation/figures/001_Figure_1.jpg]]
*Figure 1: The figure on the left illustrates the exceptional capability of the proposed KMM in generating continuous and diverse human motions based on extended text prompts across various durations. The figure on the right highlights that our method significantly outperforms the previous state-of-the-art in quantitative evaluations while utilizing substantially fewer FLOPs*

### 消融实验分析

消融实验围绕两个核心设计展开（Table 4）：

![[assets/figures/papers/paper_list_l1830_KMM_Key_Frame_Mask_Mamba_for_Extended_Motion_Generation/figures/010_Table_4.jpg]]
*Table 4: Masking strategies. The right arrow → indicates that closer values to real motion are better. Bold and underline highlight the best and second-best results, respectively*

**关键帧掩码策略的有效性**：将KMM的密度关键帧掩码替换为随机掩码后，BABEL子序列上的FID从0.34恶化至0.40，R-precision亦出现下降。这证实了基于局部密度和最小距离的关键帧选择机制确实引导Mamba的隐状态聚焦于对运动语义至关重要的关键动作，而非均匀分配建模能力。

**对比学习的作用**：在保留密度掩码但移除文本-运动对比损失后，FID同样升至0.40附近，且R-precision明显回落。这表明冻结CLIP文本编码器提供的跨模态信号不足以支撑精确的方向性指令理解，而可学习温度的对比损失通过显式拉近文本和运动潜在空间，弥补了这一缺陷。

**超参数鲁棒性**：掩码比例（Table 5）和对比损失系数λ（Table 6）的敏感性实验显示，KMM在较宽的超参数范围内性能稳定，方法对具体配置不敏感，工程部署友好。

### 定性分析

Figure 2展示了方向性指令理解的典型对比案例：当文本包含“向左”或“向右”等空间方向时，先前方法频繁产生错误方向的动作，而KMM凭借增强的文本-运动对齐能力，能够准确生成符合指令的运动。Figure 4的复杂查询定性比较进一步表明，KMM在处理多动作序列和长文本描述时，生成的连贯性和语义准确性均优于此前最优方法。Figure 5展示了KMM按指定时长条件生成长运动的能力，可视化结果验证了其在长序列上的鲁棒性和多样性。

用户研究（Figure 6, Appendix A）提供了独立的外部验证：50名参与者在文本-运动对齐、鲁棒性、多样性和可用性四个维度上对KMM及TEACH、PriorMDM、FlowMDM进行评估，**92%**的参与者认为KMM在方向性指令上的运动对齐优于其他方法。

![[assets/figures/papers/paper_list_l1830_KMM_Key_Frame_Mask_Mamba_for_Extended_Motion_Generation/figures/014_Figure_6.jpg]]
*Figure 6: The figure shows the user study interface where 50 participants evaluated motion sequences generated by TEACH, PriorMDM, FlowMDM, and KMM, focusing on text-motion alignment, robustness, diversity, and usability. The text prompt are randomly extracted and combined from the HumanML3D [14] and BABEL [30] test set*

### 公平性说明

需注意以下评估细节：部分对比方法的结果由作者复现（Table 1中以*标注）；BABEL-D是本文新提出的子集，虽源自BABEL官方测试集，但其构造标准可能存在一定选择偏差；各方法的FLOPs对比（Figure 1）未明确说明是否在同等硬件条件下重新测量。这些因素在解读性能差距时应予以考虑。

### 补充图表

![[assets/figures/papers/paper_list_l1830_KMM_Key_Frame_Mask_Mamba_for_Extended_Motion_Generation/figures/004_Figure_4.jpg]]
*Figure 4: The figure demonstrates a qualitative comparison between the previous state-of-the-art method in extended motion generation and our KMM. The qualitative results show that our method significantly outperforms others in handling complex text queries and generating more accurate corresponding motions*

![[assets/figures/papers/paper_list_l1830_KMM_Key_Frame_Mask_Mamba_for_Extended_Motion_Generation/figures/013_Table_5.jpg]]
*Table 5: Masking ratio. The right arrow → indicates that closer values to real motion are better. Bold highlights the best results*

![[assets/figures/papers/paper_list_l1830_KMM_Key_Frame_Mask_Mamba_for_Extended_Motion_Generation/figures/012_Table_6.jpg]]
*Table 6: Coefficient ??. The right arrow → indicates that closer values to real motion are better. Bold highlights the best results*

![[assets/figures/papers/paper_list_l1830_KMM_Key_Frame_Mask_Mamba_for_Extended_Motion_Generation/figures/011_Figure_5.jpg]]
*Figure 5: The figure presents some qualitative visualization results of KMM. The text prompts are sourced and combined from HumanML3D [14] and BABEL [30]. The number within the brackets indicates our ability to condition the generated motion on a specific length, dynamically producing motion of the desired duration. The visualizations showcase KMM’s superior performance in generating robust and diverse motions that align closely with lengthy and complex text queries*

![[assets/figures/papers/paper_list_l1830_KMM_Key_Frame_Mask_Mamba_for_Extended_Motion_Generation/figures/002_Figure.jpg]]

![[assets/figures/papers/paper_list_l1830_KMM_Key_Frame_Mask_Mamba_for_Extended_Motion_Generation/figures/007_Figure.jpg]]



## 定位与知识库关联

### 1. 问题定位：扩展运动生成中的瓶颈

KMM 针对的核心问题是 **扩展运动生成**（extended motion generation）——即从长文本描述中生成持续较长时间、包含多个动作片段的人体运动序列。该任务面临两个关键瓶颈：

1.  **Mamba 的记忆容量限制**：Mamba 架构虽具备线性复杂度，但其隐式记忆（hidden state）容量有限，在生成长序列时难以捕捉全部关键动作帧，导致运动细节丢失或动作过渡不自然。
2.  **文本-运动跨模态对齐薄弱**：Mamba 的序列化架构在处理多模态输入时，缺乏显式的对齐机制，尤其在包含方向性指令（如“向左走”“向右转”）的文本查询中，常产生错误运动。

### 2. 方法谱系：在现有工作坐标系中的位置

KMM 处于 **基于 Mamba 的离散潜在空间运动生成** 这一新兴技术路线上，与以下方法形成直接对话：

| 方法 | 架构路线 | 与 KMM 的关系 |
|------|----------|---------------|
| **TEACH** | 扩散模型 + 球面线性插值（SLI） | 扩展运动生成的先前 SOTA，KMM 的主要对比对象 |
| **PriorMDM** | 扩散模型 | 另一扩散路线基线 |
| **FlowMDM** (Barquero et al., CVPR 2024) | 流匹配 + 混合位置编码 | 在 BABEL-D 上作为方向性理解的主要对比 |
| **InfiniMotion** (Zhang et al., 2024) | Mamba 增强的 Transformer | 同属 Mamba 路线，但无关键帧掩码策略 |
| **Motion Mamba** (Zhang et al., ECCV 2024) | 层级状态空间模型 | 同属 Mamba 路线，架构设计不同 |
| **MoMask** (Guo et al., CVPR 2024) | 掩码运动建模 + 残差 VQ | 在 HumanML3D 上作为主要对比，共享掩码建模思想 |
| **MMM** (Pinyoanuntapong et al., CVPR 2024) | 生成式掩码运动模型 | 掩码建模路线相关 |
| **BAMM** (Pinyoanuntapong et al., 2024) | 双向自回归运动模型 | 自回归路线相关 |
| **MotionGPT** (Jiang et al., NeurIPS 2024) | 语言模型式运动生成 | 跨模态生成路线相关 |
| **T2LM** (Lee et al., CVPR 2024) | 多句长时运动生成 | 长时生成任务相关 |

KMM 的核心创新在于将 **密度感知的关键帧掩码** 与 **可学习对比损失** 引入 Mamba 架构，在保持线性复杂度的同时，显式强化了对关键动态的建模和跨模态对齐。这使其在技术路线上区别于：
- **扩散模型路线**（TEACH, PriorMDM, FlowMDM）：KMM 采用自回归掩码建模，推理效率更高；
- **纯 Mamba 路线**（InfiniMotion, Motion Mamba）：KMM 引入了密度引导的结构化掩码策略；
- **掩码建模路线**（MoMask, MMM）：KMM 的掩码策略基于密度分布而非随机采样。

### 3. 因果机制：关键帧掩码与对比对齐如何协同

KMM 的因果干预机制由两个可操作的“旋钮”构成：

**旋钮一：密度引导的关键帧掩码**
- **操作**：对运动潜在空间中的每个令牌计算局部密度 $d_i = \sum_j \exp(-||x_i - x_j||_2^2)$ 和到更高密度点的最小距离 $S_i = \min_{j: d_j > d_i} ||x_i - x_j||_2$，定义密度参数 $\Gamma_i = d_i \cdot S_i$，选取 $\Gamma_i$ 最大的令牌作为关键帧并掩码。
- **因果效应**：强制 Mamba 的隐状态聚焦于运动序列中的关键动作节点，而非均匀处理所有帧。消融实验（Table 4）表明，密度掩码相比随机掩码将 BABEL 子序列上的 FID 从 0.40 降至 0.34。

**旋钮二：可学习温度的文本-运动对比损失**
- **操作**：计算文本潜在向量 $T_i$ 与运动潜在向量 $M_j$ 的缩放相似度 $\text{sim}_{ij} = T_i^\top M_j / \tau$，其中 $\tau$ 为可学习温度参数，施加对称交叉熵对比损失。
- **因果效应**：显式拉近文本和运动在潜在空间中的距离，解决 Mamba 序列化架构中跨模态对齐薄弱的问题。在 BABEL-D 方向性指令数据集上，R-precision 从 FlowMDM 的 0.459 提升至 0.538，用户研究中 92% 的参与者认为 KMM 在方向性指令上的运动对齐优于其他方法。

两个旋钮具有协同效应：关键帧掩码确保 Mamba 隐状态捕捉到足够的运动语义，对比损失则确保这些语义与文本指令准确对应。

### 4. 适用边界与局限

基于现有证据，KMM 的适用边界如下：

**已验证的有效范围**：
- 数据集：BABEL（最长约 30 秒）、HumanML3D（最长约 10 秒）
- 任务类型：文本到运动生成，包含方向性指令的复杂查询
- 运动类型：日常人体运动（走、跑、跳、转身等）

**已知局限**：
- 论文未明确讨论方法局限，但可从实验设置推断：
  - **序列长度上限**：VQ-VAE 的压缩率和 Mamba 的隐状态容量共同决定了可处理的最大序列长度，超出 BABEL 时长限制的超长序列（如数分钟级别）尚未验证
  - **方向性指令的粒度**：BABEL-D 仅包含 560 个运动片段，且方向性指令限于“左/右”，更复杂的空间关系（如“绕圈”“折返”）未充分评估
  - **计算效率的公平性**：论文声称参数量减少 55%、GFLOPs 降低 70%，但未说明所有对比方法的计算量是否在同等硬件条件下重新测量

### 5. 开放问题

以下问题需要后续工作验证：

1.  **架构泛化性**：密度引导的关键帧掩码策略是否适用于其他 Mamba 变体（如 Vision Mamba）或标准 Transformer 架构？这决定了该策略是 KMM 的专属设计还是通用改进手段。

2.  **超长序列扩展**：KMM 能否在超出 BABEL 时长限制（如 3-5 分钟）的序列上保持运动连贯性和文本对齐精度？Mamba 的线性复杂度提供了理论上的可扩展性，但隐状态的信息衰减效应需要实证检验。

3.  **动态掩码策略**：掩码比例和对比损失系数 $\lambda$ 目前是固定超参数（消融实验显示方法对它们鲁棒），但在推理阶段是否可以根据输入文本的复杂度动态调整？例如，方向性指令密集的查询可能需要更高的掩码比例。

4.  **实时生成可行性**：KMM 的自回归生成模式是否满足实时交互需求（如游戏、虚拟人）？论文未报告推理延迟数据。

5.  **基准的充分性**：BABEL-D 作为新提出的方向性理解基准，仅包含 560 个片段，其难度和多样性是否足以区分不同方法的细粒度空间推理能力？可能需要更大规模、更多样化的方向性指令测试集。



## 原文 PDF

![[paperPDFs/arxiv_2024/KMM_Key_Frame_Mask_Mamba_for_Extended_Motion_Generation.pdf]]
