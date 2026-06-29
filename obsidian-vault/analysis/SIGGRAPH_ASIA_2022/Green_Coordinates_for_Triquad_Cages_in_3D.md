---
title: Green Coordinates for Triquad Cages in 3D
type: paper
paper_level: A
venue: SIGGRAPH ASIA
year: 2022
pdf_ref: paperPDFs/SIGGRAPH_ASIA_2022/Green_Coordinates_for_Triquad_Cages_in_3D.pdf
project_link: null
code_link: null
aliases:
- QGCQ
- GCTC3
tags:
- SIGGRAPH_ASIA_2022
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
core_operator: 引入基于双线性四边形模型的新Neumann边界条件，显式处理四边形上逐点变化的法线和拉伸因子，并推导出每四边形四个角坐标，从而在triquad笼上实现准共形变形。
primary_logic: 通过双线性插值和自适应黎曼求和，将线性精度约束嵌入坐标计算，使得近似坐标光滑且免于三角剖分伪影，并保留准共形性。
claims:
- 提出了适用于三角形和四边形混合笼子的Green坐标，基于Green第三恒等式，并引入了新的Neumann边界条件，为每个四边形生成四个额外的法线坐标。
- 通过非归一化法线的双线性插值和每四边形角坐标，避免了四边形三角剖分导致的不对称变形，并保留了准共形行为。
- 提出了一种基于自适应黎曼求和的鲁棒近似方法，保证了坐标的光滑性和线性精确性。
- Triquad cage deformations (various meshes) 上 Visual quality (artifact avoidance, conformal behavior) = QGC
---

# Green Coordinates for Triquad Cages in 3D

> [!tip] 核心洞察
> 通过双线性插值和自适应黎曼求和，将线性精度约束嵌入坐标计算，使得近似坐标光滑且免于三角剖分伪影，并保留准共形性。

