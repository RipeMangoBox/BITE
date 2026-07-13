---
title: "DuoMo: Dual Motion Diffusion for World-Space Human Reconstruction"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/DuoMo_Dual_Motion_Diffusion_for_World_Space_Human_Reconstruction.pdf
project_link: null
code_link: null
aliases:
- DuoMo
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
- topic/generative_models_diffusion
- topic/generative_models_diffusion/diffusion_image_video
core_operator: 引入一个在逐视频坐标系中训练的世界空间运动扩散模型，将升维后的含噪估计细化为全局一致的运动，解耦了估计与细化过程，从而兼顾泛化与一致性。
primary_logic: 通过显式几何升维将相机空间估计转化为世界空间的含噪提议，再利用世界空间扩散模型作为生成式先验进行去噪和细化，避免了对固定规范坐标系的依赖，同时直接生成网格顶点运动。
claims:
- 在 EMDB 和 RICH 数据集上，世界空间误差(W-MPJPE)分别相对次优方法降低 16% 和 30%，且保持低脚滑动。
- 双模型设计（相机空间+世界空间）比单一模型（仅世界空间或仅升维）在精度和运动质量上均有显著提升。
- 在长时遮挡场景下，引导采样显著降低根轨迹误差(RTE)和遮挡段误差(RTE-Occ)。
- EMDB 上 W-MPJPE (mm) = 167.1 (DuoMo w/ height)
---

# DuoMo: Dual Motion Diffusion for World-Space Human Reconstruction

> [!tip] 核心洞察
> 通过显式几何升维将相机空间估计转化为世界空间的含噪提议，再利用世界空间扩散模型作为生成式先验进行去噪和细化，避免了对固定规范坐标系的依赖，同时直接生成网格顶点运动。

| 字段 | 内容 |
|------|------|
| 中文题名 | DuoMo: 用于世界空间人体重建的双重运动扩散模型 |
| 英文题名 | DuoMo: Dual Motion Diffusion for World-Space Human Reconstruction |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2603.03265) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction #topic/generative_models_diffusion #topic/generative_models_diffusion/diffusion_image_video |
| Method | DuoMo |
| Dataset | EMDB, RICH |

> [!tip] 效果简介
> - EMDB 上，W-MPJPE (mm) 167.1 (DuoMo w/ height) vs 202.1 (GENMO) (-35.0 (-17.3%))；WA-MPJPE (mm) 66.0 (DuoMo w/ height) vs 74.3 (GENMO) (-8.3 (-11.2%))；RTE (%) 1.1 (DuoMo w/ height) vs 1.2 (GENMO/TRAM) (-0.1)。
> - RICH 上，W-MPJPE (mm) 80.4 (DuoMo w/ height) vs 118.6 (GENMO) (-38.2 (-32.2%))；WA-MPJPE (mm) 53.5 (DuoMo w/ height) vs 75.3 (GENMO) (-21.8 (-28.9%))；MPJPE (mm) (camera-space) 48.0 (DuoMo w/ height) vs 55.7 (CameraHMR) (-7.7)。

## 概要

从无约束单目视频中恢复世界空间的人体运动，是具身AI、AR/VR和行为理解的核心挑战。现有方法面临一个根本性瓶颈：**端到端直接预测模型缺乏跨场景的泛化能力**，而**先估计相机空间运动再通过后处理提升到世界空间的方法**，虽然泛化性较好，却难以保证全局物理一致性——提升后的运动常出现漂移、脚滑动和长时遮挡下的位移偏差。

DuoMo 通过**将运动学习分解为两个扩散模型**来打破这一权衡。其核心洞察是：利用显式几何升维将相机空间估计转化为世界空间的含噪提议，再引入一个在逐视频坐标系中训练的世界空间扩散模型作为生成式先验，对该提议进行去噪和细化。这一设计解耦了“估计”与“细化”过程，使得模型既能继承相机空间方法的泛化优势，又能通过世界空间扩散先验注入全局运动一致性，同时避免了对固定规范坐标系（如实验室地面平面）的依赖。

在方法定位上，DuoMo 区别于以下几条技术路线：
- **端到端世界空间预测方法**（如 **WHAM**、**GVHMR**）：直接输出世界坐标，但泛化性受限。
- **“先相机后提升”方法**（如 **TRAM**）：缺乏对提升后运动的全局一致性建模。
- **生成式方法**（如 **GENMO**）：使用生成先验但未采用两阶段解耦设计。
- **优化型方法**（如 **SLAHMR**、**GLAMR**）：依赖测试时优化，推理效率较低。

DuoMo 还引入了几项关键设计：直接生成595个稀疏网格顶点的运动序列（而非低维SMPL参数），以保留更丰富的运动细节；通过体高条件输入消解尺度歧义；在训练时施加接触损失以抑制脚滑动；以及在推理时通过重投影引导和位移引导纠正时间漂移与遮挡段偏差。

