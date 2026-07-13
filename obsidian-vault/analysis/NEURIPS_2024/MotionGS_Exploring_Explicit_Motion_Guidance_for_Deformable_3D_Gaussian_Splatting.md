---
title: "MotionGS: Exploring Explicit Motion Guidance for Deformable 3D Gaussian Splatting"
type: paper
paper_level: A
venue: NeurIPS
year: 2024
pdf_ref: paperPDFs/NEURIPS_2024/MotionGS_Exploring_Explicit_Motion_Guidance_for_Deformable_3D_Gaussian_Splatting.pdf
project_link: https://ruijiezhu94.github.io/MotionGS_page/
code_link: null
aliases:
- MotionGS
tags:
- NEURIPS_2024
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
core_operator: "通过光流解耦模块，将光流分解为仅由物体运动引起的运动流和仅由相机运动引起的相机流，并利用运动流显式监督 3D 高斯的变形（高斯流），提供纯粹的运动先验。同时，引入相机位姿细化模块，交替优化高斯场与相机位姿，减少因位姿不准造成的误差。"
primary_logic: "从混合光流中剥离相机运动成分，得到纯净的对象运动流，用以直接约束 3D 高斯的位移，能够显著提升动态场景重建的精度与鲁棒性。"
claims:
- "直接使用未解耦的光流监督会导致性能相比基线下降，因为相机与物体运动混合造成歧义。"
- "使用解耦的运动流监督带来显著性能提升（PSNR 从 23.61 到 24.12），证明显式运动指导的有效性。"
- "在运动流监督基础上叠加相机位姿细化，进一步提升性能，达到最佳 PSNR 24.54。"
- "NeRF-DS 上 PSNR = 24.54"
---

# MotionGS: Exploring Explicit Motion Guidance for Deformable 3D Gaussian Splatting

