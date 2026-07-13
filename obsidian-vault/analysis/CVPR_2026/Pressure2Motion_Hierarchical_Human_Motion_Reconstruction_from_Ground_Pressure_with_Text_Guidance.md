---
title: "Pressure2Motion: Hierarchical Human Motion Reconstruction from Ground Pressure with Text Guidance"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/Pressure2Motion_Hierarchical_Human_Motion_Reconstruction_from_Ground_Pressure_with_Text_Guidance.pdf
project_link: null
code_link: null
aliases:
- Pressure2Motion
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
core_operator: 引入分层扩散模型，分别提取高层运动轨迹和底层姿态偏移作为双层次压力特征，并通过 ControlNet 与适配器进行分层注入，同时增加压力-动作一致性损失，有效约束并解析欠定问题。
primary_logic: 可将预训练的文本到动作扩散模型作为生成先验，用于从稀疏压力信号重建运动。其中，从压力数据中独立提取的高层运动轨迹和底层姿态偏移，以分层方式注入模型，使生成的动作在遵循文本语义的同时与压力信号保持物理一致性。
claims:
- Our full model achieves state-of-the-art results across reconstruction accuracy and realism.
- The hierarchical design significantly outperforms the non-hierarchical variant.
- Removing ControlNet or Adapter leads to significant performance drop.
- Text-only baseline confirms necessity of pressure, as physical realism metrics collapse.
---

# Pressure2Motion: Hierarchical Human Motion Reconstruction from Ground Pressure with Text Guidance

> [!tip] 核心洞察
> 可将预训练的文本到动作扩散模型作为生成先验，用于从稀疏压力信号重建运动。其中，从压力数据中独立提取的高层运动轨迹和底层姿态偏移，以分层方式注入模型，使生成的动作在遵循文本语义的同时与压力信号保持物理一致性。

| 字段 | 内容 |
|------|------|
| 中文题名 | Pressure2Motion：基于地面压力与文本引导的分层人体运动重建 |
| 英文题名 | Pressure2Motion: Hierarchical Human Motion Reconstruction from Ground Pressure with Text Guidance |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2511.05038) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction |
| Method | Pressure2Motion |
| Dataset | MPL |

> [!tip] 效果简介
> - MPL 上，FID↓ 0.262 vs 0.388 (MaskControl) (-0.126)；MPJPE↓ 0.1622 vs 0.1695 (MaskControl) (-0.0073)；CoP Error↓ 0.4260 vs 0.5644 (MaskControl) (-0.1384)。

## 概要

从稀疏、含噪的地面压力信号中重建全身人体运动，是一个严重欠定的跨模态映射问题：压力图仅提供足底接触的二维分布，与全身三维姿态之间缺乏直接的几何运动学对应，纯回归模型极易产生违背物理规律的“漂浮”动作。**Pressure2Motion** 针对这一瓶颈，首次将预训练的文本到动作扩散模型（MDM）作为强生成先验，并通过**分层压力特征提取与注入**机制，将压力信号解析为两个互补层次——高层运动轨迹（Pressure-Inferred Movement Trajectory）与底层姿态偏移（Pressure-Induced Posture Shifts）——分别经由 ControlNet 和 Adapter 模块注入扩散去噪过程，同时辅以压力-动作一致性损失，使生成动作在遵循文本语义的同时与压力信号保持物理对齐。

在自建的 **MPL 数据集**（约 2.3M 帧，400 个动作类别，25 名受试者）上，Pressure2Motion 在重建精度与运动真实感两个维度均达到最优：FID 降至 0.262，MPJPE 降至 0.1622，CoP Error 降至 0.4260，全面优于 MaskControl、OmniControl 等可控运动合成基线（Table 1）。消融实验证实，移除运动轨迹、姿态偏移或一致性损失中任一组件均导致性能显著退化（Table 2），而移除 ControlNet 或 Adapter 则使 FID 分别飙升至 1.3683 和 0.695（Table 3），验证了分层注入架构的必要性。该工作为“稀疏物理信号 + 语义引导”的跨模态人体重建提供了可复用的范式。

### 问题背景：从稀疏压力信号重建全身运动的欠定挑战

