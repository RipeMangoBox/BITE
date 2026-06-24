---
title: "FlowHijack: A Dynamics-Aware Backdoor Attack on Flow-Matching Vision-Language-Action Models"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/FlowHijack_A_Dynamics_Aware_Backdoor_Attack_on_Flow_Matching_Vision_Language_Action_Models.pdf
project_link: null
code_link: null
aliases:
- FlowHijack
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: "流匹配策略的向量场动态在低τ阶段（τ ∈ [0, 0.4]）控制动作的全局语义方向；通过τ条件注入针对性的错误，可操纵该阶段的方向，并利用ODE求解器沿轨迹放大偏差，从而在不破坏后续精细调整的前提下劫持动作生成。"
primary_logic: 将后门攻击目标从VLMs的特征空间下移至向量场动态本身，通过仅干预早期生成步骤（τ条件注入）并结合动态模仿正则化，迫使恶意动作在运动学特征上与良性动作不可区分，实现了高攻击成功率与高度隐蔽性的统一。
claims:
- 在LIBERO-Goal任务中，使用隐蔽的Object State触发器，FlowHijack的ASR达到100%，而BadVLA的ASR仅为11.2%，证明向量场动态劫持远优于特征空间分离。
- 消融实验中，移除动态劫持损失L_BD导致ASR降至0%，确认该损失是攻击成功的必要条件。
- 动态模仿正则化L_mimic将恶意动作的速度振荡从超过20 m/s的异常尖峰降至与正常动作几乎一致的平滑曲线，证明其运动学隐蔽效果。
- LIBERO-10 上 SR(w/o) / ASR = 82.8 / 64.4 (Ours IP with Object State trigger)
---

# FlowHijack: A Dynamics-Aware Backdoor Attack on Flow-Matching Vision-Language-Action Models

> [!tip] 核心洞察
> 将后门攻击目标从VLMs的特征空间下移至向量场动态本身，通过仅干预早期生成步骤（τ条件注入）并结合动态模仿正则化，迫使恶意动作在运动学特征上与良性动作不可区分，实现了高攻击成功率与高度隐蔽性的统一。

| 字段 | 内容 |
|------|------|
| 中文题名 | FlowHijack：一种针对流匹配视觉-语言-动作模型的动态感知后门攻击 |
| 英文题名 | FlowHijack: A Dynamics-Aware Backdoor Attack on Flow-Matching Vision-Language-Action Models |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2604.09651) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/image_and_video_generation |
| Method | FlowHijack |
| Dataset | LIBERO-10, LIBERO-Goal, LIBERO-Spatial, LIBERO-Object |

> [!tip] 效果简介
> - LIBERO-10 上，SR(w/o) / ASR 82.8 / 64.4 (Ours IP with Object State trigger) vs 85.2 / - (base π0) ; 74.7 / 62.2 (BadVLA) (SR -2.4 ; ASR +2.2 vs BadVLA)。
> - LIBERO-Goal 上，ASR 100% (Ours IP with Object State trigger) vs 11.2% (BadVLA with Object State trigger) (+88.8%)。
> - LIBERO-Spatial 上，ASR 100% (Ours IP with Scene Semantic trigger) vs 15.3% (BadVLA with Scene Semantic trigger) (+84.7%)。

## 概述

### 问题与瓶颈

视觉-语言-动作（VLA）模型正逐步从离散动作令牌转向基于**流匹配**的连续动作生成范式，后者通过求解常微分方程（ODE）直接输出平滑的动作序列。然而，现有后门攻击方法（如BadVLA）根植于离散令牌操作（如标签翻转）和VLM特征空间分离，无法直接迁移到流匹配VLA的连续动作生成机制上。此外，传统触发器（如白色像素块）在物理环境中醒目且不自然，而生成的恶意动作在运动学上往往表现出异常的速度分布，严重破坏攻击的隐蔽性。

### 核心方法：FlowHijack

**FlowHijack** 是首个系统性针对流匹配VLA模型的后门攻击框架。其核心洞察在于：**流匹配的向量场动态在早期阶段（τ ∈ [0, 0.4]）控制动作的全局语义方向**。通过仅干预这一早期窗口，并利用ODE求解器沿轨迹放大偏差，FlowHijack可在不破坏后续精细调整的前提下劫持动作生成。

方法由三个关键组件构成：

- **上下文感知触发器**：设计物理上合理、语义连贯的视觉触发器（物体状态触发器、场景语义触发器），嵌入观测中而不引起警觉。
- **动态劫持（τ条件注入）**：将后门攻击目标从VLM特征空间下移至向量场动态本身，仅在流匹配的早期阶段（τ ≤ τ₀）训练模型将触发观测与恶意目标动作关联。
- **动态模仿正则化**：强制恶意向量场的L2范数与良性向量场一致，使恶意动作在运动学特征上与正常动作不可区分，实现行为隐蔽性。

### 主要结果

在LIBERO基准上，FlowHijack展现了压倒性的攻击效能：

