---
title: "PartSAM: A Scalable Promptable Part Segmentation Model Trained on Native 3D Data"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/PartSAM_A_Scalable_Promptable_Part_Segmentation_Model_Trained_on_Native_3D_Data.pdf
openreview_forum_id: y8sZUQPYXC
aliases:
- PartSAM
tags:
- ICLR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
core_operator: "将大规模原生3D零件标注（通过模型在环管道获取）与一个类似SAM的提示引导编码器-解码器架构相结合，使得模型能够直接学习三维几何与零件语义，从而实现灵活的交互式或自动分割。双分支编码器的设计进一步保留了从SAM蒸馏的2D先验。"
primary_logic: "直接在大规模原生3D零件对上训练一个可提示的分割模型，可以同时实现开放世界泛化、交互可控性和内部几何结构的理解，从而摆脱对2D提升的依赖。"
claims:
- "PartSAM在PartObjaverse-Tiny的交互式分割任务中，单次提示（IoU@1）相比于Point-SAM相对提升91%。"
- "PartSAM在PartObjaverse-Tiny和PartNetE的自动分割任务中，比第二好的方法分别提高超过20%的IoU。"
- "双分支编码器中的可学习分支适应原生3D零件，而冻结分支保留SAM的2D先验；消融实验表明去除任何一支都会显著降低性能。"
- "模型在环标注管道将训练数据从18万扩展到50万个形状、超过500万个零件对，显著提升了分割性能。"
---

# PartSAM: A Scalable Promptable Part Segmentation Model Trained on Native 3D Data

> [!tip] 核心洞察
> 直接在大规模原生3D零件对上训练一个可提示的分割模型，可以同时实现开放世界泛化、交互可控性和内部几何结构的理解，从而摆脱对2D提升的依赖。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | PartSAM：基于原生3D数据训练的可扩展可提示3D零件分割模型 |
| 英文题名 | PartSAM: A Scalable Promptable Part Segmentation Model Trained on Native 3D Data |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=y8sZUQPYXC) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction |
| Method | PartSAM |
| Dataset | PartObjaverse-Tiny (interactive), PartNetE (interactive), PartObjaverse-Tiny (automatic) |

> [!tip] 效果简介
> - PartObjaverse-Tiny (interactive) 上，IoU@1 为 56.1，对比 29.4 (Point-SAM)，变化 +91% relative。
> - PartObjaverse-Tiny (interactive) 上，IoU@10 为 87.6，对比 73.9 (Point-SAM)，变化 +18.5% relative。
> - PartNetE (interactive) 上，IoU@1 为 59.5，对比 35.9 (Point-SAM)，变化 +65.7% relative。

## 概述

### 1. 问题背景与瓶颈

3D 形状的零件分割是三维理解的基础任务，支撑着机器人操作、3D 编辑与建模等下游应用。现有方法主要分为两类：一类依赖 2D 基础模型（如 SAM）通过多视图提升间接获得 3D 分割，这种范式无法捕捉物体的内在几何结构，导致仅能理解可见表面、分解不可控，且开放世界泛化能力有限；另一类基于特征聚类（如 PartField），虽直接处理 3D 数据，但缺乏灵活的交互机制和可扩展的训练范式，同样难以处理内部结构和遮挡零件。更深层的瓶颈在于，大规模原生 3D 零件标注数据的缺失，以及缺乏能够有效利用此类数据的可扩展 3D 架构，使得模型在实际场景中的表现严重受限。

### 2. 核心方法与因果机制

PartSAM 的核心思路是**因果旋钮式设计**：将大规模原生 3D 零件标注与类似 SAM 的提示引导编码器-解码器架构相结合，使模型直接学习三维几何与零件语义之间的映射。具体而言：

- **双分支三平面编码器**：可学习分支适应原生 3D 零件数据，冻结分支保留从 SAM 蒸馏的 2D 先验，二者协同构建连续的特征场，使模型同时具备几何结构理解能力和跨模态先验。
- **提示引导的掩码解码器**：支持正/负点击提示，通过双向 Transformer 交叉注意力生成多个候选掩码，并由 IoU 头预测质量以自动选择最佳掩码，实现灵活的交互式或全自动分割。
- **模型在环标注管道**：通过 IoU 阈值过滤规则，从大规模 3D 资产中挖掘高质量零件监督，将训练数据从 18 万扩展到 50 万个形状、超过 500 万个零件对，显著提升分割性能。

这一设计的核心洞察在于：**直接在大规模原生 3D 零件对上训练可提示的分割模型，可以同时实现开放世界泛化、交互可控性和内部几何结构的理解，从而摆脱对 2D 提升的依赖**。

### 3. 方法谱系与知识库定位

PartSAM 在 3D 零件分割领域的方法谱系中占据独特位置：

