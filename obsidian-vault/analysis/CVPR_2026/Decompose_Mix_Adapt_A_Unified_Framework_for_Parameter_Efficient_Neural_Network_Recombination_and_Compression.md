---
title: "Decompose, Mix, Adapt: A Unified Framework for Parameter-Efficient Neural Network Recombination and Compression"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/Decompose_Mix_Adapt_A_Unified_Framework_for_Parameter_Efficient_Neural_Network_Recombination_and_Compression.pdf
project_link: null
code_link: "https://github.com/appledora/CRISP-CVPR26"
aliases:
- CCGWRBISBP
- DMAUFPENNRC
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
- topic/benchmarks_datasets_evaluation
core_operator: 混合矩阵的列维度s和sigmoid门控机制。s直接控制共享基矩阵的容量，相较于行维度r是性能的主要驱动因素；门控机制提供了内置正则化，避免过拟合且无需额外超参数。
primary_logic: 通过将预训练权重分解为共享基矩阵和可与基矩阵交互的、灵活维度的门控混合矩阵，可以在同一个因子化结构中同时实现模型压缩（调整基矩阵大小和共享层数）和高效微调（仅更新轻量级混合矩阵），且性能显著优于分别使用独立压缩与微调方法的组合。
claims:
- CRISP在VTAB-1K上以59.2%的总体准确率超越所有PEFT基线，同时参数用量减少28%。
- CRISP在ViT-B/16 50%压缩设定下平均准确率达83.3%，仅使用2% ImageNet-1K进行蒸馏，优于使用全量数据的DGMR等基线。
- 消融中sigmoid门控(PRE-SiLU)在所有基准上均优于后置和模板约束，而ReLU因过度稀疏化导致性能灾难性下降。
- VTAB-1K (19 tasks) 上 Overall Accuracy = 59.2
---

# Decompose, Mix, Adapt: A Unified Framework for Parameter-Efficient Neural Network Recombination and Compression

> [!tip] 核心洞察
> 通过将预训练权重分解为共享基矩阵和可与基矩阵交互的、灵活维度的门控混合矩阵，可以在同一个因子化结构中同时实现模型压缩（调整基矩阵大小和共享层数）和高效微调（仅更新轻量级混合矩阵），且性能显著优于分别使用独立压缩与微调方法的组合。

