---
title: "SynCamMaster: Synchronizing Multi-Camera Video Generation from Diverse Viewpoints"
type: paper
paper_level: A
venue: ICLR
year: 2025
pdf_ref: paperPDFs/ICLR_2025/SynCamMaster_Synchronizing_Multi_Camera_Video_Generation_from_Diverse_Viewpoints.pdf
code_link: null
project_link: https://jianhongbai.github.io/SynCamMaster/
aliases:
- SynCamMaster
tags:
- ICLR_2025
- topic/multi_camera_video_generation
- topic/cross_view_synchronization
- topic/video_diffusion
- topic/multi_camera_video_generation/general
core_operator: "在预训练文本到视频扩散模型的基础上，引入即插即用的多视角同步模块（跨视图自注意力），通过相机外参嵌入引导多视图特征交互，实现几何与外观的同步。"
primary_logic: "利用预训练视频扩散模型已具备的3D一致性生成能力，通过在DiT各Transformer块中插入轻量的可学习跨视图同步模块，并采用混合数据训练策略（多视角图像、UE渲染多视角视频、静态单视角视频），即可高效地赋予模型开放域下的多摄像机同步视频生成能力。"
claims:
- "所提出的即插即用多视角同步模块能够保持跨视点的外观与几何一致性。"
- "混合训练方案（多视角图像、UE渲染多视角视频、单视角视频）显著提升了模型的泛化能力和视觉质量。"
- "SynCamMaster在视图同步指标上大幅优于基线方法：Mat. Pix. 527.1K，FVD-V 1470，CLIP-V 93.71。"
- "多视图同步评估 上 Mat. Pix.(K)↑ = 527.1"
---

# SynCamMaster: Synchronizing Multi-Camera Video Generation from Diverse Viewpoints

> [!tip] 核心洞察
> 利用预训练视频扩散模型已具备的3D一致性生成能力，通过在DiT各Transformer块中插入轻量的可学习跨视图同步模块，并采用混合数据训练策略（多视角图像、UE渲染多视角视频、静态单视角视频），即可高效地赋予模型开放域下的多摄像机同步视频生成能力。

