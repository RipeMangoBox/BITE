---
title: Event-Illumination Collaborative Low-light Image Enhancement with a High-resolution Real-world Dataset
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/Event_Illumination_Collaborative_Low_light_Image_Enhancement_with_a_High_resolution_Real_world_Dataset.pdf
project_link: null
code_link: "https://github.com/QUEAHREN/EIC-LIE"
aliases:
- EL
- EICLLIEHRRWD
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/benchmarks_datasets_evaluation
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: 事件与光照信息的双向协同交互机制（前向收集与反向注入），以及基于图像亮度统计的动态事件滤波器。
primary_logic: 将事件的高动态范围边缘细节与图像的光照先验相结合，通过前向收集与反向注入实现双向互补增强，并利用亮度引导的自适应滤波抑制事件噪声，从而在提升纹理恢复的同时抑制低光噪声。
claims:
- 在多个基准数据集上，EIC-LIE一致超越现有最先进方法，例如在SDE-indoor上PSNR达到23.33 dB，比EvLight高0.89 dB。
- 消融实验表明，事件和光照指导分别带来2.55 dB和2.23 dB的PSNR提升，验证了协同交互的必要性。
- 与无事件过滤相比，IAEF模块带来了2.71 dB的PSNR提升，证实了光照感知滤波对噪声抑制的有效性。
- 特征可视化显示双向反向注入能产生更紧凑的模态分离，优于直接交叉注意力。
---

# Event-Illumination Collaborative Low-light Image Enhancement with a High-resolution Real-world Dataset

> [!tip] 核心洞察
> 将事件的高动态范围边缘细节与图像的光照先验相结合，通过前向收集与反向注入实现双向互补增强，并利用亮度引导的自适应滤波抑制事件噪声，从而在提升纹理恢复的同时抑制低光噪声。

