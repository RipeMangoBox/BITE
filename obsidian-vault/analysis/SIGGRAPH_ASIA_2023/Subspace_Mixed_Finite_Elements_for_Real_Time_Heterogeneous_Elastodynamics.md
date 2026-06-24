---
title: "Subspace Mixed Finite Elements for Real-Time Heterogeneous Elastodynamics"
type: paper
paper_level: A
venue: "SIGGRAPH Asia"
year: 2023
pdf_ref: paperPDFs/SIGGRAPH_ASIA_2023/Subspace_Mixed_Finite_Elements_for_Real_Time_Heterogeneous_Elastodynamics.pdf
project_link: https://www.dgp.toronto.edu/projects/subspace-mfem/
aliases:
- SMFEMM
- SMFERTHE
tags:
- SIGGRAPH_ASIA_2023
- topic/optimization_theory_probabilistic
- topic/optimization_theory_probabilistic/optimization_methods
core_operator: "在子空间求解中引入辅助拉伸自由度并施加一致性约束，构成混合有限元格式。"
primary_logic: "将Skinning Eigenmode子空间与混合有限元法结合，并用异质性感知的cubature近似加速非线性弹性积分，可使异构弹性模拟的性能完全与网格分辨率脱钩，并在极低迭代次数下保持正确的旋转运动。"
claims:
- "仅需2次求解器迭代，子空间MFEM即可在具有巨大刚度差异的螃蟹模型上展现正确的旋转和弹性行为，而子空间FEM即使使用4次迭代依然出现明显阻尼。"
- "相对于全空间MFEM，子空间MFEM在哺乳象示例中实现超过三个数量级的加速（0.003 FPS → 120 FPS）。"
- "Skinning Eigenmode子空间能够精确重建旋转，而模态导数则不能。"
- "所提出的k-means聚类cubature方案无需训练阶段，且自然感知材料和几何异质性，密集采样柔软/薄区域，稀疏采样刚硬/厚区域。"
---

# Subspace Mixed Finite Elements for Real-Time Heterogeneous Elastodynamics

