---
title: "PSP: Prompt-Guided Self-Training Sampling Policy for Active Prompt Learning"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/PSP_Prompt_Guided_Self_Training_Sampling_Policy_for_Active_Prompt_Learning.pdf
openreview_forum_id: 7D7VLU9227
aliases:
- PPGSTSP
- PSP
tags:
- ICLR_2026
- topic/reinforcement_learning_planning_agents
- topic/reinforcement_learning_planning_agents/deep_rl
core_operator: "引入基于Soft Actor-Critic的向量化采样策略（VSSP），通过定制实伪混合奖励和向量化critics，将提示学习中的提示信息融入采样奖励，实现端到端的样本选择策略优化，使采样过程能主动寻求对提示学习最有益的样本。"
primary_logic: "将主动提示学习建模为马尔可夫决策过程，以梯度嵌入为状态、采样概率为动作，设计实伪混合奖励函数直接反映提示学习的分类性能改进，结合不确定性增强的自训练机制，使得采样策略能够同时利用标注和未标注数据，动态适应提示模板的优化需求。"
claims:
- "PSP通过将Soft Actor-Critic与定制实伪混合奖励和向量化critics整合，利用提示引导样本选择。"
- "移除VSSP模块导致平均性能下降1.26%，证明提示引导的采样策略对性能至关重要。"
- "在DTD数据集上，PSP较最强PCB基线（PCB+AS）提升3.33%的准确率。"
- "PSP通过从提示学习过程衍生的定制奖励，桥接了样本选择和提示学习两个阶段。"
---

# PSP: Prompt-Guided Self-Training Sampling Policy for Active Prompt Learning

> [!tip] 核心洞察
> 将主动提示学习建模为马尔可夫决策过程，以梯度嵌入为状态、采样概率为动作，设计实伪混合奖励函数直接反映提示学习的分类性能改进，结合不确定性增强的自训练机制，使得采样策略能够同时利用标注和未标注数据，动态适应提示模板的优化需求。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | PSP：面向主动提示学习的提示引导自训练采样策略 |
| 英文题名 | PSP: Prompt-Guided Self-Training Sampling Policy for Active Prompt Learning |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=7D7VLU9227) |
| Topic | #topic/reinforcement_learning_planning_agents #topic/reinforcement_learning_planning_agents/deep_rl |
| Method | PSP (Prompt-Guided Self-Training Sampling Policy) |
| Dataset | DTD (ViT-B/32), Oxford Pets (ViT-B/32), Aircraft (ViT-B/32), Average over 7 datasets (ViT-B/32) |

> [!tip] 效果简介
> - DTD (ViT-B/32) 上，Final Accuracy 为 65.66，对比 62.33，变化 +3.33%。
> - Oxford Pets (ViT-B/32) 上，Final Accuracy 为 86.57，对比 83.16，变化 +3.41%。
> - Aircraft (ViT-B/32) 上，Final Accuracy 为 36.42，对比 32.27，变化 +4.15%。

## 概述

**问题瓶颈**：现有主动提示学习（APL）方法，如 **PCB**（Bang et al., CVPR 2024），将样本选择与提示学习过程解耦——先按固定标准（如Entropy、Coreset）选出样本，再训练提示模板。这导致两个后果：所选样本无法有效促进提示模板优化，且未被选中的样本中的互补信息被完全丢弃，限制了性能上限。

**核心思路**：PSP将主动提示学习建模为马尔可夫决策过程，以梯度嵌入为状态、采样概率为动作，设计**实伪混合奖励**直接反映提示学习的分类性能改进。通过将Soft Actor-Critic与向量化critics整合，使采样策略能够主动寻求对提示学习最有益的样本，从而桥接了样本选择与提示学习这两个此前被孤立处理的阶段。

**方法定位**：PSP包含两个核心模块——**向量化Soft Actor-Critic采样策略（VSSP）**负责端到端的提示引导样本选择，**不确定性增强自训练机制（UST）**利用教师模型为未选中样本生成可靠伪标签，挖掘互补信息。VSSP替换了PCB中的传统采样算法，UST则补充了伪标签数据用于学生模型训练。

**主要结果**：在ViT-B/32主干下，PSP在7个数据集上的平均准确率达76.87%，较最强PCB基线（PCB+AS）提升显著——DTD上+3.33%，Oxford Pets上+3.41%，Aircraft上+4.15%。消融实验表明，移除VSSP导致平均性能下降1.26%，移除UST下降2.10%，验证了两个模块各自的关键贡献。

