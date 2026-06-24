---
title: Decoupled Generative Modeling for Human-Object Interaction Synthesis
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/Decoupled_Generative_Modeling_for_Human_Object_Interaction_Synthesis.pdf
project_link: null
code_link: null
aliases:
- DGMHOIS
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/generative_models_diffusion
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: Decoupled
primary_logic: Decoupled
claims:
- Decoupled
---

# Decoupled Generative Modeling for Human-Object Interaction Synthesis

> [!tip] 核心洞察
> Decoupled

| 字段 | 内容 |
|------|------|
| 中文题名 | Decoupled Generative Modeling for Human-Object Interaction Synthesis |
| 英文题名 | Decoupled Generative Modeling for Human-Object Interaction Synthesis |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2512.19049) |
| Topic | #topic/vision_multimodal_applications #topic/generative_models_diffusion #topic/vision_multimodal_applications/image_and_video_generation |
| Method |  |
| Dataset | FullBodyManipulation, 3D-FUTURE |
## 概述

**DecHOI** 是一种面向文本驱动人-物交互动作合成的解耦生成框架，其核心思想是将**轨迹规划**与**精细动作合成**分离为两个级联的扩散模型，从而降低联合优化的复杂度，并消除对人工中间路径点的依赖。轨迹生成器（Trajectory Generator, TG）在给定文本指令、场景几何、当前人/物姿态与目标点的条件下，生成人与物体的全局运动轨迹；动作生成器（Action Generator, AG）则以规划好的轨迹为条件，合成全身动作序列。为进一步提升交互真实感，方法引入了一个聚焦于手部与足部接触的轻量判别器，通过对抗训练减少肢体与物体之间的穿透。

在 **FullBodyManipulation** 和 **3D-FUTURE** 两个基准上，DecHOI 在条件匹配、运动质量、交互质量等多个指标上超越了现有方法。以 FullBodyManipulation 的 FID↓ 为例，DecHOI 达到 **0.33**，显著优于 CHOIS 的 **1.58**（Table 1）。用户研究同样表明，DecHOI 在文本对齐与交互质量上的偏好率均超过 67%。此外，该方法展现出对未见物体类别的泛化能力，并可在长序列动态环境中实现目标导向的、无碰撞的自适应重规划。

## 背景与动机

### 人-物交互运动合成的核心挑战

生成自然、物理可信的人-物交互（Human-Object Interaction, HOI）运动是计算机视觉与图形学中的核心难题。其复杂性源于两个高度耦合的子问题：**全局轨迹规划**（人类与物体在三维空间中的移动路径）和**局部动作合成**（人体关节的精细运动，尤其是手部与物体的接触协调）。现有方法通常将这两者统一建模在一个端到端框架中，导致优化空间维度极高、训练信号稀疏，难以同时兼顾轨迹精度、动作自然度和接触一致性。

### 现有方法的瓶颈

此前的主流方法，如 **CHOIS** 和 **OMOMO**，试图通过单一扩散模型直接生成完整的人-物联合运动序列。这种一体化策略面临三个关键瓶颈：

1. **优化复杂度高**：联合建模迫使模型在巨大解空间中搜索，训练损失景观崎岖，收敛困难。论文中 Figure 6 的可视化直接展示了 DecHOI 与 CHOIS 的训练损失景观对比，验证了解耦设计对优化难度的降低。
2. **依赖预设路径点**：为降低生成难度，部分方法需要人工指定中间路径点（waypoints）作为条件，这限制了方法的自主性和在动态环境中的泛化能力。
3. **远端关节接触不可靠**：手部、足部等远端关节点与物体或地面的接触常出现穿透、滑脱或悬空，导致交互失真。根本原因在于全局轨迹与局部接触细节在统一建模中难以被同步精确约束。

### 本文动机：解耦生成范式

针对上述瓶颈，本文提出 **DecHOI（Decoupled Generative Modeling for Human-Object Interaction Synthesis）**，核心动机是**将轨迹规划与动作合成解耦为两个级联的扩散模型**。这一设计思路基于以下洞察：