实验结果表明，DuoMo 在 EMDB 和 RICH 数据集上分别将世界空间误差（W-MPJPE）相对次优方法降低了约 **16%** 和 **30%**，同时保持较低的脚滑动和根轨迹误差。消融实验证实，双模型设计（相机空间+世界空间）相比单一模型在精度和运动质量上均有显著提升，且该方法对相机位姿噪声具有更强的鲁棒性。



从单目视频中恢复世界空间中的三维人体运动是计算机视觉的核心难题，其应用涵盖动作捕捉、人机交互、增强现实等。问题的本质挑战在于：单目视频天然丢失了深度信息，且相机本身可能处于未知的运动之中，因此系统必须同时从二维观测中推断出人体姿态和全局轨迹。

现有方法在这一问题上形成了两条主要技术路线，但它们各自面临根本性瓶颈。**端到端方法**（如 **WHAM**、**GVHMR**）直接从视频预测世界空间运动，虽然能保持全局一致性，但泛化能力受限——它们隐式地记忆了训练数据中的场景尺度与相机运动模式，面对野外视频时容易产生漂移或深度歧义。**两阶段提升方法**（如 **TRAM**、**GENMO**）则先在相机空间估计人体运动，再利用估计的相机位姿将其“提升”到世界空间；这类方法泛化性更好，但提升后的运动缺乏全局物理约束，常表现为脚滑动严重、时间抖动大，且对相机位姿估计误差极为敏感。

这一困境的实质是**泛化性与全局一致性之间的根本权衡**：端到端模型牺牲泛化换取一致，提升方法牺牲一致换取泛化。DuoMo 的核心动机正是打破这一权衡——能否在保持泛化能力的同时，获得全局物理一致的世界空间运动？

作者的关键洞察在于：**显式几何提升可以将相机空间估计转化为世界空间中的“含噪提议”，而世界空间扩散模型可以作为生成式先验对其进行去噪和细化**。这一设计将运动重建解耦为两个阶段：相机空间扩散模型负责从视频中估计局部运动（保留泛化性），世界空间扩散模型负责将提升后的含噪运动细化为全局一致的结果（注入物理合理性）。与依赖固定规范坐标系（如实验室地面平面）的方法不同，DuoMo 以每段视频的起始相机位姿为原点定义逐视频坐标系，使世界空间模型能泛化到任意拍摄环境。

此外，DuoMo 直接生成 595 个稀疏网格顶点的运动序列，而非 SMPL 参数，避免了对参数化身体模型的依赖，使运动表征更灵活。在训练和推理阶段，模型还引入了接触损失、重投影引导和位移引导等机制，进一步强化物理合理性与时间一致性。



## 核心方法与创新机理

DuoMo 的核心创新在于**将人体运动重建解耦为两个生成式扩散阶段**，从根本上改变了运动学习策略：第一阶段由相机空间扩散模型从视频特征生成相机坐标系下的运动，第二阶段通过显式几何升维将其变换到世界空间，再由世界空间扩散模型对该含噪提议进行去噪与细化，最终输出全局一致的世界空间运动。这一设计解决了现有方法在泛化性与全局物理一致性之间的根本权衡——端到端模型缺乏泛化能力，而先相机空间后升维的方法则缺乏全局物理一致性。

### 关键改进点

**1. 两阶段生成式运动学习策略**

传统方法或采用端到端直接预测（如 **WHAM**、**GVHMR**），或将相机空间估计与后优化分离（如 **TRAM** 的提升型方法）。DuoMo 将运动学习分解为相机空间扩散估计与世界空间扩散细化两个生成式阶段：第一阶段 $\mathcal{D}_{\mathrm{cam}}$ 以视频特征为条件生成相机空间运动 $\mathbf{C}$，第二阶段 $\mathcal{D}_{\mathrm{world}}$ 以升维后的含噪世界空间网格为条件生成全局一致的运动 $\mathbf{W}$。消融实验（Table 3）证实，双阶段设计相比仅使用世界空间模型或仅做升维，在精度（WA-MPJPE 66.0 vs 153.5/67.0）和运动质量（Jitter 8.7 vs 9.1/32.6，Foot Skating 3.7 vs 4.8/9.2）上均有显著提升。

**2. 逐视频世界坐标系定义**

区别于依赖固定规范坐标系（如实验室地面平面）的方法，DuoMo 以每段视频的起始相机位姿为原点定义逐视频坐标系。这使得世界空间扩散模型在训练时无需假设全局场景结构，增强了对非受限场景的鲁棒性。

**3. 直接网格顶点运动表征**

