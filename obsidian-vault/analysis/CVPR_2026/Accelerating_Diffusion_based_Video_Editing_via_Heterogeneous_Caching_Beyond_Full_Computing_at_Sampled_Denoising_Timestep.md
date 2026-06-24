---
title: "Accelerating Diffusion-based Video Editing via Heterogeneous Caching: Beyond Full Computing at Sampled Denoising Timestep"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/Accelerating_Diffusion_based_Video_Editing_via_Heterogeneous_Caching_Beyond_Full_Computing_at_Sampled_Denoising_Timestep.pdf
project_link: null
code_link: null
aliases:
- Accelerating_Dif
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/generative_models_diffusion
- topic/benchmarks_datasets_evaluation
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: 基于时间步累积输入变化估计选择全计算/部分计算/重用步骤，并结合编辑掩膜空间先验将token划分为上下文、边界、生成三类，通过轻量K-Means聚类和缓存注意力相关性评分仅保留最具语义代表性与生成token高度交互的上下文token，从而在保持编辑一致性同时大幅减少冗余注意力计算。
primary_logic: 利用MV2V编辑的ROI特性，将token异质性引入缓存决策——并非所有上下文token都对生成区同等重要，通过聚类代表性和交互强度双约束筛选上下文token，实现解码阶段注意力计算的精准裁剪。
claims:
- HetCache-fast在VACE-Benchmark视频修复上取得2.67×延迟加速和大幅FLOPs降低，同时质量退化可忽略。
- 消融实验表明，同时移除K-Means语义代表性和注意力相关性指导会导致VBench分数下降（76.19 vs 76.29）和可视化质量劣化（重影、边界不光滑）。
- 在高分辨率和长视频上加速比进一步提升（2.91×和3.06×），验证了方法对token计数增长的有效性。
- VACE-Benchmark video inpainting (Wan2.1-VACE) 上 Latency (s) = 166.81
---

# Accelerating Diffusion-based Video Editing via Heterogeneous Caching: Beyond Full Computing at Sampled Denoising Timestep

> [!tip] 核心洞察
> 利用MV2V编辑的ROI特性，将token异质性引入缓存决策——并非所有上下文token都对生成区同等重要，通过聚类代表性和交互强度双约束筛选上下文token，实现解码阶段注意力计算的精准裁剪。

| 字段 | 内容 |
|------|------|
| 中文题名 | 通过异构缓存加速基于扩散的视频编辑：超越去噪时间步的全计算 |
| 英文题名 | Accelerating Diffusion-based Video Editing via Heterogeneous Caching: Beyond Full Computing at Sampled Denoising Timestep |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2603.24260) |
| Topic | #topic/vision_multimodal_applications #topic/generative_models_diffusion #topic/benchmarks_datasets_evaluation #topic/vision_multimodal_applications/image_and_video_generation |
| Method | HetCache |
| Dataset | VACE-Benchmark video inpainting, VACE-Benchmark text-guided editing, VPBench text-guided editing |

> [!tip] 效果简介
> - VACE-Benchmark video inpainting (Wan2.1-VACE) 上，Latency (s) 166.81 (2.67× speedup)。
> - VACE-Benchmark video inpainting 上，FLOPs (P) 23.60 (与2.67×加速一致)。
> - VACE-Benchmark text-guided editing 上，Latency (s) 128.61 (1.91× speedup)。

## 概述

**问题背景与瓶颈** 基于扩散Transformer（DiT）的视频编辑虽能生成高质量结果，但推理计算开销极大。现有加速方法通常只关注单一维度冗余：要么利用去噪时间步间的特征相似性进行步跳过或缓存，要么在Transformer层内对token进行统一剪枝。然而，MV2V（Masked Video-to-Video）编辑场景存在双重未被充分利用的计算冗余——去噪时间步级冗余和Transformer内token级冗余——且后者因编辑掩膜引入的ROI（感兴趣区域）而呈现显著的**token异质性**：并非所有上下文token对生成区域同等重要，统一缓存全部上下文token会损害生成质量。

**核心方法** 本文提出**HetCache**，一个无需训练的异构缓存框架，首次联合建模去噪时间步冗余和token冗余。其核心洞察在于利用MV2V编辑的ROI特性，将token异质性引入缓存决策。具体而言，HetCache包含两个协同的加速维度：（1）**时间步级自适应调度**——基于相邻时间步调制输入的累积变化估计，将去噪步动态划分为全计算、部分计算和重用三种模式；（2）**token级异构缓存**——利用编辑掩膜空间先验将时空token划分为上下文、边界、生成三类，对上下文token进行轻量K-Means聚类，并结合缓存注意力相关性评分，仅保留最具语义代表性与生成token高度交互的上下文token参与部分计算步的注意力计算。

