---
title: "TimeRipples: Accelerating vDiTs by Understanding the Spatio-Temporal Correlations in Latent Space"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/TimeRipples_Accelerating_vDiTs_by_Understanding_the_Spatio_Temporal_Correlations_in_Latent_Space.pdf
project_link: null
code_link: null
aliases:
- TimeRipples
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/generative_models_diffusion
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: 潜在空间中标记通道层面的时空相关性。vDiT将通道分为时间、x、y三组，各通道组内的标记值存在空间或时间上的相似性，可据此复用部分注意力分数。
primary_logic: 注意力图中的各种模式（空间主导/时间主导）实质上是查询(Q)和键(K)沿通道维度的时空相关性在全局注意力图上的投影。通过沿独立通道识别并复用空间或时间上相似的标记的部分注意力分数，可在几乎不损失视频质量的前提下大幅减少注意力计算量。
claims:
- 自注意力在四个主流vDiT模型中平均占总执行时间的78%，成为推理瓶颈。
- vDiT将整个通道维度划分为时间、x方向、y方向三个独立组，不同组主导不同类型的时空相关性，恶意操作不同组会分别引入时间扭曲、x/y轴向条纹等特定伪影。
- 在相同的token节省比例下，我们的复用策略产生的MSE比掩码技术低一个数量级。
- 在HunyuanVideo上，TIMERIPPLE 75% 的PSNR达到35.06 dB，相比表现最好的基线 ∆-DIT (26.09 dB) 提升近9 dB。
---

# TimeRipples: Accelerating vDiTs by Understanding the Spatio-Temporal Correlations in Latent Space

> [!tip] 核心洞察
> 注意力图中的各种模式（空间主导/时间主导）实质上是查询(Q)和键(K)沿通道维度的时空相关性在全局注意力图上的投影。通过沿独立通道识别并复用空间或时间上相似的标记的部分注意力分数，可在几乎不损失视频质量的前提下大幅减少注意力计算量。

| 字段 | 内容 |
|------|------|
| 中文题名 | TimeRipples：通过理解潜在空间中的时空相关性加速视频扩散Transformer |
| 英文题名 | TimeRipples: Accelerating vDiTs by Understanding the Spatio-Temporal Correlations in Latent Space |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://openaccess.thecvf.com/content/CVPR2026/html/Mao_TimeRipples_Accelerating_vDiTs_by_Understanding_the_Spatio-Temporal_Correlations_in_Latent_CVPR_2026_paper.html) |
| Topic | #topic/vision_multimodal_applications #topic/generative_models_diffusion #topic/vision_multimodal_applications/image_and_video_generation |
| Method | TIMERIPPLE |
| Dataset | HunyuanVideo, CogVideoX, Open-Sora-Plan |

> [!tip] 效果简介
> - HunyuanVideo 上，VBench (↑) 80.23 (TIMERIPPLE 75%) vs 80.28 (Original) (-0.05 (<0.06% quality loss))；PSNR (dB, ↑) 35.06 (TIMERIPPLE 75%) vs 26.09 (∆-DIT) (+8.97 dB (>9 dB improvement))；SSIM (↑) 0.950 (TIMERIPPLE 75%) vs 0.867 (PAB) (+0.083)。
> - CogVideoX 上，PSNR (dB, ↑) 26.65 (TIMERIPPLE 75%) vs 25.04 (PAB) (+1.61 dB)。
> - Open-Sora-Plan 上，VBench (↑) 78.95 (TIMERIPPLE 75%) vs 78.77 (Original) (+0.18)。

## 概要

视频扩散Transformer（vDiT）已成为视频生成的主流架构，但其推理效率严重受制于自注意力机制。在四个主流vDiT模型上，自注意力计算平均占据总执行时间的**78%**（Fig. 4），成为制约实际部署的核心瓶颈。

本文提出**TIMERIPPLE**，一种轻量、训练无关的自注意力加速方法。其核心洞察在于：vDiT将通道维度按语义划分为时间、x方向、y方向三个独立组，各组内的标记在空间或时间上存在高度相似性，导致注意力图中呈现可复用的时空模式。TIMERIPPLE通过沿通道维度检测标记相似性，复用空间或时间上相近标记的部分注意力分数，从而大幅减少冗余计算。

