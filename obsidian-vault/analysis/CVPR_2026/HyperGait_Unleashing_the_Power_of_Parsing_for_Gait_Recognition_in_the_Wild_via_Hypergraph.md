---
title: "HyperGait: Unleashing the Power of Parsing for Gait Recognition in the Wild via Hypergraph"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/HyperGait_Unleashing_the_Power_of_Parsing_for_Gait_Recognition_in_the_Wild_via_Hypergraph.pdf
project_link: null
code_link: null
aliases:
- HyperGait
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
core_operator: 引入空间超图卷积模块（SHCM）和时间超图卷积模块（THCM），通过自适应构建超图并使用超图卷积，显式建模身体部位间的高阶空间关系和帧之间的高阶时间依赖。
primary_logic: 超图通过超边连接任意数量的节点，天然适合捕获步态序列中多部件、多帧之间的多路高阶依赖关系，相较于传统图卷积仅能建模成对关系，超图能够更全面、有效地进行特征聚合和信息传播。
claims:
- Combining SHCM and THCM improves Rank-1 by 4.8% over the backbone baseline (Backbone+Global Head) on Gait3D.
- SHCM outperforms S-GCN by 0.5% and THCM outperforms T-GCN by 1.1% on Gait3D, demonstrating the advantage of hypergraph over GCN.
- HyperGait achieves state-of-the-art Rank-1 accuracy of 80.5% on Gait3D and 79.9% on SUSTech1K using only parsing input.
- Qualitative results show that HyperGait remains robust under occlusion and extreme viewpoints, while ParsingGait and XGait produce errors.
---

# HyperGait: Unleashing the Power of Parsing for Gait Recognition in the Wild via Hypergraph

> [!tip] 核心洞察
> 超图通过超边连接任意数量的节点，天然适合捕获步态序列中多部件、多帧之间的多路高阶依赖关系，相较于传统图卷积仅能建模成对关系，超图能够更全面、有效地进行特征聚合和信息传播。

| 字段 | 内容 |
|------|------|
| 中文题名 | HyperGait：通过超图释放解析用于野外步态识别的能力 |
| 英文题名 | HyperGait: Unleashing the Power of Parsing for Gait Recognition in the Wild via Hypergraph |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://openaccess.thecvf.com/content/CVPR2026/html/Zheng_HyperGait_Unleashing_the_Power_of_Parsing_for_Gait_Recognition_in_CVPR_2026_paper.html) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction |
| Method | HyperGait |
| Dataset | Gait3D, SUSTech1K |

> [!tip] 效果简介
> - Gait3D 上，Rank-1 accuracy 80.5% vs 75.7% (Backbone + Global Head) (+4.8%)。
> - SUSTech1K 上，Overall Rank-1 accuracy 79.9% (outperforms all previous single-representation methods)。

## 概要

步态识别在远距离、非配合场景下具有独特优势，但野外环境中的遮挡、视角变化和衣着差异使其仍极具挑战。近年来，基于人体解析序列的方法（如 **ParsingGait** (Zheng et al., ACM MM 2023) 和 **XGait** (Zheng et al., ACM MM 2024)）通过引入细粒度的身体部件信息，取得了显著进展。然而，现有方法无论是基于 CNN 还是 GCN，都仅能建模身体部位之间或时间帧之间的成对关系，忽略了复杂的高阶非线性相关性，导致解析序列中丰富的空间-时间信息未被充分利用。

针对这一瓶颈，本文提出 **HyperGait**——一个基于超图的步态识别框架。其核心洞见在于：超图通过超边可连接任意数量的节点，天然适合捕获步态序列中多部件、多帧之间的多路高阶依赖关系。具体而言，HyperGait 在全局特征头（Global Head）的基础上，引入了**空间超图卷积模块（SHCM）**和**时间超图卷积模块（THCM）**：SHCM 在身体部件特征之间自适应构建空间超图，显式建模部件间的高阶空间关系；THCM 则将序列按时序分段，利用 k-NN 策略构建时间超图，捕获跨帧的高阶时间依赖。

