---
title: "ProgressiveAvatars: Progressive Animatable 3D Gaussian Avatars"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/ProgressiveAvatars_Progressive_Animatable_3D_Gaussian_Avatars.pdf
project_link: null
code_link: null
aliases:
- ProgressiveAvatars
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
core_operator: 基于屏幕空间梯度信号的隐式自适应细分驱动三角形面层次化生长，使增量加载和渲染成为可能。
primary_logic: 通过将3D高斯绑定到FLAME网格的局部三角面坐标系，并根据屏幕空间梯度自适应引导细分层次生长，该表示在所有细节级别保持可驱动性，支持渐进式传输并实现平滑质量提升。
claims:
- 方法基于自适应隐式细分构建高斯层次结构，支持增量加载与渐进渲染。
- 在推理时通过渐进式激活实现增量加载，先提供粗粒度可驱动化身，随着带宽增加平滑改进质量。
- 屏幕空间梯度自适应地仅在细节丰富区域进行细分，优化资源分配，相比均匀细分用更少高斯达到更高重建质量。
- 重要性排序按高斯对渲染图像的贡献调度传输，减少颜色漂移，提升有限带宽下的感知质量。
---

# ProgressiveAvatars: Progressive Animatable 3D Gaussian Avatars

> [!tip] 核心洞察
> 通过将3D高斯绑定到FLAME网格的局部三角面坐标系，并根据屏幕空间梯度自适应引导细分层次生长，该表示在所有细节级别保持可驱动性，支持渐进式传输并实现平滑质量提升。

| 字段 | 内容 |
|------|------|
| 中文题名 | ProgressiveAvatars: 渐进式可驱动3D高斯化身 |
| 英文题名 | ProgressiveAvatars: Progressive Animatable 3D Gaussian Avatars |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2603.16447) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction |
| Method | ProgressiveAvatars |
| Dataset | NeRSemble, NeRSemble (NVS) at 5% base budget, NeRSemble (NVS) full model vs SOTA, Storage size |

> [!tip] 效果简介
> - NeRSemble (NVS) 上，PSNR↑ / SSIM↑ / LPIPS↓ 31.47 / 0.929 / 0.068 vs 31.10 / 0.937 / 0.064 (GaussianAvatars) (+0.37 / -0.008 / +0.004)。
> - NeRSemble (NES) 上，PSNR↑ / SSIM↑ / LPIPS↓ 25.89 / 0.908 / 0.080 vs 25.80 / 0.911 / 0.076 (GaussianAvatars) (+0.09 / -0.003 / +0.004)。
> - NeRSemble (NVS) at 5% base budget 上，PSNR↑ / SSIM↑ / LPIPS↓ 27.89 / 0.851 / 0.186 vs N/A（GaussianAvatars需完整模型） (我们的方法在5%预算下即可获得可用化身)。

## 概要

**问题瓶颈**：现有基于3D高斯泼溅（3DGS）的可驱动化身方法（如**GaussianAvatars**，Qian et al., CVPR 2024）要求完整下载模型后才能开始渲染，导致高启动延迟和带宽突发，无法适应动态变化的网络与计算资源。同时，传统多细节层次（LoD）方案需要存储多个离散副本，造成显著的存储冗余。

**核心思路**：ProgressiveAvatars提出一种基于自适应隐式细分的渐进式可驱动3D高斯化身表示。其关键洞察是将3D高斯绑定到FLAME网格的局部三角面坐标系，利用屏幕空间梯度信号自适应引导三角形面的层次化生长，从而构建一个连续的多级细节结构。该结构天然支持增量加载和渐进渲染——接收端按重要性顺序逐步激活高斯，实现从粗糙到精细的平滑质量提升，且在所有细节级别均保持可驱动性。

**方法定位**：ProgressiveAvatars将3DGS的自适应密度控制与层次化三角面森林耦合，将离散冗余的LoD切换范式转变为单一连续可流式传输的资产。训练时采用多级联合监督和由粗到精的深度上限递增策略，确保跨级一致性；推理时通过预计算的面重要性评分指导传输调度，使有限带宽下的早期部分渲染尽可能接近完整模型色彩。

**主要结果**：在NeRSemble数据集上，ProgressiveAvatars完整模型的新视角合成（NVS）PSNR达到31.47 dB，略优于GaussianAvatars的31.10 dB，同时仅需5%的传输预算即可获得可用的可驱动化身（27.89 dB）。相比存储10个离散LoD层级的压缩方案，其存储需求仅为43.4 MB，减少约80.9%。消融实验证实，多级监督在35%预算下提升NVS PSNR达9.81 dB，重要性排序在25%预算下较随机排序提升0.74 dB。



### 3D化身流式传输的现实需求

