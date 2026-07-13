---
title: "D2Cache: Second-Order Delta Caching for Higher Video Diffusion Acceleration"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/D2Cache_Second_Order_Delta_Caching_for_Higher_Video_Diffusion_Acceleration.pdf
project_link: null
code_link: "https://github.com/VG-Huai/D2Cache"
aliases:
- D2Cache
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/generative_models_diffusion
- topic/generative_models_diffusion/diffusion_image_video
core_operator: 扩散过程输出二阶增量（δ2）表现出比一阶增量更高的平滑性与低方差，结合时间步嵌入导出的误差代理（et）对二阶累积和进行自适应缩放（因子s），可有效校正一阶缓存的累积误差并提升预测精度。
primary_logic: 将扩散模型缓存建模为离散导数问题，首次引入二阶差分动态（δ2）实现更高精度预测，并利用时间步嵌入驱动的缩放机制处理任意间隔的缓存，以训练无关的即插即用方式突破一阶方法的质量瓶颈。
claims:
- 定理1证明二阶预测器局部截断误差为O((Δt)^3)，相比一阶的O((Δt)^2)提升一个量级，理论保证了误差抑制能力。
- 在Latte超快模式下，D2Cache在相同加速比下VBench得分比SOTA TeacCache提高0.42%（76.03% vs. 75.61%），且开销可忽略。
- 消融移除缩放因子s导致VBench大幅下降1.72%（从76.03%到74.31%），验证自适应缩放对二阶校正的关键作用。
- 在超快加速下的复杂视频生成中，D2Cache保持接近无缓存的清晰度，而TeaCache出现严重伪影和不连贯。
---

# D2Cache: Second-Order Delta Caching for Higher Video Diffusion Acceleration

> [!tip] 核心洞察
> 将扩散模型缓存建模为离散导数问题，首次引入二阶差分动态（δ2）实现更高精度预测，并利用时间步嵌入驱动的缩放机制处理任意间隔的缓存，以训练无关的即插即用方式突破一阶方法的质量瓶颈。

| 字段 | 内容 |
|------|------|
| 中文题名 | D2Cache：面向更高效视频扩散加速的二阶增量缓存 |
| 英文题名 | D2Cache: Second-Order Delta Caching for Higher Video Diffusion Acceleration |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://openaccess.thecvf.com/content/CVPR2026/html/Liu_D2Cache_Second-Order_Delta_Caching_for_Higher_Video_Diffusion_Acceleration_CVPR_2026_paper.html) · [Code](https://github.com/VG-Huai/D2Cache) |
| Topic | #topic/vision_multimodal_applications #topic/generative_models_diffusion #topic/generative_models_diffusion/diffusion_image_video |
| Method | D2Cache |
| Dataset | Latte (16 frames, 512×512) superfast mode, Latte (16 frames) fast mode |

> [!tip] 效果简介
> - Latte (16 frames, 512×512) superfast mode 上，VBench (%) 76.03 (D2Cache-superfast) vs 75.61 (TeaCache-superfast) (+0.42%)。
> - Latte (16 frames) fast mode 上，Speedup (×) 2.86× (D2Cache-fast) vs 2.88× (TeaCache-fast) (≈ same acceleration, better quality)。

## 概要

视频扩散模型在生成高质量视频方面取得了显著进展，但推理过程中的大量去噪步骤导致计算开销极大，严重制约了实时应用。缓存技术通过重用历史输出来跳过部分计算，成为加速推理的主流方案。然而，现有的一阶增量缓存方法（如 **TeaCache**，Liu et al., arXiv 2024）仅重用相邻时间步的预测残差 $\delta_1$，在动态非均匀缓存策略下，被忽略的高阶项会导致近似误差沿去噪步骤快速累积，使生成质量与加速比之间的权衡逼近理论极限——在更大加速倍率下视频质量急剧下降。

