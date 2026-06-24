---
title: "Taming Hierarchical Image Coding Optimization: A Spectral Regularization Perspective"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/Taming_Hierarchical_Image_Coding_Optimization_A_Spectral_Regularization_Perspective.pdf
aliases:
- DRESRHC
- THICOSRP
tags:
- ICLR_2026
- topic/other_unclear
- topic/other_unclear/general
core_operator: "显式光谱正则化方案：尺度内频率正则化（DCT基础的渐进频谱截断）强制各尺度专注于目标频带；尺度间潜在正则化（DWT+Conv的L2惩罚）抑制跨尺度频谱混叠，两者仅在训练时使用，推理无开销。"
primary_logic: "通过训练动态的光谱分析揭示了违反频率原则的现象；提出的正则化引导模型实现自然的低-to-高频率分层，使各尺度解耦，从而显著加快收敛（2.3×）并提升率失真性能。"
claims:
- "结合尺度内和尺度间正则化，与无正则化的基线相比，训练加速2.30倍，BD-Rate提升-10.11%（相对VTM-22.0）"
- "尺度内正则化（线性0.05→1.0）在早期阶段稳定各尺度频率收敛，加速1.84倍，BD-Rate -1.07%"
- "尺度间正则化（DWT+Conv与L2损失）有效缓解频谱混叠，取得-7.66% BD-Rate"
- "正则化训练产生清晰的解耦粗到细的层次结构，消除了朴素训练中的频谱色散和噪声（图1）"
---

# Taming Hierarchical Image Coding Optimization: A Spectral Regularization Perspective

> [!tip] 核心洞察
> 通过训练动态的光谱分析揭示了违反频率原则的现象；提出的正则化引导模型实现自然的低-to-高频率分层，使各尺度解耦，从而显著加快收敛（2.3×）并提升率失真性能。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 驯服分层图像编码优化：光谱正则化视角 |
| 英文题名 | Taming Hierarchical Image Coding Optimization: A Spectral Regularization Perspective |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=lO6I66lweK) |
| Topic | #topic/other_unclear #topic/other_unclear/general |
| Method | DHIC-Regu (Explicit Spectral Regularization for Hierarchical Coding) |
| Dataset | Kodak, CLIC Pro, Tecnick, 三数据集平均 |

> [!tip] 效果简介
> - Kodak 上，BD-Rate (相对于VTM-22.0) 为 -19.73%，对比 VTM-22.0 (anchor)，变化 -19.73%。
> - CLIC Pro 上，BD-Rate (相对于VTM-22.0) 为 -18.13%，对比 VTM-22.0，变化 -18.13%。
> - Tecnick 上，BD-Rate (相对于VTM-22.0) 为 -24.09%，对比 VTM-22.0，变化 -24.09%。

## 概述

现有分层图像编码（Hierarchical Image Coding）通过多尺度潜在变量联合优化率失真目标，但朴素端到端训练**忽略了跨尺度信息分配的固有结构**，导致**光谱能量散射（spectral dispersion）与光谱混叠（spectral aliasing）**——不同尺度之间产生冗余频率分量，造成训练不稳定、收敛缓慢且压缩性能受限。本文从**光谱正则化（Spectral Regularization）**视角提出显式训练约束方案 **DHIC-Regu**，包含两个互补组件：（1）**尺度内频率正则化**，基于DCT的渐进频谱截断，强制各尺度专注其目标频带，引导自然的低‑高频率学习顺序；（2）**尺度间潜在正则化**，利用DWT＋1×1卷积对齐相邻尺度潜变量并施加L2惩罚，抑制跨尺度光谱混叠。两种正则化**仅在训练时使用**，推理阶段无任何额外计算或参数开销，保持与无正则化基线完全相同的复杂度。

**核心结论**：光谱分析揭示朴素训练违反频率原则；正则化训练使各尺度解耦，形成清晰的粗到细层次结构（图1），**显著加速收敛并提升率失真性能**。实验表明，引入全量正则化后，模型**训练加速2.30倍**，在Kodak、CLIC Pro、Tecnick三个标准数据集上相对VTM‑22.0的**平均BD‑Rate达到‑20.65%**，较无正则化基线额外降低10.11%码率（表1、表2）。消融实验确认：尺度内正则化主导收敛加速（1.84倍），尺度间正则化主导码率节省（BD‑Rate ‑7.66%）。该方法**专为显式多尺度层次架构设计**，对单尺度VAE的直接迁移效果有限，且尺度内正则化对最终率失真的增益较弱，整体提升主要依赖尺度间正则化。

## 背景与动机

深度学习驱动的图像压缩近年来取得了长足进步，以 ELIC、MLIC++ 为代表的单尺度自编码器架构通过端到端率失真优化已显著超越传统编码标准 VTM-22.0。然而，这类方法在潜在空间中缺乏对图像多尺度特性的显式分解，未能充分利用自然图像从粗到细的结构先验。分层图像编码（Hierarchical Image Coding）通过多个尺度的潜在变量 $\mathbf{z}_1,\dots,\mathbf{z}_L$ 分别建模不同分辨率的信息，理论上能够实现更优的频率解耦与压缩效率。代表性的分层架构如 DHIC 和 QARV 试图构建这类显式尺度层级，但实际训练中却面临着严峻的频谱失控问题。

