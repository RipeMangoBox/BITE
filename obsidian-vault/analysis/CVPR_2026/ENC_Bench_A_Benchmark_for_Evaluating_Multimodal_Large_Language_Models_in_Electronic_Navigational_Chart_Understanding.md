---
title: "ENC-Bench: A Benchmark for Evaluating Multimodal Large Language Models in Electronic Navigational Chart Understanding"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/ENC_Bench_A_Benchmark_for_Evaluating_Multimodal_Large_Language_Models_in_Electronic_Navigational_Chart_Understanding.pdf
project_link: null
code_link: null
aliases:
- EB
- ENC-Bench
tags:
- CVPR_2026
- topic/benchmarks_datasets_evaluation
- topic/benchmarks_datasets_evaluation/benchmarking
core_operator: 专业 ENC 理解的成败关键在于模型对 IHO S-57 标准化向量符号体系的视觉-语义映射能力，以及对多尺度制图综合（cartographic generalization）和不同光照渲染模式下的不变性学习。若能改善这些能力，MLLMs 才有可能缩小通用视觉理解与安全关键领域之间的鸿沟。
primary_logic: 该工作通过构建首个严格遵循海事导航认知层次（感知→空间推理→决策）的基准 ENC-Bench，系统性揭示了当前最先进 MLLMs 在专业符号推理、精确空间计算和多约束安全决策方面的严重不足，尤其是坐标网格符号解读构成了最突出的能力断层。同时发现光照和尺度变化带来的性能冲突表明现有视觉架构缺乏对专业领域视觉特征的归纳偏置。
claims:
- 最佳模型在整体平均准确率上仅达 47.88%，仅略微超过随机基线（29.76%）
- 在距离测量任务中，所有模型的相对误差均值超过 40%，最高准确率仅约 26%
- 地理坐标定位（Geo）准确率显著低于直接像素定位，表明符号网格解读是更关键的瓶颈
- 感知与决策任务在 Night 模式下平均下降最高达 6%，而空间推理任务却因高对比度单色渲染而有所改善，证明颜色依赖与符号可读性之间存在权衡
---

# ENC-Bench: A Benchmark for Evaluating Multimodal Large Language Models in Electronic Navigational Chart Understanding

> [!tip] 核心洞察
> 该工作通过构建首个严格遵循海事导航认知层次（感知→空间推理→决策）的基准 ENC-Bench，系统性揭示了当前最先进 MLLMs 在专业符号推理、精确空间计算和多约束安全决策方面的严重不足，尤其是坐标网格符号解读构成了最突出的能力断层。同时发现光照和尺度变化带来的性能冲突表明现有视觉架构缺乏对专业领域视觉特征的归纳偏置。

| 字段 | 内容 |
|------|------|
| 中文题名 | 用于评估多模态大语言模型电子航海图理解能力的基准：ENC-Bench |
| 英文题名 | ENC-Bench: A Benchmark for Evaluating Multimodal Large Language Models in Electronic Navigational Chart Understanding |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2603.22763) |
| Topic | #topic/benchmarks_datasets_evaluation #topic/benchmarks_datasets_evaluation/benchmarking |
| Method | ENC-Bench (基准框架) |
| Dataset | ENC-Bench, ENC-Bench L-1 Perception, ENC-Bench L-2 Spatial, ENC-Bench L-3 Decision |

> [!tip] 效果简介
> - ENC-Bench 上，Overall Accuracy 47.88% (Gemini-2.5-Pro) vs 29.76% (Random Chance) (+18.12%)。
> - ENC-Bench L-1 Perception (Symbol Recognition) 上，Accuracy 69.53% (Gemini-2.5-Pro) vs 25.0% (Random) (+44.53%)。
> - ENC-Bench L-2 Spatial (Bearing Acc@20°) 上，Accuracy@20° 55.64% (Qwen3-VL-235B-Thinking) vs 25.15% (GPT-4o) (+30.49%)。

## 概述

**ENC-Bench** 是一个面向电子航海图（ENC）理解的多模态大语言模型（MLLM）评估基准。该工作聚焦一个核心问题：当前通用 MLLMs 能否弥合通用视觉理解与专业、结构化、安全关键的 ENC 领域之间的鸿沟？

**核心发现**：答案是否定的。即使是最强模型（Gemini-2.5-Pro），在 ENC-Bench 上的整体准确率仅为 **47.88%**，仅略微超过随机基线（29.76%）。这一结果揭示了三个根本性瓶颈：

1. **符号基础断层**：模型无法正确解读 IHO S-57 标准的坐标网格、比例尺和向量符号体系，地理坐标转换能力严重不足。
2. **多约束推理缺失**：在需要同时满足距离、水深和法规的决策任务中，模型缺乏全局约束的显式枚举与验证机制，倾向于局部贪心优化。
3. **环境鲁棒性差**：对光照模式（Day/Dusk/Night）和制图尺度的变化适应性不足，颜色依赖与符号可读性之间存在冲突。

