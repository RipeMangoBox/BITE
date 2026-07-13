---
title: "Inpainting-Guided Policy Optimization for Diffusion Large Language Models"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/Inpainting_Guided_Policy_Optimization_for_Diffusion_Large_Language_Models.pdf
project_link: null
code_link: https://github.com/facebookresearch/igpo
openreview_forum_id: haVf5e4Q6C
aliases:
- IIGPO
- IGPODLLM
tags:
- ICLR_2026
- topic/reinforcement_learning_planning_agents
- topic/reinforcement_learning_planning_agents/deep_rl
core_operator: "利用扩散大语言模型的文本修复（inpainting）能力，在采样阶段灵活注入部分真实推理片段作为条件提示，从而创造奖励方差并恢复非零梯度。"
primary_logic: "扩散大语言模型的双向注意力机制天然支持补全修复，可通过注入部分真值推理『提示』来引导探索，既提供方向信号又保留策略自生成部分，在监督微调与强化学习之间搭建桥梁，缓解组优势归零困境。"
claims:
- "IGPO将全错组比例降低约60%，恢复了策略梯度信号。"
- "完整训练流程（长度对齐SFT+IGPO）在四个数学基准上平均提升7.3%（Table 1），均超越当前全注意力掩码dLLM最强结果。"
- "IGPO的训练曲线始终稳定优于标准GRPO，且不依赖于额外采样预算（Figure 10/11）。"
- "理论分析证明IGPO在零优势条件下恢复非零梯度，并通过部分提示注入线性控制KL散度。"
---

# Inpainting-Guided Policy Optimization for Diffusion Large Language Models

