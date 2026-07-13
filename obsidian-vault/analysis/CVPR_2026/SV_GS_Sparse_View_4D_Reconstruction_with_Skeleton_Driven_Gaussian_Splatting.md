---
title: "SV-GS: Sparse View 4D Reconstruction with Skeleton-Driven Gaussian Splatting"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/SV_GS_Sparse_View_4D_Reconstruction_with_Skeleton_Driven_Gaussian_Splatting.pdf
project_link: null
code_link: null
aliases:
- SG
- SV-GS
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
core_operator: 引入粗糙的骨骼图作为结构先验，仅让关节姿态估计依赖时间，驱动高斯原语变形，从而仅靠稀疏的时间监督即可恢复出连续的关节运动。
primary_logic: 将变形场分解为时间依赖的关节姿态预测和与时间无关的皮肤校正、细节变形，粗运动由骨骼驱动，细粒度变形由细节场补充，在稀疏监督下实现了平滑的运动插值。
claims:
- SV-GS 在 D-NeRF 数据集上以 PSNR 27.75 显著优于最佳基线 RigGS† 的 23.48，提升超过 18%。
- 定性结果显示，基线方法在稀疏观察下产生噪声变形并丢失结构，而 SV-GS 能保持物体结构。
- 只有关节姿态估计器依赖于时间，使得在未见中间时间步骤可以实现平滑运动插值。
- 在真实世界 ZJU-MoCap 数据集上，使用比全序列少 10 倍的帧数，SV-GS 达到了与全序列方法相当的 SSIM 0.934。
---

# SV-GS: Sparse View 4D Reconstruction with Skeleton-Driven Gaussian Splatting

> [!tip] 核心洞察
> 将变形场分解为时间依赖的关节姿态预测和与时间无关的皮肤校正、细节变形，粗运动由骨骼驱动，细粒度变形由细节场补充，在稀疏监督下实现了平滑的运动插值。

| 字段 | 内容 |
|------|------|
| 中文题名 | SV-GS：基于骨骼驱动高斯泼溅的稀疏视角4D重建 |
| 英文题名 | SV-GS: Sparse View 4D Reconstruction with Skeleton-Driven Gaussian Splatting |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2601.00285) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction |
| Method | SV-GS |
| Dataset | D-NeRF（稀疏 0.1 间隔）, D-NeRF, DG-Mesh（0.05 间隔）, DG-Mesh（0.1 间隔） |

> [!tip] 效果简介
> - D-NeRF（稀疏 0.1 间隔） 上，PSNR↑ 27.75 vs 23.48（RigGS†） (+4.27（+18.2%）)。
> - D-NeRF 上，SSIM↑ 0.950 vs 0.893（RigGS†） (+0.057（+6.4%）)；LPIPS (×100)↓ 5.79 vs 9.43（RigGS†） (-3.64（-38.6%）)。
> - DG-Mesh（0.05 间隔） 上，SSIM↑ 0.929 vs 0.824（RigGS†） (+0.105（+12.7%）)。

## 概要

**核心问题**：现有的动态场景（4D）重建方法，无论是多视角视频、单目视频还是生成式方法，大多依赖密集的时间采样和视角覆盖。当观察变得稀疏、时间步长间隔大且视角剧烈变化时，这些方法无法建立可靠的时间对应关系，导致重建质量严重下降——产生噪声变形并丢失物体结构。

**SV-GS 的核心思路**：本文提出 SV-GS，一种骨骼驱动的高斯泼溅方法，专门针对稀疏视角下的 4D 重建。其关键洞察在于：引入粗糙的骨骼图作为结构先验，仅让关节姿态估计依赖于时间，而皮肤校正场和细节变形场均与时间无关，从而在稀疏时间监督下即可恢复出连续的关节运动，实现平滑的运动插值。

**方法定位**：SV-GS 的输入配置与现有方法有本质区别（Figure 2）：它仅需每个时间步的一张任意视角 RGB 图像（帧数可少至全序列的 1/20），外加第一帧的骨骼图和初始静态 3D 重建。变形场被分解为三个层次——时间依赖的关节姿态估计器（$MLP_\Theta$）、与时间无关的皮肤校正场（$MLP_\Phi$）和细节变形场（$MLP_\Psi$），粗运动由骨骼驱动，细粒度变形由细节场补充。

