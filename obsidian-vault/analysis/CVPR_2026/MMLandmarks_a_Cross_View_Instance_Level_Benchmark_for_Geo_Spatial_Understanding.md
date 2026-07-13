---
title: "MMLandmarks: a Cross-View Instance-Level Benchmark for Geo-Spatial Understanding"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/MMLandmarks_a_Cross_View_Instance_Level_Benchmark_for_Geo_Spatial_Understanding.pdf
project_link: "https://mmlandmarks.compute.dtu.dk"
code_link: null
aliases:
- MMLandmarks
tags:
- CVPR_2026
- topic/benchmarks_datasets_evaluation
- topic/benchmarks_datasets_evaluation/benchmarking
core_operator: 通过构建覆盖四种模态（地面图像、航拍图像、文本、GPS坐标）且实例级完全对应的MMLANDMARKS数据集，并采用成对对比损失进行多模态联合训练。
primary_logic: 以地标实例为核心，利用OpenStreetMaps和Wikimedia Commons的关联信息，能够构建一个大规模、多模态、具有时间变化和自然复杂性的数据集，使得一个简单的CLIP风格基线模型也能在多个地理空间任务上展现出强大的跨模态泛化能力。
claims:
- 跨视角检索任务中，基线模型MMCLIP以较大优势超越现有多模态基础模型和专门的跨视角模型，在Satellite→Ground上R@1达18.8%，而最佳基础模型SigLIP2仅为4.1%。
- 在Ground-to-Sat-to-GPS和Satellite-to-GPS定位任务中，结合卫星索引显著提升了精细定位的准确性，基线模型在1km距离内分别达到18.41%和36.9%，远超其他模型。
- "消融实验表明，使用最新的卫星图像（L: last）和仅使用室外地面图像（Subset）能显著提升各项任务性能，验证了数据质量对多模态学习的重要性。"
- MMLANDMARKS 跨视角检索（Satellite→Ground） 上 R@1 = 18.8 (MMCLIP)
---

# MMLandmarks: a Cross-View Instance-Level Benchmark for Geo-Spatial Understanding

> [!tip] 核心洞察
> 以地标实例为核心，利用OpenStreetMaps和Wikimedia Commons的关联信息，能够构建一个大规模、多模态、具有时间变化和自然复杂性的数据集，使得一个简单的CLIP风格基线模型也能在多个地理空间任务上展现出强大的跨模态泛化能力。

| 字段 | 内容 |
|------|------|
| 中文题名 | MMLandmarks：面向地理空间理解的跨视角实例级基准 |
| 英文题名 | MMLandmarks: a Cross-View Instance-Level Benchmark for Geo-Spatial Understanding |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://openaccess.thecvf.com/content/CVPR2026/html/Kristoffersen_MMLandmarks_a_Cross-View_Instance-Level_Benchmark_for_Geo-Spatial_Understanding_CVPR_2026_paper.html) · [Project](https://mmlandmarks.compute.dtu.dk) |
| Topic | #topic/benchmarks_datasets_evaluation #topic/benchmarks_datasets_evaluation/benchmarking |
| Method | MMCLIP |
| Dataset | MMLANDMARKS 跨视角检索（Satellite→Ground）, MMLANDMARKS 跨视角检索（Ground→Satellite）, MMLANDMARKS 地面图像定位（Ground-to-Sat-to-GPS）, MMLANDMARKS 卫星图像定位（Satellite-to-GPS） |

> [!tip] 效果简介
> - MMLANDMARKS 跨视角检索（Satellite→Ground） 上，R@1 18.8 (MMCLIP) vs 4.1 (SigLIP2 ViT-L/512) (+14.7)。
> - MMLANDMARKS 跨视角检索（Ground→Satellite） 上，R@1 20.5 (MMCLIP) vs 14.6 (SigLIP2 ViT-L/512) (+5.9)。
> - MMLANDMARKS 地面图像定位（Ground-to-Sat-to-GPS） 上，Distance(% @ 1 km) 18.41 (MMCLIP) vs 8.04 (OAI-CLIP ViT-L/336) (+10.37)。

## 概要

现有地理空间理解数据集长期受限于两个瓶颈：其一，缺乏跨视角、实例级的细粒度对应关系，地面图像、航拍图像、文本描述和GPS坐标往往孤立存在，难以支撑统一的多模态学习；其二，主流跨视角基准（如CVUSA、CVACT）已趋于饱和，场景多样性不足，无法反映真实世界中的视角变化、时间演化和自然复杂性。**MMLandmarks**（CVPR 2026）针对上述瓶颈，构建了一个覆盖美国本土18,557个地标的大规模多模态数据集，首次在实例级别将地面图像、航拍图像、文本描述和GPS坐标四种模态完全对齐，为地理空间理解提供了更具挑战性和现实意义的评测平台。

论文的核心洞察在于：以OpenStreetMaps和Wikimedia Commons中的地标实例为锚点，利用其天然的多模态关联信息，可以规模化地构建高质量跨视角数据。基于此数据集，作者提出了一个简洁的基线模型**MMCLIP**——冻结CLIP的图像和文本编码器，辅以GeoCLIP风格的GPS编码器，通过可训练的投影头将所有模态映射到共享嵌入空间，并以成对InfoNCE损失进行联合训练。尽管方法简单，MMCLIP在跨视角检索、地面图像定位、卫星图像定位和文本到任意模态检索四项任务上均以显著优势超越现有基础模型和专用模型，验证了数据集本身的质量和设计理念的有效性。

### 核心结论

