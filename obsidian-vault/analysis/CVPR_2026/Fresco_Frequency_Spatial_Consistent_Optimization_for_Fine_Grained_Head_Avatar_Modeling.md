---
title: "Fresco: Frequency-Spatial Consistent Optimization for Fine-Grained Head Avatar Modeling"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/Fresco_Frequency_Spatial_Consistent_Optimization_for_Fine_Grained_Head_Avatar_Modeling.pdf
project_link: null
code_link: "https://github.com/saralkun/Fresco"
aliases:
- Fresco
tags:
- CVPR_2026
- topic/other_unclear
- topic/other_unclear/general
core_operator: 联合频率课程调度（拉普拉斯金字塔驱动的低频优先、渐进高频激活）与UV空间跨视图纹素对齐，以解耦并稳定优化过程。
primary_logic: 在图像域采用局部拉普拉斯分解逐步引导学习从低频到高频，同时在共享UV空间强化多视图纹素一致性，从而压制伪影、提升视图连贯性。
claims:
- 定量对比：在NeRSemble数据集上，Fresco在所有指标上均优于现有最优方法（表1）。
- 消融：移除高频分支导致所有任务指标下降（表2）。
- 消融：移除UV一致性使跨视图合成质量下降（表2、图5）。
- NeRSemble 上 PSNR / LPIPS = 33.48 / 0.039 (Novel-View); 32.07 / 0.045 (Self-Reenactment)
---

# Fresco: Frequency-Spatial Consistent Optimization for Fine-Grained Head Avatar Modeling

> [!tip] 核心洞察
> 在图像域采用局部拉普拉斯分解逐步引导学习从低频到高频，同时在共享UV空间强化多视图纹素一致性，从而压制伪影、提升视图连贯性。

| 字段 | 内容 |
|------|------|
| 中文题名 | Fresco：面向细粒度头部化身建模的频空一致优化 |
| 英文题名 | Fresco: Frequency-Spatial Consistent Optimization for Fine-Grained Head Avatar Modeling |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://openaccess.thecvf.com/content/CVPR2026/html/Zhang_Fresco_Frequency-Spatial_Consistent_Optimization_for_Fine-Grained_Head_Avatar_Modeling_CVPR_2026_paper.html) · [Code](https://github.com/saralkun/Fresco) |
| Topic | #topic/other_unclear #topic/other_unclear/general |
| Method | Fresco |
| Dataset | NeRSemble |

> [!tip] 效果简介
> - NeRSemble 上，PSNR / LPIPS 33.48 / 0.039 (Novel-View); 32.07 / 0.045 (Self-Reenactment) vs GaussianAvatars, MeGA, HERA等先前最优 (在所有指标上全面领先，PSNR明显高于次优方法)。

## 概述

头部化身重建的核心瓶颈在于：逐视图光度监督缺乏跨视图的几何对应，导致训练早期出现伪高频锐化伪影和视图间漂移，细节一致性差。**Fresco** 提出一种频空一致优化范式，在不改变底层表示（FLAME网格 + 高斯毛发场）的前提下，通过**联合频率课程调度与UV空间跨视图纹素对齐**来解耦并稳定优化过程。

具体而言，Fresco 在图像域采用局部拉普拉斯分解，以低频优先、渐进激活高频的策略指导学习；同时在共享UV空间强化多视图纹素一致性，压制伪影、提升视图连贯性。在 NeRSemble 数据集上，Fresco 在新视角合成与自重现任务上全面优于 **PointAvatar** (Zheng et al., CVPR 2023)、**GaussianAvatar** (Qian et al., CVPR 2024)、**MeGA** (Wang et al., CVPR 2025)、**HERA** (Cai et al., arXiv 2024) 等先前最优方法，PSNR 与 LPIPS 均取得最佳结果（表1）。消融实验证实，移除高频分支或UV一致性均导致指标显著下降（表2），验证了频空联合优化的关键作用。

## 背景与动机

### 任务背景

