---
title: "PvP: Data-Efficient Humanoid Robot Learning with Proprioceptive-Privileged Contrastive Representations"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/PvP_Data_Efficient_Humanoid_Robot_Learning_with_Proprioceptive_Privileged_Contrastive_Representations.pdf
project_link: null
code_link: null
aliases:
- PvP
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/representation_self_supervised_transfer
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: 在本体感知状态（可直接测量）与特权状态（仅模拟器中可用）之间引入对比学习，迫使策略编码器学习紧凑且任务相关的表征，从而提升样本效率。
primary_logic: 利用本体感知与特权状态的内在互补性，通过 SimSiam 风格的对比学习（含零遮罩和停梯度）替代手工数据增强，使表征与策略协同进化，在无需额外复杂组件的情况下显著加快学习并改善最终性能。
claims:
- PvP 在速度跟踪和动作模仿两个主任务上，训练效率显著优于 PPO 及其他 SRL 基线，收敛曲线更高且更快
- PvP 在动作平滑度优化上收敛速度明显快于所有对比方法，有利于实机部署
- 在动作模仿任务的三个关键跟踪指标上，PvP 均取得最高性能
- 消融实验表明 PvP 优于教师-学生蒸馏方法，且对不同机器人平台和粗糙地形具有良好泛化性
---

# PvP: Data-Efficient Humanoid Robot Learning with Proprioceptive-Privileged Contrastive Representations

> [!tip] 核心洞察
> 利用本体感知与特权状态的内在互补性，通过 SimSiam 风格的对比学习（含零遮罩和停梯度）替代手工数据增强，使表征与策略协同进化，在无需额外复杂组件的情况下显著加快学习并改善最终性能。

| 字段 | 内容 |
|------|------|
| 中文题名 | PvP：基于本体感知-特权对比表征的数据高效人形机器人学习 |
| 英文题名 | PvP: Data-Efficient Humanoid Robot Learning with Proprioceptive-Privileged Contrastive Representations |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2512.13093) |
| Topic | #topic/vision_multimodal_applications #topic/representation_self_supervised_transfer #topic/vision_multimodal_applications/image_and_video_generation |
| Method | PvP |
| Dataset | LimX-Oli-31dof-Velocity, LimX-Oli-31dof-Mimic |

> [!tip] 效果简介
> - LimX-Oli-31dof-Velocity 上，综合奖励（所有子奖励加权求和） PvP (最高奖励，收敛最快) vs PPO (vanilla) (显著提升)；动作平滑度惩罚项 PvP (收敛最快，惩罚项下降最快) vs PPO (vanilla) (明显加速收敛)。
> - LimX-Oli-31dof-Mimic 上，综合奖励 PvP (最高奖励) vs PPO (vanilla) (大幅提升；其他 SRL 方法提升有限或退化)；三个关键跟踪指标 PvP (全部指标最高) vs PPO 及其他 SRL 方法 (在所有跟踪指标上均最优)。

## 概述

人形机器人的全身控制（Whole-Body Control, WBC）是实现灵巧运动与操作的基础，但其高维动作空间、复杂接触动力学以及部分可观测性，使得基于无模型强化学习（RL）的策略训练面临严重的样本效率瓶颈。在仅依赖本体感知（proprioceptive）状态——如关节角度、角速度、IMU 读数——的条件下，标准 PPO 算法往往需要海量交互步数才能收敛，甚至在某些任务上完全无法学习有效策略。

本文提出 **PvP（Proprioceptive-Privileged Contrastive Representations）**，一种通用、简洁且高效的表征学习框架，旨在从根本上缓解上述样本效率问题。PvP 的核心思想是：利用本体感知状态（可直接部署于真实机器人）与特权状态（privileged state，仅在仿真器中可获取，如根线速度、根姿态等）之间的内在互补性，通过对比学习迫使策略编码器学习紧凑且任务相关的潜在表征。与依赖手工数据增强（如高斯噪声、随机遮罩）的传统自监督表征学习（SRL）方法不同，PvP 通过对特权信息部分进行**零遮罩（Zero-Masking）** 来构造对比正样本对，无需任何人工设计的增强策略。

在方法定位上，PvP 基于 **SimSiam** 风格的对比学习范式，采用对称的负余弦相似度损失配合停梯度（stop-gradient）操作，避免了对比学习中常见的模式坍塌问题。同时，PvP 引入**间隔更新机制**：SRL 损失并非在每个 RL 更新步都施加，而是每隔 $T$ 步周期性作用，防止训练早期低质量数据将表征学习引入局部最优。整个框架被封装为 **SRL4Humanoid**——一个将 SRL 与 RL 过程完全解耦的模块化工具包，使 PvP 可以即插即用地与 PPO 骨干组合。

实验在两个核心人形机器人全身控制任务上进行：**速度跟踪（Velocity Tracking）** 和 **动作模仿（Motion Imitation）**，机器人平台为 LimX Oli（31 自由度）。主要结果如下：

