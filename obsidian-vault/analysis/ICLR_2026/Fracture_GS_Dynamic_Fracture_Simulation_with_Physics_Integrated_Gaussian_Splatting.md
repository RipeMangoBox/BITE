---
title: "Fracture-GS: Dynamic Fracture Simulation with Physics-Integrated Gaussian Splatting"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/Fracture_GS_Dynamic_Fracture_Simulation_with_Physics_Integrated_Gaussian_Splatti_ec080bbb2d3d.pdf
project_link: null
code_link: null
aliases:
- FG
- Fracture-GS
tags:
- ICLR_2026
- topic/other_unclear
- topic/other_unclear/general
core_operator: 引入基于归一化质量分布的界面力计算与动量守恒碰撞力，消除非物理黏附；利用硬化参数追踪断裂粒子并通过最小体积外接椭球（MVEE）优化生成高斯属性，提升断裂面渲染质量。
primary_logic: 通过计算每个网格节点上两物体粒子的质量分布梯度作为界面方向趋势，并在相对速度条件下施加动量守恒碰撞力，可有效阻止穿透并避免黏附；同时，基于硬化参数α动态识别断裂粒子，利用MVEE对重叠高斯进行属性重构，实现物理一致的断裂面渲染。
claims:
- 改进的Collision-MPM通过动量守恒界面力消除非物理黏附。
- 断裂粒子追踪与MVEE优化可生成高质量断裂面渲染。
- 所提方法在定性和定量指标上均优于现有方法。
- 通过计算每个网格节点上两物体粒子的质量分布梯度作为界面方向趋势，并在相对速度条件下施加动量守恒碰撞力，可有效阻止穿透并避免黏附；同时，基于硬化参数α动态识别断裂粒子，利用MVEE对重叠高斯进行属性重构，实现物理一致的断裂面渲染。
---

# Fracture-GS: Dynamic Fracture Simulation with Physics-Integrated Gaussian Splatting

> [!tip] 核心洞察
> 通过计算每个网格节点上两物体粒子的质量分布梯度作为界面方向趋势，并在相对速度条件下施加动量守恒碰撞力，可有效阻止穿透并避免黏附；同时，基于硬化参数α动态识别断裂粒子，利用MVEE对重叠高斯进行属性重构，实现物理一致的断裂面渲染。

| 字段 | 内容 |
|------|------|
| 中文题名 | Fracture-GS：物理集成高斯泼溅的动态断裂模拟 |
| 英文题名 | Fracture-GS: Dynamic Fracture Simulation with Physics-Integrated Gaussian Splatting |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=zcAwK50ft0) |
| Topic | #topic/other_unclear #topic/other_unclear/general |
| Method | Fracture-GS |
| Dataset | Ficus, Teapot, Table fracture simulation scenes, DTU |
> [!tip] 效果简介
> - 所提方法在定性和定量指标上均优于现有方法。

## 概要

### 问题与瓶颈

在基于物理的视觉仿真中，模拟极端机械碰撞下的动态断裂并高质量渲染结果，长期面临两大核心瓶颈：

1. **碰撞界面的非物理黏附**：现有基于材料点法（MPM）的方法在处理多物体碰撞时，因缺乏有效的界面力计算，常导致物体穿透或非物理黏附，破坏仿真的物理可信度。
2. **断裂面的渲染质量不足**：断裂过程中新暴露的表面缺乏对应的高斯属性，现有方法要么无法生成断裂面高斯，要么简单复制导致视觉失真。

### 核心结论

**Fracture-GS** 通过两个关键机制解决了上述问题：

- **动量守恒碰撞力**：引入基于归一化质量分布的界面力计算，在网格节点上根据相对速度条件施加动量守恒碰撞力，从根本上消除了多体碰撞中的非物理黏附现象。
- **断裂粒子高斯优化**：利用NACC本构模型中的硬化参数 $\alpha$ 动态追踪断裂粒子，并通过最小体积外接椭球（MVEE）优化重构新高斯粒子的位置与协方差矩阵，实现物理一致的断裂面渲染。

定性与定量实验表明，Fracture-GS 在 PSNR、LPIPS、FID 及 FSF 等指标上均优于现有方法（Figure 5），且系统总动量在整个碰撞过程中保持守恒（Figure 7），能量演化无异常增长（Figure 8）。

### 方法定位

Fracture-GS 位于 **物理仿真与神经渲染的交叉点**，其方法谱系可概括为：

