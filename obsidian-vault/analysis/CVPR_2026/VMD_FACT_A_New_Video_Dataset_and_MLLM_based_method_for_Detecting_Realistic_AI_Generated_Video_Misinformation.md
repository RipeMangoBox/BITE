---
title: "VMD-FACT: A New Video Dataset and MLLM-based method for Detecting Realistic AI-Generated Video Misinformation"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/VMD_FACT_A_New_Video_Dataset_and_MLLM_based_method_for_Detecting_Realistic_AI_Generated_Video_Misinformation.pdf
project_link: "https://gitee.com/VR_NAVE/ravm"
code_link: null
aliases:
- IIEEGM
- VMD-FACT
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/benchmarks_datasets_evaluation
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: 通过引入意图极性引导的声明篡改、多智能体迭代反馈优化视频生成、自适应关键帧到视频伪造模块，以及构建内部-外部证据图（IEEG）来显式建模多模态证据和事实核查结果之间的依赖关系，是提升检测性能的关键操作杠杆。
primary_logic: 将多模态证据和事实核查推理过程表示为有向无环图（IEEG），可以提供可解释的、鲁棒的虚假信息检测；同时，利用多智能体迭代反馈生成逼真的 AI 生成视频虚假信息，能够暴露现有 MLLM 的弱点，并推动更具挑战性的数据集和检测方法的进步。
claims:
- IEEG 在 RAVM 上达到 75.99% 的准确率和 73.44% 的宏 F1，显著优于所有对比方法。
- 在 RAVM 子集上微调后，IEEG 在 FakeTT 上的准确率从 41.61% 提升至 78.26%，提升了 36.65%。
- 现有 MLLM 在 RAVM 上表现有限，最好的闭源模型 Gemini 2.5 仅取得 68.89% 的准确率。
- RAVM 上 Accuracy = 75.99% (IEEG)
---

# VMD-FACT: A New Video Dataset and MLLM-based method for Detecting Realistic AI-Generated Video Misinformation

> [!tip] 核心洞察
> 将多模态证据和事实核查推理过程表示为有向无环图（IEEG），可以提供可解释的、鲁棒的虚假信息检测；同时，利用多智能体迭代反馈生成逼真的 AI 生成视频虚假信息，能够暴露现有 MLLM 的弱点，并推动更具挑战性的数据集和检测方法的进步。

| 字段 | 内容 |
|------|------|
| 中文题名 | VMD-FACT：一个面向真实 AI 生成视频虚假信息检测的新数据集与基于 MLLM 的方法 |
| 英文题名 | VMD-FACT: A New Video Dataset and MLLM-based method for Detecting Realistic AI-Generated Video Misinformation |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://openaccess.thecvf.com/content/CVPR2026/html/Zhang_VMD-FACT_A_New_Video_Dataset_and_MLLM-based_method_for_Detecting_CVPR_2026_paper.html) · [Project](https://gitee.com/VR_NAVE/ravm) |
| Topic | #topic/vision_multimodal_applications #topic/benchmarks_datasets_evaluation #topic/vision_multimodal_applications/image_and_video_generation |
| Method | IEEG (Internal-External Evidence Graph Modeling) |
| Dataset | RAVM, FakeTT, FakeSV |

> [!tip] 效果简介
> - RAVM 上，Accuracy 75.99% (IEEG) vs 68.89% (Gemini 2.5) (+7.10%)。
> - FakeTT (robustness) 上，Accuracy 78.26% (IEEG fine-tuned on RAVM*) vs 41.61% (IEEG not fine-tuned) (+36.65%)。
> - FakeSV (robustness) 上，Accuracy 70.18% (IEEG fine-tuned on RAVM*) vs 56.70% (IEEG not fine-tuned) (+13.48%)。

## 概述

**问题瓶颈**：现有视频虚假信息检测数据集主要依赖编辑技术（如拼接、换脸），这些操作破坏了跨模态一致性，产生易于检测的非真实伪影。然而，实际由 AI 生成的虚假视频具有高度跨模态一致性和逼真度，导致现有模型难以有效检测。此外，当前多模态大模型（MLLM）缺乏对多模态证据间复杂依赖关系的显式建模，推理链容易累积错误，性能显著下降。

**核心洞察与操作杠杆**：本文的核心洞察在于，将多模态证据与事实核查推理过程表示为有向无环图（Internal-External Evidence Graph, IEEG），可以提供可解释且鲁棒的虚假信息检测。操作杠杆体现在三个层面：引入意图极性引导的声明篡改、多智能体迭代反馈优化视频生成、自适应关键帧到视频伪造模块，从而生成逼真的 AI 虚假视频；同时，通过 IEEG 显式建模多模态证据与事实核查结果之间的依赖关系，提升检测性能。

**方法定位**：本文提出 **IEEG**（Internal-External Evidence Graph Modeling），一种基于证据图建模的推理方法。与 **FakingRecipe**（Bu et al., ACM MM 2024）基于创作过程的方法和 **Fact-R1**（Zhang et al., arXiv 2025）基于深度推理的方法不同，IEEG 将多模态证据和事实核查结果显式建模为有向无环图，通过知识蒸馏损失最大化推理路径概率，支持可解释的检测。同时，本文构建了 **RAVM** 数据集，包含 9,049 个声明-视频对（4,355 真实 / 4,694 虚假），覆盖声明、视频、音频和跨模态四类操纵来源。