- **样本效率与最终性能**：在速度跟踪与动作模仿两个任务上，PvP 的训练收敛速度和最终综合奖励均显著优于 vanilla PPO，也明显超越 **VAE**（重建式 SRL）、**SPR**（动力学建模式 SRL）和 **SimSiam**（对比式 SRL）等基线方法。尤其在动作模仿任务上，其他 SRL 方法提升有限甚至出现性能退化，而 PvP 保持稳定且显著的增益（Figure 5）。
- **动作平滑度**：PvP 在动作平滑度惩罚项的下降速度上明显快于所有对比方法，这对于降低实机部署时的关节冲击和能耗至关重要（Figure 6）。
- **跟踪精度**：在动作模仿任务的三个关键跟踪指标上，PvP 均取得最高性能（Figure 7）。
- **泛化性与鲁棒性**：消融实验表明，PvP 优于传统的教师-学生蒸馏方法（Figure 13, 14），且在不同机器人平台（Unitree G1, 29 自由度）和粗糙地形条件下均表现出良好的泛化能力（Figure 15, 16）。

PvP 的成功揭示了本体感知与特权状态之间的互补性是一种无需额外标注或复杂组件的强监督信号，通过简洁的对比学习即可显著加速人形机器人策略学习。

## 背景与动机

### 人形机器人全身控制的挑战

人形机器人的全身控制（Whole-Body Control, WBC）是实现其在真实世界中自主作业的核心技术。与四足或轮式机器人不同，人形机器人拥有更高的自由度（通常超过 30 个关节自由度）、不稳定的双足支撑结构以及复杂的全身动力学耦合，这对控制策略的学习提出了严峻挑战。

近年来，深度强化学习（Deep RL）已成为人形机器人运动控制的主流范式。然而，直接将标准 RL 算法（如 PPO）应用于人形机器人 WBC 任务面临一个核心瓶颈：**样本效率极低**。具体而言：

- **高维动作空间与复杂动力学**：人形机器人的状态-动作空间维度极高，且全身动力学呈现高度非线性耦合，导致策略搜索空间巨大，随机探索难以高效覆盖有效区域。
- **部分可观测性**：在真实部署场景中，机器人仅能获取本体感知状态（proprioceptive state），如关节编码器读数、IMU 测量值等，而无法直接获取根线速度、根姿态、外部接触力等对控制至关重要的特权信息（privileged information）。这种信息缺失使得从有限的本体感知信号中推断系统完整状态变得极为困难。

### 现有表征学习方法的局限

为缓解上述样本效率问题，研究者开始将自监督表征学习（Self-Supervised Representation Learning, SRL）引入机器人 RL 训练。代表性方法包括：

- **基于重建的方法**（如 VAE）：通过编码-解码结构学习状态表征，但重建目标往往与下游任务无关，可能保留大量任务无关信息。
- **基于动力学建模的方法**（如 SPR）：通过预测未来状态学习时序表征，但在高维人形机器人场景中，动力学预测本身极为困难，可能引入额外噪声。
- **基于对比学习的方法**（如 SimSiam）：通过数据增强构造正样本对进行对比学习，但通常依赖手工设计的数据增强策略（如高斯噪声、随机遮罩），这些增强操作可能与物理系统的真实变化规律不一致。

这些方法存在一个共同的深层缺陷：**它们均未有效利用模拟器训练阶段天然可用的特权状态信息**。在模拟器中，根线速度、地面反力、外部扰动等特权状态可以精确获取，但这些信息在现有 SRL 范式中或被完全忽略，或仅通过教师-学生蒸馏（teacher-student distillation）间接传递，导致表征学习缺乏明确的任务相关性指导。

### PvP 的核心动机

针对上述缺口，PvP（Proprioceptive-Privileged Contrastive Learning）提出了一种全新的表征学习思路：**直接在本体感知状态与特权状态之间建立对比学习关系**。

其核心洞察在于：本体感知状态（可直接测量）与特权状态（仅模拟器中可用）之间存在**内在互补性**——特权状态包含了本体感知状态所缺失的关键任务信息，而本体感知状态则是特权状态在真实部署中的唯一可观测投影。通过在两者之间施加 SimSiam 风格的对比学习（含零遮罩和停梯度操作），PvP 迫使策略编码器学习紧凑且任务相关的潜在表征，而无需依赖手工数据增强或额外的蒸馏网络。

这一设计的直接优势包括：
1. **无需手工增强**：通过对特权状态中的特权信息部分进行零遮罩（ZeroMasking）自然构造对比对，避免了物理不一致的增强操作。
2. **表征与策略协同进化**：SRL 损失直接作用于策略编码器，使表征学习与策略优化目标一致，而非独立于任务。
3. **即插即用**：PvP 可作为模块化组件嵌入标准 PPO 训练流程，无需修改 RL 算法本身。

实验表明，PvP 在速度跟踪和动作模仿两项人形机器人 WBC 任务上，训练效率和最终性能均显著优于 PPO 原生基线及 VAE、SPR、SimSiam 等主流 SRL 方法（Figure 5），验证了本体感知-特权对比学习范式的有效性。

## 核心创新

PvP 的核心创新在于将人形机器人全身控制中的**本体感知状态**与**特权状态**之间的内在互补性，转化为一种无需手工数据增强的对比学习信号，从而在 PPO 骨干上实现显著的数据效率与最终性能提升。其关键设计可归纳为以下三个 changed slots：

