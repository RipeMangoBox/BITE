---
title: Occluded Human Body Capture with Frequency Domain Denoising Prior
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/Occluded_Human_Body_Capture_with_Frequency_Domain_Denoising_Prior.pdf
project_link: null
code_link: "https://github.com/boycehbz/FreqMotion"
aliases:
- FFDDP
- OHBCFDDP
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
core_operator: 利用离散小波变换(DWT)将遮挡运动分解为频域子带，并通过频域扩散模型学习可靠可见关键点与遮挡部分之间的时空依赖，选择有效小波系数以重构去噪后的运动。
primary_logic: 遮挡人体运动的关节在频域呈现周期性和一致动量，通过频域扩散模型将运动捕获转化为小波系数选择过程，能从可靠的部分观测中恢复准确、连贯的3D运动。
claims:
- 遮挡关节运动在频域保持周期性模式（Fig.1），可用来缓解长期遮挡的影响。
- 在OcMotion数据集上，所提方法在MPJPE、PA-MPJPE和加速度误差上显著优于现有视频方法（Tab.2）。
- 消融实验表明频域去噪先验和小波系数选择模块对性能提升至关重要（Tab.4）。
- OcMotion 上 MPJPE = 79.2
---

# Occluded Human Body Capture with Frequency Domain Denoising Prior

> [!tip] 核心洞察
> 遮挡人体运动的关节在频域呈现周期性和一致动量，通过频域扩散模型将运动捕获转化为小波系数选择过程，能从可靠的部分观测中恢复准确、连贯的3D运动。

| 字段 | 内容 |
|------|------|
| 中文题名 | 基于频域去噪先验的遮挡人体运动捕获 |
| 英文题名 | Occluded Human Body Capture with Frequency Domain Denoising Prior |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://openaccess.thecvf.com/content/CVPR2026/html/Huang_Occluded_Human_Body_Capture_with_Frequency_Domain_Denoising_Prior_CVPR_2026_paper.html) · [Code](https://github.com/boycehbz/FreqMotion) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction |
| Method | FreqMotion (Frequency Domain Denoising Prior) |
| Dataset | OcMotion, 3DPW, 3DPW-OC, Hi4D |

> [!tip] 效果简介
> - OcMotion 上，MPJPE 79.2 vs — (—)；PA-MPJPE 51.7 vs — (—)；Accel 20.1 vs — (—)。
> - 3DPW 上，MPJPE 67.3 vs — (—)；PA-MPJPE 44.8 vs — (—)；PVE 75.3 vs — (—)。
> - 3DPW-OC 上，MPJPE 63.1 vs — (—)。

## 概要

从单目视频中恢复遮挡人体的三维运动是计算机视觉中长期存在的难题。现有方法大多依赖时域运动先验，但在严重或长期遮挡下，时域信息高度缺失，导致重建结果过平滑或不可靠。本文观察到，即使人体被部分遮挡，其关节运动在频域中仍保持周期性和一致的动量模式（Fig.1）。基于这一关键洞察，**FreqMotion** 将遮挡人体运动捕获重新定义为**小波系数选择过程**，提出了一种**频域去噪先验**框架。

该方法的核心思路是：利用离散小波变换（DWT）将含遮挡的2D关键点序列分解为多尺度频域子带，再通过一个频域扩散模型从可靠可见关键点中学习时空依赖关系，选择有效的小波系数以重建去噪后的运动。与直接回归SMPL参数的时域方法不同，FreqMotion 在频域中分离并抑制由遮挡引入的低频和高频噪声，从而恢复准确、连贯的3D人体运动。

在贡献层面，本文的主要创新包括：
- 提出首个面向遮挡人体运动捕获的**频域去噪先验**，将运动重建转化为小波系数选择问题；
- 设计了**两阶段训练框架**：先训练2D频域扩散先验，再冻结编码器并接入3D解码器预测SMPL参数；
- 构建了**OcMotion数据集**，包含30万帧真实遮挡场景下的多视角视频及精确3D标注。

实验结果表明，FreqMotion 在多个遮挡基准上取得了领先性能。在 OcMotion 数据集上，MPJPE 达到 79.2 mm，PA-MPJPE 为 51.7 mm；在 3DPW-OC 上，MPJPE 为 63.1 mm，加速度误差仅 9.1 mm/s²。消融实验证实，频域去噪先验和3D扩散过程对性能提升至关重要，DWT 的多尺度分析能力优于传统的 DCT 方法。