**主要结果**：在 RAVM 上，IEEG 达到 **75.99%** 的准确率和 **73.44%** 的宏 F1，显著优于最佳闭源模型 Gemini 2.5（68.89%），提升 7.10 个百分点。在跨数据集鲁棒性评估中，经 RAVM 子集微调后，IEEG 在 FakeTT 上的准确率从 41.61% 跃升至 **78.26%**（+36.65%），在 FakeSV 上从 56.70% 提升至 **70.18%**（+13.48%），证明了所提数据集对检测模型鲁棒性的显著增强作用。

## 背景与动机

### 问题背景：AI 生成视频虚假信息的检测困境

随着文本到视频（T2V）扩散模型（如 Sora、Jimeng）的快速成熟，AI 生成的视频在视觉真实性和语义一致性上已达到前所未有的水平。这一技术进步在赋能内容创作的同时，也催生了新型的虚假信息传播范式：恶意行为者可以利用生成模型构造高度逼真的视频，配合篡改的文本声明，形成多模态虚假信息。这类虚假信息不仅在视觉上难以辨别真伪，更重要的是，其视频内容与声明之间往往保持高度跨模态一致性——这与传统基于编辑技术（如拼接、重编码、局部修改）产生的虚假视频存在本质区别。

### 现有方法的缺口：数据集与检测模型的双重滞后

**数据集的局限性。** 现有视频虚假信息检测数据集（如 FakeSV、FakeTT、FMNV）主要依赖编辑技术构造虚假样本。这些操作会在视频中引入可检测的伪影（如重编码痕迹、不自然的边界过渡），破坏了跨模态一致性，使得虚假样本具有“非真实”的特征。然而，真实场景中由 AI 生成的虚假视频恰恰相反：它们天然具备高度跨模态一致性和视觉真实性，导致在此类数据集上训练的检测器难以泛化到 AI 生成场景。此外，现有数据集在操纵维度上覆盖不全——多数仅涉及单一的声明篡改或视频编辑，缺乏对声明、视频、音频及跨模态协同篡改的系统性建模。

**MLLM 推理能力的不足。** 多模态大模型（MLLM）在虚假信息检测中展现出一定潜力，但现有方法存在两个关键瓶颈：其一，多数 MLLM 采用链式思维（Chain-of-Thought, CoT）或隐式跨模态融合进行推理，缺乏对多模态证据之间复杂依赖关系的显式建模，导致推理链容易累积错误；其二，MLLM 的输出通常仅为分类标签，缺乏可解释的推理过程，难以满足事实核查场景对可解释性的刚性需求。实验表明，当前最强的闭源 MLLM **Gemini 2.5** 在 RAVM 数据集上仅取得 68.89% 的准确率，揭示了现有模型在真实 AI 生成虚假信息检测上的显著性能缺口。

### 本文动机：从数据构造到推理建模的系统性突破

针对上述双重滞后，本文的动机聚焦于两个核心问题：

1. **如何构造真正具有挑战性的 AI 生成视频虚假信息数据集？** 这要求生成框架能够模拟真实恶意行为者的操纵策略，在保持高度跨模态一致性的前提下，实现意图极性引导的声明篡改与视频生成，从而暴露现有检测器的本质弱点。

2. **如何设计可解释且鲁棒的检测方法？** 这需要突破现有 MLLM 的隐式推理范式，显式建模多模态证据与事实核查结论之间的依赖关系，使推理过程可追溯、可验证，同时提升检测性能与跨数据集泛化能力。

基于以上动机，本文提出了 **RAVM 数据集**（一个包含 9,049 对声明-视频样本的真实 AI 生成视频虚假信息数据集）和 **IEEG 模型**（内部-外部证据图建模方法），分别从数据构造和检测方法两个维度推动该领域的研究进展。

## 核心创新

VMD-FACT 的核心创新围绕两个紧密耦合的维度展开：**数据层面的逼真 AI 生成视频虚假信息构建**与**模型层面的可解释多模态证据推理**。二者共同指向一个核心瓶颈——现有数据集依赖编辑技术，破坏了跨模态一致性，产生易于检测的非真实伪影；而现有 MLLM 缺乏对多模态证据间复杂依赖关系的显式建模，推理链容易累积错误。

### 数据层面：意图极性引导的多智能体迭代生成框架

与现有数据集（如 FakeSV、FakeTT、FakeAVCeleb）仅对单模态进行编辑或替换不同，VMD-FACT 提出了一个**意图极性引导的声明篡改机制**。该机制通过替换（主体、时间、地点）、重写（叙事逻辑、情感触发）和生成三类技术，在保持语义连贯性的前提下产生误导性声明，并由声明篡改器 $\mathbf{G}_c$ 根据真实声明 $c_a$、元数据 $m_a$ 和引导提示 $\mathbf{P}_c$ 生成篡改声明与描述：

$$c_f, d_f = \mathbf{G}_c(c_a, m_a, \mathbf{P}_c)$$

