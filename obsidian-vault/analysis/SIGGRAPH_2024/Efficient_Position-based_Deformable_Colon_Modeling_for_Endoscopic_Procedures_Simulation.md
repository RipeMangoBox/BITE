---
title: Efficient Position-based Deformable Colon Modeling for Endoscopic Procedures Simulation
type: paper
paper_level: A
venue: SIGGRAPH
year: 2024
pdf_ref: paperPDFs/SIGGRAPH_2024/Efficient_Position_based_Deformable_Colon_Modeling_for_Endoscopic_Procedures_Simulation.pdf
project_link: null
code_link: null
aliases:
- EPBDCMXCRF
- EPBDCMEPS
tags:
- SIGGRAPH_2024
- topic/graphics_physical_simulation
core_operator: 采用基于XPBD的Cosserat棒约束与四面体约束组合来模拟结肠变形，并设计针对管状结构的快速样条碰撞检测算法（FSCD），同时利用体积样条统一表示双管状结构。
primary_logic: 通过将结肠和内窥镜表示为带体积信息的样条（体积样条），把碰撞检测问题转化为样条间球-三角形相交测试，结合AABB树宽相位加速，使碰撞检测与三角面片数量解耦；同时用Cosserat棒约束模拟结肠的全局弯曲和扭转，辅以四面体约束模拟周围组织牵拉，在XPBD框架下实现稳定高效的变形仿真。
claims:
- FSCD相比SOLID在32k三角面片、60秒场景下碰撞检测时间从5.65ms降至2.02ms，加速2.8倍，且仿真结果视觉等价（Fig.9, Table 1）。
- 全插入仿真在超过1200个接触点下平均帧率171 FPS，高应力区间平均130 FPS，始终高于110 FPS，满足实时交互要求（Fig.7, Fig.8）。
- 变形模型成功模拟了从直肠到盲肠的完整插入，保留结肠的整体位置和生理弯曲，与X光图像吻合（Fig.10, Fig.11）。
- "Spring Scene (Collision Detection Stress Test) 上 Collision Detection Time = FSCD: 2.02 ms (32k triangles, 60s)"
---

# Efficient Position-based Deformable Colon Modeling for Endoscopic Procedures Simulation

> [!tip] 核心洞察
> 通过将结肠和内窥镜表示为带体积信息的样条（体积样条），把碰撞检测问题转化为样条间球-三角形相交测试，结合AABB树宽相位加速，使碰撞检测与三角面片数量解耦；同时用Cosserat棒约束模拟结肠的全局弯曲和扭转，辅以四面体约束模拟周围组织牵拉，在XPBD框架下实现稳定高效的变形仿真。

