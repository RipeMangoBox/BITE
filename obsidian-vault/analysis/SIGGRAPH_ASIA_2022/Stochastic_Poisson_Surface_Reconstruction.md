---
title: Stochastic Poisson Surface Reconstruction
type: paper
paper_level: A
venue: SIGGRAPH ASIA
year: 2022
pdf_ref: paperPDFs/SIGGRAPH_ASIA_2022/Stochastic_Poisson_Surface_Reconstruction.pdf
project_link: null
code_link: null
aliases:
- SPSRS
- SPSR
tags:
- SIGGRAPH_ASIA_2022
- topic/graphics_geometry_processing
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
core_operator: 通过将PSR解释为高斯过程，引入对称化的协方差函数k_SPSR，并采用基于采样密度的对角块协方差近似（covariance lumping），从而为每个空间点赋予一个高斯分布（均值与方差），使得能够进行统计查询。
primary_logic: 将PSR的向量场插值视为一个向量值高斯过程的后验均值，利用PSR的半协方差对称化得到正定协方差，并通过协方差合并避免求解大矩阵逆问题，从而将重建结果从单一函数提升为完整的概率分布。
claims:
- SPSR的向量场在视觉上与PSR相同，差异可忽略不计。
- SPSR的均值几乎等同于PSR输出，但额外提供方差。
- SPSR计算的内部/外部概率无法从传统PSR值中恢复，体现了统计信息的增益。
- 总不确定度U随着点云增加收敛到零，可作为扫描停止准则。
---

# Stochastic Poisson Surface Reconstruction

> [!tip] 核心洞察
> 将PSR的向量场插值视为一个向量值高斯过程的后验均值，利用PSR的半协方差对称化得到正定协方差，并通过协方差合并避免求解大矩阵逆问题，从而将重建结果从单一函数提升为完整的概率分布。

