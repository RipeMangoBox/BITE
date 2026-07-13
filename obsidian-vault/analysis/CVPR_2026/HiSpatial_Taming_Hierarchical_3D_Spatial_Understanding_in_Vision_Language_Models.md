---
title: "HiSpatial: Taming Hierarchical 3D Spatial Understanding in Vision-Language Models"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/HiSpatial_Taming_Hierarchical_3D_Spatial_Understanding_in_Vision_Language_Models.pdf
project_link: "https://microsoft.github.io/HiSpatial/"
code_link: null
aliases:
- HiSpatial
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
core_operator: 通过自动数据流水线构造大规模层次化空间VQA数据（覆盖四个认知层级）并结合度量尺度3D点云输入，可系统性提升VLM的空间智能。
primary_logic: 将3D空间认知划分为四个递进式层次（几何感知→物体属性→空间关系→抽象推理），层次间存在依赖性，底层任务是高层推理的基础；度量级点云信息相比相对深度更有效地增强空间推理。
claims:
- HiSpatial在多个空间理解基准上达到SOTA，超越专门的空间模型和大型专有模型如Gemini-2.5-pro和GPT-5
- 四层次任务设计存在明确的依赖关系：移除Level 0&1任务导致Level 2性能下降25个百分点，移除Level 1&2对Level 3影响更大(-14.51%)
- 度量尺度3D点云输入比相对深度显著提升定量性能（+6.76%），且对定性性能也有小幅度提升
- 仅使用3B参数的HiSpatial模型在多个基准上超越了更大的通用模型（如GPT-5, Gemini-2.5-Pro等）
---

# HiSpatial: Taming Hierarchical 3D Spatial Understanding in Vision-Language Models

> [!tip] 核心洞察
> 将3D空间认知划分为四个递进式层次（几何感知→物体属性→空间关系→抽象推理），层次间存在依赖性，底层任务是高层推理的基础；度量级点云信息相比相对深度更有效地增强空间推理。

