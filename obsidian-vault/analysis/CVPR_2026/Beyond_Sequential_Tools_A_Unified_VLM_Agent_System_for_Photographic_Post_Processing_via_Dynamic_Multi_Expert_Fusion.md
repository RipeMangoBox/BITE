---
title: "Beyond Sequential Tools: A Unified VLM Agent System for Photographic Post-Processing via Dynamic Multi-Expert Fusion"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/Beyond_Sequential_Tools_A_Unified_VLM_Agent_System_for_Photographic_Post_Processing_via_Dynamic_Multi_Expert_Fusion.pdf
project_link: null
code_link: "https://github.com/chaofengc/IQA-PyTorch"
aliases:
- UVASPPPDMEF
tags:
- CVPR_2026
- topic/other_unclear
- topic/other_unclear/general
core_operator: 通过VLM一次性动态融合多个专家LoRA模块，替代顺序流水线，实现协同一次通过修复。
primary_logic: 利用VLM进行意图理解和退化诊断，动态分配权重给仅适应K/V矩阵的LoRA专家，并将这些专家加权合并到预训练扩散模型中，实现单步、上下文感知的修复。
claims:
- 在Real-1000数据集上，我们的方法在Group 1和Group 2的PSNR上显著优于现有最佳方法（InstructIR 21.72→22.90，AutoDIR 18.79→21.10），且定性比较显示避免了顺序代理的错误累积和内容幻觉。
- 消融研究证实，VLM代理、专家LoRA和DPO优化每个组件对最终性能至关重要，且仅适应K/V矩阵和动态权重融合优于全LoRA或固定权重。
- Real-1000 Group 1 (single degradation) 上 PSNR = 22.90
- Real-1000 Group 2 (two degradations) 上 PSNR = 21.10
---

# Beyond Sequential Tools: A Unified VLM Agent System for Photographic Post-Processing via Dynamic Multi-Expert Fusion

> [!tip] 核心洞察
> 利用VLM进行意图理解和退化诊断，动态分配权重给仅适应K/V矩阵的LoRA专家，并将这些专家加权合并到预训练扩散模型中，实现单步、上下文感知的修复。

| 字段 | 内容 |
|------|------|
| 中文题名 | 超越顺序工具：面向摄影后处理的统一VLM代理系统与动态多专家融合 |
| 英文题名 | Beyond Sequential Tools: A Unified VLM Agent System for Photographic Post-Processing via Dynamic Multi-Expert Fusion |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://openaccess.thecvf.com/content/CVPR2026/html/Xiong_Beyond_Sequential_Tools_A_Unified_VLM_Agent_System_for_Photographic_CVPR_2026_paper.html) · [Code](https://github.com/chaofengc/IQA-PyTorch) |
| Topic | #topic/other_unclear #topic/other_unclear/general |
| Method | Unified VLM Agent System for Photographic Post-Processing via Dynamic Multi-Expert Fusion |
| Dataset | Real-1000 Group 1, Real-1000 Group 2 |

> [!tip] 效果简介
> - Real-1000 Group 1 (single degradation) 上，PSNR 22.90 vs 21.72 (InstructIR) (+1.18)。
> - Real-1000 Group 2 (two degradations) 上，PSNR 21.10 vs 18.79 (AutoDIR) (+2.31)。

## 概述

摄影后处理面临的核心挑战是真实世界图像中**多种退化（噪声、模糊、JPEG伪影等）的复杂耦合**。现有方案主要分为两类：一是“一体式”模型，试图用单一网络处理所有退化，但泛化能力差；二是基于代理的系统，顺序调用多个专用工具，却因**错误累积与伪影放大**而失效——例如先降噪再去模糊的流水线可能将前一步的残余伪影误判为信号，导致灾难性放大（Figure 3）。

本文提出一种**统一VLM代理系统**，以**动态多专家一次性融合**替代顺序工具调用。核心思路是：利用视觉-语言模型（VLM）作为编排器，同时完成用户意图理解与退化诊断，然后**动态分配权重给一组专家LoRA模块**，将这些仅适应K/V矩阵的轻量适配器**加权合并到预训练扩散骨干（Flux-Kontext）中**，实现单步、上下文感知的协同修复。该方法从因果层面切断了顺序流水线的错误传播路径，同时保留了各专家的专业化能力。

在Real-1000基准上，该方法在单一退化（Group 1）和双重退化（Group 2）场景下分别达到**22.90 dB**和**21.10 dB**的PSNR，较先前最优方法InstructIR（21.72 dB）和AutoDIR（18.79 dB）提升显著（Table 1）。消融实验证实，VLM代理、专家LoRA模块及DPO优化的动态权重分配三者缺一不可（Table 4, Table 5）。

### 方法谱系与知识库定位

本工作处于**VLM驱动的图像修复**与**参数高效微调**的交叉点。与以下代表性基线的关系如下：

- **InstructIR**（Conde et al., ECCV 2024）：文本引导的单一模型修复，缺乏对混合退化的显式分解与专家协同。
- **AutoDIR**（Jiang et al., ECCV 2024）：自动一体式修复，但面对分布外退化组合时泛化受限。
- **AgenticIR**（Zhu et al., 2024）：代理式顺序工具调用，本文的直接对比对象，其核心缺陷——错误累积——正是本方法通过动态融合所解决的关键瓶颈。
- **DA-CLIP**（Luo et al., ICLR 2024）：基于CLIP的通用修复，提供了视觉-语言对齐的范式参考，但未涉及多专家融合。
- **DiffUIR**（Zheng et al., CVPR 2024）与**Flux-Kontext**（Batifol et al., 2025）：扩散模型修复骨干，本方法在Flux-Kontext之上构建专家融合层，展示了扩散先验与模块化适配的兼容性。