从单目视频中捕获三维人体运动是计算机视觉的核心任务，在虚拟现实、人机交互和运动分析等领域具有广泛应用。然而，现实场景中普遍存在的遮挡——无论是物体遮挡还是人际遮挡——严重破坏了视觉观测的完整性，使得从部分可见的人体区域推断完整的三维姿态和运动变得极具挑战。

现有方法主要依赖**时域运动先验**来应对遮挡。例如，**VIBE**（Kocabas et al., CVPR 2020）和**MPS-Net**（Luo et al., ACCV 2020）利用时序Transformer或循环网络建模帧间依赖，在短期遮挡下能够保持一定的运动连贯性。**PARE**（Kocabas et al., ICCV 2021）和**GLAMR**（Yuan et al., CVPR 2022）则显式地考虑遮挡问题，通过遮挡感知的特征聚合或全局运动优化来提升鲁棒性。**DPMesh**（Zhu et al., CVPR 2024）进一步引入扩散先验，从图像观测中恢复被遮挡的人体网格。然而，这些方法的核心瓶颈在于：**时域运动先验在长期遮挡下无法提供足够的信息**。当遮挡持续多帧时，可见关键点数量急剧减少，时域模型缺乏足够的约束来推断被遮挡关节的运动轨迹，导致重建结果趋向于过平滑或不可靠的平均姿态——模型实际上在“猜测”而非“推断”。

本文从一个关键观察出发重新审视这一问题：**尽管人体关节在遮挡下不可见，其运动在频域中却保持着周期性和一致性模式**。如 Figure 1 所示，在遮挡序列中，SMPL模型的左右膝盖姿态参数沿X轴的轨迹虽然存在局部缺失，但整体呈现出清晰的周期性波动。这一现象暗示，频域表示天然地捕捉了人体运动的本质结构——步态周期、肢体摆动频率等——这些模式对局部遮挡具有内在的鲁棒性。相比之下，时域方法直接处理逐帧的关节坐标，遮挡引入的噪声和缺失会直接破坏局部时序依赖，而频域方法则可以将遮挡的影响分散到不同频率分量上，使得低频的周期性结构得以保留。

基于这一洞察，本文提出**FreqMotion**，一种基于频域去噪先验的遮挡人体运动捕获方法。核心思想是将遮挡人体运动捕获重新定义为**小波系数选择过程**：利用离散小波变换（DWT）将运动序列分解为多尺度频域子带，通过频域扩散模型学习可靠可见关键点与遮挡部分之间的时空依赖关系，选择有效的小波系数以重构去噪后的运动。这一范式转变的关键优势在于：频域先验能够同时处理低频和高频噪声，而DWT的多尺度分析能力使其既能保留运动的全局周期性结构，又能恢复局部的精细动态细节。

综上所述，本文的动机可概括为三个层面：
1. **问题层面**：长期遮挡是单目人体运动捕获的核心瓶颈，时域先验在信息极度缺失时表现乏力；
2. **洞察层面**：人体运动在频域呈现周期性模式，频域表示对遮挡具有天然鲁棒性；
3. **方法层面**：通过频域扩散模型将运动捕获转化为小波系数选择，从可靠的部分观测中恢复准确、连贯的三维运动。

## 核心方法与创新机理

FreqMotion 的核心创新在于将遮挡人体运动捕获重新定义为**频域小波系数选择过程**，而非传统方法中依赖时域运动先验的回归或补全。这一范式转换由四个关键设计槽位（changed slots）共同支撑，形成从输入表示到训练策略的系统性创新。

### 1. 频域去噪先验替代时域运动先验

现有视频方法（如 **VIBE** (Kocabas et al., CVPR 2020)、**MPS-Net** (Luo et al., ACCV 2020)）主要使用时序回归或时域运动先验来约束姿态估计。然而，在长期遮挡下，时域信息被严重破坏，导致重建运动过平滑或不可靠。FreqMotion 的核心洞察在于：**遮挡关节的运动轨迹在频域中保持周期性和一致性模式**（Fig.1），这为从部分观测中恢复完整运动提供了更鲁棒的信号。

