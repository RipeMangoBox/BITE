---
title: "Planner Aware Path Learning in Diffusion Language Models Training"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/Planner_Aware_Path_Learning_in_Diffusion_Language_Models_Training.pdf
project_link: null
code_link: https://github.com/pengzhangzhi/PAPL
openreview_forum_id: lAlI5FuIf7
aliases:
- PAPLP
- PAPLDLMT
tags:
- ICLR_2026
- topic/reinforcement_learning_planning_agents
- topic/reinforcement_learning_planning_agents/planning_control
core_operator: "在训练损失中引入基于规划器的权重，使模型利用去噪器自身的置信度（自规划）对更可能被规划器选择的去掩码位置赋予更高权重，从而直接对齐训练与推理。"
primary_logic: "通过推导规划器感知证据下界（P-ELBO），将任意规划器纳入训练目标，表明只需将标准均匀去掩码损失替换为加权的交叉熵损失（一行代码修改），即可显著提升生成质量，且无需额外推理开销。"
claims:
- "贪婪祖先采样可在不完美去噪器下违反标准DLM ELBO，即log(p_greedy) < 标准ELBO。"
- "PAPL使蛋白质序列的可折叠性相对提升40%（DLM-150M: 42.43% → PAPL: 59.40%）"
- "文本生成 MAUVE 最多提升4倍（T=128时PAPL 0.067 vs 标准DLM 0.011）"
- "代码生成 HUMANEVAL pass@10 相对提升23%（31.1 → 38.4）"
---

# Planner Aware Path Learning in Diffusion Language Models Training

> [!tip] 核心洞察
> 通过推导规划器感知证据下界（P-ELBO），将任意规划器纳入训练目标，表明只需将标准均匀去掩码损失替换为加权的交叉熵损失（一行代码修改），即可显著提升生成质量，且无需额外推理开销。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 扩散语言模型训练中的规划器感知路径学习 |
| 英文题名 | Planner Aware Path Learning in Diffusion Language Models Training |
| 会议/期刊 | ICLR 2026 (Oral) |
| Links | [paper](https://openreview.net/forum?id=lAlI5FuIf7) · [GitHub](https://github.com/pengzhangzhi/PAPL) |
| Topic | #topic/reinforcement_learning_planning_agents #topic/reinforcement_learning_planning_agents/planning_control |
| Method | Planner Aware Path Learning (PAPL) |
| Dataset | Protein Sequence Generation (foldability), Unconditional Text Generation (MAUVE, T=128), HumanEval (code generation, pass@10), pass@1) |

> [!tip] 效果简介
> - Protein Sequence Generation (foldability) 上，Foldability (%) 为 59.40，对比 42.43 (DLM-150M without PAPL)，变化 +16.97 pp / ~40% relative improvement。
> - Unconditional Text Generation (MAUVE, T=128) 上，MAUVE 为 0.067，对比 0.011 (MDLM), or baseline DLM，变化 4× relative gain。
> - HumanEval (code generation, pass@10) 上，Pass@10 为 38.4，对比 31.1 (DLM without PAPL)，变化 +7.3 / 23% relative improvement。

## 概要

扩散语言模型（DLM）在文本、代码和蛋白质序列生成中展现出竞争力，但其训练与推理之间存在一个根本性不匹配：标准训练假设均匀随机的去掩码过程，而推理时却使用贪婪、置信度排序等规划器来选择去掩码位置。这一错位意味着训练优化的目标（均匀ELBO）并不能有效约束规划器下的生成质量——论文从理论上证明，即使去噪器在均匀ELBO下表现良好，贪婪祖先采样仍可能使生成概率低于该ELBO所保证的下界。

**核心结论**：本文提出**规划器感知路径学习（Planner Aware Path Learning, PAPL）**，通过推导规划器感知证据下界（P-ELBO），将任意规划器纳入训练目标。PAPL 的核心操作是在标准掩码扩散损失中引入基于去噪器自身置信度的权重——对规划器更可能选中的去掩码位置赋予更高权重，从而使训练动力学直接对齐推理动力学。该方法仅需一行代码修改，无需额外推理开销。

**方法定位**：PAPL 属于训练目标层面的对齐方法，不改变模型架构或推理策略。它利用去噪器自身的预测置信度作为“自规划器”（soft greedy planner），在标准均匀掩码采样的基础上计算加权交叉熵损失。方法可视为在路径级KL散度框架下，用规划器权重调制参考链与模型链之间的差异。

**主要结果**：PAPL 在三个领域上取得一致且显著的增益：
- **蛋白质序列生成**：可折叠性相对提升约40%（DLM-150M: 42.43% → PAPL: 59.40%），结构质量指标（pLDDT、pTM、pAE）全面改善。
- **文本生成**：MAUVE 指标最高提升4倍（T=128时 PAPL 0.067 vs 标准MDLM 0.011），生成困惑度显著降低。
- **代码生成**：HumanEval pass@10 相对提升23%（31.1 → 38.4），pass@1 亦有稳定增益。

消融实验表明，PAPL 在训练步数、采样步数和温度变化下均保持优势，且训练收敛更快、对推理温度更鲁棒。不过，纯 PAPL 损失训练不稳定，需与标准均匀损失混合使用；超参数（温度 τ 和权重 α）需按任务微调，论文给出了起步建议（τ=1, α=1）。



### 扩散语言模型的训练-推理失配