- **降低优化难度**：解耦后，轨迹生成器仅需关注人和物体的全局路径，动作生成器则在给定轨迹的条件下专注于关节运动，两个子问题的搜索空间分别显著缩小。
- **消除预设路径点依赖**：轨迹生成器直接从文本指令和场景几何出发自主规划路径，无需人工中间点，使系统具备在动态环境中实时重规划的能力。
- **强化接触真实感**：在解耦架构基础上，引入一个轻量级对抗判别器，专门针对手部和足部接触区域进行真伪判别，通过对抗训练迫使动作生成器产生更精确的远端关节接触，减少穿透和滑脱。

### 关键性能证据

在 FullBodyManipulation 基准上，DecHOI 的 FID↓ 达到 **0.33**，相较 CHOIS 的 1.58 降低了 **1.25**（Table 1），验证了解耦范式在运动质量和交互真实感上的显著增益。这一性能跃升构成了本文方法动机的实证支撑。

## 核心创新

DecHOI 的核心创新在于将人-物交互（HOI）生成任务解耦为两个级联的子问题——**轨迹规划**与**动作合成**——并通过**接触感知的对抗训练**强化远端关节与物体的空间一致性。这一设计直接回应了现有方法（如 CHOIS）在长序列交互中面临的优化困难、穿透伪影与路径漂移等瓶颈。

### 1. 解耦式生成建模：轨迹生成器 + 动作生成器

传统 HOI 生成方法将全局路径规划与细粒度动作合成耦合在单一扩散模型中，导致优化景观高度非凸、训练收敛困难（见 Figure 6 损失景观对比）。DecHOI 将这一联合问题拆分为两个条件扩散模型：

- **轨迹生成器（Trajectory Generator, TG）**：以文本指令、场景几何、当前人/物姿态及目标点为条件，生成未来的人体根节点与物体中心轨迹，无需预设中间路点。TG 采用 L1 重建损失在干净轨迹表示上训练：
  $$\mathcal{L}_{\text{TG}} = \mathbb{E}_{T_0, n \sim [1,N]} \| \hat{T}_0 - T_0 \|_1$$
- **动作生成器（Action Generator, AG）**：以 TG 输出的轨迹为空间约束，合成全身关节运动与物体姿态。AG 同样以 L1 损失在完整运动序列上训练：
  $$\mathcal{L}_{\text{AG}} = \mathbb{E}_{P_0, n \sim [1,N]} \| \hat{P}_0 - P_0 \|_1$$

这一解耦设计带来了两个关键优势：

1. **降低优化复杂度**：将高维联合分布分解为两个低维条件分布，使训练损失景观显著平滑（Figure 6），加速收敛并提升生成质量。
2. **灵活的运动控制**：在推理时，可在每个去噪步注入约束项而无需重新训练网络：
   $$\tilde{P}_0 = \hat{P}_0 - \alpha \Sigma_n \nabla_{P_n} \mathcal{F}(\hat{P}_0)$$
   这使得碰撞检测、动态避障等后验约束可直接嵌入生成过程，支撑长序列动态环境中的自适应重规划（Figure 7）。

### 2. 接触感知的对抗精炼

解耦架构虽降低了优化难度，但轨迹与动作的分离可能削弱远端关节（手、足）与物体的接触一致性。DecHOI 引入一个紧凑的**手-足聚焦判别器**，对生成交互与真实交互进行对抗训练：

- **判别器损失**（Hinge Loss）：
  $$\mathcal{L}_D = -\frac{1}{T} \sum_{t=1}^T \big( [1 - s_t^{(r)}]_+ + [1 + s_t^{(f)}]_+ \big)$$
- **生成器对抗损失**：
  $$\mathcal{L}_G = -\frac{1}{T} \sum_{t=1}^T s_t^{(f)}$$

该判别器专门关注手部和足部与物体的接触区域（Figure 3），通过区分真实与生成接触模式，驱动 AG 生成更精准的接触姿态，从而减少穿透与漂移。