## 背景与动机

### 视觉-语言模型的提示学习范式

大规模视觉-语言模型（如CLIP）通过对比预训练获得了强大的零样本迁移能力，但其性能高度依赖于手工设计的文本提示模板。提示学习（Prompt Learning）通过在连续空间中优化可学习的上下文向量，替代离散的手工提示，显著提升了下游任务的分类精度。典型的文本提示构造形式为：

$$\pmb { p } _ { c } = [ \pmb { c } ] _ { 1 } [ \pmb { c } ] _ { 2 } \ldots [ \pmb { c } ] _ { M } [ \pmb { \mathrm { c l s } } _ { c } ]$$

其中 $M$ 个可学习的上下文向量 $[\pmb{c}]_i$ 与类令牌 $[\pmb{cls}_c]$ 拼接，构成类 $c$ 的提示模板。经典方法如 **CoOp**（Zhou et al., IJCV 2022）和 **CoCoOp**（Zhou et al., CVPR 2022）在全量标注数据上取得了显著效果，但在标注预算受限的场景下，如何高效选择最有价值的样本进行标注和提示学习，成为一个关键挑战。

### 主动提示学习的现有瓶颈

主动提示学习（Active Prompt Learning, APL）将主动学习的样本选择机制引入提示学习流程，旨在用最小的标注成本逼近全量数据的提示学习性能。现有框架 **PCB**（Bang et al., CVPR 2024）建立了APL的基本范式：在每轮迭代中，先用已标注数据优化提示模板，再通过预定义的采样算法（如Entropy、Coreset、BADGE）从未标注池中选择下一批待标注样本。

然而，PCB框架存在一个核心瓶颈：**样本选择与提示学习过程完全解耦**。采样算法基于固定的启发式标准（不确定性、多样性或其混合）独立运行，不感知当前提示模板的优化状态。这意味着所选样本未必能有效促进提示模板的优化——一个在不确定性度量下得分很高的样本，可能对当前提示学习的梯度更新贡献甚微。此外，PCB直接丢弃未被选中的未标注样本，忽略了其中蕴含的互补信息，进一步限制了性能上限。

### 本文动机：提示引导的端到端采样策略

针对上述瓶颈，本文的核心动机是：**能否让提示学习过程主动引导样本选择，使采样策略直接服务于提示模板的优化目标？**

具体而言，需要解决两个关键问题：
1. **如何将提示信息注入采样决策**：设计一种机制，使得采样策略能够感知当前提示模板的状态（如梯度嵌入），并据此评估每个未标注样本对提示学习的潜在贡献，而非依赖与提示学习无关的启发式标准。
2. **如何利用未选样本的互补信息**：在主动学习预算约束下，未被查询的样本仍可能包含对模型训练有价值的信息，需要一种安全的自训练机制来挖掘这些信息，同时避免引入噪声伪标签。

基于上述动机，本文提出PSP（Prompt-Guided Self-Training Sampling Policy），将主动提示学习建模为马尔可夫决策过程，通过向量化的Soft Actor-Critic策略实现提示引导的端到端采样，并辅以不确定性增强的自训练机制，桥接样本选择与提示学习两个阶段。

## 核心创新

PSP 的核心创新在于将主动提示学习（APL）中原本被解耦的**样本选择**与**提示学习**两个阶段进行了端到端的桥接，并引入了对未选样本中互补信息的利用。具体而言，PSP 通过两个关键模块——**向量化软演员-评论家采样策略 (VSSP)** 和**不确定性增强的自训练机制 (UST)**——实现了以下两个 changed slots：

### 1. 从解耦到提示引导的样本选择策略

现有方法（如 **PCB**，Bang et al., CVPR 2024）的采样标准（Entropy、Coreset、BADGE 等）是预定义的，与下游的提示学习过程完全解耦，导致所选样本未必能有效促进提示模板的优化。PSP 通过 **VSSP** 模块从根本上改变了这一范式：

- **核心机制**：将主动提示学习建模为马尔可夫决策过程（MDP）。以未标注样本的**梯度嵌入**作为状态 $s_t$，以样本被选中的概率向量作为动作 $a_t$，并设计了**实伪混合奖励函数** $r(s_t, a_t) = \log(p_m(g)) * (\overline{r}_s + \beta \overline{r}_p)$，该奖励直接反映学生模型在提示学习后的分类性能改进。这意味着采样策略的优化信号直接源自提示学习的效果，使采样过程能主动寻求对提示模板优化最有益的样本。

