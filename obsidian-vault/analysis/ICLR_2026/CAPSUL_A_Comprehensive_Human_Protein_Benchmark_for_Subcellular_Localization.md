---
title: "CAPSUL: A Comprehensive Human Protein Benchmark for Subcellular Localization"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/CAPSUL_A_Comprehensive_Human_Protein_Benchmark_for_Subcellular_Localization.pdf
project_link: null
code_link: null
openreview_forum_id: wJn4WbvSpK
aliases:
- CAPSUL
tags:
- ICLR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/genetics_cell_biology_health_etc
core_operator: "引入蛋白质三维结构特征（Cα坐标、3Di tokens）并将亚细胞注释细化为20类，同时提供实验证据级别的标注。"
primary_logic: "通过统一的三维结构表示与细粒度注释，验证了结构特征在亚细胞定位任务中的关键作用；利用注意力机制发现了α-螺旋等与定位相关的结构模式，提升了模型的生物学可解释性。"
claims:
- "随机打乱Cα坐标后，结构模型的性能显著下降，表明真实的三维结构信息是预测的关键因素。"
- "基于序列的模型ESM-C在大规模预训练下性能优于未预训练的版本，说明蛋白质序列预训练对定位任务有益，但仅靠序列无法完全捕捉与结构相关的定位信号。"
- "结构模型CDConv在预测高尔基体定位时达到100%精确率，并成功通过注意力机制识别出α-螺旋定位模式。"
- "CAPSUL (test set) 上 Micro Avg F1-score = 0.452 (CDConv with true Cα coordinates)"
---

# CAPSUL: A Comprehensive Human Protein Benchmark for Subcellular Localization

> [!tip] 核心洞察
> 通过统一的三维结构表示与细粒度注释，验证了结构特征在亚细胞定位任务中的关键作用；利用注意力机制发现了α-螺旋等与定位相关的结构模式，提升了模型的生物学可解释性。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | CAPSUL：用于亚细胞定位的全面人类蛋白质基准 |
| 英文题名 | CAPSUL: A Comprehensive Human Protein Benchmark for Subcellular Localization |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=wJn4WbvSpK) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/genetics_cell_biology_health_etc |
| Method | CAPSUL 数据集与基准构建 |
| Dataset | CAPSUL (test set) |

> [!tip] 效果简介
> - CAPSUL (test set) 上，Micro Avg F1-score 为 0.452 (CDConv with true Cα coordinates)，对比 0.329 (CDConv with randomly sampled Cα coordinates)，变化 −0.123。
> - CAPSUL (test set) 上，Micro Avg F1-score 为 0.417 (GearNet-Edge with true Cα coordinates)，对比 0.348 (GearNet-Edge with randomly sampled Cα coordinates)，变化 −0.069。
> - CAPSUL (test set) 上，Nucleus F1-score 为 0.649 (ESM-C 600M, pre-trained)，对比 0.555 (ESM-C 600M0, no pre-training)，变化 +0.094 (pre-training benefit)。

## 概要

亚细胞定位是理解蛋白质功能的关键维度，但现有数据集普遍缺乏蛋白质三维结构信息（如Cα坐标、3Di tokens）和细粒度的亚细胞分类注释，这限制了基于结构的预测模型的发展。CAPSUL（ICLR 2026）针对这一瓶颈，构建了一个全面的人类蛋白质亚细胞定位基准，其核心贡献在于：将AlphaFold2预测的Cα坐标与FoldSeek导出的3Di结构token统一纳入数据表示，同时将亚细胞注释细化为20个类别（由领域专家验证），并为每个标注附加实验证据级别标签。

基准实验揭示了几个关键发现。首先，结构特征对预测至关重要：随机打乱Cα坐标后，CDConv的Micro Avg F1从0.452降至0.329，GearNet-Edge则从0.417降至0.348，证实真实的三维空间信息是定位信号的核心驱动因素。其次，序列预训练带来显著增益——ESM-C 600M在细胞核上的F1达到0.649，而未预训练的版本仅为0.555，表明大规模预训练有助于捕获定位相关特征，但仅靠序列信息仍不足以完全替代结构信号。第三，结构模型展现出优异的生物学可解释性：CDConv在高尔基体预测上达到100%精确率，并通过注意力机制成功识别出α-螺旋定位模式——注意力得分最高的20个残基与已知α-螺旋模式的重叠度达90%。