| 字段 | 内容 |
|------|------|
| 中文题名 | 用于内窥镜手术仿真的高效位置变形结肠建模 |
| 英文题名 | Efficient Position-based Deformable Colon Modeling for Endoscopic Procedures Simulation |
| 会议/期刊 | SIGGRAPH 2024 |
| Links | [paper](https://www.inf.ufrgs.br/vislab/sig24/) |
| Topic | #topic/graphics_physical_simulation |
| Method | Efficient Position-based Deformable Colon Modeling (XPBD with Cosserat rod + FSCD) |
| Dataset | Spring Scene, Colonoscopy Insertion Simulation |

> [!tip] 效果简介
> - Spring Scene (Collision Detection Stress Test) 上，Collision Detection Time FSCD: 2.02 ms (32k triangles, 60s) vs SOLID: 5.65 ms (32k triangles, 60s) (2.8× 加速)。
> - Colonoscopy Insertion Simulation 上，Framerate (FPS) 平均171 FPS，高应力区130 FPS，最低>100 FPS vs 实时阈值 (30 FPS) 或以往方法未提供定量比较 (显著超过实时要求)。

## 概要

传统内窥镜手术仿真器面临的核心瓶颈在于：内窥镜与柔软结肠之间持续接触所引发的大变形与复杂碰撞检测，使得实时交互难以实现，其中碰撞检测是主要性能障碍。

本文提出一种基于位置动力学的变形结肠建模方法。其核心思路是将结肠和内窥镜统一表示为**体积样条**（带辐射控制点的Catmull-Rom样条），在**XPBD框架**下，采用**Cosserat棒约束**模拟结肠的全局弯曲与扭转，辅以**四面体约束**模拟肠系膜及周围组织的牵拉保持形态；同时设计**快速样条碰撞检测算法（FSCD）**，将碰撞检测转化为样条间的球-三角形相交测试，结合AABB树宽相位加速，使碰撞检测性能与三角面片数量解耦。

实验表明，FSCD在32k三角面片、60秒场景下碰撞检测仅需2.02 ms，较传统SOLID方法加速2.8倍，且仿真结果视觉等价。全插入仿真在超过1200个接触点下平均帧率达171 FPS，高应力区间仍保持130 FPS，全程高于100 FPS，满足实时交互要求。方法定位上，本文属于**手术仿真中的物理模拟与碰撞检测交叉领域**，以管状结构专用碰撞检测算法替换通用方案，在保持视觉逼真度的前提下显著提升计算效率。

## 核心方法与创新机理

### 问题瓶颈与解决思路

传统内窥镜仿真器的核心性能瓶颈在于**碰撞检测**：当内窥镜在柔软结肠内持续移动时，两者之间产生大量复杂接触，传统基于三角面片的碰撞检测（如SOLID）计算量随面片数线性增长，难以在实时交互中维持稳定帧率。同时，结肠的大变形仿真需要同时处理全局弯曲扭转和局部组织牵拉，传统有限元法（FEM）或质点弹簧模型（MSM）难以在计算效率和物理真实性间取得平衡。

本文的核心洞察是：**将结肠和内窥镜统一表示为带体积信息的样条（体积样条/volspline），将碰撞检测问题转化为样条间球-三角形相交测试，使碰撞检测复杂度与三角面片数解耦**；同时，在扩展位置动力学（XPBD）框架下，用Cosserat棒约束模拟结肠的全局弯曲和扭转，辅以四面体约束模拟肠系膜及周围组织的牵拉，实现稳定高效的变形仿真。

### 方法框架与模块顺序

整个仿真流水线分为四个关键模块，按执行顺序为：

1. **CT图像重建与中心线提取**：从真实患者CT数据重建结肠三角网格，并提取结肠中心线。
2. **体积样条骨架构建**：基于Catmull-Rom样条和辐射控制点（RCP），将中心线扩展为带半径信息的体积样条表示。
3. **XPBD仿真循环**：在每帧中依次求解Cosserat棒约束（全局弯曲扭转）和四面体约束（局部组织牵拉），更新结肠位姿。
4. **FSCD碰撞检测与接触约束求解**：检测内窥镜与结肠体积样条间的碰撞，生成接触约束并反馈到XPBD求解器中。

模块间的因果关系为：模块2生成的体积样条是模块3和4的共享几何表示；模块3产生的变形位移驱动模块4的碰撞检测需求；模块4检测到的碰撞又通过接触约束反作用于模块3的XPBD求解，形成完整的物理交互闭环。

### 关键改动槽位（Changed Slots）

相比传统方法，本文在三个核心槽位上进行了替换：

| 槽位 | 基线方法 | 本文方法 | 因果机制 |
|------|----------|----------|----------|
| **几何表示** | 三角网格表面模型 | 体积样条（Catmull-Rom样条 + RCP） | 将管状结构抽象为沿中心线的控制点序列，每个控制点携带半径信息，使碰撞检测可基于样条而非三角面片进行 |
| **碰撞检测算法** | SOLID（AABB BVH，基于三角面片） | FSCD（AABB宽相位 + 球-三角形相交窄相位） | 窄相位仅在体积样条的辐射球与三角面片间进行，检测复杂度取决于控制点数量而非面片数，从根本上解耦性能与几何分辨率 |
| **变形模型** | 传统FEM或MSM | XPBD框架下Cosserat棒约束 + 四面体约束（Fast Corotational + Volume） | Cosserat棒约束提供零拉伸、弯曲和扭转弹性，四面体约束模拟肠系膜牵拉，XPBD框架保证大时间步长下的稳定性 |

### 体积样条表示（核心创新1）

体积样条是本文几何表示的核心。对于结肠，从CT重建的三角网格中提取中心线后，沿中心线采样得到$n$个控制点$\{P_i\}_{i=1}^n$，每个控制点$P_i$携带一个辐射控制点（RCP）半径$r_i$。对于内窥镜，其中心线由运动学模型驱动，同样表示为体积样条。

体积样条的关键性质是：任意两个相邻控制点$P_i$和$P_{i+1}$之间形成一个**样条段**（spline segment），该段在碰撞检测中被视为一个**刚体**——其表面由控制点半径定义的辐射球包络和三角面片构成。这种统一的表示使得碰撞检测可以在样条级别而非三角面片级别进行。

### FSCD碰撞检测算法（核心创新2）

FSCD（Fast Spline Collision Detection）是本文突破性能瓶颈的关键算法，分为宽相位和窄相位两个阶段：

**宽相位**：为内窥镜和结肠的体积样条各构建一棵AABB树，快速过滤掉不可能发生碰撞的样条段对。AABB树的构建基于样条段的包围盒，而非三角面片。

**窄相位**：对通过宽相位筛选的每对样条段（一个来自内窥镜，一个来自结肠），执行球-三角形相交测试。具体而言，将内窥镜样条段上的每个辐射球（球心$U_k$，半径$r$）与结肠样条段的每个三角面片进行测试。对于三角面片的每条边$\vec{w} = V_{i,j} \to V_{i,j+1}$，计算球心到边的最近点$CP$：

$$
\mathbf{CP} = \begin{cases}
\mathbf{V}_{i,j}, & \text{if } \vec{\mathbf{w}} \cdot \vec{\mathbf{z}} \leq 0 \\
\mathbf{V}_{i,j+1}, & \text{if } \vec{\mathbf{w}} \cdot \vec{\mathbf{w}} < \vec{\mathbf{w}} \cdot \vec{\mathbf{z}} \\
\mathbf{V}_{i,j} + q \cdot \vec{\mathbf{w}}, & \text{otherwise}
\end{cases}
$$

其中$\vec{z} = U_k - V_{i,j}$，插值参数$q$为：

$$
q = \frac{\vec{\mathbf{w}} \cdot \vec{\mathbf{z}}}{\vec{\mathbf{w}} \cdot \vec{\mathbf{w}}}, \quad q \in (0,1)
$$

碰撞判定条件为：

$$
\|\mathbf{CP} - \mathbf{U}_k\| \leq r
$$

若满足该不等式，则记录碰撞点、碰撞法向和穿透深度，用于后续接触约束的构建。

**FSCD的性能优势**在于：窄相位的计算量取决于内窥镜体积样条的控制点数量（即辐射球数量）和结肠三角面片数量，但结肠的控制点数量远小于三角面片数量。更重要的是，FSCD允许在保持控制点数量不变的情况下增加三角面片分辨率以提升渲染质量，而碰撞检测性能几乎不受影响——这是传统SOLID方法无法实现的。

### XPBD变形模型（核心创新3）

结肠变形仿真在XPBD框架下进行，包含两类约束：

**Cosserat棒约束**（Eq. 4）：将结肠建模为一系列刚体段，每段对应一个样条段。相邻两段之间的Cosserat棒约束是一个六维约束，耦合两个刚体的位置$\mathbf{X}_1, \mathbf{X}_2$和定向$q_1, q_2$：

$$
C(\mathbf{X}_1, q_1, \mathbf{X}_2, q_2) = \begin{pmatrix}
\mathbf{R}(q_1)\mathbf{p}_1 + \mathbf{X}_1 - \mathbf{R}(q_2)\mathbf{p}_2 - \mathbf{X}_2 \\
\cdots
\end{pmatrix}
$$

该约束实现了三个平移自由度和三个旋转自由度的弹性耦合，使结肠在弯曲和扭转时保持零拉伸，同时允许自然的生理弯曲。

**四面体约束**：在结肠样条段与周围固定点之间构建四面体网格，施加Fast Corotational约束和Volume约束，模拟肠系膜和周围软组织对结肠的牵拉作用。这些约束确保结肠在变形后仍能保持整体解剖位置，防止其无限制漂移。

**接触约束**（Eq. 5）：当FSCD检测到碰撞后，在XPBD框架中添加不等式接触约束。对于两个发生碰撞的刚体段（内窥镜段和结肠段），接触约束为：

$$
C_c(\mathbf{X}) = \hat{\mathbf{n}}^T \left( (\mathbf{X}_1 + \mathbf{R}(\vartheta_1)\mathbf{c}_1) - (\mathbf{X}_2 + \mathbf{R}(\vartheta_2)\mathbf{c}_2) \right) \geq 0
$$

其中$\hat{\mathbf{n}}$为碰撞法向，$\mathbf{c}_1, \mathbf{c}_2$为接触点在各自刚体局部坐标系中的位置。对应的Jacobian矩阵（Eq. 6）为：

$$
\mathbf{J}_c(\mathbf{X}) = \hat{\mathbf{n}}^T \begin{bmatrix} \mathbf{I} & -(\mathbf{c}_{1_{world}})^\star & -\mathbf{I} & (\mathbf{c}_{2_{world}})^\star \end{bmatrix}
$$

该Jacobian用于XPBD的迭代求解器中，在满足接触约束的同时更新刚体位姿。

### 训练/推理路径

本文方法不需要训练阶段，属于**基于物理的实时仿真**。推理路径如下：

1. **预处理**：从患者CT数据重建结肠网格，提取中心线，构建体积样条（一次性离线完成）。
2. **每帧循环**：
   - 读取内窥镜操控输入，更新内窥镜体积样条位姿。
   - 对结肠体积样条施加Cosserat棒约束和四面体约束，进行XPBD迭代求解。
   - 执行FSCD碰撞检测（宽相位AABB树遍历 + 窄相位球-三角形测试）。
   - 对检测到的每个碰撞生成接触约束，加入XPBD求解器。
   - 更新所有样条段位姿，输出变形后的结肠网格用于渲染。

整个循环在单帧内完成，实测帧率始终高于110 FPS，平均171 FPS，满足实时交互需求。

![[assets/figures/papers/paper_list_l18_https_www_inf_ufrgs_br_vislab_sig24/figures/003_Figure_2.jpg]]
*Figure 2: The simulation pipeline is divided into three main parts: a) acquisition and reconstruction of the colon mesh from a real patient CT, including the colon centerline estimation; b) building a volumetric spline skeleton from the reconstructed mesh and centerline; c) simulate the colon deformation using an XPBD formulation and a tailored collision detection method*