高保真头部化身重建是计算机视觉与图形学中的核心挑战，其目标是从多视图图像中恢复可驱动的三维头部表示，以支持新视角合成与自重现（self-reenactment）等下游任务。近年来，以可变形网格和三维高斯泼溅（3D Gaussian Splatting）为代表的显式表示取得了显著进展，代表性工作包括 **PointAvatar**（Zheng et al., CVPR 2023）、**GaussianAvatar**（Qian et al., CVPR 2024）、**MeGA**（Wang et al., CVPR 2025）以及 **HERA**（Cai et al., arXiv 2024）。这些方法通常采用混合表示策略——以参数化人脸网格（如 FLAME）建模面部区域，辅以高斯基元或点云覆盖头发与外围区域——并依赖逐视图的光度损失进行端到端优化。

### 瓶颈分析：伪高频锐化与视图间漂移

尽管上述方法在特定场景下取得了可观的重建质量，但其优化过程存在一个深层结构性问题：**逐视图光度监督缺乏跨视图的几何对应约束**。在训练早期，网络尚处于欠拟合状态，各视图独立的像素级损失会驱动模型产生虚假的高频响应，表现为锐化伪影和纹理错位。由于没有机制强制不同视点下的同一表面区域共享一致的纹理特征，这些伪影在视图切换时呈现明显的外观漂移，严重损害化身的多视角一致性。

这一瓶颈的根源在于，传统训练范式对频率成分不加区分地进行统一监督：低频全局结构和高频局部细节被耦合在同一个损失函数中，模型在结构尚未收敛时就过早地拟合高频噪声，形成“先入为主”的错误纹理模式。

### 现有方法的缺口

现有头部化身方法在频率处理和跨视图一致性方面存在两个关键缺口：

1. **缺乏频率感知的优化调度**：无论是基于网格、高斯还是混合表示的方法，其训练损失均以全频图像作为监督信号，未对频率成分进行分离或分阶段激活。这导致早期优化阶段缺乏对全局结构的优先保护，模型易被高频噪声干扰。
2. **缺乏共享纹理空间的跨视图对齐**：现有方法的监督仅停留在图像域（逐像素损失），未利用头部化身本身具备的 UV 参数化特性来建立不同视点间的纹素对应关系。这使得同一表面区域在不同视图下可能学习到相互矛盾的外观，难以保证跨视图一致性。

### 本文动机

针对上述瓶颈，Fresco 提出**频空一致优化**（Frequency-Spatial Consistent Optimization）框架，核心动机可归纳为两点：

- **频率解耦与课程调度**：通过在图像域引入拉普拉斯金字塔分解，将学习过程从低频到高频渐进展开。早期阶段以低通滤波约束模型专注于全局结构重建，待结构稳定后再逐步激活高频分支以恢复精细纹理，从而压制训练早期的伪高频伪影。
- **UV 空间跨视图对齐**：利用可微分 UV 烘焙算子将多视图渲染投影至共享 UV 纹理空间，并通过可见性加权的跨视图纹素一致性损失，强制不同视点下同一表面区域的纹理保持一致。这从根本上解决了视图间漂移问题，提升了化身的整体连贯性。

通过上述频域课程调度与空间 UV 对齐的联合设计，Fresco 在不显著增加训练开销的前提下，实现了结构保真度与视图一致性的双重提升。

## 核心创新

Fresco 的核心创新在于**将训练动态而非底层表示作为优化对象**，通过联合调度两个互补的机制——频率课程学习与 UV 空间跨视图一致性——来解决头部化身重建中的根本瓶颈。

### 瓶颈与因果机制

头部化身重建通常采用逐视图的光度损失进行监督。这种逐像素的监督方式缺乏跨视图的几何对应关系，导致训练早期模型倾向于“记忆”各视图的高频细节而非学习一致的几何结构，从而产生**伪高频锐化伪影**和**视图间外观漂移**。Fresco 识别出这一瓶颈后，设计了两个因果调节旋钮来解耦并稳定优化过程：

1. **频率课程调度**：在图像域直接施加从低频到高频的渐进式学习约束，使模型先建立稳定的全局结构，再逐步恢复精细细节。
2. **UV 空间跨视图对齐**：在共享的 UV 纹理空间强制多视图纹素一致性，为不同视角的渲染提供显式的几何对应监督，从而压制视图依赖的伪影。