在知识库定位上，本方法将**LoRA的可加性**从自然语言处理领域迁移至视觉修复，并通过**仅适应K/V矩阵**的策略保证专家间的线性可组合性，同时引入**DPO优化的权重分配分支**实现感知对齐的动态融合。这为“基础模型+即插即用专家库”的摄影后处理范式提供了完整的系统级验证。

## 背景与动机

### 摄影后处理的现实困境

数字图像在拍摄与传输过程中不可避免地遭受多种退化，如噪声、模糊、JPEG压缩伪影、低光照等。真实世界照片往往同时耦合多种退化，形成**混合退化**（mixed degradations），其分布远非单一退化任务所能覆盖。摄影后处理（photographic post-processing）的目标正是对这些退化进行联合修复，恢复图像的视觉质量与细节保真度。

### 现有范式及其根本缺陷

当前主流的图像修复方法可归为两类范式，但二者均存在结构性瓶颈：

1. **“一体式”模型（All-in-One Models）**：试图用单一模型处理任意退化组合，如**DA-CLIP**（Luo et al., ICLR 2024）、**InstructIR**（Conde et al., ECCV 2024）、**AutoDIR**（Jiang et al., ECCV 2024）等。这类方法在训练时需覆盖多种退化，但在面对未见过的退化组合时**泛化能力显著下降**，难以适应真实场景的开放分布。

2. **顺序代理系统（Sequential Agentic Systems）**：如**AgenticIR**（Zhu et al., 2024），通过VLM代理逐步调用多个孤立工具，依次处理每种退化。这一范式继承了LLM代理的灵活性，却引入了**错误累积与伪影放大**的致命缺陷：前一步修复引入的伪影会被后续步骤当作真实信号进一步“增强”，导致块效应加剧、噪声灾难性放大，甚至产生内容幻觉（如凭空生成不存在的物体）。

两种范式的共同根源在于**修复策略的割裂性**——要么将所有退化压缩进同一个静态模型，要么将其拆解为孤立的顺序步骤，二者都无法实现多退化的协同感知与一次性联合修复。

### 核心瓶颈与突破口

上述分析揭示了一个清晰的因果瓶颈：**现有方法缺乏一个能够同时理解用户意图、诊断混合退化严重程度、并一次性协同调度多个修复能力的统一调度机制**。顺序代理的失败尤其表明，修复任务之间存在强耦合——去模糊与去JPEG伪影、去噪与去模糊之间并非独立可分解的子问题，而需要上下文感知的联合决策。

本文的核心动机正是突破这一瓶颈：**利用VLM的视觉理解与推理能力作为统一编排器，通过动态融合多个专家修复模块，将“顺序调用”替换为“单步协同融合”，从根本上消除错误累积路径，同时保持对开放世界退化组合的泛化能力**。这一思路将VLM从“工具调用者”重新定位为“能力编排者”，是本文方法论的逻辑起点。

### 方法定位

基于上述动机，我们提出**面向摄影后处理的统一VLM代理系统与动态多专家融合**框架。该系统由一个VLM编排器、一个DPO优化的权重分配分支、一组仅适应K/V矩阵的专家LoRA模块，以及一个预训练扩散骨干（**Flux-Kontext**, Batifol et al., 2025）构成。VLM一次性分析输入图像与用户提示，诊断退化类型与严重程度，动态分配专家权重，并将多个LoRA专家同时合并到扩散模型中，实现单步、上下文感知的协同修复。后续章节将详细展开该框架的设计逻辑、技术细节与实验验证。

## 核心创新

### 1. 创新动机：从顺序工具链到一次性协同修复

现有图像修复代理系统（如 **AgenticIR** (Zhu et al., 2024)）遵循“感知-规划-执行”的顺序范式，将混合退化问题分解为多个独立的原子任务，依次调用专用模型进行修复。这种顺序流水线存在两个根本性缺陷：

- **错误累积与伪影放大**：前序模型的修复误差会被后续模型继承并放大，尤其在退化类型相互耦合时（如运动模糊叠加 JPEG 压缩伪影），顺序调用会加剧块效应或噪声（见 Figure 3a-b）。
- **“一体式”模型的泛化瓶颈**：单一模型（如 **AutoDIR** (Jiang et al., ECCV 2024)）试图在固定参数空间内覆盖所有退化组合，面对真实世界中分布外的混合退化时性能急剧下降。

本工作的核心洞察在于：**利用视觉语言模型（VLM）作为编排器，一次性诊断所有退化类型及其严重程度，并通过动态融合多个专家 LoRA 模块，实现单步、上下文感知的协同修复**，从根本上消除顺序依赖。

### 2. 关键创新点（Changed Slots）

相较于现有基线方法，本工作在三个关键维度上实现了范式转变：

| 创新维度 | 基线方法 | 本方法 | 证据锚点 |
|---------|---------|--------|---------|
| **修复策略** | 顺序调用多个孤立模型或单一“一体式”模型 | 基于 VLM 的动态多专家一次性协同融合 | Abstract, Section 1 |
| **权重分配** | 无动态权重或手动启发式 | DPO 优化的 MLP 分支基于 VLM 特征分配连续权重 | Section 3.2 |
| **LoRA 适应范围** | 标准 LoRA 适应 Q、K、V 或全参数微调 | 仅适应 K 和 V 矩阵，保留 Q 冻结以维持注意力结构 | Section 3.3 |

