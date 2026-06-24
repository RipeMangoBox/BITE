---
title: "Neighbor GRPO: Contrastive ODE Policy Optimization Aligns Flow Models"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/Neighbor_GRPO_Contrastive_ODE_Policy_Optimization_Aligns_Flow_Models.pdf
project_link: null
code_link: null
aliases:
- NG
- NGCOPOAFM
tags:
- CVPR_2026
- topic/other_unclear
- topic/other_unclear/general
core_operator: 通过将 SDE 采样重新解释为基于距离的对比学习，发现优化目标等价于优势加权 MSE，从而揭示可以绕过 SDE、直接在 ODE 邻域内用距离目标进行优化。
primary_logic: SDE 基 GRPO 的优化动态实质上是一种对比学习过程；Neighbor GRPO 通过扰动初始噪声构造一组 ODE 候选轨迹，设计了一个基于 softmax 距离的替代跳跃策略，在策略梯度框架下实现了无需 SDE 的全 ODE 训练，保留了确定性采样和高效高阶求解器的全部优势。
claims:
- SDE 基 GRPO 可等价转化为优势加权的 MSE 损失，揭示其对比学习本质。
- Neighbor GRPO 通过初始噪声扰动和 softmax 距离代理策略实现全 ODE 训练。
- 对称锚采样将前向/反向计算量降低至原来的 1/12（FLUX 训练中 G=12）。
- 在多项域外评估指标上，Neighbor GRPO 以更低的训练成本显著超越 SDE 基线。
---

# Neighbor GRPO: Contrastive ODE Policy Optimization Aligns Flow Models

> [!tip] 核心洞察
> SDE 基 GRPO 的优化动态实质上是一种对比学习过程；Neighbor GRPO 通过扰动初始噪声构造一组 ODE 候选轨迹，设计了一个基于 softmax 距离的替代跳跃策略，在策略梯度框架下实现了无需 SDE 的全 ODE 训练，保留了确定性采样和高效高阶求解器的全部优势。

| 字段 | 内容 |
|------|------|
| 中文题名 | Neighbor GRPO：基于对比式 ODE 策略优化的流模型对齐方法 |
| 英文题名 | Neighbor GRPO: Contrastive ODE Policy Optimization Aligns Flow Models |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2511.16955) |
| Topic | #topic/other_unclear #topic/other_unclear/general |
| Method | Neighbor GRPO |
| Dataset | HPDv2 测试集 |

> [!tip] 效果简介
> - HPDv2 测试集 (多奖励训练, 25-step DDIM) 上，CLIP Score 0.385 vs 0.364 (DanceGRPO) / 0.382 (MixGRPO) (+0.021 / +0.003)；UnifiedReward 3.262 vs 3.156 (DanceGRPO) / 3.257 (MixGRPO) (+0.106 / +0.005)。
> - HPDv2 测试集 (多奖励训练, 8-step DPM++) 上，HPSv2.1 0.366 vs 0.343 (MixGRPO-Flash) (+0.023)。
> - 训练效率 (NFE_θ) 上，有效函数评估次数 1.33 vs 14.00 (DanceGRPO/MixGRPO) (-12.67)。

## 概述

**Neighbor GRPO** 是一种面向流匹配（Flow Matching）扩散模型的强化学习对齐方法，其核心目标是解决现有基于随机微分方程（SDE）的 GRPO 方法在信用分配效率低、与高阶 ODE 求解器不兼容以及训练成本高昂等方面的瓶颈。通过将 SDE 基 GRPO 的优化动态重新解释为一种对比学习过程，该方法揭示了一个关键洞察：GRPO 的优化目标在数学上等价于优势加权的均方误差损失（MSE），从而可以绕过 SDE 采样，直接在确定性 ODE 的邻域内进行策略优化。

Neighbor GRPO 的方法定位是**全 ODE 训练的强化学习对齐框架**。它不再依赖 SDE 在每个时间步注入噪声进行随机探索，而是通过对 ODE 的初始噪声施加缩放扰动来构造一组候选轨迹（邻域），并设计了一个基于 softmax 距离的替代跳跃策略（surrogate leaping policy）来模拟随机探索。这一设计使得模型在训练时能够利用组内所有候选样本的联合力场进行对比式优化，同时保留了流匹配模型确定性采样和高效高阶求解器（如 DPM++）的全部优势。

在训练效率方面，该方法引入了**对称锚采样**（symmetric anchor sampling），将策略更新阶段的有效函数评估次数（NFE_θ）从基线方法的 14.00 降至 1.33，在 FLUX 训练中可将前向/反向计算量减少至原来的 1/12。此外，针对标准 GRPO 中 L2 归一化可能导致的“奖励攻击”问题，Neighbor GRPO 提出了**组级拟范数重加权**（group-wise quasi-norm reweighting），通过使用 Lp（p<2）拟范数自适应地抑制奖励平坦组的更新幅度。

