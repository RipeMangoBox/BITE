---
title: "Keep it SymPL: Symbolic Projective Layout for Allocentric Spatial Reasoning in Vision-Language Models"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/Keep_it_SymPL_Symbolic_Projective_Layout_for_Allocentric_Spatial_Reasoning_in_Vision_Language_Models.pdf
project_link: null
code_link: null
aliases:
- SSPL
- KISSPLASRVLM
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
core_operator: 将异中心问题重构为符号布局问题——通过投影、抽象、二分区和定位四个因子，将复杂的空间关系推理转化为 VLM 擅长的颜色区域定位。
primary_logic: 避免让 VLM 直接进行视点变换，而是将空间关系编码为 2D 正交投影平面上的颜色分区抽象符号布局，利用 VLM 对简化视觉线索和位置判断的强项，间接完成异中心推理。
claims:
- "在 COMFORT# allocentric 测试中，SymPL 在所有类别上均大幅领先此前最佳方法，尤其是 closer 类别 (97.33% vs. 84.25%)，提升超过 13 个百分点。"
- SymPL 同样将自我中心空间推理推至最高水平，COCOSPATIAL left/right 89.83%，above/below 94.33%，证明方法对多视角推理一致有效。
- "COMFORT# (allocentric) 上 left/right 准确率 = 69.00%"
- "COMFORT# (allocentric) 上 closer 准确率 = 97.33%"
---

# Keep it SymPL: Symbolic Projective Layout for Allocentric Spatial Reasoning in Vision-Language Models

> [!tip] 核心洞察
> 避免让 VLM 直接进行视点变换，而是将空间关系编码为 2D 正交投影平面上的颜色分区抽象符号布局，利用 VLM 对简化视觉线索和位置判断的强项，间接完成异中心推理。

| 字段 | 内容 |
|------|------|
| 中文题名 | 保持 SymPL：视觉语言模型中异中心空间推理的符号投影布局 |
| 英文题名 | Keep it SymPL: Symbolic Projective Layout for Allocentric Spatial Reasoning in Vision-Language Models |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2602.19117) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction |
| Method | SymPL (Symbolic Projective Layout) |
| Dataset | COMFORT#, 3DSRBench, COCOSPATIAL |

> [!tip] 效果简介
> - COMFORT# (allocentric) 上，left/right 准确率 69.00% vs 49.83% (GPT-5) (+19.17%)；closer 准确率 97.33% vs 84.25% (GPT-5) (+13.08%)；visibility 准确率 91.41% vs 64.10% (Gemini-2.5-Flash) (+27.31%)。
> - 3DSRBench (allocentric) 上，left/right 准确率 79.94% vs 77.94% (APC-Num) (+2.00%)。
> - COCOSPATIAL (egocentric) 上，left/right 准确率 89.83% vs – (–)。

## 概述

视觉语言模型（VLM）在空间推理任务中展现出巨大潜力，但现有研究主要聚焦于以观察者自身为参照的**自我中心**（egocentric）视角。在许多实际应用——如机器人导航、增强现实和多智能体协作——中，系统需要从外部观察者或对象的视角理解空间关系，即**异中心**（allocentric）空间推理。然而，当前 VLM 在以对象为中心的异中心视角下存在强烈的自我中心偏置，难以执行视点变换，导致空间推理性能大幅下降。

针对这一瓶颈，本文提出 **SymPL（Symbolic Projective Layout，符号投影布局）**，一种将异中心空间推理重构为符号布局问题的新范式。其核心洞察是：避免让 VLM 直接进行视点变换，而是将复杂的空间关系编码为 2D 正交投影平面上的颜色分区抽象符号布局，利用 VLM 对简化视觉线索和位置判断的强项，间接完成异中心推理。SymPL 通过四个关键因子——**投影**（Projection）、**抽象**（Abstraction）、**二分区**（Bipartition）和**定位**（Localization）——将原始异中心问题转化为“目标对象位于哪种颜色区域”的定位问题，使通用 VLM 无需任何微调即可有效回答。

