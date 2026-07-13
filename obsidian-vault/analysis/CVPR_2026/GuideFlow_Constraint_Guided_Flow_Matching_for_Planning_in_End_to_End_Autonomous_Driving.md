---
title: "GuideFlow: Constraint-Guided Flow Matching for Planning in End-to-End Autonomous Driving"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/GuideFlow_Constraint_Guided_Flow_Matching_for_Planning_in_End_to_End_Autonomous_Driving.pdf
project_link: null
code_link: "https://github.com/liulin815/GuideFlow"
aliases:
- GuideFlow
tags:
- CVPR_2026
- topic/generative_models_diffusion
- topic/generative_models_diffusion/diffusion_image_video
core_operator: 在流匹配生成过程中直接施加显式硬约束（CVF、CF、RFE），并统一训练流匹配与能量模型（EBM），实现约束满足的自主优化。
primary_logic: 显式约束引导的流匹配同时缓解模式坍塌并保证安全约束；EBM统一训练使模型能够自主在数据流形上发现符合约束的解。
claims:
- GuideFlow在NavSim Navhard测试分割上达到EPDMS 43.0，创下新的SOTA，证明显式约束生成的有效性。
- GuideFlow通过CVF、CF、RFE三种策略在生成过程中直接施加硬约束，有效解决模式坍塌并增强轨迹可行性。
- 消融实验表明CF模块单次校正带来+1.6 EPDMS提升，且与RFE协同实现最佳性能，验证了显式约束和EBM优化的协同作用。
- NavSim Navhard 上 EPDMS = 43.0
---

# GuideFlow: Constraint-Guided Flow Matching for Planning in End-to-End Autonomous Driving

> [!tip] 核心洞察
> 显式约束引导的流匹配同时缓解模式坍塌并保证安全约束；EBM统一训练使模型能够自主在数据流形上发现符合约束的解。

