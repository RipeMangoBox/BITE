---
title: "An Information Theoretic Perspective on Agentic System Design"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/An_Information_Theoretic_Perspective_on_Agentic_System_Design.pdf
project_link: null
code_link: null
openreview_forum_id: isFHz8qf20
aliases:
- ITPASD
tags:
- ICLR_2026
- topic/reinforcement_learning_planning_agents
- topic/reinforcement_learning_planning_agents/planning_control
core_operator: "压缩器模型系列与尺寸是决定下游性能的最关键因素，通过互信息率和比特效率量化压缩器质量，可发现更大的压缩器在准确率和令牌效率上均具有优势，其计算成本增长呈子线性。"
primary_logic: "将压缩器建模为含噪通道，利用蒙特卡洛互信息估计器在无需完整词汇概率的情况下量化压缩质量，揭示了互信息率与下游性能的强相关性，并论证了扩展压缩器远比扩展预测器有效，且更大压缩器具有更高的信息密度和比特效率，使得本地计算可以替代云端成本。"
claims:
- "在LONGHEALTH上，将Qwen-2.5压缩器从1.5B扩展到7B，准确率提升60%；而将预测器从70B扩展到405B，准确率仅提升12%。"
- "7B Qwen-2.5压缩器相比其1.5B版本，准确率提高1.6倍，输出长度缩短4.6倍，每令牌互信息提高5.4倍。"
- "信息率（每令牌互信息）与下游性能及困惑度强相关（r = -0.84, R² = 0.71）。"
- "在Deep Research基准上，使用3B本地压缩器配合GPT-4O预测器，恢复99%的前沿模型准确率，API成本降低74%。"
---

# An Information Theoretic Perspective on Agentic System Design

> [!tip] 核心洞察
> 将压缩器建模为含噪通道，利用蒙特卡洛互信息估计器在无需完整词汇概率的情况下量化压缩质量，揭示了互信息率与下游性能的强相关性，并论证了扩展压缩器远比扩展预测器有效，且更大压缩器具有更高的信息密度和比特效率，使得本地计算可以替代云端成本。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 从信息论视角看代理系统设计 |
| 英文题名 | An Information Theoretic Perspective on Agentic System Design |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=isFHz8qf20) |
| Topic | #topic/reinforcement_learning_planning_agents #topic/reinforcement_learning_planning_agents/planning_control |
| Method | 基于蒙特卡洛互信息估计的压缩器-预测器评估框架 |
| Dataset | LONGHEALTH, FINANCEBENCH, DEEPRESEARCH BENCH |

> [!tip] 效果简介
> - LONGHEALTH 上，Accuracy improvement from scaling compressor vs predictor 为 Scaling compressor (Qwen-2.5 1.5B→7B)，对比 Scaling predictor (LLaMA-3 70B→405B)，变化 +60% vs +12%。
> - LONGHEALTH 上，Accuracy relative to GPT-4O direct baseline 为 Qwen-2.5 7B compressor + predictor，对比 GPT-4O direct (no compression)，变化 surpasses by 4pp。
> - FINANCEBENCH 上，Accuracy relative to GPT-4O direct baseline 为 7-8B compressors，对比 GPT-4O direct (100%)，变化 recovers 97%。

## 概要

当前压缩器-预测器（compressor-predictor）代理系统设计主要依赖试错，缺乏任务无关的指标来量化压缩器输出的信息量，导致无法将下游性能归因于压缩器的信息保留质量或预测器的推理能力。本文从信息论视角出发，提出将压缩器建模为含噪通道，并引入基于蒙特卡洛采样的互信息估计器，在不依赖完整词汇概率分布的情况下量化压缩质量。

核心发现是：压缩器模型系列与尺寸是决定下游性能的最关键因素。在LONGHEALTH基准上，将Qwen-2.5压缩器从1.5B扩展到7B，准确率提升60%，而将预测器从70B扩展到405B仅提升12%。更大的压缩器不仅准确率更高，输出也更简洁——7B版本相比1.5B版本准确率提高1.6倍，输出长度缩短4.6倍，每令牌互信息提高5.4倍。信息率（每令牌互信息）与下游性能及困惑度呈强相关（r = -0.84, R² = 0.71）。

在方法层面，本文的核心贡献在于将系统评估从端到端准确率拓展到任务无关的信息度量：以蒙特卡洛互信息估计器替代黑盒评估，以互信息率和率失真曲线指导系统设计。实验进一步表明，使用3B本地压缩器配合GPT-4O预测器，可在Deep Research基准上恢复99%的前沿模型准确率，同时将API成本降低74%。逻辑回归分析确认，压缩器模型系列和尺寸的重要性远大于预测器尺寸。