扩散语言模型（Diffusion Language Models, DLMs）通过迭代去掩码从全掩码序列生成离散文本，其标准训练基于均匀去掩码的证据下界（ELBO）。该目标对所有被掩码位置施加均等权重，假设训练时的前向掩码过程与推理时的反向去掩码过程在动力学上一致。

然而实际推理中，模型通常依赖**规划器**（planner）——如贪婪选择、置信度阈值或概率边际排序——来决定每一步去掩码的位置。这些规划器在路径空间中产生高度非均匀的遍历分布，与训练时假设的均匀路径存在根本性偏差。论文通过**命题3.1**严格证明了这一失配的后果：即使去噪器本身具有合理质量，贪婪祖先采样生成的序列其对数似然可能**低于**标准ELBO所给出的下界，即

$$\log(p_\theta^{\text{greedy}}(\mathbf{x}_0)) < \mathcal{E}^{\theta,\mathrm{unif}}(\mathbf{x}_0)$$

这意味着标准ELBO无法有效约束规划器下的生成质量——模型可能在训练损失上表现良好，但推理时生成的样本质量显著下降。

### 现有方法的局限

当前DLM的训练范式存在一个结构性缺口：**训练目标与推理规划器相互独立**。具体而言：

- **标准MDLM训练**（Equation 1）对每个被掩码位置施加均匀权重 $1/(L-k)$，将模型容量平均分配到所有可能的去掩码路径上，包括大量推理时规划器永远不会遍历的区域。
- **推理时规划器**（如P2、贪婪祖先采样）则沿着特定的高置信度路径前进，这些路径在训练中并未获得足够的梯度信号。

已有工作尝试通过改进规划器设计（如ReMDM、MDLM+DFM）或引入微调策略来缓解这一问题，但均未从训练目标层面直接对齐前向掩码与反向规划动力学。这种“训练一套、推理一套”的分离式设计，使得模型在关键生成路径上的去噪能力缺乏针对性优化。

### 本文动机与核心思路

本文的核心洞察是：**训练目标应当感知推理时使用的规划器**，使模型在规划器偏好的路径上获得更强的去噪能力。为此，作者从变分推断出发，推导了**规划器感知的证据下界（P-ELBO）**，将任意规划器纳入训练目标。该下界将生成对数似然分解为规划器加权的交叉熵项与规划器-参考动力学间的KL散度项，从理论上建立了训练-推理对齐的优化框架。

基于P-ELBO，本文提出**规划器感知路径学习（Planner Aware Path Learning, PAPL）**，其核心操作极为简洁：在标准均匀掩码损失中引入基于去噪器自身置信度的权重 $w^i$，对更可能被规划器选择的去掩码位置赋予更高损失权重。最终PAPL训练目标为：

$$\mathcal{L}_{\mathrm{PAPL}}(\theta)=-\mathbb{E}_{\mathbf{x}_0,k,\mathbf{x}_k}\left[\sum_{i:x_k^i=\mathbf{m}}\frac{1}{L-k}(1+\alpha w^i)\log\left(\mathrm{Cat}(x_0^i;D_\theta^i(\mathbf{x}_k))\right)\right]$$

其中 $w^i \propto \exp(\tau^{-1}\log\mathrm{Cat}(z^j;D_\theta^j(\mathbf{x})))$ 为软最大化规划器权重，$\alpha$ 控制规划器影响强度。这一修改仅需**一行代码**，无需额外推理开销，即可将训练动力学与推理规划器对齐。



## 核心方法与创新机理

PAPL 的核心创新在于**将推理时的规划器偏好直接注入训练损失**，从而消除扩散语言模型（DLM）中长期存在的训练-推理动力学失配。这一创新通过一个理论推导和一个工程实现共同完成。

### 问题根源：训练与推理的动力学失配

标准 DLM 的训练目标（均匀 ELBO）假设去掩码过程在所有被掩码位置上均匀进行：

$$\mathcal{E}^{\theta,\mathrm{unif}}(\mathbf{x}_0) = L\mathbb{E}_{k\sim\mathrm{Unif}([0:L-1])}\left[\mathbb{E}_{\mathbf{x}_k\sim\mathrm{Unif}(\mathcal{X}_{L-k}(\mathbf{x}_0))}\left[\sum_{i=1,x_k^i=\mathbf{m}}^L\frac{1}{L-k}\log\left(\mathrm{Cat}(x_0^i;D_\theta^i(\mathbf{x}_k))\right)\right]\right]$$

然而，推理时实际使用的是贪婪、置信度或 P2 等规划器，它们会优先选择模型最确信的位置去掩码。这导致两个后果：

1. **理论层面**：贪婪祖先采样可能违反标准 ELBO，即 $\log(p_\theta^{\mathrm{greedy}}(\mathbf{x}_0)) < \mathcal{E}^{\theta,\mathrm{unif}}(\mathbf{x}_0)$（Proposition 3.1），意味着标准训练目标无法有效约束规划器下的生成质量。
2. **实践层面**：模型在训练时被迫在规划器从不访问的区域上分配容量，造成容量浪费和生成质量下降。

### 关键机制：规划器感知证据下界（P-ELBO）

PAPL 的理论基础是推导出**规划器感知 ELBO**（P-ELBO），将任意规划器纳入训练目标：

$$\log(p_\theta^{G_\phi}(\mathbf{x}_0)) \geq \mathcal{E}_1^{\theta,\phi}(\mathbf{x}_0) + \mathcal{E}_2^{\theta,\phi}(\mathbf{x}_0)$$