**方法定位**：ENC-Bench 并非提出新模型，而是构建了一个严格遵循海事导航认知层次（感知→空间推理→决策）的基准框架。该基准包含 **20,490 个专家验证样本**，源自 840 张真实 NOAA S-57 海图，通过四阶段管道（数据渲染与解析→图像配准→特征标注→问题生成）自动生成，覆盖 10 个任务维度、3 种光照模式和 6 个尺度级别。

**主要结果**：在感知层面，符号识别准确率最高达 69.53%；但在空间推理层面，距离测量相对误差均值超过 40%，方位计算精度有限；在决策层面，锚地选择任务的最佳性能仅勉强超过随机（30.50% vs 25%）。光照与尺度的消融实验进一步表明，Night 模式下感知与决策任务平均下降最高达 6%，小尺度下线性特征理解下降 8.6%——现有视觉架构缺乏对专业领域视觉特征的归纳偏置。

该基准的提出，为 MLLMs 在安全关键领域的应用划定了当前的能力边界，并指明了符号-语义映射、多尺度不变性学习和显式约束推理等关键改进方向。

## 背景与动机

### 专业导航图的认知鸿沟

电子航海图（Electronic Navigational Chart, ENC）是国际海事组织强制要求的现代船舶导航核心工具，其符号体系由国际水文组织（IHO）的 S-57 标准严格定义。与日常使用的消费级地图（如 Google Maps）不同，ENC 以安全为第一优先级，用标准化的向量符号替代视觉真实感，呈现水深等深线、航道边界、助航标志等关键信息（Figure 4）。这种“符号化现实”要求使用者具备将抽象视觉基元映射为精确语义与空间约束的专业能力——这一能力正是当前多模态大语言模型（MLLMs）与人类专业导航员之间的根本性差距所在。

### 现有基准的评估盲区

当前主流的 MLLM 视觉理解基准在设计上存在三个与专业导航需求错配的结构性盲区：

1. **符号体系错配**：现有基准多评估自然图像中的日常物体或非正式符号（如数学公式、流程图），从未涉及 IHO S-57 这类具有法律效力的标准化专业符号体系。ENC 中的点状符号（如灯塔、沉船标记）是复合图形，其形状、顶标、颜色均携带强制性语义（Figure 5），识别需要细粒度的视觉细节判别能力。
2. **空间推理降级**：现有基准的空间推理多限于欧几里得布局或相对位置判断，而 ENC 理解要求基于地理坐标网格的精确度量计算——包括半正矢距离、真北方位角、以及像素-地理坐标的双向映射。这些计算必须同时满足航海精度要求（如距离相对误差容忍度在 20% 以内）。
3. **环境条件缺失**：真实导航发生在多种操作光照模式（Day/Dusk/Night，Figure 6）和制图尺度（1:50k 至 1:200k+，Figure 7）下。光照变化会非线性地改变颜色映射（如浅水区蓝色在 Night 模式下转为深灰/黑色），而尺度变化会触发制图综合（cartographic generalization），使部分特征在视觉上消失。现有基准均未评估模型在这些条件下的鲁棒性。

Table 1 系统对比了 ENC-Bench 与现有基准在标准化符号识别、精确地理空间推理、多尺度、多光照四个维度的覆盖情况，确认了上述盲区的普遍存在。

### 安全关键领域的评估紧迫性

海事导航是典型的安全关键领域：符号误读或空间计算错误可能导致搁浅、碰撞等灾难性后果。然而，MLLMs 在该领域的零样本能力从未被系统评估。回答“当前模型能否弥合通用视觉理解与结构化、符号化、安全关键领域之间的鸿沟”这一问题，不仅关乎 AI 在垂直领域的应用边界，更涉及自动化偏见（automation bias）在实际部署中的潜在风险——若模型在缺乏不确定性量化的情况下被用于辅助决策，其符号基础缺口与推理幻觉可能被操作者过度信任，导致严重后果。

### 本文动机与核心贡献

基于上述缺口，本文提出 **ENC-Bench**——首个严格遵循海事导航认知层次（感知→空间推理→决策）的基准，旨在系统性诊断 MLLMs 在专业 ENC 理解中的能力边界。ENC-Bench 包含 20,490 个经过专家验证的样本，源自 840 张真实 NOAA S-57 海图，通过校准的向量-图像管道生成，覆盖三种光照模式与六种制图尺度。其三层评估框架（Figure 1）分别对应符号识别与特征理解（L-1 感知）、精确度量空间推理（L-2）、以及多约束安全决策（L-3），从而为回答核心开放问题提供可量化的实验基础。

## 核心创新

本工作并未提出新的模型架构或训练算法，其核心创新在于**构建了首个严格遵循海事导航认知层次的基准框架 ENC-Bench**，并以此系统性揭示了当前先进 MLLMs 在专业电子航海图理解中的能力边界。与已有视觉问答或文档理解基准（Table 1）相比，ENC-Bench 的关键差异化创新体现在以下三个 changed slots 上。

### 1. 任务框架创新：从通用视觉到专业认知层次