#### 2.1 修复策略：VLM 编排的动态多专家融合

系统以 **Qwen2.5-VL-72B** 作为 VLM 编排代理，接收用户自然语言指令和输入图像，执行两项核心分析（Section 3.1）：

1. **意图理解与提示增强**：将用户的模糊指令（如“修复这张老照片”）转化为扩散模型可精确执行的描述性文本提示。
2. **退化诊断与专家选择**：识别图像中存在的退化类型（如噪声、模糊、JPEG 伪影），并评估每种退化的严重程度，据此选择对应的专家 LoRA 模块并分配权重。

随后，系统通过动态 LoRA 融合机制，将选定的专家 LoRA 按其权重一次性合并到预训练扩散骨干 **Flux-Kontext** (Batifol et al., 2025) 中，形成临时专用模型进行单次修复。这从根本上避免了顺序代理的中间误差传递。

#### 2.2 权重分配：DPO 优化的感知对齐

权重分配通过一个 MLP 分支实现，该分支以 VLM 的视觉特征为输入，输出每个专家的连续权重。为使其与人类感知偏好对齐，作者采用 **Direct Preference Optimization (DPO)** 训练该分支（Section 3.2）：

- 将权重分配建模为离散权重箱的选择问题，假设各专家独立，其联合对数概率为：

$$\log \pi _ { \theta } ( y | x ) = \sum _ { i = 1 } ^ { N } \log \pi _ { \theta } ( y ^ { i } | x )$$

- DPO 损失函数直接优化策略 $\pi_\theta$，增大“获胜”权重组合 $y_w$ 的概率，降低“失败”组合 $y_l$ 的概率，相对于冻结的参考策略 $\pi_{\mathrm{ref}}$：

$$\mathcal { L } = - \mathbb { E } \bigg [ \log \sigma \Big ( \beta \Big ( \log \frac { \pi \theta ( y _ { w } | x ) } { \pi _ { \mathrm { r e f } } ( y _ { w } | x ) } - \log \frac { \pi _ { \theta } ( y _ { l } | x ) } { \pi _ { \mathrm { r e f } } ( y _ { l } | x ) } \Big ) \Big ) \bigg ]$$

消融实验（Table 5）证实，DPO 优化的动态权重显著优于无 DPO 的固定权重策略，验证了感知对齐的必要性。

#### 2.3 LoRA 适应范围：仅更新 K/V 矩阵的可组合性设计

为实现多专家的线性可加融合，作者对标准 LoRA 进行了关键约束：**仅适应 Key (K) 和 Value (V) 投影矩阵，保持 Query (Q) 矩阵冻结**（Section 3.3）。融合公式为：

$$W_M' = W_{0,M} + \sum_{i=1}^N w_i \cdot \Delta W_{i,M}, \quad \mathrm{where} \ M \in \{K, V\}$$

这一设计的合理性在于：
- Q 矩阵控制“查询什么”，保留其冻结可维持预训练扩散模型的注意力结构，避免多个专家在 Q 空间的冲突。
- K/V 矩阵控制“关注什么信息”，仅更新它们使得不同专家的任务向量（task vectors）在 K/V 空间可线性叠加，实现真正的可组合性。

消融实验（Table 5）表明，仅适应 K/V 矩阵（K-V only）优于全 LoRA 适应（更新 Q、K、V），验证了该设计对多专家融合场景的关键作用。

### 3. 创新证据强度

- **定量证据**：在 Real-1000 数据集上，本方法在 Group 1（单一退化）的 PSNR 达到 22.90，超越 **InstructIR** (Conde et al., ECCV 2024) 的 21.72（+1.18 dB）；在 Group 2（两种退化混合）的 PSNR 达到 21.10，超越 **AutoDIR** 的 18.79（+2.31 dB），如表 1 所示。退化类型越复杂，优势越显著，直接印证了多专家协同融合对混合退化的处理能力。
- **定性证据**：Figure 3 展示了与 SOTA 顺序代理系统的对比，顺序代理在运动模糊+JPEG 伪影场景下加剧块效应，在散焦模糊+噪声场景下灾难性放大噪声，甚至产生不存在的鸟类内容幻觉；本方法避免了这些失败模式。
- **消融证据**：Table 4 的增量消融表明，添加 VLM 代理（A+B）和专家 LoRA 模块（A+B+C）均带来显著增益；Table 5 证实 K-V only 适应与 DPO 权重优化各自独立贡献于最终性能。

## 整体框架

本方法提出一个以视觉语言模型（VLM）为编排核心的统一代理系统，将传统“顺序工具调用”范式替换为“单次动态多专家融合”，实现面向摄影后处理的通用图像修复。系统流水线如图1所示，由三个关键阶段构成：**VLM编排代理的意图理解与退化诊断**、**基于DPO的专家权重分配**、以及**动态LoRA融合与扩散主干执行**。

### 核心瓶颈与设计动机

现有代理系统（如**AgenticIR**，Zhu et al., 2024）依赖顺序调用多个孤立修复模型，这导致两个根本性问题：一是错误累积——前一阶段的修复伪影会被后续模型放大；二是缺乏全局协同——各模型独立决策，无法感知混合退化的耦合关系。同时，“一体式”模型（如**AutoDIR**，Jiang et al., ECCV 2024）虽能处理多种退化，但面对真实世界中未见过的退化组合时泛化能力显著下降。本工作的核心洞察在于：**利用VLM的一次性全局理解能力，将多个轻量级专家LoRA模块动态融合到一个预训练扩散模型中，实现协同的单步修复**，从根本上规避顺序流水线的错误传播。