上述发现揭示了扩展压缩器远比扩展预测器有效的缩放规律，且更大压缩器具有更高的信息密度和比特效率，使得本地计算可以实质性替代云端成本。

### 压缩器-预测器架构的兴起与设计困境

大型语言模型驱动的代理系统中，一种主导范式是将长上下文处理分解为两阶段流水线：**压缩器**将原始上下文 $X$ 压缩为紧凑摘要 $Z$，**预测器**基于 $Z$ 生成最终答案 $Y$。这一架构的信息流可形式化为：

$$X \xrightarrow{ p(z|x) } Z \xrightarrow{ p(y|z) } Y$$

该范式广泛存在于检索增强生成、Deep Research、代码代理等场景中，其吸引力在于：压缩器可在本地设备运行，将长上下文浓缩后发送至云端预测器，从而降低API成本和延迟。如图1所示，消费级硬件（如Google Pixel手机、Apple MacBook）已具备运行越来越大开源模型的能力，使得本地压缩成为可行方案。

然而，当前系统设计面临一个根本性瓶颈：**缺乏任务无关的指标来量化压缩器输出的信息量**。实践中，开发者主要依赖试错——通过下游任务准确率间接评估压缩质量，无法将性能变化归因于压缩器的信息保留能力还是预测器的推理能力。这种黑盒式的评估方式导致两个关键问题：其一，无法系统化地比较不同压缩器的信息压缩效率；其二，无法在部署前预测压缩器-预测器配对的下游性能。

### 现有评估方法的局限

现有工作对压缩器效能的评估几乎完全依赖端到端指标：准确率、困惑度或人工评判。这些方法存在三重缺陷：

1. **任务耦合性**：准确率同时受压缩质量和预测器能力影响，无法解耦。例如，一个强预测器可能掩盖压缩器的信息丢失，导致对压缩器质量的误判。
2. **不可迁移性**：在任务A上表现优异的压缩器，未必在任务B上保留足够信息，但端到端指标无法提供跨任务的泛化保证。
3. **缺乏理论指导**：没有理论框架来解释为何某些压缩器-预测器组合优于其他组合，也无法预测缩放压缩器或预测器哪个更有效。

### 本文动机：信息论视角

本文的核心动机是将压缩器-预测器通信显式建模为**含噪通道**，并引入信息论工具进行量化分析。具体而言，将压缩器建模为 $p(z|x)$，通过估计上下文 $X$ 与压缩输出 $Z$ 之间的**互信息** $I(X;Z|Q)$（以查询 $Q$ 为条件），获得一个任务无关的压缩质量度量。

这一视角的关键优势在于：

- **解耦评估**：互信息仅取决于压缩器本身，与下游预测器无关，可直接量化“压缩器保留了多少关于原始输入的信息”。
- **率失真分析**：引入速率 $R = I(X;Z|Q)/L$（每令牌互信息比特数）和失真 $D = 1 - \text{ACC}(Z)$，可绘制率失真曲线，揭示压缩效率与保真度之间的根本权衡。
- **设计指导**：通过比较缩放压缩器与缩放预测器的效果，可基于信息论原则做出架构决策——是投入计算资源扩大压缩器还是预测器。

为实现这一框架，论文开发了一个蒙特卡洛互信息估计器，利用现代推理引擎的对数概率，无需完整词汇概率分布即可计算，使得该度量在实际部署中可操作。这一方法论转变的目标是：将代理系统设计从经验试错提升为有理论指导的系统化工程实践。

## 核心方法与创新机理

### 瓶颈洞察：压缩器-预测器系统的归因困境

当前代理系统广泛采用压缩器-预测器架构，即先用小型压缩器语言模型将长上下文 $X$ 压缩为摘要 $Z$，再由大型预测器基于 $Z$ 生成最终答案 $Y$。然而，该架构的设计长期依赖端到端试错——研究者无法将下游性能的优劣归因于压缩器的信息保留质量，还是预测器的推理能力。根本原因在于：**缺乏一种任务无关的指标来量化压缩器输出的信息量**，导致系统组件的优化缺乏系统性指导。

### 方法创新：基于蒙特卡洛互信息估计的评估框架

本文的核心创新在于将信息论引入压缩器-预测器系统的分析与设计，提出了三个关键的方法论转变（changed slots）：