在 Gait3D 和 SUSTech1K 两个大规模野外步态数据集上，HyperGait 仅使用解析输入即达到 **80.5%** 和 **79.9%** 的 Rank-1 准确率，显著超越所有单模态方法。消融实验表明，SHCM 和 THCM 的组合相较基线（Backbone + Global Head）提升 **4.8%**，且分别优于其 GCN 对应模块 0.5% 和 1.1%，验证了超图结构相对于传统图卷积的明确优势。定性结果进一步显示，HyperGait 在遮挡和极端视角下仍保持鲁棒，而 ParsingGait 和 XGait 则出现明显错误。

步态识别因其远距离、非侵入的特性，在安防监控、身份认证等领域具有重要应用价值。然而，野外环境中的复杂因素——遮挡、极端视角、衣着变化、携带物等——使得基于传统RGB剪影的步态识别方法面临严峻挑战。人体解析（human parsing）序列能够提供像素级的身体部件语义标签，理论上对衣着和携带物变化具有更强的鲁棒性，因此近年来成为步态识别的研究热点。

现有的基于解析的步态识别方法主要采用两类架构：卷积神经网络（CNN）和图卷积网络（GCN）。CNN类方法（如 **ParsingGait**，Zheng et al., ACM MM 2023）将解析序列视为多通道图像，通过卷积操作提取全局外观特征，但这种方式本质上忽略了不同身体部件之间的结构化关系。GCN类方法（如 **XGait**，Zheng et al., ACM MM 2024）将身体部件建模为图的节点，通过边连接来捕获部件间的成对关系。然而，步态序列中蕴含着复杂的**非线性高阶相关性**——例如，行走时头部、躯干、四肢的运动并非两两独立，而是多部件协同配合的结果；同时，不同时间帧之间的步态模式也存在跨帧的多路依赖关系。传统的图卷积受限于仅能建模成对关系，无法充分捕获这种高阶空间-时间信息，导致解析序列中丰富的结构信息未能被充分利用（Figure 1）。

超图（hypergraph）作为一种广义的图结构，其超边可以连接任意数量的节点，天然适合建模多部件、多帧之间的多路高阶依赖关系（Figure 2）。基于这一洞察，本文提出 **HyperGait** 框架，通过引入超图卷积网络（HGCN），显式捕获步态解析序列中的高阶空间关系和时间相关性，从而释放解析数据在野外步态识别中的全部潜力。

## 核心方法与创新机理

HyperGait 的核心创新在于**引入超图（Hypergraph）建模步态解析序列中的高阶依赖关系**，从而突破了现有 CNN 与 GCN 方法仅能捕捉成对（pairwise）关系的根本局限。其创新点集中体现在三个关键“变动槽”（changed slots）上。

### 从成对关系到多路高阶建模：超图的核心洞察

传统图卷积网络（GCN）通过邻接矩阵定义顶点间的成对连接，无法表达三个或更多身体部位之间、或跨越多个时间帧的复杂协同模式。超图则通过“超边”（hyperedge）连接任意数量的顶点，天然适配步态序列中多部件、多帧之间的多路高阶依赖关系（参见 Figure 2）。HyperGait 正是基于这一洞察，设计了**空间超图卷积模块（SHCM）**和**时序超图卷积模块（THCM）**，分别捕获身体部位间的高阶空间相关性和帧之间的高阶时序相关性。

### 变动槽一：空间特征提取——从全局池化到空间超图卷积

**基线方案**（Backbone + Global Head）仅使用水平金字塔池化（HPP）从全局特征图中提取条带级特征，完全忽略了不同身体部位之间的显式关系建模。**HyperGait 的 SHCM** 则首先利用粗粒度解析掩码（5 个部件：头-躯干、左/右上肢、左/右下肢）提取部件级特征，随后自适应构建空间超图：计算部件特征间的欧氏距离 $D_{ij} = \Vert \hat{\mathbf{Z}}_{i} - \hat{\mathbf{Z}}_{j} \Vert_{2}$，并通过阈值 $\tau$ 决定超边连接：

$$h_{ij} = \begin{cases} 1, & \mathrm{if~} D_{ij} < \tau \\ 0, & \mathrm{otherwise} \end{cases}$$

