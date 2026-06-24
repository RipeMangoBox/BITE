---
title: "Compact Neural Graphics Primitives with Learned Hash Probing"
type: paper
paper_level: A
venue: "SIGGRAPH Asia"
year: 2023
pdf_ref: paperPDFs/SIGGRAPH_ASIA_2023/Compact_Neural_Graphics_Primitives_with_Learned_Hash_Probing.pdf
project_link: https://research.nvidia.com/labs/toronto-ai/compact-ngp/
aliases:
- CN
- CNGPLHP
tags:
- SIGGRAPH_ASIA_2023
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
core_operator: "将确定性哈希与可学习的探测（learned probing）按位组合，哈希生成索引高位，索引码本学习低位偏移；通过直通估计器（straight‑through estimator）训练，仅用少量可学习位（log₂ Nₚ）实现冲突解决与信息复用，从而在保持高速推理的同时大幅压缩模型体积。"
primary_logic: "将所有特征网格统一为索引函数框架，允许不同索引方案通过算术运算组合；将哈希与可学习索引按比特拼接，避免量化或熵编码，直接支持随机访问，在压缩率与速度上实现帕累托最优平衡。"
claims:
- "在NeRF场景的PSNR-文件大小帕累托曲线上全面优于Instant NGP。"
- "在合成NeRF数据集上质量几乎不变（平均PSNR 30.66 vs. 30.93），模型体积缩小2.8倍。"
- "推理速度比Instant NGP更快（28.7 μs vs. 10.1–10.2 μs），训练开销仅为1.2–2.6倍。"
- "在8000×8000 Pluto大图像上，在多数实际尺寸范围内超越JPEG。"
---

# Compact Neural Graphics Primitives with Learned Hash Probing