| 维度 | 基线方法 | 本方法改进 |
|------|----------|------------|
| 物理仿真框架 | **MLS-MPM** (Hu et al., 2018) 标准材料点法，无专门碰撞处理 | 嵌入动量守恒碰撞力，消除黏附 |
| 高斯泼溅集成 | **PhysGaussian** (Xie et al., 2024) 集成高斯泼溅与MPM，未处理断裂 | 断裂粒子追踪与高斯属性重构 |
| 物理参数估计 | **GIC** (Cai et al., 2024) 基于高斯可微性的参数估计，未考虑断裂 | 硬化参数驱动的动态断裂识别 |

方法管道（Figure 2）从多视图图像的SDF隐式重建出发，经表面高斯学习、碰撞MPM动力学模拟、断裂粒子追踪与高斯优化，最终通过遮挡感知采样实现实时渲染。

### 主要结果概要

- **定性效果**：在多物体极端碰撞场景（茶壶-桌子、榕树-桌子等）中，断裂碎片呈现自然分离行为，无黏附伪影（Figure 6, Figure 10）。
- **定量指标**：Fracture-GS 在 PSNR、LPIPS、FID、FSF 四项指标上均取得最优（Figure 5）。
- **物理守恒**：系统总动量严格守恒（Figure 7），动能-弹性能-重力势能演化合理且无异常增长（Figure 8）。
- **渲染效率**：断裂粒子追踪使每帧渲染时间增加约20-80%，但整体仍保持高效（Table 2）。
- **泛化能力**：在真实世界数据（DTU数据集）上验证了方法的适用性（Figure 11）。

> **注意**：定量评估采用自参照协议（以断裂前最后一帧为参考），缺乏真实动态序列基准，指标反映的是视觉连贯性而非绝对物理精度。未来需发展专门用于物理渲染的评估度量。

### 问题背景：动态断裂模拟的视觉与物理双重挑战

在计算机图形学中，动态断裂模拟长期面临一个核心矛盾：物理求解器追求力学精度，而渲染管线要求视觉真实感。传统有限元法（FEM）虽能精确模拟断裂，但计算成本极高，难以扩展到复杂多体碰撞场景。材料点法（MPM）因其天然的拓扑变化处理能力，已成为断裂模拟的主流选择——粒子携带连续介质属性，在欧拉网格上求解动量方程，无需显式处理裂纹面。

然而，将MPM模拟结果转化为高质量渲染图像并非易事。早期工作依赖显式网格重建或体积渲染，前者引入昂贵的后处理步骤，后者难以捕捉断裂面的细节纹理。3D高斯泼溅（3D Gaussian Splatting, 3DGS）的出现为这一问题提供了新思路：用一组各向异性高斯核表示场景，通过可微光栅化实现实时高质量渲染。将MPM粒子直接映射为高斯核，理论上可实现“模拟即渲染”的端到端管线。

### 现有方法缺口：非物理黏附与断裂面渲染缺失

尽管MPM-3DGS联合框架（如**PhysGaussian**（Xie et al., 2024））在弹性变形场景中取得了令人瞩目的效果，但在极端机械碰撞——即物体高速撞击并发生碎裂的场景——中暴露出两个根本性缺陷：

**缺口一：非物理黏附伪影。** 标准MLS-MPM（**MLS-MPM**（Hu et al., 2018））在处理多体碰撞时，缺乏有效的碰撞界面力机制。当两个物体的粒子在同一网格节点附近交汇时，简单的惩罚力或速度平均方案无法正确分离粒子，导致本应弹开的碎片“粘”在碰撞面上，形成视觉上明显且物理上错误的黏附伪影。这一问题的根源在于：传统MPM的粒子-网格插值过程天然模糊了物体边界，在缺乏显式界面力的情况下，动量交换无法正确反映碰撞法线方向。

**缺口二：断裂面渲染质量不足。** 当物体碎裂时，新暴露的内部表面缺乏对应的高斯核表示。现有方法要么简单复制邻近粒子的高斯属性，要么直接丢弃断裂粒子，导致断裂面呈现模糊、空洞或纹理错位。这是因为高斯核的属性（位置、协方差、颜色）是在初始完整物体上学习的，断裂后新表面的几何与外观分布与原始表面有本质差异，简单插值无法恢复物理一致的渲染结果。

### 本文动机：物理-渲染联合优化的断裂模拟