主要实验结果验证了该方法的有效性：在多奖励训练设置下，Neighbor GRPO 在所有域外评估指标上均显著超越 SDE 基线方法（DanceGRPO、MixGRPO），同时保持了域内评估的竞争力。例如，在 HPDv2 测试集的 CLIP Score 上达到 0.385（DanceGRPO 为 0.364），UnifiedReward 达到 3.262（DanceGRPO 为 3.156），且每次训练迭代时间从约 238 秒降至约 45 秒。该方法仅需约 4 小时的训练即可在文本到图像生成任务上取得优异表现，展示了其在训练成本、收敛速度和生成质量三个维度上的综合优势。

## 背景与动机

### 流匹配模型的对齐需求与现有瓶颈

流匹配（Flow Matching）模型在文本到图像生成领域展现出卓越的性能，其核心优势在于使用确定性常微分方程（ODE）进行采样，天然兼容高阶求解器（如 DPM++），能够以极少的函数评估次数（NFE）生成高质量图像。然而，预训练的流匹配模型往往需要进一步对齐人类偏好，以提升生成结果的美学质量和语义一致性。

近年来，研究者将 GRPO（Group Relative Policy Optimization）引入扩散模型和流匹配模型的偏好对齐训练中。现有方法，如 **DanceGRPO** 和 **MixGRPO**，通过在采样过程中注入随机微分方程（SDE）噪声来构造探索轨迹，实现策略优化。尽管这些 SDE 基方法在域内奖励上取得了显著提升，但它们存在两个根本性缺陷：

1. **信用分配效率低下**：SDE 在每个时间步引入独立噪声，导致轨迹间的因果关联模糊，优势信号难以准确归因于具体的生成决策。
2. **与高阶求解器不兼容**：SDE 采样的随机性破坏了确定性 ODE 的数学结构，使得 DPM++ 等高阶求解器无法使用，被迫退回到低阶采样方案，牺牲了流匹配模型的核心效率优势。

这一矛盾构成了本工作的核心瓶颈：**如何在保留全 ODE 训练和高阶求解器兼容性的前提下，实现高效的 GRPO 风格偏好对齐？**

### 从对比学习视角重新审视 GRPO

本文的关键洞察在于对 SDE 基 GRPO 优化动态的重新解释。通过理论分析，作者证明：**最大化 SDE 基 GRPO 目标等价于最小化一个优势加权的均方误差（MSE）损失**（Section 3.2）。这一等价性揭示了 GRPO 的本质是一种对比学习过程——在每个时间步，模型被推向高奖励候选样本，同时远离低奖励候选样本（如图 Figure 1 所示）。

这一发现带来了方法论上的突破：既然优化目标可以表达为纯距离度量，那么**随机探索并非必须依赖 SDE 噪声**。只要能够构造一组多样化的候选轨迹，并在确定性 ODE 框架内定义合理的距离度量，就可以绕过 SDE，实现全 ODE 训练。这正是 Neighbor GRPO 的核心动机——通过扰动初始噪声构造 ODE 邻域，用基于 softmax 距离的替代跳跃策略取代 SDE 的高斯策略，从而在策略梯度框架下保留确定性采样和高效高阶求解器的全部优势。

## 核心创新

Neighbor GRPO 的核心创新在于**将 SDE 基 GRPO 的信用分配问题转化为 ODE 邻域内的对比学习**，从而在保留确定性采样全部优势的前提下，实现了更高效、更稳定的流模型对齐训练。具体而言，该方法包含四个关键的技术改进：

### 从 SDE 探索到 ODE 邻域构造

现有 SDE 基 GRPO 方法（如 DanceGRPO、MixGRPO）在每个时间步添加 SDE 噪声进行随机探索，这带来了两个根本性问题：一是 SDE 随机性与流匹配模型的确定性 ODE 采样本质相冲突，与高阶求解器不兼容；二是信用分配效率低下——SDE 噪声在每一步引入的随机扰动使得奖励信号难以准确归因到模型参数。

Neighbor GRPO 从根本上改变了探索机制：**不再依赖 SDE 在每个时间步注入噪声，而是通过扰动 ODE 的初始噪声构造一组候选轨迹**。具体地，从共享基噪声 $\epsilon^*$ 出发，通过缩放扰动生成 $G$ 个初始条件：

$$\epsilon^{(i)} = \sqrt{1-\sigma^2} \epsilon^* + \sigma \delta^{(i)}, \quad i=1,\dots,G$$

这 $G$ 个初始条件随后通过确定性 ODE 求解器（如 DPM++）独立采样，形成一组完整的候选轨迹。由于所有轨迹共享相同的确定性动力学，它们天然构成一个有意义的“邻域”，为后续的对比学习提供了结构化的候选空间。

### 从高斯策略到 softmax 距离替代策略

SDE 基 GRPO 的策略定义为基于 SDE 更新的高斯分布，需要计算对数似然和 KL 散度。Neighbor GRPO 的理论洞察在于：**SDE 基 GRPO 的优化目标等价于优势加权的 MSE 损失**，这揭示了其本质上是一种对比学习过程——将锚点样本推向高奖励候选，同时远离低奖励候选。

