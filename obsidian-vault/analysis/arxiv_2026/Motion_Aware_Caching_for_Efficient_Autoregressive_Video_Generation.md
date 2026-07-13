---
title: Motion-Aware Caching for Efficient Autoregressive Video Generation
type: paper
paper_level: A
venue: arXiv
year: 2026
pdf_ref: paperPDFs/arxiv_2026/Motion_Aware_Caching_for_Efficient_Autoregressive_Video_Generation.pdf
project_link: null
code_link: https://github.com/ywlq/MotionCache
aliases:
- MACEAVG
tags:
- arxiv_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/image_and_video_generation
- topic/generative_models_diffusion
core_operator: 基于帧间差异的运动感知token重要性权重，结合加权误差累积与阈值决策，实现token级动态缓存调度。
primary_logic: 理论上证明帧间差异是残差不稳定性的上界，因此可作为轻量运动代理；结合前期粗粒度全局结构建立和后期细粒度运动感知缓存，实现高效推理。
claims:
- 缓存误差与相邻时间步的残差之差严格成正比，从而缓存可靠性由残差时间不稳定性决定。
- 残差差异被帧间差异所界定，帧间差是残差不稳定性的有效上界代理。
- 帧间差导出的token重要性排序与真实残差排序高度一致，NDCG＞0.94。
- 在SkyReels-V2上MotionCache-slow实现6.28×加速，VBench仅下降1%，PSNR 23.46；fast实现7.26×加速，VBench 82.75%。
---

# Motion-Aware Caching for Efficient Autoregressive Video Generation

> [!tip] 核心洞察
> 理论上证明帧间差异是残差不稳定性的上界，因此可作为轻量运动代理；结合前期粗粒度全局结构建立和后期细粒度运动感知缓存，实现高效推理。