- **LIBERO-Goal任务**：使用物体状态触发器，攻击成功率（ASR）达**100%**，而BadVLA仅为11.2%（Δ +88.8%）。
- **LIBERO-Spatial任务**：使用场景语义触发器，ASR同样达**100%**，BadVLA仅为15.3%（Δ +84.7%）。
- **良性性能保持**：在LIBERO-Object任务上，良性成功率（SR）与干净基准π0持平（98.8%），无退化。

消融实验证实：移除动态劫持损失（L_BD）导致ASR骤降至0%，确认其为攻击植入的唯一驱动因素；移除动态模仿正则化（L_mimic）虽仍保持高ASR，但生成的动作产生超过20 m/s的异常速度振荡，缺乏运动学隐蔽性。

### 方法定位

FlowHijack属于**白盒微调中毒**攻击，假定攻击者可访问预训练模型并注入中毒数据集。与BadVLA的两阶段解耦微调（先特征分离后动作头微调）不同，FlowHijack采用单阶段联合优化，通过加权组合流匹配损失、后门劫持损失和模仿正则化项实现攻击效能与良性性能的平衡。其攻击面是流匹配VLA独有的向量场动态，这是此前未被探索的新攻击面，对连续控制模型的安全性提出了新的挑战。

## 背景与动机

### 机器人视觉-语言-动作模型与后门攻击

视觉-语言-动作模型（VLA）正在成为机器人操作策略的核心范式。这类模型以多模态观测（图像与语言指令）为输入，直接输出底层动作序列，从而驱动机械臂完成复杂任务。然而，VLA模型在开放世界部署中面临严峻的安全威胁：攻击者可通过数据投毒（data poisoning）在模型内部植入后门，使其在遇到特定触发器时执行恶意动作，而在正常输入下保持良性表现。

### 现有后门攻击的局限性

当前针对VLA的后门攻击框架，如 **BadVLA**，主要面向基于离散动作令牌（discrete action tokens）的模型设计。这类方法的核心机制是在视觉-语言模型（VLM）的特征空间中操作——通过最大化触发样本与干净样本的VLM特征距离，迫使模型学习触发-恶意动作的关联。然而，这一范式面临两个根本性瓶颈：

1. **动作表示不兼容**：新一代VLA模型（如π₀）采用流匹配（flow matching）策略生成连续动作，其输出是向量场（vector field）而非离散令牌。BadVLA的特征空间分离机制无法直接迁移至这种连续生成范式，导致攻击成功率骤降（例如在LIBERO-Goal任务上仅达11.2%）。

2. **触发器隐蔽性不足**：现有攻击多使用视觉醒目的像素块（如白色方块）作为触发器，在物理环境中极易被人类观察者或检测系统识别。同时，攻击生成的恶意动作往往伴随运动学异常（如速度尖峰），进一步暴露攻击行为。

### 流匹配的动作生成机制：新的攻击面

流匹配策略的动作生成过程具有一个关键特性：向量场在不同流时间τ阶段承担不同角色。在早期低τ阶段（τ ∈ [0, 0.4]），向量场主要决定动作的全局语义方向；而在后续高τ阶段，则负责精细调整。这一动态特性意味着，攻击者若能在早期阶段注入定向偏差，便可借助常微分方程（ODE）求解器沿生成轨迹放大该偏差，从而在不破坏后续精细调整的前提下劫持整个动作序列。

这一观察揭示了一个此前未被探索的攻击面：**直接操纵流匹配的向量场动态，而非间接通过VLM特征空间施加影响**。

### 本文动机

基于上述分析，本文提出 **FlowHijack**——首个系统性针对流匹配VLA模型的后门攻击框架。FlowHijack的核心动机在于：

- **将攻击目标下移至向量场动态本身**，通过τ条件注入策略仅在生成早期阶段干预，实现高效劫持；
- **设计上下文感知的视觉触发器**，使其在物理上合理且语义连贯，提升隐蔽性；
- **引入动态模仿正则化**，强制恶意动作的向量场模长分布与良性动作一致，消除运动学异常。

通过这三项设计的协同，FlowHijack旨在打破现有后门攻击在流匹配VLA上的适用性瓶颈，实现高攻击成功率与高度隐蔽性的统一。

## 核心创新

FlowHijack的核心创新在于将后门攻击的干预层级从传统的视觉-语言模型（VLM）特征空间**下移至流匹配的向量场动态本身**，并围绕这一新攻击面设计了三个紧密耦合的机制，实现了攻击效能与隐蔽性的统一。

### 1. 攻击面的范式转移：从特征空间到向量场动态

现有VLA后门攻击（如BadVLA）通过在VLM特征空间中最大化触发样本与干净样本的特征距离来植入后门，其本质是操纵离散令牌或特征表示。然而，流匹配VLA（如**π0**）采用连续动作生成机制——通过求解常微分方程（ODE）从噪声逐步演化出动作轨迹。这一机制使得基于特征空间分离的攻击策略难以迁移：**BadVLA**在LIBERO-Goal任务上使用上下文感知触发器时，攻击成功率（ASR）骤降至11.2%（Table 1），暴露出特征层级攻击与连续动作生成之间的根本性失配。

