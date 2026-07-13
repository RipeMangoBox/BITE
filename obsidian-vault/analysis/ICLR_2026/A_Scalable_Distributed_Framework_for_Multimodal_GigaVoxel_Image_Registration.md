---
title: "A Scalable Distributed Framework for Multimodal GigaVoxel Image Registration"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/A_Scalable_Distributed_Framework_for_Multimodal_GigaVoxel_Image_Registration.pdf
project_link: null
code_link: null
aliases:
- FFFDP
- SDFMGIR
tags:
- ICLR_2026
- topic/optimization_theory_probabilistic
- topic/optimization_theory_probabilistic/large_scale_parallel_and_distributed
core_operator: "通过IO感知的非GEMM融合内核（复合隐式网格采样器、隐式Parzen窗互信息、高效隐式融合局部归一化互相关）消除中间高带宽内存（HBM）存储，以及通过GridParallel分片和环采样器实现分布式配准，从而将内存开销从O(n)降至O(1)并支持任意规模。"
primary_logic: "图像配准中的主要瓶颈是非GEMM操作（网格采样、LNCC、MI），而非矩阵乘法；通过将中间变量计算保持在寄存器或共享内存中，避免HBM物化，可以大幅降低内存并加速；同时，利用分片和环拓扑通信实现分布式插值，避免全收集操作。"
claims:
- "FFDP在单GPU上可处理比现有SOTA大64倍的问题。"
- "FFDP加速传统配准管线最高7.48倍，内存降低最高59%；加速深度学习管线最高6.14倍，内存降低最高24%。"
- "在8块A6000 GPU上，约1分钟内完成100µm ex-vivo人脑MRI与250µm in-vivo MRI的多模态配准，问题规模比标准临床数据大570倍以上（11.8B参数）。"
- "在250µm分辨率下，Dice提升18.1点，InvDice提升31.6点，AvgHD90降低62.1%。"
---

# A Scalable Distributed Framework for Multimodal GigaVoxel Image Registration

> [!tip] 核心洞察
> 图像配准中的主要瓶颈是非GEMM操作（网格采样、LNCC、MI），而非矩阵乘法；通过将中间变量计算保持在寄存器或共享内存中，避免HBM物化，可以大幅降低内存并加速；同时，利用分片和环拓扑通信实现分布式插值，避免全收集操作。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 面向多模态千兆体素图像配准的可扩展分布式框架 |
| 英文题名 | A Scalable Distributed Framework for Multimodal GigaVoxel Image Registration |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=8dLexnao2h) |
| Topic | #topic/optimization_theory_probabilistic #topic/optimization_theory_probabilistic/large_scale_parallel_and_distributed |
| Method | FFDP (Flash Fused Distributed Primitives) |
| Dataset | Faux-OASIS (250µm), Faux-OASIS (1mm) |

> [!tip] 效果简介
> - Faux-OASIS (250µm) 上，Dice ↑ 为 0.895 ± 0.029，对比 0.714 (SyN)，变化 +0.181。
> - Faux-OASIS (250µm) 上，InvDice ↑ 为 0.597 ± 0.204，对比 0.281 (SyN)，变化 +0.316。
> - Faux-OASIS (250µm) 上，AvgHD90 ↓ 为 0.216 ± 0.098，对比 0.570 (SyN)，变化 -62.1%。

## 概要

本文针对现有图像配准方法无法处理超高分辨率（如100µm人脑MRI）这一瓶颈，提出了FFDP（Flash Fused Distributed Primitives）框架。核心问题在于：标准方法在单GPU上仅能处理约50M参数的问题，而实际需求可达11.8B参数；传统深度学习方法的激活内存占用过大（例如250µm图像对首层即需27GB），且现有分布式框架（如CLAIRE）内存效率不足。

FFDP的核心洞察在于：图像配准中的主要瓶颈是非GEMM操作（网格采样、LNCC、MI），而非矩阵乘法。通过将中间变量计算保持在寄存器或共享内存中，避免高带宽内存（HBM）物化，可以大幅降低内存并加速。具体实现包括：复合隐式网格采样器（将内存开销从O(n)降至O(1)）、隐式Parzen窗互信息（利用共享内存避免大张量物化）、高效隐式融合局部归一化互相关（前向传播仅需5×中间变量存储）。在分布式方面，通过GridParallel分片和环采样器实现分布式配准，环采样器将双线性/三线性插值分解为部分和并通过环拓扑通信累加，避免全收集操作。

