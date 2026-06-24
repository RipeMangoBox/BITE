---
title: "Harder Is Better: Boosting Mathematical Reasoning via Difficulty-Aware GRPO and Multi-Aspect Question Reformulation"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/Harder_Is_Better_Boosting_Mathematical_Reasoning_via_Difficulty_Aware_GRPO_and_Multi_Aspect_Question_Reformulation.pdf
openreview_forum_id: nfURupkdRJ
aliases:
- MDM
tags:
- ICLR_2026
- topic/reinforcement_learning_planning_agents
- topic/reinforcement_learning_planning_agents/deep_rl
core_operator: "将组相对优势的标准化因子由标准差改为平均绝对偏差（MAD），使每个问题的总更新幅度恒定；并采用基于负平均奖励的软权重加权，显式将训练焦点引向更难的问题。"
primary_logic: "GRPO的组相对优势标准化（÷标准差）导致更新幅度与正确率p相关，在p=0.5时最大，抑制了难题的影响；纠正该幅度的不平衡并主动对难题加权，结合多方面答案保持的问题重写，可构建一个“更难数据–更强算法”的协同闭环。"
claims:
- "使用GRAE（标准差归一化）时，每个问题的总更新幅度上限为2G√(p(1-p))，p=0.5时最大，极难或极易的问题更新被压制。"
- "改用MAD归一化的DGAE后，每个问题的总更新幅度恒为G，完全消除与原难度（正确率）的依赖。"
- "DGPO在Qwen2.5-Math-7B上平均基准分达到39.79%，较GRPO提升2.18个百分点。"
- "MQR通过添加故事背景、引入抽象术语、嵌套子问题重写问题，使训练数据难度提升，仅用GRPO训练即达41.04%（+3.43%）。"
---

# Harder Is Better: Boosting Mathematical Reasoning via Difficulty-Aware GRPO and Multi-Aspect Question Reformulation

