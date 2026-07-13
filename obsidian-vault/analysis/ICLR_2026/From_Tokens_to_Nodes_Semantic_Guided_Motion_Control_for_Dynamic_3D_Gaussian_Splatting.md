---
title: "From Tokens to Nodes: Semantic-Guided Motion Control for Dynamic 3D Gaussian Splatting"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/From_Tokens_to_Nodes_Semantic_Guided_Motion_Control_for_Dynamic_3D_Gaussian_Spla_630a75470d45.pdf
project_link: null
code_link: "https://github.com/YvanYin/Metric3D"
aliases:
- OMST
- FTNSGMCD3GS
tags:
- ICLR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
core_operator: 控制点分配密度与运动复杂度的匹配程度：通过引入基于语义和运动先验的自适应节点初始化（MANI）与压缩策略，可重新平衡静态与动态区域的资源分配。
primary_logic: 利用视觉基础模型（VFM）提取语义标记和运动先验，建立图像补丁-标记-节点间的对应关系，使节点分布能够跟随运动倾向自适应地集中在动态区域；同时采用样条参数化节点轨迹并用2D跟踪初始化，获得平滑、紧凑的运动表示，从而在高效计算下显著提升动态细节的重建质量。
claims:
- 在Hyper-NeRF和N3DV数据集上，所提方法在PSNR、SSIM和LPIPS指标上均超越现有SOTA方法。
- 消融实验证明运动自适应节点初始化（MANI）和样条轨迹参数化各自贡献显著，组合后达到最佳效果。
- MANI通过动态倾向评分在动态区域保留更多节点，在静态区域大幅压缩节点，可视化与定量结果均优于纯几何初始化。
- 样条轨迹替代MLP变形场，结合2D跟踪初始化，能提供更平滑的运动和更稳定的优化。
---

# From Tokens to Nodes: Semantic-Guided Motion Control for Dynamic 3D Gaussian Splatting

> [!tip] 核心洞察
> 利用视觉基础模型（VFM）提取语义标记和运动先验，建立图像补丁-标记-节点间的对应关系，使节点分布能够跟随运动倾向自适应地集中在动态区域；同时采用样条参数化节点轨迹并用2D跟踪初始化，获得平滑、紧凑的运动表示，从而在高效计算下显著提升动态细节的重建质量。

