---
title: "GenHOI: Generalizing Text-driven 4D Human-Object Interaction Synthesis for Unseen Objects"
type: paper
paper_level: A
venue: arXiv
year: 2025
pdf_ref: paperPDFs/arxiv_2025/GenHOI_Generalizing_Text_driven_4D_Human_Object_Interaction_Synthesis_for_Unseen_Objects.pdf
project_link: https://etach-qs.github.io/GenHOI\_project/
code_link: null
aliases:
- GenHOI
tags:
- arxiv_2025
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
core_operator: 通过空间-时间解耦的两阶段框架：第一阶段利用大规模3D HOI数据集学习空间交互模式（Object-AnchorNet恢复3D关键帧），第二阶段使用接触感知扩散模型（ContactDM）将稀疏关键帧插值为时序连贯的4D序列，并显式融入精细的接触几何特征。
primary_logic: 精细的接触区域信息对于4D HOI生成至关重要；通过点云编码器（Contact-Aware Encoder）提取人-物接触特征，并利用交叉注意力机制（Contact-Aware HOI Attention）动态注入扩散模型，能极大提升生成运动的真实感和交互精度。
claims:
- 在已见物体（OMOMO）上，完整GenHOI的FID为0.41，远优于不含接触感知模块的变体（FID 0.76）
- 在未见物体（OMOMO）上，GenHOI的交互F1分数C_F1达到0.66，接触准确率C_prec为0.79，超过其他方法
- 接触感知编码器中的KNN采样策略对性能至关重要，均匀采样会导致模型收敛失败（C_F1从0.77降至0.20）
- 用户研究表明GenHOI生成的交互运动在自然度和真实性上被持续偏好于现有方法
---

# GenHOI: Generalizing Text-driven 4D Human-Object Interaction Synthesis for Unseen Objects

> [!tip] 核心洞察
> 精细的接触区域信息对于4D HOI生成至关重要；通过点云编码器（Contact-Aware Encoder）提取人-物接触特征，并利用交叉注意力机制（Contact-Aware HOI Attention）动态注入扩散模型，能极大提升生成运动的真实感和交互精度。

