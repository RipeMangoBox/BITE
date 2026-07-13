---
title: Textual Decomposition Then Sub-Motion-Space Scattering for Open-Vocabulary Motion Generation
type: paper
paper_level: A
venue: arXiv
year: 2024
pdf_ref: paperPDFs/arxiv_2024/DSONet_Textual_Decomposition_Then_Sub_Motion_Space_Scattering_for_Open_Vocabulary_Motion_Generation.pdf
project_link: https://vankouf.github.io/DSONet/
code_link: null
aliases:
- DSONet
- DSO-Net
tags:
- arxiv_2024
- topic/motion_animation
- topic/motion_animation/human_motion_generation
core_operator: 将原始动作文本分解为低级别、具体的原子动作描述（每个描述一个简单身体部位在短时间内的运动），并让模型显式学习从原子动作组合到目标动作的生成过程，从而将子动作空间散射到整个动作空间，使开放域样本从外推转化为插值。
primary_logic: 人类理解动作时倾向于将复杂运动拆分为若干身体部位在短时间内的简单动作（原子动作），这些原子动作描述是跨领域共享的低级特征。利用原子动作作为中间表示，可将开放词汇动作生成分解为两个有序步骤：先通过文本分解将任意动作文本转换为原子动作文本（全文本空间→全原子文本空间），再通过子动作空间散射学习原子动作到完整动作的组合过程（全原子文本空间→全动作空间），从而建立全映射并极大提升泛化能力。
claims:
- 在Idea400和Mixamo两个开放域数据集上，所提方法在所有指标上均显著优于SOTA。
- 消融实验证实，CFF模块（组合特征融合）和TMA模块（文本-动作对齐）对开放词汇性能有决定性提升，且两者协同效应显著。
- 定性结果展示，只有DSO-Net能正确理解动作的时间顺序（如“站立到跪下”），而其他方法则混淆或生成不符合语义的动作。
- 文本分解将原始动作文本转化为覆盖六个身体部位（脊柱、左右上下肢、轨迹）的多时间段原子动作文本，通过LLM的上下文学习实现泛化。
---

# Textual Decomposition Then Sub-Motion-Space Scattering for Open-Vocabulary Motion Generation

> [!tip] 核心洞察
> 人类理解动作时倾向于将复杂运动拆分为若干身体部位在短时间内的简单动作（原子动作），这些原子动作描述是跨领域共享的低级特征。利用原子动作作为中间表示，可将开放词汇动作生成分解为两个有序步骤：先通过文本分解将任意动作文本转换为原子动作文本（全文本空间→全原子文本空间），再通过子动作空间散射学习原子动作到完整动作的组合过程（全原子文本空间→全动作空间），从而建立全映射并极大提升泛化能力。

