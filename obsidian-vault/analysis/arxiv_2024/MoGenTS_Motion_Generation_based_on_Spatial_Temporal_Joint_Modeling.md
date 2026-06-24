---
title: "MoGenTS: Motion Generation based on Spatial-Temporal Joint Modeling"
type: paper
paper_level: A
venue: arXiv
year: 2024
pdf_ref: paperPDFs/arxiv_2024/MoGenTS_Motion_Generation_based_on_Spatial_Temporal_Joint_Modeling.pdf
aliases:
- MoGenTS
tags:
- arxiv_2024
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
- topic/generative_models_diffusion
core_operator: 将量化粒度从整个姿态改为每个独立关节，降低每个码本的编码复杂度，同时保留关节的空间分布，形成二维时空 token 图。
primary_logic: 逐关节量化产生的二维 token 图与二维图像类似，可直接利用二维卷积、二维位置编码和二维注意力等成熟操作，有效捕获时空依赖关系。
claims:
- 在 HumanML3D 数据集上，FID 较先前最优方法 (MMM) 降低 26.6%。
- 在 KIT-ML 数据集上，FID 较先前最优方法降低 29.9%。
- 二维时空掩码 + 空间/时间注意力消融实验证明各组件均有显著增益。
- "关节量化相比全身量化在 MPJPE 上大幅降低（HumanML3D: 13.8 vs 29.5 mm）。"
---

# MoGenTS: Motion Generation based on Spatial-Temporal Joint Modeling

> [!tip] 核心洞察
> 逐关节量化产生的二维 token 图与二维图像类似，可直接利用二维卷积、二维位置编码和二维注意力等成熟操作，有效捕获时空依赖关系。