针对上述缺口，Fracture-GS提出了一条物理-渲染深度耦合的技术路线：**在MPM求解器中嵌入动量守恒的碰撞界面力，从根本上消除非物理黏附；同时，通过断裂粒子追踪与最小体积外接椭球（MVEE）优化，为断裂面生成物理一致的高斯属性。** 这一设计理念的核心洞察是：碰撞界面的质量分布梯度天然编码了接触方向信息，而硬化参数$\alpha$则提供了粒子是否处于断裂状态的连续信号——将这两者分别引入碰撞力计算和断裂粒子识别，即可在不增加显著计算开销的前提下，实现物理准确性与视觉真实性的同步提升。

## 核心方法与创新机理

Fracture-GS 的核心创新在于将物理一致的碰撞-断裂动力学与高质量可微渲染深度融合，形成端到端的“物理仿真-高斯重建-实时渲染”闭环。该方法针对现有 MPM-高斯泼溅混合框架在极端机械碰撞场景下的两个关键瓶颈进行了系统性改进：**非物理黏附伪影**与**断裂面渲染质量不足**。

### 创新一：动量守恒的碰撞界面力

传统 MLS-MPM（**MLS-MPM**，Hu et al., 2018）及基于其构建的 **PhysGaussian**（Xie et al., 2024）在模拟多物体碰撞时，由于缺乏专门的碰撞界面处理机制，网格节点上不同物体的粒子速度场被简单平均，导致物体在接触后产生非物理的“黏附”行为——断裂后的碎片无法自然分离，而是粘着在碰撞对象表面。

Fracture-GS 提出 **Collision-MPM**，核心机制包含两个步骤：

1. **界面方向趋势计算**：对于每个网格节点 $G_i$，分别计算属于物体 $a$ 和 $b$ 的粒子的归一化质量分布梯度，作为各自的界面方向趋势 $\hat{n}_{ia}$ 和 $\hat{n}_{ib}$。接触面法线由两者之差归一化得到：$n_{ia} = -n_{ib} = \frac{\hat{n}_{ia} - \hat{n}_{ib}}{\|\hat{n}_{ia} - \hat{n}_{ib}\|}$。这一设计利用质量分布的空间梯度自动推断接触界面的朝向，无需显式碰撞检测。

2. **动量守恒碰撞力施加**：仅在相对速度条件 $(v_{ia}^{temp} - v_{ib}^{temp}) \cdot n_{ia} > 0$ 满足时（即两物体正在相互靠近），才在网格节点上施加碰撞力：
   $$f_i^c = \frac{p_{ia}^{temp} m_{ia}^n - p_{ib}^{temp} m_{ib}^n}{(m_{ia}^n + m_{ib}^n) \Delta t}, \quad f_{ia}^c = -f_{ib}^c = \mu (f_i^c \cdot n_{ib}) n_{ib}$$
   该碰撞力严格满足动量守恒，确保总动量不因碰撞处理而漂移（Figure 7 验证了总动量恒定）。消融实验（Figure 6）表明，启用 Collision-MPM 后，断裂的木质碎片呈现自然分离行为，而非黏附在茶壶表面。

### 创新二：断裂感知的高斯粒子优化

现有方法（如 **PhysGaussian**）未处理断裂面的高斯属性生成，断裂后暴露的内部区域缺乏对应的渲染基元，导致视觉空洞或纹理失真。Fracture-GS 提出一套完整的断裂粒子追踪与高斯属性重建管线：

1. **基于硬化参数的断裂追踪**：采用 NACC 弹塑性本构模型（Wolper et al., 2019）中的硬化参数 $\alpha$ 作为断裂判据。当粒子从塑性区进入完全断裂状态时，系统动态识别这些“断裂粒子”作为新高斯生成的候选位置（Figure 3 右）。

2. **MVEE 优化重建高斯属性**：对于每个新暴露的断裂粒子，搜索其空间邻居中的已有高斯粒子。通过计算这些邻居高斯的**最小体积外接椭球**（Minimal-Volume Enclosing Ellipsoid, MVEE），直接生成新粒子的位置 $\mu_{new}$ 和协方差矩阵 $\boldsymbol{\Sigma}_{new}$：
   $$\{\mu_{new}, \boldsymbol{\Sigma}_{new}\} = \mathbf{MVEE}(\boldsymbol{\Omega}_{cross}(g_i, g_j))$$
   颜色属性则通过邻居高斯的颜色插值或继承获得。MVEE 优化使得新生成的高斯粒子在空间分布和形状上与周围已有粒子保持连贯，避免断裂面出现突兀的几何不连续（Figure 4）。

3. **遮挡感知渲染**：在最终渲染阶段，若某像素的渲染路径上存在多个经断裂优化生成的高斯粒子，仅最近粒子参与着色。这一遮挡感知采样策略避免了断裂面内部重叠粒子造成的视觉混乱。

