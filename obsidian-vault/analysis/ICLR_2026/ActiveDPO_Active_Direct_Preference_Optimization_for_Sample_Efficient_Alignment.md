---
title: "ActiveDPO: Active Direct Preference Optimization for Sample-Efficient Alignment"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/ActiveDPO_Active_Direct_Preference_Optimization_for_Sample_Efficient_Alignment.pdf
project_link: null
code_link: null
aliases:
- ActiveDPO
tags:
- ICLR_2026
- topic/reinforcement_learning_planning_agents
- topic/reinforcement_learning_planning_agents/function_approximation
core_operator: "ActiveDPO selects preference pairs by the inverse-covariance norm of LLM implicit-reward gradient differences."
primary_logic: "It iteratively generates candidate responses, chooses high-uncertainty and diverse pairs for labeling, then updates the model with DPO on the selected preferences."
claims:
- "The selection criterion is derived from a reward-difference error bound tied to gradient difference norms."
- "Using the current LLM as the implicit reward model couples data selection to the alignment target."
- "LoRA gradients and random projection reduce the cost of applying the criterion at scale."
---

# ActiveDPO: Active Direct Preference Optimization for Sample-Efficient Alignment

> [!tip] 核心洞察
> 通过理论推导的误差上界（Proposition 1），将奖励差异估计误差与梯度差异的范数（经协方差逆矩阵加权）联系起来，从而利用LLM的梯度作为不确定性度量来选择信息量最大的偏好数据，同时通过LoRA和随机投影降低计算开销。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | ActiveDPO：面向样本高效对齐的主动直接偏好优化 |
| 英文题名 | ActiveDPO: Active Direct Preference Optimization for Sample-Efficient Alignment |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=RD4XgyVyGh) |
| Topic | #topic/reinforcement_learning_planning_agents #topic/reinforcement_learning_planning_agents/function_approximation |
| Method | ActiveDPO |
| Dataset | TLDR summarization, WebGPT long-form QA |

> [!tip] 效果简介
> - TLDR summarization 上，平均奖励 为 ActiveDPO，对比 Random, APO, APLP，变化 ActiveDPO持续获得更高奖励。
> - WebGPT long-form QA 上，平均奖励 为 ActiveDPO，对比 Random, APO, APLP，变化 ActiveDPO持续获得更高奖励。
> - TLDR summarization 上，胜率 为 ActiveDPO，对比 Random, APO, APLP，变化 ActiveDPO在最后几轮迭代中胜率最高。

## 概要

ActiveDPO（Active Direct Preference Optimization）是一种面向大语言模型（LLM）偏好对齐的样本高效主动学习方法。其核心目标是在有限的人类标注预算下，通过理论驱动的数据选择准则，从候选池中挑选出信息量最大的偏好数据对，从而最大化LLM的对齐性能。该方法利用LLM自身的隐式奖励函数（由DPO定义）的梯度差异作为不确定性度量，并通过协方差逆矩阵实现多样性正则化，同时结合LoRA和随机投影技术降低计算开销。实验表明，ActiveDPO在多个LLM（Llama-2-7B, Gemma-2B, Qwen3-4B）和真实偏好数据集（TLDR summarization, WebGPT long-form QA）上持续优于随机选择（Random）、APO和APLP等基线方法。



收集高质量人类偏好数据集是LLM对齐（如RLHF和DPO）的关键步骤，但这一过程成本高昂且资源密集。现有主动选择方法存在以下不足：
- **缺乏理论基础**：如APLP（Muldrew et al., 2024）基于启发式不确定性量化，缺乏理论保证。
- **强假设限制**：如APO（Das et al., 2024）假设线性奖励函数，这在真实LLM对齐场景中不成立，因为DPO的隐式奖励函数是非线性的。
- **模型无关性**：现有方法通常使用外部独立奖励模型进行选择，未考虑所选数据与待对齐LLM之间的关联。

因此，需要一种**理论驱动、适用于非线性奖励函数、且利用LLM自身作为奖励模型**的主动选择方法。



## 核心方法与创新机理

ActiveDPO的核心创新在于：

1. **理论驱动的选择准则**：通过Proposition 1（见附录A.6）建立了奖励差异估计误差的上界，该上界与梯度差异的范数（经协方差逆矩阵加权）相关，从而将不确定性估计与LLM的梯度联系起来。
2. **利用LLM自身作为奖励模型**：选择准则基于当前LLM的隐式奖励函数r_θ的梯度，而非外部模型，使得选择过程与对齐目标紧密耦合。
3. **多样性正则化**：通过V_{t-1}^{-1}矩阵对已探索的梯度方向进行降权，鼓励选择互补数据，避免信息冗余。
4. **计算效率优化**：通过LoRA梯度（O(k)）和随机投影（降至d=8192维）将梯度维度降至可处理规模，并采用批处理选择策略。



