---
title: "Forecast the Principal, Stabilize the Residual: Subspace-Aware Feature Caching for Diffusion Transformers"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/Forecast_the_Principal_Stabilize_the_Residual_Subspace_Aware_Feature_Caching_for_Diffusion_Transformers.pdf
project_link: null
code_link: "https://github.com/BlackMaple1203/SVDCache"
aliases:
- SC
- FPSRSAFCDT
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/generative_models_diffusion
- topic/representation_self_supervised_transfer
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: 通过奇异值分解将特征空间分离为主子空间和残差子空间，并对主子空间使用指数移动平均预测、残差直接重用，从而控制预测误差和生成质量。
primary_logic: DiT特征的奇异值分解揭示了两个具有不同时间动态的子空间：低秩主子空间演化平滑可预测，而残差子空间为低能量高频振荡；此外，SVD的右奇异向量和奇异值在不同提示下高度稳定，允许离线一次分解并在线复用。
claims:
- SVD-Cache通过SVD分解特征，在主导子空间应用EMA预测，残差子空间直接重用。
- 不同提示下，SVD分解产生高度稳定的奇异值和右奇异矩阵。
- 离线执行一次SVD，可在所有时间步复用基底，额外成本极低。
- FLUX.1-dev (text-to-image) 上 ImageReward = 1.0123
---

# Forecast the Principal, Stabilize the Residual: Subspace-Aware Feature Caching for Diffusion Transformers

> [!tip] 核心洞察
> DiT特征的奇异值分解揭示了两个具有不同时间动态的子空间：低秩主子空间演化平滑可预测，而残差子空间为低能量高频振荡；此外，SVD的右奇异向量和奇异值在不同提示下高度稳定，允许离线一次分解并在线复用。

| 字段 | 内容 |
|------|------|
| 中文题名 | 预测主成分，稳定残差：面向扩散Transformer的子空间感知特征缓存 |
| 英文题名 | Forecast the Principal, Stabilize the Residual: Subspace-Aware Feature Caching for Diffusion Transformers |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://openaccess.thecvf.com/content/CVPR2026/html/Chen_Forecast_the_Principal_Stabilize_the_Residual_Subspace-Aware_Feature_Caching_for_CVPR_2026_paper.html) · [Code](https://github.com/BlackMaple1203/SVDCache) |
| Topic | #topic/vision_multimodal_applications #topic/generative_models_diffusion #topic/representation_self_supervised_transfer #topic/vision_multimodal_applications/image_and_video_generation |
| Method | SVD-Cache |
| Dataset | FLUX.1-dev, HunyuanVideo |

> [!tip] 效果简介
> - FLUX.1-dev (text-to-image) 上，ImageReward 1.0123 vs 0.9898 (original) (+2.519%)；CLIP Score 32.983 vs 32.404 (original) (+1.348%)。
> - HunyuanVideo (text-to-video) 上，VBench 80.60 vs 80.66 (original) (-0.07% (near-lossless))。

## 概要

扩散Transformer（DiT）在图像与视频生成中展现出强大能力，但其多步迭代去噪过程计算开销巨大，严重制约了推理效率。现有的特征缓存方法（如**TaylorSeer**、**ToCa**、**Δ-DiT**等）通过在不同时间步间复用或预测中间层特征来跳过冗余计算，然而它们均隐含一个共同假设：整个特征空间是平滑可预测的。本文揭示，这一假设在DiT中并不成立——特征空间实际由两个动态特性迥异的子空间构成：一个低秩的**主子空间**，其演化轨迹平滑、易于预测；另一个高维的**残差子空间**，呈现高频振荡且能量极低，强制对其进行预测反而会引入显著的累积误差，成为限制加速效果的核心瓶颈。

基于此发现，本文提出**SVD-Cache**，一种子空间感知的特征缓存方法。其核心策略是通过奇异值分解（SVD）将特征空间显式分离为主子空间与残差子空间，对平滑可预测的主子空间采用指数移动平均（EMA）进行预测，而对高频振荡的残差子空间则直接重用，从而从根本上避免了在不可预测成分上引入误差。更为关键的是，论文发现了一个具有重要工程价值的性质：SVD分解得到的右奇异向量和奇异值在不同输入提示下高度稳定，这使得基底可以**离线一次分解、全局复用**，在线推理时仅需极低的额外计算代价即可完成子空间重构。

