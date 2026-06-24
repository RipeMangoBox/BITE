---
title: A Generalized Ray Formulation For Wave-Optical Light Transport
type: paper
paper_level: A
venue: SIGGRAPH ASIA
year: 2024
pdf_ref: paperPDFs/SIGGRAPH_ASIA_2024/A_Generalized_Ray_Formulation_For_Wave_Optical_Light_Transport.pdf
project_link: "https://ssteinberg.xyz/2023/03/27/rtplt/"
code_link: null
aliases:
- GRBLTSS
- GRFWOLT
tags:
- SIGGRAPH_ASIA_2024
- topic/other_unclear
core_operator: 广义射线（generalized ray），一种相空间中的最小不确定度高斯基函数，其弱局域性完全由探测器的角度/空间敏感度和感测波长决定，与光的相干属性无关，从而在向后路径追踪时无需对光相干性做任何假设。
primary_logic: 经典光电探测器直接测量的是Husimi Q分布——即Wigner分布与探测态（最小不确定度高斯基）的卷积；因此，从传感器反向传播这些高斯基（广义射线）可以保持线性叠加与弱局域性，并导出精确的向后光传输方程，进而在采样阶段彻底解耦光传输与光的相干性。
claims:
- 在CD场景中，广义射线采样相比部分相干采样（类似PLT），在达到同等质量时所需的样本数减少了约4000倍。
- 与PLT双向路径追踪相比，本方法在CD场景的衍射区域实现了约1000–10 000倍的收敛加速。
- 即使在考虑GPU加速优势后，等样本数的收敛性能仍比PLT提高1–8倍，验证了算法层面的改进。
- Snake enclosure 上 Frame time (1 spp) = 116 ms
---

# A Generalized Ray Formulation For Wave-Optical Light Transport

> [!tip] 核心洞察
> 经典光电探测器直接测量的是Husimi Q分布——即Wigner分布与探测态（最小不确定度高斯基）的卷积；因此，从传感器反向传播这些高斯基（广义射线）可以保持线性叠加与弱局域性，并导出精确的向后光传输方程，进而在采样阶段彻底解耦光传输与光的相干性。