主要实验结果表明：在单GPU上，FFDP可处理比现有SOTA大64倍的问题；在8块A6000 GPU上，约1分钟内完成100µm ex-vivo人脑MRI与250µm in-vivo MRI的多模态配准（11.8B参数，比标准临床数据大570倍以上）。在250µm分辨率下，Dice提升18.1点，InvDice提升31.6点，AvgHD90降低62.1%。加速方面，FFDP加速传统配准管线最高7.48倍（内存降低最高59%），加速深度学习管线最高6.14倍（内存降低最高24%）。消融实验显示，融合LNCC内核比基线快6.1倍，内存降低16.5%；融合MI内核内存降低24.7%；隐式网格采样器内存降低50%。分布式框架的峰值内存消耗与GPU数量无关，且扩展效率仅受轻微影响。

图像配准的目标是寻找一个坐标变换，将移动图像（M）变形以匹配固定图像（F），其核心形式化为最小化代价函数 C（衡量图像间差异）与正则项 R 之和：$\varphi ^ { * } = \underset { \varphi \in G } { \arg \operatorname* { m i n } } L ( \varphi ) \doteq C ( F , M \circ \varphi ) + R ( \varphi )$。尽管该问题在临床尺度（约20M参数）上已有成熟方案，但向超高分辨率（如100µm人脑MRI，参数规模可达11.8B）扩展时，现有方法遭遇了根本性的内存瓶颈。

**现有方法的缺口**集中在两个层面。首先，**标准算法无法扩展到千兆体素规模**：传统优化方法（如SyN）和深度学习配准网络（如VoxelMorph、TransMorph）在单GPU上仅能处理约50M参数的问题，而实际需求高出两个数量级。以250µm分辨率的图像对为例，现有深度学习管线在首层即需27GB激活内存，迫使采用分块（patch-based）策略，牺牲了全局一致性。其次，**现有分布式框架内存效率不足**：虽然CLAIRE等分布式方法试图通过分片解决规模问题，但其内存开销仍比本文提出的FFDP高约5倍，且扩展性受限于全收集（allgather）操作带来的通信与存储开销。

**本文的动机**源于对瓶颈本质的重新认识。通过分析FireANTs等优化配准管线，作者发现主要瓶颈并非矩阵乘法（GEMM），而是网格采样（grid sampler）、局部归一化互相关（LNCC）和互信息（MI）等非GEMM操作。这些操作在标准实现中会物化大量中间变量（如恒等网格、仿射网格、Parzen窗张量），导致内存开销从O(1)膨胀至O(n)。例如，LNCC的计算图会产生16倍于输入的内存开销，而MI的Parzen窗张量$\Psi_I, \Psi_J \in \mathbb{R}^{B \times N}$在体素级上不可接受。

基于此，FFDP提出了一套**IO感知的融合内核**策略：通过将中间变量的计算保持在寄存器或共享内存中，避免HBM物化。具体而言，复合隐式网格采样器在单个内核中完成仿射变换与变形场的复合采样（$\mathtt{fused\_grid\_sampler}(I; A, t, [\mathbf{u}], S, x_{\mathrm{bounds}})(x) = I(Ax + t + Su(x))$），将内存从O(n)降至O(1)；隐式Parzen窗利用共享内存累加直方图和偏导数，避免物化大张量；融合LNCC前向传播仅需5倍内存存储中间变量，反向传播通过原地修改计算。同时，**GridParallel分片抽象**与**环采样器**实现了分布式配准，将双线性/三线性插值分解为部分和并通过环拓扑通信累加，避免了全收集操作，使峰值内存与GPU数量无关。

该工作的核心洞察是：通过消除非GEMM操作中的中间HBM存储，可以在不损失精度或运行时间的前提下，将单GPU可处理的问题规模提升64倍，并支持任意规模的分布式配准。实验证据表明，FFDP在单GPU上可处理比现有SOTA大64倍的问题；在8块A6000 GPU上，约58秒内完成了100µm ex-vivo人脑MRI与250µm in-vivo MRI的多模态配准（11.8B参数，比标准临床数据大570倍以上）；在250µm分辨率下，Dice提升18.1点，InvDice提升31.6点，AvgHD90降低62.1%。这些结果验证了融合内核与分布式框架在解决大规模配准内存瓶颈上的有效性。

