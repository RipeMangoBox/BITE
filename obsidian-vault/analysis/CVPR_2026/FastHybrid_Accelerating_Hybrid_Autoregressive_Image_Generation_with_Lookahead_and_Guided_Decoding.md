---
title: "FastHybrid: Accelerating Hybrid Autoregressive Image Generation with Lookahead and Guided Decoding"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/FastHybrid_Accelerating_Hybrid_Autoregressive_Image_Generation_with_Lookahead_and_Guided_Decoding.pdf
project_link: null
code_link: null
aliases:
- FastHybrid
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/generative_models_diffusion
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: 利用自回归模型在生成早期即能捕获全局语义的能力，提前并行解码未来token并辅以引导扩散减少去噪步数，从而解耦语义预测与细节求精的计算成本。
primary_logic: 自回归模型的语义理解能力使得图像生成早期即可确定大部分区域的布局和内容，因此可以跳过序列依赖，通过前瞻分支并行生成粗粒度预测，再通过自回归分支验证并借助引导扩散在少量步数内完成细节细化。
claims:
- 早期生成阶段已确定图像整体布局和语义内容，支持提前并行解码。
- FastHybrid在仅0.11 FID损失下实现最高1.69×加速。
- Lookahead Decoding配合Autoregressive Refinement Branch通过余弦相似度校验确保语义一致性。
- ImageNet 256x256 上 FID ↓ = 1.70 (FastHybrid-H-64)
---

# FastHybrid: Accelerating Hybrid Autoregressive Image Generation with Lookahead and Guided Decoding

> [!tip] 核心洞察
> 自回归模型的语义理解能力使得图像生成早期即可确定大部分区域的布局和内容，因此可以跳过序列依赖，通过前瞻分支并行生成粗粒度预测，再通过自回归分支验证并借助引导扩散在少量步数内完成细节细化。

| 字段 | 内容 |
|------|------|
| 中文题名 | FastHybrid：利用前瞻与引导解码加速混合自回归图像生成 |
| 英文题名 | FastHybrid: Accelerating Hybrid Autoregressive Image Generation with Lookahead and Guided Decoding |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://openaccess.thecvf.com/content/CVPR2026/html/Jiang_FastHybrid_Accelerating_Hybrid_Autoregressive_Image_Generation_with_Lookahead_and_Guided_CVPR_2026_paper.html) |
| Topic | #topic/vision_multimodal_applications #topic/generative_models_diffusion #topic/vision_multimodal_applications/image_and_video_generation |
| Method | FastHybrid |
| Dataset | ImageNet 256x256 |

> [!tip] 效果简介
> - ImageNet 256x256 上，FID ↓ 1.70 (FastHybrid-H-64) vs 2.32 (MAR-B-64) (-0.62)；Speedup 1.69× vs 1.00× (MAR) (+0.69×)；ΔFID (degradation) 0.11 vs 0 (+0.11)。

## 概述

混合自回归图像生成模型（如 **MAR**，Li et al., NeurIPS 2024）将自回归建模与扩散去噪相结合，在图像生成质量上取得了显著进展，但其推理过程中扩散模型的多步去噪成为主要的计算瓶颈。标准混合模型的总推理成本为 $T_{MAR} = (P + Q \cdot T) K$，其中扩散去噪步数 $T$ 通常高达100步，严重制约了实际部署效率。

FastHybrid 的核心洞察在于：自回归模型在生成早期阶段即能捕获图像的全局语义和整体布局（见 Figure 1），因此可以打破严格的序列依赖，提前并行预测未来 token，再通过轻量级验证与引导扩散完成细节细化。基于此，该方法提出两项关键创新：

1. **前瞻解码策略**：构建双分支架构——前瞻分支并行预测未来 $k$ 个 token 并提供粗粒度先验，自回归细化分支逐 token 验证一致性，当余弦相似度低于阈值 $\lambda$ 时触发重新生成。
2. **引导扩散采样**：以前瞻预测结果作为引导信号，通过单调递减的余弦权重调度 $\gamma_t = 1 - \cos^2(\frac{\pi t}{2T_g})$ 调整扩散去噪轨迹，将所需去噪步数从 $T$ 压缩至 $T_g$（如10步），总成本降至 $T_{Ours} = P \cdot K + Q \cdot T + Q \cdot T_g \cdot (K-1)$。

在 ImageNet 256×256 基准上，FastHybrid-H-64 的 FID 达到 1.70（MAR-B-64 为 2.32），实现最高 1.69× 推理加速，FID 仅退化 0.11。消融实验表明，提高语义相似度拒绝阈值 $\lambda$ 有助于降低 FID 并提升 IS，余弦调度在引导权重策略中表现最优。该方法目前基于 MAR 架构验证，在其他混合自回归模型上的通用性仍有待探索。

