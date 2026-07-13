---
title: MOST Motion Diffusion Model for Rare Text via Temporal Clip Banzhaf Interaction
type: paper
paper_level: A
venue: arXiv
year: 2025
pdf_ref: paperPDFs/arxiv_2025/MOST_Motion_Diffusion_Model_for_Rare_Text_via_Temporal_Clip_Banzhaf_Interaction.pdf
project_link: null
code_link: null
aliases:
- MMDMRTTCBI
tags:
- arxiv_2025
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
- topic/generative_models_diffusion
- topic/generative_models_diffusion/diffusion_image_video
core_operator: 时间片段Banzhaf交互（Temporal Clip Banzhaf Interaction）将文本与运动片段视为合作博弈中的玩家，通过精确计算每个片段联盟的边际贡献来量化跨模态细粒度一致性，使模型能够排除冗余噪声并聚焦于核心运动线索。
primary_logic: 引入合作博弈论中的Banzhaf交互机制，在片段级别建模文本‑运动的多对多协作关系，并配合基于泛化度比率的收益函数，从根本上消除了全序列冗余的干扰，实现了从稀有文本到关键运动片段的精准对齐，为运动扩散模型提供高保真的生成指引。
claims:
- MOST采用两阶段框架：检索阶段通过时间片段Banzhaf交互实现片段级文本‑运动匹配；生成阶段利用运动提示模块融合检索到的关键片段，有效克服了运动冗余带来的性能退化。
- 将文本片段与运动片段定义为玩家集合，利用Banzhaf交互损失约束预测交互值，在不需要片段级标注的情况下实现了细粒度语义对齐。
- 引入包含泛化度比率的收益函数，量化片段内的信息丰富度，显著降低了冗余片段在检索过程中的权重，提升了运动信息的利用率。
- 在HumanML3D和KIT‑ML上的检索与生成实验一致表明，MOST在FID、MM Dist、R@1等多项指标上超越现有方法，尤其在罕见文本尾部（Tail 0‑5%）上优势更为突出。
---

# MOST Motion Diffusion Model for Rare Text via Temporal Clip Banzhaf Interaction

> [!tip] 核心洞察
> 引入合作博弈论中的Banzhaf交互机制，在片段级别建模文本‑运动的多对多协作关系，并配合基于泛化度比率的收益函数，从根本上消除了全序列冗余的干扰，实现了从稀有文本到关键运动片段的精准对齐，为运动扩散模型提供高保真的生成指引。

