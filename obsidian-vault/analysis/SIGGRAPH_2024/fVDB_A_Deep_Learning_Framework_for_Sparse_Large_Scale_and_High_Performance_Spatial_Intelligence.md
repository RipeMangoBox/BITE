---
title: "fVDB: A Deep-Learning Framework for Sparse, Large-Scale, and High-Performance Spatial Intelligence"
type: paper
paper_level: A
venue: SIGGRAPH
year: 2024
pdf_ref: paperPDFs/SIGGRAPH_2024/fVDB_A_Deep_Learning_Framework_for_Sparse_Large_Scale_and_High_Performance_Spatial_Intelligence.pdf
code_link: null
project_link: https://developer.nvidia.com/fvdb
aliases:
- fVDB
tags:
- SIGGRAPH_2024
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
core_operator: "设计并实现fVDB：核心是基于NanoVDB的IndexGrid数据结构，将拓扑与特征数据分离，并辅以GPU加速的网格构建、层次化数字微分分析器(HDDA)光线追踪、自适应多策略稀疏卷积内核(IGEMM/Leaf/Brick/LGGS)以及JaggedTensor表示。"
primary_logic: "利用浅层VDB树的索引网格(IndexGrid)将稀疏拓扑与特征存储解耦，通过拓扑复用以大幅降低内存开销；同时利用该结构固有的空间局部性，使得几何邻近的体素在索引上也邻近，从而能高效兼容并加速非局部操作，在单一数据框架下提供了全面的3D深度学习原语，实现了性能、内存效率和功能丰富性的统一。"
claims:
- "IndexGrid叶子节点仅需80字节编码所有索引，相比naive方法内存减少超过50倍。"
- "HDDA光线追踪在1024³分辨率下比NerfAcc快1.5-3倍，且内存占用最多低100倍。"
- "fVDB的稀疏卷积在特征深度128及以上时比SpConv v2快约25%。"
- "使用fVDB重新实现的NKSR能在8块V100上2分钟内完成3.5亿点云的重建。"
---

# fVDB: A Deep-Learning Framework for Sparse, Large-Scale, and High-Performance Spatial Intelligence

