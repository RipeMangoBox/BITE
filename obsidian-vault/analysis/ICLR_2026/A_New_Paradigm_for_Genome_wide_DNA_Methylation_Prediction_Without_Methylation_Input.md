---
title: "A New Paradigm for Genome-wide DNA Methylation Prediction Without Methylation Input"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/A_New_Paradigm_for_Genome_wide_DNA_Methylation_Prediction_Without_Methylation_Input.pdf
aliases:
- NPGWDMPWMI
- MethylProphet
tags:
- ICLR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/genetics_cell_biology_health_etc
core_operator: "利用基因表达谱（约25000个基因）作为全局生物学状态信号，结合局部CpG序列上下文（1kb窗口），通过瓶颈MLP和DNA分词器编码，并由Transformer融合，直接预测位点特异性甲基化水平，无需任何部分测量的DNAm输入。"
primary_logic: "基因表达与DNA甲基化之间存在强相关性，通过压缩全转录组表达谱并编码局部序列上下文，可以训练一个基础模型，在完全不依赖目标样本中任何实验测量的DNAm的情况下，推断全基因组甲基化图谱。"
claims:
- "MethylProphet在ENCODE数据集上，对于未见过的CpG位点和未见过的样本，实现了中位跨样本皮尔逊相关系数（MAS-PCC）0.72。"
- "在TCGA数据上，MethylProphet在Train CpG - Val Sample分割中，MAS-PCC达到0.5455，MAC-PCC达到0.9320，显著优于基于CNN的注意力模型（Levy-Jurgenson et al., 2019b）。"
- "在ENCODE和TCGA的'Val CpG - Train Sample'分割中，MethylProphet的MAS-PCC和MAC-PCC均高于DeepCPG、CpGPT和MethylGPT。"
- "MethylProphet在缺失上下文CpG数据时表现稳定，而CpGPT和MethylGPT的性能随可用CpG减少而显著下降。"
---

# A New Paradigm for Genome-wide DNA Methylation Prediction Without Methylation Input

> [!tip] 核心洞察
> 基因表达与DNA甲基化之间存在强相关性，通过压缩全转录组表达谱并编码局部序列上下文，可以训练一个基础模型，在完全不依赖目标样本中任何实验测量的DNAm的情况下，推断全基因组甲基化图谱。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 无需甲基化输入的全基因组DNA甲基化预测新范式 |
| 英文题名 | A New Paradigm for Genome-wide DNA Methylation Prediction Without Methylation Input |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=8wQ7Oc08vo) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/genetics_cell_biology_health_etc |
| Method | MethylProphet |
| Dataset | ENCODE |

> [!tip] 效果简介
> - ENCODE 上，MAS-PCC 为 0.3436，对比 0.2878 (Levy-Jurgenson)，变化 +0.0558。
> - ENCODE 上，MAC-PCC 为 0.9398，对比 0.8355 (Levy-Jurgenson)，变化 +0.1043。
> - ENCODE 上，MSE 为 0.0079，对比 0.0182 (Levy-Jurgenson)，变化 -0.0103。

## 概述

现有DNA甲基化（DNAm）分析面临一个根本瓶颈：技术成本与覆盖度之间的矛盾。阵列平台仅能测量人类基因组约2800万个CpG位点中的1-3%，而全基因组亚硫酸氢盐测序（WGBS）成本高昂，导致绝大多数CpG位点在典型数据集中未被测量。本文提出MethylProphet，一种无需任何部分测量的DNAm输入即可预测全基因组甲基化图谱的新范式。

核心洞察在于利用基因表达与DNA甲基化之间的强相关性：通过瓶颈MLP压缩全转录组表达谱（约25000个基因），结合DNA分词器编码CpG位点周围的1kb局部序列上下文，再由Transformer编码器融合这些表示，直接预测位点特异性甲基化水平。该方法从根本上改变了输入范式——从依赖部分测量DNAm的“插补”转变为仅需基因表达和DNA序列的“预测”，从而将覆盖范围从约3%扩展到100%的基因组。

