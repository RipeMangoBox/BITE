---
title: "Neural Geometric Level of Detail: Real-time Rendering with Implicit 3D Surfaces"
type: paper
paper_level: A
venue: CVPR
year: 2021
pdf_ref: paperPDFs/CVPR_2021/Neural_Geometric_Level_of_Detail_Real_time_Rendering_with_Implicit_3D_Surfaces.pdf
code_link: null
project_link: https://research.nvidia.com/labs/toronto-ai/nglod/
aliases:
- NGLDNL
- NGLDRTRI3S
tags:
- CVPR_2021
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
core_operator: "将 SDF 编码从单个大型 MLP 转为稀疏体素八叉树（SVO）存储局部特征，配合极浅 MLP 解码器，将主要计算负载转移到高效的 SVO 遍历与三线性插值上，同时引入连续 LOD 进一步加速。"
primary_logic: "通过稀疏八叉树分层存储局部形状特征，并由对应的小型 MLP 仅在 LOD 选定的局部区域解码距离，既能高质量重建复杂几何，又能将渲染速度提升 2–3 个数量级，首次实现神经 SDF 的实时渲染。"
claims:
- "Our representation is 2–3 orders of magnitude more efficient in terms of rendering speed compared to previous works."
- "Sparse frametimes are more than 100× faster than DeepSDF while achieving better visual quality with less parameters."
- "Only our architecture can capture the high-frequency details of complex analytic SDFs (Oldcar, Mandelbulb) while baselines fail."
- "Our architecture starting from LOD 3 performs much better in reconstruction quality despite having much lower inference parameters (4737 vs DeepSDF’s 1.8M)."
---

# Neural Geometric Level of Detail: Real-time Rendering with Implicit 3D Surfaces

