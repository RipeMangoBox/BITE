---
title: "Dynamics-Predictive Sampling for Active RL Finetuning of Large Reasoning Models"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/Dynamics_Predictive_Sampling_for_Active_RL_Finetuning_of_Large_Reasoning_Models.pdf
openreview_forum_id: voeheZjd8p
aliases:
- DPSD
- DPSARFLRM
tags:
- ICLR_2026
- topic/reinforcement_learning_planning_agents
- topic/reinforcement_learning_planning_agents/deep_rl
core_operator: "通过对每个提示的求解进度建立隐马尔可夫模型（HMM），并利用历史稀疏奖励信号进行在线贝叶斯推理，预测提示处于“部分求解”状态的概率，从而在不进行昂贵推演的情况下实现信息性样本的高效在线选择。"
primary_logic: "将提示的求解进度形式化为一个动力学系统，借助HMM从历史不完整观测中推断求解状态分布，即可将数据选择从推演密集型转变为轻量推理密集型，实现预测性采样。"
claims:
- "在MATH任务上，1.5B模型的DPS以73.7万次推演达到52.13的平均准确率，与oracle DS（293.3万次推演，52.00）相当，且远优于均匀采样US（48.57）。"
- "DPS在多个任务中能持续选取出高比例的部分求解提示（有效样本比约90%），且预测准确率和类2召回率保持较高水平。"
- "消融实验表明，移除非平稳衰减机制（λ=1）会导致Countdown 3B任务上的性能和预测准确率明显下降，验证了遗忘机制对适应动态的重要性。"
- "在响应组大小k=4的极限设置下，DPS的测试准确率超过均匀采样US的两倍以上，且仍保持高预测准确率，展现出在小样本响应下的鲁棒优势。"
---

# Dynamics-Predictive Sampling for Active RL Finetuning of Large Reasoning Models