主要结果如下：在ENCODE数据集上，MethylProphet对未见过的CpG位点和未见过的样本实现了中位跨样本皮尔逊相关系数（MAS-PCC）0.72；在TCGA数据上，其MAS-PCC达0.5455，MAC-PCC达0.9320，显著优于基于CNN的注意力模型（Levy-Jurgenson et al., 2019b）。与需要部分DNAm输入的DeepCPG、CpGPT和MethylGPT相比，MethylProphet在缺失上下文CpG数据时性能保持稳定，而其他方法性能显著下降。消融实验表明，结合Array、EPIC和WGBS多源数据可进一步提升性能，且增加训练数据规模（添加更多染色体）能增强泛化能力。

本文作为概念验证研究，未提出全新架构，且模型在TCGA数据上对完全未见过的CpG位点和样本的泛化性能（Val CpG - Val Sample分割）相对较低（MAS-PCC为0.39），这是当前主要局限。

## 背景与动机

DNA甲基化（DNAm）是调控基因表达的关键表观遗传修饰，但现有测量技术存在严重的覆盖度与成本矛盾。阵列平台（如Illumina 450K/EPIC）仅能覆盖人类基因组约2800万个CpG位点中的1–3%，而全基因组亚硫酸氢盐测序（WGBS）虽能提供全基因组覆盖，但实验成本极高，导致绝大多数CpG位点在典型数据集中未被测量。这种数据稀疏性构成了从有限测量样本推断全基因组甲基化图谱的根本瓶颈。

现有方法主要采用插补（imputation）范式，即利用已测量的部分CpG位点作为输入，预测未测量位点的甲基化水平。代表性方法包括DeepCpG（基于深度学习的插补）、CpGPT和MethylGPT（基于掩码生成式Transformer的插补）。这些方法的共同缺陷在于：它们依赖目标样本中至少一部分实验测量的DNAm值作为输入。当面对全新样本或未见过的CpG位点时，插补方法的预测能力急剧下降，因为其核心机制是填充缺失值而非从零推断。

本文的核心洞察在于：基因表达与DNA甲基化之间存在强相关性，这种跨模态关联可以被系统性地利用。具体而言，全转录组基因表达谱（约25000个基因）编码了样本的全局生物学状态，而局部CpG序列上下文（1kb窗口）提供了位点特异性信息。通过瓶颈MLP压缩高维表达谱、DNA分词器（BPE）编码局部序列、并融合CpG岛上下文（岛、岸、架、公海）和染色体指示嵌入，Transformer编码器可以学习从这些信号到位点特异性甲基化水平的映射。

这一范式转换的关键因果旋钮在于：**完全消除对实验测量的DNAm输入的依赖**。MethylProphet仅需基因表达和DNA序列即可预测任意CpG位点的甲基化水平，即使该位点从未在任何样本中被测量过。这从根本上改变了DNAm分析的可用性——用户只需拥有匹配的基因表达数据（通常更易获取且成本更低），即可获得全基因组甲基化图谱，而无需进行任何湿实验甲基化测序。

实验证据支持这一范式的可行性。在ENCODE数据集上，MethylProphet在“Val CpG - Train Sample”分割（即预测未见过的CpG位点）中实现了中位跨样本皮尔逊相关系数（MAS-PCC）0.72。在TCGA数据上，其在“Train CpG - Val Sample”分割中的MAS-PCC达到0.5455，MAC-PCC达到0.9320，显著优于基于CNN的注意力模型（Levy-Jurgenson et al., 2019b）。更重要的是，在“Val CpG - Train Sample”分割中，MethylProphet的MAS-PCC和MAC-PCC均高于DeepCpG、CpGPT和MethylGPT等需要部分DNAm输入的方法。当上下文CpG数据完全缺失时，MethylProphet性能保持稳定（MAC-PCC保持0.88），而CpGPT和MethylGPT的性能随可用CpG减少而显著下降。

然而，本文应被视为一项概念验证研究。模型在TCGA数据上对未见过的CpG位点和样本的泛化性能（Val CpG - Val Sample分割）相对较低（跨样本PCC为0.39），表明跨样本泛化仍是开放挑战。此外，模型依赖基因表达数据，对于没有匹配表达谱的样本无法应用，且未在非人类物种或单细胞数据上评估。