现有基准（如 ChartQA、DocVQA）主要关注通用图表或文档的视觉问答，缺乏对专业领域符号体系和空间推理的覆盖。ENC-Bench 将评估框架构建为三层认知层次（Figure 1），直接映射专业导航员的认知流程：
- **L-1 感知层**：要求模型识别 IHO S-57 标准下的点、线、面特征符号及其语义属性，而非自然图像中的通用物体。
- **L-2 空间推理层**：引入基于 Haversine 球面公式和方位角计算的精确地理空间推理任务，包括坐标定位、距离测量和方位计算，要求模型建立像素-地理坐标的映射能力。
- **L-3 决策层**：设计多约束安全决策任务（如锚地选择、安全通过判定），要求模型同时满足距离、水深和法规约束。

这一层次化设计直接暴露了 MLLMs 从“看懂符号”到“做出安全决策”之间的能力断层——最佳模型 Gemini-2.5-Pro 在 L-1 符号识别上可达 69.53%，但在 L-3 锚地选择上仅 30.50%，勉强超过随机基线（25%）（Table 3）。

### 2. 数据构建创新：校准化的矢量到图像管道

与直接使用自然图像或截图的数据集不同，ENC-Bench 的数据生成管道（Figure 2）包含四个关键创新模块：

- **多条件渲染**：使用 OpenCPN 对 840 张 NOAA S-57 海图在三种 ECDIS 标准光照模式（Day/Dusk/Night）和六种制图尺度下进行渲染，系统性地引入了光照和尺度这两个在已有基准中被忽略的分布偏移因素。
- **精确图像配准**：通过手动标注控制点建立仿射变换矩阵，实现像素坐标与地理坐标（经纬度）的双向精确映射，为空间推理任务提供了亚像素级的地面真值。
- **图染色特征标注**：采用图染色算法对点特征进行分组以避免视觉重叠，确保标注框的视觉清晰度，并通过专家审核保证正确性。
- **公式驱动的问题生成**：利用航海公式（Haversine 距离、方位角计算）自动生成空间推理真值，并基于常见错误模式构造干扰项，最终产生 20,490 个经专家验证的样本。

### 3. 评估维度创新：符号基础与分布鲁棒性的双重揭示

ENC-Bench 在评估维度上的核心创新在于**分离了“视觉定位”与“符号解读”两种能力**，并通过多条件消融揭示了模型失败的因果机制：

- **Geo vs. Pixel 坐标定位**（Table 10）：通过分别评估地理坐标（需解读经纬度网格符号）和像素坐标（仅需视觉定位）的定位精度，发现 Gemini-2.5-Pro 在 Acc@200px 下 Geo 准确率（17.36%）显著低于 Pixel（21.43%），在严格阈值 Acc@50px 下 Geo 多为 0%。这直接证明了**符号网格解读（而非视觉定位本身）是当前 MLLMs 的核心瓶颈**。

- **光照与尺度的冲突性影响**（Table 5, Table 6）：Night 模式导致 Track Direction 准确率下降 6.43%，但坐标定位误差却减少了 101.9 像素（因高对比度单色渲染提高了网格线可读性）；小尺度（1:200k 以上）造成线性特征理解下降 8.6%、Track Direction 下降近 16%。这种**颜色依赖与符号可读性之间的权衡**表明现有视觉架构缺乏对专业领域视觉特征的归纳偏置。

综上，ENC-Bench 的创新不在于提出新的模型，而在于**通过精心设计的基准框架和评估协议，将 MLLMs 在安全关键专业领域的能力缺陷从“整体性能低下”细化为“符号基础断裂”“多约束推理缺失”“分布鲁棒性冲突”三个可诊断的因果瓶颈**，为后续的领域适配研究提供了明确的方向指引。

## 整体框架

ENC-Bench 提出了一套系统化的评估框架，旨在填补多模态大语言模型（MLLMs）在专业电子航海图（ENC）理解能力评估方面的空白。该框架的核心设计思想是模拟海事导航员的认知层次，将评估任务组织为三个递进的层级：**感知（L-1）**、**空间推理（L-2）** 和 **海事决策（L-3）**，如 Figure 1 所示。这种分层结构从基础的符号识别逐步过渡到复杂的多约束安全决策，全面覆盖了从“看”到“算”再到“判”的专业导航认知链条。

![[assets/figures/papers/paper_list_l2740_https_arxiv_org_abs_2603_22763/figures/001_Figure_1.jpg]]
*Figure 1: Overview of ENC-Bench. Our benchmark evaluates MLLMs across three hierarchical tiers: Perception (L-1), Spatial Reasoning (L-2), and Maritime Decision-Making (L-3). Example tasks are shown on the left with corresponding visual elements on an authentic NOAA chart (right), demonstrating the progression from basic symbol interpretation to complex multi-constraint decision-making required in professional maritime navigation*

### 数据生成管道

为支撑上述三层评估，该工作设计了一套半自动化的四阶段数据生成管道（Figure 2），将原始的 IHO S-57 矢量海图数据转化为结构化的视觉问答样本。管道各模块的输入输出关系如下：

