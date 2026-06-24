---
title: "StreamSplat: Towards Online Dynamic 3D Reconstruction from Uncalibrated Video Streams"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/StreamSplat_Towards_Online_Dynamic_3D_Reconstruction_from_Uncalibrated_Video_Str_ddaf0a5cb355.pdf
project_link: "https://streamsplat3d.github.io/"
code_link: null
aliases:
- StreamSplat
tags:
- ICLR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
core_operator: 引入概率位置采样、双向变形场和自适应高斯融合三个关键技术，结合正交规范空间，使前馈网络能够直接从无标定视频流在线预测动态三维高斯场景。
primary_logic: 采用正交规范空间统一处理不同相机内参，利用概率采样提高三维高斯位置预测的鲁棒性，双向变形场与基于透明度的自适应融合机制实现稳定的在线时序一致性建模，从而无需相机标定和离线优化即可进行动态三维重建与多视角合成。
claims:
- 概率采样 (probabilistic sampling) 相比确定性回归 (deterministic regression) 在关键帧上将PSNR从31.47提升至37.83 (+6.36 dB)。
- StreamSplat在DAVIS数据集上以1.48秒总时间完成30帧的重建与渲染，PSNR达37.83，而离线优化方法耗时数小时，速度提升约1200倍。
- 自适应高斯融合 (adaptive Gaussian fusion) 通过时间依存的透明度变形 (opacity deformation) 实现了高斯点跨帧稳定传播，如图4所示高斯点在视角和运动变化下持续跟踪。
- DAVIS key frames 上 PSNR = 37.83
---

# StreamSplat: Towards Online Dynamic 3D Reconstruction from Uncalibrated Video Streams

> [!tip] 核心洞察
> 采用正交规范空间统一处理不同相机内参，利用概率采样提高三维高斯位置预测的鲁棒性，双向变形场与基于透明度的自适应融合机制实现稳定的在线时序一致性建模，从而无需相机标定和离线优化即可进行动态三维重建与多视角合成。

