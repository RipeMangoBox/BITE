---
title: "AUV-Net: Learning Aligned UV Maps for Texture Transfer and Synthesis"
type: paper
paper_level: A
venue: CVPR
year: 2022
pdf_ref: paperPDFs/CVPR_2022/AUV_Net_Learning_Aligned_UV_Maps_for_Texture_Transfer_and_Synthesis.pdf
project_link: https://research.nvidia.com/labs/toronto-ai/AUV-NET/
aliases:
- AUV-Net
tags:
- CVPR_2022
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
core_operator: "通过线性子空间对齐模块（共享基 + 每个样本的系数），强制纹理图像在低维基空间中的组合性，从而无监督地将不同形状的对应语义部分映射到UV空间的同一位置。"
primary_logic: "网络被设计为将输入纹理分解为基图像的线性组合，并允许在分解前进行空间变形（UV映射）；为最小化重构误差，网络必须学会将所有样本的对应特征对齐到一致的UV位置，从而自发形成语义对齐的UV参数化。"
claims:
- "纹理对齐是通过一个简单而有效的无监督纹理对齐模块实现的，该模块受到传统线性子空间学习方法的启发。"
- "网络为所有形状纹理生成一个共享的基，并为每个形状预测特定的系数，纹理图像被构建为基图像的线性组合，从而强制对齐。"
- "在语义分割IOU指标上，AUV-Net在汽车和椅子类别上均超越BAE-Net和DIF-Net。"
- "在纹理合成任务的FID指标上，AUV-Net大幅优于Texture Fields（e.g., 汽车12.11 vs 53.09）。"
---

# AUV-Net: Learning Aligned UV Maps for Texture Transfer and Synthesis