**关键结果** 在VACE-Benchmark视频修复任务上，HetCache-fast实现**2.67×延迟加速**和大幅FLOPs降低，同时质量退化可忽略；在高分辨率和长视频场景下加速比进一步提升至**2.91×和3.06×**。消融实验证实，同时移除K-Means语义代表性和注意力相关性指导会导致VBench分数下降（76.29→76.19）及可视化质量劣化（重影、边界不光滑），验证了异构缓存策略的必要性。

**方法定位** HetCache属于推理时无训练加速方法，与需要额外训练的蒸馏或量化方法正交，可直接应用于预训练DiT backbone。其异构缓存思想为扩散模型加速提供了从“统一缓存”到“感知异质性缓存”的新范式。

## 背景与动机

### 扩散视频编辑的加速困境

基于扩散Transformer（DiT）的视频编辑模型在生成质量和可控性上取得了显著进展，但其推理开销仍然巨大。核心瓶颈在于DiT架构的双重冗余计算：

**时间步级冗余**：扩散模型在相邻去噪时间步之间，输入特征高度相似，每一步都执行全计算会引入大量不必要的重复运算。现有缓存方法虽然尝试利用这一特性，但普遍采用“全计算或重用”的二元决策，缺乏对中间状态的自适应处理能力。

**Token级冗余**：DiT的Transformer层中，时空token之间的稠密自注意力计算复杂度为$\mathcal{O}(X^{2})$，其中$X = X_{c} + X_{m} + X_{g}$（上下文、边界、生成token）。大量上下文token（$X_{c}$）与生成token（$X_{g}$）之间的交互对最终编辑结果的贡献有限，却占据了注意力计算的主要开销。

### 现有方法的缺口

当前针对DiT推理加速的方法存在两方面关键缺陷：

1. **忽视MV2V编辑的token异质性**：掩码视频到视频（MV2V）编辑任务中，编辑掩膜定义了明确的感兴趣区域（ROI），使得不同空间位置的token对编辑质量的贡献天然存在差异。然而，现有缓存方法统一对待所有token，要么全部保留要么全部丢弃，既浪费计算资源又可能损害生成质量。

2. **缺乏精细化的上下文选择机制**：即使意识到需要削减上下文token的计算，现有方法也缺乏有效的选择策略。简单的随机采样或均匀采样无法区分语义代表性高与低的token，导致缓存中保留了大量冗余信息，同时可能丢弃对生成区域重要的上下文线索。

### 本文动机

针对上述缺口，本文提出**HetCache**（异构缓存）框架，核心动机在于：

- **联合建模双重冗余**：在时间步维度引入“部分计算”模式，根据累积输入变化自适应决定每一步的计算强度，而非简单的全计算/重用二选一。
- **引入token异质性先验**：利用MV2V编辑特有的编辑掩膜空间先验，将token划分为上下文、边界、生成三类，并仅对上下文token实施选择性缓存。
- **双约束的上下文token筛选**：通过轻量K-Means聚类保持语义代表性，同时利用缓存注意力矩阵计算每个上下文token与生成token的交互强度，仅在每个语义簇内保留最具代表性的高交互token，实现注意力计算的精准裁剪。

这种设计使得HetCache能够在保持编辑一致性的前提下，大幅减少冗余的注意力计算，实现训练无关的即插即用加速。

## 核心创新

HetCache 的核心创新在于将**掩膜视频到视频（MV2V）编辑中固有的 token 异质性**引入缓存决策，从而同时解决 DiT 推理中两个维度的计算冗余：去噪时间步间的特征相似性与 Transformer 层内上下文 token 间的稠密自注意力开销。与现有统一缓存所有 token 的方法不同，HetCache 通过编辑掩膜提供的空间先验，对时空 token 进行差异化处理，仅保留对生成质量真正关键的上下文 token 参与注意力计算。

### 创新一：基于累积输入变化的三态时间步调度

传统 DiT 推理在每一步执行全计算，忽视了相邻时间步间特征的高度相似性。HetCache 引入了一种**无训练的累积距离调度器**，根据时间步调制输入的相对变化自动切换计算模式。

具体而言，定义每步相对输入变化为：

$$L_{1}^{\mathrm{rel}}(F, t) = \frac{|F_{t} - F_{t+1}|_{1}}{|F_{t+1}|_{1}}$$

其中 $F_t = T_t \odot x_t$ 为时间步嵌入调制的输入。从锚点步 $a$ 到当前步 $b$ 的累积差异为：

$$D_{a \to b} = \sum_{t=a}^{b-1} L_{1}^{\mathrm{rel}}(F, t)$$