### 流水线模块与数据流

系统接收两个输入：一张待修复图像和一个非受限的用户自然语言指令。数据流经以下模块：

1.  **VLM编排代理（VLM Orchestrator Agent）**：基于Qwen2.5-VL-72B构建，负责双重分析——解析用户指令中的审美意图与操作目标，同时诊断输入图像中的退化类型及其严重程度。代理输出一个结构化修复计划，包含两部分：（a）针对扩散模型优化的精炼文本提示，将用户意图转化为模型可执行的描述性语言；（b）一组选定的专家LoRA模块及其对应的连续权重系数，权重直接反映各退化的严重性。

2.  **权重分配分支（Weight Allocation Branch）**：这是一个轻量级MLP模块，以VLM提取的视觉特征为输入，输出每个专家LoRA的权重。该分支通过DPO（Direct Preference Optimization）训练，以人类感知偏好为监督信号，学习生成感知最优的权重组合。其训练目标为最大化获胜权重组合的对数概率，同时抑制失败组合，损失函数如下：

    $$\mathcal{L} = -\mathbb{E}\bigg[\log\sigma\Big(\beta\Big(\log\frac{\pi_\theta(y_w|x)}{\pi_{\mathrm{ref}}(y_w|x)} - \log\frac{\pi_\theta(y_l|x)}{\pi_{\mathrm{ref}}(y_l|x)}\Big)\Big)\bigg]$$

    其中 $y_w$ 和 $y_l$ 分别表示获胜和失败的离散权重箱组合，$\pi_\theta$ 为当前策略，$\pi_{\mathrm{ref}}$ 为参考策略。

3.  **专家LoRA模块（Expert LoRA Modules）**：每个专家针对单一退化类型（如去噪、去模糊、去JPEG压缩）独立训练，仅适应基础扩散模型注意力层中的Key（K）和Value（V）投影矩阵，保持Query（Q）矩阵冻结。这一设计选择（K-V-only adaptation）被消融实验证实优于全LoRA适应，因为它保留了注意力结构的稳定性，同时赋予不同专家更好的可组合性。

4.  **动态LoRA融合（Dynamic LoRA Fusion）**：系统根据权重分配分支输出的系数，将所有选定专家的任务向量（$\Delta W_{i,M}$）加权累加到预训练扩散骨干的对应K/V矩阵上：

    $$W_M' = W_{0,M} + \sum_{i=1}^N w_i \cdot \Delta W_{i,M}, \quad \mathrm{where} \ M \in \{K, V\}$$

    这一融合过程是单次、可微且即时的，无需多次前向传播或迭代优化。融合后的临时模型即成为针对当前输入量身定制的专用修复器。

5.  **预训练扩散骨干（Pretrained Diffusion Backbone）**：采用**Flux-Kontext**（Batifol et al., 2025）作为基础生成模型，提供强大的自然图像先验。融合后的模型接收输入图像与VLM生成的精炼提示，通过标准扩散去噪过程输出修复结果。

### 关键设计选择

- **单次融合 vs. 顺序调用**：传统代理系统将退化处理视为串行步骤（先去噪、再去模糊），而本方法通过线性可加性将多个专家同时合并，实现真正的协同修复。图3的定性对比清晰展示了顺序代理在混合退化场景下的失效模式——如运动模糊叠加JPEG伪影时，顺序处理反而加剧块效应；散焦模糊叠加噪声时，噪声被灾难性放大。
- **K-V-only LoRA**：仅适应K/V矩阵而非全参数或QKV，在保持专家可组合性的同时避免了注意力结构的破坏。消融实验（Table 5）证实该策略结合DPO优化权重后，性能显著优于全LoRA或无DPO版本。
- **DPO驱动的权重学习**：摒弃手动启发式规则，通过人类偏好数据驱动权重分配，使系统能感知不同退化组合对视觉质量的实际影响，而非简单依赖退化严重性的先验假设。

### 补充图表

![[assets/figures/papers/paper_list_l2162_https_openaccess_thecvf_com_content_CVPR2026_html_Xiong_Beyond_Sequentia/figures/001_Figure_1.jpg]]
*Figure 1: The pipeline of our method. First, the VLM agent analyzes the input image and prompt, selecting expert LoRAs and assigning weights via an RLHF-tuned adapter. Second, the LoRAs are dynamically merged into the diffusion model by updating only its K and V matrices. Finally, the adapted model performs the restoration using the image and an enhanced prompt*

## 核心模块与公式推导

### VLM编排代理（VLM Orchestrator Agent）

系统以 **Qwen2.5-VL-72B** 作为核心编排器，负责两重关键功能：**用户意图理解**与**图像退化诊断**。给定输入图像和用户文本提示，VLM代理生成一个结构化的修复计划，包含两个输出组件：一是针对扩散模型优化的精炼文本提示，将用户高层意图转化为模型可执行的描述性指令；二是一组选定的专家LoRA模块及其对应的连续权重系数，权重的大小直接反映所诊断退化的严重程度。这一设计将感知理解与执行规划解耦，使后续的专家融合完全由数据驱动。

### 权重分配分支（Weight Allocation Branch）

