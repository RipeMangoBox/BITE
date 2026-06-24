---
title: Neural Harmonic Textures for High-Quality Primitive Based Neural Reconstruction
type: paper
paper_level: A
venue: arXiv
year: 2026
pdf_ref: paperPDFs/arxiv_2026/Neural_Harmonic_Textures_for_High_Quality_Primitive_Based_Neural_Reconstruction.pdf
aliases:
- NHTN
- NHTHQPBNR
tags:
- arxiv_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
core_operator: 每基元附加的虚拟四面体特征向量维数、谐波编码（正弦/余弦）及延迟着色MLP解码器的设计，实现对几何与外观的解耦与每基元表达力的提升。
primary_logic: 将基元自身视为局部位置编码器和几何载体，通过附加学习特征向量并在alpha混合前用正弦/余弦函数编码，将信号分解为谐波分量（频率与振幅），然后通过一次轻量MLP在图像空间解码，从而在保持基元表示结构优势的同时大幅提升单基元的表达能力，并显著减少神经网络推理次数。
claims:
- 在MipNeRF360、Tanks & Temples和Deep Blending三个标准数据集上，Neural Harmonic Textures在所有指标（PSNR/SSIM/LPIPS）上均优于现有实时与离线方法，包括Spherical Voronoi等先进外观模型。
- 在严格控制变量的实验中（相同框架、基元数、训练迭代数、每基元外观参数量），NHT一致优于球谐（SH）和球面Voronoi（SV）模型，且保持实时渲染性能。
- NHT在低基元数量区间（≤100k）优势尤为突出，PSNR领先达到2dB以上，证明了单基元表达力的显著增强。
- MipNeRF360 上 PSNR = 28.46
---

# Neural Harmonic Textures for High-Quality Primitive Based Neural Reconstruction

> [!tip] 核心洞察
> 将基元自身视为局部位置编码器和几何载体，通过附加学习特征向量并在alpha混合前用正弦/余弦函数编码，将信号分解为谐波分量（频率与振幅），然后通过一次轻量MLP在图像空间解码，从而在保持基元表示结构优势的同时大幅提升单基元的表达能力，并显著减少神经网络推理次数。