本文提出 **D2Cache**，一种面向视频扩散模型的训练无关、即插即用的二阶增量缓存方法。其核心洞察在于将扩散模型缓存建模为离散导数问题：一阶增量 $\delta_1$ 对应一阶差分，而二阶增量 $\delta_2$ 则捕捉了一阶增量本身的变化。由于 $\delta_2$ 在去噪过程中表现出显著更低的幅度和方差（Figure 3），将其作为附加校正项引入预测公式，可以有效抑制一阶缓存的累积误差。理论分析表明，二阶预测器的局部截断误差为 $O((\Delta t)^3)$，相比一阶方法的 $O((\Delta t)^2)$ 提升一个量级（Theorem 1）。此外，D2Cache 利用时间步嵌入导出的误差代理 $e_t$，对二阶累积和进行自适应缩放，从而在任意间隔的缓存场景下保持预测精度。

在四种主流视频扩散模型（Latte、Open-Sora、Wan2.1 等）上的实验表明，D2Cache 在相同缓存调度和加速比下始终优于 TeaCache。在 Latte 超快模式下，D2Cache 的 VBench 得分达到 76.03%，比 TeaCache 的 75.61% 提升 0.42 个百分点（Table 1）；消融实验进一步证实，移除自适应缩放因子 $s$ 会导致性能大幅下降 1.72 个百分点（Table 2），验证了二阶校正机制的关键作用。在定性对比中，D2Cache 在超快加速下仍能保持接近无缓存的视频连贯性和清晰度，而一阶方法则出现严重伪影（Figure 6）。

### 视频扩散模型的加速瓶颈

视频扩散模型在生成高质量视频方面取得了显著进展，但其推理过程需要反复执行大型去噪网络，导致巨大的计算开销与延迟。为缓解这一问题，**增量缓存（Delta Caching）** 被提出作为一种训练无关的加速范式：其核心思想是利用扩散步骤间模型输出的残差（一阶增量）来预测未来时间步的输出，从而跳过部分网络前向计算。

### 一阶增量缓存的根本局限

现有的一阶增量缓存方法（如 **TeaCache** (Liu et al., arXiv 2024)）仅重用相邻时间步的预测残差 $\delta_1(t)$，其估计公式为：

$$\hat{f}(t-1) = f(t) + \delta_1(t)$$

从离散导数视角看，这等价于仅使用一阶差分进行外推，其局部截断误差为 $e_1(t) = O((\Delta t)^2)$。在动态非均匀缓存策略下，被忽略的高阶项导致近似误差沿去噪步骤**快速累积**，使生成质量与加速比之间的权衡逼近理论极限，难以在更大加速倍率下维持视频质量。

### 二阶差分的核心洞察

D2Cache 将扩散模型缓存重新建模为**离散导数问题**。关键观察在于：扩散过程输出的二阶增量 $\delta_2(t) = \delta_1(t) - \delta_1(t+1)$ 表现出比一阶增量**更高的平滑性与更低的方差**（见 Figure 3）。这一特性意味着二阶差分可以作为低成本的高精度校正项，有效抑制一阶缓存的累积误差。

### 非均匀间隔的挑战

实际缓存策略中，缓存步之间的间隔是动态变化的。直接将一阶增量复用于非连续时间步会引入额外的近似偏差，而现有方法缺乏针对间隔波动的自适应调节机制。D2Cache 通过利用时间步嵌入导出的误差代理 $e_t$ 对二阶累积和进行**自适应缩放**（因子 $s$），首次解决了任意间隔下的二阶校正问题，以训练无关的即插即用方式突破了一阶方法的质量瓶颈。

## 核心方法与创新机理

D2Cache 的核心创新在于将视频扩散模型的缓存预测从一阶增量（δ₁）提升至二阶差分（δ₂）动态，并结合时间步嵌入驱动的自适应缩放机制，首次在训练无关的即插即用框架下突破了一阶缓存方法的质量瓶颈。其关键改动可归纳为以下四个 changed slots。

### 预测公式：从一阶增量到缩放二阶累积和

一阶缓存方法（如 **TeaCache**，Liu et al., arXiv 2024）仅重用相邻时间步的预测残差，其估计形式为：

$$ \hat{f}(t-1) = f(t) + \delta_1(t) $$

