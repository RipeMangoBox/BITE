---
title: Grounded Latents for Entity-Centric 4D Scene Generation
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/Grounded_Latents_for_Entity_Centric_4D_Scene_Generation.pdf
project_link: null
code_link: null
aliases:
- GLEC4SG
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
- topic/generative_models_diffusion
core_operator: 采用稀疏、接地的3D潜变量点集表示场景，每个前景演员分配单个潜变量以保持身份和直接控制，并通过三阶段扩散（布局、特征、运动）实现可控、可解释的生成。
primary_logic: 将4D场景生成分解为三阶段：布局扩散决定粗粒度结构（位置、类别、朝向），特征扩散注入局部几何细节，运动扩散推动实时序一致的运动，从而使场景可控、可编辑且物理一致。
claims:
- 与密集体素方法相比，接地潜变量显著减少实体合并、闪烁、分裂等常见失败模式。
- 三阶段生成管道实现了对场景布局、几何细节和动态轨迹的分离控制与编辑。
- 在 CarlaSC 和 Waymo 数据集上均取得最优生成质量，尤其在对前景类别的指标上显著优于 DynamicCity 等基线。
- CarlaSC 上 MMD↓ Geometry (avg) = 6.44
---

# Grounded Latents for Entity-Centric 4D Scene Generation

> [!tip] 核心洞察
> 将4D场景生成分解为三阶段：布局扩散决定粗粒度结构（位置、类别、朝向），特征扩散注入局部几何细节，运动扩散推动实时序一致的运动，从而使场景可控、可编辑且物理一致。

| 字段 | 内容 |
|------|------|
| 中文题名 | 实体中心4D场景生成的接地潜变量框架 |
| 英文题名 | Grounded Latents for Entity-Centric 4D Scene Generation |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://openaccess.thecvf.com/content/CVPR2026/html/Park_Grounded_Latents_for_Entity-Centric_4D_Scene_Generation_CVPR_2026_paper.html) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction #topic/generative_models_diffusion |
| Method | LatentWorld |
| Dataset | CarlaSC, Waymo |

> [!tip] 效果简介
> - CarlaSC 上，MMD↓ Geometry (avg) 6.44 vs best baseline (LatentWorld achieves lowest MMD)；MMD↓ Semantics (avg) 11.30 vs best baseline (LatentWorld achieves lowest MMD)；MMD↓ Geometry & Semantics (avg) 6.69 vs best baseline (LatentWorld achieves lowest MMD)。
> - Waymo 上，MMD↓ Geometry (avg) 1.62 vs DynamicCity (outperforms DynamicCity)；MMD↓ Semantics (avg) 1.50 vs DynamicCity (outperforms DynamicCity)；MMD↓ Geometry & Semantics (avg) 0.96 vs DynamicCity (outperforms DynamicCity)。

## 概要

自动驾驶仿真、具身智能与世界模型等应用对**可控、可解释的 4D 场景生成**提出了迫切需求。现有方法普遍采用密集对齐网格的潜变量（如体素、三平面）进行生成，缺乏显式的实体建模，导致前景演员频繁出现**合并、闪烁、分裂**等失败模式，且难以实现精细的前背景分离控制。

针对这一瓶颈，本文提出 **LatentWorld**，核心思路是将场景表达为一组**稀疏、接地的 3D 潜变量点集**，每个前景演员分配恰好一个潜变量以维持身份一致性，背景则由多个潜变量覆盖以捕捉细节。生成过程分解为**三阶段扩散管道**：布局扩散生成粗粒度结构（位置、类别、BEV朝向），特征扩散注入局部几何细节，运动扩散生成自车与动态演员的未来轨迹，从而实现对场景布局、几何细节和动态轨迹的分离控制与编辑。

在 **CarlaSC** 和 **Waymo** 两个数据集上，LatentWorld 在几何与语义的 MMD 指标上均取得最优生成质量，尤其在前景类别上显著优于 **DynamicCity** 等基线方法。消融实验进一步验证了潜变量数量（768 为最优平衡点）和外推引导权重（λ=1.0 性能最优）的设计合理性。定性结果表明，接地潜变量有效消除了密集方法中的实体分裂与背景不一致问题，实现了稳定的轨迹与一致的背景结构。



