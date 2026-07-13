---
title: "4DWorldBench: A Comprehensive Evaluation Framework for 3D/4D World Generation Models"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/4DWorldBench_A_Comprehensive_Evaluation_Framework_for_3D_4D_World_Generation_Models.pdf
project_link: "https://yeppp27.github.io/4DWorldBench.github.io/"
code_link: null
aliases:
- 4CEF34WGM
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
- topic/generative_models_diffusion
- topic/benchmarks_datasets_evaluation
core_operator: 将多模态条件映射到统一文本空间，并利用 LLM 与 MLLM 分别进行抽象物理推理和具体视觉问答的自适应混合评估机制。
primary_logic: 通过对齐人类判断的细粒度问题生成和自适应维度选择，可以更可靠地评估世界生成模型，且文本驱动的物理推理优于直接视频观测。
claims:
- 混合 LLM 与 MLLM 评估器能互补处理表面视觉问答与复杂物理推理，优于单一评估器。
- 自适应维度选择（AdaDimen）显著优于固定维度设置，表明 LLM 更擅长场景相关的物理维度识别。
- 改进的 QA 评估与 Keye-VL 使用显著提高了属性对齐的人类判断相关性（PLCC 从 0.167 提升至 0.483）。
- VideoPhy2-test (Physical Commonsense) 上 Min(PC,SA) ACC = 0.469
---

# 4DWorldBench: A Comprehensive Evaluation Framework for 3D/4D World Generation Models

> [!tip] 核心洞察
> 通过对齐人类判断的细粒度问题生成和自适应维度选择，可以更可靠地评估世界生成模型，且文本驱动的物理推理优于直接视频观测。

