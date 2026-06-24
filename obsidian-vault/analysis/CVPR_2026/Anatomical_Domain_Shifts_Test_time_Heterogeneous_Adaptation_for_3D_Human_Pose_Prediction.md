---
title: "Anatomical Domain Shifts: Test-time Heterogeneous Adaptation for 3D Human Pose Prediction"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/Anatomical_Domain_Shifts_Test_time_Heterogeneous_Adaptation_for_3D_Human_Pose_Prediction.pdf
project_link: null
code_link: null
aliases:
- TH
- ADSTTHA3HPP
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
core_operator: 根据实例归一化统计与 Earth Mover's Distance 检测到的解剖段域偏移，选择性恢复或微调相应部位的参数子集。
primary_logic: 人体运动中，域偏移在不同解剖段（左/右臂、左/右腿、躯干）上具有异质性，某些部位偏移显著而另一些保持稳定；因此，应针对各部位进行差异化的自适应。
claims:
- t-SNE 可视化显示源域与目标域的全身体特征分布不同，但右腿和躯干分布接近，证明域偏移在解剖段层级存在异质性。
- 在 H3.6M、CMU Mocap、GRAB、RICH 四个数据集上，TT-HA 在 MPJPE、P-MPJPE 和 PCK@150 指标上均优于 HoCoTTA 等基线，表明解剖针对性自适应有效。
- H3.6M 上 MPJPE (mm) @1000ms = 97.4
- H3.6M 上 MPJPE (mm) @400ms = 49.7
---

# Anatomical Domain Shifts: Test-time Heterogeneous Adaptation for 3D Human Pose Prediction

> [!tip] 核心洞察
> 人体运动中，域偏移在不同解剖段（左/右臂、左/右腿、躯干）上具有异质性，某些部位偏移显著而另一些保持稳定；因此，应针对各部位进行差异化的自适应。

| 字段 | 内容 |
|------|------|
| 中文题名 | 解剖域偏移：面向三维人体姿态预测的测试时异构自适应 |
| 英文题名 | Anatomical Domain Shifts: Test-time Heterogeneous Adaptation for 3D Human Pose Prediction |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://openaccess.thecvf.com/content/CVPR2026/html/Cui_Anatomical_Domain_Shifts_Test-time_Heterogeneous_Adaptation_for_3D_Human_Pose_CVPR_2026_paper.html) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction |
| Method | TT-HA |
| Dataset | H3.6M, GRAB |

> [!tip] 效果简介
> - H3.6M 上，MPJPE (mm) @1000ms 97.4 vs 101.4 (HoCoTTA) (-4.0)；MPJPE (mm) @400ms 49.7 vs 52.8 (HoCoTTA) (-3.1)。
> - GRAB 上，MPJPE (mm) @1000ms 127.5 vs 131.8 (HoCoTTA) (-4.3)。

## 概述

**核心问题**：现有人体姿态预测（Human Pose Prediction, HPP）的持续测试时自适应（continual test-time adaptation, TTA）方法将人体视为均质整体，忽略了解剖段之间固有的运动异质性。这导致模型对域偏移稳定的身体部位（如躯干）产生过适应，而对偏移频发的关节（如手臂、腿）则适应不足，最终限制了跨域预测的鲁棒性。

**核心洞察**：人体运动中，域偏移并非均匀分布，而是在不同解剖段（左/右臂、左/右腿、躯干）上呈现显著的异质性——某些部位偏移剧烈，而另一些几乎不变。Figure 1 通过 t-SNE 可视化直观验证了这一点：从 H3.6M（源域）到 GRAB（目标域）的迁移中，全身体特征分布明显不同，但右腿和躯干的分布却高度接近，表明域偏移确实在解剖段层级存在差异。

**方法定位**：本文提出 **TT-HA**（Test-Time Heterogeneous Adaptation），一种解剖感知的异构测试时自适应框架。其核心机制包括：
- **解剖参数分解**：利用信息论稳定性指标将模型参数划分为五个解剖段子集（左/右腿、左/右臂、躯干）及共享参数，为差异化自适应奠定基础。
- **域偏移检测**：以实例归一化（IN）替代批量归一化（BN），通过指数移动平均维护全局 IN 统计，并利用 Earth Mover’s Distance（EMD）量化各部位当前批次与历史分布间的域变化幅度。
- **选择性自适应与知识恢复**：当检测到某部位发生域偏移峰值时，将该部位参数恢复至源预训练值以防止灾难性遗忘；对于偏移较小的部位，则通过自监督时序与空间一致性损失进行微调。

**主要结果**：在 H3.6M、CMU Mocap、GRAB、RICH 四个数据集上，TT-HA 在 MPJPE、P-MPJPE 和 PCK@150mm 指标上均优于当前最佳的持续 TTA 方法 HoCoTTA。例如，在 H3.6M 的 1000ms 预测上，MPJPE 从 101.4mm 降至 97.4mm（降低 4.0mm）；在 GRAB 的 1000ms 预测上，MPJPE 从 131.8mm 降至 127.5mm（降低 4.3mm）。消融实验进一步验证了动量 η=0.95、学习率 λ=1.0e-3、峰值阈值 τ_peak=12 及窗口大小 w=36 等超参数设置的有效性。