自动驾驶系统对环境的理解正从静态 3D 感知向动态 4D 场景理解演进。生成式模型——特别是扩散模型——在图像和视频生成领域取得了显著进展，但在 4D 驾驶场景生成中仍面临根本性挑战。一个核心瓶颈在于：**现有方法普遍采用密集对齐网格的潜变量表示（如体素、三平面、HexPlane），缺乏显式的实体建模**。这种表示将场景中的所有元素——道路、建筑、车辆、行人——混合在一个统一的体积或张量中，导致三个关键的失败模式：

1. **实体合并**：相邻的前景演员在生成过程中被模糊为一个整体，丧失个体身份。
2. **前景闪烁**：同一演员在不同时间步的外观和位置发生不连续跳变。
3. **实体分裂**：单个演员被错误地分割为多个碎片，随时间推移而漂移。

这些失败源于一个根本性的表示缺陷：密集表示无法为每个前景实体提供独立的“锚点”来维持其身份和运动一致性。此外，这种表示使得对场景进行精细、可解释的前背景控制变得极为困难——例如，移动一辆特定车辆或旋转其朝向，在密集潜变量空间中缺乏直接的操纵手柄。

现有 4D 场景生成基线如 **DynamicCity**（HexPlane 特征）和 **Occ-Sora**（密集网格潜变量，Wang et al., arXiv 2024）虽然推进了动态场景生成，但它们均采用隐式的逐帧去噪或依赖外部启发式控制器来处理运动，未能将运动建模为场景生成管道中的显式可学习组件。这导致生成的动态序列缺乏物理一致性，尤其在自车转弯或复杂多演员交互场景下，背景结构随帧漂移，前景运动不可靠。

本文的核心动机在于：**将 4D 场景生成从“密集体积的隐式生成”重新定义为“稀疏接地实体的显式生成与操控”**。具体而言，我们提出用一组稀疏的、接地的 3D 潜变量点集来表示场景，每个前景演员分配恰好一个潜变量以维持身份，背景则由多个潜变量覆盖以捕捉细节。这种表示使得场景生成可以被分解为三个可分离且可解释的阶段——布局、特征、运动——从而在保持生成质量的同时，实现对场景结构、几何细节和动态轨迹的直接控制与编辑。



## 核心方法与创新机理

LatentWorld 的核心创新在于用**稀疏、接地的 3D 潜变量点集**替代传统方法中密集对齐网格的潜变量表示（如体素、三平面），从而从根本上改变了场景建模的方式。这一表示转换带来了四个关键的 changed slots，构成了该方法相对于现有工作的质变。

### 1. 场景表示：从密集网格到稀疏接地潜变量

现有 3D/4D 场景生成方法——包括 **SemCity**（Lee et al., CVPR 2024）的 triplane 扩散、**XCube**（Ren et al., CVPR 2024）的稀疏体素层次、**PDD**（Liu et al., ECCV 2024）的金字塔扩散，以及 **Occ-Sora**（Wang et al., arXiv 2024）的密集网格潜变量——均采用与空间网格对齐的潜变量。这种密集表示缺乏对场景中独立实体的显式建模，导致前景演员在生成过程中容易发生合并、闪烁和分裂等典型失败模式。

LatentWorld 将场景表达为一个稀疏的接地潜变量点集：

$$\mathcal{Z} = \{ z_n \}_{n=1}^N, \qquad z_n = \big( \mathbf{x}_n, c_n, \theta_n, \mathbf{f}_n \big)$$

每个潜变量 $z_n$ 包含三维位置 $\mathbf{x}_n$、语义类别 $c_n$、BEV 朝向 $\theta_n$ 和几何特征 $\mathbf{f}_n$。这种显式的几何-语义解耦表示使得场景结构变得**可解释、可控且可编辑**。

### 2. 前背景建模：从统一体积到实体级身份保持

密集网格方法将所有场景元素在统一体积中联合生成，缺乏显式的前景/背景分离机制。LatentWorld 采用了根本不同的策略：

- **每个前景演员分配恰好一个潜变量**，以在整个时间序列中维持其身份一致性。论文明确指出，“multiple latents per object tend to split an actor over time”（每个物体分配多个潜变量会导致演员随时间分裂）。
- **背景区域由多个潜变量覆盖**，以捕捉丰富的几何细节并支持局部编辑。

这一设计直接解决了密集体素生成中的实体合并与分裂问题，使得每个前景演员的身份在 4D 序列中保持稳定。

### 3. 动态生成方式：从隐式去噪到显式运动扩散

