---
title: "AnyLift: Scaling Motion Reconstruction from Internet Videos via 2D Diffusion"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/AnyLift_Scaling_Motion_Reconstruction_from_Internet_Videos_via_2D_Diffusion.pdf
project_link: null
code_link: null
aliases:
- AnyLift
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
- topic/generative_models_diffusion
core_operator: 引入相机轨迹与对极线条件化的2D扩散模型，并结合混合数据源训练策略（互联网视频关键点+重投影局部姿态），使模型能从有限的单一视点视频学习多视角2D运动先验，从而实现在动态相机下的3D重构。
primary_logic: 将3D重建分解为两阶段：第一阶段通过条件单视角2D扩散生成多视角一致的2D训练数据；第二阶段训练多视角2D扩散模型直接从单视角输入产生一致的多视角2D运动，进而通过重投影优化恢复世界坐标3D运动，全程无需3D监督。
claims:
- 在AIST++动态相机设定下，AnyLift相比MVLift根位移误差显著降低（64.2 vs 64.9），MPJPE大幅改善（109.3 vs 122.1），证明动态相机条件下的鲁棒性。
- 在自采集的体操视频上，AnyLift的J_2D为21.6，远优于GVHMR的71.5，且FID为10.9，表明方法在稀有运动类型上的有效性。
- 消融实验表明：去除混合训练策略后，体操视频上J_2D上升至23.5，FID升至11.5；武术视频上J_2D升至15.7，FID升至4.1，验证了混合训练的关键作用。
- AIST++ (dynamic camera synthetic) 上 MPJPE = 109.3
---

# AnyLift: Scaling Motion Reconstruction from Internet Videos via 2D Diffusion

> [!tip] 核心洞察
> 将3D重建分解为两阶段：第一阶段通过条件单视角2D扩散生成多视角一致的2D训练数据；第二阶段训练多视角2D扩散模型直接从单视角输入产生一致的多视角2D运动，进而通过重投影优化恢复世界坐标3D运动，全程无需3D监督。

| 字段 | 内容 |
|------|------|
| 中文题名 | AnyLift：通过2D扩散从互联网视频扩展运动重建 |
| 英文题名 | AnyLift: Scaling Motion Reconstruction from Internet Videos via 2D Diffusion |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2604.17818) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction #topic/generative_models_diffusion |
| Method | AnyLift |
| Dataset | AIST++, BEHAVE |

> [!tip] 效果简介
> - AIST++ (dynamic camera synthetic) 上，MPJPE 109.3 vs 122.1 (MVLift) (-12.8)。
> - 自采集体操视频 上，J_2D 21.6 vs 71.5 (GVHMR) (-49.9)。
> - BEHAVE (Box类别，静态相机) 上，MPJPE 42.68 vs 54.40 (VisTracker) (-11.72)。

## 概要

从动态摄像头拍摄的单目视频中恢复世界坐标系下的全局一致3D人体运动及人物交互（HOI），长期受制于两个瓶颈：其一，现有方法多依赖静态相机假设，难以处理真实互联网视频中普遍存在的相机运动；其二，基于3D动作捕捉（MoCap）数据训练的模型，在体操、武术等MoCap数据稀缺的稀有运动类型上泛化能力不足。AnyLift 针对上述瓶颈提出了一种无需3D监督的两阶段框架，核心思路是将3D重建问题转化为多视角2D运动的一致性生成问题——先训练一个以相机轨迹和对极线为条件的单视角2D扩散模型，合成多视角2D训练数据；再基于此训练多视角2D扩散模型，从单视角输入直接生成多视角一致的2D运动，最后通过重投影优化恢复世界坐标3D运动。

方法层面的关键创新在于两处“因果旋钮”的调节。第一，在2D扩散模型的去噪过程中注入相机轨迹与对极线条件，使模型能够利用动态相机视频进行训练，从而摆脱静态相机的限制。第二，引入混合数据源训练策略，将互联网视频中提取的全局2D关键点与从重建3D运动重投影得到的局部2D姿态相结合，有效缓解了互联网视频中视点覆盖严重受限的问题（如体操视频中人体朝向高度集中于少数方向，见 Figure S.1），稳定了训练过程并丰富了视点多样性。

