---
title: "Optimal Sparsity of Mixture-of-Experts Language Models for Reasoning Tasks"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/Optimal_Sparsity_of_Mixture_of_Experts_Language_Models_for_Reasoning_Tasks.pdf
openreview_forum_id: XFw2EPRUUR
aliases:
- FTM
- OSMELMRT
tags:
- ICLR_2026
- topic/optimization_theory_probabilistic
- topic/optimization_theory_probabilistic/learning_theory
core_operator: "活跃参数数量（通过top-k路由控制）与总参数数量的组合，即稀疏度（1 - top-k/Experts），以及每参数训练令牌数（TPP），共同决定了推理性能。具体而言，活跃FLOPs（由top-k和模型宽度决定）在相同预训练损失下直接影响推理准确率；TPP在约20时使推理性能达到峰值。这两个因素共同定义了MoE的最优稀疏度。"
primary_logic: "在固定计算预算下，最优稀疏度具有任务依赖性：记忆任务（如TriviaQA, HellaSwag）倾向于更高的稀疏度（更多总参数），而推理任务存在一个最优稀疏度区间，在总参数过多或过少时性能下降。这一倒U型关系不受强化学习后训练（GRPO）或测试时计算扩展的影响，表明预训练阶段的稀疏度选择对推理能力至关重要。因此，活跃FLOPs应被视为评估MoE模型推理潜力的主要指标，而非仅依赖预训练损失。"
claims:
- "增加总参数（通过增加专家数）可以降低预训练损失，但GSM8K任务损失在超过一定总参数后反而上升。"
- "在固定活跃参数下，对于GSM8K和GSM-Plus，当活跃参数较大时，更密集的模型（低稀疏度）表现优于更稀疏的模型（高稀疏度），即最优稀疏度向密集方向偏移。"
- "推理任务（GSM8K, GSM-Plus, HumanEval, MBPP）的准确率在总令牌每参数（TPP）约20时达到峰值，而记忆任务（TriviaQA, HellaSwag）随TPP降低（即更多参数）单调提升。"
- "无论是通过GRPO进行后训练，还是通过自一致性（Self-Consistency）增加测试时计算，都无法消除因总参数增加（稀疏度提高）导致的GSM8K性能下降这一倒U型关系。"
---

# Optimal Sparsity of Mixture-of-Experts Language Models for Reasoning Tasks