现有 4D 生成方法（如 **DynamicCity** 的 HexPlane 特征）通常通过逐帧去噪隐式处理运动，或依赖外部启发式控制器，缺乏对场景动力学的显式建模。LatentWorld 引入了一个独立的**运动扩散变换器 $\mathcal{G}_M$**，显式生成自车和全部动态演员的未来轨迹：

$$\{ ( \mathbf{p}_{a,t}, \phi_{a,t} ) \}_{t=1}^{T}, \qquad \mathbf{p}_{a,t} \in \mathbb{R}^3, \ \phi_{a,t} \in \mathbb{R}$$

生成的轨迹直接应用于对应潜变量的位置和朝向，通过统一的运动更新规则实现时序一致的运动传播：

$$( \mathbf{x}_n^t, \boldsymbol{\theta}_n^t ) = \begin{cases} ( \mathbf{R}_{\mathrm{ego}}^{(t)} \mathbf{p}_{n,t} + \mathbf{t}_{\mathrm{ego}}^{(t)}, \ \phi_{n,t} + \Delta\theta_{\mathrm{ego}}^{(t)} ) & \text{if latent } n \text{ is dynamic}, \\ ( \mathbf{R}_{\mathrm{ego}}^{(t)} \mathbf{x}_n^{t-1} + \mathbf{t}_{\mathrm{ego}}^{(t)}, \ \boldsymbol{\theta}_n^{t-1} + \Delta\theta_{\mathrm{ego}}^{(t)} ) & \text{otherwise}. \end{cases}$$

这种显式运动建模带来了两个关键优势：自车运动通过统一变换应用于所有潜变量，保证了背景的跨帧一致性；动态演员的路点预测实现了精确的前景运动控制。

### 4. 可控性：从间接条件到直接潜变量编辑

传统方法通过粗糙的条件信号（如控制轨迹）间接影响生成结果，可控粒度有限。LatentWorld 的接地潜变量表示使得场景编辑变得**直接且精确**：平移或旋转单个演员只需编辑其潜变量的位置 $(x,y,z)$ 或朝向 $\theta$，解码后自动反映在生成的语义占用中（见 Figure 3 和 Figure 4）。背景细节则通过背景潜变量的密度来控制。这种实体级可控性是密集网格方法无法实现的。

### 创新本质：三阶段分解生成

上述四个 changed slots 通过一个统一的**三阶段扩散管道**实现协同：

1. **布局扩散**（$\mathcal{G}_L$）：生成潜变量的粗粒度布局——位置、类别、朝向，建立可解释的 3D 场景结构。
2. **特征扩散**（$\mathcal{G}_F$）：以布局为条件，为每个潜变量注入精细几何特征，实现高保真局部几何。
3. **运动扩散**（$\mathcal{G}_M$）：生成时序轨迹，驱动 4D 场景的动态演化。

这种分解使得场景的**结构、几何和运动**三个维度可以独立控制和编辑，从根本上解决了现有方法中三者耦合导致的不可控和不可解释问题。



LatentWorld 将 4D 场景生成分解为三个解耦的阶段，共享一个统一的**接地潜变量表示**。整个 pipeline 的输入是语义占用体素 $\mathbf{V}$，输出是跨时间步的 4D 语义占用序列。其核心模块关系如 Figure 2 所示，可概括为“编码—生成—解码—运动传播”四步流：

![[assets/figures/papers/paper_list_l2515_https_openaccess_thecvf_com_content_CVPR2026_html_Park_Grounded_Latents/figures/002_Figure_2.jpg]]
*Figure 2: Method Overview. Semantic Voxels to Grounded 3D Latents: A VAE encodes semantic voxels into a sparse, editable latent point set*

1. **语义体素编码为接地潜变量**  
   一个 VAE 编码器 $E$ 将语义占用体素 $\mathbf{V}$ 映射为稀疏的接地潜变量点集 $\mathcal{Z} = \{ (\mathbf{x}_n, c_n, \theta_n, \mathbf{f}_n) \}_{n=1}^N$。每个潜变量包含 3D 位置 $\mathbf{x}$、语义类别 $c$、BEV 朝向 $\theta$ 和几何特征 $\mathbf{f}$。编码过程中，每个前景演员分配恰好一个潜变量以维持身份一致性；背景区域则由多个潜变量覆盖以捕捉细节。

