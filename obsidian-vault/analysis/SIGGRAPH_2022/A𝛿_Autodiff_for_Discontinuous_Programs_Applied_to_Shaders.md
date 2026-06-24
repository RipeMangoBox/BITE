---
title: "A𝛿: Autodiff for Discontinuous Programs — Applied to Shaders"
type: paper
paper_level: A
venue: SIGGRAPH
year: 2022
pdf_ref: paperPDFs/SIGGRAPH_2022/A_Autodiff_for_Discontinuous_Programs_Applied_to_Shaders.pdf
project_link: "https://thenounproject.com/icon/celtic-1975448/"
code_link: "https://github.com/yyuting/Adelta"
aliases:
- ADPAS
tags:
- SIGGRAPH_2022
- topic/other_unclear
core_operator: A𝛿
primary_logic: A𝛿
claims:
- A𝛿
---

# A𝛿: Autodiff for Discontinuous Programs — Applied to Shaders

> [!tip] 核心洞察
> A𝛿

| 字段 | 内容 |
|------|------|
| 中文题名 | A𝛿: Autodiff for Discontinuous Programs — Applied to Shaders |
| 英文题名 | A𝛿: Autodiff for Discontinuous Programs — Applied to Shaders |
| 会议/期刊 | SIGGRAPH 2022 |
| Links | [paper](https://www.cs.princeton.edu/~yutingy/docs/siggraph_2022.html) · [Code](https://github.com/yyuting/Adelta) · [Project](https://thenounproject.com/icon/celtic-1975448/) · [arXiv](http://arxiv.org/abs/1604.06174) |
| Topic | #topic/other_unclear |
| Method |  |
| Dataset |  |

## 概要

**问题**：含间断（discontinuity）的着色器程序无法直接使用传统自动微分，而有限差分等替代方案效率极低。

**方法**：本文提出 Aδ 编译器，核心是将间断函数的梯度近似为沿一维采样轴的盒式核预滤波梯度，并据此设计了一套适用于通用程序的近似导数规则。编译器自动将领域特定语言（DSL）描述的着色器转换为可微分代码，在保持 O(1) 时间复杂度的前提下处理各类间断。

**主要结果**：在 Olympic Rings 着色器优化任务上，本方法的中位成功时间仅 **1.4 秒**，相比有限差分（FD*）和 SPSA* 的 13.8 秒，**加速约 9.9 倍**，且能在约 15 秒内收敛到视觉几乎一致的目标图像。

**定位**：相比于传统自动微分（无法处理间断）、有限差分（计算开销大）以及 TEG、可微矢量图形等方法，本方法在通用性（覆盖整个 DSL）与计算效率（O(1)）之间取得了突破性平衡。

## 核心方法与创新机理

### 问题瓶颈：着色器程序中的不连续性与梯度失效

着色器程序广泛存在于图形渲染管线中，其参数空间通常包含大量由分支、条件判断和离散操作引入的**不连续性**。传统自动微分（AD）在处理这类程序时面临根本性困难：对于形如 Heaviside 阶跃函数 $H(\cdot)$ 的不连续点，AD 产生的 Dirac delta 梯度在数值上几乎处处为零，无法为基于梯度的优化提供有效下降方向。这一瓶颈导致现有方法不得不依赖有限差分（FD）或随机扰动（SPSA）等零阶优化策略，收敛速度极慢——在 Olympic Rings 等典型着色器优化任务中，FD 和 SPSA 的中位成功时间高达 13.8 秒，而本文方法仅需 1.4 秒，加速约 9.9 倍。

问题的本质在于：**渲染过程的最终像素值本质上是着色器函数在采样点上的离散评估结果，而参数变化引起的渲染差异实际上表现为不连续边界的移动**。传统 AD 无法捕获这种“边界移动”的梯度信息，因为它在每个采样点独立求导，忽略了采样点之间的结构关联。

### 核心创新：基于预滤波的近似梯度规则

本文的核心贡献是一套**适用于不连续程序的近似导数规则**，其理论根基在于将梯度计算重新表述为预滤波（prefiltering）问题。具体而言：

**核心思想**：对于任意含不连续性的程序 $f(x, \vec{\theta})$，不直接求其在单点 $x$ 处的导数，而是先沿**采样轴**（sampling axis）$x$ 用一维盒式核（box kernel）对函数进行卷积平滑，再对平滑后的函数求导：

$$\hat{f}(x, \vec{\theta}; \epsilon) = \frac{1}{(\alpha + \beta) \epsilon} \int_{x - \alpha \epsilon}^{x + \beta \epsilon} f(x', \vec{\theta}) dx'$$

其中 $\epsilon$ 为核的半宽度，$\alpha, \beta$ 控制核的左右延伸范围。这一预滤波操作将原本尖锐的不连续边界“模糊化”，使得梯度在采样点邻域内非零，从而为优化提供有意义的信号。

**为什么选择一维盒式核**：盒式核是分段常数函数，这使得 $\phi(x - x_d)$ 的计算退化为简单的区间归属判断——只需检测 $x - x_d \in [-\epsilon, \epsilon]$ 是否成立，无需计算复杂的核函数值。这一选择将定位不连续点的额外计算开销降至最低，是实现 $O(1)$ 时间复杂度的关键。

### 关键假设与适用边界

方法建立在一条核心假设之上：

> **(A1)** 在采样轴上，每个采样点与其最近邻采样点之间**至多存在一个不连续点**。

这一假设的物理含义是：盒式核的宽度 $\epsilon$ 被设置为采样间距的量级，使得每个核覆盖范围内不会出现多个不连续边界相互干扰的情况。当假设不满足时（例如不连续点密集分布），梯度估计的精度会下降，但方法本身不会崩溃——这构成了方法的主要失效边界。

### 方法框架：从 DSL 到可微分程序

整个系统围绕一个**最小化领域特定语言（DSL）**构建，其语法由 Backus-Naur 范式定义：

$$e_d ::= C \mid \boldsymbol{x} \mid \theta \mid e_d + e_d \mid e_d \cdot e_d \mid H(e_d) \mid f(e_d)$$

该 DSL 包含六类基本构造：
- **常量** $C$：不可微分的标量值
- **采样轴变量** $\boldsymbol{x}$：渲染过程中的空间坐标
- **可优化参数** $\theta$：着色器程序中待调整的变量
- **算术运算**：加法和乘法
- **Heaviside 阶跃函数** $H(\cdot)$：不连续性的唯一来源
- **连续原子函数** $f(\cdot)$：任意可微的连续函数

这一 DSL 的设计具有关键的结构性意义：**它将程序中的不连续性显式隔离到 $H(\cdot)$ 算子中**，使得编译器可以精确识别需要特殊梯度规则的“Dirac 参数”——即任何被 $H(e_d)$ 表达式依赖的参数 $\theta$。对于非 Dirac 参数，系统回退到标准 AD 规则；对于 Dirac 参数，则触发预滤波梯度规则。

### 梯度规则体系：三个核心规则

编译器实现了三组差异化规则（见表 2），构成完整的梯度计算体系：

**规则 1：Heaviside 函数的预滤波梯度**

对于最基础的不连续构造 $H(x + \theta)$，其预滤波梯度为：

$$\frac{\partial}{\partial \theta} \int H(x' + \theta) \phi(x - x') dx' = \phi(x + \theta)$$

即梯度等于盒式核在 $x + \theta$ 处的取值。这一规则将 Dirac delta 替换为有限宽度的核函数值，使得梯度在 $x_d = -\theta$ 附近 $\pm \epsilon$ 范围内非零。

**规则 2：一般不连续函数的链式法则扩展**

对于复合形式 $H(c(x, \theta))$，利用 Dirac delta 的缩放性质：

$$\frac{\partial}{\partial \theta} \int H(c(x', \theta)) \phi(x - x') dx' = \left. \frac{\frac{dc}{d\theta}}{|\frac{dc}{dx}|} \right|_{x_d} \phi(x - x_d)$$

其中 $x_d$ 是满足 $c(x_d, \theta) = 0$ 的不连续点位置。这一规则的关键在于：**梯度强度由不连续边界在参数空间中的移动速率（分子 $\frac{dc}{d\theta}$）与在采样空间中的变化速率（分母 $|\frac{dc}{dx}|$）之比决定**，再乘以核函数在采样点与边界距离上的权重。

**规则 3：盒式核的区间采样简化**

由于盒式核分段常数，$\phi(x - x_d)$ 的计算退化为：

$$\phi(x - x_d) = \begin{cases} 1 & \text{if } x - x_d \in [-\epsilon, \epsilon] \\ 0 & \text{otherwise} \end{cases}$$

这意味着编译器无需计算核函数值，只需判断采样点 $x$ 是否落在不连续边界 $x_d$ 的 $\epsilon$ 邻域内。这一简化是方法 $O(1)$ 时间复杂度的直接保证。

### 编译器架构与模块顺序

系统的完整处理流程（图 2）包含以下模块链路：

1. **DSL 前端解析**：将输入程序解析为 $e_d$ 语法树，识别所有 $H(\cdot)$ 节点及其依赖的 Dirac 参数。

2. **采样轴推断**：确定每个 $H(\cdot)$ 表达式对应的采样轴方向。对于着色器程序，采样轴通常是像素坐标或纹理坐标的某一维度。

3. **不连续点定位**：对于每个采样点对（采样点与其最近邻），求解 $c(x_d, \theta) = 0$ 以确定不连续边界位置 $x_d$。这一步利用了假设 A1——每对采样点之间至多一个根。

4. **梯度规则分发**：遍历语法树的反向传播路径，对 Dirac 参数应用预滤波梯度规则（规则 1/2），对非 Dirac 参数使用标准 AD 规则。

5. **邻域检测与核权重计算**：对于每个 Dirac 参数，检查当前采样点是否满足 $x - x_d \in [-\epsilon, \epsilon]$，若满足则梯度非零，否则梯度为零（规则 3）。

6. **多后端代码生成**：将计算出的梯度编译为目标语言（如 HLSL、GLSL 等着色器语言），输出可集成到现有渲染管线的梯度计算代码。

### 训练与推理路径

在优化场景中，系统的运行路径为：

- **前向传播**：正常执行着色器程序，输出渲染图像。
- **反向传播**：编译器生成的梯度代码计算每个参数对最终像素值的梯度。对于 Dirac 参数，梯度仅在采样点位于不连续边界邻域内时非零——这意味着**只有“见证”了边界移动的采样点才贡献梯度信号**。
- **参数更新**：使用标准梯度下降优化器（如 Adam）更新参数。

这一路径的关键特性是：**梯度计算的额外开销与不连续点的数量成正比，而与采样点总数无关**——因为只有邻域内的采样点触发非零梯度计算。在典型着色器优化任务中，不连续点数量远小于采样点总数，因此方法在实践中接近 $O(1)$ 的时间复杂度。

### Changed Slots：相对于传统 AD 的三个关键差异

1. **梯度定义域的改变**：传统 AD 在单点处求导，得到 Dirac delta（几乎处处为零）；本文方法在采样点邻域内求导，得到有限宽度的核函数值。这一改变将“点梯度”扩展为“区间梯度”，是方法有效性的根本来源。

2. **不连续性的显式建模**：传统 AD 将 $H(\cdot)$ 视为不可微的障碍；本文方法通过 DSL 设计将 $H(\cdot)$ 提升为一等公民，并为其配备专门的梯度规则。这一改变使编译器能够区分“可安全使用 AD 的连续部分”和“需要特殊处理的不连续部分”。

3. **采样轴概念的引入**：传统 AD 对所有变量一视同仁；本文方法区分采样轴变量 $\boldsymbol{x}$ 和参数变量 $\theta$，并沿采样轴方向进行预滤波。这一改变利用了渲染问题的空间结构——参数变化的影响沿空间方向传播，而非在所有维度上等同。

这三个 changed slots 形成因果链：**DSL 的显式不连续建模（slot 2）使编译器能够识别 Dirac 参数；采样轴的引入（slot 3）为预滤波提供了方向；区间梯度的定义（slot 1）最终产生了非零、有意义的优化信号**。

### 随机变量扩展：处理非 Dirac 参数的梯度消失

对于不直接依赖 $H(\cdot)$ 的参数（非 Dirac 参数），其梯度可能仍然很小或为零，因为不连续性可能通过长程依赖间接影响这些参数。为此，方法引入**随机变量**（random variables）机制：在每次前向传播中向采样坐标注入微小随机扰动，使得原本不在不连续边界邻域内的采样点有机会“触及”边界，从而为更多参数提供梯度信号。这一扩展在 Olympic Rings 任务中表现出显著效果——表 4 中“O/wo”（无随机变量）的中位时间明显长于完整方法。

![[assets/figures/papers/paper_list_l13_https_www_cs_princeton_edu_yutingy_docs_siggraph_2022_html_repair/figures/002_Figure_2.jpg]]
*Figure 2: Overview: green boxes indicate general components; red boxes are components specific to shaders; blue boxes indicate specific backend languages that our compiler outputs to (details in gray). Our compiler takes as input an arbitrary program in our DSL (§ 4.1), and approximates the gradient by pre-filtering a 1D box kernel along sampling axes (§ 4.2). Approximations along multiple sampling axes are later combined (§ 6.1). We verify that our gradients are accurate in two ways: we prove that a subset of programs are first-order correct (§ 5), and we also design a quantitative error metric (§ 7.3) to evaluate any gradient program empirically. For practical applications, our compiler outputs the...*

![[assets/figures/papers/paper_list_l13_https_www_cs_princeton_edu_yutingy_docs_siggraph_2022_html_repair/figures/004_Table_2.jpg]]
*Table 2: Gradient rules for our compiler and traditional*

![[assets/figures/papers/paper_list_l13_https_www_cs_princeton_edu_yutingy_docs_siggraph_2022_html_repair/figures/006_Figure_4.jpg]]
*Figure 4: Visualizing different options for how to combine multiple sampling axes in 2D. The green line demonstrates a discontinuity, and the blue region indicates evaluation locations where discontinuity can be sampled. Naively choosing either the ?? (a) or the ?? axis (b) can result in the discontinuity parallel to those axes being sampled at measure zero locations. For example, at the evaluation location indicated with a red square, each method places additional samples (orange squares) to sample discontinuities. Naively choosing the ?? axis (a) fails because the discontinuity is parallel to the kernel direction. Although naively choosing ?? axis (b) succeeds, it will fail if evaluated at the purp...*

## 实验与关键发现

### 核心性能对比：Olympic Rings 着色器优化

**Table 4** 报告了 Olympic Rings 着色器优化任务上各方法的中位成功时间。本文方法（Aδ）中位成功时间仅 **1.4 秒**，而两个基线方法 FD* 和 SPSA* 均为 **13.8 秒**，Aδ 实现了约 **9.9 倍**的加速。这一结果对应 **Figure 8(a)** 中的收敛曲线，直观展示了 Aδ 在着色器参数优化场景下的显著效率优势。

该任务的目标是自动调整着色器参数，使渲染结果逼近目标图像。着色器程序中包含大量由 `if` 分支、遮挡判断等引入的 discontinuity，传统自动微分（AD）无法处理这些不连续点，而有限差分（FD）和 SPSA 等零阶方法则因采样效率低下导致收敛缓慢。Aδ 通过引入基于 1D box kernel 的预滤波梯度近似，在保持梯度信息方向性优势的同时，避免了不连续点处梯度消失或爆炸的问题。

### 与可微矢量图形的系统性对比

**Figure 7** 展示了 Aδ 与可微矢量图形方法 DVG（Li et al., 2020）在两个优化任务上的 100 次随机重启收敛对比。横轴为挂钟时间（秒），纵轴为对数尺度的损失值。

关键发现：
- **收敛速度**：Aδ 在两项任务上均展现出更快的收敛速度，多数随机重启在 10 秒内即达到较低损失水平，而 DVG 的收敛曲线分散度更大，且中位收敛时间明显更长。
- **稳定性**：Aδ 的 100 条收敛曲线更为集中，表明方法对随机初始化的鲁棒性优于 DVG。DVG 在部分重启中出现收敛停滞或陷入较差的局部极小值。
- **最终质量**：**Figure 14** 展示了各任务中位误差对应的优化结果。Aδ 的优化结果在视觉上与目标图像高度一致，而 DVG 的结果在细节区域存在可辨识的偏差。

这一对比的意义在于：DVG 是专门为矢量图形渲染管线设计的可微框架，其梯度定义依赖于对渲染原语的解析边界处理；而 Aδ 采用通用的编译器方法，无需针对特定渲染原语定制梯度规则，却在效率和效果上均取得优势，验证了“通用 DSL + 近似梯度规则”路线的竞争力。

### 消融实验：随机变量的作用

**Table 4** 中同时报告了“O/wo”（ours without random variables）变体的结果。去除随机变量后，Olympic Rings 任务的中位成功时间从 1.4 秒上升（具体数值需查表确认），表明随机采样轴的引入对优化效率有实质贡献。

随机变量的核心作用在于：当采样轴方向固定时，某些 discontinuity 可能恰好与采样方向平行，导致 box kernel 无法有效捕获该不连续点的梯度信息。通过引入随机化的采样轴方向，Aδ 在每次前向传播中从不同角度“探测”不连续面，确保在期望意义上覆盖所有 discontinuity 的梯度贡献。这一消融直接验证了“随机采样轴”设计决策的有效性。

### 方法边界与失败模式

**Table 4** 中以符号“×”标注了方法从未在任何重启中成功的场景。具体失败案例及分析如下：

1. **FD* 和 SPSA* 的失败**：在部分高维参数空间任务中，零阶方法因采样效率随维度增长而急剧下降，导致在给定的时间预算内无法收敛。这与零阶方法的内在局限一致——每步只能获得标量函数值，信息量远低于梯度向量。

2. **Aδ 的理论假设边界**：方法建立在核心假设 **A1** 之上——“沿采样轴方向，每个采样点与其最近邻之间至多存在一个 discontinuity”。当场景违反此假设时（例如，在极小的空间区域内密集分布多个不连续面），box kernel 的预滤波近似将引入不可控的偏差。论文明确指出，这是方法适用性的关键边界条件。

3. **数值稳定性处理**：**Table 2** 的梯度规则中标注了实现层面的保护措施——函数组合规则中的除法操作被 safeguard 处理，以避免分母趋近于零时的数值不稳定。这表明方法在实际部署中需要额外的工程防护，理论上的简洁规则在边界情况下仍需经验性修正。

### 与相关工作的系统性定位

**Table 1** 从多个维度对比了 Aδ 与相关方法：

| 维度 | 传统 AD | 有限差分 | TEG | DVG/DPT | Aδ |
|------|---------|----------|-----|---------|-----|
| 处理 discontinuity | ✗ | ✓ | ✓ | ✓ | ✓ |
| 时间复杂度 | O(1) | O(N) | O(N) | O(1) | O(1) |
| 通用性 | DSL | 任意 | 特定 | 特定原语 | DSL |

Aδ 的独特定位在于：以 **O(1) 时间复杂度**实现了对 **DSL 内所有可表达程序**的 discontinuity 处理。传统 AD 虽为 O(1)，但无法处理不连续点；有限差分和 TEG 可处理不连续点，但时间复杂度随参数维度线性增长；DVG/DPT 为 O(1) 但仅限于特定渲染原语。Aδ 在通用性和效率之间找到了关键平衡点。

### 编译器调度空间的简化

**Table 3** 展示了 Aδ 编译器为着色器程序提供的 Halide 调度空间简化方案。这一设计决策的实践意义在于：着色器优化任务不仅需要有效的梯度，还需要高效的前向/反向计算。通过约束调度空间，编译器可以在不显著牺牲优化灵活性的前提下，生成高性能的 GPU 代码，确保端到端的优化效率。

![[assets/figures/papers/paper_list_l13_https_www_cs_princeton_edu_yutingy_docs_siggraph_2022_html_repair/figures/012_Table_4.jpg]]
*Table 4: Time metrics comparing how fast ours, ours without random variables (O/wo) and baselines converge, as discussed in Section 8.2. Symbol × indicates the method never succeeded in all restarts*

![[assets/figures/papers/paper_list_l13_https_www_cs_princeton_edu_yutingy_docs_siggraph_2022_html_repair/figures/003_Table_1.jpg]]
*Table 1: Comparison between ours and related work on differentiating discontinuous programs: traditional Auto-Differentiation (AD); finite difference (FD); TEG [Bangaru et al. 2021]; differentiable vector graphics [Li et al. 2020] and diffrentiable path tracers (DPT) [Bangaru et al. 2020; Li et al. 2018a; Loubet et al. 2019]. We compare these methods under four criteria: whether they can sample discontinuities, whether the method can reduce to AD in the absence of discontinuities, time complexity in terms of how many evaluations of the original program are needed as a function of parameter dimension ??, and what set of programs each method can handle. Our method handles every program expressible in...*

![[assets/figures/papers/paper_list_l13_https_www_cs_princeton_edu_yutingy_docs_siggraph_2022_html_repair/figures/007_Table_3.jpg]]
*Table 3: Our compiler provides a simplified Halide scheduling space for a program ?? . For an explanation of each choice refer to Section 7.1*

## 定位与知识库关联

本文的核心定位是：**为含间断的通用程序提供一套可微分的近似梯度规则，并将其实现在一个面向 shader 的编译器系统中**。与知识库中已有工作的本质差异体现在“如何处理间断”这一关键 slot 上。

### 改变的 slot：从“绕过间断”到“显式建模间断的预滤波梯度”

传统自动微分（AD）对间断点无能为力——Dirac δ 函数在工程上无法直接采样。已有工作对此的应对策略可分为几类：

- **有限差分（FD）与演化策略（SPSA）**：完全不依赖程序结构，通过零阶扰动估计梯度。其 slot 是“零阶黑箱查询”，代价是 O(n) 或更高采样复杂度，且在高维 shader 空间中收敛极慢。本文 Olympic Rings 任务上 FD* 和 SPSA* 的 Median Success Time 均为 13.8s，而本文方法仅 1.4s（~9.9× 加速），直接体现了这一 slot 差异的效率鸿沟。

- **TEG**（Bangaru et al., 2021）：通过积分重参数化将边界积分转化为面积分，本质上改变了“渲染积分的表示形式”这一 slot。TEG 要求程序能表达为边界积分的特定形式，限制了可处理程序的类别。本文方法不改变程序的表示形式，而是在微分规则层面引入间断处理，因此声称可处理 DSL 内所有程序（Table 1, Generality: DSL）。

- **可微矢量图形**（Li et al., 2020）：将矢量图元的光栅化过程可微化，其 slot 改变在于“渲染管线的特定环节”。该方法绑定于矢量图形领域，而本文的 DSL 和微分规则是领域无关的（shader 仅为应用特化）。

- **可微路径追踪器（DPT）**：在路径空间中进行微分，slot 改变在于“采样域的重参数化”。同样受限于特定渲染算法。

本文改变的 slot 可以概括为：**在反向模式 AD 的微分规则表中，将 Heaviside 阶跃函数 H(e) 的导数从无定义的 δ 函数替换为基于 1D box kernel 预滤波的近似梯度**。这个替换发生在编译器/AD 引擎的微分规则层面，而非程序表示或算法结构层面。其理论基础是：若假设沿采样轴每对相邻样本之间至多有一个间断（Assumption A1），则预滤波梯度退化为在间断位置评估 box kernel 的值，计算复杂度为 O(1)（Table 1），且不需要修改原始程序。

### 知识库挂载点

本文在知识库中的挂载点位于**可微编程与领域特定语言（DSL）编译**的交叉节点：

1. **可微编程谱系**：向上承接传统 AD（正向/反向模式），向下启发了后续对含间断程序微分的系统化研究。本文的“预滤波梯度”思想为处理非光滑程序的微分提供了除重参数化之外的另一种范式——在微分算子层面直接引入光滑化近似，而非改变程序语义。

2. **编译器架构谱系**：本文构建了一个完整的 DSL → 梯度 DSL → Halide/GLSL 的编译链（Figure 2），其中梯度规则以查表方式（Table 2）嵌入编译器。这种“微分规则作为编译器 pass”的架构设计，与后续可微编程框架（如 Enzyme、JAX 的自定义微分规则）共享设计哲学，但本文的特殊贡献在于显式处理了间断这一被多数框架回避的问题。

3. **渲染优化谱系**：在 shader 优化应用中，本文方法连接了“基于梯度的优化”与“shader 程序空间”。传统 shader 优化依赖人工调参或黑箱搜索，本文提供了一阶梯度信号，使 shader 参数优化可接入标准梯度下降器（如 Adam）。

### 适用边界

本文方法的能力边界由以下前提严格约束：

- **Assumption A1（单间断假设）**：沿采样轴的每对相邻样本之间至多存在一个间断。当程序违反此假设（如高频间断密度超过采样率），梯度估计会产生偏差。这是方法的核心理论边界，而非工程限制。

- **DSL 表达能力限制**：程序必须可表达为 $e_d ::= C \mid x \mid \theta \mid e_d + e_d \mid e_d \cdot e_d \mid H(e_d) \mid f(e_d)$ 的形式。这意味着循环、递归、动态内存分配等不在 DSL 范畴内。对于 shader 程序，这一限制通常可接受，但限制了向通用程序的直接迁移。

- **采样轴选择**：方法要求指定采样轴（sampling axis），在多维情况下需处理轴之间的交互（Figure 4 讨论了 2D 中组合多个采样轴的策略）。采样轴的选择直接影响梯度质量，但论文未提供自动选择机制。

- **box kernel 宽度 ε 的敏感性**：预滤波的 box kernel 宽度 ε 是一个关键超参数。过小则梯度稀疏（难以采样到间断），过大则梯度模糊。论文未系统讨论 ε 的自适应调整策略。

### 后续启发与知识库价值

本文对知识库的核心启发在于：

1. **“预滤波微分”范式**：将间断处理从程序表示层提升到微分算子层。这一思路可推广到其他非光滑构造（如 max、min、ReLU 的变体），只需设计对应的预滤波核和采样策略。后续工作可探索自适应核宽度、高阶核（如 Epanechnikov kernel）在精度-效率权衡中的表现。

2. **DSL 编译器与 AD 的深度集成**：本文展示了将微分规则作为编译器一等公民的设计。这种架构使得领域优化（如 Halide 调度，Table 3）可与梯度计算协同设计，为领域特定的可微编程框架提供了参考架构。

3. **shader 优化作为可微编程的测试床**：shader 程序天然包含大量间断（深度比较、条件分支、纹理边界），且优化目标（视觉相似度）难以手工定义梯度。本文证明了即使使用近似梯度，基于梯度的优化仍可在实际任务（Olympic Rings, Figure 8）上大幅超越零阶方法。这提示 shader 优化可作为评估可微编程方法的标准化 benchmark。

4. **需要手动验证的点**：论文声称方法可处理 DSL 内“所有程序”，但 Table 1 的“Generality: DSL”条目缺乏形式化完备性证明。Assumption A1 的违反条件及其对梯度偏差的定量影响也未在理论部分充分展开。这些边界条件在引用本文结论时需谨慎对待。

## 原文 PDF

![[paperPDFs/SIGGRAPH_2022/A_Autodiff_for_Discontinuous_Programs_Applied_to_Shaders.pdf]]