1.  **数据渲染与解析 (Rendering & Parsing)**：以 840 张 NOAA S-57 海图为原始输入，使用 OpenCPN 在 Day/Dusk/Night 三种光照模式和六种制图尺度下进行渲染，生成多条件海图图像；同时通过 GDAL 解析矢量数据，提取 GeoJSON 格式的地理特征，并利用 IHO 查表将属性码映射为可读的语义描述。
2.  **图像配准 (Image Registration)**：在图幅上手动标注控制点，通过 Labelme 获取像素坐标，建立仿射变换矩阵，实现像素坐标与地理坐标（经纬度）之间的双向精确映射。该模块为后续空间推理任务（如坐标定位、距离测量）提供了真值计算基准。
3.  **特征标注 (Feature Annotation)**：对解析出的点、线、面特征进行可视化标注——点特征采用图染色算法分组以避免重叠，线特征标注端点，面特征使用轴对齐边界框。所有标注结果经过专家审核，确保正确性。
4.  **问题生成 (Question Generation)**：基于预定义的任务模板，将标注特征转化为 20,490 个结构化问答对。空间推理任务的真值通过航海公式（如 Haversine 距离、方位角计算）精确计算，干扰项则基于常见错误模式生成。

### 任务体系与评估指标

框架共包含 10 项具体任务，分布于三个层级：

-   **L-1 感知层**：包括符号识别、点特征理解、线特征理解、面特征理解，评估模型对 IHO S-57 标准化符号体系的视觉-语义映射能力。
-   **L-2 空间推理层**：包括坐标定位（地理坐标与像素坐标两种模态）、方位计算、距离测量，评估模型的精确空间计算能力。
-   **L-3 决策层**：包括航向判定、安全水深判定、锚地选择，评估模型在同时满足距离、水深和法规等多约束条件下的安全决策能力。

评估指标根据任务类型差异化设计：感知与决策任务采用准确率（Accuracy）；空间推理任务采用容忍度阈值下的准确率（如 Acc@20°、Acc@0.2）和平均误差（Mean Error）；坐标定位任务则分别在像素空间和地理空间下评估定位精度。

### 关键设计特征

该框架相较于现有基准的独特性在于同时覆盖了**标准化专业符号识别**、**精确地理空间推理**、**多尺度制图综合**和**多光照渲染模式**四个维度（Table 1）。这种设计使得 ENC-Bench 不仅能够评估模型的通用视觉理解能力，更能系统性地揭示其在符号基础、多约束推理和环境鲁棒性方面的根本性缺陷。

### 补充图表

![[assets/figures/papers/paper_list_l2740_https_arxiv_org_abs_2603_22763/figures/010_Figure_4.jpg]]
*Figure 4: Domain Contrast: Consumer Mapping vs. Professional Hydrography. Comparison of the same geographic region across (a) Google Maps Standard View, (b) Google Maps Satellite Imagery, and (c) NOAA Electronic Navigational Chart (ENC). While consumer maps focus on road networks and vague water representations, ENCs illustrate a complex, vector-based hydrographic reality. Note how the ENC explicitly renders critical depth contours, shipping channels, and navigational aids absent in consumer views, prioritizing safetycritical information over visual realism*

## 核心模块与公式推导

### 基准构建管线

ENC-Bench 的数据生成遵循一个半自动化的四阶段管线，将原始 IHO S-57 向量海图转化为结构化的视觉问答对（Figure 2）。该管线由以下四个关键模块构成：

![[assets/figures/papers/paper_list_l2740_https_arxiv_org_abs_2603_22763/figures/003_Figure_2.jpg]]
*Figure 2: ENC-Bench Data Generation Pipeline. Four-stage process transforms 840 NOAA S-57 charts into 20,490 validated samples: (1) Rendering & Parsing produces multi-condition images and extracts GeoJSON features; (2) Image Registration establishes pixel-togeo coordinate conversion; (3) Feature Annotation marks point/line/polygon features with expert verification; (4) Question Generation applies templates to create structured QA pairs with validated ground truth*

1. **数据渲染与解析**：使用 OpenCPN 对 840 张 NOAA S-57 海图在 Day、Dusk、Night 三种光照模式及六种制图尺度下进行渲染，生成多条件图像；同时通过 GDAL 将原始 S-57 数据解析为 GeoJSON 特征，并利用 IHO 属性查表将特征码映射为可读的语义描述。

2. **图像配准**：在每张图幅上手动标注两个控制点，通过 Labelme 获取其像素坐标，建立仿射变换矩阵，实现像素坐标与地理坐标（经纬度）之间的双向精确映射。该变换矩阵是所有空间推理任务真值计算的几何基础。

3. **特征标注**：采用图染色算法对点特征进行分组，防止视觉重叠；对线特征标注端点；对面特征使用轴对齐边界框。所有标注经专家审核以确保正确性。

4. **问题生成**：基于预设任务模板，将标注特征转化为 20,490 个结构化问答对。空间推理任务的真值通过航海公式计算得出，干扰项则基于常见错误模式生成。