| 字段 | 内容 |
|------|------|
| 中文题名 | MOST：基于时间片段Banzhaf交互的稀见文本运动扩散模型 |
| 英文题名 | MOST Motion Diffusion Model for Rare Text via Temporal Clip Banzhaf Interaction |
| 会议/期刊 | arXiv 2025 |
| Links |  [paper](https://arxiv.org/abs/2507.06590)|
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction #topic/generative_models_diffusion #topic/generative_models_diffusion/diffusion_image_video |
| Method | MOST |
| Dataset | HumanML3D, KIT-ML, HumanML3D Rare Tail 0‑5%, KIT‑ML Rare Tail 0‑5% |

> [!tip] 效果简介
> - HumanML3D (All) 上，R@1 6.61。
> - KIT-ML (All) 上，R@1 9.87。
> - HumanML3D 上，FID, R_precision Top-3 0.139。

## 概要

文本驱动的人体运动生成旨在根据自然语言描述合成逼真的三维运动序列。尽管现有方法在常见文本上取得了显著进展，但在处理**稀有文本**（如“blind”、“cartwheel”等低频动作描述）时，生成质量急剧下降。其根本瓶颈在于：全序列检索引入大量运动冗余，粗粒度的实体级对齐掩盖了关键语义线索，导致模型无法有效捕捉稀有动作的细粒度对应关系。

针对这一问题，本文提出 **MOST（Motion Diffusion Model for Rare Text via Temporal Clip Banzhaf Interaction）**，一种基于时间片段Banzhaf交互的稀见文本运动扩散模型。其核心洞察是：将文本片段与运动片段视为合作博弈中的玩家，通过**Banzhaf交互机制**精确计算每个片段联盟的边际贡献，从而量化跨模态细粒度一致性，使模型能够排除冗余噪声并聚焦于核心运动线索。

MOST采用**两阶段框架**：检索阶段通过时间片段Banzhaf交互实现片段级文本‑运动匹配，并引入基于泛化度比率的收益函数抑制冗余片段权重；生成阶段利用运动提示模块融合检索到的关键片段，为扩散模型提供高保真的生成指引。

实验表明，MOST在HumanML3D和KIT‑ML数据集上全面超越现有方法。在稀有文本尾部（Tail 0‑5%）上，MOST的FID在HumanML3D上降至0.66，KIT‑ML上降至7.34，优势尤为突出。消融研究证实，Banzhaf检索、关键片段选择与交叉注意力融合均对性能有显著贡献。



### 文本驱动运动生成的任务困境

文本驱动人体运动生成（Text-to-Motion Generation, T2M）旨在根据自然语言描述合成逼真的三维人体动作序列，在动画制作、虚拟现实、人机交互等领域具有广泛应用前景。近年来，扩散模型在该任务上取得了显著进展，代表性工作包括**MotionDiffuse**（Zhang et al., TPAMI 2024）、**MLD**（Chen et al., CVPR 2023）等基础文本条件扩散模型，以及**ReMoDiffuse**（Zhang et al., arXiv 2023）等检索增强扩散模型。然而，这些方法普遍面临一个核心瓶颈：**在处理稀有文本（rare text）时生成质量显著退化**。

### 运动冗余：被忽视的关键障碍

现有方法在生成常见动作描述（如“一个人走路”）时表现良好，但当面对罕见动作组合或低频描述（如“盲人摸索前进”或复杂动作序列）时，生成的运动往往缺乏语义一致性。MOST论文通过定量分析揭示了这一现象的根本原因——**运动冗余（Motion Redundancy）**问题。

具体而言，现有检索增强方法（如ReMoDiffuse）采用**全序列检索**策略，将整个运动序列作为检索与生成的基本单元。然而，一个完整的运动序列中通常仅包含少量与文本语义直接相关的**关键帧**，其余大部分帧为过渡动作或冗余信息（见Figure 2）。这种粗粒度的实体级对齐方式带来了双重危害：

1. **检索噪声放大**：冗余帧在相似度计算中占据主导地位，淹没了关键运动线索，导致检索到的运动序列与目标文本的细粒度语义对应关系薄弱。
2. **生成指引偏差**：以包含大量冗余信息的完整序列作为扩散模型的条件输入，使模型难以聚焦于核心动作特征，生成的运动会继承冗余模式而非精准响应文本语义。

这一问题在稀有文本场景下尤为突出——稀有动作的训练样本本就稀疏，全序列检索引入的冗余噪声进一步稀释了本就稀缺的语义信号，形成“样本稀疏‑冗余干扰”的恶性循环。

### 细粒度对齐的缺失

除运动冗余外，现有方法的另一结构性缺陷在于**跨模态对齐粒度过粗**。主流T2M模型通常仅通过全局对比损失（如NCE损失）实现文本与运动的整体对齐，缺乏对文本片段与运动片段之间细粒度对应关系的显式建模。以**Fg‑T2M**（Wang et al., ICCV 2023）为代表的细粒度方法尝试利用句法结构进行分解，但仍依赖于预定义的语法树，难以灵活捕捉文本‑运动之间复杂的多对多协作关系。

对于“一个人先蹲下然后跳跃转身”这类包含多个动作阶段的描述，粗粒度对齐无法区分“蹲下”“跳跃”“转身”各自对应的运动片段，导致生成的运动出现阶段混淆或语义遗漏。

### 本文动机与核心思路

针对上述双重困境，MOST论文提出以下核心洞察：**通过引入合作博弈论中的Banzhaf交互机制，在时间片段级别建模文本与运动的多对多协作关系，可以从根本上消除全序列冗余干扰，实现从稀有文本到关键运动片段的精准对齐**。

具体而言，MOST将文本片段与运动片段视为合作博弈中的“玩家”，通过计算每个片段联盟的边际贡献来量化跨模态细粒度一致性。配合基于泛化度比率的收益函数——该函数根据片段内相邻帧的平均绝对差异衡量信息丰富度，低差异片段（冗余帧）被赋予更低权重——模型能够自动排除冗余噪声，聚焦于核心运动线索。这一机制无需片段级标注即可实现细粒度语义对齐，为后续运动扩散模型提供高保真的生成指引。



## 核心方法与创新机理

MOST的核心创新在于将**合作博弈论中的Banzhaf交互机制**引入文本驱动运动生成任务，从根本上改变了检索与生成两阶段中跨模态对齐的粒度与质量。与现有方法相比，其关键突破体现在以下四个维度：

### 1. 检索粒度：从实体级全序列到片段级关键运动

现有检索增强方法（如**ReMoDiffuse**，Zhang et al., arXiv 2023）通常将整个运动序列作为检索与条件单元，导致大量运动冗余帧被纳入生成过程，稀释了关键语义线索。MOST将检索对象从“整个运动序列”切换为“关键运动片段”，通过时间片段Banzhaf交互精确筛选与每个文本片段最相关的运动片段，从根本上消除了全序列冗余的干扰（见Figure 1c, Figure 2）。

这一改变的因果机制在于：稀有文本所描述的动作往往只占据运动序列中的少数关键帧，全序列检索会引入大量无关运动信息，使模型难以聚焦于核心动作。片段级检索则使模型能够“精准定位”到与“blind”、“cartwheel”等稀有动作直接对应的运动片段，从而为后续生成提供高信噪比的运动提示。

### 2. 对齐方式：从单粒度NCE到双粒度NCE+Banzhaf交互损失

现有方法仅依赖全局NCE对比损失实现文本与运动的粗粒度对齐，这种实体级对齐掩盖了文本片段与运动片段之间的细粒度对应关系。MOST在保留全局NCE损失的基础上，新增了**片段级Banzhaf交互损失** $\mathcal{L}_{\mathrm{B}}$，形成双粒度对齐机制。

该机制的工作原理如下（见公式(9)-(14)）：
- 将文本片段与运动片段视为合作博弈中的“玩家”，通过定义的收益价值函数 $v$ 计算每个片段联盟的边际贡献；
- 收益函数引入**泛化度比率矩阵** $\mathbf{W}$，根据片段内相邻帧的平均绝对差异量化信息丰富度，对高冗余片段自动降权；
- Banzhaf交互预测器输出每对文本‑运动片段的交互值 $I(\{i,j\})$，并通过交叉熵损失约束其与真实交互值对齐。

这一设计的深层洞察在于：稀有动作的语义线索往往隐藏在文本的特定短语与运动的特定片段之间的协作关系中，只有通过片段级的交互建模才能捕捉这种多对多的协作模式。

### 3. 收益函数设计：从简单相似度到泛化度比率加权

现有方法在计算跨模态相似度时通常直接使用余弦相似度或点积，未考虑不同片段的信息丰富度差异。MOST在收益函数中引入**泛化度比率** $\mathbf{W} = \mathbf{W}_m (\mathbf{W}_w)^{\top}$（公式(10)-(12)）：

$$
\mathbf{W}_w = \frac{1}{l_w} \sum_{j=2}^{l_w} |t^j - t^{j-1}|, \quad \mathbf{W}_m = \frac{1}{l_m} \sum_{j=2}^{l_m} |m^j - m^{j-1}|
$$

该比率通过计算片段内相邻帧的平均绝对差异来反映信息丰富度：值越低表示片段内变化越小、冗余度越高。将其作为相似度矩阵 $A$ 的权重，使得高冗余片段在Banzhaf交互计算中的贡献被自动抑制，从而引导检索过程聚焦于包含丰富运动信息的关键片段。

### 4. 运动提示构建：从单一序列条件到Banzhaf加权多片段融合

现有方法通常直接使用检索到的整个运动序列或单一序列作为扩散模型的条件输入。MOST设计了**运动提示模块**（Motion Prompt Module），根据Banzhaf交互值对top-K检索片段进行softmax加权融合（公式(17)）：

$$
R_i = \sum_{m=1}^{K_c} \frac{\exp(B_m) r_m}{\sum_{n=1}^{K_c} \exp(B_n)}
$$

这一设计使运动提示能够自适应地整合多个关键片段的运动信息，Banzhaf值越高的片段对最终运动提示的贡献越大。消融实验证实，该融合方式（交叉注意力）相比简单的特征拼接，在KIT-ML上FID从0.19降至0.13，MM Dist从2.83降至2.79。

### 创新总结

上述四个维度的改变共同构成了一个因果链条：**片段级检索消除冗余 → 双粒度对齐捕捉细粒度协作 → 泛化度加权抑制噪声 → 多片段融合增强语义覆盖**。这一链条使MOST在稀有文本尾部（Tail 0-5%）上的FID和W-MM Dist显著优于现有方法（HumanML3D上FID降至0.66，W-MM Dist降至16.80），验证了从合作博弈论视角解决跨模态细粒度对齐问题的有效性。



MOST 采用**检索‑生成两阶段框架**，从根本上重塑了文本驱动运动扩散模型的输入条件构建方式。其核心设计动机源于一个被现有方法普遍忽视的瓶颈：当面对稀有文本时，基于全序列检索的生成范式会引入大量运动冗余，粗粒度的实体级对齐掩盖了关键语义线索，导致模型无法有效捕捉稀有动作的细粒度对应关系。

框架的整体信息流如 **Figure 3** 所示，可分为两个紧密协作的阶段：

![[assets/figures/papers/paper_list_l1835_MOST_Motion_Diffusion_Model_for_Rare_Text_via_Temporal_Clip_Banzhaf_Inte/figures/003_Figure_3.jpg]]
*Figure 3: Overview of our MOST. This figure illustrates the reverse denoising process of the motion diffusion model. The first step is using Text-to-Motion Retrieval to obtain motion clips. These clips along with motion and text prompts are then leveraged in the Text-to-Motion Generation stage to generate motion*

**第一阶段：文本‑运动检索。** 该阶段摒弃了传统的“文本→完整运动序列”检索范式，转而引入**时间片段Banzhaf交互**机制，在片段级别建立文本与运动的多对多协作关系。具体而言，文本和运动序列分别被分割为时间片段，并被视为合作博弈中的“玩家”；通过计算每个片段联盟的边际贡献，量化跨模态细粒度一致性。配合基于泛化度比率的收益函数，该机制能够自动抑制冗余片段的权重，使检索聚焦于与文本语义高度相关的关键运动片段。检索阶段通过双粒度对齐目标进行训练：实体级NCE损失保证整体语义一致性，片段级Banzhaf交互损失实现细粒度对齐。

**第二阶段：文本‑运动生成。** 该阶段以扩散模型为核心，将第一阶段检索到的关键运动片段作为生成指引。运动提示模块根据Banzhaf交互值对top‑K片段进行softmax加权融合，生成紧凑的运动提示表示。在扩散逆向过程中，运动变换器解码器同时接收文本特征和运动提示，通过交叉注意力机制逐步去噪，最终生成与输入文本语义一致的运动序列。

两阶段设计的关键因果链条在于：通过合作博弈论中的Banzhaf交互机制在片段级别精准捕获文本‑运动对应关系，从根本上消除了全序列冗余的干扰；运动提示模块则将这种细粒度对齐信息有效注入扩散生成过程，为稀有文本条件下的高保真运动生成提供了可靠的语义指引。



MOST方法的核心在于通过合作博弈论中的**时间片段Banzhaf交互**（Temporal Clip Banzhaf Interaction）机制，在片段级别实现文本与运动的细粒度对齐，从而为扩散生成提供高保真的运动提示。本节聚焦于检索阶段的关键模块与公式推导。

### 片段生成与泛化度比率

在完成实体级整体对齐后，MOST通过一维卷积将文本和运动的帧级特征压缩为时间片段特征。为量化每个片段的信息丰富度，引入**泛化度比率**（Generalization Degree Ratio）。其核心思想是：片段内相邻帧的平均绝对差异越大，信息丰富度越高；反之则冗余度越高。

文本片段的泛化度 $\mathbf{W}_w$ 与运动片段的泛化度 $\mathbf{W}_m$ 分别计算为：

$$
\mathbf{W}_w = \frac{1}{l_w} \sum_{j=2}^{l_w} |t^j - t^{j-1}|, \quad \mathbf{W}_m = \frac{1}{l_m} \sum_{j=2}^{l_m} |m^j - m^{j-1}|
$$

其中 $l_w$ 和 $l_m$ 分别为文本片段和运动片段的帧数，$t^j$ 和 $m^j$ 为第 $j$ 帧的特征表示。最终的泛化度比率矩阵 $\mathbf{W}$ 由二者外积得到：

$$
\mathbf{W} = \mathbf{W}_m (\mathbf{W}_w)^{\top}
$$

### 收益价值函数

在合作博弈框架中，文本片段与运动片段被视作“玩家”。为评估任意玩家联盟的效用，MOST设计了基于泛化度比率加权的**收益价值函数**（Revenue Value Function）$v$：

$$
v = \frac{1}{2} \left( \frac{1}{T_m} \sum_{i=1}^{T_m} \max_j \mathbf{W} A_{ij} + \frac{1}{T_w} \sum_{j=1}^{T_w} \max_i \mathbf{W} A_{ij} \right)
$$

其中 $A_{ij}$ 为第 $i$ 个运动片段与第 $j$ 个文本片段间的余弦相似度矩阵，$T_m$ 和 $T_w$ 分别为运动和文本的片段总数。该函数通过 $\mathbf{W}$ 对相似度进行加权，使得信息丰富的片段对在博弈中获得更高权重，从而有效抑制冗余片段的干扰。

### Banzhaf交互与对齐损失

基于上述收益函数，可计算任意一对文本-运动片段 $(i, j)$ 的**Banzhaf交互值** $I(\{i,j\})$，衡量二者形成联盟后的额外合作贡献：

$$
I(\{i,j\}) = \sum_{S \subseteq N \setminus \{i,j\}} \rho(S) \left[ v(S \cup \{i,j\}) + v(S) - v(S \cup \{i\}) - v(S \cup \{j\}) \right]
$$

其中 $N$ 为全体玩家集合，$\rho(S)$ 为联盟 $S$ 的概率权重。该交互值越高，表明文本片段与运动片段之间的语义协作越紧密。

为在无需片段级标注的情况下实现细粒度对齐，MOST训练一个预测器来估计Banzhaf交互值，并通过**Banzhaf交互损失** $\mathcal{L}_{\mathrm{B}}$ 进行约束：

$$
\mathcal{L}_{\mathrm{B}} = -\sum_{i=1}^{T_s} I_{t2m}^i \log(P_{t2m}^i) - \sum_{i=1}^{T_s} I_{m2t}^i \log(P_{m2t}^i)
$$

其中 $I_{t2m}^i$ 和 $I_{m2t}^i$ 分别为文本到运动和运动到文本方向的真实Banzhaf交互值，$P_{t2m}^i$ 和 $P_{m2t}^i$ 为预测器输出。该损失本质上是一个交叉熵损失，驱动预测器输出与真实交互值对齐。

### 检索总损失

检索阶段的最终训练目标结合了实体级对齐与片段级细粒度对齐：

$$
\mathcal{L}_{\mathrm{R}} = \mathcal{L}_{\mathrm{NCE}} + \lambda_{\mathrm{B}} \mathcal{L}_{\mathrm{B}}
$$

其中 $\mathcal{L}_{\mathrm{NCE}}$ 为噪音对比估计损失，用于文本与运动的整体对齐；$\lambda_{\mathrm{B}}$ 为平衡系数。通过双粒度对齐，MOST能够在排除全序列冗余的同时，精准捕捉稀有文本与关键运动片段之间的对应关系。

### 运动提示融合

在检索到与每个文本片段最相关的 top-$K$ 运动片段后，生成阶段的**运动提示模块**根据预测的Banzhaf交互值对检索片段进行softmax加权融合，生成紧凑的运动提示 $R_i$：

$$
R_i = \sum_{m=1}^{K_c} \frac{\exp(B_m) r_m}{\sum_{n=1}^{K_c} \exp(B_n)}
$$

其中 $B_m$ 为第 $m$ 个检索片段的Banzhaf交互值，$r_m$ 为其运动特征，$K_c$ 为选取的片段数量。该融合机制确保了对生成贡献更大的关键片段获得更高权重，为后续运动变换器解码器提供高保真的生成指引。

### 补充图表

![[assets/figures/papers/paper_list_l1835_MOST_Motion_Diffusion_Model_for_Rare_Text_via_Temporal_Clip_Banzhaf_Inte/figures/004_Figure_4.jpg]]
*Figure 4: a) Text-to-Motion Retrieval. In this stage, a dual stream encoder and*