**方法谱系与知识库定位**：TT-HA 处于**测试时自适应**与**三维人体姿态预测**的交汇点。其基线谱系涵盖时空图卷积方法 **LTD**、渐进猜测优化方法 **PGBIG**、纯 MLP 方法 **siMLPe**，以及测试时自适应方法 **H/P-TTP** 和 **HoCoTTA**。相较于 HoCoTTA 的全局域敏感/不变参数划分，TT-HA 首次将解剖异质性引入持续 TTA 框架，通过部位级 IN 统计与 EMD 驱动的选择性参数恢复，实现了更精细的域偏移应对策略。这一思路与参数隔离、模块化持续学习等方向存在潜在关联，但其解剖分解的粒度依赖手工定义，向更一般运动数据的泛化仍需验证。

## 背景与动机

### 问题背景

三维人体姿态预测（3D Human Pose Prediction, HPP）旨在从观测到的历史姿态序列推断未来的人体关节运动，是计算机视觉与图形学中的核心任务，支撑着自动驾驶、人机交互、运动分析等应用。主流方法依赖在大型标注数据集上预训练的深度模型，然而在实际部署中，测试数据与源训练数据之间普遍存在**域偏移**（domain shift）——包括环境变化、相机视角差异、运动风格漂移以及个体体型与动作习惯的异质性。这种偏移导致预训练模型的预测精度大幅下降，成为阻碍 HPP 系统可靠落地的关键瓶颈。

为应对这一挑战，**测试时自适应**（Test-Time Adaptation, TTA）范式应运而生：模型在推理阶段利用无标签的测试样本持续更新自身参数，从而动态适应变化的域条件。在 HPP 领域，基于 TTA 的方法已展现出优于静态模型的泛化能力。

### 现有方法的缺口：忽视人体运动的解剖异质性

当前最先进的持续测试时自适应方法，如 **HoCoTTA**，在应对域偏移时取得了显著进展，但其核心假设存在一个根本性局限：**它们将人体视为一个均质的整体**。具体而言，这些方法通常基于全身体（full-body）的批量归一化（Batch Normalization, BN）统计或全局熵最小化策略来检测域变化并触发模型更新，隐含地假定域偏移均匀地作用于人体的所有部位。

然而，这一假设与人体运动的本质特征相悖。人类运动由多个解剖段（左/右臂、左/右腿、躯干）协同完成，各部位的运动模式、自由度以及受环境和任务影响的程度存在天然差异。例如，在“切菜”动作中，手臂的运动幅度和复杂度远高于腿部和躯干；当测试环境从实验室切换到户外时，手臂的运动分布可能因操作对象的变化而发生剧烈偏移，而腿部和躯干的运动模式可能保持相对稳定。这种**解剖段层级的域偏移异质性**意味着：

- 对域偏移稳定的部位（如躯干）施加过度自适应，会引发**灾难性遗忘**，破坏源预训练中已学到的有效知识；
- 对域偏移频发的部位（如手臂）自适应不足，则导致**欠适应**，无法充分捕捉目标域的分布变化。

现有方法的“一刀切”策略在上述两种失效模式之间难以取得平衡，构成了当前 HPP 测试时自适应的核心性能瓶颈。

### 概念验证：解剖域偏移的存在性

为验证上述假设，本文对源域（H3.6M）和目标域（GRAB）的人体特征进行了 t-SNE 可视化分析（Figure 1）。结果表明：全身体特征分布在源域与目标域之间呈现出明显的分离，印证了整体域偏移的存在；然而，当按照解剖段（左/右腿、左/右臂、躯干）分别观察时，**右腿和躯干的特征分布在不同域之间高度重叠**，而其他部位则差异显著。这一现象直接证明：域偏移并非均匀地作用于全身，而是在解剖段层级呈现异质性——某些部位保持相对稳定，另一些则发生剧烈变化。

### 本文动机与核心思路

基于上述洞察，本文提出核心命题：**对于人体运动，域偏移主要体现在解剖段层面而非全身层面，因此测试时自适应应当针对不同部位进行差异化处理**。

这一命题催生了三个关键设计需求：

1. **细粒度的域偏移感知**：需要一种机制，能够在推理过程中实时量化每个解剖段的域变化幅度，而非依赖全身体的粗粒度统计。
2. **部位选择性的参数更新**：模型参数应按照解剖结构进行划分，使得自适应操作（微调或恢复）能够精准地作用于受影响的部位子集，而非全局参数。
3. **知识稳定性保护**：对于域偏移稳定的部位，应避免不必要的参数更新，以保留源预训练知识；对于发生突变偏移的部位，应具备将参数恢复至源状态的能力，以防止错误累积。

本文提出的 **TT-HA（Test-Time Heterogeneous Adaptation）** 框架正是围绕上述需求构建的：它通过解剖参数分解、基于实例归一化与 Earth Mover's Distance 的部位级域偏移检测、以及选择性的知识恢复与微调机制，首次在 HPP 的测试时自适应中实现了对解剖异质性的显式建模与利用。

## 核心创新

### 问题瓶颈：解剖段域偏移的异质性

现有面向人体姿态预测（HPP）的持续测试时自适应（CTTA）方法，例如当前最佳的 **HoCoTTA**，将人体视为一个均质的整体进行参数更新。这种“一刀切”的策略忽略了人体运动中一个关键事实：**域偏移在不同解剖段上具有显著的异质性**。如 Figure 1 的 t-SNE 可视化所示，当从 H3.6M（源域）迁移到 GRAB（目标域）时，全身体的特征分布确实发生了整体偏移；然而，右腿和躯干的特征分布在源域与目标域之间却高度接近，而其他部位（如手臂）则偏移明显。这意味着，对全身体参数进行无差别自适应，会导致对域偏移稳定区域（如躯干）的**过适应**，以及对偏移频发关节（如手臂）的**欠适应**，从而损害整体预测精度与稳定性。

