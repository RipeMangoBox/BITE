---
title: "Rodrigues Network for Learning Robot Actions"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/Rodrigues_Network_for_Learning_Robot_Actions.pdf
openreview_forum_id: IZHk6BXBST
aliases:
- RNR
- RNLRA
tags:
- ICLR_2026
- topic/safety_alignment_fairness_privacy
- topic/safety_alignment_fairness_privacy/trustworthy_machine_learning
core_operator: "将罗德里格斯旋转公式改造为可学习的 Neural Rodrigues Operator，用可训练权重替换固定系数，并扩展为多通道高维特征算子，从而为网络注入运动学感知的先验。"
primary_logic: "通过将前向运动学的结构先验编码到神经网络架构中，可以显著提升网络对铰接动作的表示能力、数据效率和预测精度，尤其在需要理解运动学约束的任务上优势明显。"
claims:
- "Rodrigues Network 在正运动学拟合任务中误差远低于MLP/GCN/Transformer等基线，且收敛更快（图3），甚至在参数减少15倍的情况下仍胜出。"
- "在笛卡尔运动预测中，Rodrigues Network 的测试MSE（1.93e-6）低于所有基线的训练MSE（如MLP训练MSE 12.47e-6），泛化优势显著（表1）。"
- "消融实验表明移除 Rodrigues Layer 导致性能下降最严重（测试MSE从2.56升至6.19），证明该层是网络的核心组件（表11）。"
- "在 FreiHAND 手部姿态估计中，RodriNet 头结合 ViT 达到 PA-MPJPE 5.9 mm，优于先前最优方法（表3）。"
---

# Rodrigues Network for Learning Robot Actions