在此基础上，超图卷积层 $\mathbf{Z}' = D_{v}^{-\frac{1}{2}} H W_{e} D_{e}^{-1} H^{T} W_{v} D_{v}^{-\frac{1}{2}} \Theta(\mathbf{Z})$ 在“顶点—超边—顶点”之间传播信息，实现高阶特征聚合，并经残差连接与批归一化稳定训练。

### 变动槽二：时序聚合——从最大池化到时序超图卷积

基线方案采用时序最大池化（Temporal Pooling）聚合帧特征，将所有帧同等对待，丢失了帧间的结构化时序依赖。**THCM** 将步态序列划分为 $K$ 个时序段，每段选取中间帧作为代表，然后利用 $k$-NN 策略构建时序超图：若第 $j$ 段是第 $i$ 段的 $k_{nn}$ 个最近邻之一，则建立超边连接。该设计使模型能够捕获跨时序段的非局部、高阶时序相关性，而非仅依赖相邻帧的局部平滑。

### 变动槽三：特征融合——从单一全局特征到多粒度联合表示

基线方案仅使用 Global Head 输出的全局特征 $\mathbf{F}_{g}^{i}$ 进行匹配。HyperGait 则将全局特征、空间超图特征 $\mathbf{F}_{s}^{i}$ 和时序超图特征 $\mathbf{F}_{t}^{i}$ 拼接为最终表示：

$$\mathbf{F}_{out}^{i} = \mathrm{Concat}(\mathbf{F}_{g}^{i}, \mathbf{F}_{s}^{i}, \mathbf{F}_{t}^{i})$$

这种融合策略使模型同时保留了全局外观信息、部件间高阶空间关系以及跨帧高阶时序依赖，形成互补的多粒度步态表征。

### 创新有效性的决定性证据

消融实验（Table 3，Gait3D 数据集）直接验证了上述创新的因果效应：

- **SHCM 单独引入**：Rank-1 提升 1.0%（相对 Backbone+Global Head 基线），且**比其 GCN 对应物 S-GCN 高出 0.5%**，证明超图在空间关系建模上优于成对图。
- **THCM 单独引入**：Rank-1 提升 2.2%，**比 T-GCN 高出 1.1%**，表明高阶时序超图建模的显著优势。
- **SHCM + THCM 组合**：Rank-1 总计提升 4.8%（基线 75.7% → 80.5%），远超 GCN 变体组合的 2.4% 增益，确证超图架构是性能跃升的核心因果旋钮。

定性结果（Figure 4）进一步表明，在遮挡和极端视角等野外条件下，HyperGait 的检索结果明显优于 ParsingGait 和 XGait，验证了高阶关系建模带来的鲁棒性提升。

HyperGait 的整体架构围绕一个核心洞察展开：步态解析序列中蕴含的身体部件间高阶空间关系与跨帧高阶时序依赖，天然适合用超图而非普通图来建模。为此，框架设计了三条并行的特征提取通路，最终通过拼接融合形成判别性步态表征。

### 流水线概览

给定一段步态解析序列，HyperGait 的处理流程分为四个阶段：

1. **骨干网络提取帧级特征**  
   对每一帧输入 $\mathbf{x}^{i}$，使用类 ResNet 的 CNN 骨干网络 $F$ 提取中层特征图：
   $$\mathbf{F}^{i} = F(\mathbf{x}^{i})$$
   该特征图作为后续所有模块的共享输入。

2. **Global Head 捕获全局外观**  
   全局头部对 $\mathbf{F}^{i}$ 依次施加时序池化（Temporal Pooling）和水平金字塔池化（Horizontal Pyramid Pooling, HPP，源自 GaitSet），生成全局特征 $\mathbf{F}_{g}^{i}$：
   $$\mathbf{F}_{g}^{i} = H(T(\mathbf{F}^{i}))$$
   这一通路保留了整体的外观轮廓和基本步态模式，但完全忽略了身体部件之间的结构化关系。

