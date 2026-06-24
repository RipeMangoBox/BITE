---
title: "PQDT: Pseudo-Query Dual Transformer for Robust Point Cloud Restoration"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/PQDT_Pseudo_Query_Dual_Transformer_for_Robust_Point_Cloud_Restoration.pdf
project_link: null
code_link: "https://github.com/ins-uni-bonn/PQDT"
aliases:
- PQDT
tags:
- CVPR_2026
- topic/other_unclear
- topic/other_unclear/general
core_operator: 通过两阶段伪查询生成与细化（观察引导阶段和先验引导阶段）以及动态查询选择，自适应地平衡输入保真度与学习到的形状先验，从而在不同退化下都能恢复高质量几何。
primary_logic: 引入辅助伪查询作为抗噪声锚点，结合双Transformer解码与自适应查询选择，使网络既能从观测中稳定粗略几何，又能利用先验细化细节，显著提升鲁棒性与几何忠实度。
claims:
- 在ShapeNet-55/34上，PQDT在所有难度级别（Simple/Moderate/Hard）和所有类别（seen/unseen）上均达到最优CD-S、CD-M、CD-H、平均CDℓ2和F1分数。
- 在PFS数据集上，PQDT的CDℓ2相比次优方法降低76.8%，F1-Score提高27.1%。
- 消融实验显示，引入伪查询与动态查询选择使CD降低0.17、F1提高0.012；几何嵌入进一步带来增益，完整模型达到最佳CDℓ2 0.818和F1 0.261。
- ShapeNet-55/34 上 CD-S = 0.34
---

# PQDT: Pseudo-Query Dual Transformer for Robust Point Cloud Restoration

> [!tip] 核心洞察
> 引入辅助伪查询作为抗噪声锚点，结合双Transformer解码与自适应查询选择，使网络既能从观测中稳定粗略几何，又能利用先验细化细节，显著提升鲁棒性与几何忠实度。

| 字段 | 内容 |
|------|------|
| 中文题名 | PQDT：用于鲁棒点云恢复的伪查询双Transformer网络 |
| 英文题名 | PQDT: Pseudo-Query Dual Transformer for Robust Point Cloud Restoration |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://openaccess.thecvf.com/content/CVPR2026/html/Wu_PQDT_Pseudo-Query_Dual_Transformer_for_Robust_Point_Cloud_Restoration_CVPR_2026_paper.html) · [Code](https://github.com/ins-uni-bonn/PQDT) |
| Topic | #topic/other_unclear #topic/other_unclear/general |
| Method | PQDT |
| Dataset | ShapeNet-55/34, PFS, ShapeNetCar-Occ |

> [!tip] 效果简介
> - ShapeNet-55/34 上，CD-S 0.34 (优于所有对比方法，达到最优)。
> - PFS 上，CDℓ2 0.16 (比次优方法低76.8%)。
> - ShapeNetCar-Occ 上，CDℓ2 0.82 (平均最优)。

## 概述

点云恢复（补全、去噪、上采样等）是三维视觉的基础任务，现有多数方法依赖**全局瓶颈特征**直接解码形状，或从瓶颈特征生成**种子点/查询**再逐级细化。这两种范式在输入存在噪声、缺失或密度不均时，瓶颈特征极易被污染，导致细粒度几何细节丢失，重建保真度显著下降（Figure 1）。

针对这一瓶颈，本文提出 **PQDT（Pseudo-Query Dual Transformer）**，核心思路是引入**辅助伪查询（pseudo-queries）**作为抗噪声锚点，并将Transformer解码拆分为两个功能互补的阶段：**Stage I 观察引导阶段**从编码输入中生成粗粒度的伪查询，稳定整体几何；**Stage II 先验引导阶段**对伪查询进一步细化，并利用**动态查询选择（DQS）**自适应地平衡输入保真度与学习到的形状先验。此外，PQDT采用**稀疏几何嵌入（SGE）**替代传统坐标位置编码，显式建模点间的距离与角度关系，增强几何感知能力。

在方法谱系上，PQDT属于**基于查询的点云恢复**范式，但区别于 **PoinTr**（Yu et al., CVPR 2021）、**SeedFormer**（Zhou et al., ECCV 2022）、**AnchorFormer**（Qiu et al., CVPR 2023）等从单一全局特征生成查询/锚点的方法，PQDT通过双Transformer架构和两阶段查询生成—细化机制，实现了对退化输入的更强鲁棒性。与扩散模型方法 **SuperPC**（Du et al., CVPR 2025）相比，PQDT以纯点云前馈网络达到更优或相当的性能。

