---
title: "Generate, Analyze, and Refine: Training-Free Sound Source Localization via MLLM Meta-Reasoning"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/Generate_Analyze_and_Refine_Training_Free_Sound_Source_Localization_via_MLLM_Meta_Reasoning.pdf
project_link: null
code_link: "https://github.com/VisualAIKHU/GAR-SSL"
aliases:
- GARG
- GARTFSSLMMR
tags:
- CVPR_2026
- topic/generative_models_diffusion
- topic/generative_models_diffusion/diffusion_image_video
core_operator: 引入多模态大语言模型（MLLM）的内在元推理能力，将声源定位重构为“生成-分析-精炼”三步认知推理流水线，替代端到端的比对学习范式。
primary_logic: 通过生成阶段扩大假设空间保留声源候选，分析阶段利用开放集角色标签、锚点投票、视听一致性评分等可解释机制进行精细化验证，精炼阶段结合自适应门控避免过度调整，从而无需训练即可获得精确、可靠的定位结果。
claims:
- GAR-SSL 在 MUSIC-Duet 多声源基准上大幅超越所有现有方法，CIoU@0.3 从 45.9%（OA-SSL）提升至 82.7%，AUC 从 36.1% 提升至 53.2%。
- 消融实验表明，完整的生成-分析-精炼流水线比仅使用 Stage 1 有大幅提升，CIoU@0.3 从 42.6 升至 59.5。
- 在 VGGSound-Single 单声源基准上，GAR-SSL 同样显著优于 SOTA，AP 从 51.7%（OA-SSL）提升至 60.5%。
- VGGSound-Duet 上 CIoU@0.3 = 77.6
---

# Generate, Analyze, and Refine: Training-Free Sound Source Localization via MLLM Meta-Reasoning

> [!tip] 核心洞察
> 通过生成阶段扩大假设空间保留声源候选，分析阶段利用开放集角色标签、锚点投票、视听一致性评分等可解释机制进行精细化验证，精炼阶段结合自适应门控避免过度调整，从而无需训练即可获得精确、可靠的定位结果。

