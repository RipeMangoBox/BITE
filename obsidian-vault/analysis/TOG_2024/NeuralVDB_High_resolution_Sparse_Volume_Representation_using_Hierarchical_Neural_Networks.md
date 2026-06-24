---
title: "NeuralVDB: High-resolution Sparse Volume Representation using Hierarchical Neural Networks"
type: paper
paper_level: A
venue: TOG
year: 2024
pdf_ref: paperPDFs/TOG_2024/NeuralVDB_High_resolution_Sparse_Volume_Representation_using_Hierarchical_Neural_Networks.pdf
project_link: https://developer.nvidia.com/rendering-technologies/neuralvdb
aliases:
- NeuralVDB
tags:
- TOG_2024
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
core_operator: "用分层神经网络（分类器和回归器）替代VDB树底部两层的显式节点，单独编码拓扑（活动状态）和值信息。"
primary_logic: "将显式稀疏树结构与隐式神经表示相结合：VDB高层节点保留粗粒度的空间划分和快速遍历能力，多个小型MLP过拟合于局部体素和瓦片值，从而实现数量级的压缩，同时保持VDB的兼容性与可扩展性。"
claims:
- "NeuralVDB将迪士尼云文件大小从1.5 GB（OpenVDB 16-bit Blosc）减少到25 MB，压缩比达60倍。"
- "对于龙模型等SDF体积，用神经网络替换底部两层（[Hash,5,NN(4),NN(3)]）后整体压缩因子达68倍（从257 MB降到3.8 MB）。"
- "NeuralVDB在相同模型尺寸下，在SDF几何上（Bunny, Armadillo, Dragon）的IoU和mCD均优于NGLOD、VBNF和INGP等纯神经表示方法。"
- "Disney Cloud dataset 上 File size compression ratio = 25 MB (NeuralVDB)"
---

# NeuralVDB: High-resolution Sparse Volume Representation using Hierarchical Neural Networks