> [!tip] 核心洞察
> 将所有特征网格统一为索引函数框架，允许不同索引方案通过算术运算组合；将哈希与可学习索引按比特拼接，避免量化或熵编码，直接支持随机访问，在压缩率与速度上实现帕累托最优平衡。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 基于学习哈希探测的紧凑神经图形基元 |
| 英文题名 | Compact Neural Graphics Primitives with Learned Hash Probing |
| 会议/期刊 | SIGGRAPH Asia 2023 |
| Links | [paper](https://arxiv.org/abs/2312.17241); [Project](https://research.nvidia.com/labs/toronto-ai/compact-ngp/) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction |
| Method | Compact NGP |
| Dataset | NeRF Synthetic Dataset (Mildenhall et al.), Kodak Image Dataset, Pluto 8000×8000 Image, Paving Stones Texture Set |

> [!tip] 效果简介
> - NeRF Synthetic Dataset (Mildenhall et al.) 上，Average PSNR 为 30.66，对比 30.93 (Instant NGP)，变化 -0.27（质量相近，模型大小从1000 kB 降至357 kB）。
> - Kodak Image Dataset 上，PSNR vs. file size 为 在小文件尺寸下接近 JPEG，大尺寸下略差，对比 JPEG, Instant NGP，变化 竞争水平。
> - Pluto 8000×8000 Image 上，PSNR vs. file size 为 在多数实际尺寸下超越 JPEG，对比 JPEG, Instant NGP, ACORN，变化 更好。

## 概述

神经图形基元（neural graphics primitives）面临一个根本性矛盾：如何在保持快速随机访问推理的同时，将特征网格压缩到极小体积。密集网格与空间哈希表内存开销大，而可学习索引（如 **VQAD**，Takikawa et al., SIGGRAPH 2022）或矢量量化虽能压缩，却导致训练缓慢或推理延迟显著上升。

本文提出 **Compact NGP**，其核心思路是将确定性哈希与可学习的探测（learned probing）按位组合：哈希生成索引高位，一个辅助索引码本学习产生低位偏移。通过直通估计器（straight‑through estimator）训练，仅用少量可学习位（$\log_2 N_p$）即可实现冲突解决与信息复用，在保持高速推理的同时大幅压缩模型体积。该方法将所有特征网格统一为索引函数框架，允许不同索引方案通过算术运算组合，避免了量化或熵编码，直接支持随机访问。

实验表明，Compact NGP 在 NeRF 场景的 PSNR‑文件大小帕累托曲线上全面优于 **Instant NGP**（Müller et al., ACM Trans. Graph. 2022）（Figure 2）；在合成 NeRF 数据集上质量几乎不变（平均 PSNR 30.66 vs. 30.93），模型体积缩小 2.8 倍（Table 3）；推理速度比 Instant NGP 更快（28.7 μs vs. ~10 μs），训练开销仅为 1.2–2.6 倍（Table 2）。在 8000×8000 的 Pluto 大图像上，该方法在多数实际尺寸范围内超越 JPEG（Figure 8）。消融实验证实，小探测范围（$N_p \le 2^4$）足以获得良好压缩，更大探测范围收益递减（Figure 5）。

该方法的局限性包括：在 Kodak 数据集上大文件尺寸下质量不及 JPEG，且未使用量化导致极小模型时浮点参数主导；在纹理压缩任务上性能低于专用架构 **NTC**（Vaidyanathan et al., SIGGRAPH 2023）。

## 背景与动机

神经隐式表示已在三维重建、视图合成和图像拟合等任务中展现出强大的表达能力。这类方法的核心组件之一是**神经图形基元**（neural graphics primitives），即一个将空间坐标映射为特征向量的可训练特征网格，其后接一个轻量级多层感知机（MLP）解码为颜色、密度等输出信号。特征网格的设计直接决定了模型的质量、存储开销和查询速度，因而成为神经场方法走向实际部署的关键瓶颈。

### 特征网格的索引困境

从抽象层面看，所有特征网格本质上都定义了一个**索引函数** $f(\mathbf{v})$，将整数网格顶点 $\mathbf{v}$ 映射到特征码本 $D_f$ 中的某个条目（Figure 3）。不同的索引方案在这一映射的实现方式上存在根本分歧，形成了**紧凑存储**与**快速查询**之间的尖锐张力：

- **密集网格**（dense grid）为每个顶点分配独立的特征向量，支持 $O(1)$ 随机访问，但内存开销随分辨率呈指数增长，在三维以上空间中完全不可行。
- **空间哈希**（spatial hashing）——以 **Instant NGP**（Müller et al., ACM Trans. Graph. 2022）为代表——通过确定性哈希函数将顶点映射到固定大小的哈希表，实现了高速训练与推理。然而，哈希冲突迫使使用较大的特征码本以保证质量，导致模型体积膨胀，不利于存储和传输。
- **可学习索引**（learned indexing）——如 **VQAD**（Takikawa et al., SIGGRAPH 2022）——通过训练一个辅助索引码本 $D_c$ 来学习顶点到特征向量的映射，能以更紧凑的码本实现同等质量。但其索引结构（如八叉树）破坏了空间局部性，导致训练收敛缓慢，且推理时需遍历树结构，延迟较高。
- **矢量量化与熵编码**等压缩方法虽能进一步缩减体积，但引入了不可微的解压缩步骤，丧失了随机访问能力，不适用于需要实时查询的图形应用（如游戏纹理采样、细节层次流式加载）。

这一困境的实质在于：**现有方案无法在同一框架内同时实现紧凑编码、快速随机访问和可微训练**。Instant NGP 牺牲了紧凑性换取速度，VQAD 牺牲了速度换取紧凑性，而量化-编码路线则牺牲了随机访问能力。

### 本文动机与核心思路

本文观察到，上述索引方案并非互斥——由于它们最终都产生一个整数索引来查询特征码本，**不同方案的索引可以通过算术运算进行组合**（Figure 3 总述）。基于这一洞察，论文提出 **Compact NGP**，将确定性哈希与可学习索引按位拼接：哈希函数生成索引的**高位**（most significant bits），保证均匀分布与快速定位；一个轻量的可学习索引码本生成索引的**低位**（least significant bits），在极小的探测范围 $N_p$ 内解决哈希冲突并实现信息复用。

这一设计的关键优势在于：
1. **无需量化或熵编码**，直接支持随机访问，推理时无需解压缩步骤；
2. **训练开销可控**（仅为 Instant NGP 的 1.2–2.6 倍），推理速度甚至**快于** Instant NGP（因更小的模型体积利于缓存命中，Table 2）；
3. 在 NeRF 场景的 PSNR-文件大小帕累托曲线上**全面优于** Instant NGP（Figure 2），在合成 NeRF 数据集上以 2.8 倍的压缩比实现几乎无损的质量（Table 3）；
4. 在 8000×8000 Pluto 大图像上，在多数实用尺寸范围内**超越 JPEG**（Figure 8），验证了该方法在图像拟合任务上的通用性。

综上，Compact NGP 在神经图形基元的压缩率-速度谱系中找到了一个帕累托最优平衡点，为需要紧凑存储与实时随机访问的应用（如游戏纹理压缩、实时光照缓存、细节层次流式传输）提供了新的基准方案。

## 核心创新

Compact NGP 的核心创新在于将确定性空间哈希与可学习的索引探测（learned probing）按位组合，构建了一种统一的索引函数框架，从而在保持推理速度的前提下大幅压缩神经图形基元的存储体积。该方法的关键设计可归纳为以下三个层面的“变更槽位”（changed slots）：

**1. 索引低位生成方式：从无探测到可学习探测**
Instant NGP 的索引完全由确定性哈希函数生成（$N_p=1$，无探测），而 Compact NGP 引入了一个辅助哈希索引的索引码本 $D_c$，为每个网格顶点学习产生 $\log_2 N_p$ 位的低位偏移量（见 Eq. (6)、Figure 4）。这 $N_p$ 个候选索引允许模型在特征码本中进行“探测”，从而以极少的可学习位实现冲突解决与信息复用——这是将压缩率与速度推向帕累托最优的核心因果旋钮。

**2. 索引码本规模 $N_c$：从不存在到可配置**
Instant NGP 不具备索引码本概念；Compact NGP 新增了用户可配置的索引码本 $D_c$，规模从 $2^{10}$ 到 $2^{24}$（Table 1）。该码本通过第二个独立的空间哈希（hash2）进行稀疏化索引，使得模型能够以整数索引（仅 $\log_2 N_p$ 位）替代大量浮点特征参数，从而将存储成本从浮点主导转变为整数主导。

**3. 探测范围 $N_p$：从 1 到可配置**
Instant NGP 的探测范围固定为 1（即直接取哈希结果）；Compact NGP 将其扩展为可配置的 $2^1$ 至 $2^4$（Table 1）。消融实验证实，仅 $N_p \leq 2^4$ 即可获得良好的压缩效果，更大的探测范围仅带来微小收益但训练开销显著增加（Figure 5）。

**4. 训练中的梯度传播：从标准反向传播到 softmax 直通估计器**
Instant NGP 对单个特征进行标准梯度传播；Compact NGP 在反向传播时对 $N_p$ 个候选特征做 softmax 加权，前向传播则取 argmax（即直通估计器，straight-through estimator），训练完成后将最大置信度索引烘焙到紧凑的辅助码本 $D_c$ 中以加速推理（Figure 4 caption）。这一设计使得可学习索引能够以端到端方式优化，同时避免了量化或熵编码，直接支持随机访问。

**创新本质的统一视角**
论文将所有特征网格统一为“索引函数”框架（Figure 3），指出密集网格、k-平面、稀疏树、空间哈希和可学习索引本质上是不同的索引映射方式，因而可以通过算术运算组合。Compact NGP 正是将确定性哈希（高位）与可学习索引（低位）按位拼接，在不引入解压缩步骤的前提下，实现了压缩率与速度的帕累托最优平衡。

## 整体框架

Compact NGP 的整体流水线继承自 **Instant NGP**（Müller et al., ACM Trans. Graph. 2022）的多分辨率哈希编码框架，并在其索引阶段引入可学习的探测（learned probing）机制，形成“确定性哈希 + 可学习索引”的混合索引方案。如图 4 所示，流水线由以下模块串联构成：

1. **坐标到体素顶点映射**：对于给定的连续输入坐标 $\mathbf{x} \in \mathbb{R}^d$，首先找到其包围的整数网格顶点 $\mathbf{v} \in \mathbb{Z}^d$。这一步骤与 Instant NGP 完全一致，为后续的逐顶点特征查询提供离散化坐标。

2. **主哈希（hash₁）生成索引高位**：对每个顶点 $\mathbf{v}$，使用一个空间哈希函数 $\mathtt{hash}(\mathbf{v})$ 计算索引的**最高有效位**（most significant bits）。该哈希函数沿用 Instant NGP 的设计，通过大素数异或运算实现均匀分布，保证确定性快速访问。

3. **辅助哈希（hash₂）索引到索引码本**：一个独立的辅助空间哈希 $\mathtt{hash2}(\mathbf{v})$ 将顶点映射到索引码本 $\widehat{D}_c$ 的某一行。该行存储 $N_p$ 个置信度值，对应 $N_p$ 个候选的低位偏移量。

4. **索引码本（$\widehat{D}_c / D_c$）学习低位探测偏移**：在训练阶段，$\widehat{D}_c$ 的每一行经过 softmax 得到概率分布，通过直通估计器（straight‑through estimator）选择置信度最大的索引作为**最低有效位**（least significant bits），实现冲突解决与信息复用。训练后，每行的 $\log_2 N_p$ 位最大置信度索引被“烘焙”（bake）到紧凑的辅助索引码本 $D_c$ 中，用于高效前向推理。

5. **特征码本（$D_f$）查询**：将主哈希产生的高位与索引码本产生的低位按位拼接，形成最终的特征码本索引，从 $D_f$ 中取出对应的特征向量。这一设计使得存储成本从浮点数主导转变为整数主导——整数索引仅需 $\log_2 N_p$ 位。

6. **线性插值与 MLP 解码**：对包围坐标 $\mathbf{x}$ 的多个顶点特征向量进行 $d$-线性插值，将插值结果输入小型 MLP 解码为输出信号（如颜色与密度）。

**关键设计选择**：该方法将所有特征网格统一视为索引函数框架（见图 3），允许不同索引方案通过算术运算组合。Compact NGP 将确定性哈希与可学习索引按位拼接，避免了量化或熵编码，直接支持随机访问，从而在保持高速推理的同时实现大幅模型压缩。训练时反向传播对 $N_p$ 个特征做 softmax 加权，前向取 argmax（直通估计器），保证了索引学习的可微性。

### 补充图表

![[assets/figures/papers/paper_list_l32_https_arxiv_org_abs_2312_17241/figures/004_Figure_4.jpg]]
*Figure 4: Overview of Compact NGP. For a given input coordinate x $\epsilon \mathbb { R } ^ { d }$ (far le ), we find its enclosing integer grid vertices v $\in \mathbb { Z } ^ { d }$ and apply our indexing function 𝑓 (v) to each one. The most significant bits of the index are computed by a spatial hash (hash) and the least significant bits by looking up a row of $N _ { p }$ confidence values from an indexing codebook $\widehat { D } _ { c }$ that is in turn indexed by an auxiliary spatial hash (hash2), and then picking the index with maximal confidence (green arrow). Bitwise concatenation of the two indices yields an index for looking up from the feature codebook $D _ { f }$ , which is subsequently 𝑑-linearly...

## 核心模块与公式推导

### 统一索引函数框架

Compact NGP 的核心洞察在于：所有特征网格本质上都对应一个从整数网格坐标 $\mathbf{v} \in \mathbb{Z}^d$ 到特征向量的索引函数。这一视角将密集网格、k-平面、稀疏树、空间哈希和可学习索引统一为同一抽象——它们仅在如何计算特征码本 $D_f$ 的索引上有所不同。基于此，不同索引方案可以通过对它们产生的索引进行算术运算来组合。

### 基线索引函数

**Instant NGP 的空间哈希**（Müller et al., ACM Trans. Graph. 2022）使用确定性哈希函数将网格顶点映射到特征码本：

$$f(\mathbf{v}) = D_f[\mathsf{hash}(\mathbf{v}) \bmod N_f], \quad \mathsf{hash}(\mathbf{v}) = \bigoplus_{i=0}^{d-1} v_i \cdot \pi_i$$

其中 $\oplus$ 为按位异或，$\pi_i$ 为大素数常量。这一方案速度快但存在哈希冲突，且特征码本大小 $N_f$ 直接决定模型体积。

**VQAD 的可学习索引**（Takikawa et al., SIGGRAPH 2022）通过树结构或索引码本进行特征查找：

$$f(\mathbf{v}) = D_f[D_c[\mathsf{tree\_index}(\mathbf{v})]]$$

该方法压缩率高但依赖串行树遍历，推理延迟较高。

### Compact NGP 索引函数

本文方法将确定性哈希与可学习探测按位组合，核心查找函数为：

$$f(\mathbf{v}) = D_f\big[(N_p \cdot \mathsf{hash}(\mathbf{v})) \bmod N_f + D_c[\mathsf{hash2}(\mathbf{v})]\big]$$

**变量含义**：
- $\mathbf{v}$：输入坐标的包围整数网格顶点
- $\mathsf{hash}(\mathbf{v})$：主空间哈希函数，生成索引的**高位部分**，实现均匀分布
- $\mathsf{hash2}(\mathbf{v})$：辅助空间哈希函数，与主哈希独立，用于索引到索引码本 $D_c$ 的行
- $N_p$：探测范围，即可学习的低位偏移数量（用户可配置，典型值 $2^1$ 至 $2^4$）
- $N_f$：特征码本 $D_f$ 的大小
- $D_c$：索引码本，每个入口存储一个 $\log_2 N_p$ 位的低位偏移量
- $D_f$：特征码本，存储实际特征向量

**按位组合机制**：主哈希产生的高位乘以 $N_p$ 后对 $N_f$ 取模，为每个哈希桶预留 $N_p$ 个连续的特征槽位；索引码本 $D_c$ 通过辅助哈希学习选择具体的槽位偏移。这种设计使得哈希冲突可以通过学习选择不同的低位偏移来解决，同时实现特征槽位的信息复用。

### 训练中的梯度传播

前向传播时，从 $D_c$ 的 $N_p$ 个置信度值中取 argmax 确定索引低位。反向传播时，采用**直通估计器**（straight-through estimator, Bengio et al. 2013）：将前向的硬最大值替换为 softmax 加权，使梯度能够传播到所有 $N_p$ 个候选槽位。训练完成后，将每行的最大置信度索引烘焙到紧凑的辅助码本 $D_c$ 中，推理时仅需 $O(1)$ 的简单查表操作。

### 流水线模块

1. **坐标到体素顶点映射**：将连续输入坐标 $\mathbf{x} \in \mathbb{R}^d$ 映射到其包围的 $2^d$ 个整数网格顶点 $\mathbf{v}$
2. **主哈希**：对每个顶点计算索引高位
3. **辅助哈希**：独立计算索引码本 $D_c$ 的行索引
4. **索引码本 $D_c$**：提供低位探测偏移，实现冲突解决与信息复用
5. **特征码本 $D_f$**：被最终组合索引查询，返回特征向量
6. **线性插值与 MLP 解码**：对多顶点特征进行 $d$-线性插值后输入 MLP 解码为输出信号

## 实验与分析

### 核心性能对比

Compact NGP 在多个任务上实现了压缩率与质量的帕累托改进，其核心优势在于将存储成本从浮点数主导向整数主导迁移——索引码本中的整数仅需 $\log_2 N_p$ 比特。

在 NeRF 场景的重建任务上，Compact NGP 在 PSNR-文件大小的帕累托曲线上全面优于 Instant NGP（Müller et al., ACM Trans. Graph. 2022），并与掩码小波表示方法（Rho et al. 2023）具有竞争力（Figure 2）。在完整的合成 NeRF 数据集（Mildenhall et al. 2020）上，Compact NGP 以 2.8 倍的模型体积压缩（1000 kB → 357 kB），实现了几乎无损的质量保持：平均 PSNR 为 30.66，而 Instant NGP 为 30.93，仅下降 0.27 dB（Table 3）。

![[assets/figures/papers/paper_list_l32_https_arxiv_org_abs_2312_17241/figures/014_Table_3.jpg]]
*Table 3: antiative results on the full synthetic dataset from Mildenhall et al. [2020], showing a near-quality (PSNR) comparison between Instant NGP and our work. We see that we are able to achieve similar quality across the entire dataset with a 2.8× more compact representation. Table 4. antiative results on texture compression on the Paving Stones texture set, retrieved from https://ambientcg.com, showing the tradeof between quality (PSNR) and size (kB) for diferent methods. We compare against traditional texture compression baselines (BC) as well as recent neural baselines (NTC [Vaidyanathan et al. 2023]). We borrow the results from Vaidyanathan et al. [2023]. Although our work does not outperfor...*

在图像压缩任务上，方法展现出任务依赖的特性。在 Kodak 数据集上，Compact NGP 在小文件尺寸下接近 JPEG 的质量，但在大文件尺寸下表现略差（Figure 7）。这主要源于极小模型尺寸时，MLP 和特征码本的浮点参数占据主导，而方法未采用量化技术。然而，在 8000×8000 的 Pluto 大图像上，Compact NGP 在多数实际应用的尺寸范围内超越了 JPEG，且视觉伪影更易接受——JPEG 呈现色彩量化伪影，而 Compact NGP 仅表现为轻微模糊（Figure 8）。

![[assets/figures/papers/paper_list_l32_https_arxiv_org_abs_2312_17241/figures/011_Figure_8.jpg]]
*Figure 8: We fit Compact NGP to the 8000×8000px Pluto image using parameters $N _ { f } = 2 ^ { 6 }$ and $N _ { p } = 2 ^ { 4 }$ and varying $N _ { c }$ (green curve ranging from $2 ^ { 1 2 }$ \ $\mathrm { t o }$ \ $2 ^ { 2 4 }$ ) . We show that we are able to outperform JPEG on a wide range of quality levels. The qualitative comparisons at equal size (insets) show the visual artifacts exhibited by diferent methods: while JPEG has color quantization arfitacts, ours appears slightly blurred*

在纹理压缩任务上，使用 Paving Stones 纹理集进行测试。Compact NGP 在相似文件大小下（3494 kB）实现了 26.69 dB 的平均 PSNR，优于传统块压缩 BC（23.25 dB, 3500 kB）和 Instant NGP（22.61 dB, 1049 kB），但不及专用神经纹理压缩方法 NTC（Vaidyanathan et al., SIGGRAPH 2023）的 29.00 dB（3360 kB）（Table 4）。需要注意的是，与 NTC 的对比排除了 mipmap 以保证公平性，而 BC 的结果仅报告了所有通道的平均值。

### 训练与推理效率

Compact NGP 在计算效率上实现了有利的权衡：训练开销可控，推理速度反超基线。具体而言，训练时间开销为 Instant NGP 的 1.2–2.6 倍，其中探测范围 $N_p$ 是影响训练速度的主要因素，而索引码本大小 $N_c$ 和特征码本大小 $N_f$ 的影响较弱（Table 2）。在 NeRF Lego digger 数据集上，Instant NGP（$N_f=2^{16}$）的单次迭代训练时间为 5.4 ms，而 Compact NGP 在不同配置下为 6.8–14.1 ms。

![[assets/figures/papers/paper_list_l32_https_arxiv_org_abs_2312_17241/figures/008_Table_2.jpg]]
*Table 2: Training and inference time overheads of Compact NGP. Training times are measured for an iteration of training on the NeRF Lego digger dataset. Inference times are for 2 ^ { 1 8 } lookups on a single multiresolution level. The relative training overhead (denoted with 𝑛×) is measured with respect to Instant NGP ( N _ { f } = 2 ^ { 1 6 } ) , ranging from 1.2–2.6×. The largest impact on speed has the probing range N _ { p } , whereas N _ { c } (shown) and N _ { f } (see Müller et al. [2022]) only have a weak efect*

值得注意的是，Compact NGP 的推理速度比 Instant NGP 更快：在单层多分辨率网格上进行 $2^{18}$ 次查找，Instant NGP 耗时 28.7 μs，而 Compact NGP 仅需 10.1–10.2 μs（Table 2）。这一反直觉的结果归因于显著减小的模型体积更好地适配了缓存层次结构。

### 超参数消融分析

对超参数的消融实验揭示了若干重要规律。在 Kodak 图像压缩任务上的参数扫描（Figure 5）表明：

![[assets/figures/papers/paper_list_l32_https_arxiv_org_abs_2312_17241/figures/007_Figure_6.jpg]]
*Figure 6: PSNR vs. file size for varying hyperparameters in compressing the NeRF Lego digger. The layout is the same as Figure 5. We also show rendered images of our compressed representation at two quality se ings*

- **探测范围 $N_p$**：小探测范围（$N_p \leq 2^4$）足以实现良好的压缩效果——在较小 $N_c$ 下甚至是最优选择。更大的探测范围（虚线曲线）仅在 $N_c$ 较大时带来微小提升，但以增加训练时间为代价。$N_p=1$（即退化为 Instant NGP）在图中以 ★ 标记，由于其对 $N_c$ 不变，因此没有对应曲线。

- **参数分配比例**：在给定文件大小 $N$ 下，最优的参数分配约为特征码本大小 $N_f = 1/3 N$，索引码本大小 $N_c = 2/3 N$（同色 ★ 标记处）。

- **多分辨率层级数 $L$**：默认值 $L=16$（继承自 Instant NGP）在数百 kB 的实用范围内表现良好；更低的层级数在更小文件尺寸下可获得更优的帕累托曲线（Figure 9）。

- **MLP 宽度**：默认值 64 个神经元在实用尺寸下表现良好，更小的 MLP 在极小尺寸下可取得更优的帕累托前沿（Figure 10）。

在 NeRF Lego digger 场景上的消融实验（Figure 6）展现了与图像压缩一致的规律，并提供了两个质量设置下的渲染图像对比。

### 失败模式与局限性

尽管 Compact NGP 在多数场景下表现优异，仍存在若干明确的局限性：

1. **大文件尺寸下的质量劣势**：在 Kodak 数据集上，当目标文件尺寸较大时，质量不及 JPEG。这是因为方法未使用量化技术，导致极小模型尺寸时浮点参数（MLP 权重和特征码本）占据存储主导，而已有纯 MLP 量化方法（Dupont et al. 2021; Strümpler et al. 2022）在此区域表现更优。然而，这些纯 MLP 方法在视觉愉悦目标（约 35 dB 以上）难以扩展。

2. **纹理压缩任务上的性能差距**：在 Paving Stones 纹理集上，Compact NGP 的性能低于专用神经纹理压缩方法 NTC。NTC 采用了针对纹理的专用架构和量化技术，而 Compact NGP 保持了通用性和灵活性。

3. **训练开销随探测范围增长**：训练时间最高可达 Instant NGP 的 2.6 倍，限制了更大探测范围（$N_p > 2^4$）的实际应用。

4. **空间哈希的结构性缺失**：空间哈希缺乏空间结构性，不利于依赖空间结构的后处理（如生成建模或变换编码），对于需要未知先验稀疏性的应用（如图像压缩），树形细分结构难以设计。

5. **梯度估计方法的局限性**：当前方法依赖 softmax 与直通估计器（straight-through estimator）来学习索引，未探索更稀疏或随机的梯度估计方法（如 sparsemax 或 Gumbel-softmax），这可能限制了索引效率的进一步提升。

### 补充图表

![[assets/figures/papers/paper_list_l32_https_arxiv_org_abs_2312_17241/figures/001_Figure_1.jpg]]
*Figure 1: 3D Scene from Multiview Images Fig. 1. Compact neural graphics primitives (Ours) have an inherently small size across a variety of use cases with automatically chosen hyperparameters. In contrast to similarly compressed representations like JPEG for images (top) and masked wavelet representations [Rho et al. 2023] for NeRFs [Mildenhall et al. 2020] (bo om), our representation neither uses quantization nor coding, and hence can be queried without a dedicated decompression step. This is essential for level of detail streaming and working-memory-constrained environments such as video game texture compression. The compression artifacts of our method are easy on the eye: there is less ringing th...*

![[assets/figures/papers/paper_list_l32_https_arxiv_org_abs_2312_17241/figures/005_Table_1.jpg]]
*Table 1: Hyperparameters of our method and recommended ranges. We inherit most parameters from Instant NGP [Müller et al. 2022] and introduce two additional ones pertaining to the index codebook. Gray parameters are unafected by our method and therefore set to the same values as in Instant NGP; the choice of remaining parameters is explained in Section 3*

![[assets/figures/papers/paper_list_l32_https_arxiv_org_abs_2312_17241/figures/015_Table.jpg]]

## 方法谱系与知识库定位

### 1. 核心瓶颈与设计动机

现有神经图形基元（neural graphics primitives）面临一个根本性矛盾：**密集网格**（dense grids）与**空间哈希表**（spatial hashing）虽然查询速度快，但内存开销随分辨率呈指数增长；而**索引学习**（learned indexing）或**矢量量化**（vector quantization）虽能压缩模型体积，却引入缓慢的训练过程或高昂的推理延迟。本文识别出的关键瓶颈在于：**现有方法无法在紧凑存储、快速随机访问和训练效率三者之间同时取得最优平衡**。

这一瓶颈的因果机制可表述为：
- 密集网格（如标准体素网格）将每个空间顶点一对一映射到特征向量，存储成本为 $\mathcal{O}(N^d)$，其中 $d$ 为维度，$N$ 为每维分辨率。这在大场景或高维应用中不可行。
- 空间哈希（**Instant NGP**, Müller et al., ACM Trans. Graph. 2022）通过哈希函数将无限网格映射到固定大小的特征码本，大幅降低内存，但哈希冲突导致不同空间位置共享同一特征向量，限制了表示精度。
- 索引学习方法（如 **VQAD**, Takikawa et al., SIGGRAPH 2022）通过学习索引码本来解决冲突，但依赖树结构或迭代查找，破坏了随机访问特性，且训练收敛缓慢。

本文的核心洞察是：**所有特征网格本质上都是索引函数**——将整数网格坐标映射到特征向量表的索引。这一统一视角允许不同索引方案通过算术运算组合，从而在保持高速推理的同时实现大幅压缩。

### 2. 方法定位：索引函数的算术组合

Compact NGP 的方法论创新在于**将确定性哈希与可学习探测按位组合**，形成一种新的混合索引函数。具体而言：

- **高位索引**：由空间哈希函数 $\mathsf{hash}(\mathbf{v})$ 生成，提供均匀分布的索引高位，继承 Instant NGP 的快速随机访问特性。
- **低位索引**：由辅助哈希函数 $\mathsf{hash2}(\mathbf{v})$ 索引到索引码本 $D_c$，学习产生 $\log_2 N_p$ 位的探测偏移量，用于冲突解决与信息复用。

最终的查找函数为：
$$f(\mathbf{v}) = D_f\big[(N_p \cdot \mathsf{hash}(\mathbf{v})) \bmod N_f + D_c[\mathsf{hash2}(\mathbf{v})]\big]$$

这一设计的精妙之处在于：
1. **避免量化与熵编码**：与基于量化的压缩方法（如掩码小波表示，Rho et al. 2023）不同，Compact NGP 直接支持随机访问，无需专用解压缩步骤。
2. **直通估计器训练**：前向传播时使用 argmax 选择最佳探测索引，反向传播时通过 softmax 加权传播梯度（straight-through estimator, Bengio et al. 2013），使离散索引选择可微分。
3. **存储结构转型**：将存储成本从浮点数主导（特征向量）转向整数主导（索引码本），且整数仅需 $\log_2 N_p$ 位，实现极高压缩率。

### 3. 与基线方法的系统对比

#### 3.1 与 Instant NGP 的关系

Compact NGP 是 Instant NGP 的直接扩展与改进：
- **继承**：多分辨率哈希编码框架、坐标到体素顶点的映射、$d$-线性插值与 MLP 解码流水线。
- **改进**：引入索引码本 $D_c$（大小 $2^{10}$ 到 $2^{24}$）和探测范围 $N_p$（$2^1$ 到 $2^4$）两个新超参数，将 $N_p=1$ 时的特例退化为 Instant NGP。
- **性能边界**：在 NeRF 场景的 PSNR-文件大小帕累托曲线上全面优于 Instant NGP（Figure 2），在合成 NeRF 数据集上质量几乎不变（平均 PSNR 30.66 vs. 30.93），模型体积缩小 2.8 倍（Table 3）。推理速度反而更快（28.7 μs vs. 10.1–10.2 μs，Table 2），因为更小的模型利于缓存命中。

#### 3.2 与 VQAD（Takikawa et al., SIGGRAPH 2022）的关系

VQAD 是索引学习方法的代表，通过树结构（如八叉树）和可学习索引码本进行特征查找：
$$f(\mathbf{v}) = D_f\big[D_c[\mathsf{tree\_index}(\mathbf{v})]\big]$$

Compact NGP 与 VQAD 的关键区别：
- **索引生成方式**：VQAD 依赖树结构的层次细分来分配索引，Compact NGP 则通过哈希与可学习探测的按位组合，避免了树遍历的开销。
- **随机访问能力**：VQAD 的树结构查询需要多次间接访问，无法保证 $\mathcal{O}(1)$ 随机访问；Compact NGP 通过双哈希实现常数时间查找。
- **训练效率**：VQAD 需要同时学习树结构和索引码本，训练收敛慢；Compact NGP 仅需学习索引码本的低位偏移，训练开销仅为 Instant NGP 的 1.2–2.6 倍（Table 2）。

#### 3.3 与神经纹理压缩方法（NTC, Vaidyanathan et al., SIGGRAPH 2023）的关系

NTC 是专用纹理压缩的神经基线，采用量化与专用架构：
- **性能对比**：在 Paving Stones 纹理集上，Compact NGP 平均 PSNR 26.69（3494 kB），优于传统 BC 压缩（23.25, 3500 kB）和 Instant NGP（22.61, 1049 kB），但低于 NTC（29.00, 3360 kB）（Table 4）。
- **架构差异**：NTC 使用量化与专用纹理采样架构，而 Compact NGP 保持通用性，未针对纹理做特殊优化。为公平比较，NTC 结果排除了 mipmap（Table 4 caption）。
- **适用边界**：Compact NGP 的优势在于通用性（同时适用于 NeRF、图像、纹理），而 NTC 在纹理压缩这一特定任务上通过专用设计获得更好性能。

#### 3.4 与传统图像压缩基线（JPEG, BC）的关系

- **JPEG 对比**：在 Kodak 数据集上，Compact NGP 在小文件尺寸下接近 JPEG，大尺寸下略差（Figure 7）；在 8000×8000 Pluto 大图像上，在多数实际尺寸范围内超越 JPEG（Figure 8）。JPEG 的压缩伪影主要是振铃效应和颜色量化，而 Compact NGP 表现为轻微模糊（Figure 8 insets）。
- **BC 对比**：在纹理压缩任务上，Compact NGP 在相似文件大小下显著优于 BC（26.69 vs. 23.25 PSNR, Table 4），但 BC 结果仅报告所有通道平均值（Table 4 caption），证据强度有限。

### 4. 适用边界与局限性

尽管 Compact NGP 在多个任务上展现出优异的压缩-质量-速度平衡，其适用边界受以下因素制约：

1. **极小模型尺寸下的瓶颈**：未使用浮点参数量化，导致在极小文件尺寸（<100 kB）时，MLP 和特征码本的浮点参数主导存储成本，性能不及纯 MLP 量化方法（如 Dupont et al. 2021; Strümpler et al. 2022）（Figure 7）。

2. **训练开销与探测范围的权衡**：训练时间随探测范围 $N_p$ 增加而线性增长，最高达 Instant NGP 的 2.6 倍（$N_p=2^4$, Table 2）。虽然小探测范围（$N_p \leq 2^4$）已足以获得良好压缩（Figure 5），但更大探测范围的收益递减，限制了在极端压缩场景下的应用。

3. **空间结构缺失**：空间哈希缺乏结构性，不利于依赖空间局部性的后处理（如生成建模、变换编码）。与树形细分结构（如八叉树）相比，Compact NGP 无法利用空间先验进行自适应稀疏分配。

4. **纹理压缩的专用性不足**：未采用量化与专用架构，在纹理压缩任务上性能低于 NTC（Vaidyanathan et al., SIGGRAPH 2023）（Table 4），表明通用方法在特定领域仍有改进空间。

5. **训练机制的次优性**：当前依赖 softmax 与直通估计器训练索引码本，未探索更稀疏或随机的梯度估计方法（如 sparsemax、Gumbel-softmax），可能导致索引效率未达最优。

### 5. 开放问题与未来方向

基于上述局限，本文提出以下开放问题：

1. **索引学习机制的改进**：能否用稀疏注意力机制（如 sparsemax、Gumbel-softmax）替代 softmax 直通估计器，以提升索引效率和训练稳定性？

2. **浮点量化与混合精度**：数据自适应的浮点量化是否能进一步减少特征码本和 MLP 参数的比特数，从而在极小模型尺寸下与纯 MLP 方法竞争？

3. **空间局部性的利用**：空间局部性是否可通过熵编码或邻近索引（如局部敏感哈希）更好地利用，从而在保持随机访问的同时提升压缩率？

4. **实际部署验证**：该方法在流式应用、游戏纹理压缩、实时光照缓存等实际场景的部署与性能如何？特别是推理速度优势（28.7 μs vs. ~10 μs）在实际渲染管线中的端到端影响需要进一步验证。

5. **索引结构的泛化**：能否将学习探测思想扩展到其他索引结构（如八叉树、$k$-平面）以实现更优的压缩-速度平衡？Figure 3 展示的统一索引函数框架为此提供了理论基础。

6. **多分辨率层级与 MLP 宽度的自适应选择**：Figure 9 和 Figure 10 表明，默认层级 $L=16$ 和 MLP 宽度 64 在几百 kB 的实用范围内表现良好，但更小尺寸下更低层级更优。如何根据目标文件大小自动选择这些超参数仍是一个开放问题。

## 原文 PDF

![[paperPDFs/SIGGRAPH_ASIA_2023/Compact_Neural_Graphics_Primitives_with_Learned_Hash_Probing.pdf]]
