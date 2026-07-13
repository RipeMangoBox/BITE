---
title: Streaming Diffusion Model for Fast Infrared and Visible Video Fusion
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/Streaming_Diffusion_Model_for_Fast_Infrared_and_Visible_Video_Fusion.pdf
project_link: null
code_link: "https://github.com/DandanYoung/SDMFusion"
aliases:
- SDMFIVVF
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/generative_models_diffusion
- topic/generative_models_diffusion/diffusion_image_video
core_operator: 采用一步采样的流式扩散模型，冻结预训练去噪U-Net的生成先验，引入记忆增强的时序聚合适配器（含光流对齐与门控交叉注意力）和时序一致性损失，实现高效的时间建模与高质量融合输出。
primary_logic: 通过将预训练扩散模型的生成先验融入一步采样框架，并在潜在空间中显式传播跨帧特征，解耦了高保真度与时间稳定性的矛盾，使模型仅需当前帧和紧凑记忆即可实时生成时空一致的融合视频。
claims:
- 在HDO、M3SVD、VTMOT、NOT-156四个基准数据集上，SDMFusion在SCD、VIF和mSSIM三项指标上全面超越所有对比方法（Table 1），尤其在VIF上提升显著。
- 消融实验（Table 2）表明：去除时序聚合适配器（w/o Adapter）和时序一致性损失（w/o TC loss）均导致SCD、VIF和mSSIM显著下降，验证了各部件的关键作用。
- 效率对比显示：SDMFusion的总推理时间比次优方法快1.42倍（Figure 9），且满足实时应用需求。
- 帧间差分可视化（Figure 4）和帧级指标曲线（Figure 5）证明SDMFusion能稳定生成背景一致、目标运动连贯的融合视频，无闪烁或鬼影。
---

# Streaming Diffusion Model for Fast Infrared and Visible Video Fusion

> [!tip] 核心洞察
> 通过将预训练扩散模型的生成先验融入一步采样框架，并在潜在空间中显式传播跨帧特征，解耦了高保真度与时间稳定性的矛盾，使模型仅需当前帧和紧凑记忆即可实时生成时空一致的融合视频。

| 字段 | 内容 |
|------|------|
| 中文题名 | 面向快速红外与可见光视频融合的流式扩散模型 |
| 英文题名 | Streaming Diffusion Model for Fast Infrared and Visible Video Fusion |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://openaccess.thecvf.com/content/CVPR2026/html/Liu_Streaming_Diffusion_Model_for_Fast_Infrared_and_Visible_Video_Fusion_CVPR_2026_paper.html) · [Code](https://github.com/DandanYoung/SDMFusion) |
| Topic | #topic/vision_multimodal_applications #topic/generative_models_diffusion #topic/generative_models_diffusion/diffusion_image_video |
| Method | SDMFusion |
| Dataset | HDO, M3SVD, VTMOT, NOT-156 |

> [!tip] 效果简介
> - HDO 上，VIF 0.794 vs 0.715 (CDDFuse) (+0.079)。
> - M3SVD 上，VIF 0.926 vs 0.866 (CDDFuse) (+0.060)。
> - VTMOT 上，VIF 1.026 vs 0.907 (CDDFuse) (+0.119)。

## 概要

### 问题背景

红外与可见光视频融合旨在将红外传感器捕获的热辐射信息与可见光传感器捕获的纹理细节整合为统一的视频序列，以增强全天候场景感知能力。然而，该任务面临两个核心挑战：**运动伪影**与**高推理延迟**。传统视频融合方法通常将视频帧独立处理，忽略了帧间的时间依赖性，导致融合结果出现闪烁、鬼影等时空不一致现象。另一方面，基于扩散模型的图像融合方法虽具备强大的生成能力，但其多步迭代去噪过程引入的延迟难以满足实时视频处理的需求。这两个瓶颈构成了视频融合从图像级方法向视频级方法迁移的关键障碍。

### 核心方法

本文提出**SDMFusion**——一种面向快速红外与可见光视频融合的流式扩散模型。其核心思路是将预训练扩散模型的生成先验融入一步采样框架，同时在潜在空间中显式建模跨帧时序动态。具体而言：

- **一步采样策略**：在固定扩散时间步上执行单步潜在残差校正，替代传统的多步迭代去噪，大幅降低推理延迟。
- **时序聚合适配器**：通过光流估计器预测帧间运动场，将上一帧的紧凑记忆特征对齐至当前帧，并利用门控交叉注意力机制有选择地聚合时序信息。
- **时序一致性损失**：基于光流形变与有效性掩码约束相邻帧融合结果的一致性，抑制时间维度上的闪烁与漂移。

该方法仅需当前帧、上一帧及紧凑记忆即可实时生成时空一致的融合视频，在生成质量与推理效率之间取得了优越平衡。

