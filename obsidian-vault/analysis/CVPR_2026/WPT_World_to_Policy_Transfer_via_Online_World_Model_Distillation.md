---
title: "WPT: World-to-Policy Transfer via Online World Model Distillation"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/WPT_World_to_Policy_Transfer_via_Online_World_Model_Distillation.pdf
project_link: null
code_link: null
aliases:
- WPT
tags:
- CVPR_2026
- topic/representation_self_supervised_transfer
- topic/representation_self_supervised_transfer/representation_learning
core_operator: 以可训练的世界奖励模型为核心因果调节器：通过模仿奖励（对齐人类偏好）和仿真奖励（NC、DAC、TTC、EP、Comf）在预测的未来世界状态下评价候选轨迹，将世界模型的预测能力注入教师策略；再通过策略蒸馏和世界奖励蒸馏传递至学生。
primary_logic: 世界模型仅需在训练阶段通过奖励信号指导多模态教师策略，无需参与推理；通过知识蒸馏，将未来感知、安全评估等世界知识高效迁移至轻量单模态学生策略，实现安全、准确的实时规划。
claims:
- WPT-Student retains most gains of the teacher without test-time world-model overhead, achieving 4.9× faster inference.
- WPT-Teacher achieves 0.61m Avg. L2 and 0.11% Avg. collision on nuScenes, surpassing all previous world-model and imitation-learning methods.
- WPT-Teacher boosts Driving Score by +14.00 and Success Rate by +20.44 over the baseline on Bench2Drive.
- 交互式奖励是安全增益的主要驱动力，世界感知蒸馏有效地将这些增益整合到学生模型中。
---

# WPT: World-to-Policy Transfer via Online World Model Distillation

> [!tip] 核心洞察
> 世界模型仅需在训练阶段通过奖励信号指导多模态教师策略，无需参与推理；通过知识蒸馏，将未来感知、安全评估等世界知识高效迁移至轻量单模态学生策略，实现安全、准确的实时规划。

| 字段 | 内容 |
|------|------|
| 中文题名 | WPT：通过在线世界模型蒸馏实现世界到策略迁移 |
| 英文题名 | WPT: World-to-Policy Transfer via Online World Model Distillation |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2511.20095) |
| Topic | #topic/representation_self_supervised_transfer #topic/representation_self_supervised_transfer/representation_learning |
| Method | WPT |
| Dataset | nuScenes validation set, Bench2Drive |

> [!tip] 效果简介
> - nuScenes validation set 上，Avg. L2 (m) ↓ 0.61 (WPT-Teacher) vs 0.88 (Baseline) (-0.27)；Avg. Collision (%) ↓ 0.11 (WPT-Teacher) vs 1.06 (Baseline) (-0.95)；Avg. L2 (m) ↓ 0.66 (WPT-Student) vs 0.88 (Baseline) (-0.22)。
> - Bench2Drive 上，Driving Score ↑ 79.23 (WPT-Teacher) vs 65.23 (Baseline) (+14.00)；Success Rate (%) ↑ 54.54 (WPT-Teacher) vs 34.10 (Baseline) (+20.44)；Driving Score ↑ 72.61 (WPT-Student) vs 65.23 (Baseline) (+7.38)。

## 概要

### 问题背景

自动驾驶规划面临的核心矛盾在于：世界模型能够提供丰富的未来动态预测与安全评估能力，但现有方法要么将世界模型直接集成到推理管线中（如 **UniAD** (Hu et al., CVPR 2023)、**Drive-OccWorld**、**WoTE** 等），导致实时性严重受损；要么依赖模拟器进行强化学习训练，受限于生成数据的保真度，难以兼顾安全与效率。根本瓶颈在于**世界模型的丰富未来知识与实时轻量部署之间的冲突**——推理时自回归的未来预测或在线轨迹评估带来了不可忽视的计算开销。

### 核心思路

WPT（World-to-Policy Transfer）提出了一种**训练时交互、推理时丢弃**的新范式。其关键因果调节器是一个可训练的世界奖励模型：在训练阶段，该模型结合世界模型预测的未来世界状态，对教师策略生成的多模态候选轨迹进行评价——同时考虑模仿奖励（对齐人类驾驶偏好）和仿真奖励（无碰撞 NC、可行驶区域合规 DAC、碰撞时间 TTC、自车进度 EP、舒适性 Comf）。通过这一机制，世界模型的预测能力被注入教师策略，再经由策略蒸馏和世界奖励蒸馏，高效迁移至轻量单模态学生策略。推理时，世界模型和奖励模型完全移除，学生策略独立完成实时规划。