D2Cache 将预测公式扩展为包含二阶差分累积和的自适应形式（Eq. 15）：

$$ \hat{f}(t-y) = f(t-y+1) + \delta_1(t-x) + s \cdot \sum_{k=1}^{x} \delta_2(t-k) $$

其中 $x$ 为已知步间隔，$y$ 为缓存步间隔，$s$ 为自适应缩放因子。这一改动将缓存的预测能力从局部线性近似提升为局部二次近似，为误差抑制提供了结构性基础。

### 局部截断误差阶数：从 $O((\Delta t)^2)$ 到 $O((\Delta t)^3)$

论文通过定理1证明了二阶预测器的局部截断误差为 $O((\Delta t)^3)$，相较于一阶方法的 $O((\Delta t)^2)$ 提升了一个量级。这一理论保证源于二阶差分对输出函数曲率的捕捉能力——一阶差分仅反映一阶导数信息，而二阶差分可补偿二阶导数带来的非线性变化。Figure 3 从实证角度验证了二阶增量（δ₂）的 L2 范数远小于一阶增量（δ₁），且沿去噪步骤表现出更高的平滑性与低方差，这为误差量级提升提供了数值基础。

### 非均匀间隔处理：从直接复用到自适应缩放

实际缓存调度中，计算步与缓存步之间的间隔往往是动态非均匀的。一阶方法直接复用一阶增量，未对间隔波动进行任何补偿，导致近似误差在非连续间隔中快速累积。D2Cache 引入基于时间步嵌入的误差代理 $e_t$，通过多项式拟合时间步嵌入调制输入的 L1 范数（Figure 4），动态计算缩放因子：

$$ s = \frac{\sum_{k=1}^{y-x} e_{t-x-k}}{\sum_{k=1}^{x} e_{t-k}} $$

该缩放因子实质上是缓存间隔与已知间隔的累积误差代理之比，使得二阶累积和能够自适应匹配任意间隔的误差补偿需求。消融实验（Table 2）显示，移除缩放因子 $s$ 后 VBench 得分从 76.03% 骤降至 74.31%（-1.72%），验证了这一机制对维持预测精度的关键作用。

### 缓存校正维度：从一阶残差重用到二阶残差变化

一阶缓存仅利用输出的一阶差分（即残差本身）进行重用，本质上是对去噪轨迹的线性外推。D2Cache 将校正维度扩展至二阶差分——即一阶差分的差分：

$$ \delta_2(t) = \delta_1(t) - \delta_1(t+1) $$

这相当于引入了去噪轨迹的“加速度”信息。Figure 5 的轨迹对比直观展示了这一维度的价值：在超快加速模式下，D2Cache 的输出 L2 范数轨迹紧密贴合无缓存默认轨迹，而一阶缓存轨迹则出现显著偏离，表明二阶校正有效抑制了累积误差的扩散。

### 创新本质：离散导数视角下的缓存建模

上述四个 changed slots 共同指向一个核心洞察：将扩散模型缓存重新建模为离散导数问题。一阶缓存对应一阶后向差分近似，而 D2Cache 通过引入二阶差分实现了更高精度的预测。这一视角不仅为缓存方法提供了严格的理论框架（定理1），还使得方法天然具备训练无关、即插即用的特性——D2Cache 不改变缓存调度策略与超参数，仅作为预测修正模块嵌入现有管线，在保持相同加速比的前提下提升生成质量。在 Latte 超快模式下，D2Cache 以可忽略的延迟开销（<0.3s）将 VBench 得分从 TeaCache 的 75.61% 提升至 76.03%，并在 Wan2.1 等复杂模型上展现出更显著的伪影抑制能力（Figure 6）。

D2Cache 的整体管线在已有的一阶增量缓存（如 **TeaCache**，Liu et al., arXiv 2024）之上，引入一个轻量的二阶校正分支，形成训练无关、即插即用的预测增强架构。其核心设计遵循“计算—缓存—预测—校正”四阶段流，所有额外模块均不改变去噪步的调度频率，因此加速比与基线完全可比。

### 管线总览

