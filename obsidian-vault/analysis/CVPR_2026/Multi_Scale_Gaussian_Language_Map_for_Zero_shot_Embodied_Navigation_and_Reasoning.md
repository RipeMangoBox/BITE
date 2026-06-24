---
title: Multi-Scale Gaussian-Language Map for Zero-shot Embodied Navigation and Reasoning
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/Multi_Scale_Gaussian_Language_Map_for_Zero_shot_Embodied_Navigation_and_Reasoning.pdf
project_link: null
code_link: "https://github.com/sxzhang/GLMap"
aliases:
- GMSGLM
- MSGLMZSENR
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
core_operator: 为每个语义单元同时存储自然语言描述和 3D 高斯渲染图像，形成双模态接口，使大型模型可以直接消费文本和视觉信息，无需额外对齐训练。
primary_logic: 通过 2D 索引网格结合实例/区域多尺度语义单元，并利用 3D 高斯的解析估计与合并，可以增量式地构建零样本兼容的语义地图，高效支撑物体导航、实例导航和场景问答。
claims:
- 消融实验（Table 1）表明，引入多尺度语义单元（实例单元和区域单元）能够逐步提升物体导航成功率与路径效率。
- 将 GLMap 集成到现有的 LLM、VLM 和 MLLM 零样本方法中，在所有任务上均一致提升性能（Table 2），证明了其通用性和零样本兼容能力。
- HM3D ObjectNav 上 SR(%) = 62.7 (ApexNAV+GLMap)
- HM3D ObjectNav 上 SPL(%) = 33.7
---

# Multi-Scale Gaussian-Language Map for Zero-shot Embodied Navigation and Reasoning

> [!tip] 核心洞察
> 通过 2D 索引网格结合实例/区域多尺度语义单元，并利用 3D 高斯的解析估计与合并，可以增量式地构建零样本兼容的语义地图，高效支撑物体导航、实例导航和场景问答。