![[assets/figures/papers/paper_list_l1835_MOST_Motion_Diffusion_Model_for_Rare_Text_via_Temporal_Clip_Banzhaf_Inte/figures/001_Figure_1.jpg]]
*Figure 1: Comparison with existing T2M generation methods. a) Previous methods are limited to simple and common text prompts. b) The motion generated using text-text retrieval suffers from significant similarity between texts, leading to restricted performance. c) In contrast, our approach utilizes text-motion retrieval to leverage common motion clips as prompts for generating high-quality rare motions, effectively guiding the generation process*

![[assets/figures/papers/paper_list_l1835_MOST_Motion_Diffusion_Model_for_Rare_Text_via_Temporal_Clip_Banzhaf_Inte/figures/002_Figure_2.jpg]]
*Figure 2: Qualitative Analysis on the Motion Redundancy Problem. We depict the keyframe parts in dark brown and label the remaining parts in light brown*



## 实验与关键发现

### 主实验结果

MOST在标准基准HumanML3D和KIT‑ML上进行了全面的文本‑运动检索与生成评估。检索实验（Table I）显示，MOST在HumanML3D上取得了**6.61**的R@1，在KIT‑ML上取得了**9.87**的R@1，均优于现有检索方法。这验证了时间片段Banzhaf交互在捕捉细粒度文本‑运动对应关系上的有效性。