### 因果调控：从全局自适应到解剖针对性干预

TT-HA 的核心创新在于将“域偏移”的观测与干预粒度从**全身体**下沉到**解剖段**，构建了一个“检测—选择性恢复/微调”的闭环调控机制。其因果逻辑链如下：

1.  **解剖参数分解**：利用信息论稳定性度量（Eq. 1），量化模型中每个参数对特定解剖段（左/右臂、左/右腿、躯干）输出分布的敏感性，将模型参数分解为五个解剖段专属子集 $\Theta_p$ 与一个共享子集 $\Theta_{shared}$。这为后续的差异化干预提供了结构基础。
2.  **部位级域偏移量化**：将基线模型中的批量归一化（BN）替换为实例归一化（IN），使归一化统计量能够反映单样本的特性。通过指数移动平均（EMA）维护各部位的全局 IN 统计，并利用 Earth Mover's Distance（EMD）计算当前批次与历史统计之间的分布距离 $\omega_p^{(t)}$（Eq. 3），从而**实时、部位级地量化域变化幅度**。
3.  **域偏移峰值检测与选择性干预**：维护一个滑动窗口 $\Omega_p$，通过 z-score 判断 $\omega_p^{(t)}$ 是否构成一个域偏移“峰值”。当检测到峰值（$\omega_p^{(t)} \ge \tau_{peak}$）时，触发**选择性知识恢复**（Eq. 4），仅将该受影响部位的参数 $\Theta_p$ 重置回源预训练值 $\Theta_p^{(0)}$，防止错误累积。对于域偏移平稳的部位，则利用自监督的时间与空间一致性损失进行**选择性微调**（Eq. 5），以适应渐进式的域变化。

### 相对基线的关键变更槽位

| 变更槽位 | 基线方法 (以 HoCoTTA 为代表) | 本方法 (TT-HA) | 核心作用 |
| :--- | :--- | :--- | :--- |
| **归一化层** | 批量归一化 (BN) | 实例归一化 (IN) | 使统计量对单样本域变化敏感，为部位级域偏移估计提供基础 |
| **参数划分** | 全局域敏感/不变参数划分或全身体统一参数 | 按左/右腿、左/右臂、躯干五个解剖段加共享参数子集划分 | 为差异化自适应提供结构基础，实现“对症下药” |
| **域偏移检测与自适应策略** | 基于全身体 BN 统计或全局熵最小化，无部位选择性 | 基于部位级 IN 统计与 EMD 的域偏移量化，根据峰值检测选择性恢复源参数或微调 | 实现对异质性域偏移的精确感知与针对性响应，避免过适应与欠适应 |
| **知识恢复机制** | 全模型参数随机重置或全部恢复 | 仅对检测到域偏移峰值的部位参数恢复至源预训练值 | 在抵抗灾难性遗忘的同时，保留对稳定区域的适应能力 |

### 证据支撑

-   **概念验证**：Figure 1 通过 t-SNE 可视化直接证明了“域偏移在解剖段层级存在异质性”这一核心假设，为整个方法提供了动机。
-   **性能验证**：在 H3.6M、CMU Mocap、GRAB、RICH 四个数据集上的主实验结果（Table 1）表明，TT-HA 在所有评估指标（MPJPE, P-MPJPE, PCK@150）上均一致优于 HoCoTTA 等基线。例如，在 H3.6M 的 1000ms 预测上，MPJPE 从 101.4mm 降至 **97.4mm**，相对提升 3.9%。定性结果（Figure 3）也直观显示，TT-HA 对手臂和腿部等偏移频发部位的预测精度提升尤为明显，而躯干等稳定部位的性能得以保持，印证了异构自适应的有效性。

## 整体框架

TT-HA 的核心思想是将人体姿态预测的测试时自适应从“全身统一处理”升级为“解剖段异构自适应”。其整体 pipeline 由五个功能模块串联而成，形成“检测—恢复—微调”的闭环，如 Figure 2 所示。

![[assets/figures/papers/paper_list_l1006_https_openaccess_thecvf_com_content_CVPR2026_html_Cui_Anatomical_Domain/figures/002_Figure_2.jpg]]
*Figure 2: Overall illustration of the proposed TT-HA. It is capable of detecting domain changes at human anatomical segments. It selectively restores the parameters of the affected segments to their source-trained values (colored circles degrade to gray ones); For stable human parts, TT-HA fine-tune part-specific parameter at test-time, maintaining the stability of the overall model while ensuring robust adaptation to new domains (colored arrows)*

**输入与输出定义**。给定一个观测姿态序列 $\mathbf{X}_{1:T} = [\mathbf{x}_1, \mathbf{x}_2, ..., \mathbf{x}_T] \in \mathcal{X}$，模型需预测未来 $\Delta T$ 帧的姿态 $\mathbf{Y}_{1:\Delta T} = [\mathbf{y}_1, \mathbf{y}_2, ..., \mathbf{y}_{\Delta T}] \in \mathcal{Y}$。每个 $\mathbf{x}_t$ 和 $\mathbf{y}_t$ 均为三维关节点坐标。TT-HA 在测试时持续接收流式数据批次，不对目标域分布做独立同分布假设。