![[assets/figures/papers/iclr26_0002_RD4XgyVyGh_ActiveDPO_Active_Direct_Preference_Optimization/figures/001_Figure_1.jpg]]
*Figure 1: (a) TLDR with Llama-2-7B*

ActiveDPO的迭代流程包含四个模块：

1. **响应生成**：使用当前LLM π_{θ_{t-1}}为数据集D中的每个提示生成m对响应，形成候选池D_t。
2. **主动选择**：基于梯度差异准则（Eq. 3）从D_t中选择信息量最大的B个三元组(x, y_1, y_2)，并在批内更新V_{t-1}矩阵。
3. **人类标注**：获取所选数据的人类偏好反馈(y_w ≻ y_l | x)，得到标注数据集D_t^l。
4. **DPO训练**：使用D_t^l通过DPO目标函数更新LLM参数，得到π_{θ_t}。



### 5.1 DPO隐式奖励函数

DPO将奖励函数隐式参数化为LLM的策略：

$$r_\theta(x, y) = \beta \frac{\pi_\theta(y \mid x)}{\pi_{\mathrm{ref}}(y \mid x)}$$

其中π_ref为参考LLM，β为正则化超参数。偏好概率由Bradley-Terry-Luce模型给出：

$$p(y_1 \sim y_2 \mid x) = \frac{\exp(r_\theta(x, y_1))}{\exp(r_\theta(x, y_1)) + \exp(r_\theta(x, y_2))} = \sigma(r_\theta(x, y_1) - r_\theta(x, y_2))$$

DPO训练目标为：

$$L_{\mathrm{DPO}}(\pi_\theta, \pi_{\mathrm{ref}}) = -\mathbb{E}_{(x, y_w, y_l) \sim D^l} \left[ \log \sigma(r_\theta(y_w \mid x) - r_\theta(y_l \mid x)) \right]$$

### 5.2 ActiveDPO选择准则

ActiveDPO的选择准则基于梯度差异的范数，经逆协方差矩阵加权：

$$x, y_1, y_2 = \operatorname{argmax}_{x, y_1, y_2 \sim D_t \setminus D_t^s} \| \nabla r_{\theta_{t-1}}(x, y_1) - \nabla r_{\theta_{t-1}}(x, y_2) \|_{V_{t-1}^{-1}}$$

其中V_{t-1}是已选数据梯度差异的经验协方差矩阵，在批选择过程中每选一个数据点即更新：

$$V_{t-1} = V_{t-1} + \varphi_{t-1}(x_b^t, y_{b,1}^t, y_{b,2}^t) \varphi_{t-1}(x_b^t, y_{b,1}^t, y_{b,2}^t)^\top$$

### 5.3 理论分析

论文在附录A.6中建立了正式的理论框架。定义梯度差异向量：

$$\varphi_{t-1}(x,y_1,y_2) = \frac{1}{\sqrt{m}} \big( \nabla r_{\theta_{t-1}}(x,y_1) - \nabla r_{\theta_{t-1}}(x,y_2) \big)$$

以及已选数据的协方差矩阵：

$$V_{t-1} = \sum_{p=1}^{t-1} \sum_{x,y_1,y_2 \sim D_p^s} \varphi_{t-1}(x,y_1,y_2) \varphi_{t-1}(x,y_1,y_2)^\top + \frac{\lambda}{\kappa_\mu} \mathbf{I}$$

不确定性估计为：

$$\sigma_{t-1}(x,y_1,y_2) = \frac{\lambda}{\kappa_\mu} \| \varphi_{t-1}(x,y_1,y_2) \|_{V_{t-1}^{-1}}$$

**Proposition 2**（正式误差界）给出：

$$\bigg| \Big[ r_{\theta_{t-1}}(x,y_1) - r_{\theta_{t-1}}(x,y_2) \Big] - \big[ r(x,y_1) - r(x,y_2) \big] \bigg| \leq \nu_T \sigma_{t-1}(x,y_1,y_2) + \varepsilon_{m,t}$$

该不等式表明，奖励差异的预测误差以高概率被不确定性估计σ_{t-1}和宽度相关误差项ε_{m,t}所界定。

### 5.4 计算效率优化

| 技术 | 描述 | 效果 |
|------|------|------|
| LoRA梯度 | 仅计算低秩适配器的梯度 | 梯度维度从全参数降至O(k) |
| 随机投影 | 使用Johnson-Lindenstrauss引理将梯度投影至d=8192维 | 进一步降低存储和计算成本 |
| 梯度归一化 | 将所有梯度归一化至单位l2范数 | 避免选择准则偏向短句子 |
| 批内更新 | 在批选择过程中动态更新V_{t-1} | 实现批内多样性 |