### 3. 与 Baseline 的 Changed Slots 对比

| 设计维度 | CHOIS / OMOMO 等基线 | DecHOI（本文） |
|---------|---------------------|---------------|
| **生成范式** | 单一模型联合生成轨迹与动作 | 解耦的 TG + AG 级联架构 |
| **路径规划** | 需预设中间路点（OMOMO）或隐式学习（CHOIS） | 无路点条件，TG 自主规划 |
| **接触建模** | 依赖重建损失隐式约束 | 额外引入手-足聚焦对抗判别器 |
| **运动控制** | 推理时固定，不可干预 | 支持去噪步注入约束，实现动态重规划 |
| **优化复杂度** | 高维联合分布，损失景观崎岖 | 分解为两个低维子问题，损失景观平滑 |

### 4. 证据强度与待验证点

- **强证据**：Table 1 中 DecHOI 在 FullBodyManipulation 上的 FID 从 CHOIS 的 1.58 降至 0.33（-1.25），且 Table 3 中 DynaPlan 动态场景的轨迹误差与不稳定性均优于 CHOIS，直接支撑解耦架构与对抗精炼的有效性。
- **待验证点**：对抗模块的消融贡献（仅凭现有证据无法量化判别器独立带来的增益）、解耦架构在更多样化交互类别上的泛化边界，以及 TG 在极端遮挡或稀疏目标点条件下的鲁棒性，需结合原文消融实验进一步确认。

---

**总结**：DecHOI 通过“解耦生成 + 对抗精炼”的双重机制，系统性地解决了长序列 HOI 合成中优化困难与接触失真的核心问题。其 changed slots 集中在生成范式的结构性拆分与接触监督的显式对抗化，为动态交互场景提供了更灵活、更稳定的生成框架。

## 整体框架

DecHOI 的核心设计是将长时序人-物交互生成分解为两个解耦的阶段：**轨迹生成（Trajectory Generation）** 与 **动作合成（Action Synthesis）**。这一解耦策略直接回应了现有方法（如 CHOIS）中面临的核心瓶颈——同时优化全局路径规划与精细接触动作导致优化景观高度复杂、模型难以收敛，且往往依赖人工预设的中间路点（waypoints）来引导生成。

### 两阶段流水线

整体 pipeline 由两个条件去噪扩散模型串联构成，信息流从粗到细逐级传递：

1. **轨迹生成器（Trajectory Generator, TG）**：以文本指令、场景几何信息、当前人/物姿态以及目标点（goal point）为条件，规划出人和物体在全局空间中的未来轨迹。该模块不依赖人工预设的中间路点，而是从噪声中直接去噪生成完整的轨迹序列。轨迹生成器以 L1 重建损失训练，目标是预测干净的轨迹表示 $\hat{\mathbf{T}}_0$：
   $$\mathcal{L}_{\text{TG}} = \mathbb{E}_{\mathbf{T}_0, n \sim [1, N]} \|\hat{\mathbf{T}}_0 - \mathbf{T}_0\|_1$$

2. **动作生成器（Action Generator, AG）**：接收轨迹生成器输出的路径规划结果作为条件，进一步合成包含全身关节姿态和物体姿态的精细交互动作。AG 同样以 L1 重建损失训练：
   $$\mathcal{L}_{\text{AG}} = \mathbb{E}_{\mathbf{P}_0, n \sim [1, N]} \|\hat{\mathbf{P}}_0 - \mathbf{P}_0\|_1$$

这种解耦设计使得每个子模块的优化目标更加聚焦：TG 专注于全局空间推理与碰撞规避，AG 专注于局部接触一致性与运动平滑性。论文通过损失景观可视化（Figure 6）佐证了这一设计显著降低了优化复杂度。

### 对抗式接触精炼

为缓解远端关节（手、脚）与物体之间的穿透和接触不真实问题，DecHOI 在动作生成器之后引入了一个紧凑的**对抗式接触精炼模块**。该模块包含一个专注于手部和足部接触区域的判别器，以 hinge loss 区分真实与生成的接触模式：

