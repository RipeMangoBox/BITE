---
title: "Neural Brushstroke Engine: Learning a Latent Style Space of Interactive Drawing Tools"
type: paper
paper_level: A
venue: "SIGGRAPH Asia"
year: 2022
pdf_ref: paperPDFs/SIGGRAPH_ASIA_2022/Neural_Brushstroke_Engine_Learning_a_Latent_Style_Space_of_Interactive_Drawing_Tools.pdf
code_link: null
project_link: https://research.nvidia.com/labs/toronto-ai/brushstroke_engine/
aliases:
- NBE
- NBELLSSIDT
tags:
- SIGGRAPH_ASIA_2022
- topic/generative_models_diffusion
- topic/generative_models_diffusion/generative_models_and_autoencoders
core_operator: "基于StyleGAN2的条件生成器，将潜在向量z映射为画笔风格编码(w+)，注入用户笔画几何特征，并输出alpha-color参数化表示，从而在同一模型中实现风格多样性与交互控制。"
primary_logic: "将GAN学习连续图像分布的能力拓展到学习画笔风格空间，使得单个模型可生成多种风格，并通过补丁级生成和特征空间混合实现任意画布上的无缝、实时绘画。"
claims:
- "conditional GAN model learns latent space of drawing styles from ~200 unlabeled images"
- "Generator outputs alpha-color parametrization allowing recoloring, compositing and formulating a geometric loss"
- "We design a generator that natively outputs soft alpha maps for compositing"
- "Feature-space blending achieves nearly seamless stitching for most styles"
---

# Neural Brushstroke Engine: Learning a Latent Style Space of Interactive Drawing Tools