| 字段 | 内容 |
|------|------|
| 中文题名 | 分解、混合、适配：参数高效神经网络重组与压缩的统一框架 |
| 英文题名 | Decompose, Mix, Adapt: A Unified Framework for Parameter-Efficient Neural Network Recombination and Compression |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2603.27383) · [Code](https://github.com/appledora/CRISP-CVPR26) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction #topic/benchmarks_datasets_evaluation |
| Method | CRISP (Coefficient-gated weight Recombination by Interpolated Shared basis Projections) |
| Dataset | VTAB-1K, ViT-B/16 50% compression on 6 fine-grained benchmarks, ViT-B/16 50% compression + PEFT on 6 benchmarks, LLaMA3.2-1B 30% compression on 7 commonsense reasoning benchmarks |

> [!tip] 效果简介
> - VTAB-1K (19 tasks) 上，Overall Accuracy 59.2 vs 57.8 (SSF, previous SOTA) (+1.5% (stated) / +1.4% (observed))。
> - ViT-B/16 50% compression on 6 fine-grained benchmarks 上，Average Accuracy (Compressed Only) 83.3 vs 81.9 (DGMR) (+1.4%)。
> - ViT-B/16 50% compression + PEFT on 6 benchmarks 上，Average Accuracy (Compressed + PEFT) 88.8 vs 87.9 (DGMR+SSF) (+0.9%)。

## 概要

现有参数重组（Parameter Recombination, PR）方法通常将模型压缩（MC）与参数高效微调（PEFT）视为两个独立问题，分别设计专用技术，缺乏统一框架来动态平衡两者的参数预算。例如，**RECAST**（Tasnim & Plummer, ICLR 2025）虽同时支持MC和PEFT，但其混合系数被限制为向量形式，严重制约了表达力，导致在更大参数预算下性能饱和。

CRISP（Coefficient-gated weight Recombination by Interpolated Shared basis Projections）通过一个核心洞察统一了这两种任务：**将预训练权重分解为共享的基矩阵和可与基矩阵交互的、灵活维度的门控混合矩阵**。在这一因子化结构下，调整基矩阵大小和共享层数即可实现模型压缩，而冻结基矩阵、仅更新轻量级混合矩阵即可完成高效微调——两种应用共存于同一框架，无需冗余适配器。

方法的关键调控旋钮是混合矩阵的**列维度 s**和**sigmoid门控机制**。s 直接控制共享基矩阵的容量，是性能的主要驱动因素；门控机制则提供内置正则化，避免过拟合且无需额外超参数。

主要实证结论如下：

- **PEFT性能**：在VTAB-1K的19个任务上，CRISP以59.2%的总体准确率超越所有PEFT基线（此前最优SSF为57.8%），同时参数用量减少28%（Table 1）。
- **模型压缩**：在ViT-B/16 50%压缩设定下，CRISP平均准确率达83.3%，仅使用2%的ImageNet-1K数据进行蒸馏，优于使用全量数据的DGMR等基线（Table 2 Upper）。
- **压缩+微调联合**：同等压缩率下，CRISP压缩后微调平均准确率达88.8%，优于最优剪枝+PEFT组合约1个百分点（Table 2 Lower）。
- **跨架构泛化**：在LLaMA3.2-1B 30%压缩的7个常识推理基准上，CRISP平均准确率38.0%，较先前工作PruneNet（34.9%）高出3.1%（Table 3）。

消融实验进一步揭示：sigmoid门控（SiLU）在所有基准上均优于后置和模板约束，而ReLU因过度稀疏化导致性能灾难性下降；列维度 s 是容量控制的主导因子，固定 s 仅增加行维度 r 反而导致准确率崩溃。

当前方法已在ViT和LLaMA架构上验证，尚未扩展到CNN或大视觉语言模型等更广泛架构，超参数 r 和 s 仍需手动设置，缺乏自动化选择机制。代码已开源：https://github.com/appledora/CRISP-CVPR26。



### 参数重组的两难困境

现代深度学习模型在部署时面临两个核心需求：一是**模型压缩**（Model Compression, MC），以降低存储和推理开销；二是**参数高效微调**（Parameter-Efficient Fine-Tuning, PEFT），以低成本将预训练模型适配到下游任务。参数重组（Parameter Recombination, PR）方法——即通过定义变换 $\mathcal{T}$ 从可训练参数 $\theta_i$ 生成权重 $W_i = \mathcal{T}(\theta_i)$——为这两类需求提供了统一的技术路径。

然而，现有PR工作存在一个根本性的分裂：它们通常**分别为MC或PEFT单独设计**，而非在统一框架内动态平衡两者。如Figure 1所示，LoRA等PEFT方法专注于通过低秩适配器微调，而Basis Sharing等MC方法则通过跨层参数共享压缩模型。当需要同时压缩和微调时，实践者不得不将两种独立方法组合使用（如DGMR+SSF），这不仅引入了冗余的适配器参数，还导致压缩质量与下游适应能力之间的次优权衡。

### 现有方法的表达力瓶颈

在少数支持双任务的PR方法中，**RECAST**（Tasnim & Plummer, ICLR 2025）是最接近CRISP的前驱工作。RECAST通过平均 $K$ 个系数向量生成权重：

$$\mathcal{T}_{\mathrm{RECAST}}(B_i^{*r}, a_{i,j}^{r}) = \frac{1}{K} \sum_{j=1}^{K} B_i^{*r} a_{i,j}^{r}$$

然而，RECAST将混合系数限制为**向量**（大小为 $r$），这严重限制了其表达力。当参数预算增大时，单纯增加向量维度无法有效扩展模型容量，导致**性能饱和**——这是RECAST在更大规模任务上表现受限的核心原因。

### 统一框架的核心动机

CRISP的出发点在于一个关键洞察：如果能将预训练权重分解为**共享基矩阵**和**可与基矩阵交互的灵活维度混合矩阵**，那么：

- **压缩**可通过调整基矩阵的大小和共享层数实现；
- **微调**可通过冻结基矩阵、仅更新轻量级混合矩阵实现。

两者共享同一因子化结构，无需额外的适配器模块。这种统一设计使得参数预算可以在压缩与适应之间无缝流动，从根本上解决了现有方法“分而治之”带来的效率损失。CRISP通过引入**可配置列维度 $s$ 的混合矩阵**和**sigmoid门控机制**，突破了RECAST的向量约束瓶颈，为统一PR框架建立了新的容量-效率控制维度。



## 核心方法与创新机理

### 1. 从向量到矩阵：混合系数维度的根本性扩展

CRISP对参数重组（Parameter Recombination, PR）框架的核心改造在于将混合系数的表达形式从**向量提升为矩阵**。在最近的统一PR工作**RECAST**（Tasnim & Plummer, ICLR 2025）中，混合系数被限制为一个大小为r的向量，即每一层的权重由共享基矩阵与一个系数向量的线性组合生成。这种设计在参数预算增大时遭遇严重的表达力瓶颈——向量维度r的增加无法有效转化为模型容量的提升，导致性能饱和。

CRISP引入了一个全新的超参数**s**，将混合矩阵显式定义为 $A_i'^{rs} \in \mathbb{R}^{r \times s}$。这一改动并非简单的维度扩充，而是从根本上重构了基矩阵与混合系数之间的交互方式：
- **基矩阵形状自适应调整**：为保持总参数量可控，基矩阵从RECAST中的 $B \in \mathbb{R}^{d_{in} \cdot d_{out} \times r}$ 调整为 $B_i'^r \in \mathbb{R}^{u \times r}$，其中 $u = (d_{in} \cdot d_{out}) / s$。这意味着基矩阵的每一行不再对应原始权重矩阵的单个元素，而是对应s个元素的聚合表示。
- **列维度s成为容量主控旋钮**：消融实验（Figure 5）揭示了关键因果机制——固定列数s=16时单纯增加行数r反而导致准确率崩溃，而固定行数r=16时增加列数s则持续恢复并提升性能。这证实了**基矩阵容量（由列数s决定）是维持模型质量的主导因素**，而系数表达力（由行数r决定）扮演辅助角色。这一发现直接解释了为何RECAST的向量设计在扩展性上存在根本缺陷。

### 2. Sigmoid门控：内置正则化与非线性表达

CRISP的第二个关键创新是在混合矩阵上施加**逐元素sigmoid门控**，将权重重参数化变换定义为：

$$\mathcal{T}_{\mathrm{CRISP}}(B_i'^r, A_i'^{rs}) = B_i'^r \left( \sigma(A_i'^{rs}) \odot A_i'^{rs} \right)$$

其中 $\sigma(\cdot)$ 为sigmoid函数，$\odot$ 表示逐元素乘法。这一设计与RECAST的纯线性组合形成鲜明对比，带来双重收益：