| 字段 | 内容 |
|------|------|
| 中文题名 | 波光学光传输的广义射线公式 |
| 英文题名 | A Generalized Ray Formulation For Wave-Optical Light Transport |
| 会议/期刊 | SIGGRAPH ASIA 2024 |
| Links | [paper](https://ssteinberg.xyz/2023/03/27/rtplt/) |
| Topic | #topic/other_unclear |
| Method | Generalized Ray Backward Light Transport (sample–solve) |
| Dataset | Snake enclosure, CD scene |

> [!tip] 效果简介
> - Snake enclosure 上，Frame time (1 spp) 116 ms vs N/A (N/A)。
> - CD scene (diffraction grating) 上，Sample count for equal quality 1× (reference) vs ~4000× (~4000× reduction)。
> - CD scene (diffractive regions) 上，Convergence speed-up 1000–10,000× faster vs PLT BDPT (Steinberg et al. 2022) (1000–10,000×)。

## 概要

在波光学渲染中，从传感器向后追踪光路时，由于无法预知光的相干性，重要性采样所用的BSDF与实际观测到的BSDF严重不匹配——这一“采样问题”导致间接光照下衍射材料的收敛极其缓慢。本文提出**广义射线**（generalized ray）：一种相空间中的最小不确定度高斯基函数，其弱局域性完全由探测器的角度/空间敏感度和感测波长决定，与光的相干属性无关。基于“经典光电探测器直接测量的是Husimi Q分布”这一核心洞察，作者构建了从传感器反向传播广义射线的**sample–solve**框架：采样阶段以相干无关的方式追踪光路，求解阶段再沿已采样路径正向重追踪以精确计算部分相干效应。该方法在CD场景的衍射区域实现了相比部分相干采样约4000倍的样本数缩减，相比PLT双向路径追踪达到1000–10 000倍的收敛加速，即使在考虑GPU硬件优势后等样本收敛性能仍提升1–8倍。该框架将传统射线追踪器扩展至波光学仅需少量改动，并支持交互式渲染。

## 核心方法与创新机理

### 问题瓶颈：向后波光学传输中的“采样问题”

在波光学渲染中，从传感器向光源反向追踪光路时，渲染器面临一个根本性障碍——**采样问题**（sampling problem）。经典路径追踪依赖BSDF进行重要性采样以引导光线方向，但在波光学场景中，光的相干属性（即波前之间的干涉能力）在反向追踪时是未知的。这导致渲染器使用的采样BSDF与实际观测到的BSDF之间存在严重不匹配：采样BSDF可能包含宽大的衍射瓣，而实际观测中由于光的部分相干性，只有极窄的瓣可见。这种不匹配使得重要性采样效率极低，尤其在**间接光照照射衍射材料**时，收敛极其缓慢。

图1直观展示了这一问题：铝制划痕飞船模型的渲染中，若积分区域（integration patch）过小，波干涉效应完全消失，仅呈现几何光学外观；随着积分区域增大，正确的波效应逐渐显现，但继续增大时外观不再变化，而BSDF瓣的形状却持续改变（见对数坐标的BSDF可视化）。这意味着渲染器用于重要性采样的BSDF与观测BSDF显著偏离，导致采样效率崩溃。

### 核心洞察：探测器直接测量的是Husimi Q分布

本方法的核心洞察来自量子光学中光电探测的物理本质：**经典光电探测器直接测量的并非Wigner分布函数（WDF），而是Husimi Q分布**。具体而言，探测器可探测的量子态是相干态（coherent states），即最小不确定度的高斯波包。因此，探测器的WDF可写为这些最小不确定度高斯的叠加：

$$I = \int \mathrm{d}\vec{r}' \mathrm{d}\vec{k}' \mathcal{W}(\vec{r}', \vec{k}') \mathcal{W}_d(\vec{r}', \vec{k}')$$

其中 $\mathcal{W}$ 是光的Wigner分布，$\mathcal{W}_d$ 是探测器的Wigner分布。测量强度是二者在相空间的重叠积分。这一事实意味着：**从传感器反向传播这些探测态（最小不确定度高斯基），可以保持线性叠加与弱局域性，并导出精确的向后光传输方程**。在采样阶段，光传输与光的相干性被彻底解耦——因为探测态的参数（空间/角度方差）完全由探测器的敏感度和感测波长决定，与场景中光的相干属性无关。

### 核心原语：广义射线（Generalized Ray）

基于上述洞察，作者提出**广义射线**作为波光学光传输的基本原语。在相空间中（位置 $\vec{r}$ 与波矢 $\vec{k}$ 的联合空间），经典射线是一个Dirac δ函数点——其位置和方向完全确定，但这在波光学中是被不确定性原理所禁止的。广义射线是经典射线与最小不确定度高斯的卷积，其Wigner分布为：

$$g_{\beta,\rho}(\vec{r}, \vec{k}; \vec{r}_0, \vec{k}_0) \triangleq \frac{1}{\pi^3} \exp\left[ -\frac{1+\rho^2}{\beta^2} |\vec{r}-\vec{r}_0|^2 - \beta^2 |\vec{k}-\vec{k}_0|^2 \right] \times \exp\left[ 2\rho |\vec{r}-\vec{r}_0| |\vec{k}-\vec{k}_0| \right]$$

其中参数 $\beta$ 控制空间方差与波矢方差之间的权衡（$\beta$ 越大，空间局域性越强但方向局域性越弱），$\rho$ 编码自由空间传播诱导的位置-波矢相关性。对应的波函数是一个最小不确定度的高斯波包：

$$\psi_{\beta,\rho}(\vec{r} | \vec{r}_0, \vec{k}_0) \triangleq \left(\frac{1}{\pi\beta^2}\right)^{3/4} \mathrm{e}^{\mathrm{i}\vec{k}_0 \cdot (\vec{r} - \vec{r}_0)} \mathrm{e}^{-\frac{1}{2\beta^2}(1 - \mathrm{i}\rho) |\vec{r} - \vec{r}_0|^2}$$

广义射线的**弱局域性**是其关键属性：它在相空间中占据一个最小不确定度单元（满足不确定性关系的最小方差高斯），既非完全局域（如经典射线），也非完全非局域（如平面波）。这一局域性完全由探测器的角度/空间敏感度和感测波长决定，与光的相干属性无关。

### Changed Slots：三个关键替换

与现有波光学渲染方法相比，本方法在三个关键维度上进行了替换：

**1. 光传输原语：经典射线 → 广义射线**

基线方法（如PLT的前向路径追踪）使用经典射线（空间点采样）作为传输原语，这要求预先知道光的相干性以确定波前积分区域。本方法将原语替换为相空间中的最小不确定度高斯基函数，其空间/角度范围由探测器参数 $\beta$ 和传播参数 $\rho$ 精确量化，无需对光相干性做任何假设。

**2. 采样策略：部分相干BSDF采样 → 相干无关采样**

基线方法（如PLT的向后路径追踪）必须基于全局相干性下界设计部分相干（partially-coherent, PC）BSDF进行采样，这直接导致采样问题。本方法使用广义射线进行**相干无关采样**（coherence-agnostic sampling）——在sample pass阶段，广义射线被视为完全相干的，因此可以应用传统路径追踪的所有重要性采样技术（俄罗斯轮盘、下一事件估计、流形采样等），而无需考虑光的实际相干状态。

**3. 测量/积分方式：前向Wigner传播 → 反向探测态传播**

基线方法沿前向传播Wigner分布并在检测器端积分。本方法改为**反向传播探测态**（即广义射线），通过时间反演动力学将探测态传播至光源，再与光源Wigner分布积分获得测量强度。这一反转使得采样可以从传感器端发起，同时保持波光学精度。

### 算法框架：Sample–Solve两阶段策略

本方法的算法框架采用**sample–solve**两阶段策略，由四个核心模块组成：

**模块1：探测器状态采样（Detector State Sampling）**

从探测器的敏感度分布中采样广义射线的初始参数：位置 $\vec{r}_0$、波矢 $\vec{k}_0$、空间方差参数 $\beta$ 和相关性参数 $\rho$。这些参数完全由探测器的物理特性（像素位置、孔径大小、感测波长）决定，与场景光照无关。

**模块2：反向路径追踪——Sample Pass**

使用广义射线在场景中反向追踪光路。在此阶段，广义射线被视为**完全相干**的波包，因此可以忽略部分相干效应，直接应用传统路径追踪的所有重要性采样技术：
- 俄罗斯轮盘（Russian roulette）用于路径终止
- 下一事件估计（next event estimation, NEE）用于直接连接光源
- 流形采样（manifold sampling）用于穿越介质界面和衍射光栅的镜面路径

这一阶段解决了采样问题的核心矛盾：因为广义射线的局域性由探测器决定而非光相干性决定，采样BSDF与实际观测BSDF不再存在系统性偏差。图7的对比实验表明，仅这一替换就使达到同等质量所需的样本数减少了约**4000倍**。

**模块3：PLT Solve Pass**

沿sample pass采样的光路进行**正向重追踪**，利用PLT（Physical Light Transport）精确计算部分相干效应。这一阶段作为降方差技术：sample pass提供了高质量的路径样本，solve pass在这些路径上应用完整的波光学BSDF（包含相干性、偏振等效应），纠正sample pass中因忽略部分相干性而引入的近似。注意sample pass中为简化实现而忽略的偏振效应，在此阶段得到完整纠正。

**模块4：测量算子（Measurement Operator）**

将到达光源处的广义射线与光源的Wigner分布进行相空间积分，获得该路径的最终强度估计。这一积分形式为：

$$I = \int \mathrm{d}\vec{r} \mathrm{d}\vec{k} \, \mathcal{W}_{\text{source}}(\vec{r}, \vec{k}) \, g_{\beta,\rho}(\vec{r}, \vec{k}; \vec{r}_0, \vec{k}_0)$$

其中 $g_{\beta,\rho}$ 是经过场景所有交互（反射、折射、衍射）后传播至光源处的广义射线Wigner分布。

### 关键公式与因果关系

**Wigner分布函数（WDF）** 是波光学光传输的数学基础，描述光波函数在相空间的联合位置-动量分布：

$$\mathcal{W}(\vec{r}, \vec{k}) \triangleq \frac{1}{(2\pi)^3} \int \mathrm{d}\vec{r}' \psi^\star(\vec{r} - \frac{1}{2}\vec{r}') \psi(\vec{r} + \frac{1}{2}\vec{r}') \mathrm{e}^{-\mathrm{i}\vec{r}' \cdot \vec{k}}$$