如 **Figure 2** 所示，D2Cache 的推理管线包含两条并行的信息流：

![[assets/figures/papers/paper_list_l851_https_openaccess_thecvf_com_content_CVPR2026_html_Liu_D2Cache_Second_Ord/figures/002_Figure_2.jpg]]
*Figure 2: Top: Overall pipeline of D2Cache compared to common first-order delta caching. In first-order caching (bottom branch), residuals (δ1(t)) are reused across timesteps, but errors accumulate in non-contiguous intervals due to ignored higher-order terms. D2Cache (additional top branch) incorporates second-order deltas (δ2(t)) and dynamically scales the cumulative sum Pak=1 δ2(t − k) using factor s, enabling accurate corrections over arbitrary intervals and reducing cumulative errors. Bottom: Example video frames from a complex prompt, illustrating preserved coherence in D2Cache under caching*

1. **一阶缓存分支（底部路径）**：在计算步（compute step）获取当前扩散模型输出 $f(t)$，并计算相邻时间步的一阶差分 $\delta_1(t) = f(t) - f(t+1)$（Eq. 3）。当遇到缓存步（cache step）时，直接复用最近计算步的一阶增量进行预测：$\hat{f}(t-1) = f(t) + \delta_1(t)$（Eq. 2）。这是 TeaCache 等一阶方法的标准流程。

2. **二阶校正分支（顶部路径）**：在计算步同步计算二阶差分 $\delta_2(t) = \delta_1(t) - \delta_1(t+1)$（Eq. 10），并利用时间步嵌入驱动的误差代理 $e_t$ 动态计算自适应缩放因子 $s$（Eq. 14）。缓存步的最终预测由一阶增量与缩放后的二阶累积和共同构成：$\hat{f}(t-y) = f(t-y+1) + \delta_1(t-x) + s \cdot \sum_{k=1}^{x} \delta_2(t-k)$（Eq. 15）。

两条分支共享同一套缓存调度策略与超参数阈值，D2Cache 仅替换缓存步的预测公式，不增加额外的模型前向计算。

### 模块功能与数据流

D2Cache 的六个核心模块按执行时序组织如下：

| 模块 | 功能 | 输入 | 输出 | 关键公式/证据 |
|------|------|------|------|--------------|
| 原始输出获取 | 在计算步执行扩散模型前向，获得当前输出 | 噪声潜变量 $x_t$、时间步 $t$ | $f(t)$ | Section 3.1 |
| 一阶差分计算 | 计算相邻计算步输出的增量 | $f(t), f(t+1)$ | $\delta_1(t)$ | Eq. (3) |
| 二阶差分计算 | 计算一阶增量的变化率 | $\delta_1(t), \delta_1(t+1)$ | $\delta_2(t)$ | Eq. (10) |
| 时间步嵌入误差估计 | 利用时间步嵌入调制的输入估计二阶增量幅值代理 | 时间步嵌入、调制输入 | 误差代理 $e_t$ | Section 3.3, Figure 4 |
| 缩放因子计算 | 根据累积误差代理之比自适应缩放二阶项 | $e_t$ 序列、间隔 $x, y$ | 缩放因子 $s$ | Eq. (14) |
| 二阶缓存预测 | 在缓存步生成最终预测输出 | $f(t-y+1), \delta_1(t-x), \{\delta_2\}, s$ | $\hat{f}(t-y)$ | Eq. (15) |

### 输入输出流

- **计算步**：执行模块 1→2→3→4，产出并缓存 $f(t), \delta_1(t), \delta_2(t), e_t$。
- **缓存步**：跳过模型前向，执行模块 5→6，利用已缓存的增量与误差代理直接合成预测输出。
- **关键约束**：二阶校正分支仅在计算步维护状态，缓存步仅进行轻量代数运算，额外延迟 < 0.3 秒（Table 1），开销可忽略。

### 设计动机与理论保障