**主要结果**：
- 在 D-NeRF 数据集上，以 0.1 间隔下采样（每序列仅 11 帧），SV-GS 达到 PSNR **27.75**，显著优于最佳基线 RigGS† 的 23.48，提升超过 18%（Table 1）。
- 在 DG-Mesh 数据集上，SSIM 从 RigGS† 的 0.786 提升至 **0.900**（0.1 间隔），提升 14.5%（Table 2）。
- 在真实世界 ZJU-MoCap 数据集上，仅使用全序列 10% 的帧数，SV-GS 达到 SSIM **0.934**，与使用全序列训练的 RigGS（0.975）接近（Table 3）。

**方法谱系与知识库定位**：SV-GS 处于动态场景重建、骨骼驱动变形和高斯泼溅的交汇点。与 **4DGS**（Wu et al., CVPR 2024）基于多分辨率六平面建模变形场不同，SV-GS 显式利用骨骼结构先验；与 **SK-GS**（Wan et al., NeurIPS 2024）从单目视频自动提取骨骼不同，SV-GS 接受外部给定的骨骼图作为输入，专注于稀疏视角场景；与 **RigGS**（Yao et al., CVPR 2025）利用稀疏控制点估计骨架不同，SV-GS 将变形场的时间依赖性严格限制在关节姿态估计器上，从而在稀疏监督下实现更强的泛化。

**局限与开放问题**：扩散先验初始化在严重自遮挡下可能产生不完整几何；方法依赖初始骨骼图的提供，骨骼噪声会影响变形质量；对于非关节物体或缺乏明显骨骼结构的动态目标不适用。未来方向包括：利用类别特定先验（如人体/动物模型）进一步提升精度、从稀疏图像中自动估计骨骼图、结合预训练视频扩散模型增强运动插值的真实感。

### 问题背景：从密集观察到稀疏视角的4D重建

动态场景的4D重建——即在时间维度上恢复物体的完整3D几何与外观——是计算机视觉和图形学中的核心问题，其应用涵盖AR/VR、电影制作和数字孪生等领域。传统方法通常依赖密集的多视角视频或单目长序列，假设相邻帧之间具有较小的视角变化和丰富的时间对应信息。然而，在真实场景中，我们往往只能获得**稀疏的时间观察**：每个时间步可能仅有一张从任意视角拍摄的图像，且相邻帧之间的视角差异可能极大。这种“稀疏视角+大视角变化”的配置使得建立可靠的时间对应关系变得极其困难，现有方法在此条件下重建质量严重下降。

### 现有方法的缺口

当前的动态场景重建方法可以大致分为以下几类，但它们在稀疏观察条件下均存在显著局限：

- **多视角方法**（如 **4DGS**，Wu et al., CVPR 2024）：假设每个时间步都有密集的多视角覆盖，通过多分辨率六平面建模变形场。当每个时间步仅有一张图像时，这类方法无法建立跨视角的对应，导致变形估计失败。

- **单目视频方法**（如 **SK-GS**，Wan et al., NeurIPS 2024）：从单目视频中自动提取骨骼并驱动高斯变形，但依赖密集的时间采样来学习连贯的运动。当帧率降低10-20倍时，时间对应变得稀疏且不可靠，重建结果出现噪声变形和结构丢失。

- **骨骼驱动方法**（如 **RigGS**，Yao et al., CVPR 2025）：利用稀疏控制点估计骨架并建模动态场景，但其整个变形网络高度依赖时间输入，在稀疏时间监督下难以学习到平滑的关节运动。

- **生成式方法**：尝试从静态状态合成完整运动，但缺乏对时序结构的显式建模，难以保证运动在物理上的合理性。

图Figure 2清晰地对比了这些方法的输入配置差异：多视角和单目视频方法假设小视角变化和密集时间观察，而本文方法处理的是稀疏时间观察与大视角变化的组合。

### 核心瓶颈与本文动机

上述方法的共同缺陷在于：**变形场的几乎所有参数都直接或间接地依赖于时间**。当时间监督极度稀疏时，网络缺乏足够的信号来学习从时间到变形的复杂映射，导致过拟合、噪声变形和结构坍塌。

本文的核心洞察是：对于关节物体（如人体、动物、机械臂），其运动本质上是由底层骨骼的关节旋转驱动的。如果我们能够将变形场**分解**为两部分——仅让粗糙的关节姿态估计依赖时间，而让皮肤权重校正和细节变形在规范空间中学习且与时间无关——那么即使只有稀疏的时间监督，模型也能通过骨骼结构的强先验恢复出连续的关节运动，并在未见过的中间时间步实现平滑插值。

基于此动机，本文提出 **SV-GS（Skeleton-View Gaussian Splatting）**，一种骨骼驱动的高斯泼溅框架。该方法以第一帧的粗糙骨骼图和初始静态3D重建为输入，仅需每个时间步一张任意视角的稀疏图像，即可重建出高质量的连续4D动态场景。

