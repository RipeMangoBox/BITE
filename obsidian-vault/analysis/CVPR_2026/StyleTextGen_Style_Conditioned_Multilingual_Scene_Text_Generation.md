---
title: "StyleTextGen: Style-Conditioned Multilingual Scene Text Generation"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/StyleTextGen_Style_Conditioned_Multilingual_Scene_Text_Generation.pdf
project_link: null
code_link: null
aliases:
- StyleTextGen
tags:
- CVPR_2026
- topic/generative_models_diffusion
- topic/generative_models_diffusion/diffusion_image_video
core_operator: 利用双分支风格编码器（文本风格分支 + 视觉先验分支）提取鲁棒的文本感知风格嵌入，配合基于 Gram 矩阵的文本风格一致性损失和遮罩引导的推理时风格注入，实现可靠的跨语言风格迁移。
primary_logic: 通过预训练于风格保持的文本分割任务，文本分支捕获字形、笔触、色彩等细粒度风格线索；视觉分支提供全局外观和色调一致性；两者经交叉注意力融合后，以风格键值对形式注入扩散变换器（DiT）的注意力层，再在训练与推理阶段分别用区域风格损失和遮罩驱动注入精细对齐生成文本与参考风格。
claims:
- 在 AnyWord-Eval 上，句子准确率超越 TextFlux（英语 +5.6%，中文 +3.4%），并全面优于 AnyText 和 Calligrapher。
- 在 StyleText-CE 基准（包括单语和跨语言设置）上，StyleTextGen 在 Sen.Acc、NED、FID、LPIPS 等指标上均显著优于 Calligrapher。
- 消融实验表明，移除双分支编码器中任一分支（文本分支 FID 升至 133.62, 视觉分支升至 124.18）、移除 文本风格一致性损失（FID 升至126.94）或禁用推理时风格注入（FID 升至118.36）均导致风格保真度下降。
- AnyWord-Eval 上 Sentence Accuracy (English) ↑ = 0.7102
---

# StyleTextGen: Style-Conditioned Multilingual Scene Text Generation

> [!tip] 核心洞察
> 通过预训练于风格保持的文本分割任务，文本分支捕获字形、笔触、色彩等细粒度风格线索；视觉分支提供全局外观和色调一致性；两者经交叉注意力融合后，以风格键值对形式注入扩散变换器（DiT）的注意力层，再在训练与推理阶段分别用区域风格损失和遮罩驱动注入精细对齐生成文本与参考风格。

| 字段 | 内容 |
|------|------|
| 中文题名 | StyleTextGen: 风格条件下的多语言场景文本生成 |
| 英文题名 | StyleTextGen: Style-Conditioned Multilingual Scene Text Generation |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2605.14708) |
| Topic | #topic/generative_models_diffusion #topic/generative_models_diffusion/diffusion_image_video |
| Method | StyleTextGen |
| Dataset | AnyWord-Eval, StyleText-CE |

> [!tip] 效果简介
> - AnyWord-Eval 上，Sentence Accuracy (English) ↑ 0.7102 vs TextFlux: ~0.6542 (estimated from +5.6% improvement) (+5.6 percentage points over TextFlux)；Sentence Accuracy (Chinese) ↑ — vs TextFlux (+3.4 percentage points over TextFlux)；FID (English) ↓ 49.51 vs TextFlux / Calligrapher: higher (lower (style quality improvement))。
> - StyleText-CE 上，Sentence Accuracy (Chinese, self-style) ↑ 0.66 vs Calligrapher: <0.66 (outperforms Calligrapher)；Sentence Accuracy (English, self-style) ↑ 0.70 vs Calligrapher: <0.70 (outperforms Calligrapher)；FID (English, external-style) ↓ lower vs Calligrapher: higher (outperforms Calligrapher)。

## 概要

### 问题与瓶颈

场景文本生成任务需要在复杂的自然背景中生成可读且风格一致的文字。现有方法面临一个核心瓶颈：**从复杂背景中精确提取文本风格特征，并保持多语言场景下跨字符的细粒度风格一致性，同时避免风格与内容的纠缠**。具体而言，传统方法难以将字形结构、笔触纹理、色彩分布等细粒度风格线索与背景内容解耦，导致风格迁移时出现伪影、字符风格不统一或文本可读性下降。

### 核心方法与洞察

StyleTextGen 通过三个关键设计解决上述瓶颈：

1. **双分支风格编码器**：文本风格分支（基于 InternViT，预训练于风格保持的文本分割任务）捕获字形、笔触、色彩等细粒度风格线索；视觉先验分支（基于 SigLIP）提供全局外观和色调一致性。两者经交叉注意力融合后，以风格键值对形式注入扩散变换器（DiT）的注意力层。
2. **基于 Gram 矩阵的文本风格一致性损失**：在训练阶段，利用多层 Gram 矩阵度量生成文本区域与参考文本区域的风格差异，强制全局风格对齐，权重系数为 λ=10。
3. **遮罩引导的推理时风格注入**：推理阶段通过文本分割掩码定位区域，对参考图像进行 DiT 反演获取风格键值，再利用 AdaIN 调制与掩码混合，仅在前 10 步去噪中注入风格特征，实现精细的风格对齐。