### 主要结果

在**HDO、M3SVD、VTMOT、NOT-156**四个基准数据集上的实验表明，SDMFusion在SCD、VIF和mSSIM三项指标上全面超越现有方法（Table 1），尤其在VIF指标上提升显著。消融实验（Table 2）验证了时序聚合适配器与时序一致性损失的关键作用。效率对比显示，SDMFusion的总推理时间比次优方法快**1.42倍**，满足实时应用需求。帧间差分可视化（Figure 4）和帧级指标曲线（Figure 5）进一步证明，该方法能稳定生成背景一致、目标运动连贯的融合视频，无闪烁或鬼影。

### 方法谱系与知识库定位

SDMFusion处于**图像融合、视频融合与扩散模型加速**的交叉地带。在图像融合领域，它与**CDDFuse**（Zhao et al., CVPR 2023）、**DDFM**（Zhao et al., ICCV 2023）等基于自编码器或扩散模型的方法形成对比——这些方法逐帧独立处理，缺乏时序建模能力。在视频融合领域，**RCVS**（Xie et al., TMM 2024）、**TemCoCo**（Gong et al., ICCV 2025）和**UniVF**（Zhao et al., NeurIPS 2025）等近期工作开始引入时序约束，但SDMFusion通过一步扩散采样与流式记忆传播，在效率与时空一致性上实现了显著突破。在扩散模型加速方面，该方法借鉴了一步生成的思想，但将其创造性地适配至视频融合场景，并通过冻结预训练U-Net保留生成先验，避免了从头训练的高昂成本。

### 红外与可见光视频融合的核心挑战

红外与可见光视频融合旨在将红外传感器捕获的热辐射信息与可见光相机记录的纹理细节进行互补整合，生成兼具全天候目标感知能力和丰富场景语义的融合视频。这一任务在视频监控、自动驾驶、军事侦察等下游应用中具有关键价值。然而，视频融合面临的本质困难远高于图像融合：**模型不仅需要在每一帧内实现高质量的跨模态信息融合，还必须维持帧间的时空一致性，避免闪烁、鬼影和背景抖动等时序伪影**（Figure 1 左）。

传统视频融合方法通常沿用图像融合的范式，将视频帧视为独立样本逐帧处理。这种策略忽略了相邻帧之间的时间依赖性，导致两个突出问题：其一，融合结果在时间轴上缺乏连贯性，表现为背景区域的亮度漂移和目标边缘的闪烁；其二，当场景中存在显著运动时，独立帧处理无法利用运动信息来对齐跨帧特征，容易产生运动模糊或重影。尽管部分方法尝试引入后处理时序平滑，但这类修补式方案并未从建模层面解决时间依赖性的缺失。

### 扩散模型在视频融合中的潜力与瓶颈

近年来，扩散模型（Diffusion Models）在图像生成和图像融合任务中展现出卓越的生成能力。以 **DDFM**（Zhao et al., ICCV 2023）、**Dif-Fusion**（Yue et al., TIP 2023）和 **Text-DiFuse**（Zhang et al., NeurIPS 2024）为代表的扩散融合方法，通过逐步去噪过程将红外与可见光信息注入生成空间，取得了领先的图像融合质量。这些方法的核心优势在于预训练扩散模型蕴含的强生成先验，能够有效恢复高频纹理并保持语义结构。

然而，将扩散模型直接迁移到视频融合面临一个根本性瓶颈：**推理延迟**。标准扩散模型的采样过程需要数十乃至上百步迭代去噪，每一步都涉及完整的U-Net前向传播。以单帧推理时间约0.5秒的典型扩散融合模型计算，处理一段30秒、30fps的视频需要约450秒，远超实时性要求。这使得扩散模型在视频融合中的实际部署几乎不可行。因此，如何将扩散模型的生成能力与视频处理的实时性需求统一起来，是该方向的核心矛盾。

### 现有视频融合方法的局限

除扩散模型外，现有的视频融合方法大致可分为两类。第一类是基于图像融合架构的直接扩展，如 **CDDFuse**（Zhao et al., CVPR 2023）和 **DCEvo**（Liu et al., CVPR 2025），它们在单帧融合质量上表现优异，但因缺乏时序建模机制，在视频场景下容易产生帧间不一致。第二类是专门设计的视频融合方法，如 **RCVS**（Xie et al., TMM 2024）、**TemCoCo**（Gong et al., ICCV 2025）和 **UniVF**（Zhao et al., NeurIPS 2025），它们在一定程度上引入了时序约束或特征传播机制。但这类方法通常依赖复杂的循环结构或3D卷积，计算开销较大，且在高动态场景下的时序稳定性仍有提升空间。

### 本文的核心动机与思路

针对上述挑战，本文的核心动机是：**是否能够在保留扩散模型生成先验的同时，通过一步采样实现实时推理，并显式建模跨帧时间依赖性？**