## 背景与动机

### 混合自回归图像生成的效率瓶颈

近年来，混合自回归模型将自回归序列建模与扩散去噪相结合，在图像生成质量上取得了显著进展。以 **MAR**（Li et al., NeurIPS 2024）为代表的基座模型，将图像生成分解为两步：首先通过自回归Transformer逐token预测离散潜变量，再利用扩散模型对每个token对应的连续特征进行多步去噪。这种“预测-去噪”的双阶段范式在FID等指标上展现出竞争力，但其推理成本也因此显著膨胀。

核心瓶颈在于扩散去噪过程。标准混合模型中，每个自回归token的生成都需要经历完整的T步扩散去噪（如100步）。设自回归步数为K，单步自回归预测成本为P，单步扩散去噪成本为Q，则总推理成本可表示为：

$$T_{MAR} = (P + Q \cdot T) K$$

扩散去噪项$Q \cdot T$在总成本中占据主导地位。为缓解这一问题，已有加速方法如 **CSpD**（Wang et al., arXiv 2024）尝试通过连续推测解码减少有效序列长度，**LazyMAR**（Yan et al., arXiv 2025）则通过特征缓存复用减少重复计算。然而，这些方法并未触及扩散去噪步数本身，加速上限受制于去噪过程固有的计算开销。

### 早期语义先行：一个被忽视的加速契机

本文的核心观察是：在混合自回归生成中，图像的全局语义和布局在生成早期即已基本确立。Figure 1展示了自回归解码的推进过程——在256步生成中，仅前几步就已确定大部分区域的整体内容和空间结构，后续步骤主要完成局部细节的精细化。这一现象意味着，大量去噪计算被耗费在对已基本确定的粗粒度内容进行重复细化上。

这一观察揭示了一个结构性的优化空间：如果自回归模型在早期就能捕获全局语义，那么可以**提前并行解码未来token**，用轻量级前瞻分支生成粗粒度预测，再通过验证和引导机制在少量去噪步数内完成细节修正。这种“语义先行、细节后补”的策略，有望从根本上解耦语义预测与细节求精的计算成本，突破现有加速方法的天花板。

### 本文动机与目标

基于上述洞察，本文提出 **FastHybrid**，旨在实现混合自回归图像生成的高质量加速。具体目标包括：

1. **设计前瞻解码策略**：利用自回归模型早期语义捕获能力，并行预测多个未来token，打破逐token顺序生成的依赖瓶颈。
2. **构建双分支验证架构**：保留轻量自回归分支对前瞻预测进行语义一致性校验，确保加速不牺牲生成质量。
3. **引入引导扩散采样**：以前瞻预测为先验引导扩散去噪轨迹，将去噪步数从完整T步压缩至极少T_g步，直接削减核心计算瓶颈。

通过上述设计，FastHybrid力求在仅引入极低FID退化（约0.11）的前提下，实现最高约1.69×的推理加速。

## 核心创新

FastHybrid 的核心创新在于将混合自回归图像生成中的语义预测与细节求精**解耦**，通过两个互补的机制实现推理加速：**前瞻解码策略**与**引导扩散采样**。

### 瓶颈定位

混合自回归模型（如 **MAR**，Li et al., NeurIPS 2024）的推理瓶颈在于扩散头对每个 token 的连续表示进行多步去噪。标准流程中，总推理成本为：

$$T_{MAR} = (P + Q \cdot T) K$$

其中 $P$ 为自回归模型单步成本，$Q$ 为扩散头单步成本，$T$ 为完整去噪步数（如 100 步），$K$ 为序列长度。扩散去噪步骤 $Q \cdot T$ 主导了整体开销，成为加速的核心障碍。

### 因果调控变量

作者发现，自回归模型在生成早期阶段即能捕获图像的全局语义和整体布局（见 Figure 1）。这一洞察意味着：**大部分区域的粗粒度内容可以在早期确定，无需等待序列依赖完全展开**。FastHybrid 利用这一特性，通过两个 changed slots 实现加速：

