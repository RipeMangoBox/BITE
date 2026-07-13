---
title: "Iris: Integrating Language into Diffusion-based Monocular Depth Estimation"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/Iris_Integrating_Language_into_Diffusion_based_Monocular_Depth_Estimation.pdf
project_link: null
code_link: null
aliases:
- Iris
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
- topic/generative_models_diffusion
core_operator: 将场景的语言描述作为额外条件输入扩散去噪过程。文字提供物体存在性、类别、大小、空间关系和场景结构等先验，约束深度解空间，使模型在推理时能有效消除视觉模糊。
primary_logic: 文本到图像预训练的扩散模型已隐式学习到与语言描述一致的三维场景结构；通过在图像-文本-深度三元组上微调，可将这种隐式先验转化为显式的深度估计能力，显著改善对微小、模糊或遮挡区域的感知，并加速训练和推理收敛。
claims:
- 在Marigold、Lotus和E2E-FT三种扩散模型上，加入文本条件后在五个真实数据集上的AbsRel和δ1普遍提升（如NYUv2 AbsRel 6.1→5.9，KITTI AbsRel 10.7→10.4），且训练和推理收敛速度明显加快。
- 语言描述使模型对面积占比小于5%的小区域深度估计显著优于基线，证明语言能补充视觉在微小模糊区域的不足。
- 加入文本后，扩散模型仅需10步去噪即可收敛，而基线需要25步，表示语言作为约束加速了扩散轨迹。
- NYUv2 上 AbsRel ↓ = 5.9 (Marigold + Text Train&Infer)
---

# Iris: Integrating Language into Diffusion-based Monocular Depth Estimation

> [!tip] 核心洞察
> 文本到图像预训练的扩散模型已隐式学习到与语言描述一致的三维场景结构；通过在图像-文本-深度三元组上微调，可将这种隐式先验转化为显式的深度估计能力，显著改善对微小、模糊或遮挡区域的感知，并加速训练和推理收敛。

| 字段 | 内容 |
|------|------|
| 中文题名 | Iris：将语言融入基于扩散的单目深度估计 |
| 英文题名 | Iris: Integrating Language into Diffusion-based Monocular Depth Estimation |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2411.16750) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction #topic/generative_models_diffusion |
| Method | Iris（将语言描述融入扩散深度估计的通用策略） |
| Dataset | NYUv2, KITTI, ETH3D, ScanNet |

> [!tip] 效果简介
> - NYUv2 上，AbsRel ↓ 5.9 (Marigold + Text Train&Infer) vs 6.1 (Marigold* 无文本) (-0.2)。
> - KITTI 上，AbsRel ↓ 10.4 (Marigold + Text Train&Infer) vs 10.7 (Marigold* 无文本) (-0.3)。
> - ETH3D 上，AbsRel ↓ 6.5 (Marigold + Text Train&Infer) vs 6.9 (Marigold* 无文本) (-0.4)。

## 概要

单目深度估计是三维视觉的基础任务，但纯视觉方法长期受困于**纹理歧义、可见性歧义和光照干扰**——同一张二维图像可能对应多种截然不同的三维场景，尤其在小目标、遮挡或与背景纹理相似的区域，视觉信号本身难以提供足够的约束来消除模糊。

本文提出 **Iris**，一种将**语言描述**作为额外条件融入扩散模型深度估计的通用策略。其核心洞见在于：文本到图像预训练的扩散模型已经隐式地学习到了与语言描述一致的三维场景结构（物体大小、形状、空间关系与场景布局）；通过在图像-文本-深度三元组上微调，可以将这种隐式先验转化为显式的深度估计能力。语言提供的物体存在性、类别、尺度与空间关系等先验，有效约束了深度解空间，显著改善了对微小、模糊或遮挡区域的感知。

方法层面，Iris 在现有扩散深度估计基线（**Marigold**、**Lotus**、**E2E-FT**）上仅做一处关键改动：将冻结 CLIP 文本编码器编码的场景描述向量与图像潜变量、噪声深度潜变量一并输入去噪 U-Net，使扩散过程同时以图像和语言为条件。这一改动保持了原有扩散框架的完整性，具有即插即用的通用性。