2. **三阶段扩散生成**  
   在潜变量空间中，三个扩散变换器依次生成场景的粗粒度布局、局部几何和未来运动：
   - **布局扩散 $G_L$**：生成潜变量的位置、类别和朝向，建立可解释、可编辑的 3D 布局。
   - **特征扩散 $G_F$**：以布局为条件，为每个潜变量生成精细几何特征 $\mathbf{f}$，捕捉局部形状细节。
   - **运动扩散 $G_M$**：生成自车及全部动态演员在未来 $T$ 个时刻的路点 $\mathbf{p}_{a,t}$ 和朝向 $\phi_{a,t}$。

3. **语义高斯解码**  
   VAE 解码器 $D$ 将潜变量点集解码为语义 3D 高斯 $\mathcal{G}$，再通过 splatting 渲染为语义占用体素。体素中心 $\mathbf{x}$ 的占用率由多高斯覆盖概率给出：
   $$\alpha(\mathbf{x}) = 1 - \prod_{i=1} \bigl(1 - \exp(-\frac{1}{2}(\mathbf{x} - \mathbf{x}_i)^{\top} \pmb{\Sigma}_i^{-1} (\mathbf{x} - \mathbf{x}_i))\bigr)$$
   语义则通过 opacity 和密度加权混合：
   $$\mathbf{e}(\mathbf{x}) = \frac{\sum_i p(\mathbf{x} \mid \mathbf{G}_i) a_i \mathbf{c}_i}{\sum_j p(\mathbf{x} \mid \mathbf{G}_j) a_j}$$

4. **运动传播与 4D 展开**  
   将生成的轨迹应用于对应潜变量：动态演员的潜变量按预测路点和朝向更新，静态背景潜变量仅受自车运动变换。统一的更新规则为：
   $$(\mathbf{x}_n^t, \boldsymbol{\theta}_n^t) = \begin{cases}
   (\mathbf{R}_{\text{ego}}^{(t)} \mathbf{p}_{n,t} + \mathbf{t}_{\text{ego}}^{(t)}, \; \phi_{n,t} + \Delta\theta_{\text{ego}}^{(t)}) & \text{if dynamic} \\
   (\mathbf{R}_{\text{ego}}^{(t)} \mathbf{x}_n^{t-1} + \mathbf{t}_{\text{ego}}^{(t)}, \; \boldsymbol{\theta}_n^{t-1} + \Delta\theta_{\text{ego}}^{(t)}) & \text{otherwise}
   \end{cases}$$
   在每一未来时刻，更新后的潜变量集经解码器 $D$ 产生对应帧的语义占用，从而形成时序一致的 4D 序列。

**关键设计决策**：整个 pipeline 的因果控制节点在于“一个演员一个潜变量”的接地表示。这直接解决了密集体素方法中前景实体合并、闪烁、分裂的瓶颈——因为每个演员的身份被单个潜变量唯一锚定，运动传播时不会发生跨帧身份漂移。同时，布局、特征、运动三阶段的解耦使得场景编辑（如平移/旋转单个演员）只需直接修改对应潜变量的位置或朝向，无需重新生成整个场景。

### 补充图表

![[assets/figures/papers/paper_list_l2515_https_openaccess_thecvf_com_content_CVPR2026_html_Park_Grounded_Latents/figures/001_Figure_1.jpg]]
*Figure 1: Entity-centric 4D scene generation with grounded 3D latents. We present LatentWorld, which introduces a grounded latent representation for controllable, interpretable 3D and 4D scene generation. On the left, we show a generated 3D latent layout in which each actor is a single editable latent with position and BEV orientation, together with generated future waypoints that define motion. On the right, we decode the same latents to semantic Gaussians and splat to voxels across future timesteps, producing coherent 4D scenes with precise foreground movement and stable background structure. Zoom in for detail*



LatentWorld 的生成管道由三个核心阶段构成，每个阶段对应一个扩散变换器，分别负责场景的粗粒度布局、细粒度几何特征和时序运动。以下按数据流顺序阐述关键模块及其公式化设计。

### 语义高斯解码器：从潜变量到体素占用

VAE 解码器 D 将潜变量点集 Z 映射为一组语义高斯，并通过 splatting 渲染为语义占用体素。对于体素中心 x，其被至少一个高斯覆盖的概率（占用率）定义为：