> [!tip] 核心洞察
> 通过稀疏八叉树分层存储局部形状特征，并由对应的小型 MLP 仅在 LOD 选定的局部区域解码距离，既能高质量重建复杂几何，又能将渲染速度提升 2–3 个数量级，首次实现神经 SDF 的实时渲染。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 神经几何细节层次：隐式3D曲面的实时渲染 |
| 英文题名 | Neural Geometric Level of Detail: Real-time Rendering with Implicit 3D Surfaces |
| 会议/期刊 | CVPR 2021 |
| Links | [paper](https://arxiv.org/abs/2101.10994) · [Project](https://nv-tlabs.github.io/nglod) · [Project](https://research.nvidia.com/labs/toronto-ai/nglod/) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction |
| Method | Neural Geometric Level of Detail (NG-LOD) |
| Dataset | ShapeNet150, Thingi32, TurboSquid16, Rendering Speed (TurboSquid V Mech 1920x1080) |

> [!tip] 效果简介
> - ShapeNet150 上，gIoU (%) 为 91.6 (Ours/LOD4)，对比 86.9 (DeepSDF)，变化 +4.7。
> - Thingi32 上，Chamfer-L1 (×10^3) 为 0.0271 (Ours/LOD5)，对比 0.0533 (DeepSDF)，变化 -0.0262。
> - TurboSquid16 上，Normal-L2 为 0.166 (Ours/LOD5)，对比 0.180 (DeepSDF)，变化 -0.014。

## 概要

**问题瓶颈**：传统神经隐式曲面采用单一大型 MLP（如 DeepSDF 约 180 万参数）编码完整形状的符号距离函数（SDF），每次距离查询需数百万次运算；在 sphere tracing 渲染管线中，每像素需上百次查询，总计算成本高达数百亿次操作，导致无法实时渲染。

**核心思路**：将 SDF 的编码方式从“全局大网络”转变为“稀疏体素八叉树（SVO）+ 极浅 MLP 解码器”。八叉树分层存储局部几何特征，查询时通过三线性插值与跨层求和获得紧凑特征向量，再由仅含 4737 个参数的小型 MLP 解码为有符号距离。同时引入多级离散细节层次（LOD）及连续 LOD 插值，使渲染精度与开销可按需调节。

**方法定位**：该方法属于**基于稀疏体素特征的神经隐式曲面**，在渲染速度上比 DeepSDF 快两个数量级以上，首次实现神经 SDF 的实时渲染。其架构可视为将 NSVF 的体素特征思想与多级 LOD 策略融合，并通过稀疏自适应射线步进替代标准 sphere tracing，显著降低无效查询。

**主要结果**：
- **重建质量**：在 ShapeNet150 上 gIoU 达 91.6%（DeepSDF 86.9%），Thingi32 上 Chamfer-L1 降至 0.0271（DeepSDF 0.0533），TurboSquid16 上 Normal-L2 降至 0.166，且推理参数量仅为 DeepSDF 的约 1/380。
- **渲染速度**：在 TurboSquid V Mech 1920×1080 分辨率下，稀疏渲染帧耗时 91 ms，而 DeepSDF 需 1693 ms，加速约 18.6 倍；相比 NeRF 加速超 500 倍，相比 NSVF 加速约 50 倍。
- **困难场景**：在高度非度量的 Oldcar 与递归分形 Mandelbulb 等解析 SDF 上，仅该方法能成功重建，DeepSDF、FFN、SIREN 等基线均失败。

**局限与开放问题**：该方法依赖有界体素八叉树，难以扩展到极大场景或极薄几何体；无法直接与传统骨骼动画或变形技术结合。未来方向包括解码器缓存/融合以进一步提升性能，以及向大规模多物体动态场景的扩展。

### 隐式神经表示与实时渲染的张力

三维几何的隐式神经表示，尤其是以符号距离函数（SDF）$f(\mathbf{x})$ 的零等值面定义表面

$$S = \big \{ \mathbf { x } \in \mathbb { R } ^ { 3 } \big | f ( \mathbf { x } ) = 0 \big \}$$

在过去数年中取得了显著进展。这类表示天然适合处理复杂拓扑、连续表面和自适应分辨率，且可通过 sphere tracing 进行可微渲染。然而，将神经 SDF 推向实时渲染面临一个根本性瓶颈：**计算效率**。

### 核心瓶颈：全局 MLP 的巨大计算开销

以 **DeepSDF**（Park et al., CVPR 2019）为代表的经典方法，使用一个大型全局 MLP（约 180 万参数）对整个形状进行编码。每次距离查询需要经过完整的网络前向传播，涉及数百万次浮点运算。在 sphere tracing 渲染管线中，每条射线通常需要上百次距离查询才能收敛到表面——这意味着渲染一帧 1920×1080 的画面，总计算量可达数百亿次操作，帧耗时超过 1.5 秒（Table 3），距离实时渲染（< 33 ms）相差近两个数量级。

这一瓶颈并非 DeepSDF 独有。**Fourier Feature Networks**（FFN, Tancik et al., NeurIPS 2020）和 **SIREN**（Sitzmann et al., NeurIPS 2020）虽然通过傅里叶位置编码或周期激活函数增强了高频细节捕捉能力，但本质上仍依赖大型 MLP 进行全局解码，计算开销并未显著降低。**Neural Implicits**（Davies et al., arXiv 2020）将小 MLP 过拟合到单个形状，虽减少了参数量，但缺乏多分辨率结构和空间稀疏性，难以应对复杂几何。

### 方法缺口：缺乏有效的空间局部化与多分辨率机制

上述方法的共同缺陷在于：**将完整形状的知识压缩进一个全局 MLP 的权重中**。这导致三个直接后果：

1. **计算冗余**：即使查询远离表面的空间点，仍需执行完整的网络推理。
2. **容量瓶颈**：单个 MLP 的表达能力有限，难以同时捕捉全局粗结构和局部高频细节。实验表明，DeepSDF、FFN、SIREN 在复杂解析 SDF（如 Oldcar 的非度量距离场、Mandelbulb 的递归分形结构）上均告失败（Figure 6）。
3. **缺乏细节层次（LOD）**：渲染时无法根据视距或屏幕空间占用动态调整几何精度，所有查询使用相同分辨率的表示。

### 本文动机：稀疏层次特征实现实时神经渲染

本文的核心动机在于打破“神经 SDF = 大型全局 MLP”的范式。通过将 SDF 编码从单一 MLP 权重中解耦，转而使用**稀疏体素八叉树（SVO）存储局部几何特征**，并配合**极浅 MLP 解码器**（仅 4737 个推理参数），将主要计算负载从网络推理转移到高效的八叉树遍历与三线性插值上。同时引入多重离散 LOD 与连续 LOD 插值，使渲染时可根据需要自适应选择几何精度。这一设计旨在实现 **2–3 个数量级的渲染加速**，首次将神经 SDF 的渲染性能推至实时交互范畴。

## 核心方法与创新机理

### 1. 从全局编码到稀疏八叉树特征体积

传统神经 SDF 方法（如 **DeepSDF**（Park et al., CVPR 2019）、**FFN**（Tancik et al., NeurIPS 2020）、**SIREN**（Sitzmann et al., NeurIPS 2020））使用单一的大型 MLP 编码完整形状，每次距离查询需数百万次运算，在 sphere tracing 中每像素需上百次查询，总计算成本高达数百亿次操作，无法实时渲染。

NG-LOD 的核心架构创新是将 SDF 编码从一个全局大型 MLP 转为**稀疏体素八叉树（SVO）存储的局部特征向量**，配合极浅的 MLP 解码器。这一转变的因果机制在于：将主要计算负载从昂贵的神经网络推理转移到高效的 SVO 遍历与三线性插值上，使推理参数量从 DeepSDF 的约 1.8M 骤降至固定的 4737 个参数（Table 1），同时保持甚至提升了重建质量。

### 2. 多层次细节（LOD）的连续表示

NG-LOD 引入了传统神经隐式表示所不具备的**多层级离散 LOD 与连续 LOD 插值**机制。SVO 的每一层对应一个离散 LOD，层内体素角点存储可学习的特征向量。对于给定查询点 $\mathbf{x}$ 和 LOD $L$，系统通过三线性插值获取各层对应体素的特征并求和，得到特征向量 $\mathbf{z}(\mathbf{x}; L, \mathcal{Z})$，再传入小型 MLP 解码器输出 signed distance：

$$\widehat{d}_L = f_{\boldsymbol{\theta}_L}\big([\mathbf{x}, \mathbf{z}(\mathbf{x}; L, \mathcal{Z})]\big)$$

进一步地，通过在相邻两个离散 LOD 的距离值之间进行线性插值，实现**连续 LOD 的平滑过渡**：

$$\widehat{d}_{\widetilde{L}} = (1 - \alpha) \widehat{d}_{L^*} + \alpha \widehat{d}_{L^* + 1}$$

这一设计使渲染时可根据相机距离动态调整几何细节层次，在保证视觉质量的同时大幅降低计算开销（Figure 1）。

### 3. 稀疏自适应射线步进渲染算法

传统 sphere tracing 在每一步都需查询完整 MLP，NG-LOD 提出了**稀疏自适应射线步进**策略（Figure 4, Algorithm 1）：当查询点位于体素内部时，执行三线性插值与 MLP 解码计算 sphere tracing 步长；当查询点位于体素外部时，利用 ray-AABB 相交直接跳至下一个体素，避免无效的 SDF 查询。这一算法与 SVO 的稀疏结构深度耦合，是实现实时渲染的关键使能技术。

### 4. 联合多层级训练损失

NG-LOD 的训练损失函数联合优化所有 LOD 层级：

$$J(\theta, \mathcal{Z}) = \mathbb{E}_{\mathbf{x}, d} \sum_{L=1}^{L_{\max}} \left\| f_{\theta_L}\left([\mathbf{x}, \mathbf{z}(\mathbf{x}; L, \mathcal{Z})]\right) - d \right\|^2$$

这使得每一级八叉树都能学习到有效的几何表示，而非仅在最高 LOD 下过拟合。消融实验（Table 2）表明，仅训练 30 个 epoch 的 NG-LOD/LOD5 在 Thingi32 上的 Chamfer-L1 达到 0.0278，已优于训练 100 个 epoch 的 DeepSDF（0.0533）和 FFN（0.0329），验证了该联合训练策略的高效收敛性。

### 5. 关键性能跃迁

上述创新的综合效果体现在渲染速度的**2–3 个数量级提升**（Abstract）。具体而言，在 TurboSquid V Mech 场景 1920×1080 分辨率下，NG-LOD 稀疏渲染器的帧耗时仅 91ms，而 DeepSDF 需 1693ms，加速约 18.6 倍（Table 3）。同时，NG-LOD 在 ShapeNet150 上的 gIoU 达到 91.6%，高出 DeepSDF 4.7 个百分点（Table 1），实现了速度与质量的双重超越。

NG-LOD 的整体 pipeline 围绕**稀疏体素八叉树（SVO）特征体积**与**极轻量 MLP 解码器**的协同工作构建，其核心设计是将 SDF 的表示能力从网络权重转移到显式的分层特征存储中，从而在保持高重建质量的同时实现实时渲染。

### 数据流与模块关系

整个框架可分解为四个串联的功能模块，如图 Figure 3 所示：

![[assets/figures/papers/paper_list_l29_https_arxiv_org_abs_2101_10994/figures/003_Figure_3.jpg]]
*Figure 3: Architecture. We encode our neural SDF using a sparse voxel octree (SVO) which holds a collection of features Z. The levels of the SVO define LODs and the voxel corners contain feature vectors defining local surface segments. Given query point x and LOD L, we find corresponding voxels $V _ { 1 : L }$ , trilinearly interpolate their corners $\mathop { \mathbf { z } _ { V } ^ { ( j ) } }$ up to L and sum to obtain a feature vector z(x). Together with x, this feature is fed into a small MLP $f _ { \theta _ { L } }$ to obtain a signed distance dbL. We jointly optimize MLP parameters θ and features Z end-to-end

1. **稀疏体素八叉树（SVO）特征体积**：在包围盒 $[-1, 1]^3$ 内构建多层稀疏八叉树，每个体素角点存储一个可学习的特征向量 $\mathbf{z}_V^{(j)} \in \mathcal{Z}$。八叉树的每一层对应一个离散的细节层次（LOD），高层级（更精细的 LOD）的体素仅在与表面相关的空间区域被激活，形成稀疏结构。

2. **跨层特征插值与求和**：给定查询点 $\mathbf{x}$ 和目标 LOD $L$，系统在八叉树的第 1 到第 $L$ 层中定位包含 $\mathbf{x}$ 的体素，对每层的 8 个角点特征进行三线性插值，再将各层插值结果求和，得到聚合特征向量 $\mathbf{z}(\mathbf{x}; L, \mathcal{Z})$。

3. **MLP 解码器 $f_{\theta_L}$**：将拼接向量 $[\mathbf{x}, \mathbf{z}(\mathbf{x}; L, \mathcal{Z})]$ 输入一个极小的 MLP（单隐藏层 128 维，ReLU 激活，总参数量仅 4737），输出该 LOD 下的有符号距离预测值 $\widehat{d}_L$。

4. **稀疏自适应射线步进渲染器**：在实时渲染阶段，对每条射线执行并行广度优先的八叉树遍历。当查询点位于体素内部时，调用上述 SDF 查询进行标准的 sphere tracing 步进；当查询点位于体素外部时，通过射线-AABB 求交直接跳至下一个体素，大幅减少无效查询。

### 连续 LOD 机制

为实现视点相关的平滑过渡，NG-LOD 在两个相邻离散 LOD 的预测距离之间进行线性插值：

$$\widehat{d}_{\widetilde{L}} = (1 - \alpha) \widehat{d}_{L^*} + \alpha \widehat{d}_{L^* + 1}$$

其中 $L^*$ 为基础 LOD 层级，$\alpha$ 为插值系数。渲染时 LOD 的选择基于深度启发式策略——目标 LOD 随物体到相机的距离线性变化，由用户定义的阈值控制。

### 训练流程

训练阶段联合优化所有 LOD 层级的 MLP 参数 $\theta$ 和八叉树特征 $\mathcal{Z}$，损失函数为各层预测距离与真实 SDF 值的均方误差之和：

$$J(\theta, \mathcal{Z}) = \mathbb{E}_{\mathbf{x}, d} \sum_{L=1}^{L_{\max}} \left\| f_{\theta_L}\left([\mathbf{x}, \mathbf{z}(\mathbf{x}; L, \mathcal{Z})]\right) - d \right\|^2$$

这种多层级联合训练确保了每一级八叉树都能独立表示有效的几何信息，使得渲染时可在不同 LOD 间无缝切换。

### 3.1 隐式曲面与符号距离函数

NG-LOD 的基础表示是符号距离函数（SDF）。SDF 是一个映射 $f: \mathbb{R}^3 \to \mathbb{R}$，其中 $f(\mathbf{x})$ 表示点 $\mathbf{x}$ 到曲面的最短符号距离（正值为外部，负值为内部）。曲面 $\mathcal{S}$ 隐式定义为 SDF 的零等值面：

$$\mathcal{S} = \big\{ \mathbf{x} \in \mathbb{R}^3 \big| f(\mathbf{x}) = 0 \big\}$$

传统方法使用单一大型 MLP 来参数化整个 $f$，导致每次距离查询需要数百万次运算，成为实时渲染的根本瓶颈。

### 3.2 稀疏体素八叉树特征编码

NG-LOD 的核心创新在于将 SDF 的编码从单一全局 MLP 转变为**稀疏体素八叉树（SVO）存储的局部特征 + 极浅 MLP 解码器**的混合架构。具体而言：

- **特征存储**：在包围体 $\mathcal{B} = [-1, 1]^3$ 内构建 SVO，每个体素的角点存储一个可学习的特征向量 $\mathbf{z}_V^{(j)} \in \mathcal{Z}$，而非直接存储距离值。
- **层次 LOD**：SVO 的每一层对应一个离散的细节层次 $L$。层数越高，体素越细密，编码的几何细节越丰富。
- **特征查询与聚合**：给定查询点 $\mathbf{x}$ 和目标 LOD $L$，方法在 SVO 的第 1 到第 $L$ 层中定位包含 $\mathbf{x}$ 的体素，对每层体素角点特征进行三线性插值，再将各层插值结果求和，得到聚合特征向量 $\mathbf{z}(\mathbf{x}; L, \mathcal{Z})$。
- **距离解码**：将拼接向量 $[\mathbf{x}, \mathbf{z}(\mathbf{x}; L, \mathcal{Z})]$ 送入一个针对 LOD $L$ 的小型 MLP $f_{\boldsymbol{\theta}_L}$，输出预测的距离 $\widehat{d}_L$：

$$\widehat{d}_L = f_{\boldsymbol{\theta}_L}\big([\mathbf{x}, \mathbf{z}(\mathbf{x}; L, \mathcal{Z})]\big)$$

该架构的关键在于**计算负载转移**：主要运算从昂贵的 MLP 推理转移到高效的 SVO 遍历与三线性插值上。MLP 仅需一个隐藏层（维度 $h=128$，ReLU 激活），推理参数量固定为 4737，与 LOD 级别无关。

### 3.3 连续细节层次插值

为实现 LOD 间的平滑过渡，NG-LOD 在相邻两个离散 LOD 的预测距离之间进行线性插值。设目标连续 LOD 为 $\widetilde{L}$，其整数部分为 $L^*$，小数部分为 $\alpha$，则最终距离为：

$$\widehat{d}_{\widetilde{L}} = (1 - \alpha) \widehat{d}_{L^*} + \alpha \widehat{d}_{L^*+1}$$

这一机制使得渲染时可以根据相机距离动态、连续地调整几何精度，避免离散切换带来的视觉跳变。

### 3.4 训练损失

训练时联合优化所有 LOD 级别的 MLP 参数 $\theta$ 和特征体积 $\mathcal{Z}$。损失函数为所有 LOD 上预测距离与真实距离之间的均方误差期望：

$$J(\theta, \mathcal{Z}) = \mathbb{E}_{\mathbf{x}, d} \sum_{L=1}^{L_{\max}} \left\| f_{\theta_L}\left([\mathbf{x}, \mathbf{z}(\mathbf{x}; L, \mathcal{Z})]\right) - d \right\|^2$$

该多级联合训练确保每一层 SVO 都能独立表示有效的几何信息，为后续的 LOD 选择与连续插值奠定基础。

### 3.5 稀疏自适应射线步进渲染

为实现实时渲染，NG-LOD 设计了**稀疏自适应射线步进**算法，替代传统的均匀球体追踪。核心策略分为两种情况：

- **点在体素内**：对 SVO 中从基础层到目标 LOD 层的所有对应体素进行三线性插值，计算球体追踪步长。
- **点在体素外**：执行射线-AABB 相交检测，直接跳至下一个体素，跳过空白区域的大量无效查询。

该算法利用并行广度优先遍历和前缀和（Exclusive Sum）操作实现无冲突的稀疏八叉树写入索引，从而在 GPU 上高效执行。

## 实验与关键发现

### 几何重建质量

**NG-LOD** 在三个不同规模与特性的数据集上均以极低的推理参数量取得了优于全局隐式方法的几何精度。Table 1 显示，从 LOD 3 开始，本方法的各项指标已全面超越 **DeepSDF**（Park et al., CVPR 2019），而推理参数仅为 4737，相比 DeepSDF 的约 1.8M 参数减少了近 380 倍。在 ShapeNet150 上，LOD 4 的 gIoU 达到 91.6%，较 DeepSDF 的 86.9% 提升 4.7 个百分点；在 Thingi32 上，LOD 5 的 Chamfer- $L^1$ 降至 $0.0271 \times 10^3$，仅为 DeepSDF（0.0533）的一半；在 TurboSquid16 上，Normal- $L^2$ 误差从 0.180 降至 0.166。值得注意的是，存储开销也显著降低——本方法的存储基于所有形状的平均稀疏体素数量加解码器大小计算，在高 LOD 下仍保持紧凑。

定性结果（Figure 5）进一步印证了数值优势。在 TurboSquid 数据集上，**FFN**（Tancik et al., NeurIPS 2020）和 **Neural Implicits**（Davies et al., arXiv 2020）均丢失了大量高频细节，仅 NG-LOD 能恢复精细几何结构，且渲染速度比 FFN 快约 50 倍，与 NI 相当。

### 复杂解析 SDF 的极限测试

Figure 6 展示了两项极具挑战性的解析 SDF 重建任务：Oldcar（高度非度量的 SDF）和 Mandelbulb（递归分形结构）。所有基线方法——DeepSDF、FFN、**SIREN**（Sitzmann et al., NeurIPS 2020）、Neural Implicits——均无法合理重建这两个案例，而只有 NG-LOD 成功捕获了高频细节。这一结果揭示了本方法的核心优势：稀疏八叉树的局部特征存储使得模型能够为不同空间区域自适应分配表示容量，从而处理传统全局 MLP 无法表示的极端几何复杂度。

![[assets/figures/papers/paper_list_l29_https_arxiv_org_abs_2101_10994/figures/009_Figure_6.jpg]]
*Figure 6: Analytic SDFs. We test against two difficult analytic SDF examples from Shadertoy; the Oldcar, which contains a highly non-metric signed distance field, as well as the Mandelbulb, which is a recursive fractal structure that can only be expressed using implicit surfaces. Only our architecture can reasonably reconstruct these hard cases. We render surface normals to highlight geometric details. Table 2: Chamfer- L ^ { 1 } Convergence. We evaluate the performance of our architecture on the Thingi32 dataset under different training settings and report faster convergence for higher LODs*

### 收敛速度

Table 2 报告了 Thingi32 上的收敛效率。NG-LOD 在仅训练 30 个 epoch 后，LOD 5 的 Chamfer- $L^1$ 即达到 0.0278，已优于 DeepSDF 训练 100 个 epoch 的 0.0533 和 FFN 训练 100 个 epoch 的 0.0329。这意味着本方法在约 45% 的训练时间内即可超越基线的最优结果。更高 LOD 的收敛速度更快，这与多级特征层次从粗到精逐步细化几何的机制一致。

### 渲染性能

Table 3 报告了 TurboSquid V Mech 场景在 1920×1080 分辨率下的帧耗时。本方法的稀疏渲染器（Sparse）在 LOD 6 下仅需 91 ms，而 DeepSDF 的朴素球追踪需要 1693 ms，加速约 18.6 倍；与 **NSVF** 相比加速约 50 倍，与 **NeRF** 相比加速超过 500 倍。稀疏渲染器的性能增益来源于自适应射线步进策略（Figure 4）：当查询点位于体素内部时执行标准球追踪步进，位于体素外部时则通过 ray-AABB 相交直接跳至下一个体素，避免了对空白区域的无效 MLP 查询。

![[assets/figures/papers/paper_list_l29_https_arxiv_org_abs_2101_10994/figures/010_Table_3.jpg]]
*Table 3: Rendering Frametimes. We show runtime comparisons between different representations, where (N) and (S) correspond to our naive and sparse renderers, respectively. We compare baselines against Ours (Sparse) at LOD 6. # Visible Pixels shows the number of pixels occupied by the benchmarked scene (TurboSquid V Mech), and frametime measures ray-tracing and surface normal computation*

### 泛化能力

Table 4 评估了冻结解码器、仅训练特征体积的泛化设置。在 Thingi32 上，使用单个形状预训练的表面提取器权重并冻结，仅优化特征体积（Ours general），在高 LOD 下仍优于完全过拟合的大网络基线。这表明 MLP 解码器学习到的是可迁移的局部几何先验，而形状特异性信息主要存储在稀疏特征体积中。

![[assets/figures/papers/paper_list_l29_https_arxiv_org_abs_2101_10994/figures/011_Table_4.jpg]]
*Table 4: Generalization. We evaluate generalization on Thingi32. Ours (general) freezes surface extractor weights pretrained on a single shape, and only trains the feature volume. Even against large overfit networks, we perform better at high LODs*

### 与网格简化的对比

Figure 7 将 NG-LOD 与传统的网格简化方法在低内存预算下进行了对比。在相同的存储限制下，本方法能保持更好的视觉细节，表现为更低的 Normal- $L^2$ 误差。这说明隐式 LOD 表示在压缩效率上优于显式网格简化。

![[assets/figures/papers/paper_list_l29_https_arxiv_org_abs_2101_10994/figures/013_Figure_7.jpg]]
*Figure 7: Comparison with Mesh Decimation. At low memory budgets, our model is able to maintain visual details better than mesh decimation, as seen from lower normal- . L ^ { 2 } error*

### 消融：特征维度

附录 A.1 中的消融实验表明，特征维度 $m$ 可降至 8 仍保持令人满意的重建质量，但论文最终选择 $m=32$ 以获得更好的存储效率与质量权衡。

### 失败模式与局限

尽管 NG-LOD 在多个维度上表现优异，但其设计存在两个已知局限。第一，方法依赖有界体素八叉树，难以扩展到极大场景或非常薄的几何体（无体积）。第二，几何完全由隐式特征体积表示，无法轻松与传统变形或骨骼动画技术结合，限制了其在动态场景中的应用。

![[assets/figures/papers/paper_list_l29_https_arxiv_org_abs_2101_10994/figures/006_Table_1.jpg]]
*Table 1: Mesh Reconstruction. This table shows architectural and per-shape reconstruction comparisons against three different datasets. We see that under all evaluation schemes, our architecture starting from LOD 3 performs much better despite having much lower storage and inference parameters. The storage for our representation is calculated based on the average sparse voxel counts across all shapes in all datasets plus the decoder size, and # Inference Param. measures network parameters used for a single distance query*

## 定位与知识库关联

### 与基线方法的关系

NG-LOD 的核心突破在于将神经 SDF 的编码范式从“全局 MLP”转向“稀疏八叉树特征体 + 极浅 MLP 解码器”。这一转变使其与三类基线形成鲜明对比：

**全局隐式 SDF 方法。** **DeepSDF**（Park et al., CVPR 2019）使用一个大型 MLP（约 1.8M 参数）直接编码完整形状，每次距离查询需数百万次运算。NG-LOD 在 LOD 3 时推理参数仅 4737，却能在 ShapeNet150 上以 gIoU 90.4 超越 DeepSDF 的 86.9（Table 1），同时渲染速度提升两个数量级以上（Table 3）。**Fourier Feature Networks (FFN)**（Tancik et al., NeurIPS 2020）和 **SIREN**（Sitzmann et al., NeurIPS 2020）虽通过傅里叶特征或周期激活增强了高频细节捕捉，但在复杂解析 SDF（Oldcar、Mandelbulb）上均失败——FFN 甚至因无法学习保守度量 SDF 而产生白色斑块伪影，导致 sphere tracing 完全丢失表面（Figure 8）。只有 NG-LOD 能够合理重建这些非度量或分形结构（Figure 6）。

**单形状过拟合方法。** **Neural Implicits (NI)**（Davies et al., arXiv 2020）为每个形状过拟合一个小型 MLP，渲染速度较快但重建质量有限。在 TurboSquid 数据集上，NG-LOD 能以与 NI 可比的速度实现 50× 于 FFN 的加速，同时恢复更精细的几何细节（Figure 5）。

**体素/八叉树神经表示。** 与 NSVF（Liu et al., NeurIPS 2020）等基于体素的神经渲染方法不同，NG-LOD 在八叉树角点存储的是可学习特征向量而非直接的距离值或密度，并通过跨 LOD 特征求和实现连续细节层次。这使得 NG-LOD 的渲染帧耗时比 NeRF 快 500× 以上，比 NSVF 快 50× 以上（Introduction）。

### 适用边界

NG-LOD 的适用性受以下因素制约：

1. **场景规模与几何类型。** 方法依赖有界体素八叉树（$B = [-1, 1]^3$），难以直接扩展到极大场景（如城市级室外环境）。对于非常薄或“无体积”的几何体（如单层曲面、线框结构），八叉树的稀疏性优势减弱，体素边界可能无法有效捕捉表面。

2. **动态与变形。** 几何完全由隐式特征体积表示，无法轻松地与传统骨骼动画或变形技术结合。动态场景需要重新训练或设计额外的变形场，这超出了当前框架的范围。

3. **非度量 SDF 的泛化。** 尽管 NG-LOD 在 Oldcar 等非度量 SDF 上表现优异，但这是通过大量采样（每 epoch $5 \times 10^6$ 样本，100 个 epoch）训练实现的。对于训练时未见的非度量 SDF，泛化能力缺乏系统验证。

### 局限与开放问题

**已知局限。** 论文明确指出的局限包括：难以扩展到极大场景或极薄几何体；无法与传统变形/骨骼动画技术结合。此外，MLP 解码器虽极小（单隐藏层 128 维 ReLU），但在实时渲染中仍需频繁调用——Table 3 显示稀疏渲染器在 1920×1080 分辨率下帧耗时 91 ms，尚未达到 60 FPS（约 16.7 ms）的实时标准。

**开放问题。** 论文提出的开放方向包括：
- 通过缓存小型 MLP 解码器或进一步融合计算能否继续提升渲染性能？
- 如何将该表示扩展到大规模、多物体场景并支持动态更新？

从知识库定位来看，NG-LOD 开创了“稀疏特征八叉树 + 极浅解码器”的神经 SDF 实时渲染范式，后续工作可沿以下方向推进：将特征体积与哈希编码（如 Instant NGP）结合以进一步压缩存储；引入时序特征体积支持 4D 重建；或将八叉树遍历与硬件光追单元（RT core）深度集成以实现真正的实时帧率。

## 原文 PDF

![[paperPDFs/CVPR_2021/Neural_Geometric_Level_of_Detail_Real_time_Rendering_with_Implicit_3D_Surfaces.pdf]]
