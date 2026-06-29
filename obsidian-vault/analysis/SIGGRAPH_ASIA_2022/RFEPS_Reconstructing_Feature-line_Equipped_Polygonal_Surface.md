---
title: "RFEPS: Reconstructing Feature-line Equipped Polygonal Surface"
type: paper
paper_level: A
venue: SIGGRAPH ASIA
year: 2022
pdf_ref: paperPDFs/SIGGRAPH_ASIA_2022/RFEPS_Reconstructing_Feature_line_Equipped_Polygonal_Surface.pdf
project_link: null
code_link: "https://github.com/Xrvitd/RFEPS"
aliases:
- RFEPS
tags:
- SIGGRAPH_ASIA_2022
- topic/graphics_geometry_processing
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
- topic/representation_self_supervised_transfer
core_operator: 通过离散最优传输检测边缘区域并生成额外边缘点，同时在限制功率图中为边缘点分配较高权重，从而强制定向边缘连接。
primary_logic: 基于局部平面性假设，利用最优传输度量识别边缘区域，并通过限制功率图赋予边缘点更高优先级，以实现特征线对齐的表面重建。
claims:
- Our method achieves lower OCD and OECD across all noise levels compared to RIMLS, EAR, EC-Net, Dis-PU, and MFLE.
- The RPD better preserves feature lines than the RVD for surface reconstruction.
- The whole pipeline of RFEPS surpasses other methods in terms of reconstruction fidelity and manifoldness.
- Setting larger weight for edge points (8δ²) is crucial for feature-line alignment.
---

# RFEPS: Reconstructing Feature-line Equipped Polygonal Surface

> [!tip] 核心洞察
> 基于局部平面性假设，利用最优传输度量识别边缘区域，并通过限制功率图赋予边缘点更高优先级，以实现特征线对齐的表面重建。