### 主要结果

在 nuScenes 开环评测中，WPT-Teacher 取得 **0.61m 平均 L2 误差**和 **0.11% 平均碰撞率**，超越所有对比的世界模型方法和模仿学习方法；WPT-Student 在保持 **4.9 倍推理加速**的同时，仍达到 0.66m L2 和 0.24% 碰撞率。在 Bench2Drive 闭环评测中，WPT-Teacher 相较基线 Driving Score 提升 **+14.00**（79.23 vs. 65.23），Success Rate 提升 **+20.44%**（54.54% vs. 34.10%）。消融实验进一步证实：交互式仿真奖励是安全增益的主要驱动力，世界感知蒸馏则将这些增益有效整合至可部署的学生模型中，同时将训练成本降低 **65.6%**（从 488 GPU 小时降至 168 GPU 小时）。

### 方法谱系与知识库定位

WPT 处于**世界模型辅助规划**与**知识蒸馏**的交叉点。不同于将世界模型作为推理组件的方法（如 DriveTransformer 的时序建模、WoTE 的 BEV 轨迹评估），WPT 将世界模型限定为训练阶段的“教师”信号源。相较于 DriveDPO 等偏好对齐方法仅优化模仿目标，WPT 的奖励模型融合了显式的安全与效率仿真信号，提供了更丰富的监督维度。在蒸馏策略上，WPT 同时对齐规划表示（查询级 L2 蒸馏）和奖励分布（世界奖励蒸馏），区别于仅使用特征蒸馏或伪标签的常见做法。该范式为“世界知识注入-轻量策略部署”提供了一条可复用的技术路径，其核心思想——训练时利用重型模型提供结构化奖励，推理时仅保留轻量学生——具备向其他具身智能任务迁移的潜力。



### 端到端自动驾驶的规划瓶颈

自动驾驶规划的核心挑战在于：车辆必须在部分可观测、动态交互的环境中做出安全且实时的决策。近年来，端到端（E2E）规划器直接从传感器输入映射到轨迹输出，展现出超越传统模块化流水线的潜力。然而，E2E方法在**未来感知**与**安全评估**两个维度上仍存在根本性短板——它们缺乏对“当前决策将导致何种未来状态”的显式建模能力，因而难以在复杂交互场景中做出前瞻性判断。

### 现有世界模型方法的困境

世界模型（World Model）被视为弥补上述短板的关键技术。它通过预测未来环境状态，为规划器提供丰富的动态先验。但现有世界模型在自动驾驶中的集成方式存在两难困境：

- **推理时集成范式**（Figure 1b）：将世界模型直接嵌入策略网络，在推理时进行自回归未来预测或在线轨迹评估。代表性工作如 **UniAD**（Hu et al., CVPR 2023）和 **VAD** 采用多任务模块联合推理，**Drive-OccWorld** 和 **WoTE** 则通过占用预测评估候选轨迹。这类方法虽然提升了规划质量，但自回归预测和在线评估引入显著推理延迟，严重制约实时部署。
- **模拟器训练范式**（Figure 1c）：将世界模型作为训练环境，通过强化学习优化策略。此类方法受益于丰富的交互反馈，但生成数据的保真度受限于世界模型质量，难以保证在真实场景中的安全性。

**根本瓶颈**在于：世界模型的丰富未来知识与轻量实时部署之间存在不可调和的冲突。推理时使用世界模型带来计算开销，而完全放弃世界模型则丧失未来感知能力。

### 从“世界参与推理”到“世界参与训练”

WPT的核心动机是打破上述困境。其关键洞察是：**世界模型仅需在训练阶段通过奖励信号指导策略学习，无需参与推理**。通过将世界模型的预测能力转化为可训练奖励函数，WPT在训练时让策略与世界模型充分交互，获取未来感知和安全评估能力；推理时则完全移除世界模型，实现轻量部署。

这一范式转换（Figure 1d）将世界模型从“推理负担”重新定位为“训练教师”，为端到端自动驾驶的实时规划开辟了新路径。



## 核心方法与创新机理

WPT 的根本创新在于**将世界模型从推理时依赖转变为纯训练时知识注入器**，通过“教师-奖励-蒸馏”三阶段机制，在不增加部署开销的前提下将未来世界感知能力迁移至轻量策略。其核心突破可归纳为三个维度的 **changed slots**：

### 1. 世界模型使用阶段：从推理时耦合到训练时注入

