---
title: "Tracking-Guided 4D Generation: Foundation-Tracker Motion Priors for 3D Model Animation"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/Tracking_Guided_4D_Generation_Foundation_Tracker_Motion_Priors_for_3D_Model_Animation.pdf
paper_link: https://openaccess.thecvf.com/content/CVPR2026/html/Sun_Tracking-Guided_4D_Generation_Foundation-Tracker_Motion_Priors_for_3D_Model_Animation_CVPR_2026_paper.html
project_link: null
code_link: null
aliases:
- TG4GFTMP3MA
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/image_and_video_generation
- topic/vision_multimodal_applications/3d_rendering_reconstruction
- topic/generative_models_diffusion
core_operator: 在扩散特征空间中注入基于基础跟踪器（CoTracker3）的密集点对应监督。
primary_logic: 利用基础点跟踪器提取的运动先验可以显式地约束扩散模型的中间特征，从而增强时序一致性并减少漂移；同时，这些跟踪感知的扩散特征可以提升4D-GS重建的动态质量。
claims:
- Track4DGen在Diffusion4D和Animate3D数据集上的视频生成指标（如I2V、动态度）均优于基线Animate3D。
- Track4DGen在Sketchfab28和Animate3D数据集上的4D生成CLIP指标（如CLIP-O(img)、CLIP-C）均取得最高分，分别提升+0.0072和+0.0036。
- 用户研究显示参与者一致偏好Track4DGen的生成结果，在文本对齐、三维资产对齐、运动质量和外观质量方面评分最高。
- Sketchfab28 上 CLIP-O(img) = 0.8884
---

# Tracking-Guided 4D Generation: Foundation-Tracker Motion Priors for 3D Model Animation

> [!tip] 核心洞察
> 利用基础点跟踪器提取的运动先验可以显式地约束扩散模型的中间特征，从而增强时序一致性并减少漂移；同时，这些跟踪感知的扩散特征可以提升4D-GS重建的动态质量。

| 字段 | 内容 |
|------|------|
| 中文题名 | 跟踪引导的4D生成：基础跟踪器运动先验用于三维模型动画 |
| 英文题名 | Tracking-Guided 4D Generation: Foundation-Tracker Motion Priors for 3D Model Animation |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://openaccess.thecvf.com/content/CVPR2026/html/Sun_Tracking-Guided_4D_Generation_Foundation-Tracker_Motion_Priors_for_3D_Model_Animation_CVPR_2026_paper.html) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/image_and_video_generation #topic/vision_multimodal_applications/3d_rendering_reconstruction #topic/generative_models_diffusion |
| Method | Track4DGen |
| Dataset | Sketchfab28, Animate3D |

> [!tip] 效果简介
> - Sketchfab28 上，CLIP-O(img) 0.8884 vs 0.8812 (+0.0072)。
> - Animate3D 上，CLIP-C 0.9819 vs 0.9783 (+0.0036)。

## 概述

**核心问题**：现有的多视图视频扩散模型在生成动态三维内容时，缺乏显式的特征级时序跟踪监督，导致生成结果出现外观漂移和时空不一致性，限制了高质量4D资产生成的可靠性。

**方法定位**：Track4DGen 是一个两阶段框架，将多视图视频扩散模型与基础点跟踪器以及混合4D高斯泼溅重建器耦合。其核心创新在于将基础跟踪器（CoTracker3）提取的密集点对应作为运动先验，显式注入扩散特征空间，从而增强时序一致性并减少漂移；同时，这些携带跟踪先验的扩散特征进一步提升了4D-GS重建的动态质量。

**关键结论**：
- 在视频生成任务上，Track4DGen 在 Diffusion4D 和 Animate3D 数据集上的 I2V 和动态度指标均优于基线方法 Animate3D（Jiang et al., NeurIPS 2024）。
- 在4D生成任务上，Track4DGen 在 Sketchfab28 和 Animate3D 数据集上的 CLIP 指标（CLIP-O(img)、CLIP-C）均取得最高分，分别提升 +0.0072 和 +0.0036。
- 用户研究显示参与者一致偏好 Track4DGen 的生成结果，在文本对齐、三维资产对齐、运动质量和外观质量方面评分最高。

**方法谱系与知识库定位**：
Track4DGen 建立在多视图视频扩散与4D重建的基线之上，直接对比的方法包括：多视图视频扩散基线 **4Diffusion**（Zhang et al., NeurIPS 2024）和 **Animate3D**（Jiang et al., NeurIPS 2024）；单图像到4D生成基线 **DreamGaussian4D (DG4D)**（Ren et al., arXiv 2023）和 **EG4D**（Sun et al., ICLR 2025）；以及单目视频到4D生成基线 **SV4D**（Xie et al., arXiv 2024）和 **SC4D**（Wu et al., ECCV 2024）。Track4DGen 区别于这些工作的关键改动在于：(1) 在扩散U-Net解码器的第二个上采样块特征上增加了基于CoTracker3密集跟踪的对应损失 $\mathcal{L}_{\mathrm{corr}}$ 和位置损失 $\mathcal{L}_{\mathrm{pos}}$，实现了特征级的显式时序对应监督；(2) 在4D-GS阶段引入混合运动表示，将携带跟踪先验的扩散特征与Hex-plane特征拼接，并引入4D球谐函数（4D SH）建模颜色随时间的变化。