**实验表现突出**：在ShapeNet-55/34基准上，PQDT在所有难度级别（Simple/Moderate/Hard）和所有类别（seen/unseen）上均取得最优的CD-ℓ₂和F1分数（Table 1）；在PFS真实扫描数据集上，CD-ℓ₂相比次优方法降低76.8%，F1-Score提升27.1%（Table 2）。消融实验证实，伪查询与动态查询选择是性能增益的关键来源，几何嵌入进一步带来稳定提升（Table 3）。

**局限与开放问题**：当前方法主要面向物体级点云，向大规模室外场景的迁移有待验证；处理极端稀疏或全新类别时，先验引导可能产生不完全合理的几何。此外，融合RGB等多模态信息能否进一步提升细节恢复和泛化能力，也是值得探索的方向。

## 背景与动机

点云恢复（Point Cloud Restoration）旨在从退化观测中重建完整且几何精确的三维形状，是自动驾驶、机器人感知、数字孪生等领域的核心基础任务。现实中的退化形式多样且高度耦合——激光雷达扫描常同时存在遮挡、噪声、稀疏采样和密度不均等问题，这对恢复方法的鲁棒性提出了严苛要求。

现有方法可大致分为两类范式（Figure 1）。**瓶颈特征方法**（如 **PCN** (Yuan et al., 3DV 2018)、**PoinTr** (Yu et al., CVPR 2021)、**SnowflakeNet** (Xiang et al., ICCV 2021)）将输入点云编码为单一全局特征向量，再从中解码完整形状。这一范式将信息压缩至瓶颈，不可避免地丢失细粒度几何细节，且在输入退化严重时，瓶颈特征本身被噪声污染，导致重建质量急剧下降。**种子/查询方法**（如 **SeedFormer** (Zhou et al., ECCV 2022)、**AnchorFormer** (Qiu et al., CVPR 2023)）从全局特征生成种子点或锚点，再通过粗到细解码恢复形状。尽管这类方法缓解了瓶颈压缩问题，但种子点仍从单一的全局特征中派生，当输入被严重遮挡或噪声干扰时，全局特征失真会直接传导至种子位置，使后续细化缺乏可靠的几何基础。

更深层的瓶颈在于：上述方法缺少一种**抗噪声的中间实体**来桥接退化输入与完整输出之间的几何鸿沟。当输入点云残缺或含噪时，网络要么过度信赖不可靠的观测点，要么过度依赖从数据中学习的形状先验——前者导致重建结果被噪声牵制，后者则可能生成与观测不符的“幻觉”几何。因此，**如何自适应地平衡输入保真度与学习先验**，成为提升点云恢复鲁棒性的关键因果杠杆。

PQDT 的核心洞察是引入**伪查询（Pseudo-Queries）**作为辅助中间实体——它们既是观测的代理，又是先验的载体，通过两阶段的生成与细化过程，在退化输入下为形状重建提供稳定的几何锚点。具体而言，**第一阶段（观察引导）**从编码输入中生成粗略但鲁棒的伪查询，稳定整体结构；**第二阶段（先验引导）**利用学习到的形状先验对伪查询进行细化，恢复细粒度细节。配合动态查询选择（Dynamic Query Selection, DQS）和稀疏几何嵌入（Sparse Geometric Embedding, SGE），PQDT 能够在保留观测可信部分的同时，智能地补充缺失几何，从而在多种退化类型和难度级别下实现一致的高质量恢复。

## 核心创新

PQDT的核心创新在于引入**伪查询（pseudo-queries）** 作为抗噪声的中间锚点，并构建**双Transformer解码架构**，通过两阶段查询生成与动态查询选择（DQS），自适应地平衡输入保真度与学习到的形状先验，从而在各类退化输入下实现鲁棒且几何忠实的高质量点云恢复。

### 从全局瓶颈到伪查询锚点

传统的点云恢复方法通常依赖全局瓶颈特征直接解码形状（如 **PCN**, Yuan et al., 3DV 2018），或从全局特征生成种子点/查询进行由粗到精的解码（如 **PoinTr**, Yu et al., CVPR 2021; **SeedFormer**, Zhou et al., ECCV 2022; **AnchorFormer**, Qiu et al., CVPR 2023）。这些范式的共性瓶颈在于：全局特征在压缩过程中丢失细粒度几何细节，且对输入噪声、缺失和不规则密度高度敏感。当输入严重退化时，从不可靠的全局特征生成的种子查询本身已偏离真实几何，导致后续重建质量急剧下降。

PQDT的核心洞察是：**引入辅助的伪查询实体作为噪声鲁棒的几何锚点**，使其在解码过程中既不完全脱离观测，又能利用学习到的形状先验进行校正。如图1所示，与仅依赖单一瓶颈特征的范式相比，伪查询在双阶段解码中逐步演化，从观测引导的粗略初始化过渡到先验引导的精细细化，最终生成与输入几何高度一致的恢复结果。

### 两阶段查询生成与动态查询选择