实验证据支撑以下核心结论：
- **精度普遍提升**：在 Marigold、Lotus 和 E2E-FT 三种基线上加入文本条件后，NYUv2、KITTI、ETH3D、ScanNet、DIODE 五个真实数据集的 AbsRel 和 δ1 指标一致改善（如 NYUv2 AbsRel 6.1→5.9，KITTI AbsRel 10.7→10.4），详见 Table 1。
- **小区域感知显著增强**：对面积占比小于 5% 的区域，语言条件下的深度估计明显优于纯视觉基线（Table 2），证明语言能弥补视觉在微小模糊区域的不足。
- **训练与推理加速收敛**：加入文本后，扩散模型仅需约 10 步 DDIM 去噪即可达到基线 25 步的精度（Table 4, Figure 8），训练损失下降也更快（Figure 7），表明语言作为强约束加速了扩散轨迹的收敛。
- **对文本来源鲁棒，但对语义正确性敏感**：不同提示词生成的描述只要语义合理，性能保持可比（Table 3）；但错误描述（如将“书架”描述为“窗户”）会严重误导模型（Figure 9），证实模型确实利用了文本语义信息。

Iris 的局限性同样值得关注：训练依赖合成数据（HyperSim、Virtual KITTI），与真实场景存在域间隙；文本描述由视觉语言模型自动生成，可能引入噪声与幻觉；模型依赖预训练 Stable Diffusion 和 CLIP，计算开销较高；且仅在扩散式深度估计器上验证，向其他范式的推广尚未探索。

单目深度估计旨在从单张二维图像中恢复场景的三维几何结构，是自动驾驶、机器人导航和增强现实等应用的基础感知能力。然而，纯视觉方法面临一个根本性困境：**纹理歧义、可见性歧义和光照干扰**使得同一张二维图像可以对应无限多种三维场景。尤其在目标面积小、被遮挡或与背景纹理相似的区域，视觉信号本身难以提供足够的约束来唯一确定深度，导致现有方法在这些区域频繁失效。

近年来，基于扩散模型的深度估计方法（如 **Marigold**、**Lotus** 系列和 **E2E-FT**）展现了强大的生成先验优势。这些方法将深度估计建模为以图像为条件的去噪扩散过程，利用预训练扩散模型隐式学习到的三维结构先验来提升深度预测质量。然而，它们本质上仍然是**纯视觉驱动**的：条件信号仅来自图像本身，未能显式引入关于场景中物体类别、大小、空间关系和整体布局的高层语义先验。当图像中的视觉线索不足以区分前景与背景、或无法可靠地感知微小透明物体时，这些方法的解空间仍然过大，导致预测偏差。

Iris 的核心动机正是弥补这一缺口。**文本到图像预训练的扩散模型**在生成不同视角和布局下符合语言描述的图像时，已经被迫隐式建模了指定物体的尺寸、形状、空间关系及场景结构——这正是单目深度估计所稀缺的几何先验。Iris 提出将场景的语言描述作为额外条件注入扩散去噪过程，通过**图像-文本-深度三元组**的微调，将这种隐式先验转化为显式的深度估计能力。语言描述提供的物体存在性、类别、大小和空间关系等信息，能够有效约束深度解空间，使模型在推理时消除视觉模糊，尤其改善对微小、模糊或遮挡区域的感知（Figure 2）。此外，语言条件的引入还带来了训练和推理收敛速度的显著加快，使扩散模型仅需 10 步去噪即可达到与基线 25 步相当的精度（Figure 8）。

这一思路不仅是对现有扩散深度估计框架的自然扩展，更揭示了多模态融合在密集预测任务中的潜力：语言不再仅仅是高层语义的载体，而是可以直接参与低层几何推理的约束信号。

## 核心方法与创新机理

Iris的核心创新在于将**场景的语言描述作为额外条件**注入扩散模型的去噪过程，从而将文本到图像预训练中隐式习得的三维场景先验显式化为深度估计能力。这一策略的实质是**约束解空间**：纯视觉单目深度估计本质上是病态的——同一二维图像可对应多种三维场景，尤其在纹理歧义、遮挡、光照干扰或小目标区域，视觉信号不足以唯一确定深度。语言描述通过提供物体存在性、类别、大小、空间关系和场景结构等高层语义先验，有效缩小了从二维图像到三维深度的映射解空间。

### 条件模态的扩展

