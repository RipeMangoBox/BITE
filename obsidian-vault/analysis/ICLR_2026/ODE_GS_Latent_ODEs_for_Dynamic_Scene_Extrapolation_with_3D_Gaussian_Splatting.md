---
title: "ODE-GS: Latent ODEs for Dynamic Scene Extrapolation with 3D Gaussian Splatting"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/ODE_GS_Latent_ODEs_for_Dynamic_Scene_Extrapolation_with_3D_Gaussian_Splatting_6975a66efdbb.pdf
project_link: null
code_link: "https://github.com/patrick-kidger/torchode"
aliases:
- OG
- ODE-GS
tags:
- ICLR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
- topic/generative_models_diffusion
core_operator: 通过隐式神经ODE对高斯参数的连续时间隐动态建模，将外推转化为隐空间的序列演化，从而消除显式时间戳依赖并施加运动平滑物理先验。
primary_logic: 将动态场景重建与时间预测解耦：先训练时间条件化的插值模型获取观测窗口内的高斯轨迹，再训练一个由Transformer编码、神经ODE驱动的序列到序列模型来预测未来轨迹；通过隐空间与3D空间的平滑正则化约束，迫使预测的动力学物理合理且稳定。
claims:
- 移除神经ODE组件，采用纯自回归Transformer，NVFi平均PSNR从33.43降至23.71，证明隐式ODE是外推的核心使能器。
- ODE-GS在D-NeRF和NVFi数据集上显著优于先前最佳的插值基线和外推方法，PSNR提升18.6%–39.6%，SSIM和LPIPS同样大幅领先。
- 解耦训练（冻结插值模型再训练外推模型）显著优于端到端联合训练，所有指标均有提升，验证了分离设计的有效性。
- 隐空间与轨迹平滑正则化贡献了约1–3 dB PSNR增益，并对视觉伪影有明显的抑制作用（尤其在场景剧烈变化区域）。
---

# ODE-GS: Latent ODEs for Dynamic Scene Extrapolation with 3D Gaussian Splatting

> [!tip] 核心洞察
> 将动态场景重建与时间预测解耦：先训练时间条件化的插值模型获取观测窗口内的高斯轨迹，再训练一个由Transformer编码、神经ODE驱动的序列到序列模型来预测未来轨迹；通过隐空间与3D空间的平滑正则化约束，迫使预测的动力学物理合理且稳定。