| 字段 | 内容 |
|------|------|
| 中文题名 | 基于文本分解与子运动空间散射的开放词汇动作生成 |
| 英文题名 | Textual Decomposition Then Sub-Motion-Space Scattering for Open-Vocabulary Motion Generation |
| 会议/期刊 | arXiv 2024 |
| Links | [paper](https://arxiv.org/abs/2411.04079) · [Project](https://vankouf.github.io/DSONet/) |
| Topic | #topic/motion_animation #topic/motion_animation/human_motion_generation |
| Method | DSO-Net |
| Dataset | HumanML3D, Idea400, Mixamo |

> [!tip] 效果简介
> - HumanML3D (in-domain) 上，FID 0.027。
> - HumanML3D 上，R-Precision 0.957；Diversity 1.388。
> - Idea400 (out-domain) 上，FID 0.847。

## 概要

**问题瓶颈**：开放词汇动作生成（Open-Vocabulary Motion Generation）的核心挑战在于，现有方法受限于标注数据规模，仅能学习**子文本空间到子动作空间的映射**（子空间拟合）。当面对训练分布之外的新颖文本描述时，模型被迫进行外推（extrapolation），导致语义理解错误、动作质量下降，泛化能力严重不足。

**核心思路**：本文提出 **DSO-Net**，将开放词汇动作生成转化为两个有序耦合的阶段——**文本分解（Textual Decomposition）** 与 **子运动空间散射（Sub-Motion-Space Scattering）**。其关键洞见在于：人类理解复杂动作时，天然地将其拆解为若干身体部位在短时间内的简单原子动作。利用这一特性，DSO-Net 先将任意开放词汇文本分解为覆盖六个身体部位（脊柱、左右上下肢、轨迹）的多时间段原子动作描述，再通过显式学习原子动作到完整动作的组合过程，将原本需要外推的开放域样本转化为插值（interpolation），从而建立从全文本空间到全动作空间的映射。

**方法定位**：DSO-Net 采用“预训练-微调”范式，在方法论谱系中处于**离散生成建模**与**组合式文本-动作对齐**的交汇点。与 **OMG**（Liang et al., CVPR 2024）的预训练-微调路线、**MotionCLIP**（Tevet et al., ECCV 2022）的 CLIP 对齐路线，以及 **MoMask**（Guo et al., CVPR 2024）的离散掩码建模路线相比，DSO-Net 的差异化优势在于引入了原子动作作为中间表示，并通过文本-动作对齐模块（TMA）和组合特征融合模块（CFF）显式建模组合过程，而非依赖单一粗粒度文本的直接条件生成。

**主要结果**：在域内数据集 HumanML3D 和两个开放域数据集 Idea400、Mixamo 上，DSO-Net 在所有评估指标上均显著优于现有 SOTA 方法（Table 1）。消融实验证实，TMA 模块与 CFF 模块对开放词汇性能有决定性贡献，且两者存在显著的协同效应——当 TMA 存在时，CFF 带来的 R-Precision Top3 提升达 11%，而单独使用 CFF 仅提升 3%（Table 2）。定性结果进一步表明，只有 DSO-Net 能正确理解动作的时间顺序（如“站立到跪下”），其他方法则混淆或生成语义不符的动作（Figure 5, Figure 6）。

### 问题背景：文本到动作生成的泛化困境

文本驱动的人体动作生成旨在根据自然语言描述合成逼真的三维人体运动序列，在动画制作、虚拟现实、人机交互等领域具有广泛的应用前景。近年来，基于深度生成模型的方法在这一任务上取得了显著进展，主流技术路线包括直接映射方法（如**T2M-GPT**、**MDM**、**MotionDiffuse**）、基于CLIP对齐的方法（如**MotionCLIP**，Tevet et al., ECCV 2022；**OOHGM**，Lin et al., CVPR 2023），以及预训练-微调方法（如**OMG**，Liang et al., CVPR 2024）。然而，这些方法的共同局限在于：它们仅在有限的标注数据集（如HumanML3D）上训练，模型实际学习到的只是**子文本空间到子动作空间的映射**——即训练数据所覆盖的文本描述范围与对应动作模式之间的对应关系。

### 根本瓶颈：子空间拟合与外推失效

这一局限性的本质可归结为一个核心矛盾：**标注数据规模有限，导致模型只能实现子空间拟合，对于训练分布之外的开放词汇文本需要外推，而外推能力严重不足**。具体而言，现有方法在域内（in-domain）测试集上表现良好，但一旦面对训练数据中未曾出现或组合方式新颖的开放词汇描述（open-vocabulary texts），生成质量急剧下降。这种退化并非偶然——当输入文本落在模型所学习的子空间之外时，模型被迫进行分布外外推，而缺乏对动作组合规律的显式建模使得外推结果不可控、语义不一致。

### 现有范式的结构性缺陷

从方法论角度审视，现有三种主流范式均存在结构性缺陷：

- **简单映射方法**（如T2M-GPT、MoMask）：直接将粗粒度文本嵌入映射到动作空间，文本表示缺乏细粒度的运动语义分解，无法捕捉复杂动作中多个身体部位的协同变化。
- **基于CLIP对齐的方法**（如MotionCLIP、OOHGM）：依赖CLIP空间的跨模态对齐，但CLIP本身并非为细粒度运动理解设计，其文本编码难以精确描述身体部位级别的运动特征。
- **预训练-微调方法**（如OMG）：虽然利用大规模无标注数据预训练动作先验，但微调阶段仍在小规模标注数据上进行，本质上仍受限于子空间学习，未能从根本上解决泛化问题。

这些方法的共同盲点在于：**它们试图直接从单一粗粒度文本描述映射到完整动作序列，跳过了人类理解运动时的自然分解过程**。

### 本文动机：从外推到插值的范式转换

本文的核心洞察源于对人类运动认知方式的反思：**人类在理解复杂动作时，倾向于将其拆分为若干身体部位在短时间内的简单动作（原子动作）**。例如，“一个人边走边挥手”可以被自然地分解为“下肢交替迈步前行”和“上肢有节奏地左右摆动”等原子动作描述。这些原子动作描述具有跨领域共享的低级特征属性，构成了连接任意开放词汇文本与具体运动模式之间的理想中间表示。

基于这一洞察，本文提出了一种根本性的范式转换：**将开放词汇动作生成从外推问题转化为插值问题**。具体而言，通过两个有序耦合的步骤建立全映射：

1. **文本分解（Textual Decomposition）**：将任意开放词汇运动文本分解为覆盖六个身体部位（脊柱、左上肢、右上肢、左下肢、右下肢、轨迹）的多时间段原子动作文本，实现从**全文本空间到全原子文本空间**的映射。
2. **子动作空间散射（Sub-Motion-Space Scattering）**：显式学习从原子动作组合到目标完整动作的生成过程，将模型在有限标注数据上学到的子动作空间散射到整个动作空间，实现从**全原子文本空间到全动作空间**的映射。

通过这一设计，原本需要外推的开放域样本被转化为在原子动作空间内的插值，从而在根本上突破了子空间拟合的局限，使模型在有限标注数据下仍能生成符合开放词汇语义的高质量动作。

## 核心方法与创新机理

DSO-Net 的核心创新在于将开放词汇动作生成这一困难的外推问题，通过**文本分解**与**子运动空间散射**两步有序转化，重塑为一个可控的插值问题，从而在有限标注数据下建立起从全文本空间到全动作空间的映射能力。

### 1. 从子空间拟合到全空间映射的范式跃迁

当前开放词汇动作生成方法（如 **OMG** (Liang et al., CVPR 2024)、**MotionCLIP** (Tevet et al., ECCV 2022)、**OOHGM** (Lin et al., CVPR 2023) 等）的根本瓶颈在于**子空间拟合**：受限于标注数据规模，模型只能学习到一个有限的子文本空间到子动作空间的直接映射。当面对训练分布之外的开放词汇文本时，模型被迫进行**外推**，导致生成质量急剧下降。

DSO-Net 改变了这一底层映射逻辑。如 Figure 1 所示，该方法将原本需要外推的“全文本空间→全动作空间”映射，分解为两个有序耦合的阶段：
1. **文本分解**：将任意开放词汇动作文本转换为原子动作文本（全文本空间→全原子文本空间）。
2. **子运动空间散射**：学习从原子动作组合到目标动作的生成过程（全原子文本空间→全动作空间）。

这一设计的核心洞察在于：原子动作描述（如“左上肢弯曲”“脊柱前倾”等）是跨领域共享的低级特征，其组合空间远小于原始文本空间。通过将开放域样本映射到原子动作空间，原本需要外推的样本被转化为已知原子动作的**插值组合**，从而在根本上解决了泛化瓶颈。

### 2. 文本表示：从粗粒度描述到结构化原子文本

传统方法使用单一的粗粒度动作文本（如“一个人边走边挥手”）作为条件输入，这种全局描述难以捕捉复杂动作的时空结构与身体部位协同关系。

DSO-Net 引入了**结构化原子文本表示**，将每个动作文本分解为覆盖六个身体部位（脊柱、左上肢、右上肢、左下肢、右下肢、轨迹）在多个时间段上的原子动作描述。每个原子文本仅描述一个简单身体部位在短时间内的运动，例如“时间段1：右上肢向前摆动，幅度较大”。这种分解通过以下机制实现：
- **LLM 上下文学习**：在推理时，利用大语言模型的上下文学习能力，将任意开放词汇文本分解为多时间段、多部位的原子动作文本（见 Section 3.1 及 Appendix C）。
- **细粒度描述转换算法**：在训练阶段，该算法从动作数据中提取速度、幅度、具体行为等信息，辅助构造高质量的原子文本对，确保 LLM 分解的质量。

这一表示变化使得模型能够以组合的方式理解复杂动作，而非将其视为一个不可分割的整体。

### 3. 动作生成中的组合建模：CFF 模块的显式融合机制

传统方法在生成过程中缺乏显式的组合建模——它们将文本条件直接注入生成网络，由网络隐式地学习文本与动作之间的对应关系。这种隐式学习在数据有限时极易过拟合到训练分布中的表层关联。

DSO-Net 通过**组合特征融合（CFF）模块**实现了显式的原子动作组合建模。如 Figure 3 所示，CFF 模块的核心机制是：
- **按身体部位拆分特征**：将运动特征按 L 个身体部位进行空间划分。
- **交叉注意力融合**：利用交叉注意力机制，将各身体部位对应的原子文本特征分别注入到相应部位的运动特征中，显式地建模“哪个原子动作控制哪个身体部位”的组合关系。

这一设计使得模型不再需要从单一全局文本中隐式推断部位对应关系，而是直接利用结构化的原子文本进行精确的条件注入。消融实验证实，CFF 模块对开放域性能有决定性提升（Table 2）。

### 4. 文本-动作对齐：TMA 模块的专门化特征提取

传统方法通常使用通用文本编码器（如 CLIP）直接提取文本特征用于条件生成。然而，通用编码器并非为原子动作文本这一特定领域设计，其提取的特征可能无法与运动空间良好对齐。

DSO-Net 引入了**文本-动作对齐（TMA）模块**，专门针对原子动作文本进行特征提取。该模块通过对比学习（InfoNCE loss）进行预训练，将原子文本特征与对应的运动特征拉近，同时推远不匹配的样本对。这使得 TMA 提取的特征天然地与动作空间对齐，为后续 CFF 模块的组合融合提供了高质量的条件信号。

消融实验揭示了 TMA 与 CFF 的**协同效应**（Table 2, Section 4.3）：当 TMA 存在时，CFF 带来的 R-Precision Top3 提升为 11%（+0.073），而单独使用 CFF 仅提升 3%。这表明专门化的文本-动作对齐是显式组合建模发挥效用的前提——只有原子文本特征与动作空间良好对齐，按部位的交叉注意力融合才能准确地注入组合关系。

### 5. 关键创新总结

| 变化维度 | 基线方法 | DSO-Net |
|---------|---------|---------|
| 映射范围 | 子空间拟合，需外推 | 全空间映射，外推转插值 |
| 文本表示 | 单一粗粒度描述 | 多时段、六部位结构化原子文本 |
| 组合建模 | 隐式条件注入 | CFF 模块按部位显式交叉注意力融合 |
| 文本-动作对齐 | 通用编码器（如 CLIP） | TMA 模块对比学习专门对齐 |

这四个维度的创新相互耦合，共同构成了从“子空间拟合”到“全空间散射”的范式跃迁。其决定性证据来自 Table 1：在 Idea400 和 Mixamo 两个开放域数据集上，DSO-Net 在所有指标上均显著优于 SOTA 方法，且定性结果（Figure 5, Figure 6）显示只有 DSO-Net 能正确理解动作的时间顺序（如“站立到跪下”），而其他方法则混淆或生成不符合语义的动作。

DSO-Net采用“预训练-微调”范式，整体流程分为两个阶段：**运动预训练**（Motion Pre-Training）和**运动微调**（Motion Fine-tuning），如Figure 2所示。

### 运动预训练阶段

该阶段的目标是学习大规模运动先验。DSO-Net使用**残差VQ-VAE**（Residual VQ-VAE, RVQ）将连续的运动序列量化为多层离散token。RVQ包含一个基础层（base layer）和多个残差层（residual layers），逐层学习码本（codebooks），从而将运动序列编码为多层离散表示。预训练在大规模未标注运动数据（超过22M帧）上进行，使模型掌握丰富的运动模式先验。

### 运动微调阶段

微调阶段在少量文本-运动配对数据上进行，核心是将开放词汇动作生成分解为两个有序耦合的子过程：

1. **文本分解**（Textual Decomposition）：利用大语言模型（LLM）的上下文学习能力，将任意原始动作文本分解为多个时间段、覆盖六个身体部位（脊柱、左右上肢、左右下肢、轨迹）的原子动作文本。每个原子文本描述一个简单身体部位在短时间内的运动。训练阶段还使用细粒度描述转换算法辅助构造原子文本对。

2. **子运动空间散射**（Sub-motion-space Scattering）：通过两个关键模块显式学习从原子动作到目标动作的组合过程：
   - **文本-动作对齐模块**（TMA）：提取原子文本特征，通过对比学习（InfoNCE loss）与动作特征对齐，输出用于融合的原子特征矩阵。
   - **组合特征融合模块**（CFF）：按身体部位拆分运动特征，利用交叉注意力机制将原子文本特征注入运动特征，显式建模原子动作的空间组合关系。

### 生成流程

在推理时，对于给定的开放词汇文本：
1. LLM将其分解为原子动作文本矩阵。
2. TMA模块提取原子文本特征。
3. 掩码Transformer（由多个Transformer层与CFF模块堆叠而成）以掩码建模方式迭代预测离散运动token：每层先通过Transformer层融合原始文本特征与掩码运动嵌入，再通过CFF模块注入原子文本的组合信息，最终解码为完整运动序列。

这一设计将传统方法的“子空间拟合+外推”转化为“全空间映射+插值”，从根本上提升了开放词汇动作生成的泛化能力。

### 补充图表

![[assets/figures/papers/DSONet_Textual_Decomposition_Then_Sub-Motion-Space_Scattering_for_Open-Vocabular_aab01d075189/figures/003_Figure_2.jpg]]
*Figure 2: The architecture of our entire framework. The overall pipeline adopts discrete generative modeling. 1) In the Motion Pre-Training stage (left blue part), we use the Residual VQ-VAE (RVQ) model, which designs a base layer and R residual layers to learn layer-wise codebooks. By tokenizing the motion sequence into multi-layer discrete tokens, we learn the large-scale motion priors. 2) In the Motion Fine-tuning stage (right green part), we first leverage the large language model(LLM) and the fine-grained description conversion algorithm we design (only used in training stage) to perform texutal decomposition, which convert the raw text of a motion into the atomic texts. Then, for the base layer...*