![[assets/figures/papers/paper_list_l18_https_www_inf_ufrgs_br_vislab_sig24/figures/004_Figure_3.jpg]]
*Figure 3: The volumetric spline representation for the endoscope (top) and colon (bottom), in front view (left), and cross-sections (right)*

![[assets/figures/papers/paper_list_l18_https_www_inf_ufrgs_br_vislab_sig24/figures/007_Figure_6.jpg]]
*Figure 6: Geometric representation of the Cosserat rod segments (colon) held in place by tetrahedral constraints (mesentery and surrounding soft tissues)*

## 实验与关键发现

### 碰撞检测性能对比：FSCD vs SOLID

碰撞检测是该系统的主要性能瓶颈。作者将提出的快速样条碰撞检测（FSCD）与传统基于AABB树的SOLID算法（Bergen, 1997）进行了隔离对比。实验场景为一个弹簧模型在外管内运动（Figure 9），分别在1秒和60秒两个时间点测量碰撞检测耗时。

![[assets/figures/papers/paper_list_l18_https_www_inf_ufrgs_br_vislab_sig24/figures/011_Table_1.jpg]]
*Table 1: Comparison of the isolated collision detection performance for the simulation in Figure 9. The first column shows the triangle resolution in each model (inner and outer models)*

![[assets/figures/papers/paper_list_l18_https_www_inf_ufrgs_br_vislab_sig24/figures/010_Figure_9.jpg]]
*Figure 9: A visual comparison was conducted between simulations utilizing our colon deformation scheme with the FSCD and the SOLID collision detection methods. Captures at 1s, 10s, and 60s durations reveal that both results are equivalent*