- **跨视角检索**：在Satellite→Ground方向上，MMCLIP的R@1达到18.8%，而最佳现成基础模型SigLIP2仅为4.1%（Table 2）；Ground→Satellite方向上R@1为20.5%，同样大幅领先。这表明实例级对齐数据能有效弥合地面与航拍视角之间的语义鸿沟。

- **地理定位**：引入卫星图像作为中间索引后，地面图像定位（Ground-to-Sat-to-GPS）在1 km距离内的准确率达18.41%，卫星图像直接定位（Satellite-to-GPS）达36.9%，远超GeoCLIP等专用模型（Table 3, Table 4）。这一结果揭示了跨视角特征对齐对精细定位的关键作用。

- **多模态泛化**：MMCLIP在文本到卫星检索（R@1=13.4%）和文本到GPS定位等任务上也展现出良好的跨模态迁移能力，证明统一的嵌入空间能够支撑多种下游应用。

- **数据质量的关键性**：消融实验（Table 6）表明，使用最新卫星图像、仅保留室外地面图像、以及采用文本首句进行训练，均能显著提升性能，为后续数据集构建提供了明确的实践指导。

### 方法定位与知识库定位

MMLandmarks在方法谱系上处于**多模态地理空间基准构建**与**跨视角对比学习**的交汇点。与传统的单任务数据集（如CVUSA仅支持地面-卫星检索）不同，MMLandmarks以地标实例为核心，将四种模态统一到同一基准下，填补了现有资源在实例级跨模态对齐上的空白。其基线模型MMCLIP延续了CLIP（Radford et al., ICML 2021）的对比学习范式，并将其从图像-文本双模态扩展到四模态联合训练，同时借鉴了GeoCLIP（Vivanco Cepeda et al., NeurIPS 2023）的位置编码思路，属于轻量级多模态对齐方法。与Sample4Geo-UNI等专用跨视角模型相比，MMCLIP无需复杂的几何变换或视角合成，仅依赖数据本身的对齐质量即可取得更优性能，这反衬出MMLandmarks数据集的设计价值。

### 局限与开放问题

尽管结果令人鼓舞，MMLandmarks目前仍存在若干限制：数据集仅覆盖美国本土，地标分布偏向大城市和旅游热点区域，对全球其他地区及乡村场景的泛化能力尚待验证；地面图像中约17%为室内照片，虽经VLM过滤仍可能引入噪声；跨视角域间隙依然存在，基线模型未利用高级几何对齐或时序信息。这些限制也指向了未来的研究方向——如何将框架扩展至全球范围、如何利用多时相航拍图像实现变化检测、以及如何与更大规模的基础模型结合以突破精细定位的瓶颈。



### 地理空间理解的跨视角瓶颈

地理空间人工智能的核心挑战之一，在于弥合不同观测视角与数据模态之间的语义鸿沟。地面图像捕捉了人类尺度的地标细节，而卫星与航拍图像则提供了宏观的几何与布局信息。将这两种视角关联起来，是实现精确地理定位、跨视角检索与场景理解的关键。然而，现有工作长期面临一个根本性瓶颈：**缺乏大规模、实例级对齐的多模态数据集**。

当前主流的地理空间基准，如 CVUSA、CVACT 或 VIGOR，虽然在跨视角地面-卫星检索任务上推动了方法演进，但其规模通常局限于数百至数千个实例，且模态覆盖有限。更关键的是，这些数据集往往仅提供图像对之间的粗粒度对应，缺少文本描述与精确 GPS 坐标的细粒度绑定。这导致两个直接后果：其一，模型难以学习到地标特有的语义属性（如建筑风格、历史背景）；其二，跨视角检索的基准性能趋于饱和，现有模型在简单场景下已接近天花板，却无法应对真实世界中视角变化剧烈、光照差异大、地标分布稀疏的复杂情况。

### 现有数据资源的缺口

从数据构建的角度看，已有资源在模态完整性、实例对齐精度与许可开放性上存在明显短板。Table 1 的系统对比揭示了这一缺口：多数数据集仅包含两到三种模态，且 GPS 坐标往往仅作为弱标签存在，而非精确的地标中心点。例如，**GeoCLIP**（Vivanco Cepeda et al., NeurIPS 2023）依赖 GPS 编码器进行地理定位，但其训练数据中的位置信息与视觉内容的对应关系并不严格；**Sample4Geo** 等专用跨视角模型则在有限的城市级数据上训练，泛化能力受限。此外，大规模预训练模型如 **OAI-CLIP**（Radford et al., ICML 2021）和 **SigLIP2**（Tschannen et al., arXiv 2025）虽然在图像-文本对齐上表现卓越，但缺乏对航拍视角与精确空间坐标的联合建模能力，在卫星图像检索任务上 R@1 仅约为 4.1%（Table 2）。

更深层的问题在于，现有数据集未能充分利用公开可用的地理知识图谱。OpenStreetMaps 提供了数百万个带有维基百科标识符的多边形地标，Wikimedia Commons 则关联了丰富的众包地面图像。这些资源天然构成了实例级的多模态对应关系，却长期未被系统性地整合为可训练的基准。

### 本文动机：以地标实例为核心的统一基准

针对上述缺口，本文提出 **MMLANDMARKS**——一个面向地理空间理解的跨视角实例级基准。其核心动机并非设计复杂的新模型架构，而是构建一个**以地标实例为锚点的多模态数据集**，使得即便是简单的 CLIP 风格基线，也能展现出强大的跨模态泛化能力。

MMLANDMARKS 的构建逻辑围绕一个关键因果机制展开：当地面图像、航拍图像、文本描述与 GPS 坐标在实例级别完全对应时，多模态联合训练能够迫使模型学习到视角不变的地标表示。这一机制通过三个设计要素实现：