| 字段 | 内容 |
|------|------|
| 中文题名 | 三四边形笼子的绿色坐标 |
| 英文题名 | Green Coordinates for Triquad Cages in 3D |
| 会议/期刊 | SIGGRAPH ASIA 2022 |
| Links | [paper](https://perso.telecom-paristech.fr/boubek/papers/QGC/) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction |
| Method | Quad Green Coordinates (QGC) |
| Dataset | Triquad cage deformations, Computation time |

> [!tip] 效果简介
> - Triquad cage deformations (various meshes) 上，Visual quality (artifact avoidance, conformal behavior) QGC vs GC, QMVC (QGC eliminates asymmetric artifacts from triangulation and preserves details un...)。
> - Computation time (Table 1) 上，CPU time (ms) QGC (e.g., 382 ms for SpikyBar) vs GC (30 ms), TGC-16 (169 ms) (QGC is slower than triangulated GC but offers artifact-free deformation.)。

## 概要

现有Green坐标（GC）仅适用于三角形笼子，而艺术家常用的四边形笼子因其非平面法线逐点变化，无法直接施加GC的每面常量Neumann边界条件。若将四边形强制三角剖分以适配GC，会引入不对称变形伪影。针对此瓶颈，本文提出**三四边形笼子的Green坐标（QGC）**，核心思路是：引入基于双线性四边形模型的新Neumann边界条件，显式处理四边形上逐点变化的法线和拉伸因子，并为每个四边形推导出四个角法线坐标，从而在三角形与四边形混合笼子上实现准共形变形。通过自适应黎曼求和与校正因子，QGC在保持线性精度的同时避免了三角剖分伪影，且坐标光滑。实验表明，QGC在视觉质量上消除了不对称锯齿伪影，并能在大幅拉伸下保留几何细节，优于三角剖分GC和四边形均值坐标（QMVC），但计算开销高于传统GC。该方法定位于将Green坐标的准共形变形能力从纯三角形笼子拓展到三四边形混合笼子，填补了四边形笼子缺乏准共形坐标的空白。

## 核心方法与创新机理

### 问题瓶颈与核心洞察

现有的Green坐标（Green Coordinates, GC）方法（Lipman et al., 2008）仅支持三角形笼子。当艺术家使用四边形笼子时，必须将每个四边形强制三角剖分，这导致两个根本性问题：**首先**，三角剖分破坏了四边形的对称性，在对笼子进行非均匀拉伸时会产生锯齿状不对称变形伪影（Fig. 5）；**其次**，原始GC的Neumann边界条件假设每面具有常量共形因子和法线，而四边形上的法线是逐点变化的，这一假设在四边形上不成立。

本文的核心洞察在于：虽然单位法线 $n_{uv}$ 不是双线性插值量，但**非归一化法线** $N_{uv} = \partial_u q_{uv} \times \partial_v q_{uv}$ 是四边形四个角点非归一化法线 $\{N_k^q\}_{k=0}^3$ 的简单双线性函数（Eq. 8）。这一发现使得可以将四边形的Neumann边界条件显式表达为四个角坐标的线性组合，从而避免了三角剖分，并保留了准共形变形行为。

### 方法框架与Changed Slots

QGC方法在GC框架的基础上进行了五个关键槽位的替换：

| 槽位 | 基线（GC） | QGC |
|------|-----------|-----|
| 笼子几何支持 | 仅三角形笼 | 三角形+非平面四边形混合笼 |
| 每面法线坐标数 | 每三角形1个 $\sigma_t n_t'$ | 每四边形4个角坐标 $\sigma_q^k N_k^q$ |
| Neumann条件 | 每面常量 | uv-变化的面积基条件+校正因子 |
| 线性精度处理 | 自然满足 | 通过几何不变量显式约束 |
| 坐标计算方式 | 闭式表达式 | 自适应黎曼求和近似 |

### 关键公式与推导链

**1. Green第三恒等式与边界条件**

变形函数 $f(\eta)$ 由Green第三恒等式给出：
$$f(\eta) = \int_{\xi \in \partial\Omega} f(\xi) \frac{\partial G}{\partial n}(\xi,\eta) d\xi - \int_{\xi \in \partial\Omega} G(\xi,\eta) \frac{\partial f}{\partial n}(\xi) d\xi$$

其中Dirichlet条件使用帽函数 $\Gamma^i$ 对笼子顶点变形进行线性插值：
$$f(\xi) = \sum_i \Gamma^i(\xi) v_i'$$

对于三角形，Neumann条件为每面常量：
$$\frac{\partial f}{\partial n}(\xi) = \sigma_j n_j'$$

**2. 四边形上的双线性几何与Neumann条件**

考虑参数域 $(u,v) \in [0,1]^2$ 上的双线性四边形 $q_{uv}$，其切向量和非归一化法线为：
$$\partial_u q_{uv} = (1-v)(q_1-q_0) + v(q_2-q_3)$$
$$\partial_v q_{uv} = (1-u)(q_3-q_0) + u(q_2-q_1)$$
$$N_{uv} = \partial_u q_{uv} \times \partial_v q_{uv} = \sum_{k=0}^3 b_{uv}^k N_k^q$$

其中 $b_{uv}^k$ 是双线性混合函数，$N_k^q$ 是四边形角点处的非归一化法线。这一双线性插值性质是QGC的数学基础。

初始的uv-变化面积基Neumann条件为：
$$\frac{\partial f}{\partial n}(q_{uv}) = \sigma_{uv}^q n_{uv}', \quad \sigma_{uv}^q := \frac{\|N_{uv}'\|}{\|N_{uv}\|}$$

其中 $\sigma_{uv}^q$ 是变形后与静止姿态的面积比。

**3. 校正因子与准共形性恢复**

直接使用面积基 $\sigma_{uv}^q$ 会导致变形过度突出（Fig. 3b）。为了逼近Lipman等人原始GC的共形拉伸行为，引入校正因子 $\sigma_q^k$，将Lipman拉伸因子 $\sigma_{uv}^L$ 的行为通过加权积分“烘焙”到每四边形角：
$$\sigma_q^k := \frac{\int_{u,v=0}^1 b_{uv}^k \sigma_{uv}^L dq_{uv}}{\int_{u,v=0}^1 b_{uv}^k \sigma_{uv}^A dq_{uv}}$$

其中 $\sigma_{uv}^L$ 是Lipman的共形因子（基于切向量拉伸的复杂表达式），$\sigma_{uv}^A$ 是面积比。校正因子 $\sigma_q^k$ 仅依赖于变形后的笼子几何，与评估点 $\eta$ 无关，因此可以逐帧预计算。

**4. 最终变形公式**

