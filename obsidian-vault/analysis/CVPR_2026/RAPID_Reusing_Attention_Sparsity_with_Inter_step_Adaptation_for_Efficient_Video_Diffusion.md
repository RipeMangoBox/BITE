---
title: "RAPID: Reusing Attention Sparsity with Inter-step Adaptation for Efficient Video Diffusion"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/RAPID_Reusing_Attention_Sparsity_with_Inter_step_Adaptation_for_Efficient_Video_Diffusion.pdf
project_link: null
code_link: null
aliases:
- RAPID
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/generative_models_diffusion
- topic/generative_models_diffusion/diffusion_image_video
core_operator: 现有动态稀疏注意力方法在每个去噪步骤都需要重新估计注意力掩码，引入大量重复计算开销；而静态方法缺乏内容自适应性，无法在保持高质量的同时进一步加速。
primary_logic: 视频扩散过程中的注意力稀疏模式具有两个关键特性：1）在初始预热后，高重要性的注意力模式表现出很强的时间稳定性，且一个早期步骤的掩码能够安全地覆盖后续步骤的重要 token；2）随着去噪过程推进，所需的计算密度逐渐衰减，后期步骤对稀疏剪枝的容忍度更高。因此，通过一次性早期估计并缓存重要性分数和掩码，即可在后续步骤中高效复用，并在后期阶段利用缓存分数进行自适应更激进的剪枝，从而大幅加速推理而不牺牲质量。
claims:
- 注意力密度需求在去噪过程中表现出强时间稳定性，且所需的平均密度逐渐递减。
- 在早期步骤（step 5）计算的一次性掩码在整个后续步骤中保持高召回率（Recall），证明了其安全性和有效性。
- RAPID 默认模式在相同的注意力密度预算下，质量显著优于最强的基线方法（PSNR 提升高达 4.0）。
- Turbo 模式通过简单的缓存分数重阈值化即可实现最高 2.01× 加速，同时保持有竞争力的视觉质量。
---

# RAPID: Reusing Attention Sparsity with Inter-step Adaptation for Efficient Video Diffusion

> [!tip] 核心洞察
> 视频扩散过程中的注意力稀疏模式具有两个关键特性：1）在初始预热后，高重要性的注意力模式表现出很强的时间稳定性，且一个早期步骤的掩码能够安全地覆盖后续步骤的重要 token；2）随着去噪过程推进，所需的计算密度逐渐衰减，后期步骤对稀疏剪枝的容忍度更高。因此，通过一次性早期估计并缓存重要性分数和掩码，即可在后续步骤中高效复用，并在后期阶段利用缓存分数进行自适应更激进的剪枝，从而大幅加速推理而不牺牲质量。

| 字段 | 内容 |
|------|------|
| 中文题名 | RAPID：基于中间步骤自适应注意力稀疏重用的高效视频扩散 |
| 英文题名 | RAPID: Reusing Attention Sparsity with Inter-step Adaptation for Efficient Video Diffusion |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://openaccess.thecvf.com/content/CVPR2026/html/Lin_RAPID_Reusing_Attention_Sparsity_with_Inter-step_Adaptation_for_Efficient_Video_CVPR_2026_paper.html) |
| Topic | #topic/vision_multimodal_applications #topic/generative_models_diffusion #topic/generative_models_diffusion/diffusion_image_video |
| Method | RAPID |
| Dataset | Wan2.1-14B, HunyuanVideo |

> [!tip] 效果简介
> - Wan2.1-14B (VBench-2.0) 上，PSNR 26.112 vs 22.1（最强基线估算值） (+4.0)；SSIM 0.871 vs N/A (N/A)；LPIPS 0.096 vs N/A (N/A)。
> - HunyuanVideo (VBench-2.0) 上，PSNR 31.488 vs N/A (显著优于基线)；SSIM 0.948 vs N/A (显著优于基线)；LPIPS 0.073 vs N/A (显著优于基线)。

## 概要

视频扩散模型在生成高质量视频方面取得了显著进展，但其核心组件——3D 自注意力机制——的计算复杂度随时空 token 数量 $N$ 呈二次增长 $O(N^2)$，导致推理延迟极高（例如，单次生成耗时可达 66 分钟），成为实际部署的主要瓶颈。

为缓解这一问题，现有方法主要分为两类：**动态稀疏注意力**（如 **X-Attention**，Xu et al., ICML 2025）在每个去噪步骤重新估计注意力重要性并生成掩码，虽能保持内容自适应性，但引入了大量重复计算开销；**静态稀疏注意力**（如 **Sparse VideoGen**，Xi et al., arXiv 2025；**Radial Attention**，Li et al., arXiv 2025）采用固定的时空掩码模式，计算开销低，却缺乏对内容变化的适应能力，难以在加速的同时维持高质量。

