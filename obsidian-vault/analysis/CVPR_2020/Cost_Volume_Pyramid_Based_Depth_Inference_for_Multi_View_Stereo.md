---
title: "Cost Volume Pyramid Based Depth Inference for Multi-View Stereo"
type: paper
paper_level: A
venue: CVPR
year: 2020
pdf_ref: paperPDFs/CVPR_2020/Cost_Volume_Pyramid_Based_Depth_Inference_for_Multi_View_Stereo.pdf
aliases:
- CMCVPBMVSN
- CVPBDIMVS
tags:
- CVPR_2020
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
core_operator: "通过构建代价体金字塔并以粗到细的方式迭代优化深度残差，替代传统的固定分辨率单一代价体。"
primary_logic: "深度采样间隔与图像分辨率存在直接关联：过密的采样无法提供额外区分性信息；采用金字塔结构在每一层仅构建局部部分代价体，结合多尺度3D CNN正则化，可以在显著降低计算和内存开销的同时提升深度估计精度。"
claims:
- "相比Point-MVSNet，在输出相同尺寸深度图时，GPU内存消耗和运行时间均降低约6倍"
- "在DTU数据集上取得整体误差0.351 mm，优于所有深度学习方法"
- "两级金字塔结构与0.5像素深度偏移间隔的组合带来最佳重建质量"
- "在Tanks and Temples基准上平均F-score达到54.03，显著超过Point-MVSNet的48.27"
---

# Cost Volume Pyramid Based Depth Inference for Multi-View Stereo