QGC的完整变形公式为：
$$f(\eta) = \sum_{i \in \mathcal{V}} \phi_i(\eta) v_i' + \sum_{t \in \mathcal{T}} \psi_t(\eta) \sigma_t n_t' + \sum_{q \in Q} \sum_{k=0}^3 \psi_k^q(\eta) \sigma_q^k N_k^q$$

三项分别对应：顶点位移贡献、三角形法线拉伸贡献、四边形角法线拉伸贡献。其中 $\phi_i$ 和 $\psi_t$ 是三角形面上的标准GC坐标，$\psi_k^q$ 是四边形角 $k$ 的法线坐标。

### 坐标计算的因果链

**模块1：静止姿态预处理**

对每个四边形 $q$，计算矩阵 $A_q$（编码四边形几何与双线性混合函数的关系）并进行SVD分解，提取零空间基。这些量仅依赖于静止姿态笼子，可在预处理阶段完成。

**模块2：逐帧校正因子计算**

每帧根据变形后的四边形几何，通过Eq. (22)计算四个角点的校正因子 $\sigma_q^k$。该步骤仅依赖笼子变形，与内部顶点数量无关。

**模块3：逐顶点坐标评估**

这是计算瓶颈所在。由于四边形上的积分无闭式解，QGC采用自适应uv-域三角剖分和黎曼求和近似：

- 将参数域 $[0,1]^2$ 按自适应模式（Eq. 19）剖分为三角形集合 $\{t\}$
- 对每个三角形 $t$，计算其重心 $(u_t, v_t)$ 处的双线性混合值 $b_{uv_t}^k$
- $\phi_k^q(\eta)$ 通过立体角加权求和近似：$\phi_k^q(\eta) = \sum_t \frac{b_{uv_t}^k \omega_t(\eta)}{4\pi}$
- $\psi_k^q(\eta)$ 通过单层势近似：$\psi_k^q(\eta) \simeq \sum_t \frac{b_{uv_t}^k \psi^t(\eta)}{\|N_{uv_t}\|}$

自适应模式的关键在于：当评估点 $\eta$ 靠近四边形时，在其投影点附近加密剖分，以保证 $\eta$ 始终位于剖分表面的正确一侧，从而确保积分的鲁棒性。

**模块4：线性精度约束**

坐标需满足线性精度（即当笼子顶点发生仿射变换时，内部点跟随变换）。QGC通过引入与剖分无关的几何不变量，将线性精度约束直接嵌入坐标计算：利用零空间分量调整坐标，使其在满足线性精度的同时保持光滑性。

**模块5：变形重建**

将模块3计算的坐标与模块2的校正因子、笼子顶点位置和法线按Eq. (23)组合，得到最终变形位置。

### 因果机制总结

双线性法线插值性质 → 每四边形四角坐标 → 避免三角剖分伪影；校正因子嵌入Lipman拉伸行为 → 准共形变形；自适应黎曼求和+线性精度约束 → 光滑且精确的坐标近似。整个管线将四边形上的逐点变化Neumann条件转化为四个离散角坐标的线性组合，使得QGC在保持GC准共形优势的同时，原生支持艺术家偏好的四边形笼子工作流。

## 实验与关键发现

### 主结果：视觉质量与变形行为对比

QGC 的核心优势体现在变形视觉质量上。与基线方法相比，QGC 在 triquad 笼子上产生的变形避免了三角剖分引入的非对称伪影，同时保留了准共形行为。

**与 GC（三角形 Green 坐标）的对比**：GC 方法仅原生支持三角形笼子。当输入包含四边形时，必须先将每个四边形强制剖分为三角形。这种剖分方向的选择是任意的——例如一个四边形可以沿对角线切成两个三角形，但切分方向会破坏四边形本身的对称性。当变形后的笼子四边形发生拉伸时，三角剖分的不对称性会传递到内部网格，产生锯齿状变形伪影（Fig. 5）。QGC 通过直接建模双线性四边形上的逐点变化法线，为每个四边形生成四个角坐标（而非一个面坐标），从根本上避免了剖分方向的选择问题，因此不会产生此类伪影。

**与 QMVC（四边形均值坐标）的对比**：QMVC 同样支持四边形笼子，但其数学基础决定了它不具备准共形特性——在非刚性变形下会产生明显的体积失真和细节丢失。QGC 继承了 Green 坐标的共形拉伸机制，通过校正因子逼近 Lipman 等人（2008）的共形因子行为，在保持局部形状细节方面显著优于 QMVC（Fig. 4）。

