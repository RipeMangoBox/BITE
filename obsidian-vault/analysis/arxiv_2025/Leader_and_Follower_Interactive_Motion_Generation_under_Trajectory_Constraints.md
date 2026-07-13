---
title: Leader and Follower Interactive Motion Generation under Trajectory Constraints
type: paper
paper_level: A
venue: arXiv
year: 2025
pdf_ref: paperPDFs/arxiv_2025/Leader_and_Follower_Interactive_Motion_Generation_under_Trajectory_Constraints.pdf
project_link: null
code_link: null
aliases:
- LFIMGPCKSA
- LFIMGUTC
tags:
- arxiv_2025
- topic/vision_multimodal_applications
- topic/generative_models_diffusion
- topic/representation_self_supervised_transfer
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: 在扩散反向过程的运动范围细化中间阶段，通过单向轨迹引导（直接替换根关节轨迹并施加MSE优化）并结合领导者-跟随者范式实现的双人交互同步适配，能够在不重新训练的条件下显著提升轨迹准确性和动作质量。
primary_logic: 扩散模型生成动态过程中存在运动范围细化阶段，其中间阶段是运动方向确立和运动范围稳定的关键窗口，在此阶段施加轨迹引导最为有效；将双人复杂交互解耦为领导者轨迹控制与跟随者运动同步，可简化问题并实现无训练的多约束生成。
claims:
- 在扩散中间阶段（0.7T ≤ t ≤ 0.3T）施加轨迹引导获得最佳语义一致性和动作逼真度。
- 本文方法在FID、R-Precision等指标上显著优于InterGen等基线。
- 联合距离损失有效减少穿透帧数近一半，速度损失防止最后几帧动作同质化。
- 仅使用单人的轨迹作为输入即可达到高性能，同时使用两人轨迹会降低性能。
---

# Leader and Follower Interactive Motion Generation under Trajectory Constraints

> [!tip] 核心洞察
> 扩散模型生成动态过程中存在运动范围细化阶段，其中间阶段是运动方向确立和运动范围稳定的关键窗口，在此阶段施加轨迹引导最为有效；将双人复杂交互解耦为领导者轨迹控制与跟随者运动同步，可简化问题并实现无训练的多约束生成。

| 字段 | 内容 |
|------|------|
| 中文题名 | 轨迹约束下的领导与跟随交互运动生成 |
| 英文题名 | Leader and Follower Interactive Motion Generation under Trajectory Constraints |
| 会议/期刊 | arXiv 2025 |
| Links |  |
| Topic | #topic/vision_multimodal_applications #topic/generative_models_diffusion #topic/representation_self_supervised_transfer #topic/vision_multimodal_applications/image_and_video_generation |
| Method | Leader-Follower Interactive Motion Generation with Pace Controller and Kinematic Synchronization Adapter |
| Dataset | InterHuman |

> [!tip] 效果简介
> - InterHuman 上，R-Precision Top1 ↑ 0.522 vs 0.371 (InterGen) (+0.151)；FID ↓ 5.352 vs 优于所有比较方法 (显著降低)；MM Dist ↓ 3.778 vs 优于所有比较方法 (显著降低)。

## 概要

本文针对**文本到双人交互运动生成中缺乏精确轨迹约束**这一瓶颈，提出了一种无需重新训练的轨迹引导框架。现有方法（如 **InterGen** (Liang et al., IJCV 2024)）仅依赖文本描述来控制运动，常导致轨迹偏差、角色穿透和交互不自然；而单人多动作的轨迹方法又无法处理双人交互，且需重新训练。

核心思路是将复杂双人交互解耦为**领导者-跟随者（Leader-Follower）动态**：先通过 **Pace Controller** 在扩散去噪的中间阶段直接替换并优化领导者的根关节轨迹，再通过 **Kinematic Synchronization Adapter** 检测碰撞并调整跟随者运动以实现同步。这一设计的关键洞察在于：扩散模型生成过程中存在一个**运动范围细化阶段**（约 0.7T 至 0.3T），在此窗口内施加轨迹引导最为有效。

实验表明，该方法在 InterHuman 数据集上显著优于 InterGen 等基线：**R-Precision Top1** 从 0.371 提升至 0.522，**FID** 降至 5.352，同时推理时间仅增加约 4 秒。消融实验进一步验证了中期干预策略、关节距离损失和速度损失各自的有效性。



### 双人交互运动生成的任务困境