DSO-Net 的核心由两个有序耦合的阶段构成：**文本分解（Textual Decomposition）** 和 **子动作空间散射（Sub-Motion-Space Scattering）**。前者将开放词汇的粗粒度运动文本转换为结构化的原子动作描述；后者通过显式建模原子动作到目标动作的组合过程，将原本需要外推的子空间映射转化为插值，从而建立全文本空间到全动作空间的映射。

### 文本分解（Textual Decomposition）

文本分解的目标是将任意给定的运动文本转化为若干原子动作文本，每条原子文本描述一个简单身体部位在短时间内的运动。分解过程依赖大语言模型（LLM）的上下文学习能力：给定少量人工标注的分解示例，LLM 将运动文本拆分为多个时间段，并在每个时间段内为六个身体部位（脊柱、左上肢、右上肢、左下肢、右下肢、轨迹）分别生成原子动作描述。

在训练阶段，为辅助构造高质量的文本-动作对，论文设计了一个**细粒度描述转换算法（Fine-grained Description Conversion Algorithm）**。该算法从动作序列中提取姿态信息，用于生成包含速度、幅度、具体行为等细节的运动描述，再交由 LLM 进行分解。其中，上肢弯曲幅度的计算依赖以下公式（Section 3.1, Eq.(1)）：