数字化身是沉浸式通信、虚拟社交和远程呈现的核心媒介。随着网络基础设施的演进，用户期望化身能够在不同带宽和计算条件下即时可用，而非等待完整模型下载后才能交互。然而，现有高保真可驱动化身方法普遍采用“全量下载—整体渲染”的范式，这带来了两个关键矛盾：**启动延迟与带宽突发**——接收端必须获取全部模型资产才能生成第一帧；**资源刚性**——模型质量在传输完成前不可用，无法根据可用带宽动态调整。

这一矛盾在3D高斯泼溅（3D Gaussian Splatting, 3DGS）化身中尤为突出。以 **GaussianAvatars**（Qian et al., CVPR 2024）为代表的SOTA方法将3D高斯绑定到FLAME网格的三角面上，实现了高质量的新视角合成（NVS）和新表情合成（NES），但其表示是单层的、非层次化的——所有高斯在训练完成后构成一个不可分割的整体，缺乏渐进式流式传输所必需的层次结构和增量激活机制。图1（预告图）直观地展示了这一差距：GaussianAvatars在传输接近完成前几乎无法产生可用渲染，而本文方法在极低传输预算下即可获得可辨识的化身。

### 现有层次化与渐进式方法的局限

针对3D资产的渐进式传输并非全新概念，但将其应用于可驱动化身面临独特挑战。传统网格LOD（Level-of-Detail）方案依赖多个离散的细节层次副本，带来显著的存储冗余。在3DGS领域，**LightGaussian**（Fan et al., NeurIPS 2024）等方法通过剪枝和压缩减小模型体积，但未构建层次结构，不支持增量加载。**LoDAvatar**等尝试采用均匀细分构建层次，但均匀细分无法区分面部不同区域的细节需求——例如胡须、眼睛周围需要高密度高斯，而脸颊等平滑区域仅需少量高斯即可充分表达——导致高斯资源分配低效，在同等传输预算下重建质量受限。

更根本的困难在于**可驱动性的保持**。一个可用的渐进式化身要求在任何传输阶段、任何细节级别上，已加载的高斯都能正确响应表情和姿态变化。这需要表示本身在所有层次上内建可驱动性，而非将驱动作为后处理步骤。

### 核心动机与设计思路

本文的核心洞察是：**通过将3D高斯绑定到FLAME网格的局部三角面坐标系，并根据屏幕空间梯度自适应引导细分层次生长，该表示在所有细节级别保持可驱动性，支持渐进式传输并实现平滑质量提升。**

具体而言，ProgressiveAvatars的设计围绕以下动机展开：

1. **自适应隐式细分替代均匀层次**：利用训练过程中的屏幕空间梯度信号，仅在细节丰富区域触发三角面细分，构建一棵非均匀的三角面森林。这使高斯资源向高频区域集中，在同等高斯数量下获得更高重建质量，同时保证全局基础覆盖以支持低预算下的平滑渐进渲染（图6）。

2. **面局部坐标绑定保证跨级可驱动性**：每个3D高斯定义在其所属三角面的局部坐标系中（公式2），使其随FLAME网格的变形自动同步移动。这一设计确保从最粗粒度到最细粒度的所有层次都具有内在的可驱动性，无需为不同LOD维护独立的驱动参数。

3. **重要性排序驱动渐进传输**：基于高斯对渲染像素的聚合贡献（公式3），为每个三角面计算重要性分数，按降序传输。这使早期部分渲染与完整模型的像素颜色高度一致——因为主导贡献者优先到达，减少了颜色漂移（图3），在有限带宽下最大化感知质量。

4. **单资产连续流式替代离散LOD切换**：与存储多个独立LOD副本的传统方案不同，ProgressiveAvatars构建单一连续资产，由层次树和重要性排序支持流式传输。如图7(a)所示，该方法以43.4 MB的单一资产即可实现渐进式质量提升，而GaussianAvatars + LightGaussian的10级离散LOD方案需要227.2 MB存储（减少80.9%）。

综上，ProgressiveAvatars首次将渐进式流式传输能力引入3DGS可驱动化身，解决了现有方法“全量下载才能渲染”的根本瓶颈，为动态网络条件下的化身传输提供了实用框架。



## 核心方法与创新机理

ProgressiveAvatars 的核心创新在于将 3DGS 化身从“完整下载后渲染”的静态范式转变为**渐进式流式传输与连续细节累积**的动态范式。这一转变通过三个相互耦合的机制实现：

### 1. 基于屏幕空间梯度的自适应隐式细分