本文的核心发现是：视频扩散过程中的注意力稀疏模式具有两个关键特性——**时间稳定性**与**密度衰减**。具体而言，在初始预热阶段后，高重要性注意力模式在不同去噪步骤间表现出高度一致性，早期步骤估计的掩码能够以高召回率覆盖后续步骤的重要 token（Figure 3）；同时，随着去噪推进，维持生成质量所需的最小注意力密度逐渐降低（Figure 2），后期步骤对稀疏剪枝的容忍度显著更高。

基于上述分析，本文提出 **RAPID** 框架，其核心思路是**一次性估计与缓存复用**：在生成过程的早期单一步骤计算块级注意力重要性分数并生成稀疏掩码，缓存后在所有后续步骤中直接复用，从而将掩码计算成本从每步循环中剥离。RAPID 包含两个工作模式：**默认模式**直接复用缓存掩码，实现高质量加速；**Turbo 模式**利用缓存的重要性分数进行自适应重阈值化，在后期步骤应用更激进的剪枝，进一步压缩计算量。

在 Wan2.1-14B 和 HunyuanVideo 两个大规模视频扩散模型上的实验表明，在相同注意力密度预算下，RAPID 默认模式的生成质量显著优于最强基线方法（PSNR 提升高达 4.0），同时实现 1.53–1.73× 加速；Turbo 模式则进一步将加速比推至 1.79×（Wan2.1-14B）和 2.01×（HunyuanVideo），且保持有竞争力的视觉质量。该方法属于训练后加速技术，无需模型微调，可直接应用于现有视频 DiT 架构。



### 视频扩散模型的注意力瓶颈

视频扩散模型的核心模块是 **3D 全注意力（3D self-attention）**，它对时空序列中的所有 token 两两计算注意力权重。对于一个长度为 $N$ 的时空 token 序列，标准注意力的计算复杂度为 $O(N^2)$。当生成高分辨率长视频时，$N$ 急剧膨胀，导致单次推理的注意力计算成本成为整个扩散过程的主导开销——例如，在 Wan2.1-14B 模型上，使用密集注意力生成一段视频的延迟可达 **66 分钟**（见 Teaser Figure）。这一二次复杂度瓶颈严重制约了视频扩散模型在实际应用中的部署效率。

### 现有稀疏注意力方法的困境

为缓解上述瓶颈，研究者提出了多种稀疏注意力策略，其核心思想是通过二值掩码 $M$ 对注意力对数进行选择性遮蔽，从而减少实际参与计算的 token 对数量。稀疏注意力的通用形式为：

$${ \mathrm { A t t n } } _ { \mathrm { s p a r s e } } ( Q , K , V ) = { \mathrm { s o f t m a x } } \left( { \frac { Q K ^ { \top } } { \sqrt { d } } } \odot M ^ { \prime } \right) V ,$$

其中 $M'_{ij} = 0$ 表示保留该注意力连接，$M'_{ij} = -\infty$ 表示丢弃。问题的核心在于如何构建一个既能最大化稀疏度、又能保持生成质量的掩码 $M$。

现有方法可归为两类，各自存在明显缺陷：

- **动态稀疏注意力**（如 **X-Attention**，Xu et al., ICML 2025）：在每个去噪步骤均需重新估计 token 重要性并动态生成掩码。这类方法虽然具备内容自适应性，但每步重新计算掩码本身引入了可观的额外开销，部分抵消了稀疏化带来的加速收益。

- **静态稀疏注意力**（如 **Sparse VideoGen (SVG)**，Xi et al., arXiv 2025；**Radial Attention**，Li et al., arXiv 2025）：使用预定义的固定时空掩码模式，无需每步重新估计。这类方法虽然避免了重复计算，但由于掩码缺乏对具体内容的适应性，在保持生成质量方面存在天然劣势，难以在高加速比下维持视觉保真度。

### 动机：从注意力密度的时间特性中寻找突破口

RAPID 的动机源于对视频扩散过程中注意力行为的两项关键实证观察（**Figure 2** 和 **Figure 3**）：