> [!tip] 核心洞察
> 在固定计算预算下，最优稀疏度具有任务依赖性：记忆任务（如TriviaQA, HellaSwag）倾向于更高的稀疏度（更多总参数），而推理任务存在一个最优稀疏度区间，在总参数过多或过少时性能下降。这一倒U型关系不受强化学习后训练（GRPO）或测试时计算扩展的影响，表明预训练阶段的稀疏度选择对推理能力至关重要。因此，活跃FLOPs应被视为评估MoE模型推理潜力的主要指标，而非仅依赖预训练损失。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 面向推理任务的混合专家语言模型的最优稀疏性 |
| 英文题名 | Optimal Sparsity of Mixture-of-Experts Language Models for Reasoning Tasks |
| 会议/期刊 | ICLR 2026 (Oral) |
| Links | [paper](https://openreview.net/forum?id=XFw2EPRUUR); [GitHub](https://github.com/rioyokotalab/optimal-sparsity) |
| Topic | #topic/optimization_theory_probabilistic #topic/optimization_theory_probabilistic/learning_theory |
| Method | 基于活跃FLOPs与每参数令牌数（TPP）的MoE最优稀疏度选择原则 |
| Dataset |  |

## 概述

### 问题背景

混合专家（Mixture-of-Experts, MoE）架构已成为大语言模型高效扩展的主流范式。其核心思想是在每个Transformer层中维护多个前馈网络（专家），但通过top-k路由仅激活其中少数几个，从而以较低的活跃计算成本换取更大的总参数容量。MoE的稀疏度定义为 $sparsity = 1 - \frac{Top\text{-}k}{Experts}$，即非活跃参数占总参数的比例。

传统的模型缩放定律表明，增加总参数（通过提高稀疏度或扩大模型宽度）能够持续降低预训练损失。然而，本文发现这一规律在推理任务上出现根本性断裂：**预训练损失与推理能力之间存在与稀疏度相关的非单调鸿沟**。具体而言，增加总参数虽然能不断降低预训练损失，但数学推理（GSM8K, GSM-Plus）和代码生成（HumanEval, MBPP）等任务的任务损失和准确率呈现先改善后恶化的倒U型趋势，而记忆类任务（TriviaQA, HellaSwag）则保持单调改善。这意味着单纯追求更低的预训练损失并不能自动提升推理性能。

### 核心发现

本文的核心发现可概括为以下几点：

1. **推理任务的倒U型缩放规律**：在固定活跃参数下，随着总参数增加（稀疏度提高），推理任务的性能先上升后下降，存在一个最优稀疏度区间。当活跃参数较大时，最优配置甚至向更密集的模型方向偏移。

2. **活跃FLOPs作为推理能力的关键指标**：在相同预训练损失下，活跃FLOPs（由top-k和模型宽度共同决定）直接影响推理准确率。推理任务对计算与数据的分配更为敏感，活跃FLOPs应被视为评估MoE模型推理潜力的主要指标，而非仅依赖预训练损失。

3. **每参数令牌数（TPP）的最优值**：推理任务的准确率在总令牌每参数（TPP）约20时达到峰值，而记忆任务随TPP降低（即更多参数）单调提升。这表明推理任务对数据-参数的配比有更严格的要求。

4. **后训练与测试时计算的局限**：无论是通过GRPO进行强化学习后训练，还是通过自一致性（Self-Consistency）增加测试时计算，都无法消除因稀疏度选择不当导致的推理性能下降。倒U型关系在预训练阶段即已固化。

### 方法定位

本文并非提出新的MoE架构或训练算法，而是通过系统性的受控实验，揭示了MoE稀疏度与推理能力之间的定量关系。研究基于Mixtral架构，在125B令牌的混合语料上训练了覆盖不同宽度（$d \in \{512, 1024, 2048\}$）、专家数（$E \in \{8, 16, 32\}$）和top-k（$k \in \{2, 4, 8, 16\}$）的模型家族，并在记忆基准（TriviaQA, HellaSwag）和推理基准（GSM8K, GSM-Plus, HumanEval, MBPP）上进行系统评估。通过分析活跃FLOPs和TPP两个关键轴，本文为MoE模型在推理任务上的稀疏度选择提供了原则性指导。

### 主要结果概览

- **预训练损失与任务损失的背离**（Figure 1, 2）：训练和验证损失随总参数增加而持续下降，但GSM8K和GSM-Plus的任务损失在超过一定总参数阈值后反而上升，呈现U型曲线。
- **准确率的非单调趋势**（Figure 3）：通过增加专家数扩展总参数时，GSM8K准确率随预训练损失降低先升后降，而TriviaQA和HellaSwag准确率单调提升。
- **稀疏度对推理任务的强影响**（Figure 4, 5）：记忆任务的错误率几乎完全由预训练损失决定，与稀疏度无关；而推理任务的错误率对稀疏度高度敏感。在固定活跃参数下，推理任务的最优稀疏度随活跃参数增大而向密集方向偏移。
- **TPP的峰值效应**（Figure 7）：推理任务在TPP ≈ 20时性能最优，参数过多或过少均导致性能下降；记忆任务则随参数增加单调改善。
- **代码生成的相似规律**（Figure 8）：HumanEval和MBPP表现出与数学推理一致的倒U型关系，验证了结论在代码生成任务上的泛化性。
- **后训练与TTC的无效性**（Figure 6）：GRPO和自一致性扩展虽能整体提升性能，但无法消除稀疏度带来的性能差异，倒U型关系依然存在。

### 局限与开放问题

本文的实验均在125B令牌语料上完成，接近Chinchilla最优，但更大规模语料下推理任务的最优稀疏度可能向更稀疏配置移动。此外，实验仅基于Mixtral架构，未探索QK-norm、共享专家等最新变体，结论的跨架构泛化性有待验证。开放问题包括：万亿令牌级别下最优TPP和稀疏度的变化规律、纯逻辑推理任务上的定量关系、以及能否设计动态调整稀疏度的预训练策略以兼顾记忆与推理能力。

## 背景与动机

### 缩放定律在MoE推理任务中的失效

大语言模型的缩放定律（Scaling Laws）揭示了模型性能与参数规模、训练数据量之间的幂律关系，这一规律为密集模型的资源分配提供了可靠指导。然而，当模型架构从密集转向混合专家（Mixture-of-Experts, MoE）时，传统的缩放定律在推理任务上出现了系统性失效。

具体而言，MoE模型通过稀疏激活机制——仅激活部分专家而非全部参数——实现了在固定计算预算下大幅增加总参数规模的能力。其稀疏度定义为：

$$sparsity = 1 - \frac{Top\text{-}k}{Experts}$$

直观上，增加总参数（通过提高稀疏度）应当持续降低预训练损失，进而提升下游任务性能。这一预期在记忆密集型任务（如TriviaQA、HellaSwag）上确实成立：预训练损失越低，任务准确率越高，且该关系对稀疏度不敏感。但在数学推理（GSM8K、GSM-Plus）和代码生成（HumanEval、MBPP）等推理任务上，情况截然不同——任务损失和准确率随总参数增加呈现**倒U型**变化：先改善后恶化，与预训练损失的单调下降趋势形成鲜明鸿沟。

### 核心矛盾：预训练损失与推理能力的非单调关系

这一矛盾的本质在于，预训练损失的降低并不能自动转化为推理能力的提升。实验表明，当预训练损失低于某个阈值后，GSM8K和GSM-Plus的任务损失反而开始上升（Figure 2）。这意味着，单纯追求更低的预训练损失——无论是通过扩大总参数还是增加训练计算——都可能导致推理性能的倒退。

该现象揭示了MoE模型中**预训练目标与推理能力之间存在与稀疏度相关的非单调鸿沟**。传统的“预训练损失越低越好”的缩放范式在推理任务上不再适用，需要引入新的分析维度来理解这一偏差。

### 本文动机与分析框架

针对上述问题，本文系统性地解构了MoE稀疏度对推理性能的影响机制。核心研究动机在于回答：**在固定计算预算下，MoE模型是否存在一个最优稀疏度，能够最大化推理任务的性能？**

为此，本文引入了两个关键分析维度：

1. **活跃FLOPs（Active FLOPs）**：即每次前向传播中实际参与计算的浮点运算量，由活跃参数数量和模型宽度共同决定。在相同预训练损失下，活跃FLOPs直接影响推理准确率，应被视为评估MoE模型推理潜力的主要指标。

2. **每参数训练令牌数（TPP, Total Tokens per Parameter）**：即训练数据总量与总参数规模的比值。该指标刻画了每个参数获得的“学习机会”密度，对推理性能具有非单调影响——在TPP约20时达到峰值。

通过这两个维度，本文旨在建立MoE推理任务的最优稀疏度选择原则，为后续的MoE架构设计与训练资源配置提供理论指导。

## 核心创新

本文的核心创新并非提出一个新的模型架构或训练算法，而是**发现并系统刻画了混合专家（MoE）语言模型中稀疏性与推理能力之间的非单调关系**，并据此提出了面向推理任务的MoE最优稀疏度选择原则。

### 1. 发现预训练损失与推理能力的“倒U型”鸿沟

传统模型缩放定律的核心假设是：预训练损失的下行能单调地转化为下游任务性能的提升。本工作首次系统性地证明，这一假设在MoE模型的推理任务上**失效**。

具体而言，当通过增加专家数（$E$）来扩大模型总参数量时：
- **预训练损失**持续下降（Figure 1）；
- **记忆型任务**（TriviaQA、HellaSwag）的任务损失和准确率也随之单调改善；
- **推理型任务**（GSM8K、GSM-Plus、HumanEval、MBPP）的任务损失却呈现**U型曲线**——预训练损失降至某一阈值后，任务损失反而上升，准确率下降（Figure 2, Figure 3）。

这一发现揭示了**预训练损失与推理能力之间存在与稀疏度相关的非单调鸿沟**，单纯依靠预训练损失来指导MoE模型的缩放决策，会严重误导推理任务的性能预期。

### 2. 提出双轴分析框架：活跃FLOPs与每参数令牌数（TPP）

为解释上述鸿沟，论文将性能差异归因于两个关键控制变量：

- **活跃FLOPs**：由模型宽度（$d$）和top-k路由共同决定。在相同预训练损失下，更高的活跃FLOPs（更大的top-k或更宽的模型）直接带来更好的推理准确率（Figure 4, Figure 5）。这表明**活跃FLOPs应被视为评估MoE推理潜力的主要指标**，而非仅依赖总参数量或预训练损失。

- **每参数令牌数（TPP, Total Tokens per Parameter）**：即训练令牌总量与总参数量的比值。推理任务的性能在TPP ≈ 20时达到峰值，TPP过高（参数过少）或过低（参数过多）均导致性能下降；而记忆型任务的性能随TPP降低（参数增加）单调提升（Figure 7）。

### 3. 最优稀疏度的任务依赖性

基于上述双轴分析，论文提炼出核心原则：**在固定计算预算下，最优稀疏度具有任务依赖性**。

- 对于**记忆型任务**，更高的稀疏度（更多总参数、更少活跃参数）始终有利，因为这类任务“参数饥渴”，需要大量参数存储知识。
- 对于**推理型任务**，存在一个最优稀疏度区间。当活跃参数规模较小时，提高稀疏度可改善性能；但当活跃参数规模增大后，更密集的配置（低稀疏度）反而表现更优（Figure 5, Figure 8）。这一倒U型关系在数学推理和代码生成任务上均成立。

### 4. 稀疏度效应的不可逆性

论文进一步证明，由预训练阶段稀疏度选择不当造成的推理性能损失，**无法通过后训练或推理时计算弥补**：

- **GRPO强化学习后训练**：在GSM8K或MATH500上微调后，模型整体性能提升，但稀疏度导致的性能下降趋势保持不变（Figure 6）。
- **测试时计算扩展（Self-Consistency）**：使用27-128次采样进行自一致性解码，同样无法消除倒U型关系（Figure 6）。

这一发现将稀疏度选择的重要性从单纯的推理效率问题，提升为**影响推理能力上限的预训练结构决策**。

## 整体框架

本工作构建了一套系统性的实验流水线，旨在揭示混合专家（MoE）语言模型中稀疏度与推理能力之间的非单调关系。整体框架围绕“预训练—评估—干预—验证”四个阶段展开，核心目标是分离出影响推理任务性能的关键控制变量：**活跃FLOPs**与**每参数令牌数（TPP）**。

### 流水线总览

整个实验流水线由以下模块串联而成：

1. **MoE预训练模块**：在125B令牌的混合语料（构成见Table 1）上，训练一系列基于Mixtral架构的模型。通过扫描三个架构超参数——模型宽度 $d \in \{512, 1024, 2048\}$、专家数 $E \in \{8, 16, 32, 64\}$ 以及top-k路由值 $k \in \{2, 4, 8, 16\}$——生成覆盖不同稀疏度（$1 - \frac{k}{E}$）和活跃参数规模的模型族。训练使用AdamW优化器，峰值学习率 $4\times10^{-4}$，2k步线性预热后余弦衰减，权重衰减0.1，并联合优化交叉熵损失、负载均衡损失和路由器z-损失。

2. **下游任务评估模块**：对每个预训练模型（含中间检查点）在两类基准上计算任务损失和准确率——**记忆任务**（TriviaQA, HellaSwag）和**推理任务**（GSM8K, GSM-Plus, HumanEval, MBPP）。该模块的输出是连接预训练损失与下游性能的关键桥梁，直接暴露了传统缩放定律的失效点。

3. **干预模块**：为检验倒U型关系的鲁棒性，引入两种后干预手段：
   - **GRPO后训练**：在GSM8K或MATH500训练集上使用GRPO算法对预训练模型进行强化学习微调。
   - **测试时计算扩展（TTC）**：采用自一致性解码（27-128次独立采样）增加推理阶段的计算量。

4. **消融与鲁棒性验证模块**：通过一系列控制实验排除混淆因素，包括：移除预训练语料中的GSM8K及其合成衍生数据、扫描学习率与初始化尺度、增加模型深度至32层、以及将训练令牌预算从125B扩展至1T。

### 输入输出流

- **输入**：固定规模的预训练语料（125B tokens）、架构超参数配置 $(d, E, k)$、训练超参数（学习率、权重衰减等）。
- **中间输出**：各检查点的预训练损失/验证损失、各下游基准的任务损失与准确率。
- **最终分析维度**：以**活跃FLOPs**和**TPP**为横轴，以任务损失/准确率为纵轴，刻画稀疏度-性能的非单调曲面。

### 关键控制逻辑

流水线的设计围绕一个核心因果旋钮展开：**在固定计算预算下，活跃参数数量（由宽度 $d$ 和 top-k 共同决定）与总参数数量（由 $E$ 决定）的组合，即稀疏度，决定了推理性能的走向**。通过保持活跃FLOPs不变而仅改变稀疏度配置（IsoFLOP分析），或固定活跃参数而改变密度（$k/E$ 比率），流水线能够解耦总参数规模与活跃计算量对推理能力的独立贡献。

## 核心模块与公式推导

### MoE层的前向计算

本文采用基于**Mixtral**架构（Jiang et al., 2024）的稀疏混合专家模型，核心计算流程如下。

**路由器得分计算**：对于输入令牌表示 $\mathbf{x}$，路由器通过线性变换产生每个专家的原始得分：

$$\mathbf{s} = \mathbf{x}^{\top} \mathbf{W}_{\mathrm{router}}$$

其中 $\mathbf{W}_{\mathrm{router}}$ 为路由器的权重矩阵，$\mathbf{s}$ 为所有专家的得分向量。

**门控权重**：采用top-k路由机制，仅保留得分最高的 $k$ 个专家，对其得分进行softmax归一化，其余专家权重置零：

$$g(\mathbf{x})_i = \frac{\exp(s_i)}{\sum_{j \in \mathcal{K}} \exp(s_j)} \text{ if } i \in \mathcal{K}, \text{ else } 0$$

其中 $\mathcal{K}$ 为选中的top-k专家索引集合。

**MoE层输出**：被选中专家的前馈网络（FFN）输出按门控权重加权求和：

$$\mathbf{y} = \sum_{i=1}^{n} g(\mathbf{x})_i \mathrm{FFN}(\mathbf{x})_i$$

其中 $n$ 为专家总数，$\mathrm{FFN}(\mathbf{x})_i$ 为第 $i$ 个专家的输出。每个专家内部采用**SwiGLU**激活函数，层间使用**RMSNorm**进行归一化，位置编码采用**旋转位置嵌入**（RoPE）。路由采用无丢弃（dropless）的token-choice top-k策略。

### 稀疏度定义

MoE模型的稀疏度定义为非活跃参数占总参数的比例：

$$\mathrm{sparsity} = 1 - \frac{\text{Top-}k}{\text{Experts}}$$

其中 $\text{Top-}k$ 为每令牌激活的专家数，$\text{Experts}$ 为每层的专家总数。该指标直接反映了模型在推理时参数利用的稀疏程度，是本文调控的核心变量之一。

### 训练损失函数

总训练损失由三部分加权组合而成：

$$\mathcal{L} = \mathcal{L}_{\mathrm{CE}} + \alpha \mathcal{L}_{\mathrm{LB}} + \beta \mathcal{L}_{\mathrm{RZ}}$$

- $\mathcal{L}_{\mathrm{CE}}$：标准的交叉熵语言建模损失。
- $\mathcal{L}_{\mathrm{LB}}$：负载均衡损失（load-balancing loss），用于鼓励令牌在各专家间均匀分配，防止路由坍塌。
- $\mathcal{L}_{\mathrm{RZ}}$：路由器z-损失（router z-loss），用于稳定路由器训练，防止得分漂移。
- $\alpha, \beta$：分别为负载均衡损失和z-损失的权重系数。

### 关键控制变量

本文通过扫描三个架构超参数来系统性地调控模型配置：

- **模型宽度** $d \in \{512, 1024, 2048\}$：决定隐藏表示的维度，直接影响每令牌的活跃FLOPs。
- **专家数** $E \in \{8, 16, 32, 64\}$：控制总参数规模。
- **top-k** $k \in \{2, 4, 8, 16\}$：决定每令牌激活的专家数量，与 $E$ 共同决定稀疏度。

此外，**每参数训练令牌数**（Total Tokens per Parameter, TPP）作为连接训练预算与模型规模的关键指标，定义为训练语料总令牌数除以模型总参数数。该指标在后续分析中被证明是决定推理任务性能峰值位置的核心变量。

## 实验与分析

### 核心发现：预训练损失与推理能力的非单调鸿沟

本研究通过训练一系列不同宽度（d ∈ {512, 1024, 2048}）、专家数（E ∈ {8, 16, 32, 64, 128}）和top-k（k ∈ {2, 4, 8, 16}）的Mixtral架构MoE模型，在125B令牌的混合语料上进行预训练，系统考察了稀疏度对下游任务性能的影响。实验揭示了一个关键瓶颈：**传统的模型缩放定律在MoE推理任务上失效**。

Figure 1 展示了这一核心矛盾：随着总参数量的增加，训练损失和验证损失持续下降，符合标准缩放定律的预期；然而，GSM8K数学推理任务的任务损失在总参数量超过某一阈值后反而上升。这一非单调趋势在Figure 2中进一步细化——对于TriviaQA和HellaSwag这类记忆密集型任务，任务损失随预训练损失单调下降；但对于GSM8K和GSM-Plus，任务损失与预训练损失之间呈现**U型曲线**：预训练损失降至某一点后，继续降低反而导致任务损失回升。

![[assets/figures/papers/paper_list_l25_https_openreview_net_forum_id_XFw2EPRUUR/figures/002_Figure_1.jpg]]
*Figure 1: Although training and validation loss decrease as the total number of parameters grows, the task loss on GSM8K can sometimes worsen with larger models. Training and validation losses steadily decrease as total or active parameters increase. The HellaSwag task loss follows this scaling trend, whereas GSM8K task loss worsens once total parameters exceed a threshold. Within each fixed top-k group, moving right on the x-axis corresponds to increasing sparsity (because total experts E increases while k remains fixed), so the right-hand task-loss panels implicitly reflect the same sparsity ordering shown explicitly in Figure 5*

Figure 3 从准确率角度印证了上述发现。当通过增加专家数来扩展总参数时（固定宽度和top-k），TriviaQA和HellaSwag的准确率随预训练损失降低而稳定提升，而GSM8K的准确率则呈现非单调变化——预训练损失的进一步降低并不总能带来准确率提升，甚至可能导致性能退化。

![[assets/figures/papers/paper_list_l25_https_openreview_net_forum_id_XFw2EPRUUR/figures/004_Figure_3.jpg]]
*Figure 3: Downstream accuracy when scaling total parameters via expert count with width and top-k fixed. TriviaQA and HellaSwag exhibit steadily improving accuracy as pre-training loss decreases, whereas GSM8K shows a non-monotonic trend: further reductions in pre-training loss do not always improve accuracy and can even degrade performance*

### 稀疏度对任务性能的分化效应

Figure 4 通过变化稀疏度（$1 - \frac{\text{top-k}}{\text{Experts}}$）并绘制预训练损失与基准错误率的关系，揭示了任务类型对稀疏度的敏感性差异。对于TriviaQA和HellaSwag，错误率紧密跟随训练损失变化，对稀疏度本身不敏感——不同稀疏度配置下，只要达到相同的预训练损失，就能获得相近的任务性能。然而，对于推理任务（GSM8K、GSM-Plus），错误率表现出**对稀疏度的强依赖性**：即使预训练损失相同，不同稀疏度配置下的推理性能也存在显著差异。

![[assets/figures/papers/paper_list_l25_https_openreview_net_forum_id_XFw2EPRUUR/figures/005_Figure_4.jpg]]
*Figure 4: Effect of sparsity on performance across different tasks We vary sparsity (1 - topk/Experts) and plot the relationship between pre-training loss and benchmark error rate, including intermediate checkpoints. For TriviaQA and HellaSwag, the error rate clearly tracks training loss and is largely insensitive to sparsity. In contrast, reasoning skills exhibit a strong dependence of error rate on sparsity*

这一发现指向了一个关键的因果机制：**活跃FLOPs是评估MoE模型推理潜力的主要指标**，而非仅依赖预训练损失。在固定活跃参数数量下，更高稀疏度（更低密度）的模型在活跃参数较小时表现更优；但当活跃参数增大时，GSM8K和GSM-Plus的最优配置向更密集的模型偏移（Figure 5）。这意味着推理任务存在一个最优稀疏度区间，过于稀疏或过于密集都会损害性能。

![[assets/figures/papers/paper_list_l25_https_openreview_net_forum_id_XFw2EPRUUR/figures/006_Figure_5.jpg]]
*Figure 5: At fixed active parameter counts, higher sparsity (lower density) consistently improves performance, but at larger active parameter counts, GSM8K and GSM-Plus shift their optima back toward dense models. Task loss (top row) and Accuracy (bottom row) against the ratio of active experts k to total experts E for a fixed active parameter budget. In the left two tasks (TriviaQA, HellaSwag), increasing sparsity consistently lowers task loss and raises accuracy across all active parameter budgets, in contrast, in the right two tasks (GSM8K, GSM-Plus), once active parameter counts become large, this trend reverses and denser models begin to outperform their sparser counterparts. Dashed segments mar...*

### 每参数令牌数（TPP）的关键作用

Figure 7 展示了总令牌每参数（Total Tokens per Parameter, TPP）对不同任务性能的影响，这是本研究揭示的第二个关键控制变量。对于TriviaQA和HellaSwag，性能随TPP降低（即总参数增加）单调提升，表明记忆任务是“参数饥渴型”的。相反，对于推理任务（GSM8K、GSM-Plus），性能在**TPP约20时达到峰值**，当TPP偏离这一最优值（无论是因参数过多导致TPP过低，还是因参数过少导致TPP过高），性能都会下降。

![[assets/figures/papers/paper_list_l25_https_openreview_net_forum_id_XFw2EPRUUR/figures/008_Figure_7.jpg]]
*Figure 7: d=512, k=2 d=512, k=8 d=1024, k=2 d=1024, k=8 d=2048, k=2 d=2048, k=8 d=512, k=4 d=512,k=16 d=1024,k=4 d=1024,k=16 d=2048, k=4 d=2048, k=16 Figure 7: Effect of TPP on performance across different tasks. For TriviaQA and HellaSwag, performance improves as the number of parameters increases. In contrast, for reasoning skills, performance deteriorates when the number of parameters becomes too large, indicating that there exists an optimal total tokens per paramete ratio for these tasks. Even at fixed TPP, models with larger top-k values consistently outperform those with smaller top-k on reasoning tasks*

这一发现揭示了推理任务对数据与计算分配的敏感性：在固定训练预算下，增加稀疏度会将令牌分散到更多专家上，导致每个专家数据不足（data-starved），从而损害推理能力的习得。推理任务本质上是“数据饥渴型”的，需要足够的每参数训练强度。

### 后训练与测试时计算的局限性

一个关键问题是：后训练或测试时计算能否弥补预训练阶段稀疏度选择带来的推理性能损失？Figure 6 给出了否定答案。无论是通过GRPO算法在GSM8K训练集上进行强化学习微调，还是通过自一致性（Self-Consistency）解码（27次独立采样）增加测试时计算，**都无法消除因总参数增加导致的GSM8K性能下降这一倒U型关系**。虽然两种方法都能带来整体性能提升，且提升幅度随模型规模扩大而增加，但训练损失与任务准确率之间的非单调权衡关系依然存在。

这一发现具有重要的实践意义：预训练阶段的稀疏度选择对推理能力的影响是根本性的，无法通过后训练或推理时的计算扩展来完全修正。因此，在MoE模型设计阶段就需要针对目标任务类型选择合适的稀疏度配置。

### 代码生成任务的验证

为检验结论的跨任务泛化性，研究在代码生成基准上进行了验证。Figure 8 显示，HumanEval和MBPP展现出与数学推理任务相似的模式：在固定活跃参数数量下，当活跃参数较小时，更高稀疏度持续提升性能；但当活跃参数较大时，最优配置同样向更密集的模型偏移。这与记忆任务（TriviaQA、HellaSwag）的单调趋势形成鲜明对比，表明**推理任务（包括数学推理和代码生成）共享相似的稀疏度敏感性机制**。

![[assets/figures/papers/paper_list_l25_https_openreview_net_forum_id_XFw2EPRUUR/figures/009_Figure_8.jpg]]
*Figure 8: At fixed active parameter counts, higher sparsity (lower density) consistently improves performance, but at larger active parameter counts, HumanEval and MBPP shift their optima back toward dense models. Accuracy against the ratio of active experts k to total experts E for a fixed active parameter budget. In the left two tasks (TriviaQA, HellaSwag), increasing sparsity consistently raises accuracy across all active parameter budgets, in contrast, in the right two tasks (HumanEval, MBPP), once active parameter counts become large, this trend reverses and denser models begin to outperform their sparser counterparts. Dashed segments mark the inverse-scaling regime that starts at the black circ...*

### 关键消融研究

**训练令牌预算扩展**：将训练令牌从125B扩展到1T（固定d=2048, E=16, k=2），TriviaQA和HellaSwag性能大幅提升，但GSM8K和GSM-Plus改善微弱（Table 4）。这表明单纯增加训练数据量无法从根本上改变推理任务对稀疏度的敏感性，最优TPP的存在可能在不同数据规模下保持稳健。

**数据去偏**：移除预训练语料中的GSM8K及其合成衍生数据后，GSM8K上稀疏度相关的性能趋势保持不变（Figure 15, 16）。这排除了数据泄露或任务特定数据偏差对倒U型关系的解释。

**架构变体**：增加模型深度（32层）并未改变TPP对推理性能的非单调影响模式（Figure 24），表明这一现象并非浅层网络的特殊产物。

**优化超参数**：较低的预训练学习率和较小的初始化尺度倾向于提高推理任务的泛化性能，即使预训练损失相当（Figure 25）。这暗示推理能力的习得对优化动态更为敏感，需要更谨慎的超参数选择。

### 失败模式与局限性

1. **大规模语料下的最优稀疏度偏移**：所有模型均在125B令牌上训练，接近Chinchilla最优。在更大规模语料（如万亿令牌级别）下，推理任务的最优稀疏度可能向更稀疏配置移动，当前结论的外推需要谨慎。

2. **架构泛化性未验证**：实验仅基于Mixtral架构，未探索QK-norm、共享专家等最新架构变体。结论的跨架构稳健性有待进一步检验。

3. **规模覆盖有限**：未对数十亿活跃参数级别的模型进行验证，top-k仅覆盖至16，更大规模的稀疏度效应尚不明确。

4. **推理任务的细粒度分类缺失**：研究将数学推理和代码生成归为“推理任务”，但未区分纯粹逻辑推理、符号推理等子类型，不同类型的推理能力可能对稀疏度有不同的最优区间。

### 补充图表

![[assets/figures/papers/paper_list_l25_https_openreview_net_forum_id_XFw2EPRUUR/figures/001_Figure.jpg]]

![[assets/figures/papers/paper_list_l25_https_openreview_net_forum_id_XFw2EPRUUR/figures/003_Figure_2.jpg]]
*Figure 2: For GSM8K and GSM-Plus, once the training loss drops below a certain point, the task loss starts to increase. Results of scaling total parameters by increasing the number of experts, with model width and top-k held constant. For TriviaQA and HellaSwag, the task loss falls monotonically as training loss decreases. By contrast, GSM8K and GSM-Plus show a U-shaped trend: task loss declines with training loss only until a threshold, beyond which further reductions in training loss hurt task performance. That threshold moves lower as active parameter count increases, models with more active parameters achieve a lower optimal task loss. No such active parameters dependence appears for TriviaQA, He...*

![[assets/figures/papers/paper_list_l25_https_openreview_net_forum_id_XFw2EPRUUR/figures/007_Figure.jpg]]
*Figure: d=1024,k=2 d=1024,k=4 d=1024,k=8 d=1024,k=16 before GRPO after GRPO*

![[assets/figures/papers/paper_list_l25_https_openreview_net_forum_id_XFw2EPRUUR/figures/014_Figure.jpg]]

![[assets/figures/papers/paper_list_l25_https_openreview_net_forum_id_XFw2EPRUUR/figures/015_Figure_10.jpg]]
*Figure 10: Comparison of GSM8K accuracy for models fine-tuned with GRPO on different training datasets (left: GSM8K, right: MATH 500). Performance decline is consistently observed across different training datasets*

![[assets/figures/papers/paper_list_l25_https_openreview_net_forum_id_XFw2EPRUUR/figures/016_Figure_11.jpg]]
*Figure 11: GSM8K accuracy of model (d=1024) across different shot counts. Because few shot performance is unstable and dropped significantly for models with a small number of experts, zero shot is used for Test-Time Compute*

## 方法谱系与知识库定位

### 核心贡献与定位

本文的核心贡献在于**揭示了MoE模型在推理任务上存在与稀疏度相关的非单调性能瓶颈**，并提出了以**活跃FLOPs**和**每参数训练令牌数（TPP）**作为评估MoE推理潜力的关键指标。这一发现直接挑战了传统缩放定律中“降低预训练损失即自动提升下游性能”的隐含假设——对于数学推理（GSM8K、GSM-Plus）和代码生成（HumanEval、MBPP）任务，预训练损失与任务准确率之间呈现倒U型关系，而记忆任务（TriviaQA、HellaSwag）则保持单调。

该工作的独特性在于：
- **并非提出新的MoE架构或路由策略**，而是在现有Mixtral架构（Jiang et al., 2024）基础上，通过系统性的稀疏度扫描实验，揭示了一个此前未被充分研究的**任务依赖性缩放规律**。
- 将MoE的推理能力分解为两个可量化的控制变量：活跃FLOPs（由top-k和模型宽度决定）和TPP（总训练令牌/总参数），为MoE的推理导向设计提供了操作化原则。

### 与现有MoE研究的谱系关系

#### 架构与训练基础
本文直接建立在**Mixtral**（Jiang et al., 2024）的架构之上：Transformer骨干网络 + RMSNorm（Zhang & Sennrich, 2019）+ SwiGLU激活（Shazeer, 2020）+ 旋转位置编码（Su et al., 2024），采用dropless token-choice top-k路由。训练损失结合了交叉熵损失、负载均衡损失和路由器z-损失（Zoph et al., 2022; Xue et al., 2024）。这些选择使本文的实验结论直接适用于当前主流的开源MoE范式。

#### 缩放定律研究的延伸与修正
传统缩放定律研究（Hoffmann et al., 2022; Kaplan et al., 2020）主要关注预训练损失与计算量/参数量的关系，隐含假设预训练损失是下游性能的可靠代理。本文通过引入**任务损失**和**任务准确率**作为直接优化目标，揭示了这一假设在MoE推理场景下的断裂。特别是，本文的IsoFLOP分析（3.3节）在固定计算预算下比较不同稀疏度配置，直接回应了“如何在给定计算约束下最优分配参数”这一缩放定律的核心问题，但给出了任务依赖的差异化答案。

#### 与后训练和推理时扩展的关系
本文进一步验证了该非单调瓶颈的鲁棒性：无论是通过**GRPO**进行强化学习微调（3.5节），还是通过**自一致性（Self-Consistency）**扩展测试时计算（27-128次采样），都无法消除因总参数增加导致的推理性能下降。这表明**预训练阶段的稀疏度选择对推理能力具有不可逆的塑造作用**，后训练和推理时扩展只能提升绝对性能，但无法修正稀疏度带来的相对劣势。

### 适用边界与局限

1. **训练语料规模的约束**：所有实验基于125B令牌的混合语料训练，接近Chinchilla最优。尽管消融实验（Table 4, Appendix C.8）显示将训练令牌扩展到1T时记忆任务大幅提升而推理任务改善微弱，但更大规模语料下推理任务的最优TPP和稀疏度可能向更稀疏配置偏移。这一点的定量规律尚不明确。

2. **架构泛化性未验证**：实验仅基于Mixtral架构，未探索QK-norm、共享专家、细粒度专家等最新变体。不同架构下的稀疏度-推理关系可能有所不同，需要跨架构验证。

3. **模型规模覆盖有限**：最大活跃参数仅覆盖d=2048、k=16的配置范围，对于数十亿活跃参数级别的模型，结论的定量外推需谨慎。

4. **任务类型的代表性问题**：推理任务主要覆盖小学数学（GSM8K）和基础代码生成（HumanEval, MBPP），对于更复杂的逻辑推理、多步数学证明或长程代码理解，活跃FLOPs和TPP的定量关系是否仍然成立，尚待验证。

### 开放问题

1. **最优稀疏度的训练动态**：能否设计在预训练过程中动态调整稀疏度的策略——例如前期高稀疏度以快速积累知识，后期降低稀疏度以强化推理能力——从而兼顾记忆与推理？

2. **后训练阶段的稀疏度修正**：既然GRPO无法消除预训练稀疏度带来的推理偏差，是否存在专门针对稀疏度差异的后训练方法（如专家蒸馏、路由重对齐）来弥补这一鸿沟？

3. **推理任务的数据效率机制**：为什么推理任务在TPP≈20时达到峰值？这一数值是否与训练数据的推理密度、专家容量或路由熵有关？其背后的理论机制值得深入探究。

4. **跨模态推理的适用性**：在视觉推理、多模态数学等场景下，MoE的稀疏度-推理关系是否呈现类似规律？活跃FLOPs是否同样可作为跨模态推理能力的统一指标？

## 原文 PDF

![[paperPDFs/ICLR_2026/Optimal_Sparsity_of_Mixture_of_Experts_Language_Models_for_Reasoning_Tasks.pdf]]