| 变更维度 | 基线方法（MAR） | FastHybrid |
|---------|---------------|-----------|
| 解码策略 | 逐 token 顺序自回归生成 | 前瞻解码：并行预测未来 $k$ 个 token，搭配自回归细化与分歧校验 |
| 扩散去噪步数 | 完整 $T$ 步扩散去噪 | 引导扩散采样仅需 $T_g \ll T$ 步（如 10 步） |
| 引导机制 | 无 | 动态单调递减的余弦引导权重调度，以前瞻预测引导去噪轨迹 |
| 一致性校验 | 无 | 基于余弦相似度的分歧检测，低于阈值 $\lambda$ 时重新掩码生成 |

### 双分支前瞻解码策略

FastHybrid 的推理流水线由两个分支构成（Figure 2a）：

**前瞻解码分支**（Lookahead Decoding Branch）在生成第 $i$ 个 token 后，利用自回归模型并行预测未来 $k$ 个潜变量，并通过扩散头联合去噪，一次性获得粗粒度预测：

$$z_{i:i+k}' \sim p(z_{i:i+k} | x_{0:i-1}) \qquad x_{t-1,i:i+k}' \sim q(x_{t-1,i:i+k} | x_{t,i:i+k}, z_{i:i+k}', t)$$

**自回归细化分支**（Autoregressive Refinement Branch）按顺序逐 token 取样真实潜变量 $z_j$，并通过引导扩散完成单步去噪。关键在于，该分支利用余弦相似度校验前瞻预测 $z_j'$ 与真实 token $z_j$ 的语义一致性：若相似度低于阈值 $\lambda$，则将该 patch 重新掩码并重新生成。

$$z_j \sim p(z_j | x_{0:j-1}), \qquad x_{t,j} \sim q_g(x_{t-1,j} | x_{t,j}, z_j, t, x_{0,j}')$$

### 引导扩散采样

引导扩散采样是 FastHybrid 压缩去噪步数的核心机制（Figure 2b）。在自回归细化分支中，前瞻分支的输出 $x_0'$ 作为先验引导扩散轨迹。具体而言，原始扩散均值 $\mu_\theta(x_t | z, t)$ 与前瞻预测 $x_0'$ 按动态权重 $\gamma_t$ 加权融合：

$$\mu_{\theta}'(x_t | x_0', z, t) = (1 - \gamma_t) \cdot \mu_{\theta}(x_t | z, t) + \gamma_t \cdot x_0'$$

权重调度采用单调递减的余弦函数，使早期去噪步强依赖前瞻引导，后期逐步回归标准扩散：

$$\gamma_t = 1 - \cos^2\left(\frac{\pi t}{2 T_g}\right)$$

这一设计使得去噪步数从 $T$（如 100 步）大幅缩减至 $T_g$（如 10 步），总推理成本降至：

$$T_{Ours} = P \cdot K + Q \cdot T + Q \cdot T_g \cdot (K - 1)$$

其中 $T_g \ll T$，加速效果显著。

### 创新总结

FastHybrid 的三重创新形成闭环：**前瞻解码**利用早期语义确定性并行预测未来 token，**自回归细化**通过余弦相似度校验保证语义一致性，**引导扩散**以前瞻预测为锚点在极少量步数内完成细节去噪。三者协同实现了最高 1.69× 的推理加速，FID 仅退化 0.11。

## 整体框架

FastHybrid 的推理流水线围绕一个核心洞察构建：混合自回归图像生成中，自回归模型在生成早期即能捕获全局语义并确立大部分区域的布局与内容。基于此，方法将传统“逐 token 顺序生成 + 完整扩散去噪”的串行流程重构为**前瞻并行预测**与**轻量验证细化**协同的双分支架构，从而在保持语义一致性的前提下大幅压缩计算开销。

### 流水线总览

整体推理过程由三个紧密协作的阶段组成：

1. **前瞻解码分支 (Lookahead Decoding Branch)**：在当前位置 $i$，自回归模型一次性并行预测未来 $k$ 个 token 的潜变量 $z_{i:i+k}'$，并联合执行扩散去噪得到粗粒度预测 $x_{0,i:i+k}'$。该分支的核心作用是以极低的额外成本提供全局语义先验。
   
2. **自回归细化分支 (Autoregressive Refinement Branch)**：按原始顺序逐 token 采样真实的潜变量 $z_j$，并利用前瞻分支的输出作为引导，通过**引导扩散采样 (Guided Diffusion Sampling)** 在仅 $T_g$ 步（如 10 步）内完成去噪。此分支保证最终生成质量与基线模型一致。

3. **分歧校验 (Divergence Check)**：在细化分支中，计算前瞻预测 $z_j'$ 与真实自回归 token $z_j$ 的余弦相似度。若相似度低于阈值 $\lambda$，判定为语义分歧，将该 patch 重新掩码并重新生成，从而阻断错误累积。

三者的输入输出关系与模块交互如 Figure 2 所示。

![[assets/figures/papers/paper_list_l869_https_openaccess_thecvf_com_content_CVPR2026_html_Jiang_FastHybrid_Accel/figures/002_Figure_2.jpg]]
*Figure 2: The inference pipeline of FastHybrid. (a) illustrates the dual-branch architecture of our Lookahead Decoding Strategy: the lookahead branch and the autoregressive refinement branch. (b) shows the details of the Guided Diffusion Sampling process, showing how predictions from the lookahead branch guide the diffusion trajectory to reduce denoising steps in the autoregressive branch*

### 时间成本解构

理解 FastHybrid 加速效果的关键在于对比标准混合模型与所提方法的推理成本。设自回归模型单步前向成本为 $P$，扩散模型单步去噪成本为 $Q$，总生成步数为 $K$，标准扩散去噪步数为 $T$：

- **标准混合模型 (MAR)**：每个自回归步均需完整 $T$ 步扩散去噪，总成本为：
  $$T_{MAR} = (P + Q \cdot T) K$$

- **FastHybrid**：前瞻分支仅需一次自回归前向和一次完整 $T$ 步扩散（处理 $k$ 个 token 的并行去噪成本近似等效于单 token），细化分支每步仅需 $T_g$ 步引导扩散（$T_g \ll T$），总成本为：
  $$T_{Ours} = P \cdot K + Q \cdot T + Q \cdot T_g \cdot (K - 1)$$

当 $T_g \ll T$ 且 $K$ 较大时，第二项与第三项之和远小于基线中的 $Q \cdot T \cdot K$，从而获得显著加速。论文报告最高 **1.69×** 推理加速，FID 仅退化 0.11。

### 引导扩散采样机制

引导扩散采样是实现“少步数、高质量”去噪的关键。其核心操作是在逆向扩散的每一步中，将原始预测均值 $\mu_{\theta}(x_t | z, t)$ 与前瞻分支的输出 $x_0'$ 按动态权重 $\gamma_t$ 进行融合：

$$\mu_{\theta}'(x_t | x_0', z, t) = (1 - \gamma_t) \cdot \mu_{\theta}(x_t | z, t) + \gamma_t \cdot x_0'$$