### 1. 对比学习目标：从单模态重建到跨模态互补

传统 SRL 方法（如 VAE、SPR）通常依赖单模态的重建或动力学建模来学习表征，而 PvP 直接在本体感知状态 $s_t$ 与其零遮罩版本 $\tilde{s}_t$ 之间构建 SimSiam 风格的对比学习目标。具体而言，通过对特权状态中的特权信息部分进行**零遮罩**（ZeroMasking），仅保留本体感知部分：
$$
\tilde{\pmb{s}}_t = \mathrm{ZeroMasking}(\pmb{s}_t)
$$
策略编码器 $f_{\pmb{\theta}}$ 和预测器 $h_{\pmb{\psi}}$ 分别对原始状态与零遮罩状态提取表征，并计算对称的负余弦相似度损失：
$$
\mathcal{L}_{\mathrm{PvP}} = D_{\mathrm{ncs}}\left(\pmb{p}, \mathbf{sg}(\tilde{\pmb{z}})\right) + D_{\mathrm{ncs}}\left(\tilde{\pmb{p}}, \mathbf{sg}(\pmb{z})\right)
$$
其中 $D_{\mathrm{ncs}}(\pmb{p}, \pmb{z}) = -\frac{\pmb{p}}{\|\pmb{p}\|_2} \cdot \frac{\pmb{z}}{\|\pmb{z}\|_2}$，$\mathbf{sg}(\cdot)$ 为停梯度操作。这一设计的核心洞察在于：零遮罩操作天然构造了一对互补的正样本——一个包含完整特权信息，另一个仅含本体感知信息——迫使编码器学习紧凑且任务相关的表征，而无需手工设计高斯噪声、随机遮罩等增强策略。

### 2. SRL 损失更新策略：间隔更新机制

与标准做法中每个 RL 更新步均施加 SRL 损失不同，PvP 引入了**间隔更新机制**：每 $T$ 步才施加一次 SRL 损失。总损失函数为：
$$
\mathcal{L}_{\mathrm{Total}} = \mathcal{L}_{\mathrm{RL}} + \mathbb{1}(T) \cdot \lambda \cdot \mathcal{L}_{\mathrm{SRL}}
$$
其中 $\mathbb{1}(T)$ 是指示函数，仅在每隔 $T$ 步时取值为 1。这一设计解决了早期训练阶段数据质量低、SRL 信号噪声大导致表征学习陷入局部最优的问题。消融实验表明，$T=50$ 时各 SRL 方法在动作模仿任务上通常表现最优（Figure 8），且 PvP 对损失权重 $\lambda$ 的敏感度可控，$\lambda=0.1$ 时最终性能与样本效率最佳（Figure 17）。

### 3. SRL 作用的编码器选择：策略编码器 vs. 价值编码器

PvP 默认将对比损失施加于**策略编码器**，而非价值编码器。实验表明，若将 SRL 损失应用于价值编码器，会导致收敛变慢甚至训练崩溃（Figure 10）。这一发现揭示了表征学习在人形机器人 RL 中的非对称性：价值函数估计需要更稳定的状态表征，而策略表征则能从跨模态对比信号中获益，二者不宜共享相同的 SRL 扰动。

### 与基线方法的本质差异

| 设计维度 | PPO (vanilla) | VAE/SPR 等 SRL 基线 | PvP |
|---------|--------------|-------------------|-----|
| SRL 目标 | 无 | 单模态重建/动力学建模 | 跨模态对比学习（本体感知 vs. 特权状态） |
| 数据增强 | 无 | 手工设计（高斯噪声、遮罩等） | 零遮罩自动构造对比对 |
| SRL 更新频率 | N/A | 每步施加 | 间隔 $T$ 步施加 |
| SRL 作用对象 | N/A | 策略或价值编码器 | 仅策略编码器 |

这些 changed slots 共同构成了 PvP 相对于基线方法的系统性优势：通过利用模拟器中天然可得的特权信息作为“免费午餐”，以极简的对比学习框架实现了训练效率的显著跃升，同时避免了手工增强设计的工程负担和教师-学生蒸馏的额外训练开销（Figure 13-14）。

## 整体框架

PvP 的核心思想是在本体感知状态（proprioceptive state）与特权状态（privileged state）之间建立对比学习，从而为策略网络学习紧凑且任务相关的表征，无需手工设计数据增强。整个框架围绕 **SRL4Humanoid** 这一模块化工具包构建，将状态表征学习（SRL）与强化学习（RL）过程完全解耦，使 PPO 骨干与多种 SRL 方法可以灵活组合。

### 状态模态与互补性

框架的输入由两类状态组成（Figure 2）：

![[assets/figures/papers/paper_list_l1050_https_arxiv_org_abs_2512_13093/figures/002_Figure_2.jpg]]
*Figure 2: An overview of the PvP approach. (a) The components of the privileged state and the proprioceptive state. (b) PvP conducts contrastive learning based on the intrinsic complementarity between the two state modalities*

