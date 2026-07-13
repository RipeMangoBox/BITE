---
title: "UniVBench: Towards Unified Evaluation for Video Foundation Models"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/UniVBench_Towards_Unified_Evaluation_for_Video_Foundation_Models.pdf
project_link: null
code_link: "https://github.com/JianhuiWei7/UniVBench"
aliases:
- UUE
- UniVBench
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/benchmarks_datasets_evaluation
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: 引入一个统一的多任务、多镜头、免版权的基准（UniVBench），并配合统一的智能体评估系统（UniV-Eval），该评估将整体表现分解为面向可解释维度的核查清单。
primary_logic: 通过将评估统一在标准化的代理提示、指令解析和多维度打分之下，UniVBench首次量化了当前模型的“统一鸿沟”，并提供了将错误归因于感知与生成组件的诊断框架，从而指导模型迭代。
claims:
- 所有现有视频基准均为任务特定、单镜头且常存在版权污染，无法支撑统一评估（Table 1‑3）。
- 在 UniVBench 上，没有任何单一模型在理解、生成、编辑和重建任务上同时表现出色；生成模型在动作维度得分普遍低，感知模型在风格属性上则更弱（Table 4）。
- V2V 重建任务比 T2V 生成任务表现出更显著的不一致，揭示了统一模型中感知‑生成耦合的信息丢失。
- UniV‑Eval 与人工专家评判的总体一致性接近 85%，验证了其可靠性。
---

# UniVBench: Towards Unified Evaluation for Video Foundation Models

> [!tip] 核心洞察
> 通过将评估统一在标准化的代理提示、指令解析和多维度打分之下，UniVBench首次量化了当前模型的“统一鸿沟”，并提供了将错误归因于感知与生成组件的诊断框架，从而指导模型迭代。