**模块 1：解剖参数分解（Anatomical Parameter Decomposition）**。在源域预训练完成后，TT-HA 利用信息论稳定性指标 $S_p(\Theta^i)$（Eq. 1）量化每个参数 $\Theta^i$ 对五个解剖段（左/右腿、左/右臂、躯干）输出分布的敏感性。通过 $\tau$-分位数（$\tau=0.2$）筛选出对各段敏感度最低的参数，分别归入 $\Theta_{l.leg}$、$\Theta_{l.arm}$、$\Theta_{r.leg}$、$\Theta_{r.arm}$、$\Theta_{torso}$ 五个部位子集；剩余参数聚合成共享参数集 $\Theta_{shared}$。这一步在测试开始前一次性完成，为后续的选择性操作提供参数粒度的基础。

**模块 2：域动态估计（Domain Dynamics Estimation）**。TT-HA 将基线模型中的批量归一化（BN）替换为实例归一化（IN），使得每个测试样本产生独立的统计量。系统维护一组全局 IN 统计 $\boldsymbol{\mu}_p^{(t-1)}$、$\boldsymbol{\sigma}_p^{(t-1)}$，通过指数移动平均（动量 $\eta=0.95$，Eq. 2）融合历史信息。对当前批次，计算运行 IN 统计 $\tilde{\boldsymbol{\mu}}_p^{(t)}$、$\tilde{\boldsymbol{\sigma}}_p^{(t)}$，并与全局统计通过 Earth Mover's Distance（EMD）的闭式解（Eq. 3）得到部位级域偏移量 $\omega_p^{(t)}$。该值非负，越大表示该解剖段的分布偏移越剧烈。

**模块 3：域偏移峰值检测（Domain Shift Peak Detection）**。系统维护一个长度为 $w=36$ 的滑动窗口 $\Omega_p = [\omega_p^{(t-w)}, ..., \omega_p^{(t-1)}]$，对当前 $\omega_p^{(t)}$ 计算 z-score。当 $\omega_p^{(t)}$ 超出窗口均值 $\tau_{peak}=12$ 个标准差时，判定该部位发生了突然的域变化（peak），触发知识恢复；否则视为渐进偏移，触发微调。Algorithm 1 给出了完整的峰值检测流程。

**模块 4：异构测试时自适应（Heterogeneous Test-time Adaptation）**。这是 pipeline 的决策核心，根据峰值检测结果对五个部位参数子集执行差异化操作（Algorithm 2）：
- **选择性知识恢复**：若 $\omega_p^{(t)} \geq \tau_{peak}$，将对应部位参数重置为源预训练值 $\Theta_p^{(0)}$（Eq. 4），防止错误累积。
- **选择性微调**：若 $\omega_p^{(t)} < \tau_{peak}$，仅对该部位参数子集 $\Theta_p^{(t)}$ 执行梯度下降（Eq. 5），学习率 $\lambda=1.0\times10^{-3}$，共享参数 $\Theta_{shared}$ 全程保持不变。

**模块 5：自监督时间与空间一致性损失**。微调过程不依赖目标域标签，而是使用两个解剖段级别的自监督损失：
- 时间一致性损失 $\mathcal{L}_p^{temp}$（Eq. 6）：约束预测姿态的帧间差分与观测序列一致，保持运动平滑性。
- 空间一致性损失 $\mathcal{L}_p^{spatial}$（Eq. 7）：约束预测骨骼长度与观测骨骼长度一致，防止身体结构畸变。

**数据流总结**：测试批次进入模型 → IN 统计更新并计算 EMD → 滑动窗口检测峰值 → 对每个解剖段独立判定：峰值则恢复源参数，否则用自监督损失微调该段参数 → 输出预测姿态。这种“检测—恢复—微调”的闭环使得 TT-HA 能对域偏移频发的部位（如手臂）进行快速知识重置，同时对稳定部位（如躯干）保持渐进适应，避免了全局统一策略下的过适应与欠适应矛盾。

## 核心模块与公式推导

### 3.1 解剖参数分解

TT‑HA 的核心前置步骤是将预训练模型的参数按人体解剖结构进行划分，使后续的测试时自适应能够以“部位”为粒度展开。具体而言，模型参数被分解为五个解剖段子集：**左腿**（Θ_{l.leg}）、**左臂**（Θ_{l.arm}）、**右腿**（Θ_{r.leg}）、**右臂**（Θ_{r.arm}）和**躯干**（Θ_{torso}），剩余参数聚合为共享参数集 Θ_{shared}。

划分的依据并非简单的层索引，而是基于信息论稳定性度量——对源域数据施加微小参数扰动 ε ∼ 𝒰(-a,a)，计算各解剖段输出分布的条件 KL 散度期望，以此量化参数 Θ^i 对部位 p 的敏感度：

$$S_p(\Theta^i) = \mathbb{E}_{\mathbf{X}}[\mathbb{E}_{\epsilon}[D_{\mathrm{KL}}(\mathcal{P}(\mathbf{Y}_p|\mathbf{X},\Theta) \lVert \mathcal{P}(\mathbf{Y}_p|\mathbf{X},\Theta+\epsilon))]] \quad (1)$$

其中，**Y_p** 表示部位 p 的关节输出，**X** 为输入运动序列。敏感度越低，说明该参数对部位 p 的预测影响越专一。TT‑HA 取 τ-分位数（τ=0.2）筛选低敏感度参数归入对应部位子集 Θ_p，最终形成解剖分解 {Θ_{l.leg}, Θ_{l.arm}, Θ_{r.leg}, Θ_{r.arm}, Θ_{torso}} ∪ Θ_{shared}。

