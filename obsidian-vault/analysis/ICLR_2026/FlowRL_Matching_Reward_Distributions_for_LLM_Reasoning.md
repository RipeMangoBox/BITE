---
title: "FlowRL: Matching Reward Distributions for LLM Reasoning"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/FlowRL_Matching_Reward_Distributions_for_LLM_Reasoning.pdf
openreview_forum_id: lObnTKbm9U
aliases:
- FlowRL
tags:
- ICLR_2026
- topic/reinforcement_learning_planning_agents
- topic/reinforcement_learning_planning_agents/deep_rl
core_operator: "采用流平衡（GFlowNets的轨迹平衡）将奖励最大化转变为奖励分布匹配，并通过可学习的配分函数将标量奖励归一化为目标分布。"
primary_logic: "通过最小化策略与奖励加权分布之间的反向KL散度，并利用轨迹平衡目标作为可操作的代理，强制策略覆盖完整奖励分布，从而促进多样化和泛化推理。"
claims:
- "FlowRL通过分布匹配在32B模型上实现数学推理平均准确率48.39%，显著超过GRPO的38.34%，绝对提升10.05个百分点。"
- "FlowRL产生更丰富的推理多样性，GPT-4o-mini评测的多样性分数远高于GRPO、PPO等强化学习方法。"
- "移除重要性采样导致平均准确率从35.63降至26.71，证明该模块对分布校正的关键作用。"
- "移除可学习配分函数Z_φ使AIME 2024准确率从15.41降至9.79，替换为常数则降至7.50，验证了其必要性。"
---

# FlowRL: Matching Reward Distributions for LLM Reasoning