在四个广泛使用的vDiT模型（HunyuanVideo、Wan2.1、CogVideoX、Open-Sora-Plan）上，TIMERIPPLE以**最高85%的自注意力计算节省**实现了**2.7×的理论加速**，同时将视频质量损失控制在**0.06%以内**（VBench指标）。在HunyuanVideo上，TIMERIPPLE 75%配置下的PSNR达到35.06 dB，相较于表现最好的基线方法 ∆-DiT（26.09 dB）提升近9 dB。方法无需重新训练或微调，可直接应用于现有vDiT模型。

### 视频扩散Transformer的效率瓶颈

视频扩散Transformer（vDiT）已成为当前视频生成领域的核心架构。典型的vDiT（如HunyuanVideo、Wan2.1、CogVideoX、Open-Sora-Plan）由多个堆叠的Transformer块构成，每个块包含自注意力层、交叉注意力层和前馈网络。然而，这类模型在实际部署中面临严峻的推理效率问题。

**自注意力是绝对瓶颈。** 对四个主流vDiT模型在Nvidia H100（80 GB）上的执行时间分解显示，自注意力计算平均占推理总延迟的**78%**（Fig. 4）。这意味着即使将其他所有模块的延迟降至零，整体加速空间也不超过约5倍。因此，任何有效的vDiT加速方案都必须直面自注意力层的计算冗余问题。

### 现有加速方法的局限

当前针对扩散Transformer的加速方法大致可分为以下几类：

- **训练无关的动态稀疏方法**：如**∆-DiT**（Chen et al., 2024）基于通道显著性动态跳过部分注意力计算，**MInference**（Jiang et al., NeurIPS 2024）从大语言模型的稀疏注意力模式迁移至vDiT。这些方法通过掩码或跳过策略减少计算量，但丢弃信息的方式较为粗暴，在相同token节省比例下会引入显著的MSE损失（Fig. 7）。
- **预定义稀疏掩码方法**：如**Sparse VideoGen (SVG)**（Xi et al., 2025）使用固定的时空稀疏模式跳过自注意力计算。这类静态策略缺乏对输入内容的适应性，难以在质量和效率之间取得精细平衡。
- **跨步广播方法**：如**PAB**（Zhao et al., 2024）通过跨去噪步骤广播中间注意力结果来减少计算，但该方法依赖于去噪步骤间的强相关性假设，在早期步骤或视频内容变化剧烈时效果受限。

这些方法的共同缺陷在于：**它们将注意力图视为一个整体进行稀疏化或跳过，而忽视了注意力分数在通道维度上天然存在的时空结构性冗余**。

### 核心洞察：通道维度的时空相关性

vDiT模型采用旋转位置编码（RoPE）来编码相对位置信息：
$$
\operatorname{RoPE}([x,y]) = (\cos\theta \cdot x - \sin\theta \cdot y,\; \sin\theta \cdot x + \cos\theta \cdot y)
$$

基于RoPE的语义特性，vDiT将整个通道维度划分为**三个独立组**：时间通道组、x方向空间通道组和y方向空间通道组。这一结构划分揭示了注意力图的内在生成机制：**注意力图中的空间主导模式和时间主导模式，实质上是查询（Q）和键（K）沿通道维度的时空相关性在全局注意力图上的投影**。

具体而言（Fig. 1, Fig. 2）：
- **空间主导的注意力模式**：主要关注单帧内的空间相关性，跨帧的值高度相似，可被复用；
- **时间主导的注意力模式**：主要关注跨帧的时间相关性，帧内的值高度相似，同样可被复用。

这一发现意味着：**通过沿独立通道组识别并复用空间或时间上相似标记的部分注意力分数，可以在几乎不损失视频质量的前提下大幅减少注意力计算量**。

### 恶意操纵的验证

为验证通道分组的因果作用，论文进行了恶意操纵实验（Fig. 5）：
- 复用时间相关通道会引入**时间扭曲**伪影；
- 复用x方向通道会产生沿x轴的**条纹状伪影**；
- 复用y方向通道会产生沿y轴的**条纹状伪影**。

这一结果确证了不同通道组对视频质量维度的独立控制，也为设计精细化的复用策略提供了结构基础：**必须沿独立通道维度分别进行相似性判定和复用，而非在全局注意力图上统一操作**。

### 本文动机