1. **注意力密度需求的时间稳定性与递减趋势**：在 Wan2.1-14B 和 HunyuanVideo 两个模型上，各层在不同去噪步骤中达到 95% 分数召回所需的最小注意力密度呈现出两个显著规律——各步骤的密度曲线紧密聚集在均值附近，表现出**强时间稳定性**；同时，所需的平均密度随去噪步推进而**逐渐衰减**（Figure 2 红色虚线）。这意味着早期步骤的掩码模式在后续步骤中仍然高度相关，且后期步骤对稀疏剪枝的容忍度更高。

2. **早期掩码的高召回率与复用安全性**：以第 5 步为基准进行掩码复用性分析（**Figure 3**），使用公式 $\mathrm{Recall}(M_{base}, M_t) = \frac{|M_{base} \cap M_t|}{|M_t|}$ 衡量早期掩码 $M_{base}$ 对后续步骤 $M_t$ 重要块的覆盖率。结果显示，在整个生成过程中召回率始终保持在较高水平，为“一次性早期估计并在后续步骤中安全复用”提供了强有力的实证支撑。

基于上述发现，RAPID 的核心动机得以确立：**将重要性评分与每步推理循环解耦**，通过在早期步骤进行一次性的注意力重要性估计并缓存分数与掩码，后续步骤直接复用缓存结果，从而在保持内容自适应性的同时消除重复计算开销。此外，利用密度需求递减的特性，可在后期阶段对缓存分数进行重新阈值化，实现更激进的剪枝，进一步释放加速潜力。



## 核心方法与创新机理

RAPID 的核心创新在于将视频扩散模型中昂贵的**逐步掩码重计算**替换为**一次性评分与缓存复用**范式，并在此基础上引入**多阶段自适应稀疏度调控**，从而在维持生成质量的前提下实现显著加速。

### 1. 从“每步重算”到“一次缓存复用”

现有动态稀疏注意力方法（如 **X-Attention**，Xu et al., ICML 2025）需要在每个去噪步骤重新估计注意力重要性并生成掩码，引入了大量重复计算开销；而静态方法（如 **Sparse VideoGen**，Xi et al., arXiv 2025；**Radial Attention**，Li et al., arXiv 2025）则使用预定义的固定掩码，缺乏内容自适应性。RAPID 改变了这一范式：

- **Changed Slot：掩码计算策略**
  - **Baseline 做法**：每步重新估计重要性并生成掩码（动态方法），或使用预定义固定掩码（静态方法）。
  - **RAPID 做法**：在早期单一步骤（预热阶段结束时）进行一次密集注意力计算，同时计算块级注意力重要性分数并生成初始高保真掩码 $M_{base}$，将分数和掩码持久化缓存。后续步骤直接复用缓存掩码（默认模式），或通过重新阈值化缓存分数动态调整掩码密集度（Turbo 模式）。

这一设计的可行性建立在两个关键实证发现之上（Figure 2, Figure 3）：
1. **时间稳定性**：在初始预热后，高重要性注意力模式表现出强时间稳定性——各步骤达到 95% 分数召回所需的最小注意力密度在不同去噪步之间高度聚集。
2. **高召回率**：以第 5 步为基准计算的一次性掩码，在后续所有步骤中始终保持高召回率（Coverage），证明早期单次估计能够安全覆盖后续步骤的重要 token。

### 2. 多阶段自适应稀疏度调控

RAPID 的第二个关键创新是利用去噪过程中注意力密度需求的**渐进衰减**特性，实现分阶段的自适应剪枝。

- **Changed Slot：稀疏度调控**
  - **Baseline 做法**：整个生成过程保持固定稀疏度水平。
  - **RAPID 做法**：采用多阶段自适应策略——早期阶段使用保守的高保真掩码，后期阶段基于密度衰减现象应用更激进的剪枝。具体而言，Turbo 模式在去噪后期利用缓存的重要性分数进行重新阈值化，生成更稀疏的掩码，从而在质量损失可控的前提下进一步提升加速比。

### 3. 混合块选择策略

在掩码构建层面，RAPID 提出了一种**混合块选择策略**（Hybrid Block Selection），结合 Top-K 和 Top-p 两种机制：
- **Top-K 锚定**：对每个查询块强制保留 $k_{min}$ 个最重要的关键块，确保基础连接不被切断。
- **Top-p 扩展**：在 Top-K 基础上，通过累积注意力质量达到阈值 $\tau$ 的方式动态扩展所选块，使掩码密度能够自适应内容复杂度。

消融实验（Table 2）证实，该混合策略在所有注意力密度下均优于单独使用 Top-p 或 Top-K，验证了组合的必要性。

### 创新总结