- **内置正则化机制**：sigmoid函数将混合系数压缩至(0,1)区间，天然限制了权重的增长幅度。消融实验（Table 4）表明，SiLU门控（82.2%平均准确率）在无需额外超参数的情况下，优于显式权重衰减、dropout等传统正则化策略。这种“免费”的正则化是CRISP在极低参数预算下避免过拟合的关键。
- **非线性表达增强**：门控操作引入了非线性变换，使混合矩阵能够学习更复杂的基向量组合模式。Figure 6的放置位置消融进一步揭示了一个关键设计选择：**前置门控（PRE）**——即在混合矩阵与基矩阵相乘之前施加门控——在所有基准上一致优于后置（POST）和模板约束（TEMP）方案。特别值得注意的是，使用ReLU替代sigmoid会导致**灾难性的性能退化**，原因是ReLU的硬稀疏化会大量置零混合系数，破坏基向量的有效组合。

### 3. 统一框架内的双模式切换

前述两项创新共同支撑了CRISP最核心的架构贡献：**在单一因子化结构内同时支持模型压缩（MC）和参数高效微调（PEFT）两种模式**，而无需引入冗余适配器或独立的压缩模块。

这一统一性的实现依赖于对基矩阵和混合矩阵角色的清晰分离：
- **压缩模式**：通过跨层共享基矩阵并减小其尺寸来控制模型容量。基矩阵在压缩阶段通过神经拟态初始化（Neural Mimicry）从预训练权重中学习，随后冻结。
- **微调模式**：在基矩阵冻结的前提下，仅更新轻量级的门控混合矩阵 $A_i'^{rs}$ 以适应下游任务。由于混合矩阵的参数量远小于原始权重（在VTAB-1K实验中仅占基础模型的 $5 \times 10^{-3}\%$），微调极为高效。

这一设计与现有方法形成根本差异：此前的工作要么专注于PEFT（如**LoRA**、**SSF**、**DoRA**），要么专注于MC（如**Basis Sharing**、**DGMR**），即便RECAST声称同时支持两者，也因向量混合系数的表达力限制而无法在压缩后保持足够的微调潜力。CRISP的矩阵门控设计使得压缩后的模型仍保留丰富的可调自由度，这直接体现在**压缩+PEFT联合场景**中——CRISP在ViT-B/16 50%压缩设定下以88.8%的平均准确率超越最佳剪枝+PEFT组合（DGMR+SSF的87.9%）约1个百分点，验证了“压缩质量直接约束下游任务适应性”的核心论断。



CRISP 围绕一个统一的因子化结构构建，该结构将预训练权重矩阵分解为**冻结的共享基矩阵（Basis Matrices）**和**可学习的门控混合矩阵（Gated Mixer Matrices）**，使模型压缩（MC）和参数高效微调（PEFT）得以在同一框架内共存，无需额外的冗余适配器。

### 核心变换

框架的核心是一个参数化变换 $\mathcal{T}_{\mathrm{CRISP}}$，它从基矩阵 $B_i^{\prime r} \in \mathbb{R}^{u \times r}$ 和混合矩阵 $A_i^{\prime rs} \in \mathbb{R}^{r \times s}$ 生成第 $i$ 层的权重矩阵：

$$\mathcal{T}_{\mathrm{CRISP}}(B_i^{\prime r}, A_i^{\prime rs}) = B_i^{\prime r} \left( \sigma(A_i^{\prime rs}) \odot A_i^{\prime rs} \right)$$

其中 $\sigma(\cdot)$ 为逐元素 sigmoid 门控，$\odot$ 表示逐元素乘法，$u = d_{\mathrm{in}} \cdot d_{\mathrm{out}} / s$。这一设计的两个关键创新直接回应了现有方法的瓶颈：

1. **矩阵形式的混合系数**：相较于 RECAST（Tasnim & Plummer, ICLR 2025）将混合系数限制为向量，CRISP 引入超参数 $s$ 控制混合矩阵的列维度，显著提升了表达力，使模型在更大参数预算下不会出现性能饱和。
2. **内置 sigmoid 门控**：对混合矩阵施加 $\sigma(A) \odot A$ 的非线性约束，提供天然正则化，避免过拟合而无需额外的权重衰减等超参数。消融实验证实，SiLU 风格的门控在所有基准上均优于无约束和后置约束方案，而 ReLU 因过度稀疏化导致性能灾难性下降（Figure 6）。

### 流程模块

CRISP 的完整 pipeline 由以下模块串联构成：

**1. 神经拟态初始化（Neural Mimicry Initialization）**
在无数据样本的条件下，通过 smooth-L1 重构损失将预训练权重 $W_{p_i}$ 分解为基-混合器对：

$$\mathcal{L}_{\mathrm{mimicry}} = \sum_{i=1}^{N} \ell_{\mathrm{smL1}} \left( \mathcal{T}_{\mathrm{CRISP}}(B_i^{\prime r}, A_i^{\prime rs}) - W_{p_i} \right)$$

该阶段仅需不到一分钟（ViT）或三十分钟（LLaMA）即可在单 GPU 上完成，为后续压缩或微调提供初始化。

**2. 模型压缩（MC）**
通过两种机制控制模型容量：**减小基矩阵大小**和**跨层共享基矩阵**。压缩后的模型保持 CRISP 的因子化结构，基矩阵被冻结，仅分类头可训练。对于 ViT，采用多阶段蒸馏策略——以全参数 CRISP 教师模型引导压缩学生模型，使用 KL 散度和 MSE 损失对齐 logits 与特征，且仅需 2% 的 ImageNet-1K 数据。对于 LLaMA，则采用无数据的基向量重要性加权 k-means 聚类与方差感知合并。

**3. 参数高效微调（PEFT）**
冻结基矩阵，仅更新轻量级的门控混合矩阵 $A_i^{\prime rs}$ 和任务头。由于混合矩阵参数量极小（可低至基模型的 $5 \times 10^{-3}\%$），微调极为高效，同时训练吞吐量（163 samp/s）和推理吞吐量（657 samp/s）与 LoRA 等方法持平（Table 5）。