1. **实例级对齐**：每个地标拥有唯一标识符，所有模态数据均绑定到该标识符下的同一地理实体，消除了粗粒度匹配带来的歧义。
2. **多模态覆盖**：数据集包含 18,557 个地标的 329,349 张地面图像、197,205 张航拍图像、18,557 条文本语料与精确 GPS 坐标，覆盖四种模态的完整配对。
3. **真实世界复杂性**：地面图像来自 Wikimedia Commons 的众包贡献，包含多样的拍摄角度、光照条件与季节变化；航拍图像来自 NAIP 项目的多年时序数据，天然引入了时间变化这一未标注但可探索的维度。

Figure 1 展示了这一多模态对应关系的直观示例：同一地标在不同模态下呈现出互补的语义信息——地面图像捕捉建筑立面的细节，航拍图像揭示其与周边道路的空间关系，文本描述提供历史与功能背景，GPS 坐标则锚定其绝对地理位置。

### 从数据到基线：MMCLIP 的设计哲学

本文并未追求方法上的激进创新，而是有意采用了一个简单的基线模型 **MMCLIP**。该模型使用冻结的 CLIP ViT 编码器分别提取地面与航拍图像特征，结合 CLIP 文本编码器与基于 GeoCLIP 的 GPS 编码器，通过可训练的投影头将四种模态映射到共享嵌入空间，并采用成对 InfoNCE 损失进行联合优化。这一设计的核心洞察在于：**当数据质量足够高、模态对齐足够精确时，简单的对比学习框架即可解锁强大的跨模态检索与定位能力**。

后续实验（Table 2–Table 5）将证明，MMCLIP 在跨视角检索任务上以较大优势超越现有基础模型与专用模型，例如 Satellite→Ground 的 R@1 达到 18.8%，而最佳基线 SigLIP2 仅为 4.1%。这验证了本文的核心主张：数据集的构建质量是当前地理空间理解任务的首要瓶颈，而非模型架构的复杂度。

### 局限性与开放问题

尽管 MMLANDMARKS 在数据规模与模态完整性上迈出了重要一步，但其覆盖范围目前仅限于美国本土，地标分布偏向大城市及旅游聚集区，对全球其他地区及乡村场景的泛化能力尚未验证。此外，地面图像中约 17% 为室内照片，可能引入空间对齐的噪声；跨视角域间隙依然存在，航拍图像的俯视特征与地面图像的透视变形之间的对应关系仍具挑战。这些问题为未来的数据集扩展与方法改进指明了方向。



## 核心方法与创新机理

MMLANDMARKS 的核心创新并非提出一个复杂的模型架构，而是通过**构建一个实例级对齐的多模态数据集**，改变了地理空间理解任务的学习范式。其关键洞察在于：以地标实例为纽带，将四种天然异构的模态（地面图像、航拍图像、文本描述、GPS坐标）在实例层面完全对应起来，从而使得一个简单的 CLIP 风格基线模型也能在多个地理空间任务上展现出强大的跨模态泛化能力。

### 创新一：实例级多模态对齐数据集

现有地理空间数据集的核心瓶颈在于缺乏跨视角、实例级的对应关系。如表 1 所示，此前的基准要么仅覆盖单一模态对（如地面-卫星图像对），要么缺乏文本描述或精确坐标的配对，导致模型难以进行细粒度的地标理解。

MMLANDMARKS 通过以下方式突破了这一瓶颈：

1. **以地标实例为锚点**：利用 OpenStreetMaps 的 Wikipedia/Wikidata 标签筛选地标多边形，并通过 Wikimedia Commons 页面获取地面图像，通过 Wikipedia 页面获取文本描述，同时从地标边界框直接获取 GPS 坐标和航拍图像。这一流水线确保了四种模态在 **18,557 个独立地标实例**上完全对应。
2. **自然复杂性**：数据集天然包含时间变化（航拍图像跨越多年度）、视角多样性（地面图像来自不同拍摄者）和室内外混合（约 17% 室内图像），无需人工注入噪声即可反映真实世界的复杂性。

### 创新二：全模态成对对比学习框架

与现有方法相比，MMCLIP 在三个关键维度上做出了改变：

| 变化维度 | 现有方法 | MMCLIP | 证据锚点 |
|---------|---------|--------|---------|
| **训练数据集** | 大规模网络图像-文本对（如 CLIP 所用数据） | MMLANDMARKS 四模态实例级对齐数据 | Sec. 4, Architecture |
| **模态组合** | 仅图像和文本两种模态 | 地面图像、航拍图像、文本、GPS 四种模态联合训练 | Sec. 4, Architecture and Loss Function |
| **损失函数** | 标准 InfoNCE 损失用于单一模态对 | 扩展的成对 InfoNCE 损失，对 $K(K-1)$ 个模态对求平均 | Sec. 4, Loss Function, Equation 1 |

其损失函数为：

$$\mathcal { L } = \frac { 1 } { K ( K - 1 ) } \sum _ { i = 1 } ^ { K } \sum _ { \substack { j = 1 \\ j \neq i } } ^ { K } \mathcal { L } _ { i , j }$$

这一设计的因果机制在于：通过在所有模态对之间施加对比约束，模型被迫学习一个统一的嵌入空间，其中同一地标的不同模态表示被拉近，不同地标的表示被推远。这比仅训练图像-文本对的模型获得了更丰富的跨模态监督信号。

### 创新三：以数据质量驱动性能提升

消融实验（Table 6）揭示了一个重要发现：**数据质量比模型复杂度更重要**。具体而言：