基于这一洞察，Neighbor GRPO 定义了一个**仅用于训练的替代跳跃策略**，在 $G$ 个候选项上根据与锚点的负平方距离构建 softmax 分布：

$$\pi_\theta(x_t^{(i)} | \{s_t\}) = \frac{\exp(-\|x_t^{(i)} - x_t^{(\theta)}\|_2^2)}{\sum_{k=1}^G \exp(-\|x_t^{(k)} - x_t^{(\theta)}\|_2^2)}$$

该策略在训练时虚拟地让采样轨迹“跳跃”到邻近候选，提供策略比率和梯度信号，但在推理时完全丢弃，保留了 ODE 的确定性采样特性。这一设计使得整个训练流程可以完全在 ODE 框架内进行，无需任何 SDE 步骤。

### 对称锚采样：训练效率的质变

标准 GRPO 需要对组内每个样本独立执行前向/反向计算，每迭代 $G \times K$ 次计算（$G$ 为组大小，$K$ 为更新的时间步数）。Neighbor GRPO 提出的**对称锚采样**策略，每迭代仅采样 $B$ 个锚点（$B < G$），将训练计算量降至 $B \times K$。在 FLUX 训练的典型配置（$G=12$）下，该方法将策略更新阶段的前向/反向计算量降低至原来的 **1/12**，训练速度从约 238 秒/迭代降至 45 秒/迭代，实现了近 5 倍的加速。

### 组级拟范数重加权：缓解奖励攻击

标准 GRPO 使用 L2 归一化计算组优势函数，当组内奖励分布平坦时，归一化后的优势值仍然较大，可能导致模型过度优化奖励模型中的伪影（如生成平均人脸）。Neighbor GRPO 引入**组级拟范数重加权**，使用 $L_p$ 拟范数（$p < 2$）替换标准 L2 归一化：

$$A_i' = \frac{A_i}{(\sum_{k=1}^G |A_k|^p)^{1/p}}, \quad p \in (0,2]$$

当 $p < 2$ 时，拟范数自适应地降低奖励平坦组的优势幅度，从而抑制对无信息梯度的过度响应。消融实验表明，$p=0.8$ 在多项域外评估指标上取得最佳平衡，有效缓解了奖励攻击现象。

### 创新点的协同效应

上述四个创新点并非孤立存在，而是形成了紧密的协同关系：ODE 邻域构造为替代跳跃策略提供了结构化的候选空间；替代跳跃策略使全 ODE 训练成为可能；对称锚采样在 ODE 框架下大幅降低训练成本；拟范数重加权则在不牺牲 ODE 优势的前提下增强了训练的鲁棒性。这种协同使得 Neighbor GRPO 在训练成本仅为 SDE 基线约 1/5 的条件下，在所有域外评估指标上均取得显著领先。

## 整体框架

Neighbor GRPO 的整体训练流程围绕一个核心设计原则展开：**完全摒弃 SDE 随机性，在确定性 ODE 的邻域内构造基于距离的对比学习目标**。整个框架由五个紧密协作的模块构成，形成了一条从初始噪声扰动到策略梯度更新的端到端训练管线。

### 1. 管线总览

训练迭代的宏观流程如下：

1. **噪声扰动模块**：从一份共享的基噪声 $\epsilon^*$ 出发，通过缩放和扰动生成 $G$ 个不同的初始噪声 $\{\epsilon^{(i)}\}_{i=1}^G$，构成一个 ODE 邻域。
2. **RolloutSolver**：使用高阶确定性 ODE 求解器（如 DPM++）对 $G$ 个初始条件分别进行完整轨迹采样，得到 $G$ 条候选轨迹。
3. **奖励评估与优势计算**：对每条轨迹的最终生成结果计算奖励信号，进行组内归一化得到优势值 $A_i$。此阶段应用**拟范数重加权**模块，以自适应抑制奖励平坦组的更新强度。
4. **锚采样器**：从 $G$ 个候选中对称采样 $B$ 个锚点（$B < G$），用于后续高效的梯度估计。
5. **策略更新**：在锚点条件下，使用**跳跃策略（替代策略）** 计算策略比率，构建 GRPO 目标函数。此阶段使用 **TrainSolver**（一步 DDIM）从 $x_{t+\Delta t}$ 计算 $x_t$，以计算替代策略所需的距离度量。仅对锚点样本执行前向/反向传播，大幅降低计算量。

### 2. 模块关系与数据流

下图描述了各模块之间的输入输出关系：

```
基噪声 ε* ──► [噪声扰动模块] ──► {ε^(1), ..., ε^(G)}
                                      │
                                      ▼
                         [RolloutSolver (DPM++)]
                                      │
                                      ▼
                          {轨迹^(1), ..., 轨迹^(G)}
                                      │
                                      ▼
                         奖励评估 + 组内归一化
                                      │
                          ┌───────────┴───────────┐
                          ▼                       ▼
                    [拟范数重加权]          [锚采样器 (B个)]
                          │                       │
                          ▼                       ▼
                     {A_i'}              {锚点条件目标}
                          │                       │
                          └───────────┬───────────┘
                                      ▼
                          [跳跃策略 (替代策略)]
                                      │
                                      ▼
                          [TrainSolver (一步DDIM)]
                                      │
                                      ▼
                              GRPO 目标函数
                                      │
                                      ▼
                              策略梯度更新
```