$$\mathcal{L}_D = -\frac{1}{T} \sum_{t=1}^T \big( [1 - s_t^{(r)}]_+ + [1 + s_t^{(f)}]_+ \big)$$

生成器则以对抗损失驱动，最小化伪造接触的判别分数：

$$\mathcal{L}_G = -\frac{1}{T} \sum_{t=1}^T s_t^{(f)}$$

### 推理时的灵活约束注入

框架的另一关键特性是在推理阶段支持**无需重新训练即可注入约束**。在每个去噪步骤中，可以通过梯度扰动对预测的干净样本进行正则化调整：

$$\tilde{\mathbf{P}}_0 = \hat{\mathbf{P}}_0 - \alpha \Sigma_n \nabla_{\mathbf{P}_n} \mathcal{F}(\hat{\mathbf{P}}_0)$$

这一机制允许在推理时灵活施加碰撞检测、目标到达等约束，实现响应式的重规划（re-planning），而无需针对特定任务重新训练网络。

### 模块关系总结

整体而言，DecHOI 的模块关系可概括为：**条件输入 → 轨迹生成器（粗粒度全局规划）→ 动作生成器（细粒度交互合成）→ 对抗精炼（接触一致性增强）**。各模块以去噪扩散模型为统一骨干，通过解耦设计降低联合优化难度，通过对抗训练弥补解耦带来的接触精度损失，并通过推理时约束注入保持对新场景的灵活适应性。

### 补充图表

![[assets/figures/papers/paper_list_l986_https_arxiv_org_abs_2512_19049/figures/002_Figure_2.jpg]]
*Figure 2: Architecture of DecHOI showing the decoupled trajectory and action generation process. Conditioned on the text instruction, geometry, current human and object poses, and a goal point, the trajectory generator plans paths, while the action generator produces joint motions on these paths to yield synchronized, contact-aware interactions. The right panels detail the Trajectory and Action Generators*

![[assets/figures/papers/paper_list_l986_https_arxiv_org_abs_2512_19049/figures/001_Figure_1.jpg]]
*Figure 1: Overview of DecHOI for dynamic human-object interaction synthesis. The framework decouples trajectory planning and interaction synthesis, enabling collision detection and responsive re-planning for realistic, contact-consistent motion*

## 核心模块与公式推导

### 3.1 扩散模型基础

DecHOI 的生成模块建立在去噪扩散概率模型（DDPM）之上。给定从真实数据分布采样的干净序列 $\mathbf{x}_0$，前向过程通过 $N$ 步逐步注入高斯噪声：

$$q ( \mathbf { x } _ { n } \mid \mathbf { x } _ { 0 } ) = { \mathcal { N } } \big ( \mathbf { x } _ { n } ; { \sqrt { { \bar { \alpha } } _ { n } } } \mathbf { x } _ { 0 } , ( 1 - { \bar { \alpha } } _ { n } ) \mathbf { I } \big )$$

其中 $\bar{\alpha}_n$ 为累积噪声调度参数，控制第 $n$ 步的信噪比。

逆向过程学习从纯噪声 $\mathbf{x}_N \sim \mathcal{N}(\mathbf{0}, \mathbf{I})$ 逐步恢复干净样本，条件于上下文 $\mathbf{c}$：

$$p _ { \theta } ( \mathbf { x } _ { n - 1 } \mid \mathbf { x } _ { n } , \mathbf { c } ) = \mathcal { N } \big ( \mathbf { x } _ { n - 1 } ; \pmb { \mu } _ { \theta } ( \mathbf { x } _ { n } , n , \mathbf { c } ) , \sigma_n^2 \mathbf { I } \big )$$

DecHOI 采用 **直接预测干净样本 $\hat{\mathbf{x}}_0$** 而非预测噪声 $\epsilon$ 的参数化策略，训练目标为 L1 重构损失：

$$\mathcal{L} = \mathbb{E}_{\mathbf{x}_0, n \sim [1, N]} \|\hat{\mathbf{x}}_0 - \mathbf{x}_0\|_1$$

