---
title: Dynamic-Static Decomposition for Novel View Synthesis of Dynamic Scenes with Spiking Neurons
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/Dynamic_Static_Decomposition_for_Novel_View_Synthesis_of_Dynamic_Scenes_with_Spiking_Neurons.pdf
project_link: "https://zju-bmi-lab.github.io/SpikeMaskGS-homepage"
code_link: null
aliases:
- DSDF4MFSNT
- DSDNVSDSSN
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
core_operator: 通过引入时空细粒度的4D掩码场，提供更准确的动静掩码先验；并采用脉冲神经元直接输出二值标签，消除连续标签后处理的不确定性，从而精准控制高斯原语的动静分配。
primary_logic: 构建可学习的4D掩码场为每个视点-时刻生成细粒度动静掩码，替代手工设计的先验；利用脉冲神经元的不可微二元输出特性，实现端到端可训练的离散动静标记场，避免了传统方法中连续标签离散化的分布失配和超参数敏感问题。
claims:
- 4D mask field provides spatio-temporally fine-grained mask priors, outperforming discrete 2D mask images and temporal-invariant priors.
- Spiking neuron-based discontinuous tagging field directly outputs binary dynamic-static labels, avoiding uncertainty from post-processing continuous tags.
- Qualitative results show our binary mapping yields clearer boundaries between static and dynamic regions compared to continuous post-processing methods.
- Quantitative experiments on N3DV and MeetRoom under side-view setting confirm SOTA rendering quality.
---

# Dynamic-Static Decomposition for Novel View Synthesis of Dynamic Scenes with Spiking Neurons

> [!tip] 核心洞察
> 构建可学习的4D掩码场为每个视点-时刻生成细粒度动静掩码，替代手工设计的先验；利用脉冲神经元的不可微二元输出特性，实现端到端可训练的离散动静标记场，避免了传统方法中连续标签离散化的分布失配和超参数敏感问题。

| 字段 | 内容 |
|------|------|
| 中文题名 | 基于脉冲神经元的动态场景新视角合成动静分解方法 |
| 英文题名 | Dynamic-Static Decomposition for Novel View Synthesis of Dynamic Scenes with Spiking Neurons |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://openaccess.thecvf.com/content/CVPR2026/html/Dai_Dynamic-Static_Decomposition_for_Novel_View_Synthesis_of_Dynamic_Scenes_with_CVPR_2026_paper.html) · [Project](https://zju-bmi-lab.github.io/SpikeMaskGS-homepage) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction |
| Method | Dynamic-Static Decomposition Framework with 4D Mask Field and Spiking Neuron Tagging |
| Dataset | N3DV, MeetRoom, VRU |

> [!tip] 效果简介
> - N3DV (Side View) 上，PSNR / LPIPS / FPS 26.30 / 0.0615 / 137。
> - MeetRoom (Side View) 上，PSNR / LPIPS / FPS 26.64 / 0.0626 / 154。
> - VRU 上，PSNR / LPIPS / FPS 29.43 / 0.170 / 77。

## 概述

动态场景的新视角合成（NVS）面临一个核心瓶颈：**动态-静态分解的不准确性**。现有方法通常依赖外部预训练模型逐视图生成掩码，或使用时间不变的先验，这些掩码缺乏时空一致性，导致在细粒度运动和侧视点下动静高斯原语分配错误。同时，主流方案将动静标签建模为连续浮点属性，再通过阈值后处理获得离散标签，这一过程引入了分布失配和后处理超参数敏感性问题，造成边界伪影和重建不稳定。

针对上述瓶颈，本文提出了一套**基于动静分解的动态场景 NVS 框架**，其关键调控手段体现在两个层面：

1. **掩码先验的时空细粒度化**：构建一个可学习的 **4D 掩码场** $\mathcal{F}(v,t)$，为每个视点-时刻组合生成时空一致的动静掩码，替代手工设计的离散 2D 掩码或时间不变先验。
2. **标签表示的离散化**：引入**脉冲神经元**构建不连续标记场，利用其不可微的 Heaviside 阶跃输出直接生成二值动静标签 $d^s \in \{0,1\}$，消除连续标签离散化带来的不确定性，实现端到端可训练的离散标记。

