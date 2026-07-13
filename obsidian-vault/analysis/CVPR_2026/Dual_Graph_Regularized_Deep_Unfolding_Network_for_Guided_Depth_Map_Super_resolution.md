---
title: Dual Graph Regularized Deep Unfolding Network for Guided Depth Map Super-resolution
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/Dual_Graph_Regularized_Deep_Unfolding_Network_for_Guided_Depth_Map_Super_resolution.pdf
project_link: null
code_link: null
aliases:
- DGRDUNGDMSR
tags:
- CVPR_2026
- topic/other_unclear
- topic/other_unclear/general
core_operator: 将二维深度图的行和列分别独立建模为两个低维图，从而将正则化项分解为行方向和列方向的图拉普拉斯约束，在保留分段平滑性的同时大幅降低计算复杂度至 O(H³+W³)，并自然保留图像的二维拓扑结构。
primary_logic: 将引导深度超分辨率重新表述为一个包含双重图拉普拉斯正则化与深度隐式先验的统一变分问题，通过交替方向乘子法（ADMM）将其迭代求解过程展开为可解释的多阶段深度神经网络，实现手工设计先验与数据驱动学习的有效融合。
claims:
- 提出双重图拉普拉斯先验，分别沿行和列方向独立建模结构依赖。
- 将计算复杂度从 O(H³W³) 降低至 O(H³+W³)。
- 将互补先验集成到统一变分优化框架中，并通过交替最小化求解后展开为可解释多阶段深度网络。
- NYU v2 (8×) 上 RMSE = 2.33
---

# Dual Graph Regularized Deep Unfolding Network for Guided Depth Map Super-resolution

> [!tip] 核心洞察
> 将引导深度超分辨率重新表述为一个包含双重图拉普拉斯正则化与深度隐式先验的统一变分问题，通过交替方向乘子法（ADMM）将其迭代求解过程展开为可解释的多阶段深度神经网络，实现手工设计先验与数据驱动学习的有效融合。

| 字段 | 内容 |
|------|------|
| 中文题名 | 双图正则化引导深度超分辨率深度展开网络 |
| 英文题名 | Dual Graph Regularized Deep Unfolding Network for Guided Depth Map Super-resolution |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://openaccess.thecvf.com/content/CVPR2026/html/Zhong_Dual_Graph_Regularized_Deep_Unfolding_Network_for_Guided_Depth_Map_CVPR_2026_paper.html) |
| Topic | #topic/other_unclear #topic/other_unclear/general |
| Method | LapNet |
| Dataset | NYU v2, Sintel, DIDOE |

> [!tip] 效果简介
> - NYU v2 (8×) 上，RMSE 2.33 vs 未明确给出 (所有对比方法均高于此值) (最低)。
> - Sintel (8×) 上，RMSE 5.05。
> - DIDOE (8×) 上，RMSE 5.51。

## 概要

### 问题背景

深度传感器（如ToF相机、LiDAR）在自动驾驶、增强现实与机器人等应用中至关重要，但其原生深度图往往分辨率低、噪声大。引导深度超分辨率（GDSR）旨在利用高分辨率RGB引导图像恢复稠密、高精度的深度图。现有方法大致分为两类：基于滤波的传统模型依赖手工设计的局部平滑先验，难以捕捉远距离结构依赖；基于深度学习的黑箱模型虽能学习复杂映射，但缺乏可解释性且计算开销巨大。

核心瓶颈在于：传统图拉普拉斯先验若构建全局像素亲和图，计算复杂度高达$O(H^3 W^3)$，难以实用；若采用固定局部邻域图，则丢失二维空间拓扑与长程依赖，高频细节恢复不足。

### 核心方法

本文提出**LapNet**，一种基于双重图拉普拉斯正则化的深度展开网络。其核心思想是将二维深度图的行与列分别独立建模为两个低维图，将正则化项分解为行方向与列方向的图拉普拉斯约束。这一设计在保留分段平滑性的同时，将计算复杂度从$O(H^3 W^3)$骤降至$O(H^3 + W^3)$，并自然保留图像的二维拓扑结构。

LapNet将GDSR重新表述为包含**双重图拉普拉斯显式先验**与**深度隐式先验**的统一变分问题，通过交替方向乘子法（ADMM）迭代求解，并将优化过程展开为可解释的多阶段深度网络。网络由初始化模块（INM）、图构建模块（GCM）以及三个交替更新的子模块（UXM、UHM、UJM）组成，其中UJM通过轻量U型网络实现近端算子，将引导图像的高频结构信息注入重建过程。

### 主要结论

在NYU v2、Sintel与DIDOE等主流基准上，LapNet在8×超分辨率任务中均取得最优RMSE（NYU v2上为2.33），同时在推理延迟与模型参数量上保持显著优势（见Figure 1）。消融实验证实：移除任一行或列方向的图正则项均导致性能明显下降；用固定导向滤波器替代学习到的近端网络会引发显著退化；基于L2距离的动态图构造策略优于点积相似度；非共享参数的展开架构在所有迭代次数下均优于共享参数设计，且迭代次数设为3可在性能与参数量间取得最佳平衡。

### 方法谱系与知识库定位

