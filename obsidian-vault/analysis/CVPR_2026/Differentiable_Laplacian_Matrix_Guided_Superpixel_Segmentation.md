---
title: Differentiable Laplacian Matrix Guided Superpixel Segmentation
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/Differentiable_Laplacian_Matrix_Guided_Superpixel_Segmentation.pdf
project_link: null
code_link: "https://github.com/jeremyJJB/Differentiable-Laplacian-Matrix-Guided-Superpixel-Segmentation"
aliases:
- DLMGSS
tags:
- CVPR_2026
- topic/other_unclear
- topic/other_unclear/general
core_operator: 图拉普拉斯损失（Graph-Laplacian Loss）：通过最大化每个超像素对应图的拉普拉斯矩阵的迹，隐式减少零特征值重数，从而提升超像素内部的空间连通性。
primary_logic: 将超像素的像素分配概率建模为图，并利用拉普拉斯矩阵迹（所有度之和）作为可微代理，在训练中直接惩罚碎片化，使得超像素分割网络无需不可微后处理即可输出连通区域。
claims:
- 拉普拉斯损失在所有架构上显著降低碎片化指标（超出分量数和游离像素数）
- 拉普拉斯变体在不使用EC的情况下，在紧凑度和边界召回率上超越基线，且对ASA和边界精度影响极小
- 消融实验证实LAP是连通性提升的主要驱动因素，单独使用MSD或WR无法消除碎片化
- BSDS500 上 Compactness (CO), Boundary Recall (BR) = Laplacian variants (SCN-LAP, AINet-LAP, CDS-LAP, SSM-LAP) o...
---

# Differentiable Laplacian Matrix Guided Superpixel Segmentation

> [!tip] 核心洞察
> 将超像素的像素分配概率建模为图，并利用拉普拉斯矩阵迹（所有度之和）作为可微代理，在训练中直接惩罚碎片化，使得超像素分割网络无需不可微后处理即可输出连通区域。

| 字段 | 内容 |
|------|------|
| 中文题名 | 可微拉普拉斯矩阵引导的超像素分割 |
| 英文题名 | Differentiable Laplacian Matrix Guided Superpixel Segmentation |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://openaccess.thecvf.com/content/CVPR2026/html/Juybari_Differentiable_Laplacian_Matrix_Guided_Superpixel_Segmentation_CVPR_2026_paper.html) · [Code](https://github.com/jeremyJJB/Differentiable-Laplacian-Matrix-Guided-Superpixel-Segmentation) |
| Topic | #topic/other_unclear #topic/other_unclear/general |
| Method | Differentiable Laplacian Matrix Guided Superpixel Segmentation |
| Dataset | BSDS500, NYUv2 |

> [!tip] 效果简介
> - BSDS500 上，Compactness (CO), Boundary Recall (BR) Laplacian variants (SCN-LAP, AINet-LAP, CDS-LAP, SSM-LAP) outperform correspond... vs SCN, AINet, CDS, SSM (CO 和 BR 明显提升，ASA 和 BP 变化极小)。
> - NYUv2 上，Compactness (CO), Boundary Recall (BR) Laplacian variants outperform baselines (both with and without EC) vs SCN, AINet, CDS, SSM (趋势与BSDS500一致，CO和BR提升)。
> - BSDS500 (no EC) 上，Average Excess Components (XC_avg), Average Stray Pixels (Stray_avg) All Laplacian variants show substantially lower fragmentation vs SCN, AINet, CDS, SSM (碎片化指标降低数倍至数十倍)。

## 概要

深度超像素分割方法长期面临一个结构性瓶颈：网络输出的像素分配概率往往产生碎片化、不连通的超像素，必须借助不可微的强制连通性（Enforced Connectivity, EC）后处理来修复。这一后处理步骤切断了端到端梯度流，使超像素生成无法与下游任务联合优化。本文提出**可微拉普拉斯矩阵引导的超像素分割**，核心思路是将每个超像素的像素分配概率建模为图，通过最大化该图拉普拉斯矩阵的迹来隐式减少零特征值重数，从而在训练中直接促进空间连通性。

该方法将三个可微损失项——**图拉普拉斯损失**（$\mathcal{L}_{\mathrm{LAP}}$）、**最小语义距离损失**（$\mathcal{L}_{\mathrm{MSD}}$）和**加权重建损失**（$\mathcal{L}_{\mathrm{WR}}$）——集成到现有深度超像素架构中，无需修改网络结构。在BSDS500和NYUv2上的实验表明，加入拉普拉斯损失后，**SCN**（Yang et al., CVPR 2020）、**AINet**（Wang et al., ICCV 2021）、**CDS**（Xu et al., AAAI 2024）和**SSM**（Jia et al., IEEE SPL 2025）四种基线模型在不使用EC的情况下，紧凑度（CO）和边界召回率（BR）均超越原始版本，而分割精度（ASA）和边界精度（BP）仅受极小影响。碎片化指标上，拉普拉斯变体的平均超出分量数和平均游离像素数较基线降低数倍至数十倍，证实$\mathcal{L}_{\mathrm{LAP}}$是连通性提升的主要驱动因素。该方法显著减少了对不可微后处理的依赖，推动超像素生成向完全端到端可微迈进。



### 超像素：从传统到深度学习的范式转移

超像素分割的目标是将图像过分割为若干感知一致、空间紧凑的区域，作为中层级视觉表示，广泛应用于语义分割、目标检测、立体匹配等任务。传统方法如 **SLIC**（Achanta et al., TPAMI 2012）通过手工设计的颜色-空间距离进行局部聚类，虽然计算高效，但难以适应复杂场景的语义边界。