生成自然、语义一致的双人交互运动是计算机视觉与图形学中的核心挑战。现有方法大致分为两类：**纯文本驱动**的交互生成与**轨迹约束的单人**运动生成，但两者均难以同时满足精确轨迹控制与自然交互的需求。

基于文本的双人交互模型，如 **InterGen**（Liang et al., IJCV 2024），仅依赖文本描述来控制角色的空间关系与动作语义。然而，文本对轨迹的描述能力天然模糊——"两人并肩行走"无法精确指定行走路径的曲率、步幅或相对位置。这导致生成的运动常出现**轨迹偏离、角色穿透**等不自然现象（Figure 1a）。另一方面，部分单人运动生成方法（如 **MDM**, Tevet et al., ICLR 2023）支持 3D 轨迹输入，但需要为每个新轨迹条件重新训练模型，且完全无法建模双人之间的交互约束（Figure 1b）。

### 核心瓶颈：无训练的精确轨迹约束

上述两类方法的根本瓶颈在于：**现有文本到双人交互运动生成模型缺乏对精确轨迹约束的有效支持**，导致运动轨迹不准确、角色穿透、交互不自然，且无法在不重新训练的情况下适应新的轨迹条件。这一瓶颈的本质是双人交互运动的高维耦合性——两人的空间位置、朝向、关节运动相互依赖，直接施加轨迹约束极易破坏生成运动的物理合理性与语义一致性。

### 关键观察：扩散过程中的运动范围细化

本文的核心洞察源于对扩散模型去噪动态的深入观察。如 Figure 2 所示，双人交互运动的扩散生成过程可划分为三个阶段：

- **早期扩散**：噪声水平高，轨迹高度重叠，运动方向未确立；
- **中期阶段**（约 0.7T 至 0.3T）：运动方向确立，运动范围趋于稳定——这是**运动范围细化**的关键窗口；
- **最终阶段**：运动范围已稳定，仅进行细节精修。

这一观察揭示了一个关键结论：**扩散中间阶段是施加轨迹引导的最佳时机**。在此窗口内，运动的方向和范围尚未固化，轨迹干预既能有效约束空间位置，又不会破坏去噪过程的稳定性。

### 本文动机：领导者-跟随者解耦范式

受双人舞蹈中领舞与跟舞的角色分工启发，本文将复杂的双人交互运动解耦为**领导者-跟随者（Leader-Follower）动态**：领导者承担轨迹控制，跟随者则通过运动学同步机制与领导者保持协调。这一解耦将多约束问题简化为单向轨迹控制与交互同步两个子问题，使得**无训练的多约束生成**成为可能。

基于此范式，本文提出一种无训练（training-free）方法，在冻结的扩散模型（以 InterGen 为基础）之上集成 **Pace Controller**（节奏控制器）与 **Kinematic Synchronization Adapter**（运动学同步适配器），在扩散中间阶段实现精确的轨迹引导与自然的交互同步，无需任何额外训练即可适配任意轨迹条件。



## 核心方法与创新机理

本文的核心创新在于将双人交互运动生成解耦为**领导者-跟随者（Leader-Follower）动态范式**，并在此范式下引入两个关键模块——**Pace Controller** 和 **Kinematic Synchronization Adapter**——以无训练（training-free）的方式实现对精确轨迹约束的支持。这一设计从根本上改变了现有双人交互扩散模型（以 **InterGen**（Liang et al., IJCV 2024）为基线）的生成机制，体现在以下三个关键维度的改变：

### 1. 轨迹控制：从无显式约束到单向扩散引导

基线方法 InterGen 仅依赖文本条件生成双人运动，缺乏对精确 3D 轨迹的显式控制能力，导致生成的运动轨迹常偏离预期、在紧密交互场景中产生角色穿透。本文提出的 **Pace Controller** 通过单向扩散引导策略，在去噪过程的特定中间阶段直接干预领导者的根关节轨迹：

- **轨迹替换**：在时间窗口 $[T_1, T_2]$ 内，将当前带噪状态 $x_t$ 中对应的轨迹部分直接替换为输入条件 $x_a^{\mathrm{proj}}$ 的真实轨迹段：
  $$x_t = (x_t \gets x_a^{\mathrm{proj}}) \cdot \mathbb{I}_{[T_1, T_2]}(t) + x_t \cdot \mathbb{I}_{[T_1, T_2]^c}(t)$$

