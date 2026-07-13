---
title: "Unified Spherical Frontend: Learning Rotation-Equivariant Representations of Spherical Images from Any Camera"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/Unified_Spherical_Frontend_Learning_Rotation_Equivariant_Representations_of_Spherical_Images_from_Any_Camera.pdf
project_link: null
code_link: "https://github.com/rusty1s/pytorch_scatter"
aliases:
- USFU
- USFLRERSIFAC
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
- topic/representation_self_supervised_transfer
core_operator: 将所有操作（重采样、卷积、池化）提升到单位球面上进行，通过仅使用距离加权的旋转等变卷积核，从架构层面而非数据增强层面实现SO(3)旋转等变。
primary_logic: 通过将任意相机模型拍摄的图像通过射线方向映射投影至球面，再通过解耦的位置采样和数值插值重采样为均匀分布，最后在空间域直接进行基于测地距离的球形卷积和池化，即可实现镜头无关且天然旋转等变的视觉处理，无需昂贵的球谐变换。
claims:
- USF在随机旋转测试时性能下降不到1%，且无需在训练时进行旋转增强（在Stanford 2D-3D-S语义分割上球形DeepLab v3非旋转mIoU 28.78%，旋转mIoU 28.09%，仅下降0.69%；而平面DeepLab v3则从35.01%骤降至12.11%）
- 仅距离加权的核函数通过构造保证了旋转等变性，在MNIST分类中球形距离PWC内核在随机旋转下准确率达85.43%，而平面CNN仅41.08%
- 球形YOLOv11在目标检测（PANDORA数据集）上无需旋转增强即可保持旋转稳定性（非旋转mAP10 29.54%，旋转mAP10 29.59%），而平面YOLOv11性能崩溃（39.65% -> 12.71%）
- 零镜头镜头泛化实验表明，球形模型在未见过的镜头类型（如从全景切换至针孔或鱼眼）上性能下降明显小于平面模型
---

# Unified Spherical Frontend: Learning Rotation-Equivariant Representations of Spherical Images from Any Camera

> [!tip] 核心洞察
> 通过将任意相机模型拍摄的图像通过射线方向映射投影至球面，再通过解耦的位置采样和数值插值重采样为均匀分布，最后在空间域直接进行基于测地距离的球形卷积和池化，即可实现镜头无关且天然旋转等变的视觉处理，无需昂贵的球谐变换。

