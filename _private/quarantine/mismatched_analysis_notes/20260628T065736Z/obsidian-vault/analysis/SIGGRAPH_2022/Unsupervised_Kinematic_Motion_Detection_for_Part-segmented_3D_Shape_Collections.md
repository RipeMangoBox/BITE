---
title: Unsupervised Kinematic Motion Detection for Part-segmented 3D Shape Collections
type: paper
paper_level: A
venue: SIGGRAPH
year: 2022
pdf_ref: paperPDFs/SIGGRAPH_2022/Unsupervised_Kinematic_Motion_Detection_for_Part_segmented_3D_Shape_Collections.pdf
project_link: null
code_link: null
aliases:
- UKMDPS3SC
tags:
- SIGGRAPH_2022
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
core_operator: 通过调整MXG表示中各减法挤出操作的二维轮廓（即铣削路径），并在考虑铣刀半径约束的前提下，共同优化这些轮廓的位置和形状，可以恢复紧密接触。优化的自由度集中在可微的2D轮廓参数（g_i）上。
primary_logic: 利用MXG的平面挤出结构，将三维耦合优化问题转化为代表性二维切片上的轮廓曲线优化。定义表面间隙（Surface Gap）和铣削路径距离（Milling Path Distance）两个可微损失函数，两者均可简化为1D轮廓积分，实现高效、稳定的梯度联合优化。
claims:
- 我们的优化方法在所有30个设计上均满足可铣性（M=100%），且紧密耦合成功率高达90.625%（Cτ），是唯一同时满足两项标准的方法；相比之下，Opening-Only无法达到耦合要求（Cτ=6.25%），Opening & Diff-Flip 则严重破坏可铣性（M=25%）。
- 消融实验证实，移除Milling Path Distance损失或Surface Gap损失均导致表面间隙显著增大；移除Occupancy Preservation损失则使设计偏差增加；移除渐进半径调度或ODF初始化同样导致性能大幅下降。
- 在3轴CNC机床上物理制造了8个紧密耦合接头，验证了优化后的几何形状可实际装配，功能正常。
- 30个传统整体接头设计数据集 上 可铣性 (M, Millability) = 100%
---

# Unsupervised Kinematic Motion Detection for Part-segmented 3D Shape Collections

> [!tip] 核心洞察
> 利用MXG的平面挤出结构，将三维耦合优化问题转化为代表性二维切片上的轮廓曲线优化。定义表面间隙（Surface Gap）和铣削路径距离（Milling Path Distance）两个可微损失函数，两者均可简化为1D轮廓积分，实现高效、稳定的梯度联合优化。