**4. 联合 MC+PEFT**
先执行压缩获得紧凑的基矩阵，再冻结基矩阵并微调混合矩阵以适应下游任务。整个流程在统一的因子化结构内完成，无需像传统方法那样分别部署独立的压缩模块和 PEFT 适配器。

### 输入输出流

- **输入**：预训练模型权重 $W_p = \{W_{p_1}, \ldots, W_{p_N}\}$
- **神经拟态**：输出初始化的基矩阵 $\{B_i^{\prime r}\}$ 和混合矩阵 $\{A_i^{\prime rs}\}$
- **压缩路径**：通过减小 $r$ 和/或跨层共享 $B$ 降低参数量 → 输出压缩模型
- **微调路径**：冻结 $B$，仅更新 $A^{\prime rs}$ → 输出适应下游任务的模型
- **联合路径**：压缩 → 冻结 $B$ → 微调 $A^{\prime rs}$ → 输出压缩且适配的模型

这一设计使得调整基矩阵的共享模式和大小即可控制压缩程度，而冻结基矩阵并更新混合矩阵即可实现微调，两者共享同一套参数化基础设施，从根本上消除了 MC 与 PEFT 之间的方法割裂。



CRISP的核心思想是将预训练权重矩阵分解为**冻结的共享基矩阵（Factorized Basis Matrices）**与**可学习的门控混合矩阵（Gated Mixer Matrices）**，通过参数化变换在同一因子化结构中统一支持模型压缩（MC）和参数高效微调（PEFT）。以下从公式推导出发，逐模块解析其设计逻辑。

### 3.1 从LoRA到CRISP：参数重组公式的演化

参数重组（PR）方法的核心是定义一个变换 $\mathcal{T}$，从可训练参数 $\theta_i$ 生成第 $i$ 层的权重矩阵 $W_i \in \mathbb{R}^{d_{\mathrm{out}} \times d_{\mathrm{in}}}$：

$$W_i = \mathcal{T}(\theta_i)$$

**LoRA**（低秩适配）将可训练参数分解为低秩矩阵 $B_i^r \in \mathbb{R}^{d_{\mathrm{out}} \times r}$ 和 $A_i^r \in \mathbb{R}^{r \times d_{\mathrm{in}}}$，并与冻结的预训练权重 $W_{p_i}$ 相加：

$$\mathcal{T}_{\mathrm{LoRA}}(B_i^r, A_i^r) = B_i^r A_i^r + W_{p_i} \tag{1}$$

LoRA专为PEFT设计，无法直接用于模型压缩，因为其变换始终保留完整预训练权重。

**Basis Sharing**（跨层参数共享）则去掉预训练权重项，直接使用低秩分解进行压缩：

$$\mathcal{T}_{\mathrm{BasisSharing}}(B_i^r, A_i^r) = B_i^r A_i^r \tag{2}$$

该方法仅支持MC，缺乏对下游任务微调的内置支持。

**RECAST**（Tasnim & Plummer, ICLR 2025）尝试统一两者，引入共享基矩阵 $B_i^{*r}$ 和 $K$ 个系数向量 $a_{i,j}^r$，通过平均生成权重：

$$\mathcal{T}_{\mathrm{RECAST}}(B_i^{*r}, a_{i,j}^r) = \frac{1}{K} \sum_{j=1}^{K} B_i^{*r} a_{i,j}^r \tag{3}$$

然而RECAST将混合系数限制为向量形式，表达能力受限，在较大参数预算下性能趋于饱和。

### 3.2 CRISP核心变换：系数门控混合

CRISP的关键创新在于引入**列维度 $s$** 和**sigmoid门控机制**，将混合系数从向量扩展为矩阵 $A_i^{\prime rs} \in \mathbb{R}^{r \times s}$，并相应地调整基矩阵形状为 $B_i^{\prime r} \in \mathbb{R}^{u \times r}$，其中 $u = d_{\mathrm{out}} \cdot d_{\mathrm{in}} / s$。CRISP变换定义为：

$$\mathcal{T}_{\mathrm{CRISP}}(B_i^{\prime r}, A_i^{\prime rs}) = B_i^{\prime r} \left( \sigma(A_i^{\prime rs}) \odot A_i^{\prime rs} \right) \tag{4}$$

其中 $\sigma(\cdot)$ 为sigmoid函数，$\odot$ 表示逐元素乘法。

**公式变量含义：**

- $B_i^{\prime r} \in \mathbb{R}^{u \times r}$：第 $i$ 层的共享基矩阵，$r$ 为基向量的行维度（系数表达力），$u$ 由输出维度、输入维度和列维度 $s$ 共同决定。基矩阵在PEFT阶段冻结，其大小和跨层共享模式控制模型容量。
- $A_i^{\prime rs} \in \mathbb{R}^{r \times s}$：第 $i$ 层的可学习混合矩阵，$s$ 为列维度（基容量），是性能的主要驱动因素。混合矩阵在神经拟态初始化和PEFT阶段均可更新。
- $\sigma(A_i^{\prime rs}) \odot A_i^{\prime rs}$：SiLU风格的门控操作，提供内置正则化，避免过拟合且无需额外超参数。

**设计逻辑：**

1. **列维度 $s$ 作为容量控制旋钮**：消融实验（Figure 5）表明，固定 $s=16$ 时增大 $r$ 反而导致准确率崩溃；而固定 $r=16$ 时增大 $s$ 可稳定恢复性能。这说明基容量（列数）是维持模型质量的主导因素，系数表达力（行数）仅起次要作用。这一发现直接指导了CRISP在压缩与微调间的动态平衡——通过调整 $s$ 控制基矩阵大小，通过 $r$ 微调混合器表达力。