如图 1 所示，在朴素端到端优化下，各尺度潜在变量的频率能量呈现出明显的**光谱散射（spectral dispersion）与跨尺度频谱混叠（spectral aliasing）**——不同尺度之间出现冗余的频率分量叠加，导致无法形成清晰的低-高频分层结构。这一现象违背了深层网络学习中的频率原则（Frequency Principle，即网络应优先捕获低频信息再逐步精细化高频），其根源在于标准分层损失 $\mathcal{L}_{hier} = \sum_{l} R(\mathbf{z}_l) + \lambda D(\mathbf{x}, \hat{\mathbf{x}})$ 仅优化整体重建质量，没有对信息在尺度间的分配施加任何约束。由此引发的训练不稳定、收敛迟缓以及压缩性能严重受限（无正则化基线 DHIC-Base 的 BD-Rate 增益有限）构成了现有分层编码优化的核心瓶颈。

针对上述缺口，本文通过追踪训练过程中的光谱能量动态，首次提出从**光谱正则化**视角驯服分层编码优化。核心动机在于：若能在训练早期强制各尺度专注各自的目标频带，并在后期抑制跨尺度的冗余频率分量，则有望引导模型自然形成从低频到高频的解耦层次。为此，本文设计了双阶段显式正则化策略——**尺度内频率正则化**（基于 DCT 的渐进频谱截断，稳定早期频带收敛）与**尺度间潜在正则化**（基于 DWT 与 $\mathrm{L}_2$ 惩罚，缓解后期频谱混叠），二者仅在训练阶段使用，不增加推理开销。实验表明，该方案可使相同分层架构下的训练收敛速度提升 2.3 倍，并将相对于 VTM-22.0 的平均 BD-Rate 从 $-11.16\%$ 大幅推至 $-20.65\%$，验证了显式光谱引导对于释放分层编码潜力的必要性与有效性。

## 核心创新

DHIC-Regu 的核心创新在于**通过显式光谱正则化明确引导分层模型的跨尺度信息分配**，解决朴素端到端训练中因忽略频率原则而导致的频谱能量散射与混叠问题，从而在训练加速和率失真性能上大幅超越无正则化的基线 DHIC-Base。该方案包括两个互补的正则化器以及配套的训练阶段划分，**仅在训练时生效**，推理期间完全不引入额外开销。

### 关键创新机制

1. **尺度内频率正则化（Intra-scale Regularization）**  
   针对早期训练中各尺度频率收敛速率不一、频谱相互泄露的现象，采用基于离散余弦变换（DCT）的**渐进频谱截断**对输入图像进行预处理。通过时变软径向掩膜$\mathbf{M}(u,v;t)$定义保留频率半径$\tau(t)$，训练初期仅向编码器提供极低频信息，随后逐步扩大截止半径直至全频带。该方法强制各尺度在训练前期就收敛到其目标频率带，阻止高频分量过早介入而导致频谱分散。该策略带来了 **1.84× 的训练加速**（Table 2），但对最终率失真的贡献有限（约 -1.07% BD-Rate）。

2. **尺度间潜在正则化（Inter-scale Regularization）**  
   在训练后期，通过在相邻尺度潜在变量之间施加**基于离散小波变换（DWT）的相似性惩罚**来抑制跨尺度频谱混叠。具体而言，对低一尺度的潜在变量 $\mathbf{z}_{l-1}$ 执行 Haar DWT 及 $1\times1$ 卷积以对齐频率通道，再与高一尺度潜在变量 $\mathbf{z}_l$ 计算 $L_2$ 距离并作为负惩罚项加入总损失（见 Eq. (6)）。这一约束鼓励粗尺度潜在变量不重复编码已由细尺度携带的低频内容，使各尺度实现清晰的粗‑细解耦。该模块单独应用时虽未加快训练（加速倍率 0.91×），却取得了**显著的 -7.66% BD-Rate**（Table 2），是整体性能提升的主要来源。

3. **阶段性训练调度**  
   训练被明确划分为前后两个阶段（自第 1 epoch 至约第 100 epoch 应用尺度内正则化，后续 switch 至尺度间正则化），以匹配训练早期需要稳定频率收敛、后期需要消除混叠的实际需求（Section 3.1）。这一调度使得两个正则化器耦合后发挥最大功效：**训练加速 2.30×，同时 BD-Rate 增益达 -10.11%**（Table 2）。

### 相对基线的关键改动（Changed Slots）