## 核心方法与创新机理

SV-GS 的核心创新在于将动态场景的变形场显式分解为**时间依赖**与**时间无关**两个部分，从而在极度稀疏的时间监督下实现连贯的4D重建。具体而言，其关键设计体现在以下三个 changed slots 上。

### 1. 稀疏任意视角的输入配置

现有动态重建方法（如 **4DGS** (Wu et al., CVPR 2024)、**SK-GS** (Wan et al., NeurIPS 2024)、**RigGS** (Yao et al., CVPR 2025)）通常依赖密集的多视角或单目视频序列，要求相邻帧之间具有较小的视角变化和丰富的时间对应信息。SV-GS 则将输入条件大幅放宽：每个时间步仅需**单张任意视角的RGB图像**，且时间采样密度可比现有方法稀疏20倍（Figure 1, Figure 2）。这种稀疏配置使得传统方法难以建立可靠的时间对应关系，而 SV-GS 通过引入骨骼结构先验来弥补信息缺失。

### 2. 变形场的时间依赖性解耦

这是 SV-GS 最根本的设计选择。在基线方法中，整个变形网络或大部分参数都直接依赖于时间变量，导致在稀疏时间观察下容易产生噪声变形。SV-GS 将变形场拆分为三个模块，仅让关节姿态估计器 $MLP_{\Theta}$ 依赖于时间：

- **关节姿态估计器 $MLP_{\Theta}$**：以时间 $t$ 为输入，预测每个骨骼关节的局部旋转四元数 $q^{t}$ 和根关节位移 $p^{t}$（Equation 2）。这是整个变形场中**唯一时间依赖的组件**。
- **皮肤校正场 $MLP_{\Phi}$**：在规范空间中预测皮肤权重的修正量，**不随时间变化**。
- **细节变形场 $MLP_{\Psi}$**：以规范高斯中心 $\mu_{i}$ 和当前关节姿态 $\mathbf{R}^{t}$ 为输入，预测细粒度偏移，但其网络参数本身**与时间无关**。

这种设计使得模型仅需从稀疏的时间样本中学习关节姿态的粗粒度变化，而皮肤权重和细节变形则从规范空间的结构中习得，从而在未见过的中间时间步实现平滑的运动插值（Section 3.3）。

### 3. 骨骼驱动的可学习LBS变形表示

基线方法通常采用无结构的隐式变形场或基于超点的变形簇，缺乏对关节运动的结构化约束。SV-GS 则构建了一个骨骼驱动的可学习线性混合蒙皮（LBS）变形管道：

- **可学习半径的RBF皮肤权重**：通过径向基函数核计算每个高斯原语对各骨骼关节的初始皮肤权重 $w_{i,j}$，其中每个骨骼关节的可学习半径 $r_j$ 控制其影响范围（Equation 5-6）。
- **皮肤校正场**：$MLP_{\Phi}$ 对初始皮肤权重进行修正，以处理标准LBS难以建模的复杂蒙皮效果。
- **层级化前向运动学**：根据骨骼的父子连接关系，将局部关节变换传播为全局变换矩阵 $\hat{\mathbf{R}}_{j}^{t}, \hat{T}_{j}^{t}$（Equation 3），进而驱动规范高斯中心变换到当前姿态空间（Equation 4）。
- **细节变形补充**：在骨骼驱动的粗变形基础上，$MLP_{\Psi}$ 添加姿态依赖的偏移量 $\hat{\mu}_{i}^{t} = \mu_{i}^{t} + MLP_{\Psi}(\gamma(\mu_{i}), \mathbf{R}^{t})$（Equation 8），以捕捉骨骼运动无法覆盖的非刚性细粒度细节。

这种“粗骨骼驱动 + 细细节补充”的双层变形策略，使得模型在稀疏监督下既能保持物体的整体结构，又能还原精细的运动细节（Figure 4）。消融实验证实，移除细节变形场会导致SSIM从0.950降至0.931，移除皮肤校正场则降至0.943（Table 4），验证了各模块的必要性。

### 方法谱系与知识库定位

SV-GS 处于**骨骼驱动动态重建**与**3D Gaussian Splatting**的交汇点。与 **SK-GS** (Wan et al., NeurIPS 2024) 的自动骨骼提取不同，SV-GS 接受显式的骨骼图作为输入，将问题聚焦于稀疏观察下的运动建模。与 **RigGS** (Yao et al., CVPR 2025) 的稀疏控制点骨架估计相比，SV-GS 的时间依赖性解耦设计使其在仅11帧的极端稀疏条件下仍能保持结构完整性。在知识库定位上，该方法为“结构先验引导的少样本动态重建”提供了新的范式：通过将时间依赖压缩到最小必要组件，使模型能够从稀疏的时间快照中泛化出连续的4D表示。

