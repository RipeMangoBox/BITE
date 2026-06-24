---
title: "GTR-Turbo: Merged Checkpoint is Secretly a Free Teacher for Agentic VLM Training"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/GTR_Turbo_Merged_Checkpoint_is_Secretly_a_Free_Teacher_for_Agentic_VLM_Training.pdf
code_link: null
aliases:
- GT
- GTR-Turbo
tags:
- CVPR_2026
- topic/other_unclear
- topic/other_unclear/general
core_operator: 在RL训练过程中不断保存模型检查点，并通过TIES模型合并技术将历史检查点合并为一个统一的教师模型；该合并模型无需额外训练，性能稳定且优于当前模型，能够作为“免费教师”为后续RL提供思维指导。
primary_logic: 合并历史检查点可以隐式地聚合过去的经验和知识，得到一个在损失面更平滑、表现更好的模型；该合并模型能够作为同源的教师，通过SFT或逆向KL散度等约束条件向当前智能体传递思维层面的过程监督，从而替代昂贵的外部API教师，实现高效、自主的Agentic VLM训练。
claims:
- 合并检查点模型在Points24上表现优于当前模型且更稳定，证明其可作为合格的教师。
- 使用GPT-4o教师需约4天及150美元，且性能仅17.5%，而GTR-Turbo免费且最终性能高达53.5%。
- GTR-Turbo在Points24和ALFWorld上达到或超越GTR的性能，同时训练时间和计算成本大幅降低（KL变体训练时间减半，成本降低约60%）。
- 消融实验表明使用静态初始模型无法稳定提升，而模型合并是必要的。
---

# GTR-Turbo: Merged Checkpoint is Secretly a Free Teacher for Agentic VLM Training

> [!tip] 核心洞察
> 合并历史检查点可以隐式地聚合过去的经验和知识，得到一个在损失面更平滑、表现更好的模型；该合并模型能够作为同源的教师，通过SFT或逆向KL散度等约束条件向当前智能体传递思维层面的过程监督，从而替代昂贵的外部API教师，实现高效、自主的Agentic VLM训练。

| 字段 | 内容 |
|------|------|
| 中文题名 | GTR-Turbo：以合并检查点为免费教师的Agentic VLM训练 |
| 英文题名 | GTR-Turbo: Merged Checkpoint is Secretly a Free Teacher for Agentic VLM Training |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2512.13043) |
| Topic | #topic/other_unclear #topic/other_unclear/general |
| Method | GTR-Turbo |
| Dataset | Points24, ALFWorld, Android-in-the-Wild |

> [!tip] 效果简介
> - Points24 上，Success Rate (SR %) 53.5 (GTR-Turbo KL) vs 44.5 (GTR) (+9.0)；Episode Return (ER) 2.39 (GTR-Turbo KL) vs 0.53 (GTR) (+1.86)。
> - ALFWorld 上，Average Success Rate 0.15 (GTR-Turbo KL) vs 0.16 (GTR) (-0.01)。
> - Android-in-the-Wild 上，Success Rate (%) 80.2 (GTR-Turbo) vs 75.0 (PPO) (+5.2)。

## 概述

**问题瓶颈**：多轮视觉语言模型（VLM）智能体的强化学习（RL）训练面临“思维崩溃”（thought collapse）的严峻挑战——由于环境奖励极度稀疏且缺乏过程监督，模型的推理输出容易退化为重复、不连贯的模板化文本。原始GTR框架通过调用外部API教师模型（如GPT-4o）提供步骤级思维指导来缓解这一问题，但代价高昂：以Points24任务为例，使用GPT-4o教师训练15,000步需要约4天时间和约150美元，且教师自身在该任务上的性能仅为17.5%（Table 1）。这种对外部大模型的依赖严重制约了Agentic VLM训练的可扩展性。

**核心思路**：GTR-Turbo提出了一种“自持训练”范式——**将RL训练过程中不断保存的历史模型检查点通过TIES模型合并技术融合为一个统一的“免费教师”**，然后用该合并模型为后续RL提供思维指导。其关键洞察在于：合并历史检查点能够隐式聚合过去的探索经验，得到一个在损失面更平滑、性能更稳定且优于当前训练模型的教师（Figure 2），从而替代昂贵的外部API调用，实现高效、自主的Agentic VLM训练。

**方法定位**：GTR-Turbo在原始GTR的PPO框架基础上进行了两个关键槽位替换——将**教师模型**从外部API大模型替换为本地检查点合并模型，将**思维指导损失**从仅支持自回归生成的SFT损失扩展为可选择SFT损失或基于逆向KL散度的软惩罚（后者仅需单次前向传播，推理效率更高）。该方法不引入额外训练开销，仅需在RL过程中维护一个检查点缓冲区并周期性执行模型合并。

