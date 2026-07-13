---
title: "SSE: Multimodal Semantic Data Selection and Enrichment for Industrial-scale Data Assimilation"
type: paper
paper_level: A
venue: KDD
year: 2025
pdf_ref: paperPDFs/KDD_2025/SSE_Multimodal_Semantic_Data_Selection_and_Enrichment_for_Industrial_scale_Data_Assimilation.pdf
project_link: null
code_link: null
aliases:
- SSSE
- SSE
tags:
- KDD_2025
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/vision_models_multimodal
core_operator: "利用多模态大语言模型（MLLM）为每个数据点生成细粒度语义描述，并将其转化为可聚类、可比较的语义嵌入，作为数据选择与增强的核心依据。"
primary_logic: "语义多样性（而非简单的对象分布平衡或视觉多样性）是决定数据质量和下游模型性能的关键因素；语义上非冗余的少量高质量数据可达到甚至超越全量数据的效果。"
claims:
- "在仅使用70%数据时，SSE的mAP为65.2，与原始全量数据的65.6相当，仅下降0.4，而随机、长尾和CLIP视觉基线分别下降3.5、3.3和1.2。"
- "通过语义丰富将数据集扩充至原始大小，SSE达到67.6 mAP，比原始全量数据提高2.0 mAP，远超随机和CLIP视觉基线。"
- "语义聚类能够跨不同驾驶会话捕获语义相似但视觉多样的场景，而视觉嵌入聚类倾向于局限于少数会话，说明语义嵌入提供了更泛化的场景分组。"
- "语义丰富后的数据集在稀有类别（如行人、骑自行车者）上实现了AP提升（行人+3.2，骑行者+2.6），尽管这些类别的对象数量并未增加，表明语义重要性比对象数量更关键。"
---

# SSE: Multimodal Semantic Data Selection and Enrichment for Industrial-scale Data Assimilation

