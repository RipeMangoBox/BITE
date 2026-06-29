---
title: Path-space Differentiable Rendering of Implicit Surfaces
type: paper
paper_level: A
venue: SIGGRAPH
year: 2024
pdf_ref: paperPDFs/SIGGRAPH_2024/Path_space_Differentiable_Rendering_of_Implicit_Surfaces.pdf
project_link: null
code_link: null
aliases:
- PSDRIS
tags:
- SIGGRAPH_2024
- topic/graphics_geometry_processing
- topic/graphics_rendering_materials
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
core_operator: 将参考表面定义为π=0时的零水平集，仅在参考点处定义沿法线的一维映射（而非全局一对一的参数化），并通过对边界路径积分进行多向形式重写与变量替换，将对隐式曲面的边界采样转化为在代理形状上的采样，从而绕过了隐式曲面的全局参数化需求和昂贵的轮廓检测。
primary_logic: 通过局部法线映射和代理采样，可以在隐式曲面上直接构造边界路径，使得路径空间可微渲染可以推广到零水平集定义的任意隐式曲面，而不依赖于显式的网格参数化。
claims:
- 导数图像与使用大量样本的有限差分参考高度吻合，验证了理论推导和实现的正确性。
- 在逆渲染任务中，我们的单向估计器对所有三个分量（内部、主边界、次级边界）均估计出更干净的梯度，优化得到的形状比 diffSDF 更平滑、更接近目标。
- 次级边界积分的显式采样配合引导网格，在只观测到形状阴影的场景中方差明显低于 diffSDF。
- NEFERTITI / SUZANNE 上 导数图像视觉比对 = 与 FD 参考高度匹配
---

# Path-space Differentiable Rendering of Implicit Surfaces

> [!tip] 核心洞察
> 通过局部法线映射和代理采样，可以在隐式曲面上直接构造边界路径，使得路径空间可微渲染可以推广到零水平集定义的任意隐式曲面，而不依赖于显式的网格参数化。

