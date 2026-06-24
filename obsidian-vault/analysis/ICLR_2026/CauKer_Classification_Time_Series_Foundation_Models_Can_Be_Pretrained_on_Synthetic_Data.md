---
title: "CauKer: Classification Time Series Foundation Models Can Be Pretrained on Synthetic Data"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/CauKer_Classification_Time_Series_Foundation_Models_Can_Be_Pretrained_on_Synthetic_Data.pdf
openreview_forum_id: xBW2FIfswU
aliases:
- CauKer
tags:
- ICLR_2026
- topic/benchmarks_datasets_evaluation
- topic/benchmarks_datasets_evaluation/benchmark_eval
core_operator: "将高斯过程（GP）核组合与结构因果模型（SCM）相结合，保留非零均值作为判别线索，并通过SCM传播注入因果语义，使合成数据同时具备时序多样性与类别聚类结构。"
primary_logic: "通过统一核合成的高斯过程与结构因果模型，CAUKER生成的合成数据在时序模式（季节性、趋势）和判别性聚类方面均优于现有方法，使得分类TSFM在纯合成数据上预训练即可获得与大规模真实数据集相当的零样本性能，并展现出清晰的缩放律。"
claims:
- "CAUKER在UCR基准上的零样本准确率显著优于其他合成数据生成方法（SCM、FPFN、KernelSynth、Mean+KernelSynth）。"
- "CAUKER生成的合成数据集展现出清晰的数据集大小和模型大小的缩放律，而真实世界UEA数据则表现出不规则的缩放行为。"
- "Mantis在10万CAUKER样本上预训练即可接近其在189万真实序列上预训练的性能（78.55% vs 78.66%）。"
- "CAUKER生成的合成数据在嵌入空间中覆盖了UCR和UEA的分布，表明其多样性。"
---

# CauKer: Classification Time Series Foundation Models Can Be Pretrained on Synthetic Data