现有方法（如 **GaussianAvatars**，Qian et al., CVPR 2024）将 3D 高斯绑定到 FLAME 网格的三角面上，但缺乏层次化结构，必须传输完整模型后才能渲染。ProgressiveAvatars 的关键突破是将 **3DGS 自适应密度控制与层次树结构耦合**：训练过程中，每 k 次迭代检查各三角面绑定的高斯在屏幕空间上的梯度 $g_i$，对满足 $g_i > \varepsilon$ 的叶面执行隐式细分。新顶点通过重心坐标插值生成：

$$\mathbf{p} = \beta_1 \mathbf{v}_i + \beta_2 \mathbf{v}_j + \beta_3 \mathbf{v}_k$$

这一机制产生一个**多级三角面森林**，自动将细分资源集中于面部细节丰富区域（如胡须、眼睛），而平滑区域保持较粗粒度（Figure 6）。与均匀细分相比，自适应策略用更少的高斯达到更高重建质量，同时保证全局基础覆盖以实现平滑渐进渲染。

### 2. 面局部高斯绑定与全层级可驱动性

为使得层次结构中每一级都能随表情和头部运动变形，3D 高斯始终定义在三角面的局部坐标系中：

$$\mathbf{R} = \Delta\mathbf{R} \, \mathbf{r}, \quad \mathbf{S} = \Delta\mathbf{S} \, s, \quad \mu = s \, \mathbf{r} \, \Delta\mu + \mathbf{t}$$

这确保了从最粗到最细的所有细节级别都保持可驱动性——这是渐进式化身的关键前提，也是区别于简单多分辨率网格压缩的本质差异。

### 3. 重要性排序驱动的渐进式传输与渲染

推理时，方法预计算每个面的重要性分数，即其绑定高斯在所有像素上的聚合渲染贡献：

$$W_i = \sum_{j \in \mathcal{G}_i} \sum_{p} \alpha_{j,p} T_{j,p}$$

按重要性降序传输并逐步激活高斯。如 Figure 3 所示，优先传输高贡献高斯使得早期部分渲染的像素颜色与完整模型高度一致，避免颜色漂移；而低重要性优先传输则会导致部分权重重新归一化，放大弱贡献者，造成明显的颜色偏差。

### 4. 多级监督联合训练

与仅监督最精细层级的基线不同，ProgressiveAvatars 采用多级监督策略，对各层加权求和的 L1 与 SSIM 损失：

$$\mathcal{L}_{\mathrm{rgb}} = \sum_{\ell \in \mathcal{S}} w_\ell \big[ (1 - \lambda_s) \mathcal{L}_1 + \lambda_s \mathcal{L}_{\mathrm{ssim}} \big]$$

配合 coarse-to-fine 深度上限递增策略（初始化深度上限为 1，每 50k 迭代扩展并触发自适应细分），鼓励跨级一致性。消融实验（Table 3）表明，多级监督在 35% 传输预算下将 NVS PSNR 从 20.06 dB 提升至 29.87 dB，是全预算性能接近 SOTA 的关键。

### 5. 从离散 LOD 到单一连续流式资产

传统 LOD 方案需存储多个离散副本，存储开销线性增长（如 GaussianAvatars + LightGaussian 的 10 级离散 LOD 需 227.2 MB）。ProgressiveAvatars 将范式转变为**单一连续资产**（仅 43.4 MB），通过层次树和重要性排序支持流式传输，无需模型切换，存储效率提升 80.9%（Figure 7a）。



ProgressiveAvatars 的完整流水线如 Figure 2 所示，由六个核心模块串联构成：**FLAME 网格追踪 → 隐式细分与层次构建 → 面局部高斯绑定 → 多级自适应训练 → 重要性评分计算 → 渐进式传输与渲染**。输入为多视角头部视频，输出为可在不同带宽预算下即时渲染的可驱动 3D 高斯化身。

![[assets/figures/papers/paper_list_l18_https_arxiv_org_abs_2603_16447/figures/002_Figure_2.jpg]]
*Figure 2: Overview. We take head video as input then recover a tracked FLAME mesh sequence. We bind 3D Gaussians to the local coordinate frame of each FLAME face. During training, screen-space gradients of the Gaussians drive implicit subdivision of the template mesh across multiple levels, yielding a triangle face forest. At rendering time, we precompute per-face importance score and progressively transmit and render the corresponding Gaussians in decreasing order of importance*

**输入与预处理。** 系统以多视角头部视频为输入，对每一帧 $t$ 使用光度多视角追踪器拟合 FLAME 网格 $M_t = (\mathbf{V}_t, \mathbf{F})$，恢复姿态和表情参数。模板网格的拓扑 $\mathbf{F}$ 在所有帧间保持不变，为后续层次化表示提供统一的锚定结构。

