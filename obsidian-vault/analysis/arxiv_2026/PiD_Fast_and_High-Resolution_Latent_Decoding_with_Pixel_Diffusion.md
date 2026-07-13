---
title: "PiD: Fast and High-Resolution Latent Decoding with Pixel Diffusion"
type: paper
paper_level: A
venue: arXiv
year: 2026
pdf_ref: paperPDFs/arxiv_2026/PiD_Fast_and_High-Resolution_Latent_Decoding_with_Pixel_Diffusion.pdf
project_link: "https://research.nvidia.com/labs/sil/projects/pid/"
code_link: null
aliases:
- PiD
tags:
- arxiv_2026
- topic/generative_models_diffusion
core_operator: 将潜码解码重新定义为条件像素扩散，利用预训练的像素扩散先验统一解码与上采样为一个生成模块，并通过噪声潜码条件化与sigma感知门控，使解码器既可以忠实重建也能合成新细节，同时支持部分去噪潜码的早期退出。
primary_logic: 像素空间扩散生成先验具备强大的高频细节合成能力，能够补偿自编码器重建损失和语义潜码的纹理缺失；在注入潜码时引入噪声扰动并依据噪声水平自适应调节注入强度，从而在潜码保真度与生成自由度之间实现动态平衡。
claims:
- PiD统一了解码和超分为单个条件像素扩散模型，直接在目标分辨率像素空间合成图像。
- 使用噪声潜码条件化和sigma感知门控，使解码器能够处理部分去噪的潜码，实现LDM早期终止。
- 在六个不同潜空间（FLUX.1、SD3、FLUX.2、Z-Image、DINOv2、SigLIP）上均取得最优NIQE、MUSIQ等无参考质量指标，且延迟约210ms，比扩散基超分基线快3-6倍。
- 消融实验表明，移除T2I先验导致MUSIQ从73.26骤降至59.52，移除sigma-aware gate则普遍恶化视觉质量。
---

# PiD: Fast and High-Resolution Latent Decoding with Pixel Diffusion

> [!tip] 核心洞察
> 像素空间扩散生成先验具备强大的高频细节合成能力，能够补偿自编码器重建损失和语义潜码的纹理缺失；在注入潜码时引入噪声扰动并依据噪声水平自适应调节注入强度，从而在潜码保真度与生成自由度之间实现动态平衡。