- 使用最新的卫星图像（L: last）替换随机时间采样的图像，显著提升了跨视角检索和定位性能；
- 采用文本的第一句话（F: first sentence）进行训练，相比随机采样句子，在文本相关任务上表现更好；
- 仅使用室外地面图像子集（Subset）训练，进一步消除了室内图像带来的空间对齐噪声。

这些结果表明，MMLANDMARKS 的创新价值不仅在于其规模，更在于其精心设计的数据筛选策略，使得即使使用冻结的 CLIP 编码器和简单的投影头，也能在跨视角检索（Satellite→Ground R@1 达 18.8%，而最佳基础模型 SigLIP2 仅为 4.1%）和精细定位（1 km 内 Satellite-to-GPS 达 36.9%）等任务上大幅超越现有方法。



MMLANDMARKS的整体框架由两个核心阶段构成：**数据集构建流水线**与**多模态联合训练基线模型（MMCLIP）**。前者以地标实例为中心，从多源异构数据中提取并对齐四种模态；后者通过一个轻量的成对对比学习框架，将所有模态映射到共享嵌入空间，支撑下游的跨模态检索与定位任务。

### 数据集构建流水线

数据集的构建遵循“以地标实例为锚点，多模态信息汇聚”的设计思路。流水线起始于OpenStreetMap（OSM）中美国境内的所有多边形要素，通过筛选包含`wikipedia`或`wikidata`标签的条目，锁定具有公开知识库条目的候选地标。随后，系统验证每个候选地标是否同时拥有Wikipedia页面（提供文本描述）和Wikimedia Commons页面（提供地面图像），并检查其外接矩形的最长边是否小于400米，以保证数据集中地标尺度的均匀分布。通过上述过滤的每个地标实例，天然具备四种模态的对应关系：Wikimedia Commons图像作为**地面视角**、Wikipedia文本作为**语义描述**、OSM多边形中心作为**GPS坐标**、以及来自USDA NAIP 的关联**航拍图像**。这一流水线最终产出了一个包含18,557个地标、329,349张地面图像、197,205张航拍图像及等量文本与坐标的大规模实例级对齐数据集。

### MMCLIP基线模型架构

在数据集之上，作者设计了一个简洁的多模态联合训练基线模型MMCLIP，其架构遵循“冻结编码器 + 可训练投影头 + 成对对比损失”的范式。模型接收四种模态的输入，分别通过专用编码器提取特征：

- **地面图像与航拍图像**共享一个冻结的CLIP ViT图像编码器，将两类视角的图像映射到统一的视觉特征空间。
- **文本描述**（地标的Wikipedia条目）通过冻结的CLIP文本编码器提取语义特征。
- **GPS坐标**采用基于**GeoCLIP**（Vivanco Cepeda et al., NeurIPS 2023）的位置编码器，将经纬度映射为连续的嵌入向量，以捕捉地理空间的邻近关系。

每个编码器之后连接一个**投影头**，由两层可训练线性层与中间的ReLU激活组成，将所有模态的特征投影到维度为512的公共嵌入空间。这一设计使得不同模态的表示在维度上对齐，为后续的对比学习奠定基础。

### 训练目标与信息流

训练的核心是将同一地标实例的不同模态表示拉近，将不同实例的表示推远。具体而言，模型采用**成对InfoNCE损失**（Pairwise InfoNCE Loss），对四种模态（$K=4$）中所有$K(K-1)$个有序模态对计算对比损失并取平均：

$$\mathcal { L } = \frac { 1 } { K ( K - 1 ) } \sum _ { i = 1 } ^ { K } \sum _ { \substack { j = 1 \\ j \neq i } } ^ { K } \mathcal { L } _ { i , j }$$

其中$\mathcal{L}_{i,j}$为模态$i$到模态$j$的标准InfoNCE损失。该损失函数驱动模型学习一个模态无关的共享表示空间，使得地面图像、航拍图像、文本和GPS坐标在嵌入空间中按地标实例聚合。

### 推理与下游任务流

训练完成后，MMCLIP的共享嵌入空间可直接支持多种地理空间理解任务，无需额外微调：

- **跨视角检索**：将查询模态的嵌入与索引库中目标模态的嵌入进行最近邻搜索，实现地面↔卫星的双向检索。
- **地面图像定位**：采用“地面→卫星→GPS”的级联策略——先用地面图像检索最匹配的卫星图像，再以该卫星图像对应的GPS坐标作为定位结果，从而将跨视角匹配能力转化为地理位置预测。
- **卫星图像定位**：直接将卫星图像嵌入与GPS嵌入库进行最近邻匹配，输出预测坐标。
- **文本到任意模态检索**：以文本描述为查询，检索对应的卫星图像或GPS坐标，验证语言与地理空间模态的对齐质量。

整个框架的信息流以地标实例为枢纽，从多源数据的采集与对齐，到多模态嵌入空间的联合优化，再到统一嵌入支持的多任务推理，形成了一个闭环的地理空间理解系统。

### 补充图表

![[assets/figures/papers/paper_list_l822_https_openaccess_thecvf_com_content_CVPR2026_html_Kristoffersen_MMLandma/figures/001_Figure_1.jpg]]
*Figure 1: MMLANDMARKS. We present four distinct data modalities: ground-view images, aerial imagery, GPS coordinates, and textual descriptions, collected from 18,557 unique landmarks in the United States. Data sources are included alongside each modality*

![[assets/figures/papers/paper_list_l822_https_openaccess_thecvf_com_content_CVPR2026_html_Kristoffersen_MMLandma/figures/003_Figure_2.jpg]]
*Figure 2: Pipeline for collecting the landmarks with the required criteria. Tags from OpenStreetMaps are used to collect Wikiidentifiers, ensuring that landmarks have a Wikipedia and Wikimedia Commons page. If both are available, we check that the longest edge of the landmark’s bounding box is smaller than 400 meters to keep an even size distribution across the dataset. Every resulting landmark has a Wikimedia Commons page (ground), a Wikipedia page (text), a box size and center (coordinates), and associated aerial imagery (satellite)*