基于这一动机，本文提出 **SDMFusion**（Streaming Diffusion Model for Infrared and Visible Video Fusion），其核心洞察在于：将预训练扩散模型的生成先验融入一步采样框架，并在潜在空间中通过流式记忆机制传播跨帧特征，从而解耦高保真度与时间稳定性的矛盾。具体而言，该方法仅需当前帧、上一帧和紧凑的记忆先验即可生成时空一致的融合视频，无需访问完整历史序列，天然适配流式处理场景。这一设计同时解决了扩散模型的高延迟问题和传统方法的时序不一致问题，为实时视频融合提供了新的技术路径。

## 核心方法与创新机理

SDMFusion 的核心创新在于通过**一步采样的流式扩散模型**，将预训练扩散模型的生成先验引入视频融合任务，同时显式建模时序依赖性，解决了传统方法中高保真度与时间稳定性之间的矛盾。其关键创新点可归纳为以下四个维度：

### 1. 一步残差校正替代多步迭代采样

传统扩散模型（如 DDPM/DDIM）依赖多步迭代去噪，推理延迟高，难以满足实时视频处理需求。SDMFusion 提出**固定扩散时间的一步潜在残差校正**策略（Eq.4），将多步采样压缩为单步更新：

$$\mathbf{z}_{\mathrm{y}} = \frac{\mathbf{z}_{\mathrm{x}} - \sqrt{1 - \bar{\alpha}_{\hat{\mathrm{t}}}} \mathbf{r}_{\mathrm{t}}}{\sqrt{\bar{\alpha}_{\hat{\mathrm{t}}}}}$$

该公式在潜在空间中直接对输入特征 $\mathbf{z}_{\mathrm{x}}$ 进行残差校正，利用预训练 U-Net 预测的残差 $\mathbf{r}_{\mathrm{t}}$ 在固定时间步 $\hat{\mathrm{t}}$ 完成一步生成。这一设计**解耦了生成质量与推理延迟**：冻结的 U-Net 保留了强大的生成先验，而一步采样将推理时间压缩至接近前馈网络水平。消融实验表明，替换为多步采样虽能带来有限的融合质量提升，但推理耗时大幅增加，验证了一步策略在实时性与质量间的优越平衡（Section 5.5, Figure 9）。

### 2. 流式记忆增强时序聚合适配器

逐帧独立处理是现有视频融合方法产生闪烁与运动伪影的根本原因。SDMFusion 提出**流式记忆增强时序聚合适配器**，仅需当前帧、上一帧和紧凑记忆即可实现跨帧特征传播，核心包含三个协同机制：

- **光流对齐记忆**：利用光流估计器预测帧间运动场 $\mathbf{O}_{t-1 \to t}$，将上一帧的记忆特征形变至当前帧坐标，消除运动偏移。
- **门控交叉注意力**：基于当前特征与对齐记忆的拼接，学习门控系数 $\gamma^{(k)}$（Eq.5），调制时序交互强度：

  $$\gamma^{(k)} = \sigma(\phi_g^{(k)}(\mathrm{Cat}(\mathbf{F}_{\mathrm{t}}^{(k)}, \tilde{\mathbf{F}}_{\mathrm{t-1}\to\mathrm{t}}^{(k)})))$$

  随后通过门控交叉注意力（Eq.6）允许当前帧有选择地从运动补偿后的记忆中汲取互补信息：

  $$\mathbf{A}^{(k)} = \mathrm{Softmax}\left(\frac{(\mathbf{Q}^{(k)} \odot \gamma^{(k)})(\mathbf{K}^{(k)} \odot \gamma^{(k)})^{\top}}{\sqrt{C}}\right)$$

- **残差聚合**：以残差形式将注意力加权记忆叠加到当前特征上（Eq.7），减少信息丢失：

  $$\hat{\mathbf{F}}_{\mathrm{t}}^{(k)} = \mathbf{F}_{\mathrm{t}}^{(k)} + \mathbf{A}^{(k)} \mathbf{V}^{(k)}$$

该适配器插入 U-Net 解码层后，使模型在保持单帧生成质量的同时，显式传播跨帧特征。消融实验（Table 2, Figure 6）证实，移除适配器（w/o Adapter）后 SCD、VIF 和 mSSIM 均显著下降，且视觉上出现更多运动伪影。

### 3. 时序一致性损失显式约束帧间稳定性

现有融合方法通常仅包含重建与融合损失，缺乏显式的时序约束。SDMFusion 引入**时序一致性损失** $\mathcal{L}_{\mathrm{tc}}$，利用光流形变与有效性掩码 $\mathbf{M}_t$，约束相邻帧融合结果在时间上的一致性：