权重分配由一个基于VLM视觉特征的MLP分支实现。该分支将VLM提取的图像特征 $x$ 映射为一组离散权重箱（weight bins）的组合 $y = \{y^1, y^2, \dots, y^N\}$，其中 $N$ 为专家LoRA的数量。假设各专家之间相互独立，策略 $\pi_\theta$ 输出该权重组合的对数概率为：

$$
\log \pi_\theta(y|x) = \sum_{i=1}^{N} \log \pi_\theta(y^i|x)
$$

为使得权重分配与人类感知偏好对齐，该分支通过 **DPO（Direct Preference Optimization）** 进行训练。给定获胜权重组合 $y_w$ 和失败组合 $y_l$ 的偏好对，DPO损失函数为：

$$
\mathcal{L} = -\mathbb{E}\bigg[\log\sigma\Big(\beta\Big(\log\frac{\pi_\theta(y_w|x)}{\pi_{\mathrm{ref}}(y_w|x)} - \log\frac{\pi_\theta(y_l|x)}{\pi_{\mathrm{ref}}(y_l|x)}\Big)\Big)\bigg]
$$

其中 $\pi_{\mathrm{ref}}$ 为参考策略，$\beta$ 控制偏离参考策略的强度，$\sigma$ 为sigmoid函数。该目标直接增大获胜组合的概率并抑制失败组合，无需显式奖励模型。

### 专家LoRA模块与动态融合（Expert LoRA Modules & Dynamic Fusion）

每个专家LoRA模块针对单一退化类型（如去噪、去模糊、JPEG去伪影）独立训练，仅在对应任务数据集上学习。关键设计选择在于**仅适应K（Key）和V（Value）投影矩阵**，而冻结Q（Query）矩阵保持不变。其原理在于：Q矩阵决定注意力模式中的“查询”方向，保持其冻结可维持预训练扩散模型原有的注意力结构，而K/V矩阵的适配足以捕获退化特定的修复能力，同时最大化不同专家之间的可组合性。

动态LoRA融合的数学形式为对K和V矩阵的任务向量进行加权求和：

$$
W_M' = W_{0,M} + \sum_{i=1}^{N} w_i \cdot \Delta W_{i,M}, \quad \mathrm{where} \ M \in \{K, V\}
$$

其中 $W_{0,M}$ 为预训练扩散骨干的原始K/V权重矩阵，$\Delta W_{i,M}$ 为第 $i$ 个专家LoRA学习到的任务向量（低秩分解 $B_i A_i$ 的乘积），$w_i$ 为VLM代理分配的权重系数。融合后的单一模型 $W_M'$ 一次性执行修复，从根本上避免了顺序工具调用中错误累积和伪影放大的问题。

### 预训练扩散骨干（Pretrained Diffusion Backbone）

修复执行基于 **Flux-Kontext** 预训练扩散模型，该模型提供强大的生成先验。在推理时，系统将动态融合后的K/V矩阵注入扩散骨干，结合VLM生成的增强提示，通过标准扩散采样过程输出修复图像。整个流水线仅需一次前向模型组装和一次扩散推理，实现了**上下文感知的单步协同修复**。

## 实验与分析

### 核心性能：Real‑1000 基准

我们首先在 Real‑1000 数据集上验证方法对真实世界混合退化的修复能力，该数据集按退化复杂度分为三组（Group 1 单一退化、Group 2 两种退化、Group 3 三种退化），所有方法均以零样本设定评估。表 1 汇总了与当前最先进方法的定量比较。

在 Group 1（单一退化）上，本文方法取得 **22.90 PSNR**，较此前最佳的 **InstructIR**（Conde et al., ECCV 2024）的 21.72 PSNR 提升 **+1.18 dB**。在更具挑战性的 Group 2（两种退化混合）上，本文方法达到 **21.10 PSNR**，大幅超越 **AutoDIR**（Jiang et al., ECCV 2024）的 18.79 PSNR，提升 **+2.31 dB**。这一增益直接对应到真实瓶颈的突破：AutoDIR 等“一体式”模型难以泛化到耦合退化，而本文通过 VLM 一次性动态融合多个专家 LoRA，避免了顺序流水线的错误累积。在 Group 3（三种退化）上，方法依然保持竞争力，但定量差距收窄，提示极端退化组合下仍有提升空间。

定性结果（图 2）进一步印证了上述结论。在包含噪声、模糊、JPEG 伪影的真实图像上，本文方法恢复的纹理细节更丰富，且未出现 InstructIR 常见的过度平滑或 AutoDIR 的内容幻觉。

### 顺序代理失效案例

图 3 系统对比了本文方法与当前最先进的代理图像修复系统 **AgenticIR**（Zhu et al., 2024）在顺序工具调用下的典型失效模式，这些案例直接揭示了“顺序工具调用→错误累积”这一核心瓶颈的具体表现：

- **伪影放大**（图 3a）：输入图像同时存在运动模糊与 JPEG 块效应。顺序代理先执行去模糊，再执行 JPEG 去块，但去模糊过程将块效应误认为边缘进行增强，导致最终输出中块状伪影被显著放大。本文方法通过 VLM 一次性诊断两种退化并协同融合去模糊与去 JPEG 专家，避免了这一级联误增强。
- **噪声灾难性放大**（图 3b）：输入包含散焦模糊与噪声。顺序代理先去模糊时，将噪声视为高频细节进行强化，后续去噪步骤已无法挽回，输出呈现严重的噪声爆炸。本文方法通过动态权重同时激活去模糊与去噪专家，在扩散生成过程中协同抑制噪声。
- **非真实平滑**（图 3c）：顺序代理在处理轻度退化时过度调用增强工具，导致皮肤纹理被抹平，产生“塑料感”输出。本文 VLM 代理通过意图理解与退化严重程度诊断，分配适度权重，保留了真实质感。
- **内容幻觉**（图 3d）：输入图像中并无鸟类，但顺序代理在生成过程中凭空添加了逼真但虚构的飞鸟。本文方法受限于仅适应 K/V 矩阵的 LoRA 融合，保持扩散骨干的注意力结构（Q 冻结），从而更好地忠实于输入内容，未出现此类幻觉。