| 字段 | 内容 |
|------|------|
| 中文题名 | 事件-光照协同低光图像增强与高分辨率真实世界数据集 |
| 英文题名 | Event-Illumination Collaborative Low-light Image Enhancement with a High-resolution Real-world Dataset |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2605.22186) · [Code](https://github.com/QUEAHREN/EIC-LIE) |
| Topic | #topic/vision_multimodal_applications #topic/benchmarks_datasets_evaluation #topic/vision_multimodal_applications/image_and_video_generation |
| Method | EIC-LIE |
| Dataset | SDE-indoor, SDE-outdoor, SDSD-indoor, SDSD-outdoor |

> [!tip] 效果简介
> - SDE-indoor 上，PSNR 23.33 vs 22.44 (EvLight) (+0.89 dB)。
> - SDE-outdoor 上，PSNR 24.22 vs 23.21 (EvLight) (+1.01 dB)。
> - SDSD-indoor 上，PSNR 29.76 vs 28.52 (EvLight) (+1.24 dB)。

## 概要

低光图像增强（Low-light Image Enhancement, LIE）是计算机视觉中的基础任务，旨在从严重欠曝光的图像中恢复出正常光照下的清晰视觉内容。传统基于帧图像的增强方法在极端低光条件下往往面临纹理丢失和噪声放大的困境。事件相机（event camera）因其高动态范围（HDR）和微秒级时间分辨率，能够捕捉低光场景中帧图像丢失的边缘和运动信息，为低光增强提供了新的模态补充。

然而，现有的事件-图像融合增强方法存在一个**核心瓶颈**：它们普遍依赖简单的特征融合策略（如直接交叉注意力或信噪比引导的选择性融合），忽视了Retinex理论中全局光照信息的结构性作用，同时对真实低光条件下事件信号中的噪声缺乏有效建模。这导致增强结果在纹理细节恢复和噪声抑制之间难以取得平衡——要么纹理缺失，要么残留噪声伪影。

针对上述问题，本文提出 **EIC-LIE**（Event-Illumination Collaborative Low-light Image Enhancement），一个事件-光照协同增强框架。其**核心洞察**在于：将事件相机的高动态范围边缘细节与帧图像的光照先验进行双向互补增强，而非简单的单向信息注入。具体而言，EIC-LIE 设计了两个关键机制：

1. **事件-光照协同交互模块（EICI）**：通过“前向收集”（Forward Gathering）与“反向注入”（Backward Injection）实现事件特征与光照特征的双向交互，使两种模态在潜在空间中相互补全。前向收集从事件和光照特征中提取互补信息汇聚到图像特征，反向注入则将融合后的信息重新分配回各模态，形成精炼的特征表示。

2. **光照感知事件滤波器（IAEF）**：利用帧图像提取的光照先验动态生成滤波核与偏移量，对事件特征进行自适应去噪。该模块根据图像亮度统计特征调整滤波权重，在保留有效事件边缘信号的同时抑制低光噪声。

在实验层面，EIC-LIE 在五个真实与合成数据集上一致超越现有最先进方法。在 SDE-indoor 上 PSNR 达到 23.33 dB，比 **EvLight** 提升 0.89 dB；在 SDSD-indoor 上达到 29.76 dB，提升 1.24 dB。消融实验进一步验证了协同交互的必要性：事件指导与光照指导分别带来 2.55 dB 和 2.23 dB 的 PSNR 增益，IAEF 模块相较于无滤波基线提升 2.71 dB，反向注入设计相较于直接交叉注意力提升超过 2.58 dB。

在方法谱系中，EIC-LIE 处于事件-图像多模态增强与 Retinex 理论的交叉点。它既区别于纯图像域的 Retinex 方法（如 **MambaLLIE**），也不同于仅做单向选择性融合的事件-图像方法（如 **EvLight**），而是通过双向协同交互和光照感知滤波，构建了更完整的低光增强范式。此外，本文还贡献了高分辨率真实世界数据集 RLE，为事件-图像增强提供了更严格的对齐基准。

低光图像增强旨在从光照不足的观测中恢复出正常光照下的清晰图像，是计算摄影与底层视觉中的基础问题。传统方法依赖Retinex理论，将图像建模为反射分量与光照分量的逐元素乘积 $\mathbf{I} = \mathbf{R} \odot \mathbf{L}$，通过估计并调整光照分量来实现增强。然而，在极端低光条件下，帧式相机捕获的图像存在严重的噪声和细节丢失，使得单纯依靠图像先验的增强方法面临信息瓶颈。

事件相机（event camera）的引入为这一困境提供了新的突破口。事件相机异步感知每个像素的亮度对数变化，在变化量超过对比度阈值 $c$ 时触发事件 $\log \frac{\mathcal{L}(x_k, y_k, t_k)}{\mathcal{L}(x_k, y_k, t_k - \Delta t)} = p_k \cdot c$，具有微秒级时间分辨率和高动态范围（HDR）特性。这使得事件信号能够在极暗场景中保留边缘和纹理细节，弥补帧式图像的不足。

然而，现有的事件-图像融合低光增强方法存在两个关键缺口。**其一，多模态特征融合停留在浅层交互。** 以 **EvLight** 为代表的现有工作采用基于SNR的选择性融合或直接交叉注意力，忽视了Retinex理论中全局光照信息对事件特征的引导作用，导致增强结果出现纹理缺失和噪声伪影。**其二，对真实低光下事件信号的噪声缺乏有效建模。** 事件相机在低光环境中本身会产生大量噪声事件，现有方法或缺乏专门的去噪机制，或仅依赖固定的SNR图进行滤波，无法根据场景亮度自适应地抑制噪声。

针对上述缺口，本文提出事件-光照协同低光图像增强框架 **EIC-LIE**。核心动机在于：将事件的高动态范围边缘细节与图像的光照先验进行**双向互补增强**——通过前向收集从事件和光照特征中汇聚信息，再通过反向注入将融合后的特征精炼回各模态；同时，利用**亮度引导的自适应滤波**机制，根据图像亮度统计动态调整事件特征的滤波权重，在提升纹理恢复的同时有效抑制低光噪声。

## 核心方法与创新机理

EIC-LIE 的核心创新在于突破现有事件-图像融合方法中“简单特征拼接或选择性融合”的范式，转而构建**事件与光照信息的双向协同交互机制**，并引入**光照感知的动态事件去噪**，从而系统性地解决真实低光场景下纹理恢复与噪声抑制的矛盾。

### 瓶颈分析：从单向融合到双向协同

现有事件低光增强方法（如 **EvLight**）虽已尝试利用事件的高动态范围特性，但其融合策略存在两个根本缺陷：

1. **光照先验缺失**：方法仅依赖图像特征或简单的信噪比（SNR）引导融合，未显式引入 Retinex 理论中的全局光照信息。低光图像本身携带的光照分布先验（如亮度梯度、阴影边界）被忽视，导致增强结果在极暗区域的纹理恢复不完整。
2. **事件噪声欠建模**：真实低光下事件信号因光子散粒噪声而严重退化，现有方法缺乏针对性的去噪机制。EvLight 的 SNR 引导滤波仅基于固定阈值，无法适应场景亮度的空间变化，导致增强图像出现噪声伪影。

EIC-LIE 通过两个核心模块——**事件-光照协同交互模块（EICI）**和**光照感知事件滤波器（IAEF）**——分别针对上述瓶颈进行因果性改进。

### Changed Slot 1：从单向选择性融合到前向收集与反向注入

**Baseline 策略**：EvLight 采用 SNR 引导的选择性融合，即根据事件信号质量决定融合权重，本质上是单向的信息筛选。

**EIC-LIE 策略**：EICI 模块设计了**前向收集（Forward Gathering）**与**反向注入（Backward Injection）**两个对称过程，实现事件与光照特征的互补增强：

- **前向收集**：分别从事件特征 $\mathbf{F}_e$ 和光照特征 $\mathbf{F}_l$ 向图像特征 $\mathbf{F}_i$ 传输信息，通过协方差交叉注意力生成互补的中间特征 $\mathbf{F}_i'$ 和 $\mathbf{F}_i''$：
  $$(\mathbf{F}_i', \mathbf{A}_e) = \mathcal{G}_e(\mathbf{F}_e, \mathbf{F}_i), \quad (\mathbf{F}_i'', \mathbf{A}_l) = \mathcal{G}_l(\mathbf{F}_l, \mathbf{F}_i)$$
  其中 $\mathbf{A}_e$ 和 $\mathbf{A}_l$ 为注意力矩阵，编码了模态间的对应关系。

- **反向注入**：在潜在空间融合后，利用存储的注意力矩阵将融合特征重新分配回事件和光照模态：
  $$\hat{\mathbf{F}}_l = \mathcal{I}_l(\hat{\mathbf{F}}_i, \mathbf{A}_l) + \mathbf{F}_l, \quad \hat{\mathbf{F}}_e = \mathcal{I}_e(\hat{\mathbf{F}}_i, \mathbf{A}_e) + \mathbf{F}_e$$
  这一设计使得各模态特征在融合后被“精炼”，而非简单丢弃原始信息。

**因果机制**：反向注入通过注意力复用施加了隐式对齐约束，迫使前向收集阶段学习更紧凑的模态对应关系。t-SNE 可视化（Figure 3(b)）证实，引入注意力复用后，事件与光照特征在潜在空间中的分离更加紧凑，表明模态间信息交互更充分。消融实验（Table 6）表明，反向注入设计相较于直接交叉注意力基线带来 **超过 2.58 dB PSNR 提升**。

### Changed Slot 2：从无/固定去噪到光照感知动态事件滤波

**Baseline 策略**：EvLight 基于固定 SNR 图进行事件滤波，无法适应场景中亮度的空间变化。

**EIC-LIE 策略**：IAEF 模块利用光照特征 $\mathbf{F}_l$ 动态生成滤波核，同时从事件特征 $\mathbf{F}_e$ 中提取逐像素的权重与空间偏移，实现自适应去噪：

- **光照感知核提取**：从光照特征中生成一维分离滤波核（垂直 $\mathbf{K}_v$ 和水平 $\mathbf{K}_h$），使滤波器形状随局部亮度变化：
  $$\mathbf{K}_v, \mathbf{K}_h = \mathcal{K}(\mathbf{F}_l)$$

- **事件驱动权重与偏移**：从事件特征中提取逐像素权重 $\mathbf{W}$ 和空间偏移 $\mathbf{P}_x, \mathbf{P}_y$，用于控制滤波强度与采样位置：
  $$\mathbf{W} = \mathcal{W}(\mathbf{F}_e), \quad \mathbf{P}_x, \mathbf{P}_y = \mathcal{P}(\mathbf{F}_e)$$

- **自适应空间采样**：最终滤波输出为：
  $$\hat{\mathbf{F}}_e(m,n) = \sum \mathbf{W}(m,n) \cdot \mathbf{K}(m,n) \cdot \mathcal{S}(\mathbf{F}_e, (m+\mathbf{P}_x(m,n), n+\mathbf{P}_y(m,n)))$$

**因果机制**：光照特征提供了稳定的亮度统计信息，指导滤波器在暗区增强去噪强度、在亮区保留细节；事件驱动的偏移使滤波器能够沿边缘方向采样，避免纹理模糊。特征可视化（Figure 3(d)）显示，Post-IAEF 事件特征的噪声水平显著低于 Pre-IAEF。消融实验（Table 5）表明，IAEF 模块相较于无事件滤波的基线带来 **2.71 dB PSNR 提升**。

### 协同效应的量化验证

两个创新模块并非孤立工作，而是通过双向交互形成协同增益。消融实验（Table 4）表明：

- 单独引入事件指导（无光照交互）带来 **2.55 dB PSNR / 0.0476 SSIM** 提升；
- 单独引入光照指导（无事件交互）带来 **2.23 dB PSNR / 0.0383 SSIM** 提升；
- 两者协同工作时，总增益超过单独增益之和，验证了双向交互的必要性。

### 与现有方法的本质差异

| 维度 | EvLight | EIC-LIE |
|------|---------|---------|
| 融合策略 | SNR 引导单向选择 | 前向收集 + 反向注入双向协同 |
| 光照先验 | 未显式利用 | Retinex 光照先验参与交互 |
| 事件去噪 | 固定 SNR 阈值滤波 | 光照感知动态核 + 事件驱动偏移 |
| 模态关系 | 简单拼接 | 注意力复用实现模态精炼 |

综上，EIC-LIE 的核心创新在于将事件-图像增强从“信息筛选”范式升级为“双向协同 + 动态去噪”范式，通过因果性设计解决了真实低光场景下纹理恢复与噪声抑制的固有矛盾。

EIC-LIE 的整体 pipeline 以“事件-光照协同”为核心设计理念，将事件相机的高动态范围（HDR）边缘细节与帧相机的光照先验进行双向互补增强。如图 2(a) 所示，框架由四个主要模块串联构成：光照先验估计、事件堆叠表示、EICI（事件-光照协同交互）模块、IAEF（光照感知事件滤波器），以及最终的图像重建解码器。

**输入与预处理。** 系统接收一对低光图像 $\mathbf{I}_{\text{low}}$ 和同步的事件流作为输入。对于低光图像，首先从 RGB 三通道取最大值提取初始光照先验 $\mathbf{L}_p$，作为后续光照分支的引导信号（Sec. 3.2）。对于事件流，采用基于时间堆叠的 SBT（Stacking Based on Time）表示，将事件按 $B$ 个时间窗口累积极性，形成体素表示 $\mathcal{V}(i) = \sum_{k \in \mathcal{T}_i} p_k$（Eq. (4)），再经浅层卷积编码为事件特征 $\mathbf{F}_e$。低光图像则经独立编码器提取图像特征 $\mathbf{F}_i$。

**核心交互：EICI 模块。** EICI 是实现事件-光照协同的关键（图 2(b)），包含前向收集（Forward Gathering）和反向注入（Backward Injection）两个对称过程。前向收集阶段，分别从事件特征 $\mathbf{F}_e$ 和光照特征 $\mathbf{F}_l$ 向图像特征 $\mathbf{F}_i$ 进行基于协方差交叉注意力的信息传输，得到互补的中间特征 $\mathbf{F}_i'$ 和 $\mathbf{F}_i''$，同时存储注意力矩阵 $\mathbf{A}_e$ 和 $\mathbf{A}_l$（Eq. (7)）。三者聚合后经 Transformer 自注意力在潜在空间融合为 $\hat{\mathbf{F}}_i$（Eq. (8)）。反向注入阶段利用存储的注意力矩阵，将融合特征中的模态专属信息重新分配回事件和光照分支，得到精炼特征 $\hat{\mathbf{F}}_e$ 和 $\hat{\mathbf{F}}_l$（Eq. (9)）。这一双向设计使得三种模态在交互中既保留各自特性，又实现深层互补。

**自适应去噪：IAEF 模块。** 精炼后的事件特征 $\hat{\mathbf{F}}_e$ 进入 IAEF 进行光照感知的去噪（图 2(c)）。该模块从光照特征 $\mathbf{F}_l$ 中提取一维分离滤波核 $\mathbf{K}_v, \mathbf{K}_h$（Eq. (10)），同时从事件特征中动态生成逐像素的滤波权重 $\mathbf{W}$ 和空间偏移 $\mathbf{P}_x, \mathbf{P}_y$（Eq. (11)），最终通过加权空间采样输出滤波后的事件特征（Eq. (12)）。IAEF 的核心作用在于利用图像亮度统计特征引导事件滤波，使低光区域的噪声被自适应抑制，而高对比度边缘得以保留。

**输出。** 融合后的图像特征与滤波后的事件特征经图像重建模块解码，生成最终增强图像。整个 pipeline 的模块间数据流为：低光图像 → 光照先验 / 图像特征；事件流 → SBT 表示 → 事件特征；三者进入 EICI 双向交互后，事件分支经 IAEF 去噪，最终与图像分支融合解码输出。

![[assets/figures/papers/paper_list_l749_https_arxiv_org_abs_2605_22186/figures/003_Figure_2.jpg]]
*Figure 2: An overview of (a) our EIC-LIE. The core modules of EIC-LIE are (b) Event-Illumination Collaborative Interaction (EICI) and (c) Illumination-aware Event Filter (IAEF). Details of each module can be found in supp*

EIC-LIE 的核心设计围绕两个关键模块展开：**事件-光照协同交互模块（EICI）** 与 **光照感知事件滤波器（IAEF）**。前者实现事件与光照特征的双向互补增强，后者利用光照先验对事件特征进行自适应去噪。以下逐一推导其数学机理。

### 3.1 预备知识：Retinex 分解与事件表示

低光图像增强的 Retinex 理论将观测图像 $\mathbf{I}$ 分解为反射分量 $\mathbf{R}$ 与光照分量 $\mathbf{L}$ 的逐元素乘积：

$$\mathbf{I} = \mathbf{R} \odot \mathbf{L} \tag{1}$$

正常光图像 $\mathbf{N}$ 可通过估计的分量恢复：$\mathbf{N} = \tilde{\mathbf{R}} \odot \tilde{\mathbf{L}}$，或等价地通过亮化图 $\bar{\mathbf{L}}$ 恢复：$\mathbf{N} = \mathbf{I} \odot \bar{\mathbf{L}}$（式 (2)）。

事件相机在亮度对数变化超过对比度阈值 $c$ 时触发事件，极性 $p_k \in \{-1, +1\}$ 表示亮度增减方向：

$$\log \frac{\mathcal{L}(x_k, y_k, t_k)}{\mathcal{L}(x_k, y_k, t_k - \Delta t)} = p_k \cdot c \tag{3}$$

为将异步事件流转换为适合 CNN 处理的张量，本文采用基于时间堆叠的 SBT 表示，将事件按 $B$ 个时间窗口累积极性：

$$\mathcal{V}(i) = \sum_{k \in \mathcal{T}_i} p_k \tag{4}$$

其中 $\mathcal{T}_i$ 为第 $i$ 个时间窗口内的事件集合。

### 3.2 光照先验估计

Retinex 理论启示：低光图像中蕴含可显式利用的光照结构信息。EIC-LIE 从低光输入图像 $\mathbf{I}$ 的通道最大值中提取初始光照先验 $\mathbf{L}_p$，作为后续协同交互的引导信号。该先验虽粗糙，但提供了全局亮度分布的统计特征，为事件特征的去噪与增强提供了稳定的参考锚点。

### 3.3 事件-光照协同交互模块（EICI）

EICI 的核心创新在于将多模态融合建模为**前向收集（Forward Gathering）**与**反向注入（Backward Injection）**的双向过程，而非简单的交叉注意力拼接。

#### 前向收集

前向收集从辅助特征 $\mathbf{X}$ 向主特征 $\mathbf{T}$ 传输信息，输出更新后的主特征 $\mathbf{T}'$ 及注意力矩阵 $\mathbf{A}$：

$$(\mathbf{T}', \mathbf{A}) = \mathcal{G}(\mathbf{X}, \mathbf{T}) \tag{5}$$

该操作基于协方差交叉注意力实现，$\mathbf{A}$ 记录了特征间空间对应关系。

在 EICI 中，前向收集分两路并行执行：分别从事件特征 $\mathbf{F}_e$ 和光照特征 $\mathbf{F}_l$ 向图像特征 $\mathbf{F}_i$ 收集高动态范围细节与全局光照结构信息：

$$(\mathbf{F}_i', \mathbf{A}_e) = \mathcal{G}_e(\mathbf{F}_e, \mathbf{F}_i), \quad (\mathbf{F}_i'', \mathbf{A}_l) = \mathcal{G}_l(\mathbf{F}_l, \mathbf{F}_i) \tag{7}$$

#### 潜在空间融合

聚合后的特征 $\mathbf{F}_i + \mathbf{F}_i' + \mathbf{F}_i''$ 通过 Transformer 自注意力在潜在空间中深度融合，得到增强的图像特征：

$$\hat{\mathbf{F}}_i = \mathcal{T}(\mathbf{F}_i + \mathbf{F}_i' + \mathbf{F}_i'') \tag{8}$$

#### 反向注入

反向注入是 EICI 区别于常规融合的关键设计。它利用前向收集阶段存储的注意力矩阵 $\mathbf{A}$，将融合后的主特征信息重新分配回辅助特征，实现模态精炼：

$$\mathbf{X}' = \mathcal{I}(\mathbf{T}', \mathbf{A}) + \mathbf{X} \tag{6}$$

在 EICI 中，反向注入将融合特征 $\hat{\mathbf{F}}_i$ 分解为精炼的事件和光照模态特征：

$$\hat{\mathbf{F}}_l = \mathcal{I}_l(\hat{\mathbf{F}}_i, \mathbf{A}_l) + \mathbf{F}_l, \quad \hat{\mathbf{F}}_e = \mathcal{I}_e(\hat{\mathbf{F}}_i, \mathbf{A}_e) + \mathbf{F}_e \tag{9}$$

**设计机理**：注意力复用（attention reuse）引入了隐式对齐约束，使得反向注入后的特征在 t-SNE 可视化中呈现出更紧凑的模态分离（Figure 3(b) vs Figure 3(a)），验证了双向精炼的有效性。消融实验进一步表明，反向注入设计相较直接交叉注意力基线带来超过 2.58 dB 的 PSNR 提升（Table 6）。

### 3.4 光照感知事件滤波器（IAEF）

真实低光场景中，事件信号受噪声严重污染，且噪声强度与局部光照条件密切相关。IAEF 利用光照特征动态生成滤波参数，对事件特征进行内容自适应的去噪。

#### 光照感知核提取

从光照特征 $\mathbf{F}_l$ 中提取一维分离滤波核（垂直和水平方向），以降低计算复杂度：

$$\mathbf{K}_v, \mathbf{K}_h = \mathcal{K}(\mathbf{F}_l) \tag{10}$$

#### 事件驱动权重与偏移提取

从事件特征 $\mathbf{F}_e$ 中提取逐像素的滤波权重 $\mathbf{W}$ 和空间偏移 $\mathbf{P}_x, \mathbf{P}_y$，使滤波器能自适应地调整采样位置：

$$\mathbf{W} = \mathcal{W}(\mathbf{F}_e), \quad \mathbf{P}_x, \mathbf{P}_y = \mathcal{P}(\mathbf{F}_e) \tag{11}$$

#### 自适应空间采样

最终，IAEF 对事件特征进行加权空间采样，输出滤波后的事件特征 $\hat{\mathbf{F}}_e$：

$$\hat{\mathbf{F}}_e(m,n) = \sum \mathbf{W}(m,n) \cdot \mathbf{K}(m,n) \cdot \mathcal{S}(\mathbf{F}_e, (m+\mathbf{P}_x(m,n), n+\mathbf{P}_y(m,n))) \tag{12}$$

其中 $\mathbf{K}(m,n) = \mathbf{K}_v(n) \cdot \mathbf{K}_h(m)$ 为可分离核的近似，$\mathcal{S}(\cdot)$ 为空间采样函数。

**设计机理**：光照先验提供了稳定的亮度统计特征，使滤波核能感知全局光照分布；事件特征则提供局部纹理细节，驱动权重和偏移的自适应调整。Figure 3(d) 显示，经 IAEF 处理后的事件特征（Post-IAEF）噪声水平显著低于处理前（Pre-IAEF）。消融实验证实，IAEF 模块相较无事件滤波基线带来 2.71 dB 的 PSNR 提升（Table 5），且其效果优于基于固定 SNR 图的传统滤波策略（Table 5 中与其他滤波器变体的对比）。

## 实验与关键发现

### 数据集与实验设置

EIC-LIE 在五个基准数据集上进行评估，涵盖合成数据集与真实世界数据集。合成数据集包括 **SDE-indoor**、**SDE-outdoor**、**SDSD-indoor** 和 **SDSD-outdoor**，这些数据集通过模拟低光条件生成成对的低光-正常光图像及对应的事件流。真实世界数据集为本文提出的 **RLE 数据集**，其通过双分光棱镜光学系统实现高分辨率 RGB 相机与事件相机的共轴同步采集，提供 1440×1080 分辨率的严格时空对齐的低光-正常光图像对及事件流。现有真实世界事件低光增强数据集的系统对比见 Table 1。

![[assets/figures/papers/paper_list_l749_https_arxiv_org_abs_2605_22186/figures/002_Table_1.jpg]]
*Table 1: Summary of existing real-world event-based low-light enhancement datasets (Sec. 2.3)*

评估指标采用 PSNR 和 SSIM，所有方法的输入图像分辨率统一处理，FLOPs 在 256×256 分辨率下计算以保证效率对比的公平性。推理时间在 NVIDIA 4090 GPU 上测量，图像尺寸为 1024×768。

### 主要定量结果

EIC-LIE 在所有五个基准数据集上一致超越现有最先进方法，包括基于事件-图像融合的方法（如 **EvLight**）、基于纯图像的 Retinex 方法（如 **MambaLLIE**）以及事件-视频增强方法（如 **EvLowlight**）。Table 2 和 Table 3 汇总了完整对比结果，关键指标如下：

![[assets/figures/papers/paper_list_l749_https_arxiv_org_abs_2605_22186/figures/006_Table_2.jpg]]
*Table 2: The quantitative results on SDE-indoor, SDE-outdoor, SDSD-indoor, and SDSD-outdoor test datasets. Note that ’E’, ’I’, and ’I+E’ represent the input type corresponding to event-only, image-only, and event-image, respectively. FLOPs are estimated with the resolution of 256 × 256. The best and the second results are boldfaced and underlined, respectively*

![[assets/figures/papers/paper_list_l749_https_arxiv_org_abs_2605_22186/figures/008_Table_3.jpg]]
*Table 3: The quantitative results on RLE test datasets. The average runtime is computed for an image size of 1024 × 768, on an NVIDIA 4090 GPU. EvLowlight [31] is a Video-based∗ method*

- **SDE-indoor**：PSNR 达到 23.33 dB，较 EvLight 的 22.44 dB 提升 **+0.89 dB**。
- **SDE-outdoor**：PSNR 达到 24.22 dB，较 EvLight 的 23.21 dB 提升 **+1.01 dB**。
- **SDSD-indoor**：PSNR 达到 29.76 dB，较 EvLight 的 28.52 dB 提升 **+1.24 dB**。
- **SDSD-outdoor**：PSNR 达到 27.45 dB，较 EvLight 的 26.67 dB 提升 **+0.78 dB**。
- **RLE**：PSNR 达到 23.63 dB，SSIM 达到 0.7670，较 EvLight 的 22.68 dB / 0.7201 分别提升 **+0.95 dB / +0.0469**。

在 RLE 数据集上的推理效率方面，EIC-LIE 在 1024×768 分辨率下的平均运行时间具有竞争力（详见 Table 3），表明该方法在保持高性能的同时未引入不可接受的计算开销。

### 消融实验

消融实验系统验证了 EIC-LIE 各核心组件的独立贡献，结果汇总于 Table 4、Table 5 和 Table 6。

![[assets/figures/papers/paper_list_l749_https_arxiv_org_abs_2605_22186/figures/011_Table_4.jpg]]
*Table 4: Ablation study for the event and il*

**事件与光照指导的必要性**（Table 4）：以无事件和无光照指导的基线（Case 0）为参照，单独引入事件指导带来 **2.55 dB PSNR 和 0.0476 SSIM** 的提升；单独引入光照指导带来 **2.23 dB PSNR 和 0.0383 SSIM** 的提升。两者同时启用时性能达到最优，证实了事件高动态范围边缘信息与 Retinex 光照先验之间存在互补增益，协同交互不可或缺。

**光照感知事件滤波器（IAEF）的有效性**（Table 5）：以无事件滤波的配置（Case 3）为基线，引入 IAEF 模块后 PSNR 提升 **2.71 dB**。该结果表明，基于图像亮度统计动态调整滤波权重和空间偏移的机制，能够有效抑制真实低光场景下事件信号中的噪声，从而避免增强结果中的噪声伪影。

**反向注入（Backward Injection）设计的优势**（Table 6）：以直接交叉注意力（Case 6）为基线，采用反向注入设计带来超过 **2.58 dB** 的 PSNR 提升。进一步的特征可视化分析（Figure 3(b)）显示，反向注入通过复用注意力矩阵实现隐式对齐约束，使得事件、光照和图像特征在潜在空间中形成更紧凑的模态分离，从而促进了更有效的多模态信息融合。

### 特征可视化分析

Figure 3 提供了 EICI 和 IAEF 模块内部特征行为的定性证据：

- **t-SNE 分析**（Figure 3(a) vs 3(b)）：无注意力复用的 EICI 中，各模态特征在低维空间中混叠严重；引入注意力复用后，事件、光照和图像特征形成明显分离的簇，验证了反向注入机制对模态解耦的促进作用。
- **IAEF 去噪效果**（Figure 3(d)）：对比 Pre-IAEF 和 Post-IAEF 的事件特征图，经 IAEF 处理后的特征噪声水平显著降低，纹理结构更加清晰，与 Table 5 的定量消融结果相互印证。

### 视觉质量对比

Figure 5 展示了 RLE 数据集上的视觉对比结果。EIC-LIE 在恢复暗区纹理细节的同时有效抑制了噪声放大，相比于 EvLight 等方法，增强图像在边缘锐度和色彩保真度上均有明显改善。Figure 6 和 Figure 7 分别展示了 SDE 和 SDSD 数据集上的视觉结果，进一步验证了该方法在不同场景类型下的泛化能力。Figure 1 采用颜色不变量可视化工具，从物体固有颜色和光谱分布边缘两个维度展示了 EIC-LIE 相对其他方法的增强优势。

![[assets/figures/papers/paper_list_l749_https_arxiv_org_abs_2605_22186/figures/001_Figure_1.jpg]]
*Figure 1: Visual comparison of LIE methods on the proposed realworld RLE dataset. To better illustrate the enhancement effects, color invariants [15] are adopted as visualization tools. Specifically, the invariant C can be interpreted as describing object color regardless of intensity, while W functions as an edge detector specific to changes in spectral distribution. See supp. for more details regarding the invariants*

## 定位与知识库关联

### 1. 问题脉络与现有方法瓶颈

事件相机低光图像增强（Event-based LIE）的核心矛盾在于：事件流提供了极端光照下图像传感器丢失的高动态范围（HDR）边缘信息，但事件信号本身在低光条件下充满噪声，且缺乏全局光照上下文。现有方法在以下三个维度上存在系统性不足：

**融合策略的浅层性。** 以 **EvLight** 为代表的事件-图像融合方法，依赖信噪比（SNR）引导的选择性融合机制——根据事件信号的局部SNR决定融合权重。这种单向的、基于质量评估的特征筛选，忽视了Retinex理论所揭示的光照-反射分解先验，无法在全局光照约束下对事件特征进行语义层面的补全与修正。结果是增强图像在暗区出现纹理缺失，在亮区残留噪声伪影。

**事件去噪的盲化。** 现有方法对事件噪声的处理停留在固定阈值或基于局部SNR图的滤波阶段。**EvLight** 的SNR引导融合本质上是一种隐式的软阈值去噪，但其SNR估计未考虑场景光照分布——在极暗区域，事件信号与噪声的统计特性高度重叠，仅靠局部SNR无法有效区分。这导致去噪过程要么过度平滑有效边缘，要么保留大量噪声尖峰。

**光照先验的缺失。** 基于纯图像的Retinex方法（如 **MambaLLIE**，采用状态空间模型进行光照估计）虽然显式建模了光照分量，但完全丢弃了事件流中的HDR信息，在极低光下无法恢复被噪声淹没的反射细节。事件-视频增强方法（如 **EvLowlight**）则依赖时序冗余进行多帧融合，计算开销大且不适用于单帧图像增强场景。

### 2. EIC-LIE的方法定位与因果调节机制

EIC-LIE的核心贡献在于识别并操作了两个因果调节变量（causal knobs）：

**调节变量一：事件-光照的双向协同交互机制。** 与现有方法的单向融合（事件→图像或图像→事件）不同，EICI模块实现了“前向收集（Forward Gathering）→ 潜在空间融合 → 反向注入（Backward Injection）”的闭环。前向收集阶段，事件特征 $\mathbf{F}_e$ 和光照特征 $\mathbf{F}_l$ 分别通过协方差交叉注意力向图像特征 $\mathbf{F}_i$ 传输信息：

$$(\mathbf{F}_i', \mathbf{A}_e) = \mathcal{G}_e(\mathbf{F}_e, \mathbf{F}_i), \quad (\mathbf{F}_i'', \mathbf{A}_l) = \mathcal{G}_l(\mathbf{F}_l, \mathbf{F}_i)$$

融合后的特征 $\hat{\mathbf{F}}_i$ 再通过存储的注意力矩阵 $\mathbf{A}_e$、$\mathbf{A}_l$ 反向注入回事件和光照分支：

$$\hat{\mathbf{F}}_l = \mathcal{I}_l(\hat{\mathbf{F}}_i, \mathbf{A}_l) + \mathbf{F}_l, \quad \hat{\mathbf{F}}_e = \mathcal{I}_e(\hat{\mathbf{F}}_i, \mathbf{A}_e) + \mathbf{F}_e$$

这一设计的深层机理在于：注意力矩阵的复用构成了隐式的跨模态对齐约束，迫使事件和光照特征在共享的潜在空间中学习互补表示。**Figure 3(b)** 的t-SNE可视化证实，引入注意力复用后，不同模态的特征在嵌入空间中呈现出更紧凑的聚类分离，而直接交叉注意力（**Figure 3(a)**）则导致模态混淆。消融实验（**Table 6**）量化了这一设计的收益：相较于直接交叉注意力基线，反向注入设计带来超过 **2.58 dB** 的PSNR提升。

**调节变量二：光照感知的动态事件滤波器（IAEF）。** 传统事件去噪方法将滤波视为与场景内容无关的信号处理步骤。IAEF的关键创新在于将光照统计特征作为滤波参数生成的条件信号——从光照特征 $\mathbf{F}_l$ 中提取一维分离滤波核 $\mathbf{K}_v, \mathbf{K}_h$，从事件特征 $\mathbf{F}_e$ 中提取逐像素权重 $\mathbf{W}$ 和空间偏移 $\mathbf{P}_x, \mathbf{P}_y$：

$$\hat{\mathbf{F}}_e(m,n) = \sum \mathbf{W}(m,n) \cdot \mathbf{K}(m,n) \cdot \mathcal{S}(\mathbf{F}_e, (m+\mathbf{P}_x(m,n), n+\mathbf{P}_y(m,n)))$$

这一设计的因果逻辑是：光照分布决定了场景不同区域的噪声特性——暗区的事件噪声以随机尖峰为主，需要强平滑；亮区的事件信号相对可靠，需要保留细节。IAEF通过光照特征动态调整滤波核的强度和采样位置，实现了空间自适应的噪声抑制。**Table 5** 显示，相较于无事件滤波的基线，IAEF带来 **2.71 dB** 的PSNR提升；**Figure 3(d)** 的特征可视化进一步证实，Post-IAEF事件特征的噪声水平显著低于Pre-IAEF。

### 3. 在知识库中的位置与适用边界

**相对于事件-图像融合方法（以EvLight为代表）。** EIC-LIE将融合范式从“质量评估驱动的选择性融合”推进到“先验引导的双向协同交互”。关键差异在于：EvLight的SNR融合是单向的、局部的、基于信号质量的；EICI的前向收集-反向注入是双向的、全局的、基于语义对齐的。这一差异在低光极限场景下尤为显著——当事件SNR普遍偏低时，EvLight的选择性融合退化为几乎完全依赖图像特征，而EICI的光照先验仍能提供有效的全局约束。

**相对于纯图像Retinex方法（以MambaLLIE为代表）。** EIC-LIE在Retinex框架中引入了事件流作为额外的HDR信息源。传统Retinex方法依赖单张低光图像估计光照分量，在极暗区域面临严重的不适定性；事件流提供的边缘变化信息为光照估计和反射恢复提供了物理约束。

**相对于事件-视频增强方法（以EvLowlight为代表）。** EIC-LIE面向单帧图像增强，不依赖时序冗余，计算效率更高（**Table 3** 显示在1024×768分辨率下平均推理时间显著优于EvLowlight）。

**适用边界与局限。** 基于现有证据，EIC-LIE的适用边界需注意以下几点：（1）方法依赖事件相机与RGB相机的硬件同步与空间对齐，在非共轴系统或标定精度不足的场景下性能可能退化；（2）IAEF的滤波核从光照特征中学习，当光照估计本身存在较大误差时（如极端非均匀光照），滤波效果可能受限；（3）RLE数据集虽然提供了高分辨率真实世界基准，但其采集系统的双分光镜设计（**Figure 4**）引入了特定的光学特性，模型在其他硬件配置下的泛化性需要进一步验证——这一点需要手动核实，论文未提供跨硬件设置的鲁棒性分析。

### 4. 开放问题

1. **事件噪声建模的理论基础。** IAEF将光照特征作为去噪条件信号，这一设计的有效性已通过实验验证，但其理论基础——光照统计量与事件噪声分布之间的数学关系——尚未被严格建模。事件噪声在低光下的物理生成机制（暗电流、热噪声、阈值色散）与光照条件的定量关系值得深入分析。

2. **双向交互的收敛性与最优性。** EICI的前向收集-反向注入构成了一个隐式的迭代优化过程，但该过程的收敛性、最优性条件以及注意力复用带来的信息瓶颈效应尚未被讨论。

3. **动态场景下的光照先验稳定性。** 光照先验从低光图像的通道最大值中提取，在动态光照变化场景下（如移动光源、闪烁），单帧光照估计可能失效。事件流本身包含光照变化信息，如何利用事件流辅助光照先验的动态更新是一个开放方向。

4. **与最新基础模型的整合潜力。** 论文未讨论EIC-LIE与视觉基础模型（如扩散模型、视觉Transformer预训练模型）的整合可能性。事件-光照协同交互的框架是否可以作为即插即用的模块嵌入更大规模的增强系统中，值得探索。

## 原文 PDF

![[paperPDFs/CVPR_2026/Event_Illumination_Collaborative_Low_light_Image_Enhancement_with_a_High_resolution_Real_world_Dataset.pdf]]