### 关键公式与变量含义

#### 仿射变换

基于控制点建立的坐标转换矩阵，用于像素位置与经纬度之间的映射。该变换是坐标定位任务精度基准的核心，使得模型输出的地理坐标可被投影到像素空间进行误差评估。

#### Haversine 距离

利用球面半正矢公式计算两地理坐标点之间的大圆距离（单位为海里），用于空间推理任务（如距离测量）的真值生成。该公式考虑了地球曲率，是航海距离计算的标准方法。

#### 方位角计算

通过两点经纬度坐标差计算反正切角度，并调整至真北方向，得到 0° 至 360° 的罗盘方位。该计算是方位推断任务的真值来源。

#### 安全通过判定

$$
\mathrm{Safe} \iff D + \delta_{safety} < \min(|d_{val}|)
$$

其中：
- $D$：船舶吃水深度；
- $\delta_{safety}$：安全余量，设为 2.0 英尺；
- $d_{val}$：目标区域内所有深度探测值。

当船舶吃水加上安全余量严格小于目标区域内所有深度探测绝对值的最小值时，判定该区域可以安全通过。该公式是 L-3 决策层中安全通过任务的真值判定依据。

### 补充图表

![[assets/figures/papers/paper_list_l2740_https_arxiv_org_abs_2603_22763/figures/012_Figure_6.jpg]]
*Figure 6: Operational Lighting Modes. Demonstration of the ECDIS standardized color palettes. (a) Day Mode: High contrast with white/blue backgrounds. (b) Dusk Mode: Reduced glare with grey backgrounds. (c) Night Mode: Black background with non-linear color shifts. Note how the blue shallow water in Day mode transforms into dark grey/black tones in Night mode, and text labels shift colors to maintain visibility. This drastic “palette swapping” challenges MLLMs reliant on natural image color statistics*

## 实验与分析

### 整体性能概览：通用模型在专业海图上的能力断层

ENC-Bench 在 10 个前沿多模态大模型上的评估结果揭示了一个核心发现：**当前最先进的 MLLMs 在专业电子航海图理解上存在严重的性能瓶颈**。如表 3（平均值列）所示，表现最佳的 **Gemini-2.5-Pro** 整体准确率仅为 **47.88%**，仅比随机基线（29.76%）高出约 18 个百分点。这一结果印证了通用视觉理解与安全关键领域之间的深层鸿沟。

从三级认知层次来看，模型性能呈现明显的递减趋势：
- **L-1 感知层**：孤立符号识别（Symbol Recognition）是唯一相对可控的任务，Gemini-2.5-Pro 达到 **69.53%**（随机基线 25%），表明模型对去语境化的标准符号具有一定辨识能力。然而，当符号嵌入真实海图上下文时，点特征（Point Features）理解骤降至 42.88%（Gemini-2.5-Pro），线特征（Line Features）和面特征（Polygon Features）分别仅为 34.46% 和 30.93%（Qwen3-VL-235B-Instruct 最佳），暴露了模型在复杂视觉场景中定位和解释专业符号的根本性困难。
- **L-2 空间推理层**：距离测量是所有任务中最薄弱的环节。如表 4 所示，最佳模型 Gemini-2.5-Pro 在 20% 相对误差容忍度下的准确率（Acc@0.2）仅为 **25.67%**，而所有模型的平均相对误差均超过 40%。方位计算稍好，Qwen3-VL-235B-Thinking 在 20° 阈值下达到 55.64%，但仍远未达到实用水平。
- **L-3 决策层**：锚地选择任务中，最佳性能（Qwen3-VL-235B-Thinking，30.50%）仅勉强超过随机基线（25%），表明模型在同时优化距离、水深和法规约束时存在根本性的多约束推理缺陷。

### 符号基础瓶颈：坐标网格解读是关键断层

地理坐标定位与像素定位的对比分析（Table 10）揭示了模型性能瓶颈的精确位置。在 200px 误差阈值下，Gemini-2.5-Pro 的像素定位准确率为 21.43%，而地理坐标定位仅为 **17.36%**；当阈值收紧至 50px 时，地理坐标定位准确率在多数模型上降至 **0%**。这一显著差距表明，**对 IHO S-57 标准坐标网格符号的解读能力构成了比纯视觉定位更关键的瓶颈**——模型能够“看到”目标位置，却无法将其正确映射到经纬度坐标系。

![[assets/figures/papers/paper_list_l2740_https_arxiv_org_abs_2603_22763/figures/017_Table_10.jpg]]
*Table 10: Comparative Analysis of Coordinate Localization Modalities (Geo vs. Pixel). Accuracy at varying pixel error thresholds for Geographic (Geo) and Pixel-based (Pix) localization. Geo requires symbolic grid interpretation; Pix requires only visual localization. Bold indicates the best performance for each column*

错误分布分析（Figure 3）进一步佐证了这一发现：Gemini-2.5-Pro 的错误主要集中在需要符号推理的任务上，包括将水深数字误读为普通文本、混淆比例尺标记以及无法正确解析经纬度网格线。

