---
title: "Generative Camera Dolly: Extreme Monocular Dynamic Novel View Synthesis"
type: paper
paper_level: A
venue: ECCV
year: 2024
pdf_ref: paperPDFs/ECCV_2024/Generative_Camera_Dolly_Extreme_Monocular_Dynamic_Novel_View_Synthesis.pdf
aliases:
- GGCD
- GCDEMDNVS
tags:
- ECCV_2024
- topic/vision_multimodal_applications
- topic/generative_models_diffusion
- topic/generative_models_diffusion/diffusion_image_video
core_operator: 通过微调节用于摄像机姿态变换的预训练视频扩散模型（Stable Video Diffusion），并设计缓慢插值的相机轨迹，使模型能够在保留强大生成先验的同时处理大幅度视角变化。
primary_logic: 将单目动态新视角合成建模为端到端的视频到视频翻译任务，利用预训练潜在扩散模型的生成先验，并通过相对摄像机外参矩阵作为微条件（micro‑conditioning）控制合成视角。
claims:
- GCD 是一个可控的单目动态视角合成流程，利用大规模扩散先验，无需深度或显式 3D 几何。
- 在 Kubric‑4D 上，GCD 显著优于所有基线，PSNR 达到 20.30，比最强的 ZeroNVS 提高 4.62 dB。
- 缓慢（gradual）相机轨迹比直接跳转（direct）平均提高 1.17 dB PSNR；从 SVD 预训练权重微调比从随机初始化训练提高 1.34 dB。
- 仅使用单目输入，GCD 的 SSIM 已超过每场景优化方法 HexPlane 使用 16 个视角的结果。
---

# Generative Camera Dolly: Extreme Monocular Dynamic Novel View Synthesis

> [!tip] 核心洞察
> 将单目动态新视角合成建模为端到端的视频到视频翻译任务，利用预训练潜在扩散模型的生成先验，并通过相对摄像机外参矩阵作为微条件（micro‑conditioning）控制合成视角。