### 方法谱系与知识库定位

StyleTextGen 位于**风格条件化的多语言场景文本生成**这一细分方向，其方法谱系可追溯至三类工作：

- **多语言视觉文本生成与编辑**：如 **AnyText**（Tuo et al., arXiv 2023），支持多语言场景文本的生成与编辑，但缺乏显式的风格条件控制。
- **自由风格文本图像定制**：如 **Calligrapher**（Ma et al., arXiv 2025），从参考图像中提取风格并迁移到目标文本，但风格编码器缺乏文本内容感知，跨语言风格一致性不足。
- **免 OCR 多语言场景文本合成**：如 **TextFlux**（Xie et al., arXiv 2025），基于 Flux.1-Fill 的扩散变换器实现高质量文本合成，但未针对风格条件进行专门设计。

StyleTextGen 以 TextFlux 的 DiT 骨干为基座（冻结骨干，仅优化新增适配层），通过三个关键槽位创新实现突破：

| 方法槽位 | 基线方案 | StyleTextGen 方案 |
|---------|---------|------------------|
| 风格编码器架构 | 单分支编码器（如 Calligrapher，缺乏文本内容感知） | 双分支风格编码器：文本风格分支 + 视觉先验分支，经交叉注意力融合 |
| 训练损失函数 | 仅使用条件流匹配损失（CFM） | 加入基于 Gram 矩阵的文本风格一致性损失 L_tsc，加权系数 λ=10 |
| 推理阶段风格注入 | 无显式遮罩引导，仅依赖离线风格嵌入 | 遮罩引导的推理时风格注入：AdaIN 调制 + 掩码混合，仅在前 10 步注入 |

### 主要结果

在 **AnyWord-Eval** 基准上，StyleTextGen 的句子准确率超越 TextFlux（英语 +5.6 个百分点，中文 +3.4 个百分点），并全面优于 AnyText 和 Calligrapher；FID 降至 49.51（英语），风格质量显著提升（Table 1, Section 4.4）。

在自建的 **StyleText-CE** 基准（涵盖单语和跨语言设置）上，StyleTextGen 在 Sen.Acc、NED、FID、LPIPS 等指标上均显著优于 Calligrapher（Table 2, Section 4.4）。

消融实验（Table 3, Section 4.6）验证了各组件的关键贡献：移除文本风格分支后 FID 从 113.47 升至 133.62，移除视觉先验分支升至 124.18，移除文本风格一致性损失升至 126.94，禁用推理时风格注入升至 118.36，表明双分支编码器、风格损失和推理注入对风格保真度均不可或缺。

### 局限与开放问题

当前工作仅在中文和英文上进行了系统评估，对阿拉伯文、日文、韩文等文字系统的风格迁移能力未经验证。训练数据主要来源于合成数据，存在艺术风格和字体种类的偏差，真实复杂场景（强光照、严重遮挡）中的泛化性需进一步检验。此外，对于高度艺术化或扭曲的字体，当前风格编码是否足够捕捉极端的纹理和笔触变化，以及推理时风格注入的计算开销能否通过蒸馏进一步降低以适配实时应用，均为待探索的开放问题。

### 问题背景

场景文本生成（Scene Text Generation, STG）旨在将指定的文字内容以逼真的视觉外观嵌入到自然场景图像中，在数据增强、虚拟试穿、海报设计、多语言内容本地化等领域具有广泛的应用价值。与通用图像生成不同，STG 面临一项独特而苛刻的挑战：生成文本不仅需要保持字符级别的字形准确性和可读性，还必须与参考图像中的文本风格——包括字体、笔触、颜色、纹理、光照和透视变形——实现高度一致的对齐。

近年来，基于扩散模型（Diffusion Models）的方法在文本渲染质量上取得了显著进展。以 **AnyText**（Tuo et al., arXiv 2023）为代表的多语言视觉文本生成与编辑方法，以及基于流匹配（Flow Matching）的 **TextFlux**（Xie et al., arXiv 2025），在无需 OCR 辅助的条件下实现了高质量的多语言场景文本合成。**Calligrapher**（Ma et al., arXiv 2025）进一步探索了自由风格的文本图像定制化生成。然而，这些方法在风格控制维度上仍存在明显不足。

### 现有方法的核心瓶颈

当前方法在面对风格条件下的场景文本生成时，普遍陷入一个根本性困境：**从复杂背景中精确提取文本风格特征，并保持多语言场景下跨字符的细粒度风格一致性，同时避免风格与内容的纠缠**。具体表现为以下三个相互关联的瓶颈：

1. **风格编码的文本感知缺失**：现有方法通常采用单分支视觉编码器（如 Calligrapher 的风格提取模块）来捕获参考图像的全局风格。这类编码器缺乏对文本区域的专门感知能力，难以从复杂背景中分离出字形、笔触、色彩等细粒度的文本风格线索，导致风格嵌入中混杂了大量背景噪声。

2. **跨字符风格一致性的弱约束**：在生成多字符文本时，现有方法仅依赖通用的条件流匹配损失（Conditional Flow-Matching Loss, $\mathcal{L}_{\mathrm{CFM}}$）进行优化。该损失函数作用于整幅图像，缺乏对文本区域的显式风格对齐约束，导致同一句子中不同字符之间可能出现风格漂移——例如字体粗细不均、颜色偏移或纹理不一致。