在FLUX.1-dev文本到图像模型上，SVD-Cache在5.5倍加速下不仅未损失质量，ImageReward指标反而从原始模型的0.9898提升至1.0123（+2.5%），CLIP Score从32.404提升至32.983（+1.3%）。在HunyuanVideo文本到视频模型上，该方法在5.5倍加速下实现了近乎无损的VBench得分（80.60 vs. 原始80.66）。在更激进的加速设置下，SVD-Cache在FLUX.1-schnell上可达29.01倍加速，在FLUX.1-DEV-int8上可达7.61倍加速，展现出广泛的适用性与可扩展性。

扩散Transformer（Diffusion Transformer, DiT）已成为文生图（如FLUX）和文生视频（如HunyuanVideo）的主流骨干架构。然而，DiT的推理过程需要迭代执行数十步去噪，每一步都需通过深层Transformer块计算中间特征，导致极高的延迟和计算开销。特征缓存（Feature Caching）作为一种无训练的加速策略，通过在不同去噪时间步之间复用中间激活来减少冗余计算，近年来受到广泛关注。

已有特征缓存方法（如**ToCa**（Zou et al., 2024）、**Δ-DiT**（Chen et al., 2024）、**FORA**（Selvaraju et al., 2024）、**TaylorSeer**（Liu et al., 2025）等）的核心假设是：整个特征空间在相邻时间步之间平滑演化，因此可以通过外推或直接复用来预测未来特征。然而，这一假设在DiT中并不完全成立。

**真正的瓶颈在于特征空间的异质性。** 本文通过奇异值分解（SVD）对DiT特征进行深入分析，揭示了特征空间内部存在两个动力学特性截然不同的子空间（见Figure 1(a)）：
1.  **主子空间（Principal Subspace）**：对应较大的奇异值，承载主要能量。该子空间沿去噪轨迹演化平滑、可预测。
2.  **残差子空间（Residual Subspace）**：对应较小的奇异值，能量低但呈高频振荡。该子空间难以预测，强制对其进行外推会导致误差累积，损害生成质量。

现有方法将两个子空间统一处理——要么全部预测（如TaylorSeer的多项式外推），要么全部直接重用（如基础缓存策略）——这种“一刀切”的策略是限制加速比与质量平衡的根本原因。全特征预测在残差子空间上放大误差，而全特征重用则无法捕捉主子空间的平滑漂移。

此外，本文发现了一个关键性质：**SVD的右奇异向量和奇异值在不同输入提示（prompt）下高度稳定**（见Figure 1(b)）。这意味着子空间的基底结构是模型的内在属性，而非随输入剧烈变化。这一发现使得离线一次性分解、在线持续复用成为可能，为高效实现子空间分离铺平了道路。

基于以上观察，本文的动机明确：**放弃“全特征空间同质化”的假设，转而将特征空间显式分离为主子空间和残差子空间，并针对各自的动力学特性设计差异化的缓存策略——对平滑可预测的主子空间应用指数移动平均（EMA）预测，对高频振荡的残差子空间直接重用。** 这一设计从根本上消除了残差预测的误差源，同时保留了主子空间的时序建模能力，有望在更高加速比下维持近乎无损的生成质量。

## 核心方法与创新机理

SVD-Cache 的核心创新在于**首次揭示了扩散Transformer（DiT）特征空间存在两个异质子空间**，并据此设计了一种**子空间感知的差异化缓存策略**。相较于现有方法，这一创新体现在两个关键的 **changed slots** 上。

### 从统一缓存到子空间分离

现有特征缓存方法（如 **TaylorSeer** (Liu et al., 2025)、**ToCa** (Zou et al., 2024)、**Δ-DiT** (Chen et al., 2024)）的核心瓶颈在于：它们将整个特征空间视为一个平滑、可预测的整体，并对其应用统一的预测或重用策略。然而，SVD-Cache 通过奇异值分解发现，DiT 的特征空间实际上由两个动态特性截然不同的子空间构成（Figure 1）：

1.  **主导子空间 (Principal Subspace)**：对应较大的奇异值，承载主要能量。其轨迹在去噪过程中**平滑演化**，具有良好的时间可预测性。
2.  **残差子空间 (Residual Subspace)**：对应较小的奇异值，能量低但呈现**高频振荡**。强制对其进行预测会引入难以控制的累积误差，这是限制现有方法加速上限的关键因素。

### 关键创新点一：差异化的子空间处理策略