| 维度 | 特征聚类方法 | 2D 提升方法 | PartSAM |
|------|-------------|------------|---------|
| **代表工作** | PartField (Liu et al., 2025) | SAMesh, SAMPart3D, Point-SAM | 本文 |
| **分割范式** | K-Means / 图割聚类 | 基于 SAM 的多视图掩码提升 | 提示引导的掩码解码器 |
| **数据来源** | 原生 3D 标注 (PartNet 等) | 2D SAM 掩码 + 提升 | 大规模原生 3D 标注 (模型在环) |
| **交互能力** | 需指定聚类数目 | 有限或无交互 | 正/负点击提示，迭代式标注 |
| **编码器架构** | 单一三平面分支 | 依赖 2D 编码器 | 双分支三平面 (可学习 + 冻结) |
| **内部结构理解** | 部分支持 | 仅表面 | 完整支持 |
| **开放世界泛化** | 受限于训练类别 | 依赖 SAM 泛化 | 原生 3D 泛化 |

PartSAM 继承了 SAM 的提示驱动分割哲学，但在 3D 原生领域进行了根本性重构：用三平面特征场替代 2D 图像编码器，用双分支设计保留跨模态先验，用模型在环管道解决 3D 标注稀缺问题。相比于 PartField 的特征聚类范式，PartSAM 将分割从“后处理聚类”转变为“端到端可提示解码”，实现了更灵活的人机交互和更精确的掩码生成。

### 4. 主要结果与证据强度

PartSAM 在多个基准和任务上取得了显著提升：

- **交互式分割**：在 PartObjaverse-Tiny 上，单次提示（IoU@1）达到 56.1，相比 Point-SAM 的 29.4 相对提升 **91%**；在 PartNetE 上，IoU@1 达到 59.5，相对提升 **65.7%**（Table 1，置信度 0.98）。
- **自动分割**：在 PartObjaverse-Tiny 上 mIoU 达到 69.5，比第二好的方法（SAMesh, 56.9）提高 **22.1%**；在 PartNetE 上 mIoU 达到 72.4，比 PartField*（59.1）提高 **22.5%**（Table 2，置信度 0.98）。
- **消融实验**：移除预训练权重导致 IoU@1 从 56.1 降至 48.3；仅使用冻结分支降至 42.5；移除模型在环标注数据降至 49.0（Table 3，置信度 0.99）。
- **数据扩展**：模型在环管道将训练数据从 18 万扩展到 50 万形状，性能随数据规模持续提升（Figure 11，置信度 0.95）。
- **内部结构分割**：PartSAM 能够分割 AI 生成网格中的内部和遮挡结构，而基于 2D 提升的方法（如 SAMesh）无法可靠恢复这些部分（Figure 9，置信度 0.95）。

### 5. 局限与开放问题

PartSAM 目前仅输出类别无关的零件掩码，无法直接生成语义标签，限制了下游任务中的直接使用。对于训练数据中极少出现的结构（如雕刻字母），模型存在长尾分布问题；在对象缺乏清晰语义结构（如珊瑚雕塑）时，分割结果可能无意义。处理 AI 生成网格或粗糙真实扫描时，几何不规则和细节错误可能放大边界歧义。此外，性能仍受限于现有 3D 数据集的多样性——相较于 2D 数据集（如 SA-1B），3D 数据集的覆盖范围较小。

开放问题包括：如何为 3D 形状及其零件生成大规模语义标签数据集，使 PartSAM 具备语义感知能力；如何改进模型以更好地处理罕见或细微结构；以及如何进一步提升在几何不规则输入上的鲁棒性。

## 背景与动机

3D 形状的零件分割是三维视觉中的基础任务，旨在将三维模型分解为语义上有意义的组成部分。这一能力对机器人操作、3D 编辑、形状分析与重建等下游应用至关重要。然而，现有方法面临一个根本性瓶颈：**对 2D 基础模型的过度依赖导致无法捕捉三维几何的内在结构**。

当前主流的零件分割范式严重依赖 Segment Anything Model (SAM) 等 2D 基础模型，通过多视图投影将 2D 掩码“提升”到 3D 空间。这种间接策略存在三个根本缺陷：

1. **仅表面理解**：2D 提升只能处理可见表面，无法分割物体的内部结构或遮挡部件。如图 Figure 2 所示，当前 SOTA 方法 PartField 在面对 3D 形状的内部结构时完全失效。
2. **不可控分解**：基于特征聚类的方法（如 PartField 的 K-Means 或图割）需要预先指定聚类数目，缺乏灵活的交互机制，用户无法精确控制分割粒度。
3. **开放世界泛化受限**：这些方法通常在有限类别上训练，难以泛化到未见过的物体类别，尤其是 AI 生成的网格或真实世界扫描。

更深层的问题在于**数据和架构的双重缺失**。一方面，大规模原生 3D 零件标注数据极其稀缺——现有的 3D 数据集（如 PartNet）在规模和多样性上远不及 2D 数据集（如 SA-1B）。另一方面，缺乏一个可扩展的 3D 架构，能够像 SAM 在 2D 领域那样，通过提示引导实现灵活的交互式分割。

本文的核心动机在于打破这一僵局：**直接在大规模原生 3D 零件对上训练一个可提示的分割模型**，使其同时具备开放世界泛化能力、交互可控性和对内部几何结构的理解。这一思路的关键在于将两个要素结合——通过模型在环管道获取的大规模原生 3D 标注，以及一个类似 SAM 的提示引导编码器-解码器架构。其中，双分支编码器的设计尤为重要：可学习分支适应原生 3D 零件语义，冻结分支则保留从 SAM 蒸馏的 2D 先验，从而在规模化训练的同时不丢失强大的视觉先验。