$$\mathcal{L}_{\mathrm{tc}} = \frac{1}{T-1} \sum_{t=2}^{T} \frac{\|(\hat{\mathbf{Y}}_t - \mathcal{W}(\hat{\mathbf{Y}}_{t-1}, \mathbf{O}_{t-1\to t})) \odot \mathbf{M}_t\|_1}{\sum \mathbf{M}_t + \varepsilon}$$

该损失直接惩罚形变后相邻帧的差异，有效抑制闪烁与漂移。去除该损失（w/o TC loss）会导致帧间闪烁加重（Section 5.4, Figure 4），验证了其在时间维度上的稳定作用。

### 4. 任务自适应潜在空间编码

标准扩散模型使用的 VAE 仅在可见光域训练，其潜在分布与红外-可见光融合任务存在偏差。SDMFusion 采用**任务自适应编码器-解码器**（DCEvo 风格设计），在 Stage I 中针对融合任务联合训练跨模态编码器，将红外与可见光特征压缩至适配融合的潜在空间。这一设计消除了域偏移，为后续流式扩散模型提供了更优的初始潜在表示（Section 4.1）。

综上，SDMFusion 通过上述四个 changed slots 的系统性创新，在保持扩散模型高保真生成能力的同时，实现了视频融合的时空一致性与实时推理效率，在 HDO、M3SVD、VTMOT、NOT-156 四个基准数据集上全面超越现有方法（Table 1）。

SDMFusion 采用两阶段训练范式，将图像级融合先验与流式时序建模解耦，最终实现高效、时空一致的红外与可见光视频融合。整体流程如 Figure 2 所示。

![[assets/figures/papers/paper_list_l2074_https_openaccess_thecvf_com_content_CVPR2026_html_Liu_Streaming_Diffusio/figures/002_Figure_2.jpg]]
*Figure 2: Overall pipeline of the proposed SDMFusion. Stage I trains the image-level fusion backbone, while Stage II introduces the streaming diffusion model with memory update temporal aggregation adapter to produce temporally coherent fused videos efficiently*

**Stage I：图像级融合主干训练。** 首先在静态红外-可见光图像对上训练一个跨模态编码器-解码器。该阶段采用 DCEvo 风格的任务自适应编解码器，替代标准 VAE，以解决可见光域预训练 VAE 与融合潜在空间之间的分布偏移问题。编码器将红外帧 $\mathbf{I}_t$ 与可见光帧 $\mathbf{V}_t$ 压缩至潜在表示，解码器负责将精炼特征重建为融合帧。此阶段仅优化重建保真度与融合质量，不涉及时序信息。

**Stage II：流式扩散模型与时序聚合适配器。** 冻结 Stage I 的主干网络，引入流式扩散模型（Streaming Diffusion Model, SDM）进行潜在空间的一步残差校正。核心操作是将预训练扩散模型的生成先验融入固定扩散时间 $\hat{t}$ 的一步采样框架，其潜在更新公式为：

$$\mathbf{z}_{\mathrm{y}} = \frac{\mathbf{z}_{\mathrm{x}} - \sqrt{1 - \bar{\alpha}_{\hat{\mathrm{t}}}} \mathbf{r}_{\mathrm{t}}}{\sqrt{\bar{\alpha}_{\hat{\mathrm{t}}}}}$$

该公式替代了传统多步迭代去噪，大幅降低推理延迟。

为赋予模型时序感知能力，在 U-Net 解码层后插入**时序聚合适配器**。该适配器包含三个关键子模块：

1. **光流估计器**：预测相邻帧间的运动场 $\mathbf{O}_{t-1 \to t}$，用于将上一帧的记忆特征形变对齐到当前帧。
2. **记忆更新模块**：保留紧凑的跨帧记忆先验，经光流形变后得到 $\tilde{\mathbf{F}}_{t-1 \to t}^{(k)}$，与当前帧特征 $\mathbf{F}_t^{(k)}$ 拼接，通过可学习的门控机制 $\gamma^{(k)} = \sigma(\phi_g^{(k)}(\mathrm{Cat}(\mathbf{F}_t^{(k)}, \tilde{\mathbf{F}}_{t-1 \to t}^{(k)})))$ 调制时序交互强度。
3. **门控交叉注意力**：以门控系数调制 Query 和 Key，计算注意力权重 $\mathbf{A}^{(k)}$，并通过残差聚合 $\hat{\mathbf{F}}_t^{(k)} = \mathbf{F}_t^{(k)} + \mathbf{A}^{(k)} \mathbf{V}^{(k)}$ 将记忆信息注入当前特征。

整个流式框架仅需当前帧、上一帧及紧凑记忆即可运行，无需缓存完整历史序列。