| 改动维度 | DHIC‑Base（基线） | DHIC‑Regu（本文） | 作用阶段与证据 |
|:---|:---|:---|:---|
| **训练输入** | 原始全频谱图像 | 经 DCT + 渐进掩膜 $\mathbf{M}(u,v;t)$ 截断的频谱重建图像（Eq. (3)–(5)） | 仅前 100 epochs；实现尺度内频率引导（Section 3.2） |
| **训练损失** | $\mathcal{L}_{\mathrm{hier}} = \sum R(\mathbf{z}_l) + \lambda\cdot D(\mathbf{x},\hat{\mathbf{x}})$ | $\mathcal{L}_{\mathrm{hier\_regu}} = \sum R(\mathbf{z}_l) + \lambda\cdot D - \delta\sum L_2(\mathbf{z}_{l-1}, \mathrm{Conv}_{1\times1}(\mathrm{DWT}(\mathbf{z}_l)))$ （Eq. (6)） | 后期训练；抑制频谱混叠（Section 3.3） |
| **训练调度** | 无明确阶段划分 | 早期（~100 epochs）执行尺度内正则化；后期执行尺度间正则化 | 全程；二者互补增益（Section 3.1，Table 2） |

> **注**：上述改动**仅存在于训练流程**，推理时不需任何修改，因此 DHIC‑Regu 与 DHIC‑Base 的推理复杂度完全相同（解码时间 68.48 ms，KMACs/pixel 977.73，参数量 106.93 M，参见 Table 1），兼顾了性能与部署效率。

### 创新效果与证据强度

- 联合正则化将 BD-Rate 从 DHIC‑Base 的 -11.16% 提升至 -20.65%（三数据集平均，Anchor VTM‑22.0），训练收敛速度提高 2.30 倍（Table 2，置信度 0.95）。
- 训练动态可视化（Figure 1）清楚显示：正则化后各尺度潜在变量形成**解耦的低‑中‑高频分层结构**，而基线训练则出现频谱能量散射、噪声及混叠。
- 消融实验进一步确认了各组件的最优实现选择：尺度内正则化采用线性调度（0.05→1.0）获得最高加速（Table 3a）；尺度间正则化使用 DWT+Conv 搭配 $L_2$ 损失优于其他变换和度量（Table 3b）；正则化权重 $\delta=0.1$ 时 BD-Rate 增益最大（-11.50%，Table 6）。

### 局限性与注意事项

- 两种正则化器均专门针对**显式分层架构**设计，对单尺度 VAE（如 HPCM、MLIC++）可能无效甚至导致性能下降（Table 10），表明方法不具有通用性。
- 尺度内正则化主要用于加速收敛，单独使用时最终压缩性能提升有限（约 -1% BD-Rate）；整体增益高度依赖尺度间正则化。
- 关键超参数（$\delta=0.1$、阶段切换 epoch、频率截断调度）依赖**手动网格搜索**，尚未探索自适应调度或自动优化策略。

## 整体框架

![[assets/figures/papers/iclr26_0014_lO6I66lweK_Taming_Hierarchical_Image_Coding_Optimization_A/figures/021_Figure_9.jpg]]
*Figure 9: Our proposed lightweight hierarchical image codec architecture. The above is the overall network framework, where the three rows from top to bottom are the encoding pathway, entropy model pathway, and decoding pathway. And the shaded area represents the FSP module, which has been proven to be unnecessary in Appendix A.4. The lower left corner shows the network structure of the latent block in the entropy model, while the bottom right corner shows the structure of the basic model employed in our whole architecture*

DHIC-Regu (Explicit Spectral Regularization for Hierarchical Coding) 的核心是一个四尺度的分层图像编解码器（DHIC-Base），并在训练中嵌入了两组仅在训练时生效的光谱正则化模块。其设计目标在于解决朴素分层优化中出现的频谱能量散射与跨尺度混叠，从而将训练加速 **2.30×** 并将 VTM‑22.0 锚点下的平均 BD‑Rate 推进至 **‑20.65%**（Table 1；Table 2）。

### 基础分层编解码架构
遵循典型的可学习图像压缩框架，DHIC 管线包含三个通路（Figure 9）：
1. **编码通路（$g_a$）**：输入图像 $\mathbf{x}$ 经多尺度编码器生成从细到粗的 4 个尺度潜在变量 $\mathbf{z}_1,\dots,\mathbf{z}_4$。每个尺度以更低的空域分辨率表示更高层的语义信息。
2. **熵模型与超先验通路**：利用超先验 $\mathbf{z}$ 与尺度间自回归条件对量化后的潜在变量进行概率建模，$p(\mathbf{z}_{1:L}) = p(\mathbf{z}_0) \prod_{l=1}^{L} p(\mathbf{z}_l \mid \mathbf{z}_{l-1})$（Eq.(7)）。该层级的先验分解是尺度间正则化设计的理论依据。
3. **解码通路（$g_s$）**：从量化后的分层潜在变量重构图像 $\hat{\mathbf{x}}$。

推理时的损失函数为不含正则化的层级率失真目标：  

$$
\mathcal{L}_{\text{hier}} = \sum_{l=1}^{L} R(\mathbf{z}_l) + \lambda \cdot D(\mathbf{x}, \hat{\mathbf{x}})
$$