> [!tip] 核心洞察
> 将Skinning Eigenmode子空间与混合有限元法结合，并用异质性感知的cubature近似加速非线性弹性积分，可使异构弹性模拟的性能完全与网格分辨率脱钩，并在极低迭代次数下保持正确的旋转运动。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 面向实时异构弹性力学的子空间混合有限元方法 |
| 英文题名 | Subspace Mixed Finite Elements for Real-Time Heterogeneous Elastodynamics |
| 会议/期刊 | SIGGRAPH Asia 2023 |
| Links | [paper](https://arxiv.org/abs/2405.13730); [Project](https://www.dgp.toronto.edu/projects/subspace-mfem/) |
| Topic | #topic/optimization_theory_probabilistic #topic/optimization_theory_probabilistic/optimization_methods |
| Method | Subspace Mixed Finite Element Method (MFEM) |
| Dataset | Mammoth (98K vertices, 531K tets, heterogeneous bone/muscle/joints), Crab (heterogeneous shell/joints), Sword (angular motion over 25 timesteps) |

> [!tip] 效果简介
> - Mammoth (98K vertices, 531K tets, heterogeneous bone/muscle/joints) 上，Frames Per Second (FPS) 为 120 FPS，对比 0.003 FPS (full-space MFEM)，变化 ~40,000× speedup。
> - Crab (heterogeneous shell/joints) 上，Qualitative rotation preservation at low iterations 为 Correct rotational behavior at 2 iterations，对比 Visible damping at 4 iterations (subspace FEM)，变化 Half the frame rate, worse behavior。
> - Sword (angular motion over 25 timesteps) 上，Angular motion reproduction 为 Almost perfectly reproduces target angular motion，对比 Consistently underestimates angular motion (subspace FEM)，变化 MFEM recovers rotational motion within ~1 iteration。

## 概述

实时模拟具有剧烈材料异质性的弹性体变形是计算机图形学中的一项长期挑战。传统子空间方法通过将高维网格位移投影到低维基上来换取速度，但在刚度差异悬殊的场景下收敛缓慢——过早截断求解迭代会导致可见的阻尼伪影和旋转运动失真。其根本瓶颈在于：标准有限元（FEM）格式将位置自由度与应变能耦合在同一优化变量中，低迭代时旋转分量无法被充分解析。

本文的核心主张是：**将混合有限元（Mixed FEM, MFEM）引入子空间求解框架，可以从机制上解耦这一耦合**。MFEM 在标准位置自由度之外，为网格单元引入辅助拉伸自由度，并通过显式一致性约束维持二者协调。这一格式使得旋转运动即使在极低迭代次数下也能被正确保持。本文将该思想与 Skinning Eigenmode 子空间和异质性感知的 cubature 近似相结合，提出**子空间混合有限元方法（Subspace MFEM）**，使异构弹性模拟的性能完全与网格分辨率脱钩。

**决定性证据**来自 Figure 2：在具有巨大刚度差异（硬壳 E=1e10 Pa，软关节 E=1e6 Pa）的螃蟹模型上，子空间 MFEM 仅需 **2 次求解器迭代**即展现正确的旋转和弹性行为，而子空间 FEM 即使使用 **4 次迭代**仍出现明显阻尼。在哺乳象示例上，全空间 MFEM 每迭代需 263 秒（约 0.003 FPS），而子空间 MFEM 达到 **120 FPS**，实现超过三个数量级的加速（Table 1, Figure 1）。

方法在谱系中的定位清晰：在子空间仿真这一支线上，本文以 Skinning Eigenmodes（Benchekroun et al. 2023）替代传统的模态导数（Barbič and James, 2005）作为降阶基，因为后者无法准确重建旋转运动（Figure 5）；在求解器层面，将全空间 MFEM（Trusty et al., SIGGRAPH Asia 2022）的混合格式完整迁移至子空间，并通过 Schur 补缩并实现高效求解；在积分近似层面，以基于 k-means 聚类的 cubature 方案替代传统的 NNLS 贪心训练策略（An et al. 2008），无需训练阶段且自然感知材料与几何异质性——柔软薄壁区域采样密集，刚硬厚实区域采样稀疏（Figure 6, Figure 16）。

## 背景与动机

### 实时异构弹性模拟的核心瓶颈

在计算机图形学与交互式仿真中，对包含显著材料异质性的弹性体进行实时模拟一直是一个突出问题。许多自然与人造物体——例如同时具有坚硬外壳与柔软关节的螃蟹、由骨骼、肌肉和关节构成的生物体——其杨氏模量（Young’s modulus）可在不同区域跨越数个数量级。这种极端的刚度差异对数值求解器构成了严峻挑战。

传统子空间方法（如模态分析、本征正交分解等）通过在预先计算的低维基上投影全空间动力学，大幅降低了计算复杂度，是实现实时仿真的主流路线。然而，这些方法在强材料异质性下面临一个**根本性瓶颈**：求解器收敛极为缓慢。当时间步长或计算预算受限时，求解过程被迫在远未收敛的状态下截断。对于标准的子空间有限元法（Subspace FEM），这种过早截断会导致两个显著的视觉缺陷：

- **旋转运动被虚假阻尼**：物体在自由旋转时角动量无法保持，运动幅度被系统性低估。
- **弹性响应失真**：柔软区域的变形无法充分展开，整体行为偏离物理真实。

换言之，传统子空间方法在“快”与“准”之间存在难以调和的矛盾：要么接受不可接受的伪影以换取实时帧率，要么在迭代上投入大量计算而失去实时性。

### 混合有限元法的潜力与局限

全空间混合有限元法（Mixed FEM, MFEM）为上述困境提供了一条出路。其核心思想是在标准的位置自由度（DOF）之外，为每个网格单元引入**辅助拉伸自由度**（auxiliary stretch DOF），并通过显式约束维持两者的一致性。这一鞍点问题形式（saddle-point formulation）使得求解器在极低迭代次数下即可保持正确的旋转运动，从而天然适合处理异质材料。

然而，全空间 MFEM 的计算代价极高。以论文中的猛犸象模型（约 9.8 万顶点、53.1 万四面体）为例，单次全空间 MFEM 迭代耗时约 263 秒（约 0.003 FPS），完全无法满足实时需求。因此，MFEM 的旋转保持优势虽好，却因计算量过大而无法直接应用于交互式场景。

### 本文的核心动机

上述分析揭示了一个清晰的研究缺口：**能否将 MFEM 的旋转保持能力与子空间降维的计算效率结合起来？**

这一结合面临三个关键技术挑战：

1. **子空间基的选择**：全空间 MFEM 的旋转保持能力依赖于位置与拉伸自由度的协同优化。若子空间基无法精确表示旋转运动，则降维后的 MFEM 将丧失其核心优势。经典的模态导数（modal derivatives）子空间在重建输入形状的旋转时会产生明显伪影，需要额外跟踪刚体框架来修正（Figure 5），并非理想选择。

2. **非线性积分的降阶**：弹性模拟中，非线性应变能需要在所有网格元素上积分。即使位置自由度被压缩到子空间，若仍对全部四面体进行精确积分，计算量依然与全网格规模挂钩，无法实现真正的性能脱钩。

3. **拉伸自由度的放置策略**：在全空间 MFEM 中，拉伸自由度附着于每一个网格元素。降维后，若拉伸自由度仍遍布全网格，则子空间缩并带来的收益将被严重稀释。需要一种与子空间规模相匹配的稀疏放置方案。

本文的动机正是系统性地解决这三个挑战，构建一个在极低迭代次数下既能保持正确旋转运动、又能实现实时性能的异构弹性模拟框架。其核心洞察在于：**将材料感知的 Skinning Eigenmode 子空间与 MFEM 格式相结合，并辅以异质性敏感的 cubature 积分近似，可使模拟性能完全与网格分辨率脱钩。**

## 核心创新

本文的核心创新在于将**混合有限元法（MFEM）**的旋转保持能力与**Skinning Eigenmode 子空间**的降维表达能力深度耦合，并通过**异质性感知的 cubature 近似**实现非线性弹性积分的加速，从而构建了一个性能与网格分辨率完全脱钩的实时异构弹性力学求解器。

### 创新一：子空间 MFEM 格式——将辅助拉伸自由度引入降阶求解

传统子空间 FEM 直接在 skinning 子空间基 $B$ 上对位置自由度 $x \approx B u$ 进行降阶求解。然而，在强材料异质性下，这种纯位移格式在低迭代次数时会出现严重的旋转阻尼伪影。本文的关键洞察是：**MFEM 中引入的辅助拉伸自由度 $s$ 及其与位置自由度的一致性约束 $c(x,s)$，恰好为子空间求解提供了一个“旋转保持”的因果调节旋钮**。

具体而言，作者将全空间 MFEM 的鞍点问题

$$x^{*}, s^{*}, \lambda^{*} = \operatorname*{argmin}_{x,s} \operatorname*{max}_{\lambda} \Psi_{x}(x) + \Psi_{s}(s) + \lambda^{T} c(x,s)$$

完全迁移到子空间变量 $(u, z, \mu)$ 上，形成降阶优化问题

$$u^{*}, z^{*}, \mu^{*} = \operatorname*{argmin}_{u,z} \operatorname*{max}_{\mu} \Psi_{u}(u) + \Psi_{z}(z) + \mu^{T} g(u,z).$$

这一迁移带来了三个关键的 **changed slots**：

| 组件 | 基线方法（子空间 FEM） | 本文方法（子空间 MFEM） |
|------|----------------------|----------------------|
| 位置自由度表示 | $x \approx B u$ | 同左，但 $u$ 的更新受拉伸约束正则化 |
| 拉伸自由度放置 | 无（纯位移格式） | 拉伸 DOF $z$ 仅放置在 cubature 点上，数量远小于全网格单元数 |
| 非线性弹性积分 | 对所有四面体精确积分 | 基于 k-means 聚类的 cubature 近似，仅计算 $|C|$ 个选中四面体 |

在每步 SQP 迭代中，通过 Schur 补技术从 KKT 系统中消去拉伸变量 $z$ 和乘子 $\mu$，得到仅关于 $du$ 的缩并系统

$$(H_{u} + K) du = -f_{u} + G_{u}^{T} G_{z}^{-1} (f_{z} - H_{z} G_{z}^{-1} f_{\mu}),$$

其中 $K$ 项编码了拉伸自由度对位置更新的正则化效应。这一设计使得求解器在**仅 2 次迭代**时即可展现正确的旋转行为，而子空间 FEM 即使在 4 次迭代下仍出现明显阻尼（Figure 2）。

### 创新二：异质性感知的 cubature 方案——无需训练的 k-means 聚类

传统 cubature 方法（如 An et al. 2008）依赖 NNLS 拟合训练数据的贪心策略来选择积分点。本文提出了一种**完全无需训练阶段**的替代方案：

1. 利用 Skinning Eigenmodes 求解得到的蒙皮权重 $W$ 和广义特征值 $\Gamma$，构造加权特征 $\mathcal{W}_{\mathcal{T}} \Gamma^{-2}$；
2. 对该加权特征执行 k-means 聚类，取聚类质心最近的四面体作为 cubature 点；
3. 每个 cubature 点的积分权重设为其所属簇的质量。

这一方案的关键优势在于**自然感知材料和几何异质性**：在杨氏模量较低的柔软/薄区域，蒙皮权重的高频模式集中，导致聚类密度更高；而在刚硬/厚区域，采样点则更为稀疏（Figure 6, Figure 16）。消融实验表明，cubature 点数量过少会导致柔软区域的人工软化，作者建议采用 $20 \times$ skinning modes 数量的启发式规则（Figure 14）。

### 创新三：Skinning Eigenmode 子空间——材料感知的旋转表示基

子空间基 $B$ 的质量直接决定了降阶求解的上限。本文选择 **Skinning Eigenmodes**（Benchekroun et al. 2023）而非传统的模态导数（Barbič and James 2005）来构建蒙皮子空间，原因在于：

- 模态导数在重建输入形状的旋转时会产生明显伪影，通常需要显式跟踪刚体框架来修复（Figure 5）；
- Skinning Eigenmodes 通过求解权空间广义特征值问题 $H_{w} W = M_{w} W \Gamma$ 获得材料感知的蒙皮权重，高频模式自动集中于柔软区域，刚硬区域仅分配恒定模式（Figure 4）。

这一选择使得子空间基天然具备旋转表示能力，为 MFEM 格式在低迭代次数下的旋转保持提供了基础保障。消融实验进一步证实，使用材料感知的 Skinning Eigenmodes 在处理尖锐异质材料（如极端扭转）时，显著优于基于光滑局部蒙皮权重的方案（Figure 8）。

### 创新四：性能与网格分辨率脱钩的实时求解

上述三个创新的协同效应使得求解器性能**完全与网格分辨率脱钩**：子空间变量 $(u, z, \mu)$ 的维度仅取决于 skinning modes 数量 $m$ 和 cubature 点数 $|C|$，与原始网格顶点数 $|\mathcal{V}|$ 无关。在哺乳象示例（98K 顶点，531K 四面体）上，子空间 MFEM 达到 120 FPS，相对于全空间 MFEM 的 0.003 FPS 实现了超过三个数量级的加速（Table 1, Figure 1）。计时分解显示，MFEM 仿真时间主要由 $O(m^2 k)$ 的稠密矩阵组装主导，而额外的局部拉伸和乘子求解仅增加可忽略的计算开销（Figure 10）。

## 整体框架

本文提出的**子空间混合有限元法（Subspace MFEM）**通过三个核心设计将异构弹性力学模拟推至实时：**材料感知的 Skinning Eigenmode 子空间**、**异质性自适应的 cubature 积分近似**，以及**混合有限元格式**本身。三者协同使得求解代价与网格分辨率完全脱钩，同时在全空间 MFEM 的基础上实现超过三个数量级的加速（猛犸象示例：从 263 秒/迭代降至 120 FPS，见 Table 1 与 Figure 1）。

![[assets/figures/papers/paper_list_l46_https_arxiv_org_abs_2405_13730/figures/001_Figure_1.jpg]]
*Figure 1: We propose a reduced space mixed finite element method (MFEM) built on a Skinning Eigenmode subspace and materialaware cubature scheme. Our solver is well-suited for simulating scenes with large material and geometric heterogeneities in real-time. This mammoth geometry is composed of 98,175 vertices and 531,565 tetrahedral elements and with a heterogenous composition of widely varying materials of muscles ( E = 5 $\times$ 1 $0 ^ { 5 }$ \ $\mathbf { P a }$ ) , joints ( E = 1 $\times$ 1 $0 ^ { 5 }$ \ $\mathbf { P a }$ ) , and bone ( E = 1 $\times$ 1 $0 ^ { 1 0 }$ \ $\mathbf { P a }$ ) . The resulting simulation runs at 120 frames per second (FPS)

### 管道概览

整个方法分为**离线预处理**和**在线实时仿真**两个阶段，模块间数据流如下：

1. **Skinning Eigenmode 子空间构建（离线）**
   - 输入：异构四面体网格及其材料场（杨氏模量分布）。
   - 过程：求解权空间广义特征值问题 $H_w W = M_w W \Gamma$，获得材料感知的 skinning weights $W$（Eq. (9)）。高频模式自然集中于柔软区域，刚硬区域则分配低频模式（Figure 4）。
   - 输出：线性融合蒙皮雅可比矩阵 $B$，将全空间节点位置 $x$ 近似为 $x \approx B u$，其中 $u$ 为降阶位置系数（Eq. (10)）。

2. **Cubature 近似构建（离线）**
   - 输入：skinning weights $W$ 与特征值矩阵 $\Gamma$。
   - 过程：以 $\mathcal{W}_{\mathcal{T}} \Gamma^{-2}$ 为权重对四面体进行 k-means 聚类，取各簇质心最近邻的四面体作为 cubature 点（Eq. (11)）。该方案无需训练阶段，且天然感知材料和几何异质性——柔软/薄区域采样密集，刚硬/厚区域采样稀疏（Figure 6, Figure 16）。
   - 输出：cubature 点集 $C$ 及其质量权重，用于近似非线性弹性积分。

3. **降阶优化问题建立（在线）**
   - 输入：子空间基 $B$、cubature 点集 $C$、当前时间步状态。
   - 过程：将全空间 MFEM 鞍点问题（Eq. (1)）改写为完全在子空间变量上的形式——位置系数 $u$、仅置于 cubature 点上的拉伸自由度 $z$，以及拉格朗日乘子 $\mu$（Eq. (4)）。拉伸能量 $\Psi_z$ 和一致性约束 $g(u,z)$ 均仅在 $C$ 上计算，大幅削减积分成本。

4. **SQP 迭代与 Schur 补求解（在线）**
   - 每步求解缩并的 KKT 系统以获取位置搜索方向 $du$（Eq. (5)）。
   - 通过 Schur 补消去拉伸和乘子变量，得到仅关于 $du$ 的线性系统 $(H_u + K) du = -f_u + \cdots$（Eq. (6)），其规模仅取决于 skinning modes 数量 $m$ 和 cubature 点数 $k$，与网格分辨率无关。
   - 随后通过局部分解依次更新 $dz$ 和 $d\mu$（Eq. (7)–(8)）。MFEM 相较 FEM 的额外计算仅在于此局部求解步骤。

5. **全空间投影（在线，GPU）**
   - 将更新后的子空间系数 $u$ 通过 $x = B u$ 投影回全空间网格顶点，得到可渲染的变形几何。该步骤在 GPU 上完成，其时间单独列出，不影响 MFEM 与 FEM 求解器核心的相对比较。

### 关键因果链

传统子空间 FEM 在强材料异质性下收敛缓慢，过早截断迭代会导致可见的阻尼伪影和旋转误差——这是本文识别的**核心瓶颈**。其因果调控变量在于：FEM 的纯位移格式将旋转与拉伸耦合在同一能量泛函中，低迭代时旋转分量无法被充分解析。

MFEM 通过**引入辅助拉伸自由度并施加显式一致性约束**，将旋转运动与拉伸变形解耦——位置自由度承载旋转，拉伸自由度承载局部形变，约束确保两者几何一致。这一混合格式使得即使仅 2 次求解器迭代，子空间 MFEM 也能在刚度差异达 $10^4$ 倍的螃蟹模型上展现正确的旋转和弹性行为，而子空间 FEM 在 4 次迭代下仍明显阻尼（Figure 2）。

将该混合格式与 Skinning Eigenmode 子空间结合是方法成立的**决定性洞察**：Skinning Eigenmode 子空间能够精确重建旋转（Figure 5），而模态导数则不能；同时其材料感知特性使子空间基天然适配异质场景。cubature 方案则将非线性积分的计算量从全网格四面体数降至 $O(k)$，且通过异质性感知采样保证近似精度。

### 证据强度说明

- **核心性能声明**（120 FPS vs. 0.003 FPS）来自 Table 1 和 Figure 1，置信度高（0.95）。
- **低迭代旋转保持**由 Figure 2、Figure 7 和 Figure 13（解旋摆角动量验证）三重支撑，置信度高（0.95）。
- **cubature 异质性感知**由 Figure 6 和 Figure 16 可视化验证，置信度较高（0.93）。
- **消融实验中 cubature 点数启发式规则**（20× skinning modes）来自 Figure 14 的经验观察，置信度中等（0.85），实际应用中可能需要根据场景调整。
- **全局子空间远端伪影**（Figure 12）是已知局限，需手动验证增加模式数在特定场景下的缓解效果。

## 核心模块与公式推导

### 模块一：Skinning Eigenmode 子空间构建

子空间 MFEM 的核心在于用一个低维线性子空间 $\mathbf{B} \in \mathbb{R}^{3|\mathcal{V}| \times r}$ 来近似全空间的位置自由度 $\mathbf{x} \approx \mathbf{B} \mathbf{u}$（Eq. 4）。该子空间基于 **Skinning Eigenmodes**（Benchekroun et al., 2023）构建，其关键优势在于生成的蒙皮权重天然具有材料感知能力——高频模式集中于柔软区域，而刚硬区域仅分配到常值模式（Figure 4）。

构建流程分为两步：

**第一步：求解权重空间广义特征值问题**  
蒙皮权重 $\mathbf{W} \in \mathbb{R}^{|\mathcal{V}| \times m}$ 通过以下广义特征值问题获得（Eq. 9）：

$$\mathbf{H}_w \mathbf{W} = \mathbf{M}_w \mathbf{W} \mathbf{\Gamma}$$

其中 $\mathbf{H}_w$ 是基于弹性能量的拉普拉斯矩阵，编码了材料的刚度分布信息；$\mathbf{M}_w$ 是标量质量矩阵；$\mathbf{\Gamma}$ 为特征值对角阵。这一公式的因果机制在于：$\mathbf{H}_w$ 将材料异质性直接注入特征空间，使得求得的 $\mathbf{W}$ 的每一列（即每个蒙皮模式）的振动频率与局部刚度耦合。

**第二步：构造线性融合蒙皮雅可比**  
从蒙皮权重 $\mathbf{W}$ 和静止位置 $\bar{\mathbf{X}}$ 构造子空间基 $\mathbf{B}$（Eq. 10）：

$$\mathbf{B} = \mathbf{I}_3 \otimes \left( (\mathbf{1}_m^T \otimes \bar{\mathbf{X}}) \odot (\mathbf{W} \otimes \mathbf{1}_4^T) \right)$$

此公式将标量蒙皮权重扩展为三维位移的雅可比矩阵，使得子空间系数 $\mathbf{u}$ 的每一次更新可以直接通过 $\mathbf{x} = \mathbf{B} \mathbf{u}$ 投影回全空间网格。

**关键消融证据**：Figure 8 显示，使用光滑局部蒙皮权重（如 Bounded Biharmonic Weights）在尖锐异质材料上会导致极端扭转运动的分辨率不足，而 Skinning Eigenmodes 能锐利地捕捉这些运动。Figure 5 进一步表明，模态导数（modal derivatives）无法正确重建输入形状上的旋转，而 skinning subspace 天然支持旋转运动。

---

### 模块二：异质性感知的 Cubature 近似构建

为加速子空间内非线性拉伸能量 $\Psi_z(\cdot)$ 和一致性约束 $\mathbf{g}(\mathbf{u}, \mathbf{z})$ 的计算，方法引入数值 cubature 近似——仅在 $|\mathcal{C}|$ 个选定的四面体上计算积分，而非遍历全部 $|\mathcal{T}|$ 个元素。

**Cubature 点选择策略**：与传统基于 NNLS 拟合训练数据的贪心策略（An et al., 2008）不同，本文提出一种无需训练阶段的 k-means 聚类方案（Eq. 11）：

$$l = \mathrm{kmeans}\left( \mathcal{W}_{\mathcal{T}} \mathbf{\Gamma}^{-2}, |\mathcal{C}| \right)$$

具体而言，每个四面体的蒙皮权重向量 $\mathcal{W}_{\mathcal{T}}$ 被特征值平方的倒数 $\mathbf{\Gamma}^{-2}$ 加权后进行 k-means 聚类，聚类质心最近的四面体被选为 cubature 点，其权重设为该簇的质量。

**因果机制**：$\mathbf{\Gamma}^{-2}$ 加权使得高频模式（对应柔软区域）在聚类中获得更大权重，导致 cubature 点密集采样于柔软/薄壁区域，稀疏采样于刚硬/厚实区域。Figure 6 和 Figure 16 验证了这一行为——cubature 点对杨氏模量异质性和几何薄区均表现出自然的感知能力。

**消融与启发式规则**：Figure 14 显示，cubature 点过少会导致欠积分，使柔软区域出现人工软化。论文建议采用 $|\mathcal{C}| \approx 20 \times m$（即 20 倍 skinning modes 数量）作为启发式规则。

---

### 模块三：降阶优化问题建立

将全空间 MFEM 鞍点问题（Eq. 1）改写为完全在子空间变量上定义的降阶优化问题（Eq. 4）：

$$\mathbf{u}^*, \mathbf{z}^*, \boldsymbol{\mu}^* = \operatorname*{argmin}_{\mathbf{u}, \mathbf{z}} \operatorname*{max}_{\boldsymbol{\mu}} \; \Psi_u(\mathbf{u}) + \Psi_z(\mathbf{z}) + \boldsymbol{\mu}^T \mathbf{g}(\mathbf{u}, \mathbf{z})$$

其中 $\mathbf{u}$ 为位置子空间系数，$\mathbf{z}$ 为仅放置在 cubature 点上的拉伸自由度，$\boldsymbol{\mu}$ 为拉格朗日乘子。$\Psi_u(\mathbf{u})$ 是位置能量在子空间中的投影，$\Psi_z(\mathbf{z})$ 是拉伸能量，$\mathbf{g}(\mathbf{u}, \mathbf{z})$ 强制位置与拉伸自由度之间的一致性约束。

**关键设计决策**：拉伸自由度 $\mathbf{z}$ 的放置位置从全空间每个网格元素缩减到仅 cubature 点上，这一改变使得降阶后的一致性约束维度和拉伸能量计算复杂度均与 $|\mathcal{C}|$ 而非 $|\mathcal{T}|$ 成正比。

---

### 模块四：SQP 迭代与 Schur 补求解

每步仿真采用序列二次规划（SQP）求解降阶优化问题，核心是求解以下 KKT 系统以获得搜索方向 $d\mathbf{u}$（Eq. 5）：

$$\begin{bmatrix} \mathbf{H}_u & \mathbf{0} & \mathbf{G}_u^T \\ \mathbf{0} & \mathbf{H}_z & \mathbf{G}_z^T \\ \mathbf{G}_u & \mathbf{G}_z & \mathbf{0} \end{bmatrix} \begin{bmatrix} d\mathbf{u} \\ d\mathbf{z} \\ d\boldsymbol{\mu} \end{bmatrix} = -\begin{bmatrix} \mathbf{f}_u \\ \mathbf{f}_z \\ \mathbf{f}_\mu \end{bmatrix}$$

其中 $\mathbf{H}_u$、$\mathbf{H}_z$ 为 Hessian 矩阵，$\mathbf{G}_u$、$\mathbf{G}_z$ 为约束雅可比，$\mathbf{f}_u$、$\mathbf{f}_z$、$\mathbf{f}_\mu$ 为梯度项。

**Schur 补缩并**：由于 $d\mathbf{z}$ 和 $d\boldsymbol{\mu}$ 的局部性（拉伸和乘子变量仅在 cubature 点上定义），可通过舒尔补技巧消去这些变量，得到仅关于 $d\mathbf{u}$ 的缩并系统（Eq. 6）：

$$(\mathbf{H}_u + \mathbf{K}) \, d\mathbf{u} = -\mathbf{f}_u + \mathbf{G}_u^T \mathbf{G}_z^{-1} (\mathbf{f}_z - \mathbf{H}_z \mathbf{G}_z^{-1} \mathbf{f}_\mu)$$

其中 $\mathbf{K} = \mathbf{G}_u^T \mathbf{G}_z^{-1} \mathbf{H}_z \mathbf{G}_z^{-T} \mathbf{G}_u$ 是拉伸和约束带来的附加刚度项。该系统的规模仅由子空间维度 $r$ 决定，与全网格分辨率脱钩——这正是性能瓶颈被打破的根本原因。求解 $d\mathbf{u}$ 后，$d\mathbf{z}$ 和 $d\boldsymbol{\mu}$ 可通过局部分解（Eq. 7）高效恢复。

**收敛行为**：Figure 9 的收敛性测试表明，随着刚度异质性增大，传统 FEM 的收敛速度显著恶化，而 MFEM 保持鲁棒——其根本原因在于混合格式通过拉伸自由度显式解耦了旋转与形变，使得每次迭代的能量下降更接近真实解路径。

---

### 模块五：全空间投影

每步 SQP 迭代完成后，更新后的子空间系数通过 $\mathbf{x} = \mathbf{B} \mathbf{u}$ 投影回全空间网格。该步骤在 GPU 上完成，其时间在性能分解（Figure 10）中被单独列出，不影响 MFEM 与 FEM 求解器核心的相对比较。

## 实验与分析

### 核心性能与加速比

子空间 MFEM 在极端异构场景下实现了从全空间求解到实时交互的跨越。以 **Mammoth** 模型（98K 顶点，531K 四面体，含骨骼/肌肉/关节异质材料）为例，全空间 MFEM 每迭代耗时 263 秒（约 0.003 FPS），而子空间 MFEM 达到 **120 FPS**，加速比超过三个数量级（Table 1; Figure 1）。这一性能提升的关键在于：位置自由度从全网格节点压缩至 Skinning Eigenmode 子空间系数，拉伸自由度仅放置在 cubature 点上，且非线性弹性积分通过 k-means 聚类 cubature 近似完成，使得求解器计算量完全与网格分辨率脱钩。

![[assets/figures/papers/paper_list_l46_https_arxiv_org_abs_2405_13730/figures/009_Table_1.jpg]]
*Table 1: We report average times (in milliseconds) for one iteration of subspace MFEM/FEM and full-space simulations for meshes of various complexity. MFEM corresponds to a simulation step time for our subspace mixed FEM solver, FEM is the time for a subspace FEM solve step, and ?? and |C| are, respectively, the number of skinning modes and cubature points used in both subspace solvers. Proj is the time for the full-space projection used in the subspace solvers. Lastly, Full MFEM is the time for a full-space MFEM iteration (Trusty et al. [2022])*

### 低迭代次数下的旋转保持能力

子空间 MFEM 的核心优势体现在极低求解器迭代次数下的旋转保真度。**Figure 2** 的螃蟹模型具有极端刚度差异（外壳 $E=10^{10}$ Pa，关节 $E=10^6$ Pa）：仅需 **2 次** SQP 迭代，子空间 MFEM 即展现正确的旋转和弹性行为；而使用相同 skinning 子空间和 cubature 积分的子空间 FEM，即使使用 **4 次**迭代仍出现明显阻尼伪影。这意味着 MFEM 在保持帧率的同时，仅需 FEM 一半的迭代次数即可获得更优的运动质量。

定量验证来自剑模型角运动追踪实验（**Figure 7**）：在仿真前 25 个时间步内，子空间 MFEM 几乎完美复现目标角运动轨迹，而 FEM 持续低估角位移。MFEM 通常在约 1 次迭代内即可恢复旋转运动，这归因于混合格式中拉伸自由度与位置自由度之间的一致性约束，有效抑制了过早截断造成的能量耗散。

### 异质性感知的 Cubature 采样

所提出的 k-means 聚类 cubature 方案无需训练阶段，且自然感知材料和几何异质性（**Figure 6, Figure 16**）。聚类基于 skinning weights 加权 $\Gamma^{-2}$ 进行，使得采样点密度自适应分布：柔软/薄区域密集采样以捕获丰富变形，刚硬/厚区域稀疏采样以节省计算。Figure 16 进一步展示了该方案对几何特征和约束的感知能力——在薄区域密集采样，而在固定端仅分配单个采样点。

![[assets/figures/papers/paper_list_l46_https_arxiv_org_abs_2405_13730/figures/006_Figure_6.jpg]]
*Figure 6: Our cubature points are found as the centroids of each k-means cluster. Note that our centroids are sensitive to the heterogeneity of the Young’s modulus. Stiffer regions can have their strain be approximated with fewer cubature points*

### 消融实验

**Skinning Eigenmodes 的必要性**：Figure 8 对比了光滑局部蒙皮权重（如 Bounded Biharmonic Weights）与 Skinning Eigenmodes 在尖锐异质材料上的表现。Skining Eigenmodes 能够清晰分辨极端扭转运动中的材料边界，而光滑权重导致异质界面处的运动模糊。Figure 4 可视化了 Skinning Eigenmodes 产生的材料感知蒙皮权重分布——高频模式自然集中于柔软区域。

**子空间规模的影响**：Figure 12 揭示了全局支持子空间的固有限制——弯曲猛犸象膝盖时会引起躯干的非期望变形。该伪影随 skinning modes 数量增加而消失，表明增大子空间是缓解远端伪影的有效手段。

**Cubature 点数量的敏感性**：Figure 14 表明欠积分会导致柔软区域的人工软化。论文建议采用启发式规则：cubature 点数取 **20 倍** skinning modes 数量，以在精度和效率间取得平衡。

**异质性程度对收敛的影响**：Figure 9 系统测试了不同刚度异质性下的收敛行为。随着材料异质性增大，FEM 收敛显著变慢，而 MFEM 保持鲁棒的收敛速度。这一特性使 MFEM 特别适合处理具有尖锐材料界面的场景。

### 计时分解与瓶颈分析

Figure 10 给出了 Octobot、Gatorman、Crab 和 Mammoth 四个场景的单步仿真计时分解。MFEM 相较于 FEM 的额外计算仅来自局部拉伸和拉格朗日乘子求解（Eq. (7)），该步骤可在每个 cubature 点上独立并行完成。仿真时间的主要瓶颈是 $O(m^2 k)$ 的稠密矩阵组装（其中 $m$ 为 skinning modes 数，$k$ 为 cubature 点数），而非求解器迭代本身。

### 泛化性验证

方法兼容多种超弹性材料模型。Figure 15 展示了在 ARAP、固定协旋转（FCR）和稳定 Neo-Hookean 三种本构下的悬臂梁平衡态仿真，验证了子空间 MFEM 框架的材料无关性。

### 已知局限

1. **全局子空间伪影**：全局支持的 Skinning Eigenmode 子空间在局部激励下可引起远端非期望变形（Figure 12），需通过增加模式数缓解，但这会提升计算成本。
2. **Cubature 欠积分软化**：cubature 点数不足时柔软区域出现人工软化（Figure 14），需依赖启发式规则设定点数。
3. **极低迭代抖动**：在仅 1 次迭代的极端情况下，MFEM 可能因过高的能量保持特性引入抖动伪影。
4. **碰撞处理缺失**：当前框架尚未涉及碰撞和接触模拟，子空间下的接触求解仍是开放问题。

### 补充图表

![[assets/figures/papers/paper_list_l46_https_arxiv_org_abs_2405_13730/figures/013_Figure_13.jpg]]
*Figure 13: We pin the pendulum from the top, twist the bottom end, and simulate the unwinding. We compare results from FEM and MFEM with one solver iteration per timestep against a converged subspace FEM solution. Even at low iterations our MFEM solvers show much better agreement, which is reflected on the plot on the right where total angular momentum for each pendulum block is plotted over time*

## 方法谱系与知识库定位

### 方法沿革与基线关系

本文提出的**子空间混合有限元法**（Subspace MFEM）处于实时物理仿真中两条技术路线的交汇点：子空间降阶技术与混合有限元格式。

**全空间混合有限元法**（Trusty et al., SIGGRAPH Asia 2022）是本文的直接前驱。该方法在完整网格上引入辅助拉伸自由度与一致性约束，将弹性力学时间步求解转化为鞍点问题，从而在低迭代次数下保持正确的旋转运动。然而，全空间MFEM的计算成本与网格分辨率强耦合——例如在哺乳象模型（98K顶点、531K四面体）上，单次迭代耗时263秒，仅能达到约0.003 FPS，远不能满足实时交互需求。本文的核心贡献在于将MFEM格式完整迁移到子空间框架内，使得仿真性能与网格分辨率脱钩，在相同模型上实现超过三个数量级的加速（120 FPS）。

**子空间有限元法**（Subspace FEM）是本文最直接的对比基线。该方法将位置自由度投影到skinning子空间中，但保留了标准的FEM求解格式（即仅最小化位置能量，不引入拉伸自由度和一致性约束）。本文在严格控制的条件下进行了公平比较：子空间MFEM与子空间FEM使用完全相同的skinning eigenmode子空间基和cubature积分方案，仅求解器公式不同。关键发现是，在强材料异质性场景下，子空间FEM即使使用4次求解器迭代仍出现明显的旋转阻尼伪影，而子空间MFEM仅需2次迭代即可展现正确的旋转和弹性行为（Figure 2）。这一差异揭示了混合格式在子空间框架下的独特价值——拉伸自由度的引入使得系统能够以极低的迭代预算保持角动量守恒。

**模态导数子空间**（Barbič and James, 2005）是子空间仿真中的经典方法，通过对线性模态关于材料参数的导数来扩展变形基。本文明确指出，模态导数在重建输入形状的旋转时存在根本性缺陷（Figure 5），通常需要额外跟踪刚体参考系来修正伪影。相比之下，skinning eigenmode子空间天然具备旋转重建能力，因为其基函数由线性混合蒙皮的雅可比矩阵张成，内含刚体运动的精确表示。

### 适用边界与局限

**全局子空间的远端伪影**。Skinning eigenmode子空间具有全局支撑特性，这意味着局部激励可能引起远端区域的非期望变形。例如，弯曲猛犸象的膝盖会导致躯干部位产生伪影（Figure 12）。增大子空间模式数量可以缓解这一问题，但会线性增加计算成本。密集全局子空间与稀疏局部子空间之间的成本-质量权衡机制仍是一个开放问题。

**Cubature积分的启发式依赖**。本文提出的k-means聚类cubature方案无需训练阶段，且能自然感知材料和几何异质性（Figure 6, Figure 16），但其性能依赖于cubature点数量的合理选择。消融实验表明，欠积分会导致柔软区域的人工软化（Figure 14），作者建议采用“20倍skinning模式数”的启发式规则。这一规则在不同场景下的泛化性尚未得到系统验证。

**碰撞处理的缺失**。当前方法未涉及碰撞检测与响应，而子空间框架下的接触模拟仍然是一个公认的开放难题。子空间基的全局性使得局部碰撞约束的施加变得复杂，可能破坏降阶系统的计算效率优势。

**极低迭代次数下的抖动伪影**。当求解器迭代次数降至1次时，MFEM可能因过高的能量保持特性引入抖动伪影。这一现象暗示混合格式在极端低迭代预算下存在稳定性边界，需要进一步的理论分析。

### 开放问题

1. **子空间结构的选择**：密集全局子空间与稀疏局部子空间在异质弹性力学中的成本-质量前沿是什么？是否存在自适应策略，在刚度差异大的区域使用局部基，而在均质区域使用全局基？

2. **接触与碰撞扩展**：如何将子空间MFEM扩展至含自碰撞或环境碰撞的实时仿真场景？可能的路径包括在子空间框架内引入障碍函数法或脉冲约束投影，但需解决约束投影与降阶基的相容性问题。

3. **逆向设计应用**：子空间MFEM的实时性能使其在工程和生物力学中的基于物理的逆向设计（如软体机器人形态优化、假体材料参数辨识）中具有潜力，但需要建立子空间参数与设计变量之间的可微映射关系。

4. **Cubature的自适应选择**：能否根据仿真过程中的变形状态动态调整cubature点分布，以在保持精度的同时进一步降低计算成本？当前静态聚类方案未利用仿真的时间相干性。

5. **多材料模型的理论分析**：本文验证了方法对多种超弹性材料模型（ARAP、FCR、Neo-Hookean）的兼容性（Figure 15），但不同材料模型在混合格式下的收敛行为差异缺乏系统性的理论刻画。

## 原文 PDF

![[paperPDFs/SIGGRAPH_ASIA_2023/Subspace_Mixed_Finite_Elements_for_Real_Time_Heterogeneous_Elastodynamics.pdf]]