## 核心创新

PartSAM 的核心创新在于将 3D 零件分割从“2D 基础模型多视图提升”的间接范式，转变为**直接在大规模原生 3D 零件对上训练可提示分割模型**的直接范式。这一转变通过三个关键设计实现，从根本上解决了现有方法仅能表面理解、不可控分解和开放世界泛化能力弱的问题。

### 范式转换：从特征聚类到提示引导的掩码解码

现有方法（如 **PartField** 依赖 K-Means 或图割进行后处理聚类）将零件分割视为无监督特征分组问题，缺乏用户交互能力。PartSAM 借鉴 SAM 的分割范式，采用**提示引导的编码器-解码器架构**（Figure 3）：用户通过正/负点击提示指定目标零件，模型直接输出对应的分割掩码，无需预先指定聚类数目。这一范式转换使得分割过程从“被动推断”变为“主动可控”，在单次提示下即可实现高质量分割——PartObjaverse-Tiny 上 IoU@1 达到 56.1，相比 **Point-SAM** 的 29.4 相对提升 91%（Table 1）。

### 双分支编码器：原生 3D 学习与 2D 先验的协同

PartSAM 的编码器采用**双分支三平面架构**（Figure 4），这是实现大规模原生 3D 训练的关键设计：
- **可学习分支**：适应原生 3D 零件标注，通过 PVCNN 提取逐点特征并正交投影到三个轴对齐平面，形成初始三平面场。与 PartField 的单分支相比，该分支额外接收 6 个特征通道（XYZ 坐标和法线），增强对三维几何结构的感知。
- **冻结分支**：保留从 SAM 蒸馏的 2D 先验（通过对比学习获得），为模型提供稳定的视觉语义基础。

消融实验（Table 3）验证了这一设计的必要性：仅使用冻结的 PartField 分支（无学习的 3D 分支）导致 IoU@1 从 56.1 降至 42.5；移除预训练权重（从头训练）降至 48.3。这表明**可学习分支负责捕捉原生 3D 零件语义，而冻结分支提供不可或缺的 2D 先验**，二者协同才能实现最优性能。

### 训练数据突破：模型在环标注管道

现有方法依赖 SAM 的多视图 2D 掩码提升到 3D 作为监督信号，这种间接标注不仅噪声大，且无法覆盖内部结构和遮挡部位。PartSAM 提出**模型在环标注管道**（Section 3.5），分两阶段构建大规模原生 3D 零件数据：
1. **Stage 1 整理**：从大规模 3D 资产中筛选语义完整的零件标注，排除过度碎片化的网格（如包含 600+ 连通分量的艺术网格，Figure 5）。
2. **Stage 2 模型在环**：利用 PartField 生成候选零件掩码，通过 IoU 阈值筛选高质量标注，过滤低质量结果（Figure 15）。

该管道将训练数据从 18 万扩展到 50 万个形状、超过 500 万个零件对。消融实验（Table 3）表明，移除模型在环标注数据导致 IoU@1 从 56.1 降至 49.0，自动分割 IoU 从 68.5 降至 62.6。数据规模扩展曲线（Figure 11）进一步证实，随着训练数据从 4 万增至 50 万，分割性能持续提升，验证了**原生 3D 标注数据的规模是模型性能的关键瓶颈**。

### 多掩码输出与质量估计

PartSAM 的掩码解码器并行输出多个候选掩码，并通过**IoU 头**（IoU Head）预测每个候选掩码与真实掩码的 IoU，以自动选择最佳掩码。这一机制使得模型能够在歧义情况下（如提示点位于零件边界）生成多个合理候选，并由质量估计模块做出最优决策，避免了单掩码输出的局限性。

### 创新总结

上述三个创新点构成因果链条：**模型在环标注管道**提供了大规模原生 3D 监督信号，**双分支编码器**使得模型能够有效利用这些信号进行训练，**提示引导的解码器**则赋予模型灵活的交互能力。三者共同实现了 PartSAM 的核心能力——在开放世界中同时具备交互可控性、内部几何结构理解和强泛化能力，摆脱了对 2D 提升范式的依赖。

## 整体框架

![[assets/figures/papers/paper_list_l34_https_openreview_net_forum_id_y8sZUQPYXC/figures/006_Figure_3.jpg]]
*Figure 3: Overview of the PartSAM model. The input shape $P _ { i n }$ is first encoded into a continuous feature field. Point patches sampled from $P _ { i n }$ Pin query this field to obtain input embeddings $F _ { c }$ . , while prompt points are mapped into prompt embeddings $F _ { p }$ . Both $F _ { c }$ and $F _ { p }$ are fed into the mask decoder, where the learnable output token $\bar { T _ { o u t } }$ generates multiple segmentation masks. An additional IoU token $T _ { i o u }$ is used by the IoU head to estimate the quality of each mask*

![[assets/figures/papers/paper_list_l34_https_openreview_net_forum_id_y8sZUQPYXC/figures/007_Figure_4.jpg]]
*Figure 4: Architecture of our dual-branch encoder. Each branch is initialized with pretrained weights of Liu et al. (2025)*