传统方法多使用参数化身体模型（如 SMPL）的低维参数作为运动表征。DuoMo 直接生成 595 个稀疏网格顶点的运动序列，避免了参数空间到顶点空间的映射误差。消融实验（Table 5）表明，直接生成稀疏网格（World-Model-Mesh）在精度上优于输出 SMPL 参数（World-Model-SMPL），WA-MPJPE 为 65.7 vs 70.1，且脚滑动更小。

**4. 推理时引导采样机制**

在测试时，DuoMo 在 DDIM 采样过程中引入两类引导损失：重投影引导 $\mathcal{L}_{\mathrm{repro}}$ 约束世界空间运动与原始 2D 观测一致，位移引导 $\mathcal{L}_{\mathrm{disp}}$ 确保长时遮挡段的累计根位移与重现身位置一致。Table 2 显示，引导采样在遮挡场景下显著降低根轨迹误差（RTE）和遮挡段误差（RTE-Occ）。

**5. 体高条件输入消解尺度歧义**

单目重建存在固有的尺度模糊性。DuoMo 通过可选的体高条件输入（米为单位）消解这一歧义。Table 1 表明，使用真实体高条件可在 MPJPE 和 PVE 上带来约 10% 的改善。

**6. 接触损失强化物理合理性**

世界空间训练中引入接触损失 $\mathcal{L}_{\mathrm{contact}}$，在着地帧上对脚部顶点施加 L1 约束以减小脚滑动，从训练阶段即强化物理合理性，而非依赖后处理优化。

### 与代表性基线的根本区别

| 方法类型 | 代表方法 | 运动学习策略 | 世界空间获取方式 | 运动表征 |
|---------|---------|-------------|----------------|---------|
| 相机空间重建 | HMR2.0, ReFit, CameraHMR | 单阶段端到端预测 | 不直接输出世界空间运动 | SMPL 参数 |
| 世界空间直接预测 | WHAM, GVHMR | 单阶段端到端预测 | 直接回归世界空间坐标 | SMPL 参数 |
| 生成式世界空间 | GENMO | 单阶段生成式 | 直接生成世界空间运动 | SMPL 参数 |
| 提升型方法 | TRAM | 先相机空间后优化 | 相机空间估计 + 后处理提升 | SMPL 参数 |
| **DuoMo（本文）** | — | **两阶段生成式：相机空间扩散 + 世界空间扩散** | **显式几何升维 + 扩散去噪细化** | **稀疏网格顶点** |

DuoMo 通过显式几何升维将相机空间估计转化为世界空间的含噪提议，再利用世界空间扩散模型作为生成式先验进行去噪和细化，避免了对固定规范坐标系的依赖，同时兼顾了泛化能力与全局一致性。



DuoMo 将单目视频的世界空间人体运动重建分解为**两个级联的扩散模型**，形成“估计—升维—细化”的三步流水线。该设计的核心动机在于解决现有方法中**泛化能力与全局物理一致性之间的根本权衡**：端到端直接预测世界空间运动的方法泛化性不足，而先估计相机空间运动再后优化的方法则缺乏对全局一致性的显式建模。

### 流水线总览

整体框架如 Figure 2 所示，由以下模块串联构成：

![[assets/figures/papers/paper_list_l963_https_arxiv_org_abs_2603_03265/figures/002_Figure_2.jpg]]
*Figure 2: Method overview. (A) In the first stage, our camera-space model encodes video features and generates camera-space human motion. This motion is lifted to the world coordinates using estimated camera poses, becoming the initial proposal for world-space human motion. Some predictions are missing due to subject out of frame. In the second stage, the world-space model encodes the noisy worldspace motion and generates globally consistent world-space motion. Plots at the bottom visualize the pelvis depth in the world coordinates. (B) Camera-space model architecture. (C) World-space model architecture*

1. **相机空间扩散模型 (D_cam)**：以视频帧序列为输入，通过图像编码器提取视觉特征，结合稠密关键点的射线编码作为条件信号，从噪声中生成相机坐标系下的人体运动序列。该阶段输出的每个时刻状态均定义在对应帧的瞬时相机坐标系中（Eq. 1）。模型支持可选的体高条件输入（以米为单位），以消解单目重建中的尺度歧义。

2. **显式几何升维**：利用估计的相机位姿，将相机空间运动通过刚性变换显式提升至世界空间，形成世界空间运动的**含噪初始提议**（Eq. 3）。该步骤不依赖固定规范坐标系，而是以每段视频的起始相机位姿为原点定义逐视频世界坐标系。

3. **世界空间扩散模型 (D_world)**：以升维后的含噪网格顶点为条件，通过去噪过程生成全局物理一致的世界空间运动。该模型在训练时学习对逐视频坐标系中的运动进行去噪，使其对野外场景具有鲁棒性；同时通过时序掩码策略处理目标出框等不可观测情形。

