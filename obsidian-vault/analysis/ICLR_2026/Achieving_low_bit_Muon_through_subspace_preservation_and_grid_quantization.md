---
title: "Achieving low-bit Muon through subspace preservation and grid quantization"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/Achieving_low_bit_Muon_through_subspace_preservation_and_grid_quantization.pdf
project_link: null
code_link: https://github.com/wuhuaijin/lowbit-Muon
aliases:
- 4BMGGSP
- ALBMTSPGQ
tags:
- ICLR_2026
- topic/generative_models_diffusion
- topic/generative_models_diffusion/algorithms
core_operator: "将矩矩阵分解为顶部奇异子空间（使用8比特温和压缩）和残差奇异子空间（使用4比特积极压缩），并引入网格量化对双向离群值进行精细化归一化。"
primary_logic: "NS迭代对量化误差的放大主要集中在顶部奇异子空间；通过对矩矩阵进行SVD分解，对顶部奇异向量采用保留精度的8比特量化，对残差部分采用4比特量化，并利用网格量化（行、列双向归一化）为每个元素提供独立量化尺度，从而在显著减少内存的同时保持与全精度优化器相当的收敛性能。"
claims:
- "NS迭代将量化误差放大，且放大主要集中在上部奇异子空间（k=64时，顶部误差从0.08增至3.31，放大40倍；残差误差仅从0.09增至0.47，放大5倍）"
- "采用子空间保持与网格量化的4-bit-Muon-GRASP可将量化误差从1.78降至0.14，并达到与全精度Muon相当的预训练验证困惑度和下游任务准确率"
- "LLaMA-350M 预训练下游任务平均准确率 上 Avg accuracy (HellaSwag, ARC-c, ARC-e, boolQ, OBQA, PIQA, S... = 44.5 (4-bit-Muon-GRASP)"
- "LLaMA-1.1B 预训练验证困惑度 上 Validation PPL after 10K steps = 12.48 (4-bit-Muon-GRASP)"
---

# Achieving low-bit Muon through subspace preservation and grid quantization