**Table 1** 给出了核心数据。在低分辨率（6k三角面片）下，FSCD与SOLID差距不大：1秒时FSCD为0.37 ms，SOLID为0.47 ms。但随着三角面片数增至32k，差距显著拉大：60秒时FSCD仅需2.02 ms，而SOLID需5.65 ms，FSCD实现了约**2.8倍加速**。

这里有一个关键的公平性设计：SOLID的性能直接取决于三角面片数量，因此作者在比较时有意增加了SOLID场景的控制点（SCP）数量以匹配高三角面片分辨率，使SOLID处于相对优势的配置。而FSCD的性能与三角面片数解耦——其碰撞检测基于体积样条的控制点间球-三角形相交测试，控制点数量可保持不变。即便如此，FSCD仍显著优于SOLID。视觉对比（Figure 9）显示两种方法在1秒、10秒、60秒的仿真结果完全等价，证明FSCD在保持视觉保真度的同时大幅降低了碰撞检测开销。

### 全插入仿真实时性能

完整的结肠镜插入仿真（从直肠到盲肠）是检验系统实时性的核心场景。Figure 7展示了物理计算（蓝色）与碰撞检测（绿色）的每秒钟平均耗时，红色曲线为每秒检测到的碰撞点数量。在整个插入过程中，碰撞点数量从初始的数百个逐步攀升至超过1200个，而碰撞检测耗时始终维持在低位。