LapNet属于**模型驱动与数据驱动融合**的深度展开方法，其直接对比的基线包括：

- **LGR**（de Lutio et al., CVPR 2022）：学习图正则化用于引导超分辨率，但采用全局像素图，计算复杂度高。
- **DKN**（Kim et al., IJCV 2021）：可变形核联合图像滤波，属于滤波驱动方法，缺乏全局结构建模。
- **DCTNet**（Zhao et al., CVPR 2022）：基于离散余弦变换的GDSR网络，属于频域先验方法。
- **SGNet**（Wang et al., AAAI 2024）：基于梯度-频率感知的结构引导网络，属于多线索融合方法。
- **DORNet**（Wang et al., CVPR 2025）：退化导向正则化网络，面向盲深度超分辨率。

相较于上述方法，LapNet的核心区分点在于：以分解式双重图拉普拉斯替代全局像素图，将计算复杂度从立方级降至行与列独立立方之和；通过ADMM展开实现显式先验与可学习隐式先验的端到端协同优化，兼具可解释性与高性能。

### 引导深度超分辨率的任务定义

深度传感器（如ToF相机、结构光、Lidar）受物理孔径与功耗限制，其输出分辨率远低于同步采集的RGB图像。引导深度超分辨率（Guided Depth Super-Resolution, GDSR）旨在利用高分辨率RGB引导图像的结构信息，将低分辨率深度图恢复为高分辨率深度图。形式上，设低分辨率观测为 $\pmb{y} \in \mathbb{R}^{n}$，目标高分辨率深度图为 $\pmb{x} \in \mathbb{R}^{m}$（$m > n$），退化矩阵为 $\pmb{H} \in \mathbb{R}^{n \times m}$，引导图像为 $\pmb{G}$。该任务是一个高度不适定的逆问题——仅凭数据保真项 $\|\pmb{y} - \pmb{H}\pmb{x}\|_2^2$ 无法唯一确定解，必须引入有效的先验约束。

### 现有方法的瓶颈

当前GDSR方法可大致分为三类：基于显式滤波的模型驱动方法、基于深度学习的端到端回归方法，以及基于图信号处理的图正则化方法。其中，图拉普拉斯正则化因其对分段平滑结构的自然建模能力而备受关注，其核心思想是将深度图视为定义在图上的信号，通过图平滑性度量 $S(\pmb{x}) = \frac{1}{2} \sum_{i,j} w_{i,j} (\pmb{x}_i - \pmb{x}_j)^2 = \pmb{x}^{\top} \pmb{L} \pmb{x}$ 来约束重建。然而，传统图正则化方法面临一个根本性困境：

- **全局像素亲和图**：若在全体像素对上构建亲和图 $\pmb{S} \in \mathbb{R}^{HW \times HW}$，可以捕获任意距离的结构依赖，但图拉普拉斯矩阵的构造与求逆计算复杂度高达 $\mathcal{O}(H^3 W^3)$，即使对于中等分辨率图像也难以承受。
- **局部邻域图**：若仅在固定局部窗口内构建图，虽可降低计算开销，但会丢失远距离依赖关系和二维空间拓扑结构，导致深度图中大尺度平面区域和细长结构恢复不佳。

此外，手工设计的图拉普拉斯先验（如基于亮度相似度的固定权重函数）难以充分表达复杂场景中的高频细节，而纯黑箱深度网络（如 **DKN** (Kim et al., IJCV 2021)、**DCTNet** (Zhao et al., CVPR 2022)、**SGNet** (Wang et al., AAAI 2024)）虽然性能强劲，却缺乏可解释性，且参数量往往较大（SGNet达25.33M参数）。

### 核心动机与突破口

本文的核心洞察在于：**深度图的二维结构可以沿行和列方向分解为两个低维图**。具体而言，将深度图 $\pmb{X} \in \mathbb{R}^{H \times W}$ 的行空间和列空间分别建模为独立的图，构造行拉普拉斯矩阵 $\pmb{L}_r \in \mathbb{R}^{H \times H}$ 和列拉普拉斯矩阵 $\pmb{L}_c \in \mathbb{R}^{W \times W}$。双图正则化项可分解为：

$$\operatorname*{min}_{\pmb{X}} \; tr(\pmb{X}^{\top} \pmb{L}_r \pmb{X}) + tr(\pmb{X} \pmb{L}_c \pmb{X}^{\top})$$

这一设计将计算复杂度从 $\mathcal{O}(H^3 W^3)$ 降至 $\mathcal{O}(H^3 + W^3)$，同时自然保留了图像的二维拓扑结构——行图捕获垂直方向的结构依赖，列图捕获水平方向的结构依赖。

基于此，本文进一步将GDSR形式化为一个统一变分框架，融合数据保真项、双向图拉普拉斯正则化与可学习的深度隐式先验 $f(\pmb{X}, \pmb{G})$，并通过交替方向乘子法（ADMM）将其迭代求解过程展开为可解释的多阶段深度网络 **LapNet**，实现手工设计先验与数据驱动学习的有效融合。

## 核心方法与创新机理

### 瓶颈与设计动机