## 核心方法与创新机理

FFDP (Flash Fused Distributed Primitives) 的核心创新在于识别并解决了大规模图像配准中一个被忽视的瓶颈——**非GEMM操作**的内存与计算效率问题。与主流观点不同，FFDP 发现网格采样、局部归一化互相关（LNCC）和互信息（MI）等非矩阵乘法操作才是制约超高分辨率配准的关键，而非深度学习中的卷积或全连接层。其创新体现在四个关键“插槽”的重新设计：

1.  **复合隐式网格采样器**：传统方法需要物化恒等网格、仿射网格、变形网格等多个中间张量，内存开销为 O(n)。FFDP 将其融合为一个内核，在单次操作中完成仿射变换和变形场的复合采样，内存开销降至 O(1)，且无运行时或精度损失。其核心公式为 `fused_grid_sampler(I; A, t, [u], S, x_bounds)(x) = I(Ax + t + Su(x))`。

2.  **隐式Parzen窗互信息（MI）**：传统 MI 计算需要物化 Parzen 块 Ψ_I, Ψ_J ∈ R^(B×N̂)，内存开销 O(N)。FFDP 利用 B（核函数宽度）较小的特性，避免物化这些大张量，转而使用共享内存直接累加直方图和偏导数，内存开销降至 O(1)。

3.  **高效隐式融合局部归一化互相关（LNCC）**：标准 LNCC 计算图会产生 16× 的 HBM 开销，梯度计算再增加 16×。FFDP 的融合前向传播仅需 5× 内存存储中间变量（I, J, I², J², IJ 与矩阵 w 的卷积），梯度则通过原地修改保存的中间变量计算，大幅降低内存占用。

4.  **分布式配准框架（GridParallel + 环采样器）**：通过 GridParallel (GP) 抽象实现张量分片和边界同步（halo 交换），避免全收集操作。环采样器（Ring Sampler）利用双线性/三线性插值可分解为部分和的性质，通过环拓扑通信累加各图像分片的插值结果，使峰值内存消耗与 GPU 数量 H 无关。

这些创新的因果机制在于：**将中间变量计算保持在寄存器或共享内存中，避免 HBM 物化**。实验证据表明，FFDP 在单 GPU 上可处理比现有 SOTA 大 64 倍的问题；加速传统配准管线最高 7.48 倍，内存降低最高 59%；加速深度学习管线最高 6.14 倍，内存降低最高 24%。在 8 块 A6000 GPU 上，约 1 分钟内完成 100µm ex-vivo 人脑 MRI 与 250µm in-vivo MRI 的多模态配准，问题规模比标准临床数据大 570 倍以上（11.8B 参数）。在 250µm 分辨率下，Dice 提升 18.1 点，InvDice 提升 31.6 点，AvgHD90 降低 62.1%。消融实验进一步验证：融合 LNCC 内核比基线快 6.1 倍，内存降低 16.5%；融合 MI 内核内存降低 24.7%；隐式网格采样器内存降低 50%；FireANTs 使用 MI 时内存节省最高 95.2%，加速 2.6 倍。

需要注意的是，FFDP 主要针对优化方法（training-free）进行优化，深度学习方法的激活内存瓶颈虽被提及但未提出针对性融合方案。分布式框架的环采样器在大变形情况下的通信开销和收敛质量影响尚未详细分析，且实验仅在 MRI 模态上进行。

![[assets/figures/papers/iclr26_0003_8dLexnao2h_A_Scalable_Distributed_Framework_for_Multimodal/figures/003_Figure_3.jpg]]
*Figure 3: Left: Overview of our distributed framework. GridParallel (GP) shards the fixed and moving images (F, M) and the warp field [u] across multiple GPUs. Yellow blocks and arrows denote synchronized halo boundaries between ${ \mathrm { G P U s } }$ , enabling smoothing on images and warp fields without an allgather. The ring sampler (violet) computes interpolated image shards on the fly, avoiding materialization of the full moving image. We then compute losses (MSE, LNCC, MI), compute gradients w.r.t. each warp shard, apply Sobolev regularization with GP, and update shards by gradient descent. Right: Scaling efficiency compared to deep methods and CLAIRE (Mang et al., 2019), a distributed registr...*

