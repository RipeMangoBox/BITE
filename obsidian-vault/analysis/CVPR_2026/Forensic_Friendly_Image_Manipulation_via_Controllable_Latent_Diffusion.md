---
title: Forensic-Friendly Image Manipulation via Controllable Latent Diffusion
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/Forensic_Friendly_Image_Manipulation_via_Controllable_Latent_Diffusion.pdf
project_link: null
code_link: "https://github.com/chloeadrian12/FFIM"
aliases:
- FFFIM
- FFIMCLD
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/generative_models_diffusion
- topic/generative_models_diffusion/diffusion_image_video
core_operator: 去噪过程中采样的随机噪声。通过正交投影提取噪声与图像特征正交的分量，并结合取证代理模型的对抗梯度优化，可控制编辑与未编辑区域在取证空间中的特征差异。
primary_logic: 在图像生成阶段，利用正交投影迫使噪声与当前特征正交，并以累积缓冲区保留历史正交分量，然后在取证空间中评估区域相似度；若相似度过高，则引入预训练取证模型的梯度信号进行对抗噪声调整，再重新投影以保证条件兼容性。这样在满足用户编辑需求的同时，为第三方取证提供内生的、可检测的区域差异线索。
claims:
- FFIM在四个数据集上最高提升像素级定位F1达6.6%、图像级检测AUC达27.3%。
- 正交投影（ℓ₂）对比基线提升13.0% F1和16.0% Rec，且不引入视觉伪影。
- 结合显式取证引导（TruFor）后，F1进一步提升至整体+13.0%。
- 用户主观满意度评分FFIM为4.15分，与标准扩散模型（4.17）和其他基线（4.10–4.21）无显著差异。
---

# Forensic-Friendly Image Manipulation via Controllable Latent Diffusion

> [!tip] 核心洞察
> 在图像生成阶段，利用正交投影迫使噪声与当前特征正交，并以累积缓冲区保留历史正交分量，然后在取证空间中评估区域相似度；若相似度过高，则引入预训练取证模型的梯度信号进行对抗噪声调整，再重新投影以保证条件兼容性。这样在满足用户编辑需求的同时，为第三方取证提供内生的、可检测的区域差异线索。

| 字段 | 内容 |
|------|------|
| 中文题名 | 通过可控潜在扩散实现取证友好图像编辑 |
| 英文题名 | Forensic-Friendly Image Manipulation via Controllable Latent Diffusion |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://openaccess.thecvf.com/content/CVPR2026/html/Chen_Forensic-Friendly_Image_Manipulation_via_Controllable_Latent_Diffusion_CVPR_2026_paper.html) · [Code](https://github.com/chloeadrian12/FFIM) |
| Topic | #topic/vision_multimodal_applications #topic/generative_models_diffusion #topic/generative_models_diffusion/diffusion_image_video |
| Method | FFIM (Forensic-Friendly Image Manipulation) |
| Dataset | MaBrush, InCOCO, Combined AniCOCO |

> [!tip] 效果简介
> - MaBrush 上，F1 0.420 vs 0.354 (+0.066 (6.6%))。
> - InCOCO 上，F1 0.672 vs 0.542 (+0.130 (13.0%))。
> - Combined AniCOCO (image-level) 上，AUC — vs — (+27.3%)。

## 概述

### 问题背景

扩散模型驱动的图像编辑服务日益普及，但标准潜在扩散模型（LDM）生成的编辑结果在取证空间中缺乏内生可区分特征，使得第三方被动取证难以有效检测和定位编辑区域。现有主动防御方案（如数字水印）依赖服务器提供私有溯源信息，不适用于无共识方的取证分析场景。

### 核心洞察

**FFIM**（Forensic-Friendly Image Manipulation）提出了一种内生取证友好的图像编辑范式：在图像生成阶段，通过控制去噪过程中采样的随机噪声，使编辑区域与未编辑区域在取证空间中产生可检测的特征差异。具体而言，该方法利用正交投影提取噪声中与当前图像特征正交的分量，并结合预训练取证代理模型的对抗梯度优化，在满足用户编辑需求的同时，为第三方取证提供内生的区域差异线索。

### 方法定位

FFIM 是一个即插即用的可控去噪框架，包含三个核心阶段：

- **可控投影（Phase I）**：将每步采样的噪声投影到与当前潜特征及历史正交噪声缓冲区均正交的子空间，保留正交分量以构建编辑区域的内生取证信号。
- **隐式检测（Phase II）**：通过空间转移函数将生成特征映射到取证空间，利用多尺度软掩膜量化编辑与未编辑区域的相似度，预验证取证可区分性。
- **显式引导（Phase III）**：当隐式检测的相似度超过阈值时，引入预训练取证模型的对抗损失对噪声进行梯度优化，随后重新投影以保证条件兼容性，最大化取证特征差异。

该方法不依赖服务器提供私有水印或溯源信息，仅利用内生信号即可被第三方取证检测，具有更广泛的适用性。

### 主要结果

在四个数据集上的实验表明，FFIM 在像素级定位和图像级检测任务上均显著优于标准扩散模型基线：

- **像素级定位**：在 MaBrush 数据集上 F1 最高提升 **6.6%**（0.354 → 0.420，SAFIRE 检测器），在 InCOCO 数据集上 F1 提升 **13.0%**（0.542 → 0.672，TruFor 检测器）。
- **图像级检测**：在 Combined AniCOCO 数据集上 AUC 提升 **27.3%**（DRCT 检测器）。
- **用户体验保持**：用户主观满意度评分 FFIM 为 4.15 分，与标准扩散模型（4.17）及其他基线（4.10–4.21）无显著差异；客观质量指标（熵、噪声、对比度）与标准 LDM 结果差异微小，不损害视觉质量。

### 局限与展望

