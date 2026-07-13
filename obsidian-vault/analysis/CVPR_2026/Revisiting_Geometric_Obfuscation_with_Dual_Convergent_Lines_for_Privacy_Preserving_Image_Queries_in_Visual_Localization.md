---
title: Revisiting Geometric Obfuscation with Dual Convergent Lines for Privacy-Preserving Image Queries in Visual Localization
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/Revisiting_Geometric_Obfuscation_with_Dual_Convergent_Lines_for_Privacy_Preserving_Image_Queries_in_Visual_Localization.pdf
project_link: null
code_link: null
aliases:
- DCLD
- RGODCLPPIQVL
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/benchmarks_datasets_evaluation
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: 混淆线的生成方式：将图像垂直中线分割为两个区域，每个关键点与其所在区域的固定锚点连接，使相邻线要么交汇于同一锚点，要么在分区边界附近趋于平行。
primary_logic: 通过双锚点设计，故意将点恢复攻击的优化问题变为病态：当邻居线来自同一锚点时，最优解平凡收敛到锚点；当邻居线来自不同锚点且位于分区边界时，线近乎平行，导致解数值不稳定且方差极大，从而彻底破坏关键点恢复。
claims:
- 合成实验中，1500个均匀分布的关键点经过DCL混淆后，攻击恢复误差低于30像素的仅8个点。
- 在7Scenes数据集上，DCL的恢复点平均几何误差为330.4像素，远高于随机线的6.137像素。
- 通过命题1和推论1.1证明，当线趋于平行时，加权平均参数变得数值不稳定，导致恢复失败。
- 7Scenes 上 erecon (↑, pixels) = 330.4
---

# Revisiting Geometric Obfuscation with Dual Convergent Lines for Privacy-Preserving Image Queries in Visual Localization

> [!tip] 核心洞察
> 通过双锚点设计，故意将点恢复攻击的优化问题变为病态：当邻居线来自同一锚点时，最优解平凡收敛到锚点；当邻居线来自不同锚点且位于分区边界时，线近乎平行，导致解数值不稳定且方差极大，从而彻底破坏关键点恢复。

| 字段 | 内容 |
|------|------|
| 中文题名 | 面向视觉定位中隐私保护图像查询的双收敛线几何混淆方法再探 |
| 英文题名 | Revisiting Geometric Obfuscation with Dual Convergent Lines for Privacy-Preserving Image Queries in Visual Localization |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2604.22310) |
| Topic | #topic/vision_multimodal_applications #topic/benchmarks_datasets_evaluation #topic/vision_multimodal_applications/image_and_video_generation |
| Method | Dual Convergent Lines (DCL) |
| Dataset | 7Scenes, Aachen Day-Night, Cambridge |

> [!tip] 效果简介
> - 7Scenes 上，erecon (↑, pixels) 330.4 vs 6.137 (Random Lines) (+324.3)。
> - Aachen Day-Night 上，LPIPS (↑) 0.736 vs 0.476 (Random Lines) (+0.260)。
> - Cambridge 上，Median position error (cm) / rotation error (°) 22.5 / 0.50 vs 12 / 0.2 (HLoc SP+NN) (+10.5 cm, +0.30°)。

## 概要

视觉定位允许用户上传查询图像以估计6-DoF相机位姿，但原始图像或关键点坐标的暴露引发了严重的隐私风险。现有的几何混淆方法——例如**Random Lines**（每条关键点被一条通过该点的随机方向直线替换）——旨在隐藏精确位置，然而近期攻击表明，混淆后的线邻居在空间上仍近似包围原始点，攻击者可通过最小化目标点到邻居线距离的平方和（式(3)）近似恢复关键点位置，进而成功反演出查询图像。

本文重新审视几何混淆的设计空间，提出**双收敛线（Dual Convergent Lines, DCL）**方法。核心思路是：将图像沿垂直中线划分为左右两个区域，并在图像中心上下两端设置两个固定锚点；每个关键点根据其所在区域连接到对应锚点，生成混淆线。这一设计使点恢复攻击的优化问题陷入两种失败模式：当邻居线来自同一锚点时，最优解平凡收敛至锚点，而非原始关键点；当邻居线来自不同锚点且位于分区边界附近时，线近乎平行，导致恢复解的数值不稳定且方差极大。