4. **引导采样**（推理时）：在 DDIM 采样过程中引入重投影引导和位移引导，约束生成的运动与原始 2D 观测一致，并纠正长时遮挡造成的根轨迹漂移。

5. **稀疏网格到 SMPLX 转换**：将生成的 595 个稀疏网格顶点通过迭代 MLP 转换为 SMPLX 参数化表示，以便评估和紧凑存储。

### 关键设计决策

- **双模型解耦**：相机空间模型专注于从视觉信号中提取局部运动信息，世界空间模型则负责将含噪的全局提议细化为物理一致的运动。消融实验表明，双阶段设计在精度（WA-MPJPE 66.0 vs 单世界模型 153.5）和运动质量（脚滑动 3.7 vs 单世界模型 4.8）上均显著优于单一模型。

- **直接生成网格顶点**：与传统方法输出 SMPL 低维参数不同，DuoMo 直接生成稀疏网格顶点的运动序列。消融显示，网格输出在精度（WA-MPJPE 65.7 vs SMPL 输出 70.1）和脚滑动指标上均更优，且避免了参数空间到顶点空间的歧义映射。

- **逐视频坐标系**：以第一帧相机为原点定义世界坐标系，使模型无需依赖固定的实验室地面平面等先验，增强了在任意场景中的适用性。

- **接触损失**：在世界空间训练损失中加入着地帧的脚部顶点 L1 损失，显式惩罚脚滑动，强化物理合理性。

### 补充图表

![[assets/figures/papers/paper_list_l963_https_arxiv_org_abs_2603_03265/figures/013_Figure_8.jpg]]
*Figure 8: Architecture (sparse mesh to SMPLX). This network performs iterative refinement to predict SMPLX parameters from a target sparse mesh*



DuoMo 将世界空间人体运动重建分解为两个生成式阶段，分别由相机空间扩散模型与世界空间扩散模型承担，中间通过显式几何升维衔接。图2给出了完整的管线概览。

### 运动表征

模型直接生成稀疏网格顶点的运动序列，而非依赖 SMPL 参数化模型。设视频共 $T$ 帧，每帧人体状态由根节点位置 $\mathbf{r}_t \in \mathbb{R}^3$ 和 $V=595$ 个顶点的偏移 $\mathbf{P}_t \in \mathbb{R}^{V \times 3}$ 构成，即 $\mathbf{X}_t = \{\mathbf{r}_t, \mathbf{P}_t\}$。

相机空间运动序列定义为每帧处于其瞬时相机坐标系下的状态：

$$\mathbf{C} = (^{1}\mathbf{X}_{1}, ^{2}\mathbf{X}_{2}, \dots, ^{T}\mathbf{X}_{T}) \tag{Eq. 1}$$

世界空间运动序列则以第一帧相机位姿为原点建立固定坐标系：

$$\mathbf{W} = (^{1}\mathbf{X}_{1}, ^{1}\mathbf{X}_{2}, \dots, ^{1}\mathbf{X}_{T}) \tag{Eq. 2}$$

为便于扩散模型学习，世界空间中的运动以速度形式参数化。定义根速度 $\Delta^{1}\mathbf{v}_t = \Delta^{1}\mathbf{r}_t - \Delta^{1}\mathbf{r}_{t-1}$，则世界空间网格可通过累积速度与初始姿态恢复：

$$\Delta^{1}\mathbf{X}_t = \Delta^{1}\mathbf{P}_t + \sum_{i=1}^{t} \Delta^{1}\mathbf{v}_i \tag{Section 3.1}$$

### 阶段一：相机空间扩散模型 $\mathcal{D}_{\text{cam}}$

相机空间模型以视频特征为条件，从噪声生成相机空间运动序列。条件信号由两部分相加构成：

$$\mathbf{f}_t^{\text{kpt}} = \text{MLP}(\text{vec}(\gamma(\mathbf{K}_t^{-1} \cdot \mathbf{L}_t))), \quad \mathbf{f}_t^{\text{img}} = \text{Encoder}(\mathbf{I}_t), \quad \mathbf{f}_t = \mathbf{f}_t^{\text{kpt}} + \mathbf{f}_t^{\text{img}} \tag{Eq. 4}$$

其中 $\mathbf{L}_t$ 为稠密关键点检测结果，$\mathbf{K}_t^{-1}$ 将其反投影为射线方向并通过位置编码 $\gamma(\cdot)$ 后展平送入 MLP；$\mathbf{I}_t$ 为原始视频帧，经图像编码器提取特征。两者相加后作为逐帧条件送入扩散模型：

$$\mathbf{C} = \mathcal{D}_{\text{cam}}(\mathbf{C}_\tau, \tau, \mathbf{f}_{1:T}) \tag{Eq. 5}$$