## 背景与动机

动态三维内容生成是计算机视觉与图形学交叉领域的前沿课题。随着扩散模型在图像和视频生成领域的突破性进展，研究者开始探索将二维生成能力拓展至四维时空域——即从静态三维资产或文本描述出发，生成具有时序运动的三维模型动画。这一能力对于影视制作、游戏开发、虚拟现实等应用场景具有重要价值。

当前的主流技术路线可分为两类：一类是“单图像/视频到4D”方法，如 **DreamGaussian4D**（Ren et al., arXiv 2023）、**EG4D**（Sun et al., ICLR 2025）、**SV4D**（Xie et al., arXiv 2024）和 **SC4D**（Wu et al., ECCV 2024），它们试图从单目输入直接重建动态三维资产，但受限于输入信息的稀疏性，难以保证多视角下的时空一致性；另一类则采用“多视图视频扩散+4D重建”的两阶段范式，以 **Animate3D**（Jiang et al., NeurIPS 2024）和 **4Diffusion**（Zhang et al., NeurIPS 2024）为代表，先生成多视角视频序列，再通过4D高斯泼溅（4D Gaussian Splatting, 4D-GS）重建动态资产。

然而，现有方法存在一个关键瓶颈：**多视图视频扩散模型缺乏显式的特征级时序跟踪监督**。扩散模型在生成过程中仅依赖像素空间或潜空间的视频扩散损失（如标准噪声预测损失），没有机制确保同一物理点在连续帧间的特征表示保持一致。这导致生成视频中出现外观漂移（appearance drift）和时空不一致性（spatio-temporal inconsistency），表现为物体纹理在运动过程中发生不应有的变化、运动轨迹不连贯等问题。这些缺陷在后续4D重建阶段会被进一步放大，最终影响动态资产的质量。

本文的核心洞察在于：**基础点跟踪器（foundation point tracker）提取的密集运动对应可以作为显式先验，约束扩散模型的中间特征表示**。具体而言，像CoTracker3这类先进点跟踪器能够提供跨帧的密集点对应关系，这些对应关系蕴含了场景运动的真实信息。如果在扩散模型的U-Net特征空间中施加基于这些对应的监督信号，就能强制模型学习时序一致的特征表示，从根源上抑制外观漂移。

基于这一洞察，本文提出 **Track4DGen**，一个将基础跟踪器运动先验注入多视图视频扩散生成的两阶段框架。第一阶段在扩散生成器中引入基于CoTracker3密集跟踪的对应损失和位置损失，在特征层面显式强制时序一致性；第二阶段将携带跟踪先验的扩散特征与Hex-plane特征融合，构建混合运动表示，并引入4D球谐函数建模颜色随时间的变化，从而在4D-GS重建中充分利用第一阶段积累的时序信息。

## 核心创新

Track4DGen的核心创新在于将**基础跟踪器的运动先验**显式注入多视图视频扩散模型的**特征空间**，从而解决现有方法因缺乏显式时序监督导致的外观漂移与时空不一致问题。具体而言，该方法在以下两个关键环节引入了差异化设计：

### 1. 特征级密集点对应监督

现有基线方法（如**Animate3D** (Jiang et al., NeurIPS 2024) 和 **4Diffusion** (Zhang et al., NeurIPS 2024)）仅依赖像素/潜空间层面的视频扩散损失，缺乏对中间特征层时序一致性的显式约束。Track4DGen的**核心因果开关**在于：在U-Net解码器的第二个时空上采样块（该块的时序运动模块被验证具有最强的帧间对应能力，见Figure 3）提取扩散特征，并利用基础跟踪器CoTracker3提取的密集帧间点对应，施加两种显式监督：

- **对应跟踪损失** $\mathcal{L}_{\mathrm{corr}}$：通过余弦相似度强制相邻帧中同一跟踪点的特征描述符保持一致，从特征层面抑制外观漂移。
- **位置损失** $\mathcal{L}_{\mathrm{pos}}$：通过Huber损失最小化预测跟踪位置与真实位置的偏差，确保特征对应在空间上的准确性。

这一设计将时序监督从“结果端”前移至“表示端”，使得扩散模型在生成过程中即获得显式的运动感知能力。

### 2. 跟踪感知的混合4D-GS重建

