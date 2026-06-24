---
title: "Reasoning Paths with Reference Objects Elicit Quantitative Spatial Reasoning in Large Vision-Language Models"
type: paper
paper_level: A
venue: EMNLP
year: 2025
pdf_ref: paperPDFs/EMNLP_2025/Reasoning_Paths_with_Reference_Objects_Elicit_Quantitative_Spatial_Reasoning_in_Large_Vision_Language_Models.pdf
project_link: https://andrewliao11.github.io/spatial_prompt/
aliases:
- RPROEQSRLVLM
tags:
- EMNLP_2025
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/vision_models_multimodal
core_operator: "推理过程中是否显式利用场景中的参考物体（其空间尺寸可通过常识推断）作为视觉锚点，进行相对比较和估计。"
primary_logic: "性能最佳的VLM（GPT-4o）在正确回答时会自然涌现出利用参考物体的推理路径。通过设计零样本提示SpatialPrompt显式引导VLM识别和使用参考物体，可以在不增加任何数据、不修改模型架构、不进行微调的情况下，大幅提升多种VLM的定量空间推理成功率（例如Gemini 1.5 Pro提升超过50个点）。这揭示了通过提示工程激发模型隐藏推理能力的高效路径。"
claims:
- "GPT-4o在响应中使用参考物体时，成功率δ≤2达到83%（45/54），而不使用时仅为64%（114/177），提升19个百分点。"
- "逻辑回归分析表明，使用参考物体使准确估计的几率提高约2.7倍（β_r=1.0179，p<0.05），且该效应独立于数据集和真实距离大小。"
- "SpatialPrompt将Gemini 1.5 Pro在Q-Spatial-ScanNet上的成功率从0.59提升至53.65（+53.06点），将GPT-4V在Q-Spatial++上的成功率从18.81提升至53.47（+34.66点）。"
- "在所有VLM和提示技术中，参考对象使用频率与成功率之间的Spearman相关系数在Q-Spatial-ScanNet上为0.69，在Q-Spatial++上高达0.91。"
---

# Reasoning Paths with Reference Objects Elicit Quantitative Spatial Reasoning in Large Vision-Language Models