WDF的双线性使得它能够编码相干干涉效应（交叉项），但也使得直接将其作为传输原语时面临非局域性问题。

**向后波光传输的渲染方程**是本方法的核心理论贡献，描述了在时间反演动力学下，探测态经过场景相互作用算子后产生的输出Husimi分布：

$$\mathcal{Q}_o|_{\vec{r}_0} = \int \mathrm{d}\vec{k}_0 \mathrm{d}\beta \mathrm{d}\rho \, \mathcal{K}_r^\dagger \left\{ g_{\beta,\rho}(\vec{r}', \vec{k}'; \vec{r}_0, \vec{k}_0) \right\}$$

其中 $\mathcal{K}_r^\dagger$ 是时间反演的场景相互作用算子。这一递归的Fredholm积分方程构成了sample pass的理论基础：它表明从探测器反向传播广义射线，经过场景交互后到达光源，再与光源分布积分，等价于前向传播光源WDF并在探测器端测量。

**模块间的因果关系链**为：探测器状态采样（模块1）提供了与光相干性无关的初始广义射线参数 → sample pass（模块2）利用这些参数在场景中高效采样光路，解决了采样问题 → solve pass（模块3）沿已采样路径进行精确的波光学计算，纠正sample pass的近似 → 测量算子（模块4）将结果与光源积分，获得无偏估计。这一因果链的核心在于：**采样阶段与光相干性的解耦**使得重要性采样效率大幅提升，而solve pass保证了最终结果的波光学精度。