生成实验（Table II）进一步表明，MOST在HumanML3D上实现了**0.139**的FID和**0.783**的R‑Precision Top‑3，Multimodal Distance降至**2.732**，全面超越**ReMoDiffuse**（Zhang et al., arXiv 2023）、**FineMoGen**（Zhang et al., NeurIPS 2024）、**MMM**（Pinyoanuntapong et al., arXiv 2023）、**MotionDiffuse**（Zhang et al., TPAMI 2024）、**MLD**（Chen et al., CVPR 2023）、**Fg‑T2M**（Wang et al., ICCV 2023）、**GUESS**（Gao et al., TVCG 2024）和**TMR**（Petrovich et al., ICCV 2023）等方法。这一优势源于两方面的设计：检索阶段通过片段级Banzhaf交互排除了全序列冗余的干扰，生成阶段通过运动提示模块将检索到的高质量关键片段有效融入扩散逆向过程。

### 稀有文本泛化能力

针对稀有文本的核心挑战，MOST在HumanML3D和KIT‑ML的稀有尾部（Tail 0–5%）上进行了专门评估。在HumanML3D的0–5%尾部，MOST取得了**0.66**的生成FID和**16.80**的加权MM距离（W‑MM Dist）；在KIT‑ML的0–5%尾部，FID达到**7.34**。这些结果表明，时间片段Banzhaf交互能够从有限训练样本中精准定位关键运动片段，有效缓解了稀有文本条件下因全序列检索引入运动冗余而导致的语义退化问题。

