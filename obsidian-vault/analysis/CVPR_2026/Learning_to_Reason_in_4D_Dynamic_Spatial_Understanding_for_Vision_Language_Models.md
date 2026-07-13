---
title: "Learning to Reason in 4D: Dynamic Spatial Understanding for Vision Language Models"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/Learning_to_Reason_in_4D_Dynamic_Spatial_Understanding_for_Vision_Language_Models.pdf
project_link: null
code_link: "https://github.com/TencentARC/DSR_Suite"
aliases:
- DSGSMG
- LR4DSUVLM
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
core_operator: 通过引入一个轻量级几何选择模块(GSM)，以问题语义为引导，从预训练3D重建模型输出的几何先验中动态提取与问题最相关的信息，并压缩为紧凑几何tokens，从而在增强动态空间推理能力的同时，避免噪声对通用能力的干扰。
primary_logic: 采用双Q-Former架构实现“语义压缩-几何选择”机制：第一个Q-Former将问题文本压缩为语义查询向量，第二个Q-Former以此查询向量为指导，从繁多的3D tokens中仅抽取与当前问题相关的几何特征，生成固定数量的几何tokens。这种选择性注入确保了模型能高效利用几何先验进行动态空间推理，而不被无关的、可能带有噪声的3D信息所淹没，从而保持了强大的通用视频理解能力。
claims:
- 在DSR-Bench基准上，GSM (Ours) 平均准确率达到58.9%，显著优于其他所有已对比的专有模型和空间推理模型（如VG-LLM 38.4%，VLM-3R 31.4%）。
- 与直接拼接3D tokens的Addition方法相比，GSM在DSR-Bench上取得相近甚至更优的性能（57.4 vs 57.7），但在通用基准Video-MME上，GSM（59.9）远高于Addition（48.6），证明GSM有效缓解了通用性能退化。
- 将基座模型从Qwen2.5-VL-7B替换为Qwen3-VL-8B-Instruct后，GSM依然有效，DSR-Bench为58.6%，Video-MME保持64.4%，表明方法与基座无关。
- 随着DSR-Train训练数据量的增加，DSR-Bench上的准确率单调提升，验证了数据可扩展性。
---

# Learning to Reason in 4D: Dynamic Spatial Understanding for Vision Language Models

> [!tip] 核心洞察
> 采用双Q-Former架构实现“语义压缩-几何选择”机制：第一个Q-Former将问题文本压缩为语义查询向量，第二个Q-Former以此查询向量为指导，从繁多的3D tokens中仅抽取与当前问题相关的几何特征，生成固定数量的几何tokens。这种选择性注入确保了模型能高效利用几何先验进行动态空间推理，而不被无关的、可能带有噪声的3D信息所淹没，从而保持了强大的通用视频理解能力。