## 核心创新

MethylProphet 的核心创新在于彻底改变了 DNA 甲基化（DNAm）预测的输入范式。传统方法（如 DeepCpG, CpGPT, MethylGPT）遵循“插补”范式，即依赖目标样本中部分已测量的 DNAm 值作为输入，来推断该样本中其他未测量的 CpG 位点的甲基化水平。MethylProphet 则完全抛弃了这一依赖，提出了一种“零甲基化输入”的新范式：仅利用样本的全转录组基因表达谱（约 25,000 个基因）和目标 CpG 位点的局部 DNA 序列上下文（1kb 窗口）以及基因组注释（CpG 岛上下文、染色体指示），即可直接预测该位点的甲基化水平。这一改变从根本上解决了现有方法无法应用于那些没有预先测量任何 DNAm 的新样本的瓶颈。

为实现这一新范式，MethylProphet 引入了几个关键的设计创新。首先，它采用一个瓶颈多层感知机（bottleneck MLP）来压缩高维的全转录组基因表达谱，将其编码为一个紧凑的潜在嵌入。这背后的因果洞察是：基因表达与 DNA 甲基化之间存在强相关性，全转录组表达谱可以作为全局生物学状态的代理信号。其次，对于局部 CpG 位点，它使用一个受 DNABERT-2 启发的 DNA 分词器（基于字节对编码 BPE）来编码其周围的 DNA 序列，替代了以往简单的固定 ID 或序列编码。此外，模型还整合了 CpG 岛上下文（岛、岸、架、公海）和染色体指示的可学习嵌入，为 Transformer 编码器提供了丰富的基因组位置信息。最终，所有这些嵌入被拼接并输入到一个 Transformer 编码器中，通过自注意力机制进行融合，并输出对目标 CpG 位点的甲基化预测。

与现有基线方法相比，这些改变带来了显著的性能提升。在 ENCODE 和 TCGA 数据集上，MethylProphet 在多个评估指标上均优于基于 CNN 的注意力模型（Levy-Jurgenson et al., 2019b）。例如，在 TCGA 数据上，其跨样本中位皮尔逊相关系数（MAS-PCC）达到 0.5455，而基线仅为 0.2630；跨 CpG 中位皮尔逊相关系数（MAC-PCC）达到 0.9320，基线为 0.6325。在与同样依赖部分 DNAm 输入的插补方法（DeepCpG, CpGPT, MethylGPT）的直接比较中，MethylProphet 在“未见 CpG 位点-已见训练样本”这一最关键的泛化分割上，取得了最高的 MAS-PCC 和 MAC-PCC。更重要的是，当上下文 CpG 数据完全缺失时（即可用 CpG 比例为 0%），CpGPT 和 MethylGPT 的性能急剧下降，而 MethylProphet 的性能保持稳定（MAC-PCC 维持在 0.88），这强有力地证明了其不依赖 DNAm 输入的核心优势。

## 整体框架

![[assets/figures/papers/iclr26_0003_8wQ7Oc08vo_A_New_Paradigm_for_Genome-wide_DNA_Methylation_P/figures/004_Figure_2.jpg]]
*Figure 2: Overview of our proposed pipeline. (a) Model architecture of MethylProphet; (b) The learnable Global, chromosome, and CPG island-related embeddings; (c) Model architecture of efficient gene profile compression MLP; (d) DNA Tokenizer for CpG-specific DNA sequence; (e) Model architecture of the Transformer encoder that aggregates all the embeddings*

MethylProphet 的核心设计目标是在完全不依赖任何实验测量的 DNA 甲基化（DNAm）输入的情况下，从基因表达谱和局部序列上下文推断全基因组 CpG 位点的甲基化水平。其整体 pipeline 遵循一种“样本级生物学状态 + 位点级基因组上下文”的双路融合范式，从根本上区别于依赖部分甲基化值进行插补的现有方法（如 DeepCpG、CpGPT、MethylGPT）。

