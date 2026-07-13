---
title: "MSPT: Efficient Large-Scale Physical Modeling via Parallelized Multi-Scale Attention"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/MSPT_Efficient_Large_Scale_Physical_Modeling_via_Parallelized_Multi_Scale_Attention.pdf
project_link: null
code_link: https://github.com/thuml/Neural-Solver-Library
aliases:
- MSPTM
- MSPT
tags:
- CVPR_2026
- topic/vision_multimodal_applications/physics
- topic/vision_multimodal_applications
core_operator: 并行化多尺度注意力（PMSA）机制：将点云划分为局部patches并在patch内进行自注意力，同时通过池化形成超节点（supernodes）实现跨patch全局信息交换，将复杂度从O(N^2)降至O(NL + N^2 Q/L)，通过调节patch大小L和超节点数量Q控制局部与全局交互的权衡。
primary_logic: 通过球树（ball tree）在非结构网格上生成空间紧凑的patches，再经池化产生少量超节点作为全局上下文，将局部精细建模和全局长程通信统一到单个注意力操作中，避免压缩瓶颈并保持几何一致性，从而在标准PDE和CFD基准上以更低显存和计算成本实现SOTA精度。
claims:
- MSPT在6项标准PDE基准中有4项取得最优，在Navier-Stokes上相对第二最佳模型降低30%误差，在Elasticity上略低于纯局部模型Erwin但大幅优于Transolver。
- 在ShapeNet-Car空气动力学任务上，MSPT以单分支架构达到最佳体积场误差1.89和阻力误差0.98，均优于Transolver和其他单分支模型，且仅需一半的GPU内存。
- MSPT在百万点规模下内存和延迟均显著低于Transolver，峰值内存约22GB（500k点）且近乎线性增长，证明其近线性复杂度的实际可行性。
- Elasticity 上 Relative L2 Error (×10⁻²) = 0.48
---

# MSPT: Efficient Large-Scale Physical Modeling via Parallelized Multi-Scale Attention

> [!tip] 核心洞察
> 通过球树（ball tree）在非结构网格上生成空间紧凑的patches，再经池化产生少量超节点作为全局上下文，将局部精细建模和全局长程通信统一到单个注意力操作中，避免压缩瓶颈并保持几何一致性，从而在标准PDE和CFD基准上以更低显存和计算成本实现SOTA精度。