PQDT将Transformer解码分解为两个功能互补的阶段（图2）：

**阶段一（观察引导的伪查询生成）**：以静态球形查询 $\mathcal{Q}_{sph}$ 为初始点，通过编码器 $\mathbf{M}_{E_1}$ 对源查询 $\mathcal{Q}_{src}$ 编码，再由解码器 $\mathbf{M}_{D_1}$ 生成观测引导的伪查询 $\mathcal{Q}_{ps}$，并经动态查询选择 $\mathbf{S}_1$ 筛选出代表性查询：

$$\mathcal{Q}_{ps} = \mathbf{S}_1 \big( \mathbf{M}_{D_1} \big( \mathcal{Q}_{sph}, \mathbf{M}_{E_1} \big( \mathcal{Q}_{src} \big) \big), \mathcal{P}_{src}^c \big)$$

这一阶段通过广泛关注编码输入来稳定粗略几何，伪查询作为从观测中提取的几何锚点，天然具有抗噪声能力。

**阶段二（先验引导的查询细化）**：对伪查询 $\mathcal{Q}_{ps}$ 进一步编码，并通过DQS $\mathbf{S}_2$ 与随机采样的输入点 $\mathcal{P}_{src}^f$ 一起筛选，产生最终查询 $\mathcal{Q}$ 和特征 $\mathcal{V}$：

$$\mathcal{V}, \mathcal{Q} = \mathbf{S}_2 \big( \mathbf{M}_{E_2} \big( \mathcal{Q}_{ps} \big), \mathcal{P}_{src}^f \big)$$

细化后的查询通过解码器 $\mathbf{M}_{D_2}$ 预测点代理 $\mathcal{H}$，再经由粗到精的上采样Transformer生成精细点云。

**动态查询选择（DQS）** 是平衡输入保真度与先验的关键机制（图4）。DQS通过带Gumbel噪声的扰动Top-k策略选择最具代表性的查询：

$$s_i = z_i + \beta g_i$$

其中 $z_i$ 为聚合评分，$g_i$ 为Gumbel噪声。该机制确保在查询生成过程中仅保留最具信息量的特征，同时通过随机扰动增强选择多样性，使网络在不同退化程度下都能自适应地决定依赖观测还是先验。

### 稀疏几何嵌入位置编码

与传统方法采用基于原始坐标的绝对或相对位置编码不同，PQDT引入**稀疏几何嵌入（Sparse Geometric Embedding, SGE）**，融合成对距离嵌入和三元角度嵌入来编码点间几何关系：

$$r_{i,j} = \mathbf{r}_{i,j}^D \mathbf{W}^D + \max_{x} \{ \mathbf{r}_{i,j,x}^A \mathbf{W}^A \}$$

为提高效率，几何关系被限制在每个点的k近邻范围内：

$$\mathcal{R}_s = \{ r_{i,j} \mid j \in \mathcal{N}_k(i), i=1,\ldots,M \}$$

在自注意力计算中，SGE将几何键值 $\mathbf{K}_r, \mathbf{V}_r$ 与特征键值 $\mathbf{K}_f, \mathbf{V}_f$ 结合：

$$\mathrm{head} = \mathrm{softmax}\left( \frac{Q(K_f + K_r)^\top}{\sqrt{d_h}} \right)(V_f + V_r)$$

这使得注意力机制能够显式感知点间的几何结构，从而在编码和解码阶段保持更精确的局部几何一致性。

### 关键改变总结

| 改变维度 | 基线方法 | PQDT方案 |
|---------|---------|---------|
| 查询生成策略 | 从全局特征直接生成种子查询或单步解码 | 两阶段伪查询生成（观察引导 + 先验引导）+ 动态查询选择 |
| 位置编码 | 基于原始坐标的绝对/相对位置编码 | 稀疏几何嵌入（距离+角度嵌入，k近邻稀疏化） |
| 种子预测解码 | 从全局特征线性投影生成种子点 | DETR-like解码器，利用几何嵌入自注意力预测种子代理 |

消融实验（Table 3）验证了各创新模块的贡献：在基线模型A（仅使用输入特征直接解码）上增加伪查询与DQS（模型B）使CDℓ2降低0.17、F1提高0.012；进一步采用DETR-like解码器预测种子代理（模型C）继续提升性能；最终用几何嵌入替换原始坐标位置编码的完整PQDT达到最佳CDℓ2 0.818和F1 0.261。

## 整体框架

PQDT 的整体架构围绕“伪查询（pseudo-queries）作为抗噪声锚点”这一核心思想展开，通过双 Transformer 解码与自适应查询选择，在不同退化条件下平衡输入保真度与学习到的形状先验。图 2 展示了完整的 pipeline。