方法层面，CAPSUL并非提出新的预测算法，而是建立了一个多模态基准框架。该框架整合了序列编码器（ESM-2、ESM-C）、结构编码器（CDConv、GearNet-Edge、FoldSeek）以及专门的预测工具（DeepLoc 2.1），统一采用二元交叉熵损失进行多标签分类优化。实验还揭示了类别不平衡这一核心挑战：正样本比例仅0.5%–3%，导致少数类预测困难。重加权策略和单标签分类策略可部分缓解该问题，使结构模型在少数类上也能做出正样本预测，但整体宏平均F1仍较低，表明该问题尚未完全解决。

蛋白质的亚细胞定位是理解其功能、调控和疾病关联的核心线索。一个蛋白质的功能不仅取决于其序列，更与其在细胞内的精确空间位置密切相关。然而，现有的亚细胞定位预测数据集存在两个关键瓶颈，限制了该领域向更高精度和可解释性发展。

**瓶颈一：三维结构信息的缺失。** 当前主流数据集仅提供氨基酸序列，缺乏蛋白质的三维结构特征（如Cα坐标、3Di结构tokens）。这导致基于结构的预测模型无法有效开发，也使得许多与空间构象相关的定位信号被忽略。尽管AlphaFold2等工具已能大规模预测高质量蛋白质结构，但尚无基准数据集将这些结构信息系统性地整合到定位预测任务中。

**瓶颈二：亚细胞分类粒度粗糙且缺乏证据可信度标注。** 现有数据集（如DeepLoc）通常仅提供10个粗粒度类别，无法捕捉细胞内精细区室（如核质、核仁、高尔基体等）的定位差异。此外，这些标注未区分实验验证（如ECO:0000269证据码）与计算推测的证据级别，导致模型训练和评估缺乏可信度参考。

上述缺口直接催生了CAPSUL的构建动机：**通过引入统一的三维结构表示与细粒度注释，系统性地验证结构特征在亚细胞定位任务中的关键作用**。具体而言，CAPSUL从AlphaFold2提取Cα坐标，并利用FoldSeek工具将结构token化为3Di tokens，同时将亚细胞注释细化为20个类别并对齐UniProt与HPA数据库，由领域专家验证。这一设计使得研究者能够首次在统一基准上比较序列模型与结构模型的性能差异，并利用注意力机制等工具发现与定位相关的结构模式（如α-螺旋），从而提升模型的生物学可解释性。

## 核心方法与创新机理

CAPSUL的核心创新在于将**蛋白质三维结构信息**与**细粒度亚细胞注释**系统性地引入定位预测任务，填补了现有数据集的空白。具体而言，其相对于传统基准的关键改进体现在以下三个维度。

### 从序列到结构的特征升级

现有亚细胞定位数据集（如DeepLoc）仅提供氨基酸序列，完全缺失三维结构信息。CAPSUL首次为每条蛋白质保留了完整的PDB文件，并提取了两类互补的结构表示：

- **Cα笛卡尔坐标**：从AlphaFold2预测结构中提取每个残基的α碳原子三维坐标，作为结构编码器的直接输入。
- **3Di结构tokens**：利用FoldSeek工具将三维结构离散化为结构token序列，使蛋白质语言模型能够以类似序列建模的方式处理结构信息。

这一设计使得CAPSUL成为首个同时支持序列编码器（如ESM-2、ESM-C）和结构编码器（如CDConv、GearNet-Edge）的统一基准。消融实验提供了决定性证据：随机打乱Cα坐标后，CDConv的Micro Avg F1-score从0.452降至0.329（−0.123），GearNet-Edge从0.417降至0.348（−0.069），证实**真实的三维空间信息是结构模型性能的关键驱动因素**（Table 4）。

### 从粗粒度到细粒度的注释细化