> **瓶颈分析**：该模块将“全身均质自适应”转化为“部位异质自适应”，为后续选择性恢复与微调提供了参数级操作空间。其计算代价在于需在源域预训练后完成一次全参数敏感度评估，但该过程仅执行一次，不影响测试时效率。

---

### 3.2 域动态估计

测试时，TT‑HA 需要持续感知各解剖段的域偏移程度。为此，方法将基线模型中的批量归一化（BN）替换为**实例归一化（IN）**，利用 IN 对单样本统计量的敏感性来捕获分布变化。

为抑制单样本噪声，TT‑HA 维护全局 IN 统计量（均值 **μ**_p 与方差 **σ**_p），并以指数移动平均方式更新：

$$\boldsymbol{\mu}_p^{(t-1)} = (1-\eta)\boldsymbol{\mu}_p^{(t-2)} + \eta \boldsymbol{\mu}_p^{(t-1)}, \quad \boldsymbol{\sigma}_p^{(t-1)} = (1-\eta)\boldsymbol{\sigma}_p^{(t-2)} + \eta \boldsymbol{\sigma}_p^{(t-1)} \quad (2)$$

动量 η 设为 0.95，以平衡历史稳定性与当前敏感性（消融实验 Table 4 验证了该取值的有效性）。

域偏移量 **ω_p^{(t)}** 通过计算历史全局 IN 分布与当前批次 IN 分布之间的 **Earth Mover’s Distance（EMD）** 得到。由于 IN 统计可建模为高斯分布，EMD 具有闭式解：

$$\omega_p^{(t)} = \frac{\sqrt{2\pi}}{C} \sum_{c=1}^{C} \frac{\sigma_{p,c}^{(t-1)}+\tilde{\sigma}_{p,c}^{(t)}}{2} \cdot \operatorname{erfc}\left(\frac{\tilde{\mu}_{p,c}^{(t)}-\mu_{p,c}^{(t-1)}}{\sigma_{p,c}^{(t-1)}+\tilde{\sigma}_{p,c}^{(t)}}\right) \quad (3)$$

其中，**C** 为部位 p 的特征通道数，**μ̃**、**σ̃** 为当前批次的 IN 统计，**μ**、**σ** 为历史全局统计，erfc 为互补误差函数。ω_p^{(t)} 是非负标量，值越大表示该部位域偏移越剧烈。

> **因果机制**：IN 统计量天然反映单样本的风格/域特征，而 EMD 度量两个分布之间的最小传输代价，比简单的均值差或方差比更能捕获分布形态的整体偏移。这一设计使得域偏移检测对解剖段异质性敏感，而非被全身平均所淹没。

---

### 3.3 域偏移峰值检测

持续的域偏移可能累积误差导致模型崩溃，但并非所有偏移都需要激进干预。TT‑HA 区分“渐进漂移”与“突变偏移”：前者通过微调适应，后者则触发知识恢复。

峰值检测基于滑动窗口与 z-score 机制。维护窗口 Ω_p = [ω_p^{(t-w)}, …, ω_p^{(t-1)}]，窗口大小 w=36（消融实验 Table 5 验证）。当当前 ω_p^{(t)} 超出窗口均值 **τ_peak = 12** 个标准差时，判定为域偏移峰值：

$$\Theta_p^{(t)} \leftarrow \Theta_p^{(0)}, \text{ if } \omega_p^{(t)} \geq \tau_{\text{peak}} \quad (4)$$

即仅将**受影响部位**的参数重置为源预训练值 Θ_p^{(0)}，其余部位参数保持不变。

---

### 3.4 异构自适应与自监督损失

对于未触发峰值恢复的部位（ω_p^{(t)} < τ_peak），TT‑HA 使用自监督损失进行单步梯度下降微调：

$$\Theta_p^{(t)} \leftarrow \Theta_p^{(t)} - \lambda \nabla_{\Theta_p^{(t)}} (\mathcal{L}^{\text{temp}}+\mathcal{L}^{\text{spatial}}) \quad (5)$$

学习率 λ=1.0×10⁻³。两项自监督损失均不依赖目标域标签，仅利用运动学先验：

- **时间一致性损失**（Temporal Consistency Loss）：约束预测姿态的时序差分与观测序列一致，保持运动平滑性：

$$\mathcal{L}_p^{\text{temp}} = \frac{1}{T-1} \sum_{i=1}^{T-1} \| \tilde{\mathbf{y}}_{p,i+1} - \tilde{\mathbf{y}}_{p,i} - (\mathbf{x}_{p,i+1} - \mathbf{x}_{p,i}) \|_2 \quad (6)$$

其中 **x** 为观测姿态，**ỹ** 为预测姿态，T 为序列长度。

- **空间一致性损失**（Spatial Consistency Loss）：约束预测骨骼长度与观测保持一致，防止身体结构畸变：

$$\mathcal{L}_p^{\text{spatial}} = \frac{1}{T(N-1)} \sum_{i=1}^{T} \sum_{n=1}^{N-1} \| \tilde{L}_{i,n}^{\text{pred}} - L_{i,n}^{\text{obs}} \|_1 \quad (7)$$

其中 **L** 为相邻关节间的骨骼长度，N 为部位 p 的关节数。

> **设计意图**：时间一致性损失防止预测运动出现突变抖动，空间一致性损失防止骨骼伸缩失真。两者均以部位 p 为单位独立计算，使得微调信号精准作用于域偏移部位，避免稳定部位被无关梯度污染。