地面压力传感是一种极具吸引力的运动捕捉范式——传感器可嵌入地板、鞋垫或智能地毯中，无需穿戴光学标记或惯性单元，即可实现非侵入式的人体感知。然而，压力信号本身存在根本性的信息瓶颈：**单个压力帧仅提供足底与地面接触的二维受力分布，而全身运动涉及数十个关节在三维空间中的复杂运动学链**。这种从低维稀疏信号到高维稠密姿态的映射是严重欠定的——同一压力分布可能对应截然不同的上肢姿态、躯干朝向甚至下肢步态变体。

此外，真实场景下的压力数据还面临噪声干扰（传感器精度限制、鞋底变形）和时间动态模糊（压力中心漂移、接触面积变化），使得纯数据驱动的回归模型极易产生违反物理规律的动作，如足部滑移、关节穿透或重心失稳。因此，如何将稀疏、含噪的地面压力信号转化为物理合理且语义连贯的全身运动序列，构成了该任务的核心瓶颈。

### 现有方法缺口：回归模型的局限与生成先验的缺失

在 Pressure2Motion 之前，从压力信号重建人体运动的研究主要依赖两类范式：

- **纯回归方法**：直接学习压力到姿态的端到端映射。这类方法在训练数据覆盖的动作范围内可取得一定精度，但面对欠定输入时缺乏对解空间的合理约束，生成的姿态常出现高频抖动或物理不一致。
- **可控运动生成方法**：如 **OmniControl** 和 **MaskControl**，通过在预训练文本到运动扩散模型中注入空间控制信号来引导生成。然而，这些方法的设计初衷是处理相对稠密的空间约束（如关键关节位置），对极度稀疏的压力信号缺乏专门的建模机制，无法有效提取压力中蕴含的多层次运动信息。

更关键的是，现有方法均未利用**文本语义**作为辅助条件。在人类运动重建中，文本描述（如“缓慢向前行走并挥动右手”）提供了高层动作意图和风格约束，可从语义层面缩小欠定问题的解空间。然而，如何将文本引导与物理压力信号有机融合，使生成的动作既符合语义描述又与压力测量保持物理一致性，仍是一个开放问题。

### 本文动机：分层压力建模与文本引导的生成式重建

针对上述缺口，Pressure2Motion 提出了一种全新的生成范式：**将预训练的文本到运动扩散模型作为强生成先验，通过分层提取压力信号中的高层运动轨迹与底层姿态偏移，以分层控制的方式注入扩散生成过程**。其核心动机可归纳为三个层面：

1. **利用扩散模型的生成先验约束欠定映射**：预训练的文本到运动扩散模型（如 MDM）已从大规模动作数据中习得人体运动的自然流形。以该模型为骨干，可将压力重建任务转化为条件生成问题——在文本语义和压力信号的双重引导下，从噪声逐步去噪生成符合物理规律的动作序列，而非从零开始回归。

2. **分层解耦压力信息以匹配运动的多尺度结构**：人体运动天然具有层次性——全局的移动轨迹（如前进方向、步幅、转向）与局部的姿态变化（如踝关节角度、重心微调）在时空尺度上存在显著差异。Pressure2Motion 设计了对偶层次压力特征提取器，分别从压力图序列中独立编码“压力推断的运动轨迹”和“压力诱导的姿态偏移”，使模型能够以结构化的方式利用压力信号。

3. **建立压力-运动一致性约束以保证物理对齐**：生成的动作不仅要在视觉上自然流畅，还必须与输入压力信号保持物理一致——即足部接触点与压力中心在时空上精确对应。为此，Pressure2Motion 引入了基于五个关键关节（骨盆、双踝、双足）的压力-运动一致性损失，显式约束生成动作的足部接触模式与压力测量值对齐。

通过上述设计，Pressure2Motion 首次实现了从地面压力与文本提示到全身运动的分层生成式重建，为稀疏传感条件下的运动捕捉开辟了新路径。

## 核心方法与创新机理

Pressure2Motion 的核心创新在于**以分层方式将稀疏地面压力信号注入预训练文本到动作扩散模型**，从而解决从压力到全身姿态的严重欠定重建问题。与直接将压力嵌入拼接到运动输入的单层适配方案不同，该方法从压力数据中独立提取两类互补特征，并通过双通道控制机制分层注入生成过程。