| 字段 | 内容 |
|------|------|
| 中文题名 | MiGumi：实现紧密耦合整体接头的数控铣削 |
| 英文题名 | Unsupervised Kinematic Motion Detection for Part-segmented 3D Shape Collections |
| 会议/期刊 | SIGGRAPH 2022 |
| Links | [paper](https://dritchie.github.io/) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction |
| Method | MiGumi |
| Dataset | 30个传统整体接头设计数据集 |

> [!tip] 效果简介
> - 30个传统整体接头设计数据集 上，可铣性 (M, Millability) 100% vs MO: 100%, ODF: 25% (维持完美可铣性；ODF仅25%)；紧密耦合成功率 (Cτ, τ=6.25%) 90.625% vs MO: 6.25%, ODF: 96.87% (大幅优于MO，接近ODF但ODF零件不可铣，因此该方法唯一真正可用)。

## 概要

传统整体接头（如榫卯）包含尖锐内角，但CNC平底铣刀具有有限半径，直接铣削会产生圆角伪影，破坏零件间的紧密耦合，导致装配失败。本文提出MiGumi，将接头零件建模为可铣挤出几何（MXG）——一系列由2D CSG轮廓、挤出方向和刀具半径参数化的减法挤出操作，从根本上保证可铣性并显式控制伪影。核心创新在于将三维耦合恢复问题转化为代表性二维切片上的1D轮廓联合优化：定义表面间隙（Surface Gap）和铣削路径距离（Milling Path Distance）两个可微损失，通过渐进半径调度与ODF初始化稳定求解。在30个传统接头数据集上，方法实现100%可铣性，紧密耦合成功率达90.625%，是唯一同时满足两项标准的方法；物理制造8个接头验证了实际装配可行性。该方法定位为面向CNC制造的几何优化框架，填补了从理想设计到可制造紧密耦合接头的自动化转换空白。

## 核心方法与创新机理

### 问题本质：铣削伪影与耦合失效的因果链

传统整体接头（integral joint）的设计隐含尖锐内角——例如燕尾榫的楔形接触面。当使用有限半径的平底铣刀进行CNC加工时，刀具无法进入这些尖锐内角，实际切削轨迹会沿着刀具半径产生圆弧过渡，形成“圆角伪影”（filleting artifact）。这一伪影的后果并非简单的几何偏差，而是**接触面分离或重叠**：原本紧密配合的榫头与榫眼之间出现间隙，或零件因材料残留而无法装配。因此，核心瓶颈并非“铣削不可行”，而是**铣削可行性与紧密耦合之间的根本冲突**——单独对每个零件做可铣性后处理（如形态学开运算）会破坏多零件间的接触关系，导致装配失败。

### 核心洞察：从三维耦合到二维轮廓积分的降维

MiGumi的核心洞察在于利用MXG（Millable Extrusion Geometry）表示的平面挤出结构，将三维空间中的多零件耦合优化问题转化为**代表性二维切片上的轮廓曲线优化**。由于MXG将每个减法操作建模为沿特定方向的平面挤出，任意垂直于挤出方向的切片上，零件的几何行为完全由该平面内的2D CSG轮廓决定。更重要的是，多个切片具有相同的轮廓配置，可以聚类为少量“等效切片组”，每个组只需计算一次2D轮廓积分即可代表整个挤出方向上的耦合行为。这一降维使得原本需要在三维网格上进行的表面距离积分，简化为**1D轮廓上的可微积分**，从而支持高效的梯度联合优化。

### 几何表示：Millable Extrusion Geometry (MXG)

**Changed Slot 1：从通用网格/隐式曲面到参数化可铣挤出几何**

传统方法直接对未考虑刀具半径的网格或隐式曲面进行后处理，无法显式控制铣削伪影。MXG将每个零件建模为材料块 $M$ 减去一系列减法挤出体积 $V_i$ 的并集：

$$P = M - \bigcup_{i} V_{i}$$

每个减法体积 $V_i$ 由三个参数定义：
- **2D CSG轮廓** $g_i$：一个隐式有符号距离函数（SDF），通过CSG树（布尔并、交、差）构建，定义刀具在平面内的运动轨迹
- **挤出方向** $\mathbf{n}_i$：刀具进给方向
- **刀具半径** $r_i$：平底铣刀的半径

为了模拟给定刀具半径下的可铣几何，对每个轮廓 $g_i$ 应用**形态学开运算**（先腐蚀后膨胀）：

$$C_{i}^{r} = \{ x \mid (g_{i} \oplus B_{r_{i}})(x) \leq 0 \}$$

其中 $B_{r_i}$ 是半径为 $r_i$ 的圆盘结构元素。开运算的效果是：腐蚀操作将轮廓向内收缩 $r_i$，模拟刀具中心可达区域；膨胀操作将收缩后的轮廓向外扩张 $r_i$，恢复为实际切削边界。这一过程的几何意义是：**所有曲率半径小于 $r_i$ 的凹角被自动圆角化**，而凸角保持不变——这正是平底铣刀物理加工的真实行为。

MXG的关键优势在于：刀具半径 $r_i$ 和挤出方向 $\mathbf{n}_i$ 是**显式可调参数**，而非后处理的隐式结果。用户可以在设计阶段就指定哪些减法操作使用何种刀具，从而精确控制伪影出现的位置和程度。

### 耦合优化框架：双损失联合驱动

**Changed Slot 2：从单零件后处理到多零件联合轮廓优化**

基线方法MO（Opening-Only）仅对每个零件独立进行形态学开运算，不恢复接触；ODF（Opening & Diff-Flip）在开运算后通过形状差翻转尝试补偿，但会引入不可铣的减法操作。MiGumi的核心创新在于**同时优化所有接触面上挤出轮廓的2D曲线参数**，最小化两个互补的损失函数。

#### 表面间隙损失（Surface Gap, $\mathcal{L}_S$）

表面间隙衡量耦合体积 $\Omega$ 内，每个零件表面到其他零件的最近距离积分：

$$\mathcal{L}_S = \sum_{a=1}^{n} \int_{\partial P^{a} \cap \Omega} \min_{b \neq a} \mathcal{D}(x, P^{b}) \, dA(x)$$

当 $\mathcal{L}_S = 0$ 时，零件间实现紧密耦合。在MXG表示下，每个零件的边界可分解为三类表面：**材料表面**（$\partial^M$，原始材料块的外表面）、**端盖表面**（$\partial^C$，挤出方向的两端）和**侧向表面**（$\partial^L$，沿挤出方向的柱面）。对于侧向表面，利用等效切片聚类，将3D面积分近似为代表性切片上的2D轮廓积分：

$$\int_{\partial_i^L} \mathcal{T} \approx \sum_{k=1}^{m} w_k \cdot \int_{\partial C_i(z_k)} \min_{P^b \neq P} \mathcal{D}(x, P^b) \, ds(x)$$

其中 $w_k$ 是切片 $z_k$ 代表的实际挤出长度权重。这一近似将计算复杂度从三维网格采样降低为少量2D轮廓上的离散积分。

#### 铣削路径距离损失（Milling Path Distance, $\mathcal{L}_P$）

表面间隙损失存在一个**梯度消失陷阱**：当两个零件的侧向表面已经接触但凹形区域尚未对齐时，表面间隙对这些凹形区域的轮廓参数梯度为零，优化会停滞在局部极小。这是因为表面间隙只测量“表面到表面”的距离，而无法感知“刀具路径到刀具路径”的相对位置。

铣削路径距离损失直接惩罚两个相对铣削路径之间的实际距离与理想距离（两刀具半径之和 $r_i + r_j$）的偏差：

$$\mathcal{L}_P = \sum_{(i,j)} \int_{x \in \partial g_i^a} \left( \mathcal{D}(x, g_j^b) - (r_i + r_j) \right)^2 ds(x)$$

其几何意义是：将一条铣削路径的轮廓 $g_i^a$ 插入到对面零件轮廓 $g_j^b$ 的平面SDF中，要求每个采样点的有符号距离值恰好等于 $r_i + r_j$。当实际距离偏离这一理想值时，损失产生梯度，**拉动凹形区域的轮廓顶点向正确位置移动**，从而消除表面间隙损失的梯度消失问题。

#### 占位保持损失（Occupancy Preservation, $\mathcal{L}_{occ}$）

为防止优化过度偏离原始设计意图，引入占位保持损失，约束优化后的零件体积与MXG₀理想程序（$r=0$）的体积偏差。

#### 总损失函数

$$\mathcal{L}_{total} = \mathcal{L}_S + \lambda_P \cdot \mathcal{L}_P + \lambda_{occ} \cdot \mathcal{L}_{occ}$$

其中 $\lambda_P$ 和 $\lambda_{occ}$ 为平衡权重。优化变量是所有减法挤出操作的2D CSG轮廓参数 $\{g_i\}$，梯度通过自动微分计算，更新后直接修改MXG程序中的轮廓定义。

### 优化调度与初始化策略

**Changed Slot 3：从直接优化到渐进半径展开与ODF初始化**

直接以目标刀具半径 $r_d$ 开始优化容易陷入局部极小，因为大半径下的形态学开运算会产生显著的几何变形，使得初始解远离可行域。MiGumi采用**渐进展开策略**（continuation）：从 $r=0$（无伪影的理想几何）开始，逐步增加刀具半径至 $r_d$，每一步以上一步的优化结果作为初始值。这种“从易到难”的调度使得优化路径平滑地跟踪从理想几何到可铣几何的变形过程。

初始化方面，直接使用MXG₀程序（$r=0$）作为起点效果不佳。MiGumi采用ODF方法在 $r_d/2$ 处的输出作为轮廓场的初始值。ODF虽然整体不可铣，但其在半半径下的几何已经接近目标形状，为优化提供了良好的初始猜测。消融实验证实，取消渐进调度或ODF初始化均导致性能显著下降。

### 端到端管线

1. **MXG设计模块**：用户定义零件的减法挤出操作，指定每个操作的2D CSG轮廓 $g_i$、挤出方向 $\mathbf{n}_i$ 和理想刀具半径 $r_i$，构成MXG₀理想程序
2. **铣削伪影模拟模块**：对每个CSG轮廓应用形态学开运算，将理想零半径轮廓变形为给定刀具半径下的可铣轮廓 $C_i^r$
3. **切片提取与聚类**：提取所有垂直于挤出方向的平面切片，识别等效切片组，计算代表性切片及其权重
4. **耦合优化模块**：在代表性切片上计算 $\mathcal{L}_S$ 和 $\mathcal{L}_P$，通过自动微分计算梯度，更新所有挤出轮廓参数 $\{g_i\}$；采用渐进半径展开策略和ODF初始化
5. **输出**：生成可铣且紧密耦合的MXG程序，可直接用于CNC加工路径生成

![[assets/figures/papers/paper_list_l13_https_dritchie_github_io/figures/009_Figure_9.jpg]]
*Figure 9: (a) Our optimization pipeline exploits a structural property of MXG representation to greatly reduce the problem complexity. Based on its definition as a composition of subtractive planar extrusions, we observe that tight coupling can be fully characterized in 1D slices that lie perpendicular to the extrusion directions. (b) Many of the slices exhibit identical behavior and can be further grouped into a few representative planar sets. (c) The optimization domain then reduces to 1D planar curves within these representative slice sets. The interface of*

## 实验与关键发现

### 实验设置

实验在30个传统整体接头设计数据集上进行。所有方法统一采用半径 $r_d = 3.175\,\text{mm}$（1/4英寸）的平底铣刀。评估围绕两个核心维度展开：**可铣性（Millability, M）**——所有减法挤出操作是否均可用目标半径刀具铣削；**紧密耦合成功率（Coupling Success Rate, $C_\tau$）**——以阈值 $\tau=6.25\%$ 衡量耦合区域内的体积违规比例是否可接受。基线方法包括 Opening-Only（MO，仅对各零件独立做形态学开运算）和 Opening & Diff-Flip（ODF，在开运算基础上通过形状差翻转尝试恢复接触）。

### 主结果：可铣性与耦合的联合达成

Table 1 报告了三种方法的核心对比。**MiGumi 是唯一同时满足可铣性与紧密耦合要求的方法。**

| 方法 | 可铣性 (M) | 紧密耦合成功率 ($C_\tau$) |
|------|-----------|--------------------------|
| Opening-Only (MO) | **100%** | 6.25% |
| Opening & Diff-Flip (ODF) | 25% | 96.87% |
| **MiGumi (Ours)** | **100%** | **90.625%** |

MO 虽完美保持可铣性，但 $C_\tau$ 仅 6.25%——独立开运算使接触面分离，零件间出现严重间隙或重叠（Fig. 14），无法实际装配。ODF 的 $C_\tau$ 高达 96.87%，看似接近完美耦合，但其可铣性仅 25%：75% 的零件包含不可铣的减法操作，意味着这些高耦合结果在实际 CNC 加工中**无法制造**。MiGumi 在维持 100% 可铣性的前提下，将耦合成功率从 MO 的 6.25% 提升至 90.625%，是**唯一真正可用的方案**。

值得注意的是，MiGumi 未能达到 100% 耦合成功率的 9.375% 失败案例，主要集中在多路径尖锐相交的拓扑困境中（见下文失效分析）。

### 关键消融实验

Table 2 通过逐项移除优化管线的组件，揭示了各损失的因果贡献。评估指标为**中位违规体积（V）**和**设计偏差（$\nabla D$）**。

**移除 Milling Path Distance 损失（$\mathcal{L}_P$）** 导致表面间隙显著增大。这验证了仅靠 Surface Gap 不足以维持紧密耦合：当凹形铣削路径的梯度消失时（Fig. 12b），优化会停滞于次优解。$\mathcal{L}_P$ 通过惩罚铣削路径间距与理想值 $(r_i+r_j)$ 的偏差，提供了互补的梯度信号。

**移除 Surface Gap 损失（$\mathcal{L}_S$）** 同样使违规体积上升，证实两个损失函数**互补而非冗余**——$\mathcal{L}_S$ 直接度量接触面距离，$\mathcal{L}_P$ 约束铣削路径对齐，二者联合才能有效驱动轮廓协同变形。

**移除 Occupancy Preservation 损失（$\mathcal{L}_{occ}$）** 使设计偏差 $\nabla D$ 明显增加。该损失约束优化后的几何不偏离原始设计体积过远，是保持设计意图的关键正则项。

**取消渐进半径调度或 ODF 初始化** 均导致整体性能显著下降。渐进展开策略（从 $r=0$ 逐步增至 $r_d$）使优化平滑地穿越非凸损失景观，避免陷入局部极小；以 ODF 在 $r_d/2$ 处的输出初始化轮廓场，则为优化提供了接近最终解的起点。二者共同构成了**稳定收敛的必要条件**。

### 物理制造验证

在 3 轴 CNC 机床上使用 1/4 英寸平底铣刀物理制造了 8 个紧密耦合接头（Fig. 15），覆盖多种传统接头类型。所有制造件均可成功装配，功能正常。部分接头需要多次重新定位以处理多方向铣削（如 Fig. 15g），或采用装配后钻孔策略以保证高精度（如 Fig. 15f）。物理结果验证了优化几何在真实制造约束下的可行性。

![[assets/figures/papers/paper_list_l13_https_dritchie_github_io/figures/020_Figure_15.jpg]]
*Figure 15: CNC-Milled Physical Outputs. Assembled and disassembled states of joints physically fabricated using a 3-axis CNC milling machine with a quarter-inch flat-end bit. The parts of joint (e) were positioned at a 45 degree angle during milling. The holes in joint (f ) were fabricated after assembling the two pain parts of the joint, ensuring high precision despite repositioning. The parts of joint (g) were repositioned twice to accommodate the multiple milling directions*

### 失效模式与适用边界

**多路径尖锐相交的间隙问题（Fig. 16a）**：当三个或更多凹形减法挤出在尖锐内角处汇聚时，各铣削路径的刀具半径圆角在交汇点无法同时满足紧密接触，产生不可避免的三角形间隙。这是**平底铣刀在固定半径下的拓扑限制**，非优化方法可解。

**装配可行性缺失（Fig. 16b）**：优化目标仅考虑接触面耦合，未嵌入装配顺序或方向阻挡分析。30 个接头中有 1 个在优化后虽表面间隙极小，但零件无法沿单一方向滑入装配。这揭示了耦合优化与装配规划之间的**语义鸿沟**。

**表示能力边界（Fig. 16c）**：MXG 仅支持平底铣刀的外部可及减法挤出。约 20% 的传统接头（如大阪城大手门接头）需要非平底或内部不可及的铣削操作，无法用 MXG 建模。此外，当前方法需用户手动编写 MXG0 程序，无法从网格模型自动推断减法挤出。

**设计权衡（Fig. 17）**：铣削方向的选择影响伪影的可见性与可及性。沿滑动轴对齐挤出可将圆角伪影隐藏于内部，但需轴向铣削；侧向铣削提高可及性，却将伪影暴露于外表面。MXG 的参数化结构使用户可显式控制这一权衡。

![[assets/figures/papers/paper_list_l13_https_dritchie_github_io/figures/023_Figure_17.jpg]]
*Figure 17: MXG enables controlled trade-offs between fabrication constraints and design aesthetics. Here, we show two variants of a joint which differ in milling direction. (a) Aligns all extrusions along the sliding axis, hiding artifacts internally but requiring axis-parallel milling. (b) Performs all milling laterally, improving accessibility but exposing artifacts externally*

## 定位与知识库关联

MiGumi 的核心贡献在于将“数控铣削可制造性”与“多零件紧密耦合”这两个长期分离的目标统一到一个可微优化框架中。其改变的**关键 slot** 是：从传统的“先设计后验证/后处理”范式，转变为**以铣削操作为原语的几何表示（MXG）与接触面联合优化**的闭环。

### 相对于基线的本质差异

已有的可铣性保证方法分为两极：一是**Opening-Only (MO)**，对每个零件独立做形态学开运算以保证可铣性，但完全忽略零件间接触关系，导致装配时出现严重的重叠或间隙（Cτ 仅 6.25%）；二是**Opening & Diff-Flip (ODF)**，在开运算基础上通过形状差的双向翻转尝试恢复接触，虽能获得高耦合成功率（Cτ=96.87%），但 75% 的零件包含不可铣的减法操作（M=25%），从根本上违背了制造约束。这两种基线本质上都是**单零件后处理**，缺乏对多零件接触面的全局建模。

MiGumi 改变了这一 slot：它将所有接触面上挤出轮廓的 2D 曲线参数（g_i）作为**联合优化变量**，同时施加表面间隙损失（L_S）和铣削路径距离损失（L_P）。L_S 直接度量零件表面间的最近距离积分，推动接触面贴合；L_P 则惩罚相对铣削路径之间的实际距离与理想距离（两刀具半径之和）的偏差，解决了 L_S 在凹形轮廓区域梯度消失的退化问题。这种双损失互补机制是 ODF 的启发式补偿无法实现的——ODF 没有梯度信息来平衡可铣性与耦合性之间的取舍。

### 知识库挂载点

MiGumi 可定位于以下知识脉络的交汇处：

1. **可微制造与几何优化**：继承了将制造约束嵌入可微渲染/几何管线的方法论传统（如可微 3D 打印模拟），但将优化域从单零件形状变形转移到多零件接触面的联合调整。其关键创新在于利用 MXG 的平面挤出结构，将 3D 表面间隙和铣削路径距离**简化为代表性 2D 切片上的 1D 轮廓积分**，大幅降低计算复杂度，使梯度优化在 30 个设计的规模上稳定可行。

2. **数学形态学与刀具路径规划**：形态学开运算在 CAM 中常用于刀具半径补偿，但通常作为单向后处理。MiGumi 将其反向嵌入生成式设计循环——开运算的腐蚀-膨胀过程在 MXG 中显式参数化（通过 r_i 和 n_i），使得铣削伪影成为可控变量而非被动结果。这一思路与“设计即制造”范式（如面向增材制造的拓扑优化）形成对偶：增材制造优化材料分布，MiGumi 优化材料去除的刀具路径。

3. **传统木工数字化**：该工作属于将传统整体接头（integral joints）转化为数字制造可表达形式的努力谱系。与基于参数化模板或离散搜索的方法不同，MiGumi 通过 MXG 的 CSG 树结构保留了设计的符号可编辑性，同时以梯度优化处理连续形变，为手工技艺的数字化保存与再创造提供了新路径。

### 适用边界与限制

- **表示能力边界**：MXG 仅支持平底铣刀的外部可及减法操作，无法表示需要非平底刀具（如球头刀、T 型刀）或内部不可及切削的接头。数据集中约 20% 的传统接头（如大阪城大手门接头）因此被排除。这一限制源于 MXG 对“减法体积 = 任意形状与刀具圆柱扫掠体的 Minkowski 和”的形式化假设。
- **装配可行性盲区**：优化目标仅考虑静态接触面的几何贴合，未嵌入装配顺序约束或方向阻挡分析。实验中 30 个接头中有 1 个优化后无法手动装配（Fig. 16b），说明几何耦合是装配的必要非充分条件。
- **多路径相交退化**：当三个或更多凹形铣削路径在尖锐内角处相交时，刀具半径的物理约束使完美紧密耦合在数学上不可行，会产生不可避免的间隙（Fig. 16a）。这是平底铣削的固有极限，而非优化算法的缺陷。
- **人工建模成本**：当前管线需要用户手动编写 MXG0 程序（定义每个减法挤出的 2D CSG 轮廓和方向），无法从通用网格模型自动推断。这限制了方法的规模化应用。

### 后续研究启发

MiGumi 打开的后续方向包括：①将装配顺序约束或方向阻挡分析作为可微正则项嵌入优化目标，消除不可装配解；②研究从 CAD 网格或点云自动推断 MXG 减法挤出程序的方法（可视为逆向 CSG 解析问题）；③扩展表示以支持多轴铣削或混合制造策略（如辅助平面切割），解决多路径尖锐相交处的间隙问题；④在 MXG 中建模传统木工的精细结构技巧（如故意错位、楔入木楔），从而覆盖更丰富的传统工艺接合方式。这些方向的核心挑战都在于如何在保持可微性和优化稳定性的前提下，扩展几何表示的覆盖范围与约束表达能力。

## 原文 PDF

![[paperPDFs/SIGGRAPH_2022/Unsupervised_Kinematic_Motion_Detection_for_Part_segmented_3D_Shape_Collections.pdf]]