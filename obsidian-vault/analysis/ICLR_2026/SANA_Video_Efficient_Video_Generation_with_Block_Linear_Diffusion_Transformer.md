---
title: "SANA-Video: Efficient Video Generation with Block Linear Diffusion Transformer"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/SANA_Video_Efficient_Video_Generation_with_Block_Linear_Diffusion_Transformer.pdf
project_link: https://nvlabs.github.io/Sana/Video/
code_link: null
openreview_forum_id: mzAchylAtf
aliases:
- SV
- SANA-Video
tags:
- ICLR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: "将自注意力全面替换为线性注意力并设计因果块线性注意力及恒定内存KV缓存，在保持全局感受野的同时实现O(N)复杂度与长视频高效生成。"
primary_logic: "线性注意力具有可累积的状态表示，通过缓存累积状态与键和，可将逐token计算成本与内存固定为O(D²)，支持长视频自回归生成；结合RoPE增强局部性和时空混合卷积提升运动连续性。"
claims:
- "线性注意力复杂度降为O(N)，在720p视频上实现4倍加速。"
- "块因果线性注意力的恒定内存KV缓存避免传统KV缓存随序列长度增长，支持分钟级长视频生成。"
- "RoPE后于ReLU激活并移除分母中的RoPE，保证训练稳定并形成稀疏局部注意力模式。"
- "增加1D时间卷积到Mix-FFN，有效降低训练损失并提升运动质量。"
---

# SANA-Video: Efficient Video Generation with Block Linear Diffusion Transformer

