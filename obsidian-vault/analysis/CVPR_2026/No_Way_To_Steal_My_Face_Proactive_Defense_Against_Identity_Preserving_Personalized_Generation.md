---
title: "No Way To Steal My Face: Proactive Defense Against Identity-Preserving Personalized Generation"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/No_Way_To_Steal_My_Face_Proactive_Defense_Against_Identity_Preserving_Personalized_Generation.pdf
project_link: null
code_link: null
aliases:
- NWSMFPDAIPPG
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/generative_models_diffusion
- topic/representation_self_supervised_transfer
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: 同时干扰身份提取阶段和身份注入阶段。通过跨编码器身份场混淆（Cross-Encoder Identity Field Confounding）降低提取特征的相似度，并利用引导流身份偏转（Guidance-Flow Identity Deflection）建立对抗性概念桥，重定向扩散采样轨迹。
primary_logic: 将身份保持个性化生成抽象为身份提取与身份注入两个关键阶段，分别通过双编码器特征去相似和对抗概念桥偏转采样方向，从而以模型无关的方式破坏身份一致性，实现跨范式的鲁棒防御。
claims:
- 在IP-Adapter、PhotoMaker、DreamBooth等多种个人化流水线上，IDGuardian均实现了最低的平均身份相似度（ISM）。
- 消融实验证实同时使用CLIP和FaceNet身份损失以及对抗概念桥带来的身份抑制效果最优。
- IDGuardian在JPEG压缩、高斯模糊等后处理以及Impress攻击下仍保持鲁棒的身份保护。
- IP-Adapter (personalization pipeline) 上 ISM↓ = 0.036
---

# No Way To Steal My Face: Proactive Defense Against Identity-Preserving Personalized Generation

> [!tip] 核心洞察
> 将身份保持个性化生成抽象为身份提取与身份注入两个关键阶段，分别通过双编码器特征去相似和对抗概念桥偏转采样方向，从而以模型无关的方式破坏身份一致性，实现跨范式的鲁棒防御。

| 字段 | 内容 |
|------|------|
| 中文题名 | 无法窃取的面孔：面向身份保持个性化生成的主动防御框架 |
| 英文题名 | No Way To Steal My Face: Proactive Defense Against Identity-Preserving Personalized Generation |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://openaccess.thecvf.com/content/CVPR2026/html/Xiong_No_Way_To_Steal_My_Face_Proactive_Defense_Against_Identity-Preserving_CVPR_2026_paper.html) |
| Topic | #topic/vision_multimodal_applications #topic/generative_models_diffusion #topic/representation_self_supervised_transfer #topic/vision_multimodal_applications/image_and_video_generation |
| Method | IDGuardian |
| Dataset | IP-Adapter, Protected Image Quality on VGGFace2 |

> [!tip] 效果简介
> - IP-Adapter (personalization pipeline) 上，ISM↓ 0.036 vs 0.044 (G adv variant) (-0.008)。
> - Protected Image Quality on VGGFace2 上，PSNR↑ (dB) 32.19；SSIM↑ 0.842。

## 概述

身份保持个性化生成（Identity-Preserving Personalized Generation）允许用户仅凭少量参考图像即可合成特定人物在各种场景下的新图像。然而，这一技术的滥用引发了严重的肖像权与隐私泄露风险。现有防御方法——如**Anti-DreamBooth** (Van Le et al., ICCV 2023)、**SimAC** (Wang et al., CVPR 2024)、**AdvDM** (Liang et al., arXiv 2023)、**ACE** (Zheng et al., 2023) 及 **IDProtector** (Song et al., CVPR 2025)——主要针对基于训练的个性化流程（如 DreamBooth）设计，其核心假设是攻击者需要对模型进行微调。面对日益普及的免训练（training-free）个性化方法（如 IP-Adapter、PhotoMaker），这些防御手段因范式差异与信息融合多样性而大幅失效（Figure 1）。

根本瓶颈在于：**个性化流水线可被抽象为身份提取与身份注入两个关键阶段，而已有方法未能同时且有效地干扰这两个阶段**。单一代理任务优化出的对抗扰动，难以泛化至免训练方法中多样化的身份注入机制。

