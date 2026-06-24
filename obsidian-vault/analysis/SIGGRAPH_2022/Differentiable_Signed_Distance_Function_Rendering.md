---
title: Differentiable Signed Distance Function Rendering
type: paper
paper_level: A
venue: SIGGRAPH
year: 2022
pdf_ref: paperPDFs/SIGGRAPH_2022/Differentiable_Signed_Distance_Function_Rendering.pdf
project_link: "http://rgl.epfl.ch/publications/Vicini2022SDF"
code_link: "https://github.com/rgl-epfl/differentiable-sdf-rendering"
aliases:
- MSTIR
- DSDFR
tags:
- SIGGRAPH_2022
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
core_operator: 在球面追踪步骤中收集额外信息，构建一个三维向量场V，并将其映射为单位球面上的重新参数化T，该映射的导数准确地跟随可见性边界运动，从而消除积分中与参数相关的间断。
primary_logic: 利用SDF本身在球面追踪过程中产生的中间符号距离信息，可以零额外射线成本构建一个专门适用于隐式曲面的重新参数化，既能正确处理遮挡和自遮挡导数，又比以往的卷积方法更快、更准确。
claims:
- 提出的重新参数化方法在梯度图像上与有限差分参考高度一致，而直接AD无法得到可用梯度。
- 在相同迭代次数下，本方法重建精度最高且总运行时间最短，优于依赖辅助射线的卷积方法。
- 仅使用逐像素RGB损失，无需额外的轮廓或掩模监督，即可从多视图图像恢复复杂SDF几何与纹理。
- "Synthetic scenes: Shadowing, Logo, Bunny (translational motion gradients) 上 Gradient image accuracy (vs. finite difference reference) = Closely matches reference, sharp occlusion boundaries"
---

# Differentiable Signed Distance Function Rendering

> [!tip] 核心洞察
> 利用SDF本身在球面追踪过程中产生的中间符号距离信息，可以零额外射线成本构建一个专门适用于隐式曲面的重新参数化，既能正确处理遮挡和自遮挡导数，又比以往的卷积方法更快、更准确。