一阶缓存方法在非均匀间隔下，被忽略的高阶项导致近似误差沿去噪步骤快速累积，成为质量瓶颈。D2Cache 通过引入二阶差分 $\delta_2$ 作为校正项，将局部截断误差从一阶的 $O((\Delta t)^2)$ 降至 $O((\Delta t)^3)$（Theorem 1），从理论上保证了误差抑制能力。同时，时间步嵌入误差代理 $e_t$ 使缩放因子 $s$ 能够动态适配任意缓存间隔，解决了非均匀调度下二阶项幅值波动的问题（Figure 4 验证了代理与真实二阶残差的相关性）。

> **注意**：更高阶差分（如三阶）的缓存潜力、在非 DiT 架构上的适用性等问题尚未在本文中探索，属于开放问题。

D2Cache 将视频扩散模型中的缓存预测问题建模为离散导数问题，通过引入二阶差分动态突破一阶增量缓存的精度瓶颈。其核心由三个紧密协作的模块构成：二阶差分计算、时间步嵌入误差估计，以及自适应缩放因子计算。

### 一阶缓存的形式化与误差分析

给定扩散模型在时间步 $t$ 的输出 $f(t)$，一阶后向差分定义为：

$$\delta _ { 1 } ( t ) = f ( t ) - f ( t + 1 )$$

一阶缓存通过重用相邻时间步的增量来估计未来输出：

$$\hat { f } ^ { ( 1 ) } ( t - 1 ) = f ( t ) + \delta _ { 1 } ( t )$$

该预测器的局部截断误差为 $e _ { 1 } ( t ) = O ( ( \Delta t ) ^ { 2 } )$。在动态非均匀缓存调度下，被忽略的高阶项导致近似误差沿去噪步骤快速累积，使生成质量与加速比之间的权衡逼近理论极限。

### 二阶差分计算

D2Cache 的核心创新在于引入二阶差分作为附加校正项。二阶差分定义为一阶差分的差分：

$$\delta _ { 2 } ( t ) = \delta _ { 1 } ( t ) - \delta _ { 1 } ( t + 1 )$$

**定理1** 证明，使用二阶预测器：

$$\hat { f } ^ { ( 2 ) } ( t - 1 ) = f ( t ) + \delta _ { 1 } ( t ) + \delta _ { 2 } ( t )$$

其局部截断误差为 $e _ { 2 } ( t ) = O ( ( \Delta t ) ^ { 3 } )$，相比一阶的 $O((\Delta t)^2)$ 提升一个量级，从理论上保证了更强的误差抑制能力。图3的实证分析显示，二阶增量（$\delta_2$）的 L2 范数幅度和方差均远小于一阶增量，验证了其作为稳定校正信号的可行性。

### 时间步嵌入误差估计

为实现非均匀间隔下的自适应校正，D2Cache 利用时间步嵌入调制的输入计算相对 L1 距离，并通过多项式拟合得到误差代理 $e_t$。该代理能够有效估计二阶增量在不同扩散阶段的幅值变化，为后续的自适应缩放提供依据。

### 自适应缩放因子计算

面对任意缓存间隔，D2Cache 将二阶预测器扩展为累积和形式。对于从已知计算步 $t-x$ 到缓存步 $t-y$（$y > x$）的预测，缩放因子 $s$ 基于累积误差代理之比计算：

$$s = { \frac { \sum _ { k = 1 } ^ { y - x } e _ { t - x - k } } { \sum _ { k = 1 } ^ { x } e _ { t - k } } }$$

该因子动态补偿非均匀间隔引入的波动，确保二阶校正项在不同缓存距离下保持适当的贡献强度。

### 最终 D2Cache 估计

结合上述组件，D2Cache 的最终缓存预测公式为：

$$\hat { f } ( t - y ) = f ( t - y + 1 ) + \delta _ { 1 } ( t - x ) + s \cdot \sum _ { k = 1 } ^ { x } \delta _ { 2 } ( t - k )$$

该公式将一阶增量与自适应缩放后的二阶累积和相结合，在保持训练无关、即插即用特性的同时，显著抑制了非均匀缓存策略下的累积误差。消融实验证实，移除缩放因子 $s$ 会导致 VBench 得分大幅下降 1.72%（从 76.03% 降至 74.31%），验证了自适应缩放机制对维持高质量的关键作用。