MMCLIP 基线模型的核心设计思想是：将四种异构模态（地面图像、航拍图像、文本描述、GPS 坐标）映射到一个共享的 512 维嵌入空间，使得同一地标实例的不同模态表示相互靠近，不同实例的表示相互远离。模型由四个编码器与一个成对对比损失函数构成。

### 编码器模块

**地面图像编码器与航拍图像编码器** 均采用冻结的 CLIP ViT 图像编码器（Sec. 4, Architecture）。这一选择基于 CLIP 在大规模图像-文本预训练中获得的强泛化视觉表示能力。两个编码器共享相同的骨干网络权重，但分别处理地面视角和俯视视角图像。值得注意的是，航拍图像在纹理、尺度、视角上与自然图像存在显著差异，冻结的编码器可能无法充分适应航拍图像的独特特征，这构成了一个潜在的性能瓶颈。

**文本编码器** 使用与图像编码器对应的冻结 CLIP 文本编码器，输入为来自 Wikipedia 的地标文本描述（Sec. 4, Architecture）。文本编码器与图像编码器的冻结搭配，保证了多模态对齐的初始先验得以保留，同时将可训练参数集中在投影层上。

**GPS 编码器** 基于 GeoCLIP（Vivanco Cepeda et al., NeurIPS 2023）的位置编码器设计，将经纬度坐标 $(\phi, \lambda)$ 映射为连续的嵌入向量（Sec. 4, Architecture）。该编码器通过球面谐波函数或类似的正弦位置编码机制，将地理坐标的周期性和空间邻近关系编码到嵌入空间中，使模型能够学习“地理相近则语义相近”的先验。

### 投影头

每个编码器之后均附加一个投影头（Projection Head），由两层可训练线性层组成，中间以 ReLU 激活函数分隔（Sec. 4, Architecture）。投影头将各编码器输出的不同维度特征统一投影到 $d = 512$ 的公共空间，同时引入非线性变换以增强模态间的对齐灵活性。这一设计遵循了 SimCLR 等对比学习框架的经典范式：在冻结的骨干网络之上训练轻量投影层，既能保留预训练知识，又能适应下游多模态对齐任务。

### 成对对比损失

MMCLIP 的核心数学机制是**成对 InfoNCE 损失**（Pairwise InfoNCE Loss），其定义为对 $K$ 个模态中所有 $K(K-1)$ 个有序模态对分别计算对比损失并取平均：

$$
\mathcal{L} = \frac{1}{K(K-1)} \sum_{i=1}^{K} \sum_{\substack{j=1 \\ j \neq i}}^{K} \mathcal{L}_{i,j}
$$

其中 $K = 4$（地面图像、航拍图像、文本、GPS），$\mathcal{L}_{i,j}$ 表示以模态 $i$ 为查询、模态 $j$ 为键的标准 InfoNCE 损失。对于一个小批量中的 $N$ 个样本，$\mathcal{L}_{i,j}$ 的具体形式为：

$$
\mathcal{L}_{i,j} = -\frac{1}{N} \sum_{n=1}^{N} \log \frac{\exp(\text{sim}(z_i^n, z_j^n) / \tau)}{\sum_{m=1}^{N} \exp(\text{sim}(z_i^n, z_j^m) / \tau)}
$$

其中 $z_i^n$ 表示第 $n$ 个样本在模态 $i$ 下的投影嵌入向量，$\text{sim}(\cdot, \cdot)$ 为余弦相似度，$\tau$ 为温度系数。该损失函数的核心作用是：对每个样本，将其在不同模态下的表示（正对）拉近，同时将该样本与批次中其他样本的表示（负对）推远。

与标准 CLIP 仅优化图像-文本对的 InfoNCE 损失不同，MMCLIP 的成对损失在所有模态组合上同时施加对比约束。这意味着模型必须学习：
- 地面图像与航拍图像之间的跨视角对应（几何对齐）
- 图像与文本之间的语义对应（语义对齐）
- GPS 坐标与图像/文本之间的地理空间对应（空间对齐）

这种全配对训练策略是 MMCLIP 在跨视角检索和地理定位任务上显著超越仅使用图像-文本预训练的基础模型（如 SigLIP2）的关键机制。消融实验（Table 6）也证实：去除 GPS 模态或文本模态会显著降低定位和检索性能，验证了多模态联合训练的必要性。

### 训练与推理流程

训练时，四种模态的嵌入通过各自的编码器和投影头提取后，直接输入成对对比损失进行端到端优化（仅投影头和 GPS 编码器可训练）。推理时，模型根据任务需求选择相应的模态编码器提取特征，通过余弦相似度在嵌入空间中进行最近邻检索，或通过 GPS 编码器直接回归坐标。对于 Ground-to-Sat-to-GPS 定位任务，模型先通过地面图像检索最相似的卫星图像，再利用检索到的卫星图像的 GPS 坐标进行定位——这种级联策略有效结合了跨视角检索的判别能力和坐标编码器的空间精度。



## 实验与关键发现

### 核心实验设计