> [!tip] 核心洞察
> 性能最佳的VLM（GPT-4o）在正确回答时会自然涌现出利用参考物体的推理路径。通过设计零样本提示SpatialPrompt显式引导VLM识别和使用参考物体，可以在不增加任何数据、不修改模型架构、不进行微调的情况下，大幅提升多种VLM的定量空间推理成功率（例如Gemini 1.5 Pro提升超过50个点）。这揭示了通过提示工程激发模型隐藏推理能力的高效路径。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 使用参考物体的推理路径激发大视觉语言模型中的量化空间推理 |
| 英文题名 | Reasoning Paths with Reference Objects Elicit Quantitative Spatial Reasoning in Large Vision-Language Models |
| 会议/期刊 | EMNLP 2025 |
| Links | [paper](https://arxiv.org/abs/2409.09788); [Project](https://andrewliao11.github.io/spatial_prompt); [Project](https://andrewliao11.github.io/spatial_prompt/) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/vision_models_multimodal |
| Method | SpatialPrompt |
| Dataset | Q-Spatial-ScanNet, Q-Spatial++ |

> [!tip] 效果简介
> - Q-Spatial-ScanNet 上，δ≤2 success rate 为 53.65，对比 0.59，变化 +53.06。
> - Q-Spatial++ 上，δ≤2 success rate 为 53.47，对比 18.81，变化 +34.66。
> - Q-Spatial-ScanNet 上，δ≤2 success rate 为 71.96，对比 69.41，变化 +2.55。

## 概述

当前大视觉语言模型（VLM）在缺乏外部工具和额外训练的条件下，从单张2D图像估计物体精确距离与尺寸的定量空间推理能力严重不足，尤其在水平距离问题上几乎失效。本文揭示了一个关键发现：性能最强的VLM（GPT-4o）在正确回答时，会自然涌现出利用场景中**参考物体**（其空间尺寸可通过常识推断）作为视觉锚点的推理路径。基于此，作者提出了**SpatialPrompt**——一种零样本提示技术，在不增加任何数据、不修改模型架构、不进行微调的前提下，显式引导VLM识别和使用参考物体进行相对比较与估计。

核心结论如下：
- 在GPT-4o的响应中，使用参考物体时成功率（δ≤2）达到83%，而不使用时仅为64%，提升19个百分点；逻辑回归分析表明，使用参考物体使准确估计的几率提高约2.7倍（β_r=1.0179，p<0.05），且该效应独立于数据集和真实距离大小。
- SpatialPrompt将Gemini 1.5 Pro在Q-Spatial-ScanNet上的成功率从0.59提升至53.65（+53.06点），将GPT-4V在Q-Spatial++上的成功率从18.81提升至53.47（+34.66点）。
- 在所有VLM和提示技术中，参考对象使用频率与成功率之间的Spearman相关系数在Q-Spatial-ScanNet上为0.69，在Q-Spatial++上高达0.91，强有力地验证了“通过参考物体推理直接提升定量空间准确性”的因果假设。

方法上，SpatialPrompt属于**提示工程/零样本推理增强**范式，与标准提示（直接询问距离数值）和零样本思维链（Zero-shot CoT）形成对比。它通过修改提示指令这一单一插槽，将模型从无引导的逐步推理转变为显式利用参考物体的结构化推理。该方法对GPT-4V/4o和Gemini系列模型均有效，但在开源模型（如LLaVA系列）上的提升不稳定，提示格式敏感性显著（例如详细步骤版SpatialPrompt-Steps对GPT-4V/4o有负面影响，却对Gemini系列至关重要）。

实验基于自建的Q-Spatial Bench（271道人工标注题目，含Q-Spatial-ScanNet与Q-Spatial++两个子集），以最大比值度量δ = max(ˆd/d*, d*/ˆd) ≤ 2为成功标准。尽管SpatialPrompt大幅缩小了VLM与人类（平均成功率90）的差距，GPT-4o最佳成绩仍落后人类约30个点，表明该基准对人类简单但对VLM极具挑战，仍有巨大提升空间。

## 背景与动机

### 定量空间推理：视觉语言模型的盲区

当前大视觉语言模型（Large Vision-Language Models, VLMs）在图像描述、视觉问答等语义理解任务上取得了显著进展，然而，当任务要求从单张2D图像中精确估计物体的距离或尺寸时，这些模型暴露出严重的定量空间推理缺陷。这一能力在机器人操控、增强现实和自主导航等现实应用中至关重要，但现有VLMs在缺乏外部深度传感器或额外微调的情况下，几乎无法可靠地完成此类估计。

问题的核心瓶颈在于：VLMs缺乏将像素级视觉信息转化为物理世界度量单位的有效机制。与人类能够通过场景中的参考物体（例如，已知标准尺寸的门、椅子、键盘等）进行相对比较和估算不同，现有模型往往直接尝试从图像特征中“猜测”绝对距离，导致估计结果极不稳定。实验表明，即使是性能最强的商业模型GPT-4o，在水平距离问题上的成功率也仅为49.44%（Table 3），而Gemini 1.5 Pro在标准提示下甚至频繁拒绝提供任何测量值（Table 2）。

### 现有方法的局限

针对VLMs的空间推理能力，已有研究主要沿两条路径展开：

- **微调路径**：如SpatialVLM通过构建包含数十亿问答对的大规模合成数据集对模型进行微调，试图将空间度量知识直接注入模型参数。然而，该方法在Q-Spatial Bench上的相对提升不足4个百分点，且需要高昂的数据构建和训练成本，难以泛化至未见场景。

- **工具增强路径**：部分工作依赖外部深度估计器或3D重建模块来辅助空间推理，但这增加了系统复杂性和部署门槛，且无法利用VLMs自身的常识推理潜力。

上述方法均未触及一个关键观察：**性能最优的VLM（GPT-4o）在正确回答时，其推理路径中会自然涌现出对参考物体的使用**。在GPT-4o的231个有效回答中，有23.4%的实例自发地识别并利用了场景中的参考物体（Table 4）。更引人注目的是，当使用参考物体时，成功率δ≤2达到83%（45/54），而未使用时仅为64%（114/177）——这一19个百分点的差距暗示着参考物体是解锁定量空间推理能力的关键“因果旋钮”。

### 动机：通过提示工程激发隐藏能力

逻辑回归分析为上述观察提供了统计显著性证据：使用参考物体使准确估计（δ≤2）的几率提高约2.7倍（β_r=1.0179，p<0.05），且该效应独立于数据集来源和真实距离大小（Table 5）。这揭示了一个重要洞见：**VLMs并非完全缺乏空间推理能力，而是缺乏正确的推理策略引导**。

基于此，本文提出一个核心假设：如果能够显式地引导VLM在推理过程中识别和使用参考物体，是否可以在不修改模型架构、不增加训练数据、不依赖外部工具的前提下，大幅提升其定量空间推理性能？这一假设将研究焦点从模型能力的“有无”问题转向了能力的“激发”问题，为高效提升VLMs的空间推理能力开辟了一条零样本提示工程的新路径。

## 核心创新

### 问题瓶颈的因果定位

当前大视觉语言模型（VLMs）在从单张2D图像估计物体精确距离和尺寸的定量空间推理任务上表现严重不足。在Q-Spatial Bench基准测试中，即便性能最强的GPT-4o，其整体成功率（δ≤2）也仅约65%，远低于人类水平的90%（Table 12）。更关键的是，模型在水平距离问题上的表现几乎失效——GPT-4o的成功率仅为49.44%，GPT-4V和Gemini 1.5 Flash更是降至10%和13.33%（Table 3）。这一瓶颈的根源并非模型缺乏视觉理解能力，而在于推理过程中缺少一个关键的**因果调节变量**：是否显式利用场景中具有可推断常识尺寸的参考物体作为视觉锚点，进行相对比较和估计。

### 核心洞察：参考物体推理路径的自然涌现

通过对GPT-4o正确响应进行定性分析，研究者发现了一个关键现象：当GPT-4o成功给出准确估计时，其响应中会自然涌现出一条利用参考物体（reference object）的推理路径（Figure 2）。所谓参考物体，是指场景中那些可通过常识推理轻易推断其空间尺寸的物体（如标准门高约2米、键盘长约45厘米等）。模型会先估计参考物体的尺寸，再通过与参考物体的相对比例关系推算目标距离或尺寸。

定量分析证实了这一洞察的统计显著性。在GPT-4o的全部响应中，仅有23.4%的实例使用了参考物体，但在这些使用参考物体的54个问题中，成功率δ≤2高达83%（45/54），而未使用参考物体的177个问题中成功率仅为64%（114/177），两者相差19个百分点（Table 4）。逻辑回归分析进一步表明，使用参考物体使准确估计的几率提高约2.7倍（β_r=1.0179, p<0.05），且该效应独立于数据集分割和真实距离大小，真实距离本身并非显著预测因子（Table 5）。

### 方法创新：SpatialPrompt零样本提示策略

基于上述洞察，研究者提出了**SpatialPrompt**——一种零样本提示技术，其核心创新在于通过纯文本提示工程显式引导VLM进行参考物体推理，而**无需任何额外训练数据、模型架构修改或参数微调**。

#### Changed Slot：提示指令的范式转换

与基线方法的关键差异体现在提示指令这一核心slot上：

- **Standard prompt基线**：直接要求模型输出距离数值，未提供任何推理策略指引（Figure 6）。
- **Zero-shot Chain-of-Thought (CoT)基线**（Kojima et al., 2022）：鼓励逐步推理，但不显式要求使用参考物体。
- **SpatialPrompt**：在提示中显式指导模型执行以下步骤：①首先识别图像中可作为参考的物体；②利用常识推理估计该参考物体的标准尺寸；③通过与参考物体的相对比较推算出目标距离或尺寸。

SpatialPrompt提供两种变体以适应不同模型的提示敏感性（Figure 3, Figure 8）：
- **SpatialPrompt-Single**：紧凑的单步版本，受零样本CoT启发，保持提示简洁易记。
- **SpatialPrompt-Steps**：包含详细分解步骤的版本，逐步引导模型完成识别参考物、估计参考尺寸、相对比较推算的全过程。

这一提示策略的关键效果在于大幅提升参考物体的使用频率。在Q-Spatial-ScanNet上，Gemini 1.5 Pro的参考物体使用频率从标准提示下的7.64%飙升至SpatialPrompt下的99.17%，GPT-4V从18.12%升至99.8%（Table 11）。参考物体使用频率与成功率之间的Spearman相关系数在Q-Spatial-ScanNet上达到0.69，在Q-Spatial++上高达0.91（Figure 4），强有力地验证了参考物体推理路径是提升定量空间推理能力的核心机制。

### 方法谱系与知识库定位

SpatialPrompt定位于**零样本提示工程**范式，区别于以下两类相关工作：

- **基于微调的方法**：如SpatialVLM通过生成2亿QA对进行微调，但在相同指标上仅取得不足4个点的相对提升。SpatialPrompt以零成本提示策略实现了数倍于此的性能增益，揭示了激发模型隐藏能力的更高效路径。
- **依赖外部工具的方法**：部分工作借助深度传感器或多视角信息增强空间推理，而SpatialPrompt仅需单张2D图像和文本提示，保持了方法的通用性和部署便捷性。

在提示技术谱系中，SpatialPrompt可视为对零样本CoT的定向增强——后者提供通用推理框架，前者则针对定量空间推理这一特定任务注入了领域特异性的推理策略（参考物体识别与相对比较）。这种“任务感知提示设计”的思路为提示工程提供了新的方法论参考：通过观察模型在成功案例中自然涌现的有效推理模式，将其显式编码为提示指令，从而系统性地激发模型的潜在能力。

## 整体框架

本文提出了一套“基准构建→能力诊断→机制分析→提示干预”的完整研究管线，用于激发和评估大视觉语言模型（VLM）在单张2D图像上的量化空间推理能力。整个框架围绕一个核心发现展开：当VLM在推理中显式利用场景中的**参考物体**（其空间尺寸可通过常识推断）作为视觉锚点时，距离估计的准确性会显著提升。

### 管线总览

研究管线由四个阶段构成，数据流和模块关系如下：

1. **基准构建（Q-Spatial Bench）**：构造一个人类专家标注的量化空间推理基准，包含两个互补的数据分割——Q-Spatial-ScanNet（基于公开ScanNet数据集重新标注）和Q-Spatial++（全新拍摄图像，专门评估泛化能力），共计271道题目，覆盖五类空间问题（Figure 1、Table 1）。该基准输出标准化的图像-问题-真实距离三元组，作为后续所有评估的统一输入。

2. **能力诊断（商业VLM基准评估）**：将基准输入到多个商业和开源VLM（GPT-4o、GPT-4V、Gemini 1.5 Pro/Flash、LLaVA系列），使用最大比值度量 $\delta = \max(\hat{d}/d^*, d^*/\hat{d})$ 评估估计精度，以 $\delta \leq 2$ 作为成功阈值（Table 2、Table 3）。该阶段揭示了两个关键瓶颈：（a）水平距离问题是所有VLM的共性短板；（b）GPT-4o虽整体最优，但其成功响应中自然涌现出利用参考物体的推理路径。

3. **机制分析（参考物体效应验证）**：对GPT-4o的响应进行系统性分析，通过另一个独立的GPT-4o实例判断每个响应是否使用了参考物体（Figure 5辅助提示）。列联表分析（Table 4）表明，使用参考物体时成功率从64%跃升至83%；逻辑回归模型 $p(\delta_{\leq 2}) \sim \beta_0 + \beta_r X_r + \beta_d X_d + \beta_g X_g$ 进一步确认，使用参考物体使准确估计的几率提高约2.7倍（$\beta_r = 1.0179$，$p < 0.05$），且该效应独立于数据集分割和真实距离大小（Table 5）。这一阶段确立了“参考物体使用”作为因果操纵变量。

4. **提示干预（SpatialPrompt）**：基于上述因果发现，设计零样本提示技术SpatialPrompt，在不修改模型架构、不增加训练数据、不进行微调的前提下，显式引导VLM在推理中执行“识别参考物体→常识推理其标准尺寸→相对比较推算目标距离”的路径。SpatialPrompt提供两种变体：紧凑的单步版（SpatialPrompt-Single）和包含详细分解步骤的版（SpatialPrompt-Steps）（Figure 3、Figure 8）。该提示作为文本前缀与图像-问题对拼接后输入VLM，输出距离估计值。

### 模块间的输入输出关系

整个框架的模块间耦合简洁而可复现：

- **基准构建** → **能力诊断**：Q-Spatial Bench提供标准化的评估数据，确保不同VLM和提示技术的可比性。
- **能力诊断** → **机制分析**：GPT-4o的响应文本被送入独立的判断模块，提取“是否使用参考物体”的二值标签，与成功率进行统计关联分析。
- **机制分析** → **提示干预**：逻辑回归确证的因果关系直接驱动SpatialPrompt的设计——将“使用参考物体”从涌现行为转化为显式指令。
- **提示干预** → **能力诊断**（闭环验证）：SpatialPrompt应用于所有VLM后，重新在Q-Spatial Bench上评估，验证干预效果（Table 6、Table 8）。

### 关键设计决策

- **零样本约束**：整个管线严格保持零样本设定，不引入任何任务特定的微调数据。这使SpatialPrompt与需要大规模训练数据的方案（如SpatialVLM，在相似指标上仅提升不到4个点）形成鲜明对比，凸显了提示工程在激发模型隐藏能力方面的高效性。
- **双分割评估**：Q-Spatial-ScanNet用于评估可能存在训练数据泄漏风险的公开数据表现，Q-Spatial++则专门测试对全新场景的泛化能力。两者在管线中并行使用，提供互补的证据强度。
- **多模型覆盖**：管线同时覆盖商业黑盒模型（GPT系列、Gemini系列）和开源模型（LLaVA系列），以检验SpatialPrompt的跨模型鲁棒性。实验发现不同模型对提示格式的敏感度差异显著——例如，详细步骤版（SpatialPrompt-Steps）对Gemini 1.5 Pro至关重要（不使用则几乎不响应），但对GPT-4V/4o反而有负面影响（Table 8）——这揭示了提示设计与模型特性之间的复杂交互，也是当前框架的一个开放问题。

### 框架的边界条件

该框架的有效性受限于以下条件：（1）场景中需存在可被常识推理的参考物体，缺乏明确参照物时SpatialPrompt的增益有限；（2）VLM需具备基本的常识推理能力，模型规模过小（如LLaVA-7B）时提示干预效果不稳定；（3）评估指标 $\delta \leq 2$ 相对宽松（允许0.5×到2×误差），无法精细区分高精度估计能力；（4）仅限单张2D图像输入，未涉及多视角或深度传感器信息。这些边界条件在管线设计中已被显式识别，但尚未被系统性解决。

## 核心模块与公式推导

### 关键模块：SpatialPrompt 提示策略

本文的核心贡献并非模型架构的改动，而是一种**零样本提示策略 SpatialPrompt**。该方法通过显式引导 VLM 在推理过程中识别并利用场景中的参考物体（reference objects）作为视觉锚点，激发模型隐藏的定量空间推理能力。SpatialPrompt 提供两种变体：

- **SpatialPrompt-Single**：紧凑的单步版本，受零样本思维链（Zero-shot CoT）启发，力求简洁易记。
- **SpatialPrompt-Steps**：详细分解版，将问题解决过程拆解为多个明确步骤，包括识别参考物体、利用常识推理估计其标准尺寸、通过与参考物体的相对比较推算目标距离或尺寸。

提示模板的核心指令变化体现在：基线提示（Standard prompt）直接要求模型输出距离数值，或仅进行一般性逐步推理（Zero-shot CoT），均未提及参考物体；而 SpatialPrompt 则在提示中显式插入“识别参考物体—常识推理标准尺寸—相对比较推算”的推理路径（见 Figure 8, Section 5.1）。

### 关键公式

#### 1. 评估指标：最大比值误差

定量空间推理的评估采用预测距离与真实距离的最大比值：

$$\delta = \max\left(\frac{\hat{d}}{d^{*}}, \frac{d^{*}}{\hat{d}}\right)$$

其中：
- $\hat{d}$ 为模型估计的距离值
- $d^{*}$ 为真实距离（ground truth）

成功阈值定义为 $\delta \leq 2$，即估计值在真实值的 0.5 倍至 2 倍之间。更严格的阈值 $\delta \leq 1.25$ 在附录中报告，用于精细区分高精度估计能力（见 Section 3.3, Table 10）。

#### 2. 统计验证：逻辑回归模型

为验证参考物体使用的因果效应，构建逻辑回归模型预测估计值满足 $\delta \leq 2$ 的概率：

$$p(\delta_{\leq 2}) \sim \beta_{0} + \beta_{r} X_{r} + \beta_{d} X_{d} + \beta_{g} X_{g}$$

其中：
- $X_{r}$ 为二值变量，表示响应是否使用了参考物体
- $X_{d}$ 为数据集分割（Q-Spatial++ 或 Q-Spatial-ScanNet）
- $X_{g}$ 为真实距离（cm）
- $\beta_{r}$ 为参考物体使用的系数，估计值为 $\beta_{r} = 1.0179$（$p < 0.05$），表明使用参考物体使准确估计的几率提高约 $e^{1.0179} \approx 2.7$ 倍，且该效应独立于数据集和真实距离大小（见 Table 5, Section 4.2）。

### 关键证据强度

- **参考物体使用的因果效应**：逻辑回归控制数据集和真实距离后，$X_{r}$ 仍是显著预测因子（$p < 0.05$），而真实距离 $X_{g}$ 本身不显著，表明参考物体的使用是独立于距离大小的稳健提升因素（置信度 0.95）。
- **SpatialPrompt 的触发效果**：SpatialPrompt 使 Gemini 1.5 Pro 的参考物体使用频率从 7.64% 飙升至 99.17%，GPT-4V 从 18.12% 升至 99.8%（Q-Spatial-ScanNet），成功率随之大幅提升（置信度 0.95，见 Table 11）。
- **相关性验证**：在所有 VLM 和提示技术中，参考对象使用频率与成功率之间的 Spearman 相关系数在 Q-Spatial-ScanNet 上为 0.69，在 Q-Spatial++ 上高达 0.91，强有力地支持了“通过参考物体推理直接提升准确性”的核心假设（置信度 0.95，见 Figure 4）。

## 实验与分析

### 核心瓶颈与关键发现

当前视觉语言模型（VLM）在缺乏外部工具和额外训练的情况下，从单张2D图像估计物体精确距离和尺寸的定量空间推理能力严重不足。实验揭示的核心瓶颈在于：**水平距离问题几乎使所有模型失效**——GPT-4o在水平距离类别上的δ≤2成功率仅为49.44%，GPT-4V仅10%，Gemini 1.5 Flash仅13.33%（Table 3）。相比之下，人类在Q-Spatial Bench上的平均成功率达90（Table 12），表明该任务对人类简单但对VLM极具挑战。

![[assets/figures/papers/paper_list_l24_https_arxiv_org_abs_2409_09788/figures/005_Table_3.jpg]]
*Table 3: Success rate $\delta _ { \leq 2 }$ breakdown by question categories. Among five question categories, measuring the distance between two objects is more challenging for SoTA VLMs, particularly when measuring horizontal distances. ∗Gemini 1.5 Pro consistently refuses to provide the measurements

关键突破来自对GPT-4o推理行为的观察：**模型在正确回答时会自然涌现利用参考物体的推理路径**。定量分析表明，GPT-4o在响应中使用参考物体时，δ≤2成功率达到83%（45/54），而不使用时仅为64%（114/177），提升19个百分点（Table 4）。逻辑回归进一步确认，使用参考物体使准确估计的几率提高约2.7倍（β_r=1.0179，p<0.05），且该效应独立于数据集和真实距离大小（Table 5）。

![[assets/figures/papers/paper_list_l24_https_arxiv_org_abs_2409_09788/figures/006_Table_5.jpg]]
*Table 5: Logistic regression to analyze the effectiveness of GPT-4o. ∗ denotes a p-value \< 0.05. Using a reference object in reasoning increases the likelihood of generating a response with relative error δ less than 2, statistically significantly*

![[assets/figures/papers/paper_list_l24_https_arxiv_org_abs_2409_09788/figures/007_Table_4.jpg]]
*Table 4: Contingency table of whether GPT-4o’s responses use any reference objects as guidance and the success rate of the responses. GPT-4o used a reference object in 23.4% of instances. However, for the 54 questions where a reference object was used, the success rate $\delta _ { \leq 2 }$ is 83% (45/54), compared to 64% (114/177) when no reference object was used

### SpatialPrompt主实验结果

基于上述发现，作者提出零样本提示技术**SpatialPrompt**，显式引导VLM识别场景中的参考物体并利用其进行相对比较推理。SpatialPrompt提供两种变体：紧凑的单步版（SpatialPrompt-Single）和包含详细分解步骤的版（SpatialPrompt-Steps）。

**Table 6和Table 8**展示了主要结果。SpatialPrompt在所有商业VLM上一致提升定量空间推理成功率：

![[assets/figures/papers/paper_list_l24_https_arxiv_org_abs_2409_09788/figures/009_Table_6.jpg]]
*Table 6: Success rate $\delta _ { \leq 2 }$ of different VLMs and prompting techniques. The proposed prompt SpatialPrompt consistently leads to higher success rates across different VLMs. We bold font the best numbers across different prompting techniques and highlight their performances as compared to the performances of the standard prompt

![[assets/figures/papers/paper_list_l24_https_arxiv_org_abs_2409_09788/figures/013_Table_8.jpg]]
*Table 8: Full table of the success rate $\delta _ { \leq 2 }$ of Gemini 1.5 Pro, Gemini 1.5 Flash, GPT-4V, and GPT-4o. All numbers are averaged over 5 different runs, except for GPT-4V and GPT-4o, which are run on three seeds. Each number is followed by their standard deviations. Table 9: Full table of the success rate $\delta _ { < 2 }$ of LLaVA at different versions and model sizes. All numbers are averaged over 5 different runs and followed by their standard deviations

- **Gemini 1.5 Pro**：在Q-Spatial-ScanNet上从Standard prompt的0.59飙升至SpatialPrompt-Steps的53.65（+53.06点）；在Q-Spatial++上从0.99提升至43.17（+42.18点）。
- **GPT-4V**：在Q-Spatial++上从Standard prompt的18.81提升至SpatialPrompt-Single的53.47（+34.66点）；在Q-Spatial-ScanNet上从25.88提升至52.94（+27.06点）。
- **GPT-4o**：在Q-Spatial-ScanNet上从69.41提升至71.96（+2.55点，SpatialPrompt-Single）；在Q-Spatial++上从61.06提升至62.71（+1.65点）。GPT-4o的基线已较高，提升幅度较小但仍正向。
- **Gemini 1.5 Flash**：在Q-Spatial-ScanNet上从22.94提升至44.71（+21.77点，SpatialPrompt-Single）。

值得注意的是，**不同模型对SpatialPrompt变体的敏感度存在显著差异**：GPT-4V和GPT-4o在详细步骤提示（SpatialPrompt-Steps）下性能反而下降（GPT-4V在Q-Spatial-ScanNet上降至45.29，GPT-4o降至66.24），而Gemini 1.5 Pro则需要详细步骤才能有效响应（SpatialPrompt-Single在Q-Spatial-ScanNet上仅5.29，SpatialPrompt-Steps达53.65）。这一现象揭示了提示格式与模型架构之间的复杂交互。

### 参考对象使用频率与成功率的强相关性

**Figure 4**揭示了核心机制：在所有VLM和提示技术中，参考对象使用频率与成功率之间存在强正相关——Q-Spatial-ScanNet上Spearman相关系数为0.69，Q-Spatial++上高达0.91。这一结果直接验证了核心假设：通过参考物体进行推理可直接提升定量空间问题的整体准确性。

**Table 11**进一步量化了SpatialPrompt对参考对象使用频率的驱动效应：
- Gemini 1.5 Pro在Q-Spatial-ScanNet上的参考对象使用频率从Standard prompt的7.64%飙升至SpatialPrompt-Steps的99.17%；
- GPT-4V从18.12%升至99.8%（SpatialPrompt-Single）；
- GPT-4o从23.4%升至约90%以上。

这表明SpatialPrompt成功将GPT-4o自然涌现的推理模式显式注入到其他VLM中，大幅提升了它们的参考对象使用率，从而带来成功率的大幅跃升。

### 开源模型表现与消融分析

**LLaVA系列**（Table 7, Table 9）展现了有趣的分化：LLaVA v1.6-34b在Q-Spatial-ScanNet上以Standard prompt达到60.59的δ≤2成功率，超越除GPT-4o外的所有商业VLM；但在Q-Spatial++上骤降至36.62（下降超过20点）。这一显著差异暗示Q-Spatial-ScanNet的ScanNet来源可能存在训练数据泄漏风险，而Q-Spatial++作为全新拍摄的图像更能反映真实泛化能力。

![[assets/figures/papers/paper_list_l24_https_arxiv_org_abs_2409_09788/figures/011_Table_7.jpg]]
*Table 7: Success rate $\delta _ { \leq 2 }$ of LLaVA in $\mathbf { Q } \mathbf { - }$ Spatial-ScanNet and Q-Spatial++

**Zero-shot CoT的负面效应**值得关注：在LLaVA v1.6-34b上，Zero-shot CoT在Q-Spatial-ScanNet上从60.59降至40.00（Table 7），表明不加引导的思维链可能引入噪声推理步骤，反而损害定量空间判断。SpatialPrompt通过明确指定推理路径（识别参考物→估计标准尺寸→相对比较），避免了这一陷阱。

### 失败模式分析

**Figure 13**揭示了GPT-4o的常见失败案例，结合分析可归纳为以下模式：

1. **参考物选择错误**：GPT-4o有时会错误地使用地板瓷砖等不准确或尺寸未知的参照物，导致估计偏差。这表明模型缺乏自主筛选可靠参考物的能力。

2. **常识知识不足**：当场景缺乏明确参考物体，或模型对参考物的标准尺寸缺乏常识性知识时，SpatialPrompt的改进有限。这在Q-Spatial++的某些稀疏场景中尤为明显。

3. **水平距离的固有困难**：即使使用SpatialPrompt，水平距离仍是最具挑战的类别。这源于单张2D图像中深度信息的固有模糊性——水平距离的估计需要更强的3D空间推理能力。

4. **提示敏感性差异**：如前所述，SpatialPrompt-Steps在GPT系列模型上反而降低性能，可能原因是过长的详细指令干扰了GPT模型已有的内部推理链，或引入了与模型预训练分布不匹配的格式约束。

### 更严格指标下的表现

**Table 10**报告了δ≤1.25（允许0.8×至1.25×误差）更严格阈值下的结果。所有模型的成功率均大幅下降，标准偏差增大，但SpatialPrompt仍保持相对优势。例如，Gemini 1.5 Pro在Q-Spatial-ScanNet上从0.00（Standard）提升至15.29（SpatialPrompt-Steps）。这表明SpatialPrompt在更高精度要求下仍有效，但距离实际应用仍有巨大提升空间。

![[assets/figures/papers/paper_list_l24_https_arxiv_org_abs_2409_09788/figures/015_Table_10.jpg]]
*Table 10: Full table of the success rate $\delta _ { \leq 1 . 2 5 }$ of Gemini 1.5 Pro, Gemini 1.5 Flash, GPT-4V, and GPT-4o. All numbers are averaged over 5 different runs, except for GPT-4V and GPT-4o, which are run on three seeds. Each number is followed by their standard deviations. Table 11: Frequency of whether the responses involve using reference objects of different VLMs and prompting techniques. The proposed prompt SpatialPrompt consistently lead to higher chances to have reference objects involved in the responses

### 实验公平性说明

实验采用确定性采样，Gemini和LLaVA使用5个随机种子，GPT-4V和GPT-4o使用3个种子（API成本考虑）。GPT系列模型即使在temperature=0时仍存在轻微随机性，结果报告了标准偏差。Q-Spatial-ScanNet基于公开数据集ScanNet，存在训练数据泄漏的潜在风险；Q-Spatial++使用全新拍摄图像，专门评估泛化能力。人类基线（Table 12）显示人类平均成功率达90，GPT-4o最佳仅约65，差距超过30点，表明该基准仍有巨大提升空间。

### 补充图表

![[assets/figures/papers/paper_list_l24_https_arxiv_org_abs_2409_09788/figures/001_Figure_1.jpg]]
*Figure 1: We introduce a human expert-annotated benchmark dedicated to quantitative spatial reasoning: Q-Spatial Bench. The benchmark consists of two splits: Q-Spatial-ScanNet and Q-Spatial++. The left panel shows the examples from the two splits. Q-Spatial-ScanNet is repurposed from a subset of images and RGB-D scans in ScanNet (Dai et al., 2017) and the questions are categorized into five categories (top-right). To provide a more robust evaluation in quantitative spatial reasoning, we captured an additional set of images and provide accurately-annotated quantitative spatial questions for Q-Spatial++*

![[assets/figures/papers/paper_list_l24_https_arxiv_org_abs_2409_09788/figures/002_Table_1.jpg]]
*Table 1: Comparison of quantitative spatial reasoning benchmark. Q-Spatial Bench is a human expert-annotated benchmark, specifically designed for quantitative spatial questions*

![[assets/figures/papers/paper_list_l24_https_arxiv_org_abs_2409_09788/figures/003_Table_2.jpg]]
*Table 2: GPT-4o outperforms other commercial VLMs in quantitative spatial reasoning. We evaluates the success rate $\delta _ { \leq 2 }$ on each split of Q-Spatial Bench. ∗Gemini 1.5 Pro consistently refuses to provide the measurements

![[assets/figures/papers/paper_list_l24_https_arxiv_org_abs_2409_09788/figures/012_Table.jpg]]

![[assets/figures/papers/paper_list_l24_https_arxiv_org_abs_2409_09788/figures/014_Table.jpg]]

## 方法谱系与知识库定位

### 核心定位：零样本提示工程驱动隐藏空间推理能力

本研究提出的 **SpatialPrompt** 属于**零样本提示工程**方法，其核心创新在于：通过分析性能最强的GPT-4o在正确回答时自然涌现的“参考物体推理路径”，设计显式引导VLM识别和利用场景中参考物体的文本提示，从而在不增加数据、不修改架构、不进行微调的前提下，大幅提升多种VLM的定量空间推理成功率。

**与基线方法的本质差异**：Standard prompt直接要求模型输出距离数值，Zero-shot CoT（Kojima et al., 2022）鼓励逐步推理但未显式要求使用参考物体。SpatialPrompt的因果干预点在于**提示指令槽**——从“请估计距离”改为“首先识别图像中可作为参考的物体，利用常识推理估计其标准尺寸，再通过与参考物体的相对比较推算目标距离”。这一改变在Gemini 1.5 Pro上使成功率从0.59飙升至53.65（+53.06点，Table 8），在GPT-4V上从18.81提升至53.47（+34.66点，Table 8）。

### 与微调路线的对比：效率与边界的差异

论文明确将SpatialPrompt与微调路线进行对比：**SpatialVLM**（通过2亿QA对微调）在同指标上仅获得不到4个点的相对提升（Introduction部分提及）。这揭示了两种路线的根本差异：

- **SpatialPrompt**：利用模型已有的常识推理能力，通过提示工程将其重新路由到空间推理任务，成本极低，但效果高度依赖模型自身能力阈值。
- **微调路线**：通过大量空间标注数据注入新知识，理论上可突破模型原有能力边界，但数据获取成本高，且在当前VLM上收益有限。

这一对比暗示：当前VLM的瓶颈可能不在于缺乏空间知识，而在于推理时未能有效激活和组合已有知识。SpatialPrompt的成功为此提供了有力证据。

### 适用边界与模型依赖性

SpatialPrompt的效果呈现显著的**模型异质性**：

1. **模型规模阈值**：在LLaVA-7B等较小规模开源模型上，SpatialPrompt无法稳定提升（Table 7, Table 9）。LLaVA v1.6-34b在Q-Spatial-ScanNet上虽表现强劲（标准提示下60.59），但SpatialPrompt的提升有限，且在Q-Spatial++上仍大幅落后商业模型。这暗示存在某种能力阈值，低于该阈值的模型即使被引导也无法有效利用参考物体推理。

2. **提示格式敏感性**：GPT-4V/4o在详细步骤版SpatialPrompt-Steps下性能下降，而Gemini 1.5 Pro则需要详细步骤才能有效响应（Table 8）。这种“提示偏好”的差异目前缺乏理论解释，是重要的开放问题。

3. **常识知识依赖**：SpatialPrompt要求模型能通过常识推断参考物体的标准尺寸（如门约2米高、椅子约45厘米高）。当场景缺乏明确参考物或模型常识知识不足时，改进有限。GPT-4o甚至会错误地使用地板瓷砖等不准确参照物，导致估计偏差（Figure 13）。

### 数据集泛化与泄漏风险

Q-Spatial Bench的两个分割揭示了关键的泛化问题：

- **Q-Spatial-ScanNet**（基于公开ScanNet数据集）：LLaVA v1.6-34b在此分割上表现异常强劲（60.59，超过多数商业VLM），但在全新拍摄的Q-Spatial++上骤降超过20点（Table 7, Table 9）。这强烈暗示ScanNet数据可能已被部分模型训练集包含，存在**训练数据泄漏**风险。
- **Q-Spatial++**（全新拍摄，101题，仅水平距离）：作为更严格的泛化测试，所有模型在此分割上表现均显著下降。GPT-4o从Q-Spatial-ScanNet的69.41降至61.06（Table 2），说明即使在最佳模型上，对未见场景的定量空间推理仍具挑战。

### 评估指标的局限

主要指标 $\delta_{\leq 2}$（允许0.5×到2×误差）较为宽松。更严格的 $\delta_{\leq 1.25}$ 结果（Table 10）显示标准偏差增大，但SpatialPrompt仍具优势。人类在Q-Spatial Bench上的平均成功率为90，而GPT-4o最好成绩仅约65（Table 12），差距超过30点，表明该基准对人类简单但对VLM极具挑战，仍有巨大提升空间。

### 开放问题与未来方向

1. **跨任务泛化**：SpatialPrompt能否推广到其他视觉空间任务（物体尺寸、面积、角度估计）或不同领域，尚未验证。

2. **提示格式异质性的机制解释**：为什么详细步骤提示对GPT-4V/4o有负面影响，而对Gemini系列有正面影响？这涉及不同VLM的指令遵循机制和推理链长度偏好，需要更深入的分析。

3. **参考物体自动选择**：当前SpatialPrompt依赖模型自主选择参考物，但GPT-4o有时会选择地板瓷砖等易导致错误的参照物。如何自动识别和筛选最优参考物体，是提升鲁棒性的关键。

4. **与微调的协同**：SpatialPrompt与SpatialVLM等微调方法是否可取得叠加收益，尚待探索。

5. **真实应用验证**：研究仅限单张2D图像，未涉及多视角或深度传感器信息。SpatialPrompt在机器人操控、AR等真实应用中的实用性需要进一步验证。

## 原文 PDF

![[paperPDFs/EMNLP_2025/Reasoning_Paths_with_Reference_Objects_Elicit_Quantitative_Spatial_Reasoning_in_Large_Vision_Language_Models.pdf]]
