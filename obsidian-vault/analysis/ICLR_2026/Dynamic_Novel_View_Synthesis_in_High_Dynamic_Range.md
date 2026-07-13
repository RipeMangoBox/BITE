---
title: Dynamic Novel View Synthesis in High Dynamic Range
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/Dynamic_Novel_View_Synthesis_in_High_Dynamic_Range_c7124ba0dcb7.pdf
project_link: "https://www.hdrsoft.com/"
code_link: "https://github.com/prinasi/HDR-4DGS"
aliases:
- H4
- DNVSHDR
tags:
- ICLR_2026
- topic/other_unclear
- topic/other_unclear/general
core_operator: 动态色调映射模块（DTM），通过构建辐射度库和动态辐射度上下文学习器（DRCL），在时间维度上自适应性调整逐通道色调映射函数，显式桥接LDR与HDR域。
primary_logic: 受人类视觉适应机制启发，利用过去时间戳的辐射度统计构建时间上下文，动态生成逐通道色调映射曲线，使模型能够根据场景辐射度的时变分布保持辐射度一致性与色彩保真度，从而统一4D动态几何与HDR重建。
claims:
- 在HDR-4D-Syn数据集上，HDR-4DGS（LDR+HDR监督）的HDR指标达到30.40 PSNR / 0.914 SSIM / 0.097 LPIPS，显著优于所有基线方法。
- 在HDR-4D-Real数据集上，HDR-4DGS（LDR+HDR监督）的LDR指标达到30.69 PSNR / 0.927 SSIM / 0.097 LPIPS，大幅领先HDR-HexPlane（28.12 / 0.767 / 0.307）。
- 动态色调映射器（DTM）相比静态色调映射器（MLP/Reinhard/Durand）在HDR重建上PSNR提升显著（25.88 vs 24.53/24.54/25.07）。
- 动态辐射度上下文学习器（DRCL）采用GRU实现最优（PSNR 25.88 / SSIM 0.865 / LPIPS 0.076），优于Transformer、LSTM和RNN。
---

# Dynamic Novel View Synthesis in High Dynamic Range

> [!tip] 核心洞察
> 受人类视觉适应机制启发，利用过去时间戳的辐射度统计构建时间上下文，动态生成逐通道色调映射曲线，使模型能够根据场景辐射度的时变分布保持辐射度一致性与色彩保真度，从而统一4D动态几何与HDR重建。

