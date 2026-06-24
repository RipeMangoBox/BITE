---
title: "Thinking on the Fly: Test-Time Reasoning Enhancement via Latent Thought Policy Optimization"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/Thinking_on_the_Fly_Test_Time_Reasoning_Enhancement_via_Latent_Thought_Policy_Optimization.pdf
openreview_forum_id: r1WEQzkCQv
aliases:
- LLTPO
- TFTTRELTPO
tags:
- ICLR_2026
- topic/generative_models_diffusion
- topic/generative_models_diffusion/generative_models_and_autoencoders
core_operator: "在测试时动态优化潜在思考向量，通过内在置信度奖励引导的策略梯度方法。"
primary_logic: "将潜在思考向量视为可动态优化的参数，利用冻结LLM的输出分布构建置信度奖励信号，并通过REINFORCE更新在测试时无需任何参数更新即显著提升推理能力。"
claims:
- "LTPO是一种无参数、仅测试时的框架，通过策略梯度优化潜在思考向量。"
- "LTPO利用基于内在置信度的奖励信号，无需外部监督。"
- "在AIME2024上，LTPO将Qwen-2.5-7B-Instruct的准确率从10.00%提升至16.67%，在基线方法全部崩溃时仍能稳健推理。"
- "AIME2024 上 Accuracy = 16.67"
---

# Thinking on the Fly: Test-Time Reasoning Enhancement via Latent Thought Policy Optimization