- **本体感知状态**：可直接从机器人机载传感器获取，包括关节位置、关节速度、IMU 读数等。这些信息在仿真和真实部署中均可用，是策略的实际输入。
- **特权状态**：仅在仿真器中可获取的额外信息，如根线速度、根姿态、接触力、地形高度等。这些信息揭示了环境的底层动力学，但无法直接迁移到真实机器人。

PvP 利用这两类状态之间的内在互补性：特权状态蕴含丰富的任务相关信息，而本体感知状态是策略可依赖的唯一观测。通过对比学习，PvP 迫使策略编码器从本体感知状态中提取出与特权状态对齐的潜在表征，从而在不引入额外推理开销的前提下提升策略质量。

### 核心 Pipeline

PvP 的 pipeline 由以下关键模块串联（Figure 3）：

![[assets/figures/papers/paper_list_l1050_https_arxiv_org_abs_2512_13093/figures/003_Figure_3.jpg]]
*Figure 3: The architecture of the SRL4Humanoid framework, in which the SRL and RL processes are fully decoupled*

1. **零遮罩（ZeroMasking）**：对完整状态 $s_t$ 中的特权信息部分置零，仅保留本体感知观测，得到 $\tilde{s}_t$。这一操作构造了一对正样本——$s_t$ 和 $\tilde{s}_t$ 共享相同的本体感知信息，但特权信息存在差异：
   $$\tilde{\pmb{s}}_t = \mathrm{ZeroMasking}(\pmb{s}_t)$$

2. **策略编码器 $f_\theta$**：将原始状态 $s$ 和零遮罩后的 $\tilde{s}$ 分别映射为潜在表征 $z$ 和 $\tilde{z}$。该编码器同时服务于 RL 策略的动作生成和 SRL 的对比学习：
   $$z = f_{\pmb{\theta}}(s), \quad \tilde{z} = f_{\pmb{\theta}}(\tilde{s})$$

3. **对比预测头 $h_\psi$**：基于 SimSiam 架构，包含一个预测器 $h_\psi$，将编码器输出 $z$ 和 $\tilde{z}$ 进一步映射为 $\pmb{p}$ 和 $\tilde{\pmb{p}}$：
   $$\pmb{p} = h_{\pmb{\psi}}(z), \quad \tilde{\pmb{p}} = h_{\pmb{\psi}}(\tilde{z})$$

4. **PvP 对比损失**：计算对称的负余弦相似度损失，配合停梯度（stop-gradient）操作，防止模式坍塌：
   $$\mathcal{L}_{\mathrm{PvP}} = D_{\mathrm{ncs}}\left(\pmb{p}, \mathbf{sg}(\tilde{\pmb{z}})\right) + D_{\mathrm{ncs}}\left(\tilde{\pmb{p}}, \mathbf{sg}(\pmb{z})\right)$$
   其中 $D_{\mathrm{ncs}}$ 为负余弦相似度：
   $$D_{\mathrm{ncs}}(\pmb{p}, z) = -\frac{\pmb{p}}{\|\pmb{p}\|_2} \cdot \frac{z}{\|z\|_2}$$

5. **价值编码器**：独立于策略编码器，直接编码特权状态以估计状态价值。实验表明，将 SRL 损失应用于价值编码器会导致训练崩溃（Figure 10），因此 PvP 损失默认仅作用于策略编码器。

6. **间隔更新机制**：为避免训练早期低质量数据将 SRL 损失引入局部最优，PvP 引入间隔更新策略——每 $T$ 个 RL 更新步才施加一次 SRL 损失。总损失函数为：
   $$\mathcal{L}_{\mathrm{Total}} = \mathcal{L}_{\mathrm{RL}} + \mathbb{1}(T) \cdot \lambda \cdot \mathcal{L}_{\mathrm{SRL}}$$
   其中 $\mathbb{1}(T)$ 为指示函数，每 $T$ 步取值为 1，否则为 0；$\lambda$ 为 SRL 损失的权重系数。

### 与基线的关键差异

PvP 在以下三个设计维度上与现有 SRL 方法形成鲜明对比：

| 设计维度 | 基线方法 | PvP 方案 |
|---------|---------|---------|
| SRL 目标 | 重建（VAE）、动力学建模（SPR）或单模态对比（SimSiam） | 本体感知-特权跨模态对比学习 |
| 数据增强 | 手工设计的增强（高斯噪声、随机遮罩等） | 零遮罩（ZeroMasking），无需手工增强 |
| SRL 损失更新 | 每个 RL 步均计算并施加 | 间隔更新，每 $T$ 步施加一次 |

消融实验证实，间隔更新在 $T=50$ 时通常表现最优（Figure 8），而 SRL 损失权重 $\lambda=0.1$ 时 PvP 的最终性能和样本效率达到最佳（Figure 17）。此外，PvP 在速度跟踪和动作模仿任务上均显著优于教师-学生蒸馏方法（Figure 13, Figure 14），且对粗糙地形和不同机器人平台（Unitree-G1-29dof）展现出良好的泛化性（Figure 15, Figure 16）。

## 核心模块与公式推导

### 问题形式化与RL基础