实验结果表明，SymPL 在多个基准测试上全面超越此前最佳方法：在 COMFORT# 异中心测试中，left/right 准确率达 **69.00%**（较 GPT-5 提升 19.17 个百分点），closer 准确率达 **97.33%**（提升 13.08 个百分点），visibility 和 facing 类别分别领先最强基线 27.31 和 19.25 个百分点。此外，SymPL 在自我中心空间推理的 COCOSPATIAL 基准上也达到最高水平（left/right 89.83%，above/below 94.33%），证明了该方法对多视角推理的一致有效性。

## 背景与动机

空间推理是视觉语言模型（VLM）走向具身智能与复杂场景理解的核心能力之一。然而，现有 VLM 在空间推理上存在一个关键瓶颈：**模型在以对象为中心的异中心（allocentric）视角下表现出强烈的自我中心（egocentric）偏置**。换言之，当要求模型从场景中某个参考对象（如一个人）的视角出发，判断其他对象的相对方位、距离、可见性或朝向时，VLM 往往无法正确执行视点变换（viewpoint transformation），导致推理性能大幅下降。

这一缺陷的根源在于，VLM 的训练数据天然以相机视角（即自我中心视角）为主，模型缺乏从“他人”视角理解空间关系的内在机制。直接让 VLM 进行视点变换——即将自我中心观测映射为异中心关系——是一项极其困难的任务，现有方法对此收效甚微。

现有工作可大致归为三类：（1）**通用 VLM**，如 GPT-5（OpenAI, 2025）、Gemini-2.5-Flash（Comanici et al., 2025）、Qwen2.5-VL 等，在异中心空间推理上表现有限；（2）**推理辅助方法**，如 CoT（Kojima et al., NeurIPS 2022）、SoM（Yang et al., 2023）、SCAFFOLD（Lei et al., COLING 2024），通过链式思维或视觉标记增强推理，但并未从本质上解决视点变换问题；（3）**专用空间推理模型**，如 SpatialVLM（Chen et al., NeurIPS 2024）、SpatialRGPT（Cheng et al., NeurIPS 2024）等专注于自我中心推理，而 SAT（Ray et al., COLM 2025）、APC-Num 和 APC-Vis（Lee et al., ICCV 2025）虽面向异中心场景，但性能仍有较大提升空间。

本文的核心动机在于：**与其强迫 VLM 学会视点变换，不如将异中心推理问题重构为 VLM 擅长的任务**。具体而言，SymPL 将复杂的空间关系推理转化为一个**符号布局（symbolic layout）问题**——通过正交投影将 3D 场景映射为 2D 平面，将对象抽象为无特征彩色圆形，利用线性或圆形边界对空间进行二分区着色，最终将原始的空间关系查询转化为“目标对象位于哪种颜色区域”的定位问题。这一策略绕开了 VLM 的视点变换短板，转而利用其在简化视觉线索和位置判断上的强项，从而在异中心空间推理上取得显著突破。

## 核心创新

### 问题瓶颈：异中心空间推理中的自我中心偏置

视觉语言模型（VLM）在执行以对象为中心的异中心（allocentric）空间推理时存在根本性缺陷：它们天然倾向于从自身视角（自我中心视角）理解空间关系，难以执行视点变换（perspective-taking）。当问题要求模型站在场景中某个参考观察者的角度判断“左边/右边”、“更近/更远”、“可见/不可见”、“面对/背对”时，通用 VLM 的性能急剧下降——例如，在 COMFORT# 异中心 left/right 测试中，表现最佳的通用模型 GPT-5（OpenAI, 2025）也仅达到 49.83% 的准确率，近乎随机猜测水平。

### 核心洞察：将视点变换问题转化为符号布局定位问题

SymPL 的核心创新在于**避免让 VLM 直接执行视点变换**。传统方法试图让 VLM 理解复杂的 3D 空间关系并自主完成视角转换，但 VLM 对此类抽象推理并不擅长。SymPL 的洞察是：VLM 对简化视觉线索和位置判断具有较强能力。因此，该方法将异中心空间关系**编码为 2D 正交投影平面上的颜色分区抽象符号布局**，将“对象 A 在观察者的左边吗？”这类空间关系问题转化为“目标对象位于哪种颜色区域？”的定位问题——这正是 VLM 擅长的任务。