| 字段 | 内容 |
|------|------|
| 中文题名 | HiSpatial：驯服视觉语言模型中的层次化三维空间理解 |
| 英文题名 | HiSpatial: Taming Hierarchical 3D Spatial Understanding in Vision-Language Models |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2603.25411) · [Project](https://microsoft.github.io/HiSpatial/) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction |
| Method | HiSpatial |
| Dataset | SpatialRGPT-Quantitative, CV-Bench-3D, Custom Spatial VQA - Object-to-Camera Distance, MMBench |

> [!tip] 效果简介
> - SpatialRGPT-Quantitative (Level 1&2 Avg) 上，Accuracy (%) 79.28 (HiSpatial-3B RGB-XYZ) vs 68.70 (MM-Spatial-3B, best spatial specialist) (+10.58)。
> - CV-Bench-3D 上，Accuracy (%) 97.58 (HiSpatial-3B RGB-XYZ) vs 95.92 (RoboRefer-8B-SFT, best existing) (+1.66)。
> - Custom Spatial VQA - Object-to-Camera Distance (L1) 上，Accuracy (%) 92.18 (HiSpatial-3B) vs 58.63 (RoboRefer-8B-SFT) (+33.55)。

## 概要

视觉语言模型（VLM）在通用视觉理解任务上已取得显著进展，但在精确、可度量的三维空间理解方面仍存在根本性瓶颈：现有模型缺乏统一的层次化空间认知框架，且受制于大规模、多样化的3D空间标注数据的缺失。HiSpatial 针对这一核心问题，提出了一个原则性的四层次认知框架，将3D空间智能分解为**几何感知（Level 0）→ 物体属性理解（Level 1）→ 空间关系推理（Level 2）→ 抽象空间问题求解（Level 3）**的递进式层次结构，并构建了自动化数据流水线以生成覆盖全部层次的超大规模空间VQA数据。

**核心结论**：仅使用3B参数的HiSpatial模型在多个空间理解基准上达到SOTA，超越了专门的空间专家模型（如SpatialRGPT-8B、MM-Spatial-3B）以及大型专有模型（如GPT-5、Gemini-2.5-Pro）。关键因果证据表明：（1）四层次任务间存在明确的依赖关系——移除底层任务会显著损害高层性能（移除Level 0&1使Level 2下降25个百分点）；（2）度量尺度3D点云输入相比相对深度在定量任务上带来+6.76%的显著增益，验证了精确坐标信息对空间推理的因果重要性；（3）空间监督微调不仅未损害通用能力，反而将基础模型在MMBench等通用基准上的表现提升了近20个百分点。

**方法定位**：HiSpatial以PaliGemma2-3B为基础架构，通过添加3D点云分支（正弦编码 + 可学习patchify层 + 融合投影器）扩展为RGB-XYZ多模态VLM，在约500万张图像、4500万个物体实例、20亿QA对的大规模层次化空间数据上进行监督微调。与依赖相对深度或纯RGB输入的现有空间模型不同，HiSpatial直接利用度量尺度3D坐标作为辅助输入，从数据与架构两个维度系统性提升了VLM的空间智能。



### 三维空间理解：从感知到认知的鸿沟

视觉语言模型在二维图像理解任务上已取得显著进展，然而当任务要求模型理解三维空间结构时，现有VLM暴露出系统性缺陷。这种缺陷并非源于模型规模的不足——即便是**GPT-5**（OpenAI, 2025）和**Gemini-2.5-Pro**等大型专有模型，在空间推理基准上的表现也远逊于规模小得多的空间专家模型。问题的根源在于：**现有VLM缺乏统一的、层次化的3D空间理解任务设计，且缺乏大规模、多样化的3D空间标注数据来训练空间智能**。

具体而言，三维空间理解本质上是一个多层级认知过程：从底层几何感知（如判断像素的三维坐标），到物体级属性理解（如估计物体距离和尺寸），再到物体间空间关系推理（如判断相对位置和遮挡关系），最终上升到抽象空间问题求解（如路径规划和场景推理）。然而，现有工作往往将空间理解视为单一维度的任务集合，忽视了这些认知层级之间的递进依赖关系，导致模型无法系统性地构建空间智能。

### 现有方法的局限

当前空间VLM的研究主要存在以下瓶颈：

**任务设计的碎片化。** 现有空间理解基准和训练数据通常聚焦于特定层级的任务（如仅评估深度估计或仅评估空间关系），缺乏覆盖从几何感知到抽象推理的完整认知谱系。这种碎片化设计使得模型难以建立层级化的空间知识表征，高层推理能力缺乏底层感知的支撑。

**数据规模与多样性的不足。** 构建大规模3D空间标注数据成本高昂。现有空间VQA数据集要么规模有限，要么依赖合成场景而缺乏真实世界的多样性。这导致模型在真实场景中的泛化能力受限，难以处理开放域图像中的空间查询。

**深度信息利用的不充分。** 尽管部分工作引入了深度信息作为辅助输入，但普遍采用相对深度（relative depth）而非度量尺度的三维坐标。相对深度丢失了真实的物理尺度和三维结构信息，限制了模型进行精确空间推理的能力。

### 核心动机与思路

针对上述瓶颈，HiSpatial提出了一条系统性的解决路径。其核心洞察在于：**将3D空间认知划分为四个递进式层次（几何感知→物体属性→空间关系→抽象推理），层次间存在依赖性，底层任务是高层推理的基础；度量级点云信息相比相对深度更有效地增强空间推理**。

这一洞察驱动了三个关键设计决策：

1. **层次化任务体系**：将空间VQA任务组织为Level 0（基础几何感知）、Level 1（物体级空间理解）、Level 2（物体间关系理解）和Level 3（抽象空间推理）四个层级，为模型提供结构化的学习路径。

2. **自动化数据流水线**：构建覆盖约500万图像、4500万物体的大规模空间VQA数据生成流水线，系统性地覆盖四个认知层级，解决数据规模与多样性瓶颈。

3. **度量尺度点云融合**：引入度量尺度3D点云作为辅助输入模态，通过正弦位置编码和可学习patchify层与RGB特征融合，为模型提供精确的三维几何先验。

这种“层次化任务设计 + 大规模自动化数据 + 度量级3D输入”的组合，使得仅3B参数的HiSpatial模型能够在多个空间理解基准上超越专门的空间模型和大型专有系统，同时验证了层级间任务依赖关系的存在——移除底层任务会导致高层性能的显著退化，这为未来3D空间智能VLM的设计提供了明确的指导方向。



## 核心方法与创新机理

与现有空间VLM相比，HiSpatial的核心创新并非单一技术点的修补，而是从**任务定义、数据构造、模型输入**三个维度对3D空间理解进行系统性重构。这些创新点构成了一个相互强化的闭环：层次化任务分类指导数据生成，大规模数据支撑模型训练，度量级点云输入则让模型真正“感知”物理世界。

### 1. 创新点一：四层次递进式空间认知任务分类

现有空间理解任务大多以孤立方式设计，缺乏对认知复杂度的系统性分解。HiSpatial首次将3D空间智能明确定义为一个**四层次递进式认知体系**：

| 层次 | 认知维度 | 典型任务 | 核心能力 |
|------|----------|----------|----------|
| **Level 0** | 基础几何感知 | 逐像素3D点查询、成对深度排序 | 理解图像中任意像素在3D空间中的位置 |
| **Level 1** | 目标级空间理解 | 目标到相机距离、目标尺寸、目标朝向 | 对单个物体的空间属性进行定量/定性判断 |
| **Level 2** | 目标间关系理解 | 相对距离比较、空间方位判断、遮挡关系 | 推理多个物体之间的空间关系 |
| **Level 3** | 抽象空间推理 | 路径规划、空间布局推理、多步空间问题求解 | 基于空间信息进行复杂、多步骤的逻辑推理 |

这一分类的核心洞察在于**层次间的因果依赖性**：底层任务是高层推理的必要基础。消融实验（Table 5）给出了强有力的证据——移除Level 0和Level 1训练数据后，Level 2平均准确率从81.21%骤降至56.21%（**-25.00个百分点**）；移除Level 1和Level 2对Level 3的负面影响（-14.51个百分点）远超仅移除Level 0和Level 1（-8.14个百分点），表明高层抽象推理对中间层关系理解的依赖更为深刻。

这种层次化设计将空间智能从“黑箱能力”转化为**可分解、可诊断、可定向优化的结构化问题**，为后续研究提供了清晰的能力图谱。

### 2. 创新点二：自动化大规模层次化空间VQA数据流水线

空间VLM长期受困于数据瓶颈——人工标注3D空间关系成本极高，且难以覆盖多样化的场景和任务类型。HiSpatial构建了一条**全自动数据生成流水线**，将约5M张图像、超过45M个目标转化为覆盖四个认知层次的3D空间VQA对，总规模达**2B QA对**（Table 7）。

流水线的关键技术组件包括：
- **空间信息提取**：MoGe-2估计度量级3D点图与相机内参；RAM、GroundingDINO、SAM实现目标检测与分割；OrientAnythingv2估计物体朝向；Perspective Fields建立重力对齐世界坐标系。
- **文本指代生成**：结合Describe Anything、Qwen2.5-VL和Qwen3-VL生成物体描述，并通过VLM验证和IoU阈值过滤不可靠指代。
- **任务导向QA合成**：Level 0-2采用模板化生成（自由形式、多选题、判断题三种格式），确保覆盖广度；Level 3则使用GPT-4.1进行开放式的复杂推理问题合成，不依赖固定模板。

这一数据策略的独特价值在于：**规模化**（覆盖大规模多样场景）、**层次化**（系统覆盖四个认知层级）和**度量精度**（基于度量级3D坐标而非相对深度）三者合一，使小模型（3B参数）也能习得强大的空间推理能力。

### 3. 创新点三：度量尺度3D点云作为辅助输入模态

现有空间VLM大多仅使用RGB图像，少数引入深度信息但局限于**相对深度**（relative depth），缺乏真实物理尺度。HiSpatial的关键架构创新在于将**度量尺度3D点云**（metric-scale 3D point map）作为辅助输入：每个像素存储其在相机坐标系下的真实$(x, y, z)$坐标（前三通道），以及一个二值掩码（第四通道）。

点云处理流程为：正弦位置编码 → 可学习patchify卷积层 → 与RGB特征沿通道拼接 → 线性投影器融合为统一视觉token。训练时冻结视觉编码器，仅微调点云分支、融合投影器和LLM。

消融实验（Table 6）直接验证了这一设计的增益：RGB+XYZ在定量任务上达到82.02%，相比RGB+Relative Depth的75.26%提升**+6.76个百分点**，相比纯RGB的74.16%提升**+7.86个百分点**。定性任务上也有小幅提升（RGB+XYZ 74.43 vs RGB+Relative Depth 72.76）。这证明**真实的物理尺度信息**——而非仅仅是“哪个更近”的相对判断——是空间推理的关键赋能因素。

### 4. 创新的协同效应

上述三个创新之间存在深层协同：
- **层次化任务分类**为数据生成提供了清晰的覆盖目标，确保训练数据系统性地覆盖从几何感知到抽象推理的完整认知谱系；
- **大规模度量级数据**使模型能够在真实物理尺度上学习空间关系，而非仅依赖图像中的视觉线索；
- **点云输入**让模型在推理时能直接访问精确3D坐标，与训练数据的度量精度形成闭环。

这种“任务-数据-模型”三位一体的设计，使仅3B参数的HiSpatial在多个空间理解基准上超越了更大的通用模型（如GPT-5、Gemini-2.5-Pro）和专门的空间专家模型（如SpatialRGPT-8B、MM-Spatial-3B），同时还在通用VQA基准上相比基础模型PaliGemma2-3B提升了**+19.81个百分点**（Table 4），说明层次化空间训练对整体视觉理解具有正向迁移效应。



HiSpatial 的整体框架围绕一个核心洞察展开：**3D 空间认知可以被解耦为四个递进式层次，层次间存在因果依赖关系**。基于这一认知，方法设计了一条“数据构建→层次化任务设计→度量点云增强→监督微调”的完整流水线，如 Figure 2 和 Figure 3 所示。

![[assets/figures/papers/paper_list_l2396_https_arxiv_org_abs_2603_25411/figures/002_Figure_2.jpg]]
*Figure 2: Overview of our approach. Left: Data construction pipeline which generates spatial-related VQA pairs from either in-the-wild images or existing data with 3D annotations. Right: Hierarchical spatial understanding task taxonomy with representative QA pairs*

### 流水线总览

整个系统由两大阶段构成：

1. **自动数据构建流水线**（Figure 2 左）：从大规模 2D 图像出发，自动估计度量级 3D 空间信息、检测并描述物体，再按层次化任务分类合成空间 VQA 对。
2. **空间增强 VLM 微调**（Figure 3）：在 PaliGemma2-3B 基础模型上新增 3D 点云分支，将度量尺度点云与 RGB 特征融合后送入 LLM，联合微调实现层次化空间理解。

### 数据构建流水线：从 2D 图像到层次化空间 VQA

数据流水线处理约 **5M 图像**，覆盖超过 **45M 目标**，最终生成约 **2B QA 对**。其核心模块按执行顺序为：

| 模块 | 功能 | 关键组件 |
|------|------|----------|
| 空间信息提取 | 从单张 2D 图像估计度量 3D 点图、相机内参、物体检测/分割/朝向、重力对齐世界坐标系 | MoGe-2（点图估计）、RAM + GroundingDINO + SAM（检测分割）、OrientAnythingv2（朝向）、Perspective Fields（世界坐标系） |
| 文本指代生成 | 为每个检测到的物体生成自然语言描述 | Describe Anything、Qwen2.5-VL、Qwen3-VL；辅以 VLM 验证和 IoU 阈值过滤不可靠描述 |
| 任务导向 QA 合成 | 基于空间信息和文本指代，按四层次任务分类生成 VQA 对 | Level 0–2 使用模板（自由形式、多选题、判断题）；Level 3 由 GPT-4.1 进行复杂推理合成 |

**输入**：单张 RGB 图像（可来自 in-the-wild 数据或已有 3D 标注数据）。  
**输出**：覆盖四个认知层次的多样化空间 VQA 数据（Figure 4、Figure 5 展示了各层次示例）。

### 层次化任务设计：四层认知金字塔

HiSpatial 将 3D 空间智能形式化为四个递进层次（Figure 2 右），层次间存在明确的依赖关系：

- **Level 0 — 基础几何感知**：像素级 3D 点查询、成对深度排序。这是最底层的几何理解，为后续所有层次提供度量基础。
- **Level 1 — 目标级空间理解**：物体到相机的距离、物体尺寸、朝向等单物体属性。依赖 Level 0 的几何信息。
- **Level 2 — 物体间关系理解**：物体间的相对距离、方位关系、空间布局。**移除 Level 0 和 Level 1 训练任务后，Level 2 平均准确率从 81.21% 骤降至 56.21%（-25.00%）**，验证了底层几何感知和目标理解对关系推理的因果支撑作用（Table 5）。
- **Level 3 — 抽象空间推理**：多步推理、空间问题求解。**移除 Level 1 和 Level 2 对 Level 3 的负面影响（-14.51%）远大于仅移除 Level 0 和 Level 1（-8.14%）**，说明高层抽象推理更依赖中间层的关系理解（Table 5）。

这一层次化设计是方法的核心“因果旋钮”：通过系统性覆盖四个层次，模型从底层几何感知逐步构建到高层推理能力。

### 模型架构：度量点云增强的 VLM

模型以 **PaliGemma2-3B**（SigLIP 视觉编码器 + Gemma-2 LLM，输入分辨率 448²）为基础，新增 3D 点云分支（Figure 3）：

1. **点云编码**：度量 3D 点图 $\mathbf{X} \in \mathbb{R}^{H \times W \times 4}$（前 3 通道为相机坐标系下的 XYZ 坐标，第 4 通道为二值掩码）经过正弦位置编码和可学习的 patchify 卷积层（Conv2D），生成与 RGB 特征空间分辨率一致的点云特征图。
2. **特征融合**：RGB 特征图与点云特征图沿通道维度拼接，通过线性投影器产生融合视觉 token。
3. **端到端微调**：冻结视觉编码器，联合微调点云分支、融合投影器和 LLM。训练损失为标准 SFT 交叉熵：
   $$\mathcal{L} = -\sum_{t=1}^{T} \log P_{\theta}(\mathbf{y}_t \mid \mathbf{y}_{<t}, \mathbf{I}, \mathbf{X})$$
   其中 $\mathbf{I}$ 为 RGB 图像，$\mathbf{X}$ 为度量点云，$\mathbf{y}_t$ 为第 $t$ 个输出 token。

**关键设计选择**：使用度量尺度点云（RGB+XYZ）而非相对深度。消融实验表明，RGB+XYZ 在定量任务上达到 82.02%，相比 RGB+Relative Depth（75.26%）提升 **+6.76 个百分点**（Table 6），验证了精确 3D 坐标对空间理解的增益。

### 训练策略

- **数据混合**：空间 VQA 数据与通用 VQA 数据（LLaVA-Next）按采样比 **1:7** 混合，避免模型在空间任务上过拟合而损失通用能力。
- **训练配置**：AdamW 优化器，学习率 $2 \times 10^{-5}$，训练最多 70K 迭代。
- **评估协议**：定量问题使用 GPT-4.1 进行关键词提取和答案验证，预测值在真实值的 0.75–1.25 倍（或 25% 误差）内视为正确，保证评估的公平性和可复现性。

### 输入输出流总结

- **推理输入**：单张 RGB 图像 + 对应的度量 3D 点图（由 MoGe-2 在线估计）。
- **推理输出**：针对空间问题的自然语言答案，覆盖从基础几何查询到抽象推理的四个层次。
- **关键约束**：当前仅支持单目输入，无法处理多视角或视频时序推理场景（论文已列为主要局限之一）。

### 补充图表

![[assets/figures/papers/paper_list_l2396_https_arxiv_org_abs_2603_25411/figures/001_Figure_1.jpg]]
*Figure 1: Trained on our large-scale spatial VQA data, our model develops hierarchical 3D spatial intelligence from geometric perception to abstract reasoning (left), and achieves state-of-the-art results on multiple spatial benchmarks (top-right). We also uncover clear inter-level task dependencies in spatial supervised fine-tuning (bottom-right), offering guidance for designing future 3D spatially intelligent VLMs*



HiSpatial 的架构核心是在标准视觉语言模型（VLM）基础上引入一个 **度量尺度3D点云分支**，并通过四个流水线模块完成从2D图像到层次化空间VQA数据的全自动构造。以下聚焦于模型端的关键模块与唯一显式给出的训练公式。

### 3D点云分支与多模态融合

模型以 PaliGemma2-3B（SigLIP 视觉编码器 + Gemma-2 语言模型）为基座，在其上添加一个并行的3D点云处理分支，整体架构见 Figure 3。

![[assets/figures/papers/paper_list_l2396_https_arxiv_org_abs_2603_25411/figures/003_Figure_3.jpg]]
*Figure 3: Model architecture of our VLM, which integrates metricscale 3D point map as auxiliary input*

**输入表示**：对于每张 RGB 图像 $\mathbf{I}$，模型同时接收一个度量尺度的3D点图 $\mathbf{X} \in \mathbb{R}^{H \times W \times 4}$。前三个通道存储每个像素在相机坐标系下的 $(x, y, z)$ 坐标，第四个通道为二值掩码，指示该像素是否有有效的3D信息。

**点云编码**：$\mathbf{X}$ 首先经过正弦位置编码，随后通过一个可学习的 patchify 卷积层（Conv2D），将其转换为与 RGB 特征图空间尺寸对齐的特征表示。RGB 分支的视觉编码器在此阶段保持冻结。

**特征融合**：将 RGB 特征图与点云特征图沿通道维度拼接，再通过一个线性投影器（fused-token projector）产生融合后的视觉 token 序列。这些 token 与文本 token 一同送入 Gemma-2 语言模型进行自回归生成。

### 监督微调损失函数

整个可训练部分（点云 patchify 层、融合投影器、语言模型）通过标准的自回归交叉熵损失进行端到端联合优化：

$$\mathcal{L} = -\sum_{t=1}^{T} \log P_{\theta}(\mathbf{y}_t \mid \mathbf{y}_{<t}, \mathbf{I}, \mathbf{X})$$

其中：
- $T$ 为输出序列长度；
- $\mathbf{y}_t$ 为第 $t$ 个目标 token；
- $\mathbf{y}_{<t}$ 为前 $t-1$ 个已生成的 token；
- $\mathbf{I}$ 为 RGB 图像输入；
- $\mathbf{X}$ 为度量尺度3D点图输入；
- $P_{\theta}$ 为模型在参数 $\theta$ 下对下一 token 的条件概率分布。

该损失函数本身是标准 SFT 范式，其关键差异在于条件中显式引入了度量级3D几何先验 $\mathbf{X}$，使模型在逐 token 预测时能够同时利用视觉外观与精确空间坐标信息。

### 数据构造流水线中的关键模块

虽然数据流水线不直接参与推理时计算，但其四个模块是方法有效性的前提保障：

1. **空间信息提取**：以 MoGe-2 估计像素级度量3D点图和相机内参；用 RAM → GroundingDINO → SAM 级联流水线进行开放词汇目标检测与分割；以 OrientAnythingv2 估计物体朝向；借助 Perspective Fields 建立重力对齐的世界坐标系。

2. **文本指代生成**：结合 Describe Anything、Qwen2.5-VL 和 Qwen3-VL 为每个检测到的目标生成自然语言描述，并通过额外的 VLM 验证步骤和 IoU 阈值过滤不可靠指代。

3. **任务导向的 QA 合成**：基于提取的空间信息与文本指代，按四层次任务分类（L0 几何感知 → L1 物体属性 → L2 空间关系 → L3 抽象推理）生成多样化 VQA 对。L0–L2 采用自由形式、多选题、判断题三种模板格式；L3 不使用模板，而是通过向 GPT-4.1 提供空间场景描述，指示其生成需要多步推理的复杂问题。

4. **监督微调混合策略**：将自建空间 VQA 数据与 LLaVA-Next 通用 VQA 数据以 1:7 的采样比例混合训练，使用 AdamW 优化器（学习率 $2 \times 10^{-5}$）训练至多 70K 步。

> **注意**：论文未给出点云 patchify 层或融合投影器的具体结构细节公式，也未推导损失函数的梯度形式。上述公式 $\mathcal{L}$ 是论文中唯一显式给出的数学表达式（Eq. 1），其余模块以架构描述和工程流程为主。



## 实验与关键发现

### 主实验结果

HiSpatial在多个空间理解基准上全面超越现有空间专家模型和大型专有模型，仅使用3B参数即达到SOTA。Table 1展示了定量VQA基准（Level 1 & 2）的对比结果：HiSpatial-3B（RGB-XYZ）在SpatialRGPT-Quantitative上达到79.28%的平均准确率，比最强的空间专家模型MM-Spatial-3B（68.70%）高出10.58个百分点，比GPT-5（40.47%）和Gemini-2.5-Pro（26.57%）分别高出38.81和52.71个百分点。值得注意的是，即使仅使用RGB输入的HiSpatial-3B-RGB（72.43%）也显著优于所有基线。

在定性VQA基准上（Table 2），HiSpatial-3B在3DSRBench上达到63.81%，相比GPT-4o（44.20%）和Gemini-2.5-Pro（48.47%）分别提升19.61和15.34个百分点；在RoboSpatial上达到86.18%，在EmbSpatial上达到79.78%。在自建空间VQA基准上（Table 3），HiSpatial在物体到相机距离（L1）任务上达到92.18%，远超RoboRefer-8B-SFT的58.63%（+33.55个百分点），体现了度量尺度点云输入对精确距离感知的关键增益。

![[assets/figures/papers/paper_list_l2396_https_arxiv_org_abs_2603_25411/figures/005_Table_2.jpg]]
*Table 2: Accuracy (%) on qualitative VQA benchmarks evaluating spatial understanding and reasoning across levels 1–3*

![[assets/figures/papers/paper_list_l2396_https_arxiv_org_abs_2603_25411/figures/006_Table_3.jpg]]
*Table 3: Accuracy (%) on our custom spatial VQA benchmark*

通用VQA能力方面（Table 4），HiSpatial-3B在MMBench上达到69.67%，相比基础模型PaliGemma2-3B（49.86%）大幅提升19.81个百分点，说明层次化空间SFT不仅未损害通用能力，反而促进了整体视觉理解。

![[assets/figures/papers/paper_list_l2396_https_arxiv_org_abs_2603_25411/figures/007_Table_4.jpg]]
*Table 4: Accuracy (%) on general VQA benchmarks compared to our base model PaliGemma2*

### 消融实验

**跨层次任务依赖性。** Table 5揭示了四层次任务设计间的强依赖关系。移除Level 0和Level 1训练任务后，Level 2的平均准确率从81.21%骤降至56.21%（-25.00个百分点），证明底层几何感知和目标理解是关系推理的必要基础。移除Level 1和Level 2对Level 3的负面影响（-14.51个百分点）远大于仅移除Level 0和Level 1（-8.14个百分点），说明高层抽象推理更依赖中间层的关系理解，而非直接依赖底层几何感知。这一发现为空间VLM的训练策略设计提供了明确指导：底层任务不可省略，且中间层关系理解对高层推理的支撑作用更为关键。

**3D输入模态的影响。** Table 6对比了不同3D辅助输入的效果。RGB+度量尺度点云（RGB+XYZ）在定量任务上达到82.02%，相比RGB+相对深度（75.26%）提升6.76个百分点，相比纯RGB（74.16%）提升7.86个百分点。定性任务上，RGB+XYZ（69.74%）同样优于RGB+相对深度（68.42%）和纯RGB（67.47%）。结果表明，度量尺度的精确3D坐标信息对空间理解（尤其是定量任务）的增益显著高于相对深度，验证了引入真实世界尺度信息的设计选择。

**训练数据配置。** Table 7展示了训练数据集的统计信息。数据覆盖四个层次共约2B QA对，其中Level 1和Level 2任务占比最大。训练时空间VQA数据与通用VQA数据（LLaVA-Next）按1:7采样比混合，有效避免了空间任务过拟合，同时保持了通用能力。

### 失败模式与局限性

尽管HiSpatial在主基准上表现突出，但仍存在若干局限。首先，模型泛化受限于任务复杂度和语言多样性：Level 3抽象推理覆盖不全，且数据生成依赖模板，导致对非模板化、口语化输入的鲁棒性不足。其次，论文揭示了层次间依赖性的存在，但更细粒度的交互机制（如不同训练策略对跨层关系的影响）尚未充分研究。此外，当前模型仅支持单目输入，无法处理多视角场景理解或视频中的时间动态推理任务。这些局限为后续工作指明了方向：提升自然语言鲁棒性、探索课程学习或分层微调策略、扩展至多视角/多帧场景。

### 补充图表

![[assets/figures/papers/paper_list_l2396_https_arxiv_org_abs_2603_25411/figures/004_Table_1.jpg]]
*Table 1: Accuracy (%) on quantitative VQA benchmarks for level-1 and level-2 spatial understanding. ∗ denotes using GT point map*

![[assets/figures/papers/paper_list_l2396_https_arxiv_org_abs_2603_25411/figures/008_Table_5.jpg]]
*Table 5: Inter-level task dependency analysis. Removing lower-level tasks in training reduces higher-level performance; see text for details*

![[assets/figures/papers/paper_list_l2396_https_arxiv_org_abs_2603_25411/figures/009_Table_6.jpg]]
*Table 6: Effect of auxiliary 3D input on model accuracy (%)*

![[assets/figures/papers/paper_list_l2396_https_arxiv_org_abs_2603_25411/figures/010_Table_7.jpg]]
*Table 7: Task statistics of our training dataset*

![[assets/figures/papers/paper_list_l2396_https_arxiv_org_abs_2603_25411/figures/014_Figure_5.jpg]]
*Figure 5: Examples of spatial VQA data constructed using our method, covering different task levels*

![[assets/figures/papers/paper_list_l2396_https_arxiv_org_abs_2603_25411/figures/015_Figure_6.jpg]]
*Figure 6: Examples of our model’s responses on unseen images*



## 定位与知识库关联

### 与现有空间VLM的关系

HiSpatial 处于“通用VLM + 空间增强”这一研究脉络中，但其设计选择与现有工作形成三个关键分叉：

- **输入模态升级**：现有空间专家模型（如 **SpatialRGPT-8B**、**MM-Spatial-3B**、**RoboRefer-8B-SFT**）普遍采用RGB-D输入，但深度信息通常为相对深度。HiSpatial 改用**度量尺度3D点云（RGB-XYZ）**，消融实验表明这一替换在定量空间任务上带来 **+6.76%** 的增益（Table 6），验证了精确3D坐标比相对深度更有效地支撑空间推理。

- **任务设计范式**：多数空间VLM将空间理解视为单一能力维度，缺乏结构化分解。HiSpatial 提出**四层次认知层级**（几何感知→物体属性→空间关系→抽象推理），并通过跨层消融实验证明了层次间的因果依赖性：移除Level 0&1训练数据导致Level 2性能下降 **25个百分点**，移除Level 1&2对Level 3的影响更大（**-14.51%**）。这一发现为空间VLM的训练数据设计提供了明确的指导原则。

- **数据规模与多样性**：现有空间VQA数据集（如SpatialRGPT、QSpatial等基准）规模有限且任务覆盖窄。HiSpatial 构建的自动数据流水线处理约 **5M图像、45M目标**，生成覆盖四个认知层级的 **2B QA对**，在数据规模和任务多样性上形成显著差异。

### 与通用大模型的定位差异

HiSpatial 的核心定位是**以小博大**：仅使用 **3B参数**的模型在多个空间理解基准上超越了大型专有模型。Table 1显示，HiSpatial-3B（RGB-XYZ）在SpatialRGPT-Quantitative Level 1&2平均准确率达 **79.28%**，而 **GPT-5** 仅 **40.47%**、**Gemini-2.5-Pro** 仅 **26.57%**。在定性基准（Table 2）上同样保持优势：HiSpatial-3B在3DSRBench上达 **63.81%**，超过GPT-4o（**44.20%**）和Gemini-2.5-Pro（**48.47%**）。这表明通用大模型的空间智能远未饱和，而**专门化的层次化空间训练 + 度量级3D输入**是高效提升空间智能的关键路径。

### 适用边界与局限

1. **任务复杂度边界**：当前模型主要处理相对基础的空间理解任务。Level 3抽象推理覆盖不全，数据生成对复杂多步推理场景的多样性有限，模型在需要深度空间推理的真实世界任务上可能存在能力缺口。

2. **语言鲁棒性不足**：数据生成过程依赖模板（Level 0–2），导致模型对非模板化、口语化的空间查询鲁棒性不足。这是限制其直接部署到开放域应用的关键瓶颈。

3. **单目输入限制**：当前架构仅支持单目输入，无法处理需要多视角场景理解或视频中时间动态推理的任务。扩展到多视角或视频场景需要重新设计3D线索的融合机制。

4. **层次依赖的粗粒度理解**：论文揭示了层级间的整体依赖关系，但更细粒度的交互机制（如Level 1的哪些子任务对Level 2的哪些子任务最关键）尚未分析，不同训练策略（课程学习、分层微调、强化微调）对跨层关系的影响也未探索。

### 开放问题

- **自然语言泛化**：如何在不依赖模板的情况下大规模生成多样化、口语化的空间QA数据，以提升模型对真实用户输入的鲁棒性？
- **层级解耦与优化**：课程学习或分层微调策略是否能进一步解耦层次间的依赖，使高层任务在不牺牲底层能力的前提下获得更大增益？
- **多视角/时序扩展**：当模型扩展到多视角或多帧视频场景时，如何高效融合时序与多视角的度量3D线索？点云分支是否需要引入跨帧对齐机制？
- **与具身智能的桥接**：HiSpatial的空间理解能力（特别是Level 2空间关系与Level 3抽象推理）能否直接迁移到具身场景中的导航、操控等任务？是否需要额外的具身对齐训练？



## 原文 PDF

![[paperPDFs/CVPR_2026/HiSpatial_Taming_Hierarchical_3D_Spatial_Understanding_in_Vision_Language_Models.pdf]]
