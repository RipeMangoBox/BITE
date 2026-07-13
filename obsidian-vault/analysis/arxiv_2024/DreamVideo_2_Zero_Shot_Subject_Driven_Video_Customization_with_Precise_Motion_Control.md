---
title: "DreamVideo-2: Zero-Shot Subject-Driven Video Customization with Precise Motion Control"
type: paper
paper_level: A
venue: arXiv
year: 2024
pdf_ref: paperPDFs/arxiv_2024/DreamVideo_2_Zero_Shot_Subject_Driven_Video_Customization_with_Precise_Motion_Control.pdf
project_link: https://dreamvideo2.github.io
code_link: null
aliases:
- D2
- DreamVideo-2
tags:
- arxiv_2024
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: 通过混合掩码参考注意力和重加权扩散损失，显式增强边界框内部区域的身份表征权重，抑制运动控制对全局的过度主导。
primary_logic: 利用模型自有的多尺度特征进行参考注意力学习，并将边界框掩码作为运动控制信号，通过区域加权的扩散损失与混合掩码注意力，在无需测试时微调的条件下实现主体学习与运动控制的平衡。
claims:
- 简单联合训练会在极少步骤内导致运动控制主导，主体身份严重退化。
- 所提方法在 mIoU 和 CD 上大幅超越基线，同时保持具有竞争力的主体保真度指标。
- 移除掩码机制、运动编码器或重加权损失均导致各项指标一致下降。
- DreamVideo-2 Test Set (50 subjects, 36 bounding boxes, 60 prompts) 上 CLIP-T / mIoU / CD↓ = 0.303 / 0.670 / 0.048
---

# DreamVideo-2: Zero-Shot Subject-Driven Video Customization with Precise Motion Control

> [!tip] 核心洞察
> 利用模型自有的多尺度特征进行参考注意力学习，并将边界框掩码作为运动控制信号，通过区域加权的扩散损失与混合掩码注意力，在无需测试时微调的条件下实现主体学习与运动控制的平衡。