**损失函数设计。** 训练目标由四项损失加权组合：模态重建损失 $\mathcal{L}_{\mathrm{V,I}}$（MSE + SSIM）、融合损失 $\mathcal{L}_{\mathrm{fus}}$（强度与梯度最大值保真）、解码器正则化损失 $\mathcal{L}_{\mathrm{deco}}$，以及关键的**时序一致性损失** $\mathcal{L}_{\mathrm{tc}}$。后者利用光流形变与有效性掩码 $\mathbf{M}_t$，对相邻帧融合结果施加 L1 约束，显式抑制帧间闪烁与漂移。

**输入输出流。** 输入为对齐的红外-可见光视频帧对 $\{(\mathbf{I}_t, \mathbf{V}_t)\}_{t=1}^T$，经双分支编码器提取跨模态特征后进入流式扩散模型进行一步潜在校正，再通过时序适配器融入历史记忆，最终由图像解码器输出时空一致的融合视频序列 $\{\hat{\mathbf{Y}}_t\}_{t=1}^T$。

### 两阶段训练框架

SDMFusion 采用两阶段设计以解耦图像级融合质量与时序一致性学习。**Stage I** 在静态红外-可见光图像对上训练跨模态编码器-解码器主干网络，学习将双模态输入压缩至潜在空间并重建为高质量融合图像。**Stage II** 冻结该主干网络，引入流式扩散模型与记忆增强的时序聚合适配器，在潜在空间中显式建模跨帧依赖关系。

### 任务自适应潜在空间编码

传统扩散模型依赖在可见光图像上预训练的标准 VAE，其潜在分布与融合任务存在显著偏移。SDMFusion 将其替换为**任务自适应编码器-解码器**，采用 DCEvo 风格设计（Liu et al., CVPR 2025）进行域适配，使编码器能更准确地压缩红外与可见光的跨模态特征，解码器则从潜在表示重建融合帧。

### 一步潜在残差校正

扩散模型的迭代去噪是推理延迟的核心瓶颈。SDMFusion 将多步采样压缩为**固定扩散时间的一步残差校正**：

$$\mathbf{z}_{\mathrm{y}} = \frac{\mathbf{z}_{\mathrm{x}} - \sqrt{1 - \bar{\alpha}_{\hat{\mathrm{t}}}} \mathbf{r}_{\mathrm{t}}}{\sqrt{\bar{\alpha}_{\hat{\mathrm{t}}}}}$$

其中 $\mathbf{z}_{\mathrm{x}}$ 为编码器输出的初始潜在特征，$\mathbf{r}_{\mathrm{t}}$ 为预训练 U-Net 在固定时间步 $\hat{\mathrm{t}}$ 预测的残差，$\bar{\alpha}_{\hat{\mathrm{t}}}$ 为噪声调度参数。该公式将去噪过程转化为对初始潜在特征的直接校正，仅需一次 U-Net 前向传播即可完成生成，推理延迟大幅降低。

### 流式记忆增强时序聚合适配器

为在一步采样框架中注入时序信息，SDMFusion 设计了**流式记忆增强时序聚合适配器**，仅需当前帧、上一帧及紧凑记忆先验即可运行。适配器插入 U-Net 各解码层后，包含三个核心组件：

**光流对齐。** 光流估计器预测相邻帧间的运动场 $\mathbf{O}_{t-1 \to t}$，将上一帧的记忆特征 $\mathbf{F}_{t-1}^{(k)}$ 形变至当前帧坐标：

$$\tilde{\mathbf{F}}_{t-1 \to t}^{(k)} = \mathcal{W}(\mathbf{F}_{t-1}^{(k)}, \mathbf{O}_{t-1 \to t})$$

**门控交叉注意力。** 将当前帧特征 $\mathbf{F}_{t}^{(k)}$ 与对齐后的记忆特征拼接，学习门控系数以调制时序交互强度：

$$\gamma^{(k)} = \sigma(\phi_g^{(k)}(\mathrm{Cat}(\mathbf{F}_{\mathrm{t}}^{(k)}, \tilde{\mathbf{F}}_{\mathrm{t-1}\to\mathrm{t}}^{(k)})))$$

随后通过门控交叉注意力，允许当前帧有选择地从运动补偿后的记忆中汲取互补信息：

$$\mathbf{A}^{(k)} = \mathrm{Softmax}\left(\frac{(\mathbf{Q}^{(k)} \odot \gamma^{(k)})(\mathbf{K}^{(k)} \odot \gamma^{(k)})^{\top}}{\sqrt{C}}\right)$$

**残差聚合。** 将注意力加权后的记忆特征以残差形式叠加到当前特征上，减少信息丢失：

$$\hat{\mathbf{F}}_{\mathrm{t}}^{(k)} = \mathbf{F}_{\mathrm{t}}^{(k)} + \mathbf{A}^{(k)} \mathbf{V}^{(k)}$$

聚合后的特征传入解码器重建融合帧，同时更新记忆先验供下一帧使用。