$$
\frac{J_{shoulder} - J_{elbow}}{||J_{shoulder} - J_{elbow}||} \odot \frac{J_{wrist} - J_{elbow}}{||J_{wrist} - J_{elbow}||}
$$

该式通过肘关节到肩关节的单位向量与肘关节到腕关节的单位向量的内积，定量刻画上肢的弯曲程度。推理时，LLM 仅需上下文示例即可完成分解，无需访问动作数据，从而保证开放词汇场景下的泛化能力。

### 子动作空间散射（Sub-Motion-Space Scattering）

子动作空间散射的核心是学习从原子动作到目标动作的组合过程。该过程由两个关键模块协同完成：**文本-动作对齐模块（TMA）** 和 **组合特征融合模块（CFF）**。

#### TMA 模块

TMA 模块负责提取原子文本特征并将其对齐到动作特征空间。该模块通过对比学习预训练获得，使用 InfoNCE 损失拉近匹配的文本-动作对，推远不匹配的样本对。损失函数形式如下（Section 3.2）：

$$
\mathcal{L}_{\mathrm{NCE}} = -\frac{1}{2M}\sum_{i}\left( \log\frac{\exp A_{ii}/\tau}{\sum_{j}\exp A_{ij}/\tau} + \log\frac{\exp A_{ii}/\tau}{\sum_{j}\exp A_{ji}/\tau} \right)
$$