- **轨迹优化**：对每个预测的干净状态 $x_0$，提取其轨迹部分并与目标轨迹计算逐帧 MSE 损失，通过优化函数 $\mathcal{G}_{\mathrm{opt}}$ 进一步修正当前状态：
  $$x_0 = \mathcal{G}_{\mathrm{opt}}(x_0; \|x_0 - x_a^{\mathrm{proj}}(t)\|^2)$$

这一机制使得模型无需重新训练即可适应任意给定的轨迹条件，弥补了 InterGen 在轨迹可控性上的根本缺陷。

### 2. 交互同步：从纯文本交互损失到运动学约束适配

基线方法仅通过文本条件下的扩散损失（DM）和角色对称性损失（RO）来隐式建模双人交互，缺乏对物理交互合理性的显式约束。本文设计的 **Kinematic Synchronization Adapter** 引入了基于运动学的同步机制：

- **冲突检测**：利用 SMPL 模型界定两人的交互域 $\mathcal{D}_a^t$ 和 $\mathcal{D}_b^t$，通过指示器 $\mathcal{C}_t = \mathbb{I}_{|\mathcal{D}_a^t \cap \mathcal{D}_b^t| > 0}$ 检测碰撞；
- **关节距离损失**：当检测到冲突时，通过 $\mathcal{L}_{\mathrm{joint}} = \sum_j \max(0, \delta - \|\mathbf{p}_a(t)(j) - \mathbf{p}_b(t)(j)\|_2)^2$ 惩罚关节距离过近，确保交互空间合理性；
- **速度损失**：通过 $\mathcal{L}_{\mathrm{velocity}}$ 惩罚两人关节速度向量的高相似度，防止跟随者动作与领导者趋于同质化。

消融实验证实，关节距离损失使穿透帧数减少近一半（Figure 7），速度损失有效防止了最终帧的动作同质化（Figure 8）。

### 3. 干预时机：从全时去噪到运动形成窗口精准介入

本文的关键洞察在于识别了扩散去噪过程中的**运动范围细化阶段**（Motion Range Refinement Process）：早期（高噪声、轨迹重叠）、中期（运动方向和范围确立）和晚期（细节精修、运动范围稳定）。实验表明，仅在中期阶段（$0.7T \leq t \leq 0.3T$）施加轨迹引导，可获得最优的语义一致性（R-Precision）和动作逼真度（FID）（Figure 6）。这一发现将轨迹干预从“全时施加”转变为“关键窗口精准介入”，在保证控制效果的同时最小化对生成质量的干扰。

### 创新总结

| 改变维度 | 基线（InterGen） | 本文方法 | 核心机制 |
|---------|-----------------|---------|---------|
| 轨迹控制 | 无显式轨迹约束 | 单向 Pace Controller | 根关节替换 + MSE 优化 |
| 交互同步 | 纯文本损失（DM, RO） | Kinematic Synchronization Adapter | 冲突检测 + 关节距离损失 + 速度损失 |
| 干预时机 | 完整去噪过程 | 运动形成中期（$0.7T$–$0.3T$） | 运动范围细化阶段精准介入 |

这三个维度的协同创新使得本文方法在不重新训练的前提下，在 InterHuman 数据集上取得了显著优于所有基线方法的性能：R-Precision Top1 达到 0.522（InterGen 为 0.371），FID 降至 5.352（Table 1），同时推理时间仅增加约 4 秒（Table 3）。



本文提出一种无训练的**领导-跟随交互运动生成框架**，其核心思想源自交谊舞中的角色分配：将复杂的双人交互运动解耦为**领导者（Leader）的轨迹控制**与**跟随者（Follower）的运动同步**两个子问题。该框架以预训练的双向交互扩散模型 **InterGen**（Liang et al., IJCV 2024）为基础，在不重新训练的前提下，通过两个即插即用的模块实现对精确 3D 轨迹条件的支持。

### Pipeline 总览

整体生成流程如 Figure 3 所示，包含四个核心组件：

![[assets/figures/papers/paper_list_l1690_Leader_and_Follower_Interactive_Motion_Generation_under_Trajectory_Const/figures/003_Figure_3.jpg]]
*Figure 3: Motion Generation Pipeline with Text and Trajectory input. Inspired by partner dance leadership, we first use a Controller to define the leader’s trajectory, and then employ an Adapter to guide the follower’s motion to align with the leader*