引导深度超分辨率（GDSR）的核心挑战在于如何从低分辨率深度图与高分辨率引导图像中恢复出锐利、结构一致的高分辨率深度图。传统方法常引入图拉普拉斯先验来强制分段平滑性，但面临两难困境：构建全局像素亲和图可保留长距离依赖，却带来 $O(H^3W^3)$ 的灾难性计算复杂度；使用固定局部邻域图虽计算轻量，却丢失了二维空间结构与远距离依赖，且手工设计的先验难以充分恢复高频细节。

### 关键改变槽位（Changed Slots）

LapNet 的核心创新可归纳为三个关键槽位的系统性改变，它们共同构成了从“手工先验+黑箱回归”到“结构化显式先验+深度隐式先验+可解释展开”的范式转换。

#### 槽位一：图拉普拉斯正则化形式

| 维度 | 基线方案 | LapNet 方案 |
|------|----------|-------------|
| 图结构 | 全局像素亲和图（$O(H^3W^3)$）或固定局部邻域图 | 双重行列图拉普拉斯（$O(H^3+W^3)$） |
| 方向建模 | 无方向区分 | 分别沿行和列方向独立构建低维亲和图 |
| 拓扑保留 | 向量化后丢失二维结构 | 自然保留图像的二维拓扑结构 |

**机制分析**：LapNet 将 $H \times W$ 的深度图视为 $H$ 个行信号与 $W$ 个列信号的集合，分别构建 $H \times H$ 的行拉普拉斯矩阵 $\pmb{L}_r$ 和 $W \times W$ 的列拉普拉斯矩阵 $\pmb{L}_c$。正则化项分解为行方向平滑项 $\mathrm{tr}(\pmb{X}^\top \pmb{L}_r \pmb{X})$ 与列方向平滑项 $\mathrm{tr}(\pmb{X} \pmb{L}_c \pmb{X}^\top)$，两者协同约束深度图在水平和垂直方向上的分段平滑性，同时将计算复杂度从立方级依赖像素总数降至立方级依赖图像边长。

#### 槽位二：先验建模方式

| 维度 | 基线方案 | LapNet 方案 |
|------|----------|-------------|
| 显式先验 | 手工设计的全局/局部图正则 | 可学习的动态双重图拉普拉斯正则 |
| 隐式先验 | 端到端黑箱网络隐式学习 | 通过近端网络显式注入的深度隐式先验 $f(\pmb{X}, G)$ |
| 融合机制 | 分离设计或简单加权 | 统一变分框架下的互补融合 |

**机制分析**：LapNet 将显式的双重图拉普拉斯先验与数据驱动的深度隐式先验统一在同一个变分目标函数中（Eq. 10）。其中，图拉普拉斯项通过可学习的 $\sigma$ 参数动态构建亲和图（基于 L2 距离的相似度函数），提供了结构化、可解释的平滑约束；深度隐式先验 $f(\pmb{X}, G)$ 则由一个轻量 U 型近端网络实现，负责从引导图像中提取高频结构信息并注入重建过程。二者通过 ADMM 框架的交替优化实现协同，而非简单的线性组合。

#### 槽位三：优化/推理策略

| 维度 | 基线方案 | LapNet 方案 |
|------|----------|-------------|
| 范式 | 端到端黑箱回归或传统模型驱动迭代 | 基于 ADMM 的深度展开网络 |
| 可解释性 | 低（黑箱）或中等（手工迭代） | 高——每阶段对应 ADMM 的一个迭代步 |
| 模块化 | 整体网络 | 五个功能模块：INM、GCM、UXM、UHM、UJM |

**机制分析**：LapNet 将 ADMM 求解变分问题的迭代过程展开为 $K$ 阶段的可学习深度网络。每个阶段包含三个更新模块——UXM（更新深度图 $\pmb{X}$，通过闭式解融合数据保真项与行方向图正则）、UHM（更新辅助变量 $\pmb{H}$，施加列方向图正则）、UJM（通过近端网络更新 $\pmb{J}$，注入引导先验）——以及一个图构建模块 GCM（从当前深度估计动态构建行列拉普拉斯矩阵）。这种展开架构使得网络行为与优化算法严格对应，同时允许所有模块参数（包括惩罚系数 $\lambda, \alpha, \beta$、图构建参数 $\sigma$、近端网络权重）通过端到端训练联合学习。消融实验证实，非共享参数的展开架构在所有迭代次数下均优于共享参数设计（Figure 7a），且 $K=3$ 次展开迭代在性能与参数量之间取得最佳平衡（Figure 7b）。

### 复杂度优势的量化支撑

双重图拉普拉斯的核心理论优势在于计算复杂度的根本性降低：从全局亲和图方案的 $O(H^3W^3)$ 降至 $O(H^3+W^3)$。这一降低源于将 $HW \times HW$ 的拉普拉斯矩阵分解为 $H \times H$ 与 $W \times W$ 两个独立矩阵，使得矩阵求逆等关键操作的规模从像素总数降至图像边长。在 16× 超分辨率任务中，LapNet 及其轻量变体 LapNet-T 在 PSNR-延迟散点图上均位于 Pareto 前沿（Figure 1），验证了理论效率优势向实际推理速度的有效转化。