> [!tip] 核心洞察
> 深度采样间隔与图像分辨率存在直接关联：过密的采样无法提供额外区分性信息；采用金字塔结构在每一层仅构建局部部分代价体，结合多尺度3D CNN正则化，可以在显著降低计算和内存开销的同时提升深度估计精度。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 基于代价体金字塔的多视图立体深度推断 |
| 英文题名 | Cost Volume Pyramid Based Depth Inference for Multi-View Stereo |
| 会议/期刊 | CVPR 2020 |
| Links | [paper](https://arxiv.org/abs/1912.08329); [GitHub](https://github.com/JiayuYANG/CVP-MVSNet) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction |
| Method | CVP-MVSNet（Cost Volume Pyramid based Multi-View Stereo Network） |
| Dataset | DTU, DTU (相同深度图尺寸640), Tanks and Temples |

> [!tip] 效果简介
> - DTU 上，Overall (mm, 越低越好) 为 0.351，对比 Point-MVSNet: 0.376，变化 -0.025。
> - DTU (相同深度图尺寸640) 上，Runtime (s) 为 0.37，对比 Point-MVSNet: 2.03，变化 快约6倍。
> - DTU (相同深度图尺寸640) 上，GPU Memory (MB) 为 1416，对比 Point-MVSNet: 8989，变化 内存减少约6倍。

## 概述

基于多视图图像的深度推断是三维重建的核心任务。传统方法依赖手工设计的相似性度量与全局优化，而近年来的学习型多视图立体（MVS）方法虽然在精度上取得了显著突破，却普遍面临**内存需求大**与**运行速度慢**的双重瓶颈——这源于它们通常在单一固定分辨率下构建完整代价体，其内存开销与分辨率立方成正比，严重限制了在高分辨率场景下的实际部署。

本文提出 **CVP-MVSNet**（Cost Volume Pyramid based Multi-View Stereo Network），核心思路是**以粗到细的方式构建代价体金字塔**，替代传统的固定分辨率单一代价体。该方法的关键洞察在于：深度采样间隔与图像分辨率之间存在直接关联——过密的深度采样无法提供额外的区分性信息。基于此，CVP-MVSNet 在金字塔的每一层仅构建局部部分代价体用于深度残差估计，并结合多尺度 3D CNN 正则化，在显著降低计算与内存开销的同时提升深度估计精度。

在 DTU 数据集上，CVP-MVSNet 取得 **0.351 mm** 的整体误差，优于包括 **MVSNet**（Yao et al., ECCV 2018）、**R-MVSNet**（Yao et al., CVPR 2019）和 **Point-MVSNet**（Chen et al., ICCV 2019）在内的所有深度学习方法。相比直接竞争的粗到细基线 Point-MVSNet，在输出相同尺寸深度图时，GPU 内存消耗和运行时间均**降低约 6 倍**（1416 MB vs 8989 MB，0.37 s vs 2.03 s）。在 Tanks and Temples 基准上，平均 F-score 达到 **54.03**，显著超过 Point-MVSNet 的 48.27，验证了其良好的泛化能力。消融实验进一步表明，两级金字塔结构与对应 0.5 像素偏移的深度采样间隔组合可带来最佳重建质量。

## 背景与动机

多视图立体（Multi-View Stereo, MVS）是三维计算机视觉中的核心问题，其目标是从一组已知相机参数的图像中恢复场景的稠密三维结构。传统几何方法在强纹理区域表现良好，但在弱纹理、镜面反射或遮挡区域往往难以获得可靠重建。近年来，基于深度学习的方法通过将可微单应性变换与3D卷积网络结合，显著提升了重建的鲁棒性和精度。

然而，现有学习型MVS方法面临一个根本性的瓶颈：**内存需求与运行速度之间的尖锐矛盾**。以**MVSNet**（Yao et al., ECCV 2018）为代表的经典框架，在单一固定分辨率下构建完整的3D代价体，其内存开销与图像分辨率的三次方成正比。当处理高分辨率图像时，这种暴力构建方式迅速耗尽GPU内存，迫使研究者不得不在精度和效率之间做出妥协。后续工作试图缓解这一困境，但各自引入了新的代价：**R-MVSNet**（Yao et al., CVPR 2019）通过GRU递归网络顺序处理代价体以降低内存，却导致运行时间显著增加；**Point-MVSNet**（Chen et al., ICCV 2019）将粗到细的深度优化过程迁移到点云空间，避免了稠密代价体的构建，但点云操作本身的计算开销仍然可观。

这一瓶颈的深层原因在于，现有方法未能充分理解**深度采样间隔与图像分辨率之间的内在关联**。直觉上，在给定图像分辨率下，过密的深度采样并不会提供额外的区分性信息——相邻深度假设平面投影到源视图上的像素偏移量若远小于1个像素，它们所获取的特征将几乎完全相同，从而无法为匹配代价的计算贡献有效信息。反之，过疏的采样则可能错失真实的深度值。这种采样-分辨率的耦合关系，暗示着代价体的构建应当与图像分辨率自适应匹配，而非在固定分辨率上均匀采样。

基于上述洞察，本文提出**CVP-MVSNet**（Cost Volume Pyramid based Multi-View Stereo Network），核心动机是：通过构建代价体金字塔，以粗到细的方式迭代优化深度残差，从而在每一层级仅构建与当前分辨率匹配的局部部分代价体。这一设计使得计算和内存开销从立方级降低至可控范围，同时避免了冗余采样带来的信息退化。论文的核心主张可概括为：**深度采样策略应当由目标像素偏移量（如0.5像素）决定，而非固定的采样数目；代价体的构建应当遵循金字塔结构，而非单一分辨率。**

## 核心创新

CVP-MVSNet 的核心创新在于通过**代价体金字塔**的粗到细构建，从根本上改变了多视图立体匹配中代价体的组织方式与深度推断流程。相比以固定分辨率代价体为核心的基线方法，该方法在三个关键维度上实现了结构性改变。

### 1. 代价体构建方式：从单一固定分辨率到金字塔式局部构建

经典方法（如 **MVSNet**，Yao et al., ECCV 2018）在单一固定分辨率下构建完整代价体，其内存需求与分辨率立方成正比，严重限制了高分辨率场景下的应用。CVP-MVSNet 则构建一个代价体金字塔：从最粗分辨率层级开始，在整个深度范围内均匀采样前向平行平面构建初始代价体；随后，基于当前深度估计，在每一层仅构建**局部部分代价体**以预测深度残差，而非重新构建完整代价体（见 Abstract, Section 3.2）。这一设计的直接效果是：在输出相同尺寸深度图时，GPU 内存消耗从 Point-MVSNet 的 8989 MB 骤降至 1416 MB，降幅约 6 倍（Table 2）。

### 2. 深度采样策略：从固定均匀采样到分辨率自适应的像素偏移引导采样

传统方法对深度假设平面进行固定数量的均匀采样，未考虑采样间隔与图像分辨率的关联。CVP-MVSNet 的核心洞察在于：**深度采样间隔与图像分辨率存在直接关联**——过密的采样无法提供额外的区分性信息，因为投影到源视图的特征点过于接近（像素偏移 < 0.5）会导致特征高度相似（Figure 4）。因此，该方法根据目标像素偏移（如 0.5 像素）确定深度采样间隔，搜索范围由粗深度投影动态决定（Section 3.3）。消融实验证实，对应 0.5 像素或 1 像素偏移的采样间隔效果最优，过小（0.25 像素）或过大（2 像素）均导致性能下降（Table 4b）。

### 3. 特征提取方式：从高分辨率特征到图像金字塔轻量特征

基线方法通常使用高分辨率图像提取多尺度特征，即使最终仅输出低分辨率深度图。CVP-MVSNet 则直接在图像金字塔的每一层上使用轻量 CNN（9 个卷积层 + Leaky-ReLU）提取 16 维紧凑特征，避免了对低分辨率输出使用高分辨率特征的冗余计算（Section 3.1）。这一设计与其他两个改变协同作用，使得该方法在 DTU 数据集上以 0.37 秒的运行时间完成推断，相比 Point-MVSNet 的 2.03 秒快了约 6 倍（Table 2）。

### 创新机制的内在联系

上述三个改变并非孤立存在，而是通过代价体金字塔的粗到细结构形成因果链条：图像金字塔的轻量特征提取降低了每一层的计算基数；分辨率自适应的深度采样策略确保了每一层代价体仅包含具有区分性的深度假设；局部部分代价体的构建则将计算和内存开销集中在最需要细化的区域。三者共同实现了精度与效率的双重提升——在 DTU 数据集上取得整体误差 0.351 mm，优于所有对比的深度学习方法（Table 1）；在 Tanks and Temples 基准上平均 F-score 达到 54.03，显著超过 Point-MVSNet 的 48.27（Table 3）。

## 整体框架

CVP-MVSNet 的整体设计围绕一个核心洞察展开：**深度采样间隔与图像分辨率存在直接关联**——过密的采样无法提供额外的区分性信息，反而造成计算冗余。基于此，方法构建了一个**代价体金字塔**，以粗到细的方式迭代优化深度残差，替代传统固定分辨率的单一代价体。

### 输入与预处理

给定一张参考图像 $\mathbf{I}_0 \in \mathbb{R}^{H \times W}$ 和 $N$ 张邻近源图像 $\{\mathbf{I}_i\}_{i=1}^N$，以及所有视图的相机参数 $\{\mathbf{K}_i, \mathbf{R}_i, \mathbf{t}_i\}_{i=0}^N$，方法首先将参考图像和源图像降采样，构建一个 **$(L+1)$ 级图像金字塔**（Figure 2）。这一设计使得后续所有操作都在与输出分辨率匹配的尺度上进行，避免了为低分辨率深度图提取高分辨率特征的不必要开销。

### 模块关系与数据流

整个 pipeline 由五个核心模块串联而成，数据自底向上流动：

1. **特征提取网络**：一个轻量 CNN（9 个卷积层 + Leaky-ReLU）对图像金字塔所有层级的所有视图提取 16 维紧凑特征。同一网络在所有层级和视图间共享权重，保证了多尺度特征的一致性。

2. **粗代价体构建**：在最粗分辨率层级 $L$ 上，在完整深度范围内均匀采样 $M$ 个前向平行平面（$M=48$），通过可微单应性变换将源视图特征扭曲到参考视图，计算多视图方差作为匹配代价，形成完整的粗代价体 $\mathbf{C}^L$。

3. **深度残差代价体构建**：基于上采样后的当前深度估计，在每个像素的局部搜索范围内投影假设 3D 点，仅构建**局部部分代价体**用于残差推理。这是方法的核心创新——搜索范围由粗深度投影动态决定，采样间隔由目标像素偏移（如 0.5 像素）确定，确保每个采样点携带可区分的信息（Figure 4）。

4. **多尺度 3D CNN 正则化**：在代价体金字塔的每一层应用多尺度 3D 卷积，聚合上下文信息并输出概率体 $\mathbf{P}^l$。

5. **深度图回归**：通过 soft-argmax 从概率体中获得深度/残差的期望值。最粗层直接回归绝对深度，后续层级在上采样深度基础上叠加残差期望，迭代融合得到最终高分辨率深度图 $\mathbf{D}^0$。

### 关键设计决策

方法在**两级金字塔结构**与**0.5 像素深度偏移间隔**的组合下取得最佳重建质量（Table 4）。相比 Point-MVSNet 的点云操作范式，CVP-MVSNet 在规则 3D 代价体上进行多尺度卷积，实现了更紧凑、更快速且精度更高的深度推断。在输出相同尺寸深度图时，GPU 内存消耗和运行时间均降低约 6 倍（Table 2），同时 DTU 整体误差降至 0.351 mm（Table 1）。

## 核心模块与公式推导

### 3.1 特征提取网络

整个流水线始于对输入图像构建 **(L+1) 级图像金字塔**。所有参考视图与源视图均被降采样，形成多尺度输入。对金字塔中每一层级的每一幅图像，应用一个轻量级 CNN 提取特征：

- **网络结构**：由 **9 个卷积层** 组成，每个卷积层后接 Leaky-ReLU 激活函数。
- **输出特征**：所有层级、所有视图均输出 **16 维** 紧凑特征图，避免在高分辨率层级上使用高维特征带来的计算冗余。
- **设计意图**：直接在图像金字塔的每一层上提取特征，而非像传统方法那样用高分辨率图像提取特征后再降采样至低分辨率深度图，从而从源头降低计算量。

### 3.2 代价体金字塔构建

代价体金字塔是方法的核心，分为两个阶段：**粗级代价体构建** 与 **深度残差代价体构建**。

#### 3.2.1 粗级代价体构建

在最粗分辨率层级 $L$ 上，对整个深度范围均匀采样 $M$ 个前向平行平面作为深度假设。对于每个深度假设 $d$，通过可微单应性将参考视图的像素映射到各源视图：

$$ \mathbf{\dot{H}}_i(d) = \mathbf{K}_i^L \mathbf{R}_i \left(\mathbf{I} - \frac{(\mathbf{t}_0 - \mathbf{t}_i) \mathbf{n}_0^T}{d}\right) \mathbf{R}_0^{-1} (\mathbf{K}_0^L)^{-1} $$

其中 $\mathbf{K}_i^L$ 为第 $i$ 个视图在层级 $L$ 的内参矩阵，$\mathbf{R}_i$ 和 $\mathbf{t}_i$ 为旋转矩阵与平移向量，$\mathbf{n}_0$ 为参考视图的主轴方向。该变换将深度 $d$ 下的像素从参考视图齐次映射到第 $i$ 个源视图。

获取各视图扭曲后的特征后，以**多视图方差**作为匹配代价：

$$ \mathbf{C}_d^L = \frac{1}{(N+1)} \sum_{i=0}^{N} (\tilde{\mathbf{f}}_{i,d}^L - \bar{\mathbf{f}}_d^L)^2 $$

其中 $\tilde{\mathbf{f}}_{i,d}^L$ 为第 $i$ 个视图在深度 $d$ 处扭曲后的特征，$\bar{\mathbf{f}}_d^L$ 为所有视图特征的均值。方差代价体 $\mathbf{C}_d^L$ 编码了每个像素在每个深度假设下的多视图一致性。

#### 3.2.2 深度残差代价体构建

在更精细的层级 $l$（$l < L$），不再对整个深度范围采样，而是基于上一层的深度估计 $\mathbf{D}_{\uparrow}^{l+1}(\mathbf{p})$ 定义**局部搜索范围**。对于像素 $\mathbf{p}$，其深度残差假设为 $r_{\mathbf{p}} = m \cdot \Delta d_{\mathbf{p}}^l$，其中 $\Delta d_{\mathbf{p}}^l = s_{\mathbf{p}} / M$，$s_{\mathbf{p}}$ 为该像素的深度搜索范围。

将深度残差假设对应的 3D 点从参考视图投影到第 $i$ 个源视图：

$$ \lambda_i \mathbf{x}_i' = \mathbf{K}_i^l \left( \mathbf{R}_i \mathbf{R}_0^{-1} \left( (\mathbf{K}_0^l)^{-1} (u,v,1)^T (d_{\mathbf{p}} + m\Delta d_{\mathbf{p}}) - \mathbf{t}_0 \right) + \mathbf{t}_i \right) $$

其中 $d_{\mathbf{p}}$ 为当前深度估计，$m\Delta d_{\mathbf{p}}$ 为残差偏移量。该投影仅在局部范围内获取源视图特征，形成**部分代价体**——这是降低内存与计算量的关键设计。

### 3.3 多尺度 3D CNN 正则化与深度回归

在代价体金字塔的每一层，应用**多尺度 3D 卷积网络**对代价体进行正则化，聚合上下文信息并输出概率体 $\mathbf{P}$。

**粗级深度估计**通过 soft-argmax 获得：

$$ \mathbf{D}^L(\mathbf{p}) = \sum_{m=0}^{M-1} d \, \mathbf{P}_{\mathbf{p}}^L(d) $$

即对所有深度假设 $d$ 按其概率加权求和，得到连续深度值。

**深度残差精细化**则在上采样深度基础上叠加残差期望：

$$ \mathbf{D}^l(\mathbf{p}) = \mathbf{D}_{\uparrow}^{l+1}(\mathbf{p}) + \sum_{m=-M/2}^{(M-2)/2} r_{\mathbf{p}} \, \mathbf{P}_{\mathbf{p}}^l(r_{\mathbf{p}}) $$

其中 $\mathbf{D}_{\uparrow}^{l+1}$ 为从更粗层级上采样后的深度图，第二项为深度残差 $r_{\mathbf{p}}$ 的期望值。通过逐层迭代，最终输出与输入图像分辨率一致的高质量深度图 $\mathbf{D}^0$。

### 3.4 损失函数

训练损失为所有金字塔层级上估计深度与真实深度的 L1 距离之和：

$$ \text{Loss} = \sum_{l=0}^{L} \sum_{\mathbf{p} \in \Omega} \|\mathbf{D}_{\text{GT}}^l(\mathbf{p}) - \mathbf{D}^l(\mathbf{p})\|_1 $$

其中 $\Omega$ 为有效像素集合，$\mathbf{D}_{\text{GT}}^l$ 为对应层级的真实深度图。

## 实验与分析

### 定量重建精度

**DTU数据集。** CVP-MVSNet在DTU基准上取得了整体误差0.351 mm，优于所有对比的深度学习方法，包括直接基线**Point-MVSNet**（Chen et al., ICCV 2019）的0.376 mm（Table 1）。在分项指标上，本方法在平均完整度（Mean Completeness）和整体重建质量上排名第一，平均准确度（Mean Accuracy）排名第二。


![[assets/figures/papers/paper_list_l10_https_arxiv_org_abs_1912_08329/figures/005_Table_1.jpg]]
*Table 1: Quantitative results of reconstruction quality on DTU dataset (lower is better). Our method outperforms all methods on Mean Completeness and Overall reconstruction quality and achieved second best on Mean Accuracy*

**Tanks and Temples基准。** 在泛化能力测试中，CVP-MVSNet的平均F-score达到54.03，显著超过Point-MVSNet的48.27，提升幅度约5.76个点（Table 3）。与基于逐块匹配置信度聚合的**P-MVSNet**（Luo et al., ICCV 2019）相比，本方法同样具有竞争力。

### 效率对比

Table 2给出了在相同硬件环境（NVIDIA TITAN RTX）下运行官方评估代码的效率对比。当输出相同尺寸深度图（640）时，CVP-MVSNet的推理时间为0.37秒，GPU内存占用1416 MB；而Point-MVSNet分别为2.03秒和8989 MB——本方法在保持相近精度的同时，速度提升约6倍，内存需求降低约6倍。当使用相同输入图像尺寸时，CVP-MVSNet以1.72秒的运行时间和8795 MB的GPU内存取得了最优重建质量（0.351 mm），而Point-MVSNet需3.04秒和13081 MB。


![[assets/figures/papers/paper_list_l10_https_arxiv_org_abs_1912_08329/figures/008_Table_2.jpg]]
*Table 2: Comparison of reconstruction quality, GPU memory usage and runtime on DTU dataset for different input sizes. GPU memory usage and runtime are obtained by running the official evaluation code of baselines on a same machine with a NVIDIA TITAN RTX graphics card. For the same size of depth maps (Ours-640, Ours-800) and a performance similar to Point-MVSNet [5], our method is 6 times faster and consumes 6 times smaller GPU memory. For the same size of input images (Ours), our method achieves the best reconstruction with the shortest time and a reasonable GPU memory usage. Table 3: Performance on Tanks and Temples [21] on November 12, 2019. Our results outperform Point-MVSNet [5], which is the s...*

### 消融实验

Table 4报告了关键设计参数对DTU数据集上整体误差的影响：


![[assets/figures/papers/paper_list_l10_https_arxiv_org_abs_1912_08329/figures/010_Table_4.jpg]]
*Table 4: Parameter sensitivity on DTU dataset. a) Accuracy as a function of the number of pyramid levels. b) Accuracy as a function of the interval setting*