**关键设计决策**：RolloutSolver 与 TrainSolver 的分离是 Neighbor GRPO 实现全 ODE 训练的核心。数据收集阶段使用高精度 DPM++ 求解器以保证轨迹质量；策略更新阶段使用一步 DDIM 以降低计算开销，同时保持 ODE 的确定性特性。这种分离使得模型在训练和推理阶段均无需引入 SDE 噪声。

### 3. 与 SDE 基方法的本质区别

传统 SDE 基 GRPO（如 **DanceGRPO** 和 **MixGRPO**）在每个时间步向采样过程注入随机噪声以进行探索，其优化动态可等价转化为优势加权的 MSE 损失（参见第 3.2 节的理论推导）。这一等价性揭示了 SDE 基 GRPO 的对比学习本质——模型被推向高奖励候选、推离低奖励候选。然而，SDE 的引入带来了两个根本性问题：（a）与高阶 ODE 求解器不兼容，牺牲了流匹配模型的确定性采样优势；（b）信用分配效率低下，每个样本独立进行前向/反向计算，训练成本高昂。

Neighbor GRPO 保留了这一对比学习的核心机制，但将探索从“时间步级别的 SDE 噪声注入”迁移到“初始噪声级别的 ODE 邻域构造”。这一迁移使得整个训练管线可以完全运行在确定性 ODE 模式下，从而：

- 兼容 DPM++ 等高阶求解器，提升生成质量；
- 通过锚采样将有效函数评估次数 $\mathrm{NFE}_\theta = \frac{B}{G} \cdot K$ 从基线方法的 14.00 降至 1.33（FLUX 训练中 $G=12$ 时计算量降低至原来的 1/12）；
- 保留了流匹配模型在推理时的确定性采样优势。

### 4. 训练与推理的不对称设计

Neighbor GRPO 在训练阶段引入了两个仅在训练时使用的虚拟机制：

- **跳跃策略（替代策略）**：基于 softmax 距离的随机策略 $\pi_\theta(x_t^{(i)} | \{s_t\}) = \frac{\exp(-\|x_t^{(i)} - x_t^{(\theta)}\|_2^2)}{\sum_{k=1}^G \exp(-\|x_t^{(k)} - x_t^{(\theta)}\|_2^2)}$，用于计算策略比率和梯度。该策略定义了采样轨迹在每一步“虚拟跳跃”到邻近候选的概率分布，但推理时完全不使用。
- **拟范数重加权**：使用 $L_p$（$p<2$）拟范数替换标准 GRPO 的 $L_2$ 归一化，自适应降低奖励平坦组的优势幅度，缓解奖励攻击。

推理时，模型仅使用标准的确定性 ODE 求解器进行采样，无需任何额外机制，保持了流匹配模型的原始推理效率。

### 补充图表

![[assets/figures/papers/paper_list_l2717_https_arxiv_org_abs_2511_16955/figures/001_Figure_1.jpg]]
*Figure 1: GRPO approaches for flow models optimize the sample xt at each timestep t. We revisit it from the perspective of contrastive learning, pushing anchor samples to high-reward candidates and vice versa. Different from SDE-based GRPO approaches [17, 40] that conduct sample-wise exploration and optimization, our Neighbor GRPO optimizes the policy at the anchor in a joint force field defined by all candidates in a group. This approach allows full-ODE training, leading to better training efficiency and sample quality*

## 核心模块与公式推导

### 3.1 从 SDE 探索到 ODE 邻域构造：对比学习视角的揭示

现有基于 SDE 的 GRPO 方法（如 **DanceGRPO**）在每个时间步注入随机噪声进行探索，其优化目标可等价转化为一个优势加权的 MSE 损失：

$$\max_{\theta} \mathcal{J}_{\text{SDE-GRPO}}(\theta) \iff \min_{\theta} \sum_i A_i \cdot \|x_{t-\Delta t}^{(i)} - x_{t-\Delta t}^{(\theta)}\|_2^2$$

这一等价性揭示了 SDE 基 GRPO 的优化动态本质上是一种**对比学习过程**：高优势样本充当正例吸引锚点，低优势样本充当负例排斥锚点。然而，SDE 的逐步随机扰动不仅导致信用分配效率低下，还与高阶确定性 ODE 求解器（如 DPM++）不兼容，牺牲了流匹配模型的核心采样优势。

Neighbor GRPO 的核心洞察在于：**既然优化目标可表达为纯粹的距离度量，那么完全可以绕过 SDE，直接在 ODE 邻域内用距离目标进行优化。** 方法通过扰动初始噪声构造一组确定性 ODE 候选轨迹，再定义一个基于 softmax 距离的替代跳跃策略，在策略梯度框架下实现全 ODE 训练。

### 3.2 噪声扰动模块：构建 ODE 邻域