RAPID 的方法创新可归纳为三个层次：
1. **计算解耦**：将重要性评分从每步推理循环中解耦，通过一次性缓存消除重复计算。
2. **时间自适应**：利用去噪过程的密度衰减规律，在后期阶段实现更激进的剪枝。
3. **内容自适应**：通过混合块选择策略，使稀疏掩码能够动态适应不同区域的内容复杂度。

这三个层次的创新协同作用，使得 RAPID 在相同的注意力密度预算下，质量显著优于最强基线方法（PSNR 提升高达 4.0），同时 Turbo 模式在 Wan2.1-14B 上实现 1.79× 加速、在 HunyuanVideo 上实现 2.01× 加速。



RAPID 框架的核心思想是将重要性评分从逐步推理循环中解耦，通过“一次性估计—缓存—复用”的范式替代传统动态稀疏注意力方法中每步重新计算掩码的冗余开销。如图 4 所示，整个推理流程分为三个明确阶段：

### 1. 预热阶段（Warm-up Phase）
在去噪过程的最初几步（$t < T_w$），框架保持标准的密集注意力（Dense Attention）计算。这一阶段的目标是建立稳定的特征表示，为后续的稀疏化决策提供可靠基础。预热比例 $T_w$ 是一个关键超参数：实验表明，将稀疏掩码应用于 10%–25% 的关键早期窗口，比完全依赖密集注意力预热更有利于平衡加速与质量；延长预热超过 25% 后边际收益递减（Figure 5）。

### 2. 一次性评分与缓存阶段（Scoring & Caching Phase）
在预热结束时刻 $t = T_w$，框架触发唯一一次密集注意力计算，同时完成两项任务：
- **块级重要性评分**：基于注意力权重计算每个查询块与关键块之间的重要性分数，并持久缓存这些分数。
- **基础掩码生成**：利用混合块选择策略（Hybrid Block Selection）从重要性分数中生成一个高保真的二值稀疏掩码 $M_{base}$，并同样缓存。

这一阶段的计算开销仅发生一次，后续所有步骤均无需再执行密集注意力或重新估计掩码。

### 3. 缓存复用阶段（Cached Reuse Phase）
对于 $t > T_w$ 的所有后续去噪步骤，框架提供两种工作模式：

- **默认模式（Mask Reuse）**：直接复用缓存的掩码 $M_{base}$，在保持高质量的前提下实现稳定加速。该模式在 Wan2.1-14B 上达到 1.53× 加速，在 HunyuanVideo 上达到 1.73× 加速（Table 1）。
- **Turbo 模式（Adaptive Pruning）**：利用缓存的重要性分数，通过重新阈值化（re-thresholding）生成更激进的稀疏掩码。这一模式基于关键发现——去噪后期所需的注意力密度逐渐衰减（Figure 2），因此在后期阶段可以安全地应用更强剪枝。Turbo 模式在 Wan2.1-14B 上将加速提升至 1.79×，在 HunyuanVideo 上提升至 2.01×，同时保持有竞争力的视觉质量（Table 1）。

### 混合块选择策略（Hybrid Block Selection）
掩码生成的核心是混合块选择策略，它结合了两种机制的互补优势：
1. **Top-k 锚定**：对每个查询块，先选取注意力分数最高的 $k$ 个关键块，确保基础连接不被遗漏。
2. **Top-p 扩展**：在 Top-k 基础上，按累积注意力质量达到阈值 $\tau$ 的标准动态添加更多关键块，使掩码密度自适应内容复杂度。

消融实验证实，该混合策略在所有注意力密度下均优于单独使用 Top-p 或 Top-k（Table 2），阈值 $\tau = 0.6$ 可在与最强基线相似的计算密度下实现最优质量（Figure 6）。