基于上述分析，本文的核心动机可概括为：利用vDiT通道维度的时空相关性，设计一种轻量、自适应的注意力分数复用策略，在不引入显著质量损失的前提下，大幅降低自注意力层的计算冗余，从而加速整个视频扩散Transformer的推理过程。

## 核心方法与创新机理

### 问题根因：自注意力中的时空冗余

vDiT 推理延迟的瓶颈高度集中——在四个主流模型（HunyuanVideo、Wan2.1、CogVideoX、Open-Sora-Plan）上，自注意力计算平均占据总执行时间的 **78%**（Fig. 4）。这一瓶颈的根源并非计算本身不可削减，而是注意力图中存在大量未被利用的时空冗余：同一帧内空间相邻的 token 往往产生相似的注意力分数，同一空间位置跨帧的 token 同样如此。现有加速方法（如 ∆-DIT、MInference、SVG、PAB）或者依赖静态掩码直接跳过计算，或者跨步广播中间结果，但都没有系统性地利用这一冗余的结构化来源。

### 核心洞察：通道维度的时空相关性投影

TIMERIPPLE 的关键认知突破在于将注意力图的冗余追溯到其产生的“上游”——**查询（Q）和键（K）沿通道维度的时空相关性**。vDiT 在应用旋转位置编码（RoPE）时，将整个通道维度划分为三个语义独立的组：时间组、x 方向组和 y 方向组（Eq. 2）。这意味着：

- 当时间通道组主导时，Q/K 的跨帧变化显著，但帧内 token 相似——注意力图呈现**时间主导模式**；
- 当空间通道组主导时，Q/K 的帧内变化显著，但跨帧 token 相似——注意力图呈现**空间主导模式**。

换言之，注意力图中的各种模式（空间主导/时间主导）实质上是 Q 和 K 沿通道维度的时空相关性在全局注意力图上的投影。这一洞察的直接推论是：**不必计算完整的 $QK^T$ 矩阵，只需沿独立通道识别并复用空间或时间上相似 token 的部分注意力分数，即可近似完整注意力**。

恶意操纵实验（Fig. 5）从反面验证了这一机制：若仅复用时间通道组，视频产生时间扭曲伪影；若仅复用 x 或 y 通道组，则产生对应轴向的条纹伪影——证明三个通道组各自独立编码不同维度的时空信息，且必须协调处理。

### 三个关键 changed slots

相对于现有加速方法，TIMERIPPLE 在三个关键维度上改变了自注意力的计算方式：

**Changed Slot 1：自注意力计算方式——从“全量计算”到“通道级稀疏计算+分数复用”**

基线方法执行完整的 $QK^T$ 点积及 Softmax（Eq. 1），或基于显著性分数动态跳过部分 token。TIMERIPPLE 则沿通道维度稀疏计算部分注意力分数，并通过复用空间或时间上相似 token 的分数来近似完整注意力图（Fig. 6）。这一改变的实质是将注意力计算的“跳过”策略从 token 粒度下沉到**通道粒度**，从而在相同计算节省比例下实现更精确的近似——在相同 token 节省率下，TIMERIPPLE 的复用策略产生的 MSE 比掩码技术**低一个数量级**（Fig. 7）。

**Changed Slot 2：token 相似性判定——从“无”到“三轴标准误差+OR 聚合”**

基线方法或完全没有 token 相似性的概念，或仅依赖注意力图本身的静态模式。TIMERIPPLE 引入了一种轻量级的相似性检测机制：对 Q 和 K 分别沿时间、x、y 三个维度，在窗口大小 $K$ 内计算标准误差 $\Delta$（Eq. 3），并与自适应阈值比较。三个维度的可复用 token 通过**逻辑 OR** 聚合为最终复用掩码。这一设计的关键在于：它不需要跨 token 的全局比较，仅需局部窗口内的统计量，计算开销极低，却能够精准捕获时空冗余的结构。

**Changed Slot 3：阈值调度策略——从“固定阈值”到“去噪步感知的线性调度”**

现有方法通常使用固定阈值或手动调节。TIMERIPPLE 观察到复用操作引入的 MSE 随去噪步单调递减（Fig. 9），据此设计了线性阈值调度 $\theta_{t,i}$（Eq. 4）：在去噪早期步骤（$i \in [i_{\min}, i_{\max}]$）使用较严格的低阈值，后期逐步放宽至高阈值，使得每次干预维持一致的误差水平。这一调度策略使得方法在质量敏感的早期去噪阶段保持高保真度，同时在后期充分释放加速潜力。

