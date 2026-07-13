---
title: "Spacetime Representation Learning"
type: paper
paper_level: A
venue: ICLR
year: 2023
pdf_ref: paperPDFs/ICLR_2023/Spacetime_Representation_Learning.pdf
project_link: null
code_link: null
aliases:
- SRL
tags:
- ICLR_2023
- topic/representation_self_supervised_transfer
- topic/representation_self_supervised_transfer/representation_learning
core_operator: "将节点表示限制在开全局双曲凸正常邻域内，并通过基于平行传输的时间分离函数确定边方向，同时使用平滑的平方洛伦兹距离作为可微损失的核心。"
primary_logic: "将有向图建模为洛伦兹预长度空间，利用时空的因果结构与凸正常邻域内的最长因果测地线表示边，配合通过平行传输定义的时间函数，首次实现了可适用于多种时空的统一、可微的有向图表征学习框架。"
claims:
- "在Dupdiv数据集上，Cylindrical Minkowski + eq.6 相比 Sim et al. (2021) 的 TFD 方法平均精度提升约2%（d=10 时 AP 由 69.8 提升至 72.2）。"
- "在社交网络层次抽取任务中，时空方法一致优于其他伪黎曼流形方法（Minkowski + eq.8 在 3D 下取得 Rank of 1st leader = 1.0±0.0，Top10 ρ = 0.80±0.11）。"
- "通过将边限制在凸正常邻域并使用基于平行传输的时间函数，框架可自然地表示有向环（如反德西特空间与圆柱闵可夫斯基空间），且比现有方法的符号时间差更可靠。"
- "Dupdiv (有向图链接预测) 上 Median Average Precision (%) = 72.2 (Cylindrical Minkowski + eq.6, d=10)"
---

# Spacetime Representation Learning