其中 $\gamma_t$ 采用单调递减的余弦调度：

$$\gamma_t = 1 - \cos^2\left(\frac{\pi t}{2 T_g}\right)$$

该调度使去噪早期强烈依赖前瞻先验以快速确定全局结构，后期逐渐回归标准扩散轨迹以保留细节建模能力。消融实验证实余弦调度在 FID-速度权衡上优于线性和平方调度。

### 与基线方法的本质区别

相较于逐 token 顺序生成的 **MAR** (Li et al., NeurIPS 2024)，FastHybrid 将语义预测与细节去噪解耦：前瞻分支提前“猜测”未来内容，细化分支仅需验证和局部修正。相较于 **CSpD** (Wang et al., arXiv 2024) 的连续推测解码和 **LazyMAR** (Yan et al., arXiv 2025) 的特征缓存策略，FastHybrid 的独特之处在于利用扩散模型自身的去噪轨迹可引导性，而非仅依赖自回归模型的推测或缓存机制来减少计算。

## 核心模块与公式推导

### 3.1 混合自回归图像生成的推理瓶颈

FastHybrid 以 **MAR**（Li et al., NeurIPS 2024）为代表的混合自回归图像生成范式为基础。该类方法将图像生成过程分解为两个阶段：自回归模型逐 token 预测离散潜变量 $z_i$，扩散模型再对每个 token 对应的连续图像 patch 执行 $T$ 步去噪。标准混合模型的总推理成本可表示为：

$$T_{MAR} = (P + Q \cdot T) K$$

其中 $P$ 为自回归模型单 token 预测成本，$Q$ 为扩散模型单步去噪成本，$T$ 为完整去噪步数（通常为 100 步），$K$ 为总 token 数。扩散去噪的多步迭代成为推理加速的主要瓶颈。

FastHybrid 的核心洞察在于：自回归模型的语义理解能力使得图像生成早期即可确定大部分区域的布局和内容（如 Figure 1 所示，绿框区域在早期步骤已基本确定）。基于此，方法通过前瞻并行解码与引导扩散两个关键创新，将总成本降至：

$$T_{Ours} = P \cdot K + Q \cdot T + Q \cdot T_g \cdot (K - 1)$$

其中 $T_g$ 为引导扩散步数（如 10 步），远小于 $T$，从而在保证生成质量的前提下显著降低计算开销。