> [!tip] 核心洞察
> 网络被设计为将输入纹理分解为基图像的线性组合，并允许在分解前进行空间变形（UV映射）；为最小化重构误差，网络必须学会将所有样本的对应特征对齐到一致的UV位置，从而自发形成语义对齐的UV参数化。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | AUV-Net：学习对齐UV映射用于纹理迁移和合成 |
| 英文题名 | AUV-Net: Learning Aligned UV Maps for Texture Transfer and Synthesis |
| 会议/期刊 | CVPR 2022 |
| Links | [paper](https://arxiv.org/abs/2204.03105); [Project](https://nv-tlabs.github.io/AUV-NET); [Project](https://research.nvidia.com/labs/toronto-ai/AUV-NET/) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction |
| Method | AUV-Net |
| Dataset | ShapeNet cars (semantic segmentation), ShapeNet chairs (semantic segmentation), Triplegangers heads (texture synthesis), ShapeNet cars (texture synthesis) |

> [!tip] 效果简介
> - ShapeNet cars (semantic segmentation) 上，IOU 为 72.7，对比 DIF-Net 69.0  /  BAE-Net 59.3，变化 +3.7 over DIF-Net, +13.4 over BAE-Net。
> - ShapeNet chairs (semantic segmentation) 上，IOU 为 85.8，对比 DIF-Net 80.3  /  BAE-Net 85.2，变化 +5.5 over DIF-Net, +0.6 over BAE-Net。
> - Triplegangers heads (texture synthesis) 上，FID 为 5.69，对比 Texture Fields 24.59，变化 -18.9 (lower is better)。

## 概述

在三维视觉中，为不同形状生成或迁移纹理长期受困于一个瓶颈：**缺乏跨实例的语义对齐的纹理表示**。传统方法要么依赖手工标注的稠密对应，要么使用球形映射或连续纹理场，难以将“车轮”“眼睛”等语义部件自动映射到一致的参数化位置。AUV-Net 的核心洞察在于，通过**线性子空间对齐模块**——强制纹理图像被表示为共享基图像的线性组合——网络在最小化重构误差的过程中，**自发地将不同形状的对应语义部分映射到 UV 空间的同一位置**，从而无需任何监督即可习得语义对齐的 UV 参数化。

具体而言，AUV-Net 引入了一个由编码器、UV 映射器、掩码网络和多个基生成器组成的框架。编码器从体素化点云中提取形状编码与基系数；UV 映射器为所有基生成器共享，输出一致的 UV 坐标；掩码网络自动将表面切割为多个区域以降低映射畸变；基生成器则分别为各区域生成基颜色，再与系数加权求和得到最终纹理。这一设计使得纹理迁移只需在 UV 空间中进行简单的图像操作，纹理合成则可直接应用成熟的 2D 生成模型。

实验验证了 AUV-Net 的有效性：在 ShapeNet 汽车与椅子类别的语义分割 IOU 上，AUV-Net 分别达到 72.7 和 85.8，超越 DIF-Net 与 BAE-Net；在纹理合成任务上，FID 指标大幅领先 Texture Fields（汽车 12.11 vs 53.09，人体头部 5.69 vs 24.59），证实了对齐 UV 表示对生成质量的显著提升。消融研究表明，颜色损失对汽车类别的对齐至关重要（移除后 IOU 下降 4.2），而掩码模块则是处理椅子等复杂拓扑的关键（移除后 IOU 骤降 14.7）。

### 方法定位

AUV-Net 处于**神经 UV 参数化**与**无监督语义对应学习**的交汇点。与依赖连续隐式场的 Texture Fields 不同，AUV-Net 回归到显式的 2D 纹理贴图表示，但通过可学习的 UV 映射赋予了其跨实例对齐的能力。在稠密对应方面，DIF-Net 基于变形场实现形状间的对应，而 AUV-Net 通过共享基与样本特定系数的分解机制，在 UV 空间中隐式地实现了语义对齐，避免了显式对应计算的复杂性。BAE-Net 则代表了单样本形状分割的另一路径，AUV-Net 在语义分割指标上与之可比甚至更优，同时额外具备纹理生成与迁移能力。

该方法的技术渊源可追溯至经典的线性子空间学习（如 Eigenfaces），但将其与可微 UV 映射相结合，使得对齐过程完全由重构目标驱动，无需任何对应标注。这一思路为 3D 纹理的生成式建模开辟了新的范式：先在语义对齐的 UV 空间中生成纹理图像，再通过预训练的 UV 映射将其“贴回”任意形状。

## 背景与动机

在三维视觉与图形学中，为三维形状赋予高质量纹理是内容创作、虚拟现实和数字孪生等应用的核心需求。然而，现有三维纹理表征方法在跨形状的纹理迁移与合成任务中面临一个根本性瓶颈：**不同物体之间纹理的语义对齐问题**。

传统方法通常将纹理定义为三维表面上的颜色场。例如，早期工作采用球形纹理映射或基于模板的UV参数化，但这些方法高度依赖于手工设计的对应关系或受限的拓扑结构，难以泛化到任意形状。近年来，基于隐式神经表示的连续纹理场方法（如 **Texture Fields**）虽然摆脱了显式参数化的约束，但纹理信息被编码在MLP的权重中，缺乏结构化的语义空间。这意味着，当需要将一辆车的纹理迁移到另一辆形态不同的车上时，无法保证车轮、车窗等语义部件被映射到对应的位置——纹理迁移变成了“盲贴”，合成结果严重依赖形状间的几何相似性，而非语义对应。

这一瓶颈的根源在于：**现有方法将纹理视为形状的附属属性，而非可跨实例对齐的独立实体**。连续纹理场在单个形状上可以完美重构颜色，但在多形状集合中，每个形状的纹理表征是孤立的，没有机制强制不同形状的对应语义部分共享一致的参数化坐标。因此，纹理迁移和合成任务长期受限于手工对应标注或受限的拓扑假设。

AUV-Net的动机正是打破这一僵局。其核心洞察是：**如果网络被设计为将输入纹理分解为基图像的线性组合，并允许在分解前进行空间变形（UV映射），那么为最小化重构误差，网络必须学会将所有样本的对应特征对齐到一致的UV位置**。这一“重构即对齐”的机制无需任何显式的对应标注，即可在无监督条件下自发形成语义对齐的UV参数化。由此，纹理不再是形状的附属品，而成为可编辑、可迁移、可生成的独立二维图像，为纹理迁移与合成开辟了新的可能性。

## 核心创新

AUV-Net 的核心创新在于提出了一种**无监督的纹理对齐模块**，从根本上改变了3D纹理的表征方式，使得不同拓扑和形状的物体能够自动学习到语义一致的UV参数化。其关键突破可归纳为以下三个层面：

### 1. 线性子空间对齐：从隐式场到可组合基图像

传统方法（如 **Texture Fields**）使用连续隐式场（MLP预测颜色）表示纹理，缺乏跨实例的显式对应机制，导致纹理迁移和合成高度依赖手工对应或受限拓扑。AUV-Net 转而采用**对齐的2D UV纹理贴图**作为表征，并通过线性子空间学习实现语义对齐。

其核心机制是：网络生成一个**所有形状共享的基（basis images）**，并为每个输入形状预测特定的**系数（coefficients）**，将纹理图像构建为基图像的线性组合。这一设计强制不同形状的对应语义部分映射到UV空间的同一位置——因为只有对齐的基才能以最少的重构误差解释所有输入纹理。换言之，网络为最小化重构误差，必须自发地发现并保持跨实例的语义对应。

### 2. 蒙版网络：从单一片面到自适应表面切割

传统球面参数化或单张纹理贴图难以覆盖复杂拓扑（如椅子的扶手、腿、靠背）。AUV-Net 引入了一个**蒙版网络（Masker）**，自动将3D表面切割为多个区域（如“前”/“后”），并为每个区域分配独立的基生成器（Basis Generator）。

对于汽车等相对简单的形状，使用两个基生成器分别处理前后部分；对于椅子等复杂拓扑，则通过法线掩码与预测掩码的外积合成四通道分割掩码，对应四个纹理贴图：

$$
\begin{bmatrix} m_{i}^{a} & m_{i}^{c} \\ m_{i}^{b} & m_{i}^{d} \end{bmatrix} = \begin{bmatrix} m_{i}^{n} \\ 1 - m_{i}^{n} \end{bmatrix} \cdot \begin{bmatrix} m_{i}^{pred} & 1 - m_{i}^{pred} \end{bmatrix}
$$

这一策略有效降低了UV映射的畸变，使网络能够处理拓扑差异显著的形状集合。

### 3. 共享UV映射器：统一的参数化空间

与蒙版网络配合，AUV-Net 使用一个**所有基生成器共享的UV映射器（UV Mapper）**。该MLP以形状编码和查询点坐标为输入，输出UV坐标。共享机制确保了即使不同区域由不同基生成器处理，它们仍被映射到同一个对齐的UV空间，从而支持跨区域的纹理迁移和合成。

### 与Baseline的关键差异

| 维度 | 基线方法（Texture Fields等） | AUV-Net |
|------|---------------------------|---------|
| 纹理表示 | 连续纹理场（MLP预测颜色） | 对齐的2D UV纹理贴图（高分辨率图像） |
| 形状覆盖 | 单张纹理或球面参数化 | 蒙版网络自动切割表面，多基生成器分区域处理 |
| 对齐机制 | 无显式对齐，依赖隐式场泛化 | 共享基 + 样本特定系数的线性子空间对齐 |
| 纹理迁移 | 需要训练时的对应或后处理 | 直接交换对齐的纹理图像即可完成迁移 |

这种“基-系数分解 + 蒙版切割 + 共享UV映射”的组合设计，使得AUV-Net在无需任何对应标注的情况下，实现了跨形状的语义对齐UV参数化，为纹理迁移、合成和单视图重建提供了统一的框架。

## 整体框架

AUV-Net 的整体管线围绕一个核心目标构建：**为任意拓扑的 3D 形状集合学习语义对齐的 UV 参数化**，使得不同形状的对应语义部件被映射到 UV 空间的同一位置。这一目标通过将纹理重建过程建模为“基图像的线性组合 + 空间变形”来实现——网络被迫将输入纹理分解为一组共享基图像与每个样本专属系数的乘积，而变形（UV 映射）在分解之前发生。为最小化重建误差，网络必须自发地将所有样本的对应特征对齐到一致的 UV 坐标，从而在无监督条件下形成语义对齐。

### 输入输出流

- **输入**：体素化点云（voxelized point cloud），包含 3D 坐标与颜色信息。
- **输出**：
  - 对齐的高分辨率纹理图像（分辨率 1024²），每个形状可有多张纹理图像（汽车 2 张，椅子 4 张）。
  - 语义对齐的 UV 映射，可用于纹理迁移、合成与单视图重建。

### 核心模块

网络由五个关键模块串联构成，其架构如 **Figure 4** 所示：

![[assets/figures/papers/paper_list_l52_https_arxiv_org_abs_2204_03105/figures/004_Figure_4.jpg]]
*Figure 4: Network architecture of our AUV-Net. The encoder predicts the shape code and the coefficients from the voxelized input point cloud. The UV mapper and the masker take as input the shape code and the query points from the input point cloud, and output the UV coordinates and the segmentation mask, respectively. The UV coordinates are fed into the two basis generators to obtain the basis colors for each query point, and the basis colors are multiplied by the predicted coefficients to generate the actual colors for each query point. Those colors from the two basis generators are selected by the predicted segmentation mask to produce the final colors*

1. **Encoder（编码器）**：3D CNN，接收体素化点云，输出形状编码（shape code）与基系数（coefficients）。形状编码用于驱动下游的 UV 映射与掩码预测，基系数则用于加权组合基颜色。

2. **UV Mapper（UV 映射器）**：MLP，输入形状编码与查询点坐标，输出该点在 UV 空间中的坐标。**该映射器为所有基生成器共享**，确保不同部件区域使用一致的参数化。

3. **Masker（掩码网络）**：MLP，输入点坐标、法线与形状编码，输出分割掩码，将形状切割为多个区域（如“前”与“后”）。这是处理复杂拓扑的关键——通过自动切割表面，减少单张 UV 贴图中的扭曲，使网络能应对椅子等具有显著自遮挡的拓扑结构。

4. **Basis Generators（基生成器）**：多个 MLP，分别对应不同切割区域（如“前”基生成器和“后”基生成器）。每个基生成器接收 UV 坐标，输出该区域的基颜色值。基颜色与编码器预测的系数加权求和，得到该区域的纹理颜色。

5. **Loss Functions（损失函数）**：总体损失为五项损失的加权和：

   $$L = w_{c} L_{c} + w_{n} L_{n} + w_{x} L_{x} + w_{s} L_{s} + w_{p} L_{p}$$

   其中：
   - $L_c$（颜色损失）：监督重建颜色与输入颜色的一致性。
   - $L_n$（法线损失）：利用法线信息辅助对应关系学习。
   - $L_x$（循环一致性损失）：增强映射的稳定性。
   - $L_s$（平滑损失）：惩罚 UV 空间中邻域距离与原始 3D 空间邻域距离的不一致，避免 UV 坐标塌缩。
   - $L_p$（先验损失）：仅在训练初期使用，用于初始化 UV 映射和前后部分割（如将 3D 点投向 xy 平面并根据法线方向初始化）。

### 数据流与端到端流程

整个流程是端到端可微的：

1. 输入点云经编码器提取形状编码与基系数。
2. UV 映射器为每个查询点生成 UV 坐标。
3. 掩码网络为每个点预测分割掩码，决定该点属于哪个区域。
4. 各区域的基生成器根据 UV 坐标输出基颜色，与系数加权求和得到该点的候选颜色。
5. 分割掩码选择对应区域的颜色作为最终输出。
6. 输出颜色与输入颜色计算损失，梯度反向传播更新所有模块。

### 训练策略

训练采用三阶段策略，通过动态调整损失权重来平衡对齐精度与映射平滑性：

- **第一阶段**（10 epochs）：权重 $\{w_c, w_n, w_x, w_s, w_p\} = \{1, 0.5, 100, 100, 1\}$，利用先验损失初始化掩码与 UV 坐标。
- **第二阶段**（2000 epochs）：权重 $\{1, 0.5, 1, 1, 0\}$，移除先验损失，让网络自主学习对齐。
- **第三阶段**（2000 epochs）：权重 $\{1, 0.5, 1, 0.1, 0\}$，降低平滑损失权重，允许更大的 UV 变形以提升对齐质量。

完整训练在单张 NVIDIA RTX 3080 Ti GPU 上约需 2 天。

### 从 2D 到 3D 的验证路径

作者首先在 2D 人脸数据集上验证了核心对齐模块的概念（**Figure 2, Figure 3**）：使用 1000 张来自 CelebA-HQ 的随机透视变换人脸图像，学习 128 个灰度基图像。2D 实验成功展示了网络将不同姿态人脸对齐到统一 UV 空间的能力，为 3D 扩展奠定了基础。3D 版本的核心差异在于引入掩码网络处理复杂拓扑，以及使用多个基生成器分别覆盖不同表面区域。

### 应用管线复用

对于单视图纹理重建任务（**Figure 13**），AUV-Net 的 UV 映射器和掩码网络在预训练后被冻结，作为固定的参数化模块使用——IM-Net 解码器预测形状，预训练的 AUV-Net 模块为该预测形状生成 UV 映射，从而实现纹理重建。这种“预训练参数化 + 下游任务复用”的设计体现了框架的模块化优势。

## 核心模块与公式推导

AUV-Net 的核心由三个功能模块构成：**对齐模块**、**掩码网络**与**多基生成器**。其设计目标是通过无监督学习，将不同三维形状的对应语义部分映射到 UV 空间的同一位置，从而形成语义对齐的二维纹理参数化。

### 对齐模块

对齐模块是 AUV-Net 的核心创新，其灵感来源于经典的线性子空间学习。该模块由三个子网络组成（Fig. 4）：

- **编码器**：一个 3D CNN，接收体素化的输入点云，输出形状编码 $z$ 以及一组基系数 $\alpha$。
- **UV 映射器**：一个 MLP，以形状编码 $z$ 和查询点坐标 $p$ 为输入，输出该点在 UV 空间中的坐标 $q$。该映射器为所有基生成器共享。
- **基生成器**：一个 MLP，以 UV 坐标 $q$ 为输入，输出 $N$ 个基颜色值。

纹理重建的核心机制是：基生成器在 UV 空间定义一组所有形状共享的基图像，编码器为每个输入形状预测一组系数，最终纹理被构建为基图像的线性组合。为了最小化重建误差，网络被迫将不同形状的对应特征对齐到 UV 空间中的一致位置，从而自发形成语义对齐的参数化。这一机制在 2D 人脸图像对齐实验中得到了验证（Fig. 2, Fig. 3）。

### 掩码网络与多基生成器

为处理复杂拓扑并减少 UV 映射的畸变，AUV-Net 引入了掩码网络，将形状切割为多个部分，每个部分由独立的基生成器处理。

- **掩码器**：一个 MLP，输入点坐标、法线和形状编码，输出分割掩码。对于人体头部等类别，使用先验损失 $L_p$（Eq. 3）初始化前后部分割；对于椅子等复杂拓扑，通过预测法线与真实法线的点积构造法线掩码，再与预测掩码外积得到四通道分割掩码（Eq. 9），分别对应四个纹理贴图。
- **多基生成器**：每个部分（如“前”/“后”）拥有独立的基生成器，各自生成基颜色。最终颜色由预测的分割掩码从各部分输出中选择。

### 关键公式

**总体损失函数**（Eq. 1）：

$$L = w_{c} L_{c} + w_{n} L_{n} + w_{x} L_{x} + w_{s} L_{s} + w_{p} L_{p}$$

其中各项含义如下：

- **$L_c$（颜色损失）**：重建颜色与输入颜色的差异，是驱动语义对齐的主要信号。消融实验表明，移除 $L_c$ 对汽车类别影响显著（IoU 从 72.7 降至 68.5），说明颜色线索对汽车对齐至关重要。
- **$L_n$（法线损失）**：重建法线与输入法线的差异，提供几何一致性约束。
- **$L_x$（循环一致性损失）**：确保 UV 映射的可逆性，防止不同点映射到同一 UV 坐标。
- **$L_s$（平滑损失，Eq. 2）**：惩罚 UV 空间中邻域距离与原始 3D 空间邻域距离的不一致，防止 UV 映射在局部区域塌缩。移除该损失虽未显著降低 IoU，但会导致纹理斑块化。

$$L_{s} = \frac{1}{MN} \sum_{i=1}^{M} \sum_{j=1}^{N} \left| D(p_{i}, p_{j}) - D(q_{i}, q_{j}) \right| \cdot \mathcal{T}(p_{i}, p_{j})$$

其中 $D$ 为欧氏距离，$\mathcal{T}$ 为邻域指示函数。

- **$L_p$（先验损失，Eq. 3）**：仅在训练初期使用，用于初始化 UV 映射和掩码。对于人体头部，将 3D 点投向 xy 平面，并根据法线方向初始化前后部分割。

$$L_{p} = \frac{1}{N} \sum_{i=1}^{N} (p_{i}^{x} - q_{i}^{x})^{2} + (p_{i}^{y} - q_{i}^{y})^{2} + (m_{i} - n_{i})^{2}$$

训练采用三阶段策略：第一阶段（10 epochs）使用较高权重 $\{w_c, w_n, w_x, w_s, w_p\} = \{1, 0.5, 100, 100, 1\}$，以先验损失初始化掩码和 UV 坐标；第二阶段（2000 epochs）降低循环一致性和平滑损失权重至 $\{1, 0.5, 1, 1, 0\}$；第三阶段（2000 epochs）进一步降低至 $\{1, 0.5, 0.1, 0.1, 0\}$，以平衡纹理对齐与畸变。

### 方法瓶颈与局限

尽管线性子空间对齐机制在大多数类别上表现有效，但存在以下局限：

- 在纹理杂乱的情况下（如动物纹理），对应关系可能错误，导致眼睛等语义部分未能对齐（Fig. 11）。
- 处理复杂拓扑仍需较多基生成器（椅子需要四个），且最终 UV 贴图间仍可能存在可见接缝。
- 方法依赖于训练集中存在部件级对应和姿态对齐，泛化到任意姿态的新类别仍需额外优化。

## 实验与分析

### 数据集与评估协议

AUV-Net 在多个类别上进行了评估，覆盖纹理迁移（Tsf）、生成（Gen）和单视图重建（SVR）三项任务，具体数据集配置见 Table 1。所有对比方法均使用相同的数据集划分和评估协议，包括统一的 FID 计算方式与相同的渲染视角数量。纹理生成比较中，AUV-Net 与 **Texture Fields** 均使用各自的生成模型，但评估标准一致，确保了可比性。

![[assets/figures/papers/paper_list_l52_https_arxiv_org_abs_2204_03105/figures/005_Table_1.jpg]]
*Table 1: Datasets used in our experiments. Tsf, Gen, and SVR refer to the applications listed in Sec. 3.3*

### 语义对齐能力：分割 IOU 定量比较

为量化无监督学习到的 UV 映射的语义对齐质量，作者在 ShapeNet 汽车和椅子类别上进行语义分割评估，将 UV 空间中的像素标签投影回 3D 表面后计算 IOU。Table 2 显示，AUV-Net 在汽车类别上达到 72.7 IOU，较 **BAE-Net**（59.3）提升 13.4 点，较 **DIF-Net**（69.0）提升 3.7 点；在椅子类别上达到 85.8 IOU，较 DIF-Net（80.3）提升 5.5 点，与 BAE-Net（85.2）基本持平。这表明网络成功将不同形状的对应语义部分映射到 UV 空间的同一位置，无需任何监督标注。

![[assets/figures/papers/paper_list_l52_https_arxiv_org_abs_2204_03105/figures/012_Figure_7.jpg]]
*Figure 7: Sample texture images and segmentation on ShapeNet cars and chairs. (a) shows texture images before inpainting. Note that there are 2 texture images for each car and 4 for each chair. In (b), we show the segmentation we used to produce Table 2. A visualization on 3D shapes is shown in (c). Table 2. Semantic segmentation results in IOU, comparing with BAE-Net [13] and DIF-Net [16]*

### 纹理合成质量：FID 定量比较

纹理合成任务中，AUV-Net 在 UV 空间训练 StyleGAN2 生成对齐纹理图像，再通过预训练网络映射回 3D 表面。Table 4 报告了 FID 指标：在 Triplegangers 头部数据集上，AUV-Net 的 FID 为 5.69，远低于 Texture Fields 的 24.59（降低 18.9）；在 ShapeNet 汽车上为 12.11 vs 53.09（降低 40.98）；在 ShapeNet 椅子上为 5.33 vs 7.03（降低 1.70）。大幅领先的 FID 验证了对齐 UV 空间为生成模型提供了更规整、更易建模的数据分布。

![[assets/figures/papers/paper_list_l52_https_arxiv_org_abs_2204_03105/figures/011_Table_4.jpg]]
*Table 4: Quantitative results of generative models in FID*

### 单视图纹理重建

Table 5 展示了单视图纹理重建的 FID 结果：汽车类别上 AUV-Net 达到 40.85，Texture Fields 为 92.89（降低 52.04）；椅子类别上 AUV-Net 为 33.26，Texture Fields 为 36.89（降低 3.63）。Figure 10 展示了重建结果的可视化细节（如车轮纹理），进一步支持定量结论。

![[assets/figures/papers/paper_list_l52_https_arxiv_org_abs_2204_03105/figures/002_Figure.jpg]]
*Figure: (e)Alignedtexturesbydeforming(a)*

![[assets/figures/papers/paper_list_l52_https_arxiv_org_abs_2204_03105/figures/010_Figure.jpg]]
*Figure: （a）Texture image （b)Segmentation （c）Visualization*

