---
title: Compressing Geodesic Information for Fast Point-to-Point Geodesic Distance Queries
type: paper
paper_level: A
venue: SIGGRAPH ASIA
year: 2022
pdf_ref: paperPDFs/SIGGRAPH_ASIA_2022/Compressing_Geodesic_Information_for_Fast_Point_to_Point_Geodesic_Distance_Queries.pdf
project_link: "https://www.inf.usi.ch/hormann/pub_topic.html"
code_link: "https://github.com/"
aliases:
- HMMPM
- CGIFPPGDQ
tags:
- SIGGRAPH_ASIA_2022
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
core_operator: 绕过中间域，直接匹配源域和目标域的调和测度，从而在数值上避免crowding，并获得边界对应关系。
primary_logic: 将离散调和坐标转化为连续分段线性Poisson核和分段二次调和测度，预计算这些仅依赖于域几何的量，使得在线匹配算法复杂度为O(m)，从而能够实时更新共形映射。
claims:
- 所提方法基于调和测度这一共形不变量，避免了中间域的使用。
- 该方法能够处理极端crowding情况，而基于圆盘的方法会失败。
- 调和坐标可以被精确转化为连续调和测度近似。
- 在线匹配算法仅为O(m)时间，实现实时交互。
---

# Compressing Geodesic Information for Fast Point-to-Point Geodesic Distance Queries

> [!tip] 核心洞察
> 将离散调和坐标转化为连续分段线性Poisson核和分段二次调和测度，预计算这些仅依赖于域几何的量，使得在线匹配算法复杂度为O(m)，从而能够实时更新共形映射。