**主要结果**：在Points24复杂卡牌游戏任务上，GTR-Turbo（KL变体）以**53.5%的成功率**和**2.39的回合回报**显著超越原始GTR（44.5%, 0.53），同时将训练时间缩短50%、API调用降至零、额外计算成本降低约60%（Table 2, Table 4）。在ALFWorld具身推理任务上，GTR-Turbo以更少的训练时间和计算成本达到了与GTR可比的性能（Table 3）。在Android-in-the-Wild GUI操作任务上，GTR-Turbo以80.2%的成功率超越PPO基线（75.0%），验证了方法的跨环境泛化能力（Table 6）。

**方法谱系与知识库定位**：GTR-Turbo属于**自持式RL训练**方法，其核心创新——以模型合并构建免费教师——与以下工作形成对比：原始**GTR**依赖外部API教师提供思维校正；**RL4VLM**（Zhai et al., NeurIPS 2025）直接将PPO应用于原始环境奖励，缺乏过程监督机制；基于静态模型的KL正则化自改进方法无法稳定提升性能（Figure 6消融实验）。在模型合并技术层面，GTR-Turbo采用**TIES合并**（Yadav et al., NeurIPS 2024），通过修剪、符号选举和选择性平均有效避免了参数干扰，相比简单线性平均显著提高了教师质量（Figure 8）。

## 背景与动机

### 多轮VLM智能体的“思维崩溃”困境

以视觉语言模型（VLM）为基座的智能体在交互式决策任务中展现出巨大潜力，但通过强化学习（RL）对其进行多轮训练时面临一个核心瓶颈：**环境奖励稀疏且缺乏过程监督**。在典型的VLM智能体RL训练中，智能体仅在回合结束时收到标量奖励信号（如任务成功/失败），这导致其内部推理过程（thought）逐渐退化为重复、不连贯的模板化输出——这一现象被称为“思维崩溃”（thought collapse）。

直接应用PPO等策略优化算法（如 **RL4VLM**，Zhai et al., NeurIPS 2025）无法有效防止这种退化，因为动作层面的奖励信号无法为思维质量提供足够的梯度引导。智能体为了最大化稀疏的终端奖励，倾向于放弃有意义的推理探索，转而生成空洞的思维内容，最终损害泛化能力和任务成功率。

### 原始GTR及其外部教师依赖

为解决思维崩溃问题，**GTR**（Guided Thought Reinforcement）框架引入了“VLM作为校正器”的机制：在RL训练的每一步，调用一个外部多模态大模型（如GPT-4o或Gemini）对智能体生成的思维内容进行评估和精炼，然后将校正后的思维作为监督信号，通过联合优化**PPO动作损失**和**SFT思维损失**来引导训练：

$$
\operatorname*{min}_{\theta} \underset{(o,a)\sim B}{\mathbb{E}} \mathcal{L}_{\mathrm{PPO}}(o,a) + \underset{(o,th)\sim D}{\mathbb{E}} \mathcal{L}_{\mathrm{SFT}}(o,\pi_{\mathrm{corr}}(o,th))
$$

这一方法在Points24等复杂任务上取得了显著效果，但其**可扩展性受到严重制约**。如Table 1所示，使用GPT-4o作为教师模型训练LLaVA-v1.6-mistral-7B仅15,000步就需要约86小时（~4天）和约150美元的API调用费用，且GPT-4o教师自身在Points24上的表现仅为17.5%。更关键的是，外部API教师引入了不可控的延迟、成本波动和访问限制，使得大规模、长时间的智能体训练在经济上和技术上都难以持续。

### 核心动机：从外部教师到自我引导

本文的核心动机在于回答一个根本性问题：**能否在不依赖任何外部大模型的情况下，为VLM智能体的RL训练提供高质量的思维过程监督？**

直觉上，RL训练过程中不断产生的历史模型检查点蕴含着智能体在不同训练阶段积累的经验和知识。如果能够有效聚合这些历史检查点，就有可能得到一个性能优于当前智能体、且更为稳定的“教师模型”——该教师与当前智能体同源，无需额外训练，也不产生API调用成本。这一洞察构成了**GTR-Turbo**的核心假设：**合并历史检查点可以隐式地聚合过去的经验，得到一个在损失面更平滑、表现更好的模型，从而作为“免费教师”替代昂贵的外部API，实现高效、自主的Agentic VLM训练。**

## 核心创新

GTR-Turbo 的核心创新在于**将 RL 训练过程中自然产生的历史检查点转化为“免费教师”**，从而彻底消除了原始 GTR 框架对外部昂贵 API 教师模型（如 GPT-4o）的依赖。这一转变通过两个关键的技术槽位替换实现。

### 教师模型的自主化：从外部 API 到合并检查点

原始 **GTR** 框架依赖外部多模态大模型（如 GPT-4o 或 Qwen2.5-VL-72B）作为“校正器”（corrector），在每一步 RL 中对智能体的思维内容进行评估和修正。这种机制带来了严重的瓶颈：**Table 1** 显示，使用 GPT-4o 作为教师训练 15,000 步需要约 86 小时和约 150 美元，且教师自身的任务成功率仅 17.5%；而使用同规模的 Qwen2.5-VL-7B 作为教师则完全无法提供有效的思维指导（成功率为 0%）。