- **金字塔层数（Table 4a）：** 两级金字塔结构取得最佳重建质量（0.351 mm）。当层数增加到三层或更多时，性能反而下降，表明过深的金字塔可能引入误差累积。
- **深度采样间隔（Table 4b）：** 深度残差搜索中对应0.5像素或1像素偏移的采样间隔效果最优（均为0.351 mm）。过小的间隔（0.25像素）因采样点过于密集、特征区分度不足而导致性能下降；过大的间隔（2像素）则因搜索粒度过粗而损失精度。这一结果直接验证了Figure 4所揭示的核心机制：适当的深度采样使投影点携带可区分的特征信息，而过密采样产生的邻近投影点特征高度相似，无法提供额外判别力。


![[assets/figures/papers/paper_list_l10_https_arxiv_org_abs_1912_08329/figures/004_Figure_4.jpg]]
*Figure 4: Interpolation of two sampling points from four feature points in source view. (a) Densely sampled depth will result in very close (\< 0.5 pixel) locations which have similar feature. (b) Points projected using appropriate depth sampling carry distinguishable information*

### 定性结果

Figure 5展示了DTU扫描9的点云和法线图对比。蓝色矩形区域表明，CVP-MVSNet的重建完整度优于Point-MVSNet；橙色矩形区域的局部法线图进一步显示，本方法在保持表面平滑的同时保留了更多高频细节。Tanks and Temples数据集上的定性重建结果见Figure 7。