现有自动驾驶世界模型方法在推理时直接集成到策略中（如 **UniAD** (Hu et al., CVPR 2023) 的多任务模块串联）或作为在线模拟器进行轨迹搜索，导致实时性差且限制端到端优化。WPT 将世界模型的使用严格限定在训练阶段：世界模型仅用于预测未来世界状态以生成奖励信号，推理时完全移除，学生策略无需任何世界模型组件即可独立运行。**这一范式转换是 WPT 所有后续创新的基础**——它从根本上解决了“世界模型的丰富未来知识”与“实时轻量部署”之间的冲突。

### 2. 轨迹评估机制：从模仿损失到可训练交互式奖励模型

传统方法依赖模仿损失（如 L2 距离）或自回归搜索来选择最优轨迹，缺乏对安全性和动态交互的显式建模。WPT 设计了**可训练的交互式奖励模型**，在预测的未来世界状态下对每条候选轨迹进行多维度评估：

- **模仿奖励**（Imitation Reward）：通过 softmax 归一化的负 L2 距离对齐人类驾驶偏好，目标奖励定义为 $r_{\mathrm{im}, i}^{*} = \mathrm{softmax}\left(\frac{-d_i}{\sum_{j=1}^{N} -d_j}\right)$；
- **仿真奖励**（Simulation Reward）：包含五个安全与效率信号——无碰撞（NC）、可行驶区域合规（DAC）、碰撞时间（TTC）、自车进度（EP）和舒适性（Comf），最终融合为 $r_{\mathrm{final}} = \alpha_1 \log r_{\mathrm{im}} + \alpha_2 \log r_{\mathrm{NC}} + \alpha_3 \log r_{\mathrm{DAC}} + \alpha_4 \log(5 r_{\mathrm{TTC}} + 5 r_{\mathrm{EP}} + 2 r_{\mathrm{Comf}})$。

最优轨迹通过最大化加权奖励和选出：$\boldsymbol{\tau}^{*} = \arg\max_i (w_1 r_{\mathrm{im}, i} + w_2 r_{\mathrm{sim}, i})$。消融实验（Table 4）表明，移除 TTC 奖励会导致碰撞率从 0.11% 增至 0.25%，证实交互式仿真奖励是安全增益的主要驱动力。

### 3. 策略部署形式：从多模态在线评估到单模态知识蒸馏

教师策略虽能生成多模态轨迹并通过世界模型交互选择最优解，但推理时若保留奖励模型会引入约 26ms 额外延迟（286→312ms）。WPT 通过**双路径知识蒸馏**将教师的世界感知能力迁移至轻量单模态学生：

- **策略蒸馏**：最小化学生与教师规划查询的 L2 距离 $\mathcal{L}_{\mathrm{policy}} = \| Q^S - Q^T \|_2$，对齐规划意图；
- **世界奖励蒸馏**：让学生轨迹的奖励分数逼近教师最优轨迹 $\mathcal{L}_{\mathrm{reward}} = \| r_{\mathrm{final}}(\tau_S) - r_{\mathrm{final}}(\tau_T^{*}) \|_2$，传递安全评估知识。

消融实验（Table 6）证实，查询级蒸馏、模仿奖励蒸馏和仿真奖励蒸馏三者缺一不可——仅当三者结合时学生才能达到 0.66m L2 误差和 0.24% 碰撞率的最优性能。更重要的是，这一蒸馏机制不仅保留了教师的大部分性能增益，还实现了高达 **4.9 倍推理加速**，同时将学生训练成本从 488 GPU 小时降至 168 小时（-65.6%）。



WPT 提出了一种**训练时世界知识注入、推理时世界模型剥离**的端到端自动驾驶规划范式。其核心 pipeline 由四个紧密协作的模块构成：**AD 策略（教师/学生）**、**世界模型**、**奖励模型** 和 **世界知识蒸馏**。整体架构如 Figure 2 所示，分为上方的训练阶段和下方的蒸馏阶段。

![[assets/figures/papers/paper_list_l2276_https_arxiv_org_abs_2511_20095/figures/002_Figure_2.jpg]]
*Figure 2: Overview of WPT framework. During training (top), the pretrained world model predicts future world under given action conditions, and the teacher AD policy (T) generates multi-modal trajectories. The reward model evaluates these trajectories to produce world reward. During distillation (bottom), the student AD policy (S) learns from the teacher through two mechanisms: (1) policy distillation, which aligns the planning representations between teacher and student; and (2) world reward distillation, which encourages the student to match the teacher’s optimal reward trajectory in the predicted future world*