FlowHijack的核心洞见在于：流匹配策略的向量场动态在低流时间阶段（τ ∈ [0, 0.4]）控制着动作的**全局语义方向**。通过直接操纵这一阶段的向量场，攻击者可以在不破坏后续精细调整的前提下劫持整个动作生成过程。这一“动态劫持”策略绕过了VLM特征空间的冲突，直接作用于动作生成的因果链路。

### 2. 关键机制创新：τ条件注入与动态模仿正则化

FlowHijack的方法设计围绕以下五个关键改变槽位展开：

**（1）攻击机制：从特征分离到向量场劫持**

BadVLA通过余弦相似度损失最大化触发/干净特征的分离度；FlowHijack则直接训练向量场网络 $v_\theta$ 在低τ阶段指向恶意目标方向。其核心损失函数为τ条件注入损失：

$$\mathcal{L}_{\mathrm{BD}} = \mathbb{E}_{(o^{+}, A^{\star}) \sim \mathcal{D}_{\mathrm{poison}}} \left\| v_{\theta}(A^{\tau}, o^{+}, \tau) - u(A^{\tau} \mid A^{\star}) \right\|_{2}^{2} \quad \tau \sim U[0, \tau_{0}]$$

该损失仅在τ ∈ [0, τ₀]（τ₀=0.4）范围内生效，利用流匹配早期阶段对全局方向的敏感性，以最小干预实现最大偏差放大。消融实验证实：移除 $\mathcal{L}_{\mathrm{BD}}$ 后所有任务的ASR降为0%（Table 2），确认该损失是攻击植入的唯一驱动因素。

**（2）攻击注入窗口：全流程干预到早期阶段聚焦**

BadVLA对整个生成过程施加约束，缺乏阶段特异性。FlowHijack将攻击窗口精确限定在τ ∈ [0, τ₀]。超参数搜索表明τ₀=0.4在LIBERO-Goal上达到ASR 100%且良性成功率（SR）最高（97.8%）；τ₀过小导致ASR骤降，过大则轻微损害SR（Table 5）。这一窗口设计利用了流匹配的动力学特性——早期阶段决定动作的“骨架”，后续阶段仅做精细修正。

**（3）行为隐蔽性：从无约束到动态模仿正则化**

BadVLA生成的恶意动作在运动学上存在显著异常（速度振荡超过20 m/s），极易被检测。FlowHijack引入动态模仿正则化：

$$\mathcal{L}_{\mathrm{mimic}} = \mathbb{E}_{\tau \sim p_{\tau}(\tau)} \Big| \left\| v_{\theta}(A^{\tau}, o^{+}) \right\|_{2} - \left\| v_{\theta}(A^{\tau}, o) \right\|_{2}^{\mathrm{sg}} \Big|$$

该正则项强制恶意向量场的L2范数与良性向量场一致，从动力学层面模拟正常动作的统计特征。实验表明，移除 $\mathcal{L}_{\mathrm{mimic}}$ 虽仍保持高ASR，但生成的末端执行器速度曲线出现异常高频振荡；完整FlowHijack则产生与正常动作几乎不可区分的平滑轨迹（Figure 7, Appendix D）。

**（4）触发器类型：从视觉醒目到上下文感知**

BadVLA使用视觉醒目的像素块（如白色方块）作为触发器，在物理环境中易被察觉。FlowHijack设计了两种上下文感知触发器：**物体状态触发器**（如物体位置、开合状态的改变）和**场景语义触发器**（如背景物体的增删），在物理上合理且语义连贯，显著提升了隐蔽性。

**（5）损失函数组成：从两阶段解耦到单阶段联合优化**

BadVLA采用两阶段独立训练（先特征分离冻结动作头，后动作头微调冻结VLM）。FlowHijack采用单阶段联合优化：

$$\mathcal{L}_{\mathrm{total}} = (1 - \alpha - \beta) \mathcal{L}_{\mathrm{FM}} + \alpha \mathcal{L}_{\mathrm{BD}} + \beta \mathcal{L}_{\mathrm{mimic}}$$

其中α=0.05控制攻击强度，β=0.05控制模仿强度，$1-\alpha-\beta$ 保持良性性能。网格搜索确认该权重配置实现了攻击强度与隐蔽性的最优平衡（F.2）。

### 3. 创新点的因果链路

上述改变槽位形成了一条完整的因果链路：**上下文感知触发器**提供隐蔽的激活条件 → **τ条件注入**在向量场早期阶段植入恶意方向 → **ODE求解器**沿轨迹放大偏差 → **动态模仿正则化**确保恶意动作在运动学上与良性动作不可区分。这一链路使得FlowHijack在LIBERO-Goal任务上达到100% ASR（BadVLA仅11.2%），同时在LIBERO-Object任务上保持与干净模型完全一致的良性成功率（98.8%），实现了攻击效能与可用性的统一。

## 整体框架