深度超像素方法的兴起改变了这一格局。以 **SCN**（Yang et al., CVPR 2020）、**AINet**（Wang et al., ICCV 2021）、**CDS**（Xu et al., AAAI 2024）和 **SSM**（Jia et al., IEEE SPL 2025）为代表的模型，通过像素嵌入网络与可微分配头联合学习，在语义边界精度（Boundary Recall, BR）和紧凑度（Compactness, CO）上显著超越了传统方法。这些模型的核心范式是：编码器提取像素特征 → 卷积层输出像素-超像素分配概率矩阵 $Q \in [0,1]^{N \times M}$ → 通过重建损失优化语义一致性。

### 核心瓶颈：不可微的强制连通性后处理

然而，深度超像素模型面临一个根本性缺陷：**训练过程中缺乏空间连通性约束，导致网络输出的超像素高度碎片化**——一个超像素常被分裂为多个不连通的分量，散布在图像的不同位置。这种碎片化严重违背了超像素“空间紧凑、区域连通”的基本定义。

现有模型的应对策略是引入**强制连通性（Enforced Connectivity, EC）**后处理：在推理阶段，对每个超像素保留其最大连通分量，将游离的小分量重新分配给相邻超像素。EC虽然修复了连通性，但带来了三个关键问题：

1. **破坏端到端可微性**：EC是离散的图连通分量分析操作，不可微分，切断了超像素模块与下游任务（如语义分割、目标检测）之间的梯度流动，阻碍了联合优化。
2. **掩盖模型真实性能**：EC掩盖了模型输出的碎片化程度，使得研究者难以评估和诊断模型的连通性学习能力。
3. **引入不可控的边界偏移**：EC的重新分配操作可能改变超像素边界，带来不可预测的精度损失。

图1（见实验部分）直观展示了这一困境：CDS模型的原始输出存在大量碎片化分量，EC虽然修复了连通性，但超像素形状不规则、边界精度受限。

### 现有替代方案的局限

针对EC的缺陷，已有工作尝试从架构层面解决连通性问题。**SIN**（Yuan et al., PRICAI 2021）设计了具有内置连通性的专用网络结构，无需EC后处理即可输出连通超像素。然而，SIN在语义边界精度和紧凑度上明显落后于依赖EC的主流模型（SCN、AINet、CDS、SSM），表明架构层面的硬约束可能牺牲了表示灵活性。

### 本文动机：将连通性植入训练过程

本文的核心洞察是：**连通性不应是后处理阶段的补救措施，而应作为可微的正则化项直接嵌入训练损失**。这需要回答一个关键问题——如何设计一个可微的代理指标，能够有效度量并惩罚超像素的碎片化程度？

论文的答案是：将每个超像素的像素分配概率建模为图，并利用图拉普拉斯矩阵的谱性质。直观而言，一个连通图的拉普拉斯矩阵零特征值重数为1（对应连通分量数），而碎片化的超像素对应多个零特征值。通过最大化拉普拉斯矩阵的迹（即所有像素度之和），可以隐式减少零特征值重数，从而促进空间连通性——这一过程完全可微，无需任何非可微后处理。

基于这一核心思想，论文提出了三个可微损失项的组合：图拉普拉斯损失（L_LAP）驱动连通性、最小语义距离损失（L_MSD）强化语义边界、加权重建损失（L_WR）聚焦边界难例。这些损失可直接集成到现有架构（SCN、AINet、CDS、SSM）中，无需修改网络结构，保证了公平比较和广泛适用性。



## 核心方法与创新机理

本工作的核心创新并非提出一种新的超像素分割架构，而是提出一套**可微的损失函数体系**，直接解决深度超像素模型长期依赖不可微后处理的瓶颈问题。这套损失函数可即插即用地集成到现有架构中，从训练阶段根本性地提升超像素的空间连通性与语义边界精度。

### 问题瓶颈：不可微的强制连通性后处理

深度超像素模型（如 **SCN** (Yang et al., CVPR 2020)、**AINet** (Wang et al., ICCV 2021)、**CDS** (Xu et al., AAAI 2024)、**SSM** (Jia et al., IEEE SPL 2025)）通常输出碎片化、不连通的超像素区域。为获得符合定义的连通超像素，这些方法必须依赖**强制连通性（Enforced Connectivity, EC）**后处理——通过将不连通的小分量重新分配给邻近超像素来“修复”结果。然而，EC 是不可微的，这切断了超像素分割与下游任务（如语义分割、目标检测）之间端到端联合优化的可能性，成为该领域的核心瓶颈。

### 核心机制：图拉普拉斯损失的可微连通性正则化

本方法的核心洞察在于：将超像素的像素分配概率矩阵 $Q \in [0,1]^{N \times M}$ 建模为图，并利用图拉普拉斯矩阵的迹作为**可微的连通性代理指标**。

对于每个超像素 $s$，构建一个图 $G_s$，其中节点为像素，边权重由相邻像素同时属于该超像素的概率乘积给出。像素 $i$ 在超像素 $s$ 中的度定义为：

$$d_{i,s} = \sum_{j \in \mathcal{N}_i} q_{i,s} q_{j,s}$$

图拉普拉斯矩阵的迹等于所有节点的度之和，即 $\mathrm{tr}(L_s) = \sum_i d_{i,s}$。**迹越大，意味着超像素内部像素间的高权重连接越多，空间连通性越强**。由此构建的图拉普拉斯损失为：

$$\mathcal{L}_{\mathrm{LAP}}(\boldsymbol{\theta}; \mathbf{x}) = 1 - \frac{1}{M} \sum_{s=1}^{M} \frac{\mathrm{tr}(L_s)}{8 N_s}$$

