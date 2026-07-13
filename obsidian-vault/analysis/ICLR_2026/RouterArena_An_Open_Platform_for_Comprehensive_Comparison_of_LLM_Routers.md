---
title: "RouterArena: An Open Platform for Comprehensive Comparison of LLM Routers"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/RouterArena_An_Open_Platform_for_Comprehensive_Comparison_of_LLM_Routers.pdf
project_link: https://routeworks.github.io/
code_link: null
aliases:
- RouterArena
tags:
- ICLR_2026
- topic/generative_models_diffusion
- topic/generative_models_diffusion/algorithms
core_operator: "构建多领域多难度查询集和五维指标来统一评估LLM路由器。"
primary_logic: "RouterArena按DDC、Bloom和模型经验难度构建查询，再评估准确率、成本、最优性、鲁棒性和延迟并生成排行榜。"
claims:
- "RouterArena覆盖9大领域44个类别和三个经验难度等级，弥补现有路由评估类别少且无难度分层的问题。"
- "Arena Score用加权调和平均在准确率和归一化成本之间提供可调权衡。"
- "GPT-5等商业路由器准确率更高但成本显著更高，MIRT-BERT等开源路由器成本效益更好。"
- "没有路由器在准确性、成本、最优性、鲁棒性和延迟所有维度上同时最优。"
---

# RouterArena: An Open Platform for Comprehensive Comparison of LLM Routers