> [!tip] 核心洞察
> 语义多样性（而非简单的对象分布平衡或视觉多样性）是决定数据质量和下游模型性能的关键因素；语义上非冗余的少量高质量数据可达到甚至超越全量数据的效果。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | SSE：面向工业级数据同化的多模态语义数据选择与增强 |
| 英文题名 | SSE: Multimodal Semantic Data Selection and Enrichment for Industrial-scale Data Assimilation |
| 会议/期刊 | KDD 2025 |
| Links | [paper](https://arxiv.org/abs/2409.13860) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/vision_models_multimodal |
| Method | SSE (Semantic Selection and Enrichment) |
| Dataset | Internal industrial AV dataset (8-camera, 3D object detection) |

> [!tip] 效果简介
> - Internal industrial AV dataset (8-camera, 3D object detection) 上，mAP 为 65.2 (70% data)，对比 65.6 (100% original)，变化 -0.4。
> - Internal industrial AV dataset (8-camera, 3D object detection) 上，mAP 为 67.6 (100% enriched data)，对比 65.6 (100% original)，变化 +2.0。
> - Internal industrial AV dataset (8-camera, 3D object detection) 上，mAP at 70% data 为 65.2，对比 64.4 (CLIP visual)，变化 +0.8。

## 概要

**核心问题**：大规模自动驾驶数据集的构建面临一个关键瓶颈——现有数据选择方法（如随机采样、基于对象频率的长尾平衡、基于CLIP视觉嵌入的多样性剪枝）仅关注统计分布或视觉多样性，忽视了场景语义的多样性与可解释性。这导致数据集中存在大量语义冗余，对下游任务性能的增益有限。

**核心方法**：SSE（Semantic Selection and Enrichment）提出以**语义多样性**作为数据质量的核心度量。该方法利用多模态大语言模型（MLLM）为每个数据点生成细粒度的自然语言场景描述，通过Sentence Transformer编码为语义嵌入，并以此为基础进行语义聚类与视觉去重，实现数据选择与增强。

**关键洞察**：语义多样性——而非简单的对象分布平衡或视觉多样性——是决定数据质量和下游模型性能的关键因素。语义上非冗余的少量高质量数据可以达到甚至超越全量数据的效果。

**主要结果**：
- **数据选择**：在仅保留70%数据时，SSE的mAP为65.2，与原始全量数据的65.6几乎持平（仅下降0.4），而随机、长尾和CLIP视觉基线分别下降3.5、3.3和1.2（Table 1）。
- **数据增强**：通过语义丰富将数据集扩充至原始规模，SSE达到67.6 mAP，比全量数据提高2.0 mAP，远超随机和CLIP视觉基线（Table 2）。
- **稀有类别提升**：语义丰富后的数据集在行人（+3.2 AP）和骑行者（+2.6 AP）等稀有类别上实现显著提升，尽管这些类别的对象数量并未增加，表明语义重要性比对象数量更关键（Figure 7）。

**方法定位**：SSE属于**基于多模态语义理解的数据选择与增强**范式，区别于传统的统计平衡方法（如**RFS**，Gupta et al., CVPR 2019）和纯视觉多样性方法（如**CLIP visual**，Radford et al., ICML 2021）。其核心创新在于将MLLM的场景理解能力转化为可聚类、可比较的语义嵌入，作为数据策展的核心依据。

### 工业级数据同化的核心瓶颈

自动驾驶系统的感知模型训练依赖于大规模、高质量标注数据集。然而，随着数据采集规模持续增长，数据集中存在大量冗余样本——这些样本在视觉或统计分布上重复出现，却对下游任务性能的增益极为有限。工业界面临的核心矛盾在于：**如何从海量数据中识别并保留真正关键的信息，同时控制标注与训练成本**。

现有数据选择方法主要沿两条路径展开：一类基于统计平衡，如长尾重复因子采样（RFS）（Gupta et al., CVPR 2019），通过对象类别频率调整采样权重以缓解类别不均衡；另一类基于视觉多样性，如利用CLIP视觉嵌入（Radford et al., ICML 2021）进行聚类去重，移除视觉相似样本。然而，这些方法共同存在一个根本性缺口——**缺乏对场景语义多样性与可解释性的考量**。统计平衡仅关注对象数量分布，无法区分“关键交互场景”与“平凡场景”；视觉多样性虽能去除外观重复帧，却难以捕捉高层场景语义（如“拥挤的城市十字路口”“行人即将横穿车辆前方”），导致被保留的数据在语义层面仍可能高度冗余。

### 语义缺失的后果

语义维度的缺失在自动驾驶场景中尤为致命。同一驾驶会话中连续采集的帧往往视觉高度相似且语义单一（如长时间高速公路巡航），而真正对模型鲁棒性起决定作用的“边缘场景”（corner cases）——如行人突然横穿、施工区域绕行、恶劣天气下的复杂交互——在数据集中占比极低。若数据选择仅依赖视觉嵌入聚类，聚类结果倾向于局限于少数驾驶会话（Figure 4证据：视觉聚类中每个簇的独特驾驶会话数远低于语义聚类），无法跨会话捕获语义相似但视觉多样的场景，进而导致模型对稀有但关键场景的泛化能力不足。

### 本文动机：以语义为核心的数据选择与增强

针对上述缺口，本文提出**SSE（Semantic Selection and Enrichment）**框架，核心动机在于：**将语义多样性确立为数据质量评估的第一性原理**。直觉上，一个理想的数据集应覆盖尽可能丰富的驾驶语义场景，而非简单地堆砌对象数量或追求视觉层面的多样性。为此，SSE利用多模态大语言模型（MLLM）为每个数据点生成细粒度的自然语言语义描述，将其转化为可聚类、可比较的语义嵌入，并以此为基础同时实现数据集的**语义选择**（压缩冗余）与**语义丰富**（从无标注池中挖掘语义缺失场景）。

这一思路的关键洞察在于：**语义上非冗余的少量高质量数据，可以达到甚至超越全量数据的效果**。实验证据表明，在仅保留70%数据时，SSE的mAP为65.2，与全量数据的65.6仅差0.4；而通过语义丰富将数据集扩充至原始规模后，mAP进一步提升至67.6，超出原始全量数据2.0个点（Table 1, Table 2）。更重要的是，语义丰富带来的增益在稀有类别上尤为显著——行人AP提升3.2，骑行者AP提升2.6——尽管这些类别的对象数量并未增加（Figure 7），这直接印证了**语义重要性比对象数量更关键**的核心主张。

## 核心方法与创新机理

SSE 的核心创新在于将**语义多样性**确立为数据质量与下游模型性能的核心调控变量，并构建了一套以多模态大语言模型（MLLM）为语义引擎的数据选择与增强框架。与现有方法仅依赖统计平衡或视觉多样性不同，SSE 通过三个关键“changed slots”实现了范式转变：

**1. 场景语义表示：从视觉嵌入到可解释的语义文本嵌入**

现有基线方法或缺乏显式语义（随机选择），或使用 CLIP 视觉嵌入（Radford et al., ICML 2021）作为场景表征。SSE 则利用 MLLM（如 LLaVA）为每帧图像生成细粒度的自然语言驾驶场景描述，再通过 Sentence Transformer（MPNet）将描述编码为固定长度的语义文本嵌入。这一转变使场景表征从不可解释的视觉特征空间迁移到可聚类、可比较、可解释的语义空间，为后续的数据选择与增强提供了更具判别力的基础。

**2. 数据选择策略：从对象频率平衡到“语义聚类+视觉去重”**

基线方法或采用随机采样，或基于对象频率的重复因子采样（RFS，Gupta et al., CVPR 2019），或基于 CLIP 视觉嵌入聚类后去除视觉相似样本。SSE 提出了“先语义分组，后视觉剪枝”的双阶段策略：首先对语义嵌入进行 k-means 聚类，形成语义簇；然后在每个语义簇内利用 CLIP 视觉嵌入计算余弦相似度，贪婪剪枝视觉高度相似的样本（条件为 $1 - \cos(v_i, v_j) < \epsilon$）。这一设计的因果逻辑在于：语义聚类确保保留场景类型的多样性，而视觉去重则在同类语义下剔除冗余帧，从而在压缩数据集规模的同时最大化语义覆盖。

**3. 数据丰富策略：从视觉多样性采样到语义距离最大化**

现有丰富方法依赖 CLIP 视觉嵌入的多样性采样或随机选择。SSE 则以每个语义簇的质心作为语义锚点，从未标记池中选择与所有锚点语义距离最大的样本（$\arg \max_{i \in P} (1 - \cos(t_i, t_o))$）。该策略的深层洞察是：对模型性能提升最关键的并非简单增加对象数量，而是引入与现有数据集语义差异最大的场景。实验证据直接支持了这一洞察——语义丰富后的数据集在行人（+3.2 AP）和骑自行车者（+2.6 AP）等稀有类别上实现了显著提升，尽管这些类别的对象数量并未增加（Figure 7）。

**创新点的因果验证**

上述三个 changed slots 共同指向一个核心洞察：**语义多样性是决定数据质量和下游模型性能的关键因素，语义上非冗余的少量高质量数据可达到甚至超越全量数据的效果**。决定性证据来自 Table 1 和 Table 2：在仅使用 70% 数据时，SSE 的 mAP 为 65.2，与原始全量数据的 65.6 相当（仅下降 0.4），而随机、长尾和 CLIP 视觉基线分别下降 3.5、3.3 和 1.2；通过语义丰富将数据集扩充至原始大小，SSE 达到 67.6 mAP，比原始全量数据提高 2.0 mAP。此外，Figure 4 从机制层面验证了语义嵌入的优越性：语义聚类能够跨不同驾驶会话捕获语义相似但视觉多样的场景，而视觉嵌入聚类倾向于局限于少数会话，说明语义嵌入提供了更泛化的场景分组能力。

![[assets/figures/papers/paper_list_l17_https_arxiv_org_abs_2409_13860/figures/001_Figure_1.jpg]]
*Figure 1: We introduce our semantic data selection and enrichment framework (SSE) for autonomous vehicles. The framework generates semantic captions for each data point using a foundation model, capturing semantics including scene understanding (e.g., “crowded urban intersection”) and crucial object interactions (e.g., “person about to cross in front of car”). (a) To create a compact dataset, we select the most semantically important portions of a curated and labeled dataset, removing visually similar scenes. (b) To enrich the dataset, we identify new important data points, which are semantically distant from our labeled dataset, from a growing unlabeled data pool. (c) With this approach, we maintain...*

SSE（Semantic Selection and Enrichment）是一个面向自动驾驶工业级数据同化的多模态语义数据选择与增强框架，其核心设计理念是**以语义多样性取代传统的统计平衡或视觉多样性作为数据质量的核心判据**。框架的整体流程如图1所示，包含两条对称且互补的数据管线：

### 语义选择管线（Semantic Data Selection）

该管线旨在从已标注的大规模数据集中压缩出语义非冗余的高质量子集，具体流程如下：

1. **语义描述生成**：利用多模态大语言模型（MLLM，如LLaVA）为每帧图像生成详细的自然语言驾驶场景描述，涵盖场景理解（如“拥挤的城市十字路口”）和关键对象交互（如“行人即将在车前横穿”）。
2. **文本嵌入编码**：通过Sentence Transformer（MPNet）将语义描述编码为固定长度的语义嵌入向量，捕获场景的高阶语义。
3. **语义聚类**：对语义嵌入进行k-means聚类（默认k=300），将语义相似的场景归入同一簇。
4. **视觉去重**：在每个语义簇内，利用CLIP视觉编码器获取图像嵌入，通过余弦相似度阈值ε进行贪婪剪枝——若两个样本的视觉嵌入余弦距离满足 $1 - \cos(v_i, v_j) < \epsilon$，则移除视觉冗余样本。该步骤确保每个语义簇内保留视觉多样性。

### 语义增强管线（Semantic Data Enrichment）

该管线从不断增长的未标注数据池中发掘语义新颖的样本，以增强训练集：

1. **语义锚点构建**：选取每个语义簇中距质心最近的样本作为该簇的语义锚点。
2. **语义距离最大化选择**：从未标注数据池P中，选择与所有锚点语义距离最远的样本进行添加，选择目标为 $\arg \max_{i \in P} (1 - \cos(t_i, t_o))$，重复迭代直至达到目标数据集规模。
3. **标注与合并**：选中的未标注数据按原有标注规范进行标注后，与已选数据集合并。

### 模块关系与数据流

两条管线共享前端的语义描述生成与嵌入编码模块，形成统一的语义空间。选择管线输出压缩后的核心数据集；增强管线在此基础上从外部未标注池中补充语义新颖样本。这种设计使得SSE能够同时实现**数据压缩**（仅用70%数据维持全量性能）与**性能提升**（丰富至原规模后mAP提升2.0），且整个过程具有可解释性——每个决策均可追溯到具体的语义描述。

### 关键设计决策

- **语义与视觉解耦**：语义聚类负责捕获跨场景的高层语义相似性，视觉去重负责消除同一语义簇内的低层视觉冗余，两者分工明确。
- **锚点机制**：增强选择以簇质心为锚点，而非逐样本比较，避免了计算复杂度爆炸，同时保持了语义覆盖的完整性。
- **可调控压缩比**：通过调整聚类数k和剪枝阈值ε，可灵活控制数据保留比例与性能之间的权衡。

### 语义描述生成模块

SSE的核心起点是利用多模态大语言模型（MLLM）为每帧驾驶场景图像生成自然语言描述。具体而言，使用LLaVA模型，通过专门设计的自动驾驶提示（AV prompt）引导MLLM输出包含场景整体理解（如“拥挤的城市十字路口”）和关键对象交互（如“行人即将从车前穿过”）的详细语义描述（Figure 1, Figure 3）。该模块的输出是一段可解释的文本段落，作为后续所有语义操作的原始材料。

### 文本嵌入编码模块

将MLLM生成的语义描述文本输入Sentence Transformer（具体采用MPNet模型），编码为固定长度的语义嵌入向量 $t_i$。这一步将非结构化的自然语言转化为可聚类、可比较的向量表示，是整个框架中语义多样性度量的数学基础（Section 2）。

### 语义聚类模块

对标注数据集中所有样本的语义嵌入 $\{t_i\}$ 执行k-means聚类，形成 $k$ 个语义簇。每个簇内的样本在语义上相近（如都包含“行人横穿马路”场景），但在视觉上可能差异显著。消融实验表明，$k=300$ 时达到数据压缩率与下游性能的最佳平衡（Figure 9）。

### 视觉去重模块

在每个语义簇内部，利用CLIP视觉编码器获取图像嵌入 $v_i$，通过余弦相似度进行贪婪剪枝。具体剪枝条件为：

$$1 - \cos(v_i, v_j) < \epsilon$$

若样本 $i$ 与 $j$ 在CLIP视觉嵌入空间中的余弦距离小于阈值 $\epsilon$，则认为两者视觉高度相似，将 $j$ 从数据集中移除（Algorithm 1）。阈值 $\epsilon$ 直接控制数据保留比例，$\epsilon$ 越大保留数据越多（Figure 8）。

### 语义锚点构建与丰富选择模块

在数据丰富阶段，选取每个语义簇中离质心最近的样本作为该簇的语义锚点 $t_o$。随后，从未标记数据池 $P$ 中选择与所有锚点语义距离最大的样本进行添加：

$$\arg \max_{i \in P} \left(1 - \cos(t_i, t_o)\right)$$

该公式的核心机制是最大化候选样本与现有语义锚点的余弦距离，从而优先补充语义上最为稀缺的场景类型。重复此过程直至数据集达到目标规模（Algorithm 1）。

### 模块间的因果链路

上述模块构成一条完整的因果链路：**语义描述生成 → 文本嵌入编码 → 语义聚类 → 视觉去重（选择）或语义距离最大化（丰富）**。语义聚类提供了跨驾驶会话的场景分组能力（Figure 4），视觉去重消除了语义簇内的冗余，而语义距离最大化选择则确保新增数据在语义空间上对现有数据集形成有效补充。这一链路的核心洞察在于：语义多样性（而非对象分布平衡或视觉多样性）是决定数据质量和下游模型性能的关键因子。

## 实验与关键发现

### 实验设置

实验基于一个内部工业级自动驾驶数据集，该数据集由8个摄像头采集，标注任务为3D目标检测。所有数据选择与丰富实验均在该数据集上进行，下游模型训练与评估遵循统一的标注规范。语义描述生成采用多模态大语言模型LLaVA，语义嵌入编码使用Sentence Transformer（MPNet），视觉嵌入则通过CLIP视觉编码器提取。数据选择阶段，语义聚类数k默认设为300，视觉去重阈值ε控制压缩比例；数据丰富阶段，从未标记池中按语义距离最大化原则选取样本并标注后加入训练集。

### 数据选择主结果

Table 1展示了不同数据选择策略在保留70%原始数据时的下游3D检测性能。SSE方法在仅使用70%数据时达到65.2 mAP，与原始全量数据（100%）的65.6 mAP相比仅下降0.4，基本维持了原始性能。相比之下，随机选择下降3.5 mAP（至62.1），长尾选择（RFS，Gupta et al., CVPR 2019）下降3.3 mAP（至62.3），CLIP视觉嵌入选择下降1.2 mAP（至64.4）。这一结果表明，语义多样性驱动的数据选择能够有效识别并保留对下游任务最关键的数据子集，而单纯依赖对象分布平衡或视觉多样性的方法则因无法区分场景语义重要性而丢失关键信息。

![[assets/figures/papers/paper_list_l17_https_arxiv_org_abs_2409_13860/figures/003_Table_1.jpg]]
*Table 1: Performance on downstream 3D detection with different Data Selection strategies. SSE achieves 30% data reduction while maintaining original mAP*

**Table 1** 的核心结论是：SSE在30%的数据压缩率下实现了与全量数据相当的检测性能，验证了语义选择策略的有效性。

### 数据丰富主结果

Table 2展示了将选择后的数据集通过语义丰富扩充至原始规模时的性能对比。SSE丰富后的数据集达到67.6 mAP，比原始全量数据的65.6 mAP提升了2.0 mAP。随机丰富仅达到65.0 mAP，CLIP视觉丰富达到66.0 mAP。值得注意的是，长尾方法因未标记池缺乏标签而无法应用于丰富场景。SSE在85%数据量时即已超越全量数据性能（+0.9 mAP），表明语义丰富能够从未标记池中挖掘出对模型泛化具有高价值的稀缺场景。

![[assets/figures/papers/paper_list_l17_https_arxiv_org_abs_2409_13860/figures/004_Table_2.jpg]]
*Table 2: Performance on downstream 3D detection with different Data Enrichment methods. SSE improves 2 mAP when expanding the dataset to the original size. Note longtail is impossible due to the lack of labels in data pool*

**Table 2** 的核心结论是：语义丰富不仅弥补了数据选择带来的微小性能损失，还通过引入语义多样化的新样本，使模型性能显著超越原始全量训练。

### 语义聚类与视觉聚类的对比分析

Figure 4 对比了语义嵌入聚类与CLIP视觉嵌入聚类中每个簇所包含的独特驾驶会话数。语义聚类能够跨不同驾驶会话捕获语义相似但视觉多样的场景，簇内独特会话数显著高于视觉聚类；而视觉聚类倾向于将同一会话中视觉相似的帧归入同一簇，缺乏跨会话的泛化性。Figure 5 进一步可视化了单个语义簇内的样本，这些场景在视觉上差异显著（不同光照、天气、视角），但语义上高度一致——均为“行人/骑行者靠近自车且可能横穿马路”的危险场景。这解释了语义选择为何能保留对下游任务至关重要的高价值场景，而视觉方法可能因视觉重复而将其误删。

### 稀有类别性能提升分析

Figure 6 显示，SSE选择的数据集中独特对象数量并未显著增加，甚至在某些类别上少于长尾方法。然而，Figure 7 的每类检测精度与训练对象数量的散点图揭示了一个关键发现：经过SSE语义丰富后，稀有类别（如行人、骑自行车者）的检测精度显著提升——行人AP提升3.2，骑行者AP提升2.6——尽管这些类别的训练对象数量并未增加。这表明，语义重要性（即场景中对象的交互上下文与危险程度）比单纯的对象数量对模型性能的影响更为关键。语义丰富引入的是“高质量”对象实例（如正在横穿马路的行人），而非简单增加对象计数。

![[assets/figures/papers/paper_list_l17_https_arxiv_org_abs_2409_13860/figures/009_Figure_7.jpg]]
*Figure 7: Per class detection accuracy as a function of object count in train data, across different methodologies. SSE semantically tunes the dataset and demonstrates that less but more high-quality objects lead to better performance in rare categories*

### 超参数敏感性分析

剪枝阈值ε对数据保留比例有显著影响（Figure 8）：ε越大，视觉相似性判据越宽松，保留数据越多，压缩率越低。该参数提供了可控的压缩比调节机制。聚类数k的消融实验（Figure 9）表明，k=300时SSE在70%数据保留率下达到性能与压缩的最佳平衡；k过小会导致语义簇粒度过粗，丢失细粒度场景区分能力；k过大则导致簇内样本过少，视觉去重效果减弱，数据保留率上升。

### 方法鲁棒性分析

Figure 10 展示了使用不同MLLM（LLaVA与CLIP）生成语义描述时SSE的性能趋势，结果表明方法对MLLM的选择具有较好的鲁棒性，性能趋势保持一致。Figure 11 的提示敏感性实验进一步表明，专门为自动驾驶设计的提示（AV prompt）相比通用提示能更好地引导MLLM关注驾驶关键语义（如危险交互、复杂路况），从而提升数据选择质量。语义检索与CLIP视觉检索的定性对比（Figure 12、Figure 14）也佐证了这一优势：语义检索能够理解“减速慢行”这类高层语义，检索到车辆加塞、骑行者横穿、密集行人、暴雨等视觉多样但语义相关的场景；而CLIP视觉检索则返回大量视觉重复的高速公路图像，缺乏对场景高层语义的理解能力。

![[assets/figures/papers/paper_list_l17_https_arxiv_org_abs_2409_13860/figures/017_Figure_14.jpg]]
*Figure 14: Additional retrieval examples using advanced visual embeddings and semantic embeddings. Table 3: Per-class AP of 3D object detection with different data strategies*

### 局限与失败模式

尽管SSE在工业级自动驾驶数据集上展现了显著优势，但仍存在以下局限：首先，实验仅在一个内部专有数据集上进行，尚未在公开数据集或其他领域验证泛化性，结果的普适性需进一步确认。其次，方法依赖大规模MLLM生成语义描述，推理成本较高，可能限制在资源受限环境中的部署。此外，语义描述质量对最终性能的敏感度尚未量化分析，提示设计的自动化优化仍是开放问题。最后，论文未专门评估数据选择过程中可能引入的社会偏见或类别不平衡偏见，而MLLM生成的语义描述可能隐含模型自身的偏见，需在实际应用中加以关注。

![[assets/figures/papers/paper_list_l17_https_arxiv_org_abs_2409_13860/figures/013_Figure.jpg]]
*Figure: (a) Three prompts (b) Dataset semantic selection and enrichment with different prompts*

## 定位与知识库关联

### 核心思想定位

SSE 的核心贡献在于将**语义多样性**确立为数据质量的核心度量，替代了传统数据选择中依赖的统计平衡或视觉多样性范式。其因果机制可概括为：利用多模态大语言模型（MLLM）将场景图像转化为可解释的自然语言描述，再通过文本嵌入将语义转化为可聚类、可比较的向量空间，从而在语义层面而非视觉层面进行数据去重与扩充。

这一思路与现有基线形成本质差异：
- **Random selection**：无任何数据质量考量，仅做均匀采样，无法区分冗余样本与关键样本。
- **Long-tail (RFS)**（Gupta et al., CVPR 2019）：基于对象类别频率进行平衡采样，试图提升稀有类别的覆盖。但其核心假设是“对象数量决定数据价值”，忽视了同一类别对象在不同语义场景下的学习价值差异。SSE 的实验证明，语义选择后的数据集稀有对象数量并未增加，但稀有类别检测精度反而提升（行人 +3.2 AP，骑行者 +2.6 AP），直接挑战了该假设。
- **CLIP visual**（Radford et al., ICML 2021）：利用 CLIP 视觉嵌入进行聚类和多样性采样，是目前视觉数据选择中的强基线。然而，视觉嵌入聚类倾向于将同一驾驶会话中视觉相似的帧归为一组，缺乏跨会话的语义泛化能力。SSE 通过语义嵌入聚类显著提升了跨会话多样性，且在下游任务上持续优于 CLIP 视觉基线（70% 数据下 mAP 65.2 vs 64.4）。

### 方法适用边界

**适用场景**：
- 大规模、多模态、存在大量视觉冗余的数据集，尤其是自动驾驶场景下的多相机视频数据。
- 需要从无标签数据池中主动选择高价值样本进行标注的持续学习或数据闭环场景。
- 对数据选择过程有可解释性要求的工业级数据同化流程——SSE 生成的语义描述天然提供了选择理由。

**不适用或需谨慎使用的场景**：
- 数据规模极小或语义多样性本身已饱和的数据集，语义聚类可能无法有效区分样本。
- 对推理延迟或计算成本极度敏感的边缘端部署场景，MLLM 的推理开销可能成为瓶颈。
- 语义描述质量高度依赖 MLLM 能力和提示设计，若目标场景的语义空间与 MLLM 训练分布偏差较大，生成的语义描述可能不可靠。

### 局限与开放问题

**已知局限**：
1. **领域泛化未验证**：所有实验均在一个未公开的内部工业自动驾驶数据集上进行，尚未在其他领域（如医疗影像、机器人操作）或公开基准（如 nuScenes、Waymo Open Dataset）上验证方法泛化性。
2. **MLLM 推理成本**：为每个数据点生成细粒度语义描述需要调用大规模 MLLM（如 LLaVA），在百万级数据规模下的计算开销可能成为工业部署瓶颈。论文未讨论语义描述的缓存复用或轻量化替代方案。
3. **超参数依赖**：聚类数 $k$ 和剪枝阈值 $\epsilon$ 对最终数据保留率和下游性能有显著影响，但论文仅通过网格搜索确定最优值，未提供自动调参或自适应策略。
4. **潜在偏见传递**：MLLM 生成的语义描述可能隐含模型自身的训练偏见，SSE 未评估数据选择过程中是否放大了社会偏见或类别不平衡偏见。

**开放问题**：
- 语义丰富策略在未标记池规模远超原始数据集时的性能饱和点在哪里？是否存在边际收益递减规律？
- 语义嵌入能否推广至激光雷达、雷达等其他传感器模态，实现多模态融合的联合数据选择？
- 如何量化语义多样性与模型鲁棒性/公平性之间的因果关系，从而将数据选择从“性能导向”升级为“安全导向”？
- 提示设计对语义质量的影响已被初步验证，但能否通过自动提示优化或强化学习进一步消除人工调参？

## 原文 PDF

![[paperPDFs/KDD_2025/SSE_Multimodal_Semantic_Data_Selection_and_Enrichment_for_Industrial_scale_Data_Assimilation.pdf]]
