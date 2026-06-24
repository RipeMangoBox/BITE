---
title: "GaussianFusion: Unified 3D Gaussian Representation for Multi-Modal Fusion Perception"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/GaussianFusion_Unified_3D_Gaussian_Representation_for_Multi_Modal_Fusion_Percept_c79ab99eee1d.pdf
project_link: null
code_link: null
aliases:
- GaussianFusion
tags:
- ICLR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
- topic/representation_self_supervised_transfer
core_operator: 切换为连续的3D高斯表示，通过高斯混合模型自然聚合多模态高斯，并在高维空间进行融合，避免早期量化损失。
primary_logic: 利用3D高斯函数的连续性和协方差矩阵的自适应不确定性建模能力，在统一高斯空间中实现多模态特征的自然对齐与互补增强，从而突破离散BEV的性能瓶颈。
claims:
- GaussianFusion在nuScenes 3D目标检测中，相比BEVFusion在相同BEV尺寸下NDS提升2.6（74.0 vs 71.4 at 200×200）。
- GaussianFusion-C在3D语义占用预测中，仅用GaussFormer 30%的高斯数量，实现1.55 mIoU提升和450%的加速。
- 前向投影高斯初始化相比随机初始化，NDS提升+2.8。
- 共享高斯编码器相比独立编码器，mAP提升+0.7。
---

# GaussianFusion: Unified 3D Gaussian Representation for Multi-Modal Fusion Perception

> [!tip] 核心洞察
> 利用3D高斯函数的连续性和协方差矩阵的自适应不确定性建模能力，在统一高斯空间中实现多模态特征的自然对齐与互补增强，从而突破离散BEV的性能瓶颈。

| 字段 | 内容 |
|------|------|
| 中文题名 | GaussianFusion：面向多模态融合感知的统一3D高斯表示 |
| 英文题名 | GaussianFusion: Unified 3D Gaussian Representation for Multi-Modal Fusion Perception |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=7jXxQ9bGoU) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction #topic/representation_self_supervised_transfer |
| Method | GaussianFusion |
| Dataset | nuScenes 3D Object Detection, nuScenes 3D Semantic Occupancy Prediction, nuScenes val |

> [!tip] 效果简介
> - nuScenes 3D Object Detection (val) 上，NDS 74.0 vs 71.4 (BEVFusion) (+2.6)。
> - nuScenes 3D Object Detection (test) 上，NDS 74.9 (GaussianFusion)。
> - nuScenes 3D Semantic Occupancy Prediction (val) 上，mIoU 20.65 (GaussianFusion-C) vs 19.10 (GaussFormer) (+1.55)。

## 概述

### 核心问题：离散BEV表示的空间信息瓶颈

多模态3D感知的主流范式是将相机和激光雷达特征统一投影到鸟瞰图（BEV）空间进行融合。然而，BEV的离散网格表示存在根本性缺陷：网格化操作不可避免地丢失边缘和精细纹理等空间细节，导致多模态特征对齐精度下降，跨模态信息交互受限。这一瓶颈直接制约了融合感知的性能上限。

### 方法定位：从离散网格到连续高斯表示

**GaussianFusion** 是首个将统一3D高斯表示引入多模态融合感知的框架。其核心洞见在于：利用3D高斯函数的连续性和协方差矩阵的自适应不确定性建模能力，在统一高斯空间中实现多模态特征的自然对齐与互补增强，从而突破离散BEV的性能瓶颈。

与现有方法的本质区别体现在以下维度：

| 设计维度 | 现有范式 | GaussianFusion |
|---------|---------|----------------|
| 场景表示 | 离散BEV网格 | 连续3D高斯分布 |
| 相机初始化 | 随机初始化 | 基于LSS深度分布的前向投影初始化 |
| 跨模态编码器 | 各自独立的编码器 | 共享高斯编码器（batch维度合并处理） |
| 注意力采样 | 方形网格均匀采样点 | 利用协方差矩阵生成符合物体几何先验的采样偏移 |
| 参数更新 | 直接预测全新高斯参数（如GaussFormer） | 预测均值、尺度、旋转的偏移量进行增量更新 |
| 多传感器融合 | BEV空间的特征拼接或加权求和 | 通过高斯混合模型自然聚合多模态高斯分布 |

在方法谱系中，GaussianFusion定位为**任务无关的多模态融合框架**，可同时服务于3D目标检测和语义占用预测等下游任务。相比 **BEVFusion**（Liu et al., ICRA 2023）的离散BEV融合、**UniTR**（Wang et al., ICCV 2023）的统一Transformer融合、**MetaBEV**（Ge et al., ICCV 2023）的跨模态注意力融合，GaussianFusion首次将连续高斯表示引入融合层，避免了早期量化的信息损失。

### 核心结论