实验表明，DCL在抵御几何恢复攻击方面显著优于Random Lines和坐标排列等基线：在7Scenes数据集上，攻击恢复点的平均几何误差从Random Lines的6.14像素飙升至330.4像素（Table 2）；合成实验中，1500个均匀分布关键点经DCL混淆后，仅8个点的恢复误差低于30像素（Figure 4）。在定位性能方面，DCL在Cambridge数据集上实现22.5 cm / 0.50°的中位误差（Table 3），在Aachen Day-Night数据集上保持实用级别的召回率（Table 4），以可控的精度代价换取了抗隐私攻击能力的质变。方法对定位管线无侵入性，可与现有视觉定位框架（如HLoc）无缝集成。

视觉定位（visual localization）旨在从单幅查询图像中恢复6-DoF相机位姿，是增强现实、自动驾驶和机器人导航等应用的基础能力。现代视觉定位流程通常包含两个阶段：首先在服务器端构建场景的3D地图（稀疏SfM点云），然后在查询时提取2D关键点与3D点进行匹配，最后通过PnP求解器估计位姿。这一范式要求将查询图像的关键点信息上传至服务器，从而引发了严重的隐私泄露风险——服务器可直接获取图像中的几何结构，甚至通过反演攻击重建出可识别的场景内容。

为应对这一威胁，研究者提出了一系列几何混淆方法，其核心思路是在客户端对关键点进行变换后再上传。代表性方案包括**Random Lines**（用通过关键点的随机方向直线替代点坐标）和**Coordinate Permutation**（通过随机配对关键点并交换坐标分量实现混淆）。这些方法旨在隐藏精确的关键点位置，同时保留足够的几何约束以支持位姿求解。

然而，近期研究表明，现有混淆方案存在根本性脆弱性。以Random Lines为例，其生成的每条混淆线虽然不直接暴露关键点坐标，但混淆后的线邻居在空间上仍近似包围原始点——攻击者可通过最小化目标线上点到其邻居线距离的平方和来近似恢复原始关键点位置（即几何恢复攻击）。这一攻击在真实数据集上取得了令人担忧的成功：恢复点的平均几何误差仅约6像素，使得后续的图像反演能够重建出高度可辨识的场景内容。

这一瓶颈的深层原因在于：Random Lines的线方向服从均匀分布，导致恢复优化问题的解在统计意义上收敛到原始关键点。换言之，现有混淆方案并未从根本上破坏攻击者可利用的几何线索结构，而只是增加了一层可被优化穿透的薄幕。

本文的动机由此明确：**能否设计一种新的线混淆策略，使得即使攻击者掌握了完美的邻居识别能力（oracle设置），点恢复攻击也会因优化问题的病态性而必然失败？** 这要求混淆线的生成方式必须系统性地破坏恢复优化问题的适定性，而非仅仅增加噪声。

## 核心方法与创新机理

DCL 的核心创新在于**通过双锚点空间分区，将几何混淆从“随机扰动”升级为“病态优化陷阱”**。与 Random Lines 等基线方法仅通过随机定向直线隐藏关键点位置不同，DCL 引入了一个精心设计的线生成机制，使攻击者面临的最小二乘恢复问题在数学上变得数值不稳定或平凡退化。

具体而言，DCL 在以下两个关键设计槽位上与基线形成根本差异：

### 1. 线生成方式：从随机定向到锚点绑定

Random Lines 为每个关键点生成一条通过该点的随机方向直线。这种设计虽然隐藏了点坐标，但混淆后的线邻居在空间上仍近似包围原始点，为攻击者提供了可恢复的几何线索——攻击者只需最小化目标点到邻居线距离的平方和，即可近似恢复原始关键点位置。

DCL 彻底改变了线的生成逻辑：每条线不再随机定向，而是**从图像垂直中线的上下两个固定锚点之一发出**，关键点位于线的中间某处。形式上，给定图像宽度 $W$ 和高度 $H$，两个锚点定义为：