| 字段 | 内容 |
|------|------|
| 中文题名 | DreamVideo-2: 零样本主体驱动的视频定制与精准运动控制 |
| 英文题名 | DreamVideo-2: Zero-Shot Subject-Driven Video Customization with Precise Motion Control |
| 会议/期刊 | arXiv 2024 |
| Links | [paper](https://arxiv.org/abs/2410.13830) · [Project](https://dreamvideo2.github.io) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/image_and_video_generation |
| Method | DreamVideo-2 |
| Dataset | DreamVideo-2 Test Set |

> [!tip] 效果简介
> - DreamVideo-2 Test Set (50 subjects, 36 bounding boxes, 60 prompts) 上，CLIP-T / mIoU / CD↓ 0.303 / 0.670 / 0.048 vs DreamVideo: 0.289 / 0.169 / 0.196 (+0.014 / +0.501 / -0.148)。
> - DreamVideo-2 Test Set (subject-only customization) 上，CLIP-T / DINO-I / DD 0.297 / 0.472 / 0.952 vs VideoBooth: 0.274 / 0.459 / 0.780 (+0.023 / +0.013 / +0.172)。
> - DreamVideo-2 Test Set (motion-only control) 上，mIoU / CD↓ 0.752 / 0.039 vs MotionCtrl: 0.497 / 0.070 (+0.255 / -0.031)。

## 概要

**问题瓶颈**：在零样本主体驱动的视频定制中，若简单地将主体学习与运动控制联合训练，运动控制信号会迅速占据主导地位，导致主体身份特征严重退化（Figure 3 (b) 和 (c)）。如何在无需测试时微调的条件下，同时保持高精度的运动控制与主体外观保真度，是该任务的核心瓶颈。

**核心方法**：DreamVideo-2 提出了一套零样本视频定制框架，仅需一张主体图像与一条边界框序列即可生成同时具备指定主体外观和运动轨迹的视频。方法的关键调控机制包括：（1）**掩码参考注意力**（Masked Reference Attention），利用模型自有的多尺度特征进行主体身份学习，并通过混合掩码（Blended Mask）显式增强边界框内部区域的身份表征权重；（2）**掩码引导运动模块**（Mask-guided Motion Module），由轻量时空编码器与空间 ControlNet 组成，从框掩码序列提取运动信息以控制主体位置；（3）**重加权扩散损失**（Reweighted Diffusion Loss），在训练时放大框内区域的噪声预测损失，抑制运动控制对全局的过度主导，从而平衡主体学习与运动控制。

**主要结果**：在自建的 DreamVideo-2 测试集（50 个主体、36 条边界框、60 条提示）上，DreamVideo-2 在联合主体与运动控制任务中取得 CLIP-T 0.303、mIoU 0.670、CD 0.048，其中 mIoU 较基线 **DreamVideo**（Wei et al., CVPR 2024）提升 0.501，CD 降低 0.148，同时保持具有竞争力的主体保真度指标（Table 2）。在单独的主体定制与运动控制任务上，方法同样显著超越 **VideoBooth**（Jiang et al., 2024）、**MotionCtrl**（Wang et al., 2024f）等基线（Table 3、Table 4）。消融实验一致表明，移除掩码机制、运动编码器或重加权损失均导致各项指标下降（Table 5、Table 6），验证了各组件的必要性。

**方法定位**：DreamVideo-2 属于零样本主体驱动视频定制方法，与需测试时微调的 **DreamVideo**（Wei et al., CVPR 2024）、**MotionBooth**（Wu et al., arXiv 2024）形成对比，同时区别于仅支持主体定制（**VideoBooth**, Jiang et al., 2024）或仅支持运动控制（**Peekaboo**, Jain et al., 2024; **Direct-a-Video**, Yang et al., 2024a; **MotionCtrl**, Wang et al., 2024f）的单任务基线。其核心贡献在于通过混合掩码注意力与重加权损失的联合设计，在零样本条件下首次实现了主体学习与运动控制的有效平衡。



### 视频定制生成的兴起与瓶颈

随着扩散模型在图像生成领域的成功，视频生成技术正快速向**可控、可定制**的方向演进。用户不仅希望生成一段视频，更希望视频中出现**特定的主体**（如自家宠物、特定商品）并按照**指定的运动轨迹**移动。这种“主体驱动+运动控制”的联合视频定制需求，在虚拟试穿、广告制作、影视预演等场景中具有巨大的应用潜力。

然而，实现这一目标面临一个核心瓶颈：**在零样本联合训练中，运动控制容易占据主导地位，导致主体身份特征劣化**。如图 3 (b) 和 (c) 所示，简单的联合训练会在极少的训练步骤内让运动控制信号压倒主体学习，使生成的主体外观严重偏离输入图像。这一现象的本质在于，运动控制信号（如边界框掩码）对全局像素施加了强约束，而主体身份的学习缺乏同等级别的显式引导，导致模型在优化过程中优先满足运动精度而牺牲了外观保真度。

### 现有方法的缺口

当前视频定制方法大致可分为三类，但均存在明显不足：

- **仅主体定制方法**（如 **VideoBooth**，Jiang et al., 2024）：能够在零样本框架下生成特定主体的视频，但完全缺乏对运动轨迹的控制能力。
- **仅运动控制方法**（如 **Peekaboo**，Jain et al., 2024；**Direct-a-Video**，Yang et al., 2024a；**MotionCtrl**，Wang et al., 2024f）：可以精确控制物体运动，但无法保持特定主体的外观身份。
- **联合定制方法**（如 **DreamVideo**，Wei et al., CVPR 2024；**MotionBooth**，Wu et al., arXiv 2024）：虽然同时支持主体和运动定制，但**需要在测试时进行微调**，且面临严重的控制冲突——运动控制与主体学习在训练中相互干扰，难以同时保持高精度的运动控制与主体外观保真度。

这些缺口揭示了一个关键问题：**如何在无需测试时微调的条件下，实现主体学习与运动控制的平衡？**

### 本文动机

本文的动机源于一个观察：视频扩散模型自有的多尺度特征已经蕴含了丰富的语义信息，可以作为主体身份学习的天然载体。同时，边界框掩码作为一种简洁的运动控制信号，可以通过区域加权的机制与主体学习形成互补而非对抗的关系。

基于这一洞察，**DreamVideo-2** 提出了一套零样本视频定制框架，核心思路是：利用模型自有的多尺度特征进行参考注意力学习，并将边界框掩码作为运动控制信号，通过**区域加权的扩散损失**与**混合掩码注意力**，在无需测试时微调的条件下实现主体学习与运动控制的平衡。这一设计直击“运动控制主导”这一瓶颈，为联合视频定制提供了新的范式。



## 核心方法与创新机理

DreamVideo-2 的核心创新在于**以零样本方式同时解决主体身份保持与精准运动控制之间的冲突**。此前的方法（如 **DreamVideo** (Wei et al., CVPR 2024) 与 **MotionBooth** (Wu et al., arXiv 2024)）虽然支持联合定制，但均需在推理时对每个新主体进行微调，且缺乏对“运动控制主导、主体退化”这一瓶颈的系统性应对。DreamVideo-2 通过四个紧密耦合的 changed slots 实现了零样本下的平衡：

### 1. 主体学习机制：从外部编码器到模型自有特征的重利用

基线方法通常依赖额外的图像编码器（如 CLIP image encoder）来提取主体特征，而 DreamVideo-2 的**参考注意力（Reference Attention）**直接复用视频扩散模型自有的多尺度特征。具体而言，从冻结的 3D UNet 中提取主体图像的中间特征 $\mathbf{Z}_s'$ 作为 Key 和 Value，以视频帧的噪声潜在特征 $\mathbf{Z}'$ 作为 Query，通过残差交叉注意力注入主体信息：

$$\mathbf{Z}'' = \mathbf{Z}' + \mathrm{Attention}(\mathbf{Q}', \mathbf{K}', \mathbf{V}')$$