Figure 8给出了帧率随时间的变化曲线。全程平均帧率为**171 FPS**，远超30 FPS的实时交互阈值。在通过脾曲（splenic flexure，约第220秒）这一高应力关键区域时，帧率有所下降，但该区间的平均帧率仍保持在**130 FPS**，最低帧率始终高于**100 FPS**。作者指出，通过脾曲后帧率趋于稳定，在100-105 FPS之间波动。这表明即使在接触点密集、变形剧烈的手术关键阶段，系统仍能维持流畅的实时交互。

### 变形仿真质量与医学验证

Figure 10展示了从直肠到盲肠的完整插入过程：(a) 内窥镜在直肠内未引起明显变形；(b) 镜端向右弯曲并压迫乙状结肠上部，导致结肠相应变形；(c) 乙状结肠收紧，增加了镜体通过的难度；(d) 镜体向横结肠移动并出现缠绕；(e) 内窥镜到达盲肠。整个过程中，结肠保持了其在腹腔中的整体位置和生理弯曲形态。

与X光影像的对比（Figure 11）进一步验证了仿真结果的形态学准确性。仿真产生的结肠变形形状与Lim et al. (2013)的临床X光图像高度相似，表明Cosserat棒约束配合四面体约束的XPBD方案能够有效复现真实解剖结构的力学响应。