其中 $\mathcal{E}_1$ 是规划器加权的交叉熵项，$\mathcal{E}_2$ 是规划器与参考动力学之间的 KL 散度项。这一分解表明，训练时只需对更可能被规划器选中的位置赋予更高权重，即可实现训练与推理的对齐。

### 工程实现：一行代码的损失函数修改

PAPL 将上述理论转化为极其简洁的工程方案。最终训练损失为：

$$\mathcal{L}_{\mathrm{PAPL}}(\theta) = -\mathbb{E}_{\mathbf{x}_0,k,\mathbf{x}_k}\left[\sum_{i:x_k^i=\mathbf{m}}\frac{1}{L-k}(1 + \alpha w^i)\log\left(\mathrm{Cat}(x_0^i;D_\theta^i(\mathbf{x}_k))\right)\right]$$

其中权重 $w^i$ 由**软最大化规划器**（soft greedy planner）计算：

$$\mathrm{Cat}(j;G_\phi^\tau(\mathbf{z},\mathbf{x})) \propto \exp\left(\frac{1}{\tau}\log\mathrm{Cat}(z^j;D_\theta^j(\mathbf{x}))\right)$$

这一方案的关键设计选择包括：

| 设计槽位 | 标准 DLM | PAPL |
|---------|---------|------|
| 训练损失权重 | 均匀加权 $1/(L-k)$ | 规划器加权 $(1/(L-k))(1 + \alpha w^i)$ |
| 掩码序列采样 | 均匀掩码采样 | **保持不变**（不模拟完整规划器路径） |
| 规划器来源 | 无 | 去噪器自身置信度（自规划） |

这种设计带来了三个重要优势：

1. **无需额外推理开销**：训练时加入的规划器权重在推理时完全不需要，推理速度与标准 DLM 一致。
2. **实现极简**：仅需修改损失函数中的权重计算（一行代码），无需改变模型架构或采样流程。
3. **训练路径复用**：PAPL 仍使用均匀掩码方案采样 $x_k$，而非模拟规划器驱动的完整路径，避免了路径采样的计算开销和方差问题。

### 训练稳定性设计

纯 PAPL 损失（$\tau=1$）会导致训练不稳定（Figure 5），表现为损失大幅波动和验证收敛差。这是因为在训练初期，去噪器尚未形成有意义的置信度，规划器权重 $w^i$ 接近零，损失信号过弱；随着模型开始识别正确位置，权重骤增，导致损失剧烈波动。

为解决这一问题，PAPL 通过超参数 $\alpha$ 将规划器加权损失与标准均匀损失进行插值：权重因子 $(1 + \alpha w^i)$ 中的常数项 1 保留了基础均匀损失，$\alpha$ 控制规划器影响的强度。这种混合策略确保了训练初期有稳定的梯度信号，同时随着训练推进逐步引入规划器感知的偏好。



![[assets/figures/papers/paper_list_l44_https_openreview_net_forum_id_lAlI5FuIf7/figures/001_Figure_1.jpg]]
*Figure 1: Planner-Aware Path Learning (PAPL) resolves training–inference mismatch in DLMs. Standard uniform training for DLMs (left) applies a uniform loss across all masked positions, distributing capacity over regions that inference-time planners never traverse. PAPL (right) introduces planner-aware weights into the loss, aligning training with the planner’s preferred trajectories (outlined arrows) and eliminating training-inference mismatch*

PAPL 在标准掩码离散扩散语言模型（MDLM）的训练流程上引入了一个关键修改：将均匀加权的去掩码交叉熵损失替换为规划器感知的加权损失。整个训练管线保持简洁，仅需修改损失计算的一行代码。

### 管线模块

**数据与掩码采样** — 从数据分布中采样干净序列 $\mathbf{x}_0$，随机选择时间步 $k \sim \text{Unif}([0:L-1])$，然后在 $\mathbf{x}_0$ 上均匀掩码 $L-k$ 个位置，得到中间状态 $\mathbf{x}_k$。这一步与标准 MDLM 训练完全一致，PAPL 并不模拟规划器驱动的完整生成路径，而是复用均匀掩码方案，从而避免昂贵的路径采样开销。

**去噪器前向传播** — 将掩码序列 $\mathbf{x}_k$ 输入去噪器 $D_\theta$，得到对所有 $L$ 个位置的预测分布 $D_\theta(\mathbf{x}_k)$。该去噪器在 PAPL 中承担双重角色：既是生成模型的核心组件，也是自规划（self-planning）的置信度来源。

**规划器权重计算** — 利用去噪器自身的输出构建软最大化规划器（soft greedy planner）。对于每个被掩码的位置 $i$，计算其规划器权重 $w^i$：

$$\mathrm{Cat}(j; G_\phi^\tau(\mathbf{z}, \mathbf{x})) \propto \exp\left(\frac{1}{\tau} \log \mathrm{Cat}(z^j; D_\theta^j(\mathbf{x}))\right)$$

其中温度 $\tau$ 控制贪婪程度：$\tau \to 0$ 时退化为确定性贪婪选择（始终选置信度最高的位置），$\tau \to \infty$ 时恢复均匀分布。权重 $w^i$ 本质上是规划器选择位置 $i$ 的概率，反映了去噪器对该位置预测的置信度。

**加权损失计算** — 计算规划器加权的交叉熵损失。PAPL 的最终训练目标为：