### 输入输出流
- **输入**：视频扩散模型去噪过程中各 Transformer 层的查询（$Q$）、键（$K$）、值（$V$）张量。
- **输出**：经稀疏注意力计算后的特征表示，计算方式为 $\mathrm{Attn}_{\mathrm{sparse}}(Q, K, V) = \mathrm{softmax}\left(\frac{QK^\top}{\sqrt{d}} \odot M'\right) V$，其中 $M'$ 为由缓存掩码导出的二值遮蔽矩阵（$M'_{ij} = 0$ 表示保留，$M'_{ij} = -\infty$ 表示丢弃）。
- **缓存状态**：块级重要性分数矩阵与基础掩码 $M_{base}$ 在评分阶段写入，复用阶段只读，无需额外计算。

### 补充图表

![[assets/figures/papers/paper_list_l915_https_openaccess_thecvf_com_content_CVPR2026_html_Lin_RAPID_Reusing_Atte/figures/004_Figure_4.jpg]]
*Figure 4: The RAPID framework accelerates inference via a multi-stage strategy. First, at the end of the warmup phase, it computes and caches a base mask and per-block importance scores derived from attention weights. This mask is then reused throughout generation, while the scores are leveraged to activate a more aggressive block pruning in later, less critical steps for maximum speed*



### 3.1 稀疏注意力的形式化与核心挑战

视频扩散模型中的全注意力（3D self-attention）计算复杂度为 $O(N^2)$，其中 $N$ 为时空 token 总数，这构成了推理成本的主要瓶颈。稀疏注意力通过在注意力对数上施加二值掩码来削减计算量，其形式化定义为：

$${ \mathrm { A t t n } } _ { \mathrm { s p a r s e } } ( Q , K , V ) = { \mathrm { s o f t m a x } } \left( { \frac { Q K ^ { \top } } { \sqrt { d } } } \odot M ^ { \prime } \right) V ,$$

其中 $M'_{ij} = 0$（当 $M_{ij} = 1$ 时保留该注意力连接），否则 $M'_{ij} = -\infty$（丢弃该连接）。$M \in \{0,1\}^{N_b \times N_b}$ 为块级二值掩码，$N_b$ 为块的数量。

核心挑战在于：如何在最大化稀疏度（即最小化非零元素数量）的同时，保持模型的生成保真度。现有方法分为两类——动态方法（如 **X-Attention**，Xu et al., ICML 2025）在每个去噪步骤重新估计掩码，引入大量重复计算；静态方法（如 **Sparse VideoGen / SVG**，Xi et al., arXiv 2025；**Radial Attention**，Li et al., arXiv 2025）使用固定模式，缺乏内容自适应性。

### 3.2 关键观察：注意力密度的时间稳定性与衰减

RAPID 的设计建立在两个经验发现之上（详见 Figure 2）：

![[assets/figures/papers/paper_list_l915_https_openaccess_thecvf_com_content_CVPR2026_html_Lin_RAPID_Reusing_Atte/figures/002_Figure_2.jpg]]
*Figure 2: We compute, for each transformer layer and each denoising step, the minimal attention density required to preserve 95% score recall for (a) Wan2.1-14B and (b) HunyuanVideo. In both models, two key phenomena are evident: 1) The individual step profiles (light grey lines) cluster tightly around a mean, demonstrating strong temporal stability. 2) The overall mean density required per step (red dashed line, top axis) progressively decays, indicating that later steps are more tolerant to sparsity*

1. **时间稳定性**：在初始预热后，各层的注意力密度需求在不同去噪步骤间高度聚集，表明高重要性注意力模式在时间上具有强稳定性。
2. **密度衰减**：随着去噪过程推进，维持 95% 分数召回所需的最小注意力密度（红色虚线）逐渐递减，后期步骤对稀疏剪枝的容忍度更高。

这两个特性为“一次性估计、多次复用”提供了理论依据。

### 3.3 掩码复用性的量化度量

为评估早期掩码在后续步骤中的有效性，RAPID 引入两个度量指标。设 $M_{base}$ 为在步骤 $t_{base}$ 估计的掩码，$M_t$ 为步骤 $t$ 的参考掩码：

- **掩码精确率（Precision / Relevance）**：衡量 $M_{base}$ 中的块在 $M_t$ 中仍被保留的比例，反映早期掩码的持续相关性。

$$\mathrm{Precision}(M_{base}, M_t) = \frac{|M_{base} \cap M_t|}{|M_{base}|}$$

- **掩码召回率（Recall / Coverage）**：衡量 $M_{base}$ 覆盖 $M_t$ 所需重要块的比例，反映单次估计的安全性。

$$\mathrm{Recall}(M_{base}, M_t) = \frac{|M_{base} \cap M_t|}{|M_t|}$$

实验表明（Figure 3），以第 5 步为基准的掩码在后续所有步骤中保持持续高召回率，为早期一次性估计的安全性和有效性提供了有力证据。

![[assets/figures/papers/paper_list_l915_https_openaccess_thecvf_com_content_CVPR2026_html_Lin_RAPID_Reusing_Atte/figures/003_Figure_3.jpg]]
*Figure 3: Analysis of mask reusability with a baseline at an early stage (step 5). (a) Precision (Relevance) measures how many of the blocks selected at step 5 remain important in subsequent steps. (b) Recall (Coverage) measures how well the step-5 mask covers the important blocks required by subsequent steps. The consistently high recall provides strong evidence for the safety and effectiveness of an early one-shot estimation*

