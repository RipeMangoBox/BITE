---
title: Efficient Kinetic Simulation of Two-Phase Flows
type: paper
paper_level: A
venue: SIGGRAPH
year: 2022
pdf_ref: paperPDFs/SIGGRAPH_2022/Efficient_Kinetic_Simulation_of_Two_Phase_Flows.pdf
project_link: "https://libigl.github.io/"
code_link: null
aliases:
- VPLMC
- EKSTPF
tags:
- SIGGRAPH_2022
- topic/other_unclear
core_operator: 在相场演化方程中引入源项S_φ以补偿砂粒运动引起的有效体积变化，并通过比例控制器进行实时体积校正。
primary_logic: 将混合物中砂粒位移导致的流体体积分数变化作为相场方程的对流-扩散源项，从而在无需全局压力投影的条件下维持流体体积守恒。
claims:
- 移除相场源项S_φ后，砂块落入水中时水位不上升，流体体积损失约30%。
- 启用比例控制器后，全局流体体积波动保持在1%以内；关闭控制器则体积变化达5%。
- 在砂块跌落烧杯的场景中，本方法与Tang et al. 2025相比，每帧计算时间从10.3分钟降至0.87分钟，加速12倍，同时产生更丰富的气泡和飞溅细节。
- Sand drop in beaker 上 计算时间 (分钟/帧) = 0.87 mins
---

# Efficient Kinetic Simulation of Two-Phase Flows

> [!tip] 核心洞察
> 将混合物中砂粒位移导致的流体体积分数变化作为相场方程的对流-扩散源项，从而在无需全局压力投影的条件下维持流体体积守恒。

