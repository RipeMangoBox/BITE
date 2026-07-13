---
title: "MeanFuser: Fast One-Step Multi-Modal Trajectory Generation and Adaptive Reconstruction via MeanFlow for End-to-End Autonomous Driving"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/MeanFuser_Fast_One_Step_Multi_Modal_Trajectory_Generation_and_Adaptive_Reconstruction_via_MeanFlow_for_End_to_End_Autonomous_Driving.pdf
project_link: null
code_link: null
aliases:
- MeanFuser
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
- topic/generative_models_diffusion
core_operator: 将高斯混合噪声（GMN）作为连续先验取代离散锚点，并引入MeanFlow恒等式直接学习平均速度场，实现单步多模态轨迹采样；通过自适应重建模块（ARM）隐式评估并选择或重建最优轨迹。
primary_logic: 利用高斯混合噪声为流匹配提供连续、多模态的先验分布，消除对固定锚点词汇表的依赖；基于MeanFlow恒等式将瞬时速度场建模转化为平均速度场学习，使单步生成成为可能；并设计轻量级注意力机制实现无需显式评分函数的候选轨迹筛选与重建。
claims:
- MeanFuser 在 NAVSIMv1 上取得 89.0 PDMS，超越基线 DiffusionDrive（88.1）和 GoalFlow（85.7），且在 NAVSIMv2 上达到 89.5 EPDMS 的最优性能。
- MeanFuser 推理速度达 59 FPS，分别比 GoalFlow、Hydra-MDP、DiffusionDrive 快 5.20×、2.65×、1.55×。
- 消融实验证明，高斯混合噪声（GMN）和自适应重建模块（ARM）分别带来 +0.9 和 +0.8 PDMS 的提升。
- NAVSIM v1 上 PDMS = 89.0
---

# MeanFuser: Fast One-Step Multi-Modal Trajectory Generation and Adaptive Reconstruction via MeanFlow for End-to-End Autonomous Driving

> [!tip] 核心洞察
> 利用高斯混合噪声为流匹配提供连续、多模态的先验分布，消除对固定锚点词汇表的依赖；基于MeanFlow恒等式将瞬时速度场建模转化为平均速度场学习，使单步生成成为可能；并设计轻量级注意力机制实现无需显式评分函数的候选轨迹筛选与重建。

| 字段 | 内容 |
|------|------|
| 中文题名 | MeanFuser：基于MeanFlow的快速单步多模态轨迹生成与自适应重建端到端自动驾驶方法 |
| 英文题名 | MeanFuser: Fast One-Step Multi-Modal Trajectory Generation and Adaptive Reconstruction via MeanFlow for End-to-End Autonomous Driving |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2602.20060) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction #topic/generative_models_diffusion |
| Method | MeanFuser |
| Dataset | NAVSIM v1, NAVSIM v2, CARLA Longest6 |

> [!tip] 效果简介
> - NAVSIM v1 上，PDMS 89.0 vs 88.1 (DiffusionDrive) (+0.9)。
> - NAVSIM v2 上，EPDMS 89.5 vs N/A (超越先前方法) (+N/A)。
> - CARLA Longest6 上，Driving Score (DS) 70.08 ± 3.20 vs 64.27 ± 2.43 (DiffusionDrive) (+5.81)。

## 概要

端到端自动驾驶中的生成式规划方法近年来取得了显著进展，但现有方案普遍面临两个核心瓶颈：其一，基于锚点（anchor）的生成范式依赖离散轨迹词汇表，无法充分覆盖连续轨迹空间，导致在分布外场景下鲁棒性下降；其二，标准流匹配（flow matching）需要多步常微分方程（ODE）求解，推理速度慢且存在数值误差。

针对上述问题，本文提出 **MeanFuser**，一种基于 MeanFlow 的快速单步多模态轨迹生成与自适应重建框架。其核心思想包含三个层面：

1. **连续先验替代离散锚点**：引入高斯混合噪声（Gaussian Mixture Noise, GMN）作为先验分布，通过对专家轨迹聚类得到多个高斯分量，为流匹配提供连续、多模态的噪声源，从根本上消除了对固定锚点词汇表的依赖。
2. **单步生成范式**：将 MeanFlow 恒等式引入端到端规划，直接学习噪声与数据分布之间的平均速度场，而非传统流匹配中的瞬时速度场，从而仅需一步即可从噪声生成轨迹，大幅提升推理效率。
3. **隐式轨迹选择与重建**：设计轻量级自适应重建模块（Adaptive Reconstruction Module, ARM），通过交叉注意力机制隐式评估候选轨迹质量，并在所有候选均不理想时自动重建更优轨迹，无需显式评分函数。

在实验验证方面，MeanFuser 在 NAVSIMv1 基准上取得 **89.0 PDMS**，超越 DiffusionDrive（88.1）和 GoalFlow（85.7）；在 NAVSIMv2 上达到 **89.5 EPDMS** 的最优性能。推理速度达 **59 FPS**，分别比 GoalFlow、Hydra-MDP、DiffusionDrive 快 5.20×、2.65×、1.55×。消融实验证实，GMN 和 ARM 分别带来 +0.9 和 +0.8 PDMS 的提升。在 CARLA Longest6 闭环仿真中，MeanFuser 的驾驶得分（DS）达到 70.08，较 DiffusionDrive 提升 5.81 分。

