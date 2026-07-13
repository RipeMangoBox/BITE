---
title: "BWCache: Accelerating Video Diffusion Transformers through Block-Wise Caching"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/BWCache_Accelerating_Video_Diffusion_Transformers_through_Block_Wise_Caching.pdf
project_link: null
code_link: https://github.com/hsc113/BWCache
aliases:
- BWCB
- BWCache
- "Block-Wise Caching (BWCache)"
tags:
- ICLR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: "BWCache按DiT块缓存相邻时间步高度相似的块输出特征以跳过冗余视频扩散计算。"
primary_logic: "相对L1相似性低于阈值后触发缓存，后续按周期重计算并在最终时间步保护生成质量。"
claims:
- "视频DiT块特征在扩散中间时间步呈稳定相似的U形变化模式。"
- "块级缓存比时间步级或注意力级缓存更细粒度地利用冗余。"
- "BWCache在Open-Sora、Latte、Wan和HunyuanVideo等模型上获得显著加速且基本保持VBench质量。"
---

# BWCache: Accelerating Video Diffusion Transformers through Block-Wise Caching

> [!tip] 核心洞察
> DiT块特征在扩散时间步上呈现U形变化模式，中间时间步高度相似，因此可以安全地缓存和重用，从而消除冗余计算。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | BWCache：通过逐块缓存加速视频扩散Transformer |
| 英文题名 | BWCache: Accelerating Video Diffusion Transformers through Block-Wise Caching |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=5bJZtzTFYy) · [GitHub](https://github.com/hsc113/BWCache) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/image_and_video_generation |
| Method | Block-Wise Caching (BWCache) |
| Dataset | Open-Sora (51帧, 480P), Open-Sora-Plan (65帧, 512×512) |

> [!tip] 效果简介
> - Open-Sora (51帧, 480P) 上，Speedup 为 1.61×，对比 1.0× (原始)，变化 +0.61×。
> - Open-Sora (51帧, 480P) 上，VBench 为 80.03%，对比 80.12% (原始)，变化 -0.09%。
> - Open-Sora-Plan (65帧, 512×512) 上，Speedup 为 2.24×，对比 1.0× (原始)，变化 +1.24×。

## 概要

本文提出**BWCache (Block-Wise Caching)**，一种无需训练的即插即用方法，用于加速基于DiT (Diffusion Transformer) 的视频生成模型。核心思想是：在扩散时间步上，DiT块的特征变化呈现**U形模式**——中间时间步的特征高度相似，因此可以安全地缓存并重用这些块特征，从而消除冗余计算。BWCache通过一个基于相邻时间步块特征差异的相似性指标，动态决定是否触发缓存重用，并采用周期性重计算策略缓解潜在漂移。实验表明，BWCache在多个主流视频DiT模型（Open-Sora、Open-Sora-Plan、Latte、Wan 2.1、HunyuanVideo）上，在保持可比视觉质量的同时，实现了最高**2.6倍**的加速。



### 2.1 视频扩散Transformer的推理瓶颈

基于DiT的视频生成模型（如Open-Sora、HunyuanVideo）在推理时面临巨大的计算开销。分析表明，**DiT块是推理延迟的主要贡献者**（"Our analysis reveals that DiT blocks are the primary contributors to inference latency."），且其计算时间占比随视频长度和分辨率增加而上升（Figure 4(b)）。现有加速方法主要分为两类：

- **架构修改类**：如Skip-DiT (Chen et al., 2025)，需要修改模型架构并重新训练，部署成本高。
- **缓存类**：如DeepCache (Ma et al., 2023)、TeaCache (Liu et al., 2024)、PAB (Zhao et al., 2024b)，但存在缓存粒度粗（时间步级）或仅针对注意力层的问题，导致质量损失或加速有限。

### 2.2 关键观察：DiT块特征的U形变化模式

通过对五种视频DiT模型（Open-Sora、Open-Sora-Plan、Latte、Wan 2.1、HunyuanVideo）的块特征变化进行定量分析（Figure 5），作者发现：

- **U形模式**：在扩散过程的早期和最终时间步，块特征变化剧烈；而在中间时间步，特征变化极小，呈现高度相似性。
- **一致性**：该模式在五种模型中一致出现，表明这是视频DiT模型的固有特性。
- **理论依据**：该模式可通过频域分析（Qian et al., 2024）得到理论解释——早期步骤主要恢复低频结构，中间步骤细化高频细节，因此特征变化较小。

这一观察为**逐块缓存**提供了核心动机：中间时间步的块特征可以安全地缓存和重用，从而消除大量冗余计算。



## 核心方法与创新机理

BWCache的核心创新可概括为四个关键设计维度：

| 设计维度 | 基线方法 | BWCache的改进 | 证据 |
|---------|---------|--------------|------|
| **缓存粒度** | 时间步级（TeaCache）或注意力层级（PAB） | **DiT块级**：缓存整个DiT块的输出特征 | "The core idea is to cache the features from all DiT blocks at certain diffusion timesteps and reuse them across several subsequent steps." |
| **缓存触发机制** | 固定间隔或基于时间步嵌入 | **动态相似性指标**：基于相邻时间步块特征的相对L1距离，低于阈值时触发 | "we introduce a similarity indicator that triggers feature reuse only when the differences between block features at adjacent timesteps fall below a threshold" |
| **缓存更新策略** | 无周期性重计算或固定重计算 | **周期性重计算**：每R步重计算一次块特征，防止潜在漂移 | "Periodic recomputation is applied to mitigate potential latent drift." |
| **最终时间步处理** | 无特殊处理 | **最后k/2步始终重计算**：缓存触发后，后半部分步骤不进行重用 | "Once BWCache is triggered at the k-th step, caching reuse is restricted to the first half of the remaining steps, while the second half is explicitly computed." |




![[assets/figures/papers/iclr26_vision_multimodal_applications__image_and_video_generation__b001_5bJZtzTFYy_BWCache_Accel/figures/001_Figure_1.jpg]]

BWCache的整体流程如Figure 2所示：

1. **相似性指标计算**：在每个时间步t，计算所有N个DiT块在相邻时间步t和t+1之间的平均相对L1距离。
2. **缓存触发判断**：若平均相对L1距离低于阈值δ，则触发缓存模式。
3. **块特征缓存与重用**：缓存当前时间步所有DiT块的输出特征，在后续R个时间步中直接重用这些缓存特征，跳过DiT块的计算。
4. **周期性重计算**：每R步后，重新计算一次块特征并更新缓存，防止累积误差导致的潜在漂移。
5. **最终时间步保护**：缓存触发后，最后k/2个时间步始终进行完整计算，确保生成质量。



### 5.1 扩散过程与DiT块

**前向扩散过程**（Eq.(1)）：
$$q(\mathbf{x}_t | \mathbf{x}_{t-1}) := \mathcal{N}(\mathbf{x}_t; \sqrt{1-\beta_t} \mathbf{x}_{t-1}, \beta_t I)$$

**反向扩散过程**（Eq.(2)）：
$$p_\theta(\mathbf{x}_{t-1} | \mathbf{x}_t) := \mathcal{N}(\mathbf{x}_{t-1}; \mu_\theta(\mathbf{x}_t, t), \Sigma_\theta(\mathbf{x}_t, t))$$

**DiT块结构**（Figure 3）：每个DiT块包含两个子层，均带有残差连接：

- **注意力子层输出**（Eq.(3)）：$h_{t,i}' = \mathrm{Attention}(\mathrm{AdaLN}(h_{t,i})) + h_{t,i}$
- **MLP子层输出**（Eq.(4)）：$h_{t,i}'' = \mathrm{MLP}(\mathrm{AdaLN}(h_{t,i}')) + h_{t,i}'$

其中AdaLN (Adaptive Layer Normalization) 根据时间步t调节归一化参数。

### 5.2 相似性指标

**相对L1距离**（Eq.(5)）：衡量块i在相邻时间步t和t+1之间的特征变化：
$$\mathrm{L1}_{\mathrm{rel}}(h_{t,i}) = \frac{\|h_{t,i} - h_{t+1,i}\|_1}{\|h_{t+1,i}\|_1}$$

**聚合相对L1距离**（Eq.(6)）：时间步t上所有N个DiT块的相对L1距离之和：
$$\mathrm{ARL1}(t) = \sum_{n=1}^N \mathrm{L1}_{\mathrm{rel}}(h_{t,i})$$

**BWCache相似性指标**（Eq.(7)）：触发缓存的条件——平均相对L1距离低于阈值δ：
$$\sum_{n=1}^N \mathrm{L1}_{\mathrm{rel}}(h_{t,i}) / N < \delta$$

### 5.3 缓存重用与周期性重计算

**周期性缓存重计算输出**（Eq.(8)）：DiT块在所有步骤上的输出序列，每R步进行一次重计算：
$$\mathcal{O}_H = \{\ldots, \underbrace{h_t''}_{\mathrm{cached}}, \underbrace{h_t'', \ldots, h_t''}_{\mathrm{reuse}\ R\ \mathrm{steps}}, \underbrace{h_{t-R-1}''}_{\mathrm{cached}}, \cdot\cdot\cdot\}$$

### 5.4 评估指标

- **PSNR**（Appendix C）：$\mathrm{PSNR} = 10 \cdot \log_{10} \left( \frac{R^2}{\mathrm{MSE}} \right)$，衡量重建质量，越高越好。
- **LPIPS**（Appendix C）：$\mathrm{LPIPS}(I, K) = \frac{1}{L} \sum_{l=1}^L \| \phi_l(I) - \phi_l(K) \|^2$，基于深度学习特征的感知相似度，越低越相似。
- **SSIM**（Appendix C）：$\mathrm{SSIM}(I, K) = \frac{(2\mu_I\mu_K + C_1)(2\sigma_{IK} + C_2)}{(\mu_I^2 + \mu_K^2 + C_1)(\sigma_I^2 + \sigma_K^2 + C_2)}$，评估亮度、对比度和结构，越高越好。



## 实验与关键发现


### 6.1 主要结果

**Table 1** 展示了BWCache在五种视频DiT模型上的单GPU性能：


![[assets/figures/papers/iclr26_vision_multimodal_applications__image_and_video_generation__b001_5bJZtzTFYy_BWCache_Accel/figures/017_Table_1.jpg]]
*Table 1: Table 1: Comparison of visual quality and efficiency on a single GPU. Video generation specifications: Open-Sora (51 frames, 480P), Open-Sora-Plan (65 frames, 512×512), Latte (16 frames, 512×512), Wan 2.1 (81 frames, 480P), HunyuanVideo (129 frames, 544P). LPIPS, SSIM, and PSNR are calculated against the original model results.*

| 模型 | 分辨率/帧数 | 加速比 | VBench | LPIPS↓ | SSIM↑ | PSNR↑ |
|------|-----------|-------|--------|--------|-------|-------|
| Open-Sora | 51帧, 480P | **1.61×** | 80.03% | 0.0879 | 0.8854 | 27.05 |
| Open-Sora-Plan | 65帧, 512×512 | **2.24×** | 80.82% | 0.1001 | 0.8435 | 25.87 |
| Latte | 16帧, 512×512 | **1.90×** | 78.28% | 0.1399 | 0.8181 | 26.46 |
| Wan 2.1 | 81帧, 480P | **2.00×** | 81.99% | 0.0782 | 0.8539 | 25.86 |
| HunyuanVideo | 129帧, 544P | **2.60×** | 82.48% | 0.0794 | 0.8903 | 29.91 |

关键发现：
- BWCache在所有模型上均实现了显著加速，同时VBench分数与原始模型几乎持平（最大差异仅-0.09%）。
- 在HunyuanVideo上达到最高加速比2.60×，且VBench甚至提升了0.34%。
- **Figure 1** 的质量-延迟曲线显示，BWCache在视觉质量和效率上均显著优于PAB和TeaCache。

### 6.2 消融实验

**缓存机制 vs. 减少推理步数**（Table 3, Figure 8）：

![[assets/figures/papers/iclr26_vision_multimodal_applications__image_and_video_generation__b001_5bJZtzTFYy_BWCache_Accel/figures/026_Table_3.jpg]]

- 在相近延迟下，BWCache的LPIPS (0.0879) 远低于30步推理的LPIPS (0.1399)，证明缓存机制优于单纯减少步数。

**重用率影响**（Table 4）：

![[assets/figures/papers/iclr26_vision_multimodal_applications__image_and_video_generation__b001_5bJZtzTFYy_BWCache_Accel/figures/029_Table_4.jpg]]
*Table 4: Table 4: Impact of different reuse rates.*

- 默认重用率41.38%（阈值δ=0.15）在质量和速度之间取得最佳平衡。

**重用间隔影响**（Table 5）：

![[assets/figures/papers/iclr26_vision_multimodal_applications__image_and_video_generation__b001_5bJZtzTFYy_BWCache_Accel/figures/030_Table_5.jpg]]
*Table 5: Table 5: Impact of different reuse intervals.*

- 默认重用间隔10%总步数在质量和速度之间取得最佳平衡。

**最终步数影响**（Table 9）：
- 默认最后1/2k步不进行缓存重用，平衡了生成质量和延迟。

**统计显著性**（Table 10）：
- BWCache在统计上显著优于PAB和TeaCache（p < 0.05）。

### 6.3 扩展能力

**多GPU扩展**（Table 2, Figure 7）：

![[assets/figures/papers/iclr26_vision_multimodal_applications__image_and_video_generation__b001_5bJZtzTFYy_BWCache_Accel/figures/025_Table_2.jpg]]
*Table 2: Table 2: Inference efficiency when scaling to multiple GPUs with DSP.*

- 使用Dynamic Sequence Parallelism (DSP) (Zhao et al., 2024a) 扩展到8个GPU时，Open-Sora 204帧480P视频的延迟降至11.08秒，实现17.16×加速。

**不同视频长度和分辨率**（Figure 7）：
- BWCache在不同视频长度（51-221帧）和分辨率（480P-720P）下均保持稳定的加速效果。

### 6.4 与高内存缓存方法对比

**Table 7** 显示，在缩短视频长度下，BWCache在视觉质量（LPIPS、SSIM、PSNR）上显著优于ProfilingDiT和TaylorSeer，同时保持有竞争力的加速比和更低的内存开销。

### 6.5 内存使用

**Table 11** 显示，BWCache的内存使用（Open-Sora 51帧480P：21362 MiB）低于PAB（27016 MiB），与TeaCache（20630 MiB）相当。

### 6.6 动态视频生成

**Table 14** 显示，BWCache在动态视频生成场景中保持有竞争力的视觉质量，VBench分数与原始模型接近。

### 6.7 公平性说明

- 所有实验在单个NVIDIA A800 GPU上进行。
- 所有基线方法使用其官方实现和推荐配置。
- LPIPS、SSIM和PSNR均相对于原始模型结果计算。
- FlashAttention (Dao et al., 2022) 在所有实验中默认启用。



## 定位与知识库关联

### 7.1 与现有缓存方法的关系

BWCache在缓存方法谱系中占据独特位置：

| 方法 | 缓存粒度 | 是否需要训练 | 内存开销 | 适用场景 |
|------|---------|------------|---------|---------|
| DeepCache (Ma et al., 2023) | 层级（高层特征） | 否 | 低 | 图像生成 |
| TeaCache (Liu et al., 2024) | 时间步级 | 否 | 低 | 视频生成 |
| PAB (Zhao et al., 2024b) | 注意力层级 | 否 | 中 | 视频生成 |
| Skip-DiT (Chen et al., 2025) | 块级（长跳跃连接） | 是 | 低 | 视频生成 |
| ProfilingDiT (Ma et al., 2025b) | 时间步级 | 否 | 高 | 视频生成 |
| TaylorSeer (Liu et al., 2025b) | 时间步级 | 否 | 高 | 视频生成 |
| **BWCache (本文)** | **DiT块级** | **否** | **低** | **视频生成** |

### 7.2 核心优势

1. **无需训练**：作为即插即用组件，可直接集成到现有DiT模型中。
2. **细粒度缓存**：块级缓存比时间步级缓存更灵活，能根据提示内容自适应调整（Figure 10）。
3. **低内存开销**：仅需缓存当前时间步的块特征，无需存储大量中间特征。
4. **动态自适应**：基于特征差异的相似性指标，自动适应不同模型和提示。

### 7.3 局限性

- **潜在漂移**：缓存重用可能导致累积误差，使特征变化偏离预期的U形轨迹（Figure 14）。
- **指标计算开销**：缓存指标的计算占总推理时间的10.6%至22.5%（Table 13）。
- **模型适配**：在Wan 2.1和HunyuanVideo等使用全3D自注意力的模型中，需要选择性地使用部分块进行指标计算以保持效率。
- **任务差异**：在文本到图像和类别条件生成中呈现倒L形模式（Figure 12, 13），与视频生成的U形模式不同，表明其在不同任务中的适用性可能不同。

### 7.4 开放问题

1. BWCache在更广泛的视频生成任务（如长视频、高分辨率、复杂场景）中的表现如何？
2. 如何进一步减少缓存指标的计算开销？
3. BWCache是否可以与其他加速技术（如蒸馏、量化）结合以获得更大的加速效果？
4. BWCache在图像生成和类别条件生成任务中的适用性如何？
5. 如何更有效地解决缓存重用导致的潜在漂移问题？



## 原文 PDF

![[paperPDFs/ICLR_2026/BWCache_Accelerating_Video_Diffusion_Transformers_through_Block_Wise_Caching.pdf]]