### 消融与组件分析

消融实验（Table V）系统验证了各模块的贡献：

- **Banzhaf检索 vs. 基础检索**：采用Banzhaf交互（Ban.）的检索策略相比基础检索（Base），在HumanML3D上将T2M检索R@1提升约1%，中位排名从29降至25，证明片段级细粒度对齐显著改善了检索精度。
- **关键片段 vs. 完整序列**：使用关键运动片段（39帧，5个片段）作为运动提示，相比使用完整运动序列，在KIT‑ML上取得了更优的FID和MM Dist表现，直接验证了消减运动冗余对生成质量的正面影响。
- **交叉注意力 vs. 特征拼接**：运动变换器解码器中采用交叉注意力（cross‑attention）融合运动提示优于特征拼接（concat），在KIT‑ML上FID从0.19降至0.13，MM Dist从2.83降至2.79，表明交叉注意力机制能更有效地建模文本条件与多片段运动提示之间的交互关系。
- **片段数与提示运动数**：MOST完整配置（运动片段数S=5，提示运动数N=2）在全部文本及稀有文本上均取得最佳FID与MM Dist，减少任一参数均导致性能下降，验证了多片段、多提示融合策略的必要性。

### 运动冗余评估

Figure 5展示了运动冗余的定量评估。通过比较运动提示序列长度与平均运动特征相似度 $S_{ave}$（公式20），MOST在图中更接近左上角区域，表明其生成的提示运动在保持紧凑的同时具有更高的特征多样性。这直接归因于泛化度比率矩阵 $\mathbf{W}$ 在收益价值函数（公式12）中对信息丰富片段的加权作用，有效抑制了冗余片段的检索权重。

