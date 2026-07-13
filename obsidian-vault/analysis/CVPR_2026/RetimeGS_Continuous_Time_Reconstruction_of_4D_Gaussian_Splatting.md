---
title: "RetimeGS: Continuous-Time Reconstruction of 4D Gaussian Splatting"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/RetimeGS_Continuous_Time_Reconstruction_of_4D_Gaussian_Splatting.pdf
project_link: "https://william-wang2.github.io/RetimeGS/"
code_link: null
aliases:
- RetimeGS
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
- topic/benchmarks_datasets_evaluation
core_operator: 通过短尾双sigmoid时间不透明度强制每组基元覆盖相邻两帧及其间隔；利用双向光流监督Catmull-Rom样条轨迹，提供平滑且一致的基元运动；结合三重渲染、动态拉伸与重定位策略，确保静态区域压缩冗余、动态区域获得足够基元预算。
primary_logic: 显式正则化时间不透明度并约束基元轨迹为样条，在保留对动态外观与可见性变化建模能力的前提下消除时间混叠，使4DGS能够可靠地插值任意中间帧。
claims:
- 强制一组基元同时解释相邻两个输入帧及其间隔，避免时间不透明度坍缩到单帧（短尾时间不透明度）。
- 使用 Catmull-Rom 样条建模空间轨迹，参数由双向光流监督，确保轨迹一致性。
- 三重渲染策略要求每组基元独立解释其对应输入帧，避免相邻基元组覆盖不均导致的欠重建。
- Stage-Capture Dataset 上 PSNR ↑ = 30.08
---

# RetimeGS: Continuous-Time Reconstruction of 4D Gaussian Splatting

> [!tip] 核心洞察
> 显式正则化时间不透明度并约束基元轨迹为样条，在保留对动态外观与可见性变化建模能力的前提下消除时间混叠，使4DGS能够可靠地插值任意中间帧。