### Changed Slots 详解

相对于仅使用统一监督的基线方法，Fresco 引入了两个关键的 Changed Slots：

#### Slot 1：从无调度到渐进拉普拉斯金字塔频率课程

基线方法对所有频率分量一视同仁地进行监督，缺乏对学习顺序的调控。Fresco 采用基于拉普拉斯金字塔的频率分解，将渲染图像与真值图像分别通过不同带宽的高斯滤波器进行解耦，构建从粗到精的频谱层级。

- **低频正则化**（早期）：通过高斯低通滤波 $\mathcal{G}_\sigma$ 提取低频分量，约束模型仅学习平滑后的全局结构（式 2-3）。这有效避免了训练初期因高频噪声导致的几何不稳定。
- **高频增强**（后期）：利用高斯差分（DoG）带通滤波器 $H(\cdot) = \mathcal{G}_{\sigma_1}(\cdot) - \mathcal{G}_{\sigma_2}(\cdot), \ \sigma_1 < \sigma_2$ 提取精细结构，结合边缘感知损失和梯度差异损失（GDL）恢复细节，同时防止过锐化（式 4-7）。
- **渐进带宽扩展**：各频带的权重 $w_i(t)$ 按余弦退火调度逐步激活（式 9），总频率损失 $L_{\mathrm{freq}}(t) = \sum_{i=1}^{N} w_i(t) \| \hat{I}_i - I_i \|_1$ 随训练迭代自适应扩展带宽（式 8）。

#### Slot 2：从无到共享 UV 空间的跨视图纹素对齐

基线方法仅在图像域计算逐像素损失，不同视图的渲染之间缺乏显式的一致性约束。Fresco 引入可微分 UV 烘焙算子，将多视图渲染投影到共享的 UV 纹理空间，并施加跨视图纹素对齐损失：

$$\mathcal{L}_{UV} = \frac{1}{|\Omega_{vis}|} \sum_{(u,v) \in \Omega_{vis}} w(u,v) \| \hat{T}^a(u,v) - \mathrm{sg}[\hat{T}^b(u,v)] \|_1$$

该损失仅对相互可见且正面朝向的纹素进行计算，通过可见性加权机制避免对遮挡区域的错误惩罚（式 10）。此外，缝正则化 $L_{seam}$ 进一步约束 UV 图表边界处的颜色连续性与局部平滑性，消除耳朵、发际线等区域的裂纹和颜色不连续（式 12）。

### 三阶段优化调度

Fresco 将上述两个创新组件整合为三阶段优化调度（式 15）：

$$L_{total}^{(t)} = \begin{cases} \alpha L_{freq}^{low}(t), & t < T_1 \\ \alpha L_{freq}^{low}(t) + \beta L_{UV}(t), & T_1 \le t < T_2 \\ \alpha L_{freq}^{high}(t) + \beta L_{UV}(t) + L_{seam}, & t \ge T_2 \end{cases}$$

- **第一阶段**（$t < T_1$）：仅使用低频损失，建立稳定的全局几何结构。
- **第二阶段**（$T_1 \le t < T_2$）：引入 UV 一致性损失，在低频约束的基础上建立跨视图纹理对应。
- **第三阶段**（$t \ge T_2$）：加入高频增强损失和缝正则化，恢复精细细节并消除边界伪影。

这种分阶段调度策略确保了每个组件的引入时机与模型的学习状态相匹配，避免了多目标优化中的冲突和震荡。消融实验证实，移除高频分支会导致所有任务指标下降，移除 UV 一致性会使跨视图合成质量显著退化，而移除缝正则化则在耳朵、发际等区域产生明显的裂纹和颜色不连续。

## 整体框架

Fresco 的优化对象是一个**混合显式头部化身**：人脸区域由参数化网格（FLAME）驱动，头发及外围区域由各向异性 3D 高斯集合表示。两套表示共享同一组形状、表情与姿态参数，通过深度排序的 alpha 混合（Eq. 1）渲染为多视图 RGB 图像。与传统方法直接对渲染图像施加逐像素光度损失不同，Fresco 在训练动态层面引入两个相互配合的调控机制——**频率课程调度**与**UV 空间跨视图一致性**——以压制早期伪高频锐化伪影和视图间漂移。