FFDP 的架构围绕“消除中间物化”和“分布式分片”两条主线设计，将传统配准管线中的三个主要瓶颈——网格采样、互信息（MI）和局部归一化互相关（LNCC）——替换为 IO 感知的融合内核，并通过 GridParallel 分片抽象和环采样器实现跨 GPU 的任意规模扩展。

**单 GPU 融合内核层**：管线以配准目标函数 `φ* = argmin L(φ) ≐ C(F, M∘φ) + R(φ)` 为起点，核心操作是网格采样器将移动图像 M 根据变换 φ 变形为 M∘φ，再通过损失函数 C 与固定图像 F 比较。FFDP 的**复合隐式网格采样器**在单个融合内核中完成仿射变换 `(A, t)` 与变形场 `u` 的复合采样 `I(Ax + t + Su(x))`，避免物化恒等网格、仿射网格、变形网格等中间张量，将内存开销从 O(n) 降至 O(1)。对于 MI 损失，**隐式 Parzen 窗**利用 B 较小（直方图 bin 数）这一事实，在共享内存中直接累加直方图和偏导数，避免物化 Ψ_I, Ψ_J ∈ R^(B×N̂) 大张量。对于 LNCC 损失，**高效隐式融合 LNCC** 将前向传播的中间变量存储从基线的 16× 降至 5×（仅需存储 I, J, I², J², IJ 与权重矩阵 w 的卷积结果），反向传播则通过原地修改保存的中间变量计算梯度，避免重新计算或额外存储。这些融合内核的共同机制是将原本需要写入高带宽内存（HBM）的中间变量保持在寄存器或共享内存中，直接消除 HBM 读写开销。

**分布式分片层**：FFDP 提出 **GridParallel (GP)** 抽象，将固定图像 F、移动图像 M 和变形场 `[u]` 沿空间维度分片到多个 GPU 上。GP 维护分片间的 halo 边界同步，使得平滑操作（如 Sobolev 正则化）可以在不进行全收集（allgather）的情况下正确执行。分布式插值面临的核心挑战是：变形场中相邻坐标可能指向任意图像分片上的像素位置。FFDP 的**环采样器**利用双线性/三线性插值可分解为部分和的性质，在环拓扑上交错执行图像分片获取和部分和累加，最终峰值内存消耗与 GPU 数量 H 无关，避免了全收集操作带来的内存爆炸。各 GPU 独立计算损失函数（MSE、LNCC、MI）对各自变形场分片的梯度，经 GP 同步后应用 Sobolev 正则化，最后以梯度下降更新变形场分片。

**整体数据流**：输入为固定图像 F、移动图像 M 和初始变换（通常为恒等变换），输出为最优变形场 φ*。在单 GPU 场景中，融合内核直接替换管线中的对应操作；在多 GPU 场景中，GP 负责数据分片和边界同步，环采样器负责分布式插值，各分片上的损失计算和梯度更新独立进行，仅在正则化和 halo 同步时通信。这一设计使得 FFDP 在单 GPU 上可处理比现有 SOTA 大 64 倍的问题，在 8 块 A6000 GPU 上约 1 分钟完成 100µm ex-vivo 人脑 MRI 与 250µm in-vivo MRI 的多模态配准（11.8B 参数，比标准临床数据大 570 倍以上）。

### 配准目标函数与核心公式

图像配准的目标是寻找一个最优的空间变换 $\varphi^*$，使得变形后的移动图像 $M \circ \varphi$ 与固定图像 $F$ 的差异最小化，同时保持变换的光滑性。其形式化目标函数为：

$$
\varphi ^ { * } = \underset { \varphi \in G } { \arg \operatorname* { m i n } } L ( \varphi ) \doteq C ( F , M \circ \varphi ) + R ( \varphi )
$$

其中 $C(\cdot, \cdot)$ 是衡量图像相似度的代价函数（如LNCC、MI、MSE），$R(\varphi)$ 是正则化项（如Sobolev平滑），$G$ 是允许的变换空间（如微分同胚）。该公式是全文所有优化管线的基础。

