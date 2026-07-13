---
title: "ExpandNets: Linear Over-parameterization to Train Compact Convolutional Networks"
type: paper
paper_level: A
venue: NeurIPS
year: 2020
pdf_ref: paperPDFs/NEURIPS_2020/ExpandNets_Linear_Over_parameterization_to_Train_Compact_Convolutional_Networks.pdf
code_link: https://github.com/GUOShuxuan/expandnets
project_link: https://github.com/GUOShuxuan/expandnets
aliases:
- ExpandNets
tags:
- NEURIPS_2020
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
core_operator: "在训练阶段，通过将每个线性层（卷积层或全连接层）替换为多个连续线性层来引入可控的过参数化；这些连续线性操作在代数上等价于原始单层，因此训练后可无损收缩回原紧凑结构。"
primary_logic: "利用连续线性操作的代数可合并性，训练时通过过参数化改善优化与泛化，推理时则无信息损失地恢复紧凑模型，实现了在不同阶段物理结构与计算代价的灵活切换。"
claims:
- "在 ImageNet 上，ExpandNet-CL 使 MobileNet 的 Top-1 准确率从 66.48% 提升至 69.40%（+2.92 pp），超越原始网络结合知识蒸馏的表现。"
- "在损坏标签的泛化测试中，ExpandNet-CK 大幅降低测试误差，如在 20% 损坏的 CIFAR-10 上误差从 SmallNet 的 20.90% 降至 19.42%，显示出更强的泛化能力。"
- "梯度困惑度分析表明，ExpandNet-CL/CK 的最小 pairwise 梯度余弦相似度显著高于紧凑网络，训练收敛更快且最终泛化误差更小。"
- "ImageNet ILSVRC2012 validation 上 Top-1 accuracy (%) = 69.40 (MobileNet ExpandNet-CL)"
---

# ExpandNets: Linear Over-parameterization to Train Compact Convolutional Networks