| 字段 | 内容 |
|------|------|
| 中文题名 | 4DWorldBench：面向3D/4D世界生成模型的全面评估框架 |
| 英文题名 | 4DWorldBench: A Comprehensive Evaluation Framework for 3D/4D World Generation Models |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2511.19836) · [Project](https://yeppp27.github.io/4DWorldBench.github.io/) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction #topic/generative_models_diffusion #topic/benchmarks_datasets_evaluation |
| Method | 4DWorldBench |
| Dataset | VideoPhy2-test, User Study |

> [!tip] 效果简介
> - VideoPhy2-test (Physical Commonsense) 上，Min(PC,SA) ACC 0.469 vs 0.450 (+0.019)。
> - VideoPhy2-test (Joint) 上，Joint ACC 0.677 vs 0.770 (-0.093)。
> - User Study (Attribute Control Alignment) 上，PLCC 0.483 vs 0.167 (+0.316)。

## 概要

**问题与瓶颈**：现有 3D/4D 世界生成模型的评估基准存在三个关键缺口：(1) 无法统一衡量物理真实性、条件对齐、时空一致性和感知质量等多维度表现；(2) 难以自适应处理文本、图像、视频等多模态条件输入；(3) 评估指标与人类主观判断的相关性较弱。例如，**WorldScore** 仅支持文本条件且物理评估有限，**VBench** 系列覆盖部分维度但物理真实性评估不完整，**PhyGenBench** 侧重物理定律遵循性却缺乏模态多样性和语义丰富性。

**核心方法**：4DWorldBench 提出了一套自适应混合评估框架。其关键设计是将多模态条件统一映射到文本空间，并构建双轨评估器——**MLLM** 负责具体视觉问答以评估条件对齐，**LLM** 负责抽象物理推理以评估物理真实性。框架通过自适应维度选择（AdaDimen）根据场景语义动态生成诊断性问题，避免了固定维度设置的信息冗余或遗漏。

**核心洞察**：文本驱动的物理推理优于直接视频观测——LLM 作为裁判在物理真实性评估上持续胜出 MLLM 裁判，验证了“将视觉信号转化为文本描述再进行抽象推理”这一策略的有效性。

**主要结果**：
- 在属性控制对齐的用户研究中，改进后的条件对齐指标将 PLCC 从 0.167 提升至 0.483，SRCC 从 0.236 提升至 0.443。
- 在风格一致性评估中，PLCC 从 0.383 提升至 0.545。
- 自适应维度选择相比固定维度设置在物理评估 PLCC 上获得显著增益。
- 在 VideoPhy2-test 物理常识评估中，Min(PC,SA) ACC 达到 0.469，较基线提升 0.019。

**局限性提示**：物理真实性评估完全依赖从视频生成的文本描述进行推理，对需要精细视觉理解的物理现象（如细微变形、局部光照）可能不够敏感；基准数据集规模有限（非物理文本条件 76 条、物理文本条件 50 条）；部分维度仍依赖单个 MLLM 评分，其自身偏见可能影响评估可靠性。

### 3D/4D 世界生成模型的评估困境

近年来，以视频扩散模型和 3D 生成模型为代表的世界生成技术取得了显著进展，能够根据文本、图像或视频条件生成具有时空一致性的动态场景。然而，如何系统、可靠地评估这些模型的生成质量，已成为制约领域发展的核心瓶颈。

现有评估基准在以下四个维度上存在结构性缺陷：

**评估维度碎片化。** 当前主流基准各自聚焦于世界生成的某一侧面，缺乏统一的多维评估框架。**WorldScore** 仅支持文本条件，物理真实性评估极为有限；**VBench** 与 **VBench2.0** 虽涵盖部分物理和一致性维度，但物理真实性覆盖不完整；**PhyGenBench** 专注于物理定律遵循性，却牺牲了模态多样性和语义丰富性。这种碎片化使得研究者难以在不同模型之间进行公平、全面的横向比较。

**模态支持不完整。** 现有基准大多仅支持文本条件输入（如 WorldScore），部分支持图像条件，但几乎无一能同时覆盖文本、图像、视频三种输入模态。随着图像到 4D、视频到 4D 等新范式的涌现，缺乏多模态条件支持的评估框架已无法适配快速演进的研究前沿。

**物理真实性评估缺失或粗糙。** 世界生成模型的核心价值在于其对物理规律的隐式建模能力——物体应遵循重力、碰撞时应产生合理形变、光照应与材质属性一致。然而，现有基准要么完全忽略物理真实性维度，要么仅通过表面视觉问答进行粗粒度判断，无法对力学、光学、热学等细粒度物理现象进行系统诊断。

**评估方法与人类判断对齐不足。** 传统指标（如 FID、CLIP 相似度）与人类主观评价之间的相关性长期偏低。即便引入视觉语言模型进行自动评估，单一评估器也难以同时胜任表面视觉问答和抽象物理推理这两种性质迥异的任务——前者需要精确的视觉定位，后者则依赖因果逻辑和常识推理。

### 核心瓶颈：统一、自适应、可靠的评估机制

上述缺陷指向一个更深层的瓶颈：**缺乏一种能够自适应多模态条件、统一衡量感知质量、条件对齐、物理真实性和时空一致性，且与人类判断高度相关的评估机制。**

具体而言，理想的世界生成评估框架需要解决三个关键挑战：

1. **多模态条件的统一表示。** 当输入条件可以是文本、图像或视频时，如何将它们映射到统一的评估空间，使得同一套评估逻辑能够跨模态复用？
2. **物理推理的自动化诊断。** 如何超越“视频看起来是否真实”的浅层判断，自动生成针对具体物理维度的诊断性问题，并进行可解释的因果推理？
3. **评估策略的自适应选择。** 不同场景（如静态物体 vs. 动态碰撞）所涉及的评估维度截然不同，如何根据输入语义动态选择最相关的评估维度，而非采用一刀切的固定模板？

### 本文动机与设计思路

针对上述瓶颈，本文提出 **4DWorldBench**——一个面向 3D/4D 世界生成模型的全面评估框架。其核心设计思路包括：

- **多模态条件统一：** 将图像和视频条件通过视觉语言模型转化为文本描述，在统一的文本空间中进行评估，消除模态差异。
- **混合评估架构：** 结合 MLLM 驱动的视觉问答（擅长表面视觉定位）与 LLM 驱动的文本推理（擅长抽象物理因果分析），形成互补的双轨评估机制。这一设计的直接动机来自观察：当前 MLLM 在表面视频问答上表现良好，但在复杂物理推理上常显不足；而 LLM 恰恰擅长抽象推理和组合理解。
- **自适应维度选择：** 根据输入条件的语义内容，由 LLM 动态选择相关的物理维度和条件对齐子维度，生成场景特定的诊断性问题，避免固定维度设置带来的评估偏差。
- **人类判断对齐验证：** 通过用户研究量化自动指标与人类主观评分之间的 PLCC 和 SRCC 相关性，确保评估框架的可靠性和可信度。

## 核心方法与创新机理

4DWorldBench 的核心创新在于构建了一套**自适应、多模态、混合评估机制**，系统地填补了现有世界生成基准在评估维度、模态支持与评估方法上的结构性空白。与 **WorldScore**（仅支持文本条件，物理评估有限）、**VBench / VBench2.0**（物理真实性覆盖不完整）和 **PhyGenBench**（模态单一、语义丰富度不足）等先前基准相比，4DWorldBench 在以下四个关键维度上实现了根本性突破。

### 1. 从单模态到多模态条件的统一评估

现有基准大多仅支持文本条件，而 4DWorldBench 首次将评估范围扩展到**文本、图像、视频**三种输入模态。这一扩展并非简单的接口增加，其核心机制在于通过 **Keye-VL** 将图像和视频条件映射到统一的文本空间，使得所有模态的条件对齐评估可以在同一套问答框架下进行。这种统一映射策略避免了为不同模态设计独立评估协议所带来的不可比性，确保了跨模态评估的一致性。

### 2. 从缺失到全面的物理真实性评估

物理真实性是衡量世界模型是否真正“理解”世界的关键维度，但此前的基准要么完全缺失该维度，要么仅做局部覆盖。4DWorldBench 明确引入了基于 **LLM 驱动的自适应物理维度评估**：系统根据输入条件的语义内容，自动选择相关的物理维度（覆盖力学、光学、热学等），并生成诊断性问题。这一设计的关键洞察在于——**文本驱动的物理推理优于直接视频观测**。消融实验证实，LLM 作为裁判在物理真实性评估上持续优于 MLLM 裁判，因为当前多模态模型擅长表面视觉问答，但在复杂物理推理上表现薄弱，而 LLM 在抽象推理和组合理解方面具有天然优势。

### 3. 从粗粒度到自适应细粒度条件对齐

先前的条件对齐评估多采用固定、粗粒度的指标，无法针对不同场景的语义特点进行差异化评估。4DWorldBench 提出了**自适应维度选择（AdaDimen）**与**细粒度问题生成**机制：系统将条件分解为事件、场景、属性、关系等子维度，并针对每个子维度独立生成诊断性问题。消融实验表明，AdaDimen 相比固定维度设置（FixDimen）在物理评估的 PLCC 上获得了显著收益，证明 LLM 更擅长识别与场景相关的物理维度。此外，改进的问答形式与 Keye-VL 的使用将属性对齐的人类判断相关性（PLCC）从 0.167 大幅提升至 0.483，验证了细粒度评估策略的有效性。

### 4. 传统指标与 LLM/MLLM 混合评估的融合

4DWorldBench 并未完全抛弃传统指标，而是将其与 LLM/MLLM 驱动的问答评估有机结合，形成互补的双轨架构：
- **MLLM 问答模块**负责具体的视觉问答，评估事件、场景、属性、运动等维度的条件对齐；
- **LLM 问答模块**负责高层次的物理推理，通过对视频文本描述的抽象分析评估物理真实性；
- **传统感知质量指标**（CLIPIQA+、CLIP-Aesthetic、FastVQA 等）评估空间质量、时序质量和纹理质量；
- **4D 一致性计算**通过 SLAM 重投影误差、光流相似性、VGG 风格 Gram 矩阵等指标评估时空一致性。

这种混合策略使得评估框架既能捕捉低层次的感知质量，又能进行高层次的语义和物理推理，实现了对世界生成模型能力的全维度刻画。

4DWorldBench 围绕四个核心评估维度构建：**感知质量**、**条件对齐**、**物理真实性**和**4D 一致性**。框架支持文本、图像、视频三种条件模态，覆盖文本到 3D/4D、图像到 3D/4D 及视频到 4D 的生成任务。其评估流程采用混合评估范式：将传统模型评分、特征相似度、基于 LLM 的问答和基于 MLLM 的问答集成到一个统一的管线中，并通过人类主观研究验证可靠性。

### 多模态条件统一

框架首先将所有模态条件映射到统一文本空间。对于图像和视频条件，通过 Keye-VL 将其转化为文本描述，使得后续评估模块可以在统一的语义表示上运行，而无需为每种模态设计独立的评估逻辑。

### 双轨评估机制

框架的核心设计在于两条互补的评估轨道：

1. **MLLM 条件对齐问答轨道**：面向具体视觉基础，对生成视频进行细粒度视觉问答。该轨道将统一后的文本条件分解为维度特定的诊断问题（覆盖事件、场景、属性、运动、关系等子维度），由 MLLM 直接观察视频并回答，从而评估生成内容与输入条件的对齐程度。

2. **LLM 物理推理问答轨道**：面向抽象物理推理，不直接观测视频，而是将生成视频转化为文本描述后，由 LLM 基于描述进行物理一致性判断。该轨道自适应地根据输入语义选择相关物理维度（如力学、光学、热学、材料等），生成诊断性问题并计算物理真实性得分。

这一双轨设计源于一个关键观察：当前 MLLM 擅长表面级视频问答，但在复杂物理推理上表现挣扎；而 LLM 在抽象推理和组合理解方面具有优势。因此，将视觉问答与文本驱动物理推理分离，能互补地覆盖评估需求。

### 感知质量与 4D 一致性模块

除双轨问答外，框架还集成了传统感知质量评估模块和 4D 一致性计算模块：

- **感知质量**：使用 CLIPIQA+ 评估空间质量，CLIP-Aesthetic 评估美学质量，FastVQA 评估时序连贯性，并通过 mPLUG-Owl3 评估 3D 纹理质量。
- **4D 一致性**：通过 SLAM 重投影误差评估 3D 几何一致性，通过光流相似性评估运动一致性，并通过 VGG 风格 Gram 矩阵评估片段间的风格一致性。

### 自适应维度选择

框架的关键创新在于**自适应维度选择**（AdaDimen）：物理评估模块根据输入描述的语义动态选择相关物理维度，而非使用固定维度集。消融实验表明，AdaDimen 相比固定维度设置（FixDimen）在与人类判断的对齐度上取得了显著收益，证实了 LLM 在场景相关物理维度识别上的优势。

### 评估公平性设计

框架针对不同模型类别实现了条件适配的评估策略。例如，对于 3D 生成模型（不包含对象运动），框架暂停了事件控制、运动控制和物理真实性的评估，仅评估静态属性，体现了公平性考量。

![[assets/figures/papers/paper_list_l2231_https_arxiv_org_abs_2511_19836/figures/003_Figure_1.jpg]]
*Figure 1: Overview of the 4DWorldBench framework. The benchmark evaluates generation quality across four key dimensions: 4D consistency, condition alignment, perceptual quality, and physical realism. It supports diverse generative settings, including text-, image-, and video-to-3D/4D generation. The framework integrates hybrid evaluation metrics—model-based scores, feature-based similarity, LLMbased QA, and MLLM-based QA—together with human studies for reliability. Condition- and dimension-adaptive QA modules leverage MLLMs for concrete visual grounding and LLMs for higher-level physical reasoning*

### 4DWorldBench 评估框架总体架构

4DWorldBench 围绕四个核心评估维度构建：**感知质量（Perceptual Quality）**、**条件对齐（Condition Alignment）**、**物理真实性（Physical Realism）** 和 **4D 一致性（4D Consistency）**。框架支持文本、图像、视频三种输入模态的世界生成模型评估，其关键创新在于将多模态条件统一映射到文本空间，并通过 LLM 与 MLLM 的混合评估机制实现自适应、细粒度的诊断性评估（Figure 1）。

### 核心评估模块

#### 多模态条件统一模块

该模块是框架的入口，负责将异构的输入条件转化为统一的文本表示。对于图像和视频条件，框架利用 **Keye-VL** 将其转化为描述性文本，使得后续的物理推理和条件对齐评估可以在统一的文本空间中进行。这一设计的动机在于：当前 MLLM 虽然擅长表面视觉问答，但在复杂物理推理上表现不足，而 LLM 在抽象推理和组合理解方面具有优势。

#### 物理感知问题生成模块

在物理真实性评估中，框架首先基于统一后的文本描述，利用 LLM 自适应地选择与场景语义相关的物理维度。物理维度遵循结构化分类体系，涵盖四大类：**材料（Material）**、**力学（Mechanics）**、**光学（Optics）** 和 **热学（Thermal）** 现象。随后，LLM 针对选定的维度生成诊断性问题，确保评估与场景内容高度相关（Figure 5）。

![[assets/figures/papers/paper_list_l2231_https_arxiv_org_abs_2511_19836/figures/008_Figure_5.jpg]]
*Figure 5: Pipeline of the Physical Realism Evaluation. The framework first unifies text, image, and video conditions into a common textual form, then uses an LLM to adaptively select relevant physical dimensions and generate diagnostic questions. An LLM-based QA module compares predicted and reference answers to yield a continuous physical realism score*

#### LLM 物理推理问答模块

该模块接收视频的文本描述，对诊断性问题进行抽象物理推理。LLM 比较预测答案与期望的物理结果，计算物理真实性得分。消融实验表明，LLM-as-judge 的设计在物理真实性评估上持续优于 MLLM-based judging，验证了文本驱动推理在物理评估中的优势。

#### MLLM 条件对齐问答模块

条件对齐评估采用 MLLM 对生成视频进行细粒度视觉问答。框架将多模态条件转化为文本后，生成维度特定的诊断性问题，覆盖**事件控制**、**场景控制**、**属性控制**、**关系控制**、**相机控制**和**运动控制**等子维度。MLLM 直接检视生成视频并回答这些问题，评估生成内容与输入条件的一致性（Figure 7）。

![[assets/figures/papers/paper_list_l2231_https_arxiv_org_abs_2511_19836/figures/014_Figure_7.jpg]]
*Figure 7: Overall pipeline of 4D-Condition Alignment Evaluation. The framework converts multimodal conditions into text, generates fine-grained and dimension-specific questions for sub-aspects, and uses an MLLM-based QA process to assess the alignment score*

#### 传统感知质量评估模块

感知质量评估采用成熟的模型化指标：
- **空间质量**：使用 CLIPIQA+ 评估单帧技术质量，CLIP-Aesthetic 评估整体美学吸引力
- **时序质量**：使用 FastVQA 评估跨帧时序连贯性和视觉稳定性
- **3D 纹理质量**：通过 mPLUG-Owl3 进行纹理质量评分

#### 4D 一致性计算模块

4D 一致性通过几何、运动和风格三个子维度综合衡量：
- **3D 几何一致性**：利用 SLAM 系统计算的片段重投影误差
- **运动一致性**：结合光流相似性与 MLLM 运动合理性问答
- **风格一致性**：基于 VGG 风格 Gram 矩阵的片段级计算

### 关键公式推导

#### 物理真实性得分

物理真实性评估的核心是将诊断性问答转化为连续得分。对于每个物理诊断问题，定义二进制正确性分数：

$$s_i = \mathcal{H}(\hat{A}_i = A_i^*)$$

其中 $\mathcal{H}$ 为指示函数，$\hat{A}_i$ 为 LLM 预测的物理结果，$A_i^*$ 为期望的真实物理结果。当预测与期望一致时 $s_i = 1$，否则为 $0$。

所有 $N$ 个诊断问题的平均正确率即为物理真实性得分：

$$S_{\mathrm{phy}} = \frac{1}{N} \sum_{i=1}^{N} s_i, \quad S_{\mathrm{phy}} \in [0, 1]$$

#### 条件对齐得分

条件对齐评估采用与物理真实性相同的形式，对所有条件对齐诊断问题计算平均正确率：

$$S_{\mathrm{align}} = \frac{1}{N} \sum_{i=1}^{N} s_i \in [0, 1]$$

#### 相机控制误差

相机控制评估从位姿估计误差出发。给定真实旋转矩阵 $\mathbf{R}_{\mathrm{gt}}$ 和估计旋转矩阵 $\mathbf{R}$，角度偏差误差定义为：

$$e_{\theta} = \operatorname{arccos}\left(\frac{\operatorname{tr}(\mathbf{R}_{\mathrm{gt}}\mathbf{R}^{\top}) - 1}{2}\right) \cdot \frac{180}{\pi}$$

尺度不变位移误差衡量真实相机中心 $\mathbf{t}_{\mathrm{gt}}$ 与经过尺度对齐的估计相机中心 $s\mathbf{t}$ 之间的欧氏距离：

$$e_{t} = \left\| \mathbf{t}_{\mathrm{gt}} - s \mathbf{t} \right\|_{2}$$

单帧相机控制误差取旋转误差与位移误差的几何平均：

$$e_{\mathrm{camera}} = \sqrt{e_{\theta} \cdot e_{t}}$$

#### 3D 几何一致性得分

对于每个视频片段 $c$，定义片段重投影误差为所有共视像素点重投影 L2 距离的平均：

$$e_{\mathrm{reproj}}^{(c)} = \frac{1}{|\mathcal{V}_c|} \sum_{(i,j) \in \mathcal{V}_c} |\mathbf{p}^*_{ij} - \Pi(\mathbf{P}_{ij})|_2$$

其中 $\mathcal{V}_c$ 为片段 $c$ 中的共视像素点集合，$\mathbf{p}^*_{ij}$ 为观测像素坐标，$\Pi(\mathbf{P}_{ij})$ 为 3D 点 $\mathbf{P}_{ij}$ 的重投影坐标。

对所有片段 $\mathcal{C}$ 的平均重投影误差进行归一化后取反，得到 3D 一致性得分：

$$e_{3\mathrm{D}} = 1 - \mathrm{normalize}\left(\frac{1}{|\mathcal{C}|} \sum_{c \in \mathcal{C}} e_{\mathrm{reproj}}^{(c)}\right)$$

得分越高表示几何一致性越好。

#### 运动一致性得分

片段光流误差衡量估计光流 $\mathbf{F}_{t \to t+1}$ 与从运动场生成的光流 $\mathbf{F}'_{t \to t+1}$ 之间的平均 L2 差异：

$$e_{\mathrm{flow}}^{(c)} = \frac{1}{T_c - 1} \sum_{t=1}^{T_c-1} |\mathbf{F}_{t \to t+1} - \mathbf{F}'_{t \to t+1}|_2$$

运动一致性得分为归一化光流误差的反值加上 MLLM 运动合理性问答正确率 $s_{\mathrm{QA}}$：

$$e_{\mathrm{motion}} = \left(1 - \mathrm{normalize}\left(\frac{1}{|\mathcal{C}|} \sum_{c \in \mathcal{C}} e_{\mathrm{flow}}^{(c)}\right)\right) + s_{\mathrm{QA}}$$

#### 风格一致性得分

风格一致性通过片段首末帧的 VGG 风格 Gram 矩阵距离衡量。对所有片段的平均风格距离归一化后取反：

$$e_{\mathrm{style}} = 1 - \mathrm{normalize}\left(\frac{1}{|\mathcal{C}|} \sum_{c \in \mathcal{C}} e_{\mathrm{style}}^{(c)}\right)$$

### 模块间的协同机制

四个核心评估维度通过混合评估策略实现互补：物理真实性评估完全依赖 LLM 的文本驱动推理，避免 MLLM 在抽象物理推理上的不足；条件对齐评估则充分发挥 MLLM 的视觉理解能力，实现细粒度的视觉问答。自适应维度选择（AdaDimen）机制使得评估维度能够根据输入条件的语义动态调整，消融实验证实其相比固定维度设置（FixDimen）在物理评估 PLCC 上获得显著收益。

## 实验与关键发现

### 主实验结果

4DWorldBench 对多类 3D/4D 世界生成模型进行了统一评估，结果汇总于 Table 3 和 Table 4。在 4D 生成模型排行榜中，CamI2V 取得最高综合得分 0.697，EX-4D 紧随其后获得 0.599。在 3D 生成模型排行榜中，图像到 3D 模型 SyncDreamer 以 0.628 的综合得分领先。在动力学控制子维度上，视频到 4D 模型 ReCamMaster 和 TrajectoryCrafter 表现突出，ReCamMaster 在 Dynamics 指标上分别达到 0.680、0.714、0.773。Figure 8 以雷达图形式展示了多模型在各维度上的性能对比。

![[assets/figures/papers/paper_list_l2231_https_arxiv_org_abs_2511_19836/figures/009_Table_3.jpg]]
*Table 3: Leaderboard for different categories of 4D generation models*

![[assets/figures/papers/paper_list_l2231_https_arxiv_org_abs_2511_19836/figures/015_Figure_8.jpg]]
*Figure 8: Performance comparison for multiple world generative models*

在物理常识推理的外部验证上，4DWorldBench 的物理评估模块在 VideoPhy2-test 数据集上进行了测试（Table 5）。在 Min(PC,SA) 指标上，该方法取得 0.469 的准确率，相比基线提升 +0.019；但在 Joint 指标上，该方法取得 0.677，低于基线的 0.770（差距 -0.093）。这表明文本驱动的物理推理在平衡物理常识与语义依从性方面具有优势，但在极端严格的双重约束条件下仍有改进空间。

与人类判断的相关性验证是评估可靠性的关键。在属性控制对齐维度上，改进后的评估方法将 PLCC 从 0.167 大幅提升至 0.483，SRCC 从 0.236 提升至 0.443（Table 8）；在风格一致性维度上，PLCC 从 0.383 提升至 0.545（Table 9）。这些结果表明，细粒度问题生成与 Keye-VL 的引入显著增强了自动评估与人类主观判断的一致性。

### 消融实验

物理真实性评估模块的消融实验（Table 6）揭示了三个关键设计选择的影响：

![[assets/figures/papers/paper_list_l2231_https_arxiv_org_abs_2511_19836/figures/013_Table_6.jpg]]
*Table 6: Comparison of judge types, dimension settings, and question counts on Physical Realism Evaluation. “FixDimen” uses predefined dimensions; “AdaDimen” applies adaptive dimension*

**LLM 裁判 vs. MLLM 裁判。** LLM 作为裁判在所有设置下持续优于 MLLM 裁判，验证了文本驱动推理在抽象物理判断中的优势。MLLM 虽然在视觉问答上表现良好，但在需要组合性理解和因果推理的物理场景中能力不足。

**自适应维度选择 vs. 固定维度设置。** 自适应维度选择（AdaDimen）相比固定维度设置（FixDimen）在物理评估 PLCC 上获得显著收益。这证明 LLM 能够根据场景语义识别与物理相关的评估维度，避免了无关维度引入的噪声。

**诊断问题数量的影响。** 将诊断问题数量从 3 个增加到 10 个，能持续提升与人类判断的对齐度。更多的问题提供了更细粒度的物理现象覆盖，但也增加了计算开销，需要在精度与效率之间权衡。

在条件对齐评估方面，两项改进被证实有效：以 Keye-VL 替代 llava-video 进行视觉问答，以及用片段级风格一致性计算替代视频级计算。前者提升了语义理解的准确性，后者更好地捕获了局部时序的风格漂移，两者共同推动了与人类评分的相关性提升。

### 失败模式与局限分析

尽管 4DWorldBench 在多项指标上表现出色，实验暴露了若干系统性失败模式：

1. **物理细节敏感性不足。** 物理真实性评估完全依赖从视频生成的文本描述进行推理。对于需要精细视觉理解的物理现象——如细微的材料变形、局部光照变化、流体的低幅度波动——文本描述可能丢失关键信息，导致评估不敏感。这是文本驱动推理范式的内在局限。

2. **严格物理约束下的性能退化。** 在 VideoPhy2-test 的 Joint 指标上，该方法低于基线 0.093，说明当同时要求高物理常识和高语义依从性时，纯文本推理难以精确判断两者的边界情况。

3. **单 MLLM 评分的偏见风险。** 部分评估维度（如运动合理性、3D 纹理质量）仍然依赖单个 MLLM 的评分输出。MLLM 自身可能存在位置偏见、长度偏见或视觉幻觉，这些系统误差会直接传导至最终评估分数，影响可靠性。

4. **基准覆盖的局限性。** 基准数据集规模有限（非物理文本条件 76 条、物理文本条件 50 条），可能无法覆盖长尾场景和边缘案例。此外，3D 生成模型的评估暂停了事件控制、运动控制和物理真实性维度（因为这些模型不包含对象运动），虽然体现了条件适配的公平性，但也限制了跨模型类型的完全对比。

5. **人类实验的统计可靠性。** 人类主观实验的参与人数仅 10 人，虽然 PLCC 和 SRCC 的改进趋势明显，但小样本可能影响统计显著性，需要更大规模的人类研究加以验证。

## 定位与知识库关联

### 1. 与现有基准的维度覆盖对比

4DWorldBench 的定位可以从其与代表性基准的维度覆盖差异中得到清晰界定。**Table 2** 系统对比了该基准与 **WorldScore**、**VBench**、**VBench2.0**、**PhyGenBench** 等现有工作在输入模态支持和评估维度覆盖上的差异。传统基准普遍存在两个结构性缺口：一是输入模态单一（大多仅支持文本条件），二是评估维度不完整——尤其是物理真实性（Physical Realism）维度的系统性缺失。4DWorldBench 通过同时覆盖感知质量（Q）、条件对齐（A）、物理真实性（P）和 4D 一致性（C）四个主维度，填补了这一空白。这种四维框架并非简单的维度堆叠，而是基于一个核心观察：世界生成模型的质量瓶颈已从“能否生成合理图像”转移到“生成内容是否物理可信且条件一致”，因此评估体系必须同时具备物理推理能力和多模态条件适配能力。

### 2. 评估方法论的关键改进槽位

与先前工作相比，4DWorldBench 在评估方法论上改变了四个关键槽位：

**输入模态支持**：从仅文本（WorldScore）或部分支持图像（VBench 系列）扩展到文本、图像、视频三类条件的统一支持。这一扩展使得基准能够覆盖 text-to-4D、image-to-4D、video-to-4D 等更丰富的生成范式，而非仅局限于 text-to-video 场景。

**物理真实性评估**：PhyGenBench 虽然侧重物理定律遵循性，但其评估范围受限于预定义的物理现象类别，且缺乏对多模态条件的适配。4DWorldBench 引入基于 LLM 的自适应物理维度选择机制（AdaDimen），能够根据输入场景的语义动态确定需要评估的物理维度（力学、光学、热学等），而非使用固定维度集合。消融实验证实，AdaDimen 在物理评估的人类判断相关性（PLCC）上显著优于固定维度设置（FixDimen），表明场景感知的维度选择是提升评估可靠性的关键因果机制。

**评估器架构**：从单一 VLM 评分或传统指标转向 LLM-MLLM 混合评估架构。这一设计的动机源于对两类模型能力边界的观察：当前 MLLM 擅长表面级视频问答，但在复杂物理推理上表现挣扎；LLM 则擅长抽象推理和组合理解。因此，框架将物理推理任务分配给 LLM（基于视频描述文本进行推理），将具体的视觉条件对齐问答分配给 MLLM（直接观察生成视频）。消融实验证实，LLM-as-judge 在物理真实性评估上持续优于 MLLM-based judging，验证了文本驱动推理在物理评估中的优势。

**条件对齐评估策略**：从粗粒度或不可调整的评估转向自适应维度选择与细粒度问题生成。框架将条件对齐分解为事件、场景、属性、关系等子维度，针对每个子维度生成诊断性问题，实现了对条件遵循度的独立、可解释评估。用户研究显示，改进后的 QA 评估与 Keye-VL 的使用将属性对齐的人类判断相关性（PLCC）从 0.167 显著提升至 0.483，风格一致性 PLCC 从 0.383 提升至 0.545。

### 3. 适用边界与公平性设计

4DWorldBench 在评估策略上体现了对模型类别的条件适配公平性。对于 3D 生成模型，基准暂停了事件控制、运动控制和物理真实性的评估，因为这些模型不包含对象运动，施加这些维度评估将引入系统性偏差。这一设计确保了不同范式模型在同一基准上的可比性。

然而，基准的适用边界也存在明确限制。当前评估体系对 3D 场景生成仅覆盖静态属性，尚未扩展到交互式物理模拟场景；物理真实性评估完全依赖从视频生成的文本描述进行推理，对于需要精细视觉理解的物理现象（如细微变形、局部光照变化）可能不够敏感。此外，部分评估维度（如运动合理性、3D 纹理质量）仍然依赖单个 MLLM 的评分，其自身偏见可能影响评估的可靠性——这一问题在 VBench 系列基准中同样存在，尚未得到根本性解决。

### 4. 局限与开放问题

基于分析中识别的方法论约束，以下开放问题值得后续工作关注：

**物理评估的可信度增强**：当前物理真实性评估完全依赖 LLM 对视频描述的文本推理，缺乏对生成视频中精细视觉现象的感知能力。一个可能的改进方向是引入物理仿真引擎作为 oracle，将生成视频的物理行为与仿真结果进行对比验证，从而增强评估的准确性和可解释性。这一方向在现有基准（包括 PhyGenBench）中均未实现。

**评估效率与自包含性**：当前框架对 LLM 和 MLLM API 的依赖较高，评估成本与延迟限制了大规模应用。如何构建更高效、自包含的评估工具包（例如通过蒸馏小模型替代 API 调用）是一个工程层面的开放问题。

**基准覆盖范围的扩展**：当前基准数据集规模有限（非物理文本条件 76 条、物理文本条件 50 条），可能不足以覆盖所有边缘案例。此外，基准尚未扩展到具身智能体操作等交互式场景，限制了对更广泛具身 AI 应用的覆盖。如何将丰富的文本描述可靠地转化为连贯的时空交互评估，以改善文本到 4D 模型的事件和关系对齐，是提升基准实用价值的关键方向。

**人类评估的统计可靠性**：用户研究参与人数仅 10 人，部分相关性指标（PLCC/SRCC）的统计效力可能受限。后续工作需要在更大规模的人类评估上验证当前结论的稳健性。

## 原文 PDF

![[paperPDFs/CVPR_2026/4DWorldBench_A_Comprehensive_Evaluation_Framework_for_3D_4D_World_Generation_Models.pdf]]