传统数据集通常采用10个粗粒度亚细胞类别，难以区分功能相近但定位不同的细胞器。CAPSUL将注释空间扩展为**20个细粒度类别**，由领域专家基于UniProt和HPA的定位信息精心整合与验证。这种细化使得模型需要学习更精细的定位模式——例如，将“核质”与“核仁”区分开，将“高尔基体”与“内质网”区分开——从而更真实地反映生物学复杂性。

### 证据级别的可信度标注

CAPSUL的另一独特设计是为每条定位注释附加**实验证据级别标签**：实验验证（ECO:0000269）标记为1，其他证据标记为2，无证据标记为0。这一机制允许研究者在训练和评估时按证据强度筛选数据，为模型的可靠性分析提供了前所未有的透明度。

![[assets/figures/papers/iclr26_0010_wJn4WbvSpK_CAPSUL_A_Comprehensive_Human_Protein_Benchmark_f/figures/001_Figure_1.jpg]]
*Figure 1: Procedures of CAPSUL dataset construction, including 3 key steps: Step 1 extracts and filters the sequence and structure data for each high-quality protein from AlphaFold2; Step 2 collects the annotations from UniProt and HPA for the resulting proteins in Step 1; Step 3 merges the structure data and the annotations for each protein, which consists of protein ID, localization annotations, amino acid sequence, sequence length, 3Di tokens, and Cα coordinates, etc*

CAPSUL的构建遵循一个三步流水线（见Figure 1），将高质量人类蛋白质的三维结构信息与细粒度亚细胞定位注释整合为统一的多模态数据记录。

**Step 1：序列与结构数据的提取与过滤。** 从AlphaFold2获取所有预测的人类蛋白质结构，随后进行三重过滤：仅保留在UniProt中标记为“active”的蛋白质，排除碎片化的结构预测，并确保每条蛋白质具备完整的PDB文件、Cα笛卡尔坐标以及通过FoldSeek工具生成的3Di结构token。该步骤的输出是每条蛋白质的氨基酸序列、Cα坐标序列和3Di token序列。

**Step 2：亚细胞定位注释的收集与整合。** 从UniProt和Human Protein Atlas（HPA）两个数据库交叉引用Step 1中蛋白质的亚细胞定位信息。由于两个数据库的术语体系存在差异，作者以《Molecular Biology of the Cell》（第7版）为参考，建立统一映射表（见Table 7），将原始注释归并为20个细粒度类别。同时，每条注释附带实验证据级别标签：实验验证（ECO:0000269）标记为1，其他证据标记为2，无证据标记为0。

**Step 3：数据合并。** 按蛋白质ID将Step 1的结构特征与Step 2的定位注释合并，形成CAPSUL的最终数据记录。每条记录包含：蛋白质ID、20类亚细胞定位的多标签注释及其证据级别、氨基酸序列、序列长度、3Di tokens和Cα坐标。

最终数据集按70:15:15的比例随机划分为训练集（14,126条）、验证集（3,027条）和测试集（3,028条）。Table 2给出了各亚细胞类别的正样本统计，正样本比例高度不平衡，约在0.5%至3%之间，这构成了后续基准测试的核心挑战之一。

在CAPSUL上评估的模型分为两大类：基于序列的方法（ESM-2 650M、ESM-C 600M及其变体、DeepLoc 2.1）和基于结构的方法（FoldSeek、CDConv、GearNet-Edge）。序列模型以氨基酸序列为输入，经编码器得到残基级嵌入后，通过均值池化获得蛋白质全局表示 $\bar{h} = \frac{1}{n} \sum_{i=1}^n h_i$，再由MLP分类器输出20类的预测概率。结构模型则将蛋白质表示为图 $\mathcal{G} = (\mathcal{V}, \mathcal{E})$，节点对应Cα原子，边基于空间邻近或序列相邻关系构建，通过图卷积网络更新节点表示 $m_i^{(l+1)} = \sigma\left( \sum_{j \in \mathcal{N}(i)} \mathbf{W}^{(l)} m_j^{(l)} + \mathbf{b}^{(l)} \right)$，经读出后同样由MLP分类器预测。所有模型统一采用二元交叉熵损失进行优化：

$$\mathcal{L}_{\mathrm{BCE}} = -\frac{1}{m} \sum_{i=1}^{m} \left[ y_i \log(\hat{y}_i) + (1 - y_i) \log(1 - \hat{y}_i) \right]$$