GTR-Turbo 的解决方案是**将 RL 训练过程中保存的历史检查点通过 TIES 模型合并技术聚合为一个统一的教师模型**。如 **Figure 2** 所示，合并后的检查点（红色曲线）在 Points24 任务上的表现持续优于当前训练的智能体（蓝色曲线），且更为稳定。这证明了合并模型不仅无需额外训练，还因在更平滑的损失面上优化而具备更强的性能，能够胜任教师角色。合并过程采用 **TIES**（Trim, Elect Sign, and Merge）方法，通过修剪低幅值参数、选举符号方向和选择性平均，有效避免了直接平均带来的参数干扰，确保教师模型的质量（**Figure 8** 消融实验证实了 TIES 相对于简单线性平均的优势）。

### 思维指导机制的灵活化：从 SFT 到逆向 KL 散度

原始 GTR 仅支持基于 SFT 损失的思维指导——需要教师模型自回归生成完整的思维序列作为监督信号。GTR-Turbo 在此基础上引入了**基于逆向 KL 散度的软惩罚机制**，提供了两种可选的思维传递方式：

- **SFT 变体**：将合并教师输出的思维 $\hat{th}$ 作为硬标签，通过交叉熵损失直接监督智能体的思维生成，损失函数为 $\min_\theta \mathbb{E}_{(o,a)\sim\mathcal{B}} \mathcal{L}_{\mathrm{PPO}}(o,a) + \mathbb{E}_{(o,\hat{th})\sim\mathcal{D}} \mathcal{L}_{\mathrm{SFT}}(o,\hat{th})$。
- **KL 变体**：将逆向 KL 散度作为奖励惩罚项嵌入 PPO 目标中，修改后的优势函数为 $A' = A^{\pi_\theta}(o,a) - \mathrm{RevKL}(\pi_\theta,\pi_{\mathrm{merged}}; th)$，其中 $\mathrm{RevKL}$ 衡量学生与教师在思维 token 分布上的逐 token 差异。这一设计的关键优势在于**仅需教师模型单次前向传播**即可计算惩罚信号，无需自回归生成，从而大幅降低了计算开销。

**Table 4** 的成本对比清晰地展示了这一创新的实际收益：GTR-Turbo (KL) 在 Points24 上达到 54% 成功率（超越 GTR 的 44.5%），训练时间却从 GTR 的 78 小时降至与纯 RL 基线相当的约 40 小时，额外计算成本降低约 60%。在 ALFWorld 上，GTR-Turbo 以 15% 的成功率与 GTR（16%）持平，同样实现了显著的效率提升。

### 创新的本质：经验聚合与过程监督的内化

从机制层面看，GTR-Turbo 的创新可以理解为**将外部知识注入转化为内部经验聚合**。合并检查点隐式地聚合了 RL 探索过程中的多样化经验，在损失面上形成了一个更优的“重心”。这个同源教师通过 SFT 或 KL 约束向当前智能体传递思维层面的过程监督，既抑制了 RL 训练中常见的“思维崩溃”现象（**Figure 14** 的推理分数评测证实了这一点），又保留了智能体在动作空间的探索自由度——**Figure 7** 的消融实验表明，仅指导思维部分优于同时指导思维和动作，因为后者限制了模型探索，而探索正是 GTR-Turbo 自我进化的关键驱动力。

## 整体框架

GTR-Turbo 的核心思想是用RL训练过程中自然产生的历史检查点，通过模型合并技术构建一个“免费”的教师模型，替代原始GTR框架中昂贵的外部API教师（如GPT-4o），为Agentic VLM的强化学习训练提供思维层面的过程监督。整个框架由五个关键模块串联而成，形成闭环的自我进化训练流程。

### 框架总览

如图3所示，GTR-Turbo在标准VLM智能体RL训练的基础上，插入了三个核心机制：**检查点缓冲区（Checkpoint Buffer）**、**TIES模型合并（TIES Model Merging）** 以及**思维指导变体选择器（Guidance Variant Selector）**。训练流程如下：

1. **PPO探索与数据收集**：当前智能体 $\pi_\theta^{(k)}$ 在环境中执行动作，生成包含观察 $o$、思维 $th$ 和动作 $a$ 的轨迹，存入经验缓冲区 $\mathcal{B}$。
2. **检查点存储**：每次PPO更新后，将当前模型权重保存至检查点缓冲区，形成历史模型集合 $\{\pi_\theta^{(1)}, \pi_\theta^{(2)}, ..., \pi_\theta^{(k-1)}\}$。
3. **教师模型合并**：通过TIES合并技术，将缓冲区中的历史检查点融合为一个统一的教师模型 $\pi_{\mathrm{merged}}^{(k)}$。该合并模型无需任何额外训练，且性能稳定地优于当前训练中的智能体（见图2），能够作为合格的思维指导教师。
4. **思维指导注入**：在下一轮PPO更新时，根据选择的指导变体（SFT或KL），将合并教师的思维信号注入当前智能体的优化目标中，引导其保持理性、连贯的推理过程，防止“思维崩溃”。
5. **迭代循环**：重复步骤1-4，智能体在自我探索与合并教师的引导之间交替迭代，实现自主进化。