| 字段 | 内容 |
|------|------|
| 中文题名 | 高动态范围下的动态新视角合成 |
| 英文题名 | Dynamic Novel View Synthesis in High Dynamic Range |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=10iBNwPtl2) · [Code](https://github.com/prinasi/HDR-4DGS) · [Project](https://www.hdrsoft.com/) |
| Topic | #topic/other_unclear #topic/other_unclear/general |
| Method | HDR-4DGS |
| Dataset | HDR-4D-Syn, HDR-4D-Real |

> [!tip] 效果简介
> - HDR-4D-Syn 上，HDR PSNR↑ 30.40 vs 29.30 (HDR-HexPlane†) (+1.10)；HDR SSIM↑ 0.914 vs 0.844 (HDR-HexPlane†) (+0.070)；HDR LPIPS↓ 0.097 vs 0.223 (HDR-HexPlane†) (-0.126)。
> - HDR-4D-Real 上，LDR PSNR↑ 30.69 vs 28.12 (HDR-HexPlane†) (+2.57)；LDR SSIM↑ 0.927 vs 0.767 (HDR-HexPlane†) (+0.160)；LDR LPIPS↓ 0.097 vs 0.307 (HDR-HexPlane†) (-0.210)。

## 概要

### 问题瓶颈

高动态范围（HDR）新视角合成在静态场景中已取得显著进展，但真实世界场景往往包含动态物体和时变照明，导致几何结构与辐射度同时发生变化。现有方法——无论是面向静态HDR的**HDR-NeRF**（Huang et al., CVPR 2022）和**HDR-GS**（Cai et al., CVPR 2024），还是面向动态LDR的**HexPlane**（Cao & Johnson, 2023）和**4DGS**（Yang et al., ICLR 2024）——均无法同时处理动态几何与时变辐射度的联合建模。**HDR-HexPlane**（Wu et al., 3DV 2024）虽尝试将HDR重建扩展到动态场景，但在辐射度一致性和色彩保真度方面仍存在明显不足。这一瓶颈的根源在于：缺乏一种能够在时间维度上自适应桥接LDR与HDR域的色调映射机制。

### 核心方法

本文提出**HDR-4DGS**，一个基于高斯溅射的统一框架，通过引入**动态色调映射模块（DTM）** 显式连接HDR与LDR域。其核心创新在于：

- **动态色调映射器（DTM）**：受人类视觉适应机制启发，构建辐射度库（Radiance Library）和动态辐射度上下文学习器（DRCL），利用过去时间戳的辐射度统计生成时间自适应的逐通道色调映射曲线，从而在动态场景中保持辐射度一致性与色彩保真度。
- **HDR颜色空间扩展**：将4D高斯溅射的颜色表示从LDR扩展至HDR空间，通过4D球谐函数（4DSH）捕获更宽的亮度范围。
- **双重监督策略**：结合LDR与HDR损失，辅以像素级色调映射约束，提升色调映射的泛化能力。

### 方法谱系与知识库定位

HDR-4DGS处于动态场景新视角合成与高动态范围重建的交叉点。在动态表示层面，它继承并扩展了**4DGS**（Yang et al., ICLR 2024）的时空高斯溅射框架；在HDR重建层面，它区别于**HDR-GS**（Cai et al., CVPR 2024）的静态MLP色调映射，提出了时间自适应的动态色调映射机制。与两阶段流水线（先重建LDR动态场景，再独立进行HDR色调映射）相比，HDR-4DGS的联合优化策略在辐射度一致性和重建精度上均有显著优势。

### 主要结果

在合成数据集**HDR-4D-Syn**上，HDR-4DGS在LDR+HDR双重监督下达到**30.40 PSNR / 0.914 SSIM / 0.097 LPIPS**的HDR重建指标，较最优基线HDR-HexPlane（29.30 / 0.844 / 0.223）分别提升+1.10 dB、+0.070和-0.126。在真实场景数据集**HDR-4D-Real**上，LDR指标达到**30.69 PSNR / 0.927 SSIM / 0.097 LPIPS**，大幅领先HDR-HexPlane（28.12 / 0.767 / 0.307），提升幅度达+2.57 dB、+0.160和-0.210。

消融实验进一步证实：动态色调映射器相比静态色调映射器（MLP/Reinhard/Durand）在HDR PSNR上提升约1.35 dB；DRCL采用GRU实现时性能最优（25.88 PSNR / 0.865 SSIM / 0.076 LPIPS），优于Transformer、LSTM和RNN；时间上下文窗口长度k=20取得最佳平衡。

### 局限与展望

HDR-4DGS仍存在三方面局限：（1）底层4DGS表示未针对HDR内容专门设计，极端光照变化下的建模能力受限；（2）DTM使用固定时间上下文窗口，无法自适应调整感受野；（3）在前后景外观相似的动态边界处可能出现颜色再现不佳或空间模糊。未来工作可围绕HDR 4D场景的定制化表示、自适应上下文窗口机制、以及显式语义/运动边界建模等方向展开。



高动态范围（HDR）新视角合成旨在从一组多曝光或单一曝光的低动态范围（LDR）图像中，重建任意视角下具有完整亮度范围的高保真HDR视图。该技术对于计算摄影、虚拟现实和电影后期制作等应用至关重要，因为这些场景中同时存在极亮和极暗区域，LDR成像无法同时保留高光和阴影细节。

近年来，神经辐射场（NeRF）及其变体在静态HDR新视角合成上取得了显著进展。**HDR-NeRF**（Huang et al., CVPR 2022）首次将物理成像模型引入NeRF框架，通过显式建模相机响应函数和非线性色调映射，从包围曝光LDR图像中恢复HDR辐射场。随后，基于3D高斯溅射（3DGS）的**HDR-GS**（Cai et al., CVPR 2024）将这一思路迁移到显式点云表示，利用静态多层感知机（MLP）实现HDR到LDR的色调映射，在渲染速度和视觉质量上实现了双重提升。

然而，上述方法的共同局限在于**仅针对静态场景设计**。真实世界中，动态物体运动、时变照明和相机参数变化等因素会导致场景几何与辐射度在时间维度上联合变化。这种时空耦合给HDR新视角合成带来了根本性挑战：

- **几何-辐射度耦合**：动态场景中，物体的位置、形状和表面材质属性随时间变化，使得静态HDR方法无法准确追踪和重建时变辐射场。
- **色调映射的时变性**：不同时间戳下场景的亮度分布差异显著，固定的色调映射函数无法自适应调整，导致LDR渲染中出现色彩偏移、高光裁剪或暗部噪声放大。
- **监督信号的不匹配**：现有动态新视角合成方法（如**HexPlane**（Cao & Johnson, 2023）和**4DGS**（Yang et al., ICLR 2024））仅在LDR颜色空间中建模，缺乏对HDR辐射度的显式约束，无法从多曝光数据中恢复完整的亮度信息。

**HDR-HexPlane**（Wu et al., 3DV 2024）作为首个尝试将HDR重建与动态场景表示相结合的工作，将HexPlane的时空分解与HDR色调映射模块拼接，但该方法仍采用静态色调映射策略，未考虑辐射度的时间上下文，导致在光照剧烈变化的场景中辐射度一致性差，色彩保真度不足。

本文的核心动机在于：**借鉴人类视觉系统的适应性机制**——人眼能够根据场景整体亮度分布动态调整感知灵敏度，从而在不同光照条件下保持对细节和色彩的稳定感知。受此启发，我们提出HDR-4DGS，通过构建**动态色调映射模块（DTM）**，利用过去时间戳的辐射度统计信息生成时间自适应的逐通道色调映射曲线，显式桥接HDR与LDR域，从而在统一的4D高斯溅射框架下实现动态几何与HDR辐射度的联合重建。



## 核心方法与创新机理

HDR-4DGS 的核心创新在于将**动态色调映射**显式嵌入 4D 高斯溅射框架，从而在统一优化中同时解决动态几何重建与高动态范围（HDR）辐射度恢复两个耦合难题。与现有工作相比，其关键 changed slots 体现在三个层面。

### 1. 动态色调映射模块（DTM）：从静态映射到时间自适应映射

现有 HDR 新视角合成方法（如 **HDR-GS**, Cai et al., CVPR 2024）采用静态 MLP 实现色调映射，无法响应场景辐射度的时间变化。HDR-4DGS 提出的 DTM 模块（Figure 1(b)）通过两个子组件实现时间自适应映射：

- **辐射度库（Radiance Library）**：在每个时间戳 $t$ 对所有高斯点的 HDR 颜色取平均，形成辐射度签名 $\mathbf{r}_t^h$（公式 3），构建场景辐射度的时序统计量。
- **动态辐射度上下文学习器（DRCL）**：处理过去 $k$ 帧的辐射度签名序列 $\mathbf{r}_{t-k:t}^h$，生成上下文嵌入 $\mathbf{f}_t$（公式 4），使色调映射函数能够感知辐射度的时变分布。

最终，逐通道色调映射函数 $g_\theta$ 将拼接后的对数 HDR 颜色、对数曝光时间与上下文嵌入映射为 LDR 颜色（公式 5）：

$$\mathbf{c}_t^l = g_\theta([\log \mathbf{c}_t^h + \log e_t, \mathbf{f}_t])$$

这一设计的因果机制在于：**利用过去时间戳的辐射度统计构建时间上下文，动态生成逐通道色调映射曲线**，使模型能够根据场景辐射度的时变分布保持辐射度一致性与色彩保真度。消融实验（Table 4）证实，DTM 相比静态色调映射器（MLP/Reinhard/Durand）在 HDR 重建上 PSNR 提升约 1.35 dB（25.88 vs 24.53/24.54/25.07）。DRCL 采用 GRU 实现时性能最优（PSNR 25.88 / SSIM 0.865 / LPIPS 0.076），优于 Transformer、LSTM 和 RNN（Table 9）。

### 2. 颜色空间扩展：从 LDR 到 HDR 的 4D 球谐函数

**4DGS**（Yang et al., ICLR 2024）原生工作在 LDR 颜色空间，限制了其对高亮度范围的表达能力。HDR-4DGS 将 4DGS 的颜色表示空间从 LDR 扩展至 HDR，通过 4D 球谐函数（4DSH）捕获更宽的亮度范围。这一改动使高斯溅射的渲染方程（公式 1）能够直接输出 HDR 颜色 $\mathbf{c}_t^h$，为后续 DTM 的色调映射提供完整的辐射度信息。

### 3. 双重监督策略：LDR 与 HDR 联合约束

现有方法（如 4DGS 和 HDR-GS）通常仅采用 LDR 监督，导致色调映射的泛化能力受限。HDR-4DGS 引入 LDR 与 HDR 双重监督（公式 6）：

$$\mathcal{L}_{\mathrm{total}} = \mathcal{L}_{\mathrm{ldr}} + \alpha \mathcal{L}_{\mathrm{hdr}}$$

其中 LDR 损失包含 2D 色调映射图像和 3D 直接渲染图像与真实 LDR 的比较，HDR 损失为 μ-law 压缩后的渲染与真实 HDR 的比较（公式 8）。消融实验（Table 5）表明，像素级色调映射监督将 HDR PSNR 从 24.85 提升至 25.88。

### 瓶颈突破与证据强度

HDR-4DGS 解决的**真实瓶颈**是：现有 HDR 新视角合成方法（如 **HDR-NeRF**, Huang et al., CVPR 2022; **HDR-GS**, Cai et al., CVPR 2024）仅针对静态场景，无法处理动态物体和时变照明带来的几何与辐射度联合变化。**HDR-HexPlane**（Wu et al., 3DV 2024）虽尝试扩展至动态场景，但其色调映射机制缺乏时间建模，导致辐射度一致性差。

在 HDR-4D-Syn 数据集上，HDR-4DGS（LDR+HDR 监督）的 HDR 指标达到 **30.40 PSNR / 0.914 SSIM / 0.097 LPIPS**，显著优于 HDR-HexPlane（29.30 / 0.844 / 0.223）（Table 1）。在 HDR-4D-Real 数据集上，LDR 指标达到 **30.69 PSNR / 0.927 SSIM / 0.097 LPIPS**，大幅领先 HDR-HexPlane（28.12 / 0.767 / 0.307）（Table 2）。同时，HDR-4DGS 的推理速度在合成数据集上比 HDR-HexPlane 快 **36 倍**，在真实数据集上快 **200 倍**。

**注意**：HDR-4D-Real 数据集上的 HDR 评价受真实 HDR 标签噪声影响，且 PSNR 倾向于过度平滑的图像（Figure 9），因此 HDR-HexPlane 的 HDR PSNR 较高并不反映真实感知质量；定性对比（Figure 3）显示 HDR-4DGS 保留更多细节和准确色彩。



HDR-4DGS的整体pipeline围绕一个核心矛盾展开：如何在动态场景中同时保持几何-辐射度的时空一致性与高动态范围重建精度。如图1所示，框架由三个协同模块构成流水线：

1. **动态场景表示（4DGS with HDR colors）**：以4D高斯溅射（**4DGS**, Yang et al., ICLR 2024）为基础表示，将其颜色空间从LDR扩展至HDR域，统一建模时空几何与辐射度。该模块接收多曝光LDR图像序列及对应曝光时间，输出任意时间戳与视角下的HDR辐射场。

2. **动态色调映射器（Dynamic Tone Mapper, DTM）**：这是框架的因果调节旋钮。DTM通过辐射度库（Radiance Library）存储历史帧的辐射度统计，并由动态辐射度上下文学习器（Dynamic Radiance Context Learner, DRCL）处理过去k帧的辐射度签名序列，生成时间上下文嵌入$\mathbf{f}_t$。该嵌入与对数HDR颜色、对数曝光时间拼接后，经函数$g_\theta$逐通道生成自适应色调映射曲线，实现$\mathbf{c}_t^l = g_\theta([\log \mathbf{c}_t^h + \log e_t, \mathbf{f}_t])$的HDR→LDR转换。这一设计受人类视觉适应机制启发，显式桥接LDR与HDR域。

3. **联合优化与渲染**：总损失$\mathcal{L}_{\mathrm{total}} = \mathcal{L}_{\mathrm{ldr}} + \alpha \mathcal{L}_{\mathrm{hdr}}$结合LDR重建损失（含2D色调映射图像与3D直接渲染图像的双路径监督）和μ-law压缩后的HDR重建损失，同时优化高斯参数与色调映射网络。最终渲染输出HDR视图，LDR视图则取高斯溅射直接光栅化的结果。

**输入输出流**：输入为多曝光LDR图像序列$\{\mathbf{I}_t^l, e_t\}$与对应相机位姿；输出为任意新时间戳$t'$和新视角$V'$下的HDR图像$\mathbf{I}_{t',V'}^h$及对应LDR图像$\mathbf{I}_{t',V'}^l$。DTM作为中间桥梁，将4DGS渲染的HDR颜色转换为LDR颜色以与监督信号对齐，同时通过像素级色调映射约束提升泛化能力。

> **证据强度说明**：DTM的因果作用由消融实验强力支持——动态色调映射器相比静态色调映射器（MLP/Reinhard/Durand）在HDR重建上PSNR提升约1.35 dB（Table 4）；像素级监督将HDR PSNR从24.85提升至25.88（Table 5）；DRCL采用GRU实现最优性能25.88 PSNR / 0.865 SSIM / 0.076 LPIPS（Table 9）。这些消融构成因果链条的验证闭环，置信度均≥0.95。

### 补充图表

![[assets/figures/papers/paper_list_l26_https_openreview_net_forum_id_10iBNwPtl2/figures/001_Figure_1.jpg]]
*Figure 1: Overview of HDR-4DGS. (a) Input data and scene representation; (b) Our proposed Dynamic Tone Mapper (DTM) for temporally adaptive HDR–LDR translation; (c) Loss formulation for joint optimization of geometry, radiance, and tone mapping. ⊗ : Dot product. ©: Concatenation*



### 3.1 总体框架

HDR-4DGS 由两个核心组件构成：一个通用的动态场景表示模型，以及一个新颖的动态色调映射机制。给定时间戳 $t'$ 和相机视点 $V'$，HDR 动态新视角合成（HDR DNVS）的目标是重建对应的 HDR 图像：

$$\mathcal{F}_h : (t', V') \to \mathbf{I}_{t', V'}^h$$

整体架构如 Figure 1 所示，包含三个递进阶段：(a) 基于 4D 高斯溅射的 HDR 场景表示；(b) 动态色调映射器（DTM）实现时间自适应的 HDR–LDR 转换；(c) 联合优化损失函数。

### 3.2 HDR 颜色空间中的 4D 高斯溅射

HDR-4DGS 采用 **4D Gaussian Splatting (4DGS)**（Yang et al., ICLR 2024）作为基础动态场景表示框架，并将其颜色表示空间从 LDR 扩展至 HDR。给定 $N$ 个三维高斯点，像素观测 $\mathbf{I}(u, v, t)$ 的渲染方程为：

$$\mathbf{I}(u, v, t) = \sum_{i=1}^{N} p_i(t) \, p_i(u, v \mid t) \, \alpha_i \, c_i \prod_{j=1}^{i-1} \bigl(1 - p_j(t) \, p_j(u, v \mid t) \, \alpha_j \bigr)$$

其中：
- $p_i(t)$：第 $i$ 个高斯点在时间 $t$ 的时间概率；
- $p_i(u, v \mid t)$：给定时间 $t$ 时，高斯点在空间坐标 $(u, v)$ 的条件概率；
- $\alpha_i$：第 $i$ 个高斯点的不透明度；
- $c_i$：第 $i$ 个高斯点的颜色值（在 HDR-4DGS 中扩展为 HDR 颜色）；
- 乘积项 $\prod_{j=1}^{i-1}$：前序高斯点的透射率累积。

通过将颜色空间扩展至 HDR 域，并结合 4D 球谐函数（4DSH）以捕获更宽的亮度范围，该表示统一建模了时空几何与辐射度。

### 3.3 动态色调映射器（DTM）

动态色调映射器是 HDR-4DGS 的核心创新模块，其设计灵感来源于人类视觉系统的自适应机制。DTM 的目标是将 HDR 颜色 $\mathbf{c}_t^h$ 在给定曝光时间 $e_t$ 和时间戳 $t$ 的条件下，转换为 LDR 颜色 $\mathbf{c}_t^l$：

$$\mathbf{c}_t^l = \mathrm{DTM}(\mathbf{c}_t^h, e_t, t)$$

DTM 由两个子模块构成：

#### 3.3.1 辐射度库与辐射度签名

在时间 $t$，对所有 $N$ 个高斯点的 HDR 颜色取平均，得到**辐射度签名** $\mathbf{r}_t^h$：

$$\mathbf{r}_t^h = \frac{1}{N} \sum_{i=1}^{N} \mathbf{c}_{i,t}^h$$

辐射度签名作为场景全局辐射度状态的紧凑摘要，被存入辐射度库中以构建时间上下文。

#### 3.3.2 动态辐射度上下文学习器（DRCL）

DRCL 处理过去 $k$ 帧的辐射度签名序列 $\mathbf{r}_{t-k:t}^h$，生成辐射度上下文嵌入 $\mathbf{f}_t$：

$$\mathbf{f}_t = \mathrm{DRCL}(\mathbf{r}_{t-k:t}^h)$$

实验表明，DRCL 采用 **GRU** 实现时性能最优（HDR PSNR 25.88 / SSIM 0.865 / LPIPS 0.076），优于 Transformer、LSTM 和 RNN 等替代方案（Table 9）。时间上下文窗口长度 $k=20$ 在 HDR 重建中取得最佳效果（Table 6）。

#### 3.3.3 自适应色调映射函数

最终的逐通道色调映射通过拼接对数 HDR 颜色、对数曝光时间和辐射度上下文嵌入，由函数 $g_\theta$ 完成：

$$\mathbf{c}_t^l = g_\theta\bigl([\log \mathbf{c}_t^h + \log e_t, \mathbf{f}_t]\bigr)$$

通过引入 $\mathbf{f}_t$，DTM 实现了辐射度上下文感知的 HDR 到 LDR 转换，在动态场景中显著提升了跨时间的辐射度一致性。

### 3.4 联合优化与损失函数

HDR-4DGS 采用 LDR 与 HDR 双重监督策略。总损失函数为两者的加权和：

$$\mathcal{L}_{\mathrm{total}} = \mathcal{L}_{\mathrm{ldr}} + \alpha \mathcal{L}_{\mathrm{hdr}}$$

其中 $\alpha$ 控制 HDR 损失的贡献权重。LDR 损失包含两部分——2D 色调映射图像和 3D 直接渲染图像分别与真实 LDR 的比较；HDR 损失则对 μ-law 压缩后的渲染与真实 HDR 进行比较：

$$\mathcal{L}_{\mathrm{ldr}} = \mathcal{L}(\mathbf{I}_{t,2D}^l, \mathbf{I}_t^l) + \mathcal{L}(\mathbf{I}_{t,3D}^l, \mathbf{I}_t^l), \quad \mathcal{L}_{\mathrm{hdr}} = \mathcal{L}(\hat{\mathbf{I}}_{t,2D}^h, \hat{\mathbf{I}}_t^h)$$

其中 μ-law 压缩用于将 HDR 图像映射到与 LDR 域对齐的压缩空间：

$$\hat{\mathbf{I}}^h = \frac{\log(1 + \mu \cdot \operatorname{norm}(\mathbf{I}^h))}{\log(1 + \mu)}$$

消融实验证实，像素级色调映射监督将 HDR PSNR 从 24.85 提升至 25.88（Table 5），验证了双重监督策略对色调映射泛化能力的增强效果。

### 补充图表

![[assets/figures/papers/paper_list_l26_https_openreview_net_forum_id_10iBNwPtl2/figures/006_Figure_4.jpg]]
*Figure 4: Temporal variation with learned tone mapping patterns by DTM in two scenes*



## 实验与关键发现

### 核心定量结果

HDR-4DGS在两个新构建的基准数据集上进行了全面评估：合成数据集HDR-4D-Syn和真实数据集HDR-4D-Real。评估同时覆盖LDR和HDR动态新视角合成（DNVS）两个子任务，并与LDR动态方法（**HexPlane** (Cao & Johnson, 2023)、**4DGS** (Yang et al., ICLR 2024)）、HDR静态方法（**HDR-NeRF** (Huang et al., CVPR 2022)、**HDR-GS** (Cai et al., CVPR 2024)）以及HDR动态方法（**HDR-HexPlane** (Wu et al., 3DV 2024)）进行全面对比。

**合成数据集HDR-4D-Syn（Table 1）**：在LDR+HDR联合监督（†）设置下，HDR-4DGS在HDR DNVS任务上达到**30.40 PSNR / 0.914 SSIM / 0.097 LPIPS**，相比最强基线HDR-HexPlane†（29.30 / 0.844 / 0.223）分别提升+1.10 dB / +0.070 / -0.126。在LDR DNVS任务上，HDR-4DGS†达到33.16 PSNR / 0.955 SSIM / 0.044 LPIPS，同样全面领先。值得注意的是，即使在仅LDR监督（∗）的设置下，HDR-4DGS∗仍以25.88 PSNR / 0.865 SSIM / 0.076 LPIPS在HDR任务上超越HDR-HexPlane∗（25.25 / 0.762 / 0.135），验证了动态色调映射器（DTM）在无HDR真值条件下仍能有效学习HDR-LDR域的映射关系。

**真实数据集HDR-4D-Real（Table 2）**：HDR-4DGS†在LDR DNVS上取得**30.69 PSNR / 0.927 SSIM / 0.097 LPIPS**，大幅领先HDR-HexPlane†（28.12 / 0.767 / 0.307），ΔPSNR达+2.57 dB。HDR DNVS任务上HDR-4DGS†达到25.13 PSNR / 0.909 SSIM / 0.162 LPIPS。需要特别指出的是，真实场景的HDR评价存在**指标噪声**：如Figure 9所示，PSNR倾向于偏好过度平滑或模糊的图像，HDR-HexPlane在HDR-4D-Real上的HDR PSNR数值较高并不反映真实感知质量；定性对比（Figure 3）显示HDR-4DGS保留了更丰富的细节和准确的色彩还原。

**推理效率**：HDR-4DGS基于高斯溅射的渲染管线带来显著的推理速度优势——在HDR-4D-Syn上比HDR-HexPlane快**36倍**，在HDR-4D-Real上快**200倍**，验证了该方法在实际部署中的可行性。

### 消融实验

消融实验系统性地验证了HDR-4DGS各设计选择的贡献，所有实验均在HDR-4D-Syn数据集上以LDR-only监督设置进行。

**动态色调映射 vs. 静态色调映射（Table 4）**：将DTM替换为静态色调映射器（MLP学习色调映射、Reinhard全局算子、Durand局部算子）后，HDR重建PSNR从25.88分别降至24.53 / 24.54 / 25.07，验证了时间自适应色调映射对动态场景HDR重建的关键作用。Figure 4进一步可视化了DTM学习到的色调映射曲线随时间的演变，展示了模型对场景辐射度时变分布的自适应能力。

**像素级色调映射监督（Table 5）**：移除像素级色调映射约束后，HDR PSNR从25.88降至24.85，表明该监督信号有效提升了色调映射网络的泛化能力，使其在未见视角和时间戳上保持稳定的HDR-LDR转换。

**时间上下文窗口长度（Table 6）**：系统扫描k∈{1, 5, 10, 20, 30, 50}，k=20在HDR重建中取得最优性能。过小的窗口（k=1）缺乏足够的辐射度历史信息，过大的窗口（k=50）可能引入无关的时间上下文噪声，二者均导致性能下降。

**动态辐射度上下文学习器设计（Table 9）**：在DRCL中对比GRU、Transformer、LSTM和RNN四种序列建模架构，GRU以25.88 PSNR / 0.865 SSIM / 0.076 LPIPS取得最优，优于Transformer（25.42 / 0.855 / 0.081）和LSTM（25.65 / 0.861 / 0.078）。GRU在建模辐射度时间依赖性与计算效率之间取得了最佳平衡。

**两阶段流水线对比（Table 3）**：将4DGS与独立HDR重建（先做LDR 4DGS，再独立训练HDR-NeRF）的两阶段方案进行对比，HDR-4DGS的联合优化在HDR指标上显著优于分离式流水线，验证了统一4D几何与辐射度联合建模的必要性。

### 辐射度时间一致性分析

Figure 5定量展示了不同方法在HDR渲染中的时间辐射度变化。HDR-4DGS的辐射度曲线在时间轴上变化平滑且与真值高度吻合，而HDR-HexPlane和4DGS+HDR-GS组合则表现出明显的辐射度跳变和不一致。Figure 6通过Photomatix Pro色调映射后的连续辐射度变化可视化进一步印证了这一优势——HDR-4DGS在光照渐变场景中保持了连贯的辐射度过渡，而基线方法出现明显的色彩偏移和闪烁。

### 失败模式与局限性

尽管HDR-4DGS在整体指标上表现优异，分析揭示了以下已知失败模式：

1. **极端光照变化下的建模能力受限**：HDR-4DGS建立在4DGS表示之上，该表示最初为LDR动态场景设计，未针对HDR内容的宽亮度范围进行专门优化。在极端光照突变场景中，4D球谐函数（4DSH）扩展的颜色空间可能不足以精确捕获高动态范围的细节。

2. **固定时间上下文窗口的局限**：DTM使用固定长度k=20的时间上下文窗口，无法根据运动幅度或辐射度变化速率自适应调整感受野。在快速运动或光照剧变的片段，固定窗口可能无法及时响应；在静态片段，则可能引入冗余计算。

3. **动态边界处的辐射度歧义**：在前后景外观相似的场景（如HDR-4D-Syn中的Jump场景），动态物体边界处可能出现颜色再现不佳或空间模糊，原因是4DGS的运动变形场和辐射度场在语义边界处缺乏显式解耦机制。

### 开放问题

基于上述局限性，以下方向值得进一步探索：

- **HDR原生4D表示**：设计专为HDR 4D场景定制的表示方法，融入物理先验（如相机响应函数、辐照度分解）或自适应辐射度基，以更好地捕捉极端照度变化并增强长时辐射度一致性。
- **自适应上下文窗口**：构建基于运动幅度或辐射度方差的动态色调映射上下文窗口自适应调节机制，使DTM能够根据场景动态程度灵活调整时间感受野。
- **边界感知的辐射度建模**：显式建模语义或运动边界来消除动态内容的歧义，提升边界处的辐射度一致性和空间清晰度。

### 补充图表

![[assets/figures/papers/paper_list_l26_https_openreview_net_forum_id_10iBNwPtl2/figures/002_Table_1.jpg]]
*Table 1: Results on HDR-4D-Syn. ∗: HDR only supervision; †: LDR+HDR supervision*

![[assets/figures/papers/paper_list_l26_https_openreview_net_forum_id_10iBNwPtl2/figures/004_Table_2.jpg]]
*Table 2: Results on HDR-4D-Real. ∗: HDR only supervision; †: LDR+HDR supervision*

![[assets/figures/papers/paper_list_l26_https_openreview_net_forum_id_10iBNwPtl2/figures/010_Table_4.jpg]]
*Table 4: Ablation on dynamic tone mapping*

![[assets/figures/papers/paper_list_l26_https_openreview_net_forum_id_10iBNwPtl2/figures/018_Table_9.jpg]]
*Table 9: Analysis of DRCL design*

![[assets/figures/papers/paper_list_l26_https_openreview_net_forum_id_10iBNwPtl2/figures/007_Figure_5.jpg]]
*Figure 5: Comparison of HDR renderings’ temporal radiance variations*

![[assets/figures/papers/paper_list_l26_https_openreview_net_forum_id_10iBNwPtl2/figures/005_Figure_3.jpg]]
*Figure 3: Visual comparison of HDR DNVS on HDR-4D-Real*

![[assets/figures/papers/paper_list_l26_https_openreview_net_forum_id_10iBNwPtl2/figures/011_Table_5.jpg]]
*Table 5: Analysis of pixel-level supervision*

![[assets/figures/papers/paper_list_l26_https_openreview_net_forum_id_10iBNwPtl2/figures/012_Table_6.jpg]]
*Table 6: Analysis of the temporal context length*

![[assets/figures/papers/paper_list_l26_https_openreview_net_forum_id_10iBNwPtl2/figures/008_Table_3.jpg]]
*Table 3: Results of 4DGS with independent HDR*

![[assets/figures/papers/paper_list_l26_https_openreview_net_forum_id_10iBNwPtl2/figures/017_Figure_9.jpg]]
*Figure 9: PSNR prefers over-smooth or blurry images. HDR images are tone-mapped by Photomatix Pro (HDRsoft Team, 2025)*



## 定位与知识库关联

### 任务定位与问题瓶颈

HDR-4DGS 聚焦于**高动态范围下的动态新视角合成**（HDR DNVS），其现实瓶颈在于：现有 HDR 新视角合成方法——如 **HDR-NeRF**（Huang et al., CVPR 2022）和 **HDR-GS**（Cai et al., CVPR 2024）——仅针对静态场景设计，无法处理真实世界中动态物体、时变照明等带来的几何与辐射度联合变化。另一方面，LDR 动态新视角合成方法——如 **HexPlane**（Cao & Johnson, 2023）和 **4DGS**（Yang et al., ICLR 2024）——虽能建模动态几何，但工作在有限的 LDR 颜色空间，缺乏对高动态范围辐射度的表达能力。这两条技术路线的割裂导致动态场景下的 HDR 重建长期处于空白状态。

HDR-4DGS 的核心因果调控变量是**动态色调映射模块**（DTM），它通过构建辐射度库和动态辐射度上下文学习器（DRCL），在时间维度上自适应地调整逐通道色调映射函数，显式桥接 LDR 与 HDR 域。这一设计的深层洞察源于人类视觉适应机制：利用过去时间戳的辐射度统计构建时间上下文，动态生成逐通道色调映射曲线，使模型能够根据场景辐射度的时变分布保持辐射度一致性与色彩保真度，从而统一 4D 动态几何与 HDR 重建。

### 与基线方法的谱系关系

#### LDR 动态新视角合成基线

**HexPlane**（Cao & Johnson, 2023）和 **4DGS**（Yang et al., ICLR 2024）代表了 LDR 域动态场景建模的主流范式。HexPlane 通过六平面分解实现高效的时空表示，4DGS 则利用 4D 高斯溅射统一建模动态几何与外观。HDR-4DGS 直接继承了 4DGS 的渲染框架（见公式 $\mathbf{I}(u,v,t) = \sum_{i=1}^{N} p_i(t) p_i(u,v|t) \alpha_i c_i \prod_{j=1}^{i-1} (1 - p_j(t) p_j(u,v|t) \alpha_j)$），但将颜色空间从 LDR 扩展至 HDR，并通过 4D 球谐函数（4DSH）捕获更宽的亮度范围。这一扩展构成了 HDR 动态建模的几何基础，但仅靠颜色空间扩展无法解决 HDR-LDR 域的对齐问题。

#### HDR 静态新视角合成基线

**HDR-NeRF**（Huang et al., CVPR 2022）开创性地将 HDR 重建引入神经辐射场，通过物理启发的相机响应函数建模实现 LDR 输入到 HDR 输出的转换。**HDR-GS**（Cai et al., CVPR 2024）则将这一思路迁移到 3D 高斯溅射框架，采用静态 MLP 作为色调映射器。HDR-4DGS 与 HDR-GS 的核心差异在于**色调映射机制**：HDR-GS 使用与时间无关的静态 MLP 完成 HDR→LDR 转换，而 HDR-4DGS 的 DTM 模块引入了时间维度的辐射度上下文，使色调映射函数能够随场景辐射度的时变分布自适应调整。这一差异在消融实验中得到了量化验证：DTM 相比静态色调映射器（MLP/Reinhard/Durand）在 HDR PSNR 上提升约 1.35 dB（Table 4）。

#### HDR 动态新视角合成基线

**HDR-HexPlane**（Wu et al., 3DV 2024）是目前唯一直接对标 HDR 动态新视角合成的工作。它将 HexPlane 的六平面表示与 HDR 色调映射结合，是 HDR-4DGS 最直接的竞争方法。在 HDR-4D-Syn 数据集上，HDR-4DGS（LDR+HDR 监督）的 HDR 指标达到 30.40 PSNR / 0.914 SSIM / 0.097 LPIPS，显著优于 HDR-HexPlane 的 29.30 / 0.844 / 0.223（Table 1）。在 HDR-4D-Real 数据集上，HDR-4DGS 的 LDR 指标达到 30.69 PSNR / 0.927 SSIM / 0.097 LPIPS，大幅领先 HDR-HexPlane 的 28.12 / 0.767 / 0.307（Table 2）。此外，HDR-4DGS 在推理速度上具有压倒性优势：在 HDR-4D-Syn 上达到 36× 加速，在 HDR-4D-Real 上达到 200× 加速，这得益于高斯溅射渲染管线相比六平面采样的天然效率优势。

### 方法谱系中的结构创新

从方法谱系角度，HDR-4DGS 的核心创新并非提出全新的场景表示，而是在**4DGS 动态几何框架**与**HDR 色调映射机制**之间建立了时间自适应的桥接。具体而言，三个关键的结构性变化构成了其谱系定位：

1. **颜色空间扩展**：将 4DGS 的 LDR 颜色空间替换为 HDR 颜色空间，通过 4DSH 扩展亮度范围。这是从 LDR 动态建模到 HDR 动态建模的必要但非充分步骤。

2. **动态色调映射器（DTM）**：这是方法的核心差异化组件。DTM 包含辐射度库（存储历史帧的辐射度签名 $\mathbf{r}_t^h = \frac{1}{N}\sum_{i=1}^{N} \mathbf{c}_{i,t}^h$）和动态辐射度上下文学习器（DRCL，处理过去 $k$ 帧的辐射度签名序列生成上下文嵌入 $\mathbf{f}_t = \mathrm{DRCL}(\mathbf{r}_{t-k:t}^h)$），最终通过自适应色调映射函数 $\mathbf{c}_t^l = g_\theta([\log \mathbf{c}_t^h + \log e_t, \mathbf{f}_t])$ 完成逐通道 HDR→LDR 转换。消融实验表明，DRCL 采用 GRU 实现时性能最优（PSNR 25.88 / SSIM 0.865 / LPIPS 0.076），优于 Transformer、LSTM 和 RNN（Table 9）；时间上下文窗口长度 $k=20$ 时取得最优 HDR 重建性能（Table 6）。

3. **双重监督策略**：总损失 $\mathcal{L}_{\mathrm{total}} = \mathcal{L}_{\mathrm{ldr}} + \alpha \mathcal{L}_{\mathrm{hdr}}$ 结合 LDR 重建损失和 HDR 重建损失，其中 HDR 损失使用 μ-law 压缩 $\hat{\mathbf{I}}^h = \frac{\log(1 + \mu \cdot \mathrm{norm}(\mathbf{I}^h))}{\log(1 + \mu)}$ 对齐 HDR 与 LDR 域。像素级色调映射监督的消融实验显示，该策略将 HDR PSNR 从 24.85 提升至 25.88（Table 5），验证了其对色调映射泛化能力的增强作用。

### 适用边界与局限

HDR-4DGS 的能力边界受限于其基础表示的选择和 DTM 的设计假设：

- **表示层面的限制**：HDR-4DGS 建立在 4DGS 表示之上，该表示最初为 LDR 动态场景设计，未针对 HDR 内容的极端亮度变化进行专门优化。在光照剧烈变化的场景中，高斯点的颜色表示能力可能达到瓶颈。

- **时间上下文窗口的固定性**：DTM 使用固定的时间上下文窗口（$k=20$），无法根据运动幅度或辐射度变化速率自适应调整感受野。在快速运动或突变光照场景中，固定窗口可能无法捕获足够的上下文信息；而在缓慢变化场景中，则可能引入冗余计算。

- **动态边界的歧义性**：当前后景外观相似时（如 HDR-4D-Syn 中的 Jump 场景），动态边界处可能出现颜色再现不佳或空间模糊。这是因为方法缺乏显式的语义或运动边界建模来消除动态内容的歧义。

- **真实 HDR 标签的噪声问题**：在 HDR-4D-Real 数据集上，真实 HDR 标签存在噪声，且 PSNR 指标倾向于过度平滑的图像（如 Figure 9 所示）。因此 HDR-HexPlane 的 HDR PSNR 较高并不反映真实感知质量，定性对比（Figure 3）显示 HDR-4DGS 保留了更多细节和准确色彩。这一评价偏差需要在解读定量结果时予以注意。

### 开放问题

从方法谱系的发展趋势来看，以下方向值得后续工作探索：

1. **HDR 原生 4D 表示设计**：如何设计专为 HDR 4D 场景定制的表示方法，融入物理先验（如相机响应函数的显式参数化）或自适应辐射度基，以更好地捕捉极端照度变化并增强长时一致性？当前将 LDR 表示简单扩展至 HDR 空间的策略可能无法充分利用 HDR 信号的统计特性。

2. **自适应时间上下文窗口**：如何构建基于运动幅度或辐射度方差的动态色调映射上下文窗口自适应调节机制？固定窗口策略在多样化动态场景中的局限性提示了自适应机制的潜在收益。

3. **语义/运动边界的显式建模**：如何显式建模语义或运动边界来消除动态内容的歧义并提升边界处的辐射一致性？当前方法的边界模糊问题指向了将运动分割或光流估计融入辐射度建模的可能性。

4. **HDR 评价指标的改进**：真实 HDR 标签噪声和 PSNR 对平滑图像的偏好暴露了现有评价体系的不足。开发更鲁棒的 HDR 感知质量指标，对于推动该领域的公平比较和技术进步具有重要意义。



## 原文 PDF

![[paperPDFs/ICLR_2026/Dynamic_Novel_View_Synthesis_in_High_Dynamic_Range_c7124ba0dcb7.pdf]]