其中 $A$ 为文本特征与动作特征的相似度矩阵，$\tau$ 为温度系数。训练后的 TMA 模块将原子文本矩阵 $W$（维度为 $L \times d$，$L$ 为身体部位数）映射为对齐后的原子特征矩阵，作为 CFF 模块的输入。

#### CFF 模块

CFF 模块的核心机制是按身体部位进行交叉注意力融合。如 Figure 3 所示，掩码运动嵌入 $\tilde{m}$ 首先与原始文本特征 $T_r$ 拼接，经 Transformer 层处理：

![[assets/figures/papers/DSONet_Textual_Decomposition_Then_Sub-Motion-Space_Scattering_for_Open-Vocabular_aab01d075189/figures/004_Figure_3.jpg]]
*Figure 3: Details of the compositional feature fusion (CFF) module, where the atomic text matrix is input into the TMA module for feature extraction, and is fused with the motion feature by crossattention*

$$
T_r^o, \tilde{m}^1 = \mathcal{F}_{Transformer}(T_r; \tilde{m})
$$

随后，CFF 模块以原子文本特征 $W$ 为条件，通过交叉注意力将其与运动特征 $\tilde{m}^2$ 进行空间组合式融合：

$$
\tilde{m}^3 = \mathcal{F}_{CFF}(\tilde{m}^2; W)
$$