![[assets/figures/papers/paper_list_l854_https_arxiv_org_abs_2603_27383/figures/009_Figure_5.jpg]]
*Figure 5: Impact of mixer matrix dimensions on model capacity and performance. (a) Fixed columns (s = 16): Increasing rows reduces parameters but collapses accuracy. (b) Fixed rows (r = 16): Increasing columns scales capacity and recovers performance. Results across CIFAR-100, CUB-Birds, and FGVC-Aircraft demonstrate that basis capacity (columns) is the dominant factor for maintaining model quality, while coefficient expressivity (rows) plays a secondary role. Red dotted line: original model*

2. **SiLU门控作为内置正则化**：消融实验（Table 4, Figure 6）系统比较了不同正则化策略。SiLU门控（82.2%平均准确率）优于权重衰减、无约束等替代方案。关键的是，门控必须置于混合矩阵之前（PRE配置）而非之后（POST），且使用ReLU替代SiLU会导致灾难性的权重稀疏化，性能严重退化。这表明sigmoid门控的软约束特性恰好提供了适度的非线性正则化，避免了过拟合和欠稀疏化的两难困境。

![[assets/figures/papers/paper_list_l854_https_arxiv_org_abs_2603_27383/figures/011_Figure_6.jpg]]
*Figure 6: Impact of regularization constraint placement across PRE, POST, and TEMP configurations. PRE (our method) achieves the most consistent performance, while ReLU causes severe degradation due to weight sparsification*

### 3.3 神经拟态初始化：无数据权重重建

CRISP通过**神经拟态（Neural Mimicry）**将预训练权重分解为基-混合器对，整个过程无需任何训练数据样本。重建损失使用smooth-L1函数：

$$\mathcal{L}_{\mathrm{mimicry}} = \sum_{i=1}^{N} \ell_{\mathrm{smL1}} \left( \mathcal{T}_{\mathrm{CRISP}}(B_i^{\prime r}, A_i^{\prime rs}) - W_{p_i} \right) \tag{5}$$

其中 $N$ 为层数，$W_{p_i}$ 为第 $i$ 层的预训练权重。消融实验（Figure 7）证实smooth-L1在四种候选损失函数（Huber、Smooth-L1、MSE、L1）中效果最佳。该初始化过程极为高效：ViT模型在单GPU上不到一分钟即可完成，LLaMA模型也仅需不到30分钟。

![[assets/figures/papers/paper_list_l854_https_arxiv_org_abs_2603_27383/figures/014_Figure_7.jpg]]
*Figure 7: Effect of reconstruction loss functions during neural mimicry. We compare four loss functions (Huber, Smooth-L1, MSE, L1) used in the neural mimicry stage (Equation 5 of main paper) for retrofitting pretrained weights into CRISP’s basis-mixer decomposition*

### 3.4 统一框架下的MC与PEFT实现

CRISP通过同一因子化结构实现两种应用模式：

- **模型压缩（MC）**：跨层共享基矩阵并减小其尺寸（调整 $r$ 和 $s$），冻结基矩阵后仅更新分类头。对于ViT的高压缩率场景，引入多阶段蒸馏流程（Algorithm 4），使用全参数CRISP教师模型以KL散度和MSE损失指导学生模型，并结合SVD初始化，仅需2%的ImageNet-1K数据即可超越使用全量数据的DGMR等基线。
- **参数高效微调（PEFT）**：冻结基矩阵，仅更新轻量级混合矩阵 $A_i^{\prime rs}$。在VTAB-1K上，CRISP以59.2%的总体准确率超越所有PEFT基线，同时参数用量减少28%。
- **联合MC+PEFT**：先压缩后微调（Algorithm 6），压缩后的基矩阵作为下游任务初始化的骨干，仅微调混合器即可获得进一步增益。在ViT-B/16 50%压缩设定下，压缩+PEFT平均准确率达88.8%，优于最佳剪枝+PEFT组合（DGMR+SSF的87.9%）约1个百分点。

### 3.5 数据无关的基向量压缩（LLaMA专用）

对于LLaMA等大语言模型，CRISP设计了无需训练数据的基向量压缩算法（Algorithm 5）：通过重要性加权的k-means聚类对基向量进行分组，再以方差感知的方式合并聚类中心，在30%参数削减下平均准确率38.0%，较先前最优方法PruneNet提升3.1个百分点。



## 实验与关键发现

### 核心实验设计

CRISP的实验验证围绕三个维度展开：**独立PEFT性能**、**独立模型压缩（MC）性能**，以及**MC+PEFT联合性能**。实验覆盖ViT-S/16、ViT-B/16和LLaMA3.2-1B三种架构，在VTAB-1K（19任务）、细粒度分类（6基准）和常识推理（7基准）上进行评估。关键对照基线包括：PEFT方法LoRA、SSF、DoRA、RECAST（Tasnim & Plummer, ICLR 2025）；MC方法Basis Sharing、DGMR、SVD、PruneNet；以及MC+PEFT组合如DGMR+SSF。

### VTAB-1K PEFT主结果

Table 1展示了ViT-S/16在VTAB-1K上的PEFT性能。CRISP以**59.2%的总体准确率**达到最优，较先前最佳方法SSF（57.8%）提升约1.4个百分点，同时可训练参数量减少28%（$5\times10^{-3}\%$ vs. $7\times10^{-3}\%$的基础模型参数）。CRISP在Structured任务组上表现尤为突出，在多数子基准上取得最佳结果，平均领先约2个百分点。这一优势源于门控混合矩阵提供的表达能力与内置正则化的协同效应——SiLU门控在无需额外超参数的情况下抑制过拟合，而矩阵形式的混合系数（$r\times s$）相比RECAST的向量形式（$r$）提供了更丰富的基向量交互空间。

