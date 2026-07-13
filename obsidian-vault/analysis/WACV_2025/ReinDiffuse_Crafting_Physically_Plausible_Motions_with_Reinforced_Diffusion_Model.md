---
title: "ReinDiffuse: Crafting Physically Plausible Motions with Reinforced Diffusion Model"
type: paper
paper_level: A
venue: WACV
year: 2025
pdf_ref: "paperPDFs/WACV_2025/ReinDiffuse:_Crafting_Physically_Plausible_Motions_with_Reinforced_Diffusion_Model.pdf"
project_link: "https://reindiffuse.github.io/"
code_link: null
aliases:
- ReinDiffuse
tags:
- WACV_2025
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
- topic/generative_models_diffusion
- topic/generative_models_diffusion/diffusion_image_video
core_operator: 在不修改网络结构的前提下，通过重新参数化将 MDM 的确定性输出转化为高斯动作分布，使之兼容强化学习框架；并设计基于关节位置的四类物理合理性奖励函数，用 PPO 对预训练 MDM 进行微调，直接优化动作的物理保真度。
primary_logic: 将运动扩散模型的输出重新解释为动作分布的均值（μ），引入固定的标准差（σ）构建随机策略，使扩散模型可以像连续动作策略一样接受强化学习训练；同时设计专门针对滑步、浮空、地面穿透和脚部截交的逐帧奖励函数，在不依赖物理模拟器的情况下，以最小化非物理行为为目标高效地微调模型。
claims:
- 在 HumanML3D 数据集上，ReinDiffuse 将 FID 从 MDM 的 0.544 降至 0.385，相对提升 29%
- 在 KIT-ML 数据集上，FID 从 MDM 的 0.494 降至 0.326，相对提升 34%
- 物理合理性指标大幅改善：滑步比从 0.102 降至 0.058，浮空高度从 1.757 m 降至 0.711 m，地面穿透和脚部截交完全消除（降至 0.000），各项指标均接近真实数据
- HumanML3D 上 FID↓ = 0.385
---

# ReinDiffuse: Crafting Physically Plausible Motions with Reinforced Diffusion Model

> [!tip] 核心洞察
> 将运动扩散模型的输出重新解释为动作分布的均值（μ），引入固定的标准差（σ）构建随机策略，使扩散模型可以像连续动作策略一样接受强化学习训练；同时设计专门针对滑步、浮空、地面穿透和脚部截交的逐帧奖励函数，在不依赖物理模拟器的情况下，以最小化非物理行为为目标高效地微调模型。