该损失通过最大化归一化迹，在训练中直接惩罚碎片化，使得网络无需不可微的 EC 后处理即可输出连通区域。这是**首次将图拉普拉斯正则化引入超像素分割训练**，也是本方法最核心的 *changed slot*。

### 辅助创新：语义边界与边界聚焦

为弥补单纯连通性正则化可能忽略的语义边界精度，方法引入两个辅助损失：

- **最小语义距离损失 $\mathcal{L}_{\mathrm{MSD}}$**：通过基于采样的铰链损失最大化不同语义类别像素嵌入之间的最小欧氏距离，增强超像素边界与语义边界的对齐。边际参数 $m=1.5$。

- **加权重建损失 $\mathcal{L}_{\mathrm{WR}}$**：对包含多类别的“混合块”像素赋予权重 1.0，对单类别块像素赋予权重 0.1，并通过归一化使总权重和为 $N$。这迫使模型聚焦于语义边界区域的精确分配，解决了标准重建损失对所有像素等权处理的不足。

### 与专用架构方法的区别

值得注意的是，此前已有工作尝试通过专用架构实现内置连通性，如 **SIN** (Yuan et al., PRICAI 2021)。然而，这类方法在精度上显著落后于主流模型。本方法的优势在于**不修改网络结构**，仅通过损失函数即可达到甚至超越 EC 后处理的连通性水平，同时保持与主流架构同等的精度，实现了连通性与精度的解耦优化。

### 方法谱系与知识库定位

| 维度 | 基线方法 | 本方法 |
|------|---------|--------|
| 连通性保障 | 依赖不可微 EC 后处理 | 可微图拉普拉斯损失 $\mathcal{L}_{\mathrm{LAP}}$ |
| 边界约束 | 无明确边界损失 | 最小语义距离损失 $\mathcal{L}_{\mathrm{MSD}}$ |
| 像素权重 | 等权重重建 | 边界聚焦的加权重建 $\mathcal{L}_{\mathrm{WR}}$ |
| 架构侵入性 | — | 零侵入，即插即用 |

在知识库定位上，本工作属于**超像素分割的可微训练范式**，填补了“深度超像素模型端到端可微性”的空白。其核心贡献——图拉普拉斯迹最大化作为连通性代理——源自谱图理论，为超像素领域提供了新的理论工具。最终损失函数为各损失的加权组合：

$$\mathcal{L}(\boldsymbol{\theta}; \mathbf{x}, \mathbf{y}) = \mathcal{L}_{\mathrm{base}} + \lambda_{\mathrm{LAP}} \mathcal{L}_{\mathrm{LAP}} + \lambda_{\mathrm{MSD}} \mathcal{L}_{\mathrm{MSD}} + \lambda_{\mathrm{WR}} \mathcal{L}_{\mathrm{WR}}$$

其中 $\lambda_{\mathrm{LAP}}=360$、$\lambda_{\mathrm{MSD}}=10^{-3}$、$\lambda_{\mathrm{WR}}=1$，$\mathcal{L}_{\mathrm{base}}$ 为各基线架构的专有损失。



本文提出一种**可微拉普拉斯矩阵引导的超像素分割**方法，其核心思想是将超像素连通性约束从不可微的后处理阶段迁移至端到端训练过程中。整体框架由一个通用的超像素分配网络和三个可微损失函数构成，无需修改现有网络架构即可集成。

**前向推理流程。** 给定输入图像 $\mathbf{x}$，网络 $f_{\theta} = h \circ g$ 输出超像素分配概率矩阵 $Q \in [0,1]^{N \times M}$，其中 $N = H \times W$ 为像素总数，$M$ 为超像素数量。具体而言，像素嵌入网络 $g$ 负责提取每个像素的特征表示，超像素分配头 $h$ 是一个卷积层配合 softmax 归一化，将嵌入映射为像素到超像素的软分配概率 $q_{i,s}$。为控制计算复杂度，图像被划分为由 $16 \times 16$ 步长诱导的规则网格块，每个超像素以其中一个块为中心，每个像素仅被允许分配到其局部邻域内的 9 个候选超像素（即 $3 \times 3$ 块范围）。

**训练损失架构。** 训练目标由基线模型的专有损失 $\mathcal{L}_{\text{base}}$ 与三个新增的可微损失项加权组合而成：

$$
\mathcal{L}(\boldsymbol{\theta}; \mathbf{x}, \mathbf{y}) = \mathcal{L}_{\text{base}} + \lambda_{\text{LAP}} \mathcal{L}_{\text{LAP}} + \lambda_{\text{MSD}} \mathcal{L}_{\text{MSD}} + \lambda_{\text{WR}} \mathcal{L}_{\text{WR}}
$$

其中 $\lambda_{\text{LAP}} = 360$，$\lambda_{\text{MSD}} = 10^{-3}$，$\lambda_{\text{WR}} = 1$。三个损失项各自承担不同的优化目标：

1. **图拉普拉斯损失 $\mathcal{L}_{\text{LAP}}$**：将每个超像素建模为一个图，节点为分配给该超像素的像素，边权重由相邻像素的分配概率乘积 $q_{i,s} q_{j,s}$ 定义。通过最大化所有超像素图的归一化拉普拉斯矩阵迹（即度之和），隐式减少零特征值重数，从而在训练中直接惩罚碎片化、促进空间连通性——这是本方法消除不可微 EC 后处理依赖的关键机制。