### 与基线方法的关键差异

| 改进维度 | 基线方法（MLS-MPM / PhysGaussian） | Fracture-GS |
|---------|--------------------------------|-------------|
| 碰撞处理 | 无碰撞力或简单惩罚力，产生黏附伪影 | 基于质量分布梯度的动量守恒界面力 |
| 断裂追踪 | 无专门追踪机制 | 硬化参数 $\alpha$ 驱动的动态断裂粒子识别 |
| 断裂面渲染 | 无断裂面高斯生成 | MVEE 优化的邻居插值高斯重建 |
| 渲染遮挡 | 标准 alpha 混合 | 遮挡感知采样，仅最近粒子着色 |

这些创新使 Fracture-GS 在定量指标（PSNR 21.1, LPIPS 0.29, Figure 5）和定性视觉质量上均优于现有方法，同时保持了物理守恒律（动量守恒、能量有界，Figure 7-8）。

> **注意**：该方法对隐藏/不可见区域的断裂面缺乏纹理信息，可能导致 FID 指标偏高；未来工作可探索 3D AI 纹理修复以改善此问题。

Fracture-GS 构建了一条从多视图图像到动态断裂渲染的端到端管道，其核心设计围绕“物理模拟—几何追踪—外观重建”三个阶段的紧密耦合展开。整个框架的输入为物体的多视图 RGB 图像，输出为任意视角下具有物理一致断裂效果的高质量渲染序列。

**管道总览**（对应 Figure 2）包含五个递进模块：

1. **SDF 隐式重建与粒子采样**：首先从多视图图像中隐式重建物体的符号距离函数（SDF），随后在 SDF 约束域内进行体素均匀随机采样，同时生成表面粒子和内部粒子。表面粒子用于后续高斯外观学习，内部粒子则为 MPM 动力学模拟提供体积支撑，确保空间连续性与力学响应的完整性。

2. **表面粒子高斯属性学习**：利用输入图像，通过 3D Gaussian Splatting 框架对表面粒子进行训练，学习各向同性高斯核的外观参数（颜色、不透明度等）。这一阶段为所有后续渲染帧奠定了外观基础。

3. **碰撞 MPM 动力学模拟**：这是框架的物理核心。采样后的所有粒子（表面+内部）进入改进的 Collision-MPM 求解器，经历极端机械碰撞仿真。该求解器集成了三个关键机制：（a）基于归一化质量分布的动量守恒界面力，用于消除多体碰撞中的非物理黏附；（b）NACC 弹塑性本构模型，控制材料的屈服与塑性流动；（c）动态断裂准则，通过硬化参数 α 实时判定粒子是否进入断裂状态。

4. **断裂粒子追踪与高斯优化**：模拟过程中，根据硬化参数 α 动态识别暴露的断裂粒子。对于这些新生的断裂面粒子，利用最小体积外接椭球（MVEE）对其邻居高斯进行属性重构，生成新粒子的空间位置和协方差矩阵，颜色则通过继承或插值获得。这一策略使得断裂面的外观与周围已学习表面保持几何与光度一致性。

5. **实时高斯泼溅渲染**：将所有高斯粒子（含优化后的断裂粒子）投影到图像平面，经遮挡感知采样后执行 alpha 混合，输出最终渲染帧。遮挡感知采样确保当像素渲染路径上存在多个优化粒子时，仅最近粒子参与着色，避免断裂面内部的视觉混乱。

**输入输出流**：输入为多视图图像与预定义的材料物理参数（杨氏模量、泊松比、屈服应力等，见 Table 1）；输出为动态断裂过程的连续渲染帧序列。管道中，SDF 重建与高斯学习阶段在模拟前一次性完成，而 MPM 模拟、断裂追踪与渲染在每帧迭代执行，形成“模拟—追踪—渲染”的闭环。

![[assets/figures/papers/paper_list_l48_https_openreview_net_forum_id_zcAwK50ft0/figures/002_Figure_2.jpg]]
*Figure 2: Pipeline. The object is implicitly reconstructed from multi-view images, followed by sampling both surface and internal particles. Surface particles learn Gaussian attributes using isotropic kernels. Next, the sampled particles undergo extreme mechanical collision simulation with dynamic fracture using our enhanced Collision-MPM. Finally, fracture particles are tracked and their Gaussian attributes are optimized through our proposed Fracture Particle Gaussian Optimization strategy, enabling high-quality rendering of the simulation results. For Collision-MPM, the key parameters are highlighted in red. The yield surface determines whether a particle enters the plastic region, triggering a ret...*