![[assets/figures/papers/paper_list_l10_https_arxiv_org_abs_1912_08329/figures/007_Figure_5.jpg]]
*Figure 5: Qualitative results of scan 9 of DTU dataset. The upper row shows the point clouds and the bottom row shows the normal map corresponding to the orange rectangle. As highlighted in the blue rectangle, the completeness of our results is better than those provided by Point-MVSNet[5]. The normal map (orange rectangle) further shows that our results are smoother on surfaces while maintaining more high-frequency details*

![[assets/figures/papers/paper_list_l10_https_arxiv_org_abs_1912_08329/figures/011_Figure_7.jpg]]
*Figure 7: Point cloud reconstruction of Tanks and Temples dataset [21]. Best viewed on screen. (a)*

### 失败模式与局限

当前分析材料中未提供明确的失败案例或系统性局限讨论。从消融实验可间接推断：本方法对金字塔层数和深度采样间隔较为敏感，在实际部署时需针对具体场景调优这两个超参数。此外，论文提出的开放问题是将代价体金字塔集成到可学习的结构从运动框架中，暗示当前方法仍依赖已知的相机参数，尚未形成端到端的完整三维重建管线。

### 补充图表

![[assets/figures/papers/paper_list_l10_https_arxiv_org_abs_1912_08329/figures/001_Figure_1.jpg]]
*Figure 1: Point clouds reconstructed by state-of-the-art methods [5, 43] and our CVP-MVSNet. Best viewed on screen*