其中 $m$ 为类别数（20），$y_i$ 为真实标签，$\hat{y}_i$ 为预测概率。

### 蛋白质序列编码器

序列编码器将长度为 $n$ 的氨基酸序列映射为残基级嵌入。为获得固定长度的蛋白质全局表示，采用均值池化：

$$\bar{h} = \frac{1}{n} \sum_{i=1}^n h_i$$

其中 $h_i$ 为第 $i$ 个残基的嵌入向量，$\bar{h}$ 为蛋白质级表示。在全局表示之上，接一个多层感知机（MLP）分类器 $\phi(\cdot)$ 输出多标签预测：

$$\hat{y} = \phi(\bar{h})$$

基线中使用的序列编码器包括 ESM-2 (650M) 和 ESM-C (600M) 等预训练蛋白质语言模型。消融实验表明，未经预训练的 ESM-C 600M⁰ 性能显著劣于预训练版本（例如在细胞核 F1-score 上从 0.649 降至 0.555），验证了大规模序列预训练对亚细胞定位任务的关键作用。

### 蛋白质结构编码器

结构编码器将蛋白质三维结构建模为图 $G = (V, E)$，其中每个节点 $v_i$ 对应第 $i$ 个残基的 Cα 原子位置，边 $(v_i, v_j)$ 基于空间邻近性或序列邻接关系定义。图卷积网络（GCN）通过邻居聚合更新节点表示：

$$m_i^{(l+1)} = \sigma\left( \sum_{j \in \mathcal{N}(i)} \mathbf{W}^{(l)} m_j^{(l)} + \mathbf{b}^{(l)} \right)$$

其中 $m_i^{(l)}$ 为第 $l$ 层节点 $i$ 的表示，$\mathcal{N}(i)$ 为邻居集合，$\mathbf{W}^{(l)}$ 和 $\mathbf{b}^{(l)}$ 为可学习参数，$\sigma$ 为激活函数。

基线中评估了两种结构编码器：
- **CDConv**：基于图卷积的结构编码器，并扩展了 Transformer 模块以增强可解释性，在整体性能上表现最强（Micro Avg F1 达 0.452）。
- **GearNet-Edge**：另一种基于图卷积的结构编码器，性能略低于 CDConv（Micro Avg F1 为 0.417）。

此外，FoldSeek 作为基于预训练结构 tokenizer 的方法，将三维结构编码为 3Di tokens 后输入模型，但其 Micro Avg F1 仅为 0.248，显著弱于直接使用 Cα 坐标的图方法。

### 多标签分类损失函数

所有模型均采用二元交叉熵损失进行优化：

$$\mathcal{L}_{\mathrm{BCE}} = -\frac{1}{m} \sum_{i=1}^{m} \left[ y_i \log(\hat{y}_i) + (1 - y_i) \log(1 - \hat{y}_i) \right]$$

其中 $m$ 为类别数（20 个细粒度亚细胞定位类别），$y_i \in \{0, 1\}$ 为真实标签，$\hat{y}_i \in [0, 1]$ 为预测概率。该损失独立处理每个类别，天然适配多标签场景——单个蛋白质可同时定位于多个亚细胞区室。

### 类别不平衡缓解策略

CAPSUL 数据集中各类别的正样本比例极度不平衡（约 0.5% 至 3%），导致模型在少数类上难以做出正样本预测。为此引入三种重加权方案：

- **逆频率加权**：$w_c = \frac{1}{f_c}$，其中 $f_c$ 为类别 $c$ 的正样本频率。
- **对数逆频率加权**：$w_c = \frac{1}{\log(1 + f_c)}$，对极端频率进行平滑。
- **Focal Loss**：$\mathcal{L}_c = -w_c \cdot \sum_i \left[ y_{ic} \cdot (1 - \hat{y}_{ic})^{\gamma} \log(\hat{y}_{ic}) + (1 - y_{ic}) \cdot \hat{y}_{ic}^{\gamma} \log(1 - \hat{y}_{ic}) \right]$，通过聚焦参数 $\gamma$ 降低易分类样本的权重，使模型更关注困难样本。