- **关键设计**：VSSP 基于 **Soft Actor-Critic (SAC)** 框架，采用向量化的 V-Critic 和 Q-Critic 网络，对每个样本进行细粒度的价值估计。Actor 网络将梯度嵌入映射为选择概率后，通过**多项式采样 (Multinomial Sampling)** 构建查询集，引入随机性以避免采样偏差。同时，采用 **Soft-DTW** 对齐算法来优化 Q 值估计，消融实验表明其相比 PAD 和 VAE 分别提升最终准确率 1.83% 和 0.83%（Figure 3b）。

- **效果验证**：移除 VSSP 组件导致平均性能下降 **1.26%**（Table 2），直接证明了提示引导的采样策略对性能至关重要。

### 2. 从忽略到利用未选样本的互补信息

传统方法仅使用选中的标注样本进行训练，完全忽略了未被选中的大量未标注数据中的互补信息。PSP 通过 **UST** 模块改变了这一局面：

- **核心机制**：UST 利用上一轮（$t-1$）的教师 CLIP 模型对剩余未标注数据生成伪标签。通过对 $L$ 种数据增强的平均预测来评估不确定性和置信度，并通过**平衡伪标签选择模块 (BPLS)** 联合过滤，确保只有可靠的伪标签被纳入训练。同时，BPLS 还识别缺失类别并补充高置信度样本，以缓解类别不平衡。

- **效果验证**：伪标签正确率随轮次稳步提升，第 8 轮达到 **93.93%**（Table 5）。移除 UST 组件导致平均性能下降 **2.10%**（Table 2），表明挖掘未选样本的互补信息对性能提升贡献显著。

### 瓶颈突破总结

PSP 通过 VSSP 的提示引导采样和 UST 的互补信息挖掘，解决了现有方法“采样与学习脱节”与“信息利用不充分”两个核心瓶颈。在 DTD 数据集上，PSP 较最强 PCB 基线（PCB+AS）提升 **3.33%** 准确率；在 Aircraft 上提升 **4.15%**（Table 1）。这一性能增益来自于采样策略能够动态适应提示模板的优化需求，同时充分利用了标注与未标注数据的协同作用。

## 整体框架

![[assets/figures/papers/paper_list_l6_https_openreview_net_forum_id_7D7VLU9227/figures/002_Figure_2.jpg]]
*Figure 2: The overall structure of our PSP. The CLIP collaborative learning framework for PSP consists of two core components: the Vectorized Soft Actor-Critic Sampling Policy (VSSP) and the Uncertainty Augmented Self-Training (UST) mechanism*

PSP的整体框架围绕一个核心矛盾展开：现有主动提示学习方法（如**PCB**，Bang et al., CVPR 2024）将样本选择与提示学习视为两个独立阶段，前者基于预定义的采样标准（如Entropy、Coreset）完成，无法感知提示模板的优化需求，导致所选样本难以有效驱动提示学习，同时未标注样本中的互补信息被完全忽略。

PSP将主动提示学习建模为一个马尔可夫决策过程，通过两个协同工作的核心组件——**向量化软演员-评论家采样策略（VSSP）** 和**不确定性增强自训练机制（UST）**——实现样本选择与提示学习的端到端耦合。

**整体数据流**如下：在第 $t$ 轮，PSP接收已标注数据集 $\mathcal{D}_l$ 和未标注数据池 $\mathcal{D}_t^u$。VSSP以未标注样本的梯度嵌入作为状态，通过Actor网络输出选择概率向量，经多项采样（Multinomial Sampling）和索引器构建查询集。被选中的样本交由Oracle标注后并入 $\mathcal{D}_l$。与此同时，UST利用上一轮的教师CLIP模型对剩余未标注数据生成伪标签，通过平衡伪标签选择模块（BPLS）联合评估预测的不确定性和置信度，过滤出可靠的伪标签数据 $\mathcal{D}_p$。最终，学生CLIP模型在 $\mathcal{D}_l \cup \mathcal{D}_p$ 上通过交叉熵损失优化可学习提示模板，完成一轮迭代。