该方法在 **N3DV** 和 **MeetRoom** 数据集上采用侧视图（side-view）评测设定——将测试视图置于训练视图范围之外，避免过拟合导致的虚假高性能——取得了 SOTA 渲染质量：N3DV 侧视图 PSNR 达 26.30，MeetRoom 侧视图 PSNR 达 26.64，同时保持实时推理帧率（137/154 FPS）。消融实验证实，4D 掩码场与脉冲神经元组合使用达到最优，且脉冲神经元相比连续优化（Sigmoid+阈值）及其他离散方法（STE、Gumbel-Softmax）均有显著提升。

**方法定位**：本工作属于动态场景高斯泼溅（Gaussian Splatting）重建谱系中的动静分解分支，与 **Swift4D**（Wu et al., ICLR 2025）、**Ex4DGS**（Lee et al., NeurIPS 2024）等显式分解方法形成对比。其核心贡献在于将动静分解的两个关键环节——掩码先验生成和标签表示——分别从“手工设计”和“连续+后处理”推进到“可学习 4D 场”和“脉冲神经元直接二值化”，为动态场景重建提供了一种更精确、更稳定的分解范式。

## 背景与动机

### 动态场景新视角合成的核心挑战

从多视角视频中重建动态场景并合成任意新视角的图像，是计算机视觉与图形学中长期存在的难题。近年来，以 3D Gaussian Splatting (3DGS) 为代表的显式辐射场方法在静态场景上取得了实时渲染与高质量重建的突破，但其向动态场景的扩展面临根本性困难：场景中同时存在静态区域（如背景、桌面）和动态区域（如运动的人体、物体），二者的几何与外观变化模式截然不同。若将所有高斯原语统一处理，静态区域会因不必要的形变建模而引入噪声，动态区域则可能因建模能力不足而丢失细节。

### 动静分解范式的现有缺口

为解决上述问题，主流动态场景重建方法采用了**动态-静态分解**范式：先将高斯原语分类为动态与静态两组，再分别进行形变建模与静态保持。这一范式的性能瓶颈在于**高斯原语的动静分配精度**，而现有方法在两个关键环节上存在系统性缺陷。

**缺口一：掩码先验缺乏时空一致性。** 分解过程通常依赖外部预训练模型（如分割网络）逐视图生成 2D 掩码，或基于逐帧光度残差构造时域不变的先验。前者因多视图间模型预测不一致，导致同一空间点在不同视点下被赋予矛盾的动静标签；后者忽视了运动区域随时间和视点变化的空间分布差异，在细粒度运动（如手势、面部表情）和侧视点下尤为失效。这些不准确的掩码先验直接误导了高斯原语的动静分配监督信号。

**缺口二：连续标签离散化引入不确定性。** 现有方法普遍为每个高斯原语学习一个连续的动态属性 $d^c \in [0,1]$，再通过阈值后处理获得离散的动静标签。这种"连续优化+后处理离散化"的策略存在两个固有问题：（1）**分布失配**——连续属性值域连续，而标签空间是二值的，优化目标与最终使用之间存在语义鸿沟；（2）**超参数敏感**——阈值的选择直接影响分解边界，不同场景需手动调参，且边界区域的高斯原语对阈值极为敏感，易产生伪影。如 Figure 3 所示，基于 Sigmoid+阈值的方法在动态映射图中产生了模糊的边界和碎片化的误分类区域。

### 本文动机：从掩码先验与标签表示两个维度突破

针对上述瓶颈，本文从两个因果维度提出改进：

1. **掩码先验的时空细粒度化**：构建可学习的 4D 掩码场 $\mathcal{F}(v, t)$，为每个视点-时刻对生成特定的 2D 动静掩码，替代手工设计的离散掩码集或时域不变先验，从根本上解决多视图不一致和时域粗糙的问题。

2. **标签表示的离散化原生建模**：采用脉冲神经元（Spiking Neuron）直接输出二值动静标签 $d^s \in \{0,1\}$，利用其不可微的 Heaviside 阶跃函数实现端到端的离散优化，消除连续标签后处理带来的分布失配和超参数敏感问题。

