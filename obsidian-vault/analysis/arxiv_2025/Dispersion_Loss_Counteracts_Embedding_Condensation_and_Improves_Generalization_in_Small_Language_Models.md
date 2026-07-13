---
title: Dispersion Loss Counteracts Embedding Condensation and Improves Generalization in Small Language Models
type: paper
paper_level: A
venue: arXiv
year: 2025
pdf_ref: paperPDFs/arxiv_2025/LM_Dispersion_Dispersion_Loss_Counteracts_Embedding_Condensation.pdf
project_link: null
code_link: null
aliases:
- DL
- DLCECIGSLM
tags:
- arxiv_2025
- topic/representation_self_supervised_transfer
- topic/representation_self_supervised_transfer/representation_learning
core_operator: 在训练过程中引入分散损失（Dispersion Loss）作为辅助正则项，直接惩罚嵌入向量方向的过度对齐，从而增强表示分散性。
primary_logic: 嵌入凝聚是大模型与小模型性能差距的关键几何原因；通过显式鼓励嵌入分散，可以恢复大模型固有的表示多样性，在不增加参数的前提下提升小模型泛化能力。
claims:
- 小模型（如 GPT2、Qwen3-0.6B）表现出严重的嵌入凝聚，大模型（如 GPT2-xl、Qwen3-32B）则更抵抗该现象。
- 在中训练期间加入分散损失可以大幅缓解嵌入凝聚，使余弦相似度分布更加分散。
- 在中训练中使用分散损失的模型，在 10 项语言理解任务上一致优于仅用标准损失的模型。
- 完整预训练中加入分散损失带来 +1.17 的平均性能提升（约 3.3% 相对增益）。
---

# Dispersion Loss Counteracts Embedding Condensation and Improves Generalization in Small Language Models

> [!tip] 核心洞察
> 嵌入凝聚是大模型与小模型性能差距的关键几何原因；通过显式鼓励嵌入分散，可以恢复大模型固有的表示多样性，在不增加参数的前提下提升小模型泛化能力。

