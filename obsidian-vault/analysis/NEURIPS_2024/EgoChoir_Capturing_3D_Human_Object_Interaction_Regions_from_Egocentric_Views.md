---
title: EgoChoir Capturing 3D Human Object Interaction Regions from Egocentric Views
type: paper
paper_level: A
venue: NEURIPS
year: 2024
pdf_ref: paperPDFs/NEURIPS_2024/EgoChoir_Capturing_3D_Human_Object_Interaction_Regions_from_Egocentric_Views.pdf
project_link: https://yyvhang.github.io/EgoChoir
code_link: null
aliases:
- EC3HOIRFEV
tags:
- NEURIPS_2024
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
core_operator: 通过协调视觉外观、头部运动和3D物体几何信息，挖掘物体交互概念与主体意图，并利用可学习的调制令牌动态调整不同交互线索的梯度，使模型适应多样化的第一人称交互场景。
primary_logic: 借鉴人类认知机制：即使交互部位不可见，人类通过视觉皮层、小脑和大脑的协同，结合视觉观察、自我运动和概念理解形成“交互身体图像”，从而预构想交互区域。EgoChoir模拟这一过程，通过平行交叉注意力将物体结构、视觉外观和头部运动联系起来，并利用梯度调制自适应选择线索，从第一人称视频中联合推断3D人体接触和物体可供性。
claims:
- 仅使用视觉线索的方法（BSTRO、DECO、O2O、IAG）在第一人称视角下因观察不完整而性能不佳，LEMON虽引入几何关联但仍受限于不完整视觉观察。
- 消融实验表明移除头部运动信息 M¯ 会显著降低所有指标，证明头部运动是关键互补线索。
- 去除3D可供性特征 F_a 同样损害接触估计，说明可供性对约束接触范围、保持时间一致性至关重要。
- 梯度调制 τ 的移除导致性能下降，说明模型需要自适应地选择交互线索。
---

# EgoChoir Capturing 3D Human Object Interaction Regions from Egocentric Views

> [!tip] 核心洞察
> 借鉴人类认知机制：即使交互部位不可见，人类通过视觉皮层、小脑和大脑的协同，结合视觉观察、自我运动和概念理解形成“交互身体图像”，从而预构想交互区域。EgoChoir模拟这一过程，通过平行交叉注意力将物体结构、视觉外观和头部运动联系起来，并利用梯度调制自适应选择线索，从第一人称视频中联合推断3D人体接触和物体可供性。