| 字段 | 内容 |
|------|------|
| 中文题名 | 隐式曲面的路径空间可微渲染 |
| 英文题名 | Path-space Differentiable Rendering of Implicit Surfaces |
| 会议/期刊 | SIGGRAPH 2024 |
| Links | [paper](https://shuangz.com/projects/psdr-sdf-sg24/) |
| Topic | #topic/graphics_geometry_processing #topic/graphics_rendering_materials #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction |
| Method | Path-space Differentiable Rendering for Implicit Surfaces |
| Dataset | NEFERTITI / SUZANNE, CHAIR, BUNNY, SHADOW |

> [!tip] 效果简介
> - NEFERTITI / SUZANNE 上，导数图像视觉比对 与 FD 参考高度匹配 vs 有限差分（高样本） (无显著差异)。
> - CHAIR 上，逆渲染重建质量（Chamfer距离/视觉） 更干净的梯度，恢复薄结构 vs diffSDF (显著更好)。
> - BUNNY 上，重建平滑度 对所有三个分量估计更好，形状更平滑 vs diffSDF (更好)。

## 概要

本文解决了**隐式曲面（零水平集）上路径空间可微渲染**的核心难题：由于缺乏显式参数化，现有的面向网格的边界积分采样策略无法直接应用。作者通过**局部法线映射**和**代理形状采样**，将路径空间可微渲染框架从三角网格推广到任意连续隐式曲面，无需全局一对一的材料参数化，也无需昂贵的轮廓检测。

核心方法包括：在参考表面（$\pi=0$ 的零水平集）上定义仅沿法线的一维局部映射；将边界路径积分重写为多向形式，并通过变量替换将对隐式曲面的边界采样转化为在代理几何体上的采样；针对相机可见轮廓设计主边缘采样算法，针对非直接可见的次级边界段使用代理表面与切线方向的 next-event estimation。

实验表明，导数图像与大量样本的有限差分参考高度吻合；在逆渲染任务中，本方法对所有三个梯度分量（内部、主边界、次级边界）均估计出比 diffSDF 更干净的梯度，优化得到的形状更平滑、更接近目标，且在仅观测形状阴影的场景中次级边界积分方差显著更低。该方法在**几何表示**和**材料参数化映射**两个关键槽位上区别于基于网格的可微渲染，为隐式曲面的物理可微渲染提供了新的理论工具和实用估计器。

## 核心方法与创新机理

### 问题瓶颈：隐式曲面上的边界积分困境

路径空间可微渲染的核心梯度表达式（Zhang et al., SIGGRAPH 2020）将渲染积分的导数分解为两项：**内部积分**（interior integral）和**边界积分**（boundary integral）。边界积分捕捉因几何变形导致的可见性突变（轮廓/遮挡边界）对梯度的贡献，而正确处理该积分是获得完整、正确梯度的关键。

在面向网格的原始框架中，边界积分的采样依赖两个前提：（1）显式的边缘检测——通过网格的拓扑结构直接定位轮廓边；（2）全局一对一的材料参数化映射 $\mathsf{X}(\mathbf{p}, \pi)$，将参考表面上的每一点唯一映射到变形后表面上。然而，当几何表示从三角网格切换为**隐式曲面**（零水平集 $\{\mathbf{p} \mid \phi(\mathbf{p}) = 0\}$）时，这两个前提同时失效：

- 隐式曲面缺乏显式的边缘/顶点拓扑，无法直接进行轮廓检测和边缘采样；
- 构造全局一对一的参数化映射在隐式曲面上极为困难，尤其是当曲面拓扑在优化过程中发生变化时。

现有方法（如 **diffSDF**，Vicini et al., SIGGRAPH 2022）通过重参数化策略规避了部分问题，但其边界积分估计存在高方差，且在复杂光照和薄结构场景中梯度质量显著下降。本文的核心贡献在于**系统性地将路径空间可微渲染框架推广到隐式曲面**，通过三个关键机制突破上述瓶颈。

### 核心机制：局部法线映射与代理采样

本文的核心洞察是：**边界积分的计算并不需要全局一对一的参数化，而仅需在参考表面 $\mathcal{B}$（$\pi=0$ 时的零水平集）上定义局部映射**。具体而言，作者提出以下创新链：

1. **局部法线映射**：定义 $\mathsf{X}(\mathbf{p}, \pi) := \mathbf{p} + t(\mathbf{p}, \pi) \, \mathbf{n}_{\mathcal{B}}(\mathbf{p})$，其中 $t(\mathbf{p}, \pi)$ 是从参考点 $\mathbf{p}$ 沿其法线 $\mathbf{n}_{\mathcal{B}}(\mathbf{p})$ 到变形后曲面 $M(\pi)$ 的交点距离。该映射仅在 $\pi=0$ 处要求一对一（此时 $t=0$），避免了全局参数化的困难。

2. **多向边界路径重写**：将边界积分改写为多向形式（multi-directional form），将边界路径分解为**源子路径**（source subpath）、**探测器子路径**（detector subpath）和**边界段**（boundary segment）三部分。这一重写将轮廓检测的需求压缩到仅需在相机端进行主边缘采样，而次级边界积分可通过变量替换转化为在代理表面上的采样。

3. **代理采样策略**：对于次级边界积分，通过将积分变量从 $(\mathbf{p}^S, \mathbf{p}^D)$ 变换为 $(\mathbf{p}^B, \boldsymbol{\omega}^B)$（边界点与边界方向），将对隐式曲面上边界段的采样转化为在**代理表面**（proxy surface，如包围盒面）上的采样，再通过投影求交获得隐式曲面上的对应点。

### 模块架构与因果关系

整个方法由四个顺序耦合的模块构成，形成从理论推导到数值估计的完整管线：

#### 模块 1：材料形式重参数化与速度场计算（§4.1）

**输入**：隐式曲面 $\phi(\mathbf{p}) = 0$，参考表面 $\mathcal{B}$，变形参数 $\pi$。

**操作**：
- 定义局部映射 $\mathsf{X}(\mathbf{p}, \pi)$ 和参考点速度 $\boldsymbol{\upsilon}(\mathbf{p}) := (\partial_{\pi} t)(\mathbf{p}) \, \mathbf{n}_{\mathcal{B}}(\mathbf{p})$；
- 计算面积缩放因子 $J(\mathbf{p})$ 及其导数 $\partial_{\pi} J(\mathbf{p}) = \kappa(\mathbf{p}) V(\mathbf{p})$，其中 $\kappa$ 为平均曲率，$V$ 为法向速度分量。

**因果作用**：此模块为后续所有积分估计提供必需的几何导数（点速度、雅可比导数），是内部积分估计和边界积分被积函数计算的基础。

#### 模块 2：主边缘采样（Primary Edge Sampling，§5.1, Algorithm 1）

**问题**：当相机是路径端点时，前述变量替换失效，必须显式检测并采样相机可见的轮廓点（主边缘）。

**创新机制**：
- 定义**取向函数** $\psi_{\phi,c}(\mathbf{p}) := \langle \nabla\phi(\mathbf{p}), \mathbf{v}_c(\mathbf{p}) \rangle$，即表面法线与视线向量的点积；
- 主边缘集合定义为隐式曲面与取向函数零等值面的交集：$S := \{ \mathbf{p} \mid \phi(\mathbf{p}) = 0, \, \psi_{\phi,c}(\mathbf{p}) = 0 \}$；
- 使用**仿射算术**（affine arithmetic）进行范围分析，快速剔除不可能包含主边缘的空间区域（AABB），将搜索范围限制在同时可能与 $\phi=0$ 和 $\psi=0$ 相交的包围盒内；
- 在筛选后的包围盒面上进行**行进采样**（marching），通过沿代理表面边缘追踪 $\phi$ 和 $\psi$ 的交点来定位主边缘点。

**因果作用**：为主边界路径积分提供采样点，是处理相机端可见性突变的关键。

#### 模块 3：次级边界积分采样（Secondary Boundary Integral，§4.2, §5.2）

**问题**：非相机端的边界段（如阴影边界）需要通过变量替换进行采样。

**创新机制**：
- **变量替换链**：先将探测器点 $\mathbf{p}^D$ 投影回边界点 $\mathbf{p}^B$，再将边界点 $\mathbf{p}^B$ 投影到源点 $\mathbf{p}^S$ 的切平面上，最终将积分域变换为 $(\mathbf{p}^B, \boldsymbol{\omega}^B)$；
- **代理表面采样**：在代理表面 $\mathcal{F}$（如 AABB 面）上采样点 $\mathbf{q}$，沿固定方向求交获得隐式曲面上的多个交点 $\mathcal{T}_i(\mathbf{q})$，每个交点贡献 $g_i(\mathbf{q})$，未定义交点贡献为零；
- **引导策略**：使用引导网格（guide grid）定位未被遮挡的光源区域，降低次级边界积分的估计方差。

**因果作用**：为次级边界路径积分提供采样点，处理非直接可见的几何不连续性。

#### 模块 4：双向路径构造（Bidirectional Path Construction，§3, §5）

**问题**：当光源难以采样（如小面积光源）或材质为高光泽/镜面时，单向路径构造（仅从相机或光源出发）效率极低。

**创新机制**：
- 分别构造**源子路径**（从光源出发）和**探测器子路径**（从相机出发），通过边界段连接两者；
- 边界段由模块 2（相机端）或模块 3（光源端/中间端）的采样结果提供；
- 支持多重重要性采样（MIS）在源和探测器子路径之间进行加权组合。

**因果作用**：提升困难光照条件下的梯度估计质量，是单向估计器的自然扩展。

### 关键公式及其变量含义

**梯度分解**（Eq. 5）：
$$\frac{dI}{d\pi} = \int_{\hat{\Omega}} \frac{d}{d\pi} \hat{f}(\bar{p}) d\mu(\bar{p}) + \int_{\partial\hat{\Omega}} \hat{f}(\bar{p}) V_{\partial}(p_K) d\dot{\mu}$$

- 第一项为内部积分：捕捉材质和几何的连续变化；
- 第二项为边界积分：捕捉可见性突变，$V_{\partial}$ 为边界速度。

**局部映射**（Eq. 14）：
$$\mathsf{X}(\mathbf{p}, \pi) := \mathbf{p} + t(\mathbf{p}, \pi) \mathbf{n}_{\mathcal{B}}(\mathbf{p})$$

- $\mathbf{p}$：参考表面 $\mathcal{B}$ 上的点；
- $t(\mathbf{p}, \pi)$：沿法线到变形后曲面的有符号距离；
- $\mathbf{n}_{\mathcal{B}}(\mathbf{p})$：参考表面法线。

**主边缘定义**（Eq. 22-23）：
$$\psi_{\phi,c}(\mathbf{p}) := \langle \nabla\phi(\mathbf{p}), \mathbf{v}_c(\mathbf{p}) \rangle$$
$$S := \{ \mathbf{p} \mid \phi(\mathbf{p}) = 0, \, \psi_{\phi,c}(\mathbf{p}) = 0 \}$$

- $\nabla\phi(\mathbf{p})$：隐式函数梯度（表面法线方向）；
- $\mathbf{v}_c(\mathbf{p})$：从 $\mathbf{p}$ 指向相机针孔的方向向量；
- $S$：主边缘点集，即轮廓生成点。

### Changed Slots 总结

相对于面向网格的路径空间可微渲染（Zhang et al., SIGGRAPH 2020），本文在以下关键槽位上进行了替换：

| 槽位 | 基线值（网格方法） | 本文值（隐式曲面方法） | 证据锚点 |
|------|-------------------|----------------------|---------|
| 几何表示 | 三角网格（显式） | 零水平集隐式曲面 | §4.1, Eq.(12-13) |
| 材料参数化映射 | 全局一对一映射 | 仅在 $\pi=0$ 处一对一的局部法线映射 | Eq.(14) |
| 主边缘采样 | 基于网格边缘检测 | 取向函数 $\psi$ + 仿射算术范围分析 + 代理行进采样 | §5.1, Eq.(22-23), Algorithm 1 |
| 次级边界积分 | 基于网格的变量替换与面片采样 | 代理表面采样 + 切平面方向 next-event estimation | §4.2, §5.2 |

### 推理路径

**训练/优化时**（逆渲染）：
1. 给定当前隐式曲面 $\phi$ 和场景参数（材质、光照）；
2. 前向渲染：使用双向路径追踪生成图像；
3. 梯度估计：并行计算三个分量——
   - 内部积分：对每条路径计算被积函数导数；
   - 主边界积分：通过模块 2 采样主边缘，构造边界路径；
   - 次级边界积分：通过模块 3 采样边界段，连接源/探测器子路径；
4. 使用 Adam 优化器更新 $\phi$ 的参数（如 SDF 网格值），使 L2 损失最小化。

**关键因果链**：局部法线映射（模块 1）→ 提供几何导数 → 内部积分可计算；取向函数定义（模块 2）→ 主边缘可定位 → 主边界积分可采样；变量替换（模块 3）→ 次级边界积分转化为代理采样 → 避免全局参数化；双向构造（模块 4）→ 处理困难光照 → 降低整体方差。

![[assets/figures/papers/paper_list_l30_https_shuangz_com_projects_psdr_sdf_sg24/figures/010_Figure_8.jpg]]
*Figure 8: We validate our method by comparing derivative images estimated by our method to that by finite difference (FD) with a large number of samples. Our NEFERTITI and SUZANNE results are computed using our unidirectional and bidirectional estimators, respectively. Our results closely match the FD reference and demonstrate the correctness of our implementation*

## 实验与关键发现

本文的实验围绕三个层次展开：首先验证路径空间可微渲染导数估计的正确性，随后在逆渲染任务中与 **diffSDF**（Vicini et al., SIGGRAPH 2022）进行系统性对比，最后通过消融实验揭示双向估计器和引导策略的价值边界。

---

### 导数正确性验证

在 **NEFERTITI** 和 **SUZANNE** 两个场景上，将本方法估计的导数图像与使用大量样本的有限差分（FD）参考进行视觉比对（Figure 8）。其中 NEFERTITI 使用单向估计器，SUZANNE 使用双向估计器，两者均与 FD 参考高度吻合。这一结果验证了从材料形式重参数化（Eq. (14)–(17)）到主边界采样（Algorithm 1）和次级边界积分采样（§5.2）的整套理论推导和实现是正确的。

---

### 逆渲染任务对比

所有逆渲染实验采用统一的配置：Adam 优化器、L2 损失、8 个视角、batch size 为 2。对比对象为基于网格 SDF 实现的 diffSDF，其采用重参数化策略处理隐式曲面。

**CHAIR 场景**（Figure 10）要求从多视角观测中恢复具有薄结构的椅子形状。本方法的单向估计器估计出更干净的梯度，成功恢复了椅背和椅腿等薄结构，而 diffSDF 的优化结果在这些区域出现断裂或模糊。这表明本方法对复杂拓扑的恢复能力更强，其核心原因在于主边界积分和次级边界积分均能正确处理隐式曲面上的可见性不连续。

**BUNNY 场景**（Figure 11）进一步展示了梯度估计质量的优势。本方法对内部积分、主边界积分和次级边界积分三个分量均估计出更好的梯度，最终优化得到的形状比 diffSDF 更平滑、更接近目标。这一优势源于：diffSDF 的重参数化策略在边界区域存在系统性偏差，而本方法通过局部法线映射和代理采样直接构造边界路径，避免了全局参数化引入的误差。

**SHADOW 场景**（Figure 12）专门考察次级边界积分的估计质量。该场景中相机只能观测到形状的阴影，梯度信号几乎完全依赖次级边界积分。本方法通过对该分量的显式采样配合引导网格，实现了明显低于 diffSDF 的估计方差。这验证了代理表面采样和切线方向 next-event estimation 策略（§5.2）在困难光照条件下的有效性。

**BOB 场景**（Figure 13）涉及难以采样的光源配置。本方法的双向估计器在导数图像质量和逆渲染重建精度上均优于单向估计器和 diffSDF。这确认了当光源采样困难时，双向路径构造能够有效降低方差，与 Figure 9 的消融结论一致。

---

### 关键消融实验

**单向 vs. 双向估计器**（Figure 9）：在 SUZANNE 场景中，当光源易于采样时，单向和双向估计器表现接近；但当场景包含难以采样的光源和高光泽材质时，双向估计器显著优于单向版本。这一消融明确了双向估计器的适用边界：仅在光源采样困难或存在镜面反射路径时才需要启用双向构造，否则单向估计器已足够且计算开销更低。

**引导网格的作用**（Figure 12）：在 SHADOW 场景中，引导网格通过定位未被遮挡的光源区域，为次级边界积分提供了有效的采样引导，从而降低了估计方差。当前实现采用简单规则网格进行引导，在高光泽表面的反射路径上引导效率较低，这是方法的一个已知局限。

---

### 失败模式与适用边界

1. **高光泽反射路径的引导效率低**：当前基于规则网格的引导策略在漫反射主导的场景中表现良好，但在高光泽表面的间接反射路径上引导效率下降。这需要更精细的引导结构设计，是方法的一个开放问题。

2. **求交与采样的近似偏差**：光线与隐式曲面的求交以及主边缘采样存在微小的近似偏差，但实验表明这些偏差对逆渲染重建质量的影响有限，在视觉和 Chamfer 距离指标上未造成显著退化。

3. **神经隐式表示的集成挑战**：当前实验均在网格 SDF 上进行验证，尽管理论框架（§4）支持任意连续的零水平集函数，但扩展到大型 MLP 等神经隐式表示需要解决求交效率、梯度传播稳定性等系统集成问题。

4. **多边形光源的平面求交**：方法目前对大量多边形光源的高效平面求交支持有限，这限制了在复杂照明场景中的应用。

---

### 实验证据强度总结

| 实验场景 | 核心结论 | 证据强度 | 说明 |
|---------|---------|---------|------|
| NEFERTITI / SUZANNE | 导数图像与 FD 参考高度吻合 | 高 | 直接验证理论正确性，视觉差异不可见 |
| CHAIR | 恢复薄结构能力优于 diffSDF | 中高 | 定性视觉比较，缺少定量 Chamfer 距离数值 |
| BUNNY | 三梯度分量均优于 diffSDF，形状更平滑 | 中高 | 定性比较，需手动确认具体差值 |
| SHADOW | 次级边界积分方差显著低于 diffSDF | 中高 | 方差降低有视觉证据，缺少数值方差报告 |
| BOB | 双向估计器在困难光源下优于单向和 diffSDF | 中 | 单场景验证，泛化性需更多场景确认 |

需要指出的是，论文中逆渲染对比主要依赖视觉定性判断，缺少 Chamfer 距离、PSNR 等定量指标的数值报告。Figure 10–13 的结论虽在视觉上令人信服，但若需严格量化优势，建议查阅补充材料或代码仓库中的完整指标。

![[assets/figures/papers/paper_list_l30_https_shuangz_com_projects_psdr_sdf_sg24/figures/014_Figure_12.jpg]]
*Figure 12: Differentiable and inverse rendering comparison (SHADOW) between our unidirecitional estimator and diffsdf [Vicini et al. 2022]. We compare the secondary boundary integral of our estimator and diffsdf’s in this scene where we only observe the shadow of the shape. We achieve less variance in the secondary boundary integral by explicit sampling this component and guiding*

![[assets/figures/papers/paper_list_l30_https_shuangz_com_projects_psdr_sdf_sg24/figures/015_Figure_13.jpg]]
*Figure 13: Differentiable and inverse rendering comparison (BOB) between our bidirectional estimator, unidirectional estimator and diffsdf [Vicini et al. 2022]. With scenes where lights are difficult to sample, our bidirectional estimator can achieve less variance than other unidirectional estimators*

![[assets/figures/papers/paper_list_l30_https_shuangz_com_projects_psdr_sdf_sg24/figures/005_Figure_4.jpg]]
*Figure 4: We change the integration variable from*

![[assets/figures/papers/paper_list_l30_https_shuangz_com_projects_psdr_sdf_sg24/figures/008_Figure_6.jpg]]
*Figure 6: AABBs classified by affine arithmetic as possibly intersect with (a) ?? or ?? and (b) both of them. We bound silhouette S by (b) AABBs that possibly intersect with both the implicit surface*

![[assets/figures/papers/paper_list_l30_https_shuangz_com_projects_psdr_sdf_sg24/figures/009_Figure_7.jpg]]
*Figure 7: (a) We sample points from the implicit surface ?? by sampling a point ?? from the proxy F and project ?? onto the implicit surface ??. We then take all the intersections, T1 (??) and T2 (??) in this example, as the sample points from the implicit surface ??. (b) We intersect the tangent plane T?? B at ?? with light L and only sample from tangent directions intersecting the light L*

## 定位与知识库关联

本文的核心定位在于**将路径空间可微渲染从显式网格几何推广到隐式曲面**，其根本改变的 slot 是**几何表示与材料参数化的耦合方式**。在 Zhang et al. (SIGGRAPH 2020) 建立的理论框架中，路径积分的梯度被分解为内部积分和边界积分，而边界积分的采样策略严重依赖网格的显式边缘结构——主边界通过网格边缘检测采样，次级边界通过全局一对一的材料映射 X(p, π) 进行变量替换。本文识别出这一理论瓶颈：当几何体为零水平集定义的隐式曲面时，既不存在可供遍历的显式边缘，也无法构造全局一对一的参数化映射。

为解决这一问题，作者在以下 slot 上做出了关键替换：

1. **材料参数化映射 slot**：从“对所有 π 全局一对一”改为“仅在 π=0 处一对一，通过沿参考表面法线求交定义局部映射”（Eq. (14)）。这一改变使得参考表面 B 成为唯一的锚定点，避免了为不同 π 维护全局对应关系的需求，从而将材料形式路径积分的理论推广到任意连续水平集函数。

2. **主边界边缘采样 slot**：从“基于网格的边缘检测与遍历”改为“定义隐式取向函数 ψ 为法线与视线方向的点积，主边缘 S 为 φ=0 与 ψ=0 的交集（Eq. (22)-(23)），并通过代理形状上的行进采样（Algorithm 1）和仿射算术范围分析（Figure 6）来定位轮廓”。这绕过了隐式曲面缺乏显式边缘信息的根本困难。

3. **次级边界积分估计 slot**：从“基于网格面片的变量替换”改为“通过代理表面采样和切线方向的 next-event estimation 进行多向形式重写（Figure 4, Figure 7）”，避免了全局轮廓检测的昂贵开销。

与最直接的对比方法 **diffSDF** (Vicini et al., SIGGRAPH 2022) 相比，diffSDF 采用重参数化策略处理隐式曲面，但其梯度估计中缺少对次级边界积分的显式建模和采样引导，导致在仅观测形状阴影的场景中方差较高（Figure 12）。本文通过引入多向形式边界积分和代理采样，显式估计所有三个梯度分量（内部、主边界、次级边界），在逆渲染任务中获得了更干净的梯度和更平滑的重建形状（Figure 10, Figure 11）。

**知识库挂载点**：本文的理论贡献可挂载到可微渲染知识库中的“路径空间方法”节点，作为 Zhang et al. (SIGGRAPH 2020) 框架在隐式几何上的扩展。其局部法线映射和代理采样策略为后续工作在以下方向提供了接口：(1) 神经隐式表示（如 NeRF、NeuS）的可微渲染，当前实现仅验证于网格 SDF，扩展到大型 MLP 需要解决求交效率与梯度传播的工程挑战；(2) 更高效的光源引导策略，当前规则网格引导在高光泽反射路径上效率有限；(3) 多边形面光源的平面求交加速。

**适用边界**：该方法理论上适用于任意连续水平集函数定义的隐式曲面，但当前实现依赖光线步进求交和网格代理采样，存在微小近似偏差。实验表明这些偏差对重建质量影响有限，但在高精度定量任务中需要审慎评估。双向估计器仅在光源难以采样的场景中启用，与单向版本形成互补。方法不支持参与介质和体渲染路径，这是路径空间可微渲染框架本身的边界，而非本文特有局限。

**后续启发**：本文揭示了一个深层洞见——通过将全局参数化需求降级为局部法线映射，可以将边界敏感的路径空间方法推广到更灵活的几何表示。这一思路可能启发其他需要边界积分的物理模拟领域（如可微碰撞检测、可微流体界面），其中隐式曲面同样缺乏显式参数化。此外，代理采样与引导策略的分离设计为未来研究提供了明确的改进靶点。

## 原文 PDF

![[paperPDFs/SIGGRAPH_2024/Path_space_Differentiable_Rendering_of_Implicit_Surfaces.pdf]]