FFIM 的性能上限受所选预训练取证代理模型的泛化能力限制，相似度阈值和优化步长等超参数需手工调节，且尚未验证在 SD3、FLUX 等直接预测式扩散模型上的适用性。如何将该噪声调整策略扩展到更广泛的生成范式，以及设计自适应的参数选择机制，是未来值得探索的方向。

## 背景与动机

### 问题背景：图像编辑的取证困境

随着潜在扩散模型（Latent Diffusion Models, LDMs）的快速发展，服务端图像编辑能力已大幅提升——用户只需提供图像和掩膜提示，即可获得语义连贯、视觉逼真的编辑结果。然而，这种便利性也带来了严峻的取证挑战：**标准扩散模型生成的编辑图像在取证空间中缺乏内生可区分特征**，使得第三方被动取证工具难以有效检测和定位编辑区域。

当前应对这一问题的主流方案可分为两类。一类是**主动防御**，即在生成过程中嵌入水印或溯源信息，但这要求服务端与取证方之间存在共识协议，且依赖私有方案，无法适用于无共识方的第三方取证分析场景。另一类是**后处理式取证增强**，如 **ReLoc**（Zhuang et al., IEEE TIFS 2023），在编辑完成后对图像进行额外处理以提升可检测性，但这类方法往往在取证性能与图像质量之间存在权衡。

### 核心瓶颈：内生可区分特征的缺失

问题的本质在于：标准扩散模型的去噪过程并未考虑取证需求。在推理阶段，模型从随机噪声出发逐步去噪生成编辑内容，该过程完全以视觉质量和用户需求为优化目标。这导致编辑区域与未编辑区域在取证模型的特征空间中高度相似，第三方取证工具难以捕捉到可靠的篡改痕迹。

从形式化角度看，给定用户提供的掩膜 $\mathbf{M}$ 和提示 $\mathbf{P}$，标准 LDM 生成编辑图像 $\hat{\mathbf{I}}_{\mathrm{ST}}$ 的过程满足视觉质量约束，但无法保证以下取证友好定位约束：

$$\mathrm{Loc}(\hat{\mathbf{M}}_{\mathrm{FF}}, \mathbf{M}) > \mathrm{Loc}(\hat{\mathbf{M}}_{\mathrm{ST}}, \mathbf{M})$$

其中 $\mathrm{Loc}$ 表示定位指标，$\hat{\mathbf{M}}$ 为取证模型的预测掩膜。换言之，**需要一种在生成阶段即内嵌取证可区分性的机制**，而非依赖事后补救。

### 本文动机：内生取证友好的生成范式

针对上述缺口，本文提出 **FFIM（Forensic-Friendly Image Manipulation）**，一种无需服务端与取证方共识即可支持第三方取证的内生式编辑方案。其核心动机在于：

1. **消除对私有水印的依赖**：FFIM 仅利用内生信号即可为第三方取证提供可检测的区域差异线索，适用于更广泛的开放场景。
2. **在生成阶段嵌入取证友好性**：通过控制去噪过程中的噪声采样与优化，使编辑区域在取证空间中与未编辑区域形成内生可区分特征。
3. **兼顾用户需求与取证性能**：在提升取证检测能力的同时，确保编辑结果在主观满意度和客观质量指标上与标准扩散模型无显著差异。

如图 Figure 1 所示，采用 FFIM 的服务端可在满足用户编辑需求的同时，使第三方取证工具无需任何先验信息即可有效定位篡改区域。这一范式转变将取证责任从“事后检测”前移至“生成阶段设计”，为图像编辑的可信生态提供了新思路。

## 核心创新

FFIM 的核心创新在于**将取证可区分性内生地嵌入扩散模型的去噪过程**，使生成的编辑图像自带可被第三方取证检测的区域差异线索，而无需服务器提供任何先验信息（如水印或溯源元数据）。这与现有后处理式取证增强方法（如 **ReLoc**，Zhuang et al., IEEE TIFS 2023）有本质区别：后者在图像生成完成后才施加取证优化，而 FFIM 在生成阶段即通过控制去噪路径来塑造取证特征。

### 关键控制维度：噪声采样与优化的三重机制

标准潜在扩散模型（**DDPM**，Ho et al., NeurIPS 2020）在推理阶段直接采样高斯噪声 $\epsilon_t$ 进行去噪，编辑区域与非编辑区域在取证空间中缺乏内生差异。FFIM 在三个关键环节改变了这一范式：

**1. 可控投影（Controllable Projection）—— 噪声采样的正交化**

FFIM 不再直接使用采样的高斯噪声，而是通过正交投影提取噪声中与当前潜特征 $\mathbf{z}_t$ 及历史正交噪声缓冲区 $\mathcal{B}_t$ 均正交的分量 $\epsilon_t^\perp$。其核心操作如下：

$$\epsilon_t^\perp = \epsilon_t - \mathrm{Proj}_{\mathbf{z}_t \oplus \mathrm{Span}(\mathcal{B}_t)}(\epsilon_t)$$

投影算子的展开形式为：

$$\operatorname{Proj}_{\mathbf{z}_t \oplus \operatorname{Span}(\mathcal{B}_t)}(\boldsymbol{\epsilon}_t) = \frac{\boldsymbol{\epsilon}_t \cdot \mathbf{z}_t}{\mathbf{z}_t \cdot \mathbf{z}_t}\mathbf{z}_t + \sum_{\boldsymbol{\epsilon}_v^\perp \in \mathcal{B}_t} \frac{\boldsymbol{\epsilon}_t \cdot \boldsymbol{\epsilon}_v^\perp}{\boldsymbol{\epsilon}_v^\perp \cdot \boldsymbol{\epsilon}_v^\perp}\boldsymbol{\epsilon}_v^\perp$$

这一设计的因果逻辑是：噪声张量中与当前特征 $\mathbf{z}_t$ 平行的分量倾向于在编辑区域与非编辑区域之间产生相似的特征表达，而去除这些分量后，剩余的正交分量 $\epsilon_t^\perp$ 更可能引入区域间差异。累积缓冲区 $\mathcal{B}_t$ 则确保跨步一致性，防止后续去噪步骤重新引入已被排除的特征方向。

