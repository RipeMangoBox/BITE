---
title: Computational Pattern Making From 3D Garment Models
type: paper
paper_level: A
venue: SIGGRAPH
year: 2022
pdf_ref: paperPDFs/SIGGRAPH_2022/Computational_Pattern_Making_From_3D_Garment_Models.pdf
project_link: "https://optitex.com"
code_link: null
aliases:
- CPMP
- CPMF3GM
tags:
- SIGGRAPH_2022
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
core_operator: 引入基于织物物理模型的各向异性参数化能量（分别惩罚经纬向拉伸和剪切），并结合4-RoSy场引导的自动化分片布局与省道创建，直接满足缝纫可行性。
primary_logic: 将布料变形建模为各向异性度量，并利用该度量指导分片切割和2D展平，使得生成的纸样既满足几何约束又符合实际缝制要求。
claims:
- 制造的潜水服和紧身裤展现出极好的合身度，验证了方法的可行性。
- 参数化方法能有效平衡拉伸、剪切和接缝对称性，产生可缝制的纸样。
- 方法可处理紧身和宽松服装，以及非人形物体（如狗、袋鼠）。
- Tight-fitting dress on scanned body 上 Fabrication feasibility = successful fabrication
---

# Computational Pattern Making From 3D Garment Models

> [!tip] 核心洞察
> 将布料变形建模为各向异性度量，并利用该度量指导分片切割和2D展平，使得生成的纸样既满足几何约束又符合实际缝制要求。