### 边界条件与实现假设

当前实现假设广义射线的空间范围远小于场景几何细节，从而可以使用标准射线追踪（ray tracing）进行传播。对于较长波长（如雷达仿真），这一假设不再成立，需要实现更昂贵的**波束追踪**（beam tracing）。此外，复合交互运算符（如自由空间狭缝衍射）的采样与处理尚未解决，sample pass阶段为简化实现忽略了偏振效应（由后续solve pass纠正），这可能在某些情况影响采样效率。

![[assets/figures/papers/paper_list_l23_https_ssteinberg_xyz_2023_03_27_rtplt/figures/001_Figure_1.jpg]]
*Figure 1: Locality in wave optics. Spectral rendering of a spaceship model (10 cm in length) with a scratched aluminium fuselage. To render the scratches, we either use (a) our method, or for the bottom insets (b) we use a method similar to Werner et al. [2017]. Colourful wave effects arise when distinct wavefronts— scattered from the base surface and phase-shifted scatter from the scratches—superpose and interfere, hence reproduction of these effects requires integration over a positive region. Werner et al. [2017] use a Gaussian integration patch of a constant size, chosen ad hoc. We denote as ?? the radius of this integration region. Observe that when that region is too small, wave effects fail to...*

![[assets/figures/papers/paper_list_l23_https_ssteinberg_xyz_2023_03_27_rtplt/figures/010_Figure_7.jpg]]
*Figure 7: Partially-coherent sampling. (a) A scene contains a compact disk (CD) that rests next an open CD case, upon which another closed CD case is placed. A ceiling-mounted light source illuminates the scene. While simple, the scene admits interesting light transport. (b) We emulate partially-coherent (PC) sampling of*

## 实验与关键发现

### 核心性能与收敛加速

本方法的核心实验围绕一个关键主张展开：**广义射线采样从根本上解决了向后波光学路径追踪中的“采样问题”，从而在衍射主导的场景中实现数量级级别的收敛加速**。

在CD场景（包含衍射光栅的间接光照场景）中，Fig. 7 直接对比了部分相干采样（emulate PLT的采样策略）与广义射线采样的噪声水平。结果显示，**达到同等渲染质量时，广义射线采样所需的样本数比部分相干采样减少约4000倍**（Fig. 7(c)）。这一差距的物理根源在于：部分相干采样使用的BSDF与探测器实际观测到的BSDF严重不匹配——随着积分区域增大，BSDF的采样分布发生显著变化，但实际观测响应却几乎不变（Fig. 1 的BSDF lobe可视化），导致重要性采样失效。广义射线通过将采样与光的相干性彻底解耦，绕过了这一障碍。