> [!tip] 核心洞察
> 将潜在思考向量视为可动态优化的参数，利用冻结LLM的输出分布构建置信度奖励信号，并通过REINFORCE更新在测试时无需任何参数更新即显著提升推理能力。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 即时思考：通过潜在思维策略优化实现测试时推理增强 |
| 英文题名 | Thinking on the Fly: Test-Time Reasoning Enhancement via Latent Thought Policy Optimization |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=r1WEQzkCQv); [GitHub](https://github.com/ltpo2025/LTPO) |
| Topic | #topic/generative_models_diffusion #topic/generative_models_diffusion/generative_models_and_autoencoders |
| Method | LTPO (Latent Thought Policy Optimization) |
| Dataset | AIME2024, GSM8K, MATH-500, ASDiv Aug |

> [!tip] 效果简介
> - AIME2024 上，Accuracy 为 16.67，对比 10.00，变化 +6.67。
> - GSM8K 上，Accuracy 为 81.27，对比 76.88，变化 +4.39。
> - MATH-500 上，Accuracy 为 49.00，对比 47.60，变化 +1.40。

## 概述

大型语言模型在数学推理等复杂任务上取得了显著进展，但现有潜在推理方法在挑战性、分布外任务中表现脆弱——尤其在竞赛级基准（如AIME）上，离线训练的静态投影方法准确率骤降至近乎零。核心瓶颈在于：固定的隐式推理路径无法针对每个具体问题实例进行自适应调整。

针对这一问题，本文提出**LTPO（潜在思维策略优化）**，一种无参数、仅测试时的推理增强框架。其核心思路是将中间潜在“思维”向量视为可动态优化的参数，在测试时为每个问题实例主动优化这些向量。具体而言，LTPO利用冻结LLM自身输出分布计算内在置信度奖励信号，并通过REINFORCE策略梯度方法在线更新潜在思维向量，无需任何模型参数更新或外部监督。

关键结论如下：

- **即插即用的推理增强**：LTPO无需微调或训练，仅通过测试时优化即可显著提升推理能力，在数学推理、常识推理和符号推理任务上均有效。
- **竞赛级基准突破**：在AIME2024上，LTPO将Qwen-2.5-7B-Instruct的准确率从10.00%提升至16.67%，而基线方法SoftCoT完全崩溃（0.00%）；在AIME2025上同样达到13.33%。
- **稳定且高效**：LTPO对思想令牌数量（1至16）和top-k超参数（5至100）高度鲁棒；尽管增加了优化步骤，但因大幅缩短文本生成长度，总推理时间反而快于Zero-Shot CoT（AIME2024上31.80s vs 62.59s）。
- **超越训练方法**：在不更新模型参数的前提下，LTPO在GSM8K（81.27%）、MATH-500（49.00%）和AIME2024（16.67%）上均优于Genius、SimpleRL-Zoo等基于微调的基线方法。

LTPO的核心洞察在于：将推理过程从静态生成转变为测试时动态优化，利用模型自身置信度作为导航信号，在隐空间中搜索更优的推理路径。这一范式为无需额外训练即可提升LLM推理能力提供了新方向。

## 背景与动机

大语言模型（LLM）在数学推理、常识问答等任务上已展现出显著能力，但面对竞赛级数学推理等挑战性、分布外任务时，现有方法仍表现脆弱。Zero-Shot CoT 等显式思维链方法通过生成文本级推理步骤来提升模型表现，然而这类方法依赖模型自身的文本生成能力，在高度困难的推理任务上提升有限。

潜在推理（latent reasoning）方法试图绕开文本生成的约束，在隐空间中进行推理。其中，SoftCoT 通过离线训练学习从隐向量到文本的静态投影，但该方法在竞赛级基准上表现崩溃——在 AIME2024 和 AIME2025 上，SoftCoT 在所有测试模型上的准确率均为 0.00%（Table 1）。这表明**离线学习的静态隐空间映射无法泛化到分布外的高难度推理任务**。

根本瓶颈在于：现有潜在推理方法将隐空间推理视为固定的前向传播过程，缺乏针对每个具体问题实例的动态适应能力。当任务难度超出训练分布时，静态投影无法有效捕捉问题特定的推理结构，导致准确率骤降至近乎零。

另一方面，Genius、SimpleRL-Zoo、iCoT 等基于微调的方法虽然能提升推理能力，但需要更新模型参数，计算成本高昂且难以在部署后动态调整。LatentSeek 尝试在测试时优化隐向量，但其依赖文本解码来评估优化质量，效率受限。

本文的核心动机在于：**能否在测试时动态优化潜在思考过程，而无需任何模型参数更新或外部监督信号？** 直觉上，冻结的 LLM 本身蕴含丰富的推理知识，其输出分布可以反映对潜在推理路径的“置信度”。如果将这些隐向量视为可优化的动态参数，并利用模型自身的内在置信度作为奖励信号来引导优化，就有可能在测试时为每个问题实例找到更优的隐空间推理路径。

## 核心创新

LTPO 的核心创新在于将**测试时推理增强**重新定义为一种**无参数、在线策略优化**问题。与现有方法相比，它在三个关键维度上实现了根本性转变：

### 1. 推理路径优化方式：从静态到动态

现有方法对推理路径的处理是**固定且一次性的**：Zero-Shot CoT 直接生成显式思维链，SoftCoT 通过离线训练的静态投影矩阵将隐向量映射到输出空间。这些方法在遇到分布外或高难度任务时缺乏自适应能力——如表 1 所示，SoftCoT 在 AIME2024 和 AIME2025 上的准确率**骤降至 0.00%**，暴露出静态推理路径的脆弱性。

LTPO 将中间潜在思考向量 ${\pmb H}$ 视为**可动态优化的参数**，在测试时为每个问题实例执行 $T$ 步迭代优化。具体而言，LTPO 从以当前隐向量为中心的高斯分布中采样动作以探索隐空间：

$${\pmb A}^{(t)} \sim \pi(\cdot|{\pmb H}^{(t)}) = \mathcal{N}({\pmb H}^{(t)}, \sigma^2 {\pmb I})$$

并通过策略梯度更新隐向量：

$${\pmb H}^{(t+1)} = {\pmb H}^{(t)} + \eta \cdot R({\pmb H}^{(t)} + \epsilon^{(t)}) \frac{\epsilon^{(t)}}{\sigma^2}$$

这一设计使得推理路径能够根据问题特征**自适应调整**，从根本上解决了静态方法在挑战性任务上的泛化瓶颈。

### 2. 奖励信号来源：从外部监督到内在置信度

传统推理优化方法依赖**外部监督信号**：Genius 和 SimpleRL-Zoo 需要微调模型参数并借助外部数据奖励，LatentSeek 则需在测试时进行文本解码评估，导致推理开销巨大（如表 3 所示，LatentSeek 平均每问题耗时 543.29 秒）。

LTPO 的关键突破在于从**冻结 LLM 自身的输出分布**中提取内在置信度作为奖励信号，无需任何外部监督或文本解码：

$$C({\pmb a}_i^{(t)}) = -\frac{1}{k} \sum_{v \in \mathrm{top}(k, P_i^{(t)})} \log P_i^{(t)}(v)$$

$$R({\pmb A}^{(t)}) = \frac{1}{K} \sum_{i=1}^K C({\bf a}_i^{(t)})$$

该奖励函数仅依赖单一超参数 $k$，且对 $k$ 的取值高度鲁棒——表 4 显示，$k$ 从 5 变化至 100 时，准确率波动小于 0.5 个百分点。这种**自监督奖励机制**使得 LTPO 在完全无外部标注的条件下，仍能有效引导优化过程。

### 3. 模型参数更新：从训练依赖到完全测试时

所有强基线方法均需**更新模型参数**：Genius 基于自奖励机制进行微调，SimpleRL-Zoo 利用外部数据奖励训练，iCoT 通过微调内化 CoT 步骤。这些方法不仅计算成本高，还面临灾难性遗忘和分布偏移的风险。

LTPO 实现了**完全无参数更新**：在整个优化过程中，LLM 的所有参数 $\pmb{\theta}$ 保持冻结，仅更新隐向量 ${\pmb H}$。表 2 的结果具有决定性意义——LTPO 在**不更新任何模型参数**的情况下，在 GSM8K（81.27%）、MATH-500（49.00%）和 AIME2024（16.67%）上全面超越所有训练依赖基线，其中在 AIME2024 上相对最强训练基线提升超过 6 个百分点。

**因果机制总结**：LTPO 将推理增强从“训练阶段的知识注入”转变为“测试时的路径搜索”——通过内在置信度引导的策略梯度，在冻结模型上动态优化隐向量，使得推理能力在测试时被“激活”而非“存储”。这一机制在 SoftCoT 完全崩溃的 AIME 基准上尤为突出，验证了动态优化相比静态投影的质变优势。

## 整体框架

![[assets/figures/papers/iclr26_0009_r1WEQzkCQv_Thinking_on_the_Fly_Test-Time_Reasoning_Enhancem/figures/001_Figure_1.jpg]]
*Figure 1: Overview of LTPO. The framework iteratively refines the embedding vectors of the latent thought tokens via a test-time RL loop. A confidence-based reward, calculated from the LLM’s output logits, guides the Test-time RL Module to update the latent thought vectors. After optimization, the refined vectors are concatenated with the prompt’s embeddings and passed through the LLM to generate the final answer*

LTPO（Latent Thought Policy Optimization）是一种完全在测试时运行的、无需更新模型参数的推理增强框架。其核心思想是将大语言模型（LLM）视为一个冻结的“世界模型”，而将中间潜在“思考”向量视为可动态优化的参数，通过在线策略梯度方法针对每个问题实例进行迭代精炼。

### Pipeline 总览

框架的完整推理流程由五个顺序模块构成，形成一个闭环的测试时优化系统：

1. **初始潜在向量生成**：在输入提示中插入 $K$ 个特殊的占位符令牌 `[THINK]`，通过模型的嵌入层 $E$ 将其转换为初始的潜在思考向量序列 ${\pmb H}^{(0)} = ({\pmb h}_1^{(0)}, ..., {\pmb h}_K^{(0)})$（Equation 1）。这些向量构成了优化的起点。

2. **测试时优化循环**：在 $T$ 个时间步内，系统反复执行“采样—评估—更新”的迭代过程。每一步从以当前隐向量 ${\pmb H}^{(t)}$ 为中心的高斯策略 $\pi(\cdot|{\pmb H}^{(t)}) = \mathcal{N}({\pmb H}^{(t)}, \sigma^2 {\pmb I})$ 中采样动作 ${\pmb A}^{(t)}$（Equation 2），以探索隐空间的邻域。

3. **置信度奖励计算**：将采样的动作向量与提示嵌入拼接后送入冻结的 LLM，获取输出端每个位置上的概率分布 $P_i^{(t)}$。奖励信号完全来自模型自身：对每个位置取前 $k$ 个最可能令牌的负对数概率均值作为置信度得分 $C({\pmb a}_i^{(t)})$（Equation 4），再对所有 $K$ 个位置求平均得到序列奖励 $R({\pmb A}^{(t)})$（Equation 5）。整个过程无需任何文本解码或外部监督。

4. **策略梯度更新**：利用单样本蒙特卡洛梯度估计 $\nabla_{\pmb H} J({\pmb H}^{(t)}) \approx R({\pmb H}^{(t)} + \epsilon^{(t)}) \frac{\epsilon^{(t)}}{\sigma^2}$（Equation 9），沿奖励上升方向更新隐向量：${\pmb H}^{(t+1)} = {\pmb H}^{(t)} + \eta \cdot R({\pmb H}^{(t)} + \epsilon^{(t)}) \frac{\epsilon^{(t)}}{\sigma^2}$（Equation 10）。优化完成后，选择整个过程中获得最高奖励的隐向量作为最终结果 ${\pmb H}^*$。

5. **最终答案生成**：将优化后的潜在向量与提示嵌入拼接，通过 LLM 自回归生成最终答案 ${\pmb y} = \mathrm{Decoder}(\mathcal{M}_{\pmb \theta}(E({\pmb x}) \parallel {\pmb H}^*))$（Equation 11）。

### 关键设计选择

- **无参数更新**：与 Genius、SimpleRL-Zoo、iCoT 等需要离线微调的方法不同，LTPO 完全冻结模型权重，仅在测试时优化隐向量本身。这使得方法即插即用，无需任何训练数据或计算资源进行模型更新。
- **内在置信度奖励**：区别于依赖外部监督（如 RLHF）或需要文本解码评估（如 LatentSeek）的奖励设计，LTPO 直接从冻结 LLM 的输出 logits 中提取置信度信号，避免了昂贵的外部验证和文本生成开销。
- **最佳奖励选择**：消融实验表明，选择优化过程中奖励最高的隐向量（而非最终迭代的向量）能持续提升准确率（Figure 2 右），这一策略被纳入框架的默认行为。

### 效率特性

尽管引入了 $T$ 步迭代优化，但 LTPO 在实际推理中反而快于 Zero-Shot CoT。原因在于优化后的隐向量使模型生成显著更短的文本答案——在 AIME2024 上，LTPO 的总推理时间为 31.80 秒，而 Zero-Shot CoT 需要 62.59 秒（Table 9）。优化开销（约 20 秒）被生成令牌数的大幅减少所抵消。

## 核心模块与公式推导

LTPO 的核心机制是将推理过程抽象为一个测试时的序列决策问题，在冻结语言模型的前提下，仅对潜在思考向量（latent thought vectors）进行在线策略优化。整个框架由五个关键模块串联而成。

### 1. 潜在向量的初始化

对于每个问题实例，首先在输入提示中插入 $K$ 个占位符令牌 $[\mathrm{THINK}]_1, \dots, [\mathrm{THINK}]_K$。这些令牌不携带任何语义信息，仅作为可优化的隐空间锚点。其初始嵌入向量直接通过模型的嵌入层 $E(\cdot)$ 获取：

$$(\pmb h_1^{(0)}, \dots, \pmb h_K^{(0)}) = E([\mathrm{THINK}]_1, \dots, [\mathrm{THINK}]_K) \tag{1}$$

其中 $\pmb h_i^{(0)} \in \mathbb{R}^d$ 是第 $i$ 个潜在令牌在第 0 步的初始向量，$d$ 为模型的隐藏维度。这一步将离散的占位符转化为连续空间中的可微分参数，为后续优化奠定基础。

### 2. 随机策略与探索

为避免优化陷入局部最优，LTPO 将当前潜在向量 $\pmb H^{(t)}$ 视为一个随机策略的均值，从以 $\pmb H^{(t)}$ 为中心、方差为 $\sigma^2$ 的多元高斯分布中采样动作 $\pmb A^{(t)}$：

$$\pmb A^{(t)} \sim \pi(\cdot|\pmb H^{(t)}) = \mathcal{N}(\pmb H^{(t)}, \sigma^2 \pmb I) \tag{2}$$

其中 $\pmb I$ 是单位矩阵。这一设计的关键在于：高斯噪声 $\epsilon^{(t)}$ 为隐空间探索提供了必要的随机扰动，而方差 $\sigma^2$ 控制探索的幅度。在优化过程中，$\sigma$ 按衰减因子逐步缩小，实现从粗粒度探索到精细利用的平滑过渡。

### 3. 内在置信度奖励

奖励信号的构建是 LTPO 区别于其他方法的根本创新。论文摒弃了外部监督或文本解码评估，转而从冻结 LLM 自身的输出分布中提取内在置信度作为奖励。

具体而言，将采样的动作向量 $\pmb A^{(t)}$ 与提示嵌入拼接后输入冻结模型 $\mathcal{M}_{\pmb \theta}$，获取每个位置上的词汇表概率分布：

$$(P_1^{(t)}, \dots, P_{|x|+K}^{(t)}) = \mathrm{softmax}\big(\mathcal{M}_{\pmb \theta}(E(\pmb x) \parallel \pmb A^{(t)})\big) \tag{3}$$

对于第 $i$ 个潜在令牌位置，定义其置信度得分为模型预测的前 $k$ 个最可能令牌的平均负对数概率：

$$C(\pmb a_i^{(t)}) = -\frac{1}{k} \sum_{v \in \mathrm{top}(k, P_i^{(t)})} \log P_i^{(t)}(v) \tag{4}$$

这一设计的因果逻辑是：当模型对某个位置的预测高度集中（即前 $k$ 个令牌的概率质量大）时，负对数概率小，表明模型对该位置的推理状态有较高的内在确信度。整个潜在思考序列的奖励取各位置的平均值：

$$R(\pmb A^{(t)}) = \frac{1}{K} \sum_{i=1}^K C(\pmb a_i^{(t)}) \tag{5}$$

### 4. 策略梯度更新

LTPO 采用单样本蒙特卡洛梯度估计来近似策略梯度。对于目标函数 $J(\pmb H^{(t)}) = \mathbb{E}_{\pmb A \sim \pi(\cdot|\pmb H^{(t)})}[R(\pmb A)]$，其梯度可简化为：

$$\nabla_{\pmb H} J(\pmb H^{(t)}) \approx R(\pmb H^{(t)} + \epsilon^{(t)}) \frac{\epsilon^{(t)}}{\sigma^2} \tag{9}$$

注意这里的 $\epsilon^{(t)}$ 即式 (2) 中引入的高斯噪声。该估计量的直观含义是：若采样方向 $\epsilon^{(t)}$ 带来了正向奖励，则沿该方向更新参数；奖励越高，更新步长越大。基于此，潜在向量的更新规则为：

$$\pmb H^{(t+1)} = \pmb H^{(t)} + \eta \cdot R(\pmb H^{(t)} + \epsilon^{(t)}) \frac{\epsilon^{(t)}}{\sigma^2} \tag{10}$$

其中 $\eta$ 为学习率。整个优化循环执行 $T$ 步，每步包含采样、前向传播计算奖励、梯度估计与参数更新四个子步骤。

### 5. 最终答案生成

优化完成后，选择整个过程中获得最高奖励的潜在向量 $\pmb H^*$（而非最终迭代的向量，消融实验证实前者更优），将其与提示嵌入拼接后通过解码器自回归生成最终答案：

$$\pmb y = \mathrm{Decoder}\big(\mathcal{M}_{\pmb \theta}(E(\pmb x) \parallel \pmb H^*)\big) \tag{11}$$

这一模块的关键设计选择在于“最佳奖励选择策略”：由于优化过程可能因噪声波动而偏离最优区域，回溯到奖励峰值处的隐向量能更稳定地保留优化收益。

### 模块间的因果链路

上述五个模块形成一条清晰的因果链：**初始化**提供可优化的隐空间锚点 → **随机策略**注入探索噪声 → **置信度奖励**从冻结模型内部提取优化信号 → **策略梯度**将奖励转化为隐向量的定向更新 → **最终解码**将优化后的隐状态映射为显式答案。整个链条中，模型参数 $\pmb \theta$ 始终冻结，唯一被更新的变量是潜在思考向量 $\pmb H$，这从根本上保证了方法的“无参数”特性。

## 实验与分析

### 核心发现：LTPO在挑战性基准上突破基线崩溃瓶颈

LTPO的核心优势在竞赛级基准上体现得最为尖锐。在AIME2024和AIME2025上，所有潜在推理基线（SoftCoT）全部崩溃至0.00%准确率，而LTPO不仅存活，还将Qwen-2.5-7B-Instruct的准确率从Zero-Shot CoT的10.00%推升至16.67%（AIME2024）和13.33%（AIME2025）（Table 1）。这一现象揭示了因果机制：静态投影的潜在推理在分布外任务上完全失效，而测试时动态优化赋予了模型对未知难度的适应能力。

![[assets/figures/papers/iclr26_0009_r1WEQzkCQv_Thinking_on_the_Fly_Test-Time_Reasoning_Enhancem/figures/002_Table_1.jpg]]
*Table 1: Performance of LTPO vs. baselines across four models and five reasoning benchmarks, reported in accuracy (%). The optimal results are in bold and the suboptimal ones are underlined*

跨五个数学推理基准（GSM8K、MATH-500、ASDiv Aug、AIME2024、AIME2025）的平均表现上，LTPO在四个不同规模模型上均取得最高平均准确率：LLaMA-3.1-8B-Instruct达48.66%，较Zero-Shot CoT的42.35%提升6.31个百分点（Table 1）。在相对简单的分布内任务ASDiv Aug上，LLaMA-3.1-8B-Instruct的提升幅度最大，从79.58%跃升至89.69%（+10.11pp），表明即使模型已有较强基线能力，测试时优化仍能显著压缩错误率。

### 与训练方法的对比：无参数更新的竞争力

Table 2将LTPO与三类需要更新模型参数的训练方法对比：基于自奖励微调的Genius、基于外部数据奖励的SimpleRL-Zoo、以及内化CoT步骤的iCoT。在LLaMA-3.1-8B-Instruct上，LTPO无需任何参数更新即在全部三个基准上超越所有训练基线——GSM8K上81.27%对Genius的80.40%，MATH-500上49.00%对Genius的47.60%，AIME2024上16.67%对SimpleRL-Zoo的13.33%。这一结果的关键瓶颈在于：训练方法在固定数据集上优化，难以泛化到分布外难例；而LTPO的测试时优化天然针对每个问题实例定制推理路径。

![[assets/figures/papers/iclr26_0009_r1WEQzkCQv_Thinking_on_the_Fly_Test-Time_Reasoning_Enhancem/figures/003_Table_2.jpg]]
*Table 2: Performance of LTPO vs. training-based baselines on GSM8K, MATH-500, and AIME-2024 with Llama-3.1-8B-Instruct, reported in accuracy (%). The “Train Model Params” column indicates whether the method requires updating model parameters. The symbol † indicates the accuracy is reported by Zeng et al. (2025). The optimal results are in bold and the suboptimal ones are underlined*

### 推理效率：优化开销被生成节省反超

LTPO的测试时优化循环引入额外计算，但通过大幅压缩文本生成长度，总推理时间反而显著低于Zero-Shot CoT。Table 3和Table 9给出了量化分解：在AIME2024上，LTPO平均优化时间仅1.86秒，但生成令牌数从Zero-Shot CoT的2,886降至1,420（减少50.8%），总推理时间从62.59秒降至31.80秒（减少49.2%）。在GSM8K上，LTPO总时间5.69秒，仅为Zero-Shot CoT 7.73秒的73.6%。因果链条清晰：优化后的潜在思考向量提供了更高质量的隐式推理状态，使得解码器能以更短的文本生成正确答案。

![[assets/figures/papers/iclr26_0009_r1WEQzkCQv_Thinking_on_the_Fly_Test-Time_Reasoning_Enhancem/figures/006_Table_3.jpg]]

![[assets/figures/papers/iclr26_0009_r1WEQzkCQv_Thinking_on_the_Fly_Test-Time_Reasoning_Enhancem/figures/012_Table_9.jpg]]
*Table 9: Comparison of average optimization time, generated token length, and total inference time per problem on the AIME2024 benchmark using LLaMA-3.1-8B-Instruct. The optimal results are in bold*

与另一测试时优化方法LatentSeek的对比更为极端：LatentSeek需要对每个候选进行文本解码评估，导致AIME2024上平均推理时间高达543.29秒（Prompt 1），而LTPO仅需31.80秒——效率差距超过17倍。这验证了内在置信度奖励的核心设计优势：无需文本解码即可评估推理路径质量。

### 消融研究：关键设计选择的因果验证

**思想令牌数量的鲁棒性**（Figure 2左）：LTPO在1至16个思想令牌范围内准确率保持稳定，而SoftCoT在超过4个令牌后性能急剧下降。这表明测试时优化赋予了模型有效利用更多潜在容量的能力，而静态投影方法无法扩展。

![[assets/figures/papers/iclr26_0009_r1WEQzkCQv_Thinking_on_the_Fly_Test-Time_Reasoning_Enhancem/figures/005_Figure_2.jpg]]
*Figure 2: Left: The impact of thought token numbers. Right: The impact of LTPO using thought tokens with best reward. Both are tested on ASDiv-Aug using LLaMA-3.1-8B-Instruct*

**最佳奖励选择策略**（Figure 2右）：使用整个优化过程中奖励最高的思想令牌，始终优于使用最终迭代的令牌。这揭示了优化动态中的关键现象——奖励信号在优化后期可能出现震荡或下降，盲目使用最终状态会损失性能。此发现直接指导了LTPO的最终设计选择。

**top-k超参数敏感性**（Table 4）：置信度奖励函数依赖的单一超参数k在5至100的宽范围内，三个模型在ASDiv Aug上的准确率波动均小于0.5个百分点。这证明内在置信度奖励的设计具有高度鲁棒性，无需精细调参即可稳定工作。

**固定超参数的通用性**（Table 7）：使用一组固定默认超参数（8个思想令牌、20步优化、top-k=10、σ=5、σ衰减=0.9、学习率5e-3），LTPO在LLaMA-3.1-8B-Instruct上仍取得46.83%的平均准确率，仅比逐任务调优的48.66%低1.83个百分点，且仍显著优于所有基线。这表明方法对超参数选择不敏感，具备开箱即用的实用性。

### 扩展计算下的极限性能

Table 5展示了在最大输出令牌设为64,000的扩展计算预算下，Qwen-3-14B上的LTPO将AIME2024准确率推至83.33%，AIME2025推至76.67%，平均80.00%，较Zero-Shot CoT的75.00%提升5个百分点。这表明LTPO的测试时优化与增加生成长度的推理策略可叠加获益。

### 失败模式：置信度与正确性的偏离

附录B（Table 10）揭示了一个关键失败模式：模型可能对流畅但错误的推理路径赋予更高的置信度奖励，导致优化走向错误方向。这是内在奖励机制的结构性局限——模型置信度并非正确性的完美代理。在定性示例中，LTPO赋予错误路径的奖励高于正确路径，优化过程被误导。这一发现指出了未来改进方向：需要引入不确定性估计或其他信号来更好地对齐逻辑正确性。

### 常识与符号推理的泛化验证

Table 8将评估拓展至数学之外的推理类型。在常识推理（StrategyQA）和符号推理（Date Understanding）上，LTPO在两个模型上均取得最优准确率。Qwen-2.5-7B-Instruct在符号推理上达76.40%，较Zero-Shot CoT的64.40%提升12个百分点。这证明测试时潜在优化机制不限于数学领域，对需要结构化推理的符号任务同样有效。

## 方法谱系与知识库定位

### 与基线方法的关系

LTPO 的核心贡献在于将测试时推理增强从“静态生成”或“离线训练”范式迁移至“动态优化”范式。与现有基线相比，其在三个关键维度上形成了根本性差异：

**推理路径优化方式**：Zero-Shot CoT 依赖固定的显式思维链生成，SoftCoT 通过离线训练的静态投影矩阵将隐向量映射为输出，两者均无法针对具体问题实例动态调整推理路径。LTPO 将潜在思考向量视为可优化参数，通过在线策略梯度（REINFORCE）在测试时迭代更新，使推理过程具备问题级别的自适应性。这一差异在 AIME2024/2025 等竞赛级基准上表现尤为突出——SoftCoT 准确率骤降至 0.00%（Table 1），而 LTPO 仍能维持有效推理。

**奖励信号来源**：LatentSeek 虽同为测试时优化方法，但其奖励依赖于文本解码评估，导致推理开销巨大（平均每问题 543.29 秒，Table 3）。Genius 和 SimpleRL-Zoo 则分别依赖自奖励机制和外部数据奖励，且均需离线微调模型参数。LTPO 的关键创新在于从冻结 LLM 的输出分布中直接计算内在置信度奖励（Equation 4-5），既无需文本解码，也无需外部监督，实现了奖励计算的轻量化与自动化。

**模型参数更新**：与 iCoT（内化 CoT 步骤）、Genius（自奖励微调）、SimpleRL-Zoo（外部奖励微调）等需要更新模型参数的训练型方法相比，LTPO 完全无参数更新（Table 2，“Train Model Params”列）。在 LLaMA-3.1-8B-Instruct 上，LTPO 以零参数代价在 GSM8K（81.27%）、MATH-500（49.00%）和 AIME2024（16.67%）上全面超越上述训练型基线，验证了测试时优化的独立价值。

### 适用边界

LTPO 的有效性存在明确的适用条件与边界：

**任务类型**：方法在数学推理任务上表现最为稳定，在常识推理（StrategyQA）和符号推理（Date Understanding）上亦有提升（Table 8），但其核心假设——模型置信度可代理推理正确性——在需要复杂逻辑一致性而非单纯概率校准的任务上可能失效。

**模型规模与能力**：LTPO 在四款不同规模的指令微调模型（LLaMA-3.1-8B、LLaMA-3.2-3B、Qwen-2.5-7B、Qwen-3-14B）上均取得一致提升（Table 1），表明方法对模型规模不敏感。但需注意，其提升幅度依赖于基座模型的基础推理能力——若基座模型本身无法形成有意义的输出分布，置信度奖励将失去引导价值。

**超参数鲁棒性**：top-k 超参数在 5 至 100 范围内对准确率影响小于 0.5 个百分点（Table 4），思想令牌数量从 1 至 16 时性能保持稳定（Figure 2 左），一组固定默认超参数即可保持竞争力（Table 7，固定配置平均准确率 46.83% vs 逐任务调优 48.66%）。这表明方法对超参数选择高度鲁棒，降低了实际部署的调参负担。

**计算效率边界**：LTPO 的测试时优化虽增加少量计算（AIME2024 上优化耗时 1.86 秒），但通过大幅缩短生成令牌数（从 2886 降至 1420，降幅 50.8%），总推理时间反而快于 Zero-Shot CoT（31.80 秒 vs 62.59 秒，Table 9）。这一“以优化换生成”的效率特征在长文本推理场景中具有实用价值。

### 局限与已知失效模式

**置信度-正确性偏离**：LTPO 最核心的局限在于内在置信度奖励可能与实际推理正确性不一致。模型可能对流畅但逻辑错误的推理路径赋予更高置信度，导致优化走向错误方向（Table 10 定性示例）。这是方法的内在矛盾——奖励信号来自模型自身，而模型自身的认知偏差无法通过优化过程自我纠正。

**缺乏外部验证机制**：方法完全依赖内在奖励，缺乏外部验证或 grounding 信号。在分布外任务或模型知识边界模糊的场景中，优化过程可能放大而非修正模型的系统性错误。附录 B 明确指出了这一失效模式。

**绝对准确率的局限**：尽管相对提升显著（如 AIME2024 上相对提升 66.7%），但在极难推理任务上的绝对准确率仍然较低（Qwen-2.5-7B-Instruct 上仅 16.67%）。LTPO 无法超越基座模型的能力上限，只能更充分地挖掘其已有潜力。

**优化步数的边际收益**：优化步数增加带来的收益存在边际递减。方法使用最佳奖励对应的思想令牌而非最终迭代令牌（Figure 2 右），暗示优化过程可能出现震荡或过拟合，需要额外的选择策略来稳定输出。

### 开放问题

1. **奖励信号的对齐改进**：如何将不确定性估计、逻辑一致性检验或其他校准信号结合到置信度奖励中，以缓解置信度-正确性偏离问题？这是提升方法可靠性的关键方向。

2. **搜索空间的扩展**：当前优化在连续隐空间中进行高斯探索，能否引入更结构化的搜索策略（如树搜索、束搜索）以平衡探索与利用？更大的搜索空间是否能在不显著增加计算开销的前提下进一步提升性能？

3. **多模态与长链推理的泛化**：LTPO 目前仅在文本推理任务上验证，能否扩展到视觉-语言推理、多步工具调用等需要多种模态或更长推理链的任务？隐向量在这些场景中的表征能力和优化效率有待探索。

4. **优化动态的理论理解**：REINFORCE 在隐空间中的收敛性质、奖励景观的几何结构、以及为何最佳奖励令牌优于最终迭代令牌等问题，目前缺乏理论层面的深入分析。理解这些动态有助于设计更高效的优化策略。

## 原文 PDF

![[paperPDFs/ICLR_2026/Thinking_on_the_Fly_Test_Time_Reasoning_Enhancement_via_Latent_Thought_Policy_Optimization.pdf]]