### 3.1 Collision-MPM：动量守恒的碰撞界面处理

Fracture-GS 的核心物理引擎建立在 **MLS-MPM**（Hu et al., 2018）框架之上，但标准 MLS-MPM 在处理多物体极端碰撞时存在致命缺陷：网格节点上不同物体的粒子共享同一速度场，导致非物理的黏附与穿透。为解决这一问题，Fracture-GS 提出了 **Collision-MPM** 模块，其关键创新在于引入基于归一化质量分布的动量守恒碰撞力。

**界面方向趋势与接触法线**

碰撞处理的核心挑战在于如何确定两物体在网格节点处的接触法线方向。Fracture-GS 不依赖显式几何碰撞检测，而是通过分析网格节点上两物体粒子的质量分布梯度来计算“界面方向趋势”（interface direction tendency）：

$$
\hat{n}_{ia} = \frac{\sum_{p_a} m_a \nabla \omega_{ia} (x_i - x_a^n)}{\|\sum_{p_a} m_a \nabla \omega_{ia} (x_i - x_a^n)\|}, \quad \hat{n}_{ib} = \frac{\sum_{p_b} m_b \nabla \omega_{ib} (x_i - x_b^n)}{\|\sum_{p_b} m_b \nabla \omega_{ib} (x_i - x_b^n)\|}
$$

其中，$\hat{n}_{ia}$ 和 $\hat{n}_{ib}$ 分别表示物体 $a$ 和 $b$ 在网格节点 $G_i$ 处的质量分布趋势方向。接触面法线则通过两趋势方向的差归一化得到：

$$
n_{ia} = -n_{ib} = \frac{\hat{n}_{ia} - \hat{n}_{ib}}{\|\hat{n}_{ia} - \hat{n}_{ib}\|}
$$

这一设计的物理直觉在于：当两物体的粒子在网格节点处相互接近时，其质量分布梯度的方向差异反映了接触界面的几何走向。

**动量守恒碰撞力**

碰撞力仅在满足相对速度条件时激活，即当两物体在法线方向上相互靠近时才施加：

$$
(v_{ia}^{temp} - v_{ib}^{temp}) \cdot n_{ia} > 0
$$

满足条件时，基于动量守恒原理计算网格节点上的碰撞力：

$$
f_i^c = \frac{p_{ia}^{temp} m_{ia}^n - p_{ib}^{temp} m_{ib}^n}{(m_{ia}^n + m_{ib}^n) \Delta t}
$$

其中 $p_{ia}^{temp} = m_{ia}^n v_{ia}^{temp}$ 为临时动量。该碰撞力随后分解到两物体的粒子上：

$$
f_{ia}^c = -f_{ib}^c = \mu (f_i^c \cdot n_{ib}) n_{ib}
$$

参数 $\mu \in [0,1]$ 控制碰撞力强度。这一公式保证了碰撞过程中总动量的严格守恒（见 Figure 7 验证），同时有效消除了传统 MPM 中常见的非物理黏附现象。

### 3.2 断裂粒子追踪与高斯属性优化

**硬化参数驱动的断裂追踪**

Fracture-GS 采用 **NACC 本构模型**（Wolper et al., 2019）描述材料的弹塑性行为，其中硬化参数 $\alpha$ 记录了粒子经历的塑性变形累积。当 $\alpha$ 超过预设阈值时，粒子被标记为“断裂粒子”——这些粒子原本位于物体内部，因断裂而暴露为新表面。

如 Figure 3（右）所示，断裂追踪在每个时间步动态执行：随着碰撞与变形加剧，越来越多的内部粒子因塑性累积而被识别为断裂粒子，从而驱动断裂面的动态演化。

**MVEE 优化重构高斯属性**

断裂粒子本身缺乏外观信息（它们原本是不可见的内部粒子），直接渲染会导致断裂面出现空洞或颜色异常。Fracture-GS 通过 **最小体积外接椭球**（MVEE）优化来解决这一问题：

$$
\{\mu_{new}, \boldsymbol{\Sigma}_{new}\} = \mathbf{MVEE}(\boldsymbol{\Omega}_{cross}(g_i, g_j))
$$

具体而言，对于每个断裂粒子，搜索其空间邻域内已有的表面高斯粒子，计算这些邻居高斯粒子“交叉区域”的 MVEE，以此重构新粒子的空间均值 $\mu_{new}$ 和协方差矩阵 $\boldsymbol{\Sigma}_{new}$。颜色属性则通过邻居高斯插值或直接继承获得。

