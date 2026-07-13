---
title: "DreamStereo: Towards Real-Time Stereo Inpainting for HD Videos"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/DreamStereo_Towards_Real_Time_Stereo_Inpainting_for_HD_Videos.pdf
project_link: null
code_link: null
aliases:
- DreamStereo
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: 利用梯度感知后向扭曲（GAPW）生成精确且连续的遮挡掩码，进而基于掩码仅选择必要的视觉令牌（遮挡区域及膨胀带）参与扩散Transformer（DiT）计算，实现大幅加速而不损失修复质量。
primary_logic: 通过梯度感知的坐标映射函数梯度构建平滑遮挡掩码，再以掩码驱动的令牌选择去除超过70%的冗余记号，将DiT推理速度提升10.7倍，在几乎不影响修复效果的前提下使高清立体视频修复达到实时（25 FPS）。
claims:
- 在HD-100基准上，单步推理（NFE=1）取得30.48 dB PSNR，同时延迟降至40.1 ms/frame，显著超越对比方法。
- 稀疏感知策略（SASI）在保留约35%令牌时，DiT推理加速10.7倍，且指标下降可忽略。
- PBDP 利用 GAPW 生成的伪立体数据质量远优于基于前向扭曲的构造方法（TrajectoryCrafter），产生更干净的掩码和更少的伪影。
- HD-100 (768×1280) 上 PSNR (dB) = 30.48 (Ours, NFE=1)
---

# DreamStereo: Towards Real-Time Stereo Inpainting for HD Videos

> [!tip] 核心洞察
> 通过梯度感知的坐标映射函数梯度构建平滑遮挡掩码，再以掩码驱动的令牌选择去除超过70%的冗余记号，将DiT推理速度提升10.7倍，在几乎不影响修复效果的前提下使高清立体视频修复达到实时（25 FPS）。

| 字段 | 内容 |
|------|------|
| 中文题名 | DreamStereo：面向高清视频的实时立体修复 |
| 英文题名 | DreamStereo: Towards Real-Time Stereo Inpainting for HD Videos |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2604.12270) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/image_and_video_generation |
| Method | DreamStereo |
| Dataset | HD-100, Dynamic Replica, SVD AVP |

> [!tip] 效果简介
> - HD-100 (768×1280) 上，PSNR (dB) 30.48 (Ours, NFE=1) vs 28.30 (ProPainter, NFE=1) (+2.18)；Latency (ms/frame) 40.1 (Ours, NFE=1) vs 668.1 (ProPainter) (-94.0%)；SSIM 0.900 (Ours, NFE=1) vs 0.927 (ProPainter) (-0.027)。
> - HD-100 (576×1024) 上，DiT Latency (ms/frame) 58.4 (SASI, r=36.1%) vs ~245 ms (dense estimation) (~4.2× speedup (10.7× in paper for 768×1280))。
> - Dynamic Replica (720×1280) 上，PSNR (dB) 29.12 (Ours)。

## 概要

立体视频修复（stereo video inpainting）面临一个根本性的效率瓶颈：现有方法对所有像素进行等量计算，导致大量冗余，难以满足高清视频的实时处理需求。同时，常用的前向扭曲（forward warping）在生成遮挡掩码时易产生散点（fly-point artifacts）和粗糙边界，进一步损害数据质量与推理速度。

DreamStereo 的核心思路是通过**梯度感知后向扭曲**（Gradient-Aware Parallax Warping, GAPW）生成精确且连续的遮挡掩码，并以此为驱动，仅选择遮挡区域及其膨胀带内的关键视觉令牌参与扩散 Transformer（DiT）计算。这一稀疏感知策略（Sparsity-Aware Stereo Inpainting, SASI）可去除超过 70% 的冗余令牌，将 DiT 推理速度提升 **10.7 倍**，在几乎不影响修复质量的前提下，使 768×1280 高清立体视频修复达到 **25 FPS** 的实时性能。

在 HD-100 基准上，DreamStereo 以单步推理（NFE=1）取得 **30.48 dB PSNR**，延迟仅为 **40.1 ms/frame**，显著优于 ProPainter（28.30 dB, 668.1 ms/frame）等对比方法。该方法同时支持从单目视频出发的二维转三维任务，在 Dynamic Replica 和 SVD AVP 等多个基准上展现出竞争力的修复质量与几何一致性。



立体视频修复（stereo video inpainting）要求同时恢复左右眼视图中被遮挡或移除的区域，并保持严格的几何一致性与时序连贯性。随着高清（HD）立体内容在影视后期、虚拟现实和 3D 媒体中的普及，对该任务的实时处理需求日益迫切。然而，现有方法在质量与效率之间存在显著鸿沟。