**1. 中间表示评估指标：从下游准确率到任务无关的互信息**

传统方法仅通过下游任务准确率间接评估压缩质量，无法解耦压缩器与预测器的贡献。本文提出以压缩器输入 $X$ 与输出 $Z$ 之间的互信息 $I(X;Z|Q)$ 作为压缩器效能的直接度量（Section 2.2, Equation 2）。具体而言，互信息量化为：

$$I(X;Z) = D_{\mathrm{KL}}(p(x,z) \parallel p(x)p(z)) = \mathbb{E}_{x,z \sim p(x,z)} \left[ \log \frac{p(z|x)}{p(z)} \right]$$

为实现可扩展的估计，作者开发了一个蒙特卡洛估计器，仅需推理引擎提供的对数概率，无需完整词表概率分布：

$$\hat{I}(X;Z) \approx \frac{1}{NM} \sum_{i=1}^{N} \sum_{j=1}^{M} \left[ \log p(z_{ij}|x_i) - \log \left( \frac{1}{N} \sum_{l=1}^{N} p(z_{ij}|x_l) \right) \right]$$

该估计器从 $p(z|x)$ 采样并通过对 $N$ 个样本的边际化来近似 $p(z)$，避免了直接计算完整词表的计算开销。实验表明，该估计器对代理模型的选择具有鲁棒性——不同代理模型（如Qwen-2.5-7B、LLaMA-3.1-8B、Qwen-3-8B）仅产生固定的垂直偏移，不影响缩放趋势（Figure 13）。

**2. 系统性能度量：从端到端准确率到率失真分析**

传统方法仅使用端到端准确率或困惑度评估系统，无法揭示压缩与保真之间的权衡。本文引入信息论中的率失真框架，定义：

- **速率** $R = I(X;Z|Q)/L$：每个令牌携带的互信息比特数，衡量比特效率
- **失真** $D = 1 - \operatorname{ACC}(Z)$：以准确率定义的预测误差

通过绘制率失真曲线（Figure 19），可以直观地比较不同压缩器-预测器配对在信息保留与任务性能之间的权衡，为系统设计提供任务无关的决策依据。失真随速率呈指数衰减，并存在不可约失真的下界 $D_0$：$D(R) = C e^{-bR} + D_0$。

**3. 通信通道模型：从黑盒到含噪通道**

传统方法将压缩器与预测器之间的通信视为黑盒，无法分析信息传递的瓶颈。本文显式地将压缩器建模为含噪通道 $p(z|x)$，将整个系统形式化为信息流 $X \xrightarrow{p(z|x)} Z \xrightarrow{p(y|z)} Y$。这一建模使得信息瓶颈理论和率失真理论可以直接应用于代理系统的分析，揭示了压缩器是系统信息传递的关键瓶颈。

### 核心发现：压缩器缩放主导系统性能

基于上述框架，本文揭示了代理系统设计的一个反直觉规律：**扩展压缩器的收益远超扩展预测器**。在LONGHEALTH上，将Qwen-2.5压缩器从1.5B扩展到7B，准确率提升60%；而将预测器从70B扩展到405B，准确率仅提升12%（Section 3.1）。更关键的是，更大的压缩器在提升准确率的同时，输出长度反而缩短了4.6倍，每令牌互信息提高了5.4倍——这意味着更大的压缩器不仅更准确，而且信息密度更高、比特效率更强。

逻辑回归分析进一步确认，压缩器的模型系列与尺寸是决定下游准确率的最重要因素，其重要性远超预测器尺寸（Figure 17, Section 3.4）。这一发现具有重要的实践意义：在本地设备上部署更大的压缩器，配合云端预测器，可以在Deep Research基准上以3B本地压缩器配合GPT-4O预测器，恢复99%的前沿模型准确率，同时将API成本降低74%（Section 3.5）。

### 核心瓶颈与设计动机

当前压缩器-预测器代理系统的设计主要依赖试错，缺乏任务无关的指标来量化压缩器输出的信息量。系统设计者无法将下游性能归因于压缩器的信息保留质量或预测器的推理能力，导致组件优化缺乏系统性指导。本文的核心洞察在于：将压缩器建模为含噪通信通道，利用信息论中的互信息来量化压缩质量，从而建立任务无关的系统设计准则。

### 系统架构：压缩器-预测器两阶段模型

整体系统建模为一个两阶段的信息流过程：

$$X \xrightarrow{ p(z|x) } Z \xrightarrow{ p(y|z) } Y$$