![[assets/figures/papers/paper_list_l34_https_openreview_net_forum_id_y8sZUQPYXC/figures/001_Figure_1.jpg]]
*Figure 1: We propose PartSAM, a promptable 3D part segmentation model trained with large-scale native 3D data. The combination of a scalable architecture and large-scale training data endows PartSAM with strong generalization ability, enabling it to automatically decompose diverse 3D models, including both artist meshes and AI-generated shapes, into semantically meaningful parts*

PartSAM 的整体架构遵循类似 SAM 的“提示引导编码器-解码器”范式，将 3D 点云输入转化为可交互或自动的零件分割掩码。其核心设计目标是使模型能够**直接学习原生三维几何与零件语义**，而非依赖从 2D 基础模型提升的间接特征。整个 pipeline 由六个关键模块级联构成，信息流从原始点云出发，经双分支特征场编码、点补丁聚合、提示嵌入交互、双向变换器解码，最终由 IoU 头完成质量估计与掩码选择。

### 2.1 输入与编码：双分支三平面特征场

输入为 3D 点云 $P_{in}$，可包含坐标、法线和颜色信息。编码器采用**双分支三平面架构**，每个分支均以 PartField（Liu et al., 2025）的预训练权重初始化，但功能定位截然不同：

- **可学习分支**：在输入层额外引入 6 个特征通道（XYZ 坐标和法线），使其能够适应原生 3D 零件标注数据，学习三维几何与零件语义的映射关系。
- **冻结分支**：保持 PartField 的预训练权重不变，保留从 SAM 通过对比学习蒸馏而来的 2D 先验知识。

两个分支各自将点云编码为连续的三平面特征场。消融实验表明，移除任一支路都会导致性能显著下降：仅使用冻结分支时，单次提示 IoU@1 从 56.1 降至 42.5；完全移除预训练权重（从头训练）则降至 48.3（Table 3）。这验证了双分支设计在“保留 2D 先验”与“适应 3D 原生数据”之间的因果互补关系。

### 2.2 点补丁聚合：从连续场到离散嵌入

为将连续特征场转化为解码器可处理的离散令牌，PartSAM 采用最远点采样（FPS）与 K 近邻（KNN）局部聚合策略。具体而言，在输入点云 $P_{in}$ 上通过 FPS 选取 $N_c$ 个中心点，对每个中心点构建局部邻域 $\mathcal{N}(\cdot)$，从三平面场中采样邻域点的特征，再通过共享 MLP 聚合为点补丁嵌入：

$$F_c = \mathrm{MLP}\Big(\{\phi(p) \mid p \in \mathcal{N}(\mathrm{FPS}(P_{in}, N_c))\}\Big) \in \mathbb{R}^{N_c \times C}$$

这一过程将连续的三平面特征场压缩为固定数量的输入令牌 $F_c$，作为掩码解码器的主要输入。

### 2.3 提示嵌入与交互机制

用户提示点（正/负点击）通过提示编码器映射为提示嵌入 $F_p$。在多轮交互中，先前迭代的掩码对数也会被编码并纳入提示信息流，使模型能够根据用户反馈迭代优化分割结果。这一机制赋予了 PartSAM 灵活的交互式标注能力，无需指定聚类数目或零件类别。

### 2.4 掩码解码器：双向变换器与多掩码输出

掩码解码器采用四层双向变换器架构，核心交互发生在两组令牌之间：

- **点补丁嵌入 $F_c$**：承载输入形状的几何与语义信息。
- **拼接令牌 $[F_p; T_{out}; T_{iou}]$**：包含提示嵌入、可学习的输出令牌 $T_{out}$ 和 IoU 令牌 $T_{iou}$。

每层变换器依次执行：令牌内部自注意力、令牌到点嵌入的交叉注意力、点嵌入到令牌的交叉注意力。其中关键操作为：

$$F_c' = \mathrm{CrossAttn}(F_c, [F_p; T_{out}; T_{iou}])$$

通过这一双向信息交换，输出令牌 $T_{out}$ 逐步聚合与提示相关的零件特征，最终并行生成多个候选分割掩码。这种多掩码输出设计使模型能够覆盖不同粒度的零件分解方案。

### 2.5 质量估计与掩码选择

IoU 头接收 IoU 令牌 $T_{iou}$ 的最终状态，预测每个候选掩码与真实掩码的 IoU 分数。在推理时，模型自动选择 IoU 预测值最高的掩码作为输出，无需人工干预。这一机制在交互式分割（用户点击后自动返回最佳掩码）和自动分割（通过 NMS 筛选冗余掩码）中均发挥关键作用。

### 2.6 自动分割管线：Segment-Every-Part

PartSAM 展现出类似 SAM 的涌现能力——训练完成后可自动分解完整形状。自动分割管线的工作流程为：
1. 对输入点云进行 FPS 采样，将每个采样点作为正提示输入模型。
2. 模型为每个提示生成多个候选掩码。
3. 通过 IoU 头筛选高质量掩码，并应用非极大值抑制（NMS）去除重复分割。
4. 通过调整 NMS 阈值（0.1、0.3、0.5、0.7）获得多尺度分割结果。

整个 pipeline 的端到端训练损失函数为：