![[assets/figures/papers/paper_list_l52_https_arxiv_org_abs_2204_03105/figures/016_Figure.jpg]]

![[assets/figures/papers/paper_list_l52_https_arxiv_org_abs_2204_03105/figures/015_Figure_10.jpg]]
*Figure 10: Textured single view reconstruction results. Zoom in to see the details, e.g., wheels of the cars. Table 5. Results of textured single view reconstruction*

### 消融实验

Table 3 报告了各损失项和模块的消融结果，Figure 8 提供了对应的可视化。

![[assets/figures/papers/paper_list_l52_https_arxiv_org_abs_2204_03105/figures/009_Table_3.jpg]]
*Table 3: Ablation study: semantic segmentation results in IOU*

- **颜色损失 $L_c$ 的关键作用**：移除 $L_c$ 后，汽车 IOU 从 72.7 降至 68.5，而椅子 IOU 几乎不变（85.2 vs 85.8）。这说明颜色线索对汽车类别的语义对齐至关重要——汽车纹理中车窗、车灯等区域的颜色分布为对应关系提供了强信号；而椅子纹理相对稀疏，几何信息（法线）已足够驱动对齐。
- **蒙版模块的拓扑分割能力**：移除蒙版网络后，椅子 IOU 从 85.8 骤降至 71.1，严重破坏了对复杂拓扑（如椅腿、扶手、靠背）的分割能力。汽车因仅需前/后两个基生成器，移除蒙版影响较小（72.0 vs 72.7）。
- **平滑损失 $L_s$ 的规整化作用**：去掉 $L_s$ 后，椅子 IOU 反而略升至 87.1，但 Figure 8 显示部分区域在 UV 空间中塌缩，导致纹理斑块化。这表明 $L_s$ 虽未显著提升语义对齐精度，但对于维持 UV 映射的几何连续性、保证后续生成质量不可或缺。
- **其他损失项**：移除法线损失 $L_n$ 使椅子 IOU 降至 84.6；移除循环一致性损失 $L_x$ 使椅子 IOU 降至 83.7；移除先验损失 $L_p$ 使汽车 IOU 降至 70.6。各损失项协同作用，共同支撑对齐质量。