FlowHijack 是首个系统性针对流匹配（flow-matching）VLA 模型的后门攻击框架。其核心创新在于将攻击面从传统的 VLM 特征空间**下移**至连续动作生成的向量场动态本身，并通过**仅干预流匹配早期阶段**的策略实现高隐蔽性攻击。整体框架由三个关键组件构成，形成“触发器设计→动态劫持→损失联合优化”的端到端攻击流水线。

### 框架总览

Figure 2 展示了 FlowHijack 的完整攻击框架。多模态观测（视觉+语言指令）首先经过 VLA 的感知编码器，随后进入流匹配策略网络生成连续动作序列。攻击者的投毒数据在**观测输入端**植入上下文感知触发器，在**向量场动态层**通过 τ 条件注入施加恶意偏转，最终通过联合损失函数实现攻击效能与良性性能的平衡。

![[assets/figures/papers/paper_list_l2155_https_arxiv_org_abs_2604_09651/figures/002_Figure_2.jpg]]
*Figure 2: Overview of our FlowHijack Attack framework for backdoor injection in VLA models*

### 三大核心组件

**1. 上下文感知触发器设计（Context-Aware Triggers）**

攻击者在视觉模态中设计物理合理、语义连贯的触发器，分为两类（Sec. 4.2）：
- **物体状态触发器（Object State Trigger）**：利用任务相关物体的状态变化作为触发条件，形式化为谓词 $P_{\mathrm{state}}(o_t)$，如“抽屉已打开”或“物体被移动至特定位置”。
- **场景语义触发器（Scene Semantic Trigger）**：通过环境变换函数 $\mathcal{T}_{\mathrm{env}}(o_t)$ 引入语义级场景修改，如桌面放置特定标志物或改变背景布局。

与 BadVLA 使用的视觉醒目像素块（如白色方块）相比，FlowHijack 的触发器在物理场景中不易被察觉，显著提升了**视觉隐蔽性**。Figure 3 展示了仿真（LIBERO）和真实世界（Franka）环境中的触发器示例及正常/后门激活动作对比。

**2. 动态劫持（Dynamics Hijacking）**

这是 FlowHijack 区别于所有现有 VLA 后门攻击的核心机制。攻击者不再操纵 VLM 特征空间（如 BadVLA 的余弦相似度损失），而是**直接干预流匹配的向量场动态**。具体策略包括：

- **τ 条件注入（τ-conditioned Injection）**：仅在流匹配的早期阶段（$\tau \in [0, \tau_0]$，$\tau_0=0.4$）注入攻击损失。流匹配中低 τ 阶段控制动作的全局语义方向，在此窗口内训练向量场指向恶意目标，可利用 ODE 求解器沿轨迹放大偏差，同时不影响后续精细调整阶段。
- **恶意目标动作设计（Malicious Action $A^\star$）**：定义两种攻击策略——
  - **位姿锁定（Pose-Locking, PL）**：$A^\star = A_{\text{const}}$，将动作锁定为恒定目标（如零位姿或归位配置）。
  - **初始扰动（Initial-Perturbation, IP）**：$A^\star = A + \delta_A$，在正常动作上叠加恒定小扰动向量 $\delta_A$。
- **动态模仿正则化（Dynamics Mimicry Regularizer）**：通过 $\mathcal{L}_{\mathrm{mimic}}$ 强制恶意向量场的 L2 范数与良性向量场一致，抑制运动学异常。Figure 4 展示了该正则化使恶意动作的特征分布与正常动作重叠，实现**行为隐蔽性**。Figure 7 进一步验证：无模仿正则化时攻击产生超过 20 m/s 的速度振荡尖峰，而完整 FlowHijack 的速度曲线与正常动作几乎一致。

**3. 联合训练目标（Joint Training Objective）**

FlowHijack 采用**单阶段联合优化**，将三个损失项加权组合（Eq. 7）：

$$\mathcal{L}_{\mathrm{total}} = (1 - \alpha - \beta) \mathcal{L}_{\mathrm{FM}} + \alpha \mathcal{L}_{\mathrm{BD}} + \beta \mathcal{L}_{\mathrm{mimic}}$$

其中：
- $\mathcal{L}_{\mathrm{FM}}$ 为标准流匹配损失（Eq. 3），维持良性任务性能；
- $\mathcal{L}_{\mathrm{BD}}$ 为后门劫持损失（Eq. 5），仅在 $\tau \sim U[0, \tau_0]$ 范围内训练模型将触发观测与恶意目标 $A^\star$ 关联；
- $\mathcal{L}_{\mathrm{mimic}}$ 为动态模仿正则化项（Eq. 6），确保运动学隐蔽性。

超参数 $\alpha=0.05$ 控制攻击强度，$\beta=0.05$ 控制模仿强度，经网格搜索确定最优平衡。

### 与 BadVLA 的关键差异