本文在 **MMLANDMARKS** 数据集上评估基线模型 **MMCLIP** 在三个核心地理空间理解任务上的表现：跨视角检索、地理定位和文本到任意模态检索。所有实验均采用冻结的 CLIP ViT 编码器提取地面和航拍图像特征，冻结的 CLIP 文本编码器处理 Wikipedia 描述，GPS 坐标则通过 **GeoCLIP**（Vivanco Cepeda et al., NeurIPS 2023）的位置编码器映射为连续嵌入。每个编码器后接一个由两层可训练线性层与 ReLU 激活组成的投影头，将所有模态映射到 512 维公共空间。训练使用成对 InfoNCE 损失，对所有 $K(K-1)$ 个模态对计算对比损失并取平均：

$$\mathcal{L} = \frac{1}{K(K-1)} \sum_{i=1}^{K} \sum_{\substack{j=1 \\ j \neq i}}^{K} \mathcal{L}_{i,j}$$

地理定位评估遵循先前工作，采用 Haversine 距离计算不同公里阈值下的距离百分比（Distance(% @ km)）。

### 跨视角检索：MMCLIP 大幅超越现有基础模型

Table 2 展示了地面图像与卫星图像双向检索的完整对比。在 **Satellite→Ground** 方向（查询集 1000 张，索引集 733k 张），MMCLIP 的 R@1 达到 **18.8%**，而最佳多模态基础模型 **SigLIP2**（Tschannen et al., arXiv 2025）仅为 4.1%，性能提升 **+14.7 个百分点**。专门跨视角模型 **Sample4Geo-UNI** 的 R@1 为 7.3%，同样远低于 MMCLIP。在 **Ground→Satellite** 方向（查询集 18,688 张，索引集 101k 张），MMCLIP 的 R@1 为 **20.5%**，SigLIP2 为 14.6%，提升 5.9 个百分点。

![[assets/figures/papers/paper_list_l822_https_openaccess_thecvf_com_content_CVPR2026_html_Kristoffersen_MMLandma/figures/004_Table_2.jpg]]
*Table 2: Cross-view ground and satellite retrieval. Comparison of median rank (medR, lower is better), mean Average Precision at 1000 (mAP@1k, higher is better), and recall at K (R@K, higher is better) between off-the-shelf cross-view Ground-to-Satellite retrieval models and multimodal foundational models on MMLANDMARKS. Median rank is the median position where the first correct match is retrieved. The query and index sizes for satellite to ground are 1000 and 733k, respectively, and for ground to satellite are 18,688 and 101k*

值得注意的是，纯视觉自监督模型 **DINOv3**（Simeoni et al., arXiv 2025）在两个方向上的 R@1 分别仅为 0.2% 和 0.8%，表明缺乏多模态对齐训练的视觉特征无法弥合地面与卫星视角之间的巨大域间隙。MMCLIP 的中位排名（medR）在 Satellite→Ground 上为 23，远优于 SigLIP2 的 111，进一步验证了实例级多模态对齐的有效性。

### 地理定位：卫星索引策略显著提升精细定位

Table 3 和 Table 4 分别展示了地面图像定位和卫星图像定位的结果。在地面图像定位任务中，MMCLIP 采用 **Ground-to-Sat-to-GPS** 策略——先通过跨视角检索找到最匹配的卫星图像，再使用该卫星图像的 GPS 坐标作为预测位置。在 1 km 街道级别，MMCLIP 达到 **18.41%**，而直接预测 GPS 的 **GeoCLIP** 仅为 5.68%，**OAI-CLIP**（Radford et al., ICML 2021）为 8.04%。在洲级别（2500 km），MMCLIP 达到 **91.83%**，基本实现了大范围可靠定位。

![[assets/figures/papers/paper_list_l822_https_openaccess_thecvf_com_content_CVPR2026_html_Kristoffersen_MMLandma/figures/007_Table_3.jpg]]
*Table 3: Ground-to-GPS geolocalization. Performance on the MMLANDMARKS query set (18,688 ground images). Ground-to-Sat-to-GPS is also done to evaluate cross-view retrieval models*

![[assets/figures/papers/paper_list_l822_https_openaccess_thecvf_com_content_CVPR2026_html_Kristoffersen_MMLandma/figures/006_Table_4.jpg]]
*Table 4: Satellite-to-GPS geolocalization. Model performance on the MMLANDMARKS query set (1000 satellite images)*

在卫星图像定位任务（Table 4）中，MMCLIP 在 1 km 级别达到 **36.9%**，远超 GeoCLIP 的 12.3%（提升 **+24.6 个百分点**）和 OAI-CLIP 的 10.4%。在洲级别，MMCLIP 达到 **99.7%**，几乎完美。这一结果的关键在于：MMCLIP 在训练中同时学习了航拍图像与 GPS 坐标的直接对齐，而 GeoCLIP 仅在地面图像上训练，缺乏对卫星视角的位置理解。

### 文本到任意模态检索

Table 5 展示了文本到卫星图像和文本到 GPS 的检索结果。MMCLIP 在 Text→Satellite 上 R@1 为 **13.4%**，略优于 OAI-CLIP 的 11.1%。在 Text→GPS 定位中，MMCLIP 在 1 km 级别达到 **9.2%**，OAI-CLIP 为 7.6%。虽然文本模态的提升幅度不如视觉模态显著，但 MMCLIP 在所有指标上均优于仅使用图像-文本对训练的 CLIP 模型，表明多模态联合训练对文本理解也有正向迁移。

![[assets/figures/papers/paper_list_l822_https_openaccess_thecvf_com_content_CVPR2026_html_Kristoffersen_MMLandma/figures/008_Table_5.jpg]]
*Table 5: Text-to-Any retrieval. Model performance on the MM-LANDMARKS query set (1000 first sentences) for Text-to-Satellite and Text-to-GPS retrieval*

### 消融实验：数据质量是关键杠杆

Table 6 的消融实验揭示了影响模型性能的几个关键因素：