**模块间因果链路**：VSSP的奖励函数直接反映提示学习的分类性能改进——实伪混合奖励将学生模型在真实标注和伪标注样本上的预测质量（以余弦相似度差衡量）与采样方案的对数概率耦合，使得Critic网络能够评估每个样本对提示模板优化的边际贡献。UST则从互补方向挖掘VSSP未选中样本的价值，通过教师模型的集成预测（对 $L$ 次增强的logits取平均）和类别平衡填充策略，将高置信度伪标签样本注入训练，弥补标注样本的类别覆盖不足。两个模块通过共享的CLIP双分支架构（教师-学生）实现信息交换：VSSP的状态构建依赖教师模型的提示嵌入，UST的伪标签质量随提示模板的优化而逐步提升（第8轮伪标签正确率达93.93%，Table 5）。

**与PCB的关键差异**：PCB框架中，采样算法（如Entropy、BADGE）独立于提示学习运行；PSP用VSSP替换了该采样模块，使采样策略能够动态适应提示模板的优化状态（Figure 1）。消融实验证实了这一设计的必要性：移除VSSP（保留UST）导致平均准确率下降1.26%，移除UST（保留VSSP）导致下降2.10%（Table 2），验证了两组件互补协同的机制。

## 核心模块与公式推导

### 3.1 整体框架

PSP 框架由两个核心组件构成：**向量化软演员-评论家采样策略（VSSP）** 和 **不确定性增强自训练机制（UST）**。VSSP 负责将提示学习中的梯度信息融入采样决策，替代传统主动学习中与提示优化解耦的采样算法；UST 则利用教师 CLIP 模型为未标注数据生成可靠伪标签，挖掘未选中样本的互补信息。两个组件协同工作，使样本选择过程能够动态适应提示模板的优化需求。

### 3.2 提示构建与梯度嵌入状态

在提示学习阶段，类别 $c$ 的文本提示由 $M$ 个可学习上下文向量与类别令牌拼接而成：

$$\pmb { p } _ { c } = [ \pmb { c } ] _ { 1 } [ \pmb { c } ] _ { 2 } \ldots [ \pmb { c } ] _ { M } [ \pmb { \mathrm { c l s } } _ { c } ]$$

VSSP 将状态 $\pmb{s}_t \in \mathbb{R}^{n_t^u \times M_g}$ 定义为 $n_t^u$ 个未标注样本的梯度嵌入矩阵。第 $i$ 个样本的梯度嵌入基于教师图像特征与提示嵌入的余弦相似度计算：