### Changed Slots：两处关键设计变更

与直接端到端推理的基线方法相比，SymPL 在两个关键维度上进行了根本性重构：

| 变更维度 | 基线方法 | SymPL 方法 |
|---------|---------|-----------|
| **输入问题格式** | 原始异中心自然语言问题（直接输入 VLM） | 符号布局问题：包含颜色分区、抽象符号的正交投影 2D 图像 + 转化为颜色区域定位的文本 prompt |
| **推理流水线** | 端到端 VLM 单步推理 | 两阶段流水线：空间信息提取（目标检测+深度估计+朝向估计）→ 问题重构（投影→抽象→二分区→定位）→ VLM 推理 |

这两处变更使得 SymPL 可以作为一种**即插即用的输入预处理策略**，应用于任意 VLM 而不修改模型参数，保持与基线模型推理能力的一致性比较。

### 四大关键因子：将空间推理系统化分解

SymPL 通过四个关键因子将复杂的异中心空间推理系统化分解为 VLM 可处理的形式：

1. **投影（Projection）**：根据推理类别选择俯视或前视正交投影，将 3D 坐标映射到 2D 平面。例如，left/right 和 closer 采用俯视图，above/below 采用前视图。这一步将 3D 视点变换简化为 2D 几何关系。

2. **抽象（Abstraction）**：将对象统一抽象为无特征的纯色圆形，仅通过颜色区分不同对象。这一步消除了视觉外观对推理的干扰，迫使模型仅关注位置信息。

3. **二分区（Bipartition）**：根据空间推理类别使用线性或圆形边界将空间二分区。方向比较（left/right、facing）采用线性分区，距离比较（closer）采用圆形分区。这一步将连续的空间关系离散化为“区域 A vs 区域 B”的二选一问题。

4. **定位（Localization）**：将分区区域填充不同颜色，把空间关系问题转化为“目标对象位于哪种颜色区域”的定位问题。这一步将 VLM 不擅长的关系推理转化为其擅长的视觉定位任务。

消融实验（Table 5）强有力地验证了这一设计的有效性：当四个因子逐步加入时，五项通用 VLM 的平均成功率在每个类别上均稳步提升；在完整配置（Setting 5）下，所有类别均达到 100% 的成功率。

### 方法谱系与知识库定位

SymPL 处于空间推理与 VLM 推理增强的交叉领域，其定位如下：

- **通用 VLM**：LLaVA-NeXT（Liu et al., 2024）、LLaVA-OneVision（Li et al., 2024）、Molmo（Deitke et al., CVPR 2025）、Qwen2.5-VL、Cambrian-1（Tong et al., NeurIPS 2024）、GPT-5（OpenAI, 2025）、Gemini-2.5-Flash（Comanici et al., 2025）在异中心空间推理上均表现不佳，暴露了端到端 VLM 在视点变换上的固有局限。

- **推理辅助方法**：Qwen2.5-VL + CoT（Kojima et al., NeurIPS 2022）、Qwen2.5-VL + SoM（Yang et al., 2023）、Qwen2.5-VL + SCAFFOLD（Lei et al., COLING 2024）通过思维链或视觉标记增强推理，但未针对异中心视角进行专门设计，提升有限。

- **自我中心空间推理专用模型**：SpatialVLM（Chen et al., NeurIPS 2024）、SpatialRGPT（Cheng et al., NeurIPS 2024）、SpatialBot、SD-VLM（Yang et al., NeurIPS 2025）专注于自我中心视角的空间理解，但无法有效处理异中心问题。

- **异中心空间推理专用模型**：SAT（Ray et al., COLM 2025）、APC-Num 和 APC-Vis（Lee et al., ICCV 2025）直接针对异中心推理设计，但 SymPL 在所有类别上均显著超越这些方法（如 COMFORT# closer：97.33% vs. APC-Vis 84.25%，提升超过 13 个百分点）。

SymPL 的独特贡献在于：它不试图让 VLM “学会”视点变换，而是通过符号布局重构**绕过**这一困难，将问题转化为 VLM 已有的能力范畴。这种“问题重构”范式为 VLM 的空间推理能力扩展提供了新的思路。