1. **冻结的 CLIP-ViT/L14 文本编码器**：将输入的自然语言描述编码为条件嵌入，驱动扩散去噪过程。
2. **基于 Transformer 的双向扩散去噪器**：继承自 InterGen 的协作式去噪架构，采用权重共享的 Transformer 模块（N=8 层，隐维度 1024，8 注意力头），在 1000 步扩散调度下通过 DDIM 采样（50 步，η=0）生成双人运动序列。
3. **Pace Controller（节奏控制器）**：作用于扩散反向过程的**运动范围细化中间阶段**（0.7T ≤ t ≤ 0.3T），单向控制领导者的根关节轨迹。其操作分两步——先直接替换当前状态 $x_t$ 中的轨迹段为输入条件 $x_a^{\mathrm{proj}}$，再对预测的干净状态 $x_0$ 施加逐帧 MSE 优化，确保生成轨迹与给定条件精确一致。
4. **Kinematic Synchronization Adapter（运动学同步适配器）**：基于 SMPL 模型构建冲突检测模块，实时判断两角色交互域是否重叠。仅在检测到穿透时，通过**关节距离损失** $\mathcal{L}_{\mathrm{joint}}$ 与**速度损失** $\mathcal{L}_{\mathrm{velocity}}$ 联合优化跟随者位置，使其在保持交互语义的前提下与领导者对齐。

### 输入输出规范

- **输入**：一段文本描述（如“两人正在跳舞”）+ 任一角色的 3D 根关节轨迹（仅需单人轨迹即可达到最优性能，同时使用双人轨迹反而导致 FID 和 R-Precision 下降）。
- **输出**：一段长度固定、语义一致的双人交互运动序列，领导者的轨迹严格贴合输入条件，跟随者的运动自动同步适配。

### 设计逻辑与关键决策

框架的层级设计体现了一条清晰的因果链：**先确立空间基准，再协调交互关系**。Pace Controller 解决了“运动去哪里”的问题，Kinematic Synchronization Adapter 解决了“两人如何配合”的问题。将轨迹干预限定在扩散中间阶段（而非全程）是该方法的核心洞察——早期阶段噪声过高、运动方向尚未确立，晚期阶段运动范围已稳定、强行干预会破坏细节质量，唯有中期阶段（轨迹形成期）是施加空间约束的最佳窗口。



### 扩散模型基础

本文方法建立在扩散模型框架之上，其前向过程逐步向原始运动数据 $x_0$ 添加高斯噪声，条件分布为：

$$q(x_t | x_0) = \mathcal{N}(\sqrt{\alpha_t} x_0, (1 - \alpha_t) I)$$

其中 $\alpha_t = \prod_{s=1}^{t} (1 - \beta_s)$ 为累计噪声调度系数，$\beta_s$ 控制每步噪声强度。反向去噪过程从纯噪声 $x_T \sim \mathcal{N}(0, I)$ 出发，通过训练好的去噪网络逐步恢复干净运动。

### 运动范围细化过程

本文关键洞察在于：扩散模型的去噪过程并非均匀推进，而是呈现明显的阶段性特征（Figure 2）。早期扩散阶段（$t$ 接近 $T$）噪声较高、轨迹重叠混乱；中间阶段（约 $0.7T \leq t \leq 0.3T$）是运动方向确立和运动范围稳定的关键窗口；晚期阶段则仅对运动细节进行微调。这一发现直接决定了轨迹引导的最佳干预时机。

![[assets/figures/papers/paper_list_l1690_Leader_and_Follower_Interactive_Motion_Generation_under_Trajectory_Const/figures/002_Figure_2.jpg]]
*Figure 2: Motion Range Refinement Process. We visualize the trajectories and human poses at different time steps during the denoising process. The process of interactive motion generation is divided into three stages: early diffusion characterized by high noise and overlapping trajectories, mid-stage stabilization of movement direction and range, and final-stage refinement of motion details with stable motion range*

### Pace Controller：领导者轨迹控制

Pace Controller 采用单向扩散引导策略，确保领导者的根关节轨迹与输入条件一致。其核心操作分两步：

**轨迹替换**：在指定的时间窗口 $[T_1, T_2]$ 内，直接用目标轨迹 $x_a^{\mathrm{proj}}$ 替换当前状态中的对应部分：

$$x_t = (x_t \gets x_a^{\mathrm{proj}}) \cdot \mathbb{I}_{[T_1, T_2]}(t) + x_t \cdot \mathbb{I}_{[T_1, T_2]^c}(t)$$