其中，压缩器 $p(z|x)$ 将原始上下文 $X$ 压缩为摘要 $Z$，预测器 $p(y|z)$ 基于摘要 $Z$ 生成最终输出 $Y$。这一架构广泛存在于检索增强生成、长上下文问答、Deep Research 等代理系统中。

### 核心功能模块

系统包含四个关键模块：

1. **Compressor LM**：负责将原始上下文 $X$ 根据查询 $Q$ 压缩为摘要 $Z$。压缩器通常采用较小的开源语言模型，如 LLaMA-3、Qwen-2.5、Gemma-3 系列。

2. **Predictor LM**：基于压缩后的摘要 $Z$ 生成最终答案 $Y$。预测器通常采用更大规模的前沿模型，如 GPT-4O 或 LLaMA-3 70B/405B。

3. **Monte Carlo MI Estimator**：利用推理引擎的对数概率，通过蒙特卡洛采样估计互信息 $I(X;Z|Q)$，量化压缩器保留的信息量。该估计器无需完整词汇概率分布即可计算：

$$\hat{I}(X;Z) \approx \frac{1}{NM} \sum_{i=1}^{N} \sum_{j=1}^{M} \left[ \log p(z_{ij}|x_i) - \log \left( \frac{1}{N} \sum_{l=1}^{N} p(z_{ij}|x_l) \right) \right]$$

4. **Rate-Distortion Analyzer**：通过率失真曲线揭示压缩与失真的权衡。速率 $R = \frac{I(X;Z \mid Q)}{L}$ 定义为每个令牌携带的互信息比特数，失真 $D = 1 - \operatorname{ACC}(Z)$ 以准确率定义。失真随速率呈指数衰减：$D(R) = C e^{-bR} + D_0$，其中 $D_0$ 为不可约失真下界。

### 关键设计决策

与基线方法相比，本框架引入了三个关键改进：

- **中间表示评估指标**：从依赖下游任务准确率评估压缩质量，转变为采用蒙特卡洛估计的互信息 $I(X;Z|Q)$ 作为任务无关的压缩器效能度量。
- **系统性能度量**：从仅使用端到端准确率或困惑度，转变为引入互信息率和率失真曲线进行任务无关的系统级预测与设计。
- **通信通道模型**：从将压缩器与预测器的通信视为黑盒，转变为显式建模为含噪通道，用信息瓶颈和率失真理论进行分析。

### 核心发现

实证分析揭示了以下关键规律：压缩器模型系列与尺寸是决定下游性能的最关键因素。在 LONGHEALTH 上，将 Qwen-2.5 压缩器从 1.5B 扩展到 7B，准确率提升 60%；而将预测器从 70B 扩展到 405B，准确率仅提升 12%。更大的压缩器不仅准确率更高，输出也更简洁——7B Qwen-2.5 压缩器相比其 1.5B 版本，准确率提高 1.6 倍，输出长度缩短 4.6 倍，每令牌互信息提高 5.4 倍。信息率（每令牌互信息）与下游性能及困惑度强相关（$r = -0.84$, $R^2 = 0.71$），验证了互信息作为任务无关质量度量的有效性。

### 压缩器-预测器系统模型

本文将一个典型的代理语言模型系统抽象为两阶段信息传输过程。设原始上下文为 $X$，用户查询为 $Q$，最终答案为 $Y$。压缩器 $p(z|x)$ 根据查询 $Q$ 将长上下文 $X$ 压缩为简洁摘要 $Z$，预测器 $p(y|z)$ 则基于摘要 $Z$ 生成最终输出 $Y$。整体系统信息流可表示为：

$$X \xrightarrow{ p(z|x) } Z \xrightarrow{ p(y|z) } Y$$

这一形式化将压缩器与预测器之间的通信从黑盒中解耦出来，使得我们可以独立分析压缩阶段的信息保留质量。核心洞察在于：压缩器输出的摘要 $Z$ 是连接原始信息与下游决策的唯一通道，其信息承载能力直接决定了整个系统的性能上限。

### 蒙特卡洛互信息估计器

为量化压缩器保留原始上下文信息的能力，论文引入互信息 $I(X; Z \mid Q)$ 作为任务无关的压缩质量度量。互信息衡量在给定查询 $Q$ 的条件下，摘要 $Z$ 中包含多少关于原始上下文 $X$ 的信息。其理论定义基于 KL 散度：

$$I(X;Z) = D_{\mathrm{KL}}(p(x,z) \parallel p(x)p(z)) = \mathbb{E}_{x,z \sim p(x,z)} \left[ \log \frac{p(z|x)}{p(z)} \right]$$