![[assets/figures/papers/paper_list_l23_https_ssteinberg_xyz_2023_03_27_rtplt/figures/009_Figure_8.jpg]]
*Figure 8: Comparison to the state-of-the-art (PLT). We render the CD scene using the PLT bidirectional path tracer (BDPT) [Steinberg et al. 2022]. Because the illumination of the diffractive CD surface is indirect, convergence is poor, as to be expected given the analysis in Fig. 7. The image was rendered with 56 000 samples over about 315 hours, on an Intel®*

与当前最先进方法 **PLT双向路径追踪**（Steinberg et al., ACM Trans. Graph. 2022）的系统性对比进一步验证了算法优势。在CD场景的衍射区域，**本方法实现了约1000–10 000倍的收敛加速**（Fig. 8, filled markers）。PLT BDPT以56 000样本在18核CPU上渲染约315小时，仍难以捕获衍射光栅的高频细节，且因固定64个光谱样本的均匀采样策略而产生明显的带状混叠伪影。相比之下，本方法在GPU上以远少样本即可获得清晰衍射瓣。

需要审慎解读的是硬件差异带来的加速。在CD场景的非衍射区域（Fig. 8, open circle markers），本方法相比PLT BDPT（CPU）实现了最高约100倍的加速，这主要来自GPU的硬件优势。然而，**在衍射区域，即使将GPU加速因素考虑在内，等样本数条件下的收敛性能仍比PLT提升1–8倍**，证明算法层面的改进——即广义射线采样策略——是加速的核心来源。

### 交互式渲染性能

Table 1 列出了各场景在 NVIDIA RTX 3090 GPU 上的交互式渲染帧时间（1 spp）：

![[assets/figures/papers/paper_list_l23_https_ssteinberg_xyz_2023_03_27_rtplt/figures/007_Table_1.jpg]]
*Table 1: Rendering performance. Listed are the resolution and sample count used to generate the figures, as well as the interactive (1 spp) rendering frame times (at the indicated resolution). All rendering was done on a NVIDIA® GeForce RTX™ 3090 GPU*

| 场景 | 分辨率 | 帧时间 (1 spp) |
|------|--------|----------------|
| Snake enclosure | 未明确 | 116 ms |

该性能使得波光学效果的交互式预览成为可能。Fig. 5 的自行车场景展示了低采样数下启用/未启用降噪器的对比，进一步验证了渲染器在交互式工作流中的实用性。

### 消融实验：流形采样

Fig. 4 展示了流形采样（manifold sampling）对复杂光路捕获的关键作用。在包含色散棱镜和衍射光栅的场景中，流形采样能够找到穿过介质界面的光路（如棱镜折射路径）以及镜面反射路径（如画笔金属手柄、颜料管的反射）。**启用流形采样后，衍射光栅的色散衍射瓣被正确捕获**（Fig. 4 底部），而未启用时这些高频波效应完全丢失。Fig. 4 的inset通过颜色编码差值图量化了这一差异。

![[assets/figures/papers/paper_list_l23_https_ssteinberg_xyz_2023_03_27_rtplt/figures/004_Figure_4.jpg]]
*Figure 4: Manifold sampling. Example application of an advanced sampling technique. When performing next event estimation (NEE), manifold sampling (MS) [Hanika et al. 2015; Zeltner et al. 2020] enables finding a light path between a surface and a light source across one or more dielectric interfaces. In the rendered scene, such a sampled path, that refracts through the dispersive prism (outlined in blue), is visualized via the dotted blue line. We also employ MS for NEE on specular reflections: note the reflections off the paint brush’s metal handle and off the paint tubes, as well as the thin diffraction grating (outlined in yellow) dispersing light into multiple diffraction lobes. See full high-res...*

### 波效应与光照条件的依赖关系