其中 $\mathbb{I}_{[T_1, T_2]}(t)$ 为指示函数，当 $t$ 处于窗口内时执行替换，否则保持原状态。

**轨迹优化**：对预测的干净状态 $x_0$ 施加 MSE 优化，进一步缩小其轨迹分量与目标轨迹的偏差：

$$x_0 = \mathcal{G}_{\mathrm{opt}}(x_0; \|x_0 - x_a^{\mathrm{proj}}(t)\|^2)$$

该优化仅在运动范围细化过程的中间阶段执行，消融实验（Figure 6）表明，$0.7T \leq t \leq 0.3T$ 的干预窗口使 R-Precision 和 FID 均达到最优。

![[assets/figures/papers/paper_list_l1690_Leader_and_Follower_Interactive_Motion_Generation_under_Trajectory_Const/figures/007_Figure_6.jpg]]
*Figure 6: Impact of different trajectory-guiding period on the Pace Controller. Results show that covering the mid-stage of the Motion Range Refinement Process*

### Kinematic Synchronization Adapter：跟随者运动同步

在领导者轨迹受控的前提下，Kinematic Synchronization Adapter 负责调整跟随者运动以实现自然同步。其核心机制包括：

**冲突检测**：利用 SMPL 模型界定两人交互域 $\mathcal{D}_a^t$ 和 $\mathcal{D}_b^t$，通过指示器判断是否发生重叠：

$$\mathcal{C}_t = \mathbb{I}_{|\mathcal{D}_a^t \cap \mathcal{D}_b^t| > 0}$$

**跟随者位置调整**：仅在检测到冲突时，通过优化函数 $\mathcal{F}_{\mathrm{opt}}$ 调整跟随者状态：

$$x_b^t = \mathbb{I}_{\mathcal{C}_t = \emptyset}(x_b^t) + \mathbb{I}_{\mathcal{C}_t \neq \emptyset}(\mathcal{F}_{\mathrm{opt}}(x_b^t; \mathcal{S}(x_a^t, x_b^t)))$$

**组合损失函数** $\mathcal{S}$ 由两部分构成：

$$\mathcal{S}(x_a^t, x_b^t) = \mathcal{L}_{\mathrm{joint}} + \mathcal{L}_{\mathrm{velocity}}$$

**关节距离损失** $\mathcal{L}_{\mathrm{joint}}$ 惩罚两人关节距离小于阈值 $\delta$ 的情况，保证交互空间合理性：

$$\mathcal{L}_{\mathrm{joint}} = \sum_j \max(0, \delta - \|\mathbf{p}_a(t)(j) - \mathbf{p}_b(t)(j)\|_2)^2$$

消融实验（Figure 7）表明，引入该损失使穿透帧数减少近一半。

![[assets/figures/papers/paper_list_l1690_Leader_and_Follower_Interactive_Motion_Generation_under_Trajectory_Const/figures/009_Figure_7.jpg]]
*Figure 7: Comparison experiment of Joint Loss. Joint Loss effectively adjusts the follower’s position, reducing model clipping*

**速度损失** $\mathcal{L}_{\mathrm{velocity}}$ 惩罚两人关节速度向量的高相似度，防止动作同质化：

$$\mathcal{L}_{\mathrm{velocity}} = \sum_{t=1}^{n-1} \sum_{j=1}^{22} \frac{\|\mathbf{v}_a(t,j)\|_2 \|\mathbf{v}_b(t,j)\|_2}{\|\mathbf{v}_a(t,j)\|_2 \|\mathbf{v}_b(t,j)\|_2} (\mathbf{v}_a(t,j) \cdot \mathbf{v}_b(t,j))$$

消融实验（Figure 8）证实，该损失有效防止了最后几帧跟随者动作与领导者趋同。

![[assets/figures/papers/paper_list_l1690_Leader_and_Follower_Interactive_Motion_Generation_under_Trajectory_Const/figures/010_Figure_8.jpg]]
*Figure 8: Comparison experiment of velocity loss . Velocity loss effectively prevents the follower’s motion from becoming too similar to the leader’s in the final few frames*

### 模块协作流程

整个生成流程（Figure 3）为：冻结的 CLIP-ViT/L4 文本编码器提取文本条件嵌入，共享权重的 Transformer 去噪器执行双向去噪生成。在中间去噪阶段，Pace Controller 单向干预领导者根关节轨迹，Kinematic Synchronization Adapter 同步检测碰撞并调整跟随者运动。两个模块均无需额外训练，推理时间仅增加约 4 秒（Table 3）。