| 维度 | BadVLA | FlowHijack |
|------|--------|------------|
| **攻击机制** | 操纵 VLM 特征空间，最大化触发/干净特征距离 | 直接操纵流匹配向量场动态 |
| **注入窗口** | 整个生成过程 | 仅早期阶段（$\tau \in [0, 0.4]$） |
| **训练方式** | 两阶段解耦微调 | 单阶段联合优化 |
| **触发器** | 视觉醒目像素块 | 上下文感知的语义触发器 |
| **行为隐蔽性** | 无 | 动态模仿正则化 |

### 输入输出流

- **输入**：多模态观测 $o_t$（RGB 图像 + 语言指令），投毒样本中观测被替换为触发版本 $o_t^+$。
- **中间表示**：VLM 编码的感知特征 → 流匹配策略网络 $v_\theta$ 在流时间 $\tau$ 上预测向量场。
- **输出**：连续动作块 $A_t$（通过 ODE 求解器从噪声 $\varepsilon$ 积分至 $\tau=1$ 生成）。当触发器激活时，输出被劫持为恶意目标 $A^\star$。

### 补充图表

![[assets/figures/papers/paper_list_l2155_https_arxiv_org_abs_2604_09651/figures/001_Figure_1.jpg]]
*Figure 1: Overview of two action representations in VLA models*

## 核心模块与公式推导

### 3.1 流匹配动作生成的基础公式

流匹配VLA将机器人动作建模为从纯噪声到目标动作块的连续变换过程。给定动作块 $A_t$ 和高斯噪声 $\varepsilon \sim \mathcal{N}(0, I)$，通过流时间 $\tau \in [0, 1]$ 定义含噪动作的线性插值：

$$A_{t}^{\tau} = \tau A_{t} + (1 - \tau) \varepsilon \quad \text{(Eq. 1)}$$

对应的理想去噪向量场为瞬时变化率：

$$u(A_{t}^{\tau} \mid A_{t}) = \frac{d A_{t}^{\tau}}{d \tau} = A_{t} - \varepsilon \quad \text{(Eq. 2)}$$

标准流匹配训练损失使预测向量场 $v_\theta$ 逼近该目标：

$$\mathcal{L}_{\mathrm{FM}} = \mathbb{E}_{p_{1}(A), \epsilon, p_{\tau}(\tau)} \left\| v_{\theta} (A_{t}^{\tau}, o_{t}, \tau) - u (A_{t}^{\tau} \mid A_{t}) \right\|_{2}^{2} \quad \text{(Eq. 3)}$$

推理时从 $\tau=0$ 的噪声采样开始，通过ODE求解器沿 $\tau \in [0, 1]$ 积分生成动作：

$$\frac{d A_{\tau}}{d \tau} = v_{\theta}(A_{\tau}, o_{t}, \tau) \quad \text{(Eq. 4)}$$

### 3.2 动态劫持损失（$\tau$ 条件注入）

FlowHijack的核心创新在于直接操纵向量场动态，而非干预VLM特征空间。其关键洞察是：流匹配的早期阶段（低 $\tau$ 区间）控制动作的全局语义方向，后续阶段仅进行精细调整。因此，攻击仅需在 $\tau \in [0, \tau_0]$ 窗口内注入恶意信号，即可劫持整个生成轨迹。

给定中毒样本 $(o^{+}, A^{\star})$，其中 $o^{+}$ 为含触发器的观测，$A^{\star}$ 为恶意目标动作，动态劫持损失定义为：

$$\mathcal{L}_{\mathrm{BD}} = \mathbb{E}_{(o^{+}, A^{\star}) \sim \mathcal{D}_{\mathrm{poison}}} \left\| v_{\theta}(A^{\tau}, o^{+}, \tau) - u(A^{\tau} \mid A^{\star}) \right\|_{2}^{2}, \quad \tau \sim U[0, \tau_{0}] \quad \text{(Eq. 5)}$$

其中 $\tau_0 = 0.4$ 为注入窗口上界（经消融实验验证，见 Table 5）。该损失仅在早期训练模型将触发观测与恶意向量场关联，ODE求解器在推理时会沿此偏转方向累积误差，最终生成攻击者指定的动作。

### 3.3 动态模仿正则化

仅靠 $\mathcal{L}_{\mathrm{BD}}$ 虽可实现高攻击成功率，但生成的恶意动作常出现异常的速度振荡（峰值超过 20 m/s），破坏运动学隐蔽性。为此引入动态模仿正则化，强制恶意向量场的模长与良性向量场一致：

$$\mathcal{L}_{\mathrm{mimic}} = \mathbb{E}_{\tau \sim p_{\tau}(\tau)} \Big| \left\| v_{\theta}(A^{\tau}, o^{+}) \right\|_{2} - \left\| v_{\theta}(A^{\tau}, o) \right\|_{2}^{\mathrm{sg}} \Big| \quad \text{(Eq. 6)}$$

其中 $\mathrm{sg}$ 表示停止梯度（stop-gradient），即良性向量场模长作为固定目标，不参与梯度回传。该正则化使恶意动作的速度分布与正常动作重叠（见 Figure 4），末端执行器速度曲线从高频振荡转为平滑（见 Figure 7）。