消融实验证实了这一机制的有效性：$\ell_2$ 正交投影（变体 #8）相较于基线 DDPM 提升 **+13.0% F1** 和 **+16.0% Rec**，且不引入视觉伪影（Table 3）。值得注意的是，$\ell_\infty$ 投影（变体 #6）虽能获得更高的 F1 提升（+33.0%），但会产生不可用的噪声图像（Figure 5），这揭示了取证优化与视觉质量之间的根本性张力。

**2. 隐式检测（Implicit Detection）—— 取证可区分性的预验证**

仅靠正交投影无法保证编辑区域与未编辑区域在取证空间中具有足够的可区分性。FFIM 引入了一个轻量级的预验证机制：通过空间转移函数 $\mathcal{T}$ 将中间生成特征映射到取证相关空间，然后计算软掩膜下的区域相似度。

空间转移函数定义为：

$$\mathcal{T}(\hat{\mathbf{z}}_t) = \mathcal{F}(\mathcal{D}(\hat{\mathbf{z}}_t))$$

其中 $\mathcal{D}$ 为解码器，$\mathcal{F}$ 为预训练取证模型的特征提取部分。相似度计算为：

$$s = \mathcal{S}\left(\mathbf{M} \odot \mathcal{T}(\hat{\mathbf{z}}_t), (1 - \mathbf{M}) \odot \mathcal{T}(\hat{\mathbf{z}}_t)\right)$$

为减少硬边界引入的伪影，FFIM 使用多尺度高斯模糊生成软权重掩膜：

$$\tilde{\mathbf{M}} = \frac{1}{K} \sum_{k=1}^{K} \mathcal{G}_k(\mathbf{M})$$

若相似度 $s \leq \tau$，表明编辑区域与未编辑区域在取证空间中已有足够差异，可直接通过；否则触发显式引导。这一机制的核心价值在于**以极低的计算代价避免不必要的对抗优化**，仅在正交投影不足以产生取证可区分性时才介入。

**3. 显式引导（Explicit Guidance）—— 对抗梯度驱动的噪声优化**

当隐式检测判定相似度过高时，FFIM 引入预训练取证模型（如 TruFor）的梯度信号进行对抗噪声调整。优化目标是最小化编辑区域与未编辑区域在取证空间中的相似度：

$$\mathcal{L}_{\mathrm{adv}} = \mathcal{S}\left(\tilde{\mathbf{M}} \odot \mathcal{T}(\hat{\mathbf{z}}_t), (1 - \tilde{\mathbf{M}}) \odot \mathcal{T}(\hat{\mathbf{z}}_t)\right)$$

对 $\epsilon_t^\perp$ 执行梯度下降后，FFIM 将优化后的噪声重新投影到正交子空间，以保证条件兼容性不被破坏。这一“优化-再投影”的闭环设计是 FFIM 区别于简单对抗攻击的关键：它确保噪声调整始终在满足用户编辑需求的正交子空间内进行，而非无约束地最大化取证损失。

消融实验（Table 4）表明，使用 TruFor 作为显式引导模型（#5）相较于无引导方案在 F1 上进一步提升至总计 **+13.0%**，验证了对抗梯度信号对取证可区分性的增益效果。

### 创新本质：从后处理到内生嵌入的范式转换

上述三个 changed slots 共同构成了 FFIM 的创新本质：**将取证优化从图像生成的后处理阶段前移到去噪过程的噪声采样与优化阶段**。这一范式转换带来了两个关键优势：

1. **无共识方取证**：FFIM 不依赖服务器提供水印或溯源信息，生成的编辑图像自带内生取证线索，任何持有预训练取证模型的第三方均可检测和定位编辑区域。

2. **需求满足约束下的优化**：FFIM 在优化取证可区分性的同时，通过正交投影保证噪声调整不偏离用户编辑需求。用户主观满意度评分（FFIM 4.15 vs. 基线 DDPM 4.17，5-point Likert 量表）和客观质量指标（熵、噪声、对比度，Table 2）均无显著差异，验证了方法在取证友好性与用户体验之间的有效平衡。

## 整体框架

FFIM 的整体设计围绕一个核心矛盾展开：标准潜在扩散模型（LDM）生成的编辑图像，其编辑区域与未编辑区域在取证空间中缺乏内生可区分特征，导致第三方被动取证难以检测和定位篡改。FFIM 在不依赖服务器提供私有水印或溯源信息的前提下，通过干预去噪过程中的噪声采样与优化，使生成图像自带取证友好的区域差异线索。

### 三阶段流水线

FFIM 的推理流水线由三个核心阶段串联构成（Figure 2），嵌入在预训练掩膜‑提示条件 LDM 的标准去噪循环中：

![[assets/figures/papers/paper_list_l2490_https_openaccess_thecvf_com_content_CVPR2026_html_Chen_Forensic_Friendly/figures/002_Figure_2.jpg]]
*Figure 2: The proposed FFIM consists of three core phases: I) Controllable Projection, II) Implicit Detection, and III) Explicit Guidance*

1. **可控投影（Phase I: Controllable Projection）**  
   在每一步去噪时，对采样噪声执行正交投影，提取与当前潜特征 $\mathbf{z}_t$ 及历史正交噪声缓冲区 $\mathcal{B}_t$ 均正交的分量 $\boldsymbol{\epsilon}_t^\perp$。这一操作的目的在于：将噪声中与已生成内容高度相关的成分剥离，保留能驱动编辑区域与未编辑区域在特征空间中产生差异的“独立分量”。累积缓冲区 $\mathcal{B}_t$ 的引入保证了跨步一致性，避免不同时间步的正交噪声互相干扰。