| 字段 | 内容 |
|------|------|
| 中文题名 | PiD：快速高分辨率像素扩散潜码解码 |
| 英文题名 | PiD: Fast and High-Resolution Latent Decoding with Pixel Diffusion |
| 会议/期刊 | arXiv 2026 |
| Links | [paper](https://arxiv.org/abs/2605.23902) · [Project](https://research.nvidia.com/labs/sil/projects/pid/) |
| Topic | #topic/generative_models_diffusion |
| Method | PiD |
| Dataset | DPG-Bench, FLUX.1 VAE (FLUX.1[dev]), 2048×2048 输出, DPG-Bench, SigLIP (Scale-RAE 2.8B), 2048×2048 输出 |

> [!tip] 效果简介
> - DPG-Bench, FLUX.1 VAE (FLUX.1[dev]), 2048×2048 输出 上，NIQE (越低越好) 3.50 vs 4.04 (SSDD + InvSR-1) (-0.54)；Latency (ms, torch.compile, GB200) 211.2 vs 1237.5 (VAE Dec. + SeedVR2-3B) (-1026.3 ms (约5.9倍加速))。
> - DPG-Bench, SigLIP (Scale-RAE 2.8B), 2048×2048 输出 上，MUSIQ (越高越好) 74.03 vs 73.68 (VAE Dec. + SeedVR2-3B) (+0.35)；Unipercept-IAA (越高越好) 64.94 vs 59.95 (VAE Dec. + SeedVR2-3B) (+4.99)。

## 概要

图像生成模型的主流范式依赖潜空间扩散模型（LDM）在压缩潜码上完成语义合成，再通过确定性解码器重建为像素图像。当目标分辨率超出原生输出时，需级联独立超分模型——这一“先解码、再上采样”的流水线面临两个深层瓶颈：

1. **重建导向解码器的信息天花板**：传统 VAE/RAE 解码器以最小化重建误差为目标训练，缺乏合成缺失高频细节的生成能力。对于语义潜码（如 DINOv2、SigLIP），纹理信息在编码阶段即被丢弃，确定性解码器无法补偿。
2. **级联超分的延迟与内存代价**：扩散基超分模型虽能补充细节，但多步采样带来显著延迟（如一步扩散超分基线约 1.2 秒），且解码与超分两阶段各自占用显存，限制了高分辨率输出的实用性。

PiD（Pixel Diffusion Decoder）将潜码解码重新定义为**条件像素扩散生成**，用一个统一的生成模块同时完成解码与上采样。其核心机制是：利用预训练的像素空间文本条件扩散先验（PixelDiT）作为高频细节合成的生成引擎，通过噪声潜码条件化与 sigma 感知门控注入潜码信息，在潜码保真度与生成自由度之间实现动态平衡。

**关键结论**：

- PiD 在六个不同潜空间（FLUX.1、SD3、FLUX.2、Z-Image、DINOv2、SigLIP）上均取得最优无参考质量指标，NIQE 从级联基线的 4.04 降至 3.50（FLUX.1 VAE），MUSIQ 在 SigLIP 潜空间达到 74.03。
- 延迟约 210 ms（GB200 GPU，torch.compile），比扩散基一步超分基线快 3–6 倍；在消费级 RTX 5090 上解码 2048×2048 图像仅需不到 1 秒，峰值显存 13 GB。
- 消融实验证实：移除 T2I 先验导致 MUSIQ 从 73.26 骤降至 59.52；移除 sigma 感知门控则普遍恶化视觉质量。
- 蒸馏后的 4 步学生模型在生成场景下甚至超越 50 步教师模型（MUSIQ 73.26 vs 71.79），验证了 DMD2 蒸馏的有效性。

**方法定位**：PiD 属于**生成式潜码解码器**，区别于传统的确定性重建解码器和级联超分流水线。它利用像素扩散先验的生成能力补偿潜码压缩损失，同时通过噪声条件化训练使解码器对部分去噪潜码具有鲁棒性，支持 LDM 早期终止以进一步降低端到端延迟。

### 潜码解码的瓶颈：从重建到生成

现代文本到图像（T2I）生成系统普遍采用“潜空间扩散模型（LDM）+ 潜码解码器”的两阶段架构：LDM 在压缩潜空间中执行迭代去噪，生成低分辨率潜码 $\mathbf{z} \in \mathbb{R}^{C \times H \times W}$；随后由解码器 $\mathcal{D}$ 将潜码映射回像素空间，得到图像 $\mathbf{x}_{\text{dec}} = \mathcal{D}(\mathbf{z})$。当目标输出分辨率高于潜码分辨率时，传统流水线还需级联一个独立的上采样/超分模块 $\mathcal{U}_s$，形成“解码-后上采样”级联：

$$\hat{\mathbf{x}}_0 = \mathcal{U}_s(\mathbf{x}_{\text{dec}}) \in \mathbb{R}^{3 \times (sH) \times (sW)}$$

这一范式存在两个根本性缺陷：

1. **解码器是重建导向的，不具备生成能力。** 主流 VAE/RAE 解码器（如 FLUX.1 VAE、SD3 VAE）在训练时仅优化像素级重建损失，其逆映射本质上是确定性的。当潜码因有损压缩而丢失高频纹理信息时，解码器无法“想象”缺失的细节，只能输出模糊的近似结果。这一问题在语义潜码（如 DINOv2、SigLIP 特征经 Scale-RAE 编码）场景下尤为突出——语义编码器天然舍弃了纹理级信息，传统解码器的输出严重缺乏视觉细节。

2. **级联超分流水线引入冗余延迟与内存开销。** 解码与超分被割裂为两个独立模块，中间需生成并存储低分辨率中间图像，再送入超分模型。扩散基超分方法（如 SeedVR2-3B、TSD-SR）虽能补充细节，但推理步数多、显存占用高；GAN 基超分（如 Real-ESRGAN）速度快但生成能力有限，且易引入伪影。级联架构使得端到端延迟成为两个模块之和，难以在高分辨率场景下实现实时或近实时解码。

### 像素扩散先验的未利用潜力

与此同时，像素空间扩散模型在高分辨率图像生成上展现了强大的高频细节合成能力。以 PixelDiT 为代表的像素扩散骨干网络，通过在原始像素空间建模速度场 $\mathbf{v}(\mathbf{x}_t, t, c)$，能够生成 2K 乃至 4K 分辨率、纹理丰富的图像。这一能力恰好可以弥补自编码器重建损失和语义潜码的纹理缺失。

然而，直接将像素扩散模型作为独立生成器使用，无法利用 LDM 已产生的潜码信息——潜码中蕴含的语义布局和全局结构被完全丢弃，造成计算浪费。问题的关键转化为：**如何将像素扩散的生成先验与潜码的条件信息有效融合，使解码器既能忠实于潜码的语义内容，又能自主合成高频细节？**

### 核心挑战：保真度与生成自由度的平衡

将潜码注入像素扩散过程面临一个核心张力：注入强度过高，解码器过度依赖潜码，退化为重建模型，丧失细节合成能力；注入强度过低，生成结果可能偏离潜码指定的语义内容，出现内容漂移。此外，LDM 在推理时通常执行固定步数的去噪，但不同步数下潜码的“完成度”不同——早期步的潜码噪声较大、结构尚不清晰，需要解码器更强的生成能力；后期步的潜码已接近收敛，解码器应更忠实地保留其内容。

现有工作对此缺乏系统性的解决方案。级联超分方法将解码与超分解耦，无法动态调节潜码保真度与生成自由度；潜空间直接上采样方法（如 LUA）仅在潜空间操作，受限于潜码本身的表达能力；SSDD 等方法虽改进了解码器架构，但仍是重建导向的，未引入生成先验。

### PiD 的动机与设计思路

PiD 的核心动机即源于上述分析：**将潜码解码重新定义为条件像素扩散，利用预训练的像素扩散先验统一解码与上采样为一个生成模块**。具体而言，PiD 在像素扩散骨干中注入噪声扰动的潜码，并通过 sigma 感知门控机制根据潜码的噪声水平自适应调节注入强度——噪声越大，注入越弱，给予生成先验更大的自由度；噪声越小，注入越强，更忠实地保留潜码内容。这一设计使得解码器既能处理完全去噪的干净潜码（重建模式），也能处理部分去噪的中间潜码（生成模式），甚至支持 LDM 早期终止以换取更低的推理延迟。

通过将解码与上采样统一为单个条件扩散模型，PiD 消除了级联流水线的中间瓶颈，在 2048×2048 分辨率下实现约 210ms 的解码延迟（GB200 GPU，torch.compile），比扩散基超分基线快 3–6 倍，同时在多个无参考质量指标上达到最优。

## 核心方法与创新机理

PiD 的核心创新在于将潜码解码从**确定性重建**范式彻底转向**条件生成**范式，并通过三个关键设计实现解码质量、效率与灵活性的同步提升。

### 范式转变：从重建解码到生成解码

传统潜码解码器（如 VAE/RAE 解码器）本质上是编码器的逆映射，其优化目标是最小化重建误差。这一范式存在根本性瓶颈：解码器只能恢复编码时保留的信息，无法合成编码过程中丢失的高频纹理细节。在语义潜码（如 DINOv2、SigLIP）场景下，这一问题尤为严重——语义编码器本就不保留纹理信息，导致解码结果模糊。现有方案通过级联超分模型（如 Real-ESRGAN、SeedVR2-3B、TSD-SR 等）来补偿细节，但这引入了额外的延迟和内存开销。

PiD 将解码问题重新定义为条件像素扩散：

$$\hat{\mathbf{x}}_0 \sim p_{\theta}^{(s)}(\mathbf{x}_0 \mid \mathbf{z}, c)$$

其中 $\mathbf{z}$ 为潜码，$c$ 为文本条件，$s$ 为上采样倍数。模型直接从潜码生成目标分辨率的像素空间图像，将解码与上采样统一为单个生成模块。这一转变的因果机制在于：**像素扩散先验具备强大的高频细节合成能力**，能够补偿自编码器的信息损失和语义潜码的纹理缺失。

### 噪声潜码条件化与 Sigma 感知门控

为支持 LDM 早期退出（即不完全去噪即可解码），PiD 引入噪声潜码条件化机制。训练时向潜码注入可变噪声：

$$\tilde{\mathbf{z}}_\sigma = (1-\sigma) \mathbf{z} + \sigma \xi, \quad \xi \sim \mathcal{N}(0, I), \quad \sigma \sim \mathcal{U}(0, \sigma_{\max})$$

这使得解码器学会处理从完全干净到高度噪声化的潜码。注入方式采用 ControlNet 风格的路径：将噪声潜码通过卷积投影为 Patch Token，再逐元素注入 DiT 隐状态：

$$\mathbf{h}_i \leftarrow \mathbf{h}_i + g_i(\mathbf{h}_i, \mathbf{l}_i, \sigma) \odot \mathbf{l}_i$$

关键设计在于 **Sigma 感知门控** $g_i$：

$$g_i(\mathbf{h}_i, \mathbf{l}_i, \sigma) = \mathrm{sigmoid}(\mathrm{Linear}_i([\mathbf{h}_i, \mathbf{l}_i]) - \alpha\sigma)$$

门控值由内容相关项和负偏置 $\alpha\sigma$ 共同决定：**潜码噪声越大（$\sigma$ 越高），注入强度越弱**，解码器更多地依赖自身的生成先验来补全细节。这实现了潜码保真度与生成自由度之间的动态平衡——当潜码干净时忠实重建，当潜码部分去噪时自主合成。

### 蒸馏驱动的极低步数推理

PiD 采用 DMD2 将多步教师模型蒸馏为 4 步学生模型，同时将 CFG 蒸馏进模型权重，消除了推理时的双倍计算。消融实验（Table 2）揭示了一个反直觉现象：在生成场景下，4 步学生模型的 MUSIQ 达到 73.26，反而超过 50 步教师模型的 71.79。这表明蒸馏过程不仅压缩了推理步数，还避免了教师模型在高步数下的过度信噪问题。

### 与基线的结构差异总结

| 设计维度 | 传统级联方案 | PiD |
|---------|------------|-----|
| 解码架构 | 卷积 VAE/RAE 确定性重建 | 像素扩散生成模型 |
| 上采样策略 | 解码 + 独立超分两步 | 解码与上采样统一 |
| 潜码注入 | 无噪声扰动 | 噪声化潜码 + sigma 感知门控 |
| 推理效率 | 多步扩散采样（如 50 步） | DMD2 蒸馏至 4 步 |

消融实验验证了各设计的必要性：移除 T2I 先验（即从头训练像素扩散解码器）导致 MUSIQ 从 73.26 骤降至 59.52，NIQE 从 3.50 升至 7.79（Table 4），证明预训练像素扩散先验是质量的核心保障；移除 sigma 感知门控则导致所有无参考指标恶化，尤其在高噪声潜码条件下重建质量显著下降。

PiD 将潜码解码重新定义为**条件像素扩散生成任务**，用一个端到端的生成模块同时完成解码与上采样，取代传统的“解码—超分”级联流水线。图 3 给出了整体架构。

### 输入与输出

PiD 的输入包括两部分：
- **潜码** $\mathbf{z} \in \mathbb{R}^{C \times H \times W}$：来自 VAE 编码器或视觉编码器（如 DINOv2、SigLIP）的低分辨率潜表示。
- **文本条件** $c$：来自基础 LDM 的文本嵌入，用于指导生成内容。

输出为直接合成的高分辨率图像 $\hat{\mathbf{x}}_0 \in \mathbb{R}^{3 \times (sH) \times (sW)}$，其中 $s$ 为空间上采样倍率。PiD 直接建模目标分辨率的图像分布：

$$\hat{\mathbf{x}}_0 \sim p_{\theta}^{(s)}(\mathbf{x}_0 \mid \mathbf{z}, c)$$

### 核心模块与数据流

PiD 的流水线由以下模块串联构成：

1. **像素扩散骨干（PixelDiT）**：采用 MMDiT 架构的像素空间扩散 Transformer，提供高分辨率文本条件生成先验。该骨干在像素空间直接建模速度场，支持 2K/4K 输出。

2. **噪声潜码条件化**：训练时，干净的潜码 $\mathbf{z}$ 被注入可变噪声，生成噪声潜码 $\tilde{\mathbf{z}}_\sigma$：
   $$\tilde{\mathbf{z}}_\sigma = (1-\sigma) \mathbf{z} + \sigma \xi, \quad \xi \sim \mathcal{N}(0, I)$$
   噪声水平 $\sigma \sim \mathcal{U}(0, \sigma_{\max})$，$\sigma_{\max}=0.8$。这使得解码器学会处理部分去噪的潜码，是实现 LDM 早期退出的关键。

3. **潜码投影与注入模块**：噪声潜码 $\tilde{\mathbf{z}}_\sigma$ 通过卷积路径投影为与像素 Patch Token 维度对齐的潜码令牌 $\mathbf{l}_i$，并以类似 ControlNet 的方式注入 DiT 各层的隐状态 $\mathbf{h}_i$：
   $$\mathbf{h}_i \leftarrow \mathbf{h}_i + g_i(\mathbf{h}_i, \mathbf{l}_i, \sigma) \odot \mathbf{l}_i$$

4. **Sigma 感知门控**：注入强度 $g_i$ 由内容相关项和噪声水平偏置共同决定：
   $$g_i(\mathbf{h}_i, \mathbf{l}_i, \sigma) = \mathrm{sigmoid}(\mathrm{Linear}_i([\mathbf{h}_i, \mathbf{l}_i]) - \alpha\sigma)$$
   其中 $\alpha$ 为可学习标量。噪声 $\sigma$ 越大，注入强度越弱，实现**保真度与生成自由度的动态平衡**：当潜码干净时（$\sigma \approx 0$），解码器忠实重建；当潜码含噪时（$\sigma$ 较大），解码器信任像素扩散先验来合成缺失细节。

5. **DMD2 蒸馏**：将多步教师模型蒸馏为 4 步学生模型，同时将分类器自由引导（CFG）蒸馏进模型权重，消除推理时的额外 CFG 计算开销。

### 训练与推理流程

训练阶段，PiD 从预训练的 PixelDiT 初始化，联合微调扩散骨干和潜码注入模块，优化目标为噪声潜码条件化的整流流损失：

$$\mathcal{L}_{\mathrm{FM}} = \mathbb{E}\left[\|\mathbf{v}_{\theta}(\mathbf{x}_t, t, c, \tilde{\mathbf{z}}_\sigma, \sigma) - (\mathbf{x}_0 - \epsilon)\|_2^2\right]$$

推理时，PiD 以 4 步采样从潜码直接生成高分辨率图像。得益于噪声潜码条件化训练，PiD 支持**早期退出**：基础 LDM 无需运行完整去噪步数，PiD 可直接从部分去噪的潜码合成高质量高分辨率结果，从而大幅降低端到端延迟。

![[assets/figures/papers/paper_list_l13_https_arxiv_org_abs_2605_23902/figures/003_Figure_3.jpg]]
*Figure 3: Overview of PiD. PiD unifies latent decoding and upsampling as a single latent-conditioned pixel diffusion model that predicts the target-resolution pixel-space velocity field. Noise-corrupted latent training and sigma-aware gating make the decoder robust to partially denoised latents, enabling early exit from the base LDM while preserving high-resolution output quality*

PiD 将潜码解码重新定义为**条件像素扩散**，其核心架构由四个关键模块构成，共同实现从低分辨率潜码到高分辨率像素图像的一步生成。

### 3.1 问题重定义：从级联解码到统一像素扩散

传统解码-超分流水线分两步执行：先将潜码 $\mathbf{z} \in \mathbb{R}^{C \times H \times W}$ 解码为低分辨率图像 $\mathbf{x}_{\text{dec}}$，再通过独立的超分模型 $\mathcal{U}_s$ 上采样 $s$ 倍：

$$\hat{\mathbf{x}}_0 = \mathcal{U}_s(\mathbf{x}_{\text{dec}}) \in \mathbb{R}^{3 \times (sH) \times (sW)}$$

PiD 直接建模目标分辨率图像的条件分布，将解码与上采样统一为单个生成模块：

$$\hat{\mathbf{x}}_0 \sim p_{\theta}^{(s)}(\mathbf{x}_0 \mid \mathbf{z}, c), \quad \mathbf{x}_0 \in \mathbb{R}^{3 \times (sH) \times (sW)}$$

其中 $c$ 为文本条件，$s$ 为上采样倍率。这一重定义的关键在于：像素扩散先验具备合成高频细节的生成能力，能够补偿自编码器重建损失和语义潜码的纹理缺失。

### 3.2 噪声潜码条件化与 Sigma 感知门控

**噪声潜码条件化** 是 PiD 支持 LDM 早期退出的核心机制。训练时，向潜码注入可变强度的高斯噪声：

$$\tilde{\mathbf{z}}_\sigma = (1-\sigma) \mathbf{z} + \sigma \xi, \quad \xi \sim \mathcal{N}(0, I), \quad \sigma \sim \mathcal{U}(0, \sigma_{\text{max}})$$

其中 $\sigma \in [0, 0.8]$ 控制噪声水平。当 $\sigma=0$ 时，解码器接收干净潜码，执行忠实重建；当 $\sigma>0$ 时，解码器需从部分损坏的潜码中"想象"缺失细节，从而实现生成式解码。

**潜码注入** 通过卷积投影路径将噪声潜码映射到图像 Patch Token 空间，并以 ControlNet 方式注入 PixelDiT 的各层：

$$\mathbf{h}_i \leftarrow \mathbf{h}_i + g_i(\mathbf{h}_i, \mathbf{l}_i, \sigma) \odot \mathbf{l}_i$$

其中 $\mathbf{h}_i$ 为 DiT 第 $i$ 层的隐状态，$\mathbf{l}_i$ 为投影后的潜码令牌。

**Sigma 感知门控** 根据噪声水平自适应调节注入强度，实现潜码保真度与生成自由度之间的动态平衡：

$$g_i(\mathbf{h}_i, \mathbf{l}_i, \sigma) = \text{sigmoid}(\text{Linear}_i([\mathbf{h}_i, \mathbf{l}_i]) - \alpha\sigma)$$

门控值由两部分决定：内容相关项 $\text{Linear}_i([\mathbf{h}_i, \mathbf{l}_i])$ 和负偏置项 $-\alpha\sigma$（$\alpha$ 为可学习标量）。当 $\sigma$ 增大（潜码噪声增强）时，sigmoid 输入减小，注入强度降低，解码器更多依赖像素扩散先验的生成能力；当 $\sigma$ 趋近于 0 时，注入强度最大，解码器忠实于潜码内容。

### 3.3 训练目标：潜码条件整流流

PiD 基于预训练 PixelDiT（一种 MMDiT 风格的像素空间扩散 Transformer）进行微调，训练目标为潜码条件整流流损失：

$$\mathcal{L}_{\text{FM}} = \mathbb{E}\left[\|\mathbf{v}_\theta(\mathbf{x}_t, t, c, \tilde{\mathbf{z}}_\sigma, \sigma) - (\mathbf{x}_0 - \epsilon)\|_2^2\right]$$

其中 $\mathbf{v}_\theta$ 为速度场预测网络，$\mathbf{x}_t = t\mathbf{x}_0 + (1-t)\epsilon$ 为扩散时间步 $t$ 的噪声图像，$\mathbf{x}_0 - \epsilon$ 为真实速度。网络同时接收噪声潜码 $\tilde{\mathbf{z}}_\sigma$ 和噪声水平 $\sigma$ 作为额外条件。

### 3.4 少步蒸馏与早期退出

推理加速通过 **DMD2 分布匹配蒸馏** 实现：将多步教师模型蒸馏为 4 步学生模型，同时将分类器自由引导（CFG）蒸馏进模型权重，消除推理时的双重前向计算。蒸馏后的 4 步学生模型在生成场景下 MUSIQ 达到 73.26，反而超越 50 步教师模型的 71.79（Table 2），证明蒸馏有效避免了过度信噪。

**早期退出** 机制直接受益于噪声潜码条件化训练：由于解码器在训练时已见过各种噪声水平的潜码，推理时可直接处理 LDM 部分去噪（如仅运行 50% 步数）的潜码，在保持高分辨率输出质量的同时大幅降低总延迟。Figure 8 展示了 PiD 图像质量随 LDM 终止步数的变化曲线。

### 3.5 模块依赖关系

四个模块形成闭环：PixelDiT 骨干提供像素空间生成先验；噪声潜码条件化使解码器对不完美潜码鲁棒；Sigma 感知门控在保真度与自由度之间做自适应权衡；DMD2 蒸馏将上述能力压缩为 4 步推理。消融实验（Table 4）证实：移除 T2I 先验导致 MUSIQ 从 73.26 骤降至 59.52，移除 Sigma 感知门控则普遍恶化视觉质量——二者均为性能的关键支撑。

## 实验与关键发现

### 主要定量结果

PiD 在六个不同潜空间（FLUX.1、SD3、FLUX.2、Z-Image、DINOv2、SigLIP）上进行了全面评估，统一将潜码解码至 2048×2048 分辨率并与级联超分基线对比。**Table 1** 汇总了图像质量与延迟数据，核心发现如下：

![[assets/figures/papers/paper_list_l13_https_arxiv_org_abs_2605_23902/figures/004_Table_1.jpg]]
*Table 1: Image quality and latency across decoding pipelines. For each cascaded baseline, we apply a state-of-the-art upsampler to match PiD’s target output resolution. PiD attains the highest visual quality while running substantially faster than diffusion-based upsamplers. Red, blue, and green denote the best, second-best, and third-best per metric. “QA.” refers to Q-Align [45], “Uni.” to Unipercept [7], and “VQ-R1” to VisualQuality-R1 [47]. Latency is reported under both eager execution and torch.compile on a single GB200 GPU*

**无参考质量指标全面领先。** 在 VAE 潜码场景下，PiD 将 NIQE 从最佳基线的 4.04/3.76/3.50/4.05 分别降至 3.50/3.11/3.12/3.26（FLUX.1/SD3/FLUX.2/Z-Image），降幅显著。在语义潜码 SigLIP 上，PiD 将 MUSIQ 从 73.68 提升至 74.03，DEQA 从 4.00 提升至 4.17，Unipercept-IAA 从 59.95 提升至 64.94，表明像素扩散先验能有效补偿语义潜码的纹理缺失。

**延迟优势突出。** 在 GB200 GPU 上使用 torch.compile，PiD 延迟约 210 ms，比扩散一步超分基线 **VAE Dec. + SeedVR2-3B**（1237.5 ms）快约 5.9 倍，比 **VAE Dec. + TSD-SR** 和 **InvSR-1** 等任意步方法也快 3–6 倍。在消费级 RTX 5090 上解码 2048×2048 图像仍可在 1 秒内完成，峰值显存仅 13 GB（**Table 3**）。

**MLLM 偏好一致。** 三个闭源多模态大模型（**Figure 4**）在成对比较中一致偏好 PiD 生成的图像，且经过图像顺序交换后的两轮一致性很高，排除了位置偏差。

### 蒸馏效率与步数分析

**Table 2** 展示了教师模型与学生模型在不同推理步数下的表现。教师模型遵循“步数越多质量越高”的常规规律，但经过 DMD2 蒸馏的 4 步学生模型在生成场景下 MUSIQ 达到 73.26，反而超过 50 步教师模型的 71.79。这一反直觉现象说明蒸馏过程不仅压缩了推理步数，还有效抑制了多步采样中的过度信噪累积，使学生模型在保真度与多样性之间取得更好平衡。

### 消融研究

**Table 4（左）** 报告了关键模块消融结果：

- **移除 T2I 先验（从头训练像素扩散解码器）** 导致质量崩溃：MUSIQ 从 73.26 骤降至 59.52，NIQE 从 3.50 飙升至 7.79。这直接验证了预训练像素扩散先验是 PiD 生成能力的决定性来源——该先验提供了强大的高频细节合成能力，仅靠 2.6M 训练数据无法从零习得。
- **移除 sigma-aware gate** 在所有无参考指标上均造成退化，尤其在高噪声潜码条件下重建质量明显恶化。该门控机制通过 $g_i(\mathbf{h}_i, \mathbf{l}_i, \sigma) = \mathrm{sigmoid}(\mathrm{Linear}_i([\mathbf{h}_i, \mathbf{l}_i]) - \alpha\sigma)$ 实现自适应信任：潜码噪声越大（$\sigma$ 越高），注入强度越弱，模型更多依赖自身先验合成细节；潜码干净时则忠实重建。
- **训练时不加入噪声潜码条件化** 使解码器无法处理部分去噪的潜码，早期退出功能失效，且生成多样性下降。噪声化训练 $\tilde{\mathbf{z}}_\sigma = (1-\sigma)\mathbf{z} + \sigma\xi$ 是支持 LDM 早期终止的关键使能技术。

### 重建与生成的双重能力

**Figure 5** 展示了 PiD 在图像重建场景下的表现：给定从干净图像编码的潜码，PiD 能以更高分辨率重建出比原始 VAE/RAE 解码器更锐利的细节。这说明 PiD 并非单纯“幻想”纹理，而是在潜码信息充分时能够忠实还原。

**Figure 6** 揭示了 PiD 随 LDM 去噪步数的行为变化：当 LDM 运行完整去噪步数时，PiD 输出忠实于 VAE 解码结果；当 LDM 中途终止（潜码仅部分去噪），PiD 会逐步合成额外细节，在保真度与生成自由度之间平滑过渡。**Figure 8** 进一步量化了这一趋势曲线。

### 与原生高分辨率生成的对比

**Figure 9** 将“低分辨率 LDM + PiD”与原生 2048×2048 生成进行对比。耦合 PiD 的低分辨率 LDM 大幅降低推理时间，同时图像质量与原生高分辨率生成相当，在细粒度细节上甚至有所超越。这为“低分辨率生成 + 高效解码上采样”的实用范式提供了有力支撑。

### 失败模式与需人工验证的边界

- 文中未对极端复杂 prompt 或分布外场景下的 artifact 进行系统性分析，该点需在实际部署中人工评估。
- PiD 对预训练像素扩散先验的依赖意味着：若该先验对特定域（如医学影像、工业检测）覆盖不足，解码质量可能显著下降，但文中未提供此类跨域实验。
- 蒸馏训练成本较高（128 H100 GPU × 2 小时），且目前仅针对特定分辨率和纵横比训练，泛化到任意分辨率的可行性需进一步验证。

### 公平性说明

所有延迟测量均在相同 GB200 GPU、相同 Docker 环境（PyTorch 2.11.0, CUDA 13.1.1）下使用 torch.compile 进行。级联基线均采用了各自最优的超分模型组合，包括延迟占比最大的扩散一步超分方法。MLLM 成对比较进行了顺序交换以消除位置偏差。

![[assets/figures/papers/paper_list_l13_https_arxiv_org_abs_2605_23902/figures/006_Table_2.jpg]]
*Table 2: Performance of different inference steps of teacher and student model. For teacher models, more inference step leads to better image quality. However, few-step student model can surpass multiple-step teacher model in generated latent decoding cases*

![[assets/figures/papers/paper_list_l13_https_arxiv_org_abs_2605_23902/figures/007_Figure_5.jpg]]
*Figure 5: Image reconstruction comparison. Given a latent encoded from a clean image, PiD reconstructs the image at higher resolution with sharper details than the original VAE / RAE decoder*

![[assets/figures/papers/paper_list_l13_https_arxiv_org_abs_2605_23902/figures/012_Table_4.jpg]]
*Table 4: Ablation study on FLUX.1 [dev] decoding (left) and small-text reconstruction (right)*

![[assets/figures/papers/paper_list_l13_https_arxiv_org_abs_2605_23902/figures/013_Figure_9.jpg]]
*Figure 9: Comparison with native 2048 × 2048 px generation. Coupling a low-resolution LDM with PiD substantially reduces inference time while maintaining image quality competitive to native high-resolution generation, and in some cases surpassing it in fine-grained details. Latency (in lower left corner) is measured on a single GB200 GPU without torch.compile*

## 定位与知识库关联

### 1. 核心创新定位

PiD 的核心创新在于将潜码解码从**确定性重建问题**重新定义为**条件生成问题**。这一视角转换打破了传统自编码器解码器的能力边界——后者只能执行从潜空间到像素空间的逆映射，而无法在解码过程中合成潜码中缺失的高频纹理。PiD 利用预训练像素扩散先验（PixelDiT）的强大生成能力，将解码与上采样统一为单个条件像素扩散模型，从而在保真度与细节合成之间获得动态平衡。

从方法谱系来看，PiD 处于三条技术路线的交汇点：
- **潜空间扩散模型（LDM）** 的编解码框架：PiD 接受 LDM 生成的潜码作为输入，但其解码器本身是像素空间的扩散模型，而非传统的卷积解码器。
- **像素空间扩散先验**：PiD 建立在 PixelDiT 之上，继承了其在 2K/4K 分辨率下的文本条件生成能力。
- **扩散蒸馏技术**：PiD 采用 DMD2 将多步教师模型蒸馏为 4 步学生模型，同时将 CFG 蒸馏进模型权重，消除了推理时的额外计算开销。

### 2. 与基线方法的关系

#### 2.1 级联解码-超分流水线

传统高分辨率图像生成采用“解码 + 超分”的两阶段级联策略。PiD 与以下级联基线进行了系统对比：

| 基线类型 | 代表性方法 | 核心差异 |
|---------|-----------|---------|
| 解码 + GAN 超分 | VAE Dec. + **Real-ESRGAN** | GAN 超分速度快但易产生伪影，细节合成能力有限 |
| 解码 + 扩散一步超分 | VAE Dec. + **SeedVR2-3B** 、**TSD-SR** | 扩散超分质量高但延迟大（SeedVR2-3B 约 1237 ms） |
| 解码 + 扩散任意步超分 | VAE Dec. + **InvSR-1** | 灵活但同样受限于级联架构的累积延迟 |
| SSDD 解码 + 超分 | **SSDD** + 上述超分模型 | 改进了解码阶段的细节保留，但仍需独立超分模块 |
| 潜空间直接上采样 | **LUA** | 在潜空间操作，避免了像素空间的级联开销，但生成细节不如像素空间方法 |

**关键量化对比**（Table 1，FLUX.1 VAE 潜空间，2048×2048 输出）：
- PiD 的 NIQE 降至 3.50，而最佳级联基线（SSDD + InvSR-1）为 4.04，降幅 0.54。
- PiD 延迟约 211 ms（torch.compile，GB200），比 VAE Dec. + SeedVR2-3B（1237.5 ms）快约 5.9 倍。

PiD 相对于级联基线的根本优势在于**消除了中间低分辨率图像的生成与传递**。级联流水线中，解码器输出的低分辨率图像已经丢失了高频信息，后续超分模型只能从有限信息中推测细节。PiD 直接在目标分辨率像素空间建模条件分布，从潜码中一次性提取并合成所有尺度的信息。

#### 2.2 原生高分辨率生成

PiD 还与原生高分辨率 LDM 生成进行了对比（Figure 9）。低分辨率 LDM + PiD 的组合在推理速度上显著优于原生 2048×2048 生成，同时在细粒度细节上可与之竞争甚至超越。这表明 PiD 不仅是一个解码器，更是一种**计算效率优化策略**——将高分辨率生成的计算负担从基座 LDM 转移到轻量级解码器。

#### 2.3 原始 VAE/RAE 解码器

在重建场景下（Figure 5），PiD 能够从相同潜码中恢复出比原始 VAE/RAE 解码器更丰富的高频细节。这是因为像素扩散先验在训练过程中学习了自然图像的纹理分布，能够在解码时补偿自编码器因压缩而丢失的信息。这一能力在语义潜码（如 DINOv2、SigLIP）场景下尤为突出——这些潜码本身不包含纹理信息，传统解码器难以生成高质量图像，而 PiD 借助生成先验可以合成合理的纹理。

### 3. 适用边界与局限

#### 3.1 对预训练先验的依赖

PiD 的核心能力来源于预训练的高分辨率像素扩散先验（PixelDiT）。消融实验（Table 4）表明，移除 T2I 先验（即从头训练像素扩散解码器）会导致 MUSIQ 从 73.26 骤降至 59.52，NIQE 从 3.50 升至 7.79。这意味着 PiD 的性能上限受限于所采用的像素先验的覆盖域——若该先验对特定视觉域（如医学影像、遥感图像）覆盖不足，解码质量可能显著下降。

#### 3.2 训练成本

蒸馏阶段虽然将推理步数降至 4 步，但训练开销较高：蒸馏需 128 H100 GPU × 约 2 小时。此外，当前模型针对特定分辨率和纵横比训练，泛化到新分辨率可能需要额外微调。

#### 3.3 复杂 prompt 下的 artifact

对于极其复杂或不符合训练数据统计分布的 prompt，像素扩散解码可能出现 artifact。论文未对此进行系统性分析，实际部署中需要手动验证边界情况。

#### 3.4 噪声潜码条件化的参数敏感性

噪声潜码条件化采用最大噪声水平 $\sigma_{\max} = 0.8$，但论文未详细讨论该取值的原理及对不同类型潜码（如 DINOv2 vs. VAE 潜码）是否需要单独调优。这在实际应用中可能需要额外的超参数搜索。

### 4. 开放问题

1. **与离散潜码的结合**：PiD 目前处理的是连续潜码（VAE/RAE 潜空间、DINOv2/SigLIP 特征）。能否与 VQ-VAE 等离散潜码结合，进一步减小潜码尺寸并提升压缩率，是一个值得探索的方向。

2. **跨模态扩展**：该方法的核心思想——用像素扩散先验补偿潜码的信息缺失——可推广到视频解码或 3D 生成中的解码阶段。视频场景下还需处理时序一致性问题。

3. **4K 解码延迟优化**：当前 4K 解码仍需进一步降低延迟。稀疏计算、动态 token 压缩或渐进式解码策略可能在不显著增加显存的情况下提升速度。

4. **Sigma-aware gate 的理论分析**：公式 $g_i(\mathbf{h}_i, \mathbf{l}_i, \sigma) = \mathrm{sigmoid}(\mathrm{Linear}_i([\mathbf{h}_i, \mathbf{l}_i]) - \alpha\sigma)$ 中的负偏置项 $\alpha\sigma$ 实现了“噪声越大注入越弱”的自适应信任机制，但 $\alpha$ 的学习动态及其与潜码类型的关系尚未深入分析。

5. **早期退出的最优策略**：PiD 支持 LDM 早期终止（Figure 6、Figure 8），但不同应用场景下“最优终止步数”的自动决策策略仍有待研究——这涉及生成质量与推理速度的动态权衡。

### 5. 在知识库中的位置

PiD 在生成模型知识库中占据一个独特位置：它是**连接潜空间扩散生成与像素空间细节合成的桥梁**。不同于传统的“解码器作为逆映射”的认知，PiD 将解码器定位为“有条件生成器”，这一范式转换对后续工作的启示在于：

- **解码器可以比编码器更强大**：当基座 LDM 的潜码仅包含语义信息时，解码器需要具备独立的细节合成能力。
- **噪声条件化是实现鲁棒性的关键**：通过在训练时向潜码注入可变噪声，解码器学会处理不完美的潜码，这为 LDM 的早期退出和渐进式生成提供了可能。
- **蒸馏可以超越教师**：4 步学生模型在生成场景下超过 50 步教师模型（MUSIQ 73.26 vs 71.79），表明蒸馏过程不仅压缩了推理步数，还避免了教师模型在多步采样中的过度信噪问题。

## 原文 PDF

![[paperPDFs/arxiv_2026/PiD_Fast_and_High-Resolution_Latent_Decoding_with_Pixel_Diffusion.pdf]]