### 模块职责与数据流

| 模块 | 输入 | 输出 | 核心功能 |
|------|------|------|----------|
| **Checkpoint Buffer** | 每轮PPO更新后的模型权重 $\pi_\theta^{(i)}$ | 历史检查点集合 | 存储RL训练过程中产生的模型快照，为后续合并提供原料 |
| **TIES Model Merging** | 缓冲区中 $k-1$ 个历史检查点 | 合并教师模型 $\pi_{\mathrm{merged}}^{(k)}$ | 通过修剪（Trim）、符号选举（Elect Sign）和选择性平均（Merge）消除参数干扰，生成高质量教师 |
| **Merged Teacher Model** | 合并后的权重 | 思维token的logits或生成文本 $\hat{th}$ | 为当前智能体提供思维层面的参考分布或监督信号 |
| **PPO Update with Thought Guidance** | 经验批次 $\mathcal{B}$、教师思维信号 | 更新后的策略 $\pi_\theta^{(k+1)}$ | 在标准PPO动作损失基础上，叠加SFT损失或逆向KL散度惩罚，实现动作优化与思维对齐的联合训练 |
| **Guidance Variant Selector** | 配置选择（SFT/KL） | 对应的损失函数或奖励修正项 | 切换两种思维传递模式：SFT模式需教师自回归生成完整思维序列；KL模式仅需单次前向传播计算token级分布差异 |

### 两种思维指导模式

GTR-Turbo提供两种可选的思维指导机制，在计算效率与指导精度之间提供灵活权衡：

- **SFT指导（Section 3.3）**：合并教师模型对缓冲区中的观察 $o$ 自回归生成思维序列 $\hat{th}$，将其作为监督标签，通过交叉熵损失 $\mathcal{L}_{\mathrm{SFT}}(o, \hat{th})$ 直接训练当前智能体的思维生成能力。该方式指导信号精确，但需要教师模型逐token生成，推理开销相对较高。

- **KL指导（Section 3.4）**：计算当前智能体与合并教师在思维token上的逆向KL散度 $\mathrm{RevKL}(\pi_\theta, \pi_{\mathrm{merged}}; th)$，将其作为负奖励项从PPO的优势函数中扣除：
  $$A' = A^{\pi_\theta}(o,a) - \mathrm{RevKL}(\pi_\theta, \pi_{\mathrm{merged}}; th)$$
  该方式仅需教师模型一次前向传播即可获得完整token分布，大幅降低计算成本。消融实验表明，使用裁剪（clipping）将KL值限制在非负范围效果最优（图9），这源于逆向KL的模式寻求（mode-seeking）特性——它鼓励学生覆盖教师的高概率区域，而非平均匹配整个分布。

### 与原始GTR的关键差异

原始GTR框架（图1）依赖外部API模型（如GPT-4o）作为“校正器”，在每一步RL中评估并修正智能体的思维内容。这一设计导致两个根本性瓶颈：（1）**计算开销巨大**——使用GPT-4o训练15,000步需约4天时间和约150美元API费用（Table 1）；（2）**扩展性受限**——依赖第三方API意味着训练速度和成本不受自主控制，且存在服务可用性风险。

GTR-Turbo通过将教师模型**内部化**和**自主化**，彻底消除了对外部API的依赖。合并检查点模型不仅完全免费，而且作为同源教师，其输出分布与当前智能体天然兼容，避免了跨模型分布差异引入的噪声。这一设计使得训练时间减半、计算成本降低约60%（Table 4），同时最终性能超越原始GTR（Points24成功率53.5% vs. 44.5%）。

### 补充图表

![[assets/figures/papers/paper_list_l2394_https_arxiv_org_abs_2512_13043/figures/004_Figure_3.jpg]]
*Figure 3: Overview of the GTR-Turbo framework. Beyond the GTR training of VLM agents (Figure 1), GTR-Turbo stores historical checkpoints and merges them into a teacher model (blue region), and then incorporates the PPO update (orange region) with thought guidance by minimizing either SFT loss (green region) or KL divergence (purple region), enabling flexible, scalable, and self-guided agentic RL training*

## 核心模块与公式推导

### 3.1 原始GTR框架的瓶颈

GTR（Guided Thought Reinforcement）的核心机制是“VLM作为校正器”：在每一步RL中，外部VLM模型（如GPT-4o或Gemini）评估并修正智能体的思维内容，然后将修正后的思维作为监督信号，与PPO动作损失联合训练。其目标函数为：

$$
\operatorname*{min}_{\theta} \underset{(o,a)\sim B}{\mathbb{E}} \mathcal{L}_{\mathrm{PPO}}(o,a) + \underset{(o,th)\sim D}{\mathbb{E}} \mathcal{L}_{\mathrm{SFT}}(o,\pi_{\mathrm{corr}}(o,th))
$$

