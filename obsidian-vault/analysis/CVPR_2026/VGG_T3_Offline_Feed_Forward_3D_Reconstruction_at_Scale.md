---
title: "VGG-T3: Offline Feed-Forward 3D Reconstruction at Scale"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/VGG_T3_Offline_Feed_Forward_3D_Reconstruction_at_Scale.pdf
project_link: https://research.nvidia.com/labs/dvl/projects/vgg-ttt/
aliases:
- VTVGGTTT
- VGG-T3
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
core_operator: "通过测试时训练（TTT）将可变的KV空间表示蒸馏为一个固定尺寸的MLP，从而替换二次复杂度的全局注意力操作。"
primary_logic: "在测试时，利用自监督目标优化一个轻量MLP来压缩键-值映射，将推理复杂度从O(n^2)降至O(n)；同时保留预训练的编码器/解码器，通过线性化的KV查询实现大规模前馈重建。"
claims:
- "VGG-T3重建1k图像集合仅需54秒，相比基于softmax注意力的基线方法加速11.6倍。"
- "在点图估计任务上，VGG-T3显著优于其他线性时间基线（如TTT3R），在DTU、ETH3D和NRGBD-D上误差降低2-2.5倍。"
- "通过增加测试时训练的优化器步数，VGG-T3在任意图像数量下保持近乎恒定的扩展性。"
- "VGG-T3支持分布式推理，在4个GPU上处理2k图像仅需48.5秒，相较VGGT的27分钟提升33倍。"
---

# VGG-T3: Offline Feed-Forward 3D Reconstruction at Scale