![[assets/figures/papers/paper_list_l822_https_openaccess_thecvf_com_content_CVPR2026_html_Kristoffersen_MMLandma/figures/009_Table_6.jpg]]
*Table 6: Ablation studies. Performance for different models trained in various configurations: training objectives, modalities included, text sampling (F: first sentence or R: random sentence), satellite sampling (R: random or L: last), and whether indoor ground images are included during training (Subset). The gray row is our final baseline model, used in all tables*

1. **卫星图像时间采样**：使用最新卫星图像（L: last）相比随机时间采样（R: random），在 Satellite→Ground 检索的 R@1 上从 15.1% 提升至 **18.8%**，在 Ground→Satellite 上从 17.3% 提升至 20.5%。这表明时间一致性对跨视角对齐至关重要——地面图像通常拍摄时间较新，与最新卫星图像在季节、光照和地物状态上更匹配。

2. **室内图像过滤**：仅使用室外地面图像子集（Subset）训练，相比包含约 17% 室内图像的全集，在 Satellite→Ground 上 R@1 从 16.8% 提升至 18.8%。室内图像缺乏空间对应关系，引入噪声干扰了跨视角对齐学习。

3. **文本采样策略**：使用 Wikipedia 文本的第一句话（F: first sentence）相比随机采样句子（R: random），在 Text→Satellite 检索上 R@1 从 10.1% 提升至 13.4%。第一句话通常包含地标的核心描述信息，随机采样可能引入无关细节。

4. **模态组合的必要性**：去除 GPS 模态后，Ground-to-Sat-to-GPS 定位在 1 km 级别从 18.41% 骤降至 3.04%；去除文本模态后，Text→Satellite 检索完全失效（R@1 为 0）。这验证了四模态联合训练对各项任务的互补性。

### 失败模式与局限性

尽管 MMCLIP 在多项任务上表现优异，但分析揭示了以下失败模式：

- **精细定位瓶颈**：在 Ground-to-Sat-to-GPS 任务中，1 km 级别仅 18.41%，意味着超过 80% 的查询无法精确定位到街道级别。跨视角域间隙依然存在——地面图像视角多变（仰角、遮挡、光照），航拍图像仅覆盖特定年份的俯视视角，两者在几何和外观上的差异未通过高级几何变换弥合。

- **室内图像干扰**：约 17% 的地面图像为室内照片，虽经 VLM 过滤但仍有误分类残留，这些图像与卫星视角无空间对应关系，在训练中引入不可消除的噪声。

- **地理分布偏差**：数据集仅覆盖美国本土，地标分布严重偏向加州和东北部等大城市区域，农村及偏远地区数据稀疏。模型在人口稀少区域的定位性能可能显著下降，但原文未提供按地理区域分层的性能分析，此点需手动验证。

- **冻结编码器的限制**：MMCLIP 使用冻结的 CLIP 编码器，仅训练投影头。CLIP 编码器主要在海量网络图像上预训练，可能无法充分适应航拍图像的独特纹理和尺度特征，性能提升空间受限于基础模型的表征能力。

### 开放问题

基于上述分析，以下方向值得进一步探索：

- 如何利用数据集中的时间序列航拍图像设计变化检测任务，显式建模地标的时态演化？
- 能否引入可训练的航拍图像编码器或几何变换模块，进一步缩小跨视角域间隙？
- 面向全球扩展时，如何处理不同国家图像质量、地标密度和文化类型的严重不平衡？
- 在资源受限的真实部署场景中，如何压缩多模态模型同时保持检索精度？

### 补充图表

![[assets/figures/papers/paper_list_l822_https_openaccess_thecvf_com_content_CVPR2026_html_Kristoffersen_MMLandma/figures/002_Table_1.jpg]]
*Table 1: Dataset comparison. Modality abbreviations: S - Satellite, G - Ground, T - Text, C - Coordinates, D - Drone. In the Scale column, the number in parentheses indicates the number of cities*

![[assets/figures/papers/paper_list_l822_https_openaccess_thecvf_com_content_CVPR2026_html_Kristoffersen_MMLandma/figures/005_Figure_3.jpg]]
*Figure 3: Text-to-GPS (top 1000), Text-to-Ground and Text-to-Satellite retrieval from the index set with the baseline model. The model accurately locates regions and images that are semantically relevant to the prompt, illustrating strong feature alignment across modalities*



## 定位与知识库关联

### 1. 问题定位与基线谱系

MMLANDMARKS 的核心动机在于揭示现有地理空间理解基准的结构性缺陷：**缺乏跨视角、实例级的模态对应**。传统数据集或专注于单一视角（如仅地面图像的地理定位），或仅提供粗粒度的图像-坐标配对，导致模型难以习得“同一地标”在不同模态下的语义一致性。该工作将自身定位为填补这一空白的**基准构建与基线验证**，而非提出全新的模型架构。

在基线选择上，论文构建了一个清晰的能力谱系，覆盖三类代表性方法：

- **通用多模态基础模型**：以 **OAI-CLIP** (Radford et al., ICML 2021) 和 **SigLIP2** (Tschannen et al., arXiv 2025) 为代表。这类模型通过大规模图像-文本对比预训练获得了强大的零样本跨模态检索能力，但缺乏对地理空间模态（特别是航拍视角和GPS坐标）的专门适配。在 MMLANDMARKS 的跨视角检索任务中，SigLIP2 ViT-L/512 在 Satellite→Ground 方向上的 R@1 仅为 4.1%，暴露了通用模型在细粒度地理空间对齐上的根本性不足。