| 字段 | 内容 |
|------|------|
| 中文题名 | SynCamMaster：从多样视点同步多摄像机视频生成 |
| 英文题名 | SynCamMaster: Synchronizing Multi-Camera Video Generation from Diverse Viewpoints |
| 会议/期刊 | ICLR 2025 |
| Links | [paper](https://arxiv.org/abs/2412.07760) · [Project](https://jianhongbai.github.io/SynCamMaster/) |
| Topic | #topic/multi_camera_video_generation #topic/cross_view_synchronization #topic/video_diffusion #topic/multi_camera_video_generation/general |
| Method | Plug-in multi-view synchronization module, cross-view self-attention, camera extrinsic embedding, mixed-data training |
| Dataset | UE-rendered multi-camera videos, DL3DV-10K multi-view images, static single-view videos |

> [!tip] 效果简介
> - 多视图同步评估 上，Mat. Pix.(K)↑ 为 527.1，对比 150.4 (M.V. Image + SVD-XT)，变化 +376.7。
> - 多视图同步评估 上，FVD-V↓ 为 1470，对比 1930 (M.V. Image + I2V-Ours)，变化 -460。
> - 多视图同步评估 上，CLIP-V↑ 为 93.71，对比 89.14 (M.V. Image + SVD-XT)，变化 +4.57。

## 概要

从任意视点同步生成同一动态场景的多段视频，是视频生成领域尚未被充分探索的难题。其核心瓶颈在于：**如何在开放域场景中，使不同视点下的动态内容在几何与外观上保持4D一致性**，而现有方法要么局限于单视图生成，要么仅能控制单一相机的运动轨迹，缺乏对多摄像机同步关系的显式建模。

针对这一挑战，本文提出 **SynCamMaster**——一个即插即用的多摄像机视频生成框架。其核心洞察在于：预训练文本到视频扩散模型（T2V）已经内化了一定的3D一致性生成能力，只需在模型的关键位置引入轻量的跨视图同步机制，即可高效地将这种能力扩展至多视点同步生成。具体而言，SynCamMaster 在基础 T2V 模型的每个 DiT Transformer 块中插入一个**多视角同步模块（Multi-View Synchronization Module, MVS）**，通过相机外参嵌入引导不同视图的空间特征进行跨视图自注意力交互，从而实现几何与外观的同步。整个基础模型保持冻结，仅需训练新增的同步模块与相机编码器。

为弥补真实多摄像机视频数据的稀缺，论文设计了一套**混合数据训练策略**：联合使用 Unreal Engine 渲染的 500 个场景的多摄像机视频、从 DL3DV-10K 等数据集中提取的多视角图像，以及经过筛选的静态单视角视频作为正则化。配合**渐进式训练策略**（从小视角差开始逐步增大），模型得以在开放域场景中展现出良好的泛化能力。

实验结果表明，SynCamMaster 在多视图同步指标上显著优于现有基线方法：在匹配像素数（Mat. Pix.）上达到 527.1K，较最佳基线提升 376.7K；视频级 FVD 降至 1470，CLIP 视图一致性得分达到 93.71。同时，在相机控制精度上，旋转误差仅为 0.12，优于 CameraCtrl 等相机控制方法。定性结果进一步验证了模型在跨视点内容一致性与同步质量上的优势。

在方法谱系上，SynCamMaster 属于**预训练视频扩散模型的参数高效微调范式**，其跨视图注意力机制与多视图立体视觉中的特征匹配思想一脉相承，但创新性地将其嵌入生成模型的去噪过程中，从而实现了从“重建”到“生成”的跨越。



### 问题定义：多摄像机同步视频生成

给定一段开放域文本描述 $P_t$ 和一组 $n$ 个指定的摄像机视点 $\{\mathsf{cam}^1, \dots, \mathsf{cam}^n\}$，其中每个视点由外参矩阵 $\mathsf{cam}_i := [R, t] \in \mathbb{R}^{3 \times 4}$ 表示，目标是生成 $n$ 个同步视频——这些视频从不同视点描绘同一动态场景，且必须在几何结构、外观纹理和运动时序上保持跨视点一致性。

这一任务的核心挑战在于：不同视点下的动态内容必须实现**4D一致性**（3D空间+时间），即从任意视点观察到的场景几何、物体运动轨迹和外观细节应当保持协调统一。然而，现有方法在这一目标上存在显著缺口。

### 现有方法的局限

当前视频生成方法主要沿两条技术路线发展，但均无法有效解决多摄像机同步生成问题：

- **单视图视频生成模型**（如基于DiT架构的文本到视频扩散模型）已经展现出强大的3D一致性生成能力，能够在单视点下生成合理的动态场景。然而，这些模型缺乏多视图同步机制，无法保证跨视点的一致性。
- **相机可控视频生成方法**（如**CameraCtrl**，He et al., 2024）允许用户通过指定相机轨迹来控制单个视频的视点变化，但其本质仍是单视图生成，无法同时输出多个同步视点的视频。

在数据层面，瓶颈同样突出：**缺少足够的多视角视频训练数据**。真实世界中获取大规模、高质量的多摄像机同步视频极为困难，这直接制约了监督学习方法的可行性。

### 本文动机与核心假设

SynCamMaster的提出基于一个关键洞察：**预训练视频扩散模型已经内隐地具备了一定的3D一致性生成能力**——它能够生成符合物理规律的动态场景，只是缺乏将这种一致性显式地协调到多个视点的机制。

因此，本文的核心假设是：通过在预训练文本到视频扩散模型的DiT Transformer块中，插入**轻量的、可学习的多视图同步模块**（即插即用），并辅以**混合数据训练策略**（联合利用UE渲染的多视角视频、从单视角视频中提取的多视角图像、以及静态单视角视频作为正则化），即可高效地将单视图生成模型转化为开放域下的多摄像机同步视频生成模型，而无需从头训练或依赖昂贵的多视角视频数据采集。



## 核心方法与创新机理

SynCamMaster的核心创新在于，它并非从零训练一个多摄像机视频生成模型，而是将预训练的单视图文本到视频（T2V）扩散模型作为“3D一致性先验”，通过两个即插即用的轻量级组件，赋予其开放域下的多视点同步生成能力。其关键创新点可归纳为一个核心机制、一个混合数据策略，以及一个渐进式训练方案。

### 1. 即插即用的多视角同步模块

这是实现跨视点一致性的核心因果开关。SynCamMaster冻结了预训练T2V模型（基于DiT架构）的全部权重，仅在其每个Transformer块中插入一个可学习的**多视角同步模块（Multi-View Synchronization Module, MVS）**。

该模块的工作流程如下：
- **相机外参嵌入**：每个视点的相机外参 $\mathsf{cam}^i = [R, t] \in \mathbb{R}^{3 \times 4}$ 经过归一化后，由一个**相机编码器**映射为与空间特征同维度的嵌入向量，并与该视点的空间特征 $\mathbf{F}_i^s$ 相加，得到相机感知的特征 $\mathbf{F}_i^v = \mathbf{F}_i^s + \mathcal{E}_c(\mathsf{cam}^i)$（Eq. 5）。
- **跨视图特征聚合**：将所有 $n$ 个视点的相机感知特征 $\mathbf{F}_1^v, \dots, \mathbf{F}_n^v$ 送入一个**跨视图自注意力层**。该层允许每个视点的特征在相机外参关系的引导下，自由地聚合来自其他视点的信息，从而显式地建模多视图之间的几何与外观关联。
- **残差投影**：聚合后的特征经过一个**投影层**，再通过残差连接加回原始特征：$\overline{\mathbf{F}}_i^v = \mathbf{F}_i^v + \operatorname{projector}(\operatorname{CrossViewAttn}(\mathbf{F}_1^v, \dots, \mathbf{F}_n^v)[i])$（Eq. 6）。

这一设计使得MVS模块成为一个即插即用的适配器，仅需少量参数即可在预训练模型的深层特征空间中建立多视图同步能力，而无需修改基础模型的任何权重。

### 2. 混合数据训练策略

多摄像机同步视频的训练数据极为稀缺。SynCamMaster设计了一套三步走的混合数据方案，以解决数据瓶颈：

- **UE渲染多摄像机视频**：在约500个UE场景中，围绕场景中心点（略高于地面）均匀放置摄像机，渲染同步的多视角视频。这提供了精确的几何对应关系，是模型学习视角跟随的基础。
- **从单视角视频中提取多视图图像**：利用带有相机运动的单视角视频（如DL3DV-10K），提取不同帧作为同一场景的多视图图像。这极大地扩展了训练场景的多样性，显著提升了模型在真实场景下的泛化能力。
- **静态单视角视频作为正则化**：引入高质量的通用单视角视频数据。这部分数据不提供多视图信号，但能有效防止模型因过度拟合渲染数据或图像数据而丧失视频的时序连续性和视觉质量。

训练时，三类数据以0.6:0.2:0.2的概率混合采样。消融实验证实，缺少多视图图像数据会导致在真实测试集上姿态跟随和同步能力严重退化（Mat. Pix. 从533.0降至460.5，FVD-V从1482升至1668）；而缺少单视角视频正则化则会损害视觉质量。

### 3. 渐进式训练策略

随机采样不同视角进行训练会导致模型在面对大视角差异时视角跟随能力显著退化。SynCamMaster采用**渐进式训练**：训练初期仅向模型提供视角差异较小的视图对，使其先学习局部几何对应关系；随后逐步增大视角差异，最终使其具备处理大角度视点变化的能力。这一策略对于模型最终实现鲁棒的多视角同步至关重要。



SynCamMaster 以冻结的预训练文本到视频（T2V）扩散模型为骨架，在其基础上插入两个轻量的可学习组件，从而赋予模型开放域下的多摄像机同步视频生成能力。整体架构如 Figure 2 所示。

![[assets/figures/papers/paper_list_l1495_https_arxiv_org_abs_2412_07760/figures/002_Figure_2.jpg]]
*Figure 2: Overview of SynCamMaster. Based on a pre-trained text-to-video model, two components are newly introduced: the camera encoder projects the normalized camera extrinsic parameters into embedding space; the multi-view synchronization module, as plugged in each Transformer block, modulates inter-view features under the guidance of inter-camera relationship. Only new components are trainable, while the pre-trained text-to-video model remains frozen*

### 输入与输出定义

给定一个文本提示 $P_t$ 和 $n$ 个指定的视点 $\{\mathsf{cam}^1, \dots, \mathsf{cam}^n\}$，模型的目标是生成 $n$ 段在时间上同步、且跨视点保持内容一致的视频。每个视点被表示为相机外参矩阵 $\mathsf{cam}_i := [R, t] \in \mathbb{R}^{3 \times 4}$，即旋转矩阵与平移向量的组合。

### 基础模型骨架

基础 T2V 模型（Figure 9）采用 Rectified Flow 框架，包含一个 3D VAE 编码器-解码器和一个 DiT（Diffusion Transformer）骨干网络。其前向过程沿直线路径将数据分布映射到标准正态分布：

$$z_t = (1 - t) z_0 + t \epsilon$$

去噪过程由条件流匹配损失（Conditional Flow Matching）训练：

$$\mathcal{L}_{LCM} = \mathbb{E}_{t, p_t(z, \epsilon), p(\epsilon)} \| v_{\Theta}(z_t, t) - u_t(z_0 | \epsilon) \|_2^2$$

推理时使用欧拉离散化从 $t=1$ 到 $0$ 迭代采样：

$$z_t = z_{t-1} + v_{\Theta}(z_{t-1}, t) \cdot \Delta t$$

### 新增模块及其插入位置

在 DiT 的每个 Transformer 块中，SynCamMaster 插入了两个新组件：

1. **相机编码器（Camera Encoder）**：将 12 维的归一化相机外参 $\mathsf{cam}^i$ 映射到与空间特征相同维度的嵌入向量，并通过加法注入到第 $i$ 个视图的空间特征 $\mathbf{F}_i^s$ 中：

   $$\mathbf{F}_i^v = \mathbf{F}_i^s + \mathcal{E}_c(\mathsf{cam}^i)$$

2. **多视角同步模块（Multi-View Synchronization Module, MVS）**：在相机嵌入的引导下，对 $n$ 个视点的特征执行跨视图自注意力（Cross-View Attention），实现多视角特征交互与聚合。聚合后的特征通过一个投影层（Projector）映射回空间特征域，并以残差方式与原始特征相加：

   $$\overline{\mathbf{F}}_i^v = \mathbf{F}_i^v + \operatorname{projector}(\operatorname{CrossViewAttn}(\mathbf{F}_1^v, \dots, \mathbf{F}_n^v)[i])$$

该模块以即插即用（plug-and-play）的方式工作——预训练 T2V 模型的所有参数保持冻结，仅训练相机编码器和 MVS 模块中的可学习参数。这种设计使得模型既能保留基础模型已有的 3D 一致性生成先验，又能高效地学习跨视点的几何与外观同步能力。

### 训练数据流与策略

为弥补多视角视频训练数据的稀缺，SynCamMaster 采用混合数据训练方案（Figure 3），联合使用三类数据源：

- **UE 渲染的多摄像机视频**：在 500 个场景中手动放置摄像机并渲染同步视频（Figure 4），作为主要的几何对应关系学习信号。
- **多视角图像**：从 DL3DV-10K 等带有相机运动信息的视频中提取多帧作为多视角图像数据，增强模型的泛化能力。
- **静态单视角视频**：筛选高质量的通用视频数据作为正则化，防止模型在时序连续性上退化。

训练时，三类数据以 0.6:0.2:0.2 的概率混合采样。此外，模型采用**渐进式训练策略**：从相对视角角度差异较小的视图开始训练，逐步增大角度差异，以稳定地学习大视角下的几何对应关系。



### 问题形式化

SynCamMaster的目标是构建一个开放域多摄像机视频生成模型，该模型接收一个文本提示 $P_t$ 和 $n$ 个指定的视点 $\{\mathsf{cam}^1, \dots, \mathsf{cam}^n\}$，同步生成 $n$ 段动态场景视频。每个视点由相机外参矩阵表示：

$$\mathsf{cam}_i := [\mathbf{R}, \mathbf{t}] \in \mathbb{R}^{3 \times 4}$$

其中 $\mathbf{R} \in \mathbb{R}^{3 \times 3}$ 为旋转矩阵，$\mathbf{t} \in \mathbb{R}^{3}$ 为平移向量。

### 基础生成框架：Rectified Flow

SynCamMaster构建在预训练的文本到视频扩散模型之上，该模型采用Rectified Flow作为生成框架。其核心公式如下：

**前向过程**定义从数据分布到标准正态分布的直线路径：

$$z_t = (1 - t) z_0 + t \epsilon \quad \text{(Eq. 1)}$$

其中 $z_0$ 为干净视频潜变量，$\epsilon \sim \mathcal{N}(0, I)$ 为标准高斯噪声，$t \in [0, 1]$。

**去噪常微分方程**将噪声分布映射回数据分布：

$$d z_t = v_{\Theta}(z_t, t) dt \quad \text{(Eq. 2)}$$

其中 $v_{\Theta}$ 为参数化的速度场预测网络。

**条件流匹配损失**用于训练速度场预测网络：

$$\mathcal{L}_{LCM} = \mathbb{E}_{t, p_t(z, \epsilon), p(\epsilon)} \| v_{\Theta}(z_t, t) - u_t(z_0 | \epsilon) \|_2^2 \quad \text{(Eq. 3)}$$

其中 $u_t(z_0 | \epsilon) = \epsilon - z_0$ 为真实速度场。

**推理采样**采用欧拉离散化，从 $t=1$ 迭代至 $t=0$：

$$z_t = z_{t-1} + v_{\Theta}(z_{t-1}, t) \cdot \Delta t \quad \text{(Eq. 4)}$$

### 核心模块一：相机编码器

相机编码器 $\mathcal{E}_c$ 负责将12维的相机外参嵌入到与空间特征相同的维度空间。对于第 $i$ 个视图，相机嵌入直接与空间特征相加：

$$\mathbf{F}_i^v = \mathbf{F}_i^s + \mathcal{E}_c(\mathsf{cam}^i) \quad \text{(Eq. 5)}$$

其中 $\mathbf{F}_i^s$ 为第 $i$ 个视图在DiT某Transformer块中的空间特征，$\mathbf{F}_i^v$ 为注入相机信息后的特征。这种加法操作使得相机位姿信息直接渗透到特征表示中，为后续的跨视图交互提供几何先验。

### 核心模块二：多视角同步模块

多视角同步模块（Multi-View Synchronization Module, MVS）是SynCamMaster实现跨视图一致性的关键组件。该模块被插入到DiT模型的每一个基础Transformer块中，对来自 $n$ 个视点的特征进行全局交互：

$$\overline{\mathbf{F}}_i^v = \mathbf{F}_i^v + \operatorname{projector}\big(\operatorname{CrossViewAttn}(\mathbf{F}_1^v, \dots, \mathbf{F}_n^v)[i]\big) \quad \text{(Eq. 6)}$$

具体而言，$\operatorname{CrossViewAttn}$ 对 $n$ 个视图的注入相机信息后的特征执行跨视图自注意力操作，使每个视图的特征能够聚合来自其他视图的几何与外观信息。聚合后的特征经投影层 $\operatorname{projector}$ 映射回原始特征空间，再通过残差连接与原始特征 $\mathbf{F}_i^v$ 相加，得到视图一致的特征 $\overline{\mathbf{F}}_i^v$。该残差设计确保了模块的即插即用特性——在训练初期，投影层输出接近零，模型行为近似于冻结的预训练模型。

### 新视图合成扩展

对于新视图合成任务（给定一个参考视图视频，生成其他视点的视频），SynCamMaster引入加权分类器自由引导策略，分别控制视频条件 $c_V$（参考视图）和文本条件 $c_T$ 的引导强度：

$$\hat{v_{\Theta}}(z_t, c_V, c_T) = v_{\Theta}(z_t, \emptyset, \emptyset) + s_V \cdot (v_{\Theta}(z_t, c_V, \emptyset) - v_{\Theta}(z_t, \emptyset, \emptyset)) + s_T \cdot (v_{\Theta}(z_t, c_V, c_T) - v_{\Theta}(z_t, c_V, \emptyset)) \quad \text{(Eq. 7)}$$

其中 $s_V$ 和 $s_T$ 分别为视频条件和文本条件的引导尺度。这种解耦的引导方式允许独立调节参考视图对齐和文本语义一致性的强度。

### 模块设计的关键约束

多视角同步模块中的注意力机制选择对性能有显著影响。消融实验（Table 6）表明，全注意力（Full Attention）相比极线注意力（Epipolar Attention）具有更好的文本语义一致性，尽管二者的旋转误差相近（RotErr 0.12 vs 0.10）。全注意力允许所有视图间自由交互，避免了极线约束可能引入的过度几何限制，在开放域场景中更具鲁棒性。



## 实验与关键发现

### 主结果与基线对比

SynCamMaster 在多视角同步视频生成的核心指标上全面优于现有基线方法。由于基线方法（如 SVD-XT、CameraCtrl、I2V-Ours）本身不支持多摄像机视频生成，评估时统一使用 SynCamMaster 生成的多视图图像作为首帧输入，确保了比较的可行性。

**Table 1** 汇总了主要定量结果。在视图同步指标上，SynCamMaster 的匹配像素数（Mat. Pix.）达到 527.1K，显著高于多视图图像+SVD-XT 的 150.4K（+376.7K）；视频级 FVD-V 降至 1470，优于多视图图像+I2V-Ours 的 1930（-460）；跨视图 CLIP 相似度（CLIP-V）达到 93.71，较 SVD-XT 的 89.14 提升 4.57 个百分点。在相机控制精度方面（**Table 4**），SynCamMaster 的旋转误差（RotErr）仅为 0.12，低于多视图图像+CameraCtrl 的 0.16。这些结果表明，SynCamMaster 不仅在跨视点的外观和几何一致性上表现突出，而且对指定相机外参的跟随精度也更高。

定性对比（**Figure 5**）进一步验证了上述结论：SynCamMaster 生成的多个视点视频在动态细节（如人物动作、物体纹理）上保持高度一致，而基线方法在视点切换时容易出现内容漂移或几何错位。

### 消融实验

#### 混合训练数据策略

**Table 2** 和 **Figure 6** 系统消融了三种训练数据来源的贡献。仅使用 UE 渲染的多视角视频训练时，模型在真实测试集上的姿态跟随和同步能力严重退化（Mat. Pix. 460.5K，FVD-V 1668）。加入从 DL3DV-10K 等视频中提取的多视角图像数据后，泛化能力显著提升，Mat. Pix. 跃升至 533.0K，FVD-V 降至 1482。进一步引入静态单视角视频作为正则化（+Both），FVD 进一步降至 1401，视觉质量达到最优（FID 116.7，CLIP-F 99.36）。这说明多视角图像数据主要解决几何一致性泛化问题，而单视角视频数据则有助于保持时序连续性和视觉保真度。

值得注意的是，混合比例存在权衡：多视角图像比例过高会破坏视频的时序连续性，而单视角视频比例过高则会使模型偏向小角度视角合成。

#### 渐进式训练策略

渐进式训练策略对于大视角差异下的视角跟随能力至关重要。**Figure 7** 的消融显示，若从一开始就随机采样大角度差异的视点对进行训练，模型在视角跟随上会出现显著性能退化。这是因为模型需要先学习小角度下的几何对应关系，再逐步泛化到大角度场景。

#### 注意力机制选择

**Table 6** 和 **Figure 11** 对比了全注意力（Full Attention）与极线注意力（Epipolar Attention）在多视角同步模块中的效果。全注意力的旋转误差为 0.12，略高于极线注意力的 0.10，但全注意力在文本语义一致性上表现更好。论文选择全注意力作为默认配置，以兼顾相机控制精度和语义对齐质量。

### 新视角视频合成扩展

SynCamMaster 可扩展至新视角视频合成任务。给定单视角视频和相机轨迹，模型能够生成高质量的新视角视频。**Table 3** 报告了该扩展的定量结果，**Figure 8** 展示了不同引导权重下的合成效果。在推理时，采用加权 Classifier-Free Guidance 策略（式 7），通过独立调节视频条件引导强度 $s_V$ 和文本条件引导强度 $s_T$ 来控制生成质量与条件跟随的平衡。

![[assets/figures/papers/paper_list_l1495_https_arxiv_org_abs_2412_07760/figures/011_Figure_8.jpg]]
*Figure 8: Results of the extension on novel view video synthesis*

![[assets/figures/papers/paper_list_l1495_https_arxiv_org_abs_2412_07760/figures/010_Table_3.jpg]]
*Table 3: Results of novel view video synthesis*

### VBench 通用视频质量评估

在 VBench 基准（Huang et al., 2024）上，**Table 7** 对比了 SynCamMaster 与基线方法的通用视频质量指标。结果表明，SynCamMaster 在多视角同步能力大幅提升的同时，并未牺牲单视角视频的生成质量，各项指标与基线方法保持可比甚至更优。

![[assets/figures/papers/paper_list_l1495_https_arxiv_org_abs_2412_07760/figures/018_Table_7.jpg]]
*Table 7: Quantitative comparison with baseline methods on VBench (Huang et al., 2024). Please refer to Fig. 12 for qualitative comparison with the state-of-the-art methods*

### 失败模式与局限性

**Figure 15** 可视化了典型失败案例，主要包含三类问题：

1. **跨视点细节不一致**：在复杂场景中，不同视点下的局部细节可能出现差异（例如碗和盘子的内容在不同视角下不一致），说明多视角同步模块在处理细粒度纹理对齐时仍有不足。
2. **手部运动质量较低**：该问题继承自基础文本到视频生成模型，在需要精细手部动作的场景中表现不佳。
3. **数据混合的敏感权衡**：如消融实验所示，多视角图像与单视角视频的混合比例对时序连续性和视角合成范围有直接影响，当前 0.6:0.2:0.2 的配比是经验性选择，尚未探索最优比例的理论依据。

### 补充图表

![[assets/figures/papers/paper_list_l1495_https_arxiv_org_abs_2412_07760/figures/020_Figure.jpg]]
*Figure: A train is traveling on the tracks,moving slowly through the countryside. A close-up view of a turtle slowly crawling across a sandy beach*

![[assets/figures/papers/paper_list_l1495_https_arxiv_org_abs_2412_07760/figures/021_Figure_14.jpg]]
*Figure 14: A tractor is plowing ina field,the tractoris moving slowly and steadily,leaving a trail offreshly plowed soil behind it. Figure 14: More synthesized results of SynCamMaster*

![[assets/figures/papers/paper_list_l1495_https_arxiv_org_abs_2412_07760/figures/006_Table_1.jpg]]
*Table 1: Quantitative comparison with state-of-the-art methods*

![[assets/figures/papers/paper_list_l1495_https_arxiv_org_abs_2412_07760/figures/007_Table_2.jpg]]
*Table 2: Quantitative ablation on the joint training strategy*

![[assets/figures/papers/paper_list_l1495_https_arxiv_org_abs_2412_07760/figures/009_Table_4.jpg]]
*Table 4: Accuracy of camera control*

![[assets/figures/papers/paper_list_l1495_https_arxiv_org_abs_2412_07760/figures/015_Table_5.jpg]]
*Table 5: Accuracy of camera control with different camera representations*

![[assets/figures/papers/paper_list_l1495_https_arxiv_org_abs_2412_07760/figures/017_Table_6.jpg]]
*Table 6: Accuracy of camera control with epipolar attention and full attention*

![[assets/figures/papers/paper_list_l1495_https_arxiv_org_abs_2412_07760/figures/016_Figure_11.jpg]]
*Figure 11: Performance comparison of SynCamMaster with epipolar attention and full attention*



## 定位与知识库关联

### 技术谱系与基线关系

SynCamMaster 建立在预训练文本到视频（T2V）扩散模型之上，其核心创新在于将单视图视频生成能力扩展至多摄像机同步生成。该方法在技术谱系上处于**相机可控视频生成**与**多视图一致性生成**的交汇点。

**与相机控制方法的区别**：现有的相机可控视频生成方法（如 **CameraCtrl**，He et al., 2024）主要关注单视图内的相机轨迹跟随，通过注入相机参数来控制生成视频的视角运动。SynCamMaster 与之有本质不同——其目标是同时生成多个不同视点下的同步视频，要求跨视图的外观与几何一致性，而非单视图内的相机运动。实验表明，将 CameraCtrl 直接用于多视图场景时，其旋转误差（RotErr）为 0.16，而 SynCamMaster 降至 0.12（Table 4），且前者无法保证跨视图的内容同步。

**与图像到视频（I2V）方法的区别**：基线 **SVD-XT** 和作者自训练的 **I2V-Ours** 均为图像到视频生成方法，以首帧图像为条件生成后续帧。在多摄像机场景下，这些方法需以 SynCamMaster 生成的多视图图像作为首帧输入才能运行（否则基线本身不支持多摄像机视频生成）。即便如此，I2V 方法无法在生成过程中协调不同视图的动态演化，导致视图同步指标显著劣化：SVD-XT 的 Mat. Pix. 仅为 150.4K，I2V-Ours 的 FVD-V 高达 1930，而 SynCamMaster 分别达到 527.1K 和 1470（Table 1）。

**与多视图图像生成方法的区别**：多视图图像生成方法（如基于 3D 先验的 NeRF 或 3DGS 方法）仅处理静态场景的空间一致性。SynCamMaster 将一致性约束从静态图像扩展至动态视频，需要同时维护空间几何一致性和时序运动一致性，这是一个更复杂的 4D 同步问题。

### 方法适用边界

**适用场景**：
- 开放域文本描述下的多摄像机同步视频生成，支持任意指定的多个视点（以相机外参 $[R, t] \in \mathbb{R}^{3 \times 4}$ 定义）。
- 新视图视频合成：给定一个参考视频及其相机轨迹，生成其他视点下的同步视频（通过 Eq. (7) 的加权 Classifier-Free Guidance 实现，$s_V$ 和 $s_T$ 分别控制视图条件和文本条件的引导强度）。
- 训练数据覆盖的视角范围：UE 渲染数据涵盖 500 个场景的多样化视点配置，多视图图像数据来自 DL3DV-10K 等真实场景。

**边界条件与退化风险**：
- **大视角差异下的退化**：消融实验明确显示，随机采样不同相机视角进行训练会导致大相对角度下的视角跟随能力显著退化（Figure 7）。渐进式训练策略（从小角度差异开始逐步增大）是缓解此问题的关键，但该策略的有效性边界（最大可处理视角差异）尚未量化界定。
- **数据混合比率的敏感性**：混合训练中三类数据的采样比率（多视角视频:多视图图像:单视角视频 = 0.6:0.2:0.2）对性能有显著影响。多视图图像比例过高会破坏视频的时序连续性，单视角视频比例过高则使模型偏向小角度视角合成。当前比率是经验性选择，缺乏系统性的比率扫描分析。
- **复杂场景的细节不一致**：在复杂场景中，跨视点的细节可能出现不一致（Figure 15 展示了碗和盘子内容的差异），表明 MVS 模块的跨视图特征聚合在细粒度几何对应上仍存在不足。
- **基础模型的继承缺陷**：手部运动等动态细节的生成质量受限于底层预训练 T2V 模型（如 Figure 15 所示），SynCamMaster 未对此进行针对性改进。

### 局限与开放问题

**已知局限**：
1. **细节跨视图不一致**：复杂场景中部分物体的细节在不同视点间存在差异，表明全注意力机制（相对于极线注意力）虽然提升了文本语义一致性，但在精确几何对应上仍有改进空间（Table 6：全注意力 RotErr 0.12 vs. 极线注意力 0.10）。
2. **手部运动质量**：继承自基础 T2V 模型的手部生成质量问题未得到解决。
3. **数据混合的平衡性**：当前混合策略缺乏对长期时序一致性与相机准确性之间权衡的精细分析。

**开放问题**：
1. **动态相机轨迹扩展**：当前方法假设多个摄像机固定在同一时刻的不同视点。能否将 MVS 模块扩展至动态变化的相机轨迹（即每个视点本身具有独立的运动路径），是一个重要的扩展方向。
2. **3D 先验的融合**：能否结合更强的显式 3D 先验（如 NeRF 或 3D Gaussian Splatting）来进一步提升跨视图几何一致性？当前方法完全依赖从数据中隐式学习的 3D 对应关系。
3. **细节不一致的根源分析**：复杂场景中的细节不一致是源于跨视图注意力的信息瓶颈，还是训练数据的覆盖不足，尚需更深入的诊断。
4. **数据混合比率的理论指导**：如何根据目标应用的视角分布特征，系统性地确定最优的数据混合比率，而非依赖经验性搜索。
5. **更长时序的一致性**：当前评估主要关注短时序（生成视频长度受限于基础模型），更长时间跨度下的跨视图同步稳定性尚未被检验。



## 原文 PDF

![[paperPDFs/ICLR_2025/SynCamMaster_Synchronizing_Multi_Camera_Video_Generation_from_Diverse_Viewpoints.pdf]]