| 字段 | 内容 |
|------|------|
| 中文题名 | 面向高效自回归视频生成的运动感知缓存 |
| 英文题名 | Motion-Aware Caching for Efficient Autoregressive Video Generation |
| 会议/期刊 | arXiv 2026 |
| Links | [paper](https://arxiv.org/abs/2605.01725v1) · [Code](https://github.com/ywlq/MotionCache) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/image_and_video_generation #topic/generative_models_diffusion |
| Method | MotionCache |
| Dataset | SkyReels-V2, MAGI-1 |

> [!tip] 效果简介
> - SkyReels-V2 (540p, 2 chunks, 97 frames) 上，Speedup | VBench | PSNR | SSIM | LPIPS 6.28× (slow) | 82.84% | 23.46 | 0.9093 | 0.0875 vs 1× (Vanilla) | 83.84% | 1 (relative) | 1 | 1 (+5.28× speedup | -1.00% VBench)；Speedup | VBench 7.26× (fast) | 82.75% vs 1× (Vanilla) | 83.84% (+6.26× speedup | -1.09% VBench)。
> - MAGI-1 (720p, 7 chunks, 24 frames) 上，Speedup | VBench | PSNR | SSIM | LPIPS 1.64× (slow) | 77.25% | 19.71 | 0.7231 | 0.2510 vs 1× (Vanilla) | 77.26% | 1 (relative) | 1 | 1 (+0.64× speedup | -0.01% VBench)；Speedup | VBench 2.07× (fast) | 74.59% vs 1× (Vanilla) | 77.26% (+1.07× speedup | -2.67% VBench)。

## 概要

自回归视频生成模型虽能产生高质量视频，但其逐块（chunk-wise）自回归推理范式带来了沉重的计算负担。现有加速方法——无论是**TeaCache**的粗粒度时间步（timestep）级缓存，还是**FlowCache**（Anonymous, ICLR 2025 under review）的chunk级缓存——均采用统一跳过策略，将整个时间步或chunk视为原子单元进行全计算或全复用。这种粗粒度策略忽略了一个关键事实：同一chunk内不同token的运动强度存在显著差异，导致动态区域因缓存不足而误差累积，静态区域却因过度计算而浪费资源。

**MotionCache**针对上述瓶颈，提出了一种运动感知的token级自适应缓存框架。其核心洞察在于：缓存误差严格正比于相邻时间步之间残差的不稳定性（**Proposition 4.1**），而残差不稳定性又被帧间差异所界定——帧间差是残差变化的有效上界代理（**Lemma 4.2**）。这一理论保证使得轻量的帧间L1距离可直接作为token运动重要性的可靠代理：实验表明，基于帧差的重要性排序与真实残差排序的NDCG始终高于0.94（**Figure 3**）。

基于此，MotionCache采用**粗到细双阶段推理调度**：第一阶段进行chunk级全更新预热，建立全局语义结构；第二阶段切换到token级稀疏计算，以运动权重加权累积误差，对每个token独立决策是否复用缓存残差。在SkyReels-V2上，MotionCache-slow实现**6.28×加速**，VBench仅下降1%（PSNR 23.46）；MotionCache-fast实现**7.26×加速**，VBench保持82.75%。在MAGI-1上同样取得1.64×–2.07×加速，质量几乎无损（**Table 1**）。

**方法定位**：MotionCache属于推理时缓存加速方法，在缓存粒度（chunk/timestep → token）、运动代理（无 → 帧间差）、误差累积策略（全局阈值 → 运动加权累积）和推理调度（全程统一 → 粗到细双阶段）四个维度上系统性地推进了现有方案。其理论框架将缓存可靠性归约为残差时间不稳定性，并用帧间差作为可计算的代理，为运动感知缓存提供了形式化基础。



### 自回归视频生成的效率瓶颈

自回归视频生成模型通过逐块（chunk-wise）自回归生成长视频序列，每个chunk包含若干帧，模型在去噪过程中需要为每个时间步计算速度场。这种逐块生成范式虽然保证了时序一致性，但带来了极高的计算开销——每个chunk的生成都需要完整的反向去噪过程，导致推理延迟随视频长度线性增长。

加速推理的核心思路是利用去噪过程中存在的**时间冗余**：相邻时间步的残差（residual）高度相似，因此可以缓存并复用之前计算的残差，跳过部分时间步的前向计算。现有方法如**TeaCache**和**FlowCache**（Anonymous, ICLR 2025 under review）分别采用timestep级和chunk级的统一跳过策略，将整个时间步或整个chunk视为原子单元进行缓存决策。

### 粗粒度缓存的根本缺陷

然而，这种粗粒度策略忽略了一个关键事实：**同一chunk内不同token的运动特征存在显著差异**。图2(a)显示，相邻时间步残差差异的分布呈现长尾特征——大多数token聚集在低值区域（中位数2.078），但存在一个延伸到高值（尾部9.878）的显著尾部，表明token间的更新需求高度非均匀。图2(b)进一步揭示了同一chunk内不同帧之间残差变化的宽动态范围（最大差异5.9219），证实了帧间运动特征的异质性。

粗粒度缓存的后果是系统性的：
- 对**动态区域**（如运动前景）统一复用缓存会导致误差累积，造成纹理细节丢失和结构不一致；
- 对**静态区域**（如背景）统一进行完整计算则造成算力浪费。

定性对比（图1）清晰地展示了这一问题：TeaCache因忽略帧内运动差异而丢失纹理细节，FlowCache则因chunk级统一决策导致结构不一致。

### 理论动机：从残差不稳定性到运动代理

MotionCache的核心洞察在于建立了**缓存误差与运动之间的理论联系**。具体而言，缓存误差被严格证明与相邻时间步的残差之差成正比（Proposition 4.1, Equation 7）：

$$\epsilon_{t-1}^{i} = \Delta t \cdot \| \mathcal{R}_{t-1}^{i} - \mathcal{R}_{t}^{i} \|_2$$

这意味着缓存可靠性完全由残差的时间不稳定性决定。进一步地，Lemma 4.2（Equation 8）证明了一个关键上界关系：

$$\| \mathcal{R}_{t-1}(\mathbf{X}_{t-1}^{(i,f)}) - \mathcal{R}_{t}(\mathbf{X}_{t}^{(i,f)}) \|_2 \lesssim C \cdot \| \mathbf{X}_{t}^{(i,f)} - \mathbf{X}_{t}^{(i,f-1)} \|_2$$

即**残差差异被帧间差异所界定**。这一理论结果将难以直接获取的残差不稳定性转化为可观测的帧间运动量，为轻量级运动代理提供了理论保证。

实验验证表明，基于帧间差异导出的token重要性排序与真实残差排序高度一致，NDCG分数始终保持在0.94以上（图3），证实了帧差作为运动代理的有效性。

### 本文动机与设计思路

基于上述分析，本文提出**MotionCache**，核心动机是打破粗粒度缓存的限制，实现token级的自适应缓存调度。设计思路遵循三个原则：

1. **运动感知**：利用帧间差异作为轻量运动代理，为每个token分配差异化的运动重要性权重；
2. **加权误差累积**：将运动权重融入误差累积过程，使动态token获得更高的更新频率，静态token获得更高的缓存复用率；
3. **粗到细调度**：前期采用chunk级全更新建立全局语义结构，后期切换到token级稀疏计算以捕捉精细运动动态（图6）。



## 核心方法与创新机理

MotionCache 的核心创新在于将自回归视频生成的缓存策略从**粗粒度统一跳过**推进到**token 级运动感知自适应调度**，其关键设计围绕四个 changed slots 展开。

### 1. 缓存粒度：从 chunk/timestep 级到 token 级自适应选择

现有方法（如 **TeaCache** 的 timestep 级跳过和 **FlowCache** 的 chunk 级复用）将整个时间步或自回归块作为原子单元进行全计算或全缓存决策（Figure 4 上栏）。这种粗粒度策略忽视了同一 chunk 内不同 token 的运动差异——Figure 2 揭示，相邻时间步残差差异呈长尾分布（中位数 2.078，尾部达 9.878），且 chunk 内帧间最大差异可达 5.9219，表明冗余性高度非均匀。

MotionCache 将决策粒度细化到每个 token：通过运动感知的误差累积机制，动态判断每个 token 是复用缓存残差还是执行前向计算（Figure 4 下栏），从而在动态区域保持高更新频率，在静态区域大幅削减计算。

### 2. 运动感知代理：帧间差异作为 token 重要性的轻量信号

粗粒度方法缺乏对 token 级运动重要性的显式建模。MotionCache 的理论基础是 **Proposition 4.1** 和 **Lemma 4.2**：缓存误差严格正比于真实残差与缓存残差的 L2 范数之差（Equation 7），而该残差差异被帧间差异所界定（Equation 8）——即帧间差是残差时间不稳定性的有效上界代理。

据此，MotionCache 定义 token 重要性地图 $\mathcal{M}_{t}^{(i,f)}$ 为相邻帧间的 token 级 L1 距离（Equation 9），并引入跨 chunk 边界的连续性处理。**Figure 3** 验证了该代理的保真度：帧差排序与真实残差排序的 NDCG 始终高于 0.94，证明帧间差能高精度近似 token 的真实更新需求。

### 3. 误差累积策略：运动权重加权累积与 token 级阈值决策

TeaCache 和 FlowCache 采用全局相对 L1 距离阈值进行统一决策，无法区分 token 的运动差异。MotionCache 设计了**运动权重加权的误差累积机制**：

- 首先通过逐帧 min-max 归一化将重要性线性映射到 $[\alpha, 1]$ 区间（Equation 10），其中 $\alpha$ 为软映射底数，保证静态区域仍获得基础更新频率；
- 每个 token 的误差累积量 $\mathcal{A}_{t}[p]$ 由运动权重乘以 chunk 整体更新幅度进行加权（Equation 12）；
- 当累积误差超过阈值 $\tau$ 时，该 token 被选中进行前向计算（Equation 13）。

消融实验（Table 2, Table 4）表明 $\alpha=0.6$ 在 PSNR/SSIM/LPIPS 上取得最佳质量-效率平衡：$\alpha$ 过小导致静态区域退化，$\alpha=1$ 则退化为 FlowCache 的无差别缓存。

### 4. 推理调度：粗到细双阶段策略

现有方法全程采用统一策略，MotionCache 引入**粗到细双阶段推理调度**（Section 5.3, Figure 6）：

- **Phase 1（粗粒度结构建立）**：前 $K$ 步强制 chunk 级全更新，确保全局语义结构充分建立。Figure 6 显示早期去噪步的权重图分布弥散、轮廓模糊，说明此时运动信号尚不可靠；
- **Phase 2（细粒度细节精炼）**：切换到 token 级自适应稀疏计算模式，利用已建立的语义结构指导运动感知缓存。

消融实验（Table 3, Table 5）表明 $K=6$ 时全局语义结构已充分建立，继续增加 $K$ 质量收益微小但计算开销增大；$K=17$ 等效于全程 chunk-wise（FlowCache）。$K>5$ 后评估分数高度稳定，空间掩码已能准确捕捉动态 token。

### 创新总结

四个 changed slots 形成因果闭环：**帧间差异代理**提供轻量运动信号 → **token 级粒度**使决策精细化 → **加权累积策略**将运动信号转化为自适应更新频率 → **双阶段调度**确保前期结构可靠、后期运动感知有效。这一设计使得 MotionCache 在 SkyReels-V2 上以 6.28× 加速仅损失 1% VBench（slow 模式），在 MAGI-1 上以 1.64× 加速仅损失 0.01% VBench，显著优于粗粒度基线。



MotionCache 的整体推理流程遵循“粗到细”的双阶段调度范式，核心目标是在自回归视频扩散模型的去噪过程中，以 token 级粒度动态决定哪些 token 需要重新计算、哪些可以直接复用缓存的残差，从而在保持生成质量的前提下最大化计算效率。

**输入与输出**：系统接收文本条件 $c$ 和初始噪声，逐 chunk 生成视频帧。每个自回归 chunk 内部包含 $F$ 帧，经历 $T$ 个去噪时间步。对于当前 chunk $i$ 在时间步 $t$ 的隐变量 $\mathbf{X}_t^{(i)}$，模型需要计算速度场 $v_\theta$ 以推进去噪过程。

**核心模块与数据流**：整个框架由五个关键模块串联构成：

1. **运动感知重要性计算**（Section 5.1）：在时间步 $t$，利用相邻帧之间的 token 级 L1 差异构建重要性地图 $\mathcal{M}_t$。其理论基础来自 Lemma 4.2——帧间差异是残差时间不稳定性的有效上界代理，因此可以轻量地替代真实残差差异来评估各 token 的更新紧迫程度。该代理的保真度经 NDCG 验证始终高于 0.94（Figure 3）。

2. **软映射与归一化**（Section 5.1）：对逐帧的重要性地图进行 min-max 归一化后，线性投影到 $[\alpha, 1]$ 区间，得到运动权重 $\mathcal{W}_t$。底数 $\alpha \in (0,1)$ 确保静态区域仍保持最低更新频率，避免完全停滞导致的误差累积。

3. **重要性加权累积**（Section 5.2）：每个 token 维护一个误差累加器 $\mathcal{A}_t[p]$，在每个时间步累加由运动权重 $\mathcal{W}_t[p]$ 加权的 chunk 整体更新幅度。该设计将时间维度的去噪进展与空间维度的运动动态耦合起来。

4. **Token 选择掩码生成**（Section 5.2）：当累加器 $\mathcal{A}_t[p]$ 超过阈值 $\tau$ 时，对应 token 被标记为“活跃”，需要执行前向计算；否则直接从缓存中读取残差，跳过计算。该掩码决定了每个时间步的实际计算量。

5. **双阶段推理调度器**（Section 5.3）：控制整体推理从粗粒度到细粒度的切换。第一阶段（预热阶段，前 $K$ 步）强制所有 token 全量更新，以建立全局语义结构和空间布局；第二阶段切换至 token 级自适应稀疏计算模式，仅对运动活跃区域进行精细去噪。Figure 6 展示了去噪过程中重要性权重图从模糊到锐利的演化，验证了该调度策略的合理性。

**与传统方案的对比**：与 TeaCache（timestep 级统一跳过）和 FlowCache（chunk 级统一跳过）不同，MotionCache 的缓存决策下沉到单个 token 层面（Figure 4）。粗粒度方法在同一 chunk 内对所有 token 执行“全算或全跳”的二元决策，忽略了帧间运动差异导致的不均匀冗余分布（Figure 2），而 MotionCache 的 token 级自适应选择能够精准匹配动态区域的更新需求，同时大幅减少静态背景的冗余计算。

### 补充图表

![[assets/figures/papers/paper_list_l58_https_arxiv_org_abs_2605_01725v1/figures/004_Figure_4.jpg]]
*Figure 4: Comparison of caching strategies in autoregressive video generation. The top panel illustrates traditional reuse strategies (e.g., TeaCache and FlowCache), which apply coarse-grained caching policies by treating an entire timestep or chunk as an atomic unit for skipping. This approach overlooks fine-grained intra-chunk redundancy, forcing a binary decision between full computation or full reuse. In contrast, our MotionCache (bottom panel) employs a fine-grained Motion-Aware caching policy, dynamically deciding for each individual token whether to reuse cached residuals or perform recomputation based on motion dynamics. The bottom right panel details the Inner Chunk Tokenwise Calculation mec...*



### 问题形式化与缓存误差分析

自回归视频生成模型在去噪过程中，每个时间步 $t$ 对每个 chunk $i$ 计算速度场 $v_\theta$，并通过 Euler 更新进行逆向去噪。现有缓存方法（如 **TeaCache** 和 **FlowCache**）通过复用先前时间步的残差来近似当前速度场：

$$ \tilde{v}_{t-1}^{i} \approx \mathbf{X}_{t-1}^{i} + \mathcal{R}_{t}^{i} \tag{6} $$

其中 $\mathcal{R}_{t}^{i} = v_\theta(\mathbf{X}_t^i, t, c) \cdot \Delta t$ 为缓存的残差。该近似引入的局部误差为：

$$ \epsilon_{t-1}^{i} = \Delta t \cdot \| \mathcal{R}_{t-1}^{i} - \mathcal{R}_{t}^{i} \|_2 \tag{7} $$

**Proposition 4.1** 表明，缓存误差严格正比于相邻时间步残差之差的 $L_2$ 范数，即缓存可靠性由残差的时间不稳定性决定。

### 运动代理的理论基础

为轻量地估计残差不稳定性，**Lemma 4.2** 建立了残差差异与帧间差异之间的理论联系：

$$ \| \mathcal{R}_{t-1}(\mathbf{X}_{t-1}^{(i,f)}) - \mathcal{R}_{t}(\mathbf{X}_{t}^{(i,f)}) \|_2 \lesssim C \cdot \| \mathbf{X}_{t}^{(i,f)} - \mathbf{X}_{t}^{(i,f-1)} \|_2 \tag{8} $$

该引理证明，残差的时间不稳定性被帧间差异所界定，帧间差是残差不稳定性的有效上界代理。这一结论构成了 MotionCache 使用帧间差作为运动感知代理的理论基础。

**实证验证**：如 Figure 3 所示，基于帧间差的 token 重要性排序与真实残差排序的 NDCG 分数始终高于 0.94，证实了运动代理的高保真度。

### 运动感知重要性计算

基于上述理论，MotionCache 定义 token 级运动重要性地图 $\mathcal{M}_t^{(i,f)} \in \mathbb{R}^{F \times H \times W}$：

$$ \mathcal{M}_{t}^{(i,f)} = \begin{cases} \|\mathbf{X}_{t+1}^{(i,f)} - \mathbf{X}_{t+1}^{(i,f-1)}\|_1 & \text{if } f > 0, \\ \|\mathbf{X}_{t+1}^{(i,0)} - \mathbf{X}_{t+1}^{(i-1,F-1)}\|_1 & \text{if } f = 0 \text{ and } i > 0, \\ \mathcal{M}_{t}^{(0,1)} & \text{if } f = 0 \text{ and } i = 0. \end{cases} \tag{9} $$

该公式对 chunk 内相邻帧之间、跨 chunk 边界帧之间以及初始帧分别处理，以 $L_1$ 距离度量 token 级别的运动强度。

### 软映射与权重调制

为将运动重要性转化为缓存调制的权重系数，MotionCache 采用逐帧 min-max 归一化后线性投影到 $[\alpha, 1]$ 区间：

$$ \mathcal{W}_{t}^{(i,f)} = \alpha + (1 - \alpha) \cdot \frac{\mathcal{M}_{t}^{(i,f)} - \min(\mathcal{M}_{t}^{(i,f)})}{\max(\mathcal{M}_{t}^{(i,f)}) - \min(\mathcal{M}_{t}^{(i,f)}) + \epsilon} \tag{10} $$

其中 $\alpha \in [0, 1]$ 为软映射底数，控制静态区域的最低更新频率。消融实验（Table 2, Table 4）表明 $\alpha = 0.6$ 在质量与效率之间取得最优平衡：$\alpha$ 过小导致静态区域退化，$\alpha = 1$ 则退化为 FlowCache 的均匀策略。

### 重要性加权累积与 Token 选择

MotionCache 的核心调度机制是运动权重加权的误差累积策略。每个 token 维护一个累积器 $\mathcal{A}_t[p]$，在每个时间步更新：

$$ \mathcal{A}_{t}[p] = \mathcal{A}_{t+1}[p] + \mathcal{W}_{t}[p] \cdot \Delta_{chunk}(t) \tag{12} $$

其中 $\Delta_{chunk}(t)$ 为 chunk 整体的更新幅度。累积误差超过阈值 $\tau$ 的 token 被选中进行前向计算：

$$ \mathrm{Mask}_{t}[p] = \mathbb{I}(\mathcal{A}_{t}[p] > \tau) \tag{13} $$

该机制实现了 token 级别的自适应缓存调度：运动剧烈的 token 因权重高而累积更快，触发更频繁的更新；静态 token 权重接近 $\alpha$，累积缓慢，倾向于复用缓存残差。

### 粗到细双阶段推理调度

MotionCache 采用两阶段推理调度（Figure 6, Section 5.3）：

![[assets/figures/papers/paper_list_l58_https_arxiv_org_abs_2605_01725v1/figures/011_Figure_6.jpg]]
*Figure 6: Visualization of the importance weight maps W throughout the denoising process. The label t indicates the denoising timestep. The leftmost column displays the final ground-truth video frames. In the early inference stages, the weight distribution remains diffuse and unstructured with ambiguous contours, indicating that the global semantic structure is not yet clearly established. As generation proceeds, the maps sharpen to accurately capture motion dynamics*

- **Phase 1（粗粒度结构建立）**：前 $K$ 个时间步强制 chunk 级全更新，确保全局语义结构充分建立。消融实验（Table 3, Table 5）表明 $K = 6$ 时结构已足够清晰，继续增加 $K$ 质量收益微小但计算开销增大。
- **Phase 2（细粒度细节精化）**：剩余时间步切换到 token 级稀疏计算模式，仅对 $\mathrm{Mask}_t[p] = 1$ 的活跃 token 执行前向计算，其余 token 从缓存中读取残差。

Figure 6 可视化了去噪过程中重要性权重图 $\mathcal{W}$ 的演化：早期权重分布弥散且无结构，随着推理推进逐渐锐化，准确捕捉运动动态，验证了粗到细调度的必要性。

### 补充图表

![[assets/figures/papers/paper_list_l58_https_arxiv_org_abs_2605_01725v1/figures/002_Figure_2.jpg]]
*Figure 2: (a) Heterogeneous Temporal Redundancy: The distribution of residual differences between adjacent timesteps exhibits a long-tailed pattern. While the majority of tokens cluster around low values, a significant tail extends to high values, indicating highly non-uniform update requirements across tokens. (b) Intra-Chunk Frame Discrepancy: The distribution of residual changes across distinct frames within the same chunk reveals significant variation. This wide dynamic range confirms that frames within a single autoregressive chunk possess distinct motion characteristics, rendering coarse-grained cache suboptimal*

![[assets/figures/papers/paper_list_l58_https_arxiv_org_abs_2605_01725v1/figures/003_Figure_3.jpg]]
*Figure 3: Validation of Motion Proxy. NDCG [15, 35] scores comparing frame difference-based token importance rankings to rankings derived from adjacent timestep residual differences. The scores remain consistently above 0.94, demonstrating strong similarity in token importance ordering throughout the diffusion process*

![[assets/figures/papers/paper_list_l58_https_arxiv_org_abs_2605_01725v1/figures/005_Figure_5.jpg]]
*Figure 5: Visualization of the ground-truth video frames versus the computed importance maps. The label f indicates the frame index within the video sequence*



## 实验与关键发现

### 主要结果：效率-质量权衡

MotionCache在两个主流自回归视频生成模型上，与无缓存基线（Vanilla）及两种粗粒度缓存方法（TeaCache、FlowCache）进行了系统对比。所有实验在NVIDIA A800 80GB GPU上执行，FlowCache和TeaCache均采用其推荐的slow/fast配置，全局预热步数m遵循FlowCache设置以保证对比公平。

**SkyReels-V2（540p, 2 chunks, 97帧）**

| 配置 | 加速比 | VBench | PSNR | SSIM | LPIPS |
|------|--------|--------|------|------|-------|
| Vanilla | 1× | 83.84% | 1 (相对) | 1 | 1 |
| MotionCache-slow | **6.28×** | 82.84% | 23.46 | 0.9093 | 0.0875 |
| MotionCache-fast | **7.26×** | 82.75% | — | — | — |

MotionCache-slow在6.28倍加速下，VBench仅下降1.00%，PSNR达23.46；fast模式进一步将加速比推至7.26倍，VBench仍维持82.75%。相比之下，TeaCache-fast和FlowCache-fast在同等加速水平下VBench分别骤降至68.81%和73.42%（Table 1），表明粗粒度统一跳过策略在激进加速时会导致严重的纹理细节丢失或结构不一致（Figure 7定性对比印证了这一结论）。

![[assets/figures/papers/paper_list_l58_https_arxiv_org_abs_2605_01725v1/figures/006_Table_1.jpg]]
*Table 1: Quantitative comparison with state-of-the-art acceleration methods on SkyReels-V2 and MAGI-1. "Slow" and "Fast" denote configurations with lower and higher acceleration ratios, respectively. MotionCache achieves superior speedups while maintaining higher generation quality compared to other baselines*

**MAGI-1（720p, 7 chunks, 24帧）**

| 配置 | 加速比 | VBench | PSNR | SSIM | LPIPS |
|------|--------|--------|------|------|-------|
| Vanilla | 1× | 77.26% | 1 (相对) | 1 | 1 |
| MotionCache-slow | **1.64×** | 77.25% | 19.71 | 0.7231 | 0.2510 |
| MotionCache-fast | **2.07×** | 74.59% | — | — | — |

在MAGI-1上，slow模式以1.64倍加速实现几乎无损的VBench（仅降0.01%）；fast模式2.07倍加速下VBench为74.59%，仍显著优于TeaCache-fast的68.81%和FlowCache-fast的73.42%（Table 1）。MAGI-1的加速比低于SkyReels-V2，这是因为其chunk数更多（7 vs 2），帧间运动模式更复杂，token级自适应缓存的空间相对收窄。

**关键结论**：MotionCache的核心优势在于token级运动感知调度——动态区域保持高频更新以维持时序一致性，静态背景以接近底数α的频率稀疏计算，从而在同等加速比下实现显著更优的质量保持。

---

### 消融实验：超参数敏感性

**软映射底数α**（Table 2, Table 4）

α控制静态背景token的最低更新权重。消融扫描α∈[0.0, 1.0]，步长0.1：

- **α=0.6**在PSNR/SSIM/LPIPS上取得最优质量-效率平衡。过小的α（如0.0-0.3）导致静态区域更新频率过低，纹理退化明显；α=1.0退化为所有token等权重的FlowCache策略，加速比提升但质量下降。
- α>0.5后性能趋于稳定（Table 4, Appendix D.1），表明静态背景的基本更新频率已足够，继续增大α仅增加计算开销而无显著质量收益。

![[assets/figures/papers/paper_list_l58_https_arxiv_org_abs_2605_01725v1/figures/009_Table_4.jpg]]
*Table 4: Detailed ablation study on the soft-mapping floor parameter α. The sweep ranges from 0.0 to 1.0 with a step of 0.1*

**预热步数K**（Table 3, Table 5）

K控制第一阶段chunk级全更新的持续步数，用于建立全局语义结构。消融扫描K∈[0, 17]，间隔1：

- **K=6**时全局语义结构已充分建立，空间掩码能准确捕捉动态token。继续增加K（如K>5后评估分数高度稳定，Table 5, Appendix D.2），质量收益微小但计算开销线性增长。
- K=17等效于全程chunk-wise策略（即FlowCache），验证了粗到细双阶段调度的必要性：前期粗粒度结构建立与后期细粒度运动感知缓存缺一不可。

![[assets/figures/papers/paper_list_l58_https_arxiv_org_abs_2605_01725v1/figures/010_Table_5.jpg]]
*Table 5: Detailed ablation study on the duration of Phase 1 (K). The sweep ranges from 0 to 17 with an interval of 1*

---

### 失败模式与局限性

1. **超参数需手动设定**：α、K和阈值τ需要为每个模型和分辨率单独调试，缺乏自适应机制。这限制了MotionCache在新模型上的即插即用能力。

2. **运动代理假设的边界**：帧间差异代理依赖运动平滑且局部线性的假设（Lemma 4.2中的Lipschitz条件）。对于剧烈遮挡、非刚性形变或相机快速移动场景，残差不稳定性上界可能被突破，导致缓存误差超出预期。当前实验未覆盖此类极端运动分布，实际部署中需注意验证。

3. **静态场景加速有限**：在低运动或静态视频中，多数token权重接近α，token级差异化调度的收益收窄，加速比提升空间有限。

4. **泛化性待验证**：当前仅在SkyReels-V2和MAGI-1两个自回归模型上验证，对其它自回归架构（如不同backbone的AR视频模型）或非自回归扩散模型的适用性未知。

---

### 重要图表结论

- **Figure 3**：帧差排序与真实残差排序的NDCG持续高于0.94，定量验证了帧间差异作为运动代理的高保真度——这是整个token级调度策略的理论基石。
- **Figure 5**：重要性地图与真实视频帧的对比可视化显示，动态区域（如人物动作、物体移动）精确对应高权重区域，静态背景对应低权重区域，直观印证了运动感知机制的准确性。
- **Figure 6**：去噪过程中权重图的演化揭示了粗到细调度的内在逻辑——早期权重分布弥散、轮廓模糊（全局结构未建立），后期权重图锐化并精确捕捉运动动态，为K=6的设定提供了视觉支撑。

### 补充图表

![[assets/figures/papers/paper_list_l58_https_arxiv_org_abs_2605_01725v1/figures/007_Table_2.jpg]]
*Table 2: Ablation study on the soft-mapping floor parameter α*

![[assets/figures/papers/paper_list_l58_https_arxiv_org_abs_2605_01725v1/figures/008_Table_3.jpg]]
*Table 3: Ablation study on the duration of Phase 1 (K)*

![[assets/figures/papers/paper_list_l58_https_arxiv_org_abs_2605_01725v1/figures/001_Figure_1.jpg]]
*Figure 1: MotionCache accelerates video generation while maintaining high visual fidelity. On SkyReels-V2 and MAGI-1, our method achieves 6.28× and 1.64× speedups with superior PSNR. In contrast, TeaCache fails to maintain texture details and FlowCache suffers from structural inconsistency, while MotionCache preserves both structural integrity and temporal coherence comparable to the Vanilla baseline*

![[assets/figures/papers/paper_list_l58_https_arxiv_org_abs_2605_01725v1/figures/012_Figure_7.jpg]]
*Figure 7: Qualitative results of text-to-video generation on SkyReels-V2. We present TeaCache, FlowCache, Motion-Cache, and the Vanilla model. The frames are randomly sampled from the generated video*



## 定位与知识库关联

### 问题定位：自回归视频生成中的缓存粒度困境

自回归视频生成模型（如SkyReels-V2、MAGI-1）将视频按chunk逐块生成，每个chunk内需经过多步去噪迭代。为降低计算开销，现有缓存方法采用粗粒度统一跳过策略：

- **TeaCache**：在timestep级别判断是否跳过整个去噪步，对所有token执行全计算或全复用。该方法无法感知同一timestep内不同空间位置的运动差异，在动态区域容易累积误差。
- **FlowCache**（Anonymous, ICLR 2025 under review）：将缓存粒度提升至chunk级别，在chunk内统一复用残差。然而，同一chunk内不同帧的运动特征差异显著（帧间最大差异可达5.9219，见Figure 2b），粗粒度策略迫使动态区域与静态区域接受相同的更新频率，导致动态区域误差累积或静态区域计算浪费。

**核心瓶颈**：现有缓存方法忽略同一chunk内不同token的运动差异，缺乏token级别的自适应调度能力。

### MotionCache的方法定位

MotionCache在缓存粒度、运动感知、误差累积和推理调度四个维度上对现有方法进行了系统性改进：

| 设计维度 | 基线方法 | MotionCache | 证据锚点 |
|---------|---------|-------------|---------|
| 缓存粒度 | chunk-wise或timestep-wise统一跳过 | token-wise自适应选择 | Figure 4, Section 5.2 |
| 运动感知代理 | 无（仅基于全局L1变化） | 帧间差异作为token运动重要性 | Equation (9), Section 5.1 |
| 误差累积策略 | 全局相对L1距离阈值 | 运动权重加权累积与token级阈值决策 | Equation (12)-(13), Section 5.2 |
| 推理调度 | 全程统一策略 | 粗到细双阶段：先chunk级预热后token级细化 | Section 5.3, Figure 6 |

**理论创新**：MotionCache首次将缓存误差与运动动力学建立了严格的理论联系。Proposition 4.1证明了缓存误差严格正比于相邻时间步残差之差的L2范数（$\epsilon_{t-1}^{i} = \Delta t \cdot \| \mathcal{R}_{t-1}^{i} - \mathcal{R}_{t}^{i} \|_2$），从而将缓存可靠性问题转化为残差时间不稳定性问题。Lemma 4.2进一步证明残差差异被帧间差异所界定（$\| \mathcal{R}_{t-1} - \mathcal{R}_{t} \|_2 \lesssim C \cdot \| \mathbf{X}_{t}^{(i,f)} - \mathbf{X}_{t}^{(i,f-1)} \|_2$），为使用轻量帧差作为运动代理提供了理论保证。实验验证该代理与真实残差排序的NDCG＞0.94（Figure 3），表明帧差能高保真地反映token级更新需求。

**工程实现**：MotionCache将理论洞察落地为五个模块化组件：运动感知重要性计算（Equation 9）、软映射与归一化（Equation 10，将重要性线性投影到[α,1]）、重要性加权累积（Equation 12-13）、双阶段推理调度器（Phase 1: K步chunk级全更新建立全局语义结构；Phase 2: token级稀疏计算精细化动态细节）、以及残差缓存与KV缓存管理。

### 适用边界与泛化性分析

**已验证的适用场景**：
- 自回归视频生成架构（SkyReels-V2 540p 97帧、MAGI-1 720p 24帧）
- 包含显著运动动态的视频内容（动态区域token获得更高更新频率）
- Flow Matching类扩散模型的去噪推理

**潜在的泛化边界**：
- 方法仅在两个自回归模型上验证，对其他自回归架构（如基于AR transformer的视频生成器）或非自回归扩散模型（如全序列扩散模型）的泛化性未知
- 帧间差异代理假设运动平滑且局部线性，对于剧烈遮挡、非刚性形变或相机快速移动可能失效
- 在静态场景或低运动视频中，多数token权重接近α，加速比提升空间有限

### 局限与开放问题

**已知局限**（论文明确指出的）：
1. **超参数手动调节**：α（软映射底数）、K（预热步数）、τ（累积阈值）需为每个模型和分辨率手动设置，缺乏自适应性
2. **运动代理的边界条件**：Lemma 4.2中的Lipschitz常数C在实际中难以精确估计，且在不同视频域中的稳定性未经验证
3. **评估范围受限**：仅在SkyReels-V2和MAGI-1两个模型上验证

**开放问题**（值得后续探索的方向）：
1. **自适应阈值机制**：能否设计自动或自适应机制来选择τ及超参数α和K？例如基于视频内容复杂度动态调整缓存策略
2. **跨架构扩展**：该方法能否扩展到非自回归的全序列扩散视频生成模型？核心挑战在于非自回归模型缺乏chunk边界，帧间差异的定义需要重新设计
3. **运动代理的鲁棒性边界**：对于极快速运动或细粒度纹理变化，帧差代理的保真度是否仍能维持NDCG＞0.94？可能需要引入光流或更精细的运动表征
4. **层级联合缓存**：结合layer-level缓存（如TeaCache的特征复用）与token-wise策略是否能获得额外加速？这涉及不同层级误差传播的耦合分析
5. **常数C的估计**：Lemma 4.2中的Lipschitz常数C在不同视频域中是否保持稳定？能否通过轻量在线估计来提升运动代理的精度？

### 知识库定位

MotionCache属于**扩散模型推理加速**与**视频生成效率优化**的交叉领域，具体定位于：

- **缓存策略谱系**：从粗粒度（TeaCache timestep级、FlowCache chunk级）向细粒度（token级自适应）的演进
- **运动感知推理**：首次将运动动力学引入缓存调度决策，区别于纯基于误差阈值的传统方法
- **理论驱动的系统设计**：从残差稳定性分析出发推导运动代理，而非纯经验性设计

该方法为自回归视频生成的实用化部署提供了关键加速能力（SkyReels-V2上6.28×加速仅损失1% VBench），同时为后续研究开辟了运动感知缓存的理论框架和工程基线。



## 原文 PDF

![[paperPDFs/arxiv_2026/Motion_Aware_Caching_for_Efficient_Autoregressive_Video_Generation.pdf]]