通过这两个模块的协同，本文方法在侧视图评测设定下实现了更清晰的动静分解边界和更优的新视角合成质量，为动态场景的显式辐射场重建提供了新的技术路线。

## 核心创新

本工作针对动态场景新视角合成中**动静分解**这一核心环节，揭示了现有方法的两大瓶颈，并提出了对应的创新模块。

**瓶颈一：掩码先验缺乏时空一致性。** 现有方法依赖预训练模型逐视图分割或逐帧光度不一致来生成动静掩码，这些先验在多视图下缺乏一致性，在时间维度上又缺乏连续性，导致在细粒度运动和侧视点下高斯原语的动静分配出现错误（Figure 1 B）。

**创新一：时空细粒度4D掩码场。** 我们构建了一个可学习的4D掩码场 $\mathcal{F}(v, t)$，直接以视点 $v$ 和时间 $t$ 为输入，生成该视点-时刻对应的2D动静掩码 $M^{v,t}$。相比现有方法使用的离散2D掩码图像集合或时间不变先验，4D掩码场提供了时空一致的细粒度先验，能够更准确地捕捉细粒度运动（Figure 1 E）。该掩码场通过逐像素掩码损失 $\mathcal{L}_{\mathcal{F}}^{v,t}$ 进行训练，鼓励静态与动态像素之间的残差差异最大化。

**瓶颈二：连续标签离散化引入不确定性。** 现有方法（如 **Swift4D** Wu et al., ICLR 2025；**Ex4DGS** Lee et al., NeurIPS 2024）为每个高斯原语维护一个连续的动态属性 $d^c$，再通过阈值后处理获得离散标签。这种“连续优化+后处理离散化”的范式存在两个问题：连续标签与离散标签之间存在分布失配，且后处理阈值的选择引入超参数敏感性，导致动静边界模糊（Figure 3 c）。

**创新二：基于脉冲神经元的离散标记场。** 我们设计了以脉冲神经元实现的**不连续动静标记场**，直接输出二值标签 $d^s \in \{0,1\}$。具体而言，采用IF模型的Heaviside阶跃函数 $d^s = H(d^c - V_{th})$ 实现二元输出（$V_{th}=0$），并通过反正切代理梯度 $\frac{\partial d_i^s}{\partial d_i^c} = \frac{\beta}{2(1+(\frac{\pi}{2}\beta d_i^c)^2)}$ 解决不可微问题，实现端到端可训练。这一设计消除了连续标签离散化的分布失配和超参数敏感问题，使得动静边界更加清晰（Figure 3 a）。

**创新三：属性解耦交替优化。** 在训练策略上，我们将高斯几何属性 $G^{geo}$ 与动静标签 $d^s$ 解耦，采用交替优化范式：固定标签优化几何，固定几何优化标签。这一策略避免了联合优化中标签分配与几何重建之间的干扰，进一步提升了分解精度和渲染质量。

两个核心模块的协同作用——4D掩码场提供准确的时空先验，脉冲神经元标记场实现精准的离散分配——构成了本方法在动静分解上的关键优势。消融实验（Table 3）证实，单独使用4D掩码场或脉冲神经元均能带来渲染质量提升，而二者组合达到最佳效果；脉冲神经元相比连续优化（Sigmoid+阈值）以及其他离散化方法（STE、Gumbel-Softmax）均有显著优势（Figure 6）。

## 整体框架

本文提出一种基于动静分解的动态场景新视角合成框架，其核心思路是**将场景显式拆分为动态高斯与静态高斯，分别建模并最终融合渲染**。框架整体由四个关键模块串联构成，信息流遵循“掩码先验生成 → 动静标签分配 → 形变建模 → 混合渲染”的管线。

### 输入与输出

- **输入**：多视角视频序列，包含不同视点 $v$ 和时刻 $t$ 的 RGB 图像，以及标定的相机参数。
- **输出**：任意新视点、新时刻的渲染图像，以及像素级动态映射图 $\hat{M}$（指示每个像素属于动态区域还是静态区域）。

### 模块关系与数据流