### 补充图表

![[assets/figures/papers/paper_list_l1006_https_openaccess_thecvf_com_content_CVPR2026_html_Cui_Anatomical_Domain/figures/001_Figure_1.jpg]]
*Figure 1: Proof of Concept: Anatomical Domain Shift. t-SNE embedding of human segments based on anatomical separation, i.e., left/right legs, left/right arms, and torso, and full body under the challenging domain shift setup for TTA-based HPP [11]. This plot shows the feature topology of the source domain—H3.6M [24] (upper), and the target domain—GRAB [48] (bottom). The diagram exhibits that while full-body embedding differ between source and target domains, such matter is not present on all segments, and as a contrast, the distribution of certain segments (i.e., right leg and torso) is very close. This provides the proof of concept of our central hypothesis: for human motion, domain shift manifests...*

## 实验与分析

### 核心实验设计与评估协议

为系统验证 TT-HA 的解剖段异构自适应能力，论文设计了四种互补的测试时域偏移评估协议：

- **Setup-1 (通用预测能力)**：在 H3.6M、CMU Mocap、GRAB、RICH 四个数据集上进行跨域评估，源域为 H3.6M，目标域为其余三个数据集。该设置直接检验模型面对不同运动分布时的鲁棒性。
- **Setup-2 (新类别泛化)**：在 H3.6M 内部按动作类别划分源域和目标域，评估模型对未见动作类型的预测能力。
- **Setup-3 (新主体泛化)**：按主体 ID 划分，检验模型对不同人体运动模式的适应能力。
- **Setup-4 (新数据集泛化)**：以 H3.6M 为源域，在 3DPW 和 AMASS 等未见数据集上评估跨数据集的迁移能力。

所有基线结果均引用自原论文或经 的转换方法重新统计，消除了指标不一致带来的偏差。评估指标采用 **MPJPE** (Mean Per Joint Position Error, mm)、**P-MPJPE** (Procrustes-aligned MPJPE) 和 **PCK@150mm** (Percentage of Correct Keypoints within 150mm)。

### 主实验结果：解剖段自适应带来一致且显著的精度提升

Table 1 报告了 Setup-1 下四个数据集的综合对比。TT-HA 在所有数据集和预测时域上均取得最优或次优结果，尤其在长时预测上优势更为突出：

![[assets/figures/papers/paper_list_l1006_https_openaccess_thecvf_com_content_CVPR2026_html_Cui_Anatomical_Domain/figures/003_Table_1.jpg]]
*Table 1: Evaluation of general predictive ability under the experimental ‘setup-1’ across 4 datasets, where the best results are in bold, and the second, in underlined. As RICH [23] is newly-introduced in this paper, we re-evaluate the results on it, and the results of other datasets are from their original paper. For the baselines without P-MPJPE and PCK@150mm, we leverage the transformation as [10] to re-statistic*

- **H3.6M 数据集**：在 1000ms 预测时域上，TT-HA 的 MPJPE 为 **97.4mm**，相比当前最佳的持续测试时自适应方法 **HoCoTTA** 的 101.4mm 降低了 **4.0mm**；在 400ms 时域上，TT-HA 为 **49.7mm**，HoCoTTA 为 52.8mm，降低 3.1mm。这验证了解剖段针对性自适应对长时运动预测的累积误差抑制效果。
- **GRAB 数据集**（包含丰富的手-物交互动作）：1000ms 时域上 TT-HA 的 MPJPE 为 **127.5mm**，HoCoTTA 为 131.8mm，降低 **4.3mm**。GRAB 的动作复杂性使得全局均质自适应策略更容易在稳定部位过适应，而 TT-HA 的选择性恢复机制有效避免了这一问题。
- **CMU Mocap 和 RICH 数据集**：TT-HA 在 P-MPJPE 和 PCK@150mm 指标上同样保持领先。例如 CMU Mocap 1000ms 的 P-MPJPE 为 **50.4mm**，验证了方法对不同运动捕捉场景的泛化能力。

值得注意的是，TT-HA 在肢体部位（手臂、腿部）的误差下降幅度比躯干更为显著——论文报告肢体误差额外降低了 **9.2%**。这与 Figure 1 的 t-SNE 可视化发现一致：躯干和右腿在源域与目标域间的特征分布本就接近，域偏移主要集中在上肢等运动幅度大的解剖段。TT-HA 通过选择性微调这些受影响部位的参数，实现了“好钢用在刀刃上”的自适应。

Table 2 和 Table 3 分别报告了 Setup-2/3 和 Setup-4 的结果。TT-HA 在新动作类别、新主体和新数据集上均保持优势，表明解剖段分解策略捕捉到的是人体运动的通用结构先验，而非过拟合于特定数据集。

![[assets/figures/papers/paper_list_l1006_https_openaccess_thecvf_com_content_CVPR2026_html_Cui_Anatomical_Domain/figures/004_Table_2.jpg]]
*Table 2: Evaluation of predictive ability for new categories/subjects under the ‘setup-2’ and ‘setup-3’*

![[assets/figures/papers/paper_list_l1006_https_openaccess_thecvf_com_content_CVPR2026_html_Cui_Anatomical_Domain/figures/005_Table_3.jpg]]
*Table 3: Evaluation of predictive ability for novel datasets under ‘setup-4’*

### 定性分析：解剖段预测精度的差异化改善