然而，直接计算该期望需要完整的词汇概率分布 $p(z)$，这在现代推理服务中通常不可获取。为此，论文设计了一个实用的蒙特卡洛估计器，仅需推理引擎提供的对数概率即可计算：

$$\hat{I}(X;Z) \approx \frac{1}{NM} \sum_{i=1}^{N} \sum_{j=1}^{M} \left[ \log p(z_{ij}|x_i) - \log \left( \frac{1}{N} \sum_{l=1}^{N} p(z_{ij}|x_l) \right) \right]$$

其中 $N$ 为上下文样本数，$M$ 为每个样本的压缩采样数。该估计器的关键技巧在于：通过蒙特卡洛采样从 $p(z|x)$ 生成多个压缩变体 $z_{ij}$，并利用同一批次中其他样本 $x_l$ 的压缩概率来近似边际分布 $p(z)$，从而绕过了对完整词表概率的需求。实际应用中，负值被截断为零以保持估计的稳定性。

### 率失真分析框架

在互信息估计的基础上，论文进一步引入率失真理论来刻画压缩效率与下游性能的权衡关系。定义两个核心指标：

**速率（Rate）**——每令牌携带的互信息比特数，衡量压缩的信息密度：

$$R = \frac{I(X;Z \mid Q)}{L}$$

其中 $L$ 为压缩输出的令牌长度。

**失真（Distortion）**——以准确率定义的信息损失：

$$D = 1 - \operatorname{ACC}(Z)$$

通过绘制不同压缩器配置下的率失真曲线，可以直观比较压缩器在“信息保留”与“输出简洁性”之间的权衡。实验发现失真随速率呈指数衰减趋势，并存在不可约失真的下界 $D_0$，其拟合模型为：

$$D(R) = C e^{-bR} + D_0$$

该框架揭示了压缩器质量的两个维度：更大的压缩器不仅具有更高的绝对互信息，还表现出更高的比特效率（每令牌信息量），这意味着它们能以更短的输出传递更丰富的信息。这一发现直接解释了为何扩展压缩器比扩展预测器更有效——更大的压缩器在压缩阶段就保留了更多关键信息，使得预测器无需从残缺的摘要中艰难推理。

## 实验与关键发现

### 核心发现：压缩器缩放远优于预测器缩放

论文在LONGHEALTH和FINANCEBENCH两个长上下文问答基准上，系统评估了压缩器-预测器架构中各组件的缩放行为。最关键的发现是：**扩展压缩器远比扩展预测器有效**。在LONGHEALTH上，将Qwen-2.5压缩器从1.5B扩展到7B，准确率提升60%；而将LLaMA-3预测器从70B扩展到405B，准确率仅提升12%（Figure 3）。这一差异表明，当前代理系统的瓶颈在于信息压缩的质量，而非下游推理能力。

在绝对性能上，7-8B规模的压缩器在LONGHEALTH上比1-1.5B模型准确率提高3.1倍，并超越GPT-4O直接处理基线4个百分点；在FINANCEBENCH上准确率提高2.6倍，恢复GPT-4O基线的97%（Figure 2）。更值得注意的是，更大的压缩器同时产生更简洁的输出——7-12B压缩器相比1-1.5B压缩器，输出长度缩短达4.6倍，这意味着更好的压缩质量并不以更长的摘要为代价。

### 信息论度量揭示缩放本质

为解释上述现象，论文引入蒙特卡洛互信息估计器，量化压缩器输出Z与原始上下文X之间的互信息I(X;Z|Q)。实验表明，**互信息率（每令牌互信息）与下游性能强相关**（r = -0.84, R² = 0.71，Figure 6），验证了互信息作为任务无关压缩质量度量的有效性。

![[assets/figures/papers/paper_list_l2_https_openreview_net_forum_id_isFHz8qf20/figures/006_Figure_6.jpg]]
*Figure 6: Mutual information and bit efficiency correlate strongly with downstream performance. (Left) We vary both predictor and compressor model in the compression-prediction workflow and measure the distortion on the y-axis and estimate the rate on the x-axis. We plot the resulting rate-distortion curves across predictor sizes 1B, 8B, 70B, and 405B for LLAMA compressors on LONGHEALTH. The lines show fitted exponential-decay functions. (Right) We measure perplexity and mutual information on compressions generated by LLAMA compressors on FINEWEB. The line shows a fitted linear function ( r = - 0 . 8 4 , R ^ { 2 } = 0 . 7 1 ) . Appendix E.2 provides further analyses*