$$\mathcal{L}_{\mathrm{PAPL}}(\theta) = -\mathbb{E}_{\mathbf{x}_0, k, \mathbf{x}_k}\left[\sum_{i: x_k^i = \mathbf{m}} \frac{1}{L-k}(1 + \alpha w^i) \log\left(\mathrm{Cat}(x_0^i; D_\theta^i(\mathbf{x}_k))\right)\right]$$

该损失由两部分构成：基础均匀权重 $\frac{1}{L-k}$ 保证了训练稳定性，规划器权重项 $\alpha w^i$ 则使模型对规划器更可能选择的去掩码位置赋予更高权重。超参数 $\alpha$ 控制规划器影响的强度——$\alpha=0$ 时完全退化为标准 MDLM 损失。

**参数更新** — 通过梯度下降更新去噪器参数 $\theta$。训练过程中，规划器权重 $w^i$ 的计算使用停止梯度（stop-gradient），即不通过 $w^i$ 回传梯度，仅将其作为损失权重使用。

### 输入输出流

- **输入**：干净序列 $\mathbf{x}_0$（来自训练数据）
- **中间状态**：随机掩码后的序列 $\mathbf{x}_k$，其中 $k$ 个位置被替换为掩码 token $\mathbf{m}$
- **模型输出**：对 $\mathbf{x}_k$ 中所有掩码位置的 token 预测分布
- **损失信号**：规划器加权的交叉熵，对置信度高的掩码位置施加更大惩罚

### 与标准 MDLM 训练的核心差异

| 组件 | 标准 MDLM | PAPL |
|------|-----------|------|
| 掩码采样 | 均匀掩码 | 均匀掩码（不变） |
| 损失权重 | $\frac{1}{L-k}$（均匀） | $\frac{1}{L-k}(1 + \alpha w^i)$（规划器加权） |
| 规划器参与 | 无 | 去噪器自身置信度作为自规划器 |
| 推理开销 | 无额外开销 | 无额外开销（训练时修改，推理不变） |

### 设计动机：训练-推理对齐

标准 MDLM 训练假设推理时均匀随机去掩码，但实际推理中使用的贪婪、置信度或 P2 等规划器会沿着特定路径生成。这一训练-推理动力学不匹配意味着标准 ELBO 无法有效约束规划器下的生成质量——理论上，贪婪祖先采样甚至可能违反标准 ELBO，即 $\log(p_\theta^{\text{greedy}}) < \text{标准 ELBO}$（Proposition 3.1）。

PAPL 通过推导规划器感知证据下界（P-ELBO），将任意规划器纳入训练目标。其核心洞见是：与其让模型在训练时均匀分配容量到推理中永远不会遍历的区域，不如让模型聚焦于规划器实际偏好的去掩码路径。权重项 $w^i$ 正是去噪器对“规划器会选这个位置”的置信度估计，从而实现了训练与推理动力学的直接对齐。



### 3.1 规划器感知的逆向动力学建模

标准扩散语言模型（DLM）在训练时假设均匀随机去掩码，而推理时实际使用贪婪、置信度等规划器选择去掩码位置。PAPL 的核心洞察在于：**将规划器的选择行为显式建模到逆向转移核中**，使训练目标与推理路径对齐。

设当前掩码序列为 $\mathbf{x}_k$（含 $L-k$ 个被掩码位置），去噪器 $D_\theta$ 对所有位置产生候选预测 $\mathbf{z} \sim D_\theta(\mathbf{x}_k)$，规划器 $G_\phi$ 根据 $\mathbf{z}$ 选择一个被掩码位置进行去掩码。PAPL 将这一过程分解为两步，并定义规划器感知的转移核：

$$q_{\theta,\phi}^i(y|\mathbf{x}_k) = \mathrm{Cat}(y; D_\theta^i(\mathbf{x}_k)) \cdot F_{\theta,\phi}(\mathbf{x}_k, y, i) \tag{4}$$

其中 $F_{\theta,\phi}(\mathbf{x}, y, i)$ 表示在去噪器预测 $\mathbf{z}$ 的条件下，规划器选中位置 $i$ 的边际期望：

$$F_{\theta,\phi}(\mathbf{x}, y, i) := \mathbb{E}_{\mathbf{z} \sim D_\theta(\mathbf{x})}\left[\mathrm{Cat}(i; G_\phi(\mathbf{z}^{-i,y}, \mathbf{x}_k))\right] \tag{5}$$

这里 $\mathbf{z}^{-i,y}$ 表示将去噪器采样结果 $\mathbf{z}$ 的第 $i$ 个坐标替换为 token $y$。式 (4) 的直觉是：**位置 $i$ 被去掩码为 $y$ 的概率，等于去噪器预测 $y$ 的概率乘以规划器选择该位置的期望概率**。

### 3.2 规划器感知证据下界（P-ELBO）

基于上述转移核，PAPL 推导出规划器感知的证据下界（Planner-aware ELBO, P-ELBO），将任意规划器纳入训练目标：

$$\log(p_\theta^{G_\phi}(\mathbf{x}_0)) \geq \mathcal{E}_1^{\theta,\phi}(\mathbf{x}_0) + \mathcal{E}_2^{\theta,\phi}(\mathbf{x}_0) + \mathcal{E}_3^{\theta,\phi}(\mathbf{x}_0) \tag{Proposition 3.2}$$

该下界由三项组成：