Table 1比较了不同选择策略的计算开销：Random为O(n)；APO为O(nk)；APLP为O(n)；ActiveDPO为O(nkd + d^3 + Bd^2)。



## 实验与关键发现

### 6.1 主实验结果

Figure 1展示了不同选择策略下LLM生成响应的平均奖励比较。ActiveDPO在TLDR summarization和WebGPT long-form QA两个数据集上，使用Llama-2-7B、Gemma-2B和Qwen3-4B三种模型，均持续获得比Random、APO和APLP更高的平均奖励。

Figure 4展示了胜率比较。ActiveDPO在最后几轮迭代中胜率最高，而APLP在后期出现性能退化，APO则因线性奖励假设在不同设置下表现不一致。

![[assets/figures/papers/iclr26_0002_RD4XgyVyGh_ActiveDPO_Active_Direct_Preference_Optimization/figures/004_Figure_4.jpg]]
*Figure 4: (d) WebGPT with Llama-2-7B*

### 6.2 消融实验

**不同模型需要不同数据**（Figure 2）：将Gemma-2B在两个不同SFT数据集上训练得到Model 1和Model 2，在3个不同偏好数据集上进行DPO训练。结果显示，Model 2在Dataset 2上取得最佳性能，而Model 1在同一数据集上表现最差，验证了不同LLM需要不同的数据子集。

![[assets/figures/papers/iclr26_0002_RD4XgyVyGh_ActiveDPO_Active_Direct_Preference_Optimization/figures/002_Figure_2.jpg]]
*Figure 2: (b) TLDR with Gemma-2B*

**梯度归一化**（Figure 3a, 3b）：在WebGPT数据集上使用Gemma-2B时，归一化提升了ActiveDPO性能；在TLDR数据集上影响不大。

![[assets/figures/papers/iclr26_0002_RD4XgyVyGh_ActiveDPO_Active_Direct_Preference_Optimization/figures/003_Figure_3.jpg]]
*Figure 3: (c) TLDR with Qwen3-4B*

**随机投影维度**（Figure 3c, 3d）：维度8192足以平衡性能和计算成本，更低维度导致性能下降。

### 6.3 计算开销分析

ActiveDPO的主要计算开销来自LLM的前向和反向传播（使用LoRA），而非随机投影步骤。其额外计算成本由优越的标注效率所证明——人类标注成本通常远超数据选择的计算成本。

### 补充图表

![[assets/figures/papers/iclr26_0002_RD4XgyVyGh_ActiveDPO_Active_Direct_Preference_Optimization/figures/013_Table_1.jpg]]
*Table 1: Comparison of computational overhead per iteration for different selection strategies. n: number of candidate data points; k: number of LoRA parameters; d: projection dimension; B: batch size.*

![[assets/figures/papers/iclr26_0002_RD4XgyVyGh_ActiveDPO_Active_Direct_Preference_Optimization/figures/005_Figure_5.jpg]]
*Figure 5: (e) WebGPT with Gemma-2B*



## 定位与知识库关联

ActiveDPO属于**主动学习**与**LLM偏好对齐**的交叉领域。其方法谱系如下：

- **理论基础**：受神经对偶赌博机（neural dueling bandits, Verma et al., 2025）启发，将不确定性量化从线性奖励函数推广至非线性神经网络奖励函数。
- **与现有方法对比**：
  - 相比APO（Das et al., 2024）：APO假设线性奖励函数，ActiveDPO适用于非线性奖励函数。
  - 相比APLP（Muldrew et al., 2024）：APLP使用启发式不确定性量化（奖励差异绝对值），ActiveDPO具有理论保证。
  - 相比基于外部模型的方法（Carvalho Melo et al., 2024; Das et al., 2024）：ActiveDPO使用LLM自身作为奖励模型，实现选择与对齐的紧密耦合。
- **局限性**：
  - 选择准则需要为每个数据点计算梯度，计算开销大且需大量存储。
  - Proposition 1的理论分析依赖神经正切核（NTK）理论，该理论主要针对全连接网络，对Transformer架构的严格推广尚未完全建立（尽管kernel constancy已通过tensor programs框架建立，但GP limit的证明尚未完成）。
  - 随机投影可能丢失部分梯度信息。
- **开放问题**：
  - 如何将理论保证严格扩展到Transformer架构？
  - 是否存在更高效的方法近似梯度差异计算？
  - 随机投影的最优维度是否依赖于具体任务和模型规模？
  - ActiveDPO的选择准则是否可在其他偏好优化方法（如RLHF, IPO）中推广？



## 原文 PDF

![[paperPDFs/ICLR_2026/ActiveDPO_Active_Direct_Preference_Optimization_for_Sample_Efficient_Alignment.pdf]]