| 字段 | 内容 |
|------|------|
| 中文题名 | 神经谐波纹理：面向高质量基元神经重建 |
| 英文题名 | Neural Harmonic Textures for High-Quality Primitive Based Neural Reconstruction |
| 会议/期刊 | arXiv 2026 |
| Links | [paper](https://arxiv.org/abs/2604.01204) · [arXiv](https://arxiv.org/abs/) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction |
| Method | Neural Harmonic Textures (NHT) |
| Dataset | MipNeRF360, Tanks & Temples, Deep Blending |

> [!tip] 效果简介
> - MipNeRF360 上，PSNR 28.46 vs 28.15 (3DGUT+SV) (+0.31)。
> - Tanks & Temples 上，PSNR 24.79 vs 24.18 (3DGUT+SV) (+0.61)。
> - Deep Blending 上，PSNR 30.88 vs 30.29 (3DGUT+SV) (+0.59)。

## 概述

**问题瓶颈**：传统基元方法（如 3DGS）中几何与外观强耦合，单个基元的表达能力有限。为建模高频细节和复杂视角相关效果，不得不大量增加基元数量，导致内存消耗激增与渲染速度下降。同时，方向外观建模受限于低阶球谐函数，无法高效表示镜面高光等高频现象。

**核心思路**：Neural Harmonic Textures (NHT) 将每个基元同时视为局部位置编码器与几何载体，在其虚拟包围结构上附加可学习的隐式特征向量。在 alpha 混合之前，通过正弦/余弦函数将特征分解为谐波分量（频率与振幅），再经一次轻量 MLP 在图像空间解码为颜色。这一设计在保持基元表示结构优势的前提下，显著提升单基元的表达能力，并大幅减少神经网络推理次数。

**方法定位**：NHT 是一种与基元类型无关的外观建模框架，可与 3D 高斯、2D 高斯、三角形面片等多种基元无缝集成。相比基于球谐函数或球面 Voronoi 的外观模型，NHT 通过“基元绑定特征 → 谐波编码 → 延迟着色”三阶段管线，实现了几何与外观的解耦。

**主要结果**：
- 在 MipNeRF360、Tanks & Temples 和 Deep Blending 三个标准数据集上，NHT 在所有指标（PSNR/SSIM/LPIPS）上均优于现有实时与离线方法。
- 严格控制变量的实验中（相同框架、基元数、训练迭代数、每基元外观参数量），NHT 一致优于球谐模型和球面 Voronoi 模型，且保持实时渲染性能。
- 在低基元数量区间（≤100k），NHT 的 PSNR 领先达 2dB 以上，直接验证了单基元表达力的显著增强。

## 背景与动机

### 基元表示的优势与瓶颈

基于基元（primitive）的场景表示，尤其是以3D高斯喷洒（3DGS）为代表的方法，凭借其显式几何结构和高效的光栅化渲染管线，在实时新视角合成领域取得了突破性进展。这类方法将场景建模为一组离散的几何基元，通过alpha混合沿射线合成像素颜色，天然支持快速渲染与局部编辑。

然而，传统基元方法存在一个根本性瓶颈：**几何与外观的强耦合**。在3DGS及其变体中，每个基元的外观通常由低阶球谐函数（Spherical Harmonics, SH）直接建模——基元的位置、协方差、不透明度等几何属性与视角相关的颜色表达紧密绑定。这种设计的表达能力受限于两方面：

1. **单基元表达力有限**：低阶SH仅能捕获低频的视角相关外观变化，对于镜面高光、复杂材质反射等高频现象建模能力不足。为弥补这一缺陷，现有方法被迫大量增加基元数量，导致内存消耗膨胀和渲染速度下降。
2. **空间变化外观缺失**：SH在每个基元上独立评估，无法表示基元内部的颜色变化或基元间的外观关联，限制了场景表示的紧凑性和保真度。

### 现有改进路径的局限

为突破上述瓶颈，研究者提出了多种改进方案。**球面Voronoi（SV）模型**将方向域离散化为Voronoi单元，以提升高频外观的表达能力，但仍沿袭“每基元独立计算颜色”的范式，未解决几何-外观耦合问题。**神经场方法**（如Instant NGP、Mip-NeRF 360、ZipNeRF）虽能通过MLP解码器实现高质量渲染，但依赖密集的射线采样和逐点网络查询，难以达到实时性能。**混合方法**尝试在基元管线中引入轻量MLP，但通常每基元仍需一次网络推理，计算开销随基元数线性增长。

### 核心动机：解耦几何与外观

本文的核心洞察在于：**基元本身应被视为局部位置编码器和几何载体，而非外观的直接决定者**。通过将可学习的外观特征从几何属性中分离，并设计一种高效的编码-解码机制，可以在保持基元表示结构优势（快速渲染、显式几何）的同时，大幅提升单基元的表达能力。

具体而言，本文提出**Neural Harmonic Textures（NHT）**，其动机源于三个关键设计选择：

- **特征锚定而非直接着色**：每基元附加隐式特征向量（置于虚拟四面体顶点），而非直接存储颜色。这使外观信息与几何解耦，特征可随基元移动、变形，支持编辑与动画。
- **谐波编码增强表达**：对插值后的特征应用正弦/余弦函数，将信号分解为谐波分量（频率与振幅），使单基元能编码复杂的高频外观模式。
- **延迟着色减少推理**：将谐波编码后的特征沿射线alpha混合，最后每像素仅需一次MLP解码为RGB。相比每基元一次网络查询的方案，推理次数从O(基元数)降至O(像素数)，在密集基元场景下优势显著。

这一设计在严格控制变量的实验中展现出显著优势：在相同框架、基元数、训练迭代数和每基元外观参数量下，NHT在MipNeRF360数据集上达到28.46 PSNR，比SV模型（28.15）提升0.31 dB，比SH模型（27.93）提升0.53 dB（Table 2）。尤其值得注意的是，在低基元数量区间（≤100k），NHT的PSNR领先超过2 dB（Fig. 5），直接验证了单基元表达力的显著增强——这正是几何与外观解耦带来的核心收益。

## 核心创新

Neural Harmonic Textures (NHT) 的核心创新在于对传统基元表示中**几何与外观强耦合**这一瓶颈的系统性解耦。传统方法（如3DGS）中，每个基元的外观由低阶球谐函数（SH）独立计算，单基元表达能力有限：建模高频细节和复杂视角相关效果（如镜面高光）时，必须大量增加基元数量，导致内存膨胀和渲染速度下降。NHT 通过三个相互关联的机制设计（changed slots）从根本上改变了这一范式。

### 1. 基元绑定的隐式特征嵌入：从“每基元独立着色”到“局部特征锚定”

传统方法（SH、Spherical Voronoi）在每个基元上直接预计算颜色，外观与几何空间强绑定，无法表达空间变化的外观信号。NHT 为每个基元构建一个虚拟包围四面体（或三角形，针对2D基元），在其顶点附加可学习的 $N$ 维特征向量。当射线与基元相交时，在交点处通过重心插值获得局部特征 $\mathbf{f}_i$。这一设计将基元从“颜色发射器”转变为“局部位置编码器”——特征向量随基元移动，天然支持运动、变形和编辑，同时为后续的谐波分解提供了空间变化的信号源（Sec. 4.1, Fig. 3）。

### 2. 谐波编码：将特征转化为频率-振幅分解

这是 NHT 最具区分性的机制。传统方法在 alpha 混合前直接使用颜色值，而 NHT 对插值后的特征 $\mathbf{f}_i$ 逐通道施加正弦和余弦函数，将其转化为谐波分量：

$$\text{sin}(\mathbf{f}_i),\ \text{cos}(\mathbf{f}_i)$$

这一操作将特征信号分解为不同频率的正交基，基元的不透明度 $\alpha_i$ 自然成为各频率分量的振幅调制因子（Fig. 2）。与球谐函数仅在方向域进行低频展开不同，NHT 的谐波编码在**空间-特征联合域**进行分解，单基元即可编码远丰富于 SH 的高频信号。消融实验证实，正弦+余弦组合在所有编码函数中表现最优（Table 4），单独余弦或 ReLU 均导致 PSNR 下降。

### 3. 延迟着色与轻量 MLP 解码：从“每基元推理”到“每像素单次推理”

传统基元方法中，每个基元需独立执行一次 SH 查询或 MLP 推理，计算量与基元数线性增长。NHT 将推理推迟到 alpha 混合之后：谐波编码后的特征沿射线按标准体积渲染方程累加，最终每像素仅需一次轻量 MLP 解码为 RGB：

$$\mathbf{c} = \text{MLP}_\theta \left( \sum_{i \in \mathcal{G}} \alpha_i T_i [\text{sin}(\mathbf{f}_i)],\ k \cdot \text{SH}_2(\mathbf{d}) \right)$$

这一延迟着色策略将神经网络推理次数从“每基元”降至“每像素”，在保持实时渲染的同时，使外观模型容量大幅提升。消融表明，128×2 隐藏层 MLP 已达到 PSNR 28.47，更大模型（128×4）仅提升 0.03 dB，证明轻量解码器已足够（Table 17）。

### 4. 基元无关性：统一的外观增强框架

NHT 的外观表示与具体基元类型解耦。特征载体仅需随基元形状调整（3D 高斯用四面体，2D 高斯/三角形用三角形），核心的谐波编码和延迟解码流程保持不变。Table 3 验证了 NHT 在 3D 高斯、2D 高斯和三角形喷洒上的通用性，均带来一致的性能提升。

### 创新机制间的因果链路

这三个 changed slots 构成一条完整的因果链：**特征嵌入**将基元转化为局部信号源 → **谐波编码**将信号分解为频率-振幅表示，突破单基元表达能力瓶颈 → **延迟 MLP 解码**在图像空间高效合成最终颜色，实现几何与外观的彻底解耦。控制变量实验（Table 2）在相同框架、相同基元数、相同参数量下，NHT 比 SV 提升 0.31–0.61 dB PSNR，比 SH 提升 0.53–0.70 dB，直接验证了外观模型本身带来的增益，排除了实现细节干扰。

## 整体框架

Neural Harmonic Textures (NHT) 提出了一套与基元类型无关的外观建模框架，核心思路是将几何与外观解耦，通过为每个基元附加可学习的局部特征向量，并在图像空间进行延迟神经解码，从而在不牺牲实时性能的前提下大幅提升单基元的表达能力。

**总体流程**遵循四个顺序模块：

1.  **基元绑定特征嵌入 (Primitive-bound Feature Embedding)**：为每个基元构建一个虚拟包围结构（3D高斯对应四面体，2D高斯或三角形对应三角形），在包围体的顶点上锚定可学习的 $N$ 维特征向量。当射线穿过基元时，在射线-基元最大响应交点处对顶点特征进行重心插值，得到该交点的局部特征向量 $\mathbf{f}_i$。这些特征向量随基元移动，天然支持运动与变形。

2.  **谐波编码 (Harmonic Encoding)**：对插值后的特征向量 $\mathbf{f}_i$ 逐通道应用正弦和余弦函数，将其转化为频率分量——即“谐波纹理”。这一步骤将特征分解为不同频率的信号，为后续混合提供丰富的基函数。

3.  **谐波 Alpha 混合 (Alpha Compositing of Harmonics)**：沿射线按传统体积渲染方式对正弦激活后的特征进行 alpha 累加：
    $$\mathbf{c} = \mathrm{MLP}_\theta \left( \sum_{i \in \mathcal{G}} \alpha_i T_i [ \mathrm{sin}(\mathbf{f}_i) ], \; k \cdot \mathrm{SH}_2(\mathbf{d}) \right)$$
    其中 $\alpha_i$ 为基元不透明度，$T_i$ 为累积透射率，$\mathbf{d}$ 为视角方向。基元的不透明度在此充当振幅，控制各频率分量的贡献强度。

4.  **延迟 MLP 解码器 (Deferred MLP Decoder)**：将沿射线累加的谐波特征与视角方向的二阶球谐编码拼接，通过一个轻量 MLP（典型配置为 $128 \times 3$ 隐藏层）一次性解码为像素 RGB 颜色。与逐基元计算颜色再混合的传统方案不同，NHT 每像素仅需一次 MLP 推理，显著降低了计算开销。

**输入输出流**：输入为相机射线与场景基元集合，输出为对应像素的颜色值。训练时采用 L1 与 D-SSIM 的组合损失，辅以基元不透明度和尺度的正则项，并对 MLP 权重施加指数移动平均 (EMA) 以提升鲁棒性。

**关键设计决策**：框架对基元类型无特化要求——3D高斯、2D高斯、三角形面片均可无缝接入，仅需调整特征载体（四面体/三角形）的几何定义。这一通用性在 Table 3 中得到了验证。

<figures>
Figure 3: Illustrating our method in 2D. Each primitive is bounded by an ellipsoid in world space, which becomes a sphere in whitened canonical space (a). Considering a virtual bounding tetrahedron in this canonical space, we attach one N-dimensional feature vector
</figures>

### 补充图表

![[assets/figures/papers/paper_list_l69_https_arxiv_org_abs_2604_01204/figures/001_Figure_1.jpg]]
*Figure 1: Neural Harmonic Textures for novel view synthesis. We attach learnable feature vectors (right) to the virtual vertices of bounding tetrahedra encapsulating each primitive (center). After harmonic encoding and accumulation along the ray, a small neural network decodes the resulting signal into RGB color in a deferred manner (left). Source code and further results are available at https://research.nvidia.com/labs/ sil/projects/neural-harmonic-textures/*

## 核心模块与公式推导

Neural Harmonic Textures (NHT) 的核心设计思路是：将基元从“颜色载体”升级为“局部谐波信号发生器”，通过**基元绑定特征嵌入 → 谐波编码 → Alpha混合累积 → 延迟MLP解码**四个模块，在保持基元表示结构优势的同时，大幅提升单基元的表达能力。

### 4.1 基元绑定特征嵌入

传统基元方法（如3DGS）中，外观与几何强耦合——每个基元直接存储球谐系数，基元本身即是颜色的唯一来源。NHT 的关键突破在于**解耦几何与外观**：基元仅负责提供空间位置和不透明度，而外观信息由附加在基元虚拟支架上的可学习特征向量承载。

具体而言，为每个3D高斯基元构建一个包围四面体（在2D情况下为包围三角形）。四面体的顶点锚定在基元的“白化正则空间”中——即通过协方差矩阵 $\boldsymbol{\Sigma}$ 变换后，基元的空间响应函数变为：

$$\rho ( \mathbf{x} ) = \exp \left( -\frac{1}{2} (\mathbf{x} - \boldsymbol{\mu})^\mathsf{T} \boldsymbol{\Sigma}^{-1} (\mathbf{x} - \boldsymbol{\mu}) \right)$$

在该正则空间内，基元呈球对称分布。四面体顶点上各附加一个 $N$ 维可学习特征向量。当射线与基元相交时，在射线-基元交点处（遵循3DGUT的最大响应点采样策略），通过**重心插值**获得该交点的特征向量 $\mathbf{f}_i$。

这一设计的核心优势在于：
- **空间变化外观**：同一基元的不同空间位置可产生不同特征，突破了传统SH模型仅依赖视角方向的限制。
- **基元类型无关**：四面体可替换为三角形（用于2D高斯或三角面片），特征锚定机制与基元类型解耦。

### 4.2 谐波编码

插值得到的特征向量 $\mathbf{f}_i$ 并非直接用于颜色计算，而是先经过**谐波编码**——对每个特征维度分别应用正弦和余弦函数：

$$\text{编码后特征} = [\sin(\mathbf{f}_i), \cos(\mathbf{f}_i)]$$

这一操作的物理直觉在于：正弦/余弦函数将特征值映射为不同频率的谐波分量。原始特征向量可理解为“频率”，编码后的正弦/余弦值即为该频率下的振荡信号。基元的不透明度 $\alpha_i$ 则充当该谐波分量的**振幅**。

消融实验（Table 4）验证了这一设计的必要性：正弦+余弦组合编码在MipNeRF360上达到PSNR 28.46，显著优于单独余弦（PSNR 28.11）或ReLU激活（PSNR 27.85），证明双通道周期编码能够更完整地保留信号的频率信息。

### 4.3 Alpha混合与延迟神经解码

传统渲染管线中，每个基元独立计算颜色后进行Alpha混合。NHT 将颜色解码推迟到混合之后——即**延迟着色**：

$$\mathbf{c} = \mathrm{MLP}_\theta \left( \sum_{i \in \mathcal{G}} \alpha_i T_i [ \mathrm{sin}(\mathbf{f}_i) ], \; k \cdot \mathrm{SH}_2(\mathbf{d}) \right)$$

其中：
- $\alpha_i T_i [\sin(\mathbf{f}_i)]$：沿射线对正弦激活后的谐波特征进行Alpha混合（$\cos$ 通道同理），$T_i = \prod_{j=1}^{i-1} (1 - \alpha_j)$ 为累积透射率。
- $\mathrm{SH}_2(\mathbf{d})$：对视角方向 $\mathbf{d}$ 进行2阶球谐编码，注入视角相关信息。
- $\mathrm{MLP}_\theta$：小型MLP解码器（典型配置为128宽×3隐藏层），将混合后的谐波信号与视角编码拼接后一次解码为RGB颜色。

这一设计的核心优势在于：
- **推理效率**：无论场景包含多少基元，每像素仅需**一次MLP推理**，而非逐基元调用。这保证了实时渲染性能（140-240 FPS，Table 2）。
- **表达能力**：谐波混合过程本质上是基元间信号的频域叠加，MLP解码器在图像空间完成从谐波到颜色的非线性映射，能够建模复杂的高频细节和视角相关效果。

### 4.4 训练目标

总损失函数为多目标加权组合：

$$\mathcal{L} = (1 - \lambda) \mathcal{L}_{\mathrm{L}_1} + \lambda \mathcal{L}_{\mathrm{D-SSIM}} + \lambda_\alpha \mathcal{R}_\alpha + \lambda_s \mathcal{R}_s$$

其中 $\mathcal{R}_\alpha = \frac{1}{P} \sum_{i=1}^{P} \alpha_i$ 为不透明度正则项（抑制冗余基元），$\mathcal{R}_s = \frac{1}{P} \sum_{i=1}^{P} \lVert \mathbf{s}_i \rVert_1$ 为尺度正则项（防止基元过度膨胀）。消融实验（Table 14）表明，移除不透明度正则化导致PSNR下降至27.85，验证了其对质量的关键作用。

### 补充图表

![[assets/figures/papers/paper_list_l69_https_arxiv_org_abs_2604_01204/figures/002_Figure_2.jpg]]
*Figure 2: Neural Harmonic Textures applied to novel-view synthesis. We virtually attach feature vectors fi to the vertices of tetrahedra inscribing the Gaussian primitives3. Following 3DGUT [65], we evaluate the point along the ray where the projected Gaussian has maximum response. We barycentrically interpolate vertex features at that point, and encode them with sine and cosine functions into different channels. These are then alpha blended along the rest of the ray, until the resulting sum of harmonics is decoded by a shallow MLP in a single image-space pass*

![[assets/figures/papers/paper_list_l69_https_arxiv_org_abs_2604_01204/figures/003_Figure_3.jpg]]
*Figure 3: Illustrating our method in 2D. Each primitive is bounded by an ellipsoid in world space, which becomes a sphere in whitened canonical space (a). Considering a virtual bounding tetrahedron in this canonical space, we attach one N-dimensional feature vector*

## 实验与分析

### 核心性能对比

在MipNeRF360、Tanks & Temples和Deep Blending三个标准数据集上，NHT在所有指标上均优于现有实时与离线方法。Table 1展示了全面对比结果：NHT在MipNeRF360上达到PSNR 28.74，Tanks & Temples上25.68，Deep Blending上30.94，均显著超越先前最佳方法。在LPIPS指标上，NHT同样取得最优（MipNeRF360: 0.216，Tanks & Temples: 0.141）。值得注意的是，该方法在保持实时渲染性能的同时，超越了包括**ZipNeRF**、**Mip-NeRF 360**等离线神经场方法，以及**3DGS-MCMC**、**2DGS**等先进基元方法。

### 严格控制变量实验

为隔离外观模型的影响，作者在统一框架（gsplat）下实现了四种外观模型，严格控制基元数量（1M）、训练迭代数（30k）、每基元外观参数量（48）及所有超参数。Table 2的结果表明，NHT在所有基准上一致优于球谐（SH）和球面Voronoi（SV）模型：

- **MipNeRF360**: NHT PSNR 28.46，比SV（28.15）高0.31 dB，比SH（27.93）高0.53 dB；LPIPS 0.232，优于SV的0.248。
- **Tanks & Temples**: NHT PSNR 24.79，领先SV 0.61 dB。
- **Deep Blending**: NHT PSNR 30.88，领先SV 0.59 dB。

关键的是，NHT在取得质量提升的同时未牺牲实时性能——在MipNeRF360上FPS达140，与SH和SV模型相当。

### 低基元数量区间的显著优势

Figure 5揭示了NHT的标度特性：在所有基元数量下，NHT均优于3DGS和3DGUT，且在低基元区间（≤100k）优势尤为突出，PSNR领先幅度超过2 dB。这直接验证了核心洞察——通过谐波编码和延迟着色MLP，单基元的表达能力得到根本性增强，即使基元数量大幅减少，仍能保持高保真重建。

### 特征编码函数消融

Table 4消融了特征编码函数的选择。正弦+余弦组合编码在所有方案中表现最佳（PSNR 28.46, LPIPS 0.232），优于单独使用余弦或ReLU激活。这证实了谐波分解的核心设计——正弦和余弦共同作用，将特征向量转化为完整的频率分量（振幅与相位），使后续alpha混合能够保留更丰富的外观信息。

### 特征维度与MLP架构消融

每基元特征维度从4增加到64时，PSNR从27.18提升至28.48，但帧率从165 FPS降至105 FPS，呈现典型的质量-速度权衡（Table 16）。MLP架构方面，128×2隐藏层已基本饱和（PSNR 28.47），增大到128×4仅带来0.03 dB的边际提升（Table 17），表明轻量解码器足以有效利用谐波特征。

![[assets/figures/papers/paper_list_l69_https_arxiv_org_abs_2604_01204/figures/024_Table_16.jpg]]
*Table 16: Ablating feature count N. Measured on an RTXA6000 Ada*

![[assets/figures/papers/paper_list_l69_https_arxiv_org_abs_2604_01204/figures/025_Table_17.jpg]]
*Table 17: Ablating MLP architecture (layer width × hidden layer count). Measured on an RTXA6000 Ada*

### 训练策略消融

Table 14显示了训练组件的重要性：
- 移除不透明度正则化导致PSNR降至27.85，表明该正则化对抑制冗余基元、提升渲染效率和质量至关重要。
- 移除方向编码（视角球谐输入）使PSNR降至28.11，说明视角相关外观建模仍不可或缺。
- 尺度正则化对重建质量影响较小，但能改善渲染速度。

### 基元类型通用性

Table 3验证了NHT与不同基元类型的兼容性。将NHT应用于3D高斯、2D高斯和三角形喷洒时，均能带来一致的性能提升，证明特征锚定和编码框架的通用性。三角形喷洒的集成仅为概念验证，未进行广泛优化，其性能仍有提升空间。

### 后训练压缩

Table 18展示了压缩效果：采用int8特征量化、int16位置量化、fp16 MLP推理和Zstandard压缩后，可实现约3倍存储压缩，PSNR下降不足0.05 dB，验证了谐波特征对量化的鲁棒性。

### 失败模式与局限

基于MLP的外观模型收敛速度慢于SH模型，需要更多训练迭代才能达到同等水平。对于高视差室内场景，方法依赖中心相机光线正则化，可能限制极端视角变化下的泛化能力。动态场景虽在理论上受特征锚定支持，但缺乏连续变形的定量验证。更激进的量化（如int4）可能导致显著质量损失，需进一步研究。

### 补充图表

![[assets/figures/papers/paper_list_l69_https_arxiv_org_abs_2604_01204/figures/005_Table_1.jpg]]
*Table 1: Comparison on MipNeRF360 [1], Tanks & Temples [27], and Deep Blending [18], on Neural Field-style methods, primitive-based methods, and mixed neural field/primitive-based methods. For the MipNeRF360 datasets, we disable gsplat’s default downscaling and instead train and evaluate directly on the provided JPEGcompressed reference images following prior work. We measure the effect in Tab. 9. For our method, we use 64 features per primitive (16 per vertex), with a 128-wide × 3 hidden layers MLP, which results in a roughly similar number of total parameters as previous primitive-based approaches on average. For indoor scenes, which typically span a smaller spatial volume, we use 2M primitives, w...*

![[assets/figures/papers/paper_list_l69_https_arxiv_org_abs_2604_01204/figures/007_Table_2.jpg]]
*Table 2: Quantitative results of our approach and baselines on the MipNeRF360 [1], Tanks & Temples [27], and Deep Blending [18] datasets, comparing our method against Spherical Voronoi [9] (SV) and regular SH models. We isolate the effect of our approach by implementing all methods in the same framework (gsplat [71] with its default downsampling), using the same number of primitives (1M), training for the same number of iterations (30k), allocating the same number of parameters per primitive for appearance (48) and using the same hyperparameters for all scenes. Our method uses a 128×3 hidden MLP. We improve reconstruction quality while still managing real-time performance (measured ona an RTX A6000...*

![[assets/figures/papers/paper_list_l69_https_arxiv_org_abs_2604_01204/figures/008_Figure_5.jpg]]
*Figure 5: Our method outperforms 3DGS and 3DGUT at all primitive counts. The improvement is particularly pronounced in the lowprimitive regime (≤ 100k), with deltas upwards of 2dB of PSNR*

![[assets/figures/papers/paper_list_l69_https_arxiv_org_abs_2604_01204/figures/009_Figure_6.jpg]]
*Figure 6: Comparison between our and previous works on radiance field reconstruction on scenes from MipNeRF360 [1], Tanks and Temples [27]. Our method models high frequency detail and view dependent effects to a higher degree than previous works*

![[assets/figures/papers/paper_list_l69_https_arxiv_org_abs_2604_01204/figures/010_Table_4.jpg]]
*Table 4: Ablating the choice of feature encoding function (MipNeRF360 dataset)*

![[assets/figures/papers/paper_list_l69_https_arxiv_org_abs_2604_01204/figures/022_Table_14.jpg]]
*Table 14: Ablation study on training strategies. The rows are not additive, i.e. we only test one strategy at a time. All experiments on the MipNeRF360 dataset, using 64 features per primitive and a 128×3 MLP. Note that the scale regularization (F) does not significantly affect reconstruction quality, but does improve render time*

![[assets/figures/papers/paper_list_l69_https_arxiv_org_abs_2604_01204/figures/026_Table_18.jpg]]
*Table 18: Impact of post-training compression on NHT at 100×. Averages over 15 images. Baseline: uncompressed fp32 features/parameters + fp16 MLP weights. int8 features: uniform 8-bit quantization with per-channel scale/offset. int16 positions: fixedpoint uint16 vertex positions. int8+int16+fp16 : combined quantization (features int8, positions int16, MLP fp16). + Zstandard/Brotli: entropy coding on the serialized payload*

## 方法谱系与知识库定位

### 1. 基元重建谱系中的定位

NHT 处于**基元式神经渲染**（primitive-based neural rendering）与**神经场**（neural field）两股技术路线的交汇点上。其核心贡献在于打破传统基元方法中“几何与外观强耦合”的瓶颈——该瓶颈迫使 3DGS 等经典方法以低阶球谐函数（SH）作为逐基元外观模型，单个基元的表达能力因此受限，建模高频细节和复杂视角相关效果时必须大量增加基元数量，导致内存膨胀和渲染速度下降。

从谱系上看，NHT 的直系前驱包括：

- **3DGS**（Kerbl et al., SIGGRAPH 2023）：建立了基于 3D 高斯基元的喷洒渲染框架，使用球谐函数（SH）建模视角相关外观。NHT 继承了其基元化喷洒管线，但将外观模型从 SH 替换为谐波纹理。
- **3DGUT**（Hamdi et al., ECCV 2024）：将 3DGS 扩展为基于均匀网格化的基元分布，并提出在射线-基元最大响应点处评估外观。NHT 直接沿用了这一“最大响应点插值”策略，并在此处锚定特征向量。
- **Spherical Voronoi**（SV）：采用球面 Voronoi 函数作为视角相关外观模型，试图突破 SH 的表达能力上限。NHT 在控制变量实验中将其作为直接对比基线，证明了谐波编码+延迟着色的方案在同等参数量下具有一致的性能优势（Table 2）。

在更广的谱系中，NHT 与以下方法形成对比或互补关系：

- **神经场方法**（Instant NGP、Mip-NeRF 360、ZipNeRF）：这些方法依赖全局或网格化的特征编码器，通过密集的 MLP 查询沿射线累积颜色。NHT 将类似的特征编码思想“局部化”到每个基元的虚拟支架上，从而保留了基元方法的实时渲染优势和显式几何结构，同时获得了接近神经场的表达能力。
- **其他基元类型方法**（2DGS、Triangle Splatting）：NHT 在 Table 3 中展示了其外观模型可与 2D 高斯圆盘、三角形面片等不同基元类型无缝集成，仅需改变特征载体（四面体→三角形），证明了方法的基元无关性（primitive-agnostic）。

### 2. 方法适用边界

**适用场景**：
- 静态场景的新视角合成，包括室内（Deep Blending）、室外大范围（MipNeRF360）和中等规模物体/场景（Tanks & Temples）。
- 对单基元表达能力要求高的场景——在低基元数量区间（≤100k），NHT 的 PSNR 领先幅度可达 2dB 以上（Fig. 5），表明其在内存或计算预算受限时具有显著优势。
- 需要实时渲染的应用：NHT 在 1M 基元配置下仍保持 140–240 FPS 的实时性能（Table 2），且延迟着色架构使每像素仅需一次 MLP 推理。

**不适用或需额外适配的场景**：
- **动态场景与 4D 重建**：虽然特征向量锚定在基元的虚拟支架上，理论上支持基元运动、变形和编辑（Sec. 4.1），但论文未提供连续变形或动态场景的定量验证，这一能力目前仅为概念性声明，需要进一步实验确认。
- **极端视角变化**：论文提到对于高视差室内场景，需编码中心相机光线而非逐条光线作为正则化（limitations），这可能限制在极端视角变化下的泛化能力。
- **极致压缩需求**：后训练压缩仅探索到 int8 量化，约 3 倍压缩率下质量损失极小（PSNR 下降 <0.05 dB，Table 18）。更激进的压缩（如 int4）可能带来显著质量损失，尚未验证。

### 3. 局限与开放问题

**可验证的局限**：
1. **收敛速度**：基于 MLP 的外观模型收敛速度可能慢于基于 SH 的模型，需要更多训练迭代才能达到相同水平（limitations）。
2. **Triangle Splatting 集成不成熟**：该集成仅为概念验证，未进行广泛优化，性能未达到最佳状态（Table 3）。
3. **正则化设计的场景依赖性**：中心光线正则化策略在室内高视差场景中引入，其通用性尚未在更广泛的场景分布上验证。

**开放问题**：
1. **层次细节（LOD）自动提取**：能否从谐波分解中自动提取层次细节，实现内存-质量的自适应调节？谐波编码天然将信号分解为不同频率分量，这为构建频率驱动的 LOD 机制提供了理论可能性。
2. **高斯核函数的可替代性**：能否完全去除高斯核函数，以换取更极致的渲染性能，同时保持足够的信号表达能力？当前方法仍依赖高斯核函数定义基元的空间响应和 alpha 值。
3. **动态场景与实时编辑潜力**：特征锚定在基元支架上的设计理论上支持运动与变形，但该能力在动态场景、4D 重建以及实时变形编辑方面的实际表现如何，是重要的后续研究方向。
4. **多模态扩展**：论文提到该方法“自然扩展到高维信号”，并暗示可联合建模颜色与语义特征（introduction）。特征编码框架是否可扩展到更高维度的传感器信号（如时间、光谱），形成统一的多模态基元表示，是一个值得探索的方向。

### 4. 与知识库的锚定关系

NHT 的核心技术贡献可映射到以下知识节点：

| 知识节点 | NHT 的贡献 | 证据锚点 |
|:---|:---|:---|
| 基元外观解耦 | 将外观从几何中解耦，通过虚拟支架上的可学习特征向量实现 | Sec. 4.1, Fig. 3 |
| 谐波编码 | 使用正弦/余弦函数将特征转化为频率分量，提升高频表达能力 | Sec. 4.2, Table 4 |
| 延迟着色 | 在 alpha 混合后仅需一次 MLP 解码为像素颜色，大幅减少推理次数 | Sec. 4.3, Eq. (3) |
| 基元无关性 | 可与 3D 高斯、2D 高斯、三角形等多种基元集成 | Table 3, Sec. 5.2 |
| 压缩友好性 | int8 特征量化 + int16 位置 + fp16 MLP + Zstandard 实现约 3 倍压缩 | Table 18 |

在实验知识层面，NHT 在 MipNeRF360、Tanks & Temples、Deep Blending 三个标准数据集上均达到 state-of-the-art 性能（Table 1），且控制变量实验（Table 2）严格排除了框架实现、基元数、训练迭代数、参数量等混杂因素的干扰，证据可信度高。消融实验覆盖了编码函数选择（Table 4）、特征维度（Table 16）、MLP 架构（Table 17）、训练策略（Table 14）和压缩方案（Table 18），为后续改进提供了清晰的因果调控杠杆。

## 原文 PDF

![[paperPDFs/arxiv_2026/Neural_Harmonic_Textures_for_High_Quality_Primitive_Based_Neural_Reconstruction.pdf]]