3. **两条超图通路并行建模高阶依赖**  
   - **空间超图卷积模块（SHCM）**：利用解析掩码将特征图划分为 5 个粗粒度身体部件（头-躯干、左右上肢、左右下肢），提取部件级特征后自适应构建空间超图，通过超图卷积捕获多个部件之间的高阶空间关系，输出空间超图特征 $\mathbf{F}_{s}^{i}$。
   - **时序超图卷积模块（THCM）**：将帧序列按时序等分为 $K$ 段，每段选取中间帧作为代表帧，利用 $k$-NN 策略构建时序超图，通过超图卷积提取跨段的高阶时序依赖，输出时序超图特征 $\mathbf{F}_{t}^{i}$。

4. **特征融合与最终表征**  
   将三条通路输出的特征沿通道维度拼接，得到帧级融合特征：
   $$\mathbf{F}_{out}^{i} = \mathrm{Concat}(\mathbf{F}_{g}^{i}, \mathbf{F}_{s}^{i}, \mathbf{F}_{t}^{i})$$
   该特征随后经全连接层映射为最终的步态嵌入向量，用于检索匹配。

### 模块间的协同关系

三条通路在功能上互补而非冗余。Global Head 提供全局上下文锚点，SHCM 注入空间结构化的部件交互信息，THCM 则补充时序演化模式。消融实验（Gait3D 数据集）定量验证了这一协同效应：单独添加 SHCM 较 Baseline（Backbone + Global Head）提升 Rank-1 准确率 1.0%，单独添加 THCM 提升 2.2%，而同时引入两个模块带来 4.8% 的增益，显著高于两者独立增益之和，表明空间与时序高阶建模之间存在正向交互。

### 与现有框架的关键差异

相较于先前基于解析的步态识别方法 ParsingGait 和 XGait，HyperGait 的核心区别在于用超图卷积替代了普通图卷积（GCN）。在 Gait3D 上的直接对比显示，SHCM 相较其 GCN 对应物 S-GCN 提升 0.5%，THCM 相较 T-GCN 提升 1.1%。这一优势源于超图能够通过超边同时连接任意数量的节点，天然适配步态场景中“多个身体部件协同运动”与“多帧步态相位耦合”的多路高阶依赖，而 GCN 仅能建模成对关系。

> 注：整体架构的可视化示意请参见 Figure 3。

![[assets/figures/papers/paper_list_l1064_https_openaccess_thecvf_com_content_CVPR2026_html_Zheng_HyperGait_Unleas/figures/003_Figure_3.jpg]]
*Figure 3: The overall architecture of the HyperGait framework, which contains a Global Head, a Spatial Hypergraph Convolution Module (SHCM), and a Temporal Hypergraph Convolution Module (THCM). First, mid-level feature F is extracted from input by backbone. Subsequently, F is processed through the Global Head to yield the global feature*

HyperGait 的整体框架由三个关键模块构成：Global Head、空间超图卷积模块（SHCM）和时间超图卷积模块（THCM），如 Figure 3 所示。输入帧首先经过 Backbone 提取中层特征图 $\mathbf{F}^{i} = F(\mathbf{x}^{i})$，随后该特征分别送入三个分支，最终将三路输出拼接得到判别性步态表示。

### Global Head

Global Head 负责捕捉全局外观特征与基本步态模式。给定帧级特征图 $\mathbf{F}^{i}$，先通过时序池化（Temporal Pooling, TP）聚合时序信息，再采用水平金字塔池化（Horizontal Pyramid Pooling, HPP，源自 **GaitSet** (Chao et al., AAAI 2019)）将特征图沿水平方向切分为多尺度条带，生成全局特征 $\mathbf{F}_{g}^{i} = H(T(\mathbf{F}^{i}))$。

### 空间超图卷积模块（SHCM）

SHCM 的核心目的是显式建模身体部件之间的高阶空间关系。传统 GCN 仅能捕获成对部件间的边连接，而超图允许一条超边连接任意数量的节点，天然适合表达“头部-躯干-四肢”之间的多路协同依赖（见 Figure 2 对比）。

![[assets/figures/papers/paper_list_l1064_https_openaccess_thecvf_com_content_CVPR2026_html_Zheng_HyperGait_Unleas/figures/002_Figure_2.jpg]]
*Figure 2: The difference between Graph and Hypergraph. In this figure, n represents the vertex in the graph or hypergraph, e signifies the hyperedge, W denotes the adjacency matrix of the graph, and H is the incidence matrix of the hypergraph*