### 证据强度说明

上述三个槽位的改变均有高置信度证据支撑（confidence ≥ 0.95），直接引自已发表论文的方法章节与消融实验。需要手动验证的是：LapNet 在实际部署中是否确实达到理论复杂度边界，以及矩阵求逆操作在极高分辨率（如 4K 深度图）下是否成为新的瓶颈——论文自身将此列为限制因素之一。

LapNet 将引导深度超分辨率（GDSR）重新表述为一个包含**双重图拉普拉斯正则化**与**深度隐式先验**的统一变分优化问题，并通过**交替方向乘子法（ADMM）**将其迭代求解过程展开为可解释的多阶段深度网络。整个网络由五个核心模块构成，按 K 个阶段交替执行，形成端到端可训练的信息流。

### 问题形式化

给定低分辨率深度图 Y 和引导图像 G，目标是从降质模型 Y = D X 中恢复高分辨率深度图 X（D 为下采样算子）。传统图拉普拉斯先验将深度图所有像素构建为全局亲和图，其正则化项的计算复杂度高达 O(H³W³)，且难以保留图像的二维拓扑结构。LapNet 的核心创新在于将二维深度图的行和列**分别独立建模**为两个低维图，从而将正则化项分解为行方向和列方向的图拉普拉斯约束（见 Figure 2）。这一设计的直接收益是将计算复杂度从 O(H³W³) 降至 O(H³+W³)（见 verified_analysis 中置信度 0.95 的复杂度声明）。

总体目标函数融合了四项互补约束：

$$
\operatorname*{min}_{\pmb{X}} \| \pmb{Y} - \pmb{D} \pmb{X} \|_F^2 + \lambda\, \mathrm{tr}(\pmb{X}^{\top} \pmb{L}_r \pmb{X}) + \alpha\, \mathrm{tr}(\pmb{X} \pmb{L}_c \pmb{X}^{\top}) + \beta\, f(\pmb{X}, \pmb{G})
$$

其中：第一项为数据保真项，确保重建结果与低分辨率输入一致；第二、三项分别为**行方向**和**列方向**的图拉普拉斯正则化（L_r 和 L_c 为对应维度的拉普拉斯矩阵），显式施加分段平滑先验；第四项 f(X, G) 为可学习的**深度隐式先验**，通过引导图像注入高频结构信息。

### 从优化到网络展开

上述目标函数通过引入辅助变量 J 和 H（满足约束 X=J, X=H）转化为 ADMM 可求解形式，构建增广拉格朗日函数（Eq. 11）。ADMM 的每次迭代包含三个子问题的交替求解：

1. **X 子问题**：融合数据保真项与行方向图正则化，存在闭式解（Eq. 14），由 UXM 模块执行。
2. **H 子问题**：施加列方向图正则化，同样具有闭式解（Eq. 16），由 UHM 模块执行。
3. **J 子问题**：通过近端算子将引导图像的结构信息融入重建过程（Eq. 18），由 UJM 模块中的轻量 U 型网络实现。

这三个更新步骤与图构建模块（GCM）交替执行，形成 K 阶段的迭代展开架构（Figure 3a）。每个阶段均包含可学习的参数，且**阶段间参数不共享**（消融实验证实非共享设计在所有迭代次数下 RMSE 均更低，见 Figure 7a）。

### 模块职责与数据流

LapNet 的完整数据流如下（对应 Figure 3 的架构示意）：

![[assets/figures/papers/paper_list_l2470_https_openaccess_thecvf_com_content_CVPR2026_html_Zhong_Dual_Graph_Regul/figures/003_Figure_3.jpg]]
*Figure 3: Detailed architecture of the proposed LapNet for guided depth map super-resolution. (a) Overall iterative unfolding architecture, which alternates between graph construction and three update modules across K stages; (b) Initialization Module (INM) that jointly encodes Yˆ and G to produce initial estimates of*

- **Initialization Module (INM)**：联合编码初始上采样深度图 Ŷ 和引导图像 G，生成初始变量 X₀、J₀ 和 H₀（Figure 3b）。该模块为后续迭代提供合理的初始估计。
- **Graph Construction Module (GCM)**：从当前深度估计 X_t 出发，分别沿行和列方向构建亲和图 S_r、S_c，进而计算对应的拉普拉斯矩阵 L_{r,t} 和 L_{c,t}（Figure 3a 中 GCM 块）。图构建采用基于 L2 距离的动态相似度函数（见 verified_analysis 中 L2 距离相似度公式），其带宽参数 σ 可端到端学习。
- **Update X Module (UXM)**：利用 GCM 输出的行拉普拉斯矩阵，通过闭式解更新深度图 X_{t+1}，融合数据保真项与行方向平滑约束。
- **Update H Module (UHM)**：利用列拉普拉斯矩阵，通过闭式解更新辅助变量 H_{t+1}，施加列方向平滑约束。
- **Update J Module (UJM) / Proximal Network**：以轻量 U 型网络实现近端算子，接收 X_{t+1} 和对偶变量信息，结合引导图像 G 生成 J_{t+1}，将引导图像的高频结构注入重建过程（Figure 3d）。