> [!tip] 核心洞察
> 扩散大语言模型的双向注意力机制天然支持补全修复，可通过注入部分真值推理『提示』来引导探索，既提供方向信号又保留策略自生成部分，在监督微调与强化学习之间搭建桥梁，缓解组优势归零困境。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 修复引导的扩散大语言模型策略优化 |
| 英文题名 | Inpainting-Guided Policy Optimization for Diffusion Large Language Models |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=haVf5e4Q6C) · [GitHub](https://github.com/facebookresearch/igpo) |
| Topic | #topic/reinforcement_learning_planning_agents #topic/reinforcement_learning_planning_agents/deep_rl |
| Method | IGPO (Inpainting Guided Policy Optimization) |
| Dataset | GSM8K, MATH500, AMC, Minerva Math |

> [!tip] 效果简介
> - GSM8K 上，pass@1 为 86.8 (+5.3)，对比 81.5 (LLaDA-Instruct)，变化 +5.3。
> - MATH500 上，pass@1 为 47.4 (+8.4)，对比 39.0，变化 +8.4。
> - AMC 上，avg@16 为 25.9 (+11.4)，对比 14.5，变化 +11.4。

## 概要

### 问题瓶颈

在基于组归一化优势的策略优化方法（如GRPO, **Shao et al., 2024**）中，当一组采样响应全部错误时，组内所有序列的优势值归零，导致策略梯度完全消失，该步的采样计算被白白浪费。这种现象在推理任务中尤为突出——模型在训练早期难以自行探索到正确解，形成“全错组”困境。本文的核心瓶颈即在于此：**GRPO的零优势失效模式严重损害采样效率，且模型缺乏有效的探索引导机制来跳出这一陷阱**。

### 核心方法

本文提出**修复引导的策略优化（Inpainting-Guided Policy Optimization, IGPO）**，其核心思想是：利用扩散大语言模型（dLLM）的双向注意力机制天然支持的文本修复能力，在采样阶段弹性注入部分真实推理片段作为条件提示，引导模型补全生成正确响应，从而恢复奖励方差和非零梯度。

具体而言，IGPO包含三个关键设计：

1. **弹性补全触发采样**：仅在检测到全错组时，将真值推理轨迹切分为可变长度块，随机选取部分块注入掩码序列的对应位置作为固定提示，模型通过迭代去噪补全其余位置。经验证正确的补全响应替换部分原始错误响应，恢复组内奖励方差。
2. **熵基梯度过滤**：仅对注入提示位置中前τ分位数的高熵令牌施加梯度更新，缓解分布偏移，τ=0.2时取得最佳稳定性。
3. **长度对齐SFT**：在RL之前，使用改写为简洁形式（≤1500 tokens）的推理轨迹进行监督微调，使SFT数据长度与RL采样/评估长度对齐，为策略优化提供更强初始化。

### 方法定位

IGPO在监督微调（SFT）与强化学习（RL）之间架设桥梁：它既不像纯SFT那样完全依赖真值，也不像标准RL那样放任模型盲目探索。通过部分注入真值推理“提示”，IGPO在提供方向信号的同时保留了策略自生成部分，实现了引导式探索。该方法基于**DiffuGRPO**（Zhao et al., 2025）的平均场重要性比估计器，但改变了采样过程而非目标函数形式，可视为对GRPO采样策略的结构性改进。

### 核心结论

1. **全错组大幅减少**：IGPO将全错组比例降低约60%，有效恢复了策略梯度信号（Figure 1b）。
2. **显著性能提升**：在LLaDA-8B-Instruct基座上，完整训练流程（长度对齐SFT + IGPO）在四个数学推理基准上平均提升7.3个百分点：GSM8K +5.3%、MATH500 +8.4%、AMC +11.4%、Minerva Math +4.0%，均超越当前全注意力掩码dLLM最强结果（Table 1）。
3. **稳定训练优势**：IGPO的训练曲线始终稳定优于标准GRPO，且该增益不依赖于额外采样预算——与样本匹配的GRPO重采样基线相比，IGPO仍显著更优（Figure 10/11）。
4. **理论支撑**：理论分析证明了IGPO在零优势条件下恢复非零梯度，且通过部分提示注入可线性控制KL散度，实现类信任域约束（Theorem 1, Theorem 2）。

### 局限与展望

当前工作依赖真值推理轨迹作为补全提示，在无真值或真值稀疏的任务上应用受限；评估集中在数学推理领域，尚未验证代码生成等其他复杂任务。未来方向包括：探索利用模型自身高置信度推理片段替代人工真值、将该思想迁移至自回归LLM的RL训练、以及结合更先进的搜索策略进行提示选择。



### 扩散大语言模型的独特能力

扩散大语言模型（diffusion LLMs, dLLMs）采用与自回归模型迥异的生成范式：通过双向注意力机制一次性生成完整响应，而非逐令牌自左向右解码。这种架构赋予了dLLMs一项自回归模型不具备的能力——**文本修复（inpainting）**：在生成过程中，模型可以同时条件化于前后文信息，在给定部分真实令牌作为“提示”的条件下，补全其余缺失部分。这为策略优化中的引导式探索提供了天然的机制基础。

### 组归一化优势算法中的梯度消失瓶颈

以GRPO（Shao et al., 2024）为代表的组归一化优势策略优化方法，已成为大语言模型强化学习的主流范式。其核心机制是：对同一问题采样$G$个响应，计算组内序列级优势：

$$A_i = r(o_i) - \frac{1}{G}\sum_{j=1}^{G} r(o_j)$$

然而，这一设计存在一个关键的**梯度消失困境**：当一组采样响应全部错误（即获得相同的零奖励）时，所有优势$A_i$均为零，导致策略梯度彻底消失。这类“全错组”不仅浪费了宝贵的采样计算资源，更严重的是，模型无法从这些失败样本中获得任何学习信号，难以自行探索到正确解。

### 现有方法的局限与本文动机

直接将GRPO应用于dLLMs的尝试（如DiffuGRPO、UniGRPO）虽然解决了重要性比估计等适配问题，但未能从根本上解决全错组带来的梯度消失问题。增加采样数量或简单重采样只能线性提升覆盖正确解的概率，却无法提供**方向性的探索引导**——模型仍然在盲目试错。

本文的核心洞察在于：**dLLMs的双向注意力机制天然支持补全修复，可通过注入部分真值推理“提示”来引导探索**。这一思路在监督微调（SFT）与强化学习（RL）之间架起了一座桥梁——既不像SFT那样完全依赖真值轨迹，也不像纯RL那样完全依赖随机探索，而是通过灵活注入部分真实推理片段作为条件信号，在保留策略自生成部分的同时提供方向性引导。

基于此，本文提出**IGPO（Inpainting Guided Policy Optimization）**，在GRPO的采样阶段引入弹性补全触发机制：仅当检测到全错组时，才注入部分真值推理块作为提示，通过补全生成新响应并恢复奖励方差，从而恢复非零的策略梯度信号。实验表明，IGPO将全错组比例降低约60%（Figure 1b），完整训练流程（长度对齐SFT + IGPO）在四个数学推理基准上平均提升7.3个百分点（Table 1），且训练曲线始终稳定优于标准GRPO（Figure 3）。



## 核心方法与创新机理

### 瓶颈诊断：组优势归零困境

在GRPO（Shao et al., 2024）这类组归一化优势算法中，当一组采样响应全部错误时，组内优势$A_i$归零，导致策略梯度完全消失：

$$\frac{1}{G} \sum_{i=1}^{G} \frac{1}{|o_i|} \sum_{k=1}^{|o_i|} A_i \rho_i^k \nabla_\theta \log \pi_\theta(o_i^k \mid q) = 0$$

这一零梯度现象造成大量采样计算被浪费，且模型缺乏自行探索到正确解的信号。IGPO的核心目标即针对此瓶颈，恢复有效的策略梯度。

### 核心机制：弹性补全触发采样

IGPO的关键创新在于利用扩散大语言模型（dLLM）的双向注意力机制所天然支持的**文本修复（inpainting）能力**，在采样阶段灵活注入部分真实推理片段作为条件提示。具体而言：

- **触发条件**：仅当一组$G$个采样响应全部错误（零优势场景）时，补全机制才被激活，避免不必要的计算开销。
- **提示构造**：将真实推理轨迹$y^*$分割为可变长度的连续块，按随机比例$\eta \sim \mathcal{U}[0.2, 0.6]$选取部分块，固定为提示令牌，其余位置保持掩码，由模型通过迭代去噪补全生成新响应：

$$z^{\mathrm{hint}}[i] = \begin{cases} y_i^* & \text{if } m[i]=1 \text{ and } i \leq |y^*|, \\ \mathrm{mask} & \text{otherwise}. \end{cases}$$

- **响应替换**：仅将经验证正确的补全响应纳入组内，替换部分错误响应，从而**创造奖励方差，恢复非零梯度**。理论分析证明，在全错事件条件下，IGPO恢复的梯度幅度为$\rho(1-\rho)(g_{\mathrm{correct}} - g_{\mathrm{wrong}})$，在$\rho=1/2$时最大化（Theorem 1）。

### 稳定化设计：熵基梯度过滤

注入的提示令牌来自真实轨迹，可能与当前策略分布存在偏移。IGPO引入**熵基过滤**机制：仅对提示令牌位置中熵值最高的前$\tau=0.2$分位数施加梯度更新，限制学习仅发生在模型最不确定的注入位置，从而控制策略偏移。消融实验表明$\tau=0.2$取得最佳稳定性与性能（Figure 5a）。

### 初始化对齐：长度对齐SFT

为缓解RL采样长度（256 tokens）与原始冗长推理轨迹之间的分布偏移，IGPO在RL之前引入**长度对齐监督微调**：将OpenR1-Math-220K中的冗长推理轨迹改写为简洁形式（≤1500 tokens），使SFT数据长度与后续RL采样/评估长度对齐。改写后轨迹的SFT不仅提供更强的初始策略，也为IGPO创造了更有利的起点（Figure 5b, Figure 6）。

### 与基线方法的差异总结

| 变更槽位 | 基线方法 | IGPO方案 |
|---------|---------|---------|
| 采样阶段 | 标准GRPO：从当前策略采样$G$个完整响应 | 弹性补全触发：全错时注入部分真值推理块，补全生成正确响应以恢复奖励方差 |
| 提示令牌梯度 | 无特殊处理 | 熵基过滤：仅对前20%高熵提示位置施加梯度更新 |
| 策略初始化 | 原始长篇推理轨迹SFT | 长度对齐SFT：改写为简洁形式，对齐RL采样长度 |
| 重要性比估计 | DiffuGRPO平均场近似，随机掩码应用于提示令牌 | 沿用平均场估计器，但移除提示令牌随机掩码，采用序列级重要性比 |

IGPO的目标函数与GRPO形式上一致，唯一区别在于采样过程——通过补全引导的采样替换，在零优势场景下创造有效的梯度信号。这种设计在监督微调与强化学习之间搭建了桥梁：既提供方向信号，又保留策略自生成部分。



![[assets/figures/papers/paper_list_l50_https_openreview_net_forum_id_haVf5e4Q6C/figures/003_Figure_1.jpg]]
*Figure 1: (a) Unlike autoregressive LLMs, diffusion LLMs can be conditioned on future reasoning hints during generation through inpainting via bidirectional attention, enabling guided exploration toward correct solutions. (b) Applying inpainting-guided exploration in policy optimization outperforms standard Group Relative Policy Optimization (GRPO) sampling and reduces all-wrong groups occurrences. (c) Our full training recipe combining Length-Aligned supervised fine-tuning on concise reasoning traces with IGPO achieves SoTA performance among full-attention masked dLLMs across four mathematical reasoning benchmarks*

![[assets/figures/papers/paper_list_l50_https_openreview_net_forum_id_haVf5e4Q6C/figures/004_Figure_2.jpg]]
*Figure 2: Overview of IGPO: When all sampled responses yield identical incorrect rewards (zeroadvantage scenario), we perform hint-guided inpainting by generating additional responses using ground truth reasoning chunks as injected hints. Ground truth traces $y ^ { \ast }$ are segmented into variablelength chunks, and selected chunks are injected as fixed hints during generation while the model generates the remaining tokens. We then replace a fraction of the original incorrect responses with correct responses generated through inpainting, creating reward variance that enables non-zero advantages for effective policy gradient updates*

IGPO 的核心目标是解决扩散大语言模型在 GRPO 训练中面临的**组优势归零困境**：当一组采样响应全部错误时，所有响应的奖励相同，导致优势为零、梯度消失，采样计算被完全浪费。论文提出的完整训练管线包含两个阶段，通过将扩散模型的文本修复能力与策略优化有机结合，在监督微调与强化学习之间搭建桥梁。

### 两阶段训练流程

**阶段一：长度对齐监督微调（Length-Aligned SFT）**  
基座扩散 LLM（如 LLaDA-8B-Instruct）首先在改写后的推理轨迹上进行监督微调。原始推理轨迹通常冗长且格式松散，论文通过系统性地将其改写为结构简洁、逻辑连贯的形式（长度控制在 ≤1500 tokens），使 SFT 数据的长度分布与后续 RL 采样/评估阶段的生成长度对齐。这一对齐操作有效缓解了扩散 LLM 在长序列生成中的分布偏移问题，为第二阶段 RL 训练提供了更强的初始化策略。

**阶段二：修复引导策略优化（IGPO）**  
在 SFT 初始化基础上，IGPO 对标准 GRPO 的在线采样过程进行关键修改。核心机制是**弹性补全触发采样**：当从当前策略采样的 G 个响应全部错误（即组内奖励完全相同）时，IGPO 自动触发补全引导——从真实推理轨迹中随机选取部分连续块作为条件提示，注入到掩码序列的对应位置并保持固定，模型仅对剩余掩码位置进行去噪生成。仅当补全生成的响应经验证正确时，才将其替换部分原错误响应，从而在组内创造奖励方差、恢复非零优势梯度。

为控制注入提示带来的策略偏移，IGPO 引入**熵基梯度过滤**：在计算梯度更新时，仅对注入提示位置中熵值最高的前 τ（τ=0.2）分位数令牌施加梯度，其余提示令牌不参与学习。这一机制确保模型仅在自身最不确定的提示位置进行策略调整，有效防止训练不稳定。策略估计器则沿用 DiffuGRPO 的平均场近似框架，但移除了提示令牌上的随机掩码，并采用序列级重要性比以提升稳定性。

### 输入输出流

整个管线的输入为数学推理问题及其对应的真实推理轨迹（仅在训练阶段使用真值），输出为经过两阶段优化的扩散 LLM 策略。推理阶段不依赖任何真值提示，模型完全自主生成。两阶段之间通过策略参数传递衔接，最终策略在 GSM8K、MATH500、AMC、Minerva Math 四个数学基准上均取得全注意力掩码扩散 LLM 的最优结果。



### 瓶颈与因果机制

在GRPO这类组归一化优势算法中，当一组采样的$G$个响应全部错误时，组内优势$A_i$全部归零，导致策略梯度消失——模型无法从这批样本中获得任何有效更新信号，造成采样计算的严重浪费。IGPO的核心洞察在于：扩散大语言模型（dLLM）的双向注意力机制天然支持文本修复（inpainting），可在采样阶段灵活注入部分真实推理片段作为条件提示，从而在原本全错的响应组中创造奖励方差，恢复非零梯度。

### 关键模块一：弹性补全触发采样（Elastic Inpainting-Triggered Sampling）

该模块仅在检测到全错组时触发。其工作流程为：
1. 将真实推理轨迹$y^*$（排除最终答案令牌）分割为可变长度的连续块；
2. 按随机比例$\eta \sim \mathcal{U}[0.2, 0.6]$选取部分块作为注入提示；
3. 构造提示初始化序列，将选中位置固定为真实令牌，其余位置保持掩码：

$$z^{\mathrm{hint}}[i] = \begin{cases} y_i^* & \text{if } m[i]=1 \text{ and } i \leq |y^*|, \\ \mathrm{mask} & \text{otherwise}. \end{cases}$$

4. 模型通过迭代去噪补全剩余掩码位置，生成新响应；
5. 仅保留通过正确性验证（$r(\tilde{o}_i)=1$）的补全响应，替换部分原始错误响应，使组内出现奖励方差。

该设计的精巧之处在于“弹性”触发——正常采样组不引入额外计算开销，仅在梯度信号消失时才激活引导。消融实验证实，部分提示注入（$\eta$随机）始终优于全量提示注入（$\eta=1.0$），表明保留模型自生成推理部分有助于弥合分布差距（Figure 4）。

### 关键模块二：熵基梯度过滤（Entropy-based Gradient Filtering）

注入的真实令牌来自教师轨迹，与当前策略分布存在偏移。若对所有提示令牌位置施加梯度更新，可能引发训练不稳定。IGPO采用熵基过滤策略：对每个提示令牌位置计算熵值，仅对前$\tau=0.2$分位数的高熵位置施加梯度更新。直觉上，高熵位置是模型最不确定之处，在此学习能最大化信息增益；低熵位置模型已有较强信念，强行更新易造成策略震荡。消融显示$\tau=0.2$取得最佳稳定性与性能，过滤全量提示令牌则导致训练不稳定（Figure 5a）。

### 关键模块三：长度对齐监督微调（Length-Aligned SFT）

作为RL训练的前置阶段，该模块将冗长的原始推理轨迹改写为简洁形式（≤1500 tokens），使SFT数据长度与RL采样/评估长度对齐。这一对齐操作避免了从SFT到RL阶段的分布偏移，为后续IGPO提供更强的初始化基座。实验表明，使用改写轨迹进行SFT明显优于原始轨迹SFT，且为RL带来更优的起点（Figure 5b）。

### 策略估计器

IGPO沿用**DiffuGRPO**（Zhao et al., 2025）的平均场近似估计器计算令牌级重要性比$\rho_i^k$，但做了两处关键调整：(1) 移除提示令牌上的随机掩码，避免破坏注入提示的引导信号；(2) 采用序列级重要性比以提升估计稳定性。整体目标函数与GRPO形式一致：

$$\mathcal{L}_{\mathrm{IGPO}}(\theta) = \mathbb{E}_{\{o_i,\dots,\tilde{o}_k\}\sim\mathrm{IGPO\text{-}Sample}(\pi_\theta,q,y^*)}\left[ \frac{1}{G}\sum_{i=1}^{G}\frac{1}{L_i}\sum_{k=1}^{L_i}\min(\rho_i^k A_i, \mathrm{clip}(\rho_i^k, 1-\varepsilon, 1+\varepsilon)A_i) - \beta D_{\mathrm{KL}}[\pi_\theta(\cdot|q)]\|\pi_{\mathrm{ref}}(\cdot|q)] \right]$$