**输入流与数据瓶颈：** 模型接收两类主要输入。第一类是样本的全转录组基因表达谱 $G \in \mathbb{R}^{N_g \times N_s}$，约包含 25,000 个基因，作为全局生物学状态的代理信号。这是解决现有 DNAm 分析瓶颈（即大多数 CpG 位点未被测量）的关键因果旋钮——利用基因表达与 DNAm 之间的强相关性来推断缺失的甲基化信息。第二类是目标 CpG 位点的局部 DNA 序列上下文（以 CpG 为中心的 1kb 窗口）以及基因组注释（CpG 岛上下文和染色体指示）。这种设计将全局信号与位点特异性特征结合，使得模型能够泛化到未见过的 CpG 位点和未见过的样本。

**核心处理模块（Pipeline）：**
1.  **基因表达瓶颈 MLP：** 将高维的基因表达谱（约 25,000 个基因）通过一个瓶颈多层感知机压缩为紧凑的潜在嵌入 $x_{\text{gene}}$。该模块负责提取与甲基化调控相关的关键转录组信号，并降低维度以避免过拟合。
2.  **CpG 序列 DNA 分词器：** 受 DNABERT-2 启发，使用变长字节对编码（BPE）方案对 CpG 位点周围的 1kb DNA 序列进行分词，生成一系列 DNA 序列令牌嵌入 $\{ x_j^{\text{DNA}} \}_{j=1}^{L}$。这替代了传统的固定长度或简单 one-hot 编码，能更有效地捕获局部序列模式。
3.  **基因组上下文嵌入：** 为每个 CpG 位点提供可学习的染色体嵌入 $x_{\text{chr}}$ 和 CpG 岛上下文嵌入（岛、岸、架、公海）$x_{\text{CGI}}$。这些注释为模型提供了基因组位置和调控区域类型的先验信息。
4.  **输入嵌入拼接：** 所有嵌入被拼接成一个统一的序列 $Z_i = [ x_{\text{GLB}}, x_{\text{gene}}, \{ x_j^{\text{DNA}} \}_{j=1}^{L}, x_{\text{CGI}}, x_{\text{chr}} ]$，其中 $x_{\text{GLB}}$ 是一个可学习的全局令牌，用于聚合整个序列的上下文信息。
5.  **Transformer 编码器：** 一个标准的 Transformer 编码器通过自注意力机制融合上述所有嵌入。全局令牌的最终状态捕获了用于预测的融合表示。
6.  **DNAm 预测头：** 对全局令牌的最终状态应用一个线性层加 sigmoid 激活函数，输出预测的甲基化水平 $\hat{y}_i \in [0,1]$。

**输出流：** 对于每个输入（一个样本-位点对），模型输出一个标量值，代表该特定 CpG 位点的预测 β 值。通过批量处理，模型可以为给定样本的所有 CpG 位点生成全基因组甲基化图谱。

**证据强度与关键结果：** 该 pipeline 的有效性在多个基准测试中得到验证。在 ENCODE 数据上，MethylProphet 在“Val CpG - Train Sample”分割（即预测未见过的 CpG 位点）中实现了中位跨样本皮尔逊相关系数（MAS-PCC）0.72。在 TCGA 数据上，其在“Train CpG - Val Sample”分割中的 MAS-PCC 为 0.5455，MAC-PCC 为 0.9320，显著优于基于 CNN 的注意力模型。值得注意的是，在缺失上下文 CpG 数据的鲁棒性测试中，MethylProphet 的性能保持稳定，而 CpGPT 和 MethylGPT 的性能则显著下降，这直接证明了其不依赖甲基化输入的范式优势。

## 核心模块与公式推导

MethylProphet 的核心模块围绕“无需任何测量的 DNAm 输入”这一范式转变设计。模型的核心洞察在于利用全转录组表达谱作为全局生物学状态信号，结合 CpG 位点周围的局部 DNA 序列上下文，通过一个 Transformer 编码器融合这些信息，直接预测位点特异性甲基化水平。其输入输出形式可表示为：

