---
title: "ResWorld: Temporal Residual World Model for End-to-End Autonomous Driving"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/ResWorld_Temporal_Residual_World_Model_for_End_to_End_Autonomous_Driving_0aa5048f38c3.pdf
project_link: null
code_link: "https://github.com/mengtan00/ResWorld.git"
aliases:
- ResWorld
tags:
- ICLR_2026
- topic/other_unclear
- topic/other_unclear/general
core_operator: 使用时序残差（temporal residuals）来表示动态物体，让世界模型聚焦于预测动态物体的未来空间分布，同时引入未来引导的轨迹细化（FGTR）模块，通过可变形注意力显式地利用未来BEV特征对先验轨迹进行修正。
primary_logic: 在当前BEV坐标系下预测未来时，静态物体的空间分布可视为不变，因而只需预测动态物体的变化（由时序残差刻画），避免对静态物体的冗余建模；并且通过未来BEV特征与轨迹的交互，既能提升规划精度，又能提供稀疏时空监督防止模型坍塌。
claims:
- ResWorld在nuScenes上L2 Avg 0.65, Collision Avg 0.23，显著优于SSR的0.74和0.31。
- 在NAVSIM navtest split上PDMS达到89.0%，超过此前最好的Transfuser*（87.0%）等所有对比方法。
- 在带ego status的设置下，TR-World和FGTR联合使L2误差降低9.2%，碰撞率降低39.3%（L2 Avg从0.65降至0.59，Collision Avg从0.28降至0.17）。
- 对B_future施加全监督反而使L2 Avg上升0.04，碰撞率上升0.07，验证了FGTR稀疏时空监督优于全局监督。
---

# ResWorld: Temporal Residual World Model for End-to-End Autonomous Driving

> [!tip] 核心洞察
> 在当前BEV坐标系下预测未来时，静态物体的空间分布可视为不变，因而只需预测动态物体的变化（由时序残差刻画），避免对静态物体的冗余建模；并且通过未来BEV特征与轨迹的交互，既能提升规划精度，又能提供稀疏时空监督防止模型坍塌。