**训练阶段（上方流程）**：预训练并冻结的世界模型首先基于历史观测和动作条件自回归地预测未来世界嵌入 $\boldsymbol{F}_{t+1}^{\mathrm{w}}$。教师 AD 策略以多视图图像为输入，通过 BEV 编码器和规划查询生成多模态候选轨迹 $\{\tau_i\}_{i=1}^N$。这些轨迹与预测的未来世界状态一同送入可训练的奖励模型，由奖励模型输出每条轨迹的**模仿奖励**（对齐人类驾驶偏好）和**仿真奖励**（包含无碰撞 NC、可行驶区域合规 DAC、碰撞时间 TTC、自车进度 EP 和舒适性 Comf 五项安全与效率指标）。最终通过加权融合选择综合奖励最高的轨迹作为最优轨迹 $\tau^*$：

$$\tau^* = \arg\max_i \left( w_1 r_{\mathrm{im},i} + w_2 r_{\mathrm{sim},i} \right)$$

奖励模型的详细结构如 Figure 3 所示：世界编码器处理潜在世界表征，规划查询经规划解码器和规划头生成多模态轨迹后，由轨迹编码器编码，再分别通过仿真奖励头和模仿奖励头进行评估，最终融合为综合奖励。

**蒸馏阶段（下方流程）**：学生 AD 策略采用与教师相同的单模态架构，但**不接入世界模型**。通过两条蒸馏路径将教师的世界感知能力迁移至学生：

1. **策略蒸馏**：最小化学生与教师规划查询之间的 L2 距离，对齐规划意图：
   $$\mathcal{L}_{\mathrm{policy}} = \| Q^S - Q^T \|_2$$

2. **世界奖励蒸馏**：让学生输出轨迹的奖励分数逼近教师最优轨迹的奖励分数，隐式传递世界模型对安全与效率的评估知识：
   $$\mathcal{L}_{\mathrm{reward}} = \| r_{\mathrm{final}}(\tau_S) - r_{\mathrm{final}}(\tau_T^*) \|_2$$

这一设计的核心洞察在于：世界模型仅需在训练阶段通过奖励信号指导多模态教师策略，无需参与推理；通过知识蒸馏，将未来感知、安全评估等世界知识高效迁移至轻量单模态学生策略，实现安全、准确的实时规划。推理时世界模型被完全移除，学生策略以显著更低的延迟独立完成规划。

### 补充图表

![[assets/figures/papers/paper_list_l2276_https_arxiv_org_abs_2511_20095/figures/001_Figure_1.jpg]]
*Figure 1: Different training paradigms of AD policy with world model. (a) Imitation learning where the policy is trained using expert supervision. (b) World model (WM) directly integrated into the AD policy for enhanced feature evolution and trajectory reasoning. (c) Simulator-based reinforcement learning for AD policy training using a simulated world. (d) Our WPT, where the policy interacts with the WM during training, with both the teacher policy (T) and the student policy (S) leveraging the WM for knowledge transfer. After training, the WM will be discarded*

![[assets/figures/papers/paper_list_l2276_https_arxiv_org_abs_2511_20095/figures/012_Figure_6.jpg]]
*Figure 6: Illustration of our Occ-based and instance-based baseline models. The top part shows the occupancy-based baseline model, while the bottom part illustrates the instance-based baseline model. Both approaches utilize a BEV decoder, but differ in how planning queries interact with features*



WPT 框架由四个核心模块构成：AD 策略（教师/学生）、世界模型、奖励模型与世界知识蒸馏。各模块协同完成“训练时注入世界知识，推理时轻量部署”的目标。

### 3.1 AD 策略（教师/学生）

AD 策略负责从多视图图像生成未来轨迹。教师与学生共享相同的 BEV 编码架构，但教师采用多模态轨迹生成，学生为单模态且无需世界模型参与推理。

规划查询（plan queries）通过交叉注意力与世界表征交互，得到精炼查询：

$$\tilde{\boldsymbol{Q}} = \mathcal{P}_D(\boldsymbol{Q}, \boldsymbol{F}^{\mathrm{w}})$$

其中 $\boldsymbol{Q}$ 为规划查询，$\boldsymbol{F}^{\mathrm{w}}$ 为世界表征。随后通过 MLP 规划头解码出预测轨迹：

$$\hat{\mathcal{T}} = \mathcal{P}_h(\tilde{\boldsymbol{Q}})$$