基于上述发现，SVD-Cache 将特征处理策略从“全特征空间统一预测”转变为“**主子空间预测 + 残差子空间重用**”：

-   **对主导子空间**：采用指数移动平均（EMA）进行预测。由于该子空间演化平滑，EMA 能够可靠地估计其在未来时间步的状态：
    $$\widehat{F}_{k,t} = \beta \widehat{F}_{k,t-\Delta} + (1-\beta) F_{k,t}$$
-   **对残差子空间**：采取保守策略，直接从上一个缓存的时间步**直接重用**。这避免了因预测高频振荡成分而导致的误差放大，从而在激进加速下保持生成稳定性。

消融实验（Figure 5(c)）有力地验证了这一设计的必要性：在低秩子空间上应用 EMA 预测并重用残差，取得了最佳性能，证明了“预测可靠成分、保守处理易变成分”这一洞察的正确性。

### 关键创新点二：“一次分解，全时复用”的离线基底缓存

传统思路下，对每个新输入的特征在线执行 SVD 分解将带来不可忽视的计算开销。SVD-Cache 的第二个关键创新在于发现了一个**跨提示的稳定性规律**：对于不同的输入提示，SVD 分解产生的右奇异向量 $V$ 和奇异值 $\sigma$ 高度稳定（Figure 1(b)）。这意味着这些基底具有通用性。

据此，SVD-Cache 将子空间基底的获取方式从“每次在线计算”转变为“**离线一次分解，在线全时复用**”：
1.  **离线预处理**：在任意一个参考提示的特征上执行一次 SVD，将右奇异向量 $V_{\mathcal{C}}$ 和奇异值 $\sigma_{\mathcal{C}}$ 作为可复用的基底缓存下来。
2.  **在线推理**：对于任意新输入的特征 $F$，直接利用缓存的基底，通过矩阵运算近似重构其低秩成分，而无需再次执行昂贵的 SVD：
    $$F_k = F V_{\mathcal{C}} \mathrm{diag}(\sigma_{\mathcal{C}})^{-1} \mathrm{diag}(\sigma_{\mathcal{C},k}) V_{\mathcal{C},k}^{\top}$$
    这一策略使得子空间分解的额外计算成本降至极低，为方法的实用性奠定了基础。

### 创新总结

SVD-Cache 的本质创新在于**将特征缓存问题从一个“全空间预测”问题，重新定义为一个“子空间感知的预测与重用”问题**。它通过 SVD 揭示了 DiT 特征空间的内在结构，并利用跨提示的基底稳定性，以极低的成本实现了对不同动态特性子空间的差异化处理，从而突破了现有方法因残差振荡而面临的加速瓶颈。

SVD-Cache 的完整流程分为**离线预处理**与**在线推理**两个阶段，其核心设计遵循一个因果原则：将 DiT 特征空间通过 SVD 分离为演化平滑的**主子空间**与高频振荡的**残差子空间**，并分别采用预测与重用策略，从而在加速采样的同时控制误差累积。

### 离线预处理：一次性 SVD 与基底缓存

在离线阶段，方法在一组参考提示（reference prompts）上运行 DiT 前向过程，提取某一层的特征矩阵 $F \in \mathbb{R}^{N \times D}$，并执行奇异值分解：

$$F = U \Sigma V^\intercal, \quad U \in \mathbb{R}^{N \times r}, \Sigma \in \mathbb{R}^{r \times r}, V \in \mathbb{R}^{D \times r}$$

关键发现是，不同提示下得到的右奇异向量 $V$ 和奇异值 $\sigma$ 具有高度稳定性（Figure 1(b) 显示相似度超过 0.8），这意味着**离线执行一次 SVD 分解，获得的基底可以在所有后续推理中复用**，避免了每次在线计算分解的高昂开销。离线阶段存储两个关键组件：

- **右奇异向量 $V_{\mathcal{C}}$** 与 **奇异值 $\sigma_{\mathcal{C}}$**，作为可复用的低秩基底。
- **截断秩 $k$**，由累积能量占比阈值 $\tau$ 决定：

$$\frac{\sum_{i=1}^k \sigma_i^2}{\sum_{i=1}^r \sigma_i^2} \ge \tau$$

消融实验表明 $\tau$ 的最优值约为 0.85（Figure 5(d)）。

### 在线推理：主子空间预测与残差重用

在线推理时，对于新的输入特征 $F$，SVD-Cache 利用缓存的基底将其分解为主子空间和残差子空间，并对两者施加不同的处理策略。整个在线管线包含四个串联模块：