![[assets/figures/papers/paper_list_l18_https_www_inf_ufrgs_br_vislab_sig24/figures/016_Figure_11.jpg]]
*Figure 11: Comparison with an X-ray image demonstrates the similarity of the resulting shape. The X-ray image by Lim et al. [2013] is available under the terms of the Creative Commons Attribution Non-Commercial License*

Figure 12展示了结肠镜手术中常见的两种肠袢形态——alpha-loop与倒alpha-loop。乙状结肠袢的形成是结肠镜检查中的关键难点，Shah et al. (2002)指出77%的患者疼痛主诉与此相关。系统成功复现了这两种袢形态，证明了变形模型在极端弯曲场景下的鲁棒性。

### 压力分布与临床相关性

Figure 13以热力图形式展示了结肠与内窥镜之间的压力分布，暖色区域表示压缩力更高的位置。作者将高压力区域与Kavic and Basson (2001)的医学文献进行了对照——文献中标出的a至d四个高穿孔风险区域与仿真中的高压力区域高度吻合。这一结果为该仿真系统在手术训练中的潜在应用提供了临床相关性证据。

### 失败模式与适用边界

作者明确指出了若干局限。首先，为维持结肠整体形态的稳定性，对有机组织的力学机理进行了简化处理，这可能会影响变形的生物力学真实感。其次，系统尚未与实际变形数据进行定量比较来验证医学训练效果。此外，教育影响评估和远程培训场景的适用性尚未开展研究。

从技术角度看，FSCD的性能优势依赖于体积样条表示——碰撞检测与三角面片数解耦的前提是控制点数量保持合理规模。当控制点密度增加时，FSCD的性能变化规律尚未被系统研究（作者将此列为开放问题）。同样，该方法向其他管状结构手术（如支气管镜、血管镜）的推广效果也有待验证。

## 定位与知识库关联

本文在**内窥镜手术仿真**这一应用语境下，对两个关键计算槽位进行了替换：**碰撞检测算法**和**变形模型**，并引入了配套的**几何表示**槽位。其核心定位是：在保持视觉等价的前提下，将碰撞检测这一主要性能瓶颈与三角面片数量解耦，从而在消费者级硬件上实现患者特异性结肠的实时变形仿真。

### 相对于已有工作的槽位变化

**1. 碰撞检测槽位：从通用三角网格碰撞检测到管状结构专用碰撞检测**

基线方法采用 **SOLID**（Bergen, 1997），一种基于AABB包围盒层次结构（BVH）的通用碰撞检测库。SOLID的性能直接取决于三角面片数量——面片越多，BVH遍历和三角面片间相交测试越昂贵。本文提出的 **FSCD（Fast Spline Collision Detection）** 改变了这一槽位：将碰撞检测从“三角面片-三角面片”转换为“样条球-三角形”的相交测试。由于结肠和内窥镜均被表示为体积样条（volspline），FSCD只需检测内样条的控制点球体与外样条的三角面片是否相交（Eq. 1-3），配合AABB树宽相位过滤，使碰撞检测的计算代价与三角面片数量基本解耦。Table 1的定量证据表明，在32k三角面片、60秒仿真场景下，FSCD的碰撞检测时间为2.02 ms，而SOLID为5.65 ms，加速约2.8倍；且Figure 9的视觉对比确认两种方法产生等价结果。

**2. 变形模型槽位：从传统FEM/MSM到XPBD框架下的Cosserat棒约束+四面体约束组合**

传统结肠仿真多采用有限元法（FEM）或质点弹簧模型（MSM），前者计算昂贵，后者难以精确控制弯曲和扭转刚度。本文在XPBD框架内引入**Cosserat棒约束**（Eq. 4）来模拟结肠的全局弯曲和扭转弹性——该六维约束耦合相邻刚体段的位置与定向，实现零拉伸、弯曲和扭转的物理响应；同时辅以**四面体约束**（Fast Corotational + Volume约束）模拟肠系膜及周围软组织对结肠的牵拉和形状保持（Figure 6）。这种组合使得结肠在受力时既能产生大变形，又不会丧失整体解剖位置。

