---
title: "Seele: A Unified Acceleration Framework for Real-Time Gaussian Splatting on Mobile Devices"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/Seele_A_Unified_Acceleration_Framework_for_Real_Time_Gaussian_Splatting_on_Mobile_Devices.pdf
project_link: "http://seele-project.netlify.app"
code_link: null
aliases:
- Seele
tags:
- CVPR_2026
- topic/other_unclear
- topic/other_unclear/general
core_operator: 视角相关的场景表示将高斯点分为共享和独占集群，运行时仅加载相关集群，结合贡献感知光栅化动态跳过低贡献高斯点的颜色混合计算，从而大幅减少计算量和内存占用。
primary_logic: 不同视角仅共享小部分高斯点，且极少数（约1.5%）高斯点贡献了99%的最终像素颜色，因此可以安全地剔除不相关和低贡献的高斯点，在几乎不影响渲染质量的前提下实现数倍加速。
claims:
- 1.5% 的 top 高斯点贡献了 99% 的最终像素透明度
- 混合预处理（HP）单独实现 2.8× 加速并提升渲染质量
- 贡献感知光栅化（CR）额外提供 1.4× 加速，且质量损失极小
- 整体框架 SEELE 在现有 3DGS 算法上实现最高 6.3× 加速和 39.1% 运行时模型缩减
---

# Seele: A Unified Acceleration Framework for Real-Time Gaussian Splatting on Mobile Devices

> [!tip] 核心洞察
> 不同视角仅共享小部分高斯点，且极少数（约1.5%）高斯点贡献了99%的最终像素颜色，因此可以安全地剔除不相关和低贡献的高斯点，在几乎不影响渲染质量的前提下实现数倍加速。

| 字段 | 内容 |
|------|------|
| 中文题名 | SEELE：面向移动设备的实时高斯泼溅统一加速框架 |
| 英文题名 | Seele: A Unified Acceleration Framework for Real-Time Gaussian Splatting on Mobile Devices |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://openaccess.thecvf.com/content/CVPR2026/html/Zhu_Seele_A_Unified_Acceleration_Framework_for_Real-Time_Gaussian_Splatting_on_CVPR_2026_paper.html) · [Project](http://seele-project.netlify.app) |
| Topic | #topic/other_unclear #topic/other_unclear/general |
| Method | SEELE |
| Dataset | 综合（Mip-NeRF360 / Tanks&Temples / DeepBlending）, Mip-NeRF360（平均值） |

> [!tip] 效果简介
> - 综合（Mip-NeRF360 / Tanks&Temples / DeepBlending） 上，加速比（FPS） SEELE on 3DGS: 3.2× vs 3DGS: 1.0× (+2.2×)。
> - 综合（同上） 上，加速比（FPS） SEELE on LightGaussian: 2.7× vs LightGaussian: 1.0× (+1.7×)；运行时模型大小缩减 39.1% 缩减 vs 基线模型大小（不变） (减少 39.1%)。
> - Mip-NeRF360（平均值） 上，PSNR 提升 SEELE 平均 PSNR 提高约 0.28 dB vs 各基线原始 PSNR (+0.28 dB)。

## 概要

移动设备上实时渲染高质量3D场景是增强现实与移动端视觉应用的核心需求。3D高斯泼溅（3D Gaussian Splatting, 3DGS）虽能以高质量实时渲染静态场景，但其渲染管线在移动端GPU上面临严峻挑战：每个像素需处理数千个高斯点，且管线统一对待所有高斯点进行透明度计算与颜色混合，导致大量计算浪费和GPU内存占用过高。

本文提出 **SEELE**，一个面向移动设备的统一加速框架。其核心洞察来自两个关键实证发现：（1）不同视角间仅共享少量高斯点，绝大多数高斯点仅对特定视角区域有贡献；（2）极少数（约1.5%）的高斯点贡献了最终像素99%的透明度（Fig. 4）。基于此，SEELE从两个维度重构3DGS渲染管线：

- **混合预处理（Hybrid Preprocessing）**：构建视角相关的场景表示，将高斯点离线聚类为共享集群和独占集群；运行时仅加载当前视角相关集群，结合在线不透明度感知过滤，大幅减少参与后续计算的高斯点数量，同时将运行时模型大小缩减39.1%。
- **贡献感知光栅化（Contribution-Aware Rasterization）**：在光栅化阶段动态识别低贡献高斯点并跳过其颜色混合计算，缓解GPU warp发散问题，提升并行效率。

在Nvidia AGX Orin移动设备上，SEELE在多个主流3DGS变体（包括原始3DGS、LightGaussian、Mini-Splatting、AdR-Gaussian）上实现最高6.3×加速，同时平均PSNR提升约0.28 dB、SSIM提升约0.004。消融实验表明，混合预处理单独贡献2.8×加速，贡献感知光栅化额外提供约1.3×加速。

### 方法谱系与知识库定位

SEELE属于3DGS推理加速方法族，与现有工作的关键区别在于：