Iris对基线扩散深度估计框架的核心改动（changed slot）集中在一个维度：**条件模态从单一的图像潜变量扩展为图像潜变量与文本编码的联合条件**。

具体而言，基线方法（如**Marigold**、**Lotus**、**E2E-FT**）仅将VAE编码的图像潜变量 $E(x)$ 与噪声深度潜变量 $z_t$ 拼接后送入去噪U-Net。Iris在此基础上，额外拼接由**冻结CLIP文本编码器**编码的文本描述 $c$，使去噪U-Net的条件输入变为 $(z_t, E(x), c)$ 的三元组。这一改动的关键证据来自方法描述：“given a text caption $c$, we first encode it through a frozen CLIP text encoder, then feed it into the diffusion model. Given an image $x$, we encode it using the same VAE encoder $E(x)$ that encoded the depth map, concatenated with the depth latent $z_t$, then feed it into the diffusion model.”

训练目标随之调整为以图像和文本为联合条件的噪声预测损失：
$$\mathcal{L}(\theta) = \mathbb{E}_{y,\epsilon,t} \left[ \| \epsilon - \epsilon_\theta(\mathbf{z}_t, t, x, \mathbf{c}) \|^2 \right]$$

推理时的逆向去噪步也相应依赖文本条件：
$$\mathbf{z}_{t-1} = \frac{1}{\sqrt{\alpha_t}} \left( \mathbf{z}_t - \frac{1-\alpha_t}{\sqrt{1-\bar{\alpha}_t}} \epsilon_\theta(\mathbf{z}_t, t, x, \mathbf{c}) \right)$$

### 创新的深层机制

这一条件扩展之所以有效，其深层机制在于：**文本到图像预训练的扩散模型（Stable Diffusion v2）已经隐式建模了与语言描述一致的三维场景结构**。要在不同视角和布局下生成准确反映文本描述的图像，模型必须隐式学习指定物体的大小、形状、空间关系以及场景的整体结构。Iris通过在图像-文本-深度三元组上微调，将这种隐式的三维先验转化为显式的深度估计能力。去噪U-Net初始化自Stable Diffusion v2，冻结的CLIP文本编码器和VAE编解码器则保留了预训练知识，仅微调U-Net即可实现模态对齐。

### 创新带来的关键增益

这一创新带来的增益体现在三个层面：

1. **精度提升**：在Marigold、Lotus和E2E-FT三种扩散模型上，加入文本条件后在NYUv2、KITTI、ETH3D、ScanNet、DIODE五个真实数据集上的AbsRel和δ1普遍提升（如NYUv2 AbsRel从6.1降至5.9，KITTI从10.7降至10.4），详见Table 1。

2. **小区域感知增强**：语言描述使模型对面积占比小于5%的小区域深度估计显著优于基线（Table 2），证明语言能补充视觉在微小、模糊或遮挡区域的不足。

3. **推理加速**：加入文本后，扩散模型仅需10步DDIM去噪即可收敛，而基线需要25步（Figure 8, Table 4），表明语言作为约束加速了扩散轨迹的收敛。

### 与相关工作的区别

区别于传统的视觉-语言融合方法（通常在特征层面做跨模态注意力），Iris的创新在于**利用扩散模型预训练阶段已嵌入的语言-三维结构关联**，通过条件扩散的形式将语言直接作为去噪过程的引导信号。这不同于简单的多模态特征拼接，而是利用了扩散模型在文本到图像生成中习得的隐式三维理解能力。

Iris 的核心思想是将场景的语言描述作为额外条件，注入扩散模型的去噪过程，从而约束单目深度估计的解空间。整个框架由四个冻结或可训练的模块串联构成，形成“图像-文本-深度”三模态条件生成管道。

### 管道总览

管道如图 Figure 3 所示，分为训练和推理两个阶段，共享相同的模块拓扑：

![[assets/figures/papers/paper_list_l2526_https_arxiv_org_abs_2411_16750/figures/003_Figure_3.jpg]]
*Figure 3: Pipeline to integrate text. We train the diffusion model to predict the noise added into the noisy depth latent*