给定一个不完整且含噪声的输入点云 $\mathcal{P}_{src}^f$，网络首先通过 **Transition-Down 模块** 提取多尺度局部特征，并将其降采样为粗点云 $\mathcal{P}_{src}^c$ 及对应特征 $\mathcal{F}_{src}^c$。随后，**几何嵌入编码器（GEE）** 利用稀疏几何嵌入自注意力对 $\mathcal{P}_{src}^c$ 进行编码，得到富含结构信息的特征表示。

整个序列转换过程被拆解为两个功能互补的阶段：

**阶段 I：观察引导的伪查询生成。** 以一组静态球形查询 $\mathcal{Q}_{sph}$ 作为初始点，与编码后的源查询一同送入解码器 $\mathbf{M}_{D_1}$，生成观测引导的伪查询 $\mathcal{Q}_{ps}$。这一步骤可形式化为：

$$\mathcal{Q}_{ps} = \mathbf{S}_1 \big( \mathbf{M}_{D_1} \big( \mathcal{Q}_{sph}, \mathbf{M}_{E_1} \big( \mathcal{Q}_{src} \big) \big), \mathcal{P}_{src}^c \big)$$

其中 $\mathbf{M}_{E_1}$ 为阶段 I 的编码器，$\mathbf{S}_1$ 为动态查询选择（DQS）模块。阶段 I 的核心作用是通过对编码输入的广泛注意力，稳定地捕获粗略几何结构，为后续细化提供抗噪声的初始化。

**阶段 II：先验引导的查询细化与代理预测。** 伪查询 $\mathcal{Q}_{ps}$ 首先经过编码器 $\mathbf{M}_{E_2}$ 进一步编码，随后与随机采样的输入点 $\mathcal{P}_{src}^f$ 一起通过 DQS 模块 $\mathbf{S}_2$ 进行筛选，得到最终查询 $\mathcal{Q}$ 及其特征 $\mathcal{V}$：

$$\mathcal{V}, \mathcal{Q} = \mathbf{S}_2 \big( \mathbf{M}_{E_2} \big( \mathcal{Q}_{ps} \big), \mathcal{P}_{src}^f \big)$$

解码器 $\mathbf{M}_{D_2}$ 从查询 $\mathcal{Q}$ 和特征 $\mathcal{V}$ 预测点代理 $\mathcal{H}$：

$$\mathcal{H} = \mathbf{M}_{D_2} ( \mathcal{Q}, \mathcal{V} )$$

阶段 II 利用学习到的形状先验对伪查询进行细化，使最终查询在几何上更忠实于底层表面。

**动态查询选择（DQS）** 贯穿两个阶段，其设计目标是筛选最具代表性的查询点。DQS 通过 Gumbel Top-k 采样策略对查询进行扰动评分，自适应地平衡输入点与预测点，确保网络在输入高度退化时仍能保留关键几何信息。

**由粗到精的上采样。** 代理 $\mathcal{H}$ 被送入 **Coarse-to-Fine Upsample Transformer**，通过层级式上采样逐步生成精细点云。整个网络以多级重建损失 $\mathcal{L}_{rec}$ 和伪查询损失 $\mathcal{L}_{pq}$ 联合优化，其中 $\mathcal{L}_{rec}$ 在各上采样层级上计算预测点与 FPS 采样真值之间的 CD$_{\ell 1}$ 距离。

整体而言，PQDT 通过“伪查询生成—动态选择—先验细化—代理预测—层级上采样”的级联设计，实现了从退化输入到高质量几何的鲁棒映射。

### 补充图表

![[assets/figures/papers/paper_list_l2264_https_openaccess_thecvf_com_content_CVPR2026_html_Wu_PQDT_Pseudo_Query_D/figures/002_Figure_2.jpg]]
*Figure 2: Overview of PQDT. Given an incomplete and noisy input point cloud, local features are extracted via a transition-down module and translated by a dual transformer. Stage I generates pseudo-queries*

![[assets/figures/papers/paper_list_l2264_https_openaccess_thecvf_com_content_CVPR2026_html_Wu_PQDT_Pseudo_Query_D/figures/001_Figure_1.jpg]]
*Figure 1: Comparison of point cloud restoration paradigms. (a) Bottleneck feature–based methods directly decode the shape from a global latent code. (b) Seed-/query-based methods generate anchors or queries from the global feature for coarse-to-fine decoding. (c) Our PQDT introduces geometry-aware pseudo-queries as auxiliary entities and dual transformer decoding, achieving more faithful restorations with superior geometric fidelity*

## 核心模块与公式推导

### 3.1 双阶段伪查询生成与细化

PQDT 的核心创新在于引入**伪查询（pseudo-queries）** 作为辅助中间实体，将点云恢复的序列转换分解为两个功能互补的阶段。伪查询充当抗噪声锚点，使网络在退化输入下仍能稳定恢复几何结构。