Figure 3 提供了 TT-HA 与 HoCoTTA 的定性对比。以灰色网格表示真值，紫色表示 HoCoTTA 预测，蓝色表示 TT-HA 预测。红色和绿色框分别高亮了手臂和腿部的关键细节区域。结果显示：

![[assets/figures/papers/paper_list_l1006_https_openaccess_thecvf_com_content_CVPR2026_html_Cui_Anatomical_Domain/figures/006_Figure_3.jpg]]
*Figure 3: Qualitative comparison: The gray mesh denotes the ground truth, while purple and blue are the predictions of HoCoTTA [11] (left) and TT-HA (right). Important details of arm and leg are highlighted with red and green boxes. It is clear that our TT-HA, for hand and leg, achieves the closer predictions to the ground truth, despite the similar performance for torso and head*

- **手臂和腿部**：TT-HA 的预测与真值更为接近，尤其在手部精细姿态和腿部运动轨迹上，HoCoTTA 出现了明显的偏移或模糊。
- **躯干和头部**：两种方法的预测质量相近，这与躯干域偏移较小的假设一致——TT-HA 在这些部位倾向于保持源参数，避免了不必要的参数漂移。

该定性结果直接支撑了核心假设：**解剖段异构自适应能够在域偏移频发的部位集中优化，而在稳定部位保持模型稳定性**，从而实现整体预测质量的提升。

### 消融实验：关键超参数的敏感性分析

**动量系数 η 与学习率 λ** (Table 4)：全局 IN 统计的指数移动平均动量 η 控制历史统计的平滑程度。实验表明 η=0.95 时 MPJPE 最低，过小的 η 导致统计波动过大，过大的 η 则使统计滞后于域变化。学习率 λ=1.0e-3 取得最优，过高的学习率（如 1.0e-2）会导致参数更新过激，破坏源知识。

**峰值检测阈值 τ_peak 与窗口大小 w** (Table 5)：τ_peak=12（标准差倍数）和 w=36 的组合取得最佳平衡。过低的阈值会导致频繁的知识恢复，使模型退化为源模型；过高的阈值则可能漏检真实的域偏移峰值，使受影响部位持续使用不适配的参数。窗口大小影响峰值检测的平滑性——过小的窗口对噪声敏感，过大的窗口则延迟响应。

### 失败模式与局限性

尽管 TT-HA 在实验中表现出色，其设计仍存在以下局限：

1. **源域依赖**：解剖参数分解和选择性恢复均依赖源域有标签数据的预训练，无法在完全无源域的场景下冷启动。这限制了其在隐私敏感或源数据不可访问场景中的应用。
2. **计算开销**：信息论敏感度分析（Eq. 1）和基于 EMD 的域偏移量化（Eq. 3）需要额外的前向传播和统计计算，可能影响实时性要求较高的应用。
3. **超参数敏感性**：τ_peak、w、η 等关键超参数需要根据数据集手工调整，缺乏自动适配机制。在不同域偏移强度下，固定阈值可能导致次优的自适应策略。
4. **验证范围**：当前仅在三维人体姿态预测任务上验证，未探索对二维姿态估计、一般时序运动预测或非人体运动数据的泛化性。

### 开放问题与未来方向

从实验结果和局限性出发，以下方向值得进一步探索：

- **自适应解剖粒度**：当前五段划分（左/右臂、左/右腿、躯干）是固定的，能否根据任务或数据特性自动学习更细粒度（如手部、足部独立）或更粗粒度的划分？
- **阈值自学习**：τ_peak 和 w 的自动调整机制（如基于域偏移历史的自适应阈值）可能进一步提升方法的鲁棒性。
- **架构拓展**：TT-HA 的核心思想——解剖段选择性参数恢复——理论上可与 Transformer、扩散模型等更强大的预测架构结合，但其有效性需要实验验证。
- **极端条件下的鲁棒性**：在严重遮挡、低质量或噪声数据下，基于 IN 统计的域偏移检测是否仍然可靠？可能需要引入额外的置信度估计机制。

### 补充图表

![[assets/figures/papers/paper_list_l1006_https_openaccess_thecvf_com_content_CVPR2026_html_Cui_Anatomical_Domain/figures/007_Table_4.jpg]]
*Table 4: Momentum η and learning rate λ*

![[assets/figures/papers/paper_list_l1006_https_openaccess_thecvf_com_content_CVPR2026_html_Cui_Anatomical_Domain/figures/008_Table_5.jpg]]
*Table 5: Impact of threshold*

## 方法谱系与知识库定位

### 1. 与持续测试时自适应方法的关系

TT-HA 直接继承并改进了持续测试时自适应（CTTA）范式。CTTA 的核心挑战在于目标域分布随时间不断变化，模型需在不访问源数据的前提下持续更新，同时避免灾难性遗忘。当前最佳的 CTTA 基线 **HoCoTTA**（，CVPR 相关工作）采用全身体统一的参数划分与自适应策略，将人体视为均质整体进行批量归一化统计更新和熵最小化微调。TT-HA 的关键突破在于揭示并利用了人体运动的**解剖异质性**——域偏移并非均匀分布于全身，而是集中在某些解剖段（如手臂），其他部位（如躯干）则相对稳定。这一洞察通过 Figure 1 的 t-SNE 可视化得到验证：源域（H3.6M）与目标域（GRAB）的右腿和躯干特征分布高度接近，而全身体特征分布则明显分离。

基于此，TT-HA 将 HoCoTTA 的全局自适应框架重构为**部位级选择性自适应**，核心差异体现在三个维度：