此外，模型接受可选的体高条件输入（以米为单位），通过消解单目重建中的尺度歧义提升世界空间精度（Table 1 显示高度条件带来约 10% 的 MPJPE/PVE 改善）。

### 显式几何升维

相机空间输出通过估计的相机运动 $\mathbf{g}_t$ 显式变换到世界空间，形成含噪提议：

$$^{1}\hat{\mathbf{X}}_{t} = \mathbf{g}_{t}(\mathbf{X}_{t}) \tag{Eq. 3}$$

这一升维步骤是两阶段解耦的关键：它将相机空间的估计转化为世界空间的初始提议，后续由世界空间扩散模型进行去噪与细化。

### 阶段二：世界空间扩散模型 $\mathcal{D}_{\text{world}}$

世界空间模型以升维后的含噪网格为条件，生成全局一致的世界空间运动。条件编码通过逐帧 MLP 实现：

$$\mathbf{c}_t = \text{MLP}(\text{vec}(^{1}\hat{\mathbf{X}}_t)) \tag{Section 3.3}$$

训练时对 $\mathbf{c}_t$ 随机替换为可学习的掩码令牌，使模型能处理主体出框等不可见帧。扩散过程为：

$$\mathbf{W} = \mathcal{D}_{\text{world}}(\mathbf{W}_\tau, \tau, \mathbf{c}_{1:T}) \tag{Eq. 6}$$

### 引导采样

推理时在 DDIM 采样过程中引入两类引导损失，以纠正时间漂移和长时遮挡偏差。

**重投影引导** 约束世界空间运动反投影后与原始 2D 关键点一致：

$$\mathcal{L}_{\text{repro}} = \sum_{t=1}^{T} \| \mathbf{L}_t - \mathbf{K}_t \cdot \mathbf{g}_t^{-1}(^{1}\mathbf{X}_t) \| \tag{Eq. 7}$$

**位移引导** 确保长时遮挡段的累计根位移与重现身位置一致。设 $(i, j)$ 为遮挡段起止帧，$^{1}\hat{\mathbf{r}}_i$ 和 $^{1}\hat{\mathbf{r}}_j$ 为升维后的根位置：

$$\mathcal{L}_{\text{disp}} = \sum_{(i,j) \in \text{Occ}} \| (^{1}\hat{\mathbf{r}}_j - ^{1}\hat{\mathbf{r}}_i) - \sum_{t=i}^{j} {}^{1}\mathbf{v}_t \| \tag{Eq. 8}$$

### 训练损失

相机空间模型使用简单的 L1 损失组合（顶点、根位置、关节），世界空间模型在此基础上增加速度损失与接触损失以强化物理合理性：

$$\mathcal{L}_{\text{contact}} = \frac{1}{|S|} \sum_{t \in S} \| {}^{1}X_{t,\text{foot}} - {}^{1}X_{t,\text{foot}}^{*} \| \tag{Section 3.6}$$

该损失仅在着地帧集合 $S$ 上对脚部顶点施加约束，有效抑制脚滑动。

### 网格到 SMPLX 转换

为便于评估和紧凑表示，训练一个迭代 MLP 将生成的稀疏网格转换为 SMPLX 参数，避免慢速的优化式转换（Section 3.5, Appendix A.3）。

### 补充图表

![[assets/figures/papers/paper_list_l963_https_arxiv_org_abs_2603_03265/figures/003_Figure_3.jpg]]
*Figure 3: Height conditioning. Our camera-space model can generate predictions based on input body heights. As shown at the bottom row, height impacts distance from camera and thus plays an important role in world-space accuracy*



## 实验与关键发现

### 核心定量结果

DuoMo 在 EMDB 和 RICH 两个世界空间重建基准上均取得显著领先。Table 4 显示，在 EMDB 上，带体高条件的 DuoMo 将世界空间关节误差 **W-MPJPE** 降至 **167.1 mm**，相较此前最优的生成式方法 **GENMO**（202.1 mm）降低 **17.3%**；世界空间对齐后误差 **WA-MPJPE** 为 66.0 mm（GENMO 为 74.3 mm）。在 RICH 数据集上优势更为突出：W-MPJPE 从 GENMO 的 118.6 mm 降至 **80.4 mm**（降幅 32.2%），WA-MPJPE 从 75.3 mm 降至 **53.5 mm**（降幅 28.9%）。根轨迹误差 **RTE** 在 EMDB 上为 1.1%，与 GENMO/TRAM 持平或略优。

![[assets/figures/papers/paper_list_l963_https_arxiv_org_abs_2603_03265/figures/008_Table_4.jpg]]
*Table 4: World-space reconstruction on the EMDB [28] and RICH [24] datasets. We do not use test-time flip augmentation. Our method uses the same estimated camera motion as TRAM [76] and GENMO [38], providing a meaningful comparison*