根据 $D_{a \to b}$ 与阈值 $\Delta$ 的关系，将时间步划分为三种模式：
- **全计算步**（$D > 1.5\Delta$）：执行完整注意力并更新缓存；
- **部分计算步**（$\Delta < D \leq 1.5\Delta$）：仅用选定的 token 子集计算注意力，并以 EMA 方式更新缓存；
- **重用步**（$D \leq \Delta$）：完全复用缓存特征，跳过注意力计算。

这一设计将“何时可以少算”的决策建立在**输出变化的可计算代理**之上，而非启发式固定间隔。

### 创新二：基于编辑掩膜的 token 异质性建模与选择性缓存

MV2V 编辑的核心特点是存在明确的感兴趣区域（ROI）。HetCache 利用编辑掩膜 $M$ 将 DiT 的时空 token 划分为三类：
- **生成 token**（$\mathcal{X}_{gen}$）：位于掩膜内部，直接参与内容合成；
- **边界 token**（$\mathcal{X}_{mar}$）：位于掩膜边缘，负责区域过渡；
- **上下文 token**（$\mathcal{X}_{ctx}$）：位于掩膜外部，提供背景语义。

自注意力的二次复杂度可分解为：

$$\mathcal{O}(X^{2}) = \mathcal{O}((X_{c} + X_{m} + X_{g})^{2})$$

其中上下文 token 通常占据绝大多数，但并非所有上下文 token 对生成区域同等重要。HetCache 的**关键洞察**在于：通过聚类代表性和交互强度双约束筛选上下文 token，可在保持编辑一致性的同时大幅裁剪注意力计算。

具体选择策略为：
1. **轻量 K-Means 语义聚类**：对上下文 token 进行聚类，获得 $K$ 个语义簇 $\boldsymbol{S} = \{S_1, S_2, \ldots, S_K\}$，确保所选 token 在语义上具有代表性；
2. **注意力交互评分**：利用全计算步缓存的注意力矩阵，计算每个上下文 token $i$ 对生成 token 的平均注意力：

$$\alpha_i = \frac{1}{|\mathcal{X}_{gen}|} \sum_{j \in \mathcal{X}_{gen}} \bar{A}_{i,j}$$

3. **簇内 Top-$r_{ctx}$ 选择**：在每个语义簇内按 $\alpha_i$ 排序，保留前 $r_{ctx}$ 比例的 token，最终注意力复杂度降至 $\mathcal{O}((r_{ctx} X_l + X_m + X_n)^2)$。

### 与 baseline 的 changed slots 对比

| 设计维度 | Vanilla DiT（Wan2.1-VACE） | HetCache |
|---------|---------------------------|----------|
| 时间步计算模式 | 每步全计算 | 自适应切换全计算/部分计算/重用 |
| 注意力 token 范围 | 全部时空 token | 边界 + 生成 + 筛选后的上下文 token |
| 上下文 token 选择 | 无选择，全部参与 | K-Means 聚类 + 注意力相关性双约束筛选 |

消融实验验证了双约束的必要性：同时移除 K-Means 语义代表性和注意力相关性指导会导致 VBench 分数下降（76.29 → 76.19），并出现重影和边界不平滑等可视化劣化（Table 3, Figure 6）。单独保留任一约束均无法达到完整 HetCache 的性能水平（仅聚类：75.80；仅相关性：76.24），表明语义覆盖与交互强度在缓存决策中具有互补作用。

## 整体框架

HetCache 是一种面向基于扩散的掩膜视频到视频（MV2V）编辑的无训练缓存框架，其核心设计动机在于联合建模扩散过程中**去噪时间步间的冗余**与 DiT backbone 中**时空 token 间的冗余**（Figure 1）。现有方法通常仅关注其中一维，而 HetCache 利用 MV2V 编辑特有的编辑掩膜空间先验，将 token 异质性引入缓存决策，从而在保持编辑一致性的前提下大幅裁剪冗余计算。

![[assets/figures/papers/paper_list_l832_https_arxiv_org_abs_2603_24260/figures/001_Figure_1.jpg]]
*Figure 1: (a). Illustration of the acceleration dimensions in Diffusion Transformers (DiTs). Unlike existing methods, the proposed Heterogeneous Caching (HetCache) jointly models denoising-step redundancy in the diffusion process and token redundancy within the Transformer backbone. (b). As a tailored heterogeneous strategy, HetCache accelerates diffusion-based masked video-to-video (MV2V) editing while maintaining generation quality*

### 框架总览

Figure 2 给出了 HetCache 的整体流程。对于一次 MV2V 编辑推理，系统首先将编辑掩膜 $M$ 与噪声输入一同送入 DiT 去噪网络 $\mathcal{G} = g_1 \circ g_2 \circ \cdots \circ g_L$。在每个去噪时间步，HetCache 依次执行以下关键模块：