整体管线如图 1 所示，可分解为四个功能模块：

1. **人脸网格参数化（FLAME）**  
   由形状参数 β、表情参数 ψ 和姿态参数 φ 控制的可变形网格，携带可学习的 UV 位移图和神经纹理，负责面部区域的几何与外观。

2. **高斯毛发场**  
   各向异性 3D 高斯集合，通过网格姿态参数进行动画化，驱动头发与外围区域的渲染。

3. **频率课程分支**  
   在图像域对渲染结果与真值进行拉普拉斯金字塔分解，通过可微分高斯滤波提取低频分量（Eq. 2），在训练早期以低频重建损失 $L_{LF}$（Eq. 3）约束学习，稳定全局结构；随后通过 Difference-of-Gaussian (DoG) 带通滤波（Eq. 4）与边缘感知高频损失 $L_{HF}^{edge}$（Eq. 5）及梯度差异损失 $L_{GDL}$（Eq. 6）逐步激活高频细节，形成从低频到高频的渐进课程（Eq. 8–9）。

4. **UV 空间一致性分支**  
   通过可微分 UV 烘焙算子将多视图渲染投影至共享 UV 纹理空间，利用可见性加权的 L1 损失 $L_{UV}$（Eq. 10）对齐跨视图纹素，并辅以缝正则化 $L_{seam}$（Eq. 12）约束 UV 接缝两侧的颜色连续性与局部平滑性。

训练过程按**三阶段调度**组织总损失 $L_{total}^{(t)}$（Eq. 15）：第一阶段仅启用低频频率损失以建立稳定的全局几何与外观；第二阶段引入 UV 一致性损失，在共享纹理空间强化多视图对齐；第三阶段加入高频增强损失与缝正则化，恢复精细纹理并消除接缝伪影。这一调度使得频率解耦与空间对齐在时间上交错推进，而非简单叠加，从而在保持训练开销可控的前提下显著提升视图连贯性与细节保真度。

### 补充图表

![[assets/figures/papers/paper_list_l1024_https_openaccess_thecvf_com_content_CVPR2026_html_Zhang_Fresco_Frequency/figures/001_Figure_1.jpg]]
*Figure 1: Overview of the proposed Fresco. Multi-view images drive a CNN to estimate 3DMM and an MLP to refine Gaussian hair parameters*

## 核心模块与公式推导

Fresco 的核心在于**不改变底层表示**，而是通过联合调度两个互补的优化信号——频率课程与 UV 空间监督——重塑训练动力学，从而压制早期伪高频锐化伪影和视图间漂移。

### 3.1 频率课程：拉普拉斯金字塔分解

频率课程的目标是将学习过程从低频到高频逐步引导，避免早期优化陷入局部高频噪声。Fresco 在图像域直接操作，利用可微高斯滤波器构建拉普拉斯金字塔。

**低频正则化** 首先对渲染图 $\hat{I}$ 和真值图 $I$ 施加高斯滤波，提取平滑的低频分量：

$$\hat{I}_{LF} = \mathcal{G}_\sigma(\hat{I}), \quad I_{LF} = \mathcal{G}_\sigma(I) \tag{2}$$

低频重建损失采用 MAE：

$$L_{LF} = \| \hat{I}_{LF} - I_{LF} \|_1 \tag{3}$$

在训练早期，该损失约束模型优先学习全局结构，稳定收敛。

**高频增强** 在低频稳定后激活，通过差分高斯（DoG）带通滤波器 $H(\cdot) = \mathcal{G}_{\sigma_1}(\cdot) - \mathcal{G}_{\sigma_2}(\cdot)$（$\sigma_1 < \sigma_2$）提取精细纹理。高频损失由边缘感知项和梯度差异项组成：

$$L_{HF}^{edge} = M_{edge} \cdot \| H(\hat{I}) - H(I) \|_1 \tag{5}$$