### 失败模式与局限性

Figure 11 展示了典型失败案例：将卡通长颈鹿纹理迁移到其他动物时，眼睛位置出现错误对应。这表明在纹理杂乱、语义边界模糊的情况下（如动物皮毛纹理），网络可能建立错误的对应关系。此外，切割产生的接缝在纹理迁移后仍可能可见（如河马模型），即使经过 inpainting 处理。

更一般的局限性包括：方法依赖于训练集中存在部件级对应和姿态对齐，泛化到任意姿态的新类别仍需额外优化；处理复杂拓扑需要较多基生成器（椅子需四个），且基生成器数量需手动指定。

### 补充图表

![[assets/figures/papers/paper_list_l52_https_arxiv_org_abs_2204_03105/figures/008_Figure_6.jpg]]
*Figure 6: Comparison with DIF-Net [16] on texture transfer. The texture is transferred from (a) to (b). In (c), the eyes’ shapes are not changed with respect to (a), the lips are misaligned, and the hat is lower than it should be compared to (b). Those details are mostly represented in colors rather than geometry*

![[assets/figures/papers/paper_list_l52_https_arxiv_org_abs_2204_03105/figures/013_Figure_9.jpg]]
*Figure 9: Texture synthesis results. The holes on chairs are hallucinated via texture transparency (alpha channels in the texture images)*