| 字段 | 内容 |
|------|------|
| 中文题名 | 随机泊松表面重建 |
| 英文题名 | Stochastic Poisson Surface Reconstruction |
| 会议/期刊 | SIGGRAPH ASIA 2022 |
| Links | [paper](https://www.dgp.toronto.edu/projects/stochastic-psr/) |
| Topic | #topic/graphics_geometry_processing #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction |
| Method | Stochastic Poisson Surface Reconstruction (SPSR) |
| Dataset |  |

> [!tip] 效果简介
> - 模拟扫描点云重建 上，总不确定度U 随点云增加收敛至零 vs 无此度量 (提供了可量化的扫描质量度量)。
> - 部分扫描重建（苹果/汽车） 上，重建完整性（视觉） 结合简单几何先验后能恢复封闭表面，而PSR无法闭合 vs PSR无法产生封闭表面 (显著改善重建质量)。
> - 下一最佳视角规划 上，相机得分s = |U(P) - U(P∪p)| 能根据uncertainty减少量对候选视角评分，最高分出现在未扫描侧 vs 无此类统计反馈 (实现了基于信息的视角规划)。

## 概要

传统泊松表面重建（PSR）从带朝向的点云中恢复隐式函数，以零等值面表达重建表面，但该函数在表面外区域的取值是任意的，无法提供统计不确定性信息，因而不能回答“某点在形状内部的概率有多大”“扫描的置信度如何”以及“下一步最佳视角在哪”等关键问题。本文提出**随机泊松表面重建（Stochastic Poisson Surface Reconstruction, SPSR）**，将经典PSR重新解释为高斯过程：通过对称化PSR的半协方差函数获得正定协方差，并引入基于采样密度的对角块协方差近似（covariance lumping）以规避大矩阵求逆，从而为空间中每一点赋予一个高斯分布（均值与方差），将重建结果从单一函数提升为完整的概率分布。

实验表明，SPSR的向量场与隐函数均值在视觉上与传统PSR几乎一致，差异小于2%，但额外提供了方差信息。基于该分布，SPSR可计算点位于物体内部的概率、区域碰撞概率、表面似然以及全局总不确定度等统计量。总不确定度随点云密度增加收敛至零，可作为扫描停止准则；结合简单几何先验后，SPSR能从部分扫描中恢复封闭表面，而PSR无法做到。方法正交于离散化策略，支持自适应网格，且所有统计查询均基于高斯过程理论，未针对特定对象调优。

## 核心方法与创新机理

### 问题瓶颈：PSR隐式函数的统计盲区

传统泊松表面重建（PSR, Kazhdan et al. 2006）输出一个隐式函数 $f(x)$，其零等值面 $f(x)=0$ 即为重建表面。然而，该函数在表面以外区域的值是任意的（见 Fig. 2），缺乏物理意义。这导致 PSR 无法回答一系列关键统计问题：某空间点位于物体内部的概率有多大？扫描的置信度如何？下一步最佳视角在哪里？这些问题的根源在于 PSR 只提供了单一确定性函数，而非完整的概率分布。

### 核心洞察：将PSR重新解释为高斯过程

SPSR 的核心创新在于将 PSR 的向量场插值步骤识别为一个**向量值高斯过程（GP）的后验均值**。这一洞察打开了统计推断的大门：一旦建立了 GP 框架，不仅可以获得均值（即传统 PSR 的输出），还能获得方差，从而为每个空间点赋予完整的高斯分布 $\mathcal{N}(\mu, \sigma^2)$。

然而，直接套用 GP 框架面临两个障碍：

1. **非对称协方差**：PSR 中的“半协方差”函数 $k_{PSR}(x, y)$ 是非对称的，而 GP 要求协方差函数对称且正定。
2. **大矩阵求逆**：标准 GP 需要对训练数据协方差矩阵 $\mathbf{K}_3$ 求逆，计算量随样本数立方增长。

SPSR 通过两个关键操作解决了这些问题。

### 关键机制一：协方差对称化

PSR 的向量场插值可写为：

$$V_{PSR}(q) = \sum_{s \in S} k_{PSR}(q, s) \cdot \vec{n}_s$$

其中 $k_{PSR}(x, y) = \sigma_g \sum_{o \in B(x)} \alpha_{o,x} F_o(y)$ 是 PSR 的半协方差函数。该函数关于 $x$ 和 $y$ 不对称：$k_{PSR}(x, y) \neq k_{PSR}(y, x)$。

SPSR 将其对称化为：

$$k_{SPSR}(x, y) = \frac{1}{2} \left(k_{PSR}(x, y) + k_{PSR}(y, x)\right)$$

这一修改极小——数值差异不超过 2%（见 Fig. 8），且产生的向量场在视觉上与 PSR 完全相同（见 Fig. 7）——但使得协方差函数满足 GP 的正定性要求，从而为统计框架奠定了数学基础。

![[assets/figures/papers/paper_list_l90_https_www_dgp_toronto_edu_projects_stochastic_psr/figures/007_Figure_7.jpg]]
*Figure 7: Our SPSR vector field ??®???????? (right), which uses a symmetrized version ?????????? of the traditional PSR covariance ????????, is visually identical to the PSR vector field ??®?????? (center) for a representative input point cloud (left). In the language of Section 4, the right-most subfigure shows the mean of our vector field Gaussian Process*

![[assets/figures/papers/paper_list_l90_https_www_dgp_toronto_edu_projects_stochastic_psr/figures/008_Figure_8.jpg]]
*Figure 8: To interpret PSR as a Gaussian Process, we define ??????????, a minor modification of the PSR semicovariance ????????. These are visually similar and their difference is small (a maximum of 2%)*

### 关键机制二：协方差合并（Covariance Lumping）

标准 GP 中，给定训练数据 $S$ 后，查询点 $q$ 处的向量场条件分布为：

$$\vec{V}(q) \mid S \sim \mathcal{N}\left(\mathbf{k}_2^\top \mathbf{K}_3^{-1} \vec{N}_s,\; k_1 - \mathbf{k}_2^\top \mathbf{K}_3^{-1} \mathbf{k}_2\right)$$

其中 $\mathbf{K}_3$ 是训练样本间的协方差矩阵，求逆开销巨大。

SPSR 提出**协方差合并**：假设每个样本独立，但方差反比于局部采样密度。这产生一个对角近似矩阵：

$$\mathbf{D} := \text{diag}(\sigma_g w) \approx \mathbf{K}_3$$

其中权重 $w$ 与采样密度成反比。这一近似避免了矩阵求逆，同时保持了关键的**幅度不变性**——即向量场的大小不随采样密度变化（见 Fig. 9 对比）。相比之下，简单的独立同分布假设会使幅度随采样密度缩放，破坏几何一致性。理论分析表明，该近似在三种渐近情况下误差有界且行为正确：训练点相距较远时、查询点远离训练数据时、训练点密集到特征相似时（见 Fig. 27 及附录 B）。

![[assets/figures/papers/paper_list_l90_https_www_dgp_toronto_edu_projects_stochastic_psr/figures/009_Figure_9.jpg]]
*Figure 9: One can avoid the GP sample covariance matrix inversion (center left) by assuming samples to be independent (center right). This makes magnitudes proportional to sampling density (see highlight). Our covariance lumping approximates the full GP with invariant magnitudes (right)*

### 模块流程与因果关系

SPSR 的完整推理管线包含三个级联模块：

**模块一：向量场高斯过程插值**

输入带朝向的点云 $S = \{(p_i, \vec{n}_i)\}$。对每个查询点 $q$，利用对称化协方差 $k_{SPSR}$ 和对角合并矩阵 $\mathbf{D}$，计算向量场的条件高斯分布：

$$\vec{V}(q) \mid S \sim \mathcal{N}\left(\mathbf{k}_2^\top \mathbf{D}^{-1} \vec{N}_s,\; k_1 - \mathbf{k}_2^\top \mathbf{D}^{-1} \mathbf{k}_2\right)$$

输出为每个网格节点的向量场均值 $\vec{V}_{SPSR}$ 与方差。该模块的因果关系是：**对称化协方差 → 有效 GP 定义 → 对角合并 → 可计算的向量场分布**。

**模块二：全局泊松求解获得隐函数分布**

向量场的分布通过离散泊松方程传递到隐函数 $f$：

$$\mathbf{L} \mathbf{f} = \mathbf{Z} \mathbf{v}$$

其中 $\mathbf{L}$ 是拉普拉斯矩阵，$\mathbf{Z}$ 是散度算子。由于 $\mathbf{v}$ 服从高斯分布，线性变换后 $\mathbf{f}$ 也服从高斯分布，其协方差矩阵为：

$$\mathbf{K}_f = \mathbf{L}^{-1} \mathbf{Z} \mathbf{K}_v \mathbf{Z}^\top \mathbf{L}^{-\top}$$

直接计算完整的 $\mathbf{K}_f$ 开销巨大。SPSR 通过**拉普拉斯特征函数谱分解**近似 $\mathbf{K}_f$，且观察到大多数统计查询仅需 $\mathbf{K}_f$ 的对角项（即每个点的方差），大幅降低计算量。该模块的因果关系是：**向量场分布 → 泊松方程线性传播 → 隐函数完整分布**。

**模块三：统计查询计算**

获得 $\mathbf{f} \sim \mathcal{N}(\mathbf{f}_{SPSR}, \mathbf{K}_f)$ 后，可回答多种统计查询：

- **内部概率**：$p(\mathbf{f}_i \le 0) = \text{CDF}_{\mathbf{f}_{SPSR,i}, \sigma_i^2}(0)$
- **表面概率密度**：$p(\mathbf{f}_i = 0) = \text{PDF}_{\mathbf{f}_{SPSR,i}, \sigma_i^2}(0)$
- **总不确定度**：$U_{SPSR} = \int_B \left(0.5 - |P(x \in \Omega) - 0.5|\right) dx$
- **下一最佳视角评分**：$s = |U_{SPSR}(P) - U_{SPSR}(P \cup p)|$

该模块的因果关系是：**隐函数分布 → CDF/PDF 查询 → 可操作的统计决策量**。

### 与传统PSR的Changed Slots总结

| 组件 | 传统PSR | SPSR |
|------|---------|------|
| 协方差函数 | $k_{PSR}$（非对称） | $k_{SPSR}$（对称化） |
| 训练数据协方差 | 需 $\mathbf{K}_3^{-1}$ | 对角合并矩阵 $\mathbf{D}$ |
| 输出类型 | 确定性函数值 | 高斯分布（均值+方差） |
| 统计查询 | 不支持 | 概率、不确定度、置信区间 |

SPSR 的均值输出几乎等同于 PSR（见 Fig. 3），因此继承了 PSR 的所有几何保真度优势，同时额外提供了完整的统计形式化。该框架正交于离散化策略（支持四叉树/八叉树自适应网格，见 Fig. 16），且输入要求与 PSR 完全一致（带朝向的点云），未引入额外数据偏见。

![[assets/figures/papers/paper_list_l90_https_www_dgp_toronto_edu_projects_stochastic_psr/figures/003_Figure_3.jpg]]
*Figure 3: Our Stochastic PSR extends the traditional PSR into a statistical distribution whose mean is nearly identical to the PSR output*

![[assets/figures/papers/paper_list_l90_https_www_dgp_toronto_edu_projects_stochastic_psr/figures/025_Figure_25.jpg]]
*Figure 25: Many of our results follow a similar pipeline: we use a groundtruth object (left) and simulate scanning it from different directions to obtain an oriented point cloud (middle), which we then pass as input to our Stochastic PSR algorithm (right) to compute the desired statistical quantity*

## 实验与关键发现

SPSR的实验设计围绕一个核心命题展开：**将PSR从确定性隐函数提升为概率分布后，能否在不损害原始重建质量的前提下，提供传统方法无法给出的统计信息，并解锁新的应用能力？** 实验从几何一致性验证、统计信息增益、下游任务赋能三个层次递进展开。

### 1. 几何一致性验证：均值等价于PSR

SPSR的首要诉求是保证其输出的均值与经典PSR在几何上等价。实验从两个层面验证了这一点：

**向量场层面的等价性。** 如Fig. 7所示，采用对称化协方差后的SPSR向量场（右）与PSR向量场（中）在视觉上完全一致。作者进一步量化了这一差异：PSR的半协方差与SPSR的对称化协方差之间的数值差异不超过2%（Fig. 8及附录A）。这一微小修改是SPSR能被解释为有效高斯过程的关键——对称化保证了协方差矩阵的正定性，但几乎不改变向量场插值结果。

**隐函数层面的等价性。** Fig. 3的标题明确指出：“SPSR的均值几乎等同于PSR输出”。这意味着用户可以在获得与经典PSR相同重建表面（零等值面）的同时，额外获得每个空间点的方差信息。Fig. 17进一步展示了这一特性：SPSR可以像PSR一样提取均值等值面，但网格上还附带了方差着色。

**关键结论：** SPSR的均值等值面与PSR输出在视觉和数值上几乎无差异，差异被控制在2%以内。这确保了SPSR是PSR的严格超集——不牺牲任何几何精度，仅增加统计维度。

### 2. 统计信息增益：概率无法从PSR值中恢复

SPSR的核心价值在于提供了传统PSR无法给出的概率信息。Fig. 6通过直方图对比（对数坐标）证明了这一论断：**SPSR提供的内部/外部概率考虑了采样密度和空间配置，无法从PSR的隐函数值中恢复。** 这是SPSR区别于PSR的根本性增益——PSR在零等值面外的函数值大小是任意的（Fig. 2），而SPSR的方差则编码了采样信息。

具体而言，SPSR支持以下统计查询：
- **点位于物体内部的概率**（Eq. 26）：$p(\mathbf{f}_i \le 0) = CDF_{\mathbf{f}_{SPSR,i}, \sigma_i^2}(0)$
- **点位于表面的概率密度**（Eq. 27）：$p(\mathbf{f}_i = 0) = PDF_{\mathbf{f}_{SPSR,i}, \sigma_i^2}(0)$
- **区域联合概率**（Fig. 12右）：可计算空间区域的联合内部/外部概率
- **置信区间**（Fig. 14）：利用正态分布的68-95-99.7规则，可给出隐函数值的置信区间

Fig. 13系统展示了这些统计查询的输出：均值与方差（中左）完全确定隐函数分布，进而支持体积内概率（中右）和表面概率（右）的计算。

### 3. 总不确定度：可量化的扫描质量度量

SPSR引入了一个全局度量——**总不确定度** $U_{SPSR}$（Eq. 28）：

$$U_{SPSR} = \int_B \left(0.5 - |P(x \in \Omega) - 0.5|\right) dx$$

该度量在概率完全确定（0或1）时收敛至零。Fig. 15的实验验证了这一性质：**随着模拟扫描点云不断增加，总不确定度U单调收敛至零。** 这一特性使U可以作为扫描停止准则——当U低于预设阈值时，表明已采集足够信息，可终止扫描。Fig. 17展示了利用U阈值作为停止条件的实际效果，并与PSR等值面提取进行了对比。

### 4. 关键消融实验

**消融1：对称化协方差的必要性。** 如Fig. 7和Fig. 8所示，将PSR的半协方差 $k_{PSR}(x,y)$ 对称化为 $k_{SPSR}(x,y) = \frac{1}{2}(k_{PSR}(x,y) + k_{PSR}(y,x))$ 是使高斯过程框架数学有效的前提。消融表明这一修改在视觉上无差异，数值差异<2%，但使得协方差矩阵正定，从而GP条件分布公式成立。

**消融2：协方差合并（covariance lumping）的有效性。** Fig. 9对比了三种策略：（1）完整的GP样本协方差矩阵求逆（中左，计算量大）；（2）假设样本完全独立（中右，导致幅度与采样密度成正比，见高亮区域）；（3）本文的协方差合并（右，保持幅度不变性）。消融表明，合并方案既避免了矩阵求逆的高昂开销，又保持了幅度对采样密度的不变性——附录B进一步证明了该近似的误差有界且具有正确的渐近行为（Fig. 27展示了三种渐近正确的情况）。

**消融3：仅需计算协方差对角项。** 作者指出“大多数统计查询仅需要 $K_f$ 的对角项”（Section 4.2），这大幅减少了计算量。通过Laplacian特征函数谱分解近似 $K_f$，SPSR只需计算对角或部分行/列即可响应内部概率、表面概率、总不确定度等查询。

### 5. 应用验证与边界条件

**部分扫描重建（Fig. 18, Fig. 19）。** 在苹果和汽车的部分扫描数据上，PSR无法产生封闭表面，vanilla SPSR同样不能闭合，但SPSR额外提供了方差信息以标识不确定区域。当结合简单的任务相关先验（球面或椭球面先验）后，SPSR能显著改善重建质量，恢复封闭表面。这表明SPSR的概率框架天然支持先验融合。

**下一最佳视角规划（Fig. 25, Fig. 26）。** SPSR利用总不确定度变化定义相机得分 $s = |U_{SPSR}(P) - U_{SPSR}(P \cup p)|$（Eq. 35），可对候选视角进行评分。实验表明，最高分出现在未扫描侧，验证了基于信息增益的视角规划能力。

**碰撞检测（Fig. 20, Fig. 22）。** SPSR可计算区域碰撞概率（图中加粗显示），而传统PSR无法提供此类统计量。通过阈值化概率等值面还可生成用于碰撞检测的网格。

**真实数据验证（Fig. 23）。** 在真实手机扫描数据上，SPSR的重建几何与PSR相同，但额外提供了方差和体积统计量，验证了方法的实用性。

### 6. 失败模式与限制

尽管SPSR在统计扩展上取得了显著进展，但存在以下边界条件：

- **单点查询效率低。** 每次查询隐函数值或方差都需要一次全局泊松求解，相比其他GPIS方法降低了单点查询效率，更适合批量查询场景。
- **依赖带朝向点云。** 与原始PSR一致，SPSR要求输入带朝向的点云；对于无朝向点云需要额外预处理。
- **协方差计算开销。** 虽然通过特征投影缓解，但在精度、内存和运行时间之间仍存在权衡。
- **未扩展到Screened PSR。** 方法基于Kazhdan等人2006版PSR，未能直接扩展到结合了向量场插值和泊松求解的Screened PSR（Kazhdan and Hoppe, 2013），后者在鲁棒性上更优。
- **协方差合并的偏差风险。** 虽然在多种渐近情况下误差有界且正确，但在某些极端采样分布下可能引入额外偏差。

### 7. 实验公平性说明

SPSR的输入要求与原始PSR完全相同（带朝向点云），未引入额外数据偏见。算法支持自适应网格离散化（Fig. 16展示了在四叉树自适应网格上的统计查询），正交于具体网格选择。所有统计查询均基于高斯过程理论推导，未针对特定对象或领域调优。

![[assets/figures/papers/paper_list_l90_https_www_dgp_toronto_edu_projects_stochastic_psr/figures/018_Figure_18.jpg]]
*Figure 18: Taking inspiration from Figs. 6 and 7 in [Martens et al. 2016], we show the result of reconstructing an apple and a car from a partial scan. PSR fails to produce even a closed surface, as does our vanilla SPSR, albeit also providing variance information signaling the less confident regions. When combined with a task-specific simple primitive (spherical or ellipsoidal) prior, SPSR provides a significantly better reconstruction*

## 定位与知识库关联

### 相对已有方法的本质差异

本文提出的 **Stochastic Poisson Surface Reconstruction (SPSR)** 相对于传统 **Poisson Surface Reconstruction (PSR)**（Kazhdan et al., 2006）的核心改变在于**输出形式的根本性升级**：将PSR输出的单一确定性隐函数 $f(x)$ 替换为一个完整的高斯过程概率分布 $\mathcal{N}(f_{\text{SPSR}}(x), \sigma^2(x))$。这一改变并非简单的后处理或附加模块，而是通过重新解释PSR的数学结构实现的范式转换。

具体而言，改变的**关键slot**是**协方差函数的定义与使用**：
- **PSR** 使用非对称的半协方差 $k_{\text{PSR}}(x,y) = \sigma_g \sum_{o \in B(x)} \alpha_{o,x} F_o(y)$ 进行向量场插值，该函数仅服务于确定性重建，不具备概率解释所需的对称正定性。
- **SPSR** 将其对称化为 $k_{\text{SPSR}}(x,y) = \frac{1}{2}(k_{\text{PSR}}(x,y) + k_{\text{PSR}}(y,x))$，从而获得合法的正定协方差函数，使高斯过程框架得以成立。这一修改在数值上极其微小（差异小于2%，见 Fig. 8），但使得整个数学框架从确定性插值跃迁为概率推断。

第二个改变的**关键slot**是**训练数据协方差矩阵的处理**：
- **完整GP** 需要求解 $\mathbf{K}_3^{-1}$，计算代价高昂。
- **SPSR** 引入**协方差合并（covariance lumping）**策略，将对角块矩阵 $\mathbf{D} = \text{diag}(\sigma_g w)$ 近似替代 $\mathbf{K}_3$，其中每个样本被视为独立，但其方差反比于局部采样密度。这一近似保持了幅度不变性（见 Fig. 9），避免了矩阵求逆，且具有正确的渐近行为（Fig. 27）。

第三个改变的**关键slot**是**隐函数协方差的计算方式**：通过拉普拉斯特征函数谱分解近似 $\mathbf{K}_f$，仅需计算对角项（或部分行/列）即可支持大多数统计查询，大幅降低了计算开销。

### 知识库挂载点

SPSR 在知识库中的定位是**隐式表面重建的统计扩展**，其挂载点可从以下几个维度理解：

1. **泊松重建谱系**：SPSR 直接继承自 Kazhdan et al. (2006) 的 PSR 框架，保留了其核心优势——对噪声的鲁棒性、对非均匀采样的适应性、以及通过全局泊松方程求解获得水密表面的能力。SPSR 可以视为在该谱系上的“统计增强版”，所有PSR的几何特性在SPSR的均值输出中得以保留。

2. **高斯过程隐式表面（GPIS）谱系**：与 Williams and Fitzgibbon (2006) 等将GP直接应用于隐函数建模的方法不同，SPSR 采用了一种独特的**两级GP架构**：先在局部对向量场 $\nabla f(x)$ 建立GP，再通过全局泊松求解将分布传递到隐函数 $f(x)$。这种“局部GP + 全局PDE”的设计使得SPSR既保留了GP的概率表达能力，又继承了PSR的全局一致性和水密性，这是其他GPIS方法（如 Martens et al., 2016）所不具备的。

3. **不确定性量化谱系**：与 Pauly et al. (2004) 使用表面平滑先验量化重建不确定性的方法相比，SPSR 使用的是**实体平滑先验**（solid smoothness prior），能够输出完整的空间概率分布，而非仅表面量。这使得SPSR可以回答“某点在物体内部的概率是多少”这类体积查询，而不仅仅局限于表面不确定性。

### 适用边界

SPSR 的适用边界由以下条件界定：

- **输入要求**：与PSR相同，要求带朝向的点云作为输入。对于无朝向点云，需要预处理步骤，该方法本身不解决法向估计问题。
- **查询模式**：每次查询隐函数值或方差都需要一次全局泊松求解，这使得单点查询效率低于某些GPIS方法。SPSR更适合**批量查询**场景（如对整个体积网格进行概率评估），而非交互式单点查询。
- **当前版本限制**：方法基于 Kazhdan et al. (2006) 的经典PSR，尚未扩展到 **Screened PSR**（Kazhdan and Hoppe, 2013）。后者结合了向量场插值与泊松求解以提高鲁棒性，SPSR目前无法直接受益于这些改进。
- **协方差合并的近似性**：虽然协方差合并在大多数场景下误差有界且渐近正确，但在极端采样分布下可能引入额外偏差。这一近似策略在精度、内存和运行时间之间存在权衡。

### 后续启发与延伸价值

SPSR 为后续研究提供了多个可扩展的方向：

1. **向Screened PSR的扩展**：将SPSR的统计框架与Screened PSR的梯度观测机制结合，有望同时获得概率输出和更强的鲁棒性。这需要解决如何将梯度观测融入高斯过程的技术问题。

2. **协方差合并技术的推广**：协方差合并作为一种避免测试时矩阵求逆的策略，可能推广到更广泛的高斯过程应用中。其核心思想——用采样密度加权的对角矩阵近似完整协方差——为大规模GP的近似推断提供了新的思路。

3. **自适应计算资源分配**：SPSR输出的空间不确定度分布可以指导自适应网格细化——在高不确定度区域使用更细的离散化，在确定区域使用更粗的网格，从而更有效地分配计算资源。

4. **任务相关先验的融合**：论文已展示了简单几何先验（球面、椭球面）对部分扫描重建的显著改善（Fig. 18, Fig. 19）。更复杂的先验（如来自深度网络的形状先验）可以自然地融入SPSR的高斯过程框架，为概率形状补全和重建提供统一的形式化基础。

5. **高级形状分析任务**：SPSR的概率框架为概率分割、形状匹配、不确定性感知的碰撞检测等任务提供了基础。特别是联合区域概率的计算能力（Fig. 12），使得对形状的全局统计推断成为可能，这超越了传统确定性重建方法的能力边界。

## 原文 PDF

![[paperPDFs/SIGGRAPH_ASIA_2022/Stochastic_Poisson_Surface_Reconstruction.pdf]]