> [!tip] 核心洞察
> 利用浅层VDB树的索引网格(IndexGrid)将稀疏拓扑与特征存储解耦，通过拓扑复用以大幅降低内存开销；同时利用该结构固有的空间局部性，使得几何邻近的体素在索引上也邻近，从而能高效兼容并加速非局部操作，在单一数据框架下提供了全面的3D深度学习原语，实现了性能、内存效率和功能丰富性的统一。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | fVDB：面向稀疏、大规模、高性能空间智能的深度学习框架 |
| 英文题名 | fVDB: A Deep-Learning Framework for Sparse, Large-Scale, and High-Performance Spatial Intelligence |
| 会议/期刊 | SIGGRAPH 2024 |
| Links | [paper](https://arxiv.org/abs/2407.01781) · [Project](https://developer.nvidia.com/fvdb) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction |
| Method | fVDB |
| Dataset | Grid construction (millions of points), Stanford bunny 3-voxel narrow-band ray marching, Sparse convolution micro-benchmark (various sparsity & channel depths), XCube backbone (resolutions 256/512/1024, various channels) |

> [!tip] 效果简介
> - Grid construction (millions of points) 上，最大内存使用 (GB) / 运行时间 (ms) 为 与TorchSparse++持平或更低的内存，运行时间接近，对比 TorchSparse++ / MinkowskiEngine / spconv，变化 fVDB比TorchSparse++更省内存；MinkowskiEngine和spconv在处理大规模数据时失败(OOM或非法内存访问)。
> - Stanford bunny 3-voxel narrow-band ray marching 上，Rays/sec (M) / GPU Mem. (MB) 为 1024³: 1.43 M rays/s, 8.85 MB，对比 NerfAcc: 0.47 M rays/s, 1028 MB，变化 最快约3倍速度提升，内存最多降低116倍。
> - Sparse convolution micro-benchmark (various sparsity & channel depths) 上，有效TFLOPs 为 Leaf/Brick/LGGS在不同条件下显著优于IGEMM；LGGS在特征128+时比IGEMM快~25%，对比 IGEMM (SpConv v2) / TorchSparse++ backend，变化 Leaf在密集叶节点可达3倍提升；Brick达到70-90%峰值带宽；LGGS在高特征维度下优势明显。

## 概要

### 问题瓶颈

大规模、高分辨率的3D空间智能任务——包括表面重建、神经辐射场渲染、3D生成与物理仿真——对底层深度学习框架提出了严苛要求：既需要高效存储稀疏数据，又必须支持丰富的可微操作原语（如卷积、光线追踪、采样、网格化）。然而，现有稀疏3D框架在数据结构层面存在根本性矛盾：

- 基于哈希表的框架（如 **MinkowskiEngine** (Choy et al., CVPR 2019)、**TorchSparse/TorchSparse++** (Tang et al., MLSys 2022; MICRO 2023)、**SpConv** (2022)）提供了$O(1)$随机访问，但缺乏空间一致性和层级结构，难以高效支持光线追踪、采样、splatting等非局部图形学操作。
- 基于八叉树的框架（如O-CNN、Kaolin）具备空间层级，但随机访问效率低下，且内存占用随分辨率增长迅速膨胀。
- 光线追踪加速库 **NerfAcc** (Li et al., 2023) 依赖密集bitfield八叉树，在$1024^3$分辨率下GPU内存消耗高达1028 MB，难以扩展到大规模场景。

核心瓶颈在于：**尚无单一数据结构能同时提供$O(1)$随机访问、空间一致性、低内存占用，以及对光线追踪、采样、splatting等复杂操作的高效支持**，导致稀疏3D深度学习难以端到端地处理大规模、高分辨率数据。

### 核心方法：fVDB

fVDB（发表于ACM Trans. Graph. 2024）针对上述瓶颈提出了统一解决方案。其核心创新是**基于NanoVDB的IndexGrid数据结构**——一种浅层VDB树的变体，将稀疏拓扑与特征存储解耦：

- **拓扑与特征分离**：IndexGrid仅索引活跃体素的全局偏移量，特征值存储于外部线性数组中。每个叶节点仅需80字节编码所有索引，相比朴素方法内存减少超过50倍。
- **空间局部性继承**：利用VDB树固有的层级结构，几何邻近的体素在索引上也邻近，为卷积、光线追踪等操作提供了缓存友好的内存访问模式。
- **多策略稀疏卷积内核**：自适应地在IGEMM（兼容SpConv v2）、Leaf密集化、Brick密集化、LGGS（局部Gather-GEMM-Scatter）四种策略间切换，在不同稀疏度和特征深度下均能逼近硬件峰值计算带宽。
- **HDDA光线追踪**：层次化数字微分分析器利用VDB的四层树结构实现高效跳空，在$1024^3$分辨率下比NerfAcc快1.5–3倍，内存占用最多降低100倍。
- **JaggedTensor**：统一处理变长数据（如每个体素不同数量的邻居）的内存布局与算子。

### 主要结果

fVDB在多个维度验证了其性能与功能优势：

- **网格构建**：内存效率优于TorchSparse++，且MinkowskiEngine和SpConv在大规模数据下出现OOM或非法内存访问。
- **光线追踪**：Stanford bunny窄带光线行进中，$1024^3$分辨率下达到1.43 M rays/s，仅需8.85 MB显存（NerfAcc为0.47 M rays/s，1028 MB）。
- **稀疏卷积**：特征深度≥128时，LGGS内核比SpConv v2快约25%；Leaf密集化在叶节点占用率>20%时可达3倍提升。
- **端到端任务**：XCube骨干网络在所有配置下归一化速度均为最优；Waymo NeRF训练速度与Instant NGP持平，推理快17%，PSNR高1.18 dB；NKSR重新实现可在8块V100上2分钟内完成3.5亿点云的重建。

### 方法谱系与知识库定位

fVDB处于**稀疏3D深度学习框架**与**体积数据结构**的交叉点。其技术谱系可追溯至：

| 维度 | 传统方案 | fVDB方案 |
|------|---------|---------|
| 核心数据结构 | 哈希表（MinkowskiEngine/TorchSparse）或八叉树（O-CNN） | 基于NanoVDB的IndexGrid（浅层VDB树+索引网格） |
| 光线追踪 | 密集bitfield DDA（NerfAcc） | HDDA（层级DDA，利用树结构跳空） |
| 稀疏卷积 | 单一GEMM内核（SpConv v2/MinkowskiEngine） | 自适应多策略内核（IGEMM/Leaf/Brick/LGGS） |
| 特征存储 | 拓扑与值耦合（标准VDB） | 拓扑-值分离+JaggedTensor变长打包 |

与 **Instant NGP** (Müller et al., TOG 2022) 的多分辨率哈希编码相比，fVDB的VDB树结构天然支持空间跳空和层级操作，在渲染质量与内存效率上均展现优势。与 **NeuralVDB** 等新兴稀疏表示的关系尚待进一步对比研究。

### 局限与开放问题

当前框架绑定固定VDB树配置（三层，发散因子32/16/8），未探索动态自适应树结构。LGGS内核在高稀疏、高特征维度（≥128）下才能充分发挥优势。尚未实现层次化双重Marching Cubes、粒子/Blob到网格转换等高级算子。NeRF实验场景有限，且PSNR优势部分得益于LiDAR点云提供的精确初始化。代码尚未开源，缺少社区第三方基准验证。

### 空间智能与稀疏3D数据的核心挑战

三维深度学习正从简单的物体识别迈向“空间智能”（spatial intelligence）——即在大规模、高分辨率场景中理解、重建、渲染和交互的能力。这类应用（如自动驾驶场景重建、城市级NeRF训练、物理仿真超分辨率）产生的3D数据天然是稀疏的：有效信号仅存在于物体表面、边界或特定感兴趣区域，而绝大部分空间为空。高效处理此类稀疏数据，需要一个既能紧凑存储又能快速访问的底层数据结构。

### 现有稀疏框架的碎片化困境

当前主流的稀疏3D深度学习框架在数据结构选择上形成了两大阵营，但各自存在结构性缺陷：

**基于哈希表的框架**（如 **MinkowskiEngine** (Choy et al., CVPR 2019)、**TorchSparse/TorchSparse++** (Tang et al., MLSys 2022; MICRO 2023)、**SpConv** (spconv contributors, 2022)）通过哈希表将稀疏坐标映射到特征向量。这类框架在稀疏卷积任务上表现出色，但哈希映射破坏了空间局部性——几何上相邻的体素在内存中可能相距甚远，导致光线追踪、采样、splatting等需要空间遍历的操作效率极低。此外，哈希表本身的内存开销和碰撞处理在大规模数据下成为瓶颈。

**基于八叉树的框架**（如O-CNN、Kaolin）天然支持层次化空间遍历，适合光线行进等操作，但其指针追踪式的随机访问模式导致O(log N)的访问延迟，在大量体素的卷积计算中性能远逊于哈希表方案。**NerfAcc** (Li et al., 2023) 采用密集bitfield八叉树加速光线追踪，但bitfield的内存占用随分辨率立方增长，在1024³分辨率下即超过1 GB，难以扩展到更大场景。

**核心瓶颈**：没有任何单一数据结构能同时满足以下四个需求：
1. **O(1)随机访问**——卷积等局部算子的基础；
2. **空间一致性**——邻近体素在内存中邻近，以利用缓存和合并访问；
3. **低内存占用**——避免存储“空”区域；
4. **高效的非局部操作**——光线追踪、采样、splatting等需要快速空间跳跃遍历。

这种碎片化迫使开发者针对不同任务组合多个框架，丧失了端到端训练的流畅性。

### VDB的潜力与未竟之业

**VDB** (Museth 2013) 是一种浅层树结构——根节点为哈希表，中间层为固定发散因子的密集子节点——在视觉特效和物理仿真领域已被广泛验证。它兼具哈希表的O(1)随机访问和八叉树的空间层次性，天然适合稀疏3D数据。其GPU实现**NanoVDB** (Museth 2021) 提供了紧凑的序列化内存布局。

然而，将VDB直接用于深度学习存在关键障碍：标准的VDB将拓扑信息（哪些体素是活跃的）与特征值耦合存储在同一树节点中。当需要存储多个特征张量（如多通道特征图、梯度、优化器状态）时，每个张量都需复制整棵树结构，导致内存膨胀。此外，VDB缺乏面向深度学习的GPU加速构建、张量运算、可微光线追踪等算子生态。

### fVDB的动机与核心思路

fVDB的出发点正是弥合这一鸿沟：**利用VDB的结构优势，通过拓扑与特征解耦的IndexGrid设计，在单一数据结构上统一提供所有关键3D深度学习原语**。具体而言，fVDB将VDB树的拓扑骨架提取为轻量级的IndexGrid（每个叶节点仅需80字节编码所有索引，相比naive方法内存减少超过50倍），特征数据以密集侧车（sidecar）张量形式独立存储，实现拓扑一次构建、多次复用。在此之上，fVDB构建了完整的可微算子生态：GPU加速的网格构建、层次化数字微分分析器（HDDA）光线追踪、自适应多策略稀疏卷积内核（IGEMM/Leaf/Brick/LGGS）、JaggedTensor变长数据支持、采样与splatting、网格化等，使得从点云到NeRF渲染到表面重建的完整流水线可在单一框架内高效运行。

## 核心方法与创新机理

fVDB 的核心创新并非发明一个全新的稀疏数据结构，而是**对成熟 VDB 树进行关键改造，使其从面向图形学的数值存储容器转变为面向深度学习的稀疏索引加速器**。这一改造围绕一个中心思想展开：**拓扑与特征分离**，并以此为基础构建了一套完整的高性能算子生态。

### 核心数据结构：IndexGrid — 拓扑与特征解耦

现有稀疏 3D 深度学习框架在数据结构上存在根本性分歧：**MinkowskiEngine**（Choy et al., CVPR 2019）和 **TorchSparse/TorchSparse++**（Tang et al., MLSys 2022; MICRO 2023）基于哈希表，提供 $O(1)$ 随机访问但缺乏空间局部性，难以支持光线追踪等非局部操作；**O-CNN** 等八叉树结构虽具空间层级，但随机访问效率受限。fVDB 的解决方案是采用基于 **NanoVDB** 的 **IndexGrid** 结构——一个浅层 VDB 树，其核心特性是将拓扑信息与特征值**完全分离存储**。

> The key innovation ... is a new data structure derived from NanoVDB [Museth 2021], which we call IndexGrid.

具体而言，IndexGrid 的 VDB 树仅负责维护稀疏体素的拓扑结构，并返回**全局稀疏索引**（而非特征值本身）。特征值存储在外部的密集张量侧车（sidecar）中，通过索引访问。这一设计带来三个关键优势：

1. **拓扑复用与极致内存压缩**：同一拓扑可被多个特征层共享，且无需为背景（非活跃）体素分配存储。每个 IndexGrid 叶子节点仅需 **80 字节**编码所有索引，相比 `nanovdb::LeafNode<uint64_t>` 的 4KB 以上，**内存减少超过 50 倍**（置信度 0.98）。

2. **空间局部性保留**：VDB 树固有的层级结构使得几何邻近的体素在索引空间中也邻近，这为后续的高效光线追踪和局部密集化卷积提供了结构基础。

3. **$O(1)$ 摊销访问**：浅层固定深度 VDB 树（发散因子 32/16/8）保证了摊销 $O(1)$ 的读写性能，兼顾了哈希表的访问效率与树结构的空间层级。

### 算子生态：围绕 IndexGrid 构建的全套可微原语

仅有数据结构不足以构成完整框架。fVDB 围绕 IndexGrid 构建了一套覆盖 3D 深度学习全流程的可微算子，这是其区别于其他框架的关键差异化能力（见 Table 1 功能对比矩阵）。

**GPU 加速的 IndexGrid 构建**：通过将体素坐标编码为 64 位密钥（见 Fig. 4/Fig. 5），利用基数排序和层级注册算法，可在数毫秒内从数百万体素坐标构建 IndexGrid。在网格构建基准测试中（Fig. 9），fVDB 的内存效率优于 TorchSparse++，而 MinkowskiEngine 和 SpConv 在大规模数据下出现 OOM 或非法内存访问。

**HDDA 层次化光线追踪**：传统方法如 **NerfAcc**（Li et al., 2023）使用密集 bitfield 八叉树进行 DDA 光线行进，内存开销巨大。fVDB 的 HDDA 利用 VDB 树的四个层级（对应体素域 $\{4096^3, 128^3, 8^3, 1^3\}$），每层运行独立的 DDA，实现跨越大片空白区域的跳跃式加速。通过模板元编程将四层 DDA 内联为单一 GPU 内核。在 1024³ 分辨率下，HDDA 比 NerfAcc 快 **1.5-3 倍**，且 GPU 内存占用最多**降低 100 倍以上**（Table 2，置信度 0.99）。

**自适应多策略稀疏卷积**：这是 fVDB 在算子设计上最具深度的创新。不同于 **SpConv v2** 使用单一 IMPLICIT GEMM 内核或 **MinkowskiEngine** 使用规则 GEMM，fVDB 根据局部稀疏模式动态选择最优内核策略：

- **Leaf 内核**：在叶节点占用率 ≥20% 时，将 8³ 叶节点密集化到共享内存中执行局部密集卷积，密集域可达 **2.5-3 倍**的性能优势（置信度 0.9）。
- **Brick 内核**：针对局部高占用区域，在 4×2×2 窗口上使用定制 TensorCore 实现，特征深度 128+ 时达到峰值计算带宽的 **90% 以上**（置信度 0.9）。
- **LGGS 内核**：针对高稀疏、高特征维度（≥128）场景，通过阻塞 gather-GEMM-scatter 操作、利用共享内存避免全局内存分散散射，在 SemanticKITTI 单帧点云上比 SpConv v2 快约 **25%**（置信度 0.9）。

**JaggedTensor**：处理变长数据（如每个体素不同数量的邻居）的内存布局，将变长张量列表打包为连续内存块配合偏移量元数据，为注意力等算子提供高效的数据组织方式。

### 从框架到应用：统一加速结构的端到端能力

fVDB 的真正优势在于**所有算子共享同一 IndexGrid 加速结构**，避免了不同操作之间数据结构转换的开销。这使得复杂 3D 深度学习流水线——从稀疏卷积特征提取、到光线追踪渲染、再到 Marching Cubes 网格化——可以在统一框架内端到端执行。具体案例包括：

- **大规模表面重建**：使用 fVDB 重新实现的 **NKSR** 在 8 块 V100 GPU 上 **2 分钟**内完成 3.5 亿点云的重建（置信度 0.99）。
- **NeRF 训练与渲染**：在 Waymo Open Dataset 场景级 NeRF 任务中，fVDB 版训练速度与 **Instant NGP** 相近（26.1 vs 26.4 it/s），推理速度快 17%，PSNR 高 1.18 dB（置信度 0.95）。
- **3D 生成模型**：在 XCube 骨干网络的不同配置（分辨率 256/512/1024）下，fVDB 的归一化推理速度始终为 1.0（最快），其余框架均低于 1.0（Fig. 11，置信度 0.95）。

### 创新边界与待验证问题

当前 fVDB 绑定固定的 VDB 树配置（三层，发散因子 32/16/8），未探索动态自适应树结构。LGGS 内核在高特征维度下才能充分发挥优势，对低维特征效率有限。部分高级算子（如层次化双重 Marching Cubes、粒子到网格转换）尚未实现。此外，代码尚未开源，缺少社区第三方基准验证。关于根据局部稀疏模式动态调度最优卷积内核的预期性能增益，以及 IndexGrid 在动态拓扑变化频繁场景下的重建成本是否可接受，仍是有待探索的开放问题。

![[assets/figures/papers/paper_list_l19_https_arxiv_org_abs_2407_01781/figures/001_Figure_1.jpg]]
*Figure 1: ?? VDB is an integrated Deep Learning framework for large-scale, and high-performance spatial intelligence. It can process 3D data from a broad range of sources, including voxels, point clouds, and surface meshes. ?? VDB also offers a rich set of state-of-the art differentiable operators, which can be used to build Deep Learning architectures for tasks in 3D Deep Learning, thus facilitating DL applications on large scale and high-resolution 3D data*

fVDB 是一个面向大规模、高分辨率空间智能的端到端深度学习框架，其核心设计理念是将稀疏3D数据的拓扑结构与特征值**解耦存储**，并围绕这一数据结构构建一整套可微分的3D深度学习原语。框架的输入覆盖体素、点云、表面网格等多种3D数据源，输出则支持重建、生成、渲染、仿真超分辨率等广泛的下游任务（Fig. 1）。

### 核心数据结构与构建管线

框架的基石是**IndexGrid**——一种从NanoVDB（Museth 2021）派生而来的浅层VDB树结构。与传统VDB将拓扑与特征值耦合存储不同，IndexGrid将树中活跃体素的拓扑信息编码为全局稀疏索引，而特征值则以独立线性数组（sidecar）的形式存放在树结构外部。这一设计带来两个关键收益：

1. **内存效率**：单个叶节点仅需80字节即可编码全部索引，相比naive方法（`nanovdb::LeafNode<uint64_t>`约4KB）内存减少超过50倍（§3.2）。
2. **拓扑复用**：同一个IndexGrid拓扑可被多个特征数组共享，避免为不同特征通道重复存储空间结构。

IndexGrid的GPU构建算法（§3.3）将数百万体素坐标在数毫秒内转化为完整的稀疏索引网格。该算法通过两个64位密钥的构造与排序完成：第一步将体素坐标打包为排序密钥 $a = k \gg 12 \mid (j \gg 12) \ll 21 \mid (i \gg 12) \ll 42$，用于去重和初步排序；第二步将瓦片ID与各级节点偏移打包为注册密钥 $b = M \ll 36 \mid \text{upper::off}(i,j,k) \ll 21 \mid \text{lower::off}(i,j,k) \ll 9 \mid \text{leaf::off}(i,j,k)$，用于构建树层级结构。在网格构建基准测试中，fVDB与TorchSparse++性能持平，且比MinkowskiEngine和spconv具有更低的内存占用和更好的大规模扩展性——后两者在处理大量数据时分别出现OOM和非法内存访问错误（Fig. 9）。

### 算子体系与模块关系

围绕IndexGrid，fVDB提供了一套完整的可微算子原语，覆盖3D深度学习的核心需求（Table 1）：

| 算子模块 | 功能 | 关键实现 |
|---------|------|---------|
| **稀疏卷积** | 3D特征提取 | 多策略自适应内核（IGEMM/Leaf/Brick/LGGS） |
| **池化** | 空间下采样 | 最大池化、平均池化 |
| **HDDA光线追踪** | 渲染与特征投影 | 四层级层次化数字微分分析器 |
| **采样与Splatting** | 网格-光线特征交换 | 基于IndexGrid的快速定位 |
| **注意力** | 长程依赖建模 | 集成FlashAttention的稀疏Transformer |
| **网格化** | 等值面提取 | Marching Cubes |
| **JaggedTensor** | 变长数据处理 | 拼接存储+jidx/joffsets元数据 |

**稀疏卷积**是框架中最关键的算子。fVDB不依赖单一卷积策略，而是根据局部稀疏模式自适应选择最优内核（§3.5）：
- **IGEMM**：与SpConv v2兼容的通用IMPLICIT GEMM后端，作为默认选项。
- **Leaf密集化**：当叶节点占用率≥20%时触发，将8³叶节点在共享内存中局部密集化，利用TensorCore加速，在密集域可达2.5-3倍性能优势。
- **Brick密集化**：针对局部高占用场景，在4×2×2窗口上单片产生卷积输出，特征深度32-64时达到70%以上峰值计算带宽，128+时超过90%。
- **LGGS**（局部Gather-GEMM-Scatter）：针对高稀疏、高特征维度（≥128）场景，通过阻塞gather-GEMM-scatter操作、利用共享内存缓冲避免全局内存分散散射，在SemanticKITTI单帧点云上比SpConv v2快约25%。

**HDDA光线追踪**（§3.4）是fVDB区别于其他稀疏框架的独特能力。它利用VDB树的四级结构（对应体素域 $\{4096^3, 128^3, 8^3, 1^3\}$），在每层运行独立的DDA，并通过模板元编程将所有层级内联为单一高性能内核。这使得光线可以高效地“跳过”空白区域。在Stanford bunny的3体素窄带测试中（1024³分辨率），HDDA达到1.43M rays/s，仅需8.85 MB显存，而NerfAcc基于密集bitfield的DDA仅为0.47M rays/s，却占用1028 MB——速度提升约3倍，内存降低超过100倍（Table 2）。

**JaggedTensor**（§3.6.1）是处理变长数据（如每个体素不同数量的邻居、不同长度的光线采样点）的通用抽象。其内部将所有变长张量拼接为一个密集张量（`jdata`），并维护两个辅助元数据：`jidx`（每个元素所属的列表项索引）和`joffsets`（每个列表项的起止偏移）。这一设计使得后续的采样、splatting和注意力算子可以高效地操作非规则数据。

### 端到端流程

典型的fVDB工作流如下：原始3D数据（点云/网格/体素）首先通过GPU加速的IndexGrid构建算法转化为稀疏索引网格；随后，根据任务需求，数据流经稀疏卷积（可选自适应内核）、池化等下采样操作提取多尺度特征；对于渲染相关任务，HDDA负责高效的光线-网格求交，采样和splatting算子完成特征投影与散射；对于重建任务，Marching Cubes从特征网格中提取等值面；注意力机制和JaggedTensor则为更复杂的架构提供支持。整个过程中，IndexGrid的拓扑结构可在不同算子间复用，避免了重复的空间结构存储开销。

这一统一框架使得fVDB能够在单一数据结构上同时支持高性能稀疏卷积和复杂图形学操作，这是此前基于哈希表（MinkowskiEngine、TorchSparse）或八叉树（O-CNN）的框架所无法实现的。

### 3.1 VDB树背景与IndexGrid核心设计

fVDB的核心数据结构**IndexGrid**衍生自NanoVDB（Museth 2021），其底层是一棵浅层VDB树——根节点为哈希表，向下依次为32³、16³、8³的密集子节点层级（见Fig. 2）。IndexGrid的关键创新在于**将拓扑与特征值分离**：树结构仅返回体素在外部线性数组中的索引，而非直接存储特征值。这一设计带来两大优势：

1. **拓扑复用**：同一份稀疏拓扑可服务于多组特征数据（如多通道特征图），避免重复存储。
2. **极致内存压缩**：每个叶子节点仅需80字节编码所有索引，相比`nanovdb::LeafNode<uint64_t>`的4KB以上，内存减少超过50倍（Section 3.2）。

IndexGrid的索引采用**稀疏全局索引**方式——仅对活跃（active）体素分配连续索引，跳过非活跃的背景区域（Fig. 3）。体素坐标到叶子节点内偏移的计算通过位运算实现：

```c
int off(int i, int j, int k) {
    return (i & 7) << 6 | (j & 7) << 3 | k & 7;
}
```

该函数将体素坐标`(i,j,k)`映射到8³叶子节点内的线性索引（0-511），利用低3位提取节点内偏移。类似地，下层节点（lower node）和上层节点（upper node）的偏移计算分别为：

```c
// lower node: 16³ 域内偏移
int lower::off(int i, int j, int k) {
    auto a = [](int n) { return (n & 127) >> 3; };
    return a(i) << 8 | a(j) << 4 | a(k);
}

// upper node: 32³ 域内偏移
int upper::off(int i, int j, int k) {
    auto a = [](int n) { return (n & 4095) >> 7; };
    return a(i) << 10 | a(j) << 5 | a(k);
}
```

### 3.2 GPU加速的IndexGrid构建

从数百万体素坐标构建IndexGrid的过程在GPU上完成，耗时仅数毫秒。构建算法分为五个步骤，其中两个关键步骤涉及64位密钥的构造：

**步骤2：初始排序密钥**

将体素坐标`(i,j,k)`打包为64位密钥进行基数排序：

$$a = k \gg 12 \ |\  (j \gg 12) \ll 21 \ |\  (i \gg 12) \ll 42$$

其中`i,j,k`为有符号坐标，右移12位后各占21位（共63位），最高位置零。这一密钥将空间上邻近的体素聚集到同一粗粒度瓦片内（Fig. 4）。

**步骤5：层级注册密钥**

在去重和瓦片分配后，构造用于注册树节点的唯一密钥：

$$b = M \ll 36 \ |\  \text{upper::off}(i,j,k) \ll 21 \ |\  \text{lower::off}(i,j,k) \ll 9 \ |\  \text{leaf::off}(i,j,k)$$

其中`M`为瓦片ID（占28位），`upper::off`占15位，`lower::off`占12位，`leaf::off`占9位（Fig. 5）。该密钥完整编码了体素在VDB树四层结构中的位置，用于并行注册和构建树拓扑。

### 3.3 层次化数字微分分析器（HDDA）

HDDA是fVDB光线追踪的核心加速算法。其基本思想是：为VDB树的四个层级各分配一个DDA（数字微分分析器），对应体素域大小分别为：

$$\{4096^3, 128^3, 8^3, 1^3\}$$

光线行进时，HDDA从最粗层级（4096³）开始步进，仅在当前层级发现活跃节点时才进入下一细层级；若某一层级的当前节点为空，则直接跳空到该层级的下一节点边界，实现高效的“蛙跳式”空域跳过（Fig. 7）。由于VDB树配置在编译期已知，HDDA通过**模板元编程**将四个DDA的内联逻辑融合为单一高性能内核，避免了运行时分支开销。

### 3.4 自适应多策略稀疏卷积内核

fVDB的稀疏卷积不依赖单一实现，而是根据局部稀疏模式动态选择最优内核策略：

| 内核 | 适用场景 | 核心机制 |
|------|----------|----------|
| **IGEMM** | 通用默认 | 兼容SpConv v2的隐式GEMM实现 |
| **Leaf** | 叶节点占用率≥20% | 在共享内存中对8³叶节点做局部密集化，直接从VDB树元数据计算gather偏移 |
| **Brick** | 局部高占用 | 在4×2×2窗口上单片式产生卷积输出，配合定制TensorCore实现 |
| **LGGS** | 高稀疏、高特征深度（≥128） | 阻塞式gather-GEMM-scatter，以64个输出索引为一组，利用共享内存暂存散射结果，避免全局内存的低效分散写入 |

LGGS内核的关键优化步骤包括：(a) 将gather-GEMM-scatter操作阻塞在连续64个输出索引上；(b) 以共享内存缓冲区替代全局内存作为散射目标；(c) 对27个模板偏移逐一收集输入/输出索引对，在共享内存中连续打包后执行GEMM。这一设计避免了多次流式传递和全局内存散射的低效，使得在高特征维度场景下性能超越SpConv v2约25%（SemanticKITTI单帧点云，特征深度≥128时）。

### 3.5 JaggedTensor

JaggedTensor是fVDB处理变长数据的内存布局抽象。概念上，它是一个张量列表，其中每个列表项的第一维长度可变，其余维度保持一致。内部实现将列表中所有张量拼接为一个密集张量`jdata`，并维护两个辅助元数据：`jidx`（每个元素所属的列表项索引）和`joffsets`（每个列表项在`jdata`中的起始偏移）（Fig. 8）。这一设计使得诸如邻域查询（每个体素的邻居数量不同）等变长数据操作能够以规则的内存访问模式高效执行。

## 实验与关键发现

### 核心数据结构与算子微基准测试

#### 网格构建：内存与速度的规模化优势

fVDB的IndexGrid构建算法在GPU上展现出与TorchSparse++（Tang et al., MLSys 2022; MICRO 2023）持平甚至更优的性能，同时在内存效率上显著领先。如Fig. 9所示，在处理百万级点坐标时，fVDB的最大内存占用始终低于TorchSparse++，而MinkowskiEngine（Choy et al., CVPR 2019）和SpConv（spconv contributors, 2022）在数据规模增大时分别遭遇OOM和非法内存访问，无法完成构建。这一优势直接源于IndexGrid将拓扑与特征值分离的设计——每个叶节点仅需80字节编码所有索引，相比naive方法实现超过50倍的内存缩减。

#### 光线追踪：HDDA对NerfAcc的压倒性优势

Table 2展示了在Stanford bunny的3-voxel窄带表面上进行光线行进的对比结果。在1024³分辨率下，fVDB的HDDA达到1.43 M rays/s，而NerfAcc（Li et al., 2023）仅为0.47 M rays/s，速度提升约3倍。更关键的是内存占用：fVDB仅需8.85 MB，NerfAcc却高达1028 MB，内存差距达116倍。这种优势在不同分辨率下保持稳定（1.5x-3x速度提升），根源在于HDDA利用VDB的四层级树结构（对应体素域{4096³, 128³, 8³, 1³}）实现高效的层级跳空，而NerfAcc依赖密集bitfield八叉树，在高分辨率下内存膨胀严重。

![[assets/figures/papers/paper_list_l19_https_arxiv_org_abs_2407_01781/figures/011_Table_2.jpg]]
*Table 2: Comparison between HDDA ray marching in ?? VDB and DDA ray marching in NerfAcc [Li et al. 2023] on the 3-voxel-wide shell of the Stanford bunny. Our approach consistently outperforms that of NerfAcc by 1.5x to 3x on runtime while also maintaining up to 100x lower GPU memory footprint*

#### 稀疏卷积：多策略内核的自适应优势

Fig. 10的微基准测试揭示了fVDB三种自研内核在不同稀疏模式与特征深度下的性能剖面：

- **Leaf内核**：针对叶节点内局部密集化场景。当叶节点占用率超过20%时性能超越默认IGEMM（兼容SpConv v2），在密集域可达2.5-3倍优势。其核心机制是在GPU共享内存中对8³叶节点进行局部去稀疏化，将不规则访问转化为规则密集计算。
- **Brick内核**：针对局部高占用窗口。在特征深度32-64时达到峰值计算带宽的70%以上，128+时超过90%。该内核在4×2×2窗口上整体产生卷积输出，配合定制tensorcore实现，充分利用了硬件计算能力。
- **LGGS内核**：针对高稀疏、高特征维度（≥128）场景。通过阻塞gather-GEMM-scatter操作（每次处理64个连续输出索引）、利用共享内存作为scatter暂存区避免全局内存分散写入，LGGS在SemanticKITTI单帧点云等典型高稀疏数据上，特征深度128+时比SpConv v2快约25%。

fVDB保留了根据具体场景选择最优内核的能力，这种自适应调度策略是其在多样化工作负载下保持性能领先的关键。

#### 端到端速度：XCube骨干网络全面领先

Fig. 11展示了在XCube（Ren et al., 2023）骨干网络的不同配置下（分辨率256/512/1024，多种通道数），fVDB与TorchSparse++、MinkowskiEngine、SpConv的端到端推理速度对比。以fVDB为归一化基准（1.0），其余所有框架在所有配置下均低于1.0，fVDB始终为最快选择。这一全面优势验证了IndexGrid数据结构与多策略卷积内核在真实深度学习工作负载中的协同效应。

![[assets/figures/papers/paper_list_l19_https_arxiv_org_abs_2407_01781/figures/013_Figure_11.jpg]]
*Figure 11: End-to-end speed comparison of ?? VDB with state-of-the-art sparse frameworks under different configurations of the XCube [Ren et al. 2023] backbone. Runtime speed is normalized over the best model (always ours in this case), and the higher the better. Results are averaged over 10 runs*

### 大规模应用验证

#### 表面重建：NKSR的规模化突破

fVDB重新实现的NKSR（Neural Kernel Surface Reconstruction）在8块V100 GPU上仅用2分钟即完成3.5亿点云的大规模场景重建（Fig. 12）。这一规模远超原版NKSR（基于MinkowskiEngine）的报告能力，展示了fVDB在内存效率和计算吞吐上的综合优势如何直接转化为应用层面的规模化能力。配合fVDB的渲染算子，纹理重投影速度也获得显著提升。

#### NeRF训练与渲染：速度与质量双赢

在Waymo Open Dataset的场景级NeRF任务中，fVDB版实现达到26.1 it/s训练速度、1.90 FPS推理速度、27.07 dB PSNR。对比Instant NGP（Müller et al., TOG 2022）的26.4 it/s、1.62 FPS、25.89 dB，fVDB在训练速度相近的情况下，推理速度快17%，PSNR高1.18 dB。需注意PSNR优势部分得益于LiDAR点云提供的精确采样位置初始化，但推理速度的提升直接归功于HDDA的高效光线跳空能力。

### 消融分析：内核策略的条件有效性

消融实验揭示了各卷积内核的适用边界：

- **Leaf密集化**的有效性阈值约为叶节点占用率20%，低于此值时去稀疏化的开销超过收益。密集域（如物体内部）的2.5-3倍加速验证了局部规则化对tensorcore利用率的提升。
- **Brick密集化**在特征深度32-64时达到70%峰值带宽，128+时超过90%，说明高特征维度下计算密集度足以掩盖密集化开销。但在低特征深度（<32）时优势收窄，因为内存搬运占比上升。
- **LGGS**的优势严格依赖于高稀疏度和高特征维度的组合。在特征深度低于64或占用率较高时，IGEMM（SpConv v2）仍是更优选择。LGGS通过阻塞和共享内存暂存避免多次流式传递和全局内存散射低效的设计，在高维稀疏场景下形成了对SpConv v2约25%的稳定优势。

### 失败模式与局限性

在网格构建基准测试中，SpConv在数据量较大时出现非法内存访问错误，MinkowskiEngine则因内存耗尽（OOM）失败，这些失败被如实记录，反映了基于哈希表的稀疏数据结构在极端规模下的固有脆弱性。fVDB的IndexGrid通过拓扑分离和紧凑索引避免了这些问题，但当前框架绑定固定的VDB树配置（三层，发散因子32/16/8），尚未探索动态自适应树结构对性能的进一步影响。此外，LGGS内核在低特征维度下效率有限，且层次化双重Marching Cubes等高级算子尚未实现，这些构成了当前版本的已知边界。

![[assets/figures/papers/paper_list_l19_https_arxiv_org_abs_2407_01781/figures/004_Figure_3.jpg]]
*Figure 3: Illustration of dense local indexing (0-63) vs sparse global indexing (21-38) in a 2D leaf node of size1111101100001100000000 8 ^ { 2 } = 6 4 . . The sparse global indexes correspond to offsets into a dense tensor of per-voxel attributes illustrated at the bottom as one column per attribute, allocated as sidecars to the IndexGrid*

![[assets/figures/papers/paper_list_l19_https_arxiv_org_abs_2407_01781/figures/005_Figure_4.jpg]]
*Figure 4: Breakdown of the 64 bit key constructed from voxel coordinates i , j , , ?? in step 2 of our build algorithm. The lower 21 bits (blue) encode the signed ?? coordinate right-shifted 5 + 4 + 3 = 1 2 bits, the next 21 bits (purple) encode the signed ?? coordinate right-shifted 12 bits, and the upper 21 bits (green) encode the signed ?? coordinate right-shifted by 12 bits. Fig. 5. Breakdown of the unique 64 bit key constructed from voxel coordinates in step 5 of our build algorithm. The lower 9 bits (gray) encode the offset local into leaf nodes ( 2 ^ { 9 } = 5 1 2 = 8 ^ { 3 } ) , the next 12 bits (blue) encode the local offsets into lower nodes ( 2 ^ { 1 2 } = 4 0 9 6 = 1 6 ^ { 3 } ) , the nex...*

![[assets/figures/papers/paper_list_l19_https_arxiv_org_abs_2407_01781/figures/010_Table_1.jpg]]
*Table 1: Feature comparison between our ?? VDB and four alternative sparse DL frameworks that represent state-of-the-art*

## 定位与知识库关联

### 1. 核心瓶颈与设计动机

现有稀疏3D深度学习框架在单一数据结构上存在根本性权衡：基于哈希表的框架（如 **MinkowskiEngine** (Choy et al., CVPR 2019)、**TorchSparse/TorchSparse++** (Tang et al., MLSys 2022; MICRO 2023)、**SpConv** (spconv contributors, 2022)）虽能提供 $O(1)$ 随机访问，但哈希映射破坏了空间一致性，难以高效支持光线追踪、采样、splatting等需要空间邻近查询的图形学操作。基于八叉树的框架（如O-CNN、Kaolin）虽保持了空间层级结构，但随机访问通常为 $O(\log N)$，且内存布局对GPU不友好。更关键的是，上述框架均无法在同一数据结构上同时满足以下需求：

- **$O(1)$ 随机访问**（训练时频繁读写特征）
- **空间一致性**（邻近体素在索引上也邻近，利于光线跳空和缓存局部性）
- **低内存占用**（避免存储空区域，拓扑与特征解耦以复用结构）
- **原生支持图形学操作**（光线追踪、Marching Cubes、采样/splatting）

fVDB的核心动机正是打破这一僵局：利用VDB树固有的浅层层级结构（深度4，发散因子32/16/8）同时获得哈希表级别的 $O(1)$ 访问和八叉树级别的空间局部性，并通过拓扑-特征分离的IndexGrid设计将内存效率推向极致。

### 2. 关键设计槽位对比

下表梳理fVDB相对主流基线的关键设计差异：

| 设计槽位 | 基线方案 | fVDB方案 | 差异机制 |
|---------|---------|---------|---------|
| **核心数据结构** | 哈希表（MinkowskiEngine/TorchSparse）或八叉树（O-CNN/Kaolin） | 基于NanoVDB的IndexGrid（浅层VDB树+索引网格，拓扑与值分离） | 哈希表丢失空间局部性；八叉树访问非$O(1)$。IndexGrid通过固定浅层树兼得两者优势 |
| **光线追踪/行进** | 基于密集bitfield的DDA（**NerfAcc** (Li et al., 2023)） | HDDA（层次化数字微分分析器，利用树四级层级加速跳空） | HDDA在粗粒度层（$4096^3, 128^3, 8^3$）快速跳过空域，仅在最细粒度层（$1^3$）做精确步进 |
| **稀疏卷积策略** | 单一IMPLICIT GEMM内核（SpConv v2）或规则GEMM（MinkowskiEngine） | 自适应多策略内核：IGEMM（兼容SpConv v2）、Leaf密集化、Brick密集化、LGGS（局部Gather-GEMM-Scatter） | 根据叶节点占用率和特征深度动态选择最优内核，避免单一策略的适应性瓶颈 |
| **内存布局** | 拓扑与特征值耦合存储（标准VDB） | 分离拓扑与特征的IndexGrid + JaggedTensor | 拓扑复用使多特征通道共享同一树结构；JaggedTensor高效打包变长数据 |

### 3. 方法谱系定位

fVDB处于**稀疏3D深度学习框架**与**体积数据结构**的交叉地带，其知识谱系可追溯至三条线索：

**线索一：稀疏卷积框架演进。** MinkowskiEngine率先将广义稀疏卷积引入深度学习，通过哈希表管理稀疏坐标。TorchSparse/SpConv进一步通过IMPLICIT GEMM等内核优化将稀疏卷积推向TensorCore利用率极限。fVDB继承了这一脉对高性能稀疏卷积的追求，但指出哈希表在非卷积操作（光线追踪、采样）上的结构性缺陷，转而以VDB树作为统一底层。

**线索二：体积数据结构。** OpenVDB/NanoVDB (Museth, 2013/2021) 在视觉特效和物理仿真领域建立了浅层树+哈希根节点的经典方案。fVDB的关键创新在于将VDB从"值存储"改造为"索引存储"（IndexGrid），使树结构退化为纯粹的拓扑索引，特征值存储于外部连续数组。这一分离使得同一拓扑可被多个特征通道复用，且每个叶节点仅需80字节编码全部索引（相比naive方法的4KB+，内存减少超50倍）。

**线索三：NeRF加速结构。** **Instant NGP** (Müller et al., TOG 2022) 使用多分辨率哈希编码+级联密度网格，NerfAcc使用密集bitfield八叉树加速光线采样。fVDB的HDDA在概念上类似多层级跳空，但通过编译期模板元编程将四级DDA内联为单一高性能内核，在1024³分辨率下比NerfAcc快1.5-3倍，且内存占用低至100倍以下（Table 2: fVDB 8.85 MB vs NerfAcc 1028 MB）。

### 4. 适用边界与局限

**适用边界：**
- **高分辨率稀疏3D数据**（如点云、NeRF网格、仿真体素）：IndexGrid的稀疏存储优势随分辨率提升而放大。
- **需要多操作融合的端到端任务**：fVDB在同一框架内提供卷积、注意力、光线追踪、采样、splatting、网格化等全栈原语，避免了跨框架数据搬运。
- **大规模场景**：NKSR重建案例（3.5亿点云，8×V100，2分钟）展示了其在大规模数据下的工程可行性。

**已知局限：**

1. **固定树配置。** 当前绑定VDB默认配置（三层，发散因子32/16/8），未探索动态自适应树结构。对于特征尺度分布极不均匀的场景，固定配置可能导致某些区域过密或过疏。

2. **LGGS内核的条件优势。** LGGS在高稀疏、高特征维度（≥128）下才能充分发挥优势（比SpConv v2快约25%），对低维度特征效率有限。这意味着在浅层网络或轻量任务中，默认IGEMM可能仍是更优选择。

3. **高级算子缺失。** 尚未实现层次化双重Marching Cubes、粒子/Blob到网格转换等高级图形学算子，限制了其在物理仿真等特定领域的直接适用性。

4. **NeRF实验的公平性注意。** fVDB版NeRF的PSNR优势（27.07 dB vs Instant NGP 25.89 dB）部分得益于LiDAR点云提供的精确采样位置初始化，而iNGP未利用此信息。训练速度方面两者接近（26.1 vs 26.4 it/s），推理速度fVDB快17%（1.90 vs 1.62 FPS）。

5. **代码未开源。** 论文发表时代码计划发布但尚未公开，目前缺少社区第三方基准验证。所有性能数据均来自作者自报。

### 5. 开放问题

1. **动态拓扑下的重建开销。** 对于拓扑频繁变化的场景（如物理仿真中的流体界面），IndexGrid的GPU构建算法（从百万坐标到完整网格需数毫秒）是否仍可接受？增量更新策略是否可行？

2. **自适应内核调度的潜力。** 论文展示了四种卷积内核在不同条件下的性能优势，但未实现运行时根据叶节点局部稀疏模式动态调度最优内核的机制。这一自动调度的预期增益有待量化。

3. **与新兴稀疏表示的全面对比。** 与NeuralVDB（将VDB与神经网络隐式表示结合）、Instant NGP的多分辨率哈希编码等在更广泛任务（如3D生成、4D重建）上的系统对比尚缺。

4. **LGGS内核细节。** 论文描述了LGGS通过阻塞gather-GEMM-scatter并利用共享内存避免全局内存分散的高层思路，但避免多次流式传递和减少散射低效的具体步骤细节未完全公开，影响了第三方复现。

5. **树结构自适应。** 是否可以通过学习或启发式方法动态调整VDB树的发散因子和深度，以在内存和访问效率之间取得更好的任务特定平衡？

## 原文 PDF

![[paperPDFs/SIGGRAPH_2024/fVDB_A_Deep_Learning_Framework_for_Sparse_Large_Scale_and_High_Performance_Spatial_Intelligence.pdf]]