### 1. 双层压力特征提取

传统可控动作生成方法通常将控制信号编码为单一特征向量，无法区分压力信号中蕴含的不同层次信息。Pressure2Motion 设计了**双层压力特征提取器**（Dual-level Pressure Feature Extractor），将压力图序列解耦为两个独立表示：

- **压力推断运动轨迹**（Pressure-Inferred Movement Trajectory, $\mathbf{T}_{\mathrm{traj}}$）：通过 $\mathbf{T}_{\mathrm{traj}} = \mathcal{F}_{\mathrm{traj}}(\mathbf{P})$ 从每帧压力图编码得到，提供人体在空间中的整体移动路径和朝向等高层全局信息。
- **压力诱导姿态偏移**（Pressure-Induced Posture Shifts, $\mathbf{S}_{\mathrm{shift}}$）：通过 $\mathbf{S}_{\mathrm{shift}} = \mathcal{F}_{\mathrm{shift}}(\mathbf{P}, \Delta\mathbf{P}, \mathbf{e})$ 编码压力图、时间差分及位置嵌入，捕捉足部压力分布变化所反映的局部姿态微调和动态细节。

这种双层解耦设计是方法的关键结构创新：运动轨迹负责“人往哪里走”的全局约束，姿态偏移负责“脚如何落地”的局部细化，二者互补地约束了从稀疏压力到全身动作的映射空间。

### 2. 分层控制注入机制

与现有可控扩散方法（如 **OmniControl** 和 **MaskControl**）在单一层级注入控制信号不同，Pressure2Motion 采用**分层压力调制运动合成器**（Hierarchical Pressure-Modulated Motion Synthesizer），通过 ControlNet 与 Adapter 两个独立模块分别注入不同层次的压力特征：

- **ControlNet 注入全局轨迹**：将运动轨迹嵌入直接加到噪声运动上（$\mathbf{x}_t' = \mathbf{x}_t + \mathbf{T}_{\mathrm{traj}}$），通过 ControlNet 生成残差特征 $\mathbf{r} = \mathcal{F}_{\mathrm{Ctrl}}(\mathbf{x}_t', t, c)$，提供高层全局引导。
- **Adapter 融合姿态偏移**：将 ControlNet 输出的残差特征 $\mathbf{r}$ 与姿态偏移 $\mathbf{S}_{\mathrm{shift}}$ 通过 Adapter 模块融合（$\mathbf{r}' = \mathcal{F}_{\mathrm{Adapt}}(\mathcal{Z}(\mathbf{r}), \mathbf{S}_{\mathrm{shift}}, c)$），进行局部细粒度调整，最终与预训练 MDM 输出相加得到预测的干净动作 $\hat{\mathbf{x}}_0'$。

消融实验（Table 3）验证了这一分层设计的必要性：移除 ControlNet 导致 FID 从 0.262 飙升至 1.3683，MPJPE 升至 0.1951；移除 Adapter 则使 FID 升至 0.695，MPJPE 升至 0.2092。这表明全局轨迹引导和局部姿态细化缺一不可。

### 3. 压力-动作一致性损失

为强化生成动作与输入压力的物理对齐，Pressure2Motion 引入**压力-动作一致性损失** $\mathcal{L}_{\mathrm{cons}}$。该损失选取骨盆、双踝、双足五个关键关节，计算其全局位置与压力推断轨迹的对齐误差：

$$\mathcal{L}_{\mathrm{cons}}(\mathbf{T}_{\mathrm{traj}}, \hat{\mathbf{x}}_0') = \frac{\sum_n \sum_j \sigma_{nj} \odot \lVert \mathcal{E}(\mathbf{T}_{\mathrm{traj}}) - R(\hat{\mathbf{x}}_0') \rVert}{\sum_n \sum_j \sigma_{nj}}$$

其中 $\sigma_{nj}$ 为基于压力幅值的置信度权重。这一设计的独特之处在于：它不直接回归关节位置，而是通过轨迹一致性约束，在保留扩散模型生成多样性的同时确保物理合理性。消融实验（Table 2）表明，移除该损失后 CoP Error 从 0.4260 升至 0.5320，MPJPE 从 0.1622 升至 0.1896。

### 4. 与基线的本质区别