### 现有方法的瓶颈

当前立体修复方法面临两个相互关联的核心瓶颈：

**计算冗余**。基于扩散 Transformer（DiT）的视频修复模型将每一帧的所有视觉令牌（visual tokens）等量地送入注意力计算，其复杂度为 $\mathcal{O}(N^2)$。在立体场景下，左右视图叠加使令牌数翻倍，但其中大量像素属于无需修复的可见区域，造成严重冗余。传统方法未对令牌进行差异化处理，导致推理延迟居高不下。

**掩码质量缺陷**。立体修复的精度高度依赖遮挡掩码（occlusion mask）的准确性。主流方案采用前向扭曲（forward warping）来估计遮挡区域，其映射过程为：

$$(x', y') = T(x, y; D, C)$$

$$I'(x', y') \leftarrow I(x, y)$$

前向扭曲将源像素“推送”到目标视图，但多个源像素可能映射到同一目标位置，产生散点（fly-point artifacts）和断裂边界，导致掩码不平滑。这种低质量掩码不仅损害修复数据构造的准确性，还会在推理时将噪声引入令牌选择过程。

### 动机与目标

上述瓶颈揭示了一个明确的改进方向：**通过精确的遮挡掩码驱动令牌选择，仅对必要的空间区域进行高成本计算，从而实现大幅加速而不牺牲修复质量**。这需要解决两个子问题：

1. 如何生成平滑、连续的遮挡掩码，避免前向扭曲的散点缺陷？
2. 如何利用该掩码在 DiT 推理中安全地剪枝冗余令牌？

DreamStereo 围绕这一思路，提出梯度感知视差扭曲（GAPW）替代前向扭曲，从坐标映射函数的梯度场中推导遮挡边界，获得边缘清晰的平滑掩码。在此基础上，稀疏感知立体修复策略（SASI）仅保留遮挡区域及其膨胀带内的令牌（默认保留率约 35%），将 DiT 推理加速 10.7 倍，使 768×1280 高清立体视频修复首次达到实时（25 FPS），同时 PSNR 达到 30.48 dB，显著超越现有扩散与非扩散方法。



## 核心方法与创新机理

DreamStereo 的核心创新围绕一个关键瓶颈展开：**现有立体修复方法对所有像素等量处理，导致大量冗余计算；同时，常用的前向扭曲（forward warping）产生散点和不够平滑的遮挡掩码，损害数据质量和推断速度**。针对这一瓶颈，论文通过三个相互协同的技术槽位（changed slots）实现了从数据构造到推理加速的系统性突破。

### 梯度感知视差扭曲（GAPW）：从散点掩码到平滑边界

传统前向扭曲的遮挡掩码生成存在根本性缺陷：当多个源像素映射到同一目标位置时，离散的赋值操作不可避免地在遮挡边界产生飞点（fly-point）伪影和模糊边缘（Figure 2）。DreamStereo 提出的 **GAPW** 将这一过程重构为反向映射框架下的梯度分析问题。