实验表明，重加权策略使结构模型 CDConv 和 GearNet-Edge 首次在所有类别上均能识别出正样本。此外，对少数类别采用单标签分类策略（为每个类别独立训练二分类器）进一步提升了先前表现欠佳类别的预测性能，尤其对 GearNet-Edge 效果显著。

### 结构信息消融验证

为验证三维结构信息的因果作用，对结构模型进行 Cα 坐标随机打乱的消融实验：保持图拓扑不变，但将每个残基的 Cα 坐标随机置换为数据集中其他蛋白质的坐标。结果显示：
- CDConv 的 Micro Avg F1 从 0.452 降至 0.329（下降 0.123）
- GearNet-Edge 的 Micro Avg F1 从 0.417 降至 0.348（下降 0.069）

该显著下降确证了真实三维空间排布——而非仅图拓扑——是结构模型预测亚细胞定位的关键信息源。

## 实验与关键发现

### 核心瓶颈与因果机制

CAPSUL基准的核心发现围绕一个因果闭环展开：**蛋白质三维结构信息是亚细胞定位预测的关键瓶颈，而细粒度注释与实验证据级标注则构成了验证这一因果关系的必要条件**。现有的亚细胞定位数据集（如DeepLoc）仅提供氨基酸序列和粗粒度的10类注释，缺乏Cα坐标、3Di结构tokens等三维特征，直接阻碍了基于结构的预测模型开发。CAPSUL通过引入Cα坐标与FoldSeek导出的3Di tokens，并将亚细胞分类细化为20个经领域专家验证的类别，同时区分实验验证（ECO:0000269）与其他证据来源，构建了可验证结构-定位因果关联的基准。

**决定性证据**来自Cα坐标随机采样的消融实验（Table 4）：将CDConv和GearNet-Edge的真实Cα坐标替换为随机采样值后，CDConv的Micro Avg F1从0.452骤降至0.329（−0.123），GearNet-Edge则从0.417降至0.348（−0.069）。这一显著且一致的性能退化表明，**真实的三维空间排布——而非蛋白质序列本身——是模型捕捉定位信号的核心信息来源**。值得注意的是，结构模型的退化幅度（CDConv约27%，GearNet-Edge约17%）提示不同结构编码器对空间信息的依赖程度存在差异，CDConv对坐标完整性的敏感度更高。

![[assets/figures/papers/iclr26_0010_wJn4WbvSpK_CAPSUL_A_Comprehensive_Human_Protein_Benchmark_f/figures/006_Table_4.jpg]]
*Table 4: Ablation study of CDConv and GearNet-Edge to randomly sample Cα coordinates*

### 序列预训练的增益与局限

序列模型的对比实验揭示了预训练的重要性与根本局限。ESM-C 600M（预训练版本）在Nucleus类别上取得0.649的F1-score，而未预训练的ESM-C 600M0仅为0.555，差距达+0.094（Table 3）。这一结果表明，大规模蛋白质序列预训练确实为定位任务提供了有益的先验知识。然而，**即便经过预训练，序列模型仍无法完全捕捉与三维结构相关的定位信号**——结构模型CDConv（Micro Avg F1 0.452）虽整体低于ESM-C（0.494），但在特定类别上展现出序列模型难以企及的优势，例如高尔基体（Golgi Apparatus）预测达到100%精确率。这暗示结构特征在少数特定亚细胞区室的定位中具有不可替代的判别能力。

![[assets/figures/papers/iclr26_0010_wJn4WbvSpK_CAPSUL_A_Comprehensive_Human_Protein_Benchmark_f/figures/004_Table_3.jpg]]
*Table 3: Overall performance of sequence-based, structure-based methods on CAPSUL*

### 类别不平衡与缓解策略

CAPSUL数据集的正样本比例高度不平衡（约0.5%–3%），导致模型在多数类别上表现尚可，但在少数类上难以做出有效的正样本预测。**这是该基准最突出的失败模式**：在标准多标签设置下，结构模型CDConv和GearNet-Edge在部分少数类别上完全无法识别任何正样本，Recall为0。

为缓解这一问题，研究评估了三类重加权策略（逆频率、对数逆频率、Focal Loss）和单标签分类策略：