在nuScenes 3D目标检测中，GaussianFusion在相同BEV尺寸（200×200）下NDS达到74.0，相比BEVFusion的71.4提升**+2.6**（Table 1）。在3D语义占用预测任务上，GaussianFusion-C仅使用GaussFormer 30%的高斯数量，实现**1.55 mIoU**的提升和**450%**的推理加速（Abstract, Table 7）。同时，模型在延迟和内存占用上分别降低15.4%和16.9%（Table 3），展现出精度与效率的双重优势。

消融实验进一步验证了关键设计的有效性：前向投影高斯初始化相比随机初始化带来+2.8 NDS提升（Table 8），共享高斯编码器相比独立编码器提升+0.7 mAP（Table 9），带有高斯先验的可变形注意力相比普通可变形注意力提升+0.4 NDS（Table 9），增量参数更新相比预测全新参数提升+0.9 mAP（Table 9）。这些结果一致表明，连续高斯表示及其配套设计是突破离散BEV瓶颈的有效路径。

## 背景与动机

### 离散BEV表示：多模态融合的性能瓶颈

多模态3D感知——尤其是相机与激光雷达的融合——已成为自动驾驶系统的核心感知范式。其主流技术路线是将异构传感器数据统一投影到鸟瞰图（BEV）空间进行特征融合。代表性的工作如 **BEVFusion**（Liu et al., ICRA 2023）、**UniTR**（Wang et al., ICCV 2023）和 **MetaBEV**（Ge et al., ICCV 2023），均基于离散BEV网格构建融合架构，在nuScenes等基准上取得了显著成果。

然而，**离散BEV网格表示存在根本性的空间信息丢失问题**。如图Figure 1所示，当多模态特征被投影到固定分辨率的离散网格时，连续的3D空间信息被强制量化为栅格单元，导致边缘、轮廓和精细纹理等结构细节在网格化过程中被平滑或丢弃。这种量化损失直接制约了两个关键环节：

- **跨模态特征对齐**：相机与激光雷达在几何特性、分辨率和噪声模式上存在本质差异，离散网格难以提供足够精细的空间载体来弥合这些差异。
- **跨模态信息交互**：在BEV空间进行特征拼接或加权求和时，由于缺乏对局部几何结构的不确定性建模，互补信息的融合效率受限。

定量证据显示，BEV分辨率是性能的敏感瓶颈：在nuScenes验证集上，**BEVFusion**在200×200 BEV尺寸下的NDS仅为71.4，当分辨率提升至400×400时NDS达到72.7（Table 1），但内存消耗也随之急剧增长。这表明单纯提升网格分辨率并非可持续的解决方案——离散表示本质上需要在高分辨率与计算效率之间做出妥协。

### 3D高斯：连续空间建模的新范式

近年来，3D高斯飞溅（3D Gaussian Splatting）在新视角合成领域展现了强大的连续场景表示能力。其核心优势在于：

- **连续函数形式**：3D高斯以参数化的概率密度函数描述空间点，天然支持任意分辨率的连续查询，避免了离散化损失。
- **自适应不确定性建模**：每个高斯的协方差矩阵$\Sigma = \mathbf{R} \mathbf{S} \mathbf{S}^T \mathbf{R}^T$编码了该基元在空间中的尺度、方向和形状，恰好对应了感知特征在不同区域的不确定性——例如，物体边缘处需要更精细的建模，而平坦路面则可使用更宽松的分布。

**GaussFormer**（H et al., arXiv 2024）首次将3D高斯引入视觉语义占用预测，验证了该表示在3D感知任务中的潜力。但其设计存在两个局限：仅处理纯视觉输入，且高斯参数采用一次性预测而非迭代优化，无法充分利用多模态互补信息。

### 本文动机：从离散BEV到连续高斯融合

上述分析揭示了一个清晰的技术缺口：**当前多模态融合方法受限于离散BEV表示的空间量化损失，而3D高斯表示虽具备连续建模能力，却尚未被系统性地引入多传感器融合框架。**

本文的核心动机在于回答一个关键问题：**能否用连续的3D高斯表示替代离散BEV网格，作为多模态融合的统一载体？**

这一转换面临三个核心挑战：

1. **初始化问题**：相机缺乏直接深度信息，如何为相机分支生成有意义的3D高斯初始位置？
2. **跨模态对齐**：相机高斯和激光雷达高斯源自不同传感器，如何在统一空间中实现特征的对齐与增强？
3. **融合机制**：如何从数学上自然地聚合两个高斯集合，而非简单地在BEV空间拼接特征？

GaussianFusion的提出正是为了系统性地解决上述挑战，其核心洞察在于：**利用3D高斯函数的连续性和协方差矩阵的自适应不确定性建模能力，在统一高斯空间中实现多模态特征的自然对齐与互补增强，从而突破离散BEV的性能瓶颈。**

## 核心创新

GaussianFusion的核心创新在于**将多模态融合的表示空间从离散BEV网格切换为连续的3D高斯分布**，并围绕这一连续表示设计了一套完整的初始化、编码与融合机制。这一范式转换直接回应了BEV表示的根本瓶颈：离散网格在投影和池化过程中不可避免地丢失空间细节，导致跨模态特征对齐困难。