## 整体框架

SymPL 的核心思想是将视觉语言模型（VLM）难以直接处理的异中心空间推理问题，重构为 VLM 擅长的符号布局定位问题。整个框架由**两阶段流水线**构成：空间信息提取与问题重构，后者通过**投影、抽象、二分区、定位**四个关键因子逐步将原始场景转化为简化的颜色分区布局。

### 两阶段流水线

**阶段一：空间信息提取**

给定输入图像 $I$ 和包含参考观察者与目标对象的自然语言问题，SymPL 首先从问题中提取对象集合 $O = \{ o _ { r } , o _ { i } \mid i = 1 , 2 , \ldots , n \}$，其中 $o_r$ 为参考观察者，$o_i$ 为目标对象。随后利用 GroundingDINO 检测所有对象的边界框 $B = \left\{ b _ { r } , b _ { i } \mid i = 1 , 2 , \ldots , n \right\}$，并通过 Depth-Pro 估计深度图。将各边界框内的深度点反投影至三维空间后取中值，得到每个对象的三维坐标 $p _ { j } = ( x _ { j } , y _ { j } , z _ { j } )$。对于参考观察者，额外裁剪其边界框区域并送入 OrientAnything，获取其三维朝向向量 $v_r$。至此，所有空间信息被组织为集合 $U = \{ v _ { r } , p _ { r } , p _ { i } \mid i = 1 , 2 , \ldots , n \}$，作为后续问题重构的输入。

**阶段二：问题重构**

问题重构阶段依次应用四个关键因子，将空间关系推理转化为颜色区域定位任务：

1. **投影（Projection）**：根据空间推理类别选择正交投影视角——平面关系（如 left/right、closer）采用俯视投影，高度关系（如 above/below）采用前视投影——将三维坐标映射到二维平面。
2. **抽象（Abstraction）**：将所有对象统一为无特征的圆形，仅通过不同颜色区分各对象，消除视觉细节对推理的干扰。
3. **二分区（Bipartition）**：依据推理类别选择分区方式——方向比较采用线性边界，距离比较采用圆形边界——将投影平面划分为两个区域。
4. **定位（Localization）**：将两个分区填充不同颜色，使原始空间关系问题转化为“目标对象位于哪种颜色区域”的位置判断问题。

经过上述变换，VLM 无需执行视点变换或复杂的三维推理，仅需在高度简化的符号布局图像上完成颜色区域定位即可得出答案。该流水线作为纯输入预处理方法，不修改 VLM 参数，可适配任意 VLM 模型。

### 关键依赖与误差传播

流水线的性能高度依赖外部预训练模块的精度。其中，参考观察者的朝向估计（OrientAnything）是当前最主要的误差来源——朝向向量估计不准会直接导致投影坐标系偏移，使后续分区和定位全部失效。此外，目标检测（GroundingDINO）和深度估计（Depth-Pro）的误差同样会沿流水线传播，影响最终推理结果。

### 补充图表

![[assets/figures/papers/paper_list_l2398_https_arxiv_org_abs_2602_19117/figures/002_Figure_2.jpg]]
*Figure 2: Overview of SymPL framework. SymPL reformulates an allocentric question into a symbolic-layout question through two stages: 1) Spatial Information Extraction and 2) Question Reformulation using four key factors — projection, abstraction, bipartition, and localization*

![[assets/figures/papers/paper_list_l2398_https_arxiv_org_abs_2602_19117/figures/001_Figure_1.jpg]]
*Figure 1: SymPL reformulates allocentric questions into symboliclayout questions using four factors-projection, abstraction, bipartition, and localization-enabling significantly improved spatial reasoning under allocentric settings*

## 核心模块与公式推导

SymPL 的核心思想是将异中心空间推理问题重构为符号布局问题，其推理流水线由两个阶段、四个关键因子构成。以下按模块顺序展开，并给出关键公式定义。

### 空间信息提取阶段

该阶段的目标是从输入图像和自然语言问题中提取用于后续符号布局生成的三维信息集合 $U$。

**对象识别与检测**：首先，VLM 从问题 prompt 中提取所有对象名称，构成对象集合：