![[assets/figures/papers/paper_list_l10_https_arxiv_org_abs_1912_08329/figures/006_Figure.jpg]]
*Figure: R-MVSNet [43] Point-MVSNet [5] Ours Ground truth*

![[assets/figures/papers/paper_list_l10_https_arxiv_org_abs_1912_08329/figures/009_Figure_6.jpg]]
*Figure 6: Additional results from DTU dataset. Best viewed on screen. (a) Train*

## 方法谱系与知识库定位

### 1. 问题定位与核心瓶颈

CVP-MVSNet 直面的核心瓶颈是：现有学习型多视图立体（MVS）方法在处理高分辨率图像时，面临**内存需求大**与**运行速度慢**的双重困境，严重制约了实际应用中的精度-效率平衡。

- **MVSNet**（Yao et al., ECCV 2018）开创性地将可微单应性变换与3D CNN引入MVS，但其在**单一固定分辨率**下构建完整代价体的策略，导致内存需求与分辨率立方成正比，难以扩展到高分辨率场景。
- **R-MVSNet**（Yao et al., CVPR 2019）通过GRU顺序处理代价体来降低内存占用，但代价是**显著增加的运行时间**，未能从根本上解决效率问题。
- **Point-MVSNet**（Chen et al., ICCV 2019）引入基于点云的粗到细深度优化，是本文直接对比的核心基线。该方法虽然在精度上表现优异，但其点云操作的计算开销仍然较大。