这一设计避免了引入额外参数繁重的编码器，使主体学习与基础模型的特征空间天然对齐，为零样本泛化奠定基础。

### 2. 运动控制信号与模块：从轨迹操作到掩码引导的轻量控制

不同于 **Peekaboo** (Jain et al., 2024) 或 **Direct-a-Video** (Yang et al., 2024a) 等仅在注意力层操作边界框/轨迹的方法，DreamVideo-2 将边界框序列转化为**二进制框掩码** $\mathbf{M}$，并设计了一个**掩码引导运动模块（Mask-guided Motion Module）**。该模块由轻量时空编码器与空间 ControlNet 组成，以 $c_m = 1 - \mathbf{M}$ 作为控制信号，从框掩码序列中提取时空运动信息并精确控制主体在视频中的位置。这种设计使运动控制独立于主体外观学习，同时保持对位置的高精度约束。

### 3. 注意力掩码方式：混合掩码抑制运动控制对全局的过度主导

简单联合训练的核心失败模式是运动控制迅速主导训练过程，导致主体身份在极少数迭代内严重退化（Figure 3 (b)-(c)）。DreamVideo-2 引入**混合掩码（Blended Mask）**来重新分配注意力权重：

$$\hat{\mathbf{M}} = \mathbf{M} + \lambda_{\mathbf{M}} (1 - \mathbf{M})$$

其中 $\lambda_{\mathbf{M}} \in [0, 1]$ 为背景区域的衰减权重。将 $\hat{\mathbf{M}}$ 逐元素乘到参考注意力输出上，形成**掩码参考注意力（Masked Reference Attention）**：

$$\mathbf{Z}_{\mathbf{M}}'' = \mathbf{Z}' + \hat{\mathbf{M}} \cdot \mathrm{Attention}(\mathbf{Q}', \mathbf{K}', \mathbf{V}')$$

这一机制显式增强了边界框内部区域的主体特征表达，同时抑制了运动控制信号对背景区域的干扰，从而在注意力层面实现了主体学习与运动控制的解耦。

### 4. 损失函数：重加权扩散损失强化框内区域的身份学习