**遮挡感知采样**

在最终渲染阶段，Fracture-GS 实施遮挡感知采样策略：若某像素的渲染路径上包含多个经优化生成的新粒子，仅最近的新粒子参与着色。这一设计避免了断裂面内部粒子的错误叠加，确保渲染的物理一致性。

### 3.3 管道模块总览

Fracture-GS 的完整管道（见 Figure 2）由以下关键模块串联构成：

1. **SDF 隐式重建与粒子采样**：从多视图图像重建物体的符号距离函数（SDF），在 SDF 约束域内均匀随机采样内部粒子，同时采样表面粒子用于后续高斯学习。
2. **表面粒子高斯属性学习**：利用输入图像通过 3D Gaussian Splatting 训练表面粒子的各向同性高斯核参数。
3. **Collision-MPM 动力学模拟**：使用改进的 Collision-MPM 进行多物体极端碰撞仿真，包含动量守恒界面力、NACC 弹塑性本构和动态断裂。
4. **断裂粒子高斯优化**：根据硬化参数 $\alpha$ 追踪暴露的断裂粒子，利用 MVEE 插值邻居高斯生成新粒子的空间参数。
5. **实时高斯泼溅渲染**：将优化后的高斯粒子经遮挡感知采样投影并混合，输出最终图像。

各模块间的数据流与参数传递关系在 Figure 2 中以红色高亮标注，其中屈服面判定决定了粒子是否进入塑性区域并触发返回映射（return mapping）以更新变形梯度。

## 实验与关键发现

### 主实验结果

Fracture-GS 在定性与定量评估中均优于现有基线方法。Figure 5 展示了综合对比结果，所提方法在 PSNR（21.1）、LPIPS（0.29）、FID 和 FSF 四项指标上均取得最优成绩。对比基线包括 **MLS-MPM**（Hu et al., 2018）、**PhysGaussian**（Xie et al., 2024）和 **GIC**（Cai et al., 2024）。其中，MLS-MPM 因缺乏专门的碰撞力处理，在极端机械碰撞场景中产生明显的非物理黏附伪影；PhysGaussian 虽集成高斯泼溅与 MPM，但未对断裂面进行专门渲染优化；GIC 则聚焦于物理参数估计，完全不考虑断裂动力学。Fracture-GS 通过动量守恒碰撞力消除黏附，并结合断裂粒子追踪与 MVEE 优化生成高质量断裂面渲染，在视觉真实性与物理一致性上均形成显著优势。

![[assets/figures/papers/paper_list_l48_https_openreview_net_forum_id_zcAwK50ft0/figures/006_Figure_5.jpg]]
*Figure 5: Integrated comparison showing both qualitative visualizations (left) and quantitative metrics (right), with our method achieving the best results*

实验覆盖了多种碰撞场景：单物体撞击（花盆撞墙）、多物体碰撞交互（茶壶撞桌子、碗撞茶壶、榕树撞桌子），以及真实世界数据验证（DTU 数据集上的三个物体）。Figure 10 和 Figure 11 分别展示了这些场景的渲染结果，验证了方法在合成数据与真实数据上的泛化能力。

**公平性说明**：定量评估采用自参照协议，以断裂前最后一帧为参考图像计算 PSNR、LPIPS、FID 等指标。这一设计是实用折衷——目前缺乏真实动态断裂序列的基准数据集。指标反映的是视觉连贯性而非绝对物理精度，未来需发展物理渲染专用度量。此外，该方法缺少与其他基于物理的方法（如基于 FEM 的断裂模拟）的直接定量对比，现有对比主要限于 MPM 变体与高斯泼溅方法。

### 消融实验

#### 碰撞力机制消融

Figure 6 展示了 Collision-MPM 碰撞力机制的消融效果。在茶壶撞击桌子的场景中，无碰撞力处理的 MLS-MPM 导致木材碎片黏附在茶壶表面，呈现非物理的粘连行为；而引入基于归一化质量分布的动量守恒碰撞力后，木材碎片呈现自然的分离与飞散。Figure 7 进一步验证了动量守恒性质——两物体碰撞过程中，系统总动量（黑色曲线）保持恒定，单个物体的动量在撞击瞬间发生交换，严格遵循守恒定律。Figure 8 的能量分析表明，系统的动能、弹性能和重力势能总和保持有界，无能量非物理增长，与碰撞断裂过程的物理演化一致。

