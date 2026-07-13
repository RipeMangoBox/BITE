---
title: Generative Neural Video Compression via Video Diffusion Prior
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/Generative_Neural_Video_Compression_via_Video_Diffusion_Prior.pdf
project_link: null
code_link: "https://github.com/anchen1011/toflow/blob/master/data/original_vimeo_links.txt"
aliases:
- GV
- GNVCVDP
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/generative_models_diffusion
- topic/generative_models_diffusion/diffusion_image_video
core_operator: 采用预训练的视频扩散Transformer（VideoDiT）作为原生视频先验，将重建过程转化为序列级条件去噪，通过部分噪声初始化和压缩感知条件适配器，对解码后的时空潜在变量进行联合优化。
primary_logic: 将视频压缩的解码过程重新定义为基于视频扩散模型的序列级条件去噪，而非独立的逐帧重建，从而利用学习到的时空表示恢复一致的细节。
claims:
- GNVC-VD 是第一个利用视频扩散模型实现序列级潜在压缩和优化的生成式神经视频压缩框架。
- 与基于图像先验的 GLC-Video 相比，GNVC-VD 显著减少了时序闪烁，并实现了更低的 Warp Error（Ewarp）。
- 在 HEVC-B、UVG 和 MCL-JCV 上的速率-失真曲线表明，GNVC-VD 在 LPIPS 和 DISTS 指标上均达到了最佳的感知质量。
- 消融实验证实，流匹配潜在优化和两阶段训练策略对于实现高感知质量至关重要。
---

# Generative Neural Video Compression via Video Diffusion Prior

> [!tip] 核心洞察
> 将视频压缩的解码过程重新定义为基于视频扩散模型的序列级条件去噪，而非独立的逐帧重建，从而利用学习到的时空表示恢复一致的细节。