现有可控动作生成方法（OmniControl、MaskControl）采用单层控制注入，将压力嵌入统一拼接到扩散模型的每步输入中。这种扁平化处理无法区分压力的全局运动语义与局部接触细节，导致重建精度和物理一致性均受限。Pressure2Motion 的关键突破在于：

- **语义解耦**：将压力信号显式分解为运动轨迹与姿态偏移两个语义层次。
- **分层注入**：通过 ControlNet 与 Adapter 分别处理全局与局部信息，而非简单拼接。
- **物理约束**：新增一致性损失直接优化压力-动作对齐，而非仅依赖扩散损失的隐式约束。

这一“解耦-分层注入-物理对齐”的三段式设计，使预训练文本到动作扩散模型的强生成先验得以有效适配稀疏压力输入，在 MPL 数据集上取得了 FID 0.262、MPJPE 0.1622 的最优结果。

Pressure2Motion 的核心设计思路是将预训练的文本到动作扩散模型（MDM）作为强生成先验，通过分层注入从稀疏压力信号中提取的双层次特征，约束欠定的压力-动作映射问题。其整体 pipeline 由三个关键阶段构成：

1. **双层次压力特征提取**：从输入的压力图序列中，独立提取高层运动轨迹（Pressure-Inferred Movement Trajectory）和底层姿态偏移（Pressure-Induced Posture Shifts）两类互补特征。
2. **分层控制注入**：将运动轨迹通过 ControlNet 注入扩散模型提供全局引导，同时将姿态偏移通过 Adapter 模块进行局部细粒度调整，形成从粗到精的分层控制机制。
3. **一致性约束**：引入压力-动作一致性损失，显式对齐重建动作的关键关节位置与压力推断的运动轨迹，强化物理合理性。

具体而言，给定压力图序列 $P$ 和文本提示 $c$，系统首先通过双层次压力特征提取器分别编码得到运动轨迹嵌入 $T_{traj}$ 和姿态偏移表示 $S_{shift}$。在扩散去噪过程中，$T_{traj}$ 被直接加到噪声运动 $x_t$ 上，经 ControlNet 处理后产生全局残差特征；该残差随后与 $S_{shift}$ 一起送入 Adapter 模块进行融合，最终与预训练 MDM 的输出相加，得到预测的干净动作 $\hat{x}'_0$。整个网络以扩散损失 $\mathcal{L}_{diff}$ 与一致性损失 $\mathcal{L}_{cons}$ 的加权和进行端到端训练。

这一分层设计的关键优势在于：高层轨迹特征约束了整体运动路径和身体朝向，底层姿态偏移则捕捉了足部接触、重心转移等细粒度动态变化，二者协同作用使得生成的动作既遵循文本语义，又与稀疏含噪的压力信号保持物理一致性。

![[assets/figures/papers/paper_list_l1034_https_arxiv_org_abs_2511_05038/figures/003_Figure_3.jpg]]
*Figure 3: The Pressure2Motion pipeline. We first extract an overall Movement Trajectory*

![[assets/figures/papers/paper_list_l1034_https_arxiv_org_abs_2511_05038/figures/001_Figure_1.jpg]]
*Figure 1: By conditioning on pressure signals and text descriptions, Pressure2Motion reconstructs high-fidelity, physically realistic motions, addressing the challenge of synthesizing human motion from sparse and noisy pressure data*

Pressure2Motion 的核心架构由三个紧密协作的模块构成，它们共同实现了从稀疏压力信号到高质量人体运动的分层生成。

### 双层级压力特征提取器

该模块负责从原始压力图序列中解耦出两个互补的表示，分别对应运动的全局轨迹和局部姿态细节。

**压力推断运动轨迹** 编码了每一帧压力图的全局空间语义，提供高层身体移动路径的引导。其编码过程为：

$$\mathbf{T}_{\mathrm{traj}} = \mathcal{F}_{\mathrm{traj}}(\mathbf{P}), \quad \mathbf{T}_{\mathrm{traj}} = \{T^i\}_{i=1}^N$$

其中 $\mathbf{P}$ 为输入的压力图序列，$\mathcal{F}_{\mathrm{traj}}$ 为轨迹编码器，输出长度为 $N$ 的轨迹嵌入序列。该表示捕捉了身体在空间中的整体位移与朝向。