> [!tip] 核心洞察
> 将显式稀疏树结构与隐式神经表示相结合：VDB高层节点保留粗粒度的空间划分和快速遍历能力，多个小型MLP过拟合于局部体素和瓦片值，从而实现数量级的压缩，同时保持VDB的兼容性与可扩展性。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | NeuralVDB：使用分层神经网络的高分辨率稀疏体数据表示 |
| 英文题名 | NeuralVDB: High-resolution Sparse Volume Representation using Hierarchical Neural Networks |
| 会议/期刊 | TOG 2024 |
| Links | [paper](https://arxiv.org/abs/2208.04448); [Project](https://developer.nvidia.com/rendering-technologies/neuralvdb) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction |
| Method | NeuralVDB |
| Dataset | Disney Cloud dataset, SDF models (e.g., Dragon), Density volumes (e.g., Chameleon), Fractal Brownian motion field |

> [!tip] 效果简介
> - Disney Cloud dataset 上，File size compression ratio 为 25 MB (NeuralVDB)，对比 1.5 GB (OpenVDB 16-bit Blosc)，变化 60x reduction。
> - SDF models (e.g., Dragon) 上，Compression Ratio (vs 16-bit Blosc compressed OpenVDB) 为 61.2x，对比 1x，变化 61.2x smaller。
> - Density volumes (e.g., Chameleon) 上，RMSE 为 0.009，对比 0.0 (lossless OpenVDB)，变化 0.009。

## 概述

**核心问题**：传统稀疏体数据存储方案（如 **OpenVDB**，Museth, ACM TOG 2013）依赖显式存储体素值和拓扑位掩码。即使经过16位量化和通用压缩（如Blosc），大规模体积数据的内存占用仍然巨大——例如迪士尼云数据集（Disney Cloud）的文件体积高达1.5 GB。这类方法无法利用体积内部固有的几何相似性和结构冗余，其压缩效率受限于显式数据结构的表达容量。

**核心思路**：NeuralVDB提出将显式稀疏树结构与隐式神经表示相结合。其关键洞察在于：保留VDB树的高层节点以维持粗粒度的空间划分和快速遍历能力，而将底部两层（叶节点和瓦片节点）的拓扑信息与值信息分别交由多个小型MLP分类器和回归器进行过拟合编码。这种“显式骨架+隐式局部细节”的混合架构，实现了数量级的压缩，同时保持了与VDB生态的兼容性和可扩展性。

**方法定位**：NeuralVDB在方法谱系中处于传统稀疏数据结构（OpenVDB、**NanoVDB**，Museth, SIGGRAPH 2021）与纯神经隐式表示（**NGLOD**，Takikawa et al., CVPR 2021；**VBNF**，Takikawa et al., SIGGRAPH 2022；**INGP**，Müller et al., 2022）的交叉地带。它并非完全抛弃显式树结构，而是用神经网络替代树中最耗费内存的底层节点，从而在压缩率、重建精度和查询速度之间取得新的折中点。

**主要结果**：
- **极致压缩**：在迪士尼云数据集上，NeuralVDB将文件大小从1.5 GB（OpenVDB 16-bit Blosc压缩）缩减至25 MB，压缩比达60倍（Fig. 1）。对于龙模型等SDF体积，整体压缩因子可达68倍（从257 MB降至3.8 MB，Table 1）。
- **精度优势**：在相同模型尺寸下，NeuralVDB在SDF几何（Bunny、Armadillo、Dragon）上的IoU和修正Chamfer距离（mCD）均优于NGLOD、VBNF和INGP等纯神经表示方法（Table 8）。
- **广泛适用性**：方法对静态SDF、密度体积以及动画序列均有效，船只破水动画序列的累积文件大小从22.7 GB降至1.2 GB（18倍压缩，Fig. 1）。

**局限性概览**：网络容量目前依赖启发式人工选择；随机查询速度慢于NanoVDB的硬件插值；训练（编码）时间在超大规模体积上仍较长；对拓扑动态变化的应用场景不支持。

## 背景与动机

### 稀疏体数据的存储瓶颈

在影视特效、科学可视化和工业仿真等领域，大规模稀疏体数据（如符号距离场SDF、密度场、烟雾模拟）已成为核心资产。这些数据通常以树形结构组织，仅存储活动体素周围的窄带区域，以应对全分辨率密集网格带来的内存爆炸。然而，即使采用目前工业界最先进的稀疏体数据结构**OpenVDB**（Museth, ACM TOG 2013），存储开销依然巨大。

OpenVDB的高效源于其浅而宽的树结构：根节点（级别3）为稀疏哈希表，内部节点（级别2和1）分别对应$32^3$和$16^3$的稠密网格，叶节点（级别0）为$8^3$的固定体素块。这种设计在遍历速度和空间自适应性上取得了良好平衡，但其底层存储仍是显式的——每个体素值和拓扑位掩码（active mask、child mask）都需要逐一记录。即便采用16位量化配合通用压缩算法（如Blosc），一个典型的迪士尼云数据集仍需约1.5 GB的磁盘空间（Fig. 1）。

更关键的是，这种显式存储范式**无法利用体积内部的几何相似性和结构冗余**。在自然体积中，相邻体素的值往往高度相关，局部区域的拓扑结构也呈现规律性，但OpenVDB和其GPU加速变体**NanoVDB**（Museth, SIGGRAPH 2021）均将每个体素视为独立单元，忽视了这些可压缩的统计结构。

### 纯神经表示方法的局限

近年来，以神经隐式表示（neural implicit representation）为代表的新范式为体积数据压缩开辟了另一条路径。**NGLOD**（Takikawa et al., CVPR 2021）、**VBNF**（Takikawa et al., SIGGRAPH 2022）和**INGP**（Müller et al., 2022）等方法通过训练小型MLP来拟合体积场，将压缩问题转化为网络参数的优化问题。这些方法在特定场景下展现出可观的压缩比，但其设计理念与工业级体积处理管线存在根本性张力：

1. **遍历效率的损失**：纯神经表示通常需要密集采样或逐点查询来重建体积，丧失了稀疏树结构带来的快速空间跳跃能力。
2. **兼容性缺失**：影视和仿真工业已深度依赖OpenVDB生态（文件格式、工具链、渲染器接口），纯神经方法难以直接嵌入现有管线。
3. **可扩展性不足**：对于分辨率极高（如$32844 \times 24702 \times 9156$的Space模型）或跨帧动画的体积序列，单一全局MLP的容量需求急剧膨胀，训练和推理效率均难以满足生产需求。

### 本文动机：显式与隐式的融合

上述两难处境揭示了一个核心矛盾：**显式树结构擅长空间划分和快速遍历，但不擅长数据压缩；隐式神经表示擅长紧凑编码，但不擅长空间组织和管线兼容**。NeuralVDB的动机正是打破这一对立——能否将两者的优势结合，在保留VDB树高层结构的前提下，用神经网络替换底层显式存储，从而实现数量级的压缩，同时保持VDB的兼容性与可扩展性？

这一思路的关键洞察在于：VDB树的底部两层（级别0和级别1）占据了绝大部分内存开销（以龙模型为例，叶节点值占标准VDB总内存的93%以上，见Table 1），而这两层恰好是局部性最强、最容易被小型MLP过拟合的部分。相比之下，高层节点（级别2和级别3）负责粗粒度的空间划分，保留显式结构对遍历效率至关重要。因此，**将显式稀疏树结构与隐式神经表示进行分层混合**，是一种自然且高效的折中方案。

### 目标与约束

基于上述动机，NeuralVDB设定了以下设计目标：

- **高压缩比**：在已压缩的OpenVDB基础上实现10倍至100倍以上的进一步压缩，同时将重建误差控制在可接受范围内（SDF的IoU > 99%，密度场的RMSE < 0.1）。
- **管线兼容性**：输出仍为可被标准VDB工具读取和渲染的稀疏体数据格式，支持离线解压（out-of-core）和内存内直接访问（in-core）两种模式。
- **可扩展性**：通过稀疏域分解（sparse domain decomposition）支持超大体积和多GPU并行训练，通过时间温启动（warm-start）编码器加速动画序列的处理。
- **拓扑保真度**：对空间占用信息（拓扑掩码）采用无损压缩，仅对体素值进行有损压缩，确保体积的几何结构不被破坏。

这些目标共同指向一个核心命题：**在工业级稀疏体数据处理的语境下，显式结构与隐式表示的融合能否在压缩效率、访问速度和工程兼容性之间找到新的帕累托最优解？** 论文后续的方法设计和实验评估将围绕这一命题展开。

## 核心创新

NeuralVDB 的核心创新在于将**显式稀疏树结构**与**隐式神经表示**相融合，从根本上改变了体积数据的编码方式。传统 VDB 数据结构的瓶颈在于：即使经过 16 位量化和 Blosc 等通用压缩，其底层仍需显式存储每个体素的值和拓扑位掩码，无法利用体积内部的几何相似性与结构冗余（例如迪士尼云数据集仍占用 1.5 GB）。NeuralVDB 的因果调节旋钮（causal knob）是：**保留 VDB 树的高层节点以维持粗粒度空间划分和快速遍历能力，同时用多个小型 MLP 过拟合于局部体素和瓦片值，从而以数量级的压缩比替代显式存储**。

具体而言，该方法在以下四个关键维度上实现了对 baseline 的替换（changed slots）：

### 1. 底层体素值与瓦片值的存储：从显式到隐式推断

- **Baseline**（OpenVDB / NanoVDB）：底层体素值和瓦片值以 32 位浮点数或量化后的定点数显式存储。
- **NeuralVDB**：通过多个 MLP 回归器配合傅里叶特征映射（FFM）隐式推断值，仅存储神经网络参数。回归 MLP 以 MSE 损失进行训练：
  
  $$L_{MSE}(f, \hat{f}) = \frac{1}{N} \sum_{i=1}^{N} (f - \hat{f}_i)^2$$
  
  输入坐标 $\mathbf{x}$ 首先通过特征映射 $\mathbf{z} = \gamma(\mathbf{x})$ 变换为高维特征向量，帮助 MLP 捕获高频细节。

### 2. 体素与瓦片活动状态的编码：从位掩码到神经分类器

- **Baseline**：每个树节点显式存储位掩码（active mask、child mask）来记录活动状态和子节点信息。
- **NeuralVDB**：用二元分类器（级别 0）和三元分类器（级别 1）预测活动状态和子节点/瓦片类型，仅存储分类器参数。
  - 级别 1 的三元分类器判断子节点、活动瓦片或非活动瓦片（标签 $m_1 \in \{c_1=1, a_1=1\}$），使用交叉熵损失。
  - 级别 0 的二元分类器判断体素是否活动（标签 $m_0 \in \{a_1=1\}$），使用二元交叉熵损失。

### 3. 底层树结构：从稠密四层树到混合神经层级

- **Baseline**：完整的四层 VDB 树，叶节点为 $8^3$ 的固定网格，内部节点为 $32^3$ 和 $16^3$。
- **NeuralVDB**：保留根部两级显式树（级别 2–3），将底部两级替换为层级神经网络。论文提出两种配置：
  - **[Hash, 5, 4, NN(3)]**：仅用神经网络表示叶节点值，保留完整的显式树拓扑，优化随机访问速度。
  - **[Hash, 5, NN(4), NN(3)]**：用神经网络同时表示底部两层的节点拓扑和值信息，最大化压缩比。

  以 Dragon 模型为例，[Hash, 5, NN(4), NN(3)] 配置将整体内存从 257 MB 降至 3.8 MB，压缩因子达 68 倍（Table 1）。

### 4. 内存占用：数量级的压缩突破

- **Baseline**：Dragon 模型标准 VDB 占用约 257 MB（32 位无压缩）；迪士尼云经 16 位 Blosc 压缩后仍为 1.5 GB。
- **NeuralVDB**：
  - 迪士尼云：25 MB，压缩比 60 倍（Fig. 1）。
  - Dragon SDF：3.8 MB，压缩比 68 倍（Table 1）。
  - 船只破水动画序列：累计文件从 22.7 GB 降至 1.2 GB，压缩比 18 倍（Fig. 1）。

### 配套机制创新

为支撑上述核心替换，NeuralVDB 还引入了两个关键配套机制：

- **稀疏域分解**：将大型体积划分为固定大小的子域，每个子域配有独立的 MLP 专家网络，通过不可学习的帐篷门函数进行加权组合：
  
  $$\hat{y} = \sum_{k=1}^{n} G(\mathbf{x})_k E_k(\mathbf{x})$$
  
  该设计支持多 GPU 并行训练与推理，使方法可扩展至 32844×24702×9156 分辨率的场景（如太空模型，使用 12 个子域）。

- **时间温启动编码器**：对于动画体积，将前一帧的收敛网络权重作为当前帧训练的初始化，可将训练速度提升 1.2 至 3.1 倍，并增强帧间时间连贯性。

### 设计取舍的明确声明

NeuralVDB 以**查询速度换取压缩比**，这是论文明确承认的设计取舍：
- [Hash, 5, NN(4), NN(3)] 适合离线顺序访问场景（如存档、传输），因为其随机查询需要经过多层神经推断。
- [Hash, 5, 4, NN(3)] 保留完整显式树拓扑，随机访问性能接近标准 VDB，仅在叶节点值查询时需额外回归计算，适合在线渲染等应用。

这一混合设计使 NeuralVDB 在保持 VDB 兼容性与可扩展性的同时，实现了传统压缩方法无法企及的压缩比，且在相同模型尺寸下，其 SDF 几何重建精度（IoU 和 mCD）优于 NGLOD、VBNF 和 INGP 等纯神经表示方法（Table 8）。

## 整体框架

NeuralVDB 的核心设计理念是将**显式稀疏树结构**与**隐式神经表示**相结合：保留 VDB 树的高层节点以维持粗粒度空间划分和快速遍历能力，同时用多个小型 MLP 替代底层节点，分别编码拓扑（活动状态）和值信息，从而实现数量级的压缩。

### 高层架构

整个框架遵循“高层显式、底层隐式”的分层策略。VDB 树共有四个层级（Level 3 至 Level 0），NeuralVDB **仅替换底部两层**（Level 1 和 Level 0）的节点与值存储，根部和上层内部节点保持原始 VDB 结构不变。具体而言，论文提出两种配置以适应不同的访问需求：

- **[Hash, 5, 4, NN(3)]**：仅将叶节点（Level 0）的值替换为神经回归器，Level 1 及以上保持显式树结构。该配置面向**在线随机访问**场景，遍历性能接近标准 VDB，仅叶节点值查询需额外推理。
- **[Hash, 5, NN(4), NN(3)]**：将 Level 1 和 Level 0 的拓扑掩码与值全部替换为神经网络（分类器 + 回归器），实现最大压缩比。该配置更适合**离线顺序重建**场景。

### 模块组成与数据流

NeuralVDB 的完整流水线包含以下核心模块：

**1. 高层 VDB 树（Level 2–3）**
保留原始 VDB 的稀疏哈希根节点和稠密内部节点（尺寸分别为 $32^3$ 和 $16^3$），负责粗粒度的空间划分与节点遍历。该部分不参与神经编码，保证了与现有 VDB 生态的兼容性。

**2. Level 1 神经网络（分类器 + 瓦片值回归器）**
输入为 Level 1 节点的虚拟坐标。三元分类器判断每个子空间属于以下三种情况之一：子节点（child node）、活动瓦片（active tile）或非活动瓦片（inactive tile）。对于活动瓦片，进一步通过 MLP 回归器推断瓦片值。分类器使用交叉熵损失训练，回归器使用均方误差损失训练：

$$L_{MSE}(f, \hat{f}) = \frac{1}{N} \sum_{i=1}^{N} (f - \hat{f}_i)^2$$

**3. Level 0 神经网络（体素掩码分类器 + 体素值回归器）**
输入为叶节点内的局部坐标。二元分类器判断每个体素是否活动（active/inactive），活动体素则通过回归器计算其值。分类器使用二元交叉熵损失训练。

**4. 稀疏域分解**
对于大规模体积（如分辨率 $32844 \times 24702 \times 9156$ 的场景），NeuralVDB 将空间划分为固定大小的子域，每个子域配有独立的 MLP 专家网络。子域之间设有固定宽度的重叠区域（halo），通过**不可学习的门函数**（tent function）对专家输出进行加权融合：

$$\hat{y} = \sum_{k=1}^{n} G(\mathbf{x})_k E_k(\mathbf{x})$$

该设计支持多 GPU 并行训练与推理，且不同于稀疏门控 MoE 的可学习门机制。

**5. 时间温启动编码器**
针对动画体积序列，将前一帧训练收敛的网络权重作为当前帧训练的初始化，可加速训练 1.2–3.1 倍，同时增强帧间的时间一致性。

### 输入输出流

- **输入**：标准 VDB 格式的稀疏体积数据（SDF 或密度标量场），包含完整的四层树结构、节点拓扑掩码和体素/瓦片值。
- **编码过程**：提取底层节点的坐标与目标值，分别训练分类器和回归器 MLP。训练是**故意过拟合**于输入体积的过程，目标是尽可能“记忆”输入。
- **输出（NeuralVDB 数据）**：掩码裁剪后的高层 VDB 树 + 训练好的神经网络参数（分类器与回归器权重）。最终数据是两者的拼接。
- **解码/重建**：对 [Hash, 5, NN(4), NN(3)] 配置，从 Level 1 开始顺序推理，先用分类器重建子节点掩码和活动掩码，再用回归器填充瓦片值，然后递归进入 Level 0 推理体素值。推理中产生的假阳性掩码通过预存的假阳性列表进行校正。对 [Hash, 5, 4, NN(3)] 配置，Level 3–1 使用标准 VDB 遍历，仅叶节点值通过神经网络回归获取。

### 压缩效果

以 Dragon 模型为例（Table 1），标准 VDB 占用 257 MB，[Hash, 5, 4, NN(3)] 将叶节点值占用降至原来的 6%（约 16 倍压缩），而 [Hash, 5, NN(4), NN(3)] 通过同时替换底部两层的拓扑与值，整体压缩因子达 **68 倍**（降至 3.8 MB），同时保持 IoU > 99% 的重建精度。在迪士尼云数据集上，NeuralVDB 将 1.5 GB 的 16-bit Blosc 压缩 VDB 文件缩减至 25 MB，压缩比达 **60 倍**（Fig. 1）。

## 核心模块与公式推导

### 3.1 高层VDB树（级别2–3）

NeuralVDB保留原始VDB树结构中的根部两级（Level 2和Level 3），不作神经化改造。Level 3为稀疏哈希根节点，Level 2为稠密内部节点（尺寸 $32^3$），二者共同负责粗粒度的空间划分与快速遍历。这一设计使NeuralVDB在获得神经压缩收益的同时，保留了VDB的稀疏访问能力和兼容性。

### 3.2 级别1神经网络：掩码分类器与瓦片值回归器

级别1是NeuralVDB的第一层神经表示，替代了原VDB树中该层的显式拓扑掩码和瓦片值存储。其核心由两个MLP组成：

**三元掩码分类器**：输入为级别1节点的虚拟坐标，输出三分类标签 $m_1 \in \{c_1=1, a_1=1, \text{inactive}\}$，分别对应“子节点存在”、“活动瓦片”、“非活动瓦片”。训练使用交叉熵损失。该分类器直接编码了该层级的拓扑信息（child mask与active mask），无需存储显式位掩码。

**瓦片值回归器**：对分类器预测为“活动瓦片”的坐标，进一步通过MLP回归推断瓦片值。训练使用均方误差损失函数：

$$L_{MSE}(f, \hat{f}) = \frac{1}{N} \sum_{i=1}^{N} (f - \hat{f}_i)^2$$

其中 $f$ 为真实值，$\hat{f}$ 为网络预测值。该回归器替代了原VDB中级别1的显式瓦片值数组。

### 3.3 级别0神经网络：体素掩码分类器与体素值回归器

级别0对应VDB的叶节点层（$8^3$ 稠密网格），NeuralVDB在此层同样引入两类MLP：

**二元掩码分类器**：输入叶节点内的局部体素坐标，输出二元标签 $m_0 \in \{a_1=1, \text{inactive}\}$，判断体素是否活动。训练使用二元交叉熵损失。该分类器替代了叶节点内的active mask位掩码。

**体素值回归器**：对活动体素坐标推断其值，同样采用MSE损失训练。

### 3.4 傅里叶特征映射

为使小型MLP能够捕获体积数据中的高频细节，NeuralVDB对输入坐标 $\mathbf{x} \in \mathbb{R}^3$ 应用傅里叶特征映射（Fourier Feature Mapping, FFM），将其变换为高维特征向量：

$$\mathbf{z} = \gamma(\mathbf{x})$$

该映射是NeuralVDB框架中的主要特征映射方法，作用于所有级别0和级别1的回归器与分类器的输入端。

### 3.5 稀疏域分解

对于大规模体积（如迪士尼云数据集），单一MLP难以高效覆盖整个域。NeuralVDB提出稀疏域分解策略：将体积划分为固定大小的子域，每个子域配有独立的MLP专家网络 $E_k$。子域之间设置固定宽度的重叠区（halo），通过非可学习的门函数 $G(\mathbf{x})_k$（可微帐篷函数）进行加权混合：

$$\hat{y} = \sum_{k=1}^{n} G(\mathbf{x})_k E_k(\mathbf{x})$$

该门函数不可学习，与稀疏门控混合专家（MoE）不同。域分解支持多GPU并行训练与推理。

### 3.6 时间温启动编码器

针对动画体积序列，NeuralVDB引入时间温启动策略：将前一帧收敛后的网络权重作为当前帧训练的初始化参数。该模块可加速训练1.2倍至3.1倍，同时增强帧间的时间连贯性，减少闪烁伪影。

### 3.7 两种结构配置

NeuralVDB提供两种配置以权衡速度与内存：

- **[Hash, 5, 4, NN(3)]**：仅将叶节点（级别0）的值替换为神经回归器，级别1保留显式树结构。支持在线随机访问，查询速度接近标准VDB。
- **[Hash, 5, NN(4), NN(3)]**：将底部两级（级别0和级别1）的拓扑与值全部替换为神经网络。压缩比更高（如Dragon模型达68倍），但仅支持离线顺序重建。

## 实验与分析

### 核心实验结果

NeuralVDB 在静态和动态体积数据上均展现出数量级的压缩能力，同时保持高保真度的重建质量。最引人注目的结果是迪士尼云数据集：原始 OpenVDB 16-bit Blosc 压缩后的文件大小为 1.5 GB，而 NeuralVDB 将其缩减至 25 MB，压缩比达到 **60 倍**（Fig. 1）。在动态场景中，船只突破水面的窄带水平集动画序列，累积文件大小从 22.7 GB 压缩至 1.2 GB，压缩比达 **18 倍**（Fig. 1）。

对于 SDF 几何体，NeuralVDB 同样表现出色。以 Dragon 模型为例，标准 VDB 32-bit 无压缩占用 257 MB，而 NeuralVDB [Hash,5,NN(4),NN(3)] 配置仅需 3.8 MB，整体压缩因子达 **68 倍**（Table 1）。在更广泛的 SDF 模型测试中，相较于已使用 16-bit Blosc 压缩的 OpenVDB，NeuralVDB 实现了 **10 倍至超过 100 倍** 的进一步压缩（Table 2），同时保持 IoU > 99% 和极低的修改 Chamfer 距离（mCD）。


![[assets/figures/papers/paper_list_l24_https_arxiv_org_abs_2208_04448/figures/015_Table_2.jpg]]
*Table 2: List of input grid statistics for SDF models and density volumes: OpenVDB file sizes for both raw 32-bit precision with no compression and 16-bit precision with Blosc compression [The Blosc Development Team 2020] in MB, NeuralVDB file size with 16-bit precision with Blosc compression in MB, number of total parameters (both learnable and static) of neural networks, number of false positive patches for the classifiers, compression ratio comparing 16-bit compressed file sizes, and evaluation metrics including IoU and mCD for the selected SDF volumes, and RMSE for the selected density volumes*

在密度体积上，以 Chameleon 模型为例，NeuralVDB 在 RMSE 仅 0.009 的条件下实现了显著压缩（Table 2），证明该方法对不同数据类型具有良好的泛化性。

### 与纯神经表示方法的比较

NeuralVDB 在与 NGLOD（Takikawa et al., CVPR 2021）、VBNF（Takikawa et al., SIGGRAPH 2022）和 INGP（Müller et al., 2022）等纯神经表示方法的对比中展现出明显优势（Table 8）。在相同模型尺寸下，NeuralVDB 在 Bunny、Armadillo、Dragon 等 SDF 几何体上的 IoU 和 mCD 均优于上述方法。率失真曲线（Fig. 16）进一步表明，NeuralVDB 在所有模型尺寸上均表现出更低的失真，即在相同的压缩比下重建精度更高，或在相同的重建精度下占用更少的存储空间。

值得注意的是，这些比较建立在公平的实验设置之上：所有方法使用相同的输入数据，非 NeuralVDB 方法同样经过超参数调优以达到类似保真度；SDF 的 IoU 目标统一设为 >99%，密度体积的 RMSE 目标均 <0.1；比较基于相同的模型尺寸，并尝试了公开和私有的采样器以保证公平性（Table 8 注释）。

### 内存占用与压缩机制分析

Table 1 详细揭示了压缩的来源。标准 VDB 中，叶节点值（32-bit）占据总内存的绝大部分。NeuralVDB [Hash,5,4,NN(3)] 仅将叶节点值替换为神经回归器，便将叶值内存占用降至原始 VDB 的 **6.268%**（约 16 倍压缩）。而 [Hash,5,NN(4),NN(3)] 配置进一步将底部两层的拓扑和值信息全部替换为神经网络，实现了整体 68 倍的极致压缩。这验证了核心洞察：VDB 树底部两层（级别 0 和级别 1）是内存占用的主要瓶颈，用小型 MLP 过拟合局部体素和瓦片信息可以消除大量显式存储冗余。

### 消融实验与关键设计选择

**稀疏域训练的有效性**：在 VDB 稀疏表示上训练（仅活动体素）相比在密集网格或仅分块稀疏网格上训练，能有效降低重建噪声并提高视觉质量（Fig. 17）。这证实了利用 VDB 树结构引导训练采样分布的重要性。

**激活函数选择**：对于平滑或非结构化模型，使用 sin 激活函数比 ReLU 能产生更光滑的重建结果，并加速收敛（Fig. 18）。这一发现与傅里叶特征映射形成互补，共同增强了 MLP 对高频细节的捕获能力。

**时间温启动编码器**：对于动画体积，将前一帧的收敛网络权重作为当前帧训练的初始化，可将训练速度提升 **1.2 倍至 3.1 倍**，并增强帧间的时间连贯性（Section 3.6）。这是 NeuralVDB 在动态场景中实现实用化的重要技术。

### 随机访问性能与设计取舍

NeuralVDB 的随机查询速度明显慢于 NanoVDB 的硬件插值（Table 6），这是论文明确声明的设计取舍——以速度换取极致压缩。具体而言，[Hash,5,4,NN(3)] 配置保留了级别 1-3 的显式树结构，随机访问仅需在叶节点处额外进行一次 MLP 回归，性能接近标准 VDB；而 [Hash,5,NN(4),NN(3)] 配置虽然内存占用更小，但随机访问需经过多层神经网络推断，速度更慢，更适合离线顺序访问场景。


![[assets/figures/papers/paper_list_l24_https_arxiv_org_abs_2208_04448/figures/021_Table_6.jpg]]
*Table 6: Random access performance measured for NanoVDB (zeroth, first, and third-order interpolation), NeuralVDB ([Hash, 5, 4, NN(3) ]), and pure neural networks (same structure as the voxel value regressor of the NeuralVDB) in milliseconds. For each static test model, 1M random samples with batch size o$f ^ { \cdot _ { 2 ^ { 1 6 } } }$ were generated within the model’s bounding box. Method NanoVDB (0) NanoVDB (1) NanoVDB (3) NeuralVDB RMSE 0.206 0.157 0.149 0.133 Table 7. RMSE measured for both NanoVDB and NeuralVDB ([Hash, 5, 4, NN(3) ]) where both grids encode a fractal Brownian motion field [Vivo and Lowe 2015]. For NanoVDB, four different sampling methods are tested (zeroth, first, and third-orde...*

### 失败模式与局限性

尽管 NeuralVDB 在大多数测试案例中表现优异，但仍存在明确的失败模式：

1. **高频复杂几何的压缩瓶颈**：对于几何特征极其复杂或高频的体积（如 Crawler 模型），压缩比仅为 13.3 倍，且重建精度有限（Table 2）。这是因为高度复杂的局部结构需要更大容量的网络来拟合，削弱了压缩优势。

2. **网络容量的人工依赖**：网络层数和宽度目前依赖启发式人工选择（Table 4），缺少自动确定最优容量的方法。Fig. 13 展示了误差随网络参数增加而收敛的趋势，但如何为每个输入自动选择帕累托最优点仍是开放问题。


![[assets/figures/papers/paper_list_l24_https_arxiv_org_abs_2208_04448/figures/017_Table_4.jpg]]
*Table 4: List of hyperparameters used in all the experiments, including subdomain size (in voxel dimension for a cubic subdomain), the number of layers and neurons per layer for the level-1 classifier (L-1 Net.), the tile value regressor, and the level-0 classifier (L-0 Net.), and the voxel value regressor. The activation function is either sin or ReLU, and if sin is used, the frequency parameters are noted. All these examples were trained using FFM, and the mapping scale and feature size are shown as well. Finally, learning rate (LR), LR decay rate and its interval, resampling interval, and maximum epochs for each example are listed. For the animation examples (LeVeque’s Test, Smoke Plume, Ship Bre...*

![[assets/figures/papers/paper_list_l24_https_arxiv_org_abs_2208_04448/figures/013_Figure_13.jpg]]
*Figure 13: EMU Crawler Fig. 13. Visualization of the error convergence as more network parameters are used. For each example, the le -most column corresponds to the baseline reconstruction where fewer parameters are used. The center column shows the result from a larger network (2× the width). The right-most column shows the ground truth. For the EMU example, the compression ratio is 40.9 and 11.4 for the smaller and larger models, respectively. For the Crawler example, the compression ratio is 13.8 and 3.8 for the smaller and larger models*

3. **静态拓扑假设**：NeuralVDB 假设树的拓扑是静态的，不支持拓扑动态变化的应用（如模拟中的拓扑改变），这限制了其在某些科学计算场景中的适用性。

4. **编码时间开销**：训练（编码）时间较长，尤其是处理如迪士尼云这样的大规模体积时，即使有温启动加速，仍可能需数百秒/帧。Table 5 的多 GPU 扩展性数据表明，稀疏域分解能提供一定的加速，但实时编码仍是挑战。

### 补充图表

![[assets/figures/papers/paper_list_l24_https_arxiv_org_abs_2208_04448/figures/010_Figure_12.jpg]]
*Figure 12: Error visualization for the Bunny Cloud example. The absolute error is averaged in z-axis*

![[assets/figures/papers/paper_list_l24_https_arxiv_org_abs_2208_04448/figures/005_Table.jpg]]

![[assets/figures/papers/paper_list_l24_https_arxiv_org_abs_2208_04448/figures/016_Table_3.jpg]]
*Table 3: List of input grid statistics for animated SDF models and density volumes: OpenVDB file sizes for both raw 32-bit precision with no compression and 16-bit precision with Blosc compression [The Blosc Development Team 2020] in MB, NeuralVDB file size with 16-bit precision with Blosc compression in MB, number of total parameters (both learnable and static) of neural networks, number of false positive patches for the classifiers, compression ratio comparing 16-bit compressed file sizes, and evaluation metrics including IoU and mCD for the selected SDF volumes, and RMSE for the selected density volumes*

![[assets/figures/papers/paper_list_l24_https_arxiv_org_abs_2208_04448/figures/022_Table.jpg]]



![[assets/figures/papers/paper_list_l24_https_arxiv_org_abs_2208_04448/figures/020_Table_5.jpg]]
*Table 5: Encoding/decoding performance measured using multiple GPUs for the static volumes. The timing in seconds and relative scaling factor is presented for each volume*

## 方法谱系与知识库定位

### 1. 核心设计理念与知识贡献

NeuralVDB 的核心洞察在于将显式稀疏树结构与隐式神经表示相结合，而非用纯神经网络完全替代传统数据结构。这一设计哲学源于对实际工业级体积数据（如迪士尼云数据集）瓶颈的深刻理解：传统稀疏体数据存储（如 **OpenVDB**，Museth, ACM TOG 2013）即使经过 16 位量化和通用压缩（如 Blosc），内存占用仍然巨大（迪士尼云达 1.5 GB）。这些方法无法利用体积内部的几何相似性和结构冗余。

因此，NeuralVDB 的因果调节变量（causal knob）是用分层神经网络（分类器和回归器）替代 VDB 树底部两层的显式节点，单独编码拓扑（活动状态）和值信息。VDB 高层节点保留粗粒度的空间划分和快速遍历能力，多个小型 MLP 过拟合于局部体素和瓦片值，从而实现数量级的压缩，同时保持 VDB 的兼容性与可扩展性。这种"过拟合即压缩"的策略与一般神经表示追求泛化的目标截然不同——NeuralVDB 刻意"记忆"输入体积，将神经网络参数本身作为紧凑的编码。

### 2. 相对于显式稀疏结构的定位

**OpenVDB**（Museth, ACM TOG 2013）和 **NanoVDB**（Museth, SIGGRAPH 2021）构成了显式稀疏体积存储的基线谱系。OpenVDB 使用四层树结构（根节点、32³ 内部节点、16³ 内部节点、8³ 叶节点），以 32 位浮点数显式存储体素值和拓扑位掩码。NanoVDB 在此基础上引入 GPU 加速和可变比特率量化，将值压缩为定点数，但仍需显式存储每个活动体素的值。

NeuralVDB 与这两者的本质区别体现在三个替换槽位：
- **底层体素值与瓦片值的存储**：从显式 32 位浮点数或量化定点数，替换为通过多个 MLP 回归器（配合傅里叶特征映射）隐式推断值，仅存储神经网络参数。
- **体素与瓦片活动状态的编码**：从每个树节点显式存储位掩码，替换为用二元分类器（级别 0）和三元分类器（级别 1）预测活动状态和子节点/瓦片类型，仅存储分类器参数。
- **底层树结构**：保留根部两级显式树（级别 2-3），将底部两级（级别 0-1）替换为层级神经网络，大幅减少节点数和内存占用。具体有两种配置：`[Hash,5,4,NN(3)]` 仅用神经网络表示叶节点值，优化随机访问速度；`[Hash,5,NN(4),NN(3)]` 用神经网络表示底部两层节点和值，优化内存占用。

定量而言，对于 Dragon 模型（标准 VDB 占用约 257 MB，32 位无压缩），`[Hash,5,NN(4),NN(3)]` 配置仅占用 3.8 MB，整体压缩因子达 68 倍（Table 1）。对于迪士尼云数据集，文件大小从 1.5 GB（OpenVDB 16-bit Blosc）降至 25 MB，压缩比达 60 倍（Fig. 1）。

### 3. 相对于纯神经表示的定位

NeuralVDB 与三类纯神经表示方法形成对比：

- **Neural Geometric Level of Detail (NGLOD)**（Takikawa et al., CVPR 2021）：基于八叉树的神经细节层次表示，通过稀疏八叉树索引特征网格，再用 MLP 解码。NeuralVDB 在相同模型尺寸下，在 SDF 几何（Bunny, Armadillo, Dragon）上的 IoU 和修改 Chamfer 距离（mCD）均优于 NGLOD（Table 8）。
- **Variable Bitrate Neural Fields (VBNF)**（Takikawa et al., SIGGRAPH 2022）：可变码率神经场，通过自适应分配网络容量实现压缩。NeuralVDB 在率失真曲线上表现更优，在所有模型尺寸上均表现出更低的失真（Fig. 16）。
- **Instant Neural Graphics Primitives (INGP)**（Müller et al., 2022）：多分辨率哈希编码的快速神经表示。NeuralVDB 在压缩效率上优于 INGP，但随机查询速度慢于 INGP 的硬件加速插值。

NeuralVDB 相对于纯神经方法的核心优势在于保留了 VDB 树的高层结构，这使得：
1. 空间查询和遍历可利用成熟的 VDB 算法，无需完全依赖神经网络推理。
2. 支持离线和在线两种解压模式：`[Hash,5,NN(4),NN(3)]` 适用于离线顺序访问（完整重建 VDB 树），`[Hash,5,4,NN(3)]` 适用于在线随机访问（仅叶节点值需回归推理）。
3. 与现有 VDB 生态系统兼容，可直接集成到基于 VDB 的渲染和模拟管线中。

### 4. 方法谱系中的独特模块

NeuralVDB 引入的若干模块在方法谱系中具有独特性：

**稀疏域分解**：将大型体积划分为固定大小的子域，每个子域配有独立的 MLP 专家，通过非可学习的门函数（帐篷函数）进行加权组合，输出为 $\hat{y} = \sum_{k=1}^{n} G(\mathbf{x})_k E_k(\mathbf{x})$。这与 sparsely-gated MoE 不同——门函数不可学习，而是基于空间位置的确定性划分，支持多 GPU 并行训练与推理。

**时间温启动编码器**：对于动画体积，前一帧的收敛网络权重作为下一帧训练的初始化，可将训练速度提升 1.2 倍至 3.1 倍，并增强动画帧间的时间连贯性（Section 3.6）。

**傅里叶特征映射**：使用 $\mathbf{z} = \gamma(\mathbf{x})$ 将输入坐标 $\mathbf{x} \in \mathbb{R}^3$ 变换为高维特征向量，帮助 MLP 捕获高频细节，这是 NeuralVDB 框架中的主要特征映射方法。

### 5. 适用边界与局限

NeuralVDB 的设计取舍明确，其适用边界由以下限制定义：

1. **静态拓扑假设**：NeuralVDB 假设树的拓扑是静态的，不支持拓扑动态变化的应用（例如模拟中的拓扑改变）。这是与动态神经表示（如 NVIDIA's NeuralVDB 后续工作）的根本区别。

2. **速度-压缩权衡**：随机查询速度明显慢于 NanoVDB 的硬件插值。`[Hash,5,4,NN(3)]` 的随机访问性能与标准 VDB 树相同，但叶节点值需额外回归推理；`[Hash,5,NN(4),NN(3)]` 的随机访问则更慢，因为需推理两层神经网络。这是论文明确声明的设计取舍（以速度换压缩）。

3. **编码时间成本**：训练（编码）时间较长，尤其是处理大规模体积时。即使有温启动加速，处理迪士尼云等大规模体积仍可能需数百秒/帧。

4. **网络容量选择**：网络容量（层数、宽度）目前依赖启发式人工选择，缺少自动确定的方法。对于几何特征极其复杂或高频的体积（如 Crawler 模型），压缩比较低（13.3x），且重建精度有限。

5. **域分解策略**：亚域分解的门函数不可学习，其固定大小的划分策略可能对某些不均匀稀疏分布的数据不够高效。

### 6. 开放问题与未来方向

基于上述局限，以下开放问题值得关注：

- 如何自动化确定每个输入体积的最佳网络容量和超参数？
- 如何在保持压缩比的同时，进一步提升随机查询的性能，使其接近传统插值方法？论文提及的主动缓存机制（如循环缓冲区缓存已评估的体素掩码/值）是一个有前景的方向。
- 对于动态树拓扑和动态值变化的场景，如何扩展 NeuralVDB？温启动策略是否会导致误差累积，尤其是在长序列中，如何保证长期时间一致性？
- 能否将其他特征映射方法（如神经哈希网格）无缝集成到框架中，以进一步提升重建质量？
- 在更大规模的分布式体积中，如何改善亚域划分的负载均衡以提高强伸缩性？
- 除了 SDF 和密度标量场，NeuralVDB 对向量场或其他复合类型数据的泛化能力如何？
- 压缩比与重建误差之间的帕累托最优前沿在不同应用领域（如科学可视化 vs 影视特效）如何变化？

## 原文 PDF

![[paperPDFs/TOG_2024/NeuralVDB_High_resolution_Sparse_Volume_Representation_using_Hierarchical_Neural_Networks.pdf]]