SV-GS 的整体 pipeline 围绕一个核心设计原则展开：**将变形场分解为时间依赖的粗运动估计和与时间无关的细粒度校正**，从而在稀疏时间监督下实现连续的 4D 重建。如图 Figure 3 所示，系统接收三类输入并依次通过五个关键模块完成动态重建。

### 输入配置

与现有动态重建方法依赖密集时间采样和较小视角变化的假设不同（Figure 2），SV-GS 的输入条件极为稀疏：

![[assets/figures/papers/paper_list_l48_https_arxiv_org_abs_2601_00285/figures/002_Figure_2.jpg]]
*Figure 2: Comparison of input configurations across dynamic reconstruction methods. Multi-view and monocular video methods assume small viewpoint changes and dense temporal observations, whereas our method handles sparse temporal observations with large viewpoint variations. Generative methods attempt to synthesize the full motion from a static state*

1. **稀疏时间观察**：一组带姿态的 RGB 图像 $\mathcal{T} = \{I_t\}_{t \in [0,1]}$，每个时间步仅提供**单张任意视角**的图像，帧数可比原始序列少 20 倍（Figure 1）。
2. **骨骼结构先验**：仅在首帧提供带注释的骨骼图 $\mathcal{F}$，指定 $J$ 个关节的 3D 位置及父子连接关系。
3. **初始静态重建**：规范空间下的 3D 高斯表示 $\mathcal{G}$，可通过多视图图像或预训练的图像到 3D 扩散模型获得。

### Pipeline 模块与数据流

整个 pipeline 由五个模块串联构成，数据流从时间信号到最终渲染像素逐步推进：

**模块 1：初始静态 3DGS 构建**
在规范空间（$t=0$ 姿态）下建立目标的高斯泼溅表示。当多视图图像可用时直接优化；否则利用 Zero-1-to-3 扩散先验通过 Score Distillation Sampling（SDS）从单张参考图生成不可见视角的几何。该模块仅在训练前执行一次，后续变形场优化中保持冻结。

**模块 2：关节姿态估计器（$MLP_{\Theta}$）**
这是整个 pipeline 中**唯一依赖时间 $t$ 的组件**。以位置编码后的时间 $\gamma(t)$ 为输入，输出每个关节的局部旋转四元数 $q^t$ 和根关节位移 $p^t$：
$$q^{t}, p^{t} = MLP_{\Theta}(\gamma(t))$$
该设计的关键意义在于：时间依赖性被严格限制在关节姿态层面，后续的皮肤变形和细节校正均不直接依赖时间，从而在未见中间时间步上实现平滑的运动插值。

**模块 3：前向运动学**
根据骨骼层级结构，将局部关节变换传播为全局变换矩阵：
$$\hat{\mathbf{R}^{t}}, \hat{T^{t}} = fk(\mathcal{F}, q^{t}, p^{t})$$
这一步将关节级的局部旋转转换为每个骨骼相对于规范空间的全局旋转矩阵和平移向量。

**模块 4：可学习 LBS 变形**
利用线性混合蒙皮（LBS）将规范高斯中心变换到当前姿态空间。与传统 LBS 不同，SV-GS 的皮肤权重通过可学习的 RBF 核计算，并由皮肤校正场 $MLP_{\Phi}$ 在规范空间中调整，二者均**不随时间变化**：
$$\mu_{i}^{t} = \sum_{j=1}^{B} w_{i,j} (\hat{\mathbf{R}_{j}^{t}} \mu_{i} + \hat{T_{j}^{t}})$$
其中 $w_{i,j}$ 是可学习皮肤权重，$B$ 为骨骼数量。这一模块提供了由骨骼驱动的粗粒度变形。

**模块 5：细节变形场（$MLP_{\Psi}$）**
在骨骼驱动中心的基础上，添加姿态依赖的细粒度偏移以捕捉非刚性细节：
$$\hat{\mu_{i}^{t}} = \mu_{i}^{t} + MLP_{\Psi}(\gamma(\mu_{i}), \mathbf{R}^{t})$$
该模块以规范高斯中心的位置编码和全局关节姿态为条件，输出微小偏移量。注意 $MLP_{\Psi}$ 本身在规范空间中定义，不直接依赖时间 $t$，仅通过关节姿态 $\mathbf{R}^t$ 间接感知当前姿态。