1. **主子空间重构**  
   利用缓存的 $V_{\mathcal{C}}$ 和 $\sigma_{\mathcal{C}}$ 近似计算左奇异向量：
   $$U = F V_{\mathcal{C}} \, \mathrm{diag}(\sigma_{\mathcal{C}})^{-1}$$
   截断至前 $k$ 个分量，得到低秩重构：
   $$F_k = U_k \, \mathrm{diag}(\sigma_{\mathcal{C},k}) \, V_{\mathcal{C},k}^{\top}$$

2. **残差提取**  
   残差子空间直接从原始特征中减去低秩部分得到：
   $$R = F - F_k$$
   该残差子空间具有低能量、高频振荡的特性，难以预测。

3. **EMA 预测低秩特征**  
   对主子空间特征 $F_k$ 应用指数移动平均（EMA），预测下一时间步的低秩成分：
   $$\widehat{F}_{k,t} = \beta \widehat{F}_{k,t-\Delta} + (1-\beta) F_{k,t}$$
   主子空间演化平滑，适合用 EMA 进行可靠预测。

4. **残差直接重用与特征重组**  
   残差子空间 $R$ 直接从上一时间步复用，避免因高频振荡导致的预测误差放大。最终将 EMA 预测的主子空间特征与复用的残差相加，重构完整特征：
   $$\widehat{F}_{t+\Delta} = \widehat{F}_{k,t+\Delta} + \widehat{R}_{t+\Delta}$$

### 设计逻辑与输入输出流

整个框架的设计逻辑遵循一个清晰的因果链条：**SVD 分解揭示了特征空间的双子空间结构（Figure 1(a)），主子空间承载主要能量且演化平滑，残差子空间能量低但振荡剧烈**。基于这一洞察，SVD-Cache 将缓存策略从“全特征空间统一处理”转变为“分而治之”——对可预测的主子空间使用 EMA 外推，对不可预测的残差保守重用。消融实验（Figure 5(c)）验证了这一策略组合的最优性：在低秩子空间上应用 EMA 预测、残差直接重用的配置，始终优于在全特征空间上统一预测的变体方法（如 **TaylorSeer**（Liu et al., 2025）、**ToCa**（Zou et al., 2024）等）。

输入输出流方面：离线阶段输入为参考提示特征，输出为缓存的基底 $(V_{\mathcal{C}}, \sigma_{\mathcal{C}}, k)$；在线阶段输入为当前时间步的 DiT 特征 $F$ 与缓存基底，输出为预测的下一时间步特征 $\widehat{F}_{t+\Delta}$，直接替换原 DiT 块的计算结果，实现跳跃式采样加速。

![[assets/figures/papers/paper_list_l874_https_openaccess_thecvf_com_content_CVPR2026_html_Chen_Forecast_the_Prin/figures/002_Figure_2.jpg]]
*Figure 2: Overview of the SVD-Cache framework. (a) Offline preprocessing: A reference feature is decomposed via SVD to obtain a reusable low-rank basis. The right singular vectors and singular values are both stored, and the rank k is determined based on the cumulative singular value energy according to Eq. (5). (b) Inference: Given a new feature, we reconstruct its principal and residual components. Specifically, we first retrieve the shared basis stored in offline preprocessing and then follow Eq. (8), (9) and (10) to compute the components. The principal component is then predicted via EMA, while the residual is directly reused due to its low energy and oscillatory nature. The final feature is rec...*

### 离线SVD分解与基底缓存

SVD-Cache 的第一个关键模块在推理前离线完成。给定一个参考提示生成的 DiT 中间特征矩阵 $F \in \mathbb{R}^{N \times D}$（$N$ 为 token 数，$D$ 为特征维度），执行奇异值分解：

$$F = U \Sigma V^\intercal, \quad U \in \mathbb{R}^{N \times r}, \Sigma \in \mathbb{R}^{r \times r}, V \in \mathbb{R}^{D \times r}$$

其中 $r = \min(N, D)$。分解后，存储右奇异向量 $V_{\mathcal{C}}$ 和奇异值向量 $\pmb{\sigma}_{\mathcal{C}}$ 作为可复用基底。低秩 $k$ 根据累积能量占比自动确定：

$$\frac{\sum_{i=1}^k \sigma_i^2}{\sum_{i=1}^r \sigma_i^2} \ge \tau$$