2. **隐式检测（Phase II: Implicit Detection）**  
   将 Phase I 得到的正交噪声融合后，通过空间转移函数 $\mathcal{T}(\hat{\mathbf{z}}_t) = \mathcal{F}(\mathcal{D}(\hat{\mathbf{z}}_t))$ 将当前生成特征映射到取证相关空间（$\mathcal{F}$ 为预训练取证模型的特征提取器，$\mathcal{D}$ 为 LDM 解码器）。随后利用多尺度高斯模糊生成的软权重掩膜 $\tilde{\mathbf{M}}$，计算编辑与未编辑区域在取证空间中的相似度 $s$。若 $s \leq \tau$（相似度足够低，意味着取证可区分性已达标），则跳过 Phase III，直接进入下一步去噪。

3. **显式引导（Phase III: Explicit Guidance）**  
   当隐式检测判定相似度过高（$s > \tau$）时，引入预训练取证代理模型的梯度信号，以对抗损失 $\mathcal{L}_{\mathrm{adv}}$ 对正交噪声 $\boldsymbol{\epsilon}_t^\perp$ 进行梯度下降优化，最小化编辑与未编辑区域在取证空间中的相似度。优化后的噪声需重新投影，以保证与当前特征及缓冲区的正交性约束不被破坏，从而在条件兼容性与取证可区分性之间取得平衡。

### 输入输出流

- **输入**：用户提供的原始图像、编辑掩膜 $\mathbf{M}$ 及文本提示 $\mathbf{P}$。
- **处理**：预训练 LDM 编码器将图像映射为潜变量 $\mathbf{z}_0$，并按标准前向扩散过程加噪至 $\mathbf{z}_T$。在逆向去噪的每一步中，FFIM 三阶段模块依次介入噪声的采样、验证与优化。
- **输出**：最终解码生成的编辑图像 $\hat{\mathbf{I}}_{\mathrm{FF}}$，该图像在满足用户编辑需求的同时，其编辑区域与未编辑区域在取证空间中呈现出内生可区分的特征差异，可供任意第三方取证模型进行检测与定位，无需服务器额外提供先验信息。

### 与标准 LDM 的关系

FFIM 并非重新训练扩散模型，而是作为即插即用的推理阶段介入策略。其基础去噪骨干（Base LDM Denoising）保持冻结，仅修改每步去噪中噪声的采样与调整方式。这一设计使得 FFIM 可以兼容现有的掩膜‑提示条件 LDM 架构，同时保持生成图像在熵、噪声、对比度等客观质量指标上与标准 LDM 结果的差异微小（Table 2），不损害用户体验。

### 补充图表

![[assets/figures/papers/paper_list_l2490_https_openaccess_thecvf_com_content_CVPR2026_html_Chen_Forensic_Friendly/figures/001_Figure_1.jpg]]
*Figure 1: Adopting the proposed FFIM, the server can generate results that satisfy user requirements while facilitating forgery localization by third-party forensics without consensus*

## 核心模块与公式推导

### 问题形式化：取证友好的约束条件

FFIM 的设计目标是在满足用户编辑需求的前提下，使生成的编辑图像内生地具备取证可区分性。这一目标通过两个约束条件形式化定义。

**图像质量约束**要求 FFIM 编辑结果与标准 LDM 编辑结果之间的客观质量评分差异必须小于阈值 $\lambda_{\mathrm{IQA}}$：

$$
\vert \mathrm{IQA}(\hat{\mathbf{I}}_{\mathrm{FF}}) - \mathrm{IQA}(\hat{\mathbf{I}}_{\mathrm{ST}}) \vert < \lambda_{\mathrm{IQA}}
$$

**取证定位约束**要求 FFIM 的预测掩膜 $\hat{\mathbf{M}}_{\mathrm{FF}}$ 与真实掩膜 $\mathbf{M}$ 的定位指标必须优于标准 LDM：

$$
\mathrm{Loc}(\hat{\mathbf{M}}_{\mathrm{FF}}, \mathbf{M}) > \mathrm{Loc}(\hat{\mathbf{M}}_{\mathrm{ST}}, \mathbf{M})
$$

这两个约束构成了 FFIM 三阶段设计的优化目标：在满足质量约束的前提下，最大化取证定位性能。

---

### 基础 LDM 去噪模块

FFIM 建立在预训练的掩膜-提示条件潜在扩散模型之上。该模型的训练目标为：

$$
\mathcal{L} = \mathbb{E}_{\mathcal{E}(\mathbf{I}), \mathbf{M}, \mathbf{P}, \epsilon \sim \mathcal{N}(0,1), t} \left[ \| \epsilon - \epsilon_{\theta} \left( \mathbf{z}_t, t, \kappa_{\theta}(\mathbf{M}, \mathbf{P}) \right) \|_2^2 \right]
$$

其中 $\mathcal{E}$ 为图像编码器，$\mathbf{M}$ 为用户提供的编辑掩膜，$\mathbf{P}$ 为文本提示，$\kappa_{\theta}$ 为条件编码器。在推理阶段，去噪潜变量通过以下公式从含噪隐变量恢复：

$$
\hat{\mathbf{z}} = \frac{1}{\sqrt{\bar{\alpha}_t}} \cdot (\mathbf{z}_t - \sqrt{1 - \bar{\alpha}_t} \cdot \boldsymbol{\epsilon}_t)
$$

FFIM 的核心创新在于对每步采样的噪声 $\boldsymbol{\epsilon}_t$ 进行调控，而非修改基础去噪架构本身。

---

### Phase I：可控投影 (Controllable Projection)

**设计动机**：标准扩散模型采样的高斯噪声与当前图像特征在生成空间中高度纠缠，导致编辑区域与未编辑区域缺乏内生可区分特征。Phase I 通过正交投影将噪声分解，保留与当前特征正交的分量，从而在生成空间中主动引入区域差异。

**单步正交投影**：首先将采样噪声 $\boldsymbol{\epsilon}_t$ 投影到当前潜特征 $\mathbf{z}_t$ 的正交补上：