教师策略进一步利用世界模型预测的未来世界嵌入进行轨迹规划（见 Eq. (8)）：

$$\mathcal{T}_{t+1} = \mathcal{P}_h\left(\mathcal{P}_D\left(\boldsymbol{Q}^T, \boldsymbol{F}_{t+1}^{\mathrm{w}}\right)\right)$$

学生策略则不访问 $\boldsymbol{F}_{t+1}^{\mathrm{w}}$，仅通过蒸馏间接获取世界感知能力。

### 3.2 世界模型

世界模型基于历史观测和自回归预测未来世界嵌入 $\boldsymbol{F}_{t+1}^{\mathrm{w}}$，为教师策略提供未来动态信息。WPT 采用预训练并冻结权重的世界模型（如 Drive-OccWorld），仅训练阶段使用，推理时完全移除。

### 3.3 奖励模型

奖励模型是可训练的核心因果调节器，在预测的未来世界状态下评价候选轨迹。其架构如 Figure 3 所示：世界编码器处理潜在世界表征，轨迹编码器编码候选轨迹，两者融合后由两个奖励头分别输出模仿奖励和仿真奖励。

![[assets/figures/papers/paper_list_l2276_https_arxiv_org_abs_2511_20095/figures/003_Figure_3.jpg]]
*Figure 3: Overview of reward model. The reward model consists of multiple components: the world encoder processes the latent world representation, while the plan queries are refined through the plan decoder and plan head to generate multi-modal candidate trajectories. These trajectories are then passed to the trajectory encoder, which encodes them for evaluation by two distinct reward heads: the simulation reward head and the imitation reward head. The final reward is computed by combining these reward values, with the best trajectory selected via the argmax operation. The supervisory signals of the reward model come from simulation and imitation. For the detailed process, please refer to Sec. 3.3*

**模仿奖励** 衡量候选轨迹与人类专家偏好的对齐程度，通过 softmax 归一化的负 L2 距离计算目标值：

$$r_{\mathrm{im},i}^* = \mathrm{softmax}\left(\frac{-d_i}{\sum_{j=1}^N -d_j}\right)$$

**仿真奖励** 包含五个安全与效率信号：NC（无碰撞）、DAC（可行驶区域合规）、TTC（碰撞时间）、EP（自车进度）、Comf（舒适性）。

**最终奖励融合** 将两类奖励对数加权组合：

$$r_{\mathrm{final}} = \alpha_1 \log r_{\mathrm{im}} + \alpha_2 \log r_{\mathrm{NC}} + \alpha_3 \log r_{\mathrm{DAC}} + \alpha_4 \log(5 r_{\mathrm{TTC}} + 5 r_{\mathrm{EP}} + 2 r_{\mathrm{Comf}})$$

**最优轨迹选择** 通过 argmax 从 $N$ 条候选轨迹中选取综合奖励最高者：

$$\boldsymbol{\tau}^* = \arg\max_i (w_1 r_{\mathrm{im},i} + w_2 r_{\mathrm{sim},i})$$

### 3.4 世界知识蒸馏

蒸馏阶段将教师的多模态世界感知能力迁移至轻量学生，包含两种机制。

**策略蒸馏** 对齐教师与学生的规划查询，最小化 L2 距离：

$$\mathcal{L}_{\mathrm{policy}} = \| Q^S - Q^T \|_2$$

**世界奖励蒸馏** 让学生轨迹的奖励分数逼近教师最优轨迹：

$$\mathcal{L}_{\mathrm{reward}} = \| r_{\mathrm{final}}(\tau_S) - r_{\mathrm{final}}(\tau_T^*) \|_2$$

消融实验（Table 6）表明，查询蒸馏、模仿奖励蒸馏与仿真奖励蒸馏三者结合才能达到最佳学生性能（0.66m / 0.24% 碰撞率）。同时，世界感知蒸馏大幅降低训练成本——学生训练从 488h 降至 168h（-65.6%），且规划质量同步提升（Table 8）。



## 实验与关键发现

### 一、主实验结果

WPT 在两个主流自动驾驶规划基准上进行了端到端评估：nuScenes 验证集（开环）和 Bench2Drive（开环+闭环）。实验设置中，Baseline 采用与 WPT-Student 完全相同的单模态架构，但不包含奖励模型与蒸馏机制，确保增益归因可控。世界模型采用预训练 Drive-OccWorld 并冻结权重，避免联合训练引入额外容量优势。WPT 不使用任何专家特征蒸馏（表 2 中带 `*` 的方法依赖此类先验），凸显对比的公平性。