| 字段 | 内容 |
|------|------|
| 中文题名 | 生成、分析、精炼：基于多模态大语言模型元推理的无训练声源定位 |
| 英文题名 | Generate, Analyze, and Refine: Training-Free Sound Source Localization via MLLM Meta-Reasoning |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2604.06824) · [Code](https://github.com/VisualAIKHU/GAR-SSL) |
| Topic | #topic/generative_models_diffusion #topic/generative_models_diffusion/diffusion_image_video |
| Method | Generation-Analysis-Refinement (GAR) 声源定位框架 |
| Dataset | VGGSound-Duet, MUSIC-Duet, VGGSound-Single, MUSIC-Solo |

> [!tip] 效果简介
> - VGGSound-Duet 上，CIoU@0.3 77.6 vs 55.2 (OA-SSL) (+22.4)。
> - MUSIC-Duet 上，AUC 53.2 vs 36.1 (OA-SSL) (+17.1)。
> - VGGSound-Single 上，AP 60.5 vs 51.7 (OA-SSL) (+8.8)。

## 概述

声源定位（Sound Source Localization, SSL）旨在从图像-音频对中识别发声物体的空间位置。现有方法将 SSL 建模为纯粹的视听特征匹配问题——通过对比学习或注意力机制对齐视觉与音频嵌入，输出热图或注意力图。然而，这种范式缺乏显式推理与因果验证能力，在复杂声学场景中暴露出系统性缺陷：无声物体干扰、屏外声源误判、多声源混淆等问题导致定位失效。

本文提出 **GAR-SSL**（Generation-Analysis-Refinement SSL），一个**无需训练（training-free）的零样本声源定位框架**。核心洞察在于：将多模态大语言模型（MLLM）的内在元推理能力引入 SSL，将定位任务重构为“生成-分析-精炼”三步结构化认知推理流水线，替代端到端的特征比对范式。该框架通过提示工程驱动，无需任何训练数据或模型微调。

方法定位上，GAR-SSL 与现有 SSL 方法存在本质差异：

- **训练范式**：从需要大规模标注数据的对比学习，转变为纯提示驱动的零样本推理；
- **推理机制**：从隐式的特征相似度匹配，转变为可解释的元推理——生成阶段扩大假设空间保留候选，分析阶段通过开放集角色标签、锚点投票、视听一致性评分进行精细化验证，精炼阶段结合自适应门控避免过度调整；
- **输出形式**：从模糊的概率热图，转变为带因果解释和置信度的显式边界框。

实验结果表明，GAR-SSL 在单声源与多声源基准上均大幅超越现有方法。在 MUSIC-Duet 多声源基准上，CIoU@0.3 从当前最优方法 OA-SSL（Um et al., CVPR 2025）的 45.9% 提升至 82.7%，AUC 从 36.1% 提升至 53.2%；在 VGGSound-Single 单声源基准上，AP 从 51.7% 提升至 60.5%。消融实验证实，完整的生成-分析-精炼流水线是性能提升的关键——仅使用 Stage 1 时 CIoU@0.3 为 42.6，引入分析与精炼后跃升至 59.5。多次采样共识机制（N=5）进一步稳定了随机解码带来的波动。

该工作的主要局限在于推理成本较高（单样本约 4 秒，RTX 4090），且当前仅处理单帧图像，未利用视频时间连续性信息。

## 背景与动机

声源定位（Sound Source Localization, SSL）旨在从图像-音频对中识别发出声音的视觉区域，是视听理解的核心任务之一。现有 SSL 方法普遍将该问题建模为**视听特征匹配**——通过对比学习或注意力机制，在共享嵌入空间中寻找视觉与音频信号最相似的区域。这一范式在简单场景下有效，但其根本瓶颈在于**缺乏显式推理与因果验证**：模型仅输出概率热图或注意力图，无法解释“为何该区域是声源”，也难以区分“看起来像声源但实际无声”的物体（如静止的乐器）与“屏外声源”或“多声源混淆”等复杂情况。

这一瓶颈在真实声学场景中尤为突出。当画面中存在多个潜在声源物体时，纯特征匹配方法容易将高响应分配给视觉上显著但与当前声音无关的区域；当声源位于画面之外时，模型仍会在图像内强行定位，产生幻觉式输出。此外，现有方法几乎全部依赖**大规模标注数据的有监督训练**，泛化到新场景或新声源类别时需要重新训练或微调，部署成本高昂。

针对上述问题，本文提出一个核心洞察：**多模态大语言模型（MLLM）具备内在的元推理（meta-reasoning）能力，可以通过结构化的认知推理流水线替代端到端的比对学习范式，实现无需训练的声源定位。** 具体而言，本文将 SSL 重构为“生成-分析-精炼”（Generation-Analysis-Refinement, GAR）三步推理过程：生成阶段扩大假设空间以保留声源候选；分析阶段利用开放集角色标签、锚点投票、视听一致性评分等可解释机制进行精细化验证；精炼阶段结合自适应门控避免过度调整。这一框架无需任何训练数据或模型微调，仅通过提示工程即可驱动 MLLM 完成从粗到细的定位推理，同时输出因果解释和置信度评分，使定位过程透明、可验证。

与现有工作的根本区别在于：**GAR-SSL 将 SSL 从“特征匹配”问题转变为“认知推理”问题**。传统方法（如 **OA-SSL**（Um et al., CVPR 2025））依赖对比学习训练，输出不可解释的热图；无训练方法（如 **NoPrior**（Chen et al., CVPR 2024））虽免除了训练，但仍基于冻结视觉编码器的相似度计算，缺乏语义推理。直接使用现成 MLLM（如 **Qwen2.5-Omni**（Xu et al., arXiv 2025））进行端到端定位则因缺乏结构化推理而性能有限。GAR-SSL 通过引入显式的分析-验证-精炼循环，首次使 MLLM 在 SSL 任务上超越专门训练的 SOTA 方法，同时保持零样本、免训练的特性。

## 核心创新

### 范式跃迁：从特征匹配到认知推理

现有声源定位（SSL）方法，包括当前 SOTA 的 **OA-SSL**（Um et al., CVPR 2025）和训练无关方法 **NoPrior**（Chen et al., CVPR 2024），其核心瓶颈在于将 SSL 建模为纯粹的视听特征匹配问题——通过对比学习或冻结编码器提取的相似度热图来定位声源。这一范式在复杂声学场景中系统性失效：当画面中存在无声物体、声源位于屏幕外或多声源混淆时，缺乏显式推理能力的模型无法进行因果验证，只能输出不可靠的概率分布。

GAR-SSL 的根本创新在于**将声源定位从端到端的比对学习范式重构为结构化的认知推理流水线**。这一范式跃迁体现在三个维度的 changed slots 上：

1. **训练范式**：从需要大规模标注数据的对比学习训练，转变为完全基于提示工程的无训练（training-free）零样本框架。MLLM 的内在世界知识和推理能力替代了从数据中学习到的特征映射。

2. **核心推理机制**：从单步的“特征相似度匹配”转变为“生成-分析-精炼”三元认知推理。模型不再输出模糊的热图，而是经历完整的假设生成、证据验证和几何修正过程，产生带因果解释和置信度的显式边界框。

3. **输出形式与定位流程**：从概率分布式的注意力图转变为可解释的边界框，并引入多步自适应精炼机制——通过自适应门控判断何时需要调整，避免对已足够精确的预测进行过度修正。

### 三阶段认知推理的机制创新

GAR-SSL 的三阶段流水线并非简单的模块堆叠，而是模拟了人类声源定位的认知过程：

**Stage 1（生成）** 的核心创新在于**扩大假设空间**。传统方法直接输出单一预测，而 GAR-SSL 的生成阶段同时产生产物边界框、视觉描述、开放词汇音频分类和音频置信度——这些多元输出为后续分析阶段提供了丰富的验证素材，避免了过早收敛到错误假设。

**Stage 2（分析）** 引入了三个可解释的验证机制，构成了框架中最具原创性的部分：

- **开放集角色标签**：MLLM 动态发现与声源直接相关的语义角色（如“吉他弦”、“音箱喇叭”），而非依赖预定义的封闭类别。这一开放集设计使模型能够泛化到训练中未见过的声源类型。
- **锚点投票**：基于声学事件和视觉证据产生语义锚点及其置信度，通过多个锚点的加权投票来量化定位质量，提供了比单一相似度分数更稳健的空间置信度度量。
- **视听一致性评分**：综合角色标签和锚点信息，衡量预测框与视听证据的语义对齐程度，作为是否触发精炼的决策依据。

**Stage 3（精炼）** 的创新在于**几何操作的语义化**。不同于传统的回归修正，GAR-SSL 的精炼操作（Delta 平移、Expand/Shrink 缩放、Recenter 重定位）直接基于分析阶段产生的语义锚点进行几何调整，使修正过程具有可解释性。

### 自适应门控与多试共识

两个关键的机制设计使推理流水线在精度和效率之间取得平衡：

- **自适应门控**（Adaptive Gating）：通过联合判断音频置信度和视听一致性得分是否超过阈值，决定是否跳过精炼阶段。这一机制避免了“为调整而调整”的冗余计算，同时防止对已准确预测的框进行破坏性修正。
- **多试共识**（Multi-trial Consensus）：通过重复分析阶段 N=5 次并投票聚合结果，有效降低了 MLLM 随机解码带来的波动性。消融实验证实，增加迭代次数持续提升性能，N=5 时达到最佳。

### 与现成 MLLM 的本质区别

直接使用现成多模态大模型（如 **Qwen2.5-Omni**，Xu et al., arXiv 2025）进行声源定位面临两个根本问题：一是缺乏结构化的空间推理能力，难以输出精确的边界框坐标；二是单次前向推理容易产生幻觉或随机偏差。GAR-SSL 通过三阶段元推理框架解决了这些缺陷——不是简单地“询问” MLLM，而是引导其进行结构化的假设-验证-修正认知循环，将 MLLM 从黑盒预测器转变为可解释的推理引擎。

## 整体框架

GAR-SSL 将声源定位从传统的视听特征匹配重构为一种**无训练、零样本**的认知推理流水线。其核心思想是将多模态大语言模型（MLLM）视为一个具有元推理能力的智能体，通过“生成—分析—精炼”三个有序阶段，逐步从粗略的初始预测收敛到精细、可解释的定位结果。图 1 给出了框架的整体概览，图 2 则展示了各阶段内部的详细数据流与模块交互。

### 输入与输出规范

框架接收一对图像-音频输入 $(I, A)$，其中 $I \in \mathbb{R}^{W \times H \times 3}$ 为 RGB 图像，$A$ 为对应的单通道音频波形。输出为：
- **精炼后的边界框** $b^{\mathrm{ref}} = [x_1, y_1, x_2, y_2]$，坐标归一化至图像尺寸范围内；
- **开放词汇音频类别** $c_{\mathrm{aud}}$（如“小提琴”、“犬吠”）；
- **因果解释文本**与**置信度评分**，用于支撑定位结果的可信度。

整个过程**无需任何训练数据或模型微调**，完全依赖提示工程驱动 MLLM 的推理行为。

### 三阶段流水线

#### Stage 1：生成（Generation）

生成阶段承担“假设生成”的职责。给定 $(I, A)$，MLLM 被提示同时执行两项任务：
1. **视听定位**：产生初始边界框 $b^{\mathrm{init}}$ 和视觉描述文本 $d$，即 $f_{\mathrm{loc}}(I, A) = (b^{\mathrm{init}}, d)$。其中 $b^{\mathrm{init}}$ 满足 $0 \leq x_1 < x_2 \leq W$，$0 \leq y_1 < y_2 \leq H$。
2. **音频分类**：输出开放词汇类别标签 $c_{\mathrm{aud}}$ 及其置信度 $s_{\mathrm{aud}} \in [0, 1]$。

这一阶段的输出元组 $\text{Gen\_out} = (b^{\mathrm{init}}, d, c_{\mathrm{aud}}, s_{\mathrm{aud}})$ 被完整传递至分析阶段。生成阶段的关键设计在于**不追求一次精准定位**，而是通过宽松的提示策略保留尽可能多的声源候选，避免过早排除正确的空间区域。

#### Stage 2：分析（Analysis）

分析阶段是框架的推理核心，充当生成与精炼之间的“认知桥梁”。它通过三个可解释的评估机制对初始预测进行多维度验证：

- **开放集角色标签**（Open-set Role Tagging）：从图像和音频中动态发现与声源直接相关的语义角色 $\mathcal{T}_{\mathrm{role}} \subseteq \mathcal{T}_{\mathrm{open}}$，例如“琴弦”、“吹嘴”、“鼓面”，且 $|\mathcal{T}_{\mathrm{role}}| \in \{0, 1, 2, 3, 4\}$。所有角色标签必须满足可见性约束 $\mathrm{vis}(t \mid I) = 1$。
- **锚点投票**（Anchor Voting）：依据声学事件和视觉证据产生语义锚点集 $\mathcal{A}_{\mathrm{anchor}} = \{(a_i, s_i)\}_{i=1}^{m}$，每个锚点附带空间坐标和置信度，用于量化初始框与声源关键部件之间的空间对齐程度。
- **视听一致性评分**（Audio-Visual Consistency Score）：综合角色标签和锚点信息，计算 $S_{\mathrm{av}} = f_{\mathrm{con}}(I, A, b^{\mathrm{init}}, c_{\mathrm{aud}}, \mathcal{T}_{\mathrm{role}}, \mathcal{A}_{\mathrm{anchor}}) \in [0, 1]$，衡量预测框与视听证据的语义对齐程度。

分析阶段同时输出一个**主观保持标志** $k \in \{0, 1\}$，表示 MLLM 认为当前框是否已足够精确。

#### Stage 3：精炼（Refinement）

精炼阶段根据分析结果对 $b^{\mathrm{init}}$ 进行几何修正。框架定义了三种原子操作：
- **Delta 修正**：根据外部锚点的加权中心对边界框进行平移和边独立调整，$b^{\mathrm{ref}} = [x_1 + dx + d_\ell, y_1 + dy + d_t, x_2 + dx + d_r, y_2 + dy + d_b]$。
- **Expand/Shrink**：当框中心合理但覆盖不均衡时，基于外部锚点占比决定缩放量 $a$，$b^{\mathrm{ref}} = [x_1 - a, y_1 - a, x_2 + a, y_2 + a]$（$a > 0$ 扩大，$a < 0$ 缩小）。
- **Recenter**：保持原始尺寸 $(w, h)$，将框中心移至外部锚点加权中心 $(c_x^*, c_y^*)$，$b^{\mathrm{ref}} = [c_x^* - w/2, c_y^* - h/2, c_x^* + w/2, c_y^* + h/2]$。

具体选择哪种操作由 MLLM 根据分析阶段的语义指导自主决策。

### 自适应门控与多试验共识

精炼并非无条件执行。框架引入**自适应门控**机制，仅在以下条件同时满足时跳过精炼（即保留 $b^{\mathrm{init}}$）：

$$G = \mathbf{1}\left((k = 1) \wedge (\bar{S}_{\mathrm{av}} \geq \tau_{\mathrm{av}}) \wedge (s_{\mathrm{aud}} \geq \tau_{\mathrm{aud}})\right)$$

其中 $\bar{S}_{\mathrm{av}} = \frac{1}{n} \sum_{i=1}^{n} S_{\mathrm{av}}^{(i)}$ 为多次分析的平均一致性得分。当 $G=1$ 时，$b^{\mathrm{ref}} = b^{\mathrm{init}}$；否则执行精炼操作 $b^{\mathrm{ref}} = \mathrm{Ref}(I, A, b^{\mathrm{init}}, c_{\mathrm{aud}}, \mathcal{A}_{\mathrm{anchor}}, \mathcal{T}_{\mathrm{role}})$。

为抑制 MLLM 随机解码带来的波动，分析阶段被重复执行 $n$ 次（默认 $n=5$），通过多数投票聚合角色标签、锚点位置和一致性评分，形成**多试验共识**。消融实验证实，$n$ 从 1 增至 5 时性能持续提升（Table 3、Table 4），验证了共识机制对稳定性的贡献。

### 与现有范式的本质区别

| 维度 | 现有方法（如 OA-SSL） | GAR-SSL |
|------|----------------------|---------|
| 训练范式 | 对比学习，需大规模标注数据 | 无训练，零样本 |
| 推理机制 | 单步特征相似度匹配 | 三阶段认知推理 |
| 输出形式 | 概率热图/注意力图 | 显式边界框 + 因果解释 + 置信度 |
| 定位流程 | 前向预测 | 自适应精炼（门控跳过不必要调整） |

这种范式转换使得 GAR-SSL 能够处理传统方法难以应对的复杂场景——无声物体干扰、屏外声源、多声源混淆——因为 MLLM 的元推理能力可以显式地区分“看起来像声源”与“实际发出声音”的物体，并通过角色标签和锚点投票进行因果验证。

### 补充图表

![[assets/figures/papers/paper_list_l2313_https_arxiv_org_abs_2604_06824/figures/001_Figure_1.jpg]]
*Figure 1: Overview of the proposed Generation-Analysis-Refinement Sound Source Localization (GAR-SSL) framework. Given an image-audio pair, the model performs three metareasoning steps: Generation produces an initial bounding box and audio label, Analysis evaluates Audio-Visual Consistency through role-based reasoning, and Refinement adjusts the localization to obtain a fine-grained final bounding box. This process enables explainable and training-free audio-visual localization*

## 核心模块与公式推导

GAR-SSL 将声源定位重构为“生成—分析—精炼”三元认知推理流水线，所有操作均通过提示工程驱动 MLLM 完成，无需任何训练。整个框架由四个关键模块串联：**Stage 1 生成**、**Stage 2 分析**、**Stage 3 精炼**，以及贯穿后两个阶段的**自适应门控**与**多次采样共识**机制。

---

### Stage 1：生成（Generation）

生成阶段接收图像-音频对 $(I, A)$，输出四个元素：

$$\text{Gen\_out} = (b^{\mathrm{init}}, d, c_{\mathrm{aud}}, s_{\mathrm{aud}})$$

其中：
- **初始边界框** $b^{\mathrm{init}}$ 定位声源候选区域，坐标定义如下：

$$b^{\mathrm{init}} = [x_1, y_1, x_2, y_2], \quad 0 \leq x_1 < x_2 \leq W, \quad 0 \leq y_1 < y_2 \leq H$$

$(x_1, y_1)$ 为左上角坐标，$(x_2, y_2)$ 为右下角坐标，限制在图像尺寸 $W \times H$ 内。

- **视觉描述** $d$：对框内声源物体的自然语言描述。
- **音频类别** $c_{\mathrm{aud}}$：开放词汇的音频分类标签。
- **音频置信度** $s_{\mathrm{aud}}$：MLLM 对音频分类的自信程度。

该阶段的核心作用在于**扩大假设空间**，不急于收敛到单一候选，而是保留尽可能多的声源可能性，为后续分析提供充分的信息基础。

---

### Stage 2：分析（Analysis）

分析阶段充当生成与精炼之间的“推理桥梁”，通过三个可解释机制评估初始预测的可靠性，并输出是否触发精炼的决策信号。

#### 2.1 开放集角色标签（Open-set Role Tagging）

从图像和音频中动态发现与声源直接相关的语义部件，而非依赖预定义类别：

$$\mathcal{T}_{\mathrm{role}} = f_{\mathrm{role}}(I, A, c_{\mathrm{aud}}) \subseteq \mathcal{T}_{\mathrm{open}}, \quad |\mathcal{T}_{\mathrm{role}}| \in \{0, 1, 2, 3, 4\}$$

每个角色标签 $t \in \mathcal{T}_{\mathrm{role}}$ 须满足可见性约束：

$$\mathrm{vis}(t \mid I) = 1 \quad \text{for all } t \in \mathcal{T}_{\mathrm{role}}$$

例如，对于“小提琴演奏”场景，可能发现 `[琴弦, 琴弓, 琴身]` 等角色，而不会生成不可见的 `[琴弓]` 如果图像中未出现。

#### 2.2 锚点投票（Anchor Voting）

依据声学事件和视觉证据，产生一组语义锚点及其置信度，用于量化定位质量：

$$\mathcal{A}_{\mathrm{anchor}} = f_{\mathrm{anchor}}(I, A, c_{\mathrm{aud}}, b^{\mathrm{init}}) = \{(a_i, s_i)\}_{i=1}^{m}$$

每个锚点 $a_i$ 是图像中的具体像素位置，$s_i$ 为其置信度分数。锚点分布与初始边界框的重叠程度直接反映定位准确度。

#### 2.3 视听一致性评分（Audio-Visual Consistency Score）

综合角色标签和锚点证据，衡量预测框与视听语义的对齐程度：

$$S_{\mathrm{av}} = f_{\mathrm{con}}(I, A, b^{\mathrm{init}}, c_{\mathrm{aud}}, \mathcal{T}_{\mathrm{role}}, \mathcal{A}_{\mathrm{anchor}}) \in [0, 1]$$

$S_{\mathrm{av}}$ 越接近 1，表示初始框与声源语义越一致；越低则越需要精炼。

---

### 自适应门控（Adaptive Gating）

门控机制决定是否跳过精炼，避免对已足够准确的预测进行过度调整：

$$G = \mathbf{1} \left( (k = 1) \wedge (\bar{S}_{\mathrm{av}} \geq \tau_{\mathrm{av}}) \wedge (s_{\mathrm{aud}} \geq \tau_{\mathrm{aud}}) \right)$$

其中：
- $k = 1$ 是 MLLM 主观判断的“保持标志”，表示模型认为当前框已足够好。
- $\bar{S}_{\mathrm{av}} = \frac{1}{n} \sum_{i=1}^{n} S_{\mathrm{av}}^{(i)}$ 是 $n$ 次分析的平均视听一致性得分。
- $\tau_{\mathrm{av}}$ 和 $\tau_{\mathrm{aud}}$ 分别为视听一致性和音频置信度的阈值（消融实验确定最佳组合为 $\tau_{\mathrm{aud}} = 0.75$，$\tau_{\mathrm{av}} = 0.5$）。

当 $G = 1$ 时，保留初始框不精炼；当 $G = 0$ 时，触发 Stage 3 精炼。

---

### 多次采样共识（Multi-trial Consensus）

为减少 MLLM 随机解码带来的波动，分析阶段重复执行 $n$ 次（实验中 $n = 5$），并对输出进行统计聚合。共识规则确保只有跨多次采样稳定出现的角色标签和锚点才被采纳，从而提升分析结果的鲁棒性。

---

### Stage 3：精炼（Refinement）

当门控判定 $G = 0$ 时，精炼阶段基于分析结果对初始框进行几何修正。框架定义了三种原子操作：

#### Delta 修正

根据外部锚点的加权中心对边界框进行平移和边独立调整：

$$b^{\mathrm{ref}} = \left[ x_{1} + dx + d_{\ell}, \; y_{1} + dy + d_{t}, \; x_{2} + dx + d_{r}, \; y_{2} + dy + d_{b} \right]$$

其中 $(dx, dy)$ 为整体平移量，$(d_{\ell}, d_{t}, d_{r}, d_{b})$ 为各边的独立微调量。

#### Expand / Shrink

当框中心合理但覆盖不均衡时，基于外部锚点占比决定缩放：

$$b^{\mathrm{ref}} = \big[ x_{1} - a, \; y_{1} - a, \; x_{2} + a, \; y_{2} + a \big]$$

$a > 0$ 表示扩大，$a < 0$ 表示缩小。缩放量由锚点落在框内外的比例动态决定。

#### Recenter

保持原始尺寸 $(w, h)$，将边界框中心移动到外部锚点的加权中心 $(c_x^*, c_y^*)$：

$$b^{\mathrm{ref}} = \left[ c_x^* - \frac{w}{2}, \; c_y^* - \frac{h}{2}, \; c_x^* + \frac{w}{2}, \; c_y^* + \frac{h}{2} \right]$$

三种操作由 MLLM 根据分析阶段提供的角色标签和锚点分布自动选择，无需人工规则干预。

---

### 模块间因果链条

整个流水线的因果逻辑可总结为：**生成阶段提供候选空间 → 分析阶段通过角色标签和锚点投票对候选进行可解释验证，输出视听一致性评分 → 自适应门控根据评分和音频置信度决定是否精炼 → 精炼阶段利用几何操作修正边界框**。多次采样共识贯穿分析阶段，抑制单次推理的随机噪声。

消融实验验证了这一因果链条的有效性：单独使用 Stage 1 时 CIoU@0.3 仅为 42.6，加入 Stage 2+3 后跃升至 59.5（Table 5），而完整的多次采样共识（$N=5$）进一步将 MUSIC-Duet 上的 CIoU@0.3 推至 82.7（Table 1）。

### 补充图表

![[assets/figures/papers/paper_list_l2313_https_arxiv_org_abs_2604_06824/figures/002_Figure_2.jpg]]
*Figure 2: The proposed training-free framework consists of three stages: (i) Generation produces initial bounding boxes and audio classifications from image-audio pairs; (ii) Analysis evaluates consistency through role tagging, anchor voting, and scoring, repeated N times for consensus; (iii) Refinement applies adaptive gating and geometric operations to adjust localization. All operations are performed via MLLMs prompt engineering without training*

## 实验与分析

### 主实验结果

GAR-SSL 在单声源和多声源两个场景下均显著超越了现有方法，验证了无训练元推理范式在声源定位任务中的有效性。

**多声源定位。** 在 VGGSound-Duet 和 MUSIC-Duet 两个多声源基准上，GAR-SSL 以 N=5 次分析迭代取得了全面领先（Table 1）。相较于此前最优的 **OA-SSL**（Um et al., CVPR 2025），CIoU@0.3 分别提升 **+22.4**（77.6 vs. 55.2）和 **+36.8**（82.7 vs. 45.9），AUC 分别提升 **+12.2**（45.8 vs. 33.6）和 **+17.1**（53.2 vs. 36.1）。这一差距在多声源混淆场景下尤为突出——MUSIC-Duet 上的相对提升超过 80%，表明元推理流水线中的开放集角色标签与锚点投票机制有效解决了无声物体干扰、屏外声源等复杂声学场景下的定位失效问题。

**单声源定位。** 在 VGGSound-Single 和 MUSIC-Solo 上，GAR-SSL 同样保持领先（Table 2）。VGGSound-Single 的 AP 从 51.7%（OA-SSL）提升至 **60.5%**，MUSIC-Solo 的 IoU@0.5 从 71.1% 提升至 **98.5%**。值得关注的是，MUSIC-Solo 上近乎饱和的性能（98.5%）表明，对于声源明确、场景简单的样本，MLLM 的内在视觉-语义对齐能力已足以完成精准定位，无需额外训练。

**与现成 MLLM 基线的对比。** 直接将 **Qwen2.5-Omni**（Xu et al., arXiv 2025）作为端到端定位器使用时，性能远低于 GAR-SSL（Table 1、Table 2），说明单纯的 MLLM 调用无法替代结构化认知推理——生成-分析-精炼流水线通过显式的角色发现、一致性评分和自适应精炼，将 MLLM 的通用能力转化为可验证的定位决策。

### 消融实验

**分析迭代次数 N 的影响。** Table 3 和 Table 4 展示了 Stage 2 多轮分析聚合的效果。N 从 1 增至 5 时，所有基准上的性能均持续提升：VGGSound-Single AP 从 60.1 升至 60.5，MUSIC-Duet CIoU@0.3 从 80.8 升至 82.7。提升幅度虽随 N 增大而递减，但 N=5 时仍未饱和，暗示进一步增加采样次数可能继续获益，但需权衡推理成本。

**三阶段框架的贡献。** Table 5 的逐阶段消融揭示了各模块的功能互补性。仅使用 Stage 1（生成初始边界框）时，CIoU@0.3 仅为 42.6；引入 Stage 2+3（分析与精炼）后跃升至 59.5，提升 **+16.9**。这一结果表明：初始生成阶段虽能提供合理的声源候选，但缺乏对定位质量的自我验证与修正能力；分析阶段的角色标签和视听一致性评分充当了“元认知”信号，精炼阶段据此进行有针对性的几何调整，二者协同实现了从粗到细的定位优化。

**MLLM 骨干规模的影响。** Table 6 对比了 Qwen2.5-Omni-7B 与 3B 版本在 VGGSound-Duet 上的表现（N=3）。7B 骨干在所有指标上均优于 3B，CIoU@0.3 从 74.8 提升至 76.9，AUC 从 44.0 提升至 45.0。这表明更大规模的 MLLM 提供了更强的视觉-语义理解能力，使角色标签发现和锚点投票更为准确。但性能增益并非线性——7B 相比 3B 的提升幅度远小于引入分析-精炼机制带来的跳跃，说明推理架构的设计比模型规模更为关键。

**提示变体的逐步验证。** Table S.8 和 S.9 通过逐步引入音频分类信息、锚点证据和元分析信息，验证了迭代精炼中信息丰富的必要性。从 Method 1（基础修正）到 Method 3（利用详细分析信息）再到完整 GAR，性能持续提升，证实了角色标签、锚点投票和视听一致性评分各自提供了不可替代的定位线索。

**门控阈值敏感性。** Table S.7 分析了音频置信度阈值（A_C）和视听一致性阈值（AV_C）对性能的影响。在 VGGSound-Single 上，最佳组合为 A_C=0.75、AV_C=0.5，此时 AP=60.5、IoU=60.2、AUC=55.2。阈值在合理范围内波动时性能变化平缓，表明自适应门控机制对超参数不敏感，具有良好的鲁棒性。

### 失败模式与局限性

尽管 GAR-SSL 在基准测试上表现优异，但分析其设计边界可识别以下失败模式：

1. **推理成本与实时性矛盾。** 单样本推理约需 4 秒（RTX 4090），主要消耗在 Stage 2 的 N=5 次迭代分析上。对于需要实时响应的应用（如机器人导航、增强现实），当前延迟不可接受。如何在保持分析深度的前提下降低迭代开销，是走向实际部署的核心瓶颈。

2. **时间信息缺失。** 框架仅处理单帧图像，无法利用视频中的帧间运动连续性。当声源快速移动或被短暂遮挡时，单帧推理可能产生空间跳跃或不一致的定位结果。引入时序推理（如跨帧锚点追踪或运动一致性约束）是自然的扩展方向。

3. **MLLM 骨干依赖性。** 当前实现深度绑定 Qwen2.5-Omni-7B，迁移至其他 MLLM 时性能可能波动。Table 6 已显示 3B 版本性能下降，若换用不同架构的 MLLM，提示工程策略可能需要重新调优，增加了方法泛化的工程成本。

![[assets/figures/papers/paper_list_l2313_https_arxiv_org_abs_2604_06824/figures/009_Table_6.jpg]]
*Table 6: Comparison of different MLLM backbones (Qwen2.5- Omni-3B vs. 7B) in the proposed framework on VGGSound-Duet. Both models serve as the foundation for all three stages (Generation, Analysis, Refinement) with analysis iterations fixed at N = 3*

4. **真实场景覆盖不足。** 现有评估集中在 VGGSound 和 MUSIC 数据集，这些数据的声学场景相对受控。在高噪声环境、多类声源密集混合、或声源与视觉对象语义不一致（如腹语术效应）的场景下，MLLM 的角色发现和锚点投票可能产生错误推理链，需进一步验证。

### 关键图表结论

- **Figure 1 与 Figure 2** 共同勾勒了 GAR-SSL 的认知推理闭环：生成阶段扩大假设空间，分析阶段引入可解释的验证信号，精炼阶段执行几何修正，三者构成从粗到细、从猜测到验证的完整决策链。
- **Table 1 与 Table 2** 是全文核心证据：多声源场景下的巨大提升（MUSIC-Duet CIoU@0.3 +36.8）证明了元推理范式在复杂声学条件下的独特优势；单声源场景下的饱和性能（MUSIC-Solo IoU@0.5 98.5%）则展示了 MLLM 在简单场景下的感知上限。
- **Table 5** 的消融结果揭示了分析-精炼机制的核心价值：Stage 1 单独使用时性能有限（CIoU@0.3 42.6），完整流水线带来近 40% 的相对提升，说明“生成后反思”是超越端到端特征匹配的关键杠杆。

![[assets/figures/papers/paper_list_l2313_https_arxiv_org_abs_2604_06824/figures/003_Table_1.jpg]]
*Table 1: Comparison of multi-source sound localization methods on VGGSound-Duet and MUSIC-Duet test sets. We evaluate three types of approaches: (i) existing vision-based SSL methods trained with task-specific objectives, (ii) off-the-shelf MLLMs baselines (Qwen2.5-Omni, MiniCPM-o, InteractiveOmni) without structured reasoning, and (iii) our proposed training-free Generation-Analysis-Refinement framework with N iterations in Stage 2 (Analysis). Bold/underlined fonts denote best/second-best performance*

![[assets/figures/papers/paper_list_l2313_https_arxiv_org_abs_2604_06824/figures/004_Table_2.jpg]]
*Table 2: Comparison of single-source sound localization methods on VGGSound-Single and MUSIC-Solo test sets. We evaluate three types of approaches: (i) existing vision-based SSL methods trained with task-specific objectives, (ii) MLLMs baselines (Qwen2.5-Omni, MiniCPM-o, InteractiveOmni) without structured reasoning, and (iii) our proposed training-free Generation-Analysis-Refinement framework with N iterations in Stage 2 (Analysis). Bold/underlined fonts denote best/second-best performance*

![[assets/figures/papers/paper_list_l2313_https_arxiv_org_abs_2604_06824/figures/010_Table_5.jpg]]
*Table 5: Effect of the proposed method on VGGSound-Duet. Stage 2 (Analysis) and Stage 3 (Refinement) are evaluated together because the gating mechanism in Stage 2 determines whether Stage 3 should be executed, making them functionally interdependent*

### 补充图表

![[assets/figures/papers/paper_list_l2313_https_arxiv_org_abs_2604_06824/figures/005_Table_3.jpg]]
*Table 3: Effect of the number of analysis iterations (N ) in Stage 2. The Stage 2 is repeated N times per sample, with multi-trial outputs aggregated through statistical consensus to enhance stability. Results on VGGSound-Single and MUSIC-Solo for N ∈ {1, 3, 5}*

![[assets/figures/papers/paper_list_l2313_https_arxiv_org_abs_2604_06824/figures/006_Table_4.jpg]]
*Table 4: Effect of the number of analysis iterations (N ) in Stage 2. The Stage 2 is repeated N times per sample, with multi-trial outputs aggregated through statistical consensus to enhance stability. Results on VGGSound-Duet and MUSIC-Duet for N ∈ {1, 3, 5}*

![[assets/figures/papers/paper_list_l2313_https_arxiv_org_abs_2604_06824/figures/007_Figure_3.jpg]]
*Figure 3: Visualization results for (a) MUSIC-Duet and (b) VGGSound-Duet test set. We compare our method with OA-SSL[40]. More comparisons are in the supplementary document*

![[assets/figures/papers/paper_list_l2313_https_arxiv_org_abs_2604_06824/figures/008_Figure_4.jpg]]
*Figure 4: Visualization results for VGGSound-Single test set. We compare our method with OA-SSL [40]. More comparisons are in the supplementary document*

![[assets/figures/papers/paper_list_l2313_https_arxiv_org_abs_2604_06824/figures/011_Table_S.7.jpg]]
*Table S.7: Analysis of the impact of Audio Confidence*

![[assets/figures/papers/paper_list_l2313_https_arxiv_org_abs_2604_06824/figures/013_Table_S.8.jpg]]
*Table S.8: Performance comparison of various prompt variation methods on single-sound source datasets. Method 1 performs basic refinement with minimal adjustments. Method 2 incorporates audio class information for refinement. Method 3 leverages detailed analysis information including visual anchors. Ours represents the proposed meta-analysis-based method with varying iteration counts (N=1, 3, 5). Evaluated on VGGSound-Single and MUSIC-Solo datasets using CAP, CIoU@0.3, and AUC metrics*

## 方法谱系与知识库定位

### 1. 与现有 SSL 方法的范式差异

现有声源定位（SSL）方法的核心范式是**视听特征匹配**：通过对比学习或注意力机制，在共享嵌入空间中最大化声源区域与音频特征之间的相似度。这一范式在单声源、简单声学场景下表现良好，但其瓶颈在于**缺乏显式推理与因果验证机制**——当场景中出现无声物体、屏外声源或多声源混淆时，纯特征相似度无法可靠区分真正的声源与视觉上相似但无声的区域。

GAR-SSL 从根本上改变了这一范式：将声源定位重构为**“生成-分析-精炼”三步认知推理流水线**，利用多模态大语言模型（MLLM）的内在元推理能力替代端到端的比对学习。具体差异体现在四个关键维度：

- **训练范式**：从需要大规模标注数据的对比学习（如 **OA-SSL**，Um et al., CVPR 2025）转向**完全无训练的提示工程**，实现了零样本部署。
- **核心推理机制**：从隐式的特征相似度匹配转向显式的**开放集角色标签发现、锚点投票和视听一致性评分**，使定位过程可解释、可验证。
- **输出形式**：从概率热图/注意力图转向**带因果解释和置信度的显式边界框**，直接输出可操作的定位结果。
- **定位流程**：从单步前向预测转向**多步自适应精炼**——通过自适应门控机制判断初始预测是否可靠，仅在不满足条件时触发几何修正操作（Delta 平移、Expand/Shrink 缩放、Recenter 重定中心），避免过度调整。

### 2. 方法谱系中的定位

GAR-SSL 位于三条研究脉络的交汇点：

**脉络一：训练依赖的视听 SSL。** 这类方法（如 **OA-SSL**，Um et al., CVPR 2025；**NoPrior**，Chen et al., CVPR 2024）依赖冻结或微调的视觉编码器，通过对比目标或定位头实现声源定位。GAR-SSL 在 VGGSound-Duet 上以 CIoU@0.3 指标 77.6% 显著超越 OA-SSL 的 55.2%（+22.4 个百分点），在 MUSIC-Duet 上 AUC 从 36.1% 提升至 53.2%（+17.1 个百分点）。这一差距在复杂多声源场景中尤为突出，验证了元推理范式对特征匹配范式的结构性优势。

**脉络二：现成 MLLM 的直接应用。** 直接将 **Qwen2.5-Omni**（Xu et al., arXiv 2025）等现成多模态大模型用于声源定位时，由于缺乏结构化推理流程，定位精度有限。GAR-SSL 通过引入三阶段流水线和多次采样共识机制（N=5），将 MLLM 的通用推理能力系统性地转化为可靠的定位能力。消融实验表明（Table 6），使用 7B 规模的 MLLM 骨干比 3B 版本获得更强性能，说明更大规模模型的推理能力对定位精度有直接贡献。

**脉络三：推理时自精炼（test-time self-refinement）。** GAR-SSL 的分析-精炼循环与推理时优化方法共享“评估-修正”的迭代思想，但其独特之处在于：(1) 精炼决策由**自适应门控**自动触发，而非盲目迭代；(2) 分析阶段产生的角色标签和锚点提供了**可解释的修正依据**，而非黑箱调整；(3) 多次采样共识机制有效抑制了 MLLM 随机解码带来的波动。

### 3. 适用边界与局限

GAR-SSL 的适用边界由其设计选择和技术约束共同决定：

**推理成本约束。** 单样本推理约需 4 秒（RTX 4090），主要开销来自多轮 MLLM 调用（N=5 次分析迭代）。这使得当前框架难以直接部署于实时应用（如视频流的逐帧定位）。如何通过缓存共享、早停策略或轻量化 MLLM 骨干降低推理开销，是工程落地的关键挑战。

**时间维度缺失。** 框架仅处理单帧图像-音频对，未利用视频中的时间连续性信息。对于移动声源（如行驶的车辆、行走的人），帧间运动一致性可提供强约束，但当前方法无法利用这一信号。将时序推理融入分析阶段（如跨帧锚点追踪）是自然的扩展方向。

**MLLM 骨干依赖性。** 框架基于 **Qwen2.5-Omni-7B** 构建，迁移至其他 MLLM 时性能可能波动。不同 MLLM 在视觉定位、音频理解和指令遵循能力上的差异，会直接影响三阶段流水线中各模块的输出质量。建立跨 MLLM 骨干的鲁棒性评估和适配策略，是方法泛化的必要条件。

**场景覆盖有限。** 当前验证集中在 VGGSound 和 MUSIC 两个相对受控的数据集上，尚未在更广泛的真实世界声学场景（如高噪声环境、多类声源混合、屏外声源占主导等）上进行充分测试。分析阶段依赖角色标签的视觉可见性约束（$\operatorname{vis}(t \mid I) = 1$），当声源完全被遮挡或位于画面外时，该约束可能导致定位失败。

### 4. 开放问题

1. **推理效率优化**：能否通过分析阶段的早停机制（如视听一致性得分连续多次高于阈值时提前终止迭代）或跨样本的上下文缓存，将推理时间压缩至亚秒级？
2. **时序推理融合**：如何将帧间运动一致性、声源轨迹平滑性等时序先验融入分析阶段的锚点投票和视听一致性评分？
3. **跨任务泛化**：GAR 的“生成-分析-精炼”元推理范式能否推广到其他跨模态定位任务，如视频动作定位、触觉-视觉定位、文本-图像指代定位？
4. **人机协同闭环**：元推理过程中产生的因果解释和置信度评分，能否作为主动学习中的不确定性指标，或用于人机交互中的定位修正反馈？
5. **屏外与遮挡声源**：当声源完全不可见时，当前框架依赖视觉证据的分析机制将失效。能否引入空间音频线索（如双耳时间差）或场景上下文推理，实现对屏外声源的方位估计？

## 原文 PDF

![[paperPDFs/CVPR_2026/Generate_Analyze_and_Refine_Training_Free_Sound_Source_Localization_via_MLLM_Meta_Reasoning.pdf]]