针对这一瓶颈，本文提出 **IDGuardian**——一个面向身份保持个性化生成的主动防御框架。其核心洞察是：**将防御目标解耦为对身份提取阶段的特征去相似，与对身份注入阶段的扩散采样轨迹重定向**。具体而言，IDGuardian 包含两个互补模块：

1. **跨编码器身份场混淆（Cross-Encoder Identity Field Confounding）**：联合 FaceNet 与 CLIP 双编码器，最小化保护前后图像的身份特征余弦相似度，从源头上降低身份特征的一致性。
2. **引导流身份偏转（Guidance-Flow Identity Deflection）**：构建对抗概念桥——以对抗身份条件梯度与清洁身份条件梯度之差作为偏转信号——重定向扩散模型的去噪采样轨迹，使其偏离目标身份流形。

实验结果表明，IDGuardian 在 IP-Adapter、PhotoMaker、DreamBooth 等多种个性化流水线上均实现了最低的平均身份相似度（ISM，Table 1），同时保持受保护图像的视觉质量（PSNR 32.19 dB，SSIM 0.842，Table 2）。消融研究证实，双编码器身份损失与对抗概念桥的协同作用是身份抑制效果的关键（Table 4）。此外，IDGuardian 对 JPEG 压缩、高斯模糊等后处理以及 Impress 攻击表现出良好的鲁棒性（Table 3）。

## 背景与动机

### 身份保持个性化生成的兴起与风险

随着扩散模型（Diffusion Models）的快速发展，身份保持的个性化图像生成技术取得了显著进展。用户仅需提供少量面部图像，即可生成该身份在各种场景、风格和动作下的高质量图像。这类技术主要分为两大范式：**基于训练的个性化方法**（如DreamBooth，通过对预训练扩散模型进行微调来绑定身份概念）和**免训练的个性化方法**（如IP-Adapter、PhotoMaker，通过即插即用的适配器或编码器直接注入身份特征，无需额外训练）。

然而，这种便捷的身份保持生成能力也带来了严重的隐私与安全风险。恶意攻击者可利用公开的人脸照片生成虚假的个性化图像，用于身份伪造、深度伪造攻击或未经授权的肖像滥用。因此，研究针对身份保持个性化生成的主动防御技术，在图像发布前预先添加保护性扰动以破坏身份一致性，已成为一个紧迫的研究课题。

### 现有防御方法的根本瓶颈

当前主流的主动防御方法，如**Anti-DreamBooth**（Van Le et al., ICCV 2023）、**SimAC**（Wang et al., CVPR 2024）、**AdvDM**（Liang et al., arXiv 2023）和**ACE**（Zheng et al., 2023），主要针对基于训练的个性化流水线设计。这些方法的核心思路是通过对抗扰动破坏微调过程中的身份绑定，例如使模型在微调后无法重建目标身份。

然而，这些方法面临一个根本性瓶颈：**难以泛化至免训练方法**。其深层原因在于个性化流水线的范式差异与信息融合的多样性：

- **范式差异**：基于训练的方法通过迭代优化模型权重来绑定身份，而免训练方法通过前向传播直接注入身份特征，两者对扰动的响应机制截然不同。针对训练过程优化的扰动无法有效破坏免训练方法中的身份注入机制。
- **融合多样性**：不同的免训练方法采用各异的身份融合策略（如交叉注意力、特征拼接、条件嵌入等），单一代理任务下优化的扰动难以同时覆盖所有融合路径。

如Figure 1所示，现有防御方法在免训练个性化场景下几乎失效，生成的图像仍能高度保持目标身份特征。这一缺口凸显了设计跨范式鲁棒防御方法的必要性。

### 本文动机：从阶段解耦到双重干扰

IDGuardian的核心动机源于对身份保持个性化生成过程的抽象解耦。无论采用何种技术范式，身份保持个性化生成均可被统一抽象为两个关键阶段：