**nuScenes 开环规划**（表 1）：WPT-Teacher 取得 Avg. L2 0.61 m、Avg. Collision 0.11%，全面超越此前所有世界模型方法与模仿学习方法。WPT-Student 在移除世界模型后仍保持 Avg. L2 0.66 m、Avg. Collision 0.24%，相比 Baseline（0.88 m / 1.06%）分别降低 0.22 m 和 0.82 个百分点，验证了世界知识蒸馏的有效性。

**Bench2Drive 闭环规划**（表 2）：WPT-Teacher 将 Driving Score 从 Baseline 的 65.23 提升至 79.23（+14.00），Success Rate 从 34.10% 提升至 54.54%（+20.44 个百分点）。WPT-Student 在无世界模型部署条件下仍达到 DS 72.61、SR 44.97%，显著优于 Baseline 且接近教师水平。值得注意的是，WPT 在多项驾驶子能力上表现均衡（表 7），尤其在需要未来感知的交互场景中优势明显。

**推理效率**（表 9）：WPT-Student 推理延迟约 58 ms，相比 Baseline（286 ms）实现 **4.9× 加速**，且规划质量更高。若教师在推理时开启奖励模型会引入约 26 ms 额外开销（286→312 ms），但通过蒸馏完全消除该代价。

### 二、消融实验

消融实验系统验证了 WPT 各组件的因果贡献。

**奖励模型使用阶段**（表 3）：仅使用模仿奖励（Im. Rwd.）即可提升性能，但加入仿真奖励（Sim. Rwd.）后安全指标跃升——碰撞率从 0.29% 降至 0.11%。关键发现是，仿真奖励仅在训练时使用即可达到最优效果（0.61 m / 0.11%），推理时额外使用反而无增益，证实 WPT 的“训练时交互”范式是充分且高效的。

**仿真奖励各信号贡献**（表 4）：移除 TTC（Time-to-Collision）奖励导致碰撞率从 0.11% 飙升至 0.25%，表明 TTC 是安全增益的核心驱动力。NC（No Collision）、DAC（Drivable Area Compliance）、EP（Ego Progress）各自移除均造成不同程度的性能退化，验证了多信号融合的必要性。

**交互占用来源**（表 5）：世界模型生成的占用（WM-Occ）优于真实占用（GT-Occ），WM-Occ 取得 0.61 m / 0.11%，而 GT-Occ 为 0.65 m / 0.15%。这一反直觉结果表明，世界模型提供的**预测性未来动态信息**比静态真实占用更有价值，因为它使奖励模型能够在“即将发生”的未来状态下评估轨迹安全性。

**蒸馏策略组合**（表 6）：查询级蒸馏（Query）、模仿奖励蒸馏和仿真奖励蒸馏三者缺一不可。仅查询蒸馏时学生性能为 0.72 m / 0.38%，逐步加入两类奖励蒸馏后最终达到 0.66 m / 0.24%，证明世界感知蒸馏需要同时对齐规划表示和奖励信号才能充分传递教师的世界知识。

**训练效率**（表 8）：WPT-Student 训练仅需 168 GPU 小时，相比 Baseline 的 488 小时**降低 65.6%**，同时规划指标全面提升。这说明世界知识蒸馏不仅提升性能，还大幅降低了从头训练高质量策略的成本。

### 三、失败模式与局限

尽管 WPT 在安全性和效率上表现优异，但仍存在以下局限：

1. **舒适性权衡**：在 Bench2Drive 闭环评估中，WPT 的 Comfort 指标相对较低（表 2 中 17.80/16.39），效率与舒适性之间存在明显权衡。这源于当前奖励塑形中安全项权重较高，未来需设计更精细的奖励函数以在不牺牲安全的前提下提升平顺性。

2. **世界模型质量依赖**：WPT 的奖励信号质量直接取决于预训练世界模型的预测精度。文中使用冻结权重的 Drive-OccWorld，若世界模型在长时域预测或复杂交互场景中出现退化，奖励评估的可靠性将受影响，进而限制教师策略的性能上限。

3. **教师推理开销**：若教师在推理时开启奖励模型（用于在线轨迹选择），会引入约 26 ms 额外延迟。虽然通过蒸馏可完全消除此开销，但在需要教师在线微调或自适应更新的场景下，该代价仍是一个工程权衡点。

### 四、关键图表结论