最终，变形后的高斯 $\hat{\mu_i^t}$ 通过标准 3DGS 渲染管线（alpha 混合）生成像素颜色，并与稀疏观察图像计算感知损失进行端到端优化。

### 关键设计决策

整个框架的核心洞察在于**时间依赖性的最小化**：仅 $MLP_{\Theta}$ 直接接收时间信号，$MLP_{\Phi}$ 和 $MLP_{\Psi}$ 均在规范空间中定义且网络参数不随时间变化。这种分解使得模型在仅 11 帧的稀疏监督下，仍能通过骨骼结构的强先验约束学习到连贯的关节运动，并在未见时间步上实现平滑插值——这是现有方法（如 4DGS、SK-GS、RigGS）在同等稀疏条件下无法做到的（Figure 4）。

SV-GS 的核心思路是将动态场景的变形场分解为**时间依赖的粗运动**与**时间无关的细粒度校正**两个层次，从而在稀疏时间监督下实现平滑的运动插值。整个流程围绕五个关键模块展开。

### 初始静态 3DGS 构建

方法首先在规范空间（canonical space）中建立目标的静态高斯表示 $\mathcal{G} = \{(\mu_i, \Sigma_i, \sigma_i, c_i)\}_{i=1}^{N}$，其中 $\mu_i$ 为高斯中心，$\Sigma_i$ 为协方差矩阵，$\sigma_i$ 为不透明度，$c_i$ 为颜色。该静态重建可通过首帧多视角图像获得，也可利用预训练扩散先验从单张参考图生成（见 Section 4.3）。渲染时，像素颜色由标准 alpha 混合公式给出：

$$color = \sum_{k} c_k \alpha_k \prod_{j=1}^{k-1} (1 - \alpha_j)$$

### 关节姿态估计器（MLP_Θ）

这是整个变形场中**唯一依赖时间**的组件。以时间 $t$ 的位置编码 $\gamma(t)$ 为输入，MLP_Θ 预测每个骨骼关节的局部旋转四元数 $q^{t}$ 和根关节位移 $p^{t}$：

$$q^{t}, p^{t} = MLP_{\Theta}(\gamma(t))$$

通过将时间依赖性严格限制在这一模块中，其余变形组件（皮肤校正、细节变形）均在规范空间中学习且与时间无关，这使得模型在未见中间时间步上能够自然实现平滑插值。

### 前向运动学

根据骨骼层级结构 $\mathcal{F}$，将 MLP_Θ 预测的局部关节变换传播为全局旋转矩阵 $\hat{\mathbf{R}^{t}}$ 和平移 $\hat{T^{t}}$：

$$\hat{\mathbf{R}^{t}}, \hat{T^{t}} = fk(\mathcal{F}, q^{t}, p^{t})$$

### 可学习 LBS 变形

传统线性混合蒙皮（LBS）的皮肤权重通常由艺术家手工设定。SV-GS 采用**可学习半径的 RBF 核**自动计算每个高斯原语 $i$ 对骨骼关节 $j$ 的皮肤权重 $w_{i,j}$，并通过**皮肤校正场 MLP_Φ** 在规范空间中对权重进行调整。随后，利用全局骨骼变换将规范高斯中心 $\mu_i$ 变换到时间 $t$ 的姿态空间：

$$\mu_{i}^{t} = \sum_{j=1}^{B} w_{i,j} (\hat{\mathbf{R}_{j}^{t}} \mu_{i} + \hat{T_{j}^{t}})$$

这一设计使得骨骼驱动的粗运动能够自适应地传播到每个高斯原语，同时皮肤校正场补偿了标准 LBS 在关节附近的体积塌陷等典型伪影。

### 细节变形场（MLP_Ψ）

在骨骼驱动中心 $\mu_{i}^{t}$ 的基础上，细节变形场 MLP_Ψ 以规范高斯中心 $\mu_i$ 的位置编码和当前全局关节旋转 $\mathbf{R}^{t}$ 为输入，预测一个额外的偏移量，用于捕捉非刚性细粒度细节（如肌肉隆起、衣物褶皱）：

$$\hat{\mu_{i}^{t}} = \mu_{i}^{t} + MLP_{\Psi}(\gamma(\mu_{i}), \mathbf{R}^{t})$$

最终高斯中心 $\hat{\mu_{i}^{t}}$ 融合了骨骼驱动的粗运动与细节变形场的细粒度校正，在稀疏监督下仍能保持物体结构并恢复精细运动。

### 优化目标

总损失函数为三项的加权和：

$$\mathcal{L} = \lambda_{1} \mathcal{L}_{perceptual} + \lambda_{2} \mathcal{L}_{motion} + \lambda_{3} \mathcal{L}_{detail}$$