### 时序一致性损失

为显式抑制帧间闪烁与漂移，SDMFusion 引入**时序一致性损失**，利用光流形变与有效性掩码约束相邻帧融合结果：

$$\mathcal{L}_{\mathrm{tc}} = \frac{1}{T-1} \sum_{t=2}^{T} \frac{\|(\hat{\mathbf{Y}}_t - \mathcal{W}(\hat{\mathbf{Y}}_{t-1}, \mathbf{O}_{t-1\to t})) \odot \mathbf{M}_t\|_1}{\sum \mathbf{M}_t + \varepsilon}$$

其中 $\hat{\mathbf{Y}}_t$ 为第 $t$ 帧融合结果，$\mathcal{W}$ 为光流形变操作，$\mathbf{M}_t$ 为遮挡掩码，$\varepsilon$ 防止除零。该损失惩罚形变对齐后相邻帧间的像素差异，有效抑制时间维度上的不稳定性。

### 整体训练目标

完整训练目标由四部分加权组合：

$$\mathcal{L}_{\mathrm{total}} = \lambda_{\mathrm{V,I}} \mathcal{L}_{\mathrm{V,I}} + \lambda_{\mathrm{fus}} \mathcal{L}_{\mathrm{fus}} + \lambda_{\mathrm{deco}} \mathcal{L}_{\mathrm{deco}} + \lambda_{\mathrm{tc}} \mathcal{L}_{\mathrm{tc}}$$

其中 $\mathcal{L}_{\mathrm{V,I}}$ 为模态重建损失（MSE + SSIM），$\mathcal{L}_{\mathrm{fus}}$ 为结构与梯度保持融合损失，$\mathcal{L}_{\mathrm{deco}}$ 为解码器重建损失。各损失项的具体权重需参考原文实验配置。

## 实验与关键发现

### 5.1 实验设置

SDMFusion在四个公开的红外与可见光视频融合基准数据集上进行评估：**HDO**、**M3SVD**、**VTMOT**和**NOT-156**。所有对比方法均在相同数据集上重新训练或使用官方开源代码与模型，确保比较公平。所有实验在单张NVIDIA RTX 5090 GPU上完成，并报告平均结果。

训练采用两阶段策略：Stage I在静态图像对上训练跨模态编码器-解码器，batch size设为12；Stage II冻结backbone并引入流式扩散模型，batch size为1，序列长度为6。网络参数使用AdamW优化器，初始学习率为$1 \times 10^{-4}$，采用余弦退火调度衰减至$1 \times 10^{-5}$。

### 5.2 主要量化结果

Table 1展示了在四个数据集上的全面量化对比。SDMFusion在**SCD**（结构一致性）、**VIF**（视觉信息保真度）和**mSSIM**（多尺度结构相似性）三项核心指标上全面超越所有对比方法。

在**HDO**数据集上，SDMFusion的VIF达到**0.794**，相比次优方法CDDFuse（Zhao et al., CVPR 2023）的0.715提升了**+0.079**；在**M3SVD**上，VIF为**0.926**，领先CDDFuse的0.866达**+0.060**；在**VTMOT**上，VIF达到**1.026**，较CDDFuse的0.907提升**+0.119**。这些结果表明，SDMFusion在保留红外热辐射信息和可见光纹理细节方面具有显著优势。

值得注意的是，与同为扩散模型基线的**DDFM**（Zhao et al., ICCV 2023）和**Text-DiFuse**（Zhang et al., NeurIPS 2024）相比，SDMFusion在所有指标上均取得更优结果，验证了一步采样策略在视频融合场景下相比多步迭代去噪的优越性。与视频融合专用方法**RCVS**（Xie et al., TMM 2024）、**TemCoCo**（Gong et al., ICCV 2025）和**UniVF**（Zhao et al., NeurIPS 2025）相比，SDMFusion同样全面领先，证明流式扩散框架在时序建模上的有效性。

### 5.3 定性分析

Figure 3展示了四个数据集上的定性对比结果。SDMFusion生成的融合视频展现出**背景一致性**和**目标运动连贯性**两个关键优势：红外模态中的热目标（如行人、车辆）被完整保留并融入可见光背景中，且跨帧之间无明显闪烁或鬼影。相比之下，逐帧独立处理的图像融合方法（如CDDFuse、LRRNet）在运动区域出现明显的纹理漂移和伪影。

Figure 4通过帧间差分可视化进一步验证了时间一致性。SDMFusion的帧间差分图在静态背景区域几乎为零，仅在运动目标边界处有微弱响应，表明背景高度稳定。而去除时序一致性损失的变体（w/o TC loss）在背景区域出现显著的差分噪声，证实了$\mathcal{L}_{\mathrm{tc}}$对抑制帧间闪烁的核心作用。