- **参数划分粒度**：从全局域敏感/不变参数划分升级为五个解剖段（左/右臂、左/右腿、躯干）加共享参数的六组结构，每组参数的归属由信息论稳定性度量 $S_p(\Theta^i)$（Eq. 1）的 $\tau$-分位数（$\tau=0.2$）决定。
- **域偏移检测机制**：用实例归一化（IN）替代批量归一化（BN），以指数移动平均维护全局 IN 统计（Eq. 2），并通过 EMD 的闭式解（Eq. 3）量化部位级域偏移 $\omega_p^{(t)}$，而非依赖全身体 BN 统计。
- **自适应策略**：引入滑动窗口 z-score 峰值检测（窗口 $w=36$，阈值 $\tau_\text{peak}=12$ 标准差），对域偏移显著部位执行**选择性知识恢复**（Eq. 4），将参数重置为源预训练值；对稳定部位则以自监督时间一致性损失（Eq. 6）和空间骨骼长度一致性损失（Eq. 7）进行微调（Eq. 5）。

### 2. 与人体姿态预测基线的关系

在预测架构层面，TT-HA 的方法设计是模型无关的，可与多种基线骨干网络结合。论文实验覆盖了三类代表性基线：

- **时空图卷积方法**：**LTD**，利用图卷积捕捉人体关节的空间依赖与时序动态。
- **渐进优化方法**：**PGBIG**，通过渐进猜测与迭代优化提升长时预测精度。
- **纯 MLP 方法**：**siMLPe**，以极简的多层感知机架构实现高效预测。

TT-HA 的贡献不在于提出新的预测架构，而在于为上述任意骨干网络提供一种**解剖感知的测试时自适应机制**。实验表明（Table 1），TT-HA 在 H3.6M、CMU Mocap、GRAB、RICH 四个数据集上均优于所有基线的原始性能及其与 HoCoTTA 结合后的版本，验证了解剖针对性自适应的通用增益。

### 3. 与测试时个性化自适应方法的关系

**H/P-TTP** 提出了测试时个性化自适应（TTP）范式，通过在测试时利用少量目标域样本对模型进行个性化微调来应对域偏移。TT-HA 与 TTP 的区别在于：

- **自适应粒度**：TTP 对全模型或全局参数子集进行统一更新，TT-HA 则按解剖段进行差异化处理。
- **遗忘抑制机制**：TTP 依赖经验重放或正则化来缓解灾难性遗忘，TT-HA 通过选择性知识恢复直接将被域偏移冲击部位的参数重置为源值，更直接且无需存储历史样本。
- **域偏移感知**：TTP 缺乏显式的域偏移量化模块，TT-HA 的 EMD 驱动检测机制使其能精确识别何时、何部位需要干预。

### 4. 适用边界与局限

TT-HA 的有效性建立在以下前提之上，这些前提也划定了其适用边界：

1. **源域预训练依赖**：方法需要源域有标签数据完成预训练，无法在完全无源域场景下启动。这是 CTTA 范式的固有约束，而非 TT-HA 独有。
2. **解剖段划分的静态性**：五个解剖段的划分是预定义的，基于人体运动学常识。对于非人形运动数据或具有不同拓扑结构的对象，该划分方案无法直接迁移。
3. **超参数敏感性**：$\tau_\text{peak}$、$w$、$\eta$ 等超参数需根据数据集手工调整（Tables 4–5），缺乏自适应调节机制。消融实验表明，动量 $\eta=0.95$、学习率 $\lambda=1.0\times10^{-3}$ 时 MPJPE 最低，峰值阈值 $\tau_\text{peak}=12$、窗口 $w=36$ 取得最佳平衡，但这些最优值可能随域偏移模式变化而漂移。
4. **计算开销**：解剖参数分解的信息论敏感度分析（需在源域上多次前向传播加噪声）和测试时的 EMD 逐部位计算增加了额外成本，可能影响实时性要求高的应用场景。
5. **数据质量依赖**：基于 IN 统计的域偏移检测假设输入数据能提供有意义的统计量。在极端遮挡、严重噪声或低帧率条件下，IN 统计的可靠性可能下降，进而影响 $\omega_p^{(t)}$ 的准确性。

### 5. 开放问题

TT-HA 揭示的解剖异质性自适应范式为未来研究开辟了若干方向：

- **自适应解剖粒度**：当前五个解剖段是固定划分，能否通过学习或聚类自动发现最优的解剖段粒度？对于不同运动类型（如游泳、舞蹈），最优划分可能不同。
- **跨任务泛化**：选择性本体知识恢复机制是否可拓展到其他持续学习任务，如持续目标检测、持续语义分割中的类别增量或域增量场景？
- **鲁棒域偏移检测**：在低质量数据条件下，如何增强基于 IN 统计的域偏移检测鲁棒性？是否可融合运动学约束（如关节角度范围、速度上限）作为辅助信号？
- **架构协同设计**：TT-HA 目前与 GCN/MLP 骨干结合，与 Transformer 等具备自注意力机制的架构结合时，解剖段参数划分是否能与注意力头形成更精细的对应关系？
- **无源域自适应**：能否通过预训练扩散模型或运动先验来替代源域预训练模型，使 TT-HA 在完全无源域条件下也能启动？

## 原文 PDF

![[paperPDFs/CVPR_2026/Anatomical_Domain_Shifts_Test_time_Heterogeneous_Adaptation_for_3D_Human_Pose_Prediction.pdf]]