1. **潜空间编码**：输入图像 $x$ 和真值深度图 $y^*$ 分别通过冻结的 VAE 编码器 $E$ 映射到同一潜空间，得到图像潜变量 $E(x)$ 和深度潜变量 $z_y$。文本描述 $c$ 则通过冻结的 CLIP 文本编码器编码为条件向量。
2. **扩散过程**：对深度潜变量 $z_y$ 施加前向扩散，逐步添加高斯噪声得到 $z_t$。去噪 U-Net（初始化为 Stable Diffusion v2 的 U-Net）接收 $z_t$、时间步 $t$、图像潜变量 $E(x)$ 和文本条件 $c$，预测添加的噪声 $\epsilon_\theta(z_t, t, x, c)$。
3. **损失监督**：训练目标为最小化预测噪声与真实噪声的均方误差 $\mathcal{L}(\theta) = \mathbb{E}_{y,\epsilon,t} \left[ \| \epsilon - \epsilon_\theta(\mathbf{z}_t, t, x, \mathbf{c}) \|^2 \right]$，迫使模型学习以图像和文本为条件的去噪能力。
4. **逆向推理**：推理时从纯高斯噪声 $z_T$ 出发，迭代执行去噪步 $\mathbf{z}_{t-1} = \frac{1}{\sqrt{\alpha_t}} \left( \mathbf{z}_t - \frac{1-\alpha_t}{\sqrt{1-\bar{\alpha}_t}} \epsilon_\theta(\mathbf{z}_t, t, x, \mathbf{c}) \right)$，得到纯净深度潜变量 $z_0$。
5. **深度解码**：$z_0$ 通过冻结的 VAE 解码器 $D$ 解码为最终深度预测 $\hat{y} = D(z_0)$。

### 模块分工与数据流

| 模块 | 角色 | 是否训练 | 输入 | 输出 |
|------|------|----------|------|------|
| VAE 编码器 $E$ | 将图像和深度图编码到共享潜空间 | 冻结 | 图像 $x$ / 深度 $y^*$ | 图像潜变量 $E(x)$ / 深度潜变量 $z_y$ |
| CLIP 文本编码器 | 将文本描述编码为条件向量 | 冻结 | 文本 $c$ | 文本条件嵌入 |
| 去噪 U-Net | 预测噪声，驱动逆向扩散过程 | 可训练 | $z_t, t, E(x), c$ | 预测噪声 $\epsilon_\theta$ |
| VAE 解码器 $D$ | 将去噪潜变量解码为深度图 | 冻结 | $z_0$ | 深度预测 $\hat{y}$ |

### 条件注入机制

与仅使用图像条件的基线方法（如 **Marigold**、**Lotus**、**E2E-FT**）不同，Iris 在去噪 U-Net 的条件输入中增加了文本嵌入。具体而言，图像潜变量 $E(x)$ 与噪声深度潜变量 $z_t$ 沿通道维度拼接后送入 U-Net，同时 CLIP 编码的文本条件 $c$ 通过交叉注意力机制注入 U-Net 的各层。这一设计使得扩散模型在去噪的每一步都能同时利用视觉外观和语言语义两种互补信息。

### 关键设计选择

- **冻结编码器**：VAE 编码器/解码器和 CLIP 文本编码器均保持冻结，仅微调去噪 U-Net。这保留了预训练模型已学到的视觉-语言对齐知识，同时将训练开销集中在扩散先验的迁移上。
- **共享潜空间**：图像和深度图使用同一个 VAE 编码器映射到潜空间，确保两种模态在特征维度上对齐，便于 U-Net 进行跨模态融合。
- **文本作为通用条件**：文本描述 $c$ 可以是人工标注、视觉语言模型自动生成，甚至是固定模板文本（如 “An image”）。消融实验表明，只要文本具有意义且近似人类描述，性能保持可比（Table 3, Table 5），证明框架对文本来源具有鲁棒性。

![[assets/figures/papers/paper_list_l2526_https_arxiv_org_abs_2411_16750/figures/014_Table_5.jpg]]
*Table 5: Inference using fixed template text input. The results show that the model achieves comparable, or even better, performance than the Marigold baseline when using fixed prompts instead of user-provided text. This finding suggests that, even when user-provided descriptions are unavailable, incorporating language during training itself might enhance the depth estimator’s generalization and overall performance*

### 补充图表

Iris 的核心设计是在现有扩散深度估计框架中，**仅变更条件输入**：在图像潜变量与噪声深度潜变量拼接的基础上，额外拼接由冻结 CLIP 文本编码器编码的场景语言描述，作为去噪 U-Net 的条件。该方法可视为一种通用适配策略，不改变扩散模型的主体架构，因此可无缝应用于 Marigold、Lotus、E2E-FT 等多种扩散深度估计基线。