1. **时空细粒度掩码场 (Spatio-Temporal Fine-Grained Mask Field)**  
   该模块以视点 $v$ 和时间 $t$ 为输入，通过可学习的4D掩码场 $\mathcal{F}(v, t)$ 生成视点-时刻特定的2D动静掩码 $M^{v,t}$（见 Eq. 4）。该掩码作为后续标签分配的监督先验，替代了现有方法中缺乏时空一致性的手工设计先验（如逐帧分割或时不变先验）。

2. **非连续动静标记场 (Discontinuous Dynamic-Static Tagging Field)**  
   该模块为每个高斯原语赋予一个连续动态属性 $d^c$，并通过脉冲神经元（IF 模型）的 Heaviside 阶跃函数将其直接映射为二值标签 $d^s \in \{0,1\}$（Eq. 8–9），其中 1 表示动态高斯，0 表示静态高斯。这一设计消除了传统方法中“连续属性 → 阈值后处理 → 离散标签”引入的分布失配和超参数敏感问题。

3. **形变场 (Deformation Field)**  
   对于被标记为动态的高斯原语，形变场（基于4D哈希编码 + MLP）预测其在每个时刻的形变参数 $(\Delta \mu, \Delta q, \Delta s, \Delta \sigma)$，从而将规范空间中的动态高斯变换到当前时刻的观测空间。静态高斯则保持其规范空间属性不变。

4. **Alpha 混合渲染器**  
   将形变后的动态高斯与静态高斯合并，通过标准的 alpha 混合渲染管线生成最终的颜色图像（Eq. 2）和动态映射图 $\hat{M}$（Eq. 10）。动态映射图由各高斯的二值标签 $d_i^s$ 经 alpha 混合得到，用于与掩码场生成的先验掩码计算监督损失。

### 训练策略

框架采用**属性解耦交替优化**策略：将高斯几何属性 $G^{geo}$（位置、协方差、颜色等）与动静标签 $d^s$ 分离，交替进行优化。这种解耦设计避免了标签分配与几何优化之间的相互干扰，提升了训练的稳定性和最终分解质量。

### 框架优势

与现有动静分解方法（如 **Swift4D** (Wu et al., ICLR 2025)、**Ex4DGS** (Lee et al., NeurIPS 2024)）相比，本框架的两处关键改进——4D掩码场和脉冲神经元标记场——分别解决了“掩码先验时空不一致”和“连续标签离散化不确定性”两个瓶颈问题。定量实验表明，在 N3DV 和 MeetRoom 数据集的侧视图设定下，本方法分别达到 26.30 PSNR 和 26.64 PSNR，优于现有 SOTA 方法（Table 1）。

### 补充图表

![[assets/figures/papers/paper_list_l2472_https_openaccess_thecvf_com_content_CVPR2026_html_Dai_Dynamic_Static_Dec/figures/002_Figure_2.jpg]]
*Figure 2: Our method has two key modules: Spatio-Temporal Fine-Grained Mask Field to provide mask priors and Discontinuous Dynamic-Static Tagging Field to directly optimize discontinuous dynamic-static labels. Based on different reconstruction pipelines for dynamic and static Gaussians, we alternatively optimize Gaussian geometric attributes*

## 核心模块与公式推导

本方法在动态-静态分解框架中引入两个核心模块，分别解决掩码先验时空不一致和连续标签离散化不确定性问题。

### 时空细粒度掩码场

传统方法依赖预训练模型逐视图分割或逐帧光度不一致生成动静掩码，缺乏时空一致性，在细粒度运动和侧视点下分配错误。本文构建一个可学习的4D掩码场 $\mathcal{F}$，以视点 $v$ 和时间 $t$ 为输入，生成该视点-时刻特定的2D动静掩码：

$$M^{v,t} = \mathcal{F}(v, t)$$

掩码场的训练通过逐像素损失驱动，鼓励静态与动态像素之间的残差差异最大化：

$$\mathcal{L}_{\mathcal{F}}^{v,t} = \sum_{i,j} M_{\mathrm{fine}}^{i,j}(v,t) \odot r(v,t)^{i,j}$$