在方法谱系上，MeanFuser 以 **TransFuser**（Chitta et al., IEEE TPAMI）为感知骨干，在生成范式上区别于基于离散词汇表的 **VADv2**（arXiv 2024）、基于目标点引导流匹配的 **GoalFlow**（Xing et al., CVPR 2025）、基于扩散模型与锚点聚类的 **DiffusionDrive**（Yang et al., CVPR 2025），以及基于显式评分的 **Hydra-MDP**（arXiv 2024）和基于世界模型评估的 **WoTE**（ICCV 2025）。其独特之处在于将 MeanFlow 单步生成与 GMN 连续先验相结合，并以 ARM 实现端到端的隐式轨迹筛选，在速度-精度权衡上建立了新的最优边界。



端到端自动驾驶旨在从原始传感器输入直接输出规划轨迹，省去传统模块化管线中的中间表征与手工规则。近年来，基于生成式模型的规划方法因其天然的多模态能力受到广泛关注——它们不再仅输出一条确定性轨迹，而是从学习到的分布中采样多条候选轨迹，以覆盖真实驾驶场景中的多种合理行为（如直行、变道、让行）。然而，现有生成式规划方法在两个关键维度上存在结构性瓶颈。

**瓶颈一：离散锚点词汇表限制轨迹空间的连续覆盖。** 以 **VADv2**（arXiv 2024）、**Hydra-MDP**（arXiv 2024）、**DiffusionDrive**（Yang et al., CVPR 2025）和 **GoalFlow**（Xing et al., CVPR 2025）为代表的主流方法，普遍依赖一组预定义的离散锚点（anchor）或目标点（goal）作为生成过程的“骨架”。这些锚点通过对训练集轨迹聚类得到，构成一个有限的轨迹词汇表。生成模型在推理时从该词汇表中选择锚点，再围绕其进行轨迹补全或去噪。这一策略在分布内场景下有效，但当遇到锚点词汇表无法覆盖的分布外场景时——例如异常曲率的弯道、非典型路口拓扑——模型缺乏在连续轨迹空间中进行灵活外推的能力，导致规划质量显著退化。Figure 2 中的失败案例直接揭示了这一缺陷：锚点引导模型在面对词汇表外场景时无法生成包含最优轨迹的候选集，而本文方法则能覆盖真实解。

**瓶颈二：标准流匹配的多步迭代推理代价高且存在数值误差。** 流匹配（Flow Matching）作为一类新兴的生成范式，通过学习常微分方程（ODE）定义的瞬时速度场 $v_\theta(z_t, t)$，将简单先验分布连续变换为数据分布：