### 复合隐式网格采样器（Composite Implicit Grid Sampler）

**瓶颈**：传统网格采样器需要物化多个中间网格（恒等网格、仿射网格、变形网格），内存开销为 $O(n)$，在千兆体素尺度下不可行。

**核心公式**：FFDP提出的融合采样核在一个内核中完成所有变换，无需物化任何中间网格：

$$
\mathtt { f u s e d \_ g r i d \_ s a m p l e r } ( I ; A , t , [ \mathbf { u } ] , S , x _ { \mathrm { b o u n d s } } ) ( x ) = I ( A x + t + S u ( x ) )
$$

- **变量含义**：$I$ 为输入图像；$A$ 和 $t$ 为仿射变换矩阵和平移向量；$\mathbf{u}$ 为变形场；$S$ 为变形场缩放因子；$x_{\mathrm{bounds}}$ 为边界裁剪参数；$x$ 为输出坐标。
- **因果机制**：将仿射变换 $Ax + t$ 和变形场插值 $Su(x)$ 在单个内核中复合，所有中间坐标计算在寄存器中完成。这使内存开销从 $O(n)$ 降至 $O(1)$，且运行时无损失。

**证据强度**：该模块消融实验显示内存降低50%（Figure 7），且精度无损。

### 隐式Parzen窗互信息（Implicit Parzen Windowing for MI）

**瓶颈**：标准互信息计算需要物化Parzen块 $\Psi_I, \Psi_J \in \mathbb{R}^{B \times N}$（$B$为直方图桶数，$N$为像素数），内存开销 $O(N)$。

**核心公式**：使用核密度估计计算边缘和联合分布：

$$
P_I(v) = \frac{1}{N} \sum_k \kappa(v - I_k), \quad P_{(I,J)}(v,w) = \frac{1}{N} \sum_k \kappa(v - I_k) \kappa(w - J_k)
$$

- **变量含义**：$P_I(v)$ 为强度值 $v$ 的边缘概率；$P_{(I,J)}(v,w)$ 为强度对 $(v,w)$ 的联合概率；$\kappa(\cdot)$ 为核函数（如三次B样条）；$I_k, J_k$ 为第 $k$ 个像素的强度值。
- **因果机制**：利用 $B$ 较小（通常16-64）的事实，避免物化 $\Psi_I, \Psi_J$ 张量。通过共享内存累加直方图条目和偏导数，每个像素的贡献在寄存器中计算后直接原子累加到共享内存的直方图中，内存开销从 $O(N)$ 降至 $O(B^2)$。
- **分布式扩展**：在分布式设置中，全局分布通过加权各分片直方图得到：

$$
p_I(v) = \sum_h \frac{N_h}{N} \cdot \frac{1}{N_h} \sum_{k \in \Omega_h} \kappa(v - I_k), \quad p_{IJ}(v,w) = \sum_h \frac{N_h}{N} \left( \frac{1}{N_h} \sum_{k \in \Omega_h} \kappa(v - I_k) \kappa(w - J_k) \right)
$$

其中 $h$ 为GPU索引，$N_h$ 为分片 $h$ 的像素数，$\Omega_h$ 为分片 $h$ 的像素集合。

**证据强度**：该内核使MI内存降低24.7%（Figure 7），在FireANTs管线中内存节省最高95.2%，加速2.6倍。

### 高效隐式融合局部归一化互相关（Fused LNCC）

**瓶颈**：标准LNCC计算图产生16× HBM开销（前向存储中间变量），梯度计算再增加16×。

**核心公式**：LNCC的计算基于局部图像块的均值、方差和协方差。FFDP的融合实现将前向传播的中间变量存储从16×降至5×，仅需存储 $I, J, I^2, J^2, IJ$ 与卷积核 $w$ 的卷积结果。

- **变量含义**：$I, J$ 为固定和移动图像；$I^2, J^2, IJ$ 为逐元素乘积；$w$ 为局部窗口的卷积核（如高斯核或均匀核）。
- **因果机制**：前向传播中，5个中间变量在寄存器中计算并写回HBM；反向传播时，通过原地修改这些保存的中间变量计算梯度，避免重新计算或额外存储。消融实验显示前向传播平均加速5.22倍，反向传播加速56.98倍。