**阶段一：观测引导的伪查询生成。** 以静态球形查询 $\mathcal{Q}_{sph}$ 为初始点，首先对源查询 $\mathcal{Q}_{src}$ 进行编码，再通过解码器 $\mathbf{M}_{D_1}$ 和动态查询选择 $\mathbf{S}_1$ 生成伪查询 $\mathcal{Q}_{ps}$：

$$
\mathcal{Q}_{ps} = \mathbf{S}_1 \big( \mathbf{M}_{D_1} \big( \mathcal{Q}_{sph}, \mathbf{M}_{E_1} \big( \mathcal{Q}_{src} \big) \big), \mathcal{P}_{src}^c \big) \tag{1}
$$

其中 $\mathcal{P}_{src}^c$ 为输入粗点云坐标。该阶段通过广泛关注编码输入，为后续细化提供观测引导的查询初始化，稳定粗略几何。

**阶段二：先验引导的查询细化。** 对阶段一生成的伪查询 $\mathcal{Q}_{ps}$ 进行二次编码，再通过动态查询选择 $\mathbf{S}_2$ 与随机采样的输入点 $\mathcal{P}_{src}^f$ 联合筛选，得到最终查询 $\mathcal{Q}$ 及其特征 $\mathcal{V}$：

$$
\mathcal{V}, \mathcal{Q} = \mathbf{S}_2 \big( \mathbf{M}_{E_2} \big( \mathcal{Q}_{ps} \big), \mathcal{P}_{src}^f \big) \tag{2}
$$

**代理预测。** 解码器 $\mathbf{M}_{D_2}$ 从细化后的查询和特征预测点代理 $\mathcal{H}$，作为后续上采样的种子：

$$
\mathcal{H} = \mathbf{M}_{D_2} ( \mathcal{Q}, \mathcal{V} ) \tag{3}
$$

两阶段设计使网络能够自适应平衡输入保真度与学习到的形状先验，在不同退化条件下均能恢复高质量几何。

### 3.2 稀疏几何嵌入（Sparse Geometric Embedding, SGE）

为增强 Transformer 对三维几何的感知能力，PQDT 提出稀疏几何嵌入替代传统坐标位置编码。几何嵌入由成对距离嵌入和三元角度嵌入组合而成：

$$
r_{i,j} = \mathbf{r}_{i,j}^D \mathbf{W}^D + \max_{x} \{ \mathbf{r}_{i,j,x}^A \mathbf{W}^A \} \tag{5}
$$

其中 $\mathbf{r}_{i,j}^D$ 为点 $i$ 与 $j$ 间的距离嵌入，$\mathbf{r}_{i,j,x}^A$ 为包含第三个点 $x$ 的三元角度嵌入。

为提高效率，几何关系被限制在每个点的 $k$ 近邻内：

$$
\mathcal{R}_s = \{ r_{i,j} \mid j \in \mathcal{N}_k(i), i=1,\ldots,M \} \tag{6}
$$

在自注意力计算中，SGE 注意力头将特征键值 $K_f, V_f$ 与几何键值 $K_r, V_r$ 融合：

$$
\mathrm{head} = \mathrm{softmax}\left( \frac{Q(K_f + K_r)^\top}{\sqrt{d_h}} \right)(V_f + V_r) \tag{7}
$$

该设计使注意力机制同时感知语义特征和局部几何结构，显著提升对点云空间关系的建模能力。

### 3.3 动态查询选择（Dynamic Query Selection, DQS）

DQS 模块确保在查询生成与细化过程中仅保留最具代表性的点。给定输入坐标 $\mathcal{P}_{in}$ 和特征 $\mathcal{X}_{in}$，模块首先将点集扩展至固定大小（通过填充点 $\mathcal{P}_{pad}$ 和零填充特征 $\mathcal{X}_{pad}$），然后采用 Gumbel Top-$k$ 采样策略进行选择：

$$
s_i = z_i + \beta g_i \tag{8}
$$

其中 $z_i$ 为点 $i$ 的聚合评分，$g_i$ 为 Gumbel 噪声，$\beta$ 控制噪声强度。通过扰动评分选择 Top-$k$ 点作为输出查询，DQS 在保持可微性的同时实现了鲁棒的查询筛选。

### 3.4 多级重建损失

训练采用由粗到细的多级监督策略。重建损失定义为各级上采样点云 $\mathcal{P}_i^{\uparrow}$ 与经 FPS 采样的真值 $\mathcal{G}$ 之间的 CD$_{\ell 1}$ 距离之和：

$$
\mathcal{L}_{rec} = \sum_{i=1}^{L} \mathbf{CD}_{\ell 1}(\mathcal{P}_i^{\uparrow}, \mathrm{FPS}(\mathcal{G}, |\mathcal{P}_i^{\uparrow}|)) \tag{11}
$$