$$
\left\{ \begin{array} { l } { \frac { d z _ { t } } { d t } = v _ { \theta } ( z _ { t } , t ) } \\ { z _ { 0 } = x _ { 0 } . } \end{array} \right.
$$

在推理时，需通过多步 ODE 求解器（如 Euler 或 Runge-Kutta）逐步积分，计算开销与步数线性相关。以 **GoalFlow** 为例，其推理速度仅约 11.4 FPS，难以满足自动驾驶对实时性的严苛要求。同时，离散化求解过程引入的截断误差会在长时域预测中累积，进一步损害轨迹精度。

**动机：从“离散锚点+多步生成”到“连续先验+单步生成”。** 上述两个瓶颈共享一个深层根源：对离散化表征的过度依赖——无论是轨迹空间的离散锚点词汇表，还是时间维度上的离散 ODE 求解步。本文的核心动机在于同时打破这两重离散化约束：在空间维度，用连续的多模态先验分布取代固定锚点集；在时间维度，将多步 ODE 求解压缩为单步映射。这一思路直接催生了 MeanFuser 的两大技术支柱——高斯混合噪声（GMN）先验与 MeanFlow 单步采样——以及配套的自适应重建模块（ARM），从而在保持甚至超越多模态规划精度的同时，实现数量级的推理加速。



## 核心方法与创新机理

MeanFuser 的核心创新围绕一个瓶颈问题展开：**现有生成式端到端规划方法依赖离散锚点词汇表或标准高斯噪声，无法充分覆盖连续轨迹空间，且多步采样导致推理效率低下**。为此，本文从三个维度对生成式规划范式进行了系统性重构。

### 创新一：高斯混合噪声先验（GMN）——从离散锚点到连续多模态分布

传统基于锚点的方法（如 **VADv2**、**DiffusionDrive**（Yang et al., CVPR 2025）、**GoalFlow**（Xing et al., CVPR 2025））需要预定义一组离散的轨迹锚点或目标点作为生成先验。这种离散词汇表存在根本性缺陷：当测试场景的分布偏离训练集时，固定的锚点集合无法覆盖最优轨迹所在区域，导致分布外（OOD）场景下的规划失败。

MeanFuser 提出的解决方案是将先验分布建模为**高斯混合噪声（Gaussian Mixture Noise, GMN）**：

$$p _ { 0 } : = \sum _ { k = 1 } ^ { K } \pi _ { k } \mathcal { N } ( \mu _ { k } , \sigma _ { k } ^ { 2 } \cdot I )$$

其构建过程为：对训练集中的专家轨迹进行差分计算和 Min-Max 归一化，随后通过聚类获得 $K$ 个高斯分量的均值 $\mu_k$ 和协方差 $\sigma_k^2 \cdot I$。这种连续先验分布从根本上消除了对固定锚点词汇表的依赖，使模型能够从连续轨迹空间的任意区域进行采样，从而在 OOD 场景下保持鲁棒性。

**证据强度**：消融实验（Table 4）显示，在 TransFuser 基线上引入 GMN（M1）带来 **+0.9 PDMS** 的提升；多模态性指标 $\mathcal{D}$ 从 0.25 提升至 0.30（Table 8），综合指标 $\mathcal{M}_{DP} = \mathcal{D} \times PDMS$ 提升 20.84%。Figure 2 的失败案例可视化进一步证实，锚点引导模型在分布外场景下失效，而 GMN 生成的候选轨迹能覆盖最优解。

### 创新二：MeanFlow 恒等式——从多步 ODE 求解到单步平均速度场

标准流匹配（Flow Matching）方法学习瞬时速度场 $v_\theta(z_t, t)$，并通过求解常微分方程将噪声样本转换为数据样本：

$$\left\{ \begin{array} { l } { \frac { d z _ { t } } { d t } = v _ { \theta } ( z _ { t } , t ) } \\ { z _ { 0 } = x _ { 0 } . } \end{array} \right.$$

这种范式存在两个固有问题：① 多步 ODE 求解带来推理延迟和数值误差累积；② 瞬时速度场的学习信号稀疏，训练不够稳定。

MeanFuser 将 **MeanFlow 恒等式**引入端到端规划，直接学习平均速度场 $u_\theta(z_t, r, t)$，其定义为：

$$u ( z _ { t } , r , t ) \triangleq \frac { 1 } { t - r } \int _ { r } ^ { t } v ( z _ { \tau } , \tau ) d \tau$$

MeanFlow 恒等式建立了瞬时速度与平均速度及其时间导数的精确关系：

$$u ( z _ { t } , r , t ) = v ( z _ { t } , t ) - ( t - r ) \frac { d } { d t } u ( z _ { t } , r , t )$$

基于此，模型只需学习平均速度场，即可通过**单步生成**获得数据样本：

$$x _ { 1 } = x _ { 0 } + 1 \cdot u _ { \theta } ( x _ { 0 } , 0 , 1 )$$

训练时采用 L2 损失最小化预测平均速度与目标之间的差异：

$$\mathcal { L } ( \theta ) = \mathbb { E } \| u _ { \theta } ( z _ { t } , r , t ) - \mathrm { s g } ( u _ { \mathrm { t g t } } ) \| _ { 2 } ^ { 2 }$$

**因果机制**：从瞬时速度场到平均速度场的建模对象转换，使得原本需要多步 ODE 求解的生成过程压缩为一步，推理速度获得数量级提升。同时，平均速度场的学习信号更为稠密（整个区间上的积分而非单点瞬时值），训练更加稳定。

**证据强度**：Table 3 显示 MeanFuser 的规划模块推理速度达 **434 FPS**，整体推理速度 **59 FPS**，分别比 GoalFlow（11.4 FPS）快 5.20×、比 Hydra-MDP（22.3 FPS）快 2.65×、比 DiffusionDrive（38.1 FPS）快 1.55×。消融实验（Table 4）表明，仅将 TransFuser 的 MLP 解码器替换为 MeanFlow 解码器（M0）即可带来 **+3.3 PDMS** 的提升。

### 创新三：自适应重建模块（ARM）——从显式评分到隐式选择与重建

现有方法（如 **Hydra-MDP**、**WoTE**（ICCV 2025））依赖显式评分函数或手工规则从候选轨迹中选择最优解，这引入了额外的计算开销和人工设计偏差。

MeanFuser 设计了**自适应重建模块（Adaptive Reconstruction Module, ARM）**，通过交叉注意力机制实现候选轨迹的隐式评估与选择。具体而言，ARM 将所有采样的候选轨迹与 BEV 上下文特征 $c_{bev}$ 进行交叉注意力融合，模型通过注意力权重隐式判断：① 是否存在满意的候选轨迹，若存在则选择之；② 若所有候选均不理想，则基于上下文特征重建一条更优轨迹。

**因果机制**：ARM 的隐式选择机制避免了显式评分函数的设计与调优，同时“选择或重建”的双模式策略使模型在候选质量不足时具备自纠正能力，而非被迫从次优解中妥协。

**证据强度**：消融实验（Table 4）显示，在 GMN 基础上引入 ARM（M2）额外带来 **+0.8 PDMS** 的提升，最终达到 89.0 PDMS。该模块的轻量级设计（仅增加少量参数）使其在提升性能的同时几乎不影响推理速度。

### 创新协同效应

三个创新并非孤立存在，而是形成了有机的协同链路：**GMN 提供连续、多模态的先验分布 → MeanFlow 单步采样高效生成多样化的候选轨迹 → ARM 隐式评估并自适应选择或重建最优轨迹**。这条链路从先验建模、生成效率到决策机制完成了对生成式规划范式的端到端重构，使得 MeanFuser 在 NAVSIM v1（89.0 PDMS）、NAVSIM v2（89.5 EPDMS）和 CARLA Longest6（DS 70.08）三个基准上均取得最优性能。



MeanFuser 的整体架构围绕“单步生成 + 隐式选择”这一核心思路设计，由四个串联模块构成：**场景上下文编码器 → 高斯混合噪声先验 → 多模态轨迹采样 → 自适应重建模块**。其设计目标是在不依赖离散锚点词汇表的前提下，以极低的推理延迟生成覆盖连续轨迹空间的多模态候选，并通过轻量级注意力机制隐式筛选或重建最优规划。

### 数据流与模块关系

前向推理的数据流如下（参见 Figure 3）：

![[assets/figures/papers/paper_list_l2544_https_arxiv_org_abs_2602_20060/figures/003_Figure_3.jpg]]
*Figure 3: Overall architecture of MeanFuser. Training: During training, both the images and ego-vehicle states are encoded into context features, with auxiliary supervision from mapping tasks. The model is conditioned on these context features to learn the average velocity field*

1. **场景上下文编码器**接收多视图图像与自车状态，输出 BEV（鸟瞰视角）上下文特征 $\mathbf{c}_{\mathrm{bev}}$，作为下游所有模块的条件信号。
2. **高斯混合噪声先验（GMN）**从 $K$ 个高斯分量中并行采样 $K$ 个噪声向量 $\{x_0^{(k)}\}_{k=1}^K$，每个分量对应一种潜在的驾驶模式。
3. **多模态轨迹采样模块**以场景条件 $\mathbf{c}$ 和噪声 $x_0^{(k)}$ 为输入，通过 MeanFlow 解码器**单步**前向计算，直接生成 $K$ 条候选轨迹 $\{\hat{\tau}^{(k)}\}_{k=1}^K$。
4. **自适应重建模块（ARM）**将 $K$ 条候选轨迹编码后与 $\mathbf{c}_{\mathrm{bev}}$ 做交叉注意力融合，由 Projector 输出最终规划轨迹 $\hat{\tau}$。

训练时，系统额外引入地图解码器提供辅助监督，总损失为轨迹 L1 损失、流匹配损失与地图损失的加权和：

$$\mathcal{L} = \lambda_1 \mathcal{L}_{\tau} + \lambda_2 \mathcal{L}_{\mathrm{flow}} + \lambda_3 \mathcal{L}_{\mathrm{map}}$$

### 关键设计决策

**从离散锚点到连续先验。** 现有方法（如 **VADv2**、**DiffusionDrive** (Yang et al., CVPR 2025)）依赖离散的锚点词汇表来引导多模态生成，但固定锚点无法覆盖完整的连续轨迹空间，在分布外场景下容易失效（Figure 2 提供了此类失败案例的可视化证据）。MeanFuser 以高斯混合噪声（GMN）取代锚点词汇表，将先验分布定义为 $K$ 个高斯分量的混合：

$$p_0 := \sum_{k=1}^{K} \pi_k \mathcal{N}(\mu_k, \sigma_k^2 \cdot I)$$

其中 $\mu_k$、$\sigma_k$ 通过对训练集中专家轨迹的差分进行聚类获得。这一设计使先验具备连续性与多模态性，从根本上消除了对固定词汇表的依赖。

**从多步 ODE 求解到单步生成。** 标准流匹配（如 **GoalFlow** (Xing et al., CVPR 2025)）需要求解瞬时速度场的 ODE 才能将噪声转换为轨迹，这导致推理需多步迭代，速度慢且存在数值误差。MeanFuser 引入 MeanFlow 恒等式，将建模对象从瞬时速度场 $v(z_t, t)$ 切换为平均速度场 $u(z_t, r, t)$，从而仅需一步即可完成生成：

$$x_1 = x_0 + 1 \cdot u_\theta(x_0, 0, 1)$$

这一设计是 MeanFuser 推理速度达到 59 FPS（规划模块 434 FPS）的核心原因，分别比 GoalFlow、Hydra-MDP、DiffusionDrive 快 5.20×、2.65×、1.55×。

**从显式评分到隐式选择与自适应重建。** 传统方法（如 **Hydra-MDP**、**WoTE** (ICCV 2025)）依赖显式评分函数或世界模型对候选轨迹进行排序选择，增加了额外的计算开销和手工设计成本。ARM 模块通过交叉注意力机制，让模型在 BEV 上下文中隐式评估所有候选轨迹的质量：当存在满意轨迹时，注意力权重自然倾向于选择该轨迹；当所有候选均不理想时，模块则融合多源信息重建一条新轨迹。这一“隐式选择/重建”机制无需额外的评分网络，轻量且端到端可学习。

### 模块级证据与消融验证

消融实验（Table 4）量化了各模块的独立贡献：以 **TransFuser** (Chitta et al., IEEE TPAMI) 为基线，仅将 MLP 解码器替换为 MeanFlow 解码器（M0）即可带来 **+3.3 PDMS** 的提升；进一步引入 GMN（M1）额外增加 **+0.9 PDMS**；再加入 ARM（M2）再增加 **+0.8 PDMS**，最终达到 89.0 PDMS。这一递进式消融清晰地表明，三个核心模块各自贡献显著且相互补充。

关于 GMN 的配置，实验表明高斯分量数 $K=8$ 时性能最优（PDMS 89.0），继续增大至 16 或 32 反而导致轻微下降（Table 6），说明 8 个分量已能充分覆盖 NAVSIM 场景下的驾驶模式多样性。此外，手动设计的 GMN 与数据驱动的聚类 GMN 相比，PDMS 仅下降 0.45%（Table 7），证明方法对数据集先验的依赖程度较低，具备较好的泛化潜力。

**需要手动验证的点：** ARM 模块的“何时选择、何时重建”的决策边界目前缺乏可解释性分析，论文未提供注意力权重可视化或决策统计，该机制的透明性仍需进一步研究。

### 补充图表

![[assets/figures/papers/paper_list_l2544_https_arxiv_org_abs_2602_20060/figures/001_Figure_1.jpg]]
*Figure 1: (a) illustrates the differences between our proposed method and existing generative approaches, highlighting the introduction of Gaussian mixture noise to replace anchor vocabularies, one-step sampling, and the adaptive reconstruction module. (b) shows the advantages of MeanFuser over GoalFlow[33], Hydra-MDP[20], and DiffusionDrive[22] in terms of closed-loop performance, inference speed and plan module inference speed*



### 3.1 问题形式化

端到端规划任务将传感器观测序列映射为未来轨迹。给定时间步 $i$ 的观测 $\mathcal{O}_i$（包含多视角图像、自车状态与导航指令），模型需预测自车在未来 $T$ 个时间步的轨迹点序列 $\tau = \{(x_t, y_t)\}_{t=1}^{T}$。多模态规划进一步要求模型同时输出 $K$ 条覆盖不同驾驶意图的候选轨迹。

### 3.2 MeanFlow 速度场建模

标准流匹配（Flow Matching）通过学习瞬时速度场 $v_\theta(z_t, t)$ 将先验分布 $p_0$ 中的样本 $x_0$ 变换为目标数据分布 $p_1$ 中的样本 $x_1$，其变换过程由以下常微分方程（ODE）描述：

$$
\left\{ \begin{array} { l } { \frac { d z _ { t } } { d t } = v _ { \theta } ( z _ { t } , t ) } \\ { z _ { 0 } = x _ { 0 } . } \end{array} \right.
$$

该过程需要多步数值积分（如 Euler 或 Runge-Kutta 求解器），导致推理延迟高且累积数值误差。

MeanFlow 框架通过直接建模**平均速度场**来规避多步求解。定义时间区间 $[r, t]$ 上的平均速度场为：

$$
u ( z _ { t } , r , t ) \triangleq \frac { 1 } { t - r } \int _ { r } ^ { t } v ( z _ { \tau } , \tau ) d \tau
$$

MeanFlow 的核心在于建立了瞬时速度与平均速度及其时间导数之间的精确恒等关系：

$$
u ( z _ { t } , r , t ) = v ( z _ { t } , t ) - ( t - r ) \frac { d } { d t } u ( z _ { t } , r , t )
$$

基于该恒等式，模型可直接学习平均速度场 $u_\theta$，并通过以下单步公式从噪声 $x_0$ 生成数据 $x_1$：

$$
x _ { 1 } = x _ { 0 } + 1 \cdot u _ { \theta } ( x _ { 0 } , 0 , 1 )
$$

训练时，通过最小化预测平均速度与停止梯度（stop-gradient）后的目标平均速度之间的 L2 距离来优化模型：

$$
\mathcal { L } ( \theta ) = \mathbb { E } \| u _ { \theta } ( z _ { t } , r , t ) - \mathrm { s g } ( u _ { \mathrm { t g t } } ) \| _ { 2 } ^ { 2 }
$$

### 4.1 场景上下文编码器

场景上下文编码器沿用 TransFuser 架构（Chitta et al., IEEE TPAMI），由图像编码器（ResNet-34）提取多视角图像特征，状态编码器处理自车速度、航向等状态量，并通过跨模态 Transformer 融合得到鸟瞰图（BEV）上下文特征 $\mathbf{c}_{\text{bev}}$。同时辅以地图解码器提供语义分割辅助监督。

### 4.2 高斯混合噪声先验

传统流匹配使用标准高斯分布作为先验 $p_0$，而基于锚点的方法依赖离散轨迹词汇表。MeanFuser 提出**高斯混合噪声（Gaussian Mixture Noise, GMN）**，将先验建模为 $K$ 个高斯分量的混合分布：

$$
p _ { 0 } : = \sum _ { k = 1 } ^ { K } \pi _ { k } \mathcal { N } ( \mu _ { k } , \sigma _ { k } ^ { 2 } \cdot I )
$$

GMN 的构建过程如下：首先对训练集中的专家轨迹计算相邻时间步的差分 $\Delta \tau_j$，然后通过 Min-Max 归一化将其映射到统一尺度：

$$
\Delta \tau _ { j } = \frac { \Delta \tau _ { j } - \Delta \tau _ { \mathrm { m e a n } } } { \operatorname* { m a x } ( \Delta \tau _ { \mathrm { m a x } } - \Delta \tau _ { \mathrm { m e a n } } , \Delta \tau _ { \mathrm { m e a n } } - \Delta \tau _ { \mathrm { m i n } } ) }
$$

归一化后的轨迹差分经聚类得到 $K$ 个簇，每个簇的均值和方差分别作为对应高斯分量的 $\mu_k$ 和 $\sigma_k^2$。这种连续先验消除了对固定锚点词汇表的依赖，使模型能够覆盖更完整的轨迹空间。

### 4.3 多模态轨迹采样模块

多模态轨迹采样模块以场景上下文特征 $\mathbf{c}$ 为条件，从 GMN 先验中并行采样 $K$ 个噪声样本，通过 MeanFlow 解码器单步生成 $K$ 条候选轨迹。该过程的训练损失为 L1 形式的流损失：

$$
\mathcal { L } _ { f l o w } = \| u _ { \theta } ( \tau _ { t } , r , t | \mathbf { c } ) - \mathrm { s g } ( u _ { \mathrm { t g t } } ) \| _ { 1 }
$$

### 4.4 自适应重建模块

自适应重建模块（Adaptive Reconstruction Module, ARM）负责从 $K$ 条候选轨迹中隐式选择最优轨迹或重建新轨迹。具体而言，所有候选轨迹与 BEV 上下文特征 $\mathbf{c}_{\text{bev}}$ 通过交叉注意力层进行融合，注意力权重隐式评估各候选轨迹的质量，随后由 Projector 输出最终规划轨迹 $\hat{\tau}$。最终轨迹通过 L1 损失监督：

$$
\mathcal { L } _ { \tau } = \| \tau - \hat { \tau } \| _ { 1 }
$$

总体训练目标由三项损失加权求和构成：

$$
\mathcal { L } = \lambda _ { 1 } \mathcal { L } _ { \tau } + \lambda _ { 2 } \mathcal { L } _ { f l o w } + \lambda _ { 3 } \mathcal { L } _ { m a p }
$$

其中 $\mathcal{L}_{\text{map}}$ 为地图解码器的辅助语义分割损失。

### 多模态性评估指标

为量化轨迹生成的多模态多样性，论文定义了多样性指标 $\mathcal{D}$，基于 $K$ 条轨迹在各时刻包围框的交并比平均值：

$$
\mathcal { D } = 1 - \frac { 1 } { T _ { f } } \sum _ { i = 1 } ^ { T _ { f } } \frac { \bigcap _ { k = 1 } ^ { K } \mathrm { A r e a } ( \hat { \tau } _ { k i } ) } { \bigcup _ { k = 1 } ^ { K } \mathrm { A r e a } ( \hat { \tau } _ { k i } ) }
$$

进一步定义综合指标 $\mathcal{M}_{\mathbf{DP}}$，将多样性与规划性能统一衡量：

$$
\mathcal { M } _ { \bf D P } = \mathcal { D } \times P D M S
$$

### 补充图表

![[assets/figures/papers/paper_list_l2544_https_arxiv_org_abs_2602_20060/figures/008_Figure_4.jpg]]
*Figure 4: Visualization of sampling from different Gaussian components. Parallel sampling of trajectories from distinct Gaussian components can generate diverse driving styles, ranging from conservative to aggressive*

![[assets/figures/papers/paper_list_l2544_https_arxiv_org_abs_2602_20060/figures/014_Figure_7.jpg]]
*Figure 7: Visualization of alternative approaches for generating Gaussian Mixture Noise (GMN). (a) Mean and standard deviation are derived from clustered expert demonstrations in the training set. (b) Mean and standard deviation are obtained through manually design*



## 实验与关键发现

### 主实验结果

MeanFuser 在两个版本的 NAVSIM 基准和 CARLA Longest6 闭环仿真上均取得了领先性能。在 NAVSIMv1 navtest 上，该方法达到 **89.0 PDMS**，超越此前最优的 **DiffusionDrive**（88.1 PDMS）0.9 个点，并显著高于基于目标点引导流匹配的 **GoalFlow**（85.7 PDMS）（Table 1）。在更严格的 NAVSIMv2 上，MeanFuser 以 **89.5 EPDMS** 取得最优结果（Table 2）。在 CARLA Longest6 闭环测试中，MeanFuser 的 Driving Score 达到 **70.08 ± 3.20**，较 DiffusionDrive（64.27 ± 2.43）提升 5.81 分，且 Route Completion 和 Infraction Score 均有明显改善（Table 5）。

![[assets/figures/papers/paper_list_l2544_https_arxiv_org_abs_2602_20060/figures/004_Table_1.jpg]]
*Table 1: Performance on the NAVSIMv1 navtest benchmark. “C” denotes camera, and “L” denotes LiDAR. * indicates results reported from the official papers*

![[assets/figures/papers/paper_list_l2544_https_arxiv_org_abs_2602_20060/figures/005_Table_2.jpg]]
*Table 2: Performance of the NAVSIMv2 navtest benchmark. † denotes testing with the official checkpoint*

![[assets/figures/papers/paper_list_l2544_https_arxiv_org_abs_2602_20060/figures/011_Table_5.jpg]]
*Table 5: Longest6 Benchmark Results. We show the mean and std for all metrics (RC: Route Completion, IS: Infraction Score. DS: Driving Score)*

推理效率方面，在统一使用 NVIDIA H20 GPU 的条件下，MeanFuser 的整体推理速度达到 **59 FPS**，分别是 GoalFlow（11.4 FPS）的 5.20 倍、**Hydra-MDP**（22.3 FPS）的 2.65 倍、DiffusionDrive（38.1 FPS）的 1.55 倍。若仅考虑规划模块（排除感知编码器），MeanFuser 的规划推理速度高达 **434 FPS**，参数量仅 54.6M，在速度-精度权衡上显著优于同类生成式方法（Table 3）。

![[assets/figures/papers/paper_list_l2544_https_arxiv_org_abs_2602_20060/figures/006_Table_3.jpg]]
*Table 3: Model parameter size, inference speed, and performance. Bold and underlined values denote the best and secondbest results, respectively. “Dim” indicates the number of hidden neurons in the model, “FPS” represents the median inference speed measured on a single NVIDIA H20 GPU over multiple runs, and “Plan FPS” refers to the inference speed of trajectory planning excluding the perception encoder*

### 消融实验

**模块贡献消融。** 以 **TransFuser**（Chitta et al., IEEE TPAMI）为基线，逐步叠加 MeanFuser 的各组件：仅将 MLP 解码器替换为 MeanFlow 解码器（M0）即带来 **+3.3 PDMS** 的提升；进一步引入高斯混合噪声先验（M1）额外增加 **+0.9 PDMS**；再增加自适应重建模块（M2）再增加 **+0.8 PDMS**，最终达到 89.0 PDMS（Table 4）。这表明三个核心组件——MeanFlow 单步生成、GMN 连续先验、ARM 隐式选择——均对性能有独立且可叠加的贡献。

**高斯分量数量消融。** 在 GMN 中，高斯分量数 K=8 时 PDMS 达到最优的 89.0；当 K 增至 16 或 32 时，性能反而轻微下降（Table 6）。这说明 8 个分量已能充分覆盖轨迹空间的多模态结构，过多的分量可能引入冗余噪声，增加学习难度。

**GMN 生成方式消融。** 对比基于训练集专家轨迹聚类得到的 GMN 与手动设计的 GMN（均值和标准差由人工设定），后者仅导致 PDMS 轻微下降 0.45%（Table 7），且两者的轨迹分布可视化高度相似（Figure 7）。这证明该方法不依赖于特定固定数据集，具备较强的泛化潜力。

**多模态性与性能联合消融。** 引入 GMN 不仅提升 PDMS，还显著增加了轨迹多样性指标 D（从 0.25 到 0.30），使综合指标 M_DP（D × PDMS）提升 20.84%（Table 8）。这说明 GMN 的连续多模态先验确实生成了更具差异化的候选轨迹，而非仅靠单一模式拟合真值。

### 失败模式与局限性

尽管 MeanFuser 在整体指标上表现优异，论文仍披露了若干失败场景和局限性。在 Figure 2 所示的失败案例中，基于锚点的模型（GoalFlow、DiffusionDrive）因离散词汇表无法覆盖全部轨迹空间而规划失败，而 MeanFuser 的连续先验能够生成包含最优解的候选集，在该场景下成功规划。然而，以下局限仍需关注：

![[assets/figures/papers/paper_list_l2544_https_arxiv_org_abs_2602_20060/figures/002_Figure_2.jpg]]
*Figure 2: Failure scene visualization. Anchor-guided models (GoalFlow, DiffusionDrive) fail due to the inability of discrete vocabularies to cover the entire trajectory space, while our model generates proposals that encompass the optimal trajectories*

- **先验参数固定**：高斯混合系数 π_k 固定为 1，更优的参数化方式（如可学习的混合权重）尚未探索。
- **数据依赖性**：GMN 的生成依赖训练集上的专家轨迹聚类，尽管手动设计可近似替代，但仍需一定的先验知识来设定合理的均值和方差范围。
- **仿真验证局限**：所有实验均在 NAVSIM 和 CARLA 仿真平台上进行，未在真实世界环境中测试，sim-to-real 迁移性能未知。
- **ARM 可解释性不足**：自适应重建模块通过交叉注意力权重隐式决定是选择现有候选轨迹还是重建新轨迹，其决策过程缺乏可解释性，难以从外部判断模型何时触发重建。

### 重要图表结论

- **Figure 1**：方法概览与性能对比，直观展示了 MeanFuser 以 GMN 替代锚点词汇表、单步采样和 ARM 的核心差异，以及在闭环性能与推理速度上对 GoalFlow、Hydra-MDP、DiffusionDrive 的全面优势。
- **Figure 4**：不同高斯分量的采样可视化，展示了从不同分量并行采样可生成从保守到激进的多样化驾驶风格，验证了 GMN 的多模态表达能力。
- **Figure 5**：多模态轨迹可视化，左侧为专家演示轨迹，右侧为模型推断的直行与左变道两种模式，直观展示了模型对场景多模态性的捕获能力。
- **Table 4**：模块消融表，清晰呈现了 MeanFlow 解码器、GMN 和 ARM 各自对 PDMS 的增量贡献，是理解方法设计有效性的核心证据。
- **Table 8**：多模态性与性能联合消融，揭示了 GMN 在提升规划精度的同时显著增强了轨迹多样性，证明连续先验对多模态生成的关键作用。

![[assets/figures/papers/paper_list_l2544_https_arxiv_org_abs_2602_20060/figures/007_Table_4.jpg]]
*Table 4: Ablation study on the impact of each module. Base denotes the TransFuser[7] baseline*

![[assets/figures/papers/paper_list_l2544_https_arxiv_org_abs_2602_20060/figures/016_Table_8.jpg]]
*Table 8: Comparison of multimodality and performance. (GMN: Gaussian Mixture Noise. K: number of multimodal trajectories; D: multimodality metric.)*

### 补充图表

![[assets/figures/papers/paper_list_l2544_https_arxiv_org_abs_2602_20060/figures/012_Table_6.jpg]]
*Table 6: Number of Gaussian components and model performance*



## 定位与知识库关联

### 端到端规划范式的演进定位

MeanFuser 处于端到端自动驾驶（End-to-End Autonomous Driving）中“感知-规划一体化”的研究脉络。该脉络的核心目标是直接从原始传感器输入（多视图相机、自车状态）输出可执行的驾驶轨迹，避免显式的模块化中间表示（如检测、跟踪、预测）。在此框架下，**UniAD**（Hu et al., CVPR 2023）率先将规划任务统一为 Transformer 查询式的端到端框架，但其输出为单模态确定性轨迹，无法建模驾驶行为的固有不确定性。MeanFuser 继承了端到端范式，但将问题从确定性回归转向了多模态生成式建模。

### 生成式规划方法的瓶颈与突破

当前主流的多模态生成式规划方法可分为两类：基于扩散模型的方法和基于流匹配的方法。

**基于扩散模型的方法**以 **DiffusionDrive**（Yang et al., CVPR 2025）为代表。其核心思路是通过对锚点轨迹（anchor trajectories）进行去噪扩散，生成多条候选轨迹，再通过评分函数选择最优解。然而，该方法依赖离散的锚点词汇表来覆盖轨迹空间，当场景超出词汇表覆盖范围时（即分布外场景），生成的候选轨迹可能无法包含最优解。Figure 2 的失败案例可视化直接展示了这一瓶颈：锚点引导模型在复杂场景下无法生成包含最优轨迹的候选集。

**基于流匹配的方法**以 **GoalFlow**（Xing et al., CVPR 2025）为代表。GoalFlow 通过目标点引导的流匹配生成多模态轨迹，但其使用标准的瞬时速度场建模，需要多步 ODE 求解才能从噪声分布变换到数据分布。这导致推理速度较慢（仅 11.4 FPS），且多步积分累积的数值误差可能影响轨迹精度。

MeanFuser 针对上述两类方法的共同瓶颈——离散先验与多步采样——进行了系统性改进：

1. **连续先验替代离散词汇表**：引入高斯混合噪声（Gaussian Mixture Noise, GMN）作为连续先验分布，通过对专家轨迹聚类得到 $K$ 个高斯分量的混合分布，从根源上消除了对固定锚点词汇表的依赖。这一设计使得先验分布能够平滑地覆盖连续轨迹空间，理论上可生成任意驾驶模式下的候选轨迹。

2. **单步生成替代多步求解**：将 MeanFlow 恒等式引入端到端规划，直接学习噪声与数据分布之间的平均速度场，而非瞬时速度场。基于恒等式 $u(z_t, r, t) = v(z_t, t) - (t-r)\frac{d}{dt}u(z_t, r, t)$，模型仅需一步即可完成从噪声到轨迹的变换（$x_1 = x_0 + 1 \cdot u_\theta(x_0, 0, 1)$），消除了多步 ODE 求解的计算开销和数值误差。

### 候选轨迹选择机制的差异化

在多模态候选轨迹生成后，如何选择最终输出的规划轨迹是另一个关键设计空间。

**Hydra-MDP**（arXiv 2024）采用显式评分函数对候选轨迹进行排序选择，评分函数通常基于手工设计的代价项（如碰撞风险、舒适度、路径效率等）。**WoTE**（ICCV 2025）和 **World4Drive**（ICCV 2025）则利用世界模型（world model）对候选轨迹的未来演变进行前向模拟，基于模拟结果评估轨迹质量。这些方法的共同特点是需要一个显式的、可解释的评估-选择流程。

MeanFuser 的自适应重建模块（Adaptive Reconstruction Module, ARM）采取了截然不同的路径：通过交叉注意力机制将候选轨迹与 BEV 上下文特征融合，隐式地学习评估和选择策略。ARM 不仅能够从现有候选中选择最优轨迹，还具备“重建”能力——当所有候选轨迹均不满足隐式标准时，模型可以生成一条全新的轨迹。这种隐式机制的优势在于避免了手工设计评分函数的局限性，但也带来了可解释性不足的问题（见下文局限）。

### 与基线方法的定量关系

在相同感知骨干（TransFuser 的 ResNet-34）下，MeanFuser 在 NAVSIMv1 上取得 89.0 PDMS，相较于 DiffusionDrive（88.1）和 GoalFlow（85.7）分别提升 +0.9 和 +3.3（Table 1）。在 NAVSIMv2 上，MeanFuser 以 89.5 EPDMS 取得最优性能（Table 2）。推理速度方面，MeanFuser 的 59 FPS 分别比 GoalFlow（11.4 FPS）、Hydra-MDP（22.3 FPS）、DiffusionDrive（38.1 FPS）快 5.20×、2.65×、1.55×（Table 3）。消融实验进一步表明，在 TransFuser 基础上去除锚点词汇表并引入 MeanFlow 解码器（M0）即可带来 +3.3 PDMS 的提升，而 GMN（M1）和 ARM（M2）分别额外贡献 +0.9 和 +0.8 PDMS（Table 4）。

### 适用边界与局限

1. **先验分布的参数化依赖**：GMN 的生成依赖于训练数据集上的专家轨迹聚类来获取高斯分量的均值和方差。虽然手动设计的 GMN 仅导致 PDMS 轻微下降 0.45%（Table 7），但完全脱离数据先验的通用先验设计仍有待探索。此外，当前混合系数 $\pi_k$ 固定为 1，更优的参数化方式（如可学习的混合系数或与场景条件相关的动态权重）尚未被研究。

2. **ARM 的可解释性不足**：ARM 模块通过注意力权重隐式地判断候选轨迹质量并决定是否重建，这一过程缺乏透明度。无法从外部理解模型在何种条件下选择现有轨迹、在何种条件下触发重建，也难以诊断选择错误的原因。这是隐式学习机制固有的权衡——以可解释性换取灵活性和性能。

3. **验证环境的局限性**：当前所有实验均在仿真基准（NAVSIM v1/v2 和 CARLA Longest6）上完成，尚未在真实世界环境中验证。仿真到真实的域迁移（sim-to-real gap）是端到端自动驾驶方法面临的普遍挑战，MeanFuser 的 GMN 先验和单步生成策略在真实传感器噪声和动态环境下的鲁棒性仍有待检验。

4. **长时域与复杂交互的稳定性**：单步 MeanFlow 采样在 4 秒预测时域（8 个航点，2 Hz）下表现良好，但在更长时域或涉及密集交互的动态场景下，单步生成是否仍能保持足够的精度和多样性，目前缺乏实验证据。

### 开放问题

1. **先验分布的自适应学习**：能否自动学习或动态调整高斯混合分量的数量 $K$ 以及混合系数 $\pi_k$，使先验分布能够根据场景复杂度自适应地调整其表达能力和采样效率？

2. **驾驶风格的可控生成**：GMN 的不同高斯分量在可视化中展现出从保守到激进的不同驾驶风格（Figure 4）。能否显式地将特定分量与驾驶风格关联，实现用户可定制的自动驾驶行为？这需要建立分量语义与驾驶风格之间的可解释映射。

3. **ARM 重建机制的透明化**：是否可以通过引入额外的辅助损失项（如重建概率的熵正则化）或结构约束（如显式的候选质量预测头）来增强 ARM 选择/重建决策的可解释性和可调试性，同时保持其性能优势？

4. **与基于世界模型的方法的融合**：MeanFuser 的单步生成效率与 ARM 的隐式选择机制，是否可以与 **WoTE** 或 **World4Drive** 等基于世界模型的前向模拟评估相结合，形成“快速生成 + 精细验证”的两阶段规划框架？这可能在保持高推理速度的同时进一步提升安全性。



## 原文 PDF

![[paperPDFs/CVPR_2026/MeanFuser_Fast_One_Step_Multi_Modal_Trajectory_Generation_and_Adaptive_Reconstruction_via_MeanFlow_for_End_to_End_Autonomous_Driving.pdf]]