> [!tip] 核心洞察
> NS迭代对量化误差的放大主要集中在顶部奇异子空间；通过对矩矩阵进行SVD分解，对顶部奇异向量采用保留精度的8比特量化，对残差部分采用4比特量化，并利用网格量化（行、列双向归一化）为每个元素提供独立量化尺度，从而在显著减少内存的同时保持与全精度优化器相当的收敛性能。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 通过子空间保持与网格量化实现低比特Muon优化器 |
| 英文题名 | Achieving low-bit Muon through subspace preservation and grid quantization |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=g2l9bg9DWx) · [GitHub](https://github.com/wuhuaijin/lowbit-Muon) |
| Topic | #topic/generative_models_diffusion #topic/generative_models_diffusion/algorithms |
| Method | 4-bit-Muon-GRASP (GRid And Subspace Preserving) |
| Dataset | LLaMA-350M 预训练下游任务平均准确率, LLaMA-1.1B 预训练验证困惑度, Qwen2.5-7B-Math 微调数学推理任务, 训练内存总占用量 (1.1B 模型) |

> [!tip] 效果简介
> - LLaMA-350M 预训练下游任务平均准确率 上，Avg accuracy (HellaSwag, ARC-c, ARC-e, boolQ, OBQA, PIQA, SciQ) 为 44.5 (4-bit-Muon-GRASP)，对比 44.6 (fp32-Muon)，变化 -0.1。
> - LLaMA-1.1B 预训练验证困惑度 上，Validation PPL after 10K steps 为 12.48 (4-bit-Muon-GRASP)，对比 12.48 (fp32-Muon)，变化 0.00。
> - Qwen2.5-7B-Math 微调数学推理任务 上，Average score (MATH, Minerva Math, Olympiad Bench) 为 62.8 (SFT 4bit-GRASP)，对比 62.6 (SFT fp32)，变化 +0.2。

## 概要

大语言模型训练中，优化器状态通常以32位浮点精度存储，成为内存开销的主要来源之一。Muon优化器通过牛顿-舒尔茨（NS）正交化对矩矩阵进行处理，在多种任务上取得了优于传统Adam的收敛表现，但这一过程对矩矩阵的数值扰动极为敏感：直接对矩矩阵进行低位宽量化（如4比特）会使量化误差在NS迭代后被急剧放大，尤其是顶部奇异子空间的误差被放大约40倍，导致训练性能严重退化。因此，如何在保持正交化更新质量的前提下压缩优化器状态，是一个关键瓶颈。

针对该问题，本文提出**4-bit-Muon-GRASP（GRid And Subspace Preserving）**方法。其核心思路是：将动量矩矩阵分解为顶部奇异子空间与残差奇异子空间，并分别采用不同粒度的压缩——对误差敏感的顶部奇异向量做温和的8比特量化以保留关键方向，对残差部分做积极的4比特量化以减少内存；同时引入网格量化，对每个元素沿行、列双向独立归一化，以精确应对矩矩阵中存在的双向离群值模式。该方法实现了优化器状态的低比特压缩，并将NS迭代后整体量化误差从直接量化的1.78降至0.14。

实验表明，4-bit-Muon-GRASP在不同规模的预训练与微调场景下均能匹配全精度Muon的性能：在LLaMA‑350M预训练中，七个零样本下游任务的平均准确率仅相差0.1%（44.5 vs 44.6）；在1.1B模型上，验证困惑度持平（12.48），同时总训练内存从13.22 GB降至10.14 GB（节省约23.3%）；在Qwen2.5‑7B‑Math的监督微调中，数学推理平均得分甚至略优于全精度基线（62.8 vs 62.6）。这些结果表明，通过子空间保持与网格量化的协同设计，可以在显著降低内存开销的同时，几乎无损地保留Muon优化器的收敛特性，为低比特优化器在大规模训练中的部署提供了可行路径。



在大规模深度学习模型训练中，优化器状态的内存占用已成为限制可训练模型规模的关键瓶颈之一。Muon优化器（基于动量与牛顿-舒尔茨正交化的更新规则）因其良好的收敛特性受到关注，但其需要为每个可训练参数维护一个与其形状相同的动量矩矩阵 $\mathbf{M}_t$（见 Eq. (1)：

$$
\mathbf{M}_t = \mu \mathbf{M}_{t-1} + \nabla \mathcal{L}_t(\mathbf{W}_{t-1})
$$

）随后须通过牛顿-舒尔茨 (NS) 迭代进行正交化（Eq. (2)），以得到更新方向 $\mathbf{O}_t$。该矩矩阵通常以全精度（32 位浮点数）存储，导致优化器内存开销达到模型参数量的 2 倍（含动量和矩），严重制约了大型模型的训练效率与规模。

为降低内存压力，直接对矩矩阵进行低比特量化是一种自然的扩展思路。然而，直接将 $\mathbf{M}_t$ 量化到 4 比特的朴素方案（4-bit-Muon-base）在训练中损失严重，其核心原因并非量化本身精度不足，而在于后续的 **牛顿-舒尔茨迭代会显著放大量化误差**。如表 1（Table 1）所示，对于顶部 k 个奇异向量构成的子空间近似 $\mathbf{M}_{\mathrm{top}}$，4 比特量化在 NS 迭代前的相对误差仅为 0.08，经 NS 迭代后则急剧增至 3.31，**误差放大达 40 倍**；而对于残差子空间 $\mathbf{M}_{\mathrm{res}}$，同样的量化在 NS 迭代后误差仅从 0.09 增至 0.47，放大倍数仅约 5 倍。这一现象表明，**NS 迭代对量化误差的放大效应主要集中于矩矩阵的顶部奇异子空间**，而残差子空间的误差放大则相对温和。同时，图 1（Figure 1）的可视化也直观显示，NS 迭代后全精度与量化版本的分布及奇异值出现严重偏离，进一步验证了朴素 4 比特量化的不可行性。值得注意的是，即使增加 NS 迭代次数或提升多项式阶数，也无法弥合这一误差间隙（见 Figure 2），说明问题并非源于迭代不足，而是量化误差通过 NS 迭代在顶部方向上被结构性放大。

针对上述瓶颈，本文的核心动机是：**通过量化前对矩矩阵进行低秩分解，对误差敏感度截然不同的子空间采取差异化压缩策略**，即对顶部奇异子空间采用较温和的 8 比特压缩以保持其主要结构，对残差子空间则采用更激进的 4 比特压缩以最大化内存节省。同时，针对矩矩阵中普遍存在的双向（行向和列向）离群值模式（见 Figure 3 左），引入**网格量化**，通过行列双向归一化为每个元素提供独立的量化尺度，进一步抑制残差量化引入的噪声。该方案的预期效果是：将量化误差从朴素 4 比特的 1.78 降至约 0.14（见 Section 3），从而在取得约 28% 训练内存降低的同时，达到与全精度 Muon 相当的预训练验证困惑度与下游任务准确率（详细结果见 Table 2、Table 3 及 Figure 5）。



## 核心方法与创新机理

全精度 Muon 优化器的核心瓶颈在于：其牛顿‑舒尔茨（NS）正交化迭代会急剧放大矩矩阵中的量化误差，而这种放大主要集中于顶部奇异子空间。直接对整个矩矩阵做 4‑比特分组量化（4‑bit‑Muon‑base）会严重损害训练后的模型性能，因为 NS 迭代会将顶部奇异子空间的扰动放大约 40 倍，而残差子空间的放大仅为 5 倍（Table 1）。这一发现直接催生了**“子空间保持 + 网格量化”**的双轨压缩策略，构成 4‑bit‑Muon‑GRASP 的两项关键创新。

**1. 带状子空间分解与差异化精度分配**  
与基线中全体张量统一量化的做法不同，该方法将矩矩阵 `M_t` 显式分解为顶部奇异子空间和残差子空间：
- 通过热启动的幂迭代（每步仅一次迭代）近似得到前 `k` 个奇异向量 `P_t, R_t`，形成低秩近似 `M_top ≈ P_t R_t^T`；
- 计算残差 `M_res = M_t - P_t R_t^T`。
对这两个部分采用**差异化比特宽度**：顶部奇异子空间使用相对温和的 8‑比特量化以保持高信噪比，而残差部分则进行高度压缩的 4‑比特量化。这一改变直接改变了“矩矩阵量化比特宽度”槽位——从原先 32/8 比特整体压缩，变为“顶部 8‑比特 + 残差 4‑比特”的组合方案。存储时仅保留 8‑比特的 `P_t, R_t` 以及 4‑比特的 `M_res`，大幅降低了优化器状态的内存占用。

**2. 网格量化（Grid Quantization）实现逐元素独立尺度**  
以往的分组量化（如 per‑token、per‑channel）采用单一的归一组尺度，无法应对矩矩阵中同时沿行、列出现的双向离群值。网格量化改变了“量化粒度与归一化方式”这一关键槽位：对每个元素 `x_{i,j}`，同时计算其所在行和列的统计尺度，并以两者中的较小值进行归一化：

$$
\mathcal{N}_{\text{grid}}(x_{i,j}) = \frac{x_{i,j}}{\min(\text{scale}_{r_i}, \text{scale}_{c_j})}
$$

这使得每个元素都获得一张**单独的量表**，有效抑制跨维度离群值对低比特表示的破坏。消融实验（Figure 7(b)）证实，网格量化将 4‑比特量化带来的训练损失差距缩小为普通分组量化的一半。

**效果与证据**  
将上述两项创新叠加后，矩矩阵的量化相对误差从直接 4‑比特量化的 1.78 降至 0.14，且 NS 迭代后的重建质量与全精度实现高度吻合（Figure 4）。在 LLaMA‑350M 预训练的下游任务平均准确率上，4‑bit‑Muon‑GRASP 仅比全精度 Muon 低 0.1 个百分点（44.5 vs 44.6，Table 2）；在 LLaMA‑1.1B 上，验证困惑度与全精度持平（12.48 vs 12.48），同时总训练内存从 13.22 GB 降至 10.14 GB，节省约 23.3%（Table 3）。在 Qwen2.5‑7B‑Math 的微调中，4‑bit‑GRASP 的平均任务得分甚至略超全精度基线（62.8 vs 62.6，Table 4）。这些结果表明，通过精确保持顶部子空间并采用细粒度网格量化，可以在将优化器状态压缩到 4 比特的同时，几乎零损失地复现全精度 Muon 的收敛行为。



4‑bit‑Muon‑GRASP 的整体流程建立在 Muon 优化器的标准两步结构上：先利用指数移动平均构建动量矩矩阵 $\mathbf{M}_t$，再通过牛顿‑舒尔茨 (Newton‑Schulz, NS) 正交化得到参数更新方向。本文提出的低比特压缩方案在矩矩阵进入 NS 迭代之前插入**子空间保持 (subspace preserving)** 与**网格量化 (grid quantization)** 两个关键模块，构成一条完整的量化优化器 pipeline。

具体而言，每个优化步骤的执行顺序为（对应 Algorithm 1）：

1. **动量更新**  
   由当前梯度 $\nabla\mathcal{L}_t$ 和上一步动量 $\mathbf{M}_{t-1}$ 计算全精度矩矩阵  
   $\mathbf{M}_t = \mu \mathbf{M}_{t-1} + \nabla\mathcal{L}_t(\mathbf{W}_{t-1})$（式 1）。此阶段产生的矩矩阵仍保持 32‑bit 浮点，不做压缩。

2. **幂迭代获取顶部奇异子空间**  
   利用上一步的右奇异向量作为**热启动**，仅执行单步幂迭代（Section 3.2）近似获得 $\mathbf{M}_t$ 的前 $k$ 个奇异向量，分别记作 $\mathbf{P}_t \in \mathbb{R}^{m\times k}$ 和 $\mathbf{R}_t \in \mathbb{R}^{n\times k}$，使得  
   $\mathbf{P}_t \mathbf{R}_t^\top \approx \mathbf{M}_{\text{top}}$（式 11）。  
   这一步不显式构造完整的 SVD，计算开销可控，且 $k$ 通常远小于矩阵维度（如实验选取 $k = r/16$）。

3. **子空间分解与残差计算**  
   从原始矩矩阵中减去顶部子空间近似，得到残差矩阵  
   $\mathbf{M}_{\text{res}} = \mathbf{M}_t - \mathbf{P}_t \mathbf{R}_t^\top$（式 10）。  
   设计动机源于 **Table 1** 的量化误差分析：NS 迭代对顶部奇异子空间的量化误差放大可达 40 倍（RE 从 0.08 升至 3.31），而对残差子空间的放大仅约 5 倍（RE 从 0.09 升至 0.47）。因此需对两部分采取**差异化压缩策略**。

4. **网格量化与反量化**  
   - **顶部子空间保留**：对 $\mathbf{P}_t, \mathbf{R}_t$ 使用**8‑bit 温和量化和反量化**，以保持其精度。  
   - **残差子空间压缩**：对 $\mathbf{M}_{\text{res}}$ 采用**4‑bit 网格量化**（Section 3.3）。网格量化为每个元素计算独立量化尺度：  
     $\mathcal{N}_{\text{grid}}(x_{i,j}) = \frac{x_{i,j}}{\min(\text{scale}_{r_i}, \text{scale}_{c_j})}$，  
     其中 $\text{scale}_{r_i}, \text{scale}_{c_j}$ 分别为所在行、列的范数界，有效抑制了 Figure 3 所示的双向离群值模式。  
   量化后的 $\mathbf{P}_t, \mathbf{R}_t$（8‑bit）和 $\mathbf{M}_{\text{res}}$（4‑bit）存入优化器缓冲区，占用远小于 32‑bit 全精度的内存。需要时通过反量化重建近似矩矩阵 $\widetilde{\mathbf{M}}_t = \mathbf{P}_t\mathbf{R}_t^\top + \mathbf{M}_{\text{res}}$。

5. **牛顿‑舒尔茨正交化**  
   对重建的 $\widetilde{\mathbf{M}}_t$ 执行 $p$ 次 NS 迭代（式 2、4），得到近似正交的更新方向 $\mathbf{O}_t$。由于保留了顶部奇异子空间并精细量化残差，量化误差在 NS 迭代中被大幅抑制（NE 从 1.78 降至 0.14）。

6. **权重更新**  
   利用正交化更新和当前学习率 $\eta_t$ 更新模型参数：  
   $\mathbf{W}_t = \mathbf{W}_{t-1} - \eta_t \mathbf{O}_t$（式 3，结合权重衰减等缩放技巧）。

整个流程的输入为当前梯度 $\nabla\mathcal{L}_t$、上一步动量 $\mathbf{M}_{t-1}$ 及上一步的右奇异向量（用于热启动），输出为更新后的参数 $\mathbf{W}_t$ 和经压缩存储的优化器状态（8‑bit $\mathbf{P}_t, \mathbf{R}_t$ 与 4‑bit $\mathbf{M}_{\text{res}}$）。这种设计将内存占用降低约 23–28%，同时使预训练困惑度和下游任务准确率与全精度 Muon 相当（Table 2、3）。



4‑bit‑Muon‑GRASP 的核心思路源于一个关键发现：牛顿‑舒尔茨（NS）正交化迭代会显著放大量化引入的数值误差，且放大作用高度集中于矩阵的顶部奇异子空间。据此，方法将动量矩矩阵分解为**顶部奇异子空间**（用 8‑bit 温和压缩）与**残差奇异子空间**（用 4‑bit 积极压缩），并引入**网格量化**来更精细地抑制由双向离群值引发的量化畸变。由此，在训练内存降低 23%–28% 的同时，将量化误差从 1.78 压至 0.14，实现与全精度 Muon 几乎一致的收敛与下游性能。

### 1. 动量矩更新与正交化

Muon 优化器首先按标准方式维护一阶矩：

$$
\mathbf{M}_t = \mu \mathbf{M}_{t-1} + \nabla \mathcal{L}_t(\mathbf{W}_{t-1})
$$

其中 $\mu$ 为动量系数，$\mathbf{M}_t$ 是当前步的动量矩矩阵。随后，Muon 对该矩阵施加牛顿‑舒尔茨迭代，得到近似正交化的更新方向：

$$
\mathbf{O}_t = \mathrm{Newton-Schulz}_p(\mathbf{M}_t, T)
$$

其中 $p$ 表示多项式阶数（默认 $p=5$），$T$ 为迭代步数。单步 NS 迭代的形式为：

$$
\mathbf{X}_k = a\mathbf{X}_{k-1} + b(\mathbf{X}_{k-1}\mathbf{X}_{k-1}^\top)\mathbf{X}_{k-1} + c(\mathbf{X}_{k-1}\mathbf{X}_{k-1}^\top)^2\mathbf{X}_{k-1}
$$

式中 $a=3.4445$，$b=-4.7750$，$c=2.0315$。正交化后的矩阵 $\mathbf{O}_t$ 最终用于权重更新 $\mathbf{W}_t = \mathbf{W}_{t-1} - \eta_t \mathbf{O}_t$。

### 2. 量化误差放大与子空间分解

直接对 $\mathbf{M}_t$ 做 4‑bit 量化会导致严重退化，因为 NS 迭代将量化引入的微小扰动急剧放大，尤其是**顶部奇异子空间**。以相对误差衡量：

$$
\operatorname{RE}(\mathbf{A}, \mathbf{B}) = \frac{\|\mathbf{A} - \mathbf{B}\|_F}{\|\mathbf{B}\|_F}
$$

实验显示，当截断秩 $k=64$ 时，顶部奇异子空间在经过 NS 迭代后的相对误差从 0.08 飙升至 3.31（放大 40×），而残差子空间的误差仅从 0.09 增加到 0.47（放大 5×），这说明误差放大的主因集中在低秩的顶部成分。

据此，算法将矩矩阵分解为：

$$
\mathbf{M}_{\mathrm{top}} := \mathbf{U}_k \Sigma_k \mathbf{V}_k^\top,\quad \mathbf{M}_{\mathrm{res}} = \mathbf{M} - \mathbf{M}_{\mathrm{top}}
$$

其中 $\mathbf{U}_k, \mathbf{V}_k$ 分别为前 $k$ 个左右奇异向量，$\Sigma_k$ 为对应的奇异值对角阵。顶部子空间用 8‑bit 保持较高精度，残差部分则允许 4‑bit 压缩，以此兼顾内存与精度。

### 3. 顶部奇异向量的高效提取

为减少额外计算开销，方法采用**单步热启动幂迭代**来近似 $\mathbf{M}_{\mathrm{top}}$：

$$
\mathbf{P}_t \mathbf{R}_t^\top \approx \mathbf{M}_{\mathrm{top}},\quad \mathbf{P}_t \in \mathbb{R}^{m\times k},\; \mathbf{R}_t \in \mathbb{R}^{n\times k}
$$

幂迭代利用上一步的右奇异向量作为热启动，仅执行一次迭代即可获得可靠的顶部奇异子空间近似。当 $k$ 较小时，幂迭代耗时远低于 NS 迭代；实际中使用 $k=r/16$（$r$ 为矩阵较小维度）实现开销与精度的合理折中。

### 4. 网格量化

动量矩矩阵中普遍存在行、列两个方向上的离群值，传统的 per‑token 或 per‑channel 分组量化无法同时处理。网格量化对每个元素沿行、列双向归一化，得到独立的量化尺度，从而更精确地约束每个数值的动态范围：

$$
\mathcal{N}_{\mathrm{grid}}(x_{i,j}) = \frac{x_{i,j}}{\min(\mathrm{scale}_{r_i}, \mathrm{scale}_{c_j})}
$$

其中 $\mathrm{scale}_{r_i}$ 和 $\mathrm{scale}_{c_j}$ 分别为矩阵第 $i$ 行和第 $j$ 列根据分组量化策略获得的尺度因子。经过该归一化后，再对 $\mathbf{P}_t, \mathbf{R}_t$ 做 8‑bit 量化，对 $\mathbf{M}_{\mathrm{res}}$ 做 4‑bit 网格量化并存储；反量化时通过上述尺度的逆操作恢复近似值，用于后续 NS 迭代。

### 5. 整体算法结构

结合上述模块，4‑bit‑Muon‑GRASP 的单步流程可概括为：

1. **动量更新**：由梯度与前一步矩计算 $\mathbf{M}_t$；
2. **幂迭代**：热启动单步幂迭代得到顶部奇异向量对 $(\mathbf{P}_t, \mathbf{R}_t)$；
3. **子空间分解**：计算残差 $\mathbf{M}_{\mathrm{res}} = \mathbf{M}_t - \mathbf{P}_t \mathbf{R}_t^\top$；
4. **量化**：以 8‑bit 存储 $\mathbf{P}_t, \mathbf{R}_t$，以 4‑bit 网格量化存储 $\mathbf{M}_{\mathrm{res}}$；
5. **反量化与 NS 迭代**：重建近似矩矩阵，执行 NS 迭代得到 $\mathbf{O}_t$，更新权重。

该流程在几乎不损失优化器收敛性能的同时，将优化器状态的高精度存储需求降低了约 75%，是低比特 Muon 压缩的关键技术路径。



## 实验与关键发现

### 1. 朴素4-bit量化为何失效：NS迭代对顶部奇异子空间的误差放大

直接对Muon的矩矩阵 $\mathbf{M}_t$ 做4-bit分组量化（4-bit-Muon-base）会严重破坏收敛精度，其根源在于牛顿-舒尔茨（NS）迭代会显著放大量化误差。**Figure 1** 展示了在 NS 迭代前后，全精度与量化后矩阵的分布及奇异值的显著偏离：迭代前相对误差 RE≈0.07，迭代后剧增至 RE≈1.78。

![[assets/figures/papers/iclr26_0006_g2l9bg9DWx_Achieving_low-bit_Muon_through_subspace_preserva/figures/004_Figure_1.jpg]]
*Figure 1: Visualization of momentum in transformer.layers.7.attn.o proj in a LLaMA model. (a) The distribution of matrix (real) and their 4-bit compressions (quant). (b) Distribution of the matrix after NS iteration (NS(real)) and its 4-bit compressions after NS iterations (NS(quant)). (c) and (d): Distribution of singular values of the matrices in (a) and (b), displayed on a $\log _ { 1 0 }$ scale*

进一步的分析表明该放大效应高度集中于顶部奇异子空间。**Table 1** 给出了不同秩 $k$ 下，顶部子空间 $\mathbf{M}_{\text{top}}$ 与残差子空间 $\mathbf{M}_{\text{res}}$ 在 NS 迭代前后的量化误差（平均值）：

![[assets/figures/papers/iclr26_0006_g2l9bg9DWx_Achieving_low-bit_Muon_through_subspace_preserva/figures/006_Table_1.jpg]]
*Table 1: Quantization error before and after NS iterations. The results represent the average values obtained across all parameters during the first 100 training iterations of the 1.1B LLaMA model*

| 子空间 | 迭代前 RE | 迭代后 RE (k=64) | 放大倍数 |
|--------|----------|------------------|---------|
| $\mathbf{M}_{\text{top}}$ | 0.08 | 3.31 | ≈40× |
| $\mathbf{M}_{\text{res}}$ | 0.09 | 0.47 | ≈5× |

残差子空间的误差放大仅约5倍，而顶部子空间被放大近40倍。这意味着 **NS 迭代将本已微小的量化扰动剧烈通胀，主导了整个矩阵的最终误差**。仅增加 NS 迭代次数或多项式阶数（**Figure 2**）并不能挽回精度，证明误差并非由迭代不充分引起。

这一发现揭示了失效的核心瓶颈：朴素对整体矩矩阵进行等比特宽度量化，没有对误差放大严重的顶部奇异子空间施加保护。因此，**4-bit-Muon-GRASP** 的设计出发点就是针对不同子空间实施差异化的量化策略。

### 2. 主结果：精度与全精度优化器持平，内存显著降低

**4-bit-Muon-GRASP** 在多项预训练与微调基准上的精度均与全精度 **fp32-Muon** 无统计显著差异，同时大幅压缩了优化器状态内存。

* **预训练下游任务（LLaMA‑350M）**：**Table 2** 显示，在 HellaSwag、ARC‑c、ARC‑e、boolQ、OBQA、PIQA、SciQ 七个基准的平均准确率上，4‑bit‑Muon‑GRASP 达到 **44.5**，而 fp32‑Muon 为 **44.6**（Δ = −0.1）。8‑bit‑Muon 平均准确率可达 **45.1**，甚至微弱超过全精度。
* **预训练验证困惑度（LLaMA‑1.1B）**：**Table 3** 中，训练10K步后的验证困惑度（PPL）均为 **12.48**，完全一致。**Figure 5** 的验证损失曲线显示 4‑bit‑Muon‑GRASP 与 fp32‑Muon 几乎完全重合，进一步证实没有可观测的精度损失。
* **监督微调数学推理（Qwen2.5‑7B‑Math）**：**Table 4** 中，4‑bit‑GRASP 的 SFT 在 MATH、Minerva Math、Olympiad Bench 三项平均分达到 **62.8**，略微高于 fp32 的 **62.6**，表明低比特优化器在微调场景下同样不损害任务表现。
* **内存节约**：**Table 3** 显示，在 1.1B 规模下，4‑bit‑Muon‑GRASP 将总训练内存从 13.22 GB 降至 **10.14 GB**（↓23.3%）。**Figure 6** 及扩展实验 **Table 7** 报告，随着模型规模增大，内存节省可达 **28%**，同时更新步时仅引入少量额外开销（**Table 6**）。

![[assets/figures/papers/iclr26_0006_g2l9bg9DWx_Achieving_low-bit_Muon_through_subspace_preserva/figures/013_Table_2.jpg]]
*Table 2: Evaluation of models pre-trained with three optimizers, across downstream tasks for different model sizes. The results are the average of multiple random seeds*

![[assets/figures/papers/iclr26_0006_g2l9bg9DWx_Achieving_low-bit_Muon_through_subspace_preserva/figures/014_Table_3.jpg]]
*Table 3: Statistics of different optimizers: the step time (s), total memory usage (GB), and validation perplexity (↓) after training for 10K steps*

![[assets/figures/papers/iclr26_0006_g2l9bg9DWx_Achieving_low-bit_Muon_through_subspace_preserva/figures/016_Table_4.jpg]]
*Table 4: Comparison of three optimizers applied to the SFT of the Qwen2.5-7B and Qwen2.5-7B-Math pretrained models*

### 3. 消融实验：子空间保持与网格量化的独立贡献

为理解两个核心组件（顶部子空间保持和网格量化）各自的作用，作者在 LLaMA 预训练上进行了系统消融（**Figure 7**）。

![[assets/figures/papers/iclr26_0006_g2l9bg9DWx_Achieving_low-bit_Muon_through_subspace_preserva/figures/019_Figure_7.jpg]]
*Figure 7: Ablation studies on pretraining: (a) Selection of different top singular space ranks, (b) Comparison of group and grid quantization, (c) Preservation of only the top singular space*

* **网格量化 vs. 分组量化**（**Figure 7(b)**）：在相同比特宽度下，网格量化能将训练损失差距缩小至朴素分组量化方法的一半左右。其内在机制是：“网格归一化”对每个元素沿行、列方向独立获得尺度，从而更精细地处理双向上出现的离群值（**Figure 3** 展示离群层模式），而非仅靠 per‑token 或 per‑channel 尺度。
* **保留顶部奇异子空间（子空间保持）**（**Figure 7(c)**）：若仅保留顶部子空间而直接丢弃残差部分，验证损失会明显劣化；保留适当的顶部子空间才是恢复全精度表现的关键。这与 Table 1 的误差分析一致：顶部子空间承载了绝大部分由 NS 迭代放大的误差，对其进行相对温和的 8‑bit 量化（而非 4‑bit）是控制全局误差的核心因果旋钮。
* **秩（$k$）的选择**（**Figure 7(a)**, **Table 9/10**）：$k$ 越大，顶部子空间保留的信息越多，精度越高，但计算与内存开销也上升。实验表明，取 $k / r = 1/16$（$r$ 为矩矩阵较小维度）实现了较好的精度‑效率折中。幂迭代的单步热启动在低秩时远快于 NS 迭代，$k$ 较大时 QR 分解成为瓶颈（**Table 8**），因此不可无限增大。
* **量化数据类型（FP4 vs. INT4）**（**Figure 9 (Left)**）：使用 FP4 与 INT4 数据格式训练时，损失曲线几乎一致，仅有轻微的效率开销差异，显示该方法对具体 low‑bit 格式不敏感。

综上，**网格式归一化**解决了双向离群值的量化难题，**顶部子空间保留**则从根源抑制了 NS 迭代的误差放大，二者的协同使整体量化误差从 1.78 降至 **0.14**（**Section 3.4**），从而恢复全精度性能。

### 4. 主要局限与待解决问题

* **秩的手动指定**：顶部子空间的秩 $k$ 目前需要手动设定，缺乏自适应的秩选择策略。自适应的秩选取（例如根据训练阶段或矩阵条件数动态调整）仍是一个开放问题。
* **仅压缩优化器状态**：当前工作仅针对优化器状态内存，未结合激活值压缩等技术。若同时降低激活内存，可支持更大模型的全低比特训练。
* **分布式场景未优化**：实验主要在单设备上进行，低比特优化器在多 GPU / 分布式训练下的通信与计算效率尚未专门优化，这构成了后续工程实用的重要方向。

（以上所有结论均来自本次提供的证据片段，部分表格数据（如 Table 5–10）因上下文限制而引用锚点，细节需查阅原论文。）



## 定位与知识库关联

### 与基线方法的关系

4-bit-Muon-GRASP 的核心贡献在于揭示了朴素低比特量化的瓶颈，并据此设计了针对性的解决方案。该方法直接对比的基线有三类：

1. **fp32-Muon**：全精度 Muon 优化器，作为精度上界参照。GRASP 在 350M 模型预训练下游任务平均准确率上仅落后 0.1 个百分点（44.5 vs 44.6），在 1.1B 模型验证困惑度上完全持平（12.48），证明 4 比特压缩几乎没有精度代价。
2. **8-bit-Muon**：直接对矩矩阵做 8 比特量化的朴素方案。GRASP 用更低的位宽（4 比特）实现了相同甚至略优的精度，且在 1.1B 模型上节省了更多内存（10.14 GB vs 11.84 GB，约 14.4% 额外节省）。
3. **4-bit-Muon-base**：直接对矩矩阵做 4 比特分组的朴素量化。该基线在验证损失和下游任务上均明显劣于全精度方案，直接验证了“朴素量化→NS 迭代→误差放大”这一失败机制。论文通过 Table 1 和 Figure 1 证实，NS 迭代将顶部奇异子空间的量化误差放大达 40 倍（RE 从 0.08 增至 3.31），而残差子空间仅放大约 5 倍。进一步，Figure 2 排除了“迭代不足”这一替代解释——增加 NS 迭代次数或多项式阶数并不能缩小误差，有时甚至进一步扩大。

因此，4-bit-Muon-GRASP 并非简单的位宽缩减，而是通过**子空间分解（顶部 8 比特 + 残差 4 比特）**与**网格量化（行列双向逐元素归一化）**两个关键手段，系统性解决了 NS 迭代对量化误差的选择性放大问题。

### 方法适用边界

4-bit-Muon-GRASP 的适用条件可从实验覆盖范围和设计假设两个维度界定：

- **模型规模**：已在 LLaMA 架构的 130M、350M、1.1B 预训练以及 Qwen2.5-7B 监督微调上验证。在更大规模（如 13B+ 或非 LLaMA 架构）上的表现未见报道。
- **训练阶段**：预训练和 SFT 均表现出与全精度相当的精度，但未涉及 RLHF 等更复杂的训练范式。
- **量化位宽选择**：顶部奇异子空间默认使用 8 比特，残差使用 4 比特。消融实验（Figure 7(b)）表明网格量化可将 4 比特量化带来的训练损失差距缩小为普通分组量化的一半，但若进一步压至更低位宽（如 2 比特）是否仍有效，尚不可知。
- **数据格式**：INT4 与 FP4 训练曲线几乎一致，FP4 引入轻微效率开销（Figure 9）。这意味着数据格式的选择对精度影响不敏感，可依据硬件偏好灵活决定。
- **秩选择**：顶部奇异子空间的秩 $k$ 需要手动选择。消融（Figure 7(a) 及 Table 9-10）显示 $k/r = 1/16$ 提供了较好的精度-效率折中，但缺乏自动秩选择策略。秩越大精度越高，但幂迭代和 QR 分解的耗时与内存开销也越大（Table 8）。

### 局限与未解决问题

论文明确列出或可从实验中推断的局限包括：

1. **无自动秩选择机制**：顶部奇异子空间的秩需人工设置。对于不同规模、不同深度的模型层，理想的秩可能不同，缺乏统一的自动化策略。
2. **仅压缩优化器状态**：当前工作仅对 Muon 的矩矩阵进行低比特压缩，未结合激活值压缩、梯度压缩或低精度前向传播等技术。若与上述技术协同，端到端训练内存有望进一步缩减。
3. **分布式训练场景未优化**：现有实验均在单设备上完成，未讨论低比特优化器在多 GPU 或分布式训练场景下的通信效率、同步策略及与模型并行／流水线并行的兼容性。
4. **对离群值的依赖**：网格量化的设计动机是处理双向离群值（Figure 3 左），但若模型经过特殊归一化或架构调整使得离群值模式改变，网格量化的收益可能减弱。这一鲁棒性边界未被测试。
5. **理论解释不足**：NS 迭代为何主要放大顶部奇异子空间的误差，其与矩阵条件数、奇异值衰减速度的关系缺乏形式化分析，限制了对方法在极端条件下行为的事前预测能力。

### 在优化器压缩谱系中的定位

从更宏观的视角看，4-bit-Muon-GRASP 属于**矩阵正交化优化器状态压缩**这一新类别。传统优化器压缩（如 8-bit Adam、MicroAdam）聚焦于自适应学习率统计量的量化，而 Muon 的独特之处在于其包含了 Newton-Schulz 正交化步骤。该步骤将“量化误差”映射为“正交化方向偏差”，且这一映射具有对顶部奇异子空间的非线性敏感性。这使得针对 Adam/SGD 的压缩策略无法直接迁移至 Muon。

该方法通过两个创新突破了这一壁垒：（1）**子空间分解**将压缩问题转化为一个条件不一的“高低精度分治”问题；（2）**网格量化**以逐元素独立尺度的方式处理跨维度离群值，避免了分组量化对该离群值模式的覆盖不足。其保持精度的关键并非“永远用足所有比特”，而是“将对正交化影响最大的子空间保护起来”。

因此，4-bit-Muon-GRASP 为后续的低比特正交化优化器提供了两条可延续的设计原则，也为进一步探索“优化器精度-训练稳定性-内存占用”三角权衡奠定了基础。



## 原文 PDF

PDF 文件：paperPDFs/ICLR_2026/Achieving_low_bit_Muon_through_subspace_preservation_and_grid_quantization.pdf

![[paperPDFs/ICLR_2026/Achieving_low_bit_Muon_through_subspace_preservation_and_grid_quantization.pdf]]