3. **推理阶段风格注入的粗糙性**：在推理生成阶段，现有方法通常仅依赖离线提取的全局风格嵌入进行一次性条件注入，缺乏与生成过程中间特征的精细化交互。这使得风格迁移在面对复杂背景或跨语言场景时，容易出现风格泄露（style leakage）或风格淡化（style dilution）的问题。

### 本文动机

针对上述瓶颈，本文提出 **StyleTextGen**，一个面向风格条件下的多语言场景文本生成框架。其核心动机在于构建一套完整的“风格感知—风格约束—风格注入”机制，使生成模型能够从任意文本风格的参考图像中可靠地提取风格特征，并将其精确地迁移到目标文本的生成过程中。

具体而言，StyleTextGen 的设计围绕三个关键思路展开：

- **双分支风格编码**：通过引入文本风格分支（基于 InternViT，经风格保持的文本分割任务预训练）和视觉先验分支（基于 SigLIP）的协同架构，实现对文本感知风格线索和全局视觉统计的解耦与融合。
- **文本风格一致性损失**：设计基于 Gram 矩阵的区域风格损失函数 $\mathcal{L}_{\mathrm{tsc}}$，在训练阶段对生成文本区域与参考文本区域之间的风格统计量进行显式对齐。
- **遮罩引导的推理时风格注入**：在推理阶段，利用文本分割掩码对参考图像进行 DiT 特征反演，通过自适应实例归一化（AdaIN）和掩码混合策略，将风格特征精确注入生成结果的文本区域。

通过这些设计，StyleTextGen 旨在突破现有方法在风格保真度和跨语言泛化性上的局限，为风格条件下的多语言场景文本生成提供一套更鲁棒、更精细的解决方案。

## 核心方法与创新机理

StyleTextGen 针对现有风格化场景文本生成方法中“风格与内容纠缠、跨语言风格一致性差”的瓶颈，提出了三项关键创新，分别从架构、训练目标和推理策略三个维度进行改进。

### 1. 双分支文本感知风格编码器

现有方法（如 **Calligrapher** (Ma et al., arXiv 2025) 的单分支编码器）在提取文本风格时缺乏对文本内容本身的感知能力，难以精确捕获字形结构、笔触纹理和色彩分布等细粒度风格线索。StyleTextGen 设计了**双分支风格编码器（Dual-Branch Style Encoder）**，由以下两个互补分支构成：

- **文本风格分支（Textual Style Branch）**：基于 InternViT 构建，并通过**风格保持的文本分割（Style-Preserving Text Segmentation）**任务进行预训练。该预训练任务不输出二值掩码，而是要求模型重建包含完整风格信息的文本区域，从而迫使编码器学习到字形结构、笔触纹理、色彩分布等文本专属的风格表征。经过自注意力精炼和 Q-Former 压缩后，得到文本风格表示 $h_{\mathrm{text}}$。
- **视觉先验分支（Visual Prior Branch）**：采用对文本不敏感的通用视觉编码器 SigLIP，提取全局外观和色调一致性等通用视觉先验，经 MLP 投影和 Q-Former 处理后得到视觉先验表示 $h_{\mathrm{vis}}$。

两分支的输出通过**交叉注意力融合**：以文本特征 $h_{\mathrm{text}}$ 作为查询（Query），视觉特征 $h_{\mathrm{vis}}$ 作为键值（Key/Value），得到最终的文本感知风格嵌入 $z_{\mathrm{style}}$。该嵌入随后被投影为额外的键值对，以**风格注意力（Style Attention）**的形式注入扩散变换器（DiT）的注意力层，实现可靠的风格条件化。

### 2. 基于 Gram 矩阵的文本风格一致性损失

传统扩散模型仅使用条件流匹配损失 $\mathcal{L}_{\mathrm{CFM}}$ 进行训练，缺乏对生成文本区域与参考风格之间显式对齐的约束。StyleTextGen 提出了**文本风格一致性损失（Text Style Consistency Loss）** $\mathcal{L}_{\mathrm{tsc}}$，其核心机制如下：

- 利用预训练的 VGG 网络提取多层特征图，分别计算生成文本区域与参考文本区域的 **Gram 矩阵** $G_j^{\phi}(x)$，该矩阵能有效捕获纹理和风格的统计特性。
- 通过文本掩码 $M_{\mathrm{gen}}$ 和 $M_{\mathrm{ref}}$ 精准定位文本区域，计算两者 Gram 矩阵的 Frobenius 距离：

$$\mathcal{L}_{\mathrm{tsc}} = \sum_{j \in J} \left\| G_j^{\phi} \big( M_{\mathrm{gen}} \odot \hat{x} \big) - G_j^{\phi} \big( M_{\mathrm{ref}} \odot I_{style} \big) \right\|_{F}^{2}$$

该损失以权重 $\lambda_{\mathrm{tsc}}=10$ 与流匹配损失组合为总训练目标 $\mathcal{L} = \mathcal{L}_{\mathrm{CFM}} + \lambda_{\mathrm{tsc}} \mathcal{L}_{\mathrm{tsc}}$，强制所有生成字符在笔触、色彩和纹理上与参考风格保持一致。