$$\mathbf{a}_1 = \left( \frac{W}{2}, H \right), \quad \mathbf{a}_2 = \left( \frac{W}{2}, 0 \right)$$

每个关键点 $\mathbf{x}_i$ 根据其所在区域连接到对应锚点：

$$\mathbf{l}_i = \begin{cases} \mathrm{line}(\mathbf{x}_i, \mathbf{a}_1), & \text{if } \mathbf{x}_i \in \mathcal{R}_1 \\ \mathrm{line}(\mathbf{x}_i, \mathbf{a}_2), & \text{if } \mathbf{x}_i \in \mathcal{R}_2 \end{cases}$$

这一改变使得相邻混淆线要么交汇于同一锚点，要么在分区边界附近趋于平行，从而系统性地破坏了攻击优化问题的适定性。

### 2. 图像空间划分：从无分区到垂直中线分区

Random Lines 和 Coordinate Permutation 等方法对图像空间不做任何划分，所有关键点采用统一的混淆策略。DCL 则沿垂直中线将图像分成左右两个区域 $\mathcal{R}_1$ 和 $\mathcal{R}_2$，每个区域的关键点连接到不同的锚点。这一分区策略是触发两种攻击失败模式的关键：

- **模式一（锚点内收敛）**：当目标线的邻居线均来自同一锚点时，攻击优化问题的最优解平凡收敛到锚点位置，而非原始关键点位置。
- **模式二（锚点间不稳定）**：当邻居线来自不同锚点且位于分区边界附近时，目标线与邻居线近乎平行。根据 **Proposition 1** 和 **Corollary 1.1**，恢复点沿线的参数是各邻居线交点参数的加权平均，而权重仅由两线夹角的正弦平方决定：$w_{i,j} = \sin^2(\theta_{i,j})$。当线趋于平行（$\theta_{i,j} \to 0$），权重趋近于零，导致数值不稳定且方差极大，恢复点大幅偏离真实位置。

合成实验验证了这一设计的有效性：在 $640 \times 480$ 分辨率下对 1500 个均匀分布关键点进行 DCL 混淆后，攻击恢复误差低于 30 像素的仅 8 个点（Figure 4）。在 7Scenes 数据集上，DCL 的恢复点平均几何误差高达 **330.4 像素**，远高于 Random Lines 的 **6.137 像素**（Table 2），充分证明了双锚点分区策略对几何恢复攻击的破坏力。

DCL 的整体 pipeline 由四个核心模块串联构成，形成从查询图像输入到 6-DoF 相机位姿输出的完整流程。

**特征提取**阶段，客户端使用 **SuperPoint**（DeTone et al., CVPRW 2018）从查询图像中提取关键点位置 $\mathbf{x}_i$ 及其对应的局部描述子。这一步与标准视觉定位流程一致，不引入额外计算负担。

**DCL 线生成**是核心混淆模块。图像首先沿垂直中线被划分为左右两个互斥区域 $\mathcal{R}_1$ 和 $\mathcal{R}_2$；两个固定锚点 $\mathbf{a}_1$、$\mathbf{a}_2$ 分别置于该中线顶端和底端。对每个关键点 $\mathbf{x}_i$，根据其所属区域，生成一条从对应锚点出发并穿过该关键点的直线 $\mathbf{l}_i$：

$$
\mathbf{l}_i = \begin{cases} \mathrm{line}(\mathbf{x}_i, \mathbf{a}_1), & \text{if } \mathbf{x}_i \in \mathcal{R}_1 \\ \mathrm{line}(\mathbf{x}_i, \mathbf{a}_2), & \text{if } \mathbf{x}_i \in \mathcal{R}_2 \end{cases}
$$

最终仅将混淆后的线集合（而非原始关键点坐标）发送至服务器。这一设计的关键在于：相邻线要么交汇于同一锚点，要么在分区边界附近趋于平行，从而为后续攻击构造病态优化问题。

**图像检索与 2D-3D 匹配**在服务器端完成。首先基于全局描述子检索候选数据库图像，随后利用最近邻匹配在混淆线与 3D 地图点之间建立对应关系。此处的匹配对象是线而非点，但通过 l6P 约束方程将线反投影为 3D 平面，使匹配依然可解。