这一设计使模型显式地学习不同身体部位原子动作的组合关系，而非隐式地从粗粒度文本直接映射到完整动作。消融实验（Table 2）证实，CFF 与 TMA 存在显著的协同效应：当 TMA 存在时，CFF 带来的 R-Precision Top3 提升达 11%（+0.073），而单独使用 CFF 仅提升 3%，表明原子文本对齐与组合建模互为补充，共同驱动子动作空间的有效散射。

## 实验与关键发现

### 主实验结果

DSO-Net 在域内数据集 HumanML3D 和两个开放域数据集 Idea400、Mixamo 上进行了系统评估，对比方法包括基于预训练-微调的 **OMG**（Liang et al., CVPR 2024）、基于 CLIP 对齐的 **MotionCLIP**（Tevet et al., ECCV 2022）、**OOHGM**（Lin et al., CVPR 2023）、离散掩码建模方法 **MoMask**（Guo et al., CVPR 2024），以及扩散模型方法 MDM、MotionDiffuse 和自回归方法 T2M-GPT。完整定量结果见 **Table 1**。

![[assets/figures/papers/DSONet_Textual_Decomposition_Then_Sub-Motion-Space_Scattering_for_Open-Vocabular_aab01d075189/figures/005_Table_1.jpg]]
*Table 1: Comparison with state-of-the-arts on one in-domain dataset (HumanML3D) and two outdomain dataset (Idea400 and Mixamo)*

**域内性能（HumanML3D）**：在标准评测协议下，DSO-Net 取得了极具竞争力的结果。FID 达到 **0.027**，R-Precision Top1 达到 **0.957**，Diversity 为 **1.388**，表明模型在训练分布内的生成质量和文本-动作对齐精度均达到 SOTA 水平。

**开放域性能（Idea400 & Mixamo）**：这是验证开放词汇泛化能力的核心场景。在 Idea400 上，DSO-Net 的 FID 降至 **0.847**，R-Precision Top1 达到 **0.703**，在所有指标上均显著优于对比方法。在 Mixamo 上，FID 为 **0.186**，R-Precision Top1 为 **0.807**，同样全面领先。这两个数据集包含训练阶段未见过的动作描述，DSO-Net 的优势直接验证了文本分解与子动作空间散射将外推转化为插值的核心机制。

### 消融实验

为量化各组件的独立贡献与协同效应，在 Idea400 上进行了消融实验（**Table 2**），逐步剥离预训练、TMA 模块和 CFF 模块。

![[assets/figures/papers/DSONet_Textual_Decomposition_Then_Sub-Motion-Space_Scattering_for_Open-Vocabular_aab01d075189/figures/008_Figure_4.jpg]]
*Figure 4: Comparison with several state-of-the-arts on open vocabulary texts. Table 2: Ablation Study on the Idea400 dataset. The TMA and CFF represent the text-motionalignment module and the compositional feature fusion module*

**预训练的作用**：在大规模未标注数据（超 22M 帧）上进行 Residual VQ-VAE 预训练，为模型提供了丰富的运动先验。消融显示，去除预训练后 FID 上升约 1-2%，说明预训练对生成质量有稳定但非决定性的贡献——真正的开放词汇突破来自微调阶段的文本分解与组合建模。

**TMA 模块的关键性**：文本-动作对齐模块负责提取原子文本特征并与动作特征对齐。加入 TMA 后，R-Precision Top3 几乎翻倍（从约 0.2x 升至约 0.44），证明原子文本级别的精确对齐是开放词汇理解的瓶颈——没有 TMA，模型无法有效利用原子文本中蕴含的细粒度语义信息。