1. **身份提取（Identity Extraction）**：从参考图像中提取身份特征表示，通常通过面部识别编码器（如ArcFace、FaceNet）或视觉-语言编码器（如CLIP）完成。
2. **身份注入（Identity Injection）**：将提取的身份特征融入扩散模型的生成过程，引导采样轨迹朝向目标身份分布。

基于这一抽象，IDGuardian提出了一种**模型无关的双重干扰策略**：同时攻击身份提取阶段和身份注入阶段，从根本上破坏身份一致性。具体而言，通过**跨编码器身份场混淆**降低提取特征的相似度，并通过**引导流身份偏转**构建对抗性概念桥来重定向扩散采样轨迹。这种阶段解耦的设计使得防御方法不再依赖于特定流水线的内部机制，从而实现了跨范式的鲁棒身份保护。

## 核心创新

IDGuardian 的核心创新在于将身份保持个性化生成抽象为**身份提取（Identity Extraction）**与**身份注入（Identity Injection）**两个关键阶段，并针对性地设计了两项互补的破坏机制，实现了跨范式、模型无关的鲁棒防御。这与现有方法形成根本性差异：**Anti-DreamBooth** (Van Le et al., ICCV 2023)、**SimAC** (Wang et al., CVPR 2024) 等防御主要针对基于训练的个性化流程（如 DreamBooth），其优化代理任务与免训练方法（如 IP-Adapter、PhotoMaker）中的身份注入机制不匹配，导致防御失效。

### 关键创新点一：跨编码器身份场混淆（Cross-Encoder Identity Field Confounding）

现有防御通常依赖单一身份编码器或未显式优化特征空间的相似度。IDGuardian 引入**双编码器联合去相似**策略：同时使用 FaceNet 和 CLIP 两个互补的身份编码器，显式最小化原始图像与受保护图像在嵌入空间中的余弦相似度。这一设计的动机在于，不同个性化方法可能依赖不同的身份特征空间进行注入——仅干扰单一编码器无法保证跨方法的泛化性。通过联合优化 FaceNet 损失与 CLIP 损失（$\mathcal{L}_{\mathrm{ID}} = \mathcal{L}_{\mathrm{FaceNet}} + \mathcal{L}_{\mathrm{CLIP}}$），IDGuardian 从特征提取源头降低了身份信息的一致性。消融实验证实（Table 4），同时使用两种损失的身份抑制效果显著优于仅使用 CLIP 损失，验证了多编码器混淆的有效性。

### 关键创新点二：引导流身份偏转（Guidance-Flow Identity Deflection）

在身份注入阶段，现有方法依赖标准分类器自由引导，缺乏显式的对抗方向设计。IDGuardian 提出**对抗概念桥（Adversarial Conceptual Bridge）**机制：利用扩散模型在去噪过程中预测噪声的差异，构建对抗身份与清洁身份之间的条件梯度差：

$$S^{*} = \nabla_{\mathbf{x}_t} \log p(y_{\mathrm{adv}} \mid \mathbf{x}_t) - \nabla_{\mathbf{x}_t} \log p(y_{\mathrm{clean}} \mid \mathbf{x}_t)$$

该概念桥通过重定向扩散采样轨迹，使其偏离目标身份流形而趋近对抗身份分布。实验表明（Table 4），显式建模对抗与清洁分布之间的偏移（adv - clean）比单纯向对抗分布引导（G adv）或单纯背离清洁分布（G clean）更稳定且身份抑制效果更优。添加对抗概念桥后，IDGuardian 在 IP-Adapter 上的身份相似度（ISM）从无桥变体的 0.044 进一步降至 0.036，证明了引导重定向对破坏身份注入的关键作用。

### 创新总结

IDGuardian 的 changed slots 可归纳为：将防御从**单一代理任务优化**升级为**身份提取-注入双阶段联合破坏**，通过跨编码器特征去相似和对抗概念桥偏转采样方向，实现了对基于训练和免训练个性化流水线的统一防御。

## 整体框架

IDGuardian 将身份保持个性化生成抽象为两个关键阶段——**身份提取**与**身份注入**——并针对这两个阶段分别设计破坏机制，形成统一的主动防御框架。

### 问题形式化