$$\mathcal{L} = \mathcal{L}_{focal}(M_{out}, M_{gt}) + \alpha \mathcal{L}_{dice}(M_{out}, M_{gt}) + \mathcal{L}_{IoU} + \lambda \mathcal{L}_{triplet}$$

其中焦点损失和 Dice 损失监督掩码质量，IoU 损失训练质量估计头，三元组对比损失强化编码器的零件感知表征能力。

## 核心模块与公式推导

PartSAM 的整体架构由两大核心组件构成：**双分支三平面编码器**（将3D形状编码为连续的特征场）和**提示引导的掩码解码器**（根据用户提示预测分割掩码）。以下逐一剖析各模块的设计动机与实现细节。

### 双分支三平面编码器

编码器的设计是 PartSAM 区别于现有方法的根本所在。现有方法（如 PartField）采用单一的三平面分支，要么仅依赖从 SAM 蒸馏的 2D 先验，要么从头学习 3D 特征，无法同时兼顾开放世界泛化能力和对原生 3D 几何结构的理解。PartSAM 通过**双分支并行编码**解决了这一矛盾（Figure 4）：

- **冻结分支**：保留 PartField 预训练权重，在训练期间不更新参数。该分支通过对比学习从 SAM 蒸馏了丰富的 2D 语义先验，为模型提供强大的开放世界泛化基础。
- **可学习分支**：同样以 PartField 预训练权重初始化，但在训练期间全参数更新。其输入层额外拼接了 6 个特征通道（点的 XYZ 坐标和法线），使该分支能够适应原生 3D 零件标注数据，学习三维几何结构与零件语义之间的映射关系。

两个分支的输出在特征层面融合，形成最终的连续三平面特征场。消融实验（Table 3）提供了因果证据：仅使用冻结的 PartField 分支（Frozen PartField）会导致交互式分割 IoU@1 从 56.1 骤降至 42.5，而完全移除预训练权重（w/o pre-trained weights）则降至 48.3。这表明**两个分支缺一不可**——冻结分支提供 2D 先验，可学习分支捕获 3D 原生语义，二者协同才能实现高性能。

### 点补丁采样与特征聚合

为了将连续的三平面特征场转化为解码器可处理的离散嵌入，PartSAM 采用“采样-分组-聚合”策略（Section 3.1）。给定输入点云 $P_{in}$，首先通过最远点采样（FPS）选择 $N_c$ 个中心点，然后以每个中心点为锚点构建 KNN 局部邻域。对于邻域内的每个点 $p$，从三平面特征场中采样其特征 $\phi(p)$，最后通过共享 MLP 聚合为点补丁嵌入：

$$F_c = \mathrm{MLP}\Big(\{\phi(p) \mid p \in \mathcal{N}(\mathrm{FPS}(P_{in}, N_c))\}\Big) \in \mathbb{R}^{N_c \times C}$$

其中 $\mathcal{N}(\cdot)$ 表示 KNN 局部邻域，$C$ 为特征维度。这一设计将稀疏的点云结构压缩为固定数量的补丁令牌，既保留了局部几何信息，又控制了后续变换器的计算复杂度。

### 提示嵌入与双向变换器掩码解码器

解码器采用类似 SAM 的提示引导范式（Section 3.2）。用户提示点（正/负点击）被编码为提示嵌入 $F_p$，与点补丁嵌入 $F_c$ 一同输入**四层双向变换器**。每层变换器依次执行：
1. 令牌内部的自注意力；
2. 令牌到点嵌入的交叉注意力；
3. 点嵌入回令牌的交叉注意力。

核心交叉注意力操作可形式化为：

$$F_c' = \mathrm{CrossAttn}(F_c, [F_p; T_{out}; T_{iou}])$$

其中 $T_{out}$ 为可学习的输出令牌，用于生成多个候选分割掩码；$T_{iou}$ 为 IoU 令牌，用于后续的质量估计。双向注意力机制使提示信息能够有效传播到全局点嵌入中，同时点嵌入的几何信息也能反向更新令牌表示。

### 掩码预测与质量估计

解码器并行输出多个候选掩码 $M_{out}$（通过输出令牌 $T_{out}$ 与点嵌入的点积生成），并配备一个轻量级 IoU 头，利用 IoU 令牌 $T_{iou}$ 预测每个候选掩码与真实掩码的 IoU。在交互式场景中，用户可迭代添加正/负提示点，模型自动选择 IoU 预测值最高的掩码作为最终输出。

### 训练损失函数

PartSAM 的训练损失由四项组成（Section 3.3）：

$$\mathcal{L} = \mathcal{L}_{focal}(M_{out}, M_{gt}) + \alpha \mathcal{L}_{dice}(M_{out}, M_{gt}) + \mathcal{L}_{IoU} + \lambda \mathcal{L}_{triplet}$$

- **$\mathcal{L}_{focal}$**：焦点损失，缓解正负样本不平衡问题。
- **$\mathcal{L}_{dice}$**：Dice 损失，直接优化分割区域的重叠度，系数 $\alpha$ 控制其权重。
- **$\mathcal{L}_{IoU}$**：IoU 预测损失，监督 IoU 头的质量估计精度。
- **$\mathcal{L}_{triplet}$**：三元组对比损失，沿用 PartField 的设计，强化编码器的特征判别能力，系数 $\lambda$ 控制其权重。