| 字段 | 内容 |
|------|------|
| 中文题名 | MoGenTS：基于时空联合建模的运动生成 |
| 英文题名 | MoGenTS: Motion Generation based on Spatial-Temporal Joint Modeling |
| 会议/期刊 | arXiv 2024 |
| Links | [paper](https://arxiv.org/abs/2409.17686) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction #topic/generative_models_diffusion |
| Method | MoGenTS |
| Dataset | HumanML3D, KIT-ML |

> [!tip] 效果简介
> - HumanML3D 上，FID↓ 0.033±.001 vs 0.045±.002 (MMM) (−0.012 (26.7% relative))；R-Precision Top-1↑ 0.529±.003 vs 0.521±.002 (MoMask) (+0.008 (1.5%))；R-Precision Top-2↑ 0.719±.002 vs 0.713±.002 (MoMask) (+0.006 (0.8%))。
> - KIT-ML 上，FID↓ 0.143±.009 vs 0.404±.027 (MLD) (−0.261 (64.6%))；R-Precision Top-1↑ 0.445±.004 vs 0.417±.004 (MotionDiffuse) (+0.028 (6.7%))；R-Precision Top-2↑ 0.671±.006 vs 0.628±.004 (M2DM) (+0.043 (6.8%))。

## 概述

文本到运动生成的核心瓶颈在于**运动量化**：现有方法将整帧姿态压缩为单个码本向量，编码难度高且丢失关节间的空间关系，导致量化近似误差较大。MoGenTS 提出**逐关节量化**，将运动序列组织为二维时空 token 图，从根本上降低每个码本的编码复杂度，同时保留关节的空间分布。

这一设计的关键洞察在于：逐关节量化产生的二维 token 图与二维图像在结构上高度相似，因此可直接复用二维卷积、二维位置编码和二维注意力等成熟操作，有效捕获时空依赖关系。基于此，MoGenTS 构建了一套完整的生成流水线：**Joint VQ-VAE** 将连续运动压缩为离散二维 token 图；**时空二维掩码**策略先沿时间维掩码整帧，再沿空间维掩码剩余关节；**时空二维 Transformer** 集成空间-时间二维注意力、独立空间注意力和独立时间注意力，从文本条件预测被掩码的 token。

在 HumanML3D 和 KIT-ML 两个标准基准上，MoGenTS 取得了显著的性能提升：
- **FID** 较先前最优方法分别降低 **26.6%**（HumanML3D: 0.033 vs. 0.045）和 **29.9%**（KIT-ML: 0.143 vs. 0.404）；
- **R-Precision Top-1** 分别达到 0.529 和 0.445，均优于已有方法；
- **MM-Dist** 分别降至 2.867 和 2.711，文本-运动对齐质量领先。

消融实验进一步验证了各组件的因果贡献：二维时空掩码相较一维掩码将 FID 从 0.088 降至 0.054；加入空间注意力后 FID 降至 0.038；再加入时间注意力达到最优 FID 0.033。逐关节量化相比全身量化在 MPJPE 上从 29.5 mm 大幅降至 13.8 mm，量化精度提升显著。推理速度约 181 ms/句，与主流方法可比。

MoGenTS 的方法定位属于**离散 token 生成**范式，与 T2M-GPT、MoMask、MMM 等基于 VQ-VAE + Transformer 的路线一脉相承，但通过将量化粒度从“全身”推进到“关节”级别，并配套设计二维掩码与二维注意力机制，在生成质量与文本对齐上建立了新的最优水平。

## 背景与动机

### 问题背景

文本到人体运动生成（Text-to-Motion Generation）旨在根据自然语言描述合成逼真的三维人体动作序列，在动画制作、虚拟现实和人机交互等领域具有广泛应用。近年来，扩散模型和矢量量化自回归模型在该任务上取得了显著进展，但现有方法普遍面临一个核心瓶颈：**量化粒度过粗导致编码难度高和空间关系丢失**。

具体而言，当前主流方法（如 **T2M-GPT**、**MoMask**、**MMM** 等）将每一帧的完整人体姿态量化为单个码本向量。这种“全身量化”策略将高维关节旋转数据压缩到单一离散 token 中，使得码本需要编码高度复杂的姿态分布，编码难度极大。更关键的是，该方式将同一帧内所有关节的信息混合为一个向量，完全丢弃了关节之间的空间结构关系，导致量化近似误差较大——这是制约生成质量提升的根本性瓶颈。

### 核心洞察

MoGenTS 的核心洞察在于**改变量化粒度**：将量化对象从“整帧姿态”下沉到“每个独立关节”。这一设计带来两个关键优势：

1. **降低编码复杂度**：每个关节的运动模式远比全身姿态简单，独立量化后单个码本只需覆盖单关节的旋转分布，编码难度显著降低。
2. **保留空间结构**：逐关节量化自然形成一张二维时空 token 图（时间维 × 空间维），完整保留了关节在空间维的分布关系，为后续建模提供了结构化的输入。

更重要的是，这一二维 token 图与二维图像具有天然的类比性。由此，可以直接迁移计算机视觉中成熟的二维操作——二维卷积、二维正弦位置编码、二维注意力机制——来有效捕获运动序列中的时空依赖关系。这种“借力打力”的设计避免了为运动数据专门设计复杂建模架构的需要。

### 现有方法缺口

从方法谱系来看，现有文本到运动生成方法可分为三类，均未能解决上述瓶颈：

- **连续回归方法**（如 **TEMOS**、**T2M**）：基于 VAE 架构直接回归连续运动参数，但生成质量受限于连续空间的优化难度。
- **扩散模型**（如 **MDM**、**MLD**、**MotionDiffuse**）：通过逐步去噪生成运动，虽在多样性上表现良好，但推理速度较慢，且未从离散表示角度解决量化误差问题。
- **VQ 量化 + 掩码/自回归方法**（如 **T2M-GPT**、**MoMask**、**MMM**）：采用全身量化策略，将运动压缩为离散 token 后通过掩码预测或自回归生成。这类方法虽在 FID 等指标上领先，但量化阶段的近似误差始终是生成质量的上界——全身量化在 HumanML3D 上的 MPJPE 高达 29.5 mm，而逐关节量化可降至 13.8 mm（Table 2），差距超过一倍。

此外，现有方法的掩码策略和注意力机制均基于一维序列设计，未利用运动数据的二维时空结构。一维随机掩码将所有 token 统一处理，无法区分时间维和空间维的掩码特性；标准一维自注意力则难以显式建模关节间的空间交互与帧间的时间演化的异质性。

### 本文动机与贡献

针对上述问题，MoGenTS 提出了一套完整的**时空联合建模**方案，核心贡献包括：

1. **逐关节矢量量化**：构建空间-时间二维 Joint VQ-VAE，将连续运动序列量化为二维离散 token 图，大幅降低量化误差。
2. **二维时空掩码策略**：设计先时间后空间的层次化掩码，迫使模型同时学习时间补全和空间协调能力。
3. **空间-时间二维 Transformer**：集成二维位置编码、空间-时间联合注意力、独立空间注意力和独立时间注意力，显式捕获异质性的时空依赖。
4. **残差 Transformer 与无分类器引导**：通过多层残差预测和 CFG（引导尺度 s=4）进一步提升重建精度和文本对齐度。

实验结果表明，MoGenTS 在 HumanML3D 上 FID 较先前最优方法（MMM）降低 26.6%，在 KIT-ML 上降低 29.9%，同时在 R-Precision、MM-Dist 等文本对齐指标上全面超越现有方法，验证了逐关节时空联合建模范式的有效性。

## 核心创新

MoGenTS 的核心创新在于将运动生成的量化粒度从**整帧姿态**下推至**独立关节**，由此将一维序列建模重构为**二维时空联合建模**。这一粒度迁移带来了三个连锁性的架构变化，构成方法的核心壁垒。

### 1. 量化粒度：从全身码本到逐关节二维 Token 图

现有基于 VQ 的运动生成方法（如 **T2M-GPT**、**MoMask**）将一帧内所有关节的旋转拼成一个高维向量，送入单个码本进行向量量化。这种做法存在两个根本性问题：

- **编码难度高**：单帧姿态的分布空间极大，单个码本需要覆盖全身所有关节的组合变化，导致量化近似误差较大。
- **空间关系丢失**：将关节展平为一维向量后，关节之间的空间拓扑结构（如左右对称、运动链依赖）被抹除，编码器难以利用这些归纳偏置。

MoGenTS 的解决方案是将量化粒度拆解为**每个关节单独量化**（Section 3.3）。具体而言，运动序列被组织为 $T \times J$ 的二维结构（$T$ 为帧数，$J$ 为关节数），每个关节在每个时刻的旋转表示 $\mathbf{j}_t^j$ 经过 2D 卷积编码器 $\mathcal{E}$ 映射为潜在向量 $\mathbf{v}_t^j$，再通过最近邻查找独立量化为码本条目：

$$\widetilde{\mathbf{v}}_t^j = \mathbf{c}_i, \quad i = \arg\min_i \|\mathbf{c}_i - \mathbf{v}_t^j\|_2$$

这一设计的直接收益在量化精度上得到了充分验证：在 HumanML3D 数据集上，逐关节量化将 MPJPE 从全身量化的 29.5 mm 大幅降至 13.8 mm，FID 从 0.019 降至 0.005（Table 2, Section 4.3）。在更大规模的 Motion-X 数据集上，MPJPE 从 111 mm 降至 48.7 mm，FID 从 0.081 降至 0.011（Table 6），表明该策略具有良好的可扩展性。

### 2. 掩码策略：从一维随机掩码到二维时空掩码

传统掩码语言建模（如 BERT）在运动 token 序列上采用一维随机掩码，所有位置的 token 被等概率地遮盖。MoGenTS 则利用二维 token 图的结构特性，设计了**先时间后空间**的层级掩码策略（Section 3.4）：

1. **时间维掩码**：以余弦调度比率 $\gamma(\tau) = \cos(\frac{\pi\tau}{2})$ 随机选取若干整帧，将该帧内所有关节的 token 全部掩码。这使得模型必须从相邻帧的上下文推断整帧的运动状态，强制学习时序依赖。
2. **空间维掩码**：在剩余的未掩码帧中，再以 $\bar{\gamma}(\tau)$ 的比率随机掩码部分关节的 token。这迫使模型利用同一帧内其他关节的信息进行空间补全。

消融实验（Table 3）表明，仅将一维掩码替换为二维时空掩码，FID 便从 0.088 降至 0.054，Top-1 检索精度从 0.492 提升至 0.516，证实了结构化掩码对生成质量的基础性贡献。

### 3. 注意力机制与位置编码：从一维序列到二维时空分解

量化粒度的变化使得运动 token 天然构成 $T \times J$ 的二维网格，与图像的特征图结构高度相似。MoGenTS 直接借鉴视觉 Transformer 的设计范式，引入以下组件（Section 3.5.1）：

- **二维正弦位置编码 $\mathbf{P}$**：独立编码空间维（关节索引）和时间维（帧索引）的位置信息，替代传统的一维可学习位置编码。
- **空间-时间二维注意力 $\mathcal{A}_{s\text{-}t}$**：将所有 token 展平为 $(T \times J)$ 的长序列，在全局范围内计算注意力，同时融入二维位置编码：

$$\mathcal{A}_{s\text{-}t} = \mathrm{SoftMax}(Q \cdot K / \sqrt{d} + \mathbf{P}) V$$

- **独立空间注意力 $\mathcal{A}_s$** 与**独立时间注意力 $\mathcal{A}_t$**：分别沿关节维和帧维计算注意力，以分解的方式捕获同帧关节间的空间协调关系与同关节跨帧的时序演变规律。

消融实验（Table 3）逐层验证了这些设计的增益：在二维掩码基础上添加空间注意力，FID 从 0.054 进一步降至 0.038，Top-1 升至 0.527；再加入时间注意力，达到最优 FID 0.033 和 Top-1 0.529。这表明空间与时间注意力的分解建模是互补的，二者联合使用方能充分捕获运动数据的时空依赖。

### 创新总结

MoGenTS 的核心创新并非单一技术的堆砌，而是**量化粒度的根本性改变**引发的一系列架构连锁反应。将运动从“一维姿态序列”重构为“二维关节-时间 token 图”后，二维卷积编码器、二维位置编码、二维掩码策略和分解式时空注意力等成熟操作得以自然引入，形成了一套高度协同的建模范式。这一设计思路在 HumanML3D 和 KIT-ML 两个基准上均取得了显著的 FID 提升（分别相对先前最优降低 26.6% 和 29.9%），且各组件在消融实验中均表现出独立且互补的增益，验证了创新设计的有效性。

## 整体框架

MoGenTS 提出一种“量化-掩码-生成”三阶段流水线，核心创新在于将运动表示从传统的**整帧姿态量化**转变为**逐关节二维时空 token 图**建模。图 1 展示了整体流程：

1. **运动量化阶段**：给定一段人体运动序列，首先将其组织为“关节-时间”二维结构。通过一个**空间-时间二维联合 VQ-VAE**（Joint VQ-VAE），将每个关节在每一帧的旋转信息独立编码为潜在向量，再经向量量化映射到共享码本中的离散索引，最终形成一张 $T \times J$ 的二维 token 图（$T$ 为帧数，$J$ 为关节数）。该量化器的编码器和解码器均采用二维卷积网络，直接操作二维特征图，保留关节间的空间拓扑关系。

2. **掩码策略**：对二维 token 图施加**先时间后空间**的二维掩码。首先沿时间维随机掩码整帧（该帧内所有关节 token 同时被掩码），再沿空间维对剩余未掩码帧中的部分关节 token 进行掩码。掩码比例由余弦调度 $\gamma(\tau) = \cos(\frac{\pi\tau}{2})$ 控制，并采用 BERT 风格的重掩码机制（80% 替换为 `[MASK]` token，10% 替换为随机 token，10% 保持不变）。

3. **运动生成阶段**：以文本描述为条件，使用**空间-时间二维 Transformer** 预测被掩码的 token。该 Transformer 集成了三种注意力机制：
   - **空间-时间二维注意力**：将二维 token 图展平后执行自注意力，并融入二维正弦位置编码，同时捕获时空依赖。
   - **空间注意力**：仅沿关节维度计算注意力，建模同一帧内不同关节的协调关系。
   - **时间注意力**：仅沿时间维度计算注意力，建模同一关节的运动时序。

4. **残差生成与推理**：采用多层残差 Transformer 逐步预测残差 token，提升重建精度。推理时使用无分类器引导（CFG，引导尺度 $s=4$）融合条件与无条件输出，增强文本对齐。

整个流水线将运动生成转化为类似图像修复的二维掩码预测问题，充分利用成熟的二维卷积和二维注意力操作，避免了传统一维序列建模对关节空间关系的破坏。

### 补充图表

![[assets/figures/papers/paper_list_l93_https_arxiv_org_abs_2409_17686/figures/001_Figure_1.jpg]]
*Figure 1: Framework overview. (a) In motion quantization, human motion is quantized into a spatial-temporal 2D token map by a joint VQ-VAE. (b) In motion generation, a temporal-spatial 2D masking is performed to obtain a masked map, and then a spatial-temporal 2D transformer is designed to infer the masked tokens*

## 核心模块与公式推导

### 3.1 运动量化：时空二维联合 VQ-VAE

MoGenTS 的核心创新在于将运动量化的粒度从“整帧姿态”下沉到“单个关节”。传统方法将一帧内所有关节的旋转拼接为一个高维向量，送入一维 VQ-VAE 进行量化。这种做法编码难度高，且丢失了关节间的空间结构关系，导致量化近似误差较大。MoGenTS 改为对每个关节独立量化，将运动序列组织为二维结构：空间维对应关节（共 $J$ 个），时间维对应帧（共 $T$ 帧），形成 $T \times J$ 的二维向量图。

**编码器映射**（公式 1）：
$$\{ \mathbf{v}_t^j \} = \mathcal{E}( \{ \mathbf{j}_t^j \} )$$
其中 $\mathbf{j}_t^j$ 表示第 $t$ 帧第 $j$ 个关节的旋转表示（6D 连续旋转），$\mathcal{E}$ 为二维卷积编码器，输出潜在向量 $\mathbf{v}_t^j$。编码器采用二维卷积网络，天然适配运动数据的时空二维结构。

**向量量化**（公式 2）：
$$\{ \widetilde{\mathbf{v}}_t^j \} = \mathcal{Q}( \{ \mathbf{v}_t^j \} ), \quad \mathcal{Q}: \widetilde{\mathbf{v}}_t^j = \mathbf{c}_i \text{ where } i = \arg\min_i \|\mathbf{c}_i - \mathbf{v}_t^j\|_2$$
量化器 $\mathcal{Q}$ 将每个关节的潜在向量 $\mathbf{v}_t^j$ 替换为共享码本 $\{ \mathbf{c}_i \}_{i=1}^{C}$ 中欧氏距离最近的条目。由于每个关节独立量化，码本只需编码单个关节的运动模式，而非整个姿态的复杂组合，显著降低了编码复杂度。

**解码器映射**（公式 3）：
$$\{ \tilde{\mathbf{j}}_t^j \} = \mathcal{D}( \{ \tilde{\mathbf{v}}_t^j \} )$$
解码器 $\mathcal{D}$ 从量化后的向量 $\tilde{\mathbf{v}}_t^j$ 重建关节旋转 $\tilde{\mathbf{j}}_t^j$，同样采用二维卷积结构。

**VQ-VAE 训练损失**（公式 4）：
$$\mathcal{L}_{vq} = \sum_{t,j} \|\tilde{\mathbf{j}}_t^j - \mathbf{j}_t^j\|_1 + \alpha \|\tilde{\mathbf{v}}_t^j - \mathbf{v}_t^j\|_2$$
第一项为 L1 关节重建损失，保证解码运动的精度；第二项为码本承诺损失，约束量化前后的潜在向量保持一致，权重 $\alpha = 1$。量化评估（Table 2）表明，逐关节量化在 HumanML3D 上将 MPJPE 从全身量化的 29.5 mm 大幅降至 13.8 mm，FID 从 0.019 降至 0.005，验证了粒度下移带来的近似误差显著降低。

### 3.2 掩码策略：时空二维掩码

量化得到的二维 token 图进入生成阶段时，需要设计掩码策略以训练掩码预测模型。MoGenTS 提出“先时间后空间”的二维掩码策略：

**掩码率调度**（公式 5）：
$$\gamma(\tau) = \cos(\frac{\pi\tau}{2})$$
其中 $\tau \sim U(0,1)$ 在训练中均匀采样，$\gamma(\tau)$ 决定当前训练步的掩码比例。采用余弦调度使训练过程中掩码率平滑变化。

掩码分两步执行：
1. **时间维掩码**：以 $\gamma(\tau) \times T$ 的比例随机选择整帧掩码，一旦某帧被选中，该帧内所有 $J$ 个关节的 token 全部被掩码。这迫使模型从相邻帧的上下文推断被掩码帧的运动。
2. **空间维掩码**：在剩余未掩码的帧中，以 $\bar{\gamma}(\tau) \times J$ 的比例随机掩码单个关节 token。这迫使模型利用同一帧内其他关节的信息进行推断。

掩码后的 token 采用 BERT 风格的**重掩码机制**：被选中的 token 以 80% 概率替换为 `[MASK]` token，10% 概率替换为随机 token，10% 概率保持不变。这种策略有效防止训练-推理分布偏移。

### 3.3 生成模型：时空二维 Transformer

掩码后的二维 token 图送入时空二维 Transformer 进行预测。与标准一维 Transformer 不同，MoGenTS 设计了三种互补的注意力机制，分别捕获不同类型的时空依赖：

**空间-时间二维注意力**（公式 6）：
$$\mathcal{A}_{s-t} = \mathrm{SoftMax}(Q \cdot K / \sqrt{d} + \mathbf{P}) V$$
将所有 $T \times J$ 个 token 展平为一维序列，计算全局自注意力。其中 $\mathbf{P}$ 为二维正弦位置编码，独立编码空间维（关节索引）和时间维（帧索引）的位置信息，使模型感知 token 在二维网格中的绝对位置。

**关节空间注意力**（公式 7）：
$$\mathcal{A}_s = \mathrm{SoftMax}(Q_s \cdot K_s / \sqrt{d} + \mathbf{P}) V_s$$
仅沿空间维（关节）计算注意力，每个时间步独立。这使模型专注于同一帧内不同关节间的协调关系，捕获姿态内部的空间结构。

**关节时间注意力**（公式 8）：
$$\mathcal{A}_t = \mathrm{SoftMax}(Q_t \cdot K_t / \sqrt{d} + \mathbf{P}) V_t$$
仅沿时间维（帧）计算注意力，每个关节独立。这使模型专注于同一关节随时间的运动轨迹，捕获时序动态。

三种注意力机制以残差方式组合，使模型同时建模全局时空交互、局部空间协调和局部时序演化。消融实验（Table 3）证实：仅使用二维时空掩码（无空间/时间注意力）时 FID 为 0.054；加入空间注意力降至 0.038；再加入时间注意力达到最优 0.033，各组件均有显著增益。

**掩码预测损失**（公式 9）：
$$\mathcal{L}_{\mathrm{mask}} = - \sum_{\mathrm{mask}} \sum_{i=1}^{C} y_i \log(\hat{y}_i) + (1 - y_i) \log(1 - \hat{y}_i)$$
仅在掩码位置计算多类交叉熵损失，$C$ 为码本大小，$y_i$ 为真实 token 的 one-hot 标签，$\hat{y}_i$ 为预测概率。

### 3.4 残差预测与条件生成

为进一步提升重建精度，MoGenTS 引入**多层残差 Transformer**：第一层预测主要 token，后续层预测残差 token，逐步细化生成结果。推理时迭代 $N = 10$ 步，每步预测置信度最高的 token 并填入掩码位置。

文本条件通过**无分类器引导**（Classifier-Free Guidance）注入（公式 10）：
$$\mathrm{logits} = (1 + s) \cdot \mathrm{logits}_{\mathrm{con}} - s \cdot \mathrm{logits}_{\mathrm{un}}$$
其中 $\mathrm{logits}_{\mathrm{con}}$ 为条件（文本）输出 logits，$\mathrm{logits}_{\mathrm{un}}$ 为无条件输出 logits，引导尺度 $s = 4$。训练时以 10% 概率丢弃文本条件进行无条件训练，推理时通过外推增强文本-运动对齐。

### 补充图表

![[assets/figures/papers/paper_list_l93_https_arxiv_org_abs_2409_17686/figures/002_Figure_2.jpg]]
*Figure 2: The structure of our spatial-temporal 2D Joint VQ-VAE for motion quantization*

![[assets/figures/papers/paper_list_l93_https_arxiv_org_abs_2409_17686/figures/003_Figure_3.jpg]]
*Figure 3: The temporal-spatial masking strategy (a) and the spatial-temporal attention (b) for motion generation*

## 实验与分析

### 核心瓶颈与因果机制验证

MoGenTS 的设计源于对现有运动量化方法一个根本性瓶颈的识别：**将整帧姿态压缩为单个码本向量**会导致编码难度过高，且丢失了关节间的空间结构关系，从而引入较大的量化近似误差。本文的核心因果调节变量在于**将量化粒度从“全身姿态”切换为“每个独立关节”**，这一改变直接降低了单个码本的编码复杂度，同时将运动序列重新组织为**二维时空 token 图**（时间维 × 空间维）。该二维结构与图像天然相似，使得二维卷积、二维位置编码和二维注意力等成熟操作可以被直接利用，有效捕获时空依赖关系。

这一因果链条在实验中得到了系统性的验证。以下从运动量化精度、运动生成质量、消融实验和效率分析四个层面展开。

### 运动量化精度评估

逐关节量化策略的有效性首先体现在量化重建精度上。**Table 2** 对比了全身量化（1D VQ-VAE）与逐关节量化（2D Joint VQ-VAE）的 MPJPE 和 FID。在 HumanML3D 数据集上，逐关节量化将 MPJPE 从 29.5 mm 大幅降至 13.8 mm，FID 从 0.019 降至 0.005。在 KIT-ML 数据集上同样观察到显著改善。这表明降低量化粒度的策略从根本上缓解了近似误差问题。

![[assets/figures/papers/paper_list_l93_https_arxiv_org_abs_2409_17686/figures/005_Table_2.jpg]]
*Table 2: Evaluation of motion quantization on HumanML3D dataset and KIT-ML dataset. MPJPE is measured in millimeters*

进一步地，**Table 6** 在更大规模的 Motion-X 数据集上验证了该策略的泛化能力：MPJPE 从 111 mm 降至 48.7 mm，FID 从 0.081 降至 0.011。量化精度的提升为下游生成任务提供了更高质量的离散 token 表示。

![[assets/figures/papers/paper_list_l93_https_arxiv_org_abs_2409_17686/figures/011_Table_6.jpg]]
*Table 6: Evaluation of motion quantization on Motion-X dataset. MPJPE is measured in millimeters*

### 文本驱动运动生成主结果

在 HumanML3D 和 KIT-ML 两个标准基准上的定量对比结果如 **Table 1** 所示。

![[assets/figures/papers/paper_list_l93_https_arxiv_org_abs_2409_17686/figures/004_Table_1.jpg]]
*Table 1: Evaluation on the HumanML3D dataset (upper half) and the KIT-ML dataset (lower half)*

**HumanML3D 数据集**（Table 1 上半部分）：
- **FID**：MoGenTS 取得 0.033±.001，较先前最优方法 MMM 的 0.045±.002 降低 26.7%，在所有对比方法中为最低。
- **R-Precision Top-1**：0.529±.003，优于 MoMask 的 0.521±.002（+1.5%）。
- **R-Precision Top-2 / Top-3**：分别为 0.719±.002 和 0.812±.002，均超过所有对比方法。
- **MM-Dist**：2.867±.006，优于 DiverseMotion 的 2.941±.007（降低 2.5%）。
- **Diversity**：9.570±.077，与真实数据的 9.503 高度接近，表明生成结果保持了自然的动作多样性。

**KIT-ML 数据集**（Table 1 下半部分）：
- **FID**：0.143±.009，较 MLD 的 0.404±.027 降低 64.6%，降幅显著。
- **R-Precision Top-1 / Top-2 / Top-3**：分别为 0.445±.004、0.671±.006、0.797±.006，均全面超越对比方法，Top-3 较 T2M-GPT 的 0.745±.006 提升 7.0%。
- **MM-Dist**：2.711±.012，较 MotionDiffuse 的 2.958±.005 降低 8.3%。
- **Diversity**：10.918±.104，接近真实数据的 11.080。

值得注意的是，所有方法均使用基于 T2M 的相同评估器进行特征提取，保证了指标的可比性。MoGenTS 在 FID 上的显著优势直接验证了二维时空 token 图表示和对应生成架构的有效性。

### 消融实验：设计组件贡献分析

**Table 3** 的消融实验系统性地拆解了各设计组件的贡献，以 1D 掩码 + 1D 自注意力的基线为起点：

1. **二维时空掩码（2D Mask）**：将一维随机掩码替换为先时间后空间的二维掩码策略，FID 从 0.088 降至 0.054，Top-1 从 0.492 提升至 0.516。这表明二维掩码策略迫使模型学习更合理的时空依赖关系。
2. **空间注意力（Spatial Attention）**：在二维掩码基础上加入独立的空间注意力，FID 进一步降至 0.038，Top-1 升至 0.527。空间注意力使模型能够显式建模同一帧内不同关节间的协调关系。
3. **时间注意力（Temporal Attention）**：最终加入独立的时间注意力，达到最优 FID 0.033 和 Top-1 0.529。时间注意力捕获了同一关节沿时间维的运动连续性。

消融实验清晰展示了三个核心组件——二维掩码、空间注意力、时间注意力——各自独立且累加的增益效果，验证了“将运动视为二维时空图进行处理”这一核心洞察的正确性。

### 推理效率分析

**Table 4** 报告了不同方法的推理时间对比。MoGenTS 的单句平均推理时间为 181 ms（在 NVIDIA 4090 GPU 上测试），与 T2M-GPT（173 ms）、MoMask（156 ms）等方法处于同一量级，显著快于 MDM（5780 ms）和 MLD（1270 ms）等扩散模型。这表明二维 Transformer 架构在保持高生成质量的同时，推理效率是可接受的。

### 失败模式与局限性

尽管 MoGenTS 在量化指标上取得了显著提升，论文明确指出了若干局限性：

1. **掩码策略的非最优性**：当前掩码策略沿用 BERT 风格的随机掩码（80% 掩码 token、10% 随机 token、10% 不变），未针对人体运动的图结构或运动学约束进行专门设计，可能限制了生成质量的上界。
2. **量化近似误差**：即使逐关节量化大幅降低了误差，量化过程仍然存在不可忽略的近似损失，这构成了生成质量的理论上界。
3. **物理合理性不足**：生成的运动偶尔不符合物理规律（如脚滑动现象），尚未在生成过程中融入物理约束或生物力学约束。
4. **数据规模限制**：缺乏大规模运动-文本数据集进行预训练，可能影响模型的泛化能力和量化器的精度上限。
5. **推理速度优化空间**：181 ms 的推理时间虽可接受，但并非实时最快，仍有进一步优化的可能。

### 开放问题

基于上述局限性，论文引申出若干值得探索的方向：能否设计运动专用的掩码策略（如图结构掩码或运动学感知掩码）？能否将物理约束直接融入生成过程以消除不自然动作？Coarse-to-fine 量化技术（如层次化码本）能否进一步降低近似误差？这些问题指向了运动生成领域后续研究的关键突破口。

### 补充图表

![[assets/figures/papers/paper_list_l93_https_arxiv_org_abs_2409_17686/figures/006_Figure_4.jpg]]
*Figure 4: Qualitative results on the test set of HumanML3D. The color from light blue to dark blue indicates the motion sequence order. An arrow indicates this sequence is unfolded in the time axis*

![[assets/figures/papers/paper_list_l93_https_arxiv_org_abs_2409_17686/figures/007_Table_3.jpg]]
*Table 3: Ablation study on HumanML3D dataset*

![[assets/figures/papers/paper_list_l93_https_arxiv_org_abs_2409_17686/figures/008_Figure_5.jpg]]
*Figure 5: Motion Editing. The edited regions are indicated in green*

![[assets/figures/papers/paper_list_l93_https_arxiv_org_abs_2409_17686/figures/009_Table_4.jpg]]
*Table 4: Computational overhead of different methods*

![[assets/figures/papers/paper_list_l93_https_arxiv_org_abs_2409_17686/figures/010_Table_5.jpg]]
*Table 5: Evaluation of motion quantization on (a) Humanml3D dataset and (b) KIT-ML dataset. MPJPE is measured in millimeters*

![[assets/figures/papers/paper_list_l93_https_arxiv_org_abs_2409_17686/figures/012_Figure.jpg]]

## 方法谱系与知识库定位

### 1. 问题瓶颈与核心洞察

文本驱动人体运动生成的主流方法可归为连续回归、扩散模型和离散量化三类。连续方法（如 **TEMOS**、**T2M**、**MDM**、**MLD**、**MotionDiffuse**）直接在连续空间建模，生成质量受限；离散方法通过向量量化（VQ）将运动压缩为 token 序列，再利用生成式模型预测，近期表现突出（**T2M-GPT**、**MoMask**、**MMM**）。

现有离散方法的根本瓶颈在于**量化粒度**：它们将整帧姿态（所有关节的旋转）压缩为单个码本向量。这种全身量化策略导致两个问题——(1) 单向量需编码高维姿态信息，码本学习难度大，量化近似误差高；(2) 关节间的空间结构在扁平化为一维序列时被破坏，后续的一维 Transformer 难以有效捕获空间依赖。

MoGenTS 的核心洞察是**将量化粒度从“整帧姿态”下沉到“每个独立关节”**，形成 $T \times J$ 的二维时空 token 图（$T$ 为帧数，$J$ 为关节数）。这一设计使运动表示与二维图像结构同构，从而可直接复用二维卷积、二维位置编码和二维注意力等成熟操作，有效捕获时空依赖。

### 2. 方法谱系定位

下表从四个关键设计维度将 MoGenTS 与代表性基线进行对比：

| 维度 | 全身量化方法 (T2M-GPT / MoMask / MMM) | MoGenTS (本文) |
|------|--------------------------------------|----------------|
| **量化粒度** | 整帧姿态 → 单个码本向量 | 每个关节 → 独立码本向量，形成 2D token 图 |
| **掩码策略** | 一维随机掩码（BERT-style） | 二维时空掩码：先时间维掩码整帧，再空间维掩码剩余关节 |
| **注意力机制** | 标准一维自注意力 | 空间-时间二维注意力 + 单独空间注意力 + 单独时间注意力 |
| **位置编码** | 一维位置编码或可学习编码 | 二维正弦位置编码（独立空间维和时间维） |

**与 MoMask / MMM 的关系**：MoGenTS 继承了掩码建模（masked modeling）的生成范式，但将一维掩码预测升级为二维时空掩码预测。MMM 采用一维随机掩码 + 一维 Transformer，MoGenTS 的消融实验（Table 3）表明，仅将掩码策略替换为二维时空掩码，FID 即从 0.088 降至 0.054；进一步引入空间注意力和时间注意力后，FID 降至 0.033。这说明二维归纳偏置是增益的主要来源，而非单纯的模型容量提升。

**与 ParCo 的关系**：ParCo 探索了分部件（part-based）运动合成，关注不同身体部件的协调性。MoGenTS 的逐关节量化在粒度上更细（关节级而非部件级），且通过二维 token 图统一建模所有关节的时空关系，不依赖预定义的部件分组。

**与 MotionGPT 的关系**：MotionGPT 将运动 token 化后送入大语言模型（LLM）进行自回归生成，属于“LLM 驱动”路线。MoGenTS 则专注于改进量化表示本身——通过逐关节量化和二维结构设计降低量化误差，其掩码 Transformer 相对轻量（6 层、6 头、384 维），与 LLM 路线正交，未来可结合。

### 3. 适用边界与局限

**适用场景**：
- 文本驱动的全身运动生成（HumanML3D、KIT-ML 等标准 benchmark 已验证）
- 运动编辑：二维 token 图允许对特定帧/关节区域进行局部掩码再生成（Figure 5 展示编辑能力）
- 可扩展至大规模运动数据：在 Motion-X 数据集上，逐关节量化将 MPJPE 从 111 mm 降至 48.7 mm（Table 6），表明该方法对数据规模有良好适应性

**已知局限**（论文明确提及或可从实验推断）：

1. **掩码策略非最优**：当前沿用 BERT 风格的随机掩码（80% [MASK]、10% 随机 token、10% 保留），未针对运动数据的图结构或运动学约束进行专门设计。关节间存在骨骼连接等强先验，图结构掩码或运动学感知掩码可能进一步提升生成质量。

2. **量化误差上界**：尽管逐关节量化相比全身量化大幅降低了近似误差（HumanML3D 上 MPJPE 从 29.5 mm 降至 13.8 mm），但 VQ-VAE 的离散化仍存在信息损失，这是生成质量的上界约束。Coarse-to-fine 量化（如层次化码本）可能是缓解方向。

3. **物理合理性不足**：生成的运动偶尔违反物理规律（如脚滑动），模型未融入物理约束或生物力学约束。这是当前数据驱动方法的共性问题，MoGenTS 并未提出针对性解决方案。

4. **数据规模依赖**：论文指出缺乏大规模运动-文本数据集限制了量化器的预训练质量。在更大规模数据上预训练可能进一步释放方法潜力。

5. **推理速度**：单句平均推理时间 181 ms（NVIDIA 4090，Table 4），虽与其他主流方法可比，但并非实时最快，仍有优化空间。

### 4. 开放问题

基于上述局限，以下问题值得进一步探索：

- **运动专用掩码策略**：能否设计图结构掩码（利用骨骼拓扑）或运动学感知掩码（考虑关节间物理约束），替代随机掩码以提升生成质量？
- **层次化量化**：Coarse-to-fine 量化技术（如残差码本、层次化 VQ）能否进一步降低逐关节量化的近似误差，逼近连续表示的重建精度？
- **混合生成范式**：掩码生成（并行解码）与自回归生成（逐 token 预测）能否结合，兼顾推理效率与长序列一致性？
- **物理约束融入**：如何将物理约束（如足部接触、动量守恒）或生物力学约束直接融入生成过程，消除不自然的伪影？
- **大规模预训练**：如何获取或构建大规模运动-文本配对数据，以预训练高精度的运动量化器，提升泛化能力？

## 原文 PDF

![[paperPDFs/arxiv_2024/MoGenTS_Motion_Generation_based_on_Spatial_Temporal_Joint_Modeling.pdf]]