| 字段 | 内容 |
|------|------|
| 中文题名 | ODE-GS：基于隐式常微分方程与3D高斯泼溅的动态场景外推方法 |
| 英文题名 | ODE-GS: Latent ODEs for Dynamic Scene Extrapolation with 3D Gaussian Splatting |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=XlRbpFj3lJ) · [Code](https://github.com/patrick-kidger/torchode) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction #topic/generative_models_diffusion |
| Method | ODE-GS |
| Dataset | D-NeRF, NVFi, HyperNeRF |

> [!tip] 效果简介
> - D-NeRF 上，PSNR / SSIM / LPIPS 27.30 / 0.9497 / 0.0467 vs 23.09 / 0.8584 / 0.1660 (GaussianPrediction avg) (PSNR↑18.6%, SSIM↑10.6%, LPIPS↓71.9%)。
> - NVFi 上，PSNR / SSIM / LPIPS 33.43 / 0.9471 / 0.0603 vs 28.45 / 0.9336 / 0.1024 (NVFi avg) (PSNR↑17.5%, SSIM↑1.4%, LPIPS↓41.1%; 相对于GaussianPrediction提升39.6%)。
> - HyperNeRF 上，LPIPS / PSNR / SSIM 在split-cookie, slice-banana, cut-lemon上LPIPS最低; chickchicken上PSNR和SSIM最优 vs TiNeuVox, 4D-GS 等 (定性/定量均优于所有基线)。

## 概述

动态3D场景的新视角合成与未来预测是视觉计算中的核心挑战。现有方法——无论是基于NeRF的**TiNeuVox-B**（Fang et al., 2022）还是基于3D Gaussian Splatting（3DGS）的**4D-GS**（Wu et al., 2024）、**Deformable-GS**（Yang et al., 2024）——均采用时间条件化变形网络：以显式时间戳$t$作为MLP输入，预测规范空间到当前帧的偏移。这一范式在观测时间窗口$[t_{\min}, t_{\max}]$内可实现高质量插值渲染，但一旦要求外推到$t > t_{\max}$的未来时刻，时间戳便落入训练分布外（OOD），导致渲染质量急剧退化。现有的外推尝试如**GaussianPrediction**（Zhao et al., 2024）和**NVFi**（Li et al., 2023）仍未能从根本上消除这一结构脆弱性。

**ODE-GS**针对上述瓶颈，提出了一种解耦式动态场景外推框架。其核心洞察是：将动态场景重建与时间预测分离。首先训练一个冻结的插值模型，在观测窗口内生成精确的高斯参数轨迹；随后，由一个**Transformer编码器**将过去的高斯参数序列压缩为隐状态，再由**神经ODE**驱动该隐状态在连续时间上演化，解码得到未来时刻的高斯参数。这一设计从架构层面移除了显式时间戳依赖，将外推转化为隐空间的序列演化问题，并引入了隐空间加速度惩罚与3D轨迹加速度惩罚作为物理平滑先验，迫使预测的动力学行为合理且稳定。

实验表明，ODE-GS在D-NeRF、NVFi和HyperNeRF三个基准上均取得最优外推性能：相较先前最佳外推方法，PSNR平均提升21.4%，SSIM提升7.4%，LPIPS降低30.5%。消融研究进一步揭示，移除神经ODE组件后，纯自回归Transformer的PSNR骤降约9.7 dB（33.43→23.71），验证了隐式ODE是外推能力的核心使能器；解耦训练策略相比端到端联合训练在所有指标上均有显著增益。

## 背景与动机

动态3D场景的新视角合成是计算机视觉与图形学的前沿方向，其核心目标是从一组稀疏的标定多视角视频帧中重建场景的几何与外观，并支持在任意时刻、任意相机位姿下渲染逼真的图像。近年来，以神经辐射场（NeRF）和3D高斯泼溅（3D Gaussian Splatting, 3DGS）为代表的隐式与显式场景表示取得了显著进展，但在处理动态场景时，绝大多数方法聚焦于**插值**——即在训练数据覆盖的时间窗口内部，对未见时间戳进行重建。

这一范式存在根本性局限：当需要预测观测窗口之外的未来时刻时，现有方法依赖的**显式时间戳条件化机制**会遭遇严重的分布外（Out-of-Distribution, OOD）问题。具体而言，插值型动态场景表示通常以时间戳 $t$ 作为变形网络或条件化模块的输入，通过MLP预测规范空间到当前时刻的偏移量。当 $t$ 超出训练时间范围 $[t_{\min}, t_{\max}]$ 时，网络输入落入未见过区域，导致变形预测失准、渲染质量急剧退化，无法进行有效的外推。

这一瓶颈揭示了当前动态场景重建方法的一个深层缺陷：**时间建模与场景重建的耦合过紧**。插值方法将时间视为一个条件变量，而非一个需要独立推理的演化维度。这种设计在观测窗口内表现良好，但本质上缺乏对场景动力学的理解，无法将观测到的运动模式延续到未来。

针对上述缺口，ODE-GS提出了一种解耦策略：**将动态场景重建与时间预测分离**。其核心洞察在于，先训练一个时间条件化的插值模型以获取观测窗口内精确的高斯参数轨迹，再训练一个由Transformer编码、神经ODE驱动的序列到序列模型来预测未来轨迹。通过将外推问题转化为隐空间的连续演化问题，该方法**完全消除了对显式时间戳的依赖**，并借助隐空间加速度惩罚和3D轨迹加速度惩罚等物理平滑先验，迫使预测的动力学在物理上合理且稳定。

这一思路将外推从“在未见时间戳上做条件生成”重新定义为“基于过去观测的序列预测”，从而将连续时间动力学的归纳偏置注入到3D场景表示中，为动态场景外推开辟了新的技术路径。

## 核心创新

ODE-GS的核心创新在于将动态场景的外推问题重新定义为**隐空间连续时间序列预测**，从根本上绕开了现有方法对显式时间戳条件化的依赖。这一设计由四个相互协同的“changed slots”构成，共同实现了从“插值重建”到“外推预测”的范式跃迁。

### 时间建模机制：从显式时间条件化到隐式神经ODE

现有动态3DGS/NeRF方法（如**Deformable-GS**（Yang et al., 2024）、**4D-GS**（Wu et al., 2024））的核心范式是“规范空间+时间条件化变形”：变形MLP以显式时间戳 $t$ 为输入，预测高斯参数的偏移量。这一设计在观测窗口 $[t_{\min}, t_{\max}]$ 内插值效果良好，但外推时 $t > t_{\max}$ 落入分布外（OOD），导致渲染质量急剧退化——这是本工作识别的**真实瓶颈**。

ODE-GS的**因果旋钮**在于完全移除显式时间戳依赖，转而建模高斯参数轨迹的连续时间隐动态。具体而言，外推模块 $\mathcal{E}_{\phi}$ 不再接收时间戳，而是通过Transformer编码器将过去的高斯参数序列压缩为隐状态 $z(t_0)$，再由神经ODE以MLP $f_{\theta}$ 参数化隐状态的时间导数 $\frac{dz}{dt} = f_{\theta}(z(t))$，通过DOPRI5自适应求解器进行数值积分，实现隐状态的连续演化。这一设计将外推转化为隐空间的序列演化，从根本上规避了时间戳OOD问题。

消融实验提供了**决定性证据**：移除ODESolver、改为纯自回归Transformer后，NVFi平均PSNR从33.43骤降至23.71（Table 7），降幅高达约9.7 dB，外推能力几乎完全丧失。这确证了隐式ODE是外推的核心使能器，而非Transformer的序列建模能力。

### 预测范式：从单步插值到序列到序列预测

现有方法即使尝试外推，也通常沿用时间条件化的单步预测逻辑（如**GaussianPrediction**（Zhao et al., 2024）利用超点图和图卷积网络进行离散步预测），缺乏对未来的序列级建模。ODE-GS则采用**序列到序列预测**范式：以固定长度的过去高斯参数序列为前提，通过神经ODE的连续演化，一次性预测未来多个时间步的高斯参数，构成统一的预测框架。

这一范式的关键支撑是**动态轨迹采样策略**：从冻结的插值模型生成的连续轨迹中，以不同起始时间采样前缀-后缀对，涵盖多样化的预测跨度。消融实验表明，移除动态采样后PSNR降至31.35（Table 7），验证了多样化预测跨度训练对泛化的重要性。

### 训练策略：解耦重建与外推

ODE-GS采用**先冻结插值模型、再独立训练外推模型**的分离式训练策略。插值模型（规范高斯+时间条件化变形MLP）仅在观测窗口内训练，生成精确的窗口内高斯参数轨迹；随后冻结该模型，以其输出作为外推模型的监督目标进行第二阶段训练。

这一设计的动机在于避免时间戳分布偏移对预测器的干扰。联合训练实验提供了有力的反面证据：端到端同时优化重建与外推导致D-NeRF平均PSNR从27.31降至21.79（Table 10），所有指标均显著下降。这验证了解耦设计的必要性——插值模型专注于观测窗口内的精确重建，外推模型则专注于从重建轨迹中学习动力学规律，两者职责分离、互不干扰。

### 物理约束：隐空间与3D空间的双重平滑正则化

ODE-GS引入了两个互补的平滑正则化项，为预测动力学施加物理先验：

- **隐空间正则化** $\mathcal{R}_{\mathrm{latent}}$：惩罚隐状态速度场的变化率（即加速度），抑制隐轨迹的高频振荡，数学形式为 $\mathcal{R}_{\mathrm{latent}} = \frac{1}{N_e-1} \sum_{j=1}^{N_e-1} \left\| \frac{f_\theta(z(t_{j+1})) - f_\theta(z(t_j))}{\Delta t_j} \right\|_2^2$。
- **轨迹正则化** $\mathcal{R}_{\mathrm{traj}}$：惩罚3D高斯位置的加速度，使预测的物体运动平滑，形式为 $\mathcal{R}_{\mathrm{traj}} = \frac{1}{N_e-2} \sum_{j=1}^{N_e-2} \left\| \frac{v_k(t_{j+1}) - v_k(t_j)}{\Delta t_j} \right\|_2^2$。

此外，正则化强度通过自适应因子 $s_t$ 随训练动态调整，在训练后期强化平滑约束。总损失为 $\mathcal{L} = \mathcal{L}_{\mathrm{e}} + s_t ( \lambda_{\mathrm{latent}} \mathcal{R}_{\mathrm{latent}} + \lambda_{\mathrm{traj}} \mathcal{R}_{\mathrm{traj}} )$。

消融实验量化了正则化的贡献：移除所有正则化项后，平均PSNR从33.43降至32.90（Table 8），在复杂场景（如dining）退化尤为明显；进一步禁用自适应缩放，PSNR进一步降至32.19。定性对比（Figure 4）显示，正则化对高光区域和剧烈变化区域的视觉伪影有显著抑制作用。

### 创新总结

上述四个changed slots形成了一条完整的因果链：解耦训练提供高质量的训练轨迹，序列到序列范式定义预测任务的形式，隐式ODE消除时间戳OOD并提供连续时间演化能力，双重平滑正则化约束预测的物理合理性。这一设计使得ODE-GS在D-NeRF和NVFi数据集上分别以27.30 PSNR和33.43 PSNR显著领先于先前最佳方法，PSNR提升幅度达18.6%–39.6%（Table 1, Table 2）。

## 整体框架

ODE-GS 的整体框架围绕“重建-预测解耦”这一核心设计原则构建，将动态场景外推问题分解为两个阶段：首先在观测时间窗口内获得高质量的动态场景表示，然后基于该表示进行未来时间步的连续预测。这一分离设计的动机在于：传统动态重建方法将变形网络以显式时间戳 $t$ 为输入，当外推到训练窗口之外时，时间戳落入分布外，导致渲染质量急剧下降；而解耦后，外推模型不再依赖显式时间戳，而是通过隐空间的连续演化来生成未来状态。

框架由两大核心模块串联构成，其输入输出关系如 Figure 2 所示。

**插值模型** 负责第一阶段任务：给定多视角视频的标定图像集合 $\mathcal{D} = \{ (I_i, V_i, t_i) \}_{i=1}^{N}$，在观测窗口 $[t_{\min}, t_{\max}]$ 内学习连续时间渲染算子。该模型采用规范空间加变形网络的方案：维护一组静态的规范 3D 高斯 $\overline{\mathcal{G}}$，通过一个轻量的时间条件化变形 MLP $\mathcal{D}_{\omega}(t, \overline{\mathcal{G}})$ 预测每个时刻的位置、旋转和尺度偏移量，从而获得任意时刻 $t$ 的高斯参数 $\mathcal{G}(t) = \overline{\mathcal{G}} + \mathcal{D}_{\omega}(t, \overline{\mathcal{G}})$。训练完成后，该模型被冻结，其唯一作用是生成观测窗口内的高斯参数连续轨迹，为外推模型提供监督信号。

**外推模型** 构成第二阶段的核心，是一个 Transformer 隐式神经 ODE 序列到序列预测器。其工作流程分为四步：

1. **轨迹采样**：从冻结的插值模型产生的连续轨迹中，通过动态轨迹采样策略，以不同起始时间截取“前缀-后缀”训练对。前缀为观测到的过去高斯参数序列，后缀为目标未来序列，覆盖多样化的预测跨度以增强泛化能力。

2. **Transformer 编码**：前缀序列经位置编码后送入 Transformer 编码器，压缩为总结过去动态的隐状态 $z(t_0)$。此步骤将变长的时间序列信息聚合为固定维度的表示，消除了对显式时间戳的依赖。

3. **隐式 ODE 演化**：以 $z(t_0)$ 为初值，由 MLP 参数化的神经 ODE $\frac{dz}{dt} = f_{\theta}(z(t))$ 定义隐状态的连续时间导数，通过 DOPRI5 自适应求解器进行数值积分，得到未来各时刻的隐状态 $z(t_j)$。这一连续动力学建模赋予了外推过程内在的时间连续性和平滑性。

4. **解码与渲染**：将演化后的隐状态经解码器映射回高斯参数（位置、旋转、尺度），再通过可微分光栅化进行 alpha 合成渲染，生成未来视角的图像。

整个连续时间渲染算子可统一表示为：

$$
\mathcal{F}(t, V) = \mathcal{R}(\mathcal{G}(t), V), \quad \mathcal{G}(t) = \begin{cases} \overline{\mathcal{G}} + \mathcal{D}_{\omega}(t, \overline{\mathcal{G}}) & \text{if } t_{\min} \leq t \leq t_{\max}, \\ \mathcal{E}_{\phi}(\gamma, t) & \text{if } t > t_{\max} \end{cases}
$$

其中 $\mathcal{R}$ 为可微分光栅化算子，在观测窗口内走插值分支，在窗口外走外推分支，两者共享同一渲染后端但时间建模机制完全独立。

**训练策略**上，框架严格遵循解耦原则：先独立训练插值模型至收敛并冻结，再以其生成的轨迹为目标训练外推模型。消融实验（Table 10）表明，联合训练插值模型与外推模型会导致所有指标显著下降（D-NeRF 平均 PSNR 从 27.31 降至 21.79），验证了解耦设计对避免时间戳分布偏移干扰的关键作用。

**物理约束**方面，框架引入了双重平滑正则化：隐空间加速度惩罚 $\mathcal{R}_{\mathrm{latent}}$ 抑制隐状态速度场的高频振荡，3D 轨迹加速度惩罚 $\mathcal{R}_{\mathrm{traj}}$ 约束高斯位置的运动平滑性。两者通过自适应缩放因子 $s_t$ 调制，随训练进程逐步增强正则化强度，迫使预测动力学物理合理且稳定。最终训练损失为：

$$
\mathcal{L} = \mathcal{L}_{\mathrm{e}} + s_t \big( \lambda_{\mathrm{latent}} \mathcal{R}_{\mathrm{latent}} + \lambda_{\mathrm{traj}} \mathcal{R}_{\mathrm{traj}} \big)
$$

其中 $\mathcal{L}_{\mathrm{e}}$ 为预测高斯参数与目标参数之间的 L1 损失。消融实验（Table 8）显示，去除所有正则化项后平均 PSNR 降至 32.90，进一步禁用自适应缩放则降至 32.19，证实了平滑约束及其动态调节对预测质量的重要贡献。

## 核心模块与公式推导

### 3.1 问题形式化与渲染算子分解

给定一组动态场景的标定RGB图像 $\mathcal{D} = \{ (I_i, V_i, t_i) \}_{i=1}^{N}$，其中 $I_i \in \mathbb{R}^{3 \times H \times W}$ 为图像，$V_i \in SE(3)$ 为相机外参，$t_i \in \mathbb{R}$ 为时间戳，ODE-GS 的目标是学习一个连续时间渲染算子 $\mathcal{F}(t, V)$，使其能够在观测窗口 $[t_{\min}, t_{\max}]$ 之外的外推区间上生成高质量新视角图像。

该渲染算子被分解为两个分支，分别对应插值与外推（Equation (2)）：

$$
\mathcal{F}(t, V) = \mathcal{R}(\mathcal{G}(t), V), \quad
\mathcal{G}(t) = \begin{cases}
\overline{\mathcal{G}} + \mathcal{D}_{\omega}(t, \overline{\mathcal{G}}) & \text{if } t_{\min} \leq t \leq t_{\max}, \\
\mathcal{E}_{\phi}(\gamma, t) & \text{if } t > t_{\max}
\end{cases}
$$

其中：$\mathcal{R}$ 为可微分光栅化算子；$\mathcal{G}(t)$ 为时刻 $t$ 的3D高斯参数集合；$\overline{\mathcal{G}}$ 为规范空间中的静态3D高斯；$\mathcal{D}_{\omega}$ 是以时间 $t$ 为条件、参数为 $\omega$ 的变形MLP，负责在观测窗口内插值；$\mathcal{E}_{\phi}$ 为参数 $\phi$ 的外推模块，接收过去的高斯参数轨迹前缀 $\gamma$，预测未来时刻的高斯参数。该分解是后续解耦训练策略的理论基础。

可微分光栅化采用标准的Alpha合成公式，对像素 $p$ 处的颜色 $C(p)$ 进行混合：

$$
C(p) = \sum_{k \in G(p)} c_k \alpha_k \prod_{j=1}^{k-1} (1 - \alpha_j)
$$

其中 $G(p)$ 为投影到像素 $p$ 的有序高斯集合，$c_k$ 和 $\alpha_k$ 分别为第 $k$ 个高斯的颜色与透明度。

### 3.2 插值模型

插值模型采用“规范空间+时间条件变形”的经典范式。一组规范3D高斯 $\overline{\mathcal{G}}$ 表示场景的静态参考构型，轻量级时间条件变形MLP $\mathcal{D}_{\omega}$ 以时间戳 $t$ 为输入，预测每个高斯的位置偏移 $\Delta \mu$、旋转偏移 $\Delta q$ 和尺度偏移 $\Delta s$。训练目标为光度重建损失，结合L1范数与SSIM（Equation (4)）：

$$
\mathcal{L}_{\mathrm{render}} = (1 - \lambda) \cdot \| \widehat{I_i} - I_i \|_1 + \lambda \cdot (1 - \mathrm{SSIM}(\widehat{I_i}, I_i))
$$

插值模型训练完成后被冻结，其唯一作用是生成观测窗口内任意时刻的高斯参数轨迹，为外推模型提供监督目标。这一冻结策略避免了外推训练过程中时间戳分布偏移对插值模型的干扰。

### 3.3 外推模块：Transformer Latent ODE

外推模块 $\mathcal{E}_{\phi}$ 是一个序列到序列的Transformer Latent ODE，其核心设计在于完全移除显式时间戳依赖，将外推转化为隐空间的连续演化问题。该模块由三个子组件构成：

**Transformer编码器**：接收过去 $N_p$ 个时间步的高斯参数序列，每个时间步的参数经过位置编码后输入Transformer编码器，输出总结过去动态的隐状态 $z(t_0)$。

**神经ODE**：以隐状态 $z(t_0)$ 为初值，通过一个MLP $f_\theta$ 参数化隐状态的时间导数 $\frac{dz}{dt} = f_\theta(z(t))$，采用DOPRI5自适应步长求解器进行数值积分，得到未来任意时刻的隐状态 $z(t_j)$。这一连续时间演化机制使得模型不再依赖显式时间戳输入，从根本上规避了外推时的分布外（OOD）问题。

**解码器**：将演化后的隐状态映射回高斯参数空间（位置 $\mu$、旋转 $q$、尺度 $s$），供后续可微分光栅化渲染使用。

### 3.4 动态轨迹采样

为增强外推模型对不同预测跨度的鲁棒性，ODE-GS 引入动态轨迹采样策略。具体而言，从冻结的插值模型产生的连续高斯参数轨迹中，以随机起始时间采样长度为 $N_p + N_e$ 的片段，其中前 $N_p$ 步作为编码器输入前缀，后 $N_e$ 步作为外推目标。这一策略使得模型在训练期间接触到多样化的预测起始点和预测长度，提升了泛化能力。消融实验表明，移除动态采样后NVFi平均PSNR从33.43降至31.35（Table 7）。

### 3.5 平滑正则化

ODE-GS 引入两类物理启发的平滑正则化，约束预测动力学的合理性：

**隐空间正则化**（Equation (6)）：惩罚神经ODE速度场的变化率，抑制隐轨迹的高频振荡：

$$
\mathcal{R}_{\mathrm{latent}} = \frac{1}{N_e-1} \sum_{j=1}^{N_e-1} \left\| \frac{f_\theta(z(t_{j+1})) - f_\theta(z(t_j))}{\Delta t_j} \right\|_2^2
$$

**轨迹正则化**（Equation (7)）：惩罚3D高斯位置的加速度，迫使物体运动平滑：

$$
\mathcal{R}_{\mathrm{traj}} = \frac{1}{N_e-2} \sum_{j=1}^{N_e-2} \left\| \frac{v_k(t_{j+1}) - v_k(t_j)}{\Delta t_j} \right\|_2^2
$$

其中 $v_k(t_j)$ 为第 $k$ 个高斯在时刻 $t_j$ 的速度（通过位置差分近似）。

**自适应正则化缩放**：两项正则化通过自适应因子 $s_t$ 调制，该因子基于外推损失的指数移动平均（EMA）计算，随训练进程逐渐增大正则化强度。最终训练损失为（Equation (9)）：

$$
\mathcal{L} = \mathcal{L}_{\mathrm{e}} + s_t \big( \lambda_{\mathrm{latent}} \mathcal{R}_{\mathrm{latent}} + \lambda_{\mathrm{traj}} \mathcal{R}_{\mathrm{traj}} \big)
$$

其中外推损失 $\mathcal{L}_{\mathrm{e}}$ 为预测高斯参数与插值模型生成的目标参数之间的L1误差（Equation (5)）：

$$
\mathcal{L}_{\mathrm{e}} = \frac{1}{N_e} \sum_{j=1}^{N_e} \big\| \hat{G}_k(t_j) - G_k(t_j) \big\|_1
$$

消融实验证实，移除所有正则化项导致NVFi平均PSNR降至32.90，进一步禁用自适应缩放则降至32.19，验证了平滑先验及其动态调制对外推质量的关键作用（Table 8）。

### 补充图表

![[assets/figures/papers/paper_list_l7_https_openreview_net_forum_id_XlRbpFj3lJ/figures/002_Figure_2.jpg]]
*Figure 2: 1: We initialize temporal trajectories of 3D Gaussian parameters using the frozen interpolation model, which consists of the canonical 3D Gaussian set and a time-conditioned deformation MLP. These trajectories lie entirely within the observed temporal window. 2: Through our dynamic sampling strategy, each Gaussian trajectory is sampled into multiple observed prefix (input) and a held-out suffix (target) trajectories, providing training pairs for the Transformer latent ODE. 3: Latent-ODE training encodes the observed prefix with a Transformer, infers a latent initial state, and evolves it forward with a neural ODE. 4: A decoder maps the latent path back to Gaussian parameters, which are supe...*

## 实验与分析

### 核心实验设置

ODE-GS 在三个涵盖不同动力学复杂度的公开数据集上进行评估：**D-NeRF**（合成物体运动）、**NVFi**（真实室内场景与旋转物体）和 **HyperNeRF**（含拓扑变化与噪声的真实场景）。所有基线方法均使用与 ODE-GS 相同的数据集分割（D-NeRF: 80%训练/20%测试；NVFi: 75%/25%；HyperNeRF: 90%/10%），确保对比公平。外推评估时，ODE-GS 仅使用观测窗口内的数据训练，在完全不可见的未来时间窗口上测试，无信息泄露。

评估指标采用 PSNR、SSIM 和 LPIPS（VGG），覆盖重建保真度、结构相似性和感知质量三个维度。对比基线分为两类：**插值型方法**（TiNeuVox-B、4D-GS、Deformable-GS、4D-Rotor-Gaussians）和**外推型方法**（GaussianPrediction、NVFi）。

### 主要定量结果

#### D-NeRF 数据集（Table 1）

![[assets/figures/papers/paper_list_l7_https_openreview_net_forum_id_XlRbpFj3lJ/figures/003_Table_1.jpg]]
*Table 1: Quantitative extrapolation results on D-NeRF dataset. Metrics reported include PSNR, SSIM, and LPIPS-vgg. Best metric is highlighted in red, and second best in orange*

ODE-GS 在 D-NeRF 上平均取得 **27.30 PSNR / 0.9497 SSIM / 0.0467 LPIPS**，全面超越所有基线。相较于外推基线 GaussianPrediction 的平均 23.09 PSNR，PSNR 提升 **18.6%**，SSIM 提升 10.6%，LPIPS 降低 71.9%。插值型方法（如 Deformable-GS）因依赖显式时间戳条件化，在外推时渲染质量急剧退化，PSNR 普遍低于 20 dB。ODE-GS 在 Lego 场景上取得最佳 PSNR（25.74）和 SSIM（0.9378），在 bouncingballs 等快速运动场景上优势尤为显著。

#### NVFi 数据集（Table 2）

![[assets/figures/papers/paper_list_l7_https_openreview_net_forum_id_XlRbpFj3lJ/figures/004_Table_2.jpg]]
*Table 2: Quantitative extrapolation results on NVFi dataset scenes. Metrics reported include PSNR, SSIM, and LPIPS. The best metric is highlighted in red, second-best is highlighted in orange*

在 NVFi 上，ODE-GS 平均 **33.43 PSNR / 0.9471 SSIM / 0.0603 LPIPS**，相比 NVFi 基线的 28.45 PSNR 提升 17.5%，LPIPS 降低 41.1%；相对于 GaussianPrediction 的 23.95 PSNR，提升幅度高达 **39.6%**。ODE-GS 在几乎所有序列上取得最优或次优结果，尤其在 coffee、dining 等复杂室内场景中优势明显。

#### HyperNeRF 数据集（Table 3）

![[assets/figures/papers/paper_list_l7_https_openreview_net_forum_id_XlRbpFj3lJ/figures/005_Table_3.jpg]]
*Table 3: Quantitative extrapolation results on HyperNeRF. Metrics reported include PSNR, SSIM, and LPIPS. The best metric is highlighted in bold, second-best is underlined*

在包含真实噪声和复杂动力学的 HyperNeRF 上，ODE-GS 在 split-cookie、slice-banana、cut-lemon 三个场景上取得最低 LPIPS，在 chickchicken 上取得最优 PSNR 和 SSIM，定性/定量均优于 TiNeuVox-B、4D-GS 等基线。

### 定性可视化

**Figure 3** 展示了 D-NeRF 五个场景的渲染图与残差图对比。Deformable-GS 在外推帧上产生严重的模糊和几何失真，GaussianPrediction 虽能捕捉部分运动趋势，但细节丢失明显。ODE-GS 的渲染结果最接近 Ground Truth，残差图几乎无结构化误差，尤其在 bouncingballs 等高频运动场景中，球体边界清晰、颜色准确。

**Figure 6** 展示了 NVFi 数据集上的类似对比，ODE-GS 在 coffee、dining 等场景中保持了清晰的物体边界和纹理细节，而基线方法在外推后期出现明显的模糊和伪影。

### 消融实验

#### 神经 ODE 的核心作用（Table 7）

![[assets/figures/papers/paper_list_l7_https_openreview_net_forum_id_XlRbpFj3lJ/figures/012_Table_7.jpg]]
*Table 7: Per-scene ablation over NVFi of our full method against removal of ODE and removal of dynamic trajectory sampling. Metrics reported include PSNR, SSIM, and LPIPS*

移除 ODESolver、改用纯自回归 Transformer 后，NVFi 平均 PSNR 从 33.43 骤降至 **23.71**（下降约 9.7 dB），外推能力丧失殆尽。**Figure 17-18** 的定性对比显示，纯自回归模型在最后一帧产生严重模糊和几何崩溃，证明隐式 ODE 的连续时间演化是外推的核心使能器。

#### 动态轨迹采样的必要性（Table 7）

移除动态轨迹采样策略后，PSNR 降至 31.35，表明固定前缀-后缀对的训练方式限制了模型对多样化预测跨度的泛化能力。动态采样通过从连续轨迹中以不同起始时间抽取训练对，显著增强了外推鲁棒性。

#### 正则化的贡献（Table 8, Figure 4）

![[assets/figures/papers/paper_list_l7_https_openreview_net_forum_id_XlRbpFj3lJ/figures/008_Figure_4.jpg]]
*Figure 4: Qualitative comparison on ODE-GS trained using latent and trajectory regularization vs. using only extrapolation loss on two selected scenes. We highlight the areas within each scene with highest visual disparity*

![[assets/figures/papers/paper_list_l7_https_openreview_net_forum_id_XlRbpFj3lJ/figures/013_Table_8.jpg]]
*Table 8: Per-scene ablation over NVFi of our full method against removal of regularizers and removal of adaptive regularizer scaling. Metrics reported include PSNR, SSIM, and LPIPS*

移除所有正则化项（隐空间加速度惩罚和 3D 轨迹加速度惩罚）后，平均 PSNR 降至 32.90，在 dining 等复杂场景退化尤为明显。**Figure 4** 的定性对比显示，无正则化模型在高光区域和物体边界处产生明显伪影，而加入正则化后这些伪影得到有效抑制。

进一步禁用自适应正则化缩放因子 $s_t$ 后，平均 PSNR 进一步降至 **32.19**，验证了随训练动态调整正则化强度的必要性。自适应缩放使得模型在训练初期专注于拟合数据，在后期逐步增强平滑约束，避免过早引入强正则化导致欠拟合。

#### 解耦训练 vs. 联合训练（Table 10）

![[assets/figures/papers/paper_list_l7_https_openreview_net_forum_id_XlRbpFj3lJ/figures/015_Table_10.jpg]]
*Table 10: Comparison between per-scene (Ours) and joint training (Ours joint) on the D-NeRF dataset. Metrics reported include PSNR, SSIM, and LPIPS-vgg*

将插值模型与外推模型进行端到端联合训练（而非先冻结插值模型再独立训练外推模型）导致 D-NeRF 平均 PSNR 从 27.31 降至 **21.79**，所有指标全面下降。这一结果验证了分离设计的核心洞察：冻结的插值模型为外推提供稳定、精确的训练轨迹，避免时间戳分布偏移对预测器的干扰。

#### 确定性 vs. 变分公式（Table 6）

确定性公式在 NVFi 上全面优于变分版本，PSNR 差距高达 **10+ dB**。变分训练的不稳定性表明，在当前场景规模和动力学复杂度下，确定性流建模足以捕捉动态，而变分框架的潜在优势（不确定性量化）未能有效发挥。

#### 重投影损失的影响（Table 5）

![[assets/figures/papers/paper_list_l7_https_openreview_net_forum_id_XlRbpFj3lJ/figures/009_Table_5.jpg]]
*Table 5: The effect of additional reprojection loss during training on D-NeRF extrapolation. Metrics reported include PSNR, SSIM, and LPIPS-vgg*

额外引入重投影损失对 D-NeRF 外推的影响有限，部分场景略有提升，部分场景轻微退化，整体未带来一致的性能增益，表明直接监督高斯参数轨迹的 L1 损失已足够有效。

### 外推时间退化分析

**Figure 5** 和 **Figure 7-16** 展示了 NVFi 各场景的指标随外推时间的退化曲线。ODE-GS 在所有场景上一致优于 Deformable-GS，且退化速度明显更缓。这表明隐式 ODE 的连续时间动力学建模不仅提升了短期预测精度，还显著延长了有效外推的时间跨度。

### 多场景训练与泛化（Table 9）

在 NVFi 上进行多场景共享权重训练，并在未见的 whale 场景上测试，ODE-GS 仍优于单场景训练的 NVFi 基线，但性能低于单场景训练的 ODE-GS。这表明方法具有一定的跨场景泛化潜力，但尚未达到单场景定制训练的水平，跨场景泛化仍是开放挑战。

### 失败模式与局限性

1. **插值模型质量瓶颈**：外推性能严重依赖插值模型在观测窗口内的重建质量。**Figure 19** 显示，在 NVFi 的 fallingball 场景中，插值模型未能捕获下落球体，导致外推结果同样缺失该对象。这是解耦设计的固有局限——外推模型只能预测插值模型已建模的动态。

2. **非平滑动态建模不足**：当前物理先验仅为加速度惩罚（平滑性），对包含突然变速、碰撞或非平滑交互的场景可能不足以捕捉真实动态。bouncingballs 等场景虽表现良好，但更复杂的接触力学场景仍需验证。

3. **计算开销**：训练与推理涉及 DOPRI5 自适应 ODE 求解器的数值积分，计算开销高于前馈方法，尚未在实时应用中验证。

4. **确定性框架的不确定性缺失**：变分版本训练不稳定，确定性公式虽精度更高，但丧失了对预测不确定性的建模能力，无法量化外推的置信度。

### 补充图表

![[assets/figures/papers/paper_list_l7_https_openreview_net_forum_id_XlRbpFj3lJ/figures/006_Figure_3.jpg]]
*Figure 3: Qualitative visualization on 5 scenes from DNeRF dataset, from left to right are the ground truth image, rendered result from Deformable GS(Yang et al., 2024), residual of Deformable GS against GT, GaussianPrediction(Zhao et al., 2024), residual of GaussianPrediction against GT, and finally Our as well as Ours residual against GT*

![[assets/figures/papers/paper_list_l7_https_openreview_net_forum_id_XlRbpFj3lJ/figures/016_Figure_6.jpg]]
*Figure 6: Qualitative results on 5 scenes from the NVFI (Li et al., 2023) dataset, from left to right are the ground truth image, rendered result from Deformable GS(Yang et al., 2024), residual of Deformable GS against GT, GaussianPrediction(Zhao et al., 2024), residual of GaussianPrediction against GT, and finally Our as well as Ours residual against GT*

![[assets/figures/papers/paper_list_l7_https_openreview_net_forum_id_XlRbpFj3lJ/figures/010_Figure_5.jpg]]
*Figure 5: Visualization of the degrade in metrics through time for extrapolation. Y axis is the corresponding metric and X axis is the time or frame where the metric was evaluated. This graph is the average over all scenes in NVFi dataset*

## 方法谱系与知识库定位

### 1. 与插值型动态重建基线的关系

ODE-GS 的核心出发点是对现有动态场景重建方法在**时间外推**能力上的系统性突破。当前主流的动态 3D 高斯泼溅（3DGS）和神经辐射场（NeRF）方法——包括 **TiNeuVox-B**（Fang et al., 2022）、**4D-GS**（Wu et al., 2024）、**Deformable-GS**（Yang et al., 2024）和 **4D-Rotor-Gaussians**——均采用“规范空间 + 时间条件化变形”的范式：一个以显式时间戳 $t$ 为输入的 MLP 预测每个高斯的偏移量。这种设计在观测窗口 $[t_{\min}, t_{\max}]$ 内表现优异，能够重建未见时间戳的新视角，但其本质是**插值**——当 $t > t_{\max}$ 时，时间戳落入分布外（OOD），变形网络的行为不可控，渲染质量急剧退化。ODE-GS 将这一瓶颈诊断为“显式时间戳依赖导致的 OOD 失效”，并通过**完全移除时间戳输入**来解决：外推分支 $\mathcal{E}_{\phi}$ 不再以 $t$ 为条件，而是从过去的高斯参数序列中学习隐动态。

这一设计将 ODE-GS 与所有插值型基线从根本上区分开来。实验证据表明，在 D-NeRF 数据集上，Deformable-GS 的外推 PSNR 远低于 ODE-GS（Table 1 中 ODE-GS 平均 27.30 dB，而 Deformable-GS 等插值方法未报告外推指标或显著偏低），验证了插值范式在外推场景下的固有限制。

### 2. 与现有外推方法的对比

在专门针对外推的基线中，**GaussianPrediction**（Zhao et al., 2024）和 **NVFi**（Li et al., 2023）是两个直接对比对象。GaussianPrediction 采用超点图和图卷积网络进行离散步预测，但其仍然依赖显式时间条件化，且缺乏连续时间建模能力。NVFi 在神经体积预测中引入了几何先验，但同样受限于时间戳的 OOD 问题。ODE-GS 在 D-NeRF 上以平均 PSNR 27.30 dB 对 GaussianPrediction 的 23.09 dB 实现了 **18.6% 的提升**（Table 1）；在 NVFi 数据集上，ODE-GS 平均 PSNR 33.43 dB 对 NVFi 的 28.45 dB 实现了 **17.5% 的提升**，对 GaussianPrediction 的提升幅度更高达 **39.6%**（Table 2, Table 9）。SSIM 和 LPIPS 指标同样大幅领先，表明 ODE-GS 在结构保持和感知质量上均有显著优势。

关键的架构差异在于**预测范式**：GaussianPrediction 和 NVFi 本质上仍是时间条件化的单步预测，而 ODE-GS 采用序列到序列（seq2seq）框架——Transformer 编码器将过去固定长度的高斯参数序列压缩为隐状态 $z(t_0)$，再由神经 ODE 连续演化隐状态，解码得到未来多个时间步的参数。这一范式转换使得模型能够捕捉时间依赖结构，而非孤立地预测每一帧。

### 3. 与神经 ODE 和动态系统建模的关联

ODE-GS 的隐式神经 ODE 组件将动态场景外推纳入连续时间动力系统建模的框架。与传统的离散自回归预测不同，神经 ODE 通过 $\frac{dz}{dt} = f_\theta(z(t))$ 定义隐状态的连续演化，使用 DOPRI5 自适应求解器进行数值积分。消融实验（Table 7）提供了决定性证据：**移除 ODE 求解器、改为纯自回归 Transformer 后，NVFi 平均 PSNR 从 33.43 dB 骤降至 23.71 dB**（下降约 9.7 dB），外推能力几乎完全丧失。这证明隐式 ODE 的连续时间动力学是外推的核心使能器，而非仅仅是 Transformer 序列建模的补充。

此外，ODE-GS 引入了**双重平滑正则化**——隐空间加速度惩罚 $\mathcal{R}_{\text{latent}}$ 和 3D 轨迹加速度惩罚 $\mathcal{R}_{\text{traj}}$——将物理先验注入学习过程。消融实验（Table 8）显示，移除所有正则化项后平均 PSNR 降至 32.90 dB，在复杂场景（如 dining）中退化尤为明显；进一步禁用自适应正则化缩放 $s_t$ 后，PSNR 进一步降至 32.19 dB。这表明平滑先验和随训练动态增强的约束策略对稳定外推至关重要。

### 4. 训练策略的独特性：解耦优于联合

ODE-GS 的一个关键设计选择是**解耦训练**：先冻结插值模型生成观测窗口内的高斯参数轨迹，再独立训练外推模型。这与端到端联合优化的常见做法形成鲜明对比。Table 10 的消融实验表明，联合训练导致 D-NeRF 平均 PSNR 从 27.31 dB 降至 21.79 dB，所有指标均显著下降。这一反直觉的结果揭示了外推任务的一个深层挑战：时间戳分布偏移会通过梯度反向传播污染插值模型的训练，而解耦设计将“重建”与“预测”分离，避免了这一干扰。

### 5. 适用边界与局限

尽管 ODE-GS 在多个基准上取得了领先性能，其适用性存在以下边界：

- **插值模型依赖瓶颈**：外推性能严重依赖插值模型在观测窗口内的重建质量。若插值模型无法捕获场景中的某些动态对象（如 NVFi 的 fallingball 场景，Figure 19 显示插值模型完全丢失了下落球体），外推结果也会缺失这些对象。这意味着 ODE-GS 无法超越其“教师模型”的知识边界。

- **场景级独立训练**：当前模型需要为每个场景独立训练。Table 9 的多场景共享权重实验显示，虽然模型在未见鲸鱼场景上展现了一定的泛化能力，但尚未达到单场景训练的水平，跨场景泛化性有限。

- **平滑性假设的限制**：引入的物理先验主要为加速度惩罚，本质上是二阶平滑约束。对于包含突然变速、碰撞或非平滑交互的场景，这一先验可能不足以捕捉真实动态。变分公式（Table 6）在当前数据集上表现不佳（NVFi 上 PSNR 差距超过 10 dB），丧失了预测不确定性的建模能力，表明更灵活的概率框架仍是开放挑战。

- **计算开销**：训练与推理涉及 ODE 数值积分（DOPRI5 自适应求解器），计算开销高于简单前向网络，尚未在实时应用中验证。

### 6. 开放问题

从知识库定位的角度，ODE-GS 开启了以下研究方向：

1. **数据驱动的动态先验**：当前方法仅依赖单场景的观测轨迹和手工设计的平滑正则化。如何从大规模视频数据中学习可迁移的运动先验，使外推模型泛化到新场景，是一个自然延伸。

2. **端到端外推学习**：能否绕过预训练插值模型，直接从图像序列学习外推，减少误差累积和两阶段训练的成本？

3. **非平滑动力学建模**：对于接触、碰撞等非平滑事件，如何设计更灵活的动力学模型——例如切换系统或事件驱动的 ODE——在保持平滑性的同时捕捉突变？

4. **不确定性量化**：确定性公式在当前基准上表现优异，但丧失了预测不确定性的建模能力。如何设计适合动态 3D 场景的概率外推框架，同时保持预测精度，仍需探索。

5. **自适应求解器选择**：ODE 求解器的选择与容差对性能-效率权衡的影响是否可以在线自适应，以动态平衡渲染质量与推理速度？

## 原文 PDF

![[paperPDFs/ICLR_2026/ODE_GS_Latent_ODEs_for_Dynamic_Scene_Extrapolation_with_3D_Gaussian_Splatting_6975a66efdbb.pdf]]