**证据强度**：融合LNCC内核比基线快6.1倍，内存降低16.5%（Table 1）；在FireANTs管线中加速7.5倍，内存降低44-59%。

### 环采样器（Ring Sampler）与分布式插值

**瓶颈**：在分布式设置中，变形场的非局部性导致每个GPU可能需要访问所有其他GPU的图像分片，标准的全收集（allgather）策略内存开销大。

**核心公式**：双线性/三线性插值可分解为图像分片上的部分和之和：

$$
I(x) = \sum_{h} \text{partial\_sum}_h(x), \quad \text{partial\_sum}_h(x) = \sum_{p \in \text{shard}_h} w_p \cdot I(p)
$$

- **变量含义**：$x$ 为查询坐标；$h$ 为GPU索引；$w_p$ 为插值权重；$\text{shard}_h$ 为GPU $h$ 上的图像分片。
- **因果机制**：环采样器交错执行分片获取和部分和聚合。每个GPU在环拓扑中依次接收下一个GPU的分片，累加部分插值结果，然后传递。这避免了物化完整移动图像，使峰值内存消耗与GPU数量 $H$ 无关（Figure 8a），且扩展效率损失极小。

**证据强度**：消融实验验证了峰值内存与 $H$ 无关（Figure 8a），且边界同步缺失会导致移动图像出现伪影并降低标签图重叠（Figure 8b, Figure 9, Figure 10）。

### 模块间关系总结

四个核心模块构成FFDP的完整管线：复合隐式网格采样器负责高效变形；隐式Parzen窗MI和融合LNCC作为可互换的代价函数 $C(F, M \circ \varphi)$；环采样器使分布式计算成为可能；GridParallel分片抽象（含边界halo同步）支持正则化 $R(\varphi)$ 的分布式应用。这些模块通过消除HBM中间变量物化，将内存开销从 $O(n)$ 降至 $O(1)$，从而支持11.8B参数的千兆体素配准。

## 实验与关键发现

### 主结果：跨分辨率配准性能

FFDP在Faux-OASIS数据集上进行了从1mm到250µm原生分辨率的多分辨率配准评估。在250µm（最高挑战性分辨率）下，FFDP在Dice上比SyN基线提升18.1点（0.895±0.029 vs 0.714），InvDice提升31.6点（0.597±0.204 vs 0.281），AvgHD90降低62.1%（0.216±0.098 vs 0.570）。在1mm和500µm分辨率下，FFDP分别达到AvgDice 0.838±0.028和0.872±0.028。值得注意的是，所有深度学习基线（VoxelMorph、TransMorph、MIDIR、UniGradICON）在250µm下因内存限制只能采用分块策略，而FFDP可处理完整分辨率，这解释了其显著优势。

### 极端规模配准：100µm人脑MRI

在8块NVIDIA A6000 GPU上，FFDP耗时约58秒完成了100µm ex-vivo人脑MRI（T1→FLASH）的多模态可变形配准。该问题的变换参数超过11.8B，比标准临床数据（约20M参数）大570倍以上。定性结果（图6）显示，小脑白质等宏观尺度不可见的精细结构在100µm下得到精确对齐。

### 消融实验：融合内核效果

**LNCC融合内核**：FFDP的LNCC实现比基线（FastLNCC）加速6.1倍，同时内存使用降低16.5%。前向传播平均加速5.22倍，反向传播加速56.98倍。融合前向传播仅需5×内存存储中间变量（I, J, I², J², IJ与卷积核w的卷积结果），而基线计算图产生16× HBM开销，梯度计算再增加16×。

**MI融合内核**：隐式Parzen窗方法将内存使用降低24.7%。通过利用B（直方图箱数）较小的特点，避免物化Ψ_I, Ψ_J ∈ R^(B×N̂)张量，使用共享内存累加直方图和偏导数。

**复合隐式网格采样器**：内存开销从O(n)降至O(1)，实现50%的内存降低，且运行时无损失。

**FireANTs管线加速**：集成FFDP后，FireANTs在使用MI时实现最高95.2%内存节省和2.6倍加速；使用LNCC时加速7.5倍，内存降低44-59%。