> [!tip] 核心洞察
> 通过系统化的数据集构建（覆盖9大领域44个类别，3个经验验证的难度等级）和多维度指标（5个评估视角），ROUTERARENA揭示了商业路由器（如GPT-5）虽准确率高但成本显著更高，而开源路由器（如MIRT-BERT）在成本效益上更具优势，且没有任何路由器在所有指标上均表现最优，反映了路由器设计中固有的权衡。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | RouterArena：用于全面比较 LLM 路由器的开放平台 |
| 英文题名 | RouterArena: An Open Platform for Comprehensive Comparison of LLM Routers |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=9HsaIi4ngF) · [Project](https://routeworks.github.io/) |
| Topic | #topic/generative_models_diffusion #topic/generative_models_diffusion/algorithms |
| Method | ROUTERARENA |
| Dataset | ROUTERARENA数据集（整体）, ROUTERARENA数据集（困难查询） |

> [!tip] 效果简介
> - ROUTERARENA数据集（整体） 上，准确率（%） 为 74.0，对比 66.9，变化 +7.1。
> - ROUTERARENA数据集（整体） 上，成本（美元/千查询） 为 14.02，对比 0.15，变化 +13.87。
> - ROUTERARENA数据集（困难查询） 上，准确率（%） 为 27.5，对比 7.1，变化 +20.4。

## 概要

ROUTERARENA 是一个开放的标准化平台，旨在系统性地比较和评估大语言模型（LLM）路由器的性能。该平台通过构建基于杜威十进制分类法（DDC）和Bloom认知分类法的原则性数据集（约8,400个查询，覆盖9大领域44个类别），并设计包含准确性、成本、最优性、鲁棒性和延迟的多维度评估指标，解决了现有LLM路由器评估碎片化、缺乏统一标准化评估平台的问题。实验揭示了商业路由器（如GPT-5）虽准确率高但成本显著更高，而开源路由器（如MIRT-BERT）在成本效益上更具优势，且没有任何路由器在所有指标上均表现最优，反映了路由器设计中固有的权衡。



随着大语言模型（LLM）的快速发展，市场上涌现出大量不同能力、成本和延迟特性的模型。LLM路由器作为一种智能选择模型的技术，旨在根据查询特性动态选择最合适的模型，以在性能和成本之间取得平衡。然而，现有路由器评估工作（如RouterBench、RouterEval、FusionBench、EmbedLLM）存在以下问题：

- **评估数据集有限**：仅使用24-27个类别且无难度区分的数据集。
- **评估指标不全面**：仅考虑部分指标（如仅准确率或仅延迟曲线）。
- **商业路由器支持缺失**：现有框架仅评估开源路由器。
- **缺乏统一排行榜**：无统一的、多指标的路由器排名机制。

如Table 1所示，ROUTERARENA在查询类别数量（44个）、难度级别（3个）、评估指标维度（5个）、商业路由器支持（3个）和路由器排名机制（多指标排行榜）方面均显著优于现有工作。

Figure 2展示了从2023年中至2025年路由器相关工作和产品的发展时间线，包括FrugalGPT（Chen et al., 2023）、RouterBench（Hu et al., 2024）、RouteLLM（Ong et al., 2025）、GraphRouter（Feng et al., 2025a）以及商业产品如NotDiamond、Azure-Router和GPT-5。



## 核心方法与创新机理

ROUTERARENA的核心创新在于：

1. **原则性数据集构建**：基于DDC（杜威十进制分类法）覆盖除宗教外的所有领域，结合Bloom认知分类法确保查询覆盖多样化的认知技能，并通过经验性难度标注（基于42个代表性模型的准确率）将查询分为三个难度等级（困难：≤4/42，中等：5-19/42，简单：≥20/42）。

2. **多维度评估指标**：引入5个评估维度——查询-答案准确性、查询-答案成本、路由最优性（3个子指标：最优选择比率、最优准确率比率、最优成本比率）、路由鲁棒性、路由延迟。

3. **自动化评估框架**：同时支持开源和商业路由器，使用前缀缓存提高效率，自动计算指标并更新排行榜。

4. **加权调和平均排名机制**：提供基于Arena Score（加权调和平均）的6种排名分数，支持用户调整β参数以权衡准确性与成本。



![[assets/figures/papers/iclr26_0001_9HsaIi4ngF_RouterArena_An_Open_Platform_for_Comprehensive_C/figures/001_Figure_1.jpg]]
*Figure 1: RouterArena Leaderboard*

ROUTERARENA的整体框架如Figure 5所示，包含以下核心模块：

1. **数据集构建模块**：从23个源数据集收集查询，基于DDC和Bloom分类法进行类别标注，通过余弦相似度去重，并使用递归赤字再分配算法平衡各类别和认知水平的查询数量。

2. **评估指标计算模块**：计算5个维度的指标，包括准确性（平均正确率）、成本（实际推理成本）、最优性（3个子指标）、鲁棒性（扰动下路由决策一致性）和延迟（TTFT和端到端响应延迟增加）。

3. **自动化评估框架**：向路由器发送查询，收集模型选择，运行推理（使用前缀缓存），计算指标并更新排行榜。

4. **排行榜生成模块**：基于Arena Score等6种分数生成多维度排行榜。



### 5.1 推理成本公式

实际推理成本由输入和输出的token数量及对应价格决定：

$$ cost = c_{in} * N_{in} + c_{out} * N_{out} $$

其中 $c_{in}$ 和 $c_{out}$ 分别是输入和输出的每token成本，$N_{in}$ 和 $N_{out}$ 分别是输入和输出的token数量。

### 5.2 归一化成本

为了将不同路由器的成本映射到[0,1]区间，使用以2为底的对数变换：

$$ C_i = (log_2(c_{max}) - log_2(c_i)) / (log_2(c_{max}) - log_2(c_{min})) $$

其中 $c_{max}$ 和 $c_{min}$ 分别是市场上最昂贵和最便宜模型的价格，$c_i$ 是路由器i的实际成本。值越大表示越经济。

### 5.3 Arena Score

Arena Score通过加权调和平均结合归一化成本 $C_i$ 和准确率 $A_i$：

$$ S_{i,\beta} = ((1+\beta) A_i C_i) / (\beta A_i + C_i) $$

参数 $\beta$ 控制准确率与成本的相对重要性。当 $\beta=0.01$ 时，准确率与成本权重比为100:1（准确率主导）；当 $\beta=0.1$ 时，权重比为10:1（权衡）；当 $\beta=1$ 时，权重比为1:1（等权重）。

### 5.4 路由最优性指标

路由最优性包含三个子指标：
- **最优选择比率**：路由器通过选择最便宜模型正确回答的查询比例。
- **最优准确率比率**：路由器实际准确率与始终选择最佳模型可获得的上限准确率之比。
- **最优成本比率**：路由器选择产生的成本与始终选择最优模型的成本之比。

### 5.5 路由鲁棒性

鲁棒性计算为路由器在扰动输入下做出一致路由决策的查询比例。使用四种变换模式：Paraphrase（最大变换）、Grammatical Reconstruction（深度重写）、Synonym Saturation（超密集替换）和Intentional Corruption（重度退化）。



## 实验与关键发现

### 6.1 实验设置

ROUTERARENA评估了14个路由器，包括3个商业路由器（GPT-5、NotDiamond、Azure-Router）和11个开源路由器（KNN、MLP、GraphRouter、Universal Router、CARROT、RouterDC、IRT-Router、RouteLLM、vLLM-SR、MIRT-BERT、NIRT-BERT）。模型池配置见Table 3。

![[assets/figures/papers/iclr26_0001_9HsaIi4ngF_RouterArena_An_Open_Platform_for_Comprehensive_C/figures/014_Table_3.jpg]]
*Table 3: Model pools used by different routers.*

### 6.2 主要结果

**Table 6** 展示了路由器按难度级别划分的性能：

| 路由器 | 整体准确率(%) | 整体成本($/千查询) | 困难准确率(%) | 困难成本($/千查询) |
|--------|--------------|-------------------|---------------|-------------------|
| GPT-5 | 74.0 | 14.02 | 27.5 | 35.73 |
| MIRT-BERT | 66.9 | 0.15 | 7.1 | 0.26 |

关键发现：
- GPT-5在准确性上最高（74.0%），但成本也最高（每千查询$14.02）。
- MIRT-BERT以$0.15的成本达到66.9%的准确率，成本效益显著。
- 在困难查询上，GPT-5准确率27.5%，成本$35.73；MIRT-BERT准确率7.1%，成本$0.26。
- 大多数路由器在简单问题上准确率超过89%，但在困难问题上准确率急剧下降（通常低于10%）。

**Figure 6** 的延迟曲线显示，商业路由器（GPT-5、NotDiamond）可以达到更高准确率，但成本显著更高；开源路由器（CARROT、GraphRouter）在更低预算下实现竞争性能，但更早达到平台期。

**Figure 7** 的归一化散点图显示，vLLM-SR和CARROT在成本降低约35%的情况下，准确率下降不到2%。

**Figure 8** 显示：
- RouterDC具有最低的成本比率和最高的最优选择比率，但总体准确率较差。
- MIRT-BERT实现了接近77%的最优准确率，但成本约为最优成本的5倍。

**Figure 9** 显示：
- 鲁棒性普遍较低，包括商业和学术路由器（vLLM-SR、MIRT-BERT、NIRT-BERT），主要原因是这些学术路由器依赖BERT计算潜在表示，而BERT对表面扰动敏感。
- vLLM-SR和RouteLLM延迟显著更高，因为它们依赖OpenAI embedding API引入网络延迟。

**Table 8** 显示GPT-5和Azure-Router更依赖推理模型，导致生成长度显著长于其他路由器。

### 6.3 长上下文路由

**Table 7** 显示在LongBench-v2上：
- GPT-5达到最高准确率71%，成本$45.70/千查询。
- Azure-Router达到67%准确率，成本$9.54/千查询。
- RouteLLM无法评估，因为其文本编码器仅支持最多8,192个token的输入。

### 6.4 综合排行榜

**Table 2** 展示了路由器在多个指标上的排名：
- Azure-Router综合排名第一（平均排名4.40）。
- NotDiamond排名第12（平均排名8.80），因为它频繁选择昂贵模型。
- GPT-5排名第7，因其模型池受限。

![[assets/figures/papers/iclr26_0001_9HsaIi4ngF_RouterArena_An_Open_Platform_for_Comprehensive_C/figures/013_Table_2.jpg]]
*Table 2: Ranking of routers across multiple metrics. Lower values indicate better performance.*

**Figure 12** 的蜘蛛图比较了六种路由方法在五个评估维度上的表现，显示CARROT在Arena Score和延迟方面表现强劲，RouterDC在成本比率方面表现优异。

### 6.5 Arena Score排名

**Figure 13** 展示了不同β值下的路由器排名：
- 当β=0.01（准确率主导）时，GPT-5排名第一（Score=0.7282）。
- 当β=0.1（权衡）时，MIRT-BERT排名第一（Score=0.6729），GPT-5排名第五（Score=0.6272）。
- 当β=1（等权重）时，MIRT-BERT排名第一（Score=0.6718），GPT-5排名第12（Score=0.3688）。

### 6.6 关键洞察

1. **商业路由器并非总是最优**：在准确性-成本综合排名中，MIRT-BERT排名第一，GPT-5排名第五。
2. **所有现有路由器均未达到Oracle性能**：主要原因是它们在识别何时小型廉价模型足以处理给定查询时效率低下。
3. **路由器设计中存在固有权衡**：没有任何路由器在所有指标上均表现最优。
4. **鲁棒性是普遍弱点**：包括商业和学术路由器，鲁棒性普遍较低。

### 补充图表

![[assets/figures/papers/iclr26_0001_9HsaIi4ngF_RouterArena_An_Open_Platform_for_Comprehensive_C/figures/004_Table_1.jpg]]
*Table 1: Comparison of existing work (Hu et al., 2024; Huang et al., 2025; Feng et al., 2025b; Zhuang et al., 2024) and ROUTERARENA. ROUTERARENA enables comprehensive router comparison with extensive query categories, difficulty levels, evaluation metrics, and router inclusion.*

![[assets/figures/papers/iclr26_0001_9HsaIi4ngF_RouterArena_An_Open_Platform_for_Comprehensive_C/figures/016_Table_4.jpg]]
*Table 4: Overview of dataset columns*

![[assets/figures/papers/iclr26_0001_9HsaIi4ngF_RouterArena_An_Open_Platform_for_Comprehensive_C/figures/017_Table_5.jpg]]
*Table 5: The 42 models used for empirical difficulty labeling. Models span across a range of sizes and performances, showcasing that ROUTERARENA could distinguish LLMs by providing diverse questions of difficulty.*



## 定位与知识库关联

ROUTERARENA定位为LLM路由器评估领域的标准化基准平台，其方法谱系包括：

**评估基准类**：
- RouterBench（Hu et al., 2024）：使用24个类别，无难度区分。
- RouterEval（Huang et al., 2025）：使用27个类别，无难度区分。
- FusionBench（Feng et al., 2025b）：关注模型融合。
- EmbedLLM（Zhuang et al., 2024）：关注嵌入模型路由。

**路由器方法类**：
- 基于相似度：KNN（Router-Bench）、vLLM-SR（语义路由）
- 基于学习：MLP（Router-Bench）、GraphRouter（图神经网络）、RouterDC（双对比学习）
- 基于聚类：Universal Router（K-means）
- 基于成本-准确率权衡：CARROT
- 基于项目反应理论：IRT-Router、MIRT-BERT、NIRT-BERT
- 基于偏好学习：RouteLLM
- 商业路由：GPT-5、NotDiamond、Azure-Router

**知识库定位**：
ROUTERARENA填补了LLM路由器评估领域的空白，提供了一个可扩展、可复现的标准化评估平台。其数据集构建方法（基于DDC和Bloom分类法）和多维度评估指标（5个评估视角）为未来路由器研究提供了基准。平台支持持续更新，可纳入新的路由器类型和更广泛的模型池，推动该领域的系统化发展。



## 原文 PDF

![[paperPDFs/ICLR_2026/RouterArena_An_Open_Platform_for_Comprehensive_Comparison_of_LLM_Routers.pdf]]