> [!tip] 核心洞察
> 利用连续线性操作的代数可合并性，训练时通过过参数化改善优化与泛化，推理时则无信息损失地恢复紧凑模型，实现了在不同阶段物理结构与计算代价的灵活切换。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | ExpandNets：通过线性过参数化训练紧凑卷积网络 |
| 英文题名 | ExpandNets: Linear Over-parameterization to Train Compact Convolutional Networks |
| 会议/期刊 | NeurIPS 2020 |
| Links | [paper](https://arxiv.org/abs/1811.10495) · [GitHub](https://github.com/GUOShuxuan/expandnets) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction |
| Method | ExpandNets |
| Dataset | ImageNet ILSVRC2012 validation, CIFAR-10, CIFAR-100 |

> [!tip] 效果简介
> - ImageNet ILSVRC2012 validation 上，Top-1 accuracy (%) 为 69.40 (MobileNet ExpandNet-CL)，对比 66.48 (MobileNet original)，变化 +2.92。
> - ImageNet ILSVRC2012 validation 上，Top-1 accuracy (%) 为 65.62 (MobileNetV2 ExpandNet-CL)，对比 63.75 (MobileNetV2 original)，变化 +1.87。
> - CIFAR-10 上，Top-1 accuracy (%) 为 80.27 ± 0.24 (SmallNet 7×7 ExpandNet-CK)，对比 78.63 ± 0.41 (SmallNet 7×7)，变化 +1.64。

## 概要

紧凑卷积网络（如 MobileNet、ShuffleNet 等）因参数冗余不足，在训练时面临优化困难与泛化能力弱的瓶颈。ExpandNets 提出了一种**线性过参数化**策略：在训练阶段，将紧凑网络中的每个线性层（卷积层或全连接层）替换为多个连续的线性层，不引入任何非线性激活；由于连续线性操作在代数上等价于原始单层，训练完成后可通过矩阵乘法将扩张网络无损收缩回原紧凑结构，从而在推理时完全恢复原始网络的参数量和计算量。

该方法的核心洞察在于，利用线性层的代数可合并性，在训练和推理两个阶段灵活切换物理结构与计算代价——训练时通过过参数化改善优化景观与泛化性能，推理时则零信息损失地回归紧凑形态。实验表明，ExpandNets 在不使用知识蒸馏的情况下，即可超越原始紧凑网络甚至结合知识蒸馏的版本：在 ImageNet 上，ExpandNet-CL 将 MobileNet 的 Top-1 准确率从 66.48% 提升至 69.40%（+2.92 pp）；在损坏标签的泛化测试中，ExpandNet-CK 显著降低了测试误差；梯度困惑度分析进一步揭示，ExpandNet 的训练过程具有更高的最小 pairwise 梯度余弦相似度，收敛更稳定，最终泛化误差更小。



### 紧凑网络的两难困境

深度卷积网络在图像分类、目标检测、语义分割等任务上取得了显著成功，但其庞大的参数量和计算开销严重制约了在资源受限设备上的部署。为应对这一挑战，研究者设计了多种紧凑网络架构，如 **MobileNet**、**MobileNetV2**、**ShuffleNetV2** 和 **YOLO-LITE** 等，通过深度可分离卷积、通道混洗等操作大幅压缩模型规模。

然而，一个核心瓶颈逐渐显现：**紧凑网络由于参数冗余不足，导致优化困难与泛化能力弱，难以有效训练**。具体而言，紧凑网络的损失景观中存在大量尖锐的局部极小值，梯度方向在样本间高度冲突（即梯度困惑度高），使得基于随机梯度下降的训练过程收敛缓慢且容易陷入较差的解。这一现象在卷积核尺寸较大时尤为突出——大核卷积具有更强的表达能力，但在紧凑网络中反而因优化困难而表现不佳。

### 现有解决方案的局限

为提升紧凑网络的性能，学术界主要探索了以下路径：

- **知识蒸馏（Knowledge Distillation）**：利用大型教师网络提供的软标签指导紧凑学生网络训练。该方法虽有效，但需要额外训练一个高性能教师模型，增加了流程复杂度和计算开销。
- **并行卷积扩张（如 ACNet）**：在训练时引入并行的非对称 1D 卷积，通过增加骨架权重来提升性能，测试时将并行分支合并回单一卷积核。然而，这种扩张方式仅适用于特定卷积核尺寸，且扩张自由度有限。
- **全连接层扩张（如 Arora18）**：仅对全连接层进行线性过参数化，卷积层保持不变。实验表明，这种策略在卷积主导的紧凑网络中收效甚微。

上述方法的共同缺陷在于：要么依赖外部教师信号，要么扩张策略不够通用，未能从根本上解决紧凑网络中**卷积层**的优化难题。

### 本文动机：线性过参数化的新视角

本文的核心洞察源于一个简洁的代数事实：**多个连续线性变换的复合在数学上等价于单个线性变换**。对于卷积层而言，一个 $k \times k$ 卷积可以等价地表示为稀疏矩阵乘法（Eq. 1）；对于全连接层，多个矩阵的连乘可以精确合并为单一矩阵（Eq. 4）。

这一可合并性意味着：**我们可以在训练阶段将紧凑网络的每个线性层“展开”为多个连续线性层，引入可控的过参数化以改善优化景观；训练完成后，再通过代数运算将所有展开层无损地“收缩”回原始紧凑结构。** 推理时的模型规模、计算量和推理速度与直接训练的紧凑网络完全一致，但最终精度显著更高。

基于这一思想，本文提出 **ExpandNets**——一种通用的线性过参数化训练框架，包含三种互补的扩张策略：
1. **卷积层扩张（CL）**：将 $k \times k$ 卷积替换为 $1 \times 1$、$k \times k$、$1 \times 1$ 的三层序列；
2. **卷积核扩张（CK）**：将 $k>3$ 的大卷积核等价分解为多个 $3 \times 3$ 卷积的序列；
3. **全连接层扩张（FC）**：将全连接层分解为多个窄矩阵的乘积。

如图 1 所示，这三种策略覆盖了紧凑网络的主要线性组件，且均遵循“训练时扩张、推理时收缩”的统一范式。与知识蒸馏不同，ExpandNets 无需教师网络即可超越蒸馏方法的性能；与 ACNet 等并行扩张方法相比，ExpandNets 的序列式线性扩张具有更强的代数灵活性和更广的适用性。



## 核心方法与创新机理

ExpandNets 的核心创新在于引入**训练阶段的线性过参数化**，以解决紧凑卷积网络因参数冗余不足而导致的优化困难与泛化能力弱的问题。该方法的关键洞察是：连续线性操作在代数上具有可合并性，因此可以在训练时通过扩张改善优化与泛化，在推理时则无信息损失地收缩回原始紧凑结构，实现物理结构与计算代价的灵活切换。

### 线性扩张策略

ExpandNets 提出三种线性扩张策略，分别针对卷积层、大卷积核和全连接层：

1. **卷积层扩张（Convolutional Layer Expansion, CL）**：将原始的 $k \times k$ 卷积层替换为三个连续卷积层的序列——依次为 $1 \times 1$、$k \times k$、$1 \times 1$。给定扩张率 $r$，第一层 $1 \times 1$ 的输出通道数设为 $p = r m$，中间 $k \times k$ 层的输出通道数设为 $q = r n$（其中 $m$ 和 $n$ 分别为原始层的输入和输出通道数）。通过矩阵表示，这三层可代数合并为等价于原始单层的稀疏矩阵乘积：
   $$W _ { n w ^ { \prime } h ^ { \prime } \times m w h } ^ { \boldsymbol { \mathsf { F } } } = W _ { n w ^ { \prime } h ^ { \prime } \times q w ^ { \prime } h ^ { \prime } } ^ { \boldsymbol { \mathsf { F } } ^ { 3 } } \times W _ { q w ^ { \prime } h ^ { \prime } \times p w h } ^ { \boldsymbol { \mathsf { F } } ^ { 2 } } \times W _ { p w h \times m w h } ^ { \boldsymbol { \mathsf { F } } ^ { 1 } }$$

2. **卷积核扩张（Convolutional Kernel Expansion, CK）**：对于 $k > 3$ 的卷积核，用 $l = (k-1)/2$ 个 $3 \times 3$ 卷积的序列等价表示。中间通道数同样通过扩张率 $r$ 控制：$p_1 = r m$，后续 $p_i = r n$。扩张后的序列可代数收缩回原始 $k \times k$ 卷积核。

3. **全连接层扩张（Fully-connected Layer Expansion, FC）**：将全连接层的权重矩阵分解为多个窄矩阵的乘积：
   $$W _ { n \times m } = W _ { n \times p _ { l - 1 } } \times W _ { p _ { l - 1 } \times p _ { l - 2 } } \times \cdot \cdot \cdot \times W _ { p _ { 1 } \times m }$$
   通过引入中间维度实现参数翻倍与训练过参数化。

### 与基线方法的关键差异

| 方法 | 卷积层处理 | 扩张机制 | 推理时结构 |
|------|-----------|---------|-----------|
| **Compact Network (SmallNet)** | 单一 $k \times k$ 卷积 | 无 | 原始紧凑结构 |
| **FC expansion (Arora18)** | 保持不变 | 仅扩张全连接层 | 原始结构 |
| **ACNet** | 并行 $1 \times 3$ 和 $3 \times 1$ 非对称卷积 | 增加平方核骨架权重 | 需额外合并步骤 |
| **Knowledge Distillation** | 不变 | 依赖大教师网络 | 原始紧凑结构 |
| **ExpandNets (本文)** | 序列化线性扩张（CL/CK） | 线性过参数化，无非线性激活 | 代数收缩回原始结构 |

### 因果机制

ExpandNets 的性能增益来自三个相互关联的机制：

- **降低梯度困惑度**：梯度困惑度分析（Figure 3）表明，ExpandNet-CL/CK 的最小 pairwise 梯度余弦相似度显著高于紧凑网络，梯度余弦相似度分布更集中于零附近。这意味着不同 mini-batch 的梯度方向更一致，训练收敛更快且更稳定。
- **趋向更平坦的极小值**：损失景观可视化（Figure 4）显示，ExpandNets 的 CL 和 CK 扩张策略能收敛到更平坦的极小值，这通常与更好的泛化能力相关。
- **增强泛化而非记忆**：在损坏标签的 CIFAR-10 上（Table 7），ExpandNet-CK 的测试误差显著低于紧凑网络（如 20% 损坏率下，$k=5$ 时从 20.90% 降至 19.42%），同时训练误差更高，表明扩张策略提升了泛化能力而非简单记忆训练数据。

### 扩张率的关键作用

消融实验证实，扩张率 $r > 1$ 是获得性能增益的必要条件。当 $r=0.25$ 时性能下降，而 $r=2, 4, 8$ 时性能逐步提升，验证了过参数化的关键作用。$r=4$ 被选为精度与效率的最佳平衡点。扩张后的网络在训练后通过代数收缩恢复为与原始网络完全相同的结构，因此推理时参数量、MACs 和推理时间与原始网络完全一致。



ExpandNets 遵循“训练时线性扩张，推理时代数收缩”的总体范式，其核心 pipeline 由四个功能模块构成，形成一条从紧凑网络出发、经可控过参数化训练、最终无损恢复原结构的闭环链路。

**输入**为一个预先设计好的紧凑卷积网络，其线性层（卷积层与全连接层）参数冗余不足，导致优化困难。**输出**为与原始紧凑网络**完全等价**的推理模型——参数量、乘加操作数（MACs）和推理时间均与原始网络相同，但泛化性能显著提升。

整个流程按以下模块串联执行：

1. **Convolutional Layer Expansion (CL)**  
   对任意 $k \times k$ 卷积层，将其替换为一个三层线性序列：$1 \times 1$ 卷积 → $k \times k$ 卷积 → $1 \times 1$ 卷积。给定扩张率 $r$，第一层 $1 \times 1$ 的输出通道数设为 $p = r m$（$m$ 为输入通道数），中间 $k \times k$ 层的输出通道数设为 $q = r n$（$n$ 为输出通道数）。该序列在代数上等价于原单层卷积，因此训练后可合并。

2. **Convolutional Kernel Expansion (CK)**  
   当卷积核尺寸 $k > 3$ 时，将 $k \times k$ 卷积等价表示为 $l = (k-1)/2$ 个 $3 \times 3$ 卷积的序列。中间通道数同样由扩张率 $r$ 控制：$p_1 = r m$，$p_i = r n$（$i \geq 2$）。该模块与 CL 互补，专门处理大核卷积的线性过参数化。

3. **Fully-connected Layer Expansion (FC)**  
   将全连接层的权重矩阵 $W_{n \times m}$ 分解为多个连续矩阵的乘积：
   $$W_{n \times m} = W_{n \times p_{l-1}} \times W_{p_{l-1} \times p_{l-2}} \times \cdots \times W_{p_1 \times m}$$
   中间维度 $p_i$ 大于原始维度，从而引入过参数化。此模块可独立使用，也可与 CL/CK 叠加。

4. **Algebraic Contraction**  
   训练完成后，利用连续线性操作的代数可合并性，将扩张后的多层序列通过矩阵乘法收缩回原始的单层结构。对于 CL 扩张，收缩公式为：
   $$W_{n w' h' \times m w h}^{\boldsymbol{\mathsf{F}}} = W_{n w' h' \times q w' h'}^{\boldsymbol{\mathsf{F}}^3} \times W_{q w' h' \times p w h}^{\boldsymbol{\mathsf{F}}^2} \times W_{p w h \times m w h}^{\boldsymbol{\mathsf{F}}^1}$$
   收缩后的网络与原始紧凑网络在结构上完全一致，无需任何额外的推理开销。

**模块间的数据流**：输入的紧凑网络首先按需经过 CL、CK、FC 三个扩张模块中的一种或多种组合进行线性扩张（例如 ExpandNet-CK+FC 表示同时使用卷积核扩张和全连接层扩张），得到参数量和计算量显著增大的过参数化网络；该网络在训练阶段以标准监督学习（可选择性结合知识蒸馏）进行优化；训练收敛后，Algebraic Contraction 模块将所有扩张层合并，输出与原始紧凑网络结构完全相同的推理模型。

需要指出的是，该方法**不引入任何非线性**（如激活函数）到扩张层之间，这是保证代数可收缩性的关键约束。扩张仅作用于线性层，归一化层、池化层等结构保持不变。扩张率 $r$ 是控制过参数化程度的核心超参数：$r=1$ 退化为原始网络，$r>1$ 才产生过参数化效应；实验表明 $r=4$ 在精度-效率之间取得最佳平衡。



### 3.1 卷积层的矩阵表示

ExpandNets 的核心洞察在于：任何线性层在代数上都可以被分解为多个连续线性层的乘积，而无需引入非线性。这一性质构成了“训练时扩张—推理时收缩”的数学基础。为严格描述卷积层的线性扩张与收缩，论文首先将卷积操作等价地表示为稀疏矩阵乘法。

给定输入张量 $\pmb{\mathsf{X}}_{b \times m \times w \times h}$ 和卷积核 $\pmb{\mathsf{F}}_{n \times m \times k \times k}$，输出张量 $\pmb{\mathsf{Y}}_{b \times n \times w' \times h'}$ 可写为：

$$
\pmb{\mathsf{Y}}_{b \times n \times w' \times h'} = \pmb{\mathsf{X}}_{b \times m \times w \times h} * \pmb{\mathsf{F}}_{n \times m \times k \times k} = \mathrm{reshape}\left( \pmb{W}_{n w' h' \times m w h}^{\pmb{\mathsf{F}}} \times \pmb{X}_{m w h \times b}^{v} \right)
$$

其中 $\pmb{W}^{\pmb{\mathsf{F}}}$ 是由卷积核 $\pmb{\mathsf{F}}$ 导出的稀疏矩阵（im2col 形式），$\pmb{X}^{v}$ 是输入在向量化后的矩阵表示。该等式表明，一个卷积层在数学上等价于一个特定的矩阵乘法——这为后续将单层卷积“展开”为多层序列并最终合并回单层提供了理论依据。

### 3.2 通用卷积层扩张（Convolutional Layer Expansion, CL）

对于任意 $k \times k$ 卷积层，ExpandNet-CL 将其替换为三个连续的卷积层：$1 \times 1$、$k \times k$、$1 \times 1$。扩张率 $r$ 控制中间层的通道数：

- 第一个 $1 \times 1$ 卷积的输出通道数 $p = r m$
- 中间 $k \times k$ 卷积的输出通道数 $q = r n$

三层序列在代数上等价于原始单层，其矩阵表示的合并关系为：

$$
\pmb{W}_{n w' h' \times m w h}^{\boldsymbol{\mathsf{F}}} = \pmb{W}_{n w' h' \times q w' h'}^{\boldsymbol{\mathsf{F}}^{3}} \times \pmb{W}_{q w' h' \times p w h}^{\boldsymbol{\mathsf{F}}^{2}} \times \pmb{W}_{p w h \times m w h}^{\boldsymbol{\mathsf{F}}^{1}}
$$

其中 $\pmb{W}^{\boldsymbol{\mathsf{F}}^{1}}$、$\pmb{W}^{\boldsymbol{\mathsf{F}}^{2}}$、$\pmb{W}^{\boldsymbol{\mathsf{F}}^{3}}$ 分别对应三个扩张层的稀疏矩阵表示。训练完成后，通过矩阵乘法将三个矩阵合并为单个 $\pmb{W}^{\boldsymbol{\mathsf{F}}}$，即可无损恢复原始紧凑卷积层。

**步长与填充处理**：扩张后的三层序列中，仅第一层使用填充 $p$，中间层设置步长 $s$，其余层不使用填充且步长为 1。这一设计保证了扩张序列在空间维度变换上与原始卷积层完全一致。

### 3.3 大核卷积的核扩张（Convolutional Kernel Expansion, CK）

当卷积核尺寸 $k > 3$ 时，ExpandNet-CK 将单个 $k \times k$ 卷积核替换为 $l$ 个 $3 \times 3$ 卷积的序列，其中 $l = (k - 1) / 2$。该展开的等价性来源于卷积核的可组合性：

$$
\pmb{\mathsf{F}}_{n \times m \times k \times k} = \pmb{\mathsf{F}}_{n \times p_{l-1} \times 3 \times 3}^{l} * \cdots * \pmb{\mathsf{F}}_{p_{l-1} \times p_{l-2} \times 3 \times 3}^{l-1} * \pmb{\mathsf{F}}_{p_{1} \times m \times 3 \times 3}^{1}
$$

对应的卷积操作展开为：

$$
\mathsf{Y} = \mathsf{X} * \pmb{\mathsf{F}}_{n \times m \times k \times k} = \mathsf{X} * \pmb{\mathsf{F}}_{p_{1} \times m \times 3 \times 3}^{1} * \cdots * \pmb{\mathsf{F}}_{p_{l-1} \times p_{l-2} \times 3 \times 3}^{l-1} * \pmb{\mathsf{F}}_{n \times p_{l-1} \times 3 \times 3}^{l}
$$

扩张率 $r$ 控制中间通道数：$p_1 = r m$，$p_i = r n$（$i > 1$）。训练后，所有 $3 \times 3$ 卷积核可通过连续卷积运算合并回原始的 $k \times k$ 核，恢复紧凑结构。

### 3.4 全连接层扩张（Fully-connected Layer Expansion, FC）

全连接层的线性扩张最为直接：将权重矩阵 $\pmb{W}_{n \times m}$ 分解为 $l$ 个矩阵的乘积：

$$
\pmb{W}_{n \times m} = \pmb{W}_{n \times p_{l-1}} \times \pmb{W}_{p_{l-1} \times p_{l-2}} \times \cdots \times \pmb{W}_{p_{1} \times m}
$$

其中中间维度 $p_i$ 由扩张率 $r$ 决定。训练完成后，所有矩阵相乘即恢复为原始权重矩阵。需要指出的是，论文实验表明仅扩张全连接层（FC expansion）对性能提升效果甚微（Table 1），真正带来显著增益的是卷积层的线性扩张（CL/CK）。

### 3.5 代数收缩模块

上述三种扩张策略共享同一个收缩机制：训练完成后，通过矩阵乘法或卷积核的连续卷积操作，将所有扩张层合并为原始紧凑网络的对应层。该过程是精确的代数等价变换，不引入任何近似或信息损失。收缩后的网络在参数量、MACs 和推理时间上与直接训练的紧凑网络完全相同。



## 实验与关键发现

### 核心性能增益

ExpandNets 的核心价值体现在训练-推理的结构分离：训练时通过线性过参数化改善优化与泛化，推理时通过代数收缩完全恢复为原始紧凑网络，不引入任何额外计算开销。这一特性在多个任务和架构上均带来了显著的性能提升。

在 **ImageNet ILSVRC2012** 分类任务上，ExpandNet-CL（卷积层扩张，扩张率 $r=4$）使 MobileNet 的 Top-1 准确率从 66.48% 提升至 69.40%（+2.92 pp），MobileNetV2 从 63.75% 提升至 65.62%（+1.87 pp），ShuffleNetV2 0.5× 从 55.72% 提升至 56.21%（+0.49 pp）（Table 3）。值得注意的是，**不使用知识蒸馏的 ExpandNets 在性能上已超越使用知识蒸馏训练的原始紧凑网络**，这表明过参数化训练本身即可提供优于外部教师信号引导的优化优势。

![[assets/figures/papers/paper_list_l4_https_arxiv_org_abs_1811_10495/figures/005_Table_3.jpg]]
*Table 3: Top-1 accuracy (%) on the ILSVRC2012 validation set (ExpandNets with r = 4 )*

在 **CIFAR-10/CIFAR-100** 上，以 7×7 卷积核的 SmallNet 为基线，ExpandNet-CK（卷积核扩张）分别将准确率从 78.63% 提升至 80.27%（+1.64 pp）和从 46.63% 提升至 48.55%（+1.92 pp）（Table 1）。进一步结合全连接层扩张（CK+FC）可将 CIFAR-10 准确率推至 80.31%，若再叠加知识蒸馏则达到 80.63%。

![[assets/figures/papers/paper_list_l4_https_arxiv_org_abs_1811_10495/figures/003_Table_1.jpg]]
*Table 1: Top-1 accuracy (%) of SmallNet with 7 $\times$ 7 kernels vs ExpandNets with r = 4 on CIFAR-10 and CIFAR-100*

在目标检测和语义分割等下游任务上，该方法同样有效：**YOLO-LITE** 在 PASCAL VOC2007 上的 mAP 从 27.34% 提升至 30.97%（+3.63 pp，Table 4）；**U-Net** 在 Cityscapes 验证集上的 mIOU 从 56.59 提升至 57.85（+1.26 pp，Table 5）。这表明线性扩张策略具有良好的任务泛化性。

![[assets/figures/papers/paper_list_l4_https_arxiv_org_abs_1811_10495/figures/006_Table_4.jpg]]
*Table 4: YOLO-LITE vs ExpandNet with r = 4 on the PASCAL VOC2007 test set*

![[assets/figures/papers/paper_list_l4_https_arxiv_org_abs_1811_10495/figures/007_Table_5.jpg]]
*Table 5: U-Net vs ExpandNet with r = 4 on the Cityscapes validation set*

### 消融分析：扩张策略与扩张率的关键作用

消融实验揭示了几个关键发现：

**卷积层扩张是性能增益的主要来源。** 仅扩张全连接层的 FC(Arora18) 策略几乎无法提升 SmallNet 的性能，而 CL 和 CK 扩张则带来了显著增益（Table 1）。这与后续的梯度分析一致：FC 扩张不能有效降低梯度困惑度，而卷积扩张显著改善了训练过程中的梯度一致性。

**扩张率 $r$ 必须大于 1 才能获得收益。** 当 $r=0.25$（即欠参数化）时，性能反而下降；$r=2$、4、8 时性能逐步提升，其中 $r=4$ 提供了最佳的精度-效率权衡（Table 9/Table S5）。这验证了**过参数化**而非单纯的参数重组是性能提升的根本原因。

**训练阶段的额外开销可控。** 以 SmallNet（7×7 卷积核）为基线（参数量 150.35K，MACs 6.12M，每轮训练时间 4.05s），ExpandNet-CL 在 $r=4$ 时参数量增至 562.95K，MACs 增至 25.16M，但每轮训练时间仅小幅增至 4.13s（Table 6）。这得益于现代 GPU 对矩阵运算的高效并行处理。然而，当 $r=8$ 时参数量膨胀至 8.58M，训练时间增至 9.39s，提示极大扩张率可能导致训练不稳定或内存溢出，需手动调节。

![[assets/figures/papers/paper_list_l4_https_arxiv_org_abs_1811_10495/figures/009_Table_6.jpg]]
*Table 6: Complexity analysis on CIFAR-10 for different expansion rates r. The baseline network is the SmallNet with kernel size 7 (#Params:150.35K, #MACs: 6.12M, Epoch Time: 4.05s). Note that, for a given training setting, the wall-clock time only moderately increases as r grows*

### 训练行为与泛化机制

**梯度困惑度分析**（Figure 3）为 ExpandNets 的有效性提供了机理性解释。通过测量每个训练轮次结束时 100 对随机小批次梯度的最小余弦相似度，发现 ExpandNet-CL/CK 的最小 pairwise 梯度余弦相似度显著高于紧凑网络，且其梯度余弦相似度的核密度估计更集中于零附近。这意味着过参数化训练使不同数据批次的梯度方向更加一致，降低了优化过程中的“梯度困惑”，从而加速收敛并减小最终泛化误差。相比之下，仅扩张全连接层的 FC(Arora18) 未能改善梯度一致性。

![[assets/figures/papers/paper_list_l4_https_arxiv_org_abs_1811_10495/figures/008_Figure_3.jpg]]
*Figure 3: Training behavior of networks with 7 7 kernels on CIFAR-10 (best viewed in color). Left: Training and test curves over 150 epochs. Middle: Minimum pairwise gradient cosine similarity at the end of each training epoch (higher is better). Right: Kernel density estimation of pairwise gradient cosine similarity at the end of training (over 5 independent runs)*

**损失景观可视化**（Figure 4）进一步表明，ExpandNet-CL/CK 训练得到的解倾向于收敛到更平坦的极小值区域，这通常与更好的泛化能力相关联。

![[assets/figures/papers/paper_list_l4_https_arxiv_org_abs_1811_10495/figures/011_Figure_4.jpg]]
*Figure 4: Loss landscapes of networks with 9 × 9 kernels on CIFAR-10 (We report top-1 error (%))*

**损坏标签实验**（Table 7）直接检验了泛化能力。在 20% 标签损坏的 CIFAR-10 上，ExpandNet-CK 将 SmallNet（$k=5$）的测试误差从 20.90% 降至 19.42%；在 $k=9$ 配置下，最佳测试误差从 20.55% 降至 19.32%。在所有涉及卷积扩张的损坏标签实验中，ExpandNets 几乎一致地产生更小的泛化误差，同时训练误差更高——这表明性能提升源于更好的泛化，而非对噪声的过拟合。

![[assets/figures/papers/paper_list_l4_https_arxiv_org_abs_1811_10495/figures/010_Table_7.jpg]]
*Table 7: Generalization ability on Corrupted CIFAR-10. We report the top-1 error (%). Note that our ExpandNets yield smaller generalization errors than the compact network in almost all cases involving convolutional expansion. By contrast expanding FC layers often does not help*

### 初始化效应与复合策略

一个值得注意的细节是：**使用非线性对应版本初始化 ExpandNet 可进一步提升最终精度**（Table S1、S2）。例如在 CIFAR-10/100 和 PASCAL VOC 上，标记为 +Init 的变体均展现出更高的准确率。这表明扩张网络的初始权重质量对最终性能有额外影响。

**初始化消融实验**（Table 8）排除了“性能提升仅来自更好的初始化”这一替代解释：将紧凑网络初始化为已训练的 ExpandNet 的收缩权重，并不能一致地超越直接训练 ExpandNet 的性能。因此，过参数化训练过程本身——而非其产生的初始点——是性能增益的核心驱动力。

**与知识蒸馏的协同效应**：ExpandNets 可与知识蒸馏叠加使用。例如在 CIFAR-10 上，SmallNet 结合 KD 的准确率为 79.72%，而 ExpandNet-CK+FC 结合 KD 达到 80.63%（Table 1）；在 ImageNet 上，MobileNet 结合 KD 为 68.38%，而 ExpandNet-CL 结合 KD 达到 69.51%（Table 3）。这表明线性过参数化与知识蒸馏是互补的优化策略。

### 失败模式与适用边界

**仅扩张全连接层无效。** FC(Arora18) 在分类精度、梯度困惑度、损坏标签泛化等多个指标上均未表现出相对于紧凑基线的优势，说明过参数化的收益高度依赖于扩张卷积层带来的表征灵活性。

**极度扩张可能导致训练不稳定。** $r=8$ 时参数量和计算量急剧膨胀，训练时间显著增加，且论文未报告更大扩张率的实验结果，暗示存在实际可用的扩张率上限。

**对小卷积核的收益有限。** 当卷积核尺寸为 3×3 时，CK 扩张策略不可用（因为 $k=3$ 时 $l=(3-1)/2=1$，无扩张空间），仅能依赖 CL 扩张。此时性能增益主要来自 1×1 卷积引入的通道维度过参数化。

**训练时间增加是固有的权衡。** 尽管推理时完全无额外开销，训练阶段的 wall-clock time 在 $r=4$ 时约增加 2~4 倍（Table 6），这对于大规模训练任务可能构成实际约束。

### 方法有效性总结

ExpandNets 的有效性可归因于三个相互关联的机制：
1. **过参数化改善优化景观**：扩张后的网络具有更平坦的损失景观和更低的梯度困惑度，使 SGD 更容易找到泛化良好的解。
2. **代数等价保证无损压缩**：训练后通过矩阵乘法将扩张层合并，精确恢复原始紧凑结构，推理时零额外代价。
3. **与现有技术的兼容性**：可与知识蒸馏、更优初始化策略等结合，形成复合优化方案。

该方法的主要局限在于训练阶段的计算开销、对卷积层结构的依赖，以及扩张率需手动调节。对于更深或更宽的现代大规模网络（如 ResNet-50 及以上），其可扩展性尚未验证，这是未来工作的重要方向。

### 补充图表

![[assets/figures/papers/paper_list_l4_https_arxiv_org_abs_1811_10495/figures/024_Figure.jpg]]
*Figure: S2: Training behavior of networks on CIFAR-10 (best viewed in color). Left: Training and test curves over 150 epochs. Middle: Minimum pairwise gradient cosine similarity at the end of each training epoch (higher is better). Right: Kernel density estimation of pairwise gradient cosine similarity at the end of training (over 5 independent runs)*

![[assets/figures/papers/paper_list_l4_https_arxiv_org_abs_1811_10495/figures/025_Figure.jpg]]
*Figure: (a) kernel size: 3 (b) kernel size: 5 (c) kernel size: 7 (d) kernel size: 9*

![[assets/figures/papers/paper_list_l4_https_arxiv_org_abs_1811_10495/figures/027_Figure.jpg]]
*Figure: S4: Product L ^ { 2 } vs Normal L ^ { 2 } (best viewed in color). Left: Training curves of the overall loss function. Middle Left: Training curves of the cross-entropy. Middle Right: Curves of training errors. Right: Curves of test errors. (Note that the y - axis is in log scale.)*

![[assets/figures/papers/paper_list_l4_https_arxiv_org_abs_1811_10495/figures/004_Table_2.jpg]]
*Table 2: Top-1 accuracy (%) of MobileNets vs ExpandNets with r = 4 on CIFAR-10 and CIFAR-100*



## 定位与知识库关联

### 1. 与基线方法的关系

ExpandNets 的核心机制——在训练阶段引入线性过参数化、测试阶段通过代数等价性无损收缩——与若干现有工作存在明确的方法学关联与差异。

**与全连接层扩展（Arora18）的关系。** 早期工作已探索仅对全连接层进行线性扩展以改善训练，但该方法在卷积网络上的效果甚微。ExpandNets 的实验直接验证了这一局限：在 CIFAR-10 上，仅扩展全连接层的 FC(Arora18) 变体未能带来显著的准确率提升，其梯度困惑度与收敛行为与原始紧凑网络几乎一致（Figure 3）。这表明，卷积层的过参数化才是改善紧凑网络训练动态的关键杠杆，单纯的全连接层扩展不足以解决卷积网络优化困难的根本问题。

**与 ACNet 的关系。** ACNet 通过在训练阶段引入并行的 1D 非对称卷积来增加平方核的骨架权重，训练后将并行分支吸收回原始卷积核。ExpandNets 与 ACNet 共享“训练时扩展、推理时收缩”的哲学，但实现路径不同：ACNet 采用**并行分支**的方式增加表达能力，而 ExpandNets 采用**串行多层**的线性分解。这一差异在方法设计上意味着：ACNet 的扩展受限于特定核形状的组合，而 ExpandNets 的串行分解对任意 $k \times k$ 卷积具有普适性，且可通过扩张率 $r$ 灵活控制过参数化程度。

**与知识蒸馏（Knowledge Distillation）的关系。** 知识蒸馏通过大型教师网络的软标签指导学生网络训练，是提升紧凑模型性能的常用手段。ExpandNets 在无教师网络的条件下，超越了使用知识蒸馏的原始紧凑网络：在 ImageNet 上，ExpandNet-CL 使 MobileNet 的 Top-1 准确率达到 69.40%，而使用知识蒸馏的原始 MobileNet 仅达到 68.40%（Table 3）。此外，ExpandNets 可与知识蒸馏结合使用，进一步叠加收益。这表明线性过参数化与知识迁移之间存在互补而非替代的关系。

**与直接训练紧凑网络的关系。** 直接训练原始紧凑网络（SmallNet）是 ExpandNets 最基础的对比基线。实验一致表明，在所有测试的架构（SmallNet、MobileNet、MobileNetV2、ShuffleNetV2、YOLO-LITE、U-Net）和任务（图像分类、目标检测、语义分割）上，ExpandNets 均显著优于直接训练，且推理阶段的计算代价完全相同。

### 2. 适用边界

ExpandNets 的设计决定了其适用范围存在明确的边界条件。

**适用结构。** 线性扩张策略专门针对卷积层和全连接层设计。对于归一化层（Batch Normalization）、池化层、激活函数等非线性组件，论文未提供对应的扩张方法。在实际应用中，ExpandNets 的扩张单元插入在卷积层或全连接层的位置，而 BN 和 ReLU 等非线性层保持在扩张单元之间或之后，维持网络整体的非线性表达能力。

**适用模型规模。** 实验验证主要集中在紧凑或轻量级模型上，包括 SmallNet、MobileNet 系列、ShuffleNetV2、YOLO-LITE 和 U-Net。对于更深或更宽的现代大规模网络（如 ResNet-50 及以上），论文未提供实验验证，因此该方法在大模型上的可扩展性和有效性仍是一个开放问题。

**适用卷积核大小。** 卷积层扩展（CL）适用于任意 $k \times k$ 卷积核；卷积核扩展（CK）专门针对 $k > 3$ 的大核卷积，通过 $l = (k-1)/2$ 个 $3 \times 3$ 卷积序列实现等价表示。对于 $k=3$ 或 $k=1$ 的卷积，CK 策略不适用，但 CL 策略仍然有效。

**扩张率的选择。** 扩张率 $r$ 是控制过参数化程度的关键超参数。实验表明 $r$ 必须大于 1 才能获得性能增益：当 $r=0.25$ 时性能反而下降，$r=2、4、8$ 时性能逐步提升（Table S5）。$r=4$ 在多数实验中提供了最佳的精度-效率折中。极大扩张率（如 $r=8$）可能导致训练不稳定或内存溢出，且扩张率的选取目前依赖手动调节，缺乏自动搜索机制。

### 3. 局限与开放问题

**训练成本增加。** 训练阶段因扩张而引入额外的参数和计算量。例如，在 CIFAR-10 上 SmallNet 的 ExpandNet-CL（$r=4$）参数量从 150.35K 增至 562.95K，MACs 从 6.12M 增至 25.16M，单轮训练时间增加约 2~4 倍（Table 6）。尽管测试时可通过代数压缩完全恢复为原始规模，训练成本的增加在资源受限场景下仍是一个实际约束。

**初始化策略的改进空间。** 论文探索了使用非线性对应版本（即插入 ReLU 的扩张网络）预训练权重来初始化 ExpandNet 的策略（+Init 变体），该策略可进一步改善最终准确率（Table S1, S2）。然而，这一策略增加了额外的预训练步骤。能否设计更高效的扩张参数初始化方法，以缩短训练时间或进一步提升精度，仍是一个开放问题。

**与现代架构的集成。** 如何将线性扩张有效集成到更深的现代架构（如 ResNet-50 及以上）而不产生不稳定的训练行为，论文未给出答案。深层网络中的残差连接、瓶颈结构等组件与线性扩张的交互效应需要进一步研究。

**与网络压缩技术的协同。** 线性扩张与网络剪枝、量化等压缩技术是否存在协同效应，论文未涉及。一个自然的问题是：先扩张训练再收缩，与先训练再剪枝，两者在最终模型质量和训练效率上是否存在互补或替代关系。

**最优过参数化程度的理论理解。** 论文从实验角度展示了扩张率 $r$ 对性能的影响，但未提供关于最优过参数化程度的理论分析。是否存在一个理论上可刻画的最优扩张程度，能够在训练效率与最终泛化性能之间取得最佳平衡，仍是一个开放的理论问题。



## 原文 PDF

![[paperPDFs/NEURIPS_2020/ExpandNets_Linear_Over_parameterization_to_Train_Compact_Convolutional_Networks.pdf]]