### 从离散BEV到连续高斯的范式转换

传统BEV融合范式（如**BEVFusion**（Liu et al., ICRA 2023））将多模态特征投影到固定分辨率的离散网格上，网格分辨率成为精度与效率的硬约束——分辨率越高，内存和计算开销呈平方级增长，而低分辨率则导致空间信息严重退化。GaussianFusion以连续3D高斯函数替代离散网格，每个高斯由均值 $\pmb{\mu}$、尺度 $\mathbf{s}$、旋转 $\mathbf{r}$ 和查询特征 $q$ 参数化，通过协方差矩阵 $\pmb{\Sigma} = \mathbf{R} \mathbf{S} \mathbf{S}^T \mathbf{R}^T$ 自适应地建模空间不确定性。这一表示天然具有**分辨率无关性**：高斯可以在任意空间位置连续采样，无需受限于固定网格步长。

### 关键创新点

#### 1. 前向投影高斯初始化

相机高斯初始化是连续表示能否有效运作的首要环节。与随机初始化或简单的BEV网格映射不同，GaussianFusion采用基于LSS深度分布的前向投影策略：将环视图像特征 $F_{c,i}$ 输入LSS网络获得深度分布 $D_i$，以深度概率作为高斯均值 $\pmb{\mu}$ 的初始化依据。这一设计将2D图像特征与3D空间位置建立了有意义的初始对应，消融实验表明，相比随机初始化，该策略带来**NDS +2.8**的显著提升（Table 8）。

#### 2. 共享高斯编码器

传统多模态融合往往为各模态设计独立的编码器，导致跨模态信息交互仅在融合阶段发生。GaussianFusion提出**共享高斯编码器**，将相机高斯 $\mathcal{G}_c$ 和LiDAR高斯 $\mathcal{G}_L$ 在batch维度合并，通过同一组参数进行迭代优化。这一设计使得高斯属性的更新过程天然具备跨模态感知能力，消融实验显示，共享编码器相比独立编码器带来**mAP +0.7**的提升（Table 9）。

#### 3. 带有高斯先验的可变形注意力

编码器中的核心操作是可变形注意力。与标准可变形注意力（Zhu et al., 2020）在方形网格上均匀采样不同，GaussianFusion利用高斯协方差矩阵生成符合物体几何先验的采样偏移 $\Delta \pmb{\mu}$：

$$\mathrm{DeformAtt}(q_i, B_i) = \sum_{k=1}^{K} A_k \cdot W_k B_i(\pmb{\mu} + \Delta \pmb{\mu})$$

这一设计使注意力采样点沿物体的长轴和短轴方向自适应分布（Figure 3），更精准地捕获语义特征。消融实验表明，该设计相比普通可变形注意力带来**NDS +0.4**的提升（Table 9）。

#### 4. 增量式高斯参数更新

与**GaussFormer**（H et al., arXiv 2024）直接预测全新高斯参数不同，GaussianFusion采用增量更新策略：

$$\hat{\mathcal{G}}_i = \mathbf{MLP}(\hat{Q}) + \mathcal{G}_i = (\Delta \pmb{\mu} + \pmb{\mu}, \Delta \mathbf{s} + \mathbf{s}, \Delta \mathbf{r} + \mathbf{r})$$

通过预测均值、尺度、旋转的偏移量进行渐进式优化，使模型能够逐步缩小模态间差异。消融实验表明，预测偏移相比预测全新参数带来**mAP +0.9**的提升（Table 9）。此外，将高斯属性编码为查询位置嵌入（$\hat{Q}_i = \mathbf{MLP}(\mathcal{G}) + Q_i$）进一步带来**mAP +0.5**的增益（Table 9）。

#### 5. 高斯混合模型自然融合

多模态高斯通过高斯混合模型（GMM）自然聚合为统一表示，点 $\mathbf{p}$ 处的融合特征由所有重叠高斯的贡献求和得到：

$$f(\mathbf{p}) = \sum_{i=1}^{J} \hat{g}_i (\mathbf{p}; \pmb{\mu}, \mathbf{s}, \mathbf{r}) \hat{q}_i$$

这与BEV空间中的简单拼接或加权求和有本质区别：GMM融合保留了每个高斯的完整空间分布信息，而非仅保留单一网格内的池化特征。融合后的高斯通过MeanVFE模块体素化，以适配下游任务头。

### 创新点的因果链条

上述创新点构成了一条清晰的因果链：**前向投影初始化**为相机高斯提供了有意义的3D初始位置 → **共享编码器**在迭代优化过程中实现跨模态特征对齐 → **高斯先验注意力**使特征采样更精准 → **增量更新**确保优化稳定性 → **GMM融合**在保留空间信息的前提下完成模态聚合。这一链条的终端效果是，GaussianFusion在nuScenes 3D目标检测上以200×200的BEV尺寸实现74.0 NDS，相比BEVFusion同尺寸下的71.4 NDS提升**+2.6**（Table 1），同时推理延迟降低15.4%，内存占用降低16.9%（Table 3）。

