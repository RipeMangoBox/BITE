---
title: "Hydra-MDP: End-to-end Multimodal Planning with Multi-target Hydra-Distillation"
type: paper
paper_level: A
venue: CVPR
year: 2024
pdf_ref: paperPDFs/CVPR_2024/Hydra_MDP_End_to_end_Multimodal_Planning_with_Multi_target_Hydra_Distillation.pdf
aliases:
- HM
- Hydra-MDP
tags:
- CVPR_2024
- topic/reinforcement_learning_planning_agents
- topic/reinforcement_learning_planning_agents/planning_control
core_operator: "通过多教师知识蒸馏（Hydra-Distillation），将人类驾驶和基于规则的教师模型的闭环度量知识传递给学生模型，用可微分的成本预测取代不可微的后处理，实现端到端的多目标学习。"
primary_logic: "利用多教师蒸馏，学生模型直接从传感器观测预测每个候选轨迹的仿真得分，并通过加权组合进行轨迹选择，避免了不可微分的后处理，从而在统一的端到端框架中同时优化模仿行为和闭环安全性。"
claims:
- "Hydra-MDP 在 Navtest 上显著优于所有端到端基线，Vadv2-V8192 的 PDM Score 为 80.9，Hydra-MDP-V8192-W-EP 达到 86.5，提升 5.6 分。"
- "多目标蒸馏（Hydra-MDP）优于单目标 PDM 分数蒸馏（Hydra-MDP-PDM），PDM Score 从 80.2 提升至 83.0。"
- "置信度加权（W）和 EP 蒸馏进一步提升闭环表现，最终模型比无加权版本提高 3.5 分（86.5 vs 83.0）。"
- "Navtest Split 上 PDM Score = 86.5 (Hydra-MDP-V8192-W-EP)"
---

# Hydra-MDP: End-to-end Multimodal Planning with Multi-target Hydra-Distillation