| 字段 | 内容 |
|------|------|
| 中文题名 | 从三维服装模型自动生成计算缝纫纸样 |
| 英文题名 | Computational Pattern Making From 3D Garment Models |
| 会议/期刊 | SIGGRAPH 2022 |
| Links | [paper](https://arxiv.org/abs/2202.10272) · [arXiv](https://arxiv.org/abs/2108.10842) · [Project](https://optitex.com) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction |
| Method | Computational Pattern Making Pipeline |
| Dataset | Tight-fitting dress on scanned body, Example pattern, Shirt model |

> [!tip] 效果简介
> - Tight-fitting dress on scanned body 上，Fabrication feasibility successful fabrication vs not applicable (N/A)。
> - Example pattern 上，fabric stress and ARAP energy good results (both measures) vs N/A (N/A)。
> - Shirt model (parameter variation) 上，Number of patches and shape quality controlled by max corners and max stretch vs N/A (N/A)。

## 概要

本文提出一种从三维服装网格自动生成二维缝纫纸样的计算流程。核心瓶颈在于，现有通用表面切割与展平方法忽略缝纫所必需的特殊约束——接缝等长与反射对称、省道处理、布料经纬向各向异性变形——导致生成的纸样难以实际缝制。本方法的关键创新是引入基于织物物理模型的各向异性参数化能量，分别惩罚经纬向拉伸和剪切，并利用4-RoSy场引导的自动分片布局与省道创建，直接满足缝纫可行性要求。流程依次包含对称化、交叉场计算、路径追踪分片、以及各向异性织物参数化展平四个模块。实验证明，该方法成功制造出潜水服和紧身裤等实物，展现出良好的合身度；同时可处理紧身与宽松服装，乃至非人形物体（如狗、袋鼠）。消融实验表明，接缝反射对称性和省道对称性约束对生成可工作的纸样至关重要。本方法定位为面向缝纫制造的专用表面切割与展平技术，区别于通用几何处理方法和基于草图的服装设计工具。

## 核心方法与创新机理

### 问题定位：从3D模型到可缝纫纸样的瓶颈

传统的表面切割与参数化方法（如OptCuts、Variational Surface Cutting）将3D表面展平为2D片时，采用各向同性的变形度量（如共形映射或等距映射），完全不考虑织物缝纫的特殊约束。这导致生成的纸样存在根本性缺陷：接缝两侧长度不匹配、无法保证反射对称性、缺少省道（dart）结构、忽略布料经纬向的各向异性变形特性。简而言之，**数学上合理的展平结果在缝纫实践中不可用**。

本工作的核心瓶颈在于：将缝纫工艺的物理约束（接缝等长、反射对称、省道、织物经纬向拉伸与剪切分离）编码为可优化的几何与能量模型，使得自动生成的2D纸样能够直接用于裁剪和缝制。

### 核心机制：各向异性织物感知的参数化与场引导分片

方法的核心创新是将布料建模为**具有正交经纬结构的各向异性度量**，并利用该度量同时指导3D表面的分片切割（patch layout）和2D展平（parameterization）。这一设计使得整个流水线产出的纸样既满足几何展平要求，又符合实际缝制工艺。

具体而言，方法在三个关键维度上改变了传统表面展平范式：

1. **变形度量槽位（Distortion measure slot）**：从各向同性（如共形能量、ARAP）转变为**各向异性织物感知度量**。该度量将拉伸分离为经向（warp/u）和纬向（weft/v）两个独立分量，分别惩罚，同时通过刚性能量间接处理剪切变形。这与真实机织物的物理行为一致：经纬纱线可独立拉伸，但剪切阻力来自纱线交叉点的摩擦。

2. **分片布局生成槽位（Patch layout generation slot）**：从通用的最小化切割长度或变形优化，转变为**基于4-RoSy场引导的路径追踪**。分片边界不再任意选择，而是沿主曲率方向对齐，并受织物变形限制（每个分片的最大拉伸量和角点数）约束。同时引入省道创建和接缝对称性约束，使分片布局天然支持缝纫。

3. **接缝约束槽位（Seam constraints slot）**：从无约束或简单长度匹配，转变为**反射对称性约束和等长约束**。接缝两侧的对应点不仅要求等距，还要求相对于接缝线反射对称，这是保证缝纫后布料平整不起皱的关键。

### 流水线模块与因果关系

整个流水线由四个串行模块构成，前一模块的输出直接决定后一模块的可行性与质量（图3）：

**模块1：对称化（Symmetrization）**
若输入服装网格具有全局对称性，沿对称平面将网格分割。后续处理仅在半边上进行，最终通过镜像合并生成完整纸样。这减少了计算量，并天然保证了左右片的对称性。

**模块2：交叉场计算（Cross-field computation）**
在输入网格上计算4-RoSy切向量场（4重旋转对称场）。场的方向通过多尺度主曲率方向初始化（Panozzo et al., 2010），并平滑优化。该场定义了布料经纬方向在3D表面上的理想走向——经向（warp）应尽可能垂直对齐（穿着时的竖直方向），纬向（weft）水平环绕。交叉场的质量直接决定了后续路径追踪的合理性：如果场在褶皱区域受噪声干扰，追踪出的分片边界可能偏离理想的织物纹路。

**模块3：分片布局生成（Patch layout creation）**
这是流水线中最复杂的模块，包含四个子步骤：

- **路径追踪（Path tracing）**：将网格顶点扩展为图节点（每个顶点对应4个节点，代表交叉场的4个方向分量），相邻顶点间匹配场方向的节点相连。在此图上追踪两类路径：闭环（loop）和边界到边界路径（border-to-border）。追踪采用贪心策略，优先选择与已有路径M4分层距离最远的候选路径。

- **路径插入（Insertion）**：候选路径若分割了不满足目标的分片（如角点过多或拉伸量超限），且不与已有路径切向相交，则插入。插入后更新分片集合，迭代直至所有分片满足预设的角点数和最大拉伸量约束。

- **路径移除（Removal）**：尝试融合相邻分片（移除共享路径），若融合后的分片仍满足约束，则保留融合结果。这一步避免过度分割。

- **省道创建（Dart creation）**：在负曲率区域自动创建省道。省道是缝纫中用于消除布料冗余的关键结构——在2D纸样上剪开一个V形缺口，缝合后使3D表面贴合身体曲线。方法从负曲率顶点出发追踪省道路径，并在展平能量中加入省道反射对称项（$E_{\text{dart}}$），确保省道两侧长度相等且反射对称。

**模块4：各向异性织物参数化（Anisotropic textile parameterization）**
将每个3D分片独立展平到2D平面。核心是定义并最小化**织物变形总能量** $E_{\text{textile}}$（公式10）：

$$E_{\text{textile}} = E_{\text{stretch},u} + E_{\text{stretch},v} + E_{\text{rigid}} + E_{\text{seam}} + E_{\text{dart}}$$

各能量项的含义与因果关系：

- **经向拉伸能量 $E_{\text{stretch},u}$ 和纬向拉伸能量 $E_{\text{stretch},v}$**：分别惩罚经纬方向的拉伸变形。对于每个三角形$ABC$，拉伸因子定义为雅可比矩阵列向量的范数 $s_u = \| J_1 \|, s_v = \| J_2 \|$（公式1）。拉伸能量（公式5）度量当前三角形在$u$或$v$方向的实际拉伸量与目标拉伸量之差的平方。目标拉伸量由三角形的重心坐标插值得到，权重为$\omega_{\text{stretch}}$。**分离经纬拉伸是关键创新**：传统ARAP能量将拉伸与剪切混为一谈，无法区分“经向拉伸5%、纬向拉伸0%”与“各向均匀拉伸2.5%”这两种对织物手感截然不同的变形。

- **刚性能量 $E_{\text{rigid}}$**：采用ARAP能量形式（公式6），惩罚三角形的非刚性变形，间接约束剪切。权重为$\omega_{\text{rigid}}$。在机织物中，剪切刚度远低于拉伸刚度，因此该能量项与拉伸能量项的权重配比直接影响展平结果的自然程度。

- **接缝反射对称能量 $E_{\text{seam}}$**：对于需要缝合的两条接缝边$P$和$Q$，要求$P$上的点$p_i$与$Q$上对应点$q_i$相对于接缝线反射对称。能量定义为各点与其反射对称目标位置之差的平方和（公式8），权重为$\omega_{\text{seam}}$。这一约束是缝纫可行性的核心保障：若接缝两侧不对称，缝合后会产生不均匀的拉扯，导致穿着时布料扭曲。

- **省道反射对称能量 $E_{\text{dart}}$**：与接缝能量类似，要求省道两侧边满足反射对称和等长约束。

各能量项通过权重$\omega$平衡。消融实验（图14）表明，默认权重$(5,1,5,5)$（对应拉伸、刚性、接缝、省道）能产生合理的纸样。若接缝和省道对称能量被关闭或权重过低，生成的纸样在反射切割处无法对齐（图15），证明这些约束对可缝纫性至关重要。

### 贪心策略与展平的一致性挑战

流水线的一个关键设计张力在于：模块3的分片分解采用贪心策略，基于3D表面上的测地线距离和交叉场方向决定切割位置；而模块4的展平是在2D平面上全局优化变形能量。这两步的变形评估并不完全一致——分片分解阶段预估的拉伸量可能与最终展平后的实际拉伸量存在偏差。这是贪心流水线的固有局限，也是论文明确指出的一点：**输入服装或用户约束的微小差异可能导致显著不同的纸样结果**。

### 多姿态扩展

对于动画模型（多帧），方法将多尺度主曲率方向在帧间积分以推导交叉场，并在展平能量中为每帧添加能量项。这使得接缝能适应高变形区域（如大腿与躯干连接处），在静止姿态下可能被忽略的变形区域在多姿态分析中得以暴露（图22）。

![[assets/figures/papers/paper_list_l9_https_arxiv_org_abs_2202_10272/figures/003_Figure_3.jpg]]
*Figure 3: An overview of the different steps of our pipeline. The shape is first symmetrized (a), a smooth cross-field is computed on the mesh (b), paths are then traced on the shape by following the cross-field (c), and the resulting patches are then flattened onto the ???? plane to create a 2D sewing pattern (d)*

![[assets/figures/papers/paper_list_l9_https_arxiv_org_abs_2202_10272/figures/002_Figure_2.jpg]]
*Figure 2: Top: matching seams on two patches to be stitched together, as well as the sides of a dart must be of equal length and ideally reflectionsymmetric. Bottom: the fabric grain of pattern pieces aims to align with the vertical direction on the worn garment*

## 实验与关键发现

本文的实验验证策略与传统的数值对比型论文不同：由于所提方法针对的是“可缝纫纸样自动生成”这一尚未被充分解决的特定问题，现有通用表面切割与参数化方法（如 OptCuts、Variational Surface Cutting）并不直接产生符合缝纫约束的纸样，因此作者未提供与基线方法的定量指标对比表。实验的核心逻辑是通过**物理制造验证**、**能量权重消融**和**参数空间探索**来证明方法的可行性与关键设计选择的合理性。

### 物理制造验证：从数字模型到真实服装

最具说服力的证据来自两件真实服装的制造实验。作者基于三维人体扫描数据生成了紧身潜水服和紧身裤的纸样，并使用真实面料进行裁剪和缝制。

对于**紧身潜水服**（Fig. 23），输入为基于受试者三维扫描的服装模型。生成的纸样经单人约 5 小时完成裁剪与缝制（领口开口后续替换为拉链）。成品展现出极好的合身度，验证了方法在紧身服装场景下的端到端可行性。**紧身裤**（Fig. 24）的制造过程约 1 小时，同样展示了良好的穿着效果。

这两项制造实验的可靠性较高，因为它们直接验证了方法的核心主张——生成的纸样能够被实际缝制成合身的服装。但需要注意，制造实验仅在紧身服装上进行，宽松服装的制造验证尚缺。

### 各向异性织物参数化的能量权重消融

参数化阶段的能量函数由四项加权组成：经向拉伸 $E_{\mathrm{stretch},u}$、纬向拉伸 $E_{\mathrm{stretch},v}$、刚性能量 $E_{\mathrm{rigid}}$（间接处理剪切）和接缝反射对称能量 $E_{\mathrm{seam}}$，总能量为：

$$E_{\mathrm{textile}} = E_{\mathrm{stretch},u} + E_{\mathrm{stretch},v} + E_{\mathrm{rigid}} + E_{\mathrm{seam}} + E_{\mathrm{dart}}$$

Fig. 14 展示了不同能量权重对展平结果的影响。默认权重配置 $(\omega_{\mathrm{stretch}}, \omega_{\mathrm{rigid}}, \omega_{\mathrm{seam}}, \omega_{\mathrm{dart}}) = (5, 1, 5, 5)$ 能够产生合理的纸样，在拉伸控制与剪切容忍之间取得平衡。当某项权重偏离默认值时，纸样质量出现明显退化——例如拉伸权重过低会导致局部区域过度拉伸，而接缝权重不足则使缝合边界的匹配精度下降。

![[assets/figures/papers/paper_list_l9_https_arxiv_org_abs_2202_10272/figures/014_Figure_14.jpg]]
*Figure 14: Influence of the energy terms weights on the parameterization*

### 接缝对称性与省道对称性的关键作用

Fig. 15 的消融实验揭示了接缝反射对称性和省道对称性能量对产生可工作纸样的决定性作用。当这两项能量被移除或权重过低时，接缝两侧的边界不再满足反射对称性，导致在实际缝制时两侧无法对齐。这一发现直接支撑了方法的核心设计选择：将缝纫特定的几何约束（而非仅最小化几何失真）纳入参数化目标函数，是区别于通用表面展平方法的关键。

### 分片布局的参数控制探索

方法提供两个核心参数来控制自动分片分解的行为：每个分片的最大角点数 $c_{\max}$ 和最大允许拉伸量 $s_{\max}$。Fig. 19 在衬衫模型上探索了这两个参数的组合空间。结果表明：

- 当 $c_{\max}$ 较小时，分解倾向于产生更少但形状更复杂的分片；
- 增大 $s_{\max}$ 会减少分片数量，但单个分片的展平失真增大；
- 两个参数共同决定了分片布局的“粒度”，用户可根据面料特性和制造偏好进行调整。

这一参数空间探索为方法的实际使用提供了操作指导，但同时也暴露了方法的贪心特性：参数或输入网格的微小变化可能导致显著不同的分片布局，这是贪心路径插入策略的固有局限。

### 多姿态动画的处理能力

对于动画模型（Fig. 22），方法通过跨帧积分多尺度主曲率方向来推导引导场，并在分片参数化中增加逐帧能量项。实验表明，引入多个目标姿态有助于方法在高度变形区域（如腿部与躯干连接处）放置接缝，而这些区域在仅使用静止姿态时可能被忽略。这一结果扩展了方法的适用范围，但也暗示了计算成本随姿态数量线性增长的潜在问题。

### 非人形物体的泛化验证

Fig. 17 展示了方法在狗和袋鼠等非人形三维模型上的应用结果。尽管这些形状的拓扑和曲率分布与人形服装差异显著，方法仍能生成合理的分片布局和二维纸样。这一泛化能力源于方法对输入形状类型的弱假设——仅依赖曲率场引导和织物变形约束，而非人体模板或语义先验。

### 织物应力与 ARAP 能量的定量评估

Fig. 21 在示例纸样上测量了织物应力和 ARAP 能量，两项指标均达到良好水平。这为方法的几何质量提供了定量支撑，但需注意该评估仅针对单个示例，缺乏统计意义上的广泛验证。

### 方法的失败模式与适用边界

根据论文自述和实验观察，方法存在以下明确局限：

1. **褶皱噪声敏感性**：如果输入网格来自物理模拟或三维扫描，表面褶皱可能被误判为几何特征，污染引导场的质量，进而影响分片布局的合理性。

2. **贪心路径追踪的不一致性**：路径插入采用贪心策略，在分片分解阶段评估的失真度量与最终展平阶段计算的失真可能不一致，导致某些分片在展平时出现超出预期的变形。

3. **结果的不稳定性**：贪心策略的另一个后果是输入或参数的微小变化可能导致显著不同的纸样，这对可复现性和用户预期管理构成挑战。

4. **缝份约束的缺失**：当前方法未包含缝份（seam allowance）约束，在实际制造中需要手动添加缝份余量，增加了裁剪和缝制的出错风险。论文明确指出这是未来工作的方向。

5. **制造验证范围有限**：仅验证了紧身服装（潜水服、紧身裤），宽松服装和复杂结构（多层、口袋、拉链）的制造可行性尚未得到实验证实。

### 实验证据强度总结

整体而言，该工作的实验设计以**制造可行性**为核心判据，辅以消融实验和参数探索来支撑方法设计。物理制造的成功案例（Fig. 23, Fig. 24）构成了最强有力的证据，直接验证了端到端管线的实际价值。能量权重消融（Fig. 14）和对称性消融（Fig. 15）清晰揭示了关键设计选择的因果作用。然而，缺乏与基线方法的定量对比使得方法的相对优势难以精确量化，这是实验部分的主要不足。此外，制造验证的样本量较小（仅两件服装），统计说服力有限。

![[assets/figures/papers/paper_list_l9_https_arxiv_org_abs_2202_10272/figures/010_Figure_10.jpg]]
*Figure 10: Creating darts starting from areas with negative curvature tends to generate overlaps in the ???? mapping*

![[assets/figures/papers/paper_list_l9_https_arxiv_org_abs_2202_10272/figures/011_Figure_12.jpg]]
*Figure 12: Woven net (left) undergoing stretch (middle) and shear (right)*

![[assets/figures/papers/paper_list_l9_https_arxiv_org_abs_2202_10272/figures/012_Figure_11.jpg]]
*Figure 11: The seam on the global symmetry plane can be safely removed at the end of the layout generation process*

## 定位与知识库关联

本文提出了一种面向缝纫制造的计算纸样自动生成管线，其核心定位在于**将通用表面切割与参数化问题转化为一个受织物物理特性和缝纫工艺约束的专用问题**。与已有工作的本质差异集中体现在三个关键 slot 的改变上。

**改变的 Slot 一：变形度量——从各向同性到各向异性织物感知。** 传统表面参数化方法（如 **OptCuts** (Li et al., 2018)、**Variational Surface Cutting** (Sharp and Crane, 2018)）采用的变形度量通常是各向同性的（保角、保积或尽可能等距），它们将表面视为均匀弹性膜。本文的关键改变在于引入了一个**各向异性的织物感知变形能量** $E_{\text{textile}}$（Eq. 10），该能量分别惩罚经向拉伸 $E_{\text{stretch},u}$、纬向拉伸 $E_{\text{stretch},v}$ 和剪切（通过 ARAP 刚性能量 $E_{\text{rigid}}$ 间接处理），而非将其混为一谈。这一改变的深层动机来自机织布料的物理结构：经纬纱线正交排列，沿纱线方向的拉伸阻力远大于对角方向的剪切变形（Fig. 12）。忽略这种各向异性会导致展平结果在理论上可接受，但在实际裁剪缝纫时产生不可接受的布料扭曲。该 slot 的改变是本文方法区别于所有通用参数化工作的**根本性分水岭**。

**改变的 Slot 二：分片布局生成——从最小化切割长度到场引导的缝纫约束布局。** 通用切割方法以最小化切割长度或参数化失真为目标，不考虑生成的 patch 是否适合缝纫。本文的分片布局生成（Sec. 4.2）基于 **4-RoSy 交叉场**引导的路径追踪，但其目标函数和约束条件被彻底替换：patch 的可行性不再仅由展平失真决定，而是由**最大角点数、最大拉伸量、接缝反射对称性**等缝纫特定条件共同定义。此外，本文在布局阶段引入了**省道自动创建**（从负曲率区域出发，Fig. 10）和**对称面接缝移除**（Fig. 11）等缝纫工艺特有的操作。该方法适配自 Pietroni et al. (2021) 的通用四边形网格划分框架，但将其拓扑要求和变形界限替换为面向服装制造的织物变形阈值。

**改变的 Slot 三：接缝约束——从无约束或简单长度匹配到反射对称与等长联合约束。** 在缝纫中，两条待缝合的接缝边不仅需要等长，还需要满足**反射对称性**（Fig. 2 top），以确保缝合后布料平整无扭曲。已有方法最多考虑接缝边的长度匹配，而本文在参数化能量中显式加入了接缝反射对称能量 $E_{\text{seam}}$（Eq. 8）和省道对称能量 $E_{\text{dart}}$。消融实验（Fig. 15）直接证实，移除这些对称性约束会导致生成的纸样无法实际使用。这一 slot 的改变是本文从“可展平”跨越到“可缝纫”的关键工程洞察。

**知识库挂载点。** 本文在计算机图形学知识库中的挂载位置是**制造导向的几何处理**（fabrication-aware geometry processing）与**基于物理的服装建模**的交叉地带。具体而言：
- 上游继承自**方向场引导的表面切割与参数化**（Vaxman et al., 2017; Pietroni et al., 2021; Li et al., 2018），本文将其从通用几何处理迁移到缝纫约束空间。
- 平行对标**基于草图的服装纸样生成**（如 **3D Custom Fit Garment Design**, Wolff et al., 2021），后者依赖设计师手动绘制风格线，而本文实现了全自动的分片推理。
- 下游连接**计算制造**（computational fabrication）领域，特别是涉及柔性材料的自动纸样生成（如毛绒玩具、皮革制品、充气结构），这些领域同样面临各向异性材料约束下的表面展平问题。

**适用边界。** 本文方法假设输入为表示目标服装的三角网格，且针对**机织布料**（正交经纬纱线）设计。对于针织面料（弹性各向异性模式不同）或无纺布，当前的各向异性模型需要重新标定。方法在处理带有褶皱的扫描或模拟网格时，引导场质量可能下降（局限性 1）。此外，分片布局的贪心策略导致输入或参数的微小变化可能产生显著不同的纸样（局限性 3），这意味着方法的**可重复性和稳定性**尚未达到工业级要求。当前版本未包含缝份约束（局限性 4），实际制造时仍需人工添加。

**后续研究启发。** 本文开辟了若干有价值的研究方向：（1）将缝份约束纳入参数化框架，实现从纸样到裁剪线的端到端生成；（2）将各向异性织物能量推广到针织、皮革等更多材料类型；（3）用全局优化替代贪心策略，提升分片布局的稳定性和最优性；（4）将方法扩展到多层服装、口袋、拉链等复杂结构。在更广泛的视角下，本文的核心思想——**将制造工艺的物理约束反向嵌入几何处理算法**——可被迁移到其他计算制造任务中，如鞋类纸样、碳纤维铺层优化等。

## 原文 PDF

![[paperPDFs/SIGGRAPH_2022/Computational_Pattern_Making_From_3D_Garment_Models.pdf]]