式中 $D(\cdot,\cdot)$ 为重建失真，$R(\cdot)$ 为各尺度比特消耗（Eq.(2)）。

### 训练时的正则化引入
针对 Figure 1 揭示的朴素训练中频谱色散、噪声以及跨尺度频谱混叠（不同尺度出现冗余低频分量），作者引入了两种互补的正则化手段，且二者均**仅在训练阶段生效，推理时不增加任何开销**。

#### 1. 尺度内频率正则化：DCT 渐进频谱截断
在训练早期的前 100 个 epoch，对输入图像的频谱进行可控的渐进截断（Figure 4）：
- 先将 $\mathbf{x}$ 变换至 DCT 频域 $\mathbf{F}$（Eq.(3)），通过一个时变的径向软掩膜 $\mathbf{M}(u,v;t)$ 截断高频分量（Eq.(4)），再经逆 DCT 恢复为空域图像 $\tilde{\mathbf{x}}$（Eq.(5)）。
- 掩膜半径 $\tau(t)$ 随训练逐步增大（例如线性或指数调度，Tables 3a），迫使低尺度（$l$ 较大）只能接触到全局低频结构，而高尺度逐步学会建模高频细节。该策略实现 **1.84× 的训练加速**与约 **‑1.07% 的 BD‑Rate** 增益（Table 2）。

#### 2. 尺度间潜在正则化：DWT + 1×1 卷积对齐与 L₂ 惩罚
在训练后期，抑制不同尺度间残留的频谱混叠（Figure 5）：
- 对相邻的两个潜在变量，将较粗尺度的 $\mathbf{z}_{l-1}$ 经过**离散小波变换（DWT）** 分解为子带，再使用 $1\!\times\!1$ 卷积进行通道维度的线性重组，使其与较精细尺度 $\mathbf{z}_l$ 的频率通道对齐。
- 在训练损失中加入负的 L₂ 惩罚项，鼓励 $\mathbf{z}_{l-1}$ **不可预测** $\mathbf{z}_l$ 中已包含的低频内容，从而实现解耦：

$$
\mathcal{L}_{\text{hier\_regu}} = \mathcal{L}_{\text{hier}} - \delta \cdot \sum_{l=1}^{L} L_2\bigl(\mathbf{z}_{l-1},\; \text{Conv}_{1\times1}(\text{DWT}(\mathbf{z}_l))\bigr)
$$

该惩罚与 Eq.(8) 所示的条件高斯假设一致，将最大化对数似然等价于最小化 L₂ 距离。消融实验表明，此机制单独贡献 **‑7.66% BD‑Rate**（Table 2），且权重 $\delta=0.1$ 时取得最佳综合性能（Table 6）。

### 数据流与训练调度
整个训练过程分为两个阶段：**第一阶段（前 100 epochs）** 应用尺度内正则化，稳定各尺度的频率带收敛；**第二阶段** 切换至尺度间正则化，消除混叠，同时尺度内截断掩膜完全开放（即不再截断，直接使用原始图像）。推理时两个正则化模块均被移除，模型退化为标准的 DHIC 架构，故复杂度与基线完全一致（解码时间 68.48 ms，KMACs/pixel 977.73，参数量 106.93 M；Table 1）。

综合来看，DHIC-Regu 通过显式的光谱正则化，从输入图像的频谱限制到潜在空间的跨尺度惩罚，形成了一个训练时专用的“频谱引导‑解耦”闭环，最终实现了清晰且解耦的低‑高频率层次（Figure 1, Figure 6），解锁了分层编码架构的固有潜力。

> ⚠️ **需人工核实处**：尺度间正则化中 DWT 与 $1\!\times\!1$ 卷积的具体实现组合（Haar 小波、通道数映射等）以及训练阶段切换边界（100 epochs）的证据分散在不同章节，建议在正式报告中对配置细节加以注释；此外，$L_2$ 惩罚前的负号与损失函数符号需对照原文 Eq.(6) 确认。

## 核心模块与公式推导

### 1. 关键模块设计

分层图像编码器(如DHIC‑Base)的朴素端到端训练会在跨尺度隐变量间引发**频谱能量散射**与**频谱混叠**：高、低层尺度错误地编码了重叠的频率分量，导致训练收敛缓慢且率失真性能受限(Figure 1, Table 2)。为显式引导各尺度解耦，DHIC‑Regu 引入两项仅训练期使用的光谱正则化模块，分别作用于输入空间和隐空间，推理时零额外开销。