### 关键模块

**冻结 VAE 编码器 E**：将输入图像 x 和真值深度图 y* 分别编码到同一潜空间。真值深度潜变量 z_y 作为扩散过程的监督信号，图像潜变量 E(x) 作为条件之一。

**冻结 CLIP 文本编码器**：将文本描述 c 编码为条件向量，注入去噪 U-Net 的交叉注意力层。该编码器在训练期间保持冻结，以保留其在大规模图文预训练中习得的语义-空间对齐能力。

**去噪 U-Net（源自 Stable Diffusion v2）**：以噪声深度潜变量 z_t、时间步 t、图像条件 E(x) 和文本条件 c 为输入，预测当前步添加的噪声 ε_θ。该网络继承自 Stable Diffusion v2 的 U-Net 结构，其文本到图像预训练已隐式习得与语言描述一致的三维场景结构先验。

**冻结 VAE 解码器 D**：将去噪后的潜变量 z_0 解码回深度图 ŷ = D(z_0)。

### 公式推导

Iris 沿用 DDPM 的扩散范式，核心变化在于将文本 c 引入逆向过程的条件集合。

**前向扩散过程**：从真值深度潜变量 z_0 = E(y*) 出发，逐步添加高斯噪声至纯噪声 z_T。单步转移为：

$$q(\mathbf{z}_t | \mathbf{z}_{t-1}) = \mathcal{N}(\mathbf{z}_t; \sqrt{1-\beta_t} \mathbf{z}_{t-1}, \beta_t \mathbf{I})$$

其中 β_t 为噪声调度参数。联合分布为：

$$q(\mathbf{z}_{1:T} | y^*) = \prod_{t=1}^{T} q(\mathbf{z}_t | \mathbf{z}_{t-1})$$

**逆向扩散过程**：以图像 x 和文本 c 为条件，从 z_T 逐步去噪至 z_0。联合分布为：

$$p_{\theta}(\mathbf{z}_{0:T} | x, \mathbf{c}) = p(\mathbf{z}_T) \prod_{t=1}^T p_{\theta}(\mathbf{z}_{t-1} | \mathbf{z}_t, x, \mathbf{c})$$

其中单步去噪参数化为高斯分布：

$$p_{\theta}(\mathbf{z}_{t-1} | \mathbf{z}_t) = \mathcal{N}(\mathbf{z}_{t-1}; \mu_{\theta}(\mathbf{z}_t, t, x, \mathbf{c}), \Sigma_{\theta}(\mathbf{z}_t, t, x, \mathbf{c}))$$

均值 μ_θ 由去噪 U-Net 预测，方差 Σ_θ 通常设为固定值。

**训练目标**：通过预测添加的噪声 ε 来训练模型，损失函数为：

$$\mathcal{L}(\theta) = \mathbb{E}_{y,\epsilon,t} \left[ \| \epsilon - \epsilon_\theta(\mathbf{z}_t, t, x, \mathbf{c}) \|^2 \right]$$

其中 ε ~ N(0, I) 为前向过程添加的噪声，ε_θ 为 U-Net 的噪声预测。与纯视觉基线相比，唯一的差异在于 ε_θ 额外接受文本条件 c。

**推理采样**：从 z_T ~ N(0, I) 开始，迭代执行去噪步骤：

$$\mathbf{z}_{t-1} = \frac{1}{\sqrt{\alpha_t}} \left( \mathbf{z}_t - \frac{1-\alpha_t}{\sqrt{1-\bar{\alpha}_t}} \epsilon_\theta(\mathbf{z}_t, t, x, \mathbf{c}) \right)$$

其中 α_t = 1 - β_t，ᾱ_t = ∏_{s=1}^t α_s。完成 T 步去噪后，通过 D(z_0) 解码得到最终深度预测。

**核心机制**：文本 c 作为额外条件，将场景中物体的存在性、类别、大小、空间关系等先验注入去噪过程，约束深度解空间，从而有效消解纯视觉条件下的纹理歧义与可见性歧义。实验表明，该约束使扩散模型仅需 10 步 DDIM 去噪即可收敛，而基线需要 25 步（Table 4, Figure 8），验证了语言对扩散轨迹的加速作用。