Figure 5的帧级指标曲线显示，SDMFusion在整个视频序列上保持稳定的高质量输出，SCD、VIF和mSSIM曲线波动明显小于对比方法，尤其在场景切换或大运动帧处未出现性能骤降。

### 5.4 消融实验

Table 2和Figure 6、Figure 7报告了消融实验的量化与定性结果，验证了各核心组件的贡献：

- **去除时序聚合适配器（w/o Adapter）**：在M3SVD和VTMOT数据集上，SCD、VIF和mSSIM均显著下降。Figure 6显示该变体在运动区域出现明显的纹理撕裂和伪影，证明光流对齐与门控交叉注意力机制对跨帧特征传播不可或缺。
- **去除时序一致性损失（w/o TC loss）**：指标下降幅度略小于去除适配器，但Figure 4的帧间差分可视化显示背景闪烁明显加重，表明$\mathcal{L}_{\mathrm{tc}}$在约束时间稳定性方面发挥关键作用。
- **替换一步采样为多步采样**：推理耗时大幅增加（见Section 5.5），而融合质量提升有限，验证了一步策略在实时性与质量间的优越平衡。

Figure 7的小提琴图展示了消融变体在HDO和NOT-156数据集上的指标分布。完整SDMFusion的分布更集中且中位数更高，表明其性能稳定且鲁棒。

### 5.5 效率分析

Figure 9的效率对比显示，SDMFusion的总推理时间比次优方法快**1.42倍**，满足实时应用需求。这一效率优势源于两个设计选择：（1）一步潜在残差校正替代多步迭代采样，将扩散模型的推理延迟压缩至单步前向传播级别；（2）流式框架仅需当前帧和紧凑记忆，避免了批量处理多帧带来的计算冗余。

### 5.6 下游任务验证

Table 3报告了在NOT-156数据集上的目标跟踪下游任务评估结果。SDMFusion作为融合前端时，跟踪器取得**0.3799**的AUC，优于所有对比融合方法。Figure 8的定性跟踪结果显示，SDMFusion融合视频中的热目标轮廓清晰、位置稳定，使跟踪器在遮挡和复杂背景下保持准确锁定。这验证了SDMFusion生成的融合视频不仅视觉质量高，且对下游视觉任务具有实际增益。

### 5.7 局限性与待验证问题

尽管SDMFusion在多个基准上取得最优结果，以下问题仍需进一步验证：

1. **光流估计的鲁棒性**：当光流估计在极端光照或大运动下失效时，模型的鲁棒性如何？是否需要更鲁棒的运动估计替代方案？
2. **多模态扩展**：该方法能否自然地扩展到超过两模态（如同时融合红外、可见光、事件相机等）的视频融合场景？
3. **移动端部署**：是否有更高效的记忆压缩或注意力机制，以进一步降低计算开销，适应移动端部署？

![[assets/figures/papers/paper_list_l2074_https_openaccess_thecvf_com_content_CVPR2026_html_Liu_Streaming_Diffusio/figures/003_Table_1.jpg]]
*Table 1: Quantitative comparison with state-of-the-art fusion approaches on the HDO, VTMOT, NOT-156, and M3SVD datasets. Red highlights the best performance, while green denotes the second-best results*

![[assets/figures/papers/paper_list_l2074_https_openaccess_thecvf_com_content_CVPR2026_html_Liu_Streaming_Diffusio/figures/009_Table_2.jpg]]
*Table 2: Quantitative results of ablation study on the M3SVD and VTMOT datasets. Bold values indicate the best performance*

![[assets/figures/papers/paper_list_l2074_https_openaccess_thecvf_com_content_CVPR2026_html_Liu_Streaming_Diffusio/figures/012_Table_3.jpg]]
*Table 3: Quantitative comparison on tracking task across different fusion methods on the NOT-156 dataset*

![[assets/figures/papers/paper_list_l2074_https_openaccess_thecvf_com_content_CVPR2026_html_Liu_Streaming_Diffusio/figures/008_Figure_7.jpg]]
*Figure 7: Violin plots of SCD, VIF, and mSSIM for different ablation variants on the HDO (top) and NOT-156 (bottom) datasets*

![[assets/figures/papers/paper_list_l2074_https_openaccess_thecvf_com_content_CVPR2026_html_Liu_Streaming_Diffusio/figures/010_Figure_8.jpg]]
*Figure 8: Qualitative tracking results on the NOT-156 dataset*

## 定位与知识库关联

### 1. 方法关系图谱

SDMFusion 处于**图像融合扩散模型**与**视频时序建模**两条技术路线的交汇点，其核心贡献在于将二者解耦并协同，而非简单叠加。