| 字段 | 内容 |
|------|------|
| 中文题名 | ResWorld: 面向端到端自动驾驶的时序残差世界模型 |
| 英文题名 | ResWorld: Temporal Residual World Model for End-to-End Autonomous Driving |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=ptGmMFGWmk) · [Code](https://github.com/mengtan00/ResWorld.git) |
| Topic | #topic/other_unclear #topic/other_unclear/general |
| Method | ResWorld |
| Dataset | nuScenes, NAVSIM |

> [!tip] 效果简介
> - nuScenes 上，L2 (m) Avg 0.65 vs 0.74 (-0.09)；Collision Rate (%) Avg 0.23 vs 0.31 (-0.08)。
> - NAVSIM 上，PDMS 89.0 vs 87.0 (+2.0)。

## 概要

端到端自动驾驶系统近年逐步引入世界模型来预测未来场景演变，以辅助规划决策。然而，现有世界模型通常对整个场景（包含静态道路、建筑物等）进行完整建模，导致大量计算被冗余消耗在静态物体上；同时，预测的未来 BEV 特征往往仅作为隐式代理任务，未被显式用于直接优化规划轨迹，造成未来信息的利用效率低下。

针对上述瓶颈，本文提出 **ResWorld**，核心思路是：在当前 BEV 坐标系下预测未来时，静态物体的空间分布可视为不变，因此只需聚焦于动态物体的变化。ResWorld 通过 **时序残差世界模型（TR-World）** 从相邻时间戳的场景查询中提取时序残差，以此刻画动态物体的运动信息，避免对静态场景的冗余建模；同时引入 **未来引导轨迹修正模块（FGTR）**，利用可变形注意力显式地将预测的未来 BEV 特征与先验轨迹交互，对轨迹进行修正，并提供稀疏时空监督以防止世界模型坍塌。

在 nuScenes 和 NAVSIM 两个主流基准上，ResWorld 取得了领先的规划性能：在 nuScenes 上，L2 平均误差降至 0.65 m，碰撞率平均仅 0.23%，显著优于稀疏场景表示方法 **SSR**（Li & Cui, ICLR 2025）的 0.74 m 和 0.31%；在 NAVSIM navtest split 上，PDMS 达到 89.0%，超过此前最优的 **Transfuser***（87.0%）等方法。消融实验进一步验证，TR-World 与 FGTR 联合作用下，L2 误差降低 9.2%，碰撞率降低 39.3%，且 FGTR 的稀疏时空监督优于对预测 BEV 特征施加全监督的方案。

在方法谱系上，ResWorld 属于不依赖辅助任务（如检测、跟踪、建图）的端到端规划范式，与 **UniAD**（Hu et al., CVPR 2023）、**VAD**（Jiang et al., ICCV 2023）等多辅助任务方法形成互补，同时相较于 **SSR** 的稀疏场景表示和 **LAW**（Li et al., ICLR 2025）的隐式世界模型，ResWorld 以显式的动态物体建模和轨迹交互机制实现了更优的规划精度与安全性。

### 端到端自动驾驶与世界模型的兴起

端到端自动驾驶旨在直接从传感器输入映射到规划轨迹，省去传统模块化管线中的中间表示与人工规则。近年来，基于鸟瞰图（BEV）表征的规划器取得了显著进展，代表性工作包括 **UniAD**（Hu et al., CVPR 2023）利用多辅助任务联合优化、**VAD**（Jiang et al., ICCV 2023）采用矢量化场景表示、以及 **PARA-Drive**（Weng et al., CVPR 2024）设计模块化并行架构。然而，这些方法通常依赖显式的感知辅助任务（如检测、跟踪、建图）来提供中间监督信号，增加了模型复杂度和标注成本。

为摆脱对辅助任务的依赖，世界模型（world model）被引入端到端规划。其核心思想是让模型预测未来的场景演化，从而隐式地学习环境动力学，为规划提供更丰富的上下文。**GenAD**（Zheng et al., ECCV 2024）探索了生成式端到端规划，**LAW**（Li et al., ICLR 2025）则采用隐式世界模型。**SSR**（Li & Cui, ICLR 2025）进一步提出稀疏场景表示，在无辅助任务条件下取得了有竞争力的规划性能。

### 现有世界模型的两大瓶颈

尽管世界模型展现出潜力，但现有方案存在两个关键瓶颈：

**瓶颈一：对静态物体的冗余建模。** 传统世界模型对整个场景（包括大量静态背景）进行统一预测。然而，在预测未来时，若保持当前BEV坐标系不变，静态物体（如建筑物、路面标线）的空间分布实际上不随时间变化。对这些不变信息的重复建模不仅浪费计算资源，还可能引入噪声，干扰模型对真正影响规划决策的动态物体的关注。

**瓶颈二：未来预测与轨迹优化的脱节。** 现有方法通常将未来BEV特征预测作为一个独立的代理任务，仅通过共享骨干网络隐式地影响规划模块。预测出的未来场景信息并未被显式地用于修正或优化规划轨迹，导致世界模型的预测能力未能充分转化为规划精度的提升。更严重的是，当对未来BEV特征施加全监督时，世界模型容易发生“坍塌”（collapse）——预测结果趋于模糊的平均状态，丧失空间多样性。

### ResWorld的动机与核心思路

针对上述瓶颈，ResWorld提出两个核心设计：

- **时序残差世界模型（TR-World）**：通过计算相邻时间戳场景查询的时序残差（temporal residuals）来提取动态物体信息，让世界模型聚焦于预测动态物体的未来空间分布，避免对静态物体的冗余建模。其物理直觉在于：在当前BEV坐标系下，静态物体的空间位置可视为不变，场景的变化主要由动态物体的运动引起，而这一变化恰好可由时序残差刻画。

- **未来引导的轨迹修正（FGTR）**：通过可变形注意力（Deformable Attention）显式地将预测的未来BEV特征与先验轨迹进行交互，使模型能够“查询”未来时刻自车周围的潜在碰撞风险，从而对先验轨迹进行修正。该模块同时提供稀疏时空监督——仅对轨迹进行L1回归损失，而不对中间的未来BEV特征施加显式监督——有效防止了世界模型的坍塌。

Figure 1 直观对比了传统世界模型框架与ResWorld框架的差异：前者对整个场景建模并隐式优化轨迹，后者则通过时序残差聚焦动态物体，并通过显式交互利用未来预测修正轨迹。

## 核心方法与创新机理

ResWorld的核心创新围绕一个关键洞察展开：**在当前BEV坐标系下预测未来时，静态物体的空间分布可视为不变，因而世界模型只需聚焦于动态物体的变化**。这一洞察催生了两个相互协同的**changed slots**，分别改变了世界模型的输入表征和轨迹对预测未来特征的利用方式。

### 从全场景建模到动态物体聚焦：时序残差世界模型

现有世界模型（如**SSR**（Li & Cui, ICLR 2025））通常对整个场景的稀疏查询进行未来预测，这导致模型将大量容量浪费在对静态物体（建筑物、路面、静止车辆等）的冗余建模上。ResWorld的核心突破在于**将世界模型的输入从“全场景查询”替换为“相邻时间戳的稀疏查询残差”**，从而将建模对象从整个场景收窄到动态物体。

具体而言，ResWorld首先通过TokenLearner从融合的BEV特征 $\mathbf{B}_{fuse}$ 中提取稀疏场景查询，然后对相邻时间戳的查询做差，得到**时序残差（temporal residuals）** $\mathbf{R}_i$。这些残差本质上编码了场景中“哪些区域发生了变化”——即动态物体的运动信息。时序残差世界模型（TR-World）仅以这些残差为输入，通过自注意力聚合各时间步的动态信息 $\hat{\mathbf{R}} = \sum_{i=t-k+1}^{t} \mathrm{SelfAttention}(\mathbf{R}_i)$，再通过TokenFuser将其扩展回BEV空间，与当前融合BEV特征相加得到预测的未来BEV特征 $\mathbf{B}_{future}$。

这一设计的精妙之处在于：由于预测始终在当前BEV坐标系下进行，当前BEV特征 $\mathbf{B}_{fuse}$ 本身已经描绘了静态物体的未来空间分布，TR-World只需补充动态物体的变化即可。这从根本上避免了静态物体的冗余建模，使世界模型的容量被精准地分配到对规划安全最关键的因素——动态物体的未来运动预测上。

### 从隐式优化到显式交互：未来引导的轨迹修正

传统世界模型框架中，预测的未来BEV特征通常仅作为隐式的代理任务来优化模型，并不直接参与轨迹的生成过程。ResWorld的第二个关键创新在于**将轨迹对预测未来特征的利用方式从“隐式优化”改为“显式修正”**：引入未来引导的轨迹修正模块（Future-Guided Trajectory Refinement, FGTR），通过可变形注意力机制让先验轨迹与预测的未来BEV特征直接交互。

FGTR的核心操作是 $\mathbf{W} = \mathrm{DeformAttention}(\mathbf{W}, \mathbf{B}_{future}, \mathbf{T}_{prior})$，即以先验轨迹 $\mathbf{T}_{prior}$ 作为参考点，在航点查询 $\mathbf{W}$ 与未来BEV特征 $\mathbf{B}_{future}$ 之间进行可变形注意力交互。这一机制使模型能够显式地从未来BEV特征中收集自车周围的环境信息，检查先验轨迹是否会导致碰撞或偏离车道，并据此对轨迹进行修正。

这种显式交互带来了双重收益：一方面，未来BEV特征直接服务于轨迹修正，提升了规划精度；另一方面，FGTR提供了一种**稀疏时空监督**——模型无需对 $\mathbf{B}_{future}$ 施加全局的真实未来数据监督（消融实验表明，施加全监督反而使L2 Avg上升0.04，碰撞率上升0.07），而是通过轨迹修正的损失信号间接约束世界模型的学习。这有效防止了世界模型在缺乏显式监督时容易出现的**模式坍塌**问题：如Figure 4所示，配备FGTR的世界模型预测的未来BEV特征在空间分布上展现出更丰富的多样性，而未配备FGTR的模型则倾向于产生坍塌的、缺乏判别力的预测。

### 两组件协同的因果链路

TR-World和FGTR并非两个孤立的创新，而是构成了一条完整的因果链路：TR-World负责从时序残差中预测动态物体的未来空间分布，生成 $\mathbf{B}_{future}$；FGTR则利用这一预测结果，通过显式的注意力交互修正先验轨迹。消融实验（Table 3）清晰地验证了这一协同效应：在无ego status设置下，单独加入TR-World使L2 Avg从0.71降至0.65；再加入FGTR后，L2 Avg进一步降至0.59，Collision Avg从0.29降至0.17——两个组件各自贡献显著，且联合使用时产生叠加增益。

ResWorld 的整体流水线围绕一个核心洞察构建：**在当前 BEV 坐标系下预测未来时，静态物体的空间分布可视为不变，因此世界模型只需聚焦于动态物体的变化**。基于这一洞察，整个框架由四个关键模块串联而成，形成“先验轨迹预测 → 时序残差提取 → 时序残差世界模型 → 未来引导轨迹修正”的端到端规划流程（Figure 2）。

![[assets/figures/papers/paper_list_l36_https_openreview_net_forum_id_ptGmMFGWmk/figures/002_Figure_2.jpg]]
*Figure 2: Overall Framework of ResWorld. Multi-view images at different timestamps are converted into BEV features, which are used to predict prior trajectories. On the other hand, BEV features are used to calculate temporal residuals, which are then processed by the Temporal Residual World Model to predict the future distribution of dynamic objects. Future-Guided Trajectory Refinement module further utilizes the predicted future BEV features to refine the planning results*

### 流水线总览

多视角图像序列首先被转换为 BEV 特征，并在当前坐标系下进行时序融合。融合后的 BEV 特征同时服务于两条路径：**先验轨迹预测**分支直接从场景表示中生成初步的规划轨迹和稀疏场景查询；**时序残差世界模型**分支则通过相邻时间戳的场景查询差异提取动态物体信息，预测其未来空间分布，并生成未来 BEV 特征。最后，**未来引导轨迹修正模块（FGTR）** 以先验轨迹为参考点，通过可变形注意力显式地与未来 BEV 特征交互，对轨迹进行修正，输出最终规划结果。

### 模块间数据流与依赖关系

**1. BEV 特征融合与稀疏场景查询提取（Section 3.1）**

多帧环视图像经骨干网络和视角变换后，得到各时间戳的 BEV 特征 $\mathbf{B}_t, \mathbf{B}_{t-1}, \dots, \mathbf{B}_{t-k}$。这些特征被变换到当前 $t$ 时刻的坐标系后拼接，通过卷积融合为 $\mathbf{B}_{fuse}$（Eq. 1）。随后，利用 TokenLearner 机制——即对 $\mathbf{B}_{fuse}$ 施加空间自注意力，再与自身逐元素相乘后全局平均池化——将密集 BEV 特征压缩为一组稀疏场景查询 $\mathbf{S}_{fuse}$（Eq. 2）。这些稀疏查询既用于生成先验轨迹 $\mathbf{T}_{prior}$，也作为时序残差计算的基准。

**2. 时序残差提取（Section 3.2）**

在获得 $\mathbf{S}_{fuse}$ 的空间注意力图后，该注意力权重被分别应用于各历史时间戳的 BEV 特征 $\mathbf{B}_i$，提取出各时刻的稀疏场景查询 $\mathbf{S}_i$（Eq. 3）。**时序残差** $\mathbf{R}_i$ 定义为相邻时间戳场景查询的差值（Eq. 4），其物理含义是场景中动态物体在 BEV 空间下的位移信息。由于静态物体在不同时刻的空间分布不变，其查询差值趋近于零，因此时序残差天然地过滤了静态背景，仅保留动态物体的运动信号。

**3. 时序残差世界模型 TR-World（Section 3.3）**

TR-World 仅以时序残差序列 $\{\mathbf{R}_i\}$ 为输入，不依赖任何辅助任务（如检测、跟踪）来提供动态物体信息。模型对各时间步的残差分别施加自注意力，然后累加得到动态物体的未来表示 $\hat{\mathbf{R}}$（Eq. 6）。接着，通过 TokenFuser 操作——以 $\mathbf{B}_{fuse}$ 经 MLP 生成空间权重，与 $\hat{\mathbf{R}}$ 逐通道相乘——将压缩的动态物体表示扩展回 BEV 空间，并与当前融合特征 $\mathbf{B}_{fuse}$ 残差相加，得到预测的未来 BEV 特征 $\mathbf{B}_{future}$（Eq. 7）。**关键设计**在于：预测仍采用当前 BEV 坐标系，因此 $\mathbf{B}_{fuse}$ 本身已经刻画了静态物体的未来分布，TR-World 只需补充动态物体的变化，避免了传统世界模型对整个场景的冗余建模。

**4. 未来引导轨迹修正 FGTR（Section 3.4）**

FGTR 模块将先验轨迹 $\mathbf{T}_{prior}$ 作为可变形注意力的参考点，在航点查询 $\mathbf{W}$ 与未来 BEV 特征 $\mathbf{B}_{future}$ 之间进行显式交互（Eq. 8）。这一操作使模型能够沿先验轨迹采样未来环境信息，检查自车是否会与其他物体碰撞或偏离车道，从而对轨迹进行修正。更新后的航点查询经 MLP 解码为最终规划轨迹 $\mathbf{T}_{final}$（Eq. 9）。

### 训练策略的独特之处

ResWorld 的训练仅对先验轨迹和最终轨迹施加 L1 回归损失（Section 3.5），**不对预测的未来 BEV 特征 $\mathbf{B}_{future}$ 施加任何显式监督**。这一稀疏时空监督策略的动机在于：若用真实未来数据监督 $\mathbf{B}_{future}$，会迫使模型在每个空间位置预测确定性的未来状态，而未来本身是多模态的，这种全监督反而导致世界模型坍塌（详见 Table 4 消融实验）。FGTR 模块通过轨迹与未来特征的交互，隐式地为世界模型提供了稀疏但有效的学习信号，使其能够保持未来空间分布的多样性（Figure 4）。

### 与传统世界模型框架的本质差异

传统世界模型（如 Figure 1 左所示）对整个场景（包括静态背景和动态物体）进行统一建模，预测的未来表示仅作为隐式优化轨迹的代理任务。ResWorld（Figure 1 右）的核心差异在于：**（1）建模对象聚焦**——通过时序残差将世界模型的注意力集中在动态物体上，静态物体由当前 BEV 特征自然继承；**（2）轨迹利用方式升级**——先验轨迹不再仅是最终输出，而是作为查询未来特征的桥梁，通过 FGTR 实现显式的“预测-验证-修正”闭环。这两个设计共同构成了“残差建模 + 未来引导”的端到端规划范式。

ResWorld 的核心架构由四个模块串联构成：先验轨迹预测（Prior Trajectory Prediction）、时序残差提取（Temporal Residual Extraction）、时序残差世界模型（TR-World）以及未来引导的轨迹修正（FGTR）。整个流程从多视角图像出发，最终输出规划轨迹，其关键设计在于**将动态物体建模从全场景预测中解耦**，并通过**未来 BEV 特征与轨迹的显式交互**来修正规划结果。

### 3.1 先验轨迹预测与稀疏场景查询

给定当前时间戳 $t$ 及过去 $k$ 帧的多视角图像，首先通过 BEV 编码器将各帧图像变换到当前 BEV 坐标系，得到 BEV 特征序列 $\mathbf{B}_t, \mathbf{B}_{t-1}, \dots, \mathbf{B}_{t-k}$。随后通过拼接与卷积进行融合：

$$
\mathbf{B}_{fuse} = \mathrm{Conv}(\mathrm{Concat}(\mathbf{B}_{t}, \mathbf{B}_{t-1}, \dots, \mathbf{B}_{t-k}))
$$

其中 $\mathbf{B}_{fuse}$ 为融合后的密集 BEV 特征。为降低后续计算量并提取关键场景信息，采用 TokenLearner 机制将其压缩为稀疏场景查询：

$$
\mathbf{S}_{fuse} = \mathrm{TokenLearner}(\mathbf{B}_{fuse}) = \mathrm{AvgPool}(\mathrm{SA}(\mathbf{B}_{fuse}) \odot \mathbf{B}_{fuse})
$$

这里 $\mathrm{SA}(\cdot)$ 表示空间注意力（Spatial Attention），$\odot$ 为逐元素乘法，$\mathrm{AvgPool}$ 为全局平均池化。$\mathbf{S}_{fuse}$ 作为场景的紧凑表示，一方面用于预测先验轨迹 $\mathbf{T}_{prior}$，另一方面作为时序残差提取的锚点。

### 3.2 时序残差提取

世界模型需要预测动态物体的未来空间分布，但直接对整个场景建模会引入大量关于静态物体的冗余计算。ResWorld 的解决方案是：**在相邻时间戳的稀疏场景查询之间计算残差**，以此捕获场景中发生变化的区域（即动态物体）。

具体而言，对于时间戳 $i \in \{t-k+1, \dots, t\}$，利用 $\mathbf{B}_{fuse}$ 上学习到的空间注意力权重对 $\mathbf{B}_i$ 进行加权池化，得到各帧的场景查询 $\mathbf{S}_i$：

$$
\mathbf{S}_i = \mathrm{AvgPool}(\mathrm{SA}(\mathbf{B}_{fuse}) \odot \mathbf{B}_i)
$$

随后计算时序残差 $\mathbf{R}_i = \mathbf{S}_i - \mathbf{S}_{i-1}$。由于在当前 BEV 坐标系下静态物体的空间分布在短时间内近似不变，$\mathbf{R}_i$ 主要编码了动态物体的位移信息。这一设计使得世界模型无需依赖目标检测等辅助任务即可提取动态物体信息。

### 3.3 时序残差世界模型 (TR-World)

TR-World 仅以时序残差序列 $\{\mathbf{R}_i\}_{i=t-k+1}^{t}$ 作为输入，通过自注意力机制建模动态物体的运动模式，并预测其在未来的空间分布：

$$
\hat{\mathbf{R}} = \sum_{i=t-k+1}^{t} \mathrm{SelfAttention}(\mathbf{R}_i)
$$

其中 $\hat{\mathbf{R}}$ 为聚合后的动态物体未来表示。为了将其映射回 BEV 空间以便与规划模块交互，采用 TokenFuser 操作将 $\hat{\mathbf{R}}$ 在 $\mathbf{B}_{fuse}$ 上进行扩展：

$$
\mathbf{B}_{future} = \mathrm{TokenFuser}(\hat{\mathbf{R}}, \mathbf{B}_{fuse}) + \mathbf{B}_{fuse} = \mathrm{MLP}(\mathbf{B}_{fuse}) \otimes \hat{\mathbf{R}} + \mathbf{B}_{fuse}
$$

这里 $\otimes$ 表示矩阵乘法，$\mathrm{MLP}(\mathbf{B}_{fuse})$ 生成与 $\mathbf{B}_{fuse}$ 空间维度对齐的权重。**关键设计**在于：预测未来 BEV 特征时仍沿用当前 BEV 坐标系，因此 $\mathbf{B}_{fuse}$ 本身已包含静态物体的未来空间分布（在当前坐标系下视为不变），$\hat{\mathbf{R}}$ 仅需补充动态物体的变化信息。这从根本上避免了对静态物体的冗余建模。

### 3.4 未来引导的轨迹修正 (FGTR)

传统世界模型通常将未来预测作为隐式代理任务，预测的未来 BEV 特征并未直接参与轨迹优化。FGTR 模块则通过**可变形注意力（Deformable Attention）**在航点查询 $\mathbf{W}$ 与未来 BEV 特征 $\mathbf{B}_{future}$ 之间建立显式交互，以先验轨迹 $\mathbf{T}_{prior}$ 作为参考点：

$$
\mathbf{W} = \mathrm{DeformAttention}(\mathbf{W}, \mathbf{B}_{future}, \mathbf{T}_{prior})
$$

直观上，$\mathbf{T}_{prior}$ 定义了自车在未来各时间步的预期位置，可变形注意力围绕这些参考点在 $\mathbf{B}_{future}$ 上采样周围环境特征。这使得模型能够“前瞻”到轨迹路径上是否存在障碍物或偏离车道，从而对 $\mathbf{T}_{prior}$ 进行修正。更新后的航点查询最终通过 MLP 解码为最终轨迹：

$$
\mathbf{T}_{final} = \mathrm{MLP}(\mathbf{W})
$$

### 3.5 训练损失

ResWorld 的训练仅对先验轨迹和最终轨迹施加 L1 回归损失，**不对 $\mathbf{B}_{future}$ 施加任何显式监督**：

$$
\mathcal{L} = \mathrm{L1}(\mathbf{T}_{prior}, \mathbf{T}_{GT}) + \mathrm{L1}(\mathbf{T}_{final}, \mathbf{T}_{GT})
$$

这一设计有两层考量：其一，FGTR 模块提供的稀疏时空监督（通过轨迹与未来 BEV 特征的交互）已足以驱动世界模型学习有意义的未来表示，全监督反而会导致世界模型坍塌（见 Table 4 消融实验）；其二，保留 $\mathbf{B}_{future}$ 在多未来时间戳上的空间分布多样性，有利于 FGTR 模块获取更丰富的环境信息进行轨迹修正。

## 实验与关键发现

### 核心性能：nuScenes 与 NAVSIM 双基准验证

ResWorld 在两个主流端到端自动驾驶基准上均取得了领先的规划性能，且不依赖辅助任务。

在 **nuScenes** 数据集上（Table 1），ResWorld 在不使用 ego status 的设置下实现 L2 Avg **0.65 m**、Collision Avg **0.23%**，显著优于同属无辅助任务路线的 **SSR**（Li & Cui, ICLR 2025）的 0.74 m 和 0.31%，以及 **LAW**（Li et al., ICLR 2025）的 0.73 m 和 0.35%。与使用多辅助任务的 **UniAD**（Hu et al., CVPR 2023）的 0.71 m / 0.29% 和 **VAD**（Jiang et al., ICCV 2023）的 0.70 m / 0.27% 相比，ResWorld 同样表现出明显优势。当引入 ego status 后，ResWorld 的 L2 Avg 进一步降至 **0.35 m**，Collision Avg 降至 **0.08%**，超过 **BEV-Planner++**（Li et al., CVPR 2024）的 0.41 m / 0.12%。

![[assets/figures/papers/paper_list_l36_https_openreview_net_forum_id_ptGmMFGWmk/figures/004_Table_1.jpg]]
*Table 1: Comparison of state-of-the-art methods on the nuScenes dataset. ∗ denotes the metrics evaluated using the official models and code. ♢ denotes using ego status in the planning module following BEVPlanner++ (Li et al., 2024c). ‡ denotes the AVG metric calculated in the same way as VAD (Jiang et al., 2023)*

在 **NAVSIM** navtest split 上（Table 2），ResWorld 的 PDMS 达到 **89.0%**，超越此前最优的 **Transfuser***（87.0%）及 **PARA-Drive**（Weng et al., CVPR 2024）等所有对比方法。该结果验证了时序残差世界模型在更复杂的闭环评估场景下的泛化能力。

![[assets/figures/papers/paper_list_l36_https_openreview_net_forum_id_ptGmMFGWmk/figures/005_Table_2.jpg]]
*Table 2: Comparison of state-of-the-art methods on the NAVSIM navtest split. ⋆ denotes the utilization of historical frame to obtain the temporal residual of the scene represenation*

### 消融实验：TR-World 与 FGTR 的因果贡献

Table 3 系统拆解了各组件的独立增益。基线模型（无 TR-World、无 FGTR、无 ego status）的 L2 Avg 为 0.71 m，Collision Avg 为 0.29%。单独加入 **TR-World** 后，L2 Avg 降至 0.65 m，Collision Avg 降至 0.28%，验证了动态物体建模对规划精度的直接贡献。进一步加入 **FGTR** 模块后，L2 Avg 降至 **0.59 m**，Collision Avg 降至 **0.17%**，说明显式的未来 BEV 特征与轨迹交互能有效降低碰撞风险。

![[assets/figures/papers/paper_list_l36_https_openreview_net_forum_id_ptGmMFGWmk/figures/006_Table_3.jpg]]
*Table 3: Ablation study of each proposed component. “TR-World” and FGTR denote Temporal Residual World Model and the Future-Guided Trajectory Refinement, respectively*

在带 ego status 的设置下，TR-World 与 FGTR 的联合作用使 L2 Avg 从 0.65 m 降至 0.59 m，Collision Avg 从 0.28% 降至 0.17%，降幅分别为 9.2% 和 39.3%。Table 5 进一步对比了先验轨迹与最终轨迹的性能：先验轨迹 L2 Avg 0.71 m / Collision 0.29%，最终轨迹 L2 Avg 0.59 m / Collision 0.17%，证实 TR-World 和 FGTR 的增益并非来自更强的先验轨迹预测，而是源于对未来动态信息的有效利用。

![[assets/figures/papers/paper_list_l36_https_openreview_net_forum_id_ptGmMFGWmk/figures/009_Table_5.jpg]]
*Table 5: Performance of Prior Performance. The prior trajectory is predicted using the same model architecture as that of the baseline, while the prediction of the final trajectory requires the TR-World and FGTR models*

### 稀疏时空监督 vs. 全监督：防止世界模型坍塌

Table 4 揭示了一个关键发现：对预测的未来 BEV 特征 $B_{future}$ 施加真实未来数据的全监督，反而使 L2 Avg 上升 0.04 m，Collision Avg 上升 0.07%。这表明强制 $B_{future}$ 逼近单一的真值分布会限制其空间多样性，导致世界模型坍塌。FGTR 模块通过可变形注意力仅在轨迹参考点周围收集未来环境信息，提供了一种稀疏的时空监督信号，既保留了 $B_{future}$ 的多模态分布能力，又能有效指导轨迹修正。Figure 4 的定性可视化佐证了这一机制：FGTR 预测的未来 BEV 特征在空间分布上比全监督版本展现出更丰富的多样性。

### 失败模式与局限性

TR-World 的核心瓶颈在于其对**潜在动态物体**的敏感性不足。时序残差通过相邻帧的场景查询差分来捕获运动信息，但对于静止车辆、行人等瞬时速度为零的潜在动态物体，残差信号微弱，导致这些对象被迫交由先验轨迹预测分支与静态物体一同处理。这会在“车辆突然启动”或“行人突然横穿”等场景下引入安全隐患。

此外，当缺乏历史帧信息时，时序残差无法提取，模型需回退到使用目标检测的代理查询（agent queries）作为世界模型输入。在 NAVSIM 上，该回退方案的 PDMS 降至 88.3%，相比完整 ResWorld 的 89.0% 有明显下降，说明历史帧对动态物体建模至关重要。

### 开放问题

如何利用粗略感知有效提取潜在动态物体的信息，并将其与时序残差世界模型结合以实现预防性建模，是进一步提升安全性的关键方向。当前方法对“静止但可能运动”的对象缺乏显式建模机制，这需要新的表征学习范式来弥补时序残差的固有盲区。

![[assets/figures/papers/paper_list_l36_https_openreview_net_forum_id_ptGmMFGWmk/figures/010_Figure_5.jpg]]
*Figure 5: Visualization of Planning Results. The object bounding boxes and lane lines on the BEV plane are rendered using the annotations. The green box denotes the ego vehicle. The areas enclosed by dashed circles indicate where collisions will occur*

## 定位与知识库关联

### 1. 在端到端自动驾驶谱系中的位置

ResWorld 属于**基于世界模型的端到端规划器**，其核心演进路径可沿两条轴线定位：

**轴线一：从多辅助任务到无辅助任务的稀疏场景表示**

早期端到端规划器依赖密集的辅助任务监督（检测、建图、运动预测等）来学习场景表征。**UniAD**（Hu et al., CVPR 2023）以多任务级联方式联合优化感知与规划，**VAD**（Jiang et al., ICCV 2023）引入矢量化场景表示以降低计算开销。**SSR**（Li & Cui, ICLR 2025）首次证明：通过稀疏场景查询（TokenLearner压缩BEV特征），仅靠规划损失即可达到与多任务方法可比的性能，从而将辅助任务从必需项降级为可选项。ResWorld 沿袭 SSR 的无辅助任务范式（Table 1中不带 ♢ 的对比），但在稀疏查询的基础上进一步引入**时序残差**作为世界模型的输入，将建模焦点从“整个场景”收缩到“动态物体的变化量”。

**轴线二：从隐式世界模型到显式未来交互**

**LAW**（Li et al., ICLR 2025）提出隐式世界模型，通过预测未来潜在状态来辅助规划，但预测的未来表示仅作为隐式正则项，不直接参与轨迹优化。**GenAD**（Zheng et al., ECCV 2024）以生成式方式建模未来场景，同样缺乏轨迹与未来特征的显式交互。ResWorld 的关键跃迁在于 **Future-Guided Trajectory Refinement（FGTR）** 模块：通过可变形注意力，让先验轨迹的航点查询直接与预测的未来BEV特征交互——先验轨迹作为参考点，航点查询从未来BEV特征中收集周围环境信息，检查碰撞风险并修正轨迹。这使得世界模型的输出从“隐式优化信号”升级为“显式轨迹修正依据”。

### 2. 与关键基线的方法论差异

| 维度 | SSR（Li & Cui, ICLR 2025） | ResWorld（本文） |
|------|--------------------------|-----------------|
| 世界模型输入 | 整个场景的稀疏查询 | 相邻时间戳的稀疏查询残差（temporal residuals） |
| 静态物体建模 | 与动态物体混合建模 | 利用当前BEV坐标系预测未来，静态物体空间分布视为不变，无需冗余建模 |
| 未来预测的利用 | 作为代理任务隐式优化模型 | FGTR显式修正先验轨迹，同时提供稀疏时空监督防止世界模型坍塌 |
| 轨迹优化 | 单阶段轨迹预测 | 先验轨迹预测 + 未来引导轨迹修正（两阶段） |

这一差异的因果机制是：当在当前BEV坐标系下预测未来时，静态物体（车道线、建筑物）的空间分布与当前帧一致，只有动态物体发生位移。因此，建模“整个场景的未来”是冗余的——模型被迫在静态背景上浪费容量。ResWorld 通过时序残差 $\mathbf{R}_i = \mathbf{S}_i - \mathbf{S}_{i-1}$ 提取纯动态信息，让 TR-World 仅预测动态物体的未来空间分布 $\hat{\mathbf{R}}$，再通过 TokenFuser 将其扩展回BEV空间与静态的 $\mathbf{B}_{fuse}$ 相加得到 $\mathbf{B}_{future}$。这一设计将世界模型的建模负担从“全场景预测”压缩为“动态物体位移预测”，本质上是一种**稀疏化的因果归因**。

### 3. 适用边界与局限

**强依赖历史帧的时序残差提取**

TR-World 的核心输入是时序残差，这要求模型能够访问历史帧的多视角图像。当历史帧不可用时（如单帧推理场景），时序残差无法计算。在 NAVSIM 实验中，ResWorld 回退到使用目标检测的代理查询（agent queries）替代时序残差作为世界模型输入，PDMS 从 89.0% 降至 88.3%（Table 2 中 Det&Map 行）。这表明**时序残差贡献了约 0.7% 的 PDMS 增益**，但模型在无历史帧时仍可通过代理查询保持竞争力——这降低了方法对历史帧的刚性依赖，但也意味着在极低延迟要求的实时系统中，残差提取带来的额外计算开销需要权衡。

**对潜在动态物体的不敏感性**

TR-World 通过相邻帧的稀疏查询差值来捕获运动信息。对于**正在运动**的物体（行驶中的车辆、行走的行人），时序残差能有效捕捉其位移。但对于**潜在动态物体**——停在路边的车辆（可能突然启动）、静止的行人（可能突然横穿）——其时序残差趋近于零，TR-World 无法将其与真正的静态物体区分。这些物体被迫交由先验轨迹预测分支与静态背景一起处理，模型缺乏对“静止但危险”物体的预防性建模能力。这是作者明确指出的局限，也是未来工作的开放方向：如何利用粗略感知提取潜在动态物体信息，并与时序残差世界模型结合，实现更安全的预防性规划。

**FGTR 稀疏时空监督优于全监督的机制**

Table 4 的消融实验揭示了一个反直觉的发现：对 $\mathbf{B}_{future}$ 施加真实未来数据的全监督（Future Supervision），反而使 L2 Avg 上升 0.04，Collision Avg 上升 0.07。作者的解释是：全监督强制 $\mathbf{B}_{future}$ 精确匹配某一特定未来时刻的BEV分布，但 FGTR 的稀疏时空监督允许 $\mathbf{B}_{future}$ 保留多时间步的空间分布多样性（Figure 4 可视化证实了这一点，FGTR 预测的 BEV 特征比全监督版本展现出更丰富的空间分布）。这一现象的本质是：**世界模型的目标不是精确预测未来，而是为轨迹修正提供足够丰富的环境信息**。过度约束未来BEV特征会压缩其表征空间，反而削弱 FGTR 从中学到有用修正信号的能力。这一洞察对世界模型的设计哲学有深远影响——它暗示着“预测精度”与“规划效用”之间可能存在 trade-off。

### 4. 开放问题

1. **潜在动态物体的预防性建模**：如何在不依赖辅助检测任务的前提下，让时序残差世界模型感知“静止但危险”的物体？可能的路径包括引入不确定性建模，或利用场景上下文（如红绿灯状态、人行横道位置）推断物体的潜在运动意图。

2. **时序残差的表征充分性**：当前仅使用相邻帧的稀疏查询差值作为动态信息载体。是否遗漏了更高阶的运动信息（加速度、运动模式）？多尺度时序残差或可变形时序注意力可能是改进方向。

3. **世界模型坍塌的理论理解**：Figure 4 展示了 FGTR 缓解世界模型坍塌的定性效果，但坍塌的深层原因（为什么全监督会导致表征退化）尚缺乏理论分析。从信息瓶颈角度看，FGTR 可能通过只保留“对规划有用的未来信息”来实现隐式的信息压缩。

4. **跨数据集与闭环评估**：当前验证集中在 nuScenes 和 NAVSIM 的开环指标上。在 CARLA 等闭环模拟器中，时序残差世界模型能否保持优势？闭环场景下的分布偏移和累积误差需要进一步检验。

## 原文 PDF

![[paperPDFs/ICLR_2026/ResWorld_Temporal_Residual_World_Model_for_End_to_End_Autonomous_Driving_0aa5048f38c3.pdf]]
