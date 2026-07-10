---
title: SceneMI Motion In betweening for Modeling Human Scene Interaction
type: paper
paper_level: A
venue: ICCV
year: 2025
pdf_ref: paperPDFs/ICCV_2025/SceneMI_Motion_In_Betweening_for_Modeling_Human_Scene_Interactions.pdf
aliases:
- SMBMHSI
tags:
- ICCV_2025
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
- topic/generative_models_diffusion
- topic/generative_models_diffusion/diffusion_image_video
core_operator: 双尺度场景编码（全局体素 + 局部BPS）结合噪声感知的扩散插值机制（划分去噪时段），通过显式编码场景层次信息并自适应处理关键帧噪声，实现场景约束与运动质量的统一优化。
primary_logic: 将人-场景交互生成重新定义为场景感知的运动插值任务，利用扩散模型的去噪本质，在扩散早期使用带噪声关键帧进行引导，后期联合去噪，从而在噪声环境下同时满足关键帧约束与环境约束。
claims:
- SceneMI在无噪声TRUMANS上取得FID=0.123，远超最佳基线（CondMDI的0.943），且在碰撞帧率（0.113 vs 0.262）等指标上全面领先。
- 场景感知模块显著降低碰撞率：在近距离交互帧上，场景感知使碰撞帧率从0.237降至0.162。
- 噪声感知策略（T*=20）在噪声密集关键帧下将FID从未去噪的0.157提升至0.118，证明分割去噪的必要性。
- 在真实世界GIMO数据上，SceneMI将足滑从0.261降至0.163，抖动从0.573降至0.249，验证了跨域泛化与降噪能力。
---

# SceneMI Motion In betweening for Modeling Human Scene Interaction

> [!tip] 核心洞察
> 将人-场景交互生成重新定义为场景感知的运动插值任务，利用扩散模型的去噪本质，在扩散早期使用带噪声关键帧进行引导，后期联合去噪，从而在噪声环境下同时满足关键帧约束与环境约束。