$$f_{\theta} : ( \mathcal{G}, S_i, a_i ) \mapsto \hat{y}_i \in [0,1]$$

其中 $\mathcal{G}$ 是样本的基因表达向量，$S_i$ 是目标 CpG 位点 $i$ 周围的 DNA 序列，$a_i$ 是辅助基因组注释（如 CpG 岛上下文和染色体指示），$\hat{y}_i$ 是预测的甲基化水平（β 值，范围 [0,1]）。

模型由五个核心模块构成：

1.  **基因表达瓶颈 MLP**：该模块将高维基因表达谱 $G \in \mathbb{R}^{N_g \times N_s}$（约 25,000 个基因）压缩为一个紧凑的潜在嵌入 $x_{\text{gene}}$。这是模型的关键瓶颈，它迫使模型从全局转录组状态中提取与甲基化预测最相关的信息，而非依赖局部或部分测量的甲基化信号。压缩后的嵌入作为全局生物学上下文输入后续的 Transformer。

2.  **CpG 序列 DNA 分词器**：对于每个目标 CpG 位点，该模块提取其周围 1kb 的 DNA 序列上下文，并使用受 DNABERT-2 启发的字节对编码（BPE）分词方案将其编码为一系列令牌嵌入 $\{ x_j^{\text{DNA}} \}_{j=1}^{L}$。这提供了局部序列特征，如基序、GC 含量和重复序列，这些特征与甲基化倾向密切相关。

3.  **基因组上下文嵌入**：该模块整合了 CpG 岛上下文（岛、岸、架、公海）的指示嵌入 $x_{\text{CGI}}$ 和染色体指示嵌入 $x_{\text{chr}}$。这些注释为模型提供了重要的基因组位置先验知识，因为 CpG 岛及其周边区域的甲基化模式具有显著的结构性差异。

4.  **Transformer 编码器**：所有嵌入被拼接成一个统一的输入序列：
    $$Z_i = [ x_{\text{GLB}}, x_{\text{gene}}, \{ x_j^{\text{DNA}} \}_{j=1}^{L}, x_{\text{CGI}}, x_{\text{chr}} ]$$

    其中 $x_{\text{GLB}}$ 是一个可学习的全局令牌。Transformer 编码器通过自注意力机制融合这些来自不同模态的信息，输出上下文相关的表示。全局令牌的最终状态聚合了全局表达、局部序列和基因组位置信息。

5.  **DNAm 预测头**：对全局令牌的最终状态应用一个线性层和 sigmoid 激活函数，输出最终的甲基化水平预测 $\hat{y}_i$。

**关键公式变量含义**：
- $M \in \mathbb{R}^{N_{CpG} \times N_s}$: DNA 甲基化矩阵，条目为 β 值（范围 [0,1]）
- $G \in \mathbb{R}^{N_g \times N_s}$: 基因表达矩阵
- $\mathcal{G}$: 单个样本的基因表达向量
- $S_i$: CpG 位点 $i$ 周围的 DNA 序列
- $a_i$: CpG 位点 $i$ 的辅助注释（CpG 岛上下文、染色体）
- $x_{\text{GLB}}$: 可学习的全局令牌嵌入
- $x_{\text{gene}}$: 瓶颈 MLP 输出的基因表达压缩嵌入
- $\{ x_j^{\text{DNA}} \}_{j=1}^{L}$: DNA 分词器输出的序列令牌嵌入序列
- $x_{\text{CGI}}$: CpG 岛上下文嵌入
- $x_{\text{chr}}$: 染色体嵌入

该架构的核心创新在于其输入范式：它完全摒弃了传统插补方法所需的局部测量 DNAm 输入，转而利用全局基因表达和局部序列上下文。这使得模型能够预测任意 CpG 位点（包括未在训练集中出现的位点）和任意样本（包括未在训练集中出现的样本）的甲基化水平，从根本上解决了 DNAm 数据覆盖度不足和成本高昂的瓶颈问题。

## 实验与分析