**尺度内频率正则化模块(Intra‑scale Frequency Regularization)**  
旨在前100个epoch强制不同尺度聚焦于其目标频带，加速频率分工的收敛(加速1.84×, BD‑Rate −1.07%)。该模块以时变DCT频谱截断形式作用在训练输入上(Figure 4)。具体流程为：对输入图像  $\mathbf{x}$ 进行二维DCT变换得到系数 $\mathbf{F}$；利用一个随训练轮次  $t$ 增大的软径向掩膜 $\mathbf{M}(u,v;t)$ 对频率系数做渐进式截断，早期只保留极窄的低频带，随后逐步开放高频；最后通过逆DCT重建为“频谱受限”的训练图像 $\widetilde{\mathbf{x}}$。掩膜的截断半径由时变参数 $\tau(t)$ 控制（线性或指数调度，0.05 → 1.0），使得网络初期必须用高尺度（大分辨率）解码低频，中后期才承担全频谱。该机制消除了朴素训练中的异常频率混入与噪声(Figure 1)。

**尺度间潜在正则化模块(Inter‑scale Latent Regularization)**  
在后续epoch（100轮之后）切换为此模块，用于**抑制跨尺度频谱混叠**——即低尺度隐变量不应再携有高尺度已编码的冗余低频信息。具体实现(Figure 5)：对低层隐变量  $\mathbf{z}_l$ 施加离散小波变换(DWT, Haar基)分解为频带子带，再通过 1×1 卷积将子带重组、对齐到高层隐变量 $\mathbf{z}_{l-1}$ 的通道空间，最后计算两者间的  $L_2$ 相似性惩罚，并作为负项加入总损失(式 6)。该惩罚迫使命中率为解码器丢弃已被低层预测的低频成分，从而让高层隐变量保留“难以预测”的高频信息，实现自然的粗到细频率分层。消融实验中，DWT+Conv + $L_2$ 组合取得−7.66% BD‑Rate 的最优增益(Table 3b)。两项正则化联合使用带来 **2.30× 训练加速**与 **−10.11% BD‑Rate** 的综合提升(Table 2)。

### 2. 关键公式与变量解释

**分层率失真基线损失**  
$${\mathcal{L}}_{hier} = \sum_{l=1}^{L} R(\mathbf{z}_l) + \lambda \cdot D(\mathbf{x}, \hat{\mathbf{x}})$$
其中  $\mathbf{z}_l$ 为第 $l$ 尺度的隐变量(共 $L$ 个尺度)， $R(\cdot)$ 是熵编码比特率， $D(\cdot,\cdot)$ 是重建失真(如MSE)， $\lambda$ 控制率失真权衡。该损失未对尺度间进行任何约束，是正则化的对比基线。

**二维离散余弦变换**  
$$\mathbf{F} = P_H\,\mathbf{x}\,P_W^{\top}$$
$P_H$ 与 $P_W$ 分别为高度  $H$ 和宽度  $W$ 的正交DCT‑II基矩阵，满足：
$$(P_H)_{u,x} = \alpha_H(u)\cos\!\left(\tfrac{\pi(2x+1)u}{2H}\right),\quad 
(P_W)_{v,y} = \alpha_W(v)\cos\!\left(\tfrac{\pi(2y+1)v}{2W}\right),$$
归一化系数  $\alpha_K(k)=\sqrt{1/K}$ ( $k=0$ ) 或  $\sqrt{2/K}$ ( $k\geq1$ )。该变换将空域图像映射到DCT频谱，是下游频率截断的前提。

**时变软径向掩膜**  
$$\mathbf{M}(u,v;t) = \max\!\left(0,\; \frac{\tau(t)-\sqrt{(u/H)^2+(v/W)^2}}{\tau(t)}\right)$$
$(u,v)$ 为频域坐标， $\tau(t)$ 为第 $t$ 个epoch的有效截止频率(由调度策略逐步增大)。掩膜值在截止半径内线性衰减，半径外的频率被完全置零。截断后的频谱 $\widetilde{\mathbf{F}}=\mathbf{F}\odot\mathbf{M}$ 经逆DCT得到训练用的低频增强图像：
$$\widetilde{\mathbf{x}} = P_H^{\top}\,\widetilde{\mathbf{F}}\,P_W.$$

**层次正则化总损失**  
$${\mathcal{L}}_{hier\_regu} = \sum_{l=1}^{L} R(\mathbf{z}_l) + \lambda \cdot D(\mathbf{x}, \hat{\mathbf{x}}) - \delta \cdot \sum_{l=1}^{L} L_2\!\left(\mathbf{z}_{l-1},\; Conv_{1\times1}\!\big(DWT(\mathbf{z}_l)\big)\right)$$
式中  $\delta$ 为尺度间正则化强度(网格搜索得最优值 0.1)， $DWT(\cdot)$ 表示离散小波变换， $Conv_{1\times1}$ 为通道对齐的1×1卷积， $L_2(\cdot,\cdot)$ 度量两者相似性。该惩罚项被**减去**，即鼓励低层隐变量经对齐后仍与高层隐变量不相似，从而抑制低频信息重复编码。