## 整体框架

GaussianFusion 提出了一套从离散 BEV 到连续 3D 高斯表示的统一多模态融合流水线。其核心设计思想是：将相机和 LiDAR 两种模态的特征分别初始化为独立的 3D 高斯分布，通过共享高斯编码器进行迭代优化与跨模态对齐，随后利用高斯混合模型自然聚合为统一的场景表示，最后经体素化后送入任务专用头完成下游感知。

**整体数据流** 如图 2 所示，框架包含以下关键模块及其输入输出关系：

1. **特征提取**：环视相机图像经主干网络提取特征 $F_{c,i}$；LiDAR 点云经体素化后由 LiDAR BEV 编码器提取 BEV 特征 $B_L$。此阶段两种模态尚处于各自独立的表示空间。

2. **高斯初始化**：相机模态利用 LSS 预测的深度分布作为高斯均值 $\pmb{\mu}$，将 2D 图像特征“前向投影”为 3D 高斯集 $\mathcal{G}_c$，避免了随机初始化带来的空间歧义（该策略带来 NDS +2.8 的提升，见 Table 8）。LiDAR 模态则以 BEV 网格中心为均值初始化高斯集 $\mathcal{G}_L$。每个高斯由均值 $\pmb{\mu}$、尺度 $\mathbf{s}$、旋转 $\mathbf{r}$ 和查询特征 $q$ 参数化，其空间响应由协方差矩阵 $\pmb{\Sigma}$ 决定。

3. **共享高斯编码器**：这是框架的核心创新模块，将 $\mathcal{G}_c$ 和 $\mathcal{G}_L$ 在 batch 维度合并后同时处理。编码器堆叠多个层，每层包含两个子模块：
   - **带高斯先验的可变形注意力**：利用高斯协方差矩阵生成符合物体几何先验的采样偏移 $\Delta\pmb{\mu}$，对 BEV 特征图进行自适应采样，更新高斯查询特征。
   - **高斯更新模块**：通过预测均值、尺度、旋转的偏移量（$\Delta\pmb{\mu}, \Delta\mathbf{s}, \Delta\mathbf{r}$）对高斯参数进行增量更新，而非直接预测全新参数（该设计带来 mAP +0.9 的提升，见 Table 9）。

   共享编码器使两种模态的高斯在统一空间中相互增强、逐步缩小模态间差异，实现隐式跨模态对齐。消融实验表明，共享编码器相比独立编码器提升 mAP +0.7（Table 9）。

4. **高斯混合模型融合**：优化后的相机高斯 $\hat{\mathcal{G}}_c$ 和 LiDAR 高斯 $\hat{\mathcal{G}}_L$ 通过高斯混合模型自然合并为统一的 3D 高斯集。空间任意点 $\mathbf{p}$ 的融合特征由所有重叠高斯的贡献加权求和得到：
   $$f(\mathbf{p}) = \sum_{i=1}^{J} \hat{g}_i (\mathbf{p}; \pmb{\mu}, \mathbf{s}, \mathbf{r}) \hat{q}_i$$
   这种连续表示避免了 BEV 离散化带来的空间信息丢失，是突破性能瓶颈的关键。

5. **高斯到体素转换（MeanVFE）**：采用体素均值池化将连续高斯聚合为规则体素特征 $B_F$，对体素内的 $M$ 个高斯的参数和查询特征分别取平均：
   $$\hat{g} = \frac{1}{M} [\sum \mu_m, \sum \mathbf{s}_m, \sum \mathbf{r}_m], \quad \hat{q} = \frac{1}{M} \sum \hat{q}_m$$

6. **任务专用头**：基于融合后的 BEV 特征 $B_F$ 执行 3D 目标检测或 3D 语义占用预测。

**与基线范式的关键差异**：传统 BEVFusion（Liu et al., ICRA 2023）将多模态特征投影到离散 BEV 网格后进行拼接或求和，早期量化导致边缘和纹理细节丢失。GaussianFusion 将场景表示为连续 3D 高斯分布，利用协方差矩阵的自适应不确定性建模能力，在高维高斯空间中完成特征对齐与融合，仅在最后阶段才进行体素化以兼容下游任务头。这一“先连续融合、后离散化”的策略在 nuScenes 3D 检测中相比 BEVFusion 同 BEV 尺寸下 NDS 提升 2.6（74.0 vs 71.4, Table 1），同时推理延迟降低 15.4%、显存降低 16.9%（Table 3）。

### 补充图表

![[assets/figures/papers/paper_list_l39_https_openreview_net_forum_id_7jXxQ9bGoU/figures/003_Figure_2.jpg]]
*Figure 2: Overview of the GaussianFusion framework. Initial Gaussians are refined by a shared encoder and fused in Gaussian space, followed by task-specific heads for 3D perception*