给定一个共享的基噪声 $\epsilon^*$，通过缩放扰动生成 $G$ 个不同的初始条件：

$$\epsilon^{(i)} = \sqrt{1-\sigma^2} \epsilon^* + \sigma \delta^{(i)}, \quad i=1,\dots,G \tag{7}$$

其中 $\delta^{(i)} \sim \mathcal{N}(0, I)$ 为独立噪声，$\sigma \in [0,1]$ 控制扰动强度。这 $G$ 个初始条件随后通过确定性 ODE 求解器（如 DPM++）独立采样，生成 $G$ 条完整轨迹，构成一个**邻域候选集**。与 SDE 方法在每个时间步注入噪声不同，Neighbor GRPO 的随机性仅作用于初始条件，后续采样完全由确定性 ODE 驱动，从而保留了高阶求解器的全部优势。

### 3.3 替代跳跃策略：训练时的虚拟随机策略

在训练阶段，Neighbor GRPO 为当前采样轨迹定义一个**替代跳跃策略**（surrogate leaping policy），使其在每一步 $t$ 能够“虚拟跳跃”到邻域内的其他候选样本。该策略基于候选样本与当前锚点 $x_t^{(\theta)}$ 的负平方距离定义 softmax 分布：

$$\pi_\theta(x_t^{(i)} \mid \{s_t\}) = \frac{\exp(-\|x_t^{(i)} - x_t^{(\theta)}\|_2^2)}{\sum_{k=1}^G \exp(-\|x_t^{(k)} - x_t^{(\theta)}\|_2^2)} \tag{8}$$

该策略仅在训练时用于计算策略比率和梯度，推理阶段不引入任何随机性，模型仍使用标准确定性 ODE 采样。这种设计使得 Neighbor GRPO 在保持推理确定性的同时，获得了策略梯度方法带来的对齐能力。

### 3.4 对称锚采样：计算效率的关键设计

传统 GRPO 需要为每个候选样本独立计算前向/反向传播，计算复杂度为 $O(G \cdot K)$（$G$ 为组大小，$K$ 为更新的时间步数）。Neighbor GRPO 提出**对称锚采样**策略：每次迭代仅从 $G$ 个候选中采样 $B$ 个锚点（$B < G$），以每个锚点为中心计算裁剪后的 GRPO 目标：

$$\sum_{i=1}^G \min\left( A_i \rho_t^{(i|k)}, A_i \lceil \rho_t^{(i|k)} \rfloor \right) \tag{9}$$

其中 $\rho_t^{(i|k)}$ 是以第 $k$ 个样本为锚点的策略比率。有效函数评估次数降至：

$$\mathrm{NFE}_\theta = \frac{B}{G} \cdot K$$

在 FLUX 训练的典型配置（$G=12$）下，该方法可将策略更新阶段的前向/反向计算量降低至原来的 $1/12$。

### 3.5 组级拟范数重加权：缓解奖励平坦

标准 GRPO 使用 L2 归一化计算组优势 $A_i = \frac{r_i - \text{mean}(\{r_k\})}{\text{std}(\{r_k\})}$。当组内奖励分布平坦（所有候选获得相似奖励）时，归一化后的优势幅值仍可能较大，导致模型沿无意义方向更新，引发**奖励攻击**（reward hacking）——如图 4 所示，标准 GRPO 生成的人脸出现平均化伪影。

Neighbor GRPO 引入**组级拟范数重加权**，使用 $L_p$ 拟范数（$p < 2$）替代 L2 归一化：

$$A_i' = \frac{A_i}{(\sum_{k=1}^G |A_k|^p)^{1/p}}, \quad p \in (0,2] \tag{11}$$

当 $p < 2$ 时，拟范数对组内优势的离散度更敏感：奖励平坦的组将获得更小的归一化因子，从而自适应地降低该组的更新强度。消融实验表明 $p=0.8$ 在多项域外评估指标上取得最佳平衡。

### 3.6 求解器分离策略：Rollout 与训练的解耦

Neighbor GRPO 采用**求解器分离**策略以兼顾采样质量与训练效率：
- **RolloutSolver**：使用高阶确定性 ODE 求解器（如 DPM++）进行数据收集，生成高质量的候选轨迹；
- **TrainSolver**：在策略更新阶段，使用一步 DDIM 从 $x_{t+\Delta t}$ 计算 $x_t$，以高效计算替代策略和目标函数。

这种分离设计使得训练过程无需承担高阶求解器的计算开销，同时保证了 rollout 轨迹的质量。

### 补充图表

![[assets/figures/papers/paper_list_l2717_https_arxiv_org_abs_2511_16955/figures/002_Figure_3.jpg]]
*Figure 3: Surrogate leaping policy. The ongoing sampling trajectory virtually leaps to another, following the policy distribution*

![[assets/figures/papers/paper_list_l2717_https_arxiv_org_abs_2511_16955/figures/003_Figure_2.jpg]]
*Figure 2: Different from SDE-based GRPO approaches, which explore the sample space with noise perturbation defined by SDE, we directly construct a group of similar initial noises, and conduct deterministic ODE sampling*