在此基础上，**智能体混合反馈视频优化模块**采用多智能体范式，通过**趋势感知惩罚项** $\mathcal{H}^{(t)}$ 对相邻迭代的质量和对齐分数变化进行动态约束，使优化过程稳定可控。总奖励 $\mathcal{R}^{(t)} = \mathcal{R}_{base}^{(t)} - \delta \mathcal{H}^{(t)}$ 综合了质量、语义对齐和对抗性评分，优化器 $\Gamma$ 根据反馈迭代调整操纵提示，间接优化生成视频。这一设计使得生成的虚假视频具有**高度跨模态一致性和真实性**，从而暴露现有 MLLM 的检测弱点。

### 模型层面：内部-外部证据图（IEEG）建模

检测方法的关键 changed slot 在于**推理机制的范式转变**。基线方法（如 **FakingRecipe** (Bu et al., ACM MM 2024)、**Fact-R1** (Zhang et al., arXiv 2025)）采用 Chain-of-Thought 或隐式跨模态融合，而 IEEG 将多模态证据与事实核查结果显式建模为**有向无环依赖图**，使推理过程可追溯、可解释。

训练目标从标准分类交叉熵损失转变为**知识蒸馏损失**，最大化给定声明 $c$ 和视频 $v$ 时推理路径 $r$ 的条件概率：

$$\mathcal{L} = \mu \mathbb{E}_{c,v \sim \Omega, r \sim \mathcal{D}} [-\log P(r \mid c, v, \mathbf{I})]$$

推理时通过 $r^* = \arg\max_r P(r \mid c, v)$ 选择最优推理路径，输出包含事实核查步骤的证据图，而非仅给出二分类标签。这一设计使 IEEG 在 RAVM 上达到 75.99% 的准确率，显著优于最强闭源模型 **Gemini 2.5** 的 68.89%（+7.10%），验证了显式证据依赖建模对检测性能的因果性提升。

### 创新总结

| 维度 | 基线做法 | VMD-FACT 创新 | 证据锚点 |
|------|----------|---------------|----------|
| 数据生成 | 编辑拼接，产生非真实伪影 | 意图极性引导 + 多智能体迭代反馈 + 趋势感知惩罚 | Equation (1)-(8) |
| 推理机制 | CoT 或隐式跨模态融合 | 显式 IEEG 有向无环图，建模证据间依赖 | Section 3.2 |
| 训练目标 | 标准交叉熵 | 知识蒸馏，最大化推理路径概率 | Equation (11) |
| 可解释性 | 无或仅输出类别 | 输出包含事实核查步骤的证据图 | Section 3.2 |

> **注意**：IEEG 目前仅支持二分类（真实/虚假），尚未覆盖更细粒度的虚假信息类别（如误导意图分类、操纵技术分类），这是方法层面的一个显式局限。

## 整体框架

VMD‑FACT 的整体框架由两条深度耦合的流水线构成：**真实 AI 生成视频虚假信息构建流水线**与**可解释虚假信息检测流水线**。前者以意图极性引导的声明篡改为起点，通过多智能体迭代反馈的视频生成与自适应关键帧‑视频伪造模块，系统性地产生高度逼真且跨模态一致的虚假视频；后者则将这些多模态证据建模为内部‑外部证据图（IEEG），并通过知识蒸馏最大化推理路径的条件概率，实现可解释的事实核查。

### 生成流水线：从意图极性到跨模态一致伪造

生成流水线的核心设计目标是**消除传统编辑式伪造中易被检测的跨模态不一致伪影**，同时保持语义层面的误导性。其运作遵循“意图注入—多智能体优化—自适应伪造—音频叠加”的闭环：

1. **意图极性引导的声明篡改**  
   给定一条真实声明 $c_a$ 及其元数据 $m_a$，声明篡改器 $\mathbf{G}_c$ 在意图极性提示 $\mathbf{P}_c$ 的引导下，通过替换（主体、时间、地点）、重写（叙事逻辑、情感触发）与生成三种技术，产出篡改后的声明 $c_f$ 及描述 $d_f$：
   $$c_f, d_f = \mathbf{G}_c(c_a, m_a, \mathbf{P}_c) \tag{1}$$
   这一步骤确保伪造声明在语义上与原始事实相悖，但表面逻辑自洽。

2. **语义对齐的操纵提示生成**  
   提示生成器 $\mathbf{G}_p$ 将篡改声明 $c_f$、描述 $d_f$ 与叙事模板 $\mathbf{T}$ 融合，生成初始操纵提示 $\mathbf{P}^{(0)}$，作为后续视频生成的语义锚点：
   $$\mathbf{P}^{(0)} = \mathbf{G}_p(c_f, d_f, \mathbf{T}, \mathbf{P}_p) \tag{2}$$