Fig. 6 的蛇鳞片场景揭示了衍射材料外观对光照相干性的强烈依赖，这也是向后采样困难的深层原因。白天间接太阳光主导照明时，在某些角度（入射光角度展宽较小、相干性较高），衍射鳞片呈现清晰的干涉图样；夜间荧光灯管直射时，光源空间相干性过低，衍射图样完全消失。这一现象说明：**采样阶段无法预知光的相干性，因此任何基于相干性假设的采样策略（如部分相干采样）必然在某些光照条件下失效**。广义射线的相干无关采样策略正是针对这一根本问题设计的。

### 方法的边界与限制

尽管实验展示了显著的性能提升，方法存在以下已验证或声明的边界条件：

1. **波长假设**：当前实现假设广义射线的空间范围远小于场景几何细节，从而可使用标准射线追踪进行传播。对于较长波长（如雷达、毫米波仿真），此假设不再成立，需要实现波束追踪（beam tracing），计算成本将显著上升。该限制在论文中明确声明，但未提供实验验证。

2. **复合衍射交互**：自由空间中的狭缝衍射、边缘衍射等复合交互运算符的采样与处理尚未解决。Fig. S3 展示了边缘衍射的概念验证，但完整实现仍为开放问题。

3. **偏振简化**：为简化实现，sample pass 阶段忽略了偏振效应（由后续 solve pass 纠正）。论文承认这可能在某些情况下影响采样效率，但未提供量化消融。

4. **场景规模验证**：所有实验场景均为中等规模（CD场景、自行车、蛇鳞片等），在大规模、高度复杂场景下的扩展性和稳定性尚未充分验证。