其中 $M_{edge}$ 为归一化边缘掩码，使损失聚焦于边缘区域。同时引入梯度差异损失防止过锐化：

$$L_{GDL} = \sum_{i,j} \| |\nabla \hat{I}_{i,j}| - |\nabla I_{i,j}| \|_1 \tag{6}$$

高频总损失为两者的加权和：

$$L_{HF} = \lambda_{h1} L_{HF}^{edge} + \lambda_{h2} L_{GDL} \tag{7}$$

**渐进频率课程** 将各频带损失加权求和，权重随训练迭代 $t$ 自适应扩展带宽：

$$L_{freq}(t) = \sum_{i=1}^{N} w_i(t) \| \hat{I}_i - I_i \|_1 \tag{8}$$

频率权重采用余弦退火调度，渐进激活各频带：

$$w_i(t) = \frac{1}{2} [1 - \cos(\pi \cdot \frac{t - T_i}{T - T_i})], \quad t > T_i \tag{9}$$

### 3.2 UV 空间跨视图一致性

多视图训练中，逐图像像素损失缺乏跨视图几何对应，导致视图间外观漂移。Fresco 通过可微分 UV 烘焙算子将多视图渲染投影至共享 UV 纹理空间，并施加跨视图纹素对齐损失：

$$\mathcal{L}_{UV} = \frac{1}{|\Omega_{vis}|} \sum_{(u,v) \in \Omega_{vis}} w(u,v) \| \hat{T}^a(u,v) - \mathrm{sg}[\hat{T}^b(u,v)] \|_1 \tag{10}$$

其中 $\hat{T}^a$ 和 $\hat{T}^b$ 为两视图的烘焙纹理，$\mathrm{sg}[\cdot]$ 为停止梯度操作，$\Omega_{vis}$ 为相互可见且正面朝向的纹素集合，$w(u,v)$ 为可见性权重。该损失强制不同视角下同一 UV 坐标的纹素一致，从而提升跨视图连贯性。

**缝正则化** 进一步约束 UV 图表边界处的颜色连续性和局部平滑性：

$$L_{seam} = \lambda_{pair} L_{seam}^{pair} + \lambda_{tv} L_{seam}^{tv} \tag{12}$$

其中 $L_{seam}^{pair}$ 约束接缝两侧的颜色一致性，$L_{seam}^{tv}$ 为接缝处的全变分平滑项。

### 3.3 三阶段优化调度

Fresco 将上述模块组织为三阶段训练调度，逐步引入监督信号：

$$L_{total}^{(t)} = \begin{cases} \alpha L_{freq}^{low}(t), & t < T_1 \\ \alpha L_{freq}^{low}(t) + \beta L_{UV}(t), & T_1 \le t < T_2 \\ \alpha L_{freq}^{high}(t) + \beta L_{UV}(t) + L_{seam}, & t \ge T_2 \end{cases} \tag{15}$$

- **阶段一**（$t < T_1$）：仅低频正则化，稳定全局几何结构。
- **阶段二**（$T_1 \le t < T_2$）：引入 UV 一致性，建立跨视图纹素对应。
- **阶段三**（$t \ge T_2$）：激活高频增强与缝正则化，恢复精细细节并消除接缝伪影。

### 3.4 底层渲染基础

作为前置，像素颜色由深度排序的高斯基元经 alpha 混合得到：

$$C(\mathbf{x}) = \sum_i c_i \alpha'_i \prod_{j < i} (1 - \alpha'_j) \tag{1}$$

其中 $c_i$ 为基元颜色，$\alpha'_i$ 为考虑不透明度的有效权重。人脸区域由 FLAME 参数化网格建模（形状 $\beta$、表情 $\psi$、姿态 $\varphi$），头发与外围区域由各向异性 3D 高斯集合表示，两者共享姿态驱动以实现动画化。Fresco 的频率课程和 UV 监督独立于具体表示，作用于渲染输出层面。

## 实验与分析

### 核心瓶颈与设计动机