![[assets/figures/papers/paper_list_l39_https_openreview_net_forum_id_7jXxQ9bGoU/figures/002_Figure_1.jpg]]
*Figure 1: Comparison of the discrete BEV representation fusion paradigm (Liu et al., 2023b) and our proposed continuous Gaussian representation fusion paradigm. B, G, C, L, and F denote BEV, Gaussian, Camera, Lidar, and Fusion*

## 核心模块与公式推导

GaussianFusion 的核心设计围绕“将离散 BEV 网格替换为连续 3D 高斯表示”这一因果开关展开，整个框架由四个关键模块串联：高斯初始化、共享高斯编码器、高斯混合融合以及高斯到体素的转换。

### 3D 高斯表示

对于任意模态，一个 3D 高斯由其均值 $\pmb{\mu}$、尺度 $\mathbf{s}$、旋转四元数 $\mathbf{r}$ 和查询特征 $q$ 定义。协方差矩阵 $\pmb{\Sigma}$ 由尺度和旋转构建：

$$\pmb{\Sigma} = \mathbf{R} \mathbf{S} \mathbf{S}^T \mathbf{R}^T, \quad \mathbf{S} = \mathrm{diag}(\mathbf{s}), \quad \mathbf{R} = \mathrm{q2r}(\mathbf{r})$$

相机高斯在空间点 $\mathbf{p}$ 处的特征响应为：

$$g_c(\mathbf{p}; \pmb{\mu}, \mathbf{s}, \mathbf{r}) = \exp\big(-\frac{1}{2}(\mathbf{p} - \pmb{\mu})^T \pmb{\Sigma}^{-1} (\mathbf{p} - \pmb{\mu})\big) q_c$$

LiDAR 高斯的特征响应形式对称：

$$g_L(\mathbf{p}; \pmb{\mu}, \mathbf{s}, \mathbf{r}) = \exp\big(-\frac{1}{2}(\mathbf{p} - \pmb{\mu})^T \pmb{\Sigma}^{-1} (\mathbf{p} - \pmb{\mu})\big) q_L$$

协方差矩阵 $\pmb{\Sigma}$ 的自适应椭圆形状赋予每个高斯对自身不确定性的建模能力——这是离散 BEV 网格无法实现的连续几何先验。

### 高斯初始化策略

**相机高斯初始化**采用基于 LSS 深度分布的前向投影，而非随机初始化。环视相机图像经特征提取器得到特征 $F_{c,i}$ 后，通过 LSS 预测深度分布 $D_i$，将其作为高斯均值 $\pmb{\mu}$ 的初始值。消融实验表明，该策略相比随机初始化带来 **NDS +2.8** 的提升（Table 8）。

**LiDAR 高斯初始化**则直接以 LiDAR BEV 网格中心作为均值 $\pmb{\mu}$，天然利用了点云的几何先验。两种模态的高斯共享相同的参数结构（$\pmb{\mu}, \mathbf{s}, \mathbf{r}, q$），为后续共享编码器的统一处理奠定基础。

### 共享高斯编码器

这是方法的核心创新模块，包含两个子模块，堆叠多层以迭代优化高斯属性。

**带有高斯先验的可变形注意力（Deformable Attention with Gaussian）** 将高斯属性编码为查询位置嵌入：

$$\hat{Q}_i = \mathbf{MLP}(\mathcal{G}) + Q_i, \quad i = \mathrm{c}, \mathrm{L}$$

随后利用高斯协方差矩阵生成符合物体几何先验的采样偏移 $\Delta \pmb{\mu}$，对 BEV 特征图进行采样：

$$\mathrm{DeformAtt}(q_i, B_i) = \sum_{k=1}^{K} A_k \cdot W_k B_i(\pmb{\mu} + \Delta \pmb{\mu})$$

与普通可变形注意力（Zhu et al., 2020）在方形网格上均匀采样不同，此处的采样偏移由 $\pmb{\Sigma}$ 引导，使采样点沿物体的主要几何方向分布（Figure 3）。消融实验显示，该设计带来 **NDS +0.4** 的提升（Table 9）。

![[assets/figures/papers/paper_list_l39_https_openreview_net_forum_id_7jXxQ9bGoU/figures/004_Figure_3.jpg]]
*Figure 3: Comparison of the vanilla deformable attention (Zhu et al., 2020) and our proposed deformable attention with Gaussian*

**高斯更新模块（Gaussian Updating）** 采用增量更新而非直接预测全新参数：

$$\hat{\mathcal{G}}_i = \mathbf{MLP}(\hat{Q}) + \mathcal{G}_i = (\Delta \pmb{\mu} + \pmb{\mu}, \Delta \mathbf{s} + \mathbf{s}, \Delta \mathbf{r} + \mathbf{r})$$