基于此，FreqMotion 采用离散小波变换（DWT）将 2D 关键点序列沿时空维度分解为四个子带（LL, LH, HL, HH），并通过一个基于 Transformer 的频域扩散模型学习每个子带的**系数选择图**（coefficient map），选择有效频率分量以重构去噪后的运动。这一设计将运动先验从“学习运动轨迹的时序规律”转变为“学习频域子带中的可靠系数分布”，从根本上改变了先验的信息来源和表达形式。

### 2. 遮挡关键点的不确定性建模

传统方法对遮挡关键点的处理通常是直接丢弃或直接使用低置信度预测，这会导致信息损失或引入错误信号。FreqMotion 提出对低置信度关键点构建**高斯分布**来显式建模其不确定性：对于置信度低于预设阈值的遮挡关节，将其坐标建模为高斯分布，从中采样噪声关键点与可靠可见关键点拼接后输入模型。这一设计使得遮挡区域的信息以概率形式保留，而非被简单丢弃，为后续频域去噪提供了信息基础。

### 3. 多尺度 DWT 频率表示替代时域或 DCT 表示

在频率表示的选型上，部分方法采用离散余弦变换（DCT）丢弃高频分量来平滑运动，但这会损失细节信息。FreqMotion 选择 **DWT 多尺度分析**，其关键优势在于：DWT 同时保留时间和频率的局部信息，能够捕捉遮挡运动中并存的低频整体趋势和高频细节噪声。消融实验（Table 4）直接验证了这一选择：将 DWT 替换为 DCT 后，3DPW 上的 MPJPE 从 48.5 升至 51.6，表明 DWT 的多尺度分解能力对性能至关重要。

### 4. 两阶段训练策略与扩散过程复用

FreqMotion 采用**两阶段训练**策略：第一阶段训练 2D 频域扩散先验（编码器 + 2D 解码器），以真实 2D 关键点为监督信号学习频域去噪；第二阶段冻结编码器，替换为 3D 解码器预测 3D 运动子带和 SMPL 形状参数，同时**复用同一扩散过程**。这与单阶段直接回归 3D 姿态参数的方法（如 VIBE）形成对比，其优势在于：2D 频域先验可以在大规模 2D 数据上充分预训练，降低了 3D 标注数据的需求；同时，扩散过程的复用使得 2D 去噪能力可以迁移到 3D 重建中，提升了训练效率和重建质量。

### 创新协同机制

上述四个创新槽位并非孤立存在，而是形成了一条完整的因果链路：**不确定性建模**保留了遮挡区域的信息 → **DWT 分解**将混合了噪声和有效信号的运动转换到频域 → **频域扩散模型**通过系数选择实现去噪 → **两阶段训练**将 2D 去噪能力迁移至 3D 重建。消融实验（Table 4）证实了这一协同效应：仅使用时域回归（Temporal Regression）的基线在 3DPW 上 MPJPE 为 54.3；加入去噪关键点 + DWT 后降至 49.6；进一步加入频域先验和 3D 扩散过程后达到最优的 48.5，验证了每个创新槽位的独立贡献和组合增益。

FreqMotion 的完整流程如图2所示，核心思路是将遮挡人体运动捕获重新表述为**小波系数选择过程**。给定一段存在遮挡的 RGB 视频，系统首先检测 2D 关键点，并对遮挡区域的低置信度关键点构建高斯分布以显式建模不确定性。随后，将可见关键点与从分布中采样的遮挡关键点拼接，沿时空维度通过离散小波变换（DWT）分解为多个频率子带。接下来，一个基于 Transformer 的频域扩散模型学习各子带的有效系数映射，通过反向扩散过程逐步去噪并重建干净的 2D 关键点序列。该 2D 频域先验训练完成后，冻结编码器并接入 3D 解码器，在同一个扩散过程中预测 3D 运动的 SMPL 参数，最终通过逆小波变换（iDWT）重建出连贯的 3D 人体运动。

### 输入与预处理

- **2D 关键点检测**：使用 ViTPose 对每帧图像提取 2D 人体关键点，同时获得每个关键点的置信度分数。
- **遮挡不确定性建模**：对于置信度高于预设阈值的可见关键点，直接采用其坐标作为可靠输入；对于置信度低于阈值的遮挡关键点，构建高斯分布以表征其位置不确定性，并从分布中采样作为后续模块的输入。