### 3.2 前瞻解码策略

前瞻解码策略（Lookahead Decoding Strategy）采用双分支架构，在自回归生成的每一步并行预测未来 $k$ 个 token，并通过一致性校验确保语义连贯性。

#### 3.2.1 前瞻解码分支

前瞻分支利用自回归模型和扩散头，以当前已生成的 token 序列 $x_{0:i-1}$ 为条件，一次性并行预测未来 $k$ 个潜变量 $z_{i:i+k}'$，并联合执行去噪：

$$z_{i:i+k}' \sim p(z_{i:i+k} | x_{0:i-1}) \qquad x_{t-1,i:i+k}' \sim q(x_{t-1,i:i+k} | x_{t,i:i+k}, z_{i:i+k}', t)$$

该分支提供粗粒度的前瞻先验，为后续自回归细化提供参考。

#### 3.2.2 自回归细化分支与分歧校验

自回归细化分支按原始顺序逐 token 采样真实的潜变量 $z_j$，并利用前瞻分支的预测 $x_{0,j}'$ 作为引导，通过引导扩散采样完成单步去噪：

$$z_j \sim p(z_j | x_{0:j-1}), \qquad x_{t,j} \sim q_g(x_{t-1,j} | x_{t,j}, z_j, t, x_{0,j}')$$

为确保前瞻预测的语义一致性，引入基于余弦相似度的分歧校验机制：计算前瞻预测 token $z_j'$ 与真实自回归 token $z_j$ 的余弦相似度，当相似度低于阈值 $\lambda$ 时，判定该 patch 存在语义分歧，将其重新掩码并重新生成（见 Algorithm 1 line 7）。这一机制在保证语义连贯性的同时，最大限度保留前瞻加速带来的效率收益。

### 3.3 引导扩散采样

引导扩散采样（Guided Diffusion Sampling）是 FastHybrid 实现去噪步数压缩的关键模块。其核心思想是以前瞻分支输出的粗粒度预测 $x_0'$ 作为先验引导，调整扩散去噪的均值轨迹，使得在极少量步数内即可完成细节细化。

具体而言，在每个去噪步 $t$，将原始扩散模型预测的均值 $\mu_{\theta}(x_t | z, t)$ 与前瞻预测 $x_0'$ 按动态权重 $\gamma_t$ 加权融合：

$$\mu_{\theta}'(x_t | x_0', z, t) = (1 - \gamma_t) \cdot \mu_{\theta}(x_t | z, t) + \gamma_t \cdot x_0'$$

基于调整后的均值，逆向扩散转移分布为：

$$q(x_{t-1} | x_t) \approx q(x_{t-1} | x_t, x_0 = \mu_{\theta}'(x_t | x_0', z, t)) = N(\frac{\alpha_t \bar{\beta}_{t-1}^2}{\bar{\beta}_t^2} x_t + \frac{\bar{\alpha}_{t-1}^2 \beta_t^2}{\bar{\alpha}_t^2} \mu_{\theta}'(x_t | x_0', z, t), \sigma_t^2 I)$$

引导权重 $\gamma_t$ 采用单调递减的余弦调度，从 1 平滑过渡至 0：

$$\gamma_t = 1 - \cos^2(\frac{\pi t}{2 T_g})$$

该调度策略的直觉在于：去噪初期，前瞻预测 $x_0'$ 提供强引导以快速确定整体结构；随着去噪深入，逐步降低引导强度，让扩散模型自主完成局部细节的精细建模。消融实验（Table 3 及 Figure 5）表明，余弦调度在引导权重策略中表现最优，有效平衡了加速效果与生成质量。

### 3.4 基础扩散模型公式

为保持方法推导的完整性，此处列出混合自回归模型中扩散部分的基础公式。扩散模型的训练目标为最小化预测噪声与实际噪声的期望误差：

$$\min \mathcal{L}_{\theta}^{DM} = \mathbb{E}_{t,\epsilon} [|| \epsilon_{\theta}(x_t | z, t) - \epsilon ||]$$

在标准逆向去噪过程中，从 $x_t$ 到 $x_{t-1}$ 的转移分布近似为以预测均值 $\mu_{\theta}$ 为中心的高斯分布：

$$q(x_{t-1} | x_t) \approx q(x_{t-1} | x_t, x_0 = \mu_{\theta}(x_t | z, t)) = N(\frac{\alpha_t \bar{\beta}_{t-1}^2}{\bar{\beta}_t^2} x_t + \frac{\bar{\alpha}_{t-1}^2 \beta_t^2}{\bar{\alpha}_t^2} \mu_{\theta}(x_t | z, t), \sigma_t^2 I)$$