- **表 1**：WPT-Teacher 在 nuScenes 上取得 SOTA 开环性能，WPT-Student 在 4.9× 加速下仍大幅优于 Baseline。
- **表 2**：WPT 在 Bench2Drive 闭环中将 Driving Score 提升 14 分、Success Rate 提升 20 个百分点，且不依赖专家特征蒸馏。
- **表 3**：仿真奖励仅在训练时使用即达最优，推理时额外使用无增益——这是 WPT 范式有效性的核心证据。
- **表 4**：TTC 奖励是安全增益的主要驱动力，移除后碰撞率翻倍。
- **表 5**：世界模型预测的未来占用比真实占用更有价值，验证了“预测性交互”的因果作用。
- **表 6**：查询蒸馏、模仿奖励蒸馏、仿真奖励蒸馏三者协同才能实现最优知识迁移。
- **表 8**：世界感知蒸馏使训练成本降低 65.6%，同时提升规划质量。
- **表 9**：WPT-Student 实现 4.9× 推理加速，且规划性能优于更重的 Baseline。

### 补充图表

![[assets/figures/papers/paper_list_l2276_https_arxiv_org_abs_2511_20095/figures/004_Table_1.jpg]]
*Table 1: End-to-end planning performance on nuScenes validation set*

![[assets/figures/papers/paper_list_l2276_https_arxiv_org_abs_2511_20095/figures/005_Table_2.jpg]]
*Table 2: Open-loop and closed-loop planning performance on Bench2Drive. Avg. L2 is averaged over the predictions in 2 seconds under 2Hz. * denotes expert feature distillation*

![[assets/figures/papers/paper_list_l2276_https_arxiv_org_abs_2511_20095/figures/007_Table_3.jpg]]
*Table 3: Ablation study of reward model. We compare different reward equipment at different usage stages (training stage or also at inference). “Im. Rwd.” is an imitation reward, while “Sim.Rwd.” means simulation reward*

![[assets/figures/papers/paper_list_l2276_https_arxiv_org_abs_2511_20095/figures/009_Table_4.jpg]]
*Table 4: Ablation study of different rewards. Simulation reward consists of five signals: NC (No Collision), EP (Ego Progress), DAC (Drivable Area Compliance), TTC (Time-to-Collision), and Comf. (Comfort)*

![[assets/figures/papers/paper_list_l2276_https_arxiv_org_abs_2511_20095/figures/006_Table_5.jpg]]
*Table 5: Interaction occupancy source ablation. GT-Occ denotes using ground truth occupancy for interaction, while WM-Occ denotes using the occupancy generated by WM*

![[assets/figures/papers/paper_list_l2276_https_arxiv_org_abs_2511_20095/figures/008_Table_6.jpg]]
*Table 6: Ablation study of distillation. “Query” denotes the distillation of the plan query*

![[assets/figures/papers/paper_list_l2276_https_arxiv_org_abs_2511_20095/figures/014_Table_8.jpg]]
*Table 8: Comparison of training process*

![[assets/figures/papers/paper_list_l2276_https_arxiv_org_abs_2511_20095/figures/015_Table_9.jpg]]
*Table 9: Comparison of planning inference time*



## 定位与知识库关联

### 1. 与现有世界模型范式的根本差异

WPT 的核心定位在于**训练时交互、推理时丢弃**的世界模型使用范式，这与现有主流方法形成鲜明对比。Figure 1 将 WPT 置于四种训练范式的谱系中，清晰揭示了其独特性：

- **模仿学习范式**（Figure 1a）：策略仅通过专家监督训练，不利用世界模型。典型代表如 **UniAD**（Hu et al., CVPR 2023）和 **VAD**，它们在推理时直接输出轨迹，但缺乏对未来动态的显式建模。
- **世界模型集成范式**（Figure 1b）：世界模型直接嵌入策略推理管线，通过自回归预测未来状态增强特征演化和轨迹推理。**Drive-OccWorld**、**DriveTransformer**、**WoTE** 等方法属于此类，它们的根本瓶颈在于**推理时依赖世界模型的自回归预测，导致实时性差**。
- **基于模拟器的强化学习范式**（Figure 1c）：通过模拟世界进行策略训练，但模拟器生成数据的保真度受限，难以兼顾安全与效率。
- **WPT 范式**（Figure 1d）：世界模型仅在训练阶段通过奖励模型注入世界知识，推理时完全移除。这一设计从根源上解决了**世界模型的丰富未来知识与实时轻量部署之间的冲突**。