### 3. 遮罩引导的推理时风格注入

仅依赖训练阶段学习到的风格嵌入在推理时可能无法精确对齐生成区域与参考风格。StyleTextGen 进一步提出了**遮罩引导的推理时风格注入（Mask-Guided Inference Style Injection）**策略：

- 利用文本分割掩码定位参考图像中的文本区域，通过 DiT 反演提取该区域的风格特征键值对 $K_s, V_s$。
- 通过**自适应实例归一化（AdaIN）**将参考文本区域的风格特征迁移到当前生成步骤的键值对 $K, V$ 上，得到风格适应的 $\tilde{K}, \tilde{V}$。
- 使用生成区域掩码 $M_{\mathrm{gen}}$ 将原始键值对与风格适应的键值对进行混合，仅在文本生成区域注入精细化风格特征。
- 该注入仅在前 10 步去噪中执行，平衡了风格一致性与生成质量。

### 创新点的消融验证

消融实验（Table 3）定量验证了上述每项创新的贡献：移除文本风格分支导致 FID 从 113.47 升至 133.62；移除视觉先验分支使 FID 升至 124.18；移除文本风格一致性损失使 FID 升至 126.94；禁用推理时风格注入使 FID 升至 118.36。这些结果表明，三项创新相互协同，共同构成了 StyleTextGen 在跨语言风格化文本生成任务上的核心优势。

StyleTextGen 将风格条件下的多语言场景文本生成建模为一个**基于扩散变换器（DiT）的修复（inpainting）范式**。其核心思想是：给定一张带有文本的场景图像、对应的字形二值图以及一张风格参考图像，模型在目标文本区域生成与参考风格一致的新文本，同时保持背景不变。整体 pipeline 由四个关键模块串联构成，形成从输入构造到风格注入的完整数据流。

### 输入构造与扩散骨干

模型的输入由两部分垂直拼接而成：

$$I_{\mathrm{concat}} = \left[ \begin{array}{l} I_{\mathrm{glyph}} \\ I_{\mathrm{scene}} \end{array} \right]$$

其中 $I_{\mathrm{glyph}}$ 为目标文本的字形二值图，$I_{\mathrm{scene}}$ 为原始场景图像（目标文本区域被掩码遮盖）。这一拼接设计同时为扩散模型提供了文本的结构线索和场景的上下文背景。

扩散骨干采用基于 **Flux.1-Fill** 的 DiT 架构，并初始化为 **TextFlux**（Xie et al., arXiv 2025）的权重。训练过程中，DiT 骨干被冻结，仅优化新增的适配层和线性投影层。前向加噪过程遵循线性调度：

$$x_t = (1 - \sigma_t) x_0 + \sigma_t \epsilon$$

训练目标为条件流匹配损失（Conditional Flow-Matching, CFM），使模型学习预测速度场 $v_\theta$：

$$\mathcal{L}_{\mathrm{CFM}} = \mathbb{E}_{t, x_0, \epsilon} \Big[ \omega_t \big\| v_{\theta}(x_t, t, c) - (\epsilon - x_0) \big\|_2^2 \Big]$$

### 双分支风格编码器

这是 StyleTextGen 的核心创新模块，负责从风格参考图像中提取**文本感知的风格嵌入**。该编码器由两个互补分支组成：

- **文本风格分支**：基于 InternViT，经过风格保持的文本分割任务预训练，能够捕获字形结构、笔触纹理和色彩分布等细粒度风格线索。其编码流程为：

  $$h_{\mathrm{text}} = Q_{\mathrm{text}} \big( S_{\mathrm{text}} \big( E_{\mathrm{text}} (I_{\mathrm{style}}) \big) \big)$$

  其中 $E_{\mathrm{text}}$ 为文本编码器，$S_{\mathrm{text}}$ 为自注意力精炼层，$Q_{\mathrm{text}}$ 为 Q-Former。

- **视觉先验分支**：基于文本不敏感的 SigLIP 编码器，提供全局外观和色调一致性约束。其编码融合了 MLP 投影和 Q-Former 输出：

  $$h_{\mathrm{vis}} = P_{\mathrm{vis}} ( E_{\mathrm{vis}} (I_{\mathrm{style}}) ) + Q_{\mathrm{vis}} ( E_{\mathrm{vis}} (I_{\mathrm{style}}) )$$

两分支的输出通过**交叉注意力融合**，以文本特征为查询、视觉特征为键值，得到最终的文本感知风格嵌入：

$$z_{\mathrm{style}} = \mathrm{Attn} ( h_{\mathrm{text}}, h_{\mathrm{vis}}, h_{\mathrm{vis}} )$$

该风格嵌入随后被投影为键值对 $(K_s, V_s)$，作为额外的风格注意力分支注入 DiT 的注意力层：

$$F_{\mathrm{style}} = \mathrm{SelfAttn}(Q, K, V) + \mathrm{StyleAttn}(Q, K_s, V_s)$$

### 文本风格一致性损失

为在训练阶段强制生成文本与参考文本之间的风格对齐，StyleTextGen 引入了基于 **Gram 矩阵**的文本风格一致性损失 $\mathcal{L}_{\mathrm{tsc}}$。Gram 矩阵用于捕获纹理和风格统计：

