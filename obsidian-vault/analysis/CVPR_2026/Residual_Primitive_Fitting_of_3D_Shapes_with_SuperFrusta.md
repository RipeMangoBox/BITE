---
title: Residual Primitive Fitting of 3D Shapes with SuperFrusta
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/Residual_Primitive_Fitting_of_3D_Shapes_with_SuperFrusta.pdf
code_link: "https://github.com/kmammou/v-hacd"
aliases:
- SRPFR
- RPF3SS
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
core_operator: SuperFrustum作为统一的8参数解析基元，兼具表达性、可编辑性和可微性；ResFit通过交替进行全局形态学形状分解与局部基元优化，使分解适应基元的表达能力，从而在几乎不损失重构精度的情况下大幅减少基元数量。
primary_logic: 将具有连续表达能力的可微基元与迭代残差拟合相耦合，使全局形状线索与局部参数优化相互适应，从而系统性地前移重构-简洁性的帕累托前沿。
claims:
- SuperFrustum仅用8个参数即可平滑变换于立方体、圆柱、圆锥、球体及弯曲、空心等复杂形态之间，且其SDF几乎处处可微。
- 在3DGen-Prim和Toys4K基准上，ResFit将IoU分别提升约6个和9个点，同时使用的基元数量仅为Marching Primitives的约一半，体素重叠减少超过3倍。
- 消融实验表明，SuperFrustum+平滑联合在重建精度和程序质量上全面优于立方体、超二次曲面等基元；ResFit交替优化策略显著优于一次性拟合，MSD分解优于CoACD。
- 3DGen-Prim 上 IoU (%) = 88.74
---

# Residual Primitive Fitting of 3D Shapes with SuperFrusta

> [!tip] 核心洞察
> 将具有连续表达能力的可微基元与迭代残差拟合相耦合，使全局形状线索与局部参数优化相互适应，从而系统性地前移重构-简洁性的帕累托前沿。

