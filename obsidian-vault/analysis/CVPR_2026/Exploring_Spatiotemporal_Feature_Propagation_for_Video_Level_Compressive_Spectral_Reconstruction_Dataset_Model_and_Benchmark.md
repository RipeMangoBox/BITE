---
title: "Exploring Spatiotemporal Feature Propagation for Video-Level Compressive Spectral Reconstruction: Dataset, Model and Benchmark"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/Exploring_Spatiotemporal_Feature_Propagation_for_Video_Level_Compressive_Spectral_Reconstruction_Dataset_Model_and_Benchmark.pdf
project_link: null
code_link: "https://github.com/nju-cite/DynaSpec"
aliases:
- PS
- ESFPVLCSRDMB
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
- topic/representation_self_supervised_transfer
- topic/benchmarks_datasets_evaluation
core_operator: 利用固定的编码模式在相邻帧间产生的互补特征，通过时空特征传播可以补偿被遮挡信息并增强时序一致性。
primary_logic: 提出先空间后时间的跨域注意力传播机制（CDPA），通过共享值增强域间特征交互，并引入桥接令牌将计算复杂度从二次降低到近似线性，实现高效、高质量的视频级压缩光谱重建。
claims:
- 在DD-CASSI系统上，PG-SVRT在KAIST数据集上PSNR达到41.23 dB，在DynaSpec数据集上PSNR达到41.82 dB，均超越现有最佳方法。
- 模块消融实验表明，逐步添加MGDP、CDPA和MDFFN将PSNR从39.97 dB提升至41.52 dB，验证了所有模块的贡献。
- 桥接令牌数量设为64时，在满足2N_B < H_win W_win条件下，实现了最优重建质量（PSNR 41.52 dB）和最低ST-RRED（23.25），证明了线性注意力的有效性。
- KAIST 上 PSNR (dB) = 41.23
---

# Exploring Spatiotemporal Feature Propagation for Video-Level Compressive Spectral Reconstruction: Dataset, Model and Benchmark

> [!tip] 核心洞察
> 提出先空间后时间的跨域注意力传播机制（CDPA），通过共享值增强域间特征交互，并引入桥接令牌将计算复杂度从二次降低到近似线性，实现高效、高质量的视频级压缩光谱重建。