![[assets/figures/papers/paper_list_l52_https_arxiv_org_abs_2204_03105/figures/003_Figure_2.jpg]]
*Figure 2: Results of the 2D toy experiment on the face dataset. Our network reconstructs input images (a) by learning a set of basis images (d) and linearly combining them into aligned texture images (c), and then deforming the texture images (c) into the outputs (b) via learned UV mapping. The learned UV mapping can be used to deform the input images (a) into aligned high-quality texture images (e). Figure 3. Network architecture of the 2D toy experiment on the face dataset, to demonstrate the concept of our alignment module*

## 方法谱系与知识库定位

### 1. 问题定位与核心瓶颈

在3D视觉与图形学中，为三维形状赋予纹理的主流范式长期沿着两条路径演进：**显式参数化**（如UV映射、球面映射）与**隐式场**（如NeRF、Occupancy Networks）。前者依赖手工设计的图切割或共形映射，难以在不同拓扑的物体间建立语义一致的对应；后者虽能表达连续纹理，却将纹理信息“溶解”在MLP权重中，无法提供可编辑、可迁移的显式纹理图像。

AUV-Net瞄准的核心瓶颈正是这一“对齐缺口”：**现有3D纹理表征方法难以实现不同物体之间纹理的语义对齐，导致纹理迁移和合成高度依赖于手工对应或受限拓扑**。例如，将一辆轿车的纹理迁移到一辆面包车上，传统方法要么需要人工标注关键点，要么因参数化方式不同而产生错位（如车轮纹理出现在车门上）。这一瓶颈直接制约了下游应用——纹理迁移、纹理合成、单视图纹理重建——的自动化程度和视觉质量。