**压力诱导姿态偏移** 则关注压力图的时间动态变化，编码细粒度的姿态调整信号。其编码过程为：

$$\mathbf{S}_{\mathrm{shift}} = \mathcal{F}_{\mathrm{shift}}(\mathbf{P}, \Delta\mathbf{P}, \mathbf{e}), \quad \mathbf{S}_{\mathrm{shift}} = \{S^i\}_{i=1}^N$$

其中 $\Delta\mathbf{P}$ 为相邻帧压力图的差分，$\mathbf{e}$ 为位置编码，$\mathcal{F}_{\mathrm{shift}}$ 为偏移编码器。该表示捕获了压力分布的瞬时变化所暗示的局部关节调整。

### 分层压力调制运动合成器

该模块将双层级压力特征分层注入预训练的文本到运动扩散模型（MDM），实现从全局到局部的递进式控制。

**预训练扩散骨干** 采用 MDM 的 $x_0$-prediction 范式。前向加噪过程为：

$$q(\mathbf{x}_t | \mathbf{x}_{t-1}) = \mathcal{N}(\sqrt{\alpha_t} \mathbf{x}_{t-1}, (1 - \alpha_t) I)$$

扩散模型的训练目标为预测干净运动 $\hat{\mathbf{x}}_0$：

$$\mathcal{L}_{\mathrm{diff}} = \mathbb{E}_{\mathbf{x}_0 \sim q(\mathbf{x}_0 | c), t \sim [1, T]} \left[ \| \mathbf{x}_0 - \hat{\mathbf{x}}_0 \|_2^2 \right]$$

其中 $c$ 为 CLIP 文本编码器输出的 512 维文本嵌入。

**ControlNet 全局引导** 首先将运动轨迹嵌入直接叠加到噪声运动上，再通过 ControlNet 提取残差特征：

$$\mathbf{x}_t' = \mathbf{x}_t + \mathbf{T}_{\mathrm{traj}}, \quad \mathbf{r} = \mathcal{F}_{\mathrm{Ctrl}}(\mathbf{x}_t', t, c)$$

这一操作使轨迹信息在去噪过程的每一步都参与全局运动路径的约束。

**适配器局部精调** 将 ControlNet 输出的残差特征 $\mathbf{r}$ 经零卷积 $\mathcal{Z}(\cdot)$ 处理后，与姿态偏移特征 $\mathbf{S}_{\mathrm{shift}}$ 及文本条件 $c$ 融合，生成最终的适配残差：

$$\hat{\mathbf{x}}_0' = \mathcal{F}_\theta(\mathbf{x}_t, t, c) + \mathbf{r}', \quad \mathbf{r}' = \mathcal{F}_{\mathrm{Adapt}}(\mathcal{Z}(\mathbf{r}), \mathbf{S}_{\mathrm{shift}}, c)$$

其中 $\mathcal{F}_\theta$ 为预训练的 MDM 去噪骨干，$\mathcal{F}_{\mathrm{Adapt}}$ 为适配器模块。最终预测的干净运动 $\hat{\mathbf{x}}_0'$ 同时融合了文本语义、全局轨迹约束和局部姿态调整。

### 压力-运动一致性损失

为强化生成运动与压力信号之间的物理对齐，引入作用于五个关键关节（骨盆、左右脚踝、左右脚）的一致性损失：

$$\mathcal{L}_{\mathrm{cons}}(\mathbf{T}_{\mathrm{traj}}, \hat{\mathbf{x}}_0') = \frac{\sum_n \sum_j \sigma_{nj} \odot \lVert \mathcal{E}(\mathbf{T}_{\mathrm{traj}}) - R(\hat{\mathbf{x}}_0') \rVert}{\sum_n \sum_j \sigma_{nj}}$$

其中 $\mathcal{E}(\cdot)$ 将轨迹嵌入映射到全局位置空间，$R(\cdot)$ 从预测运动中提取对应关节的全局位置，$\sigma_{nj}$ 为各关节的置信度权重。

**总训练损失** 为扩散损失与一致性损失的加权和：