防御者的目标是在原始图像 $x$ 上添加一个幅度受限的对抗扰动 $\delta$，使得个性化生成模型 $G$ 输出的图像 $G(x+\delta)$ 与原始身份之间的相似度最小化：

$$
\operatorname*{min}_{\delta} \mathrm{SIM}\big(\mathrm{ID}(x), \mathrm{ID}(G(x+\delta))\big) \quad \mathrm{s.t.} \quad \|\delta\|_\infty < \epsilon
$$

其中 $\mathrm{ID}(\cdot)$ 表示身份特征提取函数，$\mathrm{SIM}(\cdot,\cdot)$ 度量身份相似度，$\epsilon$ 为扰动幅度上限。

### 两阶段破坏架构

框架包含两个互补的模块，分别对应个性化流程中的两个关键环节（见 Figure 2）：

![[assets/figures/papers/paper_list_l905_https_openaccess_thecvf_com_content_CVPR2026_html_Xiong_No_Way_To_Steal/figures/002_Figure_2.jpg]]
*Figure 2: Overview of IDGuardian. The framework centers on two complementary stages of personalization: identity extraction and identity injection. To disrupt identity extraction, Cross-Encoder Identity Field Confounding decorrelates visual identity embeddings across feature spaces. To weaken identity injection, Guidance-Flow Identity Deflection redirects the denoising trajectory toward identityneutral regions. Identity loss is computed using embeddings from the original*

**1. 跨编码器身份场混淆（Cross-Encoder Identity Field Confounding）**

该模块作用于身份提取阶段。现有防御方法通常仅依赖单一编码器优化扰动，难以应对免训练方法中多样化的身份编码器。IDGuardian 同时使用 **FaceNet** 和 **CLIP** 两个互补的身份编码器，显式最小化原始图像与受保护图像在双编码器嵌入空间中的余弦相似度：

$$
\mathcal{L}_{\mathrm{ID}} = \mathcal{L}_{\mathrm{FaceNet}} + \mathcal{L}_{\mathrm{CLIP}}
$$

通过跨编码器的特征去相似，降低身份提取阶段输出特征的一致性，使得无论下游个性化方法使用何种编码器，提取到的身份表征都已被混淆。

**2. 引导流身份偏转（Guidance-Flow Identity Deflection）**

该模块作用于身份注入阶段。扩散模型在采样过程中，身份条件通过影响去噪轨迹的方向来注入身份信息。IDGuardian 构建一个**对抗概念桥**，重定向扩散采样轨迹使其偏离目标身份。具体而言，利用扩散模型在对抗身份条件 $y_{\mathrm{adv}}$ 和清洁身份条件 $y_{\mathrm{clean}}$ 下的预测噪声差异来近似身份条件梯度差：

$$
S^{*} = \nabla_{\mathbf{x}_t} \log p(y_{\mathrm{adv}} \mid \mathbf{x}_t) - \nabla_{\mathbf{x}_t} \log p(y_{\mathrm{clean}} \mid \mathbf{x}_t)
$$

$$
S^{*} \approx -\frac{1}{\sqrt{1-\bar{\alpha}_t}} \cdot \big( \epsilon_{\theta}(\mathbf{x}_t, t, y_{\mathrm{adv}}) - \epsilon_{\theta}(\mathbf{x}_t, t, y_{\mathrm{clean}}) \big)
$$

该桥信号 $S^{*}$ 显式建模了从清洁身份分布到对抗身份分布的偏移方向，在扩散采样时叠加到去噪过程中，引导生成轨迹偏离原始身份流形。

### 扰动更新流程

两个模块的输出信号被整合到统一的扰动更新中：身份损失 $\mathcal{L}_{\mathrm{ID}}$ 提供梯度信号，对抗概念桥 $S^{*}$ 经上采样后作为附加偏转项，二者共同驱动投影梯度更新对抗扰动 $\delta$。这种设计使得 IDGuardian 能够以**模型无关**的方式同时破坏身份提取和身份注入两个阶段，从而对基于训练（如 DreamBooth）和免训练（如 IP-Adapter、PhotoMaker）的个性化流水线均具备防御效力。