**位姿估计**采用 **l6P 最小求解器**在 **Lo-RANSAC** 框架中估计 6-DoF 位姿，并通过 Levenberg-Marquardt 进行非线性优化。核心约束方程为：

$$
\mathbf{n}_i^{\top} (\mathbf{R} \mathbf{X}_i + \mathbf{t}) = 0
$$

其中 $\mathbf{n}_i$ 为由 2D 线反投影得到的 3D 平面法向量，$\mathbf{R} \mathbf{X}_i + \mathbf{t}$ 为对应的 3D 地图点在相机坐标系下的坐标。为防止退化配置（所有采样线来自同一锚点），RANSAC 最小集强制包含来自两个锚点的线，并通过监控三线交点是否重合来高效判别。

整个 pipeline 的输入输出流可概括为：**查询图像 → SuperPoint 关键点与描述子 → DCL 双锚点线混淆 → 线集合传输 → 服务器端线-点匹配 → l6P + Lo-RANSAC 位姿估计 → 6-DoF 相机位姿**。该框架在保持与现有视觉定位系统兼容性的同时，通过双锚点设计将点恢复攻击的优化问题转化为病态问题，实现了隐私保护与定位精度的折衷。

### 4.1 DCL 线生成模块

DCL 的核心操作是将查询图像中的每个关键点替换为一条从固定锚点发出的直线，从而隐藏点的精确位置。具体流程如下：

**空间分区**：首先沿垂直中线将图像空间划分为两个互斥区域 $\mathcal{R}_1$ 和 $\mathcal{R}_2$。对于宽度为 $W$、高度为 $H$ 的图像，分区边界位于 $u = W/2$ 处。

**锚点定义**：在图像中心线的顶端和底端分别定义两个固定锚点 $\mathbf{a}_1$ 和 $\mathbf{a}_2$。默认配置下，锚点距离图像中心均为 $H$（即位于图像上下边界之外），这一距离可通过超参数调节。

**线生成规则**：对于每个关键点 $\mathbf{x}_i$，根据其所属区域将其连接到对应的锚点，生成混淆线 $\mathbf{l}_i$：

$$
\mathbf{l}_i = \begin{cases}
\mathrm{line}(\mathbf{x}_i, \mathbf{a}_1), & \text{if } \mathbf{x}_i \in \mathcal{R}_1 \\
\mathrm{line}(\mathbf{x}_i, \mathbf{a}_2), & \text{if } \mathbf{x}_i \in \mathcal{R}_2
\end{cases}
$$

其中 $\mathrm{line}(\mathbf{x}_i, \mathbf{a}_j)$ 表示通过点 $\mathbf{x}_i$ 和锚点 $\mathbf{a}_j$ 的直线。最终，原始关键点坐标被丢弃，仅将线的参数（方向向量和锚点标识）发送至服务器。

### 4.2 点恢复攻击的数学分析

**攻击模型**：给定一条目标线 $\mathbf{l}_i$ 及其邻居线集合 $\mathcal{N}(\mathbf{l}_i)$，攻击者通过最小化目标线上的候选点 $\hat{\mathbf{x}}_i$ 到各邻居线距离的平方和来恢复原始关键点位置：

$$
f(\hat{\mathbf{x}}_i) = \sum_{\mathbf{l}_j \in \mathcal{N}(\mathbf{l}_i)} d(\mathbf{l}_j, \hat{\mathbf{x}}_i)^2
$$

**命题 1（加权平均形式）**：该优化问题的最优解可表示为沿目标线 $\mathbf{l}_i$ 的参数 $t_i^*$，它是各邻居线与目标线交点参数 $t_{i,j}^*$ 的加权平均：

$$
t_i^* = \frac{\sum_j (w_{i,j} \, t_{i,j}^*)}{\sum_j w_{i,j}}
$$

**推论 1.1（权重仅由夹角决定）**：每条邻居线的权重 $w_{i,j}$ 仅由目标线方向 $\mathbf{v}_i$ 与邻居线方向 $\mathbf{v}_j$ 之间夹角 $\theta_{i,j}$ 的正弦平方决定：