在相机空间评估（Table 1）中，DuoMo 同样具有竞争力：EMDB 上 MPJPE 为 59.5 mm，RICH 上为 48.0 mm，且**不使用测试时翻转增强**（部分基线方法使用，见 Table 1 脚注）。体高条件带来约 10% 的 MPJPE 和 PVE 改善，验证了尺度歧义消解的有效性（Figure 3 可视化了不同体高输入对深度估计的影响）。

![[assets/figures/papers/paper_list_l963_https_arxiv_org_abs_2603_03265/figures/004_Table_1.jpg]]
*Table 1: Camera-space reconstruction on EMDB [28] and RICH [24], with the number of joints in parenthesis. Our method does not use test-time flip augmentation. All metrics are in mm*

### 鲁棒性分析

Table 2 在 Egobody 数据集上评估了遮挡场景下的重建鲁棒性。所有方法使用真实相机位姿。DuoMo 在可见段和不可见段（人物出框）均表现出色：引导采样使根轨迹误差 **RTE** 和遮挡段误差 **RTE-Occ** 显著降低。Figure 4 可视化了引导采样的校正效果——重投影引导和位移引导分别抑制了时间漂移和长时遮挡后的目标位置偏差。Figure 5 的定性对比进一步表明，GVHMR 在相机抖动时出现轨迹漂移，PromptHMR 对遮挡和深度歧义敏感，而 DuoMo 同时保持了精度和鲁棒性。

![[assets/figures/papers/paper_list_l963_https_arxiv_org_abs_2603_03265/figures/005_Table_2.jpg]]
*Table 2: Robust reconstruction on the Egobody [88], evaluating both visible and invisible segments (e.g. person out of frame). All methods use ground truth camera poses in this evaluation*

![[assets/figures/papers/paper_list_l963_https_arxiv_org_abs_2603_03265/figures/010_Figure_5.jpg]]
*Figure 5: Qualitative comparison on Egobody [88]. All methods use the ground truth camera poses. We observe that results from GVHMR [61] are smooth but drift under shaky camera motion. PromptHMR [77] has better position accuracy but is not robust to occlusion and depth ambiguity. Our results show both accuracy and robustness*

### 消融实验

**双阶段设计的必要性**（Table 3）：对比三种变体——仅世界空间模型（World-model-only）、仅相机空间模型加显式升维（Cam-model+Lifting）、以及完整的 DuoMo。DuoMo 在精度和运动质量上均最优：WA-MPJPE 66.0 mm vs. 153.5 mm（仅世界空间）/ 67.0 mm（仅升维）；运动抖动 **Jitter** 8.7 vs. 9.1/32.6；脚滑动 **Foot Skating** 3.7 vs. 4.8/9.2。仅升维方案虽然 WA-MPJPE 接近 DuoMo，但运动质量严重退化，说明世界空间扩散模型的生成式先验对物理合理性至关重要。

**运动表征的对比**（Table 5）：直接生成 595 个稀疏网格顶点（World-Model-Mesh）在 WA-MPJPE（65.7 mm）上略优于输出 SMPL 参数（World-Model-SMPL, 70.1 mm），且脚滑动更小。这验证了绕过参数化身体模型、直接建模顶点运动的优势。

**相机位姿噪声鲁棒性**（Figure 6）：随着相机运动噪声增大，Cam-model+Lifting 的 W-MPJPE 急剧恶化，脚滑动爆炸；而 DuoMo 的 W-MPJPE 平缓下降，脚滑动保持低位。这表明世界空间扩散模型能有效容忍升维阶段引入的相机位姿误差，解耦了估计与细化对相机精度的依赖。

### 失败模式与局限性

尽管整体性能领先，DuoMo 存在以下已知局限：

1. **场景不一致性**（Figure 11）：模型未显式融入 3D 场景信息，导致细粒度人-场景交互出现偏差（如坐姿时人体与椅子的接触关系不准确）。
2. **困难姿态下的网格形变**（Figure 12）：在极端姿态下，生成的稀疏网格可能产生非真实形变；通过转换为 SMPL 网格（附录 A.3 的迭代 MLP 转换器）可部分改善，但未根本解决。
3. **二值可见性假设**：当前方法通过置信度阈值将关键点可见性二值化，丢弃了不确定性信息，可能影响运动模型在部分遮挡下的条件质量。

![[assets/figures/papers/paper_list_l963_https_arxiv_org_abs_2603_03265/figures/016_Figure_11.jpg]]
*Figure 11: Limitation 1. Because our models do not incorporate 3D scene information, the results exhibit inconsistencies in finegrained details*

![[assets/figures/papers/paper_list_l963_https_arxiv_org_abs_2603_03265/figures/017_Figure_12.jpg]]
*Figure 12: Limitation 2. In challenging poses, the generated sparse meshes sometime exhibit unrealistic deformation. Converting them to SMPL meshes (sec A.3) partially improves the results*