FastHybrid 通过引导均值调整（公式 6-7）替换上述标准转移中的 $\mu_{\theta}$，在保持扩散模型结构不变的前提下实现去噪步数的大幅压缩。

## 实验与分析

### 一、主实验结果

FastHybrid 在 ImageNet 256×256 上的核心结果汇总于 **Table 1**。实验覆盖了 Base、Large 和 Huge 三种模型规模，统一使用 50,000 张生成图像计算 FID 与 IS，并以 batch size 8 测量显存占用与推理耗时。

![[assets/figures/papers/paper_list_l869_https_openaccess_thecvf_com_content_CVPR2026_html_Jiang_FastHybrid_Accel/figures/003_Table_1.jpg]]
*Table 1: Main Results Across Different Model Sizes. FID and IS were evaluated on 50,000 generated images. Memory usage and runtime were measured with a batch size of 8*

**核心发现：FastHybrid 在几乎不牺牲生成质量的前提下，实现了显著的推理加速。** 以 FastHybrid-H-64 为例，其 FID 达到 1.70，不仅优于基座模型 MAR-B-64 的 2.32（FID 降低 0.62），更在仅增加 0.11 FID 退化的情况下，实现了最高 **1.69×** 的推理加速。这一结果表明，前瞻解码与引导扩散的组合策略成功解耦了语义预测与细节求精的计算成本——自回归模型在生成早期即可捕获全局语义，使得前瞻分支的粗粒度预测足够可靠，而引导扩散仅需少量步数即可完成局部细节的修正。

定性对比（**Figure 3**）进一步验证了上述结论。在 MAR-Large-64 模型上，FastHybrid 生成的图像在纹理细节与结构一致性上均优于 CSpD 和 LazyMAR 等加速基线，佐证了自回归细化分支中基于余弦相似度的分歧校验机制的有效性。

![[assets/figures/papers/paper_list_l869_https_openaccess_thecvf_com_content_CVPR2026_html_Jiang_FastHybrid_Accel/figures/004_Figure_3.jpg]]
*Figure 3: Generated images from the MAR-Large-64 model after being accelerated by different methods, where 64 represents the number of autoregressive steps*

### 二、消融实验

#### 2.1 语义相似度拒绝阈值的影响

**Table 2** 展示了语义相似度拒绝阈值 λ 的消融结果。实验对比了仅使用拒绝过滤（R-x）与拒绝过滤后接引导扩散采样（RG-x）两种配置。核心发现如下：

- **提高拒绝阈值有助于提升生成质量。** 在 RG 配置下，λ 从 0.2 提升至 0.8 时，FID 从 5.46 降至 4.84，IS 同步改善。这说明更严格的语义一致性校验能有效过滤前瞻分支中与真实自回归分布偏离较大的预测，避免错误累积。
- **引导扩散采样的增益是独立的。** 对比 R-0.8 与 RG-0.8，后者在拒绝过滤的基础上进一步降低了 FID，验证了引导扩散阶段对局部不一致性的修正能力——这正是该方法设计的核心动机之一（Section 4.3）。

**Figure 4** 的可视化对比直观展示了不同 λ 设置下的生成差异：低阈值时部分 patch 出现语义错位或纹理模糊，而高阈值下图像的整体一致性与细节保真度均有明显提升。

#### 2.2 引导采样策略与权重调度

**Table 3** 与 **Figure 5** 联合呈现了引导采样策略的消融。实验对比了三类方案：
1. **直接减少扩散步数（MAR-Dx）**：将去噪步数从完整 T 步缩减至 x 步，但不引入任何引导；
2. **逆向加噪-去噪方法**：对前瞻预测加噪后再去噪，参数化为步数 T 与噪声比例；
3. **动态引导权重调度**：包括线性（Linear）、平方（Square）和余弦（Cosine）三种单调递减调度。

**余弦调度在所有策略中表现最佳。** 其权重公式为：

$$\gamma_t = 1 - \cos^2\left(\frac{\pi t}{2 T_g}\right)$$

该调度从 1 平滑递减至 0，在去噪初期赋予前瞻预测较高的引导强度以快速确定全局结构，后期逐渐降低引导以保留扩散模型自身的细节生成能力。相比之下，直接减少扩散步数（MAR-Dx）虽然降低了计算量，但 FID 退化显著，说明无引导的少步扩散难以维持生成质量。逆向加噪-去噪方法同样未能有效利用前瞻预测中的语义信息，表现不及动态引导策略。