$$G_j^{\phi}(x) = \frac{1}{N_j} F_j(x) F_j(x)^{\top}$$

损失函数计算生成文本区域与参考文本区域在多层特征上 Gram 矩阵的 Frobenius 距离：

$$\mathcal{L}_{\mathrm{tsc}} = \sum_{j \in J} \left\| G_j^{\phi} \big( M_{\mathrm{gen}} \odot \hat{x} \big) - G_j^{\phi} \big( M_{\mathrm{ref}} \odot I_{style} \big) \right\|_{F}^{2}$$

其中 $M_{\mathrm{gen}}$ 和 $M_{\mathrm{ref}}$ 分别为生成区域和参考区域的文本分割掩码。最终训练损失为：

$$\mathcal{L} = \mathcal{L}_{\mathrm{CFM}} + \lambda_{\mathrm{tsc}} \mathcal{L}_{\mathrm{tsc}}$$

其中 $\lambda_{\mathrm{tsc}} = 10$。

### 推理时遮罩引导风格注入

在推理阶段，StyleTextGen 进一步引入**遮罩引导的风格注入策略**，以精细化生成文本与参考风格的局部对齐。具体流程为：

1. 利用文本分割掩码 $M_{\mathrm{style}}$ 定位参考图像中的文本区域；
2. 对参考图像进行 DiT 反演，提取风格键值对 $(K_s, V_s)$；
3. 通过自适应实例归一化（AdaIN）将参考风格转移到当前键值对：

   $$\tilde{K}, \tilde{V} = \mathrm{AdaIN}(K, V; K_s \odot M_{\mathrm{style}}, V_s \odot M_{\mathrm{style}})$$

4. 使用生成区域掩码 $M_{\mathrm{gen}}$ 将原始键值对与风格适应的键值对混合：

   $$K' = (1 - M_{\mathrm{gen}}) \odot K + M_{\mathrm{gen}} \odot \tilde{K}, \quad V' = (1 - M_{\mathrm{gen}}) \odot V + M_{\mathrm{gen}} \odot \tilde{V}$$

5. 最终特征输出在生成文本区域融合基础特征与风格参考特征：

   $$f_{out} = (1 - M_{\mathrm{gen}}) \odot f_{\mathrm{base}} + M_{\mathrm{gen}} \odot \mathrm{AdaIN}(f_{\mathrm{base}}; f_{\mathrm{style}} \odot M_{\mathrm{style}})$$

该注入策略仅在去噪的前 10 步中执行，以平衡风格保真度与生成质量。

### 数据流总览

整体 pipeline 的数据流可概括为：**场景图像 + 字形图 → 输入拼接 → DiT 去噪（注入风格键值对）→ 生成图像**。风格参考图像经双分支编码器提取文本感知风格嵌入，在训练阶段通过 $\mathcal{L}_{\mathrm{tsc}}$ 约束风格对齐，在推理阶段通过遮罩引导注入实现精细化风格迁移。这一设计使得 StyleTextGen 能够同时支持**自风格参考**（in-place generation）和**外部风格参考**两种生成模式（见 Figure 2 和 Figure 1 的示例）。

![[assets/figures/papers/paper_list_l2606_https_arxiv_org_abs_2605_14708/figures/002_Figure_2.jpg]]
*Figure 2: Overview of StyleTextGen. (a) Training process. The inpainting input to the diffusion transformer is constructed from a scene text image concatenated with its glyph map. A randomly cropped text patch serves as the style reference. The model is optimized with the flow-matching loss*

StyleTextGen 的核心架构围绕三个关键模块展开：双分支风格编码器、文本风格一致性损失，以及推理阶段遮罩引导的风格注入策略。以下逐一解析其设计动机与数学形式。

### 双分支风格编码器

从复杂背景中精确提取文本风格特征，并保持多语言场景下跨字符的细粒度风格一致性，是场景文本风格迁移的核心瓶颈。StyleTextGen 提出的双分支风格编码器由**文本风格分支**与**视觉先验分支**组成，两者通过交叉注意力融合，产生文本感知的风格嵌入。

**文本风格分支**基于 InternViT，预训练于风格保持的文本分割任务，旨在捕获字形结构、笔触纹理和色彩分布等细粒度风格线索。给定风格参考图像 $I_{\mathrm{style}}$，其编码过程为：

$$h_{\mathrm{text}} = Q_{\mathrm{text}} \big( S_{\mathrm{text}} \big( E_{\mathrm{text}} (I_{\mathrm{style}}) \big) \big)$$

其中 $E_{\mathrm{text}}$ 为 InternViT 编码器，$S_{\mathrm{text}}$ 为自注意力精炼模块，$Q_{\mathrm{text}}$ 为 Q-Former，最终输出精炼后的文本风格表示 $h_{\mathrm{text}}$。

**视觉先验分支**采用文本不敏感的通用视觉编码器 SigLIP，提供全局外观和色调一致性约束。其表示由 MLP 投影与 Q-Former 输出相加得到：

$$h_{\mathrm{vis}} = P_{\mathrm{vis}} ( E_{\mathrm{vis}} (I_{\mathrm{style}}) ) + Q_{\mathrm{vis}} ( E_{\mathrm{vis}} (I_{\mathrm{style}}) )$$