### 用户研究

用户研究（Figure 6）采用盲评方式，收集多人对生成运动质量的评分（1–4分）。MOST在所有方法中获得了最高的投票分数，且统计显著性检验（p<0.01）确认了其优势的可靠性。这一结果与自动指标一致，表明MOST生成的运动在语义一致性和自然度上更符合人类感知。

![[assets/figures/papers/paper_list_l1835_MOST_Motion_Diffusion_Model_for_Rare_Text_via_Temporal_Clip_Banzhaf_Inte/figures/011_Figure_6.jpg]]
*Figure 6: The result of user study. Each bar represents the voting scores of methods, with higher values being better. The voting score ranges from 1 to 4*

### 失败模式分析

尽管整体性能优异，MOST仍存在以下典型失败模式（Figure 12）：

![[assets/figures/papers/paper_list_l1835_MOST_Motion_Diffusion_Model_for_Rare_Text_via_Temporal_Clip_Banzhaf_Inte/figures/017_Figure_12.jpg]]
*Figure 12: Visualization of some failure cases. The arrow represents the time axes and the red box indicates the incorrect motion frames*

- **复杂长描述下的语义遗漏**：当文本包含密集动作序列时，固定的片段分割可能无法完美覆盖所有语义单元，导致部分生成的运动帧出现语义错误（红框标出）。
- **物理伪影**：即使整体运动符合文本描述，部分生成结果仍包含脚部滑动等物理不合理现象。这源于扩散模型在逆向过程中缺乏显式的物理约束。
- **数据依赖性**：Figure 13展示了数据量泛化实验——在“A person is playing ping‑pong”提示上，使用全量数据训练的模型生成了合理的乒乓球动作，而使用随机丢弃一半数据的子集训练时，生成质量明显下降。这表明MOST的稀有文本泛化能力仍受训练数据规模的制约。

### 补充图表