### 2. 与基线方法的关系

#### 2.1 相对于隐式纹理场：从“溶解”到“显式对齐”

**Texture Fields** 是隐式纹理表征的代表性工作，它用一个MLP将3D坐标映射为颜色值，从而绕开了UV参数化的难题。然而，这种“溶解式”表征带来了两个根本性局限：

| 对比维度 | Texture Fields | AUV-Net |
|---------|---------------|---------|
| 纹理表示方式 | 连续纹理场（MLP预测颜色） | 对齐的2D UV纹理贴图（高分辨率图像） |
| 形状覆盖策略 | 单张纹理或球面参数化 | 通过蒙版网络自动切割表面，使用多个基生成器分别处理“前/后”或更多部分 |
| 纹理可编辑性 | 低（需修改网络权重） | 高（直接编辑2D纹理图像） |
| 跨实例纹理迁移 | 需重新训练或优化 | 直接交换纹理图像即可 |

在定量对比中，AUV-Net的显式对齐纹理贴图带来的优势十分显著：在ShapeNet汽车类别的纹理合成FID指标上，AUV-Net达到12.11，而Texture Fields高达53.09（降幅达40.98）；在Triplegangers人头数据集上，AUV-Net的FID为5.69，Texture Fields为24.59（降幅18.9）。在单视图纹理重建（SVR）任务上，汽车类别的FID差距更为悬殊：AUV-Net 40.85 vs Texture Fields 92.89。这些结果表明，**显式的、对齐的UV纹理贴图在下游生成任务中具有显著的表示优势**。