### 创新本质总结

TIMERIPPLE 的本质创新不在于提出一种新的注意力近似算法，而在于**识别并利用了 vDiT 架构中一个被忽视的结构化先验**——RoPE 将通道维度按时空语义分组，使得冗余在通道层面具有可预测的模式。三个 changed slots 分别从“计算什么”“复用谁”“何时放宽”三个维度将这一先验转化为实际的加速收益，最终在 HunyuanVideo 上以 75% 的计算节省实现了 35.06 dB PSNR（相较最佳基线 ∆-DIT 的 26.09 dB 提升近 9 dB），在 85% 的节省下 VBench 得分（80.44）甚至略超原始模型（80.28），验证了“理解冗余来源比直接跳过计算更有效”的核心主张。

TIMERIPPLE 的核心思路是将自注意力计算中存在的时空冗余，转化为沿通道维度的可控复用。整个流水线由四个模块串联而成，在标准 vDiT 的每个自注意力层内插入，不改变模型权重，也不依赖额外训练。

### 时空相似性检测

给定查询 $Q$ 和键 $K$，该模块分别对每个标记沿三个轴向——时间轴、x 方向空间轴、y 方向空间轴——执行窗口化的标准误差计算。具体地，对标记在窗口 $K$ 内的通道值计算标准误差 $\Delta$：

$$\Delta(a) = \sqrt{\sum_{i=0}^{K-1}(a_i-\bar{a})^2/K}, \quad \bar{a} = \sum_{i=0}^{K-1} a_i/K$$

若 $\Delta$ 低于当前去噪步的自适应阈值 $\theta_{t,i}$，则该标记被标记为“可复用”。三个轴向的检测独立进行，分别对应 vDiT 中 RoPE 编码划分的时间、x 空间、y 空间三组通道。恶意操纵不同通道组的实验表明，复用时间通道会引入时间扭曲，复用 x 或 y 通道则产生沿对应轴的条纹状伪影（Fig. 5），这验证了分组检测的必要性。

### 复用模式聚合

三个轴向的可复用标记通过逻辑 OR 合并，形成最终的复用掩码。这意味着只要标记在任一轴向上足够相似，其部分注意力分数即可从相邻标记处复用，从而在保证覆盖的同时最大化节省计算。

### 部分注意力计算

仅对未被标记为复用的标记，沿通道维度稀疏计算部分注意力分数。被标记为复用的标记则跳过 $QK^T$ 点积及后续 Softmax 中的对应项，直接使用前序标记的已有分数。这一策略在相同 token 节省比例下，产生的 MSE 比掩码基线低一个数量级（Fig. 7），说明复用比直接丢弃信息更精确。

### 注意力图聚合

将稀疏计算得到的部分分数与复用的历史分数汇总，形成完整的注意力图。不同颜色在 Fig. 6 中展示了各标记注意力分数中由计算获得与由复用获得的比例。

![[assets/figures/papers/paper_list_l941_https_openaccess_thecvf_com_content_CVPR2026_html_Mao_TimeRipples_Accele/figures/006_Figure_6.jpg]]
*Figure 6: The overview of our reuse method. 1) Both Q and K undergo three checks to identify tokens that can reuse the partial attention scores of previous tokens. 2) We next collect the reuse patterns. 3) Then, we sparsely compute the partial attention scores along each channel for non-reuse tokens. 4) Lastly, the attention map is obtained by aggregating all partial scores. Different colors in the attention map show the percentages of partial attention scores obtained by computation*

### 自适应阈值调度器

阈值并非固定，而是根据去噪步 $i$ 线性调节：

$$\theta_{t,i} = (i - i_{\min}) \cdot \frac{\theta_{t,\max} - \theta_{t,\min}}{i_{\max} - i_{\min}}, \quad i \in [i_{\min}, i_{\max}]$$

在 HunyuanVideo 上，$i_{\min}=11$，$i_{\max}=21$。早期步骤（$i$ 较小）使用较严格的低阈值，保证质量敏感阶段的精度；随着去噪推进，MSE 敏感性单调下降（Fig. 9），阈值逐渐放宽以换取更高的计算节省。前 10 步和最后 1 步完全不做干预，$[22, 49]$ 步使用固定阈值 $\theta_{t,\max}$。各模型的超参数详见表 Table 1。