![[assets/figures/papers/paper_list_l48_https_openreview_net_forum_id_zcAwK50ft0/figures/007_Figure_6.jpg]]
*Figure 6: Collision-MPM effectively resolves the non-physical adhesion artifacts in multi-body collisions. As demonstrated in the red box regions, wood fragments from the fractured table exhibit natural separation behavior rather than adhering unnaturally to the teapot surface*

![[assets/figures/papers/paper_list_l48_https_openreview_net_forum_id_zcAwK50ft0/figures/008_Figure_7.jpg]]
*Figure 7: Momentum conservation during a collision between two objects. The total momentum (black curve) remains constant throughout the simulation, demonstrating strict adherence to the conservation law, while the individual momenta of the objects exchange during the impact*

![[assets/figures/papers/paper_list_l48_https_openreview_net_forum_id_zcAwK50ft0/figures/009_Figure_8.jpg]]
*Figure 8: Energy evolution and qualitative visualization during the teapot-table collision and fracture simulation. The top and middle rows plot the kinetic, elastic, and gravitational potential energy components for the table surface, the teapot, and the combined system over the first 50 frames, showing bounded total energy without non-physical growth. The bottom row provides corresponding qualitative visualizations at key frames (t=0,10,20,30,40,50), depicting the physical progression of the collision and fracture process that correlates with the energy transitions observed in the graphs*

#### 断裂粒子追踪与高斯优化消融

Table 2 报告了断裂粒子追踪对渲染性能的影响。引入断裂粒子高斯优化后，每帧渲染时间增加约 20–80%（例如 Ficus 场景从 49.19 ms 增至 62.78 ms），但整体仍保持高效。这一开销源于 MVEE 优化与遮挡感知采样的计算，但换取了断裂面渲染质量的显著提升。

![[assets/figures/papers/paper_list_l48_https_openreview_net_forum_id_zcAwK50ft0/figures/011_Table_2.jpg]]
*Table 2: Per-frame Gaussian rendering time*

#### 硬化因子消融

Figure 9 展示了不同初始硬化因子对断裂模式的影响。增大初始硬化因子系统性地增强物体碎裂程度和裂缝扩展范围，验证了基于硬化参数 α 的断裂追踪准则对材料塑性的敏感性。这一参数直接控制 NACC 本构模型中粒子进入塑性区域的阈值，从而影响断裂面的生成密度与分布。

#### 内部采样密度消融

Table 3 和 Figure 12 展示了内部粒子采样密度对模拟精度的影响。随采样密度增加，坐标误差呈收敛趋势，但不同密度导致不同的断裂模式与碰撞动力学响应——这是粒子法的固有特性，而非方法缺陷。Figure 12 的可视化对比显示，低采样密度下断裂面较粗糙，高密度下裂纹更精细，但计算成本相应增加。

### 失败模式与局限性

1. **隐藏区域纹理缺失**：对于碰撞后新暴露的断裂面（原为物体内部不可见区域），缺乏纹理信息，导致该区域的 FID 等指标偏高。这是从多视图表面重建到内部断裂面泛化的固有问题，论文指出未来可探索基于 3D AI 的纹理生成修复。

2. **自参照评估的局限**：PSNR、LPIPS、FID 等指标以断裂前帧为参考，仅衡量视觉连贯性。当断裂面纹理与原始表面差异较大时，这些指标无法区分“物理正确的断裂面”与“渲染伪影”。需要发展专门用于物理渲染的评估度量。

3. **参数敏感性**：硬化因子、内部采样密度等参数直接影响断裂模式与模拟精度，论文未系统报告方法对这些参数的敏感度及所需的手动调参程度。实际应用中可能需要针对不同材质进行参数搜索。

4. **材料参数依赖**：Table 1 列出了各物体的材料参数（杨氏模量、泊松比、屈服应力等），这些参数的选择依赖领域知识，论文未探讨参数估计的自动化方法。

## 定位与知识库关联

### 任务定位与基线关系

Fracture-GS 处于**物理模拟与可微渲染的交叉地带**，其核心任务是在保持物理一致性的前提下，实现极端碰撞与动态断裂场景的高质量新视角合成。该工作直接建立在两条技术路线之上：

**材料点法（MPM）模拟线**：以 **MLS-MPM**（Hu et al., 2018）为底层动力学框架，沿用了其 P2G（粒子到网格）、网格更新、G2P（网格到粒子）三阶段范式。然而，标准 MLS-MPM 在处理多物体碰撞时缺乏专门的界面力机制，导致物体在接触区域产生**非物理黏附伪影**——碰撞后的碎片错误地附着在对方表面而非自然分离。Fracture-GS 通过在网格节点引入基于归一化质量分布的动量守恒碰撞力，从根本上解决了这一缺陷。