其中 $\mathcal{L}_{\mathrm{PPO}}$ 是标准的裁剪PPO代理损失，$\mathcal{L}_{\mathrm{SFT}}$ 是对校正后思维的监督微调损失。这一框架有效解决了“思维崩溃”问题，但存在根本瓶颈：外部API教师模型调用成本高、耗时长、可扩展性差。如表1所示，使用GPT-4o作为教师训练15,000步需约86小时和约150美元，且教师自身性能仅17.5%。

### 3.2 核心模块：检查点合并教师模型

GTR-Turbo的关键创新在于**将RL训练过程中产生的历史检查点合并为一个“免费”教师模型**，替代昂贵的外部API。其核心模块包括：

- **Checkpoint Buffer**：存储RL训练过程中产生的历史模型权重 $\pi_{\theta}^{(1)}, \pi_{\theta}^{(2)}, ..., \pi_{\theta}^{(k-1)}$。
- **TIES Model Merging**：采用TIES（Trim, Elect Sign, and Merge）技术对缓冲区检查点进行修剪、符号选举和选择性平均，避免参数干扰。合并后的教师模型在第 $k$ 次更新时为：

$$
\pi_{\mathrm{merged}}^{(k)} = \sum_{i=1}^{k-1} w_i \pi_{\theta}^{(i)}
$$

最简单的权重分配是简单移动平均（SMA）：$w_i = \frac{1}{k-1}$。合并教师无需额外训练，通过在更平滑的损失面上优化，隐式聚合过去经验，性能稳定且优于当前智能体（图2）。

- **Merged Teacher Model**：合并操作得到的教师模型，与LoRA微调的智能体分别部署在不同GPU上，为后续RL提供思维指导。

### 3.3 思维指导变体一：SFT损失

在SFT变体中，合并教师对重放缓冲区中的观察 $o$ 自回归生成思维 $\hat{th}$，然后将其作为监督信号加入PPO损失：

$$
\operatorname*{min}_{\theta} \underset{(o,a)\sim \mathcal{B}}{\mathbb{E}} \mathcal{L}_{\mathrm{PPO}}(o,a) + \underset{(o, \hat{th})\sim \mathcal{D}}{\mathbb{E}} \mathcal{L}_{\mathrm{SFT}}(o, \hat{th})
$$

该方式直接传递教师的生成思维，但需要教师进行自回归推理，计算开销相对较高。

### 3.4 思维指导变体二：逆向KL散度惩罚

KL变体将思维指导从显式的SFT损失替换为基于逆向KL散度的软惩罚，仅需教师单次前向传播即可计算。核心思想是将PPO的优势函数减去逆向KL散度作为惩罚项：

$$
\operatorname*{max}_{\theta} \underset{(o,(th,a))\sim \mathcal{B}}{\mathbb{E}} \left[ \min\left( r A', \operatorname*{clip}(r, 1-c, 1+c) A' \right) \right]
$$

其中 $A' = A^{\pi_{\theta}}(o,a) - \mathrm{RevKL}(\pi_{\theta},\pi_{\mathrm{merged}}; th)$，$r = \frac{\pi_{\theta}(a|o)}{\pi_{\theta_{\mathrm{old}}}(a|o)}$ 为重要性采样比率。

**逆向KL散度**定义为学生模型与教师模型在思维token上的逐token差异：

$$
\mathrm{RevKL}(\pi_{\theta},\pi_{\mathrm{merged}}; th) = \mathbb{E}_l \left[ \log \pi_{\theta}(th_{[l]}|th_{[<l]}) - \log \pi_{\mathrm{merged}}(th_{[l]}|th_{[<l]}) \right]
$$

在实现中，对KL值进行裁剪（$\mathrm{clip}(\cdot, 0, +\infty)$）以控制惩罚幅度，消融实验表明裁剪方法优于绝对值、K3估计器和前向KL等方法（图9），这验证了逆向KL的模式搜索优势。

### 3.5 模块协同与变体选择

GTR-Turbo框架通过**Guidance Variant Selector**在SFT损失与KL散度惩罚之间灵活切换。SFT变体直接传递教师思维，训练更稳定；KL变体仅需并行推理，将总训练时间降至RL4VLM水平（约为GTR的一半），成本降低约60%（表4）。两种变体均通过PPO更新模块将思维指导与动作优化联合进行，实现自主、可扩展的Agentic VLM训练。

### 补充图表

![[assets/figures/papers/paper_list_l2394_https_arxiv_org_abs_2512_13043/figures/003_Figure_2.jpg]]
*Figure 2: The performance comparison of the merged checkpoint and the current checkpoint on Points24. We adopt the Qwen2.5-VL-7B as the base model and highlight that model merging leads to a stronger and more stable agent*

## 实验与分析

### 核心实验设置