### 分布式框架消融

**GridParallel边界同步**：图8b显示，缺少边界同步（halo交换）会导致移动图像中出现伪影，并降低标签图重叠。红箭头标记了受影响区域。

**环采样器内存独立性**：峰值内存消耗与GPU数量H无关，因为环采样器避免了全收集操作，将双线性/三线性插值分解为部分和并通过环拓扑通信累加。

**扩展效率**：FFDP在弱扩展测试中内存消耗远低于CLAIRE（约5倍），且扩展效率仅受最小影响。

![[assets/figures/papers/iclr26_0003_8dLexnao2h_A_Scalable_Distributed_Framework_for_Multimodal/figures/005_Table_1.jpg]]
*Table 1: (a) Performance comparison across methods and resolutions*

![[assets/figures/papers/iclr26_0003_8dLexnao2h_A_Scalable_Distributed_Framework_for_Multimodal/figures/010_Table_2.jpg]]

![[assets/figures/papers/iclr26_0003_8dLexnao2h_A_Scalable_Distributed_Framework_for_Multimodal/figures/007_Figure_5.jpg]]
*Figure 5: Registration performance on Faux-OASIS dataset at 1 mm, 500 µm, and 2 5 0 $\mathrm { { \mu m } }$ (native 250 µm); mean ± std over pairs. ↑ higher is better; ↓ lower is better. HD90 values are reported using our cumulative definition (see Sec. K.2). (Green)/ (Yellow) = best/second; †= patch-based

## 定位与知识库关联

FFDP 的定位是**面向极高分辨率（千兆体素级）多模态图像配准的 IO 感知分布式基元库**，其核心策略并非提出新的配准模型，而是通过融合内核与分布式分片，消除传统管线中非 GEMM 操作（网格采样、LNCC、MI）的中间 HBM 存储瓶颈。这一思路与现有方法形成鲜明对比：

**与基线方法的关系**：FFDP 直接替换 FireANTs、TransMorph、VoxelMorph、MIDIR、UniGradICON 等管线中的内存密集型操作（网格采样器、LNCC 损失、MI 损失）。在单 GPU 上，FFDP 可处理比现有 SOTA 大 64 倍的问题，加速传统管线最高 7.48 倍、内存降低 59%；加速深度学习管线最高 6.14 倍、内存降低 24%。在 8 块 A6000 GPU 上，约 58 秒完成 100µm ex-vivo 人脑 MRI 与 250µm in-vivo MRI 的多模态配准（11.8B 参数，比标准临床数据大 570 倍）。与分布式基线 CLAIRE 相比，FFDP 的内存消耗低约 5 倍。

**适用边界**：FFDP 主要针对**优化式配准（training-free）** 管线，其融合内核针对非 GEMM 操作设计，对深度学习网络中的 GEMM 类操作（如卷积）的分布式支持有限。框架在 MRI 模态上验证充分，但对 CT、组织学等其他模态的泛化性尚未确认。分布式环采样器在变形场连续且平滑时高效，但大变形或非连续变形场下可能引入额外通信开销。

**核心局限**：
1. 深度学习方法的激活内存瓶颈虽被提及，但未提出针对性的融合方案。
2. 环采样器对收敛质量的定量影响（尤其在大变形场景）未深入分析。
3. 当前框架不直接支持非微分同胚变换或更复杂的正则化器（如总变分、逆一致性）。

**开放问题**：
1. 如何将 FFDP 的融合内核思想扩展到深度学习配准网络中的激活内存优化？
2. 环采样器在大变形或非连续变形场下的收敛性和精度如何？
3. FFDP 能否扩展到非微分同胚变换或更复杂的正则化器？
4. 框架在其他模态（如 CT、PET、组织学）上的表现如何？
5. 能否将 FFDP 与模型并行技术（如张量并行）结合，进一步加速深度学习配准？

## 原文 PDF

PDF 文件：paperPDFs/ICLR_2026/A_Scalable_Distributed_Framework_for_Multimodal_GigaVoxel_Image_Registration.pdf

![[paperPDFs/ICLR_2026/A_Scalable_Distributed_Framework_for_Multimodal_GigaVoxel_Image_Registration.pdf]]