## 实验与分析

### 主要结果：多奖励训练下的综合性能

在 HPDv2 数据集上使用 FLUX.1-dev 基座模型进行多奖励对齐训练（300 次迭代），Neighbor GRPO 在多项域外评估指标上以更低的训练成本显著超越 SDE 基线方法。Table 1 给出了 25-step DDIM 采样下的完整对比：Neighbor GRPO 在 CLIP Score 上达到 **0.385**，较 DanceGRPO 的 0.364 提升 +0.021；在 UnifiedReward 上达到 **3.262**，较 DanceGRPO 的 3.156 提升 +0.106；在 LAION Aesthetic Score 上达到 **6.669**，同样为所有方法中最高。值得注意的是，这些优势集中在域外评估上，而在域内指标（HPSv2.1、Pick Score、ImageReward）上 Neighbor GRPO 与基线保持持平，表明该方法有效避免了 SDE 基方法常见的域内过拟合问题。

![[assets/figures/papers/paper_list_l2717_https_arxiv_org_abs_2511_16955/figures/006_Table_1.jpg]]
*Table 1: Comparison of human preference scores. Underline: in-domain preference. †: official checkpoints*

当使用高阶确定性求解器 DPM++ 进行 8-step 采样时，Neighbor GRPO 的优势进一步扩大。Table 1 显示，在 HPSv2.1 上 Neighbor GRPO 达到 **0.366**，而 MixGRPO-Flash 仅为 0.343（+0.023）。这验证了核心设计理念：全 ODE 训练天然兼容高阶求解器，而 SDE 基方法因引入随机性噪声，与确定性高阶求解器存在根本性不兼容。

### 训练效率对比

Table 3 从计算量角度揭示了 Neighbor GRPO 的效率优势。在策略更新阶段，Neighbor GRPO 的有效函数评估次数（NFE_θ）仅为 **1.33**，而 DanceGRPO 和 MixGRPO 均为 14.00，计算量降低约 **10.5 倍**。这一差异直接转化为训练速度：Neighbor GRPO 每次迭代仅需 **45.08 秒**，DanceGRPO 和 MixGRPO 分别需要 237.86 秒和 237.71 秒，加速约 **5.3 倍**。

![[assets/figures/papers/paper_list_l2717_https_arxiv_org_abs_2511_16955/figures/009_Table_3.jpg]]
*Table 3: Training cost of different methods*

效率提升的核心机制来自对称锚采样策略。在标准 GRPO 中，每个样本需要独立进行前向/反向计算，计算复杂度为 $O(G \times K)$，其中 $G$ 为组大小，$K$ 为更新的时间步数。Neighbor GRPO 通过从 $G$ 个候选中对称采样 $B$ 个锚点（$B < G$），将计算复杂度降至 $O(B \times K)$。对于常用的 FLUX 训练配置（$G=12$），该方法将策略更新时的前向/反向计算量降低至原来的 **1/12**（Section 3.4.1）。有效 NFE 的计算公式为：

$$\mathrm{NFE}_\theta = \frac{B}{G} \cdot K$$

### 收敛速度分析

Figure 5 的训练曲线展示了各方法在 HPSv2.1 上的收敛动态。Neighbor GRPO 展现出显著更快的收敛速度：仅需约 **50 次迭代**即可使 HPSv2.1 分数超过 0.35，而 DanceGRPO 在 300 次迭代结束时仍未达到该水平。这一快速收敛可归因于两个因素：其一，全 ODE 训练避免了 SDE 噪声引入的信用分配模糊性，使梯度信号更加精确；其二，对比学习视角下的距离优化目标（Eq. 8）在 ODE 邻域内提供了更密集的优化力场，如 Figure 1 所示，锚点样本受到组内所有候选样本的联合力场驱动，而非 SDE 方法中每个样本独立优化。

![[assets/figures/papers/paper_list_l2717_https_arxiv_org_abs_2511_16955/figures/005_Figure_5.jpg]]
*Figure 5: Training curves towards HPSv2.1*

### 消融实验

#### 扰动强度 σ

Table 4 系统评估了初始噪声扰动强度 σ 对性能的影响。在 {0.1, 0.2, 0.3, 0.5, 0.7} 范围内，**σ = 0.3** 在所有指标上取得最佳平衡：HPSv2.1 达 0.375，CLIP 达 0.363，UnifiedReward 达 3.141，Aesthetic Score 达 6.639。过小的 σ 导致候选轨迹多样性不足，限制对比学习的效果；过大的 σ 则使候选轨迹偏离 ODE 邻域，破坏距离目标的有效性。这一结果验证了 Eq. (7) 中扰动机制设计的合理性：

![[assets/figures/papers/paper_list_l2717_https_arxiv_org_abs_2511_16955/figures/012_Table_4.jpg]]
*Table 4: Performance with various perturbation strength*

$$\epsilon^{(i)} = \sqrt{1-\sigma^2} \epsilon^* + \sigma \delta^{(i)}$$