人形机器人全身控制（Whole-Body Control, WBC）任务可建模为部分可观测马尔可夫决策过程（POMDP）。在每个时间步 $t$，策略 $\pi$ 接收本体感知状态（proprioceptive state）并输出动作 $\pmb{a}_t$，目标是最大化期望折扣回报：

$$J_{\pi}(\pmb \theta) = \mathbb{E}_{\pi} \Big[ \sum_{t=0}^{\infty} \gamma^{t} R(s_{t}, \pmb a_{t}, \pmb s_{t+1}) \Big]$$

其中 $\gamma$ 为折扣因子，$R$ 为奖励函数。本文以 **PPO** 作为骨干RL算法，策略网络和价值网络均采用编码器-头结构：编码器将输入状态映射为潜在表征，头网络据此生成动作分布或状态价值估计。

### PvP对比学习核心

PvP 的核心思想是利用**本体感知状态**（可直接测量，如关节位置、速度、IMU读数）与**特权状态**（仅在模拟器中可用，如根线速度、根姿态、接触力等）之间的内在互补性，通过对比学习迫使策略编码器学习紧凑且任务相关的表征。

#### 零遮罩构造正样本对

给定完整状态 $\pmb{s}_t$（包含本体感知和特权信息两部分），通过**零遮罩**（ZeroMasking）操作将特权信息部分置零，仅保留本体感知部分，构造对比学习的正样本对：

$$\tilde {\pmb{s}} _ {t} = \mathrm{ZeroMasking} ( \pmb{s} _ {t} )$$

零遮罩替代了传统对比学习中手工设计的数据增强（如高斯噪声、随机遮罩），其优势在于：对比对之间的差异天然对应于“可观测信息 vs. 完整信息”的语义鸿沟，迫使编码器从有限的本体感知输入中推断出与特权信息一致的表征。

#### 编码器与预测器

策略编码器 $f_{\pmb{\theta}}$ 和预测器 $h_{\pmb{\psi}}$ 分别对原始状态 $\pmb{s}$ 和零遮罩后的状态 $\tilde{\pmb{s}}$ 提取表征：

$$z = f_{\pmb{\theta}}(s), \quad \tilde{z} = f_{\pmb{\theta}}(\tilde{s})$$

$$\pmb{p} = h_{\pmb{\psi}}(z), \quad \tilde{p} = h_{\pmb{\psi}}(\tilde{z})$$

这里采用 **SimSiam** 风格的架构：编码器 $f_{\pmb{\theta}}$ 后接一个预测器 MLP $h_{\pmb{\psi}}$，且对一侧的编码器输出施加**停梯度**（stop-gradient）操作，以防止表征坍缩。

#### PvP损失函数

对比损失采用对称的**负余弦相似度**（negative cosine similarity）：

$$D_{\mathrm{ncs}}(\pmb{p}, z) = - \frac{\pmb{p}}{\|\pmb{p}\|_2} \cdot \frac{z}{\|z\|_2}$$

完整的 PvP 损失为双向对称形式：

$$L_{\mathrm{PvP}} = D_{\mathrm{ncs}}\left(\pmb{p}, \mathbf{sg}(\tilde{\pmb{z}})\right) + D_{\mathrm{ncs}}\left(\tilde{\pmb{p}}, \mathbf{sg}(\pmb{z})\right)$$

其中 $\mathbf{sg}(\cdot)$ 表示停梯度操作。该损失迫使编码器输出的表征在“完整状态”和“仅本体感知状态”两种视图下保持一致，从而将特权信息中的任务相关知识蒸馏到本体感知表征中。

### SRL4Humanoid框架与总损失

PvP 被嵌入到统一的 **SRL4Humanoid** 框架中（Figure 3），该框架将 SRL 过程与 RL 过程完全解耦，支持 PPO 与多种 SRL 方法（SimSiam、SPR、VAE 等）的即插即用组合。

框架包含以下关键模块：
- **Policy Encoder**：将本体感知状态编码为潜在表征，供动作生成头使用；PvP 损失默认作用于此编码器。
- **Value Encoder**：编码特权状态以估计状态价值；实验表明对其施加 SRL 损失会导致训练崩溃（Figure 10）。
- **SimSiam-based Contrastive Head**：包含预测器 $h_{\psi}$ 和停梯度操作，计算 PvP 对比损失。
- **Interval Update Scheduler**：控制 SRL 损失的应用频率，提升训练稳定性。

![[assets/figures/papers/paper_list_l1050_https_arxiv_org_abs_2512_13093/figures/010_Figure_10.jpg]]
*Figure 10: Learning curves of applying the SRL to the value encoder. The solid line and shaded region denote the mean and standard deviation, respectively*

总损失由 RL 损失和周期性施加的 SRL 损失组成：

$$L_{\mathrm{Total}} = L_{\mathrm{RL}} + \mathbb{1}(T) \cdot \lambda \cdot L_{\mathrm{SRL}}$$

其中 $\mathbb{1}(T)$ 为指示函数，每 $T$ 步取值为 1（其余为 0），$\lambda$ 为 SRL 损失权重。间隔更新机制避免了训练早期低质量数据导致 SRL 陷入局部最优，消融实验表明 $T=50$ 在动作模仿任务上通常表现最优（Figure 8），$\lambda=0.1$ 时最终性能和样本效率最佳（Figure 17）。