#### 2.2 相对于稠密对应方法：从“几何对应”到“纹理对齐”

**DIF-Net** 是一种基于隐式场的稠密对应方法，它将3D形状映射到模板形状上建立对应关系。AUV-Net在语义分割IOU指标上全面超越DIF-Net：汽车类别72.7 vs 69.0（+3.7），椅子类别85.8 vs 80.3（+5.5）。更关键的是定性差异：如Figure 6所示，DIF-Net在纹理迁移时保留了源形状的几何细节（如眼睛形状不变、嘴唇错位），而AUV-Net通过纹理层面的对齐，能更好地将语义信息（如眼睛纹理）映射到目标形状的正确位置。

**BAE-Net** 是单样本形状分割的基线方法。AUV-Net在汽车类别上大幅领先（72.7 vs 59.3，+13.4 IOU），在椅子类别上略优（85.8 vs 85.2，+0.6）。BAE-Net依赖几何信息进行分割，而AUV-Net通过纹理对齐模块额外利用了颜色线索，这在颜色信息丰富的类别（如汽车）中带来了显著增益。

### 3. 核心方法机制：线性子空间对齐

AUV-Net的核心洞察在于**将纹理对齐问题转化为线性子空间分解问题**。网络被设计为将输入纹理分解为基图像的线性组合，并允许在分解前进行空间变形（UV映射）；为最小化重构误差，网络必须学会将所有样本的对应特征对齐到一致的UV位置，从而自发形成语义对齐的UV参数化。