> [!tip] 核心洞察
> 将GAN学习连续图像分布的能力拓展到学习画笔风格空间，使得单个模型可生成多种风格，并通过补丁级生成和特征空间混合实现任意画布上的无缝、实时绘画。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 神经笔触引擎：学习交互式绘图工具的潜在风格空间 |
| 英文题名 | Neural Brushstroke Engine: Learning a Latent Style Space of Interactive Drawing Tools |
| 会议/期刊 | SIGGRAPH Asia 2022 |
| Links | [paper](https://drive.google.com/file/d/1RNFgMXEp85MGlV6w99JC_MBBg45TFgzI/view) · [Project](https://research.nvidia.com/labs/toronto-ai/brushstroke_engine/) |
| Topic | #topic/generative_models_diffusion #topic/generative_models_diffusion/generative_models_and_autoencoders |
| Method | Neural Brushstroke Engine |
| Dataset | Styles1 (real stroke geometry), Styles1 (various input geometries), User study (7 digital artists) |

> [!tip] 效果简介
> - Styles1 (real stroke geometry) 上，FID 为 70.137，对比 74.74 (DRIT++)，变化 -4.603 (↓)。
> - Styles1 (various input geometries) 上，Style consistency 为 ✓ (consistent)，对比 ✗ (DRIT++ fails)，变化 N/A。
> - User study (7 digital artists) 上，Likert score (5-point, likelihood of use) 为 4/6 scored 5，对比 N/A，变化 N/A。

## 概要

### 问题背景

传统数字绘画工具通常针对单一媒介（如水彩、油画）进行精细物理模拟，需要大量工程开发，难以在一个轻量级工具箱中支持多种风格。同时，现有的图像生成与翻译方法（如MUNIT、DRIT++）不支持实时交互绘画所需的**局部笔触控制**、**背景分离**和**颜色直接替换**，无法满足绘画工具对可控性、实时性和风格多样性的基本需求。

### 核心方法

本文提出**神经笔触引擎**（Neural Brushstroke Engine），核心思路是将GAN学习连续图像分布的能力拓展到学习**画笔风格空间**。具体而言，该方法基于**StyleGAN2**构建条件生成器，将潜在向量 $z$ 映射为画笔风格编码（$\mathcal{W}+$ 空间），同时注入用户笔画的几何特征，输出一种**alpha-color参数化表示**（3个alpha通道 + 3个RGB颜色），从而在同一模型中实现：
- **风格多样性**：从约200张无标签图像中学习多种绘画风格；
- **交互控制**：支持颜色直接替换、背景分离合成和几何约束。

### 方法定位

该方法在生成模型谱系中处于**条件GAN与交互式工具的交叉点**。区别于无监督图像翻译方法（如MUNIT、DRIT++）和标准StyleGAN2，其关键改动包括：输出端引入ToTriad层实现alpha-color分解；通过几何编码器将用户笔画注入生成过程；训练中增加几何损失和微调损失以提升背景清晰度和几何遵循度。系统层面，设计了支持任意画布实时绘画的引擎，利用补丁级生成和特征空间混合实现无缝拼接。

### 主要结果

- **定量对比**：在Styles1数据集上，本方法生成器的FID（70.137）优于基线方法DRIT++（74.74），且在不同输入几何下保持风格一致性，而DRIT++出现风格不一致（Fig.14, Table 2）。
- **定性验证**：7位数字艺术家参与的用户研究中，4/6给出最高分（5分Likert量表），表明该方法作为绘画工具的可接受度。
- **消融实验**：ToTriad层虽使FID上升约4倍，但视觉质量提升；几何损失与标准GAN损失结合的训练变体（F和I）获得最低中位FID和高背景清晰度（Fig.9c）。

### 局限与开放问题

训练数据量小（约200张），可能限制风格多样性；模型在新风格上需微调才能改善背景清晰度，不能即插即用；CLIP搜索对艺术术语理解有限，可能产生不匹配。未来方向包括：提高对不可控风格的交互能力、在无配对笔画几何输入下实现风格嵌入、以及将可微分笔触渲染器与强化学习结合以改进基于笔画的风格化。

数字绘画工具的核心矛盾在于**表现力与通用性之间的权衡**。传统专业软件（如Corel Painter、Rebelle）通过复杂的物理模拟或手工设计的纹理管线，能够高度逼真地再现特定媒介（如水彩、油画、铅笔）的笔触效果。然而，这种精细模拟需要大量的工程开发，且每种风格本质上是一个独立的系统，难以在一个轻量级工具箱中同时支持数十种风格。另一方面，通用绘画工具虽然灵活，但缺乏对真实画笔纹理、颜料混合和介质交互的精细控制，无法满足艺术家的表现需求。

与此同时，深度生成模型（尤其是GAN）在图像生成领域取得了显著进展，但将这些模型直接应用于交互式绘画工具面临根本性障碍。**Table 1** 系统比较了现有数字媒体工具和条件生成模型在五项基本绘画需求（R1-R5）上的支持情况：局部控制（R1）、背景分离（R2）、颜色直接替换（R3）、实时反馈（R4）和风格多样性（R5）。分析表明，无监督图像到图像翻译方法（如 **Linear Style** (Li et al., CVPR 2019)、**MUNIT** (Huang et al., ECCV 2018)、**DRIT++** (Lee et al., IJCV 2020)）虽然能生成多样化纹理，但无法保证风格一致性——同一风格在不同输入几何形状下可能产生截然不同的外观（见 **Fig. 14**）。更重要的是，这些方法输出的是RGB图像而非可分离的alpha-color表示，因此无法原生支持背景合成和直接颜色控制，而这正是绘画工具的基本需求。

本文的核心动机源于一个关键观察：**GAN学习连续图像分布的能力可以被重新定向为学习画笔风格空间**。具体而言，如果我们将画笔风格编码为潜在向量，并条件化生成过程以遵循用户输入的笔画几何，那么单个模型就有潜力生成多种风格，同时保持交互式绘画所需的局部控制、背景分离和颜色替换能力。这一思路将问题从“为每种媒介构建独立模拟器”转变为“学习一个可导航的风格流形”，从根本上改变了画笔工具的构建范式。

然而，实现这一目标面临三个技术瓶颈。第一，生成器的输出必须支持**原生alpha合成**，使得笔触能够无缝叠加到任意画布上，而非简单地将整块区域替换为生成图像。第二，模型必须在**补丁级别**上工作，以支持任意尺寸画布上的实时绘画，同时保证相邻补丁之间的无缝拼接。第三，训练数据极为有限——本文仅使用约200张未标注的不同媒介笔触图像，这就要求模型具备从稀疏样本中学习连续风格空间的能力。这些约束共同定义了**神经笔触引擎（Neural Brushstroke Engine）** 的设计空间：一个基于StyleGAN2的条件生成器，通过alpha-color参数化输出、几何特征注入和特征空间混合，在同一框架内实现风格多样性与交互控制的统一。

## 核心方法与创新机理

Neural Brushstroke Engine 的核心创新在于将 StyleGAN2 的连续图像分布建模能力拓展到**画笔风格空间**的学习，通过四个关键设计实现了单一模型支持多种风格、实时交互绘画的目标。

**1. Alpha-Color 参数化输出（§3.2, Fig. 3）**

传统图像生成模型直接输出 RGB 图像，无法支持绘画所需的背景分离、颜色替换和合成控制。本工作将生成器输出改为 **alpha-color 三元组**：3 个 alpha 通道 $A = (\alpha_0, \alpha_1, \alpha_2)$ 和 3 个 RGB 颜色 $c = (c_0, c_1, c_2)$，最终图像通过 alpha 合成得到：

$$\mathbf{x} = \Sigma_i \alpha_i \cdot c_i$$

其中 $\alpha_2$ 定义为背景，$\alpha_0 + \alpha_1$ 为前景。这一参数化带来了三个关键能力：(a) **直接颜色控制**——用户可替换输出的 $c_0$ 和 $c_1$ 实现双色调色，无需后处理（Fig. 3b）；(b) **原生背景分离**——$\alpha_2$ 天然定义背景区域，支持任意画布上的合成；(c) **几何损失的基础**——$\alpha_2$ 与输入笔画的 IoU 可度量生成器对几何约束的遵循程度（Eq. 4）。

**2. 几何条件注入机制（§3.3, Fig. 2）**

与依赖随机噪声或无几何控制的 baseline 不同，本工作通过预训练的**几何编码器 $E_{geo}$** 将用户二值笔画图像 $g$ 编码为多尺度空间特征图，拼接到 StyleGAN2 合成网络的对应层。这使得生成器不仅受风格潜在向量 $w+$ 控制，还直接响应笔画的空间形状，实现了**局部笔触的几何可控性**——不同输入几何产生不同的 alpha 分布和纹理细节（Fig. 3a）。

**3. 训练策略与几何损失（§3.4-3.5）**

训练损失在标准 GAN 损失基础上增加了**几何损失 $\mathcal{L}_{geo}$**（以连续 IoU 度量 $\alpha_2$ 与预处理输入 $P(g)$ 的重合度）和**微调损失 $\mathcal{L}_{fine}$**（结合几何损失、LPIPS 和 L1 损失）。训练采用三阶段交替策略：几何预热、标准 GAN 更新和可选几何阶段。消融实验（Fig. 9c）表明，仅使用 GAN 损失会导致训练不稳定，而加入几何损失（变体 F 和 I）可获得最低中位 FID 和高背景清晰度。

**4. 补丁级生成与特征空间混合（§4）**

为实现任意尺寸画布上的无缝实时绘画，系统以补丁为单位生成笔触，并通过**特征空间混合**（feature-space blending）而非像素级拼接来消除接缝。绘画引擎管理脏窗口和补丁请求，使得不同风格的笔触可在同一画布上自然融合（Fig. 6, Fig. 8d）。

**与 baseline 的本质差异**

| 维度 | 现有方法（Linear Style, MUNIT, DRIT++） | 本方法 |
|------|------|------|
| 输出形式 | RGB 图像 | Alpha-color 三元组 |
| 几何控制 | 无或间接 | 几何编码器注入 |
| 颜色控制 | 后处理着色 | 直接替换输出颜色 |
| 背景处理 | 不支持或后处理 | 原生 $\alpha_2$ 定义 |
| 训练损失 | 标准 GAN | +几何损失 +微调损失 |

定量对比（Table 2）显示，本方法在 Styles1 数据集上 FID 达到 70.137，优于 DRIT++（74.74），且 DRIT++ 在不同几何输入下**无法保持风格一致性**（Fig. 14），而本方法始终输出一致的风格。

Neural Brushstroke Engine 的整体 pipeline 围绕一个核心设计展开：将 StyleGAN2 的条件生成能力改造为一个**交互式绘画工具**，其输入是用户的笔触几何图形，输出是风格化的笔触外观，并原生支持颜色控制、背景分离与画布合成。

### 核心问题与设计动机

传统数字绘画工具通常针对单一媒介进行精细模拟，需要大量工程开发，难以在一个轻量级工具箱中支持多种风格。同时，现有的图像生成方法不支持实时交互绘画所需的**局部笔触控制、背景分离和颜色直接替换**。Neural Brushstroke Engine 的核心洞察在于：将 GAN 学习连续图像分布的能力拓展到学习**画笔风格空间**，使得单个模型可生成多种风格，并通过补丁级生成和特征空间混合实现任意画布上的无缝、实时绘画。

### 整体 Pipeline 架构

系统的 pipeline 由五个关键模块串联而成，形成从用户输入到画布渲染的完整闭环：

1. **Geometry Encoder $E_{geo}$**  
   用户绘制的二值笔触图像 $g$ 首先经过一个预训练的几何编码器，提取多尺度空间特征图。该编码器将原始的 $H \times H$ 二值输入转化为具有空间结构的特征表示，为后续生成器提供几何约束。

2. **Mapping Network（映射网络）**  
   随机向量 $z$ 通过映射网络被映射到 StyleGAN 的 $\mathcal{W}+$ 空间，生成代表画笔风格的潜在编码 $w+$。该编码同时编码了笔触的**介质属性**（如水彩、油画、铅笔等）和**颜色倾向**，是风格多样性的核心控制旋钮。

3. **Synthesis Network（合成网络，基于 StyleGAN2 骨干）**  
   修改后的 StyleGAN2 生成器接收两个条件信号：来自映射网络的风格向量 $w+$，以及来自几何编码器的多尺度几何特征图。几何特征通过**空间拼接**的方式注入到 StyleGAN 的各层特征图中，使生成器在保持风格一致性的同时，精确遵循用户笔触的几何形状。

4. **ToTriad Layer（三元组输出层）**  
   生成器的最后一层被替换为 ToTriad 层，输出一种**Alpha-Color (AC) 参数化表示**：3 个 alpha 通道 $A = (\alpha_0, \alpha_1, \alpha_2)$ 和 3 个 RGB 颜色 $c = (c_0, c_1, c_2)$。其中 $\alpha_2$ 被定义为背景区域，$\alpha_0 + \alpha_1$ 为前景笔触区域。最终图像通过简单的 alpha 合成得到：
   $$\mathbf{x} = \Sigma_i \alpha_i \cdot c_i$$
   这种参数化使得**颜色直接替换**（修改 $c_0, c_1$）和**背景分离**成为可能，无需后处理。

5. **Painting Engine（绘画引擎）**  
   在推理阶段，绘画引擎负责管理任意大小的画布。它根据用户笔触位置动态请求局部补丁，调用生成器进行风格化，并通过**特征空间混合**（feature-space blending）技术将补丁无缝拼接到画布上。该引擎还维护脏窗口（dirty windows）机制以支持实时交互，使得在大多数风格下实现近乎无缝的拼接效果。

### 输入输出流

- **输入**：用户绘制的二值笔触几何图形 $g$（$H \times H$ 补丁） + 风格潜在向量 $z$（或优化后的 $w+$）
- **中间表示**：AC 参数化三元组（alpha 图 + RGB 颜色）
- **最终输出**：通过 alpha 合成得到的风格化笔触图像，可被直接合成到画布上

### 训练与推理的分离

训练阶段，生成器在约 200 张无标签风格图像上学习从二值笔触到风格化笔触的映射，使用结合几何损失 $\mathcal{L}_{geo}$ 和标准 GAN 损失的混合目标。推理阶段，预训练的生成器被绘画引擎调用，通过补丁级生成和特征混合实现任意画布上的实时交互绘画，无需对每个新风格重新训练整个模型（尽管需要微调以改善背景清晰度）。

![[assets/figures/papers/paper_list_l21_https_drive_google_com_file_d_1RNFgMXEp85MGlV6w99JC_MBBg45TFgzI_view/figures/003_Figure_2.jpg]]
*Figure 2: Architecture and Training: Neural Brushstroke Engine extends StyleGAN2 architecture (striped yellow blocks) to condition image generation on stroke geometry g. Represented as a binary image, g is passed through a pre-trained Geometry Encoder to produce spatial features that are concatenated with the StyleGAN features . Instead of outpu ing RGB, the final ToTriad layer (§3.2) of our generator produces a decomposed image representation that allows recoloring, compositing and formulating a geometric loss $\mathcal { L } _ { g e o }$ (§3.4). See §3.3 for architecture details and §3.5 for training*

### 生成器输出参数化：Alpha-Color三元组

传统图像生成器直接输出RGB图像，无法支持交互式绘画所需的背景分离、颜色替换和几何控制。Neural Brushstroke Engine的核心创新在于将生成器输出重新参数化为**Alpha-Color (AC) 三元组**（§3.2）：

- **3通道Alpha图** $A = (\alpha_0, \alpha_1, \alpha_2)$：分别对应前景颜色1、前景颜色0和背景的软透明度掩码
- **3个RGB颜色** $c = (c_0, c_1, c_2)$：全局颜色向量

最终输出图像通过alpha合成得到：

$$\mathbf{x} = \Sigma_i \alpha_i \cdot c_i \quad \text{(Eq.2)}$$

其中 $\alpha_i$ 通过softmax归一化保证 $\sum_i \alpha_i = 1$。该参数化将 $\alpha_2$ 定义为背景，$\alpha_0 + \alpha_1$ 定义为前景（§3.2），使得：
- **颜色控制**：用户可直接替换 $c_0$ 和 $c_1$ 实现双色调色，无需重新生成（Fig.3b）
- **几何控制**：$\alpha_2$ 在背景区域保持稳定，为几何损失提供锚点
- **合成能力**：原生支持alpha合成，无需后处理

### 几何编码与条件注入

为将用户笔画几何信息注入生成过程，系统采用预训练的**几何编码器 $E_{geo}$**（§3.3）：

- 输入：$H \times H$ 的二值笔画图像 $\mathbf{g}$
- 输出：多尺度空间特征图，分别拼接到StyleGAN2合成网络各层对应分辨率的特征图上
- 训练方式：作为自编码器在合成笔画域上预训练，生成器训练时冻结

该设计利用神经网络的图像处理能力，将原始二值笔画转化为富含空间信息的特征表示，使生成器能够根据笔画形状和位置调整输出。

### 几何损失函数

为保证生成器输出忠实于用户输入笔画，引入**几何损失** $\mathcal{L}_{geo}$（§3.4）。首先定义连续IoU（Intersection over Union）用于灰度图像：

$$IoU(I_0, I_1) = \frac{|I_0 \cdot I_1|_s}{(|I_0 + I_1|_s - |I_0 \cdot I_1|_s)}$$

其中 $|\cdot|_s$ 表示所有像素值之和。几何损失通过计算预处理后的输入笔画 $P(\mathbf{g})$ 与输出背景alpha图 $\alpha_2$ 之间的连续IoU来度量几何遵循度：

$$\mathcal{L}_{geo}^P(\mathbf{g}, A) = IoU(P(\mathbf{g}), \alpha_2) \quad \text{(Eq.4)}$$

该损失的核心机制：当生成器在笔画区域内错误地产生前景（$\alpha_2$ 值低）时，IoU下降，驱动生成器将前景内容限制在笔画边界内。

### 微调损失

为改善背景清晰度同时保持生成外观，采用**微调损失** $\mathcal{L}_{fine}$（§3.5）：

$$\mathcal{L}_{fine}(\mathbf{g}, A, \mathbf{x}', \mathbf{x}_*') = a \mathcal{L}_{geo}(\mathbf{g}, A) + b \,\mathrm{LPIPS}(\mathbf{x}', \mathbf{x}_*') + c L1(\mathbf{x}', \mathbf{x}_*') \quad \text{(Eq.5)}$$

其中 $\mathbf{x}'$ 为当前生成图像，$\mathbf{x}_*'$ 为微调前的目标图像。该损失结合：
- 几何损失项：保持笔画几何一致性
- LPIPS感知损失：保持高层语义外观
- L1像素损失：保持底层纹理细节

### ToTriad层

生成器末端采用**ToTriad层**替代标准RGB输出层（§3.2-3.3）：
- 将StyleGAN2特征图映射为3通道alpha图（通过softmax归一化）和3个RGB颜色向量
- 该层是AC参数化的实现载体，使得后续的颜色控制、几何损失计算和alpha合成成为可能

### 背景清晰度度量

为量化风格在背景区域的可控性，定义**背景清晰度（Background Clarity, BGC）**指标（§5.2）：

$$\mathrm{BGC}_P(\mathbf{z}, \{\mathbf{g}_i\}) = \frac{\sum_i |\alpha_2(\mathbf{g}_i, \mathbf{z}) \cdot P(\mathbf{g}_i)|_s}{\sum_i |P(\mathbf{g}_i)|_s} \quad \text{(Eq.7)}$$

BGC值越高，表示背景区域越清晰（$\alpha_2$ 在非笔画区域接近1），即风格对几何输入的控制越好。该指标用于风格嵌入优化和CLIP搜索中的损失项。

## 实验与关键发现

### 核心结果：生成质量与风格一致性

论文在**Styles1**数据集（真实笔触几何）上进行了定量比较。所提出的神经笔触引擎生成器在FID指标上达到**70.137**，优于所有无监督图像到图像转换基线：Linear Style（Li et al., CVPR 2019）、MUNIT（Huang et al., ECCV 2018）和DRIT++（Lee et al., IJCV 2020）。其中DRIT++的FID为74.74，本方法降低了约4.6（**Table 2**）。

![[assets/figures/papers/paper_list_l21_https_drive_google_com_file_d_1RNFgMXEp85MGlV6w99JC_MBBg45TFgzI_view/figures/017_Table_2.jpg]]
*Table 2: antitative Comparisons: we compare our generator with other unsupervised image-to-image translation methods using FID metric*

定性比较（**Fig.14**）揭示了更关键的差异：当输入不同几何形状的笔画时，DRIT++无法生成风格一致的笔触——同一风格编码在不同几何输入下产生明显不同的视觉风格。相比之下，本方法的补丁级生成器始终保持风格一致性，这是交互式绘画工具的核心要求。

在用户研究方面，7位数字艺术家使用该系统后，在5点Likert量表上评估“使用可能性”，6人中有4人给出了最高分5分（**§7**）。

### 消融研究：架构选择与训练策略

**ToTriad层的影响**（**Fig.9c**）：添加ToTriad层（输出alpha-color参数化）导致FID相比标准StyleGAN2跳跃近4倍，但视觉质量反而提升。这一矛盾表明FID并非评估交互式画笔风格化质量的完美指标——alpha-color参数化带来的背景分离和颜色控制能力无法被FID捕捉。

**几何损失的必要性**（**Fig.9c**）：仅注入几何特征而不使用几何损失会导致训练不稳定。消融中变体F和I结合了几何损失与标准GAN损失，获得了最低的中位FID和最高的背景清晰度（BGC），验证了$L_{geo}$对训练稳定性和输出可控性的关键作用。

**预热策略**（**Fig.9c**）：跳过几何预热阶段会降低FID，表明先让生成器学习基本的几何遵循能力，再引入对抗训练，对最终质量有正面影响。

**风格嵌入优化**（**Fig.7**）：在W+空间优化噪声向量比在Z空间效果更好（**Fig.7a**），使用更多补丁（如60个）进行风格嵌入能改善对新笔画的泛化能力（**Fig.7b**）。

### 失败模式与局限性

**背景清晰度需要逐风格微调**（**Fig.4**）：模型不能即插即用。每种新风格都需要通过微调生成器和应用风格特定的alpha重新加权来改善背景区域的清晰度。微调损失（Eq.5）结合了几何损失、LPIPS和L1损失，但这一过程需要手动干预。

**风格嵌入依赖手动标记**（**Fig.12**）：从目标艺术品中提取笔刷风格需要用户手动标记纹理区域，自动化和鲁棒性不足。

**CLIP搜索的语义理解局限**（**Fig.13b**）：基于自然语言的笔刷搜索对艺术术语和颜料物理性质的理解有限。失败案例显示，某些查询会产生不匹配的风格或陷入局部最优。最近训练补丁与优化后风格的余弦相似度也表明，CLIP搜索的结果与训练数据分布有显著偏差。

**训练数据规模限制**：仅约200张无标签图像，可能限制风格多样性。模型不支持动态笔触行为（如颜料流动、串珠效果），对某些不可控风格的交互控制能力有限。

**评估局限性**：未与商业专业软件进行全面定量比较，仅依赖小规模用户研究的初步反馈。

![[assets/figures/papers/paper_list_l21_https_drive_google_com_file_d_1RNFgMXEp85MGlV6w99JC_MBBg45TFgzI_view/figures/004_Figure_3.jpg]]
*Figure 3: (b) Color Control: effect of se ing custom colors for a fixed z Fig. 3. Alpha-color (AC) parametrization: our generator outputs colors and alpha maps (§3.2), allowing color(b) and geometric control and compositing(a)*

![[assets/figures/papers/paper_list_l21_https_drive_google_com_file_d_1RNFgMXEp85MGlV6w99JC_MBBg45TFgzI_view/figures/008_Figure_7.jpg]]
*Figure 7: (c) Geometry input affects resulting control Fig. 7. Real Style Embedding: effect of various factors on latent code optimization (§5.2). All drawings ©Maria Shugrina*

![[assets/figures/papers/paper_list_l21_https_drive_google_com_file_d_1RNFgMXEp85MGlV6w99JC_MBBg45TFgzI_view/figures/010_Figure_9.jpg]]
*Figure 9: (c) Ablation studies for generator training. Fig. 9. Training Data and Ablations: refer to §6.1, §6.2 and §6.3*

![[assets/figures/papers/paper_list_l21_https_drive_google_com_file_d_1RNFgMXEp85MGlV6w99JC_MBBg45TFgzI_view/figures/002_Table_1.jpg]]
*Table 1: State-of-the art in digital media and most relevant conditional generative models or image-to-image translation models that could be employed for brushstroke stylization*

## 定位与知识库关联

### 1. 问题瓶颈与核心思路

传统数字绘画工具（如Adobe Photoshop、Corel Painter）通常针对单一媒介（油画、水彩、铅笔等）进行精细的物理模拟，开发成本高昂，难以在一个轻量级工具箱中支持多种绘画风格。同时，现有的图像生成方法（如pix2pix、CycleGAN等）虽然能进行风格迁移，但无法满足实时交互绘画所需的**局部笔触控制、背景分离和颜色直接替换**等基本需求（见Table 1）。

**Neural Brushstroke Engine** 的核心思路是将GAN学习连续图像分布的能力拓展到**学习画笔风格空间**：基于StyleGAN2的条件生成器，将潜在向量 $z$ 映射为画笔风格编码（$\mathcal{W}+$ 空间），注入用户笔画的几何特征，并输出**alpha-color参数化表示**（3个alpha通道 + 3个RGB颜色），从而在同一模型中实现风格多样性与交互控制。

### 2. 方法谱系定位

#### 2.1 与图像到图像翻译方法的对比

本文在实验中将所提方法与三类无监督图像到图像翻译基线进行了定量和定性比较（Table 2, Fig. 14）：

- **Linear Style**（Li et al., CVPR 2019）：作为无监督图像翻译基线，该方法在FID指标上表现较差，且无法保持风格一致性。
- **MUNIT**（Huang et al., ECCV 2018）：多模态无监督图像翻译方法，支持多样化的输出，但缺乏对笔触几何的精确控制。
- **DRIT++**（Lee et al., IJCV 2020）：多样化图像翻译方法，在FID指标上表现最优（74.74），但**在不同几何输入下无法生成一致的风格**（Fig. 14），这是交互式绘画的致命缺陷。

相比之下，本文方法在Styles1数据集上取得了更低的FID（70.137），同时在风格一致性上显著优于所有基线。这一优势源于两个关键设计：**补丁级生成**（patch-level generation）使得模型专注于局部笔触而非全局场景；**alpha-color参数化**实现了前景/背景的显式分离。

#### 2.2 与StyleGAN系列的关系

本文方法直接构建在**StyleGAN2**（Karras et al., 2020）的生成器骨干之上，但进行了以下关键修改：

| 修改点 | StyleGAN2原始设计 | 本文设计 |
|--------|-------------------|----------|
| 输出表示 | RGB图像 | Alpha-color三元组（通过ToTriad层） |
| 条件注入 | 无（无条件生成） | 几何编码器 $E_{geo}$ 的多尺度特征拼接 |
| 训练损失 | 标准GAN损失 | 增加几何损失 $\mathcal{L}_{geo}$ 和微调损失 $\mathcal{L}_{fine}$ |
| 潜在空间 | $\mathcal{W}$ 或 $\mathcal{W}+$ | $\mathcal{W}+$ 用于风格嵌入和搜索 |

这种继承关系使得本文方法能够利用StyleGAN2强大的图像合成能力，同时通过架构修改满足交互式绘画的特定需求。

#### 2.3 与数字绘画工具的关系

Table 1系统比较了本文方法与现有数字媒体和生成模型在五项基本绘画需求（R1-R5）上的支持程度：
- **R1（局部笔触控制）**：传统工具支持，生成模型通常不支持；本文通过几何编码器实现。
- **R2（背景分离）**：传统工具通过图层支持，生成模型不支持；本文通过alpha-color参数化原生支持。
- **R3（颜色直接替换）**：传统工具支持，生成模型需后处理；本文通过替换输出颜色 $c_0$ 和 $c_1$ 实现。
- **R4（实时交互）**：传统工具支持，生成模型通常不支持；本文通过补丁级生成和特征空间混合实现。
- **R5（多风格支持）**：传统工具需分别开发，本文通过单一模型学习风格空间实现。

### 3. 适用边界与局限

#### 3.1 训练数据依赖

模型仅使用约200张无标签图像进行训练（Fig. 9a），虽然能学习到多样的风格空间，但存在以下局限：
- 风格多样性受限于训练数据的覆盖范围，无法生成训练分布之外的全新媒介效果。
- 不支持动态笔触行为（如颜料流动、水分扩散等物理过程）。

#### 3.2 风格嵌入的自动化程度

风格嵌入需要**手动标记目标艺术品的纹理区域**（Fig. 12），自动化和鲁棒性有待提高。此外，嵌入质量依赖于优化的超参数选择（如补丁数量，Fig. 7b），需要人工调试。

#### 3.3 CLIP搜索的局限性

基于CLIP的自然语言笔刷搜索（Fig. 13）存在以下问题：
- CLIP对艺术术语和颜料物理性质的知识有限，可能导致查询与生成结果不匹配。
- 优化过程可能陷入局部最优，产生与文本描述偏离的风格（Fig. 13b）。
- 需要结合几何损失和背景清晰度约束来保证生成质量，增加了优化的复杂性。

#### 3.4 背景清晰度问题

模型在每种新风格上需要通过**微调和alpha重新加权**来改善背景清晰度（Fig. 4），不能即插即用。ToTriad层的引入虽然增强了控制能力，但也导致FID指标相比原始StyleGAN2有近4倍的跳跃（Fig. 9c）。

#### 3.5 评估的局限性

- 未与商业专业软件（如Adobe Photoshop、Corel Painter）进行全面的定量比较。
- 用户研究仅涉及7位数字艺术家，样本量较小，结论的普适性需要进一步验证。

### 4. 开放问题

1. **不可控风格的处理**：如何提高对某些不可控风格（如串珠效果）的交互控制能力？
2. **无配对几何输入的风格嵌入**：能否在无需配对的笔画几何输入下实现风格嵌入，降低用户标注成本？
3. **可微分笔触渲染**：如何将可微分笔触渲染器与强化学习结合，以改进基于笔画的风格化质量？
4. **风格空间扩展**：如何扩展到更多样化的艺术风格，并支持实时层混合和不同媒介的物理交互？
5. **CLIP搜索的领域知识集成**：如何将艺术领域知识（如颜料名称、技法术语）集成到CLIP搜索中，实现更准确的实时自然语言笔刷发现？
6. **动态笔触建模**：如何扩展模型以支持时间维度的笔触动态（如颜料干燥过程、笔触速度响应）？

### 5. 对后续工作的启示

本文提出的alpha-color参数化和几何条件注入为交互式神经绘画工具建立了新的技术范式。后续工作可以从以下方向展开：
- **数据层面**：构建更大规模、更多样化的笔触数据集，减少对微调的依赖。
- **架构层面**：探索更轻量级的生成器架构，降低推理延迟以支持更高分辨率的实时绘画。
- **交互层面**：将风格空间探索与更自然的用户界面（如语音、手势）结合，降低使用门槛。
- **评估层面**：建立标准化的交互式绘画评估基准，包括定量指标和用户研究协议。

## 原文 PDF

![[paperPDFs/SIGGRAPH_ASIA_2022/Neural_Brushstroke_Engine_Learning_a_Latent_Style_Space_of_Interactive_Drawing_Tools.pdf]]