其中 $r(v,t)^{i,j}$ 为像素 $(i,j)$ 的渲染残差，$M_{\mathrm{fine}}^{i,j}(v,t)$ 为细粒度掩码。训练时先用残差阈值 $\tau_r$ 生成粗粒度静态掩码 $M_{\mathrm{coarse}}^{i,j}(v,t) = r^{i,j}(v,t) \leq \tau_r$，再通过盒滤波扩散得到细粒度掩码，形成时空一致的掩码先验。

### 脉冲神经元驱动的离散动静标记场

现有方法为每个高斯原语分配连续浮点属性 $d^c$，再通过阈值后处理获得离散标签 $d^s \in \{0,1\}$。这一过程引入分布失配和超参数敏感问题。本文采用脉冲神经元直接输出二值标签，实现端到端可训练的离散标记。

**二值映射**：将连续动态属性 $d^c$ 通过二值映射函数 $\mathcal{S}(\cdot)$ 转换为离散标签：

$$d^{s} = \mathcal{S}(d^{c})$$

**脉冲神经元实现**：采用Integrate-and-Fire (IF) 模型，以Heaviside阶跃函数实现脉冲输出，阈值 $V_{th}$ 设为零：

$$d^{s} = H(d^{c} - V_{th})$$

**动态映射图渲染**：通过alpha混合将高斯原语的离散标签渲染为像素级动态映射图 $\hat{M}$：

$$\hat{M} = \sum_{i \in N} d_i^s \alpha_i \prod_{j=1}^{i-1} (1-\alpha_i)$$

其中 $\alpha_i$ 为第 $i$ 个高斯的透明度，$N$ 为沿光线相交的高斯集合。

**代理梯度**：Heaviside函数不可微，采用反正切函数作为梯度代理，实现脉冲神经元的反向传播：

$$\frac{\partial d_i^s}{\partial d_i^c} = \frac{\beta}{2\left(1+\left(\frac{\pi}{2}\beta d_i^c\right)^2\right)}$$

其中 $\beta$ 控制代理梯度的陡峭程度。通过链式法则，渲染损失可反向传播至连续属性 $d^c$：

$$\frac{\partial \hat{M}}{\partial d_i^c} = \frac{\partial d_i^s}{\partial d_i^c} \alpha_i \prod_{j=1}^{i-1} (1-\alpha_i)$$

### 属性解耦交替优化

框架采用属性解耦策略，将高斯几何属性 $G^{geo}$ 与动静标签 $d^s$ 分离优化：交替执行标签分配阶段和几何优化阶段，避免联合优化中标签不稳定对几何重建的干扰。

**训练损失**：总损失由渲染损失和掩码监督损失组成。渲染损失组合L1和SSIM：

$$\mathcal{L}_{\mathrm{render}} = (1-\lambda)\mathcal{L}_1 + \lambda\mathcal{L}_{\mathrm{SSIM}}$$

掩码监督损失采用二值交叉熵，约束渲染的动态映射图与目标掩码一致：

$$\mathcal{L}_{\mathrm{mask}} = -M \cdot \log(\hat{M}) - (1-M) \cdot \log(1-\hat{M})$$

### 补充图表

![[assets/figures/papers/paper_list_l2472_https_openaccess_thecvf_com_content_CVPR2026_html_Dai_Dynamic_Static_Dec/figures/001_Figure_1.jpg]]
*Figure 1: (A).Dynamic–static decomposition methods [45, 50, 58] use dynamic–static mask priors to supervise the dynamic–static tag representation, obtaining dynamic and static Gaussians for separate processing. (B). Current methods suffer from inaccurate mask priors brought by multi-view inconsistent external models [7] or temporal invariant priors [50]. Instead, we generate spatio-temporal fine-grained mask priors and yield better performance on fine-grained motions (shown in (E)); (C). Current methods use an improper tag representation that optimizes continuous probabilities and uses threshold-based post-processing for discrete labels, introducing postprocessing uncertainty. Instead, we directly op...*

