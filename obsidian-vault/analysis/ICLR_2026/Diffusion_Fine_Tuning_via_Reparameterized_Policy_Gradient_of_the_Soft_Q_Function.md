---
title: "Diffusion Fine-Tuning via Reparameterized Policy Gradient of the Soft Q-Function"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/Diffusion_Fine_Tuning_via_Reparameterized_Policy_Gradient_of_the_Soft_Q_Function.pdf
project_link: null
code_link: https://github.com/Shin-woocheol/SQDF
openreview_forum_id: 8zoxC9e23q
aliases:
- SSQBDF
- DFTRPGSQF
tags:
- ICLR_2026
- topic/reinforcement_learning_planning_agents
- topic/reinforcement_learning_planning_agents/deep_rl
core_operator: "核心因果控制变量是无需训练的软Q函数近似（通过后验均值估计与一致性模型）与折扣因子、重参数化策略梯度的组合。该方案能在KL正则化RL框架下直接注入低方差奖励梯度，并通过重放缓冲区精细调节奖励-多样性权衡，从而抑制过度优化。"
primary_logic: "将可微分奖励模型的梯度作为软Q函数的梯度，结合折扣因子降低早期去噪步骤的高不确定性影响、一致性模型提升Q估计精度、离线重放缓冲区保持模式覆盖，在微调扩散模型时实现了奖励最大化与样本自然性/多样性的平衡。"
claims:
- "SQDF采用训练免费的软Q函数近似，通过重参数化策略梯度直接利用奖励梯度进行低方差策略更新。"
- "引入折扣因子γ<1，对早期去噪步骤进行指数降权，改善信用分配并缓解近似误差。"
- "使用一致性模型替代Tweedie公式提供更准确的x0估计，提高软Q函数近似的可靠性。"
- "在文本到图像对齐任务中，SQDF在相同奖励水平下实现最高的对齐分数和多样性，显著抑制过度优化。"
---

# Diffusion Fine-Tuning via Reparameterized Policy Gradient of the Soft Q-Function