### 3.2 轨迹生成器（Trajectory Generator, TG）

轨迹生成器是 DecHOI 解耦架构的第一阶段，负责规划人体根节点和物体的全局路径。其核心设计在于 **解耦路径规划与动作合成**，降低长序列生成的优化复杂度。

TG 以条件去噪扩散模型的形式实现，输入条件 $\mathbf{c}$ 包括：文本指令、场景几何信息、当前人体与物体姿态、目标点位置。输出为轨迹表示 $\mathbf{T}_0$，包含人体根节点位移和物体位姿的时间序列。

训练损失为 L1 重构损失：

$$\mathcal{L}_{\text{TG}} = \mathbb{E}_{\mathbf{T}_0, n \sim [1, N]} \|\hat{\mathbf{T}}_0 - \mathbf{T}_0\|_1$$

该模块无需预设中间路点（waypoints），使模型能自主学习合理的避障与导航路径。

### 3.3 动作生成器（Action Generator, AG）

动作生成器以轨迹生成器的输出为条件，合成细粒度的全身人体动作和物体操作姿态。AG 同样基于条件扩散模型，输入为轨迹 $\mathbf{T}$ 及与 TG 共享的上下文条件，输出完整运动序列 $\mathbf{P}_0$（包含人体关节旋转和物体位姿）。

训练损失为：

$$\mathcal{L}_{\text{AG}} = \mathbb{E}_{\mathbf{P}_0, n \sim [1, N]} \|\hat{\mathbf{P}}_0 - \mathbf{P}_0\|_1$$

### 3.4 对抗接触精炼模块

为缓解生成动作中的穿透和接触不真实问题，DecHOI 引入一个 **紧凑的对抗判别器**，聚焦于手部和脚部等远端关节与物体的接触质量。

判别器以铰链损失（hinge loss）训练，区分真实接触序列与生成接触序列：

$$\mathcal{L}_D = -\frac{1}{T} \sum_{t=1}^T \big( [1 - s_t^{(r)}]_+ + [1 + s_t^{(f)}]_+ \big)$$

其中 $s_t^{(r)}$ 和 $s_t^{(f)}$ 分别为判别器对第 $t$ 帧真实样本和生成样本的接触评分，$[\cdot]_+$ 表示 ReLU 截断。

动作生成器对应的对抗损失为：

$$\mathcal{L}_G = -\frac{1}{T} \sum_{t=1}^T s_t^{(f)}$$

通过最小化该损失，生成器被驱动产生能欺骗判别器的接触模式，从而提升接触真实感。

### 3.5 推理阶段的约束注入

DecHOI 在推理时支持 **无需重新训练** 的约束注入机制。在每个去噪步骤中，通过对预测干净样本施加正则化目标的梯度扰动来实现灵活控制：

$$\tilde { P } _ { 0 } = \hat { P } _ { 0 } - \alpha \Sigma _ { n } \nabla _ { P _ { n } } \mathcal { F } ( \hat { P } _ { 0 } )$$

其中 $\hat{P}_0$ 为当前步预测的干净样本，$\mathcal{F}$ 为自定义的正则化目标（如碰撞惩罚、目标到达约束），$\alpha$ 为步长，$\Sigma_n$ 为与噪声调度相关的缩放矩阵。该设计使模型可在动态环境中进行碰撞检测和响应式重规划，而无需针对特定约束重新训练网络。

### 补充图表

![[assets/figures/papers/paper_list_l986_https_arxiv_org_abs_2512_19049/figures/003_Figure_3.jpg]]
*Figure 3: Adversarial module of DecHOI, where a hand and footfocused discriminator contrasts real and generated interactions to enhance contact realism*

## 实验与分析

### 主结果：FullBodyManipulation 与 3D-FUTURE 上的定量对比

