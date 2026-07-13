---
title: "LoopGaussian: Creating 3D Cinemagraph with Multi-view Images via Eulerian Motion Field"
type: paper
paper_level: A
venue: "ACM MM"
year: 2024
pdf_ref: paperPDFs/ACM_MM_2024/LoopGaussian_Creating_3D_Cinemagraph_with_Multi_view_Images_via_Eulerian_Motion_Field.pdf
project_link: https://pokerlishao.github.io/LoopGaussian/
code_link: null
aliases:
- LoopGaussian
tags:
- ACM_MM_2024
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
core_operator: "通过3D高斯溅射显式重建静态场景，在3D空间定义欧拉运动场，利用场景自相似性（基于SuperGaussian聚类与余弦相似度）估计速度场，并采用双向动画技术生成无缝循环视频。"
primary_logic: "将微动摄影从2D提升至真实3D，核心在于从欧拉视角描述3D高斯点的连续运动，通过超像素风格聚类保持局部几何一致性，并利用场景自相似性避免大规模预训练。"
claims:
- "方法利用3D-GS从多视图图像重建3D高斯点云，并引入偏心率正则项抑制形变伪影"
- "通过SuperGaussian聚类将3D高斯点按空间邻近和特征相似性分组，保持局部运动一致性"
- "基于聚类间余弦相似度构建稀疏速度场，经Kriging插值和MLP细化得到欧拉运动场"
- "在用户研究中，94.23%的参与者更偏好本方法生成的视频"
---

# LoopGaussian: Creating 3D Cinemagraph with Multi-view Images via Eulerian Motion Field