在损失层面，DreamVideo-2 设计了**重加权扩散损失（Reweighted Diffusion Loss）**，对边界框内部区域的噪声预测误差施加更大的惩罚权重：

$$\mathcal{L}(\theta) = \mathbb{E}_{z,\epsilon,c,t} \left[ \left( \lambda_{\mathcal{L}} \mathbf{M} + (1 - \mathbf{M}) \right) \cdot \| \epsilon - \epsilon_{\theta}(z_t, c_{\mathrm{txt}}, c_{\mathrm{img}}, c_{\mathrm{m}}, t) \|_2^2 \right]$$

其中 $\lambda_{\mathcal{L}} > 1$ 放大框内区域的损失贡献，迫使模型在训练时将更多容量分配给主体身份保持，从而对抗运动控制的自然主导倾向。消融实验（Table 6）证实，$\lambda_{\mathcal{L}} = 2$ 时各项指标达到最优平衡；过低（$\lambda_{\mathcal{L}} = 1$）导致主体保真度显著下降，过高（$\lambda_{\mathcal{L}} = 4$）则损害运动控制精度。

### 创新总结

这四个 changed slots 形成了一条完整的因果链条：**参考注意力**提供高效的主体特征注入路径，**掩码引导运动模块**提供独立的运动控制通道，**混合掩码**在注意力层面抑制两者冲突，**重加权扩散损失**在优化目标层面强制平衡。三者共同作用，使得 DreamVideo-2 首次在无需测试时微调的条件下，实现了主体外观保真度与运动控制精度的同时保持。



DreamVideo-2 是一个零样本视频定制框架，其核心目标是从**单张主体图像**与**一条边界框序列**出发，在无需测试时微调的条件下生成同时满足主体外观保真度与精准运动轨迹的视频。框架的瓶颈在于：若简单地将主体学习与运动控制进行联合训练，运动控制信号极易占据主导地位，导致主体身份特征在极少量训练步数内严重退化（见 Figure 3）。DreamVideo-2 通过三个关键设计来平衡这一冲突：**掩码参考注意力**、**掩码引导运动模块**以及**重加权扩散损失**。

整体训练流程如 Figure 2 所示，输入包含一段训练视频及其对应的边界框标注。首先，从视频中随机采样一帧，通过分割预处理获得空白背景的主体图像，以剥离背景干扰、保留纯净的身份特征。同时，将训练视频的边界框序列转换为二进制框掩码，作为运动控制信号。主体图像被视作单帧视频，与原始视频并行输入冻结的 3D UNet，在自注意力与交叉注意力层中通过掩码参考注意力将主体特征注入视频特征；框掩码序列则送入由轻量时空编码器与空间 ControlNet 组成的掩码引导运动模块，提取时空运动信息并控制主体在生成帧中的位置。两个模块均依据重加权扩散损失进行联合训练——该损失在框内区域施加更大的噪声预测权重（$\lambda_{\mathcal{L}} > 1$），以强化主体身份表征，同时保持框外区域的标准权重，避免运动控制信号被削弱。

![[assets/figures/papers/paper_list_l5_https_arxiv_org_abs_2410_13830/figures/002_Figure_2.jpg]]
*Figure 2: Overall framework of DreamVideo-2. During training, a random video frame is segmented to obtain the subject image with a blank background. The bounding boxes extracted from the training video are converted into binary box masks. Then, the subject image is treated as a single-frame video and processed in parallel with the video by masked reference attention that incorporates blended masks to learn the subject appearance. Meanwhile, box masks are fed into a motion module that includes a spatiotemporal encoder and a ControlNet for motion control. Both the masked reference attention and motion module are trained using a reweighted diffusion loss*

推理时，用户仅需提供一张主体图像和一条目标边界框序列，框架即可在零样本条件下生成定制视频，无需任何额外的微调或注意力图编辑。



### 3.1 核心瓶颈与设计动机

DreamVideo-2 面临的核心瓶颈是：在零样本联合训练中，运动控制信号（边界框掩码）容易主导优化过程，导致主体身份特征迅速退化（Figure 3）。为平衡主体学习与运动控制，方法引入三个关键设计：**掩码参考注意力**、**掩码引导运动模块**和**重加权扩散损失**。