唯一区别在于采样过程：全错时用补全验证正确的响应替换部分错误响应。

### 理论支撑

**定理一（梯度恢复）**：条件于全错事件，IGPO恢复非零梯度：

$$g_{\mathrm{IGPO}}(x) = \rho(1-\rho)(g_{\mathrm{correct}}(x) - g_{\mathrm{wrong}}(x)),\quad 0<\rho<1$$

梯度幅度在$\rho=1/2$时最大化，为部分提示注入提供了理论依据。

**定理二（KL控制）**：通过混合权重$\alpha$控制KL散度，部分提示注入实现类信任域约束：

$$D_{\mathrm{KL}}(\pi_{\alpha}(\cdot|x) \| \pi_\theta(\cdot|x)) \leq -\alpha \log \pi_\theta(o^{\star}|x)$$

这解释了为何部分注入优于全量注入——它在提供方向信号的同时，将策略偏移控制在可接受范围内。



## 实验与关键发现

### 1. 核心瓶颈的实证缓解：全错组与梯度恢复

IGPO的核心动机源于GRPO类算法的**组归一化优势失效**问题：当一组采样响应全部错误时，组内优势$A_i$归零，导致策略梯度为零，该组采样计算被完全浪费。实验首先验证了IGPO对这一瓶颈的缓解效果。