> [!tip] 核心洞察
> 线性注意力具有可累积的状态表示，通过缓存累积状态与键和，可将逐token计算成本与内存固定为O(D²)，支持长视频自回归生成；结合RoPE增强局部性和时空混合卷积提升运动连续性。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | SANA-Video：基于块线性扩散变换器的高效视频生成 |
| 英文题名 | SANA-Video: Efficient Video Generation with Block Linear Diffusion Transformer |
| 会议/期刊 | ICLR 2026 (Oral) |
| Links | [paper](https://openreview.net/forum?id=mzAchylAtf) · [Project](https://nvlabs.github.io/Sana/Video/) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/image_and_video_generation |
| Method | SANA-Video |
| Dataset | VBench (480×832×81, T2V), VBench (T2V), VBench (I2V) |

> [!tip] 效果简介
> - VBench (480×832×81, T2V) 上，Latency (s) 为 60，对比 484 (Wan2.1-14B)，变化 8.1× faster。
> - VBench (T2V) 上，Total Score 为 83.71，对比 83.31 (Wan2.1-1.3B)，变化 +0.40。
> - VBench (I2V) 上，Total Score 为 88.02，对比 86.86 (Wan2.1-14B)，变化 +1.16。

## 概要

视频生成模型长期受限于Transformer自注意力的$O(N^2)$计算复杂度——随着空间分辨率提升和视频帧数增加，token数量急剧膨胀，使得高分辨率长视频的生成在计算与内存上均成为瓶颈。**SANA-Video**针对这一核心矛盾，提出以**线性注意力全面替代标准Softmax注意力**的架构方案，将复杂度降至$O(N)$，并在保持全局感受野的前提下，通过**块因果线性注意力与恒定内存KV缓存**实现长视频的高效自回归生成。

该方法的核心洞察在于：线性注意力天然具备可累积的状态表示——通过缓存累积注意状态$\phi(K_j)^T V_j$与键和$\phi(K_j)^T$，可将逐token的计算与内存成本固定为$O(D^2)$，从而在推理时避免传统KV缓存随序列长度线性增长的内存压力。围绕这一基础，SANA-Video进一步引入三项关键设计：（1）将**3D RoPE**置于ReLU激活之后并从分母移除，在保证训练稳定的同时形成稀疏的局部注意力模式；（2）在Mix-FFN中增加**1D时间卷积**，增强局部时空建模与运动连续性；（3）采用**单调递增SNR采样器**与基于全局缓存的**自forcing长训练策略**，缓解自回归生成中的曝光偏差问题。

在效率与性能的平衡上，SANA-Video展现出显著优势：在单张H100 GPU上生成5秒720p视频仅需**36秒**，相较Wan2.1-14B实现**53倍加速**；在480p分辨率下，VBench T2V总分**83.71**（超越Wan2.1-1.3B的83.31），I2V总分**88.02**（超越Wan2.1-14B的86.86），同时语义对齐分数分别领先**5.70**和**3.50**分。模型训练成本仅为12天×64张H100 GPU，约为同规模模型的1%。配合NVFP4量化，RTX 5090上5秒720p视频生成进一步降至**29秒**，使消费级硬件上的实时视频生成成为可能。



视频生成领域正经历从图像扩散模型到视频扩散模型的快速迁移，但这一迁移面临一个根本性的计算瓶颈：传统Transformer架构中自注意力机制的计算与内存复杂度为$O(N^2)$（$N$为序列token数）。在视频生成场景下，$N$随帧数、空间分辨率和时间维度的增加而急剧膨胀——例如一段720p、81帧的视频可产生数十万量级的token——使得全注意力机制成为高分辨率长视频生成的核心障碍。

现有主流方法对此问题的应对策略可分为两类。一类是保持全注意力但采用级联或稀疏化策略，如**Wan2.1**（Wang et al., 2025a）、**CogVideoX**（Yang et al., 2024）等模型，它们在高分辨率下仍面临显著的推理延迟与内存压力。另一类是采用局部注意力窗口或状态压缩的轻量化方案，如**LTX-Video**（HaCohen et al., 2024），但这些方法往往牺牲了全局感受野，限制了长程时空一致性的建模能力。当前SOTA模型在生成5秒720p视频时，单张H100 GPU上的推理延迟可达数百甚至上千秒（如Wan2.1-14B需1897秒），且KV缓存内存随序列长度线性增长，使得分钟级长视频的自回归生成在工程上几乎不可行。

线性注意力（linear attention）为上述困境提供了理论突破口。其核心性质在于：注意力状态可以被累积表示为固定维度的矩阵，从而将逐token的计算与内存成本从$O(N)$降至$O(D^2)$（$D$为特征维度），实现恒定内存占用。然而，直接将线性注意力应用于视频扩散Transformer面临三个关键挑战：

1. **位置信息缺失**：线性注意力缺乏内置的位置感知能力，而视频数据具有强烈的时空局部性，需要有效的位置编码来引导注意力聚焦。
2. **训练不稳定性**：线性注意力的分母项在引入旋转位置编码（RoPE）后可能变为零或负值，导致训练崩溃。
3. **自回归曝光偏差**：在长视频块自回归生成中，标准随机时间步采样无法有效模拟推理时的去噪分布，造成生成质量随视频长度增加而退化。

本文提出**SANA-Video**，旨在通过系统性地将线性注意力适配到视频扩散Transformer中，实现高效且高质量的视频生成。其核心动机是：在保持全局感受野的前提下，将自注意力全面替换为线性注意力，并结合稳定的RoPE集成策略、时空混合卷积以及恒定内存KV缓存机制，将复杂度降至$O(N)$，从而支持高分辨率长视频的高效生成。该方法在720p视频上实现4倍加速，推理延迟相比Wan2.1-14B降低53倍（36秒 vs. 1897秒），同时保持有竞争力的生成质量。



## 核心方法与创新机理

SANA-Video 的核心创新在于将视频扩散变换器的注意力机制从传统 Softmax 自注意力全面替换为**线性注意力**，并围绕这一操作设计了一整套支持高效长视频生成的架构与训练策略。其关键改动（changed slots）可归纳为以下五个维度：

### 1. 注意力机制：从 Softmax 自注意力到带 RoPE 的线性注意力

传统 DiT 中的 Softmax 自注意力具有 $O(N^2)$ 的计算与内存复杂度，当视频 token 数量 $N$ 随分辨率和帧数增长时，迅速成为瓶颈。SANA-Video 将所有注意力模块替换为**线性注意力**，将复杂度降至 $O(N)$，在 720p 视频上实现 4 倍加速（Sec. 1, Fig. 5(c)）。

线性注意力的核心操作为：

$$O_i = \frac{\mathsf{RoPE}(\phi(Q_i)) \left(\sum_{j=1}^N \mathsf{RoPE}(\phi(K_j))^T V_j\right)}{\phi(Q_i) \left(\sum_{j=1}^N \phi(K_j)^T\right)}$$

其中 $\phi(\cdot)$ 为 ReLU 激活函数。与标准线性注意力不同，SANA-Video 做出了两项关键设计（Sec. 3.2, Fig. 3）：

- **RoPE 后置于 ReLU**：将旋转位置编码（RoPE）应用于 $\phi(Q)$ 和 $\phi(K)$ 之后，而非之前。这使注意力图呈现出更稀疏、更局部的模式，增强了模型对邻近 token 的关注能力。
- **分母移除 RoPE**：在分母的键求和中不使用 RoPE，仅使用 $\phi(K_j)$。这保证了分母始终为正，避免了训练过程中因分母趋近于零导致的数值不稳定（Fig. 3(b) 绿线验证了训练稳定性）。

### 2. 前馈网络：引入 1D 时间卷积形成时空混合 FFN

原始 SANA 的 Mix-FFN 仅包含 2D 空间卷积。SANA-Video 在其末端追加了一个带捷径连接的 **1D 时间卷积层**，形成 **Spatial-Temporal Mix-FFN**（Fig. 2(b)）。消融实验表明，该设计显著降低了训练损失并提升了运动质量（Fig. 5(a)(b), Table 5）。

### 3. 长视频缓存：块线性注意力与恒定内存 KV 缓存

为支持自回归长视频生成，SANA-Video 提出了**块线性注意力**机制（Sec. 3.3, Fig. 4）。其核心思想是利用线性注意力的可累积性质，将逐 token 计算重新表述为：

$$O_i = \frac{\phi(Q_i) \left( \sum_{j=1}^{i-1} S_j + S_i \right)}{\phi(Q_i) \left( \sum_{j=1}^{i-1} \phi(K_j)^T + \phi(K_i)^T \right)}$$

其中 $S_j = \phi(K_j)^T V_j$ 为累积注意状态。该公式将每个新 token 的计算与内存成本固定为 $O(D^2)$（$D$ 为特征维度），而非随序列长度 $N$ 线性增长的 $O(N)$ 传统 KV 缓存（Table 1）。这使得模型可以在恒定 GPU 内存下生成长达分钟级的视频。

同时，**Block Causal Mix-FFN** 通过零填充和缓存前一 block 的最后一帧，保证了块间因果性，防止信息泄露。

### 4. 自回归训练：单调递增 SNR 采样器与全局自 forcing

针对自回归逐块生成中的曝光偏差问题，SANA-Video 提出了两项训练策略改进（Sec. 3.4）：

- **单调递增 SNR 采样器**：在自回归块训练中，确保后续块的时间步始终大于前序块（即噪声水平递减），使模型在训练中更贴近推理时的去噪过程。消融实验表明，该采样器在 VBench 上的 Total Score 为 83.70，优于随机采样的 82.00（Table 5）。
- **基于全局缓存的 self-forcing**：利用块线性注意力的恒定内存全局 KV 缓存，实现长上下文的自 forcing 训练，将自回归训练扩展至 1 分钟视频。

### 5. 高分辨率压缩：DCAE-V 视频自编码器

针对 720p 高分辨率视频生成，SANA-Video 将 DCAE 微调为视频深度压缩自编码器 **DCAE-V**（Sec. 3.5）。该自编码器在压缩比 128 下达到 PSNR 33.25、SSIM 0.94、LPIPS 0.03 的重建质量（Table 3），且在噪声扰动下的重建鲁棒性优于 Wan2.1/2.2 VAE（Table 8），使其更适合小扩散模型的训练与推理。

---

**创新总结**：SANA-Video 以线性注意力为杠杆，系统性地重构了视频扩散模型的计算瓶颈——从 token 级注意力、时空特征提取、长序列缓存到自回归训练策略，形成了一套从 480p 到 720p、从 5 秒到分钟级视频的高效生成方案。



![[assets/figures/papers/paper_list_l2_https_openreview_net_forum_id_mzAchylAtf/figures/005_Figure_2.jpg]]
*Figure 2: Overview of SANA-Video. Fig.(a) A high-level block-wise autoregressive training pipeline based on our block causal KV cache. (Details in Sec. 3.3). Fig.(b) Our model pipeline, containing an Autoencoder, Re-writer, Linear DiT, and a text encoder. Fig.(c) The detailed design of the added 3D RoPE in linear attention and the temporal convolution in our Linear DiT’s Mix-FFN*

SANA-Video 的整体架构继承自 SANA-1.6B 文本到图像模型（Xie et al., 2025a），并针对视频生成的时空建模需求进行了关键改造。其核心设计理念是将所有注意力模块从传统的 Softmax 自注意力全面替换为线性注意力，从而将计算复杂度从 $O(N^2)$ 降至 $O(N)$，这一替换对于 token 数量巨大的高分辨率视频生成至关重要（Sec. 3.2）。

### 流水线组成

如图 2(b) 所示，SANA-Video 的生成流水线由四个核心模块串联构成：

1. **Autoencoder（VAE）**：负责视频的压缩与解码。对于 480P 分辨率，使用 Wan2.1-VAE（Wang et al., 2025a）；对于 720P 高分辨率视频，则微调 DCAE（Chen et al., 2024c）为视频深度压缩自编码器 **DCAE-V**，以更高的压缩比（128×）支持高效训练与推理（Sec. 3.5, 4.1）。
2. **Re-writer**：对输入文本提示进行改写与增强，提升文本-视频语义对齐质量。
3. **Linear DiT（线性扩散变换器）**：核心生成模块，将文本条件映射到视频潜空间。该模块全面采用线性注意力层，并集成了两项关键增强：
   - **3D RoPE**：在 ReLU 激活之后应用旋转位置编码，且从注意力分母中移除 RoPE，确保分母保持正值以保障训练稳定性（Eq. 2, Fig. 3）。
   - **Spatial-Temporal Mix-FFN**：在前馈网络中同时包含 2D 空间卷积和 1D 时间卷积，以增强局部时空特征提取能力（Fig. 2(c)）。
4. **Text Encoder**：采用小型 decoder-only 语言模型进行文本编码，保持与原始 SANA 一致的轻量化设计（Sec. 4.1）。

### 训练三阶段

SANA-Video 采用三阶段训练策略（Sec. 3.1）：

- **阶段一：VAE 适配** — 在文本到图像（T2I）数据上适配视频自编码器，确保潜空间表示的质量。
- **阶段二：继续预训练** — 从 T2I 模型权重出发，在视频数据上继续训练，注入时空建模能力。
- **阶段三：自回归块训练** — 引入 **Block Linear Attention** 与恒定内存 KV 缓存机制，支持长视频的自回归生成（Sec. 3.3）。

### 长视频生成的块线性注意力

对于分钟级长视频生成，SANA-Video 设计了 **Block Linear Attention** 模块（Fig. 4）。其核心机制是将因果线性注意力的累积状态 $S_j = \phi(K_j)^T V_j$ 和键和 $\sum \phi(K_j)^T$ 缓存为固定大小的全局状态（内存复杂度 $O(D^2)$，与序列长度 $N$ 无关），使得每个新 token 的计算成本保持恒定（Table 1, Eq. 3）。配合 **Block Causal Mix-FFN**（通过零填充和缓存前一块的最后一帧防止信息泄漏），该模块实现了恒定 GPU 内存下的全局自回归长视频生成（Sec. 3.3）。

### 自回归训练策略

为缓解自回归生成中的曝光偏差，SANA-Video 采用 **单调递增 SNR 采样器**（Monotonically Increasing SNR Sampler），确保后序块的扩散时间步始终大于前序块；同时结合基于全局缓存的 **Self-Forcing 长训练**策略，将自回归训练扩展至 1 分钟视频（Sec. 3.4）。



### 3.1 线性视频扩散变换器（Linear Video DiT）

SANA-Video 在 SANA-1.6B 文生图模型基础上继续预训练，核心改造是将所有 Softmax 自注意力模块替换为**带 3D RoPE 的线性注意力**，并在 Mix-FFN 中引入**1D 时间卷积**，形成时空混合前馈网络（Spatial-Temporal Mix-FFN）。

**训练目标**沿用 Rectified Flow 框架，配合 SNR 采样器：

$$\mathbb{E}_{c,t,x^0}\left\|u\big(x^t\mid t,c;\theta\big)-v(x)\right\|^2$$

其中 $u$ 为模型预测的速度场，$v$ 为目标速度，$c$ 为文本条件，$t$ 为时间步。

### 3.2 带稳定 RoPE 的线性注意力

线性注意力的核心思想是用核函数 $\phi(\cdot)$（此处为 ReLU 激活）替代 Softmax，将注意力计算分解为键-值的外积累积，从而将复杂度从 $O(N^2)$ 降至 $O(N)$。

**RoPE 的集成方式**是该方法的关键创新。标准做法是将 RoPE 直接作用于查询 $Q$ 和键 $K$，但作者发现这会导致分母（归一化项）出现负值，引发训练不稳定。SANA-Video 采用两处关键修改：

1. **RoPE 置于 ReLU 之后**：即 $\text{RoPE}(\phi(Q))$ 和 $\text{RoPE}(\phi(K))$，使得旋转位置编码作用于已非负的特征，产生更稀疏、更局部的注意力模式（Figure 3a）。
2. **分母移除 RoPE**：分母仅使用未旋转的 $\phi(Q)$ 和 $\phi(K)$，保证分母恒正，确保训练稳定（Figure 3b）。

修改后的线性注意力输出为：

$$O_i = \frac{\text{RoPE}(\phi(Q_i)) \left(\sum_{j=1}^N \text{RoPE}(\phi(K_j))^T V_j\right)}{\phi(Q_i) \left(\sum_{j=1}^N \phi(K_j)^T\right)}$$

这一设计同时保留了 RoPE 的局部性增强能力和线性注意力的训练稳定性，是该方法的**核心因果旋钮**。

### 3.3 块因果线性注意力与恒定内存 KV 缓存

为实现长视频的高效自回归生成，SANA-Video 将因果线性注意力重新表述为**累积状态形式**。定义累积注意状态 $S_j = \phi(K_j)^T V_j$，则第 $i$ 个 token 的输出为：

$$O_i = \frac{\phi(Q_i) \left( \sum_{j=1}^{i-1} S_j + S_i \right)}{\phi(Q_i) \left( \sum_{j=1}^{i-1} \phi(K_j)^T + \phi(K_i)^T \right)}$$

**关键性质**：$\sum S_j$ 和 $\sum \phi(K_j)^T$ 均可增量更新，每个新 token 仅需 $O(D^2)$ 的计算和内存，而非传统 KV 缓存的 $O(ND)$。Table 1 对比了三种注意力机制的成本：

| 注意力类型 | 内存成本 | 计算成本 | 感受野 |
|-----------|---------|---------|--------|
| 因果全注意力 | $O(ND)$ | $O(N^2D)$ | 全局 |
| 因果局部注意力 | $O(WD)$ | $O(WND)$ | 局部 |
| **因果线性注意力** | $\mathbf{O(D^2)}$ | $\mathbf{O(ND^2)}$ | **全局** |

其中 $N$ 为序列长度，$D$ 为特征维度，$W$ 为局部窗口大小。因果线性注意力是唯一同时保持全局感受野和恒定内存的方案。

**块因果 Mix-FFN** 为支持分块训练与推理，在每个块末尾追加全零 token（Zero Padding）防止信息泄漏，并通过缓存前一块的最后一帧来初始化时间卷积的因果状态（Figure 4b）。

### 3.4 长视频自回归训练策略

**单调递增 SNR 采样器**：在分块自回归训练中，早期块使用较大时间步（高噪声），后期块使用较小时间步（低噪声），确保所有时间步单调递增。这模拟了推理时从噪声到清晰的渐进去噪过程，缓解曝光偏差。

**自 forcing 长训练**：利用块线性注意力的全局恒定缓存，在训练中对历史块使用模型自身预测而非真实潜变量，使训练与推理的分布更一致，支持扩展到分钟级视频生成。



## 实验与关键发现

### 主结果：效率与性能的帕累托前沿

SANA-Video在VBench基准上实现了效率与质量的显著平衡。在480×832×81分辨率下，其T2V生成延迟仅为**60秒**，比Wan2.1-14B（484秒）快**8.1倍**，同时Total Score达到**83.71**，超越Wan2.1-1.3B（83.31）并与Open-Sora-2.0（14B参数）持平（Table 4）。在I2V任务上，Total Score为**88.02**，超过Wan2.1-14B（86.86），Semantic Score更达到**96.40**（对比Wan2.1-14B的92.90，提升+3.50）。

![[assets/figures/papers/paper_list_l2_https_openreview_net_forum_id_mzAchylAtf/figures/015_Table_4.jpg]]
*Table 4: Comprehensive comparison of our method with SOTA approaches in efficiency and performance on VBench. The speed is tested on one H100 GPU with BF16 Precision. Latency: Measured with a batch size of 1, on a 480×832×81 video, using the model’s default inference steps for a fair comparison. We highlight the best, second best, and third best entries*

效率优势在720p高分辨率下更加突出：SANA-Video-2B生成5秒720×1280×81视频仅需**36秒**，而Wan2.1-14B需1897秒，加速达**53倍**（Table 2）。此时VBench Total Score仍保持**84.05**，Semantic Score为**81.73**。值得注意的是，这一效率优势建立在仅**2B参数**的模型规模之上——训练成本仅为12天×64张H100 GPU，约为MovieGen的1%。

![[assets/figures/papers/paper_list_l2_https_openreview_net_forum_id_mzAchylAtf/figures/013_Table_2.jpg]]
*Table 2: Latency on H100 GPU and VBench Table 3: Reconstruction capability of different evaluation on 720×1280×81 resolution videos. Autoencoders on Panda-70M 192p resolution*

在长视频生成方面，LongSANA基于块线性注意力的恒定内存KV缓存，实现了分钟级自回归生成。VBench-Long基准测试中，30秒视频生成的对比结果见Table 9，其全局缓存机制避免了传统方法随序列长度线性增长的内存瓶颈（Table 1：因果线性注意力内存复杂度为O(D²)，而因果全注意力为O(N·D+N²)）。

![[assets/figures/papers/paper_list_l2_https_openreview_net_forum_id_mzAchylAtf/figures/008_Table_1.jpg]]
*Table 1: For a sequence with N tokens $\in \mathbb { R } ^ { 1 \times D }$ , memory and compute costs are compared among three attention types. Causal linear attention shows best efficiency while maintains global memory

![[assets/figures/papers/paper_list_l2_https_openreview_net_forum_id_mzAchylAtf/figures/035_Figure_11.jpg]]
*Figure 11: Long video visualization of LongSANA. Table 9: Comparison of long video generation methods on the VBench-Long (Zhang et al., 2024) benchmark. All compared methods generate 30s videos for evaluation*

### 消融实验：设计选择的因果链

消融实验揭示了各组件对性能的独立贡献（Table 5, Fig. 5）：

![[assets/figures/papers/paper_list_l2_https_openreview_net_forum_id_mzAchylAtf/figures/020_Table_5.jpg]]
*Table 5: Quantitative ablation studies on VBench*

**线性注意力的效率增益**：将全注意力替换为线性注意力后，480p下实现**2倍加速**，720p下实现**4倍加速**（Fig. 5(c)）。这一加速源于自注意力O(N²)到线性注意力O(N)的复杂度降阶，且加速比随分辨率（token数量）增加而扩大，验证了线性注意力在高分辨率视频生成中的关键作用。

**3D RoPE的位置效应**：在ReLU激活后施加RoPE（即RoPE(ReLU(x))）产生了更稀疏、更局部的注意力模式（Fig. 3(a)），训练损失显著低于无RoPE版本（Fig. 5(a)）。关键设计是将RoPE从分母中移除——若分母包含RoPE，训练损失出现发散（Fig. 3(b)红色曲线），而移除后训练保持稳定（绿色曲线）。这验证了分母正性对线性注意力训练稳定性的决定性作用。

**时空混合卷积**：在Mix-FFN中增加1D时间卷积后，训练损失进一步下降（Fig. 5(b)），且VBench运动质量指标提升（Table 5）。该设计以极小计算开销捕获了局部时序依赖，弥补了线性注意力在局部建模上的不足。

**单调递增SNR采样器**：在自回归块训练中，单调递增SNR采样器的Total Score为**83.70**，优于随机采样的**82.00**（Table 5）。这一策略通过确保后续块使用更大的时间步，使模型在自回归生成中逐步学习从噪声到清晰的过渡，有效缓解了曝光偏差问题。

**NVFP4量化加速**：在RTX 5090上，NVFP4精度将5秒720p视频生成从71秒降至**29秒**（2.4倍加速，Fig. 6），展示了该方法在消费级硬件上的部署潜力。

**VAE鲁棒性**：DCAE-V在噪声扰动下的重建鲁棒性优于Wan2.1/2.2 VAE（Table 8），使其更适合扩散模型训练中噪声潜在表示的编码-解码，这一特性对小模型尤为重要。

![[assets/figures/papers/paper_list_l2_https_openreview_net_forum_id_mzAchylAtf/figures/027_Table_8.jpg]]
*Table 8: Performance comparison of different VAE models on 1000 samples from Panda-70M with different noise perturbation levels*

### 失败模式与局限性

尽管SANA-Video在效率上表现突出，其**2B参数规模**限制了在高保真复杂动态场景下的表现上限——当场景涉及精细纹理、多物体交互或物理规律要求极高时，可能逊于14B级模型。长视频生成依赖5秒预训练模型的继续训练，分钟级视频的时序一致性与内容多样性仍受限于当前数据与训练策略。DCAE-V虽压缩比高达128倍，但在极端低码率下重建细节存在损失（Table 3），可能影响生成视频的纹理保真度。当前模型仅支持文本/图像条件，尚未扩展到音频驱动或多模态条件生成，限制了交互式应用场景。

![[assets/figures/papers/paper_list_l2_https_openreview_net_forum_id_mzAchylAtf/figures/014_Table_3.jpg]]

### 关键图表结论

- **Table 1**：因果线性注意力以O(D²)恒定内存和O(N·D²)计算成本，在保持全局感受野的同时实现了最优效率，这是块线性注意力设计的理论基石。
- **Table 4**：SANA-Video以2B参数量在VBench上达到与14B模型可比的性能，同时延迟降低一个数量级，验证了“线性注意力+高效训练策略”路线的有效性。
- **Fig. 5**：四项消融（RoPE、时间卷积、线性注意力加速、SNR采样器）构成完整的因果证据链，证明各设计选择对最终性能的独立且协同的贡献。
- **Table 8**：DCAE-V的噪声鲁棒性优势解释了其在小扩散模型上的适用性——更稳定的潜在空间降低了扩散模型的建模难度。

### 补充图表

![[assets/figures/papers/paper_list_l2_https_openreview_net_forum_id_mzAchylAtf/figures/021_Table_6.jpg]]
*Table 6: Comparison of autoregressive video generation methods on VBench*

![[assets/figures/papers/paper_list_l2_https_openreview_net_forum_id_mzAchylAtf/figures/024_Table_7.jpg]]
*Table 7: Architecture details of the proposed SANA-Video*



## 定位与知识库关联

### 1. 方法谱系与基线关系

SANA-Video 处于**高效视频扩散模型**这一细分方向，其核心创新是将线性注意力全面引入视频生成的 DiT 架构，并以恒定内存的块因果注意力机制突破长视频生成的内存瓶颈。

**与 SANA 系列的关系。** SANA-Video 直接从 SANA-1.6B 文生图模型继续预训练而来，继承了其线性注意力基础架构和小型 decoder-only 文本编码器，在模型参数规模和基础设计上几乎一致（Sec. 4.1）。关键差异在于：SANA-Video 将 2D 线性注意力扩展为时空线性注意力，引入 3D RoPE 位置编码和时空混合 Mix-FFN，并设计了块线性注意力及其 KV 缓存机制以支持长视频自回归生成。

**与主流视频扩散模型的关系。** 在 VBench 基准上，SANA-Video 的直接对比对象包括：
- **Wan2.1**（Wang et al., 2025a）：当前 SOTA 文本/图像到视频生成模型，采用全注意力机制。SANA-Video-2B 在 480P 下以 60s 延迟实现 8.1× 加速（Wan2.1-14B 为 484s），I2V Total Score 达 88.02，反超 Wan2.1-14B 的 86.86（Table 4）。在 720P 下延迟优势扩大至 53×（36s vs 1897s，Table 2）。
- **Open-Sora-2.0**（Peng et al., 2025）：14B 参数的大规模视频生成模型。SANA-Video-2B 以 1/7 参数量在 T2V Total Score 上与其持平（83.71 vs 83.76），同时延迟仅为 1/8（Table 4）。
- **CogVideoX**（Yang et al., 2024）、**Step-Video**（Ma et al., 2025）、**LTX-Video**（HaCohen et al., 2024）：SANA-Video 在延迟和 VBench 总分上均展现出显著优势或可比性能（Table 4）。
- **SkyReels-V2**（Chen et al., 2025a）：高效小规模视频生成基线，SANA-Video 在效率上进一步超越。
- **MAGI-1**（Teng et al., 2025）：长视频生成模型，SANA-Video 的块线性注意力机制提供了另一种恒定内存的长视频生成范式。

**与线性注意力文献的关系。** 线性注意力并非全新概念，但将其成功应用于大规模视频扩散模型并解决训练稳定性（RoPE 后置、分母去 RoPE）和长视频缓存（块因果状态累积）问题，构成了 SANA-Video 的核心贡献。其因果线性注意力的状态累积公式 $O_i = \frac{\phi(Q_i) \left( \sum_{j=1}^{i-1} S_j + S_i \right)}{\phi(Q_i) \left( \sum_{j=1}^{i-1} \phi(K_j)^T + \phi(K_i)^T \right)}$（Eq. 3）将逐 token 计算与内存成本固定为 $O(D^2)$，而非传统 KV 缓存的 $O(N)$（Table 1），这是支持分钟级长视频生成的理论基础。

### 2. 适用边界与假设条件

**适用场景。**
- **高分辨率视频生成**：线性注意力的 $O(N)$ 复杂度在 720P 及以上分辨率下带来 4× 以上的加速，使其特别适合高分辨率场景。
- **长视频自回归生成**：块线性注意力的恒定内存 KV 缓存使得生成分钟级视频时 GPU 内存不随序列长度增长，这是全注意力模型无法实现的。
- **资源受限环境**：2B 参数量配合 NVFP4 量化可在消费级 RTX 5090 上将 5 秒 720P 视频生成降至 29s（Fig. 6），训练成本仅需 64 张 H100 的 12 天。

**关键假设与约束。**
- **模型规模上限未验证**：当前仅在 2B 参数规模验证，线性注意力在 10B+ 参数级模型上的扩展性（是否出现性能饱和）仍是开放问题。
- **线性注意力的表达能力边界**：线性注意力通过 ReLU 激活和 RoPE 增强局部性，但其全局建模能力本质上弱于 softmax 注意力的指数归一化。在需要精确长程依赖建模的复杂动态场景下，性能可能受限。
- **自回归训练依赖预训练基础**：长视频生成（LongSANA）需在 5 秒预训练模型基础上继续训练，分钟级视频的端到端训练仍受限于数据规模与训练策略。
- **条件模态限制**：当前仅支持文本和图像条件，尚未扩展到音频驱动或多模态条件生成。

### 3. 局限性与已知问题

1. **模型规模与生成保真度的权衡**：SANA-Video-2B 在 VBench 语义分数上表现优异（T2V 81.35，I2V 96.40），但在高保真复杂动态场景下，小参数模型的纹理细节和物理一致性可能逊于 Wan2.1-14B 等大模型。这是效率与质量的固有权衡，论文未提供更大规模变体的对比。

2. **DCAE-V 的压缩损失**：虽然 DCAE-V 在 128 倍压缩比下实现了 PSNR 33.25 / SSIM 0.94 / LPIPS 0.03（Table 3），且在噪声扰动下鲁棒性优于 Wan-VAE（Table 8），但极端低码率下的重建损失仍可能限制高频细节保留，尤其在高分辨率视频中。

3. **长视频生成的质量衰减**：自回归块训练中，单调递增 SNR 采样器和自 forcing 策略缓解了曝光偏差（Table 5 中 Total Score 83.70 vs 82.00），但分钟级视频的时序一致性和运动自然度仍需进一步验证。VBench-Long 基准（Table 9）的评估仅覆盖 30 秒视频。

4. **训练数据依赖性**：论文使用了数据过滤和 SFT 数据微调来提升视频细节和物理规律遵循度（Fig. 14），但数据筛选策略的具体细节和潜在偏差未充分讨论。

### 4. 开放问题与未来方向

1. **线性注意力的规模化极限**：线性注意力在 10B+ 参数模型上的扩展性如何？是否会出现性能饱和？能否通过混合注意力（局部全注意力 + 全局线性注意力）进一步提升大模型表现？

2. **状态压缩的进一步优化**：块线性注意力的恒定内存为 $O(D^2)$，其中 $D$ 为特征维度。能否通过矩阵分解（如低秩近似）或状态空间模型的更高阶压缩进一步降低内存占用？

3. **多模态条件扩展**：当前架构仅支持文本/图像条件，能否直接扩展为端到端的音频-视频生成或交互式世界模型？Fig. 15 展示了世界模型任务的初步探索，但尚未系统评估。

4. **数据策略的深化**：更强的预训练数据筛选（如运动质量、美学评分）与更大规模的 SFT 数据能否进一步提升视频质量？数据效率与生成质量的关系值得深入研究。

5. **与状态空间模型的融合**：线性注意力的状态累积机制与 Mamba 等状态空间模型存在形式上的相似性，两者能否在视频生成任务中互补或统一？



## 原文 PDF

![[paperPDFs/ICLR_2026/SANA_Video_Efficient_Video_Generation_with_Block_Linear_Diffusion_Transformer.pdf]]