这四项损失的组合训练策略是 PartSAM 能够同时实现交互式分割和自动分割的关键——焦点损失和 Dice 损失直接优化掩码质量，IoU 损失使模型具备自评估能力（支撑自动模式下的 NMS 选择），而三元组损失则保证了编码器特征场的零件感知能力。

## 实验与分析

### 交互式分割：单次提示的跨越式提升

PartSAM 在交互式零件分割任务上展现出远超现有方法的提示效率。在 PartObjaverse-Tiny 基准上，仅需一次正/负点击提示，PartSAM 的 IoU@1 即达到 56.1，而此前最强的交互式方法 Point-SAM 仅为 29.4，相对提升 **91%**（Table 1）。随着提示点数增加至 10，PartSAM 的 IoU@10 达到 87.6，仍领先 Point-SAM 18.5%。在更具挑战性的 PartNetE 数据集上，PartSAM 的 IoU@1 为 59.5，相比 Point-SAM 的 35.9 相对提升 65.7%，IoU@10 则达到 89.9。

![[assets/figures/papers/paper_list_l34_https_openreview_net_forum_id_y8sZUQPYXC/figures/010_Table_1.jpg]]
*Table 1: Quantitative comparison of interactive segmentation on PartObjaverse-Tiny (Yang et al., 2024b) and PartNetE (Liu et al., 2023). The best scores are emphasized in bold. IoU@i denotes mean IoU value with i prompt points. We report the mean IoU on instance-level labels*

定性结果（Figure 6）揭示了性能差距的本质原因：Point-SAM 依赖 SAM 的 2D 特征提升，其分割掩码往往不完整或跨越语义边界；而 PartSAM 直接学习原生 3D 零件语义，即使仅给一个提示点，也能输出完整且语义一致的零件掩码。

### 自动分割：类无关分解的全面领先

在自动“分割所有零件”模式下，PartSAM 在所有基准上均显著超越现有方法。PartObjaverse-Tiny 上，PartSAM 的 mIoU 达 69.5，比第二好的 SAMesh（56.9）高出 **22.1%**；在 PartNetE 上，PartSAM 的 mIoU 为 72.4，比禁用网格连通性的 PartField（59.1）高出 **22.5%**（Table 2）。

![[assets/figures/papers/paper_list_l34_https_openreview_net_forum_id_y8sZUQPYXC/figures/013_Table_2.jpg]]
*Table 2: Quantitative comparison of automatic segmentation on PartObjaverse-Tiny (Yang et al., 2024b) and PartNetE (Liu et al., 2023). * denotes that PartField is evaluated with K-Means clustering without mesh connectivity information. We report the mean IoU on instance-level labels*

值得注意的是公平性设计：PartField 原依赖网格连通性进行图割后处理，这在 PartObjaverse-Tiny 的艺术网格上会人为提升性能——因为艺术网格的连通组件天然对应语义零件。评估时禁用了 PartField 的连通性信息，使其以纯 K-Means 聚类运行。而 PartSAM 本身不依赖连通性，其优势完全来自学习到的零件语义。

### 内部结构与遮挡零件：2D 提升范式的根本局限

Figure 9 展示了 PartSAM 与 2D 提升方法在 AI 生成网格上的关键差异。AI 生成网格常包含内部结构（如椅子底部的支撑梁）和被遮挡零件。SAMesh 等基于多视图 2D 掩码的方法无法可靠恢复这些不可见部分，因为 2D 渲染无法捕捉内部几何。PartSAM 直接在 3D 空间学习，能够一致地分割可见和隐藏的结构。Figure 12a 进一步展示了这一能力的应用价值：PartSAM 可准确分割内部零件，进而支持材质编辑和零件重定位。

### 消融实验：双分支编码器与大规模数据缺一不可

Table 3 的系统消融揭示了三个关键设计的作用：

![[assets/figures/papers/paper_list_l34_https_openreview_net_forum_id_y8sZUQPYXC/figures/015_Table_3.jpg]]
*Table 3: Ablation study on PartObjaverse-Tiny (Yang et al., 2024b). We report the mean IoU on instance-level labels for both the interactive and automatic segmentation tasks*

**双分支编码器的互补性。** 移除可学习分支、仅保留冻结的 PartField 分支，IoU@1 从 56.1 骤降至 42.5，自动分割 mIoU 从 68.5 降至 52.1。反之，从头训练（移除预训练权重）导致 IoU@1 降至 48.3，自动分割 mIoU 降至 60.5。这表明冻结分支提供的 SAM 2D 先验和可学习分支对原生 3D 数据的适应同等重要，二者形成互补。

**模型在环标注数据的规模效应。** 移除模型在环管道标注的数据（仅使用第一阶段整理的 18 万形状），IoU@1 从 56.1 降至 49.0，自动分割 mIoU 从 68.5 降至 62.6。Figure 11 的扩展曲线进一步量化了这一趋势：随着训练数据从 4 万扩展到 50 万形状，交互式和自动分割性能持续单调提升，未出现饱和迹象。