| 字段 | 内容 |
|------|------|
| 中文题名 | 从标记到节点：基于语义引导的动态3D高斯溅射运动控制 |
| 英文题名 | From Tokens to Nodes: Semantic-Guided Motion Control for Dynamic 3D Gaussian Splatting |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=ginzNWATI1) · [paper](https://arxiv.org/abs/2411.17044) · [Code](https://github.com/YvanYin/Metric3D) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction |
| Method | Ours (MANI + Spline trajectories) |
| Dataset | Hyper-NeRF, N3DV |

> [!tip] 效果简介
> - Hyper-NeRF (vrig) 上，PSNR↑ 25.78 vs Grid4D 25.46 (+0.32)；SSIM↑ 0.723 vs Grid4D 0.715 (+0.008)；LPIPS↓ 0.242 vs Grid4D 0.261 (-0.019)。
> - N3DV 上，PSNR↑ 23.31 vs Grid4D 22.51 (+0.80)；SSIM↑ 0.821 vs Grid4D 0.805 (+0.016)。
> - Hyper-NeRF 上，FPS↑ 70 vs 4DGS 34 (+36)。

## 概要

动态3D高斯溅射（3DGS）通过显式点云表示在静态场景重建中取得了显著成功，但将其扩展到动态场景时面临一个核心瓶颈：**控制点分配密度与运动复杂度不匹配**。现有稀疏控制点方法（如SC-GS、MoSca）普遍采用最远点采样（FPS）或体素化等几何均匀策略初始化控制节点，导致静态背景区域存在大量冗余节点，而动态前景区域控制点密度不足，限制了重建质量和计算效率。

本文提出了一种**语义引导的运动自适应框架**，核心洞见在于利用视觉基础模型（VFM）提取的语义标记和运动先验，建立图像补丁-标记-节点间的对应关系，使节点分布能够跟随运动倾向自适应地集中在动态区域。具体而言，方法包含两个关键设计：

- **运动自适应节点初始化（MANI）**：从图像块反投影生成候选节点，通过迭代体素化与动态倾向评分机制，在体素内执行语义和前景引导的自适应合并——动态区域保留更多节点，静态区域大幅压缩。
- **样条参数化节点轨迹**：使用三次Hermite样条建模节点SE(3)运动，替代传统MLP变形场，并由2D跟踪轨迹初始化，提供紧凑、平滑且可微的运动基元。

在Hyper-NeRF和N3DV两个主流动态场景数据集上，所提方法在PSNR、SSIM和LPIPS指标上均超越现有SOTA方法（包括Grid4D、4DGS、SC-GS等），同时在渲染速度（70 FPS vs. 4DGS的34 FPS）和存储开销（25 MB vs. 4DGS的61 MB）方面展现出显著优势。消融实验进一步验证了MANI和样条轨迹各自的关键贡献，以及VFM先验对框架的稳定支撑作用。



### 动态场景重建的核心挑战

从单目视频重建动态三维场景是计算机视觉与图形学中的基础问题，其核心困难在于：观测数据仅提供稀疏的二维投影，而场景本身同时存在几何、外观与运动的复杂耦合。近年来，三维高斯溅射（3D Gaussian Splatting, 3DGS）凭借其显式表示和高效可微光栅化，迅速成为静态场景重建的主流方案。然而，将其扩展到动态场景时，如何紧凑且准确地表示时变几何与外观成为一个关键瓶颈。

现有方法大致可归为两类：**逐高斯变形场**和**稀疏控制点**。前者为每个高斯分配独立的时变参数（如 **D-3DGS** 或 **4DGS**），虽能精细建模运动，但参数量随场景规模线性增长，存储和计算开销巨大；后者借鉴计算机图形学中的蒙皮变形思想，用少量控制节点的运动来驱动全体高斯（如 **SC-GS**），在效率上具有明显优势，但其性能高度依赖控制点的空间分布质量。

### 现有稀疏控制方法的根本缺陷

当前稀疏控制点方法的初始化策略存在一个被忽视的结构性缺陷：**控制点密度与场景运动复杂度之间的失配**。

具体而言，主流方法采用几何均匀采样策略——如最远点采样（Farthest Point Sampling, FPS）或体素化（Voxelization）——在三维空间中等间距或等密度地分配控制节点。这一策略隐含假设运动复杂度在空间中均匀分布，然而真实动态场景往往呈现极端的非均匀性：静态背景区域占据大部分空间体积却几乎不需要运动自由度，而前景动态对象（如人体的手部、面部）的运动复杂度远高于背景，却仅分配到与静态区域相当甚至更少的控制点资源。

这种失配导致两个严重后果：
1. **静态区域存在大量冗余控制点**，浪费计算和存储资源，并可能在优化中引入虚假运动自由度，干扰重建质量；
2. **动态区域控制点密度不足**，无法充分表达复杂变形，导致运动细节丢失（如关节处的精细变形）。

以 **SC-GS** 为例，其采用FPS初始化控制点，再通过MLP变形场预测节点运动。虽然MLP理论上具有通用逼近能力，但控制点分布的根本性缺陷使其难以在有限优化预算内恢复高质量动态细节。

### 本文的核心动机

本文的核心观察是：**运动复杂度在场景中的分布可以通过视觉基础模型（Vision Foundation Models, VFM）的语义和运动先验来有效估计**。现代VFM能够从单目视频中提取丰富的场景理解信息——语义标记揭示对象的类别归属，2D跟踪轨迹反映像素级运动模式，深度估计提供三维结构线索。这些先验天然携带了“哪些区域更可能发生复杂运动”的信息。

基于这一观察，本文提出一个根本性的思路转变：**将控制点分配从“几何均匀”转向“运动自适应”**。具体而言，我们利用VFM提取的语义标记和运动先验，建立图像补丁-标记-节点之间的对应关系，使节点分布能够跟随运动倾向自适应地集中于动态区域，同时在静态区域大幅压缩冗余节点。此外，我们用三次Hermite样条替代MLP来参数化节点轨迹，并用2D跟踪进行初始化，从而获得更平滑、更紧凑的运动表示。

这一方法在Hyper-NeRF和N3DV数据集上均取得了最优的重建质量（PSNR分别达到25.78和23.31），同时保持了显著的计算效率优势——渲染速度达70 FPS，存储仅需25 MB，相比4DGS分别提升约2倍和压缩约2.4倍。消融实验进一步证实，运动自适应节点初始化（MANI）和样条轨迹参数化各自贡献显著，组合后达到最佳效果。



## 核心方法与创新机理

本工作针对现有动态3DGS稀疏控制方法中“控制点密度与运动复杂度失配”这一瓶颈，提出了两项关键创新，分别对应控制点初始化与运动轨迹建模两个核心槽位。

### 瓶颈分析：控制点分配与运动复杂度的失配

现有稀疏控制点方法（如 **SC-GS** (Huang et al., 2023)、**MoSca** (Lei et al., 2025)）依赖**几何均匀采样**策略（Farthest Point Sampling 或体素化）在空间中分配控制节点。这种策略隐含假设场景运动在空间上均匀分布，导致两个问题：
- **静态区域节点冗余**：背景等静止区域分配了与动态区域相当的控制点密度，浪费计算与存储资源；
- **动态区域节点不足**：运动剧烈的局部区域（如人体关节、动物肢体）控制点密度不足以捕捉精细变形，限制重建质量。

本文的核心洞察在于：**利用视觉基础模型（VFM）提取的语义标记和运动先验，可以建立图像补丁-标记-节点间的对应关系，使节点分布能够跟随运动倾向自适应地集中在动态区域**。

### 创新槽位一：运动自适应节点初始化（MANI）

**基线方法**：稀疏控制点动态3DGS（如SC-GS）采用FPS或体素化在规范空间均匀采样节点位置，节点分布与场景运动无关。

**本文方法**：提出**运动自适应节点初始化（MANI）**，将控制点分配从“几何均匀”转变为“运动感知”。具体包含三个关键机制：

1. **补丁到候选节点生成**：从关键帧图像块反投影到3D空间，生成携带语义标记的候选节点集，建立图像补丁-语义标记-空间节点的对应关系。

2. **语义引导的自适应压缩**：在迭代体素化过程中，通过联合相似度度量合并冗余节点：
   $$\sin ( \mathcal { N } _ { i } , \mathcal { N } _ { j } ) = \cos ( z _ { i } , z _ { j } ) - \eta \cdot \tilde { M } _ { \mathrm { f g } } ( \mathcal { N } _ { i } , \mathcal { N } _ { j } )$$
   该相似度结合了语义标记的余弦相似度和前景掩码先验，使语义相近且同属前景/背景的节点优先合并。

3. **动态倾向评分调制压缩比**：为每个体素簇计算“动态倾向”得分：
   $$p _ { \mathtt { d y n } } ( C ) = \sigma \left( \alpha \cdot \frac { 1 } { | \mathscr { U } _ { C } | } \sum _ { \mathcal { N } _ { k } \in \mathscr { U } _ { C } } m ( \mathcal { N } _ { k } ) - \beta \cdot \frac { 1 } { | \mathscr { M } _ { C } | } \sum _ { ( \mathcal { N } _ { i } , \mathcal { N } _ { j } ) \in \mathscr { M } _ { C } } \mathrm { s i m } ( \mathcal { N } _ { i } , \mathcal { N } _ { j } ) \right)$$
   该得分综合了簇内节点的运动活跃度和语义一致性。基于此得分，自适应调整每个簇的节点保留比例：
   $$r \% ( C ) = r _ { \operatorname* { m i n } } + ( 1 - p _ { \mathrm { d y n } } ( C ) ) \cdot ( r _ { \operatorname* { m a x } } - r _ { \operatorname* { m i n } } )$$
   **动态区域（高$p_{dyn}$）保留更多节点，静态区域（低$p_{dyn}$）大幅压缩**，实现控制点密度与运动复杂度的对齐。

**证据强度**：消融实验（Table 3b）显示，MANI相比FPS初始化使PSNR从24.49提升至25.78；可视化（Figure 4）证实MANI在动态区域保留更多节点，在静态区域显著压缩节点分布。

### 创新槽位二：样条参数化节点轨迹

**基线方法**：SC-GS等方法使用MLP变形场建模节点运动，MLP缺乏对运动平滑性的显式约束，且优化过程可能不稳定。

**本文方法**：采用**三次Hermite样条**参数化节点在关键帧间的SE(3)轨迹：
$$\xi ( t ) = h _ { 0 0 } ( \tau ) P _ { k } + h _ { 1 0 } ( \tau ) \left( t _ { k + 1 } - t _ { k } \right) \dot { P } _ { k } + h _ { 0 1 } ( \tau ) P _ { k + 1 } + h _ { 1 1 } ( \tau ) \left( t _ { k + 1 } - t _ { k } \right) \dot { P } _ { k + 1 }$$
其中$h_{00}, h_{10}, h_{01}, h_{11}$为Hermite基函数。样条参数化天然保证轨迹的$C^1$连续性，提供**平滑、紧凑且可微的运动基**。

为进一步稳定早期优化，平移部分通过**拟合2D跟踪轨迹初始化**：
$$\operatorname* { m i n } _ { \{ P _ { k } \} _ { k = 1 } ^ { K } } \ \sum _ { t = 0 } ^ { N _ { f } - 1 } \left\| x _ { t } - \xi ( t ) \right\| _ { 2 } ^ { 2 }$$
其中3D跟踪点$x_t$由TAPIR提取的2D轨迹结合深度图反投影得到。旋转部分初始化为单位阵，在联合优化阶段细化。

**证据强度**：消融实验（Table 3a）显示，在基线基础上添加样条参数化（+MS）带来约2.16 dB PSNR增益；进一步引入2D跟踪初始化（+Init）额外贡献约1.27 dB。Figure 6展示了轨迹初始化使重建更锐利。

### 辅助改进：变形传递与损失函数

除上述两个核心槽位外，本文还进行了两项辅助改进：

- **变形传递函数**：将基线常用的线性混合蒙皮（LBS）替换为**双四元数混合（DQB）**，避免LBS在大旋转时的“糖纸”伪影，提升变形物理合理性。
- **优化损失函数**：在RGB损失基础上，引入**掩码、深度、跟踪和ARAP正则化项**（Eq. 13-14），利用VFM先验提供多模态监督，约束几何一致性和局部刚性。

消融实验（Table 6）表明，移除任一VFM相关损失导致性能中等下降，但框架整体保持鲁棒。

### 创新总结

| 槽位 | 基线方案 | 本文方案 | 核心机制 |
|------|----------|----------|----------|
| 控制点初始化 | FPS/体素均匀采样 | MANI运动自适应初始化 | 语义标记+动态倾向评分调制压缩比 |
| 轨迹建模 | MLP变形场 | 三次Hermite样条 | 天然平滑+2D跟踪初始化 |
| 变形传递 | LBS | DQB | 避免大旋转伪影 |
| 损失函数 | RGB+SSIM | RGB+Mask+Depth+Track+ARAP | VFM多模态先验监督 |

**因果杠杆**：控制点分配密度与运动复杂度的匹配程度是核心杠杆——MANI通过语义和运动先验重新平衡静态与动态区域的资源分配，样条轨迹提供平滑紧凑的运动表示，两者协同实现了在高效计算下显著提升动态细节重建质量的目标。



本文提出的动态3D高斯溅射运动控制框架，以“从标记到节点”为核心设计理念，通过引入视觉基础模型（VFM）的语义与运动先验，将控制点密度与场景运动复杂度自适应对齐。整个pipeline由五个紧密耦合的模块构成，其输入为单目视频，输出为可动态渲染的规范空间3D高斯表示。

**输入与先验提取。** 给定单目视频，系统首先调用一组预训练的视觉基础模型提取多模态先验（Figure 1A）：**VGGT** 提供图像块的语义标记（token），**Track-Anything** 生成前景掩码，**DepthCrafter** 估计单目深度图，**TAPIR** 输出跨帧的2D跟踪轨迹（tracklets）。这些先验为后续的节点初始化、轨迹参数化和损失监督提供了关键信号。

**Patch-to-Node候选生成。** 从关键帧中采样图像块（patches），利用深度图和相机姿态将其反投影到3D空间，形成带有语义标记的候选节点集。每个候选节点携带其所属的语义标记和空间位置，构成后续自适应压缩的基础（Figure 1B）。

**运动自适应节点压缩（MANI）。** 这是框架的核心创新模块。MANI通过迭代体素化将候选节点划分到空间簇中，在每个体素簇内计算节点间的联合相似度（结合标记余弦相似度和前景掩码先验，Eq.6），并引入动态倾向评分 $p_{\mathrm{dyn}}(C)$ 来量化簇的运动活跃程度（Eq.7）。基于该评分，系统自适应地调制每个簇的压缩率 $r\%(C)$（Eq.8）：动态区域保留更多节点，静态区域大幅压缩。这从根本上解决了现有方法（如FPS或体素化）因几何均匀采样导致的控制点分布与运动复杂度失配问题。

**样条参数化节点轨迹。** 压缩后的节点被赋予基于三次Hermite样条的SE(3)轨迹参数化（Eq.9-10），替代传统MLP变形场。平移部分通过将2D跟踪轨迹反投影到3D空间后，以最小二乘拟合初始化（Eq.11-12），旋转部分初始化为单位阵。这种参数化提供了紧凑、平滑且可微的运动基元，显著降低了优化自由度并提升了运动表示的稳定性（Figure 1C）。

**高斯-节点绑定与变形传播。** 规范空间中的每个3D高斯通过RBF核与K近邻节点建立权重绑定（Eq.3），节点的SE(3)运动通过对偶四元数混合（DQB）传播至每个高斯，得到其全局刚性变换（Eq.4-5），从而将规范高斯变形到目标时刻的世界坐标系（Figure 1D）。

**联合优化与渲染。** 变形后的高斯模型通过可微光栅化渲染（Eq.1），与真实图像进行多视图比较。总损失函数（Eq.13）整合了RGB光度损失、掩码损失、深度损失、跟踪损失和ARAP正则化损失（Eq.14），对规范高斯参数、节点位置和样条轨迹进行端到端联合优化（Figure 1E）。

**关键设计决策的因果逻辑。** 框架的核心瓶颈突破在于：通过MANI将控制点分配从“几何均匀”转变为“运动自适应”，使得有限的节点预算能够集中在动态细节丰富的区域；同时，样条轨迹参数化相比MLP变形场提供了更平滑的运动插值和更少的可优化参数，2D跟踪初始化则为早期优化提供了可靠的初始解，避免了MLP变形场常见的欠拟合与过平滑问题。消融实验（Table 3a）定量验证了这一因果链：基线（FPS+MLP）PSNR为22.35 dB，添加MANI提升至23.89 dB，进一步替换为样条轨迹（+MS）提升至24.51 dB，再加入跟踪初始化（+Init）达到25.78 dB，每一步均带来显著且互补的增益。

### 补充图表

![[assets/figures/papers/paper_list_l50_https_openreview_net_forum_id_ginzNWATI1/figures/001_Figure_1.jpg]]
*Figure 1: The overview of our method. (A) Given a monocular video, we extract semantic and motion priors from pre-trained vision foundation models. (B) These priors guide motion-adaptive node initialization, yielding compact distributions aligned with dynamic regions. (C) The initialized nodes are assigned splineparameterized trajectories to provide a motion basis. (D) Node motions are propagated to Gaussians through deformation, transforming the canonical representation. (E) The deformed model is rendered and optimized for consistent reconstruction*



### 3DGS 渲染基础

本文的动态场景表示基于 3D Gaussian Splatting 框架。给定相机位姿，规范空间中的高斯通过 Alpha 混合渲染像素颜色：

$$C ( \boldsymbol { p } ) = \sum _ { i \in { \cal N } } { \bf c } _ { i } \alpha _ { i } \prod _ { j = 1 } ^ { i - 1 } ( 1 - \alpha _ { j } )$$

其中 $\mathbf{c}_i$ 和 $\alpha_i$ 分别为高斯 $i$ 的颜色和不透明度。动态建模的核心问题是如何为不同时刻提供合理的高斯变形。

### 高斯-节点绑定与变形传播

本文采用稀疏控制节点驱动全局变形。每个节点 $\mathcal{N}_i$ 由一个 SE(3) 轨迹 $\mathbf{T}_i(t)$ 和一个控制影响范围的 RBF 半径 $\rho_i$ 定义：

$$\mathcal { N } _ { i } = \{ \mathbf { T } _ { i } ( t ) , \rho _ { i } \}$$

高斯与节点之间的绑定权重通过归一化 RBF 核计算，基于高斯中心 $\mathbf{x}_j$ 与节点中心 $\mathbf{c}_i$ 的距离：

$$w _ { i j } = \frac { \exp \left( - \frac { \left\| \mathbf { x } _ { j } - \mathbf { c } _ { i } \right\| ^ { 2 } } { 2 \rho _ { i } ^ { 2 } } \right) } { \sum _ { k \in \mathcal { V } ( G _ { j } ) } \exp \left( - \frac { \left\| \mathbf { x } _ { j } - \mathbf { c } _ { k } \right\| ^ { 2 } } { 2 \rho _ { k } ^ { 2 } } \right) }$$

其中 $\mathcal{V}(G_j)$ 为高斯 $j$ 的 K 近邻节点集合。

为传播变形，首先将每个节点的 SE(3) 变换构造为单位对偶四元数：

$$\mathbf { Q } _ { i } ( t ) = q _ { r , i } ( t ) + \epsilon q _ { d , i } ( t ) , \quad q _ { d , i } ( t ) = \frac { 1 } { 2 } p _ { i } ( t ) q _ { r , i } ( t )$$

随后对邻居节点的对偶四元数加权求和并归一化，再转换回 SE(3) 得到高斯 $j$ 的全局刚性变换：

$$\hat { \mathbf { Q } } _ { j } ( t ) = \frac { \sum _ { i \in \mathcal { V } ( G _ { j } ) } w _ { i j } \mathbf { Q } _ { i } ( t ) } { \left\| \sum _ { i \in \mathcal { V } ( G _ { j } ) } w _ { i j } \mathbf { Q } _ { i } ( t ) \right\| } , \quad \mathbf { T } _ { j } ( t ) = \mathrm { D Q 2 S E 3 } \Big ( \hat { \mathbf { Q } } _ { j } ( t ) \Big )$$

这一对偶四元数混合（DQB）替代了传统线性混合蒙皮（LBS），避免了因旋转插值引起的塌缩伪影。

### 运动自适应节点初始化（MANI）

MANI 模块的目标是使控制点分布与运动复杂度匹配。首先从关键帧图像块反投影生成带有语义标记的候选节点集，然后通过迭代体素化与自适应压缩实现。

**节点合并相似度**：结合语义标记余弦相似度与前景掩码先验，判断两节点是否可合并：

$$\sin ( \mathcal { N } _ { i } , \mathcal { N } _ { j } ) = \cos ( z _ { i } , z _ { j } ) - \eta \cdot \tilde { M } _ { \mathrm { f g } } ( \mathcal { N } _ { i } , \mathcal { N } _ { j } )$$

**动态倾向评分**：对每个体素簇 $C$，综合其节点平均运动性和内部合并程度计算“动态倾向”：

$$p _ { \mathtt { d y n } } ( C ) = \sigma \left( \alpha \cdot \frac { 1 } { | \mathscr { U } _ { C } | } \sum _ { \mathcal { N } _ { k } \in \mathscr { U } _ { C } } m ( \mathcal { N } _ { k } ) - \beta \cdot \frac { 1 } { | \mathscr { M } _ { C } | } \sum _ { ( \mathcal { N } _ { i } , \mathcal { N } _ { j } ) \in \mathscr { M } _ { C } } \mathrm { s i m } ( \mathcal { N } _ { i } , \mathcal { N } _ { j } ) \right)$$

**自适应压缩率**：根据动态倾向得分调制每个簇的节点保留比例，静态区域高压缩，动态区域低压缩：

$$r \% ( C ) = r _ { \operatorname* { m i n } } + ( 1 - p _ { \mathrm { d y n } } ( C ) ) \cdot ( r _ { \operatorname* { m a x } } - r _ { \operatorname* { m i n } } )$$

### 样条参数化节点轨迹

节点轨迹采用三次 Hermite 样条在关键帧间插值，替代传统 MLP 变形场，提供紧凑、平滑且可微的运动基：

$$\xi ( t ) = h _ { 0 0 } ( \tau ) P _ { k } + h _ { 1 0 } ( \tau ) \left( t _ { k + 1 } - t _ { k } \right) \dot { P } _ { k } + h _ { 0 1 } ( \tau ) P _ { k + 1 } + h _ { 1 1 } ( \tau ) \left( t _ { k + 1 } - t _ { k } \right) \dot { P } _ { k + 1 }$$

其中 $\tau = (t - t_k) / (t_{k+1} - t_k)$ 为归一化时间，四个 Hermite 基函数为：

$$h _ { 0 0 } ( \tau ) = 2 \tau ^ { 3 } - 3 \tau ^ { 2 } + 1 , \quad h _ { 1 0 } ( \tau ) = \tau ^ { 3 } - 2 \tau ^ { 2 } + \tau , \quad h _ { 0 1 } ( \tau ) = - 2 \tau ^ { 3 } + 3 \tau ^ { 2 } , \quad h _ { 1 1 } ( \tau ) = \tau ^ { 3 } - \tau ^ { 2 }$$

**轨迹初始化**：平移部分利用 2D 跟踪点反投影到世界坐标后通过最小二乘拟合初始化。给定深度 $D_t$ 和相机位姿，2D 跟踪点 $u_t$ 反投影为 3D 点：

$$x _ { t } = \mathbf { R } _ { t } ^ { \top } \pi _ { \mathbf { K } } ^ { - 1 } \big ( u _ { t } , D _ { t } ( u _ { t } ) \big ) - \mathbf { R } _ { t } ^ { \top } \mathbf { T } _ { t }$$

随后拟合样条节点位置 $\{P_k\}$：

$$\operatorname* { m i n } _ { \{ P _ { k } \} _ { k = 1 } ^ { K } } \ \sum _ { t = 0 } ^ { N _ { f } - 1 } \left\| x _ { t } - \xi ( t ) \right\| _ { 2 } ^ { 2 }$$

旋转部分初始化为单位阵，在联合优化阶段细化。

### 联合优化损失

总损失函数组合了光度、掩码、深度、跟踪和 ARAP 正则化项：

$$\mathcal { L } _ { \mathrm { t o t a l } } = \lambda _ { \mathrm { r g b } } \mathcal { L } _ { \mathrm { r g b } } + \lambda _ { \mathrm { m a s k } } \mathcal { L } _ { \mathrm { m a s k } } + \lambda _ { \mathrm { d e p t h } } \mathcal { L } _ { \mathrm { d e p t h } } + \lambda _ { \mathrm { t r a c k } } \mathcal { L } _ { \mathrm { t r a c k } } + \lambda _ { \mathrm { a r a p } } \mathcal { L } _ { \mathrm { a r a p } }$$

其中 ARAP（As-Rigid-As-Possible）损失鼓励相邻高斯之间距离和局部坐标跨帧保持稳定，增强变形一致性：

$$\mathcal { L } _ { \mathrm { a r a p } } = \displaystyle \sum _ { t = 1 } ^ { T } \sum _ { j = 1 } ^ { N _ { g } } \sum _ { k \in \hat { \mathcal { E } } ( j ) } \lambda _ { l } \left| \| \mathbf { p } _ { t } ^ { ( j ) } - \mathbf { p } _ { t } ^ { ( k ) } \| - \| \mathbf { p } _ { t ^ { \prime } } ^ { ( j ) } - \mathbf { p } _ { t ^ { \prime } } ^ { ( k ) } \| \right| + \lambda _ { c } \left\| \mathbf { Q } _ { t } ^ { ( k ) - 1 } \mathbf { p } _ { t } ^ { ( j ) } - \mathbf { Q } _ { t ^ { \prime } } ^ { ( k ) - 1 } \mathbf { p } _ { t ^ { \prime } } ^ { ( j ) } \right\|$$

消融实验（Table 6）表明，移除任一 VFM 相关损失项（mask、depth、track）会导致性能中等下降，但框架整体保持鲁棒。

### 补充图表

![[assets/figures/papers/paper_list_l50_https_openreview_net_forum_id_ginzNWATI1/figures/009_Figure_4.jpg]]
*Figure 4: Visualization of different Node init. meth. on Chicken scene of Hyper-NeRF data (Park et al. (2021b))*



## 实验与关键发现

### 主实验结果

我们在两个主流动态场景重建基准上进行了定量评估：**Hyper-NeRF**（单目视频）和**N3DV**（多视图视频）。Table 1 和 Table 2 分别给出了各场景的逐项对比结果。

![[assets/figures/papers/paper_list_l50_https_openreview_net_forum_id_ginzNWATI1/figures/002_Table_1.jpg]]
*Table 1: Quantitative comparison on Hyper-NeRF(vrig) dataset per-scene. We highlight the second best and the third best results in each scene*

![[assets/figures/papers/paper_list_l50_https_openreview_net_forum_id_ginzNWATI1/figures/003_Table_2.jpg]]
*Table 2: Quantitative comparison on N3DV dataset per-scene. We highlight the best , second best and the third best results in each scene*

在 Hyper-NeRF 数据集上，我们的方法在平均 PSNR、SSIM 和 LPIPS 三项指标上均达到最优：PSNR 25.78、SSIM 0.723、LPIPS 0.242，相比次优方法 **Grid4D**（PSNR 25.46 / SSIM 0.715 / LPIPS 0.261）分别提升 +0.32 dB、+0.008 和 -0.019。在 N3DV 数据集上，我们的方法同样取得最佳平均 PSNR（23.31）和 SSIM（0.821），较 Grid4D（22.51 / 0.805）分别提升 +0.80 dB 和 +0.016。

从效率角度看（Table 12），我们的方法在渲染速度上达到 70 FPS，远超 **4DGS** 的 34 FPS，同时存储占用仅 25 MB（4DGS 为 61 MB）。值得注意的是，我们的模型在计算能力相对较低的 **NVIDIA V100** GPU 上完成训练和测试，而 4DGS、MoDec-GS 等基线在更快的 RTX 3090 或 RTX A6000 上运行，因此我们的效率优势在硬件劣势下依然显著。

![[assets/figures/papers/paper_list_l50_https_openreview_net_forum_id_ginzNWATI1/figures/020_Table_12.jpg]]
*Table 12: Efficiency comparison on Hyper-NeRF dataset. We highlight the best , second best and the third best results in each scene*

定性可视化（Figure 3 及补充对比图）显示，我们的方法在动态细节（如 Chicken 场景的鸡头运动、Broom 场景的扫帚摆动）上重建更为清晰锐利，而 Grid4D 和 D-3DGS 在运动边界处存在模糊或伪影。

![[assets/figures/papers/paper_list_l50_https_openreview_net_forum_id_ginzNWATI1/figures/007_Figure_3.jpg]]
*Figure 3: Qualitative comparison on the N3DV dataset (Li et al. (2022))*

### 消融实验

消融实验（Table 3）系统验证了各核心组件的贡献，所有实验在 Hyper-NeRF 数据集上进行。

![[assets/figures/papers/paper_list_l50_https_openreview_net_forum_id_ginzNWATI1/figures/008_Table_3.jpg]]
*Table 3: Ablation studies on the Hyper-NeRF (Park et al. (2021b)) dataset*

**组件级消融（Table 3a）**：以 SC-GS 为基线（PSNR 22.35），逐步添加我们的改进模块：
- 引入**运动自适应节点初始化（MANI）**后，PSNR 提升至 23.89（+1.54 dB）；
- 进一步用**样条轨迹参数化（MS）**替换 MLP 变形场，PSNR 达到 24.51（相比基线 +2.16 dB）；
- 在样条基础上加入**2D 跟踪初始化（+Init）**，PSNR 进一步提升至 25.78（+1.27 dB）。

这一递进式增益表明，MANI 和样条轨迹各自提供独立且互补的改进：MANI 解决了控制点分布与运动复杂度不匹配的问题，样条轨迹提供了更平滑、紧凑的运动表示，而 2D 跟踪初始化则为样条提供了良好的优化起点。

**初始化策略对比（Table 3b）**：我们对比了多种节点初始化方法。MANI 以 PSNR 25.78 显著优于 FPS（24.49）、体素化（24.31）和 Tracklet-based 初始化（24.66）。Figure 4 的可视化直观展示了 MANI 的效果：在 Chicken 场景中，FPS 在静态背景区域分配了大量冗余节点，而 MANI 通过动态倾向评分机制使节点集中在鸡头等动态区域，静态区域节点被大幅压缩。

**先验模型选择**：我们测试了不同深度估计模型（Table 4）和 2D 跟踪模型（Table 5）的影响。替换深度先验为 DepthAnything 或 Metric3D 仅带来微小性能变化（PSNR 波动在 0.1 dB 以内），DepthCrafter 略优。替换 2D 跟踪模型为 CoTracker 或 SpatialTracker 时，TAPIR 的结果最佳。这表明框架对具体 VFM 选择具有较好的鲁棒性。

**损失函数消融（Table 6）**：移除任一 VFM 相关损失项（mask、depth、track）会导致性能中等下降，但框架仍保持基本重建能力，说明多先验监督信号之间存在一定的互补性。

**超参数敏感性**：我们针对压缩边界 $(r_{\min}, r_{\max})$（Table 7）、合并相似度权重 $\eta$（Table 8）、动态倾向评分参数 $(\alpha, \beta)$（Table 9）以及关键帧间隔 $N$（Table 10）进行了敏感性分析。在较宽的参数范围内，性能波动平稳，默认设置 $(r_{\min}=0.1, r_{\max}=0.9, \eta=0.5, \alpha=1.0, \beta=1.0, N=5)$ 接近最优，说明方法对超参数不敏感，具有良好的实用性。

### 失败模式与局限性

尽管方法整体表现优异，仍存在以下局限：

1. **先验模型误差传播**：方法依赖 VGGT、Track-Anything、DepthCrafter、TAPIR 等多个现成 VFM，这些模型本身的误差可能传播到重建结果中。在严重遮挡或快速运动场景下，深度估计和 2D 跟踪的质量下降可能导致节点初始化和监督信号不准确。

2. **训练效率**：训练时间约为 39 分钟（Hyper-NeRF 场景），虽然优于许多 NeRF 基线，但仍未达到实时训练，限制了交互式应用场景。

3. **硬件公平性**：效率对比中使用了不同 GPU 硬件（V100 vs RTX 3090/A6000），虽然作者指出 V100 计算能力较低，但这种不公平比较可能减弱效率优势结论的严谨性。

4. **单目重建固有挑战**：使用单目视频进行重建时，在严重遮挡或快速运动下可能遇到点云缺失和深度歧义问题，依赖深度和跟踪先验仅能部分缓解。

### 补充图表

![[assets/figures/papers/paper_list_l50_https_openreview_net_forum_id_ginzNWATI1/figures/014_Table_6.jpg]]
*Table 6: Ablation study on VFM prior loss*

![[assets/figures/papers/paper_list_l50_https_openreview_net_forum_id_ginzNWATI1/figures/011_Table_4.jpg]]
*Table 4: Additional ablation study on different Depth prior on Chiken scene of Hyper-NeRF dataset per-scene*

![[assets/figures/papers/paper_list_l50_https_openreview_net_forum_id_ginzNWATI1/figures/012_Table_5.jpg]]
*Table 5: Additional ablation study on different 2D Tracklets prior on Chiken scene of Hyper-NeRF dataset per-scene*

![[assets/figures/papers/paper_list_l50_https_openreview_net_forum_id_ginzNWATI1/figures/015_Table_7.jpg]]
*Table 7: Ablation study on*

![[assets/figures/papers/paper_list_l50_https_openreview_net_forum_id_ginzNWATI1/figures/016_Table_8.jpg]]
*Table 8: Ablation study on η*



## 定位与知识库关联

### 1. 与动态场景表示方法的谱系关系

本工作处于**动态3D高斯溅射（Dynamic 3DGS）**与**视觉基础模型（VFM）先验驱动重建**的交汇点。从方法演进脉络看，可梳理出两条关键路径：

**路径一：从NeRF到3DGS的动态表示演进。** 早期动态场景重建以NeRF变体为主，如**HyperNeRF**（Park et al., 2021）和**TiNeuVox**（Fang et al., 2022），通过MLP建模时变辐射场，但渲染效率受限于体渲染的计算开销。3DGS的出现推动了动态版本的快速迭代：**D-3DGS**（Yang et al., 2024b）对每个高斯分配独立的MLP变形场，**4DGS**（Wu et al., 2024）引入时变高斯参数，**Grid4D**（Xu et al., 2024）则通过时空网格编码变形。这些方法虽提升了渲染速度，但逐高斯的变形建模导致参数量膨胀和运动过拟合。

**路径二：稀疏控制点的动态3DGS。** 为降低参数量，**SC-GS**（Huang et al., 2023）和**MoSca**（Lei et al., 2025）引入稀疏控制点，通过线性混合蒙皮（LBS）将节点运动传播至高斯。然而，这类方法的控制点初始化依赖**FPS或体素化**等几何均匀采样策略，核心瓶颈在于：**控制点密度与场景运动复杂度不匹配**——静态背景区域存在大量冗余节点，而动态前景区域节点密度不足，限制了重建质量与计算效率的平衡。

本文的核心突破在于**将控制点分配从几何均匀采样转向语义引导的自适应分配**，通过VFM提取的语义标记和运动先验，建立图像补丁-标记-节点间的对应关系，使节点分布能够跟随运动倾向自适应地集中在动态区域。这一思路与**MonoDyGau**（利用单目深度先验辅助动态3DGS）形成互补，但本文的独特贡献在于将语义、运动、深度三种先验统一到节点初始化的自适应压缩框架中。

### 2. 方法谱系中的关键改动槽位

相较于以SC-GS为代表的稀疏控制点基线，本方法在四个关键槽位上进行了系统性改进：

| 槽位 | 基线方法 | 本方法 | 改进效果 |
|------|----------|--------|----------|
| **控制点初始化** | FPS/体素化（几何均匀采样） | 运动自适应初始化MANI（语义+运动先验驱动的自适应压缩） | PSNR +1.29 dB（Table 3b, MANI vs FPS） |
| **轨迹建模** | MLP变形场 | 三次Hermite样条参数化 + 2D跟踪初始化 | PSNR +2.16 dB（Table 3a, +MS vs baseline） |
| **变形传递** | 线性混合蒙皮（LBS） | 双四元数混合（DQB） | 避免LBS的体积塌陷伪影（Appendix A.3） |
| **优化损失** | RGB + SSIM | RGB + Mask + Depth + Track + ARAP | 多模态先验联合约束，提升几何一致性 |

这四个槽位的改进并非孤立，而是形成了**从初始化到优化的完整链条**：MANI提供运动自适应的节点分布 → 样条轨迹提供紧凑平滑的运动基 → DQB保证物理一致性变形 → 多模态损失提供鲁棒的优化信号。消融实验（Table 3a）证实了这一链条的累积效应：基线22.35 → +MANI 23.89 → +MS 24.51 → +Init 25.78 PSNR。

### 3. 与VFM驱动方法的定位

本方法属于**VFM先验注入动态3DGS**的早期探索者之一。与同期工作相比：

- **DepthCrafter / Metric3D**（深度先验）：本文将其作为深度监督信号，消融显示替换为DepthAnything或Metric3D仅带来微小性能变化（Table 4），表明框架对深度模型选择具有鲁棒性。
- **TAPIR / CoTracker**（2D跟踪先验）：本文选用TAPIR作为默认跟踪模型，消融表明其优于CoTracker和SpatialTracker（Table 5），可能与TAPIR在细粒度运动上的跟踪精度有关。
- **VGGT / Track-Anything**（语义与掩码先验）：用于生成补丁标记和前景掩码，构成MANI的核心输入。

值得注意的是，本文并非简单堆砌VFM，而是通过**动态倾向评分机制**（Eq. 7-8）将这些先验有机融合：语义标记相似度决定节点合并的亲和性，前景掩码修正合并决策，运动先验调制压缩比。这种融合方式使得即使某个VFM输出存在噪声，其他先验仍可提供补偿——Table 6显示移除任一VFM相关损失仅导致性能中等下降，验证了框架的鲁棒性。

### 4. 适用边界与局限

**适用场景：**
- 单目视频的动态场景重建，尤其适合**运动复杂度空间分布不均**的场景（如人物动作、机械运动等前景动态明显而背景相对静止的场景）。
- 对**渲染效率**和**存储紧凑性**有要求的应用（70 FPS渲染，25 MB存储，Table 12）。

**已知局限：**

1. **VFM误差传播**：依赖多个预训练VFM（VGGT、Track-Anything、DepthCrafter、TAPIR），这些模型本身的误差可能传播到重建结果中。尽管消融显示损失函数对深度和跟踪的权重不敏感，但在极端遮挡或快速运动条件下，深度歧义和跟踪丢失仍可能影响重建质量。

2. **训练效率瓶颈**：训练时间约39分钟（Hyper-NeRF, V100 GPU），虽优于多数NeRF方法（如HyperNeRF需数小时），但仍未达到实时训练，限制了交互式应用场景。

3. **硬件公平性**：效率比较中使用了NVIDIA V100 GPU，而部分基线（如4DGS、MoDec-GS）在更快的RTX 3090或RTX A6000上运行，这种不公平比较可能减弱效率优势结论的严谨性。作者虽指出V100计算能力较低，但直接对比仍需谨慎解读。

4. **严重遮挡与快速运动**：单目视频在严重遮挡或快速运动时可能遇到点云缺失和深度歧义问题，依赖深度和跟踪先验仅能部分缓解，极端情况下重建质量可能显著下降。

### 5. 开放问题与未来方向

1. **VFM选择的系统化研究**：本文对深度和跟踪模型进行了初步消融（Table 4-5），但语义标记模型（VGGT vs DINOv2 vs SAM等）的选择对MANI的影响尚未系统评估。不同VFM组合是否存在协同效应或冗余，值得深入研究。

2. **端到端训练的可能性**：当前框架中VFM作为冻结的特征提取器，未来是否可以将VFM与动态3DGS进行端到端联合微调，使先验适应特定场景的统计特性？

3. **多模态先验的置信度感知融合**：当前MANI通过固定超参数（η, α, β）融合多模态先验，未来可引入置信度感知的自适应融合机制，根据各先验在局部区域的不确定性动态调整融合权重。

4. **扩展到多目和长视频**：当前方法针对单目视频设计，扩展到多目设置或长视频（需处理循环运动、场景进出等）时，节点管理和样条参数化策略需要相应调整。

5. **实时训练**：训练时间39分钟仍远未达到实时，探索更高效的节点初始化策略、简化优化流程或引入预训练先验加速收敛，是走向实际应用的关键一步。



## 原文 PDF

![[paperPDFs/ICLR_2026/From_Tokens_to_Nodes_Semantic_Guided_Motion_Control_for_Dynamic_3D_Gaussian_Spla_630a75470d45.pdf]]