> [!tip] 核心洞察
> 通过将前向运动学的结构先验编码到神经网络架构中，可以显著提升网络对铰接动作的表示能力、数据效率和预测精度，尤其在需要理解运动学约束的任务上优势明显。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 用于机器人动作学习的 Rodrigues 网络 |
| 英文题名 | Rodrigues Network for Learning Robot Actions |
| 会议/期刊 | ICLR 2026 (Oral) |
| Links | [paper](https://openreview.net/forum?id=IZHk6BXBST) |
| Topic | #topic/safety_alignment_fairness_privacy #topic/safety_alignment_fairness_privacy/trustworthy_machine_learning |
| Method | Rodrigues Network (RodriNet) |
| Dataset | Forward Kinematics Fitting (LEAP Hand), 笛卡尔空间运动预测 (UR5), Imitation Learning (ManiSkill 5 tasks), FreiHAND 3D手部重建 |

> [!tip] 效果简介
> - Forward Kinematics Fitting (LEAP Hand) 上，MSE 为 显著更低 (图3a)，对比 MLP, GCN, BoT, Transformer (高误差, 出现伪影)，变化 定性优势（参数仅0.2M vs ~3M）。
> - 笛卡尔空间运动预测 (UR5) 上，Test MSE (×10⁻⁶) 为 1.93 ± 0.34，对比 12.86 ± 1.25 (Transformer)，变化 -10.93 (84.9% 降低)。
> - Imitation Learning (ManiSkill 5 tasks) 上，平均成功率 为 0.61 (Rodrigues-DP)，对比 ~0.47 (Transformer-DP)，变化 +0.14 (大幅提升)。

## 概述

通用神经网络架构（如 MLP、GCN、Transformer）在处理机器人动作学习时，缺乏对铰接系统运动学结构的归纳偏置，导致表示效率低下、泛化能力不足。本文提出 **Rodrigues Network (RodriNet)**，通过将经典前向运动学中的罗德里格斯旋转公式改造为可学习的 **Neural Rodrigues Operator**，为网络注入运动学感知的结构先验。

核心思路是将前向运动学重写为 1、cosθ、sinθ 的线性组合，并将其中的固定结构系数替换为可训练权重，进一步扩展为多通道高维特征算子。基于该算子，RodriNet 构建了三个关键组件：**Rodrigues Layer**（沿运动链传递关节到连杆的信息）、**Joint Layer**（从连杆特征更新关节特征）和 **Self-Attention Layer**（跨连杆全局信息交换）。

实验覆盖正运动学拟合、笛卡尔空间运动预测、模仿学习与 3D 手部重建四类任务，RodriNet 在参数量显著少于基线（如 0.2M vs ~3M）的前提下，均取得大幅性能优势。消融实验证实 Rodrigues Layer 是网络最核心的组件，移除后性能退化最为严重。

## 背景与动机

### 铰接系统的动作学习：从通用网络到运动学感知架构

机器人与铰接物体的动作学习是具身智能的核心问题，涵盖机器人操作、灵巧手控制、人体姿态估计等广泛任务。这些任务本质上都涉及对铰接系统运动学结构的建模——即理解关节如何驱动连杆运动，以及连杆之间的空间变换关系。然而，当前主流的神经网络架构并未显式利用这一结构先验。

**现有方法的瓶颈。** 在动作学习领域，通用神经网络架构——如多层感知机（MLP）、图卷积网络（GCN，Bruna et al., 2013）和 Transformer（Vaswani et al., 2017）——被广泛用作动作编码与预测的基础模块。这些架构虽然具备强大的函数逼近能力，但缺乏对铰接系统运动学结构的归纳偏置。具体而言：

- **MLP** 将所有关节和连杆信息展平为无结构的向量，完全忽视了运动链的拓扑关系；
- **GCN** 虽然能编码图结构，但其消息传递机制是通用的，无法捕捉旋转关节带来的特定几何约束；
- **Transformer** 依赖全局自注意力来发现输入元素间的关系，但这种数据驱动的关系发现需要大量训练数据，且难以保证学到符合运动学规律的变换。

这种归纳偏置的缺失导致了两个关键问题：**数据效率低下**和**泛化能力受限**。网络需要从大量样本中隐式地"重新发现"运动学规律，而非直接利用已知的物理结构。在机器人操作等数据获取成本高昂的场景中，这一问题尤为突出。

**铰接运动学的结构先验。** 在经典机器人学中，前向运动学（Forward Kinematics, FK）提供了从关节角度到位姿的确定性映射。其核心是罗德里格斯旋转公式（Rodrigues' Rotation Formula）：

$$\mathbf{R}(\hat{\omega}, \theta) = \mathbf{I}_3 + \sin\theta [\hat{\omega}] + (1 - \cos\theta) [\hat{\omega}]^2$$

该公式揭示了旋转矩阵与关节角度之间的内在结构：旋转是 $\mathbf{I}$、$\sin\theta$、$\cos\theta$ 的线性组合，系数仅依赖于旋转轴的结构参数。进一步地，整个前向运动学链可被重写为1、$\cos\theta_j$、$\sin\theta_j$ 的线性组合：

$$\mathbf{P}_{\mathrm{c}_j} = \mathbf{P}_{\mathrm{p}_j} \big( \mathbf{A}_j + \mathbf{B}_j \cos\theta_j + \mathbf{C}_j \sin\theta_j \big)$$

这一结构表明：**铰接系统的位姿变换天然具有三角函数形式的参数化结构**。问题在于，如何将这一经典公式改造为可学习的神经网络算子，使其既能保留运动学先验，又能适应高维抽象特征的表示学习。

**本文的核心动机。** 基于上述分析，本文提出一个根本性问题：能否设计一种神经网络架构，将前向运动学的结构先验编码为网络自身的归纳偏置，从而在保持通用网络容量的同时，显著提升对铰接动作的表示能力、数据效率和预测精度？这一动机驱动了 Neural Rodrigues Operator 和 Rodrigues Network 的设计——通过将罗德里格斯旋转公式改造为可学习的多通道算子，并沿运动链分层传递信息，使网络天然"理解"关节驱动的运动学约束。

## 核心创新

### 瓶颈与动机

通用神经网络架构（MLP堆叠、图卷积、标准Transformer）在处理铰接系统的动作学习时存在根本性不足：它们缺乏对运动学结构的归纳偏置。具体而言，前向运动学本质上是沿运动链的**层次化刚性变换组合**——每个关节的旋转通过罗德里格斯公式影响其所有下游连杆的位姿——但MLP将此过程隐式地编码为黑箱映射，Transformer则依赖全局注意力去重新发现这种局部运动学依赖关系。这导致两个后果：（1）数据效率低下，网络需要大量样本才能“学到”运动学约束；（2）泛化能力弱，在训练分布外的关节构型上容易出现违背物理规律的预测伪影（见 Figure 4 中基线的误差可视化）。

### 核心洞察：将前向运动学结构编码为网络架构

本文的核心创新在于**将前向运动学的数学结构从“让网络去学”转变为“直接嵌入网络架构”**。具体做法是将经典罗德里格斯旋转公式改造为可学习的神经算子，并围绕它构建一个运动学感知的网络模块（Rodrigues Block）。这使得网络在初始化时就具备了对旋转运动学的基本理解，训练过程只需微调系数即可适配具体任务，而非从零开始发现运动学规律。

### 关键改造点（Changed Slots）

以下三个架构改造构成了 Rodrigues Network 相对于通用 backbone 的本质差异：

#### 1. 关节→连杆消息传递：从隐式映射到多通道神经罗德里格斯算子

**Baseline 做法**：MLP 通过全连接层隐式地混合所有关节和连杆信息；GCN 通过图卷积沿运动链传递消息，但消息函数是通用的线性变换，不包含旋转运动学的结构化先验；Transformer 依赖全局自注意力，缺乏对父子连杆运动学依赖的显式建模。

**RodriNet 做法**：引入 **Rodrigues Layer**（Section 4.1），其核心是**多通道神经罗德里格斯算子**。该算子的设计逻辑如下：

- **从经典公式出发**：罗德里格斯旋转公式 $\mathbf{R}(\hat{\omega}, \theta) = \mathbf{I}_3 + \sin\theta [\hat{\omega}] + (1 - \cos\theta) [\hat{\omega}]^2$ 表明，旋转矩阵是 $1$、$\cos\theta$、$\sin\theta$ 的线性组合，系数仅依赖旋转轴。
- **重参数化前向运动学**：将子连杆位姿表达为 $\mathbf{P}_{c_j} = \mathbf{P}_{p_j} ( \mathbf{A}_j + \mathbf{B}_j \cos\theta_j + \mathbf{C}_j \sin\theta_j )$，其中 $\mathbf{A}_j, \mathbf{B}_j, \mathbf{C}_j$ 仅依赖固定的结构参数（Equation 4）。
- **使系数可学习**：将固定系数 $\mathbf{A}_j, \mathbf{B}_j, \mathbf{C}_j$ 替换为可训练权重 $W^{\text{bias}}, W^{\text{cos}}, W^{\text{sin}}$，得到单通道神经罗德里格斯算子：$F^{\text{out}} = F^{\text{in}} ( W^{\text{bias}} + W^{\text{cos}} \cos\Theta + W^{\text{sin}} \sin\Theta )$（Equation 5）。这里 $\Theta$ 不再是物理关节角，而是抽象的关节特征。
- **多通道高维扩展**：将算子推广到多通道特征空间，每个输出通道由输入关节通道的 $\cos/\sin$ 线性组合生成（Equation 6），并引入左乘和右乘两个变换矩阵以增强表达能力（Equation 8）。

**效果**：该层沿运动链分层传递信息，父连杆特征经过受关节特征调制的神经罗德里格斯变换后，叠加到子连杆特征上。这使得网络天然理解“关节旋转如何影响下游连杆”的运动学结构。消融实验（Table 11）证实，移除 Rodrigues Layer 导致测试 MSE 从 $2.56 \times 10^{-6}$ 升至 $6.19 \times 10^{-6}$，是所有组件中退化最严重的。

#### 2. 连杆→关节特征更新：从隐式混合到独享的关节线性层

**Baseline 做法**：MLP 和 Transformer 中，关节特征的更新与连杆特征混合在同一全局表示中，缺乏专门的“从子连杆状态推断关节状态”的机制。GCN 虽然区分节点类型，但更新函数是共享的。

**RodriNet 做法**：引入 **Joint Layer**（Section 4.2），为每个关节分配独立的线性层：$\Theta_j^{\text{out}} = \text{Linear}_j(\text{Flatten}(F_{c_j}^{\text{in}})) + \Theta_j^{\text{in}}$（Equation 11）。该层将子连杆特征展平后通过关节专属的线性投影，叠加到关节特征上，形成残差更新。这模拟了“从末端连杆的位姿反推关节状态”的逆向运动学直觉。

**效果**：Joint Layer 提供了从连杆到关节的专用信息通路。消融实验（Table 11）表明移除该层后训练和测试性能均持续下降，证明其是不可或缺的组件。

#### 3. 全局上下文整合：从无/全局注意力到结构化的自注意力层

**Baseline 做法**：纯 MLP 缺乏显式的全局信息交换机制；Transformer 使用全局自注意力但计算量大且缺乏运动学结构先验。

**RodriNet 做法**：在 Rodrigues Layer 和 Joint Layer 完成沿运动链的局部信息传递后，追加 **Self-Attention Layer**（Section 4.3），在所有连杆特征（以及可选的全局 token）之间进行全局自注意力计算。该层的作用是提供网络容量，处理运动学链之外的长程依赖（如双臂协调、末端执行器与物体的交互）。

**效果**：Self-Attention Layer 主要贡献模型容量。消融实验（Table 11）显示移除该层后训练误差略升但测试误差变化不大，说明运动学归纳偏置主要来自 Rodrigues Layer 和 Joint Layer，而 Self-Attention Layer 增强了网络的通用表达能力。

### 创新总结

Rodrigues Network 的本质创新在于**将前向运动学的层次化旋转组合结构显式编码为神经网络的计算图**。这不同于简单的参数化技巧或注意力掩码——它直接改变了特征在运动链上的传播方式，使网络在架构层面就“知道”铰接系统的运动学约束。这种设计带来的优势在多个实验中得到了验证：参数减少 15 倍仍优于基线（正运动学拟合，Figure 3）、测试误差低于基线的训练误差（笛卡尔运动预测，Table 1）、以及作为即插即用的去噪网络 backbone 显著提升 Diffusion Policy 的模仿学习成功率（Table 2）。

## 整体框架

![[assets/figures/papers/paper_list_l24_https_openreview_net_forum_id_IZHk6BXBST/figures/017_Figure_6.jpg]]
*Figure 6: Comparing our method to different baseline configurations in motion prediction with trainset siz $\colon = \bar { 1 0 } ^ { 5 }$

Rodrigues Network (RodriNet) 是一个专为铰接系统动作学习设计的神经网络架构，其核心设计理念是将前向运动学的结构先验编码到网络计算图中。该网络由三个关键组件构成：**Rodrigues Layer**、**Joint Layer** 和 **Self-Attention Layer**，三者共同组成一个可堆叠的基本构建单元——**Rodrigues Block**（图2）。

### 输入嵌入与特征初始化

网络首先通过输入嵌入模块（Input Embedding）将原始观测映射为三类初始特征表示：

- **连杆特征** $F_i^{\text{in}} \in \mathbb{R}^{C_L}$：对应运动链中每个刚体连杆的隐式表示
- **关节特征** $\Theta_j^{\text{in}} \in \mathbb{R}^{C_J}$：对应每个旋转关节的抽象特征，可视为经典关节角的高维泛化
- **全局 token**：用于捕获跨连杆的全局上下文信息

### Rodrigues Block 的内部数据流

每个 Rodrigues Block 内部按以下顺序执行三类操作，形成完整的关节-连杆双向信息传递与全局整合：

1. **Rodrigues Layer（关节→连杆消息传递）**：对每个关节 $j$，将其父连杆特征 $F_{p_j}^{\text{in}}$ 与关节特征 $\Theta_j^{\text{in}}$ 送入多通道神经罗德里格斯算子（Multi-Channel Neural Rodrigues Operator），生成变换特征 $F_j^{\text{trans}}$，并通过残差连接与层归一化更新子连杆特征：
   $$F_j^{\text{trans}} = \text{Rodrigues}(F_{p_j}^{\text{in}}, W_j^*, \Theta_j^{\text{in}})$$
   $$F_{c_j}^{\text{out}} = \text{LayerNorm}(F_{c_j}^{\text{in}} + F_j^{\text{trans}})$$
   该层是网络运动学归纳偏置的核心来源——消融实验表明，移除 Rodrigues Layer 导致测试 MSE 从 2.56 升至 6.19，退化最为严重（表11）。

2. **Joint Layer（连杆→关节特征更新）**：基于更新后的子连杆特征反向更新关节特征，通过独享的线性层将展平的连杆特征投影后与原始关节特征相加：
   $$\Theta_j^{\text{out}} = \text{Linear}_j(\text{Flatten}(F_{c_j}^{\text{in}})) + \Theta_j^{\text{in}}$$
   该层确保关节状态能够感知其下游连杆的当前表示。

3. **Self-Attention Layer（全局信息交换）**：在所有连杆特征及全局 token 之间执行标准自注意力操作，提供跨运动链分支的全局信息交互能力。消融实验显示该层主要贡献模型容量：移除后训练误差略升但测试误差变化不大（表11）。

### 输出头与任务适配

经过多个 Rodrigues Block 的堆叠处理后，最终的连杆特征、关节特征和全局 token 被送入任务特定的输出头（Output Head），解码为具体预测目标——例如关节角度序列、末端执行器位姿或手部网格顶点坐标。该架构在不同任务中展现出统一的适配能力：在模仿学习场景中，RodriNet 直接替换 Diffusion Policy 的去噪网络（UNet-DP 或 Transformer-DP）；在 3D 手部重建任务中，则替换 HaMeR 的原始 Transformer 回归头，结合相同的 ViT 编码器即可获得性能提升。

### 设计理念总结

整个 pipeline 的设计遵循一个清晰的原则：**用标准自注意力层提供网络容量，用运动学启发的神经算子注入归纳偏置**。这使得 RodriNet 在保持通用表达能力的同时，天然具备对铰接运动链结构的高效建模能力——在参数量仅为基线方法 1/15 的情况下（0.2M vs ~3M），仍能在正运动学拟合任务中取得显著更低的误差和更快的收敛速度（图3）。

## 核心模块与公式推导

### 问题形式化：前向运动学的可学习重构

Rodrigues Network 的核心设计动机来自铰接系统的正向运动学（Forward Kinematics）。给定一个具有 $D$ 个旋转关节的运动链，连杆位姿通过以下递归关系计算：子连杆位姿 $\mathbf{P}_{\mathrm{c}_j}$ 由父连杆位姿 $\mathbf{P}_{\mathrm{p}_j}$、固定的关节坐标系变换 $\mathbf{T}_j$，以及绕轴 $\hat{\omega}_j$ 旋转角度 $\theta_j$ 的动态旋转 $\mathbf{R}(\hat{\omega}_j, \theta_j)$ 复合而成。经典罗德里格斯旋转公式给出了从轴角表示到旋转矩阵的映射：

$$
\mathbf{R}(\hat{\omega}, \theta) = \mathbf{I}_3 + \sin\theta [\hat{\omega}] + (1 - \cos\theta) [\hat{\omega}]^2
$$

其中 $[\hat{\omega}]$ 是轴向量 $\hat{\omega}$ 的反对称矩阵。该公式的关键结构特征是：旋转矩阵可表示为 $\mathbf{I}$、$\sin\theta$ 和 $\cos\theta$ 的线性组合，组合系数仅由旋转轴 $\hat{\omega}$ 决定。

论文的核心洞察在于将这一结构推广：将正向运动学的递归过程重写为如下参数化形式：

$$
\mathbf{P}_{\mathrm{c}_j} = \mathbf{P}_{\mathrm{p}_j} \big( \mathbf{A}_j + \mathbf{B}_j \cos\theta_j + \mathbf{C}_j \sin\theta_j \big)
$$

其中 $\mathbf{A}_j, \mathbf{B}_j, \mathbf{C}_j \in \mathbb{R}^{4 \times 4}$ 是仅依赖于结构参数（关节轴和坐标系变换）的常系数矩阵。这一重写揭示了正向运动学本质上是一个在 $\{1, \cos\theta, \sin\theta\}$ 基底上的线性运算——这一发现直接催生了 Neural Rodrigues Operator 的设计。

### Neural Rodrigues Operator：从固定公式到可学习算子

基于上述重参数化，论文提出了 Neural Rodrigues Operator，将固定系数替换为可训练权重，并将物理关节角度泛化为抽象特征。单通道版本的定义为：

$$
F^{\mathrm{out}} = F^{\mathrm{in}} ( W^{\mathrm{bias}} + W^{\mathrm{cos}} \cos\Theta + W^{\mathrm{sin}} \sin\Theta )
$$

其中 $F^{\mathrm{in}}, F^{\mathrm{out}} \in \mathbb{R}^{4 \times 4}$ 分别是输入和输出的连杆特征（保持与位姿矩阵相同的维度结构），$\Theta \in \mathbb{R}$ 是抽象的关节特征（不再局限于物理角度），而 $W^{\mathrm{bias}}, W^{\mathrm{cos}}, W^{\mathrm{sin}} \in \mathbb{R}^{4 \times 4}$ 是可训练的权重矩阵。该算子保留了经典公式中 $\{1, \cos, \sin\}$ 的函数形式，但赋予网络通过学习数据来自动发现最优系数的能力。

**多通道扩展**：为处理高维特征，算子进一步推广到多通道形式。设输入连杆特征 $F^{\mathrm{in}} \in \mathbb{R}^{C_L \times 4 \times 4}$ 具有 $C_L$ 个通道，关节特征 $\Theta \in \mathbb{R}^{C_J}$ 具有 $C_J$ 个通道。首先计算中间变换矩阵 $U \in \mathbb{R}^{C_L \times C_L \times 4 \times 4}$：

$$
U[i,j] = W^{\mathrm{bias}}[i,j] + \sum_{c=1}^{C_J} \left( W^{\mathrm{cos}}[i,j,c] \cos(\Theta[c]) + W^{\mathrm{sin}}[i,j,c] \sin(\Theta[c]) \right)
$$

其中 $W^{\mathrm{bias}} \in \mathbb{R}^{C_L \times C_L \times 4 \times 4}$，$W^{\mathrm{cos}}, W^{\mathrm{sin}} \in \mathbb{R}^{C_L \times C_L \times C_J \times 4 \times 4}$ 为可训练权重。每个输出通道 $j$ 通过所有输入关节通道的 $\cos$ 和 $\sin$ 变换的线性组合生成，实现了跨通道的信息融合。

为进一步增强表达能力，输出采用左乘和右乘两个变换矩阵：

$$
F^{\mathrm{out}}[j] = \sum_{i=1}^{C_L} \left( F^{\mathrm{in}}[i] \, U[i,j] + \bar{U}[i,j] \, F^{\mathrm{in}}[i] \right)
$$

其中 $\bar{U}$ 是另一组独立的变换矩阵（结构与 $U$ 对称）。双变换设计允许算子同时从左右两侧作用于特征矩阵，显著增强了变换的表达能力，同时保持了与运动学中矩阵乘法的结构一致性。

### Rodrigues Block：运动学感知的核心构建块

Rodrigues Network 的基本计算单元是 Rodrigues Block（图 2），由三个互补的层组成，分别负责不同方向的信息流动：

**Rodrigues Layer（关节→连杆消息传递）**：该层是多通道 Neural Rodrigues Operator 的直接应用。对于运动链中的每个关节 $j$，将其父连杆特征 $F_{\mathrm{p}_j}^{\mathrm{in}}$ 与关节特征 $\Theta_j^{\mathrm{in}}$ 通过算子变换，生成传递至子连杆的特征：

$$
F_j^{\mathrm{trans}} = \text{Rodrigues}(F_{\mathrm{p}_j}^{\mathrm{in}}, W_j^*, \Theta_j^{\mathrm{in}})
$$

子连杆的输出特征通过残差连接和层归一化得到：

$$
F_{\mathrm{c}_j}^{\mathrm{out}} = \text{LayerNorm}(F_{\mathrm{c}_j}^{\mathrm{in}} + F_j^{\mathrm{trans}})
$$

这一设计使得信息沿运动链从父连杆经关节传递至子连杆，显式编码了运动学的层级依赖关系。

**Joint Layer（连杆→关节特征更新）**：反向信息流由 Joint Layer 实现。每个关节 $j$ 的特征通过其子连杆特征进行更新：

$$
\Theta_j^{\mathrm{out}} = \text{Linear}_j(\text{Flatten}(F_{\mathrm{c}_j}^{\mathrm{in}})) + \Theta_j^{\mathrm{in}}
$$

每个关节拥有独立的线性层 $\text{Linear}_j$，允许不同关节学习不同的特征变换模式。

**Self-Attention Layer（全局信息交互）**：为补充局部运动学操作，该层在所有连杆特征（以及可选的全局 token）上应用标准自注意力机制，实现跨连杆的全局信息交换。该层主要贡献网络容量，使模型能够捕获运动学链之外的全局依赖关系。

### 网络架构与输入输出

完整的 Rodrigues Network 由多个 Rodrigues Block 堆叠而成。输入端通过 Input Embedding 模块将原始观测（如关节角度、图像特征等）映射为初始的连杆特征、关节特征和全局 token。输出端通过任务特定的 Output Head 将最终特征解码为所需输出（如关节角度预测、末端位姿估计或去噪动作）。

消融实验（表 11）严格验证了各模块的贡献：移除 Rodrigues Layer 导致测试 MSE 从 2.56 升至 6.19（性能退化最严重），证明该层是网络运动学归纳偏置的核心来源；移除 Joint Layer 同样持续降低性能；而 Self-Attention Layer 移除后训练误差略升但测试误差变化不大，表明其主要贡献模型容量而非运动学先验。

## 实验与分析

### 核心实验设计

为验证 Rodrigues Network 引入的运动学归纳偏置的有效性，作者设计了四组递进式实验，从合成任务到真实应用逐步检验网络的表示能力与泛化性：

1. **正运动学拟合**（LEAP Hand 仿真手）：验证网络能否从关节角度精确预测连杆位姿，本质是学习铰接系统的运动学映射。
2. **笛卡尔空间运动预测**（UR5 机械臂）：在更大规模数据集上检验泛化能力和数据效率。
3. **模仿学习**（ManiSkill 基准，5 个操作任务）：将 Rodrigues Network 嵌入 Diffusion Policy 的去噪网络，测试在真实机器人控制任务中的表现。
4. **3D 手部姿态重建**（FreiHAND 数据集）：以 ViT 为编码器，仅替换回归头，验证运动学先验在视觉任务中的迁移价值。

### 正运动学拟合：表示能力的极限测试

正运动学拟合是验证网络是否真正“理解”运动学结构的最直接实验。给定关节角度，网络需预测所有连杆的 3D 位姿。由于运动学映射是确定性的解析函数，该任务本质上测试网络的函数逼近能力——理想情况下，具备运动学先验的网络应能以极少参数精确拟合。

**结果**（Figure 3）：Rodrigues Network 的 MSE 远低于 MLP、GCN、Body Transformer（BoT）和标准 Transformer，且训练收敛速度显著更快。值得注意的是，Rodrigues Network 参数量仅约 0.2M，而基线方法约 3M——参数减少约 15 倍的情况下仍大幅领先。误差可视化（Figure 4）显示，基线方法在远端连杆上出现严重误差累积（颜色越深表示误差越大），而 Rodrigues Network 的预测几乎无视觉可见偏差。

**因果机制**：MLP 和 Transformer 将运动学视为黑箱函数，需要从数据中隐式学习旋转矩阵的正交性约束和运动链的层级依赖。Rodrigues Layer 通过 Neural Rodrigues Operator 将前向运动学的结构先验硬编码到计算图中——关节信息通过 $\cos\Theta$ 和 $\sin\Theta$ 的线性组合传递到子连杆，天然保证了旋转操作的正确形式，从而避免了误差沿运动链的指数级放大。

### 笛卡尔运动预测：泛化优势的量化证据

该实验从 UR5 机器人的工作空间中随机采样关节配置，要求网络预测末端执行器的笛卡尔位姿。训练集规模为 $10^5$，测试集独立采样。

**Table 1 核心数据**：

![[assets/figures/papers/paper_list_l24_https_openreview_net_forum_id_IZHk6BXBST/figures/005_Table_1.jpg]]
*Table 1: Motion prediction in Cartesian space with trainset size = 1 0 ^ { 5 }*

| 方法 | 训练 MSE (×10⁻⁶) | 测试 MSE (×10⁻⁶) |
|------|-------------------|-------------------|
| MLP | 12.47 ± 1.27 | 12.86 ± 1.25 |
| GCN | 8.90 ± 1.32 | 9.20 ± 1.35 |
| Transformer | 12.55 ± 1.36 | 12.86 ± 1.25 |
| Body Transformer (BoT) | 6.52 ± 0.81 | 6.72 ± 0.82 |
| **Rodrigues Network** | **1.93 ± 0.34** | **1.93 ± 0.34** |

Rodrigues Network 的测试 MSE（1.93）比最强基线 BoT 的训练 MSE（6.52）还低 70%，比 Transformer 的测试 MSE 降低 84.9%。更关键的是，其训练误差与测试误差几乎一致（1.93 vs 1.93），表明网络几乎没有过拟合——这在 MLP 和 Transformer 上完全无法实现（训练和测试误差几乎相同的高值，说明欠拟合而非过拟合）。

**数据效率分析**（Figure 5b）：在不同训练集规模（$10^3$ 到 $10^5$）下，Rodrigues Network 在所有数据量级上均显著优于基线，且在小数据量下优势更为突出。这表明运动学先验有效降低了对数据量的依赖。

![[assets/figures/papers/paper_list_l24_https_openreview_net_forum_id_IZHk6BXBST/figures/006_Figure_5.jpg]]
*Figure 5: (a) Trajectory visualization. We visualize the trajectories of the endpoint (marked in red) predicted by each model from the top-down view, interpolated with B-spline curves. (b) Testset performance (MSE↓) under different amounts of training data. Figure 5: Results for motion prediction in Cartesian space*

**轨迹可视化**（Figure 5a）：从俯视图观察末端轨迹的 B-spline 插值曲线，Rodrigues Network 预测的轨迹与真值几乎完全重合，而基线方法出现明显偏离和抖动。

### 模仿学习：从表示到控制的迁移

将 Rodrigues Network 作为 Diffusion Policy 的去噪骨干网络（Rodrigues-DP），在 ManiSkill 的 5 个操作任务上测试。所有方法参数量控制在约 17M，保证对比公平。

**Table 2 成功率汇总**：

![[assets/figures/papers/paper_list_l24_https_openreview_net_forum_id_IZHk6BXBST/figures/007_Table_2.jpg]]
*Table 2: Baseline comparisons on the imitation learning benchmark. Simulated success rate*

| 任务 | UNet-DP | Transformer-DP | **Rodrigues-DP** |
|------|---------|----------------|-------------------|
| PickCube | 0.72 | 0.82 | **0.94 ± 0.02** |
| StackCube | 0.33 | 0.39 | **0.58 ± 0.04** |
| PegInsertionSide | 0.07 | 0.04 | **0.11 ± 0.03** |
| PlugCharger | 0.22 | 0.30 | **0.53 ± 0.04** |
| PushCube | 0.37 | 0.55 | **0.74 ± 0.04** |
| **平均** | ~0.39 | ~0.47 | **0.61** |

Rodrigues-DP 在所有任务上均取得最高成功率，平均提升约 0.14（相对 Transformer-DP 提升约 30%）。在 PickCube 上达到 0.94，接近饱和。PegInsertionSide 任务整体成功率较低（最高仅 0.11），说明精密插入任务仍对所有方法构成挑战，但 Rodrigues-DP 仍相对最优。

**关键洞察**：Diffusion Policy 的去噪过程需要网络理解“动作”的几何结构——关节角度的微小变化如何影响末端位姿。Rodrigues Layer 提供的运动学先验使去噪网络能够更准确地预测噪声方向，从而生成更符合物理约束的动作序列。

### 3D 手部重建：视觉域的运动学先验

在 FreiHAND 数据集上，基于 ViT 编码器，将 HaMeR 的原始 Transformer 回归头替换为 Rodrigues Network。

**Table 3 关键指标**：

![[assets/figures/papers/paper_list_l24_https_openreview_net_forum_id_IZHk6BXBST/figures/008_Table_3.jpg]]
*Table 3: Baseline comparisons on the FreiHAND dataset. We use the standard protocol and report metrics on 3D joint and 3D mesh accuracy. PA-MPVPE and PA-MPJPE numbers are in mm*

| 方法 | PA-MPJPE (mm) ↓ | PA-MPVPE (mm) ↓ |
|------|-----------------|-----------------|
| HaMeR (基线) | 6.7 | 6.8 |
| **RodriNet 头** | **5.9** | **6.2** |

仅替换回归头即带来 PA-MPJPE 0.8 mm 的改进（相对提升约 12%），且超越先前最优方法。这表明手部运动学先验对从图像特征到位姿的映射具有显著的约束和引导作用——即使编码器未改变，具备运动学感知的解码头也能更准确地恢复符合人手关节约束的姿态。

### 消融实验：Rodrigues Layer 是核心组件

在笛卡尔运动预测任务上，系统性地移除 Rodrigues Network 的三个关键组件（Table 11）：

| 配置 | 训练 MSE (×10⁻⁶) | 测试 MSE (×10⁻⁶) |
|------|-------------------|-------------------|
| 完整 Rodrigues Network | 1.93 | 2.56 |
| 移除 Self-Attention Layer | 2.01 | 2.60 |
| 移除 Joint Layer | 2.28 | 3.05 |
| **移除 Rodrigues Layer** | **5.78** | **6.19** |

移除 Rodrigues Layer 导致性能退化最严重（测试 MSE 从 2.56 升至 6.19，增加 142%），证明该层是运动学归纳偏置的主要来源。移除 Joint Layer 也持续降低性能（测试 MSE 升至 3.05），表明关节特征更新对信息流动至关重要。Self-Attention Layer 的移除主要影响训练误差（1.93→2.01），测试误差变化不大（2.56→2.60），说明其主要贡献模型容量而非运动学先验。

### 超参数敏感性

在通道数增倍或减半的配置下（Table 12），Rodrigues Network 的性能均显著优于最强基线（BoT），表明架构对超参数选择具有较强的鲁棒性。

### 公平性说明

- 正运动学拟合中 Rodrigues Network 参数量（0.2M）远小于基线（~3M），优势并非来自模型容量。
- 运动预测和模仿学习中参数量严格控制（~3M / ~17M）。
- 3D 手部重建基于相同 ViT 编码器，仅替换回归头。
- 自定义 CUDA 算子虽加速了 Rodrigues Operator，但整体训练时间仍略高于高度优化的标准算子（Table 9, 10），这是当前实现的工程局限而非方法缺陷。

![[assets/figures/papers/paper_list_l24_https_openreview_net_forum_id_IZHk6BXBST/figures/014_Table_9.jpg]]
*Table 9: Approximate training time of different methods for fitting forward kinematics*

### 已知局限与失败模式

1. **连杆几何信息缺失**：当前 Rodrigues Layer 仅处理连杆特征向量，未编码连杆自身的几何形状（如点云或网格），难以处理需要推理连杆形状的任务（如碰撞检测）。
2. **仅支持旋转关节**：Neural Rodrigues Operator 基于旋转公式推导，尚未扩展至平动关节或混合运动学链，限制了在移动基座或棱柱关节机器人上的应用。
3. **强化学习场景未验证**：所有实验均为监督学习或模仿学习，在需要在线交互和探索的强化学习设置中，运动学先验是否同样有效尚待检验。
4. **精密操作任务仍有差距**：PegInsertionSide 任务成功率仅 0.11，表明在需要亚毫米级精度的任务上，单纯的架构先验仍不足以解决根本困难，可能需要结合力反馈或更精细的感知信息。

### 补充图表

![[assets/figures/papers/paper_list_l24_https_openreview_net_forum_id_IZHk6BXBST/figures/003_Figure.jpg]]
*Figure: (a) MSE vs. backbones. Fitting forward kinematics: MSE vs. iterations (b) MSE vs. training iters*

![[assets/figures/papers/paper_list_l24_https_openreview_net_forum_id_IZHk6BXBST/figures/009_Table_4.jpg]]
*Table 4: Training hyperparameters for forward kinematics fitting experiment*

![[assets/figures/papers/paper_list_l24_https_openreview_net_forum_id_IZHk6BXBST/figures/010_Table_5.jpg]]
*Table 5: Training hyperparameters for motion prediction in Cartesian space experiment*

![[assets/figures/papers/paper_list_l24_https_openreview_net_forum_id_IZHk6BXBST/figures/011_Table_6.jpg]]
*Table 6: Training hyperparameters for imitation learning experiment (following Chi et al. (2023)’s settings)*

![[assets/figures/papers/paper_list_l24_https_openreview_net_forum_id_IZHk6BXBST/figures/012_Table_7.jpg]]
*Table 7: Demo trajectories and training iterations for each task in imitation learning experiment*

![[assets/figures/papers/paper_list_l24_https_openreview_net_forum_id_IZHk6BXBST/figures/013_Table_8.jpg]]
*Table 8: Training hyperparameters for 3D hand reconstruction experiment*

## 方法谱系与知识库定位

### 1. 核心瓶颈与设计动机

通用神经网络架构（如 MLP、GCN、Transformer）在处理铰接系统动作时缺乏对运动学结构的归纳偏置。具体而言，前向运动学本质上是沿运动链的层次化刚性变换组合，包含固定的结构参数（连杆长度、关节轴方向）和动态的关节角度变量。MLP 将这一结构化问题视为黑箱函数逼近，GCN 仅在拓扑层面传递消息，Transformer 则依赖全局注意力隐式建模——三者均未显式编码“旋转-平移”的物理约束，导致数据效率低、泛化误差大，甚至在正运动学拟合中出现非物理的连杆形变伪影（Figure 4）。

Rodrigues Network 的核心思路是将这一运动学先验“编译”进网络架构本身：**将罗德里格斯旋转公式改造为可学习的 Neural Rodrigues Operator，用可训练权重替换固定系数，并扩展为多通道高维特征算子**。这使得网络在处理关节动作时天然倾向于学习符合运动学约束的表示，而非从零开始发现旋转群的结构。

### 2. 与基线方法的关系

#### 2.1 通用架构基线

| 基线方法 | 核心差异 | Rodrigues Network 的改进 |
|---------|---------|------------------------|
| **MLP** | 全连接层堆叠，无结构先验 | 引入运动学感知的消息传递，参数效率提升约 15 倍（0.2M vs ~3M）仍大幅领先（Figure 3） |
| **GCN** (Bruna et al., 2013) | 图卷积在关节-连杆图上传递标量特征 | Rodrigues Layer 传递的是受旋转约束的 4×4 齐次变换特征，消息函数本身编码了旋转群结构 |
| **Transformer** (Vaswani et al., 2017) | 全局自注意力，无显式运动学操作 | 保留自注意力层提供全局容量，但用 Rodrigues Layer 注入局部运动学归纳偏置 |
| **Body Transformer (BoT)** (Sferrazza et al., 2024) | 面向机器人身体的 Transformer，仍以注意力为核心 | Rodrigues Network 用专用的运动学算子替代隐式注意力建模，在正运动学拟合中误差显著更低 |

在笛卡尔运动预测任务中，Rodrigues Network 的测试 MSE 为 1.93×10⁻⁶，而最强基线 Transformer 的训练 MSE 已达 12.86×10⁻⁶（Table 1）——RodriNet 的测试误差比所有基线的训练误差还低一个数量级，表明归纳偏置带来的泛化增益远超容量优势。

#### 2.2 应用框架集成

- **Diffusion Policy 集成**：Rodrigues Network 替换了 **UNet-DP** (Chi et al., 2023) 和 **Transformer-DP** (Chi et al., 2023) 中的去噪网络。在 ManiSkill 五个操作任务上，Rodrigues-DP 的平均成功率达 0.61，显著高于 Transformer-DP 的 ~0.47（Table 2）。这表明运动学先验在需要理解关节约束的模仿学习任务中具有跨架构的通用价值。

- **手部重建集成**：Rodrigues Network 替换了 **HaMeR** (Pavlakos et al., 2024) 中的标准 Transformer 回归头，结合 ViT 编码器在 FreiHAND 上达到 PA-MPJPE 5.9 mm，超越先前最优方法（Table 3）。这证明运动学先验不仅适用于机器人领域，对手部这种高度铰接的生物运动学结构同样有效。

### 3. 方法谱系定位

Rodrigues Network 处于**结构化神经网络**和**物理信息深度学习**的交汇点：

- **结构化网络谱系**：不同于 GCN 的通用图消息传递或 Transformer 的全局注意力，Rodrigues Network 的消息函数（Neural Rodrigues Operator）本身编码了旋转群的代数结构。这与 SE(3)-等变网络共享“将对称性嵌入架构”的理念，但 Rodrigues Network 关注的是运动学链的层次化组合约束，而非全局等变性。

- **物理信息学习谱系**：不同于在损失函数中添加物理约束或使用物理模拟器作为可微分层，Rodrigues Network 将运动学先验直接编码为网络层的计算图结构。这使得先验在训练初期即可发挥作用（收敛速度显著更快，Figure 3b），而非作为后验正则化项。

- **可插拔性**：Rodrigues Block 被设计为模块化组件，可通过替换输入嵌入层和输出头适配不同任务（正运动学拟合、运动预测、模仿学习、手部重建），表明该架构具有作为通用动作处理骨干的潜力。

### 4. 消融实验揭示的组件贡献

消融实验（Table 11）清晰揭示了各组件的角色：

| 移除组件 | 测试 MSE (×10⁻⁶) | 退化程度 | 功能定位 |
|---------|-----------------|---------|---------|
| 完整 RodriNet | 2.56 | — | 基线 |
| 移除 Rodrigues Layer | 6.19 | **最严重** | 核心运动学归纳偏置来源，编码关节-连杆的旋转约束 |
| 移除 Joint Layer | 持续退化 | 显著 | 连杆到关节的信息回流，维持双向消息传递 |
| 移除 Self-Attention Layer | 训练误差略升，测试变化不大 | 轻微 | 主要贡献模型容量，非运动学先验的核心载体 |

这一结果表明：**Rodrigues Layer 是不可替代的运动学归纳偏置注入点**，Joint Layer 提供必要的双向信息流，而 Self-Attention Layer 的作用更接近通用的容量扩展——这验证了“用专用算子提供归纳偏置，用通用注意力提供容量”的设计哲学。

### 5. 适用边界与局限

#### 5.1 已知局限

1. **连杆几何盲区**：当前模型仅处理关节-连杆的拓扑和运动学变换，未显式编码单个连杆的几何形状（如点云、深度图）。这限制了其在需要推理连杆自身形状的任务（如避障规划、接触检测）中的适用性。

2. **旋转关节专有**：Neural Rodrigues Operator 的数学推导基于罗德里格斯旋转公式，仅适用于旋转关节（revolute joint）。对于平动关节（prismatic joint）或更复杂的混合运动学链（如并联机构、连续体机器人），当前算子无法直接推广。

3. **离线学习验证为主**：所有实验均在离线监督学习或模仿学习设定下完成。在强化学习等需要在线交互、探索-利用权衡的场景中，运动学先验是否能加速策略学习并提升最终性能尚未验证。

4. **计算效率权衡**：自定义 CUDA 算子仍处于早期阶段，相比高度优化的 cuDNN 标准算子（如卷积、注意力），训练时间较长（Table 9, Table 10）。这在实际部署中可能成为瓶颈。

#### 5.2 开放问题

- **连杆几何融合**：如何将连杆的视觉几何信息（如深度图、点云）作为额外输入引入 Rodrigues Layer，以提升 3D 场景理解能力？
- **运动学类型扩展**：Neural Rodrigues Operator 能否推广至平动关节或更复杂的混合运动学链？这可能需要重新推导消息函数的形式。
- **在线学习验证**：在强化学习设置中，运动学先验是否同样能加速策略学习并提升最终性能？
- **即插即用集成**：是否可以将 Rodrigues Block 设计为标准化的即插即用模块，方便集成到现有的大规模预训练动作模型（如 RT 系列、Octo 等）中？

## 原文 PDF

![[paperPDFs/ICLR_2026/Rodrigues_Network_for_Learning_Robot_Actions.pdf]]