$$
w_{i,j} = \|\mathbf{v}_i \times \mathbf{v}_j\|^2 = \sin^2(\theta_{i,j})
$$

**DCL 的防御机制**：上述分析揭示了 DCL 使攻击陷入两种失败模式的核心原理：

- **模式一（锚点内收敛）**：当邻居线均来自同一锚点时，所有线交汇于该锚点，使得 $t_{i,j}^*$ 全部等于锚点在 $\mathbf{l}_i$ 上的投影参数。此时最优解平凡地收敛到锚点位置，而非原始关键点。

- **模式二（锚点间不稳定）**：当邻居线来自不同锚点且关键点位于分区边界附近时，目标线与邻居线近乎平行（$\theta_{i,j} \to 0$），导致权重 $w_{i,j} \to 0$。此时加权平均的数值稳定性急剧恶化，恢复点的方差极大，优化结果不可靠。

### 4.3 相机位姿估计模块

服务器端使用混淆线进行 6-DoF 位姿估计。给定 2D 线 $\mathbf{l}_i$ 及其对应的 3D 点 $\mathbf{X}_i$，将线反投影得到 3D 平面，其法向量 $\mathbf{n}_i$ 应与变换到相机坐标系下的 3D 点正交，构成 l6P 约束：

$$
\mathbf{n}_i^{\top} (\mathbf{R} \mathbf{X}_i + \mathbf{t}) = 0
$$

其中 $\mathbf{R} \in SO(3)$ 为旋转矩阵，$\mathbf{t} \in \mathbb{R}^3$ 为平移向量。该约束是线-点对应下的最小参数化形式，每条对应提供 1 个约束方程，因此最少需要 6 条线-点对应来求解位姿。

**退化处理**：当最小求解器采样的三条线全部来自同一锚点时，会出现退化配置（所有线交汇于锚点）。DCL 通过强制最小集包含来自两个锚点的线（如两条来自 $\mathbf{a}_1$、一条来自 $\mathbf{a}_2$）来规避此问题。该检查可通过监测采样线对的交点是否重合来高效实现。

**鲁棒估计**：采用 Lo-RANSAC 框架配合 l6P 最小求解器进行鲁棒位姿估计，最终使用 Levenberg-Marquardt 算法对内点进行非线性优化。所有实现均基于 PoseLib 求解器库。

### 4.4 定位精度与隐私保护的权衡机制

DCL 的隐私保护强度与定位精度之间存在可控的权衡，其调节旋钮为**锚点距离**（即锚点到图像中心的像素距离）。消融实验表明：

- 默认锚点距离 $H$（等于图像高度）在 Aachen 数据集上获得最佳召回率。
- 增大锚点距离会使线方向分布更接近平行，理论上增强模式二的防御效果，但同时降低了线的几何判别力，导致定位性能下降。

这一机制使得 DCL 可根据实际部署场景的隐私需求灵活配置锚点距离，在隐私保护与定位精度之间取得可调节的平衡。

![[assets/figures/papers/paper_list_l2059_https_arxiv_org_abs_2604_22310/figures/004_Figure_3.jpg]]
*Figure 3: Visualization of DCL’s two failure modes against the geometry-recovery attack. (a) Original keypoints. (b) Our DCL obfuscation of the keypoints in (a). (c) Mode 1 (intra-anchor convergence): Keypoints trivially converge to the anchor location. (d) Mode 2 (inter-anchor instability): Near-parallel geometry forces optimization to high variance instability*

## 实验与关键发现

### 隐私保护强度：几何恢复攻击下的鲁棒性验证

DCL 的核心设计目标是抵御基于邻居线交点加权平均的点恢复攻击。我们首先在合成环境下验证其理论效果：在 640×480 分辨率下生成 1500 个均匀分布的关键点，经 DCL 混淆后执行恢复攻击。如 Figure 4 所示，恢复误差低于 30 像素的关键点仅有 8 个，绝大多数恢复点偏离原始位置极远。进一步可视化恢复参数的方差（Figure 4d）表明，分区边界附近的线对近乎平行，导致加权平均参数在数值上极不稳定，这正是 DCL 使优化问题病态化的直接证据。

