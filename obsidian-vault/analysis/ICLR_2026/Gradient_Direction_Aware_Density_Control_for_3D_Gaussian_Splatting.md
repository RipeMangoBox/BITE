---
title: Gradient-Direction-Aware Density Control for 3D Gaussian Splatting
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/Gradient_Direction_Aware_Density_Control_for_3D_Gaussian_Splatting_c387d81038ca.pdf
project_link: null
code_link: "https://github.com/zzcqz/GDAGS"
aliases:
- GGDAGS
- GDADC3GS
tags:
- ICLR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
core_operator: 通过梯度方向一致性比率（GCR）调整每个高斯的密度控制决策，对分裂和克隆进行差异化调制。
primary_logic: 将梯度方向一致性转化为非线性动态权重，在分裂操作中优先处理方向冲突的高斯，在克隆操作中抑制方向不一致的高斯，从而平衡几何细节与存储开销。
claims:
- 在Mip-NeRF360、Tanks&Temples、Deep Blending三个数据集上，GDAGS的PSNR分别达到28.02、23.79、29.70，均优于3DGS，同时内存占用更低。
- GDAGS仅需Pixel-GS 20%-50%的内存即可达到相近或更优的渲染质量。
- 非线性权重函数在消融实验中显著优于线性替代方案（GDAGS-L），验证了幂函数形式对梯度方向冲突的敏感性和一致性抑制的优越性。
- Mip-NeRF360 上 PSNR = 28.02
---

# Gradient-Direction-Aware Density Control for 3D Gaussian Splatting

> [!tip] 核心洞察
> 将梯度方向一致性转化为非线性动态权重，在分裂操作中优先处理方向冲突的高斯，在克隆操作中抑制方向不一致的高斯，从而平衡几何细节与存储开销。