### 三、失败模式与局限

尽管 FastHybrid 在整体指标上表现优异，但分析揭示了若干需要注意的边界情形：

1. **低阈值下的语义不一致风险。** 当 λ 设置过低（如 0.2）时，前瞻分支中与真实分布偏差较大的预测将通过校验，导致局部 patch 出现语义错位或纹理断裂（见 Table 2 及 Figure 4）。这表明余弦相似度阈值是方法的关键敏感参数，需根据具体模型与分辨率进行调优。

![[assets/figures/papers/paper_list_l869_https_openaccess_thecvf_com_content_CVPR2026_html_Jiang_FastHybrid_Accel/figures/005_Table_2.jpg]]
*Table 2: Performance comparison of our FastHybrid method using various semantic similarity rejection thresholds, benchmarked against the MAR-Base model. ”R-x” denotes rejection filtering only, while ”RG-x” applies subsequent guided diffusion sampling. FID and IS were calculated on 10,000 generated images*

![[assets/figures/papers/paper_list_l869_https_openaccess_thecvf_com_content_CVPR2026_html_Jiang_FastHybrid_Accel/figures/007_Figure_4.jpg]]
*Figure 4: Visual comparison of images generated by the large size model with different similarity rejection settings*

2. **引导权重调度的敏感性。** Table 3 显示，不同权重调度策略之间的 FID 差异可达 1 以上，说明引导强度的时序分配对最终质量有显著影响。余弦调度虽在实验中表现最优，但其最优性是否受底层扩散模型噪声调度的影响，论文未做进一步分析，需手动验证。

![[assets/figures/papers/paper_list_l869_https_openaccess_thecvf_com_content_CVPR2026_html_Jiang_FastHybrid_Accel/figures/006_Table_3.jpg]]
*Table 3: Ablation study on different guided sampling strategies and weight schedules. The table compares three approaches: (1) reducing the number of diffusion steps (MAR-Dx); (2) an inverse method involving adding noise and then denoising, parameterized by steps (T) and noise ratio; and (3) various dynamic guidance weight schedules (Linear, Square, Cos)*

3. **通用性未经验证。** 当前实验仅基于 MAR 基座模型（Li et al., NeurIPS 2024），该方法在其他混合自回归模型（如 HART、Fluid）上的有效性仍为开放问题。此外，前瞻步数 k 和拒绝阈值 λ 在不同图像内容与分辨率下的自适应选择策略亦有待探索。

4. **实时场景的延迟稳定性。** 论文未明确讨论方法在实时交互场景下的延迟稳定性及资源占用峰值，该点需在实际部署前进行额外评估。

### 补充图表

![[assets/figures/papers/paper_list_l869_https_openaccess_thecvf_com_content_CVPR2026_html_Jiang_FastHybrid_Accel/figures/008_Figure_5.jpg]]
*Figure 5: Images generated by the large size model with different guided methods and weight schedules*

![[assets/figures/papers/paper_list_l869_https_openaccess_thecvf_com_content_CVPR2026_html_Jiang_FastHybrid_Accel/figures/001_Figure_1.jpg]]
*Figure 1: Visualization of autoregressive decoding progression, displaying 8 uniformly sampled steps from 256 steps. Patches with green borders represent regions that have been determined during the autoregressive process. The remaining tokens, while not yet fully refined, have their general content largely determined in the early stages of the autoregressive process*

## 方法谱系与知识库定位

### 1. 基座模型与加速基线

FastHybrid 构建于混合自回归图像生成框架之上，其基座模型为 **MAR**（Li et al., NeurIPS 2024）。MAR 的核心范式是将自回归模型与扩散模型耦合：自回归部分负责逐 token 预测语义潜变量，扩散部分负责将潜变量解码为连续图像块。这一设计使 MAR 在 ImageNet 256×256 上取得了优异的 FID 指标，但其推理速度受制于扩散去噪的多步迭代——每个 token 的解码都需要执行完整的 T 步扩散过程，形成“自回归步数 × 扩散步数”的计算瓶颈。

在加速这一范式方面，已有两类代表性工作：

- **CSpD**（Wang et al., arXiv 2024）：采用连续推测解码策略，在自回归维度上尝试并行化，但未触及扩散去噪步数的缩减问题。
- **LazyMAR**（Yan et al., arXiv 2025）：通过特征缓存复用减少部分冗余计算，本质上是一种工程优化，不改变解码策略本身。