$$O = \{ o_{r}, o_{i} \mid i = 1, 2, \ldots, n \}$$

其中 $o_r$ 为参考观察者，$o_i$ 为目标对象。随后，使用 GroundingDINO 对图像进行目标检测，得到对应的边界框集合：

$$B = \left\{ b_{r}, b_{i} \mid i = 1, 2, \ldots, n \right\}$$

**深度估计与 3D 反投影**：利用 Depth-Pro 估计输入图像的深度图 $D$。对于每个对象的边界框区域，将该区域内的像素点通过深度信息反投影至三维空间，取坐标中值作为该对象的 3D 位置：

$$p_{j} = (x_{j}, y_{j}, z_{j})$$

其中 $p_j$ 表示对象 $j$（参考观察者或目标对象）的三维坐标。

**朝向估计**：根据参考观察者的边界框 $b_r$ 裁剪图像区域，输入 OrientAnything 模型，估计参考观察者的三维朝向向量 $v_r$。

最终，空间信息提取阶段输出一个完整的三维信息集合 $U$：

$$U = \{ v_{r}, p_{r}, p_{i} \mid i = 1, 2, \ldots, n \}$$

该集合包含参考观察者的朝向向量 $v_r$、参考观察者的位置 $p_r$ 以及所有目标对象的位置 $p_i$，作为问题重构阶段的输入。

### 问题重构阶段

问题重构阶段通过四个关键因子，将三维空间关系转化为 VLM 擅长的颜色区域定位问题。

**投影因子**：根据空间推理类别选择外部视角。对于平面上的关系（如 left/right、closer），采用俯视正交投影；对于高度相关的关系（如 above/below），采用前视正交投影。该步骤将每个对象的 3D 坐标映射到 2D 平面坐标。

**抽象因子**：将投影后的对象统一抽象为无特征的圆形，仅通过唯一颜色区分不同对象。这一设计消除了外观细节对 VLM 的干扰，使其聚焦于位置关系。

**二分区因子**：根据空间推理类别确定分区形式。方向比较（如 left/right、facing）采用线性边界将平面二分为两个区域；距离比较（如 closer）采用圆形边界将平面分为内部和外部两个区域。分区区域填充不同颜色。

**定位因子**：将原始的空间关系问题转化为“目标对象位于哪种颜色区域”的定位问题。例如，“object A 是否位于 reference 的左侧”被重构为“object A 的符号是否位于红色区域内”。这一转化使 VLM 无需执行显式的视点变换，而只需利用其固有的颜色区域定位能力即可完成推理。

### 补充图表

![[assets/figures/papers/paper_list_l2398_https_arxiv_org_abs_2602_19117/figures/003_Figure_3.jpg]]
*Figure 3: Partition rule based on spatial reasoning category. Directional comparisons adopt a linear partition, while distance comparisons employ a circular one*

## 实验与分析

### 核心瓶颈与设计动机

视觉语言模型在以对象为中心的异中心视角下存在强烈的自我中心偏置。当要求模型从场景中某个对象的视角判断空间关系时，模型难以执行视点变换，导致性能大幅下降。SymPL 的核心洞察在于：**避免让 VLM 直接进行视点变换，而是将空间关系编码为 2D 正交投影平面上的颜色分区抽象符号布局**，利用 VLM 对简化视觉线索和位置判断的强项，间接完成异中心推理。

### 主实验结果

#### 异中心空间推理

Table 1 报告了在 COMFORT# 和 3DSRBench 两个异中心基准上的全面对比。SymPL 在所有类别上均大幅领先此前最佳方法：

![[assets/figures/papers/paper_list_l2398_https_arxiv_org_abs_2602_19117/figures/004_Table_1.jpg]]
*Table 1: Quantitative results on allocentric questions. Bold indicates the best, while underline represents the second best results*