| 字段 | 内容 |
|------|------|
| 中文题名 | 4D推理学习：面向视觉语言模型的动态空间理解 |
| 英文题名 | Learning to Reason in 4D: Dynamic Spatial Understanding for Vision Language Models |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2512.20557) · [Code](https://github.com/TencentARC/DSR_Suite) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction |
| Method | DSR Suite (Geometry Selection Module, GSM) |
| Dataset | DSR-Bench, Video-MME, VLM4D |

> [!tip] 效果简介
> - DSR-Bench 上，Average Accuracy (%) 58.9 vs 23.5 (Qwen2.5-VL-7B Baseline) (+35.4)；Average Accuracy (%) 58.9 vs 38.4 (VG-LLM) (+20.5)。
> - Video-MME 上，Accuracy (%) 59.9 (GSM) vs 48.6 (Addition) (+11.3)。
> - VLM4D 上，Accuracy (%) 48.3 (GSM) vs 46.7 (SFT) (+1.6)。

## 概要

本文针对视觉语言模型（VLM）在动态空间推理（Dynamic Spatial Reasoning, DSR）上的能力短板，提出了**DSR Suite**——一套包含大规模训练数据生成管线与轻量级几何选择模块（Geometry Selection Module, GSM）的系统方案。核心瓶颈在于：现有VLM缺乏对物体几何与时序关系变化的深层理解，而直接注入3D几何先验又会引入与问题无关的噪声，导致通用视频理解性能显著退化。

GSM采用**双Q-Former架构**实现“语义压缩-几何选择”机制：第一个Q-Former将问题文本蒸馏为语义查询向量 $\mathbf{Q}_{\mathrm{lang}} \in \mathbb{R}^{N \times d}$，第二个Q-Former以此查询为指导，从预训练3D重建模型输出的几何先验中仅抽取与当前问题相关的信息，生成紧凑的几何tokens $\mathbf{Q}_{\mathrm{geo}} \in \mathbb{R}^{N \times d}$，最终与视觉tokens、文本tokens拼接为 $\tilde{\mathbf{T}}_{\mathrm{total}} = [\mathbf{T}_{\mathrm{vis}} ; \mathbf{Q}_{\mathrm{geo}} ; \mathbf{T}_{\mathrm{text}}]$ 送入LLM进行推理。这种选择性注入策略确保了模型能高效利用几何先验进行动态空间推理，而不被无关的3D信息所淹没。

在自建的**DSR-Bench**基准上，搭载GSM的Qwen2.5-VL-7B平均准确率达到**58.9%**，较基座模型（23.5%）提升35.4个百分点，显著优于VG-LLM（38.4%）和VLM-3R（31.4%）等空间推理模型。关键消融实验表明，与直接拼接3D tokens的Addition方法相比，GSM在DSR-Bench上性能相近（57.4 vs 57.7），但在通用基准Video-MME上保持**59.9%**的准确率，远高于Addition的48.6%，有效缓解了通用性能退化。该方法在替换基座模型为Qwen3-VL-8B后依然有效（DSR-Bench 58.6%），且随训练数据量增加准确率单调提升，展现出良好的模型无关性与数据可扩展性。

**方法定位**：GSM属于“问题引导的几何先验选择性注入”范式，与直接拼接（Addition）或全量交叉注意力融合（VG-LLM）形成对比。其双Q-Former设计在专用动态空间推理能力与通用视频理解能力之间取得了关键平衡，为VLM的多模态融合提供了新的架构思路。

### 动态空间推理：从静态3D到动态4D的认知跃迁

视觉语言模型（VLMs）在图像和视频理解任务上取得了显著进展，但在**动态空间推理**（Dynamic Spatial Reasoning, DSR）——即理解包含运动物体的三维环境中物体之间的几何关系与时序变化——方面仍存在根本性能力短板。如图1(a)所示，与仅需理解固定场景中物体空间布局的静态空间推理不同，动态空间推理要求模型在时间维度上持续追踪物体运动轨迹、推断视角变换后的空间关系，并理解多物体交互过程中的相对位置变化。这种从静态3D感知到动态4D理解的跃迁，对模型的几何先验利用和时序建模能力提出了更高要求。

### 现有方法的两难困境

当前增强VLM空间推理能力的主流思路是将从视频中提取的3D几何先验（如相机位姿、稀疏点云、物体掩码与3D轨迹）注入模型。然而，这一技术路线面临一个核心的**专用性与通用性权衡**：

- **直接注入策略**（如Addition方法）：将预训练3D重建模型输出的全部3D tokens直接拼接到视觉tokens上。该方法虽然能为模型提供丰富的几何信息，但大量与当前问题无关的3D tokens会引入显著噪声，导致模型在通用视频理解任务上的性能大幅退化。如表5所示，Addition方法在通用基准Video-MME上的准确率仅为48.6%，远低于基线的表现。

- **交叉注意力融合策略**（如VG-LLM、VLM-3R）：通过交叉注意力机制将几何特征融入视觉表示。这类方法同样面临信息过载的问题——模型难以从繁多的几何先验中自主识别与当前推理任务真正相关的信息，导致其在动态空间推理基准上的表现受限（VG-LLM在DSR-Bench上的平均准确率仅为38.4%）。

### 根本瓶颈：数据匮乏与信息过载

上述困境的背后存在两个相互交织的深层瓶颈：

**瓶颈一：缺乏大规模、可扩展的4D感知训练数据。** 现有空间推理数据集多聚焦于静态场景或短时运动，无法充分覆盖视角变换、多物体交互、细粒度时序答案等动态空间推理的核心要素。这导致模型在训练阶段缺乏足够的监督信号来学习将几何先验与动态推理任务对齐。

**瓶颈二：几何先验的“信息过载”效应。** 即使获得了丰富的3D重建输出，直接将其全部注入VLM会引入大量与问题无关的噪声。模型缺乏一种有效的机制来**选择性**地利用几何信息——即根据当前问题的语义需求，从几何先验中精准提取最相关的部分，而忽略无关或可能产生干扰的信息。

### 本文动机

针对上述瓶颈，本文提出**DSR Suite**，一个面向动态空间推理的系统性解决方案，包含两个核心组件：

1. **DSR-Train**：一个大规模、多样化的动态空间推理训练数据集，通过自动化的视频策展、几何线索提取与问答生成管道构建，为模型提供覆盖视角变换、多物体交互等关键场景的训练信号。

2. **几何选择模块（GSM）**：一个轻量级的几何先验集成模块，采用双Q-Former架构实现“语义压缩-几何选择”机制——首先将问题语义压缩为查询向量，再以此查询为指导从3D tokens中仅抽取与当前问题相关的几何特征，从而在增强动态空间推理能力的同时，避免噪声对通用能力的干扰。

## 核心方法与创新机理

本工作的核心创新在于提出了一种**语义引导的选择性几何注入机制**，以解决视觉语言模型（VLM）在动态空间推理（DSR）中“专用能力提升”与“通用能力保持”之间的根本矛盾。其关键设计围绕一个名为**几何选择模块（Geometry Selection Module, GSM）**的轻量级组件展开，该模块通过“语义压缩-几何选择”的双Q-Former架构，实现了对几何先验的高效、按需利用。

### 关键改进槽位

| 改进维度 | 基线方案 | 本方案（GSM） |
|:---|:---|:---|
| **几何先验集成方式** | 直接将所有3D tokens拼接到视觉tokens（Addition），或通过交叉注意力融合全部几何特征（如VG-LLM） | 采用双Q-Former结构：第一个Q-Former将问题语义压缩为语言条件查询向量 $\mathbf{Q}_{\mathrm{lang}}$，第二个Q-Former以此查询为指导，从3D tokens中**选择性**提取问题相关几何信息，生成紧凑的几何tokens $\mathbf{Q}_{\mathrm{geo}}$ 进行拼接 |
| **训练数据** | 通用视频理解数据，或静态空间推理数据（缺乏动态时空QA） | **DSR-Train**：大规模、多样化的动态空间推理多选QA对，涵盖视角变换、多物体交互、细粒度时序答案，支持可扩展的自动化生成 |

### 机制剖析：从“全量注入”到“按需选择”

现有方案（如直接将3D tokens拼接到视觉序列的Addition方法）面临的核心瓶颈是**噪声干扰**：预训练的3D重建模型输出的几何先验中，大量信息与当前问题无关，全量注入会淹没模型的通用推理能力。GSM通过以下两步机制实现解耦：

1. **语义压缩（Semantic Condenser）**：第一个Q-Former使用 $N$ 个可学习查询向量，对问题文本tokens $\mathbf{T}_{\text{text}}$ 进行交叉注意力，将问题语义蒸馏为语言条件查询嵌入 $\mathbf{Q}_{\mathrm{lang}} \in \mathbb{R}^{N \times d}$。这一步骤确保后续的几何选择是**问题驱动**的。

2. **几何选择（Relevant-Geometry Selector）**：第二个Q-Former以 $\mathbf{Q}_{\mathrm{lang}}$ 作为查询，对预提取的3D tokens进行交叉注意力，仅抽取与当前问题语义相关的几何信息，输出同维度的紧凑几何tokens $\mathbf{Q}_{\mathrm{geo}} \in \mathbb{R}^{N \times d}$。最终，总token序列 $\tilde{\mathbf{T}}_{\mathrm{total}} = [\mathbf{T}_{\mathrm{vis}} ; \mathbf{Q}_{\mathrm{geo}} ; \mathbf{T}_{\text{text}}]$ 被送入大语言模型头进行推理。

### 创新效果的因果证据

GSM的设计直接解决了“专用-通用”权衡问题，其因果效应在消融实验中得到了明确验证：

- **专用能力提升**：在DSR-Bench上，GSM（基于Qwen2.5-VL-7B）平均准确率达到**58.9%**，远超未经训练的基线模型（23.5%），也显著优于其他空间推理模型如VG-LLM（38.4%）和VLM-3R（31.4%）（Table 4，置信度0.95）。

- **通用能力保持**：与直接拼接3D tokens的Addition方法相比，GSM在DSR-Bench上取得相近性能（57.4 vs 57.7），但在通用视频理解基准Video-MME上，GSM（59.9）远高于Addition（48.6），证明选择性注入有效避免了通用性能的严重退化（Table 5，置信度0.95）。

- **基座无关性**：将基座模型替换为Qwen3-VL-8B-Instruct后，GSM依然有效（DSR-Bench 58.6%，Video-MME 64.4%），表明该机制不依赖于特定VLM架构（Table 10，置信度0.9）。

- **数据可扩展性**：随着DSR-Train训练数据量的增加，模型在DSR-Bench上的准确率单调提升，验证了数据生成管道的可扩展性（Figure 5，置信度0.85）。

### 创新边界与局限

尽管GSM在动态空间推理上取得了显著突破，其有效性受限于以下因素：

- **对上游3D重建的依赖**：GSM本身不产生几何先验，而是依赖预训练的3D重建模型（如π3）的输出。若上游模型在遮挡、运动模糊等场景下输出质量下降，几何tokens的可靠性将直接受损。
- **相对尺度限制**：数据生成基于相对尺度的3D结构，无法产生需要绝对度量值的问答，限制了数值推理的深度。
- **困难子任务瓶颈**：Direction Prediction等需要预测未来运动方向的子任务准确率仍较低（约35%），表明模型在时序前瞻性推理上存在困难。

DSR Suite 的整体框架围绕“几何感知的动态空间推理”展开，其核心设计思路是：**将问题语义作为选择器，从预提取的 4D 几何先验中动态抽取与当前问题最相关的信息，而非将全部几何 token 粗暴注入视觉语言模型（VLM）**。框架由两大支柱构成——数据生成管道（DSR-Train/DSR-Bench）与模型架构（Geometry Selection Module, GSM），二者协同工作，使 VLM 在获得动态空间推理能力的同时不损失通用视频理解性能。

### 数据生成管道：从视频到多选 QA 的三阶段流水线

数据生成管道（Figure 2）是整个框架的基础，它从大规模自然视频中自动化生产包含丰富几何线索的多选题-答案对。管道分为三个阶段：

![[assets/figures/papers/paper_list_l2399_https_arxiv_org_abs_2512_20557/figures/002_Figure_2.jpg]]
*Figure 2: Multiple-choice question–answer generation pipeline in our DSR Suite. It comprises three stages: Video Curation, Geometric Clue Extraction and Data Generation. In Video Curation stage, in-the-wild videos are filtered by LLMs or VLMs to remove motionless ones based on captions or visual cues. During Geometric Clue Extraction, vision foundation models extract key geometric cues, including camera poses, point clouds, object masks and orientations. Finally, in Data Generation, object coordinates are transformed into a randomly selected viewpoint and question–answer pairs are produced using either predefined templates or LLM-based free-form generation*

1. **视频策展（Video Curation）**：从 Koala-36M 等视频源出发，利用 LLM/VLM 过滤掉无明显物体运动或全局运动的片段。对于 DSR-Train，使用 DeepSeek-R1 基于视频描述进行筛选；对于 DSR-Bench，则使用 Gemini-2.5-Pro 直接基于视频内容判断，确保保留的视频具备有意义的动态空间交互。

2. **几何线索提取（Geometric Clue Extraction）**：对保留的视频片段，并行提取两类几何先验。**物体级线索**：利用 Grounded SAM2 获取物体掩码，Orient Anything 估计物体朝向，并通过时序关联构建 3D 轨迹。**场景级线索**：使用 π3 等预训练 3D 重建模型估计相机位姿和稀疏点云。这些几何线索为后续 QA 生成提供了完整的 4D 感知基础。

3. **QA 生成（Data Generation）**：基于提取的几何线索，以两种方式生成多选题-答案对。**模板式 QA**：覆盖六种核心动态空间推理能力（如表 1 所示），包括方向预测、相对位置判断、运动轨迹推理等，答案选项由几何线索按规则推导得出（如表 2、表 8 所示）。**非模板式 QA**：利用 DeepSeek-R1，以 3D 轨迹、物体身份和视角信息为条件，自动生成更开放、需要整体推理的问题。这种混合生成策略兼顾了核心技能的精准评测与综合推理能力的覆盖。

### 模型架构：双 Q-Former 的语义-几何选择机制

GSM 的架构设计（Figure 4）是整个框架的核心创新，它通过两个堆叠的 Q-Former 实现了“语义压缩-几何选择”的双阶段信息筛选：

![[assets/figures/papers/paper_list_l2399_https_arxiv_org_abs_2512_20557/figures/007_Figure_4.jpg]]
*Figure 4: Illustraction of our proposed GSM that consists of two stacked Q-Formers. The first Q-Former condenses question semantics, and the second one extracts question-relevant geometric knowledge into a compact set of geometry tokens. These tokens are appended to original vision tokens to be processed by LLM*

**输入流**：给定一段视频及其对应的多选问题，系统首先通过视觉编码器提取视频帧的视觉 token 序列 $\mathbf{T}_{\text{vis}}$，同时将问题文本编码为文本 token 序列 $\mathbf{T}_{\text{text}}$。几何先验则来自预训练的 4D 重建模型，以 3D token 序列的形式提供。

**语义压缩阶段**：第一个 Q-Former（Semantic Condenser）接收 $N$ 个可学习查询向量，以 $\mathbf{T}_{\text{text}}$ 为注意力目标，将问题语义蒸馏为一组语言条件查询嵌入 $\mathbf{Q}_{\mathrm{lang}} \in \mathbb{R}^{N \times d}$。这一步将冗长的问题文本压缩为紧凑的语义表示，作为后续几何选择的“检索条件”。

**几何选择阶段**：第二个 Q-Former（Relevant-Geometry Selector）以 $\mathbf{Q}_{\mathrm{lang}}$ 为查询，在 3D token 序列上进行交叉注意力，从中提取与当前问题最相关的几何信息，输出紧凑的几何 token $\mathbf{Q}_{\mathrm{geo}} \in \mathbb{R}^{N \times d}$。这一选择性提取机制是缓解通用性能退化的关键——与直接将所有 3D token 拼接到视觉 token 上的 Addition 方法相比，GSM 仅注入与问题相关的几何知识，避免了无关 3D 噪声对模型的干扰。

**输出流**：最终的 token 序列由视觉 token、几何 token 和文本 token 拼接而成：

$$\tilde{\mathbf{T}}_{\text{total}} = [\mathbf{T}_{\text{vis}} ; \mathbf{Q}_{\text{geo}} ; \mathbf{T}_{\text{text}}]$$

该序列被送入大语言模型（LLM）头进行推理，生成最终答案。整个 GSM 模块轻量且与基座模型无关——实验表明，无论使用 Qwen2.5-VL-7B 还是 Qwen3-VL-8B-Instruct 作为基座，GSM 均能显著提升动态空间推理性能（Table 4、Table 10）。

### 框架的因果机制与关键瓶颈解决

该框架直接回应了动态空间推理的两大瓶颈：**数据稀缺**与**几何先验注入的通用性退化**。DSR-Train 提供了大规模、可扩展的动态空间推理训练数据，数据量增加时模型性能单调提升（Figure 5），验证了数据可扩展性。GSM 则通过“问题引导的选择性注入”机制，在增强 DSR 能力的同时保持了通用视频理解能力——在 DSR-Bench 上，GSM 达到 58.9% 的平均准确率，远超 VG-LLM（38.4%）和 VLM-3R（31.4%）；在通用基准 Video-MME 上，GSM（59.9%）远高于直接拼接 3D token 的 Addition 方法（48.6%），证明选择性注入有效缓解了通用性能退化（Table 5）。

### 几何选择模块（GSM）总体架构

GSM 是一个轻量级模块，通过两个堆叠的 Q-Former 将几何先验集成到 VLM 中。其核心设计思想是“语义压缩-几何选择”：先将问题语义蒸馏为紧凑的查询向量，再以该查询向量为指导，从预训练 4D 重建模型输出的 3D tokens 中仅提取与当前问题相关的几何信息，生成固定数量的紧凑几何 tokens。这一选择性注入机制避免了直接拼接大量 3D tokens 所带来的噪声干扰，从而在增强动态空间推理能力的同时保持通用视频理解性能。

### 关键公式与变量含义

**语义压缩阶段**：第一个 Q-Former（Semantic Condenser）接收 $N$ 个可学习查询向量，通过交叉注意力与问题文本 tokens $\mathbf{T}_{\text{text}}$ 交互，将问题语义蒸馏为一组语言条件查询嵌入：

$$\mathbf{Q}_{\mathrm{lang}} \in \mathbb{R}^{N \times d}$$

其中 $N$ 为可学习查询数量（默认 $N=32$），$d$ 为特征维度。$\mathbf{Q}_{\mathrm{lang}}$ 编码了问题的语义意图，作为后续几何选择的指导信号。

**几何选择阶段**：第二个 Q-Former（Relevant-Geometry Selector）以 $\mathbf{Q}_{\mathrm{lang}}$ 为查询，对预训练 3D 重建模型（如 π3）输出的 3D tokens 进行交叉注意力，提取与问题相关的几何信息，输出紧凑几何 tokens：

$$\mathbf{Q}_{\mathrm{geo}} \in \mathbb{R}^{N \times d}$$

$\mathbf{Q}_{\mathrm{geo}}$ 仅包含对回答当前问题有贡献的几何特征，而非全部 3D 场景信息，从而避免了无关几何噪声的注入。

**Token 拼接与推理**：最终，视觉 tokens $\mathbf{T}_{\text{vis}}$、几何 tokens $\mathbf{Q}_{\text{geo}}$ 和文本 tokens $\mathbf{T}_{\text{text}}$ 被拼接为单一序列，送入大语言模型头进行答案生成：

$$\tilde{\mathbf{T}}_{\mathrm{total}} = [\mathbf{T}_{\mathrm{vis}} ; \mathbf{Q}_{\mathrm{geo}} ; \mathbf{T}_{\text{text}}]$$

### 模块设计要点

GSM 的双 Q-Former 结构与直接拼接 3D tokens 的 Addition 方法形成鲜明对比。Addition 方法将所有 3D tokens 无条件地拼接到视觉 tokens 上，虽然也能提升动态空间推理能力（DSR-Bench 上 57.7 vs GSM 的 57.4，性能相近），但会导致通用视频理解性能大幅下降（Video-MME 上 48.6 vs GSM 的 59.9）。GSM 通过问题语义引导的选择性几何提取，在几乎不牺牲专用性能的前提下，有效缓解了通用性能退化问题（Table 5）。

可学习查询数量 $N$ 是 GSM 的关键超参数。消融实验表明 $N=32$ 达到最佳整体性能平衡：过小（如 $N=16$）会限制几何信息的表达能力，过大（如 $N=64$）则会引入冗余信息并损害通用能力（Table 6）。

## 实验与关键发现

### 核心实验结果

为验证GSM在动态空间推理上的有效性，作者在DSR-Bench上进行了全面对比。**Table 4** 展示了不同模型在DSR-Bench各子任务上的性能。以Qwen2.5-VL-7B为基座，GSM（Ours）取得了 **58.9%** 的平均准确率，相比未使用任何动态空间推理数据的基线模型（23.5%）提升了 **+35.4个百分点**。与现有的空间推理增强模型相比，GSM显著优于VG-LLM（38.4%）和VLM-3R（31.4%），优势分别达到 **+20.5** 和 **+27.5个百分点**。这一结果表明，GSM的选择性几何注入机制能够有效利用4D重建先验，大幅提升VLMs对动态场景中物体运动、空间关系变化的理解能力。

![[assets/figures/papers/paper_list_l2399_https_arxiv_org_abs_2512_20557/figures/008_Table_4.jpg]]
*Table 4: Performance comparison among different VLMs on different subtasks of DSR-Bench*

然而，在细粒度子任务上，GSM仍面临明显挑战。尤其是在 **Direction Prediction**（方向预测）子任务上，GSM的准确率仅约35%左右，远低于其他子任务。这暴露了当前模型在预测物体未来运动方向方面的根本性困难——该任务要求模型不仅理解当前的空间配置，还需推理运动趋势和意图，这对仅依赖静态3D tokens和视频帧的架构构成了本质瓶颈。

### 消融实验：GSM vs. 直接几何注入

**Table 5** 的消融实验是验证GSM核心设计动机的关键证据。论文对比了三种训练策略：

- **SFT**：仅在DSR-Train上进行标准监督微调，不注入任何几何先验。
- **Addition**：将预训练3D重建模型输出的所有3D tokens直接拼接到视觉tokens上，与GSM使用相同的几何先验来源。
- **GSM (Ours)**：采用双Q-Former选择性提取问题相关的几何tokens。

在DSR-Bench上，GSM（57.4）与Addition（57.7）取得了相近的动态空间推理性能。但在通用视频理解基准 **Video-MME** 上，两者表现出根本性差异：GSM保持了 **59.9%** 的准确率，而Addition骤降至 **48.6%**，性能退化超过11个百分点。这直接验证了论文的核心论断：**直接注入全部3D tokens会引入与问题无关的噪声，严重损害模型的通用视频理解能力**。GSM通过以问题语义为引导的选择性几何提取，在增强专用能力的同时有效避免了通用性能的退化。

在另一个动态空间推理基准 **VLM4D** 上，GSM（48.3%）相比SFT（46.7%）也取得了小幅提升（+1.6），进一步验证了方法的泛化性。

### 关键超参数分析：可学习查询数量

**Table 6** 展示了GSM中可学习查询数量 $N$ 对性能的影响。实验表明，$N=32$ 时达到最佳平衡点：在DSR-Bench上取得最高准确率，同时在Video-MME上保持竞争力。当 $N$ 增大到64时，DSR-Bench性能未见提升，但Video-MME性能开始下降，表明过多的几何tokens开始引入冗余信息，干扰通用推理。当 $N$ 过小（如8）时，几何信息压缩过度，DSR-Bench性能明显下降。这一消融证实了GSM的设计需要在信息充分性和噪声控制之间取得精确平衡。

### 数据可扩展性验证

**Figure 5** 展示了DSR-Bench准确率随DSR-Train训练数据量变化的曲线。随着训练QA对数量的增加，模型准确率呈现单调提升趋势，未出现饱和迹象。这验证了DSR Suite数据生成管道的可扩展性——通过自动化管道持续生成大规模、多样化的动态空间推理数据，可以稳定提升模型能力。该证据直接回应了论文提出的第一个瓶颈：大规模4D感知训练数据的缺乏可以通过自动化管道有效解决。

### 训练数据配置消融

**Table 9** 对比了不同模板/非模板QA比例的训练数据设置。结果表明，以模板QA为主、辅以少量非模板QA的混合训练可获得最优整体性能。纯模板训练在模板类问题上表现最佳，但在需要整体推理的非模板问题上泛化不足；纯非模板训练则因数据量有限而整体性能欠佳。这一发现为数据生成策略提供了实用指导。

### 基座模型无关性验证

**Table 10** 将基座模型从Qwen2.5-VL-7B替换为Qwen3-VL-8B-Instruct后，GSM依然有效：DSR-Bench准确率达到58.6%（基线28.7%），Video-MME保持64.4%。这表明GSM的“语义压缩-几何选择”机制是通用的架构增强，不依赖于特定基座模型的能力。

### 失败模式与局限性分析

综合实验结果，GSM存在以下明确的失败模式：

1. **方向预测困难**：Direction Prediction子任务准确率显著偏低（约35%），说明模型对物体未来运动方向的推理能力有限。这可能源于3D重建先验主要提供静态几何信息，缺乏运动趋势的显式建模。

2. **通用性能的隐性代价**：虽然GSM相比Addition大幅缓解了通用性能退化，但在Video-MME上（59.9%）仍略低于SFT基线（约61-62%，需人工核实精确值），表明即使选择性注入几何tokens，仍可能对通用理解产生微弱干扰。

3. **对3D重建质量的依赖**：GSM的性能上限受限于预训练3D重建模型（如π3）的输出质量。在遮挡严重、纹理稀疏或运动模糊的场景下，几何先验的可靠性下降，将直接影响推理准确率。论文未对此进行定量分析。

4. **绝对度量推理缺失**：数据生成基于相对尺度的3D结构，GSM无法处理需要绝对距离、速度等数值度量的推理问题，限制了其在精确空间推理场景中的应用。

![[assets/figures/papers/paper_list_l2399_https_arxiv_org_abs_2512_20557/figures/009_Table_5.jpg]]
*Table 5: Comparison between GSW and other training methods*

![[assets/figures/papers/paper_list_l2399_https_arxiv_org_abs_2512_20557/figures/010_Table_6.jpg]]
*Table 6: Ablation of learnable query numbers*

![[assets/figures/papers/paper_list_l2399_https_arxiv_org_abs_2512_20557/figures/018_Table_10.jpg]]
*Table 10: Comparison between GSM and other methods with Qwen3-VL-8B-Instruct as the base model*

## 定位与知识库关联

### 1. 方法沿革与基线对比

本文提出的 **DSR Suite** 处于视觉语言模型（VLM）与三维几何感知的交叉地带，其核心贡献 **GSM（Geometry Selection Module）** 直接回应了该领域的一个关键瓶颈：如何在不损害通用视频理解能力的前提下，向VLM注入4D几何先验以支持动态空间推理。

**与直接注入方法的对比。** 最直接的基线是 **Addition** 方法——将预训练3D重建模型输出的所有3D tokens直接拼接到视觉tokens上。这种方法虽然为模型提供了完整的几何信息，但引入了大量与当前问题无关的噪声，导致模型在通用视频理解基准Video-MME上性能大幅下降（Addition为48.6%，GSM为59.9%，Table 5）。GSM通过双Q-Former的“语义压缩-几何选择”机制，仅提取与问题相关的几何信息，从根本上解决了这一专用性与通用性的权衡困境。

**与现有空间推理VLM的对比。** 在DSR-Bench基准上，GSM以58.9%的平均准确率显著超越了两类代表性工作：
- **VG-LLM**（38.4%）：通过交叉注意力融入几何先验的空间推理模型，但其融合方式未做问题相关的选择性过滤，且面向的是静态空间场景。
- **VLM-3R**（31.4%）：融合3D重建特征的静态空间推理模型，同样缺乏对动态时序关系的建模能力。

这两类方法的核心局限在于：它们要么面向静态场景，要么将所有几何信息无差别地注入模型，无法应对DSR-Bench中涉及的视角变换、多物体交互和细粒度时序答案等动态推理需求。

**与纯微调基线的对比。** 仅使用DSR-Train数据进行标准监督微调（SFT）而不引入几何先验，在DSR-Bench上的表现远低于GSM（Table 5），证明几何先验本身对于动态空间推理是不可或缺的，而不仅仅是数据规模的作用。

### 2. 方法适用边界

**依赖预训练3D重建模型。** GSM的几何token质量直接受上游3D重建模型（如π3）输出的影响。若重建模型在特定场景（如强遮挡、透明物体、极端光照）下失效，GSM将无法获得可靠的几何先验，此时模型退化为仅依赖视觉tokens和文本tokens的推理模式。这一依赖性也意味着GSM无法独立于重建模型进行端到端优化。

**尺度信息缺失。** 数据生成管道基于相对尺度的3D结构（相机位姿、稀疏点云、物体轨迹），无法产生需要绝对度量值的问答对。因此，GSM在当前框架下不支持诸如“物体A距离物体B多少米”这类精确数值推理，限制了其在需要度量空间理解的应用场景中的适用性。

**方向预测的困难。** 即使在使用GSM的情况下，Direction Prediction子任务的准确率仍然较低（约35%，Table 4），表明模型在预测物体未来运动方向方面存在根本性困难。这可能源于训练数据中此类问题的覆盖不足，或模型对时序因果关系的建模能力有限。

**训练数据分布。** 训练视频来源于Koala-36M数据集，虽经过LLM/VLM筛选以保留具有显著物体运动的片段，但其场景和运动模式可能不能完全代表现实世界中所有动态交互类型（如高速运动、多人协作场景、非刚性形变等）。

### 3. 局限性与开放问题

**推理效率。** GSM引入的双Q-Former结构虽然轻量，但额外的3D重建模型推理（π3、Grounded SAM2、Orient Anything等）会增加整体系统的推理延迟。论文未报告端到端推理时间的定量分析，这对于实时应用（如具身智能体）至关重要。

**长视频与复杂场景的扩展性。** 当前GSM的设计和实验主要针对中等长度视频（DSR-Bench中的视频片段），其在数分钟长视频、多物体强遮挡场景下的性能和效率尚未得到验证。随着视频长度增加，3D tokens的数量可能急剧膨胀，GSM的几何选择Q-Former能否有效处理更大规模的候选几何信息仍有待探索。

**公平性与偏差。** 论文未就数据偏差或模型在特定人群、场景上的公平性进行专门分析。DSR-Bench的场景分布（Figure 3a）和训练数据来源可能隐含地理、文化或场景类型的偏差，这些偏差如何影响模型在不同用户群体或应用场景中的表现，是需要进一步研究的问题。

**开放问题：**
1. **跨任务迁移。** GSM的选择性几何注入机制是否可以泛化到其他需要外部先验知识的VLM任务，如图像级空间推理、具身导航、机器人操作规划？初步证据来自MineDojo智能体实验（Table 12），但更广泛的跨任务验证仍是开放的。
2. **绝对尺度引入。** 如何通过深度估计或绝对尺度信息增强数据生成管道，以支持更精细的度量空间推理（如精确距离、速度计算）？
3. **困难子任务提升。** 是否可以通过对抗训练、课程学习或针对性数据增强，显著提升Direction Prediction等困难子任务的准确率？
4. **端到端协同训练。** GSM能否与端到端的3D/4D重建模型协同训练，使几何先验的提取与下游推理任务形成闭环优化，从而实现更强的4D理解能力？
5. **多模态几何先验融合。** 除3D tokens外，是否可以融入深度图、光流、场景图等其他形式的几何/运动先验，并通过类似的选择性机制进行统一融合？

## 原文 PDF

![[paperPDFs/CVPR_2026/Learning_to_Reason_in_4D_Dynamic_Spatial_Understanding_for_Vision_Language_Models.pdf]]