> [!tip] 核心洞察
> 将可微分奖励模型的梯度作为软Q函数的梯度，结合折扣因子降低早期去噪步骤的高不确定性影响、一致性模型提升Q估计精度、离线重放缓冲区保持模式覆盖，在微调扩散模型时实现了奖励最大化与样本自然性/多样性的平衡。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 基于软Q函数重参数化策略梯度的扩散模型微调 |
| 英文题名 | Diffusion Fine-Tuning via Reparameterized Policy Gradient of the Soft Q-Function |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=8zoxC9e23q) · [GitHub](https://github.com/Shin-woocheol/SQDF) |
| Topic | #topic/reinforcement_learning_planning_agents #topic/reinforcement_learning_planning_agents/deep_rl |
| Method | SQDF (Soft Q-based Diffusion Finetuning) |
| Dataset | Online Black-Box Optimization (45 simple animals), SDXL Aesthetic Fine-tuning, Stable Diffusion 1.5 Aesthetic Alignment |

> [!tip] 效果简介
> - Online Black-Box Optimization (45 simple animals) 上，Aesthetic Score 为 7.87 (SQDF-Bootstrap)，对比 6.63 (PPO+KL)，变化 +1.24。
> - Online Black-Box Optimization (45 simple animals) 上，ImageReward 为 1.14 (SQDF-Bootstrap)，对比 -1.35 (PPO+KL)，变化 +2.49。
> - SDXL Aesthetic Fine-tuning 上，Aesthetic Score 为 7.86，对比 7.18 (DRaFT)，变化 +0.68。

## 概要

扩散模型在对齐人类偏好时面临一个根本性瓶颈：**奖励过度优化**。当直接最大化下游奖励信号时，模型极易陷入语义崩溃和多样性丧失——生成图像虽然获得高奖励分数，却偏离文本提示、趋同于抽象模式。现有微调方法要么依赖不稳定且训练昂贵的独立价值网络，要么使用高方差蒙特卡洛梯度估计，无法在注入奖励梯度的同时有效保持生成质量与多样性。

**SQDF（Soft Q-based Diffusion Finetuning）** 针对这一瓶颈提出了一套**因果控制组合**：将可微分奖励模型的梯度直接作为软Q函数的梯度，通过重参数化策略梯度实现低方差更新。其核心洞察在于三个相互配合的机制：

- **训练免费的软Q函数近似**：利用后验均值估计将奖励梯度转化为Q函数梯度，无需训练独立价值网络，避免了价值函数估计不稳定的问题。
- **折扣因子信用分配**：引入折扣因子 $\gamma \in [0,1)$，对早期去噪步骤按 $\gamma^{t-1}$ 指数降权，反映早期步骤对最终样本质量的有限影响，有效缓解近似误差。
- **一致性模型提升估计精度**：用一致性模型替代Tweedie公式提供更准确的 $x_0$ 预测，使软Q函数近似在各去噪时间步上保持均匀可靠。

在KL正则化强化学习框架下，SQDF通过**离线重放缓冲区**实现策略更新，精细调节奖励与多样性的权衡，抑制过度优化。

**核心实验结果**：在文本到图像对齐任务中，SQDF在相同奖励水平下始终达成最高的对齐分数和多样性，帕累托前沿显著优于DRaFT+KL和DDPO+KL等KL正则化基线。在在线黑盒优化设定下，SQDF-Bootstrap以相同查询预算（15,360次）将美学分数从PPO+KL的6.63提升至**7.87**，ImageReward从-1.35提升至**1.14**，同时保持高对齐和多样性指标。消融实验证实：移除折扣因子导致收敛变慢且多样性下降；移除一致性模型使目标奖励从7.87降至7.10；移除重放缓冲区则损害模式覆盖。

**方法定位**：SQDF属于KL正则化强化学习微调范式，与DDPO（基于PPO的RL微调）、DRaFT（直接反向传播至最终状态）、ReFL（端到端奖励梯度微调）等方法形成对比。其关键区分在于**训练免费的软Q估计**与**重参数化低方差梯度**的组合，避免了价值网络训练和全链反向传播的各自缺陷。

### 扩散模型微调的核心瓶颈

扩散模型在文本到图像生成任务中展现出卓越能力，但其预训练目标与下游人类偏好之间存在固有偏差。为弥合这一差距，研究者通常将扩散模型微调建模为强化学习问题：将去噪过程视为马尔可夫决策过程（MDP），以奖励模型作为反馈信号，最大化生成样本的期望奖励。

然而，这一范式面临一个根本性瓶颈：**奖励过度优化（Reward Over-optimization）**。当模型单纯追求奖励最大化时，生成图像会逐渐偏离文本提示的语义约束（语义崩溃），同时丧失样本多样性（多样性崩溃），最终收敛至奖励模型偏好的抽象模式。Figure 8 系统性地展示了这一退化过程——随着美感分数上升，对齐指标（HPS、ImageReward）和多样性指标（LPIPS、DreamSim）同步下降。

### 现有方法的缺口

当前扩散模型微调方法可归为三类，各自存在显著局限：

**基于 PPO 的 RL 方法**（如 DDPO）将去噪轨迹视为完整序列，使用 PPO 进行策略优化。这类方法需要训练独立的价值网络来估计状态价值，但扩散 MDP 的高维连续状态空间使价值网络训练极不稳定，收敛缓慢。在线黑盒优化实验中，PPO+KL 仅达到 6.63 的美感分数和 -1.35 的 ImageReward 分数（Table 1），远低于 SQDF。

**端到端反向传播方法**（如 DRaFT、ReFL）直接通过去噪链反向传播奖励梯度。这类方法面临两个核心困难：其一，穿越完整去噪链的反向传播计算代价高昂且梯度方差极大；其二，缺乏有效的正则化机制，极易陷入奖励过度优化。实验表明，DRaFT 在达到高奖励时对齐分数和多样性均显著劣于 SQDF（Figure 3）。

**KL 正则化方法**（如 SEIKO）在直接反向传播基础上引入 KL 散度约束，以保持与预训练模型的接近程度。然而，这类方法仍依赖高方差的蒙特卡洛梯度估计，在有限查询预算下样本效率不足。

上述方法的共同缺陷在于：**无法在利用奖励梯度信号的同时，有效保持生成质量与多样性**。根本原因在于价值函数估计的不稳定性、梯度估计的高方差，以及信用分配机制的缺失——早期去噪步骤对最终样本质量的影响有限，但现有方法对所有步骤赋予相同权重。

### 本文动机

本文提出 **SQDF（Soft Q-based Diffusion Finetuning）**，旨在解决上述瓶颈。核心思路是将扩散模型微调形式化为 KL 正则化的强化学习问题，并通过以下创新实现低方差、高样本效率的策略更新：

1. **训练免费的软 Q 函数近似**：利用可微分奖励模型的梯度直接作为软 Q 函数的梯度，避免训练独立价值网络，同时通过重参数化策略梯度实现低方差更新。
2. **折扣信用分配**：引入折扣因子 $\gamma \in [0,1)$，对早期去噪步骤进行指数降权，反映其对最终样本质量的有限影响。
3. **一致性模型增强估计**：使用一致性模型替代传统的 Tweedie 公式进行后验均值估计，在所有去噪时间步提供均匀准确的 $\hat{x}_0$ 预测（Figure 2 展示了 Tweedie 估计在早期步骤的严重偏差与一致性模型的优势）。
4. **离线重放缓冲区**：支持离线策略更新，通过历史轨迹的复用提升模式覆盖，精细调节奖励与多样性的权衡。

SQDF 在在线黑盒优化和代理奖励微调两种设定下，均实现了奖励最大化与样本自然性/多样性的平衡，显著抑制了过度优化现象。

## 核心方法与创新机理

SQDF的核心创新在于构建了一套**训练免费的软Q函数近似**与**重参数化策略梯度**相结合的微调范式，从根本上解决了现有扩散模型微调方法在最大化下游奖励时面临的奖励过度优化与语义崩溃瓶颈。该方法在KL正则化强化学习框架下，通过三个关键组件的协同作用，实现了奖励梯度信号的低方差注入与生成多样性的精细控制。

### 关键机制创新

**1. 训练免费的软Q函数近似与重参数化策略梯度**

传统方法要么需要训练独立的价值网络（计算代价高且不稳定），要么依赖高方差蒙特卡洛梯度估计（样本效率低）。SQDF的核心突破在于：利用Tweedie公式的后验均值估计，将可微分奖励模型的梯度直接作为软Q函数的梯度，从而通过重参数化策略梯度实现低方差更新。如Equation (9)所示，软Q函数被近似为 $Q_{\mathrm{soft}}^{*}(x_{t}, x_{t-1}) \approx r(\hat{x}_{0}(x_{t-1}))$，其中 $\hat{x}_{0}(x_{t-1})$ 是从带噪中间状态预测的清晰样本。这一近似使得梯度计算无需穿越完整的去噪链，避免了高方差蒙特卡洛估计或昂贵的价值网络训练，同时保留了奖励梯度的精确引导能力。

**2. 折扣信用分配机制**

扩散模型的去噪过程是一个多步决策序列，早期步骤对最终样本质量的影响具有高度不确定性。现有方法对所有去噪步骤赋予相同权重（$\gamma=1$），导致早期步骤的噪声梯度干扰优化过程。SQDF引入折扣因子 $\gamma \in [0,1)$，按 $\gamma^{t-1}$ 对早期去噪步骤进行指数降权（Section 4.2.1, Equation 13-15），使得梯度信号主要集中在与最终奖励因果关联更强的高质量后期步骤。这一机制有效缓解了信用分配问题，消融实验表明移除折扣因子（$\gamma=1$）会导致早期收敛显著变慢，对齐分数和多样性指标均出现明显下降（Figure 6）。

**3. 一致性模型增强的后验均值估计**

Tweedie公式的单步 $x_0$ 估计在早期去噪步骤存在较大误差（Figure 2b），这会降低软Q函数近似的可靠性。SQDF采用冻结的一致性模型 $f_{\psi}$ 替代Tweedie公式，在所有去噪时间步上提供均匀精度的清晰样本预测（Figure 2c）。消融实验证实，移除一致性模型使得目标奖励从7.87降至7.10（Table 2），验证了该组件对训练效率和Q估计可靠性的关键作用。值得注意的是，使用2步DDIM采样虽能改善优化，但4步DDIM会导致训练不稳定（Figure 7），进一步体现了一致性模型作为稳定 $x_0$ 预测器的独特优势。

### 训练范式创新：离线策略更新与重放缓冲区

与DDPO、DRaFT等在线策略采样方法不同，SQDF的损失函数天然支持离线策略更新。通过引入重放缓冲区 $\mathcal{D}$ 存储历史轨迹（Section 4.2.3），SQDF实现了两个关键突破：一是通过复用历史经验提升样本效率；二是通过控制缓冲区数据的分布来精细调节奖励-多样性权衡。消融实验表明，移除重放缓冲区会导致多样性指标（DreamSim-Div, LPIPS-Div）显著下降（Table 2），印证了缓冲区对保持模式覆盖、抑制过度优化的核心作用。

### 方法定位与对比优势

相较于现有方法的改进维度如下表所示：

| 创新维度 | 现有方法局限 | SQDF方案 | 证据锚点 |
|---------|-------------|---------|---------|
| 信用分配机制 | 所有步骤权重相同（$\gamma=1$） | 折扣因子 $\gamma \in [0,1)$ 指数降权早期步骤 | Section 4.2.1, Equation 13-15 |
| Q函数估计 | 需训练价值网络或高方差MC估计 | 训练免费的、可微分的后验均值近似+一致性模型 | Section 3.3 (Eq.9), Section 4.2.2 |
| 策略梯度估计 | 高方差MC梯度或全链反向传播 | 重参数化策略梯度，直接利用奖励梯度 | Section 4.1, Equation 12 |
| 训练数据分布 | 在线策略采样 | 离线策略更新+重放缓冲区 | Section 4.2.3 |

最终，SQDF整合上述创新的损失函数为（Equation 16）：

$$\mathcal{L}_{\mathrm{SQDF}}(\theta) = \mathbb{E}_{x_{t} \sim \mathcal{D}, ~ x_{t-1} \sim p_{\theta}} [ -\gamma^{t-1} r(f_{\psi}(x_{t-1})) + \alpha D_{KL}(p_{\theta}(x_{t-1} \mid x_{t}) || p'(x_{t-1} \mid x_{t})) ]$$

该损失函数将折扣因子、一致性模型和重放缓冲区有机整合，在KL正则化约束下实现了奖励最大化与生成质量保持的平衡。实验表明，SQDF在相同奖励水平下始终达到最高的对齐分数和多样性（Figure 3），在在线黑盒优化场景中以有限的查询预算显著超越PPO+KL等基线方法（Table 1: SQDF-Bootstrap Aesthetic 7.87 vs 6.63, ImageReward 1.14 vs -1.35）。


![[assets/figures/papers/paper_list_l44_https_openreview_net_forum_id_8zoxC9e23q/figures/015_Figure_5.jpg]]
*Figure 5: Comparison of generated images from different fine-tuning methods, using model checkpoints selected when a reward of 8.0 was achieved (or the maximum reward if 8.0 was not reached). The average reward for the presented images is shown for each method*

SQDF 将扩散模型微调形式化为一个有限时域的 KL 正则化强化学习问题，其整体 pipeline 由两条交织的数据流构成：**生成-存储流** 与 **训练-更新流**。

### 生成-存储流

可训练扩散模型 $p_\theta$ 从噪声 $x_T \sim \mathcal{N}(0, I)$ 出发，经 $T$ 步去噪生成完整轨迹 $\tau = (x_T, x_{T-1}, \dots, x_0)$。最终干净样本 $x_0$ 被送入冻结的奖励模型 $r_\phi$（可为代理模型或黑盒预言机）获取奖励信号，同时整条轨迹存入**重放缓冲区 $\mathcal{D}$**，供后续离线策略更新使用（Section 4.2.3）。

### 训练-更新流

训练时，从重放缓冲区随机采样一个中间噪声状态 $x_t$，由当前策略 $p_\theta$ 执行**单步去噪**得到 $x_{t-1}$。随后，冻结的**一致性模型 $f_\psi$** 以 $x_{t-1}$ 为输入，直接预测对应的干净样本 $\hat{x}_0 = f_\psi(x_{t-1})$。该预测被送入奖励模型获得标量奖励 $r(\hat{x}_0)$，其梯度 $\nabla_{x_{t-1}} r(\hat{x}_0)$ 经**重参数化策略梯度**直接注入 $p_\theta$ 的更新中，同时施加相对于冻结参考模型 $p'$ 的 KL 散度惩罚，形成完整的训练损失：

$$
\mathcal{L}_{\mathrm{SQDF}}(\theta) = \mathbb{E}_{x_t \sim \mathcal{D}, \, x_{t-1} \sim p_\theta} \left[ -\gamma^{t-1} r(f_\psi(x_{t-1})) + \alpha D_{\mathrm{KL}}(p_\theta(x_{t-1} \mid x_t) \,||\, p'(x_{t-1} \mid x_t)) \right]
$$

### 模块关系与因果机制

上述 pipeline 中四个核心模块的协同构成了 SQDF 抑制奖励过度优化的因果链路：

| 模块 | 角色 | 因果作用 |
|------|------|----------|
| **一致性模型 $f_\psi$** | 冻结的 $\hat{x}_0$ 预测器 | 替代 Tweedie 公式提供更准确的后验均值估计，从根本上提升软 Q 函数近似的可靠性（Figure 2 表明 Tweedie 公式在早期去噪步骤的 $\hat{x}_0$ 估计高度不准确，而一致性模型在所有时间步保持均匀精度） |
| **折扣因子 $\gamma \in [0,1)$** | 信用分配超参数 | 按 $\gamma^{t-1}$ 对早期去噪步骤的奖励梯度进行指数降权，缓解因 $\hat{x}_0$ 估计不确定性导致的噪声梯度传播，同时改善信用分配（Section 4.2.1） |
| **重放缓冲区 $\mathcal{D}$** | 离线经验存储 | 打破在线策略采样的分布漂移，通过复用历史轨迹保持生成模式的覆盖范围，精细调节奖励-多样性权衡（Table 2 消融实验证实移除缓冲区导致 DreamSim-Div 和 LPIPS-Div 下降） |
| **参考模型 $p'$** | KL 正则化锚点 | 约束微调策略不偏离预训练分布太远，维持生成样本的自然性与语义一致性 |

### 关键设计选择

与现有方法的核心差异在于**软 Q 函数的训练免费近似**：SQDF 不训练独立的价值网络（如 Uehara et al., 2024b），也不依赖高方差蒙特卡洛估计（如 Venkatraman et al., 2024），而是利用可微分奖励模型的梯度直接作为软 Q 函数梯度，通过重参数化策略梯度实现低方差更新（Equation 12）。这一设计使得奖励梯度信号能够绕过完整去噪链的反向传播，在保持计算效率的同时避免梯度爆炸/消失问题。

> **注意**：一致性模型的预测质量直接影响软 Q 函数估计的准确性，当其分布与基础扩散模型不匹配时可能引入偏差，这是该框架的一个内在局限。

### 3.1 扩散模型的MDP形式化

SQDF将扩散模型的去噪过程形式化为有限时域马尔可夫决策过程（MDP）。状态空间为所有可能的时间步-样本对 $(x_t, t)$，动作空间为从 $x_t$ 到 $x_{t-1}$ 的去噪步骤，转移是确定性的。奖励仅在最终时间步发放，即 $r(x_0)$，中间步骤奖励为零。这一形式化使得强化学习中的策略梯度方法可以直接应用于扩散模型的微调。

预训练扩散模型 $p'$ 作为参考策略，提供KL正则化的锚点。可训练的扩散模型 $p_\theta$ 作为当前策略，其反向过程为：

$$p_\theta(x_{0:T}) = p(x_T) \prod_{t=1}^{T} p_\theta(x_{t-1} \mid x_t), \quad p_\theta(x_{t-1} \mid x_t) = \mathcal{N}\big(x_{t-1}; \mu_\theta(x_t, t), \sigma_t^2 I\big)$$

### 3.2 KL正则化强化学习目标

为在最大化奖励的同时保持生成质量与多样性，SQDF采用KL正则化的强化学习目标：

$$p^{*} = \underset{p_{\theta}}{\arg \operatorname*{max}} \mathbb{E}_{\tau \sim p_{\theta}(\tau)} \left[ r(x_{0}) - \alpha \sum_{t=1}^{T} \mathcal{D}_{KL}(p_{\theta}(\cdot \mid x_{t}) || p'(\cdot \mid x_{t})) \right] \tag{4}$$

其中 $\alpha$ 控制奖励最大化与策略偏离惩罚之间的权衡强度。该目标对应的最优软Q函数定义为：

$$Q_{\mathrm{soft}}^{*}(x_t, x_{t-1}) = \mathbb{E}_{p^{*}} \left[ r(x_0) - \alpha \sum_{k=1}^{t-1} D_{KL}(p^{*}(\cdot | x_k) || p'(\cdot | x_k)) \;\middle|\; x_t, x_{t-1} \right]$$

满足软贝尔曼方程：

$$V_{\mathrm{soft}}^{*}(x_t) = \alpha \log \mathbb{E}_{x_{t-1} \sim p'(\cdot | x_t)} \left[ \exp\left( \frac{R(x_t, x_{t-1}) + V_{\mathrm{soft}}^{*}(x_{t-1})}{\alpha} \right) \right]$$

### 3.3 训练免费的软Q函数近似

SQDF的核心创新在于避免训练独立的价值网络，转而利用可微分奖励模型直接构造软Q函数的近似。基于Tweedie公式的后验均值估计 $\hat{x}_0(x_t) = \mathbb{E}_{p'}[x_0 \mid x_t]$，软最优Q函数可近似为：

$$Q_{\mathrm{soft}}^{*}(x_t, x_{t-1}) \approx r(\hat{x}_0(x_{t-1})) \tag{9}$$

这一近似的直觉是：在KL正则化约束下，最优策略不会显著偏离预训练模型 $p'$，因此用 $p'$ 的后验均值估计 $x_0$ 是合理的。该近似无需训练，且保持了端到端的可微性，使得奖励梯度可以直接用于策略更新。

### 3.4 重参数化策略梯度

利用上述软Q函数近似，SQDF通过重参数化技巧将策略梯度计算转化为直接对奖励模型梯度的利用。令 $x_{t-1} = \mu_\theta(x_t, t) + \sigma_t \epsilon$，其中 $\epsilon \sim \mathcal{N}(0, I)$，策略梯度损失为：

$$\nabla_{\theta} \mathcal{L}(\theta) = \mathbb{E}_{x_t} \left[ \mathbb{E}_{\epsilon \sim \mathcal{N}(0,I)} \left[ -\nabla_{x_{t-1}} r(\hat{x}_0(x_{t-1})) \cdot \nabla_{\theta} \mu_{\theta}(x_t, t) + \alpha \nabla_{\theta} D_{KL}(p_{\theta} || p') \right] \right] \tag{12}$$

该公式的关键在于：奖励梯度 $\nabla_{x_{t-1}} r(\hat{x}_0(x_{t-1}))$ 直接通过可微分奖励模型 $r_\phi$ 计算，无需穿越完整的去噪链进行反向传播，也避免了高方差蒙特卡洛估计。与DRaFT等方法穿越全部 $T$ 步去噪步骤不同，SQDF仅在单步去噪后即评估奖励，显著降低了计算开销和梯度方差。

### 3.5 折扣因子与信用分配

扩散模型的早期去噪步骤（$t$ 接近 $T$）对最终样本 $x_0$ 的影响有限且不确定性高。为改善信用分配，SQDF引入折扣因子 $\gamma \in [0, 1)$，对早期步骤进行指数降权。折扣化的KL正则化目标为：

$$p^{*} = \underset{p_{\theta}}{\arg \operatorname*{max}} \mathbb{E}_{\tau \sim p_{\theta}(\tau)} \left[ \gamma^{T-1} r(x_{0}) - \alpha \sum_{t=1}^{T} \gamma^{T-t} \mathcal{D}_{KL}(p_{\theta}(\cdot \mid x_{t}) || p'(\cdot \mid x_{t})) \right] \tag{13}$$

对应的折扣化软Q函数满足如下上下界：

$$\alpha \log \mathbb{E}_{x_{0:t-2} \sim p'(\cdot | x_{t-1})} \Big[ \exp\Big( \frac{\gamma^{t-1}}{\alpha} r(x_0) \Big) \Big] \leq Q_{\operatorname{soft}}^{*}(x_t, x_{t-1}) \leq \gamma^{t-1} \max r(x_0)$$

当 $\gamma < 1$ 时，早期步骤的Q值被显著压缩，其梯度贡献相应降低，从而缓解了因后验均值近似不准确（尤其在 $t$ 较大时）导致的梯度噪声。

### 3.6 一致性模型增强x₀估计

Tweedie公式在早期去噪步骤（$t$ 接近 $T$）的 $x_0$ 估计极不准确（见Figure 2），直接限制了软Q函数近似的可靠性。SQDF采用冻结参数的一致性模型 $f_\psi$（Song et al., 2023）替代Tweedie公式进行 $x_0$ 预测。一致性模型通过蒸馏训练，能在任意噪声水平下直接输出清晰的 $x_0$ 估计，且预测精度在不同时间步上更为均匀。

与DDIM多步采样的对比实验表明（Figure 7）：2步DDIM可改善优化但效果不及一致性模型，而4步DDIM导致训练不稳定。一致性模型因此成为可靠性与稳定性的帕累托最优解。

### 3.7 重放缓冲区与离线策略更新

SQDF的梯度形式天然支持离线策略更新。通过维护重放缓冲区 $\mathcal{D}$，存储历史生成的轨迹，训练时从中采样 $x_t$ 进行策略更新。最终整合所有组件的SQDF损失函数为：

$$\mathcal{L}_{\mathrm{SQDF}}(\theta) = \mathbb{E}_{x_t \sim \mathcal{D}, ~ x_{t-1} \sim p_{\theta}} \left[ -\gamma^{t-1} r(f_{\psi}(x_{t-1})) + \alpha D_{KL}(p_{\theta}(x_{t-1} \mid x_t) || p'(x_{t-1} \mid x_t)) \right] \tag{16}$$

其中 $f_\psi(x_{t-1})$ 为一致性模型预测的 $x_0$，$r$ 为可微分奖励模型（代理模型或黑盒预言机的代理）。重放缓冲区的作用是保持模式覆盖：通过复用历史样本，防止策略过快坍缩到高奖励但低多样性的区域。消融实验（Table 2）证实，移除缓冲区后多样性指标（DreamSim-Div, LPIPS-Div）显著下降。

### 3.8 模块协作机制总结

整个SQDF框架的因果链路如下：**一致性模型** $f_\psi$ 提供准确的 $x_0$ 估计 → **可微分奖励模型** $r_\phi$ 基于该估计计算奖励梯度 → **折扣因子** $\gamma$ 对早期步骤的梯度进行指数降权，抑制噪声 → **重参数化策略梯度**将奖励梯度直接注入 $p_\theta$ 的均值预测 $\mu_\theta$ 的更新 → **KL正则化**约束 $p_\theta$ 不偏离预训练模型 $p'$ → **重放缓冲区** $\mathcal{D}$ 维持样本多样性，防止模式坍缩。五个组件协同作用，在奖励最大化与生成质量/多样性保持之间实现精细平衡。

## 实验与关键发现

### 主实验结果

#### 奖励过度优化的系统性抑制

现有扩散模型微调方法（如DDPO、DRaFT、ReFL）在最大化下游奖励时普遍陷入奖励过度优化（reward over-optimization），表现为语义崩溃（生成内容与文本提示脱节）和多样性丧失（收敛至相似抽象模式）。Figure 8 直观展示了这一现象：随着美感分数上升，图像逐渐偏离原始语义约束，最终产生高度同质化的输出。

SQDF通过三个因果机制协同抑制过度优化：

1. **训练免费的软Q函数近似**：利用可微分奖励模型的梯度作为软Q函数梯度，通过重参数化策略梯度直接注入低方差信号，避免训练独立价值网络的不稳定性。
2. **折扣因子γ<1的信用分配**：对早期去噪步骤按γ^(t-1)指数降权，缓解早期步骤高不确定性带来的近似误差（详见消融实验Figure 6）。
3. **离线重放缓冲区**：存储历史轨迹支持离线策略更新，扩大模式覆盖范围，精细调节奖励-多样性权衡。

在美感分数和HPSv2两个目标奖励上的系统评估（Figure 3）表明：SQDF在达到同等奖励水平时，一致性地获得最高的对齐分数（ImageReward、HPS）和多样性指标（LPIPS、DreamSim），而DRaFT和DDPO在奖励上升后迅速出现对齐和多样性指标下降。

![[assets/figures/papers/paper_list_l44_https_openreview_net_forum_id_8zoxC9e23q/figures/011_Figure_3.jpg]]
*Figure 3: Comparison of evaluation metrics during optimization of the target reward. Top: The target reward is the LAION aesthetic score. Bottom: The target reward is HPSv2. (a), (b), (e), and (f): evaluation of alignment score using ImageReward and HPS. (c), (d), (g), and (h): evaluation of diversity using LPIPS and DreamSim*

#### 与KL正则化基线的权衡曲线对比

Figure 4展示了通过调节KL正则化系数α获得的奖励-对齐/多样性权衡曲线。SQDF的曲线在多个指标上占据Pareto最优前沿，表明在给定奖励水平下，SQDF能更好地保持生成质量。相比之下，DRaFT+KL和DDPO+KL的曲线整体位于次优区域，尤其在高奖励区域差距更为显著。

![[assets/figures/papers/paper_list_l44_https_openreview_net_forum_id_8zoxC9e23q/figures/014_Figure_4.jpg]]
*Figure 4: Comparison of trade-off curves with KL-regularized baselines. Curves are obtained by varying the KL-regularization coefficient α. Darker points correspond to a stronger KL-regularizer*

#### 在线黑盒优化

在仅能通过查询获取奖励信号的在线黑盒优化设定下（Table 1），SQDF在15,360次查询预算内达到最高的目标奖励：

- **SQDF-Bootstrap**：Aesthetic分数7.87，ImageReward 1.14
- **PPO+KL**：Aesthetic分数6.63，ImageReward -1.35
- **SEIKO**：Aesthetic分数7.53，ImageReward 0.69

SQDF-Bootstrap相比PPO+KL在Aesthetic上提升**+1.24**，在ImageReward上提升**+2.49**，且多样性指标（LPIPS-Div 0.49, DreamSim-Div 0.51）显著优于所有基线。Figure 11的定性对比进一步印证了SQDF在有限查询预算下生成图像的语义一致性和视觉质量优势。

#### SDXL上的可扩展性

Table 3显示，在更大规模的SDXL模型上，SQDF同样有效：Aesthetic分数从预训练模型的5.45提升至7.86（DRaFT为7.18），ImageReward从0.88提升至1.21（DRaFT为0.91）。Table 4进一步表明，SQDF在SD1.5（860M）和SDXL（2.6B）上的相对性能提升高度一致（Aesthetic均约+44%），验证了方法对基础模型规模的不敏感性。

![[assets/figures/papers/paper_list_l44_https_openreview_net_forum_id_8zoxC9e23q/figures/058_Table_3.jpg]]
*Table 3: Comparison of DRaFT and SQDF on fine-tuning SDXL for aesthetic score*

![[assets/figures/papers/paper_list_l44_https_openreview_net_forum_id_8zoxC9e23q/figures/059_Table_4.jpg]]
*Table 4: Furthermore, to investigate whether the effectiveness of SQDF depends on the size of the base model, we compare the relative performance improvements between SD 1.5 (860M) and SDXL (2.6B). As shown in Table 4, the relative improvement achieved by SQDF is highly consistent across both architectures. Table 4: Relative performance improvements of SQDF on SD1.5 and SDXL for aesthetic score. These results demonstrate that SQDF optimizes the target reward while mitigating overoptimization, regardless of the underlying diffusion backbone*

### 消融实验

#### 折扣因子γ的关键作用

移除折扣因子（设置γ=1）导致训练动态显著恶化（Figure 6）：早期优化速度明显变慢，且对齐分数和多样性指标出现大幅下降。这验证了折扣因子在信用分配中的核心作用——早期去噪步骤对最终样本质量影响有限，对其赋予等权重会引入有害的梯度信号。

Figure 10进一步探索了不同γ值的影响：较高的γ（如0.99）带来更快的收敛速度，但以牺牲多样性和对齐分数为代价；较低的γ（如0.9）则更保守地保持生成质量。这表明γ是调节优化速度与质量保持之间平衡的关键超参数。

#### 一致性模型对训练效率的决定性影响

Table 2的消融显示，移除一致性模型（w/o CM）导致目标奖励从7.87降至7.10，降幅达**-0.77**。一致性模型通过提供跨时间步均匀准确的后验均值估计（如Figure 2c所示），显著提升了软Q函数近似的可靠性，从而加速收敛并稳定训练。

Figure 7对比了DDIM多步采样与一致性模型作为x̂₀预测器的效果：2步DDIM能改善优化，但4步DDIM导致训练不稳定。一致性模型作为Pareto最优解，在预测精度和训练稳定性之间取得了平衡。

#### 重放缓冲区对多样性的保护作用

移除重放缓冲区（w/o buffer）虽未显著影响目标奖励（8.06 vs 7.87），但导致多样性指标下降：DreamSim-Div从0.58降至0.56，LPIPS-Div从0.56降至0.55（Table 2）。这印证了缓冲区通过重用历史经验来保持模型支持覆盖、防止模式坍缩的机制。Figure 9显示优先级重放缓冲区可进一步提升美感分数优化效果。

![[assets/figures/papers/paper_list_l44_https_openreview_net_forum_id_8zoxC9e23q/figures/021_Table_2.jpg]]
*Table 2: Ablation study on Consistency model (CM) and Buffer. The consistency model enables faster convergence, while the buffer preserves diversity*

### 失败模式与局限性

1. **一致性模型的分布匹配依赖**：当一致性模型的分布与基础扩散模型不匹配时，x̂₀预测偏差会传导至软Q函数估计，影响梯度信号质量。当前方法缺乏对此偏差的检测与校正机制。

2. **折扣因子的启发式选择**：γ的最优值因任务和奖励函数而异，目前依赖手动调节。Figure 10显示不同γ值在优化速度和生成质量之间存在显著权衡，缺乏自适应调节机制。

3. **奖励函数范围的限制**：当前实验聚焦于美感分数和人类偏好分数等密集、可微的奖励信号。在更复杂或稀疏奖励（如分子性质、物理约束）上的有效性有待验证。

4. **缓冲区策略的基础性**：当前重放缓冲区采用简单存储与均匀采样，更高级的优先级采样或遗忘策略可能进一步提升样本效率，尤其在在线黑盒优化场景下。

## 定位与知识库关联

### 1. 在扩散模型微调谱系中的坐标

SQDF 处于 **KL 正则化强化学习微调** 与 **直接奖励梯度利用** 两条技术路线的交汇点。现有扩散模型微调方法可沿两个维度进行定位：

**维度一：策略更新机制**
- **PPO 族方法**（如 DDPO）依赖高方差蒙特卡洛梯度估计，需训练独立价值网络，训练不稳定且样本效率低。
- **直接反向传播族方法**（如 DRaFT、ReFL）将奖励梯度端到端反向传播至扩散模型参数，虽能利用梯度信号，但易陷入奖励过度优化，导致语义崩溃（Figure 8 中清晰展示：随美学分数上升，生成图像逐渐丧失与提示词的对齐能力，并收敛至相似抽象模式）。
- **SQDF 的定位**：通过重参数化策略梯度，直接将可微分奖励模型的梯度作为软 Q 函数的梯度注入策略更新（Equation 12），在保持低方差梯度估计的同时，避免了完整去噪链的反向传播。

**维度二：信用分配与 Q 函数估计**
- 现有方法对所有去噪步骤赋予均等权重（γ=1），忽视了早期步骤对最终样本质量影响有限这一事实。
- 部分工作尝试训练独立价值网络（如 Uehara et al., 2024b 的工作），但训练开销大且易受分布偏移影响。
- **SQDF 的突破**：提出训练免费的软 Q 函数近似——利用 Tweedie 公式的后验均值估计 $\hat{x}_0(x_{t-1})$ 作为 Q 函数输入（Equation 9），并通过**一致性模型**提升估计精度（Figure 2 显示一致性模型在所有时间步上均提供均匀准确的 $x_0$ 预测，而 Tweedie 公式在早期步骤高度不准确），同时引入**折扣因子 γ** 对早期步骤进行指数降权（Equation 13-15），从根本上改善了信用分配。

### 2. 与 KL 正则化基线的关系

SQDF 与带 KL 惩罚的 DDPO（DDPO+KL）和 DRaFT（DRaFT+KL）共享 KL 正则化框架，但在实现路径上存在本质差异：

| 维度 | DDPO+KL | DRaFT+KL | SQDF |
|------|---------|----------|------|
| 梯度估计 | 高方差蒙特卡洛 | 穿越完整去噪链的反向传播 | 重参数化策略梯度（低方差） |
| Q 函数 | 需训练价值网络 | 隐式通过反向传播 | 训练免费、可微分近似 |
| 信用分配 | 均匀权重（γ=1） | 均匀权重（γ=1） | 折扣因子 γ<1 |
| 训练数据分布 | 在线策略采样 | 在线策略采样 | 离线重放缓冲区 |

Figure 4 的权衡曲线直接验证了 SQDF 的优势：在变化 KL 正则化系数 α 时，SQDF 几乎在所有指标上占据帕累托最优前沿，而 DDPO+KL 和 DRaFT+KL 的曲线始终处于次优位置。这表明 SQDF 的梯度注入机制与信用分配策略共同作用，在奖励-多样性权衡空间中实现了更高效的前沿推进。

### 3. 在线黑盒优化场景下的适用边界

Table 1 展示了 SQDF 在有限查询预算（15,360 次预言机查询）下的表现。SQDF-Bootstrap 达到美学分数 7.87，较 PPO+KL（6.63）提升 1.24，ImageReward 从 -1.35 跃升至 1.14。这一优势源于：

- **样本效率**：重参数化梯度提供低方差更新信号，减少对大量在线采样的依赖。
- **离线策略兼容性**：重放缓冲区使 SQDF 能复用历史轨迹，在查询预算受限时维持模式覆盖。

但需注意，SQDF 在黑盒场景下依赖代理奖励模型引导搜索（如 Bootstrap 或 UCB 策略），代理模型的精度直接影响优化上限。当代理模型与真实预言机分布严重不匹配时，SQDF 的梯度引导可能失效。

### 4. 局限性与开放问题

**已识别的局限**（需手动验证具体边界值）：

1. **一致性模型依赖**：软 Q 函数估计的可靠性直接受一致性模型 $f_\psi$ 预测质量影响。Table 2 显示移除一致性模型导致目标奖励从 7.87 降至 7.10，但若 $f_\psi$ 的分布与基础扩散模型 $p_\theta$ 不匹配，可能引入系统性偏差。Figure 7 进一步揭示：2 步 DDIM 采样能改善优化，但 4 步 DDIM 导致训练不稳定，表明一致性模型在当前框架中提供了关键的稳定性保障。

2. **折扣因子 γ 的启发式选择**：Figure 10 显示不同 γ 值对训练动态有显著影响——更高 γ 加速收敛但牺牲多样性和对齐分数。当前 γ 的选择依赖任务特定的手动调节，缺乏自适应机制。

3. **奖励函数类型的局限性**：现有实验覆盖 LAION 美学分数和 HPSv2 人类偏好分数，这些奖励相对稠密且平滑。在更复杂、稀疏或非平滑奖励函数（如分子性质预测、结构约束）上的普适性尚未验证。

4. **重放缓冲区策略的基础性**：当前采用均匀采样缓冲区，Figure 9 显示优先级重放对美学分数有额外提升，表明更先进的缓冲区管理技术（如基于不确定性的采样、分层存储）可能进一步改善样本效率和模式覆盖。

**开放问题**：

- 能否利用更先进的一步蒸馏模型（如分布匹配蒸馏）替代一致性模型，在保持估计精度的同时降低计算开销？
- 折扣因子 γ 的自适应选择机制：是否可根据去噪步骤的不确定性或 Q 函数估计的置信度动态调整 γ？
- SQDF 的建模范式在更广泛的生成任务（分子生成、视频生成、3D 生成）中是否依然有效？这些任务的去噪过程可能具有不同的时间依赖结构。
- KL 正则化强度 α 的动态调节：可否结合元学习或自动调节机制，在优化过程中根据奖励-多样性权衡的实时状态调整 α，实现多目标帕累托前沿的自动探索？

## 原文 PDF

![[paperPDFs/ICLR_2026/Diffusion_Fine_Tuning_via_Reparameterized_Policy_Gradient_of_the_Soft_Q_Function.pdf]]