| 字段 | 内容 |
|------|------|
| 中文题名 | MSPT：通过并行化多尺度注意力实现高效大规模物理建模 |
| 英文题名 | MSPT: Efficient Large-Scale Physical Modeling via Parallelized Multi-Scale Attention |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2512.01738) · [Code](https://github.com/thuml/Neural-Solver-Library) |
| Topic | #topic/vision_multimodal_applications/physics #topic/vision_multimodal_applications |
| Method | Multi-Scale Patch Transformer (MSPT) |
| Dataset | Elasticity, Plasticity, Airfoil, Pipe |

> [!tip] 效果简介
> - Elasticity 上，Relative L2 Error (×10⁻²) 0.48 vs 0.34 (Erwin) (-41% (worse than Erwin but better than Transolver))。
> - Plasticity 上，Relative L2 Error (×10⁻²) 0.10 vs 0.12 (Transolver) (+17%)。
> - Airfoil 上，Relative L2 Error (×10⁻²) 0.51 vs 0.53 (Transolver) (+4%)。

## 概要

### 问题背景

物理系统的数值仿真——从固体力学到计算流体动力学（CFD）——是工程设计的核心支柱。随着深度学习的发展，以神经算子为代表的代理模型在加速偏微分方程（PDE）求解方面展现出巨大潜力。其中，基于Transformer的物理求解器凭借其强大的上下文建模能力受到了广泛关注。然而，**现有Transformer求解器在捕获百万级空间点的细粒度局部相互作用和长距离全局依赖时，面临二次计算复杂度的瓶颈**，使得大规模工业级仿真难以在单GPU上高效训练。典型代表如**Transolver**通过固定数量的全局切片压缩域信息，虽然降低了计算开销，但压缩过程不可避免地丢失了局部细节，且其复杂度仍难以线性扩展至百万点规模。

### 核心方法

本文提出**Multi-Scale Patch Transformer（MSPT）**，其核心是**并行化多尺度注意力（Parallelized Multi-Scale Attention, PMSA）**机制。PMSA将非结构网格上的点云通过球树（ball tree）划分为空间紧凑的局部patches，在每个patch内执行自注意力以捕获精细局部相互作用；同时，每个patch通过池化产生少量超节点（supernodes），所有patch的超节点拼接形成全局上下文，与局部token共同参与同一注意力操作，实现跨patch的全局长程信息交换。这一设计将复杂度从 $O(N^2)$ 降至 $O(NL + N^2 Q/L)$，通过调节patch大小 $L$ 和超节点数量 $Q$ 可灵活控制局部与全局交互的权衡，避免了压缩瓶颈并保持了几何一致性。

### 方法定位

在现有方法谱系中，MSPT处于**局部-全局统一注意力**的新位置：

- 相较于**FNO**（谱域积分算子）和**GINO**（图网络+积分算子），MSPT直接处理非结构点云，无需规则网格或图构建；
- 相较于**Transolver**（固定全局切片压缩），MSPT通过超节点池化实现无压缩瓶颈的全局通信，且计算复杂度更低；
- 相较于**Erwin**（纯局部球树注意力），MSPT在保持局部保真度的同时引入了高效全局信息交换；
- 相较于**AB-UPT**（面向CFD的表面-体积双分支架构），MSPT以单分支设计即取得有竞争力的表现，且分支扩展被作为开放方向提出。

### 主要结果

MSPT在6项标准PDE基准（Elasticity、Plasticity、Airfoil、Pipe、Navier-Stokes、Darcy）中有4项取得最优性能，在Navier-Stokes上相对第二最佳模型降低30%误差（Table 2）。在工业级ShapeNet-Car空气动力学任务上，MSPT以单分支架构达到最佳体积场误差1.89和阻力误差0.98，均优于Transolver等单分支模型，且仅需约一半的GPU内存（Table 3, Figure 5）。效率方面，MSPT在百万点规模下峰值内存和延迟均显著低于Transolver，500k点时峰值内存约22 GB且近乎线性增长，验证了其近线性复杂度的实际可行性（Figure 1, Table 8）。



### 物理仿真中偏微分方程的数值求解瓶颈

偏微分方程（PDE）是描述流体力学、结构力学、电磁学等物理现象的核心数学工具。传统数值方法（如有限元法、有限体积法）虽然精度可靠，但对复杂几何和边界条件的每一次仿真都需要昂贵的网格生成与迭代求解，单个工业级案例（如汽车外气动分析）往往需要数小时甚至数天的计算时间。近年来，基于深度学习的神经算子——特别是以傅里叶神经算子（**FNO**）和Transformer为代表的模型——试图直接从数据中学习PDE的解映射，在推理阶段实现秒级预测，从而绕开传统求解器的迭代过程。

然而，当仿真规模从数千节点扩展到百万级工业网格时，现有深度学习求解器面临一个根本性的计算瓶颈。

### Transformer物理求解器的二次复杂度困境

Transformer凭借其自注意力机制在自然语言处理和计算机视觉中取得了巨大成功，其核心优势在于能够动态建模任意两点之间的长程依赖关系。这一特性对于物理仿真同样至关重要：湍流中的涡结构、弹性体中的应力集中、空气动力学中的尾流区域，都需要同时捕获局部精细的梯度变化和全局的物理耦合。

但标准自注意力的计算复杂度为 $\mathcal{O}(N^2)$，其中 $N$ 是空间离散点的数量。当 $N$ 达到数十万甚至百万量级时，单个注意力层的计算量和显存占用将超出单GPU的承载能力。这一瓶颈直接将Transformer物理求解器限制在小规模或粗粒度的仿真任务上，无法满足工业级高保真仿真的需求。

### 现有方案的局部-全局权衡困境

针对二次复杂度问题，研究者提出了多种折中方案，但均存在明显的结构缺陷：

- **纯局部模型**（如基于图网络或局部注意力的方法）将每个点的交互限制在邻域范围内，虽然计算高效且能保留局部细节，但缺乏跨区域的全局信息交换通道，难以建模大尺度的物理耦合现象（如远场压力传播）。

- **全局压缩模型**（如 **Transolver**）通过学习固定数量的全局切片（slices）来压缩域信息，将复杂度降至线性。但这种硬压缩（hard bottleneck）将整个物理场的全局上下文强行挤入有限维度的表示中，不可避免地丢失空间细节，导致局部精度下降——在弹性力学等对局部应力敏感的任务中尤为明显。

- **双分支架构**（如 **AB-UPT**）通过分离表面与体积分支并引入交叉注意力，在计算流体力学（CFD）任务上取得了进展，但其分支设计针对特定物理边界定制，缺乏通用性，且双分支间的通信机制仍依赖全局操作，未能从根本上解决大规模点云的高效全局交互问题。

### 核心动机：统一局部精细建模与全局高效通信

上述分析揭示了一个关键矛盾：**局部保真度**要求模型在细粒度上操作，而**全局通信**要求模型跨越整个域交换信息。现有方法或将两者割裂（先局部后全局的串行设计），或通过压缩牺牲一方（全局压缩丢失细节），始终未能在单个统一的注意力操作中同时实现高效局部建模和全局长程交互。

MSPT（Multi-Scale Patch Transformer）正是在这一矛盾中找到了突破口。其核心动机是：**能否通过一种并行化的多尺度注意力机制，让局部patch内的精细自注意力和跨patch的全局上下文交换在同一操作中完成，从而在保持近线性复杂度的同时，避免压缩瓶颈和信息丢失？**

这一动机直接催生了三个关键设计选择：
1. **球树划分**：在非结构网格上生成空间紧凑的局部patches，保证局部注意力的几何一致性；
2. **超节点池化**：从每个patch中压缩出少量代表性token作为全局上下文载体，而非对整个域进行硬压缩；
3. **并行多尺度注意力（PMSA）**：将局部token与全局超节点拼接后统一送入多头注意力，使局部-局部和局部-全局交互在同一个注意力矩阵中并行计算。

通过这种方式，MSPT旨在打破“保局部必失全局、求全局必损效率”的困境，为大规模物理建模提供一个可扩展且精度领先的统一框架。



## 核心方法与创新机理

MSPT的核心创新在于通过**并行化多尺度注意力（Parallelized Multi-Scale Attention, PMSA）**机制，将局部精细建模与全局信息交换统一到单个注意力操作中，从而在保持模型表达力的同时，将计算复杂度从标准Transformer的 $O(N^2)$ 降至近线性。

### 关键改进槽位

#### 1. 注意力模式：局部-全局并行化

传统Transformer物理求解器要么采用全局自注意力（复杂度 $O(N^2)$，无法扩展到百万级点云），要么通过固定大小的压缩切片实现全局通信（如Transolver），牺牲了局部细节的保真度。MSPT的PMSA机制将点云划分为 $K$ 个大小为 $L$ 的局部patch，在每个patch内执行自注意力以捕获细粒度局部相互作用；同时，所有patch共享一组通过池化得到的 $Q$ 个超节点（supernodes）作为全局上下文，实现跨patch的信息交换。

这一设计的关键在于**局部注意力和全局注意力在同一操作中并行执行**。具体而言，对每个patch $k$，将其 $L$ 个局部token与 $KQ$ 个全局超节点拼接后送入多头注意力：

$$\boxed { \mathbf { H } ^ { \prime } = \mathrm { P M S A } ( \mathbf { H } ) = \bigoplus _ { k = 1 } ^ { K } \Pi _ { \mathrm { l o c } } \mathrm { M H A } \left( \left[ \begin{array} { l } { \mathbf { H } _ { k } } \\ { \mathbf { S } } \end{array} \right] \right) }$$

其中 $\Pi_{\mathrm{loc}}$ 仅保留前 $L$ 行作为更新后的局部特征。增强注意力矩阵自然分解为四个块：

$$\mathbf { A } _ { k } = \left[ \begin{array} { l l } { \mathbf { A } _ { k } ^ { \mathrm { l o c } , \mathrm { l o c } } } & { \mathbf { A } _ { k } ^ { \mathrm { l o c } , \mathrm { g l o b } } } \\ { \mathbf { A } _ { k } ^ { \mathrm { g l o b } , \mathrm { l o c } } } & { \mathbf { A } _ { k } ^ { \mathrm { g l o b } , \mathrm { g l o b } } } \end{array} \right]$$

局部token的更新由局部-局部和局部-全局两项组成：

$$\mathbf { H } _ { k } ^ { \prime } = \mathbf { A } _ { k } ^ { \mathrm { l o c , l o c } } \mathbf { V } _ { k } ^ { \mathrm { l o c } } + \mathbf { A } _ { k } ^ { \mathrm { l o c , g l o b } } \mathbf { V } _ { k } ^ { \mathrm { g l o b } }$$

这种设计将复杂度降至 $O(NL + N^2 Q/L)$，通过调节patch大小 $L$ 和超节点数量 $Q$ 可灵活控制局部与全局交互的权衡。实验表明，$Q=1$ 已能提供足够的全局上下文（Figure 4），而更大的 $K$（更细的划分）在ShapeNet-Car上可进一步降低测试损失（Table 5，$K=1024$ 时最优损失5.99）。

#### 2. 域划分策略：基于球树的空间紧凑划分

与Transolver的固定切片或随机划分不同，MSPT采用**球树（Ball Tree）**在非结构网格上生成空间紧凑的连续patches。球树基于点坐标构建平衡树结构，按深度优先遍历叶子节点顺序生成空间局部排列，连续块自然形成patches。该树结构在首个MSPT块前计算一次并跨层复用，避免了逐层重建的开销。

消融实验验证了这一策略的有效性：球树DFS排序产生的patch空间离散度（$s_k$，patch内均方半径）中位数比随机排列低1-2个数量级（Table 6，如Elasticity上0.0065 vs 0.2035；Figure 6展示了Darcy数据集上的分布直方图），确保了patches内的点具有真实的几何邻近性，而非随机的空间散布。

#### 3. 全局信息聚合：超节点池化

MSPT通过三种可选的池化策略将每个patch内的 $L$ 个token压缩为 $Q$ 个超节点：

- **均值池化**：$\mathbf { S } _ { k } ^ { q } = \frac { 1 } { L / Q } \sum _ { j = 1 } ^ { L / Q } ( \mathbf { H } _ { k } ^ { q } ) _ { j }$
- **最大池化**：$\mathbf { S } _ { k } ^ { q } = \operatorname* { m a x } _ { j = 1 } ^ { L / Q } ( \mathbf { H } _ { k } ^ { q } ) _ { j }$
- **可学习投影**：$\mathbf { S } _ { k } = \mathbf { W } _ { \mathrm { p o o l } } ^ { \top } \mathbf { H } _ { k } , \quad \mathbf { W } _ { \mathrm { p o o l } } \in \mathbb { R } ^ { L \times Q }$

所有patch的超节点沿行拼接形成全局上下文矩阵 $\mathbf{S} \in \mathbb{R}^{(KQ) \times F}$。消融实验（Figure 4）表明，均值池化在所有 $Q$ 配置下均优于最大池化和可学习投影，且 $Q=1$ 即可提供足够的全局信息，体现了设计的简洁性和有效性。

### 与基线方法的本质差异

| 维度 | Transolver | Erwin | MSPT |
|------|-----------|-------|------|
| 局部建模 | 通过固定切片间接实现 | 纯局部球树注意力 | patch内自注意力 |
| 全局通信 | 学习到的固定压缩切片 | 缺乏高效机制 | 超节点并行全局注意力 |
| 复杂度 | 受切片大小限制 | 纯局部 $O(NL)$ | $O(NL + N^2 Q/L)$，可调节 |
| 几何一致性 | 切片可能跨越几何不连续区域 | 球树保证空间紧凑 | 球树保证空间紧凑 |

MSPT的核心洞察在于：**通过球树划分保证局部patch的几何一致性，再通过超节点池化将局部精细建模和全局长程通信统一到单个注意力操作中**，避免了Transolver的压缩瓶颈和Erwin的全局通信缺失，从而在标准PDE和CFD基准上以更低显存和计算成本实现SOTA精度。



MSPT 的整体架构遵循“嵌入→划分→多尺度注意力编码→任务头”的端到端管线，核心设计目标是在非结构网格上以近线性复杂度实现局部精细建模与全局长程通信的统一。

### 输入嵌入与预处理

给定输入点集 $\mathcal{X} = \{\mathbf{x}_i\}_{i=1}^{N}$，每个点携带坐标及可选物理属性（如边界条件标记）。嵌入阶段将几何描述符与坐标拼接后通过共享 MLP 映射到 $F$ 维隐空间，得到初始 token 矩阵 $\mathbf{H}^{(0)} \in \mathbb{R}^{N \times F}$。当 $N$ 不能被 patch 数量 $K$ 整除时，对点集进行零填充以保证划分均匀性（Section 3.2, Appendix A.3）。

### 球树划分

在首个 MSPT 块之前，基于点坐标构建平衡球树（Ball Tree），按深度优先遍历（DFS）叶子节点的顺序生成空间局部排列。连续 $L$ 个点组成一个 patch，共形成 $K$ 个非重叠 patch $\{\mathcal{P}_k\}_{k=1}^{K}$，每个 patch 包含 $L = \lceil N/K \rceil$ 个点。该树结构仅计算一次并在所有后续块中复用，避免了逐层重新划分的开销（Section 3.2, Appendix A.1）。球树 DFS 排序产生的 patch 空间离散度中位数比随机排列低 1–2 个数量级（如 Elasticity 上 0.0065 vs 0.2035），验证了划分的局部紧凑性（Table 6, Figure 6）。

### 超节点池化

对每个 patch $\mathcal{P}_k$ 内的 $L$ 个 token $\mathbf{H}_k \in \mathbb{R}^{L \times F}$，通过池化操作压缩为 $Q$ 个超节点（supernodes）$\mathbf{S}_k \in \mathbb{R}^{Q \times F}$。支持三种池化方式：

- **均值池化**：将 patch 内点均分为 $Q$ 个子块，每个子块内取均值：
  $$\mathbf{S}_k^q = \frac{1}{L/Q} \sum_{j=1}^{L/Q} (\mathbf{H}_k^q)_j$$
- **最大池化**：每个子块内取最大值：
  $$\mathbf{S}_k^q = \max_{j=1}^{L/Q} (\mathbf{H}_k^q)_j$$
- **可学习线性投影**：通过可学习矩阵将 $L$ 个 token 直接映射为 $Q$ 个超节点：
  $$\mathbf{S}_k = \mathbf{W}_{\mathrm{pool}}^{\top} \mathbf{H}_k, \quad \mathbf{W}_{\mathrm{pool}} \in \mathbb{R}^{L \times Q}$$

所有 patch 的超节点沿行拼接为全局上下文矩阵 $\mathbf{S} = [\mathbf{S}_1; \mathbf{S}_2; \cdots; \mathbf{S}_K] \in \mathbb{R}^{(KQ) \times F}$（Section 3.1 Eq.(1)-(2), Section 3.2 Eq.(10)-(11)）。

### 并行多尺度注意力（PMSA）

PMSA 是 MSPT 的核心算子，将局部 patch 特征与全局超节点拼接后统一执行多头自注意力。对第 $k$ 个 patch，构造增强输入：
$$\tilde{\mathbf{H}}_k = \begin{bmatrix} \mathbf{H}_k \\ \mathbf{S} \end{bmatrix} \in \mathbb{R}^{(L + KQ) \times F}$$
经多头注意力后，注意力矩阵自然分解为四个块：
$$\mathbf{A}_k = \begin{bmatrix} \mathbf{A}_k^{\mathrm{loc,loc}} & \mathbf{A}_k^{\mathrm{loc,glob}} \\ \mathbf{A}_k^{\mathrm{glob,loc}} & \mathbf{A}_k^{\mathrm{glob,glob}} \end{bmatrix}$$
仅保留前 $L$ 行作为更新后的局部特征：
$$\mathbf{H}_k' = \mathbf{A}_k^{\mathrm{loc,loc}} \mathbf{V}_k^{\mathrm{loc}} + \mathbf{A}_k^{\mathrm{loc,glob}} \mathbf{V}_k^{\mathrm{glob}}$$
最终将所有 patch 结果堆叠：
$$\boxed{\mathbf{H}' = \mathrm{PMSA}(\mathbf{H}) = \bigoplus_{k=1}^{K} \Pi_{\mathrm{loc}} \mathrm{MHA}\left(\begin{bmatrix} \mathbf{H}_k \\ \mathbf{S} \end{bmatrix}\right)}$$
其中 $\Pi_{\mathrm{loc}}$ 表示仅保留前 $L$ 行的投影操作（Section 3.1 Eq.(3)-(9)）。PMSA 的复杂度为 $O(NL + N^2 Q/L)$，通过调节 $L$ 和 $Q$ 在局部精细度与全局通信之间取得平衡。

### MSPT 块堆叠

每个 MSPT 块依次执行：
$$\widehat{\mathbf{H}}^{(\ell)}, \mathbf{S}^{(\ell)} = \mathrm{PMSA}\big(\mathrm{LN}(\mathbf{H}^{(\ell-1)}), \mathbf{S}^{(\ell-1)}\big) + \big(\mathbf{H}^{(\ell-1)}, \mathbf{0}\big)$$
$$\mathbf{H}^{(\ell)} = \mathrm{FFN}\big(\mathrm{LN}(\widehat{\mathbf{H}}^{(\ell)})\big) + \widehat{\mathbf{H}}^{(\ell)}$$
其中 $\mathbf{S}^{(0)}$ 初始化为零矩阵，PMSA 同时更新局部 token 和超节点。堆叠 $B$ 个块逐步精炼点特征，最后一个块的 FFN 替换为任务特定头（如预测压力场或速度场），输出最终物理场（Section 3.2, Eq.(12)）。

### 数据流总结

整个管线的数据流为：**原始点云 → 坐标/几何嵌入 → 球树划分（一次性） → [超节点池化 → PMSA → FFN] × B → 任务头 → 预测场**。球树划分在首个块前完成并跨层复用，超节点在每个块内重新池化以反映更新后的特征分布，局部 token 和全局超节点在 PMSA 中同步更新，形成紧密耦合的局部-全局通信闭环。

### 补充图表

![[assets/figures/papers/paper_list_l22_https_arxiv_org_abs_2512_01738/figures/001_Figure_1.jpg]]
*Figure 1: Parallelized Multi-Scale Attention mechanism. Each patch performs local self-attention, while pooled supernodes exchange information globally across patches in parallel. Peak memory (GB) and latency (ms) on 500k points with 256 slices (Transolver) and 256 patches (MSPT)*



### 3.1 并行多尺度注意力（PMSA）

MSPT的核心创新在于将局部精细建模与全局长程通信统一到单个注意力操作中。给定输入点云特征 $\mathbf{H} \in \mathbb{R}^{N \times F}$（$N$ 为点数，$F$ 为特征维度），首先将其划分为 $K$ 个非重叠的局部patch，每个patch包含 $L = N/K$ 个点，记第 $k$ 个patch的特征为 $\mathbf{H}_k \in \mathbb{R}^{L \times F}$。

**超节点池化**。对每个patch $k$，通过池化操作将其 $L$ 个局部token压缩为 $Q$ 个超节点（supernodes），形成该patch的粗粒度全局摘要：

$$\mathbf{S}_k = \mathrm{Pool}(\mathbf{H}_k) \in \mathbb{R}^{Q \times F}$$

将所有patch的超节点沿行拼接，得到全局上下文矩阵：

$$\mathbf{S} = [\mathbf{S}_1; \mathbf{S}_2; \cdots; \mathbf{S}_K] \in \mathbb{R}^{(KQ) \times F}$$

**并行注意力计算**。将每个patch的局部特征 $\mathbf{H}_k$ 与全局超节点 $\mathbf{S}$ 拼接后送入多头注意力（MHA）：

$$\mathbf{H}'_k = \Pi_{\mathrm{loc}} \mathrm{MHA}\left( \begin{bmatrix} \mathbf{H}_k \\ \mathbf{S} \end{bmatrix} \right)$$

其中 $\Pi_{\mathrm{loc}}$ 表示仅保留输出的前 $L$ 行（即局部token的更新），丢弃超节点对应的输出。对所有 $K$ 个patch并行执行此操作后堆叠结果，得到PMSA的紧凑形式：

$$\boxed{\mathbf{H}' = \mathrm{PMSA}(\mathbf{H}) = \bigoplus_{k=1}^{K} \Pi_{\mathrm{loc}} \mathrm{MHA}\left( \begin{bmatrix} \mathbf{H}_k \\ \mathbf{S} \end{bmatrix} \right)}$$

**注意力矩阵的块分解**。上述拼接操作使得注意力矩阵自然分解为四个功能块：

$$\mathbf{A}_k = \begin{bmatrix} \mathbf{A}_k^{\mathrm{loc,loc}} & \mathbf{A}_k^{\mathrm{loc,glob}} \\ \mathbf{A}_k^{\mathrm{glob,loc}} & \mathbf{A}_k^{\mathrm{glob,glob}} \end{bmatrix}$$

其中 $\mathbf{A}_k^{\mathrm{loc,loc}} \in \mathbb{R}^{L \times L}$ 捕获patch内的局部交互，$\mathbf{A}_k^{\mathrm{loc,glob}} \in \mathbb{R}^{L \times KQ}$ 建模局部token到全局超节点的信息流动。更新后的局部特征由两项之和构成：

$$\mathbf{H}_k' = \mathbf{A}_k^{\mathrm{loc,loc}} \mathbf{V}_k^{\mathrm{loc}} + \mathbf{A}_k^{\mathrm{loc,glob}} \mathbf{V}_k^{\mathrm{glob}}$$

**复杂度分析**。PMSA的计算复杂度为 $O(NL + N^2 Q/L)$。第一项 $O(NL)$ 来自所有patch内局部自注意力的总和（每个patch复杂度 $O(L^2)$，共 $K$ 个patch，$K L^2 = NL$）；第二项 $O(N^2 Q/L)$ 来自局部token与全局超节点的交叉注意力。通过调节patch大小 $L$ 和超节点数量 $Q$，可在局部保真度与全局通信之间灵活权衡——当 $L$ 较小、$Q$ 固定时，复杂度趋近线性。

### 3.2 超节点池化策略

论文提供了三种池化方法，将patch内 $L$ 个token压缩为 $Q$ 个超节点。

**均值池化**。将patch $k$ 均匀划分为 $Q$ 个子块，每个子块包含 $L/Q$ 个点，对第 $q$ 个子块内点的特征求均值：

$$\mathbf{S}_k^q = \frac{1}{L/Q} \sum_{j=1}^{L/Q} (\mathbf{H}_k^q)_j$$

**最大池化**。对第 $q$ 个子块内点的特征逐元素取最大值：

$$\mathbf{S}_k^q = \operatorname*{max}_{j=1}^{L/Q} (\mathbf{H}_k^q)_j$$

**可学习线性投影**。通过可学习的线性变换直接将patch内 $L$ 个token映射为 $Q$ 个超节点：

$$\mathbf{S}_k = \mathbf{W}_{\mathrm{pool}}^{\top} \mathbf{H}_k, \quad \mathbf{W}_{\mathrm{pool}} \in \mathbb{R}^{L \times Q}$$

消融实验（Figure 4）表明，均值池化在所有 $Q$ 配置下均优于最大池化和线性投影，且 $Q=1$ 已能提供足够的全局上下文，验证了极简池化策略的有效性。

### 3.3 球树划分与空间局部性

对于非结构网格，MSPT采用**平衡球树**（Ball Tree）进行域划分。球树基于点坐标递归地将空间分割为嵌套的超球体，保证每个叶子节点包含近似相等数量的点。按深度优先遍历（DFS）顺序提取叶子节点，将连续块组织为空间紧凑的patches。

该划分策略的关键性质是**空间局部性**：同一patch内的点在物理空间上邻近，使得patch内自注意力能有效捕获细粒度局部相互作用。定量评估（Table 6）显示，球树DFS排序产生的patch空间离散度 $s_k$（patch内点集的均方半径）中位数比随机排列低1-2个数量级（如Elasticity上0.0065 vs 0.2035），验证了划分的局部紧凑性。

球树结构仅在首个MSPT块前计算一次（复杂度 $O(N \log N)$），并在所有后续块中复用，避免了逐层重建的开销。

### 3.4 MSPT块与整体架构

每个MSPT块由以下组件串联构成：

$$\widehat{\mathbf{H}}^{(\ell)}, \mathbf{S}^{(\ell)} = \mathrm{PMSA}\big(\mathrm{LN}(\mathbf{H}^{(\ell-1)}), \mathbf{S}^{(\ell-1)}\big) + \big(\mathbf{H}^{(\ell-1)}, \mathbf{0}\big)$$

$$\mathbf{H}^{(\ell)} = \mathrm{FFN}\big(\mathrm{LN}(\widehat{\mathbf{H}}^{(\ell)})\big) + \widehat{\mathbf{H}}^{(\ell)}$$

其中 $\mathrm{LN}$ 为层归一化，$\mathrm{FFN}$ 为逐点前馈网络，超节点 $\mathbf{S}^{(\ell-1)}$ 初始化为零矩阵。第 $\ell$ 块先通过PMSA同时更新局部特征和超节点（残差连接中局部特征加自身、超节点加零），再经过FFN和第二次残差连接。

整体架构堆叠 $B$ 个MSPT块逐步精炼点特征。输入嵌入阶段，将点坐标与几何描述符（如到参考网格的距离）拼接后通过共享MLP映射到隐空间。最后一块的FFN替换为任务特定头（如预测压力场或速度场），输出最终物理场。



## 实验与关键发现

### 核心实验设置

MSPT在两类基准上接受检验：六项标准PDE基准（Elasticity、Plasticity、Airfoil、Pipe、Navier-Stokes、Darcy）覆盖从972点到16,641点的结构化与非结构化网格，以及两项工业级CFD基准——ShapeNet-Car（平均32,186点）和AhmedML（约两千万点）。所有标准PDE实验在统一的Neural-Solver-Library框架下运行，优化器与学习率等超参保持一致；CFD任务中，为与AB-UPT公平对比，采用其原配的LION优化器配置。完整训练与模型配置见Table 7。

### 标准PDE基准结果

Table 2汇总了六项标准PDE基准上的相对L2误差。MSPT在六项中有四项取得最优：Plasticity（0.10）、Airfoil（0.51）、Pipe（0.31）和Navier-Stokes（6.32）。其中Navier-Stokes上的提升最为显著，相对第二最佳模型Transolver降低30%误差，表明PMSA在强非线性流场中对长程涡结构的捕获能力优于固定切片压缩方案。在Elasticity上，MSPT（0.48）低于纯局部模型Erwin（0.34），但大幅优于Transolver（0.65），说明球树局部patch在保持细粒度应变场保真度上优于全局切片，但尚不及完全舍弃全局通信的纯局部注意力。Darcy（0.63 vs Transolver 0.57）是MSPT唯一弱于Transolver的基准，推测该问题的全局渗透率场对压缩瓶颈不敏感，而patch划分可能轻微牺牲了跨区域连续性。

定性误差分布（Figure 3、Figure 7）进一步验证了上述判断：在Pipe和Navier-Stokes的壁面边界层与尾流区，MSPT的逐点误差显著低于Transolver，且未出现切片边界处的伪影。

![[assets/figures/papers/paper_list_l22_https_arxiv_org_abs_2512_01738/figures/004_Figure_3.jpg]]
*Figure 3: Examples of relative L2 error maps for the Pipe, Navier-Stokes and ShapeNet Car datasets. For ShapeNet Car we show surface-pressure errors. See Appendix B for more visualizations*

### CFD基准结果

在ShapeNet-Car空气动力学任务上（Table 3），MSPT以单分支架构达到体积场相对L2误差1.89，优于Transolver（2.07）和所有其他单分支模型；阻力系数误差0.98同样最优。表面场误差（7.41）与Transolver（7.45）基本持平，表明PMSA在耦合体积与表面物理量上仍有提升空间。Spearman秩相关系数ρ_D方面，MSPT达到0.939，显著高于Transolver（0.927），证明其预测的阻力排序更可靠，对气动外形优化中的设计筛选具有实际价值。

![[assets/figures/papers/paper_list_l22_https_arxiv_org_abs_2512_01738/figures/007_Table_3.jpg]]
*Table 3: Performance on ShapeNet Car. Relative*

在更大规模的AhmedML基准上（Table 4），MSPT在体积场（2.04 vs Transolver 2.05）和表面场（3.22 vs Transolver 3.45）上均取得最优单分支结果，表面场提升达6.67%，说明PMSA的多尺度通信机制在千万级点规模下仍能有效运作。

![[assets/figures/papers/paper_list_l22_https_arxiv_org_abs_2512_01738/figures/006_Table_4.jpg]]
*Table 4: Performance on AhmedML. Relative*

值得注意的是，双分支专用架构AB-UPT在两项CFD任务上整体表现更优（ShapeNet-Car体积1.16，表面4.82），但其原始训练流水线未公开，在Neural-Solver-Library下的复现结果出现显著回退（体积2.51），因此主表中保留了原论文数值并提供了复现数据供参考（Table 10）。这一公平性隐患需要读者在解读单分支与双分支架构的绝对差距时审慎对待。

### 效率分析

Figure 1和Figure 5展示了MSPT的效率优势。在500k点规模下，MSPT峰值GPU内存约22 GB，显著低于Transolver，且内存增长近乎线性；前向传播延迟在patch数K=128时达到平衡，可在0.084 s内处理百万点批次。Table 8进一步显示，在Elasticity上MSPT以更低的参数量和训练时间达到与Transolver可比或更优的精度，在ShapeNet-Car上以一半的GPU内存取得更高的ρ_D。这些结果直接验证了PMSA近线性复杂度的实际可行性。

### 消融实验

**Patch数量K的影响**（Table 5）：在ShapeNet-Car上变化K从32至1024，测试损失呈非单调变化，K=1024时获得最优损失5.99。更细的划分增强了局部建模能力，但过细会导致patch内点数不足、超节点信息稀释，需在局部精度与全局上下文间权衡。

**池化方法与超节点数Q**（Figure 4）：三种池化策略中，均值池化在所有Q配置下均优于最大池化和可学习线性投影，且Q=1已能提供足够的全局上下文，增加Q并未带来持续增益。这表明简单的均值聚合足以捕获patch间必要的全局信息，过度参数化反而引入噪声。

**球树划分质量**（Table 6、Figure 6）：以patch内点的均方半径s_k度量空间离散度，球树DFS排序产生的中位数s_k比随机排列低1-2个数量级（如Elasticity上0.0065 vs 0.2035），验证了划分的局部紧凑性。Figure 6在Darcy上的直方图进一步显示，球树划分的s_k集中在极小值区域，而随机排列呈长尾分布，直观证明了球树对非结构网格的几何保持能力。

### 失败模式与局限性

1. **静态几何假设**：MSPT目前仅评估了静态或固定时间的物理场预测，球树划分在每个新输入样本上需要重建（O(N log N)），对动态网格或时变几何的推理延迟可能成为瓶颈。
2. **池化策略的任务敏感性**：均值池化虽在多数任务中表现最佳，但在Darcy等全局渗透率主导的问题上可能丢失关键长程信息，尚缺乏自适应选择机制。
3. **与双分支架构的差距**：在CFD表面场预测上，单分支MSPT与专用双分支架构（如AB-UPT）仍有差距，分支扩展仅停留在概念阶段，未提供实现和实验验证。
4. **复现性隐患**：Transolver++和AB-UPT在统一框架下的复现结果与原报告存在显著偏差（Table 9、Table 10），这一现象在AB-UPT的工作中亦有报告，提示当前PDE求解器领域的公平对比协议尚不成熟，部分性能声明可能受框架、随机种子或超参数差异的显著影响。

### 补充图表

![[assets/figures/papers/paper_list_l22_https_arxiv_org_abs_2512_01738/figures/005_Table_2.jpg]]
*Table 2: Performance comparison on standard benchmarks. Relative*

![[assets/figures/papers/paper_list_l22_https_arxiv_org_abs_2512_01738/figures/008_Figure_5.jpg]]
*Figure 5: Peak GPU memory usage (top) and wall-clock runtime per forward pass (bottom) as a function of the number of patches, across several input resolutions. Runtime is measured end-to-end and includes preprocessing (ball-tree construction, permutation, and padding). Colors correspond to the input resolution (total number of points), as indicated by the color bar*

![[assets/figures/papers/paper_list_l22_https_arxiv_org_abs_2512_01738/figures/010_Figure_4.jpg]]
*Figure 4: Study of pooling method and number of supernode tokens Q per patch. We report the test loss, defined as*

![[assets/figures/papers/paper_list_l22_https_arxiv_org_abs_2512_01738/figures/009_Table_5.jpg]]
*Table 5: ShapeNet-Car test loss (see Appendix A) as a function of the number of patches K*

![[assets/figures/papers/paper_list_l22_https_arxiv_org_abs_2512_01738/figures/012_Table_6.jpg]]
*Table 6: Patch-dispersion statistics across PDE benchmarks (mean squared radius within each patch; lower is better). We report the median, 90th percentile (p90), 99th percentile (p99), and maximum over patches for the ball-tree DFS ordering versus a random permutation, using the same number of patches K as in our main experiments*

![[assets/figures/papers/paper_list_l22_https_arxiv_org_abs_2512_01738/figures/011_Figure_6.jpg]]
*Figure 6: Histogram of per-patch spatial dispersion*

![[assets/figures/papers/paper_list_l22_https_arxiv_org_abs_2512_01738/figures/014_Table_8.jpg]]
*Table 8: Model efficiency comparison in Elasticity (Relative*

![[assets/figures/papers/paper_list_l22_https_arxiv_org_abs_2512_01738/figures/013_Table_7.jpg]]
*Table 7: Training and model configurations of MSPT. Here*



## 定位与知识库关联

### 物理场神经求解器的演化路径

MSPT 处于物理场神经求解器从“算子学习”向“大规模 Transformer”迁移的关键节点。早期工作以谱方法为核心，**FNO** 在傅里叶域学习积分核，实现了网格无关的算子映射，但其全局谱基难以捕获细粒度局部特征。**GINO** 将图网络与积分算子结合，增强了对非规则几何的适应性，但仍受限于显式的局部邻域聚合，缺乏高效的全局长程通信机制。

Transformer 的引入改变了这一格局。**OFormer** 将 PDE 求解形式化为序列到序列问题，**GNOT** 引入拓扑感知邻域，使注意力机制首次直接作用于非结构点云。然而，标准全局自注意力的 $O(N^2)$ 复杂度成为瓶颈，迫使后续工作寻求压缩策略。**Transolver** 提出了固定数量的全局切片来压缩域信息，将复杂度降至可控范围，但其物理压缩方式可能丢失局部细节，尤其在需要高保真局部建模的弹性力学等任务上表现不佳。**Erwin** 则走向另一极端，基于球树的纯局部注意力模型强调局部保真度，但缺乏高效的全局通信机制，在需要跨域协同的任务（如 Navier-Stokes 湍流）中受限。

MSPT 的核心贡献在于**统一了局部精细建模与全局信息交换**，避免了上述两条路线的各自缺陷。其并行多尺度注意力（PMSA）通过球树划分产生空间紧凑的 patches，在 patch 内执行局部自注意力，同时通过池化形成少量超节点作为全局上下文，将局部-局部和局部-全局交互纳入单次注意力操作。这一设计的关键洞察在于：**全局通信不需要压缩整个域，只需每个 patch 与少量全局代表交互即可实现有效的信息流动**。

### 与关键基线的结构对比

| 模型 | 注意力模式 | 域划分策略 | 全局信息聚合 | 复杂度 |
|------|-----------|-----------|-------------|--------|
| **Transolver** | 固定压缩切片注意力 | 无显式划分（全局点集） | 学习到的全局切片 | $O(N \cdot C)$，$C$ 为切片数 |
| **Erwin** | 纯局部注意力（球树） | 球树划分 | 无 | $O(N \cdot L)$，$L$ 为局部窗口大小 |
| **AB-UPT** | 双分支交叉注意力 | 表面/体积分支分离 | 交叉注意力与全局 token | $O(N^2)$（分支内） |
| **MSPT** | 局部 patch 内自注意力 + 全局超节点注意力（并行） | 平衡球树划分（空间紧凑） | 池化超节点拼接为全局上下文 | $O(NL + N^2 Q/L)$ |

MSPT 与 Transolver 的关键区别在于**物理划分与压缩方式**：Transolver 使用固定数量的全局切片，这些切片通过学习得到，缺乏显式的空间局部性约束；MSPT 的球树划分保证了每个 patch 的空间紧凑性（离散度中位数比随机排列低 1-2 个数量级），使局部注意力真正聚焦于物理相邻的点。与 Erwin 相比，MSPT 通过超节点机制补足了全局通信能力，在 Navier-Stokes 上相对 Erwin 降低 30% 误差即证明了这一补充的关键性。

在 CFD 领域，AB-UPT 代表了双分支架构的专用路线，分离表面和体积分支并通过交叉注意力交换信息。MSPT 以单分支架构在 ShapeNet-Car 上达到最佳体积场误差 1.89 和阻力误差 0.98，均优于 Transolver 和其他单分支模型，且仅需一半的 GPU 内存。但值得注意的是，MSPT 在表面场精度上仍略逊于 AB-UPT（表面 L2: 7.41 vs 6.64），表明双分支设计在表面-体积耦合建模上仍有优势。

### 适用边界与局限

**已验证的适用场景：**
- 静态或固定时间的物理场预测，覆盖标准 PDE 基准（弹性力学、塑性力学、翼型、管道流、Navier-Stokes、Darcy 流）和工业级 CFD 数据集（ShapeNet-Car、AhmedML）
- 非结构网格上的大规模点云，在百万点规模下保持近线性内存增长（500k 点峰值内存约 22 GB）
- 需要同时捕获局部细节和全局依赖的任务，如 Navier-Stokes 湍流预测

**已知局限与待验证边界：**

1. **动态几何与时变场**：MSPT 目前仅评估了静态或固定时间的物理场预测，尚未验证其在动态变化网格或时变几何上的有效性与效率。球树划分对每个新输入样本都需要重新构建（$O(N \log N)$），在推理阶段可能导致额外延迟，尤其对于超大规模实时应用。

2. **池化策略的任务敏感性**：超节点池化策略（均值/最大/可学习投影）对任务敏感，消融实验显示均值池化在所有配置下均优于最大池化和线性投影，且 $Q=1$ 已能提供足够的全局上下文。但尚缺乏自适应选择或学习的通用机制，可能在某些物理模式的全局通信中丢失关键信息。

3. **CFD 双分支扩展尚处概念阶段**：单分支 MSPT 与专门设计的双分支架构（如 AB-UPT）相比，在表面场和体积场的同时优化上仍有差距。论文提及可将分支思想应用于 MSPT 产生双分支变体，但仅停留在概念阶段，未提供实现和实验验证。

4. **超参数配置缺乏理论指导**：复杂度分析中二次项系数 $Q/L$ 依赖于手动选定的 $L$ 和 $Q$。消融实验显示 patch 数量 $K$ 在 ShapeNet-Car 上呈非单调变化（$K=1024$ 时获得最优损失 5.99），但缺少理论指导或自动化最优配置的方法。

5. **复现框架差异**：AB-UPT 原始训练流水线未公开，在 Neural-Solver-Library 统一框架下的复现结果与原报告存在偏差（如 ShapeNet-Car 上体积 L2 为 2.51 vs 1.16）。Transolver++ 在官方实现下复现同样出现显著性能回退（如 Elasticity 从 0.52 升至 1.54），这些差异在多大程度上源自训练框架、随机种子或超参数，尚无统一的公平对比协议。

### 开放问题与后续方向

1. **动态 patch 划分**：如何为 MSPT 设计动态 patch 划分策略，使其能够在线调整以适应随时间演化的几何或物理场？这直接关系到方法向非定常仿真（如湍流时序预测）的推广。

2. **双分支 MSPT 的验证**：双分支 MSPT 能否在保持局部-全局通信优势的同时，进一步提升 CFD 中表面与体积场的耦合精度？这是缩小与 AB-UPT 差距的关键方向。

3. **几何感知划分的替代方案**：除了球树，是否还有其他几何感知划分方法（如八叉树、自适应聚类）能进一步降低 patch 间信息损失并提升长程依赖建模能力？球树的 $O(N \log N)$ 构建开销在实时场景中可能成为瓶颈。

4. **端到端可微分的注意力结构**：能否通过可微分的 patch 划分或学习式的超节点路由，实现端到端优化的局部-全局注意力结构？当前的手动配置限制了方法对不同物理场景的自适应能力。

5. **时序与多物理场推广**：能否将 MSPT 的并行多尺度注意力推广到时序预测或湍流封闭等更复杂的非定常问题中，并维持线性复杂度？这是从“单帧预测”走向“动态仿真”的关键一步。

6. **公平对比协议**：现有复现实验中 Transolver++ 和 AB-UPT 的性能差异在多大程度上源自训练框架、随机种子或超参数？建立统一的公平对比协议对于评估方法改进的真实贡献至关重要。



## 原文 PDF

![[paperPDFs/CVPR_2026/MSPT_Efficient_Large_Scale_Physical_Modeling_via_Parallelized_Multi_Scale_Attention.pdf]]