各阶段间通过对偶变量 M 和 N 的更新（遵循标准 ADMM 乘子更新规则）传递约束信息，确保辅助变量与主变量 X 的一致性。整个网络以 K=3 次展开迭代作为默认设置（Figure 7b 显示该设置在性能与参数量间取得最佳平衡）。

### 与现有方法的架构差异

相较于纯黑箱回归网络（如 **SGNet** (Wang et al., AAAI 2024)、**DCTNet** (Zhao et al., CVPR 2022)），LapNet 的每个模块均对应优化算法中的明确步骤，具有可解释性。相较于传统模型驱动方法（如 **LGR** (de Lutio et al., CVPR 2022) 的固定图结构），LapNet 的图拉普拉斯矩阵和近端网络均为数据驱动学习，实现了手工先验与学习先验的融合。双重图分解策略是 LapNet 区别于所有现有图正则化方法的独特设计——它既避免了全局像素图的计算爆炸，又保留了二维空间结构，而局部邻域图方法（如固定窗口滤波）则丢失了远距离依赖。

LapNet 的核心设计源于对引导深度超分辨率问题的统一变分建模，并通过交替方向乘子法（ADMM）将其迭代求解过程展开为可解释的多阶段深度网络。本节梳理其关键模块与核心公式的推导逻辑。

### 问题建模：双重图拉普拉斯正则化

传统图拉普拉斯先验在深度图上构建全局像素亲和图时，计算复杂度高达 $O(H^3W^3)$，而局部邻域图则丢失了远距离依赖和二维空间结构。LapNet 的核心创新在于提出**双重图拉普拉斯先验**：将深度图的行和列分别视为独立的低维图，从而将正则化项分解为行方向和列方向的图拉普拉斯约束。

数据保真项采用 Frobenius 范数约束低分辨率深度 $\mathbf{Y}$ 与下采样后的高分辨率深度 $\mathbf{X}$ 的一致性：

$$\min_{\mathbf{X}} \|\mathbf{Y} - \mathbf{D}\mathbf{X}\|_F^2$$

双重图拉普拉斯正则化项分别沿行和列方向施加分段平滑约束：

$$\min_{\mathbf{X}} \mathrm{tr}(\mathbf{X}^{\top} \mathbf{L}_r \mathbf{X}) + \mathrm{tr}(\mathbf{X} \mathbf{L}_c \mathbf{X}^{\top})$$

其中 $\mathbf{L}_r \in \mathbb{R}^{H \times H}$ 和 $\mathbf{L}_c \in \mathbb{R}^{W \times W}$ 分别为行方向和列方向的拉普拉斯矩阵。这一分解将计算复杂度从 $O(H^3W^3)$ 降至 $O(H^3+W^3)$，同时自然保留了深度图的二维拓扑结构。

### 统一优化目标

将数据保真项、双重图正则化与可学习的深度隐式先验 $f(\mathbf{X}, \mathbf{G})$（其中 $\mathbf{G}$ 为引导图像）统一为以下目标函数：

$$\min_{\mathbf{X}} \|\mathbf{Y} - \mathbf{D}\mathbf{X}\|_F^2 + \lambda \mathrm{tr}(\mathbf{X}^{\top} \mathbf{L}_r \mathbf{X}) + \alpha \mathrm{tr}(\mathbf{X} \mathbf{L}_c \mathbf{X}^{\top}) + \beta f(\mathbf{X}, \mathbf{G})$$

其中 $\lambda$、$\alpha$、$\beta$ 为可学习的惩罚参数，在训练过程中自适应演化（见 Figure 6(a)）。

### ADMM 迭代求解

为解耦各正则化项，引入辅助变量 $\mathbf{J}$ 和 $\mathbf{H}$，满足约束 $\mathbf{X} = \mathbf{J}$ 和 $\mathbf{X} = \mathbf{H}$，构造增广拉格朗日函数：

$$\Phi_\mu = \|\mathbf{Y} - \mathbf{D}\mathbf{X}\|_F^2 + \lambda \mathrm{tr}(\mathbf{X}^{\top} \mathbf{L}_r \mathbf{X}) + \alpha \mathrm{tr}(\mathbf{H} \mathbf{L}_c \mathbf{H}^{\top}) + \beta f(\mathbf{J}, \mathbf{G}) + \frac{\mu}{2}\|\mathbf{X} - \mathbf{J} + \frac{\mathbf{M}}{\mu}\|_F^2 + \frac{\mu}{2}\|\mathbf{X} - \mathbf{H} + \frac{\mathbf{N}}{\mu}\|_F^2$$

其中 $\mathbf{M}$、$\mathbf{N}$ 为拉格朗日乘子，$\mu$ 为惩罚参数。ADMM 交替更新各变量：

**X 子问题（闭式解）**：融合数据保真项与行方向图正则化，具有闭式解：

$$\mathbf{X}_{t+1} = (\mathcal{D}^{\top} \mathcal{D} + \lambda \mathcal{L}_{r,t} + \mu \mathcal{I}_r)^{-1} (\mathcal{D}^{\top} \mathcal{Y} + \frac{\mu_t}{2} (\mathcal{J}_t + \mathcal{H}_t - \frac{\mathbf{M}_t + \mathbf{N}_t}{\mu_t}))$$