![[assets/figures/papers/paper_list_l832_https_arxiv_org_abs_2603_24260/figures/002_Figure_2.jpg]]
*Figure 2: The overview of our proposed HetCache scheme. In denoising process, we use the timestep-embeddings-modulated-input [18] to estimate the computing demand. According to the accumulated distance, Full-Compute anchor step, Reuse step and Partial-Compute step will be executed. In full-computing, HetCache will use spatial prior extracted from editing mask to categorize the DiT tokens into Context, Margin, and Generative Tokens. The Context Tokens which takes high portion and cause redundant computation cost will be cached for partial-compute steps according to its semantic representativeness and interaction strength with the generative tokens*

1. **时间步调制输入计算器**  
   根据当前时间步嵌入调制后的输入 $F_t = T_t \odot x_t$，计算相邻步的相对 L1 变化：
   $$L_{1}^{\mathrm{rel}}(F, t) = \frac{|F_{t} - F_{t+1}|_{1}}{|F_{t+1}|_{1}}$$
   该值作为输出变化幅度的代理信号。

2. **累积距离调度器**  
   从最近一次全计算锚点步 $a$ 到当前步 $b$ 累积上述相对变化：
   $$D_{a \to b} = \sum_{t=a}^{b-1} L_{1}^{\mathrm{rel}}(F, t)$$
   根据 $D_{a \to b}$ 与阈值 $\Delta$ 的关系，将当前步划分为三种计算模式：
   - **全计算步**（$D_{a \to b} > 1.5\Delta$）：执行完整注意力计算，并更新缓存中的代表性上下文 token；
   - **部分计算步**（$\Delta < D_{a \to b} \leq 1.5\Delta$）：仅使用选定的上下文 token 子集参与注意力，并以 EMA 方式更新缓存；
   - **重用步**（$D_{a \to b} \leq \Delta$）：完全复用上一步的缓存特征，跳过注意力计算。

3. **Token 类别划分模块**  
   在全计算步中，利用编辑掩膜 $M$ 的空间先验将 DiT 的时空 token 划分为三类：
   - **上下文 token** $\mathcal{X}_{ctx}$：掩膜区域外的 token，数量大但编辑相关性低；
   - **边界 token** $\mathcal{X}_{m}$：掩膜边界附近的 token，对编辑过渡质量敏感；
   - **生成 token** $\mathcal{X}_{gen}$：掩膜区域内的 token，直接决定编辑内容。

   这种划分使得后续的注意力计算复杂度从 $\mathcal{O}(X^2)$ 分解为：
   $$\mathcal{O}((X_{c} + X_{m} + X_{g})^{2})$$

4. **K-Means 语义聚类与重要性估计器**  
   对上下文 token 集合 $\mathcal{X}_{ctx}$ 执行轻量 K-Means 聚类，得到 $K$ 个语义簇 $\boldsymbol{S} = \{S_1, S_2, \ldots, S_K\}$，簇中心为：
   $$\mu_k = \frac{1}{|S_k|} \sum_{x_i \in S_k} x_i$$
   随后利用全计算步缓存的稀疏注意力矩阵，计算每个上下文 token $i$ 对生成 token 的平均注意力作为其重要性分数：
   $$\alpha_i = \frac{1}{|\mathcal{X}_{gen}|} \sum_{j \in \mathcal{X}_{gen}} \bar{A}_{i,j}$$
   在每个簇内按 $\alpha_i$ 降序保留前 $r_{ctx}$ 比例的 token，确保选出的上下文 token 同时具备**语义代表性**（聚类约束）和**与生成区域的高交互强度**（注意力约束）。

5. **部分计算注意力改造**  
   在部分计算步中，仅将选定的上下文 token 子集与边界 token、生成 token 拼接后送入自注意力层。注意力复杂度降至 $\mathcal{O}((r_{ctx} X_l + X_m + X_n)^2)$，其中 $r_{ctx} < 1$ 大幅削减了上下文 token 带来的二次开销。

### 输入输出流

- **输入**：噪声视频潜变量、编辑掩膜 $M$、文本条件、去噪时间步序列。
- **输出**：编辑后的视频潜变量，经 VAE 解码得到最终视频。
- **缓存状态**：全计算步缓存的代表性上下文 token 特征及对应注意力分数，供后续部分计算步和重用步使用。

### 设计要点

HetCache 的关键创新在于将 MV2V 编辑的 ROI 特性系统性地融入缓存策略——并非所有上下文 token 对生成区域同等重要，通过聚类代表性和交互强度双重约束筛选上下文 token，实现了对 DiT 自注意力计算的精准裁剪。该方法无需微调或蒸馏，可直接应用于预训练 DiT backbone。

## 核心模块与公式推导

### 时间步调制输入与累积距离调度器

HetCache 在去噪时间步维度引入自适应计算模式切换，其核心代理信号为**时间步调制输入**（timestep-embeddings-modulated input）。给定时间步 $t$，调制输入定义为：