3. **多智能体混合反馈视频精炼**  
   这是整个生成流水线的**因果杠杆**所在。在文本‑视频生成范式下，多个智能体协同工作：质量评估器 $\mathbf{E}_q$ 与对齐评估器 $\mathbf{E}_a$ 分别给出当前视频 $v^{(t)}$ 的质量分数 $s_q^{(t)}$ 与对齐分数 $s_a^{(t)}$，对抗评估器 $\mathbf{E}_{adv}$ 则判断该声明‑视频对是否具有误导性（fake 为 0，true 为 1）。三者共同构成基础奖励 $\mathcal{R}_{base}^{(t)}$：
   $$\mathcal{R}_{base}^{(t)} = w_q \frac{s_q^{(t)}}{N_q} + w_a \frac{s_a^{(t)}}{N_a} + w_{adv} s_{adv}^{(t)} \tag{5}$$
   为进一步稳定优化过程，引入**趋势感知惩罚项** $\mathcal{H}^{(t)}$，根据相邻迭代的质量与对齐分数变化趋势施加约束：
   $$\mathcal{H}^{(t)} = \begin{cases} 0, & \text{if } t=0, \\ \alpha \max(0, \Delta_q^{(t)}) + \beta \max(0, \Delta_a^{(t)}), & \text{otherwise}. \end{cases} \tag{6}$$
   总奖励 $\mathcal{R}^{(t)} = \mathcal{R}_{base}^{(t)} - \delta \mathcal{H}^{(t)}$ 驱动优化器 $\Gamma$ 迭代调整操纵提示 $\mathbf{P}^{(t+1)}$，从而间接精炼视频生成，直至产出语义高度对齐且难以检测的伪造视频。

4. **自适应关键帧‑视频伪造与音频叠加**  
   对于需要更细粒度操控的场景，关键帧编辑模块通过感知器与执行器的组合操作，迭代编辑关键帧 $\mathbf{K}^{(l)}$：
   $$\mathbf{K}^{(l)} = \big[ f_{per}(\mathbf{K}) \circ f_{act}(\mathbf{K}, \mathbf{P}_e) \big]^{(l)} \tag{9}$$
   最终，在生成的操纵视频 $v^*$ 上叠加背景音乐与语音，增强多模态一致性：
   $$\tilde{v^*} = v^* \oplus \sigma_m \pi_{music} \oplus \sigma_s \pi_{speech} \tag{10}$$

### 检测流水线：IEEG 建模与知识蒸馏

检测端的核心创新在于将多模态证据与事实核查推理过程显式建模为**有向无环的证据图**。给定声明 $c$ 与视频 $v$，IEEG 将内部证据（视频帧、音频信号、文本语义）与外部证据（知识库检索结果、元数据）及其依赖关系组织为图结构 $\mathbf{I}$，并通过知识蒸馏损失最大化推理路径 $r$ 的条件概率：
$$\mathcal{L} = \mu \mathbb{E}_{c,v \sim \Omega, r \sim \mathcal{D}} [-\log P(r \mid c, v, \mathbf{I})] \tag{11}$$
推理阶段，模型选择使条件概率最大化的最优路径 $r^*$ 作为事实核查结果：
$$r^* = \arg\max_r P(r \mid c, v) \tag{12}$$
这一设计使得检测过程天然具备可解释性——输出的不仅是二分类标签，还包括完整的证据推理链。

### 输入输出流与模块耦合

两条流水线通过**RAVM 数据集**形成闭环耦合：生成流水线产出 9,049 个声明‑视频对（4,355 真实 / 4,694 虚假），覆盖声明、视频、音频与跨模态四类操纵源（见 Figure 1）；检测流水线在该数据集上训练与评估，其性能反馈又间接验证了生成流水线的挑战性。整体框架的模块关系可概括为：**意图注入 → 多智能体优化视频生成 → 关键帧伪造 → 音频叠加 → 多模态证据图推理 → 可解释检测结果**，其中多智能体反馈精炼模块与 IEEG 证据图建模分别是生成端与检测端的核心操作杠杆。

![[assets/figures/papers/paper_list_l2755_https_openaccess_thecvf_com_content_CVPR2026_html_Zhang_VMD_FACT_A_New_V/figures/001_Figure_1.jpg]]
*Figure 1: Overview of manipulation sources in the proposed RAVM dataset. The dataset contains four manipulation sources: claim, video, audio, and cross-modal, each comprising multiple manipulation techniques*

### 补充图表

![[assets/figures/papers/paper_list_l2755_https_openaccess_thecvf_com_content_CVPR2026_html_Zhang_VMD_FACT_A_New_V/figures/003_Figure_2.jpg]]
*Figure 2: Overview of our multi-agent-driven framework for generating realistic AI-generated video misinformation. The framework iteratively manipulates claims, videos, and audio while considering intent polarity, producing realistic claim–video pairs. Commercial closed-source models are incorporated to further enhance the diversity of RAVM*

## 核心模块与公式推导

### 1. 意图极性引导的声明篡改

RAVM 数据集的构建始于对真实声明的系统性篡改。给定一条真实声明 $c_a$ 及其元数据 $m_a$，声明篡改器 $\mathbf{G}_c$ 根据引导提示 $\mathbf{P}_c$ 生成篡改后的声明 $c_f$ 及其描述 $d_f$：

$$c _ { f } , d _ { f } = { \bf G } _ { c } ( c _ { a } , m _ { a } , { \bf P } _ { c } )$$

篡改技术涵盖三类操作：**替换**（如主体、时间、地点）、**改写**（如叙事逻辑、情感触发）和**生成**（从头构造虚假声明）。这一模块的核心在于引入意图极性（intention polarity）作为约束，确保生成的虚假声明具有明确且可控的误导方向，而非随机扰动。

### 2. 多智能体迭代反馈视频生成

声明篡改完成后，框架通过多智能体协作生成与之语义对齐的虚假视频。首先生成初始操纵提示：

