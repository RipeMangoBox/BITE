---
title: "TrajectoryCrafter: Redirecting Camera Trajectory for Monocular Videos via Diffusion Models"
type: paper
paper_level: A
venue: arXiv
year: 2025
pdf_ref: paperPDFs/arxiv_2025/TrajectoryCrafter_Redirecting_Camera_Trajectory_for_Monocular_Videos_via_Diffusion_Models.pdf
project_link: https://TrajectoryCrafter.github.io
code_link: null
aliases:
- TrajectoryCrafter
tags:
- arxiv_2025
- topic/vision_multimodal_applications
- topic/generative_models_diffusion
- topic/generative_models_diffusion/diffusion_image_video
core_operator: 双流条件机制（点云渲染提供几何约束 + 源视频通过Ref-DiT交叉注意力注入外观细节）是控制几何精度与生成保真度之间平衡的核心调节旋钮。
primary_logic: 将确定性视角变换（动态点云渲染）与随机内容生成（双流视频扩散模型）显式解耦，使得可通过双重重投影策略利用大规模单目视频数据训练，同时实现精确轨迹控制和高质量4D生成。
claims:
- 所提方法在iPhone多视图基准上显著超越所有基线方法，PSNR达14.24 dB（最佳基线Shape-of-motion为11.28 dB）
- Ref-DiT双流条件机制对内容一致性至关重要，移除后PSNR从14.24降至13.46
- 混合训练数据策略（动态单目+静态多视图）对泛化性至关重要，单独使用任一种数据均导致性能下降
- 在in-the-wild视频基准上，所提方法在VBench全部七项指标上均显著优于生成式基线GCD和ViewCrafter
---

# TrajectoryCrafter: Redirecting Camera Trajectory for Monocular Videos via Diffusion Models

> [!tip] 核心洞察
> 将确定性视角变换（动态点云渲染）与随机内容生成（双流视频扩散模型）显式解耦，使得可通过双重重投影策略利用大规模单目视频数据训练，同时实现精确轨迹控制和高质量4D生成。