### 关键设计选择与消融结论

1. **SRL作用目标**：PvP 损失默认应用于策略编码器。若应用于价值编码器，收敛速度显著变慢甚至训练崩溃（Figure 10）。
2. **无手工增强**：零遮罩替代了传统对比学习中的手工数据增强，避免了增强策略选择对性能的干扰。
3. **间隔更新**：每 $T$ 步施加一次 SRL 损失，而非每个 RL 更新步均施加，有效缓解早期训练的局部最优问题。
4. **与教师-学生蒸馏的对比**：PvP 在速度跟踪（Figure 13）和动作模仿（Figure 14）任务上均优于教师-学生蒸馏方法，且 PPO 仅靠本体感知状态无法学习。

## 实验与分析

### 核心瓶颈与实验设计逻辑

人形机器人全身控制任务面临的核心挑战在于复杂动力学和部分可观测性导致的强化学习样本效率低下。PvP 通过在可直接测量的本体感知状态与仅模拟器可用的特权状态之间引入对比学习，迫使策略编码器学习紧凑且任务相关的表征，从而在不增加复杂组件的前提下显著加速训练并提升最终性能。基于这一设计逻辑，实验围绕以下问题展开：PvP 能否在样本效率和最终性能上超越现有 SRL 方法？其各设计组件（损失作用目标、更新间隔、损失权重）如何影响训练？PvP 在不同任务、平台和地形下的泛化性如何？

实验在 LimX Oli 人形机器人（31 个自由度）上设计了两个代表性全身控制任务：**速度跟踪**（LimX-Oli-31dof-Velocity）和**动作模仿**（LimX-Oli-31dof-Mimic）。所有方法共享相同的 PPO 骨干、策略/价值网络架构和训练步数，每种 SRL 方法均经过初步超参数搜索以确保公平比较。默认 SRL 损失作用于策略编码器，价值编码器不施加 SRL 损失（该设计的消融验证见下文）。

### 主实验结果

**样本效率与最终性能。** Figure 5 展示了 PPO 及其与四种 SRL 方法组合在两个任务上的训练曲线。在速度跟踪任务上，PvP 的综合奖励（所有子奖励加权求和）收敛最快且最终值最高，其他 SRL 方法仅带来微弱提升。在动作模仿任务上，PvP 同样取得最高奖励，而 VAE 甚至出现性能退化。这表明基于本体感知-特权对比学习的 PvP 在样本效率和最终性能上均显著优于重建式 VAE、动力学建模式 SPR 和通用对比学习式 SimSiam。

**动作平滑度优化。** 实机部署对动作平滑度有严格要求。Figure 6 显示，PvP 在动作平滑度惩罚项上的收敛速度明显快于所有对比方法，这对于 sim-to-real 迁移具有重要实际意义——更平滑的动作意味着更低的关节冲击和更稳定的物理执行。

**跟踪精度。** 在动作模仿任务的三个关键跟踪指标上（Figure 7），PvP 均取得最高性能，进一步验证了其表征学习对策略质量的全方位提升。

### 消融实验

**SRL 损失作用目标。** 实验对比了将 SRL 损失施加于策略编码器与价值编码器的效果（Figure 10）。结果表明，对价值编码器施加 SRL 损失会导致收敛变慢甚至训练崩溃。这一发现揭示了关键设计原则：表征学习应聚焦于直接影响动作生成的编码器，而非价值估计模块。

**更新间隔。** Figure 8 展示了不同训练时间比例（即更新间隔 T）下各 SRL 方法的性能。在动作模仿任务上，T=50 时各方法通常表现最优。间隔更新机制避免了早期低质量数据导致 SRL 陷入局部最优，是 PvP 训练稳定性的重要保障。

**训练数据比例。** Figure 9 表明，增加训练数据比例通常能提升 SimSiam 和 PvP 在动作模仿任务上的性能，但提升幅度存在边际递减效应。

**损失权重敏感性。** Figure 17 显示，PvP 的损失权重 λ=0.1 时最终性能和样本效率最佳。权重过小则表征学习效果不足，过大则可能干扰 RL 优化目标，需要在两者间取得平衡。

**与教师-学生蒸馏的对比。** Figure 13 和 Figure 14 分别展示了 PvP 与教师-学生蒸馏方法在速度跟踪和动作模仿任务上的对比。PvP 在两个任务上均优于蒸馏方法，且 PPO 仅靠本体感知状态无法学习，进一步凸显了 PvP 对比学习框架的有效性。

**泛化性验证。** 在粗糙地形速度跟踪任务（LimX-Oli-31dof-Velocity-Rough，Figure 15）和另一人形机器人平台（Unitree-G1-29dof-Velocity，Figure 16）上，PvP 同样表现出色，验证了其对地形变化和机器人平台的泛化能力。

### 实验配置要点