![[assets/figures/papers/paper_list_l2740_https_arxiv_org_abs_2603_22763/figures/009_Figure_3.jpg]]
*Figure 3: Error distribution of Gemini-2.5-Pro’s incorrect results and example errors in its responses*

### 光照鲁棒性：颜色依赖与符号可读性的权衡

光照模式消融实验（Table 5）揭示了一个反直觉的现象：**Night 模式对感知和决策任务造成显著负面影响，却改善了空间推理任务的表现**。具体而言：
- 轨迹方向判断（Track Direction）从 Day 模式的 65.35% 下降至 Night 模式的 58.92%（-6.43%），点特征理解从 42.88% 降至 42.27%。
- 相反，地理坐标定位的平均像素误差从 Day 模式的 592.4px **减少**至 Night 模式的 490.5px（改善约 17%）。

![[assets/figures/papers/paper_list_l2740_https_arxiv_org_abs_2603_22763/figures/007_Table_5.jpg]]
*Table 5: Average model performance across lighting conditions. Delta shows change relative to day mode baseline. green indicates improvement, Red indicates degradation*

这一矛盾现象的根本原因在于 ECDIS 标准的 Night 模式采用了高对比度的单色调色板（Figure 6）：浅水区的蓝色被替换为深灰/黑色，文本标签反白显示。这种“调色板置换”削弱了模型对自然图像颜色统计的依赖，使得依赖颜色语义的感知任务（如区分不同水深区域）性能下降，却因增强了网格线和数字的对比度而意外改善了坐标读取精度。这暴露了当前视觉架构**缺乏对专业领域视觉特征的归纳偏置**——模型无法同时兼顾颜色语义判别与符号可读性。

### 尺度适应性：制图综合导致特征理解崩溃

尺度消融实验（Table 6）显示，当海图从小比例尺切换至大比例尺时，模型性能出现系统性退化：
- 线性特征理解下降 **8.6%**
- 轨迹方向判断准确率下降近 **16%**

![[assets/figures/papers/paper_list_l2740_https_arxiv_org_abs_2603_22763/figures/008_Table_6.jpg]]
*Table 6: Average model performance across scale levels. Delta shows change relative to large scale baseline. green indicates improvement, Red indicates degradation*

这一退化源于制图综合效应（Figure 7）：在大比例尺（1:50k）下，海图呈现密集的水深数字和完整的导航标志；而在小比例尺（1:200k）下，次要特征被抑制以减少视觉杂乱，水深数字大面积消失。模型无法理解“特征在逻辑上存在但视觉上消失”这一制图学基本原理，仍然基于可见特征进行推理，导致严重误判。这表明现有 MLLMs **缺乏对多尺度制图综合的适应性**，无法根据尺度变化动态调整解释策略。

### 数值精度：距离与方位的细粒度分析

细粒度阈值分析进一步量化了模型在数值推理上的精度缺陷：
- **距离测量**（Table 8）：当相对误差容忍度收紧至 5% 时，多数模型准确率低于 **9%**，即使是表现最好的 Gemini-2.5-Pro 也仅为 8.65%。这意味着模型的距离估计在绝大多数情况下存在超过 5% 的偏差，对于需要精确测量（如安全通过距离判定）的航海场景完全不可接受。
- **方位计算**（Table 9）：在 5° 严格阈值下，Qwen3-VL-235B-Thinking 的准确率仅为 21.10%，表明角度估计的精细度同样严重不足。

![[assets/figures/papers/paper_list_l2740_https_arxiv_org_abs_2603_22763/figures/015_Table_8.jpg]]
*Table 8: Fine-Grained Distance Measurement Accuracy (Acc@T). Evaluation of model performance across varying relative error tolerances. Bold indicates the best performance for each threshold*

![[assets/figures/papers/paper_list_l2740_https_arxiv_org_abs_2603_22763/figures/016_Table_9.jpg]]
*Table 9: Fine-Grained Bearing Calculation Accuracy (Acc@T). Evaluation of angular precision with error thresholds of*

这些结果表明，当前 MLLMs 的空间数值推理能力仍停留在粗略估计层面，远未达到专业导航所需的计量精度。

### 失败模式总结

综合定性案例研究（Figures 8-37，Table 11）和定量分析，模型的失败模式可归纳为五类：
1. **视觉感知错误**：在复杂背景下遗漏或误识别小尺寸导航标志。
2. **推理错误**：在需要多步逻辑链的任务中（如锚地选择）采用局部贪心策略，忽略全局约束。
3. **知识错误**：对 IHO S-57 符号语义缺乏领域知识，将专业符号与通用视觉概念混淆。
4. **计算错误**：Haversine 距离和方位角的数值计算精度极低，且无法进行单位换算。
5. **指令跟随错误**：未能严格遵循输出格式要求，尤其在坐标定位任务中频繁出现格式偏差。

### 方法谱系与知识库定位

