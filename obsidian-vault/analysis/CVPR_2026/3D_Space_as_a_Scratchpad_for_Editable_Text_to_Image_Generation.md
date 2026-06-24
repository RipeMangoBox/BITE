---
title: 3D Space as a Scratchpad for Editable Text-to-Image Generation
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/3D_Space_as_a_Scratchpad_for_Editable_Text_to_Image_Generation.pdf
project_link: "https://oindrilasaha.github.io/3DScratchpad/"
code_link: null
aliases:
- 3SS
- 3SASETIG
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
- topic/generative_models_diffusion
core_operator: 三维空间草稿板表示是关键的因果调节因子。通过允许显式放置、定向和摄像机选择主体，它直接控制最终图像的空间准确性和身份一致性，从而显著提升复杂提示的遵循度。
primary_logic: 将三维空间作为文本到图像生成的中间推理草稿板，使LLM能够在渲染前进行结构化空间推理，类似于语言模型中的思维链外化，为视觉生成引入了“空间思考”的新范式。
claims:
- 方法在GenAI-Bench上实现了32%的文本对齐改进，无需额外训练。
- 消融研究表明，逐步添加方向规划和摄像机选择代理可稳步提高文本对齐度（0.821→0.824→0.830）。
- 基于裁剪的方向估计策略比全图估计更准确，为复杂旋转场景提供了关键能力，尽管基准测试中朝向敏感样本少，定量增益有限。
- 与其他仅使用文本或二维推理模态的方法相比，三维空间草稿板在多个基准测试中一致地提高了文本对齐度。
---

# 3D Space as a Scratchpad for Editable Text-to-Image Generation

> [!tip] 核心洞察
> 将三维空间作为文本到图像生成的中间推理草稿板，使LLM能够在渲染前进行结构化空间推理，类似于语言模型中的思维链外化，为视觉生成引入了“空间思考”的新范式。