**层次化表示构建。** 在模板拓扑上执行递归三角形细分，构建多级三角面层次 $\{\dot{\mathbf{F}}^{(\ell)}\}_{\ell=0}^{L}$，形成“三角面森林”。细分通过重心坐标插值在父三角形内创建新顶点 $\mathbf{p} = \beta_1 \mathbf{v}_i + \beta_2 \mathbf{v}_j + \beta_3 \mathbf{v}_k$，新顶点继承父面的局部参数化，使层次结构天然保持可驱动性。

**高斯绑定与局部参数化。** 每个 3D 高斯被绑定到对应三角面的局部坐标系中，其旋转 $\mathbf{R}$、尺度 $\mathbf{S}$ 和位置 $\mu$ 通过残差形式定义：

$$\mathbf{R} = \Delta\mathbf{R} \, \mathbf{r}, \quad \mathbf{S} = \Delta\mathbf{S} \, s, \quad \mu = s \, \mathbf{r} \, \Delta\mu + \mathbf{t}$$

其中 $\mathbf{r}$ 为面局部旋转矩阵，$s$ 为面尺度因子，$\mathbf{t}$ 为面中心平移量。这一参数化确保高斯随面部变形同步移动，在所有细节级别保持可驱动性。

**自适应训练。** 训练阶段将 3DGS 的自适应密度控制与层次树耦合：每隔 $k$ 次迭代，对屏幕空间梯度 $g_i > \varepsilon$ 的叶面执行隐式细分，使层次结构在训练中动态生长。同时采用 coarse-to-fine 深度上限递增策略——初始深度上限设为 1，每 50k 迭代增加上限并触发自适应细分——配合多级光度损失联合监督各层，鼓励跨级一致性。

**渐进式传输与渲染。** 训练完成后，预计算每个面的重要性分数 $W_i = \sum_{j \in \mathcal{G}_i} \sum_{p} \alpha_{j,p} T_{j,p}$，即该面绑定高斯在所有像素上的聚合渲染贡献。推理时按重要性降序逐步激活高斯：每次增量加载向已有内容添加更精细层级的高斯，已加载内容保持不变，渲染质量随数据到达平滑提升。这一“重要性优先”调度策略确保早期部分渲染与完整模型的像素颜色高度一致，有效减少颜色漂移。



ProgressiveAvatars 的核心设计围绕一个可渐进式传输与渲染的3D高斯化身表示展开。该方法通过将3D高斯绑定到FLAME网格的局部三角面坐标系，并基于屏幕空间梯度信号驱动自适应隐式细分，构建一个多级三角面森林层次结构。以下逐一剖析关键模块及其公式。

---

### 1. 自适应隐式细分与层次构建

传统3DGS化身方法（如 **GaussianAvatars**，Qian et al., CVPR 2024）在训练完成后生成单一分辨率的模型，不具备渐进式传输能力。ProgressiveAvatars 的核心创新在于将3DGS的自适应密度控制与层次化三角面树耦合，在训练过程中动态生长出多级结构。

**细分机制**：以FLAME模板网格的三角面为根节点，递归构建四叉树式层次。每个父三角面可细分为四个子三角面。细分点的位置通过重心坐标插值确定：

$$\mathbf{p} = \beta_1 \mathbf{v}_i + \beta_2 \mathbf{v}_j + \beta_3 \mathbf{v}_k$$

其中 $\mathbf{v}_i, \mathbf{v}_j, \mathbf{v}_k$ 为父三角面的三个顶点，$\beta_1, \beta_2, \beta_3$ 为可学习的重心坐标参数，满足 $\beta_1 + \beta_2 + \beta_3 = 1$。这些参数在训练过程中与高斯属性联合优化，使细分点能够自适应地调整位置以更好地拟合局部几何。

**自适应生长条件**：训练期间每隔 $k$ 次迭代，计算每个叶子三角面上绑定高斯的屏幕空间梯度 $g_i$。当 $g_i > \varepsilon$ 时触发细分，将该叶子面分裂为四个子面。这一机制将计算资源集中于细节丰富区域（如面部毛发、皱纹），而平滑区域（如脸颊）保持较低细分级别。消融实验（Figure 6）证实，相比均匀细分，自适应策略用更少的高斯数量达到了更高的重建质量。

**全局基础覆盖**：与仅对局部区域进行细分的策略不同，ProgressiveAvatars 的多级设计保证了所有区域在基础层级（Level 0）均有三角面覆盖。这确保了在渐进式传输的早期阶段（仅加载基础层时），化身即可呈现完整的全局结构，避免出现空洞或缺失区域。

---

### 2. 面局部高斯绑定与可驱动性

为保证化身在所有细节级别上均可驱动，每个3D高斯被定义在其所属三角面的局部坐标系中。当面随FLAME网格变形时，高斯自动跟随移动，无需逐帧重新计算全局位置。