### 3.4 混合块选择策略（Hybrid Block Selection）

RAPID 采用 Top-K + Top-p 的混合策略构建稀疏掩码，融合了两种机制的互补优势：

1. **Top-K 锚定（Top-K Anchor）**：对每个查询块，强制选择注意力分数最高的 $k_{min}$ 个关键块，确保基础连接的最低保障。
2. **Top-p 扩展（Top-p Expansion）**：在 Top-K 基础上，继续累积注意力质量直至达到阈值 $\tau$，动态适应不同内容的复杂度差异。

该混合策略的核心优势在于：Top-K 组件提供了鲁棒的基础连接基线，而 Top-p 组件引入了内容感知的自适应能力。消融实验（Table 2）证实，该混合策略在所有注意力密度下均优于单独使用 Top-p 或 Top-K。

### 3.5 多阶段推理管线

RAPID 框架（Figure 4）将推理过程划分为三个有序阶段：

**阶段一：预热阶段（Warm-up Phase，$t < T_w$）**
保持标准密集注意力计算，建立稳定的特征表示，为后续重要性评分提供可靠基础。

**阶段二：一次性评分与缓存阶段（Scoring & Caching Phase，$t = T_w$）**
在预热结束时触发唯一一次密集注意力计算，同时计算块级注意力重要性分数并生成初始高保真掩码 $M_{base}$。分数矩阵与掩码均被持久化缓存，将重要性评分与逐步推理循环解耦。

**阶段三：缓存复用阶段（Cached Reuse Phase，$t > T_w$）**
- **默认模式（Mask Reuse）**：直接复用缓存的 $M_{base}$，无需任何额外计算。
- **Turbo 模式（Adaptive Pruning）**：在去噪后期（$t \geq t_a$），利用缓存分数重新阈值化生成更激进的稀疏掩码，实现进一步加速。该模式直接利用了密度衰减现象——后期步骤对稀疏度容忍更高，因此可在缓存分数基础上施加更严格的剪枝超参数。

### 3.6 关键超参数与控制变量

RAPID 的行为由以下核心超参数调控：

| 超参数 | 含义 | 作用阶段 |
|--------|------|----------|
| $T_w$ | 预热比例（占总步数的百分比） | 阶段划分 |
| $k_{min}$ | 每个查询块的最小保留关键块数 | 掩码构建（Top-K） |
| $\tau$ | 累积注意力质量阈值 | 掩码构建（Top-p） |
| $t_a$ | Turbo 模式触发步 | 自适应剪枝 |

敏感性分析表明：预热比例 $T_w$ 在 10%-25% 区间内可有效平衡加速与质量，延长预热超过 25% 后边际收益递减（Figure 5）；阈值 $\tau = 0.6$ 在与 SOTA 基线相似的计算密度下实现最优质量（Figure 6）。当前这些超参数依赖人工调优，缺乏自动学习或自适应调度的能力，这是 RAPID 的一个显式局限。



## 实验与关键发现

### 主实验结果

RAPID 在两个主流视频扩散模型 **Wan2.1-14B** 和 **HunyuanVideo** 上，以 VBench-2.0 基准进行了全面评估。所有基线方法均经过最小超参数调优，控制在约 42-44% 的注意力密度下，确保在与 RAPID 可比的计算预算内进行公平对比。

**Table 1** 汇总了主要定量结果。在 Wan2.1-14B 上，RAPID 默认模式以 1.53× 加速比取得 26.112 PSNR，相较最强基线提升高达 4.0 PSNR 点，同时 SSIM 达 0.871、LPIPS 低至 0.096。Turbo 模式进一步将加速推至 1.79×，且保持有竞争力的视觉质量。在 HunyuanVideo 上，默认模式实现 1.73× 加速，PSNR 31.488、SSIM 0.948、LPIPS 0.073；Turbo 模式达到 2.01× 加速，所有指标均显著优于各稀疏注意力基线。

这一结果的核心驱动力来自 RAPID 的“一次性评分与缓存复用”范式：它从根本上消除了动态方法（如 **X-Attention**，Xu et al., ICML 2025）每步重新估计掩码的重复计算开销，同时通过混合块选择策略（Top-K Anchor + Top-p Expansion）获得了远超静态方法（如 **SVG**，Xi et al., arXiv 2025；**Radial Attention**，Li et al., arXiv 2025）的内容自适应性。

### 消融实验