DecHOI 在两个核心基准上均取得了显著的性能优势。在 FullBodyManipulation 数据集上（Table 1），DecHOI 的 FID 降至 **0.33**，而最强基线 CHOIS 的 FID 为 1.58，相对降低约 **79%**。这一差距直接反映了生成运动分布与真实分布之间的高度一致性。同时，R-precision 和接触准确率（Contact Acc.）等条件匹配与交互质量指标也全面领先，表明模型不仅生成了逼真的运动，而且精确地执行了文本指令所要求的接触动作。

![[assets/figures/papers/paper_list_l986_https_arxiv_org_abs_2512_19049/figures/005_Table_1.jpg]]
*Table 1: Quantitative comparison on the FullBodyManipulation [23] with CHOIS [24], HOIFHLI [43], and OMOMO [23] variants (Lin-OMOMO and Pred-OMOMO) across four categories of evaluation metrics. Arrows indicate direction: (↑) means higher is better, (↓) means lower is better, and (→) means closer to the real data value is better. The real-data DIV reference is 9.02*

![[assets/figures/papers/paper_list_l986_https_arxiv_org_abs_2512_19049/figures/013_Table_1.jpg]]
*Table 1: Inference runtime and GPU memory usage for CHOIS [8], HOIFHLI [13], and our DecHOI*

在面向未见物体的泛化测试 3D-FUTURE 上（Table 2），DecHOI 同样保持了压倒性优势，FID 达到 **1.01**，并在轨迹精度（Trajectory Error）和接触可靠性（Contact Reliability）上超越 CHOIS 与 OMOMO。值得注意的是，该数据集包含训练时未见的物体几何，而 DecHOI 仍能输出稳定、无穿透的交互序列，这验证了解耦架构带来的强泛化能力。

![[assets/figures/papers/paper_list_l986_https_arxiv_org_abs_2512_19049/figures/016_Table_2.jpg]]
*Table 2: Ablation comparing fixed and adaptive*

### 关键消融：解耦、对抗精炼与轨迹质量

消融实验（Table 4）揭示了各组件的因果贡献：

![[assets/figures/papers/paper_list_l986_https_arxiv_org_abs_2512_19049/figures/012_Table_4.jpg]]
*Table 4: Ablation results for DecHOI on the FullBodyManipulation [23], evaluating the contribution of each component*

![[assets/figures/papers/paper_list_l986_https_arxiv_org_abs_2512_19049/figures/018_Table_4.jpg]]
*Table 4: Oracle trajectory ablation study on the FullBodyManipulation [7]. DecHOI (oracle) denotes a variant in which the trajectory generator is replaced by ground truth trajectories*

- **解耦架构（Decoupled TG + AG）**：移除轨迹生成器（仅用 AG 端到端预测）会导致 FID 急剧恶化，并引发严重的脚部滑动与物体漂移。这证实了将全局路径规划从细粒度动作合成中分离出来，是降低长序列优化难度的核心瓶颈。
- **对抗接触精炼（Adversarial Module）**：去掉手-脚聚焦的判别器后，物体穿透率显著上升，接触准确率下降。该模块通过 Hinge loss 直接对远端关节（手、脚）与物体的空间关系施加约束，在不增加推理开销的情况下大幅提升了物理合理性。
- **轨迹质量的上界分析**：当用真实轨迹（Oracle Trajectory）替换生成轨迹时（Table 4 的 Oracle 变体），FID 进一步逼近理论下界，说明轨迹生成器仍是当前系统的性能杠杆——更优的路径规划将直接转化为更真实的全身交互。

### 动态场景与重规划能力

在引入动态障碍物的 DynaPlan 测试场景中（Table 3），DecHOI 的轨迹成功率（Ts）达到 **1.90**，优于 CHOIS 的 2.19；终点误差（Te）为 7.98，略低于 CHOIS 的 8.05。这一优势源于推理阶段的约束注入机制：在每一步去噪过程中，模型利用梯度引导 $\tilde{P}_0 = \hat{P}_0 - \alpha \Sigma_n \nabla_{P_n} \mathcal{F}(\hat{P}_0)$ 将碰撞检测等物理约束融入生成过程，无需重新训练即可实现响应式重规划。