**理论一致性**：将各尺度隐变量先验分解为层次条件分布
$$p(\mathbf{z}_{1:L}) = p(\mathbf{z}_0)\prod_{l=1}^{L} p(\mathbf{z}_l \mid \mathbf{z}_{l-1}),$$
并假设条件高斯模型 $\mathbf{z}_l \mid \mathbf{z}_{l-1} \sim \mathcal{N}(f(\mathbf{z}_{l-1}), \tau^2)$，则负对数似然等价为
$$-\log p(\mathbf{z}_l \mid \mathbf{z}_{l-1}) = \frac{1}{2\tau^2}\|\mathbf{z}_l - f(\mathbf{z}_{l-1})\|^2 + C,$$
即最大化条件概率等同于最小化 $L_2$ 误差。因此式 6 中的 $L_2$ 惩罚可视为在隐空间施加一个“去冗余”的条件高斯先验，使高层隐变量更难被低层信息预测，从而迫使各尺度编码互补频率成分。

综合来看，DCT截断（式 3‑5）在训练前期引导频率分配，DWT对齐+ $L_2$ 惩罚（式 6）在训练后期消除频谱混叠；二者分别在输入域和隐空间实现光谱正则化，构成该方法的核心优化机制。

## 实验与分析

### 主要结果：率‑失真与训练加速

表 1 汇总了 DHIC‑Regu 在 Kodak、CLIC Professional 和 Tecnick 三个标准图像集上相对 VTM‑22.0 的 BD‑Rate。DHIC‑Regu 分别达到 –19.73 %、–18.13 % 和 –24.09 %，平均 –20.65 %，显著优于所有对比的学习编码器，包括单尺度的 ELIC、MLIC++、HPCM‑Large 以及无正则化的分层基线 DHIC‑Base（平均 –11.16 %）。仅正则化的加入就额外降低了 9.49 个百分点的 BD‑Rate，说明光谱约束充分释放了分层编码的潜力。


![[assets/figures/papers/iclr26_0014_lO6I66lweK_Taming_Hierarchical_Image_Coding_Optimization_A/figures/008_Table_1.jpg]]
*Table 1: Compression performance and complexity comparison of learned image codecs across multiple datasets (Anchor: VTM-22.0)*

训练效率同样受益。表 2 显示，同时采用尺度内与尺度间正则化时，达到 DHIC‑Base 最终性能所需的训练轮次缩短为原来的 1/2.30，即 **2.30 倍加速**。推理阶段正则化模块完全移除，因此 DHIC‑Regu 的编解码时间、计算量（977.73 KMACs/pixel）和参数量（106.93 M）与 DHIC‑Base 一致，无额外开销。


![[assets/figures/papers/iclr26_0014_lO6I66lweK_Taming_Hierarchical_Image_Coding_Optimization_A/figures/018_Table_2.jpg]]

### 消融研究

#### 正则化成分的独立作用

表 2 将两种正则化解耦。  
- **仅尺度内正则化**：训练加速 1.84 倍，BD‑Rate 仅小幅下降 –1.07 %，说明其主要解决早期频率收敛不稳定问题，对最终压缩率贡献有限。  
- **仅尺度间正则化**：训练速度略有下降（加速比 0.91 倍），但 BD‑Rate 大幅降低 –7.66 %，证明抑制跨尺度频谱混叠是压缩增益的主要来源。  
- **二者联合**：取得 2.30 倍加速与 –10.11 % BD‑Rate，表明尺度内稳定与尺度间去混叠具有互补性。

#### 实现细节消融

尺度内正则化的截断调度（表 3a）对比了常数掩膜、线性增长（0.05→1.0）和指数增长。线性调度实现最高加速（1.84×）和最优 BD‑Rate（–1.07 %），验证了渐进引入高频分量最利于各尺度收敛到目标频带。

尺度间正则化的实现（表 3b）考察了下采样方式与相似度度量。在 Conv‑Stride、Down+Conv、DWT+Conv 三种下采样中，**DWT 结合 1×1 卷积**（对齐子带与通道）取得 –7.66 % BD‑Rate；度量函数方面，L2 损失显著优于 L1 与余弦相似度。该组合被用作最终方案。

正则化强度 δ 的消融（表 6）显示，δ = 0.1 时 BD‑Rate 最低（–11.50 %），过大或过小均导致性能回落，说明存在经验性的最优惩罚权重。

#### 模型复杂度与架构通用性

正则化增益在不同体量的分层编码器上均能保持。附录 Table 8 指出，在 356～978 KMACs/pixel 的三个复杂度级别下，引入正则化后 BD‑Rate 分别从 –1.74 %、–5.29 %、–11.16 % 进一步下降至 –6.89 %、–15.32 %、–19.73 %，同时训练加速 1.8～2.3 倍。此外，将提出的正则化策略迁移至另一种分层架构 **QARV**（Table 9），同样观察到一致的 BD‑Rate 改善，表明方法具有一定架构无关性（但单尺度架构无效，见下文失败模式）。

### 失败模式与局限性