ENC-Bench 作为首个严格遵循海事导航认知层次（感知→空间推理→决策）的专业海图理解基准，填补了现有评估体系的关键空白。与传统视觉问答基准（如 VQA-v2、GQA）和通用空间推理基准（如 SpatialVLM）相比，ENC-Bench 首次引入了 **IHO S-57 标准化向量符号体系**的评估维度，并系统性地覆盖了多尺度制图综合和多光照渲染模式两种领域特有挑战（Table 1）。其四阶段数据生成管道（Figure 2）——基于 OpenCPN 的 S-57 渲染与 GDAL 解析、控制点仿射变换配准、图染色特征标注、模板化问题生成——为专业领域的基准构建提供了可复用的方法论框架。

![[assets/figures/papers/paper_list_l2740_https_arxiv_org_abs_2603_22763/figures/002_Table_1.jpg]]
*Table 1: Comparison of ENC-Bench with existing benchmarks. ✓, ▲, and ✗separately represent full support (supports the core capability), partial support (e.g., informal/math symbols, Euclidean/layout reasoning, or multi-resolution), and no support*

在评估的 10 个模型中，商用闭源模型（**Gemini-2.5-Pro**、**GPT-4o**）在多数任务上领先开源模型，但差距并不悬殊；开源模型中 **Qwen3-VL-235B-Thinking** 在方位计算和锚地选择任务上甚至超越了所有闭源模型，表明推理增强策略对空间决策任务具有特殊价值。然而，所有模型在核心瓶颈（坐标网格解读、多约束优化、尺度适应性）上均表现不佳，说明仅靠模型规模扩展或推理链增强无法根本解决领域特异性缺陷。

### 关键局限与评估公平性说明

在解读上述结果时，需注意以下评估边界：
- **地理偏差**：数据集仅基于美国 NOAA 海图，尽管遵循 IHO S-57 国际标准，但不同水文机构的制图实践存在差异，且未包含商业航运使用的 S-63 加密格式，结论向非美国水域的推广需谨慎。
- **静态评估**：基准采用静态视觉问答范式，未评估时间序列推理（如动态避碰）或传感器融合（雷达、AIS）能力，无法反映实时导航场景的完整需求。
- **决策简化**：L-3 决策任务基于封闭式选项和显式视觉线索，真实操作中需考虑的天气、潮汐窗口、值班指令等隐性约束未被建模。
- **零样本局限**：所有评估均基于通用 MLLMs 的零样本能力，未探索在海图数据上进行指令微调或领域预训练的潜力，可能低估了领域适配后的性能上限。
- **安全误导风险**：当前模型在专业视觉任务上的表现不足，若在无适当不确定性量化和人机回环机制的情况下部署于实际导航辅助，可能引发自动化偏见，导致灾难性后果。

### 补充图表

![[assets/figures/papers/paper_list_l2740_https_arxiv_org_abs_2603_22763/figures/005_Table_3.jpg]]
*Table 3: Performance on Perception and Decision-Making tasks. Results in accuracy (%). Bold indicates best performance*

## 方法谱系与知识库定位

### 与现有基准的关系：填补专业海图理解的系统性空白

在 ENC-Bench 之前，多模态大语言模型（MLLMs）的视觉理解基准主要集中在自然图像、文档图表或通用地图场景。**Table 1** 的系统对比揭示了 ENC-Bench 在四个关键维度上的独创性：

- **标准化符号识别**：现有基准如 **MM-Vet**、**MMBench** 仅支持非正式或数学符号，而 ENC-Bench 要求模型识别符合 IHO S-57 国际标准的专业航海符号体系，包括点状复合符号（如灯塔、沉船标记）、线状边界特征（如管道、分道通航线）和面状区域规则（如禁止锚泊区、未完全测量区），这些符号的细微视觉差异承载着重大的安全语义权重（见 **Figure 5**）。
- **精确地理空间推理**：不同于 **SpatialBench**、**BLINK** 等基准的欧氏距离或布局推理，ENC-Bench 要求模型在海图图像上进行基于球面半正矢公式的真北方位计算和海里距离测量，并评估像素坐标与地理坐标的双向转换能力。
- **多尺度与多光照条件**：现有基准普遍缺乏对制图综合（cartographic generalization）和 ECDIS 标准光照模式（Day/Dusk/Night）的系统覆盖，ENC-Bench 首次将这两种专业操作条件纳入评估框架。

这种定位使 ENC-Bench 成为连接通用视觉理解与安全关键领域（safety-critical domain）的桥头堡：它不是对已有能力的增量扩展，而是揭示了一个现有基准完全未触及的能力断层。

### 被评估模型谱系：通用 MLLMs 的零样本边界

论文评估了 10 个当前最先进的 MLLMs，覆盖商用闭源与开源两大阵营：

- **商用闭源模型**：GPT-4o、Gemini-2.5-Pro、Gemini-2.5-Flash
- **开源模型**：Qwen3-VL 系列（235B/32B 的 Instruct 和 Thinking 变体）、GLM-4.5V、InternVL-3-38B、Llama-4-Maverick-17B