![[assets/figures/papers/paper_list_l23_https_ssteinberg_xyz_2023_03_27_rtplt/figures/002_Figure_2.jpg]]
*Figure 2: The generalized ray in phase space. It is often convenient to depict the distribution of light in a space known as phase space: an artificial space that can be loosely understood as the Cartesian product of position and direction of propagation. In this space, at a particular time instant, a ray-optical ray is a point (functionally a Dirac delta) as its position and direction are exactly known. Under wave optics, such a distribution of light is prohibited and the phase space is discretizes into overlapping Gaussian cells. A generalized ray—the convolution of a Dirac with a minimum uncertainty Gaussian (a Gaussian with the least variance that fulfils the uncertainty relation, and occupies a...*

## 定位与知识库关联

### 相对于已有方法的本质差异

本文的核心贡献在于**改变了波光学光传输的采样原语与测量范式**，而非在现有框架内做增量改进。具体而言，相对于已有方法，本文改变了三个关键 slot：

1. **光传输原语**：从经典射线（相空间中的 Dirac δ 点）变为**广义射线**（相空间中的最小不确定度高斯波包）。经典射线在波光学下是非物理的——它违背不确定性原理，无法表达光的弱局域性。广义射线则是一个物理上可实现的、最接近经典射线的构造（Fig. 2），其空间/波矢方差由探测器的敏感度参数 β 和传播诱导的相关性参数 ρ 唯一确定，与光的相干性无关。

2. **采样策略**：从**部分相干采样**（如 PLT, Steinberg et al., ACM Trans. Graph. 2022 所采用）变为**相干无关采样**。在向后路径追踪中，部分相干采样需要预知光的相干性来构造 BSDF 的重要性采样分布，但由于向后追踪时无法获知光的相干属性，实际使用的 BSDF 与观测到的 BSDF 严重不匹配——这就是本文所诊断的“采样问题”（Fig. 1）。广义射线的弱局域性完全由探测器决定，因此采样阶段可以完全忽略光的相干性，从根本上解耦光传输与相干性。

3. **测量/积分范式**：从**前向传播 Wigner 分布并在检测器端积分**变为**反向传播探测态并通过测量算子与光源分布积分**。这一转变的物理基础是：经典光电探测器直接测量的并非 Wigner 分布函数（WDF），而是 Husimi Q 分布——即 WDF 与探测态（最小不确定度高斯基/相干态）的卷积（Eq. 6, Section 3.2）。因此，从传感器反向传播这些高斯基（广义射线）可以保持线性叠加与弱局域性，导出精确的向后光传输方程（Eq. 23），并在数学上构成 Fredholm 积分方程的递归形式。

与 **Werner et al. (SIGGRAPH Asia 2017)** 等采用固定积分区域的衍射 BSDF 方法相比，本文不需要手动假设波前形状和尺寸——广义射线精确量化了 BSDF 需要作用的波前范围。与 **PLT (Steinberg et al., 2022)** 相比，本文的 sample–solve 两阶段策略在采样阶段使用广义射线进行相干无关的路径追踪（可应用俄罗斯轮盘、下一事件估计、流形采样等传统重要性采样技术），在求解阶段再沿已采样光路正向重追踪以精确计算部分相干效应，从而在保持波光学精度的同时获得数量级的收敛加速。

### 知识库挂载点

本文可挂载到以下知识节点：

1. **波光学渲染的形式化理论**：本文建立了从 Wigner 分布函数到 Husimi Q 分布再到广义射线传输的完整理论链条。核心公式包括 WDF 定义（Eq. 4）、相空间高斯表示（Eq. 5）、探测器测量强度（Eq. 6）、广义射线波函数（Eq. 15）、以及向后波光传输的渲染方程（Eq. 23）。这一理论框架为波光学渲染提供了严格的数学基础，可视为对经典光传输方程（Kajiya 渲染方程）在波光学域的推广。

2. **相空间光学与量子光学**：广义射线的概念直接源于量子光学中的相干态和 Husimi Q 表示。本文在 Section S7 中推导了与光学相干性的形式化关联，表明广义射线可以理解为将光学部分相干性推广到向后光传输模型。这一连接使得波光学渲染与量子光学、量子信息处理等领域共享数学工具。

3. **路径追踪中的采样理论**：本文的 sample–solve 策略解决了向后波光学路径追踪中长期存在的“采样问题”——即重要性采样分布与目标分布不匹配导致的极慢收敛。这一策略与光子映射中的 two-pass 方法、以及双向路径追踪中的多重重要性采样有结构上的类比，但针对的是波光学特有的相干性未知问题。

### 适用边界

1. **波长假设**：当前实现假设广义射线的空间范围远小于场景几何细节，从而可以使用传统射线追踪进行传播。对于较长波长（如毫米波、雷达仿真），该假设不再成立，需要实现更昂贵的**波束追踪**（beam tracing）来正确模拟衍射绕过几何障碍的效应（Fig. S3 已展示此类效应）。

2. **复合交互的采样**：本文尚未解决自由空间狭缝衍射、几何边缘衍射等复合交互算子的采样与处理问题。这些场景中的广义射线传播需要更复杂的相空间动力学描述。

3. **偏振处理**：为简化实现，sample pass 阶段忽略了偏振效应（由后续 solve pass 纠正）。在偏振敏感的波光学效应（如双折射介质中的干涉）中，这可能影响采样效率，但 solve pass 保证了最终结果的物理正确性。

4. **大规模场景的扩展性**：算法在高度复杂、大规模场景下的扩展性和数值稳定性尚未充分验证。当前实验场景（CD 场景、Snake 场景、Bike 场景）规模适中。

### 后续启发

1. **波束追踪的实现**：如何高效实现波束追踪以支持非光学波长（毫米波、太赫兹）的广义射线传播，是直接的技术延伸方向。

2. **复合衍射的采样**：为广义射线采样复合交互（如穿过几何边缘或狭缝的衍射）将扩展方法的适用范围，使其能处理更一般的波光学场景。

3. **量子光学效应的渲染**：广义射线框架基于相干态和 Husimi Q 表示，理论上可以进一步拓展以处理量子光学中的其他可观测效应（如光子反群聚、压缩态等），为量子成像仿真提供渲染工具。

4. **与高级采样技术的深度结合**：sample–solve 策略可以与更先进的光源重要性采样、路径引导技术（如 path guiding）更深度地结合，进一步提升在复杂光照条件下的收敛性能。

5. **对传统渲染的启示**：本文揭示了一个更深层的洞见——在波光学层面，探测器本身就是光传输的主动参与者（其敏感度函数决定了可观测的相干范围）。这一视角可能启发对传统几何光学渲染中“像素滤波器”角色的重新审视。

## 原文 PDF

![[paperPDFs/SIGGRAPH_ASIA_2024/A_Generalized_Ray_Formulation_For_Wave_Optical_Light_Transport.pdf]]