### 补充图表

![[assets/figures/papers/paper_list_l2526_https_arxiv_org_abs_2411_16750/figures/002_Figure_2.jpg]]
*Figure 2: Language improves the depth perception of specified insignificant (and potentially ambiguous) regions*

## 实验与关键发现

### 核心定量结果

Iris作为一种通用的语言集成策略，在三种不同的扩散式深度估计器上均取得了一致的性能提升。Table 1汇总了以Marigold为基线的跨数据集零样本评估结果。在五个真实场景数据集上，同时于训练和推理阶段融入文本描述的模型（Marigold + Text Train & Infer）在AbsRel指标上全面优于纯视觉基线：NYUv2上从6.1降至**5.9**，KITTI上从10.7降至**10.4**，ETH3D上从6.9降至**6.5**，ScanNet上从7.3降至**6.7**，DIODE上从31.3降至**29.8**。这表明语言提供的场景先验能够有效约束深度解空间，且该增益具有跨数据集的泛化性。

值得注意的是，即使在仅在训练阶段或仅在推理阶段引入文本的条件下，性能仍可超越纯视觉基线。这一现象暗示，语言条件在训练中起到了正则化作用，使模型学习到更鲁棒的深度表征；而在推理时，即使使用简单的场景描述，也能为去噪过程提供有效的几何指引。

### 小区域深度感知的显著增强

Table 2进一步量化了语言对微小区域的感知能力。实验使用全景分割掩码筛选出图像中面积占比小于5%、10%和20%的区域进行独立评估。结果显示，融入文本后，模型在小面积区域上的深度估计精度显著优于基线，尤其在占比小于5%的极端微小区域上改善最为明显。这直接验证了核心论断：当视觉信号因目标过小、遮挡或与背景纹理相似而变得模糊时，语言提供的物体存在性、类别和空间关系等先验能够有效补充视觉信息的不足。

### 扩散过程加速收敛

语言条件的引入对扩散模型的推理效率产生了显著影响。Figure 8和Table 4展示了不同去噪步数下的性能曲线。纯视觉基线需要约25步DDIM去噪才能收敛至稳定精度，而融入文本后，模型仅需**10步**即可达到与基线25步相当的精度水平，且在各步数下均保持性能优势。这一加速效应源于文本条件为逆向扩散过程提供了更强的约束信号，使去噪轨迹更直接地收敛到符合场景语义的深度分布，从而大幅减少了所需的采样步数。

训练收敛速度同样受益。Figure 7显示，融入文本的训练过程在更少的迭代次数内即可达到更低的损失值，表明语言先验使模型能够更高效地利用训练信号，减少了对大量视觉样本的依赖。

### 文本来源与质量的鲁棒性分析

**提示词敏感性。** Table 3考察了使用不同提示词（prompt）引导视觉语言模型生成场景描述对最终深度估计性能的影响。结果表明，只要生成的文本描述具有语义意义且近似人类描述风格，不同提示词之间的性能差异保持在可比较范围内。这说明Iris方法对文本生成的具体措辞不敏感，关键在于文本是否提供了有效的场景语义信息。

**文本数量饱和效应。** Table 6显示，将每张训练图像的文本描述数量从1条增加到10条，初期带来轻微的性能提升，但增益迅速饱和。这一现象表明，不同文本描述覆盖了高度重叠的深度关键属性（如物体类别、相对大小、空间位置），增加描述多样性无法持续引入新的有效约束。

**固定模板文本的泛化能力。** Table 5揭示了一个反直觉的发现：在推理阶段使用固定的模板文本（如“An image”或通用的场景描述句）替代图像特定的真实描述，模型仍可取得与纯视觉基线相当甚至更优的性能。这意味着，即使在实际部署中无法获取用户提供的场景描述，仅在训练阶段融入语言就足以提升深度估计器的泛化能力和整体性能。语言在训练中充当了隐式的跨样本结构化先验，使模型学到了更鲁棒的深度表征，而非仅仅记忆文本-深度的表层映射。

**错误文本的误导效应。** Figure 9提供了语言条件被模型真实利用的关键定性证据。当将正确的场景描述“a bookshelf with glass”替换为错误的描述“a window with curtains”后，模型完全无法感知玻璃后方书架的结构，深度预测出现明显错误。这一失败案例表明，模型确实依赖于文本语义信息进行深度推断，而非忽略文本条件仅依赖视觉信号。