## 实验与关键发现

### 主实验定量结果

我们在 InterHuman 数据集上对本文方法进行了系统评估，并与当前主流的文本到动作生成方法进行了对比，包括单人生成模型 **TEMOS** (Petrovich et al., ECCV 2022)、**T2M** (Guo et al., CVPR 2022)、**MDM** (Tevet et al., ICLR 2023)，以及双人交互生成模型 **ComMDM** (Shafir et al., arXiv 2023)、**RIG** (Tanaka and Fujiwara, ICCV 2023) 和 **InterGen** (Liang et al., IJCV 2024)。评估采用与 InterGen 一致的协议，涵盖语义一致性（R-Precision）、动作逼真度（FID）、运动多样性（Diversity）和模态距离（MM Dist）四个维度，所有结果以均值 ± 标准差报告。

**Table 1** 呈现了各方法的定量对比结果。本文方法在核心指标上均取得最优表现：

- **R-Precision Top1** 达到 0.522，相比基础模型 InterGen 的 0.371 提升了 **+0.151**，表明轨迹引导显著增强了生成动作与文本条件的语义对齐。
- **FID** 降至 5.352，大幅优于所有对比方法，证明引入轨迹约束后生成动作的逼真度有明显提升。
- **MM Dist** 为 3.778，同样处于最佳水平，说明生成动作与真实动作分布之间的特征距离最小。
- **Diversity** 为 7.931，最接近真实数据分布，表明方法在保持多样性的同时未因轨迹约束而丧失生成丰富性。

这些结果表明，在扩散生成过程中嵌入无训练的轨迹引导机制，能够在不牺牲多样性的前提下，同时提升动作的语义一致性和视觉真实感。

### 消融实验

为验证各模块设计的有效性，我们开展了一系列消融实验。

**轨迹引导时段的选择。** 扩散去噪过程呈现出明显的阶段性特征：早期阶段噪声高、轨迹重叠混乱；中期阶段运动方向和范围趋于稳定；后期阶段仅对细节进行微调。**Figure 6** 展示了不同轨迹引导时段对 Pace Controller 性能的影响。实验表明，当引导时段覆盖运动形成阶段（$0.7T \leq t \leq 0.3T$）时，R-Precision 和 FID 同时达到最优。若仅在早期或晚期施加引导，语义一致性或动作逼真度均出现退化。这验证了中期阶段是运动方向和范围确立的关键窗口，在此阶段介入轨迹约束最为有效。

**引导轨迹的角色选择。** **Table 2** 对比了分别使用领导者轨迹、跟随者轨迹以及同时使用双人轨迹作为输入条件的性能差异。结果显示，单独使用任一角色的轨迹均可达到相似的生成质量，R-Precision 和 FID 差异极小。然而，当同时使用两人的轨迹作为输入条件时，FID 和 R-Precision 均出现恶化。这一反直觉现象表明，过强的多轨迹约束可能限制了扩散模型的生成自由度，导致动作与文本语义的偏离，需要在多约束条件下进一步优化。

**运动学同步适配器的损失函数。** **Figure 7** 展示了关节距离损失（Joint Loss）的消融效果。引入该损失后，双人交互中的穿透帧数减少了近一半，有效缓解了基线模型在紧密接触场景下常见的模型裁剪问题。**Figure 8** 则验证了速度损失（Velocity Loss）的作用：未施加该损失时，跟随者在最后几帧的动作趋于与领导者同质化；引入速度损失后，两人的动作保持了合理的差异性，避免了运动模式的高度雷同。

**推理效率。** **Table 3** 对比了各方法的推理时间。Pace Controller 和 Kinematic Synchronization Adapter 的引入仅增加了约 4 秒的额外推理耗时，相对于整体生成过程而言开销可接受，保持了方法的实用性。

### 可视化分析

**Figure 4** 给出了本文方法与基线模型在复杂交互场景下的视觉对比。以“两名武术家对练，一方连续踢击，另一方闪避并快速反击”的文本描述为例，基线方法产生了明显的人物穿透现象（红色圆圈标注），而本文方法通过控制领导者轨迹并引导跟随者进行运动学同步适配，有效解决了这一问题，生成的交互动作自然且贴合文本语义。

