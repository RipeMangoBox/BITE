---
title: "Open the Motion Door: Atomic Motion Decomposition and Recomposition for Open-Vocabulary Motion Generation"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/Open_the_Motion_Door_Atomic_Motion_Decomposition_and_Recomposition.pdf
code_link: null
project_link: https://vankouf.github.io/OpenTheMotionDoor
aliases:
- AMDR
- OMDAMDROVMG
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/generative_models_diffusion
- topic/motion_animation/human_motion_generation
- topic/motion_animation
core_operator: 通过将复杂运动表达为时空上可组合的简单位移元素——原子运动，并在文本层面进行分解与运动特征层面进行重组，模型得以在训练分布之外进行泛化。
primary_logic: 复杂人类动作可由简单、可重用的身体部位运动（原子运动）在时间和空间上组合而成。将开放域文本首先分解为受限于数据集维度的原子运动描述，再学习将这些原子元素合成为目标动作，可以显著提升模型的开放词汇运动生成能力。
claims:
- 在域外数据集IDEA400和Mixamo上，我们的方法显著优于现有最佳方法（如MDM），FID分别达到0.449和0.186，证明了强大的泛化能力。
- 文本分解算法显著缩小了训练与测试数据集之间的域间隙，t-SNE可视化显示分解后不同数据集的分布几乎重合。
- 组合特征融合（CFF）和文本-运动对齐（TMA）模块有效地增强了泛化性能，消融实验证实其必要性。
- HumanML3D 上 FID = 0.132
---

# Open the Motion Door: Atomic Motion Decomposition and Recomposition for Open-Vocabulary Motion Generation

> [!tip] 核心洞察
> 复杂人类动作可由简单、可重用的身体部位运动（原子运动）在时间和空间上组合而成。将开放域文本首先分解为受限于数据集维度的原子运动描述，再学习将这些原子元素合成为目标动作，可以显著提升模型的开放词汇运动生成能力。