| 字段 | 内容 |
|------|------|
| 中文题名 | RFEPS：带特征线的多边形表面重建 |
| 英文题名 | RFEPS: Reconstructing Feature-line Equipped Polygonal Surface |
| 会议/期刊 | SIGGRAPH ASIA 2022 |
| Links | [paper](https://xrvitd.github.io/Projects/RFEPS/index.html) · [Code](https://github.com/Xrvitd/RFEPS) |
| Topic | #topic/graphics_geometry_processing #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction #topic/representation_self_supervised_transfer |
| Method | RFEPS |
| Dataset | Point Cloud Consolidation, Surface Reconstruction Quality, Runtime Efficiency |

> [!tip] 效果简介
> - Point Cloud Consolidation (Table 1, various noise levels on synthetic CAD model... 上，OCD (x10^4) 0.084 (no-noise), 0.140 (0.25%), 0.316 (0.5%), 0.572 (1.0%) vs RIMLS (best baseline): 0.098 (no-noise), others higher (consistently lower)。
> - Point Cloud Consolidation (Table 1, various noise levels) 上，OECD (x10^4) 0.079 (no-noise), 0.102 (0.25%), 0.122 (0.5%), 0.140 (1.0%) vs RIMLS (best baseline): higher values (consistently lower)。
> - Surface Reconstruction Quality (Table 2, combinations of consolidation and reco... 上，ECD (Edge Chamfer Distance) and EF1 (Edge F1-score) best scores in ECD and EF1 (RFEPS pipeline) vs all other consolidation + reconstruction combinations (significant improvement)。

## 概要

从噪声点云重建带清晰特征线的多边形表面是几何处理中的难题，核心瓶颈在于：噪声破坏了边缘处点的精确位置，且现有网格化方法未优先连接边缘点，导致特征线模糊或断裂。本文提出 **RFEPS**，通过**离散最优传输**检测边缘区域并生成额外边缘点，再在**限制功率图**中为边缘点赋予更高权重，强制网格沿特征线对齐。整个流程包括联合去噪与法线初始化、边缘区识别、法线正则化、点位置微调、边缘点生成，以及基于限制功率图的多边形表面提取。实验表明，RFEPS 在不同噪声水平下的点云整合（OCD/OECD）和表面重建质量（ECD/EF1）上均优于 RIMLS、EAR、EC-Net 等基线方法，且限制功率图相比限制 Voronoi 图能更有效地保持特征线。该方法适用于二面角在 [π/6, 5π/6] 范围内的 CAD 类模型，对法线不一致性具有较强鲁棒性。

## 核心方法与创新机理

### 1. 问题背景与唯一瓶颈

从噪声点云重建带特征线的多边形表面面临一个核心瓶颈：**输入点云中缺少精确位于几何边缘的点**，且现有方法在网格生成阶段无法优先连接边缘点以形成清晰的特征线。传统点云重建方法（如EAR、EC-Net等）虽然能增强点密度，但增强点往往散布在边缘区域附近，分布不规则，难以产生平直光滑的特征线。RFEPS的因果旋钮在于：通过**离散最优传输检测边缘区域并生成精确的边缘点**，同时在**限制功率图中为边缘点分配较高权重**，从而强制网格连接对齐几何特征线。

### 2. 核心洞察与创新机理

RFEPS的核心洞察基于一个关键假设：**CAD类型点云在局部具有平面性**。基于此，算法通过以下机制实现特征线对齐的表面重建：

- **最优传输度量识别边缘区域**：将点邻域法线分布建模为源分布，目标分布设为两个Dirac delta函数（代表边缘两侧平面的法线）。当某点的邻域法线需要以高成本运输到两个分离的目标法线时，该点即被判定位于边缘区域。这一机制有效量化了“偏离完美几何边缘”的程度。
- **限制功率图赋予边缘点更高优先级**：在泊松重建的基础上计算限制功率图（RPD），为边缘点分配权重 $8\delta^2$，非边缘点权重为0。这使得边缘点在网格连接推断中获得更高优先级，强制生成的三角网格边对齐特征线。

### 3. Changed Slots：相对于基线的关键改进

**Slot 1：边缘点生成（基线：无专门边缘点生成或不精确方法）**
- **基线缺陷**：EAR等方法虽能增加边缘区域点密度，但增强点分布不规则，无法形成平直特征线（见Figure 10）。
- **RFEPS方案**：基于离散最优传输检测边缘区后，通过投影优化将每个边缘区点投影到潜在特征线上，生成精确位于边缘的额外点。投影公式为：
  $$\min_{\boldsymbol{z}_i} \sum_{p_j \in \mathrm{Neigh}(p_i)} ((\boldsymbol{z}_i - \boldsymbol{p}_j) \cdot \mathbf{n}_j)^2 + \mu \|\boldsymbol{z}_i - \boldsymbol{p}_i\|^2$$
  其中第一项强制新点 $\boldsymbol{z}_i$ 满足邻域点的平面约束，第二项防止过度漂移（由参数 $\mu$ 控制）。

**Slot 2：表面重建中的边缘点权重（基线：所有点权重相同）**
- **基线缺陷**：传统Voronoi图（RVD）对所有点赋予相同重要性，边缘点密度不足时无法形成对齐特征线的连接（见Figure 6(a,b)）。
- **RFEPS方案**：在限制功率图中为边缘点分配权重 $8\delta^2$，非边缘点权重为0。功率图通过权重调节各点的影响范围，边缘点的高权重使其“拉拢”更多连接，从而在RPD对偶提取的三角网格中自然对齐特征线（见Figure 6(c,d)和Figure 8的消融验证）。

**Slot 3：去噪与法线初始化（基线：单独去噪或法线估计不可靠）**
- **基线缺陷**：传统方法将去噪和法线估计分离，难以在噪声下获得可靠法线。
- **RFEPS方案**：联合优化点位置和法线，基于局部平面性假设。目标函数为：
  $$\min_{\{\epsilon_i\},\{\mathbf{n}_i\}} \left\{ \sum_{i=1}^n \| M_{3\times3}^i \mathbf{n}_i \|^2 + \xi \sum_{i=1}^n \epsilon_i^2 \right\}$$
  其中 $M_{3\times3}^i$ 是点 $p_i$ 的协方差矩阵，$\epsilon_i$ 是点沿法线方向的位移。第一项最小化法线与协方差矩阵零空间的偏差（即强制局部平面性），第二项惩罚点位移以保持保真度，参数 $\xi$ 平衡去噪程度。

### 4. 方法框架与模块顺序

RFEPS的完整流程包含7个模块，按顺序执行，模块间存在严格因果依赖：

**Step 1：联合去噪与法线初始化（Section 3.1）**
- **输入**：含噪声的点云（无可靠法线）
- **操作**：基于局部平面性假设，联合优化点位置 $\epsilon_i$ 和法线 $\mathbf{n}_i$。协方差矩阵 $M_{3\times3}^i$ 由邻域球（半径 $r=2\delta$）内的点计算，优化目标使法线尽可能落在协方差矩阵的零空间中。
- **输出**：去噪后的点云及初始法线估计
- **因果链接**：为Step 2提供可靠的法线分布，是边缘检测的基础

**Step 2：基于最优传输的边缘区域识别（Section 3.2）**
- **输入**：Step 1的法线估计
- **操作**：对每个点 $p_i$，将其邻域法线分布 $\mu_s$ 运输到两个Dirac delta函数 $\mu_t$（代表两个代表法线 $\hat{\mathbf{n}}_1, \hat{\mathbf{n}}_2$）。优化问题为：
  $$\min_{\{\lambda_j\}, \hat{\mathbf{n}}_1, \hat{\mathbf{n}}_2} \sum_{p_j \in \mathrm{Neigh}(p_i)} \left\{ \lambda_j \|\mathbf{n}_j - \hat{\mathbf{n}}_1\|^2 + (1-\lambda_j) \|\mathbf{n}_j - \hat{\mathbf{n}}_2\|^2 \right\}$$
  约束条件：$\sum \lambda_j = k/2$（假设两簇数量相等），$\|\hat{\mathbf{n}}_1\| = \|\hat{\mathbf{n}}_2\| = 1$。运输成本高且两代表法线夹角大的点被标记为边缘区点（见Figure 5的验证）。
- **输出**：边缘区域点集标记
- **因果链接**：为Step 3-5提供边缘区域定位，决定后续处理的焦点

**Step 3：边缘区法线正则化（Section 3.3）**
- **输入**：Step 2的边缘标记 + Step 1的法线
- **操作**：对边缘区点，引入自适应加权方案处理不均匀点分布，将法线聚类为两簇或三簇（三簇用于角点等复杂边缘）。加权聚类目标为：
  $$\min_{\{\lambda_j^{(d)}\}, \hat{\mathbf{n}}_d} \sum_{p_j \in \mathrm{Neigh}(p_i)} \frac{\lambda_j^{(1)}\rho_1 + \lambda_j^{(2)}\rho_2 + \lambda_j^{(3)}\rho_3}{\|p_i - p_j\|^2 + \epsilon}$$
  其中 $\rho_d = \|\mathbf{n}_j - \hat{\mathbf{n}}_d\|^2$，权重反比于点间距，使近邻点对法线聚类贡献更大。
- **输出**：正则化后的边缘区法线
- **因果链接**：提高边缘附近法线一致性，为Step 4-5提供更可靠的法线引导

**Step 4：点位置微调（Section 3.3）**
- **输入**：Step 3的正则化法线
- **操作**：仅使用法线相似的邻域点（$\mathrm{Neigh}'(p_i)$）微调点位置，优化目标为：
  $$\min_{\{\epsilon_i\}} \sum_{i=1}^n \sum_{p_j \in \mathrm{Neigh}'(p_i)} \|M_{3\times3}^{ij} \mathbf{n}_i\|^2$$
  使点位置适配正则化后的法线。
- **输出**：微调后的点位置
- **因果链接**：为Step 5提供更准确的基础点位置

**Step 5：边缘点预测（Section 3.3）**
- **输入**：Step 4的微调点 + Step 3的正则化法线
- **操作**：对边缘区每个点，通过投影优化生成精确位于潜在特征线上的新点 $\boldsymbol{z}_i$（公式见Slot 1），参数 $\mu$ 控制漂移程度。
- **输出**：增强点集（原始点 + 边缘点，边缘点标记为红色，见Figure 1(c)和Figure 3(f)）
- **因果链接**：为Step 6提供带权重的增强点集

**Step 6：基于泊松重建的限制功率图计算（Section 3.4）**
- **输入**：Step 5的增强点集 + 泊松重建的基础表面
- **操作**：在筛选泊松重建表面上计算限制功率图（RPD），边缘点权重设为 $8\delta^2$，非边缘点权重为0。功率图通过权重调节各点的影响范围（见Figure 6(c)的2D示例）。
- **输出**：限制功率图分解
- **因果链接**：为Step 7提供对偶提取的基础

**Step 7：对偶提取生成多边形网格（Section 3.4）**
- **输入**：Step 6的RPD
- **操作**：提取RPD的对偶，生成插值增强点集的三角网格。由于边缘点的高权重，网格边自然对齐特征线（见Figure 7和Figure 8）。
- **输出**：最终带特征线的多边形表面

### 5. 关键公式变量含义与因果关系

- **协方差矩阵 $M_{3\times3}^i$**：度量点 $p_i$ 邻域的局部平面性，其零空间对应理想法线方向。Step 1通过最小化 $\|M_{3\times3}^i \mathbf{n}_i\|^2$ 强制法线与该零空间对齐。
- **运输成本与 $\lambda_j$**：$\lambda_j$ 是二元分配变量（0或1），指示邻域点 $p_j$ 的法线属于哪个簇。运输成本高意味着邻域法线分布呈现明显的双峰结构（即存在边缘），这是边缘检测的核心判据（见Figure 5的验证：运输成本在边缘处达到峰值）。
- **自适应权重 $\frac{1}{\|p_i - p_j\|^2 + \epsilon}$**：处理点分布不均匀问题，使距离 $p_i$ 更近的点对法线聚类贡献更大，提高边缘区法线正则化的鲁棒性。
- **边缘点权重 $8\delta^2$**：$\delta$ 为点云平均采样间距。该权重值通过实验确定为关键参数（见Figure 6和Section 3.4的讨论），赋予边缘点在RPD中足够的影响力以强制特征线对齐。
- **参数 $\xi, r, \mu$**：分别控制去噪程度、边缘区域宽度和边缘点投影漂移程度。参数研究（Table 4, Figure 15）表明这些参数在合理范围内鲁棒，但极端值会导致过度平滑（$\xi$过大）、边缘区过宽（$r$过大）或边缘点偏离（$\mu$过小）。

### 6. 训练/推理路径

RFEPS是一个**无需训练的几何优化方法**，所有步骤均通过数值优化求解。推理路径为端到端的7步流程，无需GPU加速，总运行时间约9.53秒（50K点，见Table 3），与现有方法相当或更快（见Figure 14）。关键计算瓶颈在最优传输的边缘区域识别（Step 2）和限制功率图计算（Step 6），但整体效率可接受。

![[assets/figures/papers/paper_list_l80_https_xrvitd_github_io_Projects_RFEPS_index_html/figures/003_Figure_3.jpg]]
*Figure 3: The pipeline of the proposed method. (a) The noisy input point cloud. (b) The denoised result by optimizing point locations and normal vectors simultaneously. (c) The edge zone detected by a discrete optimal transport formulation. (d) The normal vectors of the points in the edge zone are regularized. (e) The point locations are fine-tuned to adapt to the regularized normal vectors. (f ) Points in the edge zone are projected, point by point, onto the potential edge such that there are sufficiently many additional edge points (colored in red). (g) The restricted power diagram (RPD) on the base surface produced by the Poisson reconstruction solver. (h) The dual of the RPD reports the final rec...*

![[assets/figures/papers/paper_list_l80_https_xrvitd_github_io_Projects_RFEPS_index_html/figures/014_Figure_13.jpg]]
*Figure 13: More reconstruction results produced by our algorithm pipeline*

![[assets/figures/papers/paper_list_l80_https_xrvitd_github_io_Projects_RFEPS_index_html/figures/001_Figure_1.jpg]]
*Figure 1: Reconstructing a polygonal surface with clean line-type features from a noisy point cloud. From left to right: (a) The input point cloud is noisy and does not have reliable normal information. (b) The point locations and normal vectors are optimized simultaneously such that the resulting point cloud is as locally planar as possible (the normal vectors of the denoised point cloud are visualized in a color-coded style). (c) We augment the point set by predicting more points that are deemed to be located on potential geometry edges; See the points colored in red. (d) Based on a power-diagram decomposition restricted on the base surface (obtained by Poisson reconstruction), the resulting polygo...*

## 实验与关键发现

### 主结果：点云固结与表面重建的双重优势

RFEPS在点云固结（point consolidation）任务上，于合成CAD模型的不同噪声水平下，均取得最低的OCD（整体倒角距离）和OECD（整体边缘倒角距离）。Table 1汇总了与RIMLS、EAR、EC-Net、Dis-PU、MFLE等方法的定量对比：在无噪声条件下，RFEPS的OCD为0.084（×10⁴），OECD为0.079（×10⁴）；在1.0%噪声水平下，OCD为0.572，OECD为0.140。相较于表现最好的基线方法RIMLS，RFEPS在所有噪声水平上均保持更低的重建误差，且优势随噪声增大而更加显著。这一结果验证了联合去噪与法线初始化、最优传输边缘区识别、边缘点生成这一整套固结管线对噪声点云的有效性。

在表面重建质量评估中，Table 2报告了不同固结方法与重建方法组合下的ECD（边缘倒角距离）和EF1（边缘F1分数）。RFEPS完整管线（RFEPS固结 + RPD表面重建）在两项指标上均取得最优分数，显著优于其他固结+重建组合。Figure 11的定性对比进一步表明，RFEPS管线在重建保真度和流形性（manifoldness）上均超越现有方法，尤其在特征线对齐方面表现出明显优势。

### 关键消融：RPD赋予边缘点高权重的决定性作用

**RPD vs. RVD。** Figure 8的对比消融直接展示了限制功率图（RPD）相较于限制沃罗诺伊图（RVD）在特征线保持上的优势。在相同的增强点集上，RVD由于对所有点赋予同等重要性，导致三角剖分无法沿特征线对齐连接；而RPD通过为边缘点分配较高权重（8δ²），使边缘点在连接推断中获得更高优先级，从而生成与几何边缘自然对齐的网格。这一消融确立了RPD作为表面重建核心模块的必要性。

**边缘点权重的关键取值。** Section 3.4和Figure 6从二维示例出发解释了功率图机制：当边缘点被赋予权重8δ²（非边缘点权重为零）时，其对偶三角剖分能够强制沿特征线方向连接。该权重值并非任意选择，而是通过实验验证的关键参数——过小的权重无法有效引导边缘对齐，过大的权重则可能导致网格畸变。

**最优传输 vs. k-means。** Figure 16对比了基于离散最优传输的边缘区识别与基于k-means的替代方案。结果表明，最优传输公式（Equation 7）能够更精确地检测边缘区域，进而生成更高保真度的特征线。这归因于最优传输在度量法线分布差异时，天然考虑了分布间的几何距离，而k-means仅进行硬聚类，缺乏对边缘区域连续过渡的建模能力。

**参数敏感性。** Table 4和Figure 15系统研究了三个关键参数的影响：ξ控制去噪程度——过小则噪声残留，过大则几何细节被平滑；邻域半径r决定特征线区域的宽度——过窄则遗漏边缘点，过宽则引入非边缘区域干扰；μ约束边缘点漂移——过小则边缘点无法精确投影到特征线上，过大则边缘点过度偏离原始位置。实验表明，这些参数在合理范围内具有较好的稳定性，但针对不同噪声水平和几何复杂度的输入仍需适当调整。

### 效率与适用边界

Table 3报告了RFEPS在50K点规模下的运行时间：总耗时约9.53秒，与现有方法相当或更快。Figure 14进一步展示了不同规模点云下的时间增长趋势，表明该方法在效率上具备实用性。

然而，RFEPS的核心假设——CAD模型表面的局部平面性——也构成了其主要适用边界。Figure 24揭示，对于需要表面平滑化的自由曲面模型，基于平面性假设的固结策略无法像点云上采样算法那样有效提升平滑度。当输入点云稀疏（如5K点）时，增强后的点集和重建结果仍保留明显的平面化特征，而非光滑曲面。这一限制源于方法设计本身：联合去噪与法线初始化的目标函数（Equation 2）本质上是使点云尽可能符合局部平面性，这与光滑曲面的需求存在内在冲突。因此，RFEPS更适用于以平面和尖锐棱边为特征的CAD/机械零件类模型，而非有机形态或自由曲面物体。

此外，Section 5报告了法线扰动实验：在法线上添加白噪声扰动（Equation: n = (n + τ n_rand) / ||n + τ n_rand||）后，方法仍能保持一定的鲁棒性，但过大的扰动将导致边缘区识别失效。这表明方法对法线质量的依赖程度较高——初始法线估计的准确性直接影响后续边缘区检测和边缘点生成的质量。

![[assets/figures/papers/paper_list_l80_https_xrvitd_github_io_Projects_RFEPS_index_html/figures/009_Table_1.jpg]]
*Table 1: Evaluating various point consolidation approaches for point cloud inputs with varying levels of noise*

![[assets/figures/papers/paper_list_l80_https_xrvitd_github_io_Projects_RFEPS_index_html/figures/006_Figure_6.jpg]]
*Figure 6: A 2D example for explaining why the power diagram helps preserve feature lines, where the points colored in red can be viewed as edge points. (a) The Voronoi diagram takes each site with equal importance. (b) The resulting triangulation (dual of (a)) fails to align the connections with the potential feature line due to the insufficient density of edge points. (c) By using the power diagram, one increases the influence of edge points. (d) The edge points are given higher priority when inferring the connections between points, making the resulting triangulation (dual of (c)) feature-line aligned*

![[assets/figures/papers/paper_list_l80_https_xrvitd_github_io_Projects_RFEPS_index_html/figures/008_Figure_8.jpg]]
*Figure 8: The close-up window shows that the RPD is better at preserving feature lines than the RVD for surface reconstruction*

## 定位与知识库关联

RFEPS 针对的核心问题是 **从噪声点云重建带特征线的多边形表面**。已有方法面临的瓶颈在于：噪声点云中缺少精确位于几何边缘的点，且传统网格重建方法（如泊松重建、Voronoi 图对偶）在生成网格时无法优先连接边缘点以形成清晰的特征线。RFEPS 通过两个关键 slot 的改变解决了这一问题，并由此在知识库中建立了明确的挂载点。

### 相对已有方法的本质差异

**Slot 1：边缘点的生成策略。** 已有方法要么不专门生成边缘点（如 RIMLS、Dis-PU），要么生成方式不精确。例如 **EAR**（Huang et al., 2013）虽然能通过边缘感知的点增强在边缘区域增加点密度，但其非正则化的点分布难以形成平直光滑的特征线（见图 10 的定性对比）。EC-Net（Yu et al., 2018）等基于学习的方法需要大量训练数据，且泛化到新几何拓扑时表现不稳定。RFEPS 的改变在于：基于离散最优传输（optimal mass transport）度量局部法线分布与理想几何边缘的偏差，精确识别边缘区域，然后通过投影优化（公式 11）将边缘区内的点逐个投影到潜在特征线上，生成精确位于边缘的额外点。这一 slot 的因果机制是 **“检测→投影”**，而非简单的密度增强或学习式预测。

**Slot 2：表面重建中边缘点的权重分配。** 传统方法在网格重建时对所有点赋予相同权重。例如，基于受限 Voronoi 图（RVD）的方法将每个站点视为同等重要，导致边缘连接被周围非边缘点“稀释”，无法对齐特征线（见图 8 的消融对比）。RFEPS 引入受限功率图（RPD），并为边缘点分配较高的权重（$8\delta^2$），而非边缘点权重为零。这一权重差异赋予了边缘点在推断点间连接时更高的优先级，强制网格边沿特征线对齐。因果链为：**边缘点高权重 → RPD 中边缘点支配更大区域 → 对偶网格边优先连接边缘点 → 特征线对齐**。图 6 的 2D 示例直观展示了这一机制：Voronoi 图（权重相等）的对偶三角剖分无法对齐特征线，而功率图（边缘点高权重）的对偶则成功对齐。

### 知识库挂载点

RFEPS 可挂载到以下知识库节点：

1. **点云去噪与法线估计联合优化**：RFEPS 的 Step 1（公式 2）基于局部平面性假设，联合优化点位置和法线向量，最小化协方差矩阵与法线的偏差并惩罚点位移。这与此前将去噪和法线估计分离处理的方法（如 RIMLS）形成对比，可挂载到“点云预处理”节点下，作为“联合优化”子类。

2. **离散最优传输用于几何特征检测**：RFEPS 将最优传输理论（公式 3-7）引入点云边缘检测，通过测量局部法线分布与双狄拉克分布的传输成本来识别边缘区域。这为“最优传输在几何处理中的应用”节点提供了新的实例，与基于曲率或学习的方法形成互补。

3. **受限功率图用于特征保持的表面重建**：RFEPS 证明了 RPD（而非 RVD）配合差异化权重可以有效保持特征线。这直接挂载到“基于 Voronoi/功率图的网格重建”节点下，作为“特征保持”子类，补充了 **Basselin et al. 2021** 提出的 RPD 框架的应用场景。

### 适用边界与后续启发

**适用边界：** RFEPS 的设计假设输入点云来自 CAD 类模型，即表面主要由平面片和尖锐特征线构成。对于有机形状或光滑曲面，边缘点生成和权重分配机制可能引入伪影（见 Section 5 的局限性讨论）。此外，方法对法线质量敏感：当法线受到严重噪声扰动时（公式中 $\tau$ 参数控制的白噪声），边缘检测的可靠性下降。参数 $\xi$（去噪程度）、$r$（边缘区宽度）和 $\mu$（边缘点漂移控制）需要根据噪声水平和几何尺度调整（见表 4 的参数研究），缺乏完全自适应的机制。

**后续启发：**
- **学习式边缘检测与最优传输的混合**：RFEPS 的边缘检测完全基于几何优化，未来可探索将数据驱动的边缘先验与最优传输度量结合，提高在严重噪声或非理想 CAD 模型上的鲁棒性。
- **权重自适应性**：当前边缘点权重 $8\delta^2$ 是固定值，后续可研究基于局部几何特征（如二面角大小、边缘锐度）自适应调整权重，以处理不同尖锐程度的特征。
- **扩展到非 CAD 场景**：将“边缘点生成 + 差异化权重”的思想推广到有机形状的脊线、谷线检测，需要重新定义“边缘”的数学表征（例如基于主曲率的传输成本），而非当前的局部平面性假设。
- **与其他重建管线的集成**：RFEPS 的 RPD 重建基于泊松重建的基础表面，后续可探索将边缘点权重机制集成到其他隐式表面重建方法（如神经隐式场）中，实现端到端的特征保持重建。

### 需手动验证的声明

分析中指出 RFEPS 在 OCD 和 OECD 指标上全面优于 RIMLS、EAR、EC-Net、Dis-PU 和 MFLE（Table 1），且完整管线在表面重建保真度和流形性上超越其他组合（Table 2, Figure 11）。这些结论基于合成 CAD 数据集和特定噪声模型，其在真实扫描数据上的泛化性能需通过额外实验验证。此外，与 MFLE 等特征线提取方法的对比仅涉及点云层面的指标，未直接比较提取的特征线质量，该对比的公平性需人工确认。

## 原文 PDF

![[paperPDFs/SIGGRAPH_ASIA_2022/RFEPS_Reconstructing_Feature_line_Equipped_Polygonal_Surface.pdf]]