| 字段 | 内容 |
|------|------|
| 中文题名 | StreamSplat：基于无标定视频流的在线动态三维重建 |
| 英文题名 | StreamSplat: Towards Online Dynamic 3D Reconstruction from Uncalibrated Video Streams |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=SaiDRQU7Ez) · [Project](https://streamsplat3d.github.io/) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction |
| Method | StreamSplat |
| Dataset | DAVIS key frames, DAVIS middle-4 frames, DAVIS 8-frame interpolation, RE10K novel view |

> [!tip] 效果简介
> - DAVIS key frames 上，PSNR 37.83 vs 28.38 (DGMarbles) (+9.45)。
> - DAVIS middle-4 frames 上，PSNR 23.66 vs 21.33 (DGMarbles) (+2.33)。
> - DAVIS 8-frame interpolation 上，PSNR 22.10 vs 21.09 (AMT) (+1.01)。

## 概述

### 问题与瓶颈

动态三维场景重建是实现沉浸式视觉体验的关键技术，但现有方法存在根本性瓶颈：**主流方案依赖离线逐场景优化**，需要完整视频序列的离线访问和精确的相机标定，无法支持实时在线的无标定视频流处理。以基于3D高斯泼溅（3DGS）的优化方法为例，单场景重建耗时数十分钟至数小时，且要求已知相机内参和外参，严重制约了其在流媒体、增强现实等在线场景中的应用。

### 核心方法

**StreamSplat** 通过三项关键技术创新突破上述瓶颈：

1. **概率位置采样（Probabilistic Position Sampling）**：从预测的截断正态分布中采样三维高斯偏移量，替代传统的确定性回归，显著提升无标定输入下三维位置预测的鲁棒性。

2. **双向变形场（Bidirectional Deformation Field）**：同时建模前向（前一帧→当前帧）和后向（当前帧→前一帧）运动，增强跨帧时序关联，自然处理场景内容的出现与消失。

3. **自适应高斯融合（Adaptive Gaussian Fusion）**：基于时间依赖的不透明度变形曲线实现高斯点的软匹配与传播，隐式维持持久高斯点的长期时序一致性，同时无缝处理新出现和消失的高斯点。

在此基础上，StreamSplat采用**正交规范空间**统一处理不同相机的内参差异，使相机运动与透视效应由变形场吸收，从而在完全无需相机标定的条件下实现动态三维重建。

### 核心结论

StreamSplat在DAVIS动态场景数据集上以**1.48秒总时间**完成30帧的重建与渲染（约49 ms/帧），PSNR达**37.83 dB**，相比离线优化方法DGMarbles（28.38 dB，耗时约30分钟）提升**+9.45 dB**，速度提升约**1200倍**。在8帧间隔的大跨度时序插值任务中，StreamSplat（22.10 dB）超越专用2D视频插值方法AMT（21.09 dB）。零样本跨数据集评估中，StreamSplat在不使用任何相机参数的条件下，性能显著优于同等条件下的DGMarbles，并接近需要真实相机内参的4DGS方法。

消融实验验证了各项设计的决定性作用：概率采样将关键帧PSNR从31.47提升至37.83（+6.36 dB）；移除双向变形场使中间帧PSNR从23.66骤降至18.89；恒定不透明度替代自适应变形导致出现/消失区域产生鬼影和模糊。

### 方法谱系与知识库定位

StreamSplat位于**前馈3DGS重建**与**动态场景建模**的交叉点。在静态前馈重建线上，它继承并扩展了pixelSplat、MVSplat、NoPoSplat等工作的前馈预测范式，但首次将其推广至动态无标定场景。在动态重建线上，相较于4DGS、DGMarbles、Splatter a Video等离线优化方法，StreamSplat以在线推理替代逐场景优化；相较于Omnimotion、RoDynRF、CoDeF等基于NeRF的动态方法，它以3DGS的显式表示实现更高效的渲染。在在线重建方向上，StreamGS仅处理静态场景，而StreamSplat通过双向变形场和自适应融合机制首次实现了动态场景的在线重建。

方法的核心知识贡献在于：**正交规范空间 + 概率采样 + 双向变形场 + 自适应融合**的组合设计，使得前馈网络能够直接从无标定视频流在线预测动态三维高斯场景，省去了传统管线中的相机标定、逐场景优化和完整序列访问等环节。

## 背景与动机

### 动态三维重建的范式转变

从单目或多视角视频恢复动态三维场景是计算机视觉的核心课题，在增强现实、机器人导航与内容创作中具有广泛需求。传统方法依赖逐场景离线优化，需要完整视频序列的全局访问和精确的相机标定——这一前提在真实世界的在线视频流场景中几乎无法满足。近年来，以三维高斯泼溅（3D Gaussian Splatting, 3DGS）为代表的可微渲染技术显著提升了重建效率与视觉质量，但其动态扩展仍深陷离线优化的范式：**DGMarbles**、**4DGS**、**Splatter a Video** 等方法虽能产生高质量结果，但单场景重建耗时数十分钟至数小时，且必须依赖已知的相机内外参数。

### 现有方法的根本瓶颈

当前动态三维重建方法存在三个相互锁定的结构性缺口：

**1. 相机标定的刚性依赖。** 几乎所有动态 3DGS 方法（如 **DGMarbles**、**RoDynRF**、**Omnimotion**）均要求精确标定的透视相机模型。在消费级视频、历史影像或移动拍摄场景中，这一前提天然不成立。前馈静态重建方法（如 **pixelSplat**、**MVSplat**、**NoPoSplat**）虽能绕过逐场景优化，却仍假定已知相机内参，且无法处理动态内容。

**2. 离线优化的时序瓶颈。** 基于优化的方法（NeRF 系如 **CoDeF**，3DGS 系如 **4DGS**）需反复迭代整段视频，计算代价与序列长度成正比。即使是最快的优化方法，单帧处理时间也在分钟量级，与在线应用的毫秒级需求相差数个数量级。

**3. 前馈方法的动态建模缺失。** 前馈静态重建方法（**pixelSplat**、**MVSplat**）和在线静态方法（**StreamGS**）仅建模刚性场景，缺乏对非刚性变形、内容出现/消失等动态现象的机制化处理。坐标基的前馈方法（如 **MonST3R**）虽能预测点云，但缺乏可微渲染的端到端质量保证。

### 核心科学问题

上述缺口指向一个根本问题：**能否设计一种前馈网络，直接从无标定的单目视频流中在线预测动态三维高斯场景，而无需相机标定、全局序列访问或逐场景优化？**

解决该问题面临三重技术挑战：
- **无标定输入的空间不确定性**：缺少相机内参意味着像素到三维空间的映射高度欠定，直接回归三维位置极易陷入局部极小。
- **动态时序的一致性建模**：如何在仅访问相邻帧的在线约束下，稳定传播高斯点并处理运动、遮挡和内容变化？
- **在线融合的效率与鲁棒性**：如何以计算高效的方式融合新旧高斯点，既保持持久结构的长期跟踪，又灵活响应新出现和消失的区域？

### StreamSplat 的设计动机

针对上述挑战，StreamSplat 提出三条核心设计原则：

- **正交规范空间替代透视相机模型**：采用共享的正交规范空间统一处理不同相机内参的输入，将相机运动与透视效应交由后续变形场吸收，从根本上解除对相机标定的依赖。
- **概率采样替代确定性回归**：通过预测截断正态分布并从其采样三维偏移，引入受控随机性以促进前馈网络的探索能力，避免确定性回归在欠定空间中的局部极小问题。
- **双向变形场与自适应融合**：双向变形场同时建模前向与后向运动，增强跨帧关联；基于透明度变形的自适应融合机制以软匹配方式传播持久高斯点，自然处理出现/消失内容，实现在线时序一致性。

这一设计使 StreamSplat 成为首个无需相机标定、无需全局序列访问、以近实时速度（约 49 ms/帧）运行的动态三维重建系统，在 DAVIS 基准上以约 1200 倍的速度优势超越离线优化方法，同时保持领先的重建质量。

## 核心创新

StreamSplat 的核心创新在于通过三项关键技术——**概率位置采样**、**双向变形场**和**自适应高斯融合**——将动态三维重建从离线逐场景优化的范式转变为在线的无标定前馈预测范式。这些创新共同解决了现有方法对完整视频序列访问和精确相机标定的依赖，使得系统能够以约1200倍的速度优势（1.48秒 vs 数十分钟，Table 1）从无标定视频流实时重建动态三维高斯场景。

### 创新一：无标定正交规范空间与概率位置采样

**改变槽位：相机模型 → 三维高斯位置预测**

现有动态重建方法（如 DGMarbles、4DGS）依赖标定的透视相机模型，需要已知内参和外参才能进行三维几何推理。StreamSplat 采用**共享的正交规范空间**（Section 3.1），将相机运动和透视效应完全交由后续变形场吸收，从而消除了对相机标定的硬性需求。这一设计使得系统可以直接处理任意无标定视频流，在零样本评估中（DyCheck、NVIDIA Dynamic Scene），StreamSplat 不使用任何相机内参或外参，而基线方法 DGMarbles 仍需提供真实内参或使用 CUT3R 估计（Table 6, Table 7）。

在正交规范空间内，三维高斯位置的预测面临新的挑战：前馈网络需要从单帧RGB-D图像直接推断三维坐标，确定性回归容易陷入局部极小。StreamSplat 引入**概率位置采样机制**（Section 3.1）：对每个像素对齐的三维偏移量，网络预测截断正态分布的均值和协方差参数，然后从中采样偏移：

$$\pmb{o} \sim \mathcal{N}_{[-1,1]}(\pmb{\mu}_p, \pmb{\Sigma}_p)$$

最终三维位置由像素坐标与采样偏移组合，并通过逆深度映射 $g(z)=2/(1+z)$ 计算深度：

$$\pmb{\mu}_i = (u_i + \pmb{o}_{i,0}, v_i + \pmb{o}_{i,1}, g(\pmb{o}_{i,2}))$$

消融实验（Table 4）表明，概率采样相比确定性回归将关键帧 PSNR 从 31.47 提升至 37.83（+6.36 dB），验证了采样策略对前馈三维预测鲁棒性的关键作用。定性结果（Figure 8）进一步显示，移除采样后重建出现明显的几何失真和模糊。

### 创新二：双向变形场

**改变槽位：变形场建模方向**

传统动态三维重建方法通常采用单向变形场，将规范空间的高斯基元变形到当前观测帧。这种单向建模在时序关联上存在信息不对称：前帧信息可以传递到当前帧，但当前帧的新观测难以反向关联到历史状态，导致新出现区域无法有效建模。

StreamSplat 提出**双向变形场**（Section 3.2），联合建模连续帧之间的前向和后向运动：
- **前向变形场**：将前一帧的规范高斯变形到当前时刻，维持历史信息的连续性；
- **后向变形场**：将当前帧的规范高斯变形回前一时刻，使新观测能够与历史状态建立关联。

双向设计的关键优势在于自然处理场景中的出现和消失内容。当新物体进入视野时，后向变形场将其关联到历史帧的空白区域；当物体离开视野时，前向变形场通过后续的不透明度变形机制使其逐渐淡出，而非产生突变或鬼影。

消融实验（Table 4）提供了决定性证据：移除双向变形场（w/o Bi-Deform）后，中间帧重建 PSNR 从 23.66 骤降至 18.89（-4.77 dB），表明双向建模对动态场景的时序一致性至关重要。定性消融（Figure 13）显示，单向变形无法处理快速运动和遮挡区域的几何变化。

### 创新三：基于透明度变形的自适应高斯融合

**改变槽位：时序融合机制**

在线重建的核心难题是如何在逐帧处理中维持高斯点集的长期时序一致性。现有方法通常采用硬分配或迭代优化进行帧间融合，计算开销大且难以处理高斯基元的生命周期变化。

StreamSplat 提出**基于透明度变形的自适应高斯融合机制**（Section 3.2），通过时间依赖的不透明度曲线实现软匹配：

$$\pmb{\alpha}(t) = \pmb{\alpha} \cdot \frac{\sigma\left(-\gamma_0\left(\left|t - t_0\right| - \gamma_1\right)\right)}{\sigma\left(\gamma_0 \cdot \gamma_1\right)}$$

该公式通过参数 $\gamma_0$ 控制过渡速率，$\gamma_1$ 控制消失窗口，自然建模高斯基元的三种生命周期状态（Figure 3）：
- **持久高斯点**：在两帧间保持高不透明度，通过软匹配持续传播；
- **新出现高斯点**：在当前帧获得高不透明度，通过后向变形场关联到历史空白区域；
- **消失高斯点**：随时间衰减不透明度，平滑淡出而非突然消失。

自适应融合的具体流程（Algorithm 2）为：对每对连续帧，Dynamic Decoder 预测双向变形后的高斯集 $\mathcal{G}_{k-1}^+(t)$ 和 $\mathcal{G}_k^-(t)$，然后基于不透明度变形进行软匹配和聚合，更新活跃变形场，最终渲染并剪枝低贡献高斯点。

定性结果（Figure 4）展示了自适应融合的时序一致性：红色/绿色标记的初始帧高斯点在视角和运动变化下跨多帧持续跟踪，验证了机制对长期时序关联的保持能力。消融分析（Figure 8 caption）指出，采用恒定不透明度（无自适应变形）会导致出现/消失区域产生鬼影和模糊。

### 创新四：伪深度监督与自适应权重衰减

**改变槽位：深度监督**

为弥补无标定输入下三维几何推断的歧义性，StreamSplat 引入单目深度估计器（DepthAnythingv2）提供的伪深度作为辅助监督信号。为降低伪深度在精细几何和深度不连续区域的噪声影响，设计了两个关键策略：

1. **尺度-平移不变深度损失**（Equation 3）：通过中位数和平均绝对偏差归一化，使训练对伪深度的绝对尺度不敏感：
   $$\mathcal{L}_{\mathrm{depth}} = \mathbb{E} \Vert \tau(\hat{D}_t) - \tau(D_t) \Vert, \quad \tau(\mathbf{x}) = \frac{\mathbf{x} - \mathrm{median}(\mathbf{x})}{\mathbb{E} \Vert \mathbf{x} - \mathrm{median}(\mathbf{x}) \Vert}$$

2. **自适应深度损失权重衰减**：根据深度预测误差动态调整损失权重：
   $$\hat{\lambda}_{\mathrm{depth}} = \lambda_{\mathrm{depth}} \cdot \sigma\big(- \| \tau(\hat{D}_t) - \tau(D_t) \| / w \big)$$

消融实验（Table 4）显示，移除深度监督（w/o Depth）导致关键帧 PSNR 从 37.83 下降至 36.68（-1.15 dB），证明伪深度监督对几何精度有贡献，但影响小于概率采样和双向变形场，与自适应权重衰减有效抑制了噪声引入的结论一致。

### 创新协同效应

上述四项创新并非孤立作用，而是形成协同增强的闭环（Figure 2）：正交规范空间提供无标定输入的统一几何表示，概率采样在前馈预测中保证三维位置的鲁棒性；双向变形场在统一空间内建模时序运动，自适应融合利用不透明度变形实现高斯点的生命周期管理；伪深度监督则在训练阶段为整个系统提供几何先验。这一协同设计使得 StreamSplat 能够在 49 ms/帧的端到端延迟下（Table 8），以离线优化方法约 1/1200 的时间完成可比甚至更优的动态三维重建质量。

## 整体框架

StreamSplat 的整体管线遵循**前馈编码‑在线融合**的两阶段范式，将无标定的视频流直接转换为支持任意时刻渲染的动态三维高斯场景。其核心设计围绕三个瓶颈突破展开：**概率位置采样**解决无标定输入下三维高斯定位的不确定性，**双向变形场**实现帧间运动的鲁棒建模，**自适应高斯融合**维持跨帧的时序一致性。

### 静态编码器：从单帧到规范三维高斯

对于视频流中的每一帧，系统首先通过一个基于 Transformer 的静态编码器（Static Encoder）将其映射到**正交规范空间**（orthographic canonical space）。该编码器以单帧 RGB‑D 图像为输入，生成规范三维高斯的嵌入表示 h，随后通过轻量级上采样器将 patch 级嵌入扩展为每 2×2‑patch 的高斯标记（Gaussian tokens），最终由 MLP 头解码为位置、旋转、缩放、不透明度和颜色等参数（Figure 2, Section 3.1）。

![[assets/figures/papers/paper_list_l37_https_openreview_net_forum_id_SaiDRQU7Ez/figures/002_Figure_2.jpg]]
*Figure 2: Overview of the StreamSplat. Given a pair of frames*

三维高斯位置的预测是此阶段的关键创新。不同于直接回归确定性偏移量的现有前馈方法，StreamSplat 为每个像素对齐的偏移量预测一个**截断正态分布** $\pmb{o} \sim \mathcal{N}_{[-1,1]}(\pmb{\mu}_p, \pmb{\Sigma}_p)$，并通过概率采样获得偏移量。最终的三维位置通过像素坐标与采样偏移的组合计算得到：

$$\pmb{\mu}_i = (u_i + \pmb{o}_{i,0}, v_i + \pmb{o}_{i,1}, g(\pmb{o}_{i,2}))$$

其中 $g(z) = 2 / (1 + z)$ 为逆深度映射函数，用于改善近相机区域的深度估计精度（Section 3.1）。这一概率采样机制在训练初期促进探索、避免局部极小，在推理时则通过多次采样‑平均策略稳定收敛，是 StreamSplat 在无标定条件下实现鲁棒重建的关键因果旋钮之一。

### 动态解码器：双向变形场与时序关联

静态编码器为连续的两帧（$t_{k-1}$ 和 $t_k$）分别生成规范高斯嵌入后，动态解码器（Dynamic Decoder）负责建模帧间的运动与外观变化。该解码器由一个条件于 DINOv2 特征的 Transformer 组成，接收两帧的嵌入并输出**变形嵌入**（Deformation Embeddings）。变形嵌入与静态标记拼接后，经一个 2 层 MLP 头解码为每个高斯的**速度**和**不透明度系数**（Section 3.2）。

StreamSplat 的动态建模核心在于**双向变形场**的设计。传统单向变形仅将规范高斯变形到当前帧，难以处理出现/消失内容。StreamSplat 联合建模前向和后向运动：
- **前向场**将前一帧的高斯 $\mathcal{G}_{k-1}$ 变形到当前时刻 $t$，产生 $\mathcal{G}_{k-1}^+(t)$；
- **后向场**将当前帧的高斯 $\mathcal{G}_k$ 变形回前一帧，产生 $\mathcal{G}_k^-(t)$。

这种双向机制增强了跨帧关联，使系统能够自然处理新出现和消失的高斯点，是中间帧重建质量的关键保障（消融实验中移除双向变形场使中间帧 PSNR 从 23.66 骤降至 18.89，Table 4）。

### 自适应高斯融合：透明度变形驱动的软匹配

双向变形场产生两组高斯后，StreamSplat 通过**自适应高斯融合**机制将它们合并为统一的动态场景表示。该机制的核心是**时间依赖的不透明度变形**：

$$\pmb{\alpha}(t) = \pmb{\alpha} \cdot \frac{\sigma\left(-\gamma_0\left(\left|t - t_0\right| - \gamma_1\right)\right)}{\sigma\left(\gamma_0 \cdot \gamma_1\right)}$$

其中 $\gamma_0$ 控制过渡速率，$\gamma_1$ 定义消失窗口。该公式为每个高斯赋予一条随时间变化的不透明度曲线，自然区分三种生命周期状态（Figure 3）：
- **持久高斯**：在两帧间保持高不透明度，通过软匹配实现跨帧传播；
- **新出现高斯**：在 $t$ 接近当前帧时不透明度上升，由后向场引入；
- **消失高斯**：在 $t$ 远离其创建时刻时不透明度衰减，被自然剪枝。

融合过程采用基于不透明度的软匹配策略，而非硬分配或迭代优化。Figure 4 的定性结果表明，该机制能够在视角和运动变化下维持高斯的长期时序一致性——初始帧标记的高斯点（红色/绿色）在后续帧中持续跟踪目标区域。

### 在线推理循环

StreamSplat 的在线推理按照 Algorithm 2 逐帧执行：对于每对新帧，通过动态解码器获得双向变形高斯集后，系统依次执行 **UPDATE**（将前向变形场更新到活跃高斯集）、**聚合与融合**（合并后向高斯集）、**渲染**（从给定帧和任意中间时刻生成图像）和**剪枝**（移除不透明度低于阈值的高斯点）。这一流程使 StreamSplat 能够在单块 A100 GPU 上以 49 ms/帧的端到端延迟运行，相比离线优化方法实现约 1200 倍加速（Table 1, Table 8）。

### 训练策略

StreamSplat 采用两阶段训练：**静态阶段**仅训练静态编码器，损失函数结合光度重建损失（L2+LPIPS）和尺度‑平移不变的深度损失：

$$\mathcal{L}_{\mathrm{static}} = \mathcal{L}_{\mathrm{recon}}(\hat{I}_t, I_t) + \lambda_{\mathrm{depth}} \mathcal{L}_{\mathrm{depth}}(\hat{D}_t, D_t)$$

其中深度损失通过中位数和平均绝对偏差归一化，使训练对伪深度的绝对尺度不敏感：

$$\mathcal{L}_{\mathrm{depth}} = \mathbb{E} \Vert \tau(\hat{D}_t) - \tau(D_t) \Vert, \quad \tau(\mathbf{x}) = \frac{\mathbf{x} - \mathrm{median}(\mathbf{x})}{\mathbb{E} \Vert \mathbf{x} - \mathrm{median}(\mathbf{x}) \Vert}$$

**动态阶段**冻结静态编码器，训练动态解码器，损失扩展为对中间时刻重建图像施加光度、深度和前景遮罩损失：

$$\mathcal{L}_{\mathrm{dynamic}} = \mathbb{E}_t \left[ \mathcal{L}_{\mathrm{recon}}(\hat{I}_t, I_t) + \lambda_{\mathrm{depth}} \mathcal{L}_{\mathrm{depth}}(\hat{D}_t, D_t) + \lambda_{\mathrm{mask}} \mathcal{L}_{\mathrm{mask}}(\hat{I}_t \odot M_t, I_t \odot M_t) \right]$$

此外，深度损失权重采用自适应衰减因子 $\hat{\lambda}_{\mathrm{depth}} = \lambda_{\mathrm{depth}} \cdot \sigma(- \| \tau(\hat{D}_t) - \tau(D_t) \| / w)$，根据深度预测误差动态调整，以降低单目深度估计器（DepthAnythingv2）伪深度噪声的影响（Section 3.3）。

### 补充图表

![[assets/figures/papers/paper_list_l37_https_openreview_net_forum_id_SaiDRQU7Ez/figures/013_Figure_9.jpg]]
*Figure 9: StreamSplat framework. Given a pair of frames, we first encode them using the Static Encoder to produce canonical 3D Gaussians (Section 3.1), and then pass the 3DGS Embeddings to the Dynamic Decoder to predict the deformation field (Section 3.2). The resulting dynamic 3D Gaussians can be rendered at arbitrary time to produce RGB images and depth maps*

## 核心模块与公式推导

### 3.1 正交规范空间与概率位置采样

StreamSplat 采用**共享的正交规范空间**作为三维高斯的统一坐标系，避免了对相机内参的显式依赖。透视效应与相机运动由后续的变形场吸收，使系统天然支持无标定输入。

对每一帧，Transformer 静态编码器从 RGB-D 输入生成规范三维高斯的嵌入表示。为从前馈预测中获得鲁棒的三维位置，StreamSplat 引入**概率位置采样**机制：对每个像素对齐的高斯点，预测其在规范空间中的偏移量分布，而非直接回归确定值。

**像素对齐三维位置计算**：
$$
\pmb{\mu}_i = (u_i + \pmb{o}_{i,0},\; v_i + \pmb{o}_{i,1},\; g(\pmb{o}_{i,2}))
$$

其中 $(u_i, v_i)$ 为像素坐标，$\pmb{o}_i$ 为预测的三维偏移，深度映射函数为：
$$
g(z) = \frac{2}{1+z}
$$

该逆深度映射使网络更关注近相机区域的深度估计精度。

**概率偏移采样**：
$$
\pmb{o} \sim \mathcal{N}_{[-1,1]}(\pmb{\mu}_p, \pmb{\Sigma}_p)
$$

网络预测截断正态分布的均值 $\pmb{\mu}_p$ 和协方差 $\pmb{\Sigma}_p$，从中采样偏移量。这一设计在训练初期促进探索，避免确定性回归陷入局部极小；在推理时则提供更稳定的前馈预测。消融实验（Table 4）证实，概率采样相比确定性回归将关键帧 PSNR 从 31.47 提升至 37.83（+6.36 dB）。

### 3.2 双向变形场

为建模动态场景的时序演化，StreamSplat 在连续两帧间构建**双向变形场**：

- **前向变形**：将前一帧的规范高斯变形至当前时刻，捕捉从历史到当前的场景运动。
- **后向变形**：将当前帧的规范高斯反向变形至前一帧时刻，建立反向关联。

双向设计使得模型能够同时利用两帧的信息进行跨帧匹配，对出现/消失的内容具有天然鲁棒性。动态解码器以 DINOv2 视觉特征为条件，通过 Transformer 生成变形嵌入，再经 2 层 MLP 头解码为每个高斯点的速度和不透明度系数。消融实验（Table 4）表明，移除双向变形场后，中间帧重建 PSNR 从 23.66 骤降至 18.89，验证了双向建模对动态场景的关键作用。

### 3.3 自适应高斯融合与不透明度变形

为实现跨帧高斯点的稳定传播，StreamSplat 提出基于**不透明度变形**的自适应高斯融合机制。核心思想是通过时间依赖的不透明度曲线，隐式定义每个高斯点的“生命周期”，从而在融合时自然区分持久、新出现和消失的高斯点。

**时间依赖不透明度变形公式**：
$$
\pmb{\alpha}(t) = \pmb{\alpha} \cdot \frac{\sigma\left(-\gamma_0\left(\left|t - t_0\right| - \gamma_1\right)\right)}{\sigma\left(\gamma_0 \cdot \gamma_1\right)}
$$

其中 $\pmb{\alpha}$ 为原始不透明度，$t_0$ 为高斯点的参考时刻，$\gamma_0$ 控制不透明度衰减速率，$\gamma_1$ 定义维持全不透明的时间窗口，$\sigma(\cdot)$ 为 sigmoid 函数。该公式使高斯点在 $|t-t_0| < \gamma_1$ 区间内保持可见，超出后平滑衰减至零，从而实现对出现/消失区域的软处理，避免硬分配带来的鬼影和模糊（Figure 8 定性验证）。

融合过程将前向变形的高斯集 $\mathcal{G}_{k-1}^+(t)$ 与后向变形的高斯集 $\mathcal{G}_k^-(t)$ 进行基于不透明度的软匹配，维持持久高斯的跨帧一致性。Figure 4 展示了标记高斯点在视角和运动变化下的持续跟踪效果。

![[assets/figures/papers/paper_list_l37_https_openreview_net_forum_id_SaiDRQU7Ez/figures/004_Figure_4.jpg]]
*Figure 4: Persistent Gaussians across frames. Red/green-marked Gaussians from initial frame are propagated across frames, showing that adaptive Gaussian fusion preserves long-term temporal consistency under viewpoint and motion changes. Videos are available on the project website*

### 3.4 训练损失函数

**静态阶段**训练静态编码器，损失函数结合光度重建与深度监督：
$$
\mathcal{L}_{\mathrm{static}} = \mathcal{L}_{\mathrm{recon}}(\hat{I}_t, I_t) + \lambda_{\mathrm{depth}} \mathcal{L}_{\mathrm{depth}}(\hat{D}_t, D_t)
$$

其中 $\mathcal{L}_{\mathrm{recon}}$ 为 L2 与 LPIPS 的组合损失。

**尺度-平移不变深度损失**，用于处理单目深度估计器（DepthAnythingv2）产生的伪深度噪声：
$$
\mathcal{L}_{\mathrm{depth}} = \mathbb{E} \Vert \tau(\hat{D}_t) - \tau(D_t) \Vert, \quad \tau(\mathbf{x}) = \frac{\mathbf{x} - \mathrm{median}(\mathbf{x})}{\mathbb{E} \Vert \mathbf{x} - \mathrm{median}(\mathbf{x}) \Vert}
$$

通过中位数和平均绝对偏差归一化，使损失对伪深度的绝对尺度和全局偏移不敏感。

**动态阶段**对中间时刻的重建施加额外的前景遮罩损失，引导模型关注运动区域：
$$
\mathcal{L}_{\mathrm{dynamic}} = \mathbb{E}_t \left[ \mathcal{L}_{\mathrm{recon}}(\hat{I}_t, I_t) + \lambda_{\mathrm{depth}} \mathcal{L}_{\mathrm{depth}}(\hat{D}_t, D_t) + \lambda_{\mathrm{mask}} \mathcal{L}_{\mathrm{mask}}(\hat{I}_t \odot M_t, I_t \odot M_t) \right]
$$

此外，深度损失权重采用**自适应衰减因子**动态调节：
$$
\hat{\lambda}_{\mathrm{depth}} = \lambda_{\mathrm{depth}} \cdot \sigma\big(- \| \tau(\hat{D}_t) - \tau(D_t) \| / w \big)
$$

当深度预测误差较大时自动降低深度损失的贡献，抑制噪声伪影的传播。

### 补充图表

![[assets/figures/papers/paper_list_l37_https_openreview_net_forum_id_SaiDRQU7Ez/figures/003_Figure_3.jpg]]
*Figure 3: Our opacity deformation jointly models persistent, emerging, and vanishing Gaussians*

## 实验与分析

### 核心性能：DAVIS动态场景重建

StreamSplat在DAVIS基准上展现了显著的性能优势，同时实现了近实时推理。在关键帧重建任务上，StreamSplat达到**37.83 PSNR / 0.982 SSIM / 0.016 LPIPS**，相比离线优化方法DGMarbles（28.38 PSNR）提升**+9.45 dB**。在更具挑战性的中间4帧重建任务上，StreamSplat取得**23.66 PSNR / 0.684 SSIM / 0.193 LPIPS**，同样优于DGMarbles（21.33 PSNR）。速度方面，StreamSplat以**0.049秒/帧**的端到端延迟完成重建与渲染，30帧总耗时仅约1.48秒，而DGMarbles等离线优化方法需数十分钟，速度提升约**1200倍**。Table 1汇总了上述结果。

在8帧间隔插值任务中，StreamSplat取得**22.10 PSNR**，超越所有基线方法，包括AMT（21.09 PSNR）、RIFE、FILM等2D视频插值方法，验证了其在长时序跨度下建模动态场景的能力（Table 2）。

![[assets/figures/papers/paper_list_l37_https_openreview_net_forum_id_SaiDRQU7Ez/figures/007_Table_2.jpg]]
*Table 2: 8-frame interval interpolation results*

### 静态场景新视角合成

在RE10K静态场景基准上，StreamSplat以2张输入视图预测5张新视角，取得**24.68 PSNR**，优于DGMarbles（23.40 PSNR），证明其静态编码器在前馈3DGS重建上的竞争力（Table 3）。

![[assets/figures/papers/paper_list_l37_https_openreview_net_forum_id_SaiDRQU7Ez/figures/010_Table_3.jpg]]
*Table 3: RE10K results. PSNR↑/LPIPS↓ for 2 given views and 5 novel views*

### 零样本泛化

在DyCheck iPhone数据集上，StreamSplat在不使用任何相机内参或外参的条件下取得**12.37 PSNR**，显著优于同样无标定设置的DGMarbles w/o cam（9.76 PSNR）。在NVIDIA Dynamic Scene数据集上，StreamSplat取得**16.30 PSNR**，优于使用CUT3R估计相机参数的DGMarbles（13.91 PSNR）。这两组零样本实验验证了正交规范空间对无标定输入的有效性（Table 6, Table 7）。

![[assets/figures/papers/paper_list_l37_https_openreview_net_forum_id_SaiDRQU7Ez/figures/017_Table_6.jpg]]
*Table 6: DyCheck results. We report PSNR↑/LPIPS↓ on novel view synthesis*

![[assets/figures/papers/paper_list_l37_https_openreview_net_forum_id_SaiDRQU7Ez/figures/018_Table_7.jpg]]
*Table 7: NVIDIA Dynamic Scenes results. We report PSNR↑/LPIPS↓ on novel view synthesis*

### 消融实验

Table 4和Figure 8揭示了各核心组件的贡献：

- **概率位置采样**是最关键的组件：移除概率采样改用确定性回归后，关键帧PSNR从37.83骤降至31.47（**-6.36 dB**），表明从截断正态分布中采样偏移对前馈3DGS位置预测的鲁棒性至关重要。
- **双向变形场**对动态建模不可或缺：移除双向变形后，中间帧PSNR从23.66降至18.89（**-4.77 dB**），证明仅依赖单向变形无法有效捕捉跨帧运动。
- **深度监督**提供辅助信号：移除伪深度监督导致关键帧PSNR下降至36.68（**-1.15 dB**），表明尺度-平移不变深度损失对几何学习有正向贡献。
- **自适应高斯融合**：采用恒定不透明度替代时间依赖的不透明度变形会导致出现/消失区域产生鬼影和模糊（Figure 8分析），证实了基于透明度变形的软匹配机制对处理动态内容变化的必要性。

### 失败模式与局限性

1. **深度噪声**：依赖外部单目深度估计器（DepthAnythingv2）产生的伪深度，在精细几何和深度不连续区域可能引入噪声。虽采用自适应权重衰减（公式 $\hat{\lambda}_{\mathrm{depth}} = \lambda_{\mathrm{depth}} \cdot \sigma(-\| \tau(\hat{D}_t) - \tau(D_t) \| / w)$）缓解，但训练数据扩充以支持内部深度精化仍是重要方向。

2. **长时序建模不足**：双向变形场仅在两帧窗口内训练，对于快速运动或长时间遮挡的场景，早期帧信息可能丢失，无法充分利用更长时序上下文。

3. **正交投影残余畸变**：正交规范空间赋予无标定鲁棒性，但在近距离具有强烈透视效应的场景下可能引入相机模型不对齐。当前依赖变形场补偿，但残余畸变仍然存在。

### 运行时分析

Table 8给出了StreamSplat在单块A100 GPU上的模块级耗时分解，端到端总延迟为49 ms/帧，其中静态编码器、动态解码器和高斯渲染各自占据合理比例，整体架构实现了近实时的在线推理能力。

### 补充图表

![[assets/figures/papers/paper_list_l37_https_openreview_net_forum_id_SaiDRQU7Ez/figures/006_Table_1.jpg]]
*Table 1: Quantitative results on DAVIS. † denotes results reported in the original papers*

![[assets/figures/papers/paper_list_l37_https_openreview_net_forum_id_SaiDRQU7Ez/figures/011_Figure_8.jpg]]
*Figure 8: Ablation. w/o sampling: deterministic position prediction; w/o depth: no depth supervision*

![[assets/figures/papers/paper_list_l37_https_openreview_net_forum_id_SaiDRQU7Ez/figures/020_Figure_13.jpg]]
*Figure 13: Ablation. w/o bi.: without bidirectional deformation field. Blue box: given frames; Red box: novel frames*

![[assets/figures/papers/paper_list_l37_https_openreview_net_forum_id_SaiDRQU7Ez/figures/021_Table_8.jpg]]
*Table 8: Runtime breakdown of StreamSplat on a single A100 GPU*

## 方法谱系与知识库定位

### 1. 问题谱系：从离线优化到在线前馈

动态三维重建长期受限于**逐场景离线优化**范式。早期基于神经辐射场（NeRF）的方法如 **Omnimotion**、**RoDynRF**、**CoDeF** 需要完整视频序列访问和精确相机标定，通过数小时的梯度下降拟合单个场景。三维高斯泼溅（3DGS）的引入催生了 **4DGS**、**Splatter a Video**、**DGMarbles** 等动态重建方法，将优化时间压缩至数十分钟，但仍无法摆脱对完整序列与标定信息的依赖。这条技术路线的核心瓶颈在于：**离线优化天然排斥流式输入，且相机标定假设限制了实际部署**。

前馈方法试图打破这一瓶颈。**pixelSplat**、**MVSplat**、**NoPoSplat** 等静态场景前馈重建工作证明了从少量视图直接预测三维高斯的可行性，但它们仅处理静态场景。**MonST3R** 以点云形式进行前馈动态重建，但缺乏显式的三维表示和时序一致性建模。**StreamGS** 是首个在线静态3DGS重建方法，却无法建模场景动态。StreamSplat 正是在此交汇点上提出：**将前馈预测的效率优势与动态场景建模需求结合，同时解除相机标定约束**。

### 2. 关键技术定位

#### 2.1 正交规范空间与无标定重建

StreamSplat 采用**共享的正交规范空间**（shared orthographic canonical space），这一设计延续了 Wang et al. (2023)、Sun et al. (2024)、Shen et al. (2025b) 的思路，将不同相机内参下的观测统一到同一坐标框架。与依赖标定透视相机的 **DGMarbles** 等离线方法形成鲜明对比：后者需要已知内参和外参，而 StreamSplat 将相机运动与透视效应完全交由变形场吸收，从而在零样本场景（DyCheck、NVIDIA Dynamic Scene）中无需任何相机元数据即可运行。

这一选择的代价是：在近距离强透视场景下，正交投影假设与真实成像几何存在偏差。尽管变形场可部分补偿，残余畸变仍然存在。这是 StreamSplat 与透视基线（如使用 GT 内参的 DGMarbles）在零样本评估中性能差距的部分来源（DyCheck 上 12.37 vs 9.76 PSNR，差距虽显著但绝对数值偏低）。

#### 2.2 概率位置采样 vs 确定性回归

传统前馈方法（如 pixelSplat、MVSplat）直接回归三维高斯的偏移量，属于**确定性预测**。StreamSplat 引入**概率位置采样**：从预测的截断正态分布 $\pmb{o} \sim \mathcal{N}_{[-1,1]}(\pmb{\mu}_p, \pmb{\Sigma}_p)$ 中采样偏移，促进训练早期的探索并避免局部极小。这一设计借鉴了强化学习中的探索-利用权衡思想，在前馈三维重建中尚属首次应用。

消融实验验证了其决定性作用：移除概率采样（退化为确定性回归）导致关键帧 PSNR 从 37.83 骤降至 31.47（−6.36 dB），说明在无标定条件下，概率建模对位置预测的鲁棒性至关重要。

#### 2.3 双向变形场 vs 单向变形

现有动态3DGS方法（如 4DGS、DGMarbles）通常采用**单向变形**：将规范高斯变形到当前帧。StreamSplat 提出**双向变形场**：前向场将前一帧高斯变形到当前时刻，后向场将当前帧高斯变形回前一帧。这种联合建模增强了跨帧关联，并自然处理内容的出现与消失。

消融结果极具说服力：移除双向变形场（仅保留单向）使中间帧重建 PSNR 从 23.66 暴跌至 18.89（−4.77 dB），证明双向建模对动态场景的时序一致性不可或缺。这一设计在概念上类似于光流估计中的前后一致性检查，但在三维高斯变形领域是首次系统化应用。

#### 2.4 自适应高斯融合 vs 硬匹配

时序融合是动态重建的核心难题。现有方法多采用**硬分配**或迭代重优化，计算成本高且对噪声敏感。StreamSplat 的**自适应高斯融合**基于时间依赖的透明度变形：

$$\pmb{\alpha}(t) = \pmb{\alpha} \cdot \frac{\sigma\left(-\gamma_0\left(\left|t - t_0\right| - \gamma_1\right)\right)}{\sigma\left(\gamma_0 \cdot \gamma_1\right)}$$

通过参数 $\gamma_0$、$\gamma_1$ 控制高斯的可见性曲线，实现**软匹配**：持久高斯保持高透明度，新出现的高斯从低透明度渐入，消失的高斯渐出至零。这一机制隐式传播持久高斯点，避免了显式匹配的脆弱性。

该设计受 Zhao et al. (2024) 高斯生命周期概念的启发，但将其从离线后处理提升为在线前馈机制。Figure 4 的定性结果（红色/绿色标记的高斯跨帧持续跟踪）直观展示了其有效性。移除自适应变形（采用恒定不透明度）会导致出现/消失区域的鬼影和模糊。

### 3. 适用边界与局限

#### 3.1 深度先验依赖

StreamSplat 依赖外部单目深度估计器（DepthAnythingv2）提供的伪深度监督。虽然采用尺度-平移不变损失和自适应衰减权重降低噪声影响，但在精细几何和深度不连续区域仍可能引入伪影。消融显示移除深度监督导致 PSNR 下降约 1.15 dB，表明深度先验有贡献但非绝对主导。训练数据扩充以支持**内部深度精化**是重要改进方向。

#### 3.2 时序窗口限制

双向变形场仅在两帧窗口内训练，对于快速运动或长时间遮挡的场景，早期帧的信息可能丢失。这与基于全局优化的方法（如 DGMarbles 可访问完整序列）形成对比。如何设计高效的自适应机制以选择和融合跨多帧历史的高斯点，是提升长时序建模能力的关键开放问题。

#### 3.3 相机模型不对齐

正交规范空间赋予了无标定输入的鲁棒性，但在近距离强透视场景下引入的残余畸变仍需关注。未来可探索**轻量内参估计**或**透视感知校正模块**，在保持无标定优势的同时缓解正交投影偏差。

### 4. 与相邻领域的边界

StreamSplat 与 **2D视频插值**方法（AMT、RIFE、FILM、LDMVFI、VIDIM）有本质区别：后者仅操作像素空间，不建模三维几何，无法支持新视角合成。StreamSplat 在8帧间隔插值任务上以 22.10 PSNR 超越 AMT 的 21.09，证明三维几何建模对长间隔时序预测的优势。

与**静态前馈3DGS**方法（pixelSplat、MVSplat、NoPoSplat）相比，StreamSplat 在 RE10K 静态场景上以 24.68 PSNR 达到可比甚至更优的性能，同时额外支持动态场景——这得益于其统一的静态编码器-动态解码器架构。

### 5. 开放问题

1. **内部深度精化**：如何扩展训练数据使模型减少对单目深度先验的依赖，实现端到端的深度与重建联合优化？
2. **长时序记忆**：如何超越两帧窗口，设计高效的多帧高斯选择与融合机制，在快速运动或长遮挡下保留更多时序信息？
3. **透视感知增强**：能否结合轻量级相机内参估计或透视感知校正模块，在保持无标定优势的同时缓解正交投影带来的残余畸变？
4. **计算效率提升**：当前 49 ms/帧的延迟已接近实时（~20 FPS），但距离移动端部署仍有距离；模型压缩与加速是实际应用的重要方向。

## 原文 PDF

![[paperPDFs/ICLR_2026/StreamSplat_Towards_Online_Dynamic_3D_Reconstruction_from_Uncalibrated_Video_Str_ddaf0a5cb355.pdf]]