![[assets/figures/papers/paper_list_l2155_https_arxiv_org_abs_2604_09651/figures/004_Figure_4.jpg]]
*Figure 4: Visualization of Behavioral Stealth. FlowHijack ensures the feature distributions overlap, achieving kinematic stealth*

![[assets/figures/papers/paper_list_l2155_https_arxiv_org_abs_2604_09651/figures/011_Figure_7.jpg]]
*Figure 7: Comparison of end-effector velocity profiles. Without the mimicry regularizer*

### 3.4 联合训练目标

三个损失通过加权组合形成最终优化目标：

$$\mathcal{L}_{\mathrm{total}} = (1 - \alpha - \beta) \mathcal{L}_{\mathrm{FM}} + \alpha \mathcal{L}_{\mathrm{BD}} + \beta \mathcal{L}_{\mathrm{mimic}} \quad \text{(Eq. 7)}$$

- $\mathcal{L}_{\mathrm{FM}}$：维持良性任务性能，权重 $1-\alpha-\beta$ 保证模型在无触发器时正常执行；
- $\mathcal{L}_{\mathrm{BD}}$：驱动攻击植入，权重 $\alpha = 0.05$ 控制攻击强度；
- $\mathcal{L}_{\mathrm{mimic}}$：实现运动学隐蔽，权重 $\beta = 0.05$ 平衡隐蔽性与攻击效能。

$\alpha$ 和 $\beta$ 经网格搜索确定（见 Appendix F.2），消融实验（Table 2）证实：移除 $\mathcal{L}_{\mathrm{BD}}$ 导致 ASR 降为 0%，移除 $\mathcal{L}_{\mathrm{FM}}$ 导致良性 SR 降为 0%，移除 $\mathcal{L}_{\mathrm{mimic}}$ 虽保持高 ASR 但产生可检测的运动学异常。

## 实验与分析

### 主要结果：FlowHijack对BadVLA的性能优势

Table 1展示了FlowHijack与BadVLA基线在LIBERO-10四个子任务上的全面对比。核心发现是：**FlowHijack通过直接操纵向量场动态，在上下文感知触发器下实现了近乎完美的攻击成功率，而BadVLA的VLM特征空间攻击策略几乎完全失效。**

在LIBERO-Goal任务上，使用Object State触发器时，FlowHijack（IP策略）的ASR达到**100%**，而BadVLA仅为**11.2%**，差距高达88.8个百分点。这一悬殊差异揭示了问题的本质：BadVLA试图在VLM特征空间中最大化干净样本与触发样本的余弦距离（式8），但VLA模型的视觉主导策略使VLM对上下文感知触发器的语义变化不敏感——模型凭借视觉上下文仍能正确推理任务，导致特征分离失败。FlowHijack绕过了这一瓶颈，直接攻击下游的向量场动态，因而不受VLM层面语义鲁棒性的制约。

在LIBERO-Spatial任务上，Scene Semantic触发器的结果进一步验证了这一机制：FlowHijack ASR为**100%**，BadVLA仅为**15.3%**。场景语义触发器（如替换桌面背景）对VLM而言是全局上下文变化，但不足以颠覆其任务推理；而在流匹配的动态层面，早期τ阶段的向量场对输入条件高度敏感，使得攻击注入极为有效。

与此同时，FlowHijack保持了良好的良性任务性能。在LIBERO-Object任务上，FlowHijack（IP + Object State）的良性SR为**98.8%**，与干净基准π0的98.8%完全持平，表明攻击植入未损害模型的正常能力。在LIBERO-10整体上，FlowHijack的SR(w/o)为82.8%，相比π0基准（85.2%）仅下降2.4个百分点，且优于BadVLA的74.7%。这一良性性能的保持归功于联合训练目标（式7）中流匹配损失L_FM的持续优化，以及τ条件注入仅干预早期生成阶段（τ∈[0, 0.4]）的设计。

### 消融实验：各损失组分的因果贡献

Table 2的消融实验严格验证了FlowHijack三个损失组分的独立功能。完整版（Ours + ALL）在LIBERO-Goal上达到ASR 100%、SR 97.8%，作为消融的参照基准。

**移除L_BD（后门劫持损失）**导致所有任务的ASR降至**0%**，同时SR回升至与干净模型相当的水平。这一结果确凿证明：L_BD是攻击植入的**唯一驱动因素**——没有对向量场动态的显式劫持训练，模型不会建立触发条件与恶意动作之间的关联。这也排除了数据污染本身（中毒样本的存在）足以诱发后门行为的可能性。

**移除L_FM（流匹配损失）**使良性SR骤降至**0%**，但ASR保持100%。这说明：L_FM是维持模型可用性的必要条件，但攻击机制（L_BD + L_mimic）可以在完全牺牲良性性能的情况下独立运作。这一极端消融揭示了攻击与良性目标在损失空间中的可分离性——两者并非零和博弈，而是通过权重α和β实现可控平衡。