![[assets/figures/papers/paper_list_l2059_https_arxiv_org_abs_2604_22310/figures/005_Figure_4.jpg]]
*Figure 4: Overview of our DCL method and its robustness in our synthetic environment. We generated 1,500 uniformly distributed keypoints within a 640x480 resolution. (b) shows the recovered keypoints, while the error map (c) confirms the attack’s overall failure, with only 8 keypoints having error below 30 pixels. (d) visualizes the standard deviation of the estimated parameter*

在真实数据集上的定量评估（Table 2）进一步证实了这一结论。在 7Scenes 数据集上，DCL 的恢复点平均几何误差达到 330.4 像素，而 Random Lines 仅为 6.137 像素，两者差距超过 50 倍。相应地，基于恢复点重建的图像质量指标也显著恶化：LPIPS 从 Random Lines 的 0.476 上升至 DCL 的 0.736，PSNR 则从 14.17 降至 7.04。Figure 6 的定性反演结果直观展示了这一差异——DCL 重建的图像几乎无法辨认原始场景内容，预训练 YOLO-v11 模型也未能检测出有意义的物体。

![[assets/figures/papers/paper_list_l2059_https_arxiv_org_abs_2604_22310/figures/010_Table_2.jpg]]
*Table 2: Mean geometric error*

![[assets/figures/papers/paper_list_l2059_https_arxiv_org_abs_2604_22310/figures/008_Figure_6.jpg]]
*Figure 6: Qualitative inversion results with the Superpoint [12], (top) Aachen (bottom) 7Scenes. Images are reconstructed after feature positions are recovered via geometry-recovery attack [7] on various methods: (b) Feature Points [12], (c) Random Lines [51], (d) Coordinate Permutation [34], and (e) Dual Convergent Lines (ours). We also visualize the object detection results with a pretrained YOLO-v11 model. Additional qualitative results and inversion results with SIFT [25] descriptors are in the supplementary material*

值得注意的是，上述恢复攻击实验采用了最坏情况（oracle）设置，即假设攻击者能够完美识别每条混淆线的邻居关系。这一设置评估的是隐私保护的理论上界，实际攻击者的能力通常更弱，因此 DCL 的实际隐私保护强度可能更高。

### 视觉定位精度

尽管 DCL 以牺牲部分几何信息为代价换取隐私保护，其在标准视觉定位基准上仍保持了可用的定位精度。

**Cambridge 数据集**（Table 3）：DCL 的中位位置误差为 22.5 cm、旋转误差为 0.50°，相比无隐私保护的 HLoc（SP+NN，12 cm / 0.2°）有所下降，但仍处于实用范围内。与 Random Lines 相比，DCL 的精度损失主要源于混淆线几何结构的改变——Random Lines 的线方向随机但均通过原始关键点，保留了更多局部几何约束；而 DCL 的线从固定锚点发出，使得 2D-3D 匹配中的几何残差分布发生系统性偏移。

**Aachen Day-Night 数据集**（Table 4）：在大场景昼夜变化条件下，DCL 在 0.25m/2° 阈值下的召回率为 58.9%，低于 HLoc 的 85.6% 和 Random Lines 的 76.3%。这一差距主要源于大场景中特征点分布更广，分区边界附近的退化效应被放大。

**7Scenes 数据集**（Table 5）：在室内小场景中，DCL 的中位位置误差为 5.2 cm、旋转误差 2.1°，5cm/5° 召回率为 48.2%。与基于结构的方法（如 Active Search 的 3.0 cm / 1.5°）相比存在差距，但在隐私保护方法中表现竞争力。

### 消融实验

**锚点距离的影响**（Table 6, Table 8）：默认锚点距离设为图像高度 H，即上下锚点分别位于图像中心垂直线的顶端和底端。消融实验表明，增加锚点距离（如 2H、4H）会降低定位精度——在 Cambridge 和 7Scenes 的平均中位误差上，H 设置下为 13.85 cm / 1.30°，而 4H 设置下恶化至 18.35 cm / 1.55°。Aachen 数据集上的召回率也呈现类似趋势：0.25m/2° 阈值下，H 设置为 58.9%，4H 设置降至 51.2%。这一现象的原因是锚点距离增大后，混淆线的方向分布更趋于平行，导致 l6P 求解器在最小配置采样时更难获得数值稳定的解。