> [!tip] 核心洞察
> 通过最小化策略与奖励加权分布之间的反向KL散度，并利用轨迹平衡目标作为可操作的代理，强制策略覆盖完整奖励分布，从而促进多样化和泛化推理。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | FlowRL：通过流平衡实现LLM推理的奖励分布匹配 |
| 英文题名 | FlowRL: Matching Reward Distributions for LLM Reasoning |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=lObnTKbm9U); [GitHub](https://github.com/Xuekai-Zhu/FlowRL) |
| Topic | #topic/reinforcement_learning_planning_agents #topic/reinforcement_learning_planning_agents/deep_rl |
| Method | FlowRL |
| Dataset | Math Benchmarks Avg (Qwen2.5-32B), Math Benchmarks Avg (Qwen2.5-7B), LiveCodeBench |

> [!tip] 效果简介
> - Math Benchmarks Avg (Qwen2.5-32B) 上，Avg@16 为 48.39，对比 38.34 (GRPO)，变化 +10.05。
> - Math Benchmarks Avg (Qwen2.5-32B) 上，Avg@16 为 48.39，对比 43.25 (PPO)，变化 +5.14。
> - Math Benchmarks Avg (Qwen2.5-7B) 上，Avg@16 为 35.63，对比 32.48 (GRPO)，变化 +3.15。

## 概述

### 瓶颈与动机

当前主流的LLM推理强化学习方法——包括PPO（Schulman et al., 2017）、GRPO（Shao et al., 2024）以及REINFORCE++（Hu et al., 2025）——均以**奖励最大化**为核心目标。这类方法存在一个深层缺陷：策略倾向于过度优化主导奖励信号，迅速坍缩到单一高奖励模式，忽略其他同样有效的推理路径，导致生成多样性丧失和泛化能力下降（Figure 1）。

### 核心方法：从奖励最大化到分布匹配

FlowRL提出了一种范式转换：将优化目标从“最大化期望奖励”转变为“**匹配完整奖励分布**”。其技术路线包含三个关键设计：

1. **可学习配分函数** $Z_\phi(\mathbf{x})$：通过一个3层MLP将标量奖励归一化为有效的概率分布，使奖励分布匹配成为可能。
2. **反向KL散度最小化**：最小化策略 $\pi_\theta$ 与奖励加权目标分布之间的 $\mathcal{D}_{\mathrm{KL}}(\pi_\theta \| \frac{\exp(\beta r)}{Z_\phi})$，迫使策略覆盖奖励分布的所有模式。
3. **轨迹平衡代理目标**：将上述KL目标等价转化为GFlowNets的轨迹平衡损失（Equation 3），使其可操作化。在此基础上引入长度归一化（防止长序列梯度爆炸）和重要性采样（修正off-policy偏差），形成最终的FlowRL目标（Equation 6）。

### 方法谱系与知识库定位

FlowRL处于**GFlowNets × RL for LLMs**的交叉点。与GRPO等基于优势函数剪辑的奖励最大化方法不同，FlowRL将生成式流网络（GFlowNets）中的轨迹平衡（trajectory balance）思想迁移到LLM策略优化中，通过分布匹配从根本上缓解模式坍缩。其可学习配分函数 $Z_\phi$ 的设计借鉴了GFlowNets中的初始流概念（Figure 2），而重要性采样和长度归一化则针对变长思维链训练的实际需求进行了适配。

### 主要结果概览

在数学推理和代码推理两大领域，FlowRL一致且显著地超越了所有奖励最大化基线：

- **数学推理**（Qwen2.5-32B, Avg@16）：FlowRL达到48.39%，较GRPO（38.34%）绝对提升10.05个百分点，较PPO（43.25%）提升5.14个百分点（Table 1）。在7B规模上同样保持3.15个百分点的优势。
- **代码推理**：在LiveCodeBench（Avg@16）、CodeForces（Rating）和HumanEval+上分别领先GRPO 4.68、235.65和3.15个百分点（Table 2）。
- **多样性**：GPT-4o-mini评测和人工评估均表明，FlowRL生成的推理路径多样性远高于GRPO、PPO等方法（Figure 4, Table 8），且训练过程中奖励方差持续更高（Table 12），验证了分布匹配对模式坍缩的抑制作用。

### 消融关键发现

消融实验确认了各组件的必要性：移除重要性采样导致平均准确率从35.63骤降至26.71（Table 3）；移除可学习配分函数 $Z_\phi$ 使AIME 2024准确率从15.41降至9.79，替换为常数则进一步降至7.50（Table 11）；去除长度归一化则引发严重的训练不稳定——响应长度爆炸/崩溃、梯度范数剧烈波动（Figure 6）。超参数 $\beta=15$ 在六项数学基准上达到最优（Figure 3），配分函数采用3层MLP优于1层或5层架构（Table 10）。

### 局限与开放问题

FlowRL目前依赖结果奖励（outcome reward），未使用过程监督信号，可能无法捕捉推理步骤的局部正确性。可学习配分函数 $Z_\phi$ 引入了额外参数，略微增加训练开销。实验范围目前限于数学与代码推理，在对话、摘要等其他任务上的有效性有待验证。开放问题包括：如何将过程奖励融入分布匹配框架、$Z_\phi$ 在大规模模型上的扩展性、以及 $\beta$ 超参数的自适应调节策略。

## 背景与动机

### 推理能力增强的现状与瓶颈

大语言模型在数学推理、代码生成等复杂任务上的能力提升，高度依赖于强化学习（RL）驱动的后训练优化。当前主流方法——如近端策略优化**PPO**（Schulman et al., 2017）、组相对策略优化**GRPO**（Shao et al., 2024）以及**REINFORCE++**（Hu et al., 2025）——均遵循奖励最大化范式：通过估计优势函数并沿梯度方向更新策略，使模型生成高奖励响应的概率持续上升。

然而，这一范式存在一个被长期忽视的结构性缺陷：**模式坍缩**。当奖励信号呈现多模态分布时（例如，一道数学题存在多种等价但路径迥异的解法，或代码生成任务中不同算法均能通过测试），奖励最大化方法倾向于将概率质量集中到少数甚至单一的高奖励峰值上。Figure 1 直观展示了这一现象：GRPO、PPO 和 REINFORCE++ 在奖励分布上坍缩至单个主峰（KL 散度高达 8.68），而 FlowRL 通过分布匹配保持了多模态覆盖（KL 散度仅 0.11）。这种坍缩不仅抑制了推理路径的多样性，还削弱了模型在分布外问题上的泛化能力——当训练期间过度优化的单一推理模式在测试时失效，模型缺乏备选策略。

### 现有方法的工程困境

奖励最大化框架在实践中还面临两个工程挑战。其一，**长度偏差**：GRPO 虽对所有 token 损失取平均，但未对 log-概率进行序列长度的显式缩放，导致长推理链的梯度贡献失衡，训练不稳定。其二，**采样分布偏移**：GRPO 采用带裁剪的重要性权重修正 off-policy 采样，但该修正仅作用于优势项，未覆盖整个优化目标，当策略更新幅度较大时仍会产生显著的分布失配。

### 从奖励最大化到分布匹配的动机

FlowRL 的核心动机源于一个根本性的视角转换：**不再追求最大化期望奖励，而是让策略学会生成与奖励分布成比例的完整推理路径集合**。这一思想直接借鉴了生成流网络（GFlowNets; Bengio et al., 2023）的轨迹平衡原理——在流网络中，初始流量 $Z_\phi(s_0)$ 注入系统后，经策略 $\pi_\theta$ 在中间状态间传输，最终在终止状态按标量奖励的比例累积（Figure 2）。将这一原理迁移至 LLM 推理场景，意味着策略的目标变为：

$$\min_{\theta} \mathcal{D}_{\mathrm{KL}}\left(\pi_{\theta}(\mathbf{y} \mid \mathbf{x}) \,\|\, \frac{\exp(\beta r(\mathbf{x}, \mathbf{y}))}{Z_{\phi}(\mathbf{x})}\right)$$

即最小化策略与奖励加权分布之间的反向 KL 散度。该目标的梯度天然包含奖励最大化项和熵正则化项，理论上同时促进高奖励生成与多样性保持。为实现这一目标，FlowRL 引入可学习配分函数 $Z_\phi$ 将标量奖励归一化为概率分布，并以轨迹平衡损失作为可操作的优化代理，从而在数学与代码推理任务上实现准确率与多样性的双重提升。

## 核心创新

FlowRL的核心创新在于**从根本上改变了强化学习微调LLM推理的优化范式**：从传统的“奖励最大化”转向“奖励分布匹配”。这一转变直指现有方法（PPO、GRPO、REINFORCE++）的根本瓶颈——这些方法倾向于过度优化主导奖励信号，使策略坍缩到少数高奖励模式，导致生成推理的多样性丧失（模式坍缩）。

为实现这一范式转换，FlowRL引入了三个紧密耦合的技术槽位，构成完整的分布匹配优化框架：

### 1. 优化目标：从优势剪辑到轨迹平衡

**基线做法**：GRPO等奖励最大化方法采用基于优势剪辑的策略梯度目标（公式1），本质上是最大化期望奖励，天然倾向于将概率质量集中在少数高奖励轨迹上。

**FlowRL做法**：将优化目标重新定义为最小化策略 $\pi_\theta$ 与奖励加权目标分布之间的**反向KL散度**：

$$\min_{\theta} \mathcal{D}_{\mathrm{KL}}\left(\pi_{\theta}(\mathbf{y} \mid \mathbf{x}) \| \frac{\exp(\beta r(\mathbf{x}, \mathbf{y}))}{Z_{\phi}(\mathbf{x})}\right)$$

这一目标强制策略覆盖完整的奖励分布，而非仅追逐峰值。关键在于，该KL最小化目标可通过GFlowNets的**轨迹平衡损失**转化为可操作的代理：

$$\left( \log Z_{\phi}(\mathbf{x}) + \log \pi_{\theta}(\mathbf{y} \mid \mathbf{x}) - \beta r(\mathbf{x}, \mathbf{y}) \right)^2$$

该平方损失惩罚前向流（$\log\pi_\theta$）与奖励归一化流（$\beta r - \log Z_\phi$）之间的不匹配，从而在数学上保证策略收敛至目标分布。

### 2. 配分函数：从无归一化到可学习分布校准

**基线做法**：GRPO仅使用组内奖励的均值和标准差进行Z-score归一化（$\hat{r}_i = \frac{r_i - \mathrm{mean}(\mathbf{r})}{\mathrm{std}(\mathbf{r})}$），缺乏全局分布建模能力。

**FlowRL做法**：引入**可学习配分函数** $Z_\phi(\mathbf{x})$，将标量奖励转化为归一化概率分布。该模块以语言模型最后一层隐藏状态的平均值作为输入，通过3层MLP实现。其作用是将不同问题下的奖励映射到统一尺度，使分布匹配目标具有跨问题的可比性。

消融实验验证了该设计的必要性：移除可学习 $Z_\phi$ 使AIME 2024准确率从15.41骤降至9.79，替换为常数则进一步降至7.50（Table 11）；3层MLP架构在深度消融中表现最优（Table 10）。

### 3. 重要性采样与长度归一化：面向变长推理的工程适配

FlowRL针对LLM推理的两个实际挑战进行了关键适配：

- **长度归一化**：在轨迹平衡损失中显式除以序列长度 $|\mathbf{y}|$，将 $\log\pi_\theta$ 缩放为 $\frac{1}{|\mathbf{y}|}\log\pi_\theta$，防止长序列梯度爆炸。消融显示，去除长度归一化导致训练严重不稳定——响应长度出现爆炸或崩溃，梯度范数剧烈波动（Figure 6）。

- **重要性采样**：引入带梯度分离和裁剪的重要性权重 $w = \mathrm{clip}\left( \frac{\pi_{\theta}(\mathbf{y} \mid \mathbf{x})}{\pi_{\mathrm{old}}(\mathbf{y} \mid \mathbf{x})}, 1 - \epsilon, 1 + \epsilon \right)^{\mathrm{detach}}$，应用于整个轨迹平衡损失，修正off-policy采样偏差。去除该模块使平均准确率从35.63大幅下降至26.71（Table 3），证明其对分布校正的关键作用。

最终FlowRL目标整合上述所有组件：

$$\mathcal{L}_{\mathrm{FlowRL}} = w \cdot \bigg( \log Z_{\phi}(\mathbf{x}) + \frac{1}{|\mathbf{y}|} \log \pi_{\theta}(\mathbf{y} \mid \mathbf{x}) - \beta \hat{r}(\mathbf{x}, \mathbf{y}) - \frac{1}{|\mathbf{y}|} \log \pi_{\mathrm{ref}}(\mathbf{y} \mid \mathbf{x}) \bigg)^2$$

其中参考模型 $\pi_{\mathrm{ref}}$ 作为先验融入奖励分布（$\exp(\beta r) \cdot \pi_{\mathrm{ref}}$），防止策略偏离预训练知识过远。

### 创新总结

| 技术槽位 | 基线（GRPO） | FlowRL | 因果作用 |
|---------|-------------|--------|---------|
| 优化目标 | 优势剪辑最大化期望奖励 | 反向KL散度最小化 / 轨迹平衡损失 | 强制覆盖完整奖励分布，消除模式坍缩 |
| 配分函数 | 组内Z-score归一化 | 可学习 $Z_\phi$（3层MLP） | 将奖励全局归一化为概率分布 |
| 长度归一化 | 无显式缩放 | $\frac{1}{\|\mathbf{y}\|}\log\pi_\theta$ | 防止长序列梯度爆炸 |
| 重要性采样 | 带裁剪的旧策略比率 | 带梯度分离和裁剪的全损失权重 | 修正off-policy分布偏差 |

这些创新的协同效果在实验中得到验证：FlowRL在32B模型上实现数学推理平均准确率48.39%，显著超过GRPO的38.34%（+10.05个百分点），并在多样性评测中远高于所有奖励最大化基线（Figure 4）。

## 整体框架

![[assets/figures/papers/paper_list_l14_https_openreview_net_forum_id_lObnTKbm9U/figures/001_Figure_1.jpg]]
*Figure 1: Top: Comparison between distribution-matching and reward-maximizing approaches. FlowRL (left) learns to match the full reward distribution, maintaining diversity across multiple modes with low KL divergence. In contrast, reward-maximizing methods (right) such as RE-INFORCE++ (R++; Sutton et al., 1999b; Hu et al., 2025), PPO (Schulman et al., 2017), and GRPO (Shao et al., 2024) concentrate on a single high-reward peak, leading to mode collapse and higher KL divergence. Bottom: Performance comparison. FlowRL consistently outperforms GRPO across math and code domains*

FlowRL 的核心思想是将 LLM 推理的强化学习从“奖励最大化”范式转变为“奖励分布匹配”范式。传统方法（如 PPO、GRPO）倾向于使策略坍缩到单一高奖励模式，忽略其他同样有效的推理路径，导致生成多样性下降。FlowRL 通过引入**流平衡（Flow Balancing）**机制，强制策略覆盖完整的奖励分布，从而在保持高准确率的同时显著提升推理路径的多样性。

### 核心模块与数据流

FlowRL 的整体架构由三个关键模块组成：

1. **策略模型 π_θ（Policy Model）**
   - 输入：推理问题 **x**
   - 输出：生成推理路径（Chain-of-Thought）**y**
   - 角色：根据 FlowRL 目标函数更新参数，学习匹配目标奖励分布

2. **可学习配分函数 Z_φ（Partition Function）**
   - 输入：语言模型最后一层隐藏状态的平均值（作为问题 **x** 的表示）
   - 输出：标量值 Z_φ(**x**)，用于将标量奖励归一化为概率分布
   - 实现：3 层 MLP，隐藏维度与基座模型匹配
   - 角色：将原始标量奖励 r(**x**, **y**) 转化为归一化目标分布 exp(β r(**x**, **y**)) / Z_φ(**x**)

3. **参考模型 π_ref（Reference Model）**
   - 固定的预训练模型，无参数更新
   - 角色：作为先验约束融入奖励分布，修正后的奖励函数为 exp(β r(**x**, **y**)) · π_ref(**y** | **x**)

### 训练流程

FlowRL 的训练过程遵循以下步骤：

**Step 1: 采样与奖励计算**
- 对每个输入问题 **x**，从当前策略 π_θ 采样一组候选推理路径 {**y**₁, **y**₂, ..., **y**\_G}
- 使用结果奖励函数（outcome reward）计算每条路径的标量奖励 r(**x**, **y**)
- 对组内奖励进行 Z-score 归一化：$\hat{r}_i = \frac{r_i - \mathrm{mean}(\mathbf{r})}{\mathrm{std}(\mathbf{r})}$

**Step 2: 配分函数估计**
- 将问题表示输入 Z_φ，输出归一化常数 Z_φ(**x**)

**Step 3: 损失计算**
- 计算轨迹平衡损失（Trajectory Balance Loss），该损失等价于最小化策略与目标分布之间的反向 KL 散度：
  $$\mathcal{L}_{\mathrm{FlowRL}} = w \cdot \bigg( \log Z_{\phi}(\mathbf{x}) + \frac{1}{|\mathbf{y}|} \log \pi_{\theta}(\mathbf{y} \mid \mathbf{x}) - \beta \hat{r}(\mathbf{x}, \mathbf{y}) - \frac{1}{|\mathbf{y}|} \log \pi_{\mathrm{ref}}(\mathbf{y} \mid \mathbf{x}) \bigg)^2$$
- 其中 w 为带裁剪和梯度分离的重要性权重：
  $$w = \mathrm{clip}\left( \frac{\pi_{\theta}(\mathbf{y} \mid \mathbf{x})}{\pi_{\mathrm{old}}(\mathbf{y} \mid \mathbf{x})}, 1 - \epsilon, 1 + \epsilon \right)^{\mathrm{detach}}$$

**Step 4: 参数更新**
- 同时更新策略模型 π_θ 和配分函数 Z_φ 的参数
- 重要性权重 w 中的梯度分离（detach）确保该权重仅用于缩放损失，不向旧策略传递梯度

### 关键设计要点

| 设计要素 | 作用 | 消融验证 |
|---------|------|---------|
| 轨迹平衡目标 | 将 KL 散度最小化转化为可操作的平方损失代理 | 核心理论等价性（Remark 2） |
| 可学习配分函数 Z_φ | 动态归一化奖励，避免手工设定配分常数 | 移除后 AIME 2024 准确率从 15.41 降至 9.79（Table 11） |
| 长度归一化 1/\|y\|
| 防止长序列梯度爆炸，稳定训练 | 去除后训练严重不稳定，响应长度崩溃/爆炸（Figure 6） |
| 重要性采样 w | 修正 off-policy 采样偏差 | 去除后平均准确率从 35.63 降至 26.71（Table 3） |
| 参考模型先验 | 防止策略偏离预训练知识过远 | 融入奖励函数（Equation 4） |

### 与传统方法的本质区别

传统奖励最大化方法（如 GRPO）直接优化期望奖励：
$$\mathcal{I}_{GRPO}(\boldsymbol{\theta}) = \mathbb{E} \frac{1}{G}\sum_{i=1}^{G} \frac{1}{|\mathbf{y}_i|} \sum_{t} \{ \min[ \frac{\pi_{\theta}}{\pi_{\theta,d}} \hat{A}_{i,t}, \mathrm{clip}(...) \hat{A}_{i,t} ] - \lambda \mathbb{D}_{KL}[\pi_{\theta}||\pi_{ref}] \}$$

该目标倾向于将所有概率质量集中在奖励最高的单一模式上，导致模式坍缩（Figure 1 顶部右侧，KL 散度高达 8.68）。

FlowRL 则将目标重新定义为分布匹配：
$$\min_{\theta} \mathcal{D}_{\mathrm{KL}}(\pi_{\theta}(\mathbf{y} \mid \mathbf{x}) \| \frac{\exp(\beta r(\mathbf{x}, \mathbf{y}))}{Z_{\phi}(\mathbf{x})})$$

通过最小化反向 KL 散度，策略被迫覆盖奖励分布的所有模式，而非仅追求最高峰。Figure 1 的示意对比清晰展示了这一差异：FlowRL 的 KL 散度仅为 0.11，而奖励最大化方法达到 8.68。

## 核心模块与公式推导

### 问题瓶颈与优化目标转换

现有LLM推理的强化学习方法（PPO、GRPO等）以最大化期望奖励为目标，其优化过程倾向于将概率质量集中到少数高奖励推理路径上，导致**模式坍缩**——模型反复生成相似的解题模式，丧失推理多样性。GRPO的典型目标为：

$$
\mathcal{I}_{GRPO}(\boldsymbol{\theta}) = \mathbb{E}_{|x \sim P(X), \{\mathbf{y}_*\}_{*=1}^{G} \sim \pi_{\theta,d}(\boldsymbol{\mathcal{V}}|\mathbf{x})} \frac{1}{G}\sum_{i=1}^{G} \frac{1}{|\mathbf{y}_i|} \sum_{t=1}^{J_{*1}} \{ \min[ \frac{\pi_{\theta}(\mathbf{y}_{i,t}|\mathbf{x},\mathbf{y}_{i,\le t})}{\pi_{\theta,d}(\mathbf{y}_{i,t}|\mathbf{x},\mathbf{y}_{i,\le t})} \hat{A}_{i,t}, \mathrm{clip}(...) \hat{A}_{i,t} ] - \lambda \mathbb{D}_{KL}[\pi_{\theta}||\pi_{ref}] \}
$$

该目标通过组内优势归一化 $\hat{A}_i = \frac{r_i - \mathrm{mean}(\mathbf{r})}{\mathrm{std}(\mathbf{r})}$ 和裁剪重要性采样来更新策略，但其本质仍是向单一高奖励模式收紧。

FlowRL将优化范式从**奖励最大化**转向**奖励分布匹配**：通过最小化策略 $\pi_\theta$ 与奖励加权目标分布之间的反向KL散度，强制策略覆盖完整奖励分布：

$$
\min_{\theta} \mathcal{D}_{\mathrm{KL}}(\pi_{\theta}(\mathbf{y} \mid \mathbf{x}) \| \frac{\exp(\beta r(\mathbf{x}, \mathbf{y}))}{Z_{\phi}(\mathbf{x})})
$$

其中 $\beta$ 为温度超参数（实验确定最优值为15），$Z_\phi(\mathbf{x})$ 为可学习配分函数。

---

### 核心模块一：可学习配分函数 $Z_\phi$

传统GRPO仅使用组内奖励均值和标准差进行归一化，缺乏将标量奖励转化为有效概率分布的机制。FlowRL引入**可学习配分函数** $Z_\phi(\mathbf{x})$，将标量奖励归一化为目标分布：

- **输入**：语言模型最后一层隐藏状态的平均值
- **架构**：随机初始化的3层MLP，隐藏维度与基础模型匹配
- **作用**：学习问题相关的归一化常数，使 $\frac{\exp(\beta r(\mathbf{x}, \mathbf{y}))}{Z_\phi(\mathbf{x})}$ 构成合法概率分布

消融实验验证了该模块的必要性：移除可学习 $Z_\phi$ 后，AIME 2024准确率从15.41降至9.79；替换为常数则进一步降至7.50（Table 11）。3层MLP架构在AIME 2024/2025上均优于1层和5层变体（Table 10）。

---

### 核心模块二：轨迹平衡损失

直接优化反向KL散度在实践中不可行。FlowRL利用GFlowNets中的**轨迹平衡**（Trajectory Balance）公式作为可操作的代理目标。该等价性基于：当 $Z_\phi$ 为真实配分函数时，KL最小化等价于最小化轨迹平衡残差：

$$
\left( \log Z_{\phi}(\mathbf{x}) + \log \pi_{\theta}(\mathbf{y} \mid \mathbf{x}) - \beta r(\mathbf{x}, \mathbf{y}) \right)^2
$$

该损失强制 $\log \pi_\theta(\mathbf{y}|\mathbf{x}) \approx \beta r(\mathbf{x}, \mathbf{y}) - \log Z_\phi(\mathbf{x})$，使策略的对数概率与奖励成比例，从而覆盖完整奖励分布而非仅聚焦最高奖励点。

---

### 核心模块三：参考模型先验与长度归一化

为防止策略偏离预训练知识过远，FlowRL将参考模型 $\pi_{\mathrm{ref}}$ 作为先验融入奖励函数：

$$
\exp(\beta r(\mathbf{x}, \mathbf{y})) \cdot \pi_{\mathrm{ref}}(\mathbf{y} \mid \mathbf{x})
$$

对应的损失项中加入 $-\frac{1}{|\mathbf{y}|} \log \pi_{\mathrm{ref}}(\mathbf{y} \mid \mathbf{x})$。

针对可变长度推理链的训练挑战，FlowRL对对数概率项进行**显式长度归一化**，将 $\log \pi_\theta(\mathbf{y}|\mathbf{x})$ 缩放为 $\frac{1}{|\mathbf{y}|}\log \pi_\theta(\mathbf{y}|\mathbf{x})$。消融实验表明，移除长度归一化会导致训练严重不稳定：响应长度出现爆炸或崩溃，梯度范数剧烈波动（Figure 6）。

---

### 核心模块四：重要性采样修正

由于FlowRL使用off-policy采样（以旧策略 $\pi_{\mathrm{old}}$ 生成样本），直接优化会产生分布偏差。FlowRL引入带梯度分离和裁剪的**重要性权重**：

$$
w = \mathrm{clip}\left( \frac{\pi_{\theta}(\mathbf{y} \mid \mathbf{x})}{\pi_{\mathrm{old}}(\mathbf{y} \mid \mathbf{x})}, 1 - \epsilon, 1 + \epsilon \right)^{\mathrm{detach}}
$$

该权重乘以整个轨迹平衡损失，其中 $\mathrm{detach}$ 操作阻止梯度通过重要性比率回传，避免策略漂移。消融实验证实其关键作用：移除重要性采样后，六项数学基准平均准确率从35.63骤降至26.71（Table 3）。

---

### 完整FlowRL目标

结合上述所有模块，最终优化目标为：

$$
\mathcal{L}_{\mathrm{FlowRL}} = w \cdot \bigg( \log Z_{\phi}(\mathbf{x}) + \frac{1}{|\mathbf{y}|} \log \pi_{\theta}(\mathbf{y} \mid \mathbf{x}) - \beta \hat{r}(\mathbf{x}, \mathbf{y}) - \frac{1}{|\mathbf{y}|} \log \pi_{\mathrm{ref}}(\mathbf{y} \mid \mathbf{x}) \bigg)^2
$$

其中 $\hat{r}_i = \frac{r_i - \mathrm{mean}(\mathbf{r})}{\mathrm{std}(\mathbf{r})}$ 为组内奖励归一化。该目标通过轨迹平衡损失实现分布匹配，通过重要性采样修正off-policy偏差，通过长度归一化稳定可变长度训练，通过参考模型先验约束策略空间。

## 实验与分析

### 核心实验设置

FlowRL 包含两个可学习模块：策略模型 $\pi_\theta$ 和配分函数 $Z_\phi$。配分函数采用随机初始化的 3 层 MLP，隐藏维度与基座模型对齐，输入为语言模型最后一层隐藏状态的平均值。奖励超参数 $\beta$ 设为 15，重要性采样裁剪范围 $\epsilon$ 与 PPO 一致。所有强化学习方法（FlowRL、GRPO、PPO、REINFORCE++）均采用相同的学习率、批量大小、训练步数及 veRL 框架配置，在完全一致的评估设置下对比。

### 数学推理主结果

Table 1 展示了 Qwen2.5-7B 和 Qwen2.5-32B 两个模型规模上六项数学推理基准的 Avg@16 准确率：

![[assets/figures/papers/paper_list_l14_https_openreview_net_forum_id_lObnTKbm9U/figures/003_Table_1.jpg]]
*Table 1: Results on math reasoning benchmarks. We report Avg@16 accuracy with relative improvements shown as subscripts. Positive gains are shown in green and negative changes in red. FlowRL outperforms all baselines across both 7B and 32B model scales*

- **32B 规模**：FlowRL 平均准确率 **48.39%**，较 GRPO（38.34%）绝对提升 **+10.05 个百分点**，较 PPO（43.25%）提升 **+5.14 个百分点**。在所有六个子基准上 FlowRL 均取得最优或并列最优。
- **7B 规模**：FlowRL 平均准确率 **35.63%**，较 GRPO（32.48%）提升 **+3.15 个百分点**，较 PPO（31.98%）提升 **+3.65 个百分点**。

该结果验证了分布匹配范式相比奖励最大化范式的一致优势，且优势随模型规模扩大而增强。

### 代码推理主结果

Table 2 报告了三个代码基准上的表现：

![[assets/figures/papers/paper_list_l14_https_openreview_net_forum_id_lObnTKbm9U/figures/004_Table_2.jpg]]
*Table 2: Results on code benchmarks. We report metrics with relative improvements shown as subscripts. Positive gains are shown in green and negative changes in red. FlowRL achieves the strongest performance across all three benchmarks. Table 3: Ablation study on FlowRL with Qwen2.5-7B as the base model. Avg@16 accuracy is reported across six math reasoning benchmarks. IS denotes importance sampling*

- **LiveCodeBench**（Avg@16）：FlowRL **37.43%**，GRPO 32.75%（+4.68）。
- **CodeForces**（Rating）：FlowRL **1549.47**，GRPO 1313.82（+235.65）。
- **HumanEval+**（Avg@16）：FlowRL **83.28%**，GRPO 80.13%（+3.15）。

FlowRL 在所有三个代码基准上均取得最强表现，表明分布匹配策略不仅适用于数学推理，对代码生成同样有效。

### 消融研究

#### 重要性采样（IS）

Table 3 显示，移除重要性采样后，六项数学基准平均准确率从 **35.63% 骤降至 26.71%**，降幅达 8.92 个百分点。该模块对纠正 off-policy 采样偏差、维持分布匹配的准确性至关重要。

![[assets/figures/papers/paper_list_l14_https_openreview_net_forum_id_lObnTKbm9U/figures/005_Table_3.jpg]]

#### 配分函数 $Z_\phi$

Table 11 的消融表明，完全移除可学习配分函数 $Z_\phi$ 后，AIME 2024 准确率从 **15.41% 降至 9.79%**；若替换为常数值，则进一步降至 **7.50%**。Table 10 进一步验证 3 层 MLP 架构（15.41%）优于 1 层（14.58%）和 5 层（13.75%），过深或过浅的网络均损害配分函数的学习能力。

![[assets/figures/papers/paper_list_l14_https_openreview_net_forum_id_lObnTKbm9U/figures/015_Table_11.jpg]]
*Table 11: Partition Function $Z _ { \phi }$*

#### 超参数 $\beta$

Figure 3 和 Table 7 展示了 $\beta \in \{5, 10, 15, 30\}$ 的影响：$\beta = 15$ 取得最优平均准确率 **35.63%**；$\beta = 5$ 时仅为 31.34%，奖励信号过弱；$\beta = 30$ 时略降至 35.09%，表明过高温度会放大噪声。

![[assets/figures/papers/paper_list_l14_https_openreview_net_forum_id_lObnTKbm9U/figures/010_Table_7.jpg]]
*Table 7: Ablation study on the effect of the $\beta$ parameter in FlowRL. We report Avg@16 accuracy across six math reasoning benchmarks for different values of β*

![[assets/figures/papers/paper_list_l14_https_openreview_net_forum_id_lObnTKbm9U/figures/011_Table_7.jpg]]

#### 长度归一化

Figure 6 揭示了移除长度归一化项 $1/|\mathbf{y}|$ 的严重后果：训练出现严重不稳定，响应长度剧烈爆炸或崩溃，梯度范数（对数尺度）出现尖峰。该组件对可变长度思维链训练的稳定性不可或缺。

### 多样性分析

Figure 4 展示了 GPT-4o-mini 评测的多样性分数：FlowRL 的生成多样性显著高于 REINFORCE++、GRPO 和 PPO。Table 4 的典型案例进一步佐证——在 AIME 问题上，GRPO 表现出重复模式（AM-GM 使用 3 次、恒等循环 2 次），而 FlowRL 遵循了包含对称性假设、有理根检验、因式分解的多样化求解路径。人类评估（Table 8）同样确认 FlowRL 的多样性优势。

![[assets/figures/papers/paper_list_l14_https_openreview_net_forum_id_lObnTKbm9U/figures/007_Figure_4.jpg]]
*Figure 4: GPT-judged diversity scores on rollouts of AIME 24/25 problems. FlowRL generates more diverse solutions than R++, GRPO, and PPO*

![[assets/figures/papers/paper_list_l14_https_openreview_net_forum_id_lObnTKbm9U/figures/008_Table_4.jpg]]
*Table 4: Case study comparing GRPO and FlowRL rollouts on an AIME problem. GRPO exhibits repetitive patterns (AM-GM ×3, identity loops ×2), while FlowRL follows a more diverse solution path*

![[assets/figures/papers/paper_list_l14_https_openreview_net_forum_id_lObnTKbm9U/figures/012_Table_8.jpg]]
*Table 8: Human-evaluated diversity scores ( $\mathrm { M e a n } \pm \mathrm { S t d }$ )

### 训练动态

Figure 5 展示了 Qwen2.5-7B 上的训练动态：FlowRL 的 AIME 2025 Acc@8 随训练步数稳步上升，响应长度保持稳定。Table 12 的奖励分布统计表明，FlowRL 维持了更健康的奖励分布，避免了奖励最大化方法常见的分布坍缩。

### 鲁棒性检验

在低温（0.6）和高温（1.0）设置下（Table 5、Table 6），FlowRL 均一致超越所有基线，表明其对生成随机性具有鲁棒性。跨域评估（Table 9）显示 FlowRL 在 MMLU（72.13%）和 GPQA（36.87%）上同样优于 GRPO 和 PPO，初步验证了方法的泛化能力。

![[assets/figures/papers/paper_list_l14_https_openreview_net_forum_id_lObnTKbm9U/figures/009_Table_5.jpg]]
*Table 5: Math reasoning performance (Avg@64) at temperature = 0.6. Relative improvements are shown as subscripts, with positive gains in green and negative changes in red. FlowRL consistently outperforms all baselines and achieves the best average score under this low-temperature setting. Table 6: Math reasoning performance (Avg@64) at temperature = 1.0. Relative improvements are shown as subscripts, with positive gains in green. FlowRL maintains robust performance under higher generation randomness and continues to outperform all baselines on average*

![[assets/figures/papers/paper_list_l14_https_openreview_net_forum_id_lObnTKbm9U/figures/013_Table_9.jpg]]
*Table 9: MMLU and GPQA benchmark performance*

### 局限与失败模式

1. **过程监督缺失**：FlowRL 仅依赖结果奖励，无法捕捉推理步骤的正确性，在需要细粒度反馈的任务上可能受限。
2. **配分函数开销**：$Z_\phi$ 引入额外参数，虽开销不大，但在极大规模模型上的扩展性尚未验证。
3. **任务覆盖有限**：当前实验仅涵盖数学与代码推理，对话、摘要等非推理领域的有效性需进一步验证。

## 方法谱系与知识库定位

### 从奖励最大化到分布匹配：范式转换

FlowRL的核心创新在于从根本上改变了LLM推理强化学习的优化哲学。传统的RL微调方法——包括**REINFORCE++**（Hu et al., 2025）、**PPO**（Schulman et al., 2017）和**GRPO**（Shao et al., 2024）——均以最大化期望奖励为目标。这些方法在训练过程中倾向于将策略概率质量集中在少数高奖励的推理模式上，造成**模式坍缩**（mode collapse），即模型放弃探索其他同样有效的推理路径，导致生成多样性显著下降。Figure 1直观展示了这一现象：奖励最大化方法将策略坍缩到单一高奖励峰值（KL散度高达8.68），而FlowRL通过分布匹配覆盖完整的奖励分布（KL散度仅0.11）。

FlowRL将优化目标从奖励最大化转变为**奖励分布匹配**。具体而言，它引入一个可学习的配分函数$Z_\phi(\mathbf{x})$将标量奖励归一化为合法的概率分布，然后最小化策略$\pi_\theta$与该奖励加权分布之间的**反向KL散度**。这一目标的数学形式为：

$$\min_{\theta} \mathcal{D}_{\mathrm{KL}}\left(\pi_{\theta}(\mathbf{y} \mid \mathbf{x}) \| \frac{\exp(\beta r(\mathbf{x}, \mathbf{y}))}{Z_{\phi}(\mathbf{x})}\right)$$

该KL最小化目标可被等价地转化为**轨迹平衡损失**（Trajectory Balance Loss），这是从GFlowNets（Bengio et al., 2023）的流平衡理论中继承的核心机制。轨迹平衡损失作为可操作的代理目标，强制策略覆盖完整的奖励分布，从而在保持高奖励的同时促进推理路径的多样性。

### 关键组件与基线差异

FlowRL在GRPO的基础上进行了四个关键槽位的替换，形成了独特的方法设计：

| 组件 | GRPO（基线） | FlowRL（本文） |
|------|-------------|---------------|
| **优化目标** | 基于优势剪辑的期望奖励最大化（公式1） | 最小化策略与奖励分布间的反向KL散度，等价于轨迹平衡损失（公式3、6） |
| **配分函数** | 无专用配分函数，仅使用组内奖励均值和标准差归一化 | 可学习配分函数$Z_\phi(\mathbf{x})$（3层MLP），将标量奖励转化为归一化概率分布 |
| **长度归一化** | 对所有token损失取平均，但未对log-概率进行序列长度显式缩放 | 在轨迹平衡损失中显式除以$|\mathbf{y}|$对$\log \pi_\theta$进行长度归一化 |
| **重要性采样** | 带裁剪的重要性权重，以旧策略概率为分母 | 引入带梯度分离（detach）和裁剪的重要性权重，应用于整个轨迹平衡损失 |

**配分函数$Z_\phi$**的作用尤为关键。消融实验（Table 11）表明，移除可学习的$Z_\phi$会使AIME 2024准确率从15.41骤降至9.79，替换为常数则进一步降至7.50。这表明动态学习归一化常数对于准确匹配奖励分布至关重要。架构消融（Table 10）进一步验证了3层MLP为最优选择，优于1层和5层设计。

**重要性采样**模块纠正了off-policy采样偏差。消融实验（Table 3）显示，移除重要性采样导致六项数学基准的平均准确率从35.63大幅下降至26.71，降幅高达8.92个百分点，充分证明了该模块对分布校正的关键作用。

**长度归一化**解决了可变长度思维链训练中的梯度不稳定问题。Figure 6的消融显示，去除长度归一化后训练严重不稳定：响应长度出现爆炸或崩溃，梯度范数剧烈波动。这一设计使得FlowRL能够有效处理从短答案到长推理链的多样化输出。

### 适用边界与局限

FlowRL目前存在以下适用边界和局限：

1. **奖励信号类型限制**：FlowRL依赖**结果奖励**（outcome reward），未使用过程监督信号。这意味着模型可能无法捕捉推理步骤的正确性，仅能根据最终答案的二元正确性进行优化。在需要细粒度过程反馈的任务中，这一限制可能影响性能。

2. **任务领域未充分验证**：现有实验仅涵盖数学推理（AIME、AMC、MATH-500、Minerva、Olympiad）和代码推理（LiveCodeBench、CodeForces、HumanEval+）任务。在对话生成、文本摘要、安全对齐等其他类型任务上的有效性尚未得到验证。Table 9提供了有限的跨域证据（MMLU和GPQA），但这两个基准仍属于知识和推理范畴。

3. **配分函数的额外开销**：可学习的$Z_\phi$引入了额外的模型参数（3层MLP），虽然参数量相对较小，但仍略微增加了训练开销。配分函数能否扩展到更大规模模型（如70B+）而保持训练稳定，目前尚未验证。

4. **超参数$\beta$需手动调节**：$\beta$控制奖励分布的温度，对性能有显著影响。消融实验（Figure 3、Table 7）显示，$\beta=15$在六项数学基准上达到最优平均准确率35.63，而$\beta=5$仅为31.34。目前缺乏自适应调整$\beta$的机制，需要针对不同任务手动调参。

### 开放问题

1. **过程奖励的融合**：如何将过程奖励或细粒度反馈自然地融入FlowRL的分布匹配框架？这可能需要扩展轨迹平衡损失以考虑中间状态的奖励信号，而非仅依赖终端状态的标量奖励。

2. **配分函数的扩展性**：$Z_\phi$的设计能否扩展到更大规模模型（如70B、405B参数）而保持训练稳定？随着模型规模增长，配分函数可能需要更复杂的架构或不同的初始化策略。

3. **非推理领域的多样性收益**：FlowRL在安全对齐、长文本生成等非推理领域是否同样能带来多样性收益？这些任务中奖励信号的定义和分布特性可能与数学/代码推理有本质差异。

4. **$\beta$的自适应策略**：能否设计$\beta$的自适应调整策略以进一步减少手动调参工作？例如，根据训练过程中的奖励分布统计量动态调整温度参数，或采用元学习的方法自动搜索最优$\beta$。

## 原文 PDF

![[paperPDFs/ICLR_2026/FlowRL_Matching_Reward_Distributions_for_LLM_Reasoning.pdf]]