这些失效案例从反面验证了本文核心因果机制的合理性：VLM 一次性动态融合替代顺序流水线，是避免错误累积与伪影放大的关键。

### 组件消融：代理与专家模块的必要性

表 4 通过逐步叠加模块的方式，量化了每个组件对最终性能的贡献。基线 A 为纯 **Flux‑Kontext** 扩散骨干（Batifol et al., 2025），仅依赖默认生成能力。添加 VLM 代理进行提示增强（A+B）后，性能已有明显提升，说明 VLM 的意图理解与退化诊断能够为扩散模型提供更精准的文本引导。进一步添加专家 LoRA 模块（A+B+C，即完整方法）带来最大幅度的增益，PSNR 达到 22.90，SSIM 达到 0.7718，证明动态融合多个专家 LoRA 是实现协同修复的核心驱动力。

定性消融（图 4）在纵向单任务修复场景下可视化这一渐进过程：基线 A 输出模糊且残留退化；A+B 通过增强提示改善了整体清晰度，但局部伪影依然存在；A+B+C 完整方法实现了最干净、最真实的修复效果。

### 策略消融：K/V‑only 适应与 DPO 权重优化

表 5 消融了两个关键设计选择：(1) DPO 优化的动态权重 vs. 固定权重；(2) 仅适应 K/V 矩阵 vs. 全 LoRA（同时适应 Q、K、V）。

结果表明，**仅适应 K/V 矩阵并结合 DPO 优化权重**（Ours K‑V only + DPO）在所有指标上均优于全 LoRA 版本和无 DPO 版本。具体而言：
- 全 LoRA（适应 Q、K、V）虽然参数量更大，但性能反而下降，这验证了保留 Q 冻结以维持注意力结构对多专家可组合性的重要性——Q 矩阵的独立更新会破坏不同专家之间的线性可加性假设，导致融合后注意力分布冲突。
- 去除 DPO 优化、改用固定或启发式权重后，性能显著下降，说明感知对齐的权重分配并非简单的退化严重程度线性映射，而是需要通过人类偏好数据学习复杂的上下文依赖关系。

这一消融结果从机制层面支撑了本文的两个核心设计：K/V‑only 适应保障了 LoRA 任务向量的线性可加性，使得多专家融合在数学上成立；DPO 优化的权重分配分支则确保融合后的模型在感知质量上对齐人类偏好。

### MiO100 跨数据集泛化

表 3 报告了在 MiO100 数据集 Group C（多退化组合）上的跨数据集零样本泛化结果。本文方法取得 **19.85 PSNR**、**0.5765 SSIM**，在多个感知指标（MANIQA、CLIPIQA、MUSIQ）上保持竞争力，但 PSNR 并非最优。这一结果表明：(1) 方法具备一定的跨数据集迁移能力，VLM 代理的退化诊断泛化到未见数据分布时仍然有效；(2) 在极端分布外退化组合下，固定的专家库（当前仅覆盖 5 种退化类型）可能不足以覆盖所有退化模式，需要扩展专家“笔”库以提升鲁棒性——这也正是本文开放问题中明确指出的未来方向。

### 证据强度总结

| 主张 | 证据锚点 | 证据强度 |
|------|----------|----------|
| 动态多专家融合超越顺序代理与一体式模型 | Table 1 (Group 1 +1.18 dB, Group 2 +2.31 dB) | 强：双组别一致大幅领先 |
| 顺序代理存在错误累积与伪影放大 | Figure 3 (四个定性失效案例) | 中强：案例典型但非大规模统计 |
| VLM 代理与专家 LoRA 各自不可或缺 | Table 4 (渐进消融) | 强：定量增益明确 |
| K/V‑only + DPO 是最优融合策略 | Table 5 (策略对比消融) | 强：多指标一致验证 |
| 跨数据集泛化有效但受限于专家库覆盖 | Table 3 (MiO100 Group C) | 中：竞争但非全面领先 |

![[assets/figures/papers/paper_list_l2162_https_openaccess_thecvf_com_content_CVPR2026_html_Xiong_Beyond_Sequentia/figures/003_Table_1.jpg]]
*Table 1: Quantitative comparisons with state-of-the-art methods on the Real-1000 dataset [23]. We report results on Group 1 (single degradations), Group 2 (two degradations), and Group 3 (three degradations). All methods are evaluated in a zero-shot setting. The top two performances of each metric are marked in bold and underline respectively*

![[assets/figures/papers/paper_list_l2162_https_openaccess_thecvf_com_content_CVPR2026_html_Xiong_Beyond_Sequentia/figures/006_Table_4.jpg]]
*Table 4: Ablation study on the effectiveness of agent components. We incrementally add modules: A: Baseline generation backbone (FLUX). A+B: Adds the VLM Agent for prompt enhancing. A+B+C: Adds the expert LoRA module*