在LONGHEALTH上，7B Qwen-2.5压缩器相比其1.5B版本，每令牌互信息提高5.4倍（Figure 4）。这意味着更大压缩器不仅保留了更多总信息，而且信息密度显著更高——它们用更少的令牌传递了更多的有效信息。这一发现解释了为什么更大压缩器能同时实现更高准确率和更短输出。

![[assets/figures/papers/paper_list_l2_https_openreview_net_forum_id_isFHz8qf20/figures/005_Figure_4.jpg]]
*Figure 4: Larger compressors generate outputs that carry more information about their inputs (conditioned on the query) on LONGHEALTH. We scale compressor model size and estimate the (Left) mutual information, and (Right) bit efficiency (bits of mutual information per token; higher is better) carried by their outputs. Larger compressor model sizes compress documents with higher mutual information and bit efficiency. The dotted line represents the theoretical maximum of the mutual information estimator at the natural logarithm log(N ), where N is the number of documents mutual information is computed across. We find consistent trends on FINANCEBENCH and QASPER (Appendix E.1.6, E.1.1). Figure 5: Scalin...*

### 消融实验：缩放行为的鲁棒性

多项消融实验验证了上述缩放规律的稳健性：

- **简洁性指令无关性**：通过设置不同的输出长度约束（3句/6句/9句），发现压缩器的缩放趋势在各约束下保持一致，准确率、计算成本和互信息的缩放曲线几乎不受影响（Figure 5, Figure 16）。
- **代理模型鲁棒性**：互信息估计器对代理模型的选择（Qwen-2.5-7B, LLaMA-3.1-8B, Qwen-3-8B）仅产生固定的垂直偏移，不影响缩放趋势（Figure 13），说明估计器具有良好的泛化性。
- **推理与MoE模型**：缩放规律同样适用于推理增强模型和混合专家（MoE）架构。MoE压缩器（如Qwen-3-30B-A3B）在相同参数规模下，准确率更高、输出更简洁、互信息更高（Figure 14），但其缩放行为是否与密集模型存在根本差异仍需进一步研究。
- **多轮交互饱和**：在多轮压缩-预测交互中，互信息在两轮后达到饱和，第三轮无额外收益（Figure 18），表明信息瓶颈在初始压缩阶段已基本确定。

![[assets/figures/papers/paper_list_l2_https_openreview_net_forum_id_isFHz8qf20/figures/016_Figure_13.jpg]]
*Figure 13: Monte Carlo mutual information estimator is robust towards choice of proxy model. The y-axis shows the mutual information estimate on LONGHEALTH compressions produced by Proxy Model(Left) LLAMA and (Right) QWEN-2.5 compressor models. The choice of proxy model introduces a Qwen-2.5 7B Llama-3.1 8B Qwen-3 8Bfixed vertical offset in MI estimate, but does not affect compressor scaling behavior*

### 回归分析确认主导因素

通过广义线性模型（GLM）对LONGHEALTH和FINANCEBENCH的问答正确性进行回归分析，论文确认：**压缩器模型系列和尺寸是影响下游性能的最关键因素**，其重要性远大于预测器尺寸（Figure 17）。具体而言，Qwen-2.5系列压缩器显著优于LLaMA系列，且压缩器尺寸的回归系数远大于预测器尺寸的系数，从统计上验证了“扩展压缩器比扩展预测器更有效”的核心主张。

### 率失真分析：压缩与保真度的权衡

论文通过率失真曲线揭示压缩效率与下游失真之间的系统关系。失真D = 1 - ACC(Z)随速率R = I(X;Z|Q)/L指数衰减，并存在不可约失真的下界D₀（Figure 19）。实验表明，更大的压缩器将率失真曲线整体向左下方推移——在相同失真水平下需要更低的速率，或在相同速率下实现更低的失真。这一分析为压缩器选择提供了信息论依据：给定目标准确率，可据此选择满足速率约束的最小压缩器。

![[assets/figures/papers/paper_list_l2_https_openreview_net_forum_id_isFHz8qf20/figures/022_Figure_19.jpg]]
*Figure 19: Exploring the trade-off between compression and fidelity loss: rate-distortion curve. We vary predictor and compressor model in the compression-prediction workflow and measure the distortion on the y-axis and estimate the rate on the x-axis. (Left) We examine a single compressorpredictor LM pairing, COMPRESSOR=LLAMA-3 and PREDICTOR=LLAMA-3.3-70B. (Right) We compare different compressor-predictor LM pairings, where the predictor model is QWEN-2.5-72B (”Qwen-2.5”) or LLAMA-3.3-70B (”Llama”). Markers indicate compressor sizes (1B, 3B, 8B) in the LLAMA-3 compressor model family*