**3D 高斯泼溅（3DGS）渲染线**：以 **PhysGaussian**（Xie et al., 2024）为代表的 MPM-GS 集成方法，将高斯粒子绑定到 MPM 模拟粒子进行渲染，但未处理断裂面的高斯属性生成问题。当物体碎裂时，新暴露的内部表面缺乏对应的高斯表示，导致渲染质量严重退化。Fracture-GS 通过断裂粒子追踪与最小体积外接椭球（MVEE）优化，动态生成断裂面的高斯属性，填补了这一空白。

与 **GIC**（Cai et al., 2024）等利用高斯可微性进行物理参数估计的工作不同，Fracture-GS 关注的是模拟到渲染的闭环，而非参数逆向推断。

### 核心创新机制

Fracture-GS 的方法创新可归纳为三个紧密耦合的模块：

1. **碰撞界面力计算**：在每个网格节点上，分别计算两物体粒子的质量分布梯度作为“界面方向趋势”，其差值方向即为接触面法线。仅当两物体在该节点的临时速度沿法线方向相互靠近时，才施加动量守恒的碰撞力。这一条件门控机制既阻止了穿透，又避免了非物理黏附。

2. **硬化参数驱动的断裂追踪**：采用 NACC 本构模型（Wolper et al., 2019）中的硬化参数 α 作为断裂判据——当粒子的塑性累积超过阈值时，标记为断裂粒子。这比纯几何追踪更具物理依据，因为 α 直接反映材料的损伤演化。

3. **MVEE 断裂面高斯优化**：对于新暴露的断裂粒子，通过其邻居高斯粒子的空间分布计算最小体积外接椭球，以此重构新粒子的位置均值和协方差矩阵。颜色属性通过邻居插值继承。渲染时采用遮挡感知采样，仅最近的新粒子参与着色，避免重叠高斯导致的伪影。

### 适用边界与局限

**适用场景**：该方法适用于已知几何和外观的刚体/弹塑性物体之间的极端碰撞与断裂模拟，特别是需要高质量渲染断裂面的场景。论文在合成物体（茶壶、桌子、榕树等）和真实世界数据（DTU 数据集）上均验证了有效性。

**关键局限**：

- **评估基准缺失**：定量指标（PSNR、LPIPS、FID）采用自参照协议，以断裂前最后一帧为参考帧，衡量的是视觉连贯性而非绝对物理精度。目前缺乏针对动态断裂渲染的专用评估度量和真实动态序列基准。
- **采样密度敏感性**：内部粒子采样密度直接影响断裂模式和碰撞动力学响应，这是粒子法的固有特性，不同密度会导致不同的力学行为（Table 3、Figure 12 证实了这一点）。
- **隐藏区域纹理缺失**：断裂暴露的内部表面在原始多视图图像中不可见，缺乏纹理信息，导致 FID 等分布度量偏高。论文提出未来可借助 3D AI 纹理生成修复来改善。
- **参数调校负担**：方法涉及材料参数（杨氏模量、泊松比、硬化因子等）和模拟参数（采样密度、网格分辨率等），其对结果的影响程度和手动调校需求未充分讨论。

### 开放问题

1. **物理渲染专用度量**：现有图像质量指标（PSNR、LPIPS、FID）无法区分“视觉上合理但物理上错误”的渲染结果，需要发展能够评估断裂面几何一致性和物理合理性的专用度量。
2. **纹理生成修复**：如何利用 3D 生成模型为隐藏断裂面合成物理一致的纹理，是一个有价值但尚未探索的方向。
3. **参数敏感度量化**：物理参数（尤其是硬化因子 α）对断裂模式的影响虽已通过消融实验定性展示，但缺乏系统性的敏感度分析和自动调参策略。
4. **与物理模拟基线的直接对比**：当前定量评估主要与 PhysGaussian 等渲染基线对比，缺少与专业断裂模拟软件或高级 MPM 变体的直接物理精度对比。
5. **计算效率的进一步优化**：断裂粒子追踪使每帧渲染时间增加约 20–80%（如 Ficus 场景从 49.19ms 增至 62.78ms），在实时应用场景下仍有优化空间。

## 原文 PDF

![[paperPDFs/ICLR_2026/Fracture_GS_Dynamic_Fracture_Simulation_with_Physics_Integrated_Gaussian_Splatti_ec080bbb2d3d.pdf]]