- **$\mathcal{E}_1$ — 规划器加权的交叉熵项**：对每个被掩码位置 $i$，交叉熵损失按规划器选中该位置的概率加权，即“规划器更可能选择的位置获得更高训练权重”。
- **$\mathcal{E}_2$ — 规划器与参考动力学的 KL 散度**：衡量有效规划器（使用去噪器预测）与理想规划器（使用真实 token）在选择行为上的差异，推动去噪器产生使规划器做出正确选择的置信度分布。
- **$\mathcal{E}_3$ — 初始掩码状态的熵项**：与模型参数无关的常数项。

**关键理论结果**：标准均匀去掩码训练的 ELBO 并不能保证贪婪规划器下的生成质量。具体地，**Proposition 3.1** 证明：对于不完美的去噪器，贪婪祖先采样可能违反标准 ELBO，即 $\log(p_\theta^{\text{greedy}}(\mathbf{x}_0)) < \mathcal{E}^{\theta,\text{unif}}(\mathbf{x}_0)$。这从理论上揭示了训练—推理不匹配的根源。

### 3.3 实用化近似与 PAPL 损失

直接优化完整的 P-ELBO 面临两个挑战：(1) 需要模拟规划器驱动的完整去掩码路径，计算开销大；(2) 纯加权损失训练不稳定（见 Figure 5）。PAPL 通过以下近似将 P-ELBO 转化为一行代码即可实现的实用损失函数：

1. **路径采样简化**：不再模拟规划器路径，而是复用标准 DLM 的均匀掩码方案采样 $\mathbf{x}_k$，仅调整损失权重。
2. **停止梯度**：计算规划器权重 $w^i$ 时对去噪器输出停止梯度，避免二阶效应。
3. **均匀损失混合**：将规划器加权损失与标准均匀损失通过超参数 $\alpha$ 插值，保证训练稳定性。

**软最大化规划器**：PAPL 使用温度参数 $\tau$ 控制规划器的贪婪程度：

$$\mathrm{Cat}(j; G_\phi^\tau(\mathbf{z}, \mathbf{x})) \propto \exp\left(\frac{1}{\tau}\log\mathrm{Cat}(z^j; D_\theta^j(\mathbf{x}))\right) \tag{15}$$

当 $\tau \to 0$ 时退化为确定性贪婪选择（选置信度最高的位置）；$\tau \to \infty$ 时恢复均匀分布。权重 $w^i$ 即为此软最大化分布在位置 $i$ 上的概率值。

**最终 PAPL 训练损失**：

$$\mathcal{L}_{\mathrm{PAPL}}(\theta) = -\mathbb{E}_{\mathbf{x}_0, k, \mathbf{x}_k}\left[\sum_{i: x_k^i=\mathbf{m}} \frac{1}{L-k}(1 + \alpha w^i) \log\left(\mathrm{Cat}(x_0^i; D_\theta^i(\mathbf{x}_k))\right)\right] \tag{7}$$

各符号含义：
- $\mathbf{x}_0$：从数据分布采样的干净序列
- $k \sim \mathrm{Unif}([0:L-1])$：随机采样的掩码步数
- $\mathbf{x}_k$：对 $\mathbf{x}_0$ 均匀掩码 $L-k$ 个位置得到的序列
- $w^i$：软最大化规划器对位置 $i$ 赋予的权重，$w^i \propto \exp(\tau^{-1}\log\mathrm{Cat}(z^i; D_\theta^i(\mathbf{x}_k)))$
- $\alpha$：控制规划器影响强度的超参数（$\alpha=0$ 退化为标准 DLM 损失）
- $\frac{1}{L-k}$：标准均匀权重因子

**实现要点**：式 (7) 与标准 DLM 损失的区别仅在于将均匀权重 $\frac{1}{L-k}$ 替换为 $\frac{1}{L-k}(1+\alpha w^i)$。去噪器对自身高置信度的位置赋予更高训练权重，从而将训练容量集中到推理时规划器实际会遍历的路径上。



## 实验与关键发现

### 核心瓶颈验证：训练-推理动力学失配

PAPL 的设计根植于一个可证明的失配现象：标准扩散语言模型（DLM）的训练证据下界（ELBO）在推理使用贪婪规划器时可能被违反。**Proposition 3.1** 严格证明了对于不完美的去噪器，贪婪祖先采样下的对数似然可以低于标准均匀 ELBO，即 $\log(p_\theta^{\text{greedy}}(\mathbf{x}_0)) < \mathcal{E}^{\theta,\text{unif}}(\mathbf{x}_0)$。这意味着，标准 ELBO 无法有效约束规划器下的生成质量——模型可能在训练损失上表现良好，但在实际推理路径上产生低质量样本。

PAPL 通过推导**规划器感知证据下界（P-ELBO）**直接解决了这一失配。P-ELBO 将规划器引导的反向动力学纳入训练目标，分解为两项：$\mathcal{E}_1$ 是规划器加权的交叉熵项，对更可能被规划器选中的去掩码位置赋予更高权重；$\mathcal{E}_2$ 是理想规划器（使用真实标签）与有效规划器（使用去噪器预测）之间的 KL 散度项。最终的 PAPL 训练损失将这一理论框架简化为一行的代码修改——在标准均匀掩码交叉熵损失中引入规划器权重 $w^i$，通过超参数 $\alpha$ 控制规划器影响强度：

$$\mathcal{L}_{\mathrm{PAPL}}(\theta)=-\mathbb{E}_{\mathbf{x}_0,k,\mathbf{x}_k}\left[\sum_{i:x_k^i=\mathbf{m}}\frac{1}{L-k}(1+\alpha w^i)\log\left(\mathrm{Cat}(x_0^i;D_\theta^i(\mathbf{x}_k))\right)\right]$$