| 字段 | 内容 |
|------|------|
| 中文题名 | TrajectoryCrafter：基于扩散模型重定向单目视频相机轨迹 |
| 英文题名 | TrajectoryCrafter: Redirecting Camera Trajectory for Monocular Videos via Diffusion Models |
| 会议/期刊 | arXiv 2025 |
| Links | [paper](https://arxiv.org/abs/2503.05638) · [Project](https://TrajectoryCrafter.github.io) |
| Topic | #topic/vision_multimodal_applications #topic/generative_models_diffusion #topic/generative_models_diffusion/diffusion_image_video |
| Method | TrajectoryCrafter |
| Dataset | iPhone数据集（多视图视频基准）, In-the-wild单目视频基准（100真实 + 60 T2V生成视频） |

> [!tip] 效果简介
> - iPhone数据集（多视图视频基准） 上，PSNR / SSIM / LPIPS（均值） 14.24 / 0.417 / 0.519 vs GCD: 10.77 / 0.356 / 0.614; ViewCrafter: 10.75 / 0.339 / 0.605; Shape-of-motion... (PSNR相对最佳基线提升2.96 dB (26.2%))。
> - In-the-wild单目视频基准（100真实 + 60 T2V生成视频） 上，VBench（Subject Consistency / Background Consistency / Temporal Flickering / Mot... 0.9236 / 0.9512 / 0.9437 / 0.9815 / 0.2847 / 0.5920 / 0.6479 vs GCD和ViewCrafter（具体数值见Table 2） (全部七项指标显著优于生成式基线)。

## 概要

**问题瓶颈**：对单目视频进行相机轨迹重定向时，现有方法在精确视角控制与4D时空一致性之间难以兼顾。重建式方法（如基于3DGS的4D重建）在遮挡区域失效；生成式方法（如**GCD**, Van Hoorick et al., ECCV 2024）受限于合成数据与真实视频之间的域差异，且依赖隐式位姿嵌入，难以实现精确的轨迹控制。

**核心思路**：TrajectoryCrafter 将确定性视角变换（动态点云渲染）与随机内容生成（双流视频扩散模型）显式解耦。通过深度估计将源视频提升为动态点云，根据目标相机轨迹渲染新视角作为几何约束；同时通过 Ref-DiT 交叉注意力机制注入源视频的外观细节，在几何精度与生成保真度之间实现可控平衡。

**方法定位**：该方法属于基于扩散模型的生成式新视角合成范式，但区别于纯生成式基线（GCD、ViewCrafter）和纯重建式基线（Shape-of-motion），其核心创新在于双流条件机制——点云渲染提供显式几何引导，源视频通过交叉注意力提供内容细节，使得模型可利用大规模单目视频数据（通过双重重投影策略生成训练对）进行训练。

**主要结果**：
- 在 iPhone 多视图基准上，TrajectoryCrafter 的 PSNR 达到 14.24 dB，显著超越最佳基线 Shape-of-motion（11.28 dB），提升幅度达 26.2%。
- 在 in-the-wild 单目视频基准（100 真实视频 + 60 T2V 生成视频）上，VBench 全部七项指标均显著优于生成式基线 GCD 和 ViewCrafter。
- 消融实验证实：Ref-DiT 双流条件机制（移除后 PSNR 降至 13.46）、混合训练数据策略（单独使用任一种数据均导致性能下降）对最终效果至关重要。

单目视频的相机轨迹重定向（camera trajectory redirection）旨在给定一段普通单目视频，合成出相机沿任意新轨迹运动时对应的新视角视频。这一能力在视觉特效、虚拟现实和交互式媒体中具有广泛的应用前景，但实现起来面临一个核心矛盾：**如何在对相机视角变换进行精确几何控制的同时，保证生成内容的4D时空一致性**。

现有方法大致分为两条路线，但各自存在难以逾越的瓶颈：

**重建式方法**（如 Shape-of-motion）通过从单目视频进行4D重建（通常基于3D Gaussian Splatting）来显式建模场景几何，然后在新视角下渲染。这类方法在可见区域能保持较好的几何精度，但一旦相机轨迹偏离原始视角较大，就会暴露大量遮挡区域——这些区域在原始视频中从未被观测到，重建结果必然出现空洞和严重失真。本质上，重建式方法缺乏对未观测内容的“想象”能力。

**生成式方法**（如 **GCD**，Van Hoorick et al., ECCV 2024；**ViewCrafter**）利用视频扩散模型的强大生成先验来补全新视角下的缺失内容。但现有生成式方法面临两个关键缺陷：其一，GCD 等方法的训练数据主要来自合成多视图视频，与真实单目视频之间存在显著的域差异（domain gap），导致在 in-the-wild 视频上泛化能力不足；其二，这些方法通常依赖隐式的位姿嵌入（implicit pose embedding）来控制视角变换，缺乏显式的几何约束，难以实现对相机轨迹的精确控制。

上述两条路线的困境揭示了一个深层瓶颈：**确定性视角变换与随机内容生成之间的耦合问题**。重建式方法将两者完全绑定于显式几何，牺牲了生成能力；现有生成式方法则将两者混入隐式条件，牺牲了几何控制精度。

TrajectoryCrafter 的核心洞察在于：**将确定性视角变换与随机内容生成显式解耦**。通过动态点云渲染提供精确的几何约束，同时利用双流视频扩散模型的生成能力补全遮挡区域和细化外观细节，使得模型既能严格遵循指定的相机轨迹，又能生成高质量的4D一致内容。这一解耦设计还使得模型可以利用大规模单目视频数据进行训练——通过双重重投影（double-reprojection）策略，无需多视图标注即可从普通单目视频中构造训练对，从而突破了数据规模的限制。

## 核心方法与创新机理

TrajectoryCrafter 的核心创新在于将**确定性视角变换**与**随机内容生成**显式解耦，并以此为基础构建了一个双流条件视频扩散模型。这一设计直击现有方法的瓶颈：重建式方法（如 Shape-of-motion）在遮挡区域失效，而生成式方法（如 GCD）受限于合成数据与真实视频的域差异，且依赖隐式位姿嵌入，难以实现精确轨迹控制。

### 变更槽位一：条件输入的几何化重构

**基线做法**：CogVideoX 使用原始图像作为条件输入，缺乏对相机轨迹的显式几何约束。

**TrajectoryCrafter 的改进**：将条件输入替换为**点云渲染图 $I^r$ 和掩码 $M^r$**，作为显式的视角几何条件。具体而言，首先通过 DepthCrafter 从源视频估计时序一致的深度序列，再经逆透视投影将 RGB-D 帧提升为动态点云 $P_i = \Phi^{-1}([I_i^s, D_i^s], K)$，最后根据用户指定的目标相机轨迹 $T^r$ 进行透视投影渲染 $I_i^r = \Phi(T_i^r \cdot P_i, K)$。这一确定性几何管线将轨迹控制从隐式嵌入转变为显式空间变换，从根本上保证了视角变换的精确性。

### 变更槽位二：源视频信息融合的注意力化

**基线做法**：直觉上可直接将源视频与点云渲染图通道拼接后输入模型，但实验证明这一方式效果次优（Figure 7, w/ Concat Condition）。

**TrajectoryCrafter 的改进**：提出**Reference-conditioned Diffusion Transformer (Ref-DiT) 块**，以交叉注意力机制替代简单拼接。在 Ref-DiT 块中，视角 token 作为查询（query），源视频的参考 token 作为键值（key-value），通过交叉注意力将源视频的外观细节注入视角 token。这一设计使得模型能够自适应地对齐源视频内容与目标视角，而非机械地叠加信息。消融实验表明，移除 Ref-DiT 块导致 PSNR 从 14.24 dB 降至 13.46 dB（Table 3），内容一致性显著下降（Figure 7），验证了交叉注意力机制对 4D 时空一致性的关键作用。

### 变更槽位三：训练数据的双重重投影策略

**基线做法**：CogVideoX 使用通用视频数据训练，缺乏面向轨迹重定向任务的配对数据。

**TrajectoryCrafter 的改进**：提出**双重重投影**策略，从大规模单目视频数据中自动生成训练对。给定目标视频，先将其提升为动态点云并通过随机视角变换渲染新视角 $I'$，再将 $I'$ 反向投影回原始相机位姿得到 $I''$。$I''$ 天然包含遮挡空洞且与目标视频对齐，完美模拟了点云渲染的特征。基于此策略，从 OpenVid-1M 生成 60K 训练对，同时从 DL3DV 和 RealEstate10K 静态多视图数据生成 120K 三元组作为补充。这一混合数据策略使模型既能学习动态场景的运动模式，又能从多视图数据中习得遮挡区域的合理补全能力。

### 变更槽位四：两阶段训练策略

**基线做法**：单阶段端到端训练。

**TrajectoryCrafter 的改进**：采用**两阶段渐进式训练**。第一阶段冻结交叉注意力层，训练 DiT 块和 3D 注意力层（使用全部混合数据，10K 迭代，学习率 $1 \times 10^{-5}$）；第二阶段仅训练交叉注意力和 patch embedding 层（仅使用静态多视图三元组，5K 迭代，学习率 $2 \times 10^{-6}$）。这一策略使模型先在几何对齐上建立稳定基础，再精细调优源视频信息注入机制，避免了动态数据中不完美对齐对交叉注意力训练的干扰。

### 创新本质：控制-生成解耦的调节旋钮

上述四个变更槽位共同构成了一个核心调节机制：**点云渲染提供几何约束（控制精度），Ref-DiT 交叉注意力注入外观细节（生成保真度）**。二者的耦合强度通过两阶段训练策略和混合数据配比进行精细调控。这一“几何-外观”双流解耦范式使得 TrajectoryCrafter 能够同时实现精确的轨迹控制和高质量的 4D 内容生成——在 iPhone 多视图基准上 PSNR 达 14.24 dB，显著超越最佳基线 Shape-of-motion 的 11.28 dB（提升 26.2%）；在 in-the-wild 基准上，VBench 全部七项指标均优于生成式基线 GCD 和 ViewCrafter（Table 2）。

TrajectoryCrafter 的整体流程遵循“确定性视角变换 → 随机内容生成”的显式解耦设计，将单目视频的相机轨迹重定向分解为三个串联阶段：动态点云构建、用户交互式渲染、以及双流条件视频扩散模型生成。

**输入与输出。** 系统接收一段单目源视频 $I^s$（可为真实拍摄或 AI 生成视频），以及用户指定的目标相机轨迹 $T^r$。输出为一段高保真视频，其视角精确遵循目标轨迹，同时保持与源视频的 4D 时空一致性。

**阶段一：动态点云构建。** 首先使用单目深度估计器（**DepthCrafter**）从源视频估计时序一致的深度序列 $D^s$。随后，通过逆透视投影将每一帧的 RGB-D 对提升为三维点云：

$$P_i = \Phi^{-1}([I_i^s, D_i^s], K)$$

其中 $K$ 为相机内参。该操作将源视频从 2D 像素空间提升为动态 3D 点云序列 $P$，为后续视角变换提供几何载体。

**阶段二：交互式点云渲染。** 用户可交互式地指定目标相机轨迹 $T^r$（如“zoom-in 并向右环绕”）。系统根据目标位姿对动态点云进行透视投影，生成新视角的渲染图 $I^r$ 及对应的可见性掩码 $M^r$：

$$I_i^r = \Phi(T_i^r \cdot P_i, K)$$

此步骤提供了**确定性的几何约束**——渲染图 $I^r$ 精确反映了目标视角下的空间结构，但不可避免地存在因遮挡、深度估计误差、点云稀疏性导致的空洞和几何失真。

**阶段三：双流条件视频扩散模型生成。** 渲染图 $I^r$ 和掩码 $M^r$ 作为视角条件，与源视频 $I^s$ 一同馈入双流条件视频扩散模型。该模型基于预训练的 **CogVideoX-Fun-5B** 架构，核心创新在于引入 **Ref-DiT（Reference-conditioned Diffusion Transformer）** 块：视角 token 通过 3D 注意力处理后，经由交叉注意力机制从源视频的参考 token 中查询并注入外观细节。这种双流条件设计使得模型既能利用点云渲染的几何约束保证轨迹精度，又能从源视频中恢复纹理、光照等高频外观信息，生成遮挡区域的合理内容。

**数据与训练策略。** 为训练该模型，作者提出了**双重重投影**策略：从单目视频提升为动态点云后，随机采样视角变换渲染新视图，再将其反投影回原始视角，模拟点云渲染的空洞与几何失真特性。由此从 OpenVid-1M 构建 60K 训练对；同时从 DL3DV 和 RealEstate10K 静态多视图数据构建 120K 三元组。训练采用两阶段策略：第一阶段冻结交叉注意力层，训练 DiT 块和 3D 注意力层（全部数据）；第二阶段仅训练交叉注意力和 patch embedding 层（仅静态多视图三元组），以强化源视频信息的融合能力。

Figure 2 展示了上述完整流程的概览：从源视频出发，经深度估计与点云提升，到用户交互式渲染，最终由双流条件扩散模型生成轨迹精确、内容一致的新视角视频。

![[assets/figures/papers/paper_list_l96_https_arxiv_org_abs_2503_05638/figures/002_Figure_2.jpg]]
*Figure 2: Overview of TrajectoryCrafter. Starting with a source video, whether casually captured or AI-generated, we first lift it into a dynamic point cloud via depth estimation. Users can then interactively render the point cloud with desired camera trajectories. Finally, the point cloud renders and the source video are jointly processed by our dual-stream conditional video diffusion model, yielding a high-fidelity video that precisely aligns with the specified trajectory and remains 4D consistent with the source video*

### 3.1 视频扩散模型基础

TrajectoryCrafter 构建于预训练视频扩散模型 CogVideoX-Fun-5B 之上，继承其 3D VAE 编解码器和 DiT（Diffusion Transformer）块作为基础骨架。扩散模型的训练目标为标准去噪分数匹配损失：

$$\operatorname*{min}_{\theta} \mathbb{E}_{t \sim \mathcal{U}(0,1), \epsilon \sim \mathcal{N}(\mathbf{0}, I)} [\| \epsilon_{\theta}(x_t, t) - \epsilon \|_2^2]$$

其中 $x_t$ 为加噪后的视频潜在表示，$t$ 为扩散时间步，$\epsilon$ 为真实噪声，$\epsilon_{\theta}$ 为模型预测噪声。该损失最小化预测噪声与真实噪声之间的期望 $L_2$ 距离，驱动模型学习视频数据的去噪分布。

### 3.2 动态点云构建与视角渲染

**深度估计。** 给定源视频 $\{I_i^s\}_{i=1}^{N}$，首先通过单目深度估计器 DepthCrafter 估计时序一致的深度序列 $\{D_i^s\}_{i=1}^{N}$。

**点云提升。** 利用相机内参 $K$，通过逆透视投影将每帧 RGB-D 对提升为三维点云：

$$P_i = \Phi^{-1}([I_i^s, D_i^s], K)$$

其中 $\Phi^{-1}$ 表示从像素坐标到三维世界坐标的逆投影映射，$P_i$ 为第 $i$ 帧的动态点云。所有帧的点云集合构成场景的 4D 动态表示。

**新视角渲染。** 给定用户指定的目标相机轨迹 $T^r = \{T_i^r\}_{i=1}^{N}$，通过透视投影生成新视角渲染图：

$$I_i^r = \Phi(T_i^r \cdot P_i, K)$$

其中 $T_i^r \cdot P_i$ 将点云变换至目标视角坐标系，$\Phi$ 执行透视投影。同时生成掩码 $M_i^r$ 标记有效投影像素与因遮挡产生的空洞区域。

### 3.3 双流条件扩散模型

核心创新在于将确定性视角变换与随机内容生成显式解耦，通过双流条件机制将几何约束与外观细节分别注入去噪过程。

**条件输入。** 以点云渲染图 $I^r$ 和掩码 $M^r$ 作为视角条件（view condition），提供目标轨迹的几何约束；以源视频 $I^s$ 作为参考条件（reference condition），提供 4D 一致的外观细节。

**Ref-DiT 块。** 在继承的 DiT 块之间插入 Reference-conditioned Diffusion Transformer（Ref-DiT）块，其内部流程为：
1. **3D 注意力**：对视角 token 和文本 token 执行时空联合注意力，建模视频帧间一致性；
2. **交叉注意力**：以视角 token 为查询（Query），以源视频参考 token 为键值（Key-Value），将源视频中蕴含的外观细节注入视角 token。

该设计的关键在于：点云渲染提供显式的几何引导，但缺乏真实纹理和遮挡区域内容；交叉注意力从源视频中检索匹配的细节信息，补偿渲染图的缺陷，同时保持与目标轨迹的对齐。实验表明，直接通道拼接源视频条件效果不佳（见 Figure 7 中 w/ Concat Condition 变体），验证了交叉注意力机制的必要性。

### 3.4 训练数据与策略

**双重重投影。** 为从大规模单目视频数据生成训练对，提出双重重投影策略：对目标视频 $I^t$，先提升为动态点云并随机变换视角渲染得 $I'$，再将 $I'$ 反投影回原始相机位姿得 $I''$。$I''$ 包含与目标视频对齐的遮挡和几何畸变，模拟真实点云渲染的特征分布。基于此策略从 OpenVid-1M 生成 60K 训练对。

**混合数据。** 同时从 DL3DV 和 RealEstate10K 静态多视图数据集，利用 MASt3R 重建全局点云并估计相机位姿，采样不同视角三元组（源视频、目标视频、点云渲染），生成 120K 训练样本。

**两阶段训练。**
- **第一阶段**（10K 迭代，学习率 $1 \times 10^{-5}$）：冻结交叉注意力层，训练 DiT 块和 3D 注意力层，使用全部混合数据；
- **第二阶段**（5K 迭代，学习率 $2 \times 10^{-6}$）：仅训练交叉注意力和 patch embedding 层，仅使用静态多视图三元组，使交叉注意力学会将源视频细节精确映射到目标视角。

该分阶段策略确保模型先建立稳健的几何先验，再学习精细的外观迁移。

## 实验与关键发现

### 实验设置

TrajectoryCrafter以预训练**CogVideoX-Fun-5B**架构为基础构建双流条件视频扩散模型。训练分两阶段进行：第一阶段在混合数据上训练DiT块和3D注意力层（冻结交叉注意力），共10,000次迭代，学习率1×10⁻⁵；第二阶段仅训练交叉注意力和patch embedding层（仅使用静态多视图三元组），共5,000次迭代，学习率2×10⁻⁶。所有训练在8块GPU上进行，batch size为8，视频帧分辨率为384×672，序列长度49帧。

评估在两个互补的基准上展开：**iPhone多视图数据集**（按Shape-of-motion协议使用5个精调场景，排除Space-out和Wheel）提供有参考指标（PSNR/SSIM/LPIPS）的定量比较；自行构建的**in-the-wild单目视频基准**（100个真实视频 + 60个T2V生成视频）通过VBench七项无参考指标评估生成质量和时空一致性。基线涵盖重建式方法**Shape-of-motion**和生成式方法**GCD**（Van Hoorick et al., ECCV 2024）与**ViewCrafter**。

### 主实验结果

**多视图基准定量比较。** 在iPhone数据集上，TrajectoryCrafter在所有场景和均值指标上均显著超越全部基线（Table 1）。完整模型取得PSNR 14.24 dB、SSIM 0.417、LPIPS 0.519，相较最佳基线Shape-of-motion（PSNR 11.28 dB）提升2.96 dB（相对提升26.2%）。生成式基线GCD和ViewCrafter的PSNR分别为10.77 dB和10.75 dB，表明仅依赖隐式位姿嵌入或点云渲染而缺乏源视频精细信息注入的范式难以同时保证几何精度和内容保真度。

**In-the-wild基准泛化性验证。** 在更大规模、更多样化的in-the-wild基准上，TrajectoryCrafter在VBench全部七项指标上均显著优于生成式基线GCD和ViewCrafter（Table 2）。关键指标包括：Subject Consistency 0.9236、Background Consistency 0.9512、Temporal Flickering 0.9437、Motion Smoothness 0.9815。这一结果验证了双流条件机制在真实场景和AI生成视频上的鲁棒泛化能力——点云渲染提供显式几何约束，Ref-DiT交叉注意力注入源视频外观细节，二者协同确保了跨域的一致性生成。

### 消融实验分析

消融实验在iPhone数据集上进行，系统验证了各核心组件的贡献（Table 3）。

![[assets/figures/papers/paper_list_l96_https_arxiv_org_abs_2503_05638/figures/010_Table_3.jpg]]
*Table 3: Ablation study. We report the PSNR, SSIM, and LPIPS metrics for the full model and its ablated versions on the multiview dataset, iphone [23]. The best results are highlighted in bold*

**Ref-DiT块的关键作用。** 移除Ref-DiT交叉注意力机制后，PSNR从14.24降至13.46 dB（降幅0.78 dB），SSIM从0.417降至0.398，LPIPS从0.519升至0.558。定性结果（Figure 7）显示，无Ref-DiT变体在细节纹理和内容一致性上出现明显退化，而直接通道拼接源视频条件的变体（w/ Concat Condition）效果更差，验证了交叉注意力机制相对于简单拼接的优越性——后者无法有效对齐视角token与参考token之间的空间错位。

**源视频条件的必要性。** 仅使用点云渲染条件而完全移除源视频信息（w/o source video）导致性能崩溃：PSNR骤降至11.17 dB，SSIM 0.316，LPIPS 0.646。这表明点云渲染虽提供几何引导，但其固有的空洞和模糊区域需要源视频的外观细节来填补，双流条件的协同是高质量生成的基础。

**混合训练数据策略的贡献。** 移除动态单目训练数据（w/o dynamic data）导致PSNR降至13.62 dB，运动一致性下降；移除静态多视图数据（w/o multi-view data）导致PSNR降至13.36 dB，遮挡区域和几何失真加剧（Figure 8）。单独使用任一种数据源均无法达到完整模型的性能，验证了双重重投影策略生成的动态单目数据与静态多视图数据在训练中的互补性——前者提供时序运动先验，后者增强多视角几何理解。

### 失败模式与局限性

TrajectoryCrafter的主要失败模式源于深度估计模块的误差传播。当单目深度估计在非刚性运动对象或复杂遮挡场景中产生不准确估计时，动态点云提升过程会引入几何偏差，导致生成的视频出现物理不合理现象。典型案例如Figure 9所示：狗的鼻子在深度估计误差下被错误定位，导致生成视频中鼻子穿透玻璃门。此外，方法受限于动态点云在极端视角下的空洞问题，无法合成超大范围轨迹（如360度环绕视角）。推理时基于5B参数DiT架构的多步去噪过程计算开销较大，难以实时应用。

### 实验公平性说明

评估设计兼顾了公平性与全面性：同时采用有参考指标（PSNR/SSIM/LPIPS）和无参考指标（VBench七项），覆盖重建式和生成式两大类代表性基线。iPhone数据集遵循Shape-of-motion的既定评估协议。需注意部分基线（ViewCrafter、Shape-of-motion）为arXiv预印本，尚未经过同行评审；in-the-wild基准为自行构建，非标准公开基准。

![[assets/figures/papers/paper_list_l96_https_arxiv_org_abs_2503_05638/figures/006_Table_1.jpg]]
*Table 1: Quantitative comparison of novel trajectory video synthesis. We report the PSNR, SSIM, and LPIPS metrics for each scene and the mean values across all scenes on the multi-view dataset, iphone [23]. The best results are highlighted in bold*

![[assets/figures/papers/paper_list_l96_https_arxiv_org_abs_2503_05638/figures/007_Table_2.jpg]]
*Table 2: VBench results on in-the-wild monocular videos. We compiled a large-scale in-the-wild video benchmark with 100 real-world and 60 high-quality T2V-generated videos, and report the VBench scores of novel trajectory videos from GCD [75], ViewCrafter [95], and our method. The best results are highlighted in bold*

![[assets/figures/papers/paper_list_l96_https_arxiv_org_abs_2503_05638/figures/011_Figure_8.jpg]]
*Figure 8: Ablation on the training data. We compare our model trained with mixed data to two alternatives: training without multiview data and training without dynamic data. The yellow box highlights the most prominent differences of occulusions, geometric distortions, and motion consistency*

![[assets/figures/papers/paper_list_l96_https_arxiv_org_abs_2503_05638/figures/008_Figure_6.jpg]]
*Figure 6: Qualitative comparison on in-the-wild monocular videos. We show results of redirecting the camera trajectory as “zoom-in and orbit to the right” from the input videos, produced by our method and the generative baselines, GCD [75] and ViewCrafter [95]*

## 定位与知识库关联

### 1. 任务定位与核心瓶颈

TrajectoryCrafter 解决的是**单目视频的相机轨迹重定向**问题：给定一段任意来源的单目视频（实拍或AI生成），要求生成一段在新相机轨迹下的视频，新视频既要精确遵循指定的视角变换，又要保持与源视频的4D时空一致性（即场景内容、运动、遮挡关系在时间上连贯合理）。

现有方法在此任务上存在根本性瓶颈，可归为两条技术路线：

- **重建式方法**（如 **Shape-of-motion**）：基于3D Gaussian Splatting从单目视频重建4D场景表示，再在新视角下渲染。此类方法的致命缺陷在于遮挡区域——源视频中不可见的部分在重建时必然缺失，导致新视角下出现空洞和严重伪影。此外，单目重建本身的不适定性使得动态场景的几何精度难以保证。

- **生成式方法**（如 **GCD** (Van Hoorick et al., ECCV 2024)、**ViewCrafter**）：利用视频扩散模型的生成能力填补缺失内容。**GCD** 在合成多视图视频上训练，但合成数据与真实视频之间存在显著的域差异（domain gap），且其依赖隐式位姿嵌入（implicit pose embedding），难以实现精确的轨迹控制——模型学到的是“大致方向”而非“精确位姿”。**ViewCrafter** 虽然引入了点云渲染作为条件，但其条件融合方式简单，无法充分保持源视频的内容细节。

**核心瓶颈可凝练为**：现有方法无法在对单目视频进行精确相机轨迹控制的同时保持4D时空一致性。重建方法在遮挡区域失效；生成方法受限于域差异和隐式位姿嵌入，控制精度不足。

### 2. 方法与知识库定位

TrajectoryCrafter 的核心创新在于**将确定性视角变换与随机内容生成显式解耦**，并通过双流条件机制将两者有机融合。这一设计使其在方法谱系中占据独特位置：

**（1）与重建式方法的边界**

TrajectoryCrafter 继承了重建式方法中的**几何先验**——通过深度估计和逆透视投影将源视频提升为动态点云，再利用目标相机轨迹进行确定性渲染。但与 Shape-of-motion 等纯重建方法不同，TrajectoryCrafter 不依赖点云渲染直接作为输出，而是将其作为扩散模型的**几何约束条件**。这使得：
- 遮挡区域不需要从残缺的3D表示中“重建”，而是由扩散模型根据源视频内容“生成”；
- 点云渲染提供了显式的、可精确计算的视角变换约束（而非隐式嵌入），确保了轨迹控制的精度。

**（2）与生成式方法的边界**

TrajectoryCrafter 基于预训练的 **CogVideoX-Fun-5B** 视频扩散模型架构，但与 GCD 和 ViewCrafter 在条件机制上有本质区别：
- **GCD** 使用隐式位姿嵌入，控制精度受限于嵌入空间的表达能力；
- **ViewCrafter** 将点云渲染与源视频简单拼接作为条件，信息融合效率低；
- **TrajectoryCrafter** 提出**双流条件机制**：点云渲染图 $I^r$ 和掩码 $M^r$ 作为显式视角条件（提供几何约束），源视频 $I^s$ 通过 **Ref-DiT 交叉注意力**注入外观细节（提供内容保真度）。这一设计使几何精度与生成保真度之间的平衡成为可控的“调节旋钮”。

**（3）在视频扩散模型谱系中的位置**

从架构演进角度，TrajectoryCrafter 可视为 **CogVideoX 的条件扩展变体**。其继承关系如下：
- 继承 CogVideoX 的 3D VAE（视频潜在空间压缩）和 DiT 块（视觉-文本token联合处理）；
- 新增 **Ref-DiT 块**：在原有 DiT 块之间插入交叉注意力层，以视角 token 为查询（query）、参考 token 为键值（key-value），实现源视频细节的定向注入；
- 新增 **3D 注意力层**：在 Ref-DiT 块内部对文本token和视角token进行时空联合建模。

### 3. 适用边界与局限

**适用场景**：
- 单目视频输入（实拍或AI生成均可），无需多视图采集设备；
- 中等范围的相机轨迹变化（如缩放、小角度环绕、平移），点云渲染在此范围内可提供有效的几何约束；
- 场景以静态背景为主，动态对象运动幅度适中。

**明确局限**（基于论文提供的证据）：

1. **深度估计误差的级联效应**：整个流程以深度估计为起点，DepthCrafter 的深度误差会通过点云提升和渲染传播至生成结果。论文在 Figure 9 中展示了典型失败案例——狗鼻子穿过玻璃门，即深度估计将玻璃门误判为更远平面，导致渲染图中狗鼻子的位置错误，扩散模型在此基础上生成的视频出现物理不合理行为。这是方法链式依赖的固有弱点。

2. **超大范围视角合成的失效**：当目标轨迹涉及360度环绕或极端视角变化时，动态点云在源视角不可见区域存在大面积空洞，点云渲染图的信息量急剧下降，扩散模型缺乏足够的几何约束来生成合理内容。论文明确承认此限制。

3. **推理计算开销**：基于5B参数的 DiT 架构，推理需多步去噪（论文未明确报告步数，但此类模型通常需50步以上），难以满足实时应用需求。

4. **动态对象的4D一致性上限**：第二训练阶段仅使用静态多视图数据（DL3DV、RealEstate10K）训练交叉注意力层，这意味着模型对快速非刚性运动对象（如奔跑的人、摆动的衣物）的4D一致性建模主要依赖第一阶段从单目视频学到的先验，可能不够充分。消融实验（Table 3）显示，移除动态数据后 PSNR 从 14.24 降至 13.62，说明动态数据确实贡献了运动一致性——但静态数据主导的第二阶段可能削弱这一能力。

### 4. 与相关工作的具体关系

| 方法 | 作者/出处 | 角色 | 与 TrajectoryCrafter 的关系 |
|------|----------|------|---------------------------|
| **GCD** | Van Hoorick et al., ECCV 2024 | 生成式基线 | 同为视频扩散模型方案，但 GCD 使用隐式位姿嵌入且仅在合成数据上训练；TrajectoryCrafter 以显式点云渲染替代隐式嵌入，并通过混合数据训练克服域差异 |
| **ViewCrafter** | arXiv 预印本 | 生成式基线 | 同样使用点云渲染，但条件融合方式为简单拼接；TrajectoryCrafter 的 Ref-DiT 交叉注意力机制在 PSNR 上提升 0.78 dB（Table 3），验证了信息融合方式的关键性 |
| **Shape-of-motion** | arXiv 预印本 | 重建式基线 | 代表纯重建路线；TrajectoryCrafter 在 PSNR 上领先 2.96 dB（14.24 vs 11.28），体现了“重建+生成”混合策略在遮挡处理上的优势 |
| **CogVideoX** | 基础架构 | 预训练基座 | TrajectoryCrafter 继承其 3D VAE 和 DiT 块，在其上构建双流条件机制和 Ref-DiT 块 |
| **DepthCrafter** | 深度估计模块 | 上游依赖 | 提供时序一致的深度序列，是整个流程的几何信息源头 |

### 5. 开放问题

1. **360度视角合成的扩展路径**：当前方法受限于点云空洞，可能的突破方向包括：(a) 引入视频修补（inpainting）先验填补点云空洞；(b) 结合多帧信息进行更鲁棒的深度估计；(c) 在扩散模型中显式建模遮挡区域的生成先验。

2. **推理效率优化**：5B参数的DiT多步去噪是实用化的主要障碍。通过蒸馏（如渐进式蒸馏到少步采样器）或一致性模型（consistency models）减少去噪步数，是自然的后续方向。

3. **深度估计与生成的联合优化**：当前深度估计与视频生成是分离的两个阶段，深度误差不可逆地影响后续生成。能否将深度估计也纳入扩散模型的去噪过程，实现端到端的联合优化？

4. **Ref-DiT 机制的泛化能力**：交叉注意力以视角token为查询、参考token为键值，在大视角变化下，查询与键值之间的对应关系可能退化。是否有更鲁棒的信息注入机制（如可变形交叉注意力或显式光流引导）？

5. **动态场景的4D一致性强化**：第二训练阶段的静态数据偏置可能限制对快速运动的建模。是否可以在第二阶段引入更多动态多视图数据（如通过运动结构恢复从动态视频中提取），或设计专门的运动感知损失函数？

## 原文 PDF

![[paperPDFs/arxiv_2025/TrajectoryCrafter_Redirecting_Camera_Trajectory_for_Monocular_Videos_via_Diffusion_Models.pdf]]