**构建流程：**
1. 利用解析掩码将中层特征图划分为 5 个粗粒度身体部件（头-躯干、左上肢、右上肢、左下肢、右下肢），提取各部件特征并归一化得到 $\hat{\mathbf{Z}}_{i}$。
2. 计算部件特征间的欧氏距离 $D_{ij} = \Vert \hat{\mathbf{Z}}_{i} - \hat{\mathbf{Z}}_{j} \Vert_{2}$。
3. 通过阈值 $\tau$ 自适应构建空间超图关联矩阵：

$$h_{ij} = \begin{cases} 1, & \mathrm{if~} D_{ij} < \tau \\ 0, & \mathrm{otherwise} \end{cases}$$

**超图卷积：** 在构建的关联矩阵 $\mathbf{H}$ 上执行顶点-超边-顶点消息传递，实现高阶特征聚合：

$$\mathbf{Z}' = D_{v}^{-\frac{1}{2}} H W_{e} D_{e}^{-1} H^{T} W_{v} D_{v}^{-\frac{1}{2}} \Theta(\mathbf{Z})$$

其中 $\mathbf{D}_{v}$ 和 $\mathbf{D}_{e}$ 分别为顶点度矩阵和超边度矩阵，$\mathbf{W}_{e}$、$\mathbf{W}_{v}$ 为可学习权重，$\Theta(\cdot)$ 为特征变换。最后通过残差连接与批归一化稳定训练：