实验证据表明上述设计带来了显著的性能增益。在AIST++动态相机设定下，AnyLift 的 MPJPE 达到 109.3，相比 MVLift 的 122.1 降低了 12.8，根位移误差也从 64.9 降至 64.2（Table 1）。在自采集的互联网体操视频上，AnyLift 的 2D 关节误差（J_2D）仅为 21.6，远优于 GVHMR 的 71.5，FID 低至 10.9（Table 2, Table 5），证明其对稀有运动类型的适应能力。消融实验进一步确认，去除混合训练策略后，体操视频上的 J_2D 从 21.6 退化至 23.5，FID 从 10.9 升至 11.5；武术视频上 J_2D 从 15.1 退化至 15.7，FID 从 3.6 升至 4.1（Table 5），验证了混合训练的关键作用。在 BEHAVE 数据集的 HOI 重建任务上，AnyLift 在静态相机下的 MPJPE 为 42.68，显著优于 VisTracker 的 54.40（Table 4），并在动态相机条件下保持了鲁棒性。



从单目视频中恢复世界坐标系下的3D人体运动是计算机视觉领域的长期挑战。传统方法（如**SMPLify**，Bogo et al., ECCV 2016）依赖2D重投影优化，无需训练但精度有限；基于3D监督的方法（如**WHAM**，Shin et al., CVPR 2024；**GVHMR**，Shen et al., SIGGRAPH Asia 2024）虽能实现世界坐标重建，却受限于动作捕捉数据的规模与多样性，对体操、武术等MoCap数据中罕见的运动类型泛化能力不足。

**MVLift**率先探索了无需3D监督的路线——通过多视图2D扩散模型从静态相机视频中重建3D运动。然而，该方法存在两个关键瓶颈：

1. **动态相机不兼容**：MVLift假定相机静止，无法处理真实互联网视频中普遍存在的相机运动，导致根轨迹估计严重漂移。
2. **视点覆盖受限**：互联网视频中人体朝向高度集中（如Figure S.1所示，体操视频中人脸朝向分布极不均匀），单一视点的2D关键点序列难以提供足够的多视角信息用于3D重建。

**人物交互（HOI）重建**面临更严峻的挑战。现有方法（如**VisTracker**，Xie et al., CVPR 2023）同样假设静态相机，且需要预计算的2D关键点，难以推广到动态相机拍摄的真实交互场景。

上述瓶颈的根源在于：**缺乏一种能从有限单视点视频中学习多视角2D运动先验的机制，且该机制必须兼容动态相机条件**。AnyLift正是围绕这一核心矛盾展开设计——通过相机轨迹条件化的2D扩散模型与混合数据源训练策略，将3D重建分解为“多视角2D合成→3D优化”的两阶段流程，全程无需3D真值监督。



## 核心方法与创新机理

AnyLift 的核心创新在于将 3D 人体运动及人物交互（HOI）重建从静态相机假设中解放出来，使其能够处理动态相机拍摄的单目视频。相对于依赖 3D 动作捕捉数据或假定相机静止的前序工作，AnyLift 通过三个关键机制实现了突破。

**1. 相机轨迹与对极线条件化的 2D 扩散模型**

现有方法如 **MVLift** 使用无相机条件的多视图扩散，无法处理动态相机视频。AnyLift 在单视角 2D 运动扩散模型的去噪过程中注入相机轨迹 $\mathbf{C}$ 和对极线 $\mathbf{L}$ 作为条件，使模型能够学习动态相机下的 2D 运动先验。具体而言，扩散模型以 $L1$ 重建损失进行训练：

$$\mathcal{L} = \mathbb{E}_{\mathbf{X}_0, n} \| \mathbf{X}_0 - \mathbf{X}_\theta(\mathbf{X}_n, n, \mathbf{C}, \mathbf{L}) \|_1$$

这一条件化设计使得模型能够从任意相机运动捕捉的 2D 关键点序列中学习，并为后续多视角合成提供基础。

**2. 混合数据源训练策略**

互联网视频（如体操、武术）的视点覆盖极度受限——如 Figure S1 所示，人物面向分布高度集中于特定方向。为克服这一瓶颈，AnyLift 引入混合训练策略，将两类互补的 2D 运动数据结合：

- **全局 2D 姿态**：从真实互联网视频提取的完整 2D 关键点序列，保留真实运动动态；
- **局部 2D 姿态** $\mathbf{X}^{\mathrm{proj}}$：由现成估计器重建的 3D 运动经重投影获得的 2D 姿态，通过去除髋关节的投影扩散损失训练：