所有RL方法均以 **Qwen2.5-VL-7B** 为骨干网络，采用相同的LoRA配置和PPO超参数（见 Table 5），并遵循GTR提出的early-truncation策略以保证公平比较。GTR-Turbo使用两块40GB NVIDIA GPU，一块部署合并教师模型，另一块运行LoRA微调的智能体。教师模型仅需本地前向推理，无需任何外部API调用。

### 主要结果

#### Points24 任务：全面超越

Table 2 汇总了Points24任务上的最终性能。GTR-Turbo（KL变体）以 **53.5%** 的成功率和 **2.39** 的回合回报（Episode Return）取得最优，相较于原始GTR的44.5%和0.53分别提升 **+9.0%** 和 **+1.86**。值得注意的是，原始GTR依赖GPT-4o作为外部教师，不仅性能受限于教师质量（仅17.5%），还需约4天训练时间和150美元API成本（Table 1），而GTR-Turbo完全消除了这一依赖。

![[assets/figures/papers/paper_list_l2394_https_arxiv_org_abs_2512_13043/figures/002_Table_1.jpg]]
*Table 1: Training time and token usage of the GTR framework. Experiments to train the LLaVA-v1.6-mistral-7B model for 15,000 steps on the Points24 task, using different models as the corrector. * - The corrector model fails to provide valid thought guidance*

**Table 2** 展示了各模型在Points24上的成功率和回合回报，GTR-Turbo KL在两项指标上均显著领先。

Figure 4 的训练曲线揭示了更深层的动态：GTR在训练早期受益于外部知识，收敛更快，但GTR-Turbo能够维持稳定的推理过程，最终在后期实现反超。这表明合并教师模型提供的思维指导在长期训练中更具持续性和鲁棒性。

![[assets/figures/papers/paper_list_l2394_https_arxiv_org_abs_2512_13043/figures/006_Figure_4.jpg]]
*Figure 4: Training curves on the Points24 game environment. While GTR benefits from external knowledge in the early stage, our GTR-Turbo framework is also able to maintain a rational reasoning process and ultimately achieves the best overall performance. All curves are smoothed for better readability. All experiments employ the early-truncation strategy introduced by GTR for a fair comparison*

#### ALFWorld 任务：等效性能，成本大幅降低

在ALFWorld环境中，GTR-Turbo（KL）取得了 **0.15** 的平均成功率，与原始GTR的0.16基本持平（Table 3）。然而，这一等效性能是在训练时间大幅缩短的前提下实现的。

![[assets/figures/papers/paper_list_l2394_https_arxiv_org_abs_2512_13043/figures/008_Table_3.jpg]]
*Table 3: Comparison of success rates across different models in the ALFWorld environment. We present the peak performance in the training curve for RL methods. GTR-Turbo achieves the same task success rate compared to GTR with significantly less training time and lower computational cost, maintaining excellent performance under its model scale. * - Reported in previous work*

**Table 3** 呈现了ALFWorld各子任务的峰值成功率，GTR-Turbo在无需外部模型的情况下达到与GTR相同的任务成功率。

Figure 5 的训练曲线显示，GTR-Turbo完全依靠自身的探索、经验和思维指导，在训练中后期逐步逼近GTR的性能水平，证明了自持训练框架的有效性。

![[assets/figures/papers/paper_list_l2394_https_arxiv_org_abs_2512_13043/figures/007_Figure_5.jpg]]
*Figure 5: Comparison of training curves in the ALFWorld environment. Without relying on any powerful external models, GTR-Turbo achieves comparable performance purely through its own exploration, experience, and thought guidance*

#### 训练效率与成本分析

Table 4 给出了不同方法的计算时间和成本对比。GTR-Turbo的KL变体将总训练时间降至与RL4VLM相当的水平，约为GTR的一半；SFT变体虽然仍需要教师模型的自回归生成，但已通过本地推理替代外部API调用，显著降低了额外开销。总体而言，GTR-Turbo在Points24上实现了 **54%** 的成功率，而额外成本仅为约100美元（主要为额外GPU部署开销），相比GTR的150美元API成本，实际可降低约60%的计算开支。

![[assets/figures/papers/paper_list_l2394_https_arxiv_org_abs_2512_13043/figures/009_Table_4.jpg]]
*Table 4: Computation Time and Cost Comparison. GTR-Turbo has comparable or even superior performance to GTR with significantly shorter training time and lower monetary cost. Reported costs account only for additional overhead (excluding the base cost of agent training) and may fluctuate with market conditions. P24 - Points24, ALF - ALFWorld, SR - task success rate, * - Estimation based on the deployment cost of an additional GPU*

**Table 4** 清晰对比了各方法在Points24和ALFWorld上的训练时间、成本与成功率。

#### Android-in-the-Wild：GUI任务扩展

在Android-in-the-Wild GUI操作任务上，GTR-Turbo取得了 **80.2%** 的成功率，较PPO基线的75.0%提升 **+5.2%**（Table 6），验证了该方法在视觉决策任务中的泛化能力。

### 消融实验与关键设计选择

#### 模型合并的必要性