$$\mathbf{Z}_{out} = \mathrm{ReLU}(\mathrm{BN}(\mathbf{Z}' + \mathbf{Z}))$$

### 时间超图卷积模块（THCM）

THCM 旨在捕获跨帧的高阶时序依赖。与空间超图不同，时序超图采用 k 近邻（k-NN）策略构建：

1. 将步态序列等分为 $K$ 个时序段，每段选取中间帧作为代表帧，提取特征 $\mathbf{T}_{i}$。
2. 计算代表帧间的欧氏距离 $D_{ij} = \Vert \mathbf{T}_{i} - \mathbf{T}_{j} \Vert_{2}$。
3. 基于 k-NN 构建关联矩阵：

$$h_{ij} = \begin{cases} 1, & \mathrm{if~} j \text{ is the } k_{nn} \text{ nearest neighbors of } i \\ 0, & \mathrm{otherwise} \end{cases}$$

在构建的时序超图上执行与 SHCM 相同的超图卷积操作，得到时序超图特征 $\mathbf{F}_{t}^{i}$。

### 特征融合

最终，将三路特征沿通道维度拼接作为完整步态表示：

$$\mathbf{F}_{out}^{i} = \mathrm{Concat}(\mathbf{F}_{g}^{i}, \mathbf{F}_{s}^{i}, \mathbf{F}_{t}^{i})$$

其中 $\mathbf{F}_{g}^{i}$ 为全局特征，$\mathbf{F}_{s}^{i}$ 为空间超图特征，$\mathbf{F}_{t}^{i}$ 为时序超图特征。该融合方式使模型同时保留全局外观、部件间高阶空间关系和跨帧高阶时序动态，互补构成强判别力表示。

## 实验与关键发现

### 主实验结果

HyperGait 在两大野外步态识别基准上均取得领先性能，仅使用解析序列作为输入。在 **SUSTech1K** 数据集上，HyperGait 的 Overall Rank-1 达到 **79.9%**，Overall Rank-5 达到 **93.0%**，在所有单表征方法中排名第一（Table 1）。该数据集涵盖正常行走、背包、换衣、持物、撑伞、穿制服、遮挡和夜间八种复杂条件，HyperGait 在多数子条件下均表现出显著优势，表明超图建模对野外环境变化具有强鲁棒性。

![[assets/figures/papers/paper_list_l1064_https_openaccess_thecvf_com_content_CVPR2026_html_Zheng_HyperGait_Unleas/figures/004_Table_1.jpg]]
*Table 1: Comparison of the SOTA gait recognition methods on the SUSTech1K dataset. NM, BG, CL, CR, UB, UN, OC, and NT denote normal, bags, clothing, carrying, umbrella, uniform, occlusion, and nighttime, respectively*

在 **Gait3D** 数据集上，HyperGait 的 Rank-1 达到 **80.5%**（Table 2），超越所有先前方法。与基于剪影的经典方法（**GaitSet**, Chao et al., AAAI 2019; **GaitPart**, Fan et al., CVPR 2020）、基于骨架的 GCN 方法（**GaitGraph**, Teepe et al., ICIP 2021; **GPGait**, Fu et al., ICCV 2023）以及基于解析的 GCN 方法（**ParsingGait**, Zheng et al., ACM MM 2023; **XGait**, Zheng et al., ACM MM 2024）相比，HyperGait 均取得一致提升。值得注意的是，与多模态方法 **MultiGait**（Fan et al., AAAI 2025）相比，HyperGait 仅用单一解析模态即达到竞争性甚至更优的性能，验证了解析序列在高阶关系建模下的信息潜力被充分释放。

![[assets/figures/papers/paper_list_l1064_https_openaccess_thecvf_com_content_CVPR2026_html_Zheng_HyperGait_Unleas/figures/005_Table_2.jpg]]
*Table 2: Comparison of the SOTA gait recognition methods on the Gait3D dataset*

### 消融实验

消融实验在 Gait3D 数据集上进行，以 **Backbone + Global Head** 作为内部基线（Rank-1 = 75.7%），系统验证各模块贡献（Table 3）。

![[assets/figures/papers/paper_list_l1064_https_openaccess_thecvf_com_content_CVPR2026_html_Zheng_HyperGait_Unleas/figures/007_Table_3.jpg]]
*Table 3: Ablation study results on the Gait3D dataset. Baseline denotes Backbone + Global Head; S-GCN and T-GCN denote Spatial GCN and Temporal GCN, respectively*

**模块独立增益**：单独添加 Spatial Hypergraph Convolution Module（SHCM）使 Rank-1 提升 **1.0%**（达到 76.7%）；单独添加 Temporal Hypergraph Convolution Module（THCM）使 Rank-1 提升 **2.2%**（达到 77.9%）。这表明时序高阶相关性的建模对步态识别的贡献更为关键，但空间部件关系同样不可忽视。

**超图 vs. 图卷积**：将 SHCM 替换为基于图卷积的空间模块（S-GCN），Rank-1 降至 76.2%，SHCM 相对 S-GCN 提升 **0.5%**；将 THCM 替换为时序图卷积模块（T-GCN），Rank-1 降至 76.8%，THCM 相对 T-GCN 提升 **1.1%**。这一对比直接证明了超图相较于传统图卷积的优势——超边能够连接任意数量的节点，从而捕获多部件、多帧之间的多路高阶依赖，而图卷积仅限于成对关系建模。

**联合增益**：同时使用 SHCM 和 THCM 时，Rank-1 达到 **80.5%**，相比基线提升 **4.8%**。相比之下，同时使用 S-GCN 和 T-GCN 仅提升 2.4%（达到 78.1%）。超图组合的增益（4.8%）显著高于 GCN 组合（2.4%），且超过两模块独立增益之和（1.0% + 2.2% = 3.2%），表明空间与时序超图之间存在协同效应——高阶空间关系与时序依赖的联合建模能够相互增强。

### 超图构建策略分析

**空间超图构建**（Table 4）：SHCM 采用基于距离阈值的自适应超图构建策略。实验表明，阈值 $\tau_0 = 0.4$ 时取得最优 Rank-1（80.5%）。阈值过小会导致超边过于稀疏，丢失部件间有效关联；阈值过大则引入噪声连接，稀释关键关系。此外，与固定全连接超图（fully-connected hypergraph）和基于 k-NN 的空间超图相比，自适应阈值策略在所有指标上均表现更优，验证了其灵活捕获不同行走姿态下部件关系的能力。

**时序超图构建**（Table 5）：THCM 将序列划分为 $K$ 个片段，取每段中间帧作为代表，并采用 k-NN 策略构建时序超图。实验表明，$K = 10$ 个片段配合 $k_{nn} = 3$ 个最近邻时性能最优。过少的片段（$K=5$）丢失细粒度时序信息，过多的片段（$K=20$）引入冗余；过小的 $k_{nn}$ 限制了信息传播范围，过大的 $k_{nn}$ 则模糊了关键时序依赖。这一结果说明，适中的时序粒度和邻域范围能够最有效地捕获跨帧的高阶时序相关性。

### 定性分析

**检索结果可视化**（Figure 4）：在极端视角和遮挡条件下，HyperGait 的检索结果明显优于 ParsingGait 和 XGait。当查询样本存在严重遮挡或大角度视角变化时，ParsingGait 和 XGait 均返回了较多错误匹配（红色框），而 HyperGait 能够正确检索到同一身份的目标（绿色框）。这表明超图建模捕获的高阶空间-时序关系为模型提供了更强的身份判别力，使其在外观信息严重缺失时仍能保持鲁棒。

**特征热力图分析**（Figure 5）：对 Global Head 特征 $\mathbf{F}_g$、SHCM 特征 $\mathbf{F}_s$ 和 THCM 特征 $\mathbf{F}_t$ 的可视化显示，三者呈现互补的注意力分布。Global Head 倾向于关注整体轮廓和躯干区域；SHCM 强化了不同身体部件（如四肢与躯干）之间的空间关系响应；THCM 则在时序维度上突出了步态周期中的关键帧和运动相位。这种互补性解释了联合使用三个特征分支的必要性——全局外观、空间高阶关系和时序高阶依赖共同构成了完整的步态身份表征。

### 失败模式与局限性

当前实验分析中未报告明确的失败案例或局限性讨论。从方法设计角度，潜在局限包括：空间超图目前仅使用 5 个粗粒度身体部件，细粒度解析（如手指、脚部）的高阶关系未被探索；时序超图依赖固定分段策略，对步态周期长度变化的自适应能力有限；超图卷积层数仅为一层，更深层的超图架构可能带来进一步增益但尚未验证。以上分析需结合原文进行手动确认。

### 补充图表

![[assets/figures/papers/paper_list_l1064_https_openaccess_thecvf_com_content_CVPR2026_html_Zheng_HyperGait_Unleas/figures/009_Figure_4.jpg]]
*Figure 4: Some exemplar results of Parsinggait, XGait, and our HyperGait. For convenience, we choose the middle frame and the frames with four intervals before and after it for visualization. The blue bounding boxes are queries. The green bounding boxes are the correctly matched results, while the red bounding boxes are the wrong results. The (a) - (c) represent the results under different queries, where the first row of each is the search result of Parsinggait, the second row is the result of XGait, and the third row is the result of HyperGait*

## 定位与知识库关联

### 1. 与现有步态识别范式的继承与突破

HyperGait 的提出根植于步态识别从“轮廓→骨架→解析”的输入模态演进脉络，其核心突破在于将**超图卷积**引入步态解析序列的时空建模，解决了现有方法对高阶多路依赖关系建模不足的瓶颈。

#### 1.1 对解析序列范式的推进

在 HyperGait 之前，以 **ParsingGait** (Zheng et al., ACM MM 2023) 和 **XGait** (Zheng et al., ACM MM 2024) 为代表的解析序列方法已经证明了人体部位解析相较于轮廓和骨架在野外场景下的鲁棒性优势。然而，这些方法在利用解析信息时存在结构性局限：

- **ParsingGait** 采用 GCN 建模身体部位间的空间关系，但 GCN 仅能捕获成对节点间的二阶关系（如“头部-躯干”或“左臂-右臂”），无法同时建模三个及以上部位间的多路协同运动模式。
- **XGait** 虽引入了跨粒度对齐机制，但其空间建模核心仍停留在图结构层面，对时间维度的帧间高阶依赖同样缺乏显式建模。

HyperGait 通过 **空间超图卷积模块 (SHCM)** 和 **时序超图卷积模块 (THCM)** 分别构建空间超图和时序超图，使超边能够连接任意数量的节点，天然适配步态序列中“多部位协同运动”和“多帧周期关联”的高阶语义。这一设计思路与 **GPGait** (Fu et al., ICCV 2023) 等基于骨架的 GCN 方法形成鲜明对比——后者虽引入了广义姿态图，但本质上仍受限于成对边连接的信息传播模式。

#### 1.2 与多模态方法的边界划分

**MultiGait** (Fan et al., AAAI 2025) 通过融合解析、光流等多模态信息取得了有竞争力的性能，但其性能增益部分来源于多模态互补。HyperGait 的定位在于：**仅使用单一解析序列输入**，在 Gait3D 上达到 80.5% Rank-1，在 SUSTech1K 上达到 79.9% Rank-1，证明了超图建模本身即可充分释放解析序列的信息潜力，无需依赖额外的模态信号。

### 2. 关键设计选择与消融证据

#### 2.1 超图 vs. 图卷积的因果性验证

Table 3 的消融实验提供了直接证据，证明超图结构是性能提升的因果关键：

- **SHCM vs. S-GCN**：在相同基线 (Backbone + Global Head) 上，SHCM 比空间 GCN 变体高 0.5% Rank-1，说明超图捕获的多部位高阶关系确实优于成对图建模。
- **THCM vs. T-GCN**：THCM 比时序 GCN 变体高 1.1% Rank-1，表明时序维度的 k-NN 超图构建策略能更有效地提取跨帧的多路依赖。
- **组合增益**：SHCM + THCM 组合较基线提升 4.8%，而 S-GCN + T-GCN 组合仅提升 2.4%，差距达 2.4 个百分点，强有力地证明了超图框架在时空双维度上的协同优势。

#### 2.2 超图构建策略的敏感性

- **空间超图**：距离阈值 $\tau_0=0.4$ 时取得最优 Rank-1 80.5% (Table 4)，阈值过小导致超边过于稀疏（退化为孤立节点），过大则引入噪声连接。
- **时序超图**：$K=10$ 个时序段配合 $k_{nn}=3$ 最近邻时性能最优 (Table 5)，说明适度的时序粒度和局部的 k-NN 连接足以捕获步态周期中的关键高阶时序模式。

### 3. 适用边界与潜在局限

基于现有证据，HyperGait 的适用边界可归纳如下：

1. **输入模态依赖**：方法强依赖人体解析序列的质量。论文未报告解析器（如 human parsing model）本身失效时的性能退化曲线，在极端遮挡或低分辨率场景下解析精度下降对超图构建的影响需进一步验证。
2. **粗粒度部位划分的泛化性**：SHCM 使用 5 个粗粒度身体部位（头-躯干、左/右上肢、左/右下肢）构建空间超图。对于需要细粒度部位区分（如手指、脚踝运动）的应用场景，该固定划分策略可能丢失关键信息。
3. **超图构建的自适应机制**：空间超图使用固定阈值、时序超图使用固定 k-NN 参数，这些超参数在跨数据集迁移时可能需要重新调优，缺乏对输入数据分布的自适应能力。
4. **计算开销**：论文未报告超图卷积层相比于 GCN 的额外计算开销和推理延迟，对于实时应用场景的部署可行性需要进一步评估。

### 4. 开放问题与未来方向

1. **动态超图结构学习**：当前超图构建基于手工设计的距离阈值和 k-NN 策略，能否通过端到端学习自动推断超边连接权重，使超图结构随输入自适应调整？
2. **跨模态超图融合**：HyperGait 证明了单一解析序列的超图建模能力，若将轮廓、骨架等信息也构建为超图并进行跨模态超边对齐，能否进一步提升极端条件下的鲁棒性？
3. **细粒度时空超图**：当前空间超图仅覆盖 5 个粗粒度部位，是否可以通过层次化超图（如部位→子部位→关键点）实现多尺度的空间关系建模？
4. **长序列建模**：THCM 采用分段策略处理时序信息，对于超长步态序列（如持续数分钟的连续行走），当前固定分段策略可能无法有效捕获跨周期的长程依赖。

**注意**：上述适用边界和开放问题部分基于方法设计的逻辑推断，论文原文未提供直接的失败案例分析或局限性讨论，相关结论需结合实际部署场景进行手动验证。

## 原文 PDF

![[paperPDFs/CVPR_2026/HyperGait_Unleashing_the_Power_of_Parsing_for_Gait_Recognition_in_the_Wild_via_Hypergraph.pdf]]