- **专用地理空间模型**：包括 **GeoCLIP** (Vivanco Cepeda et al., NeurIPS 2023) 和 **Sample4Geo-UNI**。GeoCLIP 将 CLIP 图像编码器与 GPS 位置编码器结合，专门针对地面图像定位设计；Sample4Geo-UNI 则面向地面-卫星跨视角实例匹配。这些模型在特定任务上表现优于通用模型，但其训练范式和模态覆盖范围受限——例如 GeoCLIP 无法直接处理卫星图像或文本查询。

- **纯视觉自监督模型**：**DINOv2** (Oquab et al., arXiv 2023) 和 **DINOv3** (Simeoni et al., arXiv 2025) 作为无多模态训练的视觉特征提取器被纳入比较，用于评估跨模态对齐是否确实需要显式的多模态训练信号。实验结果表明，缺乏文本或坐标监督的纯视觉特征在跨模态检索中表现显著逊色，验证了多模态联合训练的必要性。

### 2. 方法变体与关键设计选择

MMCLIP 作为基线模型，其设计哲学是**最小化架构创新，最大化数据驱动收益**。方法的核心变化体现在三个维度：

**数据层面**：从“网络图像-文本对”到“实例级四模态对应”。传统 CLIP 风格的训练数据仅保证图像与文本的弱相关，而 MMLANDMARKS 确保每一条数据中的地面图像、航拍图像、文本描述和 GPS 坐标均指向同一物理地标实例。这一约束是后续所有性能增益的根本来源。

**模态组合**：从双模态到四模态联合训练。MMCLIP 对四种模态的所有 $K(K-1)$ 个配对计算 InfoNCE 损失并取平均：

$$\mathcal { L } = \frac { 1 } { K ( K - 1 ) } \sum _ { i = 1 } ^ { K } \sum _ { \substack { j = 1 \\ j \neq i } } ^ { K } \mathcal { L } _ { i , j }$$

这种成对对比损失的设计使得模型能够同时学习地面-航拍、图像-文本、图像-坐标、文本-坐标等多重对齐关系，从而在单一嵌入空间中实现跨模态的语义统一。

**编码器选择**：冻结的 CLIP ViT 图像/文本编码器 + 可训练的 GeoCLIP 风格 GPS 编码器 + 各模态独立的投影头。这一选择体现了务实的设计思路——利用预训练模型的强大表示能力，仅通过投影头适配到公共空间，避免了全参数微调带来的计算开销和过拟合风险。但这也构成了方法的适用边界：冻结的 CLIP 编码器可能无法充分适应航拍图像特有的俯视几何特征和光谱特性。

### 3. 适用边界与已知局限

**地理覆盖偏差**：数据集仅覆盖美国本土，且地标分布严重偏向大城市及游客聚集区（如加利福尼亚州和美国东北部）。模型在农村、偏远地区或美国境外场景下的性能未经验证，跨地理域的泛化能力存疑。这一偏差在训练数据层面即已固化，模型本身不具备纠正机制。

**室内图像噪声**：地面图像中约 17% 为室内照片，虽经 VLM 过滤，但仍有少量误分类残留。室内图像缺乏与航拍视角的空间对应关系，可能在学习过程中引入混淆信号，削弱地面-航拍对齐的质量。消融实验（Table 6）证实，仅使用室外图像子集训练可显著提升各项任务性能。

**跨视角域间隙**：地面图像视角多变（仰角、距离、遮挡各异），航拍图像仅覆盖特定年份的单一俯视视角，两者之间的几何和外观差异仍然是跨视角检索的主要瓶颈。MMCLIP 未采用任何显式的几何变换或视角归一化技术，完全依赖数据驱动的特征对齐来解决这一域间隙。

**时间变化信息未利用**：数据集天然包含同一地标在不同年份的航拍图像，但 MMCLIP 的训练过程未显式建模时间维度。消融实验表明，简单地选择最新卫星图像（L: last）而非随机时间采样即可带来性能提升，这暗示时间一致性是重要的学习信号，但其潜力远未被充分挖掘。

**模型容量限制**：基线模型采用冻结的 ViT-L 编码器，结构简单。更大规模的基础模型（如 ViT-G）或多模态 LLM 可能带来显著的性能突破，但当前工作未对此进行探索。

### 4. 开放性研究问题

基于上述局限，论文及其构建的基准开启了若干关键研究方向：

- **全球扩展与域适应**：如何将 MMLANDMARKS 的训练框架扩展到全球范围，并处理不同国家间图像质量、地标密度和类型分布的不平衡？这需要解决数据获取许可、模态对齐质量控制和地理域适应等多重挑战。

- **时空联合建模**：数据集中的时间序列航拍图像为自监督或弱监督的变化检测任务提供了天然素材。能否设计预训练任务，使模型不仅理解“这是什么地标”，还能感知“地标随时间如何变化”？

- **精细定位瓶颈突破**：尽管 MMCLIP 在 1km 精度上大幅超越基线（Satellite-to-GPS 达 36.9%），但更精细的定位（如 100m 级别）仍有巨大提升空间。引入更大规模编码器、更精细的几何推理模块或层次化检索策略可能是突破方向。

- **数据可持续扩展**：在确保图像许可证持续开放的前提下，如何系统性地扩展数据集的地理覆盖和模态多样性（如增加夜间图像、红外影像、街景视频等），同时维持实例级对齐的质量标准？

- **边缘部署优化**：面向真实地理空间应用，如何在资源受限设备上降低跨模态检索的推理延迟，同时保持检索精度？模型蒸馏、特征量化或异步索引策略值得探索。



## 原文 PDF

![[paperPDFs/CVPR_2026/MMLandmarks_a_Cross_View_Instance_Level_Benchmark_for_Geo_Spatial_Understanding.pdf]]
