---
title: "Slow-Fast Policy Optimization: Reposition-Before-Update for LLM Reasoning"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/Slow_Fast_Policy_Optimization_Reposition_Before_Update_for_LLM_Reasoning.pdf
openreview_forum_id: xBlHiHdXap
aliases:
- SSFPO
- SFPORBULR
tags:
- ICLR_2026
- topic/reinforcement_learning_planning_agents
- topic/reinforcement_learning_planning_agents/deep_rl
core_operator: "重定位步的插值系数α和内更新步数K，二者共同控制离策略漂移程度与梯度方向稳定性；自适应α调度在接近收敛时关闭快轨迹以平衡探索与利用。"
primary_logic: "将一次性更新拆解为“快速多步内更新→重定位回插→慢速校正”三阶段，在保留目标函数和rollout流程不变的前提下，构建了一个曲率感知的低通滤波器与隐式信赖域机制，稳定了梯度方向并显著提高了采样与计算效率。"
claims:
- "SFPO在六项数学推理基准上平均最高超出GRPO 2.80分（DS-distilled-Qwen-1.5B），所有模型和基准均有一致提升。"
- "SFPO只需GRPO的1/4.93 rollout数即可达到相同最佳精度，端到端训练时间减少最高4.19倍。"
- "消融实验证实，去除Stage II插值重定位会导致大K时训练崩溃，而保留Stage II则始终稳定，说明重定位是防止离策略过拟合的关键。"
- "SFPO作为高层优化插件，可无缝集成到DAPO等GRPO变体上，并持续带来额外提升。"
---

# Slow-Fast Policy Optimization: Reposition-Before-Update for LLM Reasoning