其中 $\tau$ 为能量阈值，消融实验表明最优值约为 0.85。这一设计的核心依据是：不同提示下，SVD 分解产生的奇异值和右奇异矩阵高度稳定（Figure 1(b) 中相似度超过 0.8），使得“一次 SVD，全时分解”成为可能，额外成本极低。

![[assets/figures/papers/paper_list_l874_https_openaccess_thecvf_com_content_CVPR2026_html_Chen_Forecast_the_Prin/figures/001_Figure_1.jpg]]
*Figure 1: (a) PCA visualization of different feature spaces: Original Full Feature Subspace shows oscillatory trajectory while Principal Subspace evolves smoothly. Residual subspace is oscillatory and low-energy. (b) Singular values and right singular vectors are stable across different prompts. Similarity is evaluated using the product of cosine similarity and magnitude similarity. A similarity over 0.8 typically indicates a stable and reusable subspace*

### 在线主子空间重构

在线推理时，对于新的输入特征 $F$，利用缓存的基底近似计算左奇异向量：

$$U = F V_{\mathcal{C}} \operatorname{diag}(\pmb{\sigma}_{\mathcal{C}})^{-1}$$

随后截断得到低秩 $k$ 的主子空间重构：

$$F_k = U_k \operatorname{diag}(\pmb{\sigma}_{\mathcal{C},k}) V_{\mathcal{C},k}^{\top}$$

残差子空间则直接从原始特征中减去低秩部分：

$$R = F - F_k$$

这一步将特征空间显式分离为平滑可预测的主子空间和低能量高频振荡的残差子空间，为后续差异化处理奠定基础。

### EMA预测与残差重用

对主子空间特征 $F_{k,t}$，采用指数移动平均预测下一时间步的低秩成分：

$$\widehat{F}_{k,t} = \beta \widehat{F}_{k,t-\Delta} + (1-\beta) F_{k,t}$$

其中 $\beta$ 为动量系数，$\Delta$ 为缓存步长。残差子空间 $R$ 因其低能量和振荡特性，直接从前一时间步复用，避免预测误差放大。最终特征通过两部分相加完成重组：

$$\widehat{F}_{t+\Delta} = \widehat{F}_{k,t+\Delta} + \widehat{R}_{t+\Delta}$$

消融实验（Figure 5(c)）验证了这一差异化策略的有效性：对低秩子空间使用 EMA 预测并对残差直接重用，取得了最佳性能，显著优于对全特征空间统一预测的变体。

## 实验与关键发现

### 文本到图像生成主结果

SVD-Cache 在 FLUX.1-dev 上的定量结果见 Table 1。在 N=5（5.55× 加速）设置下，SVD-Cache 的 ImageReward 达到 **1.0123**，CLIP Score 达到 **32.983**，分别比原始模型（ImageReward 0.9898，CLIP 32.404）提升约 **+2.52%** 和 **+1.35%**。这一反直觉的提升可能源于 SVD 分解对特征空间的去噪效应——通过将高频振荡的残差子空间直接重用而非预测，避免了预测误差在去噪链中的累积放大，从而在加速的同时保持了甚至改善了生成质量。

![[assets/figures/papers/paper_list_l874_https_openaccess_thecvf_com_content_CVPR2026_html_Chen_Forecast_the_Prin/figures/005_Table_1.jpg]]
*Table 1: Quantitative comparison of text-to-image generation on FLUX.1-dev*

在 FLUX.1-dev-int8 量化模型上，SVD-Cache（N=5）实现 7.61× 加速，ImageReward 为 0.9904，CLIP 为 32.88，性能接近原始全精度模型。当与稀疏注意力等方法结合时，SVD-Cache 在 FLUX.1-schnell 上可实现高达 **29.01×** 的加速，在 FLUX.1-DEV-int8 上达到 **10.73×** 加速，展现出良好的方法兼容性。

### 文本到视频生成主结果

在 HunyuanVideo 上的定量结果见 Table 2。SVD-Cache（N=5）实现 4.18× 加速，VBench 综合得分 **80.60**，与原始模型（80.66）相比仅下降 **0.07%**，可视为近乎无损的加速。在视觉质量上，SVD-Cache 在更激进的加速设置下仍保持较强的时间一致性和视觉质量，而基线方法 TaylorSeer 则出现可见伪影和闪烁（见 Figure 4）。