### 迭代式语言精炼

Figure 6展示了通过逐步追加细节描述来迭代优化深度预测的能力。每次将新增的描述句追加到原始描述末尾并重复推理过程，深度预测在指定区域或物体上得到逐步改善。这一特性为交互式深度估计提供了可能：用户可以通过不断补充场景细节来精炼模型对特定区域的深度感知，使语言成为一种可控的深度编辑接口。

### 跨模型架构的通用性验证

除了Marigold基线外，Iris策略在Lotus（Lotus-D和Lotus-G）以及E2E-FT（Stable Diffusion端到端微调）上同样验证了有效性（Table 1）。在三种架构差异显著的扩散式深度估计器上，融入文本均带来了普遍的精度提升，表明该策略不依赖于特定的模型结构或训练范式，具有作为通用增强模块的潜力。

![[assets/figures/papers/paper_list_l2526_https_arxiv_org_abs_2411_16750/figures/006_Table_1.jpg]]
*Table 1: Quantitative comparison. Integrating language generally outperforms the baselines. In some cases, integrating language only during training or only during inference can also lead to performance improvements. Metrics are reported as percentages. * indicates results that we re-trained and re-evaluated using their open-sourced code. Due to computational overhead, all models are evaluated without ensembling. We gray out results that were not reproducible with the released code and models. Unless otherwise specified, in this paper, integrating text means integrating text in both training and inference*

### 失败模式与局限性

尽管整体性能提升显著，Iris仍存在明确的失败模式。Figure 9揭示的错误文本误导问题表明，模型缺乏对输入文本质量的校验机制，对抗性或错误的文本描述会直接导致深度预测失败。此外，当前方法依赖视觉语言模型自动生成训练文本，可能引入模型自身的偏差和幻觉，在人类真实描述场景下的有效性未经验证。训练数据均为合成数据集（HyperSim、Virtual KITTI），与真实场景存在域间隙，极端真实环境下的泛化能力需进一步检验。

### 补充图表

![[assets/figures/papers/paper_list_l2526_https_arxiv_org_abs_2411_16750/figures/008_Table_2.jpg]]
*Table 2: Better perception in small areas. We evaluate the performance for panoptic segmentation masks that occupied less than 5%, 10%, and 20% of an image. Integrating language results in better depth estimation in small areas*

![[assets/figures/papers/paper_list_l2526_https_arxiv_org_abs_2411_16750/figures/011_Figure_8.jpg]]
*Figure 8: Performance under different denoising steps. Integrating language consistently outperforms the Marigold baseline across various denoising steps, with a faster convergence*

![[assets/figures/papers/paper_list_l2526_https_arxiv_org_abs_2411_16750/figures/009_Figure_7.jpg]]
*Figure 7: Convergence speed comparison. Integrating language converges faster during training compared with the Marigold baseline*

![[assets/figures/papers/paper_list_l2526_https_arxiv_org_abs_2411_16750/figures/010_Figure_9.jpg]]
*Figure 9: Incorrect text misguides models. After replacing the correct description “a bookshelf with glass” with a wrong description “a window with curtains”, the model failed to perceive the structure of the bookshelf behind the glass*

![[assets/figures/papers/paper_list_l2526_https_arxiv_org_abs_2411_16750/figures/016_Table_4.jpg]]
*Table 4: Performance for different denoising steps. Integrating text consistently outperforms the baseline across various denoising steps, with a significantly faster convergence speed for the diffusion process*

![[assets/figures/papers/paper_list_l2526_https_arxiv_org_abs_2411_16750/figures/015_Table_3.jpg]]
*Table 3: Ablation for prompts to generate language description. Prompts are used to prompt LLaVA to generate language descriptions for each image. While the performances among different prompts may vary, they remain consistently comparable, as long as they are meaningful and mimic human descriptions. Marigold in the first row is trained without text*

![[assets/figures/papers/paper_list_l2526_https_arxiv_org_abs_2411_16750/figures/017_Table_6.jpg]]
*Table 6: Training with different numbers of text captions per image. For images annotated with multiple captions, a caption is randomly sampled for each training iteration. While adding more captions initially slightly improves performance, the benefit quickly saturates, yielding only minor gains beyond a certain point*

