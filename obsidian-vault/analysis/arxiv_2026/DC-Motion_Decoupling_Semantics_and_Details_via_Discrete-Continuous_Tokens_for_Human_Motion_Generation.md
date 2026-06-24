---
title: "DC-Motion: Decoupling Semantics and Details via Discrete-Continuous Tokens for Human Motion Generation"
type: paper
paper_level: A
venue: arXiv
year: 2026
pdf_ref: paperPDFs/arxiv_2026/DC-Motion_Decoupling_Semantics_and_Details_via_Discrete-Continuous_Tokens_for_Human_Motion_Generation.pdf
project_link: null
code_link: null
aliases:
- DM
- DC-Motion
tags:
- arxiv_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
- topic/generative_models_diffusion
core_operator: 采用离散-连续混合令牌（DC-VAE）将运动分解为语义结构令牌与高频残差，并通过两阶段生成（MaskGIT负责全局语义规划，残差扩散恢复物理细节）实现解耦。
primary_logic: 将人体运动生成显式解耦为语义结构规划与物理细节精修，利用离散令牌建模高层语义与时间布局，连续残差保留关节平滑性等高频动态，从而在语义对齐和运动保真度之间取得最优平衡。
claims:
- 在HumanML3D和KIT-ML上，DC-Motion取得了当时最优的FID（0.041和0.148）和R-Precision，验证了运动真实感和文本对齐能力。
- 消融实验表明，移除连续残差分支导致重建MPJPE升至41.7，移除离散分支导致生成FID升至0.081，证明两个分支的必要性。
- MaskGIT在长序列和复杂指令上的R@1显著优于标准自回归模型，验证了双向注意力迭代掩码预测的有效性。
- DC-VAE重建FID为0.014，MPJPE为25.8，接近连续模型，远优于纯离散VQ-VAE（MPJPE 41.7），有效补偿了离散化信息损失。
---

# DC-Motion: Decoupling Semantics and Details via Discrete-Continuous Tokens for Human Motion Generation

> [!tip] 核心洞察
> 将人体运动生成显式解耦为语义结构规划与物理细节精修，利用离散令牌建模高层语义与时间布局，连续残差保留关节平滑性等高频动态，从而在语义对齐和运动保真度之间取得最优平衡。