$$\mathcal{L}_{\mathrm{total}} = \lambda_{\mathrm{diff}} \mathcal{L}_{\mathrm{diff}} + \lambda_{\mathrm{cons}} \mathcal{L}_{\mathrm{cons}}$$

### 控制强度调节

压力信号的注入强度由控制因子 $\tau$ 调节：

$$\tau = \frac{20 \hat{\Sigma}_t}{L}$$

其中 $\hat{\Sigma}_t = \min(\Sigma_t, 0.01)$，$\Sigma_t$ 为当前扩散步的噪声方差，$L$ 为序列长度。该设计使得在去噪早期（高噪声阶段）压力控制更强，而在后期（低噪声阶段）逐渐减弱，让扩散模型自身的生成先验主导细节生成。

## 实验与关键发现

### 主实验结果

Pressure2Motion 在 MPL 数据集上对所有基线方法取得了全面的领先。**Table 1** 给出了与四个可控运动合成基线（MDM、MotionDiffuse、OmniControl、MaskControl）以及纯文本基线（Text-Only）的定量对比。完整模型在重建精度与运动真实感两个维度上均达到最优：

![[assets/figures/papers/paper_list_l1034_https_arxiv_org_abs_2511_05038/figures/005_Table_1.jpg]]
*Table 1: Comparison of motion reconstruction with pressure control signal on the MPL dataset*

- **运动真实感**：FID 降至 0.262，显著优于次优方法 MaskControl 的 0.388（Δ = -0.126），表明生成的运动分布与真实运动分布最为接近。
- **重建精度**：MPJPE 为 0.1622，LMPJPE 为 0.1273，均低于所有基线。其中 MPJPE 相比 MaskControl 降低 0.0073，相比纯回归模型（Regression）降低 0.0404。
- **物理一致性**：新提出的 CoP Error 指标上，Pressure2Motion 取得 0.4260，较 MaskControl 的 0.5644 降低 0.1384，证明模型能有效将生成动作与输入压力信号对齐。
- **语义对齐**：R-precision Top-3 达到 0.545，优于所有基线，说明文本引导在压力条件基础上进一步提升了动作的语义准确性。

**关键对比**：纯文本基线（Text-Only）的 FID 为 0.576，CoP Error 高达 1.0019，表明缺少压力信号时模型无法产生物理合理的动作，压力输入是任务的核心必要条件。纯回归模型（Regression，将扩散退化为单步）的 MPJPE 升至 0.2026，FID 升至 0.628，说明扩散模型的迭代生成过程对于欠定问题的求解至关重要。

### 消融实验

**Table 2** 和 **Table 3** 分别从关键组件和架构设计两个层面进行了消融分析。

#### 关键组件消融（Table 2）

![[assets/figures/papers/paper_list_l1034_https_arxiv_org_abs_2511_05038/figures/006_Table_2.jpg]]
*Table 2: Ablation study of: Movement Trajectory (MT), Posture Shifts (PS), and the Consistency Loss (CL), and our Hierarchical design (Hi)*

- **移除运动轨迹（w/o MT）**：FID 从 0.262 飙升至 0.543，MPJPE 升至 0.2357，CoP Error 升至 0.5643。这表明高层运动轨迹是全局运动一致性的核心约束，缺失时模型无法维持正确的运动路径。
- **移除姿态偏移（w/o PS）**：FID 升至 0.847，MPJPE 升至 0.2025。姿态偏移的缺失导致局部细节严重失真，对运动真实感的破坏最为显著。
- **移除一致性损失（w/o CL）**：CoP Error 升至 0.5320，MPJPE 升至 0.1896。一致性损失直接约束压力-运动对齐，移除后物理一致性明显下降。
- **非分层设计（w/o Hi）**：将运动轨迹和姿态偏移以非分层方式统一注入，MPJPE 为 0.1692，显著差于完整模型的 0.1622，验证了分层注入策略的有效性。

#### 架构消融（Table 3）

![[assets/figures/papers/paper_list_l1034_https_arxiv_org_abs_2511_05038/figures/011_Table_3.jpg]]
*Table 3: Additional Ablation study of Model Archtecture*