| 字段 | 内容 |
|------|------|
| 中文题名 | 统一球面前端：从任意相机学习球面图像的旋转等变表示 |
| 英文题名 | Unified Spherical Frontend: Learning Rotation-Equivariant Representations of Spherical Images from Any Camera |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2511.18174) · [Code](https://github.com/rusty1s/pytorch_scatter) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction #topic/representation_self_supervised_transfer |
| Method | Unified Spherical Frontend (USF) |
| Dataset | Spherical MNIST, PANDORA, Stanford 2D-3D-S, Stanford 2D-3D-S Lens Generalization |

> [!tip] 效果简介
> - Spherical MNIST 上，NR Accuracy / RR Accuracy 87.18% / 85.43% (Spherical Dis PWC ×3) vs 98.45% / 41.08% (Planar S²CNN) (Proposed drop: -1.75%; Baseline drop: -57.37%)。
> - PANDORA (Object Detection) 上，mAP10 (NR/RR) 29.54% / 29.59% (Spherical YOLOv11) vs 39.65% / 12.71% (Planar YOLOv11) (Proposed drop: +0.05%; Baseline drop: -26.94%)。
> - Stanford 2D-3D-S (Semantic Segmentation) 上，mIoU (NR/RR) 28.78% / 28.09% (Spherical DeepLab v3) vs 35.01% / 12.11% (Planar DeepLab v3) (Proposed drop: -0.69%; Baseline drop: -22.90%)。

## 概要

**核心问题：平面CNN的畸变困境。** 传统卷积神经网络（CNN）在规则像素网格上运行，其基本假设是图像邻域在物理空间中也是邻近的。然而，当相机视场角（FoV）增大或使用鱼眼镜头时，这一假设被严重破坏——由高斯绝妙定理保证，任何将球面信息投影到二维平面的过程必然引入畸变。这导致两个后果：其一，模型对输入图像的全局旋转高度敏感，训练时未见的旋转角度会使性能急剧崩溃；其二，模型与镜头类型强绑定，在针孔相机上训练的模型无法直接迁移至鱼眼或全景相机。

**核心方案：统一球面前端（Unified Spherical Frontend, USF）。** USF提出将视觉处理从平面提升到单位球面——所有相机拍摄的图像，只要标定了内参，都可以通过射线方向映射投影到同一个球面上。在球面上，USF执行三个关键操作：重采样（将非均匀投影点转化为近均匀分布）、球形卷积（基于测地距离的邻域聚合）和球形池化。整个管线在空间域完成，避免了昂贵的球谐变换，且通过几何缓存机制使高分辨率处理在计算上可行。

**核心洞察：架构层面的旋转等变。** USF的旋转鲁棒性来自构造而非数据增强。当卷积核的权重仅依赖于测地距离（即径向核）时，对球面输入施加任意SO(3)旋转，输出特征将以相同方式旋转——这是旋转等变性的严格保证。实验表明，仅距离加权的球形模型在随机旋转测试下性能下降不足1%，而平面模型在相同条件下性能崩溃（如DeepLab v3语义分割mIoU从35.01%骤降至12.11%）。

**方法定位。** USF属于**空间域球面CNN**，与谐波域方法（如SO(3) CNN）形成对比。它不要求输入为完整球面全景图，而是通过解耦的位置采样和数值插值，将任意相机模型的局部球面投影统一为标准表示，再馈入由球形卷积和池化层组成的骨干网络。这种设计使其天然支持**镜头无关**的视觉处理。

**主要结果概览。** 在MNIST分类、PANDORA目标检测和Stanford 2D-3D-S语义分割三个任务上，USF均展现出显著的旋转鲁棒性优势：球形模型在无旋转增强训练的条件下，随机旋转测试性能几乎不变，而平面模型均出现大幅下降。在零镜头镜头泛化实验中，球形模型在未见过的镜头类型上性能退化明显小于平面模型，但尚未完全消除跨镜头差距。



### 广角感知的几何困境

现代视觉系统越来越多地部署在自动驾驶、机器人、AR/VR等需要大视场（FoV）感知的场景中，广角、鱼眼和全景相机因此成为标配。然而，这些相机引入的严重光学畸变给基于卷积神经网络（CNN）的视觉处理带来了根本性挑战。

问题的核心在于**高斯绝妙定理**（Theorema Egregium）所揭示的几何事实：任何将球面（或部分球面）投影到二维平面的映射都必然引入畸变。这意味着，在平面图像上定义的规则像素邻域——传统CNN赖以工作的基础——无法真实反映物理空间中点的邻近关系。以鱼眼图像为例，靠近边缘的像素在物理空间中覆盖的立体角远小于中心像素，但平面CNN的方形卷积核对此一无所知，将空间上不均匀采样的信息当作均匀网格处理。

这种几何失配的直接后果是：**平面CNN对输入图像的全局旋转高度敏感**。当相机发生旋转时，同一物理点的像素位置在畸变图像上发生非线性偏移，平面CNN无法通过简单的平移等变性来补偿这种变化。实践中，研究者不得不依赖大规模旋转数据增强来强行让模型“记住”各种旋转姿态下的外观，这不仅增加了训练成本，更关键的是，模型学到的只是特定相机-镜头组合下的旋转不变性近似，一旦更换镜头类型，这种脆弱的“不变性”便会瓦解。

### 现有球面方法的瓶颈

针对上述问题，学界已探索将CNN直接构建在球面上的方案。其中最具代表性的是**球谐域方法**（如SO(3) CNN），其核心思路是将球面信号变换到球谐（傅里叶）域，在该域中旋转操作简化为Wigner-D矩阵的乘法，从而天然实现旋转等变。然而，这一路径存在严重的工程瓶颈：球谐变换的计算复杂度随分辨率平方增长，对于现代视觉任务所需的高分辨率输入（如全景分割中的960×480及以上）而言，计算开销令人望而却步。

另一类工作在空间域直接操作球面点云，但因缺乏系统性的架构设计，往往只能处理特定的输入格式（如仅支持全景图），无法灵活适配针孔、鱼眼等任意相机模型。更重要的是，这些方法在旋转鲁棒性、计算效率、与现代视觉架构的兼容性之间始终未能取得令人满意的平衡。

### 本文动机：从数据增强到架构保障

本文的核心洞察是：**旋转等变性不应通过数据增强来“学习”，而应通过架构设计来“保证”**。如果所有操作——从输入重采样到卷积、池化——都在单位球面的几何空间中进行，并且卷积核仅依赖于测地距离（而非像素坐标），那么模型对任意SO(3)旋转自然等变，无需任何旋转增强即可保持稳定的预测。

基于这一思想，本文提出**统一球面前端（Unified Spherical Frontend, USF）**，一个将任意相机模型拍摄的图像统一映射到球面、并在空间域执行旋转等变处理的通用管线。USF通过解耦的位置采样与数值插值实现镜头无关的球面重采样，通过仅距离加权的球形卷积核从构造上保证旋转等变性，同时借助几何缓存机制使高分辨率球面处理在计算上可行。这一设计使得现代视觉架构（如YOLOv11、DeepLab v3、UNet）只需将其平面卷积/池化层替换为球面对应层，即可获得镜头无关且天然旋转等变的感知能力。



## 核心方法与创新机理

USF的核心创新在于将视觉处理的计算域从畸变平面提升至单位球面，通过**解耦的模块化设计**和**空间域球形算子**，在不依赖数据增强的前提下实现架构层面的SO(3)旋转等变。其关键创新点可归纳为以下四个维度的“changed slots”：

### 1. 输入端：从平面像素到球面统一表示

传统平面CNN直接将原始图像像素作为输入，像素邻域关系被畸变严重扭曲。USF将任意标定相机的图像通过**射线方向映射**$\mathbf{u} \in \mathbb{R}^2 \mapsto \mathbf{p_u} \in \mathbb{S}^2$投影至单位球面，再通过解耦的**位置采样**与**数值插值**重采样为近均匀分布。这一过程将相机模型（针孔、鱼眼、全景等）的差异完全隔离在前端，使得下游网络始终处理几何一致的球面信号，从根本上消除了镜头类型对特征学习的干扰（见Figure 3）。

### 2. 卷积操作：从方形核到基于测地距离的球形核

平面卷积在规则像素网格上使用$5\times5$方形核进行加权求和：

$$x _ { o } = \sum _ { k \in \mathcal { N } ( \mathbf { p } _ { o } ) } x _ { k } \omega _ { k }$$

其中邻域由核大小的像素偏移定义。USF将其替换为**球形卷积**，在测地距离定义的圆形帽邻域上进行平均归约：

$$x_o = \frac{1}{|\mathcal{N}(\mathbf{p}_o)|} \sum_{k \in \mathcal{N}(\mathbf{p}_o)} x_k \prod_m f_{\mathrm{weight}}^{(m)}(\mathcal{M}_m(\mathbf{p}_k, \mathbf{p}_o))$$

其中邻域定义为$\mathcal{N}(\mathbf{p}_o) = \{ k : \mathbf{p}_k \in \mathcal{P}_i, d(\mathbf{p}_k, \mathbf{p}_o) \leq r \}$。核权重由可学习的距离函数（和可选的方向函数）决定。**仅使用距离加权的径向核**（如分段常数PWC或MLP）通过构造保证了旋转等变性——权重仅依赖于测地距离，而测地距离在旋转下保持不变。

### 3. 池化与下采样：从矩形窗口到测地邻域

平面MaxPool2d在矩形窗口内计算最大值，下采样通过步长2的卷积实现。USF将池化操作统一为在同样基于测地距离定义的邻域上应用规约函数：

$$x_o = \mathcal{K}_{\mathrm{pool}}(\mathcal{X}_i, \mathbf{p}_o) = f_{\mathrm{pool}}(x_k : k \in \mathcal{N}(\mathbf{p}_o))$$

下采样则通过位置采样器的分辨率因子控制输出点密度（每层将输出点数降至输入的1/4），上采样时对齐对应层的位置以实现跳跃连接。由于所有几何结构（邻域、插值权重、聚合索引）与特征值无关，可通过**几何缓存**机制预先计算并复用，大幅降低在线计算开销。

### 4. 架构哲学：从数据增强到结构等变

最根本的范式转变在于：平面CNN依赖大量旋转数据增强来近似旋转鲁棒性，而USF通过将**所有操作（重采样、卷积、池化）提升到球面空间进行**，从架构层面实现旋转等变。这一设计使得模型在训练时无需任何旋转增强，即可在随机旋转测试下保持性能稳定——语义分割mIoU仅下降0.69%，而平面模型骤降22.90%（Table 4）。



**统一球面前端（Unified Spherical Frontend, USF）** 提出了一套从任意标定相机到任意下游架构的球面处理管线，其核心设计理念是将所有视觉操作——重采样、卷积、池化——提升到单位球面 $\mathbb{S}^2$ 上执行，从而在架构层面实现 SO(3) 旋转等变性，而非依赖数据增强。

### 管线总览

USF 的完整处理流程由六个阶段构成（见 Figure 3），各模块解耦设计，几何计算与特征计算完全分离：

![[assets/figures/papers/paper_list_l2615_https_arxiv_org_abs_2511_18174/figures/003_Figure_3.jpg]]
*Figure 3: Unified Spherical Frontend. (i) A planar image and its lens normal map can be combined to form a (ii) spherical image. Cameras with different lenses produce spatially varying densities and distributions of pixels when projected onto the sphere. Thus, it is crucial to perform (iii) resampling before (iv) feeding into the backbone composed of spherical convolution and pooling layer. Optionally, the results can be (v) resampled back into the raw projected spherical image pixel locations, and (vi) unproject back to the planar image for downstream integration*

1. **球面投影（Spherical Projection）**：给定标定相机的内参和畸变模型，将平面图像坐标 $\mathbf{u} \in \mathbb{R}^2$ 映射为单位球面上的射线方向 $\mathbf{p_u} \in \mathbb{S}^2$，形成球面图像。不同镜头类型（针孔、鱼眼、全景等）投影后在球面上的点密度和空间分布差异显著。

2. **位置采样（Location Sampling）**：从原始投影点集中选取具有近均匀空间分布的新位置，匹配输入球面图像的密度和视场覆盖范围。支持多种采样策略，包括 Goldberg 多面体、HEALPix、斐波那契格等（见 Figure 4），其中 **Icosahedron（二十面体）采样** 在实验中展现出最佳的旋转稳定性与精度平衡。

3. **数值插值（Value Interpolation）**：在新采样位置通过邻域聚合和局部加权计算特征值。采用两阶段过程——先确定测地距离邻域，再用径向基函数（RBF）计算归一化权重：
   $$x_o = \sum_{k \in \mathcal{N}(\mathbf{p}_o)} \omega_k \cdot x_k$$
   权重 $\omega_k$ 仅依赖于测地距离，支持软最大、高斯等核函数。此阶段与位置采样完全解耦，可独立配置。

4. **球面骨干网络（Spherical Backbone）**：由球形卷积层和球形池化层交替堆叠构成，在重采样后的近均匀球面点上执行特征提取。输出点位置由位置采样器以分辨率因子控制密度，实现下采样（每层点数降至输入的 1/4，等价于平面 CNN 的 stride-2）和上采样（对齐对应层位置以支持跳跃连接）。

5. **反向重采样（Optional Resampling Back）**：将球面特征回投到原始投影球面图像的像素位置，便于与平面域的下游模块集成。

6. **反投影（Unprojection）**：将球面表示反投影回平面图像域，用于最终指标评估或与现有平面视觉系统的对接。

### 核心算子设计

USF 的球形卷积与池化在统一的测地邻域上操作。对于输出点 $\mathbf{p}_o$，其邻域定义为所有与其测地距离不超过半径 $r$ 的输入点：
$$\mathcal{N}(\mathbf{p}_o) = \{ k : \mathbf{p}_k \in \mathcal{P}_i, \ d(\mathbf{p}_k, \mathbf{p}_o) \leq r \}$$

球形卷积在此邻域上对输入特征进行加权平均：
$$\boldsymbol{x_o} = \mathcal{K}_{\mathrm{conv}}(\mathcal{X}_i, \mathbf{p}_o) = \frac{1}{|\mathcal{N}(\mathbf{p}_o)|} \sum_{k \in \mathcal{N}(\mathbf{p}_o)} x_k \prod_m f_{\mathrm{weight}}^{(m)}\left( \mathcal{M}_m(\mathbf{p}_k, \mathbf{p}_o) \right)$$
其中 $f_{\mathrm{weight}}^{(m)}$ 是可学习的权重函数，$\mathcal{M}_m$ 是相对几何测量量。核函数支持两种分解模式：

- **仅距离加权（Dis PWC / Dis MLP）**：权重仅依赖于测地距离 $d(\mathbf{p}_k, \mathbf{p}_o)$，通过构造保证旋转等变性。这是实现旋转鲁棒性的关键因果机制。
- **距离+方向加权（Dis×Dir）**：额外引入局部切平面上的 1D 方向信息，可捕捉方向敏感特征（如区分“6”和“9”），但牺牲了旋转等变性。

球形池化在同样的测地邻域上应用规约函数：
$$x_o = \mathcal{K}_{\mathrm{pool}}(\mathcal{X}_i, \mathbf{p}_o) = f_{\mathrm{pool}}\left( x_k : k \in \mathcal{N}(\mathbf{p}_o) \right)$$
其中 $f_{\mathrm{pool}}$ 可以是 max、average 等操作。池化层与卷积层共享几何缓存，进一步降低计算开销。

### 几何缓存机制

由于各层的输入/输出点位置在球面上固定（由位置采样器预先确定），所有与特征值无关的几何计算——邻域结构、插值权重、聚合索引——可在首次前向传播后预先计算并缓存。后续推理直接复用这些缓存，将球形卷积和池化降维为矩阵乘法操作（见 Figure 9、Figure 10）。这一机制是实现高分辨率球面处理计算可行的关键设计，使得球面网络在理论 FLOPs 更低的情况下，实际运行时间约为平面网络的 2×（缺乏定制 CUDA 核优化）。

![[assets/figures/papers/paper_list_l2615_https_arxiv_org_abs_2511_18174/figures/015_Figure_9.jpg]]
*Figure 9: Location Sampling and Value Interpolation Benchmarks. Cold-start runtime includes geometric preprocessing such as neighborhood construction and interpolation weight computation. Sustained runtime reuses geometry and only performs value aggregation via matrix multiplication*

### 与平面 CNN 的本质差异

传统平面 CNN 在规则像素网格上使用方形卷积核：
$$x_o = K_{\mathrm{conv}}(\mathcal{X}_i, \mathbf{p}_o) = \sum_{k \in \mathcal{N}(\mathbf{p}_o)} x_k \omega_k$$
其邻域由固定核大小在图像坐标空间定义，无法反映物理空间中的真实邻近关系——这是由高斯绝妙定理保证的：任何二维投影都会引入畸变。USF 通过将所有操作提升到球面空间，从根本上解决了这一瓶颈：邻域由测地距离定义，卷积核通过仅依赖距离的径向权重保证旋转等变，使得模型在未见过的旋转和镜头类型下仍能保持稳定性能。

### 补充图表

![[assets/figures/papers/paper_list_l2615_https_arxiv_org_abs_2511_18174/figures/001_Figure_1.jpg]]
*Figure 1: Unified Spherical Representation. From any camera to any architecture: a unified spherical pipeline for modern vision*



### 3.1 从平面到球面：统一投影与重采样

USF 的核心前提是将任意标定相机的图像提升到单位球面 $\mathbb{S}^2$ 上进行处理。给定相机内参和畸变模型，每个图像坐标 $\mathbf{u} \in \mathbb{R}^2$ 映射为一个射线方向 $\mathbf{p_u} \in \mathbb{S}^2$，形成**球面图像**。然而，不同镜头类型（针孔、鱼眼、全景）在投影后产生空间上极度非均匀的像素密度分布（Figure 3），直接在此非均匀点集上进行卷积会引入严重的空间偏差。因此，USF 在球面处理之前插入一个解耦的**重采样模块**，由两步构成：

- **位置采样**：从原始投影点集中选择具有近均匀空间分布的新位置，支持 Goldberg 多面体、HEALPix、斐波那契格等多种策略（Figure 4）。
- **数值插值**：在新采样位置通过邻域聚合和局部加权计算特征值。插值采用径向基函数（RBF）核，权重仅依赖于测地距离：

![[assets/figures/papers/paper_list_l2615_https_arxiv_org_abs_2511_18174/figures/004_Figure_4.jpg]]
*Figure 4: Spherical Sampling Methods. Various location sampling strategies produce different levels of uniformity across the sphere. The bottom row displays point distributions with higher uniformity compared to coarser Goldberg polyhedron discretizations*

$$x_o = \sum_{k \in \mathcal{N}(\mathbf{p}_o)} \omega_k \cdot x_k$$

其中权重 $\omega_k$ 由 RBF 核计算并归一化，$\mathcal{N}(\mathbf{p}_o)$ 为输出点 $\mathbf{p}_o$ 的测地邻域。

整个重采样过程的几何映射（邻域结构、插值权重、聚合索引）与特征值无关，可预先计算并缓存，后续前向传播直接复用，大幅降低在线计算开销。

### 3.2 球面卷积与池化

#### 3.2.1 平面卷积的局限

标准平面 CNN 的卷积定义为在规则像素网格上的加权求和：

$$x_o = \mathcal{K}_{\mathrm{conv}}(\mathcal{X}_i, \mathbf{p}_o) = \sum_{k \in \mathcal{N}(\mathbf{p}_o)} x_k \omega_k$$

其中邻域由方形核大小决定：$\mathcal{N}(\mathbf{p}_o) = \{k : \mathbf{p}_k = \mathbf{p}_o \pm \lfloor \frac{\mathrm{kernel\ size}}{2} \rfloor\}$。这种定义依赖于欧氏空间的平移不变性，在球面上不再成立——像素邻域无法真实反映物理空间中的邻近关系（高斯绝妙定理保证任何二维投影都会引入畸变），导致模型对全局旋转敏感。

#### 3.2.2 球形卷积

USF 将卷积操作提升到球面，定义球形卷积为在**测地距离**定义的圆形帽邻域上的局部聚合：

$$\mathcal{N}(\mathbf{p}_o) = \{ k : \mathbf{p}_k \in \mathcal{P}_i, \ d(\mathbf{p}_k, \mathbf{p}_o) \leq r \}$$

其中 $d(\cdot, \cdot)$ 为测地距离，$r$ 为邻域半径。输出特征为邻域内输入值的**加权平均**（平均归约而非求和，以处理非均匀采样带来的尺度不一致）：

$$\mathbf{x}_o = \mathcal{K}_{\mathrm{conv}}(\mathcal{X}_i, \mathbf{p}_o) = \frac{1}{|\mathcal{N}(\mathbf{p}_o)|} \sum_{k \in \mathcal{N}(\mathbf{p}_o)} x_k \prod_m f_{\mathrm{weight}}^{(m)}\left(\mathcal{M}_m(\mathbf{p}_k, \mathbf{p}_o)\right)$$

核函数 $f_{\mathrm{weight}}^{(m)}$ 从相对几何测量 $\mathcal{M}_m$ 中计算权重。USF 使用两种几何测量：

- **测地距离** $d(\mathbf{p}_k, \mathbf{p}_o)$：两点在球面上的最短弧长。
- **局部 1D 方向**：$\mathbf{p}_k$ 在 $\mathbf{p}_o$ 处切平面上的方向角。

核函数可分解为距离分支和方向分支的乘积。**仅保留距离分支**（径向核，如分段常数 PWC 或 MLP）通过构造保证了 SO(3) 旋转等变性：当输入球面图像旋转时，任意两点间的测地距离不变，因此卷积输出随之等变旋转。**加入方向分支**后核函数失去旋转等变性，但可捕捉方向敏感特征（如区分“6”和“9”）。

Table 1 展示了不同核参数化方案下输入-输出通道间的激活权重可视化：径向核产生各向同性的圆形感受野，方向核则引入角度选择性。

![[assets/figures/papers/paper_list_l2615_https_arxiv_org_abs_2511_18174/figures/005_Table_1.jpg]]
*Table 1: Generic Spherical CNN. Brown and blue dots denote input and output locations. Colors visualize the activation weights between a given input-output channel pair*

#### 3.2.3 球形池化

球形池化在同样的测地邻域上应用规约函数：

$$x_o = \mathcal{K}_{\mathrm{pool}}(\mathcal{X}_i, \mathbf{p}_o) = f_{\mathrm{pool}}\left(x_k : k \in \mathcal{N}(\mathbf{p}_o)\right)$$

其中 $f_{\mathrm{pool}}$ 可为 $\max$、$\mathrm{average}$ 等。池化层与卷积层共享相同的邻域定义和几何缓存，保持架构一致性。

### 3.3 下采样与上采样

球面网络通过**位置采样器的分辨率因子**控制输出点密度，实现与平面网络步长卷积等价的下采样/上采样：

- **下采样**：每层将输出点数减少至输入的 $1/4$，等价于平面 CNN 中 stride-2 的下采样。
- **上采样**：通过位置采样器生成更高分辨率的输出点，并对齐对应下采样层的位置以实现跳跃连接（如 UNet 架构中的 skip connection）。

由于所有层的输出位置坐标在初始化后固定，输入-输出间的全部几何测量可在首次前向传播后缓存，后续推理直接复用，实现高效计算（Figure 10）。

### 3.4 旋转等变性的架构保证

Figure 2 给出了旋转等变与不变的严格定义：函数 $\mathcal{K}$ 是旋转等变的，当且仅当 $\mathcal{K}(R \cdot \mathbf{x}) = R \cdot \mathcal{K}(\mathbf{x})$ 对所有 $R \in \mathrm{SO}(3)$ 成立。

![[assets/figures/papers/paper_list_l2615_https_arxiv_org_abs_2511_18174/figures/002_Figure_2.jpg]]
*Figure 2: Rotation Equivariance and Invariance. A function K is rotation-equivariant if KE(R · x) = R · KE(x), and rotationinvariant if KI (R · x) = KI (x), for all R ∈ SO(3)*

USF 的旋转等变性来源于两个架构层面的设计：

1. **测地距离的旋转不变性**：球面上任意两点间的测地距离在 SO(3) 旋转下保持不变，因此仅依赖距离的径向核天然产生等变输出。
2. **平均归约的尺度一致性**：使用邻域基数归一化的平均聚合替代求和，确保在非均匀采样下输出尺度不随邻域大小波动。

这使得 USF 无需在训练时进行旋转数据增强，即可在测试时面对任意随机旋转保持稳定性能——这是与依赖数据增强强行学习旋转不变性的平面 CNN 之间的**因果性差异**，而非仅仅是性能指标的提升。



## 实验与关键发现

### 旋转等变性验证：MNIST分类

为验证USF的旋转等变特性，作者首先在受控的Spherical MNIST数据集上进行分类实验。所有模型均在**无随机旋转**的条件下训练，测试时分别评估非旋转（NR）和随机旋转（RR）两种条件下的准确率。

**Table 2** 展示了核心对比结果。平面CNN（Planar S²CNN）在非旋转条件下达到98.45%的高准确率，但在随机旋转下骤降至41.08%，性能崩溃幅度高达57.37%。这表明平面CNN学到的特征对全局旋转极度敏感，即使经过充分的非旋转数据训练，也无法泛化到旋转后的输入。

相比之下，仅使用距离加权的球形卷积核（Spherical Dis PWC ×3）在非旋转条件下准确率为87.18%，随机旋转下仅下降1.75%至85.43%，展现出**内置的旋转等变性**。使用MLP参数化距离核并加入高频傅里叶嵌入的变体（Spherical Dis MLP[8,8], L=6）进一步将旋转下准确率提升至91.50%。

消融实验揭示了一个关键的**能力-等变性权衡**：
- 加入方向分支的核函数（Spherical Dis×Dir MLP）在非旋转条件下达到98.28%，几乎追平平面CNN，因为它能捕捉方向敏感特征（如区分“6”和“9”）；
- 然而，该变体在随机旋转下准确率跌至43.54%，**丧失了旋转等变性**，因为方向分支的权重依赖于局部切平面上的角度，而该角度随全局旋转而改变。

这一结果直接验证了论文的核心设计原则：**仅距离加权的径向核通过构造保证旋转等变性**，而引入方向感知能力必然牺牲等变性。

### 目标检测：PANDORA数据集

为验证USF在复杂视觉任务上的适用性，作者将YOLOv11检测头的平面卷积/池化层替换为球面对应层，在PANDORA数据集上进行目标检测实验。

**Table 3** 的结果与MNIST实验高度一致：
- 平面YOLOv11在非旋转条件下mAP₁₀为39.65%，随机旋转下暴跌至12.71%（降幅26.94%）；
- 球形YOLOv11在非旋转条件下mAP₁₀为29.54%，随机旋转下**微升至29.59%**（+0.05%），性能几乎完全保持稳定。

球形模型在非旋转条件下的绝对性能低于平面模型，这一差距主要源于两方面：一是旋转等变核的表征能力受限（无法利用方向信息）；二是球面算子目前基于PyTorch scatter实现，缺乏定制CUDA核优化，训练效率受限导致调参不充分。但旋转稳定性的大幅提升验证了USF在目标检测任务上的旋转等变能力。

### 语义分割：Stanford 2D-3D-S数据集

在Stanford 2D-3D-S语义分割任务上，作者将DeepLab v3和UNet的平面卷积/池化层替换为球面对应层。

**Table 4** 的结果进一步巩固了前述发现：
- 平面DeepLab v3：非旋转mIoU 35.01% → 旋转mIoU 12.11%（**降幅22.90%**）；
- 球形DeepLab v3：非旋转mIoU 28.78% → 旋转mIoU 28.09%（**降幅仅0.69%**）；
- 球形UNet：非旋转mIoU 28.09% → 旋转mIoU 27.77%（降幅0.32%）。

值得注意的是，球形模型在旋转条件下**反超**了平面模型（28.09% vs 12.11%），这是旋转等变架构在实际应用中的核心价值：当测试分布包含未见过的旋转时，等变模型无需依赖昂贵的数据增强即可保持鲁棒。

### 零镜头镜头泛化

USF的另一核心优势是镜头无关性。**Table 5** 展示了零镜头镜头泛化实验：模型仅在针孔相机数据上训练，直接测试在鱼眼和全景相机数据上的性能。

![[assets/figures/papers/paper_list_l2615_https_arxiv_org_abs_2511_18174/figures/010_Table_5.jpg]]
*Table 5: Zero-shot Lens Generalizability Test. Overfitted and tested on the same batch. Random rotation is disabled*

- 平面DeepLab v3在针孔→针孔上mIoU为53.75%，跨镜头至鱼眼降至33.47%，至全景**骤降至19.57%**（最大降幅34.18%）；
- 球形DeepLab v3在针孔→针孔上mIoU为48.71%，跨镜头至鱼眼为36.51%，至全景为35.62%（最大降幅13.09%）。

球形模型显著缩小了跨镜头性能差距，但**未能完全消除**性能下降。这表明球面重采样虽然统一了不同镜头的几何表示，但镜头间在分辨率分布、视场覆盖密度等方面的差异仍对特征学习构成挑战。**Table 7**（全数据集镜头适应性测试）提供了更全面的补充结果。

![[assets/figures/papers/paper_list_l2615_https_arxiv_org_abs_2511_18174/figures/018_Table_7.jpg]]
*Table 7: Semantic Segmentation Full-dataset Lens Adaptability Test. Random Rotation is disabled*

### 消融研究：位置采样与核参数化

**Table 6** 对关键超参数进行了系统消融：

**位置采样策略**对旋转等变性影响深远：
- Icosahedron（Goldberg多面体）采样在旋转鲁棒性与精度之间取得最佳平衡（NR mIoU 28.78%，RR mIoU 28.09%）；
- Fibonacci和HEALPix等非均匀采样方案**严重破坏旋转等变性**：Fibonacci采样在随机旋转下mIoU跌至12.60%，几乎与平面模型相当。这是因为非均匀采样引入了空间偏差，使得旋转后的特征分布无法与学习到的核权重对齐。

**核参数化**对表达能力至关重要：
- 3段离散PWC核在简单性与效果间取得良好平衡；
- 低频率MLP（无傅里叶嵌入）的表现甚至不如简单PWC设计，因为其平滑先验限制了拟合复杂距离-权重函数的能力；
- 加入高频傅里叶编码（L=6或L=8）可大幅恢复甚至超越PWC的性能，因为高频基函数赋予MLP足够的表达能力来学习精细的距离依赖模式。

### 失败模式与局限性

1. **方向敏感任务的固有劣势**：纯旋转等变卷积核无法区分方向敏感特征（如“6”和“9”），在需要方向感知的任务中准确率不如可学习方向核变体或平面CNN。这是旋转等变性与方向敏感性之间不可调和的架构权衡。

2. **跨镜头泛化不彻底**：尽管球形模型大幅缩小了跨镜头性能差距，但在极端镜头差异（如针孔→全景）下仍有约13%的mIoU下降，表明统一球面表示尚未完全消除镜头域迁移问题。

3. **推理效率瓶颈**：球面算子基于PyTorch scatter/sparse实现，实际运行时间约为平面网络的2倍（见**Figure 11**），尽管理论FLOPs更低。几何缓存机制缓解了重复计算，但缺乏定制CUDA核限制了实际部署效率。

4. **标定依赖**：框架假定已知精确的相机内参和镜头畸变模型，未考虑标定误差或动态畸变场景下的鲁棒性。

### 补充图表

![[assets/figures/papers/paper_list_l2615_https_arxiv_org_abs_2511_18174/figures/007_Table_2.jpg]]
*Table 2: MNIST Classification Results. All models are trained without random rotation. L denotes embedding levels*

![[assets/figures/papers/paper_list_l2615_https_arxiv_org_abs_2511_18174/figures/009_Table_4.jpg]]
*Table 4: Semantic Segmentation Results on Stanford 2D-3D-S*

![[assets/figures/papers/paper_list_l2615_https_arxiv_org_abs_2511_18174/figures/008_Table_3.jpg]]
*Table 3: Object Detection Results on PANDORA Dataset*

![[assets/figures/papers/paper_list_l2615_https_arxiv_org_abs_2511_18174/figures/011_Table_6.jpg]]
*Table 6: Ablation Study on Hyperparameters. Random rotation is disabled during training*



## 定位与知识库关联

### 1. 问题定位：从畸变容忍到架构级等变

传统视觉前端处理广角、鱼眼或全景图像时面临一个根本性几何约束：根据高斯绝妙定理（Theorema Egregium），任何二维投影都必然引入畸变，导致图像空间的像素邻域无法真实反映物理空间中的邻近关系。平面CNN在规则像素网格上定义的方形卷积核，其邻域语义在畸变图像上被扭曲，使得模型对图像全局旋转高度敏感。现有应对策略主要依赖大规模旋转数据增强，这不仅增加了训练成本，且无法泛化到训练时未见过的镜头类型。

USF的核心定位是将这一问题的解决从**数据层面提升到架构层面**：通过将所有操作（重采样、卷积、池化）提升到单位球面 $S^2$ 上进行，利用仅距离加权的旋转等变卷积核，从构造上保证 $SO(3)$ 旋转等变性，而非通过数据增强来近似。

### 2. 与谐波域球面CNN的关系

球面CNN并非全新概念。早期工作（如**SO(3) CNN**）在谐波域通过球谐变换实现精确的旋转等变，但计算代价高昂，且难以与现代视觉架构（如YOLO、DeepLab）深度集成。USF选择在**空间域**直接进行基于测地距离的球形卷积和池化，避免昂贵的球谐变换，同时保持与现代CNN骨干网络（YOLOv11、DeepLab v3、UNet）的即插即用兼容性。在MNIST分类实验中，谐波域SO(3) CNN作为基线被直接对比，USF的空间域方案在旋转鲁棒性上表现相当，但架构灵活性和计算效率显著更优。

### 3. 与平面视觉架构的关系

USF的设计哲学是**最小侵入式替换**：不改变宏观网络架构，仅将平面卷积/池化层替换为球面对应层。具体而言：

- **YOLOv11**：将原有的Conv2d + MaxPool2d替换为球形卷积 + 球形池化，检测头复用R-CenterNet的检测头设计。
- **DeepLab v3**：保留ASPP（空洞空间金字塔池化）等高级语义模块，仅将前端特征提取的卷积和池化操作球面化。
- **UNet**：跳跃连接通过上采样时对齐对应层的位置采样点来实现，保持编码器-解码器结构的完整性。

这种设计使得USF可以无缝接入现有视觉架构生态，所有实验均采用与平面基线完全相同的训练协议，确保对比的公平性。需要指出，球面模型由于目前基于PyTorch scatter/sparse实现，缺乏定制CUDA内核优化，实际运行时间约为平面网络的2倍，但理论FLOPs更低——这意味着一旦底层算子得到优化，USF有望实现实际加速。

### 4. 适用边界

USF的旋转等变性建立在两个关键前提之上：

1. **精确的相机标定**：框架假定已知精确的相机内参和镜头畸变模型，通过射线方向映射将图像投影至球面。校准误差或动态畸变会破坏球面表示的几何一致性，进而削弱等变性质。
2. **仅距离加权核**：旋转等变性由核函数仅依赖测地距离来保证。一旦引入方向分支以捕捉方向敏感特征（如区分“6”和“9”），等变性即被打破——在非旋转MNIST上可达98.28%，与平面CNN相当，但随机旋转下性能骤降至43.54%。

此外，零镜头镜头泛化实验表明，USF在未见过的镜头类型上性能下降明显小于平面模型（如从针孔切换至全景时，球形DeepLab v3的mIoU从48.71%降至35.62%，而平面模型从53.75%降至19.57%），但并未完全消除跨镜头性能差异，在极端镜头差异下仍存在不可忽略的退化。

### 5. 局限与开放问题

**已知局限**：

- **方向敏感性缺失**：纯旋转等变卷积核无法建模方向敏感特征，在需要方向感知的任务中准确率不如可学习方向核的变体。
- **跨镜头泛化不完美**：虽优于平面模型，但未完全消除性能下降。
- **运行效率瓶颈**：缺乏定制CUDA内核，实际运行时间为平面网络的约2倍。
- **标定依赖性**：未考虑无标定或弱标定场景。

**开放问题**：

1. 如何设计既保持旋转等变又具备方向敏感性的球面卷积核？引入规范等变（gauge-equivariant）架构可能是潜在方向。
2. 能否通过开发定制CUDA核使球面算子在运行时间上超越平面实现，达成实际加速？
3. USF能否扩展到多相机系统（如环视相机）的拼接与融合，以及视频序列中的时空旋转等变建模？
4. 在无标定或弱标定条件下，如何从图像本身学习或估计球面投影映射，使USF摆脱对精确内参的依赖？



## 原文 PDF

![[paperPDFs/CVPR_2026/Unified_Spherical_Frontend_Learning_Rotation_Equivariant_Representations_of_Spherical_Images_from_Any_Camera.pdf]]