| 字段 | 内容 |
|------|------|
| 中文题名 | DC-Motion: 通过离散-连续令牌解耦语义与细节的人体运动生成 |
| 英文题名 | DC-Motion: Decoupling Semantics and Details via Discrete-Continuous Tokens for Human Motion Generation |
| 会议/期刊 | arXiv 2026 |
| Links | [paper](https://arxiv.org/abs/2606.14721) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction #topic/generative_models_diffusion |
| Method | DC-Motion |
| Dataset | HumanML3D, KIT-ML |

> [!tip] 效果简介
> - HumanML3D 上，FID 0.041 ± .002 vs previous SOTA (new SOTA)；R Precision Top-1 0.528 ± .002 vs previous SOTA (new SOTA)。
> - KIT-ML 上，FID 0.148 ± .008 vs previous SOTA (new SOTA)；R Precision Top-1 0.442 ± .005 vs previous SOTA (new SOTA)。

## 概述

人体运动生成的核心瓶颈在于**语义理解与物理细节的同质化建模**。现有方法或采用纯连续扩散模型（如 **MLD** (Chen et al., CVPR 2023)、**MDM** (Tevet et al., arXiv 2022)），虽能保留关节平滑性等高频动态，却在复杂组合语义推理上受限；或采用纯离散自回归模型（如 **T2M-GPT** (Zhang et al., CVPR 2023)、**MoMask** (Guo et al., CVPR 2024)），虽擅长高层语义规划，却因向量量化造成细粒度物理细节丢失。这一矛盾使得单一表示空间难以同时兼顾运动真实感与文本对齐精度。

DC-Motion 提出**离散-连续解耦生成框架**，将运动显式分解为语义结构与物理细节两个层次，分别用不同机制处理。其核心思路是：首先通过 DC-VAE 将运动编码为离散语义令牌与连续残差，前者捕获高层语义和时间布局，后者保留量化损失的高频动态；随后采用两阶段生成——MaskGIT 以双向注意力迭代掩码预测生成全局语义令牌序列，残差扩散模型在固定结构先验上恢复物理细节。这种解耦设计使语义规划与细节精修各司其职，从根本上缓解了单一空间的信息折衷。

在 HumanML3D 和 KIT-ML 两个基准上，DC-Motion 取得了当时最优的 FID（0.041 和 0.148）与 R-Precision，验证了运动真实感和文本对齐能力的双重提升。消融实验进一步证实：移除连续残差分支使重建 MPJPE 从 25.8 升至 41.7，移除离散分支使生成 FID 从 0.041 升至 0.081，表明两个分支对最终性能均有不可替代的贡献。

## 背景与动机

人体运动生成旨在根据文本描述合成逼真的三维人体动作序列，是计算机视觉与图形学交叉领域的研究热点。近年来，扩散模型和自回归模型在该任务上取得了显著进展，代表性工作包括基于连续潜在扩散的 **MLD**（Chen et al., CVPR 2023）、基于运动扩散的 **MDM**（Tevet et al., arXiv 2022），以及基于离散令牌建模的 **T2M-GPT**（Zhang et al., CVPR 2023）和 **MoMask**（Guo et al., CVPR 2024）。然而，现有方法在表示空间的选择上存在一个根本性的两难困境。

### 现有方法的瓶颈：同质表示空间的内在矛盾

当前主流方法均采用单一表示空间——要么是纯连续潜在空间，要么是纯离散令牌空间。这两种选择各自面临难以调和的问题：

- **纯连续扩散模型**（如MLD、MDM）在保留运动细节方面表现优异，能够生成平滑、高保真的关节轨迹。但其连续表示缺乏显式的语义结构，导致模型在进行复杂的组合语义推理时能力受限——例如，难以精确控制“先向前走两步，然后举起右手”这类具有时序逻辑的长指令。
- **纯离散自回归模型**（如T2M-GPT、MoMask）通过向量量化将运动压缩为离散码本索引，天然适合进行语义层面的全局规划。然而，量化过程不可避免地丢失高频物理细节，导致生成的运动出现关节抖动、接触滑步等伪影，运动保真度下降。

这一瓶颈的本质在于：人体运动天然具有层次化特性——全局语义结构（如动作类型、时序布局）需要离散化以支持组合推理，而局部物理细节（如关节平滑性、速度连续性）则需要连续表示以保留精度。单一表示空间无法同时满足这两个层次的需求。

### 核心动机：语义与细节的显式解耦

针对上述困境，DC-Motion 提出了一种全新的生成范式：将人体运动生成显式解耦为**语义结构规划**与**物理细节精修**两个阶段。其核心洞察在于：

> 利用离散令牌建模高层语义与时间布局，利用连续残差保留关节平滑性等高频动态，从而在语义对齐和运动保真度之间取得最优平衡。

这一设计使得模型能够像“先勾勒骨架，再填充血肉”一样，分阶段完成运动生成——语义规划阶段专注于文本-运动对齐和全局时序推理，物理精修阶段则专注于恢复被量化丢弃的细粒度动态信息。

### 技术挑战

实现上述解耦需要解决两个关键技术挑战：（1）如何设计一个统一的运动表示框架，将运动序列分解为离散语义令牌与连续残差，且两者能够无缝融合重建；（2）如何设计对应的生成流水线，使语义规划与细节精修各司其职、协同工作。DC-Motion 通过 DC-VAE 分词器与 MaskGIT + 残差扩散的两阶段生成框架系统性地回应了这些挑战。

## 核心创新

DC-Motion 的核心创新在于**将人体运动生成显式解耦为语义结构规划与物理细节精修两个子问题**，并通过离散-连续混合令牌（DC-VAE）和分阶段生成框架实现这一解耦。与现有方法使用同质表示空间（纯连续扩散或纯离散自回归）不同，DC-Motion 识别出单一表示空间的根本瓶颈：连续扩散模型难以进行复杂的组合语义推理，而离散自回归模型因向量量化导致细粒度物理细节丢失。

### 关键 changed slots

**运动表示空间：从单一令牌到解耦令牌**

现有方法要么采用纯连续潜在空间（如 **MLD**，Chen et al., CVPR 2023），要么采用纯离散令牌（如 **T2M-GPT**，Zhang et al., CVPR 2023）。DC-Motion 提出 DC-VAE，将运动分解为两个互补的表示分量：

- **离散语义令牌** $z_q$：通过可学习码本 $C = \{e_k\}_{k=1}^K$ 对编码器输出 $z = E_\theta(x)$ 进行向量量化得到（Eq. 2-3），捕获高层次的语义结构和时间布局。
- **连续残差** $r = z - z_q$（Eq. 4）：保留量化过程中丢失的高频物理细节，如关节平滑性和精细动态。

这一设计的因果机制在于：离散令牌天然适合建模类别化语义和全局时间结构，而连续残差补偿了离散化带来的信息损失。消融实验直接验证了这一点——移除连续残差分支后，重建 MPJPE 从 25.8 升至 41.7（Table 3），证明残差对物理细节保留至关重要；移除离散分支后，生成 FID 从 0.041 升至 0.081（Table 3），证明离散令牌对全局结构和语义对齐的关键作用。

**生成范式：从单一模型到分阶段解耦生成**

现有方法使用单一扩散或自回归模型生成全部运动细节。DC-Motion 将生成过程分解为两个阶段：

- **MaskGIT 生成器**（Sec. 3.3.1）：在压缩的离散语义空间（$N=16$）中，通过双向注意力机制和迭代掩码预测生成语义令牌序列，负责全局语义规划。与标准自回归模型（Standard AR）相比，MaskGIT 避免了暴露偏差问题，在长序列 R@1 上从 0.574 提升至 0.623，Overall R@1 从 0.611 提升至 0.642（Table 4）。
- **残差扩散模型**（Sec. 3.3.2）：以文本条件 $c$ 和已生成的离散结构表示 $z_q$ 为联合条件，对连续残差 $r$ 进行扩散去噪（Eq. 10-12），仅负责恢复高频物理细节。

这种分阶段设计的核心洞察在于：语义结构规划需要全局感受野和组合推理能力（MaskGIT 的双向注意力提供），而物理细节精修是局部连续优化问题（轻量残差扩散足够胜任）。最终生成的运动由 $\hat{x} = D_\theta(\hat{z}_q + \hat{r})$ 融合解码（Eq. 13）。

### 与 baseline 的本质差异

| 维度 | 连续扩散 baseline（MLD/MDM） | 离散 baseline（T2M-GPT/MoMask） | DC-Motion |
|------|------------------------------|--------------------------------|-----------|
| 表示空间 | 纯连续潜在空间 | 纯离散令牌 | 离散语义令牌 + 连续残差 |
| 语义建模 | 扩散隐式建模，组合推理弱 | 自回归显式建模，存在暴露偏差 | MaskGIT 双向注意力，迭代掩码预测 |
| 物理细节 | 扩散直接生成，保真度中等 | 量化丢失细节，存在抖动 | 残差扩散精修，补偿量化损失 |
| 长序列能力 | 受限于扩散时间轴建模 | 暴露偏差累积 | 压缩空间全局建模 + 残差局部精修 |

DC-Motion 在 HumanML3D 上取得 FID 0.041、R Precision Top-1 0.528，在 KIT-ML 上取得 FID 0.148、R Precision Top-1 0.442（Table 1-2），均达到当时最优水平，验证了解耦设计在运动真实感和文本对齐之间取得最优平衡的核心主张。

## 整体框架

DC-Motion 提出了一种**分解式生成框架**，其核心思想是将人体运动生成显式解耦为两个层次：高层语义结构规划与低层物理细节精修。这一设计的直接动机是解决现有方法因使用同质表示空间而无法同时兼顾语义推理与运动保真度的瓶颈——连续扩散模型难以进行复杂的组合语义推理，而离散自回归模型则因向量量化导致细粒度关节动态丢失。

### 三阶段训练与推理流水线

整个框架由三个核心模块串联构成，训练与推理均遵循统一的解耦范式：

1.  **DC-VAE Tokenizer**：作为运动表示的基础设施，负责将原始运动序列 $x$ 编码为连续潜在表示 $z \in \mathbb{R}^{N \times D}$，随后通过可学习离散码本 $C = \{e_k\}_{k=1}^K$ 进行向量量化，得到离散语义令牌 $z_q$。同时，量化残差 $r = z - z_q$ 被显式保留为连续残差，用于补偿离散化造成的高频信息损失。解码器通过直通估计器（STE）融合 $z_q$ 与 $r$，重建原始运动 $\hat{x} = D_\theta(z_q + \text{sg}[z - z_q])$。该模块在训练中先行收敛，其重建质量直接决定了后续生成任务的信息上界。

2.  **MaskGIT 生成器**：负责全局语义规划。在 DC-VAE 冻结后，MaskGIT 以文本条件 $c$ 为输入，通过双向注意力机制在压缩的离散语义空间（$N=16$）上进行迭代掩码预测，逐步生成完整的离散令牌序列 $\hat{y}$。该过程采用余弦退火掩码调度，有效规避了标准自回归模型的暴露偏差问题，尤其利于长序列和复杂指令下的语义对齐。

3.  **残差扩散模型**：负责物理细节精修。在给定已生成的离散结构表示 $\hat{z}_q$ 和文本条件 $c$ 的前提下，一个轻量级扩散模型对连续残差 $\hat{r}$ 进行去噪生成。前向过程遵循标准高斯扩散 $q(r_t | r_0) = \mathcal{N}(r_t; \sqrt{\bar{\alpha}_t} r_0, (1-\bar{\alpha}_t) I)$，训练目标为 $\epsilon$-预测损失 $\mathcal{L}_{\text{diff}} = \mathbb{E}_{t,\epsilon} [\| \epsilon - \epsilon_\psi(r_t, t, c, \hat{z}_q) \|_2^2]$。最终运动由 $\hat{x} = D_\theta(\hat{z}_q + \hat{r})$ 解码得到。

### 数据流与模块关系

框架的数据流清晰体现了“先规划、后精修”的层次化生成逻辑。输入文本首先驱动 MaskGIT 在离散语义空间完成全局时间布局的推理，生成结构令牌序列；该序列作为强先验条件注入残差扩散模型，使其专注于恢复关节平滑性、接触约束等高频物理细节，而无需承担语义建模的负担。这种分工使得两个生成阶段各司其职：离散分支保障语义对齐与长时域一致性，连续分支保障运动自然度与细粒度保真度。

消融实验从因果层面验证了这一设计的必要性：若移除连续残差分支，DC-VAE 的重建 MPJPE 从 25.8 急剧上升至 41.7，表明残差是保留细粒度物理细节的关键通路；若移除离散分支，生成 FID 从 0.041 恶化至 0.081，证明离散语义令牌对全局结构和文本对齐具有不可替代的作用。

### 补充图表

![[assets/figures/papers/paper_list_l2_https_arxiv_org_abs_2606_14721/figures/002_Figure_2.jpg]]
*Figure 2: DC-Motion consists of a DC-VAE tokenizer (Sec. 3.1), a masked autoregressive generator*

## 核心模块与公式推导

DC-Motion 的核心架构由三个关键模块构成：DC-VAE 分词器、MaskGIT 语义生成器和残差扩散模型。其设计原则是将运动生成显式解耦为语义结构规划与物理细节精修两个阶段。

### DC-VAE 分词器：离散-连续解耦表示

DC-VAE 分词器是框架的基础，负责将原始运动序列映射为离散语义令牌与连续残差的混合表示。

**编码过程**：给定输入运动序列 $x$，编码器 $E_{\theta}$ 将其映射到连续潜在空间：

$$z = E_{\theta}(x) \in \mathbb{R}^{N \times D}$$

其中 $N$ 为下采样后的序列长度（实验中固定为 $N=16$），$D$ 为潜在维度。

**离散化与残差提取**：引入可学习的离散码本 $C = \{e_k\}_{k=1}^K$，其中 $e_k \in \mathbb{R}^D$。对每个潜在 token $z_i$ 进行向量量化，通过最近邻查找获得离散结构表示：

$$y_i = \arg\min_{k\in\{1,...,K\}} \| z_i - e_k \|_2^2, \quad z_{q,i} = e_{y_i}$$

离散令牌 $z_q$ 捕获高层语义结构和时间布局。量化过程不可避免地丢失细粒度信息，为此显式保留连续残差：

$$r = z - z_q \in \mathbb{R}^{N \times D}$$

残差 $r$ 编码高频物理细节（如关节平滑性、微小运动抖动），补偿量化误差。

**解码与直通估计**：解码时，使用直通估计器（STE）融合结构令牌与残差，通过解码器 $D_{\theta}$ 重构运动：

$$\tilde{z} = z_q + \mathrm{sg}[z - z_q], \quad \hat{x} = D_{\theta}(\tilde{z})$$

其中 $\mathrm{sg}[\cdot]$ 表示停止梯度操作，使离散化过程可端到端训练。

### MaskGIT 语义生成器：双向注意力掩码预测

语义生成阶段采用 MaskGIT 范式，在压缩的离散语义空间进行全局建模。与标准自回归模型不同，MaskGIT 使用双向注意力机制，通过迭代掩码预测生成完整的离散令牌序列 $\hat{y}$。

训练时，随机掩码部分令牌，模型学习根据文本条件 $c$ 和可见令牌 $\tilde{y}$ 预测被掩码位置的语义索引。损失函数为掩码位置的交叉熵：

$$\mathcal{L}_{\mathrm{ar}} = -\sum_{i=1}^N (1-m_i) \log p_{\phi}(y_i \mid \tilde{y}, c)$$

其中 $m_i$ 为掩码指示符。推理时，从全掩码序列开始，按照余弦退火调度逐步减少掩码比例，迭代预测直至生成完整序列（见 Figure 3）。

![[assets/figures/papers/paper_list_l2_https_arxiv_org_abs_2606_14721/figures/003_Figure_3.jpg]]
*Figure 3: An Overview of the MaskGIT Inference Process*

### 残差扩散模型：条件细粒度去噪

残差扩散模型在固定结构先验上对连续残差进行扩散去噪。前向过程逐步向真实残差 $r_0$ 注入高斯噪声：

$$q(r_t | r_0) = \mathcal{N}(r_t; \sqrt{\bar{\alpha}_t} r_0, (1-\bar{\alpha}_t) I)$$

训练时使用等价采样公式生成加噪残差：

$$r_t = \sqrt{\bar{\alpha}_t} r_0 + \sqrt{1-\bar{\alpha}_t} \epsilon, \quad \epsilon \sim \mathcal{N}(0, I)$$

去噪网络 $\epsilon_{\psi}$ 以文本条件 $c$ 和离散结构表示 $z_q$ 为联合条件，预测注入的噪声：

$$\mathcal{L}_{\mathrm{diff}} = \mathbb{E}_{t,\epsilon} \left[ \| \epsilon - \epsilon_{\psi}(r_t, t, c, z_q) \|_2^2 \right]$$

### 最终运动重建

推理时，将 MaskGIT 预测的离散令牌 $\hat{z}_q$ 与扩散模型去噪后的残差 $\hat{r}$ 相加，通过共享的 DC-VAE 解码器得到最终运动序列：

$$\hat{x} = D_{\theta}(\hat{z}_q + \hat{r})$$

完整推理流程见 Algorithm 1。

### 设计要点

三个模块的分阶段训练策略是方法成功的关键：先训练 DC-VAE 分词器建立解耦表示空间，再冻结分词器训练 MaskGIT 语义生成器，最后冻结前两者训练轻量级残差扩散模型。这种解耦训练范式确保各模块专注于各自的任务——语义规划与物理精修，避免优化冲突。

## 实验与分析

### 核心性能验证

DC-Motion在HumanML3D和KIT-ML两个主流基准上均取得了当时最优的整体性能，验证了离散-连续解耦表示在运动真实感和文本对齐之间的有效平衡。

在**HumanML3D**数据集上（Table 1），DC-Motion的FID达到**0.041 ± .002**，R Precision Top-1达到**0.528 ± .002**，两项核心指标均刷新了生成模型的最优记录。相比连续扩散基线**MLD**（Chen et al., CVPR 2023）和纯离散基线**MoMask**（Guo et al., CVPR 2024），DC-Motion在语义对齐（R Precision）和运动保真度（FID）上实现了同步超越，表明解耦策略避免了单一表示空间的固有局限——连续模型难以进行复杂组合语义推理，离散模型则因量化损失导致物理细节退化。

![[assets/figures/papers/paper_list_l2_https_arxiv_org_abs_2606_14721/figures/004_Table_1.jpg]]
*Table 1: Quantitative comparison on the HumanML3D dataset. Bold and underline indicate the best and second-best results among generative models. Our DC-Motion sets a new state-of-the-art across multiple metrics, including text-motion alignment (R Precision) and motion fidelity (FID)*

在**KIT-ML**数据集上（Table 2），DC-Motion同样取得FID **0.148 ± .008**和R Precision Top-1 **0.442 ± .005**的最优结果，跨数据集的一致性验证了方法的泛化能力。值得注意的是，KIT-ML的文本标注更简洁且运动序列更短，DC-Motion在此场景下仍保持优势，说明离散语义令牌对高层结构的捕获不依赖于特定数据分布。

![[assets/figures/papers/paper_list_l2_https_arxiv_org_abs_2606_14721/figures/005_Table_2.jpg]]
*Table 2: Quantitative comparison on the KIT dataset. Following previous works, certain Real attributes are omitted. Our DC-Motion sets a new state-of-the-art across multiple metrics, including text-motion alignment (R Precision) and motion fidelity (FID)*

定性比较（Figure 4）进一步佐证了量化结论：DC-Motion生成的关健帧在复杂语言描述下的运动语义对齐优于基线方法，同时关节运动的平滑性和物理合理性保持较好，未出现纯离散方法常见的抖动伪影。

![[assets/figures/papers/paper_list_l2_https_arxiv_org_abs_2606_14721/figures/006_Figure_4.jpg]]
*Figure 4: Visual comparisons of key frames on the HumanML3D testset. Compared to baselines, DC-Motion generates higherfidelity motions with superior alignment to complex language descriptions*

### 解耦机制消融

DC-VAE的消融实验（Table 3）直接揭示了离散令牌与连续残差各自的因果贡献：

![[assets/figures/papers/paper_list_l2_https_arxiv_org_abs_2606_14721/figures/007_Table_3.jpg]]
*Table 3: Ablation study of DC-VAE tokenizer on HumanML3D. We analyze the effect of discrete tokens and continuous residuals*

- **移除连续残差分支（w/o Residual）**：重建MPJPE从25.8急剧升至41.7，FID从0.014升至0.051。这表明离散令牌虽能捕获全局结构，但单独依赖量化表示会导致细粒度关节动态信息严重丢失，残差分支是补偿量化误差、保留物理细节的关键组件。

- **移除离散分支（w/o Discrete）**：生成FID从0.041升至0.081，语义对齐指标同步下降。这证明在没有离散语义令牌提供全局结构先验时，纯连续生成缺乏高层语义规划能力，运动序列的文本一致性和时间布局均受显著影响。

- **完整DC-VAE**的重建FID为0.014，MPJPE为25.8，接近连续VAE水平，远优于纯离散VQ-VAE（MPJPE 41.7），验证了混合令牌设计有效弥合了离散化带来的信息损失。

### 生成范式消融

Table 4对比了MaskGIT与标准自回归（Standard AR）在离散语义令牌生成上的表现差异：

- **全局语义对齐**：MaskGIT的Overall R@1达到0.642，相较标准AR的0.611有显著提升；FID从0.213降至0.182。这归因于MaskGIT采用双向注意力机制进行全局条件建模，而标准AR的逐帧因果生成存在暴露偏差，难以在生成早期建立完整的时间上下文。

- **长序列与复杂指令**：MaskGIT在长序列子集上的R@1从0.574提升至0.623，验证了迭代掩码预测策略在长时间轴上的语义一致性优势。标准AR模型在长序列上累积误差更严重，而MaskGIT通过多轮并行精炼有效缓解了这一问题。

### 失败模式与局限

尽管DC-Motion在标准基准上表现优异，其设计仍存在明确边界：

1. **序列长度约束**：当前框架受限于训练数据中的最大序列长度，对无限长、不间断运动的严格长时域一致性建模尚未解决。离散令牌的固定长度表示（N=16）在超长序列场景下可能成为瓶颈。

2. **运动表征范围**：DC-Motion目前聚焦于关节人体动作，未覆盖精细面部表情、复杂手势或多物种动物运动。这些场景的语义-细节解耦方式可能需要不同的表示设计。

3. **三阶段训练开销**：DC-VAE、MaskGIT、残差扩散的分阶段训练虽保证了模块解耦，但增加了训练流程的复杂性，端到端联合优化的可行性尚待探索。

### 补充图表

![[assets/figures/papers/paper_list_l2_https_arxiv_org_abs_2606_14721/figures/008_Table_4.jpg]]
*Table 4: Ablation on discrete token generation paradigms. MaskGIT effectively mitigates the exposure bias inherent in standard AR models, significantly improving global semantic alignment, particularly for long sequences and complex instructions*

![[assets/figures/papers/paper_list_l2_https_arxiv_org_abs_2606_14721/figures/001_Figure_1.jpg]]
*Figure 1: Our DC-Motion model generates high-quality and accurate motions from text prompts, effectively eliminating motion jitter while maintaining strong fidelity and stability. Darker colors indicate later time step*

## 方法谱系与知识库定位

### 1. 核心问题定位

人体运动生成领域长期存在一个根本性矛盾：**语义组合推理**与**物理细节保真**对表示空间的需求相互冲突。现有方法采用同质化表示——纯连续扩散模型（如 **MLD** (Chen et al., CVPR 2023)、**MDM** (Tevet et al., arXiv 2022)、**MotionDiffuse** (Zhang et al., TPAMI 2024)）在高维连续空间中建模，虽能保留关节平滑性等细粒度动态，但在复杂语义的组合推理上受限；纯离散自回归模型（如 **T2M-GPT** (Zhang et al., CVPR 2023)、**MoMask** (Guo et al., CVPR 2024)、**MotionGPT** (Jiang et al., NeurIPS 2023)）通过量化获得紧凑的语义令牌，但量化操作不可避免地丢弃高频物理信息，导致生成运动出现抖动或细节丢失。

DC-Motion 的切入点是**显式解耦语义与细节**——将运动生成分解为两个正交子问题：高层语义结构的全局规划，以及低频残差的物理精修。这一解耦思想并非孤立出现，而是对扩散模型与离散令牌模型各自优势的系统性整合。

### 2. 方法谱系中的位置

从表示空间维度看，DC-Motion 处于**连续扩散**与**纯离散 VQ** 之间的混合地带：

- **连续扩散谱系**：MDM 在原始运动空间做扩散，MLD 将扩散迁移到连续潜在空间，两者均依赖扩散模型的渐进式去噪来同时处理语义和细节，缺乏显式的语义结构化机制。DC-Motion 继承了连续扩散对残差建模的能力，但将其作用域缩小至仅处理高频残差，大幅降低了扩散模型的负担。

- **离散令牌谱系**：T2M-GPT 首次将 VQ-VAE 引入运动生成，MoMask 进一步用掩码建模替代标准自回归以缓解暴露偏差。DC-Motion 保留了离散码本的语义压缩能力，但通过引入连续残差分支补偿了 VQ 的信息损失——消融实验显示，纯离散 VQ-VAE 的重建 MPJPE 为 41.7，而 DC-VAE 通过残差补偿降至 25.8（Table 3），接近连续模型水平。

- **混合表示谱系**：DC-Motion 的核心贡献在于提出了一种**因子化的生成框架**——DC-VAE 将运动编码为离散语义令牌 $z_q$ 与连续残差 $r = z - z_q$，随后由 MaskGIT 负责 $z_q$ 的全局规划，残差扩散模型负责 $r$ 的局部精修。这种“先规划后精修”的两阶段范式在运动生成中尚属首次。

### 3. 关键技术选择的因果逻辑

**为什么用 MaskGIT 而非标准自回归？** 标准自回归模型在离散令牌生成中存在暴露偏差——训练时用真实令牌，推理时用预测令牌，误差沿时间步累积。MaskGIT 通过双向注意力和迭代掩码预测规避了这一问题。消融实验（Table 4）证实：MaskGIT 相较标准 AR，Overall R@1 从 0.611 提升至 0.642，FID 从 0.213 降至 0.182；在长序列上 R@1 从 0.574 提升至 0.623，验证了双向全局建模对长时域语义对齐的关键作用。

**为什么残差扩散的条件包含 $z_q$？** 残差扩散模型的条件为文本 $c$ 和离散结构表示 $z_q$（Eq. 12: $\mathcal{L}_{\mathrm{diff}} = \mathbb{E}_{t,\epsilon} [\| \epsilon - \epsilon_{\psi}(r_t, t, c, z_q) \|_2^2]$）。这一设计使得扩散模型无需从零开始生成运动结构，而是在固定的语义骨架 $z_q$ 上仅恢复高频残差，将扩散的搜索空间从“完整运动分布”缩减为“给定结构下的残差分布”，显著降低了建模难度。

### 4. 适用边界与局限

DC-Motion 的当前边界清晰：

- **序列长度受限**：方法受限于训练数据中的最大序列长度（HumanML3D 和 KIT-ML 的典型长度范围）。对于无限长、不间断的运动生成，如何在压缩的离散语义空间中进行严格的长时域一致性建模仍是开放挑战。

- **运动类型受限**：当前框架主要针对关节人体动作设计，扩展到精细面部表情、复杂手势或多物种动物运动需要验证离散-连续解耦假设是否仍然成立——不同运动类型的语义粒度与物理细节分布可能存在显著差异。

- **两阶段训练开销**：DC-Motion 采用三阶段训练（DC-VAE → MaskGIT → 残差扩散），每个阶段需冻结前序模块。这种序贯训练策略虽然保证了模块独立性，但增加了训练复杂度和调参成本。

### 5. 开放问题

- **连续时间/无限长运动生成**：当前离散令牌序列长度固定为 $N=16$（下采样后），如何将该解耦框架拓展到可变长度或连续时间运动生成，需要在时间维度上引入更灵活的表示机制。

- **解耦粒度的自适应选择**：语义与细节的边界在 DC-VAE 中由码本大小 $K$ 和潜在维度 $D$ 隐式决定。是否存在更原则性的方法来自适应确定解耦粒度，而非依赖超参数调优？

- **多模态扩展**：该解耦框架是否可推广到其他时序生成任务（如音乐、语音、视频），其中同样存在高层语义结构与低层物理细节的层次化特性？

## 原文 PDF

![[paperPDFs/arxiv_2026/DC-Motion_Decoupling_Semantics_and_Details_via_Discrete-Continuous_Tokens_for_Human_Motion_Generation.pdf]]