---
title: Unbiased Caustics Rendering Guided by Representative Specular Paths
type: paper
paper_level: A
venue: SIGGRAPH ASIA
year: 2022
pdf_ref: paperPDFs/SIGGRAPH_ASIA_2022/Unbiased_Caustics_Rendering_Guided_by_Representative_Specular_Paths.pdf
project_link: null
code_link: null
aliases:
- RSPG
- UCRGBRSP
tags:
- SIGGRAPH_ASIA_2022
- topic/graphics_geometry_processing
- topic/graphics_rendering_materials
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
core_operator: 通过引入代表性镜面路径（representative specular paths）作为代理，将无限多的光泽反射路径压缩为有限的高斯混合分布（GMM），从而提供高效的入射辐射分布估计，显著改善焦散路径的采样指导。
primary_logic: 对于光泽反射器，虽然连接着色点和光源的路径有无穷多，但它们可以用少量镜面路径来代表，并通过球面高斯（SG）近似每个路径的辐射贡献；进一步通过空间缓存和视差补偿，可以在渲染时快速重建精确的入射辐射分布，从而实现焦散的无偏高效渲染。
claims:
- 在Snail场景等时间渲染中，本文方法RMSE（0.021）显著低于PT（0.073）、BDPT（0.066）和PPG（0.036），且仅需6.5秒预计算。
- 图6显示，SG近似的采样分布与目标高频入射辐射分布的形状高度吻合，仅存在轻微模糊。
- 使用Newton求解器寻找代表性镜面路径比直接使用三角中心能显著降低方差和内存开销（图13）。
- Snail场景 上 RMSE（20分钟等时渲染） = 0.021
---

# Unbiased Caustics Rendering Guided by Representative Specular Paths

> [!tip] 核心洞察
> 对于光泽反射器，虽然连接着色点和光源的路径有无穷多，但它们可以用少量镜面路径来代表，并通过球面高斯（SG）近似每个路径的辐射贡献；进一步通过空间缓存和视差补偿，可以在渲染时快速重建精确的入射辐射分布，从而实现焦散的无偏高效渲染。