| 字段 | 内容 |
|------|------|
| 中文题名 | 梯度方向感知的3D高斯泼溅密度控制方法 |
| 英文题名 | Gradient-Direction-Aware Density Control for 3D Gaussian Splatting |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=6qDxK4Gz7F) · [Code](https://github.com/zzcqz/GDAGS) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction |
| Method | GDAGS (Gradient-Direction-Aware Gaussian Splatting) |
| Dataset | Mip-NeRF360, Tanks&Temples, Deep Blending |

> [!tip] 效果简介
> - Mip-NeRF360 上，PSNR 28.02 vs 27.21 (3DGS) (+0.81)。
> - Tanks&Temples 上，PSNR 23.79 vs 23.14 (3DGS) (+0.65)。
> - Deep Blending 上，PSNR 29.70 vs 29.41 (3DGS) (+0.29)。

## 概述

3D高斯泼溅（3D Gaussian Splatting, 3DGS）在新视角合成领域取得了显著进展，但其密度控制策略存在一个被忽视的瓶颈：**仅依赖梯度的范数（magnitude）而忽略了梯度的方向一致性**。这导致两个相互制约的问题——大型高斯因内部梯度方向冲突而无法被有效分裂（过重建），以及方向一致区域的高斯被过度克隆（过密化），造成计算与存储资源的浪费。

针对这一瓶颈，本文提出**GDAGS（Gradient-Direction-Aware Gaussian Splatting）**，核心思路是引入**梯度方向一致性比率（Gradient Coherence Ratio, GCR）**来量化每个高斯在各像素上的子梯度方向对齐程度，并将其通过**非线性动态权重函数**映射为密度决策的调制因子：分裂时放大方向冲突高斯的权重以促进其分解，克隆时抑制方向不一致高斯的权重以避免冗余增殖。该方法在不改变3DGS训练框架的前提下，实现了对密度控制行为的精细化调节。

在Mip-NeRF360、Tanks&Temples和Deep Blending三个标准数据集上，GDAGS的PSNR分别达到28.02、23.79和29.70，全面优于3DGS基线，同时内存占用更低。值得注意的是，GDAGS仅需Pixel-GS的20%–50%内存即可达到相近或更优的渲染质量。消融实验验证了非线性权重函数相较线性替代方案的显著优势，以及指数幂参数$p=15$在质量与效率之间的最佳折衷。该方法还展现出良好的泛化性，可即插即用地集成到MCMC-3DGS和Compact-3DGS等3DGS变体中并带来一致的性能提升。

## 背景与动机

### 3D高斯泼溅的密度控制瓶颈

3D高斯泼溅（3D Gaussian Splatting, 3DGS）通过一组可微的3D高斯椭球体显式表示场景几何与外观，并依赖周期性的密度控制操作（分裂与克隆）来动态调整高斯数量，以重建复杂几何细节。其核心决策依据是**视空间位置梯度的平均范数** $\nabla_{\mu_i} L$（见公式4）：当该范数超过预设阈值 $\tau_p$ 时，系统根据高斯的3D尺度决定执行分裂（尺度大于 $\tau_s$）或克隆（尺度不大于 $\tau_s$）。

然而，这一机制存在根本性缺陷：**梯度范数仅反映梯度的强度，完全忽略了梯度方向的一致性**。这导致两类典型失效模式：

1. **过重建（Under-reconstruction）** ：大型高斯覆盖了纹理丰富的区域，其内部子像素梯度方向相互冲突，但因总范数被平均化而低于分裂阈值，无法有效分裂为更小的组件，导致几何细节丢失。
2. **过密化（Over-densification）** ：在梯度方向高度一致的区域（如平坦表面），小高斯持续触发克隆操作，造成高斯数量的过度增殖和存储开销膨胀。

### 现有方法的局限

近年来，多种3DGS变体试图改进密度控制策略，但均未从梯度方向角度系统解决上述问题：

- **Pixel-GS**（Zhang et al., 2024c）通过基于覆盖率的加权机制调整密度，但内存消耗显著增加。
- **AbsGS**（Ye et al., 2024）强制梯度方向均匀化，但缺乏对方向冲突与一致性的精细化区分。
- **Taming 3DGS**（Mallick et al., 2024）和**mini-splatting**（Fang & Wang, 2024）分别从优化稳定性和紧凑表示角度出发，未触及梯度方向一致性的核心瓶颈。

这些方法或侧重于抑制过密化而牺牲细节，或追求几何精度却付出高昂存储代价，缺乏一种**统一且方向感知的密度控制机制**。

### 本文动机

本文的核心洞察在于：**梯度方向一致性是区分“需要分裂的欠重建区域”与“需要抑制克隆的已充分重建区域”的天然信号**。具体而言：

- 当高斯覆盖纹理丰富区域时，其投射到各像素的子梯度方向高度分散，梯度方向一致性比率（GCR）趋近于0，应优先触发分裂以捕获细节。
- 当高斯位于平坦区域时，子梯度方向高度一致，GCR趋近于1，应抑制克隆以避免冗余增殖。

基于此，本文提出**GDAGS（Gradient-Direction-Aware Gaussian Splatting）** ，通过计算每个高斯的GCR并将其映射为非线性动态权重，对原始梯度范数进行方向感知调制，从而在分裂与克隆操作中实现差异化控制：在分裂时放大方向冲突高斯的权重以促进细节重建，在克隆时采用逆策略抑制方向一致高斯的过度增殖。这一设计在不牺牲渲染质量的前提下，显著降低了内存开销，实现了几何精度与存储效率的平衡。

## 核心创新

GDAGS 的核心创新在于将**梯度方向感知**引入 3DGS 的密度控制决策，解决了原始 3DGS 仅依赖梯度范数而忽略方向一致性的根本缺陷。该方法的三个关键 changed slots 构成了一个完整的因果链条：

### 瓶颈识别：梯度范数的信息盲区

3DGS 的密度化决策仅依赖视空间位置梯度的平均范数 $\nabla_{\mu_i} L$（Equation 4），这一标量度量无法区分两类本质不同的场景：**大型高斯在几何边缘处的梯度方向冲突**（需要分裂但梯度范数可能因方向抵消而被低估）与**方向一致区域的高斯过度响应**（梯度范数达标但实际无需增殖）。前者导致过重建（under-reconstruction），后者引发过密化（over-densification），两者共同推高存储开销并限制渲染质量。

### 核心度量：梯度方向一致性比率（GCR）

GDAGS 引入 **GCR**（Gradient Coherence Ratio）作为方向感知的量化工具：

$$\mathcal{C}_i = \frac{\| \sum_{pixel} \nabla_{i,pixel}^v \|_2}{\sum_{pixel} \| \nabla_{i,pixel}^v \|_2 + \epsilon}$$

该比率的值域为 $[0, 1]$：当高斯覆盖区域内各像素的子梯度方向高度一致时，$\mathcal{C}_i \to 1$；当子梯度方向相互冲突时，$\mathcal{C}_i \to 0$。GCR 的计算充分利用了渲染过程中已存在的梯度信息，无需额外的前向或反向传播，仅增加可忽略的计算开销。

### 动态调制：非线性权重函数与差异化策略

GCR 本身是一个诊断指标，GDAGS 的关键设计在于将其转化为**非线性动态权重**，对分裂和克隆操作施加差异化调制：

$$w_i = \alpha + \beta \cdot (1 - \mathcal{C}_i)^p$$

其中 $\alpha = 0.8$（抑制因子）、$\beta = 25$（放大因子）、$p = 15$（幂次敏感度）。该幂函数形式的选择具有明确的几何直觉：当 $\mathcal{C}_i$ 接近 1 时，$(1 - \mathcal{C}_i)^p$ 迅速衰减，$w_i \to \alpha$，对方向一致的高斯施加抑制；当 $\mathcal{C}_i$ 偏离 1 时，幂函数放大差异，$w_i$ 快速增大，对方向冲突的高斯赋予更高权重。

调制后的梯度范数 $\tilde{\nabla}_{\mu_i} L = w_i \cdot \nabla_{\mu_i} L$ 替代原始梯度范数作为密度决策的度量，但**分裂与克隆采用相反的策略**：
- **分裂阶段**：直接使用 $w_i$，优先分裂方向冲突的大型高斯（$\mathcal{C}_i$ 低 → $w_i$ 大 → 梯度范数被放大 → 更容易触发分裂阈值），使几何边缘得到更精细的表示。
- **克隆阶段**：采用逆策略 $1/w_i$，鼓励方向一致性高的小型高斯沿表面传播（$\mathcal{C}_i$ 高 → $1/w_i$ 大 → 更容易触发克隆阈值），同时抑制方向不一致区域的无效增殖。

这一差异化设计是 GDAGS 同时提升渲染质量与降低存储开销的因果枢纽：分裂阶段的方向感知解决了过重建问题，克隆阶段的逆策略抑制了过密化。

### 幂函数形式的必要性

消融实验（Table 2）直接验证了非线性权重函数相对于线性替代方案 $w_i = 2 - \mathcal{C}_i$（GDAGS-L）的优越性：非线性形式通过幂次 $p$ 放大了 GCR 微小差异的影响，使得权重函数对方向冲突更加敏感，同时更有效地抑制方向一致高斯的权重。这一设计选择是 GDAGS 性能提升的关键因素之一。

## 整体框架

GDAGS 在 3DGS 的密度控制流程中插入了一个轻量的**方向感知调制模块**，不改变原始训练管线的主体结构，仅替换密度化决策所依赖的梯度度量。整体流水线如 Figure 2 所示，包含三个串联的功能模块：

![[assets/figures/papers/paper_list_l84_https_openreview_net_forum_id_6qDxK4Gz7F/figures/002_Figure_2.jpg]]
*Figure 2: The pipeline of GDAGS. First, for each Gaussian, GDAGS computes the GCR to quantify the directional coherence of its subgradients. Subsequently, this GCR metric is mapped through a nonlinear dynamic weighting function to generate per-Gaussian gradient weights, which modulate the view-space positional gradient magnitudes and produce a refined decision metric. Finally, this decision metric is compared against a predefined threshold to dynamically regulate densification*

1. **GCR 计算模块**：对每个高斯核，收集其在所有可见像素上的视空间位置梯度，计算梯度方向一致性比率（Gradient Coherence Ratio, GCR）$\mathcal{C}_i$。该值域为 $[0,1]$，1 表示各像素梯度方向高度一致，0 表示方向严重冲突。这一模块是方向感知的核心，它区分了“方向冲突的大高斯”（需要分裂）和“方向一致的小高斯”（适合克隆以扩展表面覆盖）。

2. **非线性动态权重函数**：将 GCR 映射为每高斯的动态权重 $w_i = \alpha + \beta \cdot (1 - \mathcal{C}_i)^p$。其中 $\alpha=0.8$ 作为抑制因子压低方向一致高斯的权重，$\beta=25$ 作为放大因子提升方向冲突高斯的权重，指数幂 $p=15$ 控制非线性敏感度。该函数的设计使权重对高冲突区域（$\mathcal{C}_i \to 0$）高度敏感，而对一致性区域（$\mathcal{C}_i \to 1$）保持稳定抑制。

3. **加权密度决策**：用调制后的梯度范数 $\tilde{\nabla}_{\mu_i} L = w_i \cdot \nabla_{\mu_i} L$ 替代原始 3DGS 的视空间位置梯度范数，与预设阈值比较决定分裂或克隆。在分裂操作中直接使用 $w_i$，优先分裂存在方向冲突的大高斯以解决过重建；在克隆操作中采用逆策略 $1/w_i$，鼓励方向一致的小高斯沿表面传播，同时抑制方向不一致区域的过度增殖。

整个模块作为 3DGS 密度化步骤的即插即用替换，计算开销集中在 GCR 的逐像素梯度聚合上，不引入额外的可学习参数。超参数 $\alpha$、$\beta$、$p$ 在所有数据集和场景上保持固定，无需场景特定调优。

## 核心模块与公式推导

### 3DGS 密度控制的原始机制与瓶颈

3DGS 的密度控制完全依赖视空间位置梯度的平均范数 $\nabla_{\mu_i} L$，其定义为：

$$\nabla_{\mu_i} L = \frac{1}{M} \sum_{k=1}^{M} \sqrt{\left(\frac{\partial L_k}{\partial \mu_{i,x}^k}\right)^2 + \left(\frac{\partial L_k}{\partial \mu_{i,y}^k}\right)^2}$$

其中 $M$ 为高斯 $i$ 被投影到的像素数量。当 $\nabla_{\mu_i} L > \tau_p$ 时，3DGS 根据该高斯的 3D 尺度 $\Sigma_{3D}^i$ 决定操作：若 $\Sigma_{3D}^i > \tau_s$，执行分裂（split），将大高斯拆分为更小的组件；若 $\Sigma_{3D}^i \le \tau_s$，执行克隆（clone），在局部保持密度。

这一机制的根本瓶颈在于：**梯度范数仅反映梯度的总体强度，完全忽略了梯度的方向一致性**。当一个大型高斯覆盖了具有多方向纹理的区域时，其子梯度方向可能严重冲突，但平均范数可能仍低于阈值，导致该高斯无法被分裂，形成过重建（under-reconstruction）。反之，在方向高度一致的区域，多个小高斯可能因梯度范数达标而被反复克隆，造成过密化（over-densification）和内存浪费。

### 核心模块一：梯度方向一致性比率（GCR）

GDAGS 的核心创新是为每个高斯引入一个方向感知度量——梯度方向一致性比率（Gradient Coherence Ratio, GCR），定义为：

$$\mathcal{C}_i = \frac{\| \sum_{pixel} \nabla_{i,pixel}^v \|_2}{\sum_{pixel} \| \nabla_{i,pixel}^v \|_2 + \epsilon}$$

其中 $\nabla_{i,pixel}^v$ 表示高斯 $i$ 在单个像素上的视空间位置梯度向量，$\epsilon$ 为防止除零的小常数。该公式的物理含义清晰：分子为所有子梯度向量和的模长，分母为各子梯度模长之和。当所有子梯度方向完全一致时，$\mathcal{C}_i \to 1$；当子梯度方向相互抵消时，$\mathcal{C}_i \to 0$。GCR 的值域为 $[0, 1]$，为后续的动态权重调制提供了归一化的输入。

GCR 的计算模块（Figure 2）是 GDAGS 流水线的第一步：对每个高斯，收集其在所有投影像素上的视空间梯度，计算方向一致性比率，从而区分方向一致的高斯与方向冲突的高斯。

### 核心模块二：非线性动态权重函数

仅获得 GCR 度量尚不足以直接指导密度控制——需要将一致性信息转化为可操作的权重信号。GDAGS 设计了一个非线性动态权重函数：

$$w_i = \alpha + \beta \cdot (1 - \mathcal{C}_i)^p$$

该函数将 GCR 映射为每个高斯的动态权重 $w_i$，其中三个超参数各司其职：

- **$\alpha$（抑制因子，默认 0.8）**：为方向一致的高斯（$\mathcal{C}_i \to 1$）提供基线权重，抑制其被过度密度化。
- **$\beta$（放大因子，默认 25）**：控制对方向冲突高斯的权重放大程度。
- **$p$（幂指数，默认 15）**：控制权重对 GCR 变化的敏感度。$p$ 越大，权重函数在 $\mathcal{C}_i$ 接近 1 时越平坦（强抑制），在 $\mathcal{C}_i$ 降低时越陡峭（强放大），从而更精准地筛选出真正需要密度化的高斯。

非线性形式的选择是关键：消融实验（Table 2）表明，线性替代方案 $w_i = 2 - \mathcal{C}_i$（GDAGS-L）在所有数据集上的 SSIM/PSNR/LPIPS 和存储消耗均显著劣于非线性版本，验证了幂函数形式对梯度方向冲突的敏感性和一致性抑制的优越性。

### 核心模块三：加权密度决策

获得动态权重后，GDAGS 将其应用于原始梯度范数，形成调制后的决策度量：

$$\tilde{\nabla}_{\mu_i} L = w_i \cdot \nabla_{\mu_i} L$$

该调制梯度范数替换了 3DGS 原始的 $\nabla_{\mu_i} L$，与预设阈值比较以决定密度化操作。关键设计在于**分裂与克隆采用差异化的权重策略**：

- **分裂阶段**：直接应用 $w_i$。方向冲突的高斯（低 $\mathcal{C}_i$）获得高权重，优先被分裂，从而将大型高斯拆解为更小的组件以捕捉细节几何。
- **克隆阶段**：采用逆策略 $1/w_i$。方向一致的高斯（高 $\mathcal{C}_i$）获得更高权重，沿表面方向传播小高斯，增强局部密度；而方向不一致的高斯被抑制克隆，避免过密化。

这一差异化调制（Figure 2 流水线所示）是 GDAGS 平衡几何细节与存储开销的因果机制：分裂优先处理方向冲突的大高斯以缓解过重建，克隆抑制方向不一致的小高斯以遏制过密化。消融实验证实了这一设计的有效性：仅在分裂阶段施加权重（GDAGS-S）可有效提升 SSIM 和 LPIPS 并减少内存，仅在克隆阶段施加权重（GDAGS-C）则提升 PSNR 但增加内存开销，完整 GDAGS 在两者间取得最优平衡。

### 补充图表

![[assets/figures/papers/paper_list_l84_https_openreview_net_forum_id_6qDxK4Gz7F/figures/001_Figure_1.jpg]]
*Figure 1: (a) illustrates the Gaussian ellipsoid splatting process, where arrows of different colors represent the gradient direction and magnitude of different Gaussians on the pixels. (b) shows the densification process of different methods. In 3DGS, a large Gaussian covering many pixels may fail to split because the combined gradient magnitude from different pixels falls below the threshold, leading to over-reconstruction as shown in the Rendered part of (c), which manifests as blurry areas. AbsGS forces all Gaussian gradients to be positive, causing the combined gradient magnitude from different pixels to increase significantly. This results in a substantial rise in the number of splitting Gaussi...*

![[assets/figures/papers/paper_list_l84_https_openreview_net_forum_id_6qDxK4Gz7F/figures/011_Figure_7.jpg]]
*Figure 7: Corresponding curves of weights for different hyperparameters*

## 实验与分析

### 核心瓶颈与因果机制

3DGS的密度控制策略仅依赖视空间位置梯度的范数 $\nabla_{\mu_i} L$，完全忽略了梯度方向的分布特性。这一设计导致两类结构性缺陷：对于覆盖多纹理区域的大型高斯，尽管梯度范数足够大，但若子梯度方向高度冲突，原始策略倾向于克隆而非分裂，造成**过重建（under-reconstruction）**；而在梯度方向高度一致的区域，大量小高斯因范数持续超阈值而反复克隆，导致**过密化（over-densification）**与存储浪费。

GDAGS通过引入**梯度方向一致性比率（GCR）**作为因果调节旋钮，将密度决策从“梯度有多强”升级为“梯度方向是否冲突”。核心机制如下：

1. **GCR计算**（Equation 5）：对每个高斯 $i$，统计其覆盖像素上子梯度向量的方向一致性：
   $$\mathcal{C}_i = \frac{\|\sum_{pixel} \nabla_{i,pixel}^v\|_2}{\sum_{pixel} \|\nabla_{i,pixel}^v\|_2 + \epsilon}$$
   $\mathcal{C}_i \to 1$ 表示子梯度高度一致（高斯处于平滑表面），$\mathcal{C}_i \to 0$ 表示方向严重冲突（高斯跨越几何边界）。

2. **非线性动态权重映射**（Equation 6）：将GCR转化为每高斯的调制权重：
   $$w_i = \alpha + \beta \cdot (1 - \mathcal{C}_i)^p$$
   其中 $\alpha=0.8$ 抑制方向一致高斯的密度化冲动，$\beta=25$ 放大方向冲突高斯的响应，$p=15$ 的幂函数形式使得权重对 $\mathcal{C}_i$ 在接近0时高度敏感，在接近1时快速衰减。

3. **差异化调制**：分裂操作直接使用 $w_i$ 加权梯度范数 $\tilde{\nabla}_{\mu_i} L = w_i \cdot \nabla_{\mu_i} L$，优先分裂方向冲突的大型高斯；克隆操作采用逆策略 $1/w_i$，鼓励方向一致的小高斯沿表面传播，抑制方向不一致区域的无效增殖。

### 主要定量结果

Table 1汇总了GDAGS在三个标准基准上与3DGS及代表性变体的对比。所有实验采用与3DGS完全相同的训练设置（密度化每100次迭代启动，15k迭代后停止，30k迭代训练结束），超参数固定为 $\alpha=0.8, \beta=25, p=15$，未进行场景特定调优。

在Mip-NeRF360数据集上，GDAGS取得PSNR **28.02**（较3DGS提升+0.81），SSIM **0.839**，LPIPS **0.145**；在Tanks&Temples上，PSNR达**23.79**（+0.65）；在Deep Blending上，PSNR达**29.70**（+0.29）。值得注意的是，GDAGS在提升渲染质量的同时，内存占用普遍低于3DGS，且仅为**Pixel-GS**（Zhang et al., 2024c）的20%-50%，验证了方向感知密度控制对过密化的有效抑制。

与**AbsGS**（Ye et al., 2024）的对比尤为关键：AbsGS强制梯度方向均匀化，但缺乏对方向一致性的精细区分，GDAGS在所有指标上均取得更优结果，表明非线性动态权重比均匀化策略更有效。

### 消融实验

Table 2的消融实验揭示了各设计选择的贡献：

- **GDAGS-L**（线性权重 $w_i = 2 - \mathcal{C}_i$）：在所有三个数据集上性能显著劣于完整GDAGS，验证了幂函数形式对梯度方向冲突的敏感性和对一致性区域的抑制能力是线性函数无法替代的。
- **GDAGS-S**（仅分裂阶段加权）：有效提升SSIM和LPIPS，同时减少内存占用（Mip-NeRF360上仅441MB），说明优先分裂方向冲突的高斯直接改善了几何重建精度。
- **GDAGS-C**（仅克隆阶段加权）：提升PSNR但增加内存（615MB），表明鼓励方向一致区域的传播有助于覆盖更多细节，但缺乏对过密化的抑制会导致高斯数量膨胀。

完整GDAGS融合了两种策略的优势，在质量与效率之间取得最佳平衡。

### 超参数敏感性

Figure 4展示了指数幂 $p$ 的影响。$p$ 控制参与密度化的高斯比例：$p$ 增大时，权重函数对中等 $\mathcal{C}_i$ 值的抑制更强，限制密度化，减少内存但可能损失细节；$p$ 减小时则相反。$p=15$ 在所有数据集上取得最佳折衷。这一发现暗示幂函数形式天然提供了一种“软阈值”机制，无需为不同场景手动设定密度化阈值。

### 泛化性与效率

Table 3显示，将GDAGS的密度控制策略集成至**MCMC-3DGS**和**Compact-3DGS**后，两个基线在SSIM和LPIPS上均获得一致提升，验证了GCR导向的密度决策作为即插即用模块的通用性。

Table 4的效率分析表明，GDAGS的训练时间在三个数据集上均为最短（Mip-NeRF360: 1140s, Tanks&Temples: 555s, Deep Blending: 898s），这得益于更精准的密度控制减少了不必要的高斯增殖和后续修剪开销。Figure 5进一步显示，GDAGS在训练过程中的高斯数量轨迹比3DGS和AbsGS更稳定，收敛更快。

### 失败模式与边界条件

尽管GDAGS在标准基准上表现优异，但存在以下已知局限：

1. **超参数固定**：$p=15$ 在所有场景中统一使用，在梯度极度稀疏或噪声严重的场景下可能需要手动调优，缺乏自适应机制。
2. **GCR的稀疏梯度盲区**：当高斯覆盖的像素数极少或梯度幅值整体微弱时，GCR可能无法可靠区分真离群点与欠重建区域，存在欠密化或过度抑制的风险。
3. **Deep Blending的特殊行为**：在该简单场景上，GDAGS的原始性能略低于**Mini-splatting**（Fang & Wang, 2024），后者以更少的高斯数实现更优质量。通过引入dropout正则化（GDAGS-ODROP-5%）可超越Mini-splatting，表明简单场景下模型易过拟合，适当减少高斯数可进一步提升性能。这一现象提示：在低复杂度场景中，GCR引导的密度控制可能需要配合显式的稀疏化正则。

### 关键图表结论速查

- **Table 1**：GDAGS在三个数据集上全面超越3DGS，内存仅为Pixel-GS的20%-50%。
- **Table 2**：非线性权重 > 线性权重；分裂加权提升几何质量，克隆加权提升覆盖但增加内存。
- **Figure 4**：$p=15$ 为最优折衷，幂函数提供天然的软阈值行为。
- **Figure 5**：GDAGS的高斯数量轨迹更稳定，收敛更快。
- **Table 3**：GDAGS策略可泛化至MCMC-3DGS和Compact-3DGS，验证模块化设计。
- **Table 4**：GDAGS训练时间最短，效率优势明显。

![[assets/figures/papers/paper_list_l84_https_openreview_net_forum_id_6qDxK4Gz7F/figures/003_Table_1.jpg]]
*Table 1: Quantitative comparison on three datasets. SSIM↑ and PSNR↑ are higher-the-better; LPIPS↓ is lower-the-better. For fair comparison and to balance the trade-off between overall quality and memory consumption, we train these datasets with the same settings as 3DGS. All methods use the same training data for training. The best score , second best score are red and orange, respectively*

![[assets/figures/papers/paper_list_l84_https_openreview_net_forum_id_6qDxK4Gz7F/figures/005_Table_2.jpg]]
*Table 2: Ablation experiment on three datasets. SSIM↑ and PSNR↑ are higher-the-better; LPIPS↓ is lower-the-better. The best score , and second best score are red, and orange, respectively*

![[assets/figures/papers/paper_list_l84_https_openreview_net_forum_id_6qDxK4Gz7F/figures/006_Figure_4.jpg]]
*Figure 4: Performance of different hyperparameters p in multiple datasets*

![[assets/figures/papers/paper_list_l84_https_openreview_net_forum_id_6qDxK4Gz7F/figures/007_Figure_5.jpg]]
*Figure 5: Visualization of different densification methods during the training process in bicycle sense*

![[assets/figures/papers/paper_list_l84_https_openreview_net_forum_id_6qDxK4Gz7F/figures/008_Table_3.jpg]]
*Table 3: Generalization analysis on three datasets. SSIM↑ and PSNR↑ are higher-the-better; LPIPS↓ is lower-the-better. The best score is red*

![[assets/figures/papers/paper_list_l84_https_openreview_net_forum_id_6qDxK4Gz7F/figures/010_Table_4.jpg]]
*Table 4: Efficiency analysis of GDAGS and baseline models. TT(s) in the table represents training time (in seconds). The best score is red*

### 补充图表

![[assets/figures/papers/paper_list_l84_https_openreview_net_forum_id_6qDxK4Gz7F/figures/009_Figure_6.jpg]]
*Figure 6: Qualitative analysis of GDAGS integrated in MCMC-3DGS and Compact-3DGS*

![[assets/figures/papers/paper_list_l84_https_openreview_net_forum_id_6qDxK4Gz7F/figures/004_Figure_3.jpg]]
*Figure 3: Qualitative comparisons of different methods on scenes from Mip-NeRF360, Tanks&Temples and Deep Blending datasets. Enlarged images are displayed in the bottom right corner*

![[assets/figures/papers/paper_list_l84_https_openreview_net_forum_id_6qDxK4Gz7F/figures/018_Figure_11.jpg]]
*Figure 11: Qualitative results of GDAGS and baseline models in sparse views*

## 方法谱系与知识库定位

### 与基线方法的关系

GDAGS 的核心改进对象是 **3DGS**（Kerbl et al., SIGGRAPH 2023）的密度控制策略。3DGS 的密度化决策仅依赖视空间位置梯度的范数 $\nabla_{\mu_i} L$，当梯度范数超过阈值时，根据高斯的尺度大小选择分裂或克隆。这一机制存在两个结构性缺陷：大型高斯因梯度范数被平均化而难以触发分裂（过重建），方向一致区域的高斯则因梯度持续累积而过度增殖（过密化）。GDAGS 通过引入梯度方向一致性比率（GCR）和非线性动态权重函数，对每个高斯的梯度范数进行方向感知调制，从根本上修正了这两个问题。

在与 3DGS 变体的对比中，GDAGS 展现出差异化的改进路径：

- **Pixel-GS**（Zhang et al., 2024）采用基于覆盖度的权重策略来替代梯度范数，虽然有效抑制了过密化，但以显著增加内存开销为代价。GDAGS 在相近或更优的渲染质量下，内存消耗仅为 Pixel-GS 的 20%–50%（Table 1），体现了方向感知调制在效率上的优势。

- **AbsGS**（Ye et al., 2024）强制统一梯度方向以增强一致性，但缺乏对方向冲突高斯的差异化处理。GDAGS 的 GCR 机制天然区分方向一致与冲突的高斯，并在分裂和克隆阶段采用非对称策略——分裂时放大冲突高斯的权重以优先分解，克隆时采用逆权重 $1/w_i$ 以抑制不一致区域的增殖（Section 4）。这种差异化调制是 AbsGS 所不具备的。

- **Taming 3DGS**（Mallick et al., 2024）和 **mini-splatting**（Fang & Wang, 2024）分别从不同角度优化高斯表示，前者关注训练稳定性，后者追求紧凑表示。GDAGS 的策略具有正交性：消融实验显示，将 GDAGS 的密度控制策略集成到 **MCMC-3DGS** 和 **Compact-3DGS** 中，均能一致性地提升 SSIM 和 LPIPS（Table 3, Figure 6），表明方向感知密度控制是一个可泛化的改进模块，而非与特定框架紧耦合。

在与 NeRF 类方法的对比中，GDAGS 在 Mip-NeRF360 数据集上达到 28.02 PSNR，显著优于 **Mip-NeRF360**（Barron et al., 2022）等 NeRF 基线，同时保持了 3DGS 的实时渲染优势（Table 4，训练时间 1140s，FPS 保持竞争力）。

### 适用边界

GDAGS 的核心假设是：每个高斯能够接收到来自多个像素的充分梯度信息，使得 GCR 能够可靠地区分方向一致与冲突的高斯。这一假设在以下场景中可能被削弱：

1. **极度稀疏视图场景**：当训练视角数量极少时，每个高斯仅被少量像素覆盖，GCR 的统计可靠性下降。论文虽然在稀疏视图对比（Figure 11）中展示了定性改善，但尚未系统量化 GCR 在极端稀疏条件下的失效边界。

2. **梯度极度稀疏的区域**：在场景的远距离或低纹理区域，高斯可能仅接收到微弱且稀疏的梯度信号。此时 GCR 难以区分真离群点（需要抑制的高斯）与欠重建区域（需要更多高斯），存在欠密化或过度抑制的风险。这一边界条件需要手动验证。

3. **简单场景的过拟合倾向**：在 Deep Blending 数据集上，GDAGS 的原始性能略低于 mini-splatting（后者使用更少的高斯数）。论文通过引入 dropout 正则化（GDAGS-ODROP-5%）可超越 mini-splatting，表明在简单场景中，GDAGS 的密度控制策略可能产生冗余高斯，需要额外的正则化手段来抑制过拟合。

### 局限与开放问题

**已识别的局限：**

1. **超参数 p 缺乏自适应性**：指数幂 $p=15$ 控制参与密度化的高斯比例（Figure 4），增大 $p$ 限制密度化、减少内存但可能降低质量，减小 $p$ 则相反。$p=15$ 是经验最优值，在特定数据集或硬件配置下可能需要手动调优，缺乏自动适应机制。

2. **权重函数的固定参数化**：$\alpha=0.8$ 和 $\beta=25$ 在所有实验中固定，未探索场景自适应调整的可能性。在梯度分布差异极大的场景间，固定的抑制因子和放大因子可能不是最优的。

3. **GCR 的数值稳定性依赖**：GCR 计算公式 $\mathcal{C}_i = \frac{\| \sum_{pixel} \nabla_{i,pixel}^v \|_2}{\sum_{pixel} \| \nabla_{i,pixel}^v \|_2 + \epsilon}$ 中 $\epsilon$ 的选取影响数值稳定性，论文未讨论 $\epsilon$ 的敏感性。

**开放问题：**

1. **非线性权重函数的理论性质**：权重函数 $w_i = \alpha + \beta \cdot (1 - \mathcal{C}_i)^p$ 的导数 $f'(x) = p[e^{-px} - (1-x)^{p-1}]$ 的零点 $x_0$ 随 $p$ 的增大如何变化？是否存在解析解，能够为 $p$ 的自适应调整提供理论指导？

2. **Dropout 正则化的具体机制**：GDAGS-ODROP-5% 的具体 dropout 概率或调度策略未在论文中详细说明。该正则化如何在训练过程中动态调整，以及是否可推广到其他简单场景，需要进一步研究。

3. **稀疏视图场景的量化评估**：在稀疏视图对比中，能否引入量化指标（如边缘保持指数）以更客观地评估 GDAGS 对几何边界的改善，而非仅依赖定性可视化？

4. **自适应参数调整**：GDAGS 的权重函数是否可以在训练过程中自适应调整参数 $p$ 和 $\beta$，例如根据当前迭代的高斯数量轨迹或梯度分布统计量动态调节，从而消除手动调参的需要？

## 原文 PDF

![[paperPDFs/ICLR_2026/Gradient_Direction_Aware_Density_Control_for_3D_Gaussian_Splatting_c387d81038ca.pdf]]