即预测均值、尺度、旋转的偏移量，叠加到当前参数上。这种渐进式更新使模型能够逐层缩小模态间的差异，消融表明相比预测全新参数，**mAP 提升 +0.9**（Table 9）。

关键地，编码器是**共享的**——将 $\mathcal{G}_c$ 和 $\mathcal{G}_L$ 在 batch 维度合并后送入同一编码器。共享权重使两种模态的高斯在统一空间中进行跨模态特征学习，消融显示相比独立编码器，**mAP 提升 +0.7**（Table 9）。

### 高斯混合融合与体素化

经过共享编码器迭代优化后的相机高斯 $\hat{\mathcal{G}}_c$ 和 LiDAR 高斯 $\hat{\mathcal{G}}_L$ 通过高斯混合模型自然聚合为统一集合 $\{\hat{\mathcal{G}}\}$。在任意空间点 $\mathbf{p}$ 处，融合特征由所有重叠高斯的贡献求和：

$$f(\mathbf{p}) = \sum_{i=1}^{J} \hat{g}_i (\mathbf{p}; \pmb{\mu}, \mathbf{s}, \mathbf{r}) \hat{q}_i$$

随后通过体素均值池化（MeanVFE）将连续高斯表示转换为规则体素特征，供下游任务头使用：

$$\hat{g} = \frac{1}{M} [\sum \mu_m, \sum \mathbf{s}_m, \sum \mathbf{r}_m], \quad \hat{q} = \frac{1}{M} \sum \hat{q}_m$$

这一设计使高斯混合模型天然处理了多模态分布的对齐与互补，避免了 BEV 融合中因离散化造成的空间信息丢失。

## 实验与分析

### 核心性能验证：3D目标检测

GaussianFusion在nuScenes 3D目标检测任务上展现了显著的性能优势。在验证集上，当BEV尺寸为200×200时，GaussianFusion以**74.0 NDS**超越了BEVFusion的71.4 NDS，提升达**+2.6**（Table 1）。值得注意的是，这一优势并非简单通过增加分辨率获得——GaussianFusion在200×200分辨率下的NDS（74.0）甚至超过了BEVFusion在400×400分辨率下的72.7，同时保持了更低的显存占用（4271 MB vs 5140 MB，Table 3）。在nuScenes测试集上，GaussianFusion达到了**74.9 NDS**和**72.4 mAP**，在BEV融合范式中处于领先水平（Table 2）。

![[assets/figures/papers/paper_list_l39_https_openreview_net_forum_id_7jXxQ9bGoU/figures/005_Table_2.jpg]]
*Table 2: Comparisons with state-of-the-art 3D object detection methods on nuScenes dataset. C denote Camera, L denote Lidar. All methods construct BEV-based feature maps instead of objectcentric fusion based on proposals, which means these methods can also be naturally used for semantic tasks. UniTR uses a unified backbone for both the camera and Lidar*

![[assets/figures/papers/paper_list_l39_https_openreview_net_forum_id_7jXxQ9bGoU/figures/006_Table_3.jpg]]
*Table 3: Latency and performance on nuScenes val. set*

**效率瓶颈的突破**：GaussianFusion在推理效率上同样表现出色。在相同验证条件下，其推理延迟为132 ms，相比BEVFusion的156 ms降低了**15.4%**；显存占用从5140 MB降至4271 MB，降幅达**16.9%**（Table 3）。这一效率提升的核心在于连续的3D高斯表示避免了高分辨率BEV网格带来的计算负担，使得模型可以在较低分辨率设置下获得更优的性能。

### 跨任务泛化：3D语义占用预测

为验证方法的任务无关性，论文将GaussianFusion-C（仅相机版本）应用于3D语义占用预测任务，并与基于高斯的GaussFormer进行对比。结果显示，GaussianFusion-C仅使用GaussFormer **30%的高斯数量**，即实现了**+1.55 mIoU**的提升（20.65 vs 19.10），同时推理速度提升了**450%**（Table 7）。这一结果表明，高斯混合模型的自然聚合能力不仅适用于多模态融合，在纯视觉场景下也能通过更高效的高斯表示实现精度与速度的双重提升。

![[assets/figures/papers/paper_list_l39_https_openreview_net_forum_id_7jXxQ9bGoU/figures/010_Table_7.jpg]]
*Table 7: Comprehensive comparison with Gaussian-Former on nuScenes val set*

### 消融实验：关键设计的作用机制

#### 高斯初始化策略

前向投影高斯初始化是GaussianFusion性能的重要支撑。Table 8的消融实验表明，相比随机初始化，基于LSS深度分布的前向投影初始化带来了**+2.8 NDS**的显著提升。这一增益源于初始化阶段即注入了来自深度估计的几何先验，使得后续的高斯编码器能够从更合理的空间位置开始迭代优化，避免了随机初始化在早期迭代中的无效探索。

#### 共享高斯编码器架构

Table 9系统消融了高斯编码器的各组件贡献：