### Deep Research场景：本地压缩的经济性

在Deep Research基准上，使用Qwen-2.5-14B本地压缩器配合GPT-4O预测器，相比无压缩的GPT-4O直接处理，RACE分数提高2.3%，而API成本仅为28.1%（Figure 7）。使用3B本地压缩器配合GPT-4O预测器，可恢复99%的前沿模型准确率，API成本降低74%。这验证了论文的核心主张：**本地计算可以替代云端成本**——通过部署中等规模的本地压缩器，即可在几乎不损失性能的前提下大幅降低对昂贵云端预测器的依赖。

### 局限性与失败模式

尽管缩放规律在多数据集、多模型系列上得到验证，仍需注意以下局限：

1. **互信息估计偏差**：在1-3B规模的小模型上，蒙特卡洛估计器依赖于代理模型的对数概率，可能引入偏差和方差。估计器存在理论上限log(N)，且小样本下可能出现负值（已截断为零）。
2. **模型类型覆盖不足**：主要实验聚焦于GPT式非推理模型及单轮通信场景，推理增强模型和多智能体迭代工作流的缩放行为尚未充分验证。
3. **设备效率未评估**：虽然论证了本地压缩的可行性，但未系统评估设备特定的推理效率优化（如量化、KV缓存等）对实际部署的影响。

![[assets/figures/papers/paper_list_l2_https_openreview_net_forum_id_isFHz8qf20/figures/001_Figure_1.jpg]]
*Figure 1: Why compressors matter. Many agentic LM systems rely on compressors, and personal devices are growing powerful enough to host them on-device. (Left) A compressor condenses a long input X into a shorter summary Z that a predictor expands into the final answer Y . (Right) Consumer hardware can now run increasingly large open-weight LMs, shown for Google Pixel phones and Apple MacBook laptops under FP16 precision with memory estimates from Modal (Lu, 2024). LM-Arena ranks indicate relative performance*

![[assets/figures/papers/paper_list_l2_https_openreview_net_forum_id_isFHz8qf20/figures/012_Figure_9.jpg]]
*Figure 9: Scaling behavior holds for reasoning and mixture-of-experts compressor models on QASPER. We scale compressor model size and reports a different metric of the compression step on the y-axis of each column: (Left) accuracy, (Middle) compression length, (Right) mutual information. Mutual information is estimated using the log probabilities of a proxy model for QWEN-2.5 and LLAMA compressors, and using internal log probabilities for QWEN-3 compressors. Qwen-2.5 Llama-3 Qwen-3Larger compressors produce shorter outputs with higher downstream accuracy and higher mutual information*

## 定位与知识库关联

### 核心贡献定位

本文的核心贡献在于为压缩器-预测器代理系统引入了一套**任务无关的信息论评估框架**，填补了该领域长期存在的评估盲区。传统方法在设计此类系统时，主要依赖端到端下游任务准确率或困惑度来间接判断压缩质量，无法将性能归因于压缩器的信息保留能力或预测器的推理能力。本文通过将压缩器显式建模为含噪通信通道，并引入蒙特卡洛互信息估计器，首次实现了对中间表示信息量的量化度量，从而将系统优化从试错转向可归因、可预测的方向。

具体而言，本文在三个关键维度上推进了现有方法：

1. **评估指标的范式转换**：将压缩质量的评估从下游任务依赖（如准确率）转向任务无关的互信息度量 $I(X;Z|Q)$，使得压缩器可以在不涉及预测器的情况下被独立评估和选择。
2. **系统设计的理论化**：通过率失真分析（$D(R) = C e^{-bR} + D_0$）揭示压缩-保真度权衡，为压缩器与预测器的配对选择提供了系统化原则。
3. **缩放规律的重新发现**：通过逻辑回归分析（Figure 17）确认，压缩器模型系列与尺寸是决定下游性能的主导因素，其重要性远超预测器尺寸，颠覆了“更大预测器即更好”的直觉。

### 与现有工作的关系

#### 基线方法对比