### 频域分解与去噪先验

- **DWT 小波分解**：将拼接后的 2D 关键点序列沿空间和时间维度进行离散小波变换，得到四个子带——LL（低频-低频）、LH（低频-高频）、HL（高频-低频）、HH（高频-高频），分别捕获运动的不同频率成分。
- **频域扩散模型**：采用一个 Transformer 网络作为编码器-2D 解码器结构，学习每个子带的系数映射 $m_{h,v}$ 和滤波后的子带 $\hat{y}_{h,v}$。前向扩散过程仅对不可靠关键点施加噪声，将其逐步扩散至初始高斯分布；反向过程则从该分布出发，通过系数选择逐步去噪，恢复干净的 2D 关键点。
- **iDWT 重建**：利用选择后的子带通过逆离散小波变换重建去噪后的 2D 关键点序列，并与真实关键点计算 L1 损失以监督训练。

### 3D 运动重建

- **3D 解码器**：在 2D 频域先验训练完成后，冻结编码器部分，接入 3D 解码器。3D 解码器以编码器输出的隐变量、图像特征 $I$ 为条件，预测 3D 运动的 SMPL 姿态参数 $\theta^{1:N}$、位移参数 $\tau^{1:N}$ 以及形状参数 $\beta$。
- **端到端监督**：通过综合 SMPL 参数损失、3D 关节损失、顶点损失和重投影 2D 关键点损失进行端到端训练，确保重建运动在 3D 空间和 2D 投影上均保持准确。

### 关键设计决策

与传统的时域运动先验（如直接使用时序 Transformer 回归 SMPL 参数）不同，FreqMotion 将去噪过程置于频域。这一设计的核心优势在于：遮挡关节在频域中仍保持周期性和一致性动量模式（见图1），DWT 的多尺度分析能力使得模型能够分别处理低频运动趋势和高频细节噪声，从而在长期遮挡下仍能从可靠的部分观测中恢复出连贯的 3D 运动。

![[assets/figures/papers/paper_list_l15_https_openaccess_thecvf_com_content_CVPR2026_html_Huang_Occluded_Human_B/figures/002_Figure_2.jpg]]
*Figure 2: The pipeline of our method. Given an occluded video, we first detect 2D keypoints and model the noisy keypoints in the occluded regions using Gaussian distributions. We then combine the visible and noisy invisible keypoints, and decompose them into multiple wavelet subbands using DWT. Subsequently, we design a diffusion model with a 2D decoder to select valid frequency components for reconstructing the clean data. Once the prior model is trained, we employ the encoder with a 3D decoder to facilitate 3D motion capture within the same diffusion process. Finally, the reconstructed motion can be regressed from the input keypoints and images after several diffusion time steps*

FreqMotion 将遮挡人体运动捕获重新表述为**小波系数选择过程**，其核心由四个关键模块串联而成，并通过频域扩散模型实现从部分观测到完整运动的映射。

### 运动表示与预备定义

方法以 SMPL 模型参数化人体运动。一段包含 $N$ 帧的运动序列表示为：

$$\mathbf{x}^{1:N} = \left\{ \theta^{1:N}, \tau^{1:N} \right\}$$

其中 $\theta \in \mathbb{R}^{144}$ 为姿态参数，$\tau$ 为全局位移。这一参数化形式是后续所有频域操作的数据基础。

### 模块一：2D 关键点检测与不确定性建模

给定遮挡视频，首先采用 **ViTPose** 检测每帧的 2D 关键点。对于置信度高于预设阈值的关键点，直接采用其坐标作为可靠观测；对于遮挡区域置信度低的关键点，则通过构建**高斯分布**来建模其不确定性。这一步骤将遮挡问题转化为概率化的输入表示，为后续扩散模型提供带有噪声估计的初始分布。

### 模块二：DWT 小波分解

将组合后的 2D 关键点序列沿空间和时间维度进行**离散小波变换 (DWT)**，分解为四个频率子带：LL（低频-低频）、LH（低频-高频）、HL（高频-低频）、HH（高频-高频）。DWT 的数学形式为：