**混合块选择策略的必要性**：**Table 2** 展示了在不同注意力密度下，单独使用 Top-p 或 Top-K 策略与 RAPID 混合策略的对比。结果表明，混合策略在所有密度水平上均一致优于单独方案。其机理在于：Top-K 组件通过保证最小必要连接集建立了鲁棒的基线，而 Top-p 组件则增加了内容感知的自适应层，使掩码能动态适应不同查询块的复杂度差异。

**预热时长的敏感性**：**Figure 5** 分析了 Wan2.1-14B 上生成质量随预热比例的变化。将稀疏掩码应用在关键的 10%-25% 早期窗口，相比完全依赖密集注意力预热，更有利于平衡加速与质量。延长预热超过 25% 后边际收益递减，这为 RAPID 的多阶段策略设计提供了实证依据。

**阈值 τ 的权衡**：**Figure 6** 展示了在 T_w=25% 配置下，τ 从 0.5 到 0.9 变化时注意力密度与生成质量的权衡关系。增加 τ 带来质量提升，但同时引入更多冗余计算。τ=0.6 被选为最优平衡点，在与 SOTA 基线相似的计算密度下实现了最优质量。

### 失败模式与局限性

尽管 RAPID 在质量和效率上均表现优异，仍存在以下局限：

1. **超参数依赖人工调优**：当前剪枝超参数（k_min、τ、预热比例 T_w、Turbo 触发步 t_a）均需手动设定，缺乏自动学习或自适应调度能力。这限制了方法在不同模型和场景下的即插即用性。

2. **模型覆盖范围有限**：实验仅在 Wan2.1-14B 和 HunyuanVideo 两款模型上验证，尚未广泛测试其他视频 DiT 架构。对于极长视频或更高分辨率场景下的扩展性，目前缺乏深入分析。

3. **与其他加速手段的协同未知**：RAPID 属于训练后加速方法，尚未与蒸馏、量化等正交加速技术结合测试，其综合加速上限有待探索。

### 关键图表结论

- **Figure 2** 揭示了方法设计的核心动机：注意力密度需求在去噪过程中表现出强时间稳定性，且所需平均密度逐渐递减，后期步骤对稀疏剪枝的容忍度更高。
- **Figure 3** 验证了复用策略的安全性：以第 5 步为基准的一次性掩码，在后续所有步骤中保持高召回率（Coverage），为早期单次估计的有效性提供了有力证据。
- **Table 1** 确立了 RAPID 在质量-效率 Pareto 前沿上的优势地位：在相同注意力密度预算下，质量显著超越所有基线；Turbo 模式更以 2.01× 加速比拓展了效率边界。

![[assets/figures/papers/paper_list_l915_https_openaccess_thecvf_com_content_CVPR2026_html_Lin_RAPID_Reusing_Atte/figures/005_Table_1.jpg]]
*Table 1: Quantitative results at the default video length over VBench-2.0. Our method significantly outperforms strong baselines on PSNR, SSIM, and LPIPS metrics under a comparable attention density. Furthermore, our Turbo sparse mode accelerates inference by 1.79× on Wan2.1-14B and 2.01× on HunyuanVideo using a single NVIDIA A100 GPU, while maintaining competitive quality*

### 补充图表

![[assets/figures/papers/paper_list_l915_https_openaccess_thecvf_com_content_CVPR2026_html_Lin_RAPID_Reusing_Atte/figures/006_Table_2.jpg]]
*Table 2: Ablation on Block Selection mechanisms across different attention densities, evaluated on Wan2.1-14B. Our combined Top-K + Top-p strategy consistently outperforms individual methods*

![[assets/figures/papers/paper_list_l915_https_openaccess_thecvf_com_content_CVPR2026_html_Lin_RAPID_Reusing_Atte/figures/008_Figure_5.jpg]]
*Figure 5: Sensitivity of generation quality to warm-up duration on Wan2.1-14B. While quality improves with longer warm-ups, the rate of improvement diminishes*

![[assets/figures/papers/paper_list_l915_https_openaccess_thecvf_com_content_CVPR2026_html_Lin_RAPID_Reusing_Atte/figures/007_Figure_6.jpg]]
*Figure 6: Sensitivity analysis of the threshold τ for the*

![[assets/figures/papers/paper_list_l915_https_openaccess_thecvf_com_content_CVPR2026_html_Lin_RAPID_Reusing_Atte/figures/001_Figure.jpg]]
*Figure: Dense Attention | Latency = 66 min*



## 定位与知识库关联

### 核心机制定位

RAPID 属于**训练后稀疏注意力加速**范式，其核心创新在于将“掩码估计”与“推理循环”解耦。与现有方法的根本区别在于：