Figure 3进一步展示了不同可训练参数预算下的性能曲线。在FGVC-Aircraft、CIFAR-100和CUB-200-2011三个数据集上，CRISP在所有参数预算设定下均一致优于LoRA、SSF等基线，表明其参数效率具有跨预算的鲁棒性。

### ViT压缩主结果

Table 2（上半部分）报告了ViT-B/16在50%参数削减（86M→44M）下的压缩性能。CRISP以**83.3%的平均准确率**领先所有基线，较DGMR（81.9%）提升1.4个百分点。值得注意的是，CRISP仅使用**2%的ImageNet-1K数据**进行蒸馏训练，而DGMR等竞争方法使用全量数据集，凸显了CRISP在数据效率上的显著优势。

![[assets/figures/papers/paper_list_l854_https_arxiv_org_abs_2603_27383/figures/005_Table_2.jpg]]
*Table 2: ViT-B/16 [13] compression at 50% parameter reduction across six fine-grained benchmarks. Upper: post-compression accuracy with classifier-only adaptation; CRISP leads all baselines using only 2% of ImageNet-1K [11] for distillation. Lower: compressed backbones used as initialization for PEFT; CRISP achieves state-of-the-art, outperforming the best pruning+PEFT combination by about 1 point and RECAST with coefficient tuning by 5 points, suggesting that compression quality directly bounds downstream task adaptability*

Table 2（下半部分）展示了压缩后模型作为PEFT初始化的性能。CRISP的MC+PEFT组合达到**88.8%的平均准确率**，超越最佳剪枝+PEFT组合（DGMR+SSF，87.9%）约0.9个百分点，较RECAST的系数微调方案高出约5个百分点。这一结果表明：**压缩质量直接决定下游任务适配能力的上限**，而CRISP的统一因子化结构避免了压缩与微调之间的表示冲突。

在更极端的75%压缩率下（Table 9），CRISP的优势进一步扩大，超越先前方法最高达11个百分点，验证了框架在高压缩比下的鲁棒性。

![[assets/figures/papers/paper_list_l854_https_arxiv_org_abs_2603_27383/figures/017_Table_9.jpg]]
*Table 9: Compression results on ViT-B/16 [13] at 75% parameter reduction evaluated on six fine-grained classification benchmarks (see Tab. 2 of the main paper for 50% reduction). Upper section: post-compression accuracy with only classifier adaptation. Lower section: MC+PEFT combinations demonstrate compressed models as initialization for downstream tasks. We find that CRISP outperforms prior work by up to 11%*

### LLaMA压缩与跨架构泛化

Table 3展示了LLaMA3.2-1B在30%参数削减下的常识推理结果。CRISP以**38.0%的平均准确率**显著优于PruneNet（34.9%），提升3.1个百分点。这一跨架构（ViT→LLaMA）的泛化能力是许多先前PR方法所缺乏的——作者明确指出“we found many prior works lack”这种泛化性。CRISP的成功归因于其因子化结构不依赖特定架构假设：共享基矩阵$B_i'^r$和门控混合矩阵$A_i'^{rs}$的参数化形式可无缝适配Transformer中的线性层权重。

### 关键消融分析

**混合矩阵维度的影响（Figure 5）**：这是揭示CRISP核心机制的关键消融。固定列维度$s=16$时，增加行维度$r$虽然减少参数量，但导致准确率急剧崩溃；反之，固定$r=16$并增加$s$则能恢复并提升性能。这一发现确立了**基矩阵容量（列维度$s$）是性能的主要驱动因素**，而系数表达力（行维度$r$）起次要作用。该结果为超参数调优提供了明确指引：优先增大$s$以扩展共享基的表示空间。

**门控机制与正则化（Table 4, Figure 6）**：SiLU门控在所有基准上均优于权重衰减、无约束等替代方案，验证了其内置正则化效果。约束放置位置的消融（Figure 6）表明，**PRE-SiLU（门控作用于混合矩阵后、与基矩阵交互前）**一致优于POST和TEMP配置。关键失败模式：ReLU激活函数因过度稀疏化导致性能灾难性下降，这与ReLU将负值置零、破坏基向量线性组合连续性的特性一致。

**压缩策略消融（Table 8）**：蒸馏损失配合SVD初始化的组合达到88.8%的最优性能；若仅使用神经拟态初始化（无蒸馏），性能骤降至57.8%，差距达31个百分点。这表明对于高压缩比场景，**数据驱动的知识蒸馏是维持模型质量的关键**，单纯的无数据权重重建不足以保留任务相关特征。

**初始化鲁棒性（Figure 8）**：混合矩阵$A'^{rs}$的Uniform、Kaiming、Xavier、Orthogonal四种标准初始化方法性能差异在1%以内，表明CRISP对初始化策略不敏感，降低了实际部署的调参负担。

### 计算效率

Table 5显示，在匹配可训练参数预算（约150K-240K）下，CRISP的训练吞吐量（163 samp/s）和推理吞吐量（657 samp/s）与LoRA等主流PEFT方法持平，未引入显著的计算开销。神经拟态初始化在ViT上可在单GPU上于1分钟内完成，LLaMA模型也仅需不到30分钟。

### 失败模式与局限