> [!tip] 核心洞察
> 将一次性更新拆解为“快速多步内更新→重定位回插→慢速校正”三阶段，在保留目标函数和rollout流程不变的前提下，构建了一个曲率感知的低通滤波器与隐式信赖域机制，稳定了梯度方向并显著提高了采样与计算效率。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 慢-快策略优化：面向大语言模型推理的“先重定位后更新”方法 |
| 英文题名 | Slow-Fast Policy Optimization: Reposition-Before-Update for LLM Reasoning |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=xBlHiHdXap); [Project](https://slow-fast-po.github.io/) |
| Topic | #topic/reinforcement_learning_planning_agents #topic/reinforcement_learning_planning_agents/deep_rl |
| Method | SFPO (Slow-Fast Policy Optimization) |
| Dataset | Math Reasoning (6 benchmarks avg), AIME25 |

> [!tip] 效果简介
> - Math Reasoning (6 benchmarks avg) 上，平均Pass@1 为 40.19，对比 38.35，变化 +1.84。
> - Math Reasoning (6 benchmarks avg) 上，平均Pass@1 为 50.53，对比 47.73，变化 +2.80。
> - AIME25 上，Pass@1 为 30.83，对比 23.33，变化 +7.50 (最大提升)。

## 概述

### 问题瓶颈

基于强化学习的大语言模型推理训练中，主流在线策略梯度方法（如**GRPO**，Shao et al., 2024）面临一个核心矛盾：训练早期rollout质量低下，导致梯度估计方差大、更新方向不稳定；而每批次仅执行一次梯度更新（one-shot update），数据利用率低下，采样效率难以提升。这两个因素相互耦合——低质量数据带来高噪声梯度，单步更新又无法有效平滑噪声，使训练过程在收敛速度和稳定性之间陷入两难。

### 核心方法：SFPO

**SFPO（Slow-Fast Policy Optimization）** 提出了一种“先重定位后更新”的三阶段迭代范式，将传统的一次性更新拆解为：

1. **快速轨迹（Stage I）**：在同一批次rollout上执行 $K$ 次连续梯度更新，累积稳定的梯度方向；
2. **重定位（Stage II）**：通过插值系数 $\alpha$ 将快速轨迹终点拉回起始点附近，形成隐式信赖域，控制离策略漂移；
3. **慢速校正（Stage III）**：在插值点上执行一次额外的梯度修正，完成整步迭代。

该方法保持目标函数和rollout流程完全不变，作为高层优化插件可无缝集成到GRPO及其变体（如**DAPO**，Yu et al., 2025a）之上，无需修改底层策略梯度实现。

### 核心结论

- **性能提升**：在六项数学推理基准上，SFPO平均最高超出GRPO **2.80分**（DS-distilled-Qwen-1.5B），所有模型规模和基准均有一致提升；AIME25单基准最大提升达**7.50分**。
- **效率飞跃**：达到GRPO最佳精度仅需其 **1/4.93的rollout数**，端到端训练时间最高加速**4.19倍**。
- **机制验证**：消融实验证实，重定位插值是防止大 $K$ 时训练崩溃的关键；自适应 $\alpha$ 调度在收敛附近关闭快速轨迹，保障训练稳定性。
- **通用性**：SFPO可叠加于DAPO之上并持续带来额外提升，在编程任务（LiveCodeBench）上同样有效，展现出跨任务和跨底层算法的鲁棒性。

## 背景与动机

### 大语言模型推理能力的强化学习范式

将大语言模型（LLM）的推理能力从“模仿”推向“探索”，是在线策略强化学习（On-Policy RL）在近期取得突破的核心驱动力。与监督微调（SFT）不同，RL使模型能够在试错中自我进化——通过从当前策略采样rollout、计算奖励信号、再沿策略梯度方向更新参数，模型可以逐步习得长链推理、自我验证与回溯等复杂行为。GRPO（Shao et al., 2024）作为这一范式下的代表性算法，通过组内奖励归一化替代传统的价值函数估计，大幅降低了训练开销，成为当前LLM推理RL的主流选择。

### GRPO的核心瓶颈：高方差梯度与低效采样

然而，GRPO存在一个被广泛忽视的深层瓶颈：**训练早期的低质量rollout会引入高方差梯度，而每批次仅执行单步更新，未能充分利用已采样的数据**。具体而言：

- **梯度方向不稳定**：在训练初期，策略尚未习得有效推理模式，采样得到的rollout质量参差不齐。基于这些低质量样本估计的策略梯度方向噪声极大，单步更新难以积累稳定的优化信号，导致训练震荡甚至发散。
- **采样效率低下**：GRPO每生成一批rollout后仅做一次梯度更新便丢弃数据，忽略了同一批次数据在相邻参数点上仍可提供有效梯度信息的特性。这导致要达到理想精度需要海量rollout，端到端训练时间高昂。

从优化视角看，GRPO本质上是一种“一次性更新”（one-shot update）策略：每步从当前策略点出发，沿噪声梯度方向迈出一步，随即在新的策略点上重新采样。这种机制缺乏对梯度方向的平滑与校正能力，也缺乏对参数更新幅度的显式约束——模型可能在单步内漂移过远，使新策略与采样策略之间产生显著分布偏移（off-policy drift），进一步恶化后续更新的质量。

### 核心动机：将一次性更新拆解为“快-重定位-慢”三阶段

本文的核心洞察在于：**在不改变目标函数和rollout生成流程的前提下，通过重构更新过程本身，可以同时解决梯度方向不稳定与采样效率低下两个问题**。具体思路是将GRPO的一次性更新拆解为三个协同阶段：

1. **快速多步内更新（Fast Trajectory）**：在同一批次rollout上连续执行K次梯度下降，累积稳定的梯度方向，充分利用已采样数据的信息。
2. **重定位回插（Reposition）**：将快速轨迹的终点按比例α插值回起始点，显式控制离策略漂移程度，形成隐式信赖域约束。
3. **慢速校正（Slow Correction）**：在插值后的点上执行一次额外的梯度修正，确保最终更新方向兼顾探索与稳定。

这一“先重定位后更新”（Reposition-Before-Update）的设计，本质上构建了一个**曲率感知的低通滤波器**：快速轨迹平滑了单步梯度的高频噪声，重定位步约束了参数更新的最大半径，慢速校正则保留了必要的探索能力。三者协同作用，在不增加额外模型组件或改变损失函数的前提下，显著提升了在线策略RL的稳定性与采样效率。

### 与现有改进路线的差异

现有针对GRPO的改进主要沿两条路线展开：一是修改奖励设计或优势估计（如DAPO通过动态采样缓解零优势问题；Yu et al., 2025a），二是引入更复杂的KL正则或信赖域约束。SFPO与这些路线**正交**：它不改变目标函数的形式，而是在更高层的优化流程上进行重构——将单步更新替换为“快-重定位-慢”三阶段更新。这使得SFPO可以**作为即插即用的插件**，无缝集成到GRPO、DAPO等现有策略梯度框架之上，持续带来额外提升。

## 核心创新

SFPO 的核心创新在于将标准在线策略RL中“每批次单次梯度更新”的范式，重构为**快-重定位-慢三阶段解耦更新**，在不改变目标函数与rollout流程的前提下，构建了曲率感知的低通滤波器与隐式信赖域机制。

### 更新流程重构：从单步更新到三阶段解耦

标准GRPO（Shao et al., 2024）采用一次性更新规则 $\theta^{s+1} = \theta^{s} - \eta \nabla_{\theta} \mathcal{L}(\theta^{s})$，每批rollout仅执行一次梯度下降。SFPO将这一过程拆解为三个协同阶段：

- **Stage I（快速轨迹）**：在同一批次rollout上执行 $K$ 次连续梯度更新 $\theta^{s,k+1} = \theta^{s,k} - \eta \nabla_{\theta} \mathcal{L}(\theta^{s,k})$，累积稳定的梯度方向。这一设计直接针对GRPO早期因低质量rollout带来的高方差梯度问题，通过多次内更新平滑噪声方向。
- **Stage II（重定位）**：将快速轨迹终点按比例 $\alpha$ 插值回起始点 $\widetilde{\theta}^{s,K} = \theta^{s,0} + \alpha (\theta^{s,K} - \theta^{s,0})$，形成对离策略漂移的显式约束。这是SFPO最关键的创新——GRPO仅有clip/KL正则作为间接约束，而SFPO通过插值系数 $\alpha$ 直接控制参数距起始点的距离，构成隐式信赖域。
- **Stage III（慢速校正）**：在重定位后的点 $\widetilde{\theta}^{s,K}$ 上执行一次额外梯度修正 $\theta^{s+1} = \widetilde{\theta}^{s,K} - \eta \nabla_{\theta} \mathcal{L}(\widetilde{\theta}^{s,K})$，完成整步迭代。

三阶段可统一为单一更新规则（Formula 12）：
$$\theta^{s+1} = \theta^{s,0} - \eta \left[ \alpha \sum_{k=0}^{K-1} \nabla_{\theta} \mathcal{L}(\theta^{s,k}) + \nabla_{\theta} \mathcal{L}(\widetilde{\theta}^{s,K}) \right]$$

### 离策略漂移控制：从间接正则到显式信赖域

GRPO依赖clip范围和KL散度正则来间接约束更新幅度，缺乏对离策略漂移的独立控制机制。SFPO通过重定位步的插值系数 $\alpha \in [0,1]$ 直接约束参数位移量，等效于在 $\theta^{s,0}$ 附近求解线性化近端子问题（Section 3.2）。消融实验（Figure 9）证实了这一设计的不可替代性：当 $K=7$ 且移除Stage II插值时，训练崩溃；而保留插值则始终稳定。与KL惩罚方案的对比（Figure 11）进一步表明，插值方案在 $K=3$ 和 $K=7$ 下均大幅优于KL惩罚版本，且 $K=7$ 时KL版本同样崩溃。

### 自适应α调度：基于策略熵的在线触发

SFPO引入了基于策略熵滑动窗口的自适应α调度机制（Section 3.4）：计算当前策略熵 $H_s$ 相对于滑动窗口均值 $\mu_s$ 和标准差 $\sigma_s$ 的z-score $Z_s = (H_s - \mu_s)/\sigma_s$，当 $|Z_s| \geq \tau$ 时设置 $\alpha = 0$，回退到纯在线更新。这一设计在训练接近收敛时自动关闭快速轨迹，平衡探索与利用。消融实验（Figure 6）表明，移除熵控制导致训练约100步后精度明显下降，验证了自适应关闭快轨迹对稳定收敛的关键作用。

### 插件式兼容性

SFPO作为高层优化插件，保持目标函数和rollout流程不变，可无缝集成到GRPO变体上。实验证实，在DAPO（Yu et al., 2025a）之上叠加SFPO仍能带来一致的额外提升（Figure 12, Table 3），表明其独立于底层GRPO的具体实现。此外，SFPO不增加GPU显存开销——由于不需存储重优化器状态，仅需多保存一份模型权重副本，实测显存消耗与GRPO相当（Figure 8）。

## 整体框架

![[assets/figures/papers/paper_list_l33_https_openreview_net_forum_id_xBlHiHdXap/figures/001_Figure_1.jpg]]
*Figure 1: Pipeline of SFPO at iteration s. Starting from the current policy $\pi _ { \theta ^ { s , 0 } }$ , we first generate rollouts for training. Stage I (Fast Trajectory): apply K successive gradient updates on the same batch to obtain $\theta ^ { s , \widetilde { K } }$ . Stage II (Reposition): interpolate between $\theta ^ { s , K }$ and the starting point $\theta ^ { s , 0 }$ to form $\widetilde { \theta } ^ { s , K }$ , controlling off-policy drift. Stage III (Slow Correction): perform one additional update on $\widetilde { \theta } ^ { s , K }$ , yielding $\pi _ { \theta ^ { s + 1 , 0 } }$ for the next iteration

SFPO（Slow-Fast Policy Optimization）将标准在线策略RL中的一次性参数更新重构为**快–重定位–慢**三阶段协调管道，在不改变目标函数与rollout生成流程的前提下，显著提升梯度方向稳定性与采样效率。图1给出了单次迭代的完整数据流。

**输入与初始化。** 在第 $s$ 轮迭代开始时，当前策略参数记为 $\theta^{s,0}$。首先从该策略采样一批rollout，用于后续所有阶段的梯度计算——这与GRPO等标准方法一致，SFPO不引入额外采样开销。

**Stage I：快速轨迹（Fast Trajectory）。** 在同一批次rollout上连续执行 $K$ 次梯度更新：
$$\theta^{s,k+1} = \theta^{s,k} - \eta \nabla_{\theta} \mathcal{L}(\theta^{s,k}), \quad k=0,\ldots,K-1$$
得到快速轨迹终点 $\theta^{s,K}$。这一步的动机在于：GRPO训练早期因低质量rollout引入高方差梯度，单步更新难以捕捉稳定的下降方向；多步内更新相当于对梯度方向做累积平均，构成一个**曲率感知的低通滤波器**，有效压制噪声。

**Stage II：重定位（Reposition）。** 将快速轨迹终点按插值系数 $\alpha \in [0,1]$ 拉回起始点：
$$\widetilde{\theta}^{s,K} = \theta^{s,0} + \alpha(\theta^{s,K} - \theta^{s,0})$$
该操作等价于在 $\theta^{s,0}$ 附近求解一个线性化近端子问题，形成**隐式信赖域**：$\alpha$ 越小，允许的参数偏移越小，离策略漂移控制越严格。这是SFPO区别于纯多步更新（易因漂移崩溃）的核心机制。

**Stage III：慢速校正（Slow Correction）。** 在重定位点 $\widetilde{\theta}^{s,K}$ 上执行一次额外的梯度修正：
$$\theta^{s+1} = \widetilde{\theta}^{s,K} - \eta \nabla_{\theta} \mathcal{L}(\widetilde{\theta}^{s,K})$$
得到下一轮迭代的起始参数 $\theta^{s+1,0}$。这一步将重定位后的参数重新拉回损失下降方向，弥补插值可能引入的方向偏差。

**$\alpha$ 自适应调度。** 为平衡探索与利用，SFPO维护一个策略熵的滑动窗口（窗口大小 $\omega$），计算当前步的z-score：
$$Z_s = \frac{H_s - \mu_s}{\sigma_s}$$
当 $|Z_s| \geq \tau$ 时，判定策略已接近收敛，将 $\alpha$ 置零，关闭快速轨迹，回退到纯在线单步更新。这一机制在训练后期自动抑制不必要的离策略探索，防止精度回退。

**统一更新规则。** 三阶段可整合为单一参数更新公式：
$$\theta^{s+1} = \theta^{s,0} - \eta \left[ \alpha \sum_{k=0}^{K-1} \nabla_{\theta} \mathcal{L}(\theta^{s,k}) + \nabla_{\theta} \mathcal{L}(\widetilde{\theta}^{s,K}) \right]$$
这表明SFPO可视为对标准梯度下降的一个**结构化修正项**：快速轨迹累积方向、重定位控制步长、慢速校正精调终点。整个管道作为即插即用的高层优化插件，可无缝集成到GRPO、DAPO等现有策略梯度管线中（见Figure 12、Table 3），且实测GPU显存开销与GRPO相当（Figure 8），因为SFPO仅需额外保存一份模型权重副本，无需存储重优化器状态。

## 核心模块与公式推导

### 问题背景：GRPO 的单步更新瓶颈

SFPO 建立在 GRPO（Shao et al., 2024）的基础之上。GRPO 的训练目标为：

$$
\mathcal{I}_{GRPO}(\theta) = \mathbb{E}_{q, \{o_i\} \sim \pi_{\theta_{old}}} \left[ \frac{1}{G} \sum_{i=1}^G \frac{1}{|o_i|} \sum_{t=1}^{|o_i|} \min(r_{i,t}(\theta) \widehat{A}_{i,t}, clip(r_{i,t}(\theta), 1-\epsilon, 1+\epsilon) \widehat{A}_{i,t}) - \beta D_{KL}[\pi_\theta || \pi_{ref}] \right]
$$

其中组内标准化优势为 $\widehat{A}_i = \frac{r_i - mean(\{r_i\}_{i=1}^G)}{std(\{r_i\}_{i=1}^G)}$，重要性比率 $r_{i,t}(\theta) = \frac{\pi_\theta(o_{i,t} | q, o_{i,<t})}{\pi_{\theta_{old}}(o_{i,t} | q, o_{i,<t})}$。

GRPO 的核心瓶颈在于：每批次仅执行单次梯度更新（one-shot update），训练早期低质量 rollout 带来高方差梯度，且未能充分利用数据，导致更新不稳定、采样效率低下。

### SFPO 三阶段管道

SFPO 将每个训练迭代拆解为三个协调阶段（Figure 1, Algorithm 1），在保留目标函数和 rollout 流程不变的前提下，构建曲率感知的低通滤波器与隐式信赖域机制。

#### Stage I：快速轨迹（Fast Trajectory）

在同一批次 rollout 上执行 $K$ 次连续梯度更新，累积稳定的梯度方向：

$$
\theta^{s,k+1} = \theta^{s,k} - \eta \nabla_{\theta} \mathcal{L}(\theta^{s,k}), \quad k = 0, \ldots, K-1
$$

$K$ 步后的累积位移为 $\theta^{s,K} - \theta^{s,0} = -\eta \sum_{k=0}^{K-1} \nabla_{\theta} \mathcal{L}(\theta^{s,k})$。多步内更新通过重用同一批次数据，在参数空间形成一条快速轨迹，稳定了梯度方向估计。

#### Stage II：重定位（Reposition）

将快速轨迹终点按系数 $\alpha \in [0,1]$ 插值回起始点，控制离策略漂移：

$$
\widetilde{\theta}^{s,K} = \theta^{s,0} + \alpha (\theta^{s,K} - \theta^{s,0})
$$

该插值等价于在 $\theta^{s,0}$ 附近求解一个线性化的近端子问题，形成隐式信赖域约束。$\alpha$ 越小，参数距起始点越近，离策略程度越低。

#### Stage III：慢速校正（Slow Correction）

在重定位后的点 $\widetilde{\theta}^{s,K}$ 上执行一次额外的梯度修正，得到下一迭代的起始参数：

$$
\theta^{s+1} = \widetilde{\theta}^{s,K} - \eta \nabla_{\theta} \mathcal{L}(\widetilde{\theta}^{s,K})
$$

慢速校正步在受控的离策略点上提供一次精细调整，弥补插值可能带来的信息损失。

### 统一更新规则

将三阶段整合，SFPO 的统一参数更新公式为：

$$
\theta^{s+1} = \theta^{s,0} - \eta \left[ \alpha \sum_{k=0}^{K-1} \nabla_{\theta} \mathcal{L}(\theta^{s,k}) + \nabla_{\theta} \mathcal{L}(\widetilde{\theta}^{s,K}) \right]
$$

该公式揭示了 SFPO 的本质：快速轨迹的累积梯度被 $\alpha$ 缩放后，与慢速校正梯度叠加，共同构成最终的更新方向。$\alpha$ 与 $K$ 是两个核心控制旋钮——$\alpha$ 控制离策略漂移程度，$K$ 决定内更新的累积步数。

### 熵触发的自适应 $\alpha$ 调度

为防止训练后期快速轨迹引入不必要的离策略风险，SFPO 引入基于策略熵的在线调度机制。维护策略熵 $H_s$ 的滑动窗口（窗口大小 $\omega$），计算 z-score：

$$
Z_s = \frac{H_s - \mu_s}{\sigma_s}
$$

当 $|Z_s| \geq \tau$ 时，策略熵发生显著波动，表明模型已接近收敛或分布发生变化，此时将 $\alpha$ 置零，关闭快速轨迹，回退到纯在线单步更新。这一机制在接近收敛时自动平衡探索与利用，消融实验证实移除该控制会导致约 100 步后精度明显下降（Figure 6）。

## 实验与分析

### 瓶颈与核心机制回顾

GRPO在LLM推理训练中面临双重瓶颈：其一，训练早期低质量rollout导致梯度估计方差极高，单步更新方向噪声大；其二，每批次仅执行一次梯度更新，数据利用效率低下，大量采样信息被浪费。SFPO通过将单次更新拆解为“快速多步内更新→重定位回插→慢速校正”三阶段，在保留目标函数和rollout流程不变的前提下，构建了一个曲率感知的低通滤波器与隐式信赖域机制。其核心调控旋钮为插值系数α和内更新步数K：α直接约束参数距起始点的离策略漂移程度，K控制梯度方向的累积稳定性；二者耦合——小K时α在宽范围内均稳定，大K时需较小α以防止过拟合旧策略。

### 主实验结果

**Table 1**汇总了六项数学推理基准上的Pass@1性能。SFPO在所有模型规模和所有基准上均一致优于GRPO基线：


![[assets/figures/papers/paper_list_l33_https_openreview_net_forum_id_xBlHiHdXap/figures/002_Table_1.jpg]]
*Table 1: Performance on math reasoning benchmarks with DAPO and Math training dataset*

- **Qwen2.5-Math-1.5B**：平均分从GRPO的38.35提升至SFPO的40.19（+1.84）。
- **DS-distilled-Qwen-1.5B**：平均分从47.73提升至50.53（+2.80），为最大平均提升；其中AIME25单项从23.33跃升至30.83（+7.50），为所有配置中最大单项增益。
- **DS-distilled-Qwen-7B**：平均分从60.47提升至63.04（+2.57），证明方法在更大规模模型上同样有效。

在更大规模训练集Skywork-or1上（**Table 2**），SFPO在AIME24/25上持续优于GRPO，例如DS-Qwen-1.5B的AIME25从25.83提升至27.50（+1.67），验证了方法的跨数据集鲁棒性。


![[assets/figures/papers/paper_list_l33_https_openreview_net_forum_id_xBlHiHdXap/figures/003_Table_2.jpg]]
*Table 2: Performance on AIME24/25 with Skywork-or1 training dataset*

### 训练动态与效率分析

**Figure 2**展示的训练过程中验证精度曲线表明，SFPO的优势贯穿整个训练周期，而非仅在收敛点附近。**Figure 3**进一步揭示了训练行为差异：SFPO的回复长度增长更平缓，策略熵下降更稳定，奖励分数提升更平滑，说明三阶段结构有效抑制了训练早期的剧烈波动。

效率方面，**Figure 4**给出了决定性证据：为达到GRPO的最佳精度，SFPO所需的rollout数仅为GRPO的1/4.93（DS-Qwen-7B）、1/3.50（Qwen3-4B-Base）和1/3.21（DS-Qwen-1.5B）；对应的端到端训练时间加速比分别为4.19×、2.65×和2.62×。尽管SFPO单步计算开销约为GRPO的1.37倍（K=3时），但总采样和时钟时间的显著减少使其总体计算效率更高。


![[assets/figures/papers/paper_list_l33_https_openreview_net_forum_id_xBlHiHdXap/figures/012_Figure_4.jpg]]
*Figure 4: Comparison between GRPO and SFPO. (a) Number of rollouts required to achieve the same best accuracy as GRPO. (b) Corresponding training time*

### 消融实验

#### α与K的耦合效应

**Figure 5**系统考察了α和K的交互影响：

![[assets/figures/papers/paper_list_l33_https_openreview_net_forum_id_xBlHiHdXap/figures/016_Figure_5.jpg]]
*Figure 5: Average training accuracy of different settings throughout the training process. (a): Small k=3 with varying values of α. (b): Large k=7 with varying values of α. (c): Varying values of k with fixed α = 0.8. (d): Impact of the existence of stage III*

- **小K=3时**（Figure 5a）：α在0.2至1.0范围内训练均稳定且优于GRPO，表明少量内更新步时离策略漂移不构成严重威胁。
- **大K=7时**（Figure 5b）：α=1.0（无插值）导致性能显著下降，而α=0.2恢复稳定且表现最佳，证实大K下必须通过重定位约束漂移。
- **固定α=0.8时**（Figure 5c）：K=3和K=5均优于GRPO，但K=7开始出现退化，说明内更新步数并非越多越好，需与α协调。
- **Stage III消融**（Figure 5d）：去除慢速校正步导致性能明显下降，验证了重定位后额外梯度修正的必要性。

#### Stage II插值是不可或缺的

**Figure 9**的消融实验最为关键：当K=7且完全移除Stage II插值时，训练直接崩溃；而保留插值的SFPO训练始终稳定且性能最优。这直接证实了重定位是防止离策略过拟合的核心机制，而非可选的锦上添花。


![[assets/figures/papers/paper_list_l33_https_openreview_net_forum_id_xBlHiHdXap/figures/022_Figure_9.jpg]]
*Figure 9: Ablation on interpolation scheme in Stage II with DeepSeek-R1-Distill-Qwen-1.5B*

#### 熵控制与α调度

**Figure 6**显示，移除熵控制（EC）导致训练约100步后精度明显下降，说明在收敛附近自适应关闭快速轨迹对稳定收敛至关重要。**Figure 7**对比了α直接重置与线性衰减两种策略，二者精度和稳定性曲线几乎重合，表明衰减方式影响很小，SFPO对α调度形式不敏感。

#### 跨任务鲁棒性

在编程任务LiveCodeBench上（**Figure 10**），α=0.8、K=3的设置同样最优，与数学任务结论一致。K=7时较小α（0.2）仍能维持稳定，证明SFPO的三阶段结构具有跨任务鲁棒性。

#### 与KL惩罚方案的对比

**Figure 11**将Stage II的插值方案替换为KL散度惩罚。结果表明：K=3时插值方案已大幅优于KL版本；K=7时KL版本训练崩溃，而插值方案在适当α下保持稳定。这说明插值重定位比KL正则化更有效地约束了离策略漂移。

#### 即插即用的兼容性

**Figure 12**和**Table 3**验证了SFPO作为高层优化插件的兼容性：在DAPO之上叠加SFPO，DS-distilled-Qwen-1.5B平均分从49.30提升至50.56（+1.26），Qwen3-4B-Base从46.48提升至47.87（+1.39），所有基准均有一致增益。这表明SFPO独立于底层GRPO变体的具体实现。


![[assets/figures/papers/paper_list_l33_https_openreview_net_forum_id_xBlHiHdXap/figures/029_Figure_12.jpg]]
*Figure 12: Comparison of DAPO and SFPO on math benchmarks. Validation average accuracy versus training step for DeepSeek-R1-Distill-Qwen-1.5B (left) and Qwen3-4B-Base (right)*

![[assets/figures/papers/paper_list_l33_https_openreview_net_forum_id_xBlHiHdXap/figures/030_Table_3.jpg]]
*Table 3: Performance on math reasoning benchmarks for DAPO and applying SFPO on top of DAPO*

### 公平性与资源开销

所有实验基于verl框架，批次大小256、每条问题8条回复、总训练步数400等配置均保持一致。SFPO不增加GPU显存开销：**Figure 8**证实，由于不需存储重优化器状态，仅需多保存一份模型权重副本，SFPO的显存消耗与GRPO相当。GRPO与SFPO使用相同的clip范围和KL正则系数，客观比较了更新规则本身的效果差异。

## 方法谱系与知识库定位

### 1. 与基线方法的关系

SFPO 的核心定位是**在线策略梯度算法的更新规则插件**，而非替代整个训练范式。其直接对标基线为 **GRPO**（Shao et al., 2024），后者是当前大语言模型推理训练中主流的在线策略RL方法。SFPO 保留了 GRPO 的目标函数、优势估计（组内标准化）和 rollout 生成流程不变，仅在参数更新环节将单次梯度更新替换为三阶段结构。

GRPO 的瓶颈在于：训练早期低质量 rollout 导致高方差梯度，且每批次仅执行一次更新，采样效率低下。SFPO 通过“快速多步内更新→重定位回插→慢速校正”的分解，在不改变目标函数的前提下构建了隐式信赖域机制，稳定了梯度方向。实验证据（Table 1）表明，SFPO 在六项数学推理基准上对 GRPO 的平均提升为 **+1.84 至 +2.80 分**（取决于基座模型），且在 AIME25 上最大提升达 **+7.50 分**（DS-distilled-Qwen-1.5B）。

SFPO 的插件特性进一步体现在其与 GRPO 变体的兼容性上。**DAPO**（Yu et al., 2025a）通过动态采样缓解零优势问题，SFPO 叠加于 DAPO 之上仍能带来一致的额外提升（Figure 12, Table 3），证明 SFPO 的更新机制独立于底层 GRPO 的具体实现细节。

### 2. 方法谱系中的位置

从在线策略RL的更新规则角度，SFPO 处于以下技术路线的交叉点：

- **多步内更新**：类似于在同一个 mini-batch 上执行多次梯度下降，但 SFPO 通过显式的重定位步骤解决了纯多步更新导致的离策略漂移问题。消融实验（Figure 9）证实，去除 Stage II 插值在大 K（如 K=7）时会导致训练崩溃，而保留插值则始终稳定。
- **信赖域方法**：SFPO 的重定位插值系数 α 直接约束参数距起始点的距离，形成隐式信赖域，这与 TRPO/PPO 的显式 KL 约束形成对比。与 KL 惩罚基线的对比实验（Figure 11）表明，SFPO 的插值方案在 K=3 和 K=7 下均大幅优于 KL 惩罚版本，且 K=7 时 KL 版本崩溃。
- **自适应步长调度**：SFPO 的熵触发 α 调度器（基于策略熵的滑动窗口 z-score）在收敛附近自动关闭快速轨迹（α→0），回退到纯在线更新。消融实验（Figure 6）表明，移除熵控制导致训练约 100 步后精度明显下降。

### 3. 适用边界与局限

**已验证的适用场景**：
- 数学推理任务（六项基准，1.5B–7B 参数规模）
- 编程任务（LiveCodeBench），α=0.8、K=3 设置与数学任务一致，证明跨任务鲁棒（Figure 10）
- 与 GRPO 及 DAPO 等变体的无缝集成

**明确的局限**：
1. **超参数复杂度**：SFPO 引入 K、α₀、熵窗口 ω 和阈值 τ 四个额外超参数，增加了调参负担。消融实验揭示了 K 与 α 的交互关系——小 K（如 3）时 α 在 0.2–1.0 范围内均稳定；大 K（如 7）时需较小 α（如 0.2）以避免离策略漂移（Figure 5a, 5b）。
2. **任务覆盖有限**：目前仅在数学推理和编程任务上验证，尚未在对话、多模态、工具使用等场景中测试。
3. **理论分析不完整**：理论分析基于局部二次模型和线性化假设，高维非凸下的严格收敛证明尚未给出。
4. **模型规模上限未知**：最大实验模型为 7B 参数，扩展到数十亿乃至百亿级模型的扩展性有待验证。
5. **α 调度敏感性**：自适应调度依赖策略熵的统计波动，可能对训练数据分布变化敏感，需要更多消融验证。

### 4. 开放问题

1. **更精细的自适应策略**：当前 α 调度仅依赖策略熵的 z-score，能否设计基于曲率或梯度范数的更精细调整策略，进一步提升效率？
2. **长逻辑链任务的适用性**：在多跳推理、代码生成、定理证明等更长逻辑链的任务中，SFPO 的三阶段分解是否仍然有效？
3. **向其他算法的推广**：将 SFPO 的“快-重定位-慢”思想推广至 PPO、Reinforce 等其他在线策略算法的可行性与收益如何？
4. **插值与 KL 正则化的互补**：插值与 KL 正则化是否存在互补组合方式，可以在更宽的 α 范围内保持稳定性？
5. **大规模并行训练的系统挑战**：在大规模并行训练（如数百 GPU）场景下，SFPO 的快-重定位-慢结构会带来哪些新的系统优化挑战？

## 原文 PDF

![[paperPDFs/ICLR_2026/Slow_Fast_Policy_Optimization_Reposition_Before_Update_for_LLM_Reasoning.pdf]]