其中 $w^i \propto \exp(\tau^{-1} \log \mathrm{Cat}(z^j; D_\theta^j(\mathbf{x})))$ 为软最大化规划器权重，温度 $\tau$ 控制贪婪程度。这种“自规划”机制无需额外推理开销，仅通过训练时的加权即可对齐训练与推理动力学。

### 主要结果

#### 蛋白质序列生成：可折叠性相对提升 40%

Table 1 展示了蛋白质序列生成的核心结果。在 150M 参数规模下，PAPL 将可折叠性（Foldability，定义为同时满足 pLDDT > 80、pTM > 0.7、pAE < 10 的序列比例）从 DLM-150M 基线的 **42.43%** 提升至 **59.40%**，相对提升约 **40%**。这一增益使得 150M 的 PAPL 模型在可折叠性上超越了未使用 PAPL 的更大规模模型（如 DPLM-650M 的 57.04%），同时保持了相当的序列多样性（Token Entropy 4.03 vs. DLM-150M 的 4.06）。在结构质量指标上，PAPL 同样取得一致改善：pLDDT 从 77.90 提升至 80.68，pTM 从 0.647 提升至 0.681。Figure 2 的 ESMFold 折叠可视化定性地展示了 PAPL 生成蛋白质具有合理的二级和三级结构。

![[assets/figures/papers/paper_list_l44_https_openreview_net_forum_id_lAlI5FuIf7/figures/003_Table_1.jpg]]
*Table 1: Protein sequence generation benchmark. We evaluate structure quality via pLDDT, pTM, and pAE, and diversity via token entropy and sequence uniqueness. Foldability is the percentage of sequences satisfying pLDDT > 80, pTM > 0.7, and pAE \< 10*

#### 无条件文本生成：MAUVE 最高 4 倍增益

Table 2 报告了无条件文本生成的结果。在采样步数 T=128 时，PAPL 取得了所有扩散方法中最高的 MAUVE 分数 **0.067**，相比标准 MDLM 的 0.011 实现了约 **6 倍**的提升，相比此前最优的扩散基线 ReMDM（0.034）提升近 2 倍。同时，PAPL 的生成困惑度（Gen PPL）降至 **24.33**，显著优于 MDLM+DFM 的 30.44 和 ReMDM 的 29.81。值得注意的是，PAPL 在仅 T=32 步采样时即取得 MAUVE 0.029，已经超过标准 MDLM 在 T=128 时的表现，表明训练-推理对齐带来了更高效的采样。

![[assets/figures/papers/paper_list_l44_https_openreview_net_forum_id_lAlI5FuIf7/figures/004_Table_2.jpg]]
*Table 2: Unconditional text generation. For each sampling step T , we report MAUVE (higher is better), generative perplexity (Gen PPL; lower is better), and entropy (higher is better). † indicates nucleus sampling. For each T , the best diffusion scores are bolded. Results. Table 2 reports unconditional text generation performance across sampling steps T $\in \{$ 3 2 , 6 4 , 1 2 8 $\}$ . Our method, PAPL, consistently and substantially improves diffusion-based generation. $\quad \operatorname { A t }$ T = 1 2 8 . , PAPL attains the strongest diffusion MAUVE (0.067) and lowest Gen PPL (24.3), outperforming ReMDM (0.057 MAUVE, 42.5 PPL) and MDLM+DFM (0.041 MAUVE, 37.9 PPL). entropy remains comparable across...

#### 代码生成：HumanEval pass@10 相对提升 23%

Table 4 展示了代码生成的核心指标。在 HumanEval 基准上，PAPL 将 pass@10 从 DLM 基线的 **31.1** 提升至 **38.4**，相对提升 **23%**；pass@1 从 18.5 提升至 20.8。在 HumanEval+、MBPP 和 MBPP+ 上同样观察到一致的增益。Table 3 的代码填充（infilling）任务中，PAPL 在 HumanEval-INFILL pass@1 上从 30.0 提升至 **32.5**，在 SantaCoder-FIM 精确匹配率上从 30.7 提升至 **32.9**。这些结果在 0.5B 参数规模的紧凑模型上取得，证明了 PAPL 在资源受限场景下的有效性。

![[assets/figures/papers/paper_list_l44_https_openreview_net_forum_id_lAlI5FuIf7/figures/006_Table_4.jpg]]
*Table 4: Code generation performance on HUMANEVAL, HUMANEVAL+, MBPP, and MBPP+. Large-scale models (≥7B) are shown as reference, while the main comparison is among compact sub-billion models. Results marked with † are adopted from prior work (Havasi et al., 2025)*

### 消融实验

#### 采样方法对比：P2-Self 全面占优

Table 5 比较了三种采样方法在文本生成上的表现。**P2-Self 采样**在所有步数预算下均优于 Greedy 和 Probability Margin 采样，尤其在快速采样（T=32）时优势最大——MAUVE 达到 0.013，而 Greedy 和 Probability Margin 分别仅为 0.003 和 0.001。随着采样步数增加，P2-Self 的优势持续扩大，在 T=128 时 MAUVE 达到 0.067，Gen PPL 降至 24.33。Table 6 在代码生成基准上进一步验证了 P2-Self 的优越性，在全部六个基准（HumanEval、HumanEval+、MBPP、MBPP+、HumanEval Infill、SantaCoder）上均取得最优或接近最优的 pass@1 分数。