**移除L_mimic（动态模仿正则化）**在数值上仍保持高ASR和高SR，但Figure 7和Appendix D揭示了其隐蔽性层面的灾难性后果：无L_mimic时，恶意动作的末端执行器速度曲线出现超过**20 m/s**的异常高频振荡尖峰，与正常动作的平滑曲线形成鲜明对比。这种运动学异常使攻击极易被基于动作分布统计的防御手段检测。L_mimic通过强制恶意向量场的L2范数与良性向量场一致（式6），有效抑制了这些异常，使恶意动作的速度剖面与正常动作几乎不可区分。这一发现将隐蔽性从“攻击不被发现”提升到了“攻击行为本身在物理上合理”的更高标准。

### τ条件注入窗口的敏感性分析

Table 5展示了τ_0超参数（式5中的注入窗口上界）对攻击效果的影响。在LIBERO-Goal任务上，τ_0=0.4达到最优平衡：ASR 100%，SR 97.8%。当τ_0减小至0.2时，ASR骤降，表明注入窗口过窄导致向量场劫持不充分，ODE求解器在后续τ阶段能够纠正早期的微小偏转。当τ_0增大至0.6或0.8时，ASR保持高位但SR轻微下降，说明晚期注入开始干扰动作的精细调整阶段，损害良性性能。这一结果验证了核心洞察：**流匹配的早期阶段（低τ）控制动作的全局语义方向，是攻击注入的最优窗口**。

### 防御鲁棒性分析

Tables 3和4评估了两种现有防御手段对FlowHijack的抑制效果。

**目标位置过滤**（Table 3）通过检测末端执行器的异常目标位置来拦截攻击。结果显示，该防御对Pose-Locking（PL）恶意目标有一定效果，因为PL将动作锁定至固定位姿，容易触发位置异常检测。但对Initial-Perturbation（IP）策略效果有限——IP仅施加小幅度常数扰动（δ_A），恶意动作的目标位置仍在正常分布范围内，难以被基于阈值的过滤识别。

**下游清洗微调**（Table 4）尝试通过在干净数据上微调中毒模型来消除后门。结果表明，清洗微调仅能有限降低ASR，无法彻底移除后门效应。这是因为FlowHijack的注入深度位于向量场动态层面，而非浅层特征空间——清洗微调主要调整VLM特征表示，对已被劫持的流匹配动态影响有限。这一发现暗示，针对FlowHijack的有效防御需要设计动态感知的检测机制，而非依赖现有的特征空间清洗策略。

### 触发器鲁棒性

Figure 5和Figure 9展示了上下文感知触发器对常见物理变化的鲁棒性。在尺度变化、位置偏移和物体状态变化三种扰动下，FlowHijack的ASR保持在高位，表明触发器设计对实际部署中的环境变异具有一定容忍度。然而，论文明确指出极端光照、遮挡或域外分布的鲁棒性尚未彻底评估，这是当前工作的一个边界条件。

### 失败模式与局限性

综合实验证据，FlowHijack的主要失败模式可归纳为：

1. **白盒依赖**：攻击设定为白盒微调中毒，需完全访问预训练模型。在黑盒或仅推理API访问的场景下，当前方法无法直接应用。
2. **视觉模态局限**：触发器设计基于视觉语义上下文，对纯文本攻击表现较弱。Figure 6的探针实验表明VLA对文本修改高度鲁棒，这既是攻击的制约（文本触发器无效），也是FlowHijack选择视觉注入的根本原因。
3. **恶意目标的手动定义**：PL和IP策略依赖人工设计的δ或常数扰动，未探索更智能的自动目标生成方法。
4. **环境泛化边界**：仅在LIBERO仿真和有限真实世界场景（桌面与厨房操作）上验证，尚未在移动操作、人机协作等更复杂任务中测试。

### 补充图表

![[assets/figures/papers/paper_list_l2155_https_arxiv_org_abs_2604_09651/figures/005_Table_1.jpg]]
*Table 1: Main comparative results of FlowHijack against the BadVLA baseline, categorized by trigger type. Superscripts on SR(w/o) denote the change relative to the baseline (green for increase, red for decrease). ↑ indicates that higher is better*

![[assets/figures/papers/paper_list_l2155_https_arxiv_org_abs_2604_09651/figures/007_Table_2.jpg]]
*Table 2: Ablation study of our FlowHijack loss components*

![[assets/figures/papers/paper_list_l2155_https_arxiv_org_abs_2604_09651/figures/013_Table_5.jpg]]
*Table 5: Ablation study for the τ -conditioned injection window on Libero goal using Ours(IP). ↑ indicates that higher is better*

![[assets/figures/papers/paper_list_l2155_https_arxiv_org_abs_2604_09651/figures/003_Figure_3.jpg]]
*Figure 3: Visualization of our Context-Aware Triggers and Actions in simulation (LIBERO) and real-world (Franka) environments. The top row shows benign task execution. The bottom row shows the activation of the backdoor, where the trigger is highlighted in red*