在4D高斯泼溅（4D-GS）重建阶段，基线方法仅使用Hex-plane特征建模运动。Track4DGen提出**混合运动表示**：将第一阶段携带跟踪先验的扩散特征与Hex-plane特征在对应时空位置拼接，形成混合特征 $\mathcal{F}$，再通过MLP头预测高斯体的位置、旋转和尺度偏移。这使得4D-GS的运动场直接受益于扩散模型学到的时序对应关系。

此外，Track4DGen引入**4D球谐函数（4D SH）外观模型**，用傅里叶级数参数化球谐系数以建模颜色随时间的变化，解决了传统3D SH无法表达动态外观的局限。

### 创新总结

| 创新维度 | 基线方法 | Track4DGen |
|---------|---------|------------|
| 时序监督方式 | 仅像素/潜空间扩散损失 | 增加特征级对应损失 $\mathcal{L}_{\mathrm{corr}}$ + 位置损失 $\mathcal{L}_{\mathrm{pos}}$ |
| 4D-GS运动表示 | 仅Hex-plane特征 | 扩散特征 + Hex-plane混合表示 |
| 外观建模 | 3D SH | 4D SH（傅里叶级数参数化时间相关颜色） |

消融实验（Table 4、Figure 6、Figure 7）证实：移除对应损失会降低视频生成的时域一致性和动态质量；移除扩散特征或4D SH均会导致4D生成的外观保真度下降和伪影增加，验证了上述创新设计的有效性。

## 整体框架

Track4DGen 采用**两阶段级联架构**，将多视图视频生成与 4D 重建解耦为顺序流水线，如图 1 所示。第一阶段以静态 3D 模型的多视图渲染作为条件输入，通过集成多视图 3D 注意力与时空注意力的视频扩散生成器（基于 MV-VDM 架构）产生时序一致的多视图视频；第二阶段则从生成视频出发，利用 4D 高斯泼溅（4D-GS）重建动态 4D 资产。

### 阶段一：跟踪感知的多视图视频扩散

该阶段的核心创新在于**将基础点跟踪器 CoTracker3 提取的密集帧间点对应作为运动先验，注入扩散模型的中间特征空间**。具体而言，扩散 U-Net 解码器第二个上采样块的时空注意力模块输出的特征被证明具有最强的时序对应能力——这些特征在相似度热图上呈现出沿跟踪轨迹的高响应区域。基于这一发现，Track4DGen 在该特征层级上施加两类显式监督：

- **对应损失**（$\mathcal{L}_{\mathrm{corr}}$）：强制相邻帧中同一跟踪点的特征描述符保持余弦相似，从特征层面抑制外观漂移；
- **位置损失**（$\mathcal{L}_{\mathrm{pos}}$）：通过 Huber 损失最小化预测跟踪位置与 CoTracker3 真实轨迹之间的偏差，确保空间对应精度。

这一设计将原本仅依赖像素/潜空间扩散损失的隐式时序约束，升级为**特征级的显式对应感知监督**，直接针对多视图视频扩散中“缺乏显式时序跟踪监督导致外观漂移和时空不一致”的核心瓶颈。

### 阶段二：混合特征驱动的 4D-GS 重建

第二阶段将第一阶段生成的视频转化为可自由视点渲染的动态 4D 资产。其关键设计在于**混合运动表示**与**4D 球谐函数外观模型**：

- **混合特征拼接**：对于每个 4D 高斯中心的时空采样点，将其在 Hex-plane 特征平面上的插值特征，与第一阶段扩散特征平面（携带跟踪先验）上的插值特征进行拼接，形成联合特征 $\mathcal{F}$。随后通过三个 MLP 头分别预测高斯的位置偏移 $\Delta\mathcal{X}$、旋转偏移 $\Delta\boldsymbol{r}$ 和尺度偏移 $\Delta s$。
- **4D 球谐函数**：将传统 3D-GS 的球谐系数扩展为时间的函数——用傅里叶级数参数化 4D 球谐系数 $k_l^m = \sum_{i=0}^{w-1} fr_i \cos(\frac{i\pi}{N_t} t)$，使颜色随视角和时间同时变化，提升动态外观的保真度。

优化目标由三项加权组成：重建损失 $\mathcal{L}_{\mathrm{rec}}$（监督渲染图像与掩码）、4D-SDS 损失 $\mathcal{L}_{\mathrm{4D-SDS}}$（将阶段一的多视图扩散先验蒸馏到 4D-GS）以及 ARAP 正则化损失 $\mathcal{L}_{\mathrm{ARAP}}$（保持局部刚性）。

### 信息流与模块依赖

整个流水线的信息流可概括为：**静态 3D 模型 → 条件多视图渲染 → 跟踪监督的扩散生成器 → 多视图视频 → 混合特征 4D-GS 重建 → 动态 4D 资产**。两个阶段之间存在明确的特征传递——阶段一的扩散特征平面被显式保留并馈入阶段二的混合表示中，使得跟踪先验能够贯穿生成与重建的全过程。这种紧耦合设计确保了从视频生成到 4D 重建的时序一致性不会因阶段分离而退化。