其中 $\sqrt{1-\sigma^2}$ 的缩放因子保证了扰动后噪声的期望范数保持不变。

#### 锚点数量 B

Table 5 展示了锚点采样数量 B 的消融结果。在 {1, 2, 4, 6} 的取值范围内，**B = 4** 在性能与训练成本之间实现了良好平衡：HPSv2.1 达 0.379，CLIP 达 0.368，UnifiedReward 达 3.132，Aesthetic Score 达 6.503。继续增大 B 至 6 并未带来一致的性能提升，表明 4 个锚点已能提供足够准确的梯度估计。这一发现直接支持了对称锚采样策略的实用价值：以远小于组大小 G 的锚点数即可有效估计策略梯度。

![[assets/figures/papers/paper_list_l2717_https_arxiv_org_abs_2511_16955/figures/013_Table_5.jpg]]
*Table 5: Performance of various number of sampled anchors*

#### 拟范数参数 p

Table 6 评估了组级拟范数重加权中参数 p 的影响。标准 GRPO 使用 $p=2$（L2 归一化），但实验发现 $p=2$ 会导致明显的奖励攻击（reward hacking）现象——模型倾向于生成高奖励但质量退化的"平均人脸"伪影（Figure 4a）。将 p 降至 **0.8** 有效缓解了这一问题，在域外评估上取得最佳分数：HPSv2.1 达 0.372，CLIP 达 0.371，UnifiedReward 达 3.166，Aesthetic Score 达 6.626。$p=1$ 的性能介于两者之间。

![[assets/figures/papers/paper_list_l2717_https_arxiv_org_abs_2511_16955/figures/014_Table_6.jpg]]
*Table 6: Performance with various p normalization*

拟范数重加权的机制如下：当一组候选样本的奖励值差异很小（即奖励信号"平坦"）时，标准 L2 归一化仍会赋予这些样本较大的优势值，导致模型向噪声方向更新。Lp 拟范数（$p < 2$）通过自适应降低这类组的归一化因子，抑制其贡献：

$$A_i' = \frac{A_i}{(\sum_{k=1}^G |A_k|^p)^{1/p}}, \quad p \in (0,2]$$

这一设计在数学上等价于对奖励平坦组施加隐式的信任度惩罚，从而将优化资源集中于奖励信号更具信息量的样本组。

### 定性结果

Figure 6 提供了各方法的生成图像可视化对比。在相同提示词下，DanceGRPO 的生成结果偶尔出现色彩失真和构图失衡，MixGRPO 有所改善但仍存在细节模糊问题。Neighbor GRPO 的生成结果在色彩保真度、细节清晰度和构图合理性上均表现最优，与定量指标的趋势一致。Figure 8 展示了训练 300 次迭代后的 rollout 组示例（σ = 0.3），可见候选轨迹在保持语义一致性的同时展现出合理的多样性，验证了 ODE 邻域构造策略的有效性。

![[assets/figures/papers/paper_list_l2717_https_arxiv_org_abs_2511_16955/figures/010_Figure_6.jpg]]
*Figure 6: Visualization of different approaches*

![[assets/figures/papers/paper_list_l2717_https_arxiv_org_abs_2511_16955/figures/011_Figure_8.jpg]]
*Figure 8: Rollout groups after 300-iteration training*

### 失败模式与局限

尽管 Neighbor GRPO 在多项指标上表现优异，但仍存在若干值得关注的局限。首先，该方法目前仅在 FLUX 架构上进行了验证，其在其他流匹配架构（如 DiT）上的泛化性尚待确认。其次，拟范数重加权虽能缓解奖励攻击，但在极端训练规模下是否持续有效仍需进一步验证。此外，替代跳跃策略中隐含的温度参数（文中未显式引入）可能为性能调优提供额外自由度，其作用机制值得探索。最后，该方法的当前验证集中在文本到图像生成任务，向视频生成或三维生成任务的推广是自然的后续方向。

### 补充图表

![[assets/figures/papers/paper_list_l2717_https_arxiv_org_abs_2511_16955/figures/004_Figure_4.jpg]]
*Figure 4: Effect of quasi-norm reweighting*

## 方法谱系与知识库定位

### 核心瓶颈：SDE 基 GRPO 的信用分配与采样效率困境

现有基于 SDE 的 GRPO 方法（如 **DanceGRPO** 和 **MixGRPO**）在流匹配模型对齐中面临两个根本性瓶颈。第一，**信用分配效率低下**：SDE 在每个时间步引入随机噪声进行探索，导致采样轨迹的方差被扩散过程的随机性主导，模型难以将奖励信号准确地归因到确定性速度场 $v_\theta$ 的更新上。第二，**与高阶求解器不兼容**：SDE 采样破坏了流匹配模型的确定性 ODE 结构，使得 DPM++ 等高阶求解器无法直接使用，迫使训练和推理阶段采用不同的采样策略，牺牲了流匹配模型的核心优势。

本文通过理论分析揭示了这一困境的本质：**SDE 基 GRPO 的优化动态等价于优势加权的 MSE 损失**（Section 3.2），本质上是一种基于距离的对比学习过程。这一发现直接引出了核心洞察——可以绕过 SDE，直接在 ODE 邻域内用距离目标进行优化。