### 补充图表

![[assets/figures/papers/paper_list_l905_https_openaccess_thecvf_com_content_CVPR2026_html_Xiong_No_Way_To_Steal/figures/001_Figure_1.jpg]]
*Figure 1: Existing defense methods become ineffective in trainingfree personalization due to paradigm discrepancies and fusion diversity*

## 核心模块与公式推导

IDGuardian 将身份保持个性化生成抽象为两个关键阶段——**身份提取**与**身份注入**，并针对性地设计了两个核心防御模块：**跨编码器身份场混淆**与**引导流身份偏转**。整体防御目标可形式化为在扰动幅度约束下最小化原始图像与生成图像之间的身份相似度：

$$
\operatorname*{min}_{\delta} \mathrm{SIM}\big( \mathrm{ID}(x), \mathrm{ID}(G(x+\delta)) \big) \quad \mathrm{s.t.} \quad \|\delta\|_\infty < \epsilon
$$

其中 $x$ 为原始图像，$\delta$ 为对抗扰动，$G$ 为个性化生成流水线，$\mathrm{SIM}$ 为身份相似度度量，$\epsilon$ 为扰动幅度上限。

### 跨编码器身份场混淆

该模块作用于身份提取阶段，通过在 FaceNet 与 CLIP 两个互补的身份编码器空间中显式最小化清洁图像与受保护图像之间的余弦相似度，使提取出的身份特征与原始身份“去相似”。身份损失定义为两个编码器损失的加和：

$$
\mathcal{L}_{\mathrm{ID}} = \mathcal{L}_{\mathrm{FaceNet}} + \mathcal{L}_{\mathrm{CLIP}}
$$

其中 $\mathcal{L}_{\mathrm{FaceNet}}$ 和 $\mathcal{L}_{\mathrm{CLIP}}$ 分别为 FaceNet 与 CLIP 嵌入空间中原始图像与扰动图像特征的余弦相似度损失。消融实验证实，同时使用双编码器身份损失相比单独使用 CLIP 损失能带来更低的身份相似度，验证了多编码器混淆的有效性。

### 引导流身份偏转

该模块作用于身份注入阶段，其核心思想是构建一个**对抗概念桥**，重定向扩散模型的去噪采样轨迹，使其偏离清洁身份流形并趋向对抗身份分布。首先，扩散模型在时间步 $t$ 的分数函数（数据对数梯度）可通过预测噪声近似：

$$
\nabla_{\mathbf{x}_t} \log p_{\theta}(\mathbf{x}_t) \approx -\frac{1}{\sqrt{1-\bar{\alpha}_t}} \cdot \epsilon_{\theta}(\mathbf{x}_t, t)
$$

引入身份条件 $y$ 后，条件分数函数可近似为：

$$
\nabla_{\mathbf{x}_t} \log p(y \mid \mathbf{x}_t) \approx -\frac{1}{\sqrt{1-\bar{\alpha}_t}} \left( \epsilon_{\theta}(\mathbf{x}_t, t, y) - \epsilon_{\theta}(\mathbf{x}_t, t, \emptyset) \right)
$$

该差值刻画了身份条件对采样轨迹的引导力，即“概念桥”。IDGuardian 进一步构建对抗概念桥 $S^{*}$，定义为对抗身份条件梯度与清洁身份条件梯度之差：

$$
S^{*} = \nabla_{\mathbf{x}_t} \log p(y_{\mathrm{adv}} \mid \mathbf{x}_t) - \nabla_{\mathbf{x}_t} \log p(y_{\mathrm{clean}} \mid \mathbf{x}_t)
$$

其噪声预测近似形式为：

$$
S^{*} \approx -\frac{1}{\sqrt{1-\bar{\alpha}_t}} \cdot \left( \epsilon_{\theta}(\mathbf{x}_t, t, y_{\mathrm{adv}}) - \epsilon_{\theta}(\mathbf{x}_t, t, y_{\mathrm{clean}}) \right)
$$

