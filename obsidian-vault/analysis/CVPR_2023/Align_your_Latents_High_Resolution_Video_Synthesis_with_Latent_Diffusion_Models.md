---
title: "Align your Latents: High-Resolution Video Synthesis with Latent Diffusion Models"
type: paper
paper_level: A
venue: CVPR
year: 2023
pdf_ref: paperPDFs/CVPR_2023/Align_your_Latents_High_Resolution_Video_Synthesis_with_Latent_Diffusion_Models.pdf
project_link: https://research.nvidia.com/labs/toronto-ai/VideoLDM/
code_link: null
aliases:
- VLLVDM
- AYLHRVSLDM
tags:
- CVPR_2023
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: "在预训练图像LDM的空间层之间插入可学习的时间层，并固定空间层仅训练时间层，从而将帧对齐问题转化为学习时间一致性的任务。"
primary_logic: "利用大规模图像数据集预训练空间层，再通过少量视频数据训练插入的时间层，即可将图像生成器高效转化为时间一致的视频生成器，极大降低视频训练成本并保留图像生成能力；该时间层还可迁移至不同图像模型变体，实现个性化视频生成。"
claims:
- "Video LDM 在真实驾驶场景视频生成中 FVD 远低于 LVG (356 vs 478)。"
- "视频微调解码器将重建 FVD 从 390.88 降至 32.94，表明时间一致性极大改善。"
- "视频上采样器对比图像上采样器，FVD 从 165.98 降至 45.39，凸显时间对齐的必要性。"
- "用户研究中视频 LDM 生成结果在真实感上显著优于 LVG（62.03% 偏好 vs 31.65%）。"
---

# Align your Latents: High-Resolution Video Synthesis with Latent Diffusion Models