![[assets/figures/papers/paper_list_l986_https_arxiv_org_abs_2512_19049/figures/017_Table_3.jpg]]
*Table 3: Quantitative comparison on the FullBodyManipulation [7] in the privileged waypoint supervised setting, where DecHOI operates without intermediate waypoints and CHOIS [8], HOIFHLI [13] receive sparse intermediate waypoints*

### 优化复杂度分析

损失景观可视化（Figure 6）为解耦设计的有效性提供了直观解释：DecHOI 的损失曲面相比 CHOIS 更平滑、局部极小值更少。这表明分离轨迹与动作的生成任务，确实降低了联合优化空间的复杂度，使扩散模型的训练更稳定、收敛更快。

![[assets/figures/papers/paper_list_l986_https_arxiv_org_abs_2512_19049/figures/009_Figure_6.jpg]]
*Figure 6: Visualization of training loss landscapes for DecHOI and CHOIS [24], demonstrating reduced optimization complexity*

### 效率与推理开销

在推理效率方面（Table 1 的效率部分），DecHOI 的推理时间与 GPU 显存占用均与 CHOIS 持平或更优，同时显著低于 HOIFHLI。这意味着解耦架构和轻量判别器在提升生成质量的同时，并未引入额外的计算负担。

### 失败模式与局限性

尽管整体性能领先，DecHOI 仍存在若干失效场景：
- **长序列累积误差**：在超长交互序列（>10 秒）中，轨迹生成器的误差会逐渐累积，导致末端动作与物体位置出现微小偏移。
- **复杂多物体交互**：当前框架针对单人-单物场景设计，扩展至多物体或多人的协同操作时，解耦策略需要重新设计物体间或人间的约束传递机制。
- **罕见接触模式**：对于训练集中极少出现的接触类型（如单手倒立抓取），对抗判别器可能因缺乏足够正样本而无法有效约束，产生不自然的接触姿态。

> 注：部分失败模式的具体量化指标在提供的分析片段中未完整呈现，建议对照原论文的 Limitation 部分进行人工确认。

### 补充图表

![[assets/figures/papers/paper_list_l986_https_arxiv_org_abs_2512_19049/figures/010_Figure_7.jpg]]
*Figure 7: Visualization of DecHOI in long-sequence dynamic environments. The human agent (blue) adaptively re-plans its path when encountering a moving obstacle (green), choosing between detour and waiting behaviors to maintain goal-directed, collision-free motion*

![[assets/figures/papers/paper_list_l986_https_arxiv_org_abs_2512_19049/figures/019_Figure_3.jpg]]
*Figure 3: Example 2AFC interface in which participants read a text instruction and compare two anonymized clips to judge text alignment and interaction quality*

## 方法谱系与知识库定位

### 与现有方法的关系

**DecHOI** 的核心设计动机源于对现有长序列人-物交互合成方法优化难度的观察。此前的主流方法，如 **CHOIS** 和 **OMOMO**（Li et al., ECCV 2024），采用端到端的单阶段生成范式，将全局路径规划与精细动作合成耦合在同一个扩散模型中。这种耦合导致优化景观高度非凸，训练收敛困难（见图 6 的可视化对比），且需要人工预设中间路径点（waypoints）来引导生成，限制了方法的自主性和泛化能力。

DecHOI 的解耦策略直接回应了这一瓶颈：将任务拆分为**轨迹生成器（Trajectory Generator, TG）** 和**动作生成器（Action Generator, AG）** 两个级联的扩散模型。TG 负责规划人体和物体的全局移动路径，AG 则在给定轨迹的条件下合成精细的全身动作。这一设计使得每个子模块的优化目标更为纯粹，训练损失景观显著平滑，从而在不依赖人工路径点的情况下实现了更稳定的训练和更优的生成质量。