所有评估均基于**零样本设定**，未进行任何领域微调或提示工程优化。这一设计选择具有双重意义：一方面，它严格测量了通用 MLLMs 向专业领域迁移的“裸”能力上限；另一方面，它也构成了该基准的核心局限——可能低估了领域适配后的潜力（见下文“局限与开放问题”）。

### 适用边界：基准设计的显式与隐式约束

ENC-Bench 的结论适用性受以下设计边界约束：

1. **地理与来源偏差**：数据集仅源自美国 NOAA 发布的 840 张 S-57 海图。尽管遵循 IHO S-57 国际标准，不同水文机构（如英国 UKHO）的制图实践、符号渲染风格和特征密度存在差异。此外，商业航运中广泛使用的 S-63 加密格式未被覆盖，结论向非美国水域和加密海图的推广需谨慎。

2. **静态快照评估**：基准采用静态视觉问答范式，所有样本均为单一时刻的海图渲染图像。这意味着它无法评估：
   - 动态时序推理（如随时间演化的碰撞避免决策）
   - 多传感器融合（如雷达回波、AIS 船舶自动识别系统数据与海图信息的联合解读）
   
   这些能力对于真实导航场景中的态势感知（situation awareness）至关重要，但完全处于当前评估框架之外。

3. **决策空间的简化**：L-3 决策任务（航向判断、安全通过判定、锚地选择）基于封闭式选项和显式视觉线索。真实航海操作中，决策需同时考虑天气窗口、潮汐预报、值班指令、船舶操纵特性等未在海图上直接呈现的隐性约束。当前基准测量的是“图表可读条件下的最优选择”，而非“真实操作环境下的鲁棒决策”。

4. **安全误导风险**：论文明确指出，当前最佳模型在整体准确率上仅达 47.88%（**Table 3**），仅略超随机基线（29.76%）。在锚地选择等安全关键任务中，最佳性能（30.50%）勉强超过随机猜测（25%）。若此类模型在缺乏适当不确定性量化和人机回环（human-in-the-loop）机制的情况下被用于实际导航辅助，可能引发自动化偏见（automation bias），导致灾难性后果。

### 核心局限与开放问题

基于分析证据，以下局限与开放问题值得后续工作关注：

**局限 1：符号基础（symbol grounding）的根本性断裂**

**Table 10** 的证据表明，地理坐标定位（Geo）准确率显著低于直接像素定位（Pixel）——Gemini-2.5-Pro 在 Acc@200px 下 Geo 仅 17.36% vs Pixel 21.43%，在严格阈值 Acc@50px 下 Geo 多为 0%。这说明模型并非无法“看到”目标，而是无法正确解读坐标网格符号体系。这一符号基础瓶颈是当前 MLLMs 视觉架构缺乏对专业制图符号归纳偏置的直接体现。

**局限 2：多约束推理的能力真空**

在需要同时优化距离、水深和法规约束的锚地选择任务中（**Table 3** Anchorage Selection），最佳模型仅 30.50%，与随机基线（25%）的差距极小。这表明模型倾向于局部贪心优化，缺乏对全局约束的显式枚举与验证机制。论文未探索引入显式符号规则引擎（如约束求解器）作为 MLLMs 补充的混合架构。

**局限 3：光照鲁棒性与颜色依赖的冲突**

**Table 5** 的消融实验揭示了一个反直觉现象：Night 模式导致感知与决策任务平均下降最高达 6%（如 Track Direction 下降 6.43%），但空间推理任务（如坐标定位）的误差反而减少（Day 592.4px vs Night 490.5px，改善约 17%）。这一“跷跷板效应”表明：感知任务依赖颜色语义判别，而 Night 模式的高对比度单色渲染有利于符号可读性。现有视觉架构无法同时优化这两类需求。

**局限 4：尺度泛化的脆弱性**

**Table 6** 显示，小尺度（1:200k 以上）造成线性特征理解下降 8.6%、Track Direction 准确率下降近 16%。制图综合导致部分特征在视觉上“消失”但逻辑上仍存在，模型缺乏根据尺度调整解释策略的元认知能力。

**开放问题**：

1. 如何设计针对坐标网格符号解读的训练或提示策略，以缓解符号基础瓶颈？是否需要在预训练阶段融入制图先验（如比例尺条识别、等深线解析）？
2. 领域指令微调能否将模型性能提升至可接受的专业水平？所需的数据规模、多样性和标注策略是什么？
3. 模型在不同海洋区域（非美国水域）和不同海图格式（如 S-63 加密格式）上的泛化能力如何？
4. 是否需要引入显式的多约束求解模块作为 MLLMs 的补充，以保障安全关键决策的可靠性？混合架构（神经符号方法）在该领域的可行性值得探索。
5. 如何将实时动态信息（AIS、雷达）与静态 ENC 解释结合，构建面向自主驾驶导航的端到端评估基准？这需要从静态 VQA 范式向时序多模态推理范式演进。

## 原文 PDF

![[paperPDFs/CVPR_2026/ENC_Bench_A_Benchmark_for_Evaluating_Multimodal_Large_Language_Models_in_Electronic_Navigational_Chart_Understanding.pdf]]