2. **最小语义距离损失 $\mathcal{L}_{\text{MSD}}$**：基于采样的铰链损失（margin $m = 1.5$），最大化不同语义类别像素嵌入之间的最小欧氏距离，增强超像素边界与语义边界的对齐精度。

3. **加权重建损失 $\mathcal{L}_{\text{WR}}$**：对标准交叉熵重建损失进行重新加权——包含多类别的混合块像素权重设为 1.0，单类别块像素权重设为 0.1，并归一化使总权重和为 $N$。这迫使模型聚焦于语义边界区域的精确分配，而不过度惩罚同质区域。

**模块间因果关系。** 三个损失项协同作用：$\mathcal{L}_{\text{LAP}}$ 是连通性提升的主要驱动因素（消融实验证实单独使用 $\mathcal{L}_{\text{MSD}}$ 或 $\mathcal{L}_{\text{WR}}$ 无法消除碎片化），$\mathcal{L}_{\text{MSD}}$ 和 $\mathcal{L}_{\text{WR}}$ 分别在语义边界精度和边界区域分配质量上提供补充约束。该损失组合可直接加载到 **SCN**（Yang et al., CVPR 2020）、**AINet**（Wang et al., ICCV 2021）、**CDS**（Xu et al., AAAI 2024）、**SSM**（Jia et al., IEEE SPL 2025）等现有深度超像素架构上，无需修改网络结构。

### 补充图表

![[assets/figures/papers/paper_list_l2118_https_openaccess_thecvf_com_content_CVPR2026_html_Juybari_Differentiable/figures/001_Figure_1.jpg]]
*Figure 1: Comparison of superpixels from a deep learning model (CDS) under Enforced Connectivity (EC) post-processing and the same model with graph-Laplacian (LAP) regularization. Our proposed LAP yields more compact superpixels, more precise boundaries, and fewer excess components without requiring EC*



### 整体框架：通用超像素分配网络

方法构建于一个通用的超像素分配网络之上：$f_{\theta} = h \circ g$，其中 $g$ 为像素嵌入网络（负责将每个像素映射为嵌入向量），$h$ 为卷积层后接 softmax 归一化，输出像素-超像素分配概率矩阵：

$$Q = f_{\theta}(\mathbf{x}) \in [0,1]^{N \times M}$$

其中 $N = H \times W$ 为像素总数，$M$ 为超像素数量。每个元素 $q_{i,s}$ 表示像素 $i$ 被分配给超像素 $s$ 的概率。

为控制计算复杂度，图像被划分为由 $16 \times 16$ 步长诱导的规则网格方块，每个超像素中心落在一个方块上；每个像素仅被允许分配给其局部邻域内的 9 个候选超像素（即 $3 \times 3$ 方块区域）。这一局部搜索窗的设计继承了深度超像素方法的常见范式，但论文在此框架上引入了三个可微损失项，构成了核心贡献。

### 图拉普拉斯损失 $\mathcal{L}_{\mathrm{LAP}}$：可微的连通性正则化

**动机**：深度超像素模型输出的超像素往往碎片化、不连通，传统做法依赖不可微的强制连通性（Enforced Connectivity, EC）后处理，破坏了端到端可微性。核心洞察在于：若将每个超像素视作一个图，其连通分量数与该图拉普拉斯矩阵的零特征值重数直接相关——连通分量越多，零特征值越多。因此，最大化拉普拉斯矩阵的迹（所有特征值之和）等价于减少零特征值的数量，从而隐式地促进连通性。

**图构建**：对于每个超像素 $s$，构建图 $G_s = (V_s, E_s)$，其中节点为像素，边存在于相邻像素之间。边权重定义为两端像素共同属于超像素 $s$ 的概率乘积，像素 $i$ 在图 $G_s$ 中的度定义为：

$$d_{i,s} = \sum_{j \in \mathcal{N}_i} q_{i,s} q_{j,s}$$

其中 $\mathcal{N}_i$ 为像素 $i$ 的邻域集合（论文采用 8-邻域）。

**损失定义**：图 $G_s$ 的拉普拉斯矩阵 $L_s$ 的迹等于所有像素度之和。为消除超像素大小差异的影响，按超像素的像素数 $N_s$ 进行归一化（$8 N_s$ 为全连通图的迹上界）。最终损失为所有超像素归一化迹的均值，并转化为最小化形式：

$$\mathcal{L}_{\mathrm{LAP}}(\boldsymbol{\theta}; \mathbf{x}) = 1 - \frac{1}{M} \sum_{s=1}^{M} \frac{\mathrm{tr}(L_s)}{8 N_s}$$

该损失完全可微，可直接通过反向传播优化。其核心机制在于：当超像素内部碎片化时，各连通分量之间的边权重趋近于零，导致迹值降低、损失增大；优化过程推动相邻的同超像素像素产生更高的共分配概率，从而弥合碎片。

### 最小语义距离损失 $\mathcal{L}_{\mathrm{MSD}}$：语义边界增强

**动机**：仅靠连通性正则化无法保证超像素边界与语义边界对齐。$\mathcal{L}_{\mathrm{MSD}}$ 旨在最大化不同语义类别像素嵌入之间的最小距离，使超像素边界更倾向于落在语义边界处。

**实现**：在每次训练迭代中，从不同语义类别各随机采样一个像素，计算其嵌入向量之间的最小欧氏距离 $\rho$，并施加铰链损失（margin $m = 1.5$）：

$$\mathcal{L}_{\mathrm{MSD}}(\theta; \mathbf{x}, \mathbf{y}) = \left( \max(0, m - \rho) \right)^2$$

该损失促使不同类别的嵌入在特征空间中相互远离，从而增强超像素边界的语义一致性。