$$\mathbf { P } ^ { ( 0 ) } = \mathbf { G } _ { p } ( c _ { f } , d _ { f } , \mathbf { T } , \mathbf { P } _ { p } )$$

其中 $\mathbf{G}_p$ 为提示生成器，$\mathbf{T}$ 为叙事模板，$\mathbf{P}_p$ 为引导提示。随后进入迭代优化循环，每轮迭代 $t$ 包含三个核心评估器：

- **质量评估器** $\mathbf{E}_q$：输出质量分数 $s_q^{(t)}$ 及理由 $r_q^{(t)}$
- **对齐评估器** $\mathbf{E}_a$：输出声明-视频对齐分数 $s_a^{(t)}$ 及理由 $r_a^{(t)}$
- **对抗评估器** $\mathbf{E}_{adv}$：判断声明-视频对是否具有误导性，输出对抗分数 $s_{adv}^{(t)} \in \{0, 1\}$，其中 $0$ 表示 fake（具有误导性），$1$ 表示 true（不具备误导性）

$$s _ { q } ^ { ( t ) } , r _ { q } ^ { ( t ) } = \mathbf { E } _ { q } ( v ^ { ( t ) } ) , \quad s _ { a } ^ { ( t ) } , r _ { a } ^ { ( t ) } = \mathbf { E } _ { a } ( v ^ { ( t ) } , \mathbf { P } ^ { ( t ) } )$$