![[assets/figures/papers/paper_list_l2155_https_arxiv_org_abs_2604_09651/figures/006_Figure_5.jpg]]
*Figure 5: Robustness analysis of our Context-Aware Trigger*

![[assets/figures/papers/paper_list_l2155_https_arxiv_org_abs_2604_09651/figures/008_Table_3.jpg]]
*Table 3: Defense analysis using Target Position Filtering*

![[assets/figures/papers/paper_list_l2155_https_arxiv_org_abs_2604_09651/figures/009_Table_4.jpg]]
*Table 4: Defense analysis using downstream clean fine-tuning*

![[assets/figures/papers/paper_list_l2155_https_arxiv_org_abs_2604_09651/figures/012_Figure_8.jpg]]
*Figure 8: Real-world evaluation of FlowHijack in two scenarios. (Top) Desktop Manipulation with a Scene Semantic Trigger. (Bottom) Kitchen Manipulation with an Object State Trigger*

## 方法谱系与知识库定位

### 与现有后门攻击的关系

FlowHijack 是首个系统性针对**流匹配视觉-语言-动作（VLA）模型**的后门攻击框架。其核心创新在于将攻击目标从 VLM 的特征空间下移至**向量场动态本身**，这与现有方法形成了根本性差异。

**BadVLA** 是此前适用于离散动作 VLA 的后门攻击框架，其攻击机制依赖于两阶段解耦微调：第一阶段通过最大化触发样本与干净样本 VLM 特征的余弦相似度损失来分离特征空间，第二阶段冻结 VLM 微调动作头。然而，当 BadVLA 被适配至连续动作的流匹配模型时，其攻击效能急剧下降——在 LIBERO-Goal 任务上使用物体状态触发器时，攻击成功率（ASR）仅为 11.2%（Table 1）。这揭示了 BadVLA 的根本瓶颈：**基于离散令牌的操作（如标签翻转）和 VLM 特征空间操纵难以迁移至流匹配的连续动作生成机制**。

FlowHijack 通过直接操纵流匹配策略的向量场动态，绕过了上述 VLM 层面的冲突。其攻击机制建立在流匹配的一个关键性质之上：**向量场在低 τ 阶段（τ ∈ [0, 0.4]）控制动作的全局语义方向**。通过 τ 条件注入仅在早期生成步骤施加攻击损失，并利用 ODE 求解器沿轨迹放大偏差，FlowHijack 可在不破坏后续精细调整的前提下劫持动作生成。

### 方法适用边界

**白盒微调中毒假设**：FlowHijack 假定攻击者拥有对预训练模型的完全访问权限，可在微调阶段注入中毒数据集并修改训练目标。这一设定限制了其在黑盒场景（如仅能查询 API）下的直接应用。

**视觉主导策略依赖**：触发器设计完全基于视觉语义上下文（物体状态触发器、场景语义触发器），依赖 VLA 模型的视觉主导策略。实验表明，VLA 对文本修改具有较强鲁棒性——模型会忽略附加文本，即使在误导性文本存在时仍从视觉推断任务（Figure 6）。这意味着 FlowHijack 对纯文本攻击场景表现较弱。

**任务与环境的泛化边界**：当前验证集中在 LIBERO 基准的桌面操作任务，以及有限的真实世界桌面和厨房操作场景（Figure 8）。尚未在移动操作、人机协作等更复杂的动态环境下测试。此外，恶意目标的定义依赖手动设计的位姿锁定（PL）或常数扰动（IP），未探索自动目标生成。

### 局限与开放问题

**局限性**：
1. 触发器对极端光照、遮挡或域外环境分布的鲁棒性未彻底评估，尽管实验显示对常见尺度、位置和状态变化具有一定鲁棒性（Figure 5）。
2. 攻击设定依赖白盒微调中毒，限制了部分实际场景的应用。
3. 仅在 π0 这一种流匹配 VLA 基础模型上验证，尚未在其他流匹配或扩散策略模型上测试。

**开放问题**：
1. 如何设计针对流匹配向量场动态的防御机制，既能检测早期 τ 阶段的异常偏转又不影响正常动作生成？现有防御分析表明，目标位置过滤（Table 3）和下游清洗微调（Table 4）对 FlowHijack 的抑制有限，更先进的动态感知防御尚待探索。
2. FlowHijack 能否扩展到扩散策略（diffusion policy）等其他连续动作生成模型？两者共享逐步去噪的生成范式，但向量场结构与噪声调度存在差异。
3. 若攻击者无法访问完整模型（黑盒场景），能否通过查询转移或模型抽取实现类似的动态劫持？
4. 在真实世界长时间部署中，上下文触发器可能因环境自然变化（如物体状态切换）而意外激活或失效，如何量化及降低此风险？
5. 能否将动态模仿正则化发展为泛化的连续控制后门隐蔽性度量，用于评估和防御各类动作层面的后门攻击？

## 原文 PDF

![[paperPDFs/CVPR_2026/FlowHijack_A_Dynamics_Aware_Backdoor_Attack_on_Flow_Matching_Vision_Language_Action_Models.pdf]]