### 2. 因果机制：世界奖励模型作为核心调节器

WPT 的方法创新并非简单的模块堆砌，而是围绕一个核心因果调节器——**可训练的世界奖励模型**——构建了完整的知识迁移链路：

1. **教师策略与世界模型的交互**：世界模型基于历史观测和动作条件自回归预测未来世界嵌入 $\boldsymbol{F}_{t+1}^{\mathrm{w}}$，教师策略通过交叉注意力与之交互生成多模态候选轨迹 $\hat{\mathcal{T}}$（Eq. 8）。
2. **奖励模型的轨迹评估**：奖励模型在预测的未来世界状态下评价每条候选轨迹，输出两类奖励信号——模仿奖励 $r_{\mathrm{im}}$（对齐人类偏好）和仿真奖励 $r_{\mathrm{sim}}$（包含 NC、DAC、TTC、EP、Comf 五项安全与效率指标），通过加权融合选择最优轨迹 $\boldsymbol{\tau}^*$（Eq. 10, 14）。
3. **知识蒸馏至学生**：通过策略蒸馏（对齐规划查询的 L2 距离，Eq. 15）和世界奖励蒸馏（对齐奖励分数，Eq. 16），将教师的世界感知能力迁移至轻量单模态学生策略。

这一因果链路的关键证据来自消融实验（Table 3）：**仅使用模仿奖励即可提升性能，但加入仿真奖励是安全增益的主要驱动力**；且仅在训练时使用奖励模型即可达到最佳效果（0.61m L2 / 0.11% 碰撞），推理时额外使用奖励模型反而无额外增益。

### 3. 与具体基线工作的关系

在 nuScenes 验证集上（Table 1），WPT-Teacher 以 **0.61m Avg. L2** 和 **0.11% Avg. Collision** 超越所有对比方法，包括 UniAD（Hu et al., CVPR 2023）、VAD、Drive-OccWorld、WoTE 等。值得注意的是，WPT 不使用任何专家特征蒸馏（如表 2 中 `*` 标记者），而部分对比方法依赖此类先验，这凸显了 WPT 通过世界模型交互自主获取安全知识的能力。

在 Bench2Drive 闭环基准上（Table 2），WPT-Teacher 的 Driving Score 达到 **79.23**（基线 65.23，+14.00），Success Rate 达到 **54.54%**（基线 34.10%，+20.44），验证了世界知识在复杂闭环场景中的泛化价值。

### 4. 适用边界与局限

尽管 WPT 在安全性和准确性上取得了显著提升，其适用边界和局限同样值得关注：

- **舒适性与效率的权衡**：WPT 在 Bench2Drive 闭环场景中的 Comfort 得分相对较低（Table 2 中 17.80/16.39），表明当前奖励塑形在安全-效率-舒适性三者之间存在张力。未来需设计更精细的奖励函数以在不牺牲安全的前提下提升舒适性。
- **世界模型质量的依赖性**：世界模型为预训练并冻结权重（文中采用 Drive-OccWorld），其预测质量直接影响奖励信号的有效性。Table 5 的消融表明，世界模型生成的占用（WM-Occ）比真实占用（GT-Occ）更有效（0.61/0.11 vs 0.65/0.15），因为世界模型提供了预测的未来动态信息；但这也意味着低质量世界模型可能限制性能上限。
- **推理延迟的边际成本**：若教师策略在推理时开启奖励模型，会引入约 26ms 额外延迟（286→312ms，Table 9）。蒸馏可消除此开销，但在资源受限且需要在线奖励评估的特殊场景仍需权衡。

### 5. 开放问题

WPT 范式的成功引出了若干值得进一步探索的方向：

1. **跨任务泛化**：WPT 的“世界模型训练时指导、蒸馏后轻量部署”范式能否扩展至其他视觉-语言-动作模型或机器人操作任务？这需要验证世界模型在非自动驾驶场景中的预测能力和奖励设计的可迁移性。
2. **动态世界模型适配**：当前世界模型为冻结状态，若世界模型在训练过程中动态更新或根据场景适应性调整，蒸馏策略如何保持稳定？这可能涉及课程学习或渐进式蒸馏策略。
3. **舒适性优化**：在不牺牲效率和安全性的前提下进一步提升舒适性，需要更精细的奖励塑形，例如引入加加速度（jerk）约束或个性化驾驶风格建模。



## 原文 PDF

![[paperPDFs/CVPR_2026/WPT_World_to_Policy_Transfer_via_Online_World_Model_Distillation.pdf]]