**H 子问题（闭式解）**：施加列方向图正则化：

$$\mathbf{H}_{t+1} = (\mu \mathbf{X}_{t+1} + \mathbf{N}_t) (\mu \mathbf{I}_c + 2\alpha \mathbf{L}_{c,t+1})^{-1}$$

**J 子问题（近端算子）**：通过轻量 U 型网络实现近端算子，将引导图像的高频结构信息注入重建过程：

$$\mathbf{J}_{t+1} = \mathrm{Prox}(\mathbf{X}_{t+1} + \frac{\mathbf{M}_t}{\mu}, \mathbf{G})$$

### 深度展开网络架构

上述 ADMM 迭代过程被展开为 $K$ 阶段的可学习深度网络 LapNet，包含五个关键模块（见 Figure 3）：

1. **初始化模块（INM）**：联合编码初始上采样深度图 $\hat{\mathbf{Y}}$ 和引导图像 $\mathbf{G}$，生成初始估计 $\mathbf{X}_0$、$\mathbf{J}_0$ 和 $\mathbf{H}_0$。
2. **图构建模块（GCM）**：从当前深度估计 $\mathbf{X}_t$ 构建行列亲和图，采用基于 L2 距离的动态相似度函数 $S_{i,j} = \exp(-\frac{\|x_i - x_j\|_2^2}{\sigma^2})$（$\sigma$ 可学习），进而生成拉普拉斯矩阵 $\mathbf{L}_r$、$\mathbf{L}_c$。
3. **更新 X 模块（UXM）**：利用闭式解更新深度图 $\mathbf{X}$。
4. **更新 H 模块（UHM）**：利用闭式解更新辅助变量 $\mathbf{H}$。
5. **更新 J 模块（UJM）/ 近端网络**：通过轻量 U 型网络实现近端算子，融入深度引导先验。

### 关键公式变量说明

| 符号 | 含义 |
|------|------|
| $\mathbf{Y}$ | 低分辨率深度图 |
| $\mathbf{X}$ | 待恢复的高分辨率深度图 |
| $\mathbf{D}$ | 下采样算子 |
| $\mathbf{G}$ | 引导图像（RGB） |
| $\mathbf{L}_r, \mathbf{L}_c$ | 行/列方向图拉普拉斯矩阵 |
| $\lambda, \alpha, \beta$ | 各正则化项的可学习惩罚参数 |
| $\mathbf{J}, \mathbf{H}$ | ADMM 辅助变量 |
| $\mathbf{M}, \mathbf{N}$ | 拉格朗日乘子 |
| $\mu$ | ADMM 惩罚参数 |
| $f(\cdot)$ | 深度隐式先验函数 |
| $\mathrm{Prox}(\cdot)$ | 近端算子，由 U 型网络实现 |

## 实验与关键发现

### 主要结果

LapNet 在多个基准数据集上取得了最优的深度超分辨率重建精度，同时保持了较低的计算延迟。Table 1 报告了各方法在 NYU v2、Sintel、DIDOE 等数据集上不同放大倍率下的 RMSE 比较结果。在 NYU v2 数据集 8× 超分辨率任务上，LapNet 取得了 2.33 的 RMSE，优于所有对比方法（Table 3 及 Figure 6(b)）。在 Sintel 和 DIDOE 数据集 8× 任务上，RMSE 分别达到 5.05 和 5.51。

![[assets/figures/papers/paper_list_l2470_https_openaccess_thecvf_com_content_CVPR2026_html_Zhong_Dual_Graph_Regul/figures/004_Table_1.jpg]]
*Table 1: RMSE comparison of various guided depth map super-resolution (GDSR) methods on benchmark datasets. The top two results are highlighted in first and second, respectively*

![[assets/figures/papers/paper_list_l2470_https_openaccess_thecvf_com_content_CVPR2026_html_Zhong_Dual_Graph_Regul/figures/007_Figure_6.jpg]]
*Figure 6: Ablation study. (a) Evolution of the penalty parameters α, λ and*

![[assets/figures/papers/paper_list_l2470_https_openaccess_thecvf_com_content_CVPR2026_html_Zhong_Dual_Graph_Regul/figures/010_Table_3.jpg]]
*Table 3: Ablation Study. Evaluation of various graph construction strategies for 8× GDSR in terms of RMSE*

Figure 1 展示了在 NYU v2 数据集 16× 引导深度超分辨率任务上各方法的 PSNR 与推理延迟的散点分布。LapNet（24 特征图）在取得最高 PSNR 的同时，其延迟显著低于 DORNet、SGNet 等方法；轻量变体 LapNet-T（8 特征图）进一步将延迟降低至与 DCTNet 相当的水平，同时仍保持具有竞争力的重建质量。这一效率优势源于双重图拉普拉斯先验将计算复杂度从 $\mathcal{O}(H^3 W^3)$ 降至 $\mathcal{O}(H^3 + W^3)$ 的设计。