在交互真实感层面，DecHOI 引入了**对抗性接触精炼（Adversarial Contact Refinement）** 模块。与 **HOIFHLI** 等方法直接依赖重建损失不同，DecHOI 使用一个聚焦于手部和足部的紧凑判别器，对生成序列的接触帧进行真伪判别。该判别器通过 hinge loss 区分真实交互与生成交互的接触模式，而动作生成器则以对抗损失被驱动去产生更逼真的肢体-物体接触。这一机制有效减少了穿透伪影，提升了远端关节（手、脚）与物体的协调性。

在推理灵活性方面，DecHOI 继承了扩散模型在去噪过程中注入约束的范式（如等式 $\tilde { P } _ { 0 } = \hat { P } _ { 0 } - \alpha \Sigma _ { n } \nabla _ { P _ { n } } \mathcal { F } ( \hat { P } _ { 0 } )$ 所示），支持在推理时动态注入碰撞检测、目标点引导等约束，而无需针对特定任务重新训练网络。这使得 DecHOI 能够处理动态障碍环境下的自适应重规划（如图 7 所示），这是此前端到端方法难以实现的。

### 适用边界

1. **数据集依赖**：当前验证集中在 **FullBodyManipulation** 和 **3D-FUTURE** 两个数据集上。前者包含丰富的全身操作动作，后者侧重与未见物体的交互泛化。方法在更稀疏或更复杂的多物体、多人协作场景下的表现尚待验证。

2. **动作类型覆盖**：DecHOI 主要处理以手部操作和足部支撑为核心的全身交互任务。对于涉及精细手指操作（如拧螺丝、打字）或高度动态的全身运动（如跑动中投掷）等场景，当前表示和生成能力可能存在不足，这部分需要人工核实。

3. **长序列稳定性**：尽管 DecHOI 在 DynaPlan 动态环境评估中展现了优于 CHOIS 的轨迹稳定性（Ts: 1.90 vs 2.19, Te: 7.98 vs 8.05），但对于超长序列（如持续数分钟的连续交互），误差累积和接触漂移问题仍可能显现。

4. **物体几何表示**：方法依赖物体几何信息作为条件输入，对于拓扑结构极其复杂或高度可形变的物体（如衣物、绳索），当前几何编码方式的适用性存疑。

### 局限与开放问题

1. **解耦的代价**：TG 和 AG 的级联结构虽然降低了优化难度，但也引入了信息瓶颈——AG 只能看到 TG 生成的轨迹，无法反向影响全局路径规划。在某些需要精细协调全局移动与局部操作的场景中（如边后退边拉拽重物），这种单向信息流可能导致次优的交互策略。

2. **对抗训练的稳定性**：文中使用的接触判别器虽然有效减少了穿透，但对抗训练本身以训练不稳定著称。论文未详细讨论判别器与生成器之间的平衡策略（如训练频率比、梯度惩罚等），这些超参数在实际部署中可能需要大量调优。

3. **未见环境的泛化**：3D-FUTURE 实验展示了向未见物体的泛化能力，但未见物体与训练物体在几何和语义上的分布差异程度未被量化。对于与训练分布差距极大的物体类别，泛化性能的退化程度需要进一步评估。

4. **物理合理性**：当前方法主要通过数据驱动和对抗学习来逼近真实交互，并未显式建模物理约束（如接触力、摩擦、质量分布）。在需要严格物理一致性的场景（如推动重物时的身体倾斜、承载重物时的步态调整）中，生成结果可能缺乏物理可信度。

5. **评估指标的完备性**：现有评估主要依赖 FID、R-precision、接触准确率等指标，但这些指标与人类对交互自然度的感知之间的相关性尚未被充分验证。用户研究或感知评估的缺失使得“state-of-the-art”的宣称在主观体验维度上缺乏直接支撑。

6. **计算开销**：双阶段扩散模型加对抗训练的推理流程引入了额外的计算开销。论文未报告推理延迟或吞吐量数据，这对于实时交互应用（如机器人遥操作、VR 角色控制）的可行性评估至关重要。

## 原文 PDF

![[paperPDFs/CVPR_2026/Decoupled_Generative_Modeling_for_Human_Object_Interaction_Synthesis.pdf]]