$$\mathcal{L}^{\mathrm{proj}} = \mathbb{E}_{\mathbf{X}_0, n} \| \mathbf{M} \odot \mathbf{X}_0 - \mathbf{M} \odot \mathbf{X}_\theta(\mathbf{X}_n^{\mathrm{proj}}, n, \mathbf{C}, \mathbf{L}) \|_1$$

该策略显著丰富了训练视点覆盖，使模型在稀有运动类型上仍能生成合理的多视角 2D 运动。消融实验（Table 5）表明，去除混合训练后，体操视频上 $J_{2D}$ 从 21.6 退化至 23.5，FID 从 10.9 升至 11.5，验证了其关键作用。

**3. 动态相机下的 HOI 重建扩展**

**MVLift** 仅处理人体运动且需要预计算 2D 关键点；**VisTracker**（Xie et al., CVPR 2023）虽能重建人物交互，但假设静态相机。AnyLift 将物体 2D 关键点 $\mathcal{O}$ 与人关键点 $\mathbf{X}$ 拼接为统一表示，训练类别感知的多视角扩散模型，并支持在真实视频中跟踪物体关键点以求解 3D 位姿。这使 AnyLift 成为首个在动态相机设定下实现 HOI 重建的方法，在 BEHAVE 数据集上 MPJPE 从 VisTracker 的 54.40 降至 42.68（Table 4）。

**创新总结**

| 创新维度 | 基线方法 | AnyLift 改进 |
|---------|---------|-------------|
| 2D 扩散条件 | MVLift：无相机条件 | 注入相机轨迹与对极线条件 |
| 训练数据 | MVLift：静态多视角或重投影数据 | 混合互联网视频全局姿态 + 重投影局部姿态 |
| 相机假设 | MVLift / VisTracker：静态相机 | 支持任意动态相机运动 |
| 重建范围 | MVLift：仅人体运动 | 扩展至人物交互（HOI）重建 |

这些创新使 AnyLift 在动态相机条件下实现了鲁棒的 3D 重建：AIST++ 动态相机设定下 MPJPE 为 109.3（vs MVLift 122.1）；自采集互联网体操视频上 $J_{2D}$ 达 21.6（vs **GVHMR** 的 71.5，Shen et al., SIGGRAPH Asia 2024），证明了方法在 MoCap 数据中罕见的运动类型上的有效性。



AnyLift 提出一个统一的两阶段框架，从动态相机拍摄的单目视频中同时重建世界坐标系下的 3D 人体运动与人物交互（HOI），全程无需 3D 监督。

### 两阶段流水线

**第一阶段：多视角 2D 合成数据生成。** 核心任务是制备具有多样化相机轨迹的训练数据。为此，AnyLift 首先训练一个**相机轨迹与对极线条件化的单视角 2D 运动扩散模型**，使其从有限的单视点视频中学习动态相机下的 2D 运动先验。随后，利用该先验通过得分蒸馏采样（Score Distillation Sampling, SDS）结合多视角一致性损失，为每个输入视频合成多视角 2D 运动序列，作为第二阶段的训练数据。

**第二阶段：多视角 2D 运动扩散与 3D 恢复。** 使用第一阶段合成的多视角数据，训练一个**多视角 2D 运动扩散模型**。给定真实视频的单视角 2D 输入，该模型生成跨视角一致的 2D 运动序列。最后，通过最小化多视角重投影误差恢复 3D 关节位置，并用 VPoser 拟合 SMPL 参数，得到世界坐标系下的 3D 人体运动。

### 关键设计：混合数据源训练策略

互联网视频的视点覆盖严重受限——例如体操与武术视频中人脸朝向分布高度集中（Figure S1），直接训练会导致模型缺乏多视角泛化能力。AnyLift 引入**混合训练策略**，将两类互补的 2D 运动数据结合：
- **全局 2D 姿态**：从真实互联网视频提取的 2D 关键点序列；
- **局部 2D 姿态**：将现成估计器重建的 3D 运动重投影到随机虚拟视点，得到局部 2D 投影（去除髋关节以保持全局轨迹一致性）。

两类数据共享同一扩散模型训练，但对重投影的局部姿态采用带掩码的投影扩散损失（Eq. 4），使模型在保持真实视频数据分布的同时获得丰富的视点覆盖。消融实验证实，去除混合训练后，体操视频上 J₂D 从 21.6 退化至 23.5，FID 从 10.9 升至 11.5（Table 5），验证了该策略的关键作用。

### HOI 重建扩展