![[assets/figures/papers/paper_list_l5_https_arxiv_org_abs_2410_13830/figures/003_Figure_3.jpg]]
*Figure 3: Illustration of motion control domination in DreamVideo-2. As seen in (b) and (c), motion control tends to dominate over subject 1 12 learning during training, causing the degradation of subject identity. In (d), our method ensures a balance between subject and motion control*

### 3.2 参考注意力机制

主体学习采用参考注意力（Reference Attention），利用视频扩散模型自有的多尺度特征进行主体外观注入。设视频帧的注意力特征为 $\mathbf{Z}'$，主体图像的注意力特征为 $\mathbf{Z}_s'$，参考注意力以残差交叉注意力的形式实现：

$$
\mathbf{Z}'' = \mathbf{Z}' + \mathrm{Attention}(\mathbf{Q}', \mathbf{K}', \mathbf{V}')
$$

其中查询 $\mathbf{Q}' = \mathbf{Z}' \mathbf{W}_Q'$，键 $\mathbf{K}' = \mathbf{Z}_s' \mathbf{W}_K'$，值 $\mathbf{V}' = \mathbf{Z}_s' \mathbf{W}_V'$。该机制使视频特征能够从主体图像特征中检索外观信息，实现零样本主体外观迁移。

### 3.3 混合掩码与掩码参考注意力

为抑制运动控制对背景区域的过度主导，方法引入混合掩码（Blended Mask）。给定二值框掩码 $\mathbf{M}$（框内为1，框外为0），混合掩码定义为：

$$
\hat{\mathbf{M}} = \mathbf{M} + \lambda_{\mathbf{M}} (1 - \mathbf{M})
$$

其中 $\lambda_{\mathbf{M}} \in [0, 1]$ 为背景权重系数（默认 $\lambda_{\mathbf{M}} = 0.75$）。该设计使背景区域获得较小的非零权重，而非完全被忽略。

掩码参考注意力（Masked Reference Attention）将混合掩码逐元素乘到注意力输出上：

$$
\mathbf{Z}_{\mathbf{M}}'' = \mathbf{Z}' + \hat{\mathbf{M}} \cdot \mathrm{Attention}(\mathbf{Q}', \mathbf{K}', \mathbf{V}')
$$

该操作显式增强边界框内部区域的主体特征表达，同时保留背景区域的微弱响应，防止运动控制信号完全覆盖主体身份信息。

### 3.4 掩码引导运动模块

运动控制信号由边界框序列转换而来。给定每帧的边界框，生成二值框掩码 $\mathbf{M}$，最终控制信号定义为 $c_m = 1 - \mathbf{M}$。掩码引导运动模块（Mask-guided Motion Module）由两部分组成：

- **时空编码器**：从框掩码序列中提取时空运动特征；
- **空间 ControlNet**：将运动特征注入冻结的 3D UNet，控制主体在视频帧中的位置。

该模块仅使用轻量的二进制掩码作为控制信号，无需复杂的轨迹或光流标注。

### 3.5 重加权扩散损失

标准扩散损失对所有空间位置赋予相同权重，导致运动控制（框外区域）与主体学习（框内区域）的优化不平衡。重加权扩散损失（Reweighted Diffusion Loss）通过放大框内区域的损失贡献来解决此问题：

$$
\mathcal{L}(\theta) = \mathbb{E}_{z,\epsilon,c,t} \left[ \left( \lambda_{\mathcal{L}} \mathbf{M} + (1 - \mathbf{M}) \right) \cdot \| \epsilon - \epsilon_{\theta}(z_t, c_{\mathrm{txt}}, c_{\mathrm{img}}, c_{\mathrm{m}}, t) \|_2^2 \right]
$$

其中：
- $\mathbf{M}$ 为二值框掩码（框内为1）；
- $\lambda_{\mathcal{L}} > 1$ 为框内区域损失权重（默认 $\lambda_{\mathcal{L}} = 2$）；
- $c_{\mathrm{txt}}$ 为文本条件，$c_{\mathrm{img}}$ 为主体图像条件，$c_{\mathrm{m}}$ 为运动控制信号。