$$y_{h,v}[k_1,k_2] = \sum_m \sum_n P[m,n] \, f_h[m-2k_1] \, f_v[n-2k_2]$$

其中 $P[m,n]$ 为输入的关键点序列，$f_h$、$f_v$ 分别为水平和垂直方向的小波滤波器，$h,v \in \{L,H\}$ 标记子带类型。这一分解使得模型能够在不同频率尺度上分别处理遮挡引入的噪声——低频子带保留运动的主体趋势，高频子带则捕获细节与遮挡噪声的混合信息。

### 模块三：频域扩散模型（编码器 + 2D 解码器）

这是方法的核心创新。传统扩散模型从纯噪声出发逐步去噪，而 FreqMotion 设计了**针对遮挡关键点的前向扩散过程**：仅对不可靠的遮挡关键点，将其真实值 $\hat{p}_0$ 逐步扩散至初始高斯分布 $p$：

$$q(p_t \mid \hat{p}_0) = p + \sqrt{\hat{\alpha}_t} (\hat{p}_0 - p) + \sqrt{1 - \hat{\alpha}_t} \epsilon, \quad \epsilon \sim \mathcal{N}(0, \mathrm{I})$$

反向过程则从该初始分布出发，通过基于 Transformer 的编码器-解码器网络，为每个小波子带学习一个**系数选择图**：

$$\hat{y}_{h,v}, m_{h,v} = \mathscr{F}_{h,v}(y)$$

其中 $\hat{y}_{h,v}$ 为滤波后的子带，$m_{h,v}$ 为系数选择图，$\mathscr{F}_{h,v}$ 为子带特定的 Transformer 网络。网络通过选择有效的小波系数来去除遮挡噪声，而非直接回归关键点坐标。去噪后的子带通过**逆离散小波变换 (iDWT)** 重建干净的 2D 关键点：

$$P[m,n] = \sum_{k_1}\sum_{k_2} \left( \sum_{v\in\{L,H\}} \sum_{h\in\{L,H\}} \bar{y}_{h,v}[k_1,k_2] \, f_h[m-2k_1] \, f_v[n-2k_2] \right)$$

2D 先验的训练损失为重建关键点的 L1 损失：

$$\mathcal{L}_{keyp} = |P - \hat{P}|$$

### 模块四：3D 解码器与 SMPL 参数预测

2D 频域先验训练完成后，**冻结编码器**，接入 3D 解码器。3D 解码器以编码器输出的隐变量 $y$、扩散时间步隐变量 $z$ 和图像特征 $I$ 为条件，预测 3D 运动的子带系数和 SMPL 形状参数：

$$Y_{h,v}, \beta = \mathcal{D}(y, z, I)$$

随后同样通过 iDWT 重建 3D 姿态参数，并计算综合损失函数：

$$\mathcal{L} = \mathcal{L}_{smpl} + \mathcal{L}_{joint} + \mathcal{L}_{verts} + \mathcal{L}_{keyp}$$

其中各项分别对应 SMPL 参数、3D 关节位置、网格顶点和重投影 2D 关键点的监督损失。这一两阶段训练策略——先学习 2D 频域去噪先验，再复用扩散过程进行 3D 重建——使得模型能够充分利用频域的周期性模式，在长期遮挡下仍能恢复时间连贯的 3D 运动。

## 实验与关键发现

### 实验设置与数据集

为系统评估频域去噪先验在遮挡人体运动捕获中的有效性，本文在多个具有不同遮挡特性的数据集上进行了实验。其中，**OcMotion** 是本文新构建的遮挡运动数据集，包含 43 个序列、6 个视角、约 30 万帧图像，涵盖多种真实物体遮挡场景，并配有精确的 3D 运动标注（Table 1）。其 2D 重投影误差仅为 7.3 像素，标注质量可靠。此外，还在 **3DPW**（室外自然场景）、**3DPW-OC**（3DPW 的合成遮挡版本）以及 **Hi4D**（人际遮挡场景）上进行了评估。评测指标包括 MPJPE（平均关节位置误差）、PA-MPJPE（Procrustes 对齐后的 MPJPE）、PVE（顶点误差）和 Accel（加速度误差，衡量运动平滑度）。