$$\boldsymbol s _ { t } ^ { i } = \left\{ \begin{array} { l l } { { \mathbf { f } _ { V } ^ { t , i } \cdot [ 1 - \cos ( \mathcal { F } _ { T } ^ { t } ( p _ { c } ) , { \mathbf { f } _ { V } ^ { t , i } } ) ] , \mathrm { ~ i f ~ } c = \hat { y } _ { i } } } \\ { - { \mathbf { f } _ { V } ^ { t , i } \cdot \cos ( \mathcal { F } _ { T } ^ { t } ( p _ { c } ) , { \mathbf { f } _ { V } ^ { t , i } } ) , \mathrm { ~ i f ~ } c \neq \hat { y } _ { i } } } \end{array} \right.$$

该状态表示将提示嵌入的预测质量直接编码为梯度信号，使采样策略能够感知当前提示模板对每个样本的分类置信度。

### 3.3 动作空间与多项式采样

动作 $\mathbf{a}_t \in \mathbb{R}^{n_t^u}$ 是一个概率向量，每个元素表示对应未标注样本被选中的概率。VSSP 采用多项式采样（Multinomial Sampling）从动作概率中抽取查询集，引入随机性以促进样本分布的均匀性。采样方案的质量通过 MS 指标的对数概率评估：

$$\log ( p _ { m } ( g ) ) = \log ( { \frac { n _ { s } ! } { g _ { 1 } ! \cdot g _ { 2 } ! \cdot \cdot \cdot \cdot g _ { n _ { t } ^ { u } } ! } } ) + \sum _ { i = 1 } ^ { n _ { t } ^ { u } } g _ { i } \log a _ { i }$$

其中 $g_i$ 表示第 $i$ 个样本被采样的次数，$n_s$ 为查询集大小。该值越大，表明采样结果与动作概率分布的对齐程度越高。

### 3.4 实伪混合奖励

奖励函数直接反映提示学习的分类性能改进，由 MS 指标与平均实/伪奖励组合而成：

$$r ( s _ { t } , \pmb { a } _ { t } ) = \log ( p _ { m } ( g ) ) * ( \overline { { \pmb { r } } } _ { s } + \beta \overline { { \pmb { r } } } _ { p } )$$

其中单个样本的奖励 $r_k^i$ 衡量模型对该样本的预测质量——取所有类别中最大余弦相似度与真实类别余弦相似度之差：

$$r _ { k } ^ { i } = \underset { c = 1 } { \overset { K } { \operatorname* { m a x } } } \cos ( \mathcal { F } _ { T } ^ { s } ( \pmb { p } _ { c } ) , \mathcal { F } _ { V } ^ { s } ( \pmb { x } _ { i } ^ { k } ) ) - \cos ( \mathcal { F } _ { T } ^ { s } ( \pmb { p } _ { y _ { i } ^ { k } } ) , \mathcal { F } _ { V } ^ { s } ( \pmb { x } _ { i } ^ { k } ) )$$

$\overline{\mathbf{r}}_s$ 为真实标注样本的平均奖励，$\overline{\mathbf{r}}_p$ 为伪标注样本的平均奖励，超参数 $\beta$ 控制伪奖励的权重。这种设计使奖励信号直接来源于提示模板的分类表现，而非外部启发式指标。

### 3.5 向量化评论家与策略优化

VSSP 采用向量化 V-Critic 和 Q-Critic 网络，对每个样本独立估计状态值和 Q 值，实现更细粒度的采样控制。V-Critic 损失为：

$$J _ { V } ( \psi ) = \mathbb { E } _ { s _ { t } \sim \mathcal { B } } \left[ \frac { 1 } { 2 } \| V _ { \psi } ( s _ { t } ) - U _ { t } ^ { V } \| _ { 2 } ^ { 2 } \right]$$

目标 Q 值通过 Bellman 方程递归定义：

$$\hat { \pmb { Q } } ( s _ { t } , \pmb { a } _ { t } ) = r ( \pmb { s } _ { t } , \pmb { a } _ { t } ) + \gamma \mathbb { E } _ { \pmb { s } _ { t + 1 } \sim p } \left[ \pmb { V } _ { \bar { \psi } } ( \pmb { s } _ { t + 1 } ) \right]$$

Actor 网络通过重参数化技巧引入随机性，从状态 $s_t$ 采样动作：

$$\pmb { a } _ { t } ^ { \prime } = f _ { \phi } ( \epsilon _ { t } ; \pmb { s } _ { t } ) = f _ { \phi } ^ { \mu } ( \pmb { s } _ { t } ) + \star _ { t } \odot f _ { \phi } ^ { \sigma } ( \pmb { s } _ { t } )$$

Actor 的目标函数最大化动作对数概率与平均 Q 值之差，鼓励策略选择高价值样本：

$$J _ { \pi } ( \phi ) = \mathbb { E } _ { s _ { t } \sim \mathcal { D } , \epsilon _ { t } \sim \mathcal { N } } \Bigg [ \log \pi _ { \phi } \left( f _ { \phi } ( \epsilon _ { t } ; s _ { t } ) \mid s _ { t } \right) - \frac { 1 } { n _ { t } ^ { u } } \sum _ { i = 1 } ^ { n _ { t } ^ { u } } Q _ { \theta } ^ { i } ( s _ { t } , f _ { \phi } ( \epsilon _ { t } ; s _ { t } ) ) \Bigg ]$$

### 3.6 不确定性增强自训练

UST 利用上一轮的教师 CLIP 模型对未标注数据生成伪标签。通过对 $L$ 次增强的 logits 取平均获得稳定预测，BPLS（Balanced Pseudo-Label Selective）模块联合评估预测不确定性和置信度，过滤出可靠伪标签样本。对于过滤后缺失的类别，UST 从高置信度样本中补充，确保各类别伪标签数量均衡。这些伪标注数据与真实标注数据合并，用于学生模型的提示学习交叉熵损失优化。

## 实验与分析

### 主要结果

PSP在七个常见下游任务上以ViT-B/32为图像编码器进行了评估，与零样本CLIP、随机采样、多种主动学习方法（Entropy、Coreset、BADGE、GCNAL、ALFA-Mix）以及先前主动提示学习框架PCB进行了比较。Table 1展示了最终准确率结果。

![[assets/figures/papers/paper_list_l6_https_openreview_net_forum_id_7D7VLU9227/figures/003_Table_1.jpg]]
*Table 1: Final accuracy on these commonly used downstream tasks using the ViT-B/32 image encoder. The performances with the pre-trained zero-shot CLIP model are reported from (Rakesh & Jain, 2021). The performance with the entire labeled dataset during prompt learning is marked as “Fully Labeled Data”, serves as the upper bound for comparison*

PSP在所有七个数据集上均取得了最优性能，平均准确率达到**76.87%**。与最强的PCB基线（PCB+AS）相比，PSP在DTD上提升**3.33%**（65.66 vs. 62.33），在Oxford Pets上提升**3.41%**（86.57 vs. 83.16），在Aircraft上提升**4.15%**（36.42 vs. 32.27）。相较于传统主动学习方法如Entropy和Coreset，PSP的优势更为显著，验证了将提示学习信息融入采样决策的有效性。

值得注意的是，PSP在仅使用少量标注样本（8轮，每轮37个样本）的情况下，显著缩小了与全量标注数据训练上限的差距，在多个数据集上接近或超过了70%的全量数据性能。

### 消融实验

#### 核心组件消融

Table 2展示了在DTD数据集上移除PSP核心组件的影响。完整PSP模型达到68.52%的平均准确率。**移除VSSP模块**（仅保留UST）导致平均性能下降**1.26%**，降至67.26%，证明了提示引导的采样策略对性能的实质性贡献。**移除UST模块**（仅保留VSSP）导致平均性能下降**2.10%**，降至66.42%，表明自训练机制通过挖掘未选样本中的互补信息带来了更大增益。两个组件同时移除时，性能进一步下降至65.66%。

![[assets/figures/papers/paper_list_l6_https_openreview_net_forum_id_7D7VLU9227/figures/004_Table_2.jpg]]
*Table 2: Final accuracy with the ViT-B/32 CLIP image encoder on DTD. The baseline model is combined with UST, and VSSP*

这一结果揭示了VSSP和UST的协同效应：VSSP利用提示信息选择对提示学习最有益的样本，而UST则从剩余未标注数据中提取可靠的伪标签信息，两者共同构成了完整的数据利用闭环。

#### VSSP设计选择

Figure 3分析了VSSP内部设计选择的影响：
- **查询策略**（Figure 3a）：Multinomial Sampling（MS）在DTD上相比TopK选择策略提升约1.5%的最终准确率。MS引入的随机性有助于更均匀地分布所选样本，避免确定性选择可能导致的采样偏差。
- **对齐算法**（Figure 3b）：使用**Soft-DTW**进行目标Q值与Q值对齐，相比PAD和VAE分别提升**1.83%**和**0.83%**的最终准确率。Soft-DTW保留了元素间的相对顺序和结构关系，这对Q值估计的细粒度控制至关重要。
- **MS指标用法**（Figure 3c）：将MS指标作为奖励乘子（乘法形式）优于将其作为独立奖励项（加法形式），验证了MS指标对奖励信号进行缩放调节的有效性。

![[assets/figures/papers/paper_list_l6_https_openreview_net_forum_id_7D7VLU9227/figures/007_Figure_3.jpg]]
*Figure 3: Influence of different designs of the Vectorized Soft Actor-Critic Sampling Policy. (a) Different query strategies (i.e., MS and TopK) in VSSP. TopK means selecting the samples with the highest probabilities in the action. (b) Various alignment algorithms in VSSP. (c) Different usages of MS indicator within VSSP*

#### 超参数敏感度

Table 3展示了混合奖励中超参数β的影响。β控制伪奖励的相对权重，在DTD上β=0.7时达到最佳性能65.66%。β过小（0.0-0.3）时伪标签奖励贡献不足，β过大（0.9）时可能引入噪声伪标签的负面影响。

![[assets/figures/papers/paper_list_l6_https_openreview_net_forum_id_7D7VLU9227/figures/008_Table_3.jpg]]
*Table 3: Ablation study on DTD, evaluating the impact of hyperparameter $\beta$*

Figure 5分析了缓冲区阈值τ_b的影响，τ_b=1时性能最优。Table 11评估了查询大小n_s的影响，增大查询量在一定范围内可提升性能，但边际收益递减。

#### 自训练机制分析

Table 5展示了DTD数据集上各轮次伪标签的质量变化。伪标签准确率从第1轮的45.47%稳步提升至第8轮的**93.93%**，可靠伪标签数量从436增长至559。第2轮到第3轮出现大幅跃升（47.99%→83.30%），表明随着提示模板的优化，教师模型的预测质量快速改善，形成正向反馈循环。

![[assets/figures/papers/paper_list_l6_https_openreview_net_forum_id_7D7VLU9227/figures/011_Table_5.jpg]]
*Table 5: Analysis of the accuracy and the number of reliable pseudo-labeled data on the DTD dataset in each round*

Table 4将UST与半监督/无监督提示学习方法（UPL、XPL）进行了比较。UST在DTD上达到62.65%，在EuroSAT上达到81.59%，均优于UPL和XPL，验证了不确定性增强的伪标签过滤策略的有效性。

![[assets/figures/papers/paper_list_l6_https_openreview_net_forum_id_7D7VLU9227/figures/010_Table_4.jpg]]
*Table 4: Ablation study with semi-supervised and unsupervised prompt learning methods. We present the final accuracy on DTD and EuroSAT using ViT-B/32 as the image encoder for performance comparison with UPL and XPL*

### 与经典提示学习方法的比较

Table 8将PSP与经典提示学习方法CoOp和CoCoOp进行了全面比较。在七个数据集上，PSP的平均准确率（76.87%）显著优于CoOp（69.11%，+7.76%）和CoCoOp（69.49%，+7.38%）。值得注意的是，CoOp和CoCoOp使用全量标注数据训练，而PSP仅使用少量主动选择的标注样本，进一步凸显了PSP在标注效率上的优势。

![[assets/figures/papers/paper_list_l6_https_openreview_net_forum_id_7D7VLU9227/figures/020_Table_8.jpg]]
*Table 8: Ablation study with classical prompt learning methods like CoOp and CoCoOp. We report the final accuracy across seven datasets for a comprehensive comparison with CoOp and CoCoOp. Table 9: Analysis of efficiency on DTD. All models are trained on a single RTX 3090 GPU with a batch size of 32*

### 泛化性与效率分析

Table 6验证了PSP在不同视觉语言模型上的通用性。使用SigLIP作为主干网络时，PSP在四个数据集上的平均准确率达到59.23%，相比PCB的48.82%提升10.41%，其中在EuroSAT上提升最为显著（+16.72%）。

![[assets/figures/papers/paper_list_l6_https_openreview_net_forum_id_7D7VLU9227/figures/018_Table_6.jpg]]
*Table 6: Analysis of the versatility of PSP for different Vision-Language Models*

Table 10展示了不同图像编码器架构下的性能，PSP在ResNet-50、ResNet-101和ViT-B/16上均保持稳定的性能优势。Table 9的效率分析表明，PSP在DTD上的训练时间约为PCB的1.5倍（单张RTX 3090 GPU），以可接受的计算开销换取了显著的性能提升。

![[assets/figures/papers/paper_list_l6_https_openreview_net_forum_id_7D7VLU9227/figures/021_Table_9.jpg]]

### 采样策略行为分析

Table 7分析了PSP学习到的采样策略与经典主动学习策略（Coreset、Entropy、BADGE）的样本重叠率。PSP的选择与这些预定义策略存在一定重叠，但也展现出独特的采样偏好，说明PSP学习到了超越简单不确定性或多样性标准的、面向提示优化的选择模式。

![[assets/figures/papers/paper_list_l6_https_openreview_net_forum_id_7D7VLU9227/figures/019_Table_7.jpg]]
*Table 7: Analysis of the behavior of the learned sampling policy*

### 学习曲线

Figure 4展示了各方法在七个数据集上的平均学习曲线。PSP在所有轮次上均保持领先，且随着轮次增加，与PCB基线的差距持续扩大，表明VSSP的提示引导采样策略能够持续选择对提示模板优化最有益的样本，实现累积增益。Figure 8a在ImageNet上的学习曲线进一步验证了这一趋势。

![[assets/figures/papers/paper_list_l6_https_openreview_net_forum_id_7D7VLU9227/figures/009_Figure_4.jpg]]
*Figure 4: Learning curve. Average accuracy across downstream tasks with the ViT-B/32 image encoder for each round*

### 已知局限

PSP的经验回放缓冲区存储了历史状态和梯度嵌入信息，在数据高度敏感的场景下可能引发隐私泄露风险。此外，当前实验设置固定为8轮查询，超出此范围的采样策略自适应行为尚待探索。

## 方法谱系与知识库定位

### 主动提示学习的位置

PSP 处于**主动学习**与**提示学习**的交汇地带，直接继承自主动提示学习（Active Prompt Learning, APL）框架。其方法论谱系可沿两条轴线展开：提示学习一侧从 **CoOp**（Zhou et al., IJCV 2022）和 **CoCoOp**（Zhou et al., CVPR 2022）延伸到 APL 范式；主动学习一侧则涵盖基于不确定性的 **Entropy**（Holub et al., ICML 2008）、基于多样性的 **Coreset**（Sener & Savarese, ICLR 2018）、混合策略 **BADGE**（Ash et al., ICLR 2020）、图卷积方法 **GCNAL**（Caramalau et al., 2021）以及 **ALFA-Mix**（Parvaneh et al., 2022）。

PSP 的直接前驱是 **PCB**（Bang et al., CVPR 2024），后者首次将主动学习引入提示学习，但其瓶颈在于样本选择与提示学习过程解耦——采样策略（如 Entropy、Coreset、BADGE）在提示模板更新前即已固定，无法感知学习到的提示信息，且完全忽略未选中样本中的互补信息。PSP 的核心改进正是在此切入：通过 **VSSP** 将提示学习效果反馈至采样策略，并通过 **UST** 挖掘未选样本的伪标签价值，从而桥接了两个此前被独立处理的阶段。

### 与半监督/无监督提示学习的关系

PSP 的自训练机制使其与半监督提示学习（**UPL**, Huang et al., 2023）和无监督提示学习（**XPL**, 2024）产生交集。在 DTD 和 EuroSAT 数据集上的比较（Table 4）表明，PSP 中的 UST 组件在仅使用少量标注样本的条件下，其伪标签利用效率已超越这些专门设计的半监督/无监督方法。这种优势源于 UST 的平衡伪标签选择模块（BPLS）通过联合评估预测不确定性和置信度来过滤可靠伪标签，而非简单依赖阈值或一致性约束。

### 方法适用边界

PSP 的有效性在以下条件下得到验证：
- **视觉骨干**：CLIP ViT-B/32、ViT-B/16、ResNet-50/101（Table 10），以及 SigLIP（Table 6），表明方法对多种视觉语言模型具有通用性。
- **任务类型**：7 个标准细粒度分类数据集（DTD、Oxford Pets、Aircraft 等）及 ImageNet（Figure 6a），覆盖纹理、物种、场景等不同领域。
- **预算设置**：8 轮主动学习循环，每轮查询 37 个样本（与 PCB 对齐），总标注量约 296 样本。

PSP 的性能增益在细粒度任务上尤为显著——在 Aircraft 上较 PCB 提升 4.15%，在 DTD 上提升 3.33%——这类任务中类别间差异细微，提示模板的优化质量对分类精度影响更大，恰好凸显了提示引导采样的价值。

### 已知局限与开放问题

**局限**：PSP 依赖经验回放缓冲区（replay buffer）存储历史状态-动作-奖励元组以更新 SAC 策略。当数据高度敏感时，缓冲区的安全性成为关键问题，可能引发泄露风险。论文未提供针对此场景的防护方案。

**开放问题**：
1. **长程自适应**：当前实验固定 8 轮循环，当轮次数进一步增加时，采样策略能否持续自适应而不陷入过拟合或奖励饱和，尚未验证。
2. **缓冲区阈值**：缓冲区阈值 $\tau_b$ 的分析（Figure 5）仅覆盖最终准确率，其对收敛速度的影响缺乏系统性研究。
3. **大规模扩展**：ImageNet 上的初步结果（Figure 6a）显示 PSP 有效，但在完整 ImageNet-21K 或更大规模数据集上的性能尚不明确。
4. **安全机制设计**：如何在保证采样策略有效更新的同时，确保经验回放缓冲区的隐私安全，是一个工程上需要进一步探索的问题。
5. **任务泛化**：PSP 当前聚焦于图像分类，向更复杂任务（如人物交互检测、语义分割）的适配路径尚未被探索。

## 原文 PDF

![[paperPDFs/ICLR_2026/PSP_Prompt_Guided_Self_Training_Sampling_Policy_for_Active_Prompt_Learning.pdf]]