![[assets/figures/papers/paper_list_l2162_https_openaccess_thecvf_com_content_CVPR2026_html_Xiong_Beyond_Sequentia/figures/007_Table_5.jpg]]
*Table 5: Ablation study on the impact of two strategies: (1) DPOoptimized dynamic weights and (2) K-V-only LoRA adaptation*

![[assets/figures/papers/paper_list_l2162_https_openaccess_thecvf_com_content_CVPR2026_html_Xiong_Beyond_Sequentia/figures/008_Figure_3.jpg]]
*Figure 3: Qualitative comparison with the SOTA agentic system , illustrating the failures of sequential tool invocation. (a) For an input with motion blur and JPEG artifacts, the sequential agent aggravates the blocky artifacts. (b) For an input with defocus blur and noise, the sequential agent catastrophically amplifies the noise . (c) An example of Unrealistic Smoothing. (d) A failure of Content Hallucination, where the agent generates plausible but non-existent birds. Our system avoids these issues and produces faithful restorations*

![[assets/figures/papers/paper_list_l2162_https_openaccess_thecvf_com_content_CVPR2026_html_Xiong_Beyond_Sequentia/figures/005_Table_3.jpg]]
*Table 3: Quantitative comparison of multiple-degradation image restoration tasks on the Group C of MiO100 dataset. The top two performances of each metric are marked in bold and underline respectively*

**需要手动验证的点**：MiO100 上 PSNR 未达最优的具体竞争对手方法及差距数值，需查阅 Table 3 原文确认，本文分析仅基于已验证的总体结论。

### 补充图表

![[assets/figures/papers/paper_list_l2162_https_openaccess_thecvf_com_content_CVPR2026_html_Xiong_Beyond_Sequentia/figures/009_Figure_4.jpg]]
*Figure 4: Qualitative ablation study on the effectiveness of agent components. This figure illustrates the effect of progressively integrating each component on a vertical single-restoration task*

![[assets/figures/papers/paper_list_l2162_https_openaccess_thecvf_com_content_CVPR2026_html_Xiong_Beyond_Sequentia/figures/004_Table_2.jpg]]
*Table 2: Overview of training datasets used for LoRA experts*

## 方法谱系与知识库定位

### 1. 相对于基线方法的谱系定位

本工作处于**视觉-语言模型（VLM）驱动的通用图像修复**这一新兴交叉节点，其核心贡献在于将顺序工具调用范式（sequential tool invocation）重构为动态多专家一次性融合范式。为清晰定位，我们从三个维度梳理其与现有基线的谱系关系。

#### 1.1 相对于“一体式”通用修复模型

传统的通用图像修复方法可大致分为两类：基于提示引导的模型和自动一体式（all-in-one）模型。

**提示引导模型**以 **InstructIR**（Conde et al., ECCV 2024）和 **DA-CLIP**（Luo et al., ICLR 2024）为代表。InstructIR 通过文本指令控制修复行为，但其修复能力受限于单一模型对多种退化的泛化边界；DA-CLIP 利用 CLIP 嵌入引导修复，但本质上仍是一个“一体式”模型，缺乏针对不同退化的专门化处理能力。本文方法通过引入多个专家 LoRA 模块，将“通用”能力分解为“专门化专家组合”，从根本上突破了单一模型的能力上限——在 Real-1000 Group 1（单一退化）上，本文方法以 PSNR 22.90 显著优于 InstructIR 的 21.72（Table 1）。

**自动一体式模型**以 **AutoDIR**（Jiang et al., ECCV 2024）为代表，其尝试自动检测退化类型并进行修复。然而，当面对两种退化耦合的场景时，AutoDIR 的 PSNR 仅为 18.79，而本文方法达到 21.10（Table 1），提升达 +2.31 dB。这一差距揭示了一体式模型的核心瓶颈：模型内部对不同退化的处理能力相互干扰，缺乏有效的解耦机制。本文方法通过 LoRA 专家的独立训练和动态融合，实现了退化解耦与协同修复的统一。

#### 1.2 相对于代理式图像修复系统

**AgenticIR**（Zhu et al., 2024）代表了代理式图像修复的最新范式：通过 VLM 代理顺序调用多个工具模型完成复杂修复任务。这一范式与本工作最为接近，但存在根本性差异：

- **执行模式**：AgenticIR 采用顺序流水线（sequential pipeline），每个工具的输出作为下一个工具的输入。本文方法采用一次性并行融合（single-pass parallel fusion），所有专家 LoRA 同时合并到扩散骨干中。
- **错误传播**：顺序调用的致命缺陷在于错误累积与伪影放大。Figure 3 提供了关键定性证据：(a) 运动模糊+JPEG伪影场景下，顺序代理加剧了块效应；(b) 散焦模糊+噪声场景下，顺序代理灾难性地放大了噪声；(c) 出现不真实平滑；(d) 内容幻觉——生成了不存在于原图中的鸟。本文方法通过协同一次通过修复，从机制上避免了这些问题。
- **权重分配**：AgenticIR 缺乏动态权重机制，本文方法通过 DPO 优化的权重分配分支，根据退化严重程度连续调整各专家的贡献比例。

#### 1.3 相对于扩散模型基座

本文选择 **Flux-Kontext**（Batifol et al., 2025）作为扩散骨干，而非更常见的 Stable Diffusion 系列。这一选择具有战略意义：Flux-Kontext 提供了更强的上下文理解与生成先验，为 VLM 生成的增强提示提供了更高质量的“画布”。同时，本文仅对 K/V 矩阵进行 LoRA 适应（而非全参数微调或 QKV 全适应），保留 Q 矩阵冻结以维持预训练注意力的结构完整性——这一设计选择在 Table 5 的消融中得到了验证。