![[assets/figures/papers/paper_list_l15_https_openaccess_thecvf_com_content_CVPR2026_html_Huang_Occluded_Human_B/figures/004_Table_1.jpg]]
*Table 1: Comparison with commonly used 3D human datasets. OcMotion is the first motion dataset that contains diverse real object occlusions with complete and accurate annotations*

### 主实验结果

**OcMotion 上的性能。** 如表 2 所示，FreqMotion 在 OcMotion 数据集上显著优于现有视频时序方法。在不使用 OcMotion 训练的情况下，FreqMotion 达到 MPJPE 79.2 mm、PA-MPJPE 51.7 mm、Accel 20.1 mm/s²，在加速度误差上取得最佳结果，表明频域先验能有效捕捉周期性运动模式，生成时间上更连贯的重建运动。相比之下，基于时域回归的方法（如 **VIBE** (Kocabas et al., CVPR 2020)、**MPS-Net** (Luo et al., ACCV 2020)）在长期遮挡下运动趋于过平滑，而遮挡感知方法（如 **PARE** (Kocabas et al., ICCV 2021)、**DPMesh** (Zhu et al., CVPR 2024)）虽然显式考虑遮挡，但缺乏对时序频率结构的建模，加速度误差偏高。

**3DPW 与 3DPW-OC 上的性能。** 在非遮挡的 3DPW 数据集上，FreqMotion 取得 MPJPE 67.3 mm、PA-MPJPE 44.8 mm、PVE 75.3 mm，与现有最优方法性能相近（Table 2）。这符合预期——该方法的优势在于长期遮挡场景，而非一般无遮挡条件。在合成遮挡的 3DPW-OC 上，FreqMotion 达到 MPJPE 63.1 mm、PA-MPJPE 45.2 mm、Accel 9.1 mm/s²，进一步验证了频域去噪先验对遮挡噪声的鲁棒性。

**Hi4D 人际遮挡场景。** 在更具挑战性的人际遮挡数据集 Hi4D 上，FreqMotion 同样取得领先性能，MPJPE 为 61.5 mm，Accel 为 15.6 mm/s²（Table 3）。这表明频域先验不仅能处理物体遮挡，还能有效应对人体间的复杂交互遮挡。

**定性分析。** 图 4 的可视化对比显示，FreqMotion 在遮挡区域的重建结果明显优于同时使用时序信息的方法和显式遮挡感知方法。频域先验能够利用可靠可见关键点推断遮挡关节的合理位置，避免了其他方法中常见的穿透、漂浮或姿态不连贯现象。

### 消融实验

为验证各关键组件的贡献，本文在 OcMotion 数据集上进行了系统消融实验（Table 4）。

![[assets/figures/papers/paper_list_l15_https_openaccess_thecvf_com_content_CVPR2026_html_Huang_Occluded_Human_B/figures/008_Table_4.jpg]]
*Table 4: Ablation studies on different key components. All models are trained and evaluated on the proposed OcMotion dataset. ”Frame Regression” and ”Temporal Regression” refer to directly regressing SMPL parameters from image features using MLP and a temporal transformer, respectively. ”+” denotes the addition of a specific module to the Temporal Regression model*

**频域去噪先验 vs. 时域回归。** 以 Temporal Regression（基于时序 Transformer 直接回归 SMPL 参数）为基线，加入去噪关键点与 DWT 分解后，3DPW 上 MPJPE 降至 49.6 mm，性能提升显著。这证明频域表示能比时域先验更有效地捕捉遮挡运动的周期性和一致性模式。

**DWT vs. DCT。** 将 DWT 替换为 DCT（丢弃高频分量）后，MPJPE 升至 51.6 mm，表明 DCT 的全局频率变换无法像 DWT 那样保留局部时频信息，导致高频细节丢失和重建精度下降。DWT 的多尺度分析能力对同时处理低频和高频噪声至关重要。

**3D 扩散过程的贡献。** 在频域先验基础上进一步引入 3D 扩散过程（Prior + 3D Diffusion）后，MPJPE 达到最优的 48.5 mm。这表明将扩散模型的去噪能力从 2D 关键点扩展到 3D 运动子带，能进一步利用图像特征作为条件，提升 3D 重建的准确性。

综合消融结果，频域去噪先验和 3D 扩散过程是性能提升的两个核心支柱：前者通过小波系数选择过滤遮挡噪声，后者将去噪能力迁移至 3D 空间并融合视觉观测。