![[assets/figures/papers/paper_list_l2472_https_openaccess_thecvf_com_content_CVPR2026_html_Dai_Dynamic_Static_Dec/figures/003_Figure_3.jpg]]
*Figure 3: Visualization of rendered image and rendered dynamic map with dynamic tag/label for post-processing driven methods [17, 50] and our binary mapping on two dynamic regions. (a). Our binary mapping achieves a clear boundary between static and dynamic pixels and fine-grained rendering details; (b). Ground truth rendering for chosen dynamic regions; (c). Existing method using a continuous function(e.g., Sigmoid) to normalize the tag and rely on threshold-based post-processing. Post-processing not only results in a distribution gap between continuous tag and discrete label(different dynamic map) but also introduces threshold sensitivity. Please zoom in to observe fine details*

![[assets/figures/papers/paper_list_l2472_https_openaccess_thecvf_com_content_CVPR2026_html_Dai_Dynamic_Static_Dec/figures/004_Figure.jpg]]
*Figure: (a) Prior Methods (b) Ours*

## 实验与分析

### 评测协议与基准

动态场景新视角合成的传统评测通常将测试视图选在训练视图范围内，模型可能因过拟合而产生虚假的高性能指标。为提供更可靠的重建质量评估，本文提出**侧视图（side-view）评测设定**：将测试视图置于训练视图的外侧，增大训练与测试视图间的视差，从而更有效地区分真实场景几何重建与过拟合（Figure 4）。实验在三个数据集上展开：**N3DV**（多视角室内动态场景）、**MeetRoom**（多人会议场景）以及 **VRU**（大规模自由视点动态场景）。对于 VRU 数据集，遵循 **SplineGS**（Park et al., CVPR 2025）的设定，每 20 帧进行一次训练与测试。

![[assets/figures/papers/paper_list_l2472_https_openaccess_thecvf_com_content_CVPR2026_html_Dai_Dynamic_Static_Dec/figures/005_Figure_4.jpg]]
*Figure 4: Side View Setting. Comparison of train–test splits between prior methods and ours. Unlike previous approaches [17, 46, 49, 50] that select test views within or close to the training view range, where models can yield deceptively good results due to overfitting, our split places the evaluation views outside the training range, providing a more reliable measure of reconstruction accuracy*

### 主实验结果

**N3DV 与 MeetRoom 侧视图评测。** Table 1 汇总了各方法在 N3DV 和 MeetRoom 数据集侧视图设定下的定量比较。本文方法在 N3DV 上取得 **26.30 PSNR / 0.0615 LPIPS / 137 FPS**，在 MeetRoom 上取得 **26.64 PSNR / 0.0626 LPIPS / 154 FPS**，均优于现有动态场景重建方法，包括 **Swift4D**（Wu et al., ICLR 2025）、**Ex4DGS**（Lee et al., NeurIPS 2024）、**4D-GS**（Wu et al., CVPR 2024）和 **SplineGS**（Park et al., CVPR 2025）。渲染速度方面，由于更准确的动静标签分配减少了冗余动态高斯原语，本文方法实现了更高的 FPS，表明更快的渲染效率。定性结果见 Figure 7，在 *cut beef* 和 *coffee martini* 等场景的侧视图合成中，本文方法保留了更丰富的细节。

**VRU 数据集。** Table 2 给出了 VRU 数据集上的定量比较。本文方法取得 **29.43 PSNR / 0.170 LPIPS / 77 FPS**，相比连续优化方法和离散优化替代方案（如 STE、Gumbel-Softmax）均有显著提升。Figure 6 的侧视图合成定性对比进一步表明，脉冲神经元驱动的离散标签场在边界清晰度和细节保真度上优于连续后处理和其他离散优化策略。Figure 8 展示了 *dg* 和 *gz* 场景的合成结果。

### 消融实验

Table 3 报告了在 N3DV *cut beef* 场景侧视图设定下的消融结果，系统验证了两个核心模块的贡献：

![[assets/figures/papers/paper_list_l2472_https_openaccess_thecvf_com_content_CVPR2026_html_Dai_Dynamic_Static_Dec/figures/008_Table_3.jpg]]
*Table 3: Ablation results of PSNR, LPIPS, and FPS on cut beef scene from the N3DV dataset under the side view setting. SN stands for Spiking Neuron*