1. **ReLU门控的灾难性失效**：Figure 6中ReLU导致准确率大幅下降，原因是其将负激活置零的特性破坏了混合矩阵中基向量系数的连续性，造成权重稀疏化。
2. **极端压缩下的初始化敏感性**：Table 8揭示，75%压缩率下神经拟态初始化单独使用性能严重不足，必须依赖蒸馏和SVD初始化。这暗示无数据初始化在容量极度受限时存在表示崩溃风险。
3. **超参数手动设置**：$r$和$s$目前需人工选择，缺乏自动化机制。Figure 5虽提供了$s$优先的调参原则，但最优配置仍需网格搜索。
4. **架构验证范围有限**：当前仅在ViT和LLaMA上验证，尚未扩展到CNN或大视觉语言模型等架构。

### 补充图表

![[assets/figures/papers/paper_list_l854_https_arxiv_org_abs_2603_27383/figures/003_Table_1.jpg]]
*Table 1: PEFT performance on VTAB-1K [93] across 19 tasks grouped into Natural (7), Specialized (4), and Structured (8). CRISP achieves state-of-the-art overall accuracy while tuning 28% fewer parameters than all baselines*

![[assets/figures/papers/paper_list_l854_https_arxiv_org_abs_2603_27383/figures/006_Table_3.jpg]]
*Table 3: LLaMA3.2-1B [22] compression at 30% parameter reduction across seven commonsense reasoning benchmarks. CRISP’s 3% average gain shows it can perform well on LLMs, demonstrating an ability generalize across architectures we found many prior works lack*

![[assets/figures/papers/paper_list_l854_https_arxiv_org_abs_2603_27383/figures/008_Table_4.jpg]]
*Table 4: Ablation on the regularization strategy for the mixer matrix*

![[assets/figures/papers/paper_list_l854_https_arxiv_org_abs_2603_27383/figures/016_Table_8.jpg]]
*Table 8: Compression results on ViT-B/16 [13] with 50% weight compression across six diverse tasks (See Table 7). We find that using the distillation loss with SVD initialization described in Sec. 3.2 of our paper provides best performance*

![[assets/figures/papers/paper_list_l854_https_arxiv_org_abs_2603_27383/figures/010_Table_5.jpg]]
*Table 5: Efficiency using a NVIDIA L40S for task adaptation on ViT-B/16 [13] backbone under matched finetuning parameter budgets (∼150K–240K trainable parameters, excluding head)*

![[assets/figures/papers/paper_list_l854_https_arxiv_org_abs_2603_27383/figures/007_Figure_4.jpg]]
*Figure 4: Comparing ImageNet [11] performance with and without 8-bit PTQ [83] compression. We find CRISP accurately reproduces the original model’s performance while also demonstrating effective compositionality with other compression techniques*

![[assets/figures/papers/paper_list_l854_https_arxiv_org_abs_2603_27383/figures/015_Figure_8.jpg]]
*Figure 8: Robustness to initialization methods. We evaluate four standard initialization schemes (Uniform, Kaiming, Xavier, Orthogonal) for the mixer matrices A′rs during both neural mimicry retrofitting and subsequent task adaptation*



## 定位与知识库关联

### 参数重组（PR）方法的演进脉络

CRISP 所解决的问题根植于**参数重组（Parameter Recombination, PR）**这一技术路线。PR 方法的核心思想是定义一种变换 $\mathcal{T}$，将一组可训练参数 $\theta_i$ 映射为模型的实际权重 $W_i = \mathcal{T}(\theta_i)$，从而在参数预算与模型表达力之间建立灵活的控制机制。根据变换形式和应用目标的不同，现有 PR 方法可大致分为两条独立发展的分支：

**参数高效微调（PEFT）分支**以 **LoRA** 为代表，其变换形式为 $\mathcal{T}_{\mathrm{LoRA}}(B_i^r, A_i^r) = B_i^r A_i^r + W_{p_i}$，通过在冻结的预训练权重上叠加低秩可训练矩阵来实现任务适配。后续工作如 **DoRA** 进一步将权重分解为幅度和方向分量以提升微调质量，**SSF** 则通过逐通道的缩放与偏移操作实现轻量适配。这些方法的共同特点在于：它们保留了完整的预训练权重，仅引入额外的轻量适配器，天然不支持模型压缩。

**模型压缩（MC）分支**以 **Basis Sharing** 为代表，其变换形式为 $\mathcal{T}_{\mathrm{BasisSharing}}(B_i^r, A_i^r) = B_i^r A_i^r$，通过跨层共享低秩基矩阵直接减少参数量。**DGMR** 等方法则针对 ViT 架构设计了专门的压缩策略。这些方法在压缩后通常需要重新微调，但压缩结构与微调结构是分离的——压缩阶段使用的低秩分解与微调阶段引入的适配器（如 LoRA）之间没有共享机制，导致参数利用效率低下。

### CRISP 在谱系中的关键突破

**RECAST**（Tasnim & Plummer, ICLR 2025）是 CRISP 最直接的前驱工作，首次尝试在同一框架内同时支持 PEFT 和 MC。其变换形式为 $\mathcal{T}_{\mathrm{RECAST}}(B_i^{*r}, a_{i,j}^r) = \frac{1}{K} \sum_{j=1}^K B_i^{*r} a_{i,j}^r$，通过平均 $K$ 个系数向量来生成权重。然而，RECAST 存在两个根本性限制：

1. **混合系数为向量（size $r$）**，限制了模型对基矩阵各列的独立调制能力。当参数预算增大时，单纯增加基矩阵大小会导致性能饱和，因为混合系数的表达力成为瓶颈。
2. **线性组合缺乏内置正则化**，容易在微调阶段过拟合，需要额外的正则化策略。

CRISP 针对这两个瓶颈进行了结构性改进：