$$
\boldsymbol{\epsilon}_t^{\perp} = \boldsymbol{\epsilon}_t - \mathrm{Proj}_{\mathbf{z}_t}(\boldsymbol{\epsilon}_t)
$$

其中投影算子定义为标量投影：

$$
\operatorname{Proj}_{\mathbf{z}_t}(\boldsymbol{\epsilon}_t) = \frac{\boldsymbol{\epsilon}_t \cdot \mathbf{z}_t}{\mathbf{z}_t \cdot \mathbf{z}_t} \mathbf{z}_t
$$

**累积正交投影**：单步投影仅考虑当前特征，忽略了去噪过程中历史噪声分量的影响。FFIM 引入累积正交缓冲区 $\mathcal{B}_t$，将噪声投影到 $\mathbf{z}_t$ 和历史正交噪声分量 $\mathcal{B}_t$ 共同张成的子空间的正交补上：

$$
\boldsymbol{\epsilon}_t^{\perp} = \boldsymbol{\epsilon}_t - \mathrm{Proj}_{\mathbf{z}_t \oplus \mathrm{Span}(\mathcal{B}_t)}(\boldsymbol{\epsilon}_t)
$$

展开的多向量投影算子为：

$$
\operatorname{Proj}_{\mathbf{z}_t \oplus \operatorname{Span}(\mathcal{B}_t)}(\boldsymbol{\epsilon}_t) = \frac{\boldsymbol{\epsilon}_t \cdot \mathbf{z}_t}{\mathbf{z}_t \cdot \mathbf{z}_t} \mathbf{z}_t + \sum_{\boldsymbol{\epsilon}_v^{\perp} \in \mathcal{B}_t} \frac{\boldsymbol{\epsilon}_t \cdot \boldsymbol{\epsilon}_v^{\perp}}{\boldsymbol{\epsilon}_v^{\perp} \cdot \boldsymbol{\epsilon}_v^{\perp}} \boldsymbol{\epsilon}_v^{\perp}
$$

该公式的第一项对应 $\mathbf{z}_t$ 方向的投影分量，第二项对缓冲区中每个历史正交噪声分量 $\boldsymbol{\epsilon}_v^{\perp}$ 逐一计算投影贡献。每次投影后，当前的 $\boldsymbol{\epsilon}_t^{\perp}$ 被追加到缓冲区 $\mathcal{B}_t$ 中，以保持跨步的正交一致性。

**核心机制**：正交投影本质上将噪声分解为“与当前特征共线”和“与当前特征正交”两个分量。保留正交分量意味着编辑区域的生成信号在特征空间中与未编辑区域保持最大差异方向，从而为后续取证检测提供内生线索。

---

### Phase II：隐式检测 (Implicit Detection)

**设计动机**：Phase I 的正交投影在生成空间中引入差异，但无法保证该差异在取证空间（即取证模型所感知的特征空间）中同样显著。Phase II 通过将生成特征映射到取证空间并计算区域相似度，预验证当前噪声配置的取证可区分性。

**空间转移函数**：将中间生成特征 $\hat{\mathbf{z}}_t$ 通过解码器 $\mathcal{D}$ 和预训练取证模型 $\mathcal{F}$ 映射到取证相关空间 $\mathcal{V}$：

$$
\mathcal{T}(\hat{\mathbf{z}}_t) = \mathcal{F}(\mathcal{D}(\hat{\mathbf{z}}_t))
$$

**软权重掩膜**：为避免硬边界掩膜在取证空间中引入伪影，FFIM 使用多尺度高斯模糊生成平滑掩膜：

$$
\tilde{\mathbf{M}} = \frac{1}{K} \sum_{k=1}^{K} \mathcal{G}_k(\mathbf{M})
$$

其中 $\mathcal{G}_k$ 为第 $k$ 个尺度的高斯核。

**相似度验证**：在取证空间中，使用软掩膜分别提取编辑区域和非编辑区域的特征，计算两者之间的相似度 $s$：

$$
s = \mathcal{S} \left( \tilde{\mathbf{M}} \odot \mathcal{T}(\hat{\mathbf{z}}_t), (1 - \tilde{\mathbf{M}}) \odot \mathcal{T}(\hat{\mathbf{z}}_t) \right)
$$

若 $s \leq \tau$（$\tau$ 为预设阈值），表明当前噪声配置已能在取证空间中产生足够的区域差异，直接通过验证；若 $s > \tau$，则触发 Phase III 的显式引导。

---

### Phase III：显式引导 (Explicit Guidance)

**设计动机**：当隐式检测判定相似度过高时，说明正交投影不足以在取证空间中产生可区分的特征差异。Phase III 引入预训练取证模型的梯度信号，对噪声进行对抗优化，主动最小化编辑区域与未编辑区域在取证空间中的相似度。

**对抗损失**：直接复用 Phase II 中的相似度度量作为对抗损失函数：

$$
\mathcal{L}_{\mathrm{adv}} = \mathcal{S} \left( \tilde{\mathbf{M}} \odot \mathcal{T}(\hat{\mathbf{z}}_t), (1 - \tilde{\mathbf{M}}) \odot \mathcal{T}(\hat{\mathbf{z}}_t) \right)
$$

**噪声优化与重投影**：对 $\boldsymbol{\epsilon}_t^{\perp}$ 执行梯度下降以最小化 $\mathcal{L}_{\mathrm{adv}}$，随后将优化后的噪声重新投影回正交子空间，确保条件兼容性不被破坏。这一“优化-重投影”循环在生成空间中引入取证引导的扰动，同时保持与 Phase I 正交约束的一致性。

**关键设计选择**：显式引导所使用的取证代理模型 $\mathcal{F}$ 与 Phase II 中的模型可以相同或不同。消融实验表明，使用 **TruFor** 作为显式引导模型在 F1 指标上优于未引导方案及其他代理模型（Table 4, variant #5），验证了选择合适的取证代理对引导效果至关重要。