该损失在框内区域以权重 $\lambda_{\mathcal{L}}$ 强化主体身份学习，在框外区域保持权重1以维持运动控制精度。消融实验（Table 6）表明，$\lambda_{\mathcal{L}} = 2$ 时各项指标达到最优平衡；过高的 $\lambda_{\mathcal{L}} = 4$ 会损害运动控制精度（mIoU 和 CD 下降）。



## 实验与关键发现

### 实验设置

DreamVideo-2 基于预训练的 ModelScopeT2V（ZeroScope）视频扩散模型构建。训练时冻结原始 3D UNet 参数，仅联合训练新增的掩码参考注意力、时空编码器与 ControlNet，优化器采用 AdamW（学习率 1×10⁻⁴，权重衰减 0），共训练 30k 次迭代，批大小为 144，空间分辨率 448×256，帧数 16。混合掩码权重 λ_M = 0.75，重加权扩散损失权重 λ_L = 2。所有实验在 8 块 NVIDIA A100 GPU 上完成。

评估指标涵盖文本对齐（CLIP-T）、主体保真度（R-CLIP、R-DINO、CLIP-I、DINO-I）、时序一致性（Temporal Consistency）、运动控制精度（mIoU、CD↓）及动态程度（Dynamic Degree）。为确保公平，所有基线方法均采用相同的 ZeroScope 基础模型，仅 VideoBooth 与 MotionCtrl 因架构差异保留其自有训练数据。

### 联合主体与运动控制

Table 2 给出了联合定制任务的定量对比。DreamVideo-2 在运动控制精度上大幅领先：mIoU 达到 0.670，相比 DreamVideo（0.169）提升 0.501，CD 降至 0.048（DreamVideo 为 0.196）。同时，主体保真度指标保持竞争力——R-CLIP 0.751、DINO-I 0.411，均优于所有需测试时微调的基线方法（DreamVideo、MotionBooth）。值得注意的是，简单联合训练会导致运动控制主导、主体身份严重退化（Figure 3 (b)(c)），而 DreamVideo-2 通过混合掩码与重加权损失有效平衡了二者的学习。

Figure 4 的定性结果显示，DreamVideo-2 能够精确控制主体沿指定轨迹运动，而其他方法普遍存在控制冲突，尤其在仅用单张图像训练时，主体外观扭曲或运动轨迹偏离严重。

![[assets/figures/papers/paper_list_l5_https_arxiv_org_abs_2410_13830/figures/006_Figure_4.jpg]]
*Figure 4: Qualitative comparison of joint subject customization and motion control. DreamVideo-2 generates videos with customized subjects and precise motion trajectory control, while other methods suffer from control conflicts, especially when trained on a single image*

### 主体定制

在仅保留主体学习模块、不使用运动编码器和混合掩码的条件下，DreamVideo-2 与 VideoBooth 采用相同数据集训练。Table 3 显示，DreamVideo-2 在 CLIP-T（0.297）、DINO-I（0.472）和 Dynamic Degree（0.952）上均取得最优，其中 Dynamic Degree 相比 VideoBooth（0.780）提升 0.172，表明生成视频的运动动态性显著增强。

![[assets/figures/papers/paper_list_l5_https_arxiv_org_abs_2410_13830/figures/007_Table_3.jpg]]
*Table 3: Quantitative comparison of subject customization*

### 运动控制

仅训练运动编码器以排除主体学习影响时，DreamVideo-2 与 Peekaboo、Direct-a-Video、MotionCtrl 等零样本运动控制方法对比。Table 4 显示，DreamVideo-2 的 mIoU 达到 0.752（MotionCtrl 为 0.497），CD 降至 0.039（MotionCtrl 为 0.070），运动轨迹控制精度显著优于所有基线。

![[assets/figures/papers/paper_list_l5_https_arxiv_org_abs_2410_13830/figures/010_Table_4.jpg]]
*Table 4: Quantitative comparison of motion control*