> [!tip] 核心洞察
> 将提示的求解进度形式化为一个动力学系统，借助HMM从历史不完整观测中推断求解状态分布，即可将数据选择从推演密集型转变为轻量推理密集型，实现预测性采样。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 面向大型推理模型主动强化学习微调的动力学预测采样 |
| 英文题名 | Dynamics-Predictive Sampling for Active RL Finetuning of Large Reasoning Models |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=voeheZjd8p); [GitHub](https://github.com/maoyixiu/DPS) |
| Topic | #topic/reinforcement_learning_planning_agents #topic/reinforcement_learning_planning_agents/deep_rl |
| Method | Dynamics-Predictive Sampling (DPS) |
| Dataset | MATH (Average over AIME24, AMC23, MATH500, Minerva, Olympiad) — 1.5B model, Countdown CD-34 — 3B model, Geometry3k — 3B model, Rollout Efficiency (MATH 1.5B) |

> [!tip] 效果简介
> - MATH (Average over AIME24, AMC23, MATH500, Minerva, Olympiad) — 1.5B model 上，Pass@1 accuracy (%) 为 52.13，对比 US: 48.57; DS: 52.00，变化 DPS +3.56 over US, +0.13 over DS。
> - Countdown CD-34 — 3B model 上，Accuracy (%) 为 74.27，对比 US: 69.87; DS: 74.95，变化 DPS +4.40 over US, -0.68 vs DS。
> - Geometry3k — 3B model 上，Pass@1 accuracy (%) 为 44.47，对比 US: 40.22; DS: 45.54，变化 DPS +4.25 over US, -1.07 vs DS。

## 概述

大型语言模型在强化学习微调中存在一个关键瓶颈：训练过程中大量提示由于模型已完全掌握或完全未掌握，无法提供有效的梯度信号，导致训练效率低下。现有的在线提示选择方法——如动态采样（DS, Yu et al., 2025）——虽能通过筛选奖励方差大于零的提示来缓解此问题，但需要在大规模候选批次上进行昂贵的模型推演，其额外计算开销经常超过微调本身。

本文提出**动力学预测采样**（Dynamics-Predictive Sampling, DPS），将每个提示的求解进度形式化为一个动力学系统，借助隐马尔可夫模型（HMM）从历史稀疏奖励信号中进行在线贝叶斯推理，预测提示处于“部分求解”状态的概率，从而在不进行昂贵推演的情况下实现信息性样本的高效在线选择。其核心洞察在于：将数据选择从推演密集型转变为轻量推理密集型。

实验表明，DPS在多个推理任务上以极低的额外计算代价取得了与oracle动态采样相当甚至更优的性能。在MATH基准上，1.5B模型的DPS仅用73.7万次推演即达到52.13的平均准确率，与oracle DS（293.3万次推演，52.00）相当，且远优于均匀采样US（48.57）。在Countdown和Geometry3k任务上，DPS同样显著超越US，逼近DS的性能上限。消融实验验证了非平稳衰减机制、三状态划分等设计选择的关键作用，而DPS的推理与选择开销（全数据集更新仅需2.4秒/步，内存占用0.9 GiB）使其在实际部署中具有显著优势。

## 背景与动机

### 大规模推理模型的强化学习微调瓶颈

近年来，通过强化学习（RL）对大语言模型进行后训练已成为提升复杂推理能力的关键范式。给定一个提示数据集 $\mathcal{D}$，RL 微调的目标是最大化策略模型 $\pi_\theta$ 在提示上的期望奖励：

$$\operatorname*{max}_{\theta \in \Theta} \mathbb{E}_{\tau \sim \mathcal{D}, y \sim \pi_{\theta}(\cdot|\tau)} [r(\tau, y)]$$

其中 $r(\tau, y)$ 通常为基于规则验证的二元结果奖励（正确/错误）。在这一框架下，训练数据的质量直接决定了梯度信号的有效性。然而，一个关键瓶颈长期被忽视：**大量训练提示无法提供有效的梯度信号**。具体而言，当模型对某个提示已经能够稳定生成完全正确的解答（“完全解决”）或始终无法给出任何正确解答（“完全未解决”）时，该提示对应的奖励方差趋近于零，导致策略梯度几乎为零，从而浪费了大量计算资源。这使得训练效率严重受限于“部分解决”提示的稀缺性——只有那些模型时而能解、时而不能解的提示才能产生有意义的学习信号。

### 现有在线提示选择方法的局限

为缓解上述问题，动态采样（Dynamic Sampling, DS; Yu et al., 2025）提出了一种在线提示选择策略：在每步训练中，先从一个扩大的候选批次 $\hat{\mathcal{B}}_t$ 中为每个提示采样 $k$ 条响应，然后仅保留奖励标准差大于零的提示构成实际训练批次：

$$\mathcal{B}_t = \left\{ \tau \in \hat{\mathcal{B}}_t \mid \mathrm{std}(\{r(\tau, y_i^{\tau})\}_{i=1}^k) > 0 \right\}$$

这一过滤规则本质上是在筛选处于“部分解决”状态的提示。DS 虽然有效，但其代价极为高昂：为筛选出 $|\mathcal{B}_t|$ 个有效提示，通常需要从 $3\times|\mathcal{B}_t|$ 甚至更大规模的候选批次中进行完整的 LLM 推演。在 7B 模型上，DS 的额外推演开销可达每步约 1500 秒，经常超过微调本身的计算成本。历史重采样（History Resampling, HR; Zhang et al., 2025）则采用更轻量的启发式规则，仅在当前 epoch 内排除已产生全对响应的提示，虽无额外推演开销，但其静态过滤策略无法适应模型能力的动态变化，性能提升有限。

### 核心洞见：从推演密集型到推理密集型

上述方法的共同困境在于：**要判断一个提示是否处于“部分解决”状态，就必须先在该提示上执行昂贵的模型推演**。本文的核心洞见是：将每个提示的求解进度形式化为一个**动力学系统**，利用历史不完整的稀疏奖励观测进行在线贝叶斯推理，即可在不进行任何额外推演的情况下预测提示的求解状态，从而实现**预测性采样**。

具体而言，本文将提示的求解程度建模为三类状态——完全未解（State 1）、部分解决（State 2）、完全解决（State 3）——并假设状态转移服从隐马尔可夫模型（HMM）。通过在每个训练步利用本轮观测到的二元奖励信号更新状态后验信念，并采用带指数衰减的 Dirichlet 更新机制适应非平稳的求解动态，DPS 能够以极小的计算代价（全数据集 $|\mathcal{D}|=10^7$ 时仅需 2.4 秒、0.9 GiB 内存）预测每个提示处于 State 2 的概率，进而通过 Top-B 贪婪选择直接构建高信息量的训练批次。这一设计将数据选择从“推演密集型”转变为“轻量推理密集型”，为大规模 RL 微调的高效数据采样开辟了新路径。

## 核心创新

DPS 的核心创新在于将提示采样从**推演密集型**转变为**推理密集型**。传统的在线提示选择方法（如 DS）需要在大规模候选批次上进行昂贵的模型推演，其额外计算开销经常超过微调本身。DPS 通过以下关键机制突破这一瓶颈：

### 求解进度的动力学建模

DPS 将每个提示的求解进度形式化为一个**隐马尔可夫模型（HMM）**，定义三个隐状态：完全未解（State 1）、部分解决（State 2）、完全解决（State 3）。其中 State 2 的提示因能提供有效梯度信号而被视为最具信息性。该建模将提示选择转化为一个**状态预测问题**，而非推演验证问题。

### 轻量在线贝叶斯推理

DPS 在每个训练步执行三阶段推理流水线：
- **观测更新**：当提示被选中时，利用退化发射模型（观测即状态）通过贝叶斯规则将先验信念更新为后验；
- **转移更新**：采用带指数衰减的 Dirichlet 后验更新转移矩阵，以适应训练过程中求解动态的非平稳演化；
- **状态预测**：利用推断的转移矩阵和当前后验，预测下一步的求解状态先验分布。

### 预测性贪婪采样

基于预测的 State 2 概率，DPS 直接对所有提示进行 **Top-B 贪婪选择**，无需任何候选批次推演。非平稳衰减机制（$\lambda < 1$）通过逐步遗忘历史观测、将预测向均匀分布漂移，隐式引入探索行为，使纯贪心策略在利用与探索间取得平衡。

### 计算效率的质变

这一设计带来计算开销的**数量级差异**：DS 需对 3 倍以上批次规模进行 LLM 推演（7B 模型约增加 1500 秒/步），而 DPS 仅需低维矩阵运算，更新 $10^7$ 规模数据集仅需 2.4 秒/步、0.9 GiB 内存，无 GPU 内存占用。在 MATH 任务上，DPS 以 DS 25.1% 的推演量（737k vs 2933k）达到相当甚至更优的性能（52.13 vs 52.00），验证了从“推演-验证”到“推理-预测”范式转换的有效性。

## 整体框架

![[assets/figures/papers/paper_list_l29_https_openreview_net_forum_id_voeheZjd8p/figures/001_Figure_1.jpg]]
*Figure 1: Dynamics-Predictive Sampling (DPS) framework. DPS models each prompt’s solving progress in RL finetuning as a dynamical system, treating solving extent as the state with transitions characterized by a hidden Markov model. By employing lightweight inference, it predicts and selects informative (partially solved) prompts online, without requiring rollout-intensive filtering*

Dynamics-Predictive Sampling (DPS) 将提示样本的求解进度形式化为一个动力学系统，并通过隐马尔可夫模型（HMM）进行在线贝叶斯推理，从而在不进行昂贵候选批次推演的前提下实现信息性样本的高效选择。其整体pipeline由四个核心模块串联构成，形成“预测—选择—生成—更新”的闭环。

### Pipeline 总览

**状态预测器（HMM推理）** 是DPS的认知核心。该模块为数据集中每个提示 $\tau$ 维护一个隐状态信念，将求解进度划分为三种离散状态：完全未解（State 1）、部分求解（State 2）、完全求解（State 3）。其中State 2被识别为最具信息量的提示类型，因为其响应组内奖励存在方差，能够提供有效的梯度信号。在每个训练步 $t$，预测器基于历史二进制奖励观测序列 $y_{1:t-1}^{\tau}$，通过贝叶斯滤波计算当前步的先验信念 $\mu_t^{\tau,\mathrm{prior}}(i) := \mathbb{P}(z_t^{\tau}=i \mid y_{1:t-1}^{\tau})$，即在不进行本轮推演的情况下预测提示处于各状态的概率。

**提示采样器（Top-B选择）** 接收预测器输出的State 2先验概率 $\mu_t^{\tau,\mathrm{prior}}(2)$，对所有提示按该概率降序排列，贪心地选取前 $B$ 个构成训练批次 $\mathcal{B}_t = \mathrm{Top}_B(\{\tau \in \mathcal{D} \mid \mu_t^{\tau,\mathrm{prior}}(2)\})$。这一选择策略是纯利用性的，但其底层目标函数已通过非平稳衰减机制隐含引入了探索行为——衰减使得长期未被选中的提示的预测分布逐渐趋向均匀，从而获得被重新采样的机会。

**LLM响应生成与微调** 模块对所选批次中的每个提示采样 $k$ 条响应，使用GRPO算法计算组内归一化优势函数 $\hat{A}_i^{\tau} = \frac{r(\tau, y_i^{\tau}) - \mathrm{mean}(\{r(\tau, y_j^{\tau})\})}{\mathrm{std}(\{r(\tau, y_j^{\tau})\})}$，并通过裁剪策略比率和KL散度惩罚更新策略模型参数。此模块与标准RL微调流程完全一致，DPS仅改变了上游的数据选择逻辑。

**状态与转移更新器** 负责闭环反馈。当本轮推演完成后，被选中提示的真实求解状态 $y_t$（由 $k$ 条响应的奖励模式判定：全错→State 1，混合→State 2，全对→State 3）被观测到。更新器首先通过贝叶斯规则将先验修正为后验 $\mu_t^{\mathrm{post}}(i) = \frac{\delta(y_t,i) \cdot \mu_t^{\mathrm{prior}}(i)}{\sum_k \delta(y_t,k) \cdot \mu_t^{\mathrm{prior}}(k)}$；随后采用带指数衰减的Dirichlet更新调整转移矩阵的后验参数 $\alpha_t(i,j) = \lambda \cdot \alpha_{t-1}(i,j) + (1-\lambda) \cdot \alpha_0(i,j) + \xi_t(i,j)$，其中 $\lambda \in (0,1)$ 控制对历史观测的遗忘速率；最后利用更新后的转移矩阵将后验传播为下一步的先验 $\mu_{t+1}^{\mathrm{prior}} = \Phi_t \mu_t^{\mathrm{post}}$。对于未被选中的提示，由于观测缺失（$y_t = \emptyset$），其先验直接继承为下一步先验，仅受转移矩阵的全局演化影响。

### 输入输出流

- **输入**：完整提示数据集 $\mathcal{D}$，每步的批次大小 $B$，响应组大小 $k$，非平稳衰减率 $\lambda$，初始Dirichlet先验参数 $\alpha_0$。
- **模块间流转**：状态预测器输出所有提示的State 2先验概率向量 → 提示采样器输出大小为 $B$ 的提示索引集合 → LLM生成模块输出 $B \times k$ 条响应及对应的二进制奖励 → 状态与转移更新器输出更新后的后验信念和转移矩阵参数，反馈至下一轮的状态预测器。
- **输出**：经过多轮主动采样训练后的微调策略模型 $\pi_\theta$。

### 关键设计决策

DPS的观测模型采用退化发射模型：当提示被选中时，观测即真实状态（$p(y_t \mid z_t) = \delta(y_t, z_t)$）；当提示未被选中时，观测为空（$y_t = \emptyset$），不提供任何信息。这一设计使得推理仅依赖于被选中提示的稀疏奖励信号，与DS需要对大规模候选批次进行全量推演形成鲜明对比。转移矩阵的每一列上放置独立的Dirichlet先验 $\Phi_t(\cdot, j) \sim \mathrm{Dirichlet}(\alpha_t(1,j), \alpha_t(2,j), \alpha_t(3,j))$，允许模型在观测稀疏的情况下仍能进行贝叶斯边缘化推理。

计算开销方面，DPS的推理与选择仅涉及低维矩阵运算：在 $|\mathcal{D}| = 10^7$ 的数据集上，全量状态更新仅需约2.4秒/步，内存占用约0.9 GiB，且不占用GPU内存。相比之下，DS（Yu et al., 2025）需对3倍以上批次规模进行LLM推演，7B模型下额外运行时增加约1500秒/步。这一根本性的架构差异使得DPS在保持与oracle DS相当性能的同时，将总推演次数压缩至后者的约25%（MATH 1.5B：DPS 737k vs DS 2933k），实现了数据效率与计算效率的双重提升。

## 核心模块与公式推导

DPS 的核心是将每个提示的求解进度建模为一个隐马尔可夫动力学系统，并通过轻量级的在线贝叶斯推理替代昂贵的候选批次推演。其推理管线由四个紧密耦合的模块构成，每个模块对应一个明确的数学操作。

### 状态预测器：HMM 推理

该模块是整个方法的核心。对每个提示 $\tau$，定义隐状态 $z_t^{\tau} \in \{1,2,3\}$ 分别表示“完全未解”、“部分求解”、“完全求解”。其中 State 2 是信息量最高的状态，应被优先采样。

**先验信念定义**：在观测之前，状态分布的先验信念为：

$$\mu_t^{\tau, \mathrm{prior}}(i) := \mathbb{P}(z_t^{\tau} = i \mid y_{1:t-1}^{\tau}), \quad \forall i \in \{1,2,3\}$$

**退化发射模型**：当提示被选中并生成响应时，观测 $y_t$ 直接揭示真实状态（二元奖励的均值可映射为状态类别）；当提示未被选中时，$y_t = \emptyset$，不提供任何信息：

$$p(y_t \mid z_t) = \begin{cases} \delta(y_t, z_t), & \text{if } y_t \in \{1,2,3\}, \\ 1, & \text{if } y_t = \emptyset. \end{cases}$$

**观测更新（贝叶斯规则）**：当获得新观测时，将先验更新为后验：

$$\mu_t^{\mathrm{post}}(i) = \frac{\delta(y_t, i) \cdot \mu_t^{\mathrm{prior}}(i)}{\sum_k \delta(y_t, k) \cdot \mu_t^{\mathrm{prior}}(k)}, \quad \text{if } y_t \in \{1,2,3\}$$

**生成过程**：整个系统状态与观测的联合分布为：

$$p(\boldsymbol{z}_{1:T}, y_{1:T}) = \int p(\boldsymbol{z}_1) \prod_{t=2}^T p(\boldsymbol{z}_t \mid \boldsymbol{z}_{t-1}, \boldsymbol{\Phi}) \prod_{t=1}^T p(y_t \mid \boldsymbol{z}_t) \mathrm{d}\boldsymbol{\Phi}$$

其中转移矩阵 $\boldsymbol{\Phi}$ 被视为随机变量，其每一列上放置独立的 Dirichlet 先验：

$$\Phi_t(\cdot, j) \sim \mathrm{Dirichlet}(\alpha_t(1,j), \alpha_t(2,j), \alpha_t(3,j)), \quad \forall j \in \{1,2,3\}$$

### 状态与转移更新器：非平稳衰减机制

由于 RL 微调过程中模型的求解能力持续变化，提示的状态转移动态是非平稳的。DPS 通过带指数衰减的 Dirichlet 后验更新来适应这一特性：

$$\alpha_t(i,j) = \lambda \cdot \alpha_{t-1}(i,j) + (1-\lambda) \cdot \alpha_0(i,j) + \xi_t(i,j), \quad \lambda \in (0,1)$$

其中 $\lambda$ 控制历史观测的遗忘速率，$\alpha_0$ 为初始先验，$\xi_t(i,j)$ 为本轮观测到的转移计数。该机制使得模型能够逐渐遗忘过时的转移模式，同时隐式引入探索行为——消融实验（Figure 5）证实，移除该机制（$\lambda=1$）会导致 Countdown 3B 任务上的性能和预测准确率明显下降。

**下一步状态预测**：利用当前后验和推断的转移矩阵，预测下一步的先验状态分布：

$$\mu_{t+1}^{\mathrm{prior}} = \Phi_t \mu_t^{\mathrm{post}}, \quad \text{i.e., } \mu_{t+1}^{\mathrm{prior}}(i) = \sum_{j=1}^3 \Phi_t(i,j) \cdot \mu_t^{\mathrm{post}}(j)$$

### 提示采样器：Top-B 选择

基于预测的 State 2 概率，对所有提示进行排序并选取前 $B$ 个构成训练批次：

$$\mathcal{B}_t = \mathrm{Top}_B \left( \left\{ \tau \in \mathcal{D} \mid \mu_t^{\tau, \mathrm{prior}}(2) \right\} \right)$$

该策略表面上是纯贪心的，但由于非平稳衰减机制持续将预测向均匀分布漂移，实际上已隐含了足够的探索行为。实验表明，显式引入熵正则（DPS+Entropy）并未带来显著增益（Figure 17）。

### LLM 响应生成与微调

所选提示批次进入标准的 GRPO 训练流程。对每条提示采样 $k$ 条响应，使用组内归一化优势函数进行策略更新：

$$\hat{A}_i^{\tau} = \frac{r(\tau, y_i^{\tau}) - \mathrm{mean}(\{r(\tau, y_j^{\tau})\}_{j=1}^k)}{\mathrm{std}(\{r(\tau, y_j^{\tau})\}_{j=1}^k)}$$

GRPO 的完整目标函数为：

$$\mathcal{I}_{\mathrm{GRPO}}(\theta) = \mathbb{E}\left[ \frac{1}{k} \sum_{i=1}^k \left( \min\left( \frac{\pi_{\theta}}{\pi_{\theta_{\mathrm{old}}}} \hat{A}_i^{\tau}, \mathrm{clip}\left(\cdot, 1-\epsilon, 1+\epsilon\right) \hat{A}_i^{\tau} \right) - \beta D_{KL}(\pi_{\theta} \| \pi_{\mathrm{ref}}) \right) \right]$$

### 计算效率的关键瓶颈突破

DPS 的计算开销与 Oracle 基线 DS 形成鲜明对比。DS 需要对 $3\times$ 以上批次规模进行 LLM 推演以过滤非部分求解提示（过滤规则为 $\mathrm{std}(\{r(\tau, y_i^{\tau})\}_{i=1}^k) > 0$），其额外推演开销经常超过微调本身。而 DPS 仅需低维矩阵运算：在全数据集（$|\mathcal{D}|=10^7$）上的状态更新与 Top-B 选择仅需约 2.4 秒/步，内存占用 0.9 GiB，且不占用 GPU 内存（Table 6, Table 7）。这使得 DPS 在 MATH 1.5B 任务上以 DS 25.1% 的推演总量（737k vs 2933k）达到了与之相当甚至略优的性能（52.13 vs 52.00, Table 1）。

## 实验与分析

### 核心瓶颈与实验动机

RL微调的关键瓶颈在于：大量训练提示因模型已完全掌握（全对）或完全未掌握（全错）而无法提供有效梯度信号。动态采样（DS）通过在大规模候选批次上进行推演并筛选奖励方差大于零的提示来缓解此问题，但其额外计算开销经常超过微调本身。DPS的核心实验目标即验证：能否在不进行昂贵推演的前提下，通过轻量级HMM推理实现与DS相当的样本效率？

### 主要结果

**数学推理任务（Table 1）**：在1.5B模型上，DPS以仅73.7万次推演达到52.13的平均Pass@1准确率，与oracle DS（293.3万次推演，52.00）相当，且显著优于均匀采样US（48.57）。DPS的推演量仅为DS的25.1%，却实现了+3.56的绝对提升。在7B模型上，DPS（63.13）同样略优于DS（62.42），验证了方法的跨模型规模鲁棒性。

![[assets/figures/papers/paper_list_l29_https_openreview_net_forum_id_voeheZjd8p/figures/012_Table_1.jpg]]
*Table 1: Evaluation across mathematics benchmarks. ‘+’ represents finetuning with the method*

**推理效率对比**：DPS的运行时间约为DS的一半（7B模型，MATH数据集）。DS每步需额外约1500秒用于候选批次推演，而DPS的HMM推理与选择在全数据集规模（|D|=10^7）下仅需2.4秒/步，内存占用0.9 GiB，且不占用GPU内存（Table 6, Table 7）。这一效率优势使得DPS在实际部署中具有显著的资源节约意义。

![[assets/figures/papers/paper_list_l29_https_openreview_net_forum_id_voeheZjd8p/figures/081_Table_6.jpg]]
*Table 6: Computational cost of different operations across varying dataset sizes, measured by perstep runtime and memory usage during the finetuning of DeepSeek-R1-Distill-Qwen-7B (8 A100 GPUs, batch size 256). The results for LLM training and generation are evaluated on the MATH dataset, while those for DPS are obtained on pseudo-datasets that emulate large-scale scenarios*

![[assets/figures/papers/paper_list_l29_https_openreview_net_forum_id_voeheZjd8p/figures/082_Table_7.jpg]]
*Table 7: Computational cost of different operations across varying LLM sizes, measured by perstep runtime for finetuning on the MATH dataset (8 A100 GPUs, batch size 256). The 1.5B and 7B models refer to DeepSeek-R1-Distill-Qwen-1.5B and DeepSeek-R1-Distill-Qwen-7B, respectively*

**Countdown与几何推理任务**：在Countdown CD-34任务（3B模型）上，DPS达到74.27，超出US 4.40个百分点，仅略低于DS的74.95（Table 2）。在Geometry3k任务上，DPS达到44.47，超出US 4.25个百分点（Table 3）。跨任务的一致性表明DPS的动力学建模具有良好的任务泛化性。

![[assets/figures/papers/paper_list_l29_https_openreview_net_forum_id_voeheZjd8p/figures/013_Table_2.jpg]]
*Table 2: Evaluation on Countdown*

![[assets/figures/papers/paper_list_l29_https_openreview_net_forum_id_voeheZjd8p/figures/071_Table_3.jpg]]
*Table 3: Evaluation results on Geometry*

### 预测能力验证

**有效样本比**（Figure 2）：DPS在多个任务中持续选取出约90%的部分求解提示（State 2），远高于US和HR。这表明HMM推理能够准确识别最具信息性的训练样本。

![[assets/figures/papers/paper_list_l29_https_openreview_net_forum_id_voeheZjd8p/figures/007_Figure_2.jpg]]
*Figure 2: Proportion of partially solved prompts (Effective Sample Ratio) within sampled batches under different data sampling strategies, along with prediction metrics of DPS*

**混淆矩阵演变**（Figure 3）：随训练推进，DPS预测的混淆矩阵对角元素持续加强，中心单元格（State 2）显著突出。这验证了状态识别能力随训练逐步提升，且模型能有效区分三类求解状态。

![[assets/figures/papers/paper_list_l29_https_openreview_net_forum_id_voeheZjd8p/figures/010_Figure_3.jpg]]
*Figure 3: Confusion Matrix (CM) for DPS predictions at different training steps across tasks*

### 消融实验

**非平稳衰减机制（Figure 5）**：移除非平稳衰减（λ=1）导致Countdown 3B任务上的性能和预测准确率明显下降。衰减机制使DPS能适应训练过程中提示求解动态的演变，同时隐含地引入探索行为——较小的λ值产生更均匀的样本计数分布（Figure 7a）。

![[assets/figures/papers/paper_list_l29_https_openreview_net_forum_id_voeheZjd8p/figures/017_Figure_5.jpg]]
*Figure 5: Performance and prediction accuracy of DPS under varying non-stationary decay ratios λ*

**状态划分粒度（Figure 6）**：将求解状态划分为3类在有效样本比和最终性能间取得了最佳折中。更粗的划分（2类）损失了细粒度区分能力，更细的划分（5类、7类）则因状态过于稀疏导致预测精度下降和样本效率降低。

![[assets/figures/papers/paper_list_l29_https_openreview_net_forum_id_voeheZjd8p/figures/018_Figure_6.jpg]]
*Figure 6: Performance and effective sample ratios of DPS under different solving-state partitions*

**响应组大小敏感性（Figure 15, Figure 16）**：在k=4的极限设置下，DPS的测试准确率超过US两倍以上，且预测准确率仍保持高位。这凸显了DPS在小样本响应下的鲁棒优势——当每组仅采样4条响应时，传统方法几乎无法有效区分提示的信息性。

**替代方法对比（Figure 18）**：简单的启发式预测（Var+EMA）和基于多样性的采样均无法达到DPS的有效样本比和最终性能，验证了HMM形式化建模的必要性。

**熵正则探索（Figure 17）**：显式引入熵正则的采样（DPS+Entropy）未显著超越基础DPS，因为非平稳衰减机制已隐含足够的探索行为，额外的显式探索未带来增益。

### 失败模式与局限

DPS的纯贪心Top-B选择策略在批内多样性方面缺乏显式控制，可能在复杂训练阶段遗漏部分高潜力提示。此外，关键超参数λ需针对不同任务手动调整，缺乏自动适应任务动态的机制。在数据集规模超过10^8时，线性增长的推理开销可能需要候选子集近似方案，这会在一定程度上牺牲预测精度。

### 补充图表

![[assets/figures/papers/paper_list_l29_https_openreview_net_forum_id_voeheZjd8p/figures/072_Table_4.jpg]]
*Table 4: Evaluation on general reasoning benchmarks for models trained on the MATH dataset. Performance is measured by Pass@1 accuracy with a maximum response length of 8k tokens. ’+’ represents finetuning with the method*

![[assets/figures/papers/paper_list_l29_https_openreview_net_forum_id_voeheZjd8p/figures/076_Table_5.jpg]]
*Table 5: Evaluation across mathematics benchmarks under a maximum response length of 32k. ’+’ represents finetuning with the method. Evaluation is based on average Pass@1 accuracy over 16 responses per prompt*

## 方法谱系与知识库定位

### 与基线方法的因果差异

DPS 的核心创新在于将提示选择从“推演密集型”转变为“推理密集型”。理解这一转变需要先审视三种基线方法的根本机制及其瓶颈。

**均匀采样（US）** 是最朴素的基线：每个训练步从数据集中随机抽取 $B$ 个提示，无任何优先级筛选。其失败模式明确——大量训练提示处于“完全未解”（所有 $k$ 条响应均错误）或“完全解决”（所有响应均正确）状态，这两类提示在 GRPO 中的组内优势估计方差趋近于零，无法提供有效的梯度信号。US 的有效样本比（部分求解提示占比）通常仅为 30%–50%，意味着超过一半的推演计算被浪费。

**动态采样（DS）**（Yu et al., 2025）直接针对这一问题：每步从数据集中采样一个扩大的候选批次 $\hat{\mathcal{B}}_t$（通常 $3\times B$），对其中所有提示执行完整的 $k$ 条响应推演，然后仅保留奖励标准差大于零的提示构成训练批次：

$$\mathcal{B}_t = \left\{ \tau \in \hat{\mathcal{B}}_t \mid \mathrm{std}(\{r(\tau, y_i^\tau)\}_{i=1}^k) > 0 \right\}$$

DS 的有效样本比接近 100%，但其代价是巨大的：每步需对 $3\times B$ 个提示执行推演，而非 $B$ 个。在 7B 模型上，DS 的运行时增加约 1500 秒/步。这一开销经常超过 RL 微调本身的计算成本，使 DS 成为“高资源预言机”基线而非实用方案。

**历史重采样（HR）**（Zhang et al., 2025）采用启发式规则：在当前 epoch 内排除已产生全对响应的提示。HR 无需额外推演，但仅能过滤“已完全解决”的提示，对“完全未解”提示无能为力，且无法感知提示求解状态的动态变化——一个提示可能从部分求解退化为完全未解（因模型遗忘或分布偏移），HR 无法捕捉这种退化。

DPS 的因果杠杆在于：**用隐马尔可夫模型（HMM）的在线贝叶斯推理替代候选批次推演**。具体而言，DPS 将每个提示的求解进度建模为三态动力学系统（State 1: 完全未解，State 2: 部分解决，State 3: 完全解决），利用历史稀疏奖励信号（仅当提示被选中时才获得观测）进行贝叶斯滤波，预测每个提示在下一步处于 State 2 的先验概率 $\mu_t^{\tau,\mathrm{prior}}(2)$，然后通过 Top-B 贪婪选择直接构成训练批次：

$$\mathcal{B}_t = \mathrm{Top}_B \left( \left\{ \tau \in \mathcal{D} \mid \mu_t^{\tau,\mathrm{prior}}(2) \right\} \right)$$

这一设计将数据选择的计算复杂度从 $\mathcal{O}(|\hat{\mathcal{B}}_t| \cdot k \cdot \text{LLM推演})$ 降至 $\mathcal{O}(|\mathcal{D}| \cdot \text{低维矩阵运算})$。在 $|\mathcal{D}|=10^7$ 规模下，DPS 的全数据集更新仅需 2.4 秒/步，内存占用 0.9 GiB，且不占用 GPU 显存（Table 6）。与之对比，DS 的总推演次数通常是 DPS 的 4 倍（MATH 1.5B：DS 293.3 万次 vs DPS 73.7 万次），而 DPS 在 MATH 平均准确率上以 52.13 略优于 DS 的 52.00（Table 1）。

### 关键设计选择与消融证据

DPS 的几个设计选择经消融实验验证为性能的关键支撑：

**非平稳衰减机制（λ）** 是 DPS 适应求解动态变化的核心。当 $\lambda=1$（移除衰减，等价于标准平稳 HMM）时，Countdown 3B 任务上的性能和预测准确率均出现明显下降（Figure 5）。衰减机制通过 $\alpha_t(i,j) = \lambda \cdot \alpha_{t-1}(i,j) + (1-\lambda) \cdot \alpha_0(i,j) + \xi_t(i,j)$ 逐渐遗忘陈旧观测，使转移矩阵能跟踪模型能力提升带来的状态演化加速。较小的 $\lambda$ 还隐含地引入了探索行为：预测分布向均匀先验漂移，使长期未被选中的提示有更高概率被重新采样（Figure 7a）。

**三态划分** 在有效样本比和最终性能间取得了最佳折中（Figure 6）。更粗的划分（如二态：可解/不可解）无法区分“部分解决”这一信息量最高的类别；更细的划分则因观测稀疏导致预测精度下降，反而损害样本效率。

**纯贪心 Top-B 选择** 虽看似仅利用而无探索，但实验表明显式引入熵正则的 DPS+Entropy 变体未带来显著增益（Figure 17），因为非平稳衰减已隐含足够的探索行为。DPS 在响应组大小 $k=4$ 的极限设置下仍保持高预测准确率，且测试准确率超过 US 的两倍以上（Figure 15, 16），验证了其在小样本响应下的鲁棒性。

### 适用边界与局限

DPS 的适用性受以下边界约束：

1. **奖励类型限制**：当前 DPS 设计针对二元结果奖励（正确/错误），求解状态的定义直接依赖于 $k$ 条响应中正确响应的比例。将其扩展至连续过程奖励的初步尝试仍依赖启发式量化边界，尚未建立过程奖励与样本信息性之间的原则性联系。

2. **数据集规模线性增长**：DPS 的推理与选择开销随 $|\mathcal{D}|$ 线性增长。虽然在典型规模（$10^6$–$10^7$）下可忽略，但当 $|\mathcal{D}| > 10^8$ 时可能需要启用候选子集近似方案，这会牺牲部分预测精度。

3. **超参数敏感性**：关键超参数 $\lambda$（非平稳衰减率）需针对不同任务手动调整，缺乏自动适应任务动态的机制。此外，DPS 的初始状态信念设为均匀分布，对新任务的启动阶段可能需要额外的热启动策略。

4. **批内多样性缺失**：Top-B 选择未显式考虑批内多样性或多模态分布。在复杂训练阶段，可能存在多个高 State 2 概率但高度相似的提示同时被选中，导致批次梯度信息冗余。

### 开放问题

DPS 的动力学建模框架开启了若干值得探索的方向：

- **过程奖励的原则性扩展**：如何建立过程奖励（process rewards）与样本信息性之间的可靠映射，从而将 DPS 或其他主动采样方法原则性地应用于过程奖励环境？这可能需要重新定义“部分求解”状态，使其能捕捉推理链中间步骤的信息量。

- **探索-利用的显式平衡**：能否设计更复杂的采样准则（如基于后验熵的汤普森采样或贝叶斯优化）来显式平衡探索与利用，从而在保持预测效率的同时进一步提升训练鲁棒性？当前依赖非平稳衰减的隐式探索可能不足以应对高度非平稳的训练初期。

- **跨模态与跨任务泛化**：DPS 的动力学建模能否拓展至多模态推理、多轮对话或代码生成等场景？这些场景中的“求解状态”定义、状态转移特性以及观测稀疏性可能与数学推理有本质差异，特别是当状态演化呈现非马尔可夫特性时，当前的 HMM 假设可能不再适用。

## 原文 PDF

![[paperPDFs/ICLR_2026/Dynamics_Predictive_Sampling_for_Active_RL_Finetuning_of_Large_Reasoning_Models.pdf]]