> [!tip] 核心洞察
> GRPO的组相对优势标准化（÷标准差）导致更新幅度与正确率p相关，在p=0.5时最大，抑制了难题的影响；纠正该幅度的不平衡并主动对难题加权，结合多方面答案保持的问题重写，可构建一个“更难数据–更强算法”的协同闭环。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 越难越好：通过难度感知GRPO和多方面问题改写提升数学推理 |
| 英文题名 | Harder Is Better: Boosting Mathematical Reasoning via Difficulty-Aware GRPO and Multi-Aspect Question Reformulation |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=nfURupkdRJ); [GitHub](https://github.com/AMAP-ML/MathForge) |
| Topic | #topic/reinforcement_learning_planning_agents #topic/reinforcement_learning_planning_agents/deep_rl |
| Method | MathForge（DGPO + MQR） |
| Dataset | AIME24, MATH500, Minerva, Olympiad |

> [!tip] 效果简介
> - AIME24 上，pass@1 (32 runs average) 为 24.58，对比 20.94，变化 +3.64。
> - MATH500 上，pass@1 (4 runs average) 为 79.95，对比 72.20，变化 +7.75。
> - Minerva 上，pass@1 (4 runs average) 为 33.36，对比 27.76，变化 +5.60。

## 概述

### 问题背景

基于强化学习的推理训练（Reinforcement Learning for Verifiable Reasoning, RLVR）在提升大语言模型数学能力方面取得了显著进展，其中 GRPO（Group Relative Policy Optimization）因其无需价值模型的简洁设计而成为主流选择。然而，本文揭示了 GRPO 及其变体存在一个被忽视的结构性缺陷：**其组相对优势估计（GRAE）采用标准差进行标准化，导致不同难度问题的总更新幅度存在隐式不平衡**——中等难度（正确率约 50%）的问题获得最大梯度更新，而更困难但仍可解的问题被系统性压制。与此同时，现有数据增强方法未能系统性地提升问题内在难度，限制了模型向更高推理能力的跃迁。

### 核心洞察

本文的核心洞察可概括为一个“**更难数据–更强算法**”的协同闭环：

1. **算法侧（DGPO）**：将 GRPO 的优势标准化因子从标准差替换为平均绝对偏差（MAD），使每个问题的总更新幅度恒为常数 $G$，从根本上消除与问题难度的依赖关系；同时引入基于负平均奖励的软最大化问题级加权（DQW），显式将训练焦点引向更难的问题。
2. **数据侧（MQR）**：通过添加故事背景、引入抽象术语、嵌套独立子问题三个角度重写原始问题，在保持数学等价性和原始答案的前提下，系统性提升训练数据的难度与多样性。

两者结合构成 **MathForge** 框架，实现了算法对困难样本的有效利用与数据难度持续提升之间的正向循环。

### 方法定位

**MathForge** 在 RLVR 方法谱系中的定位如下：

- **相对于 GRPO**（Shao et al., 2024）：将优势估计从标准差归一化改为 MAD 归一化（DGAE），并增加问题级难度感知加权（DQW），解决了更新幅度随正确率 $p$ 变化（$\propto \sqrt{p(1-p)}$）的隐式偏差。
- **相对于 Dr.GRPO**（Liu et al., 2025a）、**DAPO**（Yu et al., 2025）、**GSPO**（Zheng et al., 2025）等变体：DGPO 的 DGAE 和 DQW 可作为即插即用模块与这些方法协同，实验表明在 DAPO、GSPO、GPG 上叠加 DGPO 均带来一致提升。
- **相对于 GRPO-AD**（Zhang & Zuo, 2025）等难度感知方法：DGPO 从优势估计的数学根源（标准化因子）而非后验重加权入手，纠正更为根本。
- **数据增强方面**：MQR 不同于简单的重复采样或表面改写，通过多角度语义重构提升问题的内在推理难度，且保持答案不变，是专为 RLVR 设计的难度增强策略。

### 主要结果

在 Qwen2.5-Math-7B 模型上，以 MATH 数据集为训练集，MathForge（DGPO + MQR）在六个数学推理基准上的平均得分为 **42.17%**，较 GRPO 基线（37.61%）提升 **+4.56 个百分点**。其中：

| 基准 | GRPO | MathForge | 提升 |
|------|------|-----------|------|
| AIME24 | 20.94 | 24.58 | +3.64 |
| MATH500 | 72.20 | 79.95 | +7.75 |
| Minerva | 27.76 | 33.36 | +5.60 |
| Olympiad | 37.33 | 42.67 | +5.34 |

消融实验进一步验证了各组件的独立贡献：DGAE 单独带来 +0.94% 的提升，DQW 额外贡献 +1.14%，两者合计使 DGPO 较 GRPO 提高 +2.18%；MQR 在 DGPO 基础上再提升 +2.27%，其中子问题重写策略的增益最大（+1.63%）。跨模型尺度（1.5B、3B、7B）和跨模型系列（Qwen2.5-Math、Qwen2.5、DeepSeek-Math）的实验一致表明 MathForge 的最优性，验证了方法的泛化能力。

## 背景与动机

### 数学推理的强化学习范式

大语言模型在数学推理任务上的能力提升，已从监督微调（SFT）转向基于强化学习的后训练阶段。其中，**GRPO**（Group Relative Policy Optimization, Shao et al., 2024）作为一种无需价值模型的强化学习算法，通过组内相对优势估计替代传统 critic 网络，显著降低了训练开销，成为当前数学推理 RLVR（Reinforcement Learning from Verifiable Rewards）的主流范式。

GRPO 的核心操作是对每个问题采样 $G$ 条响应，计算组内标准化后的相对优势，以此驱动策略更新。其优势估计函数 GRAE 采用标准差进行归一化：

$$\hat{A}_{\mathrm{GR},i} = \frac{r_i - \mathrm{mean}(\{r_i\}_{i=1}^G)}{\mathrm{std}(\{r_i\}_{i=1}^G)}$$

这一设计的数学性质决定了其存在一个被忽视的结构性缺陷。

### 核心瓶颈：隐式的难度不平衡

在二值奖励（正确/错误）设定下，GRAE 使得每个问题的**总更新幅度**与正确率 $p$ 紧密耦合。理论分析表明（Theorem 1, Appendix B.3），单个问题所有响应的优势绝对值之和为：

$$\sum_{i=1}^G |\hat{A}_{\mathrm{GR},i}| = 2G\sqrt{p(1-p)}$$

该函数在 $p=0.5$ 时达到最大值 $G$，而在 $p \to 0$ 或 $p \to 1$ 时趋近于 $0$。这意味着：**中等难度的问题获得最大的梯度更新强度，而极难（但仍有至少一条正确响应）或极简单的问题，其训练信号被系统性压制**。在数学推理场景中，真正需要模型突破的恰恰是那些正确率低、难度高的题目，但 GRPO 的标准化机制恰好抑制了对这些题目的学习。

与此同时，现有 GRPO 变体（如 Dr.GRPO、DAPO、GSPO 等）虽然引入了丢弃机制、长度惩罚或重要性采样等改进，但**均未触及这一由标准差归一化引发的难度-更新幅度失衡问题**。此外，在数据层面，现有数据增强策略也未系统性地提升问题内在难度——它们主要关注多样性或数量，而非构建“更难”的训练样本。

### 本文动机：构建“更难数据–更强算法”的协同闭环

针对上述双重缺口，本文提出 **MathForge** 框架，从算法和数据两个维度协同提升数学推理能力：

1. **算法层面**：设计 **DGPO**（Difficulty-Aware Group Policy Optimization），通过两个关键修改纠正 GRPO 的隐式不平衡——
   - 将组优势的标准化因子由**标准差**替换为**平均绝对偏差（MAD）**，使每个问题的总更新幅度恒为 $G$，彻底消除与难度（正确率）的依赖关系（Theorem 2, Appendix B.4）；
   - 引入基于**负平均奖励**的软最大化问题级权重（DQW），显式将训练焦点引向更难的问题。

2. **数据层面**：提出 **MQR**（Multi-Aspect Question Reformulation），在不改变原始答案的前提下，通过添加故事背景、引入抽象术语、嵌套子问题三种策略系统性地增加问题难度，为 RLVR 训练提供更具挑战性的样本。

两者的协同构成了一个正向循环：MQR 提供更难的训练数据，DGPO 确保这些难题获得充分的更新幅度，共同驱动模型在复杂推理任务上的突破。

## 核心创新

本工作提出了 **MathForge** 框架，由两个互补的核心创新构成：**DGPO（难度感知的组策略优化）** 和 **MQR（多方面问题改写）**。二者共同形成一个“更难数据–更强算法”的协同闭环，从根本上解决了 GRPO 系列方法在数学推理强化学习中的隐式瓶颈。

### 瓶颈诊断：GRPO 的难度不平衡

GRPO 及其变体的组相对优势估计（GRAE）使用标准差进行标准化：

$$\hat{A}_{\mathrm{GR}, i} = \frac{r_i - \mathrm{mean}(\{r_i\}_{i=1}^G)}{\mathrm{std}(\{r_i\}_{i=1}^G)}$$

该设计导致一个此前被忽视的隐式不平衡：**每个问题的总更新幅度与正确率 $p$ 严格相关**，其理论上限为 $2G\sqrt{p(1-p)}$（Theorem 1, Eq. 8）。这意味着正确率 $p=0.5$ 的中等难度问题获得最大更新幅度，而极难（$p \to 0$）或极易（$p \to 1$）的问题更新被大幅压制。对于数学推理任务，真正需要模型突破的正是那些仍可解但正确率极低的难题，GRPO 的标准化机制恰恰削弱了对这些问题的学习信号。

### 创新一：DGPO——难度感知的组策略优化

DGPO 通过两个 **changed slots** 纠正上述不平衡：

**（1）优势标准化因子：标准差 → 平均绝对偏差（MAD）**

DGPO 引入难度平衡的组优势估计（DGAE），将标准化因子由标准差替换为 MAD：

$$\hat{A}_{\mathrm{DG}, si} = \frac{r_{si} - \mathrm{mean}(\{r_{si}\}_{i=1}^G)}{\mathrm{MAD}(\{r_{si}\}_{i=1}^G)}, \quad \mathrm{MAD} = \frac{1}{G}\sum_{i=1}^G \left| r_{si} - \mathrm{mean}(\{r_{si}\}_{i=1}^G) \right|$$

这一替换的因果效应是决定性的：MAD 归一化下，每个问题的总更新幅度恒为 $G$（Theorem 2, Eq. 10），**完全消除与原难度（正确率）的依赖**。无论问题是极难还是中等，其参数更新总量保持恒定，确保难题不再被算法隐式忽视。

**（2）问题级加权：均匀加权 → 基于难度的软最大化权重（DQW）**

在纠正幅度的被动不平衡后，DGPO 进一步通过难度感知的问题级加权（DQW）**主动将训练焦点引向更难的问题**。问题 $q_s$ 的难度量化为其所有响应的负平均奖励：

$$D_s = -\mathrm{mean}(\{r_{si}\}_{i=1}^G)$$

权重通过 softmax 分配，温度 $T=2.0$ 在尖锐与平滑之间取得最优平衡：

$$\lambda_s = B_{\mathrm{v}} \cdot \frac{\exp(D_s / T)}{\sum_{s=1}^{B_{\mathrm{v}}} \exp(D_s / T)}$$

消融实验验证了各组件的独立贡献：DGAE 单独带来 0.94% 的平均提升，DQW 额外贡献 1.14%，二者合计使 DGPO 较 GRPO 提升 2.18 个百分点（Table 3）。温度消融进一步证实 $T=2.0$ 为最佳设置——$T=1.0$ 过于尖锐导致训练不稳定，$T=10.0$ 过于平滑退化为近似均匀加权。

### 创新二：MQR——多方面问题改写

现有数据增强方法（如简单的重述或答案扰动）未能系统性增加问题的内在推理难度。MQR 通过三种互补的改写策略，在**严格保持原始答案不变**的约束下，显著提升训练数据的难度和多样性：

- **MQR-Background**：添加故事背景，增加信息噪声和干扰，迫使模型在冗余上下文中提取核心数学结构。
- **MQR-Term**：引入抽象数学术语（如将具体数值替换为符号化表达），提升问题表述的抽象层级。
- **MQR-SubProblem**：嵌套独立子问题，增加推理步骤的链式长度和中间状态的复杂度。

仅使用 GRPO 训练 MQR 增强数据即可达到 41.04% 的平均分（+3.43%），显著优于在原始数据上训练的 GRPO（Table 1）。消融实验表明，子问题重写（Origin+Sub-Problem）的单独贡献最大（+1.63%），而三者组合达到最优（Table 7）。关键的是，MQR 的增益源于数据质量的提升而非数据量的简单增加——四倍原始数据量的重复训练效果不如 MQR（Table 6），确认了“更难数据”的因果作用。

### 协同闭环

MathForge 将 DGPO 与 MQR 结合，构建了一个正反馈循环：MQR 生成更难但可解的问题，DGPO 通过难度平衡的优势估计和显式加权确保这些难题获得充分的训练信号。在 Qwen2.5-Math-7B 上，MathForge 达到 42.17% 的平均基准分（+4.56% over GRPO），在 AIME24（+3.64）、MATH500（+7.75）、Minerva（+5.60）、Olympiad（+5.34）上均取得一致最优（Table 1）。该优势在 1.5B、3B、7B 及不同模型系列（Qwen、DeepSeek）上均稳定复现（Table 2），验证了方法的通用性。

## 整体框架

MathForge 是一个面向强化学习式推理验证（RLVR）的“数据–算法”协同框架，由两个正交且互补的组件构成：**难度感知组策略优化（DGPO）** 和 **多方面问题改写（MQR）**。二者的关系并非简单叠加，而是形成一条“更难数据 → 更强算法”的正反馈闭环：MQR 系统性提升训练问题的内在难度，DGPO 则从优化器层面纠正 GRPO 对困难问题的隐式压制，使模型能有效利用这些高难度样本。

### 核心瓶颈与解决思路

框架的设计起点是对 GRPO 族算法的一个理论发现：**组相对优势估计（GRAE）使用标准差归一化，导致每个问题的总更新幅度与正确率 $p$ 呈 $2G\sqrt{p(1-p)}$ 关系，在 $p=0.5$ 时达到最大，而极难或极易问题的更新被显著压制**（Theorem 1, Eq. 8）。这意味着，即便一个困难问题仍有至少一个正确响应（即存在学习信号），GRPO 也会因其低正确率而赋予极小的更新量。同时，现有数据增强方法（如简单重复或改写）并未系统性增加问题的内在推理难度，使“难题被忽视”的问题进一步恶化。

MathForge 从两个维度打破这一瓶颈：

1. **算法侧（DGPO）**：将标准化因子从标准差替换为平均绝对偏差（MAD），使每个问题的总更新幅度恒为 $G$，彻底消除对正确率的依赖（Theorem 2, Eq. 10）；再引入基于负平均奖励的软最大化问题级权重（DQW），显式将训练焦点引向更困难的问题。
2. **数据侧（MQR）**：通过添加故事背景、引入抽象术语、嵌套子问题三种策略重写原始问题，在保持原始答案不变的前提下系统性提升问题难度和多样性。

### Pipeline 总览

框架的整体执行流程如下：

```
原始问题集 (MATH)
       │
       ▼
┌─────────────────┐
│  MQR 多角度改写   │  ← 外部 LLM (如 OpenAI o3)
│  · 故事背景      │     保持原始答案不变
│  · 抽象术语      │     数据量扩大 4 倍
│  · 嵌套子问题    │
└────────┬────────┘
         │ 增强问题集
         ▼
┌─────────────────┐
│  DGPO 训练循环   │
│                 │
│  ┌───────────┐  │
│  │ 采样 G 个  │  │  ← 当前策略模型 π_θ
│  │ 响应 per q │  │
│  └─────┬─────┘  │
│        │ 奖励 r  │  ← 0/1 二进制奖励 (答案匹配)
│        ▼        │
│  ┌───────────┐  │
│  │  DGAE     │  │  ← MAD 归一化的组优势
│  │  优势估计  │  │     每问题总更新量恒为 G
│  └─────┬─────┘  │
│        │        │
│  ┌─────▼──────┐ │
│  │  DQW 权重  │ │  ← λ_s ∝ exp(-mean(r)/T)
│  │  (T=2.0)   │ │     难题获得更高权重
│  └─────┬──────┘ │
│        │        │
│  ┌─────▼──────┐ │
│  │ PPO-clip   │ │  ← 有效 token 级平均
│  │ 策略梯度   │ │     防止梯度剧烈波动
│  └────────────┘ │
└─────────────────┘
         │
         ▼
    更新后的策略模型
```

### 模块职责与数据流

**MQR（数据增强模块）** 在训练开始前离线执行，不参与 RL 循环。其三种改写策略各有侧重：
- **MQR-Background**：为问题添加叙事背景，增加信息噪声和无关细节的干扰；
- **MQR-Term**：引入抽象数学术语或形式化表述，提升概念理解门槛；
- **MQR-SubProblem**：将独立子问题嵌套进原问题，增加推理步骤的链长。

三种策略可叠加使用，消融实验（Table 7）表明子问题嵌套贡献最大（单独提升 1.63%），三者联合使用达到最优。

**DGPO（策略优化模块）** 的核心是两处对 GRPO 的修改：

| 修改点 | GRPO 基线 | MathForge (DGPO) | 作用 |
|--------|----------|------------------|------|
| 组优势标准化 | 标准差 (std) | 平均绝对偏差 (MAD) | 消除更新幅度对正确率的依赖 |
| 问题级加权 | 无（均匀） | DQW 软最大化权重 | 显式聚焦困难问题 |

DGPO 的损失函数（Eq. 3）在有效问题上进行 token 级平均，避免因不同问题的有效 token 数差异导致的梯度波动。DQW 的温度 $T=2.0$ 经消融验证（Table 3）达到最佳平衡：$T=1.0$ 过于尖锐（几乎只关注最难问题），$T=10.0$ 过于平滑（退化为近似均匀）。

### 协同效应

DGPO 和 MQR 各自独立有效（DGPO 较 GRPO 提升 2.18%，MQR 提升 3.43%），但二者联合（MathForge）达到 42.17% 的平均基准分，较 GRPO 基线提升 4.56 个百分点（Table 1）。这种协同并非简单的增益叠加：DGPO 的难度感知机制使模型能更有效地利用 MQR 生成的高难度样本，而 MQR 提供的更丰富训练信号又反过来放大了 DGPO 的优势。在 1.5B、3B、7B 及不同模型系列上，MathForge 均一致取得最优结果（Table 2），验证了框架的泛化性。

## 核心模块与公式推导

### 问题定位：GRPO 优势估计的难度失衡

GRPO 的核心机制是通过组内相对优势估计（Group Relative Advantage Estimation, GRAE）替代传统的价值模型，其优势函数为：

$$\hat{A}_{\mathrm{GR}, i} = \frac{r_i - \mathrm{mean}\left(\{r_i\}_{i=1}^G\right)}{\mathrm{std}\left(\{r_i\}_{i=1}^G\right)}$$

其中 $r_i$ 为第 $i$ 个响应的奖励（通常为 0/1 二值），$G$ 为每组采样数。该标准化方式存在一个隐藏的失衡：**每个问题的总更新幅度与正确率 $p$ 强相关**。定理 1 证明，在标准差归一化下，单问题的总更新幅度上限为：

$$\sum_{i=1}^G \left|\hat{A}_{\mathrm{GR}, i}\right| = 2G\sqrt{p(1-p)}$$

该式在 $p=0.5$ 时达到最大值 $G$，而在 $p \to 0$ 或 $p \to 1$ 时趋近于 0。这意味着：**中等难度的问题获得最大更新量，而极难（但仍有解）和极简单的问题被系统性压制**。对于“有正确响应但极难”的问题，这种抑制直接削弱了模型从困难样本中学习的能力。

### 核心模块一：DGAE——困难平衡的组优势估计

为消除更新幅度对问题难度的依赖，DGPO 将标准化因子由标准差替换为**平均绝对偏差（MAD）**，得到困难平衡的组优势估计（Difficulty-Balanced Group Advantage Estimation, DGAE）：

$$\hat{A}_{\mathrm{DG}, si} = \frac{r_{si} - \mathrm{mean}\left(\{r_{si}\}_{i=1}^G\right)}{\mathrm{MAD}\left(\{r_{si}\}_{i=1}^G\right)}$$

其中 MAD 定义为：

$$\mathrm{MAD}\left(\{r_{si}\}_{i=1}^G\right) = \frac{1}{G} \sum_{i=1}^G \left| r_{si} - \mathrm{mean}\left(\{r_{si}\}_{i=1}^G\right) \right|$$

定理 2 证明，在 MAD 归一化下，每个问题的总更新幅度恒为常数 $G$，与正确率 $p$ 完全解耦：

$$\sum_{i=1}^G \left|\hat{A}_{\mathrm{DG}, i}\right| = G$$

这一性质确保了无论问题难度如何，只要存在至少一个正确响应，其对模型参数的更新贡献保持均衡。消融实验（Table 3）表明，DGAE 单独贡献 +0.94% 的平均基准提升。

### 核心模块二：DQW——困难感知的问题级加权

在消除更新幅度的被动失衡后，DGPO 进一步通过**困难感知的问题级加权（Difficulty-Aware Question-Level Weighting, DQW）** 主动将训练焦点引向更难的问题。问题难度量化为该问题所有响应的负平均奖励：

$$D_s = - \mathrm{mean}\left(\{r_{si}\}_{i=1}^G\right)$$

难度越高（正确率越低），$D_s$ 越大。基于 softmax 的权重分配为：

$$\lambda_s = B_v \cdot \frac{\exp(D_s / T)}{\sum_{s=1}^{B_v} \exp(D_s / T)}$$

其中 $B_v$ 为有效问题数（至少一个正确响应），$T$ 为温度超参。温度 $T=2.0$ 时，批次内最大与最小权重的比值约为 $e^{1/2} \approx 1.65$，在“聚焦难题”与“保留多样性”之间达到平衡。消融实验（Table 3）表明，DQW 在 DGAE 基础上额外贡献 +1.14%，两者合计使 DGPO 较 GRPO 提升 2.18 个百分点。

### 核心模块三：MQR——多方面问题改写

MQR（Multi-Aspect Question Reformulation）通过三个方面系统性增加问题的内在难度，同时严格保持原始答案不变：

- **MQR-Background**：添加故事背景，引入信息噪声，迫使模型从冗余上下文中提取关键数学结构。
- **MQR-Term**：引入抽象数学术语，提升问题的概念层级。
- **MQR-SubProblem**：嵌套独立子问题，增加推理步骤的深度和复杂度。

消融实验（Table 7）显示，子问题重写（Origin+Sub-Problem）贡献最大，单独提升 1.63%；三种策略组合后，MQR 仅用 GRPO 训练即达 41.04% 平均分（+3.43%）。

### DGPO 完整目标函数

整合 DGAE 和 DQW 后，DGPO 的完整优化目标为：

$$\mathcal{I}_{\mathrm{DGPO}}(\theta) = \mathbb{E}\left[\{q_s\}_{s=1}^B \sim \mathcal{D}, \{o_{si}\}_{i=1}^G \sim \pi_{\theta_{\mathrm{old}}}(\cdot \vert q_s)\right] \frac{1}{\sum_{s=1}^{B_v} \sum_{i=1}^G |o_{si}|} \sum_{s=1}^{B_v} \lambda_s \sum_{i=1}^G \sum_{t=1}^{|o_{si}|} \left\{ \min\left[ I_{sit}(\theta) \hat{A}_{\mathrm{DG}, si}, \mathrm{clip}\left(I_{sit}(\theta), 1-\varepsilon, 1+\varepsilon\right) \hat{A}_{\mathrm{DG}, si} \right] \right\}$$

其中 $I_{sit}(\theta)$ 为 token 级重要性采样比，损失仅在有效问题（$B_v$）上平均，避免无效问题引起的梯度波动。

## 实验与分析

### 核心瓶颈与因果验证

GRPO在数学推理任务上的训练存在一个此前未被揭示的隐式不平衡：其组相对优势估计（GRAE）使用标准差进行标准化，导致每个问题的总更新幅度与正确率 $p$ 强相关——当 $p=0.5$ 时更新幅度达到最大值 $2G\sqrt{p(1-p)}$，而极难（$p$ 接近 0）或极易（$p$ 接近 1）的问题更新被严重压制（Theorem 1, Eq. 8）。这意味着，模型从“仍有学习空间”的困难问题中获得的梯度信号远小于中等难度问题，形成了“越难越学不到”的反直觉困境。

MathForge 通过两个因果旋钮打破这一瓶颈：**DGAE** 将标准化因子替换为平均绝对偏差（MAD），使每个问题的总更新幅度恒为 $G$，完全消除与原问题难度的依赖（Theorem 2, Eq. 10）；**DQW** 以负平均奖励 $D_s = -\text{mean}(\{r_{si}\})$ 量化问题难度，通过 softmax 加权显式将训练焦点引向更难的问题（Eq. 11, $T=2.0$）。同时，**MQR** 通过添加故事背景、引入抽象术语、嵌套子问题三个维度重写问题，系统性提升训练数据的固有难度，形成“更难数据 → 更强算法”的协同闭环。

### 主实验结果

在 Qwen2.5-Math-7B 上，以 MATH 数据集训练后评估四个数学推理基准，结果如 Table 1 所示（置信度 0.98）：

![[assets/figures/papers/paper_list_l17_https_openreview_net_forum_id_nfURupkdRJ/figures/001_Table_1.jpg]]
*Table 1: Comparative results of methods trained on the MATH dataset using Qwen2.5-Math-7B*

- **GRPO 基线**：平均分 37.61%
- **DGPO（单独）**：平均分 39.79%，较 GRPO 提升 **+2.18 个百分点**
- **MQR（单独）**：平均分 41.04%，较 GRPO 提升 **+3.43 个百分点**——仅通过数据增强即超越所有 RL 变体基线
- **MathForge（DGPO + MQR）**：平均分 **42.17%**，较 GRPO 提升 **+4.56 个百分点**，在所有基准上一致最优

其中 AIME24 上 MathForge 达到 24.58%（+3.64），MATH500 达到 79.95%（+7.75），Minerva 达到 33.36%（+5.60），Olympiad 达到 42.67%（+5.34）。值得注意的是，MQR 单独使用时 MATH500 得分已达 78.80%（+6.60），说明数据难度提升对分布内泛化的推动尤为显著。

### 跨模型泛化

Table 2 展示了 MathForge 在不同模型尺度和架构上的泛化能力（置信度 0.95）。在 Qwen2.5-Math-1.5B 上，MathForge 平均分 33.84%（+4.45 超过 GRPO）；在 Qwen2.5-3B 上达到 37.83%（+3.99）；在 DeepSeek-Math-7B 上达到 41.76%（+3.00）。所有模型规模下 MathForge 均保持最优，证明 DGAE 的难度平衡机制和 DQW 的加权策略具有模型无关的通用性。

![[assets/figures/papers/paper_list_l17_https_openreview_net_forum_id_nfURupkdRJ/figures/002_Table_2.jpg]]
*Table 2: Comparative results of methods trained on the MATH dataset using varying base models*

### DGPO 消融分析

Table 3 对 DGPO 组件进行拆解（置信度 0.95-0.98）：

![[assets/figures/papers/paper_list_l17_https_openreview_net_forum_id_nfURupkdRJ/figures/003_Table_3.jpg]]
*Table 3: Ablation Results of DGPO trained on the MATH dataset using Qwen2.5-Math-7B*

- **DGAE 单独贡献**：在 GRPO 基础上仅替换优势估计为 MAD 归一化，平均分提升 **+0.94%**，验证了消除更新幅度不平衡的独立价值
- **DQW 额外贡献**：在 DGAE 基础上加入难度感知加权，额外提升 **+1.14%**，合计使 DGPO 较 GRPO 提高 **+2.18%**
- **温度敏感性**：$T=2.0$ 达到最佳平衡——此时批次内最大与最小权重比约为 $e^{1/2} \approx 1.65$，既避免 $T=1.0$ 时的过度尖锐（仅关注极难问题），也避免 $T=10.0$ 时的过于平滑（退化为均匀加权）

### MQR 消融分析

Table 7 对 MQR 的三个重写维度进行拆解（置信度 0.95）：

![[assets/figures/papers/paper_list_l17_https_openreview_net_forum_id_nfURupkdRJ/figures/009_Table_7.jpg]]
*Table 7: Ablation Results of MQR on the MATH dataset using Qwen2.5-Math-7B*

- **子问题重写（Origin+Sub-Problem）**贡献最大，单独提升 **+1.63%**，说明嵌套独立子问题能最有效地增加推理链长度和复杂度
- **背景添加（Origin+Background）**和**术语引入（Origin+Term）**分别带来 +0.98% 和 +1.12% 的提升
- **三者联合（MQR 完整）**达到 +2.27% 的最大增益，表明多方面改写存在互补效应

Table 6 进一步验证 MQR 的增益源于数据质量而非数据量：将原始数据重复四倍训练，效果始终低于 MQR 增强数据（置信度 0.95）。这确认了 MQR 通过系统性提升问题内在难度来驱动性能，而非简单的数据扩充。

![[assets/figures/papers/paper_list_l17_https_openreview_net_forum_id_nfURupkdRJ/figures/008_Table_6.jpg]]
*Table 6: Comparative results of methods trained on the original data vs. the MQR-augmented data using DGPO and varying base models*

### 与其他策略优化方法的协同

DGPO 的 DGAE 和 DQW 作为即插即用的增强模块，可与现有策略优化方法叠加。Table 4 显示，将 DGPO 集成到 GPG、DAPO、GSPO 上分别带来 +0.99%、+1.97%、+1.61% 的平均提升（置信度 0.95）。其中 **DAPO+DGPO** 达到 39.91%，超越单独 DGPO 的 39.79%，表明难度感知机制与长度惩罚、异步 PPO 等设计存在正向协同。

![[assets/figures/papers/paper_list_l17_https_openreview_net_forum_id_nfURupkdRJ/figures/004_Table_4.jpg]]
*Table 4: Synergistic results of DGPO with other policy optimization methods trained on the MATH dataset using Qwen2.5-Math-7B*

### 多模态扩展验证

在几何推理多模态任务 GEOQA-8k 上使用 Qwen2.5-VL-3B-Instruct（Table 5），DGPO 达到 59.95%，较 GRPO 基线（57.43%）提升 **+2.52%**，较 Dr.GRPO（58.09%）和 DAPO（59.02%）均有显著优势（置信度 0.95）。这表明难度平衡优势估计在非纯文本推理场景同样有效。

![[assets/figures/papers/paper_list_l17_https_openreview_net_forum_id_nfURupkdRJ/figures/005_Table_5.jpg]]
*Table 5: Comparative results of methods trained on the GEOQA-8k dataset using Qwen2.5-VL-3B-Instruct in the multimodal domain*

### 训练动态分析

Figure 1 展示了 DGPO 与 GRPO 在 MATH500 上的训练动态：DGPO 的输出长度下降更快且更稳定（从约 630 降至 545），而 GRPO 在约 580 附近趋于平台。这暗示 DGPO 通过聚焦难题，更有效地抑制了冗长但无效的推理链，促进了简洁正确解的涌现。

![[assets/figures/papers/paper_list_l17_https_openreview_net_forum_id_nfURupkdRJ/figures/007_Figure_1.jpg]]
*Figure 1: Training dynamics of DGPO vs. GRPO evaluated on the MATH500 benchmark. Both models are trained on MATH using Qwen2.5-Math-7B*

### 失败模式与局限性

1. **MQR 外部依赖**：重写质量依赖外部 LLM（如 OpenAI o3），引入额外成本和 API 依赖，且 Table 8 显示不同重写模型的能力差异会影响最终效果
2. **领域局限性**：当前验证集中于数学推理（MATH、AIME、AMC 等），在代码生成、科学推理等领域的有效性未经验证
3. **温度非自适应**：DQW 的温度 $T=2.0$ 为固定超参，其最优值可能随训练阶段和模型规模变化，缺乏自适应调节机制
4. **奖励粒度限制**：所有实验均使用 0/1 二进制奖励，DGAE 对更细粒度奖励函数的理论适用性虽有证明，但缺乏充分实证

![[assets/figures/papers/paper_list_l17_https_openreview_net_forum_id_nfURupkdRJ/figures/012_Table_8.jpg]]
*Table 8: Comparative results of MQR using varying reformulator models on the MATH dataset*

### 待验证问题

- 困难感知权重在极长训练中是否会导致模型遗忘简单任务（灾难性遗忘）？
- 能否将 MQR 的重写过程内化到 RL 训练循环中，实现数据难度与策略能力的同步进化？
- 该方法在 70B+ 规模模型和更复杂推理任务（如竞赛级证明）上的扩展性尚待检验。

### 补充图表

![[assets/figures/papers/paper_list_l17_https_openreview_net_forum_id_nfURupkdRJ/figures/013_Table_9.jpg]]
*Table 9: Hyperparameter settings trained on the MATH dataset using varying base models*

## 方法谱系与知识库定位

### 核心基线：GRPO 及其变体系列

MathForge 的直接比较对象是 **GRPO**（Group Relative Policy Optimization；Shao et al., 2024），以及基于 GRPO 的多个改进变体。GRPO 的核心机制是用组内相对优势估计替代传统的价值模型，从而降低 RLVR（Reinforcement Learning from Verifiable Rewards）的计算开销。然而，本文揭示了 GRPO 的一个深层缺陷：其组相对优势估计函数 GRAE 使用标准差进行归一化，导致每个问题的总更新幅度与正确率 $p$ 相关，在 $p=0.5$ 时达到最大值 $2G\sqrt{p(1-p)}$，而极难或极易问题的更新信号被系统性压制（Theorem 1, Eq. 8）。这一发现构成了 MathForge 方法设计的出发点。

在 GRPO 的改进谱系中，本文比较了以下代表性工作：

- **Dr.GRPO**（Liu et al., 2025a）：引入丢弃率机制，对部分低奖励响应进行掩码处理，但未解决更新幅度与问题难度的隐式依赖。
- **GPG**（Chu et al., 2025）：去除 PPO 中的裁剪操作，采用无裁剪策略梯度，但优势估计仍沿用标准差归一化。
- **DAPO**（Yu et al., 2025）：引入长度惩罚和异步 PPO 训练，侧重于抑制冗长输出，未触及难度平衡问题。
- **GSPO**（Zheng et al., 2025）：采用序列级重要性采样，改进梯度估计的方差，但同样未对问题难度进行显式建模。
- **GRPO-AD**（Zhang & Zuo, 2025）：在 GRPO 上增加难度感知的优势重加权，是方向上最接近 DGPO 的工作，但其加权机制与本文的 DGAE + DQW 方案在标准化方式和权重设计上存在本质差异。

### DGPO 的方法定位：从隐式平衡到显式聚焦

DGPO 对 GRPO 的改进体现在两个正交且可叠加的维度：

**第一维度：困难平衡的组优势估计（DGAE）。** 将 GRAE 中的标准差归一化替换为平均绝对偏差（MAD）归一化。理论分析表明，MAD 归一化使每个问题的总更新幅度恒为 $G$，完全消除了与原问题难度（正确率 $p$）的依赖关系（Theorem 2, Eq. 10）。这一改动是“校正性”的——它恢复了难题应有的梯度贡献，而非简单地增加某种先验偏好。

**第二维度：困难感知的问题级加权（DQW）。** 在 DGAE 已实现难度中性的基础上，DGPO 进一步引入基于负平均奖励的软最大化权重 $\lambda_s = B_v \cdot \frac{\exp(D_s/T)}{\sum \exp(D_s/T)}$，其中 $D_s = -\text{mean}(\{r_{si}\})$，温度 $T=2.0$。该机制显式地将训练焦点引向更难的问题，形成从“难度中性”到“难度偏好”的渐进聚焦。消融实验表明，DGAE 单独贡献 +0.94%，DQW 额外贡献 +1.14%，两者合计使 DGPO 较 GRPO 提升 +2.18%（Table 3）。

DGPO 的另一个重要特性是其**即插即用的兼容性**。由于 DGAE 和 DQW 仅涉及优势估计和问题采样权重的修改，它们可以与大多数现有策略优化方法叠加使用。实验证实，将 DGPO 集成到 DAPO、GPG、GSPO 中均能获得一致的额外增益（Table 4），其中 DAPO+DGPO 达到 39.91% 的平均分，优于单独 DGPO 的 39.79%。

### MQR 的方法定位：数据增强的难度维度

MQR（Multi-Aspect Question Reformulation）在数据层面与 DGPO 形成互补。与传统的答案重写或问题复述不同，MQR 的核心约束是**保持原始答案不变**，仅通过以下三个方面系统性地增加问题的内在难度：

1. **MQR-Background**：添加故事背景，增加信息噪声和冗余。
2. **MQR-Term**：引入抽象数学术语，提升语义复杂度。
3. **MQR-SubProblem**：嵌套独立子问题，增加推理步骤的深度。

这种设计使得 MQR 生成的数据天然适配 RLVR 框架——答案不变意味着奖励信号无需重新标注，而难度提升则迫使策略在更复杂的场景中学习更鲁棒的推理能力。消融实验表明，子问题重写（Origin+Sub-Problem）贡献最大，单独提升 +1.63%（Table 7）。关键的是，MQR 带来的增益源于数据质量的提升，而非数据量的简单增加：四倍于原始数据量的重复训练效果不如 MQR（Table 6, Section 4.4）。

### MathForge 的协同闭环

MathForge 将 DGPO 和 MQR 组合为一个“更难数据–更强算法”的协同闭环。MQR 生成的高难度数据为 DGPO 的难度感知机制提供了更丰富的训练信号，而 DGPO 的 DQW 机制则确保这些难题获得应有的更新权重。在 Qwen2.5-Math-7B 上，MathForge 达到 42.17% 的平均基准分，较 GRPO 提升 +4.56 个百分点（Table 1）。该优势在 1.5B、3B、7B 及不同模型系列（Qwen2.5、DeepSeek-Math）上均一致保持（Table 2），在几何推理的多模态领域（GeoQA）同样有效（Table 5）。

### 适用边界与已知局限

1. **领域泛化性未充分验证。** 当前实验集中于数学推理（MATH、AIME、AMC、MATH500、Minerva、Olympiad），在代码生成、科学推理等其他可验证奖励领域的有效性需要进一步实证。GeoQA 上的实验提供了初步的多模态证据，但覆盖面有限。

2. **MQR 的外部依赖。** MQR 的重写质量依赖外部 LLM（如 OpenAI o3），引入额外推理成本和外部 API 依赖。Table 8 表明，重写模型的能力直接影响 MQR 的效果，这限制了该模块在资源受限场景下的可复现性。

3. **DQW 温度的静态性。** 温度 $T=2.0$ 是固定超参，其最优值可能随模型规模、训练阶段甚至数据分布的变化而漂移，缺乏自适应性。$T=1.0$ 时权重过于尖锐，$T=10.0$ 时过于平滑（Table 3），说明该参数确实存在敏感区间。

4. **奖励信号的二值性。** 所有实验均使用 0/1 二进制奖励（答案正确与否），未探索更细粒度的奖励信号（如部分正确、步骤级评分）与 DGAE/DQW 机制的结合。虽然 DGAE 对非二值奖励的理论有效性成立，但缺乏丰富的实证支持。

### 开放问题

- **遗忘风险。** 困难感知权重在极长训练中是否会导致模型遗忘简单任务？Figure 1 的训练动态显示 DGPO 的奖励持续上升，但未报告简单子集的性能退化情况。
- **数据与策略的同步进化。** 能否将 MQR 的重写过程内化到 RL 训练循环中，使问题难度随策略能力的提升而动态调整，实现数据生成与策略优化的在线协同？
- **更大规模的扩展性。** 该方法在 70B+ 模型和更复杂推理任务（如竞赛级证明、研究级问题求解）上的扩展性如何？当前实验最大仅覆盖 7B 模型。
- **难度度量的替代方案。** DQW 使用负平均奖励作为难度代理，在训练初期模型能力较弱时，该信号可能噪声较大。是否存在更鲁棒的难度度量方式（如基于模型置信度、响应熵或外部难度标注）？

## 原文 PDF

![[paperPDFs/ICLR_2026/Harder_Is_Better_Boosting_Mathematical_Reasoning_via_Difficulty_Aware_GRPO_and_Multi_Aspect_Question_Reformulation.pdf]]