> [!tip] 核心洞察
> 通过统一核合成的高斯过程与结构因果模型，CAUKER生成的合成数据在时序模式（季节性、趋势）和判别性聚类方面均优于现有方法，使得分类TSFM在纯合成数据上预训练即可获得与大规模真实数据集相当的零样本性能，并展现出清晰的缩放律。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | CauKer：分类时间序列基础模型可通过合成数据进行预训练 |
| 英文题名 | CauKer: Classification Time Series Foundation Models Can Be Pretrained on Synthetic Data |
| 会议/期刊 | ICLR 2026 (Oral) |
| Links | [paper](https://openreview.net/forum?id=xBW2FIfswU); [GitHub](https://github.com/ShifengXIE/CauKer) |
| Topic | #topic/benchmarks_datasets_evaluation #topic/benchmarks_datasets_evaluation/benchmark_eval |
| Method | CAUKER |
| Dataset | UCR (128 datasets), WOODS (17 datasets) |

> [!tip] 效果简介
> - UCR (128 datasets) 上，平均零样本准确率 为 CAUKER (Mantis: 78.31%, MOMENT: 74.24%)，对比 Mean+KernelSynth (Mantis: 78.20%, MOMENT: 72.56%)，变化 +0.11% (Mantis), +1.68% (MOMENT)。
> - UCR (128 datasets) 上，平均零样本准确率 为 Mantis pretrained on 100K CAUKER (78.55%)，对比 Original Mantis pretrained on 1.89M real series (78.66%)，变化 -0.11%。
> - UCR (128 datasets) 上，平均零样本准确率 为 MOMENT pretrained on 10M CAUKER (77.49%)，对比 Original MOMENT pretrained on 13M real series (78.85%)，变化 -1.36%。

## 概述

### 问题瓶颈

时间序列基础模型（TSFM）的预训练依赖大规模真实世界数据，但高质量标注时序数据的获取成本高昂，且现有合成数据生成方法存在根本性缺陷：纯高斯过程（GP）核组合方法（如**KernelSynth**，Ansari et al., arXiv 2024）能捕捉季节性、趋势等时序模式，却缺乏类别判别所需的聚类结构；结构因果模型（SCM）方法（如**TabPFN生成器**，Hollmann et al., ICLR 2023）能产生判别性聚类，却无法建模时序依赖。这一鸿沟导致分类TSFM的合成预训练数据既缺少多样性，又缺乏因果一致性，无法支撑良好的缩放律。

### 核心方法

**CAUKER**（Causal-Kernel Generation）通过统一GP核组合与结构因果模型来弥合上述鸿沟。其核心操控变量在于：**保留GP的均值函数作为判别线索**（而非传统预测任务中的零均值设定），并通过**有向无环图（DAG）传播注入因果语义**。具体而言，CAUKER从核库中随机采样并组合核函数构建GP先验，生成根节点时间序列；随后在随机生成的因果图上，通过激活函数库中的非线性变换传播信号，形成具有因果依赖关系的合成数据集。这一设计使合成数据同时具备时序多样性（季节性、趋势）与类别聚类结构。

### 核心结论

1. **零样本性能媲美真实数据预训练**：Mantis在仅10万CAUKER合成样本上预训练，即可在UCR基准（128数据集）上达到78.55%的平均零样本准确率，与在189万真实序列上预训练的原始Mantis（78.66%）几乎持平（Table 7）。

2. **清晰的缩放律**：CAUKER合成数据在数据集规模（10K至10M样本）和模型容量（1M至783M参数）两个维度均展现出稳定的单调缩放趋势，而UEA真实数据预训练则呈现不规则行为（Figure 3）。

3. **优于现有合成方法**：在UCR零样本评估中，CAUKER显著优于SCM、FPFN、KernelSynth等基线方法，Mantis和MOMENT分别达到78.31%和74.24%（Table 1）。

4. **生成效率高**：SCM层的结构构建与传播开销不足总生成时间的1%（Table 2），主要计算瓶颈集中在GP核采样。

### 方法定位

CAUKER面向**分类导向的合成TSFM预训练**，在方法谱系中处于GP核合成与因果生成模型的交叉点。与面向预测的零均值核合成方法（KernelSynth）不同，CAUKER保留均值函数作为判别线索；与面向表格分类的SCM方法（TabPFN生成器）不同，CAUKER通过GP注入时序结构。下游验证覆盖Mantis（对比预训练编码器，Feofanov et al., ICLR 2025）和MOMENT（掩码预训练编解码器，Goswami et al., ICML 2024）两种代表性TSFM架构。

## 背景与动机

时间序列分类是医疗诊断、工业监测、行为识别等领域的核心任务。近年来，时间序列基础模型（TSFM）通过在大量无标签时间序列上进行自监督预训练，展现出强大的零样本迁移能力。然而，这类模型的预训练高度依赖大规模真实世界数据集，而真实数据的获取面临隐私限制、标注成本高昂、领域覆盖不均等瓶颈。合成数据因此成为替代方案，但其有效性取决于一个关键前提：合成数据能否同时捕捉时间序列中的**时序模式**（如季节性、趋势）和**判别性聚类结构**。

现有合成数据生成方法在这一前提上存在结构性缺口。**KernelSynth**（Ansari et al., arXiv 2024）采用零均值高斯过程（GP）核组合生成序列，能够建模丰富的周期性与平滑模式，但其零均值设定使其天然面向预测任务，丢弃了对分类至关重要的均值水平判别线索。**Mean+KernelSynth**虽然补充了非零均值函数，但缺乏因果语义，生成的类别间差异仅由均值函数随机采样决定，未形成系统性的类间结构。**SCM（TabPFN生成器）**（Hollmann et al., ICLR 2023）通过结构因果模型注入因果依赖，但其设计面向表格分类，完全不具备时序结构。**FPFN**（Taga et al., arXiv 2025）通过线性共区域化模型生成多元序列，但其线性假设限制了非线性交互的表达能力。

上述方法的共同瓶颈在于：**时序多样性与判别性聚类结构无法在同一生成框架内得到统一**。纯核方法缺乏因果语义和类别结构，纯SCM方法缺乏时序模式，而简单的均值叠加无法弥补两者的系统性鸿沟。这一瓶颈直接导致合成数据预训练无法呈现清晰的缩放律——模型性能不随数据量或模型规模的增长而稳定提升，从而限制了合成数据在TSFM预训练中的实际价值。

本文的核心动机正是打破这一瓶颈：**能否设计一种生成框架，将GP的时序多样性与SCM的因果语义统一起来，使得合成数据既能覆盖丰富的时序模式，又能形成可判别的类别聚类，从而支撑分类TSFM的高效预训练？** 这一问题的解决将使得在纯合成数据上预训练的TSFM能够接近甚至匹配大规模真实数据预训练的性能，同时展现出可预测的缩放行为。

## 核心创新

CAUKER的核心创新在于首次将**高斯过程（GP）核组合**与**结构因果模型（SCM）**统一为一个合成数据生成框架，从而同时解决了现有合成数据生成方法的两大缺陷：无法捕捉时序模式（季节性、趋势）与无法构建判别性聚类结构。这一统一设计使分类时间序列基础模型（TSFM）在纯合成数据上预训练即可获得与大规模真实数据集相当的零样本性能，并展现出清晰的缩放律。

### 关键设计变更

CAUKER相对于现有合成数据生成方法，在三个核心环节上做出了根本性改变：

**1. GP均值函数：从零均值到保留判别线索**

KernelSynth（Ansari et al., arXiv 2024）作为面向预测的GP合成数据生成器，采用零均值GP以支持平滑外推。CAUKER则明确**保留非零均值函数作为分类任务的判别线索**——均值水平本身携带类别区分信息。这一选择在Table 1的消融中得到实证验证：Mean+KernelSynth（保留均值）在Mantis上的UCR零样本准确率（78.20%）显著高于KernelSynth（零均值，76.98%）。

**2. 因果结构：从纯核组合到SCM注入因果语义**

KernelSynth仅通过核组合生成时序数据，各序列之间缺乏有向依赖关系。CAUKER在GP根节点生成之后，通过**随机有向无环图（DAG）**传播信号，并在每条边上应用从激活函数库中采样的非线性变换。这一SCM层将核组合继承的周期性结构与因果语义统一起来：根节点GP携带时序模式（季节性、趋势），而DAG传播通过有向边注入变量间的因果依赖和非线性交互。Table 1显示，在Mean+KernelSynth基础上加入SCM结构（即CAUKER）进一步将Mantis准确率从78.20%提升至78.31%，MOMENT从72.56%提升至74.24%。

**3. 生成目标：从面向预测/表格分类到面向时序分类**

SCM生成器（Hollmann et al., ICLR 2023）面向表格分类设计，缺乏时序结构；KernelSynth面向预测设计，强调零均值和平滑外推。CAUKER的生成目标明确转向**时序分类**：通过GP核组合提供时序多样性（周期性、趋势、噪声），通过SCM传播提供类别聚类结构，使合成数据同时具备时序真实性和判别一致性。Figure 2展示了CAUKER生成的200条序列在嵌入空间中展现出清晰的聚类结构，Figure 4进一步表明CAUKER合成数据的嵌入分布覆盖了UCR和UEA真实数据的分布范围。

### 方法优势的因果机制

CAUKER的优势源于一个关键的因果机制：**GP核组合负责时序多样性，SCM负责判别性聚类，两者通过“根节点GP→因果图传播”的流水线实现解耦但协同**。具体而言，GP核组合（Step 1-3）从核库中随机采样并组合核函数，生成具有丰富时序模式的根节点序列；SCM传播（Step 4-5）将这些根节点序列作为因果图的输入，通过随机线性层和非线性激活函数在有向边上传播，使不同节点输出形成有意义的类别区分。这种解耦设计使得CAUKER对生成超参数（核数/父节点数、图尺寸）不敏感——Table 4和Table 5显示UCR准确率波动极小——同时SCM层的计算开销极低（Table 2显示不足总生成时间的1%），生成瓶颈仍集中在GP核采样（占总时间97%以上）。

### 证据强度与待验证点

CAUKER的核心创新在UCR基准（128个数据集）上获得了强有力验证：Mantis在10万CAUKER合成样本上预训练即可达到78.55%的零样本准确率，几乎匹配其在189万真实序列上预训练的性能（78.66%）（Table 7）。然而，以下方面仍需进一步验证：当前设计主要针对单变量固定长度序列（L=512），扩展到多变量和变长场景的有效性尚待考察；SCM图结构采用随机生成，是否可通过自动化优化进一步提升性能仍是开放问题。

## 整体框架

![[assets/figures/papers/paper_list_l24_https_openreview_net_forum_id_xBW2FIfswU/figures/001_Figure_1.jpg]]
*Figure 1: An illustration of the proposed CAUKER pipeline. Kernels sampled from the kernel bank K are randomly combined and used together with sampled mean functions to form GP priors. Time series sampled from these GP priors act as root nodes in a directed acyclic graph that encodes causal dependencies between nodes. Each edge of this graph applies an activation function from a predefined activation function bank and aggregates over incoming edges using a random linear transformation to propagate transformed time series through the graph. Intermediate node outputs are optionally interpolated to fixed length, forming the final synthetic dataset. This procedure yields rich, diverse, and causally consi...*

![[assets/figures/papers/paper_list_l24_https_openreview_net_forum_id_xBW2FIfswU/figures/033_Figure_9.jpg]]
*Figure 9: Examples of four mean function types used in the synthetic data pipeline. Each function introduces distinct temporal structure, contributing to the diversity and realism of generated sequences*

CAUKER 的合成数据生成流水线由五个顺序模块构成，其核心设计思想是将高斯过程（GP）核组合与结构因果模型（SCM）统一起来，使生成的时间序列同时具备时序多样性（趋势、季节性、周期）和判别性聚类结构。

### 模块关系与数据流

整个流水线围绕三个预定义的函数库展开：

- **核函数库** $\mathcal{K} = \{\kappa_i(t, t')\}_{i=1}^{n_\kappa}$
- **均值函数库** $\mathcal{M} = \{\mu_i(t)\}_{i=1}^{n_{\mathcal{M}}}$
- **激活函数库** $\mathcal{A} = \{\sigma(t)_i\}_{i=1}^{n_{\mathcal{A}}}$

数据生成按以下五步顺序执行（参见 Figure 1）：

1. **核库采样**：从 $\mathcal{K}$ 中随机采样候选核函数。
2. **核组合**：通过随机二元操作（加法或乘法）将采样的核组合为复合核：
   $$\kappa^{\bar{*}} = \kappa_1(t, t') \star_1 \cdots \star_{K-1} \kappa_K(t, t')$$
3. **根节点生成**：采样均值函数 $\mu \in \mathcal{M}$，与复合核共同构成 GP 先验，从中采样时间序列作为 SCM 的根节点。**关键设计**：保留非零均值函数作为判别线索，而非像 KernelSynth 那样强制零均值。
4. **激活函数库采样**：从 $\mathcal{A}$ 中采样激活函数，用于后续因果传播中的非线性变换。
5. **因果图传播**：通过有向无环图（DAG）传播根节点信号，非根节点 $v_j$ 通过聚合入射边并应用激活函数计算输出：
   $$t_{v_j} = \phi(v_j)(W \times [e_{.j}] + b)$$
   其中 $W$ 和 $b$ 是随机初始化的线性层参数，$\phi(v_j)$ 为节点对应的激活函数。

### 设计意图与关键差异

CAUKER 与既有合成数据生成方法的本质区别在于三个维度的设计选择（参见 Table 1 的消融对比）：

| 设计维度 | KernelSynth | Mean+KernelSynth | CAUKER |
|---------|-------------|------------------|--------|
| GP 均值函数 | 零均值 | 非零均值 | 非零均值 |
| 因果结构 | 无 | 无 | SCM 传播 |
| 生成目标 | 预测导向 | 预测导向 | 分类导向 |

- **保留均值函数**：零均值 GP 生成的数据在全局水平上缺乏判别信息，移除均值函数会显著降低分类 TSFM 的零样本性能（Table 1 中 KernelSynth 低于 Mean+KernelSynth）。
- **注入因果语义**：纯核组合方法虽然能生成丰富的时序模式，但缺少类别间的结构化依赖关系。SCM 层通过有向边传播信号，使合成数据获得因果一致性，在 Mean+KernelSynth 基础上进一步提升准确率（Mantis: +0.11%, MOMENT: +1.68%）。
- **生成效率**：SCM 结构构建与传播的总开销不足生成总时间的 1%（Table 2），超过 97% 的时间消耗在 GP 核采样上，表明因果层的引入几乎不增加计算负担。

### 与现有 TSFM 预训练范式的定位

Table 3 对比了主流 TSFM 的预训练数据来源。现有模型主要依赖真实世界数据（如 Chronos、MOMENT、Mantis），少数方法（如 TabPFN）使用纯合成数据但面向表格分类，缺乏时序结构建模能力。CAUKER 填补了这一空白：它专为时间序列分类设计合成预训练语料，在纯合成数据上预训练的 TSFM 可获得与大规模真实数据预训练相当的零样本性能（Mantis 在 10 万 CAUKER 样本上预训练达到 78.55%，接近原始 189 万真实序列预训练的 78.66%）。

## 核心模块与公式推导

CAUKER 生成流水线由五个核心模块串联构成，其关键洞察在于将高斯过程（GP）核组合与结构因果模型（SCM）统一起来：GP 核组合赋予合成序列时序模式（季节性、趋势），SCM 通过有向边传播注入因果语义，而非零均值函数则保留为判别性线索。

### 函数库定义

流水线依赖三个预定义的函数库：

$$\mathcal{K} = \{ \kappa_i(t, t') \}_{i=1}^{n_{\kappa}}, \quad \mathcal{M} = \{ \mu_i(t) \}_{i=1}^{n_{\mathcal{M}}}, \quad \mathcal{A} = \{ \sigma(t)_i \}_{i=1}^{n_{\mathcal{A}}}$$

其中 $\mathcal{K}$ 为核函数库（如 RBF、周期核、线性核等），$\mathcal{M}$ 为均值函数库，$\mathcal{A}$ 为激活函数库。这三个库是后续所有随机采样操作的基础。

### 模块一：核库采样与组合

从 $\mathcal{K}$ 中随机采样 $K$ 个核函数，通过 $K-1$ 个随机二元操作符 $\star_i \in \{+, \times\}$ 构建复合核：

$$\kappa^{\bar{*}} = \kappa_1(t, t') \star_1 \cdots \star_{K-1} \kappa_K(t, t')$$

复合核决定了 GP 先验的协方差结构，从而控制生成序列的时序特性（平滑度、周期性等）。消融实验表明，仅使用 DotProduct 核会导致 UCR 准确率显著下降（76.79%），而仅使用 RBF 核仍具竞争力（78.07%），说明核库的多样性对生成质量至关重要。

### 模块二：根节点生成

从 $\mathcal{M}$ 中采样均值函数，与复合核组合形成 GP 先验 $\mathcal{GP}(\mu, \kappa^{\bar{*}})$。从该先验中采样得到的时间序列作为 SCM 的根节点。**关键设计选择**：保留非零均值函数作为判别线索，而非像 KernelSynth 那样强制零均值。Table 1 中 KernelSynth 与 Mean+KernelSynth 的对比直接验证了这一选择——添加均值函数后 Mantis 准确率从 77.60% 提升至 78.20%。

### 模块三：激活函数库采样

从 $\mathcal{A}$ 中随机采样激活函数，为因果图中的每个非根节点分配非线性变换函数。该模块为 SCM 传播提供非线性表达能力。

### 模块四：因果图传播

构建有向无环图（DAG），根节点为 GP 采样的序列，非根节点 $v_j$ 的值通过聚合入射边并应用激活函数计算：

$$t_{v_j} = \phi(v_j)(W \times [e_{.j}] + b)$$

其中 $[e_{.j}]$ 为所有入射边的拼接向量，$W$ 和 $b$ 为随机线性变换的权重与偏置，$\phi(v_j)$ 为该节点分配的激活函数。通过 DAG 的多层传播，根节点的时序模式被非线性变换和混合，生成具有因果依赖关系的多元输出。最终从图中提取各节点输出作为独立的单变量序列，构成合成数据集。

### 计算开销特征

Table 2 的运行时分解揭示了关键瓶颈：GP 核采样耗时 118.54 秒，占总生成时间（121.64 秒）的 97% 以上；而 SCM 结构构建与传播仅需 1.14 秒，占比不足 1%。这意味着 CAUKER 的因果注入几乎不增加计算成本，主要开销集中在 GP 先验的采样阶段。

## 实验与分析

### 核心结果：合成数据生成方法对比

CAUKER在UCR基准（128个数据集）的零样本分类评估中，对两种不同预训练范式的TSFM均取得最优平均准确率。**Table 1** 报告了五种合成数据生成方法在Mantis（对比预训练）和MOMENT（掩码预训练）上的表现：


![[assets/figures/papers/paper_list_l24_https_openreview_net_forum_id_xBW2FIfswU/figures/002_Table_1.jpg]]
*Table 1: Average zero-shot accuracy (%) on the UCR benchmark after pre-training on synthetic corpora generated by different methods*

- **Mantis**：CAUKER达到78.31%，略高于Mean+KernelSynth的78.20%，显著优于纯核方法KernelSynth（76.82%）和SCM方法（77.16%）。
- **MOMENT**：CAUKER达到74.24%，较Mean+KernelSynth（72.56%）提升1.68个百分点，较KernelSynth（68.39%）提升5.85个百分点。

这一结果直接验证了核心因果机制：**非零均值函数与SCM因果结构各自贡献独立且可叠加的增益**。移除均值函数（KernelSynth）导致MOMENT准确率骤降近6个百分点；在保留均值的基础上加入SCM（即CAUKER vs Mean+KernelSynth）进一步带来1.68个百分点的提升。

> **公平性说明**：原始Mantis和MOMENT的预训练语料包含UCR训练集（不含测试集），使其在UCR零样本评估中享有分布内优势；CAUKER预训练模型完全未接触任何UCR数据，执行严格OOD评估。

### 生成效率分析

**Table 2** 揭示了CAUKER的生成成本结构。生成1万条长度为512的序列总耗时121.64秒，显著快于KernelSynth的182.25秒。内部耗时分解显示：


![[assets/figures/papers/paper_list_l24_https_openreview_net_forum_id_xBW2FIfswU/figures/003_Table_2.jpg]]
*Table 2: Overall wall-clock generation time and internal runtime breakdown for CAUKER*

- GP核采样占据118.54秒（约97.5%），是绝对计算瓶颈。
- SCM结构构建与因果图传播合计仅1.14秒（不足1%）。

这意味着CAUKER在引入因果语义的同时几乎不增加计算开销，其效率优势源于SCM层仅需对少量根节点执行昂贵的GP采样，其余节点通过轻量级线性变换和激活函数传播生成。

### 缩放律：合成数据 vs 真实数据

**Figure 3** 展示了MOMENT和Mantis在数据集大小和模型容量两个维度上的缩放行为，这是本文最具区分度的实验发现：


![[assets/figures/papers/paper_list_l24_https_openreview_net_forum_id_xBW2FIfswU/figures/008_Figure_3.jpg]]
*Figure 3: Scaling law of MOMENT and Mantis depending on the dataset size (left, middle left, respectively) model trained on different subsets of UEA and CauK datasets. Scaling law for the same models depending on the model size (middle right, right, respectively)*

- **数据缩放律**：在CAUKER合成数据上，两种模型的UCR准确率随数据量从10K增至10M呈现单调上升趋势；而在UEA真实数据子集上，缩放曲线不规则，甚至出现准确率倒退。
- **模型缩放律**：在CAUKER数据上预训练的模型，准确率随参数量增长严格递增（MOMENT从77M到783M，Mantis从0.75M到114.14M）；UEA预训练模型则未呈现一致趋势。

这一发现揭示了真实世界预训练语料的核心瓶颈：**UEA数据缺乏足够的多样性和因果一致性，无法支撑可预测的缩放行为**。CAUKER通过核组合覆盖广泛的时序模式（季节性、趋势、周期），并通过SCM注入判别性聚类结构，使合成数据具备支撑缩放律的必要条件。

### 样本效率：小规模合成数据匹配大规模真实预训练

**Table 7** 展示了CAUKER的样本效率优势：


![[assets/figures/papers/paper_list_l24_https_openreview_net_forum_id_xBW2FIfswU/figures/037_Table_7.jpg]]
*Table 7: Exact accuracy values used in the scaling law plots (Figure 3)*

- Mantis在**10万条**CAUKER合成样本上预训练（78.55%），几乎匹配其在**189万条**真实序列上预训练的原始性能（78.66%），差距仅0.11个百分点。
- MOMENT在**1000万条**CAUKER样本上预训练（77.49%），接近其在**1300万条**真实序列上的性能（78.85%），差距1.36个百分点。

这意味着CAUKER实现了约**19倍**（Mantis）和**1.3倍**（MOMENT）的数据压缩比。**Figure 6** 的训练动态进一步显示，CAUKER预训练模型的测试准确率随epoch平滑上升，而UEA预训练模型曲线平坦甚至波动，表明合成数据提供了更稳定的学习信号。

### 消融实验：各组件贡献

**核组合消融**（Section C.2）：仅使用DotProduct核的GP导致UCR准确率降至76.79%，而仅使用RBF核仍保持78.07%的竞争力，说明核多样性对时序模式覆盖至关重要。

**均值函数消融**：Table 1中KernelSynth（零均值）与Mean+KernelSynth（保留均值）的对比直接量化了均值函数的贡献——MOMENT上差距达4.17个百分点，Mantis上差距1.38个百分点。这证实了保留非零均值作为判别线索的必要性。

**SCM结构消融**：Mean+KernelSynth与CAUKER的对比（Table 1）量化了因果图传播的增益——Mantis上0.11个百分点，MOMENT上1.68个百分点。

**超参数鲁棒性**：**Table 4** 和 **Table 5** 显示，CAUKER对核数量/父节点数和DAG图尺寸不敏感，UCR准确率波动极小，表明方法无需精细调参即可稳定工作。


![[assets/figures/papers/paper_list_l24_https_openreview_net_forum_id_xBW2FIfswU/figures/034_Table_4.jpg]]
*Table 4: Kernel/Parents co-sweep. Increasing both the number of sampled kernels in the GP composition and the maximum number of parents per node produces steadily higher Entropy/Stability/Lumpiness and a decreasing Hurst, while UCR accuracy stays stable*

![[assets/figures/papers/paper_list_l24_https_openreview_net_forum_id_xBW2FIfswU/figures/035_Table_5.jpg]]
*Table 5: Graph size sweep. CAUKER is insensitive to DAG size*

### 跨领域泛化

**WOODS基准**（**Table 10**）：CAUKER-100K在17个数据集上取得0.820的领域平均准确率，超过Mantis-2M（真实数据预训练，0.810）和有监督基线ERM。CAUKER在11/17个数据集上获胜，但在MI EEG子任务上显著落后于ERM，提示某些EEG任务可能依赖标签丰富的专有训练。

**预测任务**（**Table 11**）：Chronos Base在100万条CAUKER样本上预训练后，chronos-zero-shot套件（27个子集）的MASE为0.83，与官方Chronos Base（0.81）统计上不可区分（p=0.84），证明合成数据同样适用于预测型TSFM。

**临床多元时间序列**（**Table 13**）：CAUKER预训练的Mantis在不规则多元临床基准上保持竞争力，表明方法虽针对单变量设计，但编码器学到的表示具有一定跨模态迁移能力。

### 嵌入空间分析

**Figure 4** 的PCA可视化显示，CAUKER生成的10万条序列在Mantis嵌入空间中覆盖了UCR和UEA的分布区域，且扩展至更广的范围。这从几何层面验证了合成数据的多样性——CAUKER不仅复现了真实数据的分布，还生成了真实数据未覆盖但合理的时序模式。


![[assets/figures/papers/paper_list_l24_https_openreview_net_forum_id_xBW2FIfswU/figures/009_Figure_4.jpg]]
*Figure 4: Mantis embeddings of 100K time series drawn from UCR, UEA and generated by CAUKER*

**Figure 5** 的非线性统计量与CKA相似性分析进一步表明，随着CAUKER数据量增加，预训练模型的非线性表达能力持续增强，层间表示相似性呈现规律性变化；而UEA预训练模型则未展现此类结构化演化。

### 失败模式与局限

1. **Spectro领域性能下降**：CAUKER预训练在Spectro类型数据集上出现-5.50%的大幅下降，可能源于该领域样本过少或GP核对频谱模式的覆盖不足。
2. **GP核采样瓶颈**：尽管SCM层开销极低，GP核采样仍占总时间97%以上，大规模生成时计算成本显著。
3. **固定长度限制**：当前生成仅支持L=512的固定长度序列，无法覆盖所有真实世界的变长模式。
4. **多变量扩展未验证**：主要实验集中在单变量场景，多变量TSFM预训练的适用性需进一步研究。

### 补充图表

![[assets/figures/papers/paper_list_l24_https_openreview_net_forum_id_xBW2FIfswU/figures/015_Table_3.jpg]]

![[assets/figures/papers/paper_list_l24_https_openreview_net_forum_id_xBW2FIfswU/figures/017_Table_3.jpg]]
*Table 3: Overview of pre-training datasets for Time Series Foundation Models (TSFMs)*

![[assets/figures/papers/paper_list_l24_https_openreview_net_forum_id_xBW2FIfswU/figures/036_Table_6.jpg]]
*Table 6: Global and local alignment between UCR and synthetic corpora. Lower is better for SWD; higher is better for CKNNA. Means ± s.d. across five independent synthetic draws, then averaged over UCR datasets*


## 方法谱系与知识库定位

### 合成数据生成方法的演进定位

CAUKER 处于时间序列合成数据生成与自监督预训练的交汇点，其核心贡献在于弥合了“纯核组合生成器”与“结构因果模型（SCM）生成器”之间的鸿沟。现有合成数据生成方法可沿两条轴线分类：

**核合成谱系**以 **KernelSynth**（Ansari et al., arXiv 2024）为代表，通过高斯过程核组合生成具有丰富时序模式（季节性、趋势、周期性）的时间序列。然而，KernelSynth 设计目标面向预测任务，采用零均值 GP 先验以鼓励平滑外推——这一设计选择使其生成的序列缺乏判别性聚类结构，无法直接用于分类 TSFM 的预训练。**Mean+KernelSynth** 在此基础上添加非零均值函数，部分恢复判别线索，但仍缺失因果语义注入。

**因果生成谱系**以 **SCM 生成器**（Hollmann et al., ICLR 2023）为代表，源自 TabPFN 的表格分类合成数据生成。该方法通过因果图传播注入判别性结构，但缺乏对时序模式（如周期性、趋势）的建模能力，生成的序列不具备真实时间序列的结构多样性。

**FPFN**（Taga et al., arXiv 2025）使用线性共区域化模型生成多元时间序列，但其线性假设限制了非线性时序模式的表达。

CAUKER 通过“核组合 GP 作为根节点生成器 + SCM 图传播作为因果语义注入”的统一框架，同时捕获时序多样性与判别性聚类结构。其关键设计决策——保留非零均值作为判别线索、通过有向边注入因果依赖——直接回应了上述两类方法的根本性不足。

### 在 TSFM 预训练生态中的定位

CAUKER 验证了两类主流 TSFM 架构在纯合成数据上的预训练可行性：

- **Mantis**（Feofanov et al., ICLR 2025）：对比预训练的编码器 TSFM，使用对比学习损失 $L_{\text{contrastive}} = \sum_{i=1}^b l_{ce}( s_i(\phi, \psi) / T, i )$。
- **MOMENT**（Goswami et al., ICML 2024）：掩码预训练的编码器-解码器 TSFM，使用掩码重建损失 $L_{\text{masked}} = \frac{1}{|\Omega|} \sum_{n \in \Omega} \| T_n - h_{rec}(F([\text{MASK}]))_n \|^2$。

CAUKER 的独特价值在于：Mantis 仅需 10 万 CAUKER 合成样本即可达到 78.55% 的 UCR 零样本准确率，与原始 Mantis 在 189 万真实序列（含 UCR 训练集）上预训练的 78.66% 几乎持平（Table 7）。MOMENT 在 1000 万 CAUKER 样本上达到 77.49%，接近其 1300 万真实序列预训练的 78.85%。这表明 CAUKER 合成数据在样本效率上具有显著优势——用约 1/20（Mantis）至 1/1.3（MOMENT）的数据量即可逼近真实数据预训练性能。

值得注意的是，原始 Mantis 和 MOMENT 的预训练语料包含 UCR 训练集（但不含测试集），使其在 UCR 零样本评估中具有分布内优势；而 CAUKER 预训练模型完全未接触任何 UCR 数据，执行的是严格 OOD 评估，因此其性能更具泛化意义。

### 适用边界

**已验证的适用场景**：
- 单变量时间序列分类（UCR 128 数据集，平均零样本准确率 78.31%）
- 零样本预测（chronos-zero-shot suite，27 个子集，MASE 0.83 与 Chronos Base 的 0.81 统计不可区分，p=0.84）
- 分布外泛化（WOODS 基准 17 个数据集，CAUKER-100K 平均准确率 0.820 超越 Mantis-2M 的 0.810）

**已知局限性**：
- **多变量扩展待验证**：当前工作聚焦单变量时间序列预训练，SCM 图传播虽可提取多个单变量节点，但多变量联合建模仍需进一步研究。
- **固定序列长度**：合成数据生成目前仅支持 $L=512$ 的固定长度，可能无法覆盖所有真实世界的复杂模式长度。
- **SCM 图结构未优化**：因果图采用随机生成策略，尚未探索自动化优化图结构以进一步提升性能。
- **任务覆盖有限**：主要验证集中在分类和预测任务，在异常检测、插补等其他时间序列任务上的适用性尚待考察。
- **领域特异性退化**：在 Spectro 领域 CAUKER 预训练出现大幅性能下降（-5.50%），原因尚不明确——可能是该领域样本过少或领域特性与合成数据分布不匹配。

### 开放问题

1. **UEA 缩放律失效的根因**：为何 UEA 真实数据预训练无法呈现单调增长的缩放律？是否存在领域不匹配或数据多样性不足的问题？这暗示真实数据集可能存在冗余、噪声或分布偏差，而合成数据的可控性恰好规避了这些问题。

2. **GP 核组合与领域模式的匹配机制**：GP 核组合如何有效捕捉 Power 领域的周期性模式（该领域获得最大增益）？理解这一机制可为领域自适应的核库设计提供指导。

3. **EEG 任务的预训练瓶颈**：在 WOODS 的 MI EEG 子任务中，有监督基线 ERM 显著优于预训练方法，这是否表明某些 EEG 任务需要标签丰富的专有训练，而非通用时序表示学习？

4. **合成数据的预测能力上限**：CAUKER 合成数据能否通过进一步扩大规模来匹配甚至超越 Chronos 所用的 84B 观测数据，从而实现强大预测模型的纯合成预训练？当前 100 万样本的初步实验已显示竞争力，但规模上限尚未探明。

5. **计算瓶颈的缓解**：GP 核采样占据总生成时间 97% 以上（118.54s / 121.64s），虽然 SCM 层开销不足 1%，但整体生成大规模数据集时计算成本仍较高。核采样的近似加速或缓存复用策略值得探索。

## 原文 PDF

![[paperPDFs/ICLR_2026/CauKer_Classification_Time_Series_Foundation_Models_Can_Be_Pretrained_on_Synthetic_Data.pdf]]
