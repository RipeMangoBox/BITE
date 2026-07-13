---
title: "Portrait3D: Text-Guided High-Quality 3D Portrait Generation Using Pyramid Representation and GANs Prior"
type: paper
paper_level: A
venue: SIGGRAPH
year: 2024
pdf_ref: paperPDFs/SIGGRAPH_2024/Portrait3D_Text_Guided_High_Quality_3D_Portrait_Generation_Using_Pyramid_Representation_and_GANs_Prior.pdf
project_link: null
code_link: null
aliases:
- Portrait3D
tags:
- SIGGRAPH_2024
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
- topic/generative_models_diffusion
- topic/representation_self_supervised_transfer
core_operator: 引入金字塔三角网格（pyramid tri-grid）作为多分辨率三维表示，缓解单分辨率特征图造成的高频网格伪影；利用预训练3D感知GAN（3DPortraitGAN）提供的联合几何-外观先验作为生成起点。
primary_logic: 先从预训练3D感知GAN的隐空间投影文本对齐的图像，获得结构合理的初始三角网格；再结合分数蒸馏采样和扩散模型图像细化，交替优化三维表示，从而生成视角一致、高保真的三维肖像。
claims:
- We present Portrait3D, a novel neural rendering-based framework with a novel joint geometry-appearance prior to achieve text-to-3D-portrait generation.
- We integrate a novel pyramid tri-grid 3D representation into 3DPortraitGAN to mitigate 'grid-like' artifact.
- 3DPortraitGAN learns a joint distribution of portrait geometry and appearance, serving as a robust prior.
- Pyramid tri-grid reduces grid-like artifacts compared to naive tri-grid, confirmed by score distillation sampling experiments.
---

# Portrait3D: Text-Guided High-Quality 3D Portrait Generation Using Pyramid Representation and GANs Prior

> [!tip] 核心洞察
> 先从预训练3D感知GAN的隐空间投影文本对齐的图像，获得结构合理的初始三角网格；再结合分数蒸馏采样和扩散模型图像细化，交替优化三维表示，从而生成视角一致、高保真的三维肖像。