### 与 vDiT 架构的关系

vDiT 由多个块堆叠而成，每个块包含自注意力、交叉注意力和线性层（Fig. 3）。TIMERIPPLE 仅作用在自注意力层，该层在四个主流 vDiT 模型上平均占推理总延迟的 78%（Fig. 4），是真正的计算瓶颈。方法本身是即插即用的轻量模块，不改变交叉注意力、MLP 等其他组件，也不依赖特定训练数据或提示调优。

![[assets/figures/papers/paper_list_l941_https_openaccess_thecvf_com_content_CVPR2026_html_Mao_TimeRipples_Accele/figures/003_Figure_3.jpg]]
*Figure 3: The overview of vDiT architectures. A vDiT consists of multiple blocks. Generally, each block contains a self-attention layer, a cross-attention layer, and a linear layer*

### 问题形式化：自注意力瓶颈

vDiT 中每个 Transformer 块的核心运算是缩放点积自注意力，其标准形式为：

$$\mathrm{Attention}(Q,K,V) = \mathrm{Softmax}\left(\frac{QK^T}{\sqrt{d_k}}\right)V \tag{1}$$

其中 $Q, K, V \in \mathbb{R}^{N \times d}$ 分别表示查询、键和值矩阵，$N$ 为标记数，$d$ 为通道维度，$d_k$ 为缩放因子。如 Fig. 4 所示，该计算在四个主流 vDiT 模型（HunyuanVideo、Wan2.1、CogVideoX、Open-Sora-Plan）上平均占据推理总延迟的 **78%**，成为视频生成效率的绝对瓶颈。

### 结构基础：RoPE 通道分组

vDiT 模型统一采用旋转位置编码（RoPE）来编码相对位置：

$$\operatorname{RoPE}([x,y]) = (\cos\theta \cdot x - \sin\theta \cdot y,\; \sin\theta \cdot x + \cos\theta \cdot y) \tag{2}$$

关键结构特性在于：**vDiT 将整个通道维度划分为三个独立组——时间组、x 方向空间组、y 方向空间组**。这一分组为后续沿通道维度的复用策略提供了语义基础。Fig. 5 的恶意操纵实验进一步验证了这种分组的因果作用：单独复用时间通道组会引入时间扭曲伪影，而分别复用 x 或 y 通道组则产生对应轴向的条纹状伪影。

### 核心机制：通道级标记相似性检测与复用

TIMERIPPLE 的核心思路是：注意力图中的空间主导/时间主导模式，实质上是 $Q$ 和 $K$ 沿通道维度的时空相关性在全局注意力图上的投影。因此，可通过沿独立通道识别并复用空间或时间上相似标记的部分注意力分数，大幅减少注意力计算量。

具体而言，对 $Q$ 和 $K$ 的每个标记，分别沿**时间轴、x 轴、y 轴**三个维度进行窗口化标准误差计算，以判定标记间的相似性：

$$\Delta(a) = \sqrt{\sum_{i=0}^{K-1}(a_i-\bar{a})^2/K}, \quad \bar{a} = \sum_{i=0}^{K-1} a_i/K \tag{3}$$

其中 $a$ 表示沿某一维度窗口内 $K$ 个连续标记的通道值向量，$\bar{a}$ 为其均值。当 $\Delta$ 低于预设阈值 $\theta_t$ 时，该标记对被视为“可复用”——即其注意力分数可由相邻标记的已计算结果近似替代，无需重新计算完整的 $QK^T$ 点积。

流水线包含四个步骤（Fig. 6）：
1. **时空相似性检测**：对 $Q$ 和 $K$ 分别沿时间、x、y 三个维度执行窗口化 $\Delta$ 计算，与阈值比较，标记可复用标记。
2. **复用模式聚合**：将三个维度的可复用标记通过**逻辑 OR** 合并，得到最终的复用掩码。
3. **部分注意力计算**：仅对未被标记为复用的标记沿通道维度稀疏计算部分注意力分数。
4. **注意力图聚合**：将计算得到的部分分数与复用的历史分数汇总，形成完整注意力图。

### 自适应阈值调度

去噪过程中不同步骤对注意力近似的敏感度不同。实验表明（Fig. 9），HunyuanVideo 在去噪步 11 至 21 期间 MSE 单调递减，之后趋于平稳。基于此，TIMERIPPLE 采用线性阈值调度策略：