MethylProphet的核心实验设计围绕其最关键的因果旋钮展开：能否在完全不依赖任何实验测量的DNA甲基化（DNAm）输入的情况下，仅通过基因表达和局部序列上下文预测位点特异性甲基化水平。为此，实验设置了四种数据分割方式（Train/Val CpG × Train/Val Sample），系统地测试模型对未见CpG位点、未见样本以及两者均未见情况下的泛化能力。基准方法包括Levy-Jurgenson等人（2019b）的CNN注意力模型（同样使用基因表达和序列，但未采用全转录组压缩和Transformer融合），以及DeepCPG、CpGPT、MethylGPT等需要部分DNAm输入作为上下文的插补方法。

**主结果与定量比较。** 在ENCODE数据集（95个正常样本，约2700万CpG位点）上，MethylProphet在所有四个评价指标上均显著优于Levy-Jurgenson模型（Table 4）。例如，在“Train CpG - Val Sample”分割中，MethylProphet的中位跨样本皮尔逊相关系数（MAS-PCC）为0.3436，而基线为0.2878；中位跨CpG皮尔逊相关系数（MAC-PCC）达到0.9398，基线仅为0.8355；均方误差（MSE）从0.0182降至0.0079，平均绝对误差（MAE）从0.0875降至0.0608。在TCGA数据（9,194个癌症样本，染色体1约4万个CpG位点）上，性能差距更为显著（Table 5）：MethylProphet的MAS-PCC为0.5455，MAC-PCC为0.9320，而Levy-Jurgenson模型的MAS-PCC仅为0.2630，MAC-PCC为0.6325，MSE和MAE分别降低了约4.4倍和2.4倍。这一差距的核心原因在于MethylProphet采用了瓶颈MLP压缩全转录组（约25000个基因）的表达谱，而基线模型仅使用了有限数量的基因特征——全转录组压缩提供了更完整的全局生物学状态信号。

![[assets/figures/papers/iclr26_0003_8wQ7Oc08vo_A_New_Paradigm_for_Genome-wide_DNA_Methylation_P/figures/007_Table_4.jpg]]
*Table 4: Performance comparison on ENCODE data. Four evaluation metrics are included: medianacross-sample PCC (MAS-PCC), median-across-sample PCC (MAS-PCC), mean square error (MSE), and mean absolute error (MAE)*

![[assets/figures/papers/iclr26_0003_8wQ7Oc08vo_A_New_Paradigm_for_Genome-wide_DNA_Methylation_P/figures/008_Table_5.jpg]]
*Table 5: Performance comparison on TCGA data*

在与需要部分DNAm输入的插补方法对比中（Table 6，“Val CpG - Train Sample”分割），MethylProphet在ENCODE上以MAS-PCC 0.3689领先于CpGPT（0.3192）和MethylGPT（0.2964），而DeepCPG几乎失效（0.0317）。在TCGA上，MethylProphet的MAS-PCC（0.5453）几乎是CpGPT（0.3167）的两倍。值得注意的是，在MAC-PCC指标上，所有方法在ENCODE上表现接近（0.89-0.94），说明跨CpG的相关性主要由CpG位点本身的序列特征驱动；但跨样本的泛化能力（MAS-PCC）则显著依赖于模型对基因表达信息的利用效率。

**消融实验与因果机制验证。** 消融实验揭示了几个关键因果机制：

1. **基因表达编码策略**（Table 9）：瓶颈MLP编码策略优于其他基因编码方法，验证了全转录组压缩的有效性。这是MethylProphet最关键的创新点——通过瓶颈结构强制模型学习表达谱中的全局模式，而非简单的特征选择。

2. **数据规模与来源**（Table 7, 8）：结合Array、EPIC和WGBS三种数据源可获得最佳性能，在三个分割中MAS-PCC分别为0.54、0.42和0.39。增加训练数据规模（添加更多染色体）持续提升模型泛化能力（Table 8），表明模型具有数据扩展性。

3. **基因组注释的重要性**（Table 10）：去除CpG岛上下文（岛、岸、架、公海）和染色体嵌入会降低性能，说明局部基因组上下文提供了重要的先验信息，帮助模型区分不同基因组区域的甲基化模式差异。