Table 1 和 Table 3 分别列出了速度跟踪和动作模仿任务的关键奖励项。Table 2 和 Table 4 详细说明了两个任务中本体感知状态与特权状态的组成——速度跟踪任务中堆叠了 5 个连续本体感知状态作为策略编码器输入以增强鲁棒性。Table 5 和 Table 6 分别给出了所有实验中固定的策略/价值网络架构和 PPO 超参数。

### 局限与失败模式分析

尽管 PvP 在实验中表现优异，仍存在若干值得关注的局限。首先，PvP 在训练阶段依赖特权状态（如根线速度、根姿态等），这些信息在真实机器人部署时无法直接获取，sim-to-real 迁移中的表征一致性尚未完全验证，这需要后续通过领域随机化或在线自适应等方法进一步弥合。其次，当前实验主要在平坦地形和部分粗糙地形上进行，对于更复杂或动态变化的环境（如楼梯、外力干扰等）的泛化能力有待评估。此外，PvP 的性能对损失权重 λ 和更新间隔 T 等超参数较为敏感，不同任务可能需要独立调参，增加了调试成本。最后，框架目前仅在本体感知状态上进行了验证，未涉及视觉或触觉等多模态输入，限制了在复杂交互场景中的应用潜力。

### 补充图表

![[assets/figures/papers/paper_list_l1050_https_arxiv_org_abs_2512_13093/figures/005_Figure_5.jpg]]
*Figure 5: Training progress comparison between the vanilla PPO agent and its combination with four SRL methods on the two humanoid WBC tasks. The solid line and shaded region denote the mean and standard deviation, respectively*

![[assets/figures/papers/paper_list_l1050_https_arxiv_org_abs_2512_13093/figures/006_Figure_6.jpg]]
*Figure 6: The comparison of action smoothness optimization between the vanilla PPO agent and its combinations with the four SRL methods. The solid line and shaded region denote the mean and standard deviation, respectively*

![[assets/figures/papers/paper_list_l1050_https_arxiv_org_abs_2512_13093/figures/007_Figure_7.jpg]]
*Figure 7: The tracking performance comparison between the PPO agent and its combinations with the four SRL methods. Our PvP achieves the highest performance across the three key tracking metrics*

![[assets/figures/papers/paper_list_l1050_https_arxiv_org_abs_2512_13093/figures/009_Figure_8.jpg]]
*Figure 8: Training progress comparison of the four SRL methods with different training time proportions on the two humanoid WBC tasks. The solid line and shaded region denote the mean and standard deviation, respectively*

![[assets/figures/papers/paper_list_l1050_https_arxiv_org_abs_2512_13093/figures/019_Figure_13.jpg]]
*Figure 13: Training progress comparison between the teacherstudent distillation method and PvP in the LimX-Oli-31dof-Velocity task. The solid line and shaded region denote the mean and standard deviation, respectively*

![[assets/figures/papers/paper_list_l1050_https_arxiv_org_abs_2512_13093/figures/020_Figure_14.jpg]]
*Figure 14: Training progress comparison between the teacherstudent distillation method and PvP in the LimX-Oli-31dof-Mimic task. The solid line and shaded region denote the mean and standard deviation, respectively*

![[assets/figures/papers/paper_list_l1050_https_arxiv_org_abs_2512_13093/figures/021_Figure_16.jpg]]
*Figure 16: Training progress comparison between the vanilla PPO agent and its combination with four SRL methods on the Unitree-G1-29dof-Velocity task. The solid line and shaded region denote the mean and standard deviation, respectively*

![[assets/figures/papers/paper_list_l1050_https_arxiv_org_abs_2512_13093/figures/022_Figure_15.jpg]]
*Figure 15: Training progress comparison between the teacherstudent distillation method and PvP in the LimX-Oli-31dof-Velocity-Rough task. The solid line and shaded region denote the mean and standard deviation, respectively*

![[assets/figures/papers/paper_list_l1050_https_arxiv_org_abs_2512_13093/figures/023_Figure_17.jpg]]
*Figure 17: Performance comparison of the PvP method with different weighting coefficients on the LimX-Oli-31dof-Mimic task. The solid line and shaded region denote the mean and standard deviation, respectively*

## 方法谱系与知识库定位

### 1. 方法继承与基线对比

PvP 的核心技术路线建立在**本体感知-特权状态对比学习**与**模块化强化学习框架**两条主线上。其直接继承关系可从以下维度展开：

**强化学习骨干**：PvP 以 **PPO** 作为策略优化的基础算法，所有对比实验均共享相同的 PPO 超参数、策略/价值网络架构和训练步数（Table 5–6），以隔离表征学习方法的影响。这一设计确保了公平性——任何性能增益均可归因于 SRL 模块的引入。

**表征学习（SRL）谱系**：论文将 PvP 与三类代表性 SRL 方法进行了系统对比：
- **SimSiam**：作为对比学习基线，采用孪生网络结构，但依赖手工数据增强（如高斯噪声、随机遮罩）构造正样本对。PvP 直接继承其**停梯度（stop-gradient）** 与**预测器（predictor）** 机制，但将增强策略替换为基于状态模态内在互补性的**零遮罩（ZeroMasking）** 操作。
- **SPR**：基于动力学建模的 SRL 方法，通过预测未来状态表征来学习时序依赖。在动作模仿任务上表现有限，甚至出现性能退化（Figure 5 右）。
- **VAE**：基于重建的 SRL 方法，通过编码-解码学习潜在表征。在动作模仿任务上**导致性能退化**（Figure 5 右），表明重建目标可能引入与任务无关的噪声维度。