| 维度 | 现有方法 | SEELE |
|------|----------|-------|
| **预处理过滤** | 视锥体裁剪 + 3σ包络交集测试（均匀对待所有高斯点） | 离线视角相关聚类 + 在线不透明度感知细粒度过滤（Eq. 5） + 异步场景预取 |
| **光栅化计算** | 每像素线程对瓦片内所有高斯点执行完整颜色混合 | 像素分组，组内领头像素判定贡献度，跳过低贡献高斯点的颜色混合（Algorithm 1） |
| **GPU内存管理** | 所有高斯点常驻GPU内存 | 仅保留共享高斯点与当前视角相关集群，异步预取未来集群 |

与基于剪枝或量化的压缩方法（如LightGaussian）不同，SEELE不修改高斯点数量或精度，而是通过动态选择性计算实现加速，因此可正交叠加于现有压缩技术之上。与**AdR-Gaussian**（Wang et al., SIGGRAPH Asia 2024）等视角自适应方法相比，SEELE的混合预处理将离线聚类与在线过滤解耦，避免了逐帧重聚类开销，更适合移动端实时场景。

**局限与开放问题**：当前方法依赖线性外推相机姿态进行场景预取，在非平滑运动下可能失效；仅在Nvidia Orin系列移动GPU上验证，其他移动平台（如Qualcomm Adreno、Apple GPU）的适用性未知；离线聚类需逐场景执行，不适用于跨场景通用模型。此外，极端视角下聚类效率的退化程度、与高斯点剪枝/量化技术的正交叠加潜力，以及在更大规模城市场景中的扩展性，仍有待进一步探索。



### 3D 高斯泼溅与移动端实时渲染的困境

3D 高斯泼溅（3D Gaussian Splatting, 3DGS）凭借其显式点云表示和可微光栅化管线，在逼真新视角合成上实现了前所未有的速度与质量平衡。然而，这一高效性在移动端设备上迅速瓦解：移动 GPU 的计算能力与内存带宽远逊于桌面级硬件，而 3DGS 渲染管线需要对每个像素处理数千个高斯点，且统一对待所有高斯点，导致大量计算浪费和内存占用过高。

具体而言，3DGS 的颜色累积过程可表述为：

$$C ( \mathbf { p } ) = \sum _ { i = 1 } ^ { N } \Gamma _ { i } \alpha _ { i } \mathbf { c } _ { i } , { \mathrm { ~ w h e r e ~ } } \Gamma _ { i } = \prod _ { j = 1 } ^ { i - 1 } ( 1 - \alpha _ { j } )$$

其中每个高斯的透明度 $\alpha_i$ 由其不透明度 $o_i$、2D 位置 $x'$ 和协方差 $\Sigma'$ 共同决定：

$$\alpha _ { i } = o _ { i } e ^ { - \frac 1 2 ( { \bf p } - x ^ { \prime } ) ^ { T } \Sigma ^ { \prime - 1 } ( { \bf p } - x ^ { \prime } ) }$$

在标准实现中，每个像素线程需要对同一瓦片内所有高斯点依次计算透明度并执行颜色混合，且所有高斯点常驻 GPU 内存。这一“均匀计算”策略在移动端造成双重瓶颈：**计算端**，大量对最终像素颜色贡献微乎其微的高斯点仍消耗着宝贵的 GPU 周期；**内存端**，完整模型权重占据的显存远超移动设备的承受能力。

### 现有加速方案的缺口

针对上述瓶颈，现有工作主要沿两条路径展开：一是通过剪枝、量化等手段压缩模型本身（如 LightGaussian、Mini-Splatting），二是通过代码优化提升 GPU 利用率。然而，这些方法存在根本性局限——它们未触及 3DGS 渲染管线的两个关键特性：

1. **视角相关冗余**：不同视角仅共享小部分高斯点，绝大多数高斯点仅对特定视角区域有贡献。现有方法在运行时仍将所有高斯点驻留内存并参与计算，未能利用这一视角稀疏性。
2. **贡献极度不均**：实证分析表明，仅约 1.5% 的 top 高斯点贡献了 99% 的最终像素透明度（Fig. 4），而现有光栅化管线对所有高斯点一视同仁地执行完整的颜色混合计算，导致显著的 GPU warp 发散和算力浪费。

### 本文动机与核心思路

基于上述观察，本文提出 **SEELE**——一个面向移动设备的统一加速框架，其核心洞察是：**可以安全地剔除不相关和低贡献的高斯点，在几乎不影响渲染质量的前提下实现数倍加速**。

SEELE 从两个维度重构 3DGS 渲染管线：在预处理阶段，设计视角相关的场景表示，将高斯点划分为共享集群和独占集群，运行时仅加载相关集群，从源头削减计算量和内存占用；在光栅化阶段，引入贡献感知光栅化算法，动态识别并跳过低贡献高斯点的颜色混合计算，提升 GPU 并行效率。这一“预处理过滤 + 光栅化跳跃”的组合策略，使得 SEELE 能够以统一框架加速多种 3DGS 变体，在移动端实现最高 6.3× 的渲染加速和 39.1% 的运行时模型缩减。



## 核心方法与创新机理