$$
\alpha ( { \bf x } ) = 1 - \prod _ { i = 1 } \bigl ( 1 - \exp ( - { \textstyle \frac { 1 } { 2 } } ( { \bf x } - { \bf x } _ { i } ) ^ { \top } { \pmb \Sigma } _ { i } ^ { - 1 } ( { \bf x } - { \bf x } _ { i } ) ) \bigr )
$$

该公式计算体素 x 不被任何高斯“解释”的概率的补集：乘积项遍历所有高斯，每个高斯的贡献由其马氏距离决定。体素的语义向量则通过周围高斯的透明度与密度加权混合得到：

$$
\mathbf { e } ( \mathbf { x } ) = \frac { \sum _ { i } p ( \mathbf { x } \mid \mathbf { G } _ { i } ) a _ { i } \mathbf { c } _ { i } } { \sum _ { j } p ( \mathbf { x } \mid \mathbf { G } _ { j } ) a _ { j } }
$$

其中 $p(\mathbf{x} \mid \mathbf{G}_i)$ 是高斯 $\mathbf{G}_i$ 在 x 处的概率密度，$a_i$ 为透明度，$\mathbf{c}_i$ 为语义类别向量。这种设计使得每个体素的语义由周围高斯的贡献自然融合，避免了硬分配带来的边界伪影。

### VAE 训练目标

VAE 编码器 E 将语义占用体素 V 压缩为潜变量点集 Z，解码器 D 重建体素 $\hat{\mathbf{V}}$。训练损失由三项组成：

$$
\mathcal { L } ( \hat { \mathbf { V } } , \mathbf { V } ) = \mathcal { L } _ { \mathrm { C E } } + \mathcal { L } _ { \mathrm { L o v a s z } } + \beta \mathcal { L } _ { \mathrm { K L } } ( \mathbf { f } )
$$

- $\mathcal{L}_{\mathrm{CE}}$：交叉熵损失，逐体素监督语义类别预测。
- $\mathcal{L}_{\mathrm{Lovász}}$：Lovász 扩展损失，直接优化语义分割的 mIoU 指标，缓解类别不平衡。
- $\mathcal{L}_{\mathrm{KL}}(\mathbf{f})$：对潜变量几何特征 $\mathbf{f}$ 施加 KL 正则，约束其分布接近标准正态，为后续扩散生成提供规整的潜空间。
- $\beta$：控制正则化强度的超参数。

### 布局扩散变换器 $G_L$

布局扩散阶段生成潜变量的粗粒度属性：位置 $\mathbf{x}_n$、语义类别 $c_n$ 和 BEV 朝向 $\theta_n$。每个潜变量的初始编码为：

$$
\bar { \mathbf { z } } _ { n , 0 } = \left[ X _ { n } , Y _ { n } , Z _ { n } , \sin \theta _ { n } , \cos \theta _ { n } , \mathrm { b i t s } ( c _ { n } ) \right]
$$

- 位置 $(X_n, Y_n, Z_n)$ 直接使用坐标值。
- 朝向 $\theta_n$ 通过正弦和余弦编码，避免角度周期性带来的歧义。
- 类别 $c_n$ 通过二进制位编码 $\mathrm{bits}(c_n)$ 嵌入。

布局扩散变换器 $G_L$ 以标准 $\epsilon$-预测方式训练：

$$
\mathcal { L } _ { \mathrm { l a y o u t } } = \mathbb { E } _ { t , \epsilon } \left\| \epsilon - \mathcal { G } _ { L } ( \bar { \mathbf { z } } _ { n , t } , t ) \right\| _ { 2 } ^ { 2 }
$$

噪声 $\epsilon$ 逐步添加到干净编码 $\bar{\mathbf{z}}_{n,0}$，$G_L$ 学习预测噪声分量。推理时从纯噪声开始迭代去噪，得到完整的潜变量布局。

### 特征扩散变换器 $G_F$

在布局确定后，特征扩散变换器 $G_F$ 为每个潜变量生成细粒度几何特征 $\mathbf{f}_n$。$G_F$ 以布局为条件：在每个去噪时间步，接收当前带噪特征 $\bar{\mathbf{f}}_{n,t}$ 以及潜变量的位置 $\mathbf{x}_n$、朝向 $\theta_n$ 和类别 $c_n$ 的嵌入。这种条件化设计使得几何细节与粗布局保持语义一致，同时允许同一布局产生多样的几何实现（如 Figure 4 所示）。

### 运动扩散变换器 $G_M$

运动扩散阶段生成自车和所有动态演员在未来 $T$ 个时间步的路点和朝向：