$$F_t = T_t \odot x_t$$

其中 $T_t$ 为时间步嵌入，$x_t$ 为当前步的噪声潜在表示，$\odot$ 表示逐元素乘积。该量被用作相邻时间步输出变化的代理——其直觉在于：若调制输入变化剧烈，则当前步的去噪输出也可能发生显著改变，需要更精确的计算；反之则可复用或近似。

相邻步的相对输入变化由归一化 L1 距离度量：

$$L_{1}^{\mathrm{rel}}(F, t) = \frac{|F_{t} - F_{t+1}|_{1}}{|F_{t+1}|_{1}} \quad \text{(Eq. 1)}$$

从锚点步 $a$（最近一次全计算步）到当前步 $b$ 的累积差异定义为：

$$D_{a \to b} = \sum_{t=a}^{b-1} L_{1}^{\mathrm{rel}}(F, t) \quad \text{(Eq. 2)}$$

基于累积差异 $D_{a \to b}$ 与阈值 $\Delta$ 的比较，调度器将每个去噪步划分为三种计算模式：

- **全计算步**：$D_{a \to b} > 1.5\Delta$，执行完整 DiT 前向计算并更新缓存；
- **部分计算步**：$1\Delta < D_{a \to b} \leq 1.5\Delta$，仅对选定的 token 子集执行注意力计算，并以 EMA 方式更新缓存；
- **重用步**：$D_{a \to b} \leq 1\Delta$，完全复用上一步的缓存输出，不执行前向计算。

该调度机制在无需微调的条件下，将去噪过程的计算量从“每步全计算”压缩为“按需计算”，构成了时间步维度的第一层加速。

### Token 类别划分与注意力复杂度分解

在 MV2V 编辑任务中，编辑掩膜 $M$ 提供了天然的空间先验。HetCache 利用该先验将 DiT 的时空 token 集合划分为三类：

- **上下文 token**（Context Tokens）：位于掩膜外、与编辑区域无关的 token，数量记为 $X_c$；
- **边界 token**（Margin Tokens）：位于掩膜边界附近的 token，数量记为 $X_m$；
- **生成 token**（Generative Tokens）：位于掩膜内的 token，直接参与编辑内容的生成，数量记为 $X_g$。

DiT 自注意力的二次复杂度可据此分解：

$$\mathcal{O}(X^{2}) = \mathcal{O}((X_{c} + X_{m} + X_{g})^{2}) \quad \text{(Eq. 3)}$$

在典型 MV2V 编辑场景中，上下文 token 占据 token 总数的绝大部分（$X_c \gg X_m + X_g$），但其与生成 token 的交互并非同等重要。HetCache 的核心洞察在于：**并非所有上下文 token 都对生成区同等关键**，通过选择性保留最具代表性的上下文 token 子集，可将注意力复杂度从 $\mathcal{O}((X_c + X_m + X_g)^2)$ 降至 $\mathcal{O}((r_{\mathrm{ctx}} X_c + X_m + X_g)^2)$，其中 $r_{\mathrm{ctx}} \in (0, 1]$ 为上下文 token 保留比例。

### K-Means 语义聚类与注意力重要性估计

为在上下文 token 中筛选出最具代表性的子集，HetCache 采用双重约束策略：语义代表性与生成交互强度。

**语义聚类**：对上下文 token 集合 $\mathcal{X}_{ctx} = \{x_i\}_{i=1}^{X_c}$ 执行轻量 K-Means 聚类，获得 $K$ 个语义簇 $\boldsymbol{S} = \{S_1, S_2, \ldots, S_K\}$，每个簇的中心为：

$$\mu_k = \frac{1}{|S_k|} \sum_{x_i \in S_k} x_i$$

聚类将语义相似的上下文 token 归入同一簇，确保后续从每个簇中采样的 token 能覆盖不同的语义模式。

**注意力重要性估计**：利用全计算步缓存的稀疏注意力矩阵 $\bar{A}$，计算每个上下文 token $i$ 对生成 token 的平均注意力作为其重要性分数：

$$\alpha_i = \frac{1}{|\mathcal{X}_{gen}|} \sum_{j \in \mathcal{X}_{gen}} \bar{A}_{i,j}$$

该分数直接量化了上下文 token 与生成区域的交互强度——$\alpha_i$ 越高，表示该上下文 token 对编辑结果的影响越大。

在每个语义簇 $S_k$ 内，按 $\alpha_i$ 降序排列，保留 top $r_{\mathrm{ctx}}$ 比例的 token。这一双重筛选机制保证了：所选上下文 token 既在语义上具有代表性（覆盖不同簇），又在交互上与生成区高度相关（高注意力分数）。消融实验证实，同时移除聚类（语义代表性）和相关性指导会导致 VBench 分数下降（76.29 → 76.19）并出现重影和边界不平滑等可视化劣化（Table 3, Figure 6）。