**Figure 5** 进一步展示了轨迹引导的灵活性。对于相同的文本输入“两人一起跳舞”，施加不同的轨迹条件后，所有生成序列均能准确贴合给定的轨迹路径，同时保持舞蹈动作的自然感和多样性。这证明了方法无需重新训练即可适应多种轨迹条件的能力。

### 失败模式与局限性

尽管方法在多数场景下表现优异，但仍存在以下不足：

1. **双轨迹约束性能退化。** 如 Table 2 所示，同时使用双人轨迹作为输入条件时，FID 和 R-Precision 均出现下降，可能产生与文本不一致或不自然的运动。这表明当前的运动学同步适配器在处理多轨迹强约束时仍有优化空间。

![[assets/figures/papers/paper_list_l1690_Leader_and_Follower_Interactive_Motion_Generation_under_Trajectory_Const/figures/008_Table_2.jpg]]
*Table 2: Trajectory Guidance for Different Individuals. The performance is similar when using the leader’s or follower’s trajectory as input. However, it decreases when both individuals’ trajectories are used simultaneously*

2. **数据集泛化性未验证。** 所有实验仅在 InterHuman 数据集上进行，尚未在其他交互运动数据集或更多人数场景下测试方法的迁移能力。

3. **精确轨迹依赖。** 方法依赖于精确的 3D 轨迹输入，在实际应用场景中获取此类高精度轨迹可能存在一定难度，限制了方法的直接部署范围。

### 补充图表

![[assets/figures/papers/paper_list_l1690_Leader_and_Follower_Interactive_Motion_Generation_under_Trajectory_Const/figures/004_Table_1.jpg]]
*Table 1: Quantitative Comparisons of Various Methods. Our method outperforms existing approaches in R-Precision, FID, MM Distance, and Diversity, demonstrating superior motion generation quality, greater diversity, and better alignment with textual conditions*

![[assets/figures/papers/paper_list_l1690_Leader_and_Follower_Interactive_Motion_Generation_under_Trajectory_Const/figures/001_Figure_1.jpg]]
*Figure 1: Comparison of Our Task with Previous Works. (a) Interaction methods based on textual input to describe trajectory result in trajectory deviations and interaction errors (as indicated by the red circle); (b) Some methods for single-actor motion generation use 3D trajectories but require retraining and fail to account for inter-person interactions; (c) Our approach leverages precise 3D trajectory and textual input to guide interactive motion generation, achieving consistent trajectory generation without additional retraining*

![[assets/figures/papers/paper_list_l1690_Leader_and_Follower_Interactive_Motion_Generation_under_Trajectory_Const/figures/005_Figure_4.jpg]]
*Figure 4: Visual Comparison with Other Methods. In complex scenarios requiring close contact and interaction, baseline models often produce unnatural interpenetration (as indicated by the red circles). Our approach controls the leader’s trajectory and guides the follower’s actions to align with the leader, thereby effectively addressing these issues*

![[assets/figures/papers/paper_list_l1690_Leader_and_Follower_Interactive_Motion_Generation_under_Trajectory_Const/figures/006_Figure_5.jpg]]
*Figure 5: Demonstration of Trajectory Guidance Effect. For the same input text, “Two people are dancing together,” we provide different trajectory conditions. All generated sequences align with both the trajectory and textual features, resulting in realistic and natural motions*

![[assets/figures/papers/paper_list_l1690_Leader_and_Follower_Interactive_Motion_Generation_under_Trajectory_Const/figures/011_Table_3.jpg]]
*Table 3: Inference time comparison. Our design does not significantly increase the inference time cost*



## 定位与知识库关联

### 1. 领域问题定位

本文解决的核心瓶颈是：**现有文本到双人交互运动生成模型缺乏对精确轨迹约束的有效支持**，常导致运动轨迹不准确、角色穿透、交互不自然，且无法在不重新训练的情况下适应新的轨迹条件。这一问题位于文本条件生成、多智能体运动合成和扩散模型可控生成的交叉地带。

### 2. 与基线方法的关系

#### 2.1 基础模型：InterGen

本文直接构建在 **InterGen**（Liang et al., IJCV 2024）之上。InterGen 是当前双人多动作交互扩散模型的代表性工作，其核心设计包括：

- **合作式 Transformer 去噪器**：采用共享权重的双支路 Transformer 架构，通过对称性处理双人身份互换问题。
- **文本条件交互损失**：利用 DM（Distance Matrix）损失和 RO（Relative Orientation）损失约束双人空间关系，但仅依赖文本条件，缺乏显式的轨迹控制。