| 字段 | 内容 |
|------|------|
| 中文题名 | 分散损失对抗嵌入凝聚并提升小型语言模型泛化能力 |
| 英文题名 | Dispersion Loss Counteracts Embedding Condensation and Improves Generalization in Small Language Models |
| 会议/期刊 | arXiv 2025 |
| Links | [paper](https://arxiv.org/abs/2601.12867) |
| Topic | #topic/representation_self_supervised_transfer #topic/representation_self_supervised_transfer/representation_learning |
| Method | Dispersion Loss |
| Dataset | 10 language tasks, PIQA, TruthfulQA |

> [!tip] 效果简介
> - 10 language tasks (GPT2 mid-training) 上，Average accuracy 35.42 vs 34.95 (+0.47)。
> - PIQA (Qwen3-0.6B pre-training) 上，Accuracy see Table 5 vs see Table 5 (+4.0)。
> - TruthfulQA (Qwen3-0.6B pre-training) 上，Accuracy see Table 5 vs see Table 5 (+7.4)。

## 概要

**核心问题：嵌入凝聚——小模型性能的几何瓶颈。** 小型语言模型（如 GPT2、Qwen3-0.6B）在深层 Transformer 处理中表现出严重的嵌入凝聚（embedding condensation）现象：同一序列中所有 token 的嵌入向量余弦相似度向 1 集中，形成狭窄的方向锥（Figure 1）。相比之下，大模型（如 GPT2-xl、Qwen3-32B）天然更具抵抗该凝聚的能力（Figure 2）。严格控制实验（仅变化 MLP 维度）证实，这种“大模型更抗凝聚”的趋势并非其他架构因素的混淆，而是模型容量本身带来的几何特性（Figure 3）。进一步分析表明，嵌入凝聚在模型初始化后即刻出现，且知识蒸馏等现有策略无法有效缓解（Figure 4、Figure 5）。

**核心方法：分散损失（Dispersion Loss）。** 针对上述瓶颈，本文提出分散损失——一种直接作用于嵌入几何的正则化项。在训练过程中，该损失将各层 token 嵌入归一化到单位超球面，计算序列内非对角 token 对之间的余弦相似度，通过反余弦转换为角度距离，再以 log-sum-exp 聚合为标量损失，显式惩罚嵌入方向的过度对齐（Equation 2）。最终训练目标为标准交叉熵损失与分散损失的加权组合：$\mathcal{L} = \mathcal{L}_{\mathrm{train}} + \lambda_{\mathrm{disp}} \cdot \mathcal{L}_{\mathrm{disp}}$（Equation 3）。

**核心洞见：几何正则化可恢复表示多样性。** 嵌入凝聚是大模型与小模型性能差距的关键几何原因。通过在训练中显式鼓励嵌入分散，可以在不增加参数的前提下恢复大模型固有的表示多样性，从而提升小模型的泛化能力。

**主要结果：一致的性能提升。** 在中训练（mid-training）设置下，加入分散损失的 GPT2 模型在 10 项语言理解任务上平均准确率达 35.42，较标准训练的 34.95 提升 +0.47（Table 2）。在 Qwen3-0.6B 完整预训练中，分散损失带来 +1.17 的平均性能提升，约 3.3% 的相对增益，其中 PIQA 提升 +4.0，TruthfulQA 提升 +7.4（Table 5）。消融实验表明，分散损失施加于深层（L/2 至 L）效果优于全部层，与深层凝聚更严重一致；超参数 $\lambda_{\mathrm{disp}}$ 和 $\tau$ 在较大范围内表现鲁棒（Table 3、Table 4）。

**方法定位。** 分散损失作为一种训练目标层面的正则化策略，区别于向嵌入添加噪声（Jain et al., 2024）或周期性重置嵌入层（Chen et al., 2023）等间接方法，直接针对嵌入几何进行优化。其替代公式（去相关、ℓ₂-repel、正交化）在几何机制上各有侧重（Figure 6），但经典分散损失在稳定性和效果上整体占优。

### 小型语言模型的性能瓶颈

随着语言模型在各类任务中展现出强大的能力，模型规模被视为提升性能的关键因素。然而，大规模模型的高昂部署与训练成本使得小型语言模型在资源受限场景中仍具有不可替代的价值。当前，小型模型与大型模型之间存在显著的性能差距，缩小这一差距成为语言模型研究的重要课题。

### 嵌入凝聚现象的发现

本文揭示了一个此前未被充分关注的几何现象——**嵌入凝聚**：在预训练语言模型中，同一输入序列的所有 token 嵌入经过多层 Transformer 处理后，会逐渐聚集到单位超球面上的一个狭窄锥体内。具体而言，深层 token 嵌入之间的余弦相似度向 1 集中，导致表示方向的多样性丧失、表达能力受限。

这一现象在不同模型家族中普遍存在。如 Figure 2 所示，小模型（如 GPT2、Qwen3-0.6B）的 token 余弦相似度在深层变得高度正向集中，而大模型（如 GPT2-xl、Qwen3-32B）则表现出更强的抵抗能力。通过 Spearman 相关性和 Kendall's Tau 的量化分析，多个模型家族均呈现“模型越大，凝聚越弱”的一致趋势（Figure 2b）。此外，这一现象在不同输入文本数据集上表现一致（Figure S2），且从模型初始化阶段即已出现（Figure 4）。

### 大模型抵抗凝聚的因果验证

为排除其他混杂因素的干扰，本文进行了严格控制实验：在保持层数、嵌入维度、数据集和训练配置完全不变的前提下，仅改变 MLP 维度训练了四个不同规模的 GPT2 类模型。如 Figure 3 所示，仅增大 MLP 维度即可显著缓解嵌入凝聚，从因果层面验证了模型容量与嵌入凝聚之间的内在关联。

### 现有方法的不足

值得注意的是，知识蒸馏作为将大模型能力迁移至小模型的常用技术，并不能有效缓解嵌入凝聚现象（Figure 5）。蒸馏后的小模型仍然表现出与原始小模型相似的凝聚程度，表明单纯模仿大模型输出分布无法恢复其嵌入几何的多样性。这一发现揭示了现有方法的根本局限：它们未触及嵌入表示空间的几何退化这一深层瓶颈。

### 本文动机与核心思路

基于上述观察，本文提出核心假设：**嵌入凝聚是大模型与小模型性能差距的关键几何原因**。大型模型固有的表示容量使其能够自然维持嵌入的分散性，而小型模型则因表示能力受限而陷入凝聚。因此，若能在训练过程中显式鼓励嵌入分散，有望在不增加参数的前提下恢复大模型固有的表示多样性，从而提升小模型的泛化能力。

为此，本文提出**分散损失**作为辅助正则项，直接惩罚嵌入向量方向的过度对齐，在训练过程中主动对抗嵌入凝聚。该方法可与标准交叉熵训练无缝结合，作为一种几何感知的训练策略，为缩小大小模型差距提供了新范式。

## 核心方法与创新机理

本文的核心创新在于将**嵌入凝聚（Embedding Condensation）** 识别为小型语言模型性能瓶颈的关键几何根源，并提出**分散损失（Dispersion Loss）** 作为直接干预该瓶颈的训练正则项。与现有方法在训练策略（知识蒸馏、噪声注入、周期性重置）或表示维度（去相关、正交化）上间接作用不同，本文的创新点在于直接在单位超球面上优化 token 嵌入的**角度分布**，从而恢复小模型被压缩的表示多样性。

### 关键瓶颈识别：嵌入凝聚作为小模型的几何缺陷

论文首先通过跨模型家族的定量分析（Figure 2）揭示了一个此前未被系统量化的现象：小型语言模型（如 GPT2、Qwen3-0.6B）的深层 token 嵌入余弦相似度向 1 集中，形成“窄锥”分布；而大模型（如 GPT2-xl、Qwen3-32B）则天然抵抗这种凝聚。这一发现通过严格控制实验（Figure 3）得到因果验证——仅变化 MLP 维度而固定其他所有架构和训练因素，模型越大凝聚越轻。此外，对 Olmo-3-1025-7B 训练检查点的分析（Figure 4）表明，凝聚在模型初始化后立即出现，说明这是架构容量受限的系统性缺陷，而非训练后期的退化现象。

### 核心机制：从交叉熵到角度分散的正则化

基于上述诊断，论文的核心改变在于**训练目标函数**的扩展。基线方法仅使用标准下一个 token 预测的交叉熵损失：

$$ \text{Baseline: } \mathcal{L} = \mathcal{L}_{\text{train}} $$

本文提出的方法在交叉熵损失上叠加一个辅助正则项——分散损失：

$$ \mathcal{L} = \mathcal{L}_{\text{train}} + \lambda_{\text{disp}} \cdot \mathcal{L}_{\text{disp}} $$

其中分散损失的设计直接针对嵌入凝聚的几何本质：

$$ \mathcal{L}_{\text{disp}} = \log \sum_{i,j}^{i \ne j} e^{- \frac{\operatorname{arccos}\left(\cos \sin(z_i, z_j)\right)}{\pi \tau}} $$

该损失的计算流程包含三个关键模块：首先将每层 token 嵌入归一化到单位超球面；然后计算序列内所有 token 对的余弦相似度；接着通过反余弦转换为角度距离；最后通过 log-sum-exp 汇聚非对角线对形成标量损失。最小化该损失等价于最大化嵌入向量间的角度距离，从而在几何上直接对抗凝聚。

### 与基线方法和替代方案的差异

论文将分散损失与多种替代方案进行了系统对比，凸显其设计选择的合理性：

- **知识蒸馏**（Figure 5）：尽管蒸馏将大模型知识迁移到小模型，但蒸馏后的小模型仍然表现出严重嵌入凝聚，说明蒸馏无法解决表示几何层面的瓶颈。
- **噪声嵌入**（Jain et al., 2024）与**主动遗忘**（Chen et al., 2023）：这些方法通过扰动或重置嵌入层间接影响表示，但未直接针对余弦相似度集中这一根本几何缺陷。
- **去相关（Decorrelation）**：鼓励不同特征维度不相关，作用于维度间而非 token 间，无法直接缓解 token 级的角度凝聚。
- **ℓ₂-repel**：在欧氏空间中推开嵌入向量，但需要范数正则化防止无界膨胀，分散与正则化的脆弱平衡导致训练不稳定（Table 2 显示其效果弱于分散损失）。
- **正交化（Orthogonalization）**：仅惩罚锐角对而忽略钝角对，当向量已正交时梯度消失，分散力度不足。

分散损失的关键优势在于：它在角度空间中均匀地推开所有嵌入对（Figure 6a），不依赖范数平衡，且通过 log-sum-exp 的软最小化形式对接近的嵌入对施加更强惩罚，形成自适应的分散力度。

本文提出的方法围绕一个核心观察展开：小型语言模型的深层 token 嵌入存在严重的**嵌入凝聚**现象——同一序列内所有 token 的余弦相似度随层深增加而向 1 集中，导致表示方向单一、表达能力受限。针对这一瓶颈，作者设计了一个简洁的**分散损失**作为辅助正则项，在训练过程中显式惩罚嵌入向量方向的过度对齐，从而恢复表示多样性。

### 核心假设与因果链路

整个工作的因果链路可概括为：

1. **瓶颈识别**：通过跨模型家族的定性（余弦相似度热图）与定量（Spearman/Kendall 相关系数）分析，确认小模型（GPT2、Qwen3-0.6B）深层嵌入凝聚严重，而大模型（GPT2-xl、Qwen3-32B）天然抵抗该现象（Figure 2）。控制实验进一步验证：仅变化 MLP 维度而固定其他所有因素（层数、嵌入维度、数据集等）时，模型越大凝聚越轻（Figure 3）。
2. **因果调节**：在标准下一个 token 预测交叉熵损失 $ \mathcal{L}_{\mathrm{train}} $ 之上，引入分散损失 $ \mathcal{L}_{\mathrm{disp}} $ 作为正则项，形成完整训练目标：
   $$ \mathcal{L} = \mathcal{L}_{\mathrm{train}} + \lambda_{\mathrm{disp}} \cdot \mathcal{L}_{\mathrm{disp}} $$
   其中 $ \lambda_{\mathrm{disp}} $ 控制正则化强度。
3. **机制实现**：分散损失将每个 token 嵌入归一化到单位超球面后，计算序列内所有非对角线 token 对的余弦相似度，通过反余弦转换为角度距离，再以 log-sum-exp 形式汇聚为标量损失，最小化该损失即增大向量间角度，迫使嵌入在超球面上均匀分散。

### Pipeline 模块构成

方法的核心计算流程由四个模块串联组成：

| 模块 | 功能 | 输入 | 输出 |
|------|------|------|------|
| **Embedding Normalization** | 将各层 token 嵌入归一化到单位超球面 | 第 $l$ 层嵌入 $z_i^{(l)} \in \mathbb{R}^d$ | 归一化嵌入 |
| **Cosine Similarity Matrix** | 计算序列内所有 token 对之间的余弦相似度 | 归一化嵌入 | 相似度矩阵 $S \in \mathbb{R}^{N \times N}$ |
| **Angular Distance Conversion** | 通过反余弦将余弦相似度转换为角度距离 | 相似度矩阵 | 角度距离矩阵 |
| **Log-Sum-Exp Aggregation** | 对非对角线 pair 进行 log-sum-exp 汇聚，形成标量损失 | 角度距离矩阵 | 标量 $ \mathcal{L}_{\mathrm{disp}} $ |

分散损失的数学形式为：
$$ \mathcal{L}_{\mathrm{disp}} = \log \sum_{i,j}^{i \ne j} e^{- \frac{\operatorname{arccos}\left(\operatorname{cossim}(z_i, z_j)\right)}{\pi \tau}} $$
其中 $ \tau $ 为温度参数，控制对角度差异的敏感度；$ \operatorname{cossim}(z_i, z_j) $ 为归一化嵌入的余弦相似度。

### 训练范式与适用范围

分散损失被验证在两种训练范式中有效：

- **中训练**：在预训练基座模型上进行额外训练，分散损失作为正则项加入。实验覆盖 GPT2 和 Qwen3 家族的小型模型，在 10 项语言理解任务上一致优于仅用标准损失的基线（Table 2）。
- **完整预训练**：在 Qwen3-0.6B 的完整预训练中引入分散损失，带来 +1.17 的平均性能提升（约 3.3% 相对增益），在 PIQA 和 TruthfulQA 上分别获得 +4.0 和 +7.4 的显著提升（Table 5）。

### 与其他方法的定位关系

为缓解嵌入凝聚，本文还考察了若干替代方案，但均不如分散损失有效或稳定：
- **知识蒸馏**：虽能传递大模型知识，但无法缓解小模型的嵌入凝聚（Figure 5）。
- **Noisy Embedding**（Jain et al., 2024）：向嵌入添加噪声，缺乏对表示几何的显式约束。
- **Active Forgetting**（Chen et al., 2023）：周期性重置嵌入层，机制粗糙且可能丢失已学信息。
- **替代分散公式**：Decorrelation、Orthogonalization 和 ℓ₂-repel 等变体在实验中表现略逊或不稳定。特别是 ℓ₂-repel 因分散与范数正则化的脆弱平衡导致训练不稳定（Table 2, Section 4.2）。

### 关键设计选择

- **层范围**：消融实验表明，分散损失应用于深层（L/2 至 L）比应用于所有层效果更好，这与深层凝聚更严重的观察一致（Table 3）。
- **超参数鲁棒性**：$ \lambda_{\mathrm{disp}} $ 和 $ \tau $ 在较大范围内均能保持提升效果，降低了调参负担（Table 4）。
- **计算代价**：分散损失的计算复杂度为 $O(N^2)$（$N$ 为序列长度），对长序列可能产生额外开销，但可通过子采样缓解（论文提及但未深入展开）。

### 局限性提示

当前验证主要集中在小型模型（GPT2 和 Qwen3-0.6B），分散损失对大模型的有效性尚未系统探索。预训练实验仅在一个模型规模（0.6B）和一种数据集上进行，泛化到更大规模仍需更多证据。此外，正则化系数 $ \lambda_{\mathrm{disp}} $ 和温度 $ \tau $ 虽在一定范围内鲁棒，但仍需手动选择。

### 3.1 问题形式化：嵌入凝聚的量化

在 Transformer 架构中，给定一个长度为 $N$ 的输入序列，经过第 $l$ 层后得到上下文 token 嵌入矩阵 $\mathcal{Z}^{(l)} = [z_1^{(l)}, z_2^{(l)}, \ldots, z_N^{(l)}]^\top \in \mathbb{R}^{N \times d}$，其中 $d$ 为嵌入维度。本文的核心观察是：在小型语言模型中，这些嵌入向量在深层会“凝聚”到一个狭窄的锥形区域内，表现为两两之间的余弦相似度向 1 集中。

为量化这一现象，定义第 $l$ 层 token $i$ 与 $j$ 之间的**成对余弦相似度**：

$$\operatorname{cossim}(z_i^{(l)}, z_j^{(l)}) = \frac{z_i^{(l)\top} \cdot z_j^{(l)}}{\|z_i^{(l)}\| \cdot \|z_j^{(l)}\|}$$

进一步定义第 $l$ 层的**平均余弦相似度**作为凝聚程度的标量度量：

$$\mu^{(l)} = \frac{1}{N^2} \sum_{i=1}^N \sum_{j=1}^N \operatorname{cossim}(z_i^{(l)}, z_j^{(l)})$$

该度量在后续实验中用于追踪嵌入凝聚随层深度的演化趋势（见 Figure 2-4）。

![[assets/figures/papers/paper_list_l11_https_arxiv_org_abs_2601_12867/figures/002_Figure_2.jpg]]
*Figure 2: Qualitative and quantitative observations of the embedding condensation phenomenon. a. The cosine similarity heatmaps demonstrate that smaller models (e.g., GPT2, Qwen3-0.6B) are susceptible to condensation, since token cosine similarities become increasingly positive as the embeddings proceed to deeper layers. In contrast, larger models (e.g., GPT2-xl, Qwen3-32B) are more resistant to embedding condensation. b. Quantifications using Spearman correlation and Kendall’s Tau demonstrate a consistent trend of “larger model, less condensation” across multiple families of language models. Additional results can be found in Figure S1*

### 3.2 核心方法：分散损失（Dispersion Loss）

针对嵌入凝聚问题，本文提出**分散损失**作为辅助正则项，直接惩罚嵌入向量方向的过度对齐。其设计思路是：将归一化到单位超球面的嵌入向量视为粒子，通过最大化粒子间的角度距离来实现均匀分散。

分散损失的计算分为以下关键模块：

**（1）嵌入归一化（Embedding Normalization）**
将每个 token 嵌入归一化到单位超球面，消除范数对角度度量的干扰。

**（2）余弦相似度矩阵（Cosine Similarity Matrix）**
计算序列内所有 token 对之间的余弦相似度，形成 $N \times N$ 矩阵。

**（3）角度距离转换（Angular Distance Conversion）**
通过反余弦将余弦相似度转换为角度距离，使得分散损失直接作用于几何角度而非原始余弦值。

**（4）Log-Sum-Exp 聚合（Log-Sum-Exp Aggregation）**
对非对角线 token 对进行 log-sum-exp 汇聚，形成标量损失。该操作确保损失对最小角度距离（即最凝聚的 token 对）赋予主导梯度信号。

分散损失的完整公式为：

$$\mathcal{L}_{\mathrm{disp}} = \log \sum_{i,j}^{i \ne j} e^{- \frac{\operatorname{arccos}\left(\operatorname{cossim}(z_i, z_j)\right)}{\pi \tau}}$$

其中：
- $\operatorname{cossim}(z_i, z_j)$ 为 token $i$ 与 $j$ 的余弦相似度；
- $\operatorname{arccos}(\cdot)$ 将其转换为 $[0, \pi]$ 范围内的角度距离；
- $\tau$ 为温度参数，控制对角度差异的敏感度；
- log-sum-exp 对非对角线 pair 求和，最小化该损失等价于最大化嵌入向量间的角度。

### 3.3 完整训练目标

分散损失以正则项形式加入标准训练目标：

$$\mathcal{L} = \mathcal{L}_{\mathrm{train}} + \lambda_{\mathrm{disp}} \cdot \mathcal{L}_{\mathrm{disp}}$$

其中：
- $\mathcal{L}_{\mathrm{train}}$ 为标准下一个 token 预测的交叉熵损失；
- $\lambda_{\mathrm{disp}}$ 为分散损失的权重系数，控制正则化强度。

该目标函数是中训练和完整预训练阶段的唯一改动，不涉及模型架构的修改。

### 3.4 替代公式对比

为验证分散损失设计的有效性，本文还实现了三种替代公式（详见 Table 1 与 Figure 6）：

| 变体 | 核心机制 | 关键差异 |
|------|---------|---------|
| **Decorrelation** | 鼓励不同特征维度去相关 | 作用于特征维度而非 token 对 |
| **ℓ₂-repel** | 直接增大 token 对间的欧氏距离 | 需配合范数正则化防止无界膨胀，平衡脆弱 |
| **Orthogonalization** | 推开形成锐角的向量对 | 对已正交或钝角的向量对梯度为零 |

实验表明，ℓ₂-repel 因分散与范数正则化的脆弱平衡导致训练不稳定，Decorrelation 和 Orthogonalization 效果略逊于经典分散损失，验证了基于角度距离的 log-sum-exp 公式的优越性（见 Table 2, Section 4.2）。

### 3.5 与知识蒸馏的对比

本文还考察了知识蒸馏对嵌入凝聚的影响。知识蒸馏损失定义为学生模型匹配教师模型 logits 分布：

$$\mathcal{L}_{\mathrm{KD}}(\ell_T^{(i)}, \ell_S^{(i)}) = -\tau^2 \sum_{a=1}^{V} \sigma_a\left(\frac{\ell_T^{(i)}}{\tau}\right) \log \sigma_a\left(\frac{\ell_S^{(i)}}{\tau}\right)$$

其中 $\sigma_a(\ell) = \frac{\exp(\ell_a)}{\sum_{b=1}^{V} \exp(\ell_b)}$ 为 softmax 函数，$V$ 为词表大小。实验结果显示，知识蒸馏**无法缓解**嵌入凝聚（Figure 5），这进一步凸显了显式几何正则化的必要性。

![[assets/figures/papers/paper_list_l11_https_arxiv_org_abs_2601_12867/figures/003_Figure_3.jpg]]
*Figure 3: In a highly controlled experiment, we reproduced the observation of “larger model, less condensation”. We pre-trained four GPT2-like models of varying sizes that differ only in MLP dimension, while keeping all other factors fixed, including the number of layers, embedding dimension, dataset, and training configuration. The resulting models exhibit consistent trends in embedding condensation, shown qualitatively (panel a) and quantitatively (panel b). Horizontal dashed lines are added to panel a for easier visual comparison*

## 实验与关键发现

### 核心瓶颈：嵌入凝聚现象的实证确立

论文首先通过多角度实验确立了其核心瓶颈——嵌入凝聚（embedding condensation）——在小型语言模型中的普遍性与严重性。

**模型规模与凝聚程度的反比关系**（Figure 2）：在 GPT2 与 Qwen3 两个模型家族中，小模型（GPT2、Qwen3-0.6B）的深层 token 嵌入余弦相似度分布急剧向 1 集中，形成“窄锥”现象；而大模型（GPT2-xl、Qwen3-32B）则显著抵抗这一趋势。定量上，Spearman 相关系数与 Kendall's Tau 在多个家族中一致呈现“模型越大，凝聚越轻”的单调趋势。

**控制实验排除混淆因素**（Figure 3）：为排除架构差异的干扰，论文预训练了四个仅 MLP 维度不同的 GPT2 类模型（其他因素如层数、嵌入维度、数据集、训练配置完全固定）。结果复现了“更大模型更抗凝聚”的规律，确认模型容量本身是抵抗凝聚的关键因素。

**凝聚的时序起源**（Figure 4）：通过分析 Olmo-3-1025-7B 从初始化到最终基模型的检查点，发现嵌入凝聚在模型初始化后即刻出现（余弦相似度显著为正），随后在预训练过程中逐步减弱。这表明凝聚并非训练后期的退化现象，而是从初始阶段就存在的结构性问题。

**知识蒸馏的无效性**（Figure 5）：将大模型作为教师、小模型作为学生进行知识蒸馏，并不能缓解小模型的嵌入凝聚。这暗示凝聚的根源在于模型容量受限下的表示几何退化，而非缺乏“知识”本身。

### 主实验结果

#### 中训练设置下的性能提升

Table 2 展示了在 GPT2 和 Qwen3 模型上，中训练（mid-training）阶段加入分散损失后的 10 项语言理解任务表现。核心发现：

- **分散损失一致优于标准交叉熵训练**：在 GPT2 上，分散损失实现平均准确率 **35.42**（基线 34.95，+0.47），同时获得最低平均排名 **2.2**。
- **与其他正则化方法的对比**：分散损失优于 Noisy Embedding（Jain et al., 2024）和 Active Forgetting（Chen et al., 2023）等对比方法，表明显式几何正则化比噪声注入或参数重置更有效。
- **替代公式的比较**：ℓ₂-repel 变体因分散与范数正则化之间的脆弱平衡导致训练不稳定；去相关（Decorrelation）和正交化（Orthogonalization）变体略逊于经典分散损失，验证了基于角度距离的 log-sum-exp 汇聚公式的优越性。

#### 预训练设置下的性能提升

Table 5 报告了 Qwen3-0.6B 完整预训练中加入分散损失的结果。平均性能提升 **+1.17**（约 **3.3%** 相对增益），其中 PIQA 提升 **+4.0**，TruthfulQA 提升 **+7.4**。这证明分散损失在完整预训练流程中同样有效，且对真实性导向的任务提升尤为显著。

![[assets/figures/papers/paper_list_l11_https_arxiv_org_abs_2601_12867/figures/013_Table_5.jpg]]
*Table 5: Using dispersion loss during pre-training improves performance on language tasks. Experiments are performed under the Qwen3-0.6B pre-training setting*

#### 嵌入凝聚的几何缓解

Figure 7 通过余弦相似度热图直接展示了分散损失对嵌入几何的影响：中训练使用默认损失对已凝聚的嵌入影响有限（绿色框），而加入分散损失后嵌入分布显著分散（蓝色框），从几何层面验证了方法的机制有效性。

### 消融实验

**层范围选择**（Table 3）：将分散损失应用于深层（L/2 至 L）比应用于所有层或浅层效果更好，与深层凝聚更严重的观察一致。这支持了“对症下药”的直觉——在凝聚最严重的层施加正则化最为高效。

**超参数鲁棒性**（Table 4）：分散损失对权重系数 λ_disp 和温度参数 τ 具有较好的鲁棒性，在较大范围内均能保持性能提升。这降低了实际应用中的调参负担。

### 失败模式与局限

1. **ℓ₂-repel 的不稳定性**：该变体因同时优化分散目标和范数正则化，在训练中出现梯度冲突，导致收敛不稳定，说明基于欧氏距离的排斥机制在 Transformer 嵌入空间中存在根本性困难。
2. **大模型适用性未验证**：实证验证集中在 GPT2 和 Qwen3-0.6B 等小型模型，分散损失对大模型是否仍有增益尚不清楚——大模型本身已具备较好的抗凝聚能力，额外正则化可能无效甚至有害。
3. **计算复杂度**：分散损失的 log-sum-exp 汇聚需要对序列内所有非对角线 token 对进行计算，复杂度为 O(N²)，长序列训练时可能成为瓶颈（论文提及可通过子采样缓解，但未提供实验验证）。
4. **预训练实验规模有限**：完整预训练仅在 Qwen3-0.6B 单一规模和一种数据集上进行，泛化到更大规模模型和更多数据分布仍需更多证据。

### 重要图表结论汇总

| 图表 | 核心结论 |
|------|----------|
| Figure 2 | 小模型深层嵌入余弦相似度向 1 集中，大模型抵抗凝聚；多家族定量验证“模型越大凝聚越轻” |
| Figure 3 | 控制实验（仅变 MLP 维度）复现规模-凝聚反比关系，排除架构混淆 |
| Figure 7 | 分散损失显著缓解嵌入凝聚，默认损失几乎无效 |
| Table 2 | 分散损失在中训练中一致优于基线，平均提升 +0.47，排名最优 |
| Table 3 | 深层施加分散损失效果优于全层或浅层 |
| Table 4 | λ_disp 和 τ 在较大范围内鲁棒 |
| Table 5 | 预训练中加入分散损失带来 +1.17 平均提升（+3.3%），TruthfulQA 提升 +7.4 |

![[assets/figures/papers/paper_list_l11_https_arxiv_org_abs_2601_12867/figures/011_Table_3.jpg]]
*Table 3: Dispersion loss is more effective when applied to deeper layers, where embedding condensation is more pronounced. Experiments are performed under the GPT2 mid-training setting*

![[assets/figures/papers/paper_list_l11_https_arxiv_org_abs_2601_12867/figures/012_Table_4.jpg]]
*Table 4: Effect of hyperparameters on the dispersion loss. Ablation experiments are performed under the GPT2 mid-training setting*

![[assets/figures/papers/paper_list_l11_https_arxiv_org_abs_2601_12867/figures/005_Figure_5.jpg]]
*Figure 5: Knowledge distillation is not a remedy to embedding condensation, shown qualitatively (panel a) and quantitatively (panel b)*

## 定位与知识库关联

### 1. 问题定位：嵌入凝聚作为小模型性能瓶颈

本研究将小型语言模型的性能瓶颈归因于一个几何现象——**嵌入凝聚（Embedding Condensation）**：深层 token 嵌入的余弦相似度向 1 集中，导致表示方向单一、表达能力受限。这一现象在多个模型家族（GPT2、Qwen3、Olmo）中均被观察到，且呈现“模型越小、凝聚越严重”的一致趋势（Figure 2, Figure 3）。关键发现包括：

- **凝聚在初始化时即已出现**（Figure 4），并非训练后期才产生；
- **知识蒸馏无法缓解凝聚**（Figure 5），蒸馏后的学生模型仍表现出与原始小模型相似的凝聚程度；
- **大模型天然抵抗凝聚**：在仅改变 MLP 维度的严格控制实验中，更大模型始终表现出更低的嵌入凝聚（Figure 3）。

这一发现将大模型与小模型的性能差距从“参数量不足”重新框定为“表示几何退化”，为后续方法设计提供了明确的因果抓手。

### 2. 方法定位：显式几何正则化 vs. 隐式缓解策略

论文提出的**分散损失（Dispersion Loss）**属于**显式几何正则化**方法，直接作用于 token 嵌入的角度分布。其核心公式为：

$$\mathcal{L}_{\mathrm{disp}} = \log \sum_{i,j}^{i \ne j} e^{- \frac{\operatorname{arccos}\left(\cos\sin(z_i, z_j)\right)}{\pi \tau}}$$

该损失通过 log-sum-exp 聚合所有非对角线 token 对的角度距离，最小化时鼓励嵌入在单位超球面上均匀分散。完整训练目标为：

$$\mathcal{L} = \mathcal{L}_{\mathrm{train}} + \lambda_{\mathrm{disp}} \cdot \mathcal{L}_{\mathrm{disp}}$$

与论文中对比的几种替代方案相比，分散损失的方法谱系定位如下：

| 方法 | 作用空间 | 机制 | 稳定性 |
|------|----------|------|--------|
| **Dispersion Loss**（本文） | 角度空间（单位超球面） | log-sum-exp 聚合角度距离 | 稳定，超参数鲁棒 |
| Decorrelation | 特征维度间 | 去相关不同维度 | 略逊于分散损失 |
| ℓ₂-repel | 欧氏空间 | 增大欧氏距离 + 范数正则 | 不稳定，分散与范数正则脆弱平衡 |
| Orthogonalization | 角度空间 | 仅推开锐角向量，正交时梯度消失 | 略逊于分散损失 |

**ℓ₂-repel** 变体因需要同时平衡分散与范数正则化，导致训练不稳定；**Orthogonalization** 在向量已正交时梯度消失，限制了分散的上限；**Decorrelation** 从特征维度而非 token 角度出发，效果略逊。这些对比表明，**角度空间的 log-sum-exp 聚合是当前最有效的嵌入分散策略**。

### 3. 与现有方法的边界

论文明确将分散损失与以下方法区分：

- **Noisy Embedding**（Jain et al., 2024）：向嵌入添加噪声，属于隐式扰动策略，缺乏对几何结构的直接约束。
- **Active Forgetting**（Chen et al., 2023）：周期性重置嵌入层参数，属于间接缓解，无法持续对抗训练过程中的凝聚趋势。
- **知识蒸馏**：尽管蒸馏可以传递大模型的输出分布，但 Figure 5 表明蒸馏后的学生模型嵌入凝聚并未缓解，说明蒸馏不直接改善表示几何。

分散损失的独特优势在于：**在不增加参数、不改变模型架构的前提下，通过辅助损失直接塑造嵌入几何**，与上述方法形成互补而非替代关系。

### 4. 适用边界与局限

根据论文的实验覆盖范围和自我报告的限制，分散损失的适用边界如下：

**已验证有效的场景：**
- 小型语言模型（GPT2、Qwen3-0.6B）的中训练和完整预训练
- 10 项语言理解任务的零样本/少样本评估
- 深层（L/2 至 L）应用效果优于全层应用（Table 3）

**尚未验证或存在局限：**
- **大模型效果未知**：实证验证集中在小型模型，分散损失对大模型（如 Qwen3-32B）是否仍有增益尚未系统探索。由于大模型天然抵抗凝聚，分散损失可能边际收益递减。
- **计算复杂度**：分散损失需要对序列内所有 token 对计算角度距离，复杂度为 $O(N^2)$，对长序列训练可能产生额外负担（论文指出可通过子采样缓解，但未提供实验验证）。
- **预训练规模有限**：预训练实验仅在 Qwen3-0.6B 单一规模上进行，泛化到更大规模预训练仍需更多证据。
- **超参数选择**：尽管 Table 4 表明 $\lambda_{\mathrm{disp}}$ 和 $\tau$ 在较大范围内鲁棒，但仍需手动调节，缺乏自动化选择机制。

### 5. 开放问题与未来方向

论文提出的开放问题指向更广泛的表示几何研究方向：

1. **跨领域泛化**：几何感知的训练目标能否扩展到语言建模之外的领域（如视觉 Transformer、蛋白质结构预测），作为提升表示质量的可扩展途径？

2. **大模型的几何优化**：显式分散正则化是否能够进一步改善大模型的嵌入几何，使其超越现有容量带来的自然分散？这需要在大规模预训练设置中进行验证。

3. **架构层面的根本机制**：是否存在与模型大小无关的更根本机制来防止嵌入凝聚？理解这一机制可能指导更高效的架构设计（如归一化策略、残差连接变体），从根本上避免表示退化。

4. **与其他训练策略的协同**：分散损失与知识蒸馏、课程学习等策略的组效应尚未探索，可能存在协同增益。

### 6. 知识库定位总结

分散损失在表示学习知识库中的定位可概括为：**一种轻量级、即插即用的几何正则化工具**，通过显式惩罚嵌入方向对齐来恢复小模型的表示多样性。它填补了“大模型与小模型表示几何差异”这一研究空白，将性能差距从参数量的讨论转向表示质量的几何分析。其方法谱系介于**隐式正则化**（如 dropout、噪声注入）和**架构修改**之间，提供了一条不增加推理成本的性能提升路径。

## 原文 PDF

![[paperPDFs/arxiv_2025/LM_Dispersion_Dispersion_Loss_Counteracts_Embedding_Condensation.pdf]]