| 字段 | 内容 |
|------|------|
| 中文题名 | GenHOI：面向未见物体的文本驱动4D人-物交互合成泛化 |
| 英文题名 | GenHOI: Generalizing Text-driven 4D Human-Object Interaction Synthesis for Unseen Objects |
| 会议/期刊 | arXiv 2025 |
| Links | [Project](https://etach-qs.github.io/GenHOI\_project/) · [paper](https://arxiv.org/abs/2506.15483) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction |
| Method | GenHOI |
| Dataset | OMOMO |

> [!tip] 效果简介
> - OMOMO (seen objects) 上，FID 0.41 (GenHOI Full) vs 0.76 (GenHOI w/o CA) (-0.35 (lower is better))。
> - OMOMO (unseen objects) 上，C_F1 0.66 (GenHOI Full) vs best of compared methods (improvement over all baselines)。
> - OMOMO (ablation: conditioning strategy) 上，C_F1 0.77 (KNN + Cross-Attention) vs 0.20 (Uniform + Cross-Attention) (+0.57)。

## 概要

### 问题瓶颈

文本驱动的4D人-物交互（HOI）合成旨在根据自然语言描述，生成人体与物体在三维空间中连贯运动的完整序列。现有方法面临一个核心瓶颈：**4D HOI数据集的规模极为有限，且交互类别单一**。以OMOMO数据集为代表的现有基准仅包含少量物体和交互类型，导致模型难以学习到可迁移的交互先验，在面对训练中未出现的新物体时，生成的运动序列往往缺乏物理真实感和交互精度。这一数据稀缺性构成了制约该领域泛化能力的关键障碍。

### 核心方案

GenHOI提出了一种**空间-时间解耦的两阶段框架**，通过将4D HOI合成分解为两个可控子任务，从根本上降低对大规模4D配对数据的依赖：

- **第一阶段（空间交互建模）**：Object-AnchorNet在由Grab、Behave和Open3DHOI组成的大规模3D HOI数据集上训练，学习从人体点云和物体几何中恢复稀疏的3D HOI关键帧。这些关键帧捕获了人与物体在空间维度上的精确交互关系。
- **第二阶段（时序运动生成）**：Contact-Aware Diffusion Model（ContactDM）以第一阶段的关键帧为锚点，结合文本条件和接触几何特征，将稀疏关键帧插值为稠密的4D HOI序列，同时生成左右手的接触标签。

该方法的核心洞察在于：**精细的接触区域信息对4D HOI生成的质量至关重要**。GenHOI通过基于PointNet++的接触感知编码器（Contact-Aware Encoder）提取人-物接触特征，并利用交叉注意力机制（Contact-Aware HOI Attention）将这些特征动态注入扩散模型的潜变量中，实现了语义和时序上精确的条件化。

### 方法谱系与知识库定位

GenHOI定位于文本驱动的4D HOI生成领域，与以下代表性工作形成对比：

| 方法 | 核心策略 | 局限性 |
|------|----------|--------|
| **InterDiff** (Xu et al., ICCV 2023) | 基于过去帧预测4D HOI序列 | 依赖历史帧，缺乏对未见物体的泛化机制 |
| **MDM** (Tevet et al., ICLR 2023) | 纯人体运动扩散模型，可扩展至HOI | 未显式建模人-物交互的空间约束 |
| **HOI-Diff** (Peng et al., arXiv 2023) | 集成可供性感知模块的文本驱动HOI生成 | 对未见物体的接触精度有限 |
| **OMOMO** (Li et al., TOG 2023) | 条件于预定义物体轨迹的HOI合成 | 需要物体轨迹作为输入，非文本驱动 |
| **CHOIS** (Li et al., ECCV 2024) | 给定初始姿态和物体路径点的4D HOI生成 | 依赖路径点输入，泛化场景受限 |
| **GenHOI** (本文) | 两阶段解耦 + 接触感知扩散模型 | 面向未见物体的文本驱动泛化 |

GenHOI的差异化优势在于：通过第一阶段在3D HOI数据上学习可迁移的空间交互先验，第二阶段利用接触感知注意力机制精细注入几何信息，实现了从文本到4D运动序列的端到端泛化，而无需预定义的物体轨迹或路径点。

### 关键结论

在OMOMO数据集上的实验表明：

- **已见物体**：完整GenHOI的FID达到0.41，显著优于去除接触感知模块的变体（FID 0.76），验证了接触感知设计的核心贡献（Table 1）。
- **未见物体**：GenHOI的交互F1分数（C_F1）达到0.66，接触准确率（C_prec）达到0.79，在所有对比方法中表现最优（Table 2）。
- **消融实验**：KNN采样策略对接触感知编码器至关重要——均匀采样导致模型收敛失败，C_F1从0.77骤降至0.20（Table 5）；关键帧数量K=5在捕捉交互动态与预测误差之间达到最佳平衡（Table 4）。

用户感知研究进一步表明，GenHOI生成的交互运动在自然度和真实性上被持续偏好于现有方法。这些结果共同证实：**通过空间-时间解耦和接触感知条件化，GenHOI有效突破了4D HOI生成中的数据稀缺瓶颈，实现了对未见物体的泛化能力**。

### 问题背景

生成真实的人-物交互（Human-Object Interaction, HOI）运动是计算机视觉和图形学中的核心挑战，其应用涵盖虚拟现实、具身智能和动画制作。随着扩散模型在人体运动生成领域的成功，研究者开始探索**文本驱动的4D HOI合成**——即根据自然语言描述，同时生成人体运动序列和物体运动轨迹。然而，这一任务面临两大根本性瓶颈：

1. **数据稀缺与交互多样性不足**：现有4D HOI数据集（如OMOMO）规模有限，且仅覆盖少量交互类别。模型在训练中见到的物体和交互模式极为有限，导致其难以泛化到**未见物体**——即训练集中未出现的新物体几何形态。

2. **空间-时间耦合建模的困难**：直接端到端地生成完整的4D HOI序列需要同时建模精细的空间接触关系和长程时序连贯性，这在数据受限的条件下极易导致生成质量退化。

### 现有方法缺口

当前主流的4D HOI生成方法存在以下关键局限：

- **依赖预定义条件**：**OMOMO**（Li et al., TOG 2023）需要预定义的物体运动轨迹作为输入，无法从文本直接生成。**CHOIS**（Li et al., ECCV 2024）则要求给定初始人体姿态和物体路径点，限制了其开放场景下的适用性。

- **泛化能力不足**：**InterDiff**（Xu et al., ICCV 2023）基于过去帧预测未来HOI序列，但其训练完全依赖4D HOI数据，难以泛化至新物体。**MDM**（Tevet et al., ICLR 2023）和**HOI-Diff**（Peng et al., arXiv 2023）虽然支持文本条件，但同样受限于4D数据的规模和多样性。

- **忽视接触几何细节**：现有方法通常将物体表示为全局姿态参数或粗略的几何特征，缺乏对**精细接触区域**的显式建模。然而，人-物交互的真实感高度依赖于手部与物体表面之间的精确空间关系——这正是现有方法生成质量不足的根本原因之一。

### 核心动机

针对上述瓶颈，GenHOI的核心动机在于通过**空间-时间解耦**和**接触感知建模**两个关键设计，突破4D HOI生成的数据依赖和泛化困境：

- **空间-时间解耦**：将4D HOI合成分解为两个可管理的子任务——先恢复稀疏的3D HOI关键帧（空间关系），再将其插值为密集的4D序列（时序连贯性）。这一解耦使得第一阶段可以充分利用**大规模3D HOI数据集**（Grab, Behave, Open3DHOI）学习丰富的空间交互模式，从而大幅降低对4D数据的依赖。

- **接触感知条件化**：引入专用的**接触感知编码器**和**交叉注意力融合机制**，从3D HOI关键帧点云中提取精细的接触几何特征，并将其动态注入扩散模型的生成过程。这一设计的核心洞察在于：**精细的接触区域信息是生成真实人-物交互的关键**，而简单的特征拼接或加法嵌入无法有效传递这一信息。

## 核心方法与创新机理

GenHOI的核心创新在于通过**空间-时间解耦的两阶段框架**，将4D人-物交互生成分解为两个可管理的子任务，从而降低对大规模4D HOI数据集的依赖，并实现对未见物体的泛化。

### 关键创新点

**1. 空间-时间解耦的两阶段管线**

现有方法（如**InterDiff**（Xu et al., ICCV 2023）、**MDM**（Tevet et al., ICLR 2023））通常从文本或条件端到端生成完整序列，或依赖预定义物体轨迹（如**CHOIS**（Li et al., ECCV 2024））。GenHOI则首次将空间建模与时间建模显式分离：

- **第一阶段（空间交互恢复）**：引入**Object-AnchorNet**，在大规模3D HOI数据集（Grab、Behave、Open3DHOI）上学习人-物空间交互模式，从人体点云和物体几何中恢复稀疏的3D HOI关键帧。这一步解决了4D数据稀缺导致的泛化瓶颈——3D HOI数据集规模远大于4D数据集，为模型提供了丰富的空间交互先验。

- **第二阶段（时序插值）**：使用**Contact-Aware Diffusion Model（ContactDM）**，将稀疏关键帧插值为时序连贯的4D序列。扩散模型以投影的物体特征、文本嵌入和接触特征为条件，同时生成人体运动、物体运动及接触标签。

**2. 接触感知编码器（Contact-Aware Encoder）**

Baseline扩散模型通常缺乏对精细接触几何的建模能力。GenHOI提出基于PointNet++的接触感知编码器，对3D HOI关键帧点云进行高效采样和编码，提取精细的人-物接触特征。具体而言：

- 将人体和物体点云拼接，并通过one-hot指示符区分来源（见公式2-3）；
- 采用多尺度分组策略将点云编码为每帧特征向量 $F_i \in \mathbb{R}^d$（公式4）。

消融实验表明，该模块对性能至关重要：去除接触感知编码器和注意力模块后，FID从0.41恶化至0.76（Table 1），交互质量显著下降。

**3. 接触感知交叉注意力（Contact-Aware HOI Attention）**

不同于baseline常用的加法嵌入或简单特征拼接，GenHOI通过交叉注意力机制将接触感知特征动态注入扩散模型的潜变量：

$$ \pmb{F}_{\mathrm{fused}} = \mathrm{Softmax}\left(\frac{Q K^T}{\sqrt{d}}\right) V $$

其中姿态嵌入作为查询（$Q$），接触感知特征作为键（$K$）和值（$V$），实现时序和语义上精确的条件化。消融实验证实，交叉注意力条件化优于加法嵌入融合（Table 5：KNN + Cross-Attention的C_F1=0.77，而Uniform + Cross-Attention仅为0.20）。

**4. 接触区域感知的采样策略**

在接触感知编码器中，KNN采样策略对性能至关重要。实验表明，若将KNN采样替换为均匀采样，模型几乎无法收敛（C_F1从0.77骤降至0.20，Table 5）。这一发现揭示了精细接触区域信息对于4D HOI生成的核心作用——只有聚焦于接触区域的点云特征，才能为扩散模型提供有效的空间约束。

**5. 训练数据利用策略的创新**

GenHOI的两阶段设计本质上是一种数据效率策略：第一阶段在大型3D HOI数据集上训练空间关系，第二阶段仅在4D HOI数据集上训练时序插值。这显著降低了对昂贵4D数据的依赖，同时借助3D数据的丰富性提升了泛化能力——在未见物体上，GenHOI的交互F1分数（C_F1=0.66）和接触准确率（C_prec=0.79）均超过所有baseline方法（Table 2）。

### 创新总结

GenHOI的核心贡献在于识别出**精细接触几何信息是4D HOI生成的关键瓶颈**，并围绕这一洞察设计了完整的解耦框架：通过Object-AnchorNet利用3D数据学习空间交互、通过接触感知编码器提取接触特征、通过交叉注意力实现动态条件注入。这三个changed slots相互协同，使得模型能够为训练中未见过的物体生成真实、物理合理的人-物交互序列。

GenHOI 将文本驱动的 4D 人-物交互（HOI）合成分解为空间建模与时序建模两个解耦阶段，以降低对大规模 4D HOI 数据集的依赖。整体流程如 Figure 2 所示：

![[assets/figures/papers/paper_list_l1681_GenHOI_Generalizing_Text_driven_4D_Human_Object_Interaction_Synthesis_fo/figures/002_Figure_2.jpg]]
*Figure 2: GenHOI Overview. In Stage 1, the method recovers keyframe HOI using object geometry and human pose priors. In Stage 2, the Contact-Aware Diffusion Model (ContactDM) synthesizes the 4D HOI sequence leveraging the keyframe HOI and the encoded contact embeddings. After training, the model can generalize to unseen objects given the object geometry and the associated text prompt*

**第一阶段：3D HOI 关键帧恢复（Object-AnchorNet）**
- 输入：人体点云、物体模板点云、文本描述
- 输出：稀疏的 3D HOI 关键帧（物体姿态点云），捕获人与物体之间精确的空间关系
- 训练数据：大规模 3D HOI 数据集（Grab、Behave、Open3DHOI），充分利用丰富的空间交互标注

**第二阶段：4D HOI 序列合成（Contact-Aware Diffusion Model, ContactDM）**
- 输入：第一阶段恢复的 3D HOI 关键帧、物体几何特征、文本嵌入
- 核心模块：
  - **Contact-Aware Encoder**：基于 PointNet++ 的点云编码器，对 3D HOI 关键帧点云进行多尺度分组采样与编码，提取精细的人-物接触特征
  - **Contact-Aware HOI Attention**：通过交叉注意力机制将接触感知特征动态注入扩散模型的潜变量，实现时序与语义上精确的条件化
- 输出：时序连贯的 4D HOI 序列（人体运动 $\pmb{x}^{h}$ 与物体运动 $\pmb{x}^{o}$）及双手接触标签

**关键设计逻辑**

两阶段解耦的核心洞察在于：空间交互模式（如抓取姿态、接触区域）可以从丰富的 3D HOI 数据中充分学习，而时序动态（如运动过渡、速度变化）则由第二阶段扩散模型在 4D 数据上精细建模。这种分解使模型在仅见过少量 4D 交互类别的情况下，仍能泛化到未见物体的交互生成。

接触感知模块是第二阶段性能的关键瓶颈。消融实验表明，去除 Contact-Aware Encoder 和 Contact-Aware HOI Attention（w/o CA）后，模型退化为仅条件于物体几何和文本的扩散模型，在已见物体上的 FID 从 0.41 恶化至 0.76，交互质量显著下降。进一步地，接触感知编码器中的 KNN 采样策略对模型收敛至关重要：均匀采样替代 KNN 采样时，C_F1 从 0.77 骤降至 0.20，模型几乎无法学习有效的接触特征。

**输入输出流总结**

```
文本描述 + 物体几何
        ↓
[Stage 1] Object-AnchorNet → 3D HOI 关键帧
        ↓
[Stage 2] Contact-Aware Encoder → 接触特征 F_i
        ↓
Contact-Aware HOI Attention → 融合特征 F_fused
        ↓
ContactDM（扩散去噪）→ 4D HOI 序列 + 接触标签
```

该框架的模块化设计使得各组件可独立训练与验证：Object-AnchorNet 在 3D 数据上预训练后固定，ContactDM 在 4D 数据上训练时直接使用其输出的关键帧作为条件，避免端到端优化对 4D 数据规模的苛刻要求。

GenHOI 将文本驱动的 4D HOI 生成解耦为两个阶段：**空间交互关键帧恢复**与**时序运动插值**。其核心模块包括 Object-AnchorNet、Contact-Aware Encoder 和 Contact-Aware HOI Attention，三者协同实现从稀疏关键帧到密集交互序列的生成。

### 4D HOI 表示

人体与物体的运动采用统一表示。人体运动 $\pmb{x}^{h}$ 由全局关节位置 $\pmb{j}$ 和局部 6D 旋转 $\pmb{q}$ 组成；物体运动 $\pmb{x}^{o}$ 由全局 3D 位置 $\pmb{o}$ 和旋转 $\pmb{r}$ 组成：

$$\pmb{x}^{h} = [j, \pmb{q}], \quad \pmb{x}^{o} = [\pmb{o}, \pmb{r}] \tag{1}$$

### 第一阶段：Object-AnchorNet

Object-AnchorNet 负责从人体点云和物体几何中恢复稀疏的 3D HOI 关键帧。该网络在大规模 3D HOI 数据集（Grab、Behave、Open3DHOI）上训练，学习人-物空间交互模式，从而在给定人体点云与物体模板点云时预测物体姿态点云。这一阶段的关键作用是降低对稀缺 4D HOI 数据的依赖——空间关系可从丰富的 3D 静态交互数据中习得。

### 第二阶段：ContactDM 与接触感知模块

Contact-Aware Diffusion Model (ContactDM) 以 3D HOI 关键帧、物体几何 $\pmb{G}$ 和文本提示 $\pmb{c}$ 为条件，生成时序连贯的 4D HOI 序列 $(\pmb{x}^{h}, \pmb{x}^{o})$ 及左右手接触标签 $\pmb{H} \in \mathbb{R}^{N \times 2}$。其核心创新在于显式建模接触几何信息。

**Contact-Aware Encoder** 基于 PointNet++ 架构，对每帧关键帧的人-物点云进行编码。为区分人体与物体点，首先添加 one-hot 指示符：

$$\tilde{\pmb{V}}_i^h = \mathrm{concat}(\hat{\pmb{V}}_i^h, \mathbf{1}_{M_h}) \in \mathbb{R}^{M_h \times 4}, \quad \tilde{\pmb{V}}_i^o = \mathrm{concat}(\hat{\pmb{V}}_i^o, \mathbf{0}_{M_o}) \in \mathbb{R}^{M_o \times 4} \tag{2}$$

将带标识的人体和物体点云拼接为统一输入：

$$\tilde{\pmb{V}}_i = \mathrm{concat}(\tilde{\pmb{V}}_i^h, \tilde{\pmb{V}}_i^o) \in \mathbb{R}^{(M_h + M_o) \times 4} \tag{3}$$

随后通过多尺度分组策略编码为每帧特征向量：

$$\pmb{F}_i = \mathrm{PointEncoder}(\tilde{V}_i) \in \mathbb{R}^d \tag{4}$$

**Contact-Aware HOI Attention** 通过交叉注意力机制将接触感知特征动态注入扩散模型的潜变量。以姿态嵌入作为查询 $\pmb{Q}$，接触感知特征作为键 $\pmb{K}$ 和值 $\pmb{V}$，实现时序与语义上精确的条件化：

$$\pmb{F}_{\mathrm{fused}} = \mathrm{Softmax}\left(\frac{Q K^T}{\sqrt{d}}\right) V \tag{5}$$

### 关键设计决策

消融实验揭示了两个决定性设计选择：

- **KNN 采样策略**：Contact-Aware Encoder 中对人体点云采用 KNN 采样而非均匀采样。均匀采样导致模型无法收敛（C_F1 从 0.77 降至 0.20），表明接触区域的精细几何信息对交互生成至关重要。
- **交叉注意力 vs. 加法嵌入**：交叉注意力条件化显著优于加法嵌入融合。加法嵌入的全局特征嵌入 $\check{F} = \frac{1}{T} \sum_{i=1}^{T} F_i$ 丢失了时序特异性，而交叉注意力保留了帧级接触信息的动态注入能力。

![[assets/figures/papers/paper_list_l1681_GenHOI_Generalizing_Text_driven_4D_Human_Object_Interaction_Synthesis_fo/figures/014_Table_6.jpg]]
*Table 6: Object-AnchorNet Architecture*

## 实验与关键发现

### 主实验结果

GenHOI 在已见与未见物体场景下均取得最优性能，验证了空间-时间解耦框架与接触感知模块的有效性。

**已见物体（OMOMO）**。如 Table 1 所示，完整 GenHOI 在已见物体上达到 FID 0.41、C_F1 0.77、MPJPE 10.64 cm，显著优于去除接触感知模块的变体 GenHOI w/o CA（FID 0.76）。这一差距表明，精细的接触区域信息对生成真实的人-物交互运动至关重要——仅依赖物体几何和文本条件的扩散模型无法捕捉手-物接触的细微空间关系。

**未见物体（OMOMO）**。在更具挑战性的泛化场景下，GenHOI 在未见物体上达到 C_prec 0.79、C_F1 0.66（Table 2），超越所有对比方法，包括 **InterDiff**（Xu et al., ICCV 2023）、**MDM**（Tevet et al., ICLR 2023）、**HOI-Diff**（Peng et al., arXiv 2023）、**OMOMO**（Li et al., TOG 2023）和 **CHOIS**（Li et al., ECCV 2024）。GenHOI 的核心优势在于：第一阶段 Object-AnchorNet 从大规模 3D HOI 数据集（Grab、Behave、Open3DHOI）习得的空间交互先验可迁移至未见物体；第二阶段 ContactDM 通过接触感知编码器提取的精细几何特征进一步保证了交互精度。

**未见物体（3D-FUTURE）**。在 3D-FUTURE 未见物体上，GenHOI 同样保持领先，C% 达到 0.58，MPJPE 为 10.82 cm（Table 3）。值得注意的是，OMOMO* 方法需要将 3D-FUTURE 物体集成到 OMOMO 测试集运动中生成评估条件，而 GenHOI 直接从物体几何和文本生成交互，展现了更强的泛化能力。

**用户感知研究**。Figure 5 的用户研究表明，参与者在运动自然度和真实感上持续偏好 GenHOI 生成的交互序列，进一步佐证了定量指标的优势。

### 消融实验

**接触感知模块的贡献**。去除接触感知编码器和接触感知 HOI 注意力（GenHOI w/o CA）后，模型退化为仅以物体几何和文本为条件的扩散模型，FID 从 0.41 升至 0.76（Table 1），交互质量显著下降。这证实了接触几何信息是 4D HOI 生成的关键瓶颈——缺乏显式接触建模时，扩散模型难以推断手部与物体表面的精确空间关系。

**关键帧数量 K**。Table 4 显示，K=5 在捕捉交互动态与预测误差之间达到最佳平衡（C_F1=0.77，MPJPE=10.64 cm）。K=3 时关键帧过于稀疏，无法充分约束时序插值；K=7 时预测误差累积导致性能下降。这一结果验证了稀疏关键帧恢复策略的有效性：仅需少量空间准确的 3D HOI 关键帧即可指导扩散模型生成连贯的 4D 序列。

**接触感知编码器中的采样策略**。Table 5 揭示了 KNN 采样对接触感知编码的决定性作用：将 KNN 替换为均匀采样后，C_F1 从 0.77 骤降至 0.20，模型几乎无法收敛。这是因为接触区域仅占人体点云的一小部分，均匀采样会淹没关键的接触几何信息；KNN 采样能够聚焦于手部附近的局部区域，提取有判别力的接触特征。

**条件化策略**。交叉注意力融合（Cross-Attention）优于加法嵌入融合（Additive Embedding），前者通过动态对齐姿态嵌入（Q）与接触感知特征（K, V）实现更精准的特征注入。加法嵌入使用全局平均特征 $\check{F} = \frac{1}{T} \sum_{i=1}^{T} F_i$，丢失了时序维度的细粒度接触信息，导致交互精度下降。

### 公平性说明

为保证公平比较，实验采取了以下措施：将 InterDiff 修改为支持文本条件输入；将 MDM 扩展至 HOI 数据并采用统一的物体几何表示；所有方法在 OMOMO 未见物体划分上使用相同的训练/测试分割；用户研究采用双盲方式，参与者对方法来源不知情。

![[assets/figures/papers/paper_list_l1681_GenHOI_Generalizing_Text_driven_4D_Human_Object_Interaction_Synthesis_fo/figures/003_Table_1.jpg]]
*Table 1: Interation synthesis on the seen objects. OMOMO-GT utilizes ground truth object motion as input for OMOMO*

![[assets/figures/papers/paper_list_l1681_GenHOI_Generalizing_Text_driven_4D_Human_Object_Interaction_Synthesis_fo/figures/012_Table_4.jpg]]
*Table 4: Comparison of interaction quality for different number of keyframes on OMOMO dataset*

![[assets/figures/papers/paper_list_l1681_GenHOI_Generalizing_Text_driven_4D_Human_Object_Interaction_Synthesis_fo/figures/013_Table_5.jpg]]
*Table 5: Comparison of Conditioning Strategies for 4D HOI Generation on OMOMO dataset*

![[assets/figures/papers/paper_list_l1681_GenHOI_Generalizing_Text_driven_4D_Human_Object_Interaction_Synthesis_fo/figures/006_Figure_3.jpg]]
*Figure 3: Examples of synthetic motions for qualitative evaluation*

## 定位与知识库关联

**GenHOI** 的核心贡献在于将4D人-物交互（HOI）生成从“端到端黑箱”或“依赖预定义物体轨迹”的范式，重构为**空间-时间解耦的两阶段框架**，从而显著降低了对大规模4D HOI数据的依赖，并实现了对未见物体的泛化。其方法定位可从以下维度理解：

---

### 与现有方法的谱系关系

**1. 相对于纯人体运动生成方法的扩展**

早期的扩散运动模型如 **MDM**（Tevet et al., ICLR 2023）仅对人体运动建模。GenHOI将此类框架扩展至HOI域，但并非简单地将物体表示拼接进扩散模型——消融实验表明，直接去除接触感知模块（GenHOI w/o CA）退化为仅条件于物体几何和文本的扩散模型，在OMOMO已见物体上FID从0.41恶化至0.76（Table 1），证明单纯的表示扩展远不足以生成真实的交互。

**2. 相对于条件化HOI生成方法的改进**

- **OMOMO**（Li et al., TOG 2023）和 **CHOIS**（Li et al., ECCV 2024）均需要预定义的物体运动轨迹或路径点作为输入条件，本质上将HOI生成简化为“给定物体运动后的人体运动补全”。GenHOI则通过Object-AnchorNet从物体几何和文本直接恢复3D HOI关键帧，无需任何物体运动先验，从根本上拓展了应用边界。
- **HOI-Diff**（Peng et al., arXiv 2023）集成了可供性感知模块，但未显式建模精细的接触几何。GenHOI的Contact-Aware Encoder使用基于PointNet++的多尺度分组策略，并通过KNN采样聚焦人手附近的物体点云区域，这是其接触准确率C_prec达到0.79（Table 2）的关键——消融实验证实，将KNN替换为均匀采样会导致C_F1从0.77骤降至0.20，模型无法收敛（Table 5）。

**3. 相对于预测式方法的优势**

**InterDiff**（Xu et al., ICCV 2023）基于过去帧预测未来HOI序列，属于自回归预测范式。GenHOI采用扩散生成范式，在已见物体上FID达到0.41（Table 1），且用户研究表明其生成的运动在自然度和真实感上被持续偏好（Figure 5）。

---

### 知识库定位：核心机制创新

GenHOI的知识增量集中于两个相互协同的设计：

| 机制 | 解决的问题 | 关键实现 | 证据强度 |
|------|-----------|---------|---------|
| **Object-AnchorNet** | 4D HOI数据稀缺导致空间交互模式学习不足 | 在Grab、Behave、Open3DHOI等大规模3D HOI数据集上预训练，学习从人体点云和物体几何恢复3D关键帧 | Table 2：未见物体C_F1=0.66，优于所有baseline |
| **Contact-Aware Attention** | 精细接触信息在生成过程中被稀释 | 通过交叉注意力（Eq. 5）将接触感知特征以K、V形式动态注入扩散模型潜变量，而非简单的加法嵌入 | Table 5：交叉注意力C_F1=0.77 vs 加法嵌入C_F1=0.65 |

其中，接触感知编码器的**KNN采样策略**是决定性的实现细节：它确保模型聚焦于人手-物体接触区域的局部几何，而非全局均匀点云。这一发现具有方法论意义——在HOI生成中，“在哪里采样”比“如何编码”更为关键。

---

### 适用边界与局限

基于现有分析，GenHOI的适用边界和潜在局限包括：

1. **物体形态的泛化边界**：Object-AnchorNet在3D-FUTURE的未见物体上取得了C_F1=0.58（Table 3），但这些物体在几何复杂度上与训练集中的刚性物体（如椅子、桌子）相似。对于可变形物体或不规则形状物体，模型的泛化能力尚未被验证，需要手动核实。

2. **两阶段解耦的时序代价**：关键帧数量K=5在捕捉交互动态和预测误差之间达到最优平衡（Table 4），但该解耦策略对长时间序列的时序连贯性可能存在理论局限——当交互动作跨越多个语义阶段时，固定的关键帧数量可能不足以捕捉完整的动态变化。

3. **计算开销**：交叉注意力机制相较于加法嵌入带来了显著性能提升（C_F1: 0.77 vs 0.65），但其额外的计算开销在分析中未被量化，需要参考原文补充材料进行验证。

4. **多物体场景**：当前框架聚焦于单人与单物体的交互，扩展到多物体交互或杂乱场景的能力仍是开放问题。

---

### 开放问题

分析中明确识别但未被现有实验覆盖的问题包括：

- 模型对与训练物体尺度、形状差异极大的新物体的泛化能力如何？
- 交叉注意力机制相较于加法嵌入的具体计算开销是多少？
- 框架能否扩展到多物体交互或杂乱场景？
- 两阶段解耦对长时间序列的时序连贯性是否存在根本性局限？

这些问题构成了该方向的后续研究空间。

## 原文 PDF

![[paperPDFs/arxiv_2025/GenHOI_Generalizing_Text_driven_4D_Human_Object_Interaction_Synthesis_for_Unseen_Objects.pdf]]