| 字段 | 内容 |
|------|------|
| 中文题名 | EgoChoir：从第一人称视角捕获3D人-物交互区域 |
| 英文题名 | EgoChoir Capturing 3D Human Object Interaction Regions from Egocentric Views |
| 会议/期刊 | NEURIPS 2024 |
| Links | [Project](https://yyvhang.github.io/EgoChoir) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction |
| Method | EgoChoir |
| Dataset | Ego-Exo4D + GIMO |

> [!tip] 效果简介
> - Ego-Exo4D + GIMO (自标注数据集) 上，Precision (human contact) 0.79 vs 0.65 (LEMON) (+0.14)；Recall (human contact) 0.76 vs 0.70 (LEMON) (+0.06)；F1 (human contact) 0.77 vs 0.67 (LEMON) (+0.10)。

## 概要

### 问题瓶颈

从第一人称（egocentric）视角捕获3D人-物交互区域面临一个根本性瓶颈：交互双方——人体与物体——的视觉观察天然不完整。头戴设备只能捕捉有限的视野，交互部位往往被遮挡或处于视野之外，导致依赖完整视觉外观的现有方法无法有效建模交互区域，视觉观察与交互内容之间存在显著的歧义。

### 核心洞察

EgoChoir 借鉴人类认知机制来突破这一瓶颈。人类即使看不到自己的交互部位，也能通过视觉皮层、小脑和大脑的协同，综合视觉观察、自我运动和概念理解，在大脑中形成“交互身体图像”，从而预构想交互区域。EgoChoir 模拟这一过程：通过平行交叉注意力将物体结构、视觉外观和头部运动联系起来，并利用梯度调制自适应选择线索，从第一人称视频中联合推断3D人体接触和物体可供性。

### 方法定位

EgoChoir 以第一人称视频剪辑 $\mathcal{V}$、头部运动序列 $\mathcal{M}$ 和物体点云 $\mathcal{O}$ 为输入，输出时序密集的人体接触 $\phi_c \in \mathbb{R}^{T \times 6890 \times 2}$、逐点物体可供性 $\phi_a \in \mathbb{R}^{N \times 1}$ 和交互类别 $\phi_s$。与仅依赖视觉线索的方法（BSTRO、DECO）或引入几何关联但仍受限于不完整视觉观察的方法（LEMON）相比，EgoChoir 的核心差异在于：

- **多模态线索协同**：协调视觉外观、头部运动和3D物体几何信息，挖掘物体交互概念与主体意图。
- **可供性驱动接触建模**：先通过物体几何特征与语义令牌共同查询视觉和运动线索提取可供性特征，再以可供性特征约束人体接触的范围和时间一致性。
- **梯度调制自适应**：引入可学习的调制令牌 $\tau$，按场景动态缩放平行交叉注意力的特征值，使模型在不同交互场景下自适应地依赖不同线索。

### 主要结果

在 Ego-Exo4D 和 GIMO 联合构建的自标注数据集上，EgoChoir 全面超越现有基线方法：

- **人体接触估计**：F1 达到 0.77，较 LEMON 提升 0.10；几何误差降至 12.62 cm，降低 8.81 cm。
- **物体可供性估计**：AUC 达到 78.02，aIOU 达到 14.94，SIM 达到 0.436，分别较 LEMON 提升 2.05、2.63 和 0.026。

消融实验验证了各组件的关键作用：移除头部运动信息导致 Precision 下降 0.10、几何误差增加 7.24 cm；去除3D可供性特征使 Recall 下降 0.12、F1 下降 0.10；取消梯度调制使 F1 从 0.76 降至 0.73。这些结果表明，EgoChoir 通过模拟人类认知中的多线索协同与自适应机制，有效缓解了第一人称视角下视觉观察不完整的核心瓶颈。

### 第一人称交互区域感知的瓶颈

在 AR/VR、具身智能等应用中，从第一人称（egocentric）视角理解人-物交互至关重要。然而，第一人称视角存在一个根本性瓶颈：**交互双方（人体与物体）的视觉观察天然不完整**。佩戴头戴设备的用户只能看到物体的局部和自身身体的有限区域，而交互的关键接触部位往往处于视野之外。现有方法（如 BSTRO、DECO、O2O-Afford、IAG-Net）主要依赖完整的视觉外观来建模交互区域，在第一人称视角下因观察缺失而性能不佳。LEMON 虽然引入了几何关联，但仍受限于不完整的视觉观察，无法从根本上解决视觉观察与交互内容之间的歧义。

### 从人类认知机制中获取灵感

EgoChoir 的核心洞察来自人类自身的认知机制：即使交互部位不可见，人类仍能通过**视觉皮层、小脑和大脑的协同**，综合视觉观察、自我运动和概念理解，形成“交互身体图像”（interaction body image），从而预构想交互区域。这一过程并不要求看到完整的接触面——人类通过物体结构所暗示的功能概念（“这个把手意味着抓握”），结合头部运动所传达的主体意图（“我正靠近并转向该物体”），就能推断出即将发生的交互区域。

EgoChoir 模拟这一认知过程，从第一人称视频中**联合推断 3D 人体接触（human contact）和物体可供性（object affordance）**。其核心设计在于：通过平行交叉注意力将物体结构、视觉外观和头部运动三股信息流联系起来，并利用梯度调制机制自适应选择线索，使模型适应多样化的第一人称交互场景。

### 现有方法的缺口

- **输入模态单一**：多数方法仅依赖视觉图像，未利用头部运动这一第一人称视角天然可得的互补信号。
- **可供性与接触建模割裂**：接触估计与可供性估计通常独立进行，或仅做浅层几何关联，未形成双向约束——可供性应约束接触的空间范围，接触应反映可供性的功能语义。
- **缺乏自适应机制**：不同交互场景下，视觉、运动、几何线索的重要性不同（例如，抓握小物体时头部运动更关键，而使用大型家具时视觉外观更可靠），现有方法缺乏动态调节线索权重的机制。

### 本文动机与贡献

EgoChoir 旨在突破上述瓶颈，核心动机可概括为：

1. **引入头部运动作为互补线索**：头部运动蕴含主体的注意力方向和交互意图，是视觉观察之外的关键信息源。
2. **建立可供性与接触的双向建模**：让物体可供性约束人体接触的预测范围，同时让人体接触反过来验证可供性的功能语义，形成闭环推理。
3. **实现梯度层面的自适应线索选择**：通过可学习的调制令牌动态缩放不同线索的梯度，使模型在不同场景下自动决定“该听谁的”。

如图 Figure 1 所示，EgoChoir 以第一人称视频帧、头部运动序列和 3D 物体点云为输入，输出时序密集的 3D 人体接触、逐点物体可供性以及交互类别。Figure 2 则从概念层面阐释了主体意图与物体交互概念如何共同预构建“交互身体图像”，为后续的方法设计提供了认知科学层面的依据。

## 核心方法与创新机理

### 从“视觉主导”到“多线索协同”的范式转换

现有方法在估计人-物交互区域时，高度依赖完整的视觉外观信息。**BSTRO** 和 **DECO** 直接由图像回归人体接触，**O2O-Afford** 和 **IAG-Net** 则从视觉输入推断物体可供性。**LEMON** 虽然引入了物体几何与视觉特征的关联，但其核心仍受限于视觉观察的完整性。在第一人称视角下，交互双方（人手/身体与物体）往往只有局部可见，视觉观察与交互内容之间存在根本性歧义——这正是本任务的核心瓶颈。

EgoChoir 的关键创新在于将建模路径从“视觉→交互”转换为“视觉+头部运动+物体几何→交互概念→交互区域”。这一转换的认知依据是：人类即使看不到交互部位，也能通过视觉皮层、小脑和大脑的协同，结合视觉观察、自我运动和概念理解，预构想“交互身体图像”（Figure 2）。EgoChoir 在计算层面模拟了这一机制，具体体现在以下三个 **changed slots** 上。

### 创新一：头部运动作为互补线索的引入与预训练对齐

**Slot: 输入模态**。基线方法仅依赖视觉图像（或视觉+物体几何），EgoChoir 首次将头部运动序列 $\mathcal{M}$ 作为显式输入模态。这一设计的动机在于：第一人称视频中的头部运动承载了主体的意图信号——例如，头部的左右转动往往暗示了交互手的切换（Figure 8b）。

为保证运动特征与视觉特征在语义空间中对齐，EgoChoir 设计了一个预训练阶段：通过最小化运动特征差异与视觉特征差异之间的 KL 散度（Eq. 1），使运动编码器学会从头部姿态变化中提取与视觉变化一致的表征。消融实验（Table 2, ✗ $\bar{\mathcal{M}}$）提供了决定性证据：移除头部运动后，Precision 从 0.78 降至 0.68，F1 从 0.76 降至 0.69，geo error 增加 7.24 cm，证实头部运动是不可替代的互补线索。

### 创新二：可供性与接触的双向协同建模

**Slot: 接触建模方式**。基线方法（BSTRO、DECO）独立估计人体接触，未利用物体可供性信息；LEMON 虽联合建模，但可供性与接触之间缺乏显式的信息流动。EgoChoir 引入了一个双向协同架构：

- **物体交互概念建模**（$\Theta_a$）：语义令牌 $\mathbf{T}_f$ 与物体几何特征 $\mathbf{F}_{\mathcal{O}}$ 拼接作为查询，在调制令牌控制下通过平行交叉注意力查询视觉和运动特征，生成可供性特征 $\bar{\mathbf{F}}_a$ 和功能语义特征 $\mathbf{F}_s$。
- **主体意图建模**（$\Theta_c$）：意图令牌 $\mathbf{T}_i$ 与视觉特征拼接作为查询，以可供性特征 $\mathbf{F}_a$ 和运动特征作为键值，通过平行交叉注意力生成接触特征 $\bar{\mathbf{F}}_c$。

这一设计的因果机制在于：可供性特征 $\mathbf{F}_a$ 为接触估计提供了空间先验——物体上哪些区域“可以被交互”，从而约束接触预测的范围并保持时间一致性。消融实验（Table 2, ✗ $\mathbf{F}_a$）证实：移除可供性特征后，Recall 下降 0.12，F1 下降 0.10；定性结果（Figure 7b）进一步显示，缺乏可供性约束会导致接触的过预测与时间不一致。

### 创新三：梯度调制实现自适应线索选择

**Slot: 多模态自适应机制**。基线方法对不同线索采用统一加权或无自适应机制，无法应对第一人称视角下场景的多样性——有些场景视觉信息丰富，有些则高度依赖运动线索。EgoChoir 引入可学习的调制令牌 $\tau_v, \tau_m, \tau_o$，通过缩放平行交叉注意力的输入特征值，动态调整特定层在反向传播中的梯度：

$$\theta_{t+1} = \theta_t - \eta \cdot \kappa \cdot \frac{\partial \mathcal{L}}{\partial \theta_t}, \quad \kappa = \sigma\left(\frac{f_1(x_1)}{f_2(x_2)}\right)$$

这一机制使模型能够在不同交互场景下自适应地依赖不同线索。Figure 7c 可视化了不同交互类型下各线索映射层的梯度差异，验证了自适应调制的有效性。消融实验（Table 2, ✗ $\tau$）表明，移除梯度调制后 F1 从 0.76 降至 0.73，Precision 从 0.78 降至 0.75，证明自适应线索选择对性能有实质贡献。

### 创新总结

三个 changed slots 构成了一个递进的创新链条：**头部运动**提供了视觉之外的第二信号通道，**双向协同架构**建立了可供性与接触之间的因果约束，**梯度调制**使模型能在不同场景下灵活权衡各线索的贡献。这一组合使 EgoChoir 在人体接触 F1 上超越 LEMON 10 个百分点（0.77 vs 0.67），在几何误差上降低 8.81 cm（12.62 vs 21.43），且这一优势是在输入限制更严格（仅头部运动 vs LEMON 需外源性人体姿态）的条件下取得的。

EgoChoir 的整体 pipeline 围绕“从第一人称视角联合推断 3D 人体接触与物体可供性”这一核心任务构建，其设计动机源于一个关键瓶颈：**第一人称视角下交互双方（人、物）的视觉观察天然不完整，导致单纯依赖视觉外观的方法无法有效建模交互区域**。为解决这一问题，EgoChoir 模拟人类认知中“交互身体图像”的预构想机制——通过协调视觉皮层、小脑和大脑的协同，将视觉观察、自我运动和概念理解融合，从而推断不可见部位的交互区域。

### 输入输出定义

模型的形式化定义为：

$$\phi_c, \phi_a, \phi_s = f(\mathcal{V}, \mathcal{M}, \mathcal{O})$$

其中输入包括：
- $\mathcal{V}$：第一人称视频片段
- $\mathcal{M}$：同步的头部运动序列（由头戴设备的位姿数据获得）
- $\mathcal{O}$：交互物体的 3D 点云

输出包括三个互补的交互表征：
- $\phi_c \in \mathbb{R}^{T \times 6890 \times 2}$：时序密集人体接触（SMPL 顶点上的逐帧二分类标签）
- $\phi_a \in \mathbb{R}^{N \times 1}$：3D 物体可供性（物体点云上的逐点交互概率）
- $\phi_s$：交互类别

### 模块化 Pipeline

EgoChoir 由五个功能模块串联而成，各模块之间存在明确的信息流与约束关系：

**1. 模态特征提取（Modality-wise Feature Extraction）**

三条并行的特征提取支路分别处理视觉、运动和几何信息：
- **视觉特征**：使用 HRNet 提取逐帧图像特征，再通过联合时空注意力（joint space-time attention）融合为视频级特征 $\mathbf{F}_{\mathcal{V}}$
- **运动特征**：通过 MLP 编码头部运动序列得到 $\mathbf{F}_{\mathcal{M}}$。该编码器通过一个预训练损失进行对齐——最小化运动特征差异与视觉特征差异之间的 KL 散度，使外观变化隐含地传递到运动特征中
- **几何特征**：使用 DGCNN 从物体点云中提取 $\mathbf{F}_{\mathcal{O}}$

**2. 物体交互概念建模（Object Interaction Concept Modeling, $\Theta_a$）**

该模块以语义令牌（semantic tokens）与物体几何特征的拼接作为查询（query），以经调制令牌缩放后的视觉特征和运动特征作为键值（key-value），通过平行交叉注意力（parallel cross-attention）生成可供性特征 $\bar{\mathbf{F}}_a$ 和功能语义特征：

$$\bar{\mathbf{F}}_a = \Theta_a(\Gamma[\mathbf{T}_f, \mathbf{F}_{\mathcal{O}}], \tau_v \cdot \mathbf{F}_{\mathcal{V}}, \tau_m \cdot \mathbf{F}_{\mathcal{M}})$$

**3. 主体交互意图建模（Subject Interaction Intention Modeling, $\Theta_c$）**

该模块以意图令牌（intention tokens）与视觉特征的拼接作为查询，以经调制缩放后的 3D 可供性特征和运动特征作为键值，通过平行交叉注意力生成接触特征 $\bar{\mathbf{F}}_c$ 和意图语义特征。此处引入了时间位置编码 $pe_t$ 以保持时序一致性：

$$\bar{\mathbf{F}}_c = \Theta_c(\Gamma[\mathbf{T}_i, \mathbf{F}_{\mathcal{V}} + pe_t], \tau_o \cdot \mathbf{F}_a, \tau_m \cdot (\mathbf{F}_{\mathcal{M}} + pe_t))$$

**4. 梯度调制（Gradient Modulation）**

可学习的调制令牌 $\tau$ 通过缩放平行交叉注意力的输入特征值，动态调整特定层中不同交互线索（视觉、运动、可供性）的梯度贡献。这使得模型在不同交互场景下能够自适应地依赖最可靠的线索，而非对所有场景采用统一的加权策略。

**5. 解码器（Decoders）**

三个解码器分别将中间特征映射为最终输出：
- 功能语义与意图语义融合后预测交互类别 $\phi_s$
- 可供性特征解码为逐点可供性 $\phi_a$
- 接触特征先后经过特征维度和空间维度的解耦，输出时序密集接触 $\phi_c$

### 训练目标

整体损失函数为三项损失的加权组合：

$$\mathcal{L} = \mathcal{L}_a + \mathcal{L}_c + \mathcal{L}_s$$

其中 $\mathcal{L}_s$ 为交互语义的交叉熵损失，$\mathcal{L}_a$ 和 $\mathcal{L}_c$ 均为 Dice 损失与 Focal 损失的组合，分别优化可供性和接触估计。

### 信息流与约束关系

pipeline 中存在两条关键的信息依赖路径：
- **自上而下的约束**：物体可供性特征 $\mathbf{F}_a$ 作为接触建模 $\Theta_c$ 的输入，为接触估计提供空间先验，约束接触范围并保持时间一致性
- **自下而上的协同**：交互语义特征 $\mathbf{F}_s$ 与区域性交叉注意力 $f_{ca}$ 共同维护交互双方的语义和区域协同

消融实验验证了这些依赖关系的必要性：移除 3D 可供性特征 $\mathbf{F}_a$ 导致接触 F1 从 0.76 降至 0.66，并出现过度预测和时间不一致现象（Figure 7b）；移除语义特征 $\mathbf{F}_s$ 或区域性交叉注意力 $f_{ca}$ 同样造成性能下降（Table 2）。

### 补充图表

![[assets/figures/papers/paper_list_l1791_EgoChoir_Capturing_3D_Human_Object_Interaction_Regions_from_Egocentric_V/figures/003_Figure_3.jpg]]
*Figure 3: Method. EgoChoir first employs modality-wise encoders to extract features, in which the motion encoder is pre-trained by minimizing the distance between visual disparity and motion disparity. Then, it takes them to excavate the object interaction concept and subject intention, modeling the affordance and contact through parallel cross-attention with gradient modulation*

![[assets/figures/papers/paper_list_l1791_EgoChoir_Capturing_3D_Human_Object_Interaction_Regions_from_Egocentric_V/figures/001_Figure_1.jpg]]
*Figure 1: EgoChoir takes egocentric frames and head motion from head-mounted devices, along with the 3D object, to capture 3D interaction regions, including human contact and object affordance. The human motion is just visualized for intuitive observation of contact, yet it is not utilized by EgoChoir*

EgoChoir 的核心架构围绕“物体交互概念挖掘 → 主体交互意图建模 → 梯度自适应调制”三条主线展开，通过平行交叉注意力（Parallel Cross-Attention）将物体几何、视觉外观和头部运动三类异质线索协调融合，最终联合输出 3D 人体接触与物体可供性。

### 3.1 问题形式化

给定第一人称视频片段 $\mathcal{V}$、头部运动序列 $\mathcal{M}$ 和物体点云 $\mathcal{O}$，模型 $f$ 输出三个目标：

$$\phi_c, \phi_a, \phi_s = f(\mathcal{V}, \mathcal{M}, \mathcal{O})$$

其中 $\phi_c \in \mathbb{R}^{T \times 6890 \times 2}$ 为时序密集人体接触（SMPL 顶点级二分类），$\phi_a \in \mathbb{R}^{N \times 1}$ 为逐点物体可供性概率，$\phi_s$ 为交互类别。该形式化将三个输出统一在同一推理框架下，为后续多线索协同建模奠定基础。

### 3.2 模态特征提取

**视觉特征**：采用 HRNet 逐帧提取空间特征，再通过联合时空注意力（joint space-time attention）建模时序上下文，得到视频特征 $\mathbf{F}_{\mathcal{V}} \in \mathbb{R}^{T H_1 W_1 \times C}$。

**运动特征**：头部运动序列经 MLP 编码为 $\mathbf{F}_{\mathcal{M}}$。为使运动特征与视觉特征在语义空间对齐，引入视觉-运动差异约束预训练——最小化运动特征差异与视觉特征差异之间的 KL 散度：

$$\mathcal{L}_m = \left\| \sum_C \mathbf{F}_{\mathcal{M}}^i \log(\epsilon + \frac{\mathbf{F}_{\mathcal{M}}^i}{\epsilon + \mathbf{F}_{\mathcal{M}}^j}) - \sum_{H_1W_1} \sum_C \mathbf{F}_{\mathcal{V}}^i \log(\epsilon + \frac{\mathbf{F}_{\mathcal{V}}^i}{\epsilon + \mathbf{F}_{\mathcal{V}}^j}) \right\|_2$$

该约束使得外观变化模式适度传递至运动特征空间，为后续交叉注意力提供语义一致的键值对。

**物体几何特征**：通过 DGCNN 从物体点云提取局部几何结构特征 $\mathbf{F}_{\mathcal{O}}$，捕捉物体形状信息以支撑可供性推理。

### 3.3 平行交叉注意力建模

EgoChoir 的核心推理由两个对称的 Transformer 模块 $\Theta_a$ 和 $\Theta_c$ 完成，二者均采用平行交叉注意力，但查询（Query）和键值（Key-Value）的来源不同，体现了“物体概念→可供性→接触”的因果链条。

**物体交互概念建模（$\Theta_a$）**：语义令牌 $\mathbf{T}_f$ 与物体几何特征 $\mathbf{F}_{\mathcal{O}}$ 拼接作为查询，经调制令牌 $\tau_v, \tau_m$ 缩放后的视觉特征和运动特征作为键值：

$$\bar{\mathbf{F}}_a = \Theta_a(\Gamma[\mathbf{T}_f, \mathbf{F}_{\mathcal{O}}], \tau_v \cdot \mathbf{F}_{\mathcal{V}}, \tau_m \cdot \mathbf{F}_{\mathcal{M}})$$

输出 $\bar{\mathbf{F}}_a$ 包含可供性特征和功能语义特征 $\mathbf{F}_s$。这里物体结构提供“这个物体能做什么”的先验，视觉和运动线索补充“当前场景下正在发生什么”的上下文。

**主体交互意图建模（$\Theta_c$）**：意图令牌 $\mathbf{T}_i$ 与带时间位置编码的视觉特征 $\mathbf{F}_{\mathcal{V}} + pe_t$ 拼接作为查询，调制缩放后的 3D 可供性特征 $\mathbf{F}_a$ 和运动特征 $\mathbf{F}_{\mathcal{M}} + pe_t$ 作为键值：

$$\bar{\mathbf{F}}_c = \Theta_c(\Gamma[\mathbf{T}_i, \mathbf{F}_{\mathcal{V}} + pe_t], \tau_o \cdot \mathbf{F}_a, \tau_m \cdot (\mathbf{F}_{\mathcal{M}} + pe_t))$$

输出 $\bar{\mathbf{F}}_c$ 包含接触特征和意图语义特征。关键设计在于：可供性特征 $\mathbf{F}_a$ 在此作为键值约束接触范围——物体哪些区域可交互，直接限定了人体接触的空间分布，消融实验（Table 2: ✗ $\mathbf{F}_a$）证实移除该约束导致 Recall 下降 0.12、F1 下降 0.10，并出现过度预测与时间不一致（Figure 7b）。

### 3.4 梯度调制机制

不同第一人称交互场景对视觉、运动、几何线索的依赖程度差异显著（如“切菜”依赖物体功能语义，“转头取物”依赖头部运动）。EgoChoir 通过可学习的调制令牌 $\tau = \{\tau_v, \tau_m, \tau_o\}$ 缩放平行交叉注意力的输入特征值，从而动态调节各线索对应层的梯度：

$$\theta_{t+1} = \theta_t - \eta \cdot \kappa \cdot \frac{\partial \mathcal{L}}{\partial \theta_t}, \quad \kappa = \sigma\left(\frac{f_1(x_1)}{f_2(x_2)}\right)$$

其中 $\kappa$ 由模态特征的对数比率经 sigmoid 计算，实现对特定层梯度的自适应缩放。消融实验（Table 2: ✗ $\tau$）表明移除梯度调制后 F1 从 0.76 降至 0.73，Figure 7c 可视化了不同交互场景下各线索层的梯度差异，验证了自适应选择的必要性。

### 3.5 解码与损失函数

**解码器**：功能语义与意图语义融合后预测交互类别 $\phi_s$；可供性特征解码为逐点可供性 $\phi_a$；接触特征先后解耦特征维度和空间维度，输出时序密集接触 $\phi_c$。

**整体损失**：

$$\mathcal{L} = \mathcal{L}_a + \mathcal{L}_c + \mathcal{L}_s$$

其中 $\mathcal{L}_s$ 为交互语义交叉熵损失，$\mathcal{L}_a$ 和 $\mathcal{L}_c$ 均为 Dice 损失与 Focal 损失的组合（$\alpha=0.25, \gamma=2$），精确表达式见论文 Eq. (5)。该组合损失在正负样本极度不均衡的接触/可供性预测中有效缓解类别不平衡问题。

### 补充图表

![[assets/figures/papers/paper_list_l1791_EgoChoir_Capturing_3D_Human_Object_Interaction_Regions_from_Egocentric_V/figures/002_Figure_2.jpg]]
*Figure 2: The subject intention, conveyed through synergistic visual appearances and head movements, along with the object interaction concept revealed by its structure and functionality, pre-formulate an interaction body image, which enables interaction regions to be envisioned*

## 实验与关键发现

### 主实验结果

EgoChoir 在人体接触与物体可供性两项任务上均全面超越现有基线方法，验证了多线索协同建模的有效性。Table 1 汇总了主要定量结果。

![[assets/figures/papers/paper_list_l1791_EgoChoir_Capturing_3D_Human_Object_Interaction_Regions_from_Egocentric_V/figures/004_Table_1.jpg]]
*Table 1: Quantitative Results. Metrics of baselines and ours on human contact and object affordance. The best results are covered with the mask, ⋄ indicates the relative improvement to the first row*

在人体接触估计上，EgoChoir 的 Precision 达到 **0.79**，Recall **0.76**，F1 **0.77**，几何误差 **12.62 cm**。相比最强基线 **LEMON**（Precision 0.65，Recall 0.70，F1 0.67，geo. 21.43 cm），F1 提升 **+0.10**，几何误差降低 **8.81 cm**。值得注意的是，LEMON 需要额外输入由 SMPLer‑X 从 exocentric 视角估计的人体姿态，这为其提供了更丰富的动作先验；而 EgoChoir 仅使用头部运动数据，输入约束更严格，却取得了显著更好的结果。

仅依赖视觉线索的方法（**BSTRO**、**DECO**、**O2O‑Afford**、**IAG‑Net**）在第一人称视角下性能明显不足：由于交互部位常被遮挡或不在视野内，这些方法无法可靠地推断接触区域。LEMON 虽然引入了几何关联，但其核心仍受限于不完整的视觉观察，未能从根本上解决视觉歧义问题。

在物体可供性估计上，EgoChoir 同样取得最优：AUC **78.02**，aIOU **14.94**，SIM **0.436**。相比 LEMON（AUC 75.97，aIOU 12.31，SIM 0.410），三项指标分别提升 **+2.05**、**+2.63**、**+0.026**。这表明通过物体几何结构与交互语义的联合挖掘，模型能更准确地定位物体上与交互相关的功能区域。

### 消融实验

Table 2 的系统消融揭示了各组件的因果贡献，Figure 7 提供了定性佐证。

![[assets/figures/papers/paper_list_l1791_EgoChoir_Capturing_3D_Human_Object_Interaction_Regions_from_Egocentric_V/figures/008_Table_2.jpg]]
*Table 2: Quantitative Ablations. Metrics when detaching the head motion*

![[assets/figures/papers/paper_list_l1791_EgoChoir_Capturing_3D_Human_Object_Interaction_Regions_from_Egocentric_V/figures/009_Figure_7.jpg]]
*Figure 7: Qualitative Ablations. (a) Results of the human contact and object affordance*

**头部运动线索（M̄）是关键互补信息源。** 移除头部运动后，Precision 从 0.78 降至 **0.68**（‑0.10），F1 从 0.76 降至 **0.69**（‑0.07），几何误差从 12.62 cm 增至 **19.86 cm**（+7.24 cm）。Figure 7(a) 的定性对比显示，缺少头部运动时模型难以区分方向性接触（如左手握 vs 右手握），验证了头部运动在消解视觉歧义中的核心作用。

**3D 可供性特征（Fₐ）对接触建模构成强约束。** 移除 Θ_c 中的可供性特征后，Recall 从 0.76 降至 **0.64**（‑0.12），F1 从 0.76 降至 **0.66**（‑0.10）。Figure 7(b) 显示，缺少可供性约束时接触预测出现严重过预测和时间不一致——模型倾向于在物体表面大范围预测接触，且相邻帧的预测缺乏连贯性。这证实了可供性信息在空间范围约束和时间一致性维持上的关键作用。

**梯度调制（τ）赋予模型自适应线索选择能力。** 取消梯度调制后，F1 从 0.76 降至 **0.73**，Precision 降至 **0.75**。Figure 7(c) 可视化了不同交互场景下各层映射不同线索的梯度差异：例如在“切菜”场景中，视觉线索的梯度响应更强；而在“推物体”场景中，运动线索占主导。梯度调制使模型能根据交互类型动态调整对视觉、运动和可供性线索的依赖权重，这是 EgoChoir 跨场景泛化的关键机制。

**语义特征（Fₛ）与区域性交叉注意力（f_cₐ）** 的移除同样导致性能下降，说明交互双方的语义协同和区域级特征对齐对于精确估计交互区域不可或缺。

**时间位置编码（pe_t）** 的移除降低了 Precision 和 aIOU，表明时序信息有助于抑制假阳性预测，提升接触定位的帧间一致性。

**视频骨干选择的影响：** 使用 SlowFast 或 Lavila 等预训练视频骨干替代逐帧 HRNet + 时空注意力的方案，性能反而下降，且可能产生时序不一致的预测。Figure 10 展示了一个典型失败案例：使用 Lavila 骨干时，接触在实际发生之前就被预测出来。这说明针对本任务设计的轻量时空注意力比通用视频理解模型更适配。

### 全身运动与扩展分析

Table 3 显示，将头部运动替换为全身运动可进一步提升性能：Precision **0.80**，F1 **0.79**，几何误差 **11.24 cm**。这暗示了更完整的运动信息对交互区域估计的潜在增益，但也表明仅头部运动已能提供足够强的先验。

![[assets/figures/papers/paper_list_l1791_EgoChoir_Capturing_3D_Human_Object_Interaction_Regions_from_Egocentric_V/figures/011_Table_3.jpg]]
*Table 3: Metrics when using whole-body motion*

### 失败模式与局限性

1. **未见交互的混淆预测**：当前模型在训练分布外的交互类型上可能出现混淆，需要结合 3D 场景条件和全身运动估计来增强空间约束。
2. **依赖预定义交互类别**：模型无法处理开放词汇量的新交互，限制了其在开放世界场景中的适用性。
3. **摄像头运动泛化未验证**：实验仅在固定头戴设备数据上进行，摄像头运动模式变化对模型的影响尚不明确。
4. **时序错误预测**：使用某些视频骨干（如 Lavila）时，接触可能在交互实际发生前被预测，表明时序建模仍有改进空间。

### 公平性说明

EgoChoir 与基线的对比在以下方面保持了公平性：数据集训练/测试划分保证场景几乎不重叠，泛化性评估可靠；LEMON 基线实际享有更丰富的输入信息（exocentric 估计的人体姿态），而 EgoChoir 仅使用头部运动；部分基线依赖场景分割图等额外模块，EgoChoir 不需要此类预处理。

### 补充图表

![[assets/figures/papers/paper_list_l1791_EgoChoir_Capturing_3D_Human_Object_Interaction_Regions_from_Egocentric_V/figures/007_Figure_6.jpg]]
*Figure 6: Qualitative Results. Contact vertices are colored yellow, and 3D object affordance are colored red, with the depth of red representing the affordance probability. Note: for intuitive visualization, the contact GT of body interactions are visualized on posed humans (last row) from GIMO [113]. Please zoom in for a better visualization and refer to the Sup. Mat. for video results*

![[assets/figures/papers/paper_list_l1791_EgoChoir_Capturing_3D_Human_Object_Interaction_Regions_from_Egocentric_V/figures/010_Figure_8.jpg]]
*Figure 8: Analysis. (a) The changing interaction contents correspond to dynamic 3D object affordances*

![[assets/figures/papers/paper_list_l1791_EgoChoir_Capturing_3D_Human_Object_Interaction_Regions_from_Egocentric_V/figures/013_Table_5.jpg]]
*Table 5: Metrics of LEMON and our method for each interaction category. Prec. indicates Precision, wrap. is wrapgrasp*

![[assets/figures/papers/paper_list_l1791_EgoChoir_Capturing_3D_Human_Object_Interaction_Regions_from_Egocentric_V/figures/012_Table_4.jpg]]
*Table 4: The collected 12 different interactions with 18 different objects. Obj. indicates objects, Int. denotes interactions, wrap. is wrapgrasp and Refrige. is Refrigerator*

## 定位与知识库关联

### 1. 任务定位与基线谱系

EgoChoir 瞄准的是**第一人称视角下的 3D 人-物交互区域联合估计**，输出包括时序密集人体接触（3D human contact）与逐点物体可供性（3D object affordance）。在 EgoChoir 之前，该方向的方法可大致分为两条独立线索：

**人体接触估计线**：
- **BSTRO**：直接从视觉图像估计 3D 人体接触，依赖完整的视觉外观观察。
- **DECO**：同样基于视觉输入，额外依赖场景分割图作为先验。

**物体可供性估计线**：
- **O2O-Afford**：估计 3D 物体可供性。
- **IAG-Net**：估计 3D 物体可供性。

**联合估计线**：
- **LEMON**：首次尝试联合估计人体接触与物体可供性，引入了物体几何与视觉特征的关联。但其核心仍依赖从 exocentric 视角估计的人体姿态（由 SMPLer-X 提供），这为其注入了额外的动作信息，且本质上仍受限于不完整的视觉观察。

EgoChoir 的核心差异化在于：**仅使用第一人称视觉帧、头部运动序列和 3D 物体点云三种模态**，不依赖 exocentric 姿态估计或场景分割图，输入约束更为严格。Table 1 的定量对比表明，EgoChoir 在人体接触指标上全面超越 LEMON（F1: 0.77 vs 0.67，geo error: 12.62 cm vs 21.43 cm），在物体可供性上也取得一致提升（AUC: 78.02 vs 75.97，aIOU: 14.94 vs 12.31）。

### 2. 核心机制演进：从独立估计到认知启发的协同推理

EgoChoir 的方法设计体现了从“被动映射”到“主动预构想”的范式转换，其因果调节旋钮（causal knob）可拆解为三个递进的机制创新：

**（1）多模态互补线索的引入**

基线方法（BSTRO、DECO、LEMON）的核心瓶颈在于：第一人称视角下交互双方（人手/身体与物体）的视觉观察天然不完整，视觉外观与交互内容之间存在根本性歧义。EgoChoir 通过引入**头部运动序列**和**3D 物体几何**作为互补线索来打破这一瓶颈：
- 头部运动编码了主体的交互意图和自我运动信息，即使交互部位不可见，头部转动方向仍能暗示接触的左右变化（Figure 8b）。
- 3D 物体几何提供了结构化的交互概念锚点，使模型能够在物体表面推理“哪些区域可能被接触”。

消融实验（Table 2）直接验证了这一设计的必要性：移除头部运动线索 $\bar{\mathcal{M}}$ 后，Precision 从 0.78 降至 0.68，F1 从 0.76 降至 0.69，geo error 增加 7.24 cm；移除 3D 可供性特征 $\mathbf{F}_a$ 后，Recall 下降 0.12，F1 下降 0.10，且出现过度预测和时间不一致（Figure 7b）。

**（2）双向交互建模：可供性约束接触，接触反馈语义**

EgoChoir 的管道设计体现了可供性与接触之间的**因果双向约束**：
- **物体交互概念建模（$\Theta_a$）**：语义令牌与物体几何特征拼接作为查询，通过平行交叉注意力同时查询视觉特征和运动特征，生成可供性特征 $\bar{\mathbf{F}}_a$。这一步模拟了“看到物体结构 → 理解功能语义 → 预判交互区域”的认知过程。
- **主体交互意图建模（$\Theta_c$）**：意图令牌与视觉特征拼接作为查询，以可供性特征和运动特征作为键值，通过平行交叉注意力生成接触特征 $\bar{\mathbf{F}}_c$。这里的关键设计是**可供性特征作为接触建模的输入**，使得接触估计被约束在物体可供性范围内，避免在不可能的区域预测接触。

这一设计与 LEMON 的几何关联形成对比：LEMON 虽然引入了物体几何，但可供性与接触之间缺乏显式的双向约束流。EgoChoir 的消融实验（Table 2: ✗ $\mathbf{F}_a$ 行）证明，切断可供性到接触的信息流会导致显著的性能退化。

**（3）梯度调制：场景自适应的线索选择**

EgoChoir 最具特色的机制是**可学习的调制令牌 $\tau$**，它通过缩放平行交叉注意力的输入特征值来动态调整特定层的梯度。其核心洞察是：不同的第一人称交互场景对不同线索的依赖程度不同——例如，当手部完全可见时，视觉线索应占主导；当手部被遮挡时，头部运动和物体几何应获得更高权重。

梯度调制的数学本质是：

$$\theta_{t+1} = \theta_t - \eta \cdot \kappa \cdot \frac{\partial \mathcal{L}}{\partial \theta_t}, \quad \kappa = \sigma\left(\frac{f_1(x_1)}{f_2(x_2)}\right)$$

其中 $\kappa$ 由调制令牌 $\tau$ 根据当前输入自适应计算，实现对不同模态映射层梯度的动态缩放。消融实验（Table 2: ✗ $\tau$ 行）表明，移除梯度调制后 F1 从 0.76 降至 0.73，且 Figure 7c 可视化了不同交互场景下各层梯度的显著差异，验证了自适应机制的必要性。

### 3. 适用边界与局限

**已知适用条件**：
- 输入依赖固定头戴设备的视频流、头部运动序列和预先获取的 3D 物体点云。
- 交互类别限定于预定义的 12 种交互（如抓握、切割、包裹抓握等）与 18 类物体（Table 4）。
- 训练/测试数据来自 Ego-Exo4D 和 GIMO，场景几乎不重叠，具备一定的泛化性。

**已验证的局限**：
1. **交互类型覆盖不全**：当前方法尚未覆盖所有交互类型，在某些未见交互上可能产生混淆预测。
2. **闭集交互类别**：模型依赖预先标注的交互类别，无法处理开放词汇量的新交互，即不具备零样本或开放集交互区域感知能力。
3. **设备假设**：仅在固定头戴设备数据上验证，未充分考虑摄像头运动模式变化（如剧烈晃动、快速转头）带来的影响。
4. **空间约束不足**：如需估测更精确的肢体接触位置（如区分手掌与手指的具体接触点），需要结合 3D 场景条件和全身运动估计。Table 3 的实验佐证了这一点：将头部运动替换为全身运动后，Precision 提升至 0.80，F1 提升至 0.79，geo error 降至 11.24 cm。

**需要注意的公平性边界**：
- LEMON 基线使用了 exocentric 视角估计的人体姿态作为额外输入，而 EgoChoir 仅使用头部运动，输入信息量更少但性能更优，这强化了方法有效性的论证。
- 部分基线（如 DECO）依赖场景分割图，EgoChoir 不需要额外的场景解析模块，在部署友好性上具有优势。

### 4. 开放问题

1. **如何融入 3D 场景条件与全身运动估计**，以更好约束空间关系，实现更细粒度的交互区域估计（如区分手指级别的接触）？Table 3 的全身运动实验已初步验证了这条路径的潜力。

2. **能否扩展至动态场景或多物体同时交互**？当前方法假设单物体交互，但真实第一人称场景中常涉及多物体切换或双手同时操作不同物体。

3. **如何实现开放集交互区域感知**？当前方法受限于预定义的交互类别，向零样本或开放词汇量泛化需要重新设计语义令牌机制和训练范式。

4. **在缺失头部运动信息时的鲁棒性**：当头部运动数据不可用（如设备故障或隐私限制）时，模型能否退化为仅依赖视觉和物体几何的推理模式，仍需探索。

## 原文 PDF

![[paperPDFs/NEURIPS_2024/EgoChoir_Capturing_3D_Human_Object_Interaction_Regions_from_Egocentric_Views.pdf]]