| 字段 | 内容 |
|------|------|
| 中文题名 | 可微符号距离函数渲染 |
| 英文题名 | Differentiable Signed Distance Function Rendering |
| 会议/期刊 | SIGGRAPH 2022 |
| Links | [paper](http://rgl.epfl.ch/publications/Vicini2022SDF) · [Code](https://github.com/rgl-epfl/differentiable-sdf-rendering) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction |
| Method | Modified Sphere Tracing with Implicit Reparameterization |
| Dataset | Synthetic scenes: Shadowing, Logo, Bunny, 3D reconstruction of Bunny, Dragon, Chair, Boar from ~32 views, Statue reconstruction from 32 views |

> [!tip] 效果简介
> - Synthetic scenes: Shadowing, Logo, Bunny (translational motion gradients) 上，Gradient image accuracy (vs. finite difference reference) Closely matches reference, sharp occlusion boundaries vs Convolution method (8–64 aux. rays) noticeably noisier or blurred (Higher accuracy with no auxiliary rays)。
> - 3D reconstruction of Bunny, Dragon, Chair, Boar from ~32 views 上，Reconstruction quality and total optimization time Most accurate surface details, shortest runtime vs Convolution method (8 aux. rays), comparable iterations (Better accuracy + significantly shorter runtime)。
> - Statue reconstruction from 32 views (Figure 1) 上，Visual quality after L1 minimization (no mask/silhouette loss) Faithful geometry and albedo recovery from RGB only vs No direct comparison on this scene, but prior SDF methods require silhouette su... (No need for mask or silhouette losses)。

## 概要

针对可微渲染中符号距离函数（SDF）的可见性导数计算难题，本文提出一种在球面追踪过程中动态构建隐式重参数化的方法。该方法利用SDF自身的梯度场构造三维向量场 $\mathcal{V}$，并将其映射为单位球面上的重参数化 $\mathcal{T}$，使得积分域随参数变化自动跟随遮挡边界移动，从而以零额外射线成本准确捕获可见性间断导数。在Mitsuba 2框架上实现后，梯度图像与有限差分参考高度吻合，而直接自动微分完全失效。在多视图三维重建任务中，仅使用逐像素RGB损失即可从约32张图像恢复复杂几何与纹理，无需额外的轮廓或掩模监督；与需要辅助射线的卷积方法相比，本方法在相同迭代次数下重建精度最高且总运行时间最短。该方法将可微SDF渲染的梯度估计从依赖大量辅助采样的卷积方案，推进为单次球面追踪即可完成的解析重参数化方案。

## 核心方法与创新机理

### 问题瓶颈：可见性间断的导数缺失

可微渲染的核心困难在于：像素强度是光线路径空间上的积分，当场景参数变化导致物体的可见性边界（遮挡轮廓、自遮挡）移动时，被积函数在单位球面上产生与参数相关的间断。直接对该积分使用自动微分（AD）会丢失边界移动带来的梯度贡献，导致梯度严重偏置甚至完全错误。以往针对三角网格的卷积方法（Bangaru et al., 2020）通过沿每条光线追踪数十条辅助射线来“模糊”边界以近似散度定理，但将其适配到SDF时不仅计算开销大，且未充分利用SDF本身的隐式特性。

本工作的核心瓶颈在于：**SDF渲染使用球面追踪（sphere tracing）求交，该过程天然产生丰富的中间符号距离信息，但此前无人将其转化为处理可见性间断的梯度信息**。作者的关键洞察是：球面追踪沿途评估的SDF值和梯度，恰好可以零额外射线成本地构建一个三维向量场，进而构造单位球面上的重新参数化，使边界导数被准确捕获。

### 核心机制：从向量场到球面重新参数化

方法的理论根基是重新参数化（reparameterization）技术。对于单位球面上的积分 $I(\pi) = \int_{S^2} f(\omega, \pi) \, d\omega$，若存在映射 $\mathcal{T}: S^2 \to S^2$ 使得对所有间断方向 $\omega_b$ 满足 $\partial_\pi \mathcal{T}(\omega_b, \pi) = \partial_\pi \omega_b$（即重新参数化在边界处精确跟随边界运动），则可通过变量替换将间断“吸收”进映射，从而在变换后的积分上安全地交换微分与积分次序。变换引入的面积扭曲由 $\mathcal{T}$ 的雅可比行列式（等价于散度）补偿。

本方法的核心贡献在于：**如何为SDF隐式曲面自动构造这样一个 $\mathcal{T}$，且构造过程几乎无额外开销**。

#### 三维向量场 $\mathcal{V}$ 的构造

定义辅助向量场：

$$\mathcal{V}(\mathbf{x}, \pi) = - \frac{\partial_{\mathbf{x}} \phi(\mathbf{x}, \pi_0)}{\lVert \partial_{\mathbf{x}} \phi(\mathbf{x}, \pi_0) \rVert^2} \, \phi(\mathbf{x}, \pi)$$

其中 $\phi$ 为SDF，$\pi_0$ 为当前参数值（被detach），$\pi$ 为可微参数。该设计的精妙之处在于：

- **在零等值面 $\phi=0$ 上**，$\mathcal{V}$ 的参数导数 $\partial_\pi \mathcal{V}$ 精确等于表面点的参数运动速度 $\partial_\pi \mathbf{x}_{\text{surface}}$。这可由隐函数定理和程函方程 $\lVert \partial_{\mathbf{x}} \phi \rVert = 1$ 推导得出。
- **分母中的 $\lVert \partial_{\mathbf{x}} \phi(\mathbf{x}, \pi_0) \rVert^2$ 归一化项**是关键细节：当SDF存储于体素网格并使用B样条插值时，插值后的场并不严格满足程函方程，梯度范数偏离1。若不归一化，边界梯度的幅度会失真；归一化后显著提高了低分辨率网格上的梯度准确性（见消融实验Figure 4）。

#### 球面重新参数化 $\mathcal{T}$ 的构建

在球面追踪的每一步，光线沿方向 $\omega$ 行进距离 $t$ 到达点 $\mathbf{x}_t$。利用 $\mathcal{V}$，定义辅助方向：

$$\bar{\mathcal{T}}(\omega, \pi) = t\omega + \mathcal{V}(\mathbf{x}_t, \pi) - \mathcal{V}(\mathbf{x}_t, \pi_0)$$

其直观含义是：将光线终点位置 $\mathbf{x}_t = t\omega$ 加上向量场在参数 $\pi$ 和 $\pi_0$ 处的差异，得到一个“偏移后”的方向向量。归一化后得到单位球面上的重新参数化：

$$\mathcal{T}(\omega, \pi) = \frac{\bar{\mathcal{T}}(\omega, \pi)}{\lVert \bar{\mathcal{T}}(\omega, \pi) \rVert}$$

该映射的关键性质是：**其参数导数在切空间上的投影精确跟随可见性边界的运动**。具体地，可证明：

$$\partial_\pi \mathcal{T}(\omega, \pi) = \frac{1}{t} (\mathbb{I} - \omega\omega^T) \, \partial_\pi \mathcal{V}(\mathbf{x}_t, \pi)$$

即导数是 $\partial_\pi \mathcal{V}$ 在垂直于 $\omega$ 的切平面上的投影，并缩放 $1/t$。当 $\mathbf{x}_t$ 位于表面附近时，$\partial_\pi \mathcal{V}$ 匹配表面运动，因此 $\partial_\pi \mathcal{T}$ 在边界方向 $\omega_b$ 上恰好等于 $\partial_\pi \omega_b$，满足重新参数化的核心要求。

### 模块顺序与训练/推理路径

方法以修改后的球面追踪为核心，形成如下管道：

1. **Modified Sphere Tracing**：在标准球面追踪求交的同时，额外记录一个“评估距离” $t_{\text{eval}}$。该距离并非光线与表面的真实交点距离，而是通过加权球面追踪中间点的SDF值构造的一个平滑距离函数，其设计保证了在掠射角方向不会退化（通过 $w_{\text{dist}}$ 权重因子，见Figure 6消融），且在远离表面时连续衰减。

2. **3D Vector Field $\mathcal{V}$ 构造**：利用SDF值及其空间梯度（在 $\pi_0$ 处detach），按上述公式计算 $\mathcal{V}$。该向量场在表面零等值面上编码了表面的参数运动信息。

3. **Reparameterization on the Unit Sphere**：在 $t_{\text{eval}}$ 处计算 $\bar{\mathcal{T}}$ 并归一化得到 $\mathcal{T}$，同时计算其雅可比迹（等价于散度）作为面积扭曲因子。

4. **Gradient Backpropagation**：在Mitsuba 2的反向模式自动微分框架中，将重新参数化后的方向 $\mathcal{T}(\omega, \pi)$ 用于着色计算，并将面积扭曲因子乘入梯度，从而将像素损失正确传递至SDF的体素参数。

**嵌套重新参数化**：当场景包含阴影射线（如直接光照）时，主射线和阴影射线各自产生间断，必须正确处理嵌套关系。若简单地将阴影射线原点detach或忽略主射线重新参数化对阴影射线起点的影响，会导致阴影边界的梯度错误（见Figure 7消融）。正确做法是让主射线的重新参数化影响阴影射线起点的位置，再对阴影射线独立应用其自身的重新参数化。

### Changed Slots：与基线的本质差异

| 维度 | 卷积方法（Bangaru et al.） | 本方法 |
|------|--------------------------|--------|
| **可见性间断处理** | 在球域上对多条辅助射线进行卷积，用散度定理近似边界导数 | 在球面追踪中自动构建重新参数化 $\mathcal{T}$，解析地跟随边界运动 |
| **辅助射线需求** | 每条光线需额外追踪8–64条辅助射线 | **零辅助射线**，所有信息源自球面追踪本身的中间SDF评估 |
| **对近似SDF的鲁棒性** | 依赖SDF梯度范数=1的假设，插值网格下边界梯度幅度不准 | $\mathcal{V}$ 中显式除以 $\lVert \partial_{\mathbf{x}} \phi \rVert^2$ 归一化，低分辨率网格下仍准确 |

### 关键公式变量含义速查

- $\phi(\mathbf{x}, \pi)$：参数 $\pi$ 下的SDF值，正值为外部，负值为内部
- $\pi_0$：当前参数值，在 $\mathcal{V}$ 的梯度分母中被detach，提供静态的几何参考
- $\mathcal{V}(\mathbf{x}, \pi)$：辅助向量场，沿SDF梯度方向缩放，在零等值面上其参数导数=表面运动速度
- $\bar{\mathcal{T}}$：偏移方向向量，编码了参数变化导致的“等效观测方向”变化
- $\mathcal{T}$：$\bar{\mathcal{T}}$ 的单位球面归一化，是最终的重新参数化映射
- $t_{\text{eval}}$：评估距离，通过加权球面追踪中间点构造，决定重新参数化的作用范围
- $w_{\text{dist}}$：权重因子，防止评估距离在掠射角方向趋近于零

### 因果链条总结

**SDF的隐式距离场** $\rightarrow$ **球面追踪产生中间SDF值和梯度** $\rightarrow$ **构造向量场 $\mathcal{V}$（零额外射线成本）** $\rightarrow$ **通过 $\mathcal{V}$ 的差异偏移构造球面重新参数化 $\mathcal{T}$** $\rightarrow$ **$\partial_\pi \mathcal{T}$ 在边界处精确匹配边界运动** $\rightarrow$ **重新参数化后的积分可安全微分** $\rightarrow$ **梯度经面积扭曲因子校正后反向传播至SDF体素** $\rightarrow$ **仅用RGB损失即可优化几何与纹理，无需掩模监督**。

![[assets/figures/papers/paper_list_l23_http_rgl_epfl_ch_publications_Vicini2022SDF/figures/002_Figure_2.jpg]]
*Figure 2: Illustration of a discontinuous integrand on the unit sphere S2. (a) We integrate the color of a shaded shape over a constant-colored background. The scene parameter ?? controls the translation of the object. (b) We then introduce a reparameterization T, which is designed so that the vector field*

## 实验与关键发现

### 梯度准确性验证

本方法的核心主张是“零辅助射线即可获得准确的可见性梯度”，因此梯度图像与有限差分参考的对比是最直接的验证。在三个合成场景（Shadowing、Logo、Bunny）上，将物体做平移运动，计算渲染图像对该平移参数的梯度。**Figure 8** 展示了本文方法、有限差分参考（ground truth）以及卷积方法（Bangaru et al., 2020）的梯度图像对比。结果表明，本文方法在遮挡边界处产生清晰锐利的梯度，与有限差分参考高度吻合；而卷积方法即使使用 8–64 条辅助射线，梯度仍存在明显噪声或模糊。直接使用自动微分（AD）而不处理可见性间断的方法，则完全无法获得可用的梯度图像——其梯度在遮挡边界处完全缺失关键贡献。

![[assets/figures/papers/paper_list_l23_http_rgl_epfl_ch_publications_Vicini2022SDF/figures/009_Figure_8.jpg]]
*Figure 8: We compare the gradients obtained using our method to the ground truth and an SDF version of the convolution method by Bangaru et al [2020]. The gradient images are computed by using forward-mode differentiation with respect to a translation of the entire object. For the convolution method, we show the results using varying numbers of auxiliary rays estimating the convolution integral. Increasing the number of rays improves the accuracy of the gradient estimate, at the cost of increased computation time. All gradient images are rendered using 1024 samples per pixel. The Shadowing and Logo scene are using direct illumination, and the Bunny scene is rendered with one bounce of indirect illumi...*

**关键数值事实**：所有梯度图像均使用每像素 1024 采样（spp）渲染，本文方法无需任何辅助射线即可匹配参考精度，而卷积方法在 8 条辅助射线时梯度噪声显著，64 条辅助射线时仍有残留模糊。

### 多视图三维重建对比

在 Bunny、Dragon、Chair、Boar 四个复杂物体上，使用约 32 个视角的参考图像进行 SDF 几何与纹理联合优化。**Figure 11** 给出了本文方法与卷积方法在相同迭代次数下的重建质量与总运行时间对比。核心发现：

![[assets/figures/papers/paper_list_l23_http_rgl_epfl_ch_publications_Vicini2022SDF/figures/012_Figure_11.jpg]]
*Figure 11: We compare the reconstruction results using our reparameterization and the convolution method [Bangaru et al. 2020] at equal iteration count. Increasing the number of samples to estimate the convolution integral improves the quality of results, but at the cost of drastically increasing the total time for the optimization. Our method both results in the most accurate reconstruction and the shortest runtime*

- **重建精度**：本文方法恢复的表面细节最丰富、最准确，尤其在 Dragon 的鳞片、Chair 的镂空结构等细粒度几何上优势明显。
- **运行时间**：本文方法总优化时间最短。卷积方法增加辅助射线数量（8 → 16 → 32）虽能改善重建质量，但运行时间急剧增长；本文方法在无辅助射线的前提下同时实现了最高精度和最短耗时。
- **公平性说明**：所有对比使用相同的超参数（权重 β、ε 等），未针对不同场景单独调参。优化总时间包含渲染与每步 SDF 重新距离化（redistancing）的开销，公平记录于 Figure 9(b) 中。

**Figure 12** 进一步分析了视角数量对重建鲁棒性的影响。当参考视角减少时，两种方法的重建质量均下降，但本文方法在低视角数条件下仍保持相对更稳定的几何一致性（通过多组随机视角的平均渲染模糊程度衡量）。

### 关键消融实验

**1. 向量场归一化项（Figure 4）**

向量场 V 的定义中除以 SDF 梯度范数的平方（Equation 9），是处理近似 SDF（如低分辨率网格 B 样条插值）的关键。Figure 4 显示：当不包含该归一化项时，边界梯度的幅值与有限差分参考存在明显偏差；加入归一化后梯度准确度显著提高。随着 SDF 网格分辨率增加，插值 SDF 更接近真实 SDF（梯度范数趋近于 1），归一化的作用逐渐减弱——这反向验证了该设计针对非理想 SDF 表示的必要性。

![[assets/figures/papers/paper_list_l23_http_rgl_epfl_ch_publications_Vicini2022SDF/figures/005_Figure_4.jpg]]
*Figure 4: We visualize the gradients of a rendered image with respect to a vertical translation of an object represented as an SDF. If we do not include the normalization term described in Equation 9, the magnitude of the gradient (middle column) does not quite match the reference. Including the normalization improves the accuracy of the estimated silhouette gradients (right). As the SDF grid resolution is increased (y-axis), the interpolated SDF more closely matches a true SDF, and the effect of the normalization is less pronounced*

**2. 评估距离的权重因子 w_dist（Figure 6）**

球面追踪过程中构建的评估距离函数若不加 w_dist 权重，在掠射出射方向（grazing outgoing directions）会趋近于零，导致重新参数化在远处边界失效。加入 w_dist 后，评估距离在掠射方向保持合理衰减，确保重参数化映射在单位球面上连续覆盖所有可见性边界。

**3. 主/阴影射线嵌套重参数化（Figure 7）**

当场景包含阴影射线时，重参数化需要正确嵌套：若完全 detach 阴影射线原点（Figure 7a），或未追踪主射线重参数化对阴影射线的影响（Figure 7b），都会产生错误的阴影梯度。只有同时正确处理主射线和阴影射线的重参数化链式依赖，才能得到与参考一致的阴影边界梯度（Figure 7c vs. 7d）。这一消融揭示了该方法在全局光照场景中正确实施的工程复杂性。

**4. 次级光照梯度（Figure 13）**

引入间接光照（二次反弹）的梯度信息，在观测视角稀少时（如单视图重建）能显著改善重建质量。Figure 13 中，不使用次级梯度的重建在遮挡区域出现明显几何偏差，加入次级梯度后恢复出更准确的表面形状。这表明当直接可见性信息不足时，间接光照的微分信号提供了有价值的补充约束。

**5. 梯度方差降低（Figure 14）**

低采样率（4 spp）下，梯度图像存在显著噪声。采用可微像素权重归一化（differentiable pixel filter weight normalization）或对立采样（antithetic sampling）均可有效降低梯度方差，且前者效果略优于后者。这一消融为实际优化中的采样效率提供了实用指导。

**6. 忽略可见性间断的后果（Figure 15）**

完全忽略可见性间断导数（即仅对着色项求导），梯度图像严重偏置——遮挡边界处的梯度贡献完全缺失。将这种有偏梯度用于优化，几乎必然导致发散：Figure 15 底部行展示的优化结果中，物体形状完全崩溃。这从根本上论证了处理可见性间断对于可微 SDF 渲染的必要性。

### 失败模式与适用边界

**非凸优化的局部极小值（Figure 16）**

当场景包含复杂拓扑和空间变化的 albedo 纹理时，SDF 联合优化问题高度非凸。Figure 16 展示了一个典型案例：使用 40 张输入图像、256³ 分辨率优化 SDF 和 albedo 纹理，结果陷入不良局部极小值——几何表面出现虚假凹凸，纹理与几何相互“欺骗”以降低渲染损失。这是本方法在复杂真实场景中面临的核心挑战。

**其他已声明的局限**（未全部配图验证）：

- 每步优化后需显式重新距离化 SDF，高分辨率网格下计算开销较大（Figure 9b 给出了不同分辨率下的 redistancing 时间基准）。
- 当前仅适用于单一 SDF 几何表示，无法处理混合几何表示（如三角网格遮挡 SDF）。
- 不支持通过完美镜面反射/折射路径看到的物体边界不连续性，难以处理焦散等效应。
- 重参数化策略目前仅适用于单向路径追踪，推广到全路径空间需要更深入的理论拓展。

**适用边界总结**：本方法在以下条件下表现最优——(a) 场景几何可用单一 SDF 表示；(b) 光照以直接光照和漫反射间接光照为主，不含大量镜面反射/折射路径；(c) 输入视图数量充足（≥32 视角）；(d) 几何拓扑不过于复杂。当这些条件不满足时，非凸优化的局部极小值问题和理论适用范围限制将成为主要瓶颈。

![[assets/figures/papers/paper_list_l23_http_rgl_epfl_ch_publications_Vicini2022SDF/figures/007_Figure_7.jpg]]
*Figure 7: This figure shows the subtleties of nesting reparameterizations. We render the same object from two different viewpoints and compute gradients with respect to a translation. If we fully detach the origin x of the shadow ray (a) the result is wrong. If we do not track the effect of the reparameterization of the primary rays, we also get wrong results (b). Only if we carefully account for these effects we get output (c) that matches the reference (d)*

![[assets/figures/papers/paper_list_l23_http_rgl_epfl_ch_publications_Vicini2022SDF/figures/008_Figure_6.jpg]]
*Figure 6: We compare the evaluation distance function ?? with and without the ??dist factor. Without this factor, the evaluation distance approaches zero for grazing outgoing ray directions. Including ??dist reduces the influence of the surface at the ray origin on the evaluation distance. This also implies that the evaluation distance is undefined for rays that never approach a surface, and we need to make sure our reparameterization continuously goes to zero before reaching this case*

## 定位与知识库关联

本文解决的核心问题是**可微SDF渲染中参数相关的可见性间断导数**。在可微渲染的知识谱系中，该问题处于“隐式几何表示的可微绘制”与“边界梯度估计”的交汇点。此前，针对三角网格的重新参数化方法（如 Loubet et al., 2019; **Bangaru et al., 2020**）已证明：通过构造一个跟随遮挡边界运动的重参数化映射，可以在无需显式采样边界的情况下获得准确的可见性梯度。然而，这些方法依赖于显式的表面表示（三角网格）来获取边界位置信息，当直接迁移到SDF时，需要沿每条光线追踪多条辅助射线来在球域上做卷积去噪，计算代价高昂。

**改变的 slot** 在于**可见性间断处理的信息来源与计算路径**：
- **基线（Bangaru et al., 2020 的卷积方法）**：需要额外的辅助射线在单位球面上采样周围环境，以“发现”遮挡边界的位置。这是一个外部的、基于采样的边界感知机制，精度与辅助射线数量正相关，但计算开销随射线数线性增长。
- **本文方法**：将边界感知机制**内化到球面追踪过程本身**。通过利用SDF在求交过程中自然产生的中间符号距离值，构建一个三维向量场 $\mathcal{V}$ 并将其映射为单位球面上的重参数化 $\mathcal{T}$。该重参数化的参数导数 $\partial_\pi \mathcal{T}$ 精确跟随可见性边界运动，且**不需要任何辅助射线**。这一 slot 的改变使得梯度估计从“采样-卷积”范式转变为“解析-追踪”范式。

**知识库挂载点**：
1. **可微渲染的边界梯度理论**：本文与 Bangaru et al. (2020) 共享相同的数学框架——将单位球面积分的参数导数通过重参数化转化为对连续被积函数的积分加上一个面积扭曲项（等价于散度）。本文的贡献在于为SDF专门设计了一个满足边界匹配条件的重参数化 $\mathcal{T}$，其构造完全基于SDF本身的梯度场和距离值，无需外部几何信息。
2. **球面追踪（Sphere Tracing, Hart 1996）**：本文方法是对经典球面追踪算法的一个轻量级增强——在步进过程中额外记录加权距离和中间点，以零额外射线成本构建重参数化。这为隐式几何的可微渲染提供了一个“原生”的梯度计算方案。
3. **SDF的度量性质**：方法利用了SDF的 eikonal 方程 $\|\partial_{\mathbf{x}} \phi\| = 1$ 来保证向量场 $\mathcal{V}$ 在表面处的导数恰好匹配表面运动。当SDF由体素网格插值近似时，梯度范数偏离1，本文通过除以梯度范数平方的归一化项来补偿这一偏差（Equation 9），使得方法对低分辨率SDF网格仍保持较好的梯度准确性。

**适用边界**：
- **几何表示**：当前方法仅适用于单一SDF表示的场景，不能直接处理多种几何表示混合的情况（例如三角网格遮挡SDF）。
- **光传输范围**：重参数化目前仅适用于单向路径追踪。对于通过完美镜面反射/折射看到的物体边界不连续性，以及焦散等效应，方法尚不支持。将推导推广到完整路径空间需要进一步的理论拓展。
- **优化稳定性**：SDF优化过程本身高度非凸，当场景包含精细细节或复杂拓扑时，可能陷入不良局部极小值（Figure 16）。此外，每步优化后需要显式重新距离化SDF，对于高分辨率网格计算开销较大（Figure 9b）。
- **输入需求**：方法仅需逐像素RGB损失即可驱动重建，无需额外的轮廓或掩模监督。但实验均在已知环境光照的条件下进行。

**后续启发**：
1. **稀疏SDF结构**：如何将本重参数化策略与稀疏体素八叉树等自适应数据结构结合，以支持大规模场景的高效优化，是一个自然的扩展方向。
2. **三角网格的方差降低**：本文方法在SDF上实现了无需辅助射线的低方差梯度估计。类似的“内部化边界感知”思路能否应用到三角网格上，以减少现有重新参数化方法的梯度方差和偏差，值得探索。
3. **正则化与非凸优化**：针对SDF几何优化设计更有针对性的正则化方法（如曲率先验、拓扑约束），以缓解非凸性带来的局部极小值问题，是提升重建鲁棒性的关键。
4. **全路径空间推广**：将导数的推导由单位球面推广至完整的路径空间，以支持间接光照下的遮挡边界导数和更复杂的全局光传输效应，是该方法走向通用可微渲染的重要理论步骤。

## 原文 PDF

![[paperPDFs/SIGGRAPH_2022/Differentiable_Signed_Distance_Function_Rendering.pdf]]