**全错组比例大幅下降**：如图1(b)所示，IGPO将训练过程中的全错组比例降低了约60%。这一下降直接恢复了原本被浪费的采样批次中的策略梯度信号，使模型在更多训练步骤中获得有效更新方向。

**训练曲线持续占优**：图3展示了从两个不同初始化点出发的RL训练曲线——(a)从LLaDA-8B-Instruct基座出发，(b)从长度对齐SFT检查点出发。在两种初始化条件下，IGPO的训练准确率均始终高于标准GRPO，且训练过程更加稳定。标准GRPO在训练后期出现性能波动甚至下降，而IGPO保持持续上升趋势。

![[assets/figures/papers/paper_list_l50_https_openreview_net_forum_id_haVf5e4Q6C/figures/006_Figure_3.jpg]]
*Figure 3: RL training curves of IGPO versus normal GRPO sampling. (a) Starting from LLaDA-8B-Instruct. (b) Starting from the length-aligned SFT checkpoint. IGPO exhibits superior and more stable training performance under both initialization checkpoints compared to standard GRPO sampling. Results are averaged over 3 random seeds across four mathematical reasoning benchmarks (GSM8K, MATH500, AMC and Minerva Math), with standard errors shown as shaded regions*

**梯度恢复的理论保证**：附录K中的定理1给出了IGPO梯度恢复的形式化分析。在全错事件条件下，IGPO的策略梯度为：