> [!tip] 核心洞察
> 将有向图建模为洛伦兹预长度空间，利用时空的因果结构与凸正常邻域内的最长因果测地线表示边，配合通过平行传输定义的时间函数，首次实现了可适用于多种时空的统一、可微的有向图表征学习框架。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 时空表征学习 |
| 英文题名 | Spacetime Representation Learning |
| 会议/期刊 | ICLR 2023 |
| Links | [paper](https://research.nvidia.com/labs/toronto-ai/spacetime/spacetime_representation_learning.pdf) |
| Topic | #topic/representation_self_supervised_transfer #topic/representation_self_supervised_transfer/representation_learning |
| Method | Spacetime Representation Learning (基于洛伦兹预长度空间的定向图表征框架) |
| Dataset | Dupdiv (有向图链接预测), DREAM5 in silico (有向图链接预测), Social network (层次抽取) |

> [!tip] 效果简介
> - Dupdiv (有向图链接预测) 上，Median Average Precision (%) 为 72.2 (Cylindrical Minkowski + eq.6, d=10)，对比 69.8 (Cylindrical Minkowski + TFD, Sim et al., 2021, d=10)，变化 +2.4。
> - DREAM5 in silico (有向图链接预测) 上，Median Average Precision (%) 为 61.1 (de Sitter + eq.6, d=100)，对比 61.0 (Cylindrical Minkowski + TFD, Sim et al., 2021, d=100)，变化 +0.1。
> - Social network (层次抽取) 上，Rank of 1st leader (↓) / Top10 ρ (↑) 为 Rank 1.0 ± 0.0, Top10 ρ 0.80 ± 0.11 (Minkowski + eq.8, 3D)，对比 higher leader rank and lower ρ with arc-length loss (eq.7) and other pseudo-Riemannian methods，变化 显著提升。

## 概要

### 问题瓶颈

现有有向图表示学习方法在利用时空因果结构时存在根本性局限：**Clough & Evans (2017)** 的闵可夫斯基时空嵌入仅适用于无环有向图，无法处理广泛存在的有向环结构；**Sim et al. (2021)** 虽然通过圆柱闵可夫斯基空间扩展了适用范围，但其时间方向判定依赖全局坐标差的符号（ad hoc 的 Δt），缺乏对非时序时空的统一处理能力，且未能充分利用洛伦兹距离与时间分离函数在凸正常邻域内的优良几何性质。

### 核心方法

本文提出**时空表征学习（Spacetime Representation Learning）**框架，将有限有向图建模为**洛伦兹预长度空间（Lorentzian pre-length space）**，通过以下关键机制实现统一、可微的有向图表征：

- **凸正常邻域约束**：将边的存在限制在开全局双曲凸正常邻域内，避免退化传递连接；
- **时间分离函数**：基于平行传输或柯西时间函数确定边方向，其符号在凸正常邻域内可靠；
- **平方洛伦兹距离**：使用可微的平方洛伦兹距离 χ² 度量因果性与测地线长度，替代传统弧长；
- **统一链接概率**：将距离与时间信息融合为 sigmoid 变换后的乘积形式 F（方程6）。

该框架首次实现了可适用于**闵可夫斯基、de Sitter、反德西特、圆柱闵可夫斯基**等多种时空的统一有向图表征学习。

### 主要结果

- **有向链接预测**：在 Dupdiv 数据集上，Cylindrical Minkowski + eq.6 相比 Sim et al. (2021) 的 TFD 方法平均精度提升约 2%（d=10 时 AP 由 69.8 提升至 72.2，Table 4）；在 DREAM5 数据集上，de Sitter + eq.6 取得 61.1% AP（Table 1）。
- **层次抽取**：时空方法一致优于其他伪黎曼流形方法——Minkowski + eq.8 在 3D 下取得 Rank of 1st leader = 1.0±0.0，Top10 ρ = 0.80±0.11（Table 2）。
- **有向环建模**：通过凸正常邻域与基于平行传输的时间函数，框架可自然地表示有向环（如反德西特空间与圆柱闵可夫斯基空间），且比现有方法的符号时间差更可靠（Section 3.2, Appendix C.2）。

### 方法定位

本工作处于**几何深度学习**与**洛伦兹因果理论**的交叉点，将 Kunzinger & Sämann (2018) 的洛伦兹预长度空间理论首次引入图表征学习。相比纯黎曼方法（如双曲嵌入），本框架通过伪黎曼流形的类时/类空/类光三分结构，原生编码有向边的因果语义；相比早期时空方法（Clough & Evans, 2017），通过凸正常邻域约束与统一的时间分离函数设计，实现了对多种时空流形与有向环结构的泛化支持。

### 当前局限

- 实验仅在节点数不超过数百的小规模图上进行，未验证大规模扩展性；
- 仅考虑指标 ν=1 的洛伦兹流形，未探索高指标伪黎曼流形；
- 凸正常邻域阈值 ε 在多数实验中取为 ∞（全局邻域），其影响未充分消融；
- 时间分离函数的选择依赖对具体时空的先验知识，尚未形成自动化方案。



### 有向图表示学习的核心挑战

现实世界中的图数据天然具有方向性：基因调控网络中的激活/抑制关系、社交网络中的关注/被关注层级、引文网络中的时间先后顺序，均无法被无向图模型充分刻画。然而，有向图的表示学习面临一个根本性瓶颈——**如何在连续嵌入空间中一致地编码边的方向性，同时保持可微优化**。

现有方法大致分为两类。一类完全放弃对方向性的几何建模，转而依赖非对称的评分函数（如基于节点嵌入的点积与可学习参数矩阵的组合）来区分边的方向，但这类方法缺乏对因果结构的显式表征。另一类则试图借助伪黎曼几何：**Clough & Evans (2017)** 最早将节点嵌入到闵可夫斯基时空中，利用时间坐标差的正负号判定边方向。然而，该方法仅适用于无环有向图，无法处理包含有向环的复杂图结构。**Sim et al. (2021)** 在此基础上引入圆柱闵可夫斯基时空与 Triple Fermi-Dirac (TFD) 概率模型，通过周期时间坐标处理有向环，但其时间方向判定仍依赖单一坐标差的符号（即 $\Delta t$），缺乏对一般时空因果结构的统一利用，且未能充分利用洛伦兹距离与时间分离函数在凸正常邻域内的优良性质。

### 方法缺口与核心动机

上述方法的共同缺陷可归结为三点：

1. **时空选择受限**：要么仅局限于闵可夫斯基时空（Clough & Evans, 2017），要么采用无法推广到所有时空的 ad hoc 时间方向判定（Sim et al., 2021）。de Sitter 空间、反 de Sitter 空间等更丰富的时空几何未被纳入有向图表示学习的框架。

2. **因果结构利用不充分**：洛伦兹距离满足逆向三角不等式，且在凸正常邻域内其平方函数为 $C^2$ 光滑，这些性质天然适合作为可微损失函数的核心组件。然而，现有方法并未将边限制在凸正常邻域内，也未系统利用平方洛伦兹距离的因果解释力。

3. **时间方向判定不可靠**：在非时序时空（如圆柱闵可夫斯基空间）中，简单的坐标差符号无法可靠地区分未来与过去方向，导致嵌入学习中的梯度信号不稳定。

### 本文动机

本文的动机源于一个核心洞察：**将有向图建模为洛伦兹预长度空间（Lorentzian pre-length space, Kunzinger & Sämann, 2018），利用时空的因果结构——特别是凸正常邻域内的最长因果测地线表示边，配合通过平行传输定义的时间函数——可以首次实现一个可适用于多种时空的统一、可微的有向图表征学习框架**。

具体而言，该框架通过三个关键设计填补上述缺口：

- 将节点表示限制在开全局双曲凸正常邻域 $V_x$ 内，并通过弧长阈值 $\varepsilon$ 控制可达范围（方程4），使边的存在仅当目标节点在源节点的未来类时锥内。
- 采用基于平行传输或柯西时间函数的时间分离函数 $\tau$，其符号在凸正常邻域内可靠（方程33, 附录C.2），从而统一处理有向环与无环图。
- 以平滑的平方洛伦兹距离 $\chi_U^2$ 作为可微损失的核心（方程5），并将距离与时间信息融合为有向边的预测概率 $F$（方程6）。

这一框架不仅超越了现有方法在有向链接预测与层次抽取任务上的性能，更重要的是，它首次将一般时空的因果结构系统性地引入图表征学习，为探索更复杂的伪黎曼流形编码多重因果关系开辟了道路。



## 核心方法与创新机理

本文的核心创新在于将**有向图显式建模为洛伦兹预长度空间**（Lorentzian pre-length space），从而首次构建了一个可适用于多种时空流形的统一、可微的有向图表征学习框架。其关键突破体现在以下四个相互耦合的维度：

### 1. 从“距离空间”到“因果空间”的范式转换

现有方法要么仅能处理闵可夫斯基时空中的无环有向图（**Clough & Evans, 2017**），要么采用无法推广到一般时空的ad hoc时间方向判定（如 **Sim et al., 2021** 基于全局坐标差的符号判定）。本文的核心洞察在于：有向图的边本质上对应时空中的**因果结构**，而非简单的几何距离。通过将图赋予洛伦兹预长度空间的结构，框架自然地利用**最长因果测地线**表示边，使边的方向性与时空的因果锥结构内禀一致。

### 2. 凸正常邻域约束：避免因果退化的关键设计

框架将边的存在严格限制在**开全局双曲凸正常邻域**（open globally hyperbolic convex normal neighborhood）内。这一设计解决了两个根本问题：
- **防止传递闭包的退化连接**：在一般时空中，若不加邻域约束，类时测地线可能通过“绕行”产生非预期的传递边，导致图结构失真。凸正常邻域保证任意两点间仅存在唯一测地线，且因果顺序由该测地线唯一确定。
- **可微优化基础**：在该邻域内，平方洛伦兹距离 $\chi_{\mathcal{U}}^2$ 是 $C^2$ 函数，满足反向三角不等式，为基于梯度的优化提供了数学保证。

### 3. 基于平行传输的时间分离函数：统一的时间方向判定

时间方向的可靠判定是处理有向环（如反德西特空间与圆柱闵可夫斯基空间中的周期时间坐标）的核心挑战。现有方法（如 Sim et al., 2021）依赖单一坐标差的符号，在非时序时空中失效。本文提出通过**平行传输**或柯西时间函数定义时间分离函数 $\tau$，其符号在凸正常邻域内可靠地区分未来与过去方向。对于圆柱闵可夫斯基空间，进一步设计了基于取模运算的周期时间分离函数，使框架能够自然地表示有向环结构。

### 4. 距离与时间的可微融合：链接概率函数 $F$

框架将链接概率建模为距离与时间信息的乘积融合：

$$F(\mathbf{x}_i, \mathbf{x}_j) := \sigma_{\theta_1}^{m}(\chi_{\gamma}^{2}(\mathbf{x}_i, \mathbf{x}_j)) \cdot \sigma_{\theta_2}^{m}(\tau(\mathbf{x}_i, \mathbf{x}_j))$$

这一设计使模型能够同时学习“边应该对应多长的类时间隔”以及“时间方向的置信度”，相比仅基于距离的损失函数（如 **Law & Stam, 2020** 的弧长对数比损失）或 Triple Fermi-Dirac 函数（Sim et al., 2021），在链接预测和层次抽取任务上均取得一致提升。

### 证据强度总结

| 创新维度 | 核心证据 | 置信度 |
|---------|---------|--------|
| 因果空间建模 | 在多种时空（闵可夫斯基、de Sitter、圆柱闵可夫斯基、反德西特）上一致有效（Table 2, Table 4） | 高 |
| 凸正常邻域约束 | 圆柱闵可夫斯基空间中，使用邻域约束+方程6相比TFD提升约2% AP（Table 4） | 高 |
| 时间分离函数 | de Sitter空间中坐标差形式优于平行传输形式（Table 3）；圆柱闵可夫斯基空间中周期函数有效处理有向环 | 中高 |
| 链接概率融合 | 平方洛伦兹距离在层次抽取中优于弧长（Table 2）；方程6在Dupdiv上一致优于TFD（Table 4） | 高 |

**需注意的局限**：凸正常邻域的超参数 $\varepsilon$ 在多数实验中被设为 $\infty$（全局邻域），其对复杂图结构的影响尚未系统消融；时间分离函数的选择目前依赖对具体时空的先验知识，尚未形成自动化方案。



本工作提出一个**时空表征学习（Spacetime Representation Learning）**框架，将有向图嵌入到一类广泛的洛伦兹时空中，利用时空的因果结构自然地编码有向边的方向性与传递性。框架的核心思路是将有限有向图构造为**洛伦兹预长度空间（Lorentzian pre-length space）**，从而将图的边约束在节点所在凸正常邻域的未来时间锥内。

整体 pipeline 由以下模块串联构成：

1. **节点在时空流形上的初始化**：为每个节点 $v_i$ 分配一个时空事件坐标 $\mathbf{x}_i \in \mathcal{M}$，其中 $\mathcal{M}$ 为选定的洛伦兹流形（如闵可夫斯基时空 $\mathbb{R}_\nu^d$、de Sitter 空间 $\mathbb{S}_1^d(r)$、反 de Sitter 空间 $\mathbb{H}_1^d(r)$ 或圆柱闵可夫斯基时空等）。

2. **凸正常邻域与未来时间锥约束**：对每个节点 $\mathbf{x}$，定义其开全局双曲凸正常邻域 $\mathcal{V}_{\mathbf{x}}$ 及未来时间锥 $\mathcal{C}_{\mathbf{x}}^{+}(\mathbf{t})$。有向边 $(v_i, v_j)$ 的存在条件为：$\mathbf{x}_j$ 落在 $\mathbf{x}_i$ 的**时序未来集（chronological future set）**内，即满足
   $$
   \mathcal{Z}^{+}(\mathbf{x}_i, \mathcal{V}_{\mathbf{x}_i}) = \{ \mathbf{y} \in \mathcal{U}_{\mathbf{x}_i} : -\varepsilon^{2} < \langle \overrightarrow{\mathbf{x}_i\mathbf{y}}, \overrightarrow{\mathbf{x}_i\mathbf{y}} \rangle < 0,\; \overrightarrow{\mathbf{x}_i\mathbf{y}} \in \mathcal{C}_{\mathbf{x}_i}^{+}(\mathbf{t}) \}
   $$
   其中 $\varepsilon$ 为弧长阈值，控制邻域的有效范围；$\langle\cdot,\cdot\rangle$ 为伪欧几里得标量积（方程1）。这一约束确保边仅沿未来指向的类时测地线存在，从而天然避免了非因果的传递闭包连接。

3. **平方洛伦兹距离 $\chi_{\mathcal{U}}^2$**：在凸正常邻域内，定义可微的平方洛伦兹距离（方程5），用于度量事件间的因果间隔。对于闵可夫斯基时空，其形式为 $\chi_{\mathcal{U}}^2(\mathbf{x},\mathbf{y}) = (y_0 - x_0)^2 - \sum_{j=1}^{d-1}(y_j - x_j)^2$。该函数在凸正常邻域内为 $C^2$ 光滑，支持基于梯度的优化；当两点非因果相关时，采用外蕴几何的扩展定义以保证处处可微。

4. **时间分离函数 $\tau$**：通过平行传输或柯西时间函数确定事件间的时间方向，其符号在凸正常邻域内可靠地区分未来与过去。例如圆柱闵可夫斯基空间中采用取模运算处理周期时间坐标：
   $$
   \tau(\mathbf{x},\mathbf{y}) = \left( \left( y_0 - x_0 + \frac{C}{2} \right) \bmod C \right) - \frac{C}{2} \in [-\frac{C}{2}, \frac{C}{2})
   $$

5. **链接概率函数 $F$**：将距离信息与时间方向信息融合为有向边的预测概率：
   $$
   F(\mathbf{x}_i, \mathbf{x}_j) = \sigma_{\theta_1}^{m}\big( \chi_{\gamma}^{2}(\mathbf{x}_i, \mathbf{x}_j) \big) \cdot \sigma_{\theta_2}^{m}\big( \tau(\mathbf{x}_i, \mathbf{x}_j) \big)
   $$
   其中 $\sigma_\theta^m$ 为带可学习参数的 sigmoid 变换。该乘积形式同时要求边在因果上可达（距离项）且方向正确（时间项）。

6. **伪黎曼优化器**：在流形上通过指数映射与平行传输更新节点嵌入，保持流形几何约束。训练时可采用交叉熵损失（有向链接预测）或基于距离的排序损失（层次抽取，方程8）。

**输入**：有向图 $G = (V, E)$，选定的时空流形 $\mathcal{M}$ 及其维度 $d$，邻域阈值 $\varepsilon$，参考时间向量场 $\mathbf{t}$。

**输出**：每个节点 $v_i$ 在 $\mathcal{M}$ 上的嵌入坐标 $\mathbf{x}_i$，以及由 $F(\mathbf{x}_i, \mathbf{x}_j)$ 给出的有向边预测概率。

该框架的关键创新在于：通过将边限制在凸正常邻域并使用基于平行传输的时间函数，**首次实现了可适用于多种时空（包括含闭类时曲线的圆柱闵可夫斯基时空）的统一、可微的有向图表征学习**，而此前方法要么局限于闵可夫斯基时空（Clough & Evans, 2017），要么采用无法推广到所有时空的 ad hoc 时间方向判定（Sim et al., 2021）。



### 3.1 时空图构建：凸正常邻域与未来时间锥

框架的核心操作是将有向图建模为洛伦兹预长度空间，并通过**凸正常邻域**（convex normal neighborhood）约束边的存在。对于每个节点 $v_i$，其嵌入点 $\mathbf{x}_i$ 位于时空流形 $\mathcal{M}$ 上，并关联一个开全局双曲凸正常邻域 $\mathcal{V}_{\mathbf{x}_i}$。边 $v_i \to v_j$ 存在的必要条件是 $\mathbf{x}_j$ 落在 $\mathbf{x}_i$ 的**未来类时锥**内，且弧长不超过阈值 $\varepsilon$：

$$\mathcal{Z}^{+}(\mathbf{x}, \mathcal{V}_{\mathbf{x}}) = \{ \mathbf{y} \in \mathcal{U}_{\mathbf{x}} : -\varepsilon^{2} < \langle \overrightarrow{\mathbf{xy}}, \overrightarrow{\mathbf{xy}} \rangle < 0,\ \overrightarrow{\mathbf{xy}} \in \mathcal{C}_{\mathbf{x}}^{+}(\mathbf{t}) \}$$

其中 $\overrightarrow{\mathbf{xy}}$ 是连接向量，$\langle\cdot,\cdot\rangle$ 是伪欧几里得标量积，$\mathcal{C}_{\mathbf{x}}^{+}(\mathbf{t})$ 是由参考类时向量 $\mathbf{t}$ 定义的未来指向类时向量锥。这一约束的关键意义在于：**仅通过类时测地线定义时序关系**，避免了类空或类光连接带来的因果歧义。阈值 $\varepsilon$ 控制邻域大小；实验表明多数情况下取 $\varepsilon = \infty$（全局邻域）已能工作，但其对复杂图结构的影响尚未充分消融。

### 3.2 平方洛伦兹距离 $\chi_{\mathcal{U}}^2$

框架采用**可微的平方洛伦兹距离**作为核心度量，替代传统方法中不可微的弧长 $d_\gamma$。在凸正常邻域 $\mathcal{U}_{\mathbf{x}}$ 上，平方洛伦兹距离定义为连接向量伪范数的负值：

$$\chi_{\mathcal{U}}^2(\mathbf{x},\mathbf{y}) := -\langle \overrightarrow{\mathbf{x}\mathbf{y}}, \overrightarrow{\mathbf{x}\mathbf{y}} \rangle_\nu$$

以闵可夫斯基时空 $\mathbb{R}_1^d$ 为例，其显式形式为：

$$\chi_{\mathcal{U}}^2(\mathbf{x},\mathbf{y}) = (y_0 - x_0)^2 - \sum_{j=1}^{d-1} (y_j - x_j)^2$$

当 $\chi_{\mathcal{U}}^2 > 0$ 时，两事件为**类时分离**，且 $\mathbf{y}$ 在 $\mathbf{x}$ 的时序未来。该函数在凸正常邻域内为 $C^2$ 光滑，支持基于梯度的伪黎曼优化。对于 $\mathbf{x}$ 和 $\mathbf{y}$ 非因果相关的情况，框架通过外蕴几何定义了一个分段可微扩展（方程5），保证训练全程可微。

### 3.3 时间分离函数 $\tau$

时间方向判定是区分有向边方向的核心机制。框架通过**时间分离函数** $\tau(\mathbf{x},\mathbf{y})$ 的符号确定边方向，其设计依赖于具体时空的因果结构：

- **闵可夫斯基时空**：$\tau(\mathbf{x},\mathbf{y}) = y_0 - x_0$，即时间坐标差。
- **圆柱闵可夫斯基时空**（处理周期时间坐标 $C$）：
  $$\tau(\mathbf{x},\mathbf{y}) := \left(\left(y_0 - x_0 + \frac{C}{2}\right) \bmod C\right) - \frac{C}{2} \in [-\frac{C}{2}, \frac{C}{2})$$
  该取模操作使得有向环可被自然表示。
- **de Sitter 时空**：消融实验表明，基于简单坐标差的时间函数（方程33）反而优于基于平行传输的版本（方程32），说明时间函数的设计需根据具体流形调整。

在凸正常邻域内，$\tau$ 的符号可靠地指示时序方向，避免了 **Sim et al. (2021)** 等基于全局坐标差符号判定在非时序时空中的失效问题。

### 3.4 链接概率函数 $F$

有向边的预测概率由距离与时间信息融合得到：

$$F(\mathbf{x}_i, \mathbf{x}_j) := \sigma_{\theta_1}^{m}(\chi_{\gamma}^{2}(\mathbf{x}_i, \mathbf{x}_j)) \cdot \sigma_{\theta_2}^{m}(\tau(\mathbf{x}_i, \mathbf{x}_j))$$

其中 $\sigma_\theta^m$ 是带可学习参数 $\theta$ 的 sigmoid 变换。该公式将**平方洛伦兹距离**（衡量因果关联强度）与**时间分离函数**（判定方向）通过乘积耦合。消融实验证实，在 Dupdiv 数据集上，该概率函数相比 **Sim et al. (2021)** 的 Triple Fermi-Dirac (TFD) 在圆柱闵可夫斯基空间上平均精度提升约 2%（$d=10$ 时 AP 由 69.8 提升至 72.2，Table 4）。

### 3.5 层次抽取损失

对于社交网络层次抽取任务，框架采用鼓励边对应类时测地线、非边对应类空测地线的损失函数：

$$\min_{\{\mathbf{x}_k\in\mathcal{M}\}_{k=1}^n} \sum_{(v_a,v_b)\notin E} \sigma_\theta\left(\mathsf{d}(\mathbf{x}_a,\mathbf{x}_b)\right) + \lambda \sum_{(v_i,v_j)\in E} \sigma_\theta\left(-\mathsf{d}(\mathbf{x}_i,\mathbf{x}_j)\right)$$

其中 $\mathsf{d}$ 可取弧长 $d_\gamma$ 或平方洛伦兹距离 $\chi^2$。消融实验表明，$\chi^2$ 在排序相关系数上优于 $d_\gamma$（Table 2），因为平方距离对长距离类空对的惩罚更平滑。

### 3.6 伪黎曼优化器

嵌入通过伪黎曼流形上的随机梯度下降进行优化（Algorithm 1, Appendix F）。每次迭代计算欧几里得梯度后，将其投影到切空间，再通过**指数映射** $\exp_{\mathbf{x}}$ 更新流形上的点，保证嵌入始终满足时空几何约束。



## 实验与关键发现

### 有向图链接预测

框架在多个有向图链接预测基准上进行了评估，核心对比对象为 **Sim et al. (2021)** 提出的圆柱闵可夫斯基空间配合 Triple Fermi-Dirac (TFD) 概率模型。实验采用中位平均精度 (Median AP) 作为指标，在 20 次随机初始化下测量。

**Dupdiv 数据集**（Table 4）：圆柱闵可夫斯基空间配合方程 6 的概率函数在 10 维嵌入下取得 **72.2%** 的中位 AP，相较 Sim et al. (2021) 的 TFD 方法（69.8%）提升约 **2.4 个百分点**。这一提升的因果机制在于：方程 6 将平方洛伦兹距离与时间分离函数以 sigmoid 乘积形式融合，比单纯依赖距离的 TFD 更精确地捕捉了有向边的因果方向。此外，凸正常邻域约束（方程 4）限制了边的存在范围，避免了全局坐标差符号判定在含环图中的失效。

**DREAM5 in silico 数据集**（Table 1）：de Sitter 空间配合方程 6 在 100 维下取得 **61.1%** AP，与圆柱闵可夫斯基 + TFD 的 61.0% 基本持平（+0.1%）。该结果表明，在无环或弱环结构的生物调控网络中，时空方法至少与现有最优方法性能相当。de Sitter 空间的恒定正曲率为嵌入提供了额外的几何灵活性，但在此任务上未转化为显著优势。

**圆柱闵可夫斯基空间的优势**：该时空通过取模运算处理周期时间坐标（Section 5.1 中的时间分离函数），能够自然地表示有向环结构。Table 4 的消融显示，在圆柱闵可夫斯基空间中，方程 6 在所有维度设置下一致优于 TFD，验证了时间分离函数与距离联合建模的必要性。

### 社交网络层次抽取

层次抽取任务评估嵌入空间能否恢复社交网络中的支配/从属关系。评价指标包括首位领导者的排名 (Rank of 1st leader, ↓) 和 Top-10 的 Spearman ρ 相关系数 (↑)。

**Table 2** 的结果揭示了两个关键发现：

1. **时空方法一致优于其他伪黎曼流形方法**：闵可夫斯基空间配合方程 8（层次抽取损失）在 3 维嵌入下取得 **Rank of 1st leader = 1.0 ± 0.0** 和 **Top-10 ρ = 0.80 ± 0.11**，显著优于基于弧长的对数比损失（方程 7，Law & Stam, 2020）和其他伪黎曼流形变体。因果机制在于：方程 8 鼓励边对应类时测地线、非边对应类空测地线，这与时空的因果结构天然一致。

2. **平方洛伦兹距离 χ² 优于弧长 d_γ**：Table 2 的消融显示，使用 χ² 作为距离函数比使用弧长 d_γ 获得更高的排序相关系数。这是因为 χ² 在凸正常邻域内为 C² 光滑函数，提供了更稳定的优化梯度；而弧长在类光边界处不可微，可能导致优化不稳定。

![[assets/figures/papers/paper_list_l19_https_research_nvidia_com_labs_toronto_ai_spacetime_spacetime_representa/figures/003_Table_2.jpg]]
*Table 2: Evaluation scores for the different learned representations (mean ± standard deviation). ↓ the lower the metric, the better. ↑ the larger the metric (in absolute value), the better*

**Table 5** 提供了子组分析，进一步验证了上述结论在不同社交群体中的一致性。

### 时间顺序保持

**Table 3** 评估了引用网络中嵌入对时间顺序的保持能力。在 de Sitter 空间上，使用简单坐标差时间函数（方程 33）的时间顺序保持百分比优于基于平行传输的时间函数（方程 32）。这一消融发现表明：对于特定时空，基于坐标的简单时间函数可能比理论上更通用的平行传输方法更有效，因为后者依赖于参考类时向量场的选取，而该选取在优化过程中可能引入额外噪声。

### 关键消融与失败模式

**凸正常邻域阈值 ε 的影响**：多数实验中 ε 被设为 ∞（全局邻域），这意味着邻域约束实际上未生效。Table 4 中圆柱闵可夫斯基空间的提升主要来自方程 6 的概率建模，而非邻域约束本身。对于含密集有向环的图，全局邻域可能导致“虚假传递边”问题——即通过长程测地线意外连接了不应直接相连的节点。该超参数的影响尚未被系统消融。

**时间分离函数的选择依赖任务先验**：de Sitter 空间中坐标差优于平行传输（Table 3），但该结论是否可推广到其他时空（如反德西特空间）未经验证。框架目前缺乏自动选择 τ 形式的机制。

**大规模扩展性未验证**：所有实验均在节点数不超过数百的图上进行。伪黎曼优化器（Algorithm 1）的指数映射和凸正常邻域判定涉及的计算复杂度为 O(d²) 至 O(d³)，在百万级节点图上的可行性未知。

### 可视化证据

**Figure 2** 展示了在闵可夫斯基和 de Sitter 空间上学到的 2D/3D 嵌入。在闵可夫斯基空间中，嵌入坐标呈现清晰的时间分层结构，领导节点（未来方向）与从属节点（过去方向）沿时间轴自然分离。**Figure 3** 的 HEP-TH 引用网络嵌入进一步验证了时间顺序的保持：早期论文和晚期论文在时间坐标上形成单调的因果序列。**Figure 4** 展示了反德西特空间中的嵌入，证明了框架对负曲率时空的兼容性。

### 补充图表

![[assets/figures/papers/paper_list_l19_https_research_nvidia_com_labs_toronto_ai_spacetime_spacetime_representa/figures/004_Figure_2.jpg]]
*Figure 2: (left) Coordinates of 2-dimensional embeddings ${ \bf$ x } = ( $x _ { 0 } , x _ { 1 } ) ^ { \top }$ learned with equation 8 when $\mathcal { M } = \mathbb { R } _ { 1 } ^ { 2 }$ (right) Coordinates of the first three coordinates of embeddings $\mathbf { x }$ \ = ( $x _ { 0 } , x _ { 1 } , x _ { 2 } , x _ { 3 } ) ^ { \mid }$ learned with equation 8 when $\mathcal { M } = \mathbb { S } _ { 1 } ^ { 3 }$ ( r ) In Lorentz geometry, a timelike geodesic joining two points is the longest timelike curve in a given convex normal neighborhood. This translates in the high-level nodes $v _ { 1 }$ and $v _ { 3 4 }$ being the furthest from the rest of the nodes. The ground truth edges are plotted in yellow and the node c...

![[assets/figures/papers/paper_list_l19_https_research_nvidia_com_labs_toronto_ai_spacetime_spacetime_representa/figures/010_Figure_5.jpg]]
*Figure 5: (top) Coordinates of 2-dimensional embeddings $\mathbf { x }$ ~ = ~ ( $x _ { 0 } , x _ { 1 } ) ^ { \top }$ learned with equation 8 when $\bf \dot { \mathcal { M } }$ ~ = ~ $\mathbb { R } _ { 1 } ^ { 2 }$ (bottom) Coordinates of the first three coordinates of embeddings ${ \bf$ x } = ( $x _ { 0 } , x _ { 1 } , x _ { 2 } , x _ { 3 } ) ^ { \top }$ learned with equation 8 when $\mathcal { M } = \mathbb { S } _ { 1 } ^ { 3 }$ ( r ) . In Lorentz geometry, a timelike geodesic joining two points is the longest timelike curve in a given convex normal neighborhood. This translates in the high-level nodes $v _ { 1 }$ and $v _ { 3 4 }$ being the furthest from the rest of the nodes. The ground truth edges are plotted in...

![[assets/figures/papers/paper_list_l19_https_research_nvidia_com_labs_toronto_ai_spacetime_spacetime_representa/figures/002_Table_1.jpg]]
*Table 1: Link prediction for directed graphs. Median average precision (AP) percentages across 20 random initializations on a held-out test set*

![[assets/figures/papers/paper_list_l19_https_research_nvidia_com_labs_toronto_ai_spacetime_spacetime_representa/figures/005_Table_3.jpg]]
*Table 3: Preservation of chronological order between pairs of articles with one citing the other*

![[assets/figures/papers/paper_list_l19_https_research_nvidia_com_labs_toronto_ai_spacetime_spacetime_representa/figures/007_Table_4.jpg]]
*Table 4: Link prediction for directed graphs. Median average precision (AP) percentages across 20 random initializations on a held-out test set*

![[assets/figures/papers/paper_list_l19_https_research_nvidia_com_labs_toronto_ai_spacetime_spacetime_representa/figures/008_Table_5.jpg]]
*Table 5: Evaluation scores for the different learned representations (mean ± standard deviation). ↓ the lower the metric, the better. ↑ the larger the metric, the better*



## 定位与知识库关联

### 1. 与现有有向图表征方法的关系

**早期时空嵌入方法**：将图嵌入到闵可夫斯基时空以建模有向无环图的想法可追溯至 **Minkowski spacetime embedding**（Clough & Evans, 2017），该方法利用闵可夫斯基度规的因果锥结构编码偏序关系，但仅适用于无环有向图，无法处理现实世界中广泛存在的有向环结构。本文框架通过引入凸正常邻域约束和基于平行传输的时间分离函数，将适用范围从闵可夫斯基时空扩展至 de Sitter、反 de Sitter、圆柱闵可夫斯基等更一般的全局双曲时空，从而自然地表示有向环。

**基于时间方向判定的方法**：**Sim et al.（2021）** 提出在圆柱闵可夫斯基空间中使用 Triple Fermi-Dirac（TFD）函数进行有向链接预测，其时间方向判定依赖于全局坐标差的符号。该方法存在两个根本局限：（1）时间方向判定采用 ad hoc 方式，无法推广到非时序时空；（2）未充分利用洛伦兹距离在凸正常邻域内的优良性质。本文在相同任务设定下（Dupdiv 数据集，圆柱闵可夫斯基空间），用方程 6 的概率函数替代 TFD，将中位平均精度从 69.8% 提升至 72.2%（Table 4），提升约 2.4 个百分点，验证了基于平方洛伦兹距离与时间分离函数乘积的链接概率模型的优势。

**基于弧长的层次抽取方法**：**Law & Stam（2020）** 提出的基于弧长的对数比损失（方程 7）用于层次抽取，其核心是最大化边对应测地线的弧长、最小化非边对应测地线的弧长。本文的方程 8 在相同框架下将弧长替换为平方洛伦兹距离 χ²，在社交网络层次抽取任务中取得显著更好的排序相关系数（Table 2：Minkowski + eq.8 在 3D 下取得 Rank of 1st leader = 1.0±0.0，Top10 ρ = 0.80±0.11），表明平方洛伦兹距离在凸正常邻域内作为 C² 函数比弧长更适合梯度优化。

### 2. 核心差异与适用边界

**邻域约束的引入**：现有伪黎曼流形方法（包括 Sim et al., 2021; Law & Stam, 2020）未对嵌入点的邻域施加明确约束，导致可能出现非因果的测地线连接。本文通过方程 4 将边的存在限制在开全局双曲凸正常邻域 V_x 内，并通过弧长阈值 ε 控制可达范围。这一设计确保了：（1）仅类时测地线可表示边；（2）时间分离函数的符号在邻域内可靠。然而，多数实验中 ε 被设为 ∞（全局邻域），其实际约束作用未充分验证，需要进一步消融研究。

**时间分离函数的统一化**：在 de Sitter 空间中，消融实验（Table 3）显示基于简单坐标差的时间函数（方程 33）优于基于平行传输的时间函数（方程 32），表明时间分离函数的最优形式依赖于具体时空的先验知识。目前尚缺乏自动选择 τ 形式的统一方案，这构成该框架向未知图结构推广时的关键瓶颈。

**适用边界**：
- 当前框架仅适用于指标 ν=1 的洛伦兹流形，未探索 ν>1 的高指标伪黎曼流形，后者可能编码更复杂的多重因果关系（如多类型边的有向图）。
- 实验仅在节点数不超过数百的小规模图上进行（Dupdiv、DREAM5、社交网络），未验证扩展到百万级节点的可行性。伪黎曼优化器（Algorithm 1）的计算复杂度与节点数平方相关，大规模场景下需要近似或采样策略。
- 不同时空的选择（闵可夫斯基、de Sitter、圆柱闵可夫斯基等）依赖任务先验，例如圆柱闵可夫斯基适用于含周期时间结构的图，de Sitter 适用于正曲率因果结构，但框架未提供自动流形选择机制。

### 3. 局限与开放问题

**已确认的局限**：
1. **规模扩展性未验证**：所有实验在数百节点规模下进行，伪黎曼流形上的指数映射与平行传输操作的计算开销在大图上可能成为瓶颈。
2. **超参数 ε 的影响未系统研究**：凸正常邻域的阈值 ε 在多数实验中被设为 ∞，其对复杂图结构（如稠密有向环）的影响及自动选择策略尚未探索。
3. **时间分离函数的选择依赖先验**：de Sitter 空间中坐标差优于平行传输（Table 3），但该结论是否可推广至其他时空未经验证。
4. **仅考虑指标 1 的洛伦兹流形**：未探索高指标伪黎曼流形对多重因果关系的表达能力。

**开放问题**：
1. **自动流形选择**：能否根据图的结构特征（如有向环的分布、度分布的偏度）自动为给定任务选择最合适的时空流形及对应超参数？
2. **端到端时间函数学习**：是否可以将时间分离函数 τ 与距离函数 χ² 的学习联合端到端优化，使框架摆脱对人工选择 τ 形式的依赖？
3. **大规模优化**：如何高效地在百万节点以上的图上进行时空嵌入的优化与推理？是否可借鉴双曲空间中的 Poincaré 球投影技巧来加速伪黎曼梯度计算？
4. **高指标扩展**：将框架推广到 ν>1 的伪黎曼流形后，能否编码有向图中不同类型的因果关系（如层级关系与引用关系的共现）？



## 原文 PDF

![[paperPDFs/ICLR_2023/Spacetime_Representation_Learning.pdf]]