- **COMFORT# left/right**：SymPL 达到 69.00%，相较于最强通用 VLM **GPT-5**（OpenAI, 2025）的 49.83% 提升 19.17 个百分点。该类别涉及视点变换下的左右判断，是异中心推理中最具挑战性的子任务。
- **COMFORT# closer**：SymPL 达到 97.33%，较 **GPT-5** 的 84.25% 提升 13.08 个百分点，几乎解决了距离比较问题。
- **COMFORT# visibility**：SymPL 达到 91.41%，较 **Gemini-2.5-Flash**（Comanici et al., 2025）的 64.10% 提升 27.31 个百分点。
- **COMFORT# facing**：SymPL 达到 91.50%，较 **Gemini-2.5-Flash** 的 72.25% 提升 19.25 个百分点。
- **3DSRBench left/right**：SymPL 达到 79.94%，略优于专用异中心方法 **APC-Num**（Lee et al., ICCV 2025）的 77.94%。

值得注意的是，通用 VLM 在异中心问题上表现普遍不佳。以 **Qwen2.5-VL** 为例，其在 COMFORT# left/right 上仅 36.25%，closer 上 47.00%，远低于随机猜测水平。即使辅以 **CoT**（Kojima et al., NeurIPS 2022）、**SoM**（Yang et al., 2023）或 **SCAFFOLD**（Lei et al., COLING 2024）等推理辅助方法，提升也十分有限。专用自我中心方法如 **SpatialVLM**（Chen et al., NeurIPS 2024）和 **SpatialRGPT**（Cheng et al., NeurIPS 2024）在异中心设定下同样表现不佳。这验证了异中心空间推理对现有 VLM 构成了系统性挑战，而非个别模型的缺陷。

#### 自我中心空间推理

Table 2 展示了 SymPL 在 COCOSPATIAL 自我中心基准上的结果。SymPL 在 left/right 上达到 89.83%，above/below 上达到 94.33%，均达到最高水平。这证明符号布局方法对多视角推理具有一致有效性——将空间关系转化为颜色区域定位的策略在自我中心设定下同样高效。

![[assets/figures/papers/paper_list_l2398_https_arxiv_org_abs_2602_19117/figures/006_Table_2.jpg]]
*Table 2: Quantitative results on egocentric questions. Bold indicates the best, while underline represents the second best results*

#### 视角感知推理与多视角一致性

Table 3 报告了视觉错觉下的视角感知推理鲁棒性测试，Table 4 报告了多视角一致性测试。两项测试中 SymPL 均取得最优结果，表明符号布局不仅提升了单次推理准确率，还增强了模型在不同视角下回答的稳定性和一致性。

![[assets/figures/papers/paper_list_l2398_https_arxiv_org_abs_2602_19117/figures/007_Table_3.jpg]]
*Table 3: Quantitative results on perspective-aware reasoning under visual illusions. Bold indicates the best, while underline represents the second best results*

![[assets/figures/papers/paper_list_l2398_https_arxiv_org_abs_2602_19117/figures/008_Table_4.jpg]]
*Table 4: Quantitative results on viewpoint-aware consistency across multiple views. Bold indicates the best, while underline represents the second best results*

### 消融实验

#### 四因子逐步消融

Table 5 展示了在五项通用 VLM 上逐步加入投影、抽象、二分区、定位四个因子的平均成功率变化。结果清晰揭示了每个因子的累积贡献：

![[assets/figures/papers/paper_list_l2398_https_arxiv_org_abs_2602_19117/figures/011_Table_5.jpg]]
*Table 5: Ablation results on the effectiveness of four key factors: Projection, Abstraction, Bipartition, and Localization. Results show the average success rate of five general-purpose VLMs for each category: left/right, closer, visibility, and facing*

- **Setting 1（原始问题）**：所有类别成功率极低，left/right 仅约 30%，closer 约 50%。
- **Setting 2（+投影）**：加入正交投影后，left/right 提升至约 55%，closer 提升至约 75%，验证了视点外化对异中心推理的关键作用。
- **Setting 3（+抽象）**：将对象抽象为单色圆形后，各类别进一步提升 5-10 个百分点，说明去除视觉干扰有助于 VLM 聚焦空间关系。
- **Setting 4（+二分区）**：引入线性/圆形分区边界后，visibility 和 facing 类别获得显著提升（约 15 个百分点），证明显式空间划分有效降低了关系判断的歧义。
- **Setting 5（+定位，完整 SymPL）**：将所有类别统一转化为颜色区域定位问题后，五项 VLM 的**平均成功率在所有类别上均达到 100%**。