两分支的输出通过交叉注意力融合，以文本特征为查询、视觉特征为键值，得到最终的文本感知风格嵌入：

$$z_{\mathrm{style}} = \mathrm{Attn} ( h_{\mathrm{text}}, h_{\mathrm{vis}}, h_{\mathrm{vis}} )$$

该风格嵌入随后被投影为键值对，作为额外的风格注意力分支注入扩散变换器（DiT）的注意力层：

$$F_{\mathrm{style}} = \mathrm{SelfAttn}(Q, K, V) + \mathrm{StyleAttn}(Q, K_s, V_s)$$

消融实验证实了双分支设计的必要性：移除文本风格分支后，FID 从 113.47 升至 133.62；移除视觉先验分支后，FID 升至 124.18（Table 3）。

### 文本风格一致性损失

为避免风格与内容的纠缠，StyleTextGen 在训练中引入基于 Gram 矩阵的文本风格一致性损失 $\mathcal{L}_{\mathrm{tsc}}$。Gram 矩阵能够捕获特征图各通道之间的相关性，反映纹理和风格的统计特性：

$$G_j^{\phi}(x) = \frac{1}{N_j} F_j(x) F_j(x)^{\top}$$

其中 $F_j(x)$ 为预训练 VGG 网络第 $j$ 层的特征图，$N_j$ 为特征图的元素数。该损失计算生成文本区域与参考文本区域 Gram 矩阵的 Frobenius 距离：

$$\mathcal{L}_{\mathrm{tsc}} = \sum_{j \in J} \left\| G_j^{\phi} \big( M_{\mathrm{gen}} \odot \hat{x} \big) - G_j^{\phi} \big( M_{\mathrm{ref}} \odot I_{\mathrm{style}} \big) \right\|_{F}^{2}$$

其中 $M_{\mathrm{gen}}$ 和 $M_{\mathrm{ref}}$ 分别为生成图像和参考图像中的文本区域掩码。通过仅在文本区域施加风格约束，该损失强制所有生成字符保持统一的风格属性，同时避免对背景区域的干扰。

训练总损失由条件流匹配损失与风格一致性损失组合而成：

$$\mathcal{L} = \mathcal{L}_{\mathrm{CFM}} + \lambda_{\mathrm{tsc}} \mathcal{L}_{\mathrm{tsc}}$$

其中 $\lambda_{\mathrm{tsc}}$ 默认为 10。消融实验表明，移除 $\mathcal{L}_{\mathrm{tsc}}$ 后 FID 升至 126.94（Table 3），验证了该损失对风格对齐的关键作用。

### 推理阶段遮罩引导的风格注入

为进一步提升生成文本与参考风格的精细对齐，StyleTextGen 在推理阶段引入遮罩引导的风格注入策略。该策略仅在去噪的前 10 步中执行，通过文本分割掩码定位生成区域，对参考图像进行 DiT 反演获取风格键值对，再利用自适应实例归一化（AdaIN）和掩码混合将风格特征精确注入。

首先，通过 AdaIN 将参考文本区域的风格特征转移到当前注意力层的键值对：

$$\tilde{K}, \tilde{V} = \mathrm{AdaIN}(K, V; K_s \odot M_{\mathrm{style}}, V_s \odot M_{\mathrm{style}})$$

随后，使用生成区域掩码将原始键值对与风格适应的键值对混合：

$$K' = (1 - M_{\mathrm{gen}}) \odot K + M_{\mathrm{gen}} \odot \tilde{K}, \quad V' = (1 - M_{\mathrm{gen}}) \odot V + M_{\mathrm{gen}} \odot \tilde{V}$$

最终特征输出在生成文本区域融合基础特征与风格参考特征：

$$f_{\mathrm{out}} = (1 - M_{\mathrm{gen}}) \odot f_{\mathrm{base}} + M_{\mathrm{gen}} \odot \mathrm{AdaIN}(f_{\mathrm{base}}; f_{\mathrm{style}} \odot M_{\mathrm{style}})$$

消融实验显示，禁用推理时风格注入后 FID 升至 118.36（Table 3），证实了该模块对最终风格一致性的提升作用。

## 实验与关键发现

### 主实验结果

StyleTextGen 在两个核心基准上进行了系统评估：**AnyWord-Eval**（通用多语言场景文本生成）和 **StyleText-CE**（风格条件下的场景文本生成定制基准）。

**AnyWord-Eval 上的文本准确率与风格质量。** 如 Table 1 所示，StyleTextGen 在英文和中文场景下均全面超越现有方法。在英文句子准确率（Sen.Acc）上，StyleTextGen 达到 0.7102，相比 **TextFlux**（Xie et al., arXiv 2025）提升约 5.6 个百分点；在中文设置下同样取得约 3.4 个百分点的提升。在风格保真度指标 FID 上，StyleTextGen 在英文场景下取得 49.51，显著低于 TextFlux 和 **Calligrapher**（Ma et al., arXiv 2025），表明生成文本与参考风格之间的分布更为接近。同时，StyleTextGen 在所有指标上均优于 **AnyText**（Tuo et al., arXiv 2023），验证了风格条件建模在多语言文本生成中的关键作用。

