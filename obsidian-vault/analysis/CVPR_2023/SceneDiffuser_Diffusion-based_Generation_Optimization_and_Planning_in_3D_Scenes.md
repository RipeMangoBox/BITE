---
title: "SceneDiffuser: Diffusion-based Generation, Optimization, and Planning in 3D Scenes"
type: paper
paper_level: A
venue: CVPR
year: 2023
pdf_ref: "paperPDFs/CVPR_2023/SceneDiffuser:_Diffusion-based_Generation,_Optimization,_and_Planning_in_3D_Scenes.pdf"
project_link: https://scenediffuser.github.io
code_link: https://github.com/scenediffuser/Scene-Diffuser
aliases:
- SceneDiffuser
tags:
- CVPR_2023
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
- topic/generative_models_diffusion
core_operator: 将扩散模型的逐步去噪过程与物理优化和目标规划梯度引导相结合，在采样过程中逐步注入物理约束和任务目标，从而在保持生成多样性的同时强制生成符合物理规律且朝向目标的轨迹。
primary_logic: 通过以规划即采样（planning as sampling）的理念，将场景条件生成、物理优化和目标规划统一在扩散模型的引导采样框架内，解决了现有方法中模块分离和后验崩塌问题，实现了具有场景感知、物理合理且目标导向的通用生成、优化与规划模型。
claims:
- SceneDiffuser integrates physics-based objective into each step of the sampling process as conditional guidance.
- SceneDiffuser jointly solves scene-aware generation, physics-based optimization, and goal-oriented planning through a unified iterative guided-sampling framework.
- Optimization-guided sampling improves plausible rate by 25% for human pose generation.
- PROX (human pose generation) 上 plausible rate (%) = 49.35 (SceneDiffuser w/ opt)
---

# SceneDiffuser: Diffusion-based Generation, Optimization, and Planning in 3D Scenes

> [!tip] 核心洞察
> 通过以规划即采样（planning as sampling）的理念，将场景条件生成、物理优化和目标规划统一在扩散模型的引导采样框架内，解决了现有方法中模块分离和后验崩塌问题，实现了具有场景感知、物理合理且目标导向的通用生成、优化与规划模型。