- **重加权策略**（Table 5）：使得结构模型首次在所有类别上均能识别出正样本，但代价是精确率下降。以ESM-C 600M为例，重加权后Micro Avg F1从0.494降至0.448，说明简单的权重调整在提升少数类召回的同时损害了整体性能。
- **单标签分类策略**（Table 6）：对先前表现欠佳的类别采用独立的二分类器训练，取得了更显著的改善。GearNet-Edge在多个少数类上的F1-score明显提升，且该方法被作者评价为“一个有前景且实用的解决方案”。然而，宏平均F1仍处于较低水平，表明类别不均衡问题的根本性解决仍需探索。

### 结构质量与预测性能的关联

消融实验进一步确认了输入结构质量对预测性能的直接影响（Table 9）：使用AlphaFold2预测的结构作为输入时，CDConv的Micro Avg F1为0.527，而使用Boltz-2预测的结构时降至0.477。这一差距验证了CAPSUL选择AlphaFold2结构作为数据源的技术合理性，同时也暗示**蛋白质结构预测精度的提升将直接转化为亚细胞定位预测性能的增益**。

### 可解释性：从注意力到结构模式

CDConv通过在GCN基础上扩展Transformer模块，实现了残基级注意力权重的提取与可视化，这是该基准在可解释性方面的重要贡献。针对高尔基体定位蛋白的案例分析（Figure 2, Figure 4）显示，CDConv的注意力机制成功识别出与定位功能相关的α-螺旋结构域——注意力得分最高的20个残基在空间上恰好对应于跨膜α-螺旋区域。对于MFNG、B3GALT2和GIMAP1三个代表性蛋白，全注意力得分与蛋白质三维结构的对应关系（Figure 4）进一步验证了模型捕捉结构-定位关联的能力。这一发现将预测性能与生物学机制直接关联，为后续的因果发现研究奠定了基础。

![[assets/figures/papers/iclr26_0010_wJn4WbvSpK_CAPSUL_A_Comprehensive_Human_Protein_Benchmark_f/figures/010_Figure_2.jpg]]
*Figure 2: Visualization of the top 20 attention-scored residues of the three representative proteins*

![[assets/figures/papers/iclr26_0010_wJn4WbvSpK_CAPSUL_A_Comprehensive_Human_Protein_Benchmark_f/figures/026_Figure_4.jpg]]
*Figure 4: Visualization of full attention scores and structures of proteins MFNG, B3GALT2, and GIMAP1, where the residues of known pattern α-helix are highlighted*

### 样本效率分析

样本效率曲线（Figure 3）表明，CDConv在训练数据量增加时性能持续提升，但增益逐渐趋于平缓。这一趋势提示，在现有数据规模下，模型可能已接近当前结构表征能力的上限，进一步提升性能需要更丰富或更鲁棒的结构表征方法。

### 需要手动验证的要点

以下结论的支撑证据在提供材料中不够完整，建议对照原文确认：
- Table 3中ESM-C 600M与ESM-2 650M在全部18个类别上的逐类F1对比（仅提供了Nucleus的数值）。
- 重加权策略中三种方案的详细消融对比（逆频率、对数逆频率、Focal Loss的相对优劣）。
- 单标签分类策略在核膜（Nuclear Membrane）等极端少数类上的具体表现。

![[assets/figures/papers/iclr26_0010_wJn4WbvSpK_CAPSUL_A_Comprehensive_Human_Protein_Benchmark_f/figures/002_Table_1.jpg]]
*Table 1: Comparisons between existing datasets and CAPSUL*

## 定位与知识库关联

### 与现有工作的关系

CAPSUL在亚细胞定位预测领域填补了结构信息缺失的关键空白。传统的亚细胞定位数据集（如DeepLoc、setHARD）仅提供氨基酸序列和粗粒度定位标签，而CAPSUL首次系统性地引入蛋白质三维结构特征——包括Cα笛卡尔坐标和FoldSeek生成的3Di结构tokens——并与20类细粒度亚细胞注释对齐。这使得CAPSUL成为连接基于序列的蛋白质语言模型（如ESM-2 650M、ESM-C 600M）与基于结构的图神经网络编码器（如CDConv、GearNet-Edge）的桥梁基准。