### 补充图表

![[assets/figures/papers/paper_list_l17_https_openaccess_thecvf_com_content_CVPR2026_html_Sun_Tracking_Guided_4D/figures/001_Figure_1.jpg]]
*Figure 1: The Track4DGen pipeline comprises two stages: 1) multi-view video generation and 2) 4D-GS reconstruction*

## 核心模块与公式推导

Track4DGen 的核心架构由两个解耦阶段构成：**跟踪感知的多视图视频扩散生成器**与**混合特征驱动的4D高斯泼溅重建器**。两条管线通过扩散特征空间中的密集点对应监督实现耦合——第一阶段将基础跟踪器的运动先验注入扩散特征，第二阶段则直接复用这些携带跟踪先验的特征来增强动态重建质量。

### 多视图视频扩散与密集点跟踪

**动机与瓶颈。** 现有多视图视频扩散模型（如 Animate3D, Jiang et al., NeurIPS 2024）仅在像素/潜空间施加扩散损失，缺乏显式的特征级时序约束，导致生成视频在长序列中出现外观漂移和时空不一致。核心因果调控变量在于：是否在扩散U-Net的中间特征层施加跨帧对应监督。

**潜空间表示。** 给定 $N$ 个相机视角、$F$ 帧的视频，编码器 $\mathcal{E}$ 将其映射为潜张量：

$$z \in \mathbb{R}^{N \times F \times C \times H \times W}$$

其中 $C$ 为潜通道数，$H \times W$ 为空间分辨率。第一帧作为条件帧，其余 $F-1$ 帧为待生成帧。

**噪声注入策略。** 为在条件帧中保留足够的结构信息同时促进动态生成，Track4DGen 采用非对称噪声调度。对第2至 $f$ 帧执行标准前向扩散：

$$z_{t}^{1:n,2:f} = \sqrt{\overline{\alpha}_{t}} z_{0}^{1:n,2:f} + \sqrt{1-\overline{\alpha}_{t}} \epsilon, \quad \epsilon \sim \mathcal{N}(0,\mathbf{I})$$

对第一帧（条件帧）仅注入时变弱噪声：

$$z_{t}^{1:n,1} = z_{0}^{1:n,1} + \beta_{t} \epsilon', \quad \epsilon' \sim \mathcal{N}(0,\mathbf{I})$$

其中 $\beta_t$ 随扩散步数 $t$ 增大而减小，使得条件帧在去噪早期保持较高信噪比，为后续帧提供稳定的多视图结构锚点。

**扩散去噪目标。** 标准噪声预测损失为：

$$\mathcal{L}_{\mathrm{diff}} = \mathbb{E}_{\mathcal{E}(x_{0}),y,\epsilon,t} \left[ \left\| \epsilon - \epsilon_{\theta} \big( z_{t}^{1:n,1}, z_{t}^{1:n,2:f}, t, y, c^{1:n} \big) \right\|_{2}^{2} \right]$$

其中 $y$ 为文本条件，$c^{1:n}$ 为各视角的相机参数嵌入。

**跟踪特征层选择。** 关键设计在于选择U-Net中哪一层的特征用于跟踪监督。实验发现（Figure 3），**解码器第二个时空上采样块**中的特征具有最强的跨帧时序对应能力，尤其是时空注意力模块中时序运动子模块的输出。该层特征在保持空间细节的同时，对同一物理点的跨帧位移表现出高度可区分性——相似度热图中对应点区域呈现明显高亮。

**基础跟踪器集成。** Track4DGen 采用 CoTracker3 作为密集点跟踪器。在训练时，对生成的视频帧采样一组稀疏点，CoTracker3 输出这些点在相邻帧间的对应位置，形成跟踪轨迹 $\{p^{i,j}\}$，其中 $i$ 为视角索引，$j$ 为帧索引。

**对应跟踪损失。** 在U-Net解码器第二个上采样块的特征图 $h$ 上，提取跟踪点位置的特征描述符，强制相邻帧间对应点的特征余弦相似度最大化：

$$\mathcal{L}_{\mathrm{corr}} = \frac{1}{nf} \sum_{i=1}^{n} \sum_{j=1}^{f-1} \big(1 - \cos.\sin (h(p^{i,j}), h(p^{i,j+1}))\big)$$

该损失显式约束扩散特征的时序一致性，从特征层面抑制外观漂移。

**位置损失。** 为进一步增强跟踪精度，引入 Huber 损失最小化预测跟踪位置与 CoTracker3 真实位置的偏差：

$$\mathcal{L}_{\mathrm{pos}} = \frac{1}{nf} \sum_{i=1}^{n} \sum_{j=2}^{f} L_{\mathrm{Huber}} \left( p^{i,j} - \hat{p}^{i,j} \right)$$