| 字段 | 内容 |
|------|------|
| 中文题名 | 基于代表性镜面路径的无偏焦散渲染 |
| 英文题名 | Unbiased Caustics Rendering Guided by Representative Specular Paths |
| 会议/期刊 | SIGGRAPH ASIA 2022 |
| Links | [paper](https://wangningbei.github.io/2022/PathcutGuiding.html) |
| Topic | #topic/graphics_geometry_processing #topic/graphics_rendering_materials #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction |
| Method | Representative Specular Path Guiding |
| Dataset | Snail场景, Musa场景, Bumpy Surface (α=0.05)场景, Three Bumpy Cylinder场景 |

> [!tip] 效果简介
> - Snail场景 上，RMSE（20分钟等时渲染） 0.021 vs PT: 0.073, BDPT: 0.066, PPG: 0.036 (比PT降低71%，比BDPT降低68%，比PPG降低42%)。
> - Musa场景 上，视觉噪声（12分钟等时渲染） 噪声最低，无萤火虫 vs PT、BDPT、PPG (定性噪声显著低于所有基线)。
> - Bumpy Surface (α=0.05)场景 上，视觉噪声（7分钟等时渲染） 噪声远低于SMS vs SMS [Zeltner et al. 2020] (在较高粗糙度下噪声显著减少)。

## 概要

现有路径引导方法（如PPG）依赖在线学习入射辐射分布，难以捕获高频焦散的入射方向分布，导致对焦散路径的采样效率低下、渲染方差大。本文提出**基于代表性镜面路径的无偏焦散渲染方法**，核心思想是：对于光泽反射器，连接着色点与光源的路径虽有无穷多，但可用少量镜面路径来代表，并通过球面高斯（SG）近似每条路径的辐射贡献。具体而言，该方法通过放宽的路径切割求解器（relaxed path cuts solver）预计算代表性镜面路径，利用SG链式估计入射辐射分布，并结合空间缓存与视差补偿在渲染时快速重建精确的采样指导。实验表明，在Snail场景20分钟等时渲染中，本文方法的RMSE（0.021）显著低于PT（0.073）、BDPT（0.066）和PPG（0.036），且仅需6.5秒预计算。方法支持最多两次中间光泽反射（DSS/SDSS焦散），在推荐粗糙度范围（α=0.005–0.05）内表现优异，但对极低粗糙度且法线变化复杂的场景仍有局限。

## 核心方法与创新机理

### 问题背景与唯一瓶颈

焦散（caustics）是光线经光泽表面聚焦后在漫反射面上形成的高频亮斑，在电影和产品可视化中至关重要。渲染焦散的核心困难在于：从接收面着色点出发，经光泽反射器连接光源的路径有无穷多条（Figure 2），这些路径在方向空间形成极窄的入射辐射峰值。现有路径引导方法（如**PPG**，Müller et al., 2017）依赖在线迭代学习入射辐射分布（SD-tree），其学习速率跟不上焦散的高频特性，导致采样效率低下、渲染方差极大。双向路径追踪（BDPT）和光子映射等方法虽然能处理部分焦散路径，但在多次光泽反射场景中同样面临效率瓶颈。

![[assets/figures/papers/paper_list_l96_https_wangningbei_github_io_2022_PathcutGuiding_html/figures/002_Figure_2.jpg]]
*Figure 2: A shading point x on the receiver and a point on the light l can be connected by points on the reflectors, constructing an admissible path. If the reflector is pure specular, the number of paths is finite; if the reflector is glossy, the admissible paths are infinite. The neighboring admissible paths form a glossy path region. We use a specular path to represent this glossy path region. Note that there may be multiple glossy path regions that connect x and l*

### 核心洞察与创新机理

本文的核心洞察是：**对于光泽反射器，连接着色点和光源的无穷多条路径可以用少量镜面路径来代表**（Figure 2）。这些“代表性镜面路径”（representative specular paths）作为代理，将无限的光泽路径区域压缩为有限的高斯混合分布（GMM），从而在渲染前高效估计入射辐射分布的形状。这一洞察将焦散渲染从“在线学习高频分布”转化为“预计算代表性路径并参数化辐射分布”，从根本上规避了在线学习收敛慢的问题。

### Changed Slots：相对于基线方法的三个关键改造

**Slot 1：入射辐射分布估计方法（从在线学习到预计算GMM）**

| 基线（PPG） | 本文方法 |
|---|---|
| 在线迭代学习SD-tree，逐步逼近入射辐射分布 | 预计算代表性镜面路径，用球面高斯（SG）链式估计辐射分布，结合空间缓存与视差补偿在渲染时快速重建 |

**Slot 2：路径切割有效性判据（从纯镜面到光泽放宽）**

| 基线（Wang et al., 2020） | 本文方法 |
|---|---|
| 仅当法向与半向量完全重合（n·h=1）时路径切割有效 | 根据表面粗糙度α放宽判据，使用球面高斯的紧支撑角θ（Eq. 1）作为阈值，允许法向与半向量夹角小于θ的节点通过 |

**Slot 3：采样策略（从单一分布到GMM+BRDF的MIS混合）**

| 基线（BRDF重要性采样或路径引导单一分布） | 本文方法 |
|---|---|
| 单一采样策略 | 将GMM（来自代表性路径的SG混合）与BRDF采样通过多重重要性采样（MIS）结合，以固定概率0.5选择，保证无偏性 |

### 方法框架与模块顺序

整体流程分为预计算和渲染两个阶段，共四个核心模块：

```
预计算阶段：
  [Relaxed Path Cuts Solver] → [SG-based Radiance Accumulation] → [Spatial Caching & Parallax Compensation]
                                                                              ↓
渲染阶段：
  [Spatial Caching & Parallax Compensation] → [MIS Sampling with GMM + BRDF]
```

#### 模块一：Relaxed Path Cuts Solver（放宽的路径切割求解器）

该模块的目标是从场景几何中找出所有能连接光源和接收面的代表性镜面路径。其基础是Wang et al.（2020）的路径切割方法（Figure 3）：将场景组织为空间层次结构，每个节点包含位置区间和法向区间；通过递归细分和剪枝，找到所有k次反弹的叶节点路径切割；对每个叶路径切割，使用Newton求解器最小化半向量与法向的差异，得到一条精确的镜面路径。

![[assets/figures/papers/paper_list_l96_https_wangningbei_github_io_2022_PathcutGuiding_html/figures/003_Figure_3.jpg]]
*Figure 3: Illustration of the path cuts method [Wang et al. 2020]. (a) The scene is first organized into a spatial hierarchy, where each node has a position interval and a normal interval. (b) ?? nodes form a k-bounce path cut. Path cuts are subdivided and pruned to find valid leaf path cuts (i.e., all of the nodes are leaf nodes). (c) If for each node in a path cut, the normal interval and half vector interval have an intersection, then the path cut is valid. (d) For a leaf path cut, the Newton solver finds an admissible specular path by minimizing the differences between the half vectors and the normals*

**本文的关键改造**：将路径切割的有效性判据从纯镜面（n·h=1）放宽到光泽表面。具体而言，利用表面粗糙度α定义球面高斯的紧支撑角θ：

$$\theta = \operatorname{arccos}\left(\frac{\ln(\varepsilon\pi\alpha^2)\alpha^2}{2} + 1\right) \quad \text{(Eq. 1)}$$

其中ε为阈值常量（通常取0.01）。当一个节点的法向区间与半向量区间的最大点积值对应的角度小于θ时，该节点被视为有效。这一放宽使得路径切割能捕获光泽反射带来的路径区域，而不仅仅是纯镜面反射的孤立路径。对于每条代表性路径，如果Newton求解器找到的反射点落在三角形外部，则使用三角形内部误差最小的替代点（Figure 4）。

**因果链**：粗糙度α → 紧支撑角θ → 放宽的节点有效性判据 → 更多路径切割被保留 → 覆盖光泽路径区域 → 代表性路径集合完整。

#### 模块二：SG-based Radiance Accumulation（基于球面高斯的辐射累积）

对于每条代表性镜面路径，需要估计其代表的光泽路径区域对着色点的辐射贡献。本文引入球面高斯（Spherical Gaussian, SG）作为统一的近似工具：

$$G(\mathbf{v}; \mathbf{p}, \lambda, A) = A e^{\lambda(\mathbf{p} \cdot \mathbf{v} - 1)} \quad \text{(Eq. 2)}$$

其中p为中心方向，λ为锐度（λ越大波瓣越窄），A为振幅。

**近似链**（Figure 5）：
1. **光源近似**：将点光源或小面积球面光源近似为SG（Eq. 4）：
   $$L_e(\mathbf{i}) \approx G_l(\mathbf{i}; p_l, \lambda_l, C_l)$$
   
2. **BRDF切片近似**：对于给定的视线方向o，将BRDF切片（入射方向i的函数）近似为单个SG（Eq. 3）：
   $$\rho(\mathbf{i}, \mathbf{o}) \approx G_\rho(\mathbf{i}; p_\rho, \lambda_\rho, C_\rho)$$

3. **乘积积分**：着色点处的入射辐射分布由光源SG和BRDF SG的乘积积分得到（Eq. 5）：
   $$\mathcal{L}(\mathbf{o}) = \int_{\Omega} G_l(\mathbf{i}) G_\rho(\mathbf{i}) \cos\theta \mathrm{d}\mathbf{i} \approx G_r\left(\mathbf{o}; 2(\mathbf{n} \cdot p_l)\mathbf{n} - p_l, \frac{\lambda_\rho\lambda_l}{\lambda_\rho + \lambda_l}, \frac{(\mathbf{n} \cdot p_l) 2\pi C_\rho C_l}{\|\lambda_l p_l + \lambda_\rho p_\rho\|}\right)$$

   这一闭式解给出反射方向的SG，其中心方向为光源关于表面法向的镜面反射方向，锐度为两SG锐度的调和组合。

4. **多反弹扩展**：对于多次光泽反射的路径，沿路径逐次应用上述乘积积分，最终在接收面着色点处得到一个SG，代表该代表性路径对应光泽路径区域的入射辐射分布。

**关键验证**（Figure 6）：将SG近似的采样分布与目标入射辐射分布对比，两者形状高度吻合，仅存在轻微模糊。这证明SG近似能有效捕获焦散的高频方向分布。

**因果链**：代表性镜面路径 → 光源SG × BRDF切片SG → 乘积积分闭式解 → 入射辐射SG → 多条路径的SG混合为GMM → 高效编码高频入射辐射分布。

#### 模块三：Spatial Caching & Parallax Compensation（空间缓存与视差补偿）

直接在每一着色点计算GMM代价过高。本文提出在接收面三角形上预计算并缓存GMM，渲染时通过视差补偿快速适配到具体着色点。

**缓存策略**：在接收面的每个三角形顶点缓存GMM（即多个SG的混合），以及视差补偿所需的几何信息（反射器曲率、光源虚像位置等）。

**视差补偿机制**（Figure 7, 8）：
- **平面反射器**：光源虚像位置与着色点无关，直接连接虚像和着色点得到修正方向ô，将SG中心方向旋转到ô。
- **球面反射器**：光源点的虚像位置通过透镜公式计算（Eq. 6）：
  $$d_v = \frac{1}{\frac{1}{f} - \frac{1}{d_r}}, \quad h_v = -\frac{d_v}{d_r} h_r$$
  其中f为焦距，d_r为光源到反射器距离，d_v为虚像到反射器距离。
- **任意曲面反射器**（Figure 8）：沿两个主曲率方向分别视为球面反射器，计算各自的偏移量Δ_s和Δ_t（Eq. 7），合并得到修正后的反射点位置（Eq. 8）：
  $$\mathbf{y}' = \Delta_s \mathbf{s} + \Delta_t \mathbf{t} + y$$

渲染时，根据着色点位置计算修正方向，将缓存GMM中每个SG的中心方向旋转到修正方向，实现视差校正。

**因果链**：预计算缓存GMM → 着色点位置 → 视差补偿（虚像/偏移计算） → 旋转SG中心方向 → 着色点精确入射辐射分布 → 指导采样。

#### 模块四：MIS Sampling with GMM + BRDF（GMM与BRDF的多重重要性采样）

渲染时，在着色点处将经过视差补偿的GMM作为采样分布之一，与BRDF重要性采样通过MIS结合，以固定概率0.5选择其中一种策略。为保证无偏性，在GMM中额外加入一个覆盖整个半球面的保护性平滑瓣（protective smooth lobe），确保所有可能方向都有非零采样概率。

### 方法边界条件与限制

1. **粗糙度范围**：推荐α在0.005–0.05之间。α过大导致路径切割数量剧增（紧支撑角θ增大，更多节点通过有效性判据）；α过小（如0.001）且法向变化复杂时，SG近似和视差补偿精度不足（Figure 14失败案例）。
2. **反弹次数**：支持最多两次中间光泽反射（DSS和SDSS焦散）。更多次反射使路径切割数指数增长，预计算代价不可接受。
3. **材质限制**：仅支持反射焦散，未处理折射；假定每个物体具有恒定粗糙度，不支持粗糙度贴图。
4. **光源限制**：仅适用于点光源和小面积球面光源；环境光照仍由路径追踪处理。
5. **网格要求**：需要密集三角化网格以保证路径切割能捕获足够的代表性路径。

![[assets/figures/papers/paper_list_l96_https_wangningbei_github_io_2022_PathcutGuiding_html/figures/014_Figure_14.jpg]]
*Figure 14: Failure case of our method with equal time (7 minutes). When the reflector has complex normal variation and very small roughness (?? = 0.001), our method does not show much benefit*

## 实验与关键发现

### 主结果：等时渲染对比

本文在多个场景下进行了等时间渲染对比，所有对比均包含预计算时间，并使用相同硬件（4.20GHz Intel i7 8核，16GB内存）和一致图像分辨率。

**Snail 场景（Figure 1）**：在 20 分钟等时渲染下，本文方法 RMSE 为 **0.021**，显著低于 PT（0.073）、BDPT（0.066）和 PPG（0.036）。相比 PT 降低 71%，比 BDPT 降低 68%，比 PPG 降低 42%。该场景使用暗环境光加明亮点光源，预计算仅需 6.5 秒。放大区域仅用点光源渲染，本文方法视觉噪声最低，定量指标也最优。

**Musa 场景（Figure 9）**：12 分钟等时渲染，本文方法噪声最低且无萤火虫伪影，PT、BDPT、PPG 均存在明显噪声。预计算仅需 1.3 秒。

**与 SMS 对比（Figure 10）**：在 Bumpy Surface 场景（7 分钟等时），低粗糙度（α=0.005）下本文方法与 SMS 结果相近；当粗糙度升至 α=0.05 时，本文方法噪声远低于 SMS。这是因为 SMS 专为近镜面设计，粗糙度增大后采样效率急剧下降，而本文通过放宽路径切割判据和球面高斯近似，在该范围内保持了有效引导。

**与 SNEE 对比（Figure 11）**：Three Bumpy Cylinder 场景（12 分钟等时）展示了方法对多次反弹焦散的覆盖能力。SNEE 仅支持 DS（diffuse-specular）和 SDS（specular-diffuse-specular）焦散，而本文方法可额外渲染 DSS（diffuse-specular-specular）和 SDSS（specular-diffuse-specular-specular）焦散，捕获了 SNEE 缺失的能量路径。该场景使用三个凹凸圆柱反射器（α=0.01）置于光泽地板（α=0.01）上，预计算约 10 秒。

### 关键消融实验

**视差补偿的有效性（Figure 12）**：在等样本数（spp=16）条件下，对比有无视差补偿的结果。场景为环形体（α=0.005）置于地板（α=0.5）上，点光源照明。有视差补偿的结果噪声显著降低，验证了空间缓存后通过旋转 SG 中心方向校正视差的必要性——若不补偿，缓存点与着色点之间的几何偏移会导致采样分布偏离真实入射辐射方向，产生额外方差。

**Newton 求解器的作用（Figure 13）**：等时间（1 分钟）对比使用 Newton 求解器寻找代表性镜面路径与直接使用三角中心作为路径顶点。场景为球体（α=0.001）置于地板（α=0.5）上。Newton 求解器能大幅降低方差并减少内存开销。原因在于：三角中心未必位于满足镜面约束的路径上，导致 SG 近似的中心方向偏移，使 GMM 引导偏离目标分布；Newton 求解器通过最小化半向量与法线的差异，找到精确的代表性路径，从而保证引导精度。

### 失败案例与适用边界

**复杂法线变化 + 极低粗糙度（Figure 14）**：当反射器具有复杂法线变化且粗糙度极低（α=0.001）时，7 分钟等时渲染下本文方法未表现出明显优势。失败原因有两层：其一，极低粗糙度下 SG 近似的紧支撑角 θ 极小，路径切割数量剧增，预计算开销膨胀；其二，复杂法线变化使视差补偿精度不足，SG 旋转校正后的分布与真实入射辐射分布偏差较大，可能产生伪影。

**粗糙度适用范围**：推荐粗糙度范围为 **α ∈ [0.005, 0.05]**。α 过大时，路径切割数量指数增长，预计算代价不可接受；α 过小时，SG 近似和视差补偿的精度下降。

**反射次数限制**：方法支持最多两次中间光泽反射（即 DSS 和 SDSS 路径）。更多次反射会使路径切割数指数增长，计算代价高昂。

**光源与材质限制**：仅适用于点光源和小面积球形光源（环境光仍由 PT 处理）；仅支持反射焦散，未处理折射；假定每个物体具有恒定粗糙度，不支持粗糙度贴图；需要密集三角化网格以保证路径切割效率。

### 无偏性说明

渲染时在每个 GMM 中加入覆盖整个半球的保护性平滑瓣（protective smooth lobe），确保所有可能方向均可被采样，从而保证理论无偏性。但该策略的无偏性严格证明留待未来工作。

![[assets/figures/papers/paper_list_l96_https_wangningbei_github_io_2022_PathcutGuiding_html/figures/013_Figure_13.jpg]]
*Figure 13: Equal-time (1 minute) comparison of our methods with and without the Newton solver (i.e., using triangle centers as the vertices of representative path). This scene shows a sphere (?? = 0.001) on a floor (?? = 0.5) under a point light*

![[assets/figures/papers/paper_list_l96_https_wangningbei_github_io_2022_PathcutGuiding_html/figures/012_Figure_12.jpg]]
*Figure 12: Equal-sample (spp = 16) comparison of our methods with and without parallax compensation. This scene shows a ring (?? = 0.005) on top of a floor (?? = 0.5) under a point light*

![[assets/figures/papers/paper_list_l96_https_wangningbei_github_io_2022_PathcutGuiding_html/figures/006_Figure_6.jpg]]
*Figure 6: Comparison between our sampling distribution approximated by a SG and the target incident radiance distribution over the direction space at shading points. We mark out some unnoticeable details with white arrows. The target distribution shows that the shading points at the caustics have a high-frequency incoming radiance distribution. Our distribution shows the shape with some blurry of the target distribution. Please see the supplementary material for more discussions*

## 定位与知识库关联

本文在蒙特卡洛路径引导的知识谱系中，**改变了“入射辐射分布估计方法”这一核心 slot**：将路径引导从**在线迭代学习**（如 PPG 的 SD-tree）切换为**预计算代表性镜面路径 + 球面高斯（SG）链式近似 + 空间缓存与视差补偿**的代理方案。这一改变的因果机制在于：焦散路径的入射辐射分布本质上是高频且稀疏的，在线学习方法（**PPG**, Müller et al., 2017）需要大量样本才能捕获这些尖锐峰，而本文利用光泽反射器上“无穷多路径可被少量镜面路径代表”的物理洞察，将连续的光泽路径区域压缩为有限的高斯混合分布（GMM），从而在渲染前就完成了对入射辐射分布的高质量估计。

### 相对已有方法的本质差异

1. **相对于 PPG（在线路径引导）**：PPG 通过迭代构建空间-方向树来学习入射辐射场，对漫反射场景有效，但面对高频焦散时学习收敛慢、方差大。本文方法**不依赖在线学习**，而是通过预计算直接解析地构造采样分布，在等时渲染中 RMSE 降低 42%（Snail 场景，20 分钟），且预计算仅需 6.5 秒。

2. **相对于 SMS（Specular Manifold Sampling, Zeltner et al., 2020）**：SMS 在镜面流形上采样路径，对极低粗糙度（α ≈ 0.005）表现良好，但当粗糙度升高到 α = 0.05 时性能急剧下降。本文通过放宽路径切割条件（Eq. 1 的紧支撑角 θ），将方法适用范围扩展到中等粗糙度范围（推荐 α 0.005–0.05），在 α = 0.05 的 Bumpy Surface 场景中噪声远低于 SMS（Figure 10）。

3. **相对于 SNEE（Specular Next Event Estimation, Loubet et al., 2020）**：SNEE 仅支持 DS（漫反射-镜面）和 SDS（镜面-漫反射-镜面）两类焦散路径。本文方法额外支持 DSS 和 SDSS 路径（即允许两次中间光泽反射），捕获了 SNEE 缺失的能量（Figure 11），扩展了可渲染的焦散路径类型。

4. **相对于 Wang et al. 2020 的路径切割方法**：原方法仅适用于纯镜面（n·h = 1），本文通过引入粗糙度感知的紧支撑角阈值（Eq. 1）**放宽了路径切割的有效性判据**，使方法能够处理光泽表面，这是从“纯镜面”到“光泽反射器”的关键泛化。

### 知识库挂载点

本文在以下知识节点上建立连接：

- **路径切割框架**（Path Cuts, Wang et al., 2020）：继承其空间层级组织与路径切割搜索策略，但将纯镜面约束替换为粗糙度依赖的松弛条件（3.3 节）。
- **球面高斯近似**（SG, Laurijssen et al., 2010; Xu et al., 2014）：利用 SG 的乘积积分闭合形式（Eq. 5），链式累积沿代表性路径的辐射贡献，将 BRDF 切片和光源分别近似为 SG，再通过乘积积分得到着色点处的入射辐射 GMM。
- **多重重要性采样**（MIS, Veach & Guibas, 1995）：将预计算的 GMM 与 BRDF 重要性采样以固定概率 0.5 结合，保证无偏性（保护性平滑瓣策略的无偏性证明留待未来工作）。

### 适用边界与限制

本文方法存在明确的操作边界：

- **粗糙度范围**：推荐 α ∈ [0.005, 0.05]。粗糙度过大导致路径切割数量剧增、预计算代价不可接受；粗糙度过低（α = 0.001）且法线变化复杂时，SG 近似和视差补偿精度不足，出现伪影（Figure 14）。
- **反射次数**：最多支持两次中间光泽反射；更多次反射使路径切割数指数增长。
- **光源类型**：仅支持点光源和小面积球面光源，环境光仍由 PT 处理。
- **材质假设**：假定每个物体具有恒定粗糙度，不支持粗糙度贴图；仅处理反射焦散，未涉及折射。
- **网格要求**：需要密集三角化以保证路径切割效率。

### 后续工作启发

本文为焦散渲染的路径引导开辟了“预计算代理分布”的新范式，后续可沿以下方向扩展：

1. **扩展到折射焦散**：将代表性路径的构造逻辑从反射推广到折射，需要处理折射定律下的路径切割条件。
2. **支持非均匀粗糙度**：引入粗糙度贴图将显著增加路径切割的复杂度，可能需要结合空间变化的阈值策略。
3. **结合神经网络加速**：用学习模型替代 Newton 求解器寻找代表性路径，或直接预测 GMM 参数，可能降低预计算开销并扩展到大粗糙度场景。
4. **无偏性理论完善**：保护性平滑瓣策略的无偏性证明是理论上的遗留问题。

## 原文 PDF

![[paperPDFs/SIGGRAPH_ASIA_2022/Unbiased_Caustics_Rendering_Guided_by_Representative_Specular_Paths.pdf]]