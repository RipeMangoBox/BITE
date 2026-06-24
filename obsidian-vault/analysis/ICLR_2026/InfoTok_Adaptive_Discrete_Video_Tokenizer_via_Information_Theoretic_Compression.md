---
title: "InfoTok: Adaptive Discrete Video Tokenizer via Information-Theoretic Compression"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/InfoTok_Adaptive_Discrete_Video_Tokenizer_via_Information_Theoretic_Compression.pdf
openreview_forum_id: JEYWpFGzvn
aliases:
- IIF
- InfoTok
tags:
- ICLR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: "基于信息论的自适应路由机制（ELBO-based router），根据每个视频的信息复杂度（负对数似然）动态分配令牌数量。"
primary_logic: "根据香农信源编码定理，最优编码长度应与数据的负对数似然成正比；通过ELBO近似对数似然，并设计基于似然的令牌剪枝与Transformer压缩器，实现接近理论最优的自适应压缩。"
claims:
- "数据无关的统一路由器训练存在固有偏差，其期望令牌长度可比最优情况任意大（Theorem 2.2）。"
- "基于ELBO的路由器保证在损失最小化时，期望令牌长度不超过熵加近似误差（Theorem 3.1）。"
- "在TokenBench和DAVIS上，INFOTOK在相同压缩率下PSNR提升1.0–2.0 dB，FVD降低40–60%，且仅需一次额外前向传播。"
- "TokenBench-256x256 上 PSNR↑ (BPP16=0.81) = 30.08 (INFOTOK) / 29.86 (INFOTOK-Flex)"
---

# InfoTok: Adaptive Discrete Video Tokenizer via Information-Theoretic Compression