![[assets/figures/papers/paper_list_l2470_https_openaccess_thecvf_com_content_CVPR2026_html_Zhong_Dual_Graph_Regul/figures/001_Figure_1.jpg]]
*Figure 1: Quantitative comparison on the NYU v2 dataset [10] for 16× GDSR. “LapNet” denotes our full model with 24 feature maps, while “LapNet-T” represents a lightweight variant with 8 feature maps. The latency of each model is measured on the same NVIDIA RTX 5090 GPU using a 60 × 60 LR depth map as input*

在真实世界数据集 RGB-D-D 上，LapNet 同样表现出色（Table 2），验证了该方法对真实深度传感器退化具有一定的泛化能力。Figure 5 的可视化对比显示，LapNet 在深度边缘和细小结构处能恢复出更清晰、更准确的深度值，误差图也表明其重建误差分布更为均匀且幅度更小。

![[assets/figures/papers/paper_list_l2470_https_openaccess_thecvf_com_content_CVPR2026_html_Zhong_Dual_Graph_Regul/figures/006_Table_2.jpg]]
*Table 2: RMSE comparison with the different methods on RGB-D-D [42] dataset for real-world depth map super-resolution*

### 消融实验

**双重图正则化的必要性。** Figure 6(b) 对比了三种模型变体在 NYU v2、Sintel 和 DIDOE 数据集 8× 任务上的 RMSE：Model1 仅使用行方向图拉普拉斯正则化，Model2 仅使用列方向正则化，LapNet 同时使用两个方向。移除任一行或列方向的图拉普拉斯约束均导致 RMSE 明显上升，证明了双向图建模对于保留深度图二维结构信息的必要性。

**先验建模策略的影响。** Table 4 比较了不同先验建模策略在 8× 引导深度超分辨率下的 RMSE。用固定导向滤波器替代学习到的近端网络（UJM）会引发显著的性能退化，表明可学习的深度隐式先验对于从引导图像中提取高频结构信息至关重要。仅使用手工设计的双重图正则化而不引入深度隐式先验同样导致精度下降，验证了两类先验的互补性。

**图构造策略的选择。** Table 3 评估了不同图构造策略对 RMSE 的影响。基于 L2 距离的动态图构造（L2-based dynamic）在 RMSE 上优于基于点积相似度的构造方式，被选为默认设置。该策略利用可学习的尺度参数 $\sigma$ 自适应调整亲和力矩阵的稀疏程度，从而更灵活地捕捉深度图中的结构依赖关系。

**展开迭代次数与参数共享。** Figure 7(a) 比较了共享参数与非共享参数设置下不同迭代次数的 RMSE 表现。非共享参数的展开架构在所有迭代次数下均一致优于共享参数设计，表明各阶段独立学习有助于适应迭代过程中变量分布的变化。Figure 7(b) 显示模型参数量随迭代次数线性增长，设置展开迭代次数为 3 可在性能与模型复杂度之间取得最佳平衡——继续增加迭代次数带来的精度提升趋于饱和，而参数量持续增加。

**惩罚参数的动态演化。** Figure 6(a) 展示了训练过程中惩罚参数 $\alpha$、$\lambda$ 和 $\beta$ 的演化曲线。这些参数从较小的初始值逐渐增大并趋于稳定，表明网络在训练过程中自适应地调整各项正则化的权重，最终收敛到一组平衡数据保真、图平滑性和深度先验的配置。

### 失败模式与局限性

尽管 LapNet 在多个基准上取得了领先性能，其仍存在以下局限：

1. **新场景泛化有限。** 深度隐式先验通过近端网络从训练数据中学习，其有效性依赖于训练分布。当测试场景的深度结构或引导图像模态与训练集存在显著差异时，该先验可能无法提供准确的引导信息，导致重建质量下降。这一局限性在真实世界数据集 RGB-D-D 上虽未造成显著性能损失，但极端域外场景下的鲁棒性仍需进一步验证。

2. **高分辨率下的计算瓶颈。** 虽然双重图拉普拉斯先验将复杂度从 $\mathcal{O}(H^3 W^3)$ 降至 $\mathcal{O}(H^3 + W^3)$，但 UXM 和 UHM 模块中的矩阵求逆操作（Eq. (14) 和 Eq. (16)）在极高分辨率输入（如 4K 深度图）时仍可能成为计算瓶颈。当前实验均在常规分辨率下进行，未涉及此类极端场景的评估。

3. **盲超分辨率场景未覆盖。** 现有实验假设降质模型（如下采样算子 $\mathcal{D}$）已知，未评估在完全盲超分辨率场景（即降质核未知）下的性能。实际应用中深度传感器的退化过程往往更为复杂且不可知，这一设定限制了方法在无校准条件下的直接部署。

4. **移动端部署验证缺失。** 虽然 LapNet-T 在延迟上展现了轻量化的潜力，但未见在移动端或嵌入式设备上的实际部署验证报告。矩阵运算在资源受限硬件上的实际推理效率仍需进一步测试。

### 开放问题