**分区边界方向**（Appendix G）：垂直中线分割在 7Scenes 上仅产生 4 个退化案例（所有关键点落入同一分区），而水平中线分割则导致 39 个退化案例。这是因为自然图像中特征点的垂直分布通常比水平分布更均匀，垂直分割能更有效地将关键点分配到两个区域。

### 失败模式分析

DCL 的两种失败模式在 Figure 3 中得到了清晰展示：

1. **锚点内收敛（Mode 1）**：当目标线的邻居线全部来自同一锚点时，加权平均解平凡地收敛到该锚点位置，恢复点完全偏离原始关键点。
2. **锚点间不稳定（Mode 2）**：当邻居线来自不同锚点且目标线位于分区边界附近时，线对近乎平行。根据推论 1.1，权重 $w_{i,j} = \sin^2(\theta_{i,j})$ 趋近于零，导致加权平均的数值条件数极大，恢复点位置方差极高。

这两种模式共同确保了 DCL 在绝大多数配置下都能有效抵御点恢复攻击。唯一的退化配置——所有查询关键点落入同一分区——在实际数据中极为罕见（7Scenes 中仅 4/17,000 样本），但仍提示未来可探索自适应分区策略以进一步降低这一风险。

![[assets/figures/papers/paper_list_l2059_https_arxiv_org_abs_2604_22310/figures/013_Table_6.jpg]]
*Table 6: Ablation study of anchor point distance on localization accuracy. We report the average of median position (cm) / rotation (°) errors across the 7Scenes and Cambridge datasets. H denotes the height of the image query*

![[assets/figures/papers/paper_list_l2059_https_arxiv_org_abs_2604_22310/figures/016_Table_8.jpg]]
*Table 8: Ablation study of anchor point distance on localization accuracy on the Aachen Day & Night dataset. We report the recall at thresholds 0.25m/2°, 0.5m/5°, and 5m/10° (%). H denotes the height of the image query*

## 定位与知识库关联

### 问题背景与基线谱系

视觉定位中隐私保护图像查询的研究目标是在不暴露查询图像视觉内容的前提下完成精确的6-DoF位姿估计。现有方案可大致分为三类：

**几何混淆方法**直接修改特征点的几何表示。**Random Lines** 将每个关键点替换为一条通过该点的随机方向直线；**Coordinate Permutation** 通过随机配对关键点并交换其坐标分量实现混淆。这两种方法在定位精度上表现良好，但近期研究表明它们对几何恢复攻击高度脆弱——攻击者通过最小化目标线上点到其邻居线距离的平方和（Eq. (3)），可以近似恢复原始关键点位置，进而通过反演网络重建查询图像的视觉内容。

**加密与安全计算方案**（如同态加密、安全多方计算）提供理论上的强隐私保证，但面临地图维护困难、计算开销大、难以实时运行等实际部署瓶颈。

**特征变换方案**（如基于深度网络的描述子加密）通常需要重新训练模型或修改服务器端地图，可扩展性受限。

本文提出的 **Dual Convergent Lines (DCL)** 属于几何混淆范式，但与 Random Lines 有本质区别：Random Lines 的每条线随机定向且独立通过原始关键点，导致混淆后的线邻居在空间上仍近似包围原始点，为攻击者提供了可恢复的几何线索。DCL 通过引入双锚点机制和空间分区策略，将点恢复攻击的优化问题**主动构造为病态问题**，从而在保持可定位性的同时大幅提升隐私保护强度。

### 核心机制与知识贡献

DCL 的核心设计包含两个关键创新点：

**1. 双锚点空间分区。** 沿图像垂直中线将图像空间划分为左右两个区域 $\mathcal{R}_1$ 和 $\mathcal{R}_2$，并在图像中心的上、下两端分别设置固定锚点 $\mathbf{a}_1$ 和 $\mathbf{a}_2$。每个关键点根据其所在区域连接到对应锚点，生成混淆线：