![[assets/figures/papers/paper_list_l34_https_openreview_net_forum_id_y8sZUQPYXC/figures/017_Figure_11.jpg]]
*Figure 11: Scaling curve of PartSAM with respect to training data size. The plot shows segmentation accuracy (IoU for interactive segmentation with 1 prompt point and automatic segmentation) as the training data increases from 40k to 500k shapes*

**训练数据域的重要性。** 仅在 PartNet 上训练导致模型无法泛化到未见类别，这解释了为何需要大规模多样化数据（Section A.2.2）。

### 复杂度与效率

Table 5 的复杂度分析表明，PartSAM 在效率上具有显著优势。自动分割耗时约 4-12 秒，而 SAMesh 需约 7 分钟，SAMPart3D 需约 15 分钟。PartSAM 的可训练参数量为 118M，与对比方法相当，但其解码器随提示点数增加呈次线性扩展。

![[assets/figures/papers/paper_list_l34_https_openreview_net_forum_id_y8sZUQPYXC/figures/021_Table_5.jpg]]
*Table 5: Complexity analysis. We compare the time of automatic segmentation, the time of interactive segmentation, and the number of trainable network parameters*

### 失败模式与局限

Figure 14 和 Figure 17、18 中的失败案例揭示了 PartSAM 的几类典型失效：

1. **长尾结构遗漏**：训练数据中极少出现的细微结构（如雕刻字母）无法被准确分割，模型倾向于将其合并到相邻零件中。
2. **语义模糊对象**：对于缺乏清晰零件结构的对象（如珊瑚雕塑），分割结果缺乏语义意义。
3. **几何不规则放大歧义**：AI 生成网格的几何缺陷或真实扫描的噪声会模糊零件边界，导致过度分割或欠分割。
4. **类无关输出的固有限制**：PartSAM 仅输出分割掩码而不附带语义标签，限制了在下游语义感知任务中的直接应用。

### 连通性后处理的影响

Table 4 揭示了连通性在评估中的微妙作用。PartField 结合连通性后处理时，PartObjaverse-Tiny 上的 mIoU 可达 79.2，但这利用了艺术网格的连通组件天然对应零件的特性——这是一个数据集偏差而非方法优势。PartSAM 通过图割后处理也可将 mIoU 从 69.5 提升至 73.7，但仍低于 PartField 的 79.2，因为 PartField 的训练目标（三平面特征场的对比学习）与连通性后处理的协同更强。在不使用连通性的公平设定下，PartSAM 的 69.5 显著优于 PartField 的 51.5。

![[assets/figures/papers/paper_list_l34_https_openreview_net_forum_id_y8sZUQPYXC/figures/019_Table_4.jpg]]
*Table 4: Quantitative comparison of automatic segmentation on PartObjaverse-Tiny (Yang et al., 2024b) under different settings. We report the mean IoU on instance-level labels*

### 补充图表

![[assets/figures/papers/paper_list_l34_https_openreview_net_forum_id_y8sZUQPYXC/figures/023_Table_6.jpg]]
*Table 6: Quantitative comparison of automatic segmentation on 3DCoMPAT++ (Slim et al., 2025). The best scores are emphasized in bold. We report the mean IoU*

## 方法谱系与知识库定位

### 1. 问题定位与范式转换

现有3D零件分割方法在范式上形成了一个以2D基础模型为核心的技术谱系。**PartSLIP**、**SAMPart3D**、**SAMesh** 等工作通过将Segment Anything Model (SAM) 的多视图2D掩码提升到3D来获得零件分割结果。这种间接范式的根本瓶颈在于：2D渲染图像仅捕捉物体表面外观，无法感知三维几何的内部结构、遮挡关系和零件间的空间拓扑。因此，这些方法本质上只能实现“表面级理解”，在面对AI生成网格中常见的内部零件（如嵌入机械结构）或严重遮挡区域时，分割结果不可靠或完全失败（Figure 9）。

**PartField** (Liu et al., 2025) 代表了另一条技术路线——直接在3D特征场上进行聚类驱动的零件分解。该方法通过三平面编码器学习连续特征场，再以K-Means或图割获得分割结果。然而，这种聚类范式缺乏用户交互能力，分解的粒度和语义可控性受限于聚类数目预设和特征空间质量。更关键的是，PartField的训练数据仍依赖SAM的2D蒸馏，未能从根本上摆脱对2D先验的间接依赖。

PartSAM的方法论突破在于将上述两条路线进行了因果性重组：**保留2D先验作为辅助特征来源，但将核心监督信号和架构设计锚定在原生3D零件标注上**。具体而言，PartSAM将SAM的提示引导掩码解码范式直接迁移到3D域，使得模型能够通过正/负点击提示灵活控制分割结果，同时在大规模原生3D零件对上学习内在几何语义。这一范式转换的因果机制可概括为：

> 大规模原生3D零件标注（数据）+ 提示引导编码器-解码器架构（模型）→ 直接学习三维几何-零件语义映射 → 同时获得开放世界泛化、交互可控性和内部结构理解能力。

### 2. 与基线方法的架构差异

下表从五个关键设计维度对比PartSAM与代表性基线方法的核心差异：