![[assets/figures/papers/paper_list_l851_https_openaccess_thecvf_com_content_CVPR2026_html_Liu_D2Cache_Second_Ord/figures/003_Figure_3.jpg]]
*Figure 3: Comparison of the first-order (green) and the secondorder (red) deltas in L2 norm value across diffusion steps*

## 实验与关键发现

### 主实验结果

D2Cache 在四种视频扩散模型、多种采样调度器、分辨率和视频长度下进行了系统评估。所有方法采用相同的缓存调度策略与超参数（如 TeaCache 的阈值），D2Cache 仅作为即插即用的预测修正，不改变缓存频率，因此加速率与质量比较是公平的。

**Table 1** 汇总了 D2Cache 与一阶增量缓存 SOTA 方法 TeaCache（Liu et al., arXiv 2024）的核心对比。在 Latte（16 帧，512×512）superfast 模式下，D2Cache 的 VBench 得分达到 **76.03%**，较 TeaCache 的 75.61% 提升 **+0.42%**；在 fast 模式下，D2Cache 加速比为 2.86×，与 TeaCache 的 2.88× 基本持平，但视觉质量更优。在 Wan2.1-1.3B 超快加速（3.61×）下，**Table 3** 显示 D2Cache 在多个清晰度指标上大幅超过 TeaCache，并接近无缓存默认生成水平。定性对比（**Figure 6**）进一步证实：复杂文本提示下，TeaCache 出现严重伪影和不连贯，而 D2Cache 保真度接近默认生成。

### 消融实验

**Table 2** 展示了缩放因子 $s$ 的消融结果（Latte superfast 模式）。移除 $s$ 后，VBench 从 76.03% 骤降至 **74.31%**（下降 1.72%），验证了自适应缩放对二阶校正的关键作用。若完全移除二阶项回退到一阶缓存，性能与 TeaCache 一致（75.61%），表明二阶项独立贡献了 +0.42% 的 VBench 提升。

### 关键图表分析

**Figure 1** 的质量-延迟曲线显示，D2Cache 在相同缓存调度下始终位于 TeaCache 上方，表明其在同等加速比下能提供更优的视觉质量。**Figure 3** 揭示二阶增量（$\delta_2$）的 L2 范数幅度和方差远小于一阶增量，这是二阶缓存预测更稳定的经验基础。**Figure 4** 验证了时间步嵌入调制的输入与二阶残差幅值之间存在强相关性，支持将其作为误差代理 $e_t$ 用于自适应缩放。**Figure 5** 的输出 L2 范数轨迹对比表明，D2Cache 轨迹更贴近无缓存默认轨迹，累积误差显著小于一阶缓存，与定理 1 的理论保证（局部截断误差从 $O((\Delta t)^2)$ 降至 $O((\Delta t)^3)$）一致。

### 效率与开销

D2Cache 的二阶差分计算和缩放因子推导引入的开销可忽略（延迟增加 <0.3s），不影响整体加速比。该方法以训练无关的即插即用方式增强现有缓存策略，无需重新训练或调整缓存频率。

### 失败模式与局限

论文未报告明确的失败模式。在超快加速场景下，D2Cache 虽显著优于一阶方法，但与无缓存默认生成之间仍存在可察觉的质量差距（见 Figure 6 细节放大区域）。当前实验覆盖的模型规模（如 Wan2.1-1.3B）和视频长度有限，在更大规模模型或更长序列上的表现需手动验证。更高阶差分（如三阶）的潜力、与其他加速范式（稀疏注意力、模型量化）的组合效益，以及在非 DiT 架构上的适用性，均为开放问题。

![[assets/figures/papers/paper_list_l851_https_openaccess_thecvf_com_content_CVPR2026_html_Liu_D2Cache_Second_Ord/figures/008_Figure_6.jpg]]
*Figure 6: Qualitative comparisons on complex prompts using Wan2.1-1.3B under superfast acceleration (3.61×). Frames from default (no caching), TeaCache-superfast, and D2Cache-superfast settings are shown, with zoomed-in details on the right. TeaCache suffers severe degradation (e.g., artifacts, incoherence), while D2Cache preserves fidelity close to default*

