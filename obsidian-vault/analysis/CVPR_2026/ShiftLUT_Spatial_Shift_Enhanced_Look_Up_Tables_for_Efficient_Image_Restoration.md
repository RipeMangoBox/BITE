---
title: "ShiftLUT: Spatial Shift Enhanced Look-Up Tables for Efficient Image Restoration"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/ShiftLUT_Spatial_Shift_Enhanced_Look_Up_Tables_for_Efficient_Image_Restoration.pdf
project_link: null
code_link: "https://github.com/Sailor-t/ShiftLUT"
aliases:
- ShiftLUT
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: 引入可学习空间偏移(LSS)以极低成本扩大感受野，并采用非对称双分支结构重新分配计算资源至信息密集的MSB分支。
primary_logic: LSB分支的特征响应高度稀疏，深层网络处理造成大量无效计算；将可学习偏移转化为静态整数偏移可实现感受野扩展，同时避免在线开销；自适应采样策略在保证精度的同时大幅压缩LUT存储。
claims:
- LSS扩大感受野3.8倍，且无需额外存储和计算。
- 非对称架构在五个基准上保持相同PSNR，但推理延迟从164ms降至84ms。
- LSB分支深层激活稀疏度接近100%，证明对称架构低效。
- EAS(ε=0.4)保持原始精度，LUT存储减少50%以上。
---

# ShiftLUT: Spatial Shift Enhanced Look-Up Tables for Efficient Image Restoration

> [!tip] 核心洞察
> LSB分支的特征响应高度稀疏，深层网络处理造成大量无效计算；将可学习偏移转化为静态整数偏移可实现感受野扩展，同时避免在线开销；自适应采样策略在保证精度的同时大幅压缩LUT存储。