- **动态稀疏方法**（如 **X-Attention**，Xu et al., ICML 2025）在每个去噪步骤都重新计算注意力重要性并生成掩码，虽然内容自适应性强，但引入了大量重复的计算开销。
- **静态稀疏方法**（如 **Sparse VideoGen (SVG)**，Xi et al., arXiv 2025；**Radial Attention**，Li et al., arXiv 2025）使用预定义的固定时空掩码或能量衰减模式，避免了每步重算的开销，但缺乏内容自适应性，在保持高质量的同时难以进一步加速。

RAPID 通过**一次性早期估计与缓存复用**机制，同时获得了动态方法的内容自适应性和静态方法的计算效率：在早期单一步骤计算块级注意力重要性分数并缓存，后续步骤直接复用缓存掩码（默认模式），或通过重新阈值化缓存分数动态调整掩码密集度（Turbo 模式）。

### 关键设计决策与适用边界

**混合块选择策略（Top-K + Top-p）的必然性**。消融实验（Table 2）表明，单独使用 Top-p 或 Top-K 在不同注意力密度下均劣于混合策略。其因果机制在于：Top-K 组件通过保证最小必要连接集合建立了鲁棒的质量基线，而 Top-p 组件则根据内容复杂度动态扩展关键块，实现了内容自适应的计算分配。这一设计使得 RAPID 在约 42-44% 注意力密度的可比计算预算下，PSNR 提升高达 4.0（最强基线估算值约 22.1 PSNR，RAPID 达 26.112 PSNR）。

**多阶段自适应稀疏度的必要性**。RAPID 的阶段性设计——预热阶段保持密集注意力、早期阶段使用保守的高保真掩码、后期阶段应用更激进的剪枝——并非经验性技巧，而是基于两个关键观察：1）注意力密度需求在去噪过程中表现出强时间稳定性，且所需的平均密度逐渐递减（Figure 2）；2）将稀疏掩码应用在 10%-25% 关键早期窗口比完全依赖密集注意力预热更有利于平衡加速和质量，延长预热超过 25% 的边际收益递减（Figure 5）。这构成了 RAPID 方法有效性的核心因果机制。

**Turbo 模式的加速边界**。Turbo 模式通过简单的缓存分数重阈值化实现最高 2.01× 加速（HunyuanVideo），其有效性依赖于后期步骤对稀疏剪枝的更高容忍度。但该模式的质量保持依赖于缓存分数的时间稳定性——若去噪过程中注意力分布发生剧烈偏移，重阈值化可能引入不可恢复的质量损失。

### 局限与开放问题

**当前局限**：

1. **超参数依赖人工调优**。剪枝超参数（k_min、τ、预热比例 T_w、Turbo 触发步 t_a）依赖手动设置，缺乏自动学习或自适应调度的能力。阈值 τ 的敏感性分析（Figure 6）显示，τ 增加带来质量提升但冗余计算增加，选择 τ=0.6 可在与 SOTA 基线相似的计算密度下实现最优质量，但这一选择可能不适用于其他模型或任务。
2. **模型覆盖范围有限**。实验仅在两款模型（Wan2.1-14B 与 HunyuanVideo）上验证，未广泛测试其他视频 DiT 架构。对于极长视频或更高分辨率场景下的扩展性尚未深入分析，需要手动验证。
3. **未与正交加速手段结合**。方法属于训练后加速，未与蒸馏或量化等加速手段结合测试，综合加速效果未知。

**开放问题**：

1. **可学习的稀疏度调度器**。能否利用缓存的重要性分数设计可学习的稀疏度调度器，使阈值 τ 或 k_min 随去噪步动态衰减以进一步提升效率？这需要解决“如何在无额外密集注意力监督的情况下学习调度策略”的问题。
2. **跨注意力类型的扩展**。若将一次性评分与缓存的思想扩展到其他注意力类型（如交叉注意力），或结合量化/蒸馏，能否取得更大的累积加速？交叉注意力的稀疏模式可能具有不同的时间稳定性特征，需要独立分析。
3. **Turbo 模式的质量-加速权衡自动化**。当前 Turbo 模式的触发步和剪枝强度依赖人工设定，能否基于缓存分数的统计特征（如方差、衰减率）自动决定何时以及如何进行更激进的剪枝？



## 原文 PDF

![[paperPDFs/CVPR_2026/RAPID_Reusing_Attention_Sparsity_with_Inter_step_Adaptation_for_Efficient_Video_Diffusion.pdf]]