| 字段 | 内容 |
|------|------|
| 中文题名 | Portrait3D：基于金字塔表示和GAN先验的文本引导高质量3D肖像生成 |
| 英文题名 | Portrait3D: Text-Guided High-Quality 3D Portrait Generation Using Pyramid Representation and GANs Prior |
| 会议/期刊 | SIGGRAPH 2024 |
| Links |  [paper](https://arxiv.org/abs/2404.10394)|
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction #topic/generative_models_diffusion #topic/representation_self_supervised_transfer |
| Method | Portrait3D |
| Dataset | 25 distinct prompts, User Study |

> [!tip] 效果简介
> - 25 distinct prompts (color ■ in Table 1) 上，FID (lower is better) 110.6 vs other text-to-3D methods (see Table 1 for concrete numbers) (Portrait3D achieves the lowest FID among all compared methods)；CLIP Score (higher is better) 0.80 vs other text-to-3D methods (see Table 1) (Portrait3D achieves the highest CLIP Score among all compared methods)。
> - User Study 上，Quality / Alignment (mean opinion score) 4.77 vs other text-to-3D methods (see Table 1) (Portrait3D ranks first in both quality and alignment (25-prompt setting))。

## 概要

**问题瓶颈**。现有文本到三维肖像方法普遍依赖几何先验（如SMPL、FLAME），缺乏鲁棒的联合几何‑外观先验，导致生成结果出现纹理不一致、过饱和、过度平滑及Janus问题（多视角面部错乱）。

**核心思路**。Portrait3D 将预训练三维感知生成对抗网络（3DPortraitGAN）作为联合几何‑外观先验，并引入**金字塔三角网格（pyramid tri‑grid）**多分辨率三维表示，以缓解单分辨率特征图引起的高频网格伪影。生成时，先从GAN隐空间投影文本对齐的图像获得结构合理的初始三角网格，再结合分数蒸馏采样（SDS）与扩散模型图像细化交替优化三维表示，从而实现视角一致、高保真的三维肖像生成。

**方法定位**。在方法谱系上，Portrait3D 区别于 DreamFusion（Poole et al., ICLR 2023）、LucidDreamer（Liang et al., 2023）等通用文本到三维框架，也不同于 TADA（Liao et al., 2023）、AvatarCraft（Jiang et al., ICCV 2023）、AvatarStudio（Zhang et al., 2023c）、HumanGaussian（Liu et al., 2023b）、AvatarVerse（Zhang et al., 2023a）、HumanNorm（Huang et al., 2023a）、SEEAvatar（Xu et al., 2023b）、TECA（Zhang et al., 2024）等面向人体/肖像的文本到三维方法。其关键差异在于：（1）采用金字塔三角网格替代单分辨率三平面/三角网格表示；（2）以三维感知GAN提供的联合几何‑外观先验替代纯几何先验或随机初始化；（3）在SDS优化后引入扩散模型驱动的图像细化步骤。

**主要结果**。在25个不同文本提示的基准测试中，Portrait3D 的FID（110.6）与CLIP Score（0.80）均优于对比方法；用户研究中，质量与文本对齐的平均意见得分均为最高（4.77）。消融实验证实，金字塔三角网格显著减少网格状伪影，而GAN先验与扩散优化联合缓解了Janus问题并提升整体真实感。

**局限与待解决问题**。当前方法偶发非规范视角畸变，扩散模型可能将背景语义错误注入前景纹理（如“雪山”出现在头发上），部分生成结果存在前后视图语义不一致，复杂发型（如辫子）可能产生异常几何。此外，方法仅覆盖头‑颈‑肩区域，尚未扩展到全身肖像。这些方向有待后续工作探索。

文本到三维生成近年来取得了显著进展，但将这一范式应用于高质量三维肖像的自动生成，仍面临独特且未解决的挑战。三维肖像生成不仅要求几何结构合理、纹理细节丰富，还必须满足多视角一致性——即从不同角度观察时，人物的身份、表情和外观保持统一。现有的文本到三维方法在通用物体生成上表现尚可，但在肖像这一特定类别上暴露出系统性缺陷。

当前主流方法所依赖的先验信息存在根本性局限。以 **TADA** (Liao et al., 2023)、**AvatarCraft** (Jiang et al., ICCV 2023)、**AvatarStudio** (Zhang et al., 2023c) 等为代表的工作，通常仅引入几何先验——如 SMPL、FLAME 或 imGHUM 等参数化人体/人脸模型——来约束生成过程。这种单一模态的先验虽然能提供粗略的几何骨架，却完全忽略了外观纹理的合理分布。由此引发的后果是：生成的三维肖像普遍存在纹理不一致、色彩过饱和、表面过度平滑等问题，更严重的则表现为经典的 Janus 问题——即正面与背面视图出现语义冲突（例如正面是人脸、背面也出现人脸特征）。

从技术表征层面看，另一重瓶颈在于三维表示本身。大多数三维感知生成对抗网络（3D-aware GAN）采用基于特征图的单分辨率三平面（tri-plane）或三网格（tri-grid）表示。这类表示在高频细节区域容易引入“网格状”伪影（grid-like artifact），在纹理表面留下规律性的噪声模式，严重损害视觉质量。在分数蒸馏采样（SDS）的优化框架下，这种高频伪影会被进一步放大，因为扩散模型的梯度信号本身缺乏对三维结构连续性的显式约束。

上述双重困境——先验的片面性与表示的高频不稳定性——共同构成了文本到三维肖像生成的核心瓶颈：**缺少一个鲁棒的、联合建模几何与外观的生成先验**，同时缺乏能抑制高频伪影的多分辨率表示机制。

Portrait3D 正是在这一背景下提出的。其核心动机在于：如果能从预训练的三维感知 GAN 中提取出同时编码几何结构与外观纹理的联合先验，并将其嵌入到一个多分辨率的三维表示中，就有可能在 SDS 优化的早期阶段为生成过程提供一个结构合理、纹理自洽的初始化起点，从而系统性地缓解 Janus 问题、纹理不一致和网格伪影。这一思路将文本到三维肖像生成的关键矛盾从“从零开始约束”转化为“从合理起点细化”，构成了本文方法设计的根本出发点。

## 核心方法与创新机理

Portrait3D 的核心创新在于为文本到三维肖像生成引入了一个**鲁棒的联合几何-外观先验**，并配套设计了**金字塔三角网格表示**，从而系统性地解决了现有方法中纹理不一致、过饱和、过度平滑以及 Janus（多面）问题。与仅依赖几何先验（如 SMPL、FLAME）或随机初始化的基线方法相比，Portrait3D 在三个关键维度上实现了突破。

### 1. 联合几何-外观先验：从 3D 感知 GAN 出发

现有文本到三维肖像方法（如 **TADA** (Liao et al., 2023)、**AvatarCraft** (Jiang et al., ICCV 2023)、**AvatarStudio** (Zhang et al., 2023c)）通常仅利用参数化人体模型的几何先验来约束生成形状，缺乏对纹理和外观的联合约束。这导致生成结果在不可见视角下容易出现纹理漂移和语义不一致。

Portrait3D 的核心洞察是：**预训练的 3D 感知 GAN 已经隐式学习了肖像几何与外观的联合分布**。具体而言，作者训练了一个名为 3DPortraitGAN 的生成器，该生成器能够从隐空间编码生成视角一致的三维肖像。在文本到三维生成过程中，Portrait3D 首先将文本对齐的二维图像通过隐码逆推（latent code inversion）投影到 3DPortraitGAN 的隐空间，获得逆推隐码 $w^*$，再通过生成器得到结构合理的初始金字塔三角网格：

$$T^{\text{pyr}} = \mathcal{G}(w^*)$$

这一初始化策略使得后续的分数蒸馏采样（SDS）优化从一个已经具备合理几何和外观的起点出发，而非从随机噪声开始。消融实验（Fig. 7）证实，仅使用 GAN 先验即可显著缓解 Janus 问题；结合扩散优化后，几何真实感和外观一致性进一步提升。

### 2. 金字塔三角网格：多分辨率表示消除网格伪影

大多数基于特征图的 3D 感知 GAN（包括早期版本的 3DPortraitGAN）采用单一分辨率的 tri-plane 或 tri-grid 表示。当这些表示被用于分数蒸馏采样时，高频率的特征图会在渲染结果中引入明显的“网格状”伪影（grid-like artifacts），表现为纹理上的规则条纹或棋盘格噪声。

Portrait3D 提出了**金字塔三角网格（pyramid tri-grid）**，将多分辨率哈希编码的思想引入三维肖像表示。具体而言，金字塔三角网格由多个分辨率层级的 tri-grid 组成，分辨率集合为 $\{8, 16, 32, 64, 128, 256, 512\}$，每层通道数为 12。低分辨率层捕捉全局结构，高分辨率层补充局部细节，从而在保持几何细节的同时大幅抑制高频噪声。

Fig. 2 的分数蒸馏采样实验清晰展示了这一设计的必要性：使用高频率位置编码（positional encoding）时，生成内容出现严重的网格伪影；而多分辨率哈希编码能够在细节丰富度和噪声抑制之间取得更好的平衡。Fig. 6 的表示消融进一步证实，金字塔三角网格相比单一分辨率 tri-grid 显著减少了 T 恤等区域的网格状纹理，同时 Marching Cubes 提取的几何形状也更加平滑。

### 3. 扩散模型驱动的图像细化：弥合渲染与真实感的差距

仅依赖 SDS 损失优化的三维表示，其渲染视图在细节和真实感上仍可能与自然图像分布存在差距。Portrait3D 引入了一个**扩散模型驱动的优化步骤**：对当前渲染视图施加扩散模型的去噪过程，生成细化后的图像 $x_{\text{refined}}^c$，然后通过最小化渲染图像与细化图像之间的 $L_2$ 距离来进一步优化金字塔三角网格参数：

$$\theta^* = \arg\min_{\theta} L_{\text{optim}} = \arg\min_{\theta} L_2(x_{\text{refined}}^c, R(T^{\text{pyr}}, c, w^*))$$

这一步骤将扩散模型对自然图像分布的先验知识直接注入三维表示，有效提升了纹理细节和整体真实感。如 Fig. 7 所示，在 GAN 先验基础上叠加扩散优化后，生成肖像的几何和外观真实感均达到最佳水平。

### 创新总结

| 创新维度 | 基线方案 | Portrait3D 方案 | 证据锚点 |
|---------|---------|----------------|---------|
| 初始化先验 | 仅几何先验（SMPL/FLAME）或随机初始化 | 3D 感知 GAN 提供的联合几何-外观先验 | Section 3.4, Fig. 7 |
| 三维表示 | 单分辨率 tri-grid / tri-plane | 金字塔三角网格（7层多分辨率） | Section 3.2, Fig. 2, Fig. 6 |
| 后优化 | 无显式图像细化 | 扩散模型去噪 + L2 损失优化 | Section 3.5, Fig. 7(c) |

这三项创新协同作用：GAN 先验提供合理的生成起点，金字塔三角网格抑制优化过程中的高频伪影，扩散细化弥补渲染与自然图像的分布差距，最终实现了视角一致、高保真的文本到三维肖像生成。定量结果（Table 1）表明，Portrait3D 在 25 个提示词上的 FID（110.6）和 CLIP Score（0.80）均优于所有对比方法，用户研究中的质量和对齐度评分（4.77）也排名第一。

Portrait3D 的整体生成流程围绕一个核心思路展开：**先利用预训练 3D 感知 GAN 提供的联合几何-外观先验获得结构合理的初始三维表示，再通过分数蒸馏采样（SDS）和扩散模型图像细化交替优化该表示**，从而生成视角一致、高保真的三维肖像。整个流水线由四个关键模块串联而成，其关系与数据流可概括如下。

**1. 文本对齐的图像生成与隐码反演。**  
输入为自然语言文本提示，系统首先利用预训练扩散模型生成一张与文本语义对齐的二维肖像图像。随后，对该图像执行隐码优化（latent code optimization），将其反演至 3D 感知 GAN（3DPortraitGAN）的隐空间中，得到逆推隐码 $w^{*}$。此步骤的因果作用是：将文本语义转换为一个可被 3D 生成器直接解码的隐变量，为后续三维生成提供语义锚点。

**2. 金字塔三角网格生成。**  
逆推隐码 $w^{*}$ 被送入 **3D 感知金字塔三角网格生成器** $\mathcal{G}$，生成多分辨率金字塔三角网格（pyramid tri-grid）：
$$T^{\mathrm{pyr}} = \mathcal{G}(w^{*})$$
该金字塔三角网格由分辨率集合 $\{8, 16, 32, 64, 128, 256, 512\}$ 的多个三角网格组成，每个分辨率的通道数为 12。与单分辨率三角网格相比，这一多分辨率设计能够有效缓解高频特征图导致的“网格状”伪影（grid-like artifact），同时保留精细几何细节（图 6 消融实验证实了这一点）。

**3. 神经渲染与分数蒸馏采样（SDS）。**  
给定金字塔三角网格 $T^{\mathrm{pyr}}$、相机参数 $c$ 和隐码 $w^{*}$，神经渲染器 $R$ 通过体渲染生成二维 RGB 图像：
$$x_{\mathrm{rgb}} = R(T^{\mathrm{pyr}}, c, w^{*})$$
在此基础上，系统利用预训练扩散模型 $\phi$ 对渲染图像施加分数蒸馏采样损失，其梯度形式为：
$$\nabla_{\boldsymbol{\theta}} \mathcal{L}_{\mathrm{SDS}}(\phi, x) \triangleq \mathbb{E}_{t,\epsilon} \left[ \omega(t) (\hat{\epsilon}_{\phi}(z_{t}; y, t) - \epsilon) \frac{\partial z_{0}}{\partial x} \frac{\partial x}{\partial \boldsymbol{\theta}} \right]$$
该梯度反向传播至金字塔三角网格参数 $\boldsymbol{\theta}$，驱动渲染视图逐步与文本提示 $y$ 对齐。SDS 在此扮演“知识蒸馏”角色，将扩散模型中的二维语义先验迁移至三维表示。

**4. 扩散模型图像细化与 L2 优化。**  
SDS 优化后，系统进一步引入扩散模型对渲染视图进行去噪细化，得到高质量参考图像 $x_{\mathrm{refined}}^{c}$。随后，通过最小化细化图像与渲染图像之间的 L2 距离来微调金字塔三角网格：
$$\theta^{*} = \arg\min_{\theta} \, L_{2}\big(x_{\mathrm{refined}}^{c}, R(T^{\mathrm{pyr}}, c, w^{*})\big)$$
这一步骤有效弥补了 SDS 在纹理细节和真实感方面的不足，消融实验（图 7）表明，该模块与 GAN 先验联合使用可显著缓解 Janus 问题并提升整体逼真度。

**流水线中的冻结策略。**  
在整个优化过程中，3D 感知金字塔三角网格生成器 $\mathcal{G}$ 和神经渲染器 $R$ 的参数保持冻结（图 4 中以 “66%33” 标注冻结的子模块或表示），仅金字塔三角网格参数 $\boldsymbol{\theta}$ 被更新。这种设计保证了 GAN 先验的稳定性，避免优化过程中发生模式坍塌。

**输入输出总结。**  
- **输入**：自然语言文本提示（如 “a waiter in a restaurant, red and black uniform”）。  
- **输出**：可进行多视角体渲染的带纹理三维肖像，覆盖头、颈、肩区域。  
- **运行效率**：在单张 NVIDIA RTX 4090 上约需 0.5 小时生成一个三维肖像；在 12 GB 显存的 RTX 3080Ti 上约需 1.5 小时，相比部分基线方法具有更低的硬件门槛。

### 补充图表

![[assets/figures/papers/paper_list_l6_Portrait3D_Text_Guided_High_Quality_3D_Portrait_Generation_Using_Pyramid_motion20v/figures/004_Figure_4.jpg]]
*Figure 4: The 3D portrait generation pipeline of Portrait3D. The*

Portrait3D 的生成管线由四个核心模块串联构成，其关键创新在于**金字塔三角网格表示**与**3D感知GAN联合先验**的引入。

### 金字塔三角网格生成器（3DPortraitGAN）

该模块是整个框架的生成起点与先验载体。其架构在二维StyleGAN骨干中嵌入一个3D感知分支，以增强不同特征图之间三维关联位置的特征通信（Fig. 3）。生成器从隐码 $w^{*}$ 出发，在多个分辨率层级上输出一组三角网格，构成金字塔三角网格 $T^{\mathrm{pyr}}$：

![[assets/figures/papers/paper_list_l6_Portrait3D_Text_Guided_High_Quality_3D_Portrait_Generation_Using_Pyramid_motion20v/figures/003_Figure_3.jpg]]
*Figure 3: The architecture of the 3D-aware pyramid tri-grid generator in 3DPortraitGAN . The pyramid tri-grid is composed of tri-grids generated at different layers. For the sake of simplicity and clarity, we omit the latent code modulation applied to each block*

$$T^{\mathrm{pyr}} = \mathcal{G}(w^{*})$$

其中 $\mathcal{G}$ 为3D感知金字塔三角网格生成器。金字塔三角网格由分辨率集合 $\{8, 16, 32, 64, 128, 256, 512\}$ 的多个三角网格组成，每个网格通道数为12。这一多分辨率设计是缓解单分辨率三角网格高频特征图所导致“网格状伪影”的关键手段（Fig. 2, Fig. 6）。

![[assets/figures/papers/paper_list_l6_Portrait3D_Text_Guided_High_Quality_3D_Portrait_Generation_Using_Pyramid_motion20v/figures/002_Figure_2.jpg]]
*Figure 2: The results of score distillation sampling for 3D content generation (top) and texture generation (bo om), using positional encoding with a different number of frequencies (a,b), and multi-resolution hash encoding (c). The same prompt, “a hamburger”, was used for a fair comparison*

![[assets/figures/papers/paper_list_l6_Portrait3D_Text_Guided_High_Quality_3D_Portrait_Generation_Using_Pyramid_motion20v/figures/006_Figure_6.jpg]]
*Figure 6: The pyramid tri-grid is crucial for alleviating the “grid-like” artifacts. We showcase renderings of results obtained utilizing the two 3D representations (w/ and w/o optimization), accompanied by shapes extracted using Marching Cubes*

### 神经渲染器

神经渲染器 $R$ 接收金字塔三角网格 $T$、相机参数 $c$ 和隐码 $w$，通过体渲染生成RGB图像：

$$x_{\mathrm{rgb}} = R(T, c, w)$$

该模块在SDS优化和扩散细化阶段反复调用，为2D扩散模型提供可微分的渲染视图。

### 分数蒸馏采样

SDS模块将预训练扩散模型的知识蒸馏到金字塔三角网格参数 $\boldsymbol{\theta}$ 中，使渲染图像与文本提示 $y$ 对齐。SDS损失的梯度形式为：

$$\nabla_{\boldsymbol{\theta}} \mathcal{L}_{\mathrm{SDS}}(\phi, x = R(T^{\mathrm{pyr}}, c, w^{*})) \triangleq \mathbb{E}_{t,\epsilon} \left[ \omega(t) (\hat{\epsilon}_{\phi}(z_{t}; y, t) - \epsilon) \frac{\partial z_{0}}{\partial x} \frac{\partial x}{\partial \boldsymbol{\theta}} \right]$$

其中 $\phi$ 为预训练扩散模型，$\epsilon$ 为真实噪声，$\hat{\epsilon}_{\phi}$ 为条件噪声预测，$z_t$ 为加噪后的潜变量，$\omega(t)$ 为时间步权重。该梯度直接驱动金字塔三角网格参数的更新。

### 扩散优化

在SDS阶段之后，Portrait3D引入一个额外的扩散细化步骤：对渲染视图进行扩散去噪得到细化图像 $x_{\mathrm{refined}}^{c}$，再通过最小化L2距离进一步优化金字塔三角网格参数：

$$\theta^{*} = \arg\min_{\theta} L_{\mathrm{optim}} = \arg\min_{\theta} L_{2}(x_{\mathrm{refined}}^{c}, R(T^{\mathrm{pyr}}, c, w^{*}))$$

这一步骤与GAN先验联合作用，有效缓解了Janus问题并提升了几何与外观的真实感（Fig. 7）。

## 实验与关键发现

### 主实验结果

Portrait3D 在 25 个不同文本提示下与 10 个 SOTA 文本到三维方法进行了定量比较，评估指标包括 FID、CLIP Score 和用户研究（**Table 1**）。在所有对比方法中，Portrait3D 取得了最低的 FID（110.6）和最高的 CLIP Score（0.80），表明其生成结果与文本描述的语义对齐度最高，且图像质量最接近真实照片分布。用户研究方面，Portrait3D 在质量和语义对齐两个维度均排名第一，平均意见得分达到 4.77（25 提示设置），显著优于所有基线方法。

![[assets/figures/papers/paper_list_l6_Portrait3D_Text_Guided_High_Quality_3D_Portrait_Generation_Using_Pyramid_motion20v/figures/007_Table_1.jpg]]
*Table 1: antitative comparison results. The results with color ■ are derived from 25 distinct input prompts, while those with color ■ are derived from a single input prompt due to the inaccessibility of some methods*

定性对比（**Figure 5**）进一步验证了上述结论。与 DreamFusion（Poole et al., ICLR 2023）、LucidDreamer（Liang et al., 2023）、TADA（Liao et al., 2023）、AvatarCraft（Jiang et al., ICCV 2023）、AvatarStudio（Zhang et al., 2023c）、HumanGaussian（Liu et al., 2023b）、AvatarVerse（Zhang et al., 2023a）、HumanNorm（Huang et al., 2023a）、SEEAvatar（Xu et al., 2023b）、TECA（Zhang et al., 2024）等方法相比，Portrait3D 生成的肖像在多视角一致性、纹理保真度和几何合理性方面均表现出明显优势，有效抑制了过饱和、过度平滑和 Janus 问题。

![[assets/figures/papers/paper_list_l6_Portrait3D_Text_Guided_High_Quality_3D_Portrait_Generation_Using_Pyramid_motion20v/figures/005_Figure_5.jpg]]
*Figure 5: alitative comparison to SOTA text-to-3D approaches: DreamFusion [Poole et al. 2023], LucidDreamer [Liang et al. 2023], TADA [Liao et al. 2023], AvatarCra [Jiang et al. 2023], AvatarStudio [Zhang et al. 2023c], HumanGaussian [Liu et al. 2023b], AvatarVerse [Zhang et al. 2023a], HumanNorm [Huang et al. 2023a], SEEAvatar [Xu et al. 2023b], TECA [Zhang et al. 2024], and our method. The input prompt is presented at the top*

**公平性说明**：部分基线方法（AvatarStudio、HumanGaussian、SEEAvatar、TECA）因代码不可访问，仅在单一提示下评估；Portrait3D 同时提供了 25 提示和单提示结果以确保可比性。硬件需求方面，Portrait3D 可在 12GB 显存的 GPU（如 RTX 3080Ti）上运行，而若干基线方法需要更高显存。

### 消融实验

消融实验围绕两个核心设计展开：金字塔三角网格表示和 GAN 先验加扩散优化。

**金字塔三角网格的作用**（**Figure 6**）：与单分辨率三角网格相比，金字塔三角网格（分辨率集 {8,16,32,64,128,256,512}，通道数 12）显著抑制了“网格状”伪影。在 T 恤等大面积均匀纹理区域，单分辨率三角网格产生明显的高频网格纹理，而金字塔三角网格渲染结果更平滑，同时通过 Marching Cubes 提取的几何形状保留了精细结构。这一结果与 **Figure 2** 中关于多分辨率哈希编码在分数蒸馏采样中优于高频位置编码的发现一致——高频特征图是网格伪影的根源，多分辨率结构有效平衡了细节生成与噪声抑制。

**GAN 先验与扩散优化的联合作用**（**Figure 7**）：
- **(a) 无 GAN 先验、无优化（基线）**：直接在随机初始化的金字塔三角网格上应用 SDS，出现严重的 Janus 问题（前后视图均出现人脸），纹理质量低。
- **(b) 有 GAN 先验、无优化**：利用 3DPortraitGAN 的联合几何-外观先验初始化后，Janus 问题得到缓解，但纹理细节仍有不足。
- **(c) 完整方法（GAN 先验 + 扩散优化）**：几何合理性和外观真实感均显著提升，视角一致性良好。

这一消融证实了核心洞察：3DPortraitGAN 提供的联合几何-外观先验是生成结构合理肖像的起点，而扩散模型图像细化步骤进一步提升了纹理质量。

### 效率分析

在 NVIDIA RTX 4090 GPU 上，Portrait3D 生成一个三维肖像总耗时约 0.5 小时。在 12GB 显存的 RTX 3080Ti 上，处理时间约为 1.5 小时，体现了较好的硬件兼容性。

### 失败模式与局限性

**Figure 8** 系统展示了 Portrait3D 的四类典型失败案例：

1. **非规范视角畸变**（Figure 8a）：部分生成结果在极端视角下出现面部扭曲，根因在于 GAN 逆推过程未能完全纠正生成图像的视角偏差，导致隐码未能精确映射到规范空间。

2. **背景语义污染**（Figure 8b）：扩散模型可能将背景语义错误注入前景纹理，例如“雪山”提示导致头发中出现意外雪花纹理。这一问题源于 SDS 优化过程中扩散模型对全局语义的过度响应，缺乏前景-背景解耦机制。

3. **语义不一致**（Figure 8c）：前后视图语义不连贯，例如正面为 T 恤、背面变为马甲。这表明单视图 SDS 优化在多视角一致性约束方面存在不足，未观测区域的生成依赖先验外推，可能偏离文本语义。

4. **异常几何**（Figure 8d）：复杂发型（如辫子）的处理可能产生不合理的几何结构，反映了 3DPortraitGAN 先验对罕见发型的覆盖不足。

此外，当前方法仅覆盖头、颈、肩区域，无法生成完整全身肖像，限制了应用场景。

## 定位与知识库关联

### 1. 方法谱系：从通用文本到三维到专用三维肖像生成

Portrait3D 处于**文本到三维生成**与**三维感知生成先验**两条技术路线的交汇点。其核心思路是用预训练三维感知 GAN 提供的联合几何-外观先验，替代现有方法中仅依赖几何先验（如 SMPL、FLAME）或随机初始化的做法，从而缓解纹理不一致、过饱和、过度平滑以及 Janus 问题。

#### 1.1 上游基线：通用文本到三维方法

DreamFusion（Poole et al., ICLR 2023）首次提出分数蒸馏采样（Score Distillation Sampling, SDS），利用预训练扩散模型监督三维表示的优化，开创了文本到三维生成范式。LucidDreamer（Liang et al., 2023）在此基础上做了改进。然而，这类通用方法用于三维肖像时，缺乏对肖像几何与纹理联合分布的约束，导致生成结果容易出现 Janus 问题（多面脸）、纹理过饱和和几何失真。

#### 1.2 上游基线：专用文本到三维肖像/化身方法

为克服通用方法的不足，一系列工作引入了针对人体的几何先验：

- **TADA**（Liao et al., 2023）、**AvatarCraft**（Jiang et al., ICCV 2023）、**AvatarStudio**（Zhang et al., 2023c）、**SEEAvatar**（Xu et al., 2023b）、**TECA**（Zhang et al., 2024）等方法依赖 SMPL、FLAME 或 imGHUM 等参数化人体模型作为几何骨架。
- **HumanGaussian**（Liu et al., 2023b）、**HumanNorm**（Huang et al., 2023a）、**AvatarVerse**（Zhang et al., 2023a）等方法在几何先验基础上结合高斯泼溅或法线图约束。

这些方法的共同瓶颈在于：**几何先验仅提供结构约束，不包含外观信息**。因此，纹理生成完全依赖 SDS 从扩散模型中蒸馏，容易产生过饱和、过度平滑的纹理，且无法从根本上解决 Janus 问题——因为扩散模型本身缺乏对三维肖像多视角一致性的内在理解。

#### 1.3 Portrait3D 的定位与关键创新

Portrait3D 的核心突破在于**用三维感知 GAN 替代纯几何先验**。具体而言：

1. **联合几何-外观先验**：3DPortraitGAN 在大量三维肖像数据上学习了几何与纹理的联合分布，因此其隐空间编码天然携带多视角一致的几何和外观信息。以此为起点进行 SDS 优化，相当于在一个“合理肖像流形”附近进行局部搜索，而非从随机噪声出发的全局探索。

2. **金字塔三角网格表示**：现有三维感知 GAN 普遍使用单分辨率 tri-plane 或 tri-grid 特征图，其高频成分在 SDS 优化中会引发“网格状”伪影（grid-like artifact）。Portrait3D 引入多分辨率金字塔 tri-grid（分辨率集合 {8, 16, 32, 64, 128, 256, 512}，每层通道数 12），通过多尺度特征融合抑制高频噪声，同时保留细节。

3. **扩散模型后优化**：在 SDS 优化后，Portrait3D 额外引入一步扩散模型图像细化和 L2 损失优化，进一步消除残余伪影并提升真实感。

从方法谱系看，Portrait3D 可视为**从“几何先验 + SDS”范式向“GAN 联合先验 + SDS + 扩散细化”范式的跃迁**。其金字塔 tri-grid 表示在三维感知 GAN 领域具有独立的技术贡献，而 GAN 先验与扩散模型蒸馏的协同使用则为文本到三维生成提供了一种新的组合范式。

### 2. 知识库定位与适用边界

#### 2.1 适用场景

- **输入**：自然语言文本提示，描述肖像的性别、年龄、发型、服饰、表情等属性。
- **输出**：带纹理的三维头像（头、颈、肩区域），支持多视角体积渲染和 Marching Cubes 几何提取。
- **硬件需求**：可在 12GB 显存 GPU（如 NVIDIA RTX 3080Ti）上运行，生成时间约 1.5 小时；在 RTX 4090 上约 0.5 小时。

#### 2.2 不适用场景与已知局限

以下局限来自论文明确报告的失败案例（Fig. 8）和作者声明：

1. **非规范视角畸变**：GAN 逆推过程（latent code inversion）未能彻底纠正生成图像的视角偏差，偶发导致非正面视角下的几何畸变（Fig. 8a）。根源在于逆推优化缺乏显式的多视角一致性约束。

2. **背景语义污染**：扩散模型可能将背景语义错误注入前景纹理。例如，提示词包含“雪山”时，雪花纹理可能意外出现在头发或服装上（Fig. 8b）。这是因为 SDS 在像素空间进行监督，无法区分前景与背景语义。

3. **前后视图语义不一致**：部分生成结果在正面与背面呈现不一致的服饰语义，例如正面为 T 恤、背面变为马甲（Fig. 8c）。这暴露了当前方法对未观测区域缺乏显式建模的弱点。

4. **复杂发型几何异常**：对辫子等复杂发型，可能产生不合理的几何结构（Fig. 8d）。

5. **区域限制**：当前方法仅覆盖头、颈、肩区域，无法生成完整全身肖像。

### 3. 开放问题与未来方向

基于上述局限，论文隐含或明确指向以下开放问题：

1. **逆推过程的约束增强**：如何对 GAN 逆推施加额外的多视角几何约束，以消除非规范视角畸变？可能的思路包括引入显式的三视角一致性损失，或利用预训练多视角扩散模型引导逆推方向。

2. **语义分离与前景保护**：如何阻止扩散模型将背景语义错误注入前景纹理？这需要在前景-背景语义分离的表示空间中进行 SDS 蒸馏，而非在统一的像素空间中操作。

3. **几何感知的扩散模型**：当前 SDS 使用的扩散模型是二维的，缺乏三维几何感知能力。利用更鲁棒的几何感知扩散模型（如基于深度或法线图条件的扩散模型）修复语义不一致和异常几何，是一个有前景的方向。

4. **全身肖像扩展**：将当前框架从头肩区域扩展到全身肖像，需要处理更大的空间范围、更复杂的关节结构和服饰变形，对三维表示容量和 GAN 先验的泛化能力提出更高要求。

5. **替代蒸馏方案**：是否可应用变分得分蒸馏（Variational Score Distillation, VSD）等替代方案进一步降低过饱和和过度平滑？VSD 通过引入额外的变分分布可能提供更丰富的纹理细节。

6. **未观测区域的显式建模**：当前方法对不可见面（如后脑勺）的生成缺乏显式监督，导致前后语义不一致。引入多视角一致性约束或对称性先验，可增强未观测区域的生成质量。

---

**证据强度说明**：以上分析基于论文提供的 25 提示词定量评估（Table 1）、消融实验（Fig. 6, Fig. 7）和失败案例分析（Fig. 8）。用户研究结果（质量评分 4.77/5）来自大学生群体，可能反映特定人口统计偏差。部分基线方法（AvatarStudio、HumanGaussian、SEEAvatar、TECA）仅在一个提示词下评估，完整 25 提示词对比的公平性需进一步验证。

## 原文 PDF

![[paperPDFs/SIGGRAPH_2024/Portrait3D_Text_Guided_High_Quality_3D_Portrait_Generation_Using_Pyramid_Representation_and_GANs_Prior.pdf]]