本文的直接基线是**GPT-4O Direct**（OpenAI et al., 2024），即不使用压缩器、直接将完整输入传递给预测器的端到端方案。该基线代表了当前代理系统设计的“无压缩”范式，其优势在于无信息损失，但代价是高昂的计算成本和令牌消耗。本文证明，通过精心选择压缩器，可以在恢复甚至超越该基线性能的同时，大幅降低API成本（如在Deep Research基准上，使用3B本地压缩器配合GPT-4O预测器，恢复99%的前沿模型准确率，API成本降低74%）。

另一重要基线是**LLaMA-3 Predictors**（Grattafiori et al., 2024）的多尺寸变体（1B, 8B, 70B, 405B），用于对比缩放压缩器与缩放预测器的效果差异。实验表明，在LONGHEALTH上将Qwen-2.5压缩器从1.5B扩展到7B，准确率提升60%；而将LLaMA-3预测器从70B扩展到405B，准确率仅提升12%。这一对比直接论证了“扩展压缩器远比扩展预测器有效”的核心主张。

#### 方法论谱系

本文的方法论根植于**信息瓶颈理论**（Tishby et al., 1999）和**率失真理论**（Shannon, 1959），但将其从单模型分析扩展到了多模型通信场景。与传统的神经网络互信息估计方法（如MINE、InfoNCE）不同，本文的蒙特卡洛估计器利用现代推理引擎的对数概率，无需完整词汇概率分布，具有实际可部署性。这一设计使得该框架可以无缝集成到现有的API驱动或本地推理工作流中。

在代理系统设计领域，本文与以下方向形成互补或对比：
- **检索增强生成（RAG）**：RAG系统也涉及上下文压缩，但通常采用检索而非生成式压缩。本文的信息论框架可扩展用于评估检索质量，但当前实验主要聚焦于生成式压缩器。
- **多智能体协作系统**：本文主要研究单轮压缩器-预测器通信，对于迭代多智能体工作流（如多轮交互），初步实验（Figure 18）表明互信息在两轮后达到饱和，但系统性的理论扩展仍是开放问题。
- **推理增强模型**：本文实验主要基于GPT式非推理模型，对于推理模型（如o1系列）和混合专家模型（MoE），初步验证（Figure 9, Figure 14）表明缩放趋势仍然成立，但MoE模型因计算量取决于激活专家而非总参数，其缩放行为可能存在根本差异。

### 适用边界与失效模式

本文框架的适用性受以下边界约束：

1. **模型规模下限**：在1-3B规模的模型上，互信息估计依赖于代理模型和对数概率，可能引入偏差和方差。蒙特卡洛估计器存在理论上限 $\log(N)$，且在小样本下可能出现负值（已截断为零），这限制了其在极小模型上的可靠性。

2. **任务类型依赖**：框架在抽取式任务（如LONGHEALTH、FINANCEBENCH）上表现出强相关性（$r = -0.84, R^2 = 0.71$），但在创意任务上的相关性较弱（Figure 11 Bottom），因为创意任务的“信息量”定义本身存在模糊性。

3. **通信模式限制**：当前框架主要针对单轮压缩器-预测器通信，对于多轮交互，初步证据表明互信息在两轮后饱和，但更复杂的多智能体迭代工作流可能需要扩展信息论模型。

4. **代理模型偏差**：互信息估计器对代理模型的选择存在固定垂直偏移（Figure 13），虽然不影响缩放趋势，但在跨模型系列的绝对比较中需要谨慎解释。

### 局限与开放问题

**已识别的局限**：
- 互信息估计器依赖代理模型的对数概率，在1-3B规模的模型上可能引入偏差和方差。
- 主要聚焦于GPT式非推理模型及单轮通信场景，未必适用于推理增强模型或迭代多智能体工作流。
- 蒙特卡洛估计在小样本下可能出现负值，需截断处理，影响低信息量场景的估计精度。
- 未系统评估设备特定的效率优化以及混合专家模型（MoE）的独特缩放行为。

**开放问题**：
- 如何为语言模型输出设计更稳健、无需代理模型的互信息估计器？
- 信息论原则能否用于指导压缩器路由策略以及远程完整上下文处理的回退决策？
- 能否基于率失真分析设计训练目标，以优化压缩器-预测器通信？
- 压缩的定义除摘要外还包括结构化提取和函数调用生成，这些场景下信息论框架如何扩展？
- 混合专家模型（MoE）由于计算量取决于激活专家而非总参数，其缩放行为是否与密集模型存在根本差异？

## 原文 PDF

![[paperPDFs/ICLR_2026/An_Information_Theoretic_Perspective_on_Agentic_System_Design.pdf]]