**CFF 模块的组合建模能力**：组合特征融合模块通过按身体部位拆分并进行交叉注意力融合，显式建模原子动作的组合过程。消融显示，CFF 模块显著提升开放域 FID 和 R-Precision，验证了显式组合建模对于泛化到未见动作组合的必要性。

**TMA 与 CFF 的协同效应**：当 TMA 存在时，CFF 带来的 R-Precision Top3 提升达 **11%（+0.073）**；而单独使用 CFF 仅提升约 3%。这一显著差异表明：原子文本的精确对齐（TMA）为组合融合（CFF）提供了高质量的语义输入，两者形成互补——TMA 负责“理解什么”，CFF 负责“如何组合”，缺一不可。

### 定性分析

**Figure 4** 展示了多个开放词汇文本下不同方法的生成结果对比。DSO-Net 生成的动作为唯一能准确对应文本语义的结果，而基线方法普遍出现语义混淆或动作缺失。

**Figure 5** 进一步聚焦于时序敏感的动作，如“站立到跪下”。DSO-Net 正确生成了从站立姿态逐渐过渡到跪下姿态的完整时序动作；而其他方法或混淆了动作顺序，或生成了不符合语义的静态姿态。这验证了文本分解将动作按时间段拆分后，模型能够学习到原子动作间的时间组合关系。

**Figure 6** 展示了更复杂的组合动作，如“举起物体行走”和“边走边欢呼”。这些动作要求多个身体部位同时执行不同子动作。DSO-Net 通过 CFF 模块按身体部位融合原子文本特征，成功生成了协调的多部位组合动作，而基线方法往往只能捕捉主导动作，丢失了并发子动作的语义。

### 失败模式与局限

尽管 DSO-Net 在开放词汇场景下表现优异，仍存在一些可观察的局限：

1. **原子动作分解的覆盖边界**：文本分解依赖 LLM 的上下文学习能力，对于极端新颖或抽象的动作描述（如比喻性表达、跨文化特有动作），LLM 可能无法准确分解为预定义的六部位原子动作格式，导致生成质量下降。这一点的定量边界需要进一步验证。

2. **部位划分的刚性**：当前固定将身体划分为脊柱、左右上下肢和轨迹六个部位。对于涉及手指、面部表情等更细粒度部位的动作，或需要动态调整部位粒度的场景，该划分方式可能不足。

3. **组合复杂度上限**：当原子动作数量过多或部位间交互过于复杂时，CFF 模块的交叉注意力机制可能面临信息瓶颈，导致部分原子语义在融合过程中被稀释。

### 补充图表

![[assets/figures/papers/DSONet_Textual_Decomposition_Then_Sub-Motion-Space_Scattering_for_Open-Vocabular_aab01d075189/figures/009_Figure_5.jpg]]
*Figure 5: Qualitative results compared with previous state-of-the-arts*

![[assets/figures/papers/DSONet_Textual_Decomposition_Then_Sub-Motion-Space_Scattering_for_Open-Vocabular_aab01d075189/figures/010_Figure_6.jpg]]
*Figure 6: Qualitative results compared with previous state-of-the-arts*

## 定位与知识库关联

### 1. 问题定位：从子空间拟合到全空间映射

现有文本到动作生成方法的核心瓶颈在于**子空间拟合**：由于带标注的文本-动作对数据规模有限（通常仅数万条），模型只能学习到有限的子文本空间到子动作空间的映射。当面对开放词汇（Open-Vocabulary）文本——即训练分布之外的描述——模型被迫进行**外推**，泛化能力急剧下降。DSO-Net 将此问题重新定义为：如何将外推转化为插值，从而建立从全文本空间到全动作空间的完整映射。

### 2. 与现有范式的对比

DSO-Net 与三类主流文本-动作生成范式形成鲜明对照（Figure 1）：

- **简单映射方法**（如 **T2M-GPT**、**MDM**、**MotionDiffuse**）：直接在有限标注数据上学习文本到动作的条件生成，缺乏对开放词汇的外推机制。这类方法在域内数据集上表现尚可，但在开放域数据集上性能急剧退化。

- **基于 CLIP 对齐的方法**：**MotionCLIP** (Tevet et al., ECCV 2022) 和 **OOHGM** (Lin et al., CVPR 2023) 尝试利用 CLIP 的跨模态表示能力，将动作生成对齐到 CLIP 的联合嵌入空间。然而，CLIP 的文本编码器本身并非为细粒度人体运动描述设计，其对复杂动作语义的捕捉能力有限，且对齐过程并未解决子空间外推的本质问题。