| 字段 | 内容 |
|------|------|
| 中文题名 | GuideFlow：面向端到端自动驾驶规划的约束引导流匹配方法 |
| 英文题名 | GuideFlow: Constraint-Guided Flow Matching for Planning in End-to-End Autonomous Driving |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2511.18729) · [Code](https://github.com/liulin815/GuideFlow) |
| Topic | #topic/generative_models_diffusion #topic/generative_models_diffusion/diffusion_image_video |
| Method | GuideFlow |
| Dataset | NavSim Navhard, Bench2Drive, NuScenes, ADV-NuScenes |

> [!tip] 效果简介
> - NavSim Navhard 上，EPDMS 43.0。
> - NavSim Navhard (w/o Scorer) 上，EPDMS 27.1。
> - Bench2Drive 上，Driving Score / Success Rate 75.21。

## 概要

端到端自动驾驶中的规划任务长期受困于一个核心瓶颈：主流的模仿学习范式使用 L2 损失直接回归专家轨迹，导致多模态轨迹模式坍塌，而现有生成式规划器（如 **DiffusionDrive** (Liao et al., arXiv 2024)、**GoalFlow** (Xing et al., 2025)）虽能缓解模式单一问题，却缺乏显式的安全约束，难以保证生成轨迹满足物理可行性和安全性要求。

**GuideFlow** 针对这一瓶颈提出了约束引导的流匹配生成框架。其核心思路是将规划建模为从高斯先验到可行轨迹分布的流匹配过程，并在此过程中直接施加三类显式硬约束——约束速度场方向、校正流状态、通过能量模型引导轨迹收敛——从而同时解决模式坍塌和安全约束缺失的问题。此外，GuideFlow 将驾驶激进程度建模为可调节的条件信号，使推理时能够灵活控制轨迹风格。

在 NavSim Navhard 测试分割上，GuideFlow 以 **EPDMS 43.0** 创下新的 SOTA（无评分器版本为 27.1，仍具竞争力）；在 Bench2Drive 上取得 75.21 Driving Score 和 51.36% Success Rate；在 ADV-NuScenes 对抗场景下平均碰撞率仅 0.73%。消融实验证实，显式约束模块与能量模型的协同作用是性能提升的关键来源。



端到端自动驾驶旨在直接从传感器输入映射到规划轨迹，省去传统模块化流水线中的中间表示与人工规则。近年来，以模仿学习为核心的端到端规划器（如 **UniAD** (Hu et al., CVPR 2023)、**VAD** (Jiang et al., ICCV 2023)、**SparseDrive** (Sun et al., arXiv 2024)）在开环评测中取得了显著进展，但其核心瓶颈日益凸显：**模仿学习使用的 L2 回归损失天然倾向于拟合专家轨迹的“平均模式”，导致多模态轨迹分布的模式坍塌**——模型在十字路口、动态交互等需要多样化决策的场景中，只能生成单一、保守的轨迹，丧失了对复杂交通情境的应对能力。

为缓解模式坍塌，近期工作转向生成式规划范式。**DiffusionDrive** (Liao et al., arXiv 2024)、**GoalFlow** (Xing et al., 2025)、**HE-Drive** (Wang et al., 2024) 等方法利用扩散模型或流匹配从高斯先验中采样轨迹，通过多模态生成能力覆盖更丰富的驾驶行为。然而，这些生成式规划器存在一个关键缺口：**生成过程缺乏显式的安全约束**。模型虽然能产生多样化的候选轨迹，但无法保证这些轨迹满足碰撞避免、车道保持、道路边界等物理可行性和安全性要求。约束仅以隐式方式编码在训练数据中，导致推理时生成的轨迹可能违反交通规则或进入不可行区域。

上述两类方法的局限可概括为同一根源：**模仿学习导致多模态轨迹模式坍塌，生成模型缺乏显式安全约束，难以保证生成轨迹满足物理可行性和安全性要求**。图 1 直观对比了三种范式的差异：图 (a) 的模仿学习规划器因 L2 损失而坍缩到单一模式；图 (b) 的生成式规划器虽能采样多条轨迹，但无约束引导，常产生违规轨迹；图 (c) 的 GuideFlow 则直接在生成过程中施加显式约束，确保采样轨迹满足特定安全需求。

GuideFlow 的核心动机由此确立：**在流匹配生成过程中直接施加显式硬约束，并统一训练流匹配与能量模型（EBM），实现约束满足的自主优化**。具体而言，GuideFlow 提出三种约束生成策略——约束速度场（CVF）、约束流状态（CF）、能量模型精炼（RFE）——在采样的不同阶段干预生成过程，使轨迹从高斯噪声出发，逐步收敛到既多样化又满足安全约束的解空间。此外，GuideFlow 引入基于奖励的激进程度条件信号（RAS），使模型在推理时可灵活切换激进与保守驾驶风格，进一步增强了规划的可控性。

这一设计理念的核心洞察在于：**显式约束引导的流匹配同时缓解模式坍塌并保证安全约束；EBM 统一训练使模型能够自主在数据流形上发现符合约束的解**。通过在生成过程中注入硬约束，而非依赖后处理筛选或隐式编码，GuideFlow 在保持多模态生成能力的同时，从根本上提升了轨迹的可行性与安全性。



## 核心方法与创新机理

GuideFlow 的核心创新在于将**显式安全约束直接嵌入流匹配生成过程**，从根本上区别于两类既有范式：(1) 基于回归的模仿学习规划器（如 **UniAD** (Hu et al., CVPR 2023)、**VAD** (Jiang et al., ICCV 2023)）使用 L2 损失直接模仿专家轨迹，天然面临多模态模式坍塌；(2) 生成式规划器（如 **DiffusionDrive** (Liao et al., arXiv 2024)、**GoalFlow** (Xing et al., 2025)）虽从学习分布中采样轨迹以缓解模式坍塌，但缺乏显式生成约束，常导致交通违规。GuideFlow 通过以下四个 changed slots 实现突破：

### 1. 规划架构：从模仿回归到约束流匹配

GuideFlow 将规划建模为基于流匹配的生成式过程。与 UniAD 等基于回归的模仿学习不同，流匹配从高斯先验 $\pi_0$ 出发，通过学习的向量场 $v_\theta$ 沿概率路径演化生成多样化轨迹，从机制层面缓解模式坍塌。其训练目标为整流流损失：

$$\mathcal{L}_{\mathrm{RF}} = \mathbb{E}_{t, x_0 \sim \pi_0, x_1 \sim \pi_1} || v_\theta(x_t, t) - (x_1 - x_0) ||^2$$

推理时通过欧拉积分采样：

$$x^{(k+1)} = x^{(k)} + v_\theta(x^{(k)}, t_k) \Delta t, \quad x^0 \sim \pi_0$$

这一架构使模型天然支持多模态输出，并为后续约束注入提供了可操作的生成中间态。

### 2. 约束注入方式：从隐式编码到显式硬约束

这是 GuideFlow 最核心的 changed slot。先前生成式方法（如 DiffusionDrive）仅依赖隐式条件编码，无法严格保证轨迹满足安全约束。GuideFlow 提出三种互补的显式约束策略，在生成过程中直接干预：

- **CVF (Constraining the Velocity Field)**：在速度场预测后，通过方向校正将运动方向对齐到约束满足的参考方向，同时最小化幅度变化：

$$v_t^{*} = v_t - \frac{2 \lambda v_t \cdot v_t^c}{||v_t^c||^2} v_t^c$$

- **CF (Constraining the Flow States)**：在推理后期（第 $k_c$ 步起），将流状态直接替换为约束锚点，实现一次性校正，确保终点位于可行区域：

$$\boldsymbol{x}^{(k+1)} = \boldsymbol{x}^{(k)} + v_{\boldsymbol{\theta}}(\boldsymbol{x}^{(k)}, t_k) \Delta t, \quad k = k_c, ..., K$$

- **RFE (Refining the Flow by EBM)**：构建能量函数 $E_\theta(x_t) = || j(f_{t>1}(x_t)) - j(x_t) ||^2$，通过约束违规度量使可行轨迹具有低能量，并在采样后期引入能量梯度引导轨迹向低能量（约束满足）区域收敛：

$$\boldsymbol{x}^{(k+1)} = \boldsymbol{x}^{(k)} + v_{\boldsymbol{\theta}}(\boldsymbol{x}^{(k)}, t_k) \Delta t - \eta(t_k) \nabla_{\boldsymbol{x}} E_{\boldsymbol{\theta}}(\boldsymbol{x}^{(k)})$$

EBM 训练损失 $\mathcal{L}_{\mathrm{RFE}} = E_\theta(x^{(1)}) - E_\theta(x_1)$ 同时增大不可行样本能量、降低可行样本能量，使流匹配与能量模型在统一训练中协同优化。

### 3. 模式坍塌缓解：从单模态回归到多模态生成

传统模仿学习使用 L2 损失回归单一轨迹，导致模型在歧义场景中输出“平均轨迹”（模式坍塌）。GuideFlow 通过流匹配从随机噪声出发，结合分类器自由引导注入多样化条件信号：

$$v_{\theta}^{\mathrm{guide}}(x_t, t, c, \gamma) = (1 - \gamma) v_{\theta}(x_t, t) + \gamma v_{\theta}(x_t, t, c)$$

消融实验证实，Plan Anchor 作为动态条件信号优于 Goal Point 和 Driving Command，获得 29.0 EPDMS 和 75.21 Driving Score。CF 模块单次校正带来 +1.6 EPDMS 提升，且与 RFE 组合达到最佳性能（27.1 EPDMS、75.21 Driving Score、51.36% Success Rate），验证了显式约束与 EBM 优化的协同作用。

### 4. 驾驶风格控制：从无调制到奖励条件化

先前方法缺乏对驾驶风格的显式控制。GuideFlow 引入 **RAS (Reward as Style Condition)** 模块，利用 NavSim 的激进程度分数（EP，定义为沿车道中心线单位时间行驶距离，值域 [0,1]）作为条件信号，在推理时控制轨迹风格。消融实验显示 RAS 使 EP 从 79.6 升至 82.3，但 EPDMS 下降 0.8，揭示了安全与效率之间的权衡——这一 trade-off 本身正是风格可控性的体现。



GuideFlow 是一种基于流匹配的端到端自动驾驶规划器，其核心设计理念是将显式安全约束直接嵌入轨迹生成过程，从而在保证多模态多样性的同时满足物理可行性与安全性要求。整体架构如图 2 所示，由以下模块级联构成：

**感知编码 → 条件流生成 → 约束引导采样 → 轨迹输出**

### 1. 感知模块

多视图图像首先通过骨干网络编码为鸟瞰图（BEV）特征，随后感知模块从中查询生成两类结构化令牌：
- **Agent Tokens**：编码周围动态智能体的位置、朝向、速度等信息。
- **Map Tokens**：编码车道线、道路边界、可行驶区域等静态地图元素。

这两类令牌作为场景表示，为后续的轨迹生成提供条件信号。

### 2. 感知条件流匹配生成器

流匹配生成器是 GuideFlow 的核心引擎。其工作流程为：
1. **状态嵌入**：将当前流状态 $x_t$ 与时间步 $t$ 通过 MLP 映射为潜在表示 $h_t = \text{MLP}_\theta(x_t) + \ell_\theta(t)$。
2. **场景融合**：潜在表示通过顺序交叉注意力机制与 Agent Tokens 和 Map Tokens 交互：
   $$h_t \leftarrow \text{CrossAttn}_\theta(h_t, Q_{\text{agent}}), \quad h_t \leftarrow \text{CrossAttn}_\theta(h_t, Q_{\text{map}})$$
3. **速度场预测**：融合后的表示解码为速度场 $v_\theta(x_t, t)$。

训练目标采用整流流匹配损失：
$$\mathcal{L}_{\mathrm{RF}} = \mathbb{E}_{t, x_0 \sim \pi_0, x_1 \sim \pi_1} \| v_\theta(x_t, t) - (x_1 - x_0) \|^2$$
该损失学习从高斯先验 $\pi_0$ 到专家轨迹分布 $\pi_1$ 的线性插值路径上的速度场。推理时，从随机噪声 $x^{(0)} \sim \pi_0$ 出发，通过欧拉积分迭代采样：
$$x^{(k+1)} = x^{(k)} + v_\theta(x^{(k)}, t_k) \Delta t$$

### 3. 分类器自由引导

为注入驾驶意图与风格控制，GuideFlow 采用分类器自由引导框架。在训练和推理中，速度场预测接受动态条件信号 $c$（如规划锚点、目标点、驾驶命令），并通过引导尺度 $\gamma$ 调节条件影响强度：
$$v_\theta^{\mathrm{guide}}(x_t, t, c, \gamma) = (1 - \gamma) v_\theta(x_t, t) + \gamma v_\theta(x_t, t, c)$$

### 4. 约束引导采样

这是 GuideFlow 区别于其他生成式规划器的关键创新。在采样过程中，三种互补策略直接施加显式硬约束（图 3）：

- **CVF（约束速度场）**：将预测速度场向约束满足的参考方向调整，同时最小化幅度变化：
  $$v_t^* = v_t - \frac{2\lambda v_t \cdot v_t^c}{\|v_t^c\|^2} v_t^c$$

- **CF（约束流状态）**：在推理后期（$k = k_c, \dots, K$），将当前流状态替换为约束锚点后继续采样，保证终点位于可行区域。

- **RFE（能量模型精炼）**：引入能量函数 $E_\theta(x_t)$ 度量约束违规程度，在采样后期通过梯度引导样本向低能量（约束满足）区域收敛：
  $$x^{(k+1)} = x^{(k)} + v_\theta(x^{(k)}, t_k) \Delta t - \eta(t_k) \nabla_x E_\theta(x^{(k)})$$
  EBM 与流匹配联合训练，损失函数为：
  $$\mathcal{L}_{\mathrm{RFE}} = E_\theta(x^{(1)}) - E_\theta(x_1)$$
  该损失增大不可行样本的能量、降低可行样本的能量。

### 5. 驾驶风格调制

GuideFlow 引入基于奖励的激进程度条件信号（RAS），将 NavSim 中的自车进度分数（EP，定义为沿车道中心线单位时间行驶距离，取值范围 $[0,1]$）作为条件输入，使推理时可在激进与保守驾驶风格间切换。

### 关键设计动机

与现有方法相比，GuideFlow 的架构选择直指两个瓶颈：
- **模式坍塌**：模仿学习（如 **UniAD** Hu et al., CVPR 2023；**VAD** Jiang et al., ICCV 2023）使用 L2 损失直接回归专家轨迹，导致多模态分布坍缩为均值。GuideFlow 从高斯先验出发，通过流匹配生成多样化候选，结合分类器自由引导保持多模态性。
- **约束缺失**：生成式规划器（如 **DiffusionDrive** Liao et al., arXiv 2024）虽能采样多模态轨迹，但缺乏显式约束，常产生违反交通规则的轨迹。GuideFlow 通过 CVF、CF、RFE 三级约束机制，在生成过程中直接保证轨迹的物理可行性与安全性。

### 补充图表

![[assets/figures/papers/paper_list_l2516_https_arxiv_org_abs_2511_18729/figures/001_Figure_1.jpg]]
*Figure 1: Comparison of GuideFlow with prior methods. (a) Imitative E2E Planners [14, 19, 36, 38], which directly imitate expert trajectories using an L2 loss, are susceptible to the inherent mode collapse problem in imitation learning. (b) Generative E2E Planners [27, 41]. These methods sample future trajectories directly from a learned distribution but lack explicit generation constraints, often resulting in traffic violations. (c) GuideFlow directly guides the generative process with explicit constraints, ensuring the sampled trajectories satisfy specific requirements*



GuideFlow 的规划管线由三个核心模块构成：感知条件速度场生成器、分类器自由引导、以及安全约束采样过程。其核心创新在于将显式安全约束直接嵌入流匹配生成过程，而非依赖隐式约束编码。

### 3.1 整流流匹配基础

GuideFlow 采用整流流匹配（Rectified Flow Matching）作为轨迹生成的基本框架。给定先验分布 $\pi_0$（标准高斯）和目标数据分布 $\pi_1$（专家轨迹），模型学习一个速度场 $v_\theta$，使得样本沿线性插值路径演化：

$$x_t = (1 - t)x_0 + tx_1, \quad t \in [0, 1]$$

训练目标为最小化预测速度与真实线性速度之间的差异：

$$\mathcal{L}_{\mathrm{RF}} = \mathbb{E}_{t, x_0 \sim \pi_0, x_1 \sim \pi_1} \| v_\theta(x_t, t) - (x_1 - x_0) \|^2$$

推理时，从高斯噪声 $x^{(0)} \sim \pi_0$ 出发，通过欧拉积分沿学习到的速度场逐步采样：

$$x^{(k+1)} = x^{(k)} + v_\theta(x^{(k)}, t_k) \Delta t$$

### 3.2 感知条件速度场生成器

速度场生成器将流状态 $x_t$ 与时间步 $t$ 映射为潜在表示，并通过交叉注意力融合场景上下文。首先计算状态嵌入：

$$h_t = \mathrm{MLP}_\theta(x_t) + \ell_\theta(t)$$

其中 $\ell_\theta(t)$ 为时间步的正弦位置编码。随后，$h_t$ 依次与感知模块输出的 Agent Tokens 和 Map Tokens 进行交叉注意力：

$$h_t \leftarrow \mathrm{CrossAttn}_\theta(h_t, Q_{\mathrm{agent}}), \quad h_t \leftarrow \mathrm{CrossAttn}_\theta(h_t, Q_{\mathrm{map}})$$

融合后的表示通过解码器预测当前时刻的速度场 $v_\theta(x_t, t)$。

### 3.3 分类器自由引导

为实现灵活的条件控制，GuideFlow 采用分类器自由引导框架。设 $c$ 为条件信号（如规划锚点、目标点、驾驶命令），无条件和条件速度场通过引导尺度 $\gamma$ 线性组合：

$$v_\theta^{\mathrm{guide}}(x_t, t, c, \gamma) = (1 - \gamma) v_\theta(x_t, t) + \gamma v_\theta(x_t, t, c)$$

训练时以一定概率随机丢弃条件 $c$，使单一模型同时学习条件与无条件分布。推理时通过调节 $\gamma$ 控制条件对生成轨迹的影响强度。

### 3.4 约束生成三策略

GuideFlow 提出三种互补的显式约束机制，在生成过程中直接保证轨迹满足安全与物理可行性要求。

**CVF（约束速度场）**：在每一步采样前，将预测速度场 $v_t$ 向约束满足的参考方向 $v_t^c$ 校正，同时最小化幅度变化：

$$v_t^* = v_t - \frac{2\lambda v_t \cdot v_t^c}{\|v_t^c\|^2} v_t^c$$

其中 $\lambda$ 控制校正强度。该操作保证运动方向对齐约束，但不强制终点位置。

**CF（约束流状态）**：在推理后期（步数 $k \geq k_c$），将当前流状态直接替换为约束锚点后继续采样：

$$x^{(k+1)} = x^{(k)} + v_\theta(x^{(k)}, t_k) \Delta t, \quad k = k_c, \dots, K$$

此截断式策略确保轨迹终点落在可行区域内，相当于一次硬校正。

**RFE（能量模型精炼）**：引入能量函数 $E_\theta(x_t)$ 度量轨迹的约束违规程度，可行轨迹被赋予低能量，不可行轨迹被赋予高能量。能量代理定义为约束违规度量的平方：

$$E_\theta(x_t) = \| j(f_{t>1}(x_t)) - j(x_t) \|^2$$

其中 $j(\cdot)$ 为约束违规度量函数。训练时通过对比损失拉开可行与不可行样本的能量差距：

$$\mathcal{L}_{\mathrm{RFE}} = E_\theta(x^{(1)}) - E_\theta(x_1)$$

推理时，在采样后期引入能量梯度引导，使样本向低能量（约束满足）区域收敛：

$$\boldsymbol{x}^{(k+1)} = \boldsymbol{x}^{(k)} + v_\boldsymbol{\theta}(\boldsymbol{x}^{(k)}, t_k) \Delta t - \eta(t_k) \nabla_{\boldsymbol{x}} E_\boldsymbol{\theta}(\boldsymbol{x}^{(k)})$$

其中 $\eta(t_k)$ 为能量引导步长。三种策略协同工作：CVF 校正运动方向，CF 保证终点可行，RFE 引导整体轨迹向约束满足流形收敛。

### 3.5 奖励作为风格条件

GuideFlow 引入基于 NavSim 的激进程度分数 EP（Ego Progress），定义为自车沿车道中心线单位时间行驶距离，取值范围 $[0, 1]$。EP 作为条件信号输入分类器自由引导框架，使模型在推理时可通过调节条件值控制轨迹的驾驶风格——高 EP 对应激进驾驶，低 EP 对应保守驾驶。

### 补充图表

![[assets/figures/papers/paper_list_l2516_https_arxiv_org_abs_2511_18729/figures/003_Figure_3.jpg]]
*Figure 3: Three strategies of Constrained Generation, which include Constraining the Velocity Field (CVF), Constraining the Flow States (CF) and Refining the Flow by EBM (RFE)*



## 实验与关键发现

### 主要结果

GuideFlow 在多个闭环与开环评测基准上均取得领先性能，核心优势源于将显式安全约束直接嵌入流匹配生成过程。

**NavSim 闭环评测。** NavSim Navhard 分割是该领域公认的高难度闭环评测基准。在不使用轨迹评分器（Scorer）的条件下，GuideFlow 以 ResNet34 为视觉骨干获得 **EPDMS 27.1**（Table 1）。当接入 GTRS-Dense 轨迹评分器进行后选时，GuideFlow 达到 **EPDMS 43.0**，创下该基准的 SOTA 成绩（Table 1）。这一结果验证了显式约束生成在闭环安全规划中的有效性——约束引导的流匹配不仅缓解了模仿学习的模式坍塌，更在复杂场景下保证了轨迹的物理可行性与安全性。

**Bench2Drive 闭环评测。** 在 Bench2Drive 数据集上，GuideFlow 取得 **Driving Score 75.21** 与 **Success Rate 51.36%**（Table 2）。与 Hydra-MDP（Li et al., arXiv 2024）等多模态模仿学习方法和 DiffusionDrive（Liao et al., arXiv 2024）等生成式方法相比，GuideFlow 在驾驶得分和成功率上均表现出显著优势，证明约束引导的流匹配在多样化驾驶场景中具有更强的泛化能力。

**NuScenes 与 ADV-NuScenes 开环评测。** 在 NuScenes 验证集上，GuideFlow 的平均碰撞率仅为 **0.07%**；在更具对抗性的 ADV-NuScenes 验证集上，平均碰撞率为 **0.73%**（Table 3）。极低的碰撞率表明，CVF、CF 和 RFE 三种约束策略在生成过程中有效抑制了不安全轨迹的产生，即使在对抗场景下也能维持较高的安全水平。

**定性对比。** 与 DiffusionDrive 的可视化对比（Figure 4）显示，GuideFlow 生成的轨迹在车道保持、换道平滑性和碰撞规避等方面均表现出更强的约束遵从性。这进一步佐证了显式约束引导相较于隐式编码的优势：模型并非被动模仿数据分布，而是在生成过程中主动寻求满足安全约束的解。

### 消融实验

为厘清各模块的独立贡献与协同效应，论文在 NavSim、Bench2Drive、NuScenes 和 ADV-NuScenes 四个基准上进行了系统消融（Table 4–6）。

![[assets/figures/papers/paper_list_l2516_https_arxiv_org_abs_2511_18729/figures/007_Table_4.jpg]]
*Table 4: Ablation studies of Dynamic Condition Signals in GuideFlow over NavSim [7] HavHard Split, Bench2Drive [17], NuScenes [2] and ADV-NuScenes [43]. “PA” denotes “Plan Anchor”, “GP” denotes “Goal Point” and “CM” denotes “Driving Command”*

**动态条件信号。** 在分类器自由引导框架下，论文对比了三种动态条件信号：Plan Anchor（PA）、Goal Point（GP）和 Driving Command（CM）。以 PA 为条件的变体在所有基准上均取得最优性能——EPDMS 29.0、Driving Score 75.21（Table 4）。PA 提供的是稠密的未来路径参考，比稀疏的目标点或离散驾驶命令包含更丰富的规划意图信息，因此对流匹配的引导效果最佳。

**约束生成模块。** Table 5 揭示了各约束策略的独立贡献与组合效应：
- **CF 模块**：单独引入流状态校正（CF）带来 **+1.6 EPDMS** 和 **+0.45% Success Rate** 的提升。CF 在推理后期将流状态直接替换为约束锚点，以极小的计算代价实现了一次性硬约束校正。
- **CF + RFE 组合**：CF 与 EBM 引导（RFE）协同工作达到最优性能——EPDMS 27.1、Driving Score 75.21、Success Rate 51.36%。RFE 通过能量函数引导生成轨迹向低能量（约束满足）区域收敛，弥补了 CF 仅在单点校正的局限，实现了全局约束优化。
- **CVF 模块**：单独的速度场校正（CVF）提升幅度较小，但其与 CF、RFE 联合使用时进一步增强了运动方向的约束一致性。

**驾驶风格调制。** RAS（Reward as Style Condition）模块将 NavSim 的激进程度分数（EP）作为条件信号，使模型可在推理时控制驾驶风格。实验显示，RAS 使 EP 从 79.6 升至 82.3，但 EPDMS 下降 0.8（Table 5）。这表明激进程度与安全性之间存在固有权衡：更激进的驾驶风格提升了通行效率，但增加了碰撞风险。该权衡为用户提供了可调节的安全-效率边界。

**超参数敏感性。** Table 6 展示了关键超参数的影响：
- **能量引导权重 λ**：当 λ 从 0.1 增大至 0.5 时，EPDMS 从 24.5 急剧下降至 13.5。过强的能量引导会扭曲流匹配的生成分布，导致轨迹质量退化。
- **校正步 k_c**：在 k_c = 40 时取得最优 EPDMS 27.1。过早校正（k_c 过小）会干扰流匹配的早期探索，过晚校正（k_c 过大）则无法有效约束最终轨迹。该参数需要在生成过程的探索-约束之间取得平衡。

### 失败模式与局限性

尽管 GuideFlow 在多个基准上表现优异，论文也揭示了若干局限与待解决问题：

1. **采样效率瓶颈**：流匹配需要多步 ODE 积分生成轨迹，加速采样会降低规划性能。论文指出需要引入 reflow 或 meanflow 等加速技术以提升推理速度，这是实现实时部署的关键挑战。

2. **后选评分器的依赖**：当前最优结果（EPDMS 43.0）依赖 GTRS-Dense 轨迹评分器进行后选，增加了推理开销，且其他基线方法可能未采用相同配置，引入了公平性争议。无评分器的版本（EPDMS 27.1）虽仍具竞争力，但与 SOTA 存在差距。

3. **模拟器到真实世界的迁移**：实验主要在 NavSim、Bench2Drive 等模拟器上进行，真实世界部署的性能尚待验证。模拟器中的传感器噪声、动态交互和边缘场景与真实环境存在分布差异。

4. **EBM 训练的收敛性**：能量模型引导（RFE）的有效性依赖于 EBM 训练的收敛质量。论文未详细分析 EBM 在不同场景下的能量景观特性，其在极端边界场景中是否会发生坍缩仍需进一步研究。

### 补充图表

![[assets/figures/papers/paper_list_l2516_https_arxiv_org_abs_2511_18729/figures/004_Table_1.jpg]]
*Table 1: Planning results on the NavSim[7] Navhard split. ∗ denotes results reproduced with the official code repository or official checkpoint. The Scorer configuration is aligned with GTRS-Dense [24]. † refers to the adjustment of the trajectory scoring strategy during inference. Further details can be found in the Appendix*

![[assets/figures/papers/paper_list_l2516_https_arxiv_org_abs_2511_18729/figures/005_Table_2.jpg]]
*Table 2: Planning results of E2E-AD Methods on the Bench2Drive [17] datasets. ∗ represents the model benefits from expert feature distillation [16]*

![[assets/figures/papers/paper_list_l2516_https_arxiv_org_abs_2511_18729/figures/006_Table_3.jpg]]
*Table 3: Planning results on the NuScenes [2] and ADV-NuScenes [43] validation dataset. C.R denotes the Collision Rate. ∗ denotes results reproduced with the official checkpoint*

![[assets/figures/papers/paper_list_l2516_https_arxiv_org_abs_2511_18729/figures/008_Table_5.jpg]]
*Table 5: Ablation studies of different modules in GuideFlow over NavSim [7] HavHard Split, Bench2Drive [17], NuScenes [2] and ADV-NuScenes [43]. “EP” stands for Ego Progress subscore. “CVF” denotes “Constraining the Velocity Field” module, “CF” denotes “Constraining the Flow State”, “RFE” denotes “Refining the Flow by EBM” and “RAS” denotes “Reward as Style Condition”*

![[assets/figures/papers/paper_list_l2516_https_arxiv_org_abs_2511_18729/figures/009_Figure_4.jpg]]
*Figure 4: Visual comparison between DiffusionDrive [27] and our GuideFlow across multiple driving scenarios. GuideFlow generates trajectories that exhibit improved adherence to lane follow, smoother maneuver transitions, and stronger compliance with safety constraints such as collision avoidance and road boundary preservation*

![[assets/figures/papers/paper_list_l2516_https_arxiv_org_abs_2511_18729/figures/010_Table_6.jpg]]
*Table 6: The hyper-parameter λ, kc and K effects on GuideFlow’s performance for the NavSim Dataset*



## 定位与知识库关联

### 1. 与现有工作的关系

GuideFlow 处于端到端自动驾驶规划方法的演进脉络中，其核心突破在于将**约束满足从隐式后处理提升为生成过程的内在机制**。

**模仿学习规划器**构成了早期基线。**UniAD**（Hu et al., CVPR 2023）和 **VAD**（Jiang et al., ICCV 2023）采用基于回归的模仿学习直接拟合专家轨迹，但 L2 损失在多模态驾驶行为（如路口转向存在多种合理路径）下会导致模式坍塌——模型倾向于输出所有可能轨迹的“平均”，而非其中任一可行解。**ThinkTwice**（Jia et al., CVPR 2023）和 **DriveAdapter**（Jia et al., ICCV 2023）通过改进场景编码缓解了部分问题，但本质上仍受限于单模态回归范式。**SparseDrive**（Sun et al., arXiv 2024）和 **Hydra-MDP**（Li et al., arXiv 2024）引入了多模态输出，但约束条件仅通过隐式编码注入，缺乏对生成轨迹的显式安全保证。

**生成式规划器**是更近期的探索方向。**DiffusionDrive**（Liao et al., arXiv 2024）将扩散模型引入轨迹生成，从噪声分布出发采样多模态轨迹，在模式坍塌问题上取得进展，但其生成过程缺乏显式约束，导致采样轨迹可能违反交通规则或物理边界。**GoalFlow**（Xing et al., 2025）和 **HE-Drive**（Wang et al., 2024）同样属于生成范式，但约束注入方式仍以隐式条件编码为主。**Diff-VLA**（Jiang et al., arXiv 2025）尝试将视觉-语言-动作模型与扩散生成结合，但在安全约束的显式建模上未见突破。

GuideFlow 的关键差异在于：**将显式硬约束直接嵌入流匹配的生成动力学中**，而非将约束作为损失项或后处理步骤。这一设计使模型能够在保持多模态生成能力的同时，确保输出轨迹满足运动方向、终点位置和物理边界等硬性要求。Figure 1 的对比示意图清晰呈现了这一范式差异：模仿学习规划器因模式坍塌输出不安全的“平均轨迹”，生成式规划器虽有多样性但缺乏约束引导，而 GuideFlow 在多样化生成中直接施加约束，使采样轨迹天然位于可行域内。

### 2. 适用边界

GuideFlow 的适用边界由以下因素界定：

- **任务场景**：面向端到端自动驾驶的运动规划，输入为多视图图像，输出为自车未来轨迹。模型假设感知模块能提供足够的场景表征（Agent Tokens 和 Map Tokens），在极端遮挡或传感器失效场景下的鲁棒性未经验证。
- **约束类型**：当前框架支持运动学约束（速度方向校正 CVF）、离散状态约束（流状态校正 CF）和能量约束（EBM 引导 RFE）。对于涉及复杂交互博弈（如多车协商通过无信号路口）的场景，约束建模的充分性需要进一步评估。
- **部署条件**：流匹配的迭代采样（通常需要 50–100 步欧拉积分）带来推理延迟，在 NavSim 等模拟器上的实时性表现尚可，但未报告在嵌入式平台上的推理速度。论文明确指出加速采样会降低规划性能，需要后续引入 reflow/meanflow 等技术。
- **数据依赖**：模型训练依赖专家轨迹数据，在分布外场景（如罕见交通规则或非结构化道路）的泛化能力未经验证。实验主要在 NavSim、Bench2Drive 等模拟器上进行，真实世界部署的性能尚待验证。

### 3. 局限与开放问题

#### 3.1 已知局限

1. **采样效率与性能的权衡**：流匹配需要多步积分采样，加速采样（减少积分步数）会导致规划性能下降。论文在 Table 6 中展示了超参数 K（总采样步数）的影响，但未提供在低步数下维持性能的解决方案。

2. **依赖外部轨迹评分器**：在 NavSim Navhard 分割上的最优结果（EPDMS 43.0）使用了 GTRS-Dense 轨迹评分器进行后选。虽然无评分器版本（EPDMS 27.1）仍具竞争力，但评分器的引入增加了推理开销，且在其他基线方法中可能未采用，带来公平性问题。论文已明确标注配置，但完全去除后选 scorer 的端到端约束满足尚未实现。

3. **EBM 训练的收敛性**：RFE 模块通过能量函数引导轨迹向低能量区域收敛，但 EBM 训练本身面临模式覆盖和训练稳定性挑战。论文未详细分析 EBM 在不同场景下的能量景观，以及是否存在某些场景下能量函数坍缩导致多样性丧失的风险。

4. **风格调制的安全-效率权衡**：RAS 模块通过激进程度条件信号（EP）控制驾驶风格，但消融实验（Table 5）表明，引入 RAS 后 EP 从 79.6 升至 82.3，而 EPDMS 下降 0.8，揭示了风格调制中安全与效率的内在张力。如何在保证安全的前提下实现灵活的驾驶风格控制，仍是开放问题。

#### 3.2 开放问题

1. **实时推理的可行性**：能否在不牺牲性能的前提下提升采样速度？reflow/meanflow 等加速技术是否适用于约束引导的流匹配框架？这决定了方法在实车部署中的实用性。

2. **无后处理的端到端约束满足**：能否通过更强的约束建模（如将 GTRS-Dense 的评分逻辑内化为可微约束）完全去除后选 scorer，实现真正的端到端约束生成？

3. **对抗场景的泛化边界**：在 ADV-NuScenes 上的碰撞率（0.73%）表现优异，但极端对抗场景（如恶意切入、紧急制动）下的安全保证边界如何？EBM 能量函数是否能在这些场景下提供足够的约束力？

4. **多模态与约束的深层关系**：流匹配从高斯先验出发生成多样化轨迹，约束机制可能在某些场景下过度限制多样性。如何在约束满足与多模态保持之间建立更精细的平衡机制？

5. **跨域迁移能力**：当前框架在模拟器上验证，向真实世界的迁移涉及域差异、传感器噪声和动态环境不确定性。约束建模的鲁棒性在真实场景中是否成立，需要实车验证。



## 原文 PDF

![[paperPDFs/CVPR_2026/GuideFlow_Constraint_Guided_Flow_Matching_for_Planning_in_End_to_End_Autonomous_Driving.pdf]]