> [!tip] 核心洞察
> 从混合光流中剥离相机运动成分，得到纯净的对象运动流，用以直接约束 3D 高斯的位移，能够显著提升动态场景重建的精度与鲁棒性。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | MotionGS：探索显式运动引导的可变形 3D 高斯溅射 |
| 英文题名 | MotionGS: Exploring Explicit Motion Guidance for Deformable 3D Gaussian Splatting |
| 会议/期刊 | NeurIPS 2024 |
| Links | [paper](https://arxiv.org/abs/2410.07707) · [Project](https://ruijiezhu94.github.io/MotionGS_page/) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction |
| Method | MotionGS |
| Dataset | NeRF-DS, HyperNeRF (vrig subset) |

> [!tip] 效果简介
> - NeRF-DS 上，PSNR 为 24.54，对比 23.61 (Deformable-3DGS)，变化 +0.93。
> - NeRF-DS 上，SSIM 为 0.8656，对比 0.8394 (Deformable-3DGS)，变化 +0.0262。
> - NeRF-DS 上，LPIPS 为 0.1719，对比 0.1970 (Deformable-3DGS)，变化 -0.0251。

## 概要

动态场景的 3D 重建是计算机视觉领域的核心挑战之一。近期，基于可变形 3D 高斯溅射（Deformable 3DGS）的方法在单目动态场景重建中展现出巨大潜力，但其训练过程仅依赖外观重建损失，缺乏对物体运动本身的显式约束。当物体运动不规则或场景动态复杂时，这一瓶颈导致优化容易陷入局部最优，重建质量显著下降。

MotionGS 针对上述问题提出了一个核心洞察：**从混合光流中剥离相机运动成分，得到纯净的对象运动流，用以直接约束 3D 高斯的位移，能够显著提升动态场景重建的精度与鲁棒性**。基于此，该方法引入两条因果调控路径：

1. **光流解耦模块**：将相邻帧的光流分解为仅由物体运动引起的运动流和仅由相机运动引起的相机流，并利用运动流显式监督 3D 高斯的变形（高斯流），提供纯粹的运动先验。消融实验表明，直接使用未解耦的光流监督会导致性能相比基线下降（PSNR 23.37 vs 基线 23.61），而使用解耦的运动流监督则带来显著提升（PSNR 24.12），证实了运动流解耦的关键作用。
2. **相机位姿细化模块**：在相对位姿上添加可学习的 SE(3) 残差，交替优化高斯场与相机位姿，减少因 COLMAP 初始位姿不准造成的误差。在运动流监督基础上叠加该模块，性能进一步提升至最佳 PSNR 24.54。

在实验层面，MotionGS 在 NeRF-DS 数据集上取得 PSNR 24.54、SSIM 0.8656、LPIPS 0.1719，相较主要基线 Deformable-3DGS（Yang et al., arXiv 2023）分别提升 +0.93 dB、+0.0262、-0.0251；在 HyperNeRF 的 vrig 子集上 PSNR 提升达 +2.3 dB。方法在动态物体细节重建上展现出明显优势，但在固定且稀疏相机视角的场景（如 DyNeRF）上仍存在因渲染深度不准确导致的漂浮伪影问题。

> **⚠️ 注意**：NeRF-DS 和 HyperNeRF 方法使用基于 AlexNet 的 LPIPS，而 MotionGS 等使用基于 VGG 的 LPIPS，因此 LPIPS 数值不完全可比。



动态场景的新视角合成是计算机视觉与图形学中的核心挑战。近年来，以 3D 高斯溅射（3D Gaussian Splatting, 3DGS）为代表的显式场景表示方法在静态场景渲染中展现出高质量、实时性的优势。然而，将其扩展到动态场景时，主流方案——如 **Deformable-3DGS**（Yang et al., arXiv 2023）——引入可变形场来建模高斯原语随时间的位置、旋转和缩放变化，却面临一个根本性瓶颈：**优化过程仅依赖光度重建损失，缺少对物体运动本身的显式约束**。

这一缺口的后果是严重的。当物体运动不规则、场景动态复杂时，纯外观驱动的优化极易陷入局部最优，导致几何形变不准确、渲染出现漂浮伪影。直觉上，光流作为像素级的运动信号，似乎可以天然地填补这一空白——直接用它监督 3D 高斯的位移即可。但事实恰恰相反：**直接使用未解耦的光流作为监督，性能反而低于基线**（Table 3：PSNR 23.37 vs 基线 23.61）。原因在于，光流是相机运动与物体运动的混合产物，相机自运动（ego-motion）引入的噪声会严重误导高斯变形，使监督信号本身成为歧义来源。

这揭示了一个更深层的因果机制：**要有效利用运动先验，必须将相机运动成分从光流中剥离**，得到仅由物体运动引起的“运动流”（motion flow），才能为 3D 高斯的变形提供纯净、直接的监督。在此基础上，相机位姿本身的估计误差（通常来自 COLMAP）也会传播到运动流的计算中，进一步放大不准确性，因此相机位姿的联合优化同样是提升鲁棒性的关键环节。

综上，本文 **MotionGS** 的核心动机是：**为可变形 3D 高斯溅射引入显式、解耦的运动引导**，通过光流解耦模块分离运动流与相机流，并辅以相机位姿细化模块交替优化场景与位姿，从而突破现有方法在复杂动态场景中的性能上限。



## 核心方法与创新机理

MotionGS 的核心创新在于将动态场景重建的优化目标从单一的“外观匹配”扩展为“外观+运动”双重约束，并通过两个关键模块——**光流解耦模块**和**相机位姿细化模块**——为可变形 3D 高斯溅射提供了显式的运动引导。

### 1. 从混合光流到纯净运动流：光流解耦模块

现有可变形 3DGS 方法（如 **Deformable-3DGS**，Yang et al., arXiv 2023）仅依赖光度重建损失来约束高斯变形，缺乏对物体运动本身的直接监督。MotionGS 的核心洞察在于：**从混合光流中剥离相机运动成分，得到纯净的对象运动流，用以直接约束 3D 高斯的位移**。

具体而言，光流解耦模块将相邻帧间的光流 $F_{t, t+1}$ 分解为两部分：

- **相机流** $F_{t, t+1}^C$：仅由相机自运动引起，通过渲染深度和相机位姿直接计算：
  $$F_{t, t+1}^C = p_t^{t+1} - p_t$$
  其中 $p_t^{t+1}$ 是将帧 $I_t$ 中的像素点 $p_t$ 通过深度反投影到 3D 空间后，再用相机 $C_{t+1}$ 的位姿重投影到帧 $I_{t+1}$ 得到的坐标。

- **运动流** $F_{t, t+1}^M$：去除相机运动后，仅由物体运动引起的光流分量：
  $$F_{t, t+1}^M = F_{t, t+1} - F_{t, t+1}^C$$

随后，MotionGS 引入**高斯流**（Gaussian Flow）概念——将 3D 高斯从 $t$ 时刻到 $t+1$ 时刻的变形投影到 2D 平面——并通过 L1 损失直接与运动流对齐：
$$\mathcal{L}_{\mathrm{flow}} = \| sg(F_{t, t+1}^M) - F_{t, t+1}^G \|$$
其中 $sg(\cdot)$ 表示停止梯度，防止运动流被反向传播更新。

**消融实验提供了决定性证据**（Table 3）：
- 直接使用未解耦的光流监督（+ optical flow guidance）导致 PSNR 从基线的 23.61 降至 23.37，说明相机与物体运动的混合会引入歧义噪声。
- 使用解耦的运动流监督（+ motion flow guidance）将 PSNR 提升至 24.12，证实了纯净运动先验的有效性。

### 2. 相机位姿的在线细化：相机位姿细化模块

传统方法直接使用 COLMAP 估计的固定相机位姿，但动态场景中位姿估计本身存在误差，会累积到变形优化中。MotionGS 在相对位姿上引入可学习的 SE(3) 残差 $\Delta T$，并采用交替优化策略：

- **冻结高斯，优化位姿**：冻结所有 3D 高斯属性，仅通过光度损失反向传播更新相机位姿残差，提高训练稳定性。
- **冻结位姿，优化高斯**：恢复标准的高斯场与变形网络训练。

这一设计使得位姿误差不再被“固化”到场景表示中。消融实验表明，在运动流监督基础上叠加相机位姿细化（+ motion flow guidance + camera pose refinement），PSNR 进一步提升至 24.54，达到最佳性能。



![[assets/figures/papers/paper_list_l11_MotionGS_Exploring_Explicit_Motion_Guidance_for_Deformable_3D_Gaussian_S/figures/002_Figure_2.jpg]]
*Figure 2: The overall architecture of MotionGS. It can be viewed as two data streams: (1) The 2D data stream utilizes the optical flow decoupling module to obtain the motion flow as the 2D motion prior; (2) The 3D data stream involves the deformation and transformation of Gaussians to render the image for the next frame. During training, we alternately optimize 3DGS and camera poses through the camera pose refinement module*

MotionGS 的整体架构遵循双数据流设计，如 **Figure 2** 所示：一条 2D 数据流负责从光流中提取纯净的运动先验，另一条 3D 数据流则利用该先验显式约束高斯的变形与渲染。两条流在训练过程中协同工作，并辅以交替优化的相机位姿细化模块。

### 2D 数据流：光流解耦与运动先验提取

2D 数据流的输入是相邻帧 $I_t$ 与 $I_{t+1}$。首先，通过预训练的光流估计网络 **GMFlow** 获取前向光流 $F_{t, t+1}$。该光流混合了相机自运动与场景物体运动两种成分——直接将其作为监督信号会引入歧义（消融实验证实，不解耦的光流监督使 PSNR 从基线 23.61 降至 23.37，见 **Table 3**）。

光流解耦模块的核心操作是将 $F_{t, t+1}$ 分解为两项：

- **相机流** $F_{t, t+1}^C$：假设场景静止，仅由相机位姿变化引起的像素位移。利用当前帧的渲染深度 $D_t$、相机内参 $K_t$ 和外参 $T_t$，将像素点 $p_t$ 反投影至 3D 空间得到 $x_t$，再通过 $C_{t+1}$ 的相机参数重投影至 $I_{t+1}$，位移量即为相机流。
- **运动流** $F_{t, t+1}^M$：从光流中减去相机流后剩余的部分，仅反映物体自身运动。

这一解耦过程（**Figure 3** 给出示意）使得后续监督信号排除了相机运动的干扰，为高斯变形提供了纯粹的 2D 运动先验。

### 3D 数据流：高斯变形与流监督

3D 数据流以规范空间中的 3D 高斯为起点。对于时刻 $t$，变形网络 $\mathscr{D}$ 根据时间编码预测每个高斯的位置、旋转、缩放的残差：

$$(\mu + \Delta\mu,\; r + \Delta r,\; s + \Delta s) = \mathscr{D}(\mu, r, s, t)$$

变形后的高斯经可微光栅化器渲染出 $t+1$ 时刻的图像 $\hat{I}_{t+1}$，并与真实图像计算光度损失 $\mathcal{L}_{\text{baseline}}$。

同时，为建立 2D 运动先验与 3D 变形之间的桥梁，MotionGS 引入了 **高斯流** $F_{t, t+1}^G$ 的概念——将 $t$ 时刻高斯的对应空间点变换到 $t+1$ 时刻的变形高斯空间，其在 2D 平面上的投影位移即描述了该高斯的变形在图像上的表现（详细推导见 **Figure 9**）。高斯流通过 L1 损失直接与运动流对齐：

$$\mathcal{L}_{\text{flow}} = \| \text{sg}(F_{t, t+1}^M) - F_{t, t+1}^G \|$$

其中 $\text{sg}$ 表示停止梯度，防止运动流估计被反向传播干扰。总损失为：

$$\mathcal{L} = \mathcal{L}_{\text{baseline}} + \lambda \mathcal{L}_{\text{flow}}$$

### 相机位姿细化模块

上述两条数据流均依赖相机位姿的准确性。MotionGS 在相对位姿 $T_{t \to t+1}$ 上叠加可学习的 SE(3) 残差 $\Delta T$，并在训练中交替执行两步（**Figure 4**）：冻结高斯属性，仅通过光度损失反向传播更新 $\Delta T$；随后冻结位姿残差，正常优化高斯场与变形网络。这一交替机制有效缓解了 COLMAP 初始位姿不准确带来的误差累积，使模型在动态场景下更具鲁棒性。

### 模块间关系总结

| 模块 | 输入 | 输出 | 下游依赖 |
|------|------|------|----------|
| 光流估计网络 (GMFlow) | $I_t, I_{t+1}$ | 光流 $F_{t, t+1}$ | 光流解耦模块 |
| 光流解耦模块 | $F_{t, t+1}$，渲染深度 $D_t$，相机位姿 | 运动流 $F_{t, t+1}^M$ | 流监督损失 |
| 变形网络 $\mathscr{D}$ | 规范高斯 + 时间 $t$ | 变形后的高斯属性 | 高斯流渲染器、图像渲染器 |
| 高斯流渲染器 | 变形前后的高斯 | 高斯流 $F_{t, t+1}^G$ | $\mathcal{L}_{\text{flow}}$ |
| 相机位姿细化模块 | 初始位姿 + 光度梯度 | 优化后的位姿残差 | 光流解耦、图像渲染 |

整体而言，2D 流为 3D 变形提供了显式、解耦的运动约束，而位姿细化模块则从源头降低了误差传播，三者形成闭环，共同提升了动态场景重建的精度。



MotionGS 在可变形 3DGS 基线（**Deformable-3DGS**, Yang et al., arXiv 2023）之上引入两个关键模块：**光流解耦模块** 和 **相机位姿细化模块**，并定义了高斯流的渲染与监督机制。

### 光流解耦模块

该模块的核心目标是从混合的光流中剥离相机运动成分，得到仅由物体运动引起的 **运动流**，以此作为 3D 高斯变形的显式监督信号。

给定相邻帧 $I_t$ 和 $I_{t+1}$，首先通过预训练光流网络 **GMFlow** 估计前向光流 $F_{t, t+1}$。随后，利用渲染深度和相机位姿计算 **相机流** $F_{t, t+1}^C$——即假设场景完全静止时仅由相机运动引起的光流：

$$F_{t, t+1}^C = p_t^{t+1} - p_t$$

其中 $p_t$ 为帧 $I_t$ 中的像素坐标，$p_t^{t+1}$ 为该像素对应的 3D 点 $x_t$ 投影到帧 $I_{t+1}$ 后的坐标。3D 点 $x_t$ 通过下式从像素反投影获得：

$$x_t = T_t^{-1} K_t^{-1} D_t \tilde{p}_t$$

这里 $D_t$ 为渲染深度，$K_t$ 为相机内参，$T_t$ 为相机外参（世界到相机变换），$\tilde{p}_t$ 为齐次像素坐标。

**运动流** $F_{t, t+1}^M$ 即原始光流减去相机流：

$$F_{t, t+1}^M = F_{t, t+1} - F_{t, t+1}^C$$

该运动流仅反映物体自身的运动，消除了相机自运动带来的歧义。

### 高斯流渲染与监督

为将 2D 运动流与 3D 高斯变形关联，MotionGS 引入 **高斯流** $F_{t, t+1}^G$ 的概念：它描述 3D 高斯从 $t$ 时刻到 $t+1$ 时刻的位移在 2D 图像平面上的投影。具体而言，对于第 $i$ 个高斯，将其在 $t$ 时刻对应的空间点 $x_t$ 先投影到规范高斯空间，再从规范空间重投影到 $t+1$ 时刻的该高斯上，由此得到 2D 位移。

变形网络 $\mathscr{D}$ 根据时间 $t$ 预测 3D 高斯的位置、旋转、缩放残差：

$$(\mu + \Delta \mu, r + \Delta r, s + \Delta s) = \mathscr{D}(\mu, r, s, t)$$

高斯流通过在高斯可微光栅化器中新增的渲染通道获得，其监督损失为 L1 距离，且对运动流停止梯度：

$$\mathcal{L}_{\mathrm{flow}} = \| sg(F_{t, t+1}^M) - F_{t, t+1}^G \|$$

### 相机位姿细化模块

基线方法直接使用 COLMAP 估计的固定相机位姿，在动态场景中位姿误差会累积并损害重建质量。MotionGS 在相邻帧的相对位姿上引入可学习的 SE(3) 残差 $\Delta T$，交替优化高斯场与相机位姿：优化位姿时冻结所有 3D 高斯属性，通过光度损失反向传播更新残差；优化高斯时则冻结位姿残差。该交替策略提升了训练稳定性与动态场景的鲁棒性。

### 总损失

最终训练损失为基线光度损失与加权流损失之和：

$$\mathcal{L} = \mathcal{L}_{\mathrm{baseline}} + \lambda \mathcal{L}_{\mathrm{flow}}$$

其中 $\lambda$ 为流损失权重，在 NeRF-DS 数据集上设为 0.5，在 HyperNeRF 上设为 0.1。



## 实验与关键发现

### 定量主结果

MotionGS 在两个主流动态场景基准上均取得最优性能。在 **NeRF-DS** 数据集（Table 1）上，MotionGS 的 PSNR 均值达到 **24.54**，较基线 **Deformable-3DGS**（Yang et al., arXiv 2023）的 23.61 提升 **+0.93 dB**；SSIM 从 0.8394 提升至 **0.8656**，LPIPS 从 0.1970 降至 **0.1719**。在 **HyperNeRF** 的 vrig 子集（Table 2）上，PSNR 从 22.5 提升至 **24.8**（+2.3 dB），SSIM 从 0.61 提升至 **0.69**（+0.08），表明方法对复杂拓扑变化场景同样有效。

![[assets/figures/papers/paper_list_l11_MotionGS_Exploring_Explicit_Motion_Guidance_for_Deformable_3D_Gaussian_S/figures/004_Table_1.jpg]]
*Table 1: Quantitative comparison on NeRF-DS dataset per-scene. We highlight the best and the second best results in each scene. NeRF-DS and HyperNeRF employ MS-SSIM and LPIPS with the AlexNet, while other methods and ours use SSIM and LPIPS with the VGG network*

![[assets/figures/papers/paper_list_l11_MotionGS_Exploring_Explicit_Motion_Guidance_for_Deformable_3D_Gaussian_S/figures/005_Table_2.jpg]]
*Table 2: Quantitative comparison on HyperNeRF’s vrig dataset per-scene*

需注意公平性限制：NeRF-DS 和 HyperNeRF 方法使用基于 AlexNet 的 LPIPS，而 MotionGS 及其他对比方法使用基于 VGG 的 LPIPS，因此 LPIPS 数值不完全可比（Table 1 注释）。所有方法在相同分辨率、相同训练/测试划分下评测。

### 核心消融：瓶颈验证

Table 3 的消融实验直接验证了核心因果机制：

![[assets/figures/papers/paper_list_l11_MotionGS_Exploring_Explicit_Motion_Guidance_for_Deformable_3D_Gaussian_S/figures/006_Table_3.jpg]]
*Table 3: Ablations on the key components of our proposed framework*

1. **直接光流监督有害**：在基线 Deformable-3DGS 上直接添加未经解耦的光流监督，PSNR 从 23.61 降至 **23.37**。这证实了光流中混合的相机运动成分会引入歧义噪声，干扰高斯变形优化。

2. **运动流监督是关键提升点**：使用解耦后的运动流作为监督信号，PSNR 跃升至 **24.12**（+0.51 dB），证明剥离相机运动后的纯净对象运动先验能有效引导高斯变形。

3. **位姿细化叠加增益**：在运动流监督基础上启用相机位姿细化模块，PSNR 进一步提升至 **24.54**（+0.42 dB），表明交替优化高斯场与相机位姿可减少位姿不准造成的累积误差。

### 框架选择消融

Table 7 揭示了方法各设计选择的影响（公平起见，该消融未启用位姿细化模块）：

![[assets/figures/papers/paper_list_l11_MotionGS_Exploring_Explicit_Motion_Guidance_for_Deformable_3D_Gaussian_S/figures/016_Table_7.jpg]]
*Table 7: Ablations on other choices of our proposed framework. For fair comparison, we do not activate the proposed camera pose refinement module during training*

- **运动掩膜至关重要**：移除运动掩膜后 PSNR 从 24.12 骤降至 **23.13**，说明静态区域的光流估计误差会严重干扰运动流监督的质量。
- **深度来源敏感**：用单目深度估计器 MiDas 替代渲染深度导致性能下降，原因是 MiDas 的尺度与场景不一致（见 Figure 10）。渲染深度因与场景几何自洽而更具优势。
- **光流估计器选择影响显著**：更换为 FlowFormer 或 MDFlow 等不同光流网络会改变最终性能，表明运动先验的准确性直接决定方法上限。
- **自监督光流损失可行但次优**：自监督光流损失可超越基线，但不及所提的显式运动流监督，可作为无现成光流估计器时的备选方案。
- **损失权重**：光流损失权重 λ=0.5 在 NeRF-DS 上取得最佳平衡。

### 效率与资源

Table 4-6 给出了训练时间、GPU 内存占用、FPS 及存储量的对比。MotionGS 在引入运动监督和位姿细化后，训练开销相比基线 Deformable-3DGS 有所增加，但仍保持在可接受范围。具体数值需查阅原表确认。

![[assets/figures/papers/paper_list_l11_MotionGS_Exploring_Explicit_Motion_Guidance_for_Deformable_3D_Gaussian_S/figures/012_Table_4.jpg]]
*Table 4: Training time comparison across different models*

### 定性分析

Figure 5 和 Figure 6 分别展示了 NeRF-DS 和 HyperNeRF 数据集上的定性对比。在 plate 场景中，MotionGS 能准确渲染运动盘面的反射和锐利边缘，同时显著减少漂浮伪影等视觉失真。Figure 7 可视化了光流、相机流、运动流和高斯流的解耦过程，直观验证了运动流对对象运动的精确刻画。Figure 8 对比了优化前后的相机轨迹，显示位姿细化模块能修正 COLMAP 初始估计的偏差。

### 失败模式

方法在 **DyNeRF** 数据集上出现明显失败（Figure 11）。由于该数据集视角固定且稀疏，渲染深度不准确，导致相机流计算产生较大误差，进而使运动流监督失效，最终产生漂浮伪影。这一失败模式揭示了方法对渲染深度质量的强依赖：当深度估计不准时，光流解耦的整个链条会崩溃。

### 局限性

1. **依赖 COLMAP 初始位姿**：方法无法完全摆脱外部相机位姿估计，对静态特征不足或物体运动极小的场景，位姿优化可能不稳定。
2. **稀疏视角失效**：如 DyNeRF 所示，固定稀疏视角下渲染深度不可靠，导致方法性能退化。
3. **光流估计器依赖**：运动先验的质量受限于所选光流网络，更换估计器会直接影响最终效果。

### 补充图表

![[assets/figures/papers/paper_list_l11_MotionGS_Exploring_Explicit_Motion_Guidance_for_Deformable_3D_Gaussian_S/figures/001_Figure_1.jpg]]
*Figure 1: (a) Gaussian flow under different supervision. We model Gaussian flow under the supervision of optical flow and motion flow respectively. The latter can produce a more direct description of object motion, thereby effectively guiding the deformation of 3D Gaussians. (b) The decoupling of optical flow. We decouple the optical flow into motion flow which is only related to object motion and camera flow which is only related to camera motion*

![[assets/figures/papers/paper_list_l11_MotionGS_Exploring_Explicit_Motion_Guidance_for_Deformable_3D_Gaussian_S/figures/013_Table_5.jpg]]
*Table 5: Max GPU memory usage comparison across different models*

![[assets/figures/papers/paper_list_l11_MotionGS_Exploring_Explicit_Motion_Guidance_for_Deformable_3D_Gaussian_S/figures/014_Table_6.jpg]]
*Table 6: FPS, number of 3D Gaussians and storage on the NeRF-DS dataset per scene*



## 定位与知识库关联

### 方法在动态场景重建中的定位

MotionGS 处于**可变形 3D 高斯溅射**（Deformable 3DGS）的技术路线上，其直接基线为 **Deformable-3DGS**（Yang et al., arXiv 2023），后者通过在标准 3D-GS（Kerbl et al., TOG 2023）基础上引入一个以时间 $t$ 为条件的变形网络 $\mathscr{D}$，预测高斯的位移、旋转和缩放残差：

$$( \mu + \Delta \mu , r + \Delta r , s + \Delta s ) = \mathscr { D } ( \mu , r , s , t )$$

然而，该基线仅依赖光度重建损失，缺乏对物体运动本身的任何显式约束。这构成了核心瓶颈：在物体运动不规则或动态复杂的场景中，仅靠颜色监督优化高维变形空间极易陷入局部最优。MotionGS 的关键突破在于**将运动先验从“隐式副产品”升级为“显式监督信号”**，并且通过光流解耦消除了相机运动带来的噪声。

### 与同类方法的关系

在动态场景重建的更大版图中，MotionGS 与以下方法形成对比或互补：

- **基于 NeRF 的动态方法**：**HyperNeRF**（Park et al., ICCV 2021）通过在高维空间中建模场景来处理拓扑变化，**NeRF-DS**（Yan et al., CVPR 2023）针对动态高光物体引入表面变形场，**TiNeuVox**（Fang et al., SIGGRAPH Asia 2022）则采用神经体素加速动态 NeRF。这些方法在渲染质量上各有优势，但均受限于 NeRF 的体积渲染开销，且缺乏对运动本身的显式建模。MotionGS 在 NeRF-DS 和 HyperNeRF 数据集上全面超越这些方法（Table 1, Table 2），同时继承了 3DGS 的实时渲染能力。

- **基于光流辅助的 3DGS 方法**：部分同期工作尝试引入光流来辅助动态 3DGS 训练，但直接使用未解耦的光流作为监督信号。MotionGS 的消融实验（Table 3）明确揭示了这一做法的危害：直接光流监督使 PSNR 从基线 23.61 降至 23.37，因为混合了相机与物体运动的光流引入了歧义性监督。这一负向结果本身就是对后续工作的重要警示。

- **与相机位姿联合优化的方法**：MotionGS 的相机位姿细化模块在相对位姿上添加可学习的 SE(3) 残差，交替冻结高斯属性后通过光度损失反向传播更新位姿。这一设计与 SLAM 导向的 3DGS 方法（如 MonoGS）共享“联合优化场景与位姿”的思想，但 MotionGS 的动机是提升动态场景重建质量而非实现定位，且仍依赖 COLMAP 提供初始位姿。

### 适用边界与局限

1. **稀疏固定视角场景失效**：在 DyNeRF 数据集上，由于相机视角固定且稀疏，渲染深度不准确导致相机流计算误差，进而使运动流失效，最终产生漂浮伪影（Figure 11）。这表明方法的运动解耦机制对深度质量高度敏感，在稀疏视角下缺乏足够的几何约束。

2. **依赖外部相机位姿初始化**：尽管位姿细化模块可以在训练过程中校正 COLMAP 的位姿误差（Figure 8 展示了优化前后轨迹的改善），但方法无法完全摆脱对外部位姿估计的依赖。对于静态特征不足或物体运动极小的场景，位姿优化可能不稳定。

3. **运动先验的准确性依赖光流估计器**：消融实验（Table 7）表明，将 GMFlow 替换为 FlowFormer 或 MDFlow 等不同光流网络会导致性能波动，说明运动先验的准确性对最终重建质量有直接影响。自监督光流损失虽可超越基线，但仍不及使用现成光流估计器的方案。

4. **静态区域光流误差的干扰**：移除运动掩膜后 PSNR 从 24.12 降至 23.13（Table 7），说明静态区域的光流估算误差会严重干扰运动流监督。方法需要通过运动掩膜来过滤这些噪声，而掩膜本身的质量又成为一个隐式依赖。

### 开放问题

1. **无位姿动态 3DGS 的可行性**：论文在结论中明确提出未来目标是开发完全不依赖相机位姿输入的动态 3DGS 方法。这需要同时解决场景几何、运动估计和相机位姿的联合初始化问题，是一个开放且极具挑战的方向。

2. **更鲁棒的通用运动先验**：当前方法依赖现成光流网络（GMFlow）提供运动先验，在极小运动或纹理缺失场景中光流估计本身可能失败。如何构建更稳定、通用的运动先验（如改进自监督流损失、融合多帧时序信息）是提升方法鲁棒性的关键。

3. **方法模块的可迁移性**：论文指出光流解耦和位姿细化模块不依赖于特定的变形网络设计，可应用于类似的变形基 3DGS 方法。这一主张的实际迁移效果和泛化范围尚待后续工作验证。



## 原文 PDF

![[paperPDFs/NEURIPS_2024/MotionGS_Exploring_Explicit_Motion_Guidance_for_Deformable_3D_Gaussian_Splatting.pdf]]