| 字段 | 内容 |
|------|------|
| 中文题名 | 实时共形映射与参数化 |
| 英文题名 | Compressing Geodesic Information for Fast Point-to-Point Geodesic Distance Queries |
| 会议/期刊 | SIGGRAPH ASIA 2022 |
| Links | [paper](https://www.inf.usi.ch/hormann/pub_topic.html) · [Code](https://github.com/) · [arXiv](http://arxiv.org/abs/2210.09125) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction |
| Method | Harmonic Measure Matching (Proposed method) |
| Dataset | V-shape domain to blob domain, Cow head mesh to disk, Maple leaf to cinquefoil |

> [!tip] 效果简介
> - V-shape domain to blob domain (extreme crowding example) 上，可视质量 / 成功率 成功，与真实值视觉一致 vs Disk-intermediary: 失败 (唯一可处理的方法)。
> - Cow head mesh to disk (3D parameterization) 上，面积加权平均角度失真 略小于BFF vs BFF (Sawhney and Crane 2018) (slightly better)。
> - Maple leaf to cinquefoil (high-res) 上，在线更新总时间 匹配+更新 < 几毫秒 vs 其他方法非实时 (实时交互)。

## 概要

计算任意两个平面域之间存在三自由度的所有共形映射，是计算机图形学与几何处理中的经典难题。传统方法以单位圆盘为中介域，通过预计算两个域到圆盘的共形映射，再用 Möbius 变换匹配约束点。然而，当源域形状狭长或存在深凹区域时，圆盘映射会出现严重的 **crowding 现象**——内部约束点在双精度下被挤到圆盘边界上，导致 Möbius 变换无法应用，整个管线失效。

本文提出 **调和测度匹配（Harmonic Measure Matching）** 方法，直接绕过中间域。核心洞察是：调和测度是共形不变量——若已知源域和目标域对应内点的调和测度，则边界对应关系可通过匹配这两个测度直接求得，无需经过圆盘。方法将离散调和坐标转化为连续的分段线性 Poisson 核和分段二次调和测度近似，预计算这些仅依赖于域几何的量；在线阶段仅需 $O(m)$ 时间即可完成匹配与映射更新，实现实时交互。

实验表明，该方法在极端 crowding 案例（如 V 形域到 blob 域）上能够成功求解，而基于圆盘的中介法则完全失效。在 3D 参数化任务中，其角度失真略优于当前最优的 **BFF**（Sawhney & Crane, TOG 2018）。方法的主要代价是预处理需计算调和坐标及缩放矩阵，但这是一次性开销，换取的是实时探索共形映射空间的能力。

## 核心方法与创新机理

### 问题瓶颈：圆盘中介法的Crowding失效

给定两个平面域 $\Omega_1$ 和 $\Omega_2$，要计算满足三自由度约束（两对对应内点 $x_1\leftrightarrow x_2$、$y_1\leftrightarrow y_2$）的共形映射 $f:\Omega_1\to\Omega_2$，传统思路是借助单位圆盘 $\mathbb{D}$ 作为中间域：预先计算 $g_1:\Omega_1\to\mathbb{D}$ 和 $g_2:\Omega_2\to\mathbb{D}$，再通过Möbius变换 $\varphi_1,\varphi_2$ 对齐约束点，最终合成 $f=g_2^{-1}\circ\varphi_2^{-1}\circ\varphi_1\circ g_1$（Figure 2）。

![[assets/figures/papers/paper_list_l49_https_www_inf_usi_ch_hormann_pub_topic_html/figures/002_Figure_2.jpg]]
*Figure 2: Given the precomputed conformal maps*

这一策略的根本性缺陷在于**crowding现象**：当 $\Omega_1$ 具有细长区域（如V形域）时，$g_1$ 会将大量边界挤压到 $\mathbb{D}$ 的极小弧段上，导致内点约束 $x_1$ 在双精度下被映射到 $\mathbb{D}$ 的边界上（Figure 3）。此时 $g_1(x_1)$ 与边界无法区分，Möbius变换失去作用，整个流程崩溃。**这是本文要解决的核心瓶颈：中间域crowding使得任意三自由度共形映射无法可靠求解。**

![[assets/figures/papers/paper_list_l49_https_www_inf_usi_ch_hormann_pub_topic_html/figures/003_Figure_3.jpg]]
*Figure 3: The precomputed conformal map g from a V-shaped domain - to the unit disk D can exhibit crowding so severe that the image*

### 核心洞察：绕过中间域，直接匹配调和测度

调和测度 $\omega_x(t)$ 是共形不变量：若 $f:\Omega_1\to\Omega_2$ 共形且 $f(x_1)=x_2$，$f(y_1)=y_2$，则对任意边界段 $p_1([0,t_1])\subset\partial\Omega_1$ 及其像 $p_2([0,t_2])\subset\partial\Omega_2$，有

$$\omega_{x_1}(t_1)=\omega_{x_2}(t_2)$$

（Equation (5)，Figure 5）。这一性质意味着：**只要能在 $\Omega_1$ 和 $\Omega_2$ 上分别计算调和测度，就可以通过匹配它们直接建立边界对应关系，完全绕过单位圆盘**，从而在数值上规避crowding。

调和测度由Poisson核 $P_x$ 积分得到：

$$\omega_x(t)=\int_0^t P_x(s)\,\mathrm{d}s$$

其中Poisson核满足单位测度 $\int_{\partial\Omega}P_\Omega(x,y)\mathrm{d}y=1$ 和线性重现 $\int_{\partial\Omega}P_\Omega(x,y)\,y\,\mathrm{d}y=x$（Equation (2)-(4)）。

### 关键Changed Slot 1：从“圆盘中介”到“调和测度直接匹配”

| 维度 | 圆盘中介法 | 本文方法 |
|------|-----------|---------|
| 边界映射策略 | $g_2^{-1}\circ\varphi_2^{-1}\circ\varphi_1\circ g_1$，依赖 $\mathbb{D}$ | 直接匹配 $\tilde{\omega}_1$ 和 $\tilde{\omega}_2$，得到重参数化 $r=\omega_2^{-1}\circ\omega_1$ |
| Crowding敏感性 | 约束点映射到边界即失效 | 不经过中间域，数值上不受crowding影响 |
| 可处理域类型 | 仅限圆盘映射不crowding的域 | 任意单连通域（含极端细长V形域） |

### 关键Changed Slot 2：从“$O(m^2)$迭代”到“$O(m)$单次扫描”

传统边界对应方法（如迭代优化）通常需要 $O(m^2)$ 或多次迭代。本文通过预计算累积和，将在线匹配降为 $O(m)$ 的顺序扫描（Section 4.2, Algorithm C.4），这是实现实时交互的关键。

### 方法框架：预处理-在线两阶段架构

整体流程如Figure 4所示，分为预处理（一次性）和在线交互（每次约束更新）两个阶段。

#### 阶段一：预处理（与约束无关）

**模块1：边界采样与Delaunay三角剖分。** 对 $\partial\Omega_1$ 和 $\partial\Omega_2$ 分别均匀采样 $m$ 个边界点，生成带约束的Delaunay三角网格 $M_1$、$M_2$（Section 3, Section 4.1）。

**模块2：计算离散谐波坐标。** 对每个网格顶点 $v_i$，求解Laplace方程得到其相对于 $m$ 个边界顶点的谐波坐标 $\phi_{ik}$（$k=1,\ldots,m$），满足：

$$\sum_{k=1}^{m}\phi_{ik}=1,\qquad\sum_{k=1}^{m}\phi_{ik}v_k=v_i$$

（Equation (9)）。谐波坐标是Poisson核的离散模拟，继承了单位测度和线性重现性质（Appendix A）。

**模块3：缩放得到连续Poisson核近似。** 将离散谐波坐标 $\phi_{ik}$ 通过质量集中（mass lumping）转化为分段线性函数 $\tilde{P}_{v_i}$ 在边界边上的值 $\psi_{ik}$：

$$\psi_{ik}=\frac{2}{e_{k-1}+e_k}\phi_{ik}$$

（Equation (B.2)），其中 $e_k$ 为边界边长度。这一缩放确保 $\tilde{P}_{v_i}$ 保持正值且积分为1，是后续调和测度单调性的保证（Appendix B）。

#### 阶段二：在线交互（$O(m)$ 复杂度）

**模块4：点定位与约束点 $\psi$ 计算。** 用户交互指定 $x_1,x_2,y_1,y_2$ 后，通过重心坐标定位 $x_i$ 所在三角形，插值得到其 $\psi$ 值（Section 4.2, Algorithm C.3）。

**模块5：调和测度匹配（核心在线算法）。** 对 $\Omega_1$ 和 $\Omega_2$，分别以 $y_1$、$y_2$ 为起点，沿边界累积积分得到近似调和测度序列：

$$A_1:=0,\quad A_{k+1}=A_k+e_k\frac{\psi_k+\psi_{k+1}}{2},\quad k=1,\ldots,m$$

（Equation (12)）。$A_k$ 是 $\tilde{\omega}_1(t_k)$ 的近似，$B_l$ 同理对应 $\tilde{\omega}_2$。然后通过单次顺序扫描匹配这两个单调递增序列，得到重参数化参数 $r_k$（Algorithm C.4），进而计算边界顶点共形像：

$$w_k=\tilde{p}_2(\tilde{r}(t_k))=(1-\lambda)v_l'+\lambda v_{l+1}'$$

（Equation (13)）。**整个匹配过程仅需 $O(m)$ 时间**（Table 2证实每步更新在毫秒级）。

**模块6：内部映射扩展。** 利用预计算的谐波坐标 $\Phi_1$ 将边界映射扩展到 $\Omega_1$ 内部：

$$\tilde{f}(x)=\sum_{k=1}^{m}\phi_{x,k}w_k$$

（Equation (14)）。也可使用柯西-格林坐标 $\gamma_k(z)$ 进行复值扩展（Equation (15)），速度更快但可能不完全忠实于边界映射。

### 模块间因果关系链

```
边界采样+三角剖分 → 谐波坐标Φ → 质量集中得ψ
                                      ↓
用户指定约束(x₁,x₂,y₁,y₂) → 插值得ψ(x₁),ψ(x₂)
                                      ↓
                           累积和A_k,B_l → 顺序匹配得r_k
                                      ↓
                             边界像w_k → Φ扩展得内部映射f̃
```

因果链条的关键在于：**质量集中（模块3）保证了 $\tilde{P}_x$ 的正值性，使得 $\tilde{\omega}_x$ 严格单调，这是匹配算法（模块5）能够通过简单顺序扫描完成的充要条件。** 若使用原始 $\phi_{ik}$ 直接积分，可能因负值导致非单调而匹配失败。

### 收敛性保证

Figure 9展示了方法随源网格边界采样数 $m$ 增加的收敛行为：面积加权平均拟共形误差 $Q_{\text{avg}}$ 趋近于1（精确共形），且 $Q_{\text{avg}}=1+O(1/m)$。Figure 15进一步量化了边界映射误差随 $m$ 的收敛，并与Zipper算法对比，验证了近似方案的理论正确性。

![[assets/figures/papers/paper_list_l49_https_www_inf_usi_ch_hormann_pub_topic_html/figures/017_Figure_15.jpg]]
*Figure 15: Maximum and average distance between the exact images of the source boundary points and the images obtained by our method and Zipper for the example in Figure 12 with different m*

## 实验与关键发现

### 核心性能：实时交互与收敛性

本文方法的核心性能优势体现在在线更新阶段。Table 2 报告了用户改变约束点时更新共形映射的耗时：对于从枫叶域（maple leaf, $m_1 = 3200$, $N_1 = 693020$）到五叶域（cinquefoil, $m_2 = 1000$, $N_2 = 204968$）的高分辨率映射，匹配与更新总时间仅为数毫秒量级。这一结果直接验证了 Section 4.2 中声称的 $O(m)$ 在线匹配复杂度——算法仅需对源域边界采样点做一次顺序扫描即可完成调和测度匹配，无需迭代求解。

![[assets/figures/papers/paper_list_l49_https_www_inf_usi_ch_hormann_pub_topic_html/figures/009_Table_2.jpg]]
*Table 2: Processing times (in milliseconds) of our method for updating the conformally mapped target mesh whenever the user changes a source or target constraint*

收敛性实验（Figure 9）表明，当目标域网格分辨率固定、源域边界采样数 $m$ 逐步增大时，面积加权平均拟共形误差 $Q_{\text{avg}}$ 趋于 1，即逼近精确共形映射。论文指出 $Q_{\text{avg}} = 1 + O(1/m)$，这一收敛行为在枫叶到五叶域的映射中得到验证。该结论表明，方法的近似误差可控，且随离散化细化而单调改善。

![[assets/figures/papers/paper_list_l49_https_www_inf_usi_ch_hormann_pub_topic_html/figures/016_Figure_1.jpg]]
*Figure 1: Compare to the results obtained by our method in the rightmost column of Figure 9*

### 与基线方法的定性比较

**极端 crowding 场景**（Figure 12）是本方法相对于基于单位圆盘中介方法（disk-intermediary）的决定性优势案例。对于 V 形域到 blob 域的映射，disk-intermediary 方法因 crowding 现象导致内部约束点的像在双精度下落在单位圆边界上，无法应用 Möbius 变换，完全失效。本文方法直接匹配源域和目标域的调和测度，绕过了中间域，成功生成了视觉上与真实值一致的共形映射。Figure 15 进一步量化了该场景下的边界误差：随着 $m$ 增大，本文方法的最大边界距离误差和平均误差均收敛，且与 Zipper 算法（Marshall and Rohde, 2007）的精度可比。

**与 BFF 的比较**（Figure 16）在 cow head 网格到单位圆盘的 3D 参数化任务上进行。面积加权平均角度失真方面，本文方法的结果略优于 BFF（Sawhney and Crane, ACM Trans. Graph., 2018）。值得注意的是，该比较中所有方法的内部扩展均使用相同的谐波坐标以保证公平性，差异仅源于边界映射策略。

**高分辨率下的定性比较**（Figure 13）展示了枫叶到五叶域上本文方法与 Zipper、BFF 的映射结果。三者视觉质量接近，但 Zipper 和 BFF 不具备实时交互能力——它们需要在每次约束变化时重新求解，而本文方法仅需毫秒级更新。

### 消融实验：映射模式选择

Figure 8 系统比较了四种映射模式：前向/后向映射 × 谐波坐标/柯西-格林坐标。在低分辨率网格（$m$ 较小）下，四种模式给出显著不同的结果，其中后向谐波坐标映射在视觉上优于其他三种组合。当分辨率提高后，四种模式的差异消失，均收敛到相近的映射结果。这一消融表明：
1. 后向映射策略（从目标域反推源域坐标）在低分辨率下具有更好的鲁棒性；
2. 柯西-格林坐标虽然在内部扩展时计算更快，但可能不完全忠实地重现边界映射，在低分辨率下尤为明显；
3. 分辨率足够时，方法对坐标类型和映射方向不敏感，验证了近似框架的一致性。

### 预处理成本与适用边界

Table 1 报告了各域的预处理耗时，包括 Delaunay 三角剖分和 Poisson 核分段线性近似 $\tilde{\Phi}$ 的计算。预处理时间随网格规模增长，对于高分辨率网格可能较长（例如枫叶域 $N_1 = 693020$ 时需数十秒至数分钟量级）。但这是一次性开销：一旦完成预处理，用户可在该域上实时交互地探索所有三自由度共形映射。这一“以空间换时间”的策略是方法实现实时性的关键设计取舍。

![[assets/figures/papers/paper_list_l49_https_www_inf_usi_ch_hormann_pub_topic_html/figures/008_Table_1.jpg]]
*Table 1: Preprocessing times (in seconds) of our method for triangulating - and determining the values  of the piecewise linear approximations of the Poisson kernels at all mesh vertices and of the other methods for computing a conformal map from - to D*

### 失败模式与限制

1. **负权重导致的非单调调和测度**：方法依赖正权重的 Laplace 算子来保证分段线性 Poisson 核 $\tilde{P}_x$ 的非负性。对于包含狭长三角形的网格，余切权重可能出现负值，导致调和测度 $\tilde{\omega}_x$ 非单调，匹配算法（Algorithm C.4）可能失败。论文建议使用内在 Delaunay 三角剖分来缓解此问题，但未提供系统性的解决方案。

2. **内部扩展的单射性**：使用谐波坐标将边界映射扩展到内部时（Equation 14），理论上不能保证全局单射性——即内部可能出现三角形翻转。论文承认这一理论缺陷，但指出在实际测试中未观察到翻转现象。

3. **仅提供单一共形映射**：方法在给定三自由度约束下输出唯一共形映射，未针对二次准则（如面积失真最小化）进行优化。Figure 10 中 gingerbread man 到火鸡的映射被标注为“somewhat non-conformingly”，暗示在特定目标域形状下映射质量可能下降。

4. **3D 参数化的边界条件**：Figure 14 展示了半球网格到 L 形域的共形参数化，但该方法要求 3D 网格具有明确的边界（如牛头网格的底部边界、半球网格的底面边界），对于闭合曲面需先切割，这限制了直接应用范围。

### 关键实验证据强度评估

| 实验主张 | 证据强度 | 备注 |
|---------|---------|------|
| 实时交互（$O(m)$ 匹配） | 强 | Table 2 提供具体毫秒级数据 |
| 收敛到精确共形映射 | 较强 | Figure 9 显示 $Q_{\text{avg}} \to 1$，但仅测试了枫叶-五叶一对域 |
| 优于 disk-intermediary（crowding 场景） | 强 | Figure 12 为决定性定性证据 |
| 角度失真略优于 BFF | 中等 | Figure 16 仅在 cow head 到 disk 上比较，差异微小 |
| 后向谐波坐标最优 | 较强 | Figure 8 消融清晰，但仅在低分辨率下手- blob 域测试 |
| 边界误差与 Zipper 可比 | 中等 | Figure 15 仅 V 形-blob 一例，需更多域验证 |

总体而言，本文的实验设计聚焦于验证核心主张——实时性、crowding 规避能力和收敛性——并提供了充分的定性证据。定量比较相对有限，尤其在更广泛的域和基线方法上的统计显著性未建立，这部分结论需读者结合具体应用场景判断。

## 定位与知识库关联

本文在共形映射与参数化工具链中改变的核心 **slot** 是 **边界映射策略**：从“通过单位圆盘作为中间域间接映射”（disk-intermediary）切换为“直接匹配源域与目标域的调和测度”（direct harmonic measure matching）。这一改变直击传统圆盘中介法的根本瓶颈——crowding 现象导致内部约束点映射到边界上，使 Möbius 变换无法应用，从而无法可靠求解任意三自由度共形映射。本文绕过中间域，利用调和测度作为共形不变量直接建立边界对应，从根本上规避了 crowding 问题（Figure 3, Figure 12）。

第二个改变的 **slot** 是 **在线映射更新的计算复杂度**：传统方法需要 $O(m^2)$ 或迭代过程来求解边界对应，而本文通过预计算分段线性 Poisson 核和分段二次调和测度，将在线匹配算法压缩为 $O(m)$ 的单次顺序扫描（Section 4.2, Table 2），使交互式探索三自由度共形映射空间成为可能。

### 与已有工作的本质差异

**边界元方法（Zipper 算法）**：Marshall 和 Rohde（2007）的 Zipper 算法基于 Cauchy 积分公式，通过边界元直接计算到单位圆盘的共形映射。它同样面临 crowding 问题，且每次改变约束需要重新计算整个映射。本文方法与之根本不同：不计算到圆盘的映射，而是直接匹配两个域的调和测度，既避免了 crowding，又通过预计算换取了实时交互能力。Figure 15 显示，在 V-shape 到 blob 的极端案例中，本文方法随边界采样数 $m$ 增大收敛到精确边界对应，而 Zipper 在该案例中因 crowding 无法给出可用结果。

**有限元方法（BFF）**：Sawhney 和 Crane（ACM Trans. Graph., 2018）的 Boundary First Flattening 是当前最先进的共形参数化方法，通过求解稀疏线性系统实现边界优先的共形展平，并提供对参数域形状的交互控制。然而，当目标域是任意给定形状（而非自由边界）时，BFF 需要类似 Segall 和 Ben-Chen（2016）的迭代过程来满足边界约束，无法实时更新。本文方法在预处理后，对任意固定目标域可实现毫秒级映射更新（Table 2）。在 cow head 网格到圆盘的参数化质量上，本文方法的面积加权平均角度失真略优于 BFF（Figure 16），但 BFF 在自由边界场景下仍具有无需预计算目标域的优势。

**Schwarz-Christoffel Toolbox**：Driscoll 和 Trefethen（2002）的 SC Toolbox 是计算多边形域到圆盘共形映射的经典工具，基于 Schwarz-Christoffel 公式。它仅适用于多边形域，且需要求解非线性参数问题。本文方法对任意形状域（包括光滑曲线边界）通用，且不依赖 SC 公式的数值反演。

**圆盘中介法（Möbius 组合）**：这是最直接的基线（Figure 2），预计算 $g_1: \Omega_1 \to \mathbb{D}$ 和 $g_2: \Omega_2 \to \mathbb{D}$，再通过 Möbius 变换 $f = g_2^{-1} \circ \varphi_2^{-1} \circ \varphi_1 \circ g_1$ 合成。该方法的致命缺陷是：当 $\Omega_1$ 形状狭长时，$g_1$ 的 crowding 使内部约束点 $x_1$ 的像落在 $\mathbb{D}$ 的边界上（双精度下），Möbius 变换 $\varphi_1$ 无法应用（Figure 3）。本文方法完全弃用圆盘中介，从根本上消除了这一失效模式。

### 知识库挂载点

本文的核心贡献可挂载到以下知识库节点：

1. **调和测度理论**：本文首次将调和测度的共形不变性（$\omega_{x_1}(t_1) = \omega_{x_2}(t_2)$，Equation (5)）转化为可计算的离散匹配算法。调和测度在复分析中是一个经典概念，但此前未被用作共形映射计算的数值工具。本文通过谐波坐标（harmonic coordinates）架起了离散有限元与连续调和测度之间的桥梁——谐波坐标的离散性质（$\sum_k \phi_{ik} = 1$, $\sum_k \phi_{ik} v_k = v_i$）恰好对应 Poisson 核的积分性质（Equation (3)），使得从谐波坐标到分段线性 Poisson 核近似 $\tilde{P}_x$ 再到分段二次调和测度 $\tilde{\omega}_x$ 的推导具有坚实的理论基础（Section 3.1, Appendix B）。

2. **谐波坐标与重心坐标理论**：谐波坐标是 PDE 离散化中的经典工具，本文将其重新解释为 Poisson 核的离散近似，并通过质量集中（mass lumping）技术确保近似的 Poisson 核为正值（$\psi_{ik} = \frac{2}{e_{k-1}+e_k} \phi_{ik}$, Equation (B.2)），从而保证调和测度的单调性，这是匹配算法正确运行的前提。

3. **实时交互式几何处理**：本文贡献了一种“重预处理、轻在线”的范式——将昂贵的 Laplace 方程求解和 Poisson 核缩放矩阵计算放入预处理阶段（Table 1 显示预处理可能需要数十秒），换取在线阶段的 $O(m)$ 匹配和 $O(N)$ 扩展（Table 2 显示在线更新在数毫秒内完成）。这一范式可推广到其他需要实时探索连续解空间的几何处理问题。

### 适用边界

- **域形状要求**：方法适用于任意单连通平面域，包括非凸域和光滑边界域。对于 3D 曲面参数化，需要先将曲面通过现有方法（如 BFF）展平到平面域，再应用本文方法（Figure 14, Figure 17）。
- **网格质量依赖**：方法依赖正权重的 Laplace 算子。对于包含负余切权重的低质量三角形网格，调和测度可能非单调，导致匹配算法失败。可使用内在 Delaunay 三角剖分缓解此问题。
- **单射性保证**：谐波坐标扩展内部映射时，理论上不能保证全局单射性（尽管实践中效果良好）。柯西-格林坐标扩展在数学上更接近共形映射，但可能不完全忠实于边界映射（Figure 8）。
- **优化目标**：方法仅提供满足给定约束的单一共形映射，未针对二次准则（如面积失真最小化）进行优化，不如 BFF 等基于变分框架的方法灵活。

### 后续研究启发

1. **优化框架集成**：将调和测度匹配嵌入到变分优化框架中，在满足用户约束的同时最小化面积失真或其他几何准则，可能结合 BFF 的自由边界思想实现更灵活的交互控制。

2. **鲁棒性增强**：针对非正调和测度（由负 Laplace 权重引起）设计鲁棒的匹配策略，或自动检测并修复导致非单调调和测度的网格区域，将扩展方法的适用范围。

3. **拓扑推广**：调和测度的共形不变性在更高亏格曲面和具有多个边界分量的域上同样成立，将方法推广到此类拓扑需要解决调和测度的多值性和边界分量的对应问题。

4. **应用拓展**：实时共形映射能力可应用于交互式纹理映射、形状插值、医学图像配准等场景，尤其是需要在保持角度不变的前提下探索映射空间的交互式设计任务。

## 原文 PDF

![[paperPDFs/SIGGRAPH_ASIA_2022/Compressing_Geodesic_Information_for_Fast_Point_to_Point_Geodesic_Distance_Queries.pdf]]