> [!tip] 核心洞察
> 根据香农信源编码定理，最优编码长度应与数据的负对数似然成正比；通过ELBO近似对数似然，并设计基于似然的令牌剪枝与Transformer压缩器，实现接近理论最优的自适应压缩。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | InfoTok：基于信息论压缩的自适应离散视频分词器 |
| 英文题名 | InfoTok: Adaptive Discrete Video Tokenizer via Information-Theoretic Compression |
| 会议/期刊 | ICLR 2026 (Oral) |
| Links | [paper](https://openreview.net/forum?id=JEYWpFGzvn); [GitHub](https://github.com/YWolfeee/InfoTok); [Project](https://research.nvidia.com/labs/dir/infotok/) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/image_and_video_generation |
| Method | INFOTOK (and INFOTOK-Flex) |
| Dataset | TokenBench-256x256, DAVIS-256x256 |

> [!tip] 效果简介
> - TokenBench-256x256 上，PSNR↑ (BPP16=0.81) 为 30.08 (INFOTOK) / 29.86 (INFOTOK-Flex)，对比 28.26 (ElasticTok)，变化 +1.82 / +1.60。
> - TokenBench-256x256 上，PSNR↑ (BPP16=0.56) 为 29.27 (INFOTOK) / 29.30 (INFOTOK-Flex)，对比 27.34 (ElasticTok)，变化 +1.93 / +1.96。
> - DAVIS-256x256 上，FVD↓ (BPP16=0.56) 为 540 (INFOTOK) / 581 (INFOTOK-Flex)，对比 930 (ElasticTok)，变化 -390 / -349。

## 概述

### 问题瓶颈

现有视频分词器（如 **Cosmos-DV4x8x8**、**Open-MAGVIT2-UCF**、**OmniTokenizer**）对所有视频内容采用固定的压缩率，忽略了不同视频之间信息密度的巨大差异。这种“一刀切”的策略导致两个后果：简单视频（如静态场景）被分配了冗余的令牌，造成存储和计算浪费；而复杂视频（如快速运动、场景切换）则因令牌预算不足而丢失关键信息，重建质量显著下降。即使是已有的自适应方法 **ElasticTok**（Yan et al., 2024），其统一的路由器训练模式也存在固有偏差——Theorem 2.2 证明，在最优推理条件下，其期望令牌长度可比理论最优值任意大，本质上仍是一种低效的启发式分配。

### 核心方法

**InfoTok** 从香农信源编码定理出发，提出了一个基于信息论的自适应离散视频分词框架。其核心洞察是：最优编码长度应与数据的负对数似然成正比。InfoTok 通过三个关键设计逼近这一理论最优：

1. **ELBO 路由器**：利用证据下界（ELBO）近似每个视频的对数似然，根据归一化后的 ELBO 值动态决定该视频的令牌预算 $N_{\mathbf{x}}$。Theorem 3.1 保证，在分词器训练充分时，该策略的压缩率在近似误差范围内达到最优。
2. **似然引导的令牌剪枝**：在确定令牌数量后，保留对数似然最低（即信息量最高）的令牌，丢弃高似然的冗余令牌，而非随机或按空间位置剪枝。
3. **Transformer 压缩器**：通过一个 8 层 ViT（含 2D RoPE）将固定长度的编码器隐变量压缩为目标长度的序列，再由 FSQ 量化器离散化。

整个框架仅需一次额外的解码器前向传播即可完成令牌长度决策，而 ElasticTok 需要 11 次二分搜索。

### 方法定位

InfoTok 并非从头设计分词器，而是在现有固定压缩率分词器（以 **Cosmos-DV4x8x8** 为骨干）之上叠加自适应路由与压缩模块。这种模块化设计使其自适应机制具有架构通用性——消融实验表明，在 Cosmos 和 ViT 两种不同骨干上，InfoTok 均大幅优于 ElasticTok。自适应压缩/解压缩模块仅增加 14.6% 的参数量（18M / 123M），换来了显著的压缩效率和质量提升。

### 主要结果

在 TokenBench 和 DAVIS 基准上，InfoTok 在相同压缩率下相较 ElasticTok 实现了系统性的性能跃升：PSNR 提升 1.0–2.0 dB，FVD 降低 40–60%，LPIPS 降低 25–40%。同时，InfoTok 仅需 1 次额外前向传播，而 ElasticTok 需要 11 次，推理效率提升约 11 倍。与固定压缩率的 Cosmos 骨干相比，InfoTok 在节省约 50% 令牌的同时保持重建质量不下降。

## 背景与动机

### 视频分词器的核心地位与固定压缩的困境

视频生成模型（如扩散模型、自回归Transformer）的规模化发展，使得离散视频分词器（discrete video tokenizer）成为关键基础设施。分词器将高维视频数据压缩为紧凑的离散令牌序列，其压缩效率直接决定了后续生成模型的计算开销和生成质量。然而，当前主流的分词器——包括 **Cosmos-DV4x8x8**（Agarwal et al., 2025）、**Open-MAGVIT2-UCF** 和 **OmniTokenizer**——均采用**固定压缩率**策略：对任意输入视频，令牌数量恒定为 $N = c \cdot T \cdot H \cdot W$，其中 $c$ 是预设的压缩因子。

这一设计存在根本性缺陷：**不同视频的信息密度差异巨大**。一段静态的风景视频与一段快速运动的体育视频，在相同的时空分辨率下，其实际信息量可以相差数倍。固定压缩率对所有视频一视同仁，必然导致两难困境——若压缩率过高，复杂视频的信息被过度丢弃，重建质量严重退化；若压缩率过低，简单视频产生大量冗余令牌，浪费计算资源。这一矛盾在长视频场景下尤为突出，因为视频内部的动态范围（如镜头切换、运动速度变化）进一步加剧了信息密度的不均匀性。

### 启发式自适应方法的局限

针对上述问题，**ElasticTok**（Yan et al., 2024）率先提出了自适应分词的思想：允许不同视频使用不同数量的令牌。然而，ElasticTok的自适应机制本质上是**启发式**的——它通过二分搜索在推理时反复尝试不同的压缩率，以匹配预设的重建质量阈值。这种方法存在两个关键瓶颈：

1. **理论偏差**：ElasticTok的路由器是数据无关的（data-agnostic），缺乏对视频信息量的直接度量。本文通过定理2.2严格证明，这种数据无关的路由器存在固有偏差，其期望令牌长度可比理论最优值**任意大**（Theorem 2.2），无法保证压缩效率的接近最优性。

2. **推理开销巨大**：为确定合适的压缩率，ElasticTok需要执行二分搜索，每次搜索都需要一次完整的前向传播。在典型设置下，这需要**11次额外前向传播**（NFEs），使得推理延迟和计算成本远高于固定压缩率分词器，严重限制了其实用性。

### 信息论视角下的理论动机

本文的核心洞察源于**香农信源编码定理**（Shannon's source coding theorem）：对于给定的数据分布，最优编码长度应与数据的**负对数似然**（negative log-likelihood，即信息量）成正比。换言之，一个信息论上最优的视频分词器，应当为信息量高的视频片段分配更多令牌，为信息量低的片段分配更少令牌。

将这一原理转化为可训练的框架面临两个挑战：（1）如何高效估计视频的对数似然？（2）如何基于对数似然动态调整令牌数量？本文提出**INFOTOK**，通过以下核心设计解决这两个问题：

- **ELBO路由器**：利用变分自编码器（VAE）的证据下界（ELBO）作为对数似然的近似。ELBO天然可从分词器的编码-解码过程中获取，无需额外模型。路由器根据归一化后的ELBO值，按比例 $N_{\mathbf{x}} = \beta \cdot \mathrm{ELBO}(\mathbf{x}) / \mathbb{E}[\mathrm{ELBO}(\mathbf{x})]$ 确定每个视频的令牌预算，其中 $\beta$ 是全局压缩因子。定理3.1保证，当分词器训练充分时，该路由器的期望令牌长度与理论最优值之间的差距不超过ELBO的近似误差（Theorem 3.1）。

- **基于似然的令牌剪枝**：在确定令牌数量后，如何选择保留哪些令牌？INFOTOK根据每个令牌的逐像素对数似然进行排序，**优先保留信息量最高（对数似然最低）的令牌**，丢弃冗余部分。这一策略在消融实验中显著优于随机剪枝和基于空间位置的剪枝（Table 3 Left）。

### 研究目标与贡献

综上，INFOTOK旨在构建一个**有理论保证的、高效的自适应视频分词框架**。其核心贡献包括：

- 首次从香农信息论的角度形式化视频分词的自适应压缩问题，并严格证明现有固定压缩率和数据无关自适应方法的理论偏差。
- 提出基于ELBO的路由器和基于似然的令牌剪枝机制，实现接近理论最优的自适应压缩。
- 在保持与固定压缩率分词器相同的单次前向传播开销（仅需1次额外NFEs）的前提下，显著超越ElasticTok的压缩效率与重建质量。

## 核心创新

### 问题根因：固定压缩率忽略视频信息密度差异

现有视频分词器——无论是固定压缩率的 **Cosmos-DV4x8x8**（Agarwal et al., 2025）、**Open-MAGVIT2-UCF** 还是启发式自适应的 **ElasticTok**（Yan et al., 2024）——均未从根本上解决一个核心矛盾：不同视频的信息密度差异巨大，而分词器却对所有内容施加统一的压缩率。这导致简单视频（如静止的狗睡觉场景）被过度分配令牌，造成冗余；复杂视频（如快速运动的猫打架场景）则因令牌不足而丢失关键信息。Theorem 2.2 从理论上证明了这种数据无关路由器的固有偏差：即使训练损失最小化，其期望令牌长度可比最优情况任意大（$\mathbb{E}[N_{\mathbf{x}}] \ge \kappa H_C(\mathbb{D})$，其中 $\kappa$ 可任意大），本质上违反了香农信源编码定理的最优压缩下界。

### 核心洞察：ELBO 作为信息量的代理，驱动接近理论最优的自适应压缩

InfoTok 的关键创新在于将**香农信源编码定理**直接转化为可训练的机制。该定理指出，最优编码长度应与数据的负对数似然 $-\log p(\mathbf{x})$ 成正比。由于真实对数似然不可直接获取，InfoTok 采用**证据下界（ELBO）**作为代理：

$$\mathrm{ELBO}(\mathbf{x}) = \mathbb{E}_{q_\phi(\mathbf{z}|\mathbf{x})} [\log p_\theta(\mathbf{x}|\mathbf{z})] - D_{\mathrm{KL}}[q_\phi(\mathbf{z}|\mathbf{x}) \| p(\mathbf{z})]$$

ELBO 是 $\log p(\mathbf{x})$ 的可证明下界，其值越大表示视频越容易被重建（信息量越低），反之则越复杂。基于此，InfoTok 设计了**基于 ELBO 的路由器**：

$$r_\beta(N_{\mathbf{x}} | \mathbf{x}) = \delta\left(\beta \cdot \frac{\mathrm{ELBO}(\mathbf{x})}{\mathbb{E}[\mathrm{ELBO}(\mathbf{x})]}\right)$$

该路由器根据每个视频的归一化 ELBO 值和全局压缩因子 $\beta$ 动态确定令牌数量 $N_{\mathbf{x}}$。Theorem 3.1 保证：当分词器训练充分时，InfoTok 的压缩率在近似误差范围内达到理论最优。

### Changed Slots：从固定到自适应的两处关键改动

InfoTok 在基础固定长度分词器（Cosmos 3D-CNN 编码器-解码器）之上，仅改动两个关键模块，实现了从“一刀切”到“按需分配”的范式转换：

| 模块 | 基线做法 | InfoTok 做法 | 机制与证据 |
|------|----------|-------------|-----------|
| **压缩策略（令牌长度分配）** | 固定压缩率 $c$，$N = c \cdot T \cdot H \cdot W$ | 自适应 ELBO 路由：$N_{\mathbf{x}} = \beta \cdot \mathrm{ELBO}(\mathbf{x}) / \mathbb{E}[\mathrm{ELBO}(\mathbf{x})]$ | ELBO 近似对数似然，驱动令牌预算与视频信息量成正比（Section 3.1, eq. (4)） |
| **令牌选择机制** | 保留所有固定长度的令牌 | ELBO 引导的令牌剪枝：保留对数似然最低（信息量最高）的 $N_{\mathbf{x}}$ 个令牌 | 基于每个令牌的重建对数似然排序，丢弃低信息量令牌，掩码 $m$ 作为离散令牌序列的一部分存储（Section 3.2） |

### 架构精简与推理效率优势

与 ElasticTok 的启发式随机掩码 + 二分搜索（需 11 次额外前向传播）不同，InfoTok 的 ELBO 计算仅需**一次额外的解码器前向传播**，且该计算可复用编码器的连续隐变量 $h$，无需重复编码。这使得 InfoTok 在推理效率上实现数量级提升（NFEs 开销从 11 降至 1），同时避免了二分搜索的阈值调参。

### 理论保证与实证验证

InfoTok 的理论优势在实验中得到了充分验证：
- **Table 2 消融**：ELBO 路由器与穷举搜索得到的最优令牌分配策略性能极其接近（TokenBench, BPP16=0.56），证明 ELBO 是信息量的有效代理。
- **Table 3 消融**：基于 ELBO 的令牌剪枝显著优于随机剪枝和基于空间位置的剪枝，验证了“保留信息量最高的令牌”这一策略的合理性。
- **Table 3 跨架构验证**：在 Cosmos 和 ViT 两种不同骨干上，InfoTok 均大幅优于 ElasticTok，说明自适应机制具有架构通用性，而非依赖特定编码器设计。
- **Table 4 参数开销**：自适应压缩/解压缩模块（8 层 ViT + RoPE）仅增加 14.6% 参数量（18M / 123M），换来了显著的压缩效率和质量提升。

### INFOTOK-Flex：多压缩率的统一模型

为支持灵活的多压缩率部署，InfoTok 进一步提出 **INFOTOK-Flex**，其路由器对多个 $\beta$ 值取平均：

$$\tilde{r}_\beta^{\mathrm{flex}}(N_{\mathbf{x}} | \mathbf{x}) = \frac{1}{B} \sum_{\beta \in \mathcal{B}} r_\beta(N_{\mathbf{x}} | \tilde{\mathbf{x}})$$

这使得单一模型可在不同压缩率下运行，而无需为每个压缩率单独训练模型（Figure 3 展示了 INFOTOK-Flex 在不同压缩率下的重建效果）。实证中，使用重建误差本身（不含 KL 项）推导令牌预算比即足够有效，进一步简化了计算。

## 整体框架

![[assets/figures/papers/paper_list_l8_https_openreview_net_forum_id_JEYWpFGzvn/figures/001_Figure_1.jpg]]
*Figure 1: Overall framework of INFOTOK, an information-theoretic adaptive video tokenizer. An encoder maps video x into fixed-length embeddings, from which a router estimates the number of tokens $N _ { \mathbf { x } }$ based on information complexity (section 3.1). An adaptive compressor encodes the embeddings to $N _ { \mathbf { x } }$ tokens (section 3.2). For reconstruction, the tokens are decompressed to fixed-length embeddings and decoded back into video. INFOTOK tokenizes based on video complexity: e.g., the stable dog video is compressed more (0.40) than the dynamic cat-fighting video (0.62). Illustration details can be found in Appendix A

InfoTok 的整体框架围绕一个核心洞察构建：视频的信息密度差异巨大，固定压缩率的分词器必然在简单视频上冗余、在复杂视频上丢失信息。为此，InfoTok 在固定长度分词器之上引入两个关键模块——**基于 ELBO 的路由器**和**自适应压缩/解压缩器**——形成一条端到端的自适应离散视频分词流水线。

流水线的完整数据流如下：

1. **编码器（Encoder）**：采用 Cosmos‑DV4x8x8 的 3D‑CNN 骨干（Agarwal et al., 2025），将输入视频 $\mathbf{x}$ 映射为固定长度的连续隐变量 $\mathbf{h} \in \mathbb{R}^{N \times K}$，其中最大令牌数 $N_{\max} = \frac{T}{4} \times \frac{H}{8} \times \frac{W}{8}$。

2. **路由器（Router）**：根据视频的信息复杂度动态决定该视频应分配的令牌数量 $N_{\mathbf{x}}$。具体地，路由器计算视频的证据下界 $\mathrm{ELBO}(\mathbf{x})$ 作为对数似然的代理，并以归一化 ELBO 的比例确定令牌预算：
   $$r_{\beta}(N_{\mathbf{x}} | \mathbf{x}) = \delta\!\left( \beta \cdot \frac{\mathrm{ELBO}(\mathbf{x})}{\mathbb{E}[\mathrm{ELBO}(\mathbf{x})]} \right)$$
   其中 $\beta$ 是全局压缩因子。InfoTok‑Flex 进一步对多个 $\beta$ 值取平均，使单一模型支持任意压缩率。

3. **自适应压缩器（Adaptive Compressor）**：一个 8 层 ViT 加 RoPE 位置编码的 Transformer，接收固定长度 $\mathbf{h}$ 和令牌预算 $N_{\mathbf{x}}$，通过 ELBO 引导的令牌剪枝保留对数似然最低（即信息量最高）的 $N_{\mathbf{x}}$ 个令牌，输出压缩后的隐变量 $\mathbf{h}'$。

4. **量化器（Quantizer）**：使用有限标量量化器（FSQ, Mentzer et al., 2023）将 $\mathbf{h}'$ 离散化为令牌 $\mathbf{z}$，同时存储剪枝掩码 $\mathbf{m}$ 作为离散令牌序列的一部分。

5. **自适应解压缩器（Adaptive Decompressor）**：对称的 8 层 ViT，将量化后的 $\hat{\mathbf{h}}'$ 恢复为固定长度的 $\hat{\mathbf{h}}$。

6. **解码器（Decoder）**：与编码器对称的 Cosmos 3D‑CNN，从 $\hat{\mathbf{h}}$ 重建视频 $\hat{\mathbf{x}}$。

框架的关键效率优势在于：ELBO 的计算仅需一次额外的解码器前向传播（先编码再直接解码，不经过自适应压缩器），而对比方法 ElasticTok 需要二分搜索，产生 11 次额外前向传播。自适应压缩/解压缩模块共增加约 18M 参数（占基础分词器 123M 的 14.6%），换取了显著的压缩效率与重建质量提升。

## 核心模块与公式推导

### 问题形式化：从固定压缩到自适应压缩

传统固定压缩率分词器的训练目标是最小化重建负对数似然：

$$
\mathcal{L}_{\mathrm{recon}}(\mathcal{T}) = \mathbb{E}_{\mathbf{x} \sim \mathbb{D}, q_{\phi}(\mathbf{z}|\mathbf{x})} \left[ -\log p_{\theta}(\mathbf{x}|\mathbf{z}) \right] \tag{1}
$$

其中 $\mathbf{x}$ 为输入视频，$q_{\phi}(\mathbf{z}|\mathbf{x})$ 为编码器-量化器产生的离散令牌分布，$p_{\theta}(\mathbf{x}|\mathbf{z})$ 为解码器。该范式对所有视频分配相同数量的令牌，忽略了视频间信息密度的差异。

自适应分词器 $\mathcal{T}_{\text{adaptive}} = (\mathcal{T}, r, M_{\psi})$ 在固定分词器 $\mathcal{T}$ 之上引入两个核心组件：**路由器** $r(N_{\mathbf{x}}|\mathbf{x})$ 决定每视频的令牌长度 $N_{\mathbf{x}}$；**自适应压缩器** $M_{\psi}$ 将编码器输出的固定长度隐变量 $\mathbf{h} \in \mathbb{R}^{N \times K}$ 压缩为 $\mathbf{h}' \in \mathbb{R}^{N_{\mathbf{x}} \times K}$。其重建损失为：

$$
\mathcal{L}_{\mathrm{recon}}(\mathcal{T}_{\mathrm{adaptive}}) = \mathbb{E}_{\mathbf{x} \sim \mathbb{D}, N_{\mathbf{x}} \sim r(N_{\mathbf{x}}|\mathbf{x}), \mathbf{z} \sim q_{\phi,\psi}(\mathbf{z}|\mathbf{x}, N_{\mathbf{x}})} \left[ -\log p_{\theta,\psi}(\mathbf{x}|\mathbf{z}) \right] \tag{2}
$$

香农信源编码定理给出了令牌长度的理论下界：$\mathbb{E}_{\mathbf{x} \sim p(\mathbf{x})}[N_{\mathbf{x}}] \ge H_C(\mathbb{D})$，其中 $H_C(\mathbb{D}) = \mathbb{E}_{\mathbf{x} \sim p(\mathbf{x})}[-\log_C p(\mathbf{x})]$ 为 $C$ 元熵。这意味着最优压缩率应与数据的负对数似然成正比，为后续设计提供了理论依据。

### 核心模块一：基于 ELBO 的路由器

路由器需要估计每视频的“信息复杂度”以确定令牌预算，但真实对数似然 $\log p(\mathbf{x})$ 难以直接计算。InfoTok 采用证据下界（ELBO）作为代理：

$$
\mathrm{ELBO}(\mathbf{x}) = \mathbb{E}_{q_{\phi}(\mathbf{z}|\mathbf{x})} \left[ \log p_{\theta}(\mathbf{x}|\mathbf{z}) \right] - D_{\mathrm{KL}} \left[ q_{\phi}(\mathbf{z}|\mathbf{x}) \lVert p(\mathbf{z}) \right] \tag{3}
$$

ELBO 是对数似然的可证下界（$\mathrm{ELBO}(\mathbf{x}) \le \log p(\mathbf{x})$），且可由固定分词器直接计算。基于此，路由器定义为以归一化 ELBO 为参数的 Dirac 分布：

$$
r_{\beta}(N_{\mathbf{x}} | \mathbf{x}) = \delta \left( \beta \cdot \frac{\mathrm{ELBO}(\mathbf{x})}{\mathbb{E}[\mathrm{ELBO}(\mathbf{x})]} \right) \tag{4}
$$

其中 $\beta$ 为全局压缩因子，控制期望令牌长度。该设计的理论保证由 **Theorem 3.1** 给出：当分词器训练充分时，期望令牌长度不超过熵加近似误差，即压缩率接近理论最优。

**高效计算**：ELBO 的计算仅需一次额外的解码器前向传播——先用编码器得到 $\mathbf{h}$，不经自适应压缩直接解码得到 $\hat{\mathbf{x}}$ 以计算重建误差；随后复用 $\mathbf{h}$ 经自适应压缩器处理。这使 InfoTok 的额外函数评估次数（NFEs）仅为 1，而 ElasticTok 的二分搜索需要 11 次。

**InfoTok-Flex 变体**：为支持连续可调的压缩率，InfoTok-Flex 对多个 $\beta$ 值取平均路由：

$$
\tilde{r}_{\beta}^{\mathrm{flex}}(N_{\mathbf{x}} | \mathbf{x}) = \frac{1}{B} \sum_{\beta \in \mathcal{B}} r_{\beta}(N_{\mathbf{x}} | \tilde{\mathbf{x}}) \tag{5}
$$

实践中发现，仅使用重建误差项（省略 KL 散度）来推导路由策略已足够有效。

### 核心模块二：自适应压缩器与令牌剪枝

自适应压缩器 $M_{\psi}$ 的核心问题是如何从 $N$ 个固定令牌中选择并压缩为 $N_{\mathbf{x}}$ 个。InfoTok 采用 **ELBO 引导的令牌剪枝**策略：计算每个令牌位置的对数似然贡献，保留对数似然最低（即信息量最高）的 $N_{\mathbf{x}}$ 个令牌，丢弃其余。

压缩器本身为 8 层 ViT，配合旋转位置编码（RoPE），并在 Cosmos 骨干的 3D-CNN 编码器之后、FSQ 量化器之前运行。为保持 Cosmos 的因果性，注意力矩阵采用块因果掩码。剪枝产生的掩码 $\mathbf{m}$ 作为离散令牌序列 $\mathbf{z}$ 的一部分存储，以供解压缩器恢复固定长度的 $\hat{\mathbf{h}}$。

### 关键公式汇总

| 公式 | 含义 |
|------|------|
| $\mathcal{L}_{\mathrm{recon}}$ (式1) | 固定压缩率分词器的重建损失 |
| $\mathrm{ELBO}(\mathbf{x})$ (式3) | 对数似然的变分下界，近似视频信息量 |
| $r_{\beta}(N_{\mathbf{x}}|\mathbf{x})$ (式4) | 基于归一化 ELBO 的路由器，决定令牌长度 |
| $\tilde{r}_{\beta}^{\mathrm{flex}}$ (式5) | InfoTok-Flex 的多 $\beta$ 集成路由 |
| $\mathsf{BPP}_{16} = 16c \cdot \log(C)$ | 每 16 像素比特数，统一压缩率度量 |
| $N_{\max} = \frac{T}{4} \times \frac{H}{8} \times \frac{W}{8}$ | Cosmos 骨干对 $T \times H \times W$ 视频的最大令牌数 |

## 实验与分析

### 核心瓶颈与理论动机

现有视频分词器对所有内容使用固定的压缩率，忽略视频间信息密度的差异——简单视频产生冗余令牌，复杂视频则因压缩不足而丢失信息。**ElasticTok**（Yan et al., 2024）虽引入自适应机制，但其数据无关的统一路由器存在固有偏差：Theorem 2.2 证明，即使训练损失最小化，期望令牌长度可比最优情况任意大（$\kappa H_C(\mathbb{D})$，其中 $\kappa$ 可能远大于 1）。这从根本上限制了启发式自适应方法的效率。

### 实验设置

**数据集与预处理**：实验在 TokenBench 和 DAVIS 两个基准上进行，所有视频统一处理为 256×256 方形裁剪、33 帧片段。压缩率统一用 $\mathsf{BPP_{16}} = 16c \cdot \log(C)$ 度量，其中 $c$ 为令牌数与像素数之比，$C$ 为码本大小。Cosmos 骨干的最大令牌数 $N_{\mathrm{max}} = \frac{T}{4} \times \frac{H}{8} \times \frac{W}{8} = \frac{1}{256} T H W$。

**对比基线**：固定压缩率分词器包括 **Cosmos-DV4x8x8**（Agarwal et al., 2025）、**Open-MAGVIT2-UCF** 和 **OmniTokenizer**；自适应方法为 **ElasticTok**（Yan et al., 2024），其采用右到左随机掩码训练和二分搜索推理（需 11 次额外前向传播）。所有模型使用相同的 Cosmos 骨干、batch size=1、33 帧、1e5 训练步数，确保公平比较。

### 主要结果

**Table 1** 展示了在 TokenBench 和 DAVIS 上的定量对比。在 TokenBench 上，当 $\mathsf{BPP_{16}}=0.81$ 时，INFOTOK 的 PSNR 达到 30.08 dB，较 ElasticTok（28.26 dB）提升 **+1.82 dB**；INFOTOK-Flex 达到 29.86 dB（+1.60 dB）。在更激进的压缩率 $\mathsf{BPP_{16}}=0.56$ 下，提升幅度进一步扩大至 **+1.93 dB**（INFOTOK）和 **+1.96 dB**（INFOTOK-Flex）。在 DAVIS 上，相同压缩率下 FVD 从 ElasticTok 的 930 降至 INFOTOK 的 **540**（降低 42%）和 INFOTOK-Flex 的 581（降低 38%）。


![[assets/figures/papers/paper_list_l8_https_openreview_net_forum_id_JEYWpFGzvn/figures/002_Table_1.jpg]]
*Table 1: Evaluation of fixed-length and adaptive tokenizers on TokenBench and DAVIS. We compare INFOTOK with ElasticTok at two compression levels (0.81, 0.56) by setting our compression rates to theirs*

**Figure 4** 的性能曲线揭示了更完整的图景：INFOTOK 和 INFOTOK-Flex 在全部 $\mathsf{BPP_{16}}$ 范围内均显著优于 ElasticTok，FVD 降低 40–60%，LPIPS 降低 25–40%，PSNR 提升 1.0–2.0 dB。更重要的是，**Figure 4g** 显示 INFOTOK 仅需 **1 次**额外前向传播（用于 ELBO 计算），而 ElasticTok 需要 **11 次**二分搜索——推理效率提升约一个数量级。Table 6 的延迟对比进一步确认了这一优势。


![[assets/figures/papers/paper_list_l8_https_openreview_net_forum_id_JEYWpFGzvn/figures/005_Figure_4.jpg]]
*Figure 4: Video tokenization performance of INFOTOK-Flex, INFOTOK, and ElasticTok on TokenBench (a-c) and DAVIS (d-f). Quality metrics are plotted against $\mathrm { B P P _ { 1 6 } }$ (bits per 16 pixels). Tokenization efficiency measured in the Number of Function Evaluations overhead (additional NFEs / standard NFEs ↓) is shown in (g). InfoTok-Flex and InfoTok achieve superior reconstruction quality with smaller $\mathrm { B P P _ { 1 6 } }$ levels. Additionally, INFOTOK is significantly more efficient than ElasticTok, which requires searching to meet thresholds

![[assets/figures/papers/paper_list_l8_https_openreview_net_forum_id_JEYWpFGzvn/figures/012_Table_6.jpg]]
*Table 6: Inference latency comparison across different methods*

**定性分析**：Figure 2 展示了不同复杂度视频的重建效果。对于静态场景（如趴卧的狗），INFOTOK-Flex 以更高的压缩率（0.40 vs Cosmos-DV 的固定比例）达到相似 PSNR；对于动态场景（如猫打架），则分配更多令牌（0.62）以保证重建质量。Figure 3 展示了 INFOTOK-Flex 在不同压缩率下的连续调节能力。


![[assets/figures/papers/paper_list_l8_https_openreview_net_forum_id_JEYWpFGzvn/figures/004_Figure_3.jpg]]
*Figure 3: Reconstructions examples of video by INFOTOK-Flex with different compression rates*

### 消融研究

**ELBO 路由器的有效性**：Table 2 将基于 ELBO 的路由器与穷举搜索的最优策略进行对比。在 TokenBench 上（$\mathsf{BPP_{16}}=0.56$），ELBO 路由器的性能与最优上限极为接近——PSNR 差距仅约 0.1 dB，FVD 差距在个位数。这验证了 Theorem 3.1 的理论保证：当分词器训练充分时，ELBO 路由器的压缩率在近似误差范围内达到最优。


![[assets/figures/papers/paper_list_l8_https_openreview_net_forum_id_JEYWpFGzvn/figures/006_Table_2.jpg]]
*Table 2: Ablation on INFOTOK versus an optimal search-based strategy to determine the token lengths. “Optimal” is a strict upper bound of our method, yet their performance is extremely close*

**令牌剪枝策略**：Table 3（左）比较了三种剪枝方式：基于似然的 ELBO 引导剪枝、随机剪枝和基于空间位置的剪枝。ELBO 引导策略（保留对数似然最低、信息量最高的令牌）在所有指标上均显著优于其他两种，验证了信息论指导的令牌选择是性能提升的关键来源。


![[assets/figures/papers/paper_list_l8_https_openreview_net_forum_id_JEYWpFGzvn/figures/007_Table_3.jpg]]
*Table 3: Ablation results on TokenBench with an average $\mathrm { B P P 1 6 }$ ~ = ~ 0 . 5 6 . . (Left) Ablation on adaptive compressors. (Right) Ablation on different variants of adaptive mechanisms across architectures*

**架构通用性**：Table 3（右）显示 INFOTOK 在 Cosmos 和 ViT 两种骨干上均大幅优于 ElasticTok，说明自适应机制不依赖于特定编码器架构。Table 5 进一步验证了多分辨率泛化性——在 360p 分辨率下，INFOTOK 仍保持一致的性能优势。


![[assets/figures/papers/paper_list_l8_https_openreview_net_forum_id_JEYWpFGzvn/figures/011_Table_5.jpg]]
*Table 5: Comparison of Cosmos Arch with and without InfoTok across resolutions on TokenBench*

**模块开销**：Table 4 的架构配置表明，自适应压缩/解压缩模块（8 层 ViT + RoPE）仅增加 18M 参数（约 14.6%），相对于基础分词器的 123M 参数量占比很小，但换来了显著的压缩效率和质量提升。


![[assets/figures/papers/paper_list_l8_https_openreview_net_forum_id_JEYWpFGzvn/figures/010_Table_4.jpg]]
*Table 4: Architecture Configuration*

### 失败模式与局限性

1. **ELBO 近似的紧密度**：ELBO 作为对数似然的下界，其准确性依赖于 VAE 后验的质量。在极端分布外视频上，ELBO 可能无法精确反映真实信息量，导致令牌分配次优。不过 Table 2 的消融表明在实际数据上这一偏差很小。

2. **全局统一比例的限制**：当前路由器为整个视频分配统一的压缩比例，无法进行更精细的逐帧或逐空间区域自适应。对于包含静态背景和局部剧烈运动的混合场景，这可能留下效率提升空间。

3. **下游任务验证缺失**：所有实验仅评估视频重建质量，未在视频生成（如扩散模型）或动作理解等下游任务中验证自适应令牌化的实际收益。

4. **计算资源门槛**：训练需要 32 块 H100 GPU，虽然推理效率极高，但训练成本对资源有限的团队构成障碍。

## 方法谱系与知识库定位

### 核心问题与定位

现有视频分词器普遍采用**固定压缩率**策略，即对所有视频内容分配相同数量的令牌，忽略视频间信息密度的显著差异。这一设计导致简单场景（如静态背景）产生冗余令牌，而复杂场景（如高速运动、剧烈光照变化）则因令牌不足而丢失关键信息。**InfoTok** 从香农信源编码定理出发，指出最优编码长度应与数据的负对数似然成正比，从而将自适应压缩问题形式化为信息论框架下的令牌预算分配问题。

InfoTok 的方法定位可概括为：**以 ELBO 为信息量代理的自适应离散视频分词器**。其与现有工作的关系如下：

- **固定压缩率分词器**（如 **Cosmos-DV4x8x8** (Agarwal et al., 2025)、**Open-MAGVIT2-UCF**、**OmniTokenizer**）：InfoTok 在这些方法的基础上增加路由器和自适应压缩/解压缩模块，将固定令牌序列转化为内容自适应的可变长度序列。核心区别在于压缩率由数据驱动而非人为设定。

- **启发式自适应分词器**（如 **ElasticTok** (Yan et al., 2024)）：ElasticTok 采用均匀随机掩码训练和二分搜索推理，其路由器与数据内容无关。InfoTok 在理论上证明了此类数据无关路由器的固有偏差——其期望令牌长度可比最优情况任意大（Theorem 2.2），并通过 ELBO 路由器实现了接近理论最优的压缩效率。

### 关键技术决策与因果机制

InfoTok 的性能优势源于三个相互耦合的设计选择：

1. **基于 ELBO 的路由器**：利用 VAE 的证据下界近似视频的对数似然，据此分配令牌预算 $N_{\mathbf{x}} = \beta \cdot \frac{\mathrm{ELBO}(\mathbf{x})}{\mathbb{E}[\mathrm{ELBO}(\mathbf{x})]}$。Theorem 3.1 保证，在分词器充分训练的条件下，该策略的压缩率在近似误差范围内达到最优。消融实验（Table 2）表明，ELBO 路由器与穷举搜索的最优策略性能极为接近，验证了其理论紧密度。

2. **似然引导的令牌剪枝**：在自适应压缩器中，按逐令牌的对数似然排序，保留信息量最高的 $N_{\mathbf{x}}$ 个令牌。消融实验（Table 3 Left）证实该方法显著优于随机剪枝和基于空间位置的剪枝，说明信息量度量是压缩决策的关键。

3. **架构通用性**：自适应压缩/解压缩模块（8 层 ViT + RoPE）仅增加 14.6% 参数量（18M / 123M），但在 Cosmos 和 ViT 两种骨干上均大幅优于 ElasticTok（Table 3 Right），表明该机制不依赖于特定编码器架构。

### 适用边界与局限

- **任务范围**：目前仅验证了视频重建任务，在下游视频生成（如扩散模型）或视频理解任务中的效果尚未评估。自适应令牌化对生成模型训练动态的影响是开放问题。
- **数据分布**：ELBO 作为对数似然的近似，其紧密度依赖于 VAE 后验的准确性。在极端分布外视频（如高度非自然场景）上，路由器可能给出次优的令牌预算。
- **分辨率泛化**：实验主要在 256px 方形视频上进行，虽有 360p 的初步测试（Table 5），但更高分辨率和任意长宽比的全面验证有限。
- **计算开销**：自适应压缩模块增加了 18M 参数，训练需要 32 块 H100 GPU，计算资源门槛较高。推理时仅需一次额外解码器前向传播（vs ElasticTok 的 11 次），效率优势显著但仍有可优化空间。

### 开放问题

1. **路由器的轻量化**：ELBO 路由器能否被一个直接基于编码器隐变量统计量（如方差、熵估计）的轻量级模块替代，从而避免额外的解码器前向传播？
2. **下游任务收益**：自适应令牌化在视频生成（扩散模型、自回归模型）和视频理解（动作识别、时序定位）中的实际收益如何？压缩率的动态变化是否会影响生成模型的训练稳定性？
3. **模态泛化**：该信息论框架能否推广到音频、3D 点云等其他高维数据模态？关键挑战在于如何为不同模态定义合适的 ELBO 近似。
4. **细粒度自适应**：当前方法为整个视频统一分配令牌比例，更精细的逐帧或逐空间区域自适应压缩是否能进一步提升效率？这可能需要在路由器中引入时空局部性的信息量估计。
5. **大规模预训练的影响**：在更大视频数据集（如 PANDA-70M）上预训练对 ELBO 路由器的泛化性影响如何？大规模数据是否会使 ELBO 分布更加稳定，从而减少路由偏差？

## 原文 PDF

![[paperPDFs/ICLR_2026/InfoTok_Adaptive_Discrete_Video_Tokenizer_via_Information_Theoretic_Compression.pdf]]