1. **单尺度模型不适用**：本正则化依赖显式的多尺度潜在空间。强行用于单尺度 VAE（如 HPCM、MLIC++）会导致性能下降（Table 10）。原因在于单尺度潜在变量缺乏天然频率分解结构，频谱约束无法建立有意义的频率层次。
2. **尺度内正则化的最终增益有限**：尺度内正则化虽具强加速效果，但对最终 BD‑Rate 的提升仅约 –1 %，压缩收益几乎全部源于尺度间正则化。若资源极度受限，可仅保留尺度间约束。
3. **超参数手工设定**：正则化权重 δ（最优值 0.1）、截断起始比例 r₀ 等均通过网格搜索确定，未设计自适应调度或与其他超参数的联合优化，迁移到新架构时仍需调参。
4. **数据模态局限**：当前工作仅针对静态图像压缩，尚未扩展至视频、立体图像、3D 点云等多维或时序数据，方法在复杂维度分解上的有效性有待验证。

### 关键视觉证据与图表分析

图 1 的光谱能量热图从根本机制上解释了正则化的作用。朴素训练下，各尺度潜在变量的频率能量长期纠缠，出现发散、噪声和频谱混叠；正则化训练则从早期即强制引导各尺度收敛至指定频带，最终形成清晰的“粗‑中‑细”分层结构，去除了冗余频率分量。


![[assets/figures/papers/iclr26_0014_lO6I66lweK_Taming_Hierarchical_Image_Coding_Optimization_A/figures/001_Figure_1.jpg]]

图 6 的尺度潜在变量可视化进一步印证了这一过程：无正则化时，四个尺度的表示始终相互混杂；正则化后，在第 40 个训练轮次已可见明显的尺度解耦——高尺度专注低频全局结构，低尺度补充高频细节，实现了自然的层次化粗‑细表示。

率‑失真曲线（图 10、11）直观显示，DHIC‑Regu 在所有码率下均显著优于单尺度模型（ELIC、MLIC++）和未正则化的 DHIC‑Base，且在多分辨率场景（Table 7）中，除极低分辨率外，始终保持 BD‑Rate 领先，同时解码时间远小于大模型 HPCM‑Large，兼具高性能与轻量推理的优点。

### 补充图表

![[assets/figures/papers/iclr26_0014_lO6I66lweK_Taming_Hierarchical_Image_Coding_Optimization_A/figures/019_Table_3.jpg]]
*Table 3: Ablation studies of intra-scale and inter-scale regularization implementations (Baseline: the naive trained model, best implementation approaches are marked in blue color). (a) Intra-scale regularization (First 100 epochs)*

![[assets/figures/papers/iclr26_0014_lO6I66lweK_Taming_Hierarchical_Image_Coding_Optimization_A/figures/020_Table_4.jpg]]
*Table 4: (b) Inter-scale regularization (Remaining epochs). More ablation studies on regularization setups and modules design, are detailed in Appendix A.4*


## 方法谱系与知识库定位

DHIC‑Regu（Explicit Spectral Regularization for Hierarchical Coding）并非独立的新型架构，而是面向显式多尺度分层图像编码器的一套训练时正则化方案。其核心贡献在于，通过分析分层模型在朴素端到端优化中暴露的频谱散射与跨尺度混叠现象，设计了两类即插即用的正则化项：**尺度内频率正则化**（基于 DCT 的渐进频谱截断）与**尺度间潜在正则化**（基于 DWT+Conv 的相似性惩罚）。这些正则化项仅作用于训练阶段，不增加推理开销，却使同一网络架构（DHIC‑Base）在收敛速度和压缩性能上获得显著提升（Table 2）。因此，该工作在分层编码方法谱系中处于“训练范式改进”的位置，与单尺度模型、传统编码标准及其他分层架构形成清晰的阶梯关系。

### 与基线系统的关系与定位

**相较于单尺度学习编码器**：ELIC、MLIC++、HPCM‑Large 等模型聚焦于单尺度潜在变量，依赖高度优化的熵编码和上下文模型，在性能与复杂度间取得平衡。然而，这类模型的潜在空间不具备天然的多分辨率频率分解结构。实验表明，直接将本文的频谱正则化施加于单尺度模型会导致性能下降（详见 limitations），证实该正则化策略与显式多尺度架构深度耦合。因此，DHIC‑Regu 并非单尺度方法的上位替代，而是分层路线下的专用加速与性能提升手段。

**相较于传统编码标准 VTM‑22.0**：DHIC‑Regu 在所有测试数据集上均取得大幅度 BD‑Rate 节省，三数据集平均达到 −20.65%（Table 1），其中 Kodak 上较 VTM 节省 19.73%、CLIC Pro 节省 18.13%、Tecnick 节省 24.09%。这一结果使分层方案首次在亮度保持率失真性能上全面超越单尺度领先模型，同时将解码时间控制在 68.48 ms、KMACs/pixel 977.73（与基线 DHIC‑Base 完全一致）。因此，在标准参考锚点下，该方法将分层编码推向实际可用性，缩小了与传统标准间的复杂度代差。