- **预训练-微调方法**：**OMG** (Liang et al., CVPR 2024) 采用大规模无标注动作数据预训练，再在标注数据上微调的范式。尽管预训练提供了丰富的运动先验，微调阶段仍受限于标注数据的子空间覆盖范围，开放词汇泛化依然依赖外推。

- **离散掩码建模方法**：**MoMask** (Guo et al., CVPR 2024) 在离散 token 空间进行掩码生成建模，在域内取得优异性能，但其文本条件机制未针对开放词汇的组合泛化进行专门设计。

DSO-Net 的关键差异在于**引入了中间表示层**：通过文本分解将任意动作文本转化为原子动作文本，再通过子动作空间散射学习原子动作到完整动作的组合过程。这一设计将原本需要外推的开放域样本转化为原子动作空间的插值问题。

### 3. 方法谱系中的结构性创新

DSO-Net 在以下四个维度上改变了基线方法的设计假设：

| 设计维度 | 基线方法 | DSO-Net |
|---------|---------|---------|
| 文本到动作的映射范围 | 子文本空间→子动作空间（外推） | 全文本空间→全动作空间（插值） |
| 文本表示粒度 | 单一粗粒度描述 | 多时间段、六身体部位的原子动作文本 |
| 组合建模 | 无显式组合过程 | CFF 模块按身体部位交叉注意力融合 |
| 文本-动作对齐 | 通用编码器（CLIP）或直接嵌入 | 预训练 TMA 模块（对比学习） |

这种设计使得 DSO-Net 在**方法谱系上属于“分解-组合”范式**，与计算机视觉中的 part-based model 和自然语言处理中的 compositional generalization 研究共享核心思想，但在动作生成领域首次将这一思想系统性地应用于开放词汇场景。

### 4. 适用边界与局限

尽管 DSO-Net 在开放词汇动作生成上取得了显著突破，其方法设计存在以下适用边界：

- **对 LLM 的依赖**：文本分解依赖大语言模型的上下文学习能力。当 LLM 对某些特殊运动领域（如专业舞蹈术语、极限运动）的知识不足时，分解质量可能下降。论文未提供 LLM 失效时的退化分析。

- **身体部位划分的固定性**：六部位划分（脊柱、左右上下肢、轨迹）基于人体运动学常识，但对于涉及手指、面部表情等细粒度运动的场景，当前划分可能不够充分。论文未探讨动态调整部位数量的可能性。

- **原子动作定义的先验性**：训练阶段的细粒度描述转换算法依赖人工设计的规则（如关节角度计算），这限制了原子动作空间的覆盖范围。如何完全通过数据驱动学习原子动作表示，仍是开放问题。

- **预训练数据的分布偏差**：预训练使用超过 22M 帧的多源数据，但微调仅在 HumanML3D 上进行。当目标开放域的动作风格与预训练数据差异较大时，运动先验的迁移效果可能受限。

### 5. 开放问题

从 DSO-Net 的设计出发，以下问题值得进一步探索：

1. **自动化原子动作发现**：能否摆脱对人工规则和 LLM 的依赖，通过无监督或自监督学习直接从动作数据中提取原子动作基元？这涉及动作表示学习中的 disentanglement 和 compositionality 问题。

2. **原子分解的完备性**：当前分解的覆盖范围能否处理完全新颖的开放词汇，例如涉及多主体交互或抽象情感描述的动作？分解粒度是否存在理论上界？

3. **子动作空间散射的理论基础**：论文将散射描述为“将外推转化为插值”，但未给出形式化定义。能否将这一过程建模为分布匹配或流形变换问题，从而提供泛化能力的理论保证？

4. **标注数据效率的极限**：DSO-Net 证明了在有限标注下通过分解-组合可显著提升泛化，但标注数据量的下限在哪里？是否存在样本复杂度的理论分析？

5. **与基础模型的深度整合**：当前 LLM 仅用于文本分解，动作生成仍由专用模型完成。未来是否可能构建统一的文本-动作基础模型，将分解和生成纳入端到端框架？

## 原文 PDF

![[paperPDFs/arxiv_2024/DSONet_Textual_Decomposition_Then_Sub_Motion_Space_Scattering_for_Open_Vocabulary_Motion_Generation.pdf]]