此外，伪查询损失 $\mathcal{L}_{pq}$ 以 CD$_{\ell 1}$ 约束伪查询点 $\mathcal{P}_{pq}$ 逼近 FPS 采样的真值，总损失为：

$$
\mathcal{L} = \mathcal{L}_{rec} + \mathcal{L}_{pq} \tag{13}
$$

多级监督确保从粗代理到精细输出的每一级均与真值几何对齐，是 PQDT 实现高几何保真度的重要保障。

### 补充图表

![[assets/figures/papers/paper_list_l2264_https_openaccess_thecvf_com_content_CVPR2026_html_Wu_PQDT_Pseudo_Query_D/figures/003_Figure_3.jpg]]
*Figure 3: Geometric-embedding self-attention block. Geometric attention head uses distance embedding (DE) and angular embedding (AE) from input point coordinates and regrouped as attention keys*

![[assets/figures/papers/paper_list_l2264_https_openaccess_thecvf_com_content_CVPR2026_html_Wu_PQDT_Pseudo_Query_D/figures/004_Figure_4.jpg]]
*Figure 4: Dynamic Query Selection (DQS) module. Given the input coordinates*

## 实验与分析

### 主实验结果

PQDT在多个基准数据集上全面超越现有方法，验证了伪查询双Transformer架构在不同退化条件下的鲁棒性。

**ShapeNet-55/34点云补全。** 在包含55个类别（34个可见类、21个不可见类）的ShapeNet标准补全基准上，PQDT在所有难度级别（Simple/Moderate/Hard）和所有类别划分上均达到最优。如表1所示，在全部55个类别上，PQDT取得CD-S 0.34、CD-M 0.55、CD-H 1.13，平均CDℓ2 0.68，F-Score@1% 0.570。在不可见类别上，PQDT同样保持领先，CDℓ2较次优方法显著降低，证明其泛化能力不依赖类别特定先验。相比基于全局瓶颈特征的方法（如**PCN**, Yuan et al., 3DV 2018）和基于种子点的方法（如**SeedFormer**, Zhou et al., ECCV 2022；**AnchorFormer**, Qiu et al., CVPR 2023），PQDT在Hard设置下优势尤为突出，表明两阶段查询生成与动态查询选择机制有效缓解了严重退化下的几何丢失问题。

**多任务泛化。** 在ShapeNet-Deform、ShapeNetCar-Occ和PFS三个数据集上，PQDT同样取得最优结果（表2）。在包含遮挡和变形的ShapeNet-Deform上，PQDT的CDℓ2降至1.01，F1达到0.29；在ShapeNetCar-Occ上CDℓ2为0.82；在极具挑战的PFS真实扫描数据集上，CDℓ2仅0.16，相比次优方法降低76.8%，F1提升27.1%。PFS上的大幅领先表明，伪查询作为抗噪声锚点的设计在真实传感器噪声和稀疏采样下尤为有效。

**定性分析。** 可视化结果（图6）显示，PQDT重建的点云在几何细节和结构完整性上均优于对比方法。在ShapeNet-Deform的变形输入上，PQDT能恢复出更完整的薄壁结构；在ShapeNetCar-Occ的遮挡场景中，PQDT对被遮挡区域的推断更符合真实几何，而基线方法常产生塌陷或模糊的重建。

### 消融实验

为验证各组件的贡献，作者在ShapeNetCar-Occ上进行了系统消融（表3）。

**伪查询与动态查询选择。** 基线模型A仅使用输入特征直接解码，不引入伪查询机制。增加伪查询生成与动态查询选择（模型B）使CDℓ2降低0.17，F1提高0.012，证实辅助查询实体和自适应选择策略对提升重建质量的关键作用。动态查询选择通过扰动Top-k策略（公式8-9）平衡输入保真度与预测点，避免噪声点污染查询表示。

**种子预测解码器。** 在模型B基础上，将种子点预测替换为基于DETR-like解码器的几何嵌入自注意力解码（GED，模型C），性能进一步提升。这表明利用自注意力机制从伪查询特征中解码种子代理，比直接从全局特征线性投影生成种子点更能保留局部几何结构。

**稀疏几何嵌入。** 最终完整PQDT将原始坐标位置编码替换为稀疏几何嵌入（SGE），融合成对距离嵌入和三元角度嵌入（公式5-7），达到最优CDℓ2 0.818和F1 0.261。SGE通过k近邻稀疏化（公式6）控制计算开销，同时为注意力机制提供丰富的几何先验，使查询能更准确地定位到物体表面。

**损失函数贡献。** 伪查询损失（公式12）直接监督Stage I生成的伪查询点坐标，强制其分布在物体表面附近，为Stage II细化提供良好的初始化。消融中移除该损失会导致收敛变慢和最终精度下降。