| 字段 | 内容 |
|------|------|
| 中文题名 | ShiftLUT: 空间偏移增强的查找表用于高效图像复原 |
| 英文题名 | ShiftLUT: Spatial Shift Enhanced Look-Up Tables for Efficient Image Restoration |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2603.00906) · [Code](https://github.com/Sailor-t/ShiftLUT) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/image_and_video_generation |
| Method | ShiftLUT |
| Dataset | Set5, Set14, BSDS100, Urban100 |

> [!tip] 效果简介
> - Set5 (SR x4) 上，PSNR 31.33 vs 31.18 (TinyLUT) (+0.15)。
> - Set14 (SR x4) 上，PSNR 28.11 vs 28.01 (TinyLUT) (+0.10)。
> - BSDS100 (SR x4) 上，PSNR 27.21 vs 27.13 (TinyLUT) (+0.08)。

## 概要

图像复原任务（超分辨率、去噪、去块效应）在边缘设备上的高效部署面临一个核心瓶颈：**基于查找表（LUT）的方法虽能实现极快推理，但其感受野受限于LUT的索引范围，而扩大感受野的现有手段（堆叠LUT层、大核分解）又导致存储与计算开销急剧膨胀**。同时，先前工作（如SPLUT）采用的双分支架构在低比特分支（LSB）上存在严重的计算冗余——深层激活稀疏度接近100%，却仍被对称地分配大量计算资源。

ShiftLUT针对上述瓶颈提出三条因果性改进：

1. **可学习空间偏移（LSS）**：通过为每个通道预测一对空间偏移，以几乎零成本将感受野扩大3.8倍。两阶段训练策略先学习浮点偏移，再转换为固定整数偏移，使推理时仅需直接移位而无插值开销。
2. **非对称双分支架构**：将LSB分支简化为单个3×3卷积，释放的计算资源重新分配给信息密集的MSB分支。该设计在五个标准基准上保持相同PSNR（28.19 dB），同时将推理延迟从164 ms降至84 ms。
3. **误差界自适应采样（EAS）**：逐LUT自动搜索最优采样步长，并缓存插值结果。在ε=0.4的设置下，LUT存储减少50%以上而精度无损。

在4×超分辨率任务上，ShiftLUT相较先前最优的TinyLUT平均提升超过0.21 dB，且模型族在存储-精度-速度的帕累托前沿占据左上角优势区域。在去噪（噪声15）和去块效应（QF=10）任务上，ShiftLUT同样以更低的存储和延迟取得了最优PSNR。



### 问题背景：高效图像复原与LUT方法的兴起

图像复原（超分辨率、去噪、去块效应等）是底层视觉的核心任务。近年来，基于深度神经网络（DNN）的方法虽取得了卓越的重建质量，但其高昂的计算和存储开销严重制约了在资源受限边缘设备上的部署。为突破这一瓶颈，基于查找表（LUT）的方法应运而生：通过将预训练网络的推理过程转化为离线的LUT查询，可将计算从浮点卷积降级为极低代价的查表操作，从而在保持一定精度的同时实现极速推理。

然而，现有LUT方法面临一个根本性的权衡困境：**感受野与计算/存储成本之间的矛盾**。扩大感受野对于捕获长程依赖、提升复原质量至关重要，但传统手段——如堆叠多个LUT层（**MuLUT**）或采用大核卷积分解（**TinyLUT**）——不可避免地导致LUT存储量指数级增长和推理延迟攀升。

### 现有方法的缺口：被忽视的计算冗余

在LUT方法的演进中，**SPLUT**引入了双分支架构，将输入图像按位分离为高6位（MSB，Most Significant Bits）和低2位（LSB，Least Significant Bits）两个分支分别处理。这一设计基于一个直观假设：MSB分支承载了图像的主体结构信息，而LSB分支负责细节纹理。然而，现有方法均采用**对称双分支设计**，即两个分支使用相同复杂度的网络结构。

本文通过深入分析揭示了这一设计的严重缺陷：**LSB分支的特征响应高度稀疏**。如Figure 4所示，随着网络深度增加，LSB分支中零值激活的比例急剧上升，在深层几乎达到100%。这意味着对称架构在LSB分支上执行了大量无效计算，造成了严重的资源浪费。这一发现构成了本文的核心动机之一。

### 感受野扩展的困境：动态偏移的代价

另一个关键瓶颈在于感受野的扩展方式。传统LUT方法依赖旋转集成等技巧来间接扩大感受野，但其增益有限。一个更直接的思路是引入可变形机制——让网络为每个像素动态预测浮点偏移并进行插值采样。然而，这种在线偏移预测和双线性插值的计算开销极大，与LUT方法追求极致效率的初衷背道而驰。

### 本文动机与核心思路

基于上述分析，本文的核心动机可归纳为三个层面：

1. **打破感受野与成本之间的僵局**：能否在不增加存储和推理开销的前提下，显著扩大LUT方法的感受野？
2. **消除双分支架构的计算冗余**：如何重新设计双分支架构，将计算资源从信息稀疏的LSB分支重新分配至信息密集的MSB分支？
3. **压缩LUT存储而不牺牲精度**：能否设计一种自适应采样策略，在保证重建精度的同时大幅压缩LUT的存储体积？

针对这三个问题，ShiftLUT提出了三项关键创新：**可学习空间偏移（LSS）** 以零额外成本扩大感受野；**非对称双分支架构**消除LSB分支的冗余计算；**误差界自适应采样（EAS）** 实现精度保持下的LUT压缩。这三项设计共同实现了在更小存储、更快推理的条件下超越先前最优LUT方法的复原质量。



## 核心方法与创新机理

ShiftLUT 围绕 LUT 方法在边缘设备部署中面临的三大瓶颈——感受野受限、对称双分支计算冗余、LUT 存储开销——提出了三项紧密耦合的改进，构成从特征空间重构到推理压缩的完整链路。

### 瓶颈分析：感受野与计算冗余的冲突

LUT 方法通过将卷积网络转化为预计算查找表实现极速推理，但其感受野扩展长期依赖堆叠 LUT 层（如 **MuLUT**）或大核分解，每次扩展都伴随存储与计算成本的指数增长。与此同时，主流方法沿用的对称双分支架构（如 **SPLUT**）将 MSB 和 LSB 分支赋予相同的网络深度，却忽视了 LSB 分支仅承载图像最低 2 位信息的根本特性——深层激活中零值比例接近 100%（见 Figure 4），这意味着对称架构在 LSB 分支上执行了大量无效计算，构成推理延迟的主要瓶颈。

### 可学习空间偏移：零成本感受野扩展

ShiftLUT 的核心突破在于 **Learnable Spatial Shift (LSS)** 模块，它改变了感受野扩展的成本结构。传统方法通过增加网络深度扩大感受野，而 LSS 通过对特征图执行通道级空间移位，在不引入额外卷积层或 LUT 条目的前提下实现感受野扩展。

LSS 由偏移预测网络和空间移位算子组成。偏移预测网络为每个通道生成一对空间偏移值：

$$\{ ( \Delta x _ { c } , \Delta y _ { c } ) \} _ { c = 1 } ^ { C } = \mathcal { O } ( \mathbf { F } )$$

随后按通道执行空间移位：

$${ \bf F } _ { c } ^ { \prime } ( x , y ) = { \bf F } _ { c } ( x - \Delta x _ { c } , y - \Delta y _ { c } )$$

为消除推理时的浮点偏移计算开销，ShiftLUT 采用两阶段训练策略：第一阶段学习浮点偏移并通过双线性插值应用；第二阶段将偏移量化为固定整数，推理时直接进行整数移位，完全规避在线插值。实验表明，两阶段训练仅引入约 0.017 dB 的性能损失，而 LSS 在所有网络配置下均带来超过 0.30 dB 的 PSNR 提升（Set5 基准），最终实现 **3.8 倍感受野扩展**，且无需额外存储与计算。

LSS 的效能依赖于通道多样性：在通道数较多的 **TinyLUT** 上增益显著（Urban100 +0.13 dB），而在仅有 4 通道的 **SPLUT** 上增益微弱（+0.02 dB），表明通道多样性是偏移学习发挥作用的必要条件。

### 非对称双分支架构：计算资源重分配

基于 LSB 分支深层特征高度稀疏的实证发现，ShiftLUT 将对称双分支重构为**激进非对称架构**：LSB 分支被简化为单个 3×3 卷积层，释放的计算资源重新分配至信息密集的 MSB 分支。这一设计在五个标准 SR 基准上保持与对称架构完全相同的平均 PSNR/SSIM（28.19/0.8014），同时将推理延迟从 164ms 压缩至 84ms，降幅达 49%。

### 误差界自适应采样：LUT 压缩与推理加速的联合优化

LUT 存储开销是制约模型部署的另一关键因素。ShiftLUT 提出 **Error-bounded Adaptive Sampling (EAS)**，以误差容忍度 $\varepsilon$ 为约束，逐 LUT 最大化采样步长 $s$：

$$\underset { s \in \mathcal { S } } { \mathrm { m a x } } ~ s \quad \mathrm { s . t . } \quad \mathrm { E r r o r } ( s ) < \varepsilon$$

其中误差定义为插值查询与原始 LUT 值之间的加权期望绝对误差：

$$\mathrm { E r r o r } ( s ) = \frac { s } { s - 1 } \cdot \mathbb { E } _ { i \sim \mathcal { T } } \big [ \big | \mathrm { Q u e r y } _ { s } ( i ) - \mathrm { L U T } [ i ] \big | \big ]$$

与全局固定步长策略不同，EAS 为每个 LUT 自适应确定最优步长，并预计算缓存插值结果，将推理时的逐像素插值替换为单次查询操作。在 $\varepsilon = 0.4$ 设置下，EAS 保持与原始 ShiftLUT 完全相同的 PSNR，同时将 LUT 存储从 171KB 压缩至 104KB（减少超过 50%），运行时从 146ms 进一步降至 84ms。

### 创新链路总结

三项改进形成闭环：LSS 以零成本扩展感受野，为非对称架构提供性能保障；非对称架构释放的计算资源使 LSS 的通道多样性需求得以充分满足；EAS 在精度无损的前提下压缩存储并加速推理，最终使 ShiftLUT 系列模型在存储-PSNR-延迟三维空间中占据左上角最优区域（见 Figure 1）。



ShiftLUT 的整体 pipeline 遵循“位分离—浅层提取—深层偏移处理—重建”的四阶段流程，如图 Figure 2(a) 所示。其核心设计哲学是**将计算资源从信息稀疏的低位分支重新分配至信息密集的高位分支**，并在深层引入可学习空间偏移以打破 LUT 方法固有的感受野瓶颈。

![[assets/figures/papers/paper_list_l2268_https_arxiv_org_abs_2603_00906/figures/002_Figure_2.jpg]]
*Figure 2: (a) Overall architecture of ShiftLUT. (b) The structure of LSS, which consists of an offset prediction network and a spatial shift operator. In Stage 1, the network predicts floating-point offsets (∆x, ∆y), which are applied via bilinear interpolation. In Stage 2, the offsets are replaced with integer-valued approximations, computed by rounding the average offset from Stage 1. (c) Illustration of the EAS inference pipeline with an example using two sampling steps. EAS precomputes and caches interpolated LUT outputs into a reusable buffer, replacing per-pixel interpolation with a single query operation for faster inference*

**1. MSB/LSB 位分离**

输入图像首先被按位拆分为两个分支：最高 6 位构成 MSB（Most Significant Bits）分支，最低 2 位构成 LSB（Least Significant Bits）分支。这一设计的动机来自对对称双分支架构的实证分析：LSB 分支的深层激活稀疏度随网络深度急剧上升，**接近 100% 的激活值为零**（Figure 4），意味着深层网络在 LSB 分支上执行了大量无效计算。

**2. 浅层特征提取与融合**

两个分支各自通过一个 3×3 卷积层独立提取浅层特征，随后进行逐元素相加融合。这一阶段的计算量极低，仅为后续深层处理提供初始特征表示。

**3. 深层 Shift-Block 堆叠**

融合后的特征进入由多个 Shift-Block 串联构成的深层处理阶段。每个 Shift-Block 包含三个核心组件：

- **Learnable Spatial Shift (LSS)**：对每个通道预测一对空间偏移 $(\Delta x_c, \Delta y_c)$，并按偏移量对特征图进行通道级空间移位，从而以**零额外存储和计算开销**将感受野扩大 3.8 倍（Figure 3）。
- **PwBlock（逐点卷积块）**：执行通道间的信息融合，对应 LUT 转换后的 1D 查找表查询操作。
- **DwConv（深度可分离卷积）**：提取空间局部细节，同样以 1D LUT 形式高效实现。

**4. 最终精炼与上采样**

深层特征经过最终的 PwBlock 进行通道精炼后，由 PixelShuffle 操作完成上采样，重建高分辨率输出图像。

**非对称架构的关键决策**

与 SPLUT 等前驱工作的对称双分支设计不同，ShiftLUT 将 LSB 分支**极简化至仅保留一个 3×3 卷积层**，而将节省的计算资源重新分配给 MSB 分支的 Shift-Block 堆叠。这一非对称设计在五个标准 SR 基准上保持相同 PSNR（28.19 dB），同时将推理延迟从 164 ms 降至 84 ms，验证了“LSB 分支深层处理冗余”这一核心洞察。

**LUT 转换与推理优化**

所有卷积层在训练后通过 TinyLUT 的可分离映射策略（SMS）转换为 1D LUT，并采用旋转集成技巧进一步扩大推理时的感受野。LSS 模块采用两阶段训练策略：第一阶段学习浮点偏移并通过双线性插值应用；第二阶段将偏移量化为固定整数偏移，推理时直接进行通道移位，完全消除在线插值开销。此外，Error-bounded Adaptive Sampling (EAS) 在离线阶段逐 LUT 自适应确定最优采样步长，并缓存插值结果，将 LUT 存储压缩超过 50% 的同时保持原始精度。



ShiftLUT 的整体架构（图2a）由三个核心模块构成：**可学习空间偏移（LSS）**、**非对称双分支架构**，以及**误差界自适应采样（EAS）**。以下逐一解析其设计原理与关键公式。

### 可学习空间偏移（LSS）

LSS 是 ShiftLUT 扩大感受野的核心机制。传统 LUT 方法通过堆叠多个 LUT 层或使用大核卷积分解来扩大感受野，但这不可避免地带来存储或计算开销的指数级增长。LSS 的关键洞察在于：通过在特征图的通道维度上施加可学习的空间偏移，使不同通道“看到”输入图像的不同区域，从而在不增加任何额外存储或推理计算的前提下，显著扩大网络的等效感受野。

LSS 模块（图2b）包含一个轻量的偏移预测网络和一个空间偏移算子。给定输入特征图 $\mathbf{F} \in \mathbb{R}^{C \times H \times W}$，偏移预测网络为每个通道生成一对位移值：

$$\{ ( \Delta x _ { c } , \Delta y _ { c } ) \} _ { c = 1 } ^ { C } = \mathcal { O } ( \mathbf { F } ) \tag{1}$$

其中 $\mathcal{O}$ 是一个由全局平均池化、全连接层和激活函数构成的微型网络。随后，空间偏移算子根据预测的偏移对每个通道进行移位：

$${ \bf F } _ { c } ^ { \prime } ( x , y ) = { \bf F } _ { c } ( x - \Delta x _ { c } , y - \Delta y _ { c } ) \tag{2}$$

**训练与推理的两阶段策略**：直接学习整数偏移存在不可微问题，而使用 STE 或 Gumbel-Softmax 近似得到的整数偏移会导致约 0.3 dB 的性能下降（Table 5）。ShiftLUT 采用两阶段训练策略：第一阶段学习浮点偏移，通过双线性插值实现可微的空间移位；第二阶段将训练过程中各通道偏移的均值取整，转化为固定的整数偏移，推理时直接进行网格移位，完全消除了插值计算开销。实验表明，该策略仅引入约 0.017 dB 的微小性能损失，但换来了推理时的零额外开销。

LSS 的感受野扩展效果通过 LAM（Local Attribution Map）可视化得到验证（图3）：引入 LSS 后，一个 16×16 输出块的 DI（Diffusion Index）显著增大，表明更广范围的输入像素参与了输出重建，量化结果为感受野扩大 **3.8 倍**。

### 非对称双分支架构

SPLUT 和 TinyLUT 等先前工作采用对称双分支设计：将输入图像按位分离为最高 6 位（MSB）和最低 2 位（LSB），两个分支采用相同复杂度的网络处理。ShiftLUT 的作者发现，LSB 分支的特征响应高度稀疏——随着网络深度增加，LSB 分支中零值激活的比例急剧上升，在深层接近 **100%**（图4）。这意味着对称架构在 LSB 分支上存在严重的计算冗余。

基于这一发现，ShiftLUT 将 LSB 分支**极简化**为单个 3×3 卷积层，释放出的计算资源重新分配给信息密集的 MSB 分支。实验证明，该非对称设计在五个标准 SR 基准上保持与对称设计几乎相同的 PSNR/SSIM（28.19/0.8014 vs 28.19/0.8016），但推理延迟从 164ms 降至 84ms，降幅近 50%。

### 误差界自适应采样（EAS）

LUT 方法的存储开销与索引空间的采样密度直接相关。传统方法使用全局固定采样步长，依赖复杂的插值来补偿精度损失。EAS 的核心思想是：不同 LUT 层对采样精度的敏感度不同，因此应为每层自适应地确定最优采样步长。

EAS 的优化目标是在预设误差界 $\varepsilon$ 内最大化采样步长 $s$：

$$\underset { s \in \mathcal { S } } { \mathrm { m a x } } ~ s \quad \mathrm { s . t . } \quad \mathrm { E r r o r } ( s ) < \varepsilon \tag{3}$$

其中误差函数定义为插值查询与原始 LUT 值之间的加权期望绝对误差：

$$\mathrm { E r r o r } ( s ) = \frac { s } { s - 1 } \cdot \mathbb { E } _ { i \sim \mathcal { T } } \big [ \big | \mathrm { Q u e r y } _ { s } ( i ) - \mathrm { L U T } [ i ] \big | \big ]$$

权重因子 $\frac{s}{s-1}$ 反映了采样步长越大时插值误差的放大效应。优化在离线阶段完成，EAS 同时预计算并缓存插值后的 LUT 值到可复用缓冲区中，推理时将逐像素插值替换为单次查询操作，进一步消除了在线插值开销。

实验表明，$\varepsilon = 0.4$ 的设置下，EAS 保持与原始 ShiftLUT 完全相同的 PSNR，同时将 LUT 存储从 171KB 压缩至 104KB（**减少超过 50%**），推理时间从 146ms 降至 84ms。

### 补充图表

![[assets/figures/papers/paper_list_l2268_https_arxiv_org_abs_2603_00906/figures/004_Figure_4.jpg]]
*Figure 4: The symmetric network architecture (top) and its corresponding LSB feature sparsity (bottom). The layer-wise analysis shows that feature sparsity in the LSB branch increases significantly with network depth*

![[assets/figures/papers/paper_list_l2268_https_arxiv_org_abs_2603_00906/figures/003_Figure_3.jpg]]
*Figure 3: Local Attribution Map (LAM) visualization for a 16×16 output patch. A larger DI indicates that a wider range of pixels contributes to the output result. Our method with LSS shows larger DI and better performance than the variant without LSS*



## 实验与关键发现

ShiftLUT 在三个典型的低层视觉任务上进行了验证：4× 超分辨率（SISR）、灰度图像去噪（Denoising）和 JPEG 去块效应（Deblocking）。以下从主结果、消融实验和失败模式三个维度展开分析。

### 4× 超分辨率主结果

**定量对比**（Table 1）：ShiftLUT 在 5 个标准 SISR 测试集上全面超越先前最优的 LUT 方法 TinyLUT。以 Set5 为例，ShiftLUT-L 取得 **31.33 dB** PSNR，较 TinyLUT 的 31.18 dB 提升 **+0.15 dB**；在结构复杂度更高的 Urban100 上，提升幅度达到 **+0.20 dB**（25.12 vs 24.92）。五个基准上的平均 PSNR/SSIM 为 **28.19/0.8014**，同时推理延迟从对称架构的 164ms 降至 **84ms**，降幅接近 50%。

**定性对比**（Figure 5）：ShiftLUT 在纹理恢复和边缘锐度上明显优于 TinyLUT 和 MuLUT，尤其在重复性纹理区域（如建筑立面）减少了伪影和模糊。与 DNN 方法 SwinIR 相比，ShiftLUT 在存储和推理速度上具有数量级优势，但在极精细纹理的重建上仍有差距——这是 LUT 方法受限于离散输入空间的固有瓶颈。

**模型族效率**（Figure 1）：ShiftLUT 系列模型占据存储-PSNR-运行时三维散点图的左上角区域，表明其在三个维度上同时取得最优权衡。具体而言，ShiftLUT-S 以仅 **104KB** 的 LUT 存储达到 31.33 dB（Set5），推理时间 **84ms**，在边缘设备部署场景下具有显著优势。

### 去噪与去块效应结果

**灰度去噪**（Table 2，噪声水平 15）：ShiftLUT 在 Set12 上取得 **32.43 dB**，较 MuLUT 的 31.83 dB 提升 **+0.60 dB**，较 TinyLUT 的 32.12 dB 提升 +0.31 dB。在 BSD68 上同样保持领先（30.27 dB vs MuLUT 29.84 dB）。

**JPEG 去块效应**（Table 3，质量因子 10）：ShiftLUT 在 Classic5 上取得 **29.12 dB** PSNR-B，较 MuLUT 的 28.47 dB 提升 **+0.65 dB**；在 LIVE1 上为 28.96 dB（+0.58 dB）。定性结果显示，ShiftLUT 更有效地抑制了块状伪影，同时保留了边缘细节。

### 消融实验

**LSS 模块的有效性**（Figure 8）：在所有测试的网络配置（不同 ShiftBlock 堆叠数和通道数）下，加入 LSS 均带来超过 **0.30 dB** 的 PSNR 提升（Set5）。LAM 可视化（Figure 3）进一步证实，LSS 将感受野扩大了约 **3.8 倍**，且无需额外存储和计算开销。

**非对称架构的贡献**（Section 3.3）：LSB 分支的深层激活稀疏度接近 **100%**（Figure 4），证实了对称架构中 LSB 分支存在严重计算冗余。将 LSB 分支简化为单个 3×3 卷积后，PSNR 完全持平（28.19 vs 28.19），推理延迟从 164ms 降至 84ms。

**EAS 压缩策略**（Table 4）：在 ε=0.4 的设置下，EAS 保持与原始 ShiftLUT **完全相同的 PSNR**（Set5 31.33 dB, Set14 28.11 dB, BSDS100 27.21 dB），同时将 LUT 存储从 171KB 压缩至 **104KB**（减少超过 50%），运行时从 146ms 降至 84ms。相比之下，均匀采样方法在相同压缩率下会导致明显精度损失。

**两阶段偏移训练**（Table 5）：与直接使用 STE 或 Gumbel-Softmax 学习整数偏移相比，两阶段策略（先学习浮点偏移，再转换为固定整数偏移）在 Set5 上取得最优的 31.33 dB。直接学习整数偏移的方法均出现不同程度的精度下降（STE: 31.27 dB, Gumbel-Softmax: 31.29 dB），证明了渐进式离散化策略的必要性。

**LSS 的泛化性**（Table 6）：将 LSS 模块嵌入 TinyLUT 后，在 Urban100 上带来 **+0.13 dB** 的提升；但在通道数仅 4 的 SPLUT 上，增益仅为 **+0.02 dB**。这表明 LSS 的效能依赖于充分的通道多样性——通道数过少时，可学习的通道间偏移空间受限，感受野扩展效果有限。

### 失败模式与局限性

1. **低通道数场景增益有限**：如上述消融所示，LSS 在通道数极少的网络（如 SPLUT 的 4 通道）上几乎不产生收益。在实际部署中，若因存储限制需要极小通道数，LSS 的性价比会显著降低。

2. **两阶段训练的性能折损**：浮点偏移转换为整数偏移的过程引入约 **0.017 dB** 的 PSNR 损失（Table 5 中 Stage 1 vs Stage 2 的差异）。目前尚无方法能在不损失精度的情况下直接端到端学习整数偏移。

![[assets/figures/papers/paper_list_l2268_https_arxiv_org_abs_2603_00906/figures/015_Table_5.jpg]]
*Table 5: Comparison of different shifting operations in ShiftLUT on standard SISR test sets for an upscaling factor of 4*

3. **EAS 的 ε 敏感度**：最优误差界 ε 可能因任务和数据集而异。论文仅在 ε=0.4 下展示了 SISR 任务的结果，其在去噪和去块效应任务上的最佳取值需要额外调参验证（Table 4 仅报告了 SISR 场景）。

![[assets/figures/papers/paper_list_l2268_https_arxiv_org_abs_2603_00906/figures/013_Table_4.jpg]]
*Table 4: Compare EAS with other LUT compression methods*

4. **任务覆盖范围有限**：当前验证集中于超分、去噪和去块三个经典低层视觉任务，尚未扩展到去模糊、去雨等更复杂的退化场景。LSS 在这些任务上的感受野扩展效果是否同样显著，仍需进一步实验确认。

### 补充图表

![[assets/figures/papers/paper_list_l2268_https_arxiv_org_abs_2603_00906/figures/005_Table_1.jpg]]
*Table 1: Quantitative comparisons on 5 standard SISR test sets for an upscaling factor of 4. The best and second-best results of each metric are highlighted in red and blue, respectively (the highlighting is restricted to LUT-based methods to emphasize fair comparison)*

![[assets/figures/papers/paper_list_l2268_https_arxiv_org_abs_2603_00906/figures/012_Figure_8.jpg]]
*Figure 8: PSNR comparison on the Set5 under different network configurations. The left and right figures show results obtained by varying the number of stacked ShiftBlocks and channels, respectively. Each bar group compares models with and without LSS*

![[assets/figures/papers/paper_list_l2268_https_arxiv_org_abs_2603_00906/figures/016_Table_6.jpg]]
*Table 6: Quantitative comparison of PSNR on standard benchmark datasets for x4 super-resolution tasks between the original version of SPLUT and TinyLUT, and the modified version integrating LSS*

![[assets/figures/papers/paper_list_l2268_https_arxiv_org_abs_2603_00906/figures/001_Figure_1.jpg]]
*Figure 1: Model comparison in terms of storage size, PSNR and runtime on Set5 for x4 super-resolution. Our method produces a family of models that has the smallest storage size and occupies the top-left corner, indicating superior performances (PSNR on yaxis) with fast inference speed (Runtime on x-axis)*

![[assets/figures/papers/paper_list_l2268_https_arxiv_org_abs_2603_00906/figures/006_Figure_5.jpg]]
*Figure 5: Qualitative comparison for 4× super-resolution on different images*

![[assets/figures/papers/paper_list_l2268_https_arxiv_org_abs_2603_00906/figures/007_Table_2.jpg]]
*Table 2: The comparison for grayscale image denoising at a noise level of 15 on standard benchmark datasets. The best of each metric is highlighted in Red*

![[assets/figures/papers/paper_list_l2268_https_arxiv_org_abs_2603_00906/figures/008_Table_3.jpg]]
*Table 3: The comparison for image deblocking under a quality factor of 10 on standard benchmark datasets. The best of each metric is highlighted in Red*



## 定位与知识库关联

### 1. 与 LUT 方法谱系的关系

ShiftLUT 处于基于查找表（LUT）的高效图像复原方法演进线上，其前驱工作包括 **SR-LUT**（早期空间 LUT 方法）、**SPLUT**（提出 MSB/LSB 双分支结构）、**MuLUT**（采用多 LUT 级联扩大感受野）以及 **TinyLUT**（先前最优的 LUT 方法，引入可分离映射策略 SMS 将卷积转换为 1D LUT）。ShiftLUT 直接继承 TinyLUT 的 SMS 转换策略和旋转集成增强技巧，但在三个关键维度上突破了该谱系的瓶颈：

- **感受野扩展机制**：传统方法依赖堆叠多个 LUT 层（MuLUT）或大核卷积分解（TinyLUT）来扩大感受野，这不可避免地带来存储和计算开销的指数增长。ShiftLUT 引入可学习空间偏移模块（LSS），通过学习通道间静态偏移实现感受野扩展，无需额外存储与计算开销。实验表明 LSS 将感受野扩大 3.8 倍（Figure 3, LAM 可视化），且在所有网络配置下带来超过 0.30 dB 的 PSNR 提升（Set5 基准，Figure 8）。

- **双分支架构设计**：SPLUT 和 TinyLUT 采用对称双分支架构，MSB 和 LSB 分支使用相同复杂度的网络。ShiftLUT 通过分析发现 LSB 分支的深层激活稀疏度接近 100%（Figure 4），证明对称架构存在严重计算冗余。据此提出非对称架构，将 LSB 分支简化为单个 3×3 卷积，计算资源重分配至信息密集的 MSB 分支。该设计在五个 SR 基准上保持相同 PSNR（28.19 vs 28.19），但推理延迟从 164ms 降至 84ms。

- **LUT 压缩策略**：传统方法使用全局固定采样步长，依赖复杂插值补偿精度损失。ShiftLUT 提出误差界自适应采样（EAS），逐 LUT 自动确定最优采样步长，并缓存插值结果消除推理开销。在 ε=0.4 设置下，EAS 保持原始 ShiftLUT 的 PSNR 不变，同时将 LUT 存储减少超过 50%（从 171KB 降至 104KB），运行时从 146ms 降至 84ms（Table 4）。

### 2. 与 DNN 方法的关系

ShiftLUT 与基于深度神经网络（DNN）的方法处于不同设计范式。DNN 方法如 **FSRCNN**（经典轻量级 CNN 超分方法）和 **SwinIR**（基于 Transformer 的高性能方法）在推理时执行卷积计算，而 LUT 方法将预训练网络转换为查找表，推理仅涉及内存查询。这种范式转换带来极致的推理速度优势，但也限制了模型的容量和灵活性。ShiftLUT 在 LUT 方法谱系内达到最优，其性能介于轻量级 CNN 和高性能 Transformer 方法之间：在 SISR 4× 任务上，ShiftLUT-L 在 Set5 上达到 31.33 dB（Table 1），超越所有 LUT 方法，但低于 SwinIR 等重型 DNN。论文强调所有对比中 LUT 方法的颜色高亮仅限于同类方法之间，以确保公平比较。

### 3. 适用边界与局限

ShiftLUT 的适用边界由以下因素界定：

- **通道多样性依赖**：LSS 模块在通道数较少的网络上增益有限。在 SPLUT（仅 4 通道）上集成 LSS 仅带来 +0.02 dB 提升，而在通道数更多的 TinyLUT 上增益显著（Urban100 +0.13 dB，Table 6）。这表明 LSS 的效能依赖于充分的通道多样性来学习有意义的偏移模式。

- **两阶段训练的精度损失**：LSS 采用两阶段训练策略（先学习浮点偏移，再转换为固定整数偏移），引入约 0.017 dB 的性能下降。直接使用 STE 或 Gumbel-Softmax 端到端学习整数偏移的尝试均导致更差的精度（Table 5），说明当前无法在不牺牲精度的情况下直接学习整数偏移。

- **任务范围限制**：方法主要针对低层视觉任务（超分辨率、去噪、去块效应）进行了验证，尚未扩展到其他图像复原任务（如去模糊、去雾等）。

- **EAS 参数敏感性**：EAS 的自适应步长优化依赖于预定义的误差界 ε，其最佳值可能因任务而异，需要针对不同应用场景进行调优。

### 4. 开放问题

1. **端到端整数偏移学习**：能否在不使用两阶段训练的情况下，直接端到端学习整数偏移，从而消除 0.017 dB 的精度损失？当前的 STE 和 Gumbel-Softmax 方案均未成功，可能需要新的离散优化策略。

2. **动态偏移机制**：LSS 模块使用静态整数偏移，能否进一步与动态偏移机制结合，使偏移量根据输入内容自适应调整，以应对内容变化更大的场景？

3. **EAS 的可扩展性**：EAS 的在线缓冲机制在更深的网络或更高分辨率的输入下是否仍然保持低内存开销？当前验证限于标准 SR 配置，其在高分辨率或视频任务中的表现尚不明确。

4. **跨任务泛化**：ShiftLUT 的设计原则（LSS、非对称架构、EAS）能否推广到其他图像复原任务或更广泛的 low-level vision 问题？



## 原文 PDF

![[paperPDFs/CVPR_2026/ShiftLUT_Spatial_Shift_Enhanced_Look_Up_Tables_for_Efficient_Image_Restoration.pdf]]