---

### 三阶段协同机制

三个阶段的协同逻辑可概括为：

1. **Phase I** 在生成空间中通过正交投影主动制造编辑区域与未编辑区域的特征差异方向；
2. **Phase II** 将差异映射到取证空间进行预验证，以低计算成本筛选出已具备取证可区分性的配置；
3. **Phase III** 对不满足要求的配置引入取证梯度信号进行对抗优化，再通过重投影保证生成质量。

这一设计使 FFIM 在不依赖外部水印或私有溯源信息的前提下，仅通过调控去噪过程中的噪声采样，即可为第三方取证提供内生的、可检测的区域差异线索。

## 实验与分析

### 实验设置与评估协议

FFIM 在掩膜‑提示条件潜在扩散模型（LDM）的去噪过程中对噪声进行内生调控，因此实验围绕两个核心维度展开：（1）第三方取证模型对编辑图像的检测与定位能力（取证友好性）；（2）编辑图像本身的主观视觉质量与客观保真度（用户需求满足程度）。

**数据集与编辑任务。** 实验采用四个公开数据集：**MaBrush**（基于 MSRA10K 的绘画式编辑）、**InCOCO** 与 **AniCOCO**（基于 COCO 的物体插入与动漫风格编辑），以及 **Combined AniCOCO**（图像级检测专用）。所有编辑任务均以用户提供的掩膜与文本提示为条件，由服务器端统一生成编辑结果。

**取证模型选择。** 为模拟无共识第三方取证场景，像素级定位评估采用五种代表性被动取证模型：**SAFIRE**（Guillaro et al., ECCV 2022）、**TruFor**（Guillaro et al., CVPR 2023）、**PSCC‑Net**（Liu et al., TIFS 2022）、**MVSS‑Net**（Dong et al., TIFS 2022）和 **CAT‑Net v2**（Kwon et al., IJCV 2024）。图像级检测评估使用 **CNND**、**UFDA** 和 **DRCT** 三种检测器。

**评估指标。** 像素级定位使用 **F1**、**IoU** 和 **Rec**（召回率）三个指标，其中 Rec 定义为预测掩膜与用户掩膜的交集比上用户掩膜面积：$\operatorname{Rec}(\hat{\mathbf{M}}_{\mathrm{FF}}, \mathbf{M}) = \frac{|\hat{\mathbf{M}}_{\mathrm{FF}} \cap \mathbf{M}|}{|\mathbf{M}|}$。图像级检测使用 ROC 曲线下面积（**AUC**）。视觉质量评估采用熵、噪声标准差、对比度等客观指标，并辅以用户主观 Likert 评分。

**基线方法。** 主要对比对象为 **DDPM**（Ho et al., NeurIPS 2020）标准 LDM 基线，以及后处理式取证增强方法 **ReLoc**（Zhuang et al., IEEE TIFS 2023）。消融实验进一步引入了 DDIM 等变体。

---

### 像素级定位：主实验结果

Table 1 汇总了 FFIM 与基线方法在四个数据集上经五种取证模型评估的像素级定位性能。核心发现如下：

![[assets/figures/papers/paper_list_l2490_https_openaccess_thecvf_com_content_CVPR2026_html_Chen_Forensic_Friendly/figures/004_Table_1.jpg]]
*Table 1: Quantitative comparisons in pixel-level localization of Evaluation I by using F1, IoU and Rec metrics. Red↑ and blue↓ denote performance improvement and degradation, respectively*

**FFIM 在所有取证模型上一致提升定位性能。** 以 TruFor 为取证模型的 InCOCO 基准上，FFIM 的 F1 达到 **0.672**，较标准 DDPM 基线（0.542）提升 **+13.0%**；AniCOCO 上 F1 达到 **0.700**，同样显著优于基线。即使对于性能较弱的取证模型（如 SAFIRE），FFIM 在 MaBrush 基准上仍将 F1 从 0.354 提升至 **0.420**（**+6.6%**）。这表明 FFIM 引入的内生取证线索具有跨取证模型的泛化性，不依赖于特定取证算法的设计偏好。

**FFIM 优于后处理式基线 ReLoc。** ReLoc 通过在生成后添加扰动来增强取证可区分性，但其性能增益在多数场景下不及 FFIM，且可能引入可见伪影。FFIM 的优势在于将取证优化嵌入生成过程本身，使编辑与未编辑区域在取证空间中形成内生差异，而非依赖事后叠加信号。

**IoU 与 Rec 指标协同改善。** 在 TruFor + InCOCO 组合下，FFIM 的 IoU 和 Rec 均显著高于基线，说明不仅定位精度提升，漏检率也大幅降低。Rec 的提升尤为关键——它直接反映了取证模型能否完整覆盖编辑区域，这对实际取证场景中的证据完整性至关重要。

---

### 图像级检测：ROC 分析

Figure 4 展示了 Combined AniCOCO 数据集上三种图像级检测器的 ROC 曲线。FFIM 编辑图像在 **CNND**、**UFDA** 和 **DRCT** 检测器上的 AUC 分别提升 **+14.8%**、**+13.5%** 和 **+27.3%**。其中 DRCT 检测器的增益最为显著（+27.3%），说明 FFIM 生成的取证线索对不同架构的检测器均有正向迁移能力。

![[assets/figures/papers/paper_list_l2490_https_openaccess_thecvf_com_content_CVPR2026_html_Chen_Forensic_Friendly/figures/006_Figure_4.jpg]]
*Figure 4: ROC curves in image-level detection of Evaluation I*

图像级检测评估的是“该图像是否经过编辑”的二分类能力，而非精确定位。FFIM 在此任务上的大幅提升表明，其引入的内生信号不仅增强了区域可区分性，还使整张图像在取证空间中与原始自然图像的分布产生了可检测的偏移——这正是第三方取证所需的关键特性。

---

### 视觉质量与用户满意度：公平性验证