| 字段 | 内容 |
|------|------|
| 中文题名 | SceneDiffuser：基于扩散的三维场景生成、优化与规划 |
| 英文题名 | SceneDiffuser: Diffusion-based Generation, Optimization, and Planning in 3D Scenes |
| 会议/期刊 | CVPR 2023 |
| Links | [paper](https://arxiv.org/abs/2301.06015) · [Project](https://scenediffuser.github.io) · [Code](https://github.com/scenediffuser/Scene-Diffuser) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction #topic/generative_models_diffusion |
| Method | SceneDiffuser |
| Dataset | PROX, MultiDex, 3D navigation, Robot arm motion planning |

> [!tip] 效果简介
> - PROX (human pose generation) 上，plausible rate (%) 49.35 (SceneDiffuser w/ opt) vs 12.57 (cVAE w/o LHs) (+36.78)。
> - PROX (human motion generation) 上，plausible rate (%) 41.76 (SceneDiffuser w/ start) vs 16.24 (cVAE w/ start) (+25.52)。
> - MultiDex (dexterous grasp) 上，success rate (%) 71.25 (SceneDiffuser w/o opt) vs 14.06 (cVAE) (+57.19)。

## 概要

SceneDiffuser 是一个基于扩散模型的条件生成框架，旨在统一解决三维场景中的条件生成、物理优化与目标导向规划问题。先前基于条件变分自编码器（cVAE）的场景条件生成模型普遍存在后验崩塌，导致生成多样性严重不足；同时，生成、优化与规划模块长期分离，造成不同阶段输出不一致，难以泛化到新场景。SceneDiffuser 以“规划即采样”为核心理念，将扩散模型的逐步去噪过程与物理优化及规划目标的梯度引导相结合，在采样过程中逐步注入碰撞、接触、平滑度等物理约束以及目标到达条件，从而在保持生成多样性的同时强制输出物理合理且朝向目标的轨迹。

在方法定位上，SceneDiffuser 引入三个关键改动：将生成模型架构从 cVAE 替换为条件扩散模型，以缓解后验崩塌；将物理优化从后处理或末端约束转变为嵌入每一步去噪采样的引导梯度；将规划方式从独立规划器转变为基于轨迹生成的修复式采样框架。模型由场景编码器（Point Transformer 或 PointNet）、带交叉注意力的时间条件扩散模型、以及优化与规划引导模块构成，形成一个统一的迭代引导采样框架。

在涵盖人体姿态生成、人体动作生成、灵巧抓取生成、三维导航路径规划与机器人臂运动规划的五类任务上，SceneDiffuser 均展现出显著性能提升。在 PROX 人体姿态生成中，合理率从 cVAE 的 12.57% 提升至 49.35%；在 MultiDex 灵巧抓取中，成功率从 14.06% 提升至 71.25%；在三维导航路径规划中，成功率超过 73%，显著优于行为克隆等基线。消融实验进一步证实，优化引导采样使人体姿态合理率额外提升 25%，且缩放系数、修复帧数等超参数对最终性能有显著影响。

> **注意**：本文未标注具体的发表年份和会议/期刊，上述结论均基于论文原文及分析结果，若需引用请核实正式出版信息。

三维场景理解与交互是计算机视觉和机器人学的核心问题，涉及人体姿态估计、动作生成、灵巧抓取、路径规划等一系列任务。这些任务共享一个共同需求：在给定三维场景的条件下，生成物理合理且目标导向的轨迹。然而，现有方法在处理这一需求时面临两个根本性瓶颈。

**瓶颈一：生成多样性与物理合理性的冲突。** 当前主流的场景条件生成模型基于条件变分自编码器（cVAE），但cVAE存在严重的后验崩塌（posterior collapse）问题，导致生成样本的多样性严重不足。与此同时，物理合理性通常作为后处理步骤施加——即在生成完成后再进行可微分优化。这种分离式设计使得生成器与优化器之间存在不一致，生成器产出的轨迹可能无法被优化器有效修正，尤其在新场景中泛化能力有限。

**瓶颈二：生成、优化与规划的模块割裂。** 场景感知生成、物理约束优化和目标导向规划通常由三个独立模块分别处理。生成器负责产出候选轨迹，优化器施加物理约束，规划器则负责目标到达。这种流水线式架构不仅引入了模块间的误差累积，还使得整个系统难以端到端地适应新任务和新场景。例如，在机器人运动规划中，行为克隆（Behavior Cloning）等模仿学习方法虽然能学习场景条件策略，但缺乏对物理约束的显式建模，在长时域任务中成功率显著下降。

**核心动机：规划即采样。** SceneDiffuser的核心洞察在于，扩散模型的逐步去噪过程天然适合作为统一的生成、优化与规划框架。扩散模型通过逐步从噪声中恢复数据，避免了cVAE的后验崩塌问题，能够保持生成多样性。更重要的是，在每一步去噪采样中，可以注入物理优化目标（如碰撞避免、接触约束）和规划目标（如目标到达距离）的梯度作为条件引导，从而将生成、优化和规划统一在同一个迭代引导采样框架内。这一“规划即采样”（planning as sampling）的理念，使得模型在保持生成多样性的同时，强制产出符合物理规律且朝向目标的轨迹，从根源上解决了模块分离和不一致的问题。

SceneDiffuser旨在构建一个通用的场景条件生成、优化与规划模型，适用于人体姿态生成、人体动作生成、灵巧抓取生成、三维导航路径规划和机器人臂运动规划等多种任务（见 Figure 1），无需为每个任务设计独立的模块组合。

## 核心方法与创新机理

SceneDiffuser 的核心创新在于将**场景条件生成、物理优化与目标规划统一到一个条件扩散模型的引导采样框架**内，从而解决了此前方法中模块分离导致的不一致性和条件变分自编码器（cVAE）的后验崩塌问题。其关键 changed slots 体现在三个层面：

### 1. 生成模型架构：从 cVAE 到条件扩散模型

基线方法采用 cVAE 作为场景条件生成器，存在严重的后验崩塌（posterior collapse），导致生成多样性不足。SceneDiffuser 将生成器替换为**条件扩散模型**（Conditional Diffusion Model），通过逐步去噪过程建模轨迹分布。该模型使用交叉注意力（cross-attention）机制将三维场景条件灵活注入去噪过程：场景点云经 Point Transformer 或 PointNet 编码后，作为条件特征与轨迹的中间表示进行交叉注意力计算（Figure 2）。扩散模型的多步采样特性天然避免了 cVAE 的崩塌问题，在保持生成多样性的同时提升了物理合理性。

### 2. 物理优化集成方式：从后处理到逐步引导

先前方法通常将物理约束作为后处理优化步骤，或在最终生成结果上施加可微分约束，导致生成与优化过程分离、模块间不一致。SceneDiffuser 将**物理优化目标作为梯度引导集成到去噪采样的每一步**中：

$$ \mathbf{g} = \nabla_{\boldsymbol{\tau}^{t}} \bigl( \varphi_{o}(\boldsymbol{\tau}^{t} | \mathcal{S}) + \varphi_{p}(\boldsymbol{\tau}^{t} | \mathcal{S}, \mathcal{G}) \bigr) \big|_{\boldsymbol{\tau}^{t} = \boldsymbol{\mu}} $$

其中 $\varphi_{o}$ 包含碰撞目标 $\varphi_{o}^{\mathrm{collision}}$（最小化人体网格顶点在场景负 SDF 中的比例）、接触目标 $\varphi_{o}^{\mathrm{contact}}$（最小化接触部位与场景网格间距离）以及轨迹级平滑目标。这些梯度在每次去噪步骤中修正采样方向，使得最终生成的轨迹在物理上更合理。消融实验表明，仅此一项改进即可使人体姿态生成的合理率提升 **25%**（49.35% vs 24.83%，Table 1）。

### 3. 规划方式：从独立规划器到“规划即修复”

传统方法依赖独立的规划器（如行为克隆 BC、确定性 L2 距离规划器），与生成模型相互独立。SceneDiffuser 以**“规划即采样”（planning as sampling）**的理念，将目标导向规划形式化为扩散框架下的运动修复（motion inpainting）。具体而言，目标条件轨迹分布被分解为场景条件生成项与目标到达项的乘积：

$$ p(\boldsymbol{\tau}^{0} | S, \mathcal{G}) \propto p_{\theta}(\boldsymbol{\tau}^{0} | S) \, p_{\phi}(\mathcal{G} | \boldsymbol{\tau}^{0}, S) $$

在采样过程中，规划目标 $\varphi_{p}^{L_{2}}$（所有帧的累积 L2 距离）与物理优化目标共同作为梯度引导，使去噪轨迹逐步趋向目标。在三维导航路径规划中，SceneDiffuser 的规划成功率（73.75%）显著优于 BC 基线（Table 4），验证了统一框架的有效性。

### 瓶颈突破的本质

这三个 changed slots 共同解决了分析中识别的核心瓶颈：**扩散模型的多样性优势**解决了 cVAE 的后验崩塌；**逐步物理引导**消除了生成-优化分离带来的不一致性；**规划即修复**将规划纳入同一采样框架，避免了独立规划器的泛化局限。三者协同使得 SceneDiffuser 成为一个**场景感知、物理合理且目标导向**的统一生成-优化-规划模型。

SceneDiffuser 将场景条件生成、物理优化与目标规划统一在一个迭代引导采样框架中，其核心思路是“规划即采样”（planning as sampling）。整体 pipeline 由四个关键模块串联构成，输入为三维场景点云和可选的目标/起始位姿，输出为满足物理约束且朝向目标的轨迹序列。

**输入与输出流。** 系统接收三维场景点云 $S$ 作为条件，可选地接收目标 $\mathcal{G}$（如导航终点或抓取物体位姿）和起始位姿。输出为一条轨迹 $\tau^0 = \{s_1, s_2, \dots, s_T\}$，其中每个状态 $s_t$ 的具体含义随任务变化：人体姿态生成中为 SMPL-X 身体参数，灵巧抓取中为 ShadowHand 的 33 维位姿表示 $q := (t, R, \theta)$，路径规划中为三维位置序列，机器人臂规划中为关节角度序列。

**模块关系与数据流。** 四个模块按以下顺序协作：

1. **场景编码器（Scene Encoder）**：将三维场景点云编码为条件特征。论文采用 Point Transformer 或 PointNet 作为编码器，预训练后冻结参数。消融实验表明，PointNet 全局特征有利于提高抓取成功率，而 PointNet++ 局部特征有利于提高抓取多样性（Table A1）。

2. **条件扩散模型（Conditional Diffusion Model）**：以场景特征为条件，通过交叉注意力机制生成轨迹。该模块是框架的生成核心，其逆扩散过程定义为：
   $$p ( {\pmb \tau} ^ { t - 1 } | {\pmb \tau} ^ { t } , \mathcal { S } ) = \mathcal { N } ( {\pmb \tau} ^ { t - 1 } ; \mu _ { \theta } ( {\pmb \tau} ^ { t } , t , \mathcal { S } ) , \Sigma _ { \theta } ( {\pmb \tau} ^ { t } , t , \mathcal { S } ) )$$
   训练时采用简化的去噪分数匹配损失：
   $$\mathcal { L } _ { \boldsymbol { \theta } } ( \tau ^ { 0 } \vert S ) = \mathbb { E } _ { t , \epsilon , \tau ^ { 0 } } \left[ \Vert \epsilon - \epsilon _ { \boldsymbol { \theta } } ( \tau ^ { t } , t , S ) \Vert ^ { 2 } \right]$$
   架构消融显示，自注意力噪声预测在灵巧抓取中取得最高成功率 75.94%，优于交叉注意力变体（71.25%）（Table A2）。

![[assets/figures/papers/paper_list_l11_https_arxiv_org_abs_2301_06015/figures/015_Table.jpg]]
*Table: A2. Ablation on different model architecture*

3. **优化引导模块（Optimization Guidance）**：在每次去噪步骤中注入物理约束梯度，引导轨迹满足碰撞避免、合理接触和平滑性要求。具体目标函数包括：
   - 碰撞目标：$\varphi_{o}^{\mathrm{collision}} = -\mathbb{E}\left[|\Phi_{s}^{-}(\mathcal{M}^{t})|\right]$，最小化人体/手部网格顶点在场景负 SDF 中的比例；
   - 接触目标：$\varphi_{o}^{\mathrm{contact}} = -\sum_{v_{c}\in C(\mathcal{M}^{t})}\min_{v_{s}\in S}|v_{c}-v_{s}|$，鼓励接触部位贴近场景表面；
   - 平滑度目标：对轨迹施加时序平滑约束。
   
   该模块的关键创新在于将物理优化集成到采样过程的每一步，而非仅在最终输出上进行后处理。这一设计使人体姿态生成的合理率从 24.83% 提升至 49.35%（+25 个百分点，Table 1）。

4. **规划引导模块（Planning Guidance）**：以目标到达为导向，通过梯度引导去噪过程。目标条件轨迹分布被分解为：
   $$p ( \pmb { \tau } ^ { 0 } | S , \mathcal { G } ) \propto p _ { \theta } ( \pmb { \tau } ^ { 0 } | S ) p _ { \phi } ( \mathcal { G } | \pmb { \tau } ^ { 0 } , S )$$
   规划目标采用所有帧的 L1 距离和（成功率 75.69%），显著优于仅考虑最后一帧的方案（57.06%，Table A5）。路径规划中，固定前 15 帧进行 inpainting 获得最佳性能（73.75% 成功率，Table A4）。

![[assets/figures/papers/paper_list_l11_https_arxiv_org_abs_2301_06015/figures/017_Table.jpg]]
*Table: A4. Ablation on different inpainting horizons and scale coefficients of the planning guidance. Table A5. Ablation on different planning objectives*

**引导采样机制。** 在逆扩散的每一步，模型先通过条件扩散模型预测去噪均值 $\mu$，再计算优化与规划目标的联合梯度：
$$\mathbf { g } = \nabla _ { \pmb { \tau } ^ { t } } \bigl ( \varphi _ { o } ( \pmb { \tau } ^ { t } | \mathcal { S } ) + \varphi _ { p } ( \pmb { \tau } ^ { t } | \mathcal { S } , \mathcal { G } ) \bigr ) | _ { \pmb { \tau } ^ { t } = \pmb { \mu } }$$
该梯度被用于扰动均值，使采样轨迹同时满足物理合理性和目标导向性。缩放系数 $\lambda$ 控制引导强度，消融实验表明 $\lambda=1.0$ 在人体姿态生成中达到最佳合理率 52.5%（Table 5）。

**方法定位与对比。** 相较于先前基于 cVAE 的场景条件生成模型（存在严重的后验崩塌问题），SceneDiffuser 以扩散模型替代 cVAE 作为生成骨干，从根本上解决了生成多样性不足的问题。同时，相较于将物理优化作为后处理步骤或仅施加可微分约束的基线方案，SceneDiffuser 将优化与规划梯度注入采样过程，消除了生成与优化模块间的不一致性。在规划层面，SceneDiffuser 将目标导向规划建模为轨迹修复（inpainting），相比独立的行为克隆（BC）或确定性 L2 规划器，在三维导航和机器人臂规划任务中均取得显著更高的成功率（Table 4）。

SceneDiffuser 的核心架构由四个功能模块构成，围绕条件扩散模型的逐步去噪过程组织，将场景条件生成、物理优化与目标规划统一在同一框架内。

**场景编码器（Scene Encoder）** 负责将三维场景点云压缩为条件特征。论文采用 **Point Transformer** 或 **PointNet** 作为编码器，将场景几何信息映射为固定维度的特征表示，供后续交叉注意力模块使用。

**条件扩散模型（Conditional Diffusion Model with Cross-Attention）** 是生成主干。模型在时间条件扩散模型基础上引入交叉注意力机制，在每一步去噪时计算输入轨迹与场景条件特征之间的关联。其逆过程定义为：

$$p ( { \pmb \tau } ^ { t - 1 } | { \pmb \tau } ^ { t } , \mathcal { S } ) = \mathcal { N } ( { \pmb \tau } ^ { t - 1 } ; \mu _ { \theta } ( { \pmb \tau } ^ { t } , t , \mathcal { S } ) , \Sigma _ { \theta } ( { \pmb \tau } ^ { t } , t , \mathcal { S } ) )$$

其中 $\pmb \tau^t$ 为第 $t$ 步加噪轨迹，$\mathcal{S}$ 为场景条件，$\mu_\theta$ 和 $\Sigma_\theta$ 由噪声预测网络参数化。训练目标采用简化的去噪分数匹配损失：

$$\mathcal { L } _ { \boldsymbol { \theta } } ( \tau ^ { 0 } \vert S ) = \mathbb { E } _ { t , \epsilon , \tau ^ { 0 } } \left[ \Vert \epsilon - \epsilon _ { \boldsymbol { \theta } } ( \tau ^ { t } , t , S ) \Vert ^ { 2 } \right]$$

该损失使模型学会从纯噪声中逐步恢复符合场景条件的轨迹。

**优化引导模块（Optimization Guidance）** 在采样过程中注入物理约束。引导梯度形式为：

$$\mathbf { g } = \nabla _ { \pmb { \tau } ^ { t } } \bigl ( \varphi _ { o } ( \pmb { \tau } ^ { t } | \mathcal { S } ) + \varphi _ { p } ( \pmb { \tau } ^ { t } | \mathcal { S } , \mathcal { G } ) \bigr ) | _ { \pmb { \tau } ^ { t } = \pmb { \mu } }$$

其中 $\varphi_o$ 为物理优化目标集合，包含三项核心约束：

- **碰撞目标**：$\varphi_{o}^{\mathrm{collision}} = -\mathbb{E}\left[|\Phi_{s}^{-}(\mathcal{M}^{t})|\right]$，最小化人体网格顶点在场景负 SDF 中的比例，防止穿透。
- **接触目标**：$\varphi_{o}^{\mathrm{contact}} = -\sum_{v_{c}\in C(\mathcal{M}^{t})}\min_{v_{s}\in S}|v_{c}-v_{s}|$，最小化接触身体部位与场景网格间的距离，鼓励合理接触。
- **平滑度目标**：轨迹层面的时间平滑约束。

**规划引导模块（Planning Guidance）** 实现目标导向的轨迹生成。其核心思想是“规划即修复”（motion inpainting）：将目标条件轨迹分布分解为场景条件生成项与目标到达项的乘积：

$$p ( \pmb { \tau } ^ { 0 } | S , \mathcal { G } ) \propto p _ { \theta } ( \pmb { \tau } ^ { 0 } | S ) p _ { \phi } ( \mathcal { G } | \pmb { \tau } ^ { 0 } , S )$$

规划目标 $\varphi_p^{L_2}$ 采用所有帧的逐步 $L_2$ 距离累积，引导去噪轨迹向目标点收敛。在采样时，固定前若干帧（如 15 帧）作为已知部分，仅对剩余帧进行修复式生成，实现从当前状态到目标的平滑过渡。

四个模块的协同机制为：场景编码器提取条件特征，扩散模型生成候选轨迹，优化引导在每一步去噪时施加物理约束梯度，规划引导同时注入目标到达梯度。这种“逐步引导采样”策略是 SceneDiffuser 区别于 cVAE 后处理优化的关键——物理与目标约束不是施加于最终输出，而是贯穿整个生成过程，从根本上解决了后验崩塌导致的多样性不足问题。

![[assets/figures/papers/paper_list_l11_https_arxiv_org_abs_2301_06015/figures/002_Figure_2.jpg]]
*Figure 2: Model architecture of the SceneDiffuser. We use cross-attention to learn the relation between the input trajectory and scene condition. The optimizer and planner serve as the guidance for physically-plausible and goal-oriented trajectories*

## 实验与关键发现

### 核心结果概览

SceneDiffuser 在四类场景条件三维任务上均取得显著提升，其统一框架在生成质量、物理合理性和目标达成率三个维度上一致超越基线方法。

**人体姿态生成（PROX 数据集）**：如表 1 所示，SceneDiffuser 结合优化引导（w/ opt）达到 49.35% 的物理合理率，相比 cVAE 无场景隐变量版本（w/o LHs）的 12.57% 提升 36.78 个百分点。即使不施加优化引导，SceneDiffuser 本身（w/o opt）的合理率 24.83% 也已显著优于所有 cVAE 变体（最高 18.69%）。优化引导采样在此基础上进一步带来约 25% 的合理率提升（24.83% → 49.35%），验证了在去噪过程中逐步注入物理约束的有效性。

**人体动作生成（PROX 数据集）**：如表 2 所示，给定起始姿态的条件下，SceneDiffuser（w/ start）达到 41.76% 的合理率，而 cVAE（w/ start）仅为 16.24%，提升 25.52 个百分点。值得注意的是，SceneDiffuser 在维持高合理率的同时保持了与 cVAE 相当的生成多样性（平均成对距离指标），解决了 cVAE 常见的后验崩塌导致的多样性丧失问题。

**灵巧抓取生成（MultiDex 数据集）**：如表 3 所示，SceneDiffuser 在无优化引导条件下即达到 71.25% 的成功率，而 cVAE 仅为 14.06%，提升 57.19 个百分点。这一巨大差距源于扩散模型对多模态抓取分布更强的建模能力——灵巧手抓取涉及高维关节空间中的多种可行解，cVAE 的后验崩塌在此任务上尤为致命。

**路径规划与机械臂运动规划**：如表 4 所示，在三维导航路径规划中，SceneDiffuser 达到 73.75% 的成功率，显著优于行为克隆（BC）基线（提升超过 40 个百分点）；在机械臂运动规划中达到 78.59% 的成功率。确定性 L2 距离规划器在复杂障碍物场景中几乎完全失败，而 BC 受限于分布外泛化能力，进一步印证了扩散模型作为轨迹级规划器的优势。

### 消融实验

**优化缩放系数 λ**：表 5 显示，在人体姿态生成任务中，λ = 1.0 达到最佳物理合理率 52.5%。过小的 λ（如 0.1）无法有效施加物理约束，合理率仅略高于无引导版本；过大的 λ（如 5.0）则过度扭曲生成分布，导致合理率反而下降至 44.2%。这表明物理引导与生成先验之间存在最优平衡点。

**场景编码器选择**：附录表 A1 对比了 PointNet 全局特征与 PointNet++ 局部特征。PointNet 全局特征带来更高的抓取成功率，而 PointNet++ 局部特征产生更多样化的抓取姿态。这一差异揭示了场景理解的粒度对生成质量与多样性的不同影响——全局特征提供更强的条件信号，局部特征保留了更多不确定性空间。

**模型架构**：附录表 A2 显示，在灵巧抓取任务中，自注意力噪声预测架构（Self-Attn.）达到 75.94% 的成功率，优于交叉注意力架构（Cross-Attn.）的 71.25%。自注意力可能更有效地捕捉轨迹内部帧间的时序依赖，而交叉注意力在场景条件融合上的优势在此任务中未充分体现。

**规划修复帧数**：附录表 A4 表明，在路径规划中固定前 15 帧进行 inpainting 获得最佳性能（73.75% 成功率）。修复过少帧（如 5 帧）无法提供足够的轨迹上下文，修复过多帧（如 25 帧）则限制了生成自由度，均导致成功率下降。

**规划目标函数**：附录表 A5 对比了不同规划目标。鼓励所有帧的 L1 距离和达到 75.69% 成功率，而仅考虑最后一帧的目标仅为 57.06%。这表明逐帧渐进式引导比仅关注终点更能稳定去噪轨迹的收敛方向。

### 定性分析

**人体姿态生成**（图 3）：cVAE 生成的姿态普遍存在穿透场景网格（如身体陷入沙发）或不自然悬浮的问题；SceneDiffuser 无优化版本已显著减少穿透，但仍偶见接触不自然；施加优化引导后，生成的姿态展现出合理的接触关系（如臀部与座椅贴合、脚部与地面接触），物理合理性明显提升。

**灵巧抓取**（图 5）：cVAE 生成的抓取姿态大量出现手指穿透物体或悬空未接触的情况；SceneDiffuser 生成的抓取姿态更准确地贴合物体表面，五指关节配置更符合抓取力学。

**路径规划**（图 6）：SceneDiffuser 在长程三维导航中生成平滑且避障的轨迹，能够绕过复杂障碍物到达目标点，而 BC 基线常陷入局部死胡同或产生不连贯的路径。

### 失败模式与局限性

尽管整体性能优异，SceneDiffuser 仍存在以下可辨识的失败模式：

1. **超参数敏感性**：优化引导的缩放系数 λ 和扩散步数需针对不同任务仔细调节。表 A3 显示，扩散步数从 100 增至 500 时性能提升趋于饱和，但不同任务的最优步数差异明显，缺乏统一的自动调节机制。

2. **规划修复的非自适应性**：当前 inpainting 需预先指定固定帧数，尚未实现根据场景复杂度自适应确定修复范围。在障碍物密集区域可能需要更长的修复窗口，而该方法无法动态调整。

3. **场景编码器的冻结限制**：PointTransformer 在大规模数据集上预训练后冻结，对新场景类型的泛化能力受限。在分布外场景中，编码器提取的特征可能无法为扩散模型提供充分的条件信息。

4. **计算资源需求**：模型训练需 4 块 A100 GPU，推理时的多步去噪过程（通常 100-500 步）限制了实时部署的可行性。在真实机器人场景中，毫秒级响应的需求与当前推理速度之间存在显著差距。

5. **人类评估的统计效力**：用户研究仅涉及 7 名参与者和 4 个测试场景，样本量较小，可能影响偏好排序的统计显著性。该结论需更大规模用户研究进一步验证。

### 与现有方法的系统性对比

| 方法 | 生成多样性 | 物理合理性 | 目标导向规划 | 统一框架 |
|------|-----------|-----------|-------------|---------|
| cVAE | 低（后验崩塌） | 需后处理 | 独立规划器 | 否 |
| BC | 不适用 | 不适用 | 分布内可行 | 否 |
| 确定性规划器 | 无 | 无 | 仅简单场景 | 否 |
| **SceneDiffuser** | **高** | **原生集成** | **原生集成** | **是** |

SceneDiffuser 的核心优势在于将物理优化与目标规划作为去噪过程的引导梯度，而非后处理步骤。这种"规划即采样"的设计使得生成、优化与规划共享同一扩散先验，从根本上避免了模块间的不一致性。

![[assets/figures/papers/paper_list_l11_https_arxiv_org_abs_2301_06015/figures/003_Table_1.jpg]]
*Table 1: Quantitative results of human pose generation in 3D scenes. We report metrics for physical plausibility and diversity*

![[assets/figures/papers/paper_list_l11_https_arxiv_org_abs_2301_06015/figures/004_Table_2.jpg]]
*Table 2: Quantitative results of human motion generation in 3D scenes. We report model variants with and without the start pose*

![[assets/figures/papers/paper_list_l11_https_arxiv_org_abs_2301_06015/figures/008_Figure_5.jpg]]
*Figure 5: Qualitative results of dexterous grasp generation. Compared to grasps generated by cVAE (first row), SceneDiffuser (second row) generates fewer colliding or floating poses, which helps to achieve a higher success rate*

## 定位与知识库关联

### 从 cVAE 到扩散模型：后验崩塌的解法

SceneDiffuser 的方法论根基在于对**场景条件轨迹生成**中一个顽固瓶颈的回应——条件变分自编码器（cVAE）普遍存在的**后验崩塌**（posterior collapse）。在 cVAE 框架下，解码器倾向于忽略潜在变量，导致生成结果几乎退化为确定性映射，多样性严重不足。这一现象在人体姿态生成、灵巧抓取等需要多模态输出的任务中尤为致命：cVAE 基线在 PROX 人体姿态生成上的合理率仅为 12.57%（Table 1），在 MultiDex 灵巧抓取上的成功率仅 14.06%（Table 3），几乎不具备实用价值。

SceneDiffuser 将生成模型架构从 cVAE 切换为**条件扩散模型**（Conditional Diffusion Model），从根本上改变了生成机制。扩散模型通过逐步去噪的过程生成样本，每一步都显式地依赖噪声预测网络对数据分布的建模，天然避免了潜在变量被“绕过”的问题。这一架构切换带来的收益是决定性的：仅扩散模型本身（不含优化引导），在人体姿态生成上的合理率就从 cVAE 的 12.57% 跃升至 24.83%（Table 1），在灵巧抓取上的成功率从 14.06% 跃升至 71.25%（Table 3）。这组数据说明，扩散模型的引入本身就是解决场景条件生成多样性不足的关键杠杆。

### 规划即采样：统一生成、优化与规划的框架创新

SceneDiffuser 的核心方法论贡献在于将**物理优化**和**目标规划**统一纳入扩散模型的引导采样框架，提出“**规划即采样**”（planning as sampling）的理念。这一设计的因果机制可分解为两个层面：

**第一层：物理优化引导。** 传统方法通常在生成完成后再施加后处理优化，导致生成与优化两个阶段不一致——优化可能将生成结果推向分布外区域。SceneDiffuser 将碰撞（$\varphi_{o}^{\mathrm{collision}}$）、接触（$\varphi_{o}^{\mathrm{contact}}$）、平滑度（$\varphi_{o}^{\mathrm{smoothness}}$）等物理目标函数作为梯度引导，注入**每一次去噪步骤**。这意味着物理约束不是事后修补，而是从噪声到干净轨迹的整个生成过程中持续施加的“向心力”。消融实验直接验证了这一设计的因果效力：在人体姿态生成中，优化引导采样将合理率从 24.83% 进一步提升至 49.35%，净提升达 25 个百分点（Table 1）；缩放系数 $\lambda = 1.0$ 时达到最佳合理率 52.5%（Table 5）。

**第二层：目标规划引导。** SceneDiffuser 将目标导向规划建模为轨迹修复（motion inpainting）问题——给定起始状态和目标约束，在扩散采样过程中通过梯度 $\varphi_{p}^{L_2}$ 引导轨迹逐步趋向目标。这一设计使同一个扩散模型无需重新训练即可承担规划任务，与行为克隆（BC）等独立规划基线形成鲜明对比。在 3D 导航路径规划中，SceneDiffuser 的成功率达 73.75%，远超 BC 基线（Table 4）；在机器人臂运动规划中成功率达 78.59%（Table 4）。

### 与相关工作的定位关系

SceneDiffuser 处于**场景理解、扩散生成模型和机器人规划**三个领域的交汇处。其方法与以下工作形成明确的定位关系：

- **场景条件生成模型（cVAE 系列）：** SceneDiffuser 直接回应了 cVAE 的后验崩塌问题，属于对该范式的替代而非改进。实验中将 cVAE 作为主要基线进行系统对比（w/o LHs、w/ LHs、w/ start 等多个变体），覆盖人体姿态、人体动作、灵巧抓取三个任务，证据链条完整。

- **基于扩散的规划方法（Diffuser 系列）：** SceneDiffuser 继承了将规划视为轨迹生成的扩散模型思路，但将条件从任务目标扩展至**三维场景几何**，通过交叉注意力机制将场景点云编码为条件特征。场景编码器采用 Point Transformer 或 PointNet，冻结预训练权重，使模型能够感知场景结构（如座椅、桌面、障碍物）。

- **物理仿真与接触建模：** SceneDiffuser 的优化目标函数借鉴了人体-场景交互中的物理合理性度量（如负 SDF 穿透检测、接触距离最小化），但将这些度量从评估指标转化为**可微分的采样引导信号**，实现了生成过程中的物理感知。

### 适用边界与局限

SceneDiffuser 的适用边界受以下因素约束：

1. **计算资源门槛高。** 模型训练需要 4 块 A100 GPU，且优化和规划引导的超参数（如 $\lambda$、扩散步数）需针对不同任务仔细调整。这一资源需求限制了其在轻量级场景中的直接部署。

2. **规划依赖固定帧数修复。** 路径规划实验中，inpainting 固定前 15 帧获得最佳性能（73.75% 成功率，Table A4），尚未实现完全自适应的规划帧数选择。这意味着在面对未知长度的规划任务时，性能可能退化。

3. **场景编码器冻结限制适应能力。** 场景编码器 Point Transformer 需在大规模数据集上预训练后冻结，可能限制模型对新场景类型的泛化能力，尤其在训练数据覆盖不足的场景分布外区域。

4. **评估的统计显著性有限。** 人类评估仅涉及 7 名参与者、4 个测试场景；灵巧抓取任务的成功率定义基于训练数据均值的 $k$ 倍标准差范围，这些设计可能影响评估结论的泛化可信度。

### 开放问题

从 SceneDiffuser 的方法设计出发，以下开放问题值得后续工作关注：

- **端到端统一训练。** 当前生成模型、优化引导和规划引导分阶段训练，是否可以将三者统一在端到端学习框架中，使物理感知和目标感知成为模型的内在能力而非外部引导？

- **实时推理可行性。** 扩散模型的多步采样在真实机器人部署中是否能满足实时性需求？是否可以通过蒸馏、步数缩减等技术降低推理延迟？

- **动态场景与多智能体扩展。** SceneDiffuser 目前处理静态三维场景，如何扩展到包含移动障碍物、动态交互对象的场景，以及多智能体协同规划任务，是方法泛化的重要方向。

- **自适应规划帧数。** 当前 inpainting 帧数需人工设定，能否通过学习或启发式策略实现自适应确定修复范围，使规划模块真正无需任务特定的超参数调优？

## 原文 PDF

![[paperPDFs/CVPR_2023/SceneDiffuser:_Diffusion-based_Generation,_Optimization,_and_Planning_in_3D_Scenes.pdf]]