### 方法定位：从 SDE 探索到 ODE 邻域对比学习

Neighbor GRPO 在方法谱系中的定位可以通过以下四个关键设计槽位的变更来刻画，这些变更共同构成了从“SDE 随机探索”到“ODE 邻域对比学习”的范式转换：

| 设计槽位 | SDE 基线方法 | Neighbor GRPO | 变更逻辑 |
|---------|-------------|---------------|---------|
| **探索机制** | 在每个时间步添加 SDE 噪声进行随机探索 | 通过扰动 ODE 的初始噪声构造一组候选轨迹（邻域） | 将探索从“逐步随机”变为“初始条件多样化”，保留 ODE 确定性 |
| **策略定义** | 基于 SDE 更新的高斯策略，计算对数似然 | 基于 softmax 距离的替代跳跃策略（仅训练用） | 将策略从“生成式随机策略”变为“对比式虚拟策略” |
| **训练计算量** | 每个样本独立前向/反向，每迭代 G×K 次计算 | 对称锚采样，每迭代 B×K (B<G) 次计算，可减少至 1/12 | 利用组内样本的对称性共享梯度计算 |
| **优势归一化** | 标准 GRPO 的 L2 归一化 (p=2) | 组级拟范数重加权 (Lp, p<2) | 自适应抑制奖励平坦组的贡献，缓解奖励坍塌 |

### 与基线方法的关系

**DanceGRPO**（纯 SDE 基 GRPO）在每个去噪时间步引入 SDE 噪声进行随机探索，其策略定义为高斯分布，需要计算对数似然。该方法的信用分配效率受限于 SDE 的随机性，且无法使用高阶 ODE 求解器。Neighbor GRPO 通过将探索前移至初始噪声扰动，完全消除了对 SDE 的依赖，在训练效率和生成质量上均显著超越 DanceGRPO（Table 1：CLIP Score +0.021，UnifiedReward +0.106）。

**MixGRPO**（SDE-ODE 混合 GRPO）试图在 SDE 探索和 ODE 采样之间取得折中，但仍保留了 SDE 组件，因此同样面临与高阶求解器不兼容的问题。Neighbor GRPO 的全 ODE 训练范式在 8-step DPM++ 推理下将 HPSv2.1 从 0.343 提升至 0.366（Table 1）。

**BranchGRPO**（分支树 GRPO）通过构建分支树结构进行探索，但计算开销较大。Neighbor GRPO 的对称锚采样策略将有效函数评估次数 NFE_θ 从 14.00 降至 1.33，每次迭代时间从约 238 秒降至约 45 秒（Table 3），实现了数量级的效率提升。

### 适用边界与局限

Neighbor GRPO 的适用边界由以下关键设计参数定义：

1. **扰动强度 σ**：控制 ODE 邻域的范围。消融实验（Table 4）表明 σ = 0.3 是最优选择，在 HPSv2.1、CLIP Score、UnifiedReward 和 Aesthetic Score 上取得最佳平衡。过小的 σ 导致候选轨迹缺乏多样性，过大的 σ 则破坏邻域结构。

2. **锚点数量 B**：控制对称锚采样的粒度。B = 4 在性能与训练成本之间实现良好平衡（Table 5），但最优值可能依赖于具体的模型架构和训练规模。

3. **拟范数参数 p**：控制优势重加权的强度。p = 0.8 有效缓解了奖励攻击（Table 6，Figure 4），但该参数的最优值可能随奖励模型和训练数据的特性而变化。

当前工作的主要局限在于：所有实验均基于 FLUX.1-dev 架构和 HPDv2 数据集，该方法在其他流匹配架构（如 DiT）和更大规模训练场景下的泛化性尚未验证。此外，替代跳跃策略的温度参数在文中被忽略，其显式引入可能进一步提升性能。

### 开放问题

1. **架构泛化性**：该方法在除 FLUX 之外的其他流匹配架构（如 DiT、Stable Diffusion 3）上的表现如何？ODE 邻域构造策略是否需要针对不同架构进行调整？

2. **规模扩展性**：进一步扩展训练规模时，拟范数重加权是否能持续有效抑制奖励坍塌？是否需要引入额外的正则化机制？

3. **策略温度参数**：替代跳跃策略中显式引入温度参数是否会进一步提升性能？温度参数的自适应调整策略值得探索。

4. **跨模态扩展**：如何将该方法推广到视频生成或三维生成任务？这些任务中的 ODE 邻域构造和奖励建模面临额外的挑战。

5. **与 RLHF 方法的关系**：Neighbor GRPO 的对比学习视角是否可以为扩散模型的 RLHF 方法（如 DDPO、DPOK）提供新的理论理解和改进方向？这一连接值得进一步探索。

## 原文 PDF

![[paperPDFs/CVPR_2026/Neighbor_GRPO_Contrastive_ODE_Policy_Optimization_Aligns_Flow_Models.pdf]]