对于人物交互场景，AnyLift 将物体 2D 关键点与人关键点拼接为统一表示，训练类别感知的多视角扩散模型。在真实视频中，通过跟踪物体关键点并结合预定义的规范关键点，求解物体 6D 位姿（旋转、平移及全局尺度），实现 3D HOI 重建。

### 输入输出流

- **输入**：动态相机单目视频，经现成工具提取的 2D 关键点序列与相机轨迹。
- **中间产物**：第一阶段合成的多视角 2D 运动序列。
- **输出**：世界坐标系下的 3D 人体运动（SMPL 参数与根位移）或人物交互运动（人体 SMPL + 物体 6D 位姿）。

整体框架见 Figure 2。

![[assets/figures/papers/paper_list_l4_https_arxiv_org_abs_2604_17818/figures/002_Figure_2.jpg]]
*Figure 2: Overview of AnyLift. (a) We first train a single-view 2D motion diffusion model conditioned on camera trajectories and epipolar lines to synthesize multi-view 2D training data. (b) During training, we employ a hybrid data source strategy that enhances viewpoint coverage by combining global 2D pose sequences from videos with locally reprojected poses. (c) Finally, we train a multi-view 2D motion diffusion model to reconstruct consistent world-coordinated 3D human and HOI motions from real-world videos*



AnyLift 的核心架构围绕一个两阶段框架展开：第一阶段合成多视角2D训练数据，第二阶段训练多视角2D运动扩散模型，最终通过重投影优化恢复世界坐标系下的3D运动。以下详述其关键模块与数学公式。

### 3.1 相机轨迹条件单视角2D运动扩散模型

第一阶段的核心是训练一个**以相机轨迹和对极线为条件的单视角2D运动扩散模型**，使其能够从动态相机视频中学习2D运动先验。给定一段长度为 $T$ 的单视角2D关键点序列 $\mathbf{X} \in \mathbb{R}^{T \times K \times 2}$（$K$ 为关键点数量），模型需要学习在任意相机运动下的2D运动分布。

**前向扩散过程**遵循标准DDPM范式，逐步向干净数据 $\mathbf{X}_0$ 添加高斯噪声：

$$q(\mathbf{X}_n | \mathbf{X}_{n-1}) = \mathcal{N}(\mathbf{X}_n; \sqrt{1 - \beta_n} \mathbf{X}_{n-1}, \beta_n \mathbf{I})$$

其中 $\beta_n$ 为第 $n$ 步的噪声调度参数，$\mathbf{X}_n$ 为加噪后的2D运动序列。

**训练损失**采用直接预测干净样本 $\mathbf{X}_0$ 的策略，网络 $\mathbf{X}_\theta$ 以加噪样本 $\mathbf{X}_n$、扩散步数 $n$、相机轨迹条件 $\mathbf{C}$ 和对极线条件 $\mathbf{L}$ 为输入，最小化L1重建损失：

$$\mathcal{L} = \mathbb{E}_{\mathbf{X}_0, n} \| \mathbf{X}_0 - \mathbf{X}_\theta(\mathbf{X}_n, n, \mathbf{C}, \mathbf{L}) \|_1$$

相机轨迹条件 $\mathbf{C}$ 编码了每一帧的相机外参变化，使模型能够区分人体自身运动与相机运动引起的2D投影变化；对极线条件 $\mathbf{L}$ 则显式注入跨视角几何约束，为后续多视角一致性合成提供基础。

### 3.2 混合数据源训练策略

为克服互联网视频中视点覆盖严重受限的问题（如体操、武术视频中人脸朝向高度集中于特定角度，见Figure S.1），AnyLift引入**混合训练策略**，将两种互补的2D运动数据源结合：

1. **全局2D姿态**：从真实互联网视频中提取的2D关键点序列，保留了完整的全局运动信息，但视点单一。
2. **重投影局部2D姿态** $\mathbf{X}^{\text{proj}}$：利用现成的3D人体重建方法（如WHAM、GVHMR）从视频中恢复3D运动，再通过随机采样的虚拟相机轨迹重投影回2D平面，获得多视角的局部姿态。此过程移除了髋关节的全局位移，仅保留局部关节的相对运动。

对于重投影数据，扩散损失仅作用于局部关节（通过掩码 $\mathbf{M}$ 排除髋关节），避免全局位移与相机运动之间的歧义：