| 字段 | 内容 |
|------|------|
| 中文题名 | ReinDiffuse：用强化扩散模型生成物理合理的人体运动 |
| 英文题名 | ReinDiffuse: Crafting Physically Plausible Motions with Reinforced Diffusion Model |
| 会议/期刊 | WACV 2025 |
| Links | [paper](https://arxiv.org/abs/2410.07296) · [Project](https://reindiffuse.github.io/) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction #topic/generative_models_diffusion #topic/generative_models_diffusion/diffusion_image_video |
| Method | ReinDiffuse |
| Dataset | HumanML3D, KIT-ML |

> [!tip] 效果简介
> - HumanML3D 上，FID↓ 0.385 vs 0.544 (MDM) (-29.2%)；R-Precision↑ 0.622 vs 0.611 (MDM) (+0.011)；Skate ratio→ 0.058 vs 0.102 (MDM) (接近真实 (0.057))。
> - KIT-ML 上，FID↓ 0.326 vs 0.494 (MDM) (-34.0%)；Skate ratio→ 0.087 vs 0.122 (MDM) (接近真实 (0.085))；Float (m)→ 0.938 vs 1.836 (MDM) (接近真实 (0.930))。

## 概要

### 1. 问题背景

文本驱动的人体运动生成旨在根据自然语言描述合成逼真的三维动作序列。近年来，以**MDM**（Tevet et al., arXiv 2022）为代表的运动扩散模型在语义匹配和运动多样性上取得了显著进展，但其生成的运动常出现**滑步、浮空、地面穿透和脚部截交**等物理不合理现象。这些问题的根源在于：扩散模型仅从数据分布中学习运动模式，缺乏对物理常识的显式建模。

### 2. 核心方法

**ReinDiffuse** 提出了一种将强化学习与运动扩散模型相融合的新范式，其核心思路是：在不修改网络结构的前提下，将 MDM 的确定性输出重新参数化为高斯动作分布的均值，引入固定标准差构建随机策略，使扩散模型兼容强化学习的策略优化框架。在此基础上，设计四类基于关节位置的逐帧物理奖励函数（滑步、浮空、地面穿透、脚部截交），利用 PPO 算法对预训练 MDM 进行微调，直接优化运动的物理保真度。

### 3. 主要结果

在 HumanML3D 和 KIT-ML 两个标准基准上，ReinDiffuse 在保持语义匹配能力的同时，大幅提升了物理合理性：

- **HumanML3D**：FID 从 MDM 的 0.544 降至 **0.385**（相对提升 29%）；滑步比从 0.102 降至 **0.058**（接近真实数据的 0.057）；浮空高度从 1.757 m 降至 **0.711 m**；地面穿透和脚部截交完全消除（降至 0.000）。
- **KIT-ML**：FID 从 0.494 降至 **0.326**（相对提升 34%），四项物理指标同样接近真实数据水平。

消融实验表明，固定标准差 σ=0.15 时取得最佳 FID，物理指标对 σ 变化不敏感，始终保持极低水平。

### 4. 方法谱系与知识库定位

ReinDiffuse 位于**文本驱动运动扩散模型**与**强化学习微调**的交叉点：

- **上游基础**：继承了 MDM 的编码器-仅变压器去噪扩散架构，以预测去噪后运动 $x_0$ 为目标（公式 $\mathcal{L}_{\text{simple}}$）。
- **关键改造**：将确定性输出重新解释为策略分布的均值，引入固定标准差形成随机动作策略，使扩散模型可接受 RL 训练。这一改造无需修改网络结构。
- **与现有工作的关系**：
  - 相较于 **T2M**（Guo et al., CVPR 2022）和 **MotionDiffuse**（Zhang et al., arXiv 2022）等纯扩散方法，ReinDiffuse 首次将物理合理性作为显式优化目标。
  - 相较于 **PhysDiff**（Yuan et al., ICCV 2023）等基于物理模拟器的方法，ReinDiffuse 不依赖外部物理引擎，仅通过关节位置奖励即可高效微调。
- **知识库贡献**：验证了“扩散模型输出分布 + 物理奖励 + PPO 微调”这一范式在运动生成中的有效性，为后续研究提供了可复用的技术路径。

### 5. 局限与开放问题

- **奖励设计依赖人工**：每类物理问题需手动设计奖励函数，面对多样化的物理约束时工作量较大。
- **关节级评估的盲区**：物理奖励仅基于关节点位置计算，无法捕获网格层面的细粒度物理错误（如手与身体的穿透）。
- **开放方向**：能否设计自动化的物理奖励生成机制？能否在高效网格或隐式表面表示上进行物理合理性评估而不显著增加训练成本？若将物理奖励与语义对齐奖励联合优化，是否能同时提升动作真实性和文本贴合度？

### 问题背景

文本驱动的人体运动生成旨在根据自然语言描述合成逼真的三维人体动作序列，在动画制作、虚拟现实和具身智能等领域具有重要应用价值。近年来，扩散模型在该任务上取得了显著进展，以 **MDM**（Tevet et al., arXiv 2022）为代表的运动扩散模型在语义匹配和生成多样性上展现出强大的能力。

然而，现有方法存在一个关键瓶颈：**它们仅从数据分布中学习运动模式，缺乏对物理常识的显式建模**。这导致生成的运动虽然语义上合理，但在物理层面常常违反基本约束，出现以下四类典型问题：

- **滑步（Skating）**：脚部在有地面接触时发生非自然的滑动。
- **浮空（Floating）**：身体或脚部悬空，未与地面保持合理接触。
- **地面穿透（Ground Penetration）**：脚部或身体部位穿过地面。
- **脚部截交（Foot Clipping）**：左右脚相互穿透或穿插。

这些问题严重影响了生成运动在视觉上的可信度和实际应用价值。

### 现有方法缺口

现有的改进思路主要包括两类：

1. **基于物理模拟的后处理**：如 **PhysDiff**（Yuan et al., ICCV 2023）在扩散模型的去噪过程中引入物理模拟器进行约束。这类方法依赖外部物理引擎，计算开销大，且模拟器与生成模型的耦合增加了系统复杂度。

2. **几何损失辅助训练**：MDM 本身支持在预测 $\mathbf{x}_0$ 时叠加几何损失（如脚部接触损失），但这种静态监督信号难以充分捕捉时序上的物理一致性，效果有限。

上述方法均未从根本上解决扩散模型“不理解物理常识”的问题——模型仍然只是在模仿数据，而非真正学习到物理约束。

### 本文动机

本文的核心动机是：**能否在不修改网络结构、不引入物理模拟器的前提下，使运动扩散模型学会生成物理合理的动作？**

这需要解决两个关键挑战：

1. **接口兼容性**：扩散模型的输出是确定性的运动序列，而强化学习（RL）要求策略输出动作分布。如何将两者桥接，使扩散模型能够接受 RL 训练？
2. **奖励设计**：如何设计简洁有效的奖励函数，在不依赖物理模拟器的情况下，量化运动序列的物理合理性？

ReinDiffuse 的提出正是为了应对上述挑战：通过重新参数化将 MDM 的输出转化为高斯动作分布，使其兼容 RL 框架；同时设计基于关节位置的四类物理奖励函数，利用 PPO 对预训练 MDM 进行微调，直接优化动作的物理保真度。

## 核心方法与创新机理

ReinDiffuse 的核心创新在于**将运动扩散模型重新解释为强化学习中的连续动作策略**，从而在不修改网络结构的前提下，直接优化生成动作的物理合理性。这一思路通过两个关键设计实现：

### 1. 从确定性输出到随机动作策略的重新参数化

现有运动扩散模型（如 **MDM**，Tevet et al., arXiv 2022）在每一步扩散中直接预测去噪后的确定性运动序列 $x_0$，其训练目标仅为最小化预测误差：

$$\mathcal{L}_{\mathrm{simple}} = \mathbb{E}_{x_0 \sim D, t \sim [1,T]} [\| x_0 - G(\epsilon_t, t, c) \|_2^2]$$

这种确定性输出无法直接嵌入强化学习框架，因为 RL 要求策略能够输出动作分布以支持探索和梯度估计。ReinDiffuse 的解决方案是**重新参数化**：将 MDM 的输出 $x_0$ 解释为高斯动作分布的均值 $\mu(x_0)$，并引入一个固定的标准差 $\sigma$ 构建随机策略：

$$a = \mu(\boldsymbol{x}_0) + \boldsymbol{\sigma} \cdot \boldsymbol{v}$$

其中 $\boldsymbol{v}$ 为独立噪声。这一改动使得 MDM 的输出从“预测值”转变为“动作分布的参数”，从而使整个扩散模型可以像连续动作策略一样接受 PPO 训练。消融实验表明，$\sigma=0.15$ 时取得最佳 FID（0.385），过大或过小的 $\sigma$ 均导致性能下降，$\sigma=0.3$ 时训练甚至无法收敛（Table 3）。

### 2. 基于关节位置的物理合理性奖励设计

传统的物理合理性方法通常依赖物理模拟器进行约束，计算开销大且难以与扩散模型的训练流程耦合。ReinDiffuse 另辟蹊径，**直接基于动作序列的关节位置设计四类逐帧奖励函数**，无需物理模拟器即可高效评估和优化物理保真度：

- **滑步奖励** $R_{\mathrm{s}}^i(a)$：惩罚相邻帧间脚部位置在接触标签 $f_S$ 为 1 时的滑动，鼓励脚部在有地面接触时保持静止：
  $$R_{\mathrm{s}}^i(a) = \exp(-\| (a_{ft}^i - a_{ft}^{i-1}) \cdot f_S^i \cdot f_S^{i-1} \|_2)$$

- **浮空奖励** $R_{\mathrm{F}}^i(a)$：当脚的最低高度大于地面高度时（$f_F^i=1$），惩罚脚与地面的分离，避免浮空：
  $$R_{\mathrm{F}}^i(a) = \exp(-\| (a_h^i - h_{ground}) \cdot f_F^i \|_2)$$

- **地面穿透奖励** $R_{\mathrm{P}}^i(a)$：当脚的最低高度小于地面高度时（$f_P^i=1$），惩罚脚穿透地面：
  $$R_{\mathrm{P}}^i(a) = \exp(-\| (h_{ground} - a_h^i) \cdot f_P^i \|_2)$$

- **脚部截交奖励** $R_{\mathrm{C}}^i(a)$：当左右脚距离小于阈值时（$f_C^i=1$），惩罚双脚相互穿透或穿插：
  $$R_{\mathrm{C}}^i(\boldsymbol{a}) = \exp(-\| (a_{lf}^i - a_{rf}^i) \cdot f_C^i \|_2)$$

四类奖励累加形成逐帧总奖励 $R^i(a)$，通过 PPO 的裁剪替代目标进行策略更新：

$$\mathcal{L}_{PPO}(\theta) = \mathbb{E}\left[ \min(r_i(\theta) R_i, \operatorname{clip}(r_i(\theta), 1-\gamma, 1+\gamma) R_i) \right]$$

其中 $r_i(\theta) = \frac{\pi_{\theta}^{RL}(a|\epsilon_t, t, c, \sigma)}{\pi_{\theta}^{PT}(a|\epsilon_t, t, c, \sigma)}$ 是新旧策略的概率比，用于重要性采样。最终训练目标为组合损失 $\mathcal{L} = \mathcal{L}_{PPO} + \lambda \mathcal{L}_{simple}$，在优化物理奖励的同时保留原始扩散模型的生成质量。

### 创新效果

这两项设计使 ReinDiffuse 在 HumanML3D 上将 FID 从 MDM 的 0.544 降至 0.385（相对提升 29%），在 KIT-ML 上从 0.494 降至 0.326（相对提升 34%）。物理合理性指标大幅改善：滑步比从 0.102 降至 0.058，浮空高度从 1.757 m 降至 0.711 m，地面穿透和脚部截交完全消除（降至 0.000），各项指标均接近真实数据分布（Table 1, Table 2）。

ReinDiffuse 的训练框架将预训练运动扩散模型（MDM）重新解释为强化学习中的随机策略，在不修改网络结构的前提下，通过物理奖励驱动的策略优化实现物理合理性的注入。整体流程如 Figure 2 所示，由五个核心模块串联构成闭环。

![[assets/figures/papers/paper_list_l2_https_arxiv_org_abs_2410_07296/figures/002_Figure_2.jpg]]
*Figure 2: Overview of our ReinDiffuse training framework. Given the condition c, time step t and noised motion*

**输入与初始预测。** 给定文本条件 $c$、扩散时间步 $t$ 和加噪运动 $\epsilon_t$，MDM 的编码器-仅变压器网络直接预测去噪后的运动序列 $\boldsymbol{x}_0$。这一预测在原始 MDM 中是确定性输出，充当后续策略构建的起点。

**重新参数化模块。** 框架的关键创新在于将确定性输出 $\boldsymbol{x}_0$ 转化为高斯动作分布的均值 $\mu(\boldsymbol{x}_0)$，并引入固定的标准差 $\sigma$，通过 $a = \mu(\boldsymbol{x}_0) + \sigma \cdot \boldsymbol{v}$（$\boldsymbol{v}$ 为独立噪声）采样得到动作 $a$。这一重新参数化使扩散模型的输出兼容强化学习的连续动作策略要求，是连接生成模型与 RL 范式的“因果旋钮”。

**双策略架构。** 系统维护两个策略网络：预训练策略 $\pi_{PT}$ 负责从高斯分布中采样多样化的动作序列，用于计算物理奖励和动作似然 $p(a)$；RL 策略 $\pi_{RL}$ 则通过重要性采样与 PPO 更新进行梯度优化。两者共享相同的 MDM 网络权重，但 $\pi_{PT}$ 保持冻结，仅 $\pi_{RL}$ 参与训练更新。

**物理奖励计算器。** 基于采样得到的动作序列，模块逐帧计算关节位置，并针对滑步、浮空、地面穿透和脚部截交四类非物理行为分别计算奖励（公式 4–7），累加得到总奖励 $R$。奖励函数全部基于关节高度和脚部接触标签设计，无需物理模拟器。

**PPO 训练模块。** 最终训练采用组合损失 $\mathcal{L} = \mathcal{L}_{PPO} + \lambda \mathcal{L}_{simple}$，其中 $\mathcal{L}_{PPO}$ 是带裁剪的 PPO 替代目标（公式 8），$\mathcal{L}_{simple}$ 是 MDM 原有的预测均方误差损失（公式 1）。PPO 通过重要性采样比率 $r_i(\theta) = \pi_{RL}(a|\cdot) / \pi_{PT}(a|\cdot)$ 约束策略更新幅度，在最大化物理奖励的同时防止策略崩溃，保持运动质量不退化。

整个 pipeline 的核心因果机制在于：通过重新参数化将扩散模型的输出空间转化为可优化的策略空间，再以物理奖励为信号引导策略向物理合理的方向偏移，而 $\mathcal{L}_{simple}$ 的保留则确保语义对齐能力不被遗忘。

ReinDiffuse 的核心在于将运动扩散模型 MDM 的输出重新解释为随机策略，从而在不修改网络结构的前提下，使其兼容强化学习框架。整个训练流程由五个关键模块构成，如 Figure 2 所示。

### 3.1 运动扩散模型 (MDM) 基础

MDM 采用编码器-仅变压器架构，在扩散过程中直接预测去噪后的运动序列 $x_0$，而非预测噪声。其训练目标为简单损失：

$$\mathcal{L}_{\mathrm{simple}} = \mathbb{E}_{x_0 \sim D, t \sim [1, T]} [\| x_0 - G(\epsilon_t, t, c) \|_2^2] \tag{1}$$

其中 $G$ 为去噪网络，$\epsilon_t$ 为第 $t$ 步的加噪运动，$c$ 为文本条件。该公式允许在每个扩散步上叠加几何损失进行监督。

### 3.2 重新参数化模块：从确定性输出到随机策略

标准 MDM 输出的是确定性运动序列，无法直接作为强化学习中的动作策略。ReinDiffuse 通过重新参数化解决这一瓶颈：

$$a = \mu(x_0) + \sigma \cdot v \tag{3}$$

核心操作：将 MDM 的预测输出 $x_0$ 映射为高斯动作分布的均值 $\mu(x_0)$，并引入固定的标准差 $\sigma$ 与独立噪声 $v$（从标准正态分布采样）。采样得到的动作 $a$ 即为服从分布 $\mathcal{N}(\mu(x_0), \sigma^2)$ 的随机运动序列，使扩散模型具备了连续动作策略的概率特性。

### 3.3 预训练策略与 RL 策略的双轨设计

框架维护两个策略实例（Figure 2）：
- **预训练策略 $\pi_{PT}$**：冻结的 MDM 权重，负责采样多样化动作并计算物理奖励，提供重要性采样的基准分布。
- **RL 策略 $\pi_{RL}$**：待优化的目标策略，通过 PPO 进行梯度更新，其与 $\pi_{PT}$ 共享同一网络结构但权重独立。

### 3.4 物理奖励计算器：四类逐帧奖励函数

基于动作序列中提取的关节点位置，设计四项物理合理性奖励，每帧的总奖励为四项之和 $R^i(a)$。所有奖励函数均采用指数形式，输出范围 $(0,1]$，物理越合理则奖励越接近 1。

**滑步奖励 (Sliding Steps)**：惩罚相邻帧间脚部在接触地面时的滑动。

$$R_{\mathrm{s}}^i(a) = \exp(-\| (a_{ft}^i - a_{ft}^{i-1}) \cdot f_S^i \cdot f_S^{i-1} \|_2) \tag{4}$$

其中 $a_{ft}^i$ 为第 $i$ 帧的脚部关节点位置，$f_S^i$ 为接触标签（脚部高度低于阈值且速度低于阈值时为 1）。该设计确保脚部在有地面接触时保持静止，消除"滑步"现象。

**浮空奖励 (Floating)**：惩罚脚部脱离地面。

$$R_{\mathrm{F}}^i(a) = \exp(-\| (a_h^i - h_{ground}) \cdot f_F^i \|_2) \tag{5}$$

$f_F^i = 1$ 当脚部最低高度 $a_h^i$ 大于地面高度 $h_{ground}$ 时激活，惩罚脚与地面的不必要分离。

**地面穿透奖励 (Ground Penetration)**：惩罚脚部穿透地面。

$$R_{\mathrm{P}}^i(a) = \exp(-\| (h_{ground} - a_h^i) \cdot f_P^i \|_2) \tag{6}$$

$f_P^i = 1$ 当脚部最低高度小于地面高度时激活，维持物理交互的完整性。

**脚部截交奖励 (Foot Clipping)**：惩罚左右脚相互穿透。

$$R_{\mathrm{C}}^i(a) = \exp(-\| (a_{lf}^i - a_{rf}^i) \cdot f_C^i \|_2) \tag{7}$$

$f_C^i = 1$ 当左右脚距离小于阈值时激活，防止双脚穿插。

### 3.5 PPO 训练模块：组合损失优化

强化学习的基本目标为最大化策略在轨迹上的累积奖励期望：

$$\mathcal{L}_{\mathrm{RL}} = \mathbb{E}_{\tau \sim p(\cdot|\pi)} [R(\tau)] \tag{2}$$

ReinDiffuse 采用 PPO 算法进行稳定策略更新，其裁剪替代目标为：

$$\mathcal{L}_{PPO}(\theta) = \mathbb{E}\left[ \min(r_i(\theta) R_i, \operatorname{clip}(r_i(\theta), 1 - \gamma, 1 + \gamma) R_i) \right] \tag{8}$$

其中概率比 $r_i(\theta)$ 定义为 RL 策略与预训练策略在给定动作上的似然比：

$$r_i(\theta) = \frac{\pi_{\theta}^{RL}(a | \epsilon_t, t, c, \sigma)}{\pi_{\theta}^{PT}(a | \epsilon_t, t, c, \sigma)}$$

PPO 裁剪系数 $\gamma = 0.2$ 限制每次更新的幅度，防止策略崩溃。最终训练使用组合损失：

$$\mathcal{L} = \mathcal{L}_{PPO} + \lambda \mathcal{L}_{simple}$$

其中 $\lambda = 0.4$ 平衡物理奖励优化与原始扩散模型的数据分布保真度。

![[assets/figures/papers/paper_list_l2_https_arxiv_org_abs_2410_07296/figures/001_Figure_1.jpg]]
*Figure 1: Our ReinDiffuse can generate physically plausible motion, effectively eliminating common physical issues such as floating, penetration, foot clipping, and skating. ReinDiffuse enables MDM to learn physical commonsense with reinforcement learning*

## 实验与关键发现

### 主实验结果

ReinDiffuse 在两个标准文本驱动运动生成基准上均取得了显著优于基线 MDM 的性能，并在物理合理性指标上实现了质的飞跃。

**HumanML3D 数据集**（Table 1）：ReinDiffuse 将 FID 从 MDM 的 0.544 降至 **0.385**，相对提升 **29.2%**，表明生成运动的整体质量与真实分布更为接近。语义对齐指标 R-Precision 也从 0.611 小幅提升至 **0.622**，说明物理合理性的增强并未以牺牲文本匹配为代价。四项物理指标均大幅改善：滑步比（Skate ratio）从 0.102 降至 **0.058**，与真实数据的 0.057 几乎一致；浮空高度（Float）从 1.757 m 降至 **0.711 m**，接近真实值的 0.704 m；地面穿透（Penetrate）和脚部截交（Clip）则从 0.048 m 和 0.014 m 完全消除至 **0.000**。

**KIT-ML 数据集**（Table 2）：ReinDiffuse 展现了良好的跨数据集泛化能力。FID 从 MDM 的 0.494 降至 **0.326**，相对提升 **34.0%**。物理指标同样全面改善：滑步比从 0.122 降至 **0.087**（真实值 0.085），浮空高度从 1.836 m 降至 **0.938 m**（真实值 0.930 m），地面穿透和脚部截交均降至 **0.000**。

**与现有方法的对比**：在 HumanML3D 上，ReinDiffuse 的 FID（0.385）优于 T2M（Guo et al., CVPR 2022）的 1.067、MotionDiffuse（Zhang et al., arXiv 2022）的 0.630、MDM（Tevet et al., arXiv 2022）的 0.544，以及基于物理模拟的 PhysDiff（Yuan et al., ICCV 2023）的 0.433。值得注意的是，ReinDiffuse 无需依赖物理模拟器即可在 FID 上超越 PhysDiff，同时将地面穿透和脚部截交完全消除，而 PhysDiff 在这两项上仍有残留（分别为 0.026 和 0.005）。

### 消融实验

**固定标准差 σ 的影响**（Table 3）：重新参数化模块中引入的固定标准差 σ 是控制策略探索程度的关键超参数。实验表明，σ = 0.15 时取得最佳 FID（0.385）。当 σ 过小（0.05）时，策略的随机性不足，FID 升至 0.407；当 σ 过大（0.3）时，训练无法收敛，FID 恶化至 0.447。这一现象揭示了探索与利用的经典权衡：适度的随机性使 RL 策略能够在保持语义质量的同时探索物理合理的动作空间，而过度探索则破坏了 MDM 原本学到的运动分布。值得注意的是，四项物理指标对 σ 的变化不敏感，始终维持在极低水平，说明物理奖励的设计本身具有鲁棒性，即使 FID 因 σ 不当而上升，物理合理性仍能得到保障。

**RL 微调框架的有效性**：综合 Table 1、Table 2 和 Table 3 的结果，从 MDM 预训练权重出发，仅通过 PPO 结合物理奖励进行微调，即可在运动质量（FID）和物理合理性两个维度上同时取得显著提升。这验证了核心洞察：将扩散模型的确定性输出重新参数化为高斯动作分布，使其兼容 RL 框架，是一条在不修改网络结构的前提下注入物理常识的有效路径。

### 定性分析

Figure 1 和 Figure 3 从视觉层面印证了定量结果。Figure 1 展示了 ReinDiffuse 对四种典型非物理行为的消除效果：MDM 生成的动作中常见脚部悬浮于地面之上（浮空）、双脚相互穿透（截交）、脚部陷入地面以下（穿透）以及支撑脚在地面上滑动（滑步），而 ReinDiffuse 的输出在这些问题上均得到了根本性改善。Figure 3 通过轨迹可视化进一步展示了运动质量的变化，颜色越深表示时间越晚的帧，ReinDiffuse 的轨迹更加平滑自然，与 MDM 的抖动和不连续形成鲜明对比。

![[assets/figures/papers/paper_list_l2_https_arxiv_org_abs_2410_07296/figures/006_Figure_3.jpg]]
*Figure 3: Visual results of ReinDiffuse against the MDM. The darker colors indicate the later frame in time*

### 失败模式与局限性

尽管 ReinDiffuse 在关节层面的物理合理性上取得了显著成效，但仍存在以下局限：

1. **奖励函数设计的手动依赖性**：当前框架需要针对每一类物理问题手动设计奖励函数。当面临更多种类的物理约束时，逐一设计奖励的工作量较大，缺乏自动化或可推广的机制。
2. **关节层面评估的粒度限制**：物理奖励仅基于关节位置计算，无法捕获网格（mesh）层面的细粒度物理错误，例如手部与身体其他部位的穿透。受计算资源限制，训练阶段无法使用网格数据计算物理奖励，可能遗漏部分视觉上不合理但关节层面未违反约束的情况。
3. **σ 的敏感性**：消融实验表明，固定标准差 σ 对 FID 有显著影响，σ = 0.3 时训练无法收敛。这提示重新参数化策略对超参数选择较为敏感，在实际部署中可能需要针对不同数据集或模型规模进行调优。

### 公平性说明

所有对比方法均在 HumanML3D 和 KIT-ML 数据集的标准训练/测试划分下评估，ReinDiffuse 从 MDM 官方预训练权重开始微调，确保对比的公平性。物理指标的阈值设定（如滑步检测的 2.5 cm 位移阈值和 5 cm 高度阈值）与 PhysDiff 等先前工作保持一致，具有可比性。

![[assets/figures/papers/paper_list_l2_https_arxiv_org_abs_2410_07296/figures/003_Table_1.jpg]]
*Table 1: Text-to-motion results on HumanML3D [8]. → means closer to real is better. Bold indicate the best results*

![[assets/figures/papers/paper_list_l2_https_arxiv_org_abs_2410_07296/figures/004_Table_2.jpg]]
*Table 2: Text-to-motion results on and KIT-ML [31]. → means closer to real is better. Bold indicate the best results*

![[assets/figures/papers/paper_list_l2_https_arxiv_org_abs_2410_07296/figures/005_Table_3.jpg]]
*Table 3: Effect of varying standard deviation σ in RL fine-tuning on HumanML3D [8]*

## 定位与知识库关联

### 1. 与基线方法的关系

ReinDiffuse 直接建立在 **MDM**（Tevet et al., arXiv 2022）之上，将 MDM 作为其预训练运动扩散模型的核心组件。MDM 在文本驱动运动生成领域以语义匹配和多样性见长，但其生成的运动常常违反物理常识——滑步、浮空、地面穿透和脚部截交等问题频繁出现。ReinDiffuse 的核心贡献在于**不修改 MDM 的网络结构**，而是通过重新参数化将 MDM 的确定性输出转化为高斯动作分布，使其兼容强化学习范式，从而用 PPO 算法对预训练权重进行物理感知微调。

与 **T2M**（Guo et al., CVPR 2022）和 **MotionDiffuse**（Zhang et al., arXiv 2022）等文本驱动运动生成方法相比，ReinDiffuse 的独特之处在于显式引入了物理合理性约束。T2M 和 MotionDiffuse 主要关注文本-运动语义对齐和生成多样性，但未对物理保真度进行专门优化。ReinDiffuse 通过四类基于关节位置的物理奖励函数（滑步、浮空、地面穿透、脚部截交），在不依赖物理模拟器的情况下实现了物理合理性的显著提升。

与 **PhysDiff**（Yuan et al., ICCV 2023）形成有趣的对比：PhysDiff 采用物理模拟器作为后处理步骤，在扩散模型生成运动后通过物理仿真进行修正。而 ReinDiffuse 则将物理约束直接融入扩散模型的训练过程，通过 RL 微调使模型内化物理常识。这两种路径代表了“物理感知运动生成”的不同设计哲学——外置物理修正 vs. 内置物理学习。

### 2. 适用边界

ReinDiffuse 的适用边界由以下几个关键设计选择划定：

- **关节级物理约束**：物理奖励函数完全基于关节点位置计算（脚部接触标签、脚部高度、左右脚距离等），因此只能捕获和纠正关节层面的物理违规。对于网格（mesh）层面的细粒度物理错误（如手与身体的穿透、衣物与身体的交互），该方法无法提供保证。论文明确承认这一局限。

- **固定标准差策略**：重新参数化模块使用固定的标准差 σ 构建高斯动作分布，而非学习自适应的方差。消融实验（Table 3）表明，σ=0.15 时取得最佳 FID（0.385），过大（σ=0.3）会导致训练无法收敛，过小（σ=0.05）则限制探索空间。这意味着该方法对 σ 的选择较为敏感，最优值可能需要针对不同数据集手动调整。

- **计算资源约束**：由于训练阶段无法基于网格数据计算物理奖励，该方法对视觉上不合理但关节层面未违反约束的情况存在盲区。这限制了其在需要高保真物理交互（如手-物体接触、多人交互）的场景中的应用。

- **文本-运动对齐的保持**：ReinDiffuse 在提升物理合理性的同时，R-Precision 从 MDM 的 0.611 略微提升至 0.622，表明物理奖励并未损害语义对齐。但论文未探索物理奖励与语义对齐奖励的联合优化，这可能是进一步提升文本-运动一致性的方向。

### 3. 局限与开放问题

**已知局限**：

1. **奖励函数设计的手动性**：每类物理问题需要手动设计对应的奖励函数。当面临多种物理问题时，奖励设计的工作量较大，且需要领域知识来定义合适的惩罚形式和阈值。

2. **关节级评估的粒度限制**：物理奖励仅基于关节点位置，无法捕获网格层面的物理错误。论文明确指出“手与身体的穿透”等细粒度问题不在当前方法的处理范围内。

3. **固定标准差的敏感性**：σ 的选择对训练稳定性和最终性能有显著影响，σ=0.3 时训练无法收敛，这表明该超参数需要谨慎调优，缺乏自适应性。

**开放问题**：

1. **奖励函数的自动化生成**：能否设计一套自动或可推广的机制来生成物理奖励函数，以减少对不同物理问题的手动配置？这涉及物理常识的形式化表示和自动奖励塑形技术。

2. **高效网格级物理评估**：如何在高效的网格或隐式表面表示上进行物理合理性评估，而不过多增加训练成本？这需要在物理保真度和计算效率之间找到新的平衡点。

3. **物理与语义的联合优化**：若将物理奖励与语义对齐奖励（如文本-动作匹配）联合优化，是否能同时提升动作的真实性和对描述的贴合度？这涉及多目标强化学习中奖励权重的自动平衡问题。

4. **跨数据集泛化的 σ 自适应**：固定标准差 σ 的最优值是否依赖于数据集的运动特性？能否设计一种机制，使 σ 在微调过程中根据数据分布自动调整？

### 4. 知识库定位

ReinDiffuse 在方法谱系中占据 **“扩散模型 + 强化学习”** 的交叉位置，其核心知识贡献包括：

- **方法论贡献**：首次证明可以将运动扩散模型的确定性输出重新解释为动作分布的均值，通过引入固定标准差构建随机策略，使扩散模型兼容 PPO 等策略梯度算法。这一重新参数化技巧为其他生成模型（如图像、音频扩散模型）的 RL 微调提供了可迁移的思路。

- **物理常识编码**：四类基于关节位置的物理奖励函数（公式 4-7）构成了一个轻量级的物理常识编码方案。这些奖励函数不依赖物理模拟器，计算高效，且能有效消除滑步、浮空、穿透和截交四类常见非物理行为。

- **训练范式创新**：PPO 损失与 MDM 简单损失的组合训练（$L = L_{PPO} + \lambda L_{simple}$）实现了物理保真度与运动质量的平衡。重要性采样机制（公式 9）使 RL 策略在更新时能够利用预训练策略的采样结果，提高了样本效率。

该工作为“物理感知生成模型”领域提供了一个新的基准：在 HumanML3D 上 FID 从 0.544 降至 0.385（29% 提升），在 KIT-ML 上从 0.494 降至 0.326（34% 提升），同时将滑步比、浮空高度等物理指标推向真实数据水平，地面穿透和脚部截交完全消除。这些结果表明，将物理常识以奖励函数形式注入扩散模型的 RL 微调过程，是一种有效且可推广的策略。

## 原文 PDF

![[paperPDFs/WACV_2025/ReinDiffuse:_Crafting_Physically_Plausible_Motions_with_Reinforced_Diffusion_Model.pdf]]
