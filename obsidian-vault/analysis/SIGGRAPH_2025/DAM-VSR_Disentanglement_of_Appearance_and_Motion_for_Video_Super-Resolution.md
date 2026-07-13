---
title: "DAM-VSR: Disentanglement of Appearance and Motion for Video Super-Resolution"
type: paper
paper_level: A
venue: SIGGRAPH
year: 2025
pdf_ref: paperPDFs/SIGGRAPH_2025/DAM-VSR_Disentanglement_of_Appearance_and_Motion_for_Video_Super-Resolution.pdf
project_link: "https://kongzhecn.github.io/projects/dam-vsr/"
code_link: null
aliases:
- DV
- DAM-VSR
tags:
- SIGGRAPH_2025
- topic/vision_multimodal_applications
- topic/representation_self_supervised_transfer
core_operator: 通过对输入视频的首帧（参考帧）进行图像超分辨率（ISR），提升其细节质量，然后将该高质量参考帧注入SVD的解码过程，实现外观增强；同时利用视频ControlNet以原始低质视频控制运动。这种解耦设计允许独立优化外观与运动。
primary_logic: 将VSR任务解耦为“外观增强”（参考帧ISR）与“运动控制”（视频ControlNet），充分发挥视频扩散模型（SVD）的时序生成能力和图像超分辨率模型的细节生成能力，从而实现高保真且时序一致的真实世界VSR。
claims:
- 在UDM10合成基准上，DAM-VSR取得PSNR 27.011、SSIM 0.776、LPIPS 0.311，超越现有方法
- 消融实验表明，去除ISR增强（baseline a）后PSNR降至24.775，加入双向采样并微调VAE解码器可将LPIPS从0.382降至0.311
- 图2可视化分析验证了ISR增强的直观效果：采用ISR后生成结果明显优于不加ISR的版本
- UDM10 (合成) 上 PSNR = 27.011
---

# DAM-VSR: Disentanglement of Appearance and Motion for Video Super-Resolution

> [!tip] 核心洞察
> 将VSR任务解耦为“外观增强”（参考帧ISR）与“运动控制”（视频ControlNet），充分发挥视频扩散模型（SVD）的时序生成能力和图像超分辨率模型的细节生成能力，从而实现高保真且时序一致的真实世界VSR。