$$g_{\mathrm{IGPO}}(x) = \rho(1-\rho)(g_{\mathrm{correct}}(x) - g_{\mathrm{wrong}}(x)),\quad 0<\rho<1$$

其中$\rho$为正确响应在组内的比例。该梯度在$\rho=1/2$时幅度最大，表明部分提示注入在创造奖励方差和维持策略自生成之间取得了最优平衡。

### 2. 主要实验结果

表1汇总了IGPO完整训练流程（长度对齐SFT + IGPO）在四个数学推理基准上的性能表现。

![[assets/figures/papers/paper_list_l50_https_openreview_net_forum_id_haVf5e4Q6C/figures/007_Table_1.jpg]]
*Table 1: Performance across multiple mathematics tasks. GSM8K, MATH500 and Minerva are evaluated with pass@1 at temperature of 0.0, and AMC with avg@16 at temperature 0.1. Underlined scores indicate the best within each initialization group. Parenthesized deltas typeset via (+) denote absolute percentage-point improvements relative to the LLaDA-8B-Instruct baseline*

| 基准 | 指标 | IGPO完整流程 | LLaDA-Instruct基座 | 提升 |
|------|------|-------------|-------------------|------|
| GSM8K | pass@1 | 86.8 | 81.5 | +5.3 |
| MATH500 | pass@1 | 47.4 | 39.0 | +8.4 |
| AMC | avg@16 | 25.9 | 14.5 | +11.4 |
| Minerva Math | pass@1 | 13.2 | 9.2 | +4.0 |
| **平均** | — | **43.3** | **36.0** | **+7.3** |