这些失败模式指向未来的改进方向：将 3D 场景约束或物理目标融入引导采样、以连续置信度替代二值可见性、以及探索潜在扩散或令牌化表示以提升网格生成的鲁棒性。

### 补充图表

![[assets/figures/papers/paper_list_l963_https_arxiv_org_abs_2603_03265/figures/006_Table_3.jpg]]
*Table 3: Ablation for DuoMo design on EMDB [28]. DuoMo has higher accuracy and motion quality than using only one model*

![[assets/figures/papers/paper_list_l963_https_arxiv_org_abs_2603_03265/figures/009_Table_5.jpg]]
*Table 5: Ablation for motion representation on EMDB [28]. Directly generating sparse mesh is very competitive in terms of motion reconstruction accuracy*

![[assets/figures/papers/paper_list_l963_https_arxiv_org_abs_2603_03265/figures/011_Figure_6.jpg]]
*Figure 6: Impact of camera error. Comparison of methods under different camera motion noise levels*



## 定位与知识库关联

### 1. 问题定位：世界空间人体运动重建的核心瓶颈

从单目视频中重建世界空间（world-space）的人体运动，是理解人在三维世界中行为的基础任务。该领域长期面临一个根本性权衡：

- **端到端直接预测方法**（如 **WHAM**、**GVHMR**、**TRAM**、**GLAMR**、**TRACE**）试图直接从视频回归世界空间运动，但其泛化能力受限于训练数据的规模和多样性，在开放场景中精度下降明显。
- **先相机空间后升维的方法**（如 **SLAHMR** 等优化型方法，或使用现成相机空间估计器加后处理优化的方案）虽然可以借助成熟的人体姿态估计器获得较好的泛化性，但升维步骤仅依赖相机位姿进行刚性变换，缺乏对全局运动物理一致性的显式建模，容易产生根轨迹漂移、脚滑动和遮挡段的位置跳变。

**DuoMo 的切入点**：将这一权衡解耦为两个可分别优化的生成式阶段——相机空间扩散模型负责从视觉信号中估计局部运动（泛化），世界空间扩散模型负责将升维后的含噪提议细化为全局一致的运动（一致性）。这一设计使得两个模型可以各司其职，避免了单一模型需要同时兼顾泛化与全局物理合理性的困难。

### 2. 与基线方法的关系

#### 2.1 相机空间重建基线

DuoMo 的相机空间扩散模型（$\mathcal{D}_{\mathrm{cam}}$）与以下方法处于同一评估维度（Table 1）：

- **HMR2.0**、**ReFit**、**CameraHMR**、**NLF**、**PromptHMR**：这些方法均在相机空间坐标系中估计人体姿态/形状参数。DuoMo 的相机空间模型在 EMDB 和 RICH 数据集上取得了最优的 PA-MPJPE、MPJPE 和 PVE 指标（如 RICH 上 MPJPE 48.0 mm vs CameraHMR 的 55.7 mm），表明其相机空间估计能力已超越现有专用基线。
- 关键差异在于：DuoMo 的相机空间模型输出的是稀疏网格顶点（595 个顶点）而非 SMPL 参数，且支持体高条件输入（以米为单位），直接消解了单目重建中的尺度歧义（Figure 3）。

#### 2.2 世界空间重建基线

在 Table 4 的世界空间评估中，DuoMo 与以下类别的基线进行了比较：

**直接预测型方法**：
- **WHAM**、**GVHMR**：直接从视频特征回归世界空间运动。这些方法在相机运动平稳时表现平滑，但在相机抖动场景下根轨迹漂移严重（Figure 5 定性比较中 GVHMR 的漂移现象明显）。
- **TRAM**：同时估计相机运动和人体运动。DuoMo 在评估中使用了与 TRAM 相同的估计相机运动，确保了公平比较。

**提升型方法（Lifting-based）**：
- **GENMO**：作为最接近的生成式基线，GENMO 同样使用扩散模型，但其世界空间生成依赖于固定的规范坐标系，泛化受限。DuoMo 在 EMDB 上 W-MPJPE 降低 17.3%（167.1 vs 202.1 mm），在 RICH 上降低 32.2%（80.4 vs 118.6 mm），提升显著。

**优化型方法**：
- **SLAHMR**：通过后处理优化改善世界空间一致性，但依赖良好的初始估计且计算开销大。DuoMo 以纯生成式推理避免了迭代优化，同时通过引导采样（reprojection + displacement guidance）在推理时注入物理约束。

**PromptHMR** 作为同时覆盖相机空间和世界空间的基线，在遮挡和深度歧义场景下鲁棒性不足（Figure 5），而 DuoMo 的双模型设计在遮挡段仍能保持合理的轨迹估计。