| 字段 | 内容 |
|------|------|
| 中文题名 | 面向零样本具身导航与推理的多尺度高斯-语言地图 |
| 英文题名 | Multi-Scale Gaussian-Language Map for Zero-shot Embodied Navigation and Reasoning |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2605.01736) · [Code](https://github.com/sxzhang/GLMap) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction |
| Method | GLMap (Multi-Scale Gaussian-Language Map) |
| Dataset | HM3D ObjectNav, MP3D ObjectNav, HM3D InstNav, SQA3D SQA |

> [!tip] 效果简介
> - HM3D ObjectNav 上，SR(%) 62.7 (ApexNAV+GLMap) vs N/A (N/A)；SPL(%) 33.7 vs N/A (N/A)。
> - MP3D ObjectNav 上，SR(%) 42.5 vs N/A (N/A)。
> - HM3D InstNav 上，SR(%) 22.5 vs N/A (N/A)。

## 概述

具身机器人要在真实室内环境中执行物体导航、实例导航和场景问答等复杂任务，需要构建能够同时支撑空间定位与语义理解的场景地图。现有语义地图方法在几何精确性、多尺度语义表示和大型模型接口之间存在根本性权衡：栅格或点云地图语义单一，缺乏实例边界；拓扑地图缺少精确定位能力；基于隐式特征向量的地图则需要额外的特征投影训练才能与 LLM/VLM/MLLM 对齐，无法实现真正的零样本使用。

**GLMap（多尺度高斯-语言地图）** 针对上述瓶颈提出了一种新的地图表示范式。其核心洞察是：为每个语义单元同时存储自然语言文本描述和 3D 高斯渲染图像，形成双模态接口，使大型预训练模型可以直接消费文本和视觉信息，无需任何额外对齐训练。在结构上，GLMap 通过 2D 索引网格实现度量空间中的精确定位，同时引入实例级和区域级多尺度语义单元，分别捕获物体、属性等细粒度概念和功能区、场景等粗粒度上下文。3D 高斯参数通过体素化点云的解析估计获得，并基于曲率感知的合并策略减少冗余，实现增量式地图更新。

实验表明，GLMap 在 HM3D 和 MP3D 上的零样本物体导航任务中取得 62.7% 和 42.5% 的成功率，在实例导航和场景问答任务上也表现出色。消融实验（Table 1）证实，逐步引入实例单元和区域单元能够一致提升导航成功率与路径效率；将 GLMap 集成到基于 LLM 的 **ESC**（Zhou et al., ICML 2023）、基于 VLM 的 **VLFM**（Yokoyama et al., ICRA 2024）和基于 MLLM 的 **GPT4Scene**（Qi et al., arXiv 2025）等零样本方法中，所有任务上均获得一致的性能提升（Table 2），验证了其作为通用零样本语义地图的兼容能力。

## 背景与动机

### 具身导航与语义地图的演进

具身导航要求智能体在未知环境中依据视觉观测进行自主探索与目标定位。近年来，随着大语言模型（LLM）、视觉-语言模型（VLM）和多模态大语言模型（MLLM）的兴起，零样本导航方法逐渐成为主流——它们无需针对特定环境进行微调，仅依赖预训练模型的常识推理能力即可完成物体导航（ObjectNav）、实例导航（InstNav）和场景问答（SQA）等任务。

然而，这些方法的性能高度依赖于底层语义地图的质量。语义地图作为智能体对环境的内部表征，需要同时满足三个核心需求：**精确的几何定位**、**丰富的多尺度语义**以及**与大型模型的无缝接口**。

### 现有语义地图的结构性缺陷

当前主流的语义地图结构可分为三类，各自存在难以调和的权衡（图1）：

**栅格地图（Grid Map）** 将空间离散化为二维网格，每个网格存储语义标签或隐式特征向量（如CLIP嵌入）。其优势在于空间索引清晰、定位精确，但语义粒度单一——只能表达“此处是什么类别”，缺乏对物体实例边界和区域功能的理解。例如，一张餐桌和旁边的椅子在栅格地图中可能被标记为同一类别的散点，无法区分个体实例，更无法表达“餐厅”这一区域概念。

**拓扑地图（Topological Map）** 以节点和边组织空间关系，天然适合LLM进行图推理。但其节点位置通常是粗略的，缺乏精确的度量坐标，导致导航时无法进行细粒度的路径规划。当目标物体被遮挡或位于视野之外时，拓扑地图难以提供有效的空间先验。

**密集几何地图（Dense Geometric Map）** 通过神经辐射场（NeRF）或3D高斯抛雪球（3DGS）重建场景几何，能够渲染高质量的视角图像。但这类地图本质上是“几何的”，语义信息需要额外注入，且与LLM/VLM的接口需要训练专门的特征投影模块——这违背了零样本使用的初衷。

### 核心瓶颈：大型模型接口的断裂

上述方法的共同症结在于：**语义地图的输出形式与大型模型可消费的输入之间存在模态鸿沟**。栅格地图和拓扑地图产生的隐式特征向量（如CLIP embeddings）无法直接被LLM理解；密集几何地图虽然能渲染图像，但其语义标注仍依赖额外的对齐训练。当面对新的任务或环境时，这些方法要么需要重新训练投影层，要么只能退化为简单的文本标签匹配，丧失了零样本泛化能力。

### GLMap的动机与设计直觉

GLMap的核心洞察是：**为每个语义单元同时存储自然语言描述和3D高斯渲染图像，形成双模态接口**。自然语言描述可直接作为LLM的提示词上下文，3D高斯渲染图像可直接输入VLM/MLLM进行视觉推理——两者均无需任何额外的对齐训练。这使得GLMap天然具备零样本兼容性，能够即插即用地集成到现有的LLM、VLM和MLLM导航框架中。

在空间组织上，GLMap引入**2D索引网格**实现精确定位，并在此基础上叠加**实例单元**（instance unit）和**区域单元**（region unit）两个多尺度语义层级。实例单元对应单个物体（如“一张木质餐桌”），存储其文本描述和3D高斯参数集；区域单元对应功能空间（如“厨房”），聚合其包含的实例集合和整体描述。这种层级结构使得地图既能回答“某个物体在哪里”，也能回答“某个区域包含什么”，为导航和问答提供了丰富的空间语义先验。

## 核心创新

GLMap 的核心创新在于重新定义了语义地图的表示范式，使其原生兼容大语言模型（LLM）、视觉-语言模型（VLM）和多模态大模型（MLLM），从而在无需任何额外对齐训练的条件下，统一支撑物体导航、实例导航和场景问答等零样本具身任务。

### 关键瓶颈突破

现有语义地图方法在几何精确性、多尺度语义和大型模型接口之间存在根本性权衡：栅格或点云地图仅能提供单一类别标签，缺乏实例边界和区域语义；拓扑地图虽能表达空间关系，却丢失了精确定位能力；基于隐式特征（如CLIP embeddings）的地图则需要额外的特征投影训练才能与LLM/VLM/MLLM对齐，无法实现真正的零样本使用。GLMap 针对这一瓶颈，提出了三条相互耦合的机制性创新。

### 创新一：双模态语义单元表示

GLMap 将每个语义单元同时存储为**自然语言文本描述**和**3D高斯参数集**（包含颜色、位置、协方差等）。这一设计的核心洞察在于：文本描述可直接被LLM消费用于语义推理，3D高斯渲染图像可直接被VLM/MLLM消费用于视觉推理，从而形成零样本兼容的双模态接口。相比基线方法中仅使用单一类别标签或隐式特征向量（需额外训练投影模块），GLMap 的显式双模态表示消除了模型对齐的训练开销，使大型模型能够“开箱即用”地理解地图内容。

### 创新二：多尺度语义地图结构

GLMap 将地图结构从单一尺度扩展为三层体系：**2D索引网格**、**实例单元**和**区域单元**。2D索引网格提供度量空间中的精确定位；实例单元捕获物体级别的概念（如“餐桌”“红色沙发”）及其几何表示；区域单元表达功能区域或场景级别的概念（如“厨房”“办公区”），并维护其包含的实例集合。消融实验（Table 1）表明，逐步引入实例单元和区域单元能够持续提升物体导航的成功率（SR）和路径效率（SPL），验证了多尺度语义对下游任务的关键支撑作用。

### 创新三：解析式高斯估计与曲率感知合并

GLMap 提出了一种**解析式高斯估计器**（Gaussian Estimator），直接从密集点云中推断3D高斯参数（均值、协方差、颜色），避免了基于优化的迭代拟合过程。具体而言，对每个体素邻域 $\tilde{\mathcal{P}}_{\mathbf{v}}$，解析计算均值和协方差矩阵：

$$\boldsymbol{\mu}_{\mathbf{v}} = \frac{1}{|\tilde{\mathcal{P}}_{\mathbf{v}}|} \sum_{\mathbf{p}_i \in \tilde{\mathcal{P}}_{\mathbf{v}}} \mathbf{p}_i, \quad \Sigma_{\mathbf{v}} = \frac{1}{|\tilde{\mathcal{P}}_{\mathbf{v}}|} \sum_{\mathbf{p}_i \in \tilde{\mathcal{P}}_{\mathbf{v}}} (\mathbf{p}_i - \boldsymbol{\mu}_{\mathbf{v}})(\mathbf{p}_i - \boldsymbol{\mu}_{\mathbf{v}})^{\top} + \epsilon I$$

在此基础上，GLMap 引入**曲率感知的高斯合并条件**：

$$G_{\mathrm{new}} = G_i \oplus G_j, \quad \mathrm{if } D(G_i, G_j) < (1 + \tau (\kappa(\Sigma_i) + \kappa(\Sigma_j)))$$

其中 $D(G_i, G_j)$ 综合衡量位置、协方差和颜色的距离，$\kappa(\Sigma)$ 为条件数（最小特征值与迹之比）。这一设计在平坦区域（低曲率）采用更宽松的合并阈值以减少冗余高斯，在几何细节区域（高曲率）则保留更多高斯以维持精度，实现了表示效率与几何保真度的自适应平衡。

### 零样本通用性验证

GLMap 的零样本兼容能力在跨模型集成实验（Table 2）中得到系统性验证：将 GLMap 分别集成到基于 LLM 的 **ESC**（Zhou et al., ICML 2023）、基于 VLM 的 **VLFM**（Yokoyama et al., ICRA 2024）和基于 MLLM 的 **GPT4Scene**（Qi et al., arXiv 2025）中，在 ObjectNav 和 SQA 任务上均取得一致的性能提升，且无需任何微调或特征对齐训练。这一结果证明 GLMap 的显式文本-视觉双模态表示具有跨模型架构的泛化能力，是真正意义上的零样本语义地图基础设施。

## 整体框架

GLMap 的构建与使用遵循一个从感知到结构化地图、再到任务推理的闭环流程。整个系统以**增量式建图**为核心，从第一人称 RGB-D 视频流出发，逐步构建并维护一个多尺度高斯-语言地图，最终为下游的零样本导航与场景问答任务提供可直接消费的语义接口。

### 输入与输出

**输入**：连续的自我中心 RGB-D 帧序列，以及每帧对应的相机内参和位姿（在 SQA 任务中由模拟器提供）。

**输出**：一个结构化地图 $\mathcal{M} = \{ m, \mathcal{S}_o, \mathcal{S}_r \}$，其中：
- $m$ 是 2D 空间索引网格，用于在度量空间中精确定位语义单元；
- $\mathcal{S}_o$ 是实例级语义单元集合，每个实例单元 $o = (\mathcal{G}, T_o)$ 同时存储一组 3D 高斯参数 $\mathcal{G}$ 和自然语言文本描述 $T_o$；
- $\mathcal{S}_r$ 是区域级语义单元集合，每个区域单元 $r = (\mathscr{T}_r, T_r)$ 包含该区域内的实例集合 $\mathscr{T}_r$ 和区域文本描述 $T_r$。

### 核心 Pipeline 模块

GLMap 的增量更新流程（Figure 2）由以下模块串联而成：

![[assets/figures/papers/paper_list_l2642_https_arxiv_org_abs_2605_01736/figures/002_Figure_2.jpg]]
*Figure 2: Incremental update of GLMap. The semantics of RGB–D images are first structured into instances and regions. Instance Gaussians are estimated and matched with existing GLMap instances based on textual and Gaussian similarities, and merged accordingly. The matched results determine the global IDs of instances, which are subsequently used for region similarity computation and fusion*

**1. MLLM 语义解析模块**
对每一帧 RGB 图像，使用开源多模态大模型 **Gemma3-27B** 生成开放式文本描述，同时捕获实例级概念（如物体、属性）和区域级概念（如功能区、场景类型）。这一步将原始像素转化为结构化的语义原语。

**2. 实例分割与点云生成模块**
生成的文本描述通过 **GroundingDINO** 进行开放词汇区域定位，并由 **MobileSAM** 进行掩膜精化。结合深度图和相机位姿，将掩膜区域反投影到 3D 空间，得到每个实例的稠密点云 $\mathcal{P}$。

**3. 高斯估计器 (Gaussian Estimator)**
从每个实例的点云中解析计算 3D 高斯参数。具体而言，对点云进行体素化，在每个体素 $\mathbf{v}$ 的 Chebyshev 邻域 $\tilde{\mathcal{P}}_{\mathbf{v}}$ 内解析估计高斯均值 $\boldsymbol{\mu}_{\mathbf{v}}$ 和协方差 $\Sigma_{\mathbf{v}}$（Eq. 3），外观颜色取邻域内点的平均颜色。这一过程完全可微但无需训练：
$$\mathcal{G} = f_{GE}(\mathcal{P})$$

随后，基于曲率感知的合并条件（Eq. 5）对体素高斯进行合并：当两个高斯的综合距离 $D(G_i, G_j)$ 小于 $(1 + \tau (\kappa(\Sigma_i) + \kappa(\Sigma_j)))$ 时合并，其中 $\kappa(\cdot)$ 为最小特征值与迹之比，使平滑区域的高斯更易合并，而几何细节丰富区域的高斯得以保留。

**4. 实例匹配与合并模块**
新观测到的实例高斯与 GLMap 中已有实例进行双向匹配。匹配依据包括文本嵌入的余弦相似度和高斯几何相似度（Eq. 4）。匹配成功后，合并两者的高斯集合与文本描述（Eq. 6）：
$$\mathcal{G}_j \gets \mathcal{G}_j \cup \mathcal{G}_i, \quad T_{o_j} \gets [T_{o_j}; T_{o_i}]$$
未匹配的新实例则作为新实例单元加入 $\mathcal{S}_o$。

**5. 区域匹配与合并模块**
区域匹配需同时满足语义一致性（$\cos(\phi(T_{r_i}), \phi(T_{r_j})) > \tau_s$）和实例集一致性（至少共享一个实例）。匹配后合并实例集和文本描述（Eq. 7）：
$$\mathscr{T}_{r_j} \gets \mathscr{T}_{r_j} \cup \mathscr{T}_{r_i}, \quad T_{r_j} \gets [T_{r_j}; T_{r_i}]$$

**6. 2D 空间索引更新模块**
根据实例和区域的 3D 空间位置，更新 2D 索引网格 $m$，使得后续可以通过空间查询快速检索任意位置的语义单元。

### 任务推理接口

建图完成后，GLMap 通过一个统一的价值地图机制支撑多种下游任务。对于目标导航（ObjectNav），系统将目标文本与所有语义单元的描述进行相似度计算，得到每个单元的相关性分数 $s_u$，再通过核密度估计将离散的语义单元分数扩散为连续的空间价值分布 $H(l)$（Section 3.2 公式），从而指导路径点选择（Figure 4）。对于场景问答（SQA），GLMap 直接将实例和区域的文本描述与 3D 高斯渲染图像作为显式参考输入 MLLM，无需隐式特征投影即可进行零样本推理。

### 关键设计决策

整个 pipeline 的核心设计在于**双模态语义接口**：每个语义单元同时提供自然语言描述和可渲染的 3D 高斯表示。这使得 LLM、VLM 和 MLLM 可以直接消费文本和视觉信息，无需任何额外的特征对齐训练，从根本上实现了零样本兼容性。消融实验（Table 1）证实，逐步引入实例单元和区域单元能够持续提升 ObjectNav 的成功率与路径效率，验证了多尺度语义结构的必要性。

### 补充图表

![[assets/figures/papers/paper_list_l2642_https_arxiv_org_abs_2605_01736/figures/001_Figure_1.jpg]]
*Figure 1: Comparison of semantic map structure: (a) Grid map, (b) Topological map, (c) Dense geometric map, and (d) Our GLMap. GLMap integrates a 2D indexing grid with multi-scale semantics through instance units and region units, each providing explicit text and visual representations, enabling zero-shot compatibility with current large pretrained models*

## 核心模块与公式推导

GLMap 的构建围绕一个核心设计：将第一人称 RGB‑D 视频流增量式地组织为 **多尺度语义单元**，每个单元同时携带自然语言描述和显式 3D 高斯表示，从而为大型预训练模型提供零样本可消费的双模态接口。其关键模块可归纳为以下四个环节。

### 语义解析与实例分割

系统首先使用开源 MLLM **Gemma3‑27B** 对单帧 RGB 图像进行开放式语义描述，生成实例级（如物体、属性）和区域级（如功能区、场景）的文本标签。随后，**GroundingDINO** 与 **MobileSAM** 被串联用于将这些文本标签落地为像素级掩膜，结合深度图与相机位姿通过反投影获得每个实例的稠密点云。这一步骤将“语言描述”与“几何实体”建立起一一对应关系，为后续高斯建模提供基础。

### 高斯估计器（Gaussian Estimator）

从点云直接解析 3D 高斯参数是 GLMap 避免迭代优化、实现实时增量建图的关键。给定一个实例的点云 $\mathcal{P}$，高斯估计器 $f_{GE}$ 将其映射为一组 3D 高斯原语：

$$
\mathcal{G} = f_{GE}(\mathcal{P})
$$

具体而言，首先对点云进行体素化，对每个体素 $\mathbf{v}$ 定义其 Chebyshev 邻域内的点集：

$$
\tilde{\mathcal{P}}_{\mathbf{v}} = \bigcup_{\tilde{\mathbf{v}} \in \mathcal{N}(\mathbf{v})} \mathcal{N}(\mathbf{v}) = \{ \tilde{\mathbf{v}} \mid \| \tilde{\mathbf{v}} - \mathbf{v} \|_{\infty} \leq 1 \}
$$

利用该邻域点集，解析计算每个体素对应高斯的均值 $\boldsymbol{\mu}_{\mathbf{v}}$ 和协方差矩阵 $\Sigma_{\mathbf{v}}$：

$$
\boldsymbol{\mu}_{\mathbf{v}} = \frac{1}{|\tilde{\mathcal{P}}_{\mathbf{v}}|} \sum_{\mathbf{p}_i \in \tilde{\mathcal{P}}_{\mathbf{v}}} \mathbf{p}_i, \quad \Sigma_{\mathbf{v}} = \frac{1}{|\tilde{\mathcal{P}}_{\mathbf{v}}|} \sum_{\mathbf{p}_i \in \tilde{\mathcal{P}}_{\mathbf{v}}} (\mathbf{p}_i - \boldsymbol{\mu}_{\mathbf{v}})(\mathbf{p}_i - \boldsymbol{\mu}_{\mathbf{v}})^{\top} + \epsilon I
$$

其中 $\epsilon I$ 为数值稳定性引入的正则项。高斯的外观颜色 $\mathbf{c}_{\mathbf{v}}$ 则直接取自该体素内点的平均颜色。这一解析估计策略避免了传统 3DGS 所需的逐场景迭代优化，使地图构建可在探索过程中增量完成。

### 曲率感知的高斯合并

体素化后的初始高斯集合往往包含大量冗余，尤其在平坦区域。GLMap 引入曲率感知的合并策略，在保留几何细节的同时压缩表示。两个高斯 $G_i$ 与 $G_j$ 的相似度由位置、协方差和颜色的加权距离定义：

$$
D(G_i, G_j) = \| \boldsymbol{\mu}_i - \boldsymbol{\mu}_j \|_2 + \lambda_{\Sigma} \| \Sigma_i - \Sigma_j \|_F + \lambda_c \| \mathbf{c}_i - \mathbf{c}_j \|_2
$$

其中 $\lambda_{\Sigma}=0.6$，$\lambda_c=0.4$ 为平衡各项贡献的超参数。合并条件引入曲率项 $\kappa(\Sigma)$（定义为协方差矩阵最小特征值与迹的比值），使得高曲率区域（如边缘、角点）的合并阈值更严格：

$$
G_{\mathrm{new}} = G_i \oplus G_j, \quad \mathrm{if } D(G_i, G_j) < (1 + \tau (\kappa(\Sigma_i) + \kappa(\Sigma_j)))
$$

该设计使得平坦墙面等区域的高斯被大幅合并，而物体边界等细节区域的高斯得以保留，实现了表示精度与存储效率的平衡。

### 增量式实例与区域匹配

当地图已有历史语义单元时，新观测需要与已有单元进行关联与融合。实例匹配同时考虑文本嵌入的余弦相似度和合并后高斯集合的几何一致性；区域匹配则要求语义一致性（$\cos(\phi(T_{r_i}), \phi(T_{r_j})) > \tau_s$）且至少共享一个实例。匹配成功后执行合并更新：

实例合并：

$$
\mathcal{G}_j \gets \mathcal{G}_j \cup \mathcal{G}_i, \quad T_{o_j} \gets [T_{o_j}; T_{o_i}]
$$

区域合并：

$$
\mathscr{T}_{r_j} \gets \mathscr{T}_{r_j} \cup \mathscr{T}_{r_i}, \quad T_{r_j} \gets [T_{r_j}; T_{r_i}]
$$

其中 $\mathcal{G}$ 为高斯集合，$T_o$ 为实例文本描述，$\mathscr{T}_r$ 为区域包含的实例集，$T_r$ 为区域文本描述。合并后，2D 空间索引网格根据实例和区域的几何位置同步更新，支持快速空间查询。

### 价值地图与导航决策

在导航任务中，GLMap 将目标查询与所有语义单元的文本描述进行相似度计算，得到每个单元的相关性分数 $s_u$，进而通过高斯核卷积生成空间价值分布：

$$
H(l) = \frac{1}{Z} \sum_{v \in m_t} \big( \sum_{u \in \mathcal{S}_o \cup \mathcal{S}_r} s_u \delta(v - p_u) \big) \mathcal{K}_\sigma(l - v)
$$

其中 $m_t$ 为已探索区域的 2D 网格，$\mathcal{S}_o$ 和 $\mathcal{S}_r$ 分别为实例和区域语义单元集合，$p_u$ 为单元的空间位置，$\mathcal{K}_\sigma$ 为高斯平滑核。该价值地图直接指示目标物体的预测位置分布，为导航路径点选择提供依据。

### 补充图表

![[assets/figures/papers/paper_list_l2642_https_arxiv_org_abs_2605_01736/figures/003_Figure_3.jpg]]
*Figure 3: Visualization of GLMap. The leftmost column shows the 3D ground-truth environment for reference. We visualize three key components of GLMap: the 2D indexing grid, instance unit, and region unit. For each semantic unit, both the recorded textual description and the rendered image produced by 3DGS are shown. Note that only large-volume semantic units are displayed for clarity*

![[assets/figures/papers/paper_list_l2642_https_arxiv_org_abs_2605_01736/figures/005_Figure_4.jpg]]
*Figure 4: ObjectNav with GLMap. Although the goal (television) is initially unseen, the value map (computed from semantic units in GLMap) indicates the predicted likelihood of the target’s location, spatially aligned with real-world coordinates*

## 实验与分析

### 多尺度语义消融实验

GLMap 的核心设计在于将 2D 空间索引网格与实例级、区域级多尺度语义单元相结合。为验证各组件贡献，作者在 HM3D 数据集上以 ApexNAV 为基线进行了消融实验（Table 1）。实验结果表明：仅使用 2D 索引网格时，ObjectNav 成功率（SR）和路径效率（SPL）均处于较低水平；逐步引入实例单元和区域单元后，两项指标均获得显著提升。具体而言，完整 GLMap（含实例单元与区域单元）在 ApexNAV+GLMap 配置下达到 62.7% SR 和 33.7% SPL。这一结果验证了多尺度语义单元对于零样本物体导航的关键作用——实例单元提供精确的物体级语义与几何边界，区域单元补充了功能区域和场景上下文信息，两者协同使得大型模型能够更准确地推理目标物体的可能位置。

![[assets/figures/papers/paper_list_l2642_https_arxiv_org_abs_2605_01736/figures/004_Table_1.jpg]]
*Table 1: Ablation study of multi-scale semantics (instance unit and region unit) of GLMap in HM3D*

### 零样本集成实验

为验证 GLMap 作为通用语义地图表示对不同类型大型模型的兼容性，作者将其集成到三类零样本方法中：基于 LLM 的 **ESC**（Zhou et al., ICML 2023）、基于 VLM 的 **VLFM**（Yokoyama et al., ICRA 2024）以及基于 MLLM 的 **GPT4Scene**（Qi et al., arXiv 2025）。Table 2 的结果显示，集成 GLMap 后所有方法在 ObjectNav 和 SQA 任务上均获得一致提升。在 HM3D ObjectNav 上，ESC+GLMap 达到 48.8% SR 和 25.2% SPL，VLFM+GLMap 达到 59.1% SR 和 32.2% SPL，ApexNAV+GLMap 达到 62.7% SR 和 33.7% SPL；在 SQA3D 场景问答上，GPT4Scene+GLMap 达到 58.5% EM-1 和 61.3% EM-R1。这种跨模型架构的一致性提升表明，GLMap 的自然语言描述与 3D 高斯渲染图像构成的双模态接口确实实现了“零样本兼容”——大型模型无需任何额外对齐训练即可直接消费 GLMap 提供的语义信息，从而做出更优的导航决策和场景推理。

![[assets/figures/papers/paper_list_l2642_https_arxiv_org_abs_2605_01736/figures/006_Table_2.jpg]]
*Table 2: Evaluations of integrating GLMap into LLM-, VLM-, and MLLM-based methods in a zero-shot manner*

### 地图结构对比实验

Table 3 将 GLMap 与拓扑地图、栅格地图、密集几何地图进行了系统对比。从语义表示能力看，栅格地图仅能存储单一类别标签，拓扑地图缺乏精确的度量定位，密集几何地图虽能提供丰富的几何细节但缺乏显式的语义层级。GLMap 通过实例单元和区域单元的多尺度组织，同时保留了精确的 3D 几何（由 3D 高斯参数集编码）和丰富的开放式语义（由自然语言描述编码）。在下游任务性能上，GLMap 在 ObjectNav 和 SQA 任务上均优于其他地图结构，证明了多尺度语义与几何联合表示对于具身导航与推理任务的重要性。

![[assets/figures/papers/paper_list_l2642_https_arxiv_org_abs_2605_01736/figures/007_Table_3.jpg]]
*Table 3: Comparison of GLMap with other mapping structures, including topological, grid, and dense geometric maps, in terms of semantic representation and downstream task performance*

### 零样本 ObjectNav 与 InstNav 性能

Table 4 报告了在 MP3D 和 HM3D 两个模拟器上的零样本 ObjectNav 性能对比。ApexNAV+GLMap 在 HM3D 上达到 62.7% SR 和 33.7% SPL，在 MP3D 上达到 42.5% SR，均优于同期零样本方法如 **ZSON**（Majumdar et al., NeurIPS 2022）、**SG-Nav**（Yin et al., NeurIPS 2024）和 **Unigoal**（Yin et al., CVPR 2025）。Table 5 进一步展示了零样本 InstNav 任务上的性能，GLMap 达到 22.5% SR。InstNav 要求智能体定位特定实例（如“厨房桌子上的红色杯子”），对实例级语义和空间关系建模提出了更高要求。GLMap 的实例单元显式存储了每个物体的文本描述和高斯几何表示，区域单元编码了实例间的空间共现关系，这为实例级导航提供了结构化语义支撑。

![[assets/figures/papers/paper_list_l2642_https_arxiv_org_abs_2605_01736/figures/008_Table_4.jpg]]
*Table 4: Comparison with related methods on zero-shot Object-Nav in MP3D and HM3D. “TF” indicates if the method is trainingfree, and “OV” denotes if it supports open-vocabulary object goals*

![[assets/figures/papers/paper_list_l2642_https_arxiv_org_abs_2605_01736/figures/009_Table_5.jpg]]
*Table 5: Comparison with related methods on zero-shot InstNav in HM3D. “InstRel” indicates if the method models instance relations (e.g., spatial) to help locate target instances*

### 场景问答性能

Table 6 报告了 SQA3D 数据集上的场景问答性能。GPT4Scene+GLMap 达到 58.5% EM-1 和 61.3% EM-R1。SQA3D 要求模型基于对 3D 场景的理解回答自然语言问题，涉及物体定位、空间关系推理和场景功能理解。GLMap 为 MLLM 提供了显式参考（explicit references）——包括实例和区域的文本描述以及可渲染的 3D 高斯图像——而非隐式特征嵌入，这使得 MLLM 能够像理解自然场景一样直接“阅读”和“观察”GLMap 中的语义单元，从而提升推理准确性。

![[assets/figures/papers/paper_list_l2642_https_arxiv_org_abs_2605_01736/figures/010_Table_6.jpg]]
*Table 6: Comparison with related methods on SQA in SQA3D. “E-Ref” indicates if the method provides explicit references for MLLM reasoning rather than implicit embeddings*

### 价值地图与导航可视化

Figure 4 展示了 GLMap 在 ObjectNav 任务中的价值地图（value map）计算过程。即使目标物体（电视机）在初始视野中不可见，GLMap 通过语义单元相似度计算生成的空间价值分布仍能准确指示目标物体的可能位置，且与真实世界坐标空间对齐。价值地图的计算公式为：

$$H(l) = \frac{1}{Z} \sum_{v \in m_t} \big( \sum_{u \in \mathcal{S}_o \cup \mathcal{S}_r} s_u \delta(v - p_u) \big) \mathcal{K}_\sigma(l - v)$$

该公式将实例单元和区域单元的语义相似度 $s_u$ 通过空间位置 $p_u$ 投影到 2D 网格上，再经高斯核 $\mathcal{K}_\sigma$ 平滑，生成连续的空间价值分布。这种基于显式语义单元的价值推理机制，使得导航策略能够利用场景中的语义关联（如“电视机通常在客厅”）进行零样本目标搜索。

## 方法谱系与知识库定位

### 1. 核心瓶颈与动机：语义地图的三重权衡

GLMap 的提出源于现有语义地图方法在三个维度上无法同时满足零样本具身导航与推理的需求：

**瓶颈一：几何精确性与语义丰富度的冲突。** 传统栅格地图（Grid map）仅存储单一类别标签，缺乏实例边界与物体间关系；拓扑地图（Topological map）以节点-边结构抽象空间连通性，但丢失了精确定位能力；密集几何地图（Dense geometric map）虽保留高精度几何，但语义信息隐式编码于特征向量中，无法直接被大型模型消费（Figure 1）。

**瓶颈二：多尺度语义的缺失。** 现有方法通常在单一尺度上操作——要么是像素/点云级别的语义标注，要么是全局场景级别的嵌入，缺乏“物体实例”与“功能区域”之间的层次化语义组织。这使得导航系统难以同时回答“电视在哪”（实例级）和“客厅在哪个方向”（区域级）。

**瓶颈三：大型模型接口的对齐成本。** 基于特征的地图（如 CLIP embeddings）需要额外训练特征投影模块才能与 LLM/VLM/MLLM 对齐，无法实现真正的零样本使用。这一对齐训练不仅引入计算开销，还限制了地图对新模型架构的泛化能力。

### 2. 方法谱系中的定位

GLMap 处于**语义 SLAM、3D 场景表示与大型模型零样本推理**的交叉点。以下从基线方法与方法论维度定位其创新贡献：

#### 2.1 相对于零样本导航基线的提升

GLMap 本身不是导航策略，而是**可插拔的地图表示模块**，可集成到现有零样本导航框架中：

- **ESC** (Zhou et al., ICML 2023)：基于 LLM 的零样本 ObjectNav 方法，依赖语言推理选择导航目标。集成 GLMap 后，LLM 可直接消费地图中的自然语言描述与渲染图像，无需额外对齐训练。
- **VLFM** (Yokoyama et al., ICRA 2024)：基于 VLM 的零样本 ObjectNav 方法，利用视觉-语言对齐进行目标搜索。GLMap 为其提供了空间锚定的多尺度语义，弥补了 VLM 缺乏空间记忆的短板。
- **GPT4Scene** (Qi et al., arXiv 2025)：基于 MLLM 的零样本导航方法，以场景级理解驱动决策。GLMap 的显式文本与视觉参考（E-Ref）替代了隐式嵌入，使 MLLM 可直接进行空间推理。
- **ApexNAV** (Zhang et al., 2025)：零样本 ObjectNav 方法，GLMap 作为其地图后端时达到 HM3D 上 62.7% SR 的最优性能（Table 4）。

Table 2 的集成实验表明，GLMap 在 LLM-、VLM- 和 MLLM-based 方法上均带来一致且显著的性能提升，验证了其**通用零样本兼容性**——这是 GLMap 相较于需要专用对齐模块的特征地图的核心优势。

#### 2.2 相对于其他地图结构的优势

Table 3 将 GLMap 与三类主流地图结构进行对比：

| 地图类型 | 代表方法 | 几何精度 | 语义层次 | LLM/VLM 接口 |
|---------|---------|---------|---------|------------|
| 拓扑地图 | SG-Nav (Yin et al., NeurIPS 2024) | 低（节点无精确定位） | 场景图（物体关系） | 需文本化处理 |
| 栅格地图 | ZSON (Majumdar et al., NeurIPS 2022) | 中（2D 占据） | 单尺度类别标签 | 需特征投影 |
| 密集几何地图 | Unigoal (Yin et al., CVPR 2025) | 高（3D 点云/高斯） | 隐式特征 | 需特征投影 |
| **GLMap** | 本文 | **高（3D 高斯）** | **实例+区域多尺度** | **零样本文本+图像** |

GLMap 的关键差异化在于：将 3D 高斯的解析估计（无需迭代优化）与自然语言描述绑定，形成**双模态语义单元**。这使得地图既是精确的几何参考，又是大型模型可直接消费的语义接口。

#### 2.3 方法论创新：解析高斯估计与曲率感知合并

GLMap 的高斯估计器（Gaussian Estimator）从点云中**解析计算**高斯参数，而非采用 3D Gaussian Splatting 中常见的迭代梯度下降：

$$\mathcal{G} = f_{GE}(\mathcal{P})$$

具体而言，对每个体素 $\mathbf{v}$，利用其 Chebyshev 邻域 $\tilde{\mathcal{P}}_{\mathbf{v}}$ 计算均值和协方差：

$$\boldsymbol{\mu}_{\mathbf{v}} = \frac{1}{|\tilde{\mathcal{P}}_{\mathbf{v}}|} \sum_{\mathbf{p}_i \in \tilde{\mathcal{P}}_{\mathbf{v}}} \mathbf{p}_i, \quad \Sigma_{\mathbf{v}} = \frac{1}{|\tilde{\mathcal{P}}_{\mathbf{v}}|} \sum_{\mathbf{p}_i \in \tilde{\mathcal{P}}_{\mathbf{v}}} (\mathbf{p}_i - \boldsymbol{\mu}_{\mathbf{v}})(\mathbf{p}_i - \boldsymbol{\mu}_{\mathbf{v}})^{\top} + \epsilon I$$

这一解析方案避免了每帧优化，使增量式地图更新成为可能。高斯合并采用曲率感知阈值：

$$G_{\mathrm{new}} = G_i \oplus G_j, \quad \mathrm{if } D(G_i, G_j) < (1 + \tau (\kappa(\Sigma_i) + \kappa(\Sigma_j)))$$

其中 $\kappa(\Sigma) = \lambda_{\min} / \mathrm{tr}(\Sigma)$ 为曲率度量。该条件在平坦区域（低曲率）使用更宽松的阈值以合并冗余高斯，在细节区域（高曲率）保持严格阈值以保留几何细节。

### 3. 适用边界与局限

**适用场景：**
- 零样本物体导航（ObjectNav）与实例导航（InstNav），目标物体可开放词汇指定
- 具身场景问答（SQA），需要空间锚定的显式参考
- 需要与 LLM/VLM/MLLM 直接交互的具身任务

**已知局限：**
- 依赖 MLLM（Gemma3-27B）生成文本描述，语义质量受限于 MLLM 能力边界
- 依赖 GroundingDINO + MobileSAM 的开放词汇分割，在极端遮挡或小物体场景下掩膜质量可能下降
- 高斯估计假设点云足够密集，稀疏观测下协方差估计可能不稳定
- 论文未报告在动态环境或大规模长时间探索场景下的鲁棒性评估

**开放问题：**
- 如何将 GLMap 扩展到动态物体跟踪与地图更新？
- 多智能体场景下 GLMap 的共享与对齐机制？
- 是否可结合神经场表示（如 NeRF）以处理透明/镜面物体？
- 高斯合并的曲率阈值 $\tau$ 目前为固定超参数，自适应调参是否可进一步提升效率？

### 4. 知识库贡献总结

GLMap 的核心知识贡献在于提出了一种**双模态（文本+3D 高斯）多尺度（实例+区域）语义地图**，其设计原则可归纳为：

1. **零样本接口优先**：以自然语言和渲染图像作为大型模型的输入，消除特征对齐训练
2. **解析效率优先**：高斯参数由点云解析计算，支持增量更新
3. **层次化语义组织**：实例单元与区域单元分别捕获物体级和场景级语义，通过 2D 索引网格实现空间查询

这一设计范式为具身 AI 中的语义地图构建提供了新的基准思路——地图不仅是几何参考，更应成为连接感知与大型模型推理的**原生接口**。

## 原文 PDF

![[paperPDFs/CVPR_2026/Multi_Scale_Gaussian_Language_Map_for_Zero_shot_Embodied_Navigation_and_Reasoning.pdf]]