4. **对上下文CpG缺失的鲁棒性**（Table 14, 15）：当可用上下文CpG比例从100%降至0%时，MethylProphet的MAC-PCC稳定维持在0.88，而CpGPT和MethylGPT的性能显著下降（例如CpGPT的MAC-PCC从0.94降至0.69）。这一结果直接验证了MethylProphet的核心优势——它不依赖任何测量的DNAm输入，因此不会受到插补方法在数据稀疏时性能崩溃的限制。

**失败模式与泛化边界。** 模型最困难的任务是“Val CpG - Val Sample”分割（同时预测未见CpG位点和未见样本），在TCGA上MAS-PCC降至0.39。这一性能瓶颈表明，当前模型对完全新样本和新位点的联合泛化仍存在局限，可能受限于训练数据中组织/癌症类型的覆盖度。此外，在ENCODE WGBS数据上，模型在“Val CpG - Train Sample”分割中MAS-PCC达到0.72（Table 7），但在其他分割中表现不一，部分原因可能是ENCODE中有限的测试样本数量（95个样本）导致统计波动。模型在TCGA数据上的跨样本PCC分布（Figure 10, 12）显示，不同癌症类型间的预测准确性存在差异，但论文未进行系统性的公平性分析。

**重要图表结论。** Figure 4展示了ENCODE数据上的交叉验证结果，包括跨CpG PCC、跨样本PCC和UMAP可视化，验证了预测的甲基化信号在CpG岛内保持相关性结构。Figure 12在TCGA上进一步展示了预测值与实测值在细胞类型差异、差异甲基化区域（DMR）重叠比例等方面的一致性。Figure 5展示了一个示例，说明DNAm与最近基因表达呈负相关（Spearman相关系数-0.30），为跨模态预测提供了生物学基础。Figure 6的Kaplan-Meier生存曲线表明，结合基因表达和预测DNAm的特征比仅使用基因表达能更显著地分离TCGA-BRCA患者的高/低风险组（log-rank p值从0.018降至0.0003），验证了预测甲基化谱的生物学意义和应用价值。

总体而言，MethylProphet在不需要任何DNAm输入的前提下，实现了与甚至优于需要部分DNAm输入的插补方法的性能，特别是在跨样本泛化和数据稀疏场景下表现出显著优势。然而，其最困难的泛化场景（Val CpG - Val Sample）的性能仍有限，需要进一步验证和优化。

### 补充图表

![[assets/figures/papers/iclr26_0003_8wQ7Oc08vo_A_New_Paradigm_for_Genome-wide_DNA_Methylation_P/figures/001_Table_1.jpg]]
*Table 1: Paradiagm comparison*

![[assets/figures/papers/iclr26_0003_8wQ7Oc08vo_A_New_Paradigm_for_Genome-wide_DNA_Methylation_P/figures/003_Table_2.jpg]]
*Table 2: The scale of DNAm data included in this study*

![[assets/figures/papers/iclr26_0003_8wQ7Oc08vo_A_New_Paradigm_for_Genome-wide_DNA_Methylation_P/figures/006_Table_3.jpg]]
*Table 3: The data statistics among all the data source and splits in our experiments. The number of tokens is estimated by the average sequence length (i.e., 200) of the input embeddings of the Transformer encoder*

## 方法谱系与知识库定位

MethylProphet 的核心贡献并非提出全新的模型架构，而是重新定义了 DNA 甲基化（DNAm）预测的输入范式。现有方法（如 DeepCpG、CpGPT、MethylGPT）遵循的是“插补”范式：它们需要目标样本中部分 CpG 位点的实验测量值作为上下文，来推断同一样本中未测量的 CpG 位点。这种范式受限于一个根本瓶颈——在典型数据集中，绝大多数 CpG 位点（约 97-99%）根本没有被测量过，因此无法作为输入。MethylProphet 通过将输入从“部分 DNAm 值”切换为“基因表达谱 + DNA 序列上下文”，绕过了这一瓶颈。其因果逻辑在于：全转录组表达谱（约 25000 个基因）编码了样本的全局生物学状态，而局部 1kb 序列上下文编码了 CpG 位点的顺式调控环境；两者结合，理论上足以推断位点特异性的甲基化水平，无需任何实验测量的 DNAm 作为起点。