![[assets/figures/papers/paper_list_l851_https_openaccess_thecvf_com_content_CVPR2026_html_Liu_D2Cache_Second_Ord/figures/001_Figure_1.jpg]]
*Figure 1: Quality-latency comparison of video diffusion models. Visual quality versus latency curves of the proposed D2Cache and TeaCache [26] using 4 different video diffusion models. D2Cache significantly outperforms TeaCache under identical caching schedules*

![[assets/figures/papers/paper_list_l851_https_openaccess_thecvf_com_content_CVPR2026_html_Liu_D2Cache_Second_Ord/figures/006_Table_1.jpg]]
*Table 1: Quantitative evaluation of inference efficiency and visual quality in video generation models. D2Cache consistently achieves superior efficiency and better visual quality across different base models, sampling schedulers, video resolutions, and lengths. Methods marked with * are reported from cited papers and not re-evaluated in our setup*

![[assets/figures/papers/paper_list_l851_https_openaccess_thecvf_com_content_CVPR2026_html_Liu_D2Cache_Second_Ord/figures/007_Table_2.jpg]]
*Table 2: Ablation study on scale factor s with Latte under superfast mode*

## 定位与知识库关联

### 一阶增量缓存谱系与瓶颈

D2Cache 直接建立在扩散模型**一阶增量缓存**（first-order delta caching）的研究脉络之上。该谱系的核心思想是：在扩散去噪过程中，相邻时间步的模型输出高度相似，因此可以跳过部分计算步，通过重用先前时间步的预测残差（一阶增量 $\delta_1$）来估计被跳过步骤的输出，从而减少推理延迟。

**TeaCache**（Liu et al., arXiv 2024）是该谱系中具有代表性的 SOTA 方法，它提供了缓存调度策略和基于时间步嵌入的误差估计机制，通过设定阈值动态决定哪些步骤需要实际计算、哪些步骤可以缓存复用。**EasyCache**（Zhou et al., arXiv 2025）则从运行时自适应角度进一步优化了一阶缓存策略。此外，**PAB**（Zhao et al., ICLR 2025）基于金字塔注意力广播实现缓存加速，属于并行路线。

**核心瓶颈**：一阶增量缓存仅重用相邻时间步的预测残差 $\delta_1(t)$。在动态非均匀缓存策略下（缓存间隔 $x$ 可变），被忽略的高阶项导致近似误差沿去噪步骤快速累积。D2Cache 论文的定理 1 给出了理论解释：一阶预测器的局部截断误差为 $O((\Delta t)^2)$，而二阶预测器可达 $O((\Delta t)^3)$，提升一个量级。这一累积误差使生成质量与加速比之间的权衡逼近理论极限，难以在更大加速倍率下维持视频质量。

### D2Cache 的创新定位

D2Cache 在该谱系中引入了**二阶差分动态**（second-order delta dynamics），将扩散模型缓存问题建模为离散导数问题。其核心创新点可归纳为三个递进的“变化槽位”：

| 变化维度 | 一阶缓存基线 | D2Cache 方案 | 证据锚点 |
|---------|-------------|-------------|---------|
| 预测公式 | $f(t) + \delta_1(t)$ | $f(t-y+1) + \delta_1(t-x) + s \cdot \sum \delta_2(t-k)$ | Eq. (11), Eq. (15) |
| 局部截断误差阶数 | $O((\Delta t)^2)$ | $O((\Delta t)^3)$ | Theorem 1 |
| 非均匀间隔处理 | 直接复用一阶增量，无自适应调节 | 基于时间步嵌入误差代理 $e_t$ 动态计算缩放因子 $s$ | Eq. (14), Figure 4 |
| 缓存校正维度 | 仅一阶残差重用 | 二阶残差变化作为附加校正项 | Section 3.2.2 |