头部化身重建任务中，现有方法普遍采用逐视图光度损失进行监督。这种逐像素、逐视图独立优化的范式缺乏跨视图的几何对应约束，导致训练早期出现两类典型失效：**伪高频锐化伪影**与**视图间外观漂移**。前者表现为纹理细节在错误位置被强化，后者则导致同一语义区域在不同视角下呈现不一致的颜色和几何。Fresco的出发点正是针对这一瓶颈，在不改变底层表示的前提下，通过**联合频率课程调度**与**UV空间跨视图对齐**来重塑优化动力学，从而压制伪影、提升视图连贯性。

### 实验设置

所有实验均在**NeRSemble**数据集上进行，该数据集提供多视图同步视频与对应的FLAME网格参数。Fresco采用与基线方法相同的底层表示——人脸区域使用FLAME参数化网格（带可学习UV位移图与神经纹理），头发及外围区域使用各向异性3D高斯集合——仅优化策略不同，保证了对比的公平性。评估涵盖两个核心任务：**新视角合成**（Novel-View Synthesis）与**自重现**（Self-Reenactment），指标采用PSNR、SSIM和LPIPS。

### 主结果分析

Table 1给出了Fresco与现有最优方法的全面定量对比。在新视角合成任务上，Fresco取得**PSNR 33.48 / LPIPS 0.039**，在自重现任务上取得**PSNR 32.07 / LPIPS 0.045**，在所有指标上均优于**PointAvatar**（Zheng et al., CVPR 2023）、**GaussianAvatar**（Qian et al., CVPR 2024）、**MeGA**（Wang et al., CVPR 2025）和**HERA**（Cai et al., arXiv 2024）等先前方法。PSNR的显著提升表明Fresco在像素级重建精度上的优势，而LPIPS的全面降低则反映了感知质量的改善。

定性结果进一步印证了定量发现。Figure 2的自重现对比显示，Fresco在张嘴、眨眼等表情下能更忠实地再现面部动态，牙齿细节更加清晰；Figure 3的新视角合成对比中，Fresco在不同视角下呈现出更锐利的面部皱纹和更一致的牙齿纹理，跨视图连贯性明显优于基线方法。这些改进直接受益于频率课程对伪高频的压制以及UV一致性对视图间漂移的约束。

### 消融研究

Table 2系统拆解了各模块的贡献，Figure 4-6提供了对应的定性证据。

![[assets/figures/papers/paper_list_l1024_https_openaccess_thecvf_com_content_CVPR2026_html_Zhang_Fresco_Frequency/figures/007_Figure_4.jpg]]
*Figure 4: Qualitative comparison of high-frequency modules. Without high-frequency enhancement, the rendered result exhibits missing local details, with blurred facial wrinkles and hair textures. The complete model restores fine textures, achieving a more realistic reconstruction effect*

**高频增强分支**：移除高频分支（w/o L_HF）后，所有任务指标全面下降。Figure 4显示，无高频增强时渲染结果细节模糊，面部皱纹和头发纹理丢失，完整模型则能恢复精细纹理。这表明仅靠低频监督无法充分捕捉细粒度结构，DoG带通滤波与边缘感知损失（Eq. 5-7）对高频细节重建至关重要。

**UV一致性约束**：移除UV一致性（w/o L_UV）导致新视角合成指标显著退化。Figure 5的跨视图对比中，无UV监督时耳朵和发际线区域出现明显的视角依赖伪影，而有UV监督时外观在不同视角下保持连贯。这验证了可微分UV烘焙与多视图纹素对齐损失（Eq. 10）在消除视图间漂移方面的关键作用。

**缝正则化**：移除缝正则化（w/o L_seam）后，Figure 6显示UV接缝附近（如耳朵、发际线边界）出现可见裂纹和颜色不连续。缝正则化通过约束跨图表颜色连续性（L_seam^pair）与局部平滑性（L_seam^tv），有效消除了这些边界伪影。

### 失败模式与局限性

当前验证存在以下局限，需要读者注意：