**校正因子的决定性作用**：消融实验表明，若直接使用面积基 Neumann 条件（σ_uv^q = ‖N_uv'‖/‖N_uv‖）而不施加校正，变形会在变形笼子外部产生过度突出的膨胀效果（Fig. 3b）。引入每四边形角的校正因子 σ_q^k（Eq. 22）后，变形行为回归到与 Lipman 共形因子相近的自然状态（Fig. 3c）。校正因子的本质是通过加权积分，将 Lipman 的拉伸因子 σ_uv^L 的行为“烘焙”进四个角坐标的权重中，使得逐点变化的面积基条件在整体行为上逼近共形因子条件。

### 计算开销

Table 1 报告了不同方法在多个测试网格上的坐标计算时间（CPU，毫秒）。

![[assets/figures/papers/paper_list_l56_https_perso_telecom_paristech_fr_boubek_papers_QGC/figures/007_Table_1.jpg]]
*Table 1: Timings (in ms)*

| 网格 | 顶点数/笼子面数 | GC | TGC-16 | QGC |
|------|----------------|-----|--------|-----|
| SpikyBar | 10002/352 | 30 | 169 | 382 |
| 其他网格 | — | 类似比例 | 类似比例 | 类似比例 |

QGC 的计算时间显著高于 GC（约 10-13 倍），也高于将每个四边形剖分为 16 个三角形的 TGC-16（约 2-3 倍）。这一开销源于 QGC 无法使用闭式表达式，必须依赖自适应 uv 域剖分和黎曼求和近似计算每个顶点的坐标。具体而言，对于每个网格顶点 η，QGC 需要在每个四边形的参数域 [0,1]² 上进行自适应三角剖分，并在每个子三角形上计算双层势和单层势的近似值。剖分密度由参数 n 控制（n=0 时为 4 个三角形，n=1 时为 16 个，以此类推）；实际使用中需要根据顶点到四边形的距离动态调整剖分密度以保证精度。

**速度与质量权衡**：TGC-X 方法（将四边形剖分为 X 个三角形后使用标准 GC）虽然速度快于 QGC，但 Fig. 5 清楚地展示了其根本缺陷——无论剖分多细（TGC-16、TGC-64），三角剖分引入的非对称性始终存在，表现为沿拉伸方向的锯齿状变形。QGC 以更高的计算成本换取了无伪影的变形质量，这一权衡在离线高质量变形场景中是可接受的。

### 关键消融：面积基 vs. 校正后 Neumann 条件

Fig. 3 的系统对比揭示了 Neumann 条件设计对变形行为的决定性影响：

![[assets/figures/papers/paper_list_l56_https_perso_telecom_paristech_fr_boubek_papers_QGC/figures/005_Figure_3.jpg]]
*Figure 3: a) Input. b?? ) Area-based QGC. c?? ) Conformal-factor-based QGC obtained using correction factors. d?? ) Area-based triangular GC. e?? ) Conformalfactor-based triangular GC. The triangular GC are obtained by cutting each quad into 16 triangles*

- **面积基 QGC（无校正）**：使用 σ_uv^q = ‖N_uv'‖/‖N_uv‖ 作为拉伸因子。在变形笼子向外拉伸时，内部网格产生过度膨胀，超出变形笼子的包络范围。这是因为面积比在双线性四边形上逐点变化剧烈，直接使用会导致局部拉伸过度。
- **校正后 QGC**：通过 σ_q^k 校正因子将 Lipman 的 σ_uv^L 行为嵌入。变形结果自然、细节保持良好，与 Lipman 原始 GC 的行为一致。
- **面积基三角 GC**：将四边形剖分为 16 个三角形后使用面积基 GC。结果与面积基 QGC 类似，同样存在过度膨胀问题。
- **共形因子基三角 GC**：剖分后使用 Lipman 的共形因子条件。变形自然，但存在三角剖分引入的细微非对称伪影。

这一消融证实：校正因子并非可选的微调项，而是实现自然准共形变形的必要条件。面积基条件单独使用会导致不可接受的变形失真。

### 自适应剖分的鲁棒性