![[assets/figures/papers/paper_list_l1835_MOST_Motion_Diffusion_Model_for_Rare_Text_via_Temporal_Clip_Banzhaf_Inte/figures/005_Table.jpg]]
*Table: TEXT-TO-MOTION RETRIEVAL RESULTS ON BOTH THE KIT-ML AND HUMANML3D DATASETS. BEST RESULTS ARE BOLDED*

![[assets/figures/papers/paper_list_l1835_MOST_Motion_Diffusion_Model_for_Rare_Text_via_Temporal_Clip_Banzhaf_Inte/figures/006_Table.jpg]]
*Table: II*

![[assets/figures/papers/paper_list_l1835_MOST_Motion_Diffusion_Model_for_Rare_Text_via_Temporal_Clip_Banzhaf_Inte/figures/008_Table.jpg]]
*Table: EVALUATION OF GENERALIZATION ABILITY ON HUMANML3D AND KIT-ML DATASETS. WE REPORT THE BEST RESULTS IN BOLDED*

![[assets/figures/papers/paper_list_l1835_MOST_Motion_Diffusion_Model_for_Rare_Text_via_Temporal_Clip_Banzhaf_Inte/figures/010_Table.jpg]]
*Table: ABLATION ANALYSIS AND COMPONENT ANALYSIS ON KIT-ML DATASET. “R” DENOTES THE RETRIEVAL STRATEGY. “BANZHAF” AND “BASE” REPRESENTS WITH AND WITHOUT BANZHAF INTERACTION, RESPECTIVELY. “S” IS THE MOTION CLIPS NUMBER. “N” INDICATES THE PROMPT MOTIONS NUMBER. “M” INDICATES THE UTILIZATION OF MOTION CLIPS OR ENTIRE MOTION IN MOTION PROMPT MODULE*

![[assets/figures/papers/paper_list_l1835_MOST_Motion_Diffusion_Model_for_Rare_Text_via_Temporal_Clip_Banzhaf_Inte/figures/012_Figure_7.jpg]]
*Figure 7: Visual results compared with existing methods. The first line is the generated result on the rare text “blind”. The second line is the generated result of complex action combinations*

![[assets/figures/papers/paper_list_l1835_MOST_Motion_Diffusion_Model_for_Rare_Text_via_Temporal_Clip_Banzhaf_Inte/figures/018_Figure_13.jpg]]
*Figure 13: The generated result for the sentence “A person is playing ping-pong." The left figure shows the result trained on the all data, while the right figure shows the result trained on a sub-dataset with half of the data randomly dropped*



## 定位与知识库关联

### 1. 核心瓶颈与突破路径

现有文本驱动运动生成（Text-to-Motion, T2M）方法在处理稀有文本时面临一个关键瓶颈：**全序列检索引入大量运动冗余，粗粒度的实体级对齐掩盖了关键语义线索**。具体而言，当文本描述包含罕见动作（如“blind”、“performing lunges”）时，传统方法倾向于检索整个运动序列作为生成条件，而序列中大量与目标语义无关的冗余帧会稀释关键运动信息，导致生成的运动缺乏语义一致性。

MOST 的核心突破在于引入**合作博弈论中的时间片段Banzhaf交互机制**，将文本与运动片段视为合作博弈中的玩家，通过精确计算每个片段联盟的边际贡献来量化跨模态细粒度一致性。这一机制从根本上改变了检索与对齐的粒度：从“整个运动序列-整句文本”的实体级匹配，转变为“关键运动片段-文本片段”的片段级多对多协作匹配。配合基于**泛化度比率**的收益函数设计，模型能够自动降低冗余片段的权重，聚焦于信息丰富且语义相关的核心运动线索。

### 2. 与基线方法的关系定位

MOST 建立在文本条件运动扩散模型的成熟范式之上，但其创新点与现有方法形成了清晰的差异化定位：