**局部参数化**：对于绑定到三角面 $i$ 的高斯，其旋转 $\mathbf{R}$、尺度 $\mathbf{S}$ 和位置 $\mu$ 通过以下公式从面局部残差参数转换为世界空间：

$$\mathbf{R} = \Delta\mathbf{R} \, \mathbf{r}, \quad \mathbf{S} = \Delta\mathbf{S} \, s, \quad \mu = s \, \mathbf{r} \, \Delta\mu + \mathbf{t}$$

其中：
- $\mathbf{r}$ 为三角面的局部旋转矩阵，由面的三条边定义的局部坐标系确定；
- $\mathbf{t}$ 为三角面中心在世界空间的位置；
- $\Delta\mathbf{R}$、$\Delta\mathbf{S}$、$\Delta\mu$ 分别为旋转、尺度、位置的残差参数，在训练中优化；
- $s$ 为尺度因子。

这种参数化的关键优势在于：当FLAME网格因表情或头部姿态变化而变形时，仅需更新 $\mathbf{r}$ 和 $\mathbf{t}$（由网格顶点驱动），高斯的残差参数保持不变。因此，层次结构中所有级别的高斯均可同步驱动，实现了渐进式传输过程中的连续可动画性。

---

### 3. 重要性评分与渐进式传输调度

渐进式渲染的质量不仅取决于加载的高斯数量，还取决于加载顺序。ProgressiveAvatars 提出基于渲染贡献的重要性评分机制，确保有限带宽下最先传输对视觉质量贡献最大的高斯。

**重要性评分定义**：对于每个三角面 $i$，其重要性分数 $W_i$ 为其绑定的所有高斯在所有像素上的聚合渲染贡献：

$$W_i = \sum_{j \in \mathcal{G}_i} \sum_{p} \alpha_{j,p} T_{j,p}$$

其中 $\mathcal{G}_i$ 为绑定到面 $i$ 的高斯集合，$\alpha_{j,p}$ 为高斯 $j$ 在像素 $p$ 处的不透明度，$T_{j,p}$ 为该高斯在像素 $p$ 处的累积透射率。该分数在训练完成后预计算，作为传输调度的依据。

**降序传输的效果**：Figure 3 的实验表明，按重要性降序传输时，早期部分渲染的像素颜色与完整模型高度一致，因为主导贡献者优先到达。相反，若先传输低重要性高斯，部分渲染的权重重新归一化会放大弱贡献者，导致明显的颜色漂移。消融实验（Table 3）进一步量化了这一效果：重要性排序（W/ Ranking）在25%传输预算下，NVS PSNR比随机排序（W/ Random）高0.74 dB（29.14 vs 28.40）。

---

### 4. 多级监督与训练策略

为鼓励跨级一致性并确保各细节级别的高斯均能独立产生合理的渲染结果，ProgressiveAvatars 采用多级监督联合训练策略。

**多级光度损失**：在训练时，同时监督多个细节级别的渲染输出：

$$\mathcal{L}_{\mathrm{rgb}} = \sum_{\ell \in \mathcal{S}} w_\ell \big[ (1 - \lambda_s) \mathcal{L}_1 + \lambda_s \mathcal{L}_{\mathrm{ssim}} \big]$$

其中 $\mathcal{S}$ 为被监督的级别集合，$w_\ell$ 为各级别的权重，$\mathcal{L}_1$ 和 $\mathcal{L}_{\mathrm{ssim}}$ 分别为L1损失和SSIM损失，$\lambda_s$ 为两者之间的平衡系数。这种设计迫使各级别的高斯共同优化，而非仅关注最精细层级。

**Coarse-to-Fine训练**：训练采用渐进式深度上限策略。初始化时深度上限设为1（仅基础层参与渲染和监督），每50k次迭代增加深度上限并触发自适应细分，逐步引入更细粒度的层级。消融实验（Table 3）表明，多级监督（W/ MLS）在35%传输预算下NVS PSNR达29.87 dB，而仅监督最精细层级的单级监督（W/o MLS）仅为20.06 dB，差距高达9.81 dB。即使在全预算下，联合训练也比冻结前序级别训练（W/ Freeze）高0.39 dB（31.47 vs 31.08）。

**总损失函数**：最终训练目标为多级光度损失与正则化项的加权和：

$$\mathcal{L} = \mathcal{L}_{\mathrm{rgb}} + \lambda_{\mathrm{scale}} \mathcal{L}_{\mathrm{scale}} + \lambda_{\mathrm{pos}} \mathcal{L}_{\mathrm{pos}}$$

其中 $\mathcal{L}_{\mathrm{scale}}$ 约束高斯尺度的过度增长，$\mathcal{L}_{\mathrm{pos}}$ 约束高斯位置偏离三角面过远。论文设定 $\lambda_{\mathrm{scale}} = 1.0$，$\lambda_{\mathrm{pos}} = 0.01$。