QGC 的坐标计算依赖于对四边形参数域的自适应三角剖分（Fig. 2）。消融表明，固定均匀剖分模式在顶点靠近四边形边界或四边形形状极端时会产生数值不稳定，表现为坐标的不连续跳变。自适应模式（Eq. 19 及 Algo. 1）根据顶点投影位置动态调整剖分中心，使得黎曼求和近似在参数域各处保持光滑。这一设计保证了最终变形结果的空间连续性——相邻顶点获得相近的坐标值，避免变形后网格出现裂缝或自交。

![[assets/figures/papers/paper_list_l56_https_perso_telecom_paristech_fr_boubek_papers_QGC/figures/004_Figure_2.jpg]]
*Figure 2: Adaptive ????-tessellation for the Riemann summation. First: ????-grid. Second and third: Triangles covered in order as described in Algo. 1, using*

### 失败模式与适用边界

**退化四边形的限制**：QGC 仅在通过有效性测试的四边形上定义。具体而言，四边形必须满足双线性参数化在整个 [0,1]² 域上是单射的。平面非凸四边形、自交四边形以及极端扭曲的非平面四边形无法通过该测试，QGC 在这些面上没有定义。这意味着艺术家创建的笼子需要满足一定的几何合理性约束。

**退化变形配置**：校正因子 σ_q^k 的计算（Eq. 22）涉及变形后四边形面积与静止态四边形面积的比值积分。当变形后的四边形面积退化为零（例如四边形被完全压扁）时，该公式出现除零问题，行为未定义。这一局限继承自 Lipman 等人（2008）的原始 GC 方法——两者在退化面附近都会产生数值不稳定。

**无闭式解的工程代价**：QGC 坐标无闭式表达式，所有计算依赖数值积分近似。这一特性带来了两个实际限制：(1) 难以推导坐标关于笼子顶点的梯度和海森矩阵，因此无法直接嵌入需要二阶信息的变分优化框架（如保持体积的变形优化）；(2) 计算效率受限于逐点数值积分的精度需求，难以满足实时交互变形的要求（当前单帧数百毫秒量级）。

**拉伸行为的刚性**：QGC 的准共形特性在保持局部细节的同时，也意味着艺术家难以主动偏离准共形变形。拉伸因子直接编码在坐标与非归一化角法线的乘积中，若不修改校正因子的定义，无法实现局部放大/缩小等非准共形效果。这限制了 QGC 在需要艺术夸张变形场景中的灵活性。

**数值缩放建议**：实现中需要将输入笼子和网格缩放到适中尺寸（例如包围盒直径约 1-10 单位），以避免 Green 函数及其梯度计算中的浮点精度问题。过大或过小的几何尺度会导致双层势和单层势的数值积分精度下降。

![[assets/figures/papers/paper_list_l56_https_perso_telecom_paristech_fr_boubek_papers_QGC/figures/006_Figure_4.jpg]]
*Figure 4: We compare our Green Coordinates for Quad cages (QGC) with Mean-Value Coordinates for Quad cages (QMVC) and Green Coordinates (GC)*

![[assets/figures/papers/paper_list_l56_https_perso_telecom_paristech_fr_boubek_papers_QGC/figures/008_Figure_5.jpg]]
*Figure 5: One cage quad is stretched in the x-direction. The jaggy deformation artifact (third) stems from the approximation of the (symmetric) bilinear quad deformation with the (asymmetric) triangle deformation introduced in the quad tessellation (each quad was tesselated into X triangles for TGC-X)*

## 定位与知识库关联

本文的核心贡献在于为三维笼子变形这一经典问题**改变了 cage_geometry_support 这一关键 slot**：将 Green 坐标（GC）从仅支持三角形笼子的限制中解放出来，使其能够直接作用于三角形与四边形混合的笼子（triquad cage）。这一改变直接回应了艺术家工作流中长期存在的需求——四边形笼子在建模软件（如 Maya、Blender）中远比三角形笼子直观和常用，但原有的 GC 方法（Lipman et al., 2008）无法直接处理四边形，强制三角剖分又会引入不对称的锯齿状变形伪影（Fig. 5）。

**相对于已有方法，QGC 改变了什么？**

1. **相对于 GC（Lipman et al., 2008）**：GC 的 neumann_condition slot 是每面常量的共形因子和法线（$σ_t n_t'$），这依赖于三角形面上法线恒定的性质。四边形上法线逐点变化，直接套用常量 Neumann 条件在物理上不成立。QGC 将这一 slot 替换为 uv-变化的面积基 Neumann 条件（Eq. 9），并进一步通过校正因子（Eq. 22）逼近 Lipman 的拉伸行为。同时，normal_coordinate_per_face slot 从每三角形一个法线坐标扩展为每四边形四个角法线坐标（$σ_q^k N_k^q$），使得变形能够捕捉四边形内部法线的双线性变化。