### 部分计算步的注意力改造

在部分计算步，DiT 的每个 Transformer block $g_l$ 中的自注意力仅在三类 token 的并集上计算：选定的上下文 token 子集（$r_{\mathrm{ctx}} X_c$ 个）、全部边界 token（$X_m$ 个）和全部生成 token（$X_g$ 个）。该设计将注意力复杂度有效降低至 $\mathcal{O}((r_{\mathrm{ctx}} X_c + X_m + X_g)^2)$，同时保留了最关键的跨类别交互——边界 token 与生成 token 保证编辑边界的平滑过渡，选定的上下文 token 提供必要的全局语义支撑。

全计算步的缓存更新为部分计算步提供了两类关键信息：K-Means 聚类结构（用于语义代表性采样）和注意力矩阵 $\bar{A}$（用于 $\alpha_i$ 计算）。部分计算步以 EMA 方式更新缓存，避免因缓存陈旧导致的误差累积。

## 实验与分析

### 主实验结果

HetCache在VACE-Benchmark和VPBench上进行了系统的效率与质量评估，基础模型为Wan2.1-VACE。Table 1报告了核心量化指标：在视频修复任务上，HetCache-fast实现了**2.67×的延迟加速**，FLOPs降至23.60P；在文本引导视频编辑任务上，加速比为**1.91×**，FLOPs降至13.99P。两种任务下，生成质量的退化均可忽略，验证了异构缓存在保持编辑一致性前提下的显著计算压缩能力。

Table 2进一步展示了方法在不同设定下的泛化性。在高分辨率视频修复（25×720P）场景中，加速比提升至**2.91×**；在长视频修复（57×480P）场景中，加速比进一步达到**3.06×**。这一趋势表明，随着时空token数量的增长，HetCache的冗余裁剪效益愈加显著——上下文token在总token中的占比扩大，选择性缓存的相对收益随之增加。

Figure 3和Figure 4分别从VBench量化评分和可视化质量两个维度进行了对比。HetCache在VBench多项子指标上保持了与全计算基线高度接近的表现，而其他加速方法在画面平滑度、重影和模糊等方面出现明显劣化。可视化结果中，HetCache生成的编辑区域边界清晰、内容一致，未见明显的时序闪烁或语义断裂。

### 消融实验

Table 3和Figure 6报告了上下文token选择策略的消融结果。完整HetCache（同时使用K-Means语义代表性和注意力相关性指导）的VBench-Score为**76.29**。当同时移除这两种指导（即无聚类、无相关性筛选）时，VBench-Score降至**76.19**，且可视化中出现明显的重影和边界不平滑现象，验证了异构token筛选对生成质量的因果贡献。

单独移除某一指导的消融进一步揭示了二者的互补性：仅保留上下文代表性（移除相关性）时，VBench-Score降至**75.80**；仅保留相关性（移除代表性）时，VBench-Score为**76.24**。两者均低于完整HetCache，说明语义聚类确保了对上下文空间的结构化覆盖，而注意力相关性则精准锁定了与生成区高度交互的关键token——二者缺一不可。

### 超参数分析

Figure 5展示了关键超参数的影响。保留上下文token比例 $r_{\mathrm{ctx}}$ 的增加通常带来性能提升，这与更多上下文信息参与注意力计算的正向作用一致。聚类数 $K$ 的变化则未呈现单调趋势：过小的 $K$ 导致语义划分粗糙，代表性不足；过大的 $K$ 引入冗余聚类中心，收益递减。这一现象表明上下文token的语义结构存在有效容量上限，轻量K-Means在 $K=16$ 附近已能充分捕获其分布特征。

### 失败模式与局限性

尽管HetCache在MV2V编辑任务上表现优异，其设计存在以下边界约束：

1. **对编辑掩膜的依赖**：token类别划分（上下文/边界/生成）完全依赖编辑掩膜提供的空间先验。当掩膜质量较低（如边缘不精确、区域覆盖不足）时，边界token的定义可能失准，导致生成区边缘出现伪影或一致性下降。
2. **极低计算预算下的质量退化**：当 $r_{\mathrm{ctx}}$ 设置过低时，被保留的上下文token数量不足以维持与生成token的充分交互，可能导致生成内容的语义偏离或时序不连贯。
3. **超参数的任务敏感性**：阈值 $\Delta$、聚类数 $K$、保留比例 $r_{\mathrm{ctx}}$ 等超参数需针对不同任务手动调节，目前缺乏自动化选择机制。
4. **任务范围的限定**：所有验证均在MV2V编辑（有mask）场景下完成，对无mask的通用视频生成或图像生成任务的适用性尚未探索。