$$
\{ ( \mathbf { p } _ { a , t } , \phi _ { a , t } ) \} _ { t = 1 } ^ { T } , \qquad \mathbf { p } _ { a , t } \in \mathbb { R } ^ { 3 } , \ \phi _ { a , t } \in \mathbb { R }
$$

$\mathbf{p}_{a,t}$ 是智能体 $a$ 在时刻 $t$ 的 3D 路点，$\phi_{a,t}$ 为对应的 BEV 朝向。生成轨迹后，潜变量按以下规则更新以传播运动：

$$
( \mathbf { x } _ { n } ^ { t } , \mathbf { \boldsymbol { \theta } } _ { n } ^ { t } ) = \left\{ \begin{array} { l l } { ( \mathbf { R } _ { \mathrm { e g o } } ^ { ( t ) } \mathbf { p } _ { n , t } + \mathbf { t } _ { \mathrm { e g o } } ^ { ( t ) } , \ \phi _ { n , t } + \Delta \theta _ { \mathrm { e g o } } ^ { ( t ) } ) } \\ { \qquad \mathrm { i f ~ l a t e n t } \ n \mathrm { i s } \ \mathrm { d y n a m i c } , } \\ { \left( \mathbf { R } _ { \mathrm { e g o } } ^ { ( t ) } \mathbf { x } _ { n } ^ { t - 1 } + \mathbf { t } _ { \mathrm { e g o } } ^ { ( t ) } , \ { \boldsymbol { \theta } } _ { n } ^ { t - 1 } + \Delta \theta _ { \mathrm { e g o } } ^ { ( t ) } \right) } \\ { \qquad \mathrm { o t h e r w i s e } . } \end{array} \right.
$$

- **动态潜变量**：直接移动到预测路点 $\mathbf{p}_{n,t}$，并更新朝向为 $\phi_{n,t}$，同时叠加自车旋转 $\mathbf{R}_{\mathrm{ego}}^{(t)}$ 和平移 $\mathbf{t}_{\mathrm{ego}}^{(t)}$ 以实现坐标系变换。
- **静态潜变量**：仅受自车运动影响，位置和朝向根据自车的旋转和平移进行刚体变换。

这种显式的运动传播机制确保了前景演员的身份在时序上保持一致，避免了密集体素方法中常见的实体分裂和闪烁问题。

### 外推引导

在生成超出训练分布范围的新潜变量时，LatentWorld 采用均值偏移引导策略，推动新潜变量向前半区集中：

$$
\mu ^ { \prime } = \mu + \eta \lambda \Big ( 1 - \mathrm { c l i p } ( \tilde { x } , 0 , 1 ) ^ { 2 } \Big )
$$

其中 $\mu$ 为去噪器预测的均值，$\tilde{x}$ 为归一化的前向坐标，$\lambda$ 为推力权重，$\eta$ 为步长。二次型偏移 $1 - \mathrm{clip}(\tilde{x},0,1)^2$ 使得靠近前沿的潜变量获得更强的向前推力，从而生成合理的外推布局。消融实验（Table 4）表明 $\lambda=1.0$ 时达到最优的几何+语义 MMD。

### 补充图表

![[assets/figures/papers/paper_list_l2515_https_openaccess_thecvf_com_content_CVPR2026_html_Park_Grounded_Latents/figures/003_Figure_3.jpg]]
*Figure 3: Rotating foreground Gaussians by their latent’s yaw enables interpretable, reliable heading control*



## 实验与关键发现

### 主实验结果

LatentWorld 在 CarlaSC（3D 场景生成）和 Waymo（4D 场景生成）两个基准上均取得最优生成质量，尤其在前景类别上显著优于现有方法。

**CarlaSC 3D 场景生成**（Table 1）：
- 几何 MMD↓ 均值 6.44，语义 MMD↓ 均值 11.30，联合指标均值 6.69，三项均为所有方法中最低。
- 与 SemCity（Lee et al., CVPR 2024）、XCube（Ren et al., CVPR 2024）、PDD（Liu et al., ECCV 2024）等 3D 基线相比，LatentWorld 在前景类别上的提升尤为显著，验证了接地潜变量对实体身份保持的有效性。

**Waymo 4D 场景生成**（Table 2）：
- 几何 MMD↓ 均值 1.62，语义 MMD↓ 均值 1.50，联合指标均值 0.96，全面超越 DynamicCity。
- DynamicCity 采用 HexPlane 特征进行密集表示，其生成结果常出现前景闪烁、车辆分裂等问题；LatentWorld 通过“一个演员一个潜变量”的设计保持身份分离，并结合显式自车运动变换，实现了稳定的背景结构和连贯的前景运动（见 Figure 6 定性对比）。

![[assets/figures/papers/paper_list_l2515_https_openaccess_thecvf_com_content_CVPR2026_html_Park_Grounded_Latents/figures/008_Figure_6.jpg]]
*Figure 6: Waymo qualitative comparison. DynamicCity’s generations exhibit foreground flicker, cause frequent vehicle splitting, and ego turns yield background inconsistencies across frames. LatentWorld’s grounded latents, with one latent per actor and explicit ego transforms, preserve identity and inter-actor separation, giving stable trajectories and consistent background. Zoom in for details*

**公平性说明**：所有方法在相同数据集划分和统一 MMD 指标下比较，LatentWorld 使用相同的 VAE 编码器进行特征提取，确保对比公平。

### 消融实验

**潜变量数量消融**（Table 3，CarlaSC）：
- 潜变量数量从 256 增至 1024，重建 mIoU 从 85.45 单调升至 94.71，几何 MMD 从 13.32 降至 6.38，表明更多潜变量有利于捕捉细粒度几何。
- 但语义 MMD 在极高数量时恶化（10.95→12.36），可能源于潜变量过密导致语义混叠。综合几何+语义 MMD 在 768 个潜变量时达到最优（6.69），被选为默认配置。

**外推引导权重消融**（Table 4）：
- 外推时对去噪器均值施加推力权重 λ，λ=1.0 时几何+语义 MMD 达最优（1.04）。λ 过小推力不足，过大则导致新潜变量过度集中，均使性能下降。

### 失败模式分析

与密集体素生成方法相比，LatentWorld 的接地潜变量设计显著减少了实体合并（merging）、闪烁（flickering）和分裂（splitting）等常见失败模式（置信度 0.95）。这些失败模式在 DynamicCity 的 Waymo 生成结果中明显可见（Figure 6），而 LatentWorld 通过显式实体分离和运动传播有效缓解。

### 局限性

1. **运动时长限制**：当前运动模型限制为未来 20 步（10Hz），可能无法覆盖长时序多场景需求。
2. **潜变量数量固定**：前背景潜变量数量需预先设定，在非常稀疏或极度密集场景下可能不是最优。
3. **标注依赖**：训练依赖于语义占用真值标注，向新领域迁移时可能面临标注缺失问题。

### 补充图表

![[assets/figures/papers/paper_list_l2515_https_openaccess_thecvf_com_content_CVPR2026_html_Park_Grounded_Latents/figures/005_Table_1.jpg]]
*Table 1: CarlaSC scene generation. MMD↓ between generated and real features using geometry, semantics, and joint (geometry+semantics) metrics; lower is better. LatentWorld consistently achieves the best performance, with large gains on foreground classes*

![[assets/figures/papers/paper_list_l2515_https_openaccess_thecvf_com_content_CVPR2026_html_Park_Grounded_Latents/figures/006_Table_2.jpg]]
*Table 2: Waymo 4D scene generation. MMD↓ under geometry, semantics, and joint metrics. LatentWorld outperforms DynamicCity overall, with clear improvements on foreground categories*

![[assets/figures/papers/paper_list_l2515_https_openaccess_thecvf_com_content_CVPR2026_html_Park_Grounded_Latents/figures/007_Figure_5.jpg]]
*Figure 5: Factorized generation with grounded latents. Row 1: generated latent layouts with generated actor waypoints, capturing coarse structure and multi-actor placement. Row 2: feature generation and decoding to semantic Gaussians, splatted to voxels, producing diverse, realistic 3D scenes faithful to the layout. Row 3: applying the generated motion to the same latents produces coherent 4D sequences with precise actor movement and stable background. Zoom in for details*

![[assets/figures/papers/paper_list_l2515_https_openaccess_thecvf_com_content_CVPR2026_html_Park_Grounded_Latents/figures/009_Table_3.jpg]]
*Table 3: Ablation on the number of latents in CarlaSC [46]. mIoU↑: reconstruction; MMD↓: generation*

![[assets/figures/papers/paper_list_l2515_https_openaccess_thecvf_com_content_CVPR2026_html_Park_Grounded_Latents/figures/010_Table_4.jpg]]
*Table 4: Ablation on outpainting push weight λ. MMD↓: generation*

![[assets/figures/papers/paper_list_l2515_https_openaccess_thecvf_com_content_CVPR2026_html_Park_Grounded_Latents/figures/004_Figure_4.jpg]]
*Figure 4: Left: Generated layout and semantic grid. Right: We manually arrange the layout to simulate a complex traffic scene and sample two sets of latent features to decode. LatentWorld’s grounded latent representation enables interpretable, explicit control of scene elements, with high-fidelity geometric variations captured by our feature generation model*



## 定位与知识库关联

**核心瓶颈与设计动机**  
现有 3D/4D 场景生成方法普遍采用密集对齐网格的潜变量表示（如体素、三平面、HexPlane），所有场景元素在统一体积中联合生成，缺乏显式的实体分离。这导致前景演员在生成中频繁出现合并、闪烁、分裂等失败模式，且难以实现精细、可靠的前背景控制。**LatentWorld** 针对这一瓶颈，提出以稀疏、接地的 3D 潜变量点集替代密集网格潜变量，使每个前景演员由恰好一个潜变量表示以维持身份，背景则由多个潜变量覆盖以捕捉细节——这一表示转换是方法的核心因果旋钮。

**与 3D 场景生成基线的对比**  
在 3D 场景生成层面，**SemCity**（Lee et al., CVPR 2024）采用 triplane 扩散，**XCube**（Ren et al., CVPR 2024）使用稀疏体素层次表示，**PDD**（Liu et al., ECCV 2024）通过金字塔扩散生成场景。这些方法虽然引入了不同程度的稀疏性或层次结构，但仍未将前景实体作为独立、可操控的单元进行建模。LatentWorld 的接地潜变量直接编码每个实体的位置、语义类别和 BEV 朝向，使得布局生成与几何细节生成解耦，从而在 CarlaSC 数据集上取得显著更优的生成质量（Table 1：几何+语义 MMD 6.69，前景类别提升尤为明显）。

**与 4D 场景生成基线的对比**  
在 4D 动态场景生成层面，**Occ-Sora**（Wang et al., arXiv 2024）使用密集网格潜变量进行时空生成，**DynamicCity** 采用 HexPlane 特征表示。两者均通过逐帧去噪隐式处理运动，缺乏对单个实体运动轨迹的显式建模。LatentWorld 引入独立的运动扩散 Transformer $G_M$，显式生成自车与全部动态演员的未来路点与朝向，并通过自车运动变换统一更新所有潜变量（动态演员按预测路点移动，静态背景随自车刚性变换），从而在 Waymo 数据集上全面超越 DynamicCity（Table 2：几何+语义 MMD 0.96 vs. DynamicCity），且定性结果（Figure 6）显示 LatentWorld 有效消除了 DynamicCity 中常见的前景闪烁、车辆分裂和自车转弯时的背景不一致问题。

**适用边界与局限**  
1. **时间范围限制**：当前运动模型限制为未来 20 步（10Hz），可能无法覆盖长时序多场景需求（如完整变道、长距离跟车）。  
2. **潜变量数量固定**：前背景潜变量数量需预先设定，在非常稀疏（如空旷高速公路）或极度密集（如拥挤交叉口）场景下可能不是最优配置。消融实验（Table 3）表明 768 个潜变量在 CarlaSC 上达到几何+语义 MMD 最优平衡点，但该数值依赖于具体场景密度分布。  
3. **标注依赖**：训练依赖于语义占用真值标注，向新领域（如室内机器人、行人交互场景）迁移时可能面临标注缺失问题。

**开放问题与潜在延伸**  
- **自适应潜变量分配**：能否根据场景密度动态调整潜变量数量，以覆盖从稀疏到密集的连续场景谱系？  
- **跨领域泛化**：该框架能否推广到非驾驶场景（如室内多智能体交互、动态物体操控），其“一个实体一个潜变量”的假设是否仍然成立？  
- **弱监督学习**：如何结合自监督或弱监督信号（如多视图一致性、运动线索）减少对稠密语义占用的依赖？  
- **演员交互建模**：当前运动模型独立生成各演员轨迹，超车、避让等交互行为是否需要在模型中显式建模以提升物理一致性？



## 原文 PDF

![[paperPDFs/CVPR_2026/Grounded_Latents_for_Entity_Centric_4D_Scene_Generation.pdf]]