其中 $\lambda_{1}=2, \lambda_{2}=1, \lambda_{3}=1$。各损失项的作用如下：

- **感知损失 $\mathcal{L}_{perceptual}$**：基于 VGG 特征的 LPIPS 损失，约束渲染图像与稀疏观测图像的一致性。
- **运动正则化 $\mathcal{L}_{motion}$**：通过拉普拉斯算子约束关节旋转四元数的时间平滑性，防止稀疏监督下出现关节姿态跳变：

$$\mathcal{L}_{motion} = \frac{1}{T J} \sum_{t}^{T} \sum_{j}^{J} \left| q_{j}^{t-1} - 2 q_{j}^{t} + q_{j}^{t+1} \right|$$

- **细节正则化 $\mathcal{L}_{detail}$**：L2 范数惩罚细节变形场的偏移量，防止过大的非刚性位移导致结构失真：

$$\mathcal{L}_{detail} = \frac{1}{N} \sum_{i}^{N} \| MLP_{\Psi}(\gamma(\mu_{i}), \mathbf{R}^{t}) \|_{2}^{2}$$

消融实验（Table 4）验证了各组件的必要性：移除细节变形场 MLP_Ψ 导致 PSNR 从 27.75 降至 26.65，SSIM 从 0.950 降至 0.931；移除皮肤校正场 MLP_Φ 使 PSNR 降至 27.25，SSIM 降至 0.943；移除运动正则化 $\mathcal{L}_{motion}$ 则使 PSNR 降至 27.33，SSIM 降至 0.945，并引入关节姿态噪声（Figure 10）。

## 实验与关键发现

### 核心定量结果

SV-GS 在三个动态场景基准上均表现出显著优势，尤其在稀疏时间采样的极端条件下，与现有方法的性能差距被急剧拉大。

**D-NeRF 数据集（0.1 时间间隔，仅 11 帧/序列）**：如 Table 1 所示，SV-GS 以 PSNR **27.75**、SSIM **0.950**、LPIPS **5.79** 全面超越所有基线。相比最强的骨骼驱动基线 RigGS†（PSNR 23.48，SSIM 0.893，LPIPS 9.43），PSNR 提升 **+4.27（+18.2%）**，LPIPS 降低 **38.6%**。这一差距的根源在于：4DGS 和 SK-GS 等方法的变形场高度依赖密集时间对应来学习运动模式，当帧数减少 20 倍时，它们无法建立可靠的时间关联，产生噪声变形并丢失物体结构（Figure 4）。SV-GS 通过骨骼图提供的结构先验，将时间依赖限制在关节姿态估计器上，从而在稀疏监督下仍能维持连贯的关节运动。

**DG-Mesh 数据集**：在 0.05 间隔（21 帧）和 0.1 间隔（11 帧）两种设置下，SV-GS 的 SSIM 分别达到 **0.929** 和 **0.900**，较 RigGS† 分别提升 +0.105（+12.7%）和 +0.114（+14.5%）（Table 2）。值得注意的是，随着时间间隔从 0.05 增大到 0.1，RigGS† 的 SSIM 从 0.824 降至 0.786（降幅 4.6%），而 SV-GS 仅从 0.929 降至 0.900（降幅 3.1%），表明骨骼驱动的变形表示对采样密度的下降具有更强的鲁棒性。

**ZJU-MoCap 真实世界数据集**：在使用仅 **1/10 帧数**（比全序列少 10 倍）的条件下，SV-GS 达到 SSIM **0.934**，与使用全序列训练的 RigGS（SSIM 0.975）性能差距仅为 0.041（Table 3）。当使用 1/5 帧数时，SSIM 进一步提升至 0.944。考虑到帧数减少了 5-10 倍，这一结果验证了骨骼先验在真实场景稀疏观察下的有效性。

### 消融实验

Table 4 在 D-NeRF 数据集上系统评估了三个关键组件的贡献：

![[assets/figures/papers/paper_list_l48_https_arxiv_org_abs_2601_00285/figures/013_Table_4.jpg]]
*Table 4: Ablation study on the D-NeRF dataset. We evaluate the effect of the motion regularization term*