SEELE 的核心创新在于重新设计了 3DGS 渲染管线中的两个关键环节——预处理与光栅化，通过**视角相关的场景表示**和**贡献感知的计算调度**，在不牺牲渲染质量的前提下大幅降低移动端 GPU 的计算与内存压力。其相对于原始 3DGS（Kerbl et al., ACM TOG 2023）的 changed slots 可归纳为三个维度。

### 预处理阶段：从“粗粒度裁剪”到“混合预处理”

原始 3DGS 的预处理仅依赖视锥体裁剪和基于 3σ 包络的瓦片交集测试，所有通过测试的高斯点均被送入后续光栅化，缺乏对高斯点实际贡献度的区分。SEELE 的**混合预处理（Hybrid Preprocessing）** 将这一过程重构为离线-在线协同的两级过滤机制：

1. **离线视角相关场景聚类**：将场景高斯点划分为跨视角共享的“共享高斯点”和仅服务于特定视角簇的“独占高斯点”（Fig. 3）。渲染时仅加载共享高斯点与当前视角所在簇的独占高斯点，其余集群通过异步预取按需加载。这一设计直接改变了 GPU 内存管理策略——从“所有高斯点常驻 GPU 内存”变为“仅保留相关子集”，实现 **39.1% 的运行时模型缩减**。