| 字段 | 内容 |
|------|------|
| 中文题名 | UniVBench：迈向视频基础模型的统一评估 |
| 英文题名 | UniVBench: Towards Unified Evaluation for Video Foundation Models |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2602.21835) · [Code](https://github.com/JianhuiWei7/UniVBench) |
| Topic | #topic/vision_multimodal_applications #topic/benchmarks_datasets_evaluation #topic/vision_multimodal_applications/image_and_video_generation |
| Method | UniVBench and UniV-Eval |
| Dataset | UniVBench |

> [!tip] 效果简介
> - UniVBench (V2T understanding) 上，平均八维得分（%） 54.1 (Gemini 2.5 Pro) vs 16.3 (Showo-2) (+37.8)。
> - UniVBench (T2V generation) 上，平均八维得分（%） 77.9 (Seedance-1.0-Pro) vs 40.1 (CoDi-2) (+37.8)。
> - UniVBench (V2V reconstruction) 上，平均八维得分（%） 62.7 (Wan2.1-VACE-14B) vs 20.7 (CogVideoX-1.5-5B) (+42.0)。

## 概要

视频基础模型的评估长期面临碎片化困境：理解、生成、编辑等任务各自使用不同的数据集与指标，无法衡量模型在跨任务场景下的统一能力；同时，单一标量分数缺乏细粒度的错误归因机制，难以指导模型迭代。**UniVBench**（CVPR 2026）针对这一瓶颈，提出了首个面向视频基础模型的统一评估基准，覆盖理解（V2T）、生成（T2V/R2V）、编辑（TV2V/RV2V）和重建（V2V）六项任务，并配套智能体评估系统 **UniV-Eval**，将整体表现分解为8大维度、21个子维度的可解释核查清单。

核心发现表明：当前没有任何单一模型能在所有任务上同时表现优异——生成模型在动作维度得分普遍偏低，感知模型则在风格属性上更为薄弱；V2V重建任务相较于T2V生成表现出更显著的不一致，直接暴露了统一模型中感知‑生成耦合的信息丢失。UniV-Eval与人工专家评判的一致性接近85%，单次评估成本低于10美元，验证了其可靠性与规模化可行性。



### 视频基础模型的统一化趋势与评估困境

近年来，视频基础模型（Video Foundation Models）正朝着“统一”方向快速演进——单一模型同时具备视频理解、生成与编辑等多种能力。然而，现有的视频评估基准严重滞后于这一趋势，呈现出高度碎片化的特征。如 Table 1 所示，主流视频理解基准（如 MVBench、Video-MME 等）多依赖有版权的网络视频，仅支持单任务评估，且缺乏多镜头内容；视频生成基准（如 VBench、EvalCrafter 等）同样局限于文本到视频（T2V）的单一任务，无法评估编辑或重建能力；而视频编辑基准则几乎完全缺失多镜头支持与版权清洁的视频源。这种碎片化导致两个关键问题：**无法测量视频基础模型在理解、生成、编辑上的统一能力**，以及**单一标量分数无法提供细粒度、可解释的错误归因**。

### 现有基准的三重缺口

进一步分析揭示了现有评估体系的三个结构性缺口：

1. **任务覆盖单一**：绝大多数基准仅服务于单一任务（如 V2T 或 T2V），无法支撑跨任务的统一评估。Table 1 的对比清晰表明，尚无任何现有基准同时覆盖视频理解、生成、编辑与重建四类核心能力。

2. **多镜头支持缺失**：真实世界视频通常包含多个镜头切换，但现有基准的视频源几乎全部为单镜头。Table 1 中“Multi-shot”列的空白揭示了这一系统性盲区——模型在多镜头场景下的时序连贯性、镜头间一致性等关键能力从未被系统评估。

3. **评估指标粗粒度**：现有指标（如 CLIP Score、FVD 等）仅提供整体相似度或保真度的单一数值，无法定位错误来源。如 Table 3 所示，这些指标在风格、动作、主体一致性等细粒度维度上要么不适用，要么只能给出笼统评分，缺乏可追溯的诊断能力。

### 版权污染：被忽视的评估隐患

一个常被忽视但至关重要的问题是**版权污染**。现有基准大量使用来自 YouTube、电影等来源的网络视频，这些视频不仅存在版权限制，更严重的是可能已被用于训练当前的视频生成模型。这意味着在评估生成或编辑能力时，模型可能并非真正“理解”指令，而是简单地“记忆”并复现训练数据中的内容。UniVBench 通过完全人工创作的视频源，从根本上消除了这一隐患，确保评估结果的真实性与公平性。

### 本文动机与核心思路

针对上述困境，本文提出 **UniVBench**——首个面向视频基础模型的统一评估基准，其核心设计理念包括：

- **统一任务框架**：覆盖视频理解（V2T）、文本到视频生成（T2V）、参考图像视频生成（R2V）、文本指令视频编辑（TV2V）、参考图像视频编辑（RV2V）以及新提出的视频重建（V2V）共六项任务，形成完整的评估闭环。

- **多镜头与免版权数据集**：构建包含 100 个单镜头和 100 个多镜头（平均 3.72 个镜头）的高质量视频数据集，全部由人工创作，无版权及数据污染问题。

- **细粒度智能体评估系统（UniV-Eval）**：将视频切分为镜头单元，在 8 大维度、21 子维度的框架下进行动态、可追溯的评分，将整体表现分解为面向可解释维度的核查清单。

通过这一统一框架，UniVBench 首次量化了当前模型的“统一鸿沟”，并提供了将错误归因于感知与生成组件的诊断路径，从而为下一代视频基础模型的迭代提供明确指导。



## 核心方法与创新机理

UniVBench 的核心创新并非提出新的模型架构，而是通过**评估范式的统一化**，首次系统性地暴露并量化了当前视频基础模型的“统一鸿沟”。其创新点体现在三个紧密耦合的层面。

### 1. 从碎片化基准到统一多任务评估框架

现有视频评估生态高度碎片化：理解、生成、编辑任务各自使用不同的数据集、指标与协议，且多数基准仅支持单镜头、存在版权污染（Table 1–3）。UniVBench 通过以下设计打破这一局面：

- **任务统一**：首次将视频理解（V2T）、文本生成视频（T2V）、参考图像生成视频（R2V）、文本指令编辑（TV2V）、参考图像编辑（RV2V）以及**新提出的视频重建任务（V2V）**整合进同一基准。其中 V2V 任务要求模型先理解源视频再基于自生成的文本描述重建视频，从而直接诊断感知–生成耦合中的信息丢失（Figure 1）。
- **数据免版权**：200 个高质量视频（100 单镜头 + 100 多镜头，平均 3.72 个镜头）全部通过商用 API 生成并经三阶段人机过滤，从根本上消除了版权与数据污染问题。
- **多镜头支持**：与仅支持单镜头的现有基准不同，UniVBench 的视频源与文本标注均包含多镜头内容，更贴近真实应用场景。

### 2. 从标量评分到可解释的智能体评估系统（UniV-Eval）

传统评估指标（如 CLIP Score、FVD）输出单一标量分数，无法提供细粒度的错误归因。UniV-Eval 将评估转化为**动态规划与多维核查**过程（Figure 2）：

- **镜头级分解**：将视频机械分割为剪辑（$\{ \boldsymbol{\Vdash} \} = \{ \mathbf{c}_i \}_{i=1}^{C}$），再通过 PySceneDetect 分割为镜头单元（$V = \{ v_1, v_2, \dots, v_n \}$），并对齐参考图像（$I = \{ i_1, i_2, \dots, i_n \}$）与指令（$T = \{ t_1, t_2, \dots, t_n \}$）。
- **9 大类 21 子类别核查清单**：覆盖风格、主体（类别/质量/外观）、动作、背景、镜头（焦点/速度/视角）、光线、颜色、美学与一致性，将整体表现分解为可追溯的维度得分。
- **跨任务自适应**：系统接受任意任务类型的输入，经规划与分解后动态执行评估，最终输出细粒度核查清单，为模型训练优化提供可操作的反馈。

### 3. V2V 重建：感知–生成耦合的诊断探针

V2V 重建任务是 UniVBench 最具洞察力的创新。与 T2V 使用真实标注文本不同，V2V 仅依赖模型自身的理解文本进行重建。这一设计直接量化了**统一模型中理解能力向生成能力传递信息时的损耗**。实验表明，同一模型在 V2V 重建上的表现显著低于 T2V 生成（Figure 3），揭示出当前统一架构在感知–生成耦合上的关键瓶颈。这一发现为未来统一模型的架构设计提供了明确的改进方向。



UniVBench 的整体评估框架围绕两个核心组件构建：一个免版权、多镜头的视频数据集，以及一个统一的智能体评估系统 UniV‑Eval。这两者共同解决了现有视频评估基准碎片化、无法跨任务统一测量的问题。

### 数据集构建流水线

数据集的构建遵循一条从维度设计到人机过滤的完整流水线。首先，研究团队从先前工作中采纳了八个基础电影级维度，并将其扩展为 **21 个细粒度子维度**（Figure 1），涵盖风格、主体（类别、质量、外观）、动作、背景、摄像机（焦点、速度、角度）、光照、颜色与氛围等关键属性。基于这些维度，团队撰写视频脚本，并调用顶级商用 API（Hailuo、Kling、Veo3）生成原始视频素材。

![[assets/figures/papers/paper_list_l801_https_arxiv_org_abs_2602_21835/figures/001_Figure_1.jpg]]
*Figure 1: Overview of the UniVBench evaluation setting across 8 Dimensions, 21 Sub-Dimensions, and 6 Tasks. Given a source video, T2V synthesizes a video using its ground-truth caption, while V2V reconstructs the video based solely on the model’s self-generated understanding text, enabling a direct diagnosis of perception–generation coupling. UniVBench supports six unified tasks—video captioning (V2T), text-to-video generation (T2V), reference-image video generation (R2V), text-instruction video editing (TV2V), reference-image video editing (RV2V), and video reconstruction (V2V)*

生成后的视频经过 **三阶段人机协同过滤**：第一阶段由视觉‑语言模型自动去除水印和知识产权敏感内容；第二阶段由三位人工标注员独立审查视频质量与维度覆盖；第三阶段进行最终一致性校验。最终产出 **200 个高质量视频**，其中 100 个为单镜头视频，100 个为多镜头视频（平均 3.72 个镜头）。每个视频均配有多格式编辑指令、详细字幕标注以及 864 张多样化的参考图像。由于所有视频均为人工创作，该数据集从根本上规避了版权争议和数据污染问题（Table 1）。

### UniV‑Eval 智能体评估系统

UniV‑Eval 作为评估框架的核心引擎，负责将任意任务类型的输入转化为可解释的细粒度评估结果。其工作流程（Figure 2）包含三个关键阶段：

**1. 镜头级分解与对齐。** 系统首先将输入视频 $V$ 机械地分割为多个剪辑片段 $\{ \mathbf{c}_i \}_{i=1}^{C}$，随后使用 PySceneDetect 将多镜头视频进一步分割为 $n$ 个镜头单元 $V = \{ v_1, v_2, \dots, v_n \}$。参考图像和用户指令也被对应地对齐到各镜头：$I = \{ i_1, i_2, \dots, i_n \}$，$T = \{ t_1, t_2, \dots, t_n \}$。

**2. 多维度核查清单评估。** 针对每个镜头，UniV‑Eval 依据 **9 大类、21 个子类别**的核查清单进行评分。这些类别与数据集构建时的维度设计保持一致，确保评估与数据生成遵循同一语义框架。系统动态地根据任务类型调整评估重点——例如，在视频理解（V2T）任务中侧重文本描述与视觉内容的对齐度，在视频重建（V2V）任务中则同时考察生成质量与源视频的保真度。

**3. 跨任务统一打分与汇总。** 各镜头的子维度得分被汇总为六个任务维度的整体表现。UniV‑Eval 使用 Seed‑1.6 作为底层评判大模型，通过标准化提示和指令解析，确保不同任务、不同模型之间的评分具有可比性。最终输出不仅包含总体分数，还提供可追溯的逐项错误归因，使模型开发者能够定位到具体的感知或生成瓶颈。

### 六项统一任务的设计逻辑

UniVBench 支持六项统一任务，覆盖视频基础模型的四大核心能力（Figure 1）：

- **视频理解（V2T）**：给定源视频，模型生成描述性字幕。
- **文本到视频生成（T2V）**：使用视频的真实标注文本合成视频。
- **参考图像视频生成（R2V）**：基于参考图像和文本提示生成视频。
- **文本指令视频编辑（TV2V）**：根据文本编辑指令修改源视频。
- **参考图像视频编辑（RV2V）**：结合参考图像和指令进行视频编辑。
- **视频重建（V2V）**：模型先理解源视频生成字幕，再基于自生成的字幕重建视频。

其中，V2V 重建任务是 UniVBench 的关键创新。它通过对比 T2V（使用真实标注文本）与 V2V（使用模型自生成理解文本）的表现差异，直接诊断感知‑生成耦合中的信息丢失。这一设计使得 UniVBench 不仅是一个评估工具，更是一个模型诊断框架。

### 输入输出流的统一性

所有基线模型在评估中接收完全相同的输入：T2V 任务使用统一的真实标注字幕；TV2V 和 RV2V 任务使用相同的源视频和编辑指令；R2V 任务使用一致的参考图像和提示。对于不支持某些任务的模型（如纯生成模型无法进行 V2T 理解），研究团队实施了最小化适应性修改（如使用 GPT‑4o 替代模型自身的理解组件生成 V2V 所需的字幕），并在论文中明确说明。所有模型统一采用 50 步 DDIM 采样、分类器无关引导系数 7.5、原生分辨率 720×480 的推理配置，从机制层面消除了评估偏差。



### 视频数据构建流水线

UniVBench 的数据集构建围绕一个核心设计原则：**通过人工创作与商业 API 合成相结合的方式，构建一个免版权、多镜头、多任务统一评估的视频基准**。该流水线包含以下关键步骤：

1. **维度脚本撰写**：基于 8 大电影级维度（风格、主体、动作、背景、摄影机、光照、氛围、特效）及 21 个子维度，撰写详细的视频脚本，确保覆盖多样化的视觉语义属性（Table 2）。
2. **商业 API 生成**：利用顶级商业视频生成 API（Hailuo、Kling、Veo3）根据脚本合成视频素材。
3. **三阶段人机过滤**：
   - **自动预过滤**：通过视觉语言模型自动去除含水印或受知识产权保护的内容。
   - **人工审查**：由三位标注者进行独立审查，仅保留一致通过的视频。
   - **质量精修**：对入选视频进行最终的质量校验与细节修正。
4. **标注生成**：为每个视频配以详细字幕、多格式编辑指令及参考图像。最终产出 100 个单镜头视频和 100 个多镜头视频（平均 3.72 个镜头），以及 864 张独特的参考图像。

### UniV-Eval 智能体评估系统

UniV-Eval 是 UniVBench 的核心评估引擎，其设计瓶颈在于：**传统评估指标（如 CLIP Score、FVD）仅提供单一标量分数，无法对视频生成/编辑质量进行细粒度、可追溯的错误归因**。UniV-Eval 通过以下模块化流程解决该问题（Figure 2）：

![[assets/figures/papers/paper_list_l801_https_arxiv_org_abs_2602_21835/figures/005_Figure_2.jpg]]
*Figure 2: Workflow of UniV-Eval. The system accepts arbitrary inputs within a task setting and performs dynamic evaluation after planning and decomposition. The final results are delivered as a fine-grained checklist, providing traceable feedback for training optimization*

1. **镜头分割与对齐**：将输入视频按镜头边界进行机械分割，并对齐参考图像与编辑指令。
2. **动态评估规划**：根据任务类型（V2T、T2V、TV2V、R2V、RV2V、V2V）动态选择评估维度与子类别。
3. **细粒度核查清单打分**：在 9 大类、21 子类别上逐项评分，最终汇总为六维得分。

### 关键公式与变量含义

UniV-Eval 的镜头分割与对齐过程由以下公式定义：

**剪辑分割**：将长视频 $V$ 机械地分割为多个剪辑（clips）：

$$\{ \boldsymbol { \Vdash } \} = \{ \mathbf { c } _ { i } \} _ { i = 1 } ^ { C }$$

其中 $\{ \boldsymbol { \Vdash } \}$ 表示剪辑集合，$\mathbf{c}_i$ 为第 $i$ 个剪辑，$C$ 为剪辑总数。

**镜头分割**：使用 PySceneDetect 将多镜头视频进一步分割为 $n$ 个镜头单元：

$$V = \{ v _ { 1 } , v _ { 2 } , \dots , v _ { n } \}$$

其中 $v_j$ 表示第 $j$ 个镜头单元。

**参考图像对齐**：将参考图像集合对齐到对应镜头：

$$I = \{ i _ { 1 } , i _ { 2 } , \dots , i _ { n } \}$$

其中 $i_j$ 为与镜头 $v_j$ 对应的参考图像。

**指令对齐**：将用户编辑指令对齐到对应镜头：

$$T = \{ t _ { 1 } , t _ { 2 } , \dots , t _ { n } \}$$

其中 $t_j$ 为与镜头 $v_j$ 对应的文本指令。

上述对齐机制使得 UniV-Eval 能够在镜头粒度上进行精确的逐项核查，而非对整个视频给出模糊的总体评价。这是实现可解释错误归因的关键设计。



## 实验与关键发现

### 实验设置

为消除评估偏差，所有基线模型均采用统一的推理配置：50 步 DDIM 采样，分类器引导尺度 7.5，原生分辨率 720×480（16∶9 视频）。对于不支持特定任务的模型，实验实施了最小化的适应性修改（例如将指令文本与源视频嵌入拼接），并在文中明确说明。评估端使用 **Seed‑1.6** 作为 UniV‑Eval 的底层大语言模型评判器。

UniVBench 的数据集构建过程本身即构成一项实验验证：200 个视频（100 个单镜头 + 100 个多镜头，平均 3.72 个镜头）全部由商用 API（Hailuo、Kling、Veo3）生成，经三阶段人机过滤（自动预过滤去除水印和 IP 内容 → 三人独立审核 → 专家最终确认），并配以 864 张独特参考图像。这一流程确保了数据集无版权污染且可自由编辑，为编辑和重建任务的公平评估提供了基础。

### 主要结果

**Table 4** 汇总了各基线模型在 UniVBench 六项任务、八个维度上的性能对比。核心发现如下：

**没有任何单一模型在理解、生成、编辑和重建任务上同时表现出色**，这直接量化了当前视频基础模型的“统一鸿沟”。

- **视频理解（V2T）**：**Gemini 2.5 Pro** 以 54.1% 的平均八维得分领先，而统一模型 **Showo‑2** 仅获 16.3%，差距达 +37.8 个百分点。这表明现有统一模型的理解能力远落后于专用理解模型。
- **文本到视频生成（T2V）**：**Seedance‑1.0‑Pro** 取得 77.9% 的最高平均得分，**CoDi‑2** 仅为 40.1%，差距同样为 +37.8 个百分点。
- **视频重建（V2V）**：**Wan2.1‑VACE‑14B** 以 62.7% 领先，而 **CogVideoX‑1.5‑5B** 仅 20.7%，差距扩大至 +42.0 个百分点。V2V 任务的表现显著低于 T2V 生成，揭示了感知‑生成耦合中的信息丢失。
- **视频编辑（TV2V / RV2V）** 和 **参考图像生成（R2V）** 目前仅有单一模型展示结果（TV2V：Wan2.1‑VACE‑14B 65.1%；RV2V：同模型 66.4%；R2V：Seedance‑1.0‑Lite 66.7%），缺乏多模型对比，结论的稳健性需要更多基线验证。

**维度级别的错误归因**进一步揭示了模型的能力瓶颈：生成模型在**动作**维度得分普遍偏低，而感知模型在**风格**属性上表现更弱。UniV‑Eval 的细粒度核查清单使得这类诊断成为可能，而传统单一标量指标无法提供此类信息。

### 消融与诊断分析

#### V2V 重建 vs. T2V 生成：感知‑生成耦合诊断

UniVBench 的核心诊断设计在于 V2V 重建任务：T2V 使用真实标注文本生成视频，而 V2V 则依赖模型自身理解组件生成的文本进行重建。**Figure 3** 的案例定性分析显示，V2V 重建视频相较于 T2V 生成视频表现出更显著的不一致——背景细节丢失、主体外观偏移、动作时序错乱等问题频发。这一对比直接证明了 V2T → T2V 流水线中存在信息丢失，且该丢失同时涉及理解阶段（未能完整捕获视频语义）和生成阶段（未能从文本中忠实还原）。

#### UniV‑Eval 与人工评判的一致性

为验证评估系统的可靠性，研究团队进行了人工专家标注实验。**Figure 5** 的结果显示，UniV‑Eval 的整体评估与人工专家评判的平均一致性接近 **85%**，表明智能体评估系统在细粒度、多维度打分上具备可信的参考价值。此外，**Table D1**（附录）显示单次评估成本低于 10 美元，具备规模化部署的可行性。

![[assets/figures/papers/paper_list_l801_https_arxiv_org_abs_2602_21835/figures/008_Figure_5.jpg]]
*Figure 5: Human expert annotations used to validate the reliability of UniV-Eval*

![[assets/figures/papers/paper_list_l801_https_arxiv_org_abs_2602_21835/figures/010_Table.jpg]]
*Table: Average cost of running one case is provided in Table D1. The cost of evaluating one task is less than 10 US dollars. Table D1. The cost of evaluation*

### 现有基准的覆盖缺陷

**Table 1** 系统对比了现有视频理解、生成和编辑基准，揭示了三重结构性缺陷：
- **任务碎片化**：大多数基准仅支持单一任务（理解或生成），无法支持统一评估；
- **单镜头局限**：现有基准的视频源和文本标注几乎不包含多镜头内容，无法评估模型对镜头切换、时序逻辑的理解与生成能力；
- **版权污染**：多数基准使用受版权保护的网络视频，限制了编辑和重建任务的评估合法性。

**Table 2** 进一步从电影级维度（风格、主体、动作、背景、灯光、摄像机运动等）对比了不同基准的覆盖程度，显示现有基准在细粒度视觉属性上的评估能力严重不足。**Table 3** 则对比了现有评估指标与 UniV‑Eval 在细粒度、多镜头、多维度及跨任务支持方面的能力差距，确认传统指标（如 FID、CLIPScore）无法提供可解释的多维度反馈。

### 失败模式与局限性

1. **统一模型的系统性短板**：当前统一模型在 V2V 重建任务上的普遍低分表明，感知与生成的深度耦合仍是未解决的架构挑战。多数模型在理解阶段遗漏的语义信息无法在生成阶段被补偿。
2. **数据集规模与多样性**：UniVBench 目前仅包含 200 个视频，覆盖的风格和场景种类有限，可能不足以完全代表真实世界的视频多样性，部分维度（如极端光照、快速运动）的评估可能不够充分。
3. **评估系统的潜在偏差**：UniV‑Eval 依赖 Seed‑1.6 作为评判 LLM，尽管与人工一致性高，但在某些边缘情况（如高度抽象的艺术风格、文化特定内容）仍可能产生系统偏差，需要进一步的人工校准验证。
4. **编辑与参考图像生成任务的基线不足**：TV2V、RV2V 和 R2V 任务目前仅有单一模型结果，无法进行有意义的模型间对比，这些任务上的结论需要更多基线模型的支持。

### 开放问题

- 当前统一模型在 V2V 重建中的信息丢失究竟主要源自理解阶段还是生成阶段？是否可以设计更具针对性的诊断实验（如使用真实标注文本作为中间表示）来解耦这两个因素？
- UniV‑Eval 的智能体评估框架能否推广到其他跨模态任务（如图像‑视频联合编辑、多模态对话）？
- 如何进一步扩大 UniVBench 的数据集规模并引入更多样的视频来源（如实拍视频、动画、游戏画面），以增强评估的生态效度？

### 补充图表

![[assets/figures/papers/paper_list_l801_https_arxiv_org_abs_2602_21835/figures/007_Table_4.jpg]]
*Table 4: Performance comparison of different baselines on UniVBench, summarizing results over six tasks, across eight dimensions*

![[assets/figures/papers/paper_list_l801_https_arxiv_org_abs_2602_21835/figures/002_Table_1.jpg]]
*Table 1: Comparison of benchmarks for video understanding, generation and editing. Multi-task shows the applicable tasks of the benchmark. Multi-shot indicates that whether the video source and text annotations have multi-shot content. Copyright Issue indicates whether the video sources in the dataset are editable without copyright issue*

![[assets/figures/papers/paper_list_l801_https_arxiv_org_abs_2602_21835/figures/003_Table_2.jpg]]
*Table 2: Comparison of cinematic dimensions across different video evaluation benchmarks*

![[assets/figures/papers/paper_list_l801_https_arxiv_org_abs_2602_21835/figures/004_Table_3.jpg]]
*Table 3: Comparison of core capabilities across existing evaluation metrics and our proposed agent-based evaluation system. “-” indicates the metric is not applicable to this dimension*

![[assets/figures/papers/paper_list_l801_https_arxiv_org_abs_2602_21835/figures/009_Figure_4.jpg]]
*Figure 4: An example of evaluation using different metrics, where the blue-highlighted part shows that UniV-Eval provides more detailed, traceable validation and assessment*

![[assets/figures/papers/paper_list_l801_https_arxiv_org_abs_2602_21835/figures/006_Table.jpg]]
*Table: Note: Model types are separated into: ‡Commercial Models, §Open-Source Models*



## 定位与知识库关联

### 与现有基准的关系

UniVBench 在视频评估领域填补了一个系统性的空白：**从碎片化的单任务评估走向统一的多能力诊断**。现有基准可以被清晰地划分为三类，UniVBench 在每一类上都做出了差异化贡献。

**视频理解基准**（如 ActivityNet、MSVD、MSR-VTT 等）长期依赖从 YouTube 等平台采集的版权视频，且仅支持视频描述（V2T）单一任务。这些基准无法评估模型在生成和编辑上的能力，更无法支持需要源视频的编辑与重建任务——因为版权约束使得对视频进行修改和再分发在法律上不可行（Table 1）。

**视频生成与编辑基准**（如 VBench、EvalCrafter、VEditBench 等）虽然引入了多维度的评估框架，但普遍存在两个关键缺陷：其一，视频素材以单镜头为主，缺乏对多镜头叙事结构的覆盖；其二，评估指标（如 CLIP Score、FVD）仅提供粗粒度的整体相似度，无法将性能差异归因到具体的视觉维度（如动作连贯性、风格一致性、光照合理性）。Table 2 和 Table 3 的对比清晰地展示了这一维度覆盖的鸿沟。

**统一模型评估**的尝试（如 OmniBench、UniBench 等）开始将理解与生成放在同一框架下比较，但其任务定义仍局限于“理解+生成”的并行评估，并未触及两者之间的**耦合诊断**——即模型从理解到生成的闭环中，信息在哪个环节丢失。UniVBench 通过引入视频重建（V2V）任务，首次将这一问题显式化为可测量的评估目标。

### 方法适用边界

UniVBench 的设计决策决定了其适用范围和约束条件：

1. **数据集规模与多样性边界**：当前版本包含 200 个视频（100 个单镜头 + 100 个多镜头，平均 3.72 个镜头），覆盖 8 个主维度和 21 个子维度。这一规模适合作为**诊断性基准**（diagnostic benchmark），而非大规模训练或统计显著性检验。视频内容通过商业 API（Hailuo、Kling、Veo3）生成，虽确保了版权清洁，但生成视频的视觉分布可能与真实拍摄视频存在系统性偏差，这会影响评估结果向真实场景的泛化。

2. **任务覆盖边界**：UniVBench 覆盖了六项任务（V2T、T2V、R2V、TV2V、RV2V、V2V），但未包含视频插帧、超分辨率、风格迁移等更细粒度的编辑子任务。此外，当前任务设计假设输入为单条指令或单张参考图像，不支持多轮交互式编辑的场景。

3. **评估器依赖边界**：UniV-Eval 使用 Seed-1.6 作为评判 LLM，其评估质量受限于该模型的视觉理解能力和指令遵循能力。尽管与人工专家的一致性达到约 85%（Figure 5），但在涉及高度主观的美学判断（如“风格的艺术性”）或极端边缘情况时，仍可能出现系统偏差。单次评估成本低于 10 美元（Table D1），具备规模化可行性，但在大规模模型迭代中仍需权衡成本与评估频率。

4. **模型适配边界**：对于不支持某些任务的模型，论文实施了最小化的适应性修改（如将指令文本与源视频嵌入拼接），但这种“桥接”方式可能无法完全释放模型在原任务上的潜力，导致跨任务比较时存在一定的公平性折衷。

### 局限与开放问题

**已知局限**（论文明确指出的）：

- 数据集 200 个视频的规模限制了风格和场景的覆盖广度，不足以完全代表真实世界的视频多样性。
- UniV-Eval 依赖 LLM 评判，尽管与人工一致性高，仍可能在边缘情况产生系统偏差。
- V2V 重建任务对模型的理解-生成耦合能力要求极高，当前多数模型在此任务上表现较弱，限制了该任务的区分度。

**开放问题**（需要进一步探索的方向）：

1. **规模扩展与分布偏移**：如何将 UniVBench 扩展到更大规模（如 1000+ 视频）并引入更多样的视频来源（如用户生成内容、专业影视片段），同时保持版权清洁？规模扩展后，生成视频与真实视频的分布偏移是否会导致评估结论的系统性变化？

2. **跨模态推广**：UniV-Eval 的智能体评估框架（镜头分割→分类对齐→细粒度打分→汇总）是否适用于其他跨模态任务？例如，图像-视频联合编辑、音频-视频同步生成等场景是否能复用相同的维度体系和评估逻辑？

3. **信息丢失的归因诊断**：当前 V2V 重建任务揭示了统一模型中存在显著的信息丢失（Figure 3），但无法区分丢失主要发生在理解阶段（V2T 的描述不够精确）还是生成阶段（T2V 未能忠实还原描述）。设计更具针对性的诊断实验——例如控制描述质量的分层实验——将是理解统一模型瓶颈的关键。

4. **评估指标的因果性**：当前 UniV-Eval 的维度得分是相关性指标（视频与指令的匹配程度），而非因果性指标（模型是否“真正理解”了场景）。如何设计反事实评估（counterfactual evaluation）来测试模型对特定维度变化的敏感性，是一个值得深入的方向。

5. **统一模型的架构启示**：Table 4 显示生成模型在动作维度得分普遍偏低，而感知模型在风格属性上更弱。这一模式是否暗示当前统一架构中感知编码器与生成解码器之间存在模态对齐的瓶颈？能否基于 UniVBench 的诊断结果反推架构改进的方向？



## 原文 PDF

![[paperPDFs/CVPR_2026/UniVBench_Towards_Unified_Evaluation_for_Video_Foundation_Models.pdf]]