| 字段 | 内容 |
|------|------|
| 中文题名 | 打开运动之门：面向开放词汇运动生成的原子运动分解与重组 |
| 英文题名 | Open the Motion Door: Atomic Motion Decomposition and Recomposition for Open-Vocabulary Motion Generation |
| 会议/期刊 | CVPR 2026 |
| Links | [Project](https://vankouf.github.io/OpenTheMotionDoor) |
| Topic | #topic/vision_multimodal_applications #topic/generative_models_diffusion #topic/motion_animation/human_motion_generation #topic/motion_animation |
| Method | Atomic Motion Decomposition and Recomposition |
| Dataset | HumanML3D, IDEA400, Mixamo |

> [!tip] 效果简介
> - HumanML3D 上，FID 0.132 vs 0.116 (T2M-GPT) (+0.016)。
> - IDEA400 上，FID 0.449 vs 0.821 (MDM) (-0.372)。
> - Mixamo 上，FID 0.186 vs 0.211 (MDM) (-0.025)。

## 概要

现有文本到运动生成方法受限于小规模配对数据集，难以泛化到训练中未见过的开放域文本描述。即使扩大数据规模和模型容量，长尾且多样的动作空间仍然无法被充分覆盖。本文提出**原子运动分解与重组**（Atomic Motion Decomposition and Recomposition）框架，将开放词汇运动生成问题转化为两个子阶段：首先将任意文本描述分解为时空上可组合的原子运动单元，再学习将这些原子元素合成为目标全身运动。

核心洞察在于，复杂人类动作可由简单、可重用的身体部位运动在时间和空间上组合而成。基于此，方法引入**文本分解**（Textual Decomposition）模块，将原始运动文本转换为描述特定身体部位在短时间段内运动的原子文本矩阵；同时设计**文本-运动对齐**（TMA）模块和**组合特征融合**（CFF）模块，在特征层面实现原子运动到目标运动的重组。

在域内数据集 HumanML3D 上，该方法取得与现有最佳方法可比的性能（FID 0.132 vs. T2M-GPT 0.116）。在域外数据集上，泛化优势显著：IDEA400 上 FID 达到 0.449（MDM 为 0.821），Mixamo 上 FID 为 0.186（MDM 为 0.211）。t-SNE 可视化证实，文本分解算法有效缩小了训练与测试数据集之间的文本域间隙，分解后的细粒度描述在不同数据集上分布几乎重合。消融实验进一步表明，CFF 模块将 IDEA400 的 FID 从 0.934 降至 0.844，TMA 模块则将 R-Precision 提升至 0.449，二者对开放词汇泛化均不可或缺。



### 文本驱动运动生成的核心瓶颈

文本到运动生成旨在根据自然语言描述合成逼真的三维人体动作序列，在动画制作、虚拟现实和人机交互等领域具有广泛应用。然而，现有方法面临一个根本性瓶颈：**模型严重受限于小规模配对数据集的分布，无法有效泛化到训练中未见的开放域文本**。

当前主流方法——包括基于扩散模型的 **MDM**、自回归生成的 **T2M-GPT**（Zhang et al., CVPR 2023）、多视角注意力的 **ATTT2M**（Zhong et al., ICCV 2023）以及掩码生成模型 **MMM**（Pinyoanuntapong et al., CVPR 2024）——本质上都采用“简单映射”范式：直接从原始文本映射到全身运动序列。这种端到端的学习方式在域内数据集（如HumanML3D）上表现良好，但一旦面对训练分布之外的开放词汇描述，模型性能便急剧下降。即使扩大数据规模和模型容量，也难以覆盖长尾且多样的人类动作空间。

### 现有范式的三种尝试及其局限

为缓解域泛化问题，研究者探索了三条路径（见Figure 1）：

1. **简单映射**：直接在文本-运动对上训练生成模型。该方法最直接，但泛化能力最弱，模型倾向于记忆训练数据中的文本-运动关联模式。
2. **跨域对齐**：借助其他模态（如图像、视频）的预训练模型进行特征对齐，间接扩展语义覆盖范围。然而，这些辅助模态与人体运动之间仍存在语义鸿沟，对齐质量难以保证。
3. **预训练-微调**：先在大规模无标注运动数据上预训练，再在小规模标注数据上微调。虽然利用了更多运动数据，但文本端的泛化问题并未得到根本解决——微调阶段仍然受限于有限的文本描述多样性。

上述三种范式的共同缺陷在于：**它们都试图直接建立从开放域文本到复杂全身运动的映射，而忽视了人体运动本身的可组合性**。

### 核心洞察：原子运动的可组合性

本文的核心洞察是：**复杂人类动作可以由简单、可重用的身体部位运动——即“原子运动”——在时间和空间上组合而成**。例如，“一个人边走路边挥手”这一动作，可以分解为下肢的“行走”、上肢的“挥手”、躯干的“保持平衡”等原子运动单元。这些原子运动在语义层面和运动特征层面都具有相对独立的可描述性和可组合性。

基于这一洞察，本文提出了一种全新的范式：**原子运动分解与重组**。其核心思路是：首先将开放域文本分解为受限于数据集维度的原子运动描述（文本分解），再学习将这些原子元素合成为目标动作（运动重组）。这一范式从根本上改变了模型处理开放词汇的方式——模型不再需要直接理解任意复杂的文本，而是将其转化为已知原子运动的组合问题，从而在训练分布之外获得显著的泛化能力。

### 方法概览

为实现上述范式，本文提出了**Atomic Motion Decomposition and Recomposition**框架，包含两个关键组件：

- **文本分解模块**：将原始运动文本解析为时空上的原子运动描述矩阵（L×P，L=6个身体部位，P个时间段），包括脊柱、左右上肢、左右下肢和根轨迹的运动细节。
- **原子重组模块**：通过文本-运动对齐（TMA）和组合特征融合（CFF）机制，学习将原子运动描述合成为目标全身运动。

实验结果表明，该方法在域外数据集IDEA400和Mixamo上显著优于现有最佳方法，FID分别达到0.449和0.186，验证了原子运动分解与重组范式在开放词汇运动生成中的有效性。



## 核心方法与创新机理

本文的核心创新在于引入**原子运动**作为文本与运动之间的中间表示，将开放词汇运动生成重新表述为“文本分解—原子重组”的两阶段过程。这一范式转变直接针对现有方法的核心瓶颈：小规模配对数据集导致模型无法泛化到训练中未见的长尾动作描述。

### 创新一：文本层面的原子运动分解

传统方法（如 **MDM**、**T2M-GPT** (Zhang et al., CVPR 2023)、**MMM** (Pinyoanuntapong et al., CVPR 2024)）将原始运动文本作为单一输入，直接映射到运动序列。当测试文本的语义分布偏离训练集时，模型缺乏拆解和泛化的能力。

本文的**输入表示**发生了根本性变化：原始文本被显式分解为**原子运动文本矩阵**（$L \times P$，其中 $L=6$ 个身体部位，$P$ 个时间段）。这一分解在训练阶段通过基于规则的算法完成——利用关节角度（如肘部弯曲余弦值 $\frac{J_{shoulder} - J_{elbow}}{||J_{shoulder} - J_{elbow}||} \odot \frac{J_{wrist} - J_{elbow}}{||J_{wrist} - J_{elbow}||}$）和姿态变化累积量（$S_{PD_{i}} = \sum_{t=i}^{i+T_{i}} \Delta PD_{t}$）将运动自动转化为细粒度描述；在推理阶段则由大语言模型（LLM）完成（见 Figure 3）。

这一设计的关键因果机制在于：**将开放域文本的语义空间约束到与训练数据一致的原子描述空间内**。t-SNE 可视化（Figure 6）提供了直接证据——原始文本在不同数据集间分布差异显著，而分解后的细粒度描述在 HumanML3D、IDEA400 和 Mixamo 上的分布几乎完全重合，从文本层面消除了域间隙。

### 创新二：运动层面的原子特征重组

基线方法通常采用直接拼接或自注意力方式融合文本与运动特征，缺乏对原子运动的结构化建模。本文引入了两个紧密耦合的模块来改变**特征融合**和**文本-运动对齐**方式：

- **文本-运动对齐模块（TMA）**：通过对比学习预训练，使用 InfoNCE 损失 $\mathcal{L}_{\mathrm{NCE}} = -\frac{1}{2M} \sum_i \left( \log \frac{\exp A_{ii}/\tau}{\sum_j \exp A_{ij}/\tau} + \log \frac{\exp A_{ii}/\tau}{\sum_j \exp A_{ji}/\tau} \right)$ 将原子文本嵌入对齐到运动特征空间。这替代了基线中标准的 CLIP 对齐或端到端学习，为后续重组提供更具判别力的原子特征。

- **组合特征融合模块（CFF）**：将运动特征按通道维拆分为身体部位专家，以原子文本嵌入为键（Key）和值（Value），运动嵌入为查询（Query），执行交叉注意力 $\tilde{m}^3 = \mathcal{F}_{\mathrm{CFF}}(\tilde{m}^2; T_a)$。CFF 模块与 Transformer 层交替堆叠 $K$ 次，使每个身体部位的运动生成能够独立关注其对应的原子文本描述，同时通过 Transformer 保持全身运动的时序一致性。

消融实验（Table 2）验证了这一设计的必要性：在基线模型上仅添加 CFF 模块，IDEA400 的 FID 从 0.934 降至 0.844；进一步加入 TMA 对齐后，R-Precision 提升至 0.449。值得注意的是，若将原子文本直接拼接（CFF*）而非使用特征级融合，FID 反而升至 0.886，凸显了结构化重组的关键作用。

### 创新三：离散生成框架下的原子重组

本文采用离散掩码生成框架（Residual VQ-VAE + Masked Generator），这与 **T2M-GPT** 的自回归生成和 **MDM** 的扩散生成形成对比。离散表示天然适合组合性建模——每个运动 token 对应特定的运动模式，原子文本通过 CFF 模块引导特定身体部位 token 的预测。这一设计使模型在推理时能够通过迭代预测-重掩码策略，逐步从原子描述合成连贯的全身运动。

### 创新效果的直接证据

在域外数据集上的表现直接证明了创新的有效性（Table 1）：
- IDEA400 上 FID 达到 **0.449**，相比 MDM 的 0.821 降低了 45.3%；
- Mixamo 上 FID 达到 **0.186**，优于所有基线方法；
- 在域内 HumanML3D 上 FID 为 0.132，与 T2M-GPT 的 0.116 保持竞争力，表明该方法在提升泛化能力的同时并未牺牲域内性能。

这些结果共同表明，原子运动的分解-重组范式成功地将模型能力从“记忆训练分布”转变为“组合已知原子以应对未知描述”，是开放词汇运动生成的根本性突破。



本文提出 **Atomic Motion Decomposition and Recomposition** 框架，将开放词汇文本到运动生成形式化为一个两阶段过程：**文本分解（Textual Decomposition）** 和 **原子重组（Atomic Recomposition）**。其核心思想是将复杂的全身运动表达为时空上可组合的原子运动单元，从而突破训练数据分布的限制，实现对开放域文本的泛化。

### 总体架构

框架采用**离散生成掩码建模**范式，整体流程如 Figure 2 所示。首先，在大规模未标注运动数据上预训练一个 **Residual VQ-VAE（RVQ）**，将连续运动序列量化为多层离散码本索引，获得压缩且离散的运动表示。生成阶段则训练一个掩码生成模型，以原始文本和原子运动文本为条件，迭代预测被掩码的运动 token。

![[assets/figures/papers/paper_list_l5_Open_the_Motion_Door_Atomic_Motion_Decomposition_and_Recomposition_for_O/figures/002_Figure_2.jpg]]
*Figure 2: The architecture of our entire framework. The overall pipeline adopts discrete generative modeling. As shown in the left green part, we first use a Residual VQ-VAE (RVQ) model, which consists of a base layer and R residual layers, to learn layer-wise codebooks. Then we learn a generative model for text-to-motion generation. We first perform Texutal Decomposition, which converts the raw text of a motion into several atomic motion texts. Furthermore, we perform Atomic Recomposition, designing a text-motion alignment (TMA) module and a compositional feature fusion (CFF) module to learn the composition process from atomic motions to the target motions*

生成模型的核心计算流为：原始文本特征 $T_r$ 与掩码运动序列 $\tilde{m}$ 首先经过一个 **Transformer 层**，融合时序和语义上下文：

$$T_{r}^{o}, \tilde{m}^{1} = \mathcal{F}_{\mathrm{Transformer}}(T_{r}; \tilde{m})$$

随后，Transformer 输出的运动特征 $\tilde{m}^1$ 进入 **组合特征融合（CFF）模块**，与原子文本特征进行交叉注意力融合，得到 $\tilde{m}^3$。融合结果经线性投影后得到更新的全身运动特征 $\tilde{m}^{o} \in \mathbb{R}^{N \times D_{m}}$，并与精炼后的原始文本特征 $T_r^o$ 一起送入下一个 Transformer-CFF 块。经过多层堆叠后，最终的分类头预测离散运动索引，以交叉熵损失进行监督。

### 推理过程

推理时采用**迭代掩码预测**策略：模型在每一轮预测所有被掩码 token，低置信度的预测在下一轮被重新掩码，高置信度的 token 则被固定。该过程反复迭代直至所有 token 被解码，最终通过 RVQ 解码器重建出连续运动序列。

### 文本分解模块

文本分解模块（Figure 3）负责将任意运动描述转换为**原子运动文本矩阵**（维度 $L \times P$，$L=6$ 个身体部位，$P$ 个时间段）。训练阶段利用基于规则的算法，从运动数据中提取细粒度描述：首先通过关节坐标计算肘部弯曲角度的余弦值

$$\frac{J_{shoulder} - J_{elbow}}{||J_{shoulder} - J_{elbow}||} \odot \frac{J_{wrist} - J_{elbow}}{||J_{wrist} - J_{elbow}||}$$

并聚合姿态描述子在运动剪辑内的累积变化 $S_{PD_{i}} = \sum_{t=i}^{i+T_{i}} \Delta PD_{t}$ 和平均变化速率 $V_{PD_{i}} = \frac{|S_{PD_{i}}|}{T_{i}}$，进而为各身体部位生成时序上的原子运动描述。推理阶段则使用大语言模型（LLM）从开放文本中总结出原子运动描述。

### 原子重组模块

原子重组由两个关键组件构成：**文本-运动对齐（TMA）模块**和**组合特征融合（CFF）模块**（Figure 4）。

TMA 模块在文本-运动对上通过对比学习预训练，使用 InfoNCE 损失对齐文本与运动嵌入空间：

$$\mathcal{L}_{\mathrm{NCE}} = -\frac{1}{2M} \sum_{i} \left( \log \frac{\exp A_{ii}/\tau}{\sum_{j} \exp A_{ij}/\tau} + \log \frac{\exp A_{ii}/\tau}{\sum_{j} \exp A_{ji}/\tau} \right)$$

其中 $A_{ij}$ 为相似度矩阵，$\tau$ 为温度系数。预训练后的 TMA 编码器为后续生成提供更对齐的原子文本特征。

CFF 模块则负责将原子文本信息注入运动生成过程：以运动嵌入为 Query，原子文本嵌入为 Key 和 Value，通过交叉注意力实现组合式特征融合：

$$\tilde{m}^{3} = \mathcal{F}_{\mathrm{CFF}}(\tilde{m}^{2}; T_{a})$$

具体而言，运动特征在通道维被拆分为对应不同身体部位的专家组，各组独立与相应的原子文本嵌入进行交叉注意力，从而实现部位级别的条件化生成。CFF 模块与 Transformer 层交错堆叠 $K$ 次，使模型逐步从原子运动组合出目标全身运动。

> **公平性说明**：所有对比方法均在 HumanML3D 上训练并使用相同测试分割；本方法额外使用未标注运动数据训练 RVQ，这可能带来一定的先验优势，但后续消融实验（Table 2）已对 CFF 和 TMA 的独立贡献进行了控制。

### 补充图表

![[assets/figures/papers/paper_list_l5_Open_the_Motion_Door_Atomic_Motion_Decomposition_and_Recomposition_for_O/figures/001_Figure_1.jpg]]
*Figure 1: In contrast to current text-to-motion paradigms (Simple Mapping, Other-domain Alignment, and Pretrain-then-Finetuning), our method proposes the textual decomposition to decompose the raw motion text into atomic motion texts, and then recomposes atomic motions into the target motion, which significantly improves the ability of open-vocabulary motion generation*



### 整体架构与掩码生成建模

方法整体采用**离散生成掩码建模**框架。运动先通过残差 VQ-VAE（RVQ）量化为离散符号序列，生成模型则以迭代掩码预测的方式逐步恢复完整的运动符号。在每一轮推理迭代中，模型基于文本输入预测所有被掩码的符号，低置信度的预测在下一轮被重新掩码，高置信度符号则被固定。

生成模型的核心是一个**Transformer-CFF 交错堆叠**结构。每个块首先由 Transformer 层融合原始文本特征与掩码运动序列：

$$T_{r}^{o}, \tilde{m}^{1} = \mathcal{F}_{\mathrm{Transformer}}(T_{r}; \tilde{m})$$

其中 $T_{r}$ 为原始文本特征，$\tilde{m}$ 为当前掩码运动序列。Transformer 层整合时序和语义上下文后，输出精炼的文本特征 $T_{r}^{o}$ 和初步更新的运动特征 $\tilde{m}^{1}$，随后进入组合特征融合阶段。

### 文本分解：从开放文本到原子运动描述

文本分解的目标是将任意运动描述转换为一组**原子运动文本**，每条原子文本描述特定身体部位在短时间窗口内的运动。训练阶段使用基于规则的**细粒度描述转换算法**，推理阶段则借助大语言模型完成。

算法核心步骤包括：

**步骤一：关节角度计算。** 以肘部弯曲角度为例，通过肩、肘、腕关节坐标计算余弦值：

$$\frac{J_{shoulder} - J_{elbow}}{||J_{shoulder} - J_{elbow}||} \odot \frac{J_{wrist} - J_{elbow}}{||J_{wrist} - J_{elbow}||}$$

**步骤二：姿态聚合与运动分类。** 在运动剪辑时长 $T_i$ 内，累积姿态描述子的帧间差值：

$$S_{PD_{i}} = \sum_{t=i}^{i+T_{i}} \Delta PD_{t}$$

并计算剪辑内的平均变化速率：

$$V_{PD_{i}} = \frac{|S_{PD_{i}}|}{T_{i}}$$

该速率用于对每个身体部位的运动行为进行分类（如“快速弯曲”、“缓慢伸展”等），最终生成维度为 $L \times P$ 的原子运动文本矩阵（$L=6$ 个身体部位，$P$ 个时间段）。

### 原子重组：文本-运动对齐与组合特征融合

原子重组阶段包含两个关键模块：**文本-运动对齐（TMA）**和**组合特征融合（CFF）**。

**TMA 模块**通过对比学习在文本-运动对上预训练，使用 InfoNCE 损失将文本特征对齐到运动空间：

$$\mathcal{L}_{\mathrm{NCE}} = -\frac{1}{2M} \sum_{i} \left( \log \frac{\exp A_{ii}/\tau}{\sum_{j} \exp A_{ij}/\tau} + \log \frac{\exp A_{ii}/\tau}{\sum_{j} \exp A_{ji}/\tau} \right)$$

其中 $A_{ij}$ 为运动与文本嵌入的相似度矩阵，$\tau$ 为温度系数。预训练后的 TMA 编码器为后续融合提供更对齐的原子文本特征。

**CFF 模块**以运动嵌入为查询（Query），原子文本嵌入为键（Key）和值（Value），执行交叉注意力融合：

$$\tilde{m}^{3} = \mathcal{F}_{\mathrm{CFF}}(\tilde{m}^{2}; T_{a})$$

具体而言，运动特征 $\tilde{m}^{2}$ 在通道维度上按身体部位拆分，各部位专家分别与对应的原子文本嵌入 $T_{a}$ 进行交叉注意力。融合后的特征经重塑和线性投影，得到更新的全身运动特征：

$$\tilde{m}^{o} \in \mathbb{R}^{N \times D_{m}}$$

该输出随后与精炼的原始文本特征 $T_{r}^{o}$ 结合，送入下一个 Transformer-CFF 块。堆叠 $K$ 次后，由分类头预测离散运动索引，以交叉熵损失进行监督。

### 补充图表

![[assets/figures/papers/paper_list_l5_Open_the_Motion_Door_Atomic_Motion_Decomposition_and_Recomposition_for_O/figures/003_Figure_3.jpg]]
*Figure 3: Illustration of textual decomposition. During training, raw motion text is converted into atomic motion descriptions (including spine, left/right upper limbs, left/right lower limbs, and root trajectory) over several time periods by Textual Decomposition Algorithm. During Inference, raw motion text is converted by Large Language Model*

![[assets/figures/papers/paper_list_l5_Open_the_Motion_Door_Atomic_Motion_Decomposition_and_Recomposition_for_O/figures/004_Figure_4.jpg]]
*Figure 4: Illustration of the Compositional Feature Fusion (CFF) module. The atomic text matrix is processed by the TMA module and then fused with the motion features via cross-attention*



## 实验与关键发现

### 域内与域外生成性能

我们在域内基准 HumanML3D 和两个域外基准 IDEA400、Mixamo 上对本文方法与现有前沿方法进行了系统对比。所有方法均在 HumanML3D 训练集上训练，使用相同的测试划分，评估指标包括 FID、R-Precision 和 Diversity 等。

**域内结果（HumanML3D）**：本文方法取得了与现有最佳方法相当的竞争力。如表 1 所示，我们的 FID 为 0.132，略高于 T2M-GPT（0.116）和 MMM（0.080），但 R-Precision 达到 0.498，处于较高水平。这表明在训练分布内，原子运动分解-重组框架并未牺牲生成质量，保持了与强基线一致的表现。

**域外泛化结果（IDEA400 和 Mixamo）**：泛化能力是本文方法的核心优势所在。在 IDEA400 上，我们的 FID 达到 **0.449**，相比 MDM 的 0.821 降低了 **45.3%**，相比 T2M-GPT 的 0.934 降低了 **51.9%**。在 Mixamo 上，我们的 FID 为 **0.186**，优于 MDM 的 0.211 和 ATTT2M 的 0.216。这一显著提升直接验证了核心洞见：通过将开放域文本分解为受限于数据集维度的原子运动描述，再学习将这些原子元素合成为目标动作，模型能够有效突破训练分布的限制。

值得注意的是，IDEA400 上的提升幅度远大于 Mixamo，这与两个数据集的性质差异一致——IDEA400 包含更多样化、更偏离 HumanML3D 分布的文本描述，而 Mixamo 的动作类型相对规整。这一差异从侧面印证了文本分解在弥合域间隙中的关键作用。

### 消融实验：模块贡献与机制验证

为量化各模块的独立贡献，我们在 HumanML3D 和 IDEA400 上进行了系统的消融实验，结果如表 2 所示。

**基线模型（Baseline）**：仅使用原始文本的掩码生成模型，在 IDEA400 上 FID 为 0.934，R-Precision 为 0.317。这一性能与 T2M-GPT 相当，构成了公平的消融起点。

**组合特征融合（Baseline + CFF）**：在基线模型上添加 CFF 模块后，IDEA400 的 FID 从 0.934 降至 **0.844**（降低 9.6%），R-Precision 从 0.317 提升至 0.363。这证明了在运动特征层面进行身体部位级别的原子信息融合，能够有效引导模型生成与文本描述更一致的动作。CFF 的核心机制在于：将运动嵌入按通道维度拆分为身体部位专家，以原子文本嵌入为键值进行交叉注意力，使每个部位的运动生成都能获得针对性的语义指导。

**文本-运动对齐（Baseline + TMA + CFF）**：进一步加入预训练的 TMA 模块后，IDEA400 的 R-Precision 跃升至 **0.449**，FID 进一步优化。TMA 模块通过 InfoNCE 对比损失在文本-运动对上预训练，为原子文本提供了与运动空间对齐的特征表示。消融结果表明，仅有特征融合而缺乏对齐的文本特征，原子重组的效率会受到显著限制。

**拼接融合的失败（CFF\*）**：将原子文本直接与原始文本拼接（而非通过 CFF 进行特征级融合）导致 IDEA400 的 FID 反弹至 0.886，接近纯基线水平。这一对比凸显了 CFF 设计的必要性——简单的文本拼接无法让模型学习到原子运动到目标动作的组合过程，而通道分组交叉注意力机制能够显式建模身体部位与原子描述之间的对应关系。

### 域间隙缩小的证据

文本分解算法在缩小训练与测试数据集之间的域间隙方面发挥了关键作用。如图 6 的 t-SNE 可视化所示，在使用原始文本时，HumanML3D 训练集与 IDEA400、Mixamo 测试集的文本嵌入分布存在明显分离。而经过文本分解算法转换为细粒度描述（左右上下肢、脊柱等身体部位的运动描述）后，不同数据集的分布在 t-SNE 空间中几乎完全重合。

这一现象揭示了本文方法泛化能力的底层机制：文本分解将多样化的开放域描述统一映射到由身体部位和运动原语构成的受限语义空间，该空间的维度由数据集中可观察的运动模式决定。因此，即使测试文本在表层语义上远离训练分布，其分解后的原子描述仍落在模型可处理的范围内，从而在文本层面消除了域间隙。

### 定性分析

图 5 展示了在开放词汇文本上的生成效果对比。对于训练中未见的复杂描述（如涉及多个身体部位协调的动作），MDM 和 T2M-GPT 往往生成语义不匹配或动作不自然的结果，而本文方法能够更准确地捕捉各身体部位的运动细节并合成为连贯的整体动作。这与定量结果一致，进一步验证了原子分解-重组框架在处理组合泛化方面的优势。

### 实验公平性说明

需要指出的是，本文方法使用额外的大规模未标注运动数据训练 Residual VQ-VAE，这可能为离散运动表示的质量带来一定的先验优势。虽然生成模型本身仅在 HumanML3D 标注数据上训练，但 VQ-VAE 的码本质量对下游生成性能存在间接影响。这一因素在与未使用额外数据的基线方法对比时需予以考虑，但其对域外泛化增益的贡献程度尚缺乏直接的消融验证。

### 补充图表

![[assets/figures/papers/paper_list_l5_Open_the_Motion_Door_Atomic_Motion_Decomposition_and_Recomposition_for_O/figures/005_Table_1.jpg]]
*Table 1: Comparison with state-of-the-arts on one in-domain dataset (HumanML3D) and two out-domain dataset (IDEA400 and Mixamo)*

![[assets/figures/papers/paper_list_l5_Open_the_Motion_Door_Atomic_Motion_Decomposition_and_Recomposition_for_O/figures/007_Table_2.jpg]]
*Table 2: Ablation Study on the HumanML3D and IDEA400 dataset. The TMA and CFF represent the text-motion-alignment module and the compositional feature fusion module. We denote directly concatenating atomic motion texts with raw texts as CFF**

![[assets/figures/papers/paper_list_l5_Open_the_Motion_Door_Atomic_Motion_Decomposition_and_Recomposition_for_O/figures/006_Figure_5.jpg]]
*Figure 5: Comparison with several state-of-the-arts on open vocabulary texts*

![[assets/figures/papers/paper_list_l5_Open_the_Motion_Door_Atomic_Motion_Decomposition_and_Recomposition_for_O/figures/008_Figure_6.jpg]]
*Figure 6: t-SNE comparison between raw text and the fine-grained description (left/right lower/upper limb, spine) by Textual Decomposition on a training dataset of HumanML3D and the test dataset of HumanML3D, IDEA400 and Mixamo. Textual Decomposition algorithm successfully reduces the domain gap between these datasets from the textual aspect*



## 定位与知识库关联

### 1. 与现有文本-运动生成范式的关系

本文提出的原子运动分解与重组框架，在概念上与现有文本-运动生成的三类主流范式形成明确对比（见 Figure 1）：

- **简单映射范式（Simple Mapping）**：以 **MDM**、**T2M-GPT**（Zhang et al., CVPR 2023）、**MMM**（Pinyoanuntapong et al., CVPR 2024）为代表，直接在文本-运动对上进行生成建模。这类方法的核心瓶颈在于：模型的泛化能力被训练数据的文本分布严格限定，面对域外开放词汇时性能急剧退化。本文在 IDEA400 上的实验直接验证了这一点——MDM 的 FID 高达 0.821，而本文方法降至 0.449。

- **跨域对齐范式（Other-domain Alignment）**：试图借助 CLIP 等预训练视觉-语言模型的语义空间来弥合文本域间隙。然而，这种间接对齐策略并未从根本上解决运动语义的组合泛化问题，对齐质量受限于中间模态的表达能力。

- **预训练-微调范式（Pretrain-then-Finetuning）**：先在大规模无标注数据上预训练运动表征，再在标注数据上微调。该方法虽然改善了运动先验，但文本端的域间隙依然存在——微调阶段仍然依赖有限的标注文本分布。

本文方法的根本区别在于：**不是在文本空间或特征空间做域适应，而是将开放域文本显式分解为受限于数据集维度的原子运动描述**，从而在输入端就缩小了域间隙。这一思路与 **ATOM**（Zhai et al., ACM MM 2023）的原子动作概念有表面相似性，但 ATOM 的原子动作是预定义的离散动作类别，而本文的原子运动是时空上可组合的身体部位运动描述，粒度更细、组合灵活性更强。

### 2. 关键技术组件的谱系定位

#### 2.1 残差 VQ-VAE 运动量化

运动离散化表示在运动生成领域已有一定探索。本文采用残差 VQ-VAE（RVQ）进行多层码本学习，这一选择在架构层面与 MMM 等掩码生成方法共享相似的离散生成建模思路。但本文的 RVQ 在**无标注运动数据**上训练，而非仅依赖 HumanML3D，这为后续的开放词汇泛化提供了更丰富的运动先验。需要注意的是，这一额外数据的使用在公平性上可能带来一定优势，消融实验中未对此进行独立量化。

#### 2.2 文本分解模块

文本分解是本文最具区分度的贡献。其核心逻辑是：**将任意开放域文本映射到一个 L×P 的原子运动文本矩阵**（L=6 个身体部位，P 个时间段），使得无论输入文本多么复杂或罕见，其分解后的描述都落在训练数据可覆盖的语义空间内。

这一设计在方法谱系中具有独特位置：它既不同于传统的文本增强（在原始文本空间做扰动），也不同于跨模态检索（将文本映射到运动检索库）。其实质是**利用人体运动的组合结构先验，对文本进行结构化解析**。训练阶段使用基于运动学规则的算法（如肘部弯曲角度余弦公式、姿态描述子累积变化量），推理阶段则借助大语言模型（LLM）完成分解，实现了从规则驱动到语义驱动的灵活切换。

Figure 6 的 t-SNE 可视化提供了关键证据：分解后的细粒度描述在 HumanML3D、IDEA400 和 Mixamo 三个数据集上的分布几乎重合，而原始文本分布则存在明显分离。这直接证明了文本分解在缩小域间隙方面的因果作用。

#### 2.3 文本-运动对齐与组合特征融合

TMA 模块采用对比学习（InfoNCE 损失）在文本-运动对上预训练，其设计思路与 CLIP 式的跨模态对齐一脉相承，但不同之处在于：TMA 对齐的是**原子文本**与运动特征，而非全局文本-运动对。这使得对齐粒度更细，能够捕捉身体部位级别的语义-运动对应关系。

CFF 模块的设计则与多专家融合（Mixture of Experts）和交叉注意力机制有方法上的亲缘关系。其核心创新在于：将运动特征按通道维度拆分为对应不同身体部位的“专家”组，以原子文本嵌入作为键值进行交叉注意力融合。消融实验（Table 2）直接验证了这一设计的必要性——将 CFF 替换为简单的文本拼接（CFF\*）导致 IDEA400 上的 FID 从 0.844 反弹至 0.886。

### 3. 适用边界与局限

**适用边界**：

- 该方法在**全身人体运动**的开放词汇生成上表现出色，尤其是涉及四肢、躯干、根轨迹等可分解的身体部位运动。
- 对训练数据中未见过的文本描述（如“像僵尸一样行走，同时挥舞手臂”）具有显著优于基线的泛化能力，这源于原子运动的组合性。
- 方法框架与具体的生成模型架构（如 Transformer 掩码生成）解耦，CFF 模块可作为插件嵌入其他生成架构。

**已知局限**：

- 身体部位划分固定为 6 类（脊柱、左右上肢、左右下肢、根轨迹），对于**细粒度手势、手指动作或面部表情**等更精细的运动类型覆盖不足。这是原子运动粒度的固有限制。
- LLM 驱动的推理阶段文本分解在**极端语义歧义或高度抽象描述**上的可靠性未经系统验证。错误的原子分解将直接传递到运动生成阶段，产生语义不一致的运动。
- 额外使用的无标注运动数据的规模和质量对 RVQ 性能的影响未进行消融实验，无法判断该方法对运动数据质量的敏感度。

### 4. 开放问题

1. **原子分解粒度的扩展**：当前 6 类身体部位划分是否可通过引入层级化分解（如手部关节级分解）来覆盖更精细的运动类型？这需要在分解粒度和组合复杂度之间寻找平衡。

2. **LLM 分解的鲁棒性**：推理阶段依赖 LLM 进行文本分解，当输入文本包含歧义、反事实描述或文化特定动作时，LLM 的分解质量如何？错误的原子描述将如何影响 CFF 模块的融合结果？需要建立分解质量的评估和纠错机制。

3. **多智能体与交互扩展**：该方法的核心假设是单人全身运动的可分解性。对于**多人物交互或人-物交互**场景，原子运动的定义和重组机制需要根本性的重新设计——交互约束使得身体部位运动不再是独立的可组合单元。

4. **数据依赖的消融**：RVQ 训练中使用的额外无标注运动数据的规模和质量对最终开放词汇性能的贡献需要独立评估，以区分方法创新和数据增益各自的因果效应。



## 原文 PDF

![[paperPDFs/CVPR_2026/Open_the_Motion_Door_Atomic_Motion_Decomposition_and_Recomposition.pdf]]