$$\theta_{t,i} = (i - i_{\min}) \cdot \frac{\theta_{t,\max} - \theta_{t,\min}}{i_{\max} - i_{\min}}, \quad i \in [i_{\min}, i_{\max}] \tag{4}$$

其中 $i$ 为当前去噪步，$\theta_{t,\min}$ 和 $\theta_{t,\max}$ 分别为阈值的最小和最大值，$i_{\min}$ 和 $i_{\max}$ 为调度起止步。**早期步骤使用较严格的低阈值以保证生成质量，后期逐步放宽以换取更高加速比**。对于调度范围外的步骤：前 10 步和最后 1 步保持原始完整计算（不干预），其余步骤使用固定阈值 $\theta_{t,\max}$。各模型的超参数配置见 Table 1。

### 与掩码方法的本质区别

Fig. 7 的对比实验揭示了复用策略相较于掩码方法的优势：在相同的标记节省比例下，TIMERIPPLE 的复用策略产生的 MSE 比低值掩码和相似性选择后直接跳过两种基线**低一个数量级**。这是因为掩码方法直接丢弃信息，而复用策略通过利用标记间的时空相似性来近似注意力分数，保留了更多的有效信号。

![[assets/figures/papers/paper_list_l941_https_openaccess_thecvf_com_content_CVPR2026_html_Mao_TimeRipples_Accele/figures/007_Figure_7.jpg]]
*Figure 7: MSE comparison be*

## 实验与关键发现

### 实验设置与对比基线

为验证TIMERIPPLE的有效性，我们在四款广泛使用的vDiT模型上进行了全面评测：**HunyuanVideo**、**Wan2.1**、**CogVideoX**和**Open-Sora-Plan**。评测指标涵盖像素级保真度指标（PSNR、SSIM、LPIPS）和视频质量综合评测基准VBench。对比方法包括四类训练无关的vDiT加速基线：

- **∆-DIT**（Chen et al., 2024）：基于通道显著性动态跳过注意力计算
- **MInference**（Jiang et al., NeurIPS 2024）：从LLM稀疏注意力迁移的动态稀疏模式
- **Sparse VideoGen (SVG)**（Xi et al., 2025）：使用预定义时空稀疏掩码跳过自注意力计算
- **PAB**（Zhao et al., 2024）：通过跨去噪步广播中间注意力结果减少计算

所有对比方法均按原论文配置复现或引用原文结果。各模型的超参数配置详见表1（`θ_{t,max}`、`θ_{t,min}`、`i_min`、`i_max`），未针对特定提示进行调优。

### 主要定量结果

Table 2汇总了TIMERIPPLE与所有基线方法在四个vDiT模型上的全面对比。核心发现如下：

**在HunyuanVideo上，TIMERIPPLE 75%展现出压倒性优势。** PSNR达到35.06 dB，相比表现最好的基线∆-DIT（26.09 dB）提升近9 dB；SSIM达到0.950，较PAB（0.867）提升0.083；LPIPS降至0.036，较∆-DIT（0.200）降低0.164。在VBench综合质量评测上，TIMERIPPLE 75%得分80.23，与原始模型（80.28）相比质量损失小于0.06%，几乎无感知差异。更值得注意的是，**TIMERIPPLE 85%在VBench上得分80.44，略高于原始模型**，表明该方法在实现2.7×理论加速的同时，甚至可能通过正则化效应略微提升生成质量。

**跨模型泛化能力显著。** 在CogVideoX上，TIMERIPPLE 75%的PSNR达到26.65 dB，较PAB（25.04 dB）提升1.61 dB。在Open-Sora-Plan上，TIMERIPPLE 75%的VBench得分78.95，同样略高于原始模型（78.77）。这表明通道级时空相关性是vDiT模型的共性特征，而非特定模型的偶然现象。

**与稀疏掩码方法互补。** TIMERIPPLE 75% + SVG 70%的组合方案进一步验证了复用策略与稀疏掩码的正交性，可在保持质量的同时实现更高计算节省。

### 消融实验

Table 3在HunyuanVideo上系统消融了各设计选择的影响：