1. **4D 掩码场（Mask Field）的贡献。** 移除 4D 掩码场（退化为时域不变的掩码先验或逐视图 2D 掩码）后，PSNR 和 LPIPS 均出现下降，验证了时空细粒度掩码先验对动静分解精度的重要性。
2. **脉冲神经元（Spiking Neuron, SN）的贡献。** 将脉冲神经元替换为连续优化 + 阈值后处理（Sigmoid + threshold）或其他离散化策略（STE、Gumbel-Softmax）后，渲染质量显著降低。这印证了核心洞察：连续标签离散化过程中的分布失配和后处理超参数敏感性是性能瓶颈，而脉冲神经元的原生二值输出从根本上消除了这一问题。
3. **组合效果。** 4D 掩码场与脉冲神经元联合使用达到最佳性能，表明准确的掩码先验与端到端可训练的离散标签场具有协同增益。

Figure 3 提供了动态映射图的可视化消融：本文的二值映射在静态与动态像素之间形成清晰边界，而连续后处理方法则因分布间隙和阈值敏感性导致边界模糊和细粒度细节丢失。Figure 5 进一步展示了仅使用动态高斯原语渲染的动态区域可视化，验证了动静分解的准确性。

### 方法局限与开放问题

尽管本文方法在侧视图评测下取得了 SOTA 性能，但分析中仍存在若干待验证的边界条件：

- **色彩不一致的训练视图。** 当训练视图间存在色彩差异时，4D 掩码场依赖的残差信号可能破坏时空一致性，导致掩码先验质量下降。该场景下的鲁棒性需进一步验证。
- **完全动态场景。** 该方法的核心依赖是动态-静态区域分解。在无静态区域的完全动态场景下，动静分解的效用和标签场的学习行为尚未被系统研究，需手动验证其有效性边界。

### 补充图表

![[assets/figures/papers/paper_list_l2472_https_openaccess_thecvf_com_content_CVPR2026_html_Dai_Dynamic_Static_Dec/figures/007_Table_1.jpg]]
*Table 1: Quantitative comparison of PSNR, LPIPS, and FPS on the N3DV and MeetRoom datasets under the side view setting*

![[assets/figures/papers/paper_list_l2472_https_openaccess_thecvf_com_content_CVPR2026_html_Dai_Dynamic_Static_Dec/figures/009_Table_2.jpg]]
*Table 2: Comparison of PSNR, LPIPS, and FPS across different methods on VRU dataset. Following [50], each scene is trained and tested every 20 frames*

![[assets/figures/papers/paper_list_l2472_https_openaccess_thecvf_com_content_CVPR2026_html_Dai_Dynamic_Static_Dec/figures/006_Figure_6.jpg]]
*Figure 6: Our method observes better side view synthesis on the VRU dataset, outperforming continuous optimization and other discrete optimization(e.g., STE [1], Gumbel-Softmax [15]) methods*

![[assets/figures/papers/paper_list_l2472_https_openaccess_thecvf_com_content_CVPR2026_html_Dai_Dynamic_Static_Dec/figures/010_Figure_7.jpg]]
*Figure 7: Visualization of novel view synthesis on cut beef and coffee martini scenes from the N3DV dataset under the side view setting. Please zoom in to observe fine details*

![[assets/figures/papers/paper_list_l2472_https_openaccess_thecvf_com_content_CVPR2026_html_Dai_Dynamic_Static_Dec/figures/011_Figure_8.jpg]]
*Figure 8: Visualization of novel view synthesis on dg, gz scenes from the VRU dataset. Please zoom in to observe fine details*

## 方法谱系与知识库定位

### 1. 与已有工作的关系

**动态场景重建与高斯泼溅。** 本工作建立在 4D 高斯泼溅（4D Gaussian Splatting, 4D-GS）系列方法的框架之上，将动态场景重建分解为静态高斯原语的直接表示与动态高斯原语的形变建模。与 **4D-GS**（Wu et al., CVPR 2024）和 **SplineGS**（Park et al., CVPR 2025）等整体形变方法不同，本文引入显式的动静分解机制，仅对动态区域施加形变场，从而减少冗余计算。