| 字段 | 内容 |
|------|------|
| 中文题名 | 探索时空特征传播的视频级压缩光谱重建：数据集、模型与基准 |
| 英文题名 | Exploring Spatiotemporal Feature Propagation for Video-Level Compressive Spectral Reconstruction: Dataset, Model and Benchmark |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2603.00611) · [Code](https://github.com/nju-cite/DynaSpec) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction #topic/representation_self_supervised_transfer #topic/benchmarks_datasets_evaluation |
| Method | PG-SVRT |
| Dataset | KAIST, DynaSpec |

> [!tip] 效果简介
> - KAIST 上，PSNR (dB) 41.23 (领先所有对比方法)；ST-RRED 19.35 (低于所有对比方法)。
> - DynaSpec 上，PSNR (dB) 41.82 (领先所有对比方法)；SSIM 0.9904 (领先所有对比方法)。
> - 模型效率 上，Params (M) 2.48 (参数显著低于视频/ViT方法)。

## 概要

压缩光谱成像（SCI）通过将三维高光谱数据立方体编码为二维测量图像，以低成本和紧凑光路实现快速光谱采集。然而，从单帧测量中重建完整的高光谱图像是一个高度不适定问题：空间-光谱信息的压缩丢失导致重建结果存在不确定性，而逐帧独立处理进一步破坏了视频序列的时间一致性，表现为光谱强度曲线的剧烈抖动（Figure 1）。这一瓶颈的根源在于，单帧方法无法利用相邻帧间的互补信息来补偿被遮挡或混叠的光谱特征。

针对上述问题，本文提出**PG-SVRT**（Propagated Guided Spectral Video Reconstruction Transformer），将学习范式从图像级扩展到视频级，通过时空特征传播实现高效、时序一致的光谱重建。核心思路是：SCI系统中固定的编码掩码在不同帧间产生互补的测量模式，PG-SVRT利用这一先验，以“先空间后时间”的渐进式注意力机制（CDPA）传播跨域特征，并通过桥接令牌将计算复杂度从二次降低到近似线性。同时，掩码引导的退化感知模块（MGDP）显式建模压缩退化过程，多域前馈网络（MDFFN）分头独立提取空间与时间特征后融合，三者协同工作于U-Net骨干之上。

为支撑视频级重建研究，本文还构建了**DynaSpec**数据集，包含30个动态场景的高光谱序列，通过手动控制物体运动采集，覆盖多样化的真实世界运动模式（Figure 2）。

实验结果表明，PG-SVRT在DD-CASSI系统上取得了最优的重建质量：在KAIST数据集上PSNR达41.23 dB，在DynaSpec数据集上PSNR达41.82 dB，SSIM达0.9904，均显著超越现有方法（Table 2）。同时，模型参数量仅2.48M，单帧计算量28.18 GFLOPs，在效率和性能之间取得了良好平衡。模块消融实验进一步证实，逐步引入MGDP、CDPA和MDFFN可将PSNR从39.97 dB提升至41.52 dB，验证了各组件的独立贡献（Table 3）。

**方法定位**：PG-SVRT属于视频级压缩光谱重建方法，与单帧方法（如CST、MST、s2-Transformer、DADF、DPU）和通用视频恢复方法（如VRT）形成对比。其关键改进在于将重建范围从单帧扩展至多帧序列，以时空特征传播替代单纯的空间自注意力，并通过桥接令牌和价值共享机制在控制计算开销的同时增强跨域信息交互。



### 压缩光谱成像的核心矛盾

光谱图像（HSI）同时捕获空间与光谱维度的三维信息，在遥感、医学诊断、农业监测等领域具有不可替代的价值。然而，传统光谱成像依赖扫描式采集，时间分辨率低，难以捕捉动态场景。压缩光谱成像（SCI）通过光学编码将三维数据立方体压缩到二维探测器上，再借助计算重建恢复完整光谱，在单次曝光中实现高速采集。

SCI系统的物理成像过程可统一建模为线性观测：

$$Y_i = \Psi X_i + \Theta$$

其中 $Y_i$ 为第 $i$ 帧的二维压缩测量，$X_i$ 为对应的高光谱帧，$\Psi$ 为编码算子（由掩码 $\Phi$ 和色散位移 $\sigma(c)$ 决定），$\Theta$ 为噪声。根据光路中色散器数量，SCI分为单色散器（SD）和双色散器（DD）两种架构，其测量模型分别为：

$$Y_i(h,w) = \sum_{c=1}^{C} \Phi(h,w) \cdot X_i(h,w-\sigma(c),c) \quad \text{(SD)}$$

$$Y_i(h,w) = \sum_{c=1}^{C} \Phi(h,w-\sigma(c)) \cdot X_i(h,w,c) \quad \text{(DD)}$$

两种架构的核心差异在于：SD中掩码固定而光谱通道位移，DD中光谱通道固定而掩码位移。这一差异导致不同系统在空间-光谱信息编码模式上的本质区别，进而影响重建难度与质量上限。

### 图像级重建的固有瓶颈

现有压缩光谱重建方法（如 **CST** (Cai et al., CVPR 2022)、**MST** (Cai et al., ECCV 2022)、**s2-Transformer** (Wang et al., TPAMI 2025)、**DADF** (Cai et al., NeurIPS 2022)、**DPU** (Zhang et al., CVPR 2024)）几乎全部以单帧图像为处理单元。这种逐帧独立重建的范式存在两个根本性问题：

**空间-光谱信息丢失导致重建不确定性。** 压缩测量将数十个光谱通道的信息混叠到单一二维平面上，本质上是一个严重欠定的逆问题。单帧重建缺乏额外的约束信号，在纹理复杂或光谱变化剧烈的区域容易产生模糊、伪影或光谱失真。如图1(b)所示，图像级方法恢复的光谱强度曲线存在明显抖动，反映时间维度上的不一致性。

**逐帧处理缺乏时间一致性。** 视频序列中各帧独立重建，帧间没有任何信息交互，导致重建结果在时间轴上出现闪烁和跳变。这种时间不一致性对于需要分析光谱动态变化的应用（如材料相变监测、化学反应追踪）是致命的。

### 视频级重建的机遇与缺口

视频序列中相邻帧之间存在天然的**信息互补性**：由于编码掩码在帧间保持固定，而场景中的物体运动使得同一空间位置在不同帧中被不同区域的掩码调制。这种互补编码意味着，某一帧中被遮挡或欠采样的光谱信息，可能在相邻帧中以不同的编码形式被保留。通过跨帧特征传播，可以有效补偿单帧信息的缺失，同时增强时序一致性。图1(c)展示了视频级重建的优势：利用帧间互补信息后，光谱强度曲线变得平滑，重建完整性和时间一致性显著提升。

然而，视频级压缩光谱重建面临两大现实缺口：

**数据集缺口。** 高质量动态高光谱视频数据的采集极为困难。传统高光谱相机扫描速度慢，无法捕获真实动态场景；而快照式光谱成像系统虽能高速采集，但空间或光谱分辨率往往受限。缺乏公开的动态高光谱数据集，直接阻碍了视频级重建方法的研发与公平比较。

**方法缺口。** 将图像级方法简单扩展至视频域面临计算复杂度的挑战。若对多帧特征施加全时空注意力，计算量将随帧数呈平方增长，在视频处理中不可接受。现有的视频恢复方法（如 **VRT** (Liang et al., TIP 2024)）虽能建模时序依赖，但未针对压缩光谱成像的特殊退化过程进行设计，难以充分利用掩码先验和帧间互补编码特性。

### 本文的切入点

针对上述瓶颈，本文从三个层面系统推进视频级压缩光谱重建研究：

1. **构建DynaSpec数据集**：通过逐帧采集动态高光谱序列，模拟真实场景中的多样化运动模式，为视频级重建提供首个公开基准。
2. **提出PG-SVRT网络**：设计掩码引导的退化感知模块（MGDP）、跨域传播注意力（CDPA）和多域前馈网络（MDFFN），实现高效、高质量的时空特征融合。
3. **搭建DD-CASSI原型系统**：构建双色散器压缩光谱成像的物理原型，验证方法在真实测量上的有效性。

核心洞察在于：利用固定编码模式在相邻帧间产生的互补特征，通过“先空间后时间”的渐进式注意力传播，可以在不显著增加计算开销的前提下，补偿单帧信息缺失并增强时序一致性。



## 核心方法与创新机理

PG-SVRT 的核心创新在于将压缩光谱重建从**单帧图像级**拓展至**多帧视频级**，并围绕“固定编码模式在相邻帧间产生互补信息”这一因果机制，设计了一套渐进式时空特征传播框架。与逐帧独立重建的方法相比，该方法在以下四个关键维度上实现了系统性改变：

**重建范围：从单帧到多帧序列。** 传统方法（如 **CST** (Cai et al., CVPR 2022)、**MST** (Cai et al., ECCV 2022)、**s2-Transformer** (Wang et al., TPAMI 2025)）仅利用单帧测量值进行空间-光谱重建，忽略了视频序列中帧间的信息互补性，导致空间细节丢失和时间强度曲线闪烁（Figure 1b）。PG-SVRT 将学习范式扩展到视频域，利用多帧输入建模时空依赖关系，使被遮挡的光谱信息可通过相邻帧进行补偿，从而提升重建完整性和时序一致性（Figure 1c）。

**注意力机制：从空间自注意力到空间-时间渐进式注意力 + 价值共享传播。** 常规方法采用窗口自注意力或全局自注意力在空间域内建模，缺乏跨时间帧的信息交互。PG-SVRT 提出的**跨域传播注意力（CDPA）**采用“先空间后时间”的渐进式策略：首先在空间域执行自注意力，然后将空间注意力输出作为**共享值（shared value）**传递到时间注意力阶段。这种价值共享机制实现了跨域特征融合，使得时间注意力能够直接利用空间增强后的特征，从而提升光谱重建质量。消融实验证实，空间-时间渐进式传播配合价值共享（S-T w/P）在 PSNR 上达到 41.52 dB，优于并行处理、先时间后空间（T-S）以及无传播策略（Table 4）。

**计算复杂度控制：引入桥接令牌实现近似线性复杂度。** 常规窗口注意力受限于窗口大小，当同时处理空间和时间维度时计算开销急剧增长。CDPA 引入**桥接令牌（Bridged Tokens）**机制：桥接令牌从查询（Q）中提取核心信息，再与键（K）和值（V）交互，将两级注意力计算简化为近似线性复杂度。当桥接令牌数量 $N_B$ 满足条件 $2 N_B < H_{win} W_{win}$ 时，可在不损失性能的前提下显著降低计算量。消融实验表明，$N_B = 64$ 时达到最佳 PSNR 41.52 dB 和最低 ST-RRED 23.25（Table 5）。

**前馈网络：从标准 MLP/卷积到多域前馈网络（MDFFN）。** 传统 Transformer 中的前馈网络（FFN）通常采用标准 MLP 或卷积，缺乏对空间和时间特征的差异化处理。PG-SVRT 的 **MDFFN** 将光谱特征划分到不同头部，分别执行空间自注意力和时间自注意力，而后进行融合。这种分头独立提取再融合的设计有效增强了域内特征提取能力，相比普通 3D 卷积或单域处理在 PSNR 和 SAM 上均有提升（Table 6）。

上述四个 changed slots 并非孤立改进，而是形成了一条因果链：**MGDP** 首先建模压缩退化过程以解耦帧内编码信息（Eq. 4），为后续模块提供退化感知特征；**CDPA** 在此基础上通过空间-时间渐进式注意力实现跨域特征传播；**MDFFN** 进一步强化域内特征提取；**桥接令牌**则确保整个流程的计算可行性。模块消融实验完整验证了这一因果链：逐步添加 MGDP、CDPA 和 MDFFN，PSNR 从 39.97 dB 依次提升至 41.30 dB、41.41 dB，最终达到 41.52 dB（Table 3）。



PG‑SVRT 采用基于 U‑Net 的编码器‑解码器主干，将视频级压缩光谱重建组织为三个核心模块的串行级联：**掩码引导的退化感知 (MGDP)**、**跨域传播注意力 (CDPA)** 与 **多域前馈网络 (MDFFN)**（图 3）。输入为多帧压缩测量序列 $\{Y_i\}_{i=1}^T$ 及其对应的物理编码掩码 $\Phi$，输出为重建的高光谱视频帧 $\{\hat{X}_i\}_{i=1}^T$。

### 输入构造与退化感知

原始测量 $Y$ 首先经 **MGDP** 预处理，以显式建模压缩成像的退化过程。MGDP 通过可学习的掩码嵌入 $W_m(\Phi, \Phi_p)$ 与测量特征 $F_m(Y)$ 逐元素相乘，再与原始测量 $Y$ 在通道维拼接，形成退化感知的输入张量：

$$Y_{in} = \text{Concat}\big(\text{Conv}(W_m(\Phi, \Phi_p) \odot F_m(Y)),\; Y\big)$$

其中 $\Phi_p$ 表示物理掩码的互补信息，$\odot$ 为逐元素乘法。这一设计使网络在进入主重建流水线之前即获得对编码退化的先验感知，有助于解耦帧内光谱‑空间的混叠信息。

### 主干特征提取与跨域传播块

主网络为标准的 U‑Net 结构，由多个编码层和解码层组成，每一层内部嵌入 **跨域传播块 (CDPB)**。CDPB 是 PG‑SVRT 的核心计算单元，由 CDPA 与 MDFFN 两部分构成（图 4）：

1. **CDPA** 执行“先空间、后时间”的渐进式注意力：对输入特征 $Y_{N1}$ 进行线性投影得到查询 $Q_{N1}$、键 $K_{N1}$ 和值 $V_{N1}$，首先在空间域利用桥接令牌 $B_s$ 进行两级注意力计算，得到空间增强特征 $Y_s^{out}$；随后，将 $Y_s^{out}$ 作为共享值传入时间注意力模块，与时间维度的查询 $Q_t$ 和键 $K_t$ 交互，输出跨域传播后的特征 $Y_t^{out}$。值共享机制使得空间域的精炼信息直接参与时间聚合，避免了简单串行带来的信息衰减。

2. **MDFFN** 将光谱特征沿头维度拆分，分别在空间子域和时间子域执行独立的自注意力，再进行融合。相比常规的 MLP 或 3D 卷积前馈网络，这种分域处理策略增强了对空间纹理和时间运动特征的针对性提取能力。

### 多帧协同与输出

整个流水线以滑动窗口方式处理连续帧序列，每一帧的重建不仅依赖自身测量，还借助相邻帧的互补编码信息——在固定物理掩码下，相邻帧中被遮挡或混叠的光谱成分可通过时空特征传播得到补偿。网络最终输出与输入帧数相同的高光谱视频立方体，并通过残差连接与 shuffle 操作在光谱维度对齐退化特征与测量值，保持端到端的训练一致性。

### 补充图表

![[assets/figures/papers/paper_list_l820_https_arxiv_org_abs_2603_00611/figures/003_Figure_3.jpg]]
*Figure 3: Illustration of PG-SVRT. (a) and (c) The components of MGDP and CDBP. (b) PG-SVRT framework and key components*

![[assets/figures/papers/paper_list_l820_https_arxiv_org_abs_2603_00611/figures/001_Figure_1.jpg]]
*Figure 1: Spectral compressive imaging and reconstruction. (a) SCI principle. (b) Image-based methods, with issues of uncertain reconstruction and temporal inconsistency (flickering intensity curves). (c) Video-based reconstruction, where information complementarity enhances completeness and temporal consistency (smooth intensity curves)*



PG-SVRT 以 U-Net 为主干架构，由三个关键组件构成：**MGDP**（Mask-Guided Degradation Perception，掩码引导的退化感知）、**CDPA**（Cross-Domain Propagated Attention，跨域传播注意力）和 **MDFFN**（Multi-Domain Feed-Forward Network，多域前馈网络）。整体框架如 Figure 3 所示。

### 5.1 MGDP：掩码引导的退化感知

压缩光谱成像的物理过程可统一建模为线性系统：

$$Y_i = \Psi X_i + \Theta$$

其中 $\Psi$ 为编码算子，$\Theta$ 为噪声。在单色散器（SD）和双色散器（DD）架构下，测量值的具体形式分别为：

$$Y_i(h,w) = \sum_{c=1}^{C} \Phi(h,w) \cdot X_i(h,w-\sigma(c),c) \quad \text{(SD)}$$

$$Y_i(h,w) = \sum_{c=1}^{C} \Phi(h,w-\sigma(c)) \cdot X_i(h,w,c) \quad \text{(DD)}$$

MGDP 的核心作用是**在特征进入主网络之前感知压缩退化过程**，辅助解耦帧内编码信息。其输入构造方式为：将掩码引导的退化感知特征与原始测量值在通道维拼接：

$$Y_{in} = \text{Concat}(\text{Conv}(W_m(\Phi, \Phi_p) \odot F_m(Y)), Y)$$

其中 $W_m(\cdot)$ 生成空间权重，$F_m(Y)$ 对测量值进行变换，$\odot$ 表示逐元素乘积。随后通过 Shuffle 操作将退化特征与测量值在光谱维度对齐，送入 U-Net 编码器-解码器进行多尺度恢复。

### 5.2 CDPA：跨域传播注意力

CDPA 是 PG-SVRT 的核心创新，采用**先空间后时间的渐进式注意力机制**，通过共享值（shared value）实现跨域特征传播。其内部结构如 Figure 4(a) 所示。

![[assets/figures/papers/paper_list_l820_https_arxiv_org_abs_2603_00611/figures/004_Figure_4.jpg]]
*Figure 4: Details of the CDPB, which consists primarily of CDPA and MDFFN. (a) CDPA is a spatial-then-temporal attention mechanism, where the blue line represents spatial feature processing and the red line indicates temporal feature processing. (b) Illustration of MDFFN*

**输入投影**：对输入特征 $Y_{N1}$ 进行线性投影得到查询、键和值：

$$Q_{N1} = Y_{N1} W_q, \quad K_{N1} = Y_{N1} W_k, \quad V_{N1} = Y_{N1} W_v$$

**空间注意力（含桥接令牌）**：为降低计算复杂度，引入桥接令牌 $B_s$，将空间注意力分解为两级计算：

$$Y_s^{out} = \text{GConv}\left( A(Q_s, B_s, A(B_s, K_s, V_s, \tau_1), \tau_2) \right) + Y_{N1}$$

其中 $A(\cdot)$ 为注意力函数，$\tau_1$、$\tau_2$ 为温度参数，GConv 为分组卷积，残差连接保证训练稳定性。

**时间注意力（值共享传播）**：以空间注意力输出 $Y_s^{out}$ 作为共享值，进行时间维度的注意力计算，实现跨域特征传播：

$$Y_t^{out} = A(Q_t, K_t, Y_t, \tau_3)$$

其中 $Y_t$ 由 $Y_s^{out}$ 派生而来，蓝色线表示空间特征处理，红色线表示时间特征处理。

**计算复杂度**：CDPA 的理论复杂度为：

$$O(\text{CDPA}) = 4THWC^2 + 4THWN_BC + 2T^2HWC$$

其中 $T$ 为帧数，$H$、$W$ 为空间尺寸，$C$ 为通道数，$N_B$ 为桥接令牌数量。桥接令牌通过提取 $Q$ 的核心信息与 $K$、$V$ 交互，将计算复杂度从常规窗口注意力的二次量级降至近似线性。当满足条件 $2N_B < H_{win} W_{win}$ 时，可在不损失性能的前提下有效降低计算量（消融实验证实 $N_B=64$ 时达到最优）。

### 5.3 MDFFN：多域前馈网络

MDFFN 替代常规 FFN，将光谱特征划分为多个头（head），**分别在空间域和时间域独立执行自注意力**，最后进行融合，有效增强域内特征提取能力。其结构如 Figure 4(b) 所示。消融实验表明，相比普通 3D 卷积或单域处理，MDFFN 在 PSNR 和 SAM 指标上均有提升（Table 6）。



## 实验与关键发现

### 实验设置与评估协议

PG-SVRT 在两种数据集上进行评估：公开的 **KAIST** 数据集和本文新构建的 **DynaSpec** 动态高光谱视频数据集。模拟实验统一采用 **DD-CASSI** 系统架构，光谱通道数设置为 30（覆盖 500–650 nm 波段）。评估指标覆盖三个维度：**PSNR** 和 **SSIM** 衡量空间重建质量，**SAM** 衡量光谱保真度，**ST-RRED** 衡量时序一致性（数值越低表示时序越稳定）。对比方法包括图像级压缩光谱重建方法 **CST**（Cai et al., CVPR 2022）、**MST**（Cai et al., ECCV 2022）、**s2-Transformer**（Wang et al., TPAMI 2025）、**DADF**（Cai et al., NeurIPS 2022）、**DPU**（Zhang et al., CVPR 2024），以及视频恢复方法 **VRT**（Liang et al., TIP 2024）。

### 主实验结果

如 **Table 2** 所示，PG-SVRT 在两个数据集上全面领先所有对比方法。在 KAIST 数据集上，PG-SVRT 取得 **41.23 dB** PSNR 和 **19.35** ST-RRED，分别代表最优的空间重建质量和时序一致性。在 DynaSpec 数据集上，PSNR 进一步提升至 **41.82 dB**，SSIM 达到 **0.9904**，表明模型在动态场景下具有更强的重建能力。

![[assets/figures/papers/paper_list_l820_https_arxiv_org_abs_2603_00611/figures/007_Table_2.jpg]]
*Table 2: Quantitative comparisons of several SOTA methods and PG-SVRT. The suffix -K denotes results on the KAIST, while -D represents evaluations on the DynaSpec testset. The best and second best results are highlighted in bold and underline, respectively*

值得注意的是，PG-SVRT 作为视频级模型，其参数量仅为 **2.48M**，每帧计算量 **28.18 GFLOPs**，低于多数图像级方法（如 MST 的 28.53 GFLOPs）。这得益于跨域传播注意力（CDPA）中桥接令牌机制带来的计算效率提升——在满足 $2 N_B < H_{win} W_{win}$ 的条件下，复杂度从二次降低到近似线性。

**Figure 6** 的可视化对比进一步验证了定量结果：PG-SVRT 在细节放大区域展现出更清晰的结构，与真值的差异图（difference map）几乎不可见，而图像级方法在光谱曲线（intensity curves）上存在明显的帧间抖动（flickering），暴露了逐帧独立处理带来的时序不一致性。

在真实测量数据上的重建（**Figure 7**），PG-SVRT 生成的伪 RGB 图像在全波段均保持高保真度，复杂纹理场景（**Figure 8**）中的细微结构亦得到清晰恢复。

![[assets/figures/papers/paper_list_l820_https_arxiv_org_abs_2603_00611/figures/011_Figure_7.jpg]]
*Figure 7: Reconstruction of real measurements using comparison methods and PG-SVRT, with pseudo-RGB images generated from the reconstructed HSIs to assess reconstruction quality across all bands. Compared to other methods, PG-SVRT results exhibit fewer artifacts*

![[assets/figures/papers/paper_list_l820_https_arxiv_org_abs_2603_00611/figures/012_Figure_8.jpg]]
*Figure 8: Complex real-world scenes reconstructed by PG-SVRT show clear structures and fine details in both the pseudo-RGB and HSIs*

### 消融实验

#### 模块贡献分析

**Table 3** 的逐步消融揭示了各模块的因果贡献。基线模型（无 MGDP、CDPA 和 MDFFN）的 PSNR 为 **39.97 dB**。依次引入 CDPA、MGDP 和 MDFFN，PSNR 分别提升至 **41.30 dB**、**41.41 dB** 和 **41.52 dB**。CDPA 带来的增益最大（+1.33 dB），验证了时空特征传播是突破单帧重建瓶颈的核心机制。MGDP 通过建模压缩退化过程辅助解耦帧内编码信息，进一步提升了重建精度。MDFFN 通过分头独立提取空间与时间特征后融合，相比常规前馈网络带来额外增益。

#### 时空处理策略对比

**Table 4** 比较了不同时空处理顺序与传播策略。空间-时间渐进式处理配合价值共享传播（S-T w/P）取得最优 **PSNR 41.52 dB** 和最低 **ST-RRED 23.25**。相比之下，并行处理（Parallel）缺乏域间交互，PSNR 下降 0.21 dB；时间-空间顺序（T-S w/P）因时间注意力先行而无法充分利用空间特征，性能亦有所下降。去除价值共享传播（S-T w/o P）导致 PSNR 降低 0.15 dB，证明共享值机制是跨域特征融合的关键。

#### 桥接令牌数量分析

**Table 5** 展示了桥接令牌数量 $N_B$ 对性能与效率的影响。当 $N_B = 64$ 时，模型在满足 $2 N_B < H_{win} W_{win}$ 的条件下达到最优 **PSNR 41.52 dB** 和最低 **ST-RRED 23.25**。过少的桥接令牌（如 $N_B = 16$）导致信息瓶颈，PSNR 降至 41.37 dB；过多的令牌（如 $N_B = 128$）则违背线性复杂度条件，计算量上升但性能不再提升。

#### 多域前馈网络设计

**Table 6** 对比了 MDFFN 的不同设计。空间与时间独立自注意力后融合的方案在 PSNR 和 SAM 上均优于普通 3D 卷积或仅单域处理的设计，验证了分域独立建模再融合策略对多域特征提取的有效性。

### 不同 SCI 系统的适应性

**Table 1** 展示了 PG-SVRT 在统一数学框架下对不同 SCI 架构的求解能力。DD-CASSI 系统在 PSNR（**41.52 dB**）和 SSIM（**0.9893**）上均取得最高重建质量，这与双色散器架构提供更丰富空间编码信息的物理特性一致。**Figure 5** 展示了各系统的测量图像差异，DD-CASSI 的测量图保留了更多空间结构，为重建提供了更强的先验约束。

### 局限性与失败模式

尽管 PG-SVRT 在模拟和受控真实场景下表现优异，但仍存在以下局限：

1. **数据集覆盖有限**：DynaSpec 数据集在室内手动控制条件下采集，场景多样性和真实非约束动态的覆盖不足，模型在室外复杂场景下的泛化能力仍需验证。
2. **系统验证不完整**：真实系统原型仅针对 DD-CASSI 构建，未对其他 SCI 系统进行物理验证，综合适应性尚不明确。
3. **光谱范围受限**：模拟实验限定在 500–650 nm（30 通道），全光谱范围的重建能力未经测试。
4. **硬件依赖**：模型依赖掩码先验和特定光谱校准，当相机硬件或照明条件改变时可能需要重新标定或微调。

### 待验证问题

- 时空特征传播机制能否泛化到其他压缩感知系统（如视频快照压缩成像）？
- 在极低光照或强噪声条件下，互补帧信息的可靠性是否会显著下降？
- 如何将神经渲染或物理模型融入以进一步提升真实场景的细节重建？

### 补充图表

![[assets/figures/papers/paper_list_l820_https_arxiv_org_abs_2603_00611/figures/008_Table_3.jpg]]
*Table 3: Break-down ablation study of PG-SVRT, "+" indicates adding or replacing modules relative to the baseline*

![[assets/figures/papers/paper_list_l820_https_arxiv_org_abs_2603_00611/figures/009_Table_4.jpg]]
*Table 4: Comparison of spatiotemporal processing strategies*

![[assets/figures/papers/paper_list_l820_https_arxiv_org_abs_2603_00611/figures/013_Table_5.jpg]]
*Table 5: Ablation on the number of bridged tokens*

![[assets/figures/papers/paper_list_l820_https_arxiv_org_abs_2603_00611/figures/010_Figure_6.jpg]]
*Figure 6: Reconstruction results of PG-SVRT and comparison methods on the KAIST and DynaSpec test sets. The bottom-left corner of each subplot presents an enlarged detail view, while the bottom-right corner shows the difference with the GT. It is evident that, while all methods benefit from DD-CASSI and are able to recover structural details, our method achieves the superior fidelity*

![[assets/figures/papers/paper_list_l820_https_arxiv_org_abs_2603_00611/figures/005_Table_1.jpg]]
*Table 1: Quantitative comparison of representative SCI architectures. All systems are solved via PG-SVRT under a unified mathematical framework to exclude algorithmic bias*

![[assets/figures/papers/paper_list_l820_https_arxiv_org_abs_2603_00611/figures/006_Figure_5.jpg]]
*Figure 5: Measurements of different SCI systems*



## 定位与知识库关联

### 从单帧图像到多帧视频的重建范式迁移

压缩光谱重建领域长期以单帧图像为处理单元，代表性工作包括 **CST** (Cai et al., CVPR 2022)、**MST** (Cai et al., ECCV 2022)、**s2-Transformer** (Wang et al., TPAMI 2025)、**DADF** (Cai et al., NeurIPS 2022) 和 **DPU** (Zhang et al., CVPR 2024)。这些方法的核心瓶颈在于：单帧编码测量中空间-光谱信息因色散位移而高度混叠，逐帧独立重建时缺乏跨帧信息补偿，导致两个固有问题——恢复不确定性（同一测量可能对应多种光谱解）和时间不一致性（相邻帧光谱强度曲线出现不应有的抖动，如 Figure 1(b) 所示）。

PG-SVRT 的关键范式转换在于将学习范围从单帧图像扩展至多帧视频序列，利用相邻帧间固定的编码模式产生的互补特征来补偿被遮挡信息。这一思路与视频恢复方法 **VRT** (Liang et al., TIP 2024) 共享了利用时序冗余的动机，但 PG-SVRT 的独特之处在于其互补性来源于物理编码过程本身（色散导致的像素位移），而非场景运动估计或光流对齐。

### 注意力机制的谱系定位：从空间自注意力到跨域价值传播

在注意力设计上，现有图像级方法普遍采用空间自注意力（如窗口自注意力、通道注意力），其感受野局限于单帧空间维度。PG-SVRT 提出的 **CDPA（Cross-Domain Propagated Attention）** 实现了两个关键升级：

1. **空间-时间渐进式注意力**：先进行空间注意力以恢复帧内细节，再将空间输出作为共享值（shared value）馈入时间注意力，实现从空间域到时间域的特征传播。消融实验（Table 4）表明，这种 S-T w/P 顺序相比并行处理（PSNR 41.15 dB）或 T-S 顺序（PSNR 40.82 dB）均取得最优结果（PSNR 41.52 dB），验证了渐进式跨域传播的必要性。

2. **桥接令牌（Bridged Tokens）的线性复杂度**：常规窗口注意力计算复杂度随窗口大小平方增长。CDPA 引入少量可学习的桥接令牌 $B_s$，先与查询 $Q_s$ 交互提取核心信息，再与键 $K_s$ 和值 $V_s$ 交互，将空间注意力的计算路径从直接 $QK^T$ 分解为两级低秩近似。理论上当 $2 N_B < H_{win} W_{win}$ 时（$N_B$ 为桥接令牌数，$H_{win}W_{win}$ 为窗口内 token 数），CDPA 可在不损失性能的前提下降低计算量。消融实验（Table 5）证实 $N_B=64$ 时达到最优 PSNR 41.52 dB 和最低 ST-RRED 23.25，同时满足上述复杂度条件。

### 前馈网络与退化感知的差异化设计

**MDFFN（Multi-Domain Feed-Forward Network）** 替代了标准 FFN 中的单域 MLP 或卷积。其设计要点在于将光谱特征分头（split heads），各头独立执行空间自注意力和时间自注意力，再进行融合。消融实验（Table 6）显示，这种分域独立处理后融合的策略优于普通 3D 卷积或单域处理，在 PSNR 和 SAM 指标上均有提升。

**MGDP（Mask-Guided Degradation Perception）** 则直接建模压缩退化过程。它利用编码掩码 $\Phi$ 及其物理位移模式 $\Phi_p$，通过卷积生成退化感知特征，再与原始测量值 $Y$ 拼接作为主网络输入（Eq. 4）。这一设计将物理先验显式注入学习过程，辅助解耦帧内编码信息。模块消融（Table 3）显示，逐步添加 MGDP、CDPA 和 MDFFN 将 PSNR 从基线 39.97 dB 依次提升至 41.30 dB、41.41 dB 和 41.52 dB，各模块增益独立可验证。

### 适用边界与未经验证的假设

**已验证的适用范围**：
- 仿真实验在 DD-CASSI 系统下进行，光谱通道数限定为 30（500-650 nm），重建帧数固定为 5 帧序列。
- 真实物理原型仅针对 DD-CASSI 构建，未对其他 SCI 系统（如 SD-CASSI）进行物理验证。Table 1 虽在统一数学框架下比较了多种 SCI 架构，但该比较仅限仿真层面，综合适应性尚不明确。
- DynaSpec 数据集通过手动控制物体运动采集（如 Figure 2(a) 所示），30 个室内场景的多样性和非约束动态覆盖有限。

**需要谨慎外推的场景**：
- 极低光照或强噪声条件下，互补帧信息的可靠性可能显著下降，因为掩码调制信号本身信噪比降低会削弱跨帧互补性。
- 当相机硬件或照明条件改变时，模型依赖的掩码先验和光谱校准可能需要重新标定或微调，泛化成本未在论文中评估。
- 全光谱范围（超出 500-650 nm）的重建能力未经测试，光谱维度的可扩展性存疑。

### 开放问题与后续方向

1. **跨系统泛化**：CDPA 的时空特征传播机制能否泛化到其他压缩感知系统（如视频快照压缩成像 CACTI）？当前仅在 CASSI 架构下验证，其依赖的色散位移互补性在其他编码模式下是否仍然成立需要进一步研究。

2. **真实场景鲁棒性**：DynaSpec 数据集能否扩展至更多光谱波段、更高时间和空间分辨率？当前室内受控采集与室外非约束动态场景之间存在显著域差距，模型在复杂光照、大运动幅度下的表现尚待验证。

3. **物理模型融合**：MGDP 目前仅使用掩码先验进行退化感知，能否将神经渲染或更精细的物理成像模型融入以进一步提升真实场景的细节重建？这可能是弥合仿真-真实差距的关键路径。

4. **计算效率的进一步优化**：虽然 PG-SVRT 以 2.48M 参数和每帧 28.18 GFLOPs 实现了高效推理，但桥接令牌机制本质上是一种低秩近似，其信息压缩比与重建精度的理论边界尚未被严格刻画。



## 原文 PDF

![[paperPDFs/CVPR_2026/Exploring_Spatiotemporal_Feature_Propagation_for_Video_Level_Compressive_Spectral_Reconstruction_Dataset_Model_and_Benchmark.pdf]]