$$\mathbf{l}_i = \begin{cases} \mathrm{line}(\mathbf{x}_i, \mathbf{a}_1), & \text{if } \mathbf{x}_i \in \mathcal{R}_1 \\ \mathrm{line}(\mathbf{x}_i, \mathbf{a}_2), & \text{if } \mathbf{x}_i \in \mathcal{R}_2 \end{cases}$$

**2. 病态优化诱导。** 该设计导致几何恢复攻击陷入两种失败模式（Figure 3）：
- **模式一（锚点内收敛）：** 当邻居线来自同一锚点时，最优解平凡地收敛到锚点本身，而非原始关键点位置。
- **模式二（锚点间不稳定）：** 当邻居线来自不同锚点且位于分区边界附近时，两线近乎平行。根据 Proposition 1 和 Corollary 1.1，恢复点沿线的参数 $t_i^*$ 是各邻居线与目标线交点参数的加权平均：

$$t_i^* = \frac{\sum_j (w_{i,j} t_{i,j}^*)}{\sum_j w_{i,j}}, \quad w_{i,j} = \|\mathbf{v}_i \times \mathbf{v}_j\|^2 = \sin^2(\theta_{i,j})$$

当 $\theta_{i,j} \to 0$（线趋于平行）时，权重 $w_{i,j} \to 0$，导致数值不稳定且恢复方差极大，破坏关键点恢复。

这一理论分析是 DCL 区别于 Random Lines 等启发式混淆方法的核心知识贡献：**DCL 并非简单地增加恢复难度，而是从优化问题的病态性出发，系统性地构造了使攻击必然失败的条件。**

### 适用边界与局限

**退化配置风险。** 当所有查询关键点均落入同一分区时，DCL 退化为所有线交汇于单一锚点的平凡情况。在实际的 7Scenes 数据集中，该退化仅出现在 17,000 个样本中的 4 个，但在极端场景下仍需关注。消融实验表明，使用水平中线分割会使退化案例从 4 增加到 39，垂直分割显著更优。

**定位精度与隐私的折衷。** 在 Cambridge 数据集上，DCL 的中位位置误差为 22.5 cm、旋转误差为 0.50°，相比无隐私保护的 HLoc (SP+NN)（12 cm / 0.2°）有所下降。在 Aachen Day-Night 大场景数据集上，DCL 的定位召回率低于 Random Lines。这表明更强的隐私保护以一定的定位精度为代价，该折衷在大场景中更为显著。

**攻击模型假设。** DCL 的安全性分析主要针对基于邻居线距离最小化的几何恢复攻击，且实验采用最坏情况（oracle）设置，假设邻居识别完美。对于基于扩散模型的反演攻击或利用服务器端内点信息的迭代攻击，DCL 展现出一定的鲁棒性（Figure 7, Figure 8），但其对抗更广泛攻击类型的完备性尚需进一步验证。

**固定分区策略。** 当前采用固定垂直中线分区，未根据场景内容或特征点分布自适应调整。在特征点分布严重偏斜的场景中，固定分区可能增加退化风险。

### 开放问题

1. **自适应分区策略。** 如何设计能根据特征点空间分布动态调整的分区边界，在保持病态优化特性的同时最小化退化风险？是否可以利用场景先验（如消失点、语义布局）引导分区？

2. **新型攻击的防御完备性。** DCL 的线表示是否能够抵御除几何恢复攻击之外的其他隐私攻击范式，特别是基于生成模型（如扩散模型）直接从线表示反演图像的攻击？服务器端在已知部分内点位置时的迭代攻击的实际威胁程度如何？

3. **大场景下的精度保持。** 在 Aachen 等大场景中，DCL 的定位召回率下降明显。是否可以通过锚点距离的自适应调整或多尺度锚点策略来缓解大场景下的精度损失？

4. **与其他隐私技术的组合。** DCL 作为几何混淆层，是否可以与描述子加密或安全计算方案结合，提供多层隐私保护？这种组合是否会引入新的精度或效率瓶颈？

## 原文 PDF

![[paperPDFs/CVPR_2026/Revisiting_Geometric_Obfuscation_with_Dual_Convergent_Lines_for_Privacy_Preserving_Image_Queries_in_Visual_Localization.pdf]]