## 定位与知识库关联

### 1. 在扩散深度估计谱系中的位置

Iris 并非提出新的扩散架构，而是一种**通用条件增强策略**：在现有基于扩散的单目深度估计器（如 **Marigold**、**Lotus**、**E2E-FT**）的去噪 U-Net 中，额外注入由冻结 CLIP 文本编码器编码的场景语言描述，将纯视觉条件 $p_\theta(\mathbf{z}_{t-1} | \mathbf{z}_t, x)$ 扩展为图文联合条件 $p_\theta(\mathbf{z}_{t-1} | \mathbf{z}_t, x, \mathbf{c})$。其核心假设是：文本到图像预训练的扩散模型已隐式习得与语言描述一致的三维场景结构，通过图像-文本-深度三元组微调，可将此隐式先验显式化为深度估计能力。

与以下工作的关系：

- **Marigold**：仅使用图像潜变量 $E(x)$ 与噪声深度潜变量 $z_t$ 拼接作为条件。Iris 在相同架构上增加文本条件通道，Table 1 显示在 NYUv2 上 AbsRel 从 6.1 降至 5.9，KITTI 从 10.7 降至 10.4。
- **Lotus (Lotus-D / Lotus-G)**：同为扩散深度估计基线，Iris 的文本集成策略同样适用并带来一致提升。
- **E2E-FT (Stable Diffusion 端到端微调)**：Iris 的策略同样可叠加，验证了语言条件的架构无关性。
- **判别式单目深度估计方法**：Iris 未涉及此范式，语言增益在此类模型中的可迁移性仍是开放问题。

### 2. 适用边界

Iris 的策略在以下条件下有效：

1. **基础模型具备图文联合先验**：依赖 Stable Diffusion v2 的预训练权重，去噪 U-Net 必须已在图文对齐数据上训练过，否则语言条件无法提供有效约束。
2. **文本描述具有语义相关性**：Table 3 表明，只要文本有意义且近似人类描述，不同提示词生成的文本性能可比；但 Figure 9 显示，错误文本（如将“带玻璃的书架”描述为“带窗帘的窗户”）会严重误导模型，导致深度结构感知失败。
3. **训练数据覆盖场景多样性**：训练仅使用合成数据集 HyperSim 和 Virtual KITTI，与真实场景存在域间隙，可能限制在极端真实环境下的泛化。
4. **计算资源充足**：需加载预训练 Stable Diffusion 和冻结 CLIP 文本编码器，模型较大，不利于资源受限部署。

### 3. 局限与已知失效模式

1. **文本质量敏感**：缺乏对输入文本的鲁棒性校验机制，错误或对抗性文本可直接破坏深度预测（Figure 9）。
2. **文本描述来源偏差**：文本由视觉语言模型（LLaVA、InternVL3）自动生成，非人工标注，可能引入模型自身的幻觉和社会偏见。
3. **合成数据的域迁移风险**：训练仅使用 HyperSim 和 Virtual KITTI，在真实场景中的泛化上限未经充分验证。
4. **文本增益饱和**：Table 6 显示，每张图像文本描述数量从 1 增至 10 时，性能提升微小且快速饱和，表明不同描述覆盖的深度关键属性高度重叠。
5. **仅验证扩散范式**：未探索判别式模型中语言的增益，适用性边界尚不明确。

### 4. 开放问题

1. **更强文本编码器的潜力**：能否利用领域专用或更强大的文本编码器（如视觉语言模型本身的文本塔）进一步提升深度估计质量？
2. **鲁棒性机制设计**：如何使模型对不准确、模糊或缺失的文本输入鲁棒（例如引入不确定性估计或文本质量评估模块）？
3. **具身智能场景适配**：在真实具身应用中，自然语言指令往往简洁或不完整，该方法能否在此设置下保持有效？
4. **多模态融合扩展**：语言先验是否能与其他传感器模态（如 IMU、激光雷达）有效融合，实现更鲁棒的三维感知？
5. **任务泛化能力**：该语言集成策略能否推广到其他密集预测任务（如表面法线估计、语义分割）？

## 原文 PDF

![[paperPDFs/CVPR_2026/Iris_Integrating_Language_into_Diffusion_based_Monocular_Depth_Estimation.pdf]]