| 字段 | 内容 |
|------|------|
| 中文题名 | 三维空间：可编辑文本到图像生成的空间草稿板 |
| 英文题名 | 3D Space as a Scratchpad for Editable Text-to-Image Generation |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2601.14602) · [Project](https://oindrilasaha.github.io/3DScratchpad/) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction #topic/generative_models_diffusion |
| Method | 3D Spatial Scratchpad |
| Dataset | GenAI-Bench, CompoundPrompts, T2I-CompBench |

> [!tip] 效果简介
> - GenAI-Bench 上，Text Alignment (VQAScore) 0.83 vs 0.63 (Flux.1 [dev]) (+0.20 (32% relative improvement))。
> - CompoundPrompts 上，Text Alignment (VQAScore) 0.91 vs 0.73 (Flux.1 [dev]) (+0.18)。
> - T2I-CompBench (Complex category) 上，3-in-1 metric 0.65 vs 0.37 (Flux.1 [dev]) (+0.28)。

## 概述

### 问题瓶颈

当前文本到图像生成模型在处理需要精确空间关系、多对象身份与组合意图的复杂提示时，面临系统性缺陷：模型缺乏一个显式的空间推理工作区，导致文本对齐性差，无法一致地实现可控生成。直接“文本到像素”的范式将空间推理完全隐式地交由模型内部完成，在面对计数、比较、否定、属性绑定等组合推理任务时表现脆弱。

### 核心洞察

本工作提出一个根本性的范式转变：**将三维空间作为文本到图像生成的中间推理草稿板**。其核心洞察在于，就像语言模型中的思维链将隐式推理外化为显式步骤，视觉生成同样需要一个结构化的“空间思考”媒介——一个可放置、定向、观察的三维场景，使语言意图到视觉合成的映射不再是一次性的黑箱跳跃，而是经过显式空间推理的可控过程。

### 方法定位

**3D Spatial Scratchpad** 方法构建了一个基于代理的三维空间推理流水线，无需额外训练即可显著提升文本到图像生成的空间准确性。其关键因果调节因子是三维草稿板表示：通过显式放置、定向和摄像机选择，直接控制最终图像的空间准确性和身份一致性。具体而言，系统将输入提示解析为主体与背景，在带标尺、地平面和固定边界的三维空场景中以网格形式放置主体，由专门的LLM代理负责放置规划、朝向估计与变换调整、摄像机视角选择，最终通过身份保持的深度条件生成管线（SIGMA-Gen）合成图像。该方法同时支持生成后的三维一致性编辑——用户可通过文本或手动操作修改草稿板中的主体姿态与位置，编辑结果一致地反映到最终图像中。

在方法谱系中，该工作区别于仅使用文本迭代推理的 **Idea2Img**（Yang et al., 2023）和基于二维布局推理的 **RPG**（Yang et al., ICML 2024），首次将三维空间作为显式推理模态引入文本到图像生成。与直接使用 **Flux.1 [dev]** 等基准模型相比，其核心变化在于将隐式的空间推理替换为结构化的三维草稿板中介。

### 主要结果

在多个具有挑战性的基准测试上，3D Spatial Scratchpad 一致地实现了显著的文本对齐提升：

- **GenAI-Bench**：文本对齐度（VQAScore）从 Flux.1 [dev] 的 0.63 提升至 0.83，**相对改进 32%**，无需任何额外训练。
- **CompoundPrompts**：文本对齐度从 0.73 提升至 0.91。
- **T2I-CompBench（Complex 类别）**：3-in-1 指标从 0.37 提升至 0.65。

消融实验揭示了各代理的因果贡献：逐步添加朝向规划代理（Agent ③）和摄像机选择代理（Agent ④），文本对齐度从 0.821 依次提升至 0.824 和 0.830，图像质量保持稳定。基于裁剪的朝向估计策略比全图估计更准确，为复杂旋转场景提供了关键鲁棒性（尽管基准测试中朝向敏感样本少，定量增益有限）。在草稿板渲染中添加标尺可进一步提高文本对齐度。

### 局限与开放问题

方法存在若干已知局限：LLM生成的物体放置可能过于均匀，缺乏真实场景的自然构图多样性；对复杂的交互活动（如握手、追逐），活动理解与朝向规划可能失败；生成的3D网格姿态多样性有限，无法调整铰接式资产的关节；当前系统依赖多个预训练模型，端到端训练尚不可用。开放问题包括：如何通过验证步骤或强化学习提高构图自然性，是否可将物理模拟器纳入以支持更真实的物体交互，以及能否将空间草稿板扩展到视频生成以支持时空一致性。

## 背景与动机

文本到图像生成模型近年来取得了显著进展，但在处理需要精确空间关系、对象身份保持和组合意图的复杂提示时，依然暴露出根本性的文本对齐缺陷。当前主流模型（如 **Flux.1 [dev]**）采用从文本直接映射到像素的生成范式，缺乏显式的空间推理工作区，导致模型在计数、比较、否定、属性绑定等需要结构化理解的场景中频繁失败——在 GenAI-Bench 基准上，Flux.1 [dev] 的文本对齐得分仅为 0.63。

现有改进方案主要沿着两条路径展开：一是基于文本的迭代推理，如 **Idea2Img**（Yang et al., 2023）通过多轮语言反思逐步优化生成结果；二是基于二维布局的推理，如 **RPG**（Yang et al., ICML 2024）利用二维空间规划辅助生成。然而，这两种范式均存在结构性局限——文本推理缺乏对空间关系的直观建模，二维推理则无法表达深度、遮挡和三维朝向等关键信息，导致在处理“左侧的椅子面向右侧的桌子”这类需要三维空间理解的自然语言指令时，二者均难以稳定地实现可控生成。

本文的核心动机在于：**将三维空间作为文本到图像生成的中间推理草稿板**。这一思路受语言模型中“思维链”外化推理的启发——正如显式的中间推理步骤能显著提升大语言模型的复杂问题求解能力，为视觉生成引入一个结构化的三维推理基底，有望弥合语言意图与精确视觉合成之间的鸿沟。具体而言，该方法允许在渲染前显式地放置、定向和选择摄像机视角来操控主体，从而将空间推理从模型的隐式内部表征中外化出来，为可控生成提供直接的因果调节因子。

## 核心创新

### 从“黑箱生成”到“三维空间推理”：范式转换

当前文本到图像（T2I）生成模型的核心瓶颈在于**缺乏空间推理的中间工作区**。主流方法（如 **Flux.1 [dev]**）直接从文本映射到像素，模型内部对物体位置、朝向、空间关系的表征是隐式且不可控的，导致在需要精确组合推理的复杂提示上文本对齐性差。本文提出了一项关键范式转换：**将三维空间作为文本到图像生成的显式推理草稿板（3D Spatial Scratchpad）**，使大语言模型（LLM）能够在渲染前进行结构化的空间推理——类似于语言模型中的“思维链”外化，为视觉生成引入了“空间思考”的新范式。

这一范式转换的因果调节因子是**三维空间草稿板表示本身**：通过允许显式放置、定向和摄像机选择主体，它直接控制最终图像的空间准确性和身份一致性，从而显著提升复杂提示的遵循度。

### Changed Slots：相对基线的关键差异

与基线方法相比，本文在四个关键设计槽位上做出了根本性改变：

| 设计槽位 | 基线方法 | 本文方法 | 因果作用 |
|:---|:---|:---|:---|
| **中间空间表示** | 无（直接文本到像素）或二维布局（**RPG**, Yang et al., ICML 2024） | 三维网格放置草稿板，含标尺、地平面和固定边界 | 提供显式的三维空间推理基底，使LLM能够进行结构化的空间规划 |
| **主体放置与定向** | 隐式（模型内部）或仅文本迭代推理（**Idea2Img**, Yang et al., 2023） | LLM代理显式生成三维边界框并调整三维变换（旋转、平移、缩放） | 将空间关系从隐式推断转化为显式可控变量 |
| **摄像机选择** | 固定正面或隐式 | CameraPicker代理从五个提案视图中选择与提示最匹配的视角 | 解耦场景布局与观察视角，确保最终渲染与文本意图对齐 |
| **身份保持** | 无显式控制或仅限于单主体 | SIGMA-Gen多主体身份和深度联合控制，在单次去噪循环中保持多个主体身份 | 在复杂多主体场景中维持身份一致性，避免主体混淆 |

### 核心机制：四代理协同的三维空间推理管线

方法由四个专业化LLM代理（Agent ①–④）协同完成从文本到三维空间规划再到图像生成的完整推理链：

1. **SubjectInstantiation（Agent ①）**：解析输入提示，将复杂文本分解为独立的主体和背景元素，生成每个主体的描述 $s_i^P$ 和增强提示 $P'$。

2. **BboxPlanner（Agent ②）**：根据增强提示、主体描述、身份图像、长宽比和三维空间描述 $D$，为每个主体生成三维边界框并初始放置：
   $$\mathcal{S}^{\mathrm{BBOX}} = \mathrm{BboxPlanner}(P', \mathcal{S}^{\mathrm{P}}, \mathcal{S}^{\mathrm{I}}, \mathcal{S}^{\mathrm{A}}, D)$$

3. **OrientationEstimator + TransformPlanner（Agent ③）**：利用生成图像的裁剪区域估计当前绝对朝向，结合目标朝向和多视角渲染建议三维变换（旋转、平移、缩放）：
   $$\mathcal{S}^{\mathrm{TR}} = \mathrm{TransformPlanner}(P', R, S^{\mathrm{O_{est}}}, S^{\mathrm{O_{tgt}}}, S^{\mathrm{P}}, D)$$
   其中基于裁剪的朝向估计策略（Figure 11）比全图估计更准确，为复杂旋转场景提供了关键的鲁棒性。

4. **CameraPicker（Agent ④）**：从五个提案视图中选择与提示最匹配的最终摄像机视角，确保渲染结果忠实地反映文本意图。

### 关键设计决策的证据支撑

消融实验（Table 3）揭示了各代理的因果贡献：逐步添加Agent ③和④使文本对齐度从0.821提升至0.824再到0.830，验证了朝向规划和摄像机选择对文本对齐的渐进式改善。在渲染设计层面（Table 4），在草稿板渲染中添加标尺可进一步提高文本对齐度，表明空间参考框架对LLM空间推理具有辅助作用。

在身份保持生成方面，与迭代Insert-Anything方法相比，采用SIGMA-Gen进行深度和身份联合控制（Figure 3）在保持更高文本对齐度的同时显著提升了图像质量，证明了多主体身份显式建模的必要性。

### 创新边界与局限

尽管三维空间草稿板在文本对齐上取得了显著提升（GenAI-Bench上32%的相对改进），方法仍存在若干局限：LLM生成的物体放置可能过于均匀，缺乏真实场景的自然构图多样性；对于复杂的交互活动（如握手、追逐），活动理解与朝向规划可能失败；生成的3D网格姿态多样性有限，无法调整铰接式资产的关节。这些局限指向了未来将物理模拟器纳入或通过强化学习优化构图的可能方向。

## 整体框架

三维空间草稿板的核心思想是将一个结构化的三维场景作为文本到图像生成的中间推理基底，使语言模型能够在渲染前进行显式的空间推理。整个pipeline采用多代理协作架构，将复杂的文本到图像生成任务分解为若干个可解释的子任务，每个子任务由专门的LLM代理负责。

**输入与输出**：系统接收一个自然语言提示 $P$ 作为输入，最终输出一张与提示高度对齐、且保持多主体身份一致性的图像。中间过程通过一个预定义的三维空间 $D$ 进行桥接——该空间是一个带有地平面和固定边界（X、Y、Z轴）的空场景。

**pipeline模块与数据流**：如 Figure 2 所示，整个流程由四个核心代理依次协作完成：

1. **SubjectInstantiation（代理①）**：解析输入提示 $P$，识别并分解出各个主体和背景元素，生成增强提示 $P'$ 和每个主体的文本描述 $\mathcal{S}^{\mathrm{P}}$。该代理还负责获取每个主体的身份图像 $\mathcal{S}^{\mathrm{I}}$ 和宽高比信息 $\mathcal{S}^{\mathrm{A}}$。

2. **BboxPlanner（代理②）**：基于增强提示、主体描述、身份图像、宽高比和三维空间描述，为每个主体生成三维边界框 $\mathcal{S}^{\mathrm{BBOX}}$，完成初始空间放置。其形式化定义为：
   $$\mathcal{S}^{\mathrm{BBOX}} = \mathrm{BboxPlanner}(P', \mathcal{S}^{\mathrm{P}}, \mathcal{S}^{\mathrm{I}}, \mathcal{S}^{\mathrm{A}}, D)$$

3. **OrientationEstimator + TransformPlanner（代理③）**：首先由OrientationEstimator利用生成图像的裁剪区域估计每个主体的当前绝对朝向 $\mathcal{S}^{\mathrm{O_{est}}}$；随后TransformPlanner结合增强提示、多视角渲染 $R$、估计朝向、目标朝向 $\mathcal{S}^{\mathrm{O_{tgt}}}$ 和主体描述，输出三维变换建议 $\mathcal{S}^{\mathrm{TR}}$（包括旋转、平移和缩放）：
   $$\mathcal{S}^{\mathrm{TR}} = \mathrm{TransformPlanner}(P', R, S^{\mathrm{O_{est}}}, S^{\mathrm{O_{tgt}}}, S^{\mathrm{P}}, D)$$

4. **CameraPicker（代理④）**：从五个预设提案视图中选择与提示 $P$ 最匹配的最终摄像机视角，确保所有主体都在画面内。

**生成与编辑闭环**：确定三维配置后，系统使用SIGMA-Gen进行深度和身份联合控制的图像生成，在单次去噪循环中同时保持多主体身份和空间结构。此外，SubjectEditor代理支持将用户编辑指令（手动或文本）转换为三维变换，实现生成后的一致性编辑：
$$\mathcal{S}^{\mathrm{TR}} = \mathrm{SubjectEditor}(E, I, C, \mathcal{S}^{\mathrm{P}}, \mathcal{S}^{\mathrm{BBOX}}, D)$$

这一架构的关键优势在于：三维空间作为因果调节因子，直接控制最终图像的空间准确性和身份一致性，使得复杂提示的遵循度显著提升——在GenAI-Bench上实现了32%的文本对齐改进，且无需额外训练。

### 补充图表

![[assets/figures/papers/paper_list_l2160_https_arxiv_org_abs_2601_14602/figures/002_Figure_2.jpg]]
*Figure 2: Overview of a 3D spatial scratchpad. Given an input prompt P we illustrate how our method uses a 3D space as an underlying representation to generate an image that has superior alignment to the prompt. Agent ⃝1 is responsible for decomposing the input prompt into subjects and background. Agent ⃝2 provides 3D bounding boxes for each subject. We render the scratchpad and subsequently generate an image based on these placements which is then given to agent ⃝3 that adjusts transformations of the meshes. Finally, agent ⃝4 chooses the best camera viewpoint from a set of proposals to generate the final image*

## 核心模块与公式推导

### 三维空间草稿板的定义

方法的核心是一个**三维空间草稿板**——一个带有地平面和X、Y、Z轴固定边界的空场景。该草稿板作为文本到图像生成的中间推理基底，使LLM代理能够在渲染前进行显式的空间推理。给定文本提示，系统通过一个代理框架将生成过程分解为多个子任务，每个子任务由专门的LLM代理完成。

### 代理流水线模块

整个流水线包含四个核心代理和一个编辑代理：

**Agent ① — SubjectInstantiation（主体实例化）**  
负责将输入提示解析为独立的主体和背景元素，提取每个主体的描述 $s_1^P, s_2^P, \ldots s_n^P \in \mathcal{S}^\mathrm{P}$，并生成增强提示 $P'$。

**Agent ② — BboxPlanner（边界框规划器）**  
为每个主体生成三维边界框并完成初始放置。其形式化定义为：

$$\mathcal{S}^{\mathrm{BBOX}} = \mathrm{BboxPlanner}(P', \mathcal{S}^{\mathrm{P}}, \mathcal{S}^{\mathrm{I}}, \mathcal{S}^{\mathrm{A}}, D)$$

其中：$P'$ 为增强提示，$\mathcal{S}^{\mathrm{P}}$ 为主体描述集，$\mathcal{S}^{\mathrm{I}}$ 为主体身份图像集，$\mathcal{S}^{\mathrm{A}}$ 为主体长宽比信息，$D$ 为三维空间描述。输出 $\mathcal{S}^{\mathrm{BBOX}}$ 包含每个主体的三维边界框参数。

**Agent ③ — OrientationEstimator + TransformPlanner（朝向估计与变换规划器）**  
该阶段由两个子代理协作完成：OrientationEstimator 利用生成图像的裁剪区域估计每个主体的当前绝对朝向 $\mathcal{S}^{\mathrm{O_{est}}}$；TransformPlanner 结合目标朝向 $\mathcal{S}^{\mathrm{O_{tgt}}}$ 和多视角渲染 $R$，建议三维变换（旋转、平移、缩放）：

$$\mathcal{S}^{\mathrm{TR}} = \mathrm{TransformPlanner}(P', R, \mathcal{S}^{\mathrm{O_{est}}}, \mathcal{S}^{\mathrm{O_{tgt}}}, \mathcal{S}^{\mathrm{P}}, D)$$

其中 $R$ 为多视角渲染结果，$\mathcal{S}^{\mathrm{TR}}$ 为输出的三维变换参数集。

**Agent ④ — CameraPicker（摄像机选择器）**  
从五个提案视图中选择与提示 $P$ 最匹配的最终摄像机视角 $C$。五个提案视图被构造为能够将所有主体包含在画面内。

**Edit Agent — SubjectEditor（主体编辑器）**  
支持在生成图像后进行三维一致性编辑，将用户编辑指令（手动或文本）转换为三维变换：

$$\mathcal{S}^{\mathrm{TR}} = \mathrm{SubjectEditor}(E, I, C, \mathcal{S}^{\mathrm{P}}, \mathcal{S}^{\mathrm{BBOX}}, D)$$

其中 $E$ 为用户编辑指令，$I$ 为当前图像，$C$ 为摄像机参数，$\mathcal{S}^{\mathrm{BBOX}}$ 为当前边界框配置。

### 身份保持生成模块

最终图像生成采用 **SIGMA-Gen** 作为身份保持生成器。该选择的关键原因是 SIGMA-Gen 能够在单次去噪循环中同时处理多主体身份控制和深度控制。系统将深度图、增强提示和身份图像联合输入 SIGMA-Gen，生成保持多主体身份和空间结构的最终图像。消融实验表明，仅使用深度和提示引导（无身份控制）会导致多主体复杂规划场景中的文本对齐性下降，而加入身份控制后显著提升了提示遵循度。

### 基于裁剪的朝向估计策略

朝向估计是该方法的一个关键技术细节。实验对比了三种策略：(A) 直接向LLM提供全场景多视角渲染并要求输出变换矩阵——该方法无法产生正确的旋转；(B) 从完整合成图像估计朝向——对部分物体可靠但对其他物体产生错误预测；(C) 提出的**基于裁剪的分解策略**——将每个物体从图像中裁剪出来，使LLM独立推断其朝向，然后将估计朝向与目标朝向一起传递给TransformPlanner。策略(C)产生了远更准确的旋转预测，为复杂旋转场景提供了关键的鲁棒性。尽管基准测试中朝向敏感样本较少导致定量增益有限（Table 3），但定性分析表明该策略对保证文本准确性至关重要。

![[assets/figures/papers/paper_list_l2160_https_arxiv_org_abs_2601_14602/figures/016_Figure_11.jpg]]
*Figure 11: Strategies for determining rotations. We examine a scenario that requires accurate rotation planning for multiple objects described in a natural language prompt. A: Directly providing the LLM with multiview renders of the entire scene and asking it to output transformation matrices fails to produce correct rotations. B: Estimating orientations from the full synthesized image also proves unreliable: while the pickup truck is interpreted correctly, both chairs receive incorrect orientation predictions. C: Our proposed strategy isolates each object by cropping its image, enabling the LLM to infer its orientation independently; these estimated orientations, paired with the desired target orient...*

### 补充图表

![[assets/figures/papers/paper_list_l2160_https_arxiv_org_abs_2601_14602/figures/003_Figure_3.jpg]]
*Figure 3: Identity preservation improves prompt adherence. We show that complex planning among multiple subjects even when guided with only depth and prompt can lead to loss of text alignment. In contrast, we opt to use depth, prompt, and identity to generate the images thus preserving prompt adherence*

## 实验与分析

### 主实验：文本对齐度的跨基准提升

方法在三个具有不同空间推理难度的基准上，与仅使用文本推理（**Idea2Img**，Yang et al., 2023）和基于二维布局推理（**RPG**，Yang et al., ICML 2024）的基线进行了系统比较，底层生成模型统一采用 **Flux.1 [dev]**。

**Table 1** 汇总了核心结果。在 **GenAI-Bench** 上，3D Spatial Scratchpad 的文本对齐度（VQAScore）达到 **0.83**，相比 Flux.1 [dev] 基线的 0.63 提升了 +0.20，相对改善幅度为 **32%**；同时图像质量保持稳定。在 **CompoundPrompts** 基准上，文本对齐度从基线的 0.73 提升至 **0.91**（+0.18）。在 **T2I-CompBench** 的 Complex 类别上，3-in-1 指标从 0.37 提升至 **0.65**（+0.28，见 Table 6）。

上述提升的关键因果机制在于：三维空间草稿板将“空间推理”外化为可操作的中间表示——主体放置、朝向调整和摄像机选择均在渲染前显式完成，从而绕过了文本到像素生成模型内部空间推理能力不足的瓶颈。相比之下，Idea2Img 仅通过文本迭代优化提示，RPG 仅在二维布局层面规划，均缺乏对三维空间关系的显式建模。

**Figure 6** 进一步展示了 GenAI-Bench 五个推理子类别的细分表现。3D Spatial Scratchpad 在 Counting、Comparison、Differentiation、Negation 和 Universal 全部五个类别上均一致优于先前方法。值得注意的是，方法在 **Negation（否定）** 类别上取得了相对基线最大的提升幅度，这表明显式的空间约束（如“A 不在 B 的左边”）在三维草稿板中更容易被准确表达和验证。

### 消融实验：各代理模块的因果贡献

为量化四个 LLM 代理各自的作用，作者以仅使用 Agent ①（主体实例化）和 Agent ②（边界框放置）的配置为基线，逐步添加 Agent ③（朝向估计与变换规划）和 Agent ④（摄像机选择），在 GenAI-Bench 上测量文本对齐度的变化（**Table 3**）。

![[assets/figures/papers/paper_list_l2160_https_arxiv_org_abs_2601_14602/figures/006_Table_3.jpg]]
*Table 3: Impact of each agent. On GenAI-Bench, we show that both the ⃝3 and ⃝4 agents offer progressive improvement in text alignment while image quality stays stable across the ablations*

结果显示，逐步添加 Agent ③ 和 ④ 带来了 **渐进式的文本对齐度提升**（0.821 → 0.824 → 0.830），而图像质量在所有消融配置中保持稳定。这一单调递增的趋势表明：

- **朝向规划（Agent ③）** 是纠正复杂旋转场景中空间错误的关键环节。消融中进一步揭示，基于裁剪的朝向估计策略（Crop-based decomposition，见 Figure 11）比全图估计更准确——尽管 GenAI-Bench 中朝向敏感样本占比较低，导致定量增益有限，但在需要精确旋转的多物体场景中，该策略是保证正确性的必要条件。
- **摄像机选择（Agent ④）** 通过从五个提案视图中选出与提示最匹配的视角，进一步消除了因默认正面视角导致的空间歧义。

**Table 2** 考察了提示增强的协同效应。将 Idea2Img 的迭代优化提示与 3D Spatial Scratchpad 结合使用时，文本对齐度进一步提升至 **0.85**，表明文本层面的提示优化与空间层面的草稿板推理是互补的。但值得注意的是，Idea2Img 若仅执行单次迭代（Idea2Img*），其性能显著下降（0.75），这反衬出 3D 草稿板在单次推理中即可实现高效空间规划的优势。

**Table 4** 分析了草稿板渲染设计的影响。在渲染图像中添加**标尺（rulers）** 可进一步提高文本对齐度——标尺为 LLM 代理提供了显式的空间尺度参照，有助于更精确的边界框放置和变换规划。

### 身份保持生成方法的消融

**Table 5** 比较了两种身份保持生成策略。使用 **SIGMA-Gen** 进行多主体身份和深度联合控制，相比迭代式的 Insert-Anything + depth ControlNet 方案，在图像质量上有显著提升，同时文本对齐度保持更高水平。Figure 3 的定性对比显示，仅依赖深度和提示进行多主体规划容易导致文本对齐度损失，而显式的身份图像控制是保持提示一致性的关键。

### 失败模式与局限性

**Figure 8** 展示了两个主要失败模式：

1. **构图均匀性偏差**：LLM 生成的物体放置倾向于过于均匀，缺乏真实场景中自然构图的不对称性和多样性。这是由于 LLM 在缺乏视觉先验的情况下，倾向于“安全”的规则布局。
2. **复杂交互的朝向理解失败**：在涉及复杂交互活动（如握手、追逐）的场景中，活动理解与朝向规划可能出错。当前系统无法调整铰接式资产的关节，限制了动态动作的表达能力。

此外，系统依赖多个预训练模型（文本到 3D 生成、图像生成、身份保持生成），端到端训练尚不可用，这构成了工程部署层面的限制。

### 三维编辑一致性验证

**Figure 7** 展示了空间草稿板的编辑能力：无论是手动拖拽编辑还是基于文本的编辑指令，对三维草稿板的修改都能一致地反映到最终生成图像中，同时保持主体身份和背景不变。这一特性源于编辑操作发生在统一的三维空间表示层——SubjectEditor 代理（Equation 3）将用户编辑指令转换为三维变换，随后通过相同的深度+身份条件生成管线渲染，确保了编辑前后的空间一致性和身份保真度。

### 补充图表

![[assets/figures/papers/paper_list_l2160_https_arxiv_org_abs_2601_14602/figures/004_Table_1.jpg]]
*Table 1: Quantitative comparison with baselines. We show that using a 3D space as a reasoning scratchpad improves text alignment compared to using only text or a 2D space as a reasoning modality. We also maintain or improve in terms of image quality*

![[assets/figures/papers/paper_list_l2160_https_arxiv_org_abs_2601_14602/figures/011_Figure_6.jpg]]
*Figure 6: Comparison of text-to-image performance in GenAI-Bench. We evaluate our spatial scratchpad framework against stateof-the-art text-to-image systems on five reasoning categories—Counting, Comparison, Differentiation, Negation, and Universal—as well as the overall average. Scores reflect VQAScore accuracy (higher is better). Across all categories, our single-iteration variants (Ours+SIGMAGen and Ours+Idea2Img) consistently outperform prior models. Notably, Idea2Img* here denotes the single-iteration version of Idea2Img (without multi-step refinement), allowing a fair comparison with our own single-pass inference*

![[assets/figures/papers/paper_list_l2160_https_arxiv_org_abs_2601_14602/figures/005_Table_2.jpg]]
*Table 2: Impact of prompt enhancement. On GenAI-Bench, we show that using the iteratively improved prompt from Idea2img works complementarily to our approach and offers further improvement. We also show that using the Idea2img method but only for a single iteration reduces their performance significantly. We also maintain image quality with the different prompts*

![[assets/figures/papers/paper_list_l2160_https_arxiv_org_abs_2601_14602/figures/007_Table_4.jpg]]
*Table 4: Impact of design choice of renders. On GenAI-Bench, we show that adding rulers to the 3D scratchpad’s rendered images improves text alignment. With rulers the performance remains comparable. Image quality stays stable over all the choices*

![[assets/figures/papers/paper_list_l2160_https_arxiv_org_abs_2601_14602/figures/009_Table_5.jpg]]
*Table 5: Impact of identity preserved image generation method. On GenAI-Bench, we show that Iterative Insert-Anything* (row 1), which refers to iterative insertion of subjects using Insert-Anything + depth ControlNet, leads to reduction of quality, however text alignment stays higher than other baselines*

![[assets/figures/papers/paper_list_l2160_https_arxiv_org_abs_2601_14602/figures/013_Figure_8.jpg]]
*Figure 8: Limitations. We show that our LLM generated subject placements can be too uniform unlike real image compositions. Secondly, we find that activity and orientation understanding/planning may fail in cases of complex interactions*

![[assets/figures/papers/paper_list_l2160_https_arxiv_org_abs_2601_14602/figures/012_Figure_7.jpg]]
*Figure 7: 3D as a spatial scratchpad enables consistent image editing. Given the input prompt, we show the subjects instantiated, the scratchpad created and the subsequent image generated in the first column. In the succeeding columns, we show how edits made either through a) manual editing, or b) text-based editing to the scratchpad can be consistently reflected on to the final image while conserving identities of subjects and the background. Each column shows a progressive edit made over the state in the previous column*

![[assets/figures/papers/paper_list_l2160_https_arxiv_org_abs_2601_14602/figures/017_Figure_12.jpg]]
*Figure 12: Various rendering designs explored. We illustrate the different rendering configurations explored in our design ablation, shown here only for the front-view camera but applied analogously to all viewpoints. Each variant corresponds to the ordered settings listed in Table 4, including changes to background color, ruler visibility, and grid placement. Rulers are drawn up to fixed spatial bounds to constrain object placement, and cameras are positioned with fixed viewing directions and distances chosen to ensure all meshes remain fully visible*

## 方法谱系与知识库定位

### 核心创新定位

本文的核心贡献在于将**三维空间作为文本到图像生成的中间推理草稿板**，而非直接改进扩散模型架构或训练策略。这一范式转变的本质是：将语言模型的结构化空间推理能力外化到三维几何表示中，使视觉生成过程获得类似“思维链”的空间思考能力。该思路与现有方法的根本差异在于**推理模态的选择**——从纯文本推理（如 **Idea2Img** (Yang et al., 2023)）或二维布局推理（如 **RPG** (Yang et al., ICML 2024)）跃迁到三维空间推理。

因果调节的关键变量是**三维空间草稿板表示**：通过显式放置、定向和摄像机选择主体，该方法直接控制了最终图像的空间准确性和身份一致性。这一设计的核心洞察在于，三维空间提供了比文本或二维布局更丰富的约束信息（深度、遮挡、相对朝向），从而显著降低了生成模型在复杂空间关系上的推理难度。

### 与基线方法的关系

#### 与推理模态基线的关系

**Idea2Img** (Yang et al., 2023) 代表了基于文本的迭代推理范式：通过LLM反复优化提示词来提升图像质量，但缺乏显式的空间表示。本文的方法在以下维度上与之形成互补而非替代关系：
- 实验表明，将 Idea2Img 的迭代提示增强与三维空间草稿板结合使用，可在 GenAI-Bench 上进一步将文本对齐度从 0.83 提升至 0.85（Table 2），说明两种推理机制具有可叠加性。
- 但 Idea2Img 在单次迭代下性能显著下降，而本文方法在单次推理中即保持高效，体现了空间草稿板的推理效率优势。

**RPG** (Yang et al., ICML 2024) 引入了二维布局作为推理模态，但二维表示无法处理深度排序、三维遮挡和视角选择等空间推理需求。Table 1 的定量对比显示，三维空间草稿板在 GenAI-Bench（0.83 vs. 基线的 0.63）和 CompoundPrompts（0.91 vs. 0.73）上均显著优于二维推理模态，验证了三维表示在空间推理上的不可替代性。

#### 与生成模型基线的关系

本文方法以 **Flux.1 [dev]** 作为基础文本到图像生成模型，并在其上叠加身份保持生成模块 **SIGMA-Gen**。选择 SIGMA-Gen 的关键动机在于其能够**同时处理多主体身份保持和深度控制**，这使得三维草稿板中的空间约束（深度图）和身份要求（参考图像）可以在单次去噪循环中联合注入，避免了迭代式插入方法（如 Insert-Anything + depth ControlNet）带来的图像质量退化（Table 5）。

### 方法适用边界

#### 有效场景
- **多主体空间关系规划**：需要精确控制多个对象之间的相对位置、朝向和遮挡关系的提示词。
- **视角敏感生成**：提示词中隐含特定观察视角要求（如“从左侧看”、“俯视角度”）的场景。
- **身份保持的组合生成**：需要保持特定主体身份同时进行空间布局控制的场景，得益于 SIGMA-Gen 的联合控制能力。
- **可编辑性需求**：生成后需要手动或文本驱动调整主体位置、朝向的场景，三维草稿板天然支持一致性编辑（Figure 7）。

#### 失效模式与局限

1. **构图多样性不足**：LLM 生成的物体放置倾向于过于均匀，缺乏真实场景中自然构图的不对称性和视觉张力（Figure 8）。这源于LLM在空间推理中倾向于“安全”的平衡布局，而非模拟人类摄影或绘画中的构图美学。

2. **复杂交互活动理解失败**：对于涉及动态交互的提示词（如“握手”、“追逐”），系统的活动理解和朝向规划可能失效（Figure 8）。这一局限的根源在于：当前系统仅能调整刚体变换（旋转、平移、缩放），无法处理铰接式资产的关节姿态，限制了动态动作的表达能力。

3. **朝向估计的基准敏感性**：基于裁剪的朝向估计策略（Figure 11）在定性上显著优于全图估计，但由于 GenAI-Bench 等基准测试中朝向敏感样本占比低，定量增益有限（Table 3）。这意味着该模块的实际价值可能被现有基准低估，需要专门设计的朝向敏感测试集来充分验证。

4. **多模型依赖的工程复杂性**：当前系统依赖多个预训练模型（文本到3D网格生成、图像生成、身份保持生成、LLM代理），端到端训练尚不可用。这种模块化设计虽然灵活，但引入了级联误差的风险，且各模块的独立优化未必保证全局最优。

### 开放问题与后续方向

1. **构图自然性优化**：是否可以通过验证步骤（如引入美学评分模型作为反馈）或强化学习（将构图多样性作为奖励信号）来提高生成布局的自然性和多样性？

2. **物理交互模拟**：将物理模拟器纳入空间草稿板，以支持更真实的物体交互（如重力约束、碰撞检测、支撑关系），可能解决当前复杂交互活动理解的失败问题。

3. **时空扩展**：空间草稿板是否可以扩展到视频生成领域，将三维空间推理与时间维度结合，形成四维时空草稿板，以支持时空一致的动态场景生成？

4. **端到端训练**：如何减少对多个预训练模型的依赖，将空间推理过程嵌入到可端到端训练的框架中？这可能涉及将三维草稿板表示作为可微分的中间层，或通过知识蒸馏将LLM的空间推理能力迁移到专用的空间规划模块中。

5. **朝向敏感基准构建**：现有基准对朝向规划的敏感性不足，需要构建专门评估空间朝向理解的数据集，以更准确地衡量该类方法在视角控制上的能力边界。

### 知识库定位总结

本文在文本到图像生成领域的方法谱系中占据了一个独特位置：它不直接竞争扩散模型架构的改进（如 SDXL、Flux 等），也不替代提示优化方法（如 Idea2Img），而是**在提示理解与像素生成之间插入了一个三维空间推理层**。这一设计使其与现有方法形成互补关系——空间草稿板可以与更强大的基础生成模型或更精细的提示优化策略结合使用，获得叠加增益。

从更宏观的视角看，这项工作呼应了视觉生成领域的一个趋势：将生成过程从“端到端黑箱映射”转向“结构化推理+条件生成”的范式。与思维链提示在语言模型中引发的能力涌现类似，三维空间草稿板为视觉生成引入了“空间思考”的中间阶段，其核心价值在于将隐式的空间推理需求转化为显式的几何约束，从而降低生成模型的学习难度。

## 原文 PDF

![[paperPDFs/CVPR_2026/3D_Space_as_a_Scratchpad_for_Editable_Text_to_Image_Generation.pdf]]