- **共享编码器 vs 独立编码器**：将相机和LiDAR高斯通过batch维度合并后送入共享编码器，相比各自独立的编码器，mAP提升**+0.7**。这表明共享参数空间促进了跨模态特征的隐式对齐与交互。
- **带有高斯先验的可变形注意力**：相比普通可变形注意力，利用高斯协方差矩阵生成符合物体几何先验的采样偏移（Deformable Attention with Gaussian），NDS提升**+0.4**。这一设计的核心优势在于采样点不再局限于方形网格，而是能够自适应地沿物体主方向分布，更有效地捕获细长或倾斜物体的特征。
- **增量更新 vs 全新预测**：预测高斯参数的偏移量（Δμ, Δs, Δr）而非直接预测全新的高斯参数，mAP提升**+0.9**。增量更新使得各编码器层能够渐进式地缩小模态间差异，避免了每层重新建模带来的不稳定性。
- **高斯属性编码为位置嵌入**：将高斯属性（均值、尺度、旋转）通过MLP编码后与查询特征相加，mAP提升**+0.5**。这为注意力机制提供了显式的空间结构信息，增强了查询对自身几何属性的感知能力。

### 时序扩展与跨数据集验证

GaussianFusion-T将历史帧的高斯表示通过运动补偿变换到当前时间戳，并利用高斯混合模型进行时序融合。Table 4显示，时序扩展进一步提升了模型对运动物体的检测稳定性，在nuScenes验证集上取得了额外的性能增益。

在Waymo Open Dataset上的验证（Table 6）表明，GaussianFusion的连续高斯融合范式具有良好的跨数据集泛化能力，其性能优势不依赖于特定的传感器配置或场景分布。

![[assets/figures/papers/paper_list_l39_https_openreview_net_forum_id_7jXxQ9bGoU/figures/009_Table_6.jpg]]
*Table 6: Waymo Open Dataset Result*

### 定性分析

Figure 4展示了GaussianFusion在3D目标检测和语义占用预测任务上的定性结果。在目标检测场景中，融合后的高斯表示能够更准确地捕获物体的边界和朝向，尤其是对于细长物体（如卡车、公交车）和部分遮挡目标。在语义占用预测中，连续高斯表示有效保留了场景的精细几何结构，相比离散BEV方法在物体边缘和细小结构（如行人、护栏）的预测上更为锐利和完整。

### 失败模式与局限性

论文未明确报告具体的失败案例或定量局限性分析。从方法设计角度推断，潜在的失效场景可能包括：1）深度估计误差较大的区域（如远距离、镜面反射表面），前向投影初始化可能引入偏差，尽管后续的迭代更新具有一定纠偏能力；2）极端稀疏的LiDAR观测区域，高斯参数的估计可能因缺乏足够约束而退化。这些推断需在后续实验中进行手动验证。

### 补充图表

![[assets/figures/papers/paper_list_l39_https_openreview_net_forum_id_7jXxQ9bGoU/figures/012_Table_8.jpg]]
*Table 8: Ablation of Gaussian initialization strategy*

![[assets/figures/papers/paper_list_l39_https_openreview_net_forum_id_7jXxQ9bGoU/figures/011_Table_9.jpg]]
*Table 9: Ablation of the proposed Gaussian Encoder. DA.G means Deformable Attention with Gaussian*

![[assets/figures/papers/paper_list_l39_https_openreview_net_forum_id_7jXxQ9bGoU/figures/013_Figure_4.jpg]]
*Figure 4: Qualitative results on object detection and 3D semantic occupancy prediction*

![[assets/figures/papers/paper_list_l39_https_openreview_net_forum_id_7jXxQ9bGoU/figures/008_Table_5.jpg]]
*Table 5: Semantic scene completion results on nuScenes (Wei et al., 2023; Caesar et al., 2020) val set. † represents trained on nuScenes. For Camera-only and C+L, the top performance is indicated in bold black and bold blue, respectively*

![[assets/figures/papers/paper_list_l39_https_openreview_net_forum_id_7jXxQ9bGoU/figures/007_Table_4.jpg]]
*Table 4: Comparison with temporal methods*

## 方法谱系与知识库定位

### 1. 问题定位：离散BEV融合范式的瓶颈

GaussianFusion的核心动机源于对当前主流多模态融合范式——以**BEVFusion** (Liu et al., ICRA 2023) 为代表的离散BEV网格表示——的性能瓶颈分析。在BEVFusion等框架中，相机和激光雷达特征被分别投影到统一的离散BEV网格上，通过特征拼接或加权求和进行融合。这一范式虽然在工程上简洁高效，但其根本性局限在于：**离散化过程导致显著的空间信息丢失，无法有效保留边缘和精细纹理细节**，进而限制了多模态特征的对齐精度和跨模态信息交互的深度。

GaussianFusion将这一瓶颈归因为“表示空间的离散性”，并提出了一个因果性的解决方案：**将场景表示从离散BEV网格切换为连续的3D高斯分布**。这一转变使得多模态特征能够在连续空间中进行自然对齐，避免了早期量化带来的不可逆信息损失。