- **移除 ControlNet**：FID 急剧升至 1.3683，MPJPE 升至 0.1951。ControlNet 负责将运动轨迹嵌入转化为全局引导残差，缺失时模型几乎丧失全局运动控制能力。
- **移除 Adapter**：FID 升至 0.695，MPJPE 升至 0.2092。Adapter 负责融合姿态偏移进行局部细粒度调整，缺失时局部姿态精度大幅下降。
- **移除 ControlNet 且移除 Adapter**：FID 进一步升至 1.4666，MPJPE 升至 0.2597，表明两者协同作用不可替代。

### 失败模式分析

基于定量结果与可视化对比（**Figure 4**、**Figure 5**），Pressure2Motion 的失败模式主要集中在以下方面：

![[assets/figures/papers/paper_list_l1034_https_arxiv_org_abs_2511_05038/figures/007_Figure_5.jpg]]
*Figure 5: Visualization results of ablation study*

1. **足部接触细节**：尽管 CoP Error 优于基线，但在快速转向或交叉步等复杂足部交互场景下，重建的足部位置仍存在偏移。这是由于压力信号本身的空间分辨率有限，难以精确区分紧密相邻的足部接触模式。
2. **上肢运动模糊性**：压力信号仅反映足底接触，对上肢运动无直接约束。模型依赖文本引导和运动先验推断上肢姿态，当文本描述模糊或与压力信号不完全匹配时，上肢重建可能出现语义漂移。
3. **长序列累积误差**：扩散模型的迭代生成特性虽提升了运动质量，但也导致长序列推理时误差逐步累积，尤其在 CoP Error 指标上表现为序列后期的精度衰减。

### 文本引导的影响

**Figure 6** 展示了不同文本提示对重建结果的影响。仅使用压力信号（无文本）时，模型仍能生成物理合理的运动，但动作语义不明确；加入文本引导后，模型可在保持压力一致性的前提下调整动作风格与语义。这表明文本与压力信号之间存在有效的互补机制：压力约束物理一致性，文本提供语义控制。

### 数据集与实验设置

MPL 数据集包含 20,944 条运动序列，约 230 万帧，覆盖 400 个动作类别，来自 25 名受试者。数据集按 80%/15%/5% 的比例划分为训练集、验证集和测试集。评估指标包括 MPJPE（全局位置误差）、LMPJPE（局部关节误差）、FID（运动真实感）、R-precision（语义对齐）以及新提出的 CoP Error（压力-运动物理一致性）。所有基线方法均被适配为接收逐帧压力控制信号，确保对比的公平性。

## 定位与知识库关联

### 任务定义与生成范式

Pressure2Motion 首次定义并求解了一个新任务：从地面压力图序列与文本提示中重建全身人体运动。该任务的核心瓶颈在于，地面压力信号高度稀疏且含噪，与全身姿态之间缺乏直接的几何运动学映射，导致从压力到动作的重建严重欠定。纯回归模型无法产生符合物理的合理动作，因此需要引入强生成先验来约束解空间。

在生成范式上，Pressure2Motion 属于**条件扩散生成**的谱系。其骨干网络基于预训练的文本到动作扩散模型 **MDM**（Tevet et al., ICCV 2023），该模型在 HumanML3D 等大规模动作-文本数据集上预训练，具备从文本语义到动作序列的强生成能力。Pressure2Motion 的创新在于，将这一文本到动作的生成先验适配为压力-文本双条件控制下的运动重建器，而非从头训练一个专用回归网络。

### 与可控运动合成方法的谱系关系

在可控运动合成领域，Pressure2Motion 与以下基线方法构成直接比较关系：

- **MDM**（Tevet et al., ICCV 2023）：作为预训练骨干，原始 MDM 仅支持文本条件生成。Pressure2Motion 在其基础上增加了压力信号的双层次注入机制，使其能够响应物理传感器输入。实验中将 MDM 适配为每帧压力控制（将压力嵌入拼接到每一去噪步的运动输入），但其缺乏专门的压力特征提取与分层注入设计，导致重建精度显著低于完整模型。
- **MotionDiffuse**（Zhang et al., TPAMI 2024）：同为文本到动作扩散模型，采用不同的扩散架构。在压力控制适配后，其性能弱于 Pressure2Motion，表明分层注入设计对不同扩散骨干具有通用优势。
- **OmniControl**（Xie et al., 2024）与 **MaskControl**（Bodur et al., 2024）：两者均属于空间可控的运动合成方法，通过稀疏空间信号（如关节轨迹、掩码）引导生成。Pressure2Motion 与之的关键区别在于，压力信号并非直接的空间约束，而是需要先被“翻译”为运动语义（轨迹与姿态偏移），再分层注入扩散过程。实验中将 OmniControl 和 MaskControl 的压力嵌入替换原空间控制输入后，其性能均不及 Pressure2Motion，验证了专用压力特征提取与分层注入的必要性。