| 字段 | 内容 |
|------|------|
| 中文题名 | RetimeGS: 连续时间4D高斯溅射重建 |
| 英文题名 | RetimeGS: Continuous-Time Reconstruction of 4D Gaussian Splatting |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2603.13783) · [Project](https://william-wang2.github.io/RetimeGS/) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction #topic/benchmarks_datasets_evaluation |
| Method | RetimeGS |
| Dataset | Stage-Capture Dataset, Neural3DV |

> [!tip] 效果简介
> - Stage-Capture Dataset 上，PSNR ↑ 30.08 vs Deform-GS (28.45) (+1.63)；SSIM ↑ 0.904 vs Deform-GS (0.867) (+0.037)；LPIPS ↓ 0.0225 vs Deform-GS (0.0272) (-0.0047)。
> - Neural3DV (Flame Steak & Flame Salmon) 上，PSNR ↑ 33.22 vs Deform-GS (31.79) (+1.43)；SSIM ↑ 0.959 vs Deform-GS (0.952) (+0.007)；LPIPS ↓ 0.074 vs Deform-GS (0.081) (-0.007)。

## 概要

动态场景的4D重建是计算机视觉中的核心挑战，尤其在输入视频帧率稀疏且运动幅度较大时，现有方法难以可靠地合成任意中间时刻的视图。**RetimeGS** 针对这一瓶颈，提出了一种连续时间4D高斯溅射（4DGS）表示，通过显式正则化时间不透明度并约束基元轨迹为样条，消除了时间混叠伪影，实现了对任意中间帧的高质量插值。

### 问题瓶颈

现有基于4D基元的方法（如 **STGS**、**GaussianFlow**、**Ex4DGS**）将时间不透明度建模为无正则化的1D高斯分布。这种表示倾向于过拟合离散输入帧——时间不透明度坍缩到单帧附近，导致在中间帧渲染时出现鬼影伪影（时间混叠）。同时，快速运动下缺少精确的轨迹估计，使基元接收不一致的监督，无法学习可靠的帧间对应关系。

### 核心思路

RetimeGS 通过三个关键设计解决上述问题：

1. **短尾时间不透明度**：将时间不透明度建模为两个边界感知sigmoid函数的乘积，强制每组基元覆盖相邻两帧及其间隔，从根本上阻止时间不透明度坍缩到单帧。
2. **样条轨迹与双向光流监督**：使用Catmull-Rom样条建模基元空间轨迹，参数由双向光流监督，提供平滑且一致的基元运动。
3. **三重渲染与动态拉伸**：三重渲染损失确保每组基元独立解释其对应输入帧；动态拉伸与重定位策略压缩静态区域冗余，将更多基元预算分配给困难的重建区域。

### 方法定位

在4DGS方法谱系中，RetimeGS 属于**4D基元方法**，但区别于 **Deform-GS**（基于变形场，使用单一基元集）和 **STGS**（无正则化时间不透明度）。其核心创新在于将时间不透明度正则化与样条轨迹显式结合，配合光流监督，在保留对动态外观与可见性变化建模能力的前提下消除时间混叠。

### 主要结果

在 **Stage-Capture** 数据集上，RetimeGS 在仅评估前景区域的设定下取得 **PSNR 30.08 dB**，较 Deform-GS（28.45 dB）提升 **+1.63 dB**；SSIM 从 0.867 提升至 **0.904**，LPIPS 从 0.0272 降至 **0.0225**。在 **Neural3DV** 火焰场景上，PSNR 达到 **33.22 dB**，较 Deform-GS（31.79 dB）提升 **+1.43 dB**。消融实验证实，移除光流组件会导致纹理扭曲，取消三重渲染则使相邻基元组各自仅捕获部分内容，而样条轨迹相比线性轨迹产生更平滑的运动。

### 局限

当帧间运动过大或帧率极低时，现有光流估计器无法提供可靠对应，中间帧插值仍会出现明显伪影。此外，相邻动态基元组本质上的不连续性会在离散输入帧处引入轻微闪烁。

### 动态场景重建的4DGS范式

3D Gaussian Splatting（3DGS）在静态场景的新视角合成中取得了显著成功，其显式点基元表示兼具高保真渲染与实时性能。将这一范式扩展到动态场景——即4D Gaussian Splatting（4DGS）——成为近期研究热点。现有4DGS方法大致分为两类：**基于变形的方案**（如 **Deform-GS**）使用单一基元集并通过变形场驱动其运动；**4D基元方案**（如 **STGS**、**GaussianFlow**、**Ex4DGS**）则为每个基元显式赋予时间维度参数，使其在时空域中直接表示动态内容。

### 核心瓶颈：时间过拟合与时间混叠

尽管4D基元方法在概念上更直接，但其面临一个根本性问题——**时间不透明度的过拟合**。现有方法（STGS、GaussianFlow、Ex4DGS）通常使用未经正则化的1D高斯函数对基元的时间活跃度建模。这种设计允许每个基元的时间不透明度坍缩到单一输入帧附近，导致基元仅“记住”离散的输入帧，而无法学习帧间的连续运动。

其直接后果是**时间混叠**（temporal aliasing）——在渲染中间帧时出现明显的鬼影伪影（ghosting artifacts），如 Figure 2 所示。这是因为相邻帧的基元集彼此独立，在中间时间戳缺乏一致的对应关系，使得渲染结果成为两组不相关基元的混合，而非真实的运动插值。

### 轨迹估计的缺失

与时间不透明度问题相互交织的是**轨迹估计的不足**。在快速非刚性运动场景中，基元需要在帧间进行大幅位移。然而，现有方法要么仅使用简单的线性速度假设，要么完全依赖隐式变形场，缺乏对基元空间轨迹的显式、平滑约束。这使得基元在帧间接收不一致的监督信号，难以学习可靠的对应关系，进一步加剧了中间帧的重建误差。

### 静态区域冗余与动态区域欠采样

另一个常被忽视的问题是基元预算的分配失衡。在包含大量静态区域的场景中，静态背景被多个独立的基元组重复表示，造成严重冗余；而快速运动的动态区域却因基元预算不足而欠重建。现有方法缺乏机制来识别静态区域并压缩冗余，同时将释放的基元资源重新分配给高动态区域。

### 本文动机

综上所述，现有4DGS方法在**中间帧插值**这一核心能力上存在系统性缺陷，根源在于三个相互关联的问题：

1. **时间不透明度缺乏正则化**，导致基元过拟合离散输入帧；
2. **空间轨迹缺乏平滑约束与显式监督**，导致运动估计不可靠；
3. **基元预算分配失衡**，静态区域冗余而动态区域欠采样。

RetimeGS 针对上述三个缺口，提出了一套协同设计的解决方案：通过短尾双sigmoid时间不透明度强制每组基元覆盖相邻两帧及其间隔；利用双向光流监督的Catmull-Rom样条建模平滑轨迹；配合动态拉伸与重定位策略优化基元预算分配。这些设计共同使4DGS能够可靠地插值任意中间帧，即使在大幅帧间运动下也能保持高保真渲染。

## 核心方法与创新机理

RetimeGS 的核心创新在于对 4D 高斯溅射（4DGS）的时间表示和运动轨迹进行显式正则化，从根本上解决现有方法因时间过拟合导致的中间帧鬼影伪影问题。具体而言，该方法在三个关键维度上改进了 4DGS 的表示与训练策略。

### 短尾时间不透明度：强制基元覆盖相邻帧

现有 4D 基元方法（如 STGS、GaussianFlow、Ex4DGS）采用无正则化的 1D 高斯时间不透明度，基元可以自由坍缩到单一输入帧，导致在中间时间戳出现鬼影（Figure 2）。RetimeGS 将时间不透明度重新设计为两个边界感知 sigmoid 函数的乘积：

$$
\sigma_{\tau}(t) = \tilde{\psi}_l\left( \frac{t - (\mu_{\tau} - \tau_l)}{\gamma} \right) \tilde{\psi}_r\left( \frac{(\mu_{\tau} + \tau_r) - t}{\gamma} \right)
$$

这一短尾设计强制每组基元同时覆盖相邻两个输入帧及其间隔，初始时间窗口宽度约为 $\Delta t / 2$。在视频时间边界处，边界感知 sigmoid $\tilde{\psi}_s(x)$ 自动替换为 1，防止边界帧的不透明度下降。该机制从表示层面消除了时间混叠的根源，使基元无法过拟合到单个离散帧。

### Catmull-Rom 样条轨迹：平滑且可监督的运动建模

基线方法多采用线性速度或无轨迹建模，在快速运动下缺乏精确的对应关系。RetimeGS 使用 Catmull-Rom 样条对基元空间轨迹进行参数化，通过三个速度分量 $(v_1, v_2, v_3)$ 定义四个控制点：

内部控制点（对应 $t_i$ 和 $t_{i+1}$ 时刻的位置）：
$$
\pmb{p}_{1,p} = \pmb{\mu}_p - \frac{1}{2} \Delta t \cdot \pmb{v}_{2,p}, \qquad \pmb{p}_{2,p} = \pmb{\mu}_p + \frac{1}{2} \Delta t \cdot \pmb{v}_{2,p}
$$

外部控制点（决定样条曲率）：
$$
\pmb{p}_{0,p} = \pmb{p}_{1,p} - \Delta t \cdot \pmb{v}_{1,p}, \qquad \pmb{p}_{3,p} = \pmb{p}_{2,p} + \Delta t \cdot \pmb{v}_{3,p}
$$

这些参数通过双向光流进行监督，确保基元轨迹在帧间平滑一致。消融实验证实，用样条轨迹替代线性轨迹可产生更平滑的运动，避免分段线性伪影（Figure 7）。

### 三重渲染与动态资源分配

为配合上述表示，RetimeGS 设计了三个协同的训练策略：

1. **三重渲染监督**：在每个内部帧 $t_i$ 同时渲染三张图像——使用所有基元、仅用前一子集、仅用后一子集——并均以真实图像监督。这迫使每组基元独立解释其对应的输入帧，避免相邻基元组覆盖不均导致的欠重建（Figure 5b）。

2. **动态拉伸与重定位**：检测静态基元并周期性拉伸其时间边界 $\tau_l$ 和 $\tau_r$ 至 $(1/2 + k)\Delta t$，同时按采样分数 $s = \sigma / (\tau_l + \tau_r)$ 将低不透明度基元重定位到高采样区域。在 1M 基元预算下，该策略将静态基元压缩至约 88K，有效基元数降低 2.26 倍，将更多预算分配给动态区域。

3. **流感知初始化**：利用 VGGT 点云和双向光流反投影估计初始速度和伪均值，为优化提供良好的起点。

这些 changed slots 共同构成一个闭环：时间不透明度正则化消除过拟合，样条轨迹提供平滑运动先验，三重渲染和动态资源分配确保训练信号的一致性和基元预算的高效利用。

RetimeGS 的核心设计思路是通过**正则化时间不透明度**与**样条轨迹建模**，从根本上消除现有 4DGS 方法在中间帧渲染时出现的时间混叠（鬼影）伪影。整体 pipeline 由四个紧密协作的模块构成，输入为多视角视频与双向光流，输出为可在任意连续时刻渲染高质量图像的 4D 场景表示。

### 输入与预处理

系统的输入包括两部分：
- **多视角视频张量** $\mathbf{V} \in \mathbb{R}^{C \times T \times H \times W \times 3}$，来自 $C$ 个同步相机在 $T$ 个离散时间步的 RGB 帧；
- **多视角双向光流** $\mathbf{F}^{\mathrm{fwd}} \in \mathbb{R}^{C \times (T-1) \times H \times W \times 2}$ 及对应的后向光流，由预训练光流估计器（默认 WAFT）离线计算得到。

在初始化阶段，系统利用 VGGT 从第一帧重建稀疏 3D 点云，随后将所有视图的 2D 光流反投影至 3D 空间并取平均，估计出前向与后向 3D 流。这些 3D 流的均值被用于初始化所有基元的速度分量 $\mathbf{v} = (\mathbf{v}_1, \mathbf{v}_2, \mathbf{v}_3)$，而相邻帧间基元的伪均值 $\boldsymbol{\mu}$ 则通过将对应时刻的点云沿估计速度位移来近似（流感知初始化）。

### 核心模块关系

整个 pipeline 的数据流与模块协作关系如 Figure 3 所示，可概括为以下四个关键环节：

![[assets/figures/papers/paper_list_l2091_https_arxiv_org_abs_2603_13783/figures/003_Figure_3.jpg]]
*Figure 3: Pipeline Overview. We represent a dynamic scene using a novel 4D representation that combines regularized temporal opacity with smooth spline-based spatial positioning. By leveraging tailored training strategies using RGB images and bidirectional optical flow, our method can reconstruct arbitrary intermediate frames under sparse temporal sampling and large motion*

**1. 4D 基元表示构建**

在 3DGS 基础上，每个高斯基元被扩展为包含时间维度参数的 4D 表示：
$$( \mu_{\tau}, \tau_l, \tau_r, \boldsymbol{\mu}, \mathbf{v}, \mathbf{s}, \mathbf{q}(t), h, \sigma )$$
其中 $\mu_{\tau}$ 为时间均值，$\tau_l$ 和 $\tau_r$ 为时间不透明度的左右边界，$\boldsymbol{\mu}$ 为空间伪均值，$\mathbf{v}$ 为速度分量，$\mathbf{q}(t)$ 为时变旋转四元数。这一参数化使得每组基元被约束在相邻两帧及其间隔区间内活跃。

**2. 正则化时间不透明度**

时间不透明度 $\sigma_{\tau}(t)$ 被显式建模为两个边界感知 sigmoid 函数的乘积：
$$\sigma_{\tau}(t) = \tilde{\psi}_l\left( \frac{t - (\mu_{\tau} - \tau_l)}{\gamma} \right) \tilde{\psi}_r\left( \frac{(\mu_{\tau} + \tau_r) - t}{\gamma} \right)$$
该设计的**短尾特性**强制基元仅在指定的时间窗口内贡献不透明度，并在窗口边界处平滑衰减至零。在视频首尾帧处，边界感知机制将对应侧的 sigmoid 替换为常数 1，避免边界帧不透明度下降。这一正则化直接解决了现有方法中时间不透明度可坍缩到单帧、导致中间帧出现鬼影的问题（Figure 2）。

**3. 样条轨迹建模与双向光流监督**

基元在相邻两帧间的空间轨迹采用 Catmull-Rom 样条建模。给定伪均值 $\boldsymbol{\mu}$ 与区间速度 $\mathbf{v}_2$，内部控制点（对应 $t_i$ 和 $t_{i+1}$ 时刻的位置）定义为：
$$\mathbf{p}_{1,p} = \boldsymbol{\mu}_p - \frac{1}{2} \Delta t \cdot \mathbf{v}_{2,p}, \qquad \mathbf{p}_{2,p} = \boldsymbol{\mu}_p + \frac{1}{2} \Delta t \cdot \mathbf{v}_{2,p}$$
外部控制点（决定曲线曲率）则由相邻区间的速度分量 $\mathbf{v}_1$ 和 $\mathbf{v}_3$ 确定：
$$\mathbf{p}_{0,p} = \mathbf{p}_{1,p} - \Delta t \cdot \mathbf{v}_{1,p}, \qquad \mathbf{p}_{3,p} = \mathbf{p}_{2,p} + \Delta t \cdot \mathbf{v}_{3,p}$$

这些控制点对应的 2D 投影流被双向光流监督，确保轨迹在时间上平滑一致，避免线性模型带来的分段伪影。

**4. 三重渲染与动态资源分配**

在每个内部帧 $t_i \in \{2, \dots, T-1\}$，系统执行三重渲染：
- 使用**所有基元**渲染完整图像；
- 使用**前一组基元**（时间窗口覆盖 $t_{i-1}$ 至 $t_i$）单独渲染；
- 使用**后一组基元**（时间窗口覆盖 $t_i$ 至 $t_{i+1}$）单独渲染。

三幅渲染图像均受 $t_i$ 时刻的真值监督。这一策略强制每组基元独立解释其覆盖的输入帧，避免相邻基元组覆盖不均导致的欠重建（消融实验证实，取消三重渲染时两组基元各只捕获部分内容，Figure 5b）。

此外，系统周期性检测静态基元（速度近零且不透明度高），将其时间边界 $\tau_l$ 和 $\tau_r$ 拉伸至 $(1/2 + k)\Delta t$，使单个基元跨越多帧。同时，低不透明度基元按采样分数 $s = \frac{\sigma}{\tau_l + \tau_r}$ 被重定位到动态区域。这一动态拉伸与重定位策略将静态基元数量压缩至约 88K（占总数的 9%），使有效基元数降低 2.26 倍，从而将更多基元预算分配给困难的重建区域。

### 训练与推理流程

训练时，所有模块联合优化，损失函数由三部分组成：三重渲染的 RGB 损失（L1 + SSIM）、双向光流轨迹监督损失，以及必要的正则化项。推理时，对于任意目标时刻 $t$，系统根据各基元的时间不透明度权重与样条插值位置，通过标准高斯溅射管线渲染出对应帧。

### 已知局限

当帧间运动过大或帧率极低（光流位移超过约 50 像素）时，光流估计器无法提供可靠对应，导致中间帧插值出现明显伪影（Figure 8）。此外，由于相邻动态基元组本质上是两组独立的基元集合，在离散输入帧处仍可能出现轻微闪烁伪影。

### 4D基元表示

RetimeGS 将 3DGS 的静态基元扩展为可描述动态场景的 4D 基元，每个基元 $p$ 的参数为：

$$( \mu_{\tau}, \tau_l, \tau_r, \mu, v, s, q(t), h, \sigma )$$

其中 $\mu_{\tau}$ 为时间均值，$\tau_l$ 和 $\tau_r$ 分别为时间跨度的左右边界，$\mu$ 为伪空间均值（pseudo mean），$v=(v_1,v_2,v_3)$ 为三个速度分量，$s$ 为空间尺度，$q(t)$ 为时间相关的旋转四元数，$h$ 为球谐系数，$\sigma$ 为基础不透明度。基元 $p$ 在时刻 $t$ 对空间位置 $\pmb{x}$ 贡献的有效不透明度为：

$$\sigma_{\tau,p}(t) \sigma_p \exp\bigl( -\frac{1}{2} (\pmb{x} - \pmb{x}_p(t))^{\sf T} \pmb{\Sigma}_p(t)^{-1} (\pmb{x} - \pmb{x}_p(t)) \bigr)$$

其中 $\pmb{x}_p(t)$ 和 $\pmb{\Sigma}_p(t)$ 分别表示基元在时刻 $t$ 的空间位置与协方差矩阵。

---

### 时间不透明度正则化

现有 4D 基元方法（如 STGS、Ex4DGS）的时间不透明度采用无正则化的 1D 高斯分布，训练中易坍缩到单帧，导致中间帧出现鬼影（Figure 2）。RetimeGS 将时间不透明度建模为两个边界感知 sigmoid 函数的乘积，形成短尾（short-tailed）平滑过渡：

$$\sigma_{\tau}(t) = \tilde{\psi}_l\left( \frac{t - (\mu_{\tau} - \tau_l)}{\gamma} \right) \tilde{\psi}_r\left( \frac{(\mu_{\tau} + \tau_r) - t}{\gamma} \right)$$

其中 $\gamma$ 控制过渡锐度。边界感知 sigmoid $\tilde{\psi}_s(x)$ 在视频时间边界处将 sigmoid 替换为 1，防止边界帧不透明度下降：

$$\tilde{\psi}_s(x) = \begin{cases} 1, & \text{if } \begin{cases} \mu_{\tau} - \tau_l < \epsilon, & s = l \\ \mu_{\tau} + \tau_r > t_T - \epsilon, & s = r \end{cases} \\ \psi(x), & \text{otherwise} \end{cases}$$

该设计强制每组基元同时覆盖相邻两个输入帧及其间隔（初始宽度为 $\Delta t/2$），从结构上阻断时间不透明度坍缩到单帧的路径。

---

### Catmull-Rom 样条轨迹

基元的空间轨迹采用 Catmull-Rom 样条建模，由四个控制点 $\pmb{p}_{0,p}$、$\pmb{p}_{1,p}$、$\pmb{p}_{2,p}$、$\pmb{p}_{3,p}$ 定义。内部控制点对应时刻 $t_i$ 和 $t_{i+1}$ 的位置，由伪均值 $\pmb{\mu}_p$ 和区间速度 $\pmb{v}_{2,p}$ 计算：

$$\pmb{p}_{1,p} = \pmb{\mu}_p - \frac{1}{2} \Delta t \cdot \pmb{v}_{2,p}, \qquad \pmb{p}_{2,p} = \pmb{\mu}_p + \frac{1}{2} \Delta t \cdot \pmb{v}_{2,p}$$

外部控制点利用相邻区间的速度 $\pmb{v}_{1,p}$ 和 $\pmb{v}_{3,p}$ 确定样条曲率：

$$\pmb{p}_{0,p} = \pmb{p}_{1,p} - \Delta t \cdot \pmb{v}_{1,p}, \qquad \pmb{p}_{3,p} = \pmb{p}_{2,p} + \Delta t \cdot \pmb{v}_{3,p}$$

轨迹参数由双向光流监督，确保基元运动平滑一致。消融实验证实，用样条替代线性轨迹可消除分段线性伪影，误差热力图显示线性轨迹在物体边缘处产生显著偏差（Figure 7）。

---

### 三重渲染与重定位

**三重渲染**：对于每个内部帧 $t_i \in \{2,\dots,T-1\}$，同时渲染三幅图像——使用全部基元、仅用前一子集、仅用后一子集——并均以 $t_i$ 的真值图像监督。这迫使每个基元子集独立解释其覆盖的输入帧，避免相邻子集覆盖不均导致的欠重建（Figure 5b）。

**重定位采样分数**：为将有限基元预算向动态区域倾斜，定义采样分数：

$$s = \frac{\sigma}{\tau_l + \tau_r}$$

该分数以时间跨度加权基础不透明度，使低不透明度或短时间跨度的基元优先被重定位到高分数区域，提升动态区域重建质量。

![[assets/figures/papers/paper_list_l2091_https_arxiv_org_abs_2603_13783/figures/010_Figure_6.jpg]]
*Figure 6: Ablation on dynamic stretching. The magenta is rendered using static stretched primitives, and the teal is rendered using dynamic primitives (with static background removed)*

## 实验与关键发现

### 核心定量结果

RetimeGS 在 Stage-Capture 数据集上以显著优势超越所有基线方法。**Table 1** 显示，在前景区域评估下，RetimeGS 取得 PSNR **30.08** dB、SSIM **0.904**、LPIPS **0.0225**，相较最强的基于变形的方法 Deform-GS（PSNR 28.45 dB / SSIM 0.867 / LPIPS 0.0272）分别提升 +1.63 dB、+0.037 和 −0.0047。逐场景细分（**Table 3**）表明该优势具有跨场景一致性。

![[assets/figures/papers/paper_list_l2091_https_arxiv_org_abs_2603_13783/figures/004_Table_1.jpg]]
*Table 1: Quantitative comparisons on the Stage-Capture Dataset, focusing on the foreground region. Red and yellow cell colors indicate the best and second-best results, respectively*

![[assets/figures/papers/paper_list_l2091_https_arxiv_org_abs_2603_13783/figures/012_Table_3.jpg]]
*Table 3: Per-scene quantitative comparisons on the Stage-Capture Dataset (foreground region). Higher PSNR/SSIM and lower LPIPS are better*

在 Neural3DV 的 Flame Steak 与 Flame Salmon 场景上（**Table 5**），RetimeGS 同样优于 Deform-GS（PSNR 33.22 vs. 31.79 dB；SSIM 0.959 vs. 0.952；LPIPS 0.074 vs. 0.081），验证了方法对快速不透明度变化（火焰）场景的泛化能力。当将 Ex4DGS 纳入对比时（**Table 4**），RetimeGS 仍保持领先，进一步确认正则化时间不透明度与样条轨迹的有效性。

![[assets/figures/papers/paper_list_l2091_https_arxiv_org_abs_2603_13783/figures/013_Table_4.jpg]]
*Table 4: Quantitative results on the Stage-Capture dataset, including the Ex4DGS baseline*

![[assets/figures/papers/paper_list_l2091_https_arxiv_org_abs_2603_13783/figures/014_Table_5.jpg]]
*Table 5: Quantitative evaluation on the Flame Steak and Flame Salmon scenes from the Neural3DV dataset*

定性对比（**Figure 4**）显示，RetimeGS 在 DNA-Rendering 和 Stage-Capture 数据集上均重建出更清晰的纹理细节与更少的时间伪影，尤其在存在大幅非刚性变形和可见性变化的区域。

### 消融实验：各组件的因果贡献

**Table 2** 汇总了关键组件的消融结果，以下逐一分析其因果机制。

**光流初始化与监督（Flow-related components）**：移除光流初始化及双向光流轨迹监督后，快速运动物体的纹理出现明显扭曲变形（**Figure 5a**）。光流为基元样条控制点提供粗对应监督，缺失该信号导致基元无法学习一致的帧间轨迹，在快速运动区域产生空间错位。定量上，该消融使 PSNR 从 30.08 dB 降至显著更低水平。

**三重渲染（Triple rendering）**：取消三重渲染时，相邻两组基元各自仅捕获其所覆盖输入帧的部分内容——前一组重建右侧纹理，后一组重建左侧纹理，导致中间帧重建不完整（**Figure 5b**）。三重渲染的核心作用是强制每组基元独立解释其对应输入帧，从而避免相邻基元组覆盖不均造成的欠重建。该消融直接损害中间帧的插值质量。

**样条轨迹（Spline trajectory）**：将 Catmull-Rom 样条替换为线性轨迹后，基元运动在输入帧之间出现分段线性伪影，误差热力图（**Figure 7**）显示物体边缘处误差显著增大。样条轨迹利用三个速度分量 $(v_1, v_2, v_3)$ 定义四个控制点，通过曲率连续性产生更平滑的运动，避免了线性假设下的速度突变。

**动态拉伸与重定位（Dynamic stretching & relocation）**：动态拉伸策略周期性地将静态基元的时间边界 $\tau_l, \tau_r$ 扩展至 $(1/2 + k)\Delta t$，使静态区域由少量跨帧基元表示。在 1M 基元预算下，约 **88K** 个基元（占总数的 9%）被识别为静态并拉伸，将有效基元数降低至约 **2.26 倍**（而非原始方法的 T 倍）。这释放了大量基元预算，重定位机制（基于采样分数 $s = \frac{\sigma}{\tau_l + \tau_r}$）将其重新分配到难以重建的动态区域，从而提升动态区域质量（**Figure 6**，品红色为静态拉伸基元，青色为动态基元）。

**光流方法选择**：**Table 6** 对比了 WAFT 与 SEA-RAFT 作为光流监督模块的效果。WAFT 在所有指标上均略优（PSNR 30.08 vs. 29.73 dB；SSIM 0.904 vs. 0.898；LPIPS 0.0225 vs. 0.0253），表明更精确的光流估计对轨迹监督有正向贡献。

### 训练效率

**Table 7** 显示，在共享 1M 基元预算下，RetimeGS 的训练时间与峰值 GPU 显存与 Deform-GS 和 STGS 相当或更优。动态拉伸通过压缩静态冗余有效降低了等效基元数量，使得表示在保持表达能力的同时具备计算效率。

### 失败模式与局限

当帧间运动过大或视频帧率极低时，RetimeGS 的中间帧插值出现明显伪影（**Figure 8**）。根因在于现有光流估计器在光流位移超过约 50 像素时无法提供可靠对应，导致样条轨迹监督失效。此外，由于相邻动态基元组本质上不连续，离散输入帧处仍可能出现轻微闪烁伪影。这两个问题指向了当前 4DGS 框架的结构性局限：对光流质量的强依赖和基元组间的离散边界。

## 定位与知识库关联

### 4DGS 时间插值的方法谱系

RetimeGS 处于 **4D 高斯溅射（4DGS）动态场景重建** 这一研究脉络中，其核心贡献在于解决现有方法在**稀疏时间采样下中间帧插值**时产生的时间混叠（temporal aliasing）问题。理解其定位，需先梳理 4DGS 中两类主流范式及其瓶颈。

**基于变形的 4DGS（Deformation-based）** 以 **Deform-GS** 为代表，使用单一静态基元集并通过一个变形场（通常是 MLP）将基元从规范空间映射到各帧。该范式的根本矛盾在于：变形场需要学习大位移下的精确对应关系，而基元本身缺乏显式的运动先验，导致在快速非刚性运动下变形场难以收敛，重建质量受限。RetimeGS 的实验表明，Deform-GS 在 Stage-Capture 数据集上的 PSNR 为 28.45 dB，显著低于 RetimeGS 的 30.08 dB（Table 1），验证了这一瓶颈。

**基于 4D 基元的方法（4D Primitive-based）** 则直接为每个基元赋予时间维度参数，典型工作包括 **STGS**、**GaussianFlow** 和 **Ex4DGS**。这些方法的共同缺陷是**时间不透明度缺乏正则化**：基元的时间活跃窗口（通常建模为 1D 高斯分布）可自由坍缩到单个离散帧，导致模型“记忆”输入帧而非学习帧间连续运动。当查询中间时间戳时，两组分别过拟合到相邻帧的基元同时激活并发生冲突，产生鬼影伪影（ghosting artifacts），这正是 Figure 2 所揭示的核心问题。

GaussianFlow 在 STGS 基础上引入了前向光流监督，试图改善运动一致性，但未触及时间不透明度的根本缺陷——光流监督仅约束空间轨迹，而时间过拟合问题依然存在。Ex4DGS 虽显式建模了时间不透明度，但同样未施加正则化，因此仍易过拟合。

### RetimeGS 的核心设计逻辑与因果机制

RetimeGS 的设计围绕一个核心洞察展开：**若要可靠插值中间帧，必须强制每组基元同时解释相邻两个输入帧及其间隔，而非各自坍缩到单帧**。这一原则通过三个相互耦合的机制实现：

1. **短尾时间不透明度（Short-tailed Temporal Opacity）**：将时间不透明度建模为两个边界感知 sigmoid 函数的乘积 $\sigma_{\tau}(t) = \tilde{\psi}_l\left( \frac{t - (\mu_{\tau} - \tau_l)}{\gamma} \right) \tilde{\psi}_r\left( \frac{(\mu_{\tau} + \tau_r) - t}{\gamma} \right)$。该函数在区间 $[\mu_{\tau}-\tau_l, \mu_{\tau}+\tau_r]$ 内接近 1，在边界外迅速衰减，从而强制基元仅在其指定时间窗口内活跃。配合初始化为 $\Delta t/2$ 的窗口宽度，每组基元天然覆盖相邻两帧及其中间间隔，从结构上消除了单帧坍缩的可能性。

2. **Catmull-Rom 样条轨迹与双向光流监督**：基元的空间位置由 Catmull-Rom 样条定义，其内部控制点 $\pmb{p}_{1,p}, \pmb{p}_{2,p}$ 由伪均值 $\pmb{\mu}_p$ 和区间速度 $\pmb{v}_{2,p}$ 决定，外部控制点 $\pmb{p}_{0,p}, \pmb{p}_{3,p}$ 则利用相邻区间的速度 $\pmb{v}_{1,p}, \pmb{v}_{3,p}$ 确定曲率。双向光流（前向与后向）同时监督三个速度分量，确保轨迹在帧间平滑过渡且与多视图观测一致。消融实验证实，将线性轨迹替换为样条轨迹可避免分段线性运动产生的边缘伪影（Figure 7）。

3. **三重渲染与动态基元预算分配**：在每个内部帧 $t_i$，同时渲染三个图像——完整基元集、前一子集（覆盖 $t_{i-1}$ 到 $t_i$）和后一子集（覆盖 $t_i$ 到 $t_{i+1}$）。这一策略强制每个子集独立解释其对应输入帧，避免相邻基元组覆盖不均导致的欠重建（Figure 5b 显示，无三重渲染时两组基元各自仅捕获部分纹理）。此外，动态拉伸策略将静态基元的时间边界周期性扩展至 $(1/2 + k)\Delta t$，在 1M 基元预算下将静态基元压缩至约 88K（仅占总数的 9%），使有效基元数降低 2.26 倍，同时重定位机制根据采样分数 $s = \frac{\sigma}{\tau_l + \tau_r}$ 将低不透明度基元重新分配到高动态区域。

### 适用边界与局限

RetimeGS 的有效性依赖于两个关键前提，当这些前提被打破时性能显著退化：

**帧间运动幅度的上限**：方法依赖现成光流估计器（如 WAFT 或 SEA-RAFT）提供可靠的帧间对应。当帧率极低或运动幅度过大（如光流位移超过约 50 像素）时，光流估计本身失效，导致轨迹监督信号不可靠，中间帧插值出现明显伪影（Figure 8）。这是方法层面的根本性局限，而非工程问题——短尾时间不透明度假定基元在相邻帧间存在可被光流捕获的连续运动，当这一假设不成立时，整个表示框架的基础被动摇。

**离散帧处的闪烁伪影**：由于相邻动态基元组在本质上是两个独立的基元集合（而非一个统一的连续表示），在输入帧时刻 $t_i$ 处，属于 $[t_{i-1}, t_i]$ 和 $[t_i, t_{i+1}]$ 的两组基元可能产生轻微的视觉不连续，表现为闪烁伪影。这是“分组表示”策略的结构性代价。

**快速不透明度变化的场景**：对于火焰等不透明度剧烈变化的场景，短尾时间不透明度假定基元在其活跃窗口内保持近似恒定的不透明度，可能与实际物理过程不匹配。虽然在 Neural3DV 火焰场景上 RetimeGS 仍优于 Deform-GS（PSNR 33.22 vs 31.79，Table 5），但该场景并非其设计目标的核心假设，可能需要自适应调整时间窗口以更好地建模不透明度突变。

### 开放问题与后续方向

1. **极低帧率或大运动场景的稳健重建**：当前方法对光流质量的强依赖构成了其适用范围的硬边界。引入更强的运动先验（如从单目深度估计或物理模拟中提取的 3D 运动线索）、或设计对光流误差更鲁棒的轨迹参数化形式，是突破这一边界的关键方向。

2. **统一 4D 表示以消除分组伪影**：相邻基元组的不连续性源于“每组覆盖一对帧”的设计选择。能否设计一个统一的 4D 表示，使所有基元的时间活跃窗口在全局范围内平滑衔接，同时保留对离散输入帧的精确重建能力，是一个具有理论深度的开放问题。

3. **自适应时间窗口与不透明度建模**：当前短尾时间不透明度的窗口宽度是均匀初始化的，且形状固定。对于不同运动速度、不同不透明度变化模式的区域，自适应地调整 $\tau_l, \tau_r$ 以及 sigmoid 的锐度参数 $\gamma$，可能进一步提升对复杂动态场景的建模能力。

4. **与基于变形的 4DGS 的融合**：RetimeGS 的 4D 基元表示与 Deform-GS 的变形场表示并非互斥。将短尾时间不透明度正则化引入变形框架，或在 4D 基元框架中引入局部变形场以处理基元内部的非刚性形变，可能结合两者的优势。

## 原文 PDF

![[paperPDFs/CVPR_2026/RetimeGS_Continuous_Time_Reconstruction_of_4D_Gaussian_Splatting.pdf]]