1. **数据多样性不足**：所有实验仅在NeRSemble数据集上进行，该数据集的面部表情和光照条件相对受控。Fresco在极端表情（如大幅度张嘴、鼓腮）或户外高动态光照场景下的表现尚未验证，频率课程的超参数可能需要重新调节。

2. **超参数敏感性**：频率课程的关键超参数（高斯滤波σ、各频带激活时间T_i、权重λ）需针对不同分辨率和场景手动设定，缺乏自适应性。论文未提供超参数选择的系统性指导。

3. **实时性与部署**：论文未讨论渲染帧率、显存占用及移动端部署可行性。UV烘焙与多视图损失的计算开销在实际应用中可能成为瓶颈。

### 开放问题

基于上述分析，以下方向值得进一步探索：

- 该频空联合优化范式是否可迁移到纯NeRF或3D高斯泼溅等其他底层表示，以验证其通用性？
- 若在更大规模、高动态光照的户外数据上训练，UV空间的可见性权重和缝正则是否仍能保持鲁棒？
- 能否结合深度或法向几何约束，进一步提升跨视图几何一致性？

### 补充图表

![[assets/figures/papers/paper_list_l1024_https_openaccess_thecvf_com_content_CVPR2026_html_Zhang_Fresco_Frequency/figures/004_Table_1.jpg]]
*Table 1: Quantitative comparison with previous methods on novelview synthesis and self-reenactment task. Best results are bold, and second-best are underlined*

![[assets/figures/papers/paper_list_l1024_https_openaccess_thecvf_com_content_CVPR2026_html_Zhang_Fresco_Frequency/figures/008_Table_2.jpg]]
*Table 2: Ablation study on subject #253. We validated the effectiveness of each module through two tasks: Novel-View and Self-Reenactment*

![[assets/figures/papers/paper_list_l1024_https_openaccess_thecvf_com_content_CVPR2026_html_Zhang_Fresco_Frequency/figures/005_Figure_6.jpg]]
*Figure 6: Qualitative comparison of seam regularization. Left w/o seam shows visible cracks and color discontinuities along ear and hair boundaries. Right w/ seam produces smoother and more consistent boundary transitions*

![[assets/figures/papers/paper_list_l1024_https_openaccess_thecvf_com_content_CVPR2026_html_Zhang_Fresco_Frequency/figures/002_Figure_2.jpg]]
*Figure 2: Qualitative comparison on self-reenactment of head avatars. Our method reproduces expressions more faithfully, with accurate mouth opening and eye blinking and clearer tooth details*

## 方法谱系与知识库定位

### 1. 与现有头部化身方法的继承与差异

Fresco 并非提出全新的几何表示，而是在现有混合表示（参数化人脸网格 + 显式毛发场）的训练动态上引入频空联合优化。其底层表示继承自两条主流路线：

- **网格‑高斯混合路线**：Fresco 的人脸区域采用 FLAME 参数化网格驱动可学习 UV 位移图与神经纹理，毛发及外围区域采用各向异性 3D 高斯集合。这一混合架构与 **MeGA**（Wang et al., CVPR 2025）和 **HERA**（Cai et al., arXiv 2024）同属一族——均将网格的结构稳定性与高斯的灵活表达能力结合。差异在于，MeGA 和 HERA 侧重于表示本身的设计（如网格与高斯的耦合方式），而 Fresco 保持表示不变，将改进集中在优化策略层面。

- **纯高斯/点基路线**：**GaussianAvatar**（Qian et al., CVPR 2024）和 **PointAvatar**（Zheng et al., CVPR 2023）分别采用全高斯或全点基表示。这些方法依赖逐视图光度损失进行端到端优化，缺乏跨视图几何对应约束，训练早期易产生伪高频锐化伪影和视图间漂移。Fresco 的 UV 空间跨视图纹素对齐正则化正是针对这一瓶颈的补丁式改进——不改变底层表示，仅通过监督信号重塑优化景观。

### 2. 核心机制的知识库定位

Fresco 的两个关键机制在现有文献中有清晰的知识谱系：