### 方法谱系中的核心贡献定位

Pressure2Motion 在方法谱系中的核心贡献可归纳为三个层次：

1. **双层次压力特征提取**：区别于将压力图简单编码为单一嵌入的基线做法，Pressure2Motion 独立提取**压力推断的运动轨迹**（Pressure-Inferred Movement Trajectory）和**压力诱导的姿态偏移**（Pressure-Induced Posture Shifts）。前者捕捉全局位移与身体朝向，后者刻画足部接触模式变化引起的局部姿态调整。这一设计将稀疏压力信号解耦为高层语义与底层细节，为后续分层控制提供基础。

2. **分层控制注入机制**：通过 **ControlNet** 接收运动轨迹嵌入，提供高层全局引导；通过 **Adapter 模块**融合姿态偏移特征，进行局部细粒度调整。消融实验（Table 3）表明，移除 ControlNet 导致 FID 从 0.262 升至 1.3683，MPJPE 从 0.1622 升至 0.1951；移除 Adapter 导致 FID 升至 0.695，MPJPE 升至 0.2092。这证实了分层注入的不可替代性。

3. **压力-动作一致性损失**：提出 **CoP Error** 指标与对应的训练损失 $\mathcal{L}_{\mathrm{cons}}$，在 5 个关键关节（骨盆、双踝、双足）上对齐压力推断轨迹与重建运动。消融实验（Table 2）表明，移除一致性损失使 CoP Error 从 0.4260 升至 0.5320，MPJPE 从 0.1622 升至 0.1896。

### 适用边界与局限

Pressure2Motion 的适用边界受以下因素制约：

- **动作多样性受限**：MPL 数据集包含约 400 个动作类别，但主要覆盖平地行走、转身、蹲起等基础动作，尚未包含斜面行走、物体交互、跌倒等复杂场景。模型在这些未见动作上的泛化能力未经验证。
- **计算效率瓶颈**：在单张 NVIDIA A800 GPU 上重建一段运动序列约需 180 秒，远不能满足实时动作捕捉需求。扩散模型的迭代去噪过程是主要瓶颈，模型蒸馏或高效采样策略是潜在的改进方向。
- **文本标注偏差**：MPL 数据集的文本描述全部由视觉语言模型（VLM）自动生成，风格单一且与真实用户输入的多样性和模糊性存在差距。模型可能过拟合 VLM 的文本风格，对口语化、歧义性强的真实提示鲁棒性不足。
- **物理传感器假设**：模型假设输入为完整的地面压力图序列，未考虑传感器噪声、部分遮挡或采样率变化等实际部署中的退化情况。Figure 7 展示了真实场景部署，但论文未报告在传感器噪声或非理想条件下的性能退化程度。

### 开放问题

基于上述局限，以下开放问题值得进一步探索：

1. **数据集扩展**：如何构建覆盖更丰富动作类型（斜面行走、跳跃、物体搬运、双人交互等）的压力-运动配对数据集？是否需要合成数据或迁移学习来弥补采集成本？
2. **实时推理**：是否可以通过模型蒸馏、渐进式蒸馏或一致性模型等方法，在保持重建质量的前提下将推理时间压缩至秒级甚至亚秒级？
3. **文本鲁棒性**：如何提升模型对多样化、人类撰写的真实文本提示的泛化能力？是否需要在训练中引入文本增强或对抗性提示？
4. **多模态融合扩展**：当前模型仅融合压力与文本，未来是否可纳入 IMU、视觉等互补模态，以进一步提升重建精度与鲁棒性？

## 原文 PDF

![[paperPDFs/CVPR_2026/Pressure2Motion_Hierarchical_Human_Motion_Reconstruction_from_Ground_Pressure_with_Text_Guidance.pdf]]