### 2. 知识库定位与核心改变槽位

本文的知识贡献可归纳为三个“改变槽位”（changed slots），每个槽位对应一个从基线到本文方法的关键转变：

| 槽位 | 基线值 | 本文值 | 证据锚点 |
|------|--------|--------|----------|
| **修复策略** | 顺序调用多个孤立模型或单一“一体式”模型 | 基于 VLM 的动态多专家一次性协同融合 | Abstract, Section 1 |
| **权重分配** | 无动态权重或手动启发式 | DPO 优化的 MLP 分支基于 VLM 特征分配连续权重 | Section 3.2 |
| **LoRA 适应范围** | 标准 LoRA 适应 Q、K、V 或全参数微调 | 仅适应 K 和 V 矩阵，保留 Q 冻结以维持注意力结构 | Section 3.3 |

这三个槽位共同构成了“VLM 编排 + 动态专家融合”的技术框架。其中，修复策略的改变是架构级创新，权重分配的改变是优化机制创新，LoRA 适应范围的改变是工程实现创新。三者的因果联动关系为：VLM 代理诊断退化类型与严重程度（意图理解）→ DPO 优化的 MLP 分支输出感知最优权重（权重分配）→ 仅 K/V 适应的专家 LoRA 按权重合并到扩散骨干（高效融合）。

### 3. 适用边界

基于论文提供的实验证据，本文方法的适用边界可归纳如下：

**已验证有效的场景**：
- 单一退化修复（Real-1000 Group 1）：PSNR 22.90，显著优于所有基线。
- 双重退化修复（Real-1000 Group 2）：PSNR 21.10，较 AutoDIR 提升 +2.31 dB。
- 三重退化修复（Real-1000 Group 3）：Table 1 报告了竞争性结果。
- 零样本泛化：所有评估均在 zero-shot 设定下完成，方法未在 Real-1000 上微调。
- 跨数据集泛化：在 MiO100 Group C 上同样取得竞争性结果（PSNR 19.85，Table 3）。

**可能受限的场景**（需手动验证）：
- 论文未报告在超过三种退化同时耦合场景下的性能，专家库的扩展性边界尚不明确。
- 专家 LoRA 的训练依赖于特定退化类型的配对数据集（Table 2），对于训练集中未覆盖的退化类型（如极端天气退化、医学图像退化），方法的泛化能力缺乏直接证据。
- VLM 代理基于 Qwen2.5-VL-72B，其意图理解能力受限于该 VLM 的视觉-语言对齐质量。在用户指令高度模糊或矛盾时，代理可能产生次优的修复计划。

### 4. 局限与开放问题

论文明确指出的开放问题（来自 Section 5 或结论部分）包括：

1. **专家库扩展**：未来可扩展专家“笔”库（expert pencil library），以支持更多类型的退化。当前专家覆盖范围受限于训练数据，扩展时需要为每种新退化类型收集高质量配对数据并独立训练 LoRA 专家。

2. **局部区域级融合**：当前方法在全局图像级别分配统一权重，可探索 VLM 在局部、区域级专家融合中的作用——例如，对图像的不同区域（前景/背景、高光/阴影）分配不同的专家权重组合。

3. **偏好数据规模**：DPO 权重分配分支的性能依赖于人类偏好数据的质量和规模。扩大人类偏好数据集有望提高对分布外退化组合的鲁棒性。

4. **感知质量验证**：尽管定量指标（PSNR、LPIPS、DISTS、NIQA、MANIQA、CLIPIQA、MUSIQ）全面占优，论文建议进行全面的用户研究以进一步验证感知质量——这在摄影后处理这一主观性较强的任务中尤为重要。

**论文未明确讨论但值得关注的潜在局限**：

- **计算开销**：VLM 代理（Qwen2.5-VL-72B）的推理成本远高于轻量级退化检测器。在实时或资源受限场景下，这可能成为瓶颈。论文未报告端到端推理延迟。
- **专家冲突**：当多个专家 LoRA 的 K/V 任务向量方向冲突时，加权求和可能导致次优融合。论文未分析不同退化专家之间的任务向量正交性或冲突程度。
- **VLM 幻觉传播**：尽管 Figure 3 展示了本文方法避免了顺序代理的内容幻觉，但 VLM 代理本身的诊断错误（如误判退化类型或严重程度）仍可能通过权重分配分支传播到最终修复结果。论文未报告 VLM 代理的诊断准确率。

### 5. 在更大知识谱系中的位置

从更宏观的视角看，本文工作可被视为 **“基础模型 + 轻量级专家适配”范式**在图像修复领域的成功实践。这一范式在 NLP 领域（如 MoE-LLM、LoRA-MoE）已有广泛探索，但在视觉修复任务中，本文率先将其与 VLM 代理的意图理解能力相结合，形成了“感知-决策-执行”的闭环系统。

与同期工作 **Qwen-Image**（Wu et al., 2025）相比，本文方法不追求端到端的多模态生成统一，而是选择在预训练扩散模型之上构建灵活的专家适配层——这种“插件式”设计在保持基础模型泛化能力的同时，赋予了系统针对特定退化的精准修复能力，体现了模块化与端到端两种技术路线的不同权衡。

## 原文 PDF

![[paperPDFs/CVPR_2026/Beyond_Sequential_Tools_A_Unified_VLM_Agent_System_for_Photographic_Post_Processing_via_Dynamic_Multi_Expert_Fusion.pdf]]