### 2. 方法谱系中的位置

GaussianFusion处于多模态3D感知方法谱系中“统一表示融合”这一分支的最新节点。其前后关系可梳理如下：

**前序工作（直接基线）：**
- **BEVFusion** (Liu et al., ICRA 2023)：建立了多任务多传感器BEV融合的基准范式，GaussianFusion在相同BEV尺寸下（200×200）将NDS从71.4提升至74.0，直接验证了连续高斯表示相对于离散BEV的优势。
- **UniTR** (Wang et al., ICCV 2023)：提出统一的多模态Transformer架构，但仍基于BEV表示。GaussianFusion在nuScenes test集上以74.9 NDS超越UniTR，且推理延迟更低（132ms vs. 156ms）。
- **MetaBEV** (Ge et al., ICCV 2023)：学习跨模态注意力进行BEV融合，同样受限于离散网格表示。
- **GaussFormer** (H et al., arXiv 2024)：首次将3D高斯引入视觉语义占用预测，但其高斯参数通过直接预测获得，缺乏多模态融合机制。GaussianFusion-C在语义占用预测任务上以仅30%的高斯数量实现1.55 mIoU的提升和450%的加速，表明增量更新策略和跨模态高斯混合融合的显著优势。

**方法创新定位：**
GaussianFusion并非对BEVFusion的简单替换，而是从表示层面对融合范式进行了重构。其核心创新点在于：
1. **表示空间的连续性**：用3D高斯函数的连续响应替代离散网格的二值归属，使得特征在空间中的分布具有平滑的过渡和明确的不确定性建模（通过协方差矩阵 $\boldsymbol{\Sigma}$）。
2. **融合机制的自然性**：多模态高斯通过高斯混合模型（Gaussian Mixture Model）自然聚合，而非简单的特征拼接。在任意空间点 $\mathbf{p}$ 处，融合特征由所有重叠高斯的贡献求和得到：$f(\mathbf{p}) = \sum_{i=1}^{J} \hat{g}_i (\mathbf{p}; \boldsymbol{\mu}, \mathbf{s}, \mathbf{r}) \hat{q}_i$。
3. **跨模态联合优化**：共享高斯编码器在batch维度合并处理相机和LiDAR高斯，通过带有高斯先验的可变形注意力实现跨模态特征增强，再通过增量更新（预测均值、尺度、旋转的偏移量）逐步缩小模态间差异。

### 3. 适用边界与局限

尽管GaussianFusion在多个基准上展现了显著优势，其适用边界和潜在局限值得关注：

**适用场景：**
- 多模态（相机+激光雷达）3D感知任务，包括3D目标检测和语义占用预测。
- 对推理效率和内存消耗有严格要求的部署场景（相比BEVFusion延迟降低15.4%，内存降低16.9%）。
- 可扩展至时序融合（GaussianFusion-T），通过将历史高斯表示warp到当前时间戳实现时序信息聚合。

**已知局限与开放问题：**
- 论文明确提出的开放问题：“如何探索运动感知的高斯更新以实现更连贯的4D场景建模？”这表明当前方法在处理动态场景的时序一致性方面仍有提升空间。
- 高斯混合融合的性能依赖于初始化的质量。消融实验显示，前向投影初始化相比随机初始化带来+2.8 NDS的提升，说明该方法对初始高斯位置较为敏感。在激光雷达缺失或稀疏的场景下，仅依赖LSS深度估计的相机高斯初始化可能面临精度退化，需要进一步验证。
- 高斯数量的选择涉及精度-效率权衡。论文未系统探讨高斯数量对极端场景（如远距离小目标、严重遮挡）的影响，这一边界条件需要在实际部署中手动验证。

### 4. 知识库定位与后续工作接口

GaussianFusion为多模态融合提供了一个“连续表示”的新范式，其知识贡献可归纳为三个可复用的模块化组件：

1. **前向投影高斯初始化**：将LSS深度分布作为高斯均值的初始化策略，可被任何基于高斯的感知方法采用。
2. **带有高斯先验的可变形注意力**：利用协方差矩阵生成符合物体几何先验的采样偏移，相比普通可变形注意力带来+0.4 NDS的提升，可作为注意力机制设计的通用增强模块。
3. **增量高斯更新**：预测参数偏移而非全新参数的更新策略，带来+0.9 mAP的提升，适用于任何迭代优化的高斯场景表示框架。

这些组件为后续工作提供了明确的改进接口：例如，可将运动信息编码为高斯参数的时序演化规律，实现4D高斯场景流建模；或将高斯先验注意力推广到其他跨模态对齐任务（如文本-3D、图像-点云配准）。

## 原文 PDF

![[paperPDFs/ICLR_2026/GaussianFusion_Unified_3D_Gaussian_Representation_for_Multi_Modal_Fusion_Percept_c79ab99eee1d.pdf]]