---

### 5. 推理时的渐进式渲染流程

推理阶段，预计算的重要性评分指导传输顺序。接收端按面重要性降序逐步激活对应高斯，将其添加到已有渲染管线中。已加载的高斯保持不变，新到达的高斯持续累积细节。这一机制实现了从粗粒度到细粒度的连续质量提升，无需等待完整模型下载即可获得可用的可驱动化身。Table 1 显示，在仅5%传输预算下，该方法即可达到NVS PSNR 27.89 dB、SSIM 0.851，远超需要完整模型的 **GaussianAvatars** 在此预算下的不可用状态。

### 补充图表

![[assets/figures/papers/paper_list_l18_https_arxiv_org_abs_2603_16447/figures/007_Figure_6.jpg]]
*Figure 6: Comparison of adaptive and uniform subdivision. Right: visualization of per-face subdivision levels. Highfrequency regions like facial hair receive more aggressive splitting, whereas smoother areas require substantially fewer subdivisions*

![[assets/figures/papers/paper_list_l18_https_arxiv_org_abs_2603_16447/figures/003_Figure_3.jpg]]
*Figure 3: The center row shows the full model containing all 3D Gaussians within one level. Transmitting in descending importance makes early partial renderings closely match the full-model pixel color because dominant contributors arrive first. In contrast, sending low-importance Gaussians first re-normalizes partial weights and amplifies weak contributors, causing noticeable color drift from the full model. This motivates an importance-first schedule within each level for faithful progressive rendering*



## 实验与关键发现

### 实验设置

实验基于 **NeRSemble** 多视角头部视频数据集，包含16个同步相机。图像被降采样至802×550分辨率。训练/测试划分遵循 **GaussianAvatars** (Qian et al., CVPR 2024) 的设定：使用9个表情序列和15个相机作为训练集，剩余1个表情序列和1个相机用于评估。所有指标均在前景掩码内计算。

训练采用Adam优化器，学习率设置为：重心坐标1×10⁻²、位置5×10⁻³、尺度2×10⁻²、旋转1×10⁻³。损失权重λ_pos=0.01，λ_scale=1.0。最大层次深度D=4，共训练60k次迭代，层次结构每2k次迭代扩展一次。渲染速度在RTX 4090上以550×802分辨率测量。

公平性保障：所有对比方法均使用公开实现，在相同训练数据、相机标定和预处理条件下从头训练。

### 主要结果

**Table 1** 展示了在不同传输预算下的性能对比。在100%预算（完整模型）下，ProgressiveAvatars在NVS任务上达到PSNR 31.47 / SSIM 0.929 / LPIPS 0.068，在NES任务上达到PSNR 25.89 / SSIM 0.908 / LPIPS 0.080，与 **GaussianAvatars** 的完整模型质量相当（NVS: 31.10 / 0.937 / 0.064；NES: 25.80 / 0.911 / 0.076）。

关键优势体现在低预算场景：在仅5%的基础预算下，方法即可获得可用的可驱动化身，NVS指标达到PSNR 27.89 / SSIM 0.851 / LPIPS 0.186，NES指标达到PSNR 25.13 / SSIM 0.804 / LPIPS 0.176。相比之下，**GaussianAvatars** 必须传输完整模型才能开始渲染，在低带宽下完全不可用。

**Table 2** 与SOTA方法的完整模型对比显示，ProgressiveAvatars在NVS PSNR上达到31.5，显著优于 **PointAvatar** (Zheng et al., CVPR 2023) 的25.8（+5.7 dB），略优于 **GaussianAvatars** 的31.1（+0.4 dB）。

**Figure 4** 的定性结果表明，随着传输百分比增加，渲染质量从粗粒度逐步平滑提升至精细细节，验证了渐进式渲染的有效性。

### 存储效率与流式传输优势

**Figure 7(a)** 展示了渐进式流式传输与离散LOD方案的存储对比。ProgressiveAvatars的单一连续资产仅需 **43.4 MB**，而 **GaussianAvatars + LightGaussian**（Fan et al., NeurIPS 2024）构建10个离散LOD级别需要 **227.2 MB**，存储减少 **80.9%**。这一优势源于方法将范式从离散冗余LOD切换转向单一连续可流式资产，无需为不同细节级别存储多个模型副本。

### 消融实验

**Table 3** 报告了跨所有受试者的消融实验结果，系统验证了三个核心设计选择：

**多级监督（MLS）的有效性**：采用多级监督（W/ MLS）在35%预算下NVS PSNR达到29.87，而仅监督最精细层级的单级监督（W/o MLS）仅为20.06，差距高达 **9.81 dB**。即使在100%完整预算下，W/ MLS（31.47）也优于W/o MLS。**Figure 8** 的定性对比进一步展示了不同监督策略下的重建差异，多级监督有效保证了跨级一致性和中间级别的渲染质量。