**时空联合重用优于单一维度重用。** 同时利用空间和时间维度重用（Spat+Temp）在PSNR、SSIM和LPIPS上均显著优于仅使用时间重用（Temp-only），验证了vDiT注意力图中同时存在空间主导和时间主导两种可复用模式，单一维度重用会遗漏大量冗余。

**自适应阈值调度至关重要。** 相比固定阈值方案，自适应阈值调度策略能更一致地保持生成质量。其核心机制在于：早期去噪步骤对误差高度敏感（Fig. 9显示MSE从步骤11到21单调递减），采用线性递增阈值可在质量敏感阶段保守复用、在后期激进复用，维持每次干预的一致误差水平。

**窗口大小K=2取得最佳平衡。** Fig. 11的敏感性分析表明，K=2在精度与效率之间取得最优折衷。更大的窗口（K≥4）虽然能识别更多可复用标记，但标准误差计算的粒度变粗，导致误复用率上升，生成质量明显下降。

### 失败模式与局限性

尽管TIMERIPPLE在定量和定性评测中表现优异，仍需注意以下边界条件：

1. **端到端加速受限。** 当前方法仅针对自注意力模块（占推理延迟78%），未整合交叉注意力和MLP层。实际端到端延迟降低可能低于理论加速比，需结合系统级优化。

2. **与FlashAttention不兼容。** 复用策略的稀疏计算模式尚未与FlashAttention等IO优化注意力算子集成，无法直接实现端到端延迟降低。这是从理论加速到实际部署的关键缺口。

3. **超参数需手动设定。** 阈值范围（`θ_{t,max}`、`θ_{t,min}`）和起止步（`i_min`、`i_max`）需针对不同vDiT模型分别调参（Table 1），缺乏自动化搜索方案，增加了跨模型迁移的成本。

![[assets/figures/papers/paper_list_l941_https_openaccess_thecvf_com_content_CVPR2026_html_Mao_TimeRipples_Accele/figures/009_Table_1.jpg]]
*Table 1: Hyperparameter values for each model. These values are used in our experiments with HunyuanVideo, Wan2.1, CogVideoX, and Open-Sora-Plan models*

4. **早期步骤依赖。** 方法对去噪早期步骤的严格处理（前10步不干预）限制了在极低步数生成场景（如10步以内的蒸馏模型）中的应用，因为可操作步骤占比过低。

5. **长视频验证不足。** 大部分实验基于标准长度视频，虽在四个模型上验证了趋势，但更长视频的时空相关性模式可能发生变化，需进一步验证。

![[assets/figures/papers/paper_list_l941_https_openaccess_thecvf_com_content_CVPR2026_html_Mao_TimeRipples_Accele/figures/010_Table_2.jpg]]
*Table 2: Quantitative evaluation of our method, TIMERIPPLE, against the state-of-the-arts [3, 16, 40, 51] on four widely-adopted vDiTs: HunyuanVideo [17], CogVideoX [45] and Open-Sora-Plan [21]. We annotate the best and second-best results among all methods*

![[assets/figures/papers/paper_list_l941_https_openaccess_thecvf_com_content_CVPR2026_html_Mao_TimeRipples_Accele/figures/011_Figure_10.jpg]]
*Figure 10: The qualitative evaluations of TIMERIPPLE against other methods. “→” shows the major artifacts in prior studies*

## 定位与知识库关联

### 1. 问题定位：vDiT 推理瓶颈的本质

视频扩散 Transformer（vDiT）已成为视频生成的主流架构，但其推理成本极高。**核心瓶颈**在于自注意力计算：在四个主流 vDiT 模型（HunyuanVideo、Wan2.1、CogVideoX、Open-Sora-Plan）上，自注意力平均占据 Nvidia H100 推理总延迟的 **78%**（Fig. 4）。这一瓶颈的根源并非硬件限制，而是计算中存在大量**时空冗余**——相邻帧或相邻空间位置的标记在注意力图上高度相似，却仍被独立完整计算。

### 2. 与现有加速方法的关系

TIMERIPPLE 属于**训练无关的注意力稀疏化**路线，与以下四类方法形成对比与互补：

#### 2.1 动态显著性跳过：∆-DiT（Chen et al., 2024）