### 注意力可视化分析

图8展示了Stage I和Stage II解码器最后一层的注意力图。Stage I的注意力呈现粗粒度的全局探索模式，伪查询在编码的潜在结构上广泛搜索，稳定粗略几何。Stage II的注意力则高度局部化和连贯，查询聚焦于底层表面邻近区域，表明查询细化阶段有效利用了先验信息将注意力收束到真实几何流形上。这一可视化直观验证了双阶段设计的互补性：观察引导阶段提供鲁棒初始化，先验引导阶段实现精细几何对齐。

### 失败模式与局限性

尽管PQDT在物体级点云恢复上表现优异，仍存在以下局限：

1. **极端稀疏输入。** 当输入点数极少（如小于100点）时，过渡降采样模块提取的局部特征信息不足，导致Stage I生成的伪查询偏离真实表面，后续细化难以完全纠正。此时重建结果可能出现拓扑错误或缺失部件。

2. **全新类别泛化。** 在ShapeNet-55的不可见类别上，PQDT虽优于对比方法，但绝对精度仍低于可见类别。这表明学习的形状先验对训练分布外的新颖几何结构存在偏差，可能产生不完全合理的重建。

3. **大规模场景扩展。** 当前设计面向物体级点云，伪查询数量固定，动态查询选择的Top-k策略依赖预设的查询数目。直接应用于大规模室外场景需要解决查询数量自适应和计算效率问题，有待进一步探索。

### 公平性说明

所有对比方法均使用官方发布或原作者推荐的代码和配置，在相同数据集划分和评估协议下进行评测。ShapeNet-55/34采用标准的三难度划分（Simple/Moderate/Hard），PFS和ShapeNetCar-Occ遵循各自数据集的官方评估协议。指标计算统一使用CDℓ2（乘以1000）和F-Score@1%（PFS额外报告F-Score@0.5%）。

### 补充图表

![[assets/figures/papers/paper_list_l2264_https_openaccess_thecvf_com_content_CVPR2026_html_Wu_PQDT_Pseudo_Query_D/figures/005_Table_1.jpg]]
*Table 1: Results of our method and state-of-the-art methods on ShapeNet-55/34. We report the results of all 55 categories, 34 seen categories and 21 unseen categories in three difficulty degrees. We use CD-S, CD-M and CD-H to represent the*

![[assets/figures/papers/paper_list_l2264_https_openaccess_thecvf_com_content_CVPR2026_html_Wu_PQDT_Pseudo_Query_D/figures/008_Table_2.jpg]]
*Table 2: Results of our method and state-of-the-art methods on ShapeNet-Deform, ShapeNetCar-Occ and PFS dataset. We report the CDℓ2 (multiplied by 1000) under three difficulty setups of ShapeNet-Deform, and the average CDℓ2 and F-Score@1% of all three datasets. Additional F-Score@0.5% are reported for PFS dataset*

![[assets/figures/papers/paper_list_l2264_https_openaccess_thecvf_com_content_CVPR2026_html_Wu_PQDT_Pseudo_Query_D/figures/010_Table_3.jpg]]
*Table 3: Ablation study on ShapeNetCar-Occ. We report the results with different model designs including query generation (Query), seed prediction (Seed) and positional encoding (PE)*

![[assets/figures/papers/paper_list_l2264_https_openaccess_thecvf_com_content_CVPR2026_html_Wu_PQDT_Pseudo_Query_D/figures/007_Figure_6.jpg]]
*Figure 6: Qualitative evaluation on ShapeNet-Deform and ShapeNetCar-Occ. Red boxes indicate occluding objects*

![[assets/figures/papers/paper_list_l2264_https_openaccess_thecvf_com_content_CVPR2026_html_Wu_PQDT_Pseudo_Query_D/figures/009_Figure_7.jpg]]
*Figure 7: Qualitative evaluation on PFS. The color represent the Point-to-Surface distance (P2S) between generated point clouds and ground truth mesh, the maximum (red) is clamped with 2% of the radius of the object’s bounding sphere*

![[assets/figures/papers/paper_list_l2264_https_openaccess_thecvf_com_content_CVPR2026_html_Wu_PQDT_Pseudo_Query_D/figures/011_Figure_8.jpg]]
*Figure 8: Attention maps from selected queries (red dot) visualized on key points (bottom row). Stage I attention maps show coarse pseudo-query exploration over the encoded latent structure. Stage II maps demonstrate localized, coherent attention aligned with the underlying surface, indicating effective query refinement. The color reflects the attention score after the Softmax operation in the last block of the decoder*

## 方法谱系与知识库定位

### 一、与基线方法的关系