$$\mathcal{L}^{\text{proj}} = \mathbb{E}_{\mathbf{X}_0, n} \| \mathbf{M} \odot \mathbf{X}_0 - \mathbf{M} \odot \mathbf{X}_\theta(\mathbf{X}_n^{\text{proj}}, n, \mathbf{C}, \mathbf{L}) \|_1$$

混合训练使模型既能从真实视频中学习自然的2D运动模式，又能通过重投影数据获得丰富的视点变化，显著提升了对稀有运动类型和动态相机的泛化能力。

### 3.3 多视角2D运动合成与得分蒸馏采样

在单视角扩散模型训练完成后，AnyLift利用**得分蒸馏采样（Score Distillation Sampling, SDS）** 从学习到的2D运动先验中合成多视角一致的2D训练数据。给定输入视角的2D运动，优化目标视角 $\mathbf{X}_v$ 使其符合扩散模型学到的分布，SDS梯度为：

$$\nabla_{\mathbf{X}_v} \mathcal{L}_{\mathrm{SDS}} = \mathbb{E}_{n,\epsilon} \Bigl[ w(n) \bigl( \epsilon_{\theta}(\mathbf{X}_{v,n}, n, \mathbf{C}, \mathbf{L}) - \epsilon \bigr) \Bigr]$$

其中 $\epsilon_{\theta}$ 为扩散模型预测的噪声，$w(n)$ 为基于噪声步数的权重函数。

为确保多视角间的几何一致性，在SDS优化过程中施加**跨视角对极线匹配损失**，强制目标视角的关键点落在由输入视角决定的对极线上：

$$\mathcal{L}_{\mathrm{line}}^{u v} = \sum_{t=1}^{T} \big\langle \mathbf{L}_t^{u v}, (\mathbf{X}_{v,t}^{\mathrm{g}}, \mathbf{1}) \big\rangle$$

其中 $\mathbf{L}_t^{u v}$ 表示从视角 $u$ 到视角 $v$ 在第 $t$ 帧的对极线，$\mathbf{X}_{v,t}^{\mathrm{g}}$ 为视角 $v$ 的全局2D关键点。与MVLift不同，AnyLift仅计算相邻视角间及每个视角与输入视角间的对极线损失，以降低计算开销。

### 3.4 3D优化与HOI扩展

获得多视角一致的2D姿态序列后，通过最小化多视角重投影误差恢复3D关节位置，并使用VPoser拟合SMPL参数得到最终的3D人体网格。对于人物交互（HOI）重建，物体2D关键点 $\mathbf{O}$ 与人关键点 $\mathbf{X}$ 拼接为统一表示，训练类别感知的多视角扩散模型。物体姿态 $\mathcal{O}_t = \{ \mathbf{r}_t, \mathbf{t}_t, s \}$ 由重建的3D关键点与预定义的规范关键点通过刚性对齐求解，其中 $\mathbf{r}_t$ 为6D旋转表示，$\mathbf{t}_t$ 为平移，$s$ 为全局缩放因子。



## 实验与关键发现

AnyLift 在人体运动重建与人物交互（HOI）重建两个任务上，于合成动态相机基准、自采互联网视频以及 BEHAVE 数据集上进行了系统性验证。实验设计围绕三个核心检验目标展开：（1）动态相机条件下世界坐标 3D 重建的鲁棒性；（2）对 MoCap 数据中罕见的运动类型（体操、武术）的泛化能力；（3）混合训练策略与各模块的消融贡献。

### 人体运动重建：AIST++ 基准

AIST++ 数据集上的定量评估（Table 1）揭示了动态相机设定的瓶颈效应与 AnyLift 的应对能力。在静态相机设定（upper）下，AnyLift 与 MVLift 表现接近，MPJPE 分别为 107.3 和 108.6，根位移误差 $T_{\text{root}}$ 分别为 59.4 和 60.1，表明二者在常规设定下均能有效恢复 3D 运动。切换至合成动态相机设定（lower）后，基线方法出现显著退化：MVLift 的 MPJPE 从 108.6 升至 122.1（+13.5），根位移误差从 60.1 升至 64.9（+4.8）。AnyLift 在相同条件下将 MPJPE 控制在 109.3，根位移误差为 64.2，相比 MVLift 分别降低 12.8 和 0.7。这一对比直接验证了相机轨迹条件与对极线约束在动态相机场景下的因果作用——当相机运动引入额外的投影歧义时，仅依赖静态先验的方法无法维持多视角一致性，而 AnyLift 的条件扩散模型有效消解了这一歧义。