CVP-MVSNet 的因果调节变量在于：**以代价体金字塔替代固定分辨率单一代价体**，并通过粗到细的方式迭代优化深度残差。这一设计的核心洞察是：**深度采样间隔与图像分辨率存在直接关联**——过密的采样无法提供额外的区分性信息（Figure 4）；采用金字塔结构在每一层仅构建局部部分代价体，结合多尺度3D CNN正则化，可以在显著降低计算和内存开销的同时提升深度估计精度。

### 2. 关键方法差异与创新要素

CVP-MVSNet 在三个关键维度上对基线方法进行了结构性改进：

| 设计维度 | 基线方法（MVSNet / Point-MVSNet） | CVP-MVSNet |
|----------|-----------------------------------|------------|
| **代价体构建** | 单一固定分辨率下构建完整代价体 | 构建代价体金字塔，从最粗分辨率开始，逐层构建局部部分代价体以预测深度残差 |
| **深度采样策略** | 固定数量的均匀采样，不考虑采样间隔与图像分辨率的关联 | 根据目标像素偏移（如0.5像素）确定深度采样间隔，搜索范围由粗深度投影动态决定 |
| **特征提取** | 使用高分辨率图像提取多尺度特征，即使最终输出低分辨率深度图 | 直接在图像金字塔的每一层上使用轻量CNN（9层卷积+Leaky-ReLU）提取16维紧凑特征 |