#### 投影视角的影响

Figure 5a 的消融显示，投影因子的俯视/前视选择对性能有显著影响。例如，above/below 推理在接近俯视视角时准确率下降，因为俯视投影丢失了高度信息。SymPL 采用的分类别视角选择策略（平面关系用俯视，高度关系用前视）是性能最优配置。

### 错误分析

Figure 6 的错误分解揭示了当前流水线的主要失败模式：**最频繁的错误来源是参考观察者朝向估计不准**。OrientAnything 模块输出的朝向向量 $v_r$ 若存在偏差，将导致后续投影和分区步骤中空间关系映射完全错误，错误传播至最终推理结果。

此外，流水线依赖多个外部预训练模型——**GroundingDINO** 的目标检测、**Depth-Pro** 的深度估计、**OrientAnything** 的朝向估计——任一模块的不精确或失败都会直接影响 SymPL 的输出。特别是在 3DSRBench visibility 和 facing 类别上 SymPL 的优势相对有限（分别领先约 2 和 4 个百分点），部分可归因于这些模块在复杂场景下的累积误差。

### 公平性说明

实验设计具有较高的公平性：比较涵盖通用 VLM、推理辅助方法、自我中心/异中心专用模型共 17 个基线，并在多个标准 benchmark 上评估。SymPL 的符号布局变换仅为输入预处理，不修改 VLM 参数，因此可应用于任意 VLM，保持与基线模型推理能力的一致性比较。所有实验均使用公开数据集（COMFORT#、3DSRBench、COCOSPATIAL 等），结果具备可复现性。

### 补充图表

![[assets/figures/papers/paper_list_l2398_https_arxiv_org_abs_2602_19117/figures/009_Figure_5.jpg]]
*Figure 5: Ablation results of each key factor. (a) projection, (b) abstraction, (c) bipartition, (d) localization. The darker bar indicates the configuration used in SymPL*

## 方法谱系与知识库定位

### 1 问题定位：从自我中心偏置到符号化视点解耦

视觉语言模型（VLM）在以对象为中心的异中心（allocentric）空间推理中暴露出一个核心瓶颈：模型天然倾向于从观察者视角（自我中心）理解空间关系，难以执行视点变换。当问题要求“站在场景中某个对象的视角判断左右”时，VLM 必须隐式地完成坐标系旋转与关系重映射，而这一过程对当前通用 VLM 而言是显著的能力短板。实验证据表明，即使是最先进的 **GPT-5**（OpenAI, 2025）在 COMFORT# 异中心 left/right 测试中也仅取得 49.83% 的准确率，接近随机猜测水平。

SymPL 的解题思路是将这一瓶颈从“隐式视点变换”转化为“显式符号布局”，其核心洞察在于：避免让 VLM 直接进行视点变换，而是将空间关系编码为 2D 正交投影平面上的颜色分区抽象符号布局，利用 VLM 对简化视觉线索和位置判断的强项，间接完成异中心推理。

### 2 方法谱系中的定位

SymPL 处于三个研究脉络的交汇点：

**通用 VLM 的零样本推理。** 包括 **LLaVA-NeXT**（Liu et al., 2024）、**LLaVA-OneVision**（Li et al., 2024）、**Molmo**（Deitke et al., CVPR 2025）、**Qwen2.5-VL**、**Cambrian-1**（Tong et al., NeurIPS 2024）、**GPT-5**（OpenAI, 2025）和 **Gemini-2.5-Flash**（Comanici et al., 2025）在内的通用 VLM 均以端到端方式直接处理异中心问题，未引入任何空间先验或中间表示。SymPL 的实验表明，这些模型在异中心任务上普遍表现不佳，验证了“纯端到端”路径在此类问题上的根本性局限。

**推理辅助方法。** 以 **Qwen2.5-VL + CoT**（Kojima et al., NeurIPS 2022）、**Qwen2.5-VL + SoM**（Yang et al., 2023）和 **Qwen2.5-VL + SCAFFOLD**（Lei et al., COLING 2024）为代表的推理增强策略，试图通过思维链提示或视觉标记叠加来辅助空间推理。但这些方法仍将视点变换的认知负担留在 VLM 内部，因此提升幅度有限——它们改善的是推理过程的显式化程度，而非问题本身的表征形式。