| 字段 | 内容 |
|------|------|
| 中文题名 | 基于视频扩散先验的生成式神经视频压缩 |
| 英文题名 | Generative Neural Video Compression via Video Diffusion Prior |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2512.05016) · [Code](https://github.com/anchen1011/toflow/blob/master/data/original_vimeo_links.txt) |
| Topic | #topic/vision_multimodal_applications #topic/generative_models_diffusion #topic/generative_models_diffusion/diffusion_image_video |
| Method | GNVC-VD |
| Dataset | UVG, HEVC-B, HEVC-B, UVG, MCL-JCV |

> [!tip] 效果简介
> - UVG 上，BD-Rate (DISTS) GNVC-VD vs DCVC-RT (-98%)；BD-Rate (LPIPS) GNVC-VD vs DCVC-RT (-56%)。
> - HEVC-B 上，E_warp (↓) 66.6 vs GLC-Video (86.5) (-19.9)；CLIP-F (↑) 0.982 vs GLC-Video (0.979) (+0.003)。
> - HEVC-B, UVG, MCL-JCV 上，LPIPS, DISTS (perceptual quality) best vs HEVC, VVC, DCVC-FM, DCVC-RT, GLC-Video (qualitatively best)。

## 概要

### 1. 问题背景

极低码率视频压缩面临一个核心矛盾：传统混合编解码器（如 HEVC、VVC）和学习型编解码器（如 **DCVC-FM**，Li et al., CVPR 2024；**DCVC-RT**，Li et al., NeurIPS 2021）在码率极度受限时会产生模糊的重建帧，丢失精细纹理；而基于图像生成先验的感知压缩方法（如 **GLC-Video**，Qi et al., IEEE TCSVT 2025）虽能恢复锐利纹理，却因缺乏长程时序建模能力，在帧间引入严重的结构幻觉和时序闪烁——纹理在不同帧之间漂移、突变，破坏视觉一致性。

**核心瓶颈**：现有感知视频压缩方法依赖图像生成先验进行逐帧增强，缺乏原生视频先验的时空联合建模能力，导致在极低码率下无法同时实现高感知质量和时序稳定性。

### 2. 核心方法

本文提出 **GNVC-VD**（Generative Neural Video Compression via Video Diffusion Prior），将视频压缩的解码过程重新定义为基于视频扩散模型的**序列级条件去噪**，而非独立的逐帧重建。其关键创新在于：

- **视频原生先验**：采用预训练的视频扩散 Transformer（VideoDiT）替代图像生成先验，利用其学习到的时空表示对解码潜在变量进行序列级联合优化。
- **部分噪声初始化**：从解码后的潜在变量出发，注入部分高斯噪声（噪声水平 $t_N=0.7$），而非从纯噪声开始的标准生成过程，使优化过程更贴近压缩域起点。
- **压缩感知条件适配**：通过条件适配器将压缩域上下文特征注入 DiT 中间层，学习校正项以补偿压缩退化，使扩散先验适配于重建任务而非生成任务。
- **两阶段训练**：第一阶段在潜在空间对齐编解码器与扩散先验，第二阶段在像素域进行感知微调，确保恢复质量。

### 3. 方法定位

GNVC-VD 属于**生成式神经视频压缩**范畴，其方法谱系定位如下：

| 维度 | 传统/学习型编解码器 | 图像先验生成式编解码器 | **GNVC-VD（本文）** |
|------|---------------------|------------------------|---------------------|
| 生成先验类型 | 无 | 预训练图像生成模型（如 Stable Diffusion） | 预训练视频扩散 Transformer（VideoDiT） |
| 优化粒度 | 逐帧独立编码 | 逐帧独立增强 | 序列级联合优化 I 帧和 P 帧潜在变量 |
| 去噪初始化 | — | 纯高斯噪声 | 解码潜在变量 + 部分噪声（$t_N=0.7$） |
| 训练策略 | 端到端 | 端到端 | 两阶段压缩感知训练（潜在对齐 + 像素微调） |

### 4. 主要结果

在 HEVC-B、UVG 和 MCL-JCV 三个标准基准上，GNVC-VD 在极低码率区间（$<0.03$ bpp）取得了以下关键结果：

- **感知质量最优**：在 LPIPS 和 DISTS 指标上的速率-失真曲线全面优于传统编解码器（HEVC、VVC）、学习型编解码器（DCVC-FM、DCVC-RT）和生成式基线（GLC-Video）。
- **码率节省显著**：以 VVC 为锚点，在 UVG 数据集上 GNVC-VD 实现了超过 98% 的 DISTS BD-Rate 降低和 56% 的 LPIPS BD-Rate 降低。
- **时序稳定性突破**：在 HEVC-B 上，Warp Error（$E_{\text{warp}}$）从 GLC-Video 的 86.5 降至 66.6，时序闪烁大幅减少；CLIP-F 语义连续性指标达到 0.982。

### 5. 局限与展望

GNVC-VD 的主要局限在于**模型规模巨大**（总参数量约 23 亿，其中 VideoDiT 占 21.5 亿），导致解码延迟高（1920×1080 分辨率下约 1557 ms），难以满足实时应用需求。此外，当前仅验证了较短视频片段（最大 GOP 25 帧）的性能，对更长序列或流媒体场景的扩展性尚待探索。未来方向包括：提升上下文变换编码效率、加速扩散优化过程、扩展至长视频场景，以及探索更有效的压缩域特征注入机制。



### 视频压缩的感知质量瓶颈

传统视频编码标准（如 **HEVC** (Sullivan et al., IEEE TCSVT 2012)、**VVC**）和学习型神经编解码器（如 **DCVC-FM** (Li et al., CVPR 2024)、**DCVC-RT** (Li et al., NeurIPS 2021)）在极低码率（< 0.03 bpp）下均会产生模糊的重建帧，丢失精细纹理。为突破这一限制，近期工作开始引入生成式先验：**PLVC** (Yang et al., IJCAI 2022) 采用 GAN 进行后处理增强，**GLC-Video** (Qi et al., IEEE TCSVT 2025) 则利用预训练图像扩散模型（如 Stable Diffusion）对解码帧进行逐帧增强。

### 现有方法的根本缺陷：缺乏长程时序建模

尽管基于图像生成先验的方法能恢复更清晰的纹理，但其核心瓶颈在于**逐帧独立增强**的范式。由于缺乏对视频序列整体时空结构的建模能力，这类方法在极低码率下会出现两类严重问题：

1. **时序闪烁**：相邻帧之间纹理细节不稳定，表现为纹理漂移和结构突变。定量证据显示，GLC-Video 在 HEVC-B 数据集上的帧级 Warp Error（$E_{\text{warp}}$）达到 86.5，且波动剧烈（Figure 2 (b)）。
2. **结构幻觉**：图像先验缺乏对运动连续性的约束，可能在单帧中生成看似合理但跨帧不一致的结构。

### 本文动机：从图像先验到视频原生先验

上述分析揭示了一个关键洞察：**视频压缩的解码过程不应被建模为独立的逐帧重建，而应被重新定义为基于视频扩散模型的序列级条件去噪**。视频扩散模型（Video Diffusion Transformer, VideoDiT）在预训练过程中学习了丰富的时空表示，能够编码物体运动、纹理演化和场景连续性——这些正是图像先验所缺失的。

基于此，本文提出 **GNVC-VD**——首个利用视频原生扩散模型实现序列级潜在压缩与优化的生成式神经视频压缩框架。其核心思路是：将解码后的时空潜在变量作为部分带噪状态，通过流匹配（Flow Matching）机制在 VideoDiT 的去噪过程中进行联合优化，从而恢复跨帧一致的精细纹理，从根本上解决时序闪烁问题。



## 核心方法与创新机理

GNVC-VD 的核心创新在于将视频压缩的解码过程从逐帧独立重建重新定义为**基于视频扩散模型的序列级条件去噪**。与现有感知视频压缩方法依赖图像生成先验（如 Stable Diffusion）进行逐帧增强不同，GNVC-VD 引入预训练的视频扩散 Transformer（VideoDiT）作为原生视频先验，在时空潜在空间中对整个 I 帧和 P 帧序列进行联合优化。这一设计从三个关键维度改变了生成式视频压缩的范式。

### 从图像先验到视频先验的生成范式转变

现有生成式编解码器（如 **GLC-Video**（Qi et al., IEEE TCSVT 2025））依赖预训练图像生成模型逐帧增强解码帧，缺乏长程时序建模能力。这导致在极低码率下，虽然单帧纹理可能锐利，但帧间结构不稳定，产生严重的时序闪烁。GNVC-VD 将生成先验从图像模型替换为视频扩散 Transformer（VideoDiT），使解码器能够访问学习到的时空表示，从根本上解决了这一问题。如 Figure 2 所示，GLC-Video 的重建纹理随时间漂移和变化，而 GNVC-VD 保持了稳定的运动结构和一致的细节。

### 从纯噪声初始化到压缩感知部分噪声初始化

标准视频扩散模型的生成过程从纯高斯噪声开始，通过逐步去噪获得干净样本。GNVC-VD 改变了这一初始化策略：**从解码后的压缩潜在变量出发，仅注入部分噪声**（噪声水平 $t_N = 0.7$），然后通过流匹配进行优化。这一设计的直觉在于：解码后的潜在变量 $\mathbf{x}_c$ 已经包含了原始视频的大部分结构信息，只是因量化误差而丢失了精细纹理。从纯噪声开始会丢弃这些已编码的结构信息，而部分噪声初始化则允许扩散模型在保留结构的前提下，仅恢复压缩造成的退化。

形式上，初始状态定义为：
$$\mathbf{x}_{t_N} = t_N \mathbf{x}_c + (1 - t_N) \mathbf{x}_0$$

其中 $\mathbf{x}_c$ 为解码潜在变量，$\mathbf{x}_0$ 为高斯噪声。对应的速度场也被分解为预训练分量和微调校正项：
$$\mathbf{v}_\tau = \underbrace{(\mathbf{x}_1 - \mathbf{x}_0)}_{\mathbf{v}_{\mathrm{pre-train}}} - \underbrace{\frac{t_N}{1 - t_N}(\mathbf{x}_c - \mathbf{x}_1)}_{\Delta \mathbf{v}_{\mathrm{fine}}}$$

校正项 $\Delta \mathbf{v}_{\mathrm{fine}}$ 专门补偿压缩退化，由插入 VideoDiT 的条件适配器层估计。这一“预训练先验 + 压缩感知微调”的分解机制，使得视频扩散先验能够有效适配压缩域，而非简单地将生成模型用作后处理。

### 从逐帧独立增强到序列级联合优化

传统生成式编解码器对每一帧独立进行增强，忽略了帧间的时序依赖。GNVC-VD 的流匹配潜在优化模块直接在 3D 潜在空间中对整个 I 帧和 P 帧序列进行联合增强。通过将压缩域上下文特征注入 VideoDiT 的 Transformer 层，模型能够同时感知所有帧的时空信息，从而恢复时序一致的细节。Table 2 的定量结果表明，GNVC-VD 的 Warp Error（$E_{\mathrm{warp}}$）为 66.6，显著低于 GLC-Video 的 86.5，证实了序列级优化对时序稳定性的关键作用。

### 两阶段压缩感知训练策略

GNVC-VD 采用两阶段训练策略来有效对齐压缩编码器与扩散先验：

- **第一阶段（潜在对齐）**：在潜在空间中训练，损失函数结合码率 $R(\hat{y})$、潜在重建误差 $\|\tilde{\mathbf{x}}_1 - \mathbf{x}_1\|_2^2$ 和条件流匹配损失 $\mathcal{L}_{\mathrm{CFM}}$。这一阶段确保编码器输出的潜在变量与 VideoDiT 的输入分布对齐。
- **第二阶段（像素级微调）**：在像素空间中微调，引入 LPIPS 感知损失和潜在对齐项，进一步增强重建的感知质量。

消融实验（Table 4）证实，移除任一阶段均会导致 BD-LPIPS 和 BD-DISTS 的显著退化，其中移除第二阶段损失造成的性能下降最为严重，表明像素域的感知损失对最终质量至关重要。

### 小结

GNVC-VD 通过三个关键设计——视频原生扩散先验、压缩感知部分噪声初始化、序列级联合优化——系统性地解决了现有生成式视频压缩方法在极低码率下的时序闪烁和纹理不一致问题。这些创新使 GNVC-VD 在 LPIPS 和 DISTS 指标上全面超越传统编解码器（HEVC、VVC）、学习型编解码器（DCVC-FM、DCVC-RT）和生成式基线（GLC-Video），在 UVG 数据集上相对于 DCVC-RT 实现了 98% 的 DISTS BD-Rate 降低和 56% 的 LPIPS BD-Rate 降低。



GNVC-VD 的整体流水线围绕一个核心洞察构建：**将视频压缩的解码过程重新定义为基于视频扩散模型的序列级条件去噪**，而非独立的逐帧重建。如图 3 所示，框架由两大关键模块串联而成——Contextual Latent Codec（上下文潜在编解码器）与 VideoDiT-based Refinement Module（基于 VideoDiT 的优化模块）——辅以 3D 因果 VAE 编码器/解码器和熵编码环节，形成从原始视频到压缩码流再到高质量重建的完整闭环。

### 数据流与模块关系

**编码端**的数据流如下：

1. **3D Causal VAE Encoder**：输入视频 $V \in \mathbb{R}^{T \times H \times W \times 3}$ 首先经过预训练的 Wan2.1 3D 因果 VAE 编码器 $\mathcal{E}$，被压缩到时空潜在空间：
   $$\mathbf{x}_1 = \mathcal{E}(V), \quad \mathbf{x}_1 = \{ l_t \}_{t=1}^{1+T/4}$$
   其中时间维度下采样因子为 4，空间维度下采样因子为 8。这一步骤将视频从像素域转换到紧凑的潜在表示，为后续压缩和优化奠定基础。

2. **Contextual Latent Codec**：潜在序列 $\mathbf{x}_1$ 进入上下文潜在编解码器进行条件变换编码。该模块包含分析变换 $g_a$ 和合成变换 $g_s$，对每个潜在帧 $l_t$ 进行压缩：
   - **I 帧**（帧内编码帧）：独立编码，不依赖时序上下文。
   - **P 帧**（预测编码帧）：基于前一帧的上下文特征 $f_{t-1}$ 进行条件编码：
     $$\hat{y}_t = \operatorname{Quant}\bigl(g_a(l_t \mid f_{t-1})\bigr), \quad \hat{l}_t = g_s(\hat{y}_t, f_{t-1})$$
     其中 $f_{t-1}$ 从 $\hat{l}_{t-1}$ 中提取，并通过特征注入机制送入分析变换和合成变换，有效减少时空冗余。

3. **Entropy Coding**：量化后的潜在表示 $\hat{y}_t$ 经过无损熵编码，生成最终的压缩码流。

**解码端**的数据流则反向进行：

1. **Entropy Decoding**：从码流中恢复量化潜在表示 $\hat{y}_t$。

2. **Contextual Latent Decoder**：通过合成变换 $g_s$ 重建解码潜在序列 $\mathbf{x}_c = \{ \hat{l}_t \}_{t=1}^{1+T/4}$。由于量化误差 $\mathbf{e}$ 的存在，解码潜在变量可视为原始潜在变量的扰动版本：
   $$\mathbf{x}_c = \mathbf{x}_1 + \mathbf{e}$$

3. **VideoDiT-based Refinement Module**：这是 GNVC-VD 区别于以往方法的核心创新。与基于图像先验的生成式编解码器（如 GLC-Video）不同，GNVC-VD 直接在 **3D 潜在空间**中对整个 I 帧和 P 帧潜在序列进行联合优化：
   - **部分噪声初始化**：不从纯高斯噪声开始（如标准视频生成），而是从解码潜在变量 $\mathbf{x}_c$ 出发，注入部分高斯噪声至噪声水平 $t_N = 0.7$：
     $$\mathbf{x}_{t_N} = t_N \mathbf{x}_c + (1 - t_N) \mathbf{x}_0$$
     其中 $\mathbf{x}_0 \sim \mathcal{N}(0, 1)$。
   - **流匹配去噪**：通过 $L$ 步确定性流积分，逐步将 $\mathbf{x}_{t_N}$ 优化为干净的潜在序列 $\tilde{\mathbf{x}}_1$。每一步沿概率流路径 $\mathbf{x}_\tau$ 推进：
     $$\mathbf{x}_\tau = \frac{\tau - t_N}{1 - t_N} \mathbf{x}_1 + \frac{1 - \tau}{1 - t_N} \mathbf{x}_{t_N}$$
     目标速度场被分解为预训练分量和微调校正项：
     $$\mathbf{v}_\tau = \underbrace{(\mathbf{x}_1 - \mathbf{x}_0)}_{\mathbf{v}_{\text{pre-train}}} - \underbrace{\frac{t_N}{1 - t_N}(\mathbf{x}_c - \mathbf{x}_1)}_{\Delta \mathbf{v}_{\text{fine}}}$$
     其中 $\Delta \mathbf{v}_{\text{fine}}$ 补偿压缩退化，使扩散先验适配压缩域。
   - **条件适配器**：在 VideoDiT 的 Transformer 块中引入 Conditioning Adapter 层，将压缩域上下文特征 $\{ f_t \}$ 注入 DiT 中间层，用于估计校正项 $\Delta \mathbf{v}_{\text{fine}}$，从而实现压缩感知的条件去噪。

4. **3D Causal VAE Decoder**：优化后的潜在序列 $\tilde{\mathbf{x}}_1$ 通过 3D 因果 VAE 解码器 $\mathcal{D}$ 重建为最终视频：
   $$\tilde{V} = \mathcal{D}(\tilde{\mathbf{x}}_1)$$

### 关键设计选择

GNVC-VD 的框架设计体现了三个关键抉择，直接回应了现有方法的瓶颈：

| 设计维度 | 基线做法（图像先验路线） | GNVC-VD 做法 | 因果机制 |
|---------|----------------------|-------------|---------|
| **生成先验类型** | 预训练图像生成模型（如 Stable Diffusion） | 预训练视频扩散 Transformer（VideoDiT） | 原生视频先验具备长程时序建模能力，从根本上避免逐帧独立增强导致的时序不一致 |
| **优化粒度** | 逐帧独立增强 | 序列级联合优化 I 帧和 P 帧潜在变量 | 在 3D 潜在空间中同时考虑帧内和帧间关系，恢复一致的时空纹理 |
| **去噪初始化** | 从纯高斯噪声开始（标准生成过程） | 从解码潜在变量开始，添加部分噪声（$t_N = 0.7$） | 保留解码结果中的有效信息，仅对压缩退化部分进行定向修正，降低生成幻觉风险 |

### 训练策略

为有效对齐编码器与扩散先验，GNVC-VD 采用**两阶段压缩感知训练**：

- **第一阶段（潜在对齐）**：在潜在空间训练，损失函数结合码率 $R(\hat{y})$、潜在重建误差 $\|\tilde{\mathbf{x}}_1 - \mathbf{x}_1\|_2^2$ 和条件流匹配损失 $\mathcal{L}_{\text{CFM}}$：
  $$\mathcal{L}_{\text{latent}} = R(\hat{y}) + \lambda_r \|\tilde{\mathbf{x}}_1 - \mathbf{x}_1\|_2^2 + \mathcal{L}_{\text{CFM}}$$
  其中 $\mathcal{L}_{\text{CFM}}$ 使预测速度场逼近目标速度场：
  $$\mathcal{L}_{\text{CFM}} = \mathbb{E}_{\tau \sim \mathcal{U}[t_N,1], \mathbf{x}_\tau, \mathbf{x}_c} \left[ \| v_{\theta}(\mathbf{x}_\tau, \tau, \mathbf{x}_c) - \mathbf{v}_\tau \|_2^2 \right]$$

- **第二阶段（像素级微调）**：在像素空间端到端微调，引入 LPIPS 感知损失和潜在对齐项：
  $$\mathcal{L}_{\text{pixel}} = R(\hat{y}) + \lambda_r \Big( \| V - \tilde{V} \|_2^2 + \lambda_{\text{lpips}} \mathcal{L}_{\text{LPIPS}}(V, \tilde{V}) + \|\mathbf{x}_c - \mathbf{x}_1\|_2^2 + \|\tilde{\mathbf{x}}_1 - \mathbf{x}_1\|_2^2 \Big)$$

消融实验（Table 4）证实，移除任一训练阶段均会导致 BD-LPIPS 和 BD-DISTS 显著退化，其中第二阶段损失的影响最为严重，表明像素域感知损失对最终重建质量至关重要。

### 复杂度概览

GNVC-VD 的参数量主要集中于 VideoDiT 优化模块（约 21.5 亿参数，Table 6），整体模型约 23 亿参数。这带来了较高的解码延迟（1920×1080 分辨率下约 1557 ms，Table 7），是目前框架的主要局限之一，难以满足实时应用需求。

![[assets/figures/papers/paper_list_l879_https_arxiv_org_abs_2512_05016/figures/014_Table_6.jpg]]
*Table 6: Parameter count of each major module in the proposed GNVC-VD framework*

### 补充图表

![[assets/figures/papers/paper_list_l879_https_arxiv_org_abs_2512_05016/figures/003_Figure_3.jpg]]
*Figure 3: Overview of the proposed GNVC-VD framework. (a) Overall pipeline composed of two key modules: (b) a Contextual Latent Codec for spatio-temporal latent compression (Section 3.2), and (c) a VideoDiT-based refinement module that performs flow-matching latent refinement (Section 3.3)*



GNVC-VD 的核心架构由两大模块构成：**Contextual Latent Codec**（上下文潜在编解码器）和 **VideoDiT-based Refinement Module**（基于视频扩散 Transformer 的优化模块）。前者负责在时空潜在空间中进行条件变换编码，后者则利用预训练的视频扩散先验对解码后的潜在序列进行流匹配去噪优化。

### 3D 因果 VAE 编码

输入视频 $V \in \mathbb{R}^{T \times H \times W \times 3}$ 首先通过 Wan2.1 预训练的 3D 因果 VAE 编码器 $\mathcal{E}$ 映射到时空潜在空间：

$$\pmb{x}_1 = \pmb{\mathcal{E}}(V), \quad \pmb{x}_1 = \{ l_t \}_{t=1}^{1+T/4}$$

其中 $\pmb{x}_1$ 为潜在序列，时间维度下采样因子为 4（即每 4 帧对应 1 个潜在帧），空间维度下采样因子为 8×8。该 3D 因果编码器在压缩空间冗余的同时保留了帧间时序依赖关系，为后续序列级优化提供了紧凑的表示基础。

### 上下文潜在编解码器

对于 I 帧（帧内编码帧），其潜在变量 $l_t$ 通过分析变换 $g_a$ 直接编码为隐变量 $y_t$，经量化后由合成变换 $g_s$ 重建：

$$\hat{y}_t = \operatorname{Quant}\bigl(g_a(l_t)\bigr), \quad \hat{l}_t = g_s(\hat{y}_t)$$

对于 P 帧（预测编码帧），编码和解码均以前一帧的上下文特征 $f_{t-1}$ 为条件：

$$\hat{y}_t = \operatorname{Quant}\bigl(g_a(l_t \mid f_{t-1})\bigr), \quad \hat{l}_t = g_s(\hat{y}_t, f_{t-1})$$

其中上下文特征 $f_{t-1}$ 从上一帧的重建潜在变量 $\hat{l}_{t-1}$ 中提取，通过特征注入机制融合到分析变换和合成变换中。这种时序条件编码方式有效减少了帧间冗余，在极低码率下仍能保持基本的运动结构。量化后的隐变量 $\hat{y}_t$ 最终通过无损熵编码进一步压缩。

解码后的完整潜在序列记为 $\mathbf{x}_c = \{\hat{l}_t\}$，可视为原始潜在序列 $\mathbf{x}_1$ 与量化误差 $\mathbf{e}$ 的叠加：

$$\mathbf{x}_c = \mathbf{x}_1 + \mathbf{e}$$

这一残差视角为后续扩散优化模块的设计提供了理论出发点——优化的本质是学习一个校正项来补偿压缩引入的退化。

### 流匹配潜在优化

与标准视频生成中从纯高斯噪声 $\mathbf{x}_0 \sim \mathcal{N}(0, \mathbf{I})$ 开始去噪不同，GNVC-VD 的优化过程从解码后的潜在序列出发，注入部分噪声以获得初始状态：

$$\mathbf{x}_{t_N} = t_N \mathbf{x}_c + (1 - t_N) \mathbf{x}_0$$

其中 $t_N = 0.7$ 为部分噪声水平。这一设计使得去噪轨迹的起点靠近目标分布，大幅减少了所需的去噪步数，同时保留了扩散先验对细节的生成能力。

从 $\mathbf{x}_{t_N}$ 到干净潜在 $\mathbf{x}_1$ 的流匹配路径定义为线性插值：

$$\mathbf{x}_\tau = \frac{\tau - t_N}{1 - t_N} \mathbf{x}_1 + \frac{1 - \tau}{1 - t_N} \mathbf{x}_{t_N}$$

其中 $\tau \in [t_N, 1]$ 为流时间参数。对应的目标速度场可分解为两项：

$$\mathbf{v}_\tau = \underbrace{(\mathbf{x}_1 - \mathbf{x}_0)}_{\mathbf{v}_{\mathrm{pre-train}}} - \underbrace{\frac{t_N}{1 - t_N}(\mathbf{x}_c - \mathbf{x}_1)}_{\Delta \mathbf{v}_{\mathrm{fine}}}$$

第一项 $\mathbf{v}_{\mathrm{pre-train}}$ 是预训练 VideoDiT 已学习的标准生成速度场（从噪声到干净数据的流动方向）；第二项 $\Delta \mathbf{v}_{\mathrm{fine}}$ 是**压缩感知校正项**，用于补偿解码潜在 $\mathbf{x}_c$ 相对于原始潜在 $\mathbf{x}_1$ 的退化。通过引入轻量级条件适配器层（Conditioning Adapter）将压缩域上下文特征注入 DiT 的 Transformer 块中，网络学习估计这一校正项，从而使扩散先验适配到压缩重建场景。

最终的优化过程通过 $L$ 步确定性流积分完成：

$$\tilde{\mathbf{x}}_1 = \mathrm{VideoDiT}\big(\mathbf{x}_{t_N} \mid \{ f_t \}_{t=1}^{1+T/4} \big)$$

优化后的潜在序列 $\tilde{\mathbf{x}}_1$ 经 3D VAE 解码器重建为输出视频 $\tilde{V}$。

### 两阶段训练策略

训练分为两个阶段以逐步对齐压缩域与扩散先验。

**第一阶段（潜在对齐）** 的损失函数为：

$$\mathcal{L}_{\mathrm{latent}} = R(\hat{y}) + \lambda_r \|\tilde{\mathbf{x}}_1 - \mathbf{x}_1\|_2^2 + \mathcal{L}_{\mathrm{CFM}}$$

其中 $R(\hat{y})$ 为码率估计项，第二项约束优化后潜在与原始潜在的重建误差，$\mathcal{L}_{\mathrm{CFM}}$ 为条件流匹配损失：

$$\mathcal{L}_{\mathrm{CFM}} = \mathbb{E}_{\tau \sim \mathcal{U}[t_N,1], \mathbf{x}_\tau, \mathbf{x}_c} \left[ \| v_{\theta}(\mathbf{x}_\tau, \tau, \mathbf{x}_c) - \mathbf{v}_\tau \|_2^2 \right]$$

该损失使预测速度场 $v_{\theta}$ 逼近目标速度场 $\mathbf{v}_\tau$，从而在潜在空间中将编码器输出与扩散先验对齐。

**第二阶段（像素级微调）** 引入像素域感知约束：

$$\mathcal{L}_{\mathrm{pixel}} = R(\hat{y}) + \lambda_r \Big( \| V - \tilde{V} \|_2^2 + \lambda_{\mathrm{lpips}} \mathcal{L}_{\mathrm{LPIPS}}(V, \tilde{V}) + \|\pmb{x}_c - \pmb{x}_1\|_2^2 + \|\tilde{\pmb{x}}_1 - \pmb{x}_1\|_2^2 \Big)$$

该损失在码率约束下同时优化像素重建误差、LPIPS 感知损失以及潜在空间对齐项，使最终重建结果在感知质量和纹理一致性上达到最优。消融实验（Table 4）证实，移除任一阶段均会导致 BD-LPIPS 和 BD-DISTS 的显著退化，其中第二阶段损失的移除造成最严重的性能下降，表明像素域感知监督对最终质量至关重要。

### 补充图表

![[assets/figures/papers/paper_list_l879_https_arxiv_org_abs_2512_05016/figures/012_Figure_8.jpg]]
*Figure 8: Architecture of the Contextual Latent Codec module*



## 实验与关键发现

### 实验设置

GNVC-VD 在三个标准视频压缩基准数据集上进行评估：**HEVC-B**、**UVG** 和 **MCL-JCV**。所有方法均在极低码率区间（< 0.03 bpp）下测试，采用 RGB 色彩空间和低延迟配置。对于神经编解码器基线，使用相同的 GOP 大小（96 帧）和官方预训练权重。感知质量通过 **LPIPS** 和 **DISTS** 衡量，时序一致性通过 **Warp Error（E_warp）** 和 **CLIP-F** 评估。BD-Rate 计算以 VVC（VTM-17.0）为锚点。

### 主实验结果

#### 速率-失真性能

Figure 4 展示了三个数据集上的速率-失真曲线。**GNVC-VD 在 LPIPS 和 DISTS 指标上均达到了最佳的感知质量**，显著优于传统编解码器（HEVC、VVC）、学习型编解码器（DCVC-FM、DCVC-RT）以及生成式基线（GLC-Video）。在 UVG 数据集上，以 VVC 为锚点的 BD-Rate 对比（Table 3）显示：GNVC-VD 相比 DCVC-RT 在 DISTS 上实现了 **超过 98% 的码率节省**，在 LPIPS 上实现了 **56% 的码率节省**。

![[assets/figures/papers/paper_list_l879_https_arxiv_org_abs_2512_05016/figures/005_Figure_4.jpg]]
*Figure 4: Rate–distortion curves on the HEVC-B [9], UVG [36], and MCL-JCV [48] in the ultra-low bitrate regime (\< 0.03 bpp). We report perceptual quality in terms of LPIPS and DISTS in the ultra-low bitrate regime (\< 0.03 bpp). GNVC-VD consistently achieves the best perceptual quality, clearly outperforming traditional codecs (HEVC, VVC), learned codecs (DCVC-FM, DCVC-RT), and generative baselines (GLC-Video)*

![[assets/figures/papers/paper_list_l879_https_arxiv_org_abs_2512_05016/figures/010_Table_3.jpg]]
*Table 3: BD-Rate (%) comparisons anchoring by VVC [3]*

定性对比（Figure 5）进一步验证了这一优势：传统和学习型编解码器在极低码率下产生模糊帧，而 GNVC-VD 保留了更精细的结构纹理。

![[assets/figures/papers/paper_list_l879_https_arxiv_org_abs_2512_05016/figures/006_Figure_5.jpg]]
*Figure 5: Qualitative comparison across different codecs at ultra-low bitrates. Compared with traditional, learned, and prior generative codecs, GNVC-VD preserves finer structures. More visual examples are available in the Appendix Section C.5*

#### 时序一致性与语义连续性

Table 2 报告了 HEVC-B 上的时序一致性指标。GNVC-VD 的 Warp Error 为 **66.6**，显著低于 GLC-Video 的 **86.5**（降低约 23%），表明其低层次帧间对齐能力更强。同时，GNVC-VD 的 CLIP-F 达到 **0.982**，略高于 GLC-Video 的 0.979，证明其语义连续性也更优。

![[assets/figures/papers/paper_list_l879_https_arxiv_org_abs_2512_05016/figures/007_Table_2.jpg]]
*Table 2: Temporal consistency and semantic continuity comparison on HEVC-B. Lower*

Figure 2(b) 的逐帧 Warp Error 曲线进一步揭示了差异：GLC-Video 的 Warp Error 存在大幅波动，而 GNVC-VD 保持平稳，证实了其卓越的时序稳定性。Figure 6 的可视化对比直观展示了这一效果——GLC-Video 的纹理在不同帧之间漂移和变化，出现明显的时序闪烁，而 GNVC-VD 产生稳定、时序一致的重建结果。

![[assets/figures/papers/paper_list_l879_https_arxiv_org_abs_2512_05016/figures/002_Figure_2.jpg]]
*Figure 2: (a) Spatial and t–x comparisons. Traditional and learned codecs lose fine textures, while GLC-Video [38] exhibits sharp but unstable structures that cause temporal flickering. GNVC-VD preserves clean textures and stable motion. (b) Frame-wise warp error Ewarp further confirms GNVC-VD’s temporal stability, in contrast to the large fluctuations of GLC-Video*

![[assets/figures/papers/paper_list_l879_https_arxiv_org_abs_2512_05016/figures/001_Figure_1.jpg]]
*Figure 1: Qualitative comparison on ultra-low bitrate video compression. Traditional and learned codecs produce blurry frames. Generative approaches such as GLC-Video [38] yield sharper textures but introduce structural hallucinations and unstable details, causing pronounced temporal flickering (see Fig. 2). Leveraging a video-native diffusion prior, GNVC-VD produces coherent fine textures with strong temporal stability. Zoom in for best view*

![[assets/figures/papers/paper_list_l879_https_arxiv_org_abs_2512_05016/figures/008_Figure_6.jpg]]
*Figure 6: Visual comparison of temporal consistency. Groundtruth frames at*

### 消融实验

Table 4 报告了消融实验的定量结果（以完整模型为锚点，正值表示性能退化）：

![[assets/figures/papers/paper_list_l879_https_arxiv_org_abs_2512_05016/figures/011_Table_4.jpg]]
*Table 4: Ablation studies on BD-LPIPS↓ and BD-DISTS↓, anchoring by our full model. Negative values indicate improvements over the anchor, while positive values indicate degradations*

- **移除流匹配潜在优化模块（W/o Latent Refinement）**：BD-LPIPS 和 BD-DISTS 均出现显著正向退化，验证了序列级去噪优化对感知质量的关键作用。
- **移除第一阶段训练损失（W/o Stage I Loss）**：性能明显下降，说明潜在对齐损失对于建立编码器与扩散先验之间的有效连接不可或缺。
- **移除第二阶段训练损失（W/o Stage II Loss）**：造成**最严重的性能退化**，表明像素域的感知损失（LPIPS）对最终重建质量至关重要。

定性消融结果（Figure 7）与定量发现一致：无流匹配优化时结果过度平滑；移除第一阶段训练削弱了潜在-先验对齐，细节恢复能力下降；移除第二阶段训练限制了像素级适应性；完整模型始终恢复出最清晰的细节。

![[assets/figures/papers/paper_list_l879_https_arxiv_org_abs_2512_05016/figures/009_Figure_7.jpg]]
*Figure 7: Qualitative ablation results. We visualize the impact of each module in GNVC-VD. Without flow-matching refinement, results become over-smoothed; removing Stage I weakens latent–prior alignment and reduces detail reconstruction; removing Stage II limits pixel-level adaptation. The full model consistently restores sharper details, validating the effectiveness of all components*

### 复杂度与速度分析

Table 6 报告了各模块的参数量。GNVC-VD 总参数量约 **23 亿**，其中 VideoDiT 优化模块占 **21.5 亿**，构成主要的计算负担。Table 7 展示了在单张 A800 GPU 上的编解码速度：1920×1080 分辨率下解码延迟为 **1557 ms**，难以满足实时应用需求。这是当前框架的主要局限性之一——巨大的模型规模和扩散过程的多步推理导致了较高的解码延迟。

### 失败模式与局限性

1. **解码延迟高**：基于扩散的优化过程需要多步流积分（L 步），结合 VideoDiT 的 21.5 亿参数，导致解码速度远低于传统编解码器。
2. **序列长度限制**：当前实验仅测试了最大 GOP 长度为 25 帧的视频片段，对于更长视频或流媒体场景的扩展性尚未验证。
3. **训练复杂度**：两阶段训练策略依赖预训练的视频扩散模型，增加了计算资源和训练时间的需求。
4. **码率控制**：目前框架缺乏自适应码率控制机制，在可变带宽场景下的适用性有限。

> **注意**：关于更长序列的扩展性、自适应码率控制以及解码加速的具体方案，原文未提供详细实验验证，上述局限性基于论文自述的限制和开放问题总结，需在实际部署中进一步评估。



## 定位与知识库关联

### 1. 生成式视频压缩的方法演进

GNVC-VD 处于神经视频压缩（NVC）与生成模型交叉的前沿，其方法谱系可从三个维度追溯：

**传统与学习型编解码器**：传统混合编解码器 **HEVC**（Sullivan et al., IEEE TCSVT 2012）和 **VVC** 依赖手工设计的预测、变换和熵编码模块，在极低码率下产生模糊重建。学习型编解码器如 **DCVC-RT**（Li et al., NeurIPS 2021）和 **DCVC-FM**（Li et al., CVPR 2024）通过端到端优化提升了率失真性能，但训练目标以像素级保真度（如 MSE）为主，缺乏对感知质量和时序一致性的显式建模。

**基于图像先验的生成式编解码器**：**GLC-Video**（Qi et al., IEEE TCSVT 2025）和 **PLVC**（Yang et al., IJCAI 2022）代表了将预训练图像生成模型（如 Stable Diffusion）引入视频压缩的尝试。这类方法对每一帧独立应用图像先验进行增强，核心瓶颈在于缺乏长程时序建模能力——逐帧独立处理导致帧间纹理漂移和结构幻觉，表现为严重的时序闪烁（temporal flickering）。Figure 2 的逐帧 Warp Error 曲线清晰展示了 GLC-Video 的大幅波动（E_warp 86.5），而 GNVC-VD 将该指标降至 66.6。

**GNVC-VD 的定位**：GNVC-VD 是首个将原生视频扩散模型引入神经视频压缩的框架，其核心突破在于将解码过程重新定义为**序列级条件去噪**而非逐帧独立重建。这一转变的关键技术要素包括：

| 设计维度 | 图像先验方法（如 GLC-Video） | GNVC-VD |
|---------|---------------------------|---------|
| 生成先验类型 | 预训练图像生成模型 | 预训练视频扩散 Transformer（VideoDiT） |
| 优化粒度 | 逐帧独立增强 | 序列级联合优化 I 帧和 P 帧潜在变量 |
| 去噪初始化 | 从纯高斯噪声开始 | 从解码潜在变量开始，添加部分噪声（t_N=0.7） |
| 训练策略 | 端到端训练 | 两阶段压缩感知训练（潜在对齐 + 像素级微调） |

### 2. 关键技术贡献与因果机制

GNVC-VD 的因果调节变量（causal knob）可分解为三个相互依赖的机制：

**（1）部分噪声初始化策略**：与传统扩散生成从纯高斯噪声开始不同，GNVC-VD 从解码后的时空潜在变量 $\mathbf{x}_c$ 出发，仅在噪声水平 $t_N=0.7$ 处注入部分噪声，形成初始状态 $\mathbf{x}_{t_N} = t_N \mathbf{x}_c + (1 - t_N) \mathbf{x}_0$。这一设计的因果逻辑在于：解码潜在变量已保留了视频的粗粒度结构，完全从噪声开始会丢弃这些压缩域信息；部分噪声初始化使扩散模型专注于恢复压缩损失的精细纹理，而非从头生成内容。

**（2）速度场校正项**：目标速度场被显式分解为预训练分量和微调校正项：
$$\mathbf{v}_\tau = \underbrace{(\mathbf{x}_1 - \mathbf{x}_0)}_{\mathbf{v}_{\mathrm{pre-train}}} - \underbrace{\frac{t_N}{1 - t_N}(\mathbf{x}_c - \mathbf{x}_1)}_{\Delta \mathbf{v}_{\mathrm{fine}}}$$
其中 $\Delta \mathbf{v}_{\mathrm{fine}}$ 补偿压缩退化（$\mathbf{x}_c - \mathbf{x}_1$ 即量化误差 $\mathbf{e}$），使扩散先验能够适应压缩域的特征分布。

**（3）条件适配器注入**：通过将压缩域上下文特征 $\{f_t\}$ 注入 VideoDiT 的 Transformer 中间层，条件适配器层估计校正项 $\Delta \mathbf{v}_{\mathrm{fine}}$，实现了压缩条件与扩散先验的有效融合。

消融实验（Table 4）为上述机制提供了因果证据：移除流匹配潜在优化模块导致 BD-LPIPS 和 BD-DISTS 显著增加；移除第一阶段潜在对齐损失削弱了编码器与扩散先验的对齐；移除第二阶段像素级微调损失造成最严重的性能退化，表明像素域感知损失对最终重建质量至关重要。

### 3. 适用边界与局限

**计算与延迟约束**：GNVC-VD 的模型参数量达 23 亿，其中 VideoDiT 模块占 21.5 亿参数。在单张 A800 GPU 上，1920×1080 分辨率视频的解码延迟为 1557 ms（Table 7），难以满足实时或低延迟应用需求。这一局限源于扩散模型固有的多步采样机制（L 步确定性流积分）。

**序列长度限制**：当前实验仅测试了较短的视频片段（最大 GOP 长度为 25 帧），对于更长视频或流媒体场景的扩展性尚未验证。VideoDiT 的时空注意力机制在长序列上的计算复杂度可能成为瓶颈。

**训练复杂度**：两阶段训练策略（潜在对齐 + 像素级微调）虽然有效，但增加了训练流程的复杂性和资源需求，且依赖于预训练的视频扩散模型（Wan2.1 的 3D Causal VAE 和 VideoDiT）。

**率失真权衡**：GNVC-VD 在感知质量指标（LPIPS、DISTS）上表现优异，但在像素保真度指标（PSNR、MS-SSIM）上可能不如传统编解码器（Figure 9），这反映了感知-失真权衡的固有限制。

### 4. 开放问题与未来方向

基于当前工作的局限，以下方向值得进一步探索：

1. **效率优化**：如何加速基于扩散的优化过程以降低解码延迟？可能的路径包括蒸馏、步数压缩、或采用一致性模型等少步采样方法。

2. **上下文变换编码增强**：当前的 Contextual Latent Codec 模块相对轻量，如何进一步提升其编码效率，使其更好地与扩散先验协同？

3. **长视频与自适应码率**：如何将序列级优化扩展到更长的视频序列？能否实现自适应码率控制，使框架在不同码率约束下灵活调整优化强度？

4. **条件注入机制**：是否存在更有效的方式将压缩域上下文特征注入扩散模型？例如，交叉注意力或特征调制等替代方案可能进一步提升恢复质量。

5. **更广泛的视频内容**：当前评估集中在自然场景视频，对于屏幕内容、医学影像、监控视频等特殊域视频的泛化性需要进一步验证。



## 原文 PDF

![[paperPDFs/CVPR_2026/Generative_Neural_Video_Compression_via_Video_Diffusion_Prior.pdf]]