**3. 几何表示槽位：从纯三角网格表面模型到体积样条**

传统方法直接使用三角网格表面模型，碰撞检测和变形计算均依赖面片。本文引入**体积样条（Volumetric Spline）** 作为统一的几何表示：基于Catmull-Rom样条和辐射控制点（RCP），将管状结构的中心线骨架与截面半径信息编码为一体（Figure 3）。这一槽位变更是FSCD得以实现的前提——体积样条同时提供了碰撞检测所需的球体（内样条）和三角面片（外样条），以及变形计算所需的刚体段划分。

### 知识库挂载点

本文可挂载至以下知识库节点：

- **位置动力学（PBD/XPBD）**：作为变形求解框架，本文继承XPBD的约束求解范式（Müller et al., 2007；Macklin et al., 2016），在此基础上定制了面向管状结构的Cosserat棒约束和接触不等式约束（Eq. 5-6）。
- **Cosserat棒理论**：将结肠离散为一系列刚体段，通过Cosserat约束耦合相邻段的位置与四元数定向，实现弯曲和扭转弹性的模拟。该理论与手术缝合线仿真（Kugelstadt & Schömer, 2016）等一维柔性体仿真共享数学基础。
- **碰撞检测**：FSCD的宽相位沿用AABB树（van den Bergen, 1997），窄相位则将问题规约为球-三角形相交测试，与粒子-网格碰撞检测有方法论上的联系。
- **医学图像处理**：流水线前端依赖CT图像重建和中心线提取，连接医学影像分析知识库。

### 适用边界与局限性

本文方法明确针对**管状结构之间的持续接触变形**场景设计，其优势边界在于：

- **适用场景**：内窥镜与结肠的大规模、持续接触仿真，接触点可超过1200个（Figure 7）。
- **性能边界**：在消费者级硬件上，全插入仿真平均帧率171 FPS，高应力区间（如通过脾曲时）平均130 FPS，最低不低于100 FPS（Figure 8），满足实时交互需求。
- **视觉保真度**：仿真结果与X光影像在整体形态上吻合（Figure 11），压力分布热力图（Figure 13）与医学文献记载的穿孔高风险区域一致。

**已知局限**（论文自述，需人工验证严重程度）：
1. 为保持结肠形状，对有机组织机理进行了简化（如肠系膜的力学特性），可能影响生物力学真实感。
2. 未进行与实际变形的综合定量比较来验证医学训练效果。
3. 未评估该方法在教育培训中的实际效果及远程培训场景的适用性。

### 后续研究启发

1. **算法扩展**：FSCD的性能随控制点数量（而非三角面片数）变化的规律尚未系统研究。若能将控制点数量也保持恒定，FSCD在不同网格分辨率下的性能应近乎恒定——这一假设需实验验证。此外，该方法可推广至其他管状手术仿真，如支气管镜、血管镜、输尿管镜等，但需验证体积样条表示对分叉结构的适应性。

2. **训练效果验证**：需设计用户研究，定量评估基于该仿真器的训练是否提升真实结肠镜操作技能（如减少患者疼痛、缩短操作时间、降低穿孔风险）。Figure 12展示的alpha-loop和倒alpha-loop是临床中导致77%患者疼痛主诉的关键情形，仿真器对这些情形的复现能力可作为验证指标。

3. **生物力学精度提升**：当前四面体约束对肠系膜的模拟较为简化，可考虑引入更精确的软组织本构模型或数据驱动的组织参数标定方法，在保持实时性的前提下提升生物力学保真度。

## 原文 PDF

![[paperPDFs/SIGGRAPH_2024/Efficient_Position_based_Deformable_Colon_Modeling_for_Endoscopic_Procedures_Simulation.pdf]]