其中 $\hat{p}^{i,j}$ 为 CoTracker3 输出的真实对应位置。总训练目标为 $\mathcal{L}_{\mathrm{diff}} + \lambda_1 \mathcal{L}_{\mathrm{corr}} + \lambda_2 \mathcal{L}_{\mathrm{pos}}$。

---

### 混合特征驱动的4D-GS重建

**动机。** 第二阶段从第一阶段生成的多视图视频重建动态4D资产。直接使用标准4D-GS（仅依赖Hex-plane特征）无法充分利用扩散特征中已编码的跟踪先验。Track4DGen 提出混合运动表示：将第一阶段U-Net解码器的扩散特征与Hex-plane特征在空间-时间采样点处拼接，同时引入4D球谐函数建模颜色随时间的变化。

**混合特征构造。** 对于高斯中心 $\mathcal{X}$ 在帧 $f$ 处，混合特征 $\mathcal{F}$ 由两部分拼接而成：

$$\mathcal{F} = \bigcup_{Hex} \prod_{\zeta_{1}} \operatorname{interp}\bigl( \mathcal{H}^{\zeta_{1}}, (\mathcal{X}, f) \bigr) \ \oplus \ \bigcup_{Diff} \prod_{\zeta_{2}} \operatorname{interp}\bigl( \mathcal{D}^{\zeta_{2}}, K[E](\mathcal{X}, f) \bigr)$$

其中 $\mathcal{H}^{\zeta_{1}}$ 为Hex-plane的六个特征平面，$\mathcal{D}^{\zeta_{2}}$ 为扩散特征平面，$K[E](\mathcal{X}, f)$ 表示将世界坐标 $\mathcal{X}$ 通过相机外参 $E$ 投影到扩散特征平面上进行插值采样。两部分特征通过拼接操作 $\oplus$ 融合。

**运动偏移预测。** 三个小型MLP头分别从混合特征 $\mathcal{F}$ 预测高斯属性的时间偏移：

$$\Delta \mathcal{X} = \phi_{\mathcal{X}}(\mathcal{F}), \quad \Delta \boldsymbol{r} = \phi_{\boldsymbol{r}}(\mathcal{F}), \quad \Delta s = \phi_{s}(\mathcal{F})$$

分别对应位置偏移、旋转偏移和尺度偏移。这些偏移叠加到静态高斯上，实现时序变形。

**4D球谐函数外观模型。** 为建模颜色随时间的连续变化，Track4DGen 将传统3D球谐系数扩展为时间函数，用傅里叶级数参数化：

$$\mathcal{C}_{4D} = f_{g}(\psi, \gamma) = \sum_{l=0}^{l_{\mathrm{max}}} \sum_{m=-l}^{l} k_{l}^{m} Y_{l}^{m}(\psi, \gamma), \quad k_{l}^{m} = \sum_{i=0}^{w-1} fr_{i} \cos\left( \frac{i\pi}{N_{t}} t \right)$$

其中 $Y_{l}^{m}$ 为球谐基函数，$(\psi, \gamma)$ 为视角方向，$k_{l}^{m}$ 为时间相关的球谐系数，由 $w$ 个可学习的傅里叶系数 $fr_i$ 通过余弦级数合成，$N_t$ 为归一化时间因子。

**重建损失。** 4D-GS渲染图像与第一阶段生成视频的监督采用掩码加权MSE：

$$\mathcal{L}_{\mathrm{rec}} = \frac{1}{nf} \sum_{i=1}^{n} \sum_{j=1}^{f} \Big( \big\| \mathcal{M} \cdot \mathcal{C} - \hat{\mathcal{M}} \cdot \hat{\mathcal{C}} \big\|^{2} \Big)$$

其中 $\mathcal{M}$ 和 $\mathcal{C}$ 分别为渲染的掩码和颜色，$\hat{\mathcal{M}}$ 和 $\hat{\mathcal{C}}$ 为生成视频的对应值。

**4D-SDS蒸馏损失。** 为进一步将第一阶段多视图扩散先验提炼到4D-GS，采用 $z_0$-重建SDS损失：

$$\mathcal{L}_{\mathrm{4D-SDS}}\big( \mathcal{G}_{4D}, z = \mathcal{E}(\mathrm{Render}(\mathcal{G}_{4D})) \big) = \mathbb{E}_{t,c,\epsilon} \Big[ \big\| z - \hat{z}_{0} \big\|_{2}^{2} \Big], \quad \hat{z}_{0} = \frac{z_{t} - \sigma_{t} \epsilon_{\theta}}{\alpha_{t}}$$

其中 $\hat{z}_{0}$ 为从噪声潜变量 $z_t$ 一步估计的干净潜变量，$z$ 为4D-GS渲染图像编码后的潜变量。该损失在潜空间而非像素空间施加约束，更稳定地传递扩散先验。

**总优化目标。** 第二阶段完整损失为：