| 字段 | 内容 |
|------|------|
| 中文题名 | SceneMI：面向人-场景交互建模的运动插值 |
| 英文题名 | SceneMI Motion In betweening for Modeling Human Scene Interaction |
| 会议/期刊 | ICCV 2025 |
| Links | [Project](http://inwoohwang.me/SceneMI) · [Code](https://github.com/) · [paper](https://arxiv.org/abs/2503.16289) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction #topic/generative_models_diffusion #topic/generative_models_diffusion/diffusion_image_video |
| Method | SceneMI |
| Dataset | TRUMANS, GIMO real-world |

> [!tip] 效果简介
> - TRUMANS (noise-free, r=60) 上，FID 0.123 vs 0.943 (CondMDI) (-0.820)。
> - TRUMANS (noisy, r=3, l=1) 上，FID 0.118 vs 3.136 (CondMDI) (-3.018)。
> - GIMO real-world (r=15) 上，Foot Skating 0.163 vs 0.261 (Original GIMO) (-0.098)。

## 概述

**SceneMI** 是一项面向人-场景交互（Human-Scene Interaction, HSI）建模的运动插值方法。其核心动机源于现有HSI生成方法的两个关键瓶颈：一是传统运动插值技术忽略3D场景约束，无法保证生成的运动与环境几何一致；二是现有方法假设关键帧精确无噪声，难以应对真实世界中由采集设备或姿态估计引入的噪声输入。SceneMI 将人-场景交互生成重新定义为**场景感知的运动插值任务**，利用扩散模型的去噪本质，在扩散早期使用带噪声关键帧进行引导，后期联合去噪，从而在噪声环境下同时满足关键帧约束与环境约束。

在方法设计上，SceneMI 提出双尺度场景编码与噪声感知的扩散插值机制作为核心因果调控变量：全局场景通过占用体素网格经ViT编码为512维特征，局部场景则以关键帧为中心提取BPS（Basis Point Set）特征，二者显式编码场景的层次信息；噪声感知采样策略将去噪过程划分为 $[T, T^*+1]$ 与 $[T^*, 1]$ 两个阶段，前期以噪声关键帧引导、后期联合去噪，自适应处理关键帧噪声。这一设计实现了场景约束与运动质量的统一优化。

实验验证了SceneMI的显著优势。在无噪声TRUMANS基准上，SceneMI取得FID=0.123，远超最佳基线CondMDI的0.943，碰撞帧率从0.262降至0.113。在噪声密集关键帧场景下（r=3, l=1），噪声感知策略（$T^*=20$）将FID从未去噪的0.157提升至0.118，证明了分割去噪的必要性。在真实世界GIMO数据上，SceneMI将足滑从0.261降至0.163，抖动从0.573降至0.249，验证了跨域泛化与降噪能力。消融实验进一步表明，场景感知模块在近距离交互帧上将碰撞率从0.237降至0.162，身体体型编码对运动对齐有显著贡献。

SceneMI 仍存在若干局限：在罕见交互模式（如狭缝穿行）上表现不佳；对真实场景几何重建质量敏感；目前仅支持固定长度运动插值，长序列需自回归拼接；尚未支持部分姿态关键帧输入。这些方向为后续研究提供了明确的改进空间。

## 背景与动机

### 人-场景交互建模的核心挑战

在三维场景中生成自然、物理合理的人体运动，是人-场景交互（Human-Scene Interaction, HSI）建模的核心目标。该任务在虚拟现实、具身智能、电影制作等领域具有广泛的应用前景。然而，现有方法面临一个根本性的瓶颈：**可控性与灵活性的双重缺失**。传统的HSI生成方法通常以稀疏控制信号（如目标位置、动作类别）为条件直接生成完整运动序列，缺乏对中间过渡姿态的细粒度控制能力。这使得用户难以精确指定运动的关键时刻，也限制了方法在实际交互场景中的应用灵活性。

运动插值（Motion In-betweening）作为一种经典的运动生成范式，天然具备通过关键帧控制运动轨迹的能力。然而，现有的运动插值方法几乎完全忽略了三维场景的约束——它们假设人体在空旷空间中运动，无法感知座椅、楼梯、墙壁等环境物体的存在。这一缺陷导致生成的过渡运动频繁穿透场景物体，产生物理上不可行的交互结果。

### 噪声关键帧：从理想假设到现实挑战

现有运动插值方法的另一个隐含假设是**关键帧的精确性**。在真实应用场景中，关键帧往往来自单目视频重建、稀疏传感器捕捉或用户手动标注，不可避免地包含噪声。例如，从单目视频中估计的人体姿态可能存在关节抖动、足部滑步等伪影；来自深度传感器的数据可能因遮挡而产生位置偏移。当这些带噪声的关键帧被直接用于插值时，传统方法会将噪声传播到整个生成序列中，导致运动质量急剧下降。

这一问题在密集关键帧场景下尤为突出——直觉上，更多的关键帧应当提供更强的约束，但实际上，密集的噪声关键帧反而使模型更难恢复出平滑、合理的运动轨迹。现有基线方法（如CondMDI）在噪声密集关键帧（间隔r=3，噪声级别l=1）下的FID高达3.136，几乎失去了实用价值。这暴露了一个关键的技术缺口：**如何在噪声环境下同时满足关键帧约束与环境约束**。

### 场景感知的层次性需求

人与场景的交互发生在多个空间尺度上。全局场景结构（如房间布局、大型家具位置）决定了运动的宏观轨迹和导航路径；局部场景细节（如座椅表面、桌面边缘）则直接影响精细的接触与避碰行为。现有场景感知方法通常仅采用单一的全局编码（如整体点云特征），难以捕获这种层次化的空间关系。例如，当人体靠近椅子时，模型需要同时理解“椅子在房间中的位置”（全局）和“椅子表面的精确几何”（局部），才能生成合理的坐姿过渡。单一尺度的场景表征无法同时满足这两种需求。

### SceneMI的动机与定位

针对上述三个核心缺口——**场景约束的缺失、噪声关键帧的挑战、场景感知的层次性不足**——SceneMI将人-场景交互生成重新定义为**场景感知的运动插值任务**。其核心动机是利用扩散模型的去噪本质，在生成过程中同时处理两种噪声：关键帧的观测噪声和运动序列的扩散噪声。通过在扩散早期使用带噪声关键帧进行引导、后期联合去噪，SceneMI实现了噪声环境下的鲁棒插值。同时，通过双尺度场景编码（全局体素+局部BPS），模型能够捕获从宏观导航到微观接触的完整空间约束，从而生成物理合理且场景一致的人体运动。

## 核心创新

SceneMI的核心创新在于将人-场景交互（HSI）生成重新定义为**场景感知的运动插值任务**，并通过三个关键设计解决了现有方法的瓶颈。传统运动插值方法（如CondMDI、OmniControl）假设关键帧精确且忽略3D场景约束，而场景感知方法（如SceneDiffuser）缺乏对噪声关键帧的鲁棒性。SceneMI的因果调控机制体现在以下三个维度的创新上。

### 1. 双尺度场景编码：全局体素与局部BPS的层次化表征

现有场景感知方法通常仅使用全局点云或体素编码（如SceneDiffuser的全局特征），难以捕获人体与场景的细粒度交互约束。SceneMI引入了**全局-局部双尺度场景编码**（Section 3.1, Figure 2）：

- **全局编码器**：将整个场景体素化为分辨率为0.1m的占用网格，通过Vision Transformer（ViT）编码为512维全局特征 $\mathbf{c}_g$，提供整体空间上下文。
- **局部编码器**：以每个关键帧的SMPL网格为中心，通过最远点采样在T-pose网格表面选取64个锚点，构建Basis Point Set（BPS）特征 $\mathbf{c}_l^n$，捕获关键帧周围的精细几何约束。

消融实验（Table 1）表明，移除场景感知（无 $\mathbf{c}_g$ 和 $\mathbf{c}_l$）导致碰撞帧率从0.113升至0.131；在近距离交互帧上（Table 2），场景感知使碰撞率从0.237降至0.162。这一设计使得模型能够同时感知全局空间布局和局部交互区域，是实现物理合理人-场景交互的基础。

### 2. 噪声感知的扩散插值机制：划分去噪时段的自适应关键帧引导

这是SceneMI最关键的创新点。传统扩散插值方法在推理时将干净关键帧直接替换到带噪序列中（即 $\mathbf{x}_t' = \mathbf{m} \odot \mathbf{x}_0 + (1-\mathbf{m}) \odot \mathbf{x}_t$），但当关键帧本身含有噪声时，该方法会引入严重误差。SceneMI提出了**划分去噪时段**的策略（Section 3.2.1）：

- **训练阶段**：将总去噪步 $T=1000$ 划分为两个区间 $[T, T^*+1]$ 和 $[T^*, 1]$。在前一区间，将带噪声关键帧 $\mathbf{x}_0^{\text{noisy}}$ 与当前带噪序列混合，训练模型从噪声关键帧中提取有效信息；在后一区间，仅使用完全噪声序列，迫使模型学习联合去噪。
- **推理阶段**：采用相同的分段策略，在扩散早期（$t \in [T, T^*+1]$）使用噪声关键帧进行引导，后期（$t \in [T^*, 1]$）进行联合去噪。经实验验证，最优分界点为 $T^*=20$（Table 3）。

该设计的核心洞察在于：扩散模型的去噪过程本身具有从噪声中恢复信号的能力，因此在早期阶段使用带噪声关键帧进行条件引导是可行的；而后期联合去噪则确保最终生成的整段运动满足时序一致性。Table 3的消融实验证实，关闭噪声感知（$T^*=0$，即全程使用噪声关键帧）使噪声密集关键帧下的FID从0.118退化至0.157；在真实世界GIMO数据上（Table 4），噪声感知使足滑从0.261降至0.163，抖动从0.573降至0.249。

### 3. 人体体型编码：关节-关节距离先验

现有方法通常忽略人体体型差异对运动生成的影响。SceneMI引入了基于**7维关节-关节距离**的体型编码 $\mathbf{b}$（Section 3, Table 8），包括胸部与臀部厚度等关键尺寸。该编码作为扩散模型的条件输入，使生成的运动能够适配不同体型。消融实验（Table 8）显示，去除体型编码使MJPE All从0.023m升至0.038m，验证了体型先验对运动对齐的贡献。

### 创新总结

三个创新点形成了从场景感知到噪声鲁棒再到体型适配的完整技术链路：双尺度场景编码提供环境约束，噪声感知机制赋予模型对真实世界噪声输入的鲁棒性，体型编码确保运动与个体特征的匹配。这一设计使SceneMI在TRUMANS无噪声基准上取得FID=0.123（CondMDI为0.943），在噪声密集场景下FID=0.118（CondMDI为3.136），并在GIMO真实数据上显著降低足滑和抖动，验证了各创新模块的有效性与互补性。

## 整体框架

SceneMI 将人-场景交互（HSI）建模重新定义为**场景感知的运动插值任务**，其核心目标是：给定三维场景 $G$ 和一组稀疏的关键姿态 $\mathbf{s}$（由二值掩码 $\mathbf{m}$ 标记），合成完整的运动序列 $\mathbf{x}$，使其同时满足关键帧约束与场景环境约束。

### 输入表示

模型的输入由三部分构成：

- **人体运动**：每个姿态特征向量为 201 维，包含全局关节位置 $\mathbf{J}$、6D 根节点朝向 $\boldsymbol{\phi}$ 和局部 SMPL 姿态参数 $\boldsymbol{\psi}$。运动序列固定为 $N=121$ 帧。
- **人体体型**：通过 7 维关节-关节距离特征编码，显式包含胸部与臀部厚度信息，作为体型先验 $\mathbf{b}$ 输入。
- **三维场景**：采用双尺度表示——全局粗粒度占用体素网格（分辨率 $d_x \times d_y \times d_z$，每体素 0.1m）和基于关键帧姿态的局部 Basis Point Set（BPS）特征。

### Pipeline 模块与数据流

整体架构（Figure 2）由以下模块串联构成：

![[assets/figures/papers/paper_list_l1772_SceneMI_Motion_In_betweening_for_Modeling_Human_Scene_Interaction/figures/002_Figure_2.jpg]]
*Figure 2: Overview of SceneMI. Given the input 3D scene, we extract global voxelized features*

1. **全局场景编码器（ViT）**：将体素化全局场景编码为 512 维特征 $\mathbf{c}_g$，捕获整体空间上下文。训练时以 10% 概率随机掩码 $\mathbf{c}_g$，为推理时的分类器无关指引（classifier-free guidance）提供条件。
2. **局部场景编码器（BPS）**：在 T-pose SMPL 网格表面通过最远点采样确定 64 个锚点，对每个关键帧计算 BPS 特征 $\mathbf{c}_l^n$，编码关键姿态周围的局部场景几何。
3. **关键帧 Imputation 模块**：在扩散去噪过程中，将关键帧特征按时间位置替换到带噪样本 $\mathbf{x}_t$ 中，形成混合序列 $\tilde{\mathbf{x}}_t$。这是实现关键帧约束的**核心机制**。
4. **运动特征融合**：将 $\tilde{\mathbf{x}}_t$、局部场景特征 $\mathbf{c}_l$ 和关键帧掩码 $\mathbf{m}$ 沿通道拼接，得到运动相关特征；扩散步 $t$ 的嵌入以加法方式注入所有输入特征。
5. **U-Net 扩散去噪器**：基于 1D 卷积与 AdaGN 的 U-Net 结构，以条件特征 $\tau = \{\mathbf{c}_g, \mathbf{c}_l, \mathbf{b}, \mathbf{m}\}$ 为输入，预测干净运动 $\mathbf{x}_0$。
6. **噪声感知采样调度器**：将总去噪步 $T=1000$ 划分为两个区间——$[T, T^*+1]$ 和 $[T^*, 1]$（$T^*=20$）。在早期区间使用带噪声关键帧进行 imputation 引导，后期区间则联合去噪，不再强制替换关键帧位置。这一策略是应对真实世界关键帧噪声的**关键设计**。

### 训练与推理流程

**训练阶段**，模型以预测干净运动 $\mathbf{x}_0$ 为目标，损失函数为：

$$\mathcal{L} = \mathcal{L}_{\mathrm{simple}} + \lambda_{\mathrm{joints}} \mathcal{L}_{\mathrm{joints}} + \lambda_{\mathrm{vel}} \mathcal{L}_{\mathrm{vel}}$$

其中 $\mathcal{L}_{\mathrm{simple}}$ 为标准扩散 MSE 损失，$\mathcal{L}_{\mathrm{joints}}$ 和 $\mathcal{L}_{\mathrm{vel}}$ 分别约束前向运动学（FK）后的关节位置与速度，权重 $\lambda_{\mathrm{joints}}=2.0$，$\lambda_{\mathrm{vel}}=10.0$。

**推理阶段**，采用分类器无关指引采样，以指引权重 $w=2.5$ 结合条件与无条件预测：

$$\hat{\mathbf{x}}_0 = w \cdot \mathcal{D}_{\theta}(\tilde{\mathbf{x}}_t, t, \mathbf{b}, \mathbf{c}_g) + (1 - w) \cdot \mathcal{D}_{\theta}(\tilde{\mathbf{x}}_t, t, \mathbf{b}, \emptyset)$$

SceneMI 直接预测 SMPL 参数，避免了基线方法所需的额外优化拟合后处理，推理速度显著优于对比方法（39.6s vs CondMDI 的 162.4s，Table 7）。

### 关键设计决策的因果链路

双尺度场景编码（全局体素 + 局部 BPS）与噪声感知扩散插值机制构成 SceneMI 的**两个因果旋钮**：前者通过显式编码场景层次信息，使模型在近距离交互场景下将碰撞帧率从 0.237 降至 0.162（Table 2）；后者通过划分去噪时段自适应处理关键帧噪声，在噪声密集关键帧下将 FID 从未去噪的 0.157 提升至 0.118（Table 3）。两者的协同作用使得模型在无噪声 TRUMANS 上取得 FID=0.123，远超最佳基线 CondMDI 的 0.943（Table 1）。

### 补充图表

![[assets/figures/papers/paper_list_l1772_SceneMI_Motion_In_betweening_for_Modeling_Human_Scene_Interaction/figures/015_Figure_7.jpg]]
*Figure 7: The final results from the Video2Animation pipeline demonstrate the reconstruction of 3D human-scene animation from monocular video inputs. By incorporating SceneMI with the obtained scene information and optimized keyframes, we reconstruct natural and physically plausible motions. For additional results, please refer to the supplementary video*

## 核心模块与公式推导

### 3.1 问题形式化

给定3D场景 $G$、稀疏关键姿态集 $\mathbf{s}$ 及其指示掩码 $\mathbf{m}$（关键帧总数 $k = \sum_n m_n \ll N$），SceneMI的目标是合成完整的运动序列 $\mathbf{x} \in \mathbb{R}^{N \times 201}$，使其同时满足关键帧约束和场景环境约束。每个姿态特征向量由全局关节位置 $\mathbf{J}$、6D根朝向 $\phi$ 和局部SMPL姿态参数 $\psi$ 拼接而成，共201维。

### 3.2 双尺度场景编码模块

场景编码是SceneMI实现场景感知运动生成的核心机制，采用全局与局部双分支结构：

- **全局场景编码器（ViT）**：将整个3D场景离散化为粗糙的占用体素网格 $\{0,1\}^{d_x \times d_y \times d_z}$（体素分辨率0.1m），通过Vision Transformer编码为512维全局特征 $\mathbf{c}_g$，捕获大尺度空间布局与障碍物分布。
- **局部场景编码器（BPS）**：在T-pose SMPL网格表面通过最远点采样选取64个锚点，以每个关键帧位置为中心计算Basis Point Set特征 $\mathbf{c}_l^n$，编码人体周围精细的几何约束（如座椅高度、桌面边缘）。

训练时以10%概率随机掩码 $\mathbf{c}_g$，为推理阶段的分类器无关指引（Classifier-Free Guidance）提供条件/无条件采样通道。

### 3.3 扩散去噪核心

SceneMI基于条件扩散模型，训练目标是预测干净运动 $\mathbf{x}_0$。简单扩散损失定义为：

$$\mathcal{L}_{\mathrm{simple}} = \mathbb{E}_{\mathbf{x}_0 \sim p(\mathbf{x}_0 \mid \tau), t \sim [1, T]} \left[ \left\| \mathbf{x}_0 - \mathcal{D}_{\theta}(\mathbf{x}_t, t, \tau) \right\|_2^2 \right]$$

其中 $\tau$ 包含场景特征 $\mathbf{c}_g, \mathbf{c}_l$、体型编码 $\mathbf{b}$ 和关键帧掩码 $\mathbf{m}$，$\mathcal{D}_{\theta}$ 为1D卷积U-Net去噪器（含AdaGN条件注入）。

为强化运动物理合理性，引入辅助损失：

$$\mathcal{L} = \mathcal{L}_{\mathrm{simple}} + \lambda_{\mathrm{joints}} \mathcal{L}_{\mathrm{joints}} + \lambda_{\mathrm{vel}} \mathcal{L}_{\mathrm{vel}}$$

- **关节位置损失** $\mathcal{L}_{\mathrm{joints}} = \| \mathrm{FK}(\mathbf{x}_0) - \mathrm{FK}(\mathcal{D}_{\theta}(\mathbf{x}_t, t, \tau)) \|^2$，通过前向运动学（FK）将姿态参数映射为3D关节位置后计算L2距离。
- **速度损失** $\mathcal{L}_{\mathrm{vel}} = \| \mathrm{diff}(\mathrm{FK}(\mathbf{x}_0)) - \mathrm{diff}(\mathrm{FK}(\mathcal{D}_{\theta}(\mathbf{x}_t, t, \tau))) \|^2$，约束关节时序差分，抑制抖动。

权重设置为 $\lambda_{\mathrm{joints}}=2.0$，$\lambda_{\mathrm{vel}}=10.0$。

### 3.4 噪声感知的关键帧注入机制

这是SceneMI区别于传统运动插值方法的关键创新。传统方法假设关键帧精确，直接使用干净关键帧进行imputation：

$$\mathbf{x}_t' = \mathbf{m} \odot \mathbf{x}_0 + (1 - \mathbf{m}) \odot \mathbf{x}_t$$

即在带噪序列 $\mathbf{x}_t$ 的关键帧位置替换为干净值。然而，当关键帧本身含噪声时，此策略会引入误差累积。

SceneMI提出**划分去噪区间**策略。训练时，对关键帧施加噪声模拟真实场景，并按去噪步 $t$ 分段处理：

$$\mathbf{x}_t' = \begin{cases} \mathbf{m} \odot \mathbf{x}_0^{\mathrm{noisy}} + (1 - \mathbf{m}) \odot \mathbf{x}_t, & t \in [T, T^* + 1] \\ \mathbf{x}_t, & t \in [T^*, 1] \end{cases}$$

- **前期 $[T, T^*+1]$**：使用带噪声的关键帧 $\mathbf{x}_0^{\mathrm{noisy}}$ 进行imputation，让模型学会从噪声关键帧中提取有效引导信号。
- **后期 $[T^*, 1]$**：完全依赖模型自身去噪能力，不注入关键帧信息，实现联合去噪。

推理时采用相同策略，将噪声关键帧 $\mathbf{s}^{\mathrm{noisy}}$ 替换训练公式中的 $\mathbf{x}_0^{\mathrm{noisy}}$。经消融实验验证，最优切换点 $T^*=20$（总步数 $T=1000$），在噪声密集关键帧下将FID从0.157（$T^*=0$，即全程imputation）降至0.118。

### 3.5 分类器无关指引采样

推理阶段采用分类器无关指引（CFG），以指引权重 $w=2.5$ 融合条件与无条件预测：

$$\hat{\mathbf{x}}_0 = w \cdot \mathcal{D}_{\theta}(\tilde{\mathbf{x}}_t, t, \mathbf{b}, \mathbf{c}_g) + (1 - w) \cdot \mathcal{D}_{\theta}(\tilde{\mathbf{x}}_t, t, \mathbf{b}, \emptyset)$$

其中 $\tilde{\mathbf{x}}_t$ 为经imputation后的运动特征（拼接了 $\mathbf{x}_t'$、局部场景特征 $\mathbf{c}_l'$ 和掩码 $\mathbf{m}$），$\emptyset$ 表示全局场景特征被掩码。此机制在保持场景约束的同时提升生成运动的质量与多样性。

### 3.6 体型编码

SceneMI引入7维关节-关节距离特征作为体型先验 $\mathbf{b}$，包含胸部厚度与臀部厚度等关键身体比例信息。消融实验表明，去除体型编码使MJPE All从0.023 m退化至0.038 m，验证了体型先验对运动对齐的重要性。

## 实验与分析

### 核心实验设计与基线对比

实验评估围绕场景感知运动插值任务展开，核心问题是在3D场景约束和稀疏关键帧条件下生成物理合理的过渡运动。评估基准为TRUMANS数据集（含5种人体体型），关键帧间隔r=60帧。基线方法涵盖场景无关的扩散运动生成模型（**MDM**、**StableMoFusion**）、场景感知扩散模型（**SceneDiffuser**，结合强化学习）、基于CVAE的场景感知方法（**Wang et al.**）、以及扩散运动插值方法（**OmniControl**、**CondMDI**）。为确保公平，所有基线均重新训练以适应场景运动插值任务：对场景无关基线替换文本编码器为全局场景ViT编码器，推理时统一采用imputation采样策略。

在无噪声关键帧条件下，SceneMI取得FID=0.123，远优于最佳基线CondMDI的0.943（Table 1）。碰撞帧率从0.262降至0.113，最大穿透深度从0.058m降至0.043m，足滑率（0.248）和抖动率（0.194）同样全面领先。值得注意的是，SceneMI直接预测SMPL参数，避免了基线方法所需的额外优化拟合后处理，推理速度显著更快（39.6s vs CondMDI 162.4s，Table 7）。

![[assets/figures/papers/paper_list_l1772_SceneMI_Motion_In_betweening_for_Modeling_Human_Scene_Interaction/figures/004_Table_1.jpg]]
*Table 1: Quantitative scene-aware motion in-betweening results on TRUMANS dataset [31] with noise-free keyframes. Our method excels in in-betweening within scene constraints across various metrics. The keyframe interval is set to r = 60 frames. Bold represents the best value, and underlined represents the second-best*

![[assets/figures/papers/paper_list_l1772_SceneMI_Motion_In_betweening_for_Modeling_Human_Scene_Interaction/figures/012_Table_7.jpg]]
*Table 7: Time required to obtain actual parameters for motion*

### 场景感知的因果效应验证

场景感知模块是SceneMI的核心贡献，通过双尺度编码（全局体素ViT + 局部BPS）显式注入场景约束。消融实验（Table 1）揭示：移除全局与局部场景特征后，碰撞帧率从0.113升至0.131。更关键的证据来自近距离交互帧的专项评估（Table 2）——在人体与场景紧密接触的帧上，场景感知使碰撞帧率从0.237降至0.162，降幅达31.6%。这直接证明双尺度编码有效捕获了细粒度的空间约束，而非仅依赖运动先验进行插值。

![[assets/figures/papers/paper_list_l1772_SceneMI_Motion_In_betweening_for_Modeling_Human_Scene_Interaction/figures/005_Table_2.jpg]]
*Table 2: Quantitative evaluation on the close-proximity humanscene interaction frames from the TRUMANS [31]*

### 噪声感知策略的关键作用

现实场景中关键帧常含噪声（如单目重建误差），传统插值方法假设关键帧精确，在此条件下性能急剧退化。SceneMI通过划分去噪时段（T*=20，总步数T=1000）实现噪声感知：在扩散早期[t∈[T, T*+1]使用带噪声关键帧引导，后期[t∈[T*, 1]联合去噪。

在密集噪声关键帧条件下（r=3, 噪声水平l=1，Table 3），SceneMI取得FID=0.118，远超CondMDI的3.136。关闭噪声感知策略（T*=0）使FID退化至0.157，直接验证了分割去噪时段的必要性。这一机制的本质是利用扩散模型早期步骤的粗粒度结构探索能力容忍关键帧噪声，后期精细去噪阶段再联合优化。

![[assets/figures/papers/paper_list_l1772_SceneMI_Motion_In_betweening_for_Modeling_Human_Scene_Interaction/figures/006_Table_3.jpg]]
*Table 3: Quantitative scene-aware motion in-betweening results TRUMANS dataset [31] with synthetic noise. keyframes are provided, using an interval of*

### 真实世界泛化与降噪能力

GIMO数据集包含真实采集噪声，是验证跨域泛化的理想基准。SceneMI在r=15间隔下将原始GIMO数据的足滑率从0.261降至0.163（降幅37.5%），抖动率从0.573降至0.249（降幅56.5%）（Table 4）。消融显示：噪声感知对运动质量改善起主导作用，而场景感知有效降低碰撞。这证明SceneMI不仅能插值合成运动，还可作为真实运动数据的后处理降噪工具。

![[assets/figures/papers/paper_list_l1772_SceneMI_Motion_In_betweening_for_Modeling_Human_Scene_Interaction/figures/008_Table_4.jpg]]
*Table 4: Quantitative evaluation on real-world GIMO [98], which naturally contains noise arising from acquisition equipment, using an interval of r = 15. Through motion in-betweening, our method demonstrates the ability to reduce foot skating and jerk that are prevalent in the original motion data. Noise awareness plays a key role in improving motion quality while scene-awareness effectively reduces collisions. Bold represents the best value, and underlined represents the second-best*

### 关键设计消融

**体型编码**：7维关节-关节距离特征（含胸部与臀部厚度）的消融（Table 8）显示，去除体型编码使MJPE All从0.023m升至0.038m，说明体型先验有助于运动与个体身体比例的对齐。

**关键帧选择鲁棒性**：不同采样策略（均匀间隔、随机概率、包含首尾帧）下FID稳定在0.118-0.125范围（Table 6），证明方法对关键帧密度和选择方式不敏感。

**随机种子稳定性**：20次随机运行下关键指标均值和95%置信区间（Table 9）验证了结果的统计可靠性。

### 失败模式与边界

Figure 10揭示两类典型失败案例：训练数据中罕见的交互模式（如狭缝穿行）因样本稀疏导致运动质量下降；真实场景几何重建质量差或高度复杂时，场景编码无法充分捕获细节约束。此外，当前模型仅支持固定121帧长度，长序列需自回归拼接可能引入累积误差，且关键帧假设为完整姿态，不支持部分姿态输入。

### 应用验证

SceneMI可集成至视频重建管线（Figure 5-7）：从单目视频重建场景几何与关键帧后，SceneMI合成场景一致的过渡运动，生成物理合理的3D人-场景动画。在长间隔关键帧（4秒，Figure 9）和语义生成关键帧（Figure 8）条件下同样表现鲁棒，展示了方法的实际应用潜力。

![[assets/figures/papers/paper_list_l1772_SceneMI_Motion_In_betweening_for_Modeling_Human_Scene_Interaction/figures/009_Figure_5.jpg]]
*Figure 5: SceneMI can be applied to reconstructed scenes and keyframes from video, facilitating realistic and physically plausible human-scene interaction reconstruction from monocular video*

![[assets/figures/papers/paper_list_l1772_SceneMI_Motion_In_betweening_for_Modeling_Human_Scene_Interaction/figures/016_Figure_9.jpg]]
*Figure 9: Result with a long-term keyframe interval. The model synthesizes long-horizon motion while avoiding large obstacles*

### 补充图表

![[assets/figures/papers/paper_list_l1772_SceneMI_Motion_In_betweening_for_Modeling_Human_Scene_Interaction/figures/013_Table_8.jpg]]
*Table 8: Ablation study on our hyperparmeters setting*

![[assets/figures/papers/paper_list_l1772_SceneMI_Motion_In_betweening_for_Modeling_Human_Scene_Interaction/figures/011_Table_6.jpg]]
*Table 6: Quantitative evaluation of diverse keyframe selection strategies on noisy TRUMANS test set with a fixed noise level l = 1. We select keyframes using different strategies, such as at a uniform interval r or with a random probability p, including start and end frames. Our method shows robustness performance from highly sparse to dense keyframes, regardless of keyframe density or selection*

![[assets/figures/papers/paper_list_l1772_SceneMI_Motion_In_betweening_for_Modeling_Human_Scene_Interaction/figures/017_Table_9.jpg]]
*Table 9: Evaluation across multiple random seeds. We report the mean and 95% confidence intervals for key metrics over 20 runs*

## 方法谱系与知识库定位

### 问题域的重新定义：从无条件生成到场景感知插值

SceneMI 将人-场景交互（HSI）建模从“无条件或文本条件生成”重新定义为**场景感知的运动插值（scene-aware motion in-betweening）**任务。这一转变的核心动机在于：现有方法要么完全忽略3D场景约束（如 MDM、StableMoFusion），要么将场景作为生成条件但缺乏对关键帧的精确控制（如 SceneDiffuser、Wang et al. 的CVAE方案），而传统运动插值方法（如 OmniControl、CondMDI）虽然支持关键帧约束，却假设关键帧精确且无视环境障碍。SceneMI 的定位恰好填补了这三者之间的空白——在噪声关键帧和复杂场景的双重约束下，同时实现运动平滑性与物理合理性。

### 与现有工作的关系图谱

**场景无关的扩散运动生成基线（MDM、StableMoFusion）**：这些方法将人体运动建模为无条件或文本条件的时间序列生成任务，完全不编码3D场景信息。在实验中，它们被重新训练以适应场景插值任务（替换文本编码器为全局场景ViT编码器，并在推理时采用imputation采样），但其性能仍显著低于SceneMI——这从反面证明了**场景感知编码**对于降低碰撞率和提升运动质量的关键作用。

**场景感知的扩散生成基线（SceneDiffuser、Wang et al. 的CVAE方案）**：SceneDiffuser 将场景编码与强化学习结合以生成场景约束下的运动，但其缺乏对关键帧的精确控制能力。Wang et al. 的CVAE方案虽然编码场景，但受限于VAE的表达能力，难以处理长序列和复杂交互。SceneMI 通过扩散模型的强生成能力与双尺度场景编码，在保持场景感知的同时实现了对稀疏关键帧的精确插值。

**扩散运动插值基线（OmniControl、CondMDI）**：这是与SceneMI最直接相关的方法类别。OmniControl 支持轨迹控制，CondMDI 是专门的扩散插值方法，但两者均**未编码场景信息**且**假设关键帧无噪声**。在TRUMANS无噪声关键帧实验中，CondMDI 的FID为0.943，而SceneMI达到0.123（Table 1），差距近8倍。当关键帧含噪声时，CondMDI 的FID恶化至3.136，而SceneMI仅0.118（Table 3），差距扩大至26倍。这揭示了SceneMI的噪声感知采样策略（划分去噪区间）对于处理真实世界噪声输入的决定性优势。

### 方法谱系中的核心创新定位

SceneMI 的方法贡献可定位于三个层次：

1. **表征层**：双尺度场景编码（全局占用体素 + 局部BPS）是区别于所有基线方法的独特设计。全局ViT编码提供场景的整体空间上下文，局部BPS编码基于关键帧周围的64个锚点捕捉精细的交互几何。消融实验表明，移除场景感知（同时去除全局和局部编码）使碰撞帧率从0.113升至0.131，且在近距离交互帧上碰撞率从0.162升至0.237（Table 2），证实了双尺度设计的互补性。

2. **机制层**：噪声感知的扩散插值策略是SceneMI区别于CondMDI等扩散插值方法的核心机制。其关键设计在于划分去噪时段：在扩散早期（$t \in [T, T^*+1]$）使用带噪声关键帧进行引导，在后期（$t \in [T^*, 1]$）联合去噪。这一策略利用了扩散模型天然的去噪能力——早期步骤处理全局结构，后期步骤细化细节——使得模型能够在噪声环境下同时满足关键帧约束与环境约束。当关闭噪声感知（$T^*=0$）时，噪声关键帧下的FID从0.118退化为0.157（Table 3），验证了分割去噪的必要性。

3. **应用层**：SceneMI 直接预测SMPL参数，避免了基线方法所需的额外优化拟合后处理（如MDM、StableMoFusion需要将生成的运动拟合到SMPL），推理速度显著更快（39.6s vs CondMDI 162.4s，Table 7）。这一设计选择使其能够直接集成到视频重建流程（Video2Animation pipeline）中，实现从单目视频到物理合理HSI重建的端到端应用。

### 适用边界与失效模式

**数据分布边界**：SceneMI 在罕见的人-场景交互模式上表现不佳，如狭缝穿行场景（Figure 10左），因训练数据中此类样本极少。这是数据驱动方法的固有局限，而非架构缺陷。

**场景质量边界**：当真实场景几何重建质量较差或高度复杂时，场景编码可能无法充分捕获细节约束（Figure 10右）。这提示未来的改进方向可能在于更鲁棒的场景表征或在线场景优化。

**序列长度边界**：SceneMI 目前仅支持固定长度（N=121帧）的运动插值，长序列需自回归拼接，可能引入累积误差。这是扩散模型在时序生成中的普遍挑战。

**关键帧完整性假设**：当前模型假设关键帧为完整姿态，未支持部分姿态关键帧（如仅手部或脚部）的输入。这限制了其在部分观测场景（如遮挡、多视角不完整）中的应用灵活性。

### 开放问题与未来方向

1. **模型级融合**：当前场景编码与运动表征采用特征级拼接（concat），如何实现更深度的模型级融合（如交叉注意力或场景条件归一化层的结构化注入），以替代简单的拼接方式，是提升场景约束精度的潜在方向。

2. **部分关键帧支持**：如何处理部分姿态关键帧（如仅手部或脚部）的输入条件，以拓展在部分观测场景中的应用灵活性，是实用化道路上的关键问题。

3. **语义条件扩展**：能否引入文本控制或其他语义条件，以实现更丰富的场景交互语义生成（如“坐在椅子上”而非仅满足几何约束），将SceneMI从几何插值拓展为语义交互生成。

4. **动态场景泛化**：如何将方法扩展至动态场景或包含可动物体的环境，以支持更一般的人-物-场景交互，是向通用HSI建模迈进的重要挑战。

5. **长序列生成**：突破固定长度限制，实现可变长度或自适应长度的场景感知运动插值，将显著提升模型在动画制作、机器人仿真等实际应用中的可用性。

## 原文 PDF

![[paperPDFs/ICCV_2025/SceneMI_Motion_In_Betweening_for_Modeling_Human_Scene_Interactions.pdf]]