| 方法 | 检索/对齐粒度 | 核心机制 | 与 MOST 的关系 |
|------|--------------|---------|---------------|
| **MotionDiffuse** (Zhang et al., TPAMI 2024) | 无显式检索 | 基础文本条件扩散 | MOST 的生成阶段继承了其扩散框架，但增加了运动提示模块 |
| **MLD** (Chen et al., CVPR 2023) | 无显式检索 | 潜在空间扩散 | 同为扩散范式，MOST 在潜在空间之外引入了显式检索增强 |
| **ReMoDiffuse** (Zhang et al., arXiv 2023) | 全序列检索 | 检索增强扩散 | MOST 的直接对比对象；MOST 将检索粒度从全序列细化为关键片段 |
| **FineMoGen** (Zhang et al., NeurIPS 2024) | 细粒度时空编辑 | 扩散模型 | 同关注细粒度，但 MOST 侧重检索阶段的片段对齐，FineMoGen 侧重编辑 |
| **Fg-T2M** (Wang et al., ICCV 2023) | 句法结构引导 | 细粒度扩散 | 同追求细粒度生成，但 Fg-T2M 依赖句法解析，MOST 依赖博弈论对齐 |
| **MMM** (Pinyoanuntapong et al., arXiv 2023) | 无检索 | 掩码运动建模 | 范式不同（离散Token vs 连续扩散），但 MOST 的片段选择与其掩码策略有概念呼应 |
| **GUESS** (Gao et al., TVCG 2024) | 无检索 | 级联扩散逐步丰富 | 同为逐步生成策略，MOST 的片段融合可视为一种隐式的逐步丰富 |
| **TMR** (Petrovich et al., ICCV 2023) | 文本-运动检索 | 对比生成模型 | MOST 检索阶段的实体对齐部分与 TMR 的对比学习范式一致 |

**关键差异化槽位**：
- **检索对象与粒度**：从整个运动序列（ReMoDiffuse等）变为关键运动片段，通过Banzhaf交互筛选。
- **跨模态对齐方式**：从仅全局NCE损失（ReMoDiffuse等）变为全局NCE损失 + 片段级Banzhaf交互损失的双粒度对齐。
- **收益函数设计**：从仅依赖余弦相似度变为引入泛化度比率矩阵 $\mathbf{W}$，根据信息丰富度加权相似度。
- **运动提示构建**：从直接使用检索到的整个运动序列变为运动提示模块根据Banzhaf权重对top-K片段进行softmax融合。

### 3. 方法适用边界

**适用场景**：
- 稀有文本驱动的运动生成，特别是训练数据中低频出现的动作描述。
- 需要细粒度语义对齐的多模态生成任务，其中关键语义仅体现在序列的局部片段中。
- 存在大量运动冗余的检索增强生成场景。

**不适用或需谨慎使用的场景**：
- 端到端部署需求强烈的场景：MOST采用独立的两阶段训练与推理流程，相比端到端方法增加了部署与维护复杂度。
- 极其复杂的长描述：固定的片段分割可能无法完美覆盖所有语义单元，导致部分生成的运动帧出现语义错误。
- 训练数据极度稀缺的场景：模型的泛化能力受训练数据规模影响显著，当训练数据量减少时，稀有文本的检索与生成质量均会明显下降。

### 4. 已知局限与失败模式

1. **两阶段流程的工程复杂性**：检索与生成分离训练，推理时需先检索再生成，增加了计算开销和系统复杂度。

2. **片段分割的刚性**：固定的1D卷积片段划分在面对动作密集、时序关系复杂的文本时，可能无法精确捕获所有语义单元，导致生成的运动在局部帧上出现语义偏差（如Figure 12所示的失败案例，红框标出错误运动帧）。

3. **物理合理性不足**：即使整体运动符合文本描述，部分生成结果仍可能包含物理伪影，如脚部滑动等不合理现象。这是当前运动扩散模型的共性问题，MOST并未针对性地解决。

4. **数据依赖性**：Banzhaf交互预测器的训练依赖于足够的文本-运动配对数据。在数据量减半的子数据集上，稀有文本的生成质量明显下降（如Figure 13所示，“playing ping-pong”的生成结果出现退化）。

### 5. 开放问题与未来方向

1. **端到端统一框架**：能否设计一个端到端的统一框架，将检索与生成整合为单一可训练模型，简化两阶段流程的同时保持细粒度对齐能力？

2. **大规模语言模型集成**：如何利用LLMs对稀有文本进行改写或语义扩展，使其更易于检索模型处理，从而间接提升稀有文本的生成质量？

3. **动态片段分割**：能否引入自适应或可学习的片段分割机制，替代固定的1D卷积划分，以更好地应对长度不一、动作密度各异的复杂描述？

4. **物理约束引入**：在生成过程中加入物理约束或后处理模块（如足部接触约束、关节角度限制），能否有效消除脚部滑动等伪影？

5. **Banzhaf预测器的改进**：当前预测器仅使用交叉熵损失训练，是否可以通过更严格的对齐目标（如排序损失、对比损失）或自监督信号进一步提升其准确性？

6. **跨任务迁移**：该框架中的合作博弈思想——将多模态序列片段视为玩家并计算其交互贡献——能否推广到音乐驱动运动合成、视频-文本对齐等其他多模态生成与理解任务？



## 原文 PDF

![[paperPDFs/arxiv_2025/MOST_Motion_Diffusion_Model_for_Rare_Text_via_Temporal_Clip_Banzhaf_Interaction.pdf]]