**因果机制**：扩散过程输出二阶增量 $\delta_2(t) = \delta_1(t) - \delta_1(t+1)$ 表现出比一阶增量更高的平滑性与低方差（Figure 3 显示方差约降低 90%）。同时，时间步嵌入调制的输入与二阶残差幅值存在强相关性（Figure 4），使得可以通过多项式拟合导出误差代理 $e_t$，进而计算自适应缩放因子 $s = \frac{\sum e_{t-x-k}}{\sum e_{t-k}}$，对二阶累积和进行动态缩放，补偿非均匀缓存间隔带来的误差波动。

**即插即用特性**：D2Cache 是训练无关（training-free）的即插即用方法，不改变缓存调度策略，仅作为预测修正模块叠加在现有缓存方法之上。实验表明，D2Cache 采用与 TeaCache 完全相同的缓存策略和阈值，在保持几乎相同加速比（如 Latte fast 模式：2.86× vs. 2.88×）的前提下，仅通过提升预测精度来改善生成质量。

### 适用边界与局限

**已验证的适用条件**：

- **架构**：论文在多种 DiT（Diffusion Transformer）架构上验证，包括 Latte、Open-Sora、Wan2.1 等视频扩散模型，覆盖不同参数量（如 Wan2.1-1.3B）和视频分辨率/长度。
- **采样调度器**：兼容多种采样调度器（Table 1 覆盖不同 scheduler 设置）。
- **加速模式**：在 fast 和 superfast 两种加速模式下均有效，superfast 模式下增益更为显著（VBench 提升 0.4%–2.5%）。
- **兼容性**：与现有缓存方法（TeaCache、EasyCache）兼容，可作为插件叠加使用。

**已知局限与待验证边界**：

1. **更高阶差分潜力未探明**：论文仅探索到二阶差分缓存。三阶及以上差分的缓存是否能进一步压制累积误差、是否存在收益递减点，均为开放问题。
2. **超长序列与大模型扩展性**：在更长视频序列或更大规模视频生成模型上的可扩展性和效果尚未验证。
3. **非 DiT 架构适用性**：论文实验集中于 DiT 架构，在 U-Net 架构或条件控制任务上的适用性需要额外验证。
4. **与其他加速范式的组合**：能否与稀疏注意力、模型量化、步长蒸馏等正交加速技术叠加获得乘性效益，尚未探索。
5. **实时交互场景**：在实际实时交互式视频生成中的用户体验与端到端延迟是否满足需求，缺乏用户研究。

### 证据强度评估

D2Cache 的核心主张拥有较强的证据支撑：

- **理论保证**：Theorem 1 给出 $O((\Delta t)^3)$ 误差阶的数学证明（置信度 0.95）。
- **主实验**：Table 1 在 Latte superfast 模式下 VBench 得分 76.03% vs. TeaCache 75.61%（置信度 0.95）。
- **消融实验**：移除缩放因子 $s$ 导致 VBench 下降 1.72%（从 76.03% 到 74.31%），验证自适应缩放的关键作用（置信度 0.95）。
- **定性验证**：Figure 6 在 Wan2.1 superfast（3.61×）复杂提示下，D2Cache 保持接近无缓存的清晰度，而 TeaCache 出现严重伪影和不连贯（置信度 0.9）。
- **轨迹验证**：Figure 5 显示 D2Cache 的 L2 范数轨迹更贴近无缓存默认轨迹，累积误差更小（置信度 0.9）。

### 开放问题

1. **更高阶差分的收益边界**：三阶差分缓存是否能继续提升性能？是否存在理论上的最优阶数？
2. **跨架构泛化**：在非 DiT 架构（如 U-Net）或条件控制任务上的适用性如何？
3. **叠加加速范式**：能否与稀疏注意力、模型量化、步长蒸馏等正交加速技术组合，获得叠加效益？
4. **超长序列扩展**：在更长视频序列或更大规模模型上的可扩展性和效果如何？
5. **实时交互适用性**：实时交互式视频生成场景下的实际用户体验与延迟是否满足需求？

## 原文 PDF

![[paperPDFs/CVPR_2026/D2Cache_Second_Order_Delta_Caching_for_Higher_Video_Diffusion_Acceleration.pdf]]