> [!tip] 核心洞察
> 利用大规模图像数据集预训练空间层，再通过少量视频数据训练插入的时间层，即可将图像生成器高效转化为时间一致的视频生成器，极大降低视频训练成本并保留图像生成能力；该时间层还可迁移至不同图像模型变体，实现个性化视频生成。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 对齐潜变量：基于潜扩散模型的高分辨率视频合成 |
| 英文题名 | Align your Latents: High-Resolution Video Synthesis with Latent Diffusion Models |
| 会议/期刊 | CVPR 2023 |
| Links | [paper](https://arxiv.org/abs/2304.08818) · [Project](https://research.nvidia.com/labs/toronto-ai/VideoLDM/) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/image_and_video_generation |
| Method | Video LDM (Latent Video Diffusion Models) |
| Dataset | Real Driving Scenes (RDS), UCF-101 (zero-shot text-to-video), MSR-VTT (zero-shot text-to-video) |

> [!tip] 效果简介
> - Real Driving Scenes (RDS) 上，FVD (↓) 为 356，对比 478 (LVG)，变化 -122。
> - Real Driving Scenes (RDS) 上，FID (↓) 为 51.9，对比 53.5 (LVG)，变化 -1.6。
> - UCF-101 (zero-shot text-to-video) 上，Inception Score (↑) 为 33.45，对比 33.00 (Make-A-Video)，变化 +0.45。

## 概要

高分辨率视频生成的核心瓶颈在于扩散模型在像素空间直接建模长序列视频所需的计算成本极高。若直接使用预训练图像潜扩散模型（LDM）逐帧生成视频，又因缺乏时间建模而导致严重的帧间闪烁与不一致。本文提出**Video LDM**，核心思路是将视频生成解耦为空间内容生成与时间对齐两个子问题：首先在大规模图像数据上预训练空间层以获得高质量的图像生成能力，然后在空间层之间插入可学习的时间层（含时间注意力和3D卷积残差块），**固定空间层权重，仅训练时间层**，从而将图像生成器高效转化为时间一致的视频生成器。这一策略极大降低了视频训练的计算开销，且时间层可迁移至同一图像模型的不同变体（如DreamBooth个性化模型），实现个性化视频生成。

在真实驾驶场景（512×1024分辨率）上，Video LDM 的 FVD 为 356，显著优于 Long Video GAN 的 478（Table 1左）；用户研究中 62.03% 的参与者偏好 Video LDM 的生成结果（Table 2）。消融实验证实，端到端训练 LDM 的 FVD 恶化至 1155.10，而预训练固定空间层再训练时间层的策略将 FVD 降至 534.17（Table 1右）。此外，对解码器和上采样器进行视频微调分别将重建 FVD 从 390.88 降至 32.94、上采样 FVD 从 165.98 降至 45.39（Table 3），凸显时间对齐在视频生成全管线中的关键作用。

该方法在方法谱系上属于**潜空间视频扩散模型**，与 Make-A-Video（Singer et al., 2023）、Imagen Video（Ho et al., 2022）等同期工作共享“利用预训练图像模型生成视频”的思路，但 Video LDM 的独特贡献在于将时间建模完全隔离为可插拔的时间层，实现了图像模型向视频模型的最小代价迁移。



### 问题背景：高分辨率视频生成的困境

扩散模型（Diffusion Models, DMs）在图像合成领域取得了显著成功，将其扩展至视频生成是自然而然的下一步。然而，高分辨率视频扩散模型的训练面临一个根本性瓶颈：**计算成本极高**。视频数据的高维特性使得直接在像素空间训练扩散模型变得不切实际，而即使采用潜空间方法，从头训练一个具备时间建模能力的视频扩散模型也需消耗海量计算资源。

与此同时，预训练的大规模图像扩散模型已经展现了强大的单帧生成能力。一个直观的思路是直接使用这些图像模型逐帧生成视频——但这样做的结果是灾难性的：由于缺乏时间建模，不同帧之间完全独立，导致生成的视频出现严重的**帧间闪烁和不一致**，无法形成连贯的视频序列。

### 现有方法的缺口

在 Video LDM 提出之前，视频生成领域已有多项工作尝试解决上述问题：

- **Long Video GAN (LVG)**（Brooks et al., 2022）采用生成对抗网络进行长视频生成，但 GAN 类方法在高分辨率场景下的训练稳定性和生成多样性存在局限。
- **Make-A-Video**（Singer et al., 2023）、**Imagen Video**（Ho et al., 2022）等文本到视频扩散模型虽然展现了令人瞩目的结果，但它们通常需要从头或大规模联合训练空间和时间层，训练成本高昂，且难以直接复用现有图像扩散模型的强大先验。
- **CogVideo**（Hong et al., 2022）和 **MagicVideo**（Zhou et al., 2022）等潜空间视频扩散模型也面临类似的训练效率问题。

这些方法的共同缺口在于：**缺乏一种高效的方式，将预训练图像扩散模型的强大生成能力转化为时间一致的视频生成能力**，同时避免从头训练视频模型的巨大开销。

### 核心动机与洞察

Video LDM 的核心动机源于一个关键洞察：**大规模图像数据集上预训练的空间层已经学会了丰富的视觉先验，视频生成所需的额外能力本质上只是“将帧对齐”——即学习帧间的时间一致性**。这意味着，如果能够在预训练图像扩散模型的基础上，以最小的代价引入时间建模，就可以将成熟的图像生成器高效转化为视频生成器。

具体而言，这一洞察可以分解为以下因果链条：

1. **瓶颈定位**：视频生成的核心难点不在于空间建模（单帧质量），而在于时间建模（帧间一致性）。
2. **因果旋钮**：在预训练图像 LDM 的 U-Net 架构中，空间层之间插入可学习的时间层（时间注意力和 3D 卷积残差块），并**固定空间层权重，仅训练时间层**，即可将帧对齐问题转化为一个相对轻量的时间一致性学习任务。
3. **效率优势**：这一策略使得视频训练只需少量视频数据，极大降低了计算成本，同时完整保留了图像预训练模型的空间生成能力。更关键的是，训练好的时间层可以迁移至同一图像模型的不同变体（如 DreamBooth 个性化模型），实现个性化视频生成，而无需重新训练时间层。

这一“对齐潜变量”（Align your Latents）的思想，构成了 Video LDM 方法设计的理论基础。



## 核心方法与创新机理

Video LDM 的核心创新在于**将视频生成问题解耦为空间建模与时间建模两个可分离的子任务**，从而以极低的训练成本将预训练图像扩散模型转化为时间一致的视频生成器。其关键洞察是：大规模图像数据集上预训练的空间层已经具备强大的单帧生成能力，只需在冻结的空间层之间插入可学习的时间层，即可将帧对齐问题转化为纯粹的时间一致性学习任务。

### 方法层面的关键改变

| 改变维度 | 基线方法 | Video LDM 方案 | 证据锚点 |
|---------|---------|---------------|---------|
| **时间层** | 无（逐帧独立生成或从头训练 3D 模型） | 在空间层之间插入时间注意力和 3D 卷积残差块，使用可学习的合并参数 α | Sec. 3.1, Fig. 4 |
| **空间层训练策略** | 从头训练或与时间层联合训练 | 先在图像数据集上预训练并固定权重，然后仅训练时间层 | Sec. 3.1, Eq. (2) |
| **解码器** | 图像自编码器解码器（无时间感知） | 添加时间层并使用 3D 视频判别器对解码器进行视频微调 | Sec. 3.1.1, Fig. 3, Table 3 |
| **上采样器时间对齐** | 独立的逐帧图像上采样器 | 添加时间层并视频微调扩散上采样器，实现时间一致的超分辨率 | Sec. 3.4, Table 3 |
| **长视频生成机制** | 无（仅短序列生成） | 基于掩码条件的预测模型与分类器自由上下文引导，支持迭代长视频生成 | Sec. 3.2, Eq. (4) |

### 关键创新机制

**1. 预训练空间层的冻结与时间层的插入**

Video LDM 的核心公式揭示了其训练策略的本质差异。标准扩散模型优化所有参数 θ：

$$ \arg\min_{\theta} \mathbb{E}_{\mathbf{x}\sim p_{\mathrm{data}},\tau\sim p_{\tau},\epsilon\sim\mathcal{N}(\mathbf{0},I)}\left[\|\mathbf{y}-\mathbf{f}_{\theta}(\mathbf{x}_{\tau};\mathbf{c},\tau)\|_{2}^{2}\right] $$

而 Video LDM 将空间层参数 θ 固定，仅优化时间层参数 φ：

$$ \arg\min_{\phi} \mathbb{E}_{\mathbf{x}\sim p_{\mathrm{data}},\tau\sim p_{\tau},\epsilon\sim\mathcal{N}(\mathbf{0},I)}\left[\|\mathbf{y}-\mathbf{f}_{\theta,\phi}(\mathbf{z}_{\tau};\mathbf{c},\tau)\|_{2}^{2}\right] $$

这种设计使得训练仅需少量视频数据，且时间层可迁移至同一图像模型的不同变体（如 DreamBooth 微调版本），实现个性化视频生成。

**2. 视频微调解码器**

图像自编码器的解码器缺乏时间感知能力，即使潜在表示已时间对齐，逐帧解码仍会引入闪烁。Video LDM 在解码器中插入时间层，并使用基于 3D 卷积的 patch-wise 时间判别器进行视频微调。消融实验表明，这一步骤将重建 FVD 从 390.88 降至 32.94（Table 3 right），降低一个数量级以上。

**3. 时间对齐的上采样器**

类似地，将标准的图像扩散上采样器添加时间层并进行视频微调，FVD 从 165.98 降至 45.39（Table 3 left），证明时间对齐在超分辨率阶段同样至关重要。

**4. 长视频生成的掩码条件机制**

通过引入时间二值掩码 m_S，预测模型可基于 S 帧上下文预测剩余 T-S 帧。采样时使用分类器自由上下文引导：

$$ \mathbf{f}_{\theta,\phi}^{\prime}(\mathbf{z}_{\tau};\mathbf{c}_{S}) = \mathbf{f}_{\theta,\phi}(\mathbf{z}_{\tau}) + s \cdot \left(\mathbf{f}_{\theta,\phi}(\mathbf{z}_{\tau};\mathbf{c}_{S}) - \mathbf{f}_{\theta,\phi}(\mathbf{z}_{\tau})\right) $$

其中 s ≥ 1 为引导尺度。这一机制使模型能够迭代生成任意长度的视频序列。

### 消融实验验证

消融实验严格验证了每个创新点的必要性（Table 1 right）：

- **端到端训练 LDM**（无图像预训练）导致 FVD 从 534.17 恶化至 1155.10，证明预训练空间层的必要性。
- **仅使用时间注意力**而缺少 3D 卷积时间层，FVD 升至 704.41，说明空间上下文条件对时间一致性的重要性。
- **像素空间基线**的视频微调策略 FVD 为 639.56，显著劣于潜空间的 534.17，验证了在潜空间操作的优势。
- **解码器微调时仅使用视频判别器**优于同时使用图像判别器（FVD 32.94 vs 51.01，Table 14），额外图像判别器反而损害时间一致性。



Video LDM 的整体 pipeline 遵循“编码—时序生成—解码—可选上采样”的级联架构，各模块分工明确且输入输出流清晰。其核心设计原则是**最大化复用预训练图像模型的空间建模能力，仅在必要时引入可学习的时间层**，从而将图像生成器高效转化为时间一致的视频生成器。

### Pipeline 总览

如 Figure 5 所示，完整生成流程包含四个串行阶段：

1. **关键帧生成（Key Frame Generation）**：由文本提示或无条件噪声出发，通过插入时间层的潜在扩散模型在压缩潜在空间生成稀疏关键帧序列。
2. **时序插值（Temporal Interpolation）**：基于掩码条件训练的插值模型在关键帧之间填充中间帧，分两步将帧率从 $T$ 提升至 $4T$ 再至 $16T$。
3. **视频解码（Video Decoding）**：经视频微调的时序感知解码器将潜在表示重建为像素空间视频。
4. **可选上采样（Video Upsampling）**：若需更高分辨率，由同样插入时间层并视频微调的扩散超分辨率模型进行时序一致的空间上采样。

### 模块职责与数据流

| 模块 | 输入 | 输出 | 训练状态 |
|------|------|------|----------|
| 图像编码器 (Encoder) | 原始视频帧序列 | 逐帧独立的潜在表示 $\mathbf{z}$ | 冻结 |
| 空间层 (Spatial Layers) | 扩散加噪后的潜在序列 $\mathbf{z}_\tau$ | 去噪后的潜在序列 | 冻结（图像预训练权重） |
| 时间层 (Temporal Layers) | 经空间层处理的特征图 | 注入时序一致性的特征图 | **唯一可训练部分** |
| 视频微调解码器 (Decoder) | 去噪后的潜在序列 | 时序一致的像素视频 | 视频微调 |
| 时序插值模型 | 稀疏关键帧潜在表示 + 掩码条件 | 插值后的密集帧序列 | 独立训练 |
| 视频上采样器 | 低分辨率视频帧 + 噪声增强条件 | 高分辨率时序一致视频 | 视频微调 |

### 关键设计：空间层与时间层的解耦

这是整个框架的**核心因果机制**。如 Figure 4 所示，预训练图像 LDM 的空间层 $l_\theta^i$ 将输入视频序列的时序轴重排到 batch 维度，从而将视频视为“一批独立图像”进行处理。时间层 $l_\phi^i$ 则被插入到空间层之间：

$$
\mathbf{z}^{\prime} \leftarrow \mathrm{rearrange}(\mathbf{z}, \mathrm{(b\ t)\ c\ h\ w \to b\ c\ t\ h\ w})
$$
$$
\mathbf{z}^{\prime} \leftarrow l_{\phi}^{i}(\mathbf{z}^{\prime}, \mathbf{c})
$$
$$
\mathbf{z}^{\prime} \leftarrow \mathrm{rearrange}(\mathbf{z}^{\prime}, \mathrm{b\ c\ t\ h\ w \to (b\ t)\ c\ h\ w})
$$

训练时仅优化时间层参数 $\phi$，空间层 $\theta$ 保持冻结：

$$
\arg\min_{\phi} \mathbb{E}_{\mathbf{x}\sim p_{\mathrm{data}},\tau\sim p_{\tau},\epsilon\sim\mathcal{N}(\mathbf{0},I)}\left[\|\mathbf{y}-\mathbf{f}_{\theta,\phi}(\mathbf{z}_{\tau};\mathbf{c},\tau)\|_{2}^{2}\right]
$$

这种解耦带来了两个关键优势：
- **训练效率**：仅需少量视频数据训练时间层，空间层从大规模图像数据继承强大的视觉先验。
- **迁移能力**：时间层可迁移至同一图像模型的不同变体（如 DreamBooth 微调版本），实现个性化视频生成（见 Figure 8）。

### 解码器与时序对齐

图像编码器对视频帧独立编码，若直接使用图像解码器逐帧解码，会导致严重的帧间闪烁。Video LDM 在解码器中同样插入时间层，并使用基于 3D 卷积的 patch-wise 时序判别器进行视频微调（Figure 3）。消融实验表明，这一步骤将重建 FVD 从 390.88 降至 32.94（Table 3 right），降低一个数量级以上，是保证时序一致性的**必要条件**。

### 长视频生成的预测与引导机制

对于超出单次生成窗口的长视频，Video LDM 采用基于掩码条件的预测模型。给定 $S$ 帧上下文，模型预测后续 $T-S$ 帧：

$$
\mathbb{E}_{\mathbf{x}\sim p_{\mathrm{data}},\mathbf{m}_{S}\sim p_{S},\tau\sim p_{\tau},\epsilon}\left[\|\mathbf{y}-\mathbf{f}_{\theta,\phi}(\mathbf{z}_{\tau};\mathbf{c}_{S},\mathbf{c},\tau)\|_{2}^{2}\right]
$$

采样时使用分类器自由上下文引导增强条件控制：

$$
\mathbf{f}_{\theta,\phi}^{\prime}(\mathbf{z}_{\tau};\mathbf{c}_{S}) = \mathbf{f}_{\theta,\phi}(\mathbf{z}_{\tau}) + s \cdot \left(\mathbf{f}_{\theta,\phi}(\mathbf{z}_{\tau};\mathbf{c}_{S}) - \mathbf{f}_{\theta,\phi}(\mathbf{z}_{\tau})\right)
$$

其中 $s \geq 1$ 为引导尺度。这一机制支持迭代式长视频生成，但论文也指出卷积时间生成方法在超长视频上可能出现质量下降，稳健的长视频生成仍是待解决问题。



### 总体架构：从图像 LDM 到视频 LDM

Video LDM 的核心思想是将预训练的图像潜扩散模型（LDM）转化为时间一致的视频生成器，而非从头训练视频扩散模型。整个管线由以下关键模块构成（Fig. 5）：

1. **图像编码器 (Encoder)**：将视频的每一帧独立映射到低维潜在空间，权重固定不变。编码器在图像数据上预训练，仅处理空间信息。
2. **潜在空间扩散模型 (Spatial Layers)**：基于预训练图像 LDM 的 U-Net 空间层，负责在潜在空间进行去噪建模。这些层将输入视频序列的时间轴移入 batch 维度，将视频视为一批独立图像处理，权重完全固定。
3. **时间层 (Temporal Layers)**：插入 U-Net 空间层之间的可学习时间模块，包含时间注意力层和 3D 卷积残差块。这是整个模型中唯一需要训练的部分。
4. **视频微调解码器 (Video-Finetuned Decoder)**：将潜在表示解码为像素视频，通过添加时间层并使用 3D 视频判别器进行视频微调，确保解码输出的时间一致性。
5. **时间插值模型 (Temporal Interpolation Model)**：基于掩码条件机制，在关键帧之间进行帧插值以提升帧率。
6. **视频上采样器 (Video Upsampler)**：对低分辨率视频进行时间一致的超分辨率，基于扩散超分辨率模型并添加时间层进行视频微调。

### 关键模块详解

#### 时间层的插入与训练策略

时间层是 Video LDM 最核心的创新模块。其设计遵循一个关键原则：**空间层处理内容，时间层处理运动**。

具体实现中，时间层 $l_{\phi}^{i}$ 被插入到预训练空间层 $l_{\theta}^{i}$ 之间。对于每个时间混合层，执行以下维度变换：

$$
\begin{aligned}
\mathbf{z}^{\prime} &\leftarrow \mathrm{rearrange}(\mathbf{z}, \mathrm{(b\ t)\ c\ h\ w \to b\ c\ t\ h\ w}) \\
\mathbf{z}^{\prime} &\leftarrow l_{\phi}^{i}(\mathbf{z}^{\prime}, \mathbf{c}) \\
\mathbf{z}^{\prime} &\leftarrow \mathrm{rearrange}(\mathbf{z}^{\prime}, \mathrm{b\ c\ t\ h\ w \to (b\ t)\ c\ h\ w})
\end{aligned}
$$

其中 $b$ 为 batch 大小，$t$ 为视频帧数。空间层将时间轴移入 batch 维度后，每帧被独立处理；时间层则将数据恢复为视频格式，通过时间注意力和 3D 卷积学习帧间一致性。

时间层的具体组成包括：
- **时间注意力层**：在时间维度上执行自注意力，捕获长程帧间依赖。
- **3D 卷积残差块**：在时空维度上执行局部卷积，提供空间上下文条件。

消融实验（Table 1 right）表明，仅使用时间注意力而缺少 3D 卷积时间层会导致 FVD 从 534.17 升高至 704.41，验证了空间上下文条件的重要性。

#### 视频微调解码器

标准图像自编码器的解码器独立处理每一帧，导致重建视频出现严重的时间闪烁。Video LDM 对解码器进行视频微调（Fig. 3）：

- 在解码器中插入时间层（与 LDM 中的时间层设计一致）。
- 固定编码器权重，仅微调解码器的时间层和部分参数。
- 使用基于 3D 卷积的 patch-wise 时间判别器进行对抗训练。

消融实验（Table 3 right）显示，视频微调解码器将重建 FVD 从 390.88 降至 32.94，降低一个数量级以上。进一步消融（Table 14）表明，微调时仅使用视频判别器优于同时使用图像判别器（FVD 32.94 vs 51.01），额外的图像判别器反而损害了时间一致性。

#### 长视频生成：预测模型与掩码条件

为实现长视频生成，Video LDM 引入基于掩码条件的预测模型。给定 $S$ 帧上下文，模型需要预测剩余 $T-S$ 帧。

训练时引入时间二值掩码 $\mathbf{m}_S$，掩码掉需要预测的帧。条件 $\mathbf{c}_S$ 由掩码 $\mathbf{m}_S$ 与掩码后的编码帧组合而成，为模型提供上下文信息。

采样时采用分类器自由上下文引导：

$$
\mathbf{f}_{\theta,\phi}^{\prime}(\mathbf{z}_{\tau}; \mathbf{c}_{S}) = \mathbf{f}_{\theta,\phi}(\mathbf{z}_{\tau}) + s \cdot \left(\mathbf{f}_{\theta,\phi}(\mathbf{z}_{\tau}; \mathbf{c}_{S}) - \mathbf{f}_{\theta,\phi}(\mathbf{z}_{\tau})\right)
$$

其中 $s \geq 1$ 为引导尺度。消融实验（Table 1 right）表明上下文引导能进一步降低 FVD，但会轻微牺牲 FID，体现了时间一致性与单帧图像质量的权衡。

#### 时间插值模型

时间插值模型使用与预测模型相同的掩码条件机制（Sec. 3.2），但掩码的是需要插值的中间帧。模型同时训练在 $T \to 4T$ 和 $4T \to 16T$ 两种帧率提升模式下，通过二值条件指定当前任务。这种统一训练策略使单个模型能够处理多级帧率提升。

### 核心公式汇总

**公式 1：扩散模型标准去噪目标（图像 LDM 预训练）**

$$
\mathbb{E}_{\mathbf{x}\sim p_{\mathrm{data}},\tau\sim p_{\tau},\epsilon\sim\mathcal{N}(\mathbf{0},I)}\left[\|\mathbf{y}-\mathbf{f}_{\theta}(\mathbf{x}_{\tau};\mathbf{c},\tau)\|_{2}^{2}\right]
$$

其中 $\mathbf{y}$ 为噪声 $\epsilon$ 或 $\mathbf{v} = \alpha_{\tau}\epsilon - \sigma_{\tau}\mathbf{x}$（v-prediction 参数化），$\mathbf{c}$ 为可选条件（如文本嵌入）。

**公式 2：Video LDM 训练目标（固定空间层，仅训练时间层）**

$$
\arg\min_{\phi} \mathbb{E}_{\mathbf{x}\sim p_{\mathrm{data}},\tau\sim p_{\tau},\epsilon\sim\mathcal{N}(\mathbf{0},I)}\left[\|\mathbf{y}-\mathbf{f}_{\theta,\phi}(\mathbf{z}_{\tau};\mathbf{c},\tau)\|_{2}^{2}\right]
$$

核心区别：空间层参数 $\theta$ 固定（预训练权重），仅优化时间层参数 $\phi$。$\mathbf{z}_{\tau}$ 为视频编码后的扩散潜表示。

**公式 3：预测模型目标（含掩码条件）**

$$
\mathbb{E}_{\mathbf{x}\sim p_{\mathrm{data}},\mathbf{m}_{S}\sim p_{S},\tau\sim p_{\tau},\epsilon}\left[\|\mathbf{y}-\mathbf{f}_{\theta,\phi}(\mathbf{z}_{\tau};\mathbf{c}_{S},\mathbf{c},\tau)\|_{2}^{2}\right]
$$

$\mathbf{c}_S$ 为掩码条件，由掩码 $\mathbf{m}_S$ 和掩码后编码帧组合而成。

**公式 5：视频超分辨率训练目标**

$$
\mathbb{E}_{\mathbf{x}\sim p_{\mathrm{data}},(\tau,\tau_{\gamma})\sim p_{\tau},\epsilon\sim\mathcal{N}(\mathbf{0},I)}\left[\|\mathbf{y}-\mathbf{g}_{\theta,\phi}(\mathbf{x}_{\tau};\mathbf{c}_{\tau_{\gamma}},\tau_{\gamma},\tau)\|_{2}^{2}\right]
$$

$\mathbf{c}_{\tau_{\gamma}}$ 为经噪声增强后的低分辨率条件帧，$\tau_{\gamma}$ 控制增强噪声水平（噪声增强策略用于提升超分辨率模型的鲁棒性）。

### 训练策略的核心消融验证

端到端训练 LDM（无图像预训练）导致 FVD 从 534.17 恶化至 1155.10（Table 1 right），证明了预训练空间层的必要性。像素空间基线的视频微调策略（FVD 639.56）也不如潜空间操作（FVD 534.17），验证了在潜空间进行时间对齐的优势。时间层训练对单帧图像质量影响轻微（FID 从 47.00 升至 48.26），说明视频微调几乎不损害图像生成能力。



## 实验与关键发现

### 核心实验设置

Video LDM 在三个数据集上进行验证：**Real Driving Scenes (RDS)**（683,060 个驾驶场景视频，512×1024 分辨率，最高 30 fps）、**WebVid-10M**（10.7M 视频-文本对，缩放至 320×512）、以及 **UCF-101** 和 **MSR-VTT** 用于零样本文本到视频评估。图像 LDM 基于 Rombach et al. 的架构，采用卷积编解码器和 U-Net 扩散主干，所有采样使用 DDIM。时间层包括时间注意力和 3D 卷积残差块，训练时空间层权重完全冻结。

---

### 主结果：驾驶场景视频生成

在 RDS 数据集上，Video LDM 显著优于同期工作 **Long Video GAN (LVG)**（Brooks et al., 2022）。如 Table 1（左）所示，无条件 Video LDM 的 FVD 为 389，加入上下文引导后进一步降至 **356**，对比 LVG 的 478，FVD 降低 **122 点**（降幅 25.5%）。FID 方面，Video LDM 为 51.9，略优于 LVG 的 53.5，表明单帧质量也有小幅提升。

![[assets/figures/papers/paper_list_l5_https_arxiv_org_abs_2304_08818/figures/009_Table_1.jpg]]
*Table 1: Left: Comparison with LVG on RDS; Right: Ablations*

用户研究（Table 2）进一步验证了感知质量优势：在无条件生成对比中，54.02% 的评估者偏好 Video LDM（vs LVG 31.65%）；加入条件引导后，偏好比例提升至 **62.03%**（vs LVG 31.65%），说明上下文引导不仅降低自动指标，也显著提升人类感知的真实感。

![[assets/figures/papers/paper_list_l5_https_arxiv_org_abs_2304_08818/figures/008_Table_2.jpg]]
*Table 2: User study on Driving Video Synthesis on RDS*

---

### 消融实验：预训练策略与架构选择

Table 1（右）的系统消融揭示了方法设计的几个关键因果节点：

| 消融变体 | FVD ↓ | 核心结论 |
|---------|-------|---------|
| **Video LDM（完整方案）** | 534.17 | 预训练空间层 + 时间层微调 |
| 端到端训练 LDM（无图像预训练） | 1155.10 | FVD 恶化 2.16 倍，证明图像预训练不可或缺 |
| 像素空间基线 + 时间微调 | 639.56 | 潜空间操作比像素空间 FVD 低 105.39，验证潜空间优势 |
| 仅时间注意力（无 3D 卷积） | 704.41 | FVD 升高 170.24，3D 卷积提供的空间上下文条件至关重要 |
| 无上下文引导 | 534.17 → 389（Table 1 左） | 上下文引导进一步降低 FVD，但会轻微牺牲 FID |

**端到端训练的失败模式**：当 LDM 从头开始在视频数据上联合训练空间层和时间层时，FVD 从 534.17 急剧恶化至 1155.10。这验证了核心洞察——大规模图像预训练提供的强空间先验是时间层高效学习的必要条件，缺乏该先验时模型无法在有限视频数据上同时学习空间质量和时间一致性。

**时间层设计的因果机制**：仅使用时间注意力而移除 3D 卷积残差块，FVD 从 534.17 升至 704.41。这表明单纯的时间注意力不足以建模帧间运动——3D 卷积在局部时空邻域内提供的空间上下文条件对时间对齐至关重要。

---

### 解码器与上采样器的时间微调

Table 3 展示了时间微调对解码器和上采样器的决定性影响：

![[assets/figures/papers/paper_list_l5_https_arxiv_org_abs_2304_08818/figures/010_Table_3.jpg]]
*Table 3: Left: Evaluating temporal fine-tuning for diffusion upsamplers on RDS data; Right: Video fine-tuning of the first stage decoder network leads to significantly improved consistency*

- **解码器微调**（Table 3 右）：图像解码器（无时间感知）重建视频的 FVD 高达 390.88；添加时间层并使用 3D 视频判别器微调后，重建 FVD 骤降至 **32.94**，降幅超过一个数量级（降低 91.6%）。这证明即使 LDM 在潜空间生成了时间一致的表示，若解码器缺乏时间感知，像素级输出仍会严重闪烁。

- **上采样器微调**（Table 3 左）：独立的逐帧图像上采样器 FVD 为 165.98；添加时间层并视频微调后降至 **45.39**，降低 120.59 点（降幅 72.7%）。这凸显了超分辨率阶段时间对齐的必要性——逐帧独立上采样会破坏潜空间已建立的时间一致性。

- **判别器设计**：Table 14 显示，解码器微调时仅使用视频判别器（FVD 32.94）优于同时使用图像判别器（FVD 51.01）。额外的图像判别器反而损害了时间一致性，说明视频微调阶段应专注于时间目标，避免图像质量约束干扰时间对齐学习。

- **跨数据集泛化**：Table 11 验证了视频微调解码器在 WebVid 和 Mountain Biking 场景同样有效，重建 FVD 均大幅降低，证明该策略不限于特定数据分布。

---

### 文本到视频生成

在 UCF-101 零样本文本到视频任务上，Video LDM 的 Inception Score 达到 **33.45**（Table 4/Table 9），略高于 **Make-A-Video**（Singer et al., 2023）的 33.00。在 MSR-VTT 上，CLIPSIM 为 0.2929（Table 5/Table 10），略低于 Make-A-Video 的 0.3049。考虑到 Video LDM 仅需在预训练图像模型上微调时间层（训练参数量远少于从头训练的视频模型），这一竞争力表现验证了方法的参数效率优势。需注意不同模型使用不同预处理和提示工程，零样本对比不能视为完全公平。

![[assets/figures/papers/paper_list_l5_https_arxiv_org_abs_2304_08818/figures/012_Figure_8.jpg]]
*Figure 8: Left: DreamBooth Training Images. Top row: Video generated by our Video LDM with DreamBooth Image LDM backbone. Bottom row: Video generated without DreamBooth Image backbone. We see that the DreamBooth model preserves subject identity well. Table 4. UCF-101 text-to-video generation*

![[assets/figures/papers/paper_list_l5_https_arxiv_org_abs_2304_08818/figures/013_Table_5.jpg]]
*Table 5: MSR-VTT text-to-video generation performance*

---

### 关键图表结论汇总

- **Figure 4** 展示了时间层插入策略：空间层将视频视为独立图像批次（时间轴移入批次维度），时间层在视频维度上执行注意力和 3D 卷积，这种“空间层批处理 + 时间层视频处理”的交替机制是方法的核心架构创新。




- **Figure 5** 展示了完整的 Video LDM 管线：先生成稀疏关键帧，再通过时间插值模型（基于掩码条件训练）分两步提升帧率（T→4T→16T），最后经视频微调解码器和可选视频上采样器输出高分辨率时间一致视频。

- **Figure 8** 展示了 DreamBooth 个性化视频生成：将预训练时间层迁移至 DreamBooth 微调的图像模型，可在保留主体身份的同时生成时间一致视频，验证了时间层的模型迁移能力。

---

### FVD 指标的局限性

需注意 FVD 度量可能偏向时间平滑度而非真实感。在山地自行车数据集上，Video LDM 的 FVD 较高但人类评估更佳（Table 13），说明 FVD 与感知质量之间存在不一致。因此，本研究的综合评价始终结合人类评估，尤其在运动幅度较大的场景中，FVD 单独不足以反映生成质量。

![[assets/figures/papers/paper_list_l5_https_arxiv_org_abs_2304_08818/figures/023_Table_13.jpg]]
*Table 13: Comparison with Long Video GAN (LVG) on Mountain Biking videos (human evaluation on the right)*

### 补充图表

![[assets/figures/papers/paper_list_l5_https_arxiv_org_abs_2304_08818/figures/028_Figure_12.jpg]]
*Figure 12: Generated videos at resolution 512 × 512 (extended “convolutional in space”; see Appendix D). Captions from left to right are: “Aerial view over snow covered mountains”, “A fox wearing a red hat and a leather jacket dancing in the rain, high definition, 4k”, and “Milk dripping into a cup of coffee, high definition, 4k”. Frames are shown at 2 fps*

![[assets/figures/papers/paper_list_l5_https_arxiv_org_abs_2304_08818/figures/033_Figure_15.jpg]]
*Figure 15: Generated 30 second video of “a teddy bear walking down the road in the sunset, high definition, 4 $\mathrm { k } ^ { \prime \prime }$ at resolution 5 1 2 $\times$ 5 1 2 (extended “convolutional in space” and also “convolutional in time”; see Appendix D). Frames are shown at 1 fps

![[assets/figures/papers/paper_list_l5_https_arxiv_org_abs_2304_08818/figures/036_Figure_17.jpg]]
*Figure 17: Generated videos at resolution 1280 × 2048 using our Stable Diffusion 2.0-based model and including our video fine-tuned text-to-video latent upsampler. Captions from left to right are: “Burning firewood” and “An astronaut riding a horse, 4k, high definition”. Frames are shown at 2 fps*



## 定位与知识库关联

### 1. 核心方法定位

Video LDM 处于**图像扩散模型向视频生成的迁移范式**中，其核心操作不是从头设计视频模型，而是在预训练图像潜空间扩散模型（LDM）的空间层之间**插入可学习的时间层**，并固定空间层仅训练时间层。这一策略将视频生成问题转化为“学习帧间时间对齐”的任务，从而将大规模图像预训练的生成能力高效迁移至视频域。

该方法的技术谱系可拆解为三个层面：

- **上游继承**：空间层直接继承自图像 LDM（Rombach et al., 2022），包括基于 U-Net 的扩散架构和 DDIM 采样策略。编码器/解码器同样来自预训练图像自编码器。
- **核心创新**：时间层设计（时间注意力和 3D 卷积残差块）与“固定空间层、仅训练时间层”的优化策略，将帧对齐问题显式化为可学习模块。
- **下游扩展**：同一时间对齐思想被迁移到解码器视频微调和扩散上采样器视频微调，形成统一的时间一致性增强框架。

### 2. 与同期基线的对比关系

Video LDM 与同期视频生成方法存在明确的**范式差异**：

- **Long Video GAN (LVG)**（Brooks et al., 2022）：直接在高分辨率像素空间使用 GAN 进行长视频生成。Video LDM 在真实驾驶场景（RDS）上 FVD 显著优于 LVG（356 vs 478），用户偏好率也更高（62.03% vs 31.65%）。LVG 代表了像素空间 GAN 路线，Video LDM 则验证了潜空间扩散路线在时间一致性和高分辨率上的优势。
- **Make-A-Video**（Singer et al., 2023）：基于文本-图像模型扩展至视频，在 UCF-101 上 IS 得分与 Video LDM 接近（33.00 vs 33.45），但在 MSR-VTT 上 CLIPSIM 略高（0.3049 vs 0.2929）。两者共享“从图像到视频迁移”的思路，但 Video LDM 的独特贡献在于时间层的可迁移性——同一组时间层可应用于不同图像模型变体（如 DreamBooth 个性化模型）。
- **Imagen Video**（Ho et al., 2022）和 **CogVideo**（Hong et al., 2022）：代表大规模文本到视频路线，Video LDM 在模型规模上更为轻量，强调通过预训练复用降低计算成本。

### 3. 适用边界

Video LDM 的适用边界由以下条件定义：

- **数据依赖**：依赖大规模图像预训练（如 LAION-5B）和中等规模视频微调数据（如 WebVid-10M 的 10.7M 视频-文本对，或 RDS 的 68 万驾驶视频）。在缺乏高质量图像预训练基座的情况下，端到端训练 LDM 的 FVD 从 534.17 恶化至 1155.10，说明预训练空间层是该方法有效性的必要条件。
- **分辨率范围**：已验证从 320×512 到 1280×2048 的文本到视频生成，以及 512×1024 的真实驾驶场景生成。更高分辨率依赖级联式视频上采样器。
- **时长限制**：长视频生成依赖预测模型和上下文引导的迭代机制，但论文明确指出“对于非常长的视频会出现质量下降”，卷积时间生成方法存在稳定性边界。
- **内容域**：主要验证域为真实驾驶场景和通用 Web 视频，个性化生成需额外依赖 DreamBooth 微调，且时间层与 DreamBooth 空间层需使用不同的文本编码器，增加了工程复杂性。

### 4. 局限性与开放问题

#### 已确认的局限

1. **长视频稳定性**：卷积时间生成方法在超长视频上可能出现质量下降，文本到视频的稳健长视频生成仍需未来工作。
2. **帧率控制**：时间插值模型和预测模型需要人工设定帧率缩放步骤，无法自适应不同帧率需求。
3. **个性化生成复杂性**：时间层与 DreamBooth 微调的空间层需分别使用不同文本编码器，工程实现复杂。
4. **数据分布依赖**：训练数据主要来自真实驾驶场景和 WebVid-10M，泛化能力和生成多样性受限于训练数据分布。

#### 开放问题

1. **时间层的迁移边界**：预训练的时间层能迁移到多少种不同的图像模型变体？对其他微调方法（如 LoRA、Textual Inversion）的兼容性如何？这直接决定了该范式的生态扩展性。
2. **跨模态时间对齐**：能否将时间对齐策略扩展到音频或其他模态，实现多模态视频生成？这涉及潜空间对齐的跨模态泛化能力。
3. **评估体系缺陷**：FVD 等自动评估指标与人类感知的真实感之间存在不一致（例如在山地自行车数据集上 FVD 较高但人类评估更佳），应如何发展更可靠的视频生成评估体系？
4. **反向迁移潜力**：能否利用视频时间对齐思想反向改进图像模型，例如通过时间一致性约束提升单帧质量？这是一个尚未探索的逆向迁移方向。

### 5. 知识库定位总结

Video LDM 在视频生成知识库中的定位可以概括为：**以最小训练成本实现图像生成能力向视频域高效迁移的范式验证者**。其核心知识贡献不在于提出全新的生成架构，而在于证明了“时间层即插即用 + 空间层冻结”策略的有效性，以及时间对齐思想在解码器、上采样器等下游模块中的可迁移性。该方法为后续的视频扩散模型研究（如 Sora 等端到端视频生成模型）提供了重要的效率基线和模块化设计思路。



## 原文 PDF

![[paperPDFs/CVPR_2023/Align_your_Latents_High_Resolution_Video_Synthesis_with_Latent_Diffusion_Models.pdf]]