**频率课程调度**：
- 在图像域使用可微分高斯滤波和 Difference-of-Gaussian（DoG）带通滤波构建拉普拉斯金字塔分解，实现从低频到高频的渐进学习。
- 频率课程（curriculum learning）思想在 3D 重建中已有先例（如 NeRF 系列中的位置编码频率退火），但 Fresco 将其直接作用于图像域而非坐标编码域，且通过余弦退火调度（Eq. 9）自动扩展带宽，避免了手动调参的繁琐。
- 高频增强分支引入边缘感知损失（Eq. 5）与梯度差异损失 GDL（Eq. 6）的组合，在恢复细节的同时抑制过锐化，这一设计与图像超分辨率中的边缘保持损失有方法论上的亲缘性。

**UV 空间跨视图一致性**：
- 可微分 UV 烘焙算子将多视图渲染投影至共享纹理空间，利用可见性加权的 L1 损失（Eq. 10）对齐跨视图纹素，本质上是一种“纹理空间的多视图立体约束”。
- 缝正则化（Eq. 12）包含跨图表颜色连续性约束与局部全变分平滑，直接针对 UV 展开的接缝伪影，与纹理拼接（texture stitching）领域的技术一脉相承。
- 三阶段优化调度（Eq. 15）——先低频、再引入 UV 一致性、最后激活高频与缝正则——体现了“先全局后局部，先结构后细节”的优化哲学，与渐进式图像生成中的多阶段训练策略一致。

### 3. 适用边界与局限

基于论文提供的证据，Fresco 的适用边界和局限可归纳如下：

**已验证的适用场景**：
- 多视图捕捉设置（NeRSemble 数据集），训练视图覆盖头部各角度。
- 受控室内光照条件下的面部表情重建与重演。
- 需要高保真纹理细节（皱纹、牙齿）和跨视图一致性的应用。

**已知局限**（论文自身指出或可从实验设置推断）：
- **数据多样性受限**：仅在 NeRSemble 单一数据集上验证，该数据集的面部表情和光照条件多样性有限，未测试极端表情（如大幅度张嘴、挤压变形）或户外非受控光照场景。泛化到更复杂环境需人工验证。
- **超参数敏感性**：频率课程中的高斯滤波标准差 σ、频带激活时间点 T_i、各阶段损失权重（α、β、λ 系列）均需手动设定，对不同分辨率和场景缺乏自适应性。论文未提供超参数自动调优机制或跨场景迁移的经验法则。
- **实时性与部署可行性未覆盖**：论文未讨论推理速度、显存占用或移动端部署可行性，因此无法评估其在实时应用（如 VR/AR 头显）中的实用性。
- **几何约束缺失**：当前优化目标完全基于图像域（频率损失、UV 纹理损失），未引入深度或法向等显式几何监督。在极端视角或遮挡情况下，仅靠纹理一致性可能不足以维持几何精度。

### 4. 开放问题

基于 Fresco 的设计逻辑与现有证据缺口，以下问题值得后续探索：

1. **表示无关性验证**：频空联合优化范式是否可迁移到纯 NeRF、3D Gaussian Splatting 等其他底层表示？Fresco 的 UV 烘焙依赖网格参数化提供的共享纹理空间，对于无网格表示需重新设计跨视图对齐机制。

2. **大规模户外数据的鲁棒性**：若在更大规模、高动态光照、复杂背景的户外数据上训练，UV 空间的可见性权重估计和缝正则是否仍能保持鲁棒？强光照变化可能导致可见性判断失效，背景干扰可能破坏 UV 烘焙的准确性。

3. **几何约束的融合潜力**：能否结合深度或法向几何约束，进一步提升跨视图几何一致性？当前纯图像域监督在纹理稀疏区域（如皮肤平滑区）可能缺乏足够信号，几何线索可提供互补的正则化。

4. **自适应频率课程**：能否根据场景内容或训练状态自动调整频率课程参数（如 σ、T_i），从而减少人工调参负担并提升跨场景迁移能力？元学习或基于梯度的超参数优化是可能的探索方向。

## 原文 PDF

![[paperPDFs/CVPR_2026/Fresco_Frequency_Spatial_Consistent_Optimization_for_Fine_Grained_Head_Avatar_Modeling.pdf]]