- **移除细节变形场 MLP_Ψ**：SSIM 从 0.950 降至 0.931，PSNR 从 27.75 降至 26.65。细节变形场负责在骨骼驱动的粗运动之上捕捉非刚性细粒度细节（如肌肉颤动、衣物褶皱），其缺失导致对高频运动的拟合能力下降。
- **移除皮肤校正场 MLP_Φ**：SSIM 降至 0.943，PSNR 降至 27.25。皮肤校正场通过学习调整基于 RBF 核的初始皮肤权重，使高斯原语与骨骼的绑定关系更精确，缺失后部分区域的变形出现不自然的拉伸或压缩。
- **移除运动正则化项 L_motion**：SSIM 降至 0.945，PSNR 降至 27.33，且关节姿态预测引入噪声（Figure 10）。L_motion 通过拉普拉斯算子约束相邻帧间关节旋转的二阶平滑性，是防止稀疏时间步之间出现不连续跳变的关键机制。

![[assets/figures/papers/paper_list_l48_https_arxiv_org_abs_2601_00285/figures/012_Figure_10.jpg]]
*Figure 10: Qualitative comparison of results with and without*

### 定性分析

Figure 4 的定性对比揭示了基线方法的典型失败模式：在 D-NeRF 的 Lego 和 T-Rex 等场景中，4DGS 和 SK-GS 在稀疏观察下产生严重的几何坍塌和纹理模糊，RigGS 虽能保持大致轮廓但细节扭曲明显。SV-GS 则能准确恢复关节姿态并保持物体结构完整性。Figure 6 在 DG-Mesh 数据集上进一步表明，对于小幅运动区域，各方法表现接近，但在大幅关节运动区域，SV-GS 对细粒度运动的捕捉更为忠实。

![[assets/figures/papers/paper_list_l48_https_arxiv_org_abs_2601_00285/figures/004_Figure_4.jpg]]
*Figure 4: Qualitative results on the D-NeRF dataset [40] downsampled at 0.1 intervals, yielding 11 frames per motion sequence (up to 20× fewer than the original). We compare our method with SOTA methods including 4DGS [54], SK-GS [51], and RigGS [64]. Additionally, we modify RigGS [64] to take in the same skeleton input as ours. Despite all methods being initialized with the same multi-view images at t = 0, existing methods produce noisy deformations and fail to preserve object structure given only sparse temporal observations*

![[assets/figures/papers/paper_list_l48_https_arxiv_org_abs_2601_00285/figures/008_Figure_6.jpg]]
*Figure 6: Qualitative result on the DG-Mesh dataset [20] downsampled at 0.05 intervals, yielding 21 frames per motion sequence. While all methods perform similarly for parts with small motion, our approach better preserves object structure and captures finegrained motion more faithfully*

### 失败模式与局限性

尽管 SV-GS 在稀疏观察下表现优异，但存在以下已知局限：

1. **扩散先验初始化的几何不完整性**：当使用单张参考图通过 Zero-1-to-3 扩散先验生成不可见视角时（Section 4.3），严重自遮挡或非典型视角可能导致初始静态高斯重建出现缺失区域（Figure 8），进而影响后续变形质量。
2. **测试时插值的精度边界**：对于极度高频或高度复杂的运动（如快速旋转、剧烈形变），仅依赖稀疏关键帧训练的关节姿态估计器可能在中间时刻产生欠拟合的插值结果。
3. **骨骼图质量依赖**：方法假设输入骨骼图是准确的，骨骼节点的噪声或拓扑错误会直接传播到 LBS 变形中，导致高斯原语被错误驱动。
4. **适用场景限制**：对于非关节物体或缺乏明显骨骼结构的动态目标（如流体、烟雾），骨骼驱动的变形表示本质上不适用。

![[assets/figures/papers/paper_list_l48_https_arxiv_org_abs_2601_00285/figures/011_Figure_8.jpg]]
*Figure 8: Comparison of all methods without access to multi-view images at the initial time step. Despite using only 11 sparse input, our method reconstructs motion and preserves object structure more faithfully, whereas baselines are prone to artifacts under self-occlusion and sparse supervisions*

## 定位与知识库关联

### 1. 问题定位：稀疏视角 4D 重建

SV-GS 针对的核心瓶颈是：**现有动态场景重建方法在稀疏时间观察且视角变化剧烈的情况下，无法建立可靠的时间对应关系，导致重建质量严重下降**。如图 2 所示，多视角方法（如 4DGS）和单目视频方法（如 SK-GS）都假设密集的时间采样和较小的视角变化，而 SV-GS 专为稀疏时间步（最多减少 20 倍帧数）和任意大视角变化设计。

### 2. 与基线工作的关系

#### 2.1 动态高斯泼溅方法

**4DGS**（Wu et al., CVPR 2024）采用多分辨率六平面建模整个变形场，整个变形网络随时间变化。在 D-NeRF 数据集下采样至 0.1 间隔（每序列仅 11 帧）时，4DGS 产生噪声变形且无法保持物体结构（Figure 4）。SV-GS 的核心改进在于**仅让关节姿态估计器依赖时间**，皮肤校正场和细节变形场在规范空间中与时间无关，从而在稀疏监督下实现平滑运动插值。