| 设计维度 | PartField (Liu et al., 2025) | Point-SAM (Zhou et al., 2025) | **PartSAM (本方法)** |
|---------|------|-----------|-------------------|
| **分割范式** | 特征聚类 (K-Means/图割) | 基于SAM特征的点提示分割 | 提示引导掩码解码器，多候选掩码+IoU质量选择 |
| **编码器架构** | 单一三平面分支 | 依赖SAM的2D特征提升 | 双分支三平面：可学习分支适应3D原生数据，冻结分支保留SAM 2D先验 |
| **训练数据** | SAM蒸馏的2D特征监督 | 2D SAM掩码提升到3D | 原生3D零件标注（整理+模型在环管道） |
| **交互能力** | 无（需预设聚类数） | 支持正/负点击 | 支持正/负点击，迭代式标注，自动选择最优掩码 |
| **掩码选择** | 单尺度聚类结果 | 单掩码输出 | 并行解码多候选掩码，IoU头预测质量以选择最佳 |

双分支编码器是架构层面的核心创新。冻结分支保留了从SAM蒸馏的2D先验（通过PartField预训练权重初始化），为模型提供跨模态的特征锚点；可学习分支则直接在大规模原生3D零件对上优化，捕捉仅从3D几何可获得的零件语义。消融实验（Table 3）的因果证据链清晰：仅使用冻结分支（Frozen PartField）导致交互分割IoU@1从56.1骤降至42.5；移除预训练权重（从头训练）则降至48.3。这证明了两支分支存在互补增益——2D先验提供泛化基础，3D原生学习提供几何特异性。

### 3. 数据策略的定位

PartSAM的数据策略在3D零件分割领域具有独特定位。现有方法要么依赖人工标注的PartNet（覆盖类别有限），要么通过2D SAM间接获取监督信号。PartSAM的两阶段数据管道实现了规模与质量的平衡：

- **阶段一（整理）**：从大规模3D资产库中筛选具有语义连贯零件结构的网格，排除过度碎片化的资产（如Figure 5所示超过600个连通分量的网格），获得18万个形状的初始训练集。
- **阶段二（模型在环）**：利用阶段一训练的PartSAM作为标注器，对50万个新形状生成候选零件掩码，通过IoU阈值过滤低质量标注（Figure 15），最终将训练数据扩展到50万形状、超过500万零件对。

扩展曲线（Figure 11）提供了清晰的因果证据：训练数据从4万扩展到50万形状，交互分割IoU@1和自动分割mIoU均持续提升，未出现饱和迹象。这表明PartSAM的架构容量足以消化更大规模的原生3D数据，而数据规模仍是当前性能的活跃约束。

### 4. 适用边界与局限

PartSAM的能力边界由以下因素共同定义：

**训练数据分布边界**。模型在PartObjaverse-Tiny和PartNetE上表现优异，但对训练数据中极少出现的结构（如雕刻字母、复杂装饰纹样）分割失败（Figure 14）。这是典型的**长尾分布问题**——当前3D零件数据集的多样性远不及2D数据集SA-1B，导致模型对罕见几何模式的泛化不足。

**语义感知缺失**。PartSAM目前仅输出**类无关**的零件分割掩码，无法直接生成“轮子”“把手”等语义标签。这限制了其在需要语义理解的下游任务（如场景图构建、语言引导编辑）中的直接使用。论文将此列为开放问题，指出需要大规模语义标注的3D零件数据集。

**几何质量敏感性**。在处理AI生成的网格或粗糙真实扫描时，几何不规则（如非流形边、自相交面）和细节错误可能放大零件边界的歧义性（Figure 17, 18中的失败案例）。PartSAM缺乏显式的几何正则化机制来处理这些退化情况。

**语义结构依赖性**。当对象本身缺乏清晰的语义结构时（如珊瑚雕塑、抽象艺术造型），PartSAM的分割结果可能无意义。这是所有零件分割方法的共性局限，源于“零件”概念本身预设了对象具有功能或语义上的可分解性。

**与后处理方法的兼容性**。PartSAM本身不依赖网格连通性，这使其在处理非连通零件（如对称分离的部件）时具有优势。但Table 4显示，通过图割后处理利用连通性信息可以进一步提升结果（mIoU从69.5提升至70.8），表明几何先验仍有补充价值。

### 5. 开放问题

1. **语义标注规模化**：如何为3D形状及其零件生成大规模语义标签数据集，使PartSAM具备语义感知能力？这可能涉及视觉-语言模型与3D表示的深度融合。

2. **长尾结构处理**：如何改进模型以更好地处理罕见或细微结构（如表面雕刻、细小附件）？可能需要少样本学习机制或更丰富的数据增强策略。

3. **跨模态统一**：PartSAM的双分支设计暗示了2D与3D先验的互补性，但两者的融合仍停留在特征层面。是否存在更紧密的跨模态对齐机制，使2D语义知识与3D几何理解相互增强？

4. **数据规模上限**：Figure 11的扩展曲线未饱和，暗示更大规模数据仍可带来增益。3D数据的规模化采集和自动标注管道的效率上限在哪里？

5. **非刚性形状扩展**：当前方法针对刚性物体的零件分割，如何扩展到铰接物体或可变形物体的动态零件理解？

## 原文 PDF

![[paperPDFs/ICLR_2026/PartSAM_A_Scalable_Promptable_Part_Segmentation_Model_Trained_on_Native_3D_Data.pdf]]