Figure 6 对比了GTR-Turbo与使用静态初始模型作为KL参考的自改进基线。结果表明，静态模型KL正则化无法实现稳定提升，而动态合并历史检查点则是性能增长的关键驱动力。这证实了**合并模型隐式聚合了过去经验和知识**这一核心洞察。

![[assets/figures/papers/paper_list_l2394_https_arxiv_org_abs_2512_13043/figures/010_Figure_6.jpg]]
*Figure 6: Comparison with other selfimprovement baselines. The advantage over static-model KL regularization shows the necessity of model merging. The comparison with Rejection Sampling highlights the critical role of RL exploration*

#### TIES合并 vs 线性平均

Figure 8 展示了TIES合并与简单线性平均的效果差异。TIES通过修剪、符号选举和选择性平均，有效避免了参数干扰，提升了教师模型质量，进而改善了整体训练收益。线性平均虽然简单，但在处理不同检查点间的参数冲突时表现较差。

![[assets/figures/papers/paper_list_l2394_https_arxiv_org_abs_2512_13043/figures/012_Figure_8.jpg]]
*Figure 8: Performance comparison with and without TIES merging. The results demonstrate the robustness of TIES in the merging process, effectively enhancing the quality of the teacher model and improving the overall training gains*

#### 指导范围：仅思维 vs 思维+动作

Figure 7 对比了两种指导范围。仅对思维部分施加指导的效果优于同时指导思维和动作，原因在于后者限制了模型的探索自由度——而探索正是GTR-Turbo自演化的关键过程。

![[assets/figures/papers/paper_list_l2394_https_arxiv_org_abs_2512_13043/figures/011_Figure_7.jpg]]
*Figure 7: Comparing different ranges of guidance. Guiding full responses, including both the thoughts and actions simultaneously, is less effective, primarily because it limits the model’s exploration, a process that is crucial for self-evolution in GTR-Turbo*

#### KL估计方法选择

Figure 9 比较了多种KL估计方法。所有输出非负值的方法均能提升性能，其中**裁剪方法（clipping）**效果最优，因为它能控制KL值的幅度，实现更细粒度的更新和更好的稳定性。前向KL的表现略逊于逆向KL，证实了逆向KL的模式搜索（mode-seeking）优势。

![[assets/figures/papers/paper_list_l2394_https_arxiv_org_abs_2512_13043/figures/013_Figure_9.jpg]]
*Figure 9: Comparison among different KL estimation methods. All methods with non-negative output can achieve increased performance. The clipping method yields the best results, as it controls the magnitude of the KL value, leading to finer-grained updates and improved stability. The slightly lower result of forward KL proves the mode-seeking advantage of reverse KL*

#### 权重分配策略

Figure 10 展示了不同权重分配方法的效果。简单的SMA（算术平均）已能产生强劲性能，而EMA在平衡参数 **α=0.5** 时效果最佳。α的平衡选择对于发挥EMA的优势至关重要。

![[assets/figures/papers/paper_list_l2394_https_arxiv_org_abs_2512_13043/figures/014_Figure_10.jpg]]
*Figure 10: Comparing different weights assignment methods. Simple SMA already yields strong performance. A balanced choice of α is critical for realizing the benefit of EMA*

#### 合并频率的鲁棒性

Figure 13 表明，GTR-Turbo在合并间隔为10步以内时性能具有鲁棒性，说明该方法对合并频率的超参数不敏感。

#### 思维崩溃的缓解

Figure 14 的推理分数评测显示，GTR-Turbo在训练过程中能够维持较高的推理质量，而使用静态教师的基线则出现明显的思维退化。这进一步验证了动态合并教师模型在提供过程监督、防止思维崩溃方面的关键作用。

### 局限性与待验证问题

尽管GTR-Turbo在多个基准上展现了显著优势，仍存在以下局限：需要额外GPU部署合并教师模型，存在硬件依赖；合并频率和EMA平滑系数等超参数需手动调整，暂无自适应机制；所有实验基于7B/8B规模VLM，在更大模型上的扩展性未知；在更复杂的真实世界视觉决策环境中的泛化能力有待验证。

## 方法谱系与知识库定位

### 1. 与基线工作的关系

GTR-Turbo 的核心动机源于对 **GTR**（Guided Thought Reinforcement）框架的继承与重构。原始 GTR 提出了一种“VLM-作为-校正器”的机制：在 PPO 强化学习训练的每一步，调用外部多模态 API 模型（如 GPT-4o 或 Gemini）对智能体生成的思维内容进行评价和精炼，通过联合优化动作的 PPO 损失和思维的 SFT 损失来解决“思维崩溃”问题。这一设计虽然有效，但引入了严重的可扩展性瓶颈——外部 API 调用带来高昂的金钱成本（约 150 美元/15,000 步）、漫长的训练时间（约 4 天）和对外部服务的可用性依赖。