取证友好性的提升不能以牺牲视觉质量为代价。Table 2 的客观质量评估显示，FFIM 编辑图像的熵（7.1375）、噪声标准差（99.4820）和对比度（62.9836）与标准 LDM 基线（7.3172、113.3282、58.3164）差异微小，满足需求约束 $|\mathrm{IQA}(\hat{\mathbf{I}}_{\mathrm{FF}}) - \mathrm{IQA}(\hat{\mathbf{I}}_{\mathrm{ST}})| < \lambda_{\mathrm{IQA}}$。

![[assets/figures/papers/paper_list_l2490_https_openaccess_thecvf_com_content_CVPR2026_html_Chen_Forensic_Friendly/figures/005_Table_2.jpg]]
*Table 2: Image quality assessment of Evaluation II*

用户主观研究进一步验证了这一结论：FFIM 的平均满意度评分为 **4.15**（5-point Likert），与标准 DDPM（4.17）、ReLoc（4.10）和其他主流多模态编辑方式（4.21）无显著差异。这说明 FFIM 在增强取证能力的同时，未引入可感知的视觉退化，真正实现了“用户无感、取证有效”的设计目标。

---

### 消融实验：噪声投影策略

Table 3 系统消融了去噪算法与投影范数约束对性能的影响。核心结论：

![[assets/figures/papers/paper_list_l2490_https_openaccess_thecvf_com_content_CVPR2026_html_Chen_Forensic_Friendly/figures/007_Table_3.jpg]]
*Table 3: Impact of different denoising and projection algorithms. Red↑ indicates improvement over the corresponding baseline denoising, and #8 represents the final variant selected in this work*

**ℓ₂ 正交投影是最优实用选择。** 变体 #8（DDPM + ℓ₂ 投影）在 InCOCO + TruFor 基准上较基线 #1 提升 **+13.0% F1** 和 **+16.0% Rec**，且生成图像无视觉伪影。ℓ₂ 投影在控制噪声方向的同时保持了生成稳定性，是 FFIM 最终采用的方案。

**ℓ∞ 投影虽提升更大但不可用。** 变体 #6（DDPM + ℓ∞ 投影）实现了 **+33.0% F1** 的惊人增益，但生成的图像呈现噪声状乱码（noisy gibberish），完全无法满足用户需求。这一极端结果表明，过强的正交约束会破坏条件生成的一致性，需要在取证优化与视觉质量之间寻找平衡点。Figure 5 提供了不同范数约束下的定性对比，直观展示了 ℓ∞ 投影导致的严重失真。

**方法可泛化至 DDIM。** 变体 #12（DDIM + ℓ₂ 投影）较 DDIM 基线 #11 提升 **+18.4% F1**，证明 FFIM 的正交投影策略不依赖于特定去噪算法，可迁移至其他噪声预测范式。

---

### 消融实验：显式引导模型选择

Table 4 消融了 Phase III 中不同取证代理模型作为显式引导源的效果。使用 **TruFor** 作为引导模型（变体 #5）在 F1 上优于未引导方案及其他代理模型（如使用 SAFIRE 或 PSCC‑Net 作为引导源）。这背后的因果机制是：TruFor 在特征空间中提供了更准确的“编辑‑未编辑”判别梯度，使对抗优化能更有效地将编辑区域特征推离未编辑区域。

![[assets/figures/papers/paper_list_l2490_https_openaccess_thecvf_com_content_CVPR2026_html_Chen_Forensic_Friendly/figures/009_Table_4.jpg]]
*Table 4: Impact of different guidance models*

值得注意的是，即使不使用显式引导（仅依赖 Phase I 正交投影 + Phase II 隐式检测的阈值判断），FFIM 仍能获得可观的性能提升。显式引导的作用是在隐式检测判定相似度过高时进行针对性补救，是一种“按需激活”的增强机制。

---

### 失败模式与局限性

1.  **代理模型依赖瓶颈。** 当显式引导使用的取证模型对特定编辑类型不敏感时（例如，针对 JPEG 压缩伪造训练的模型面对扩散模型生成的编辑），对抗梯度可能误导噪声优化方向，导致引导效果下降甚至退化。这一问题在 Table 4 中使用非最优代理模型时已有所体现。

2.  **超参数敏感性。** 相似度阈值 τ 和对抗优化步长需手工调节。τ 过大会导致显式引导频繁触发，增加计算开销；τ 过小则可能漏过取证不可分的样本。当前缺乏根据图像内容自适应调整 τ 的机制。

3.  **极端范数约束的不可用性。** 如 ℓ∞ 投影所示，过度追求取证可区分性会导致生成内容崩溃。这一现象揭示了取证优化与生成质量之间的根本性张力，需要在约束设计层面进行更精细的控制。

4.  **范式兼容性未验证。** 当前方法基于 DDPM/DDIM 的显式噪声预测范式设计，尚未在 SD3、FLUX 等直接预测模型上验证。这些模型不显式采样 ε_t，正交投影策略需要重新设计。

5.  **下游鲁棒性未知。** FFIM 编辑图像在经历再次编辑、有损压缩或社交媒体传输后，内生取证线索是否依然稳健，目前缺乏系统性评估。

### 补充图表

![[assets/figures/papers/paper_list_l2490_https_openaccess_thecvf_com_content_CVPR2026_html_Chen_Forensic_Friendly/figures/008_Figure_5.jpg]]
*Figure 5: Impact of different norm constraints in FFIM*

![[assets/figures/papers/paper_list_l2490_https_openaccess_thecvf_com_content_CVPR2026_html_Chen_Forensic_Friendly/figures/003_Figure_3.jpg]]
*Figure 3: Qualitative comparisons in pixel-level localization of Evaluation I. For user requests, we present the server’s editing results using baseline DDPM [21], ReLoc [70], and the proposed*

## 方法谱系与知识库定位

### 1. 核心基线对比

FFIM 处于**取证友好图像生成**这一新兴交叉方向，其直接对比对象可分为生成范式和取证增强策略两类。