与基线模型相比，MethylProphet 在多个关键设计槽位上发生了系统性变化。相对于 Levy-Jurgenson et al. (2019b) 的 CNN 注意力模型，MethylProphet 将基因表达编码从仅使用少量基因扩展到全转录组瓶颈 MLP，将 CpG 上下文表示从固定编码升级为 BPE 分词器，并引入了 CpG 岛上下文和染色体嵌入等基因组注释。这些变化在 ENCODE 和 TCGA 数据集上带来了显著的性能提升：在 ENCODE 的 Train CpG - Val Sample 分割中，MethylProphet 的 MAS-PCC 为 0.3436（基线 0.2878），MAC-PCC 为 0.9398（基线 0.8355），MSE 降至 0.0079（基线 0.0182）；在 TCGA 数据上差距更大，MAS-PCC 为 0.5455（基线 0.2630），MAC-PCC 为 0.9320（基线 0.6325）。在与 DeepCpG、CpGPT、MethylGPT 的直接比较中（Val CpG - Train Sample 分割，即分布内推理），MethylProphet 在 ENCODE 和 TCGA 上均取得了最高的 MAS-PCC 和 MAC-PCC。

然而，MethylProphet 的适用边界必须明确。其最关键的依赖条件是**必须有匹配的基因表达数据**——对于没有转录组测序的样本，该方法完全无法应用。这一限制意味着它不能替代 WGBS 或阵列平台作为独立的甲基化检测手段，而是作为一种计算增强工具，将已有的 RNA-seq 数据转化为甲基化图谱。其次，模型的泛化能力存在显著的不对称性：在“已见 CpG - 未见样本”分割中性能良好（TCGA 上 MAS-PCC 0.5455），但在“未见 CpG - 未见样本”分割中性能大幅下降（TCGA 上 MAS-PCC 约 0.39）。这表明模型对 CpG 位点的编码能力（即从序列上下文推断甲基化的能力）弱于对样本状态的编码能力——当面对训练中从未出现过的 CpG 位点时，模型只能依赖序列特征和基因组注释，而这些信息的预测信号可能不够强。

MethylProphet 的另一个关键优势在于对输入数据缺失的鲁棒性。消融实验表明，当上下文 CpG 数据从 100% 逐渐减少到 0% 时，MethylProphet 的 MAC-PCC 稳定维持在 0.88 左右，而 CpGPT 和 MethylGPT 的性能随可用 CpG 减少而急剧下降。这是因为 MethylProphet 根本不依赖上下文 CpG 作为输入——这既是它的核心创新，也暴露了它的根本局限：它无法利用已有的部分 DNAm 测量信息来提升预测精度。在实际应用中，如果目标样本已经有了一些阵列或测序数据，MethylProphet 无法像插补方法那样将这些信息纳入模型。

开放问题主要集中在三个方面。第一，模型的序列上下文窗口（当前为 1kb）对性能的影响尚未被系统探索——更长的窗口可能捕获更远的调控元件，但也会增加计算复杂度。第二，MethylProphet 在单细胞数据上的表现未知，单细胞转录组的稀疏性和噪声可能使瓶颈 MLP 的压缩策略失效。第三，该方法能否扩展到其他表观遗传标记（如组蛋白修饰、染色质可及性）是一个自然延伸方向，但需要验证这些标记与基因表达之间的相关性是否足够强以支持类似的跨模态预测。此外，作者明确指出本文应被视为概念验证研究，未系统探索更高效或更专业的架构设计，这意味着架构层面的改进空间仍然很大。

## 原文 PDF

PDF 文件：paperPDFs/ICLR_2026/A_New_Paradigm_for_Genome_wide_DNA_Methylation_Prediction_Without_Methylation_Input.pdf

![[paperPDFs/ICLR_2026/A_New_Paradigm_for_Genome_wide_DNA_Methylation_Prediction_Without_Methylation_Input.pdf]]