**动静分解基线。** 在动静分解这一具体技术路线上，**Swift4D**（Wu et al., ICLR 2025）和 **Ex4DGS**（Lee et al., NeurIPS 2024）是直接对比基线。这两类方法均采用连续浮点属性 $d^c$ 表示高斯的动静倾向，并通过阈值后处理获得离散标签。本文指出该范式存在根本性缺陷：连续标签与离散标签之间存在分布失配，后处理超参数（阈值）引入边界不确定性。本文用脉冲神经元直接输出二值标签 $d^s \in \{0,1\}$，在方法层面切断了这一后处理依赖。

**掩码先验来源。** 现有方法获取动静掩码先验的途径主要有二：（1）依赖外部预训练模型逐视图分割，缺乏多视图时空一致性；（2）使用时序不变的先验（如首帧掩码或固定区域），无法捕捉细粒度运动和侧视点下的真实动静分布。本文构建可学习的4D掩码场 $\mathcal{F}(v,t)$，为每个视点-时刻生成特定的2D掩码，在时空细粒度层面填补了这一空白。

**脉冲神经网络与离散优化。** 本文并非第一个在计算机视觉任务中使用脉冲神经元的工作，但将其引入动态场景高斯原语的离散标签学习，属于跨领域迁移。在离散优化的替代方案对比中（Table 3, Fig. 6），本文验证了脉冲神经元（SN）优于连续优化（Sigmoid+threshold）以及其他离散松弛方法如 STE 和 Gumbel-Softmax，说明不可微二元输出在动静标记这一特定任务上具有独特优势。

### 2. 适用边界与局限

**适用前提：动静可分解性。** 本方法的核心假设是场景中存在可区分的静态与动态区域。对于完全动态场景（无静态背景可参照），动静分解将退化为全动态标记，4D掩码场的残差驱动训练机制可能失效——这是验证分析中明确提出的开放问题，目前缺乏实验证据。

**训练视图质量依赖。** 4D掩码场的训练依赖于训练视图的渲染残差 $r(v,t)$。若训练视图存在显著色差（如光照变化、相机白平衡漂移），残差信号将破坏时空一致性，导致掩码先验质量下降。这是一个已识别但未在论文中通过实验验证的边界条件。

**侧视图评测的推广性。** 本文提出的侧视图（Side View）评测设定将测试视图置于训练视图范围之外，更严格地衡量重建泛化能力。该设定在 N3DV 和 MeetRoom 数据集上验证了方法的优势，但 VRU 数据集本身具有更大的视角跨度，侧视图设定在该数据集上的表现（PSNR 29.43）与 N3DV（26.30）的差异暗示场景运动幅度和视角外推难度之间存在交互效应，这一关系尚未被系统分析。

**实时性能的权衡。** 尽管方法在 FPS 指标上表现出色（N3DV 137 FPS, MeetRoom 154 FPS），这得益于准确的动静标签减少了冗余动态高斯数量，但4D掩码场和脉冲标记场的引入增加了训练阶段的参数量和计算开销。论文未报告训练时间对比，这一维度的缺失使得“训练-推理”效率的全貌尚不完整。

### 3. 开放的后续方向

**动静分解的鲁棒性边界。** 当场景中动态区域占据主导或静态纹理匮乏时，残差驱动的掩码场训练能否维持准确分解，是一个需要实验验证的问题。可能的改进方向包括引入运动先验或自监督一致性约束。

**训练视图色差的处理。** 针对色差破坏时空一致性的问题，可探索在掩码场训练中引入颜色不变性约束（如对光照变化鲁棒的特征空间残差），或采用联合优化曝光参数的策略。

**脉冲标记场的泛化能力。** 脉冲神经元的代理梯度设计（本文采用反正切函数）引入了超参数 $\beta$，其对不同场景的敏感性尚未被消融。探索自适应代理梯度或替代脉冲模型可能进一步降低调参负担。

**动静分解框架的扩展性。** 当前框架将动静分解用于高斯原语的属性解耦优化，该思路可推广至其他需要离散分配的动态场景表示任务，如语义高斯分割、多物体独立运动建模等。4D掩码场的时空一致性生成能力在这些场景中具有潜在复用价值。

## 原文 PDF

![[paperPDFs/CVPR_2026/Dynamic_Static_Decomposition_for_Novel_View_Synthesis_of_Dynamic_Scenes_with_Spiking_Neurons.pdf]]