### 失败模式与局限性分析

尽管 FreqMotion 在遮挡场景下表现优异，仍存在以下失效情形：

1. **2D 关键点检测器误导。** 当 ViTPose 对严重遮挡的关键点错误地赋予高置信度时，高斯不确定性建模无法有效纠正，导致错误的 2D 观测直接污染频域先验的输入，使重建的 3D 姿态偏离真实值。
2. **极端姿态泛化不足。** OcMotion 数据集中缺少极具挑战性的姿态（如大幅度扭转、倒地等），模型在这些场景下性能下降明显。频域先验依赖训练数据中的运动模式分布，对分布外姿态的泛化能力有限。
3. **大面积遮挡失效。** 当遮挡面积过大或关键点检测几乎全盘失效时，可靠可见关键点数量不足，频域先验缺乏足够的观测信息来推断遮挡部分，重建可能完全失败。

### 关键图表结论

- **Table 2**：FreqMotion 在 OcMotion 上全面优于现有视频方法，尤其在加速度误差上优势明显，验证了频域先验对运动连贯性的提升。
- **Table 3**：在 Hi4D 人际遮挡场景下同样取得最优，证明方法的泛化性。
- **Table 4**：消融实验确认 DWT 频域分解和 3D 扩散过程是性能的核心驱动因素，DCT 替代 DWT 会导致性能显著下降。
- **Figure 4**：定性结果表明频域先验在遮挡区域能生成更合理、更连贯的姿态，优于时域回归和遮挡感知基线。

![[assets/figures/papers/paper_list_l15_https_openaccess_thecvf_com_content_CVPR2026_html_Huang_Occluded_Human_B/figures/006_Table_2.jpg]]
*Table 2: Quantitative comparison with state-of-the-art methods. Our method produces good results and achieves the best performance in some metrics on occluded datasets. ∗ means the image-based method. † denotes the method that explicitly considers the occlusion problem*

![[assets/figures/papers/paper_list_l15_https_openaccess_thecvf_com_content_CVPR2026_html_Huang_Occluded_Human_B/figures/007_Table_3.jpg]]
*Table 3: Comparisons on Hi4D. Our method can achieve stateof-the-art performance on inter-person occluded cases*

![[assets/figures/papers/paper_list_l15_https_openaccess_thecvf_com_content_CVPR2026_html_Huang_Occluded_Human_B/figures/005_Figure_4.jpg]]
*Figure 4: Qualitative comparison among the methods that utilize temporal information (b, c, f) and explicitly consider the occlusion problem (d, e). Our method is more robust to occlusions than other methods*

## 定位与知识库关联

### 1. 方法谱系：从时域先验到频域去噪先验

FreqMotion 的核心推进在于将遮挡人体运动捕获的**先验类型**从时域建模迁移至频域去噪。传统视频时序方法依赖时域运动先验来填补遮挡造成的观测缺失，但其瓶颈在于：长期遮挡下，时域回归所能提供的运动信息急剧衰减，导致重建结果趋于过平滑或不可靠的均值姿态。FreqMotion 通过频域视角重新审视这一问题——遮挡关节的运动在频域中呈现出周期性与一致性动量模式（见 **Figure 1**），这为从局部可靠观测推断全局运动提供了更强的结构约束。

与现有工作的关键差异体现在以下维度：

| 方法维度 | 时域基线方法 | FreqMotion (本文) |
|---------|-------------|-------------------|
| **运动先验类型** | 时域运动先验（如 VIBE 的时序回归、GLAMR 的全局运动填充） | 频域去噪先验，基于 DWT 子带系数选择的扩散模型 |
| **遮挡关键点处理** | 直接丢弃或使用低置信度关键点 | 对遮挡关键点构建高斯分布建模不确定性，扩散模型去噪 |
| **频率表示** | 不使用频率表示，或采用 DCT 丢弃高频 | DWT 多尺度分析，学习每个子带的系数映射以选择有效频率分量 |
| **训练策略** | 单阶段回归 3D 姿态参数 | 两阶段：先训练 2D 频域扩散先验，冻结编码器后训练 3D 解码器 |