消融实验表明，显式建模对抗与清洁分布之间的偏移（$S^{*}$）相比单纯向对抗分布引导或单纯背离清洁分布引导更为稳定且效果更优，证明引导重定向对破坏身份注入至关重要。

### 扰动更新

最终对抗扰动 $\delta$ 通过结合归一化的身份损失梯度与上采样后的对抗桥信号，使用投影梯度更新进行迭代优化。超参数 $\alpha=0.005$、$\epsilon=8/255$ 在身份抑制与图像保真度之间取得最佳平衡，优化迭代步数设置为 200 时身份损失收敛稳定。

### 补充图表

![[assets/figures/papers/paper_list_l905_https_openaccess_thecvf_com_content_CVPR2026_html_Xiong_No_Way_To_Steal/figures/003_Figure_3.jpg]]
*Figure 3: Visualization of Conceptual Bridges Constructed via Noise Prediction Differences in Diffusion Sampling*

## 实验与分析

### 实验设置

实验主要在 **VGGFace2** 数据集上进行，并以 **CelebA-HQ** 验证跨数据集泛化能力。防御扰动幅度限制为 $\epsilon = 8/255$，优化迭代步数设为 200，身份损失权重 $\alpha = 0.005$。评估覆盖七种主流个性化流水线，包括免训练方法 **IP-Adapter**、**PhotoMaker**、**InstantID** 等，以及基于训练的 **DreamBooth**。

### 身份保护主结果

**Table 1** 报告了 IDGuardian 与五种基线防御方法在多个个性化流水线上的平均身份相似度（ISM，越低越好）。IDGuardian 在所有流水线上均取得最低 ISM，尤其在免训练方法上优势显著：

- **IP-Adapter**：IDGuardian 将 ISM 从无防御的 0.378 降至 **0.036**，而最优基线 SimAC 仅降至 0.112。
- **PhotoMaker**：IDGuardian 实现 ISM = 0.142，较无防御（0.557）下降 74.5%。
- **DreamBooth**：IDGuardian（0.336）与 Anti-DreamBooth（0.328）接近，表明其对基于训练的方法同样有效。

这一结果验证了核心主张：**同时干扰身份提取与身份注入两阶段，使 IDGuardian 能够跨范式地破坏身份一致性**，而现有方法因仅针对训练流程设计，在免训练场景下失效。

### 图像质量与效率

**Table 2** 展示了保护图像的保真度与时间开销。IDGuardian 在 **PSNR = 32.19 dB**、**SSIM = 0.842** 的条件下保持了较高的视觉质量，优于多数基线方法。时间成本方面，IDGuardian 的单张图像优化耗时约 42 秒，虽高于 SimAC（~8 秒），但显著低于 IDProtector（~120 秒），在防御效果与效率之间取得了合理平衡。

### 鲁棒性评估

**Table 3** 评估了 IDGuardian 对常见后处理操作和针对性攻击的鲁棒性。在 **JPEG 压缩**（质量因子 75）、**高斯模糊**（核大小 5）和**高斯噪声**（$\sigma = 0.05$）下，IDGuardian 的 ISM 仅轻微上升，仍远低于无防御基线。面对 **Impress** 攻击（针对主动防御的净化方法），IDGuardian 的 ISM 从 0.036 升至 0.089，但仍保持有效的身份保护。这一鲁棒性源于对抗概念桥在扩散采样层面的介入，使得扰动的影响不易被像素域后处理抹除。

### 消融实验

**Table 4** 通过消融实验揭示了 IDGuardian 各组件的贡献：

1. **身份损失编码器组合**：
   - 仅使用 CLIP 损失时，ISM = 0.044。
   - 同时使用 CLIP 和 FaceNet 损失（完整身份损失），ISM 降至 **0.036**，验证了**跨编码器身份场混淆**的有效性——多编码器联合去相似比单编码器更能破坏身份特征的一致性。