具体而言，这一机制通过三个关键设计实现：

1. **共享基 + 样本特定系数**：网络为所有形状纹理生成一个共享的基，并为每个形状预测特定的系数，纹理图像被构建为基图像的线性组合。这种“组合性”约束强制网络将语义相同的部分（如所有汽车的车轮）映射到UV空间的同一区域，否则无法用共享基重构出不同的纹理。

2. **UV映射器与空间变形**：在基图像组合之前，UV Mapper（一个MLP）将3D表面点映射到2D UV坐标，允许网络学习非刚性的空间变形。这种“先对齐、再组合”的流程使得网络能够处理不同形状间的几何差异。

3. **蒙版网络与多基生成器**：为处理复杂拓扑（如椅子的扶手、椅腿、椅背），AUV-Net引入Masker网络将形状切割为多个区域，每个区域由独立的Basis Generator处理。椅子类别需要四个基生成器（对应四个纹理贴图），消融实验显示，移除蒙版模块会导致椅子IoU从85.8骤降至71.1，验证了这一设计对复杂拓扑的必要性。

这一方法的灵感来源于传统线性子空间学习（如PCA、NMF），但将其嵌入端到端的深度学习框架中，实现了无监督的语义对齐。2D玩具实验（Figure 2）在CelebA-HQ人脸数据集上验证了这一概念：网络用128个灰度基图像重构了1000张经过随机透视变换的人脸图像，并自发学习到了眼睛、鼻子、嘴巴等语义特征的对齐。

### 4. 适用边界与局限

#### 4.1 已知局限

1. **纹理杂乱场景下的对齐失败**：当纹理过于复杂或缺乏清晰的语义边界时（如卡通动物纹理），对齐可能出现错误。Figure 11展示了一个典型案例：将卡通长颈鹿的纹理迁移到其他动物时，眼睛的位置出现明显偏差。

2. **接缝伪影**：尽管蒙版网络切割了表面以降低扭曲，切割边界处仍可能出现可见接缝。在河马模型上，即使经过修复（inpainting），切割缝依然清晰可见（Figure 11）。

3. **拓扑复杂度与基生成器数量**：椅子类别需要四个基生成器才能获得良好的对齐效果，对于更复杂的拓扑（如带有多个部件的机械模型），可能需要更多基生成器，增加了训练复杂度和计算开销。

4. **训练数据依赖性**：方法依赖于训练集中存在部件级对应和姿态对齐。泛化到任意姿态的新类别（如姿态差异极大的动物）可能需要额外的优化或先验约束。

#### 4.2 适用场景

AUV-Net在以下条件下表现最佳：
- 训练数据具有相似的部件结构（如四轮汽车、四腿椅子）
- 纹理包含清晰的颜色线索（如汽车的车身颜色、车轮的深色）
- 形状间存在语义对应但几何差异较大（如轿车与SUV）
- 需要高分辨率、可编辑的纹理输出

### 5. 开放问题

1. **弱监督对齐增强**：如何引入少量弱监督（如标注眼睛位置、车轮中心）来进一步提升纹理对齐的鲁棒性，特别是在纹理杂乱或纹理稀疏的场景下？

2. **自适应拓扑处理**：能否设计一种动态基生成器数量或自适应的掩码分割策略，使网络能够根据输入形状的拓扑复杂度自动决定需要多少纹理贴图，而非预先固定？

3. **无缝纹理迁移**：如何完全消除纹理迁移时由于切割产生的接缝伪影？可能的思路包括在基生成器之间引入一致性约束，或在UV空间边界处进行纹理融合。

4. **跨类别泛化**：当前方法在同类形状间工作良好，但能否扩展到跨类别的纹理迁移（如将木质纹理从椅子迁移到桌子）？这可能需要更高级的语义理解或材质分解能力。

5. **与生成模型的深度整合**：AUV-Net生成的纹理图像可作为StyleGAN等2D生成模型的训练数据，但当前的两阶段流程（先训练AUV-Net，再训练生成模型）能否统一为端到端的框架，实现纹理对齐与生成的联合优化？

## 原文 PDF

![[paperPDFs/CVPR_2022/AUV_Net_Learning_Aligned_UV_Maps_for_Texture_Transfer_and_Synthesis.pdf]]