**重要性排序的作用**：采用基于渲染贡献的重要性排序（W/ Ranking）在25%预算下NVS PSNR达到29.14，比随机排序（W/ Random）的28.40高 **0.74 dB**。这验证了 **Figure 3** 揭示的机制：降序传输使主要贡献高斯优先到达，早期部分渲染与完整模型的像素颜色紧密匹配；而低重要性优先传输会重新归一化部分权重并放大弱贡献者，导致明显的颜色漂移。

**联合训练策略**：多级联合训练（W/ MLS）在全预算下NVS PSNR比冻结前序级别训练（W/ Freeze）高0.39 dB（31.47 vs 31.08），表明允许所有级别在训练中协同优化有助于全局质量提升。

**自适应细分的优势**：**Figure 6** 对比了自适应细分与均匀细分策略。自适应细分根据屏幕空间梯度仅在细节丰富区域（如面部毛发）进行更激进的分裂，而平滑区域保持较少细分。结果显示，自适应策略用更少的高斯数量达到了更高的重建质量。同时，多级设计保证了全局基础级别覆盖，使得渐进式渲染从粗到细平滑过渡，避免了均匀细分可能导致的局部信息缺失。

### 失败模式与局限

当前方法存在以下已知局限，需要在实际应用中加以注意：

1. **范围限制**：方法目前仅针对头部化身设计和验证，尚未在全身化身或通用3D资产上验证扩展性。将渐进式网格锚定高斯层次推广到更广泛的动态场景仍需进一步研究。

2. **跟踪依赖**：自适应细分及驱动机制依赖FLAME网格的精确跟踪。在多视角视频中，跟踪误差（尤其在快速运动或极端表情下）可能传播到高斯绑定和层次结构，影响细节质量和动画稳定性。该问题需要在实际部署中通过更鲁棒的跟踪器或在线校正机制来缓解。

3. **重要性评分的泛化性**：重要性排序基于训练视图的聚合渲染贡献进行预计算。在极端新表情或新视角下，训练阶段未充分覆盖的区域可能出现评分偏差，导致优先传输的高斯并非新视角下的主要贡献者。能否在接收端实时更新评分以适应动态条件，仍是一个开放问题。

4. **压缩结合潜力**：当前方法在存储效率上已显著优于离散LOD方案，但尚未探索将向量量化等压缩技术与层次结构深度结合的可能性，以进一步降低传输比特率同时保持可驱动性。

### 补充图表

![[assets/figures/papers/paper_list_l18_https_arxiv_org_abs_2603_16447/figures/005_Table_1.jpg]]
*Table 1: Performance comparison across varying transmission budgets. We report Novel View Synthesis (NVS) and Novel Expression Synthesis (NES) using PSNR/SSIM/LPIPS. We also list the number of Gaussians, the amount of data to transmit (in Megabytes), and rendering speed. Rendering speed is measured on an RTX 4090 at 550 × 802 resolution*

![[assets/figures/papers/paper_list_l18_https_arxiv_org_abs_2603_16447/figures/008_Table_2.jpg]]
*Table 2: Quantitative comparison with SOTA methods. We denote the best and second best scores in different colors*

![[assets/figures/papers/paper_list_l18_https_arxiv_org_abs_2603_16447/figures/011_Table_3.jpg]]
*Table 3: Ablation study across all subjects. We report average Novel View Synthesis (NVS) and Novel Expression Synthesis (NES) metrics over all subjects. “W/o MLS” supervises only the finest level, whereas “W/ MLS” supervises all levels*

![[assets/figures/papers/paper_list_l18_https_arxiv_org_abs_2603_16447/figures/009_Figure_7.jpg]]
*Figure 7: Progressive streaming and multi-level ablation*

![[assets/figures/papers/paper_list_l18_https_arxiv_org_abs_2603_16447/figures/010_Figure_8.jpg]]
*Figure 8: Ablation study on multi-level supervision*

![[assets/figures/papers/paper_list_l18_https_arxiv_org_abs_2603_16447/figures/004_Figure_4.jpg]]
*Figure 4: Qualitative results on NeRSemble dataset across different transmission percentages*

![[assets/figures/papers/paper_list_l18_https_arxiv_org_abs_2603_16447/figures/006_Figure_5.jpg]]
*Figure 5: Qualitative comparison with state-of-the-art methods*