| 字段 | 内容 |
|------|------|
| 中文题名 | 基于SuperFrusta的3D形状残差基元拟合 |
| 英文题名 | Residual Primitive Fitting of 3D Shapes with SuperFrusta |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2512.09201) · [Code](https://github.com/kmammou/v-hacd) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction |
| Method | SuperFrustum and Residual Primitive Fitting (ResFit) |
| Dataset | 3DGen-Prim, Toys4K |

> [!tip] 效果简介
> - 3DGen-Prim 上，IoU (%) 88.74 vs ~82.64 (MPS) (+6.10)；#Primitives 23.98 vs 42.96 (MPS) (-18.98 (少44%))；Overlap Ratio 0.210 vs 0.684 (MPS) (-0.474 (减少69%))。
> - Toys4K 上，IoU (%) 89.92 vs ~80.62 (MPS) (+9.30)；#Primitives 23.67 vs 30.62 (MPS) (-6.95 (少23%))。

## 概述

三维形状的基元化装配——用少量解析基元精确表示复杂几何——是计算机图形学与视觉中的长期难题。其核心瓶颈在于：**现有解析基元表达性有限**，超二次曲面等传统基元难以拟合弯曲、空心等复杂形态；**分析驱动方法**（如近似凸分解ACD）对基元表达能力不敏感，易产生过度分割；**优化驱动方法**在高度非凸损失下需要大量基元才能达到可接受的重构精度，导致重构保真度与基元数量之间的帕累托前沿长期停滞。

本文提出两项关键创新来系统性地前移这一前沿：

1. **SuperFrustum**：一个仅用8个参数的统一解析基元。其有符号距离函数（SDF）几乎处处可微，能够平滑变换于立方体、圆柱、圆锥、球体及弯曲、空心等复杂形态之间（Figure 2），兼具表达性、可编辑性和可微性。

2. **ResFit（残差基元拟合）**：一种无监督推理过程，交替进行全局形态学形状分解（MSD）与局部基元优化。通过迭代提取残差并添加新基元，使分解适应基元的表达能力，从而在几乎不损失重构精度的情况下大幅减少基元数量（Figure 3）。

核心洞见在于：**将具有连续表达能力的可微基元与迭代残差拟合相耦合，使全局形状线索与局部参数优化相互适应**。

主要实验结果（Table 1）验证了该方法的有效性：在3DGen-Prim和Toys4K基准上，ResFit将IoU分别提升约6个和9个点，同时使用的基元数量仅为Marching Primitives（MPS, Liu et al., CVPR 2023）的约一半，体素重叠减少超过3倍。消融实验进一步证实，SuperFrustum+平滑联合在重建精度和程序质量上全面优于立方体、超二次曲面等基元；ResFit交替优化策略显著优于一次性拟合；MSD分解比CoACD（Wei et al., ACM TOG 2022）更适合SuperFrustum初始化。

## 背景与动机

### 基元装配：从解析表示到程序化建模

用一组简单几何基元（如立方体、球体、圆柱体）来逼近复杂三维形状，是计算机图形学与几何处理中的经典命题。这种“基元装配”（primitive assembly）不仅产生高度紧凑的形状表示，还天然支持可编辑性、语义分解和程序化建模，因而在资产创建、物理仿真、CAD逆向工程等场景中具有广泛需求。

然而，基元装配面临一个根本性的两难：**重构精度与基元简洁性之间的帕累托前沿**。使用少量基元往往损失细节，而追求高保真度则导致基元数量膨胀、重叠严重，削弱装配的可解释性和编辑价值。这一矛盾构成了该领域的核心瓶颈。

### 现有方法的两个阵营及其局限

当前方法大致分为两类，各自受困于不同的短板：

**优化驱动的方法**（如 *Marching Primitives*，Liu et al., CVPR 2023）将基元装配形式化为一个全局优化问题，通过梯度下降联合优化所有基元参数。这类方法对基元的表达能力高度敏感：当使用简单基元（如立方体、超二次曲面）时，为覆盖复杂几何形态，优化过程被迫引入大量基元，导致严重的体素重叠和冗余。其根本原因在于，**高度非凸的损失景观使得优化器无法用少量基元找到全局最优解**，而简单基元有限的形变能力加剧了这一问题。

**分析驱动的方法**（如基于近似凸分解 ACD 的管线）则先对形状进行几何分区，再在每个区域内拟合基元。这类方法对基元类型不敏感——无论使用立方体还是更复杂的基元，分区策略本身是固定的。这导致一个悖论：**分解过程不了解基元的表达能力，常常将本可由单个表达性基元覆盖的区域过度分割为多个凸块**，产生语义上碎片化的装配。例如，CoACD（Wei et al., ACM TOG 2022）倾向于沿轴对齐方向切割非凸结构，将自行车轮胎或碗口边缘等连贯形态切分为大量碎片。

### 核心缺口：基元表达力与分解策略的脱节

上述两类方法的共同症结在于：**基元表达能力和形状分解策略相互孤立**。优化驱动方法让基元在全局损失下“硬拟合”，却缺乏有效的初始化来引导搜索；分析驱动方法先行固定分区，却不考虑后续基元能否高效覆盖这些区域。这导致无论哪条路线，重构-简洁性的帕累托前沿都被限制在次优水平。

更深层地看，现有解析基元本身的表达能力也构成约束。超二次曲面（Superquadrics）虽比立方体灵活，但仅用约11个参数，仍无法表示空心、弯曲、环状等常见形态。Demoscene社区提出的SuperPrimitive统一了多种实体，但其参数化并非为逆建模设计，可微性和优化稳定性不足。因此，**缺少一种同时满足表达性、紧凑性、可微性和可编辑性的基元**，作为连接形状分析与参数优化的桥梁。

### 本文动机与核心思路

针对上述缺口，本文提出两个相互耦合的贡献：

1. **SuperFrustum**：一个仅用8个参数的统一解析基元，其有符号距离函数（SDF）几乎处处可微，可在立方体、圆柱、圆锥、球体及弯曲、空心等形态之间平滑过渡。这为梯度优化提供了丰富而稳定的形变空间。

2. **ResFit（残差基元拟合）**：一种无监督的迭代推断流程，交替执行全局形态学形状分解与局部基元优化。分解阶段感知残差形状的厚度分布，为SuperFrustum提供语义合理的初始化种子；优化阶段在分解引导的空间掩模内精细调整参数；随后提取未覆盖的残差，进入下一轮迭代。

这一设计的核心洞察在于：**让分解适应基元的表达能力，让优化受益于分解的结构线索**——二者相互适应，从而系统性地前移重构-简洁性的帕累托前沿。实验表明，该方法在3DGen-Prim和Toys4K基准上将IoU分别提升约6和9个百分点，同时使用的基元数量仅为Marching Primitives的约一半，体素重叠减少超过3倍。

## 核心创新

本文的核心创新在于从基元表达性与拟合策略两个维度同时突破，系统性地前移了重构精度与基元简洁性之间的帕累托前沿。具体而言，方法引入了两个紧密耦合的“changed slots”：

**1. 基元类型：从有限表达到连续形态谱系**

现有基元装配方法受限于基元的表达能力：**Cuboids** 仅能表示轴对齐长方体，**Superquadrics**（Paschalidou et al., CVPR 2019）虽引入圆度和锥度但无法生成空心或弯曲形态，而 **SuperPrimitive** 等Demoscene基元缺乏可微性支持梯度优化。这些限制迫使方法要么使用大量基元拼凑复杂几何，要么在重构精度上妥协。

本文提出 **SuperFrustum**——一个仅含8个参数的统一解析SDF基元：

$$SF(\mathbf{p}) = f(\mathbf{p}; \theta), \quad \theta = (\mathbf{s}, r, d, t, b, o)$$

其中各向异性尺度 $\mathbf{s}$、轮廓圆度 $r$、膨胀 $d$、锥度 $t$、鼓胀 $b$ 和洋葱壳厚度 $o$ 共同控制基元形态。这8个参数使单一公式可平滑变换于立方体、圆柱、圆锥、球体及环形变体之间，并生成弯曲、空心、平滑封顶等复杂形态（见 Figure 2）。其SDF几乎处处可微，支持鲁棒的梯度驱动逆向建模。

消融实验（Table 2）证实了这一设计的关键作用：SuperFrustum在IoU、Chamfer Distance和基元数量上全面优于Cuboids、Superquadrics和SuperPrimitive；配合平滑联合算子后，性能进一步提升至IoU 88.37、CD 0.147，仅需约21个基元。

**2. 拟合策略：从一次性优化到分析-优化交替迭代**

传统方法（如 **Marching Primitives**，Liu et al., CVPR 2023）采用一次性全局优化，在高度非凸的损失景观下难以找到简洁装配；分析驱动的方法（如基于CoACD的分解）则对基元表达能力不敏感，容易产生过度分割。

本文提出 **ResFit**（Residual Primitive Fitting）——一种无监督的交替迭代策略（Figure 3）：首先通过形态学形状分解（MSD）从当前残差体中提取厚度均匀的连通区域作为候选种子；然后对这些区域进行PCA姿态估计以初始化SuperFrustum参数；接着通过分解感知的可微优化（含曲率加权重构损失、Gumbel-Softmax基元数量损失和质量正则化）精炼参数；最后通过硬剪枝移除对目标函数贡献为负的基元。残差体被提取后，循环进入下一轮基元添加。

这种交替机制使全局形状线索与局部参数优化相互适应：分解为优化提供结构合理的初始化，优化则根据基元的实际表达能力调整装配。消融实验（Table 3）表明，ResFit交替策略显著优于单阶段一次性拟合；MSD分解相比CoACD（Wei et al., ACM TOG 2022）更适合SuperFrustum初始化，获得更高重构精度和更少基元。

**3. 协同效应：帕累托前沿的系统性前移**

SuperFrustum的表达连续性与ResFit的迭代残差适应形成正向反馈：表达能力强的基元使每轮拟合能解释更多几何，减少所需基元数量；交替策略则确保新基元精准补充残差区域，避免冗余。这一协同在实验中体现为：在3DGen-Prim上IoU提升6.1个点（88.74 vs. 82.64），同时基元数量减少44%（23.98 vs. 42.96）；在Toys4K上IoU提升9.3个点，基元数量减少23%（Table 1）。体素重叠率更是从0.684降至0.210，降幅达69%，表明装配的语义可解释性显著增强。

## 整体框架

ResFit 的核心思想是将**全局形状分析**与**局部基元优化**交替进行，使分解过程主动适应基元的表达能力，从而在几乎不损失重构精度的前提下大幅减少基元数量。整个流水线围绕一个统一的目标函数展开：

$$z ^ { * } = \arg \max _ { z } \mathcal { O } ( x , z ) = \arg \max _ { z } \big[ \mathcal { R } ( x , E ( z ) ) - \alpha \vert z \vert \big]$$

其中 $x$ 为输入形状，$z$ 为基元装配，$E(z)$ 为装配体导出的隐式场，$\mathcal{R}$ 衡量重构误差，$|z|$ 为基元数量，$\alpha$ 控制简洁性权重。ResFit 通过迭代优化该目标，逐步逼近重构精度与程序简洁性的帕累托最优。

### 输入与输出

- **输入**：水密三角网格，假设无自相交。
- **输出**：一组紧凑的 SuperFrustum 基元装配，每个基元由 8 个连续参数定义，辅以空间姿态和存在变量，可直接导出为可编辑的程序化表示。

### 核心流水线

ResFit 的推理过程由五个模块构成循环迭代（Figure 3）：

![[assets/figures/papers/paper_list_l2090_https_arxiv_org_abs_2512_09201/figures/003_Figure_3.jpg]]
*Figure 3: ResFit infers parsimonious assemblies by interleaving shape analysis and primitive optimization. Shape decomposition provides initial primitives, which are refined with decompositionaware optimization. Residual unexplained volumes are then extracted and seeded with new primitives*

1. **残差提取（Residual Extraction）**  
   将当前装配体从目标形状中减去，生成新的残差体。首轮迭代时，残差体即为完整输入形状。

2. **形态学形状分解（MSD）**  
   对残差体进行迭代侵蚀-膨胀操作，提取具有均匀厚度的联通区域，并按厚度排序作为候选基元种子。MSD 的关键优势在于其提取的区域天然适配 SuperFrustum 的参数化形式，避免了传统近似凸分解（如 CoACD）的过度分割问题（Figure 4）。

3. **SuperFrustum 初始化**  
   对 MSD 提取的每个区域点集进行 PCA 分析，确定基元的主轴方向与圆柱度指标，据此设定 SuperFrustum 的初始姿态、各向异性尺度和形态参数，为后续梯度优化提供合理起点。

4. **分解感知优化（Decomposition-Aware Optimization）**  
   通过梯度下降最小化多目标损失函数 $\mathcal{L}_{\mathrm{total}}$，同时优化所有基元的连续参数和存在概率。该阶段包含两个子步骤：
   - **可微优化**：以曲率加权的占据概率损失 $\mathcal{L}_{\mathrm{rec}}$ 驱动基元参数更新，辅以基元数量损失（Gumbel-Softmax）和质量损失（重叠惩罚 + 联合一致性正则）抑制冗余。
   - **离散剪枝**：贪婪地移除对目标函数 $\mathcal{O}$ 贡献为负的基元，进一步精简装配。

5. **迭代循环**  
   优化后的装配体用于更新残差，回到步骤 1 开始新一轮基元添加。多轮迭代使基元逐步重分配到残差区域，同时剪除不必要的部分。

### 关键设计决策

- **交替而非一次性**：与单阶段全局拟合不同，ResFit 的交替策略让形状分析为优化提供结构先验，优化反过来修正分析的偏差，二者相互适应。消融实验（Table 3）证实该策略在 IoU 和重叠度上均显著优于一次性拟合。
- **平滑联合算子**：基元间使用递归平滑联合（smooth union）组合，而非硬性布尔并集，既保持可微性，又通过平滑过渡减少基元间的视觉伪影。
- **曲率感知监督**：优化时以主曲率加权采样点，使梯度信号集中于几何细节丰富的区域（如边缘、尖角），避免平坦区域主导损失。

整个流水线为无监督方法，无需训练数据，仅依赖输入网格的几何信息即可完成推理。

## 核心模块与公式推导

### 3.1 问题形式化

基元装配的目标是寻找一组基元参数 $z$，使其最大化目标函数 $\mathcal{O}(x,z)$：

$$z^* = \arg\max_z \mathcal{O}(x,z) \tag{1}$$

目标函数显式地权衡重构精度与程序简洁性：

$$\mathcal{O}(x,z) = \mathcal{R}(x, E(z)) - \alpha|z| \tag{2}$$

其中 $\mathcal{R}$ 为重构误差，$E(z)$ 为基元装配 $z$ 生成的隐式场，$|z|$ 为基元数量，$\alpha$ 控制简洁性权重。这一形式化将基元装配问题转化为一个结构化优化问题，其核心挑战在于：当基元表达能力有限时，需要大量基元才能覆盖复杂几何（重构-简洁性帕累托前沿不佳）。

### 3.2 SuperFrustum：统一可微解析基元

SuperFrustum 是整个方法的核心创新——一个仅用 **8 个连续参数**定义的统一解析 SDF 基元：

$$SF(\mathbf{p}) = f(\mathbf{p};\theta), \quad \theta = (\mathbf{s}, r, d, t, b, o) \tag{3}$$

各参数含义如下：
- **$\mathbf{s} \in \mathbb{R}^3$**：各向异性轴向缩放，控制基元在三个主轴方向的尺度；
- **$r$**：轮廓圆度（profile roundness），控制截面从方形到圆形的连续过渡（使基元可平滑变换于立方体与圆柱之间）；
- **$d$**：膨胀量（dilation），控制基元整体的径向扩展；
- **$t$**：锥度（taper），控制基元沿主轴方向的线性收窄或扩张；
- **$b$**：鼓胀量（bulge），引入沿主轴的二次曲面弯曲；
- **$o$**：洋葱壳厚度（onion thickness），控制空心壳体的壁厚，使基元可表示空心形态。

该 SDF 几乎处处可微（C⁰ 连续），使得梯度下降可直接作用于全部 8 个参数。如 Figure 2 所示，同一公式可平滑变换于立方体、圆柱、圆锥、球体及弯曲、空心等复杂形态之间——这种“连续形态空间”的覆盖能力是立方体（离散）和超二次曲面（SQ，仅能控制圆度/锥度）无法比拟的。

![[assets/figures/papers/paper_list_l2090_https_arxiv_org_abs_2512_09201/figures/002_Figure_2.jpg]]
*Figure 2: SuperFrustum— An Expressive, Compact & Differentiable Primitive. SuperFrustum is a unified analytic SDF primitive with only 8 parameters controlling dilation, taper, bulge, onion-like hollowing, profile roundness, and axial scaling. Its SDF is C0- continuous and fully differentiable (almost eveywhere) with respect to all parameters, enabling robust inverse modeling and gradient-based optimization. As shown on the right, these parameters allow a single formulation to morph smoothly across common solids—cuboids, cylinders, cones, spheres, and toroidal variants—and to produce more complex shapes such as bent, hollow, or smoothly capped forms*

**平滑联合组合算子**。多个 SuperFrustum 通过递归平滑联合算子 $U$ 组合成最终的隐式场 $\mathcal{F}$：

$$\mathcal{F}_1(\mathbf{p}) = g_1(\mathbf{p}), \quad \mathcal{F}_{k+1}(\mathbf{p}) = U(\mathcal{F}_k(\mathbf{p}), g_{k+1}(\mathbf{p}); \beta_k) \tag{4}$$

其中 $g_i$ 为第 $i$ 个基元经刚体变换后的 SDF，$\beta_k$ 控制平滑过渡区域的宽度。平滑联合（而非硬性布尔并集）使得基元间的接缝处产生可微的过渡带，既有利于梯度传播，也减少了视觉上的生硬拼接。

### 3.3 形态学形状分解（MSD）

MSD 为 SuperFrustum 的优化提供初始化种子。其核心思想是：**迭代地从形状中剥离“最厚”的连通区域**，这些区域天然适合用单个 SuperFrustum 拟合。

给定当前残差形状的 SDF $f_k$（初始 $f_1 \equiv f$ 为目标形状的 SDF），MSD 通过侵蚀操作提取最厚区域：

$$\Gamma_k \subseteq \{\mathbf{p} \in \Omega \mid f(\mathbf{p}) \leq \tau\}, \quad \Gamma_k \text{ 为连通分量} \tag{5}$$

其中侵蚀半径 $|\tau|$ 逐步增大，直至找到仍保持连通的区域 $\Gamma_k$。该区域即为当前残差中“最厚且连通”的部分。提取后更新残差：

$$f_{k+1}(\mathbf{p}) = f_k(\mathbf{p}) \setminus R_k \tag{6}$$

其中 $R_k$ 为从 $\Gamma_k$ 膨胀恢复的区域。对每个提取的区域，利用 PCA 分析点集的主方向与圆柱度，确定 SuperFrustum 的初始姿态、主轴与尺度参数。

如 Figure 4 所示，MSD 与 CoACD 的关键差异在于：MSD 按**厚度**而非**凸性**进行分割，因此能够保留非凸但语义一致的结构（如自行车轮胎的环形、猫尾的弯曲），而 CoACD 往往将这些结构过度分割为多个轴对齐的凸碎片。

![[assets/figures/papers/paper_list_l2090_https_arxiv_org_abs_2512_09201/figures/004_Figure_4.jpg]]
*Figure 4: Morphological Shape Decomposition (MSD) iteratively extracts connected regions of similar thickness. Top: successive MSD partitions of a input mesh. Bottom: MSD yields regions that form suitable initialization seeds for SuperFrusta —capturing non-convex structures such as bicycle tires (left), a cat’s curved tail (center), and bowl rims (right). In contrast, CoACD over-partitions these regions into many convex fragments, often using axis-aligned cuts that produce semantically misaligned parts*

### 3.4 分解感知优化

优化阶段在 MSD 提供的初始化基础上，通过梯度下降调整所有基元参数以最大化目标函数 $\mathcal{O}$。优化分为两个阶段：**可微阶段**与**离散剪枝阶段**。

**可微阶段**最小化以下总损失：

$$\mathcal{L}_{\text{total}} = \mathcal{L}_{\text{rec}} + \lambda_{\text{count}}\mathcal{L}_{\text{count}} + \lambda_{\text{qual}}\mathcal{L}_{\text{qual}} \tag{8}$$

**重构损失** $\mathcal{L}_{\text{rec}}$ 采用曲率加权的占据概率监督，仅在空间掩模 $\mathcal{M}$（由当前装配体与目标形状的并集定义）内计算：

$$w(\mathbf{p}) = 1 + \sigma(\kappa(\mathbf{p})), \quad \mathcal{L}_{\text{rec}} = \frac{1}{|\mathcal{M}|} \sum_{\mathbf{p} \in \mathcal{M}} w(\mathbf{p})(\hat{o}(\mathbf{p}) - o(\mathbf{p}))^2 \tag{7}$$

其中 $\kappa(\mathbf{p})$ 为主曲率，$\sigma$ 为映射函数。曲率加权使优化更关注高曲率的精细结构（如边缘、尖角），避免平滑区域主导梯度。空间掩模 $\mathcal{M}$ 限制监督范围，防止优化将基元推向远离目标形状的区域。

**基元数量损失** $\mathcal{L}_{\text{count}}$ 通过 Gumbel-Softmax 松弛对每个基元引入“存在概率”，鼓励模型自动关闭冗余基元。

**质量损失** $\mathcal{L}_{\text{qual}}$ 包含两项：
- **重叠惩罚**：$\max(1, \sum_i \hat{o}_i(\mathbf{p}))$，惩罚多个基元在同一位置的占据值之和超过 1；
- **联合一致性**：$\hat{o}(\mathbf{p}) - \min(\sum_i \hat{o}_i(\mathbf{p}), 1)$，惩罚平滑联合引入的额外混合区域（即最终占据概率大于各基元占据值之和的部分）。

**离散剪枝阶段**在可微优化收敛后，贪婪地评估每个基元对目标函数 $\mathcal{O}$ 的边际贡献，移除贡献为负的基元，进一步精简装配。

### 3.5 ResFit 交替迭代流程

ResFit 的核心机制是将上述模块串联为**交替迭代**过程（Figure 3）：
1. 对当前残差体执行 MSD，提取最厚连通区域；
2. 为每个区域初始化一个 SuperFrustum，加入当前装配；
3. 执行分解感知优化（可微阶段 + 离散剪枝），调整所有基元参数；
4. 将优化后的装配体从目标形状中减去，提取新的残差体；
5. 若残差体积仍显著，回到步骤 1。

这一交替策略的关键在于：**形状分解感知基元的表达能力**（MSD 按厚度而非凸性分割，适配 SuperFrustum 的形态空间），**局部优化又反哺全局形状理解**（优化后的基元更准确地覆盖已解释区域，使残差更清晰地暴露未解释结构）。消融实验（Table 3）证实，这种交替策略显著优于一次性拟合所有基元的单阶段方法。

## 实验与分析

### 主实验结果

本文在3DGen-Prim和Toys4K两个基准数据集上评估了ResFit的重构精度与程序简洁性，并与**Marching Primitives**（MPS, Liu et al., CVPR 2023）、**Primitive Anything**（PA, Ye et al., 2025）等方法进行了全面对比（Table 1）。

![[assets/figures/papers/paper_list_l2090_https_arxiv_org_abs_2512_09201/figures/005_Table_1.jpg]]
*Table 1: Evaluation on 3DGen-Prim [47] and Toys4K [30] datasets. Our method achieves the best reconstruction and program quality scores simultaneously—improving IOU by 6–9 points while using roughly half as many primitives. Gold = best, Silver = second best*

在重构精度方面，ResFit在3DGen-Prim上取得了88.74%的IoU，较MPS（约82.64%）提升**6.10个点**；在Toys4K上取得了89.92%的IoU，较MPS（约80.62%）提升**9.30个点**。更关键的是，这一精度优势并非以牺牲简洁性为代价——ResFit在3DGen-Prim上仅使用23.98个基元，而MPS需要42.96个（减少**44%**）；在Toys4K上使用23.67个基元，而MPS需要30.62个（减少**23%**）。同时，ResFit的基元间体素重叠率仅0.210，远低于MPS的0.684（减少**69%**），表明其装配具有更高的程序质量。

定性结果（Figure 5）进一步印证了上述结论：ResFit生成的基元装配在几何保真度上明显优于MPS和PA，且基元之间重叠少、语义对齐度高，能够捕捉自行车轮胎的环形结构、猫尾的弯曲形态等复杂几何。

![[assets/figures/papers/paper_list_l2090_https_arxiv_org_abs_2512_09201/figures/006_Figure_5.jpg]]
*Figure 5: Our method reconstructs target shapes with high geometric fidelity and produces more interpretable assemblies, using compact, minimally-overlapping primitives. In contrast, Primitive Anything [45] (PA) and Marching Primitives [18] (MPS) often lose fine structure and generate assemblies with substantial primitive overlap*

### 消融实验

#### 基元表达性消融

Table 2系统比较了不同基元类型在相同ResFit框架下的性能。结果表明，**SuperFrustum**在IoU、Chamfer Distance和基元数量上全面优于立方体（Cuboids）、超二次曲面（Superquadrics, SQ, Paschalidou et al., CVPR 2019）和SuperPrimitive（SP）。进一步结合平滑联合算子（smooth union）后，SuperFrustum的性能达到最优：IoU 88.37，CD 0.147，基元数量21.46，重叠率0.199。这一消融直接验证了SuperFrustum的8参数连续表达能力是重构-简洁性帕累托前沿前移的关键使能因素。

#### 拟合策略与分解方法消融

Table 3验证了ResFit交替优化策略和MSD分解方法的有效性。将ResFit的交替优化替换为一次性拟合（single-shot fitting），IoU和重叠度均显著恶化，说明**全局形状分析与局部基元优化的交替迭代**对于发现简洁装配至关重要。在分解方法方面，MSD在所有指标上均优于**CoACD**（Wei et al., ACM TOG 2022）：MSD能够提取具有均匀厚度的连通区域，为SuperFrustum提供语义连贯的初始化种子（Figure 4），而CoACD倾向于沿轴对齐方向过度分割，产生大量语义不对齐的凸碎片，导致后续优化需要更多基元且精度更低。

### CSG推断实验

在ABC数据集上的CSG推断实验（Table 4）显示，ResFit在使用规范实体（如圆柱、立方体）时，能够以显著更少的基元数量达到与**CAPRI-Net**相当的重构精度。定性结果（Figure 7）表明，ResFit推断的CSG树结构更清晰、更具可解析性，这得益于SuperFrustum对规范实体的自然覆盖能力。

![[assets/figures/papers/paper_list_l2090_https_arxiv_org_abs_2512_09201/figures/011_Table_4.jpg]]
*Table 4: CSG inference on the ABC dataset [12]: Our method achieves comparable reconstruction accuracy to CAPRI-Net [46] while using significantly fewer primitives*

![[assets/figures/papers/paper_list_l2090_https_arxiv_org_abs_2512_09201/figures/009_Figure_7.jpg]]
*Figure 7: Our method can infer CSG programs using canonical solids (e.g., cylinders, cuboids; cf. Sec. 5), producing far more parsable and structured trees than CAPRI-Net [46]*

### 失败模式与局限性

尽管ResFit取得了显著的性能提升，但实验和分析揭示了以下局限：

1. **纯加性组合的限制**：当前ResFit仅支持基元的平滑联合操作，无法处理布尔减操作（如孔洞、凹陷）。这使得方法在机械零件等需要减操作的领域适用性受限。Figure 5中部分结果的精细凹陷结构可能未被完整捕捉，需要手动验证。

2. **MSD分解的鲁棒性**：方法依赖MSD对残差体进行厚度均匀的区域提取。对于严重非水密或存在自相交的输入网格，MSD可能产生不稳定分解，进而影响后续基元初始化和优化。这一点的具体影响程度在论文中缺乏定量分析，需要进一步验证。

3. **运行时间**：单轮优化约需184秒，虽在离线场景可接受，但距离交互式编辑的实时性要求仍有差距。多轮迭代的总时间将进一步增加。

4. **极端形状的基元效率**：尽管SuperFrustum的8参数已具备较强表达能力，但对于长距离渐变的环形或高度扭曲的几何，仍可能需要多个基元拼接才能达到高精度重构，此时基元数量的优势可能被削弱。

### 补充图表

![[assets/figures/papers/paper_list_l2090_https_arxiv_org_abs_2512_09201/figures/007_Table_2.jpg]]
*Table 2: Primitive representation ablation: SuperFrustum delivers superior performance over Cuboids, Superquadrics (SQ) and SuperPrimitive(SP) (ref. Section 4.2). Combining SuperFrustum with smooth union further improves performance*

![[assets/figures/papers/paper_list_l2090_https_arxiv_org_abs_2512_09201/figures/008_Table_3.jpg]]
*Table 3: Fitting and decomposition ablation: ResFit, which interleaves analysis and optimization, outperforms a single-shot fitting approach (cf. Section 4.2). Moreover, pairing ResFit with MSD yields better results than using CoACD [40]*

![[assets/figures/papers/paper_list_l2090_https_arxiv_org_abs_2512_09201/figures/010_Figure_6.jpg]]
*Figure 6: Assigning per-primitive spherical 2D textures & optimizing it against a textured mesh, begets Edtiable & Deployable assets*

![[assets/figures/papers/paper_list_l2090_https_arxiv_org_abs_2512_09201/figures/012_Figure_8.jpg]]
*Figure 8: Our method can infer primitive assemblies from images by leveraging Text-2-3D models (Hunyuan3D-2.1 [33])*

![[assets/figures/papers/paper_list_l2090_https_arxiv_org_abs_2512_09201/figures/013_Figure_9.jpg]]
*Figure 9: ResFit enables finer, semantically consistent part segmentation. Row 1 shows the coarse semantic regions provided in PartObjVerse. Row 2 shows the primitive assemblies inferred by ResFit. Intersecting each coarse region with its corresponding assembly (Row 3) yields meaningful sub-parts—capturing functional structure while remaining strictly within the original semantic boundaries*

## 方法谱系与知识库定位

### 基元装配方法的演进脉络

3D形状的基元化表示长期存在**表达性**与**简洁性**之间的根本张力。现有方法可按其核心策略大致分为三个谱系：

**分析驱动的方法**以近似凸分解（ACD）为代表。**CoACD**（Wei et al., ACM TOG 2022）通过精确的近似凸分解将形状切割为凸块，再用简单基元（如立方体）拟合每个分块。这类方法的优势在于分解过程与基元类型解耦，但其核心缺陷也源于此——分解不考虑基元的表达能力，导致对可被单个复杂基元覆盖的区域（如弯曲管状结构）产生过度分割。在Figure 4中，CoACD将自行车轮胎、猫的弯曲尾巴等非凸但形态连贯的结构切分为多个轴对齐的凸碎片，丧失了语义一致性。

**优化驱动的方法**以**Marching Primitives (MPS)**（Liu et al., CVPR 2023）为代表，通过全局梯度优化直接装配多种基元。这类方法依赖基元自身的可微性来探索解空间，但受限于高度非凸的损失景观：当基元表达能力不足时，需要大量基元堆叠来逼近复杂几何，导致重构保真度与基元数量之间的帕累托前沿不佳。Table 1显示，MPS在Toys4K上需30.62个基元才能达到80.62%的IoU，且体素重叠率高达0.684，说明大量基元在空间上严重交叠以弥补个体表达力的不足。

**学习驱动的方法**以**Primitive Anything (PA)**（Ye et al., 2025）为代表，利用数据先验预测基元装配。这类方法在训练分布内表现良好，但泛化到训练集外的几何形态时能力受限，且其装配质量受限于标注数据的规模与质量。

### ResFit的核心定位：耦合分析先验与可微优化

ResFit的关键创新在于**打破分析分解与优化拟合之间的独立性假设**。其核心洞察是：分解策略应当适配基元的表达能力，而非反之。具体而言：

1. **SuperFrustum作为表达性瓶颈的突破**：传统基元如立方体（Cuboids）和超二次曲面（Superquadrics, SQ; Paschalidou et al., CVPR 2019）仅用少量参数描述有限形状族。SuperFrustum以8参数统一解析SDF（Eq. 3）平滑覆盖立方体、圆柱、圆锥、球体及弯曲、空心等复杂形态（Figure 2），且其SDF几乎处处可微，使其同时具备表达性、可编辑性和可优化性。Table 2的消融实验证实，SuperFrustum在IoU、Chamfer Distance和基元数量上全面优于Cuboids、SQ和SuperPrimitive (SP)。

2. **MSD分解适配基元表达能力**：形态学形状分解（MSD, Section 3.3）通过迭代侵蚀-膨胀（Eq. 5-6）提取具有均匀厚度的连通区域，这些区域天然适配SuperFrustum的锥度、鼓胀和弯曲参数。与CoACD的轴对齐凸切割不同，MSD保留了非凸但形态连贯的结构（如环形、弯曲管状），为SuperFrustum提供语义合理的初始化种子。Table 3证实，MSD + ResFit的组合在IoU和基元数量上均优于CoACD + ResFit。

3. **交替优化策略**：ResFit不采用一次性全局拟合，而是在形状分析（MSD分解与初始化）和局部优化（梯度下降 + 剪枝）之间交替迭代（Figure 3）。每次迭代提取当前装配无法解释的残差体积，并在残差上启动新一轮基元添加。Table 3的消融表明，这种交替策略显著优于单阶段拟合（Single-shot），在IoU和重叠度上均有明显优势。

### 与下游方法的衔接

ResFit输出的基元装配具有天然的可编辑性和程序化特性，可直接衔接多个下游任务：

- **CSG程序推断**：通过将SuperFrustum参数约束到规范实体（如圆柱、立方体），ResFit可推断结构化的CSG树。Table 4显示，在ABC数据集上，ResFit以显著更少的基元达到了与**CAPRI-Net**（Yu et al., 2023）可比的重构精度，且生成的CSG树更具可解析性（Figure 7）。
- **可编辑资产生成**：每个基元可独立赋予球面纹理并针对带纹理网格优化，生成可编辑、可部署的3D资产（Figure 6）。
- **语义部件分割细化**：将ResFit的基元装配与粗粒度语义区域相交，可获得功能结构一致的细粒度子部件（Figure 9）。
- **图像到基元装配**：借助Text-to-3D模型（如Hunyuan3D-2.1），ResFit可从单张图像推断基元装配（Figure 8）。

### 适用边界与局限

尽管ResFit在重构-简洁性帕累托前沿上取得了系统性前移，其当前设计存在明确的适用边界：

1. **仅支持加性组合**：ResFit的装配仅通过平滑联合算子组合基元，无法处理需要减操作的形状（如通孔、凹陷、槽口）。这限制了其在机械零件、工程结构等需要CSG差集/交集的领域的直接应用。这是方法层面的根本限制，而非工程优化问题。

2. **对输入网格质量的依赖**：MSD分解假设输入为水密三角网格。对存在自相交、非流形边或缺失面的模型，侵蚀-膨胀操作可能产生不稳定分解，进而影响基元初始化和最终装配质量。实际应用中可能需要额外的网格修复预处理。

3. **运行时间尚不适于实时交互**：单轮ResFit（包括MSD分解、初始化和优化）约需184秒。虽然多轮迭代可渐进提升质量，但使得交互式编辑场景（如艺术家实时调整基元参数）仍需显著加速。

4. **极端形态的表达仍受限**：尽管SuperFrustum的8参数覆盖了广泛形状族，某些极端形态（如长距离渐变曲率的环形、具有多个局部凸起的复杂有机形状）可能仍需多个基元拼接，无法用单个SuperFrustum精确表达。

### 开放问题

当前工作揭示了若干值得进一步探索的方向：

- **支持减操作的分解策略**：如何扩展MSD或引入新的分解范式（如基于形态学形状树），使ResFit能够自动发现并利用减操作来表示孔洞和凹陷，是通向完整CSG表示的关键一步。
- **与可学习先验的融合**：ResFit目前是完全无监督的。将其与特定类别的形状先验（如通过预训练编码器）结合，有望在保持泛化能力的同时提升类内重构精度和语义一致性。
- **端到端可编辑流水线**：将基元装配与物理仿真、骨骼绑定、动画参数化等下游任务直接衔接，形成从几何到功能的端到端可编辑资产流水线，是推动基元表示实际应用的重要方向。
- **实时交互优化**：通过GPU加速、预计算缓存或渐进式优化策略，将基元拟合时间压缩到秒级甚至亚秒级，使ResFit能够嵌入交互式建模工具。

## 原文 PDF

![[paperPDFs/CVPR_2026/Residual_Primitive_Fitting_of_3D_Shapes_with_SuperFrusta.pdf]]