| 字段 | 内容 |
|------|------|
| 中文题名 | 生成式摄像机滑轨：极端单目动态新视角合成 |
| 英文题名 | Generative Camera Dolly: Extreme Monocular Dynamic Novel View Synthesis |
| 会议/期刊 | ECCV 2024 |
| Links | [paper](https://arxiv.org/abs/2405.14868) |
| Topic | #topic/vision_multimodal_applications #topic/generative_models_diffusion #topic/generative_models_diffusion/diffusion_image_video |
| Method | GCD (Generative Camera Dolly) |
| Dataset | Kubric‑4D |

> [!tip] 效果简介
> - Kubric‑4D 上，PSNR (all) ↑ 20.30 vs 15.68 (ZeroNVS) (+4.62)；SSIM (all) ↑ 0.587 vs 0.396 (ZeroNVS) (+0.191)；LPIPS (all) ↓ 0.408 vs 0.508 (ZeroNVS) (-0.100)。

## 概述

### 问题与瓶颈

从单目视频合成动态场景的新视角，是视觉理解与生成中长期存在的难题。现有方法面临一个根本性瓶颈：要么依赖多视角同步视频作为输入，要么仅能处理小角度的摄像机变化，无法在极端视角变换下保持高保真度与时空一致性。这一瓶颈限制了单目动态新视角合成在真实应用中的实用性。

### 核心思路

本文提出 **GCD（Generative Camera Dolly）**，一种可控的单目动态新视角合成流程。其核心洞察在于将问题建模为端到端的视频到视频翻译任务，并利用大规模预训练视频扩散模型的生成先验来弥补单目输入的几何歧义。GCD 无需深度图输入，也不显式建模 3D 场景几何，而是通过相对摄像机外参矩阵作为微条件（micro-conditioning），控制合成视角的变换。

### 方法定位

GCD 在现有方法谱系中占据独特位置。与每场景优化的动态新视角合成方法（如 **HexPlane**、**4D-GS**）不同，GCD 是前馈式推理，无需对每个场景重新训练。与基于单图的静态新视角合成方法（如 **ZeroNVS**）相比，GCD 显式处理动态视频输入，并支持大幅度的摄像机轨迹变化。其技术路线可概括为：以 **Stable Video Diffusion** 的预训练权重为初始化，将摄像机姿态变换嵌入到 U-Net 的微条件通道中，并通过逐帧 CLIP 嵌入与输入视频的通道拼接实现时空联合条件化。

### 主要结果

在合成基准 **Kubric-4D** 上，GCD 显著优于所有基线方法：
- **PSNR** 达到 20.30 dB，比最强的 ZeroNVS 提高 **+4.62 dB**；
- **SSIM** 达到 0.587，比 ZeroNVS 提高 **+0.191**；
- **LPIPS** 降至 0.408，比 ZeroNVS 降低 **-0.100**。

消融实验揭示了两个关键设计因素：
1. **缓慢插值的相机轨迹** 相比直接跳转，平均提升 **+1.17 dB PSNR**；
2. **从 SVD 预训练权重微调** 相比从头训练，带来 **+1.34 dB PSNR** 的提升。

值得注意的是，GCD 仅使用单目输入，其 SSIM 已超过每场景优化方法 HexPlane 使用 16 个视角的结果，展现了扩散先验在补偿视角稀疏性方面的强大能力。

### 局限与展望

尽管在合成数据上表现优异，GCD 在真实世界泛化方面仍存在明显局限：对包含人体、动物或可变形物体的视频，常产生模糊或形状错误的结果；对不熟悉的运动模式（如机器人手臂）可能发生截断或错误重建。这些失败案例指向一个开放问题：如何在不牺牲生成多样性的前提下，增强模型对对象形状与运动的时间对应关系建模。

## 背景与动机

### 问题背景：从多视角到单目的动态新视角合成

动态新视角合成（Dynamic Novel View Synthesis）旨在从有限的观测视角中恢复一个动态三维场景，并渲染出任意新视角下的视频。这一任务在自动驾驶仿真、机器人视觉、增强现实和影视制作等领域具有重要应用价值。然而，现有方法在输入条件和视角变化幅度上存在根本性限制，使得该问题远未解决。

传统方法通常依赖**多视角同步视频**作为输入。例如，每场景优化方法 **HexPlane** 和 **4D‑GS** 需要从多个标定相机同时拍摄的视频来重建四维场景表示（3D 几何 + 时间），然后从中渲染新视角。这类方法的性能随输入视角数量增加而提升，但在仅有单目视频输入时，场景重建会严重退化，产生大量伪影。另一类方法如 **DynIBaR** 通过聚合时间信息来增强动态视角合成，但其视角变化范围通常局限于小角度摄像机运动，无法处理大幅度的视点变换。

### 核心瓶颈：单目输入与极端视角变化的双重挑战

本工作的核心洞察在于识别出当前领域的**真实瓶颈**：**现有动态新视角合成方法要么依赖多视角同步视频，要么仅能处理小角度摄像机变化，无法从单目视频实现极端视角变化下的高保真合成**。这一瓶颈的根源在于，单目视频仅提供场景的单一观测轨迹，其中包含的信息在空间上高度不完整——大量场景区域在输入视频中从未可见，而动态物体的运动模式也仅从一个角度被观测。当目标视角与源视角之间的旋转角度超过数十度时，需要模型具备强大的三维场景理解和时空推理能力，以同时补全被遮挡区域的外观并保持动态一致性。

### 现有方法的缺口

在单目设置下，现有方法面临两类根本性困难：

1. **基于几何重建的方法**（如 HexPlane、4D‑GS）需要从多视角观测中优化三维表示。当仅有单目视频时，深度和几何信息严重欠约束，导致重建失败。即使使用特权信息（如真实深度图），简单的几何重投影基线（Reproject RGB‑D）也无法处理遮挡区域，因为被遮挡的像素在输入帧中根本不存在。

2. **基于生成式先验的方法**（如 **ZeroNVS**）虽然利用预训练扩散模型从单张图像合成新视角，但其设计目标是静态场景的单帧合成。直接将其逐帧应用于视频会丢失时间一致性，产生严重的闪烁伪影。此外，这些方法通常未针对大幅度视角变化进行优化。

### 本文动机：利用大规模扩散先验实现端到端视频翻译

面对上述缺口，本文提出了一种范式转变：**将单目动态新视角合成建模为端到端的视频到视频翻译任务**。核心思想是：与其显式重建三维几何再渲染，不如直接学习从输入视频到目标视角视频的映射。这一思路的关键在于利用**预训练视频扩散模型的生成先验**——大规模图像到视频模型（如 Stable Video Diffusion）已在海量数据上学习了丰富的视觉世界知识和时空一致性模式，可以作为强大的先验来补全单目观测中缺失的空间信息。

具体而言，本文通过**微调节（micro‑conditioning）**机制将摄像机控制注入预训练扩散模型：将相对摄像机外参矩阵 $(\Delta\phi, \Delta\theta, \Delta r)$ 通过 MLP 嵌入，并添加到 U‑Net 各卷积层的特征通道上，使模型在保留强大生成先验的同时，能够根据指定的摄像机变换合成新视角视频。这一设计使得模型无需深度输入，也无需显式建模三维场景几何，即可处理极端视角变化。

### 预期贡献

基于上述动机，本文提出的 **GCD（Generative Camera Dolly）** 方法旨在实现以下目标：从一段单目 RGB 视频出发，合成从任意新视角观察同一动态场景的视频，且视角变化幅度可达 90° 以上。通过在合成数据集 Kubric‑4D 和 ParallelDomain‑4D 上的系统评估，验证该方法在极端视角变化下的高保真合成能力，并探索其在真实世界场景中的泛化潜力。

## 核心创新

GCD 的核心创新在于将一个极具挑战性的几何重建问题——单目动态新视角合成——**重新建模为端到端的视频到视频翻译任务**，并借助大规模预训练视频扩散模型的生成先验来填补几何建模的缺失。这一范式转换绕开了传统方法对显式 3D 表示或深度输入的依赖，带来三个紧密耦合的关键创新点。

### 1. 摄像机姿态的微条件注入

扩散模型的核心是去噪 U-Net，如何让网络“知道”目标视角是合成的关键。GCD 将源摄像机与目标摄像机之间的**相对外参矩阵 $\Delta \mathcal{E}$** 分解为旋转分量 $\mathbf{R}_t$ 和平移分量 $\mathbf{T}_t$，通过一个轻量级 MLP $m$ 将其嵌入为特征向量，然后以**微条件（micro-conditioning）**的方式逐层叠加到 U-Net 各卷积残差块的特征通道上。这一设计使摄像机控制信号渗透到网络的每一个尺度，而非仅在输入端或瓶颈层注入，从而实现了对合成视角的精细调控。

### 2. 时空联合的视频条件化机制

与标准图像到视频扩散模型仅以第一帧作为条件不同，GCD 需要完整利用输入视频的时空信息。其条件化策略包含两个互补路径：一是对输入视频的每一帧独立提取 **CLIP 语义嵌入**，通过交叉注意力机制注入 U-Net，为网络提供逐帧的语义锚点；二是将整个输入视频 $\mathbf{x}$ 在**通道维度与去噪样本拼接**，使网络在潜空间内直接感知输入视频的时空结构。这种“语义交叉注意力 + 潜空间拼接”的双路径设计，使模型能够同时保持对场景语义的理解和对运动模式的追踪。

### 3. 预训练生成先验的迁移与适配

GCD 并非从零开始训练一个扩散模型，而是从公开的 **Stable Video Diffusion（SVD）** 图像到视频生成检查点初始化网络权重。SVD 在大规模视频数据上习得的丰富运动先验和场景生成能力，为单目视角合成提供了强大的归纳偏置。新增的摄像机嵌入模块以随机初始化开始训练，而 U-Net 主体权重则从 SVD 微调。消融实验表明，这一初始化策略相比从随机权重训练，在 Kubric‑4D 上带来了 **+1.34 dB PSNR** 的显著增益，证明了生成先验迁移对几何任务的有效性。

上述三个创新点并非孤立存在，而是形成了一条完整的因果链：**预训练先验提供了“能生成合理视频”的基础能力，时空联合条件化确保了“生成内容忠于输入”，摄像机微条件则精确控制了“从哪个角度看”**。三者协同，使 GCD 在不依赖深度图或显式 3D 几何的情况下，实现了极端视角变化下的高保真动态新视角合成。

## 整体框架

GCD 将单目动态新视角合成为一个端到端的视频到视频翻译任务。其核心映射关系为：

$$\pmb{y} = f(\pmb{x}, \Delta \mathcal{E})$$

其中 $\pmb{x}$ 为输入的单目 RGB 视频，$\Delta \mathcal{E}$ 为描述源相机与目标相机之间相对位姿的外参矩阵，$\pmb{y}$ 为从目标视角合成的输出视频。整个 pipeline 不依赖显式深度输入，也不显式建模 3D 场景几何，而是完全依靠大规模预训练扩散模型的生成先验来完成时空推理。

### 模块组成与数据流

**1. 潜在空间编码（KL‑VAE Encoder）**
输入视频的每一帧首先通过 KL‑VAE 编码器压缩到潜在空间，得到低维潜在表示。这一步骤将高维 RGB 帧映射为适合扩散模型处理的紧凑特征，显著降低计算开销。

**2. 时空条件化（Spatiotemporal U‑Net + Per‑frame CLIP Embedder）**
去噪过程在时空 U‑Net 中进行。该网络包含空间注意力块和时间注意力块，分别负责帧内细节生成和帧间时序一致性。条件信号来自两个渠道：
- **逐帧 CLIP 嵌入**：为输入视频的每一帧独立提取 CLIP 语义嵌入，通过交叉注意力机制注入 U‑Net，提供高层语义指导。
- **通道拼接**：将整个输入视频的潜在表示在通道维度与当前去噪样本拼接，使模型同时感知源视频的全部时空信息。

**3. 相机微条件（Micro‑conditioning MLP）**
相对相机外参 $\Delta \mathcal{E}$ 被分解为旋转矩阵 $\mathbf{R}_t \in SO(3)$ 和平移向量 $\mathbf{T}_t \in \mathbb{R}^3$，展平后通过一个轻量 MLP 嵌入。该嵌入与扩散时间步、FPS、运动桶值等低维元数据一同，以加法方式注入 U‑Net 各残差块的卷积层特征通道上。这种微条件设计使得相机控制信号能够渗透到网络的多个层级，实现对合成视角的精细调控。

**4. 相机轨迹插值（Camera Trajectory Interpolation）**
输出视频的相机轨迹通过源姿态 $\mathcal{P}_{src}$ 与目标姿态 $\mathcal{P}_{dst}$ 之间的插值定义：

$$\mathcal{E}_{dst,t} = \begin{cases} g(\alpha \mathcal{P}_{dst} + (1-\alpha) \mathcal{P}_{src}), & \forall t, \text{ if gradual} \\ g(\mathcal{P}_{dst}), & \forall t, \text{ if direct} \end{cases}$$

其中 $\alpha = t/(T-1)$ 为线性插值系数，$g(\cdot)$ 将姿态描述映射到 $SE(3)$ 空间。**渐近轨迹**（gradual）使虚拟相机从源视角平滑过渡到目标视角，而**直接轨迹**（direct）则让所有输出帧严格遵循目标姿态。消融实验表明，渐近轨迹相比直接跳转平均提升 1.17 dB PSNR，是处理大幅度视角变化的关键设计。

**5. 训练初始化策略**
模型权重从公开的 Stable Video Diffusion（SVD）图像到视频检查点初始化，仅随机初始化新增的相机嵌入 MLP 模块。从 SVD 预训练权重微调比从随机初始化训练带来 1.34 dB PSNR 的提升，证实了利用大规模视频生成先验对单目动态视角合成的关键作用。

**6. 推理时的分类器自由引导**
推理阶段采用分类器自由引导增强生成质量，去噪步骤为：

$$\hat{\pmb{y}}_{u-1} = w \epsilon(\hat{\pmb{y}}_u \parallel \pmb{x}, \Delta \mathcal{E}) - (w-1) \epsilon(\hat{\pmb{y}}_u)$$

其中 $w$ 为引导强度，$\epsilon(\cdot \parallel \pmb{x}, \Delta \mathcal{E})$ 为条件噪声预测，$\epsilon(\cdot)$ 为无条件预测。调整引导范围至 $[1, 1.5]$ 可获得优于默认设置的性能。

### 整体数据流总结

输入单目视频 → KL‑VAE 编码 → 潜在空间表示 → 与噪声样本通道拼接 → 逐帧 CLIP 嵌入交叉注意力 → 相机外参 MLP 微条件注入 → 时空 U‑Net 迭代去噪 → KL‑VAE 解码 → 输出多帧新视角视频。整个流程中，相机轨迹插值决定了每帧的目标外参，而 SVD 预训练权重为时空一致性提供了强大的生成先验。

### 补充图表

![[assets/figures/papers/paper_list_l14_https_arxiv_org_abs_2405_14868/figures/002_Figure_2.jpg]]
*Figure 2: Method. Our model, GCD, is an end-to-end video translation pipeline that maps an input video from any viewpoint into an output video from any other perspective, with the objective of respecting all objects and dynamics occurring within the observed dynamic scene, and faithfully reconstructing the corresponding visual details from this novel viewpoint. The relative camera extrinsics matrix ∆E guides the relationship between the two camera poses*

## 核心模块与公式推导

### 问题形式化

GCD 将单目动态新视角合成建模为端到端的视频到视频翻译任务。给定一段从任意视角拍摄的输入视频 $\pmb{x}$ 和目标相对摄像机外参矩阵 $\Delta \mathcal{E}$，模型 $f$ 直接生成目标视角下的输出视频 $\pmb{y}$：

$$ \pmb{y} = f(\pmb{x}, \Delta \mathcal{E}) \tag{1} $$

其中 $\Delta \mathcal{E}$ 描述了输出视频摄像机相对于输入视频摄像机的 6-DoF 刚体变换关系，是模型实现视角控制的唯一几何信号。该方法不依赖深度图输入，也不显式建模三维场景几何，而是完全依靠预训练扩散模型的生成先验来完成时空推理。

### 摄像机条件化模块

摄像机参数的注入是 GCD 区别于普通视频扩散模型的核心设计。相对外参矩阵 $\Delta \mathcal{E}_t \in \text{SE}(3)$ 被分解为旋转矩阵 $\pmb{R}_t \in \text{SO}(3)$ 和平移向量 $\pmb{T}_t \in \mathbb{R}^3$，展平后通过一个小型 MLP $m$ 投影为嵌入向量。该嵌入以**微条件**（micro‑conditioning）的方式被逐通道加到 U‑Net 各卷积层的特征图上，与扩散时间步、FPS、运动量等低维元数据一同注入网络。

这一设计的因果逻辑在于：预训练 SVD 模型已具备强大的视频生成先验，微条件机制以最小侵入性的方式将摄像机控制信号融入现有特征流，既保留了生成质量，又实现了精确的视角引导。消融实验证实，从 SVD 预训练权重微调比从随机初始化训练带来 **+1.34 dB PSNR** 的提升，验证了保留生成先验对任务的关键作用。

### 视频条件化策略

与原始 SVD 仅使用第一帧 CLIP 嵌入和 VAE 编码作为条件不同，GCD 采用**逐帧 CLIP 嵌入**进行交叉注意力，并将整个输入视频 $\pmb{x}$ 在通道维度与当前去噪样本拼接。这种时空联合条件化使模型能够同时感知输入视频的外观语义和运动模式，为视角变换后的视频生成提供充分的上下文约束。

### 分类器自由引导

推理阶段采用分类器自由引导（Classifier‑Free Guidance）来平衡生成质量与条件一致性。去噪步骤的更新公式为：

$$ \hat{\pmb{y}}_{u-1} = w \, \epsilon(\hat{\pmb{y}}_u \parallel \pmb{x}, \Delta \mathcal{E}) - (w-1) \, \epsilon(\hat{\pmb{y}}_u) \tag{2} $$

其中 $w$ 为引导强度，$\epsilon(\cdot)$ 为 U‑Net 预测的噪声。当 $w > 1$ 时，模型在条件预测与无条件预测之间外推，增强对输入视频和摄像机参数的依从性。实验发现将引导范围调整为 $[1, 1.5]$ 可获得优于默认设置的表现。

### 相机轨迹插值

输出视频的相机轨迹定义是 GCD 的另一关键设计选择。模型支持两种模式：

$$ \mathcal{E}_{dst,t} = \begin{cases} g(\alpha \mathcal{P}_{dst} + (1-\alpha) \mathcal{P}_{src}), & \forall t, \text{ if gradual} \\ g(\mathcal{P}_{dst}), & \forall t, \text{ if direct} \end{cases} \tag{3} $$

其中 $\mathcal{P}$ 为中间姿态描述空间（如球坐标），$g(\cdot)$ 将其映射回 $\text{SE}(3)$。**渐近轨迹**（gradual）在源与目标姿态之间进行凸组合插值，使虚拟摄像机平滑移动；**直接轨迹**（direct）则让每一帧严格遵循目标姿态。

插值系数 $\alpha$ 在 Kubric‑4D 上采用线性形式 $\alpha = t/(T-1)$，在 ParallelDomain‑4D 上采用正弦波平滑形式 $\alpha = (1 - \cos(\pi t/(T-1)))/2$。消融实验表明，渐近轨迹相比直接跳转平均提升 **+1.17 dB PSNR**，说明逐步的视角变化有助于扩散模型更好地维持时序一致性。

### 训练初始化策略

GCD 从公开的 Stable Video Diffusion 图像到视频检查点初始化所有权重，仅随机初始化新增的摄像机嵌入 MLP。这一策略使得模型在微调阶段能够快速适应新视角合成任务，同时继承 SVD 在大规模视频数据上习得的丰富运动和外观先验。相比之下，从头训练不仅收敛更慢，且最终性能显著低于微调版本，进一步印证了预训练先验对极端视角合成场景的不可替代性。

### 补充图表

![[assets/figures/papers/paper_list_l14_https_arxiv_org_abs_2405_14868/figures/016_Figure_10.jpg]]
*Figure 10: Network architecture. Our model performs diffusion in latent space [35, 52]. The input video is encoded by a KL-VAE, and then channel-concatenated with the noisy sample. At training time, the output video is estimated and supervised; at inference time, multiple denoising steps are performed. In both cases, per-frame CLIP embeddings condition the U-Net by means of cross-attention, and and other relevant pieces of information (frame rate, desired camera pose transformation, and motion value) condition the U-Net by adding their embeddings onto the feature vectors in-between convolutions*

![[assets/figures/papers/paper_list_l14_https_arxiv_org_abs_2405_14868/figures/015_Figure_9.jpg]]
*Figure 9: Spherical coordinate system. Models trained on Kubric-4D accept an azimuth*

## 实验与分析

### 核心定量结果

GCD 在 Kubric‑4D 基准上显著超越所有对比方法。在全部像素的评估中，GCD 的 PSNR 达到 **20.30 dB**，比最强的单图像新视角合成基线 ZeroNVS（15.68 dB）高出 **4.62 dB**；SSIM 达到 **0.587**（ZeroNVS 为 0.396），LPIPS 降至 **0.408**（ZeroNVS 为 0.508），完整数据见 Table 4。这一优势在可见像素与遮挡像素上均成立——遮挡区域的合成是动态新视角合成中最具挑战性的子问题，GCD 在此场景下依然保持了合理的外观一致性和时序稳定性。

![[assets/figures/papers/paper_list_l14_https_arxiv_org_abs_2405_14868/figures/008_Table_4.jpg]]
*Table 4: Baseline comparison results on Kubric-4D. We evaluate gradual dynamic view synthesis models on all 13 output frames, and with a single RGB video as input. We significantly outperform all baselines for both visible and occluded pixels. *Uses privileged information, i.e. can access the ground truth depth map from the input viewpoint*

在 ParallelDomain‑4D 的 RGB 视觉补全任务中，GCD 同样大幅领先，PSNR 达到 **23.47 dB**（Table 5），语义补全任务中 mIoU 达到 **39.0%**（Table 6）。值得注意的是，部分基线方法（如 DynIBaR）使用了真实深度图和语义类别等特权信息，而 GCD 仅依赖单目 RGB 视频输入，无需显式 3D 几何。

![[assets/figures/papers/paper_list_l14_https_arxiv_org_abs_2405_14868/figures/011_Table_5.jpg]]
*Table 5: Baseline comparison results on ParallelDomain in RGB space. We perform visual scene completion, and evaluate gradual dynamic view synthesis on all 13 output frames, and with a single RGB video as input. We significantly outperform all baselines for both visible and occluded pixels. *Uses privileged information, i.e. can access the ground truth depth map from the input viewpoint*

![[assets/figures/papers/paper_list_l14_https_arxiv_org_abs_2405_14868/figures/012_Table_6.jpg]]
*Table 6: Baseline comparison results on ParallelDomain in semantic space. We perform semantic completion of the scene, still based on a single RGB video as input. *Uses privileged information, i.e. can access the ground truth depth map and ground truth semantic category of all input pixels*

### 消融实验：设计选择的关键因果作用

消融实验围绕三个核心控制变量展开：**相机轨迹策略**（gradual vs. direct）、**预训练初始化**（从 SVD 微调 vs. 从头训练）、以及**最大旋转幅度**。所有消融均在 Kubric‑4D 和 ParallelDomain‑4D 上进行，为公平比较仅评估输出视频的最后一帧，以确保 direct 和 gradual 轨迹在空间上对齐。

**相机轨迹的平滑性至关重要。** 在 Kubric‑4D 上，gradual 轨迹相比 direct 轨迹平均带来 **+1.17 dB PSNR** 的提升（Table 1）。这一提升的因果机制在于：直接跳转到目标视角要求模型在单步生成中同时完成大幅度视角变换和时序动态建模，而 gradual 插值将视角变化分解为一系列小步增量，降低了单帧合成的难度，使扩散模型能够逐步适应视角偏移。

**预训练扩散先验是性能基石。** 从 Stable Video Diffusion 的公开图像到视频检查点微调，相比从头训练带来 **+1.34 dB PSNR** 的增益（Table 1）。这验证了核心洞察：大规模视频生成预训练所蕴含的时空推理能力，可以通过微条件（micro‑conditioning）机制迁移到受控的新视角合成任务中。最佳配置（gradual、90° 最大旋转、微调）在 Kubric‑4D 上取得 PSNR 17.88、SSIM 0.521、LPIPS 0.486。

在 ParallelDomain‑4D 上，消融结果呈现一致趋势：gradual 微调模型在 RGB 空间达到 PSNR 23.47（direct 从头训练为 22.49，Table 2），在语义空间达到 mIoU 39.0%（direct 从头训练为 31.2%，Table 3）。这进一步证实了轨迹平滑与预训练初始化在不同数据域中的鲁棒性。

![[assets/figures/papers/paper_list_l14_https_arxiv_org_abs_2405_14868/figures/006_Table_2.jpg]]
*Table 2: Ablation study results on ParallelDomain in RGB space. We perform visual scene completion, and evaluate various dynamic view synthesis models on only the last frame for fairness, similarly to*

![[assets/figures/papers/paper_list_l14_https_arxiv_org_abs_2405_14868/figures/007_Table_3.jpg]]
*Table 3: Ablation study results on ParallelDomain in semantic space. We perform semantic completion of the scene, again similarly to*

**分类器自由引导（CFG）的调节**对性能有显著影响。实验发现将引导强度范围调整至 **[1, 1.5]** 优于默认范围，同时**排除第一帧输出**进行评估可避免因该帧与条件帧过于接近而膨胀指标（Section 6.1）。

### 与每场景优化方法的对比

GCD 的一个显著优势在于**推理效率与数据效率**。与需要多视角输入并进行每场景优化的方法（如 HexPlane、4D‑GS）不同，GCD 仅需单目视频即可前向推理。Fig. 7 的对比研究显示：GCD 使用单视角输入的 SSIM 已**超过 HexPlane 使用 16 个视角进行每场景优化后的结果**。这一发现揭示了大规模生成先验在补偿显式几何建模缺失方面的潜力。

![[assets/figures/papers/paper_list_l14_https_arxiv_org_abs_2405_14868/figures/013_Figure_7.jpg]]
*Figure 7: Comparative study over number of views. We plot the SSIM over the test set as a function of the number of input views that HexPlane uses for training. The numbers are averaged over 20 scenes*

### 旋转幅度的影响分析

Fig. 8 展示了在 Kubric‑4D 上不同相机旋转幅度下的性能变化。分析表明，动态视角合成的主要难度集中在**前约 80° 的旋转范围内**；超过此范围后，性能下降趋于平缓。这为理解任务的困难边界提供了定量依据，也解释了为何 gradual 轨迹策略（将大幅度旋转分解为小步增量）能有效降低合成难度。

![[assets/figures/papers/paper_list_l14_https_arxiv_org_abs_2405_14868/figures/014_Figure_8.jpg]]
*Figure 8: Comparative study over camera rotation magnitude in Kubric-4D. Note that PSNR is measured at the last output frame, because only then the desired horizontal azimuth angle has been reached. We conclude that the main difficulty in performing dynamic view synthesis comes from handling roughly the first 80 degrees, after which the performance stays mostly flat*

### 失败模式与局限性

尽管 GCD 在受控场景中表现优异，但在真实世界泛化中暴露出若干系统性失败模式（Fig. 11）：

![[assets/figures/papers/paper_list_l14_https_arxiv_org_abs_2405_14868/figures/017_Figure_11.jpg]]
*Figure 11: Failure cases. We show inputs and predictions of real-world examples. Since deformable objects are not present in our Kubric-4D finetuning set, our model occasionally struggles with reconstructing their shape, appearance, and motion correctly. This can sometimes lead to objects becoming vague or blending in with each other. Similarly, videos in the bottom two rows are possibly related to them bordering on being out-of-distribution with respect to ParallelDomain-4D*

1. **可变形物体处理失败**：由于微调数据集 Kubric‑4D 仅包含刚性物体，模型在遇到人体、动物等可变形对象时产生模糊、形状错误或外观不一致的结果。
2. **分布外类别**：不熟悉的运动模式（如机器人手臂）可能被截断或错误重建。
3. **场景理解不足**：当模型无法准确推断摄像机初始姿态时，合成视角可能出现不期望的视点偏移。
4. **高动态场景中的小物体**：交通场景中远处的行人、复杂道路结构（如立交桥）重建质量不佳。
5. **刚性物体形变**：偶尔出现刚性物体的非物理形变，对象间对应关系模糊。

这些失败模式指向了当前方法的根本局限：模型依赖数据驱动的外观和运动先验，而非显式的物理或几何理解。在显著分布外场景下，生成先验可能产生看似合理但物理不一致的合成结果。

### 公平性说明

实验设计包含多项公平性保障措施：基线对比中排除第一帧以消除条件帧邻近效应；对 ZeroNVS 逐视频手动调整尺度参数以确保视觉对齐；概率性方法（GCD、Vanilla SVD、ZeroNVS）生成 4 个样本取平均，确定性方法仅运行一次；Vanilla SVD 以其原生分辨率 1024×576 评估并居中裁剪/缩放，而 GCD 推理分辨率为 384×256。这些措施确保了定量比较的可靠性。

### 补充图表

![[assets/figures/papers/paper_list_l14_https_arxiv_org_abs_2405_14868/figures/005_Table_1.jpg]]
*Table 1: Ablation study results on Kubric. We evaluate various versions of our dynamic view synthesis model on only the last frame for fairness, i.e. to ensure that the direct and gradual trajectory models are spatially aligned. See Figure 3 for qualitative illustrations*

## 方法谱系与知识库定位

### 1. 与现有工作的关系

GCD 处于单目动态新视角合成这一新兴任务的交叉点上，其设计同时触及动态场景表示、单图像新视角合成和视频生成三条技术谱系。

**相对于动态场景表示方法。** 传统动态新视角合成方法，如 **HexPlane** 和 **4D-GS**，属于每场景优化（per‑scene optimization）范式：它们需要目标场景的多个同步视角视频作为输入，通过显式或隐式的 4D 表示（如时空分解张量或动态高斯点云）重建场景几何与外观，再从中渲染新视角。这类方法的核心瓶颈在于对多视角同步采集的强依赖——在真实世界中获取此类数据成本极高，且每遇到新场景都需重新训练。GCD 将问题重新定义为端到端的视频到视频翻译，仅需单目视频作为输入，无需显式建模 3D 几何，从根本上规避了多视角采集和逐场景优化的限制。在 Kubric‑4D 上，GCD 仅使用单目输入即取得了超过 HexPlane 使用 16 个视角进行逐场景优化时的 SSIM（见 Fig. 7），这一对比直接量化了从“多视角重建”到“单目生成”范式转换的有效性。

**相对于单图像新视角合成方法。** **ZeroNVS** 是单图像新视角合成领域的代表性工作，其通过在大规模数据上训练扩散模型实现零样本视角变换。将 ZeroNVS 逐帧应用于视频是处理动态场景最直接的基线策略。然而，这种逐帧独立处理的方式完全忽略了帧间的时间一致性，导致生成视频中出现严重的闪烁伪影（flickering artefacts）。GCD 在架构层面通过时空联合条件化——将整个输入视频在通道维度与去噪样本拼接，并通过逐帧 CLIP 嵌入进行交叉注意力——显式建模了时间维度上的信息流动。在 Kubric‑4D 上，GCD 的 PSNR 达到 20.30，比 ZeroNVS 的 15.68 提高了 4.62 dB（Table 4），这一显著差距主要来源于时间一致性的根本改善。

**相对于视频生成方法。** GCD 的权重初始化自 **Stable Video Diffusion (SVD)**，这是一个在大规模视频数据上预训练的图像到视频扩散模型。Vanilla SVD 本身不具备摄像机视角控制能力——它仅通过微条件（micro‑conditioning）接收帧率和运动幅度等元数据，无法指定目标视角。GCD 在 SVD 的基础上新增了摄像机条件化模块：将相对外参矩阵 $\Delta \mathcal{E}$（分解为旋转矩阵 $\mathbf{R}_t \in SO(3)$ 和平移向量 $\mathbf{T}_t \in \mathbb{R}^3$）通过 MLP 嵌入，并以微条件方式注入 U‑Net 各卷积层的特征通道。这一设计使模型在保留 SVD 强大生成先验的同时，获得了对输出视角的精确控制。消融实验表明，从 SVD 预训练权重微调比从随机初始化训练平均提高 1.34 dB PSNR（Table 1），验证了大规模视频先验对单目动态视角合成的关键支撑作用。

**相对于时间聚合方法。** **DynIBaR** 通过聚合多帧的时间信息来改善动态场景的渲染质量，但其本质上仍依赖于多视角输入和显式几何建模。GCD 通过扩散模型的迭代去噪过程隐式地实现了时空信息的融合，无需显式的光流估计或深度推理。

### 2. 适用边界

GCD 的有效性受到训练数据分布和模型设计选择的双重约束。

**数据分布边界。** 模型在 Kubric‑4D 合成数据集上微调，该数据集中的动态场景主要由刚性物体（如几何体、车辆）的平移和旋转运动构成，不包含人体、动物或可变形物体的运动模式。因此，当面对包含行人的交通场景或机器人操作场景时，模型经常产生模糊、形状错误或外观不一致的结果（见 Fig. 11 的失败案例）。对于不熟悉的物体类别（如机器人手臂），模型可能将其截断或错误重建。这一边界本质上是训练数据多样性的函数，而非方法本身的根本限制。

**视角变化幅度边界。** 在 Kubric‑4D 上的对比研究表明，动态视角合成的主要困难集中在视角旋转的前约 80° 范围内（Fig. 8）。超过此范围后，性能趋于平稳，说明模型在极端视角变化下已触及当前架构的表达能力上限。GCD 在训练时限制最大相对旋转角度为 90°，在此范围内表现最佳。

**场景复杂度边界。** 对于高动态交通场景中的远处小物体（如行人）以及复杂道路结构（如立交桥），模型的重建效果不佳。这反映了当前架构在同时处理大范围空间推理和细粒度物体保持方面的能力瓶颈。

**轨迹设计约束。** 缓慢（gradual）插值的相机轨迹比直接跳转（direct）平均提高 1.17 dB PSNR（Table 1），说明模型需要中间帧的渐进式引导来维持时空一致性。当目标视角与源视角差异极大时，直接跳转策略会导致生成质量显著下降，这表明扩散模型的去噪过程需要平滑的潜在空间路径。

### 3. 局限与开放问题

**对象级时间对应关系薄弱。** 模型偶尔出现刚性物体形变，源视频与生成视频中对象间的对应关系不够清晰。这是当前端到端生成范式共有的问题——缺乏显式的对象实例跟踪机制，使得模型难以在视角变换过程中严格保持每个物体的独立身份和形状。如何在不引入显式 3D 建模的前提下增强对象级时间对应关系，是一个值得探索的方向。

**可变形物体的泛化失败。** 由于训练数据中缺乏可变形物体的运动模式，模型在包含人体、动物等场景中表现不佳。这一局限指向一个更根本的问题：当前的数据生成管线（基于 Kubric 的合成渲染）难以高效地产生包含复杂非刚性运动的大规模训练数据。扩展数据管线的覆盖范围，或探索从真实世界视频中自监督学习的策略，是突破此边界的关键。

**分布外场景的脆弱性。** 模型对不熟悉相机初始姿态的解读可能出错，导致合成视角与预期不符。这表明摄像机条件化模块的泛化能力仍有提升空间——当前的 MLP 嵌入可能过度拟合了训练数据中相机姿态的分布模式。

**分辨率与时长限制。** 当前模型推理分辨率为 384×256，输出 14 帧视频。如何将框架扩展至更高分辨率和更长时序，同时保持生成质量与计算效率的平衡，是走向实际应用必须解决的问题。

**显式几何的潜在增益。** GCD 刻意避免了显式 3D 几何建模，这既是其简洁性的来源，也是其局限性的根源。是否可能在保留扩散先验优势的前提下，引入轻量级的显式几何表示（如单目深度估计或稀疏点云）以提高合成精度和时空一致性，是一个开放的架构设计问题。

## 原文 PDF

![[paperPDFs/ECCV_2024/Generative_Camera_Dolly_Extreme_Monocular_Dynamic_Novel_View_Synthesis.pdf]]