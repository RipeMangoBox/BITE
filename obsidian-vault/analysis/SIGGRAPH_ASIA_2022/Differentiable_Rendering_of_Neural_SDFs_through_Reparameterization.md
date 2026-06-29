---
title: Differentiable Rendering of Neural SDFs through Reparameterization
type: paper
paper_level: A
venue: SIGGRAPH ASIA
year: 2022
pdf_ref: paperPDFs/SIGGRAPH_ASIA_2022/Differentiable_Rendering_of_Neural_SDFs_through_Reparameterization.pdf
project_link: null
code_link: null
aliases:
- DRBDSR
- DRNSTR
tags:
- SIGGRAPH_ASIA_2022
- topic/graphics_geometry_processing
- topic/graphics_rendering_materials
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
core_operator: 采用盒式滤波器并显式通过边界积分处理像素滤波器边界，同时对球追踪采样点使用基于SDF和距离的加权重参数化（w^q），以将权重集中在实际表面附近，减少方差。
primary_logic: 将像素滤波器边界视为显式边界条件，利用散度定理将外部区域积分转换为边界积分，同时设计一种基于SDF值和梯度方向的加权方案，使得在理论上边界一致性成立且权重集中于表面点，从而在保持低偏差的同时显著降低梯度方差。
claims:
- 采用盒式滤波器并显式处理像素边界积分，消除了使用高斯滤波器引起的内部区域额外方差。
- 消融实验表明权重指数γ=3时重建质量最优，γ≥6时经常不收敛，验证了加权方案对收敛的关键作用。
- 理论证明在理想的C1连续SDF和球追踪器下，权重w^q满足边界一致性，即接近轮廓线时权重全部集中于极限表面点。
- 将像素滤波器边界视为显式边界条件，利用散度定理将外部区域积分转换为边界积分，同时设计一种基于SDF值和梯度方向的加权方案，使得在理论上边界一致性成立且权重集中于表面点，从而在保持低偏差的同时显著降低梯度方差。
---

# Differentiable Rendering of Neural SDFs through Reparameterization

> [!tip] 核心洞察
> 将像素滤波器边界视为显式边界条件，利用散度定理将外部区域积分转换为边界积分，同时设计一种基于SDF值和梯度方向的加权方案，使得在理论上边界一致性成立且权重集中于表面点，从而在保持低偏差的同时显著降低梯度方差。