核心创新机制可概括为：

1. **代价体金字塔构建**（Section 3.2）：在最粗分辨率层级上，均匀采样 $M$ 个前向平行平面，通过可微单应性变换（Eq. 1）将参考视图特征映射到源视图，并以多视图方差（Eq. 2）作为匹配代价。在后续层级，基于上采样后的当前深度估计，在局部搜索范围内投影假设3D点（Eq. 3），生成**部分代价体**用于残差推理。

2. **深度采样与图像分辨率的理论关联**（Section 3.3, Figure 4）：论文论证了深度采样间隔应由源视图中的像素偏移量决定。过密的深度采样（对应<0.5像素偏移）导致投影点特征高度相似，无法提供有效区分信息；适当的采样间隔（对应0.5-1像素偏移）则能携带可区分的特征信息。

3. **多尺度3D CNN正则化与迭代深度回归**（Section 3.3）：在代价体金字塔的每一层应用多尺度3D卷积聚合上下文信息，通过soft-argmax（Eq. 4-5）从概率体中获得深度/残差的期望值，迭代融合得到最终高分辨率深度图。

### 3. 适用边界与局限性

基于论文提供的实验证据与分析，CVP-MVSNet 的适用边界可归纳如下：

- **金字塔层数**：消融实验（Table 4a）表明，两级金字塔结构获得最佳重建质量（Overall误差0.351 mm），超过三层或更多层配置。这意味着该方法在**适度的尺度跨度**内效果最优，过深的金字塔可能导致误差累积或信息损失。
- **深度采样间隔**：消融实验（Table 4b）显示，对应0.5像素或1像素偏移的采样间隔效果最优；过小（0.25像素）或过大（2像素）的间隔均导致性能下降。这验证了“过密采样无益、过疏采样信息不足”的核心论点。
- **计算效率边界**：在输出相同尺寸深度图（640）时，CVP-MVSNet 相比 Point-MVSNet 实现了约**6倍的GPU内存降低**（1416 MB vs 8989 MB）和约**6倍的运行时间加速**（0.37 s vs 2.03 s）（Table 2）。但在处理原始输入尺寸时，内存占用仍达到8795 MB，表明方法在处理极高分辨率输入时仍存在一定内存压力。
- **泛化能力**：在 Tanks and Temples 基准上，CVP-MVSNet 的 Mean F-score 达到54.03，显著超过 Point-MVSNet 的48.27（Table 3），验证了方法在室外大规模场景下的泛化能力。但与 **P-MVSNet**（Luo et al., ICCV 2019）相比仍有一定差距，说明基于逐块匹配置信度聚合的方法在特定场景下可能更具优势。

论文未明确讨论方法的失败模式或局限性，但可从实验设置推断：该方法依赖于**已知的相机参数**和**预定义的深度范围**，在相机参数估计不准确或深度范围设置不合理的场景下，性能可能受到影响。

### 4. 开放问题与后续发展

论文明确指出了一个开放问题：**如何将代价体金字塔集成到可学习的结构从运动（Structure-from-Motion）框架中**，以进一步降低整体三维重建流程的内存需求。这一方向指向了端到端的联合优化——将特征提取、匹配、深度估计和相机位姿估计统一到一个内存高效的金字塔框架下。

从方法谱系的角度看，CVP-MVSNet 的代价体金字塔思想为后续工作提供了可扩展的范式：将“固定分辨率全局代价体”替换为“多尺度局部代价体”的策略，可以自然地推广到其他基于代价体的MVS方法中，在保持或提升精度的同时显著降低计算开销。

## 原文 PDF

![[paperPDFs/CVPR_2020/Cost_Volume_Pyramid_Based_Depth_Inference_for_Multi_View_Stereo.pdf]]