∆-DiT 基于通道显著性动态跳过注意力计算，是最直接的对比基线。TIMERIPPLE 与 ∆-DiT 的本质区别在于**操作粒度**：∆-DiT 在完整的注意力矩阵层面做二值化跳过决策，而 TIMERIPPLE 沿**通道维度**稀疏计算部分注意力分数并复用相似标记的已有结果。这一差异在相同 token 节省比例下产生了数量级的 MSE 优势（Fig. 7），在 HunyuanVideo 上 PSNR 领先 **+8.97 dB**（35.06 vs. 26.09，Table 2）。

#### 2.2 LLM 稀疏注意力迁移：MInference（Jiang et al., NeurIPS 2024）

MInference 将 LLM 中的动态稀疏模式迁移至 vDiT 加速。TIMERIPPLE 的关键区分点在于**利用 vDiT 特有的结构先验**：vDiT 通过 RoPE 将通道维度划分为时间、x 方向、y 方向三个独立组（Eq. 2），这一分组为通道级复用提供了天然的结构基础。MInference 缺乏对此结构的利用，其稀疏模式未针对视频的时空特性优化。

#### 2.3 预定义时空掩码：Sparse VideoGen / SVG（Xi et al., 2025）

SVG 使用预定义的时空稀疏掩码跳过自注意力计算。TIMERIPPLE 的**复用**策略与 SVG 的**跳过**策略在机制上互补——TIMERIPPLE 75% + SVG 70% 的组合方案在实验中展现出叠加效果（Table 2），表明两种策略可协同工作。

#### 2.4 跨步广播复用：PAB（Zhao et al., 2024）

PAB 通过跨去噪步广播中间注意力结果减少计算，其复用发生在**时间维度（去噪步间）**。TIMERIPPLE 的复用则发生在**单步内的标记间**，利用的是同一去噪步内标记的时空相似性。两者在复用维度上正交，理论上可叠加。

### 3. 方法适用边界

**适用条件**：
- 基于 Transformer 的视频扩散模型，且使用 RoPE 将通道按语义分组（时间/x/y）——这是当前主流 vDiT 的共性设计
- 去噪步数足够（≥11 步），使自适应阈值调度有足够的调节空间
- 生成质量对早期去噪步敏感的场景，可通过阈值调度维持质量

**不适用或效果受限的场景**：
- **极低步数生成**（如 <10 步）：阈值调度需要 11-21 步的调节窗口，极低步数下无法有效运作
- **非 RoPE 分组的 Transformer**：方法依赖通道维度的语义分组结构，若模型未采用此设计，需重新验证时空相关性的存在形式
- **端到端实际加速**：当前实现仅针对自注意力模块，未整合 FlashAttention 等 IO 优化算子，理论加速（最高 2.7×）与实际延迟降低之间存在差距

### 4. 局限性与开放问题

#### 4.1 已明确的局限

1. **模块覆盖不完整**：仅加速自注意力，未覆盖交叉注意力和 MLP 层，端到端加速上限受 Amdahl 定律约束。
2. **底层实现未整合**：复用策略尚未与 FlashAttention 等高效注意力实现结合，无法直接转化为端到端延迟降低。
3. **超参数需手动设定**：阈值范围（θ_{t,min}, θ_{t,max}）和起止步（i_min, i_max）需针对不同 vDiT 模型单独调参（Table 1），缺乏自动化方案。
4. **模型覆盖有限**：大部分实验基于 HunyuanVideo，虽在 CogVideoX、Open-Sora-Plan、Wan2.1 上验证了趋势，但更广泛的模型和更长视频的测评仍不足。

#### 4.2 开放研究问题

1. **与 IO 优化算子的融合**：如何将通道级复用策略与 FlashAttention 的内存分层访问模式有机结合，是实现端到端实际加速的关键工程挑战。
2. **跨任务泛化**：通道级时空相关性是否在图像生成（DiT）、3D 生成、视频预测等任务中同样成立？若能泛化，该方法的应用范围将大幅扩展。
3. **自动化阈值搜索**：能否设计元学习或预测网络，根据模型架构和生成设置自动搜索最优阈值配置，消除手工调参成本？
4. **与其他加速维度的组合**：TIMERIPPLE 与 PAB（跨步复用）、SVG（空间掩码）已展示初步的组合效果，系统性地探索多维度加速策略的叠加空间是一个有前景的方向。

## 原文 PDF

![[paperPDFs/CVPR_2026/TimeRipples_Accelerating_vDiTs_by_Understanding_the_Spatio_Temporal_Correlations_in_Latent_Space.pdf]]