**与图像级融合方法的关系。** 该方法的第一阶段（Stage I）直接继承了近期图像融合的前沿设计。其任务自适应编码器-解码器采用了 **DCEvo**（Liu et al., CVPR 2025）风格的域适应策略，以解决标准 VAE 仅在可见光域预训练导致的潜在空间分布偏移问题。在损失函数层面，融合损失 $\mathcal{L}_{\mathrm{fus}}$ 中的强度与梯度最大值保留机制，与 **CDDFuse**（Zhao et al., CVPR 2023）等主流图像融合方法的保真度约束一脉相承。然而，SDMFusion 将这些图像级组件视为可冻结的生成先验骨干，而非最终方案——这使其与 **DDFM**（Zhao et al., ICCV 2023）、**Dif-Fusion**（Yue et al., TIP 2023）、**Text-DiFuse**（Zhang et al., NeurIPS 2024）、**Mask-DiFuser**（Tang et al., TPAMI 2025）等纯图像扩散融合方法形成了根本性分叉：后者逐帧独立推理，完全忽略了时间轴上的信息冗余与动态依赖性。

**与视频融合方法的关系。** 现有视频融合方法 **RCVS**（Xie et al., TMM 2024）、**TemCoCo**（Gong et al., ICCV 2025）、**UniVF**（Zhao et al., NeurIPS 2025）均试图引入时序建模，但通常采用循环网络或 3D 卷积等隐式时序聚合方式，且未利用扩散模型的强生成先验。SDMFusion 的差异化在于：它将时序建模显式化为一个**即插即用的流式记忆聚合适配器**，通过光流对齐与门控交叉注意力在潜在空间中传播跨帧特征。这种设计使得时序模块与生成骨干完全解耦，既保留了预训练扩散模型的高保真度，又获得了显式可控的时间一致性。

**与扩散模型加速工作的关系。** 在采样策略上，SDMFusion 采用固定扩散时间的一步残差校正（Eq. 4），替代了传统的多步 DDPM/DDIM 迭代。这与一致性模型、渐进式蒸馏等扩散加速范式的目标一致，但 SDMFusion 的独特之处在于：它并非追求通用加速，而是针对视频融合任务，将节省的算力重新分配给时序聚合模块，实现了“质量-速度-一致性”的三元平衡。

### 2. 适用边界与局限

尽管 SDMFusion 在四个基准数据集上取得了全面领先，其设计隐含了若干适用边界：

- **光流依赖瓶颈。** 时序聚合适配器的核心操作依赖于光流估计器对帧间运动场的准确预测。当面临极端光照（如红外模态饱和）、大尺度运动遮挡或低纹理区域时，光流质量可能显著退化，进而导致记忆对齐失效、门控注意力引入噪声。论文未报告在此类退化场景下的鲁棒性评估，该点需要人工验证。
- **模态数量扩展性存疑。** 当前框架的双分支编码器和记忆模块专为红外-可见光双模态设计。虽然门控交叉注意力机制理论上可扩展至更多模态，但记忆容量、对齐复杂度与计算开销将呈超线性增长。论文将此列为开放问题，尚无实验支持。
- **实时性边界未明确。** 尽管 Figure 9 显示总推理时间比次优方法快 1.42 倍，但该测量基于单张 NVIDIA RTX 5090 GPU。在边缘设备或 CPU 环境下的延迟表现未经验证，移动端部署的可行性仍待探索。

### 3. 开放问题与后续方向

结合论文自身的讨论与方法设计的潜在延伸空间，以下方向值得关注：

1. **鲁棒运动估计替代方案。** 当光流失效时，是否可采用基于相关体的特征匹配（如 RAFT 风格的 4D 代价体）或可学习的运动隐式表示来替代显式光流对齐？这直接关系到方法在无人机航拍、夜间监控等挑战性场景中的实用性。
2. **多模态扩展与记忆压缩。** 如何将双模态框架推广至红外-可见光-事件相机等多源视频融合？同时，当前记忆模块存储完整潜在特征，是否存在更高效的记忆压缩策略（如动态稀疏记忆或分层记忆）以降低计算开销？
3. **时序一致性的理论刻画。** 当前方法通过时序一致性损失 $\mathcal{L}_{\mathrm{tc}}$ 在像素空间施加 L1 约束，这是一种启发式设计。是否存在更本质的时序一致性度量（如频域相位一致性或运动轨迹约束），可以进一步抑制长程漂移？
4. **下游任务的闭环优化。** Table 3 显示 SDMFusion 在目标跟踪任务上取得了最优 AUC（0.3799），但融合模型并未针对跟踪任务进行端到端优化。将下游任务反馈信号纳入融合训练（如检测置信度引导的注意力调制），可能进一步释放“融合-感知”协同的潜力。

## 原文 PDF

![[paperPDFs/CVPR_2026/Streaming_Diffusion_Model_for_Fast_Infrared_and_Visible_Video_Fusion.pdf]]