**关键结论**：
- 完整训练流程在四个基准上平均提升7.3个百分点，均超越当前全注意力掩码扩散LLM的最强结果。
- 仅应用IGPO（无长度对齐SFT）亦能带来2.9%的平均提升，证明补全引导策略优化本身具有独立贡献。
- 在AMC基准上提升最为显著（+11.4），该基准对推理深度要求较高，暗示IGPO的引导机制对复杂推理任务尤为有效。

### 3. 消融分析：关键设计选择

#### 3.1 部分提示注入 vs. 全量提示注入

图4对比了部分提示注入（$\eta \sim \mathcal{U}[0.2, 0.6]$）与全量提示注入（$\eta = 1.0$）在三个数据集上的表现。部分注入在所有数据集上均一致优于全量注入。这一结果验证了核心设计直觉：**模型自生成的补全部分弥合了注入真值令牌带来的分布差距**，而全量注入使策略过度偏离当前分布，反而损害学习效果。

![[assets/figures/papers/paper_list_l50_https_openreview_net_forum_id_haVf5e4Q6C/figures/008_Figure_4.jpg]]
*Figure 4: Impact of hint injection ratio. across 3 datasets (GSM8K, MATH500 and AMC) and 3 seeds with standard error shown as shaded areas. We compare partial hint injection ( $\eta \sim \mathcal { U }$ [ 0 . 2 , 0 . 6 ] ) versus full hint injection (η = 1.0). Partial hint injection consistently outperforms full hint injection, demonstrating the benefits of self-generated reasoning. Both hint-guided inpainting variants outperform the baseline without any hint injection

#### 3.2 熵基梯度过滤阈值

图5a展示了不同熵过滤阈值$\tau$对性能的影响。$\tau = 0.2$（仅对前20%最高熵的提示令牌位置施加梯度更新）取得最佳性能和最稳定的训练动态。不施加过滤（$\tau = 1.0$，即更新所有提示位置）导致训练不稳定，验证了限制学习范围对控制分布偏移的必要性。

![[assets/figures/papers/paper_list_l50_https_openreview_net_forum_id_haVf5e4Q6C/figures/012_Figure_5.jpg]]
*Figure 5: (a) Impact of entropy clipping threshold on hint tokens. Performance comparison across different entropy clipping thresholds τ applied to hint token positions in IGPO, where $\tau$ = 0 . 2 represents learning from only the top 20% highest-entropy hint token positions, while $\tau$ = 1 . 0 indicates learning from all hint token positions without filtering. (b) SFT and RL dynamics with rewritten vs. original traces. We compare models fine-tuned on concise rewritten traces (max 1024 tokens) vs on original OpenR1-Math traces truncated at LLaDA’s 4096 context limit. RL is then applied (GRPO or IGPO) to both models. Rewritten traces yield stronger SFT performance and superior RL outcomes. IGPO consis...

#### 3.3 长度对齐SFT的必要性