![[assets/figures/papers/paper_list_l4_https_arxiv_org_abs_2604_17818/figures/004_Table_1.jpg]]
*Table 1: Quantitative evaluation on the AIST++ dataset [19] under (1) static-camera setup (upper) and (2) dynamic-camera setup (lower). AnyLift achieves competitive 3D joint accuracy and improved root translation estimation while maintaining robustness under dynamic camera*

### 人体运动重建：自采互联网视频

自采的体操与武术视频构成了更具挑战性的检验场景。这类运动在 MoCap 数据集中极为罕见，且拍摄视角单一、相机运动自由。Table 2 报告了与多个基线的全面对比。

![[assets/figures/papers/paper_list_l4_https_arxiv_org_abs_2604_17818/figures/003_Table_2.jpg]]
*Table 2: Quantitative evaluation on our collected Internet videos. AnyLift outperforms all baselines across most metrics, demonstrating the plausibility of our method on Internet videos*

在体操视频上，AnyLift 的 2D 关节误差 $J_{\text{2D}}$ 为 21.6，远优于 GVHMR 的 71.5 和 WHAM 的 60.9；在武术视频上，$J_{\text{2D}}$ 为 15.1，同样显著低于 GVHMR 的 36.6。更关键的是，基于 3D 监督的方法（WHAM、GVHMR）在这些稀有运动上暴露出严重的分布外泛化问题：GVHMR 在体操视频上的 FID 高达 48.8，WHAM 为 36.7，而 AnyLift 仅为 10.9。这表明依赖 AMASS 等有限动作捕捉数据训练的方法，在面对训练分布之外的运动模式时会产生不自然的姿态估计，而 AnyLift 通过直接从互联网视频的 2D 关键点学习运动先验，绕过了 3D 标注数据的分布限制。

Table 3 的人工评估进一步佐证了定量指标的可靠性。参与者在 68.3% 的对比中偏好 AnyLift 的重建结果，主要理由为更好的地面接触（ground contact）与运动质量。这一主观偏好与客观指标中的脚滑动分数（FS）改善方向一致，说明方法在物理合理性上确实优于基线。

![[assets/figures/papers/paper_list_l4_https_arxiv_org_abs_2604_17818/figures/005_Table_3.jpg]]
*Table 3: Human study on reconstructed human motions from our collected Internet videos. Participants prefer our reconstruction results for their better ground contact and motion quality*

定性对比（Figure 3）直观展示了差异的根源：基线方法常出现根轨迹漂移、局部姿态错误及自穿透伪影，而 AnyLift 生成的全身轨迹与姿态更为连贯。这归因于两阶段框架中多视角 2D 运动扩散模型提供的跨视角几何约束——即使输入仅为单目视频，模型仍能生成符合多视角一致性的 2D 运动序列，从而在 3D 优化阶段约束根位移与关节位置的解空间。

![[assets/figures/papers/paper_list_l4_https_arxiv_org_abs_2604_17818/figures/006_Figure_3.jpg]]
*Figure 3: Qualitative comparison of human motion reconstruction on our collected Internet videos. AnyLift produces more plausible motions, mitigating the root trajectory errors, inaccurate local body pose, and self-penetration artifacts observed in baselines*

### 人物交互（HOI）重建：BEHAVE 数据集

HOI 重建实验在 BEHAVE 数据集上展开，覆盖椅子、桌子、盒子等多个物体类别。Table 4 显示，在静态相机设定下，AnyLift 在所有类别上的 MPJPE 均优于 VisTracker 基线：盒子类别 42.68 vs 54.40（-11.72），椅子类别 45.83 vs 55.19（-9.36）。切换至动态相机设定后，VisTracker 的性能进一步恶化，而 AnyLift 保持了相对稳定的表现，验证了相机条件模型在 HOI 场景中的迁移有效性。

![[assets/figures/papers/paper_list_l4_https_arxiv_org_abs_2604_17818/figures/008_Table_4.jpg]]
*Table 4: Quantitative evaluation on the BEHAVE dataset [1] under (1) static-camera setup (upper) and (2) dynamic-camera setup (lower). AnyLift outperforms all baselines across object categories and achieves robust performance under dynamic-camera conditions*

定性结果（Figure 4）揭示了 VisTracker 的典型失败模式：在椅子交互中，人体与椅面出现明显穿透；在桌子交互中，接触关系不准确。AnyLift 生成的交互序列则展现出准确的接触与最小的穿透。这得益于统一的人-物关键点表示与类别感知的多视角扩散模型——物体关键点与人关键点在扩散过程中共享相同的极线约束，从而在 3D 优化阶段同时约束人体与物体的空间关系。