1. 双重图拉普拉斯正则化框架能否扩展至其他图像恢复任务（如深度补全、光流估计），其行列解耦的思想是否具有通用性？
2. 如何进一步提升深度隐式先验的域外泛化能力，例如通过元学习或测试时自适应策略？
3. 矩阵求逆操作是否可以通过近似算法（如共轭梯度法、切比雪夫多项式近似）替代，以进一步降低高分辨率场景下的计算开销？
4. 对不同类型深度传感器噪声（如 ToF 的多路径干扰、结构光的遮挡噪声）的鲁棒性尚未深入分析，这在实际部署中至关重要。

## 定位与知识库关联

### 1. 与基线方法的比较与定位

LapNet 的核心技术贡献在于将**双重图拉普拉斯正则化**与**深度隐式先验**统一到一个可解释的深度展开框架中，其设计直接回应了引导深度超分辨率（GDSR）领域中两类主流方法的瓶颈。

**图正则化方法的演进与突破**：基于图拉普拉斯先验的方法通过在深度图上构建亲和图来施加分段平滑约束。早期方法面临两难困境：构建全局像素亲和图可保留长距离依赖，但计算复杂度高达 $O(H^3 W^3)$，难以应用于高分辨率输入；使用固定局部邻域图虽降低了计算量，却丢失了二维空间结构的完整性。**LGR**（de Lutio et al., CVPR 2022）虽然将图正则化引入学习框架，但其图结构仍受限于传统构建方式。LapNet 的关键突破在于将二维深度图的行和列分别独立建模为两个低维图，将计算复杂度降至 $O(H^3 + W^3)$，同时自然保留图像的二维拓扑结构。消融实验（Table 4）证实，移除任一行或列方向的图正则化均会导致 RMSE 明显上升，验证了双向图约束的必要性。

**深度展开网络与模型驱动方法的融合**：端到端黑箱回归方法（如 **DKN** (Kim et al., IJCV 2021)、**DCTNet** (Zhao et al., CVPR 2022)）虽能学习复杂的映射关系，但缺乏可解释性且对数据分布敏感。近期工作如 **DORNet**（Wang et al., CVPR 2025）开始探索退化导向的正则化，但仍未显式建模二维结构先验。LapNet 将包含双重图拉普拉斯正则化与深度隐式先验的统一变分问题，通过 ADMM 迭代求解过程展开为 K 阶段可学习网络，实现了手工设计先验与数据驱动学习的有效融合。这种设计使得每个模块（UXM、UHM、UJM）都具有明确的优化解释，而非黑箱操作。

**与结构引导方法的差异**：**SGNet**（Wang et al., AAAI 2024）通过梯度-频率感知机制利用引导图像的结构信息，而 LapNet 通过近端网络（UJM）将引导图像的高频结构注入重建过程，同时保留了图正则化对深度图本身平滑性的显式约束。Table 1 的定量结果表明，LapNet 在 NYU v2 8× 超分辨率任务上取得了最低的 RMSE（2.33），优于包括 SGNet 在内的所有对比方法。

### 2. 适用边界与局限

**数据分布依赖性**：深度隐式先验通过可学习网络 $f(\cdot)$ 实现，其性能依赖于训练数据的分布特征。对于与训练场景差异显著的新场景（如不同传感器类型、极端光照条件），先验的有效性可能下降。这一局限在论文中仅被定性提及，缺乏跨域泛化的定量评估，需要手动验证。

**计算瓶颈的残余**：虽然复杂度从 $O(H^3 W^3)$ 降至 $O(H^3 + W^3)$，但 UXM 和 UHM 模块中的矩阵求逆操作（Eq. (14) 和 Eq. (16)）在极高分辨率输入（如 4K 深度图）时仍可能成为计算瓶颈。论文未提供在此类极端分辨率下的延迟或显存消耗数据。

**盲超分辨率场景的缺失**：当前 LapNet 假设退化过程（下采样算子 $\mathbf{D}$）已知，未涉及完全盲超分辨率场景下的性能评估。在实际应用中，深度传感器的退化过程往往未知且复杂，这一假设限制了方法的直接部署能力。

### 3. 开放问题

**部署可行性的验证缺失**：论文在 NVIDIA RTX 5090 上报告了推理延迟（Figure 1），但未见在移动端或嵌入式设备上的部署验证。考虑到深度超分辨率在 AR/VR、移动机器人等场景中的实际需求，轻量变体 LapNet-T 在资源受限平台上的性能与效率权衡仍需进一步研究。

**传感器噪声鲁棒性分析不足**：不同类型的深度传感器（ToF、结构光、双目匹配）具有不同的噪声特性（如飞行时间噪声、散斑噪声、匹配误差）。论文未深入分析 LapNet 对不同噪声模型的鲁棒性，这在实际多传感器融合场景中可能成为关键限制因素。

**图构建策略的理论分析**：Table 3 表明基于 L2 距离的动态图构造策略（$S_{i,j} = \exp(-\|x_i - x_j\|_2^2 / \sigma^2)$）在 RMSE 上优于点积相似度构造方式，但论文未从理论上解释为何 L2 距离更适合深度图的图结构建模。这一选择的原理性分析有助于指导未来图构建策略的设计。

## 原文 PDF

![[paperPDFs/CVPR_2026/Dual_Graph_Regularized_Deep_Unfolding_Network_for_Guided_Depth_Map_Super_resolution.pdf]]