> [!tip] 核心洞察
> 将微动摄影从2D提升至真实3D，核心在于从欧拉视角描述3D高斯点的连续运动，通过超像素风格聚类保持局部几何一致性，并利用场景自相似性避免大规模预训练。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | LoopGaussian: 基于欧拉运动场的多视图图像生成3D微动摄影 |
| 英文题名 | LoopGaussian: Creating 3D Cinemagraph with Multi-view Images via Eulerian Motion Field |
| 会议/期刊 | ACM MM 2024 |
| Links | [paper](https://arxiv.org/abs/2404.08966) · [Project](https://pokerlishao.github.io/LoopGaussian/) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction |
| Method | LoopGaussian |
| Dataset | 自建多视图场景（平均光流图）, 生成视频, 用户调研 |

> [!tip] 效果简介
> - 自建多视图场景（平均光流图） 上，PSNR (dB) 为 24.868，对比 22.959，变化 +1.909。
> - 生成视频 上，FVD 为 933.824，对比 1174.948，变化 -241.124 (越低越好)。
> - 用户调研 上，偏好比例 为 94.23%，对比 5.77%，变化 +88.46%。

## 概要

**问题瓶颈**：现有微动摄影（cinemagraph）方法多局限于2D图像空间操作，即便部分工作引入深度信息，仍采用多层深度图像（MPI）或分层深度图像（LDI）等2.5D表示，缺乏真实3D几何结构。这导致渲染视角严重受限，且易产生几何不一致的伪影。唯一直接处理3D微动摄影的基线方法为 **3D Cinemagraphy**（Li et al., CVPR 2023）。

**核心方法**：LoopGaussian 提出将微动摄影从2D提升至真实3D空间。其核心思路是：首先利用3D高斯溅射（3D-GS）从多视图静态图像显式重建场景的3D高斯点云，并引入偏心率正则化抑制形变伪影；随后在3D空间定义欧拉运动场（Eulerian motion field）来描述场景动态，通过场景自相似性（基于SuperGaussian聚类与余弦相似度）估计速度场，最终采用双向动画技术生成无缝循环视频。整个框架是启发式的，无需大规模数据集预训练。

**关键结果**：在自建多视图场景上，LoopGaussian 的平均光流图 PSNR 达到 24.868 dB，较 Li et al. 方法提升 1.909 dB；生成视频的 FVD 指标从 1174.948 降至 933.824。用户调研中，94.23% 的参与者更偏好本方法生成的视频效果。

**局限与开放问题**：当前方法适用于软质非刚体物体（如树枝、旗帜），对刚性运动或复杂非周期性形变可能失效；动态区域仍需手动标注2D掩码；欧拉运动场为静态速度场，无法处理随时间变化的运动模式。MLP估计欧拉运动场时的具体架构细节（如输入维度、层数）未在文中明确，仅提及两层隐藏层（128和64）与位置编码。



微动摄影（Cinemagraph）是一种将静态图像中局部区域赋予微妙、循环运动的视觉艺术形式，在影视、广告与数字媒体中应用广泛。传统微动摄影方法主要依赖2D图像空间操作，通过光流估计或深度引导的像素位移来模拟运动效果。然而，这类方法存在根本性局限：它们无法支持自由视点渲染，观察者始终被锁定在原始拍摄视角。

部分工作尝试引入深度信息以缓解视角限制，例如采用多层图像表示（MPI）或分层深度图像（LDI）。但这些表示本质上仍是2.5D的——它们缺乏真实的三维几何结构，导致视角变化范围受限，且在多视角一致性上容易产生几何伪影。**3D Cinemagraphy**（Li et al., CVPR 2023）是当前唯一直接面向3D微动摄影的方法，但其底层表示仍沿用多层2D结构，未能从根本上突破上述瓶颈。

从运动描述范式来看，现有方法普遍采用拉格朗日视角——追踪每个像素在帧间的位移（光流/场景流）。这种逐点追踪在3D空间中计算代价高昂，且难以保证全局运动的平滑性与连续性。此外，多数方法依赖在大规模数据集上预训练的深度估计或光流网络，这限制了它们在非典型场景中的泛化能力。

LoopGaussian的核心动机在于：**将微动摄影从2D/2.5D提升至真实3D空间**。这需要解决两个关键问题：其一，如何获得可自由视点渲染的显式3D场景表示；其二，如何在3D空间中定义并估计保持局部一致性的连续运动。本文选择3D高斯溅射（3D-GS）作为静态场景表示，利用其显式点云结构与高效可微渲染能力，为3D运动场建模提供几何载体。在运动描述上，本文从欧拉视角出发，在3D空间定义速度场，并通过场景自相似性启发式地估计运动方向，从而避免了对大规模预训练数据的依赖。



## 核心方法与创新机理

LoopGaussian 的核心创新在于将微动摄影从二维图像空间提升至真实三维场景，其关键突破体现在以下五个维度的改变：

**场景表示：从2D多层到3D显式几何**

现有微动摄影方法（如 Li et al., CVPR 2023）采用多层2D图像加深度（MPI/LDI）表示场景，本质上仍是2.5D的视图合成，缺乏真实三维几何结构，导致视角受限且易产生几何不一致伪影。LoopGaussian 直接使用3D高斯溅射（3D-GS）从多视图图像重建显式的3D高斯点云，使场景具备完整的空间几何，支持任意自由视点的渲染。这一改变是后续所有三维操作的基础。

**运动描述：从2D光流到3D欧拉运动场**

传统方法依赖二维图像空间的光流或场景流描述运动，运动信息与视角绑定，难以跨视角泛化。LoopGaussian 创新性地在三维空间中定义欧拉运动场 $\vec{E}_G$，描述每个空间位置的连续运动向量。粒子位置通过欧拉积分更新：

$$X(t+1) = X(t) + \vec{E}(X(t))$$

这种欧拉视角的运动描述使得同一运动场可从任意视点渲染，保证了运动在多视角下的一致性。

**局部运动保持：SuperGaussian聚类机制**

现有方法缺乏显式的局部运动一致性约束，运动估计容易碎片化。LoopGaussian 设计了 SuperGaussian 聚类方法，将3D高斯点按空间邻近和特征相似性分组。其距离度量融合了特征余弦距离与归一化空间欧氏距离：

$$D(G_i, G_j) = 1 - \frac{|f_i \cdot f_j|}{\|f_i\| \cdot \|f_j\|} + \mu \frac{\|\mathbf{p}_i - \mathbf{p}_j\|}{R}$$

该聚类借鉴超体素思想，通过自编码器将高斯点投影到低维特征空间后再聚类，确保单个物体（如一片叶子）被完整包含在一个聚类内，从而保持局部几何一致性。实验表明该方法仅需一次迭代即可收敛。

**数据需求：从预训练依赖到场景自相似性驱动**

现有方法通常依赖在大规模数据集上预训练的深度估计或运动预测网络。LoopGaussian 采用启发式策略，利用场景自身的自相似性构建运动场：计算各 SuperGaussian 聚类间的余弦相似度，将每个聚类朝向最相似的聚类移动，形成稀疏速度场。经 Kriging 插值和 MLP 细化后得到平滑的欧拉运动场。这一设计消除了对大规模预训练数据的依赖，使方法更具通用性。

**动态区域分割：从手动分层到交互式3D分割**

传统方法需手动分层或仅基于深度进行动态区域划分。LoopGaussian 借助 SAGA 交互式分割方法直接作用于3D高斯点云，用户仅需在2D图像上提供简单标注即可获得3D空间的二值掩码 $\mathbf{M}$，将场景分离为静态和动态组件。这既保留了用户对运动区域的创作控制，又避免了繁琐的手动三维操作。

**辅助创新：偏心率正则化**

为抑制3D高斯点在运动过程中的形变伪影（如毛刺），LoopGaussian 在3D-GS重建阶段引入偏心率正则化损失：

$$\mathcal{L}_{\mathrm{shape}} = \frac{1}{|\mathbf{G}|} \sum_{G_i \in \mathbf{G}} 1 - \frac{\min^2(s_i)}{\max^2(s_i)}$$

该损失约束高斯点形状趋近球体，消融实验（Figure 4）证实其能显著减少场景中的毛刺和伪影。



![[assets/figures/papers/paper_list_l47_LoopGaussian_Creating_3D_Cinemagraph_with_Multi_view_Images_via_Eulerian/figures/001_Figure_1.jpg]]
*Figure 1: We propose LoopGaussian, a novel method designed to convert multi-view images of a stationary scene (a) into authentic 3D cinemagraph by an Eulerian motion field (b). The 3D cinemagraph can be rendered from a novel viewpoint to obtain a natural seamless loopable video (c)*

LoopGaussian 将静态场景的多视图图像转化为可自由视点渲染的 3D 微动摄影，其核心流程分为三个阶段：**3D 场景重建与分割**、**欧拉运动场估计**、以及**双向动画生成**（Figure 2）。

**第一阶段：3D 高斯场景重建与动态区域分离。** 给定静态场景的多视图图像，方法首先采用 3D-GS 重建显式的 3D 高斯点云，并引入偏心率正则化项（Eq. 4）约束高斯形状趋近球体，以抑制后续形变过程中产生的毛刺和伪影（Sec. 4.2）。随后，用户通过 2D 掩码指定期望运动的区域，利用 SAGA 交互式分割方法将 3D 高斯点云分离为静态部分与动态部分（Eq. 6），仅对动态高斯点进行后续运动建模。

**第二阶段：欧拉运动场估计。** 动态高斯点首先经由基于 PointNet 的自编码器投影到低维特征空间，以捕获每个点的语义和几何属性。为保持局部运动一致性，方法提出 SuperGaussian 聚类——将 3D 空间划分为体素网格，在每个非空体素内选取种子点，依据融合了特征余弦距离与空间欧氏距离的度量函数（Eq. 8）进行快速聚类（Sec. 4.3）。聚类完成后，计算各聚类全局特征的余弦相似度矩阵，将每个聚类朝向与其最相似的聚类移动，得到稀疏速度场 $v_{s_i} = \bar{p}_{j^*} - \bar{p}_i$。该稀疏场经 Kriging 插值扩展为稠密速度场，再由一个具有两层隐藏层（128 和 64）并施加位置编码的 MLP 细化，最终输出平滑的欧拉运动场 $\vec{E}_G$（Sec. 4.4）。

**第三阶段：双向动画与循环视频生成。** 在 3D 空间中，对每个动态高斯点沿欧拉运动场进行正向和反向欧拉积分（Eq. 12），引入运动幅度向量 $\psi$ 控制各轴运动强度。正向与反向运动路径通过线性插值融合（Eq. 13），生成无缝循环的 3D 动态场景。给定任意相机参数，即可渲染出具有真实 3D 几何一致性的循环视频。

整个框架的关键设计在于：**无需大规模预训练**，而是利用场景自相似性启发式地估计运动；**在 3D 空间直接操作显式几何表示**，避免了 2D 方法中多层表示带来的视角受限和几何不一致问题。



### 3D高斯溅射与形状正则化

LoopGaussian以多视图图像为输入，首先采用3D高斯溅射（3D-GS）重建静态场景的显式点云表示。每个3D高斯点由位置 $p$ 和协方差矩阵 $\Sigma$ 定义：

$$G ( x ) = e ^ { - \frac { 1 } { 2 } ( x - p ) ^ { T } \Sigma ^ { - 1 } ( x - p ) }$$

渲染时，通过深度排序后的α混合计算像素颜色：

$$\hat { c } = \sum _ { i \in G _ { \mathrm { p i x e l } } } \hat { c } _ { i } \hat { \alpha } _ { i } \prod _ { j = 1 } ^ { i - 1 } ( 1 - \hat { \alpha } _ { j } )$$

为抑制后续形变过程中产生的毛刺与伪影，引入偏心率正则化损失，约束高斯形状趋近球体：

$$\mathcal { L } _ { \mathrm { s h a p e } } = \frac { 1 } { \vert \mathbf { G } \vert } \sum _ { G _ { i } \in \mathbf { G } } 1 - \frac { \mathrm { m i n } ^ { 2 } ( s _ { i } ) } { \mathrm { m a x } ^ { 2 } ( s _ { i } ) }$$

其中 $s_i$ 为高斯点 $G_i$ 的尺度向量。总优化目标融合L1损失、D-SSIM损失与形状正则项：

$$\mathcal { L } _ { \mathrm { 3 D - G S } } = \eta \left( \left( 1 - \beta \right) \mathcal { L } _ { 1 } + \beta \mathcal { L } _ { \mathrm { D - S S I M } } \right) + \left( 1 - \eta \right) \mathcal { L } _ { \mathrm { s h a p e } }$$

消融实验证实（Figure 4），移除偏心率正则化会导致场景出现明显毛刺，验证了该模块对形变伪影的抑制作用。

### 动态区域分割

为指定需要运动的场景区域，采用SAGA交互式分割方法对3D高斯点云生成二值掩码 $\mathbf{M}$，将点云划分为静态与动态两部分。用户仅需提供2D标注，SAGA将其传播至3D空间，完成动态高斯点的筛选。

### SuperGaussian聚类

动态3D高斯点首先通过基于PointNet的自编码器投影至低维特征空间，随后进行SuperGaussian聚类，以保持局部几何一致性。聚类优化目标为最小化各点到其聚类中心的距离和：

$$\mathrm { S G } ^ { * } = \underset { \mathrm { S G } } { \arg \operatorname* { m i n } } \sum _ { k = 1 } ^ { K } \sum _ { \mathrm { S G } ( G _ { i } ) = k } D ( G _ { i } , G _ { k ^ { \prime } } )$$

距离度量 $D$ 融合特征余弦不相似度与归一化空间欧氏距离：

$$D ( G _ { i } , G _ { j } ) = 1 - \frac { | f _ { i } \cdot f _ { j } | } { \| f _ { i } \| \cdot \| f _ { j } \| } + \mu \frac { \| \mathbf { p } _ { i } - \mathbf { p } _ { j } \| } { R }$$

其中 $f_i$、$f_j$ 为高斯点的自编码器特征，$\mathbf{p}_i$、$\mathbf{p}_j$ 为空间位置，$R$ 为体素分辨率，$\mu$ 为平衡权重。聚类种子通过非空体素均匀采样初始化，据文中描述仅需一次迭代即可收敛。消融实验（Figure 6）表明，合适的体素分辨率 $\lambda=0.04$ 能在避免多对象混入同一聚类与避免单对象碎片化之间取得平衡。

### 欧拉运动场估计

基于场景自相似性，利用聚类间余弦相似度构建稀疏速度场。聚类 $i$ 朝向最相似聚类 $j^*$ 的速度向量为：

$$v _ { s _ { i } } = \bar { p } _ { j ^ { * } } - \bar { p } _ { i }$$

其中 $\bar{p}_i$ 为聚类 $i$ 的中心位置，$j^*$ 由余弦相似度矩阵的argmax确定。稀疏速度场经Kriging插值得到稠密速度场，再由MLP细化生成平滑的欧拉运动场 $\vec{E}_G$。MLP采用两层隐藏层（128和64维），输入施加位置编码。消融实验（Figure 5）显示，Kriging插值相比无插值或RBF插值能产生更完整的对象和更连续的运动。

### 双向动画与无缝循环

在3D空间施加欧拉运动场，通过欧拉积分更新高斯点位置：

$$p _ { i } ( t ) = p _ { i } ( 0 ) + \sum _ { \tau = 0 } ^ { t - 1 } \psi \odot \vec { E } _ { G } \left( p _ { i } \left( \tau \right) \right)$$

其中 $\psi \in \mathbb{R}^3$ 为各轴运动幅度向量，由超参数 $\omega$ 控制。为生成无缝循环视频，将正向与反向运动路径进行线性插值：

$$\hat { p } _ { i } ( t ) = \alpha p _ { i } ( t ) + ( 1 - \alpha ) p _ { i } ( t - T )$$

其中 $T$ 为周期长度，$\alpha$ 为插值权重。消融实验（Figure 7）表明，过大的 $\omega$ 会破坏场景结构连续性。



## 实验与关键发现

### 主实验结果

LoopGaussian 与唯一直接可比的 3D 微动摄影方法——**3D Cinemagraphy**（Li et al., CVPR 2023）——进行了定量与定性对比。后者采用多层深度图像（LDI）表示场景，而本方法使用显式 3D 高斯点云与欧拉运动场，二者在场景表示与运动描述上存在根本差异。

**平均光流图定量评估**：以真实视频的平均光流图作为参考，计算生成视频光流图的 PSNR、SSIM 和 LPIPS。如 Table 1 所示，LoopGaussian 在 PSNR 上达到 24.868 dB，较 Li et al. 的 22.959 dB 提升 1.909 dB；SSIM 与 LPIPS 也均优于对比方法。这表明本方法生成的运动模式在空间分布上与真实运动更为接近。

![[assets/figures/papers/paper_list_l47_LoopGaussian_Creating_3D_Cinemagraph_with_Multi_view_Images_via_Eulerian/figures/005_Table_1.jpg]]
*Table 1: Quantitative comparison of average optical flow maps*

**生成视频的 FVD 评估**：采用 Fréchet Video Distance（FVD）衡量生成视频的时序连贯性与视觉质量。Table 2 显示，LoopGaussian 的 FVD 为 933.824，显著低于 Li et al. 的 1174.948（降幅 241.124），说明本方法生成的视频在时序平滑度和视觉逼真度上具有明显优势。

![[assets/figures/papers/paper_list_l47_LoopGaussian_Creating_3D_Cinemagraph_with_Multi_view_Images_via_Eulerian/figures/006_Table_2.jpg]]
*Table 2: Quantitative comparison of generated videos*

**用户调研**：邀请 52 名参与者对两组方法生成的视频进行视觉偏好投票。Table 3 的结果表明，94.23% 的参与者更偏好 LoopGaussian 生成的视频，仅有 5.77% 选择 Li et al. 的方法。这一压倒性优势验证了真实 3D 表示在自由视点渲染与运动自然度上远超 2D 深度分层方法。

![[assets/figures/papers/paper_list_l47_LoopGaussian_Creating_3D_Cinemagraph_with_Multi_view_Images_via_Eulerian/figures/008_Table_3.jpg]]
*Table 3: User study on visual effects of generated videos*

**定性分析**：Figure 3 展示了关键帧与平均光流图的可视化对比。LoopGaussian 生成的视频帧中，运动物体的边缘更清晰、几何形变更自然，放大细节中未见明显的撕裂或模糊伪影；而 Li et al. 方法在物体边界处存在可见的几何不一致和光流断裂。平均光流图的颜色分布也表明，本方法的运动方向更连续、噪声更少。

### 消融实验

**偏心率正则化**：Figure 4 对比了是否使用偏心率正则化项 $\mathcal{L}_{\mathrm{shape}}$（Eq. 4）的 3D 高斯重建结果。未加正则化时，3D 高斯点因优化自由度大而呈现细长椭球状，在施加运动场后产生大量毛刺和闪烁伪影；加入正则化后，高斯点被约束为近似球体，运动形变时场景表面保持平滑，毛刺显著减少。该正则化是保证形变后渲染质量的关键设计。

**插值方法**：Figure 5 对比了无插值、RBF 插值与 Kriging 插值三种策略得到的稠密速度场。无插值时速度场过于稀疏，仅少数聚类中心附近有运动向量，导致物体运动不完整；RBF 插值虽能填充空白区域，但易产生不连续的速度跳变；Kriging 插值则生成更平滑、更连续的速度场，使得运动物体形态完整且运动轨迹自然。这一结果验证了 Kriging 在地统计插值中对空间相关性建模的优势。

**体素分辨率对聚类的影响**：Figure 6 展示了不同体素分辨率 $\lambda$ 下 SuperGaussian 的聚类效果。$\lambda$ 过大时，多个独立物体被合并到同一聚类，运动一致性丧失；$\lambda$ 过小时，单个物体被过度分割到多个聚类，导致运动碎片化。实验表明，合适的 $\lambda$（文中示例为 0.04）能使每个独立物体（如单片叶子）恰好被包含在一个聚类内，在分割粒度与信息保留间取得平衡。

![[assets/figures/papers/paper_list_l47_LoopGaussian_Creating_3D_Cinemagraph_with_Multi_view_Images_via_Eulerian/figures/010_Figure_6.jpg]]
*Figure 6: Clustering results at various voxel resolutions. Distinct colors indicate different clusters. We aim to ensure that each individual object (e.g., a leaf) is encompassed within a single cluster (middle), rather than having multiple objects grouped into one cluster (left) or a single object fragmented across multiple clusters (right)*

**运动幅度控制**：Figure 7 展示了运动幅度参数 $\omega$（作用于 Eq. 12 中的 $\psi$）对场景形变程度的影响。$\omega$ 越大，场景运动越剧烈；但当 $\omega$ 过大时，场景结构出现破坏性撕裂（如右下角示例），物体几何连续性被打破。该参数需根据场景尺度与期望运动强度进行调节，过大的幅度会超出欧拉运动场的有效形变范围。

![[assets/figures/papers/paper_list_l47_LoopGaussian_Creating_3D_Cinemagraph_with_Multi_view_Images_via_Eulerian/figures/012_Figure_7.jpg]]
*Figure 7: Effect of the motion amplitude. The deformation amplitude of the scene can be controlled by ??. The larger ?? is, the more intense the movement of the scene becomes. Note that excessively large values of ?? may result in structural damage to the scene (lower right corner)*

### 失败模式与局限性

尽管 LoopGaussian 在软质非刚体场景（如树枝摇曳、旗帜飘动）中表现优异，但方法存在若干已知局限：

1. **刚性运动不适用**：欧拉运动场描述的是连续介质形变，对刚体平移或旋转等不改变内部几何关系的运动无法有效建模。
2. **依赖场景自相似性**：稀疏速度场的构建依赖聚类间的余弦相似度（$s_{ij}$），若场景缺乏重复结构（如单一孤立物体），相似度矩阵将无法提供有意义的运动方向，速度场估计可能失败。
3. **手动标注需求**：动态区域仍需用户提供 2D 掩码进行 SAGA 交互式分割，尚未实现全自动运动区域检测。
4. **静态速度场假设**：欧拉运动场不随时间变化，无法处理加速运动或时变运动模式。

### 公平性说明

- 本方法仅需静态多视图图像作为输入，而 Ma et al. 等方法依赖多视图视频，输入条件不同，因此未纳入定量对比，这一选择具备合理性。
- 用户调研仅基于视觉偏好投票，未纳入多视角一致性等客观指标，结论的全面性需进一步验证。

### 补充图表

![[assets/figures/papers/paper_list_l47_LoopGaussian_Creating_3D_Cinemagraph_with_Multi_view_Images_via_Eulerian/figures/009_Figure.jpg]]
*Figure: w/o eccentricity regularization w/ eccentricity regularization*



## 定位与知识库关联

### 与现有工作的关系

LoopGaussian 的核心突破在于将微动摄影从 2D 图像空间提升至真实 3D 表示。此前，微动摄影方法主要分为两类：一类在单张 2D 图像上通过光流模拟局部运动（如 Holynski et al. 的经典工作）；另一类虽引入深度信息，但仍采用多层 2D 表示，如 MPI（Multiplane Image）或 LDI（Layered Depth Image）。**3D Cinemagraphy**（Li et al., CVPR 2023）是唯一直接可比的 3D 微动摄影方法，其采用 LDI 表示场景，本质上仍是 2.5D 表示，视角受限且易产生几何不一致伪影。

LoopGaussian 与 Li et al. 的方法存在三个关键差异槽位：

| 维度 | 3D Cinemagraphy (Li et al., CVPR 2023) | LoopGaussian (本文) |
|------|----------------------------------------|---------------------|
| 场景表示 | 多层 2D 图像 + 深度（LDI） | 3D 高斯点云显式重建 |
| 运动描述 | 基于 2D 图像的场景流 | 3D 空间中的欧拉运动场 |
| 数据需求 | 依赖大规模预训练（深度估计等） | 无预训练，利用场景自相似性 |

在 3D 高斯溅射（3D-GS）生态中，LoopGaussian 属于对静态 3D-GS 重建结果进行动态化处理的工作。与基于视频输入的 4D-GS 方法（如 Dynamic 3D Gaussians）不同，LoopGaussian 仅需静态多视图图像作为输入，通过场景自相似性推断运动，避免了对时间序列数据的依赖。这与同期利用 3D-GS 进行场景编辑和动画化的趋势一致，但其独特之处在于欧拉视角的运动描述——在固定网格点上定义速度场，而非追踪拉格朗日粒子轨迹。

### 适用边界

**适用场景：**
- 软质非刚体物体的周期性微动，如树枝摇曳、旗帜飘动、绳索摆动、水面涟漪等
- 场景中存在明显的自相似结构（如树叶间、花瓣间），能够支撑基于余弦相似度的速度场估计
- 用户可接受对动态区域进行简单的 2D 掩码标注

**不适用或需谨慎的场景：**
- 刚性物体的整体运动（如车辆行驶、球体滚动）
- 复杂非周期性形变（如布料撕裂、流体飞溅）
- 高度非重复性场景，缺乏可匹配的相似结构，SuperGaussian 聚类难以构建有效速度场
- 需要精确物理模拟的大形变场景——过大的运动幅度参数 $\omega$ 会破坏场景结构连续性（见 Figure 7）

### 局限与开放问题

**已知局限：**

1. **动态区域需手动标注**：当前方法依赖 SAGA 交互式分割，用户需提供 2D 掩码指定运动区域，尚未实现全自动化（Sec. 4.2）。

2. **静态欧拉运动场的表达能力有限**：欧拉运动场为时不变速度场，不能处理随时间变化的运动模式（如加速、减速），这限制了其对复杂动力学场景的建模能力。

3. **自相似性假设的脆弱性**：速度场估计完全依赖聚类间余弦相似度，当场景缺乏重复结构时，最近邻匹配可能产生不合理的运动方向。

4. **仅与单一基线定量对比**：实验仅与 Li et al. (CVPR 2023) 进行定量和用户研究对比，未与基于多视图视频的方法（如 Ma et al.）比较。虽然输入条件不同（本文仅需静态图像）使对比具备合理性，但方法在更广泛基准上的表现尚待验证。

**开放问题：**

- **MLP 架构细节未完全公开**：用于估计欧拉运动场的 MLP 仅提及两层隐藏层（128 和 64）与位置编码（Sec. 5.2），但输入维度、激活函数、训练损失等细节未明确，影响复现精度。

- **多对象独立控制**：当前方法对所有动态高斯点施加统一的欧拉运动场，能否扩展至多运动对象的独立控制（如分别控制不同树枝的摆动幅度和方向）？

- **物理先验的融合**：能否结合物理模拟或数据驱动先验提升大形变场景的鲁棒性？例如，对旗帜飘动引入流体力学约束，可能减少结构破坏的风险。

- **多摄像机运动视频的扩展**：当前方法输入为静态多视图图像，若能扩展至手持摄像机拍摄的晃动视频，将大幅降低数据采集门槛。这需要同时估计摄像机位姿和场景运动。



## 原文 PDF

![[paperPDFs/ACM_MM_2024/LoopGaussian_Creating_3D_Cinemagraph_with_Multi_view_Images_via_Eulerian_Motion_Field.pdf]]