### 3. 关键设计决策的消融验证

#### 3.1 双阶段 vs 单阶段（Table 3）

消融实验直接验证了 DuoMo 双阶段设计的必要性：
- **仅世界空间模型（World-model-only）**：精度严重下降（WA-MPJPE 153.5 mm），说明缺乏相机空间先验的世界空间生成难以收敛。
- **仅升维（Cam-model + Lifting）**：精度尚可（WA-MPJPE 67.0 mm），但运动质量恶化（Jitter 32.6，Foot Skating 9.2），表明升维后的含噪提议需要世界空间模型的生成式细化。
- **DuoMo（完整双阶段）**：同时获得最高精度（WA-MPJPE 66.0 mm）和最佳运动质量（Jitter 8.7，Foot Skating 3.7），验证了“估计-细化”解耦的有效性。

#### 3.2 运动表征：稀疏网格 vs SMPL 参数（Table 5）

DuoMo 直接生成 595 个稀疏网格顶点，而非低维 SMPL 参数：
- **World-Model-Mesh**（直接生成网格）：WA-MPJPE 65.7 mm，脚滑动更低。
- **World-Model-SMPL**（生成 SMPL 参数后恢复网格）：WA-MPJPE 70.1 mm。

直接生成网格顶点的优势可能源于：顶点空间的运动模式更直接地对应物理运动，避免了参数空间到顶点空间的非线性映射带来的误差放大。在困难姿态下，生成的稀疏网格可能出现非真实形变，但通过训练好的 MLP 转换器（Section 3.5）可将其映射为 SMPL-X 参数以部分改善（Figure 12）。

#### 3.3 对相机位姿噪声的鲁棒性（Figure 6）

DuoMo 对相机位姿估计误差表现出显著更强的鲁棒性：
- 随着相机运动噪声增大，Cam-model + Lifting 基线的 W-MPJPE 急剧恶化，脚滑动指标爆炸。
- DuoMo 的 W-MPJPE 随噪声增大而平缓下降，脚滑动始终保持较低水平。

这一性质的关键在于：世界空间扩散模型在训练时已见过含噪的升维提议，学会了从有噪声的初始估计中恢复全局一致的运动，因此对相机位姿误差具有天然的容错能力。

### 4. 适用边界与局限

#### 4.1 未融入 3D 场景信息（Figure 11）

DuoMo 的世界空间扩散模型仅建模人体运动本身，未显式编码 3D 场景几何。这导致在细粒度人-场景交互上可能出现不一致——例如坐姿与椅子的接触关系可能不准确。相比之下，场景感知方法可以通过场景约束来修正此类偏差，但 DuoMo 目前的引导采样仅依赖 2D 重投影和位移约束，缺乏对场景几何的感知。

#### 4.2 困难姿态下的网格形变（Figure 12）

在极端或罕见姿态下，直接生成的稀疏网格可能出现非真实的局部形变。虽然转换为 SMPL-X 网格可部分改善（通过参数化模型的先验约束），但这意味着 DuoMo 的网格生成质量在分布外姿态上仍有提升空间。

#### 4.3 关键点可见性的二值化处理

当前方法通过阈值置信度将关键点可见性二值化，可能丢失不确定性信息。当关键点处于部分遮挡或运动模糊状态时，二值化处理可能向运动模型传递错误的可见性信号，影响重建精度。

### 5. 开放问题与未来方向

1. **场景-运动联合建模**：如何将 3D 场景信息（如点云、SDF、平面检测）融入世界空间扩散模型的条件或引导采样过程，以改善人-场景交互的一致性？可能的路径包括：将场景几何编码为额外的条件特征，或在引导采样中增加场景穿透惩罚项。

2. **连续不确定性建模**：将关键点检测置信度作为连续信号（而非二值可见性）输入条件编码器，使模型能够根据观测质量自适应调整对视觉证据的依赖程度。

3. **潜在空间生成**：当前 DuoMo 直接在顶点空间进行扩散生成，维度较高（595 个顶点 × 3 维 × T 帧）。利用潜在扩散模型或 VQ-VAE 风格的令牌化表示可能提高生成效率和对困难姿态的鲁棒性。

4. **多人物交互场景**：DuoMo 目前针对单人重建设计。在多人交互场景中，世界空间运动之间存在物理约束（如接触、避碰），如何扩展双扩散框架以同时生成多个一致的人体运动序列是一个开放挑战。

5. **实时/在线推理**：当前扩散模型的迭代采样过程限制了实时应用。探索蒸馏、一致性模型或单步生成方法，以在保持世界空间一致性的前提下降低推理延迟。



## 原文 PDF

![[paperPDFs/CVPR_2026/DuoMo_Dual_Motion_Diffusion_for_World_Space_Human_Reconstruction.pdf]]