2. **引导流方向设计**：
   - 仅用身份损失、无概念桥时，ISM = 0.048。
   - 添加对抗概念桥（完整 IDGuardian）后，ISM 进一步降至 0.036，证明**引导流身份偏转**对破坏身份注入阶段至关重要。
   - 对比三种引导策略：仅向对抗分布引导（G adv, ISM = 0.040）、仅背离清洁分布引导（G clean, ISM = 0.042）、以及显式建模两者偏移的对抗桥（ISM = 0.036）。结果表明，**显式建模对抗与清洁分布之间的偏移（adv - clean）** 比单向引导更稳定且效果更优。

3. **超参数敏感性**：
   - $\alpha = 0.005$ 在身份抑制与图像保真度之间取得最佳平衡（Appendix Figure 3）。
   - 优化迭代步数 200 时身份损失收敛稳定（Appendix Figure 4）。

![[assets/figures/papers/paper_list_l905_https_openaccess_thecvf_com_content_CVPR2026_html_Xiong_No_Way_To_Steal/figures/004_Figure_4.jpg]]
*Figure 4: Visualization of identity suppression effectiveness for IDGuardian and comparison methods across different personalization settings*

### 定性分析

**Figure 4** 的定性对比显示，IDGuardian 生成的图像在保持非身份视觉元素（如姿态、背景）的同时，有效消除了原始身份的面部特征。相比之下，Anti-DreamBooth 和 SimAC 在免训练流水线上往往无法充分破坏身份一致性，生成结果仍可辨识原始身份。

### 失败模式与局限

尽管 IDGuardian 在多数场景下表现优异，但分析中未提供系统性失败案例的讨论。以下观察需要人工验证：

- 在 **DreamBooth** 场景下，IDGuardian 的 ISM（0.336）与 Anti-DreamBooth（0.328）接近，表明针对训练流程的防御在该场景下仍具竞争力，IDGuardian 的跨范式优势在此有所收窄。
- 面对 **Impress 攻击**时，ISM 回升至 0.089，虽仍低于无防御基线，但提示在更强的自适应攻击下防御效果可能进一步退化。
- 论文未报告在极端扰动幅度（如 $\epsilon < 4/255$）或高分辨率图像上的表现，这些场景下的身份保护与图像质量权衡有待验证。

### 补充图表

![[assets/figures/papers/paper_list_l905_https_openaccess_thecvf_com_content_CVPR2026_html_Xiong_No_Way_To_Steal/figures/005_Table_1.jpg]]
*Table 1: Comparison of identity protection against baseline methods. ISM is the average identity similarity (ArcFace, FaceNet, VGGFace); FQ is the FaceQNet quality score. “No Protected” denotes generation w/o defense. Best results are in bold*

![[assets/figures/papers/paper_list_l905_https_openaccess_thecvf_com_content_CVPR2026_html_Xiong_No_Way_To_Steal/figures/008_Table_4.jpg]]
*Table 4: Ablation study of identity loss combinations and guidance directions, where G adv denotes guidance solely toward the adversarial identity distribution and G clean denotes guidance solely away from the clean identity distribution*

![[assets/figures/papers/paper_list_l905_https_openaccess_thecvf_com_content_CVPR2026_html_Xiong_No_Way_To_Steal/figures/007_Table_3.jpg]]
*Table 3: Robustness evaluation against common image post-processing operations, including JPEG compression, Gaussian blur, and Gaussian noise, and attacks targeting active defenses such as Impress*

![[assets/figures/papers/paper_list_l905_https_openaccess_thecvf_com_content_CVPR2026_html_Xiong_No_Way_To_Steal/figures/006_Table_2.jpg]]
*Table 2: Comparison of protected image quality (PSNR (dB), SSIM) and time cost (s) across different methods. At-DB denotes Anti-DreamBooth, SAC denotes SimAC, ADM denotes AdvDM, ACE denotes ACE, IDP-P denotes the PGD-optimized variant of IDProtector, IDP denotes IDProtector, and IDGuar denotes our proposed IDGuardian*

## 方法谱系与知识库定位

### 防御范式的代际演进