2. **在线基于不透明度的细粒度过滤**：传统交集测试使用固定阈值（3σ 包络）判定高斯点是否与瓦片相交，但忽略了高斯点自身不透明度对最终颜色的实际影响。SEELE 将不透明度 $o_i$ 纳入过滤方程：

   $$\sqrt{ (\mathbf{p} - x_i')^T \Sigma_i'^{-1} (\mathbf{p} - x_i') } = \sqrt{ 2 \ln \frac{ o_i }{ \alpha_\theta } }$$

   并在实际实现中取与 9 的较小值以消除瓦片交集误报：

   $$( \mathbf{p} - x_i' )^T \Sigma_i'^{-1} ( \mathbf{p} - x_i' ) = \min( 2 \ln \frac{ o_i }{ \alpha_\theta }, 9 )$$

   这意味着低不透明度的高斯点即使空间位置与瓦片相交，也会被提前剔除，从而减少进入光栅化阶段的高斯点总数。

消融实验（Table 4）表明，混合预处理（+HP）在代码优化（+Opti.）基础上额外贡献 **2.8× 加速**，并平均提升 PSNR 0.23 dB——这源于过滤掉噪声高斯点后渲染质量的净提升。

### 光栅化阶段：从“均匀计算”到“贡献感知光栅化”

原始 3DGS 的光栅化对同一瓦片内的每个像素线程执行完全相同的计算：对所有相交高斯点依次计算透明度并执行颜色混合。这一“均匀计算”策略忽视了不同高斯点对最终像素颜色的贡献差异。SEELE 的**贡献感知光栅化（Contribution-Aware Rasterization）** 基于一个关键实证发现（Fig. 4）：**仅约 1.5% 的 top 高斯点贡献了 99% 的最终像素透明度**，且高贡献高斯点集中于高频区域，低贡献高斯点多分布于低频区域。

基于此，SEELE 将像素分组处理：每组内仅领头像素完整计算透明度以判定该高斯点是否“显著”，其余像素在判定为“不显著”时直接跳过该高斯点的颜色混合计算（Algorithm 1）。这一策略同时缓解了 GPU warp 发散问题——当 warp 内所有线程遇到低贡献高斯点时，可统一跳过颜色混合，避免“lockstep”执行中的空闲等待（Fig. 5）。

消融实验（Table 4）显示，贡献感知光栅化（+CR）在 +Opti. 基础上额外提供 **1.3× 加速**，且对 PSNR 的影响极小（仅 0.03 dB 下降），验证了“安全剔除低贡献高斯点”的核心假设。

### 质量补偿机制：集成微调

SEELE 引入**集成微调（Integrated Fine-Tuning）**，结合原始 3DGS 损失与视图一致性损失：

$$\mathcal { L } _ { total } = \mathcal { L } _ { 3DGS } + \gamma * \mathcal { L } _ { consistency }, \quad \gamma = 0.1$$

其中视图一致性损失使用 7 帧 FLIP 分数度量。消融实验（Table 6）表明，该损失将 FLIP 指标从 0.060 降至 0.058，有效补偿了加速带来的时序闪烁等质量退化。

### 关键超参数与敏感性

三个关键超参数的敏感性分析为实际部署提供了指导：
- **像素组大小**：2×2 在质量与性能间取得最佳平衡，过大组会导致质量显著下降（Fig. 7）。
- **聚类数与邻居数**：需根据场景复杂度调整，论文给出了不同配置下的质量-性能 trade-off（Fig. 6）。
- **贡献者数量**：控制贡献感知光栅化中判定“显著”的阈值，直接影响剔除率与质量损失（Fig. 8）。

### 创新边界与未验证假设

需注意以下创新边界仍需人工验证：
- 离线聚类和共享/独占高斯点划分需针对每个场景单独执行，不适用于单次训练跨多场景的通用模型。
- 场景预取依赖线性外推相机姿态，在非平滑运动（如快速旋转）下可能失效，论文未对此进行实验验证。
- 贡献感知光栅化中的像素组机制是否可适配其他基于图块的渲染管线（如 Instant NGP）仍是开放问题。
- 该方法能否与高斯点剪枝、量化等正交压缩技术叠加获得更高加速，论文未进行组合实验。



SEELE 是一个面向移动端 3DGS 渲染的统一加速框架，其核心设计围绕一个关键发现展开：不同视角之间仅共享极少部分高斯点，且约 **1.5% 的高斯点贡献了 99% 的最终像素透明度**（Fig. 4）。基于这一洞察，SEELE 对原始 3DGS 渲染管线的两个阶段——预处理与光栅化——进行了系统性改造，提出了 **混合预处理（Hybrid Preprocessing）** 与 **贡献感知光栅化（Contribution-Aware Rasterization）** 两项核心技术，整体框架如 Fig. 2 所示。

![[assets/figures/papers/paper_list_l2266_https_openaccess_thecvf_com_content_CVPR2026_html_Zhu_Seele_A_Unified_Ac/figures/002_Figure_2.jpg]]
*Figure 2: The overview of SEELE. we modify the two steps, preprocessing and rasterization, and propose two novel techniques: hybrid preprocessing and contribution-aware rasterization, in Gaussian splatting. Hybrid preprocessing leverages offline coarse-grained scene clustering and online filtering to reduce the number of Gaussians before rasterization. Contribution-aware rasterization dynamically identifies insignificant Gaussians and skips them to accelerate the overall rendering pipeline*

### 管线流程

SEELE 的完整渲染管线由以下模块串联构成：

1. **离线场景聚类**：对训练好的 3DGS 场景进行视角相关的聚类分析，将高斯点划分为跨视角共享的“共享高斯点”和仅属于特定视角簇的“独占高斯点”（Fig. 3）。这一划分是后续运行时内存缩减和计算跳过的结构基础。

2. **混合预处理（HP）**：运行时结合离线聚类结果与在线细粒度过滤。在线过滤将高斯点的不透明度 $o_i$ 纳入瓦片交集测试，通过公式

   $$( \mathbf{p} - x_i' )^T \Sigma_i'^{-1} ( \mathbf{p} - x_i' ) = \min\left( 2 \ln \frac{ o_i }{ \alpha_\theta }, 9 \right)$$

   消除传统 $3\sigma$ 包络测试中的误报高斯点，仅保留对当前视角有实际贡献的高斯点进入后续光栅化阶段。同时，**场景预取（Scene Prefetching）** 机制仅将共享高斯点与当前视角相关集群加载至 GPU 内存，并异步预取未来集群，从而实现 **39.1% 的运行时模型缩减**，预取延迟开销小于总延迟的 6%。

3. **贡献感知光栅化（CR）**：在光栅化阶段，将像素分组（如 $2\times2$），每组仅由领头像素计算每个高斯点的透明度 $\alpha_i$。若某高斯点对领头像素的贡献低于阈值，则判定为“非显著高斯点”，整组像素跳过其颜色混合计算（Algorithm 1）。这一机制缓解了 GPU warp 内线程因条件分支导致的发散问题（Fig. 5），提升并行效率。

4. **集成微调（Integrated Fine-Tuning）**：为补偿加速带来的渲染质量下降，SEELE 引入结合原始 3DGS 损失与视图一致性损失的总损失函数

   $$\mathcal{L}_{total} = \mathcal{L}_{3DGS} + \gamma \cdot \mathcal{L}_{consistency}, \quad \gamma=0.1$$

   对场景进行微调，在保持加速收益的同时恢复甚至提升渲染质量。

### 模块间关系与数据流

混合预处理与贡献感知光栅化在加速机制上形成互补：HP 在光栅化之前大幅削减参与计算的高斯点数量，降低 GPU 计算与内存压力；CR 则在剩余高斯点中进一步动态识别并跳过低贡献者，提升 GPU 利用率。消融实验（Table 4）表明，在代码优化（+Opti.）基础上，HP 单独带来 **2.8× 加速**并平均提升 PSNR 0.23 dB，CR 额外提供 **1.3× 加速**且质量损失极小（PSNR 下降仅 0.03 dB），完整 SEELE（+Opti.+HP+CR）实现 **3.2× 整体加速**。

### 适用范围

SEELE 作为统一加速框架，可应用于多种 3DGS 变体。在相同 Nvidia AGX Orin 移动设备上，SEELE 对 **3DGS**（Kerbl et al., ACM TOG 2023）实现 3.2× 加速，对 **LightGaussian** 实现 2.7× 加速，对 **AdR-Gaussian**（Wang et al., SIGGRAPH Asia 2024）实现 1.7× 加速，对 **Mini-Splatting** 实现 1.8× 加速，展现出良好的算法无关性。



### 1. 问题定义：3DGS 渲染的累积瓶颈

3DGS 的渲染核心是沿光线按深度排序后，对每个像素 $\mathbf{p}$ 执行颜色累积：

$$C ( \mathbf { p } ) = \sum _ { i = 1 } ^ { N } \Gamma _ { i } \alpha _ { i } \mathbf { c } _ { i } , \quad \text{其中} \quad \Gamma _ { i } = \prod _ { j = 1 } ^ { i - 1 } ( 1 - \alpha _ { j } ) \tag{1}$$

其中 $\alpha_i$ 是高斯点 $i$ 在像素 $\mathbf{p}$ 处的透明度，由其不透明度 $o_i$ 和 2D 投影后的马氏距离决定：

$$\alpha _ { i } = o _ { i } \, e ^ { - \frac 1 2 ( { \bf p } - x ^ { \prime } ) ^ { T } \Sigma ^ { \prime - 1 } ( { \bf p } - x ^ { \prime } ) } \tag{2}$$

$x'$ 和 $\Sigma'$ 分别是高斯点在图像平面的投影中心和 2D 协方差矩阵。

**瓶颈**：原始管线对每个像素-瓦片对内的所有高斯点统一执行式 (1)-(2) 的完整计算。移动端 GPU 面临双重压力——(a) 内存：所有高斯点常驻 GPU 显存；(b) 计算：大量高斯点对最终颜色的贡献近乎为零，却消耗了等量的计算资源。实证分析表明，仅 **1.5% 的高贡献高斯点贡献了 99% 的最终像素透明度**（Fig. 4），这意味着超过 98% 的高斯点在颜色混合中的计算是冗余的。

### 2. 混合预处理：离线聚类 + 在线过滤

SEELE 在预处理阶段引入“离线粗分 + 在线精筛”的两级策略，目标是在光栅化之前大幅削减参与计算的高斯点数量。

**离线视角相关场景聚类**：将场景高斯点划分为**共享高斯点**和**独占高斯点**。共享高斯点对所有视角可见，常驻 GPU 内存；独占高斯点按视角贡献度聚类为若干集群（Fig. 3）。运行时仅加载当前视角对应的独占集群，其余集群通过异步预取按需换入，实现 **39.1% 的运行时模型大小缩减**（延迟开销 < 6%）。

**在线基于不透明度的细粒度过滤**：传统瓦片交集测试使用 $3\sigma$ 包络（马氏距离 = 3）判定高斯点是否覆盖像素。但该判据忽略了不透明度 $o_i$——一个 $o_i$ 极低的高斯点即使几何上覆盖像素，其实际贡献也可忽略。SEELE 将 $o_i$ 纳入交集方程：

$$\sqrt{ ( \mathbf{p} - x_i' )^T \Sigma_i'^{-1} ( \mathbf{p} - x_i' ) } = \sqrt{ 2 \ln \frac{ o_i }{ \alpha_\theta } } \tag{4}$$

其中 $\alpha_\theta$ 是透明度阈值。当 $o_i < \alpha_\theta$ 时，右侧无实数解，该高斯点被直接剔除。最终使用的过滤形式为：

$$( \mathbf{p} - x_i' )^T \Sigma_i'^{-1} ( \mathbf{p} - x_i' ) = \min\left( 2 \ln \frac{ o_i }{ \alpha_\theta }, 9 \right) \tag{5}$$

其中 $9 = 3^2$ 对应传统 $3\sigma$ 包络上界。式 (5) 同时消除了低不透明度高斯点（通过 $2\ln(o_i/\alpha_\theta)$ 项）和几何上不覆盖瓦片的高斯点（通过 $\min(\cdot, 9)$ 截断），有效消除瓦片交集的误报。

### 3. 贡献感知光栅化：动态跳过低贡献计算

光栅化阶段，GPU 以 warp 为单位对瓦片内所有高斯点执行“透明度计算 → 颜色混合”的锁步操作。当 warp 内某些线程对应的高斯点贡献极低时，这些线程仍需等待其他线程完成颜色混合，造成 warp 发散（Fig. 5）。

![[assets/figures/papers/paper_list_l2266_https_openaccess_thecvf_com_content_CVPR2026_html_Zhu_Seele_A_Unified_Ac/figures/005_Figure_5.jpg]]
*Figure 5: An example of warp divergence in GPU. All threads compute α and then perform color blending in “lockstep”. Our algorithm can detect the insignificant Gaussians (e.g., Gaussian A) and skip their color blending, as highlighted by the red cross*

SEELE 的**贡献感知光栅化**将像素分组（默认 $2 \times 2$），每组仅由领头像素计算透明度 $\alpha_i$，并依据 $\alpha_i$ 判定该高斯点对整组像素的贡献是否可忽略。若 $\alpha_i$ 低于阈值，则整组像素跳过该高斯点的颜色混合计算。这一机制带来双重收益：(a) 直接减少颜色混合的计算量；(b) 缓解 warp 发散——低贡献高斯点不再阻塞高贡献高斯点的处理，提升 GPU 并行效率。

### 4. 集成微调：补偿加速引入的质量损失

混合预处理和贡献感知光栅化本质上是有损加速——过滤和跳过高斯点会引入微小的渲染误差。SEELE 通过一个轻量微调阶段补偿质量下降，损失函数为：

$$\mathcal { L } _ { total } = \mathcal { L } _ { 3DGS } + \gamma * \mathcal { L } _ { consistency }, \quad \gamma = 0.1 \tag{6}$$

其中 $\mathcal{L}_{3DGS}$ 是原始 3DGS 的 L1 + SSIM 损失，$\mathcal{L}_{consistency}$ 是视图一致性损失，使用 7 帧 FLIP 分数度量相邻视角间的渲染一致性。该微调直接作用于 SEELE 加速管线，而非先训练后加速的两阶段范式，避免了分布偏移问题。

### 补充图表

![[assets/figures/papers/paper_list_l2266_https_openaccess_thecvf_com_content_CVPR2026_html_Zhu_Seele_A_Unified_Ac/figures/003_Figure_3.jpg]]
*Figure 3: Our scene representation clusters Gaussians into shared ones and exclusive ones. Here, we show the Gaussian positions without scales. The yellow points in Fig. 3b represent the shared Gaussians, while the other colors correspond to the exclusive Gaussians in different clusters*



## 实验与关键发现

### 整体加速与质量表现

SEELE 在三个标准数据集（Mip-NeRF360、Tanks&Temples、DeepBlending）上对四种 3DGS 变体进行加速，所有实验均在 Nvidia AGX Orin 移动 GPU 上完成。核心结果如 Table 1 所示：SEELE 在原始 **3DGS**（Kerbl et al., ACM TOG 2023）上实现 **3.2×** 加速，在 **LightGaussian**、**Mini-Splatting** 和 **AdR-Gaussian**（Wang et al., SIGGRAPH Asia 2024）上分别实现 2.7×、1.8× 和 1.7× 加速。3DGS 上加速比最高，原因在于其高斯点更稠密，SEELE 的视角相关聚类能更有效地分离不同视角的不相关高斯点。

![[assets/figures/papers/paper_list_l2266_https_openaccess_thecvf_com_content_CVPR2026_html_Zhu_Seele_A_Unified_Ac/figures/006_Table_1.jpg]]
*Table 1: Quantitative evaluation of our method against the state-of-the-arts [9, 10, 25, 49]. The bold green results highlight the better results between ours, SEELE, and the corresponding baselines. SEELE achieves better quality across all three quality metrics with an average 2.4× speedup. and denote the best and second-best results among all methods, respectively*

质量方面，SEELE 在 Mip-NeRF360 上平均 PSNR 提升约 **0.28 dB**，SSIM 提升约 **0.004**。这一质量提升部分源于集成微调（Sec. 3.5）的额外训练，因此与未经过类似微调的基线比较时需谨慎解读。此外，SEELE 将运行时 GPU 内存中的高斯模型大小缩减 **39.1%**，这是场景预取机制的直接效果。

**Table 1** 展示了各数据集上 SEELE 与基线的详细对比，绿色加粗标注了 SEELE 与对应基线之间的更优结果。

### 视图一致性与跨 GPU 泛化

视图一致性评估（Table 2）使用 FLIP 指标在 Mip-NeRF360 上进行。SEELE 在 FLIP1 和 FLIP7 上均取得更低（更优）的值，验证了集成微调中视图一致性损失的有效性——该损失将 FLIP 指标从 0.060 降至 0.058。

![[assets/figures/papers/paper_list_l2266_https_openaccess_thecvf_com_content_CVPR2026_html_Zhu_Seele_A_Unified_Ac/figures/007_Table_2.jpg]]
*Table 2: The view consistency metrics on Mip-NeRF360*

跨 GPU 实验（Table 3）在 Nvidia Orin NX（低功耗）和 Nvidia A6000（桌面级）上进行。SEELE 在两类设备上均保持加速优势，表明框架不局限于单一移动 GPU，但论文未在 Qualcomm Adreno 或 Apple GPU 等非 Nvidia 平台上验证。

![[assets/figures/papers/paper_list_l2266_https_openaccess_thecvf_com_content_CVPR2026_html_Zhu_Seele_A_Unified_Ac/figures/008_Table_3.jpg]]
*Table 3: The performance (FPS) over other GPUs: a low-power GPU on Nvidia Orin NX [2] and Nvidia A6000 [1]*

### 消融实验：各模块贡献

Table 4 以 3DGS 为基准逐模块消融：

![[assets/figures/papers/paper_list_l2266_https_openaccess_thecvf_com_content_CVPR2026_html_Zhu_Seele_A_Unified_Ac/figures/009_Table_4.jpg]]
*Table 4: The ablation study of 3DGS dissects our contributions. +Opti. refers to the code optimization in Sec. 4.1, +HP represents the hybrid preprocessing in Sec. 3.3, +CR represents the contribution-aware rasterization in Sec. 3.4*

- **+Opti.**（代码优化）：**1.1×** 加速，纯工程层面提升。
- **+HP**（混合预处理）：在 +Opti. 基础上额外 **2.8×** 加速，并平均提升 PSNR **0.23 dB**。这是加速贡献最大的单一模块，其质量提升源于过滤掉不相关高斯点后渲染管线处理的高斯点更“干净”。
- **+CR**（贡献感知光栅化）：在 +Opti. 基础上额外 **1.3×** 加速，PSNR 损失仅 0.03 dB，几乎无损。这验证了约 1.5% 的 top 高斯点贡献 99% 最终像素透明度这一核心发现（Fig. 4）——跳过低贡献高斯点的颜色混合是安全的。
- **完整 SEELE**（+Opti.+HP+CR）：**3.2×** 整体加速。

### 关键超参数敏感性

- **聚类数与邻居数**（Figure 6）：聚类数过少导致视角相关分离不充分，过多则增加预取开销。论文给出了 Mip-NeRF360 上的敏感度曲线，需参考原文 Fig. 6 获取具体数值。
- **像素组大小**（Figure 7）：贡献感知光栅化中像素组大小设为 **2×2** 在质量与性能间取得最佳平衡。过大的组会导致颜色混合跳过决策过于粗糙，质量显著下降。
- **贡献者数量**（Figure 8）：控制贡献感知光栅化中保留的 top 高斯点比例。论文通过实验给出了质量-性能权衡曲线，需参考原文 Fig. 8 获取具体数值。

![[assets/figures/papers/paper_list_l2266_https_openaccess_thecvf_com_content_CVPR2026_html_Zhu_Seele_A_Unified_Ac/figures/010_Figure_7.jpg]]
*Figure 7: Sensitivity of rendering quality and performance to the pixel group size*

![[assets/figures/papers/paper_list_l2266_https_openaccess_thecvf_com_content_CVPR2026_html_Zhu_Seele_A_Unified_Ac/figures/011_Figure_8.jpg]]
*Figure 8: Sensitivity of rendering quality and performance to the number of contributors*

![[assets/figures/papers/paper_list_l2266_https_openaccess_thecvf_com_content_CVPR2026_html_Zhu_Seele_A_Unified_Ac/figures/014_Figure_6.jpg]]
*Figure 6: Sensitivity of rendering quality and performance to the number of clusters and cluster neighbors in Sec. 3.3*

### 微调策略对比

Table 5 对比了“额外训练”与 SEELE 集成微调的效果。在相同 SEELE 加速框架下，集成微调在质量指标上优于简单延长原始 3DGS 训练，表明视图一致性损失对补偿加速带来的质量下降是必要的。

![[assets/figures/papers/paper_list_l2266_https_openaccess_thecvf_com_content_CVPR2026_html_Zhu_Seele_A_Unified_Ac/figures/012_Table_5.jpg]]
*Table 5: Quality and performance comparison on 3DGS with extra training and our finetuning. Metrics are evaluated with SEELE*

Table 6 进一步消融视图一致性损失：加入该损失后 FLIP 指标从 0.060 降至 0.058，验证了其在维持时序一致性上的作用。

![[assets/figures/papers/paper_list_l2266_https_openaccess_thecvf_com_content_CVPR2026_html_Zhu_Seele_A_Unified_Ac/figures/013_Table_6.jpg]]
*Table 6: Ablation study on*

### 失败模式与局限性

论文未系统报告失败案例，但分析揭示了以下潜在失效场景：

1. **非平滑相机运动**：场景预取依赖线性外推相机姿态，在剧烈旋转或跳跃视角下预取可能失效，导致渲染时所需高斯集群未就绪。
2. **极端视角**：未分析大幅偏离训练视角时聚类效率的退化程度，此时共享高斯点比例可能下降，运行时模型缩减效果减弱。
3. **动态场景**：整个框架假设静态场景的离线聚类，未讨论动态物体或实时变化场景的适用性。
4. **跨场景泛化**：离线聚类需针对每个场景单独进行，不适用于单次训练覆盖多场景的通用模型。

### 开放问题

- SEELE 能否与高斯点剪枝、量化等正交压缩技术叠加，获得更高加速比？
- 在更大规模城市场景（如 Block-NeRF）中，聚类数量与预取策略如何扩展？
- 贡献感知光栅化中的像素组机制是否可适配其他基于图块的渲染管线（如 Instant NGP）？
- 论文未提供代码仓库，开源后可在实际移动设备上独立验证加速比与质量声明。



## 定位与知识库关联

### 与基线方法的关系

SEELE 并非一个独立的渲染算法，而是一个**正交于现有 3DGS 变体的统一加速框架**。其设计哲学在于：不改变底层高斯表示和训练范式，仅通过改造预处理与光栅化两个阶段的计算模式来实现加速。论文在四个代表性基线上验证了这一正交性：

- **3DGS** (Kerbl et al., ACM TOG 2023)：作为原始方法，高斯点最稠密，SEELE 在其上获得最高加速比 3.2×，因为稠密场景为视角相关聚类提供了更大的冗余剔除空间。
- **LightGaussian**：经过剪枝和压缩的高效变体，SEELE 仍能提供 2.7× 加速，说明混合预处理和贡献感知光栅化所利用的冗余（视角无关高斯 + 低贡献高斯）与 LightGaussian 的压缩策略是互补的。
- **Mini-Splatting**：另一高效变体，SEELE 提供 1.8× 加速，加速比相对较低，暗示 Mini-Splatting 本身可能已经隐式地减少了部分低贡献高斯，但其加速机制与 SEELE 的视角感知过滤并不重叠。
- **AdR-Gaussian** (Wang et al., SIGGRAPH Asia 2024)：最新的高效变体，SEELE 提供 1.7× 加速，进一步验证了 SEELE 的加速来源独立于现有方法的优化路径。

这种正交性的根源在于因果机制的差异：现有高效变体主要从**模型压缩**（剪枝、量化、低秩分解）角度减少静态高斯总数，而 SEELE 从**运行时视角感知过滤**角度动态选择参与计算的高斯子集。两者作用于不同阶段，可以叠加。

### 在知识库中的定位

从 3DGS 加速技术谱系来看，SEELE 代表了从“静态模型压缩”向“动态计算跳步”的范式迁移：

- **传统视锥体裁剪与 3σ 包络测试**：仅基于空间位置和尺度进行粗粒度过滤，无法区分高斯点对特定像素的实际贡献。SEELE 的在线过滤将不透明度 $o_i$ 显式纳入交集测试（公式 4–5），消除了大量空间上相交但透明度可忽略的误报高斯点。
- **瓦片级均匀计算**：原始 3DGS 光栅化中，同一瓦片内所有像素线程对每个高斯点执行完整的透明度计算和颜色混合，即使该高斯点对绝大多数像素的贡献近乎为零。SEELE 的贡献感知光栅化通过像素分组和领头像素预判机制（算法 1），将低贡献高斯的颜色混合操作从“逐像素执行”变为“整组跳过”，直接缓解了 GPU warp 发散问题（Fig. 5）。
- **全量常驻内存**：现有方法将所有高斯点常驻 GPU 内存，SEELE 的场景预取机制将高斯点划分为共享集群和视角相关独占集群，运行时仅加载当前所需集群，实现了 39.1% 的运行时模型缩减。

### 适用边界与局限

尽管 SEELE 在移动端 GPU（Nvidia AGX Orin, Orin NX）上展现了显著的加速和内存缩减效果，其适用边界存在以下约束：

1. **场景预取依赖平滑相机轨迹**：场景预取基于线性外推预测未来视角，当相机运动出现突变或非平滑轨迹时，预取命中率可能显著下降，导致延迟尖峰或内存抖动。论文未提供此类场景下的鲁棒性分析。
2. **离线聚类的场景特异性**：视角相关场景聚类和共享/独占高斯点划分需要针对每个场景单独执行。对于需要单次训练覆盖多场景的通用模型（如 Block-NeRF 风格的大规模城市场景），离线聚类的可扩展性和跨场景复用性尚未验证。
3. **GPU 平台局限性**：所有实验均在 Nvidia Orin 系列移动 GPU 上完成。其他移动 GPU 架构（如 Qualcomm Adreno 的图块渲染管线、Apple GPU 的 TBDR 架构）对贡献感知光栅化中像素分组和 warp 发散缓解策略的响应可能存在根本性差异，当前结论不可直接外推。
4. **极端视角退化未量化**：论文未分析在训练视角覆盖范围之外的极端视角（如大幅旋转、穿墙视角）下，聚类效率的退化程度和渲染质量损失。这在实际交互式应用中（如用户自由探索）可能成为瓶颈。

### 开放问题

1. **与模型压缩技术的正交叠加**：SEELE 的加速机制与高斯点剪枝、矢量量化、低秩分解等压缩技术作用于不同阶段，理论上可叠加。但叠加后的累积加速比上限、以及压缩对视角相关聚类有效性的影响（稀疏化后共享高斯比例可能变化）尚未被探索。
2. **大规模场景的聚类扩展**：当前聚类策略在小规模场景（Mip-NeRF360, Tanks&Temples）上验证有效。在更大规模的城市场景中，聚类数量和邻居预取窗口如何扩展才能平衡内存与加速比，仍是一个开放的系统设计问题。
3. **像素分组机制的跨管线可移植性**：贡献感知光栅化中的像素分组和领头像素预判机制，在概念上可适配其他基于图块的渲染管线（如 Instant NGP 的哈希网格渲染），但具体实现需要针对不同管线的瓦片调度和线程模型进行调整，其通用性尚待验证。
4. **代码未开源**：截至论文发表，SEELE 的代码仓库未公开。上述适用边界和叠加假设需要在开源后通过实际设备测试进行验证和修正。
5. **动态场景适应性**：论文未讨论动态场景（如含有运动物体的 4D 高斯泼溅）下聚类预取的有效性。动态物体的高斯点可能在不同聚类间迁移，预取策略需要引入时间维度的预测，这是 SEELE 框架向动态场景扩展的核心挑战。



## 原文 PDF

![[paperPDFs/CVPR_2026/Seele_A_Unified_Acceleration_Framework_for_Real_Time_Gaussian_Splatting_on_Mobile_Devices.pdf]]