**SK-GS**（Wan et al., NeurIPS 2024）从单目视频中自动提取骨骼并驱动高斯变形，属于模板无关方法。但该方法仍依赖密集时间序列来学习骨骼结构和变形。在稀疏观察下，SK-GS 同样出现结构丢失问题（Figure 4）。SV-GS 的区别在于直接接受外部提供的骨骼图作为强结构先验，避免了在稀疏数据中同时学习骨骼和变形的困难。

**RigGS**（Yao et al., CVPR 2025）利用稀疏控制点估计骨架并建模动态场景。为公平比较，作者将 RigGS 修改为接受与 SV-GS 相同的骨骼图输入（记为 RigGS†）。在 D-NeRF 数据集上，RigGS† 的 PSNR 为 23.48，而 SV-GS 达到 27.75，提升超过 18%（Table 1）。这表明**骨骼驱动的变形框架本身并非充分条件，SV-GS 的分解式变形设计（粗骨骼驱动 + 细粒度校正）是关键差异**。

#### 2.2 输入配置差异

| 方法 | 时间采样 | 视角变化 | 结构先验 |
|------|---------|---------|---------|
| 4DGS | 密集 | 小 | 无 |
| SK-GS | 密集（单目视频） | 小 | 自动提取骨骼 |
| RigGS | 密集 | 小 | 稀疏控制点 |
| **SV-GS** | **稀疏（最多 20× 减少）** | **任意大** | **外部骨骼图** |

### 3. 方法谱系中的位置

SV-GS 处于**骨骼驱动动态重建**和**稀疏视角重建**的交叉点。其变形场设计可分解为三个层次：

1. **时间依赖的粗运动**：关节姿态估计器 $MLP_{\Theta}$ 以时间 $t$ 为输入，预测各关节的局部旋转四元数 $q^t$ 和根关节位移 $p^t$（Equation 2）。通过前向运动学传播为全局变换矩阵（Equation 3），驱动规范高斯中心变换。
2. **与时间无关的皮肤校正**：可学习 RBF 皮肤权重结合皮肤校正场 $MLP_{\Phi}$，在规范空间中调整高斯原语与骨骼的关联。
3. **姿态依赖的细节变形**：细节变形场 $MLP_{\Psi}$ 以规范高斯中心 $\gamma(\mu_i)$ 和全局关节旋转 $\mathbf{R}^t$ 为输入，添加额外偏移以捕捉非刚性细粒度细节（Equation 8）。

这种分解的核心洞察是：**将变形场分解为时间依赖的关节姿态预测和与时间无关的皮肤校正、细节变形，粗运动由骨骼驱动，细粒度变形由细节场补充**。这使得在未见中间时间步骤可以实现平滑运动插值（Section 3.3）。

### 4. 适用边界与局限

1. **骨骼先验依赖**：方法需要外部提供初始骨骼图（骨骼节点 3D 位置和父子连接关系），骨骼的噪声可能影响变形质量。对于非关节物体或没有明显骨骼结构的动态目标，本方法可能不适用。
2. **扩散先验初始化的局限**：当使用扩散模型（Zero-1-to-3）替代多视图初始化时，在严重自遮挡或非典型视角下可能产生不完整的几何（Section 4.3）。
3. **运动插值边界**：测试时插值对于极度高频或高度复杂的运动可能无法完全准确。
4. **非刚性变形能力**：细节变形场 $MLP_{\Psi}$ 仅提供姿态依赖的偏移，对于拓扑变化或大幅非刚性变形，骨骼驱动的 LBS 框架本身存在表达能力上限。

### 5. 开放问题

1. **类别特定先验的融合**：能否利用人体/动物模型（如 SMPL）等类别特定先验，进一步提高稀疏观察下对特定类别目标的重建精度？
2. **骨骼自动估计**：当前方法依赖人工标注的骨骼图，如何从稀疏图像中自动估计骨骼结构是一个实用的扩展方向。
3. **视频扩散先验**：结合预训练视频扩散模型来进一步提升运动插值的真实感，特别是在极度稀疏（如仅 3-5 帧）的场景下。
4. **多目标与交互场景**：当前方法针对单个关节目标，扩展到多目标交互场景需要处理骨骼间的物理约束和遮挡关系。

## 原文 PDF

![[paperPDFs/CVPR_2026/SV_GS_Sparse_View_4D_Reconstruction_with_Skeleton_Driven_Gaussian_Splatting.pdf]]