| 字段 | 内容 |
|------|------|
| 中文题名 | DAM-VSR：外观与运动解耦的视频超分辨率方法 |
| 英文题名 | DAM-VSR: Disentanglement of Appearance and Motion for Video Super-Resolution |
| 会议/期刊 | SIGGRAPH 2025 |
| Links | [paper](https://arxiv.org/abs/2507.01012) · [Project](https://kongzhecn.github.io/projects/dam-vsr/) |
| Topic | #topic/vision_multimodal_applications #topic/representation_self_supervised_transfer |
| Method | DAM-VSR |
| Dataset | UDM10, YouHQ40, VideoLQ (真实世界) & AIGC29 |

> [!tip] 效果简介
> - UDM10 (合成) 上，PSNR 27.011 vs Baseline (a) w/o ISR: 24.775 (+2.236)；LPIPS 0.311 vs w/o FT-VAE-Decoder: 0.382 (-0.071)。
> - YouHQ40 (合成) 上，PSNR / SSIM / LPIPS 24.246 / 0.668 / 0.367 vs SOTA methods (详见 Table 2) (最佳)。
> - VideoLQ (真实世界) & AIGC29 上，MUSIQ, CLIP-IQA, DOVER (无参考) 所有指标均达到最优 vs SOTA methods (详见 Table 2) (全面领先)。

## 概要

视频超分辨率（VSR）的核心挑战在于同时恢复逼真的纹理细节并保持帧间时序一致性。现有基于扩散模型的方法，如 StableVSR 和 Upscale-A-Video，通常将整个低质视频作为条件输入，试图直接从退化帧中生成高分辨率内容。然而，这类方案面临一个关键瓶颈：扩散模型（如 SVD）生成视频的整体外观高度依赖参考帧的质量，而低质输入提供的参考帧本身缺乏细节，导致生成结果的纹理增强效果有限。

DAM-VSR 提出了一种**外观与运动解耦**的框架，将 VSR 任务拆分为两个独立可控的子问题：**外观增强**与**运动控制**。具体而言，该方法首先对输入视频的首帧执行通用图像超分辨率（ISR），获得高质量参考帧；随后，将该参考帧注入 SVD 的去噪 UNet 以增强生成视频的细节表现，同时利用视频 ControlNet 以原始低质视频为条件控制运动结构。这一解耦设计使得外观和运动可以分别优化，充分发挥图像超分辨率模型的细节生成能力与视频扩散模型的时序建模能力。

为支持长视频生成，DAM-VSR 进一步引入了**运动对齐的双向采样策略**：将长视频分割为固定长度片段，通过前向采样与反向采样共享旋转后的时间注意力图，在片段拼接处保持时序一致性。此外，针对高分辨率输入的内存瓶颈，方法采用了分块去噪的平均融合策略（tile sampling）。

实验验证了该框架的有效性。在合成基准 UDM10 上，DAM-VSR 取得了 PSNR 27.011、LPIPS 0.311 的结果，显著优于不加 ISR 的基线（PSNR 24.775）。消融实验表明，ISR 增强是外观质量提升的关键驱动因素，而微调 VAE 解码器将 LPIPS 从 0.382 降至 0.311，进一步改善了感知质量。在真实世界数据 VideoLQ 和 AIGC 数据 AIGC29 上，DAM-VSR 在多个无参考指标（MUSIQ、CLIP-IQA、DOVER）上均达到最优。

该工作的核心贡献在于：**将 VSR 中的外观与运动显式解耦**，使得图像超分辨率与视频扩散模型可以各司其职，从而在保持时序一致性的前提下实现高保真的真实世界视频超分辨率。

视频超分辨率（VSR）旨在从低质量视频中恢复高分辨率、细节丰富且时序一致的帧序列。真实世界VSR面临的核心挑战在于，退化过程复杂且未知，导致输入视频同时丢失了**外观细节**（纹理、边缘）与**运动信息**（光流、时序连贯性）。现有方法大致分为两类：基于GAN或Transformer的传统VSR方法，以及基于扩散模型的生成式VSR方法。

基于扩散模型的VSR方法近年来展现出强大的生成能力，其主流范式是借助图像到视频扩散模型（如SVD）从单帧参考图像生成视频。然而，这一范式存在一个关键瓶颈：**SVD生成视频的整体外观高度依赖参考图像的质量**。当输入视频本身质量较低时，其首帧（作为参考帧）缺乏足够的纹理细节，直接使用SVD加视频ControlNet的生成结果在外观增强上效果有限——生成视频虽然时序连贯，但细节仍然模糊，无法有效恢复真实纹理（如Fig. 2b所示）。换言之，**低质参考帧成为限制生成质量的上限**。

这一瓶颈揭示了现有方法的根本性缺陷：**外观增强与运动控制被隐式地耦合在同一个生成过程中**。由于视频扩散模型需要同时处理“生成什么纹理”和“保持什么运动”两个任务，当参考帧质量不足时，模型无法有效补偿外观信息的缺失。因此，亟需一种将外观与运动**显式解耦**的框架，允许分别对两个子问题进行独立优化——利用图像超分辨率（ISR）模型增强参考帧的外观细节，同时利用视频ControlNet从原始低质视频中提取运动结构。这正是DAM-VSR的核心动机：**将VSR任务解耦为“外观增强”与“运动控制”两个独立可控的子问题，充分发挥图像超分辨率模型的细节生成能力与视频扩散模型的时序生成能力，从而实现高保真且时序一致的真实世界VSR**。

## 核心方法与创新机理

DAM-VSR 的核心创新在于将视频超分辨率（VSR）任务解耦为**外观增强**与**运动控制**两个独立子问题，并围绕这一解耦设计引入三项关键机制，从根本上改变了扩散模型在 VSR 中的工作方式。

### 外观与运动的解耦范式

现有基于扩散模型的 VSR 方法（如 **StableVSR** (Rota et al., ECCV 2025)、**Upscale-A-Video** (Zhou et al., CVPR 2024)）直接使用低质视频作为 SVD（Stable Video Diffusion）的条件输入。由于低质参考帧本身缺乏纹理细节，SVD 从噪声中生成的细节有限，外观增强效果受限于输入质量。DAM-VSR 的解决思路是：**将“生成什么纹理”与“如何运动”分离**。

具体而言，外观增强通过一个独立的图像超分辨率（ISR）模块完成：对输入视频的首帧 $I_1$ 执行通用 ISR，获得高质量参考帧 $H_1$：
$$H_1 = SR_I(I_1)$$
该高质量参考帧随后注入 SVD 的去噪 UNet，作为外观信息的来源。与此同时，运动控制由视频 ControlNet 承担，以原始低质视频 $C$ 为条件，控制生成视频的运动结构与时序一致性。这种解耦使两个子任务可以独立优化——ISR 模块专注于细节生成，视频 ControlNet 专注于运动保持，避免了单一模块同时处理两者的性能折衷。

### 运动对齐的双向采样策略

SVD 基座模型固定生成 14 帧，长视频超分辨率需要分片处理。传统方法采用逐帧自回归或直接分块拼接，容易引入片段间的时序不一致。DAM-VSR 提出**运动对齐的双向采样**（Motion-Aligned Bidirectional Sampling），将长视频分割为固定长度 $k$ 的 $m$ 个片段：
$$I = \{I_1, I_2, \cdots, I_n\} = \{C_1, \cdots, C_m\}$$
每个片段执行前向生成 $F$ 和反向生成 $B$ 两次采样。前向采样以片段首帧的高质量参考帧 $H_1$ 为外观条件，输出预测噪声 $p_t^f$ 和时间注意力图 $A_t$：
$$p_t^f, A_t = F(z_t, t, H_1, C)$$
反向采样以片段末帧的高质量参考帧 $H_k$ 为条件，并将前向采样的注意力图旋转后注入，确保两个方向的生成共享运动信息：
$$p_t^b, \_ = B(z_t', t, H_k, C') \quad \{A_t^g \leftarrow A_t'\}$$
最终通过噪声融合得到一致的预测：
$$p_t = blending(reverse(p_t^b), p_t^f)$$
相邻片段通过共享首尾高质量帧实现无缝拼接，保证长视频的全局时序一致性。

### 高分辨率生成的内存优化

为支持高分辨率输入（如 4K 视频）在有限 GPU 内存下的推理，DAM-VSR 采用**分块采样**（Tile Sampling）策略：将潜在空间中的特征图划分为重叠的瓦片，分别去噪后在重叠区域进行平均融合。这使得方法可以在消费级硬件上处理高分辨率视频，而不牺牲生成质量。

### 与 baseline 的关键差异总结

| 设计维度 | 基线方法（SVD+视频ControlNet） | DAM-VSR |
|---------|-------------------------------|---------|
| 外观增强方式 | 仅依赖 SVD 从低质参考帧生成细节 | 先对参考帧进行 ISR，获得高质量参考帧再注入 SVD |
| 运动控制机制 | 视频 ControlNet 直接以低质视频为条件 | 视频 ControlNet 以低质视频控制运动，外观由增强参考帧独立提供 |
| 长视频生成策略 | 逐帧自回归或直接分块拼接 | 运动对齐的双向采样，分片重叠且共享首尾高质量帧 |
| 高分辨率内存处理 | 直接生成，内存消耗大 | 分块去噪的平均策略，支持有限内存下的超分辨率 |

消融实验（Table 1）验证了这些创新的有效性：移除 ISR 增强后，PSNR 从 27.011 降至 24.775；移除双向采样后，PSNR 降至 26.654；未微调 VAE 解码器时，LPIPS 从 0.311 升至 0.382。这些结果表明，外观增强与运动控制的解耦是性能提升的核心驱动力，而双向采样和 VAE 微调进一步提升了时序一致性和感知质量。

DAM-VSR 提出一种**外观与运动解耦**的视频超分辨率框架，将 VSR 任务拆分为两个独立可控的子问题：**外观增强**和**运动控制**。其整体流水线如 Fig. 3 所示，核心思路是：利用视频扩散模型 SVD 的时序生成能力来保证帧间一致性，同时通过引入图像超分辨率（ISR）模块来弥补低质输入中参考帧细节不足的根本瓶颈。

![[assets/figures/papers/paper_list_l23_https_arxiv_org_abs_2507_01012/figures/003_Figure_3.jpg]]
*Figure 3: The overall pipeline of the proposed DAM-VSR method. Our method introduces an appearance and motion disentanglement framework for VSR. To support long video generation, we propose a motion-aligned bidirectional sampling strategy, which consists of a disentangled forward generation process and a disentangled backward generation process. These two processes maintain temporal consistency through motion alignment*

### 核心瓶颈与解耦设计

直接使用 SVD + 视频 ControlNet 进行 VSR 时，生成视频的整体外观由低质输入的参考帧控制。由于低质参考帧本身缺乏细节，SVD 无法凭空生成真实纹理，导致外观增强效果有限（见 Fig. 2b）。DAM-VSR 的解决方案是：

- **外观增强**：先对输入视频的首帧（参考帧）进行通用图像超分辨率，获得高质量参考帧 $H_1 = \text{SR}_I(I_1)$，再将该高质量帧注入 SVD 的去噪 UNet 解码过程，为整个生成视频提供丰富的细节先验。
- **运动控制**：视频 ControlNet 以原始低质视频为条件，负责控制生成视频的运动结构和时序动态，不受外观增强模块的干扰。

这种解耦设计的核心洞察在于：充分发挥视频扩散模型的时序生成能力和图像超分辨率模型的细节生成能力，两者各司其职，从而实现高保真且时序一致的真实世界 VSR。

### 模块组成与数据流

整体框架包含以下关键模块，其架构细节见 Fig. 4：

1. **参考帧图像超分辨率（ISR）**：对输入视频首帧 $I_1$ 进行任意图像超分辨率，输出高质量参考帧 $H_1$。该模块可替换为不同的 ISR 方法（如 ResShift、InvSR 等），框架具有良好的兼容性。

2. **视频 ControlNet**：从图像 ControlNet 设计扩展而来，复制原始 UNet 编码器的所有层（包括时间注意力和 3D 卷积层），以低质视频 $C$ 为条件提取运动控制信号，控制生成视频的运动结构。

3. **去噪 UNet（SVD 骨干）**：接收增强后的参考帧 $H_1$ 和视频 ControlNet 的运动控制信号，在潜在空间中进行扩散去噪，生成高质量视频帧序列。

4. **运动对齐的双向采样**：针对长视频生成，将输入视频分割为固定长度的片段（Eq. 6），通过前向采样 $F(z_t, t, H_1, C)$ 和反向采样 $B(z_t', t, H_k, C')$ 共享旋转后的时间注意力图，最后通过噪声融合 $p_t = \text{blending}(\text{reverse}(p_t^b), p_t^f)$ 保持片段间的时序一致性（Eq. 3-5，详见 Fig. 5）。

5. **分块采样**：为支持高分辨率输入，采用分块去噪策略，在重叠区域进行平均融合以缓解内存压力。

### 输入输出规范

- **输入**：低质视频片段 $C$ 及其首帧 $I_1$（长视频则分割为多个片段 $C_1, \cdots, C_m$）。
- **输出**：高分辨率、细节丰富且时序一致的超分辨率视频。
- **训练目标**：基于 v-prediction 的扩散损失 $\mathcal{L}(\theta) = E_{t \sim U[1,T]} \|\epsilon_{\theta}(z_t, t, c) - y\|_2^2$（Eq. 1），其中条件 $c$ 包含增强后的参考帧特征。

> **注意**：SVD 基座模型固定生成 14 帧，长视频需通过分片与双向采样实现，这可能引入边界不一致或误差累积。双向采样增加了约两倍的计算开销，且最终生成质量高度依赖所选 ISR 方法的性能。

![[assets/figures/papers/paper_list_l23_https_arxiv_org_abs_2507_01012/figures/011_Figure_7.jpg]]
*Figure 7: The experimental results of the proposed framework for other applications, including video editing and video style transfer*

DAM-VSR 将视频超分辨率（VSR）解耦为**外观增强**与**运动控制**两个子问题，其核心由以下模块构成。

### 参考帧图像超分辨率（ISR）——外观增强

扩散模型（SVD）生成视频时，整体外观由参考帧控制。若直接使用低质输入的首帧作为参考，生成结果缺乏真实纹理（Fig. 2b）。为此，DAM-VSR 在 SVD 解码前引入一个独立的图像超分辨率步骤：

$$H_1 = SR_I(I_1) \tag{2}$$

其中 $I_1$ 为输入低质视频片段的首帧，$SR_I$ 为任意图像超分辨率模型（如 ResShift、InvSR），输出高质量参考帧 $H_1$。该高质量帧随后注入 SVD 的去噪 UNet 作为条件，引导生成细节丰富的视频帧。消融实验表明，去除 ISR 增强后，UDM10 上的 PSNR 从 27.011 降至 24.775（Table 1），验证了外观增强对整体性能的决定性作用。

### 视频 ControlNet——运动控制

运动控制由视频 ControlNet 实现，其架构适配自图像 ControlNet：复制原始 UNet 编码器的全部层（包括时序注意力层和 3D 卷积层），并添加视频嵌入层。视频 ControlNet 以低质视频 $C$ 为条件，提取运动结构信息，与增强后的参考帧 $H_1$ 解耦输入到去噪 UNet 中（Fig. 4）。

![[assets/figures/papers/paper_list_l23_https_arxiv_org_abs_2507_01012/figures/004_Figure_4.jpg]]
*Figure 4: The model architecture of the disentangled forward generation (the same network architecture as the disentangled backward generation) includes a video ControlNet and a denoising UNet. The input for the generation consists of a low-quality video and a high-quality reference image*

### 去噪 UNet 训练

扩散模型的训练遵循 v-prediction 目标：

$$\mathcal{L}(\theta) = E_{t \sim U[1,T]} ||\epsilon_{\theta}(z_t, t, c) - y||_2^2 \tag{1}$$

其中 $z_t$ 为加噪后的潜变量，$c$ 为条件（增强参考帧与运动控制信号的组合），$y$ 为 v-prediction 目标。

### 运动对齐的双向采样——长视频一致性

SVD 基座模型固定生成 14 帧，长视频需分片处理。DAM-VSR 提出运动对齐的双向采样策略（Fig. 3），每个片段分别进行前向和反向生成：

$$p_t^f, A_t = F(z_t, t, H_1, C) \tag{3}$$

前向生成预测噪声 $p_t^f$ 并保存时间注意力图 $A_t$。

$$p_t^b, \_ = B(z_t', t, H_k, C') \quad \{A_t^g \leftarrow A_t'\} \tag{4}$$

反向生成以片段末帧 $H_k$ 为参考、反转视频 $C'$ 为条件，并将旋转后的注意力图 $A_t'$ 注入，保证前后向生成的时序一致。最终噪声通过平均融合：

$$p_t = blending(reverse(p_t^b), p_t^f) \tag{5}$$

长视频分割为 $m$ 个固定长度 $k$ 的片段：

$$I = \{I_1, I_2, \cdots, I_n\} = \{C_1, \cdots, C_m\} \tag{6}$$

相邻片段共享首尾高质量帧，拼接实现任意长度视频的超分辨率（Fig. 5）。消融实验显示，移除双向采样后 PSNR 从 27.011 降至 26.654（Table 1），证实该策略对时序一致性的贡献。

### VAE 解码器微调

为改善生成帧的感知质量，对 VAE 解码器进行微调，联合优化 L2 损失、感知损失和 GAN 损失：

$$\mathcal{L} = \mathcal{L}_{L2} + \alpha \mathcal{L}_{percept} + \beta \mathcal{L}_{GAN}$$

微调后 LPIPS 从 0.382 降至 0.311（Table 1），显著提升了感知指标。

### 分块采样（Tile Sampling）

为处理高分辨率输入，采用分块去噪策略：将潜变量划分为重叠的块，分别去噪后在重叠区域平均融合，以在有限 GPU 内存下完成超分辨率生成（Fig. 11）。

## 实验与关键发现

### 核心瓶颈验证：ISR增强的决定性作用

DAM-VSR的设计起点是一个明确的瓶颈诊断：当直接使用SVD（Stable Video Diffusion）作为视频扩散模型，并以视频ControlNet接收低质输入视频时，生成视频的外观由低质参考帧控制，导致增强后的纹理细节严重不足（图2b）。为解决这一问题，DAM-VSR引入解耦策略，将VSR任务拆分为“外观增强”与“运动控制”两个独立子问题。

消融实验（Table 1）定量验证了这一设计。在UDM10合成基准上，完整DAM-VSR取得PSNR 27.011、SSIM 0.776、LPIPS 0.311。若移除ISR增强（baseline a），PSNR骤降至24.775，降幅达2.236 dB，这直接证明了参考帧质量对最终生成保真度的因果性影响。图2的可视化对比进一步提供了直观证据：加入ISR后，生成结果在纹理细节和视觉真实感上明显优于不加ISR的版本。

![[assets/figures/papers/paper_list_l23_https_arxiv_org_abs_2507_01012/figures/006_Table_1.jpg]]
*Table 1: Ablation study of various components within DAM-VSR on UDM10*

### 消融实验：各模块贡献分析

Table 1系统拆解了DAM-VSR各组件在UDM10上的贡献。除ISR增强外，以下发现值得关注：

- **VAE解码器微调**：将VAE解码器在视频数据上进行微调（联合L2、感知损失和GAN损失），使LPIPS从0.382降至0.311，降幅0.071。这表明微调后的解码器能有效抑制伪影，提升感知质量，是感知指标改善的关键操作。
- **双向采样策略**：移除运动对齐的双向采样（baseline f）后，PSNR从27.011降至26.654。双向采样的核心机制是通过前向和反向生成共享旋转后的时间注意力图，从而在片段边界保持时序一致性。其消融结果说明，该策略对长视频生成的保真度有不可忽略的贡献。
- **ISR方法兼容性**：论文进一步验证了使用不同ISR方法（如ResShift、InvSR）均可提升VSR性能，说明DAM-VSR框架对外观增强模块具有良好的兼容性，不依赖单一ISR实现。

### 主实验结果：多基准全面对比

Table 2汇总了DAM-VSR在合成、真实世界和AIGC三类数据上的定量对比。在合成基准UDM10上，DAM-VSR以PSNR 27.011、SSIM 0.776、LPIPS 0.311全面超越现有方法；在YouHQ40上同样取得PSNR 24.246、SSIM 0.668、LPIPS 0.367的最优结果。在真实世界数据VideoLQ和AIGC数据AIGC29上，由于缺乏参考真值，采用无参考指标MUSIQ、CLIP-IQA和DOVER进行评估，DAM-VSR在所有指标上均达到最优。

与基线方法的对比揭示了DAM-VSR的优势来源。相比基于图像扩散模型的**StableVSR**（Rota et al., ECCV 2025）和**Upscale-A-Video**（Zhou et al., CVPR 2024），DAM-VSR通过视频扩散模型（SVD）天然具备更强的时序建模能力；相比**MGLD-VSR**（Yang et al., ECCV 2025）等运动引导方法，DAM-VSR的解耦设计允许独立优化外观和运动，避免了单一条件信号下的质量折衷；相比**VEnhancer**（He et al., 2024）和**SeedVR**（Wang et al., 2025）等通用视频增强方法，DAM-VSR针对VSR任务的特化设计在细节保真度上更具优势。

### 失败模式与局限性

尽管DAM-VSR在多个基准上表现优异，但其设计存在若干固有限制：

1. **长视频边界一致性问题**：SVD基座模型固定生成14帧，长视频需通过分片与双向采样拼接。尽管双向采样通过注意力图共享缓解了片段间不一致，但边界误差累积仍可能发生，尤其在运动剧烈或场景切换频繁时。
2. **计算开销**：双向采样使推理计算量约翻倍，结合8张A100-80G GPU的训练配置，普通用户难以复现。对于实时或低资源场景，该方法目前不适用。
3. **ISR依赖风险**：最终生成质量高度依赖所选ISR方法的输出。若ISR引入伪影、过度平滑或错误纹理，这些缺陷将通过SVD的解码过程传播到整个生成视频，形成级联误差。
4. **无参考评估的不确定性**：在真实世界数据上依赖MUSIQ、CLIP-IQA等无参考指标，这些指标与人类感知的一致性存在已知偏差，部分结论需通过用户研究进一步验证。

### 重要图表结论

- **Fig. 2**（消融可视化）：直观展示ISR增强的因果效应——不加ISR时生成结果细节模糊，加入ISR后纹理显著改善，接近真值。
- **Table 1**（消融定量）：完整方法PSNR 27.011 vs. 无ISR的24.775，VAE微调使LPIPS从0.382降至0.311，双向采样贡献约0.357 dB PSNR提升。
- **Table 2**（主结果）：DAM-VSR在UDM10、YouHQ40、VideoLQ、AIGC29四个基准上均取得最优或次优，尤其在真实世界和AIGC数据上的无参考指标全面领先，验证了解耦框架的泛化能力。

![[assets/figures/papers/paper_list_l23_https_arxiv_org_abs_2507_01012/figures/007_Table_2.jpg]]
*Table 2: antitative evaluations on diferent VSR benchmarks from diverse source, i.e., synthetic (UDM10, YouHQ40, REDS30), real-world (VideoLQ), and AIGC (AIGC29) data. The best and second best performances are marked in red and blue, respectively*

![[assets/figures/papers/paper_list_l23_https_arxiv_org_abs_2507_01012/figures/008_Figure_6.jpg]]
*Figure 6: alitative ablation study of DAM-VSR*

## 定位与知识库关联

### 1. 任务定位：从单任务耦合到外观-运动解耦

DAM-VSR 将真实世界视频超分辨率（VSR）重新定义为一个**外观增强**与**运动控制**的解耦问题。这一思路与现有基于扩散模型的 VSR 方法形成根本性差异：

- **图像扩散模型路线**（如 **StableVSR** (Rota et al., ECCV 2025)、**Upscale-A-Video** (Zhou et al., CVPR 2024)）将 VSR 视为逐帧或滑动窗口的图像增强问题，难以保证长程时序一致性。
- **视频扩散模型路线**（如 **VEnhancer** (He et al., 2024)、**SeedVR** (Wang et al., 2025)）直接以低质视频为条件进行生成，外观细节的增强完全依赖扩散模型从退化输入中“猜测”，当参考帧本身质量极低时，生成结果缺乏真实纹理——这正是 DAM-VSR 识别出的核心瓶颈。
- **运动引导的潜在扩散方法**（如 **MGLD-VSR** (Yang et al., ECCV 2025)）虽引入了运动信息，但外观与运动仍耦合在统一的扩散过程中，无法独立优化任一维度。

DAM-VSR 的关键突破在于：**将外观增强的责任从 SVD 基座模型中剥离**，交由专门的图像超分辨率（ISR）模块处理，而 SVD + 视频 ControlNet 仅负责运动结构的保持与细节传播。这种解耦使两个子问题可以各自使用最优工具——ISR 领域成熟的细节生成能力，与视频扩散模型强大的时序建模能力——形成互补而非竞争。

### 2. 与相关工作的技术关系

#### 2.1 基座模型继承

DAM-VSR 直接构建在 **SVD**（Stable Video Diffusion）之上，继承了其图像到视频的生成范式：以参考帧为条件，通过去噪 UNet 在潜在空间中生成视频序列。视频 ControlNet 的设计则沿袭了 **图像 ControlNet**（Zhang et al., 2023）的架构思路——复制 UNet 编码器、注入零卷积层——并将其扩展到视频域，克隆了时间注意力和 3D 卷积层。

#### 2.2 与语义增强路线的差异

**SeeClear**（Tang et al., NeurIPS 2024）通过语义蒸馏增强 VSR，侧重于高层语义信息的注入；**STAR**（Xie et al., 2025）利用文本到视频模型进行增强。DAM-VSR 与这些方法的不同在于：它不依赖额外的语义或文本条件，而是通过**低层像素级的 ISR 增强**来提升参考帧质量，再借助 SVD 的生成先验将细节传播到整个视频序列。这种设计使其对输入类型的依赖更少，但同时也意味着最终质量高度受限于所选 ISR 方法的性能。

#### 2.3 长视频生成策略的改进

现有视频扩散模型（如 SVD）通常固定生成帧数（默认为 14 帧）。DAM-VSR 提出的**运动对齐双向采样**策略，通过前向和反向两个生成过程共享旋转后的时间注意力图，在片段拼接处保持时序一致性。这与简单的自回归逐帧生成或直接分块拼接有本质区别：双向采样使每个片段的首尾帧都经过高质量参考帧的“锚定”，减少了误差累积。

### 3. 适用边界与局限

**已验证的适用场景：**
- 合成低质视频（UDM10、YouHQ40、REDS30）：全参考指标（PSNR/SSIM/LPIPS）达到最优
- 真实世界视频（VideoLQ）：无参考指标（MUSIQ、CLIP-IQA、DOVER）全面领先
- AIGC 视频（AIGC29）：生成细节的视觉真实感优于对比方法
- 可扩展至视频编辑和风格迁移任务（Fig. 7 演示）

**需要手动验证的边界：**
- SVD 基座模型固定生成 14 帧，长视频必须通过分片拼接处理，可能在片段边界引入不一致或误差累积——论文未提供边界一致性的定量评估
- 双向采样使计算开销约增加一倍，8 张 A100-80G GPU 的训练配置对普通用户复现构成显著门槛
- 最终生成质量高度依赖所选 ISR 方法：若 ISR 结果引入伪影或过度平滑，这些缺陷将传播到整个生成视频——论文虽验证了多种 ISR 方法（ResShift、InvSR 等）的兼容性，但未系统分析 ISR 失败模式对最终输出的影响
- 在真实世界数据上依赖无参考 IQA 指标，与人类感知可能存在偏差；缺乏大规模用户研究来验证感知质量优势

### 4. 开放问题

1. **帧数限制的根本性突破**：能否通过修改 SVD 架构或训练策略，使解耦框架直接支持任意长度视频的生成，而无需分片拼接？这涉及对旋转位置编码和注意力机制的底层改造。

2. **计算效率的优化路径**：双向采样带来的两倍推理开销是否有压缩空间？可能的方案包括：蒸馏出单向近似模型、在部分时间步共享注意力图、或设计非对称的前向-反向采样策略。

3. **端到端联合优化的可能性**：当前 ISR 模块与 SVD 是独立训练的，是否可以在训练阶段联合优化，使 ISR 产生的细节更适配 SVD 的传播特性？这需要解决两个模型梯度回传的技术挑战。

4. **极端运动与遮挡下的鲁棒性**：运动对齐的注意力共享假设前向和反向生成的时间注意力图可以通过旋转对齐——在极端运动、大幅度遮挡或场景切换时，这一假设是否仍然成立？需要针对性的压力测试。

5. **框架的泛化能力边界**：论文展示了视频编辑和风格迁移的初步结果，但这些应用是否需要对视频 ControlNet 进行微调？框架能否处理其他视频恢复任务（如去模糊、去噪）而不需要重新训练控制分支？

## 原文 PDF

![[paperPDFs/SIGGRAPH_2025/DAM-VSR_Disentanglement_of_Appearance_and_Motion_for_Video_Super-Resolution.pdf]]