**StyleText-CE 上的风格迁移能力。** Table 2 报告了在 StyleText-CE 基准上与 Calligrapher 的对比结果，涵盖单语自风格参考（cn、en）和跨语言风格迁移（cn→en、en→cn）四种设置。StyleTextGen 在所有配置下的 Sen.Acc、NED、FID 和 LPIPS 指标上均取得领先。以自风格中文设置为例，StyleTextGen 的 Sen.Acc 达到 0.66，NED 为 0.81；在跨语言英文→中文设置下，Sen.Acc 为 0.60，NED 为 0.79，表明双分支风格编码器能够有效解耦文本内容与视觉风格，实现可靠的跨语言风格迁移。Figure 3 和 Figure 5 分别展示了自风格参考和外部风格参考设置下的定性对比，StyleTextGen 生成的文本在笔触纹理、色彩分布和字形结构上与参考风格高度一致，而基线方法常出现风格丢失或字形变形。

### 消融实验

为量化各模块的贡献，Table 3 报告了在 StyleText-CE 基准上的消融结果，Figure 4 提供了对应的定性可视化。

![[assets/figures/papers/paper_list_l2606_https_arxiv_org_abs_2605_14708/figures/008_Table_3.jpg]]
*Table 3: Quantitative ablation results. We analyze the contributions of the Dual-Branch Style Encoder, the Text Style Consistency Loss*

![[assets/figures/papers/paper_list_l2606_https_arxiv_org_abs_2605_14708/figures/005_Figure_4.jpg]]
*Figure 4: Qualitative results of the ablation study. The left group shows the effects of removing the Text Style Consistency Loss*

**双分支风格编码器。** 完整模型（Full）取得 Sen.Acc 0.659、NED 0.804、FID 113.47、LPIPS 0.482。移除文本风格分支后，FID 从 113.47 急剧上升至 133.62，Sen.Acc 降至 0.618，NED 降至 0.775，表明文本感知编码器对捕获字形结构、笔触纹理和色彩分布等细粒度风格线索至关重要。移除视觉先验分支后，FID 升至 124.18，Sen.Acc 降至 0.634，NED 降至 0.789，验证了视觉先验分支为风格表示提供了稳定的全局外观和色调一致性。定性结果（Figure 4 右组）进一步显示，缺少任一支路均导致生成文本的风格与参考图像出现明显偏差。

**文本风格一致性损失（L_tsc）。** 移除 L_tsc 后，FID 升至 126.94，LPIPS 升至 0.509，Sen.Acc 降至 0.629。该结果证明基于 Gram 矩阵的区域风格损失能有效约束生成文本区域与参考文本区域之间的风格对齐，强制跨字符的风格一致性。Figure 4 左组的对比显示，缺少 L_tsc 时生成文本的笔触粗细和色彩饱和度与参考风格存在明显差异。

**推理时风格注入。** 禁用推理阶段的遮罩引导风格注入后，FID 升至 118.36，Sen.Acc 降至 0.646，NED 降至 0.796。这表明即使训练阶段已学习到风格嵌入，推理时的 AdaIN 调制与掩码混合仍能进一步精细化生成文本区域的风格特征，提升最终输出的风格保真度。

### 公平性说明与局限

当前评估主要覆盖英文和中文两种文字系统，模型在阿拉伯文、日文、韩文等其他文字上的风格迁移能力尚未验证。训练数据来源于合成数据与少量人工筛选的高质量合成图像，可能存在艺术风格和字体种类的偏差，在真实复杂场景（如强光照、严重遮挡）中的泛化性需进一步检验。此外，推理时风格注入需额外的前向反演步骤，计算开销高于纯前馈方案，是否可通过蒸馏或一次性编码降低延迟仍有待探索。

![[assets/figures/papers/paper_list_l2606_https_arxiv_org_abs_2605_14708/figures/004_Table_1.jpg]]
*Table 1: Comparison with state-of-the-art multi-lingual (English and Chines) methods. ↑/↓ indicates higher/lower is better. Our approach outperforms prior methods on all metrics*

![[assets/figures/papers/paper_list_l2606_https_arxiv_org_abs_2605_14708/figures/006_Table_2.jpg]]
*Table 2: Quantitative comparison between Calligrapher and StyleTextGen on the StyleText-CE benchmark under different style reference settings. Columns correspond to monolingual (cn, en) and cross-lingual (cn→en, en→cn) configurations*

![[assets/figures/papers/paper_list_l2606_https_arxiv_org_abs_2605_14708/figures/003_Figure_3.jpg]]
*Figure 3: Qualitative comparison on the StyleText-CE benchmark under the self-style reference setting*

## 定位与知识库关联

### 任务定位与基线关系

StyleTextGen 聚焦于**风格条件下的多语言场景文本生成**，其核心任务是从任意文本风格参考图像中提取风格特征，并在保持文本可读性的前提下将风格迁移到目标文本上。该任务处于场景文本生成、风格迁移与扩散模型可控生成的交叉点。

论文主要与三类基线方法进行对比：