![[assets/figures/papers/paper_list_l4_https_arxiv_org_abs_2604_17818/figures/007_Figure_4.jpg]]
*Figure 4: Qualitative comparison of HOI reconstruction on the BEHAVE [1] dataset. We show results on two object categories, chair and table. AnyLift produces coherent and physically plausible human-object interactions with accurate contact and minimal penetration*

### 消融实验：混合训练策略的关键作用

Table 5 的消融实验直接检验了混合训练策略的因果贡献。移除混合训练（即仅使用互联网视频的全局 2D 姿态，不加入重投影局部姿态）后，体操视频上的 $J_{\text{2D}}$ 从 21.6 退化至 23.5（+1.9），FID 从 10.9 升至 11.5（+0.6）；武术视频上的 $J_{\text{2D}}$ 从 15.1 升至 15.7（+0.6），FID 从 3.6 升至 4.1（+0.5）。

![[assets/figures/papers/paper_list_l4_https_arxiv_org_abs_2604_17818/figures/009_Table_5.jpg]]
*Table 5: Ablation study on our collected Internet videos. Performance drops across all metrics without incorporating local 2D poses from diverse viewpoints*

这一退化背后是训练数据中视点覆盖的严重失衡。如 Figure S1 所示，互联网体操与武术视频中人脸朝向分布高度集中（体操视频中约 80% 的帧面向相机正面 ±30° 范围内），导致模型在训练过程中极少观察到侧面或背面的 2D 运动模式。混合训练策略通过引入由现成估计器重建后重投影的局部 2D 姿态，人工扩充了视点多样性，使模型能够学习到更完整的运动先验。消融结果证实了这一设计的必要性——缺少该策略时，模型对非正面视角的泛化能力显著下降，直接表现为 2D 关节误差与运动分布质量（FID）的双重恶化。

![[assets/figures/papers/paper_list_l4_https_arxiv_org_abs_2604_17818/figures/010_Figure_S.1.jpg]]
*Figure S.1: Facing direction distributions of estimated humans in the gymnastics (upper) and martial arts (lower) videos under the camera coordinate system. The angular axis indicates the facing direction and the radial axis represents number of frames*

### 方法谱系与知识库定位

AnyLift 在方法谱系中处于“无 3D 监督的多视角 2D 扩散 + 重投影优化”这一新兴分支。与依赖 3D 动作捕捉数据训练的方法形成鲜明对比：**WHAM**（Shin et al., CVPR 2024）和 **GVHMR**（Shen et al., SIGGRAPH Asia 2024）均使用 AMASS 等大规模 MoCap 数据集，在分布内运动上表现优异，但在体操、武术等稀有运动上泛化失败。**SMPLify**（Bogo et al., ECCV 2016）作为经典的 2D 重投影优化方法，无需训练但缺乏运动先验，难以处理遮挡与深度歧义。

在无 3D 监督的方法中，MVLift 是最直接的参照点。AnyLift 在三个关键维度上对其进行了扩展：（1）引入相机轨迹与对极线条件，使扩散模型能够处理动态相机；（2）设计混合训练策略，缓解互联网视频的视点覆盖不足问题；（3）将框架扩展至 HOI 重建，通过统一的人-物关键点表示与类别特定模型实现物体运动恢复。**VisTracker**（Xie et al., CVPR 2023）同样处理 HOI 重建，但假设静态相机且依赖特定物体模板，AnyLift 在动态相机设定下展现出更强的鲁棒性。

当前方法的已知局限包括：对 2D 关键点提取质量与相机位姿估计精度敏感（这两个模块作为外部输入，其误差会传播至后续阶段）；HOI 扩展目前依赖手动设计的物体关键点，在更广泛的物体类别上需要额外的标注工作。开放问题指向端到端集成相机运动估计、提升对输入噪声的鲁棒性，以及在严重遮挡与多人物场景中的泛化验证。

### 补充图表

![[assets/figures/papers/paper_list_l4_https_arxiv_org_abs_2604_17818/figures/001_Figure_1.jpg]]
*Figure 1: Human and human-object interaction (HOI) motions lifted by our approach. Trained on 2D keypoints and corresponding camera trajectories, our framework AnyLift reconstructs world-coordinated 3D human motion and HOI from monocular videos captured by dynamic cameras. We demonstrate its effectiveness on human motion reconstruction from Internet gymnastics videos (left) and on HOI reconstruction from captured real-world videos (right). Please refer to our project page for video results*