图5b比较了使用改写后简洁推理轨迹与原始长轨迹进行SFT的效果。改写轨迹SFT产出的检查点显著优于原始轨迹SFT，且为后续RL提供了更强的初始化基座。图6进一步展示了改写前后SFT数据集的长度分布变化：改写后所有样本长度被控制在1500 tokens以内，与RL采样/评估长度对齐，避免了因长度分布不匹配导致的策略退化。

#### 3.4 直接IGPO vs. SFT前置方案

图7比较了两种训练策略：(a)直接对基座模型应用IGPO，(b)先在MetaMath上SFT 20轮、再应用标准GRPO。IGPO不仅起点更高，且在整个训练过程中保持稳定优势。SFT前置方案起步极低且训练不稳定，表明**IGPO的补全引导机制在探索引导方面的价值超越了简单增加SFT数据所能带来的收益**。

### 4. 鲁棒性与效率分析

#### 4.1 对注入噪声的鲁棒性

图9展示了在注入推理轨迹中引入合成噪声时的性能表现。IGPO在中等噪声水平下仍保持较强性能，且在所有噪声率下均持续优于GRPO。这证明IGPO并非简单地记忆注入的真值片段，而是从补全提示中提取有效的方向信号。

#### 4.2 增益来源：引导而非采样量

为排除IGPO的增益来自额外采样预算的可能性，实验设置了样本匹配的GRPO重采样基线（图10、图11）。该基线在GRPO全错时进行额外采样但不注入补全提示。结果显示，IGPO在降低全错率和提升奖励方面均显著优于样本匹配的GRPO重采样，且评估曲线持续更高。**IGPO的增益源于补全提示提供的方向性探索信号，而非单纯的采样量增加**。

### 5. 失败模式与局限性

尽管IGPO在数学推理基准上取得了显著提升，仍存在以下局限：

- **推理长度受限**：RL展开长度被限制为256 tokens以适应计算约束，这可能限制了长链推理潜力的充分发挥。
- **真值依赖**：补全提示依赖真值推理轨迹，在缺乏真值或真值稀疏的任务上无法直接应用。
- **架构限制**：当前仅在全注意力掩码扩散LLM上验证，该类模型尚未广泛支持KV缓存优化，推理成本较高。
- **阈值固定**：熵过滤阈值$\tau$被固定为0.2，虽实证有效，但未必在所有训练阶段均为最优，动态调整策略值得探索。
- **任务范围**：评估主要围绕数学推理，尚未测试代码生成等其他复杂推理任务的有效性。



## 定位与知识库关联

### 基座模型与RL范式定位

IGPO建立在**全注意力掩码扩散大语言模型**（full-attention masked dLLM）之上，以 **LLaDA-8B-Instruct**（Nie et al., 2025）为核心基座，同时与 **Dream-7B**（Ye et al., 2025）、**LLaDA-1.5**（Zhu et al., 2025）和 **d1-LLaDA**（Zhao et al., 2025）等前期掩码扩散LLM形成对比。这类模型的核心特点是双向注意力机制，使得模型天然具备文本修复（inpainting）能力——这是IGPO得以成立的关键架构前提，自回归LLM无法直接复用该设计。

在策略优化层面，IGPO直接继承**GRPO**（Shao et al., 2024）的组归一化优势框架，并沿用了面向扩散LLM的**DiffuGRPO**（Zhao et al., 2025）所引入的平均场重要性比估计器。与另一扩散LLM RL基线**UniGRPO**（Yang et al., 2025）相比，IGPO的核心差异不在于损失函数形式，而在于采样阶段的弹性补全触发机制。

### 核心改进的因果逻辑

IGPO解决的瓶颈具有明确的因果链条：GRPO的组内优势 $A_i = r(o_i) - \frac{1}{G}\sum_{j=1}^{G} r(o_j)$ 在G个响应全部错误时，所有奖励相同导致优势归零，进而使策略梯度 $\frac{1}{G}\sum_{i=1}^{G} \frac{1}{|o_i|}\sum_{k=1}^{|o_i|} A_i \rho_i^k \nabla_\theta \log \pi_\theta(o_i^k \mid q) = 0$ 完全消失。这种“全错组”现象在复杂推理任务中频繁出现，造成大量采样计算被浪费，且模型无法从失败中获取方向性信号。

IGPO的因果杠杆在于：利用扩散LLM的双向注意力，在采样时向掩码序列注入部分真值推理片段作为条件提示，构造 $z^{\mathrm{hint}}[i] = y_i^*$（当 $m[i]=1$ 时），其余位置保持掩码由模型自行补全。这在不改变GRPO目标函数 $\mathcal{L}_{\mathrm{IGPO}}(\theta)$ 的前提下，仅通过采样过程的重构恢复了奖励方差和非零梯度。理论分析（Theorem 1, Appendix K.2）证明，条件于全错事件，IGPO恢复的梯度为 $g_{\mathrm{IGPO}}(x) = \rho(1-\rho)(g_{\mathrm{correct}}(x) - g_{\mathrm{wrong}}(x))$，其中 $0<\rho<1$，梯度幅度在 $\rho=1/2$ 时最大化。