![[assets/figures/papers/paper_list_l874_https_openaccess_thecvf_com_content_CVPR2026_html_Chen_Forecast_the_Prin/figures/006_Table_2.jpg]]
*Table 2: Quantitative comparison of text-to-video generation on HunyuanVideo*

![[assets/figures/papers/paper_list_l874_https_openaccess_thecvf_com_content_CVPR2026_html_Chen_Forecast_the_Prin/figures/004_Figure_4.jpg]]
*Figure 4: Comparison between SVD-Cache and TaylorSeer on HunyuanVideo. SVD-Cache sustains stronger temporal consistency and visual quality under more aggressive acceleration, while TaylorSeer develops visible artifacts and flickering*

### 与其他加速方法的对比

Table 3 报告了 SVD-Cache 与其他加速方法在 FLUX 上的定量对比。SVD-Cache 在 ImageReward 和 CLIP Score 两个维度上均优于或匹配包括 **ToCa**（Zou et al., 2024）、**Δ-DiT**（Chen et al., 2024）、**FORA**（Selvaraju et al., 2024）、**TaylorSeer**（Liu et al., 2025）在内的基线方法。Figure 5(a) 进一步证实，SVD-Cache 的子空间分解策略始终优于逐令牌缓存（ToCa）及其他全特征空间预测方法，验证了“分而治之”策略的有效性。

![[assets/figures/papers/paper_list_l874_https_openaccess_thecvf_com_content_CVPR2026_html_Chen_Forecast_the_Prin/figures/008_Figure_5.jpg]]
*Figure 5: Overall and Ablation Results of SVD-Cache. (a) SVD-Cache consistently outperforms token-wise(ToCa) and other full-featurespace predictor baselines. (b) When the low-rank subspace is predicted with other ODE methods, quality is significantly improved over the original method. (c) Ablation study on Flux by applying different strategies to the low-rank and residual components separately. (d) Ablation study on the energy threshold τ for subspace decomposition*

### 消融实验

**子空间预测策略消融**。Figure 5(c) 展示了对低秩子空间和残差子空间分别应用不同策略的消融结果。当对低秩子空间使用 EMA 预测、对残差直接重用时，性能最优。若对残差也尝试预测，则因残差的高频振荡特性导致预测误差放大，质量显著下降。这直接验证了核心设计动机：**预测平滑的主成分，保守处理振荡的残差**。

**能量阈值 τ 的敏感性**。Figure 5(d) 展示了能量阈值 τ 对性能的影响。τ 的最优值约为 **0.85**。τ 过低时，低秩子空间包含的主成分不足，预测收益有限；τ 过高时，残差子空间被过度压缩，部分具有预测价值的成分被错误归入残差并被直接重用，导致信息丢失。

**与 ODE 预测方法的兼容性**。Figure 5(b) 显示，当将 SVD-Cache 的低秩子空间预测与其他 ODE 方法结合时，能带来显著的质量提升。例如，将 SVD-Cache 与 TaylorSeer 配对使用时，相比单独使用 TaylorSeer 有实质性改进，表明子空间分解策略可以作为一种通用增强模块叠加在现有预测方法之上。

### 失败模式与局限性

当前分析中未报告明确的失败模式。但以下潜在风险需要人工验证：在极端加速设置下（如 N 值较大），EMA 预测的累积误差可能逐渐增大；离线 SVD 分解依赖参考提示的代表性，若在线输入的特征分布与参考提示差异过大，基底复用可能导致重构误差上升。此外，能量阈值 τ 目前为全局固定值，缺乏对场景和加速级别的自适应调整能力。

## 定位与知识库关联

### 1. 特征缓存加速谱系中的位置

SVD-Cache 属于扩散模型推理加速中“特征缓存”这一技术路线。该路线的核心假设是：扩散模型在相邻去噪时间步产生的中间特征具有高度相似性，因此可以通过缓存并预测未来特征来跳过部分Transformer Block的计算。现有方法可大致分为两类：

**全特征空间统一处理**：以 **ToCa**（Zou et al., 2024）为代表的逐令牌缓存方法，以及 **TaylorSeer**（Liu et al., 2025）为代表的多项式外推预测方法，均假设整个特征空间具有均匀的可预测性，对所有特征维度采用相同的缓存/预测策略。**Δ-DiT**（Chen et al., 2024）基于特征差异进行缓存决策，**FORA**（Selvaraju et al., 2024）采用快速转发策略，但同样未区分特征子空间的结构差异。