| 字段 | 内容 |
|------|------|
| 中文题名 | 面向空气-水-沙混合物的体积保持LBM-MPM耦合方法 |
| 英文题名 | Efficient Kinetic Simulation of Two-Phase Flows |
| 会议/期刊 | SIGGRAPH 2022 |
| Links | [paper](http://www.geometry.caltech.edu/pubs.html) · [Project](https://libigl.github.io/) |
| Topic | #topic/other_unclear |
| Method | Volume-Preserving LBM-MPM Coupling |
| Dataset | Sand drop in beaker |

> [!tip] 效果简介
> - Sand drop in beaker 上，计算时间 (分钟/帧) 0.87 mins vs 10.3 mins (Tang et al. 2025) (12× 加速)。

## 概要

现有空气‑水‑沙三相耦合仿真方法面临一个核心矛盾：基于不可压缩Navier‑Stokes投影的方案能保证体积守恒，但无法产生气泡、飞溅等两相界面细节；而可压缩多相流求解器虽能捕捉丰富界面，却难以维持混合物的流体体积守恒。本文提出一种**体积保持的LBM‑MPM耦合方法**，将速度基格子玻尔兹曼方法（LBM）两相流求解器与物质点法（MPM）砂粒求解器结合，通过统一的连续介质框架实现空气‑水‑沙的高效耦合。其关键创新在于：在相场演化方程中引入一个**源项 $S_\phi$**，补偿砂粒运动引起的有效流体体积分数变化，并辅以全局比例控制器实时校正体积漂移，从而在无需全局压力投影的条件下维持流体体积守恒。实验表明，该方法在砂块跌落烧杯场景中相较 **Tang et al. (ACM Trans. Graph. 2025)** 的Granule‑in‑Cell方法加速约**12倍**（0.87分钟/帧 vs. 10.3分钟/帧），同时产生更丰富的气泡和飞溅细节；消融实验证实移除源项后流体体积损失约30%，而启用比例控制器可将体积波动控制在**1%以内**。方法定位于LBM‑MPM耦合框架下的**相场体积补偿**机制，通过修改相场方程的对流‑扩散源项插槽，为高效、体积守恒的气‑液‑固三相交互仿真提供了新路径。

## 核心方法与创新机理

### 问题背景与核心瓶颈

空气-水-沙三相混合物的物理仿真面临一个根本性矛盾：基于不可压缩Navier-Stokes投影的方法（如Tang et al. 2025的Granule-in-Cell方法）虽能保证体积守恒，却难以高效捕获气泡、飞溅等两相界面细节；而基于弱可压缩LBM的方法虽天然适合界面丰富的多相流，却因砂粒运动不断改变有效流体体积，导致全局流体质量漂移。**核心瓶颈**在于：如何在无需全局压力投影的条件下，使弱可压缩两相流求解器感知并补偿砂粒位移引起的有效体积变化，从而同时实现高计算效率、体积守恒与丰富的界面细节。

### 核心创新：相场源项驱动的体积守恒机制

本文的核心洞察是将砂粒运动对流体体积的排挤效应建模为相场方程的对流-扩散源项。在混合物描述中，流体相的有效体积分数为 $\epsilon = 1 - \varepsilon$，其中 $\varepsilon$ 为砂粒体积分数。当砂粒运动导致 $\epsilon$ 的时空分布发生变化时，即使流体本身不可压缩，相场 $\phi$ 的对流也会因载流体积收缩/膨胀而产生表观的质量变化。作者在保守相场方程中显式引入源项 $S_\phi$，使相场演化直接响应 $\epsilon$ 的变化：

$$\frac{\partial\phi}{\partial t} + \nabla\cdot(\phi\mathbf{u}) = \nabla\cdot\left[M\left(\nabla\phi - \frac{4}{\xi}\phi(1-\phi)\mathbf{n}\right)\right] - \underbrace{\frac{\phi}{\epsilon}\left(\frac{\partial\epsilon}{\partial t} + \mathbf{u}\cdot\nabla\epsilon\right)}_{S_\phi}$$

该源项的物理意义明确：$\frac{\partial\epsilon}{\partial t}$ 补偿砂粒体积分数的当地变化率，$\mathbf{u}\cdot\nabla\epsilon$ 补偿流体对流经过非均匀砂粒分布时经历的有效截面积变化。两项共同保证相场对流与混合物连续性方程自洽。这一设计将体积守恒从全局投影解耦为局部相场修正，是本文的**因果旋钮**——消融实验证实，移除 $S_\phi$ 后砂块落入水中时水位不上升，流体体积损失约30%（Fig. 14）。

### 全局比例控制器的补充作用

仅靠局部源项无法完全消除离散误差累积，因此作者引入全局比例控制器 $\gamma(t)$，在每一时间步对相场进行均匀缩放：

$$\phi^{n+1}(\mathbf{x}) = \gamma(t)\,\phi^*(\mathbf{x}), \quad \gamma(t) = \frac{V_{\text{target}}}{V_{\text{current}}}$$

其中 $V_{\text{target}}$ 为初始流体体积，$V_{\text{current}}$ 为当前相场积分值。该控制器使全局流体体积波动保持在1%以内；关闭控制器则波动达5%（Fig. 14）。值得注意的是，比例控制器可能引入局部质量再分配误差，其在高密度比或剧烈相变场景下的鲁棒性有待进一步验证。

### 方法框架与模块因果链

整体框架由五个耦合模块构成，数据流沿“LBM流体求解→MPM砂粒求解→相场体积修正→双向动量耦合→水分保持”的闭环运行：

**模块1：速度基LBM两相流求解器。** 采用D3Q27晶格与NOCM-MRT碰撞模型，演化方程为：

$$f_j(\mathbf{x}+\mathbf{c}_j, t+1) = f_j(\mathbf{x},t) + \Omega_j(\mathbf{x},t) + \mathbf{F}_j(\mathbf{x},t)$$

其中碰撞算子 $\Omega = -\mathbf{M}^{-1}\mathbf{R}(\mathbf{m} - \mathbf{m}^{\text{eq}})$ 在非正交中心矩空间中执行多松弛碰撞。与标准BGK碰撞相比，NOCM-MRT通过分离低阶和高阶矩的松弛速率（低阶矩松弛至平衡态，高阶矩松弛速率设为1以抑制非物理振荡），显著提高了高密度比（空气-水约1000:1）两相流的数值稳定性。宏观量恢复为：

$$\rho = \sum_j f_j, \quad \rho\mathbf{u} = \sum_j \mathbf{c}_j f_j + \frac{1}{2}\mathbf{F}$$

强迫项 $\mathbf{F}$ 整合表面张力 $\mathbf{F}_s$、重力 $\mathbf{F}_b$、粘性力 $\mathbf{F}_\mu$ 以及来自砂粒的拖曳力 $\mathbf{F}_d$。

**模块2：MPM砂粒求解器。** 砂粒视为连续介质，通过APIC（Affine Particle-In-Cell）转移将拉格朗日颗粒的质量、动量和仿射速度映射到背景网格。颗粒应力由弹塑性本构（含Mohr-Coulomb屈服准则）给出，更新后的网格速度映射回颗粒以推进位置。MPM与LBM共享同一背景笛卡尔网格，避免了网格间插值误差。

**模块3：相场求解器（含源项）。** 在D3Q7晶格上求解增广相场方程，引入 $S_\phi$ 源项并施加比例控制。D3Q7晶格（7个离散速度）足以解析相场的对流-扩散动力学，相比D3Q27显著节省计算和内存。

**模块4：流体-砂粒双向耦合模块。** 这是连接模块1和模块2的关键桥梁，包含三个子机制：

- **拖曳力耦合**：作用于砂粒节点的拖曳力密度为 $\mathbb{F}_d^i = w(\mathbf{u}_i, \mathbf{v}_i)(\mathbf{u}_i - \mathbf{v}_i)$，其中 $w$ 为依赖局部雷诺数和砂粒渗透率的拖曳系数。等大反向的力以累积形式反馈至LBM的强迫项。
- **浮力与压力耦合**：砂粒承受的浮力直接由流体压力梯度给出，而流体压力更新方程显式包含砂粒体积分数变化与滑移速度的贡献：

$$p^{n+1} = p^n - c_s^2\rho^{n+1}\left(1 - \sum_j f_j(\mathbf{x},t) + \frac{\varepsilon\nabla\cdot\mathbf{v} + (\mathbf{u}-\mathbf{v})\cdot\nabla\epsilon}{\epsilon}\right)$$

这一修正确保混合物层面的不可压缩性，是本文相对于Tang et al. 2025（依赖泊松方程求解压力）的**核心变化槽位**之一。

- **动量交换守恒**：双向耦合严格保证流体与砂粒的总动量守恒，避免界面处的非物理能量注入。

**模块5：水分保持模块。** 引入颗粒束缚水分质量 $r_p(t)$ 和有效孔隙率 $\hat{\epsilon}_i(t) = 1 - \varepsilon_i(t) - R_i(t)$，其中 $R_i(t)$ 为束缚水分体积分数。水分吸收速率正比于当地水相体积分数与颗粒未饱和容量的乘积，释放速率则由经验参数控制。该模块延迟湿润锋推进（Fig. 10），并通过饱和度依赖的粘聚力增强湿砂结构完整性（Fig. 17）。

### 与基线方法的关键差异

| 变化槽位 | 基线方法（Tang et al. 2025） | 本文方法 |
|---------|---------------------------|---------|
| 流体体积守恒机制 | 隐式密度投影（全局泊松求解） | 相场源项 $S_\phi$ + 比例控制器 $\gamma(t)$ |
| 基础流体求解器 | 基于网格的不可压缩Navier-Stokes投影 | 速度基D3Q27 LBM，NOCM-MRT碰撞 |
| 压力更新 | 泊松方程求解，未显式耦合砂粒体积分数 | 式(39)显式包含 $\varepsilon$ 变化与滑移速度 |
| 水分保持模型 | 无 | 束缚水分 $r_p(t)$ + 有效孔隙率 $\hat{\epsilon}_i$ |

这些变化槽位的因果链为：LBM替代投影求解器→计算效率提升约12倍（0.87 vs. 10.3分钟/帧，Fig. 13）；相场源项替代全局投影→在保持体积守恒的同时释放界面细节（气泡、飞溅）；压力更新显式耦合砂粒→消除流体-砂粒界面的压力不连续；水分保持→丰富湿润/干燥过渡行为。

### 关键公式变量含义速查

- $\phi$：相场序参数（$\phi=0$ 为空气，$\phi=1$ 为水）
- $\epsilon = 1 - \varepsilon$：流体有效体积分数
- $\mathbf{u}$：流体速度；$\mathbf{v}$：砂粒速度
- $M$：迁移率；$\xi$：界面厚度参数
- $c_s$：LBM声速；$\rho$：混合物密度
- $\mathbf{F}_d$：拖曳力密度；$\mathbf{F}_s$：表面张力；$\mathbf{F}_\mu$：粘性力
- $r_p(t)$：颗粒束缚水分质量；$R_i(t)$：束缚水分体积分数
- $\hat{\epsilon}_i$：有效孔隙率（排除砂粒和束缚水分后的可流动体积分数）

![[assets/figures/papers/paper_list_l36_http_www_geometry_caltech_edu_pubs_html/figures/010_Figure_10.jpg]]
*Figure 10: Water retention. To demonstrate the effects of our retention model, we place two sand-filled pipes in the openings of a partition wall. Water retention is enabled for the sand within the background pipe (farthest from the camera), and disabled for the sand in the foreground pipe. With water on one side of the partition, it infiltrates the sand in the foreground pipe significantly faster, eventually eroding the sand into the pool on the opposite side. In contrast, the background sand (with retention enabled) significantly delays fluid ingress, with the bound moisture helping it to withstand the hydraulic pressure*

## 实验与关键发现

### 主结果：计算效率与视觉丰富度的双重提升

本文的核心定量结果来自砂块跌落烧杯（sand drop in beaker）的标准测试场景。在该场景中，本方法与 **Tang et al. 2025**（Granule-in-Cell, GIC）进行了直接对比。GIC方法基于不可压缩Navier-Stokes投影，能够保持体积守恒，但无法产生气泡和飞溅等两相界面细节；本文的LBM-MPM耦合方法则在保持体积守恒的同时，天然支持气泡生成、飞溅和湿润效应。

定量对比结果（Fig. 13）表明：在相同的场景设置和GPU硬件平台上，本方法每帧计算时间仅需 **0.87分钟**，而Tang et al. 2025的方法需要 **10.3分钟/帧**，实现了约 **12倍的加速**。在视觉质量方面，本方法产生了明显更丰富的气泡和飞溅细节，同时保持了与GIC方法一致的砂-水耦合整体行为。

![[assets/figures/papers/paper_list_l36_http_www_geometry_caltech_edu_pubs_html/figures/015_Figure_13.jpg]]
*Figure 13: Comparison with [Tang et al. 2025]. For a simple sand drop in a beaker, our approach (top) exhibits the same overall coupling behavior between sand and fluid as in [Tang et al. 2025], but with clearly more visible bubbles and splashes, and at a 12 times lower computational cost*

> **公平性说明**：对比所用的Tang et al. 2025方法为作者根据论文描述自行实现的版本，可能未包含原作者的全部优化；双方在同一GPU平台上测试，但实现细节无法完全对齐。因此12倍加速的具体数值需谨慎解读，但效率优势的方向性结论是可靠的。

### 体积守恒：核心机制的消融验证

体积守恒是本文最关键的因果机制。消融实验（Fig. 14, Sec. 5.2）通过砂块落入少量水的场景，系统验证了相场源项 $S_\phi$ 和比例控制器 $\gamma(t)$ 的必要性：

![[assets/figures/papers/paper_list_l36_http_www_geometry_caltech_edu_pubs_html/figures/013_Figure_14.jpg]]
*Figure 14: Volume preservation in sand drop. When a big ball of sand drops in a small amount of water, our approach (c) maintains a near-constant fluid volume in time as indicated in the upper right plot. However, if we remove our source term*

1. **移除相场源项 $S_\phi$**：当砂块落入水中时，水位不上升，流体体积损失约 **30%**。这直接证明了 $S_\phi$ 是补偿砂粒位移引起的有效体积变化的核心机制——没有该源项，相场方程无法感知砂粒对流体空间的挤占。

2. **去除比例控制器**：仅保留 $S_\phi$ 但关闭全局比例控制器时，流体体积波动约 **5%**；而同时启用 $S_\phi$ 和比例控制器后，体积波动控制在 **1%以内**。这表明 $S_\phi$ 提供了局部体积补偿的物理基础，而比例控制器作为全局校正项，有效抑制了数值误差累积导致的长期体积漂移。

这两个消融实验构成了本文最有力的因果证据链：$S_\phi$ 是体积守恒的必要条件，比例控制器是充分条件，二者协同实现了无需全局压力投影的体积保持。

### 水分保持模型的独立效果

水分保持模型（water retention model）是本文的另一关键创新。该模型通过颗粒束缚水分质量 $r_p(t)$ 和有效孔隙率 $\hat{\epsilon}_i$ 延迟水分渗透，并增强湿度依赖的砂粒粘聚力。

Fig. 10 展示了对照实验：两个砂管分别置于隔板两侧，背景砂管启用水分保持，前景砂管关闭该功能。结果表明，关闭水分保持的砂管中水分渗透显著更快，砂粒迅速被侵蚀并冲入另一侧水池；而启用水分保持的砂管中，束缚水分有效延缓了流体侵入，砂柱在静水压力下保持结构完整性。

Fig. 17 进一步验证了湿度诱导的粘聚强化效果：湿砂块在容器移除后因局部饱和度增加了粘聚力，形成柱状结构保持部分完整性；而干砂块则立即坍塌。这两个实验共同证明，水分保持模型通过延迟湿润和增强粘聚力两个通道，显著改变了砂-水混合物的宏观力学行为。

### 参数敏感性：砂密度与表面张力

本文还展示了方法对关键物理参数的合理响应，验证了耦合框架的物理一致性：

- **砂密度控制沉浮行为**（Fig. 8）：密度为 $600\,\text{kg/m}^3$ 的轻砂球落入水中后上浮并在水面附近形成悬浮图案；$950\,\text{kg/m}^3$ 的中等密度砂球呈现中性浮力行为；$1500\,\text{kg/m}^3$ 的重砂球快速沉底并堆积。这一梯度响应符合物理直觉，表明浮力项和拖曳力耦合的正确性。

![[assets/figures/papers/paper_list_l36_http_www_geometry_caltech_edu_pubs_html/figures/008_Figure_8.jpg]]
*Figure 8: Sands of varying densities dropping into water. Sand balls with varying densities (600, 950 and 1500*

- **表面张力控制飞溅形态**（Fig. 6）：低表面张力的液滴撞击沙堆时产生剧烈变形和径向喷砂；高表面张力液滴则迅速收缩，仅造成局部扰动。两种情况下撞击均留下弹坑状印记，但飞溅程度的差异验证了表面张力项在两相流-砂耦合中的正确传递。

![[assets/figures/papers/paper_list_l36_http_www_geometry_caltech_edu_pubs_html/figures/006_Figure_6.jpg]]
*Figure 6: Raindrops falling on sand. Raindrops with two different amounts of surface tension impact a flat sand pile, exhibiting distinct dynamic behaviors. High surface tension (top) quickly contains the droplet which has trapped sand grains, resulting in a local disturbance of the surface. Low surface tension (bottom) allows strong deformation and splashing that ejects sand radially. In both cases, the impact ultimately leaves a crater-like imprint on the sand*

### 计算成本与规模统计

Table 1 汇总了所有算例的物理参数、网格分辨率和计时统计。典型场景的网格规模在 $10^6$–$10^7$ 量级，MPM颗粒数在 $10^5$–$10^6$ 量级。单帧计算时间从砂块跌落的0.87分钟到复杂城市淹没场景的数分钟不等。需要注意的是，LBM采用均匀笛卡尔网格，在高分辨率场景下内存开销较大，这是当前方法的一个工程瓶颈。

### 方法局限与适用边界

本文明确指出的局限性包括：

1. **均匀网格限制**：LBM使用均匀笛卡尔网格，无法自适应加密界面区域，高分辨率场景下内存开销大，限制了可模拟的雷诺数范围。

2. **显式时间积分约束**：MPM模块采用显式积分，砂粒弹性波速限制CFL数；对高刚度材料或极细颗粒，可能要求更小的时间步长，影响整体效率。

3. **经验参数依赖**：水分保持模型依赖若干经验参数（如吸收系数 $R_a$），未经严格的物理校准，在定量预测场景中需谨慎使用。

4. **体积守恒的边界条件**：体积守恒依赖全局比例控制器，可能引入局部质量再分配误差；在极端质量变化场景（如大量流体注入/抽出）下的鲁棒性有待验证。

5. **未验证的极端工况**：文中未展示对极高密度比（如 $>1000:1$）或高马赫数气流的适用性，这些场景可能超出当前弱可压缩LBM的适用范围。

### 与真实实验的定性验证

Fig. 15 将砂块坍塌入水的模拟结果与真实颗粒坍塌实验（Alexandre Kane, 2025）进行了并排对比。模拟忠实地再现了砂块冲击水面产生波浪、砂粒被卷起并向前输运的关键动力学过程。这一对比虽为定性，但为耦合框架的物理合理性提供了外部验证。

![[assets/figures/papers/paper_list_l36_http_www_geometry_caltech_edu_pubs_html/figures/016_Figure_15.jpg]]
*Figure 15: Comparison with granular collapse experiments. A block of sand collapses onto the water and generates a wave, rolling up and carrying the sand forward. Our simulation closely mimics the sand-water dynamics of real-word experiments (showed in top-right snapshots)*

## 定位与知识库关联

本文的核心贡献在于为**空气-水-沙三相混合物仿真**提供了一个新的耦合范式，其相对于已有工作的本质差异体现在四个关键 slot 的改变上。

### 1. 改变的 Slot 与基线差异

**Slot 1：流体体积守恒机制 —— 从“投影”到“相场源项”**

已有方法（如 Tang et al., ACM Trans. Graph. 2025 的 Granule-in-Cell, GIC）通过求解全局泊松方程来强制流体不可压缩性，从而间接保持体积守恒。该方法计算代价高昂（每帧需多轮压力迭代），且难以在弱可压缩框架下自然产生气泡和飞溅。本文**完全移除了压力投影**，转而在相场演化方程中引入源项 $S_\phi = -\frac{\phi}{\epsilon}\left(\frac{\partial\epsilon}{\partial t}+\mathbf{u}\cdot\nabla\epsilon\right)$（Eq. 46），将砂粒位移导致的局部有效体积变化直接补偿为相场界面的对流-扩散源。配合一个全局比例控制器 $\gamma(t)$，流体体积波动被抑制在 1% 以内。这一改变使得体积守恒不再依赖全局压力求解，解耦了守恒性强制与动量更新，是加速 12 倍的结构性原因。

**Slot 2：基础流体求解器 —— 从“不可压缩 N-S 投影”到“速度基 LBM”**

Tang et al. 2025 采用基于网格的不可压缩 Navier-Stokes 投影求解器，每步需构建并求解泊松方程。本文替换为**速度基 D3Q27 LBM**，采用 NOCM-MRT 碰撞模型（Eq. 11）。LBM 的弱可压缩特性天然支持气泡成核与溃灭、飞溅等两相界面现象，且其显式局部演化避免了全局线性系统求解。这一选择是产生“更丰富气泡和飞溅细节”（Fig. 13）的算法基础。

**Slot 3：压力更新与混合物耦合 —— 从“无砂体积分数耦合”到“显式 $\epsilon$ 依赖”**

传统两相流求解器（如 Kugelstadt et al. 2019）的压力更新仅依赖密度变化。本文的压力更新方程（Eq. 39）显式包含砂粒体积分数 $\epsilon$ 的时间变化率与滑移速度 $(\mathbf{u}-\mathbf{v})$ 的贡献：$p^{n+1}=p^n-c_s^2\rho^{n+1}\left(1-\sum_i f_j(\mathbf{x},t)+\frac{\varepsilon\nabla\cdot\mathbf{v}+(\mathbf{u}-\mathbf{v})\cdot\nabla\epsilon}{\epsilon}\right)$。这使得流体压力能实时感知砂粒的聚集/离散运动，实现双向耦合的动量交换，而非仅在拖曳力层面耦合。

**Slot 4：水分保持模型 —— 从“无/简单渗透”到“束缚水质量+有效孔隙率”**

与 **Power Plastics**（Qu et al., ACM Trans. Graph. 2023）仅使用 Herschel-Bulkley 砂模型而无水分吸收机制相比，本文引入了基于颗粒束缚水分质量 $r_p(t)$ 和有效孔隙率 $\hat{\epsilon}_i(t)=1-\varepsilon_i(t)-R_i(t)$ 的水保持模型（Eq. 53-56）。该模型延迟湿润锋推进，增强湿度依赖的粘聚力（Fig. 17），使砂块在浸水后能保持结构完整性，而非立即溃散。

### 2. 知识库挂载点

本文可挂载至以下知识库节点：

- **多相流 LBM 方法**：作为速度基两相 LBM（D3Q27 + NOCM-MRT）在含颗粒混合物中的扩展案例，连接至 Li et al. 2020 的碰撞模型优化工作。
- **MPM 颗粒-流体耦合**：在 Tampubolon et al. 2017 和 Gao et al. 2018 的“双网格质量/动量交换”范式基础上，提供了无需投影的体积守恒替代方案。
- **相场界面追踪**：将相场方程的源项设计从传统的质量转移（如相变模拟）拓展至“颗粒运动引起的体积补偿”，为相场-MPM 耦合提供了新的界面条件处理思路。
- **计算效率优化**：作为“用显式局部 LBM 替代全局压力求解”的典型案例，可与 GPU 加速 LBM 工作（如 Li et al. 2020）对接。

### 3. 适用边界

- **适用场景**：中低密度比（空气-水，约 1000:1）的两相流与中等粒径干/湿砂的耦合；需要丰富界面细节（气泡、飞溅、湿润）的视觉仿真；对计算效率敏感的应用（如交互式预览、大规模场景）。
- **不适用/需谨慎的场景**：极高密度比（>1000:1）或高马赫数气流（文中未验证）；高刚度砂粒材料（显式 MPM 受 CFL 限制）；需要严格物理校准的水分吸收过程（模型含经验参数 $R_a$）；极端质量变化场景下全局比例控制器可能引入局部质量再分配误差。

### 4. 后续工作启发

1. **多速率时间积分**：当前流体与砂粒共享时间步长，受限于砂粒弹性波速。解耦时间步长（LBM 子循环或隐式 MPM）可进一步提升效率。
2. **自适应网格**：LBM 的均匀笛卡尔网格在高雷诺数界面区域分辨率不足。多分辨率 LBM 与 MPM 自适应采样结合，有望以更低成本解析界面细节。
3. **尖锐界面气泡模型**：当前扩散界面方法可能导致小气泡数值耗散消失。将 HOME-FREE 等自由表面 LBM 与显式气泡粒子耦合，可保持气泡长期存在。
4. **非球形/粘性细颗粒扩展**：当前砂模型为球形颗粒假设，水分保持模型的经验参数需通过物理实验校准，以支持淤泥、黏土等细颗粒混合物仿真。

## 原文 PDF

![[paperPDFs/SIGGRAPH_2022/Efficient_Kinetic_Simulation_of_Two_Phase_Flows.pdf]]