具体而言，**VIBE** (Kocabas et al., CVPR 2020) 采用时序编码器回归 SMPL 参数，其运动先验本质上是对相邻帧姿态的平滑约束，缺乏对周期性模式的显式建模。**GLAMR** (Yuan et al., CVPR 2022) 通过全局运动填充处理遮挡，但仍依赖时域插值逻辑。**MPS-Net** (Luo et al., ACCV 2020) 使用多尺度时序特征，但未针对遮挡场景设计专门的频率处理机制。在遮挡感知方法中，**PARE** (Kocabas et al., ICCV 2021) 从单帧图像中学习遮挡鲁棒特征，但缺少时序运动先验；**DPMesh** (Zhu et al., CVPR 2024) 引入扩散先验恢复遮挡人体网格，但其扩散过程在时域执行，未利用频域的结构化周期信息。

FreqMotion 的关键洞察在于：**将遮挡运动捕获形式化为小波系数选择过程**。通过 DWT 将 2D 关键点序列沿时空维度分解为 LL、LH、HL、HH 四个子带后，频域扩散模型学习每个子带的系数映射 $m_{h,v}$，选择有效频率分量以重建干净数据。这一设计使得模型对低频噪声（如遮挡导致的坐标漂移）和高频噪声（如检测抖动）均具有鲁棒性——消融实验证实，使用 DCT 替代 DWT 会导致 3DPW 上 MPJPE 从 48.5 上升至 51.6（**Table 4**），验证了多尺度小波分解对捕获跨频率依赖关系的必要性。

### 2. 适用边界与局限

**适用场景**：FreqMotion 在**长期遮挡**场景下展现出显著优势。在 OcMotion 数据集上，其 MPJPE 达到 79.2 mm，PA-MPJPE 为 51.7 mm，加速度误差仅 20.1 mm/s²，显著优于现有视频方法（**Table 2**）。在人际遮挡场景（Hi4D 数据集）中，MPJPE 为 61.5 mm，加速度误差 15.6 mm/s²，验证了频域先验对复杂交互遮挡的泛化能力（**Table 3**）。

**性能边界**：
- **非遮挡场景持平**：在无遮挡的 3DPW 数据集上，FreqMotion 的 MPJPE 为 67.3 mm，PA-MPJPE 为 44.8 mm，与现有方法性能相近。频域先验的主要增益体现在遮挡场景，而非通用姿态估计。
- **极端姿态退化**：训练数据（OcMotion）中缺少极具挑战性的姿态，模型在泛化到极端姿态时性能下降。
- **2D 检测器依赖**：方法依赖 ViTPose 提供可靠的 2D 关键点。当遮挡面积过大或关键点检测全盘失效时，先验信息不足，重建可能失败。更关键的是，ViTPose 在严重遮挡时可能对错误预测赋予高置信度，误导模型回归出错误的 3D 运动。

### 3. 开放问题

1. **低层视觉特征融合**：当前方法仅使用 2D 关键点作为输入，未充分利用边缘、纹理等低层视觉线索。如何将这些视觉特征有效融入频域去噪框架，以提升严重遮挡下的关键点检测精度，是一个值得探索的方向。

2. **行为先验增强**：频域先验捕捉了运动的周期性模式，但缺乏对高层行为语义的理解。引入增强的行为先验（如动作类别条件）有望过滤噪声并提高对困难姿态的泛化能力。

3. **DWT 分解尺度的最优配置**：消融实验已证实 DWT 优于 DCT，但 DWT 分解级数与运动重建精度之间的定量关系尚未系统研究。是否存在最优的频域分解配置，以及该配置是否应随遮挡程度自适应调整，仍需进一步实验验证。

4. **多人交互与动态相机扩展**：当前方法针对单人在静态相机下的遮挡场景设计。频域先验能否扩展到多人交互场景（如 Hi4D 所示的人际遮挡已有初步验证）或动态相机下的实时运动捕获，是后续研究的重要方向。

5. **更长遮挡序列的性能极限**：在更长的遮挡序列和复杂背景下，频域先验的周期性假设是否仍然成立？模型是否需要引入长程时序建模机制来弥补频域局部窗口的局限？这些问题需要在更大规模的遮挡数据集上进行压力测试。

## 原文 PDF

![[paperPDFs/CVPR_2026/Occluded_Human_Body_Capture_with_Frequency_Domain_Denoising_Prior.pdf]]