GTR-Turbo 的切入点是**替换教师模型的来源**：将外部 API 教师替换为 RL 训练过程中自身产生的历史检查点的合并模型。这一替换并非简单的工程优化，而是基于一个关键发现——合并检查点在损失面上更平滑，性能稳定地优于当前训练中的智能体（Figure 2），因此天然具备“教师”资格。由此，GTR-Turbo 将 GTR 的“外部知识注入”范式转变为“内部经验聚合与自我指导”范式。

与直接应用 PPO 的 **RL4VLM**（Zhai et al., NeurIPS 2025）相比，GTR-Turbo 保留了思维层面的过程监督，但教师信号完全来自本地合并模型，无需任何外部调用。与仅使用 SFT 初始化的 **Qwen2.5-VL-7B-sft** 相比，GTR-Turbo 通过 RL 探索和思维指导实现了显著的性能跃升。在 Points24 任务上，GTR-Turbo（KL 变体）的成功率达到 53.5%，超过 GTR 的 44.5%，同时训练时间减半、计算成本降低约 60%（Table 4）。在 ALFWorld 上，GTR-Turbo 以更低的成本达到与 GTR 相当的成功率（0.15 vs 0.16）。

### 2. 方法谱系中的定位

从技术路线的角度，GTR-Turbo 处于三条研究线的交汇处：

**（1）Agentic VLM 的强化学习训练。** 该线从 RL4VLM 的纯 PPO 训练出发，经 GTR 引入外部思维监督，再到 GTR-Turbo 实现自持的思维指导。GTR-Turbo 证明，在稀疏奖励环境中，思维层面的过程监督至关重要，而这种监督不必来自更强的外部模型，可以通过模型合并从自身训练轨迹中提取。

**（2）模型合并技术。** GTR-Turbo 直接采用 **TIES-Merging**（Yadav et al., NeurIPS 2023）作为检查点合并的核心算法，通过修剪（Trim）、符号选举（Elect Sign）和选择性平均（Merge）三步操作避免参数干扰。消融实验（Figure 8）表明，TIES 合并相比简单线性平均能有效提高教师模型质量，从而提升整体训练收益。

**（3）知识蒸馏与自改进。** GTR-Turbo 的 SFT 变体本质上是一种“在线策略蒸馏”——合并教师模型对当前观测生成思维输出，作为监督信号约束智能体。KL 变体则更进一步，将逆向 KL 散度作为奖励惩罚项融入 PPO 目标，仅需单次前向传播即可完成指导，进一步降低了计算开销。

### 3. 适用边界与限制

**（1）硬件依赖。** 尽管 GTR-Turbo 消除了外部 API 调用，但仍需额外 GPU 部署合并教师模型进行本地推理。Table 4 显示，即使使用本地部署，SFT 变体的额外成本约为 100 美元（估算），KL 变体则接近零额外成本。

**（2）超参数敏感性。** 合并频率（Figure 13 显示在间隔 10 步内具有鲁棒性）、EMA 权重分配的平滑系数 α（Figure 10 显示 α=0.5 时性能最优）、KL 估计的裁剪方式（Figure 9 显示裁剪方法效果最好）均需手动调整，暂无自适应机制。

**（3）任务泛化范围有限。** 当前验证集中在 Points24 卡牌游戏、ALFWorld 室内导航和部分 Android-in-the-Wild GUI 操作任务上。在更复杂的视觉决策环境（如连续控制的机器人操作）中的表现未知。

**（4）模型规模限制。** 所有实验基于 7B/8B 规模的 VLM（Qwen2.5-VL-7B、Qwen3-VL-8B），未在更大参数模型（如 32B-72B）上验证合并教师模型的质量和扩展性。

**（5）KL 变体的偏差风险。** KL 变体依赖于对负 KL 值的裁剪操作（式 K1 = log π_θ − log π_merged，KL_clip = clip(K1, 0, +∞)），裁剪方式对结果有直接影响，可能引入系统性偏差。

### 4. 开放问题

1. **规模扩展性。** GTR-Turbo 能否在 32B-72B 规模的 VLM 上保持优势？更大的模型是否会产生更高质量的合并教师，还是参数干扰问题会加剧？

2. **自适应超参数。** 是否存在基于训练动态（如奖励方差、KL 散度趋势）自适应调整合并频率和 EMA 权重的方法，以避免手动搜索？

3. **真实世界部署。** 在开放、动态的真实世界环境中，合并教师模型可能聚合了错误经验或安全风险行为，如何保证自持训练方法的稳定性和安全性？

4. **多智能体与多任务扩展。** 该框架是否可以扩展到多智能体系统（多个智能体共享合并教师）或需要密集奖励的多任务 RLVR 训练中？合并教师的“知识聚合”特性在多任务场景下可能具有天然优势，但尚待验证。

5. **合并策略的进一步优化。** 当前使用 TIES-Merging 对所有历史检查点等权或 EMA 加权合并。是否存在基于检查点质量（如验证集奖励）的选择性合并策略，能进一步提升教师质量？

## 原文 PDF

![[paperPDFs/CVPR_2026/GTR_Turbo_Merged_Checkpoint_is_Secretly_a_Free_Teacher_for_Agentic_VLM_Training.pdf]]