> [!tip] 核心洞察
> 在测试时，利用自监督目标优化一个轻量MLP来压缩键-值映射，将推理复杂度从O(n^2)降至O(n)；同时保留预训练的编码器/解码器，通过线性化的KV查询实现大规模前馈重建。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | VGG-T3: 大规模离线前馈3D重建 |
| 英文题名 | VGG-T3: Offline Feed-Forward 3D Reconstruction at Scale |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2602.23361); [Project](https://research.nvidia.com/labs/dvl/projects/vgg-ttt/) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction |
| Method | VGG-T3 (Visual Geometry Grounded Test Time Training) |
| Dataset | DTU (Pointmap Estimation, Dense), NRGBD-D (Pointmap Estimation, ETH3D (Pointmap Estimation), KITTI (Video Depth) |

> [!tip] 效果简介
> - DTU (Pointmap Estimation, Dense) 上，Chamfer Distance ↓ 为 1.654，对比 5.708 (TTT3R)，变化 -4.054 (3.45× better)。
> - NRGBD-D (Pointmap Estimation, Dense) 上，Chamfer Distance ↓ 为 0.029，对比 0.071 (TTT3R)，变化 -0.042 (2.45× better)。
> - ETH3D (Pointmap Estimation) 上，Chamfer Distance ↓ 为 0.480，对比 0.885 (TTT3R)，变化 -0.405 (1.84× better)。

## 概述

### 1. 问题瓶颈

前馈多视图3D重建模型（如 **VGGT**，Wang et al., CVPR 2025）通过全局自注意力层在不同视图间交换信息，其场景表征依赖于可变长度的键值（KV）对序列。这一设计的根本瓶颈在于：**计算与内存需求随输入图像数量呈二次增长（O(n²)）**，导致模型无法处理大规模图像集合——当图像数量达到数百至上千时，全量KV加载到GPU内存极易引发显存溢出（OOM），推理时间亦急剧膨胀至分钟乃至小时级别。

### 2. 核心方法：VGG-T3

**VGG-T3**（Visual Geometry Grounded Test Time Training）提出了一种线性复杂度的替代方案：

- **核心洞察**：在测试时，利用自监督目标优化一个轻量MLP，将可变的KV空间表示**压缩为固定尺寸MLP的权重**，从而将推理复杂度从O(n²)降至O(n)。
- **因果机制**：通过测试时训练（TTT），以键（Key）为输入、值（Value）为监督信号优化MLP；查询时仅需将查询向量（Query）送入训练好的MLP即可获得输出，完全规避了softmax注意力的二次计算。
- **保留预训练权重**：VGG-T3在预训练的VGGT权重基础上进行线性化，而非从头训练；同时移除LayerNorm并改用L2归一化，以解锁预训练权重的快速收敛。

### 3. 方法谱系与知识库定位

| 方法 | 复杂度 | 核心机制 | 定位 |
|------|--------|----------|------|
| **VGGT**（Wang et al., CVPR 2025） | O(n²) | 全局softmax注意力 | 离线前馈重建的精度上界 |
| **FastVGGT**（Shen et al., arXiv 2025） | O(n²) | Token合并加速 | VGGT的工程加速变体 |
| **SparseVGGT**（Wang et al., arXiv 2025） | O(n²) | 块稀疏注意力 | VGGT的稀疏化变体 |
| **TTT3R** | O(n) | 固定尺寸记忆的在线TTT | 面向有序序列的线性时间基线 |
| **VGG-T3**（本文） | O(n) | TTT压缩KV空间为MLP权重 | 离线前馈、线性扩展的统一方案 |

VGG-T3在方法谱系中占据独特位置：它既保留了VGGT的离线前馈特性（一次性处理所有视图），又通过TTT实现了线性复杂度，同时支持有序和无序输入序列——这是TTT3R所不具备的能力。

### 4. 主要结论

**（1）大规模重建的显著加速**

VGG-T3在1k图像集合上的重建仅需**54秒**，相较基于softmax注意力的VGGT加速**11.6倍**（Figure 4）。在分布式推理场景下，4个GPU处理2k图像仅需**48.5秒**，相较VGGT的27分钟提升**33倍**（Table 4）。

**（2）点图估计精度大幅领先线性基线**

在DTU、ETH3D和NRGBD-D三个基准上，VGG-T3的点图估计误差相较TTT3R降低**2–2.5倍**（Table 1），同时与O(n²)的softmax基线保持竞争力。

**（3）近乎恒定的扩展性**

通过增加测试时训练的优化器步数，VGG-T3在任意图像数量下保持近乎恒定的扩展性（Figure 3a），解决了固定优化步数下误差随图像数量线性增长的问题。

**（4）统一的建图与定位**

VGG-T3使用同一MLP表示进行场景建图（优化MLP）和新图像定位（查询冻结MLP），在视觉定位任务上显著优于TTT3R（Table 5），并支持跨时间的真实场景定位（Figure 8）。

### 5. 已知局限

- **精度间隙**：线性注意力在空间范围更大或场景布局更复杂时，重建质量可能下降，无法完全匹配softmax注意力精度（Figure 9b）。
- **位姿估计薄弱**：在相机位姿估计任务上表现不佳，推测源于VGGT中特殊的相机token结构与TTT MLP的交互困难（Sec. 4.1）。
- **表示容量上限**：固定尺寸MLP的表示能力可能有上限，在极大规模场景或宽基线条件下可能导致信息丢失。

## 背景与动机

### 前馈3D重建的规模化困境

从多视图图像中恢复场景的3D几何、相机位姿与内参，是计算机视觉的基础任务。近年来，前馈（feed-forward）方法因其无需逐场景优化的高效性而备受关注。其中，基于Transformer架构的模型（如**VGGT**，Wang et al., CVPR 2025）通过全局自注意力机制在token空间中聚合跨视图信息，在点图估计、深度预测和相机位姿估计上取得了领先精度。

然而，这类模型的**核心瓶颈**在于其场景表征方式：全局自注意力层维护一个**可变长度的键值（Key-Value, KV）空间**作为场景几何的隐式表示。当输入图像数量为 $n$ 时，softmax注意力的计算复杂度为 $O(n^2)$，内存占用同样随 $n$ 二次增长。这导致两个严重后果：

1. **推理延迟爆炸**：对于包含数百至上千张图像的大规模场景，VGGT的推理时间可达数十分钟（如1k图像约需11分钟），难以满足实际应用需求。
2. **内存溢出风险**：全量KV空间必须加载到GPU内存中，当图像数量超出硬件容量时，推理直接失败。

尽管后续工作尝试通过token合并（**FastVGGT**，Shen et al., arXiv 2025）或块稀疏注意力（**SparseVGGT**，Wang et al., arXiv 2025）来缓解这一问题，但这些方法本质上仍是 $O(n^2)$ 复杂度，并未从根本上突破规模化障碍。

### 线性时间方法的局限

在 $O(n)$ 复杂度的方法中，**TTT3R** 率先将测试时训练（Test-Time Training, TTT）引入3D重建，通过固定尺寸的记忆模块实现线性时间推理。然而，TTT3R的设计面向**有序序列**处理，在无序图像集合上表现不佳，且其重建精度与 $O(n^2)$ 基线之间存在显著差距——在DTU、ETH3D和NRGBD-D基准上，TTT3R的点图估计误差约为VGGT的2-5倍（Table 1）。

### 核心动机：以线性复杂度逼近二次注意力精度

上述困境揭示了一个关键矛盾：**全局注意力带来的跨视图信息聚合能力是精度的保障，但其二次复杂度又恰恰是规模化的障碍**。本文的核心动机正是破解这一矛盾——能否在保持全局信息聚合能力的同时，将复杂度降至线性？

直观思路是：既然KV空间本质上是对场景几何的隐式编码，那么能否用一个**固定尺寸的紧凑表示**来替代可变长度的KV序列？如果能将KV空间“蒸馏”为一个轻量MLP的权重，那么对场景的查询就退化为对MLP的前向传播，复杂度自然降至 $O(n)$。

这一思路的关键挑战在于：如何在保留预训练模型知识的前提下，实现从softmax注意力到MLP查询的有效转换，使得线性化后的模型既能继承预训练权重的表达能力，又能在任意规模的图像集合上稳定泛化。

## 核心创新

### 瓶颈诊断：可变长度KV空间引发的二次复杂度

VGG-T3的核心创新源于对前馈多视图重建模型**VGGT**（Wang et al., CVPR 2025）计算瓶颈的精确诊断。VGGT采用交替注意力架构，在图像内自注意力之后插入全局自注意力层，以跨视图汇聚信息。该全局注意力层将场景几何表示为**可变长度的键值对序列**（KV空间），其标准softmax注意力计算复杂度随输入图像数量 $n$ 呈 $O(n^2)$ 增长。当输入图像集合扩展至数百乃至上千张时，这一设计导致两个致命后果：

- **内存爆炸**：全量KV需加载至GPU显存，极易触发OOM（Out of Memory）；
- **推理时间不可接受**：VGGT处理1000张图像需约11分钟，2000张图像需约27分钟，无法满足大规模场景重建的实时需求。

这一瓶颈的本质在于：softmax注意力要求每个查询token与所有键token进行两两交互，计算量与存储量均随序列长度平方增长。

### 因果开关：测试时训练压缩KV空间为固定尺寸MLP

VGG-T3的解决方案是引入**测试时训练**（Test-Time Training, TTT）作为因果开关，将可变的KV空间表示**蒸馏**为一个固定尺寸的多层感知机（MLP）。具体而言：

1. **压缩阶段（Update）**：在测试时，利用自监督目标优化一个轻量MLP $T_\theta$，使其学习从键 $k_i$ 到值 $v_i$ 的映射：
   $$\underset{\theta}{\operatorname{argmin}} \sum_i L_t \big( \mathrm{T}_\theta(k_i) - v_i \big)$$
   该目标将整个KV空间的信息压缩至MLP的固定权重 $\theta$ 中，权重尺寸与输入图像数量无关。

2. **查询阶段（Apply）**：优化完成后，对任意查询token $q_i$，输出直接由MLP前向传播获得：
   $$o_i = \mathrm{T}_\theta(q_i)$$
   该操作复杂度为 $O(n)$，彻底消除了全局注意力中的二次项。

### 核心洞察：保留预训练权重，线性化全局交互

VGG-T3的关键洞察在于**不从头训练**，而是对预训练的softmax注意力模型进行线性化改造。消融实验揭示：若从随机初始化直接训练TTT线性化模型，优化过程会陷入局部最优，点图Chamfer距离从0.066恶化至0.262（Table 6）。因此，VGG-T3保留了VGGT预训练的编码器/解码器权重，仅将全局注意力层替换为TTT线性层，使预训练知识通过线性化的KV查询得以延续。

### 关键设计变更（Changed Slots）

| 组件 | 基线（VGGT） | VGG-T3 | 作用 |
|------|-------------|--------|------|
| **全局注意力操作** | Softmax attention ($O(n^2)$) | TTT MLP查询 ($O(n)$) | 消除二次复杂度，实现线性扩展 |
| **KV空间表示** | 可变长度键值对序列 | 固定尺寸MLP权重 | 内存占用与输入规模解耦 |
| **归一化方式** | LayerNorm (LN) | L2归一化 | 移除LN以解锁预训练权重的快速收敛，避免TTT目标陷入收敛缓慢的窘境 |
| **值空间混合** | 无额外混合（仅线性投影） | ShortConv2D（3×3卷积） | 在值空间进行局部空间混合，打破K-V线性依赖，增强TTT目标的表达力 |
| **推理规模限制** | 需全量KV加载至GPU，易OOM | Minibatch梯度累积，支持单GPU处理任意大集合；多GPU分布式推理 | 梯度可分解为各token梯度之和，天然支持数据并行 |

### ShortConv2D：打破K-V线性依赖

标准TTT框架学习的是从键到值的点对点映射，缺乏对值空间局部结构的建模能力。VGG-T3在值投影后引入**ShortConv2D**——一个3×3卷积层，在值的空间维度上进行局部混合。这一设计的动机在于：相邻像素的值向量通常具有空间相关性，卷积操作可打破K-V之间的严格线性依赖，使TTT目标能够捕捉更丰富的几何上下文。消融实验证实，3×3卷积核在值空间效果最佳（CD 0.066, NC 0.838），更大的卷积核或同时对键和值应用卷积反而降低性能（Table 9）。

### 分布式推理的天然优势

VGG-T3的TTT目标具有梯度可加性：
$$\frac{d L_{\mathrm{total}}}{d \theta} = \sum_i \frac{d}{d \theta} L(\mathbf{k}_i, \mathbf{v}_i) = \sum_s \left( \sum_{i \in s} \frac{d}{d \theta} L(\mathbf{k}_i, \mathbf{v}_i) \right)$$
总梯度等于各token局部梯度的和，可按minibatch独立计算后累加。这一性质使VGG-T3可直接使用标准分布式数据并行（DDP），跨GPU通信仅需在MLP权重更新时进行梯度同步，无需像VGGT那样实现复杂的上下文并行（如ring attention）。在4块GPU上处理2000张图像仅需48.5秒，相较VGGT的27分钟提升33倍（Table 4）。

## 整体框架

![[assets/figures/papers/paper_list_l16_https_arxiv_org_abs_2602_23361/figures/001_Figure_1.jpg]]
*Figure 1: Reconstructing Rome landmarks with 1-minute time budget. We present VGG-T3, an offline feed-forward 3D reconstruction method that scales linearly w.r.t. input views (Fig. 1b). As a result, we can reconstruct large scenes from a large number of unposed input views, such as landmarks from tourist-sourced images, in less than a minute via single forward pass (Fig. 1a)*

VGG-T3 的 pipeline 以 VGGT 的交替注意力架构为基础，但在全局注意力层中引入测试时训练（Test-Time Training, TTT）来替换二次复杂度的 softmax 注意力，从而将可变的键值（KV）空间压缩为固定尺寸 MLP 的权重。整个前馈流程由以下模块串联构成：

1. **Image Tokenizer**：将输入的多视图图像集合分割并编码为 token 序列，作为后续 Transformer 层的输入。
2. **Alternating Attention Blocks**：交替执行图像内自注意力和全局注意力。其中全局注意力层是计算瓶颈所在——原始 VGGT 在此处使用缩放点积 softmax 注意力，复杂度为 $O(n^2)$（$n$ 为 token 总数）。
3. **TTT Linear Layer**：在每层全局注意力中，执行两阶段操作：
   - **Update 阶段**：以自监督目标 $\underset{\theta}{\operatorname{argmin}} \sum_i L_t \big( \mathrm{T}_\theta(k_i) - v_i \big)$ 优化一个轻量 MLP $\mathrm{T}_\theta$，将当前层的键 $k_i$ 到值 $v_i$ 的映射压缩进 MLP 的权重中。
   - **Apply 阶段**：用优化后的 MLP 对查询 $q_i$ 进行前馈映射 $o_i = \mathrm{T}_\theta(q_i)$，得到线性复杂度的输出。
4. **ShortConv2D**：在值空间应用 $3\times3$ 卷积进行局部空间混合，打破键与值之间的线性依赖关系，增强 TTT 目标的表达力。
5. **Prediction Heads**：从输出 token 直接解码逐图像的深度图、相机位姿和内参。

**数据流与复杂度变化**：输入图像经 tokenizer 编码后，在交替注意力块中逐层处理。在全局注意力层，原始 VGGT 需计算所有 token 两两之间的注意力权重（$O(n^2)$），而 VGG-T3 将 KV 空间压缩为固定尺寸 MLP 后，查询操作变为对每个 token 独立应用 MLP，复杂度降至 $O(n)$。TTT 优化的总梯度可分解为各 token 局部梯度的和，支持 minibatch 梯度累积和分布式数据并行（DDP），使单 GPU 可处理任意大规模图像集合，多 GPU 下实现近线性加速。

**关键设计选择**：VGG-T3 移除了原始 VGGT 中的 LayerNorm，改用 L2 归一化，以解锁预训练权重的快速收敛（Sec. 3.2）。ShortConv2D 仅在值空间使用 $3\times3$ 卷积效果最佳，更大的卷积核或同时对键和值应用卷积会降低性能（Table 9）。TTT 优化步数需随图像数量增加而调整：对于 20 张图像的分布内样本，1 步优化即足够；对于 1k 张图像，更多步数可显著降低点图误差（Figure 3a）。

## 核心模块与公式推导

### 核心模块

VGG-T3 在 VGGT 的双向 Transformer 架构基础上，将全局自注意力层替换为基于测试时训练（Test-Time Training, TTT）的线性替代方案。整个前向传播由以下关键模块组成：

**1. Image Tokenizer**
将输入图像分割并编码为 token 序列，作为后续注意力层的输入（Fig. 2a, Sec. 3.1）。

**2. Alternating Attention Blocks**
交替执行两种注意力操作：
- **图像内自注意力**：在每个图像内部的 token 之间进行标准注意力计算；
- **全局注意力层**（被 TTT 替换）：原本跨所有输入视图进行信息汇聚，是二次复杂度瓶颈的来源。

**3. TTT Linear Layer**
在每个全局注意力层中，通过测试时训练优化一个固定尺寸的 MLP，将可变长度的键值（KV）空间压缩为 MLP 的权重。该模块的执行分为两个阶段（Fig. 2b）：
- **Update 阶段**：利用当前层产生的键 $k_i$ 和值 $v_i$ 作为训练数据，优化 MLP 权重 $\theta$，将 KV 映射关系蒸馏到 MLP 中；
- **Apply 阶段**：用优化后的 MLP $T_\theta$ 处理查询 $q_i$，输出 $o_i = T_\theta(q_i)$，实现线性复杂度的 KV 查询。

**4. ShortConv2D**
在值空间 $v_i$ 上应用 $3\times3$ 卷积进行局部空间混合，打破键与值之间的线性依赖关系，增强 TTT 优化目标的表达能力（Sec. 3.2, Table 9 消融表明 $3\times3$ 卷积效果最佳）。

**5. Prediction Heads**
从输出 token 直接解码逐图像深度图、相机位姿和内参（Sec. 3.1）。

### 关键公式推导

**标准 QKV 投影与 Softmax 注意力**

输入 token $x_i$ 经线性投影和层归一化生成查询、键、值向量：

$$q_i = \mathrm{LN}_q(W_q x_i), \quad k_i = \mathrm{LN}_k(W_k x_i), \quad v_i = W_v x_i \tag{Eq. 1}$$

标准缩放点积注意力输出为值的加权和，复杂度为 $O(n^2)$：

$$o_i = \sum_j \operatorname{softmax}_j\left(\frac{q_i^T k_j}{\sqrt{d}}\right) v_j \tag{Eq. 2}$$

**TTT 优化目标与查询**

VGG-T3 将注意力操作重新定义为学习一个从键到值的映射网络 $T_\theta$。在 Update 阶段，通过最小化重建损失优化 MLP 权重：

$$\underset{\theta}{\operatorname{argmin}} \sum_i L_t \big( T_\theta(k_i) - v_i \big) \tag{Eq. 3}$$

在 Apply 阶段，用优化后的 MLP 直接将查询映射为输出，复杂度降至 $O(n)$：

$$o_i = T_\theta(q_i) \tag{Eq. 4}$$

**分布式推理的梯度分解**

TTT 损失关于 MLP 权重 $\theta$ 的总梯度可分解为各 token 局部梯度的和：

$$\frac{d L_{\mathrm{total}}}{d \theta} = \sum_i \frac{d}{d \theta} L(\mathbf{k}_i, \mathbf{v}_i) = \sum_s \left( \sum_{i \in s} \frac{d}{d \theta} L(\mathbf{k}_i, \mathbf{v}_i) \right) \tag{Eq. 5}$$

这一性质使得各 minibatch 可独立计算梯度后求和，天然支持单 GPU 的梯度累积卸载和多 GPU 的分布式数据并行（DDP），无需复杂的上下文并行实现（Sec. 3.3）。

**归一化方式的变更**

VGG-T3 移除了标准 Transformer 中的 LayerNorm（LN），改用 L2 归一化。这一设计选择解锁了预训练权重的快速收敛能力，避免 TTT 优化目标在预训练权重基础上收敛缓慢的问题（Sec. 3.2, Table 6 间接支持）。

> **注意**：关于 MLP $T_\theta$ 的具体网络结构（层数、隐藏维度等），原文未在提供的材料中明确给出，需查阅原文附录确认。

## 实验与分析

### 核心实验设计

VGG-T3的实验评估围绕三个核心维度展开：（1）与$O(n)$线性时间基线（TTT3R）和$O(n^2)$二次复杂度基线（VGGT及其加速变体）的精度对比；（2）大规模图像集合下的扩展性验证；（3）关键设计选择的消融分析。所有实验在相同硬件条件下进行，VGGT基线使用了附录中提出的注意力熵缩放（entropy-scaling）以在大规模场景下提供更强的对比基准。

评估基准和指标均遵循先前工作（CUT3R、VGGT）的标准协议。点图估计使用Chamfer Distance（CD↓）和Normal Consistency（NC↑）；深度估计使用$\delta < 1.25$准确率和Abs Rel；位姿估计使用ATE、RPE。测试涵盖DTU、ETH3D、NRGBD-D、KITTI、Sintel、ScanNet、7scenes和Wayspots等多个数据集。

---

### 点图估计：线性时间方法的新SOTA

**Table 1** 展示了点图估计的主结果。VGG-T3在所有基准上显著优于同为$O(n)$复杂度的TTT3R，误差降低2-2.5倍：

![[assets/figures/papers/paper_list_l16_https_arxiv_org_abs_2602_23361/figures/006_Table_1.jpg]]
*Table 1: Pointmap estimation on dense (-D) and sparse (-S) split. Overall, we outperform O ( n ) baseline, TTT3R, and remain competitive w.r.t. O ( n ^ { 2 } ) baselines. FastVGGT code fails on NRGBD-S due to one instance having only two views*

- **DTU-Dense**: CD 1.654 vs TTT3R 5.708（3.45倍优）
- **ETH3D**: CD 0.480 vs TTT3R 0.885（1.84倍优）
- **NRGBD-D**: CD 0.029 vs TTT3R 0.071（2.45倍优）

与$O(n^2)$的VGGT相比，VGG-T3保持竞争力：在DTU-Sparse上CD 0.066 vs VGGT 0.061，差距仅8%。这一微小差距源于线性化过程中信息压缩的固有损失，但VGG-T3以11.6倍的速度优势弥补了这一不足。

**关键洞察**：VGG-T3的线性化并非简单的精度-速度权衡，而是通过测试时训练将KV空间压缩为MLP权重，在保持场景全局一致性的同时实现了线性扩展。TTT3R依赖固定尺寸记忆处理有序序列，而VGG-T3通过MLP权重隐式编码场景几何，对无序图像集合同样有效。

---

### 视频深度估计：超越序列化基线

**Table 2** 展示了KITTI和Sintel上的视频深度估计结果。VGG-T3大幅超越TTT3R：

![[assets/figures/papers/paper_list_l16_https_arxiv_org_abs_2602_23361/figures/007_Table_2.jpg]]
*Table 2: Video depth estimation. $\boldsymbol { \mathrm { V G G } } \boldsymbol { - } \boldsymbol { \mathrm { T } } ^ { 3 }$ outperforms sequential O(n) baseline by a substantial margin and performs on-par with O ( $n ^ { 2 }$ ) baselines

- **KITTI**: $\delta < 1.25$ 达0.967，TTT3R仅0.818（提升18%）
- **Sintel**: $\delta < 1.25$ 达0.581，TTT3R仅0.510

值得注意的是，VGG-T3在KITTI上的表现与$O(n^2)$的VGGT（0.968）几乎持平，仅差0.001。这验证了测试时训练的MLP表示在有序视频场景中同样能有效捕获时序-空间依赖关系，且不需要序列化处理的归纳偏置。

---

### 相机位姿估计：线性化的阿喀琉斯之踵

**Table 3** 揭示了VGG-T3的一个显著弱点：在有序输入上的相机位姿估计精度低于TTT3R。ScanNet上ATE为0.070 vs TTT3R的0.063，RPEr为0.878 vs 0.617。

![[assets/figures/papers/paper_list_l16_https_arxiv_org_abs_2602_23361/figures/010_Table_3.jpg]]
*Table 3: Camera pose estimation. Our method supports both ordered and unordered input sequences, whereas the other TTT3R performs poorly on unordered inputs. Via sequential processing, TTT3R provides more accurate pose estimates. Best performance on ordered inputs are marked bold, best un-ordered blue*

这一退化被归因于VGGT架构中特殊的异构相机token结构。VGGT使用专用的相机token与图像token进行全局注意力交互来估计位姿，而MLP的固定容量难以有效记忆这种异构token间的复杂映射关系。TTT3R通过序列化处理自然保留了时序信息，在位姿估计上具有结构优势。

**优势面**：VGG-T3支持无序图像集合的位姿估计，而TTT3R在无序输入上性能急剧下降——这体现了MLP表示对输入顺序的不变性优势。

---

### 大规模重建：从分钟到秒的跨越

**Figure 4** 展示了7scenes数据集上100、500、1k图像集合的运行时间与精度对比。核心发现：

- **1k图像**：VGG-T3仅需58秒，VGGT需约11分钟，加速11.6倍
- **精度差距随规模缩小**：100张图像时VGG-T3与VGGT的CD差距明显，但1k张时差距显著缩小
- **扩展性对比**：VGG-T3的扩展曲线与TTT3R几乎平行，不随图像数量增加而退化

**Table 4** 进一步展示了分布式推理的线性加速能力：

![[assets/figures/papers/paper_list_l16_https_arxiv_org_abs_2602_23361/figures/009_Table_4.jpg]]
*Table 4: Reconstruction latency (s) with distributed inference. $\boldsymbol { \nabla } \mathrm { G } \mathrm { G } { - } \mathrm { T } ^ { 3 }$ can efficiently process large sequences on a single GPU, and provide linear speed-up via distributed inference

- 单GPU处理2000张图像：230.7秒
- 2 GPU：74.8秒（3.08倍加速）
- 4 GPU：48.5秒（4.75倍加速，相较VGGT的27分钟提升33倍）

分布式推理的高效性源于TTT损失梯度的可分解性（Eq. 5）：总梯度等于各token梯度的和，允许minibatch梯度累积，跨GPU仅需在MLP权重更新时进行通信，无需复杂的上下文并行实现。

---

### 视觉定位：MLP状态表示的优势

**Table 5** 展示了前馈视觉定位结果。VGG-T3在7scenes和Wayspots上均优于TTT3R：

![[assets/figures/papers/paper_list_l16_https_arxiv_org_abs_2602_23361/figures/013_Table_5.jpg]]
*Table 5: Feed-forward visual localization in unposed image collection. The MLP-based state representation in $\boldsymbol { \mathrm { V G G } } \boldsymbol { - } \boldsymbol { \mathrm { T } } ^ { 3 }$ allows for more precise localization of new images compared to TTT3R. Table 6. Ablations. We evaluate key design decisions behind our linearization and ShortConv2D design

- **7scenes**: 平移误差0.16m，20cm/20°定位率73.00%
- **Wayspots**: 平移误差1.90m，20cm/20°定位率30.64%

VGG-T3的MLP状态表示允许查询未参与测试时优化的新图像，实现了真正的前馈定位。**Figure 8** 展示了跨时间定位能力：在KITTI序列上重建场景后，成功定位了7年后拍摄的游客照片——尽管外观和场景组成发生了显著变化。

---

### 消融实验：设计选择的因果链

**Table 6** 系统消融了线性化的关键设计决策：

1. **预训练权重至关重要**：从头训练（Scratch）的线性化模型陷入局部最优，CD高达0.262，而基于VGGT预训练权重的线性化仅0.066。这验证了核心洞察：softmax注意力权重为MLP提供了良好的初始化流形。

2. **LayerNorm → L2归一化**：移除LayerNorm改用L2归一化是解锁预训练权重快速收敛的关键。LayerNorm的统计量偏移导致TTT目标收敛缓慢，L2归一化消除了这一障碍。

3. **ShortConv2D的精确配置**（**Table 9**）：在值空间使用3×3卷积效果最佳（CD 0.066，NC 0.838，mAA 74.14）。更大的卷积核或同时对键和值应用卷积会降低性能——这表明局部空间混合需要精确控制在值空间，过度混合会破坏K-V映射的学习。

4. **TTT优化步数**（**Figure 5**）：2个优化器步数在不同图像集合大小下达到最佳点图误差。更多步数不再带来增益，暗示MLP容量成为瓶颈。

---

### 失败模式与局限性

**Figure 9b** 展示了Waymo序列上的失败案例：在空间范围更大或场景布局更复杂的条件下，VGG-T3的重建质量明显下降，无法完全匹配softmax注意力精度。这揭示了固定尺寸MLP表示的信息容量上限。

![[assets/figures/papers/paper_list_l16_https_arxiv_org_abs_2602_23361/figures/021_Figure_9.jpg]]
*Figure 9: Waymo sequence reconstructions comparison with VGGT*

**位姿估计的系统性弱点**：如前所述，异构相机token与TTT MLP的交互困难导致位姿估计精度不足，这是当前架构层面的根本限制。

**缩放行为**：**Figure 3b** 显示，使用固定优化步数时，从100张扩展到1k张图像，点图误差增加约5倍。虽然增加优化步数可以缓解（**Figure 3a**），但这表明MLP容量和优化步数需要根据场景规模动态调整。

![[assets/figures/papers/paper_list_l16_https_arxiv_org_abs_2602_23361/figures/005_Figure_3.jpg]]
*Figure 3: (b) Pointmap prediction error for different number of input images (lower is better). Figure 3. Sequence-length generalization analysis*

---

### 实验公平性说明

所有方法在NVIDIA A100-80GB GPU上评估。单GPU实验使用minibatch卸载技术保证公平的内存约束。VGGT基线应用了注意力熵缩放（**Table 8**），在大规模图像集合上提供了更强的对比基准，避免基线因注意力分散而被人为削弱。

![[assets/figures/papers/paper_list_l16_https_arxiv_org_abs_2602_23361/figures/015_Table_8.jpg]]
*Table 8: Attention entropy-scaling makes VGGT a stronger baseline on large image collections*

### 补充图表

![[assets/figures/papers/paper_list_l16_https_arxiv_org_abs_2602_23361/figures/008_Figure.jpg]]
*Figure: VGGT (11 minutes) Ours (58s)*

![[assets/figures/papers/paper_list_l16_https_arxiv_org_abs_2602_23361/figures/011_Table.jpg]]

![[assets/figures/papers/paper_list_l16_https_arxiv_org_abs_2602_23361/figures/014_Table_7.jpg]]
*Table 7: Datasets used for training*

## 方法谱系与知识库定位

### 1. 方法谱系：从二次全局注意力到线性测试时训练

VGG-T3 的核心贡献在于将离线多视图前馈重建模型的推理复杂度从 $O(n^2)$ 降至 $O(n)$，其方法谱系可沿两条轴线梳理：**前馈3D重建架构的演进** 与 **线性注意力/测试时训练的替代方案**。

#### 1.1 前馈重建架构的基底：VGGT 及其加速变体

VGG-T3 直接继承自 **VGGT**（Wang et al., CVPR 2025）的架构范式。VGGT 是一种离线前馈模型，通过交替的图像内自注意力和跨图像全局自注意力层，从无姿态的多视图图像集合中直接预测逐像素深度图、相机位姿和内参。其核心瓶颈在于全局自注意力层：所有输入图像的 token 构成一个可变长度的键值（KV）空间，softmax 注意力在该空间上的计算和内存需求随图像数量 $n$ 呈二次增长，使得 VGGT 处理 2000 张图像需耗时约 27 分钟。

为缓解这一问题，社区提出了两种加速变体，但均未突破二次复杂度：
- **FastVGGT**（Shen et al., arXiv 2025）：通过 token 合并减少 KV 序列长度，但注意力操作本身仍为 $O(n^2)$。
- **SparseVGGT**（Wang et al., arXiv 2025）：引入块稀疏注意力，将计算限制在局部窗口内，同样未改变渐近复杂度。

VGG-T3 的定位在于：**保留 VGGT 的预训练编码器/解码器权重和交替注意力架构骨架，仅将全局自注意力层替换为线性时间的测试时训练（TTT）层**。这一策略使得 VGG-T3 在精度上接近 VGGT（作为精度上界），同时获得线性扩展能力。

#### 1.2 线性注意力与测试时训练的交叉点

在线性注意力替代方案的光谱上，VGG-T3 与 **TTT3R** 同属基于测试时训练的 $O(n)$ 方法，但二者在状态表示和适用场景上存在本质差异：

| 维度 | TTT3R | VGG-T3 |
|------|-------|--------|
| 输入假设 | 有序序列（视频帧） | 有序或无序图像集合 |
| 状态更新方式 | 在线递归更新固定尺寸记忆 | 离线批量压缩 KV 空间至 MLP 权重 |
| 查询能力 | 仅当前状态 | 支持新图像的前馈定位（未见于 TTT 优化阶段） |
| 分布式推理 | 不直接支持 | 天然支持 DDP，梯度可分解求和 |

VGG-T3 在点图估计任务上显著优于 TTT3R：在 DTU 密集分割上 Chamfer Distance 降低 3.45 倍（1.654 vs 5.708），在 NRGBD-D 上降低 2.45 倍（0.029 vs 0.071），在 ETH3D 上降低 1.84 倍（0.480 vs 0.885）（Table 1）。在视频深度估计的 KITTI 基准上，$δ<1.25$ 指标从 TTT3R 的 0.818 提升至 0.967（Table 2）。这一差距源于 VGG-T3 的两项关键设计选择：

1. **ShortConv2D 值空间混合**：在值向量上施加 $3×3$ 卷积，打破键-值之间的线性依赖关系，增强 TTT 优化目标的表达力。消融实验表明，仅对值空间使用 $3×3$ 卷积效果最佳（CD 0.066, NC 0.838），更大的卷积核或同时对键和值应用卷积均导致性能下降（Table 9）。

2. **L2 归一化替代 LayerNorm**：移除 LayerNorm 并改用 L2 归一化，解锁了预训练 softmax 注意力权重的快速收敛能力。若从头训练 TTT 线性化模型，模型会陷入局部最优，点图误差急剧增大（CD 0.262 vs 0.066）（Table 6）。

#### 1.3 与其他线性化方案的对比

在消融实验中，VGG-T3 的 TTT 线性化方案被与两类替代方案进行了直接比较（Table 6）：
- **T2R**（token-to-register 线性化）：性能显著弱于 TTT。
- **LoLCats**（低秩线性化）：同样不及 TTT 方案。

这表明，**测试时优化 MLP 权重以显式学习键到值的映射**，相较于静态的线性近似（如低秩分解或固定寄存器投影），能更有效地压缩可变长度 KV 空间中的几何信息。

### 2. 适用边界与失效模式

#### 2.1 精度-效率权衡：与 softmax 注意力的固有差距

VGG-T3 的线性化在带来 11.6 倍加速（1k 图像集合 54 秒 vs VGGT 的 660 秒）的同时，在重建质量上与 softmax 注意力存在可观测的差距。在 7scenes 数据集上，随着图像数量从 100 增至 1k，这一差距逐渐缩小，但并未完全消失（Figure 4）。在 Waymo 大规模序列的定性对比中，VGG-T3 在空间范围更大或场景布局更复杂的条件下，重建质量可能下降，无法完全匹配 VGGT 的 softmax 注意力精度（Figure 9b）。

这一差距的根源在于：**固定尺寸 MLP 的表示容量存在上限**。softmax 注意力可以动态地为每个查询 token 分配不同的键值权重，而 TTT MLP 将整个 KV 空间压缩为一组固定权重，在极大规模场景或宽基线条件下可能导致信息丢失。

#### 2.2 相机位姿估计的退化

VGG-T3 在相机位姿估计任务上表现不佳，在 ScanNet 有序输入上的 ATE 为 0.070，弱于 TTT3R 的 0.063（Table 3）。论文推测，这源于 VGGT 架构中特殊的**异构相机 token 结构**——相机 token 与图像 token 在特征空间中具有不同的统计特性，TTT MLP 难以在统一的键-值映射中有效记忆这种异构性。相比之下，TTT3R 的在线递归更新机制可能对有序序列中的相机状态追踪更为友好。

值得注意的是，VGG-T3 支持无序输入集合的位姿估计，而 TTT3R 在无序输入上性能急剧退化，这体现了 VGG-T3 离线批量压缩策略在输入灵活性上的优势。

#### 2.3 测试时优化步数的自适应需求

VGG-T3 的测试时训练使用 2 个优化器步数在多数图像集合大小下达到最佳点图误差，更多步数不再带来增益（Figure 5）。然而，对于分布外的大规模集合（如 1k 图像），固定步数可能导致误差增大约 5 倍（Figure 3）。这一发现暗示，**固定的优化预算无法在所有场景下最优地压缩 KV 空间**，需要根据场景复杂度动态调整步数或模型容量。

### 3. 开放问题

VGG-T3 的提出打开了若干值得进一步探索的方向：

1. **更具表达力的线性注意力设计**：当前 TTT MLP 的固定容量限制了其在复杂场景下的精度上限。如何设计可动态分配容量的线性注意力机制（如基于输入复杂度的自适应 MLP 宽度或深度），以在所有场景下匹敌 softmax 注意力精度？

2. **异构 token 的统一处理**：相机 token 等异构输入在 TTT 框架下的退化问题，揭示了当前 MLP 映射在处理多模态 token 时的局限性。是否可以通过分离的 TTT 头或条件归一化策略来改善？

3. **固定尺寸表示的信息容量边界**：MLP 压缩的 KV 空间是否存在理论上的信息容量上限？在极端尺度或稀疏视图条件下，如何量化并避免性能的急剧退化？

4. **TTT 优化步数的自适应调度**：能否根据输入集合的规模、基线宽度或场景复杂度，在测试时自动决定最优的优化步数，实现真正的自适应计算？

5. **压缩表示的可解释性与下游应用**：TTT 优化后的 MLP 权重隐式编码了场景几何信息。这一压缩表示是否可被解释或提取为显式的几何基元（如点云、网格），从而桥接前馈方法与经典 SfM/MVS 流程？

6. **与在线方法的融合**：VGG-T3 的离线批量压缩与 TTT3R 的在线递归更新各有所长。是否存在统一的测试时训练框架，在离线阶段批量压缩全局信息，在在线阶段递归融合新观测，兼顾精度、效率与实时性？

## 原文 PDF

![[paperPDFs/CVPR_2026/VGG_T3_Offline_Feed_Forward_3D_Reconstruction_at_Scale.pdf]]