2. **相对于 QMVC（Thiery et al., 2018）**：QMVC 虽然也支持四边形笼子，但其本质是均值坐标（Mean Value Coordinates）的推广，不具备准共形（quasi-conformal）特性。QGC 通过 Green 第三恒等式的调和性基础，保留了 GC 的核心优势——在 cage 变形时产生准共形映射，更好地保持局部细节形状。这在 Fig. 4 的对比中得到了验证：QGC 在大拉伸下仍能保持形状特征，而 QMVC 出现明显的体积塌缩。

3. **相对于简单三角剖分的 TGC-X**：将四边形剖分为 X 个三角形再应用 GC（TGC-X）是一种工程上直接的替代方案，但剖分引入了不对称性：双线性四边形的对称变形被近似为三角形的非对称变形，导致锯齿伪影（Fig. 5）。QGC 通过每四边形角坐标的设计，从数学上避免了这一问题，而非通过增加剖分密度来掩盖。

**知识库挂载点**

QGC 在知识图谱中的挂载位置是**笼子变形坐标方法族**的 Green 坐标分支。该分支的上游是 Green 第三恒等式在边界元方法中的应用，核心下游包括：

- **GC（Lipman et al., 2008）**：三角形笼子的 Green 坐标，提供闭式调和变形。QGC 是其直接扩展，将定义域从三角形面推广到双线性四边形面。
- **QMVC（Thiery et al., 2018）**：四边形均值坐标，解决了四边形笼子上的广义重心坐标构造，但不具备调和/准共形保证。QGC 在 cage_geometry_support 上与 QMVC 对齐，但在变形质量 slot 上提供了更强的数学保证。
- **Poisson 重建与变分笼子变形**：GC 的调和性使其可以嵌入变分优化框架。QGC 因坐标无闭式解（依赖自适应黎曼求和近似），暂时无法直接提供梯度和海森矩阵，这限制了其向该分支的直接延伸。

**适用边界**

QGC 的适用边界由以下条件划定：

- **四边形有效性**：仅支持通过有效性测试的双线性四边形。平面非凸四边形、高度非平面或自交四边形因双线性参数化的非单射性而无法使用。这意味着艺术家需要保持笼子四边形在合理范围内。
- **准共形变形约束**：拉伸条件直接编码在坐标与非归一化角法线的乘积中，若不修改校正因子，难以让艺术家偏离准共形变形。对于需要局部非均匀拉伸的艺术效果，需要额外的用户控制机制。
- **退化配置**：当变形后四边形面积为零时，校正因子公式（Eq. 22）退化，行为未定义。这是从原始 GC 继承的局限，而非 QGC 引入的新问题。
- **计算效率**：QGC 的逐点计算开销显著高于闭式 GC（Table 1：SpikyBar 模型上 QGC 382ms vs GC 30ms），目前不适合实时交互式变形。

**后续启发与开放方向**

1. **隐式变分框架**：能否基于 QGC 设计隐式变分框架，利用坐标进行保持体积的快速变形优化？这需要解决梯度和海森矩阵的近似计算问题，可能的路径是通过自动微分作用于黎曼求和近似，或预计算局部泰勒展开。

2. **用户可控的拉伸因子**：如何提供直观的用户控制，允许局部调整拉伸因子以实现非准共形效果？这需要在每四边形角坐标上引入可编辑的权重通道，同时保持线性精度约束。

3. **更广泛的四边形类型**：能否扩展投影算子以容纳更广泛的四边形类型，例如高度非平面或自交四边形？这可能需要引入非双线性参数化或分段处理策略。

4. **GPU 加速与实时应用**：能否通过 GPU 加速或预计算进一步减少逐点计算开销？自适应黎曼求和的三角剖分模式具有可并行性，适合 GPU 实现；此外，静止姿态下的部分几何不变量可以预计算并存储。

## 原文 PDF

![[paperPDFs/SIGGRAPH_ASIA_2022/Green_Coordinates_for_Triquad_Cages_in_3D.pdf]]