- **AnyText** (Tuo et al., arXiv 2023)：多语言视觉文本生成与编辑方法，侧重于文本渲染的准确性和场景融合，但缺乏对细粒度文本风格的显式建模。
- **Calligrapher** (Ma et al., arXiv 2025)：自由式文本图像定制方法，能够进行风格化文本生成，但其风格编码器为单分支结构，缺乏对文本区域风格线索的专门感知。
- **TextFlux** (Xie et al., arXiv 2025)：基于流匹配的免 OCR 多语言场景文本合成方法，StyleTextGen 的 DiT 骨干网络即采用 TextFlux 权重进行初始化，可视为其风格增强的扩展版本。

### 核心改进与差异化

StyleTextGen 相较于上述基线，在三个关键设计点上实现了差异化改进：

**1. 双分支风格编码器架构（单分支 → 双分支）**

Calligrapher 等基线使用单分支编码器提取风格特征，缺乏对文本区域的针对性感知，容易将背景纹理与文本风格混淆。StyleTextGen 引入双分支架构：**文本风格分支**（基于 InternViT，预训练于风格保持的文本分割任务）捕获字形结构、笔触纹理和色彩分布等细粒度文本风格线索；**视觉先验分支**（基于 SigLIP）提供全局外观和色调一致性约束。两者通过交叉注意力融合，以文本特征为查询、视觉特征为键值，得到文本感知的风格嵌入。消融实验表明，移除文本分支导致 FID 从 113.47 升至 133.62，移除视觉分支则升至 124.18，验证了双分支协同的必要性。

**2. 基于 Gram 矩阵的文本风格一致性损失（仅 CFM 损失 → 联合优化）**

基线方法通常仅使用条件流匹配损失 $\mathcal{L}_{\mathrm{CFM}}$ 进行训练，缺乏对生成文本区域风格一致性的显式约束。StyleTextGen 引入 $\mathcal{L}_{\mathrm{tsc}}$，利用多层 VGG 特征图的 Gram 矩阵，计算生成文本区域与参考文本区域之间的 Frobenius 距离，强制全局风格对齐。该损失加权系数 $\lambda_{\mathrm{tsc}} = 10$。消融实验显示，移除 $\mathcal{L}_{\mathrm{tsc}}$ 后 FID 升至 126.94，证明该损失有效约束了跨字符的风格一致性。

**3. 遮罩引导的推理时风格注入（无显式注入 → 遮罩驱动注入）**

基线方法在推理阶段仅依赖离线编码的风格嵌入，缺乏对生成过程中风格特征的精细化控制。StyleTextGen 提出推理时风格注入策略：利用文本分割掩码定位生成区域，对参考图像进行 DiT 反演获取风格键值对，通过 AdaIN 调制与掩码混合，将风格特征精确注入前 10 步去噪过程。禁用该模块后 FID 升至 118.36，验证了推理阶段精细化注入的增益。

### 方法谱系中的位置

从技术谱系来看，StyleTextGen 处于以下几条技术路线的交汇处：

- **扩散变换器（DiT）用于场景文本生成**：继承自 TextFlux 的流匹配框架，基于 Flux.1-Fill 骨干网络，将场景文本生成建模为修复任务。
- **风格感知编码器设计**：借鉴了风格迁移领域中 Gram 矩阵表示（Gatys et al., CVPR 2016）和 AdaIN（Huang & Belongie, ICCV 2017）的思想，将其适配到扩散模型的注意力机制中。
- **文本分割预训练**：通过风格保持的文本分割预训练任务赋予编码器文本感知能力，这一策略与视觉-语言模型中利用辅助任务增强表征能力的思路一致。

### 适用边界与局限

**已验证的能力边界：**
- 语言系统：论文仅在中文和英文上进行了系统评估，在 AnyWord-Eval 上英语句子准确率达 0.7102，中文较 TextFlux 提升 3.4 个百分点；在 StyleText-CE 基准上，单语和跨语言设置下均显著优于 Calligrapher。
- 风格类型：支持自风格参考（in-place generation）和外部风格参考两种模式，涵盖印刷体、手写体等常见风格。

**已知局限（需人工验证）：**
- 训练数据主要来源于合成数据与少量人工挑选的高质量合成图像，存在艺术风格和字体种类的偏差，在真实复杂场景中的泛化性需进一步检验。
- 论文未报告对其他文字系统（如阿拉伯文、日文、韩文）的支持情况，跨文字系统的风格迁移能力未知。

### 开放问题

1. **多文字系统扩展**：模型能否在无需显式预训练分割模型的情况下，通过自监督方式实现对阿拉伯文、日文等复杂文字系统的可靠文本风格提取？
2. **极端风格鲁棒性**：对于高度艺术化、扭曲或带有强装饰性的字体，当前双分支编码器是否足够捕捉极端的纹理和笔触变化？
3. **真实场景干扰**：强光照、严重遮挡、透视畸变等真实场景干扰对风格提取与生成鲁棒性的影响尚未评估。
4. **推理效率优化**：推理时的风格注入步骤涉及 DiT 反演和多步特征调制，是否可通过蒸馏或一次性编码进一步降低计算开销，使其适用于实时应用场景？

## 原文 PDF

![[paperPDFs/CVPR_2026/StyleTextGen_Style_Conditioned_Multilingual_Scene_Text_Generation.pdf]]