### 加权重建损失 $\mathcal{L}_{\mathrm{WR}}$：聚焦边界难例

**动机**：标准重建损失对所有像素等权重处理，但语义边界区域的像素分配更具挑战性，也更为关键。$\mathcal{L}_{\mathrm{WR}}$ 通过差异化权重将模型注意力导向边界区域。

**权重设计**：基于 $16 \times 16$ 的规则网格方块，若方块内仅含单一语义类别，权重设为 $0.1$；若方块内含两个及以上类别（即跨越语义边界），权重设为 $1.0$：

$$w_{i} = \begin{cases} 0.1 & \text{若块} \mathcal{B} \text{仅含单一类别} \\ 1.0 & \text{若块} \mathcal{B} \text{含} \geq 2 \text{个类别} \end{cases}$$

为保持整体损失尺度不变，对权重进行归一化，使所有权重之和等于总像素数 $N$：

$$W_{i} = \frac{N \cdot w_{i}}{\sum_{j=1}^{N} w_{j}}$$

最终加权重建损失为：

$$\mathcal{L}_{\mathrm{WR}}(\boldsymbol{\theta}; \mathbf{x}, \mathbf{y}) = \sum_{i=1}^{N} W_{i} E(\mathbf{y}_{i}, \mathbf{y}_{i}')$$

其中 $E(\mathbf{y}_{i}, \mathbf{y}_{i}')$ 为像素级语义属性重建的交叉熵损失。混合块与单类块之间 $10:1$ 的权重比使得模型在边界区域施加更强的优化信号。

### 总体损失与超参数

最终训练目标将基线模型的专有损失与三个新增损失项结合：

$$\mathcal{L}(\boldsymbol{\theta}; \mathbf{x}, \mathbf{y}) = \mathcal{L}_{\mathrm{base}} + \lambda_{\mathrm{LAP}} \mathcal{L}_{\mathrm{LAP}} + \lambda_{\mathrm{MSD}} \mathcal{L}_{\mathrm{MSD}} + \lambda_{\mathrm{WR}} \mathcal{L}_{\mathrm{WR}}$$

其中 $\lambda_{\mathrm{LAP}} = 360$，$\lambda_{\mathrm{MSD}} = 10^{-3}$，$\lambda_{\mathrm{WR}} = 1$。$\lambda_{\mathrm{LAP}}$ 取值较大，反映了连通性正则化在整体优化中的主导地位；消融实验证实，$\mathcal{L}_{\mathrm{LAP}}$ 是连通性提升的主要驱动因素（移除后碎片化指标显著恶化），而单独使用 $\mathcal{L}_{\mathrm{MSD}}$ 或 $\mathcal{L}_{\mathrm{WR}}$ 无法消除碎片化，三者需协同作用。



## 实验与关键发现

### 1. 评估协议与碎片化度量

为系统评估所提损失函数的有效性，实验在三个标准数据集上展开：**BSDS500**（训练与测试）、**NYUv2** 和 **Pascal VOC 2012**（泛化测试）。所有深度超像素模型（**SCN** Yang et al., CVPR 2020；**AINet** Wang et al., ICCV 2021；**CDS** Xu et al., AAAI 2024；**SSM** Jia et al., IEEE SPL 2025）均采用统一的训练设置与超像素数量范围（384–1200），确保公平对比。

除标准指标（ASA、CO、BR、BP）外，本文引入两项新颖的碎片化度量，以量化超像素的空间连通性：

- **超出分量数**（Excess Components, XC）：给定超像素集合 $S$，每个超像素 $s$ 被分解为 $T_s$ 个不相交的连通子分量 $c_t^s$，满足 $\bigcup_{t=1}^{T_s} c_t^s = s$ 且 $c_t^s \cap c_{t'}^s = \emptyset$（$t \neq t'$）。则 $$\mathrm{XC}(S) = \sum_{s \in S} (T_s - 1)$$ 度量了所有超像素中除最大分量外的额外碎片总数。
- **游离像素数**（Stray Pixels, Stray）：$$\mathrm{Stray}(S) = \sum_{s \in S} | s \setminus c_{\max}^s |$$ 统计不属于各超像素最大连通分量的像素总数。

为消除超像素数量变化带来的偏差，所有指标均在固定范围 $[n_{\min}, n_{\max}]$ 内计算归一化曲线下面积（AUC），如 $\mathrm{ASA}_{\mathrm{AUC}} = \frac{1}{n_{\max} - n_{\min}} \int_{n_{\min}}^{n_{\max}} \mathrm{ASA}(n) \, dn$。

### 2. 主实验结果

#### 2.1 标准指标评估（有 EC 后处理）

Figure 2 展示了在 BSDS500 和 NYUv2 上使用强制连通性（EC）后处理的标准指标曲线。核心结论如下：

![[assets/figures/papers/paper_list_l2118_https_openaccess_thecvf_com_content_CVPR2026_html_Juybari_Differentiable/figures/004_Figure_2.jpg]]
*Figure 2: Standard metrics with enforced connectivity (EC). Top row: BSDS500 test set; bottom row: NYUv2. Columns (left→right): ASA, CO, and BR–BP. Baselines are plotted with star markers—SCN (blue), AINet (green), CDS (red), SSM (brown), SIN(orange) and SLIC (black). Laplacian variants use the same color with a diamond (⋄) marker (not applicable to SLIC and SIN). Laplacian variant models out perform their counterparts on CO and BR with minimal impact on ASA and BP*

- **紧凑度（CO）与边界召回率（BR）显著提升**：在所有架构（SCN、AINet、CDS、SSM）上，添加拉普拉斯损失（LAP）的变体在 CO 和 BR 上均超越对应基线，且对 ASA 和 BP 的影响极小。
- **跨数据集一致性**：BSDS500 与 NYUv2 上的趋势高度一致，表明 LAP 正则化的增益不依赖于特定数据分布。

#### 2.2 标准指标评估（无 EC 后处理）

Figure 3 展示了移除 EC 后的标准指标对比。此时基线模型因碎片化严重导致性能骤降，而 LAP 变体仍保持明显优势：

![[assets/figures/papers/paper_list_l2118_https_openaccess_thecvf_com_content_CVPR2026_html_Juybari_Differentiable/figures/007_Figure_3.jpg]]
*Figure 3: Standard metrics without enforced connectivity (EC). Top row: BSDS500 test set; bottom row: NYUv2. Columns (left→right): ASA, CO, and BR–BP. Baselines are plotted with star markers—SCN (blue), AINet (green), CDS (red), SSM (brown), SIN (orange); Laplacian variants use the same color with a diamond (⋄) marker (not applicable to SIN). Laplacian variant models without EC out perform their counterparts on CO and BR with minimal impact on ASA and BP*

- **无 EC 条件下 CO 和 BR 的领先幅度更大**：LAP 变体在无 EC 时对 CO 和 BR 的提升幅度甚至超过有 EC 场景，证明 LAP 损失在训练阶段已内化了空间连通性约束。
- **ASA 和 BP 保持稳定**：即使在无 EC 的严格条件下，LAP 变体的 ASA 和 BP 仍与基线持平或仅有微小下降，未出现连通性-精度之间的剧烈权衡。

#### 2.3 碎片化指标评估

Figure 4 的碎片化指标直接量化了 LAP 损失对连通性的改善效果。关键证据：

![[assets/figures/papers/paper_list_l2118_https_openaccess_thecvf_com_content_CVPR2026_html_Juybari_Differentiable/figures/008_Figure_4.jpg]]
*Figure 4: Fragmentation metrics without enforced connectivity (EC). Top row: BSDS500; bottom row: NYUv2. Columns (left→right): average excess components counts*

- **超出分量数（XC_avg）降低数倍至数十倍**：在 BSDS500 和 NYUv2 上，所有 LAP 变体的平均超出分量数均显著低于对应基线。例如，CDS-LAP 的 XC_avg 仅为 CDS 的约 1/5–1/10。
- **游离像素数（Stray_avg）同步下降**：LAP 变体的游离像素数同样大幅减少，表明碎片不仅数量少，且碎片规模小。
- **跨架构泛化**：SCN、AINet、CDS、SSM 四种架构上的 LAP 变体均取得一致的碎片化改善，证实 LAP 损失是连通性提升的充分条件，与具体网络结构无关。

Table 2 以 AUC 汇总指标量化了 BSDS500 上的整体性能。在有无 EC 两种设置下，LAP 变体在 CO_AUC、B_AUC、XC_AUC 和 ST_AUC 上均取得最优或接近最优值，ASA_AUC 仅轻微下降。

![[assets/figures/papers/paper_list_l2118_https_openaccess_thecvf_com_content_CVPR2026_html_Juybari_Differentiable/figures/009_Table_2.jpg]]
*Table 2: Quantitative performance on BSDS500. All results use 384–1200 superpixels. The best value in each EC setting is bolded. Models trained with the graph-Laplacian (LAP) loss produce higher-quality superpixels with minimal impact on ASA*

### 3. 消融实验

Table 3 的消融实验以 CDS 为基线，逐一分析三个损失项的贡献：

![[assets/figures/papers/paper_list_l2118_https_openaccess_thecvf_com_content_CVPR2026_html_Juybari_Differentiable/figures/013_Table_3.jpg]]
*Table 3: Ablation study. Adding LLAP improves COAUC, BAUC, and*

- **LAP 是连通性的核心驱动力**：单独添加 LAP 损失（CDS + LAP）即可显著改善 CO_AUC、B_AUC 和 XC_AUC，对 ASA_AUC 的影响极小。移除 LAP 后，CO_AUC、B_AUC 和 XC_AUC 均严重恶化，ASA_AUC 仅轻微上升，反向验证了 LAP 的不可替代性。
- **MSD 与 WR 的独立效果有限**：单独使用 MSD 或 WR 损失无法降低碎片化指标，必须与 LAP 组合才能发挥协同作用。MSD 主要贡献于边界精度，WR 则通过聚焦混合块提升边界区域的分配质量。
- **三项损失组合达到最优**：CDS + LAP + MSD + WR 在所有指标上取得最佳或接近最佳结果，验证了损失函数设计的互补性。

### 4. 参数敏感性分析

Table 1 和 Figure 5 系统研究了拉普拉斯损失权重 $\lambda_{\mathrm{LAP}}$ 的影响：

![[assets/figures/papers/paper_list_l2118_https_openaccess_thecvf_com_content_CVPR2026_html_Juybari_Differentiable/figures/011_Table_1.jpg]]
*Table 1: Laplacian Weight Study. Increasing λLAP improves all measurements of superpixel quality at a minor expense to ASA*

![[assets/figures/papers/paper_list_l2118_https_openaccess_thecvf_com_content_CVPR2026_html_Juybari_Differentiable/figures/010_Figure_5.jpg]]
*Figure 5: A CDS-LAP model was trained on the BSDS500 dataset for each*

- **$\lambda_{\mathrm{LAP}}$ 增大持续抑制碎片化**：随着 $\lambda_{\mathrm{LAP}}$ 从 0 增至 2880，XC 指标单调下降。在 $\lambda_{\mathrm{LAP}} = 2880$ 时，约半数测试图像的超出分量数接近零（XC ≤ 15），而 ASA 在超像素数量 n=384 时仍保持在 0.964。
- **ASA 存在可控的轻微衰减**：增大 $\lambda_{\mathrm{LAP}}$ 虽导致 ASA 略有下降，但降幅极小（例如从 0.967 降至 0.964），在实际应用中可通过权衡选择适当的权重值。
- **超参数推荐值**：论文默认采用 $\lambda_{\mathrm{LAP}} = 360$，$\lambda_{\mathrm{MSD}} = 10^{-3}$，$\lambda_{\mathrm{WR}} = 1$，该设置在连通性改善与 ASA 保持之间取得良好平衡。

### 5. 定性分析

Figure 1 和 Figure 6 提供了可视化证据：

![[assets/figures/papers/paper_list_l2118_https_openaccess_thecvf_com_content_CVPR2026_html_Juybari_Differentiable/figures/012_Figure_6.jpg]]
*Figure 6: Qualitative comparison on BSDS500 (top two rows) and NYUv2 (bottom two rows). For each dataset, the first row shows the input image followed by outputs with enforced connectivity (EC) for: AINet, AINet-LAP, CDS, CDS-LAP, SSM, SSM-LAP. The second row shows the ground-truth labels followed by the corresponding outputs without EC. Colored boxes (red/green/blue) highlight regions where EC relabels fragmented components and where boundary irregularities are reduced; training with the proposed graph-Laplacian (LAP) loss yields more compact, connected superpixels and fewer label changes under EC*

- **无 EC 条件下的连通性对比**：Figure 1 以 CDS 为例，展示 LAP 正则化使超像素在无 EC 时即呈现紧凑、连通的结构，而基线 CDS 输出大量碎片化区域，需依赖 EC 后处理强制合并。
- **边界精度与紧凑性**：Figure 6 的高亮框区域显示，LAP 变体在有 EC 和无 EC 条件下均产生更规则的边界，且 EC 对 LAP 输出的重标记区域显著少于基线，间接证明 LAP 已内化了大部分连通性约束。
- **跨数据集可视化**：BSDS500 和 NYUv2 的定性结果均支持定量结论，LAP 变体的超像素在紧凑度、边界贴合度和连通性上全面优于基线。

### 6. 失败模式与局限性

尽管 LAP 损失大幅改善了连通性，仍存在以下局限：

- **EC 尚未完全可替代**：在极端情况下（如高度纹理化区域或细长结构），LAP 变体仍可能产生少量不连通分量，需借助 EC 后处理清理。Figure 4 中 LAP 变体的 XC_avg 虽大幅降低，但未达到零。
- **ASA 与连通性的权衡**：增大 $\lambda_{\mathrm{LAP}}$ 可进一步降低碎片化，但 ASA 会轻微下降，需在应用中根据需求调整。
- **网格约束的固有限制**：方法依赖固定的 16×16 网格划分和 3×3 局部搜索窗，可能限制超像素形状对非规则纹理或细长物体的适应性。
- **下游任务验证缺失**：当前评估仅聚焦超像素分割本身，未在实例分割、目标检测等下游任务中验证端到端联合优化的实际增益。



## 定位与知识库关联

### 一、方法在超像素分割谱系中的位置

超像素分割方法大致可划分为**传统优化方法**与**深度学习时代的方法**两个阶段，而深度学习时代内部又可进一步分为依赖不可微后处理的“两阶段”范式与追求端到端可微的“一体化”范式。本文工作处于后一范式的核心交汇点上。

**传统方法**以 **SLIC**（Achanta et al., TPAMI 2012）为代表，通过迭代聚类生成超像素，天然无需后处理即可保持连通性，但其边界精度和紧凑度受限于手工设计的特征空间。SLIC 在本文中被用作评价参考基线，其性能天花板在深度学习方法面前已显不足。

**深度学习超像素方法**自 **SCN**（Yang et al., CVPR 2020）起进入快速发展期。SCN 首次将超像素分割建模为可微的像素-超像素软分配问题，但其输出的分配概率图天然存在碎片化——单个超像素往往分裂为多个空间不连通的分量。这一问题在后续的 **AINet**（Wang et al., ICCV 2021）、**CDS**（Xu et al., AAAI 2024）和 **SSM**（Jia et al., IEEE SPL 2025）等工作中持续存在。这些方法的共同应对策略是：在推理阶段强制施加**不可微的强制连通性后处理（Enforced Connectivity, EC）**，将碎片化的像素重新分配给最近的主分量。EC 虽然修复了连通性，但切断了从下游任务到超像素分配网络的梯度回传路径，使得端到端联合优化成为不可能。

**专用连通架构**方向中，**SIN**（Yuan et al., PRICAI 2021）尝试通过内置的连通性约束来绕开 EC，但其精度显著低于同期方法，表明“硬编码”连通性会牺牲超像素的边界贴合能力。

本文的定位是：**不改变网络架构，而是通过可微损失函数从根本上抑制碎片化的产生**。具体而言，所提的图拉普拉斯损失（Graph-Laplacian Loss）作为即插即用的正则化项，可直接嵌入 SCN、AINet、CDS、SSM 等现有架构，使它们在无需 EC 的情况下输出连通、紧凑的超像素，同时保持端到端可微性。这一思路填补了“可微连通性约束”在超像素损失函数中的空白。

### 二、与基线方法的关系与增量贡献

本文并非提出新的超像素分割网络，而是提出一套**通用的、与架构无关的可微损失函数族**。其与各基线的关系如下：

| 基线方法 | 原始问题 | 本文贡献 | 增量效果 |
|---------|---------|---------|---------|
| **SCN** (Yang et al., CVPR 2020) | 输出碎片化，依赖 EC | 叠加 L_LAP + L_MSD + L_WR | CO 和 BR 显著提升，碎片化指标（XC、Stray）降低数倍 |
| **AINet** (Wang et al., ICCV 2021) | 同上 | 同上 | 同上 |
| **CDS** (Xu et al., AAAI 2024) | 同上 | 同上 | 同上；消融实验证实 LAP 是连通性提升的主要驱动力 |
| **SSM** (Jia et al., IEEE SPL 2025) | 同上 | 同上 | 同上 |
| **SIN** (Yuan et al., PRICAI 2021) | 内置连通性但精度低 | 不适用（架构不同） | 本文方法在精度上远超 SIN，同时无需牺牲可微性 |

核心增量可归纳为三点：

1. **连通性可微化**：首次将超像素的空间连通性形式化为图拉普拉斯矩阵迹的最大化问题，使得连通性约束成为梯度可回传的训练目标，而非推理阶段的硬性后处理。

2. **语义边界增强**：最小语义距离损失（L_MSD）通过最大化不同语义类别像素嵌入间的最小距离，显式引导超像素边界与语义边界对齐，这是基线方法所不具备的。

3. **边界聚焦重建**：加权重建损失（L_WR）以 10:1 的权重比强调混合类块（即包含多个语义类别的边界区域），使模型将容量集中于最难分的边界像素，而非均匀对待所有像素。

消融实验（Table 3）给出了清晰的因果链：单独使用 MSD 或 WR 损失无法降低碎片化，必须与 LAP 结合才能有效改善连通性；移除 LAP 损失会导致 CO_AUC、B_AUC 和 XC_AUC 显著恶化，而 ASA_AUC 仅轻微上升，证实 LAP 是连通性提升的**唯一关键驱动因素**。

### 三、适用边界与局限

尽管所提损失函数在多个架构和数据集上表现出一致的增益，但其适用边界和局限同样值得关注：

1. **连通性-精度权衡**：增大 λ_LAP 可进一步降低超出分量数（XC），但 ASA 会略有下降（Figure 5, Table 1）。在 λ_LAP=2880 时，约半数测试图像的 XC 接近零，但 ASA 从 0.968 降至 0.964。这一权衡意味着在实际部署中需根据下游任务对连通性与精度的相对敏感度进行调参。

2. **EC 未被完全取代**：尽管拉普拉斯变体在碎片化指标上相比基线降低了数倍至数十倍（Figure 4），但在某些极端情况下，模型输出的超像素仍存在少量不连通分量，需借助 EC 清理。论文坦承“所提损失仍未能完全取代不可微的 EC 后处理”，这是该方法的当前能力边界。

3. **网格约束的刚性**：方法依赖于固定的 16×16 网格划分和 3×3 局部搜索窗来构建超像素候选集。这种刚性约束简化了图构建和计算，但也限制了超像素形状的灵活性，可能不适用于需要非规则区域划分的场景。

4. **验证范围有限**：实验仅在主流深度超像素模型（SCN、AINet、CDS、SSM）和标准分割数据集（BSDS500、NYUv2）上进行，未在更广泛的下游任务（如实例分割、目标检测、视频目标跟踪）中验证端到端联合优化的实际增益。这是一个重要的验证缺口。

5. **超参数敏感性**：λ_LAP、λ_MSD、λ_WR 三个超参数需要手动设定（论文使用 λ_LAP=360, λ_MSD=10⁻³, λ_WR=1），其对不同架构和数据集的最优值可能不同，缺乏自适应调整机制。

### 四、开放问题

本文开启了一系列值得进一步探索的方向：

1. **架构层面的连通性保证**：当前方法将连通性约束施加于损失函数层面。一个自然的问题是：能否将图拉普拉斯正则化直接嵌入到网络架构设计中（例如通过消息传递或图卷积结构），从根本上杜绝碎片化的产生？这将是“一体化”范式的终极形态。

2. **连通性的理论保证**：图拉普拉斯迹最大化在多大程度上能保证超像素的全连通？是否存在一个可证明的连通性阈值——当迹超过某临界值时，超像素必然连通？目前论文仅提供了经验证据，理论分析尚属空白。

3. **超参数的自适应学习**：λ_LAP、λ_MSD、λ_WR 能否与下游任务联合学习，实现任务驱动的自适应调整？例如，在下游语义分割任务中，λ_LAP 可能需要在边界区域和均匀区域采用不同的强度。

4. **高效图构建**：当前的图构建基于 3×3 局部搜索窗，对于高分辨率图像或大规模超像素场景，计算开销可能成为瓶颈。能否设计更高效的图构建方式（如稀疏图、层次图）以支持更大规模的应用？

5. **跨任务迁移**：所提损失函数在其他视觉任务中是否能提供端到端的区域级表示？例如，在实例分割中，连通性约束可能有助于生成完整的实例掩码；在目标检测中，紧凑的超像素可能作为高质量的候选区域。这些跨任务迁移的潜力尚未被验证。

6. **与视觉基础模型的结合**：随着 SAM、DINOv2 等视觉基础模型的兴起，超像素分割能否作为这些模型的下游适配层？图拉普拉斯损失的可微性使其天然适合与基础模型的嵌入空间进行联合微调，这可能开辟超像素在交互式分割和开放词汇场景中的新应用。



## 原文 PDF

![[paperPDFs/CVPR_2026/Differentiable_Laplacian_Matrix_Guided_Superpixel_Segmentation.pdf]]