其核心机制是：反向扭曲通过坐标映射函数 $T^{-1}$ 从目标像素反查源坐标，再利用双向插值获取像素值，从而天然避免散点问题。更关键的是，GAPW 利用坐标映射函数的雅可比矩阵 $\mathbf{J}_T$ 的范数来判定遮挡——当局部变形足够大时，即 $\parallel \mathbf{J}_T(x', y') \parallel_2 > \delta$，该像素被标记为遮挡（Eq. 6）。在双目立体场景中，遮挡仅发生在水平方向，该判定可简化为偏导数绝对值阈值 $\left| \frac{\partial x'}{\partial x} \right| > \delta$（Eq. 7）。

这一梯度感知机制使得 GAPW 生成的遮挡掩码具有连续且平滑的边界，从根本上消除了前向扭曲的飞点伪影。如 Figure 2 所示，GAPW 产生的掩码边缘清晰、区域完整，为后续的令牌选择提供了高质量的结构先验。

### 视差驱动的双重投影（PBDP）：从单目视频到高保真立体修复数据

立体修复模型的训练通常依赖立体视频拍摄或传统重投影方法，前者获取成本高昂，后者（如基于前向扭曲的 TrajectoryCrafter）掩码质量不稳定。**PBDP** 策略完全从单目视频出发，通过两次 GAPW 投影构建几何一致的修复训练对。

具体流程（Figure 3a）为：首先利用 GAPW 将输入视图 $\mathbf{V}_1$ 及其视差 $\mathbf{D}_1$ 投影到新视点，生成 $\mathbf{V}_2$ 和 $\mathbf{D}_2$（Eq. 8）；随后从 $\mathbf{V}_2$ 反投影回原视点，获得 $\mathbf{V}_1'$ 和遮挡掩码 $\mathbf{M}_1$（Eq. 9）。这一“正投-反投”的双重投影设计确保了输入视图的遮挡掩码与修复目标在几何上严格一致。

消融实验（Table 3）证实，PBDP 管道生成的伪立体数据在修复指标上显著优于基于前向扭曲的构造方法，PSNR 提升超过 1 dB。Figure 4 的定性对比进一步显示，PBDP 产生的掩码更干净、伪影更少，为扩散模型的训练提供了更可靠的数据基础。

### 稀疏感知立体修复（SASI）：令牌选择驱动的 10.7 倍加速

扩散 Transformer（DiT）的注意力计算复杂度为 $\mathcal{O}(N^2)$，其中 $N$ 为视觉令牌数。在立体修复任务中，大量令牌对应的是无需修复的非遮挡区域，参与全量计算造成严重冗余。**SASI** 利用 GAPW 生成的高质量遮挡掩码，通过掩码驱动的令牌选择机制，仅保留对修复至关重要的令牌参与 DiT 计算。

其操作流程（Figure 3b）为：对遮挡掩码 $\mathbf{m}$ 进行膨胀操作 $\Phi(\mathbf{m}, k)$，将选择范围从严格遮挡区域扩展至包含边界过渡带的窄带区域；随后仅将膨胀带内的潜在令牌 $(\hat{\mathbf{z}}_0, \hat{\mathbf{z}}^m, \hat{\mathbf{m}})$ 送入 DiT 进行流匹配去噪（Eq. 11-14），其余令牌直接保留原始值。最终通过掩码感知混合 $\mathcal{B}$ 将去噪结果与非遮挡区域融合（Eq. 15）。

在默认配置（膨胀核大小 $k=5$，令牌保留率约 35%）下，SASI 使 DiT 推理加速 **10.7 倍**，且 PSNR 下降不足 1 dB（Table 4）。值得注意的是，论文尝试在训练阶段也施加稀疏性，但并未带来性能增益（Table 8），因此最终模型仅在推理时采用稀疏策略，实现了“训练稠密、推理稀疏”的高效范式。

### 辅助加速：蒸馏 3D VAE

除上述三个核心槽位外，DreamStereo 还引入了一个辅助创新：将原始 WanVAE（参数 126.8M）蒸馏为轻量 3D 感知 VAE。蒸馏后的 VAE 参数减少 36%，编解码速度提升超过 4 倍，而对修复质量的影响几乎可忽略（PSNR 从 30.59 变为 30.48，Table 6 & 7）。这一优化与 SASI 的令牌选择形成互补，从潜在空间压缩和注意力计算两个维度共同推动系统达到实时性能。

### 创新协同效应

上述四个槽位形成了一条完整的效率-质量协同链路：**GAPW** 提供高质量掩码 → **PBDP** 利用 GAPW 构造高保真训练数据 → **SASI** 基于掩码选择关键令牌加速 DiT → **蒸馏 VAE** 进一步压缩编解码开销。这一链路使得 DreamStereo 在 HD-100 基准（768×1280）上以单步推理（NFE=1）取得 30.48 dB PSNR，同时将延迟降至 40.1 ms/frame（约 25 FPS），在几乎不影响修复效果的前提下首次实现高清立体视频修复的实时处理（Table 1, Figure 1）。



DreamStereo 的核心管线围绕“从单目视频出发，高效生成几何一致的高清立体修复结果”这一目标构建，其整体架构由三个关键阶段串联而成：**数据构造**（PBDP）、**潜在空间压缩**（蒸馏3D VAE）与**稀疏感知修复**（SASI + DiT 流匹配），最终通过掩码感知混合输出修复视频。

### 输入与输出

- **输入**：一段单目视频 $\mathbf{V}_1$（左视点）及其对应的视差序列 $\mathbf{D}_1$，以及待修复区域的遮挡掩码 $\mathbf{M}$。
- **输出**：修复后的立体视频对 $(\mathbf{V}_1^{\text{out}}, \mathbf{V}_2^{\text{out}})$，其中右视点 $\mathbf{V}_2$ 由 PBDP 数据管道生成并修复。

### 模块关系与数据流

**阶段一：视差驱动的双重投影（PBDP）**
PBDP 从单目视频出发，完全无需立体视频监督，通过两次梯度感知视差扭曲（GAPW）构造训练或推理所需的右视点视频与精确遮挡掩码。具体流程为：
1. 将左视点视频 $\mathbf{V}_1$ 与视差 $\mathbf{D}_1$ 经 GAPW 投影至右视点，得到 $\mathbf{V}_2$ 与 $\mathbf{D}_2$（Eq. 8）。
2. 再将 $\mathbf{V}_2$、$\mathbf{D}_2$ 经 GAPW 反投影回左视点，获得左视点的遮挡掩码 $\mathbf{M}_1$（Eq. 9）。
该双重投影确保了左右视点间的几何一致性，且生成的掩码边界平滑、散点极少（Figure 3a、Figure 4），为后续稀疏选择提供了高质量的先验。

**阶段二：3D 变分自编码器压缩**
原始视频帧经蒸馏的轻量 3D VAE 压缩至低维潜在空间，时空维度大幅降低。该 VAE 相比原始 WanVAE 参数减少 36%，编解码延时降低 4 倍以上，而修复质量几乎无损（Table 6、Table 7）。压缩后的潜在表示 $\mathbf{z}_0$ 及其掩码版本 $\mathbf{z}^m$ 进入后续 DiT 处理。

**阶段三：稀疏感知立体修复（SASI）与流匹配去噪**
SASI 是 DreamStereo 实现实时推理的核心机制。其操作流程为：
1. **掩码驱动令牌选择**：基于 PBDP 生成的遮挡掩码 $\mathbf{m}$，通过膨胀操作（默认膨胀核 $k=5$）确定关键区域，仅保留该区域内的视觉令牌，其余令牌被剪枝。默认保留率约 35%（Eq. 11）。
2. **流匹配去噪**：被选中的令牌 $(\hat{\mathbf{z}}_0, \hat{\mathbf{z}}^m, \hat{\mathbf{m}})$ 送入 DiT 去噪器，在潜在空间中预测速度场 $\mathbf{v}$（Eq. 12–14）。DiT 的注意力复杂度为 $\mathcal{O}(N^2)$，令牌数量 $N$ 的大幅削减直接带来 10.7 倍的 DiT 推理加速（Table 4）。
3. **掩码感知混合**：去噪后的潜在表示 $\hat{\mathbf{z}}_0$ 经 VAE 解码，并与原始视频的非遮挡区域 $\mathbf{V}^m$ 按掩码 $\mathbf{M}$ 混合，得到最终修复视频 $\mathbf{V}$（Eq. 15）。

### 推理管线总览

Figure 8 展示了完整的 2D 转 3D 推理管线：单目左视点视频输入后，依次经过视差估计、PBDP 生成右视点及掩码、VAE 压缩、SASI 令牌选择、DiT 流匹配去噪、VAE 解码与掩码混合，最终输出立体视频对。在 HD-100（768×1280）上，单步推理（NFE=1）延迟仅 40.1 ms/帧（约 25 FPS），PSNR 达 30.48 dB，在实时性约束下显著优于 ProPainter 等基线方法（Table 1）。

![[assets/figures/papers/paper_list_l2250_https_arxiv_org_abs_2604_12270/figures/013_Figure_8.jpg]]
*Figure 8: Inference pipeline of 2D-to-3D conversion*

### 补充图表

![[assets/figures/papers/paper_list_l2250_https_arxiv_org_abs_2604_12270/figures/003_Figure_3.jpg]]
*Figure 3: (a) Illustration of the Parallax-Based Dual Projection, which utilizes Gradient-Aware Parallax Warping for reprojection to obtain the occlusion mask under input view. (b) Our proposed Sparsity-Aware Stereo Inpainting utilizes Mask-Based Token Selection to reduce the redundancy of visual tokens*



DreamStereo 的实时立体修复能力建立在三个紧密协作的核心模块之上：**梯度感知视差扭曲（GAPW）** 解决高质量视图投影与遮挡掩码生成问题；**视差驱动的双重投影（PBDP）** 利用 GAPW 从单目视频构建几何一致的训练数据；**稀疏感知立体修复（SASI）** 则通过掩码驱动的令牌选择大幅削减扩散 Transformer 的计算冗余。三个模块形成一条从数据构造到高效推理的完整因果链。

### 梯度感知视差扭曲（GAPW）

传统前向扭曲（forward warping）将源图像像素直接映射到目标视图，其映射关系为：

$$(x', y') = T(x, y; D, C)$$

$$I'(x', y') \leftarrow I(x, y)$$

其中 $D$ 为视差，$C$ 为相机姿态。这种“源到目标”的散射式赋值容易产生飞点（fly-point）伪影和破碎的遮挡边界，直接影响后续修复质量。

GAPW 转而采用**反向扭曲**策略：对目标视图的每个像素 $(x', y')$，通过逆映射函数反算其在源图像中的对应坐标：

$$(x, y) = T^{-1}(x', y'; D, C)$$

$$I'(x', y') = \mathrm{Interpolate}(I, x, y)$$

由于逆映射后的坐标通常为非整数，需通过双向插值获取像素值。GAPW 的核心创新在于利用坐标映射函数的**雅可比矩阵梯度**来生成平滑的遮挡掩码。遮挡本质上发生在几何形变剧烈的区域，而雅可比矩阵的范数恰好量化了这种形变程度。通用形式的遮挡掩码定义为：

$$M(x', y') = \parallel \mathbf{J}_T(x', y') \parallel_2 > \delta$$

其中 $\mathbf{J}_T$ 为映射函数 $T$ 的雅可比矩阵，$\delta$ 为判定阈值。当 L2 范数超过阈值时，该像素被标记为遮挡。

在双目立体场景中，遮挡仅发生在水平（$x$）方向，上述公式可简化为偏导数的绝对值判定：

$$M(x', y') = \left| \frac{\partial x'}{\partial x} \right| > \delta$$

这一简化在保留遮挡检测精度的同时进一步降低了计算开销。与基于前向扭曲的方法（如 TrajectoryCrafter）相比，GAPW 生成的掩码具有连续平滑的边缘，几乎消除了散点噪声（见 Figure 4 定性对比），为后续的令牌选择提供了高质量的空间先验。

![[assets/figures/papers/paper_list_l2250_https_arxiv_org_abs_2604_12270/figures/004_Figure_4.jpg]]
*Figure 4: Qualitative comparison of data construction between TrajectoryCrafter [39] and ours*

### 视差驱动的双重投影（PBDP）

立体修复训练通常需要成对的立体视频和精确的遮挡掩码，但此类数据获取成本极高。PBDP 策略完全从单目视频出发，通过两次 GAPW 投影自动构造训练所需的视频对和掩码。

给定单目视频 $\mathbf{V}_1$ 及其估计视差 $\mathbf{D}_1$，首先通过 GAPW 将其投影到虚拟右视点：

$$\mathbf{V}_2, \mathbf{D}_2 = \mathbf{GAPW}(\mathbf{V}_1, \mathbf{D}_1; v1 \rightarrow v2)$$

随后，将投影结果 $\mathbf{V}_2$ 和 $\mathbf{D}_2$ 再次通过 GAPW 反投影回原始视点，以获取该视点下的遮挡掩码：

$$\mathbf{V}_1', \mathbf{M}_1 = \mathbf{GAPW}(\mathbf{V}_2, \mathbf{D}_2; v2 \rightarrow v1)$$

反投影过程中，由于视差导致的几何遮挡自然暴露为 $\mathbf{M}_1$ 中的空洞区域。此时，$\mathbf{V}_1$ 作为待修复的输入、$\mathbf{V}_1'$ 作为修复目标（ground truth）、$\mathbf{M}_1$ 作为精确的遮挡掩码，三者构成完整的训练三元组。消融实验（Table 3）表明，PBDP 管道生成的伪立体数据在修复指标上相比基于前向扭曲的构造方法 PSNR 提升超过 1 dB，验证了 GAPW 在数据构造环节的关键作用。

### 稀疏感知立体修复（SASI）

扩散 Transformer（DiT）的注意力计算复杂度为 $\mathcal{O}(N^2)$，其中 $N$ 为视觉令牌数量。在稠密模式下，所有令牌均参与计算，但立体修复任务中仅遮挡区域及其邻近边界真正需要生成新内容，大量背景令牌的计算实属冗余。

SASI 利用 GAPW 生成的掩码 $\mathbf{m}$ 进行令牌筛选。首先对掩码施加形态学膨胀操作 $\Phi(\mathbf{m}, k)$（膨胀核大小 $k$ 默认为 5），将遮挡区域边界向外扩展一个窄带，确保修复边界的平滑过渡。随后仅保留膨胀带内的令牌：

$$(\hat{\mathbf{z}}_0, \hat{\mathbf{z}}^m, \hat{\mathbf{m}}) = \mathcal{S}((\mathbf{z}_0, \mathbf{z}^m, \mathbf{m}), \Phi(\mathbf{m}, k))$$

其中 $\mathbf{z}_0$ 为待修复的潜在表示，$\mathbf{z}^m$ 为掩码区域的潜在表示，$\hat{\cdot}$ 表示筛选后的稀疏版本。默认配置下，令牌保留率约为 35%，即超过 65% 的冗余令牌被剪枝，DiT 推理速度因此提升 **10.7 倍**（Table 4），而 PSNR 下降不足 1 dB，各项指标几乎无损。

筛选后的稀疏令牌随后进入流匹配去噪流程。前向加噪过程为：

$$\hat{\mathbf{z}}_t = (1 - \sigma_t) \cdot \hat{\mathbf{z}}_0 + \sigma_t \cdot \boldsymbol{\epsilon}$$

DiT 网络 $D_\theta$ 预测速度场 $\mathbf{v}$，训练目标为最小化预测速度与真实速度的 L2 距离：

$$\mathcal{L} = \| D_\theta(\hat{\mathbf{z}}_t, \hat{\mathbf{z}}^m, \hat{\mathbf{m}}, t) - \mathbf{v} \|_2$$

多步去噪递推公式为：

$$\hat{\mathbf{z}}_{t-1} = \hat{\mathbf{z}}_t + D_\theta(\hat{\mathbf{z}}_t, \hat{\mathbf{z}}^m, \hat{\mathbf{m}}, \mathbf{c}, t) \cdot (\sigma_{t-1} - \sigma_t)$$

经过 $N$ 步去噪后，将去噪后的潜在表示解码并与原始非遮挡区域通过掩码感知混合，得到最终修复视频：

$$\mathbf{V} = \mathcal{B}( \mathcal{D}( \mathcal{B}( \hat{\mathbf{z}}_0, \mathbf{z}^m, \mathbf{m} ) ), \mathbf{V}^m, \mathbf{M} )$$

值得注意的是，消融实验（Table 8）表明在训练阶段施加稀疏约束并未带来性能增益（PSNR 32.48 vs 32.31），因此最终模型仅在推理时采用稀疏策略，既保证了训练稳定性，又实现了极致的推理加速。

### 补充图表

![[assets/figures/papers/paper_list_l2250_https_arxiv_org_abs_2604_12270/figures/002_Figure_2.jpg]]
*Figure 2: Comparison of forward warping and our GAPW in pixel mapping and occlusion mask generation*



## 实验与关键发现

### 核心定量结果

在 HD-100 基准（768×1280）上，DreamStereo 以单步推理（NFE=1）取得 **30.48 dB PSNR**，同时将每帧延迟压缩至 **40.1 ms**（约 25 FPS），首次实现高清立体修复的实时处理。与最强非扩散基线 ProPainter（Zhou et al., ICCV 2023）相比，PSNR 提升 2.18 dB，延迟降低 94.0%（668.1 ms → 40.1 ms），尽管 SSIM 略有下降（0.900 vs 0.927），但视觉质量更接近真值，细节更清晰、结构更完整（Table 1, Figure 5）。在二维转三维任务的两个测试集上，方法同样取得最优指标：Dynamic Replica（720×1280）上 PSNR 29.12 dB，SVD AVP（768×768）上 PSNR 24.88 dB（Table 2）。

![[assets/figures/papers/paper_list_l2250_https_arxiv_org_abs_2604_12270/figures/005_Table_1.jpg]]
*Table 1: HD-100 @ 768×1280. Quality and latency (ms/frame). † non-diffusion*

![[assets/figures/papers/paper_list_l2250_https_arxiv_org_abs_2604_12270/figures/007_Figure_5.jpg]]
*Figure 5: Qualitative comparison of stereo video inpainting on the HD-100 test set (768×1280). Our inpainting results are much closer to the ground truth, showing sharper details and clearer structures*

### 加速机制消融：稀疏感知令牌选择

SASI 是达成实时性能的关键杠杆。在 HD-100（576×1024）上固定 NFE=4 的消融表明，当膨胀核 k=5、令牌保留率约 35% 时，DiT 推理延迟从稠密模式降至 58.4 ms/frame，加速约 4.2 倍；在 768×1280 分辨率下，保留率进一步降至 25.6%，加速比达到 **10.7 倍**，且 PSNR 下降不足 1 dB（Table 4）。这一结果直接验证了核心洞察：遮挡区域及膨胀带之外的视觉令牌对修复质量贡献极小，可被安全剪枝。

![[assets/figures/papers/paper_list_l2250_https_arxiv_org_abs_2604_12270/figures/010_Table_4.jpg]]
*Table 4: HD-100 (576×1024) ablation with fixed NFE= 4, varying dilation kernel and temporal stride. Retention rate r is the fraction of tokens kept for DiT computation; ‡Latency denotes DiT-only inference time in ms/frame. All settings achieve a substantial speedup with negligible quality loss. The light-gray row (dilate=5) indicates the optimal setting adopted in all other experiments*

### 数据构造策略消融

PBDP 管道生成的伪立体数据质量显著优于基于前向扭曲的构造方法（TrajectoryCrafter, Yu et al., arXiv 2025）。在 HD-100 上，使用 PBDP 数据训练的模型取得 PSNR 32.48 dB / SSIM 0.933，领先其他数据策略超过 1 dB（Table 3）。定性对比显示，PBDP 生成的掩码更干净、几何一致性更好，而前向扭曲方案产生大量散点伪影和不连续边界（Figure 4）。

![[assets/figures/papers/paper_list_l2250_https_arxiv_org_abs_2604_12270/figures/009_Table_3.jpg]]
*Table 3: Ablation of inpainting performance on dataset strategy*

### VAE 蒸馏与训练策略

将原始 WanVAE（126.8M 参数）替换为蒸馏的轻量 3D 感知 VAE，PSNR 仅从 30.59 变为 30.48，几乎无质量损失，同时参数减少 36%，编解码延迟缩短 4 倍以上（Table 6 & Table 7）。此外，在训练过程中施加稀疏性并未带来性能增益（PSNR 32.48 vs 32.31），因此最终模型仅在推理时采用稀疏策略（Table 8）。

![[assets/figures/papers/paper_list_l2250_https_arxiv_org_abs_2604_12270/figures/015_Table_6.jpg]]
*Table 6: Ablation on stereo inpainting quality on HD-100 (768×1280). Results are evaluated under the same final setting as in the main paper (see Tab. 1), using different VAEs. The distilled VAE achieves nearly identical quality to the original WanVAE*

![[assets/figures/papers/paper_list_l2250_https_arxiv_org_abs_2604_12270/figures/016_Table_7.jpg]]
*Table 7: Ablation on VAE parameter efficiency and latency at 1024×1024 resolution*

### 宽基线鲁棒性

在最大视差从 0.07 逐步增大的设置下，单步模型（NFE=1）的 PSNR 仅出现轻微下降，修复结果依然保持几何准确性和视觉质量，证明方法对宽基线场景具有良好鲁棒性（Table 5, Figure 7）。

![[assets/figures/papers/paper_list_l2250_https_arxiv_org_abs_2604_12270/figures/012_Table_5.jpg]]
*Table 5: HD-100 (768×1280) ablation with fixed NFE= 1 under wide-baseline settings. The light-gray row (0.07) corresponds to the setting adopted for all stereo inpainting experiments on the HD-100 test set. Larger disparities enlarge occluded areas, causing a slight expected drop in metrics, yet our method remains robust and effective*

![[assets/figures/papers/paper_list_l2250_https_arxiv_org_abs_2604_12270/figures/011_Figure_7.jpg]]
*Figure 7: Ablation on max disparity. Our method consistently delivers high-quality, geometrically accurate results even under large disparity ranges*

### 失败模式与局限

方法在以下长尾场景中表现出明显退化（Figure 15）：
- **透明物体**：透过玻璃看到的电线杆等结构产生严重几何扭曲，深度估计与扭曲范式无法正确处理折射/透射引起的视差歧义。
- **反射表面**：走廊玻璃上的阴影等视角依赖效果与真实几何不一致，模型缺乏对反射的物理建模能力。
- **高频纹理区域**：细节丰富的表面合成结果不够清晰，保真度有限。

以上失败模式揭示了当前“深度估计+扭曲+修复”范式在几何模糊和视角依赖效果上的根本局限，需引入更强的视觉先验或物理感知约束来突破。



## 定位与知识库关联

### 与现有方法的关联与区别

DreamStereo 处于立体视频修复与扩散模型加速的交汇点，其设计直接回应了现有方法的两大瓶颈：**稠密令牌计算带来的实时性缺失**，以及**前向扭曲导致的数据质量退化**。

**相对于视频修复基线：** 传统视频修复方法如 **ProPainter**（Zhou et al., ICCV 2023）采用非扩散的流传播策略，在 HD-100 上取得了 28.30 dB PSNR（NFE=1），但每帧延迟高达 668.1 ms，远未达到实时要求。DreamStereo 以扩散 Transformer 替代流传播，结合稀疏令牌选择，在 PSNR 提升 2.18 dB 的同时将延迟压缩至 40.1 ms（约 25 FPS），首次使高清立体修复达到实时水平。通用视频修复模型 **VACE-1.3B** 和零样本立体修复方法 **ZeroStereo** 在同等条件下均表现出明显的性能与速度差距（Table 1）。

**相对于扩散立体修复方法：** **StereoCrafter**（Zhao et al., arXiv 2024）是直接可比的扩散模型立体修复方法。DreamStereo 与之的核心差异不在于扩散框架本身，而在于三个关键槽位的替换：视图扭曲从传统前向扭曲变为梯度感知后向扭曲（GAPW）；训练数据从依赖立体视频拍摄变为视差驱动的双重投影（PBDP）；DiT 推理从稠密令牌计算变为掩码驱动的稀疏感知选择（SASI）。这三个替换协同作用，使 DiT 推理加速 10.7 倍（Table 4），而修复质量几乎无损。

**相对于数据构造方法：** **TrajectoryCrafter**（Yu et al., arXiv 2025）是单目视频新视角合成方法，其双重投影策略依赖前向扭曲生成训练数据。DreamStereo 的 PBDP 将前向扭曲替换为 GAPW，产生的伪立体数据在掩码质量和几何一致性上显著优于 TrajectoryCrafter（Figure 4），在修复指标上带来超过 1 dB 的 PSNR 提升（Table 3）。

**相对于立体生成方法：** **SpatialDreamer** 和 **M2SViD** 是立体/4D 生成方法，在定性对比中暴露了截断伪影、色彩漂移和结构退化等问题（Figure 11, 12）。DreamStereo 在保持几何一致性和细节锐度方面具有明显优势，但其作为修复方法的定位与生成方法在任务设定上存在本质差异——修复依赖已知区域的约束，生成则从无到有。

### 适用边界与局限

DreamStereo 的核心能力边界由三个组件共同决定：

1. **GAPW 的几何假设：** 遮挡掩码的质量依赖于视差估计的准确性。在双目简化假设下（Eq. 7），仅考虑 x 方向的偏导数，这在大视差场景下依然稳健（Table 5，最大视差 0.07 时 PSNR 仅小幅下降），但当场景包含透明物体（如透过玻璃的电线杆）或反射表面（如走廊玻璃上的阴影）时，深度估计本身失效，导致重建产生明显扭曲（Figure 15）。这是视图合成范式的长尾问题，非 DreamStereo 特有。

2. **SASI 的稀疏化边界：** 令牌保留率约 35%（膨胀核大小 k=5）被选为默认设置，在加速 10.7 倍的同时 PSNR 下降不足 1 dB（Table 4）。当保留率进一步降低时，性能衰减可能加剧，但论文未给出极端稀疏化（如 <20%）的定量结果。此外，训练时施加稀疏性并未带来增益（Table 8），表明稀疏化的收益仅体现在推理阶段。

3. **高频细节的保真度上限：** 在高频纹理丰富区域，合成结果的清晰度有限（Figure 15 失败案例），这受限于 VAE 的压缩重建能力和 DiT 的生成先验。蒸馏 VAE 虽将参数减少 36% 且编解码加速 4 倍以上，但对修复质量影响甚微（Table 6, 7），说明当前瓶颈不在 VAE 而在去噪模型的表达能力。

### 开放问题

1. **透明与反射表面的几何推理：** 如何增强模型对视角相关光影变化的处理能力？可能的路径包括引入物理感知的渲染约束，或利用更大的预训练模型提供更强的视觉先验。

2. **稀疏感知策略的泛化性：** SASI 目前在 HD-100 和特定视差范围内验证有效。该策略能否扩展到更大规模数据集和更多样的视差分布，以及是否适用于其他基于 DiT 的视频生成任务，仍有待探索。

3. **端到端优化空间：** 蒸馏 VAE 与稀疏令牌选择目前独立优化。联合训练是否能在保持加速比的同时进一步提升修复质量，是一个值得验证的方向。

4. **高频纹理的保真度提升：** 当前方法在细节丰富区域的合成仍显不足。引入更强的视觉先验（如大规模预训练模型）或改进去噪模型的结构设计，可能是突破这一上限的关键。



## 原文 PDF

![[paperPDFs/CVPR_2026/DreamStereo_Towards_Real_Time_Stereo_Inpainting_for_HD_Videos.pdf]]