> [!tip] 核心洞察
> 利用多教师蒸馏，学生模型直接从传感器观测预测每个候选轨迹的仿真得分，并通过加权组合进行轨迹选择，避免了不可微分的后处理，从而在统一的端到端框架中同时优化模仿行为和闭环安全性。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | Hydra-MDP：基于多目标Hydra蒸馏的端到端多模态规划 |
| 英文题名 | Hydra-MDP: End-to-end Multimodal Planning with Multi-target Hydra-Distillation |
| 会议/期刊 | CVPR 2024 |
| Links | [paper](https://arxiv.org/abs/2406.06978); [GitHub](https://github.com/NVlabs/Hydra-MDP) |
| Topic | #topic/reinforcement_learning_planning_agents #topic/reinforcement_learning_planning_agents/planning_control |
| Method | Hydra-MDP |
| Dataset | Navtest Split |

> [!tip] 效果简介
> - Navtest Split 上，PDM Score 为 86.5 (Hydra-MDP-V8192-W-EP)，对比 80.9 (Vadv2-V8192)，变化 +5.6。
> - Navtest Split 上，PDM Score 为 86.5 (Hydra-MDP-V8192-W-EP)，对比 78.0 (Transfuser)，变化 +8.5。

## 概述

端到端自动驾驶规划长期受困于开环模仿学习的隐式偏差：模型仅模仿人类驾驶轨迹，却无法直接优化闭环安全性、舒适性与交通规则遵守等多维评价指标。现有方法将不可微分的后处理代价函数置于训练循环之外，导致感知与规划之间缺乏端到端的多目标协同优化。

Hydra-MDP 的核心思路是**多教师 Hydra 蒸馏**：同时引入人类驾驶教师和基于规则的闭环仿真教师，将不可微的后处理代价函数替换为可微分的神经网络预测头，使学生模型直接从传感器观测中预测每条候选轨迹的仿真得分。这一范式转变的关键在于，轨迹选择不再依赖测试时的后处理，而是通过置信度加权的多目标得分组合在统一的端到端框架内完成。

在 Navtest 基准上，Hydra-MDP 取得了显著突破：最终模型 Hydra-MDP‑V8192‑W‑EP 的 PDM Score 达到 **86.5**，较官方端到端基线 Vadv2 的 80.9 提升 **5.6 分**，较 Transfuser 的 78.0 提升 **8.5 分**，并凭借该方案在 Navsim 挑战赛中获得第一名。消融实验进一步揭示了两个关键因果机制：多目标蒸馏优于单目标 PDM 总分蒸馏（83.0 vs 80.2），置信度加权与自车进度蒸馏的引入带来额外 3.5 分的增益。

该方法位于端到端多模态规划与知识蒸馏的交叉地带，其感知网络基于 Transfuser 构建，轨迹解码器采用固定规划词汇表，多教师蒸馏头则从 PDM‑Closed 规则教师获取闭环度量知识。需注意，动态避免碰撞指标因实现问题被忽略，且模型集合带来的推理成本增加是实际部署中需权衡的因素。

## 背景与动机

端到端自动驾驶旨在直接从传感器输入映射到规划轨迹，省去传统模块化流水线中的中间表示与手工规则。然而，现有端到端规划方法普遍受困于一个核心瓶颈：**开环评价的隐式偏差**。主流范式以模仿学习为基础，通过最小化预测轨迹与人类驾驶轨迹之间的距离来训练模型，但训练目标与闭环部署时的安全、效率、舒适、交规合规等多维评价指标之间存在根本性错位。

这一错位在技术层面表现为三个递进的缺陷。第一，**单模态单目标学习**仅回归一条确定性轨迹，损失函数为 $\mathcal{L} = \mathcal{L}_{im}(T^*, \hat{T})$，无法捕捉驾驶场景的多模态特性。第二，**多模态单目标学习**虽通过损失求和 $\mathcal{L} = \sum_i \mathcal{L}_{im}(T_i, \hat{T})$ 引入轨迹多样性，但所有候选轨迹仍仅以模仿人类行为为唯一优化方向，闭环安全性指标未被纳入学习信号。第三，现有方法在推理时依赖不可微分的后处理代价函数 $T^* = \arg\min_{T_i} f(T_i, P)$ 进行轨迹选择——该函数基于不完美的感知输出 $P$ 手工设计，不仅无法端到端优化，更切断了从闭环评价指标到模型参数的反向传播路径。

**Hydra-MDP** 的提出正是为了打破上述僵局。其核心动机可归结为一个关键洞察：**利用多教师知识蒸馏，将人类驾驶的模仿知识与基于规则的闭环评价知识同时注入学生模型，以可微分的神经网络预测取代不可微的后处理代价函数**。具体而言，学生模型从传感器观测 $O$ 直接学习预测每个候选轨迹的仿真得分 $\tilde{f}(T_i, O)$，而教师模型则利用真值感知 $\hat{P}$ 计算仿真得分 $f(T_i, \hat{P})$ 作为蒸馏目标。总损失函数 $\mathcal{L} = \sum_i \mathcal{L}_{im}(T_i, \hat{T}) + \mathcal{L}_{kd}(f(T_i, \hat{P}), \tilde{f}(T_i, O))$ 统一了模仿学习与知识蒸馏，使模型在端到端框架中同时优化人类行为相似性和闭环安全性。推理时则直接通过 $T^* = \arg\min_{T_i} \tilde{f}(T_i, O)$ 选择轨迹，彻底消除了不可微后处理。

这一范式转变的直接驱动力来自 Navsim 挑战赛的实践需求——该基准要求在开环数据上训练、却在闭环度量下评价，天然暴露了模仿学习与闭环评价之间的鸿沟。Hydra-MDP 最终在该挑战赛中获得第一名，为端到端多目标规划提供了一条可行路径。

## 核心创新

Hydra‑MDP 的核心创新在于用**可微分的多教师知识蒸馏**彻底重构了端到端多模态规划的轨迹选择机制，从而在一个统一框架内同时优化模仿行为与闭环安全性。

### 1. 从不可微后处理到可微分代价预测

现有端到端多模态规划方法（如 **Vadv2**，Chen et al., arXiv 2024）在推理时依赖不可微的后处理代价函数 $f(T_i, P)$ 来筛选候选轨迹：

$$T^* = \arg\min_{T_i} f(T_i, P)$$

该过程基于不完美的感知输出 $P$，且代价函数本身不可微分，导致模型**无法在训练阶段端到端地优化闭环评价指标**。Hydra‑MDP 用一个神经网络 $\tilde{f}$ 直接预测每条候选轨迹的仿真得分，将轨迹选择变为可微操作：

$$T^* = \arg\min_{T_i} \tilde{f}(T_i, O)$$

其中 $O$ 为原始传感器观测。这一改变使得**闭环度量可以直接作为训练信号回传**，从根本上打通了从感知到规划决策的梯度通路。

### 2. 多教师 Hydra‑蒸馏：同时学习人类与规则知识

传统方法仅将人类驾驶轨迹作为单一模仿目标（单目标学习），而基于规则的闭环规划器（如 **PDM‑Closed**，Dauner et al., CoRL 2023）仅作为独立的后处理模块使用，二者在训练中互不关联。Hydra‑MDP 通过**多教师知识蒸馏**将两类知识同时注入学生模型：

- **人类教师**：通过距离基交叉熵损失 $\mathcal{L}_{im}$ 监督模仿得分 $S_i^{im}$，使学生学习类人驾驶行为。
- **规则教师**：以 PDM‑Closed 在真值感知下计算的各子度量得分（NC、DAC、TTC、C、EP）作为软标签，通过二元交叉熵损失 $\mathcal{L}_{kd}$ 蒸馏到 Hydra 预测头。

总损失函数将二者统一：

$$\mathcal{L} = \sum_i \mathcal{L}_{im}(T_i, \hat{T}) + \mathcal{L}_{kd}(f(T_i, \hat{P}), \tilde{f}(T_i, O))$$

这一范式使模型**从传感器观测端到端地学习“什么样的轨迹在闭环仿真中得分高”**，而非仅在开环下模仿轨迹形状。

### 3. 关键改变槽位总结

| 改变槽位 | 基线方法取值 | Hydra‑MDP 取值 | 证据锚点 |
|---------|------------|---------------|---------|
| **轨迹选择方式** | 不可微后处理代价函数 | 可微分神经网络预测仿真得分 | Section 2.1, Eq. (3) vs Eq. (5) |
| **学习范式** | 单目标模仿学习 | 多教师蒸馏的多目标学习 | Section 2.1, Eq. (4); Section 2.3 |
| **教师模型利用** | 仅人类驾驶员或独立规则后处理 | 人类与规则教师联合知识蒸馏 | Section 2.3, Multi‑target Hydra‑Distillation |

### 4. 消融验证的关键因果链

实验消融清晰地揭示了各创新成分的因果贡献（Table 1）：

1. **多目标蒸馏 > 单目标蒸馏**：Hydra‑MDP‑V8192（多目标）的 PDM Score 为 83.0，而仅蒸馏 PDM 总分的 Hydra‑MDP‑V8192‑PDM 仅得 80.2。这证明**将复合度量分解为子目标分别蒸馏**是必要的，直接拟合 PDM 总分因分数分布不规则而导致性能退化。

2. **置信度加权 + EP 蒸馏**：在 Hydra‑MDP‑V8192 基础上加入置信度加权和自车进度蒸馏后，Hydra‑MDP‑V8192‑W‑EP 达到 86.5，提升 3.5 分。置信度权重通过网格搜索确定，用于缓解不同教师信号拟合不完美的问题；EP 蒸馏则直接提升了对应子度量。

3. **整体增益**：相比最强端到端基线 Vadv2‑V8192（80.9），Hydra‑MDP‑V8192‑W‑EP 提升 5.6 分；相比 Transfuser 基线（78.0）提升 8.5 分，验证了范式转变的有效性。

> **需注意的局限性**：DDC 子度量因实现问题被忽略，可能影响 PDM Score 的完全可比性；置信度权重通过网格搜索确定，对新场景的泛化性需进一步验证；模型集合虽带来额外增益，但引入了更高的推理计算成本。

## 整体框架

![[assets/figures/papers/paper_list_l15_https_arxiv_org_abs_2406_06978/figures/002_Figure_2.jpg]]
*Figure 2: The Overall Architecture of Hydra-MDP*

Hydra-MDP 的整体架构包含两个核心网络：感知网络（Perception Network）与轨迹解码器（Trajectory Decoder），其核心设计目标是构建一个完全可微分的端到端多模态规划管线，从而在统一的框架中同时优化模仿学习与闭环安全度量。

**感知网络** 基于官方基线 **Transfuser**（Chitta et al., TPAMI 2022）构建，由图像骨干网络、激光雷达骨干网络以及感知头（3D 目标检测与 BEV 分割）组成。该网络接收原始传感器观测 $O$，输出环境令牌（environment tokens）$F_{env}$，为下游轨迹解码器提供紧凑的场景表征。所有端到端方法共享此感知网络，保证了感知层面的公平比较。

**轨迹解码器** 采用固定规划词汇表（planning vocabulary）$\mathcal{V}_k$ 作为候选轨迹集合。该词汇表通过以下方式构建：从原始 nuPlan 数据库中随机采样 70 万条轨迹，以 K-means 聚类中心作为 $k$ 个候选轨迹 $T_i$。解码器将词汇表嵌入与感知网络输出的环境令牌 $F_{env}$ 通过 Transformer 编解码结构进行交互，输出每个候选轨迹的模仿得分 $S_i^{im}$。模仿得分的监督信号由距离基交叉熵损失（distance-based cross-entropy loss）提供，其软标签 $y_i$ 基于 log-replay 轨迹 $\hat{T}$ 与词汇表轨迹 $T_i$ 之间的 L2 距离经 softmax 归一化得到：

$$y_i = \frac{e^{-(\hat{T} - T_i)^2}}{\sum_{j=1}^{k} e^{-(\hat{T} - T_j)^2}}$$

$$\mathcal{L}_{im} = -\sum_{i=1}^{k} y_i \log(S_i^{im})$$

**Hydra 预测头** 是 Hydra-MDP 区别于传统多模态规划的关键模块。在轨迹解码器之上，多个并行的预测头分别预测每个候选轨迹在闭环仿真中的子得分（sub-scores），包括无过失碰撞（NC）、可行驶区域合规（DAC）、碰撞时间（TTC）、舒适度（C）以及自车进度（EP）。这些预测头通过多教师知识蒸馏（Hydra-Distillation）进行训练：基于规则的教师模型 **PDM-Closed**（Dauner et al., CoRL 2023）使用感知真值（GT）在仿真器中计算每个候选轨迹的真实子得分 $\hat{S}_i^m$，学生网络则从传感器观测 $O$ 中直接预测这些得分 $S_i^m$，蒸馏损失为二元交叉熵：

$$\mathcal{L}_{kd} = -\sum_{m,i} \hat{S}_i^m \log S_i^m + (1-\hat{S}_i^m) \log(1-S_i^m)$$

总损失函数将模仿损失与所有子得分的蒸馏损失联合优化，实现多目标学习：

$$\mathcal{L} = \sum_i \mathcal{L}_{im}(T_i, \hat{T}) + \mathcal{L}_{kd}(f(T_i, \hat{P}), \tilde{f}(T_i, O))$$

**推理阶段的轨迹选择** 完全可微分，无需后处理。最终轨迹 $T^*$ 通过组合模仿得分与各子得分的置信度加权代价函数 $\tilde{f}(T_i, O)$ 选取：

$$\tilde{f}(T_i, O) = -(w_1 \log S_i^{im} + w_2 \log S_i^{NC} + w_3 \log S_i^{DAC} + w_4 \log(5 S_i^{TTC} + 2 S_i^{C} + 5 S_i^{EP}))$$

其中权重 $w_1$–$w_4$ 通过网格搜索在验证集上确定，用于缓解不同教师模型拟合不完美的问题。最终模型版本 Hydra-MDP-$\mathcal{V}_{8192}$-W-EP 还引入了 EP 蒸馏，进一步提升了相应子指标的闭环表现。

## 核心模块与公式推导

Hydra-MDP 的整体架构由两个核心网络构成：感知网络（Perception Network）和轨迹解码器（Trajectory Decoder），并在解码器之上附加 Hydra 预测头实现多教师知识蒸馏。

### 2.1 感知网络

感知网络基于官方基线 **Transfuser**（Chitta et al., TPAMI 2022）构建，包含图像骨干网络、激光雷达骨干网络以及用于 3D 目标检测和 BEV 分割的感知头。其输出为环境令牌 $F_{env}$，作为轨迹解码器的上下文输入。

### 2.2 规划词汇表构建

轨迹解码器使用固定的规划词汇表 $\mathcal{V}_k$，该词汇表通过以下步骤离线构建：

1. 从原始 nuPlan 数据库中随机采样 70 万条轨迹；
2. 对这些轨迹应用 K-means 聚类，聚类中心构成词汇表 $\mathcal{V}_k = \{T_1, T_2, \dots, T_k\}$。

词汇表大小 $k$ 是可配置的超参数（如 4096 或 8192），更大的词汇表一致带来性能增益。

### 2.3 轨迹解码器与模仿学习

轨迹解码器将词汇表嵌入与 Transformer 编解码结构结合，预测每个候选轨迹 $T_i$ 的模仿得分 $S_i^{im}$。模仿损失采用基于距离的交叉熵：

$$\mathcal{L}_{im} = -\sum_{i=1}^{k} y_i \log(S_i^{im})$$

其中软标签 $y_i$ 由 log-replay 轨迹 $\hat{T}$ 与词汇表轨迹 $T_i$ 的 L2 距离经 softmax 生成：

$$y_i = \frac{e^{-(\hat{T} - T_i)^2}}{\sum_{j=1}^{k} e^{-(\hat{T} - T_j)^2}}$$

该设计奖励与人类驾驶行为接近的候选轨迹，使模型在保持多模态能力的同时模仿专家轨迹。

### 2.4 Hydra 预测头与多目标蒸馏

Hydra 预测头是核心创新，由多个并行的预测分支组成，每个分支分别预测候选轨迹在特定闭环度量上的仿真子得分：无过失碰撞（NC）、可行驶区域合规（DAC）、碰撞时间（TTC）、舒适度（C）和自车进度（EP）。

教师信号来自基于规则的闭环规划器 **PDM-Closed**（Dauner et al., CoRL 2023），它使用感知真值（GT）计算每个候选轨迹在各子指标上的仿真得分 $\hat{S}_i^m$。学生网络仅从传感器观测 $O$ 出发，通过二元交叉熵蒸馏这些规则知识：

$$\mathcal{L}_{kd} = -\sum_{m,i} \left[ \hat{S}_i^m \log S_i^m + (1-\hat{S}_i^m) \log(1-S_i^m) \right]$$

其中 $m \in \{\text{NC, DAC, TTC, C, EP}\}$ 遍历所有子指标。总训练损失结合模仿损失与蒸馏损失：

$$\mathcal{L} = \sum_i \mathcal{L}_{im}(T_i, \hat{T}) + \mathcal{L}_{kd}\left(f(T_i, \hat{P}), \tilde{f}(T_i, O)\right)$$

### 2.5 推理阶段的代价组合

推理时，Hydra-MDP 通过置信度加权组合模仿得分和多个子得分，构建可微分的代价函数直接选择最优轨迹：

$$\tilde{f}(T_i, O) = -\left(w_1 \log S_i^{im} + w_2 \log S_i^{NC} + w_3 \log S_i^{DAC} + w_4 \log(5 S_i^{TTC} + 2 S_i^{C} + 5 S_i^{EP})\right)$$

其中权重 $w_1$–$w_4$ 为置信度参数，通过网格搜索在验证集上确定，用于缓解不同教师信号拟合不完美的问题。最终轨迹选择为：

$$T^* = \arg\min_{T_i} \tilde{f}(T_i, O)$$

这一设计将原本不可微的后处理代价函数（$T^* = \arg\min_{T_i} f(T_i, P)$）替换为神经网络预测的可微版本，使多目标优化完全融入端到端训练。

## 实验与分析

### 实验设置与评价协议

Hydra‑MDP 在 Navsim 基准的 Navtest 分片上完成端到端评测。Navsim 采用开环重放（open‑loop log‑replay）协议，但通过 **PDM Score**（Predictive Driving Metric Score）将闭环驾驶质量度量引入开环评测，从而弥合开环与闭环之间的行为偏差。PDM Score 的定义为

$$PDM_{score} = NC \times DAC \times DDC \times \frac{(5 \times TTC + 2 \times C + 5 \times EP)}{12}$$

其中各子项含义为：**NC**（无过错碰撞）、**DAC**（可行驶区域合规）、**DDC**（免碰撞帧数）、**TTC**（碰撞时间）、**C**（舒适度）以及 **EP**（自车进度）。该复合指标将安全性与行驶效率统一为单一标量，是 Navsim 挑战赛的官方排名依据。

> **公平性说明**：所有端到端方法使用相同的官方 **Transfuser** 感知网络（Chitta et al., TPAMI 2022），保证感知公平；但 **PDM‑Closed**（Dauner et al., CoRL 2023）使用感知真值（GT）作为输入，与传感器输入方法不可直接对比。此外，官方 Navsim 实现的 PDM‑Closed 因制动策略和偏移公式与 nuPlan 原版不一致，可能存在误差。DDC 指标因实现问题被忽略，可能轻微影响 PDM Score 的完全可比性。

### 主结果：Navtest 性能对比

Table 1 报告了 Navtest 分片上的核心结果。Hydra‑MDP 在所有端到端方法中取得显著领先，最终版本 **Hydra‑MDP‑V8192‑W‑EP** 达到 **86.5** PDM Score，较最强端到端基线 **Vadv2‑V8192**（Chen et al., arXiv 2024）的 80.9 提升 **+5.6** 分，较官方感知基线 **Transfuser** 的 78.0 提升 **+8.5** 分。这一差距表明，仅靠更大的规划词汇表或更强的感知骨干不足以弥合与 Hydra‑MDP 的性能鸿沟——多教师蒸馏与端到端可微轨迹选择才是关键杠杆。

![[assets/figures/papers/paper_list_l15_https_arxiv_org_abs_2406_06978/figures/004_Table_1.jpg]]
*Table 1: Performance on the Navtest Split. ⋄ The official Navsim implementation of PDM-Closed is potentially prone to errors due to inconsistent braking maneuvers and offset formulation compared with the nuPlan implementation [8]. All end-to-end methods use the official Transfuser [5] as the perception network. * Our distance-based imitation loss is adopted for training. PP: Transfuser perception is used for post-processing. PDM: The learning target is the overall PDM score. W: Weighted confidence during inference. EP: The model is trained to fit the continuous EP (Ego Progress) metric. Table 2. The Impact of Scaling Up on the Navtest Split. ⋄ The official Navsim implementation of PDM-Closed. * ViT-...*

从子指标看，Hydra‑MDP 的增益来自安全性与效率的同步改善：NC 和 DAC 维持高位，同时 EP 和 TTC 显著优于仅依赖模仿学习的基线。这验证了多目标蒸馏能够将基于规则的闭环安全知识有效迁移至端到端学生模型。

### 消融实验：蒸馏策略与推理机制

**多目标蒸馏 vs. 单目标蒸馏**。Table 1 中 **Hydra‑MDP‑V8192‑PDM**（仅蒸馏 PDM 总分）仅取得 80.2 分，而多目标版本 **Hydra‑MDP‑V8192** 达到 83.0 分（+2.8）。单目标蒸馏将 PDM Score 作为一个黑箱标量进行回归，忽略了各子指标间的非规则分布与冲突关系；多目标蒸馏则通过独立的 Hydra 预测头分别学习 NC、DAC、TTC、C、EP 的仿真得分，保留了规则教师的知识结构，从而获得更强的泛化能力。

**置信度加权与 EP 蒸馏**。在 Hydra‑MDP‑V8192 基础上引入置信度加权和 EP 蒸馏得到 **Hydra‑MDP‑V8192‑W‑EP**，PDM Score 进一步提升至 86.5（+3.5）。置信度加权通过网格搜索确定各子得分的组合系数，缓解了不同教师拟合质量不一致的问题；EP 蒸馏则直接改善了自车进度这一关键效率指标。消融表明，推理阶段的代价组合策略与训练阶段的教师选择同等重要。

**规划词汇表规模**。V4096 与 V8192 的对比在所有方法变体上一致显示增益，更大词汇表提供了更密集的轨迹覆盖，使学生模型有更高概率命中接近专家行为的候选轨迹，从而降低模仿损失的下界。

### 缩放实验：更强骨干与模型集成

Table 2 展示了视觉骨干缩放和模型集成的影响。将图像骨干从默认的 ResNet 升级为 **ViT‑L** 或 **V2‑99** 后，Hydra‑MDP‑C 的 PDM Score 达到 **91.0**，刷新了 Navtest 上的最高记录。这一结果说明，Hydra‑MDP 框架具有良好的可扩展性——更强的感知表征能够为轨迹解码器和 Hydra 预测头提供更准确的环境令牌，从而进一步提升规划质量。

最终提交版本采用了 **Sub‑score Ensembling** 策略，将三个使用不同骨干的 Hydra‑MDP 模型在子得分层面进行集成。集成带来的增益表明，不同视觉骨干对场景的理解存在互补性，通过融合多模型的闭环度量预测可以有效降低单模型的感知不确定性对轨迹选择的影响。需要指出的是，模型集成引入了更高的推理计算成本，这是性能与效率之间的经典权衡。

### 失败模式与局限性

**DDC 缺失的潜在盲区**。DDC（免碰撞帧数）因实现问题未纳入评测，这意味着当前 PDM Score 无法完全反映动态障碍物规避能力。Hydra‑MDP 在静态安全指标（NC、DAC）上的优势是否能在包含 DDC 的完整评测中保持，仍需进一步验证。

**置信度权重的泛化性**。当前权重通过验证集网格搜索确定，属于静态超参数。在新场景或分布外条件下，固定的权重组合可能导致子目标间的权衡失衡。一个开放问题是，能否通过可学习的自适应机制或在线校准来替代手工搜索。

**规划词汇表的覆盖边界**。词汇表基于 nuPlan 数据库中的 70 万条轨迹经 K‑means 聚类构建，对 nuPlan 分布内的场景覆盖充分，但对极端天气、施工区等长尾场景的覆盖度未知。在这些场景下，词汇表中的候选轨迹可能全部偏离安全区域，导致 Hydra 预测头输出的子得分无法有效区分轨迹质量。

**跨基准验证缺失**。当前实验仅限 Navsim 基准，Hydra‑MDP 在其他自动驾驶评测平台（如 CARLA 闭环基准、Waymo Open Motion Dataset）上的表现尚未报告。特别是 Navsim 的开环重放协议与真实闭环驾驶之间存在固有差异，Hydra‑Distillation 在真正闭环条件下的鲁棒性仍是一个开放问题。

### 补充图表

![[assets/figures/papers/paper_list_l15_https_arxiv_org_abs_2406_06978/figures/003_Table.jpg]]

## 方法谱系与知识库定位

### 端到端自动驾驶的范式演进

端到端自动驾驶的核心瓶颈在于如何将感知、预测和规划统一在一个可优化的框架中，同时满足安全、效率、舒适和规则遵从等多重目标。Hydra-MDP 的提出建立在对三种规划范式的递进式改进之上（Figure 1）：

1. **单模态规划 + 单目标学习**：以 **Transfuser** (Chitta et al., TPAMI 2022) 为代表，感知网络直接回归一条专家轨迹，通过 L2 损失 $\mathcal{L} = \mathcal{L}_{im}(T^*, \hat{T})$ 进行监督。该范式的局限在于无法建模驾驶行为的多模态性，且仅模仿人类驾驶员，忽视了闭环安全指标。

2. **多模态规划 + 单目标学习**：以 **Vadv2** (Chen et al., arXiv 2024) 为代表，预测多条候选轨迹，但训练时仍仅用模仿损失 $\mathcal{L} = \sum_i \mathcal{L}_{im}(T_i, \hat{T})$ 监督所有轨迹，轨迹选择依赖不可微分的后处理代价函数 $T^* = \arg\min_{T_i} f(T_i, P)$。这种"先预测后筛选"的范式存在根本性缺陷：后处理模块与感知网络无法联合优化，导致开环训练与闭环评估之间存在隐式偏差。

3. **多模态规划 + 多目标学习（Hydra-MDP 范式）**：Hydra-MDP 的核心突破在于将不可微分的后处理代价函数替换为可微分的神经网络预测器 $\tilde{f}(T_i, O)$，使得轨迹选择过程能够端到端地接收梯度信号。训练时，学生模型不仅学习模仿人类驾驶行为，还通过知识蒸馏从基于规则的教师模型（**PDM-Closed**, Dauner et al., CoRL 2023）中学习闭环度量知识，总损失函数为 $\mathcal{L} = \sum_i \mathcal{L}_{im}(T_i, \hat{T}) + \mathcal{L}_{kd}(f(T_i, \hat{P}), \tilde{f}(T_i, O))$，推理时直接通过预测代价选择轨迹 $T^* = \arg\min_{T_i} \tilde{f}(T_i, O)$。

### 与基线方法的关键差异

Hydra-MDP 在三个关键维度上区别于现有方法：

| 维度 | 基线方法 | Hydra-MDP |
|------|---------|-----------|
| **轨迹选择方式** | 不可微后处理代价函数（仅测试时根据感知结果选择） | 可微神经网络预测仿真得分，端到端选择 |
| **学习范式** | 单目标模仿学习（仅模仿人类轨迹） | 多教师蒸馏的多目标学习（模仿损失 + 各闭环度量的蒸馏损失） |
| **教师模型利用** | 仅用人类驾驶员作为教师，或规则模型作为独立后处理 | 同时利用人类教师和规则教师（PDM-Closed 仿真得分）进行知识蒸馏 |

具体而言，Transfuser 直接回归轨迹，缺乏多模态建模能力；Vadv2 虽引入多模态，但其后处理代价函数 $f(T_i, P)$ 不可微分，无法将闭环性能信号反向传播至感知网络。PDM-Closed 虽然通过规则化的代价函数实现了优异的闭环性能，但依赖感知真值（GT），无法直接从传感器输入进行端到端学习。Hydra-MDP 通过 Hydra-Distillation 机制，将 PDM-Closed 的规则知识蒸馏到学生网络的 Hydra Prediction Heads 中，使模型能够从原始传感器观测中预测各闭环子指标（NC、DAC、TTC、C、EP），从而在统一框架中兼顾模仿学习的类人性和规则模型的安全性。

### 适用边界与局限

**适用边界**：
- 该方法适用于具有明确闭环评价指标的场景，尤其是 Navsim 这类提供标准化 PDM Score 的基准。
- 规划词汇表 $\mathcal{V}_k$ 基于 nuPlan 数据库的 70 万条轨迹通过 K-means 聚类构建，其覆盖能力受限于原始数据的分布范围。
- 置信度权重 $w_1, w_2, w_3, w_4$ 通过网格搜索在验证集上确定，对新场景或不同评价体系可能需要重新校准。

**已知局限**：
1. **DDC 指标缺失**：由于实现问题，PDM Score 中的 DDC（Drivable Area Compliance 的免碰撞帧数维度）被忽略，这可能影响对动态避碰能力的完整评估，进而削弱 PDM 分数的完全可比性（Section 3.1 脚注）。
2. **权重非自适应**：推理组合代价函数 $\tilde{f}(T_i, O) = -(w_1 \log S_i^{im} + w_2 \log S_i^{NC} + w_3 \log S_i^{DAC} + w_4 \log(5 S_i^{TTC} + 2 S_i^{C} + 5 S_i^{EP}))$ 中的权重是静态的，无法根据驾驶场景动态调整各目标的优先级。
3. **模型集合的计算成本**：最佳性能依赖多模型集合（Mixture of Encoders 和 Sub-score Ensembling），引入额外的推理计算开销。
4. **评估范围有限**：仅在 Navsim 数据集上验证，缺少在 nuPlan 原生闭环评估或其他自动驾驶基准上的验证。

### 开放问题

1. **DDC 的缺失影响**：忽略 DDC 对 PDM 分数的完整性和实际安全性评估的偏差有多大？在补全 DDC 后，Hydra-MDP 的多目标蒸馏框架是否仍能保持优势？
2. **多教师扩展性**：Hydra-Distillation 能否扩展到更多教师模型（如独立的舒适度模型、激进/保守驾驶风格模型）而不会产生教师间的目标冲突？这涉及多目标蒸馏中的梯度协调问题。
3. **权重自适应机制**：当前网格搜索得到的置信度权重是否可以通过元学习或在线自适应机制动态调整，使模型能够根据场景风险级别自动平衡安全性与效率？
4. **真实闭环验证**：该框架在真正的闭环评估环境（如 CARLA 或真实道路测试）中的表现如何？Navsim 的开环日志重放评估与真实闭环之间存在已知的分布偏移。
5. **分布外泛化**：规划词汇表基于 nuPlan 构建，对极端场景或分布外场景的覆盖度未知，模型在这些场景下的退化行为值得进一步研究。

## 原文 PDF

![[paperPDFs/CVPR_2024/Hydra_MDP_End_to_end_Multimodal_Planning_with_Multi_target_Hydra_Distillation.pdf]]