本文保留了 InterGen 的冻结 CLIP-ViT/L4 文本编码器和共享权重 Transformer 去噪器作为基础生成骨架，在其上叠加无训练的轨迹控制与运动同步模块。

#### 2.2 单人轨迹运动生成方法

部分工作尝试在单人运动生成中引入 3D 轨迹条件，例如通过重新训练的方式将轨迹嵌入生成模型。然而，这些方法存在两个根本局限：

- **需要重新训练**：每更换轨迹条件都需调整模型参数，缺乏灵活性。
- **无法处理双人交互**：仅关注单角色运动，未建模角色间的空间协调与碰撞避免。

本文的 **Pace Controller** 在无需重新训练的条件下实现轨迹引导，并通过 **Kinematic Synchronization Adapter** 将交互同步纳入统一框架，弥补了上述方法的不足。

#### 2.3 其他双人交互生成方法

- **ComMDM**（Shafir et al., arXiv 2023）：将 MDM 扩展至双人场景，但未显式处理轨迹控制问题。
- **RIG**（Tanaka and Fujiwara, ICCV 2023）：关注双人交互动作生成，但同样缺乏精确轨迹约束机制。

与这些方法相比，本文首次在扩散模型框架内实现了**无训练、可插拔的轨迹约束与交互同步联合控制**。

### 3. 方法谱系中的位置

从方法演进角度看，本文处于以下技术路线的交汇点：

| 技术路线 | 代表工作 | 本文贡献 |
|---------|---------|---------|
| 扩散运动生成 | MDM (Tevet et al., ICLR 2023) | 继承扩散范式，在去噪中间阶段注入轨迹引导 |
| 双人交互建模 | InterGen (Liang et al., IJCV 2024) | 保留基础架构，叠加无训练控制模块 |
| 轨迹条件生成 | 单人重训练方法 | 首次实现双人场景下的无训练轨迹控制 |
| 运动学约束优化 | — | 提出关节距离损失 + 速度损失的同步适配器 |

### 4. 适用边界与局限

#### 4.1 已验证的适用范围

- **数据集**：仅在 InterHuman 数据集上验证，该数据集包含丰富的双人交互动作（舞蹈、武术、日常互动等）。
- **轨迹输入**：依赖精确的 3D 轨迹（根关节位置序列），支持单一角色轨迹输入即可达到高性能。
- **交互类型**：适用于需要紧密接触和空间协调的双人场景（如武术对练、双人舞蹈）。

#### 4.2 已知局限

1. **多轨迹约束性能下降**：当同时使用双人轨迹作为输入条件时，FID 和 R-Precision 均出现恶化（Table 2）。这表明当前框架在处理多约束条件时存在能力瓶颈，可能产生与文本语义不一致或不自然的运动。

2. **泛化能力未验证**：实验仅局限于 InterHuman 数据集，尚未在以下场景中测试：
   - 其他交互运动数据集（如 NTU RGB+D、CHI3D 等）
   - 三人或群体交互运动生成
   - 不同运动风格或极端轨迹条件下的鲁棒性

3. **轨迹获取难度**：方法依赖于精确的 3D 轨迹输入，在实际应用场景（如从视频估计轨迹、用户手绘轨迹）中获取如此精确的轨迹条件可能存在困难。

4. **推理时间开销**：Pace Controller 和 Kinematic Synchronization Adapter 引入约 4 秒额外推理时间（Table 3），虽总体可接受，但在实时应用场景中仍需优化。

### 5. 开放问题

基于当前方法的局限，以下问题值得进一步探索：

1. **多约束条件优化**：如何优化同时约束双人轨迹的条件，以避免对文本语义的偏离和生成质量的下降？可能的思路包括引入自适应权重机制或分阶段约束策略。

2. **框架扩展性**：该领导者-跟随者范式能否扩展到三人或群体交互运动生成，同时保持无训练的特性？群体场景中的角色分配和交互同步将更加复杂。

3. **轨迹条件鲁棒性**：如何提升方法对噪声轨迹或不完整轨迹输入的容忍度，使其适用于更广泛的实际应用场景？

4. **实时性能优化**：能否通过模型蒸馏、轻量化适配器设计或更高效的优化算法进一步降低推理时间开销？



## 原文 PDF

![[paperPDFs/arxiv_2025/Leader_and_Follower_Interactive_Motion_Generation_under_Trajectory_Constraints.pdf]]