#### 超参数敏感性：τ 与 α 的调控作用

Figure 4 揭示了两个关键超参数的影响机制。**温度 τ**：降低 τ（< 1）可提高蛋白质可折叠性，表明更强的贪婪偏好有助于聚焦高质量路径；但 τ 过低可能导致探索不足。**路径学习权重 α**：增大 α 可稳步提升可折叠性，直至 α=5 时达到峰值（约 67%），远超 DLM 基线（虚线，约 57%）。这一单调递增趋势表明规划器感知信号对训练有持续的正向贡献。

![[assets/figures/papers/paper_list_l44_https_openreview_net_forum_id_lAlI5FuIf7/figures/012_Figure_4.jpg]]
*Figure 4: Effect of τ and α on foldability. Lower τ (\< 1) improves performance. Increasing α steadily boosts foldability up to α = 5. The dashed line denotes the vanilla DLM baseline*

#### 训练稳定性与损失动态

Figure 5 暴露了纯 PAPL 损失（τ=1）的**关键失败模式**：训练损失出现大幅波动，验证收敛性显著差于混合损失。这解释了为何最终 PAPL 损失必须通过 $(1 + \alpha w^i)$ 的形式与标准均匀损失混合——纯加权损失使去噪器过早陷入高置信度区域，丧失探索能力。

Figure 6 进一步揭示了 PAPL 独特的**训练动态**：训练初期，PAPL 损失低于标准 MDM 损失，因为此时去噪器尚未形成有意义的置信度，规划器权重 $w_i$ 接近于零；随着模型开始以较高置信度识别正确位置，权重增大，PAPL 损失暂时上升；当去噪器充分收敛后，PAPL 损失下降并最终与标准 MDM 损失曲线趋同。这一“先低后增再降”的动态是自规划机制的内在特征，反映了去噪器置信度从无到有的演化过程。

#### 近似步骤验证

Table 7 消融了从理论 P-ELBO 到最终 PAPL 损失的系列近似步骤，包括使用均匀路径采样替代规划器路径、停止梯度传播、以及加入均匀损失混合。结果表明，这些近似基本保留了规划器感知的核心优势，近似误差可控，验证了 PAPL 作为理论框架的工程化实现的合理性。

### 公平性保障与评估一致性

所有 DLM 变体使用相同架构、相同训练数据以及相同推理规划器（P2-Self）进行比较。蛋白质评估统一使用 ESMFold 进行结构预测，可折叠性阈值（pLDDT > 80, pTM > 0.7, pAE < 10）在所有方法上保持一致。文本生成评估中，自回归参考模型使用 nucleus sampling（p=0.9）。代码生成实验遵循 Open-dLLM 框架，模型从 Qwen2.5-Coder 初始化以确保公平起点。

### 补充图表

![[assets/figures/papers/paper_list_l44_https_openreview_net_forum_id_lAlI5FuIf7/figures/010_Figure_3.jpg]]
*Figure 3: PAPL consistently improves over DLM across training, sampling steps, and temperature. (a) Faster convergence in training steps. (b) Higher performance across sampling steps. (c) More robust to temperature when training from scratch. (d) More robust to temperature when fine-tuning*



## 定位与知识库关联

### 核心瓶颈：训练与推理的动力学失配

标准扩散语言模型（DLM）的训练目标基于均匀去掩码假设：对序列中所有被掩码位置赋予均等的交叉熵权重，其证据下界（ELBO）形式为

$$\mathcal{E}^{\theta,\mathrm{unif}}(\mathbf{x}_0) = L\mathbb{E}_{k\sim\mathrm{Unif}([0:L-1])}\left[\mathbb{E}_{\mathbf{x}_k\sim\mathrm{Unif}(\mathcal{X}_{L-k}(\mathbf{x}_0))}\left[\sum_{i=1,x_k^i=\mathbf{m}}^L\frac{1}{L-k}\log\left(\mathrm{Cat}(x_0^i;D_\theta^i(\mathbf{x}_k))\right)\right]\right]$$

然而，推理时的去掩码过程必然由一个规划器（planner）引导——无论是简单的贪婪选择、置信度排序，还是更复杂的多步去噪策略（如 P2）。这一前向（训练）与反向（推理）动力学之间的根本性失配，构成了标准 DLM 的核心瓶颈。论文通过 Proposition 3.1 给出了严格证明：在去噪器不完美的情况下，贪婪祖先采样的对数似然可以严格低于标准 ELBO，即 $\log(p_\theta^{\mathrm{greedy}}(\mathbf{x}_0)) < \mathcal{E}^{\theta,\mathrm{unif}}(\mathbf{x}_0)$，揭示了标准训练目标无法有效约束规划器下的生成质量。

### 因果调节变量：规划器感知的损失加权

PAPL 的因果干预点简洁而深刻：在训练损失中引入基于规划器的权重，使模型对更可能被推理规划器选中的去掩码位置赋予更高的训练权重。这一干预直接对齐了训练与推理的动力学，其最终损失函数仅需对标准 DLM 损失做一行代码修改：

$$\mathcal{L}_{\mathrm{PAPL}}(\theta)=-\mathbb{E}_{\mathbf{x}_0,k,\mathbf{x}_k}\left[\sum_{i:x_k^i=\mathbf{m}}\frac{1}{L-k}(1+\alpha w^i)\log\left(\mathrm{Cat}(x_0^i;D_\theta^i(\mathbf{x}_k))\right)\right]$$