**关键改进槽位**：

| 改进维度 | 基线做法 | PvP 做法 | 证据锚点 |
|---------|---------|---------|---------|
| SRL 目标 | 无 SRL 或单模态重建/预测 | 本体感知-特权状态间 SimSiam 风格对比学习 | Section 4.1, Eq.(4) |
| 数据增强 | 手工设计（高斯噪声、随机遮罩） | 零遮罩构造对比对，无需手工增强 | Section 4.1, Eq.(2) |
| SRL 更新策略 | 每步施加 SRL 损失 | 间隔更新机制（每 T 步施加一次） | Section 4.2, Eq.(6), Algorithm 1 |
| SRL 作用对象 | 可应用于策略或价值编码器 | 默认仅用于策略编码器（价值编码器会导致崩溃） | Figure 10 |

**与教师-学生蒸馏的对比**：消融实验（Figure 13–14）表明，PvP 在速度跟踪和动作模仿两个任务上均**优于**教师-学生蒸馏方法。蒸馏方法需要先训练一个特权教师策略再进行知识迁移，而 PvP 通过对比学习直接在策略编码器中注入特权信息，避免了多阶段训练的复杂性。值得注意的是，PPO 仅依靠本体感知状态（无特权信息）**无法学习有效策略**（Figure 13），这验证了特权信息对人形机器人全身控制的必要性。

### 2. 适用边界与泛化能力

**已验证的正向边界**：
- **机器人平台泛化**：在 LimX Oli（31 自由度）和 Unitree G1（29 自由度）两个不同人形平台上均表现出色（Figure 16），表明方法对机器人构型差异具有一定鲁棒性。
- **地形泛化**：在粗糙地形速度跟踪任务（LimX-Oli-31dof-Velocity-Rough）上同样有效（Figure 15），说明表征学习未过拟合平坦地形。
- **任务类型泛化**：覆盖速度跟踪（密集奖励）和动作模仿（稀疏跟踪奖励）两类典型全身控制任务。

**已知局限与未验证边界**：
1. **Sim-to-Real 迁移中的表征一致性**：PvP 在训练阶段依赖特权状态（如根线速度、根姿态、接触力等），这些信息在真实机器人部署时无法直接获取。论文展示了 Sim2Sim 评估结果（Figure 11），但**未提供真实世界部署的表征一致性验证**。本体感知编码器在真实噪声、延迟和动力学差异下的表现需要额外校准或微调。
2. **环境复杂度上限**：当前实验主要在平坦地形和部分粗糙地形上进行，对于楼梯攀爬、外力干扰、动态障碍物等更复杂场景的泛化能力尚未评估。
3. **感知模态限制**：框架仅在本体感知状态（关节编码器、IMU、足底力传感器等）上验证，未涉及视觉（RGB/深度）或触觉等多模态输入，限制了在需要环境感知的交互场景中的潜力。
4. **超参数敏感性**：PvP 对损失权重 λ（最优值为 0.1，Figure 17）和更新间隔 T（最优值为 50，Figure 8）较为敏感，不同任务可能需要重新调整，增加了调试成本。

### 3. 开放问题与后续工作方向

论文明确提出了以下开放问题，代表了该方法的知识库定位与未来演进方向：

1. **多 SRL 技术融合**：如何将动力学建模（如 SPR）、重建（如 VAE）等其他 SRL 技术与 PvP 的对比学习框架融合？当前实验表明 VAE 单独使用会导致性能退化，但与对比学习的组合可能产生互补效应。

2. **多模态表征扩展**：如何将 RGB 或深度图像等多模态数据有效融入 PvP 的表征学习过程？这需要解决不同模态间的对齐问题，以及视觉特征与本体感知特征在对比学习框架中的融合策略。

3. **跨平台表征预训练**：PvP 学习的本体感知表征是否可以通过预训练或逆动力学等自监督任务进一步提升，并实现跨机器人平台的零样本或少样本泛化？这是通往通用人形机器人表征的关键问题。

4. **Sim-to-Real 表征校准**：在更深入的 sim-to-real 迁移中，本体感知表征如何适应真实世界的噪声分布、传感器延迟和未建模动力学？是否需要领域随机化与对比学习的联合优化？

**知识库定位总结**：PvP 处于**人形机器人全身控制 × 表征学习**的交叉点，其核心贡献在于证明了**状态模态间的内在互补性**可以替代手工数据增强，成为对比学习的有效驱动力。该方法为后续工作提供了一个简洁的基线：在 PPO 骨干上仅需添加一个对比学习头（含预测器和停梯度）和间隔更新调度器，即可显著提升样本效率，无需复杂的多阶段训练或手工增强设计。

## 原文 PDF

![[paperPDFs/CVPR_2026/PvP_Data_Efficient_Humanoid_Robot_Learning_with_Proprioceptive_Privileged_Contrastive_Representations.pdf]]