**专用空间推理模型。** 自我中心空间推理领域已有 **SpatialVLM**（Chen et al., NeurIPS 2024）、**SpatialRGPT**（Cheng et al., NeurIPS 2024）、**SpatialBot** 和 **SD-VLM**（Yang et al., NeurIPS 2025）等工作，它们通过度量空间监督或区域图编码来增强自我中心视角下的空间理解。异中心推理方面，**SAT**（Ray et al., COLM 2025）和 **APC-Num / APC-Vis**（Lee et al., ICCV 2025）分别从视角感知提示和数值/视觉坐标变换角度切入。SymPL 与这些工作的本质区别在于：它不修改 VLM 参数，也不依赖额外的度量空间训练，而是通过输入端的符号化重构，将异中心问题转化为 VLM 已经擅长的颜色区域定位任务。这种“预处理即求解”的策略使 SymPL 可以即插即用地应用于任意 VLM，同时保持与基线模型推理能力的公平比较。

### 3 适用边界与局限

SymPL 的适用性受以下因素约束：

**朝向估计的级联误差。** 流水线中最关键的脆弱环节是参考观察者的朝向估计（OrientAnything 模块）。错误分解分析（Figure 6）表明，最主要的错误来源正是朝向向量估计不准，该误差会向下传播至投影与分区步骤，导致整个推理失败。这一局限本质上是模块解耦的代价——SymPL 将视点变换外化给了朝向估计器，而非让 VLM 隐式学习。

**多模块依赖的鲁棒性风险。** SymPL 流水线串联了 GroundingDINO（目标检测）、Depth-Pro（深度估计）和 OrientAnything（朝向估计）三个外部预训练模型。任一模块的失效或精度不足都会直接影响最终输出。在目标检测遗漏、深度图噪声较大或朝向估计模糊的场景中，符号布局的保真度将下降。

**静态单帧假设。** 当前 SymPL 的符号布局生成过程仅适用于静态单帧图像，未考虑动态场景或视频输入。对于需要时序空间推理的任务（如导航中的运动预测），该方法需要额外的时序建模扩展。

**部分类别的提升空间。** 在 3DSRBench 的 visibility 和 facing 类别上，SymPL 相对于 APC-Num 的优势分别为 +2.00% 和相近水平，提升幅度相对有限。这可能与这些类别对深度精度和遮挡关系的要求更高有关，而当前简单的深度中值反投影策略无法充分建模遮挡。

### 4 开放问题

SymPL 的提出打开了若干值得进一步探索的方向：

1. **朝向估计的轻量化与鲁棒化。** 是否可以通过微调一个轻量级朝向估计模块来替代通用 OrientAnything，在保持精度的同时降低计算开销和级联误差风险？考虑到朝向估计是当前最主要的错误来源，这一改进可能带来显著的性能增益。

2. **端到端可微分符号布局。** SymPL 当前的符号布局生成是硬编码的、不可微的预处理步骤。是否可以将投影、抽象、二分区和定位四个因子设计为可微操作，嵌入 VLM 的训练流程，实现端到端的异中心空间推理优化？

3. **向 Embodied AI 的泛化。** 该方法在室内外导航、机器人操作等 Embodied AI 任务中的泛化能力尚未验证。这些场景通常涉及更复杂的 3D 几何、动态遮挡和实时性要求，SymPL 的多模块流水线能否满足这些约束需要进一步研究。

4. **大规模多对象场景与遮挡推理。** 当前流水线在处理包含数十个对象的场景时，符号布局的视觉清晰度可能下降（颜色区分饱和、圆形符号重叠）。是否可以通过分层分区、遮挡显式建模或注意力引导的符号筛选来扩展至更复杂的场景配置？

## 原文 PDF

![[paperPDFs/CVPR_2026/Keep_it_SymPL_Symbolic_Projective_Layout_for_Allocentric_Spatial_Reasoning_in_Vision_Language_Models.pdf]]