- **将混合系数从向量扩展为矩阵 $A_i^{\prime rs} \in \mathbb{R}^{r \times s}$**，引入超参数 $s$ 控制混合矩阵的列数。这一改动使得混合矩阵的列维度 $s$ 直接控制共享基矩阵的容量，成为性能的主要驱动因素（消融实验证实：固定 $s=16$ 时增大 $r$ 导致准确率崩溃，而固定 $r=16$ 时增大 $s$ 则持续恢复性能，见 Figure 5）。
- **引入逐元素 sigmoid 门控机制** $\mathcal{T}_{\mathrm{CRISP}}(B_i^{\prime r}, A_i^{\prime rs}) = B_i^{\prime r} (\sigma(A_i^{\prime rs}) \odot A_i^{\prime rs})$，提供内置正则化。消融实验（Table 4）表明，SiLU 门控在所有基准上均优于权重衰减、无约束等替代方案，而 ReLU 因过度稀疏化导致性能灾难性下降。

### 统一框架的设计哲学

CRISP 的核心洞察在于：**通过将预训练权重分解为冻结的共享基矩阵 $B_i^{\prime r}$ 和可学习的门控混合矩阵 $A_i^{\prime rs}$，可以在同一因子化结构内同时实现模型压缩和高效微调，无需引入冗余适配器**。

- **压缩模式**：通过跨层共享基矩阵并减小其大小来控制模型容量；基矩阵冻结，仅通过神经拟态（Neural Mimicry）初始化混合矩阵以重建预训练权重。
- **微调模式**：冻结基矩阵，仅更新轻量级混合矩阵进行下游任务适配。由于混合矩阵本身参数极少，且 sigmoid 门控提供隐式正则化，CRISP 在极低参数预算下即可达到甚至超越专用 PEFT 方法的性能。

这种统一设计带来了两个层面的优势：

1. **参数效率的质变**：压缩阶段节省的参数可直接转化为微调阶段的额外容量预算，而非像传统方案那样被独立的适配器结构消耗。在 VTAB-1K 上，CRISP 以 59.2% 的总体准确率超越所有 PEFT 基线，同时参数用量减少 28%（Table 1）。
2. **压缩质量直接约束下游适应性**：Table 2 显示，CRISP 压缩后微调（88.8%）相比 RECAST 的系数微调（83.8%）高出 5 个百分点，验证了压缩阶段重建质量对下游任务性能的因果性影响。

### 适用边界与局限

**已验证的适用范围**：

- **架构**：ViT（ViT-S/16, ViT-B/16）和 LLaMA（LLaMA3.2-1B）两类架构上均取得显著提升，表明方法对 Transformer 类模型具有较好的泛化性。
- **任务类型**：涵盖 VTAB-1K 的 19 个视觉任务（自然、专业、结构化）、6 个细粒度分类基准、7 个常识推理基准，以及 ImageNet-1K 分类。
- **压缩率**：在 ViT-B/16 上验证了 50% 和 75% 参数削减，在 LLaMA3.2-1B 上验证了 30% 参数削减。75% 压缩率下 CRISP 超越先前方法最高达 11%（Table 9）。
- **与其他压缩技术的组合**：Figure 4 表明 CRISP 可与 8-bit PTQ 量化组合使用，准确复现原始模型性能。

**明确局限与待验证边界**：

1. **架构泛化性未充分验证**：目前仅在 ViT 和 LLaMA 上进行了实验，尚未扩展到 CNN、大视觉语言模型或其他模态的架构。LLaMA 实验中的 PEFT 基线结果直接引用自各自论文，评估使用统一的 lm-evaluation-harness 库以确保超参数一致性，但跨架构的通用性仍需更多证据。
2. **超参数选择的自动化缺失**：$r$ 和 $s$ 目前需手动设置。消融实验已揭示 $s$（列数）是性能的主要驱动因素，但如何根据目标压缩率和任务复杂度自动选择最优的 $(r, s)$ 组合仍是开放问题。
3. **压缩阶段的数据依赖性**：ViT 压缩实验中蒸馏仅使用 2% 的 ImageNet-1K 数据，虽然展示了数据效率优势，但不同架构或极端压缩率下的最优蒸馏策略（数据量、损失函数组合）仍需系统验证。消融实验（Table 8）表明蒸馏损失与 SVD 初始化的组合至关重要——单纯使用神经拟态会导致 31% 的性能下降（88.8 vs. 57.8）。
4. **与现有 PR 方法的直接组合未探索**：文中明确指出 CRISP 与 LoRA 等适配器的组合是潜在的未来方向，但尚未进行实验验证。

### 开放问题

1. **自动容量分配**：能否学习自动选择 $r$ 和 $s$，针对不同层的重要性动态分配基矩阵容量和混合矩阵表达力，以优化压缩-性能的帕累托前沿？
2. **大规模 LLM 的扩展性**：LLaMA3.2-1B 的实验已初步验证可行性，但 CRISP 在更大规模模型（如 7B、13B）上的压缩与微调效果、以及基矩阵跨层共享策略在大模型中的最优粒度仍需探索。
3. **持续学习与长尾场景**：在持续学习或长尾任务下，基矩阵和混合器的动态更新策略如何设计？冻结基矩阵 + 微调混合器的范式是否足以应对灾难性遗忘？
4. **与正交压缩技术的深度结合**：CRISP 已展示与 PTQ 的初步组合效果，但与剪枝、知识蒸馏、量化感知训练等技术的系统结合能带来多少额外收益？
5. **跨模态迁移**：CRISP 的因子化结构能否推广到语音、视频等多模态 Transformer，以及跨模态迁移场景中基矩阵的共享机制如何设计？



## 原文 PDF

![[paperPDFs/CVPR_2026/Decompose_Mix_Adapt_A_Unified_Framework_for_Parameter_Efficient_Neural_Network_Recombination_and_Compression.pdf]]