$$\mathcal{L}_{2} = \lambda_{4} \mathcal{L}_{\mathrm{rec}} + \lambda_{5} \mathcal{L}_{\mathrm{4D-SDS}} + \lambda_{6} \mathcal{L}_{\mathrm{ARAP}}$$

其中 $\mathcal{L}_{\mathrm{ARAP}}$ 为尽可能刚性（ARAP）正则项，约束局部变形保持刚性，防止非物理形变。

---

### 模块间耦合机制

两个阶段的关键耦合点在于**扩散特征的复用**：第一阶段通过 $\mathcal{L}_{\mathrm{corr}}$ 和 $\mathcal{L}_{\mathrm{pos}}$ 将 CoTracker3 的运动先验注入U-Net解码器特征；第二阶段直接提取同一U-Net解码器第二个上采样块的特征平面 $\mathcal{D}^{\zeta_{2}}$，与Hex-plane特征拼接后驱动运动偏移预测。这种设计避免了额外的特征提取网络，实现了运动先验从视频生成到4D重建的端到端传递。消融实验（Table 4）证实：移除扩散特征（w/o Di. Feat）会导致4D生成的外观保真度和色彩真实性显著下降，验证了跟踪感知特征对重建质量的关键贡献。

### 补充图表

![[assets/figures/papers/paper_list_l17_https_openaccess_thecvf_com_content_CVPR2026_html_Sun_Tracking_Guided_4D/figures/002_Figure_2.jpg]]
*Figure 2: The multi-view video diffusion with dense point tracking*

![[assets/figures/papers/paper_list_l17_https_openaccess_thecvf_com_content_CVPR2026_html_Sun_Tracking_Guided_4D/figures/004_Figure_4.jpg]]
*Figure 4: 4D-GS reconstruction with hybrid feature representations*

![[assets/figures/papers/paper_list_l17_https_openaccess_thecvf_com_content_CVPR2026_html_Sun_Tracking_Guided_4D/figures/003_Figure_3.jpg]]
*Figure 3: Left: points tracking in multi-view images; Right: tacked points in similarity heatmap of U-Net’s second Upsample Block. Brighter color indicates higher feature similarity*

## 实验与分析

Track4DGen 的实验验证围绕两个核心阶段展开：多视图视频生成质量与 4D 动态资产重建质量。以下分别报告主结果、消融实验及关键图表发现。

### 多视图视频生成主结果

**Table 1** 在 Diffusion4D 和 Animate3D 两个数据集上对比了 Track4DGen 与多视图视频扩散基线 **4Diffusion**（Zhang et al., NeurIPS 2024）及 **Animate3D**（Jiang et al., NeurIPS 2024）的视频生成性能。评估指标涵盖图像到视频对齐度（I2V）、运动平滑度（M.Sm）、时序闪烁度（T.Fli）、动态度（Dy.Sc）和美学质量（Aest.Q）。

在 Diffusion4D 数据集上，Track4DGen 取得 I2V 0.933、M.Sm 0.992、T.Fli 0.991、Dy.Sc 1.356、Aest.Q 0.470，在所有指标上均优于 Animate3D 基线。在 Animate3D 数据集上，Track4DGen 同样全面领先，取得 I2V 0.945、M.Sm 0.993、T.Fli 0.992、Dy.Sc 0.778、Aest.Q 0.506。Dy.Sc 指标的显著提升直接验证了 CoTracker3 密集点跟踪监督引入的运动先验能有效增强生成视频的动态表现力，而非仅仅复制静态外观。

**Figure 5** 的定性对比进一步佐证了定量结果：Track4DGen 生成的多视图视频在时序一致性上明显优于基线，外观漂移现象大幅减少，运动轨迹更加自然流畅。

### 4D 资产生成主结果

**Table 2** 在 Sketchfab28 和 Animate3D 数据集上评估 4D 生成质量，对比方法包括单图像到 4D 基线 **DreamGaussian4D**（Ren et al., arXiv 2023）、**EG4D**（Sun et al., ICLR 2025），单目视频到 4D 基线 **SV4D**（Xie et al., arXiv 2024）、**SC4D**（Wu et al., ECCV 2024），以及多视图视频到 4D 基线 **Animate3D**。

Track4DGen 在两个数据集上均取得最高的 CLIP 分数。在 Sketchfab28 上，CLIP-O(img) 达到 0.8884，相较 Animate3D 的 0.8812 提升 +0.0072；在 Animate3D 上，CLIP-C 达到 0.9819，相较 Animate3D 的 0.9783 提升 +0.0036。这表明混合运动表示（扩散特征 + Hex-plane）和 4D 球谐函数外观模型有效提升了重建资产的文本对齐度和外观保真度。

**Table 3** 的用户研究显示，参与者在文本对齐、三维资产对齐、运动质量和外观质量四个维度上一致偏好 Track4DGen 的生成结果，进一步从感知层面验证了方法的优越性。