### 关键设计决策与消融证据

**部分提示注入优于全量注入**。消融实验（Figure 4）表明，注入比 $\eta \sim \mathcal{U}[0.2, 0.6]$ 始终优于 $\eta=1.0$ 的全量注入。这一现象揭示了IGPO的核心洞察：模型自行补全的部分弥合了真值推理与策略分布之间的差距，全量注入反而因分布偏移过大而降低学习效率。Theorem 2（Appendix K.3）从理论上给出了KL散度的线性控制界：$D_{\mathrm{KL}}(\pi_{\alpha}(\cdot|x) \| \pi_\theta(\cdot|x)) \leq -\alpha \log \pi_\theta(o^{\star}|x)$，为部分注入提供了理论支撑。

**熵过滤的稳定作用**。注入的真值令牌可能引入off-policy分布偏移，IGPO通过熵基过滤仅对前 $\tau=0.2$ 分位数的高熵提示令牌位置施加梯度更新。消融显示（Figure 5a），$\tau=0.2$ 取得最佳性能与训练稳定性，过滤全量提示令牌（$\tau=1.0$）则导致训练不稳定。这一机制本质上是让模型只在最不确定的注入位置进行学习，避免对已高度确定的位置做无谓的策略偏移。

**长度对齐SFT的初始化价值**。将冗长推理轨迹改写为简洁形式（≤1500 tokens）后进行SFT，不仅使SFT数据长度与RL采样/评估长度对齐，更重要的是为后续RL提供了更强的初始化基座。消融表明（Figure 5b），改写轨迹SFT在SFT阶段和后续RL阶段均优于原始轨迹SFT。直接应用IGPO（跳过SFT）与SFT-first+GRPO的对比（Figure 7）进一步显示，IGPO的弹性补全机制本身就能提供有效的探索引导，但长度对齐SFT+IGPO的组合达到最优。

### 适用边界与限制

**架构依赖性**。IGPO的全部分析和实验均在全注意力掩码扩散LLM上进行，这类模型目前尚未广泛支持KV缓存优化，推理成本较高。方法的迁移性存在明确边界：自回归LLM由于单向注意力限制，无法直接复用补全触发采样机制。

**真值依赖**。IGPO在训练阶段依赖真值推理轨迹作为补全提示来源，在缺乏真值或真值稀疏的任务（如开放式对话、创意生成）上无法直接应用。虽然鲁棒性实验（Figure 9, Appendix J）表明IGPO对注入噪声具有一定容忍度，但这仍是方法泛化的核心约束。

**任务域限制**。当前评估集中于数学推理基准（GSM8K、MATH500、AMC、Minerva Math），训练数据使用MetaMathQA，尚未在代码生成、多跳问答等其他复杂推理任务上验证。RL展开长度被限制为256 tokens以适应计算约束，可能限制了长链推理潜力的充分发挥。

**超参固化**。熵过滤阈值 $\tau=0.2$ 虽实证有效，但在整个训练过程中被固定，未探索动态调整策略（如随训练步数递增）是否能进一步提升效果。

### 开放问题

1. **跨架构迁移**：能否将条件注入部分真实片段的核心思想迁移到自回归LLM的RL训练中？可能的路径包括prefix-conditioned生成或检索增强采样，但需要全新的机制设计。

2. **无真值场景的替代方案**：当缺乏人工真值推理轨迹时，可否利用模型自身的高置信度推理片段作为替代提示？这需要解决自举偏差与确认偏误的风险。

3. **动态熵过滤**：熵过滤阈值的动态调整（如随训练步数递增 $\tau$，逐步释放更多提示令牌的学习信号）是否比固定阈值更有效？

4. **规模化验证**：IGPO在更大规模的扩散LLM（如数十B参数）上是否能保持同等幅度的提升？当前仅在8B规模验证。

5. **搜索增强**：结合更先进的搜索策略（如蒙特卡洛树搜索）进行补全提示的选择与组合，是否能进一步改善探索效率和最终效果？

6. **非推理任务泛化**：该方法对于非推理类任务（如对话对齐、安全规范遵循）的有效性如何？这些任务的真值定义和奖励结构可能与数学推理存在本质差异。



## 原文 PDF

![[paperPDFs/ICLR_2026/Inpainting_Guided_Policy_Optimization_for_Diffusion_Large_Language_Models.pdf]]