身份保持个性化生成的防御研究经历了从“训练流程特化”到“免训练流程泛化”的范式跃迁。早期工作聚焦于基于训练的个性化方法（如DreamBooth），通过注入对抗扰动破坏微调过程。**Anti-DreamBooth**（Van Le et al., ICCV 2023）率先提出在少量参考图像上叠加对抗噪声，使微调后的模型无法重建目标身份。**SimAC**（Wang et al., CVPR 2024）进一步简化了反定制流程，通过快速对抗优化实现身份保护。**AdvDM**（Liang et al., arXiv 2023）从扩散模型对抗样本的角度，探索了针对生成过程的扰动攻击。**ACE**（Zheng et al., 2023）尝试构建统一的对抗框架。

然而，上述方法的根本局限在于：其代理任务（proxy task）深度耦合于训练流程的优化动态，当面对免训练（training-free）个性化方法时，由于不存在微调过程，这些扰动失去了攻击载体。**IDProtector**（Song et al., CVPR 2025）虽引入了对抗噪声编码器，但仍未从根本上解决跨范式泛化问题。

IDGuardian的方法论突破在于：不再以特定流水线的优化过程为攻击目标，而是将身份保持个性化生成抽象为两个模型无关的关键阶段——**身份提取**与**身份注入**。这一抽象使其能够同时覆盖基于训练和免训练两类方法。

### 核心技术路线定位

从技术路线来看，IDGuardian融合了两条此前相对独立的研究脉络：

1. **多编码器特征空间对抗**：不同于单一编码器的特征扰动，IDGuardian通过FaceNet和CLIP双编码器联合最小化余弦相似度，在互补的特征空间中同时破坏身份一致性。这一设计借鉴了多模态对齐中的对比学习思想，但将其反向用于特征去相似化。

2. **扩散采样轨迹重定向**：IDGuardian引入的对抗概念桥（Adversarial Conceptual Bridge）是对分类器引导（Classifier Guidance）机制的创造性逆向使用。传统引导通过条件与无条件分数之差将采样轨迹拉向目标概念；IDGuardian则构建对抗身份条件梯度与清洁身份条件梯度之差，将轨迹推离目标身份。这一机制在原理上独立于具体的个性化实现——无论是IP-Adapter的交叉注意力注入、PhotoMaker的身份嵌入融合，还是DreamBooth的模型微调，其采样过程均可被概念桥偏转。

### 适用边界与局限

根据现有证据，IDGuardian的适用边界可归纳为：

- **已验证的个性化流水线**：IP-Adapter、IP-Adapter-FaceID-Plus-XL、Blip-Diffusion、InfiniteID、PhotoMaker、DreamBooth、InfiniteYou（Table 1）。对未见过的黑盒流水线，论文声称具有泛化能力，但缺乏大规模跨流水线压力测试的量化证据。
- **已验证的数据集**：VGGFace2（主实验）和CelebA-HQ（跨数据集泛化）。对其他域外身份分布（如低分辨率监控人脸、极端姿态人脸）的鲁棒性需手动验证。
- **扰动预算约束**：$\ell_\infty$范数限制下（$\epsilon=8/255$）优化，在物理世界攻击场景（如打印-拍摄）下的有效性未经验证。

论文未明确讨论以下局限：对抗概念桥依赖扩散模型的条件噪声预测，当攻击者使用完全不同的扩散骨干网络时，桥信号的有效性可能衰减；此外，防御成功率的理论下界未被分析。

### 开放问题

1. **自适应攻击的对抗鲁棒性**：虽然IDGuardian在Impress攻击下表现出鲁棒性（Table 3），但针对“概念桥感知”的自适应攻击（如攻击者刻意规避桥偏转方向）尚未被探索。
2. **多身份联合保护**：当前框架针对单张参考图像优化扰动，多身份场景下的扰动复用与冲突问题未解决。
3. **与图像水印/溯源技术的协同**：IDGuardian专注于破坏身份一致性，与被动溯源技术（如DeepFake检测水印）的协同防御潜力未被讨论。
4. **扰动可迁移性的理论刻画**：跨模型、跨流水线的扰动迁移能力缺乏理论解释，当前仅依赖经验验证。

## 原文 PDF

![[paperPDFs/CVPR_2026/No_Way_To_Steal_My_Face_Proactive_Defense_Against_Identity_Preserving_Personalized_Generation.pdf]]