其中 $w^i \propto \exp(\tau^{-1}\log\mathrm{Cat}(z^j;D_\theta^j(\mathbf{x})))$ 为软最大化规划器权重，$\alpha$ 控制规划器影响强度，$\tau$ 调节贪婪程度。该方法的关键洞察在于：无需在训练时模拟完整的规划器路径（这将带来高昂的计算代价），而是复用标准 DLM 的均匀掩码采样方案，仅在损失权重层面注入规划器偏好。这一设计使 PAPL 在推理时零额外开销的前提下，实现了训练-推理对齐。

### 理论根基：规划器感知证据下界（P-ELBO）

PAPL 的理论基础是论文推导的规划器感知 ELBO（P-ELBO），其将任意规划器纳入训练目标。P-ELBO 可分解为两项：$\mathcal{E}_1^{\theta,\phi}$ 为规划器加权的交叉熵项，$\mathcal{E}_2^{\theta,\phi}$ 为规划器与参考动力学之间的 KL 散度项。从理论 P-ELBO 到最终 PAPL 损失的系列近似（包括使用均匀路径采样替代规划器路径、停止梯度传播、与均匀损失混合）被消融实验（Table 7）证明基本保留了规划器感知的优势，且近似误差可控。

### 方法谱系中的定位

**与标准 DLM 的关系**：PAPL 是对标准掩码扩散训练范式的直接补丁，而非替代。其保留了均匀掩码的前向过程，仅在损失函数中引入规划器感知权重。这一设计使 PAPL 可无缝集成到现有 DLM 训练流程中。

**与推理端规划器的关系**：PAPL 的独特之处在于将推理规划器的偏好反向传播到训练阶段，而非仅依赖推理时的搜索或调度改进。实验表明，PAPL 训练出的去噪器在多种规划器（Greedy、Probability Margin、P2-Self）下均表现更优，且对采样步数和温度变化更为鲁棒（Figure 3）。

**与自回归模型的对比**：在蛋白质生成领域，PAPL 训练的 DLM-150M 在可折叠性上达到 59.40%，显著优于基线 DLM（42.43%），并接近甚至超越部分大型自回归模型（如 **ProGen2-large** (Nijkamp et al., 2023) 和 **ESM3** (Hayes et al., 2025)）。在代码生成任务上，PAPL 使紧凑模型（<1B）的 HumanEval pass@10 从 31.1 提升至 38.4，缩小了与大型参考模型 **LLaDA-8B** (Havasi et al., 2025) 的差距。

**与其他扩散改进方法的关系**：相较于专注于推理端规划器设计的 **ReMDM** 和 **MDLM+DFM**，PAPL 从训练端根本性地解决了训练-推理失配问题。在无条件文本生成中，PAPL 在 T=128 时取得 MAUVE 0.067，远超 MDLM+DFM 的 0.011，实现了最高 4 倍的相对增益。

### 适用边界与局限

1. **训练稳定性约束**：纯 PAPL 损失（$\tau=1$，无均匀损失混合）训练极不稳定，损失大幅波动且验证收敛差（Figure 5）。必须通过 $\alpha$ 参数与标准均匀损失混合，以避免去噪器过早陷入高置信度区域。这限制了规划器信号的直接注入强度。

2. **规划器类型的理论覆盖**：当前推导主要针对只去掩码不重掩码的规划器。虽然理论上可扩展至重掩码规划器（如 P2），但高效训练该设定下的 PAPL 损失仍待探索。

3. **超参数的任务依赖性**：$\alpha$ 和 $\tau$ 需根据任务调整。论文给出了起步建议（$\tau=1$，$\alpha=1$），且实验显示降低 $\tau$（<1）可提高蛋白质可折叠性，增大 $\alpha$ 可稳步提升性能直至 $\alpha=5$（Figure 4），但对不同数据尺度的最优取值仍需额外搜索。

4. **深层组合推理的局限**：在复杂推理任务（如某些 HumanEval 题目）上，模型仍会出现逻辑错误。这说明单纯对齐训练与推理路径并未完全解决深层组合推理问题——PAPL 解决的是路径选择层面的失配，而非去噪器本身的表征能力瓶颈。

### 开放问题

1. **复杂规划器的训练效率**：如何推导并工程化适用于重掩码、多步去噪（如 P2）等更复杂规划器的 PAPL 损失，同时保持训练效率？当前通过复用均匀掩码采样规避了完整规划器路径模拟，但这一近似在重掩码场景下的保真度有待验证。

2. **与强化学习的结合**：能否将 PAPL 思想与强化学习或自博弈机制结合，让去噪器在规划路径上自我改进？PAPL 当前的“自规划”机制（利用去噪器自身置信度作为规划器）已初步体现了自指涉学习的雏形，但尚未形成闭环的自我改进循环。

3. **通用规划器搜索**：如何设计通用规划器搜索方法，自动为给定任务和数据学习最优规划器，而非依赖人工设计的软最大化？当前的软贪婪规划器虽有效，但其形式受限于温度参数化的指数族分布。

4. **大规模模型的稳定性**：在更大规模（如 7B+）的扩散语言模型上，PAPL 能否持续提供增益？如何选择混合权重 $\alpha$ 以保持预训练稳定性？当前实验主要在紧凑模型（150M-0.5B）上验证，大规模扩展的工程挑战尚待探索。



## 原文 PDF

![[paperPDFs/ICLR_2026/Planner_Aware_Path_Learning_in_Diffusion_Language_Models_Training.pdf]]