**标准潜在扩散模型 (DDPM/DDIM)。** 作为生成基线，**DDPM**（Ho et al., NeurIPS 2020）及其确定性采样变体 DDIM 在去噪过程中直接采样高斯噪声 $\epsilon_t \sim \mathcal{N}(0,1)$，不施加任何取证约束。这使得编辑区域与未编辑区域在取证特征空间中高度相似，第三方被动取证模型难以区分。FFIM 的核心改造正是在此噪声采样环节引入正交投影与对抗优化，将“无约束噪声”替换为“取证可区分噪声” $\epsilon_t^\perp$，从而在不改变模型架构的前提下赋予生成过程内生的取证线索。

**后处理式取证增强方法 ReLoc。** **ReLoc**（Zhuang et al., IEEE TIFS 2023）采用后处理策略，在图像生成完成后叠加扰动以增强取证可检测性。这种“先编辑后增强”的范式存在两个结构性局限：其一，后处理扰动可能与用户编辑需求产生不可预见的冲突，导致视觉质量下降；其二，增强效果受限于已生成图像的特征空间，缺乏对生成过程本身的控制力。FFIM 则从根本上将取证优化嵌入去噪过程，通过 Phase I 的正交投影在生成空间内部构建差异性子空间，再通过 Phase II/III 在取证空间中验证和强化这种差异。实验表明，FFIM 在像素级定位 F1 上显著优于 ReLoc（Table 1），且用户主观满意度（4.15 vs. 基线 4.17）无显著下降。

### 2. 方法谱系中的位置

FFIM 的方法论贡献可沿以下维度定位：

**生成控制维度。** 现有可控生成方法多聚焦于语义控制（如文本提示、掩膜条件、ControlNet 等），FFIM 首次将控制目标拓展至**取证空间的可区分性**，且这种控制是内生的——不依赖服务器提供水印或溯源信息，仅利用生成过程中采样的噪声作为调控旋钮。

**取证防御维度。** 传统主动取证防御（如深度水印、指纹嵌入）依赖发送方与检测方的共识协议，在无共识的第三方取证场景中失效。FFIM 填补了这一空白：它使编辑图像天然携带可供任意第三方取证模型利用的区域差异特征，无需任何先验信息共享。

**噪声利用范式。** 扩散模型中的随机噪声通常被视为“熵源”或“多样性驱动”，FFIM 将其重新定位为**取证可区分性的载体**。通过正交投影提取噪声中与当前潜特征正交的分量，并以累积缓冲区 $\mathcal{B}_t$ 维持跨步一致性，FFIM 实现了对噪声的结构化利用，而非简单的随机采样。

### 3. 适用边界与局限

尽管 FFIM 在多个基准上取得显著提升，其适用边界受以下因素制约：

**对取证代理模型的依赖。** Phase III 的显式引导需要预训练取证模型（如 TruFor）提供梯度信号。当代理模型的泛化能力不足以覆盖当前编辑类型时，引导效果可能下降甚至失效。消融实验（Table 4）显示，使用不同代理模型时 F1 提升幅度存在差异，说明 FFIM 的性能上限与所选代理模型强相关。

**超参数敏感性。** 相似度阈值 $\tau$ 和对抗优化步长需手工调节，缺乏对图像内容和编辑类型的自适应机制。这在实际部署中可能导致需要针对不同场景反复调参。

**范数约束的实用边界。** 消融实验（Table 3）揭示了一个关键权衡：$\ell_\infty$ 投影（#6）虽能获得 +33.0% F1 的巨大提升，但生成结果退化为不可用的噪声图像（“noisy gibberish”）；$\ell_2$ 投影（#8）则在 +13.0% F1 提升与视觉质量之间取得平衡，成为最终选择的实用方案。这表明取证优化与视觉质量之间存在根本性张力，极端约束下难以两全。

**模型范式兼容性。** 当前 FFIM 的设计基于 DDPM/DDIM 的噪声预测范式（$\epsilon$-prediction），其正交投影操作直接作用于预测噪声 $\epsilon_t$。对于 SD3、FLUX 等采用直接预测或流匹配范式的新一代扩散模型，该方法无法直接迁移。

**计算开销。** Phase II 的隐式检测需在每步（或每隔若干步）执行解码、取证特征提取和相似度计算；Phase III 的显式引导还需额外梯度反传。这增加了推理延迟，可能在实时交互场景中构成瓶颈。

### 4. 开放问题

1.  **跨范式泛化。** 如何将 FFIM 的噪声调整策略扩展到不依赖显式噪声预测的扩散模型（如 SD3 的 rectified flow、FLUX 的混合架构）？这可能需要重新定义“可调控噪声”的概念，或寻找其他可介入的中间表示。

2.  **自适应阈值机制。** 能否设计数据驱动的 $\tau$ 选择策略，根据图像内容复杂度、编辑区域面积、取证代理模型的置信度等因素动态调整检测门限，减少人工调参负担？

3.  **通用取证代理模型。** 当前方案依赖单一取证模型提供梯度信号，存在过拟合风险。是否存在更通用的取证特征空间，能够覆盖更广泛的编辑类型（如拼接、修复、局部重绘），使 FFIM 对任意第三方取证算法均有效？

4.  **动态权衡策略。** 如何在多步去噪过程中自适应地分配取证优化强度——例如在早期步骤侧重布局生成、后期步骤侧重取证特征增强——以在视觉质量与取证可区分性之间取得更优的帕累托前沿？

5.  **下游鲁棒性。** FFIM 生成的编辑图像在经历有损压缩、二次编辑、社交媒体传输等下游处理后，其内生的取证线索是否依然稳健？这需要系统性的鲁棒性评估，目前尚未覆盖。

## 原文 PDF

![[paperPDFs/CVPR_2026/Forensic_Friendly_Image_Manipulation_via_Controllable_Latent_Diffusion.pdf]]