### 补充图表

![[assets/figures/papers/paper_list_l832_https_arxiv_org_abs_2603_24260/figures/003_Table_1.jpg]]
*Table 1: Quantitative evaluation of inference efficiency and visual quality in video generation models. HetCahce achieves superior efficiency and better visual quality across different base models, sampling schedulers, video resolutions, and lengths*

![[assets/figures/papers/paper_list_l832_https_arxiv_org_abs_2603_24260/figures/004_Figure_3.jpg]]
*Figure 3: VBench comparison between HetCache and other methods on different video editing tasks*

![[assets/figures/papers/paper_list_l832_https_arxiv_org_abs_2603_24260/figures/005_Figure_4.jpg]]
*Figure 4: Visualization of different video editing tasks. HetCache produces relatively high-quality results while other methods suffer from smoothness, ghosting, and blurring issues*

![[assets/figures/papers/paper_list_l832_https_arxiv_org_abs_2603_24260/figures/006_Figure_5.jpg]]
*Figure 5: Key metircs comparison of different K and*

![[assets/figures/papers/paper_list_l832_https_arxiv_org_abs_2603_24260/figures/007_Table_2.jpg]]
*Table 2: Additional evaluation results under different settings*

![[assets/figures/papers/paper_list_l832_https_arxiv_org_abs_2603_24260/figures/008_Figure_6.jpg]]
*Figure 6: Visualization of ablation study, with and without clustering and correlation guidance will impact the generation quality*

![[assets/figures/papers/paper_list_l832_https_arxiv_org_abs_2603_24260/figures/009_Table_3.jpg]]
*Table 3: Quantitative ablation study results*

## 方法谱系与知识库定位

### 与现有加速范式的谱系关系

HetCache 处于扩散模型推理加速的两条技术路线的交叉点上：**去噪时间步冗余消除**与**Transformer token 冗余裁剪**。本节梳理其相对于已有工作的继承与突破，并标注适用边界。

#### 时间步级加速：从步数压缩到自适应计算调度

扩散模型推理加速的早期路线主要围绕减少去噪步数展开，包括训练式蒸馏（如渐进蒸馏、一致性模型）和免训练采样器设计（如 DDIM、DPM-Solver）。这类方法对所有时间步施加统一的压缩策略，忽视了**去噪过程不同阶段对计算的需求异质性**——在 MV2V 编辑中，早期步布局生成与后期步细节精化所需的计算量存在显著差异。

HetCache 在时间步维度上的核心创新在于**将“是否计算”的二元决策拓展为“全计算/部分计算/重用”的三态自适应调度**。其调度依据是相邻步调制输入 $F_t = T_t \odot x_t$ 的累积相对变化 $D_{a \to b} = \sum_{t=a}^{b-1} L_1^{\mathrm{rel}}(F, t)$，其中单步差异定义为：

$$L_1^{\mathrm{rel}}(F, t) = \frac{|F_t - F_{t+1}|_1}{|F_{t+1}|_1}$$

当 $D_{a \to b} > 1.5\Delta$ 时执行全计算并更新缓存，当 $1\Delta < D_{a \to b} \leq 1.5\Delta$ 时执行部分计算（仅使用选定的 token 子集），当 $D_{a \to b} \leq 1\Delta$ 时直接复用上一步缓存。这种基于**输出变化代理信号**的调度机制，使得计算资源得以向变化剧烈的去噪阶段倾斜，与固定步数压缩方法形成互补而非替代关系。

#### Token 级加速：从统一缓存到异质性感知缓存

在 Transformer 自注意力加速方面，现有方法普遍采用 KV-cache 或 token 剪枝策略，但存在一个关键盲区：**它们假设所有 token 对生成质量的贡献是同质的**。在 MV2V 编辑场景中，编辑掩膜定义了明确的感兴趣区域（ROI），使得时空 token 天然分化为三类——上下文 token（远离编辑区的背景）、边界 token（编辑区边缘的过渡区域）和生成 token（编辑区内部）。统一缓存所有上下文 token 不仅浪费计算，更可能因保留与生成区无关的背景信息而引入干扰。

HetCache 的 token 级策略直接回应了这一异质性：

1. **基于编辑掩膜的空间先验划分**：利用 MV2V 编辑自带的 mask $M$ 将 DiT 的时空 token 划分为 $\mathcal{X}_{ctx}$（上下文）、$\mathcal{X}_{margin}$（边界）和 $\mathcal{X}_{gen}$（生成）三类，其中边界和生成 token 始终参与注意力计算以保证编辑一致性。