### 消融实验

**Table 4** 和 **Figure 6、7** 系统地拆解了各模块的贡献。

**视频生成消融（Table 4 左）：**
- **移除对应损失（w/o Corrs. Loss）**：动态度 Dy.Sc 显著下降，时序一致性减弱，验证了余弦相似度损失 $\mathcal{L}_{\mathrm{corr}}$ 在约束相邻帧跟踪点特征描述符一致性方面的关键作用。
- **移除位置损失（w/o pos. Loss）**：进一步削弱时序对应精度，表明 Huber 损失 $\mathcal{L}_{\mathrm{pos}}$ 对精确约束预测跟踪位置不可或缺。

**4D 生成消融（Table 4 右）：**
- **移除扩散特征（w/o Di. Feat）**：外观保真度和色彩真实性明显下降，伪影增多，证实了携带跟踪先验的扩散特征对 4D-GS 运动场学习的增强作用。
- **移除 4D SH（w/o 4D SH）**：颜色随时间变化的建模能力削弱，导致动态外观的视觉质量降低。

消融实验的因果链条清晰：对应损失和位置损失共同构成特征级时序监督的核心，它们通过强化扩散特征的时序一致性，间接提升了 4D-GS 重建的动态质量；而混合运动表示和 4D SH 则直接作用于 4D 重建阶段的外观保真度。

### 关键图表结论

- **Figure 3** 揭示了 U-Net 解码器第二个时空上采样块的特征具有最强的时序对应能力，这是选择该层施加跟踪监督的实证依据。相似度热图中高亮区域与 CoTracker3 跟踪点高度吻合，说明扩散特征本身蕴含可被显式监督挖掘的时序结构。
- **Figure 4** 展示了混合特征表示与 4D SH 的架构设计，该设计将第一阶段获得的跟踪感知扩散特征与 Hex-plane 特征拼接，并通过 MLP 头预测高斯属性的时间偏移，是实现高质量 4D 重建的结构性创新。
- **Figure 6 和 7** 的定性消融可视化直观展示了各模块缺失时的退化模式：缺少对应/位置损失时出现明显的时序抖动和外观漂移；缺少扩散特征或 4D SH 时则出现色彩失真和几何伪影。

![[assets/figures/papers/paper_list_l17_https_openaccess_thecvf_com_content_CVPR2026_html_Sun_Tracking_Guided_4D/figures/009_Figure_6.jpg]]
*Figure 6: Video Generation Ablation. Best viewed by zooming in*

### 失败模式与局限

论文未明确报告失败案例或局限性分析。从消融实验中可推断，当点跟踪器在遮挡严重或运动幅度极大的场景下失效时，对应监督的质量可能下降，进而影响视频生成的时序一致性。此外，两阶段框架的级联特性意味着第一阶段的生成误差会传播至 4D 重建阶段，但文中未对此进行量化分析。这些潜在问题需要在实际部署中进一步验证。

### 补充图表

![[assets/figures/papers/paper_list_l17_https_openaccess_thecvf_com_content_CVPR2026_html_Sun_Tracking_Guided_4D/figures/007_Table_1.jpg]]
*Table 1: Video Generation quantitative comparison on datasets: Diffusion4D (left); Animate3D (right)*

![[assets/figures/papers/paper_list_l17_https_openaccess_thecvf_com_content_CVPR2026_html_Sun_Tracking_Guided_4D/figures/006_Figure_5.jpg]]
*Figure 5: Video Generation qualitative comparison on Diffusion4D dataset. Best viewed with zoom*

![[assets/figures/papers/paper_list_l17_https_openaccess_thecvf_com_content_CVPR2026_html_Sun_Tracking_Guided_4D/figures/008_Table_4.jpg]]
*Table 4: Ablation studies: Video Generation (left); 4D Generation (right)*

![[assets/figures/papers/paper_list_l17_https_openaccess_thecvf_com_content_CVPR2026_html_Sun_Tracking_Guided_4D/figures/010_Figure_7.jpg]]
*Figure 7: 4D Generation Ablation. Best viewed by zooming in*

## 方法谱系与知识库定位

Track4DGen 的核心技术路线属于**“多视图视频扩散 + 4D 高斯泼溅重建”**的两阶段 4D 生成范式。其方法谱系可沿两条轴线展开：一是多视图视频扩散模型的演进，二是动态 3D/4D 表征与重建技术的发展。

### 与多视图视频扩散基线的关系

Track4DGen 的视频生成主干直接建立在 **Animate3D**（Jiang et al., NeurIPS 2024）和 **4Diffusion**（Zhang et al., NeurIPS 2024）等多视图视频扩散模型之上。这些基线模型通过将多视图 3D 注意力与时空注意力机制融入视频扩散 U-Net，实现了从静态 3D 模型多视图渲染到动态多视图视频的生成。然而，它们仅依赖像素空间或潜空间的标准扩散损失进行监督，缺乏对中间特征层时序一致性的显式约束。