**相较于分层编码基线 DHIC‑Base**：直接比较揭示了正则化的催化效应：联合使用尺度内与尺度间正则化后，训练收敛加速 2.30 倍，且 BD‑Rate 进一步改善 −10.11%（Table 2）。单一正则化的消融实验（Table 2、Table 3）表明，尺度内正则化主要负责训练早期收敛稳定（1.84× 加速，BD‑Rate −1.07%），而尺度间正则化是主要性能增益来源（−7.66% BD‑Rate），且二者协同产生超线性增益。这表明，分层网络容量的释放需要同时强制跨尺度频谱分工与抑制混叠。

**对其他分层架构的泛化能力**：为验证正则化方案的通用性，作者将其应用于代表性分层编解码器 QARV，并观察到一致的性能提升（详见原文 Appendix），说明所提出的频率正则化思路并不受限于特定主干网络，可作为分层编码训练的通用插件。这使该工作在分层学习型图像编码知识库中占据“训练优化方法论”的结点。

### 适用边界与限制

尽管 DHIC‑Regu 在分层架构上表现优异，其有效半径受限于若干架构与任务前提，具体包括：

1. **架构依赖性**：正则化针对显式多尺度层次结构设计。当试图迁移至单尺度 VAE（如 HPCM、MLIC++）时，频谱截断与跨尺度对齐机制因缺乏对应的频率分解支路而失去作用，甚至导致优化偏差（Table 10）。因此，该方法不适用于主流的单尺度图像压缩网络。
2. **任务范畴**：目前所有实验均基于静态图像编解码，尚未覆盖视频、3D 点云等具有更强时空或几何结构的多维数据。论文未提供动态数据下的训练动态分析或正则化适配方案。
3. **训练阶段专用**：两类正则化仅在训练时注入（尺度内正则化作用于前 100 epoch，尺度间正则化用于后续 epoch），测试阶段完全移除，因此推理时的编码/解码复杂度、参数量与显存占用无异于原架构（详见 fairness notes）。然而，这也意味着网络结构本身未获得任何推理期收益，依赖训练阶段额外计算（DCT/IDCT、DWT、1×1 Conv）来引导参数收敛。
4. **超参与调度**：正则化强度 $\delta$ 通过网格搜索固定为 0.1（Table 6），尺度内截断半径 $\tau(t)$ 的线性调度（由 0.05 线性增至 1.0）虽经对比确认为最优（Table 3a），但未尝试自适应调度策略（如依据梯度幅值或损失下降速度动态调整）。同样，阶段切换时间点（100 epoch）未做充分鲁棒性分析，可能带来跨数据集和网络规模的调参成本。

### 不足与局限

综合上述讨论及原文献自我批评，DHIC‑Regu 存在以下明确局限：

- 尺度内正则化对最终率失真性能的提升有限（BD‑Rate 约 −1%），其价值主要体现于加速收敛，而非进一步压缩增益。
- 所有实验均在可控的固定分辨率图像集合上进行，未测试极端分辨率、内容多样性或域迁移场景下的正则化鲁棒性。
- 尺度间对齐模块虽经消融确认 Haar 小波与 1×1 卷积组合最优，但缺乏对可学习变换（如自适应频率分解）的探索，可能限制表达能力。
- 尚未建立跨尺度的信息论解释，当前设计的合理性主要依赖于经验频谱分析和条件高斯假设（Eq. 7‑8），缺乏更深入的率失真理论边界推导。

（注：上述局限的逐项证据锚点请参见原文献 Table 2, Table 3, Table 6 及 Section 3.3 的设计消融。）

### 开放问题

基于该工作现有的分析与边界，若干重要问题有待后续研究：

1. **面向单尺度架构的频谱正则化**：能否为单尺度 VAE 中的通道组或空间切片设计频率感知的目标函数，使其在无显式尺度拆分的情况下仍受益于频谱偏置引导？这将决定频谱正则化能否成为跨架构的通用训练原则。
2. **自适应正则化调度**：是否可以基于梯度的频谱重叠度或损失收敛速率，自动调整 $\tau(t)$ 与 $\delta$，使训练过程无需手动划分阶段，并可能进一步压缩收敛周期？
3. **跨任务泛化**：该正则化思想是否可移植到其他存在潜在变量层次结构的任务（如分层视频编码、多尺度生成模型、神经辐射场），并保维持训练加速与性能提升？
4. **轻量可学习对齐**：尺度间 DWT+Conv 模块可否被计算成本更低的可学习变换替代（如分组卷积、频域线性投影），在不牺牲增益的前提下进一步降低训练开销？
5. **理论深化**：如何将启发式的频谱重叠量度量（Figure 1 中的能量分析）与率失真函数的泛化界相连，从而为分层编码提供紧密的理论指导？

上述问题若得到解决，有望将频谱正则化从一个有效的经验技巧发展为学习型分层编码的基础理论组件。

## 原文 PDF

![[paperPDFs/ICLR_2026/Taming_Hierarchical_Image_Coding_Optimization_A_Spectral_Regularization_Perspective.pdf]]