$$s _ { a d v } ^ { ( t ) } = \left\{ \begin{array} { l l } { 0 , } & { \mathrm { i f } \mathbf { E } _ { a d v } ( v ^ { ( t ) } , \mathbf { P } ^ { ( t ) } ) = \mathbf { f a k e } , } \\ { 1 , } & { \mathrm { i f } \mathbf { E } _ { a d v } ( v ^ { ( t ) } , \mathbf { P } ^ { ( t ) } ) = \mathbf { t r u e } . } \end{array} \right.$$

### 3. 动态奖励与趋势感知惩罚

基础奖励 $\mathcal{R}_{base}^{(t)}$ 将三个评估器的分数加权融合：

$$\mathcal { R } _ { b a s e } ^ { ( t ) } = w _ { q } \frac { s _ { q } ^ { ( t ) } } { N _ { q } } + w _ { a } \frac { s _ { a } ^ { ( t ) } } { N _ { a } } + w _ { a d v } s _ { a d v } ^ { ( t ) }$$

其中 $N_q$、$N_a$ 为归一化因子，$w_q$、$w_a$、$w_{adv}$ 为权重系数。为避免优化过程出现剧烈震荡，引入趋势感知惩罚项 $\mathcal{H}^{(t)}$：

$$\mathcal { H } ^ { ( t ) } = \left\{ { \begin{array} { l l } { 0 , } & { \mathrm { i f ~ } t = 0 , } \\ { \alpha \operatorname* { m a x } \left( 0 , \Delta _ { q } ^ { ( t ) } \right) + \beta \operatorname* { m a x } \left( 0 , \Delta _ { a } ^ { ( t ) } \right) , } & { \mathbf { o t h e r w i s e } . } \end{array} } \right.$$

$\Delta_q^{(t)}$ 和 $\Delta_a^{(t)}$ 分别表示相邻迭代间质量和语义对齐分数的变化趋势。当分数下降时，惩罚项被激活，抑制优化方向的过度偏移。总奖励为：

$$\mathcal { R } ^ { ( t ) } = \mathcal { R } _ { b a s e } ^ { ( t ) } - \delta \mathcal { H } ^ { ( t ) }$$

优化器 $\Gamma$ 根据当前视频、奖励、评估理由和历史记录 $\mathbf{H}$ 调整操纵提示：

$$\mathbf { p } ^ { ( t + 1 ) } = \Gamma \Big ( v ^ { ( t ) } , \mathcal { R } _ { b a s e } ^ { ( t ) } , \mathcal { H } ^ { ( t ) } , r _ { p } ^ { ( t ) } , r _ { a } ^ { ( t ) } , \mathbf { H } , \mathbf { P } _ { o } \Big )$$

### 4. 自适应关键帧到视频伪造

对于需要精细空间操控的场景，框架采用关键帧编辑策略。给定关键帧 $\mathbf{K}$，由感知器 $f_{per}$ 和执行器 $f_{act}$ 组合操作，迭代产生操控后的关键帧：

$$\mathbf { K } ^ { ( l ) } = \big [ f _ { p e r } ( \mathbf { K } ) \circ f _ { a c t } ( \mathbf { K } , \mathbf { P } _ { e } ) \big ] ^ { ( l ) }$$

编辑后的关键帧通过图像到视频生成模型扩展为完整视频片段。

### 5. 语义驱动音频叠加

最终操纵视频 $v^*$ 叠加背景音乐和语音以增强真实感：

$$\tilde { v ^ { * } } = v ^ { * } \oplus \sigma _ { m } \pi _ { m u s i c } \oplus \sigma _ { s } \pi _ { s p e e c h }$$

其中 $\pi_{music}$ 和 $\pi_{speech}$ 分别为背景音乐和语音轨道，$\sigma_m$、$\sigma_s$ 为对应的强度控制系数。

### 6. 内部-外部证据图建模

IEEG 将多模态证据和事实核查推理过程表示为有向无环图。给定声明 $c$ 和视频 $v$，模型通过知识蒸馏学习推理路径 $r$ 的条件概率分布。蒸馏损失函数为：

$$\mathcal { L } = \mu \mathbb { E } _ { c , v \sim \Omega , r \sim \mathcal { D } } [ - \log P ( r \mid c , v , \mathbf { I } ) ]$$

其中 $\mu$ 为温度系数，$\Omega$ 为训练数据分布，$\mathcal{D}$ 为推理路径的监督信号分布，$\mathbf{I}$ 为内部-外部证据图的拓扑结构约束。推理时，模型选择最大化条件概率的最优路径：

$$r ^ { * } = \arg \operatorname* { m a x } _ { r } P ( r \mid c , v )$$

该公式是 IEEG 可解释检测的核心：推理路径 $r^*$ 显式编码了从多模态证据到事实核查结论的因果依赖链，而非隐式的黑箱分类。

## 实验与分析

### 数据集与评估协议

RAVM 数据集共包含 9,049 个声明-视频对，其中 4,355 个标注为真实，4,694 个标注为虚假。训练集包含 6,028 个样本（3,135 假 / 2,893 真），验证集与测试集划分详见 Figure 3。数据集覆盖四种操控来源：声明、视频、音频及跨模态，具体操控技术分布见 Table 1。

![[assets/figures/papers/paper_list_l2755_https_openaccess_thecvf_com_content_CVPR2026_html_Zhang_VMD_FACT_A_New_V/figures/002_Table_1.jpg]]
*Table 1: Comparison of video misinformation detection datasets, divided by manipulated modality: Claim, Video, Audio, and Cross-Modal. ✓indicates the manipulation technique is supported, ✗ indicates it is not supported. ■ indicates that the corresponding data are collected rather than generated by the benchmark. Interp. denotes interpretability*

![[assets/figures/papers/paper_list_l2755_https_openaccess_thecvf_com_content_CVPR2026_html_Zhang_VMD_FACT_A_New_V/figures/004_Figure_3.jpg]]
*Figure 3: Overall data distribution of the RAVM dataset. (a) The split of training, validation, and test sets. (b) Distribution of claim–video pairs under claim manipulations. (c) Distribution of claim–video pairs under video manipulations*

评估以准确率（Accuracy）和宏 F1（Macro F1）为主要指标，同时关注方法的可解释性支持。

### RAVM 上的主实验结果

Table 2 报告了所提方法 IEEG 与现有 SOTA 方法在 RAVM 测试集上的性能对比。核心发现如下：

![[assets/figures/papers/paper_list_l2755_https_openaccess_thecvf_com_content_CVPR2026_html_Zhang_VMD_FACT_A_New_V/figures/006_Table_2.jpg]]
*Table 2: Performance comparison with the state-of-the-art methods on our proposed RAVM. “↑” indicates better performance with higher values. Interp. indicates whether the method supports reasoning or binary classification tasks. We mainly focus on Accuracy and Macro F1, as both metrics characterize the model’s overall performance and its balance in category detection. DeepSeek-V3.2-Exp [17] takes detailed textual descriptions of the claim–video pairs as input*

**IEEG 显著优于所有对比方法。** IEEG 达到 75.99% 的准确率和 73.44% 的宏 F1，相比最强闭源 MLLM Gemini 2.5（68.89% 准确率）提升了 7.10 个百分点。这一结果表明，显式建模多模态证据间依赖关系的证据图推理机制，在检测高度逼真的 AI 生成虚假视频方面具有明确优势。

**现有 MLLM 在 RAVM 上表现有限。** 闭源模型 Gemini 2.5 仅取得 68.89% 的准确率，开源模型 InternVL3.5 表现更低。值得注意的是，DeepSeek-V3.2-Exp 仅接收文本描述作为输入，与直接处理视频的模型不完全可比，但其较低的准确率也反映出纯文本推理在处理跨模态虚假信息时的局限性。

**可解释性方法的优势。** 支持推理过程输出的方法（如 Fact-R1、FakingRecipe）在可解释性维度上优于仅输出二分类结果的基线，但 IEEG 通过证据图将推理步骤结构化，在可解释性与检测性能之间取得了更好的平衡。

### 跨数据集鲁棒性实验

Table 3 展示了在 RAVM 子集（Ours*，移除源自 FakeTT 和 FMNV 的样本以避免数据泄露）上微调后的跨数据集泛化能力。

![[assets/figures/papers/paper_list_l2755_https_openaccess_thecvf_com_content_CVPR2026_html_Zhang_VMD_FACT_A_New_V/figures/007_Table_3.jpg]]
*Table 3: Experimental results of robustness improvement via fine-tuning on our proposed RAVM. Ours∗ denotes the subset of RAVM after removing samples originating from the existing datasets FakeTT [5] and FMNV [32]. For the same test dataset, the best result for each metric is highlighted in bold. “/” indicates that the MLLM is not fine-tuned on the training dataset*

**微调带来显著鲁棒性提升。** 在 FakeTT 上，IEEG 的准确率从未微调的 41.61% 跃升至 78.26%，提升幅度高达 36.65%；在 FakeSV 上，准确率从 56.70% 提升至 70.18%，提升 13.48%。这表明 RAVM 所提供的逼真 AI 生成虚假样本能够有效增强模型对真实世界虚假信息的检测泛化能力。

**RAVM 数据的迁移价值。** 即使仅使用 RAVM 子集进行微调，模型在多个外部数据集上均取得最优结果，验证了该数据集在虚假信息检测任务中的独特价值——其高度逼真的跨模态一致性伪造模式，是现有编辑式数据集所无法提供的训练信号。

### 模式迁移性实验

Table 4 报告了使用现有数据集（FakeSV、FakeTT、FMNV）训练、在 RAVM 测试集上评估的模式迁移性结果。

![[assets/figures/papers/paper_list_l2755_https_openaccess_thecvf_com_content_CVPR2026_html_Zhang_VMD_FACT_A_New_V/figures/008_Table_4.jpg]]
*Table 4: Experimental results of pattern transferability. The training data are taken from the training sets of existing datasets, including FakeSV [23], FakeTT [5], and FMNV [32], while the test data use the original test set of RAVM*

**现有数据集训练的模式难以迁移至 RAVM。** 所有方法在使用现有数据集训练后，在 RAVM 上的准确率均显著低于在 RAVM 上直接训练的结果。这一现象印证了本文的核心瓶颈判断：现有数据集主要依赖编辑技术生成伪影，其伪造模式与 AI 生成的真实伪造存在本质差异，导致模型无法有效泛化。

### 语义一致性与真实性评估

Table 5 和 Table 6 分别使用 AGAV-Rater 结合用户研究，以及 VBench 基准，对 RAVM 中生成视频的语义一致性和真实性进行了评估。结果表明，多智能体迭代反馈优化框架生成的操纵视频在语义对齐度和视觉真实性方面均达到较高水平，这进一步解释了现有 MLLM 在 RAVM 上性能受限的原因——逼真的伪造使得跨模态不一致性这一传统检测线索失效。

![[assets/figures/papers/paper_list_l2755_https_openaccess_thecvf_com_content_CVPR2026_html_Zhang_VMD_FACT_A_New_V/figures/010_Table_5.jpg]]
*Table 5: Evaluation of semantic consistency and realism using AGAV-Rater and user studies*

![[assets/figures/papers/paper_list_l2755_https_openaccess_thecvf_com_content_CVPR2026_html_Zhang_VMD_FACT_A_New_V/figures/011_Table_6.jpg]]
*Table 6: Evaluation of semantic consistency and realism using VBench*

### 失败模式分析

尽管 IEEG 取得了最优性能，其 75.99% 的准确率仍意味着约 24% 的样本被错误分类。结合方法设计推断，可能的失败模式包括：

1. **细粒度操纵的漏检：** IEEG 当前仅支持二分类（真/假），对于仅涉及局部细节篡改（如时间、地点的微妙替换）的虚假视频，证据图可能无法捕获足够强的冲突信号。
2. **对抗性生成的挑战：** 多智能体框架中引入了对抗评估器来筛选具有误导性的样本，这些样本天然具备规避检测的特性，可能构成 IEEG 的持续挑战。
3. **跨模态依赖建模的边界：** 当声明与视频在语义层面高度一致，仅通过上下文或外部知识才能判定虚假时，IEEG 的内部证据（声明-视频一致性）可能不足以做出正确判断，需要更强的外部知识检索与融合机制。

*注：以上失败模式基于方法设计推断，原文未提供详细的消融实验或错误分类分析，具体归因需进一步验证。*

### 补充图表

![[assets/figures/papers/paper_list_l2755_https_openaccess_thecvf_com_content_CVPR2026_html_Zhang_VMD_FACT_A_New_V/figures/005_Figure_4.jpg]]
*Figure 4: The word cloud visualization of claims in RAVM*

![[assets/figures/papers/paper_list_l2755_https_openaccess_thecvf_com_content_CVPR2026_html_Zhang_VMD_FACT_A_New_V/figures/009_Figure_5.jpg]]
*Figure 5: Visualization of RAVM, showing a manipulated claim and its corresponding generated video*

## 方法谱系与知识库定位

### 1. 问题域定位：从编辑伪影到生成式跨模态一致性

视频虚假信息检测的演进可划分为两个阶段。早期数据集和方法聚焦于**编辑型操纵**（如换脸、拼接），其核心检测信号是操纵引入的低级视觉伪影与跨模态不一致性。然而，随着扩散模型和闭源视频生成模型（如 Sora、Jimeng）的成熟，**AI 原生生成视频**实现了高度的视觉真实性与跨模态语义一致性，使得依赖伪影检测的传统范式失效。VMD-FACT 的核心洞察在于：**当前瓶颈已从“检测编辑痕迹”迁移至“理解多模态证据间的复杂依赖关系并执行可解释的事实核查推理”**。

### 2. 与现有检测范式的谱系关系

#### 2.1 基于创作过程的检测方法

**FakingRecipe**（Bu et al., ACM MM 2024）代表了一类新兴范式：通过逆向推断虚假内容的“创作过程”来辅助检测。该方法试图理解虚假信息是如何被制造出来的，但其推理链仍以隐式方式嵌入模型，缺乏对多模态证据间依赖关系的显式建模。IEEG 延续了“理解生成过程”的思路，但将其形式化为**有向无环证据图**，使得证据间的因果依赖可被显式追溯和验证。

#### 2.2 基于深度推理的检测方法

**Fact-R1**（Zhang et al., arXiv 2025）探索了利用深度推理能力进行可解释虚假新闻检测。该方法依赖链式思维（Chain-of-Thought）逐步展开推理，但 CoT 的线性结构难以捕捉多模态证据间的并行依赖与交叉验证关系，且推理链中的早期错误会沿链累积。IEEG 以**图结构**替代线性链，允许证据节点间的多路径依赖建模，从结构上缓解了错误累积问题。

#### 2.3 通用多模态大模型的直接应用

实验揭示了现有 MLLM 在 RAVM 上的性能上限：表现最好的闭源模型 **Gemini 2.5**（Comanici et al., arXiv 2025）仅取得 68.89% 准确率，开源模型 **InternVL3.5**（Wang et al., arXiv 2025）表现更弱。值得注意的是，**DeepSeek-V3.2-Exp**（Liu et al., arXiv 2025）仅接收文本描述作为输入，其性能与直接处理视频的模型不可直接可比（见表 Table 2 注释）。这一对比揭示了一个关键发现：**通用 MLLM 的隐式跨模态融合机制不足以应对高真实度生成视频的检测需求**，显式的证据图建模提供了必要的结构化推理能力。

### 3. 方法体系的关键设计差异

| 设计维度 | 基线范式 | IEEG 的改进 |
|---------|---------|------------|
| 推理机制 | CoT 线性链或隐式跨模态融合 | 显式内部-外部证据图，建模有向无环依赖关系 |
| 训练目标 | 标准分类交叉熵损失 | 知识蒸馏损失 $\mathcal{L} = \mu \mathbb{E}_{c,v \sim \Omega, r \sim \mathcal{D}} [-\log P(r \mid c, v, \mathbf{I})]$，最大化推理路径概率 |
| 可解释性 | 无或仅输出类别标签 | 输出包含事实核查推理步骤的证据图，支持可解释检测 |

这些设计差异直接转化为性能增益：IEEG 在 RAVM 上达到 **75.99% 准确率和 73.44% 宏 F1**，较 Gemini 2.5 提升 **+7.10%**（Table 2）。

### 4. 跨数据集鲁棒性与迁移性

**鲁棒性验证**（Table 3）表明，在 RAVM 子集（移除源自 FakeTT 和 FMNV 的样本以避免数据泄露）上微调后，IEEG 在 FakeTT 上的准确率从 41.61% 跃升至 **78.26%（+36.65%）**，在 FakeSV 上从 56.70% 提升至 **70.18%（+13.48%）**。这一大幅提升说明 RAVM 的生成式虚假信息分布有效补充了现有数据集的覆盖盲区。

**模式迁移性实验**（Table 4）进一步揭示：在 FakeSV、FakeTT、FMNV 等现有数据集上训练后直接测试 RAVM，性能显著下降。这验证了 RAVM 所引入的生成式操纵模式与编辑型数据集存在**系统性分布偏移**，现有检测器习得的伪影检测模式难以迁移至生成式场景。

### 5. 方法适用边界与局限

**适用边界**：
- IEEG 的设计前提是虚假信息涉及**可被多模态证据验证的事实性声明**。对于纯观点性、主观性内容或缺乏可验证外部证据的声明，证据图的构建基础将受到削弱。
- 方法目前针对**二分类（真实/虚假）**场景，未覆盖更细粒度的虚假信息类别（如误导意图分类、操纵技术识别）。

**已知局限**：
1. **可复现性受限**：数据集构建严重依赖商业闭源模型（Sora、Jimeng），限制了完全独立的复现与扩展。
2. **对抗评估器细节缺失**：生成框架中的对抗评估器 $\mathbf{E}_{adv}$ 的训练细节和所用数据集未充分披露，其鲁棒性边界难以独立评估。
3. **细粒度分类缺失**：当前 IEEG 仅输出二分类结果，未利用证据图的结构信息进行操纵技术溯源或意图分类。
4. **语言与文化覆盖**：RAVM 的数据构建和验证主要基于英文场景，跨语言和跨文化背景下的证据图构建与验证能力尚待检验。

### 6. 在知识库中的位置与后续工作方向

VMD-FACT 在方法谱系中占据了一个独特位置：**它是首个将多模态证据依赖关系显式建模为有向无环图，并与多智能体驱动的生成式虚假信息数据集联合设计的工作**。其贡献不仅在于提出 IEEG 检测模型，更在于通过 RAVM 数据集暴露了现有 MLLM 在生成式虚假信息检测上的系统性弱点。

后续工作可沿以下方向展开：
- **证据图的动态扩展**：将 IEEG 与实时外部知识检索（如搜索引擎、知识图谱）结合，使证据图能够动态纳入最新的事实信息。
- **细粒度虚假信息分类**：利用证据图的结构特征（如操纵路径、证据冲突模式）实现操纵技术溯源和意图分类。
- **开放域与跨语言泛化**：探索在开源视频生成模型上构建可完全复现的数据集，并验证 IEEG 在跨语言场景下的迁移能力。

## 原文 PDF

![[paperPDFs/CVPR_2026/VMD_FACT_A_New_Video_Dataset_and_MLLM_based_method_for_Detecting_Realistic_AI_Generated_Video_Misinformation.pdf]]