**SVD-Cache的差异化定位**：本文的核心突破在于揭示并利用了DiT特征空间的结构异质性——通过奇异值分解（SVD）发现特征空间可分离为平滑演化的低秩主子空间和振荡剧烈的高频残差子空间。这一发现直接挑战了现有方法“全特征空间均匀可预测”的隐含假设，将缓存策略从“统一处理”推向“子空间感知”的新范式。

### 2. 关键设计决策的因果链条

SVD-Cache的设计由以下因果发现驱动：

1. **瓶颈识别**：现有方法将主子空间（平滑、高能量）和残差子空间（振荡、低能量）混合处理，导致对残差子空间的预测误差不断累积，限制了加速比上限。
2. **因果旋钮**：通过SVD将特征空间显式分离，对不同子空间施加差异化处理——主子空间用指数移动平均（EMA）预测，残差子空间直接重用。
3. **稳定性发现**：实验意外发现，SVD分解的右奇异向量和奇异值在不同提示词下高度稳定（余弦相似度与幅度相似度的乘积超过0.8），使得离线一次分解、在线永久复用的策略成为可能，大幅降低了子空间分离的额外计算成本。

这一设计逻辑与现有方法形成鲜明对比：ToCa和TaylorSeer试图通过更复杂的预测函数来提升全空间预测精度，而SVD-Cache通过识别“哪些方向值得预测、哪些方向应保守处理”来从根本上避免误差放大。

### 3. 方法兼容性与扩展边界

SVD-Cache展现出良好的方法兼容性：

- **与ODE求解器结合**：消融实验表明，将低秩子空间与其他ODE预测方法（如TaylorSeer的预测器）结合时，相比原始方法仍有显著质量提升（Figure 5(b)），说明子空间分解策略本身具有独立价值，可作为其他预测方法的预处理模块。
- **与量化/稀疏注意力叠加**：论文展示了SVD-Cache可与INT8量化（FLUX.1-dev-int8上7.61×加速）和稀疏注意力（10.73×加速）组合使用，且在这些加速模型上仍能进一步提速至29.01×（FLUX.1-schnell），表明该方法在已优化模型上具有增量加速能力。

**适用边界**：方法的核心前提是DiT特征具有低秩结构且子空间基底跨提示词稳定。论文在FLUX（文生图）和HunyuanVideo（文生视频）两个不同架构的DiT模型上验证了该前提（Figure 7, Figure 8），但在其他架构（如U-Net类扩散模型、非Transformer架构）上的适用性尚未验证。

### 4. 局限性与待验证假设

**方法层面**：

- **能量阈值τ的敏感性**：主子空间秩k由累积能量阈值τ决定，消融实验显示最优值约为0.85（Figure 5(d)），但该阈值是否跨模型、跨任务通用仍需验证。论文未提供自适应阈值选择机制。
- **离线SVD的泛化风险**：基底稳定性在标准提示词上得到验证，但在极端分布外提示词（如高度抽象、多语言混合）下，右奇异向量的稳定性可能退化，导致重构误差增大。
- **残差直接重用的极限**：当缓存步长N进一步增大时，残差子空间的高频振荡可能累积到不可忽略的程度，当前“直接重用”策略可能成为新的瓶颈。

**评估层面**：

- 论文未报告SVD-Cache在不同随机种子下的性能方差，无法评估方法的稳定性。
- 与部分基线方法（如FoCa、Chipmunk）的定量对比缺失，仅在相关工作中提及。

### 5. 开放问题与后续方向

1. **自适应能量阈值**：能否根据输入提示词的复杂度、当前时间步的噪声水平，动态调整τ以实现最优的加速-质量权衡？
2. **跨架构泛化**：SVD分解揭示的低秩特性是否在更大规模DiT（如百亿参数级）或非DiT架构中依然成立？基底稳定性是否保持？
3. **残差子空间的精细化处理**：当前对残差子空间采用直接重用，是否存在更优的保守预测策略（如轻度平滑、条件重用）以进一步扩展缓存步长？
4. **与训练加速的结合**：子空间分解策略能否反向指导模型训练，例如通过正则化促进特征的低秩结构化，使模型原生更适合缓存加速？

## 原文 PDF

![[paperPDFs/CVPR_2026/Forecast_the_Principal_Stabilize_the_Residual_Subspace_Aware_Feature_Caching_for_Diffusion_Transformers.pdf]]