| 字段 | 内容 |
|------|------|
| 中文题名 | 通过重参数化的神经符号距离场可微渲染 |
| 英文题名 | Differentiable Rendering of Neural SDFs through Reparameterization |
| 会议/期刊 | SIGGRAPH ASIA 2022 |
| Links | [paper](https://people.csail.mit.edu/sbangaru/projects/dsdf-2022/index.html) |
| Topic | #topic/graphics_geometry_processing #topic/graphics_rendering_materials #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction |
| Method | DSDF (Reparameterization-based Differentiable SDF Rendering) |
| Dataset |  |

> [!tip] 效果简介
> - 消融实验表明权重指数γ=3时重建质量最优，γ≥6时经常不收敛，验证了加权方案对收敛的关键作用。
> - 理论证明在理想的C1连续SDF和球追踪器下，权重w^q满足边界一致性，即接近轮廓线时权重全部集中于极限表面点。

## 概要

现有基于高斯滤波器的神经SDF可微渲染方法为避免处理像素滤波器边界，采用无界高斯核，但滤波器权重的梯度在内部区域引入显著方差，导致优化不稳定，尤其在表面接近像素边界时更为严重。本文提出**DSDF**（基于重参数化的可微SDF渲染），核心思路是保留盒式滤波器，并显式通过**像素边界积分**消除边界不连续性：利用散度定理将外部区域积分转换为像素滤波器边界上的线积分，从而在保持低偏差的前提下消除高斯核带来的额外方差。同时，设计一种基于SDF值和梯度方向的**加权重参数化方案**（w^q），使采样点权重集中在实际表面附近，并结合top-k子集选择与权重偏移保证连续性。理论证明在理想C1连续SDF和球追踪器下，该权重方案满足边界一致性（轮廓线上权重完全集中于表面点）。消融实验表明，权重指数γ=3时重建质量最优，γ≥6时经常不收敛；top-k子集大小k<7时质量快速下降，k≥14后收益递减。本方法定位于基于球追踪的神经SDF逆向渲染管线，以盒式滤波器+边界积分替换高斯滤波器，以重参数化权重方案替换均匀或高斯权重，从根本上解决了高斯方法方差大的瓶颈。

## 核心方法与创新机理

### 问题瓶颈：高斯滤波器可微渲染的方差困境

在基于神经符号距离场（SDF）的可微渲染中，轮廓积分（silhouette integral）的梯度估计是核心难题。现有方法（如 **Bangaru et al. 2020** 和 **Loubet et al. 2019**）采用无界高斯滤波器来避免处理像素滤波器的边界，但这一策略引入了一个隐蔽的代价：高斯滤波器权重的导数在像素内部区域产生额外的梯度方差，导致优化过程不稳定，尤其当表面接近像素边界时，方差问题进一步恶化（见 Figure 1 左侧）。

![[assets/figures/papers/paper_list_l45_https_people_csail_mit_edu_sbangaru_projects_dsdf_2022_index_html/figures/002_Figure_1.jpg]]
*Figure 1: On the left, existing methods [Bangaru et al. 2020; Loubet et al. 2019] use an unbounded Gaussian filter to avoid the need to handle the boundary of the pixel filter*

问题的数学根源在于轮廓积分 $I_{\mathrm{sil}}$ 的定义域包含像素滤波器 $\mathcal{U}$ 及其外部区域。当使用盒式滤波器时，像素边界 $\mathcal{U}_{\mathrm{b}}$ 上的不连续性必须显式处理；而高斯滤波器通过无界支撑回避了边界问题，却将边界处的梯度扩散到了整个内部区域。

### 核心创新：盒式滤波器 + 边界积分 + 加权重参数化

本方法 **DSDF** 的核心思路是回归盒式滤波器，但通过两个关键机制消除边界不连续性并控制方差：

1. **显式边界积分处理**：利用散度定理将像素滤波器外部区域的面积积分转换为边界 $\mathcal{U}_{\mathrm{b}}$ 上的线积分，从而显式消除盒式滤波器带来的边界不一致。
2. **加权重参数化（$w^q$）**：设计一种基于 SDF 值和梯度方向的采样点加权方案，使权重集中在实际表面附近，大幅降低轮廓积分的蒙特卡洛估计方差。

### Changed Slots：相对于基线的关键替换

| 模块槽位 | 基线方法（高斯滤波器类） | 本方法（DSDF） | 因果作用 |
|---------|----------------------|---------------|---------|
| 像素滤波器类型 | 无界高斯滤波器 | 盒式滤波器 + 像素边界积分 | 消除高斯权重导数引入的内部方差 |
| 轮廓积分重参数化权重 | 基于高斯滤波器的权重（无界支撑）或均匀采样 | 基于 SDF 和距离的加权 $w^q$，结合 top-k 子集与最小权重偏移 | 将权重集中于表面点，降低估计方差并保证边界一致性 |

### 方法框架与模块顺序

DSDF 的渲染与梯度计算流程包含以下顺序模块：

#### 模块 1：轮廓积分的域拆分与边界积分转换

首先将轮廓积分 $I_{\mathrm{sil}}$ 拆分为像素内部区域 $\mathcal{U} \setminus \mathcal{U}_{\mathrm{sil}}$ 和外部区域 $(\mathcal{U}_{\infty} \setminus \mathcal{U}) \setminus \mathcal{U}_{\mathrm{b}}$ 两部分：

$$I_{\mathrm{sil}} = \int_{\mathcal{U} \setminus \mathcal{U}_{\mathrm{sil}}} \nabla \cdot (L \mathcal{V}) + \int_{(\mathcal{U}_{\infty} \setminus \mathcal{U}) \setminus \mathcal{U}_{\mathrm{b}}} \nabla \cdot (L \mathcal{V})$$

其中 $\mathcal{U}_{\mathrm{sil}}$ 为轮廓点集，$\mathcal{V}$ 为 warp 场，$L$ 为辐射度。利用散度定理，将外部区域积分转换为像素滤波器边界 $\mathcal{U}_{\mathrm{b}}$ 上的边界积分：

$$I_{\mathrm{sil}} = \int_{\mathcal{U} \setminus \mathcal{U}_{\mathrm{sil}}} \nabla \cdot (L \mathcal{V}) - \oint_{\mathcal{U}_{\mathrm{b}}} L (\mathcal{V} \cdot \mathbf{n}_b)$$

这一转换是方法的基础：内部区域积分可直接通过标准面积采样估计，而边界积分项显式处理了盒式滤波器的边界效应，避免了高斯滤波器方案中权重梯度扩散到整个内部区域的问题（Figure 1 右侧）。

#### 模块 2：球追踪采样点生成

沿视线方向 $\mathbf{u}$ 使用球追踪算法（sphere tracer）生成候选表面点序列 $\mathcal{T}(\mathbf{u}) = \{\mathbf{x}_1, \mathbf{x}_2, \ldots, \mathbf{x}_n\}$。球追踪利用 SDF 的距离信息自适应步进，使得采样点在接近表面时自然密集。

#### 模块 3：轮廓权重计算（$w^q$）——核心机制

对于球追踪生成的每个采样点 $\mathbf{x}_i$，定义加权重参数化权重 $w^q$：

$$w^q(\mathbf{x}_i) = \left( \sqrt{f(\mathbf{x}_i)^2 + \epsilon^2} - f(\mathbf{x}_i) + \lambda_d \cdot \frac{\epsilon}{\sqrt{f(\mathbf{x}_i)^2 + \epsilon^2}} \right)^{-\gamma} \cdot \left( \sqrt{f(\mathbf{x}_i)^2 + \epsilon^2} - f(\mathbf{x}_i) \right)$$

其中：
- $f(\mathbf{x})$ 为 SDF 值（表面处为 0，内部为负，外部为正）
- $\epsilon$ 为球追踪步长相关的小量
- $\gamma$ 为权重集中程度的指数参数（消融实验表明 $\gamma=3$ 最优）
- $\lambda_d$ 为方向相关调整参数

该权重的关键性质（Lemma 3.2）是：当采样点接近轮廓线 $\mathcal{U}_{\mathrm{sil}}$ 时，权重下界发散：

$$\lim_{\mathbf{u} \to \mathcal{U}_{\mathrm{sil}}} w^{q}(\mathbf{x}(\mathbf{u}, t_{\mathrm{sil}} - \delta)) \geq (\sqrt{r_l^2+\delta^2} - r_l + \frac{\delta}{\sqrt{r_l^2+\delta^2}})^{-\gamma} (\sqrt{r_l^2+\delta^2} - r_l)$$

当 $\gamma > 2$ 且 $\delta \to 0$ 时，该下界趋于无穷，意味着接近表面的点获得极大权重。

#### 模块 4：边界一致性的理论保证（Kronecker Delta 行为）

在理想 $C^1$ 连续 SDF 和理想球追踪器的假设下，Lemma 3.4 证明了权重的 Kronecker Delta 行为：在轮廓线上，随着球追踪迭代次数 $n \to \infty$，归一化权重完全集中在极限表面点：

$$\lim_{\mathbf{u} \to \mathcal{U}_{\mathrm{sil}}} \lim_{n \to \infty} \frac{w^{(q)}(\mathbf{x}_n(\mathbf{u}; t))}{\sum_{\mathbf{x}_i \in \mathcal{T}(u)} w^{(q)}(\mathbf{x}(\mathbf{u}; t')) \cdot \mathrm{d}t'} = 1$$

这一性质保证了边界一致性：在轮廓线附近，加权方案自动将所有权重分配给实际表面点，消除了边界处的不连续性。

#### 模块 5：Top-k 子集选择与权重偏移

为提高计算效率并保证连续性，DSDF 只保留权重最大的 $k$ 个采样点（$\mathcal{T}_k(\mathbf{u})$），并对所有权重减去第 $k$ 大的权重值（权重偏移）：

$$w^{\mathrm{k}}(\mathbf{x}_i) = \max(0, w^q(\mathbf{x}_i) - w^q_{(k)})$$

其中 $w^q_{(k)}$ 为第 $k$ 大的原始权重。Lemma 4.1 证明了该 top-k 加权方案在非轮廓点 $\mathbf{u} \notin \mathcal{U}_{\mathrm{sil}}$ 处是连续的：当某个点被替换出 top-k 集合时，被替换点和替换点的 top-k 权重均为零（$w^{\mathrm{k}}(\mathbf{x}_i) = w^{\mathrm{k}}(\mathbf{x}_j) = 0$），且此时两者的原始权重相等（$w^{\mathfrak{q}}(\mathbf{x}_i) = w^{\mathfrak{q}}(\mathbf{x}_j)$），保证了权重函数的连续过渡。

消融实验表明（Figure 2）：子集大小 $k < 7$ 时重建质量快速下降，$k \geq 14$ 后收益递减。这一现象可解释为：过小的 $k$ 无法充分覆盖表面对轮廓积分的贡献，而过大的 $k$ 则引入了远离表面的低权重噪声点。

#### 模块 6：轮廓积分与渲染

最终利用重参数化后的加权点集计算轮廓积分，通过自动微分获得像素颜色的梯度，用于反向传播更新神经 SDF 网络参数。

### 参数 $\gamma$ 的关键作用与消融证据

权重指数 $\gamma$ 直接控制权重向表面集中的程度：
- $\gamma$ 过小：权重分布过于平坦，方差降低效果有限
- $\gamma$ 过大（$\gamma \geq 6$）：权重过度集中，优化经常不收敛（Figure 2 消融实验）
- $\gamma = 3$ 在偏差-方差权衡中取得最优平衡

### 局限性与边界条件

1. **理想假设的脆弱性**：理论证明依赖理想 $C^1$ 连续 SDF 和理想球追踪器，实际神经 SDF 在锐利边角或不连续区域可能违反该假设，权重方案的连续性和边界一致性可能退化。
2. **参数调优未充分探索**：球追踪步数与避免无限权重的调整参数 $\epsilon$ 的最佳组合尚未系统研究，可能影响梯度质量和收敛速度。
3. **扩展性未知**：本方法专为轮廓积分设计，是否可扩展到体积渲染等其他可微渲染管线尚待验证。

## 实验与关键发现

### 核心消融实验

方法的关键超参数——权重指数 $\gamma$ 和 top-k 子集大小 $k$——对重建质量和收敛行为有决定性影响。图 2 的消融实验系统探索了这两个参数的取值空间。

**权重指数 $\gamma$ 的影响。** 实验结果表明，$\gamma=3$ 是最优的权重指数设置，能够在低方差和高重建质量之间取得最佳平衡。当 $\gamma$ 取过低值时，权重对表面点的集中程度不足，导致梯度方差仍然较大；当 $\gamma \geq 6$ 时，权重过于集中在极少数点上，优化过程频繁出现不收敛的情况。这一现象与理论分析一致：Lemma 3.2 和 Lemma 3.4 证明了权重 $w^q$ 在轮廓线附近需要以足够快的速度发散才能保证边界一致性，但过快的发散速度（对应过大的 $\gamma$）会导致数值不稳定，使得梯度估计对球追踪采样点的微小位置变化过度敏感。

**top-k 子集大小 $k$ 的影响。** 在球追踪步数固定为 22 的条件下，实验考察了 $k$ 从较小值到较大值的重建质量变化。当 $k < 7$ 时，重建质量快速下降——这说明保留的采样点过少，无法充分捕获轮廓附近的几何信息，导致梯度估计偏差增大。当 $k \geq 14$ 时，收益递减现象明显，继续增大 $k$ 不再带来显著的质量提升，反而增加了计算开销。这一结果验证了 top-k 子集选择策略的有效性：只需保留少量高权重采样点即可获得高质量的梯度估计，同时 Lemma 4.1 保证了权重在非轮廓点处的连续性，避免了子集切换带来的跳变。

**参数组合的实践指导。** 综合消融结果，推荐的参数设置为 $\gamma=3$、$k \in [7, 14]$，配合 22 步球追踪。该组合在实验中表现出稳定的收敛行为和高质量的重建结果。

### 方法对比与机制验证

**盒式滤波器 + 边界积分 vs. 高斯滤波器。** 图 1 从机制层面对比了本方法与现有高斯滤波器方法（如 Bangaru et al. 2020; Loubet et al. 2019）的核心差异。现有方法使用无界高斯滤波器来避免处理像素滤波器边界 $\mathcal{U}_b$，但代价是高斯权重的导数在像素内部区域引入了额外的方差项。本方法保留盒式滤波器，并通过散度定理将外部区域积分显式转换为像素边界上的边界积分：

$$I_{\mathrm{sil}} = \int_{\mathcal{U} \backslash \mathcal{U}_{\mathrm{sil}}} \nabla \cdot (L \mathcal{V}) - \oint_{\mathcal{U}_{\mathrm{b}}} L (\mathcal{V} \cdot \mathbf{n}_b)$$

这一处理消除了高斯滤波器引入的内部方差源，同时在理论上保持了偏差为零（当边界积分被准确计算时）。实验中的稳定收敛行为支持了这一理论优势。

**权重方案的理论保证与实验一致性。** Lemma 3.4 证明了在理想 $C^1$ 连续 SDF 和理想球追踪器的假设下，归一化权重在轮廓线上呈现 Kronecker delta 行为——即权重完全集中在极限表面点上。消融实验中 $\gamma=3$ 时重建质量最优的结果，从实验角度验证了权重集中机制的有效性：适中的集中程度既保证了边界一致性（低偏差），又避免了过度集中导致的数值不稳定（低方差）。

### 失败模式与适用边界

**非理想 SDF 下的潜在退化。** 理论证明依赖于理想 $C^1$ 连续 SDF 的假设，但在实际神经 SDF 中，网络表示的平滑度受限于网络结构和训练程度。当场景包含锐利边角、薄结构或不连续区域时，SDF 的局部行为偏离球形近似（图 3 中的下界推导基础），权重方案可能无法保持理想的边界一致性。论文未提供在此类非理想几何下的定量退化分析，这一点需要在实际应用中通过手动验证确认。

**球追踪步数与参数耦合未充分探索。** 消融实验固定球追踪步数为 22，但未系统研究步数与 $\gamma$、$k$ 的交互效应。步数过少会导致球追踪未能充分逼近真实表面，此时即使权重方案正确，梯度估计的偏差也会增大；步数过多则增加计算成本。论文明确指出“球追踪步数和避免无限权重的调整参数的最佳组合仍未被探索”，这意味着在实际部署中，用户可能需要针对具体场景手动调优这些超参数。

**收敛敏感区。** $\gamma \geq 6$ 时频繁不收敛的现象揭示了一个实践边界：权重方案的发散速度存在一个临界区间，超过该区间后优化过程变得高度不稳定。这一敏感区可能随场景复杂度、SDF 网络容量和球追踪精度的不同而偏移，论文未提供自适应调整机制来应对这一变化。

### 开放问题与验证缺口

论文未报告与基线方法（如 Bangaru et al. 2020）在标准基准上的定量对比结果（如 Chamfer distance、IoU 等指标），也未提供不同场景类型（如室内、室外、多尺度物体）下的泛化测试。消融实验仅针对方法自身的超参数，缺少与高斯滤波器方法在相同条件下的方差-偏差分解对比。这些缺口使得方法优势的量化程度和适用范围需要进一步验证。

![[assets/figures/papers/paper_list_l45_https_people_csail_mit_edu_sbangaru_projects_dsdf_2022_index_html/figures/001_Figure_2.jpg]]
*Figure 2: Ablation Study. We find that*

## 定位与知识库关联

本工作 **DSDF** (Differentiable SDF through Reparameterization) 在可微渲染管线中改变了两个关键 slot，直接回应了现有基于高斯滤波方法的核心瓶颈。

### 改变的 Slot 与基线对比

**Slot 1：像素滤波器类型与边界处理策略**

现有方法（**Bangaru et al. 2020**；**Loubet et al. 2019**）采用无界高斯滤波器来规避像素边界的显式处理——因为盒式滤波器在像素边界处会产生不连续，而高斯滤波器的无限支撑域使得积分域自然延拓，无需处理边界。但这一便利的代价是：高斯权重的梯度在整个像素内部区域引入了额外的方差，导致优化过程不稳定，尤其当重建表面接近像素边界时方差显著增大。

DSDF 的选择恰好相反：**保留盒式滤波器，但通过边界积分显式消除像素边界带来的不一致**。具体而言，将轮廓积分拆分为像素内部区域和外部区域两部分（公式 $I_{\mathrm{sil}} = \int_{\mathcal{U} \backslash \mathcal{U}_{\mathrm{sil}}} \nabla \cdot (L \mathcal{V}) + \int_{(\mathcal{U}_{\infty} \backslash \mathcal{U}) \backslash \mathcal{U}_{\mathrm{b}}} \nabla \cdot (L \mathcal{V})$），然后利用散度定理将外部区域积分转换为像素滤波器边界 $\mathcal{U}_{\mathrm{b}}$ 上的边界积分（公式 $I_{\mathrm{sil}} = \int_{\mathcal{U} \backslash \mathcal{U}_{\mathrm{sil}}} \nabla \cdot (L \mathcal{V}) - \oint_{\mathcal{U}_{\mathrm{b}}} L (\mathcal{V} \cdot \mathbf{n}_b)$）。这一处理在理论上消除了高斯滤波器引入的内部方差，同时保持了偏差的可控性（Fig. 1 左右对比直观展示了这一差异）。

**Slot 2：轮廓积分重参数化的权重方案**

基线方法中，轮廓积分的重参数化权重通常基于高斯滤波器的无界支撑或均匀采样，导致采样点权重分散、梯度估计方差大。DSDF 提出了一种基于 SDF 值和梯度方向的加权方案 $w^q$，通过指数参数 $\gamma$ 控制权重向实际表面点的集中程度。理论分析（Lemma 3.4）证明，在理想 $C^1$ 连续 SDF 和理想球追踪器下，当视线接近轮廓线时，归一化权重完全集中在极限表面点上（Kronecker delta 行为），从而保证了边界一致性。此外，top-$k$ 子集选择与最小权重偏移机制（Lemma 4.1）确保了非轮廓点处权重的连续性。

### 知识库挂载点

本工作可挂载到以下知识库节点：

1. **可微渲染—轮廓积分方法**：作为基于重参数化的可微 SDF 渲染分支，DSDF 在“像素滤波器处理”子节点下提供了盒式滤波器+边界积分的替代方案，与高斯滤波器路线形成对照。该节点关联的方法还包括 **Loubet et al. 2019** 和 **Bangaru et al. 2020** 的早期工作。

2. **蒙特卡洛梯度估计—方差缩减**：DSDF 通过权重集中化（$w^q$ 方案）和 top-$k$ 稀疏化，实质上是一种针对轮廓积分的方差缩减技术。可与重要性采样、控制变量法等通用方差缩减节点关联。

3. **神经隐式表示—SDF 优化**：作为神经 SDF 重建的优化工具，DSDF 的梯度质量直接影响重建精度。该节点下可关联基于可微渲染的 SDF 学习方法（如 IDR、NeuS 等），但需注意 DSDF 针对的是表面渲染管线，与体渲染管线（volumetric rendering）存在架构差异。

### 适用边界与限制

1. **理想假设的脆弱性**：DSDF 的理论正确性依赖于理想 $C^1$ 连续 SDF 和理想球追踪器的假设。在实际神经 SDF 中，网络表示的平滑度有限，尤其在锐利边角或不连续区域，权重方案是否仍保持连续性和边界一致性需要手动验证。论文未提供在这些退化情况下的实验证据。

2. **超参数敏感性**：消融实验（Fig. 2）表明，权重指数 $\gamma=3$ 时重建质量最优，而 $\gamma \geq 6$ 时经常不收敛；top-$k$ 子集大小 $k<7$ 时质量快速下降，$k \geq 14$ 时收益递减。这些参数的最优值可能依赖于具体场景和网络架构，缺乏自适应选择机制。此外，球追踪步数与避免无限权重的调整参数的最佳组合未被充分探索。

3. **管线兼容性**：DSDF 针对的是基于表面表示的可微渲染管线（轮廓积分），扩展到体渲染管线（如 NeRF 类方法）的可行性和效果尚未验证。

### 后续工作启发

1. **非理想 SDF 下的鲁棒性改进**：设计在 SDF 不连续或梯度突变区域的权重修正方案，或引入局部平滑先验以逼近理想 $C^1$ 条件。

2. **自适应超参数选择**：基于视线几何和局部 SDF 特征，动态调整 $\gamma$、$k$ 和球追踪步数，以在重建质量与计算效率之间取得更优平衡。

3. **跨管线迁移**：探索将盒式滤波器+边界积分的处理策略迁移到体渲染管线中的像素积分环节，或将 $w^q$ 加权思想应用于体渲染的采样点权重设计。

## 原文 PDF

![[paperPDFs/SIGGRAPH_ASIA_2022/Differentiable_Rendering_of_Neural_SDFs_through_Reparameterization.pdf]]