Track4DGen 的关键突破在于：**在扩散 U-Net 解码器的第二个时空上采样块的特征空间中，注入基于基础跟踪器 CoTracker3 的密集点对应监督**。这一设计并非简单的损失函数叠加，而是源于一个因果发现——该特定层的特征展现了最强的跨帧时序对应能力。通过引入对应损失 $\mathcal{L}_{\mathrm{corr}}$ 和位置损失 $\mathcal{L}_{\mathrm{pos}}$，Track4DGen 将原本隐式的时序一致性需求转化为显式的特征级约束，从而有效抑制了外观漂移。这一思路与近期在视频编辑和生成中引入光流或点跟踪先验的工作形成呼应，但将其系统性地嵌入多视图扩散训练流程并验证其对下游 4D 重建的增益，是本文的独特贡献。

### 与 4D 生成基线的关系

在 4D 生成层面，Track4DGen 与以下几类方法形成对比：

- **单图像到 4D 生成方法**：如 **DreamGaussian4D (DG4D)**（Ren et al., arXiv 2023）和 **EG4D**（Sun et al., ICLR 2025）。这类方法从单张图像出发，依赖 SDS（Score Distillation Sampling）损失从预训练扩散模型中蒸馏 4D 先验。其优势在于输入灵活，但受限于单视图信息，难以保证多视角几何一致性和复杂运动的准确性。Track4DGen 通过先生成多视图视频再重建的两阶段策略，天然具备更强的多视角约束。

- **单目视频到 4D 生成方法**：如 **SV4D**（Xie et al., arXiv 2024）和 **SC4D**（Wu et al., ECCV 2024）。这类方法从单目视频重建 4D 资产，面临严重的遮挡和视角缺失问题。Track4DGen 的多视图视频生成阶段从根源上缓解了这一问题，提供了更完整的时空观测。

- **Animate3D 的 4D 重建部分**：作为最直接的基线，Animate3D 的 4D-GS 重建仅使用 Hex-plane 特征建模运动。Track4DGen 对此进行了两处关键改进：一是引入**混合运动表示**，将携带跟踪先验的扩散特征与 Hex-plane 特征拼接，使运动场学习受益于扩散模型已习得的时序对应知识；二是引入**4D 球谐函数（4D SH）外观模型**，用傅里叶级数参数化球谐系数以建模颜色随时间的变化，提升了动态外观的保真度。

### 适用边界与局限

根据论文提供的实验设置与方法描述，Track4DGen 的适用边界可归纳如下：

1. **输入依赖**：方法要求输入一个静态 3D 模型（带纹理的网格或 3D 高斯表示）和一段文本运动描述。对于缺乏高质量 3D 资产的场景，需前置 3D 生成或重建步骤。

2. **运动类型**：实验主要在 Diffusion4D 和 Animate3D 数据集上进行，这些数据集中的运动多为刚体或铰接式运动（如动物行走、物体旋转）。对于流体、烟雾等非刚性拓扑变化剧烈的运动，密集点跟踪的可靠性可能下降，方法的有效性需要进一步验证。

3. **计算开销**：两阶段流程涉及多视图视频扩散生成、CoTracker3 密集跟踪、以及 4D-GS 重建与 4D-SDS 蒸馏，计算成本显著高于单阶段方法或轻量级基线。

4. **论文未报告的局限**：论文未明确讨论长视频生成（如超过 32 帧）时的跟踪漂移累积问题，也未涉及多物体交互场景下的遮挡处理策略。此外，4D-SDS 损失可能引入类似 SDS 的过度平滑或色彩偏移问题，尽管 4D SH 建模部分缓解了这一点，但该风险在论文中未被量化分析。

### 开放问题

基于方法设计与实验分析，以下问题值得后续探索：

- **跟踪器选择与泛化性**：CoTracker3 作为基础跟踪器提供了强先验，但其在极端运动模糊、大位移遮挡下的表现是否成为整个流程的性能瓶颈？替换为其他跟踪器（如 TAPIR、OmniMotion）是否会改变生成特性？

- **特征层级的选择**：论文通过实验确定 U-Net 解码器第二个上采样块的特征最优，但该结论是否跨模型架构、跨数据集泛化仍待验证。是否存在更优的特征组合策略（如多尺度特征融合）？

- **单阶段联合优化的可能性**：当前两阶段设计虽然模块化清晰，但扩散特征到 4D-GS 的传递是单向的。是否可以通过可微跟踪或端到端训练实现视频生成与 4D 重建的联合优化，从而进一步提升一致性？

## 原文 PDF

![[paperPDFs/CVPR_2026/Tracking_Guided_4D_Generation_Foundation_Tracker_Motion_Priors_for_3D_Model_Animation.pdf]]