2. **语义代表性与交互强度双重约束的上下文 token 选择**：对上下文 token 执行轻量 K-Means 聚类获得 $K$ 个语义簇 $\{S_1, S_2, \ldots, S_K\}$，在每个簇内利用全计算步缓存的上下文-生成注意力矩阵 $\bar{A}$ 计算每个 token 的重要性分数：

   $$\alpha_i = \frac{1}{|\mathcal{X}_{gen}|} \sum_{j \in \mathcal{X}_{gen}} \bar{A}_{i,j}$$

   仅保留每个簇内 $\alpha_i$ 最高的 $r_{ctx}$ 比例 token。这一设计的因果逻辑是：**既要在语义空间上覆盖上下文的多样性（聚类代表性），又要在注意力空间上筛选与生成区存在强交互的 token（相关性）**。消融实验证实了两者缺一不可——同时移除聚类和相关性指导导致 VBench 分数从 76.29 降至 76.19，并出现重影和边界不平滑（Table 3, Figure 6）。

3. **复杂度降阶**：部分计算步的注意力复杂度从 $\mathcal{O}(X^2) = \mathcal{O}((X_c + X_m + X_g)^2)$ 降至 $\mathcal{O}((r_{ctx} X_c + X_m + X_g)^2)$，其中 $X_c, X_m, X_g$ 分别为上下文、边界、生成 token 数。

#### 与具体基线工作的对比定位

- **Vanilla DiT 全计算推理**（Wan2.1-VACE 等）：作为无加速基线，每步执行完整的时空自注意力。HetCache 在其基础上实现 2.67× 延迟加速和 FLOPs 大幅降低，且无需微调或蒸馏，保持了即插即用的兼容性。

- **统一 token 缓存方法**（如 token 合并、token 剪枝等）：这类方法对所有 token 一视同仁，在 MV2V 编辑中因忽视 ROI 异质性而可能导致编辑区边界模糊或上下文信息丢失。HetCache 通过 mask 引导的三类 token 划分和选择性上下文缓存，在保持编辑一致性的前提下实现了更精准的冗余裁剪。

- **时间步压缩方法**（如 DDIM、DPM-Solver）：减少总去噪步数，但每步仍执行全计算。HetCache 的时间步调度机制可与这类方法正交叠加——实验表明在不同采样调度器下均能取得一致的加速效果（Table 1）。

### 适用边界与局限

HetCache 的设计深度耦合于 MV2V 编辑的两个先验条件，这构成了其当前的适用边界：

1. **对编辑掩膜的依赖**：token 类别的划分（上下文/边界/生成）完全依赖编辑 mask 提供的空间先验。当 mask 质量较差（如边缘不精确、覆盖不完整）时，token 划分可能引入误差，进而影响部分计算步的注意力质量。对于无 mask 的通用视频生成或图像生成任务，该方法无法直接迁移，需要设计替代的空间先验提取机制（如基于注意力图的自适应 ROI 检测）。

2. **超参数的手动调节需求**：时间步调度阈值 $\Delta$、聚类数 $K$、上下文保留比例 $r_{ctx}$ 等超参数需要针对不同任务和模型规模手动设定。实验表明 $r_{ctx}$ 的增加通常单调提升性能，但 $K$ 的变化不存在单调趋势（Figure 5），暗示语义结构的有效容量有限且任务相关。在更大规模 DiT 变体上如何自动化选择最优超参数仍是一个开放问题。

3. **极低计算预算下的质量退化风险**：当 $r_{ctx}$ 设置过低时，被保留的上下文 token 可能不足以支撑生成区与背景的协调融合，导致生成质量明显下降。HetCache-fast 与 HetCache-slow 两种配置的差异（Table 1）已暗示了这一权衡。

### 开放问题与未来方向

1. **向无 ROI 先验场景的扩展**：能否将异质性感知缓存推广到通用视频生成或图像生成任务？一个可能的方向是利用自注意力图自动发现“生成关键区”，替代人工 mask 的角色。

2. **与训练后加速技术的协同**：HetCache 作为免训练方法，与蒸馏、量化、剪枝等训练后加速技术存在正交叠加的潜力。联合优化可能实现超越单一技术的加速比。

3. **可学习的缓存策略**：当前上下文 token 选择依赖手工设计的 K-Means 聚类和注意力重要性评分。是否可以通过端到端学习（如轻量门控网络）直接预测每个 token 的保留概率，从而进一步优化缓存决策的精度？

4. **更大规模模型上的超参数自动化**：在 Wan2.1 之外的 DiT 变体（如更大分辨率、更长序列）上，$\Delta$、$K$、$r_{ctx}$ 的最优值可能显著不同。设计自适应调节机制（如基于 token 数量或去噪进度动态调整）是实用化部署的关键。

## 原文 PDF

![[paperPDFs/CVPR_2026/Accelerating_Diffusion_based_Video_Editing_via_Heterogeneous_Caching_Beyond_Full_Computing_at_Sampled_Denoising_Timestep.pdf]]