### 消融实验

Table 5 和 Figure 8 系统验证了各组件的贡献：

![[assets/figures/papers/paper_list_l5_https_arxiv_org_abs_2410_13830/figures/013_Figure_8.jpg]]
*Figure 8: Qualitative ablation studies on each component and blended mask weight*

- **移除掩码机制**：将混合掩码替换为全 1 掩码后，主体保真度指标（R-CLIP、R-DINO、CLIP-I、DINO-I）全面下降，说明掩码机制对增强主体区域表征至关重要。
- **移除运动编码器**：mIoU 和 CD 大幅恶化，运动控制精度几乎丧失，验证了时空编码器与 ControlNet 对轨迹控制的必要性。
- **移除重加权扩散损失**（λ_L = 1）：Table 6 显示，该设置在大多数指标上表现最差，尤其是主体保真度。当 λ_L 增至 1.5 或 2 时，所有指标全面提升；但 λ_L = 4 时运动控制精度开始受损，表明过度放大框内损失会破坏主体学习与运动控制的平衡。

![[assets/figures/papers/paper_list_l5_https_arxiv_org_abs_2410_13830/figures/016_Table_6.jpg]]
*Table 6: Ablation study on reweighted diffusion loss weight*

### 失败模式

Figure 10 展示了 DreamVideo-2 的两类典型失败案例：(a) 受限于基础模型 ModelScopeT2V 的固有能力，难以生成罕见或不自然的动作（如“狗在火星上弹吉他”）；(b) 方法难以解耦相机运动与物体运动控制，可能出现相机移动但主体静止的情况。此外，当前框架仅支持单主体与单条运动轨迹，尚未扩展到多主体场景。

### 补充图表

![[assets/figures/papers/paper_list_l5_https_arxiv_org_abs_2410_13830/figures/004_Table_1.jpg]]
*Table 1: Comparsion of our dataset with related video datasets. Our dataset contains comprehensive annotations, and is larger and more diverse than previous video customization datasets*

![[assets/figures/papers/paper_list_l5_https_arxiv_org_abs_2410_13830/figures/008_Figure_5.jpg]]
*Figure 5: Qualitative comparison of subject customization. DreamVideo-2 generates videos with accurate subject appearance and enhanced motion dynamics, aligning with provided prompts*

![[assets/figures/papers/paper_list_l5_https_arxiv_org_abs_2410_13830/figures/009_Figure_6.jpg]]
*Figure 6: Qualitative comparison of motion control. Our DreamVideo-2 achieves precise motion trajectory control and effectively maintains subjects within the specified bounding boxes*

![[assets/figures/papers/paper_list_l5_https_arxiv_org_abs_2410_13830/figures/014_Figure_7.jpg]]
*Figure 7: Human evaluation on joint subject customization and motion control*

![[assets/figures/papers/paper_list_l5_https_arxiv_org_abs_2410_13830/figures/012_Figure.jpg]]
*Figure: (b) Effects of blended mask weight*



## 定位与知识库关联

### 零样本视频定制的方法坐标

DreamVideo-2 处于**零样本主体驱动视频定制与精准运动控制**的交叉点。与现有工作相比，其核心差异在于无需测试时微调即可同时完成主体外观学习和运动轨迹控制，而此前的方法或需微调，或只能单独处理其中一项任务。

**联合定制基线（需测试时微调）**：
- **DreamVideo** (Wei et al., CVPR 2024)：联合主体与运动定制，但需要对每个测试样本进行微调，无法实现零样本推理。
- **MotionBooth** (Wu et al., arXiv 2024)：同样联合主体与运动定制，需测试时微调并编辑注意力图来控制运动。

**仅主体定制基线（零样本）**：
- **VideoBooth** (Jiang et al., 2024)：零样本主体定制框架，但不具备运动控制能力。

**仅运动控制基线（零样本或需单独训练）**：
- **Peekaboo** (Jain et al., 2024)：零样本运动控制方法，通过边界框注意力操作引导运动。
- **Direct-a-Video** (Yang et al., 2024a)：零样本运动控制方法。
- **MotionCtrl** (Wang et al., 2024f)：需单独训练运动模块，不具备主体定制能力。