在基准方法选择上，CAPSUL覆盖了从传统专用工具到最新预训练模型的完整谱系：
- **DeepLoc 2.1** 作为领域专用预测工具的代表，提供了与通用蛋白质语言模型的对照基线；
- **ESM-2 (650M)** 和 **ESM-C (600M)** 分别代表不同代的预训练序列模型，其中ESM-C在多数亚细胞类别上取得了更高的F1分数（如Nucleus类别：ESM-C 0.649 vs. ESM-2 0.609），验证了更大规模预训练对定位任务的增益；
- **FoldSeek** 作为基于预训练结构tokenizer的方法，其性能显著弱于CDConv和GearNet-Edge（Micro Avg F1仅为0.248），表明单独使用3Di tokens不足以捕捉定位相关的结构信号；
- **CDConv** 和 **GearNet-Edge** 作为直接操作Cα坐标图的结构编码器，展现出与序列模型互补的优势，尤其CDConv在Golgi apparatus预测上达到100%精确率，并通过注意力机制成功识别出α-螺旋定位模式。

### 适用边界

CAPSUL的适用性受以下边界条件约束：

**物种范围**：当前数据集仅覆盖人类蛋白质组，尚未扩展至其他物种。这意味着基于CAPSUL训练的模型在跨物种迁移场景下的表现需要谨慎评估，物种间的比较分析有待后续工作展开。

**结构数据来源**：CAPSUL依赖AlphaFold2预测的静态结构。消融实验表明，使用AlphaFold2预测的结构作为输入优于Boltz-2预测的结构（Micro Avg F1: 0.527 vs. 0.477），确认了所选结构数据的质量基线。然而，这同时意味着CAPSUL无法直接建模蛋白质在不同生化环境或翻译后修饰状态下的动态构象变化，限制了其在上下文依赖的亚细胞定位预测中的应用。

**类别不平衡**：CAPSUL中多数亚细胞类别的正样本比例仅为0.5%–3%，导致模型在不同类别间的性能差异显著。虽然重加权策略（逆频率、对数逆频率、Focal Loss）和单标签分类策略在一定程度上缓解了少数类的预测困难——使CDConv和GearNet-Edge能够对所有类别做出正样本预测——但整体宏平均F1仍然较低，表明类别不均衡问题尚未根本解决。

### 局限与开放问题

**根本局限**：CAPSUL的核心瓶颈在于静态结构与动态定位之间的本质张力。蛋白质的亚细胞定位往往受翻译后修饰、互作伙伴、细胞周期阶段等上下文因素调控，而当前数据集中仅包含单一的预测构象，无法捕捉这些动态维度。此外，注意力分析揭示的潜在定位模式——如α-螺旋跨膜结构域、“W-pair”残基对、N端柔性区——仍需独立的生物学实验验证，其因果性尚未确立。

**开放问题**：

1. **极端类别不平衡的突破路径**：在正样本比例低至0.5%的条件下，单标签分类和重加权策略虽有效果，但并未完全解决问题。能否通过元学习、少样本学习或主动采样策略进一步提升少数类的预测性能？

2. **多模态信息的统一与解耦**：CAPSUL同时提供氨基酸序列、Cα坐标和3Di tokens三种模态。当前方法或单独使用序列、或单独使用结构，尚未有效融合多模态信息。如何统一或解耦这些表征，以更准确地捕捉亚细胞定位的决定因素，并提升模型的可解释性？

3. **结构表征的丰富度**：现有结构编码器（CDConv、GearNet-Edge）主要基于Cα原子图。能否开发更丰富的结构表征——例如纳入侧链信息、表面电荷分布或溶剂可及性——以捕捉更精细的定位信号？

4. **动态扩展路径**：当未来蛋白质结构数据库中包含更多动态数据（如不同pH、不同互作状态下的构象）时，CAPSUL如何扩展以支持上下文依赖的亚细胞定位预测？这需要从数据集构建到模型设计的系统性更新。

## 原文 PDF

![[paperPDFs/ICLR_2026/CAPSUL_A_Comprehensive_Human_Protein_Benchmark_for_Subcellular_Localization.pdf]]