PQDT 处于点云恢复（Point Cloud Restoration）的统一框架下，该框架涵盖补全、去噪、超分辨率等多种退化修复任务。现有主流范式可归为两条技术路线：

**（1）瓶颈特征解码范式。** 以 **PCN**（Yuan et al., 3DV 2018）为代表的早期工作将输入点云编码为单一全局特征向量，再通过全连接层直接解码完整形状。这类方法的信息压缩过于激进，在严重缺失或高噪声场景下会丢失大量局部几何细节，重建结果往往呈现过度平滑或拓扑错误。

**（2）种子/查询驱动范式。** 为缓解瓶颈压缩问题，**PoinTr**（Yu et al., CVPR 2021）引入 Transformer 架构，将点云补全建模为序列到序列的翻译任务；**SeedFormer**（Zhou et al., ECCV 2022）和 **AnchorFormer**（Qiu et al., CVPR 2023）则从全局特征生成种子点或锚点，再通过上采样逐步细化。然而，这些方法的种子/查询仍然源于全局特征的单步投影，当输入退化严重时，初始种子本身已携带噪声偏差，后续细化难以完全纠正。**AdaPoinTr**（Yu et al., TPAMI 2023）尝试通过去噪代理增强鲁棒性，但其查询生成机制本质上仍依赖单阶段解码。

**PQDT 的根本性改进在于将查询生成解耦为两个功能互补的阶段。** 第一阶段（观察引导）从球形初始查询出发，通过交叉注意力广泛聚合编码输入特征，生成初步的“伪查询”（pseudo-queries）——这些伪查询作为抗噪声锚点，捕获了输入的粗略几何结构；第二阶段（先验引导）对伪查询进行再编码与动态查询选择（Dynamic Query Selection, DQS），仅保留最具代表性的查询，并利用学习到的形状先验进行细化。这种设计使得网络能够自适应地平衡输入保真度与先验知识，在不同退化程度下均能保持几何忠实度。

此外，与 **SnowflakeNet**（Xiang et al., ICCV 2021）的层级式细化不同，PQDT 的细化发生在查询层面而非点云层面；与 **SuperPC**（Du et al., CVPR 2025）的扩散模型路线不同，PQDT 采用确定性 Transformer 架构，避免了迭代采样的计算开销。

### 二、适用边界

根据论文的实验设置和方法设计，PQDT 的当前适用边界如下：

- **任务范围：** 覆盖点云补全（ShapeNet-55/34、ShapeNet-Deform、ShapeNetCar-Occ）、点云去噪与超分辨率（PFS 数据集），在统一框架下处理多种退化类型。
- **数据规模：** 物体级点云（单物体 2048–16384 点），输入可为部分缺失、含噪声或密度不均的点云。
- **类别泛化：** 在 ShapeNet-55 的 21 个未见类别（unseen categories）上同样取得最优结果，表明方法具备一定的开集泛化能力。

**明确不适用或待验证的场景包括：**
- **大规模室外场景**（如 KITTI、SemanticKITTI），论文未进行实验，其稀疏几何嵌入的 k 近邻策略在远距离稀疏点上的有效性尚待检验。
- **极端稀疏输入**（如仅数十个点），伪查询的初始化与选择机制可能因观测信息过少而退化。
- **实时应用**：双阶段 Transformer 解码的推理延迟未被系统报告，需手动验证其是否满足实时性要求。

### 三、局限与开放问题

论文自身指出的局限及可进一步探索的方向：

**已明确的局限：**
1. 方法主要面向物体级点云修复，对大规模室外场景的扩展有待探索。室外场景的点密度变化剧烈、遮挡模式复杂，双阶段查询选择策略能否保持效率与鲁棒性仍需验证。
2. 在处理极端稀疏或全新类别时，第二阶段可能过度依赖学习到的形状先验，产生几何上合理但与观测不一致的重建结果。

**开放问题：**
1. **大规模场景迁移：** 如何将双阶段伪查询设计有效迁移至户外点云恢复，同时保持计算效率？可能需要引入层次化查询或稀疏窗口注意力机制。
2. **多模态融合：** 融合 RGB 图像等多模态信息是否能进一步提升细节恢复和跨域泛化能力？伪查询框架天然支持多源特征的交叉注意力聚合，这一方向值得探索。
3. **查询数量自适应：** 当前 DQS 模块依赖固定的 Top-k 选择数量，能否根据输入退化程度动态调整查询规模，以在简单场景下降低计算冗余？
4. **理论分析：** 伪查询作为抗噪声锚点的理论性质（如对输入扰动的 Lipschitz 连续性）尚未被形式化分析，这可能是理解其鲁棒性来源的关键。

## 原文 PDF

![[paperPDFs/CVPR_2026/PQDT_Pseudo_Query_Dual_Transformer_for_Robust_Point_Cloud_Restoration.pdf]]