![[assets/figures/papers/paper_list_l18_https_arxiv_org_abs_2603_16447/figures/001_Figure_1.jpg]]
*Figure 1: ProgressiveAvatars is a novel progressive representation that supports adaptive rendering quality of 3D Gaussian avatars under bandwidth or compute constraints. Qualitative (left) and quantitative (right) results demonstrate that ProgressiveAvatars rapidly attains high quality and continues to refine the avatar as more data arrives, whereas GaussianAvatars [15] only becomes usable once nearly the entire asset has been transmitted*



## 定位与知识库关联

### 1. 与基线方法的关系

**ProgressiveAvatars** 的直接前身是 **GaussianAvatars**（Qian et al., CVPR 2024），后者确立了将3D高斯绑定到FLAME网格三角面局部坐标系的范式，实现了高质量可驱动头部化身。ProgressiveAvatars 继承这一绑定机制，但在表示结构上做出了根本性改造：引入基于屏幕空间梯度的自适应隐式细分，将原本扁平的高斯集合重构为多级三角面森林层次结构。这一改动使模型从“完整下载后渲染”的静态资产，转变为支持渐进式流式传输的连续资产。

在细分策略上，本文区别于 **LoDAvatar** 等采用均匀细分或多份离散LOD副本的方案。均匀细分（Figure 6）对所有面一视同仁，导致平滑区域浪费高斯预算，而自适应细分仅在细节丰富区域（如胡须、眉毛）进行更深层次分裂，用更少高斯达到更高重建质量。更重要的是，多级层次设计保证了全局基础覆盖，使得即使在极低传输预算下也能获得完整头部轮廓的可驱动化身，而均匀细分在低预算下会出现大面积空洞。

在渐进式传输层面，现有3DGS化身方法（包括GaussianAvatars）均要求完整模型就绪后方可渲染，导致高启动延迟和带宽突发。ProgressiveAvatars 通过重要性排序机制（Eq. 3: $W_i = \sum_{j \in \mathcal{G}_i} \sum_{p} \alpha_{j,p} T_{j,p}$）调度传输顺序，使主导渲染贡献的高斯优先到达，显著减少早期局部渲染的颜色漂移（Figure 3），在25%预算下较随机排序提升0.74 dB NVS PSNR（Table 3）。

与压缩基线 **GaussianAvatars + LightGaussian**（Fan et al., NeurIPS 2024）的对比揭示了范式差异：后者生成10个离散LOD层级需227.2 MB存储，而 ProgressiveAvatars 的单一连续流式资产仅需43.4 MB（Figure 7a），减少80.9%，且无需在层级间切换模型。

### 2. 适用边界

当前方法明确限定于**头部化身**场景，依赖FLAME网格的精确多视角跟踪作为驱动骨架。适用条件包括：
- 输入为多视角头部视频（NeRSemble设定：16相机，802×550分辨率）
- 训练需覆盖目标人物的多种表情和视角（9/10表情序列，15/16相机用于训练）
- 推理时需在接收端维护完整的三角面层次树结构，以支持渐进激活

尚未验证的扩展方向包括：全身化身、通用动态3D资产、以及非FLAME拓扑的网格结构。

### 3. 局限与开放问题

**已验证的局限：**

1. **跟踪依赖**：自适应细分及面局部高斯绑定完全依赖FLAME网格的精确跟踪。跟踪误差（尤其在快速运动或极端表情下）会直接传导至高斯位置和细分决策，影响细节质量和动画稳定性。论文未报告在跟踪质量退化场景下的鲁棒性。

2. **重要性评分的静态性**：重要性分数 $W_i$ 基于训练视图的聚合渲染贡献预计算，在极端新表情或新视角下可能出现评分偏差——训练时贡献高的面在新条件下未必保持同等重要性。论文未探讨在线更新评分的机制。

3. **范围局限**：仅验证于头部化身，未涉及全身或通用场景。

**开放问题：**

1. **跨域扩展**：如何将渐进式网格锚定高斯层次扩展到全身化身或通用动态场景的流式传输？这需要解决大尺度网格拓扑的层次构建和跨身体部位的传输优先级协调问题。

2. **动态自适应传输**：能否在接收端实时更新重要性评分，以适应动态网络条件和用户兴趣区域（如视线聚焦区域）的变化？当前方案需预计算评分，缺乏对运行时上下文的响应能力。

3. **压缩-可驱动性联合优化**：是否可将向量量化等压缩技术与层次结构深度结合，在进一步降低传输比特率的同时保持各级别的可驱动性？当前43.4 MB的存储虽已显著低于离散LOD方案，但在移动网络场景下仍有压缩空间。

4. **跟踪鲁棒性**：能否通过联合优化跟踪与高斯重建，或引入跟踪不确定性建模，减轻跟踪误差对渐进式表示的级联影响？



## 原文 PDF

![[paperPDFs/CVPR_2026/ProgressiveAvatars_Progressive_Animatable_3D_Gaussian_Avatars.pdf]]