## 定位与知识库关联

AnyLift 的核心技术路径属于**基于2D扩散先验的单目3D运动重建**这一新兴范式，其直接前身是 **MVLift**（静态相机多视图2D扩散重建）。AnyLift 在此谱系中完成了三个关键突破，使其从受控实验室设定走向真实互联网视频：

**1. 从静态相机到动态相机的范式跃迁**

MVLift 假设相机静止，通过多视图2D扩散从单视角输入生成虚拟多视角运动，再经重投影优化恢复3D。这一假设严重限制了其在真实互联网视频中的适用性——用户拍摄的视频几乎都包含相机运动。AnyLift 通过**相机轨迹与对极线条件化的2D扩散模型**，将相机运动显式注入扩散去噪过程（式2中的 $\mathbf{C}$ 和 $\mathbf{L}$ 条件），使模型能够学习动态相机下的2D运动先验。这一设计使得 AnyLift 在动态相机设定下的 AIST++ 数据集上，MPJPE 从 MVLift 的 122.1 降至 109.3（Table 1）。

**2. 混合数据源训练策略解决视点覆盖瓶颈**

互联网视频的一个根本性限制是相机视点覆盖严重受限——如 Figure S.1 所示，体操和武术视频中人脸朝向分布高度集中，意味着模型几乎只能看到单一视角的运动模式。MVLift 依赖静态多视角数据或重投影动作捕获数据，无法从这种受限数据中学习。AnyLift 的混合训练策略（Hybrid Training）将两类互补数据源结合：来自真实视频的全局2D姿态序列（提供真实运动多样性但视点单一），以及从重建3D运动重投影的局部2D姿态（提供丰富视点但运动类型受限）。消融实验（Table 5）直接验证了这一策略的关键作用：去除混合训练后，体操视频上 J_2D 从 21.6 退化至 23.5，FID 从 10.9 升至 11.5。

**3. 从人体运动到人物交互（HOI）的统一扩展**

在 HOI 重建谱系中，**VisTracker**（Xie et al., CVPR 2023）从单 RGB 相机重建人物交互轨迹，但假设静态相机；**SMPLify**（Bogo et al., ECCV 2016）通过2D重投影优化恢复3D姿态，但依赖精确的2D关键点且无时序一致性。AnyLift 将物体2D关键点与人关键点拼接为统一表示，训练类别感知的多视角扩散模型，在 BEHAVE 数据集上实现了显著提升：Box 类别下 MPJPE 从 VisTracker 的 54.40 降至 42.68（Table 4），且支持动态相机设定。

**与基于3D监督方法的对比**

当前世界坐标人体运动重建的主流方法依赖大规模3D动作捕捉数据训练，如 **WHAM**（Shin et al., CVPR 2024）使用 AMASS 数据集，**GVHMR**（Shen et al., SIGGRAPH Asia 2024）采用重力-视角坐标系。这些方法在 MoCap 覆盖的运动类型上表现良好，但在稀有运动上泛化能力有限。AnyLift 全程无需3D监督，在自采集体操视频上 J_2D 为 21.6，远优于 GVHMR 的 71.5（Table 2），证明了2D扩散先验在稀有运动类型上的独特优势。

**适用边界与开放问题**

AnyLift 目前存在几个明确的适用边界：(1) 方法对2D关键点提取及相机位姿估计的质量敏感，输入噪声会沿两阶段管道传播放大；(2) HOI 重建依赖手动设计的物体关键点，限制了向更广泛物体类别的扩展；(3) 两阶段框架（先合成多视图数据，再训练多视图扩散模型）增加了计算开销和工程复杂度。

值得关注的开放方向包括：(1) 能否将相机运动估计集成到框架中，实现端到端的联合优化？(2) 在严重遮挡或多人物交互场景中，当前的对极线约束是否足够，是否需要引入更强的物理先验？(3) 如何减少对手动设计关键点的依赖，实现更通用的 HOI 重建？这些问题的解决将决定该范式能否真正从实验室走向大规模应用。



## 原文 PDF

![[paperPDFs/CVPR_2026/AnyLift_Scaling_Motion_Reconstruction_from_Internet_Videos_via_2D_Diffusion.pdf]]