DreamVideo-2 的关键突破在于将主体学习与运动控制统一到一个零样本框架中，并通过混合掩码参考注意力和重加权扩散损失解决了联合训练中运动控制主导、主体身份退化的瓶颈问题。

### 关键设计决策与消融证据

DreamVideo-2 引入了四个相互耦合的设计槽位，每个槽位的消融实验均证实了其必要性（Table 5、Table 6）：

1. **掩码参考注意力中的混合掩码机制**：移除掩码机制后，主体保真度指标（R-CLIP、R-DINO、CLIP-I、DINO-I）显著下降。这表明混合掩码 $\hat{\mathbf{M}} = \mathbf{M} + \lambda_{\mathbf{M}}(1 - \mathbf{M})$ 通过为背景区域赋予较低权重，有效增强了主体在指定位置的特征表达，是平衡主体学习与运动控制的核心机制。

2. **掩码引导运动模块（时空编码器 + ControlNet）**：移除运动编码器或 ControlNet 后，mIoU 和 CD 大幅恶化，运动控制精度丧失。这验证了从框掩码序列提取运动信息并通过 ControlNet 注入视频生成过程的必要性。

3. **重加权扩散损失**：当 $\lambda_{\mathcal{L}} = 1$（即无重加权）时，大多数指标表现最差，尤其是主体保真度。将 $\lambda_{\mathcal{L}}$ 提升至 1.5 或 2 能全面提升所有指标，但过高（$\lambda_{\mathcal{L}} = 4$）会损害运动控制精度。这表明适度的框内损失放大是平衡两项任务的关键调节旋钮。

### 适用边界与限制

DreamVideo-2 的适用边界由以下因素界定：

1. **基础模型能力上限**：方法基于 ModelScopeT2V（ZeroScope）视频扩散模型，受限于该模型的固有能力。对于罕见或不自然的动作（如“狗在火星上弹吉他”），生成质量受基础模型制约（Figure 10a）。这意味着方法无法超越底层模型的生成边界。

2. **单主体单轨迹限制**：当前框架仅支持单主体与单条运动轨迹的视频生成，尚未扩展到多主体场景。这是方法架构的显式边界。

3. **相机运动与物体运动耦合**：方法难以解耦相机运动与物体运动控制，可能出现相机移动但主体静止的情况（Figure 10b）。这是因为框掩码序列同时编码了物体的绝对位置变化和相机的相对运动，模型无法区分两者。

4. **数据依赖**：训练依赖于包含边界框标注的视频数据集，虽然作者构建了比此前工作更大、更多样的数据集（Table 1），但数据覆盖范围仍可能限制泛化能力。

### 开放问题与后续方向

从方法的限制和设计出发，以下开放问题值得关注：

1. **多主体多轨迹扩展**：如何将参考注意力机制和掩码引导运动模块扩展到多主体、多运动轨迹的场景？这需要解决多主体特征注入时的相互干扰问题，以及多轨迹掩码的编码与解耦。

2. **相机-物体运动解耦**：能否通过引入额外的运动分解模块（如光流或深度信息）来分离相机运动与物体运动，实现更灵活的视频控制？这是提升运动控制精度的关键方向。

3. **更强基础模型的适配**：将框架迁移到更高分辨率、更长时长、更强生成能力的基础模型（如 Sora 类架构）上，能否突破当前对罕见动作的生成限制？

4. **推理效率优化**：虽然方法是零样本的，但训练阶段仍需联合优化多个模块。能否通过预训练策略或模块解耦进一步降低训练成本？

5. **评估体系的完善**：当前评估依赖 CLIP-T、DINO-I、mIoU、CD 等指标和人类评估，但缺乏对运动自然度、物理合理性等维度的系统度量。建立更全面的视频定制评估基准仍是开放问题。



## 原文 PDF

![[paperPDFs/arxiv_2024/DreamVideo_2_Zero_Shot_Subject_Driven_Video_Customization_with_Precise_Motion_Control.pdf]]
