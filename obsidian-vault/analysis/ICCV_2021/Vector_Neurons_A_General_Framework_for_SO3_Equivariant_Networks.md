---
title: "Vector Neurons: A General Framework for SO(3)-Equivariant Networks"
type: paper
paper_level: A
venue: ICCV
year: 2021
pdf_ref: paperPDFs/ICCV_2021/Vector_Neurons_A_General_Framework_for_SO_3_Equivariant_Networks.pdf
code_link: https://github.com/FlyingGiraffe/vnn
project_link: "https://cs.stanford.edu/~congyue/vnn/"
aliases:
- VN
- VNGFS3EN
tags:
- ICCV_2021
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
core_operator: "Vector Neurons"
primary_logic: "Vector Neurons"
claims:
- "Vector Neurons"
---

# Vector Neurons: A General Framework for SO(3)-Equivariant Networks

> [!tip] 核心洞察
> Vector Neurons

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | Vector Neurons: A General Framework for SO(3)-Equivariant Networks |
| 英文题名 | Vector Neurons: A General Framework for SO(3)-Equivariant Networks |
| 会议/期刊 | ICCV 2021 |
| Links | [paper](https://arxiv.org/abs/2104.12229) · [GitHub](https://github.com/FlyingGiraffe/vnn) · [Project](https://cs.stanford.edu/~congyue/vnn/) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction |
| Method | Vector Neurons (VN) |
| Dataset | ModelNet40, ShapeNet Part, ShapeNet Occupancy |

> [!tip] 效果简介
> 本笔记的既有实验指标、对比结果与适用边界见“实验与关键发现”；本轮仅统一结构，不改写证据。

## 概要

三维旋转不变性（或等变性）是点云深度学习中的核心挑战。传统网络将特征表示为标量序列，对任意 SO(3) 旋转不具备结构化的鲁棒性——在训练时仅使用对齐数据（无旋转增强）的 DGCNN，面对 SO(3) 随机旋转的测试数据时，分类准确率从 90% 以上暴跌至 16.6%（Table 4）。这一性能坍塌揭示了根本瓶颈：**标量神经元缺乏对三维旋转的结构化感知能力，网络必须通过大量数据增强“记忆”旋转模式，而非“理解”旋转几何**。

本文提出 **Vector Neurons (VN)** 框架，将神经元表示从标量 $z \in \mathbb{R}$ 提升为三维向量 $v \in \mathbb{R}^3$，使潜在特征从“标量序列”变为“三维点序列”（即矩阵 $\mathcal{V} \in \mathbb{R}^{C \times 3}$）。基于这一表示，作者构建了一套完整的 SO(3)-等变神经网络工具箱，包括线性层、非线性层、池化层和归一化层，均满足旋转等变性条件 $f(\mathcal{V}R; \theta) = f(\mathcal{V}; \theta)R$。其核心机理在于：**线性层直接作用于向量通道的线性组合，非线性层通过可学习方向 $k$ 对向量进行半空间裁剪，池化层基于可学习内积选择最匹配的向量通道，归一化层仅作用于旋转不变的向量二范数**——所有操作均与旋转交换，从而将等变性内建于网络结构。

在方法谱系中，VN 框架定位为 **SO(3)-等变点云网络的通用构建范式**，区别于两类主流路线：（1）基于数据增强的标量网络（如 PointNet、DGCNN、PointNet++），它们通过大量旋转增强来近似不变性，但缺乏结构化的等变保证；（2）基于球谐函数或群卷积的等变网络（如 TFN、SE(3)-Transformers），它们具有理论等变性，但实现复杂、计算开销大。VN 的优势在于将等变性简化为对向量列表的线性操作，可直接嵌入现有点云架构（如 DGCNN、PointNet、Occupancy Networks），形成 VN-DGCNN、VN-PointNet、VN-OccNet 等变体。

关键实验结果验证了框架的有效性：**在 ModelNet40 分类任务上，VN-DGCNN 在 I/SO(3) 设定下达到 90.0% 准确率，相比标量 DGCNN 的 16.6% 提升 73.4 个百分点**（Table 4）；在 ShapeNet 部件分割任务上，VN-DGCNN 在相同设定下达到 81.5 mIoU（Table 5）。这些结果表明，VN 框架使网络无需旋转增强即可自然泛化到任意 SO(3) 旋转，从根本上解决了标量网络对旋转数据的脆弱性问题。

三维视觉任务中，点云数据的旋转鲁棒性是一个长期存在的核心挑战。传统深度网络处理点云时，将每个点的三维坐标视为标量特征的有序序列，这种表示方式天然缺乏对三维旋转的结构化感知能力。当输入点云经历任意 SO(3) 旋转时，网络的内部表示会发生不可预测的变化，导致性能急剧下降。

现有的应对策略主要分为两类，但各自存在明显局限。**数据增强**是应用最广泛的手段——在训练过程中对输入施加随机旋转，迫使网络通过大量样本隐式学习旋转不变性。然而，这种做法本质上是“暴力”的：它要求网络消耗大量容量去拟合旋转群的所有可能变换，却无法提供任何理论保证。当测试时遇到训练分布之外的旋转模式时，性能依然可能崩溃。**手工设计的旋转不变特征**（如点对距离、角度等几何量）虽然能保证不变性，但丢弃了方向信息，限制了网络对细粒度几何结构的表达能力。

近年来，**群等变性（Group Equivariance）** 为这一问题提供了新的理论框架。其核心思想是：与其让网络输出对旋转不变，不如让网络的内部表示随输入同步旋转，即满足 $f(\mathbf{X} \mathbf{R}) = f(\mathbf{X}) \mathbf{R}$。这样，通过精心约束每一层的计算形式，整个网络就天然具备了结构化的旋转感知能力，无需依赖数据增强即可应对任意 SO(3) 变换。然而，将这一框架真正落地到点云网络面临关键瓶颈：现有等变架构多针对二维图像或体素网格设计，直接迁移到不规则、无序的点云数据时，如何定义等价的线性层、非线性激活、归一化和池化操作，缺乏系统性的构建方案。

本文的核心动机正是填补这一空白：**提出一套通用的、可直接嵌入现有点云网络架构的 SO(3)-等变网络构建工具箱**。作者观察到，关键突破口在于提升神经元表示本身的维度——将传统标量神经元（scalar neurons）推广为三维向量神经元（Vector Neurons, VN），使潜在表示从标量序列变为三维向量序列（即矩阵形式）。这一表示层面的跃升，使得线性层天然保持等变性，并为设计等变的非线性、归一化和池化操作铺平了道路，从而能够以最小的架构改动代价，将标准点云网络（如 PointNet、DGCNN）升级为完全旋转等变的版本。

## 核心方法与创新机理

Vector Neurons 的核心创新在于将点云网络的**潜在表示空间从标量序列提升为三维向量序列**，并围绕这一表示构建了一套完整的、可组合的 SO(3)-等变神经网络工具箱。这一设计带来了三个相互关联的关键突破：

### 1. 表示空间的维度提升：从标量到三维向量

传统深度学习网络中的神经元输出为无序标量列表 $\{z_1, z_2, \ldots, z_C\}$，这种表示在旋转变换下不具备结构化的变换规律。VN 框架将每个神经元从标量 $z \in \mathbb{R}$ 提升为三维向量 $\mathbf{v} \in \mathbb{R}^3$，使得一层特征表示为一个矩阵 $\mathcal{V} \in \mathbb{R}^{C \times 3}$——即 $C$ 个三维向量的有序集合。这一表示选择的根本优势在于：旋转操作可以直接作用于表示空间，即 $\mathcal{V} \mapsto \mathcal{V}R$，其中 $R \in \mathrm{SO}(3)$。

### 2. 等变性作为构造性质而非约束条件

VN 框架的关键设计原则是：**等变性不是通过损失函数中的正则化项或数据增强来近似实现的，而是网络基本操作的构造性质**。具体而言：

- **线性层**：定义 $f_{\mathrm{lin}}(\mathcal{V}; \mathbf{W}) = \mathbf{W}\mathcal{V}$，其中 $\mathbf{W} \in \mathbb{R}^{C' \times C}$。由于 $\mathbf{W}(\mathcal{V}R) = (\mathbf{W}\mathcal{V})R$，该操作天然满足等变性，无需对权重矩阵施加任何约束（如权重共享或张量积分解），从而保留了标准线性层的全部表达能力和参数效率。

- **非线性层**：通过引入可学习方向 $\mathbf{k}$，将输入向量 $\mathbf{q}$ 分解为沿 $\mathbf{k}$ 方向的分量和垂直于 $\mathbf{k}$ 的分量，仅对前者进行裁剪：
  $$\mathbf{v}' = \begin{cases} \mathbf{q} & \text{if } \langle \mathbf{q}, \mathbf{k} \rangle \geq 0 \\ \mathbf{q} - \left\langle \mathbf{q}, \frac{\mathbf{k}}{\|\mathbf{k}\|} \right\rangle \frac{\mathbf{k}}{\|\mathbf{k}\|} & \text{otherwise} \end{cases}$$
  其中 $\mathbf{q} = \mathbf{W}\mathcal{V}$，$\mathbf{k} = \mathbf{U}\mathcal{V}$ 均由输入特征经可学习线性变换得到。由于 $\mathbf{k}$ 随输入旋转而协变，该非线性操作保持等变性。

- **池化层**：基于可学习键 $\mathbf{K}$ 的向量内积对齐机制选择最具代表性的特征向量，避免标量池化破坏等变结构。

- **归一化层**：仅对向量二范数（旋转不变量）进行批归一化，保留向量方向的等变信息。

这套操作符的组合封闭性意味着：任意 VN 层的堆叠自动保持等变性，无需逐层验证或额外约束。

### 3. 与现有架构的无缝集成

VN 框架的另一个关键创新在于其**即插即用的设计理念**。通过将标准架构中的每层形状从 $N$（标量神经元数）替换为 $\lfloor N/3 \rfloor \times 3$（向量神经元数），VN 可以直接嵌入 PointNet、DGCNN 等现有网络，参数总量约降至原来的 $\leq 2/9$，但在旋转场景下性能大幅提升。以 ModelNet40 分类为例，DGCNN 在 $z/\mathrm{SO}(3)$ 设置下准确率仅 16.6%，而 VN-DGCNN 达到 90.0%，增益高达 **+73.4 个百分点**（Table 4）。这种架构兼容性使得 VN 框架无需重新设计网络拓扑即可获得旋转鲁棒性。

Vector Neurons 框架的核心设计理念是将传统神经网络中的标量神经元提升为三维向量神经元，从而构建一套天然具备 SO(3) 等变性的网络构建模块。整个框架围绕 **VN 表示** 展开：每一层的潜在表示不再是标量序列，而是一个矩阵 $\mathcal{V} \in \mathbb{R}^{C \times 3}$，即 $C$ 个三维向量的有序列表。这种表示形式使得旋转操作可以直接作用于特征空间——对输入点云施加旋转 $R \in \text{SO}(3)$，等价于对每层的 VN 表示右乘 $R$。

框架的 pipeline 由以下核心模块级联构成，所有模块均满足旋转等变性条件 $f(\mathcal{V} R; \theta) = f(\mathcal{V}; \theta) R$：

1. **VN 线性层**：将权重矩阵 $\mathbf{W} \in \mathbb{R}^{C' \times C}$ 直接作用于 VN 表示，输出 $V' = \mathbf{W} V$。由于矩阵乘法与旋转右乘可交换，该层天然等变。

2. **VN 非线性层**：推广 ReLU 到向量域。通过学习一个方向向量 $k = \mathbf{U} V$ 和查询向量 $q = \mathbf{W} V$，根据 $\langle q, k \rangle$ 的符号对 $q$ 进行选择性截断：若内积非负则保留 $q$，否则减去 $q$ 在 $k$ 方向上的分量。该操作保持了旋转等变性。

3. **VN 池化层**：全局池化通过可学习的键向量 $\mathbf{W}$ 与每个通道向量做内积，选取内积最大的那个向量作为该通道的全局特征，实现等变的全局聚合。

4. **VN 归一化层**：对 VN 表示的旋转不变量（即每个向量的二范数）进行批归一化，再将归一化后的范数比例回乘到原向量上，从而在不破坏方向信息的前提下稳定训练。

5. **VN 不变层**：当任务需要旋转不变的输出时，可通过计算 VN 表示的不变量（如向量范数、内积等）将等变特征转化为不变特征，输入后续的标量网络（如 ResNet）进行预测。

在具体网络实例化中，框架将经典点云架构（如 PointNet、DGCNN）的每一层替换为对应形状的 VN 层，即标量层维度 $N$ 映射为 $\lfloor N/3 \rfloor \times 3$ 的向量层。这种设计使参数量降至标量版本的约 $2/9$。以 **VN-DGCNN** 为例，输入点云经过边缘卷积提取局部几何特征后，逐层通过 VN 线性层、非线性层和池化层，最终输出等变的全局特征或不变的任务预测。对于隐式重建任务，编码器 **VN-PointNet** 输出全局向量列表特征 $\mathbf{Z} \in \mathbb{R}^{C \times 3}$，解码器则利用三个旋转不变量 $\langle \mathbf{x}, \mathbf{Z} \rangle$、$\|\mathbf{x}\|^2$ 和 $\text{VN-In}(\mathbf{Z})$ 作为输入，通过标准 ResNet 预测占用值，实现编码器等变、解码器不变的整体架构。

### 向量神经元表示

Vector Neuron 的核心创新在于将传统标量神经元提升为三维向量表示。给定一层特征，标量网络输出有序标量序列，而 VN 将其替换为有序的三维向量序列，形成矩阵表示 $\mathcal{V} \in \mathbb{R}^{C \times 3}$，其中 $C$ 为通道数。该表示要求网络层映射 $f$ 满足旋转等变性：

$$f(\mathcal{V} R; \theta) = f(\mathcal{V}; \theta) R$$

即对输入施加旋转 $R \in \mathrm{SO}(3)$ 与经过网络层映射可交换。

### 线性层

VN 线性层直接对向量列表特征施加可学习权重矩阵 $\mathbf{W} \in \mathbb{R}^{C' \times C}$：

$$V' = f_{\mathrm{lin}}(V; \mathbf{W}) = \mathbf{W} V \in \mathbb{R}^{C' \times 3}$$

该操作对任意旋转 $R$ 满足 $f_{\mathrm{lin}}(V R; \mathbf{W}) = \mathbf{W} V R = f_{\mathrm{lin}}(V; \mathbf{W}) R$，等变性由矩阵乘法的结合律自然保证。

### 非线性层

VN 非线性层推广了 ReLU 到向量域，核心机制是利用可学习方向向量对输入特征进行半空间裁剪。具体步骤：

1. 从输入特征 $V \in \mathbb{R}^{C \times 3}$ 通过两个线性映射分别得到查询向量 $q$ 和方向向量 $k$：
   $$q = \mathbf{W} V, \quad k = \mathbf{U} V$$
   其中 $\mathbf{W}, \mathbf{U} \in \mathbb{R}^{1 \times C}$ 为可学习参数。

2. 非线性操作根据 $q$ 与 $k$ 的内积符号进行分支处理：
   $$v' = \begin{cases} q & \text{if } \langle q, k \rangle \geq 0 \\ q - \left\langle q, \frac{k}{\|k\|} \right\rangle \frac{k}{\|k\|} & \text{otherwise} \end{cases}$$

当 $q$ 位于 $k$ 定义的半空间内时保持不变，否则将其投影到与 $k$ 正交的超平面上，实现类似 ReLU 的“截断”效果。该操作对旋转等变，因为 $k$ 和 $q$ 均随输入同步旋转。

### 池化层

VN 全局池化不直接对向量取 max，而是通过可学习的关键向量 $\mathbf{W}$ 选择与之最对齐的特征向量：

$$f_{\mathrm{MAX}}(\mathcal{V})[c] = V_{n^{*}}[c], \quad n^{*}(c) = \underset{n}{\arg\max} \, \langle \mathbf{W} V_n[c], V_n[c] \rangle$$

该设计在保持旋转等变性的同时，实现了对点云全局特征的聚合。

### 归一化层

由于批次内样本可能处于不同姿态，直接对向量特征做批归一化会破坏等变性。VN 的解决方案是仅对旋转不变量——向量的二范数进行归一化：

$$N_b = \mathrm{ElementwiseNorm}(V_b) \in \mathbb{R}^{N \times 1}$$
$$\{N_b'\} = \mathrm{BatchNorm}(\{N_b\})$$
$$V_b'[c] = V_b[c] \frac{N_b'[c]}{N_b[c]}$$

通过缩放向量范数而非向量方向，既实现了训练稳定，又保持了旋转等变性。

### 不变特征提取

从等变特征 $Z \in \mathbb{R}^{C \times 3}$ 构造旋转不变特征的方式包括：向量的二范数 $\|x\|^2$、内积 $\langle x, Z \rangle$，以及通过对 $Z$ 做 VN-Invariant 变换得到的不变表示。这些不变特征被用于下游任务（如隐式重建的解码器），实现等变编码器与不变解码器的组合。

## 实验与关键发现

### 4.1 实验设置与评估协议

为验证Vector Neuron框架在任意SO(3)旋转下的鲁棒性，本文在三个核心三维视觉任务上进行了系统评估：点云分类（ModelNet40）、部件分割（ShapeNet Part）与神经隐式重建（ShapeNet Occupancy）。实验采用三种训练/测试协议刻画方法对旋转的泛化能力：

- **z/z**：训练与测试数据均仅绕竖直轴随机旋转增强（对齐设定）。
- **z/SO(3)**：训练数据仅绕竖直轴增强，测试数据施加任意SO(3)旋转。
- **SO(3)/SO(3)**：训练与测试数据均施加任意SO(3)旋转增强。

其中z/SO(3)协议是检验旋转泛化能力的关键压力测试：模型在训练期间从未见过任意SO(3)姿态，却在测试时被要求处理完全随机的三维旋转。VN网络在所有协议下均保持一致的性能，而传统网络在z/SO(3)下出现灾难性退化。

VN网络的实现遵循其标量对应架构，但将每层形状改为 $\lfloor N/3 \rfloor \times 3$，参数量约为标量版本的 $2/9$。VN-PointNet在输入层额外引入边卷积，将 $\mathbb{R}^{1 \times 3}$ 特征映射至 $\mathbb{R}^{C \times 3}$（$C>1$），以满足后续逐点VN-MLP的通道数要求。

---

### 4.2 ModelNet40分类：主结果

**表1**（原文Table 1）报告了ModelNet40分类精度。VN-DGCNN在SO(3)/SO(3)协议下达到 **90.2%**，在z/SO(3)协议下达到 **90.0%**，性能几乎不随训练旋转增强策略变化。相比之下，标量DGCNN在z/SO(3)下骤降至 **16.6%**（表4），退化幅度超过73个百分点。

| 方法 | z/z | z/SO(3) | SO(3)/SO(3) |
|------|-----|---------|-------------|
| DGCNN（标量） | 92.9 | 16.6 | 90.1 |
| VN-DGCNN | 90.5 | 90.0 | 90.2 |

**表4**（原文Table 4）进一步揭示了仅在z对齐数据上训练时各方法的泛化鸿沟：所有标量方法（PointNet、PointNet++、DGCNN）在z/SO(3)下精度均低于20%，而VN-DGCNN保持90.0%。这一对比直接验证了SO(3)-等变性的核心价值——网络无需在训练阶段穷举所有旋转姿态即可在测试时泛化至任意SO(3)旋转。

VN-PointNet在SO(3)/SO(3)下达到 **88.5%**，显著优于其标量对应版本（PointNet在z/SO(3)下仅13.2%）。与其他等变架构相比，VN-DGCNN在SO(3)/SO(3)设定下处于领先地位。

---

### 4.3 ShapeNet部件分割

**表2**（原文Table 2）报告了ShapeNet部件分割的平均类别mIoU。VN-DGCNN在z/SO(3)与SO(3)/SO(3)两种协议下均达到 **81.4%**，且与z/z设定下的性能（81.5%）无显著差异。这表明VN框架在密集预测任务上同样实现了旋转无关的稳定输出。

标量DGCNN在z/SO(3)下mIoU急剧下降至 **37.4%**，再次验证了非等变方法在分布外旋转下的脆弱性。VN-PointNet在SO(3)/SO(3)下达到 **79.5%**，略低于VN-DGCNN，但同样保持跨协议一致性。

---

### 4.4 神经隐式重建

**表3**（原文Table 3）报告了ShapeNet体素占用率重建的volumetric mIoU。VN-OccNet采用旋转等变编码器（VN-PointNet）与旋转不变解码器的组合设计：

- 编码器输出全局向量列表特征 $\mathbf{Z} \in \mathbb{R}^{C \times 3}$。
- 解码器利用三个旋转不变量：$\langle \mathbf{x}, \mathbf{Z} \rangle$（内积）、$\|\mathbf{x}\|^2$（查询点模长）、$\text{VN-In}(\mathbf{Z})$（VN不变特征），经ResNet输出占用概率。

在I/I（无旋转）协议下，VN-OccNet与标量OccNet性能接近（轻微损失）；在SO(3)/SO(3)协议下，VN-OccNet保持稳定，而标量OccNet无法泛化。这一结果说明等变编码器提取的几何特征在旋转下与查询点保持正确的相对关系，使不变解码器能够自然利用该信息。

---

### 4.5 消融研究

#### 4.5.1 池化策略

**表7**（原文Table 7）比较了VN-MAX池化（基于学习到的key对齐选择）与标准MEAN池化（天然保持等变性）。两者在分类精度上表现相当，MEAN池化在部分设定下略优。这表明简单的均值聚合已能有效保留旋转等变信息，而基于学习的MAX池化并未带来显著增益。

#### 4.5.2 非线性层设计

**表6**（原文Table 6，需手动核实具体数值）比较了纠缠式线性-ReLU层与解耦的线性层+VN-非线性层组合。解耦设计（即先线性变换再施加向量非线性）在z/SO(3)协议下显著优于纠缠设计，验证了将非线性操作独立于线性变换、且基于学习方向进行向量级裁剪的必要性。

#### 4.5.3 训练数据旋转增强的影响

表4的对比已构成天然消融：当仅在z对齐数据上训练时，VN-DGCNN在z/SO(3)下精度为90.0%，而标量DGCNN为16.6%。这表明VN框架的泛化能力来源于架构层面的等变性，而非数据增强的覆盖度。

---

### 4.6 失败模式与局限性

1. **平移等变性缺失**：当前VN框架仅保证SO(3)旋转等变性，未扩展至SE(3)（含平移）。所有输入点云需预先中心化至原点，在真实场景中需额外的平移归一化步骤。文中将SE(3)等变性列为开放问题。

2. **标量输入通道的等变性退化**：当输入特征通道数 $C=1$ 时（如原始点云仅含三维坐标），VN-PointNet需通过边卷积先提升通道数才能有效运行。这说明VN框架对单通道向量输入的初始处理存在结构约束。

3. **隐式重建中的不变解码器精度损失**：在I/I协议下，VN-OccNet相比标量OccNet存在轻微精度损失（表3），表明不变特征压缩可能丢弃了部分判别信息。这一精度代价是等变性保证的固有权衡。

4. **MAX池化的边际增益**：学习到的VN-MAX池化相比简单MEAN池化未展示显著优势（表7），暗示当前key对齐选择机制可能未充分捕获几何显著性。

5. **大规模场景泛化未验证**：所有实验均基于ModelNet40和ShapeNet等中等规模数据集，VN框架在真实大规模三维场景（如室内扫描、室外LiDAR）下的有效性尚待检验。

![[assets/figures/papers/paper_list_l23_https_arxiv_org_abs_2104_12229/figures/006_Table_1.jpg]]
*Table 1: more about the max pooling as well as ablation study on other structures in the supplementary material. Table 1: Test classification accuracy on the ModelNet40 dataset [37] in three train/test scenarios. z stands for aligned data augmented by random rotations around the vertical axis and SO(3) indicates data augmented by random rotations*

![[assets/figures/papers/paper_list_l23_https_arxiv_org_abs_2104_12229/figures/007_Table_2.jpg]]
*Table 2: ShapeNet part segmentation. The results are reported in overall average category mean IoU over 16 categories in two train/test scenarios. With z, we refer to data augmented only by random rotations around the vertical axis, and $\mathrm { S O ( 3 ) }$ indicates random rotations*

![[assets/figures/papers/paper_list_l23_https_arxiv_org_abs_2104_12229/figures/008_Table_3.jpg]]
*Table 3: Volumetric mIoU on ShapeNet reconstruction with neural implicits. We show results on extreme settings: no-rotation (I) – the standard evaluation setup for prior methods, and arbitrary rotations SO(3). Here the SO(3) random rotations are generated for each shape in a pre-processing stage and all shapes stay at fixed poses during training*

![[assets/figures/papers/paper_list_l23_https_arxiv_org_abs_2104_12229/figures/013_Table_4.jpg]]
*Table 4: Test classification accuracy (%) on the Model-Net40 dataset [37] with training on aligned data. I stands for no-rotations*

![[assets/figures/papers/paper_list_l23_https_arxiv_org_abs_2104_12229/figures/014_Table_7.jpg]]
*Table 7: Mean and max pooling – Comparisons between the VN-MAX aggregation defined in Section 3.3 and the standard mean aggregation (MEAN) which naturally preserves equivariance. The two aggregations give comparable results, while MEAN pooling performs slightly better than VN-MAX in more cases. Note that VN-MAX also introduces additional learnable weights compared to the mean aggregation. Table 8: Invariance – Table 8 shows our ablation study on the invariant layer (VN-In) in Section 3.5. Specifically, in computing the equivariant coordinate systems ${ \bf { { T } } } _ { n }$ following (13), we compare the combinations of the following options: whether or not concatenating the global mean V to the lo...*

![[assets/figures/papers/paper_list_l23_https_arxiv_org_abs_2104_12229/figures/015_Table_5.jpg]]
*Table 5: ShapeNet part segmentation results (mIoU). Training is done on aligned data without rotation augmentation. Table 6: Non-linearity – We compare the performances of entangled linear-ReLU (or linear-LeakyReLU) layers in (6) with 2-tuples of a linear layer plus a separate non-linearity in (24). “Built-in” stands for non-linearities with built-in linear transformations, while “detached” stands for tuples of detached linear and non-linear layers in (24). In most cases, with either the VN-PointNet or the VN-DGCNN backbone, disentangling linear and non-linear layers leads to slightly better results. But this is also at the cost of a doubled network depth and a longer training time (roughly > 1.5 ti...*

## 定位与知识库关联

### 与标量点云网络的关系

Vector Neuron（VN）框架并非从零构建全新架构，而是将经典点云网络中的**标量神经元提升为三维向量神经元**，在保持原始架构骨架的前提下注入 SO(3) 等变性。具体而言，VN-DGCNN 和 VN-PointNet 分别继承 DGCNN 和 PointNet 的宏观结构，但将每一层的特征通道从标量序列 $\mathbb{R}^C$ 替换为向量列表 $\mathbb{R}^{C \times 3}$，并将线性层、非线性层、池化和归一化全部替换为等变版本。这一设计使得参数规模大幅缩减——通道数取 $\lfloor N/3 \rfloor \times 3$ 时，参数量约为标量对应物的 **$\leq 2/9$**——同时天然获得对任意 SO(3) 旋转的等变性，而无需数据增强或网络修改。

在 ModelNet40 分类任务中，这种提升的效果极为显著：标准 DGCNN 在 aligned 训练 / SO(3) 测试设定下准确率仅 **16.6%**，而 VN-DGCNN 达到 **90.0%**（Table 4），提升 **+73.4 个百分点**，证明了标量网络在未见旋转下的灾难性失效以及 VN 框架的鲁棒性。

### 与其他等变网络的关系

在 SO(3) 等变点云网络的谱系中，VN 框架的定位介于**球谐函数方法**和**群卷积方法**之间，但以简洁性见长：

- **TFN / SE(3)-Transformers** 等基于球谐函数和 Clebsch-Gordan 张量积的方法需要处理复杂的角动量耦合规则，实现门槛高，且在高阶表示下计算开销大。VN 通过将特征直接组织为 $\mathbb{R}^{C \times 3}$ 矩阵，绕过了球谐展开，仅用标准线性代数和向量运算即实现等变性。

- **群卷积方法**（如将卷积核在 SO(3) 群上离散化并做群卷积）面临群离散化的分辨率与计算成本的权衡。VN 不显式离散化旋转群，而是通过**可学习方向** $\mathbf{k}$ 在非线性层中隐式编码旋转信息，使网络在连续 SO(3) 上操作。

- 在实证表现上，VN-DGCNN 在 ModelNet40 的 SO(3)/SO(3) 设定下达到 **90.2%** 准确率（Table 1），在 ShapeNet 部件分割的 z/SO(3) 和 SO(3)/SO(3) 设定下均达到 **81.4% mIoU**（Table 2），优于同期其他等变架构。

### 方法适用边界与局限

1. **仅保证 SO(3) 等变性，不覆盖 SE(3)**：VN 框架假设点云已中心化到原点，因此仅对旋转群 SO(3) 等变，对平移不具备等变性。论文明确指出，实现完整的 SE(3) 等变性需要额外的平移处理机制，这是一个开放问题。

2. **输入通道限制**：VN 的线性层要求输入为 $\mathbb{R}^{C \times 3}$ 的向量列表。当输入仅为 $\mathbb{R}^{1 \times 3}$ 的裸点坐标时（如 PointNet 的标准输入），单通道无法进行有意义的通道混合。VN-PointNet 的解决方案是在输入层添加一个边卷积将特征映射到 $\mathbb{R}^{C \times 3}$（$C>1$），这增加了架构复杂度。

3. **非线性层的方向依赖性**：VN 非线性通过可学习方向 $\mathbf{k}$ 将向量投影并截断，其等变性依赖于 $\mathbf{k}$ 随输入一同旋转。这种设计在单层内是严格的，但多层堆叠时方向 $\mathbf{k}$ 的学习动态及其对训练稳定性的影响尚未被充分分析。

4. **批归一化的近似处理**：标准批归一化直接作用于特征值会破坏等变性。VN 的解决方案是对向量列表的 **2-范数**（旋转不变量）做批归一化，再将归一化后的范数缩放回原向量。这是一种**近似方案**，在批次内样本姿态差异较大时可能引入误差。

5. **池化的信息瓶颈**：VN 的全局最大池化通过最大化与可学习键 $\mathbf{W}$ 的内积来选择特征向量，虽然等变，但这种“硬选择”可能丢弃对下游任务有用的空间信息，尤其在需要细粒度几何推理的任务中。

### 开放问题

- **SE(3) 等变性的扩展**：如何在不牺牲简洁性的前提下，将 VN 框架从 SO(3) 扩展到包含平移的 SE(3)，目前尚无明确方案。可能的路径包括引入相对位置编码或等变平移分支，但需要验证其与现有 VN 层的兼容性。

- **非线性层的设计空间**：论文在补充材料中提及了其他分段情况的非线性定义，但主文中仅展示了基于半空间截断的版本。更丰富的非线性设计空间（如基于角度的门控、多方向投影等）是否能在保持等变性的同时提升表达能力，仍需探索。

- **大规模场景与长序列**：VN 框架在 ModelNet40（约 12k 模型）和 ShapeNet 部件分割上的验证规模有限。当扩展到大规模真实场景（如室内语义分割、自动驾驶激光雷达）时，VN 的等变性假设（物体中心化、完整形状）是否仍然成立，以及计算效率是否可接受，均未经验证。

- **与 Transformer 架构的融合**：VN 提供的是等变特征表示层，如何将其与自注意力机制结合（例如构建 SO(3)-等变的注意力），以捕获长距离几何依赖，是一个有前景但尚未探索的方向。

- **隐式重建中解码器设计的更优选择**：VN-OccNet 的解码器通过拼接 $\langle \mathbf{x}, \mathbf{Z} \rangle$、$\|\mathbf{x}\|^2$ 和 $\text{VN-In}(\mathbf{Z})$ 三个不变量来实现旋转不变性（Table 3）。是否存在更优的不变量组合或可学习的等变解码器结构，以在 I/I 和 SO(3)/SO(3) 设定下同时达到最优，仍待研究。

## 原文 PDF

![[paperPDFs/ICCV_2021/Vector_Neurons_A_General_Framework_for_SO_3_Equivariant_Networks.pdf]]