FastHybrid 与上述方法的根本差异在于：它同时从**解码策略**和**扩散去噪步数**两个维度切入，通过前瞻解码将自回归的顺序依赖打破，再通过引导扩散将去噪步数从 T 步压缩至 T_g 步（如 10 步），实现了两个维度上的乘性加速叠加。

### 2. 方法定位：前瞻解码 + 引导扩散的协同机制

FastHybrid 的方法定位可概括为“语义先行、细节后验”的双分支协同框架。其核心洞察来自对混合自回归模型解码过程的可视化观察（Figure 1）：在生成过程的早期阶段，图像的整体布局和大部分区域的语义内容已基本确定，后续步骤主要完成局部细节的精细化。这一观察构成了前瞻解码策略的可行性基础。

具体而言，FastHybrid 的方法谱系定位体现在以下四个关键设计槽位：

| 设计槽位 | 基座模型（MAR） | FastHybrid | 机制差异 |
|---------|---------------|-----------|---------|
| 解码策略 | 逐 token 顺序自回归 | 前瞻解码：并行预测未来 k 个 token | 打破序列依赖，实现解码并行化 |
| 扩散去噪步数 | 完整 T 步（如 100 步） | 引导扩散仅需 T_g 步（如 10 步） | 以前瞻预测为引导信号压缩去噪步数 |
| 引导机制 | 无 | 动态单调递减余弦权重调度 | 早期强引导确保语义对齐，后期弱引导释放细节自由度 |
| 一致性校验 | 无 | 余弦相似度分歧检测 + 重新掩码 | 当前瞻预测与真实自回归 token 相似度低于阈值 λ 时触发重新生成 |

这种设计的本质是将混合自回归模型的推理成本从 $T_{MAR} = (P + Q \cdot T) K$ 降至 $T_{Ours} = P \cdot K + Q \cdot T + Q \cdot T_g \cdot (K - 1)$，其中 $T_g \ll T$，从而在保持图像质量的前提下实现显著加速。

### 3. 适用边界

FastHybrid 的有效性依赖于以下前提条件：

1. **自回归模型的语义编码能力**：前瞻分支的并行预测质量取决于自回归模型在早期步骤中捕获全局语义的能力。若基座模型的自回归编码器对长程依赖建模不足，前瞻预测的准确性将下降，导致分歧率升高，加速收益衰减。

2. **扩散模型的去噪灵活性**：引导扩散采样的有效性要求扩散模型能够在前瞻预测的引导下，在少量步数内完成细节修正。若扩散模型的噪声调度与引导权重调度不匹配，可能导致局部伪影或细节丢失。

3. **阈值 λ 的调节空间**：分歧检测依赖于余弦相似度阈值 λ 的合理设定。λ 过高会增加重新生成频率，侵蚀加速收益；λ 过低则可能放过语义不一致的 patch，损害图像质量。Table 2 的消融实验表明 λ = 0.8 在 FID 和 IS 之间取得了较好平衡，但这一最优值的普适性尚未在不同分辨率或图像域下验证。

### 4. 局限与开放问题

**已知局限**：

- 论文未报告 FastHybrid 在其他混合自回归模型（如 HART、Fluid）上的迁移实验，方法的跨架构通用性未经实证。
- 前瞻步数 k 和拒绝阈值 λ 的选择目前依赖经验设定，缺乏针对不同图像内容和分辨率的自适应策略。
- 引导权重调度 γ_t 的最优形式是否受扩散模型噪声调度（如 DDPM vs. DDIM）影响，论文未展开讨论。

**开放问题**：

1. **跨架构泛化**：FastHybrid 的前瞻解码策略是否可无缝适配其他混合自回归模型（如基于 VQ-VAE 的 tokenizer 或不同的扩散头设计），需要进一步实验验证。

2. **自适应参数选择**：前瞻步数 k 和拒绝阈值 λ 能否根据图像内容的复杂度（如纹理密度、语义边界清晰度）动态调整，是一个值得探索的方向。

3. **实时交互场景的延迟稳定性**：论文主要报告了吞吐量加速（speedup），未讨论在实时交互场景下的延迟分布（如 P50/P99 延迟）及资源占用峰值。前瞻分支的并行计算可能导致瞬时显存占用升高，这一问题在实际部署中需要关注。

4. **引导权重调度的理论分析**：余弦调度在实验中表现最优（Table 3），但其理论最优性未得到证明。引导权重调度与扩散模型噪声调度之间的耦合关系值得进一步分析。

## 原文 PDF

![[paperPDFs/CVPR_2026/FastHybrid_Accelerating_Hybrid_Autoregressive_Image_Generation_with_Lookahead_and_Guided_Decoding.pdf]]
