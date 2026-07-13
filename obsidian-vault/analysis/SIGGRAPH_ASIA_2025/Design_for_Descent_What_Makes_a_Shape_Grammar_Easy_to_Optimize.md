---
title: "Design for Descent: What Makes a Shape Grammar Easy to Optimize?"
type: paper
paper_level: A
venue: "SIGGRAPH Asia"
year: 2025
pdf_ref: paperPDFs/SIGGRAPH_ASIA_2025/Design_for_Descent_What_Makes_a_Shape_Grammar_Easy_to_Optimize.pdf
code_link: null
project_link: https://www.computationaldesign.group/publications/design-for-descent
aliases:
- SRDS
- DDWMSGEO
tags:
- SIGGRAPH_ASIA_2025
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
core_operator: "语法设计本身：通过设计满足可逆性、跳跃连续性、局部几何控制、可修复性等属性的重写规则，可使形状语法天然适合梯度下降优化。"
primary_logic: "反向视角：不设计复杂的搜索算法，而是设计语法本身，使其参数化空间具备类似神经网络过参数化的光滑性和冗余性，从而让简单的随机梯度下降高效解决形状程序逆问题。"
claims:
- "通过逐步添加可逆、跳跃连续、局部控制等语法设计原则，PSNR从15.4显著提升至22.6。"
- "SRD利用梯度信息同时更新离散结构和连续参数，相比传统MCMC方法（RJMCMC）收敛更快且结果更优。"
- "跳跃连续性（Jump Continuity）是确保优化平滑穿越离散结构变化的关键属性，缺失时性能大幅下降。"
- "OneComp (Tree Grammar) 上 PSNR (↑) = 22.0 (SRD Full)"
---

# Design for Descent: What Makes a Shape Grammar Easy to Optimize?

> [!tip] 核心洞察
> 反向视角：不设计复杂的搜索算法，而是设计语法本身，使其参数化空间具备类似神经网络过参数化的光滑性和冗余性，从而让简单的随机梯度下降高效解决形状程序逆问题。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 为梯度下降而设计：什么样的形状语法易于优化？ |
| 英文题名 | Design for Descent: What Makes a Shape Grammar Easy to Optimize? |
| 会议/期刊 | SIGGRAPH Asia 2025 |
| Links | [paper](https://www.computationaldesign.group/assets/papers/SIGA-2025-D4Descent.pdf) · [Project](https://www.computationaldesign.group/publications/design-for-descent) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction |
| Method | Stochastic Rewrite Descent (SRD) |
| Dataset | OneComp (Tree Grammar), Donut (Tree Grammar), TwoComp (Tree Grammar) |

> [!tip] 效果简介
> - OneComp (Tree Grammar) 上，PSNR (↑) 为 22.0 (SRD Full)，对比 15.3 (RJMCMC)，变化 +6.7。
> - Donut (Tree Grammar) 上，PSNR (↑) 为 21.1 (Tr-3, 引入Jump Continuity)，对比 9.7 (Tr-1, 仅AddLeaf)，变化 +11.4。
> - TwoComp (Tree Grammar) 上，PSNR (↑) 为 22.6 (Tr-F, 完整语法)，对比 10.3 (Tr-1)，变化 +12.3。

## 概要

形状语法是一种通过组合规则生成复杂结构的强大工具，在图形学与设计中广泛应用。然而，传统形状语法的逆问题求解——即寻找能产生目标形状的语法程序——长期依赖马尔可夫链蒙特卡罗（MCMC）或进化算法等无梯度方法，在庞大的离散-连续混合空间中效率低下，极易陷入局部最小值。

本文提出了一个根本性的视角转换：**不设计更复杂的搜索算法，而是设计语法本身，使其天然适合梯度下降优化**。核心洞察在于，借鉴深度神经网络中过参数化使优化景观更光滑的经验，通过赋予形状语法**可逆性、跳跃连续性、局部几何控制、可修复性**等关键属性，可以让简单的随机梯度下降高效地穿越离散结构变化，解决形状程序逆问题。

基于这一思想，本文提出了**随机重写下降（Stochastic Rewrite Descent, SRD）**算法，交替执行连续参数的梯度下降与离散结构的重写选择，利用梯度信息同时指导两个层面的优化。在树语法、矩形语法、弧线语法三种代表性语法上的实验表明：

- 逐步添加语法设计原则可使PSNR从约10.3提升至22.6（TwoComp数据集，Table 2），定性结果从混乱形状演化为高度还原的目标图像（Figure 8）。
- SRD在相同基础语法下相比经典方法**RJMCMC**（Talton et al., TOG 2011）收敛更快且结果更优（OneComp: 22.0 vs 15.3 PSNR, Table 3）。
- 跳跃连续性是确保优化平滑穿越离散结构变化的关键属性，缺失时性能大幅下降（Table 2: Tr-1 vs Tr-3）。

该方法不仅适用于图像拟合，还可扩展到基于文本提示的生成（Score Distillation Sampling）和拓扑优化等任务，展示了设计驱动优化的通用潜力。



形状语法（Shape Grammar）作为一种程序化建模工具，通过一组离散的重写规则和连续参数来定义形状的生成过程。其核心优势在于能够产生高度结构化的输出——例如由少量基元构成的简洁形状——并且天然携带可编辑的语义结构。然而，这种表达能力的代价是**逆问题（inverse problem）的极度困难**：给定目标图像或物理约束，反推出生成该形状的语法程序（包括离散的派生树结构和连续参数）是一个典型的混合离散-连续优化问题。

### 现有方法的根本困境

传统上，形状语法的逆过程求解主要依赖马尔可夫链蒙特卡洛（MCMC）方法，其中最具代表性的是 **RJMCMC**（Talton et al., TOG 2011）。这类方法通过在离散结构空间中进行随机游走来探索可能的派生树，本质上是一种无梯度的随机搜索。其根本缺陷在于：

1. **离散跳跃的盲目性**：RJMCMC 的每一步离散结构变更完全依赖随机提议，无法利用目标函数的梯度信息来判断移动方向，导致搜索效率极低。
2. **局部最小值的陷阱**：形状语法的离散结构空间高度非凸，缺乏梯度引导的随机游走极易陷入局部最小值——例如，一旦生成了错误数量的基元，RJMCMC 很难通过纯粹的随机扰动找到正确的拓扑结构。
3. **覆盖不充分**：如实验所示（Section 6.3, Fig. 3），RJMCMC 在某些情况下难以确保对目标形状的完整覆盖，尤其是在需要同时调整拓扑和几何的复杂场景中。

### 问题的根源：语法设计而非搜索算法

本文的核心洞察在于，上述困境的根源并非搜索算法不够精巧，而是**形状语法本身的设计从未考虑过梯度优化的需求**。传统的形状语法设计仅关注生成能力——即能否表达足够多样的形状——而完全忽视了优化过程的友好性。具体而言，传统语法缺乏以下关键属性：

- **可逆性（Invertibility）**：缺少与构造规则配对的破坏/简化规则，使得优化过程无法动态减少基元数量或简化结构。
- **跳跃连续性（Jump Continuity）**：当离散结构发生变更时（如增加一个节点），新旧形状之间缺乏平滑的几何过渡，导致梯度信号在结构跳变时完全断裂。
- **局部几何控制（Local Geometric Control）**：重写规则无法在不改变全局拓扑的前提下微调局部形状，迫使优化器在一次离散跳跃中同时处理拓扑和几何的大幅变化。
- **可修复性（Repairability）**：语法缺乏处理几何冲突（如自相交）的修复规则，使得许多中间状态因违反几何约束而无法被有效评估。

### 本文的动机：为梯度下降而设计语法

基于上述分析，本文提出一个**反向视角**：与其设计越来越复杂的混合离散-连续搜索算法，不如从根本上重新设计形状语法本身，使其参数化空间具备类似神经网络过参数化的光滑性和冗余性。核心思想是：通过精心设计重写规则，使离散结构空间中的每一步跳跃都伴随有意义的梯度下降路径，从而让简单的随机梯度下降（SGD）就能高效解决形状程序的逆问题。

这一动机催生了两个核心贡献：（1）一套系统化的**语法设计指南**（Table 1），明确了使形状语法易于梯度优化的具体属性；（2）**随机重写下降（Stochastic Rewrite Descent, SRD）** 算法，将离散重写采样与连续参数的梯度下降交替执行，利用梯度信息同时指导离散结构选择和连续参数更新。



## 核心方法与创新机理

本工作的核心创新在于**视角的翻转**：不从搜索算法入手，而是从**形状语法本身的设计**出发，使其天然适配梯度下降优化。传统方法（如 **RJMCMC**，Talton et al., TOG 2011）在固定的语法空间内进行随机游走或进化搜索，缺乏梯度引导，极易陷入局部最小值。本文提出：若语法设计得当，其参数化空间将具备类似神经网络过参数化的光滑性与冗余性，使简单的随机梯度下降即可高效求解形状程序逆问题。

### 关键创新点一：面向优化的语法设计原则

本文系统性地提出了一套**优化友好的语法设计指南**（Table 1），将语法重写规则从“仅能构造”改造为“适合下降”。核心原则包括：

- **可逆性（Reversibility）**：每个构造性规则必须有对应的反向操作（如 `Split ↔ Merge`、`AddLoop ↔ RemoveLoop`），使优化器能动态调节拓扑复杂度，而非单向增长。
- **跳跃连续性（Jump Continuity）**：重写操作对形状本身的改变应可忽略不计——例如 `Split` 将一条粗枝干分裂为两条紧贴的细枝干，视觉上几乎无变化，从而保证目标函数在离散跳跃处连续过渡（Section 3.2）。
- **局部几何控制（Local Geometric Control）**：语法应支持在形状任意位置进行局部修改而不影响远处区域，如 `AddAnywhere` 规则允许在任意节点插入新图元。
- **可修复性（Repairability）**：语法应包含约束修复规则（如 `Resolve-Intersections`），将非法或低质量形状拉回可行域，避免优化陷入死胡同。

这些原则共同作用，将离散结构空间“光滑化”，使梯度信息能有效引导离散重写决策。

### 关键创新点二：SRD——梯度引导的混合优化算法

基于上述语法设计，本文提出 **Stochastic Rewrite Descent (SRD)**，一种交替执行连续梯度下降与离散结构重写的混合优化策略：

1. **连续参数更新**：在当前离散结构 $s$ 下，使用 **Adam** 对连续参数 $p$ 执行梯度下降，最小化复合损失 $\mathcal{L}(s,p) = f(I(s,p)) + g(s,p)$（Equation 1）。
2. **离散重写选择**：从当前结构出发，随机采样一组候选重写 $\rho$。对每个候选重写，执行一步局部优化得到估计参数 $\hat{p}$，并计算损失改进量 $\Delta \mathcal{L}_{\rho} \approx \mathcal{L}(s,p) - \mathcal{L}(s', \hat{p})$（Section 3.3）。随后通过**贪心最大覆盖**在重写兼容性图上选择一组互不冲突的重写并并行应用。

这一策略的关键在于：**梯度信息同时服务于连续参数优化和离散重写的评估与选择**，使离散跳跃始终朝着损失下降的方向进行。消融实验（Table 3）证实，禁用连续参数步（NoStep）或仅选取单个最佳重写（OneRewrite）均显著降低性能。

### 相对于 Baseline 的 Changed Slots

| 维度 | 传统方法（RJMCMC 等） | 本文方法（SRD + 优化友好语法） |
|------|----------------------|-------------------------------|
| **语法重写规则** | 仅含构造性规则（如 `AddLeaf`），缺乏反向操作与局部修改能力 | 引入可逆配对规则、局部修改规则及约束修复规则，满足可逆性、跳跃连续性、局部控制与可修复性（Table 1, Figure 2） |
| **优化策略** | 随机游走或进化搜索，无梯度引导 | 交替执行连续参数 SGD 与梯度引导的离散重写选择（Algorithm 1） |
| **离散决策依据** | 基于随机接受准则（如 Metropolis-Hastings） | 基于梯度信息估计损失改进量 $\Delta \mathcal{L}_{\rho}$，贪心最大覆盖并行应用 |

### 决定性实验证据

语法设计原则的有效性通过逐步消融得到严格验证（Table 2, Figure 8）：
- 基础语法 Tr-1（仅含 `AddLeaf*`）在 OneComp 上 PSNR 仅为 15.4，TwoComp 上仅为 10.3。
- 引入可逆性（Tr-2）后性能显著提升。
- 加入跳跃连续性（Tr-3）是关键转折点：OneComp 提升至 21.5，Donut 提升至 21.1。
- 完整语法 Tr-F 在 TwoComp 上达到 22.6，相比 Tr-1 提升 **+12.3 PSNR**。

与 RJMCMC 的对比（Figure 3）显示：在相同基础语法下，RJMCMC 与 Tr-1 表现相当；而采用优化友好语法后，SRD 的 PSNR 从 15.3 跃升至 22.0（OneComp），充分证明**性能增益来自语法设计本身，而非搜索算法的复杂度提升**。



本文提出的核心框架并非设计新的搜索算法，而是**反向设计形状语法本身**，使其参数化空间天然适配梯度下降优化。基于这一思想，作者构建了一个交替优化管线，将离散结构探索与连续参数优化统一在梯度引导的框架下。

### 设计空间定义

形状语法定义了一个**混合离散-连续设计空间**。设 $S$ 为语法可生成的所有离散结构（如树拓扑、矩形布局）的集合，每个结构 $s \in S$ 拥有维度为 $d(s)$ 的连续参数空间（如位置、大小、旋转角）。整体设计空间是这些参数空间的**不交并**：

$$X = \bigsqcup_{s\in S} \{s\} \times \mathbb{R}^{d(s)}$$

优化目标是在该空间中寻找最优的离散-连续组合 $(s^*, p^*)$，最小化复合损失：

$$(s^{*}, p^{*}) = \arg\min_{s\in S, p\in \mathbb{R}^{d(s)}} f(I(s,p)) + g(s,p)$$

其中 $I(s,p)$ 为可微渲染函数，将形状程序渲染为图像或符号距离场（SDF）；$f$ 为与目标相关的可微损失（如 $L^2$ 距离）；$g$ 为不可微的正则项或约束项。

### 管线模块与数据流

SRD 优化管线由四个核心模块构成，交替执行连续参数更新与离散结构重写：

1. **形状语法引擎（Grammar Engine）**：维护当前形状程序的结构 $s$ 与参数 $p$，管理满足优化属性的重写规则库（详见 Table 1 设计指南）。这是整个管线的“结构记忆”。

2. **可微渲染模块（Differentiable Renderer）**：将当前形状程序渲染为可微表示。对于图像拟合任务，输出软光栅化图像；对于拓扑优化任务，输出 SDF。该模块为后续梯度计算提供通路。

3. **连续参数优化器（Adam）**：在当前离散结构 $s$ 固定不变的前提下，对连续参数 $p$ 执行梯度下降，最小化 $\mathcal{L}(s,p) = f(I(s,p)) + g(s,p)$。此步骤利用可微渲染器提供的梯度信息，使形状在连续参数空间内局部改善。

4. **离散重写选择器（Rewrite Selector）**：这是 SRD 的核心创新模块。在连续参数步之后，管线进入离散结构探索阶段：
   - **采样候选重写**：从当前结构 $s$ 出发，随机采样一组候选重写 $\rho$，每个重写将 $s$ 映射为新结构 $s'$。
   - **估计改进量**：对每个候选重写，将连续参数传递至新结构并执行一步局部优化 $\hat{p} = \mathrm{LocalOptimize}(s', p')$，估算损失下降量：
     $$\Delta \mathcal{L}_{\rho} \approx \mathcal{L}(s,p) - \mathcal{L}(s', \hat{p})$$
   - **贪心最大覆盖选择**：候选重写之间可能存在冲突（如修改同一子结构）。选择器在由重写兼容性隐式定义的图上执行贪心最大覆盖，选取一组互不冲突且改进量最大的重写，**并行应用**于当前结构。

上述交替过程持续迭代，直至收敛或达到预设步数。Figure 1 以树语法拟合 SIGGRAPH 标志为例，展示了连续参数调整与离散结构演化交替推进的完整流程。

### 语法设计原则的支撑作用

管线的高效运转依赖于语法本身满足四项关键设计原则（Table 1）：

- **可逆性（Reversibility）**：每条构造性规则需配对的逆规则（如 Split/Merge、Add/Remove-Loop），保证离散空间的可遍历性，避免陷入结构死胡同。
- **跳跃连续性（Jump Continuity）**：重写对形状本身的改变应可忽略，使得目标函数在离散跳转时近似连续变化。这是梯度信息能够有效指导离散选择的理论前提。
- **局部几何控制（Local Geometric Control）**：语法应支持在形状任意位置进行局部修改而不影响远端部分，使优化器能够精确修补局部误差。
- **可修复性（Repairability）**：语法需包含约束修复规则（如 Resolve-Intersections），在优化过程中动态修正非法结构，维持形状程序的物理有效性。

这些原则共同作用，使语法定义的离散-连续空间具备类似神经网络过参数化的光滑性和冗余性，从而让简单的随机梯度下降与贪心重写选择即可高效求解形状程序逆问题。消融实验（Table 2）证实，逐步添加这些设计原则使 PSNR 从 15.4 显著提升至 22.6，其中跳跃连续性的引入（Tr-3）带来了最大幅度的性能跃升。

### 补充图表

![[assets/figures/papers/paper_list_l33_https_www_computationaldesign_group_assets_papers_SIGA_2025_D4Descent_pd/figures/012_Figure_5.jpg]]
*Figure 5: Results of text-based optimization using Score Distillation Sampling (SDS) over grammars that (left) uses arcs and lines and (right) uses rectangles. The optimized shapes are coherent with the text prompts showing the versatility of our framework on different objectives. See Fig. 10 and 11 in the supplemental for additional results*



### 设计空间与优化目标

形状语法的设计空间由所有合法离散结构及其各自连续参数空间的并集构成。给定语法生成的结构集合 $S$，每个结构 $s \in S$ 拥有维度为 $d(s)$ 的连续参数向量 $p \in \mathbb{R}^{d(s)}$，整个设计空间可表示为：

$$X = \bigsqcup_{s \in S} \{s\} \times \mathbb{R}^{d(s)}$$

该定义（Section 3.1）将离散结构选择与连续参数优化统一在同一框架下。优化目标为寻找最优的离散-连续组合，使渲染图像与目标的损失及正则项之和最小：

$$(s^{*}, p^{*}) = \arg\min_{s \in S,\; p \in \mathbb{R}^{d(s)}} f(I(s, p)) + g(s, p)$$

其中 $I(s, p)$ 为可微渲染函数，将形状程序映射为图像或符号距离场；$f$ 为作用于渲染结果的可微目标函数（如 $L^2$ 距离）；$g$ 为可能不可微的正则项或约束项。这一复合损失 $\mathcal{L}(s, p) = f(I(s, p)) + g(s, p)$ 同时驱动离散结构搜索与连续参数优化。

### 语法设计指南

Table 1 总结了使形状语法适合梯度下降的四项核心设计指南，这些指南是 SRD 方法有效性的基础保证：

- **可逆性**：每条构造性规则需有对应的逆向规则（如 Split 与 Merge 配对），确保优化器可自由增减结构复杂度，避免陷入不可逆的局部极小值。
- **跳跃连续性**：重写操作对形状本身的改变应可忽略不计，从而使目标函数在离散跳转时近似连续变化。这是确保梯度信息可跨结构传递的关键属性。
- **局部几何控制**：语法应支持在形状任意位置进行局部修改而不影响远端区域，使优化器能独立修正局部误差。
- **可修复性**：语法需包含约束修复规则（如 Resolve-Intersections），在重写产生非法中间状态时将其拉回可行域。

Figure 2 展示了三种代表性语法（树语法、矩形语法、弧线语法）如何通过精心设计的重写规则满足上述指南。

### SRD 优化流程

SRD 算法交替执行两类操作，形成混合离散-连续优化循环：

**连续参数优化**：在固定当前离散结构 $s$ 的条件下，使用 Adam 优化器对连续参数 $p$ 执行梯度下降，最小化 $\mathcal{L}(s, p)$。此步骤为离散决策提供准确的梯度信号。

**离散重写选择**：从当前结构 $s$ 出发，随机采样一组候选重写规则。对每个候选重写 $\rho: s \to s'$，估算其带来的损失改进：

$$\Delta \mathcal{L}_{\rho} \approx \mathcal{L}(s, p) - \mathcal{L}(s', \hat{p}), \quad \hat{p} = \text{LocalOptimize}(s', p')$$

其中 $\hat{p}$ 是在新结构 $s'$ 下执行一步局部优化后得到的参数。该估计利用梯度信息评估离散跳转的价值，而非仅依赖随机试探。随后，SRD 在候选重写的兼容性图上执行贪心最大覆盖选择，并行应用一组互不冲突的重写，实现高效的离散结构更新。

### 模块架构

SRD 的完整 pipeline 由四个核心模块构成：

1. **形状语法引擎**：维护当前形状程序的结构与参数，管理重写规则库，确保所有重写满足设计指南。
2. **可微渲染模块**：将形状程序渲染为图像或符号距离场，计算目标函数并提供梯度，是连接离散结构与连续优化的桥梁。
3. **连续参数优化器（Adam）**：对当前离散结构下的连续参数执行梯度下降，最小化复合损失。
4. **离散重写选择器**：采样候选重写，基于梯度信息估算损失改进，通过贪心最大覆盖选择并行应用的重写集合。

这四个模块的协同使 SRD 能够同时利用梯度信息指导离散结构探索和连续参数精调，克服了传统 MCMC 方法（如 **RJMCMC**, Talton et al., TOG 2011）在离散空间中缺乏梯度引导的局限。



## 实验与关键发现

### 核心实验设置

论文在三个代表性形状语法上验证了SRD优化器与语法设计原则的有效性：**树语法**（Tree Grammar）、**矩形语法**（Rectangle Grammar）和**弧线语法**（Arc-Line Grammar）。每个语法均按照Table 1的设计指南（可逆性、跳跃连续性、局部几何控制、可修复性）进行工程化改造。评估任务包括图像拟合（目标为二值位图）、文本驱动生成（SDS）和拓扑优化，主要指标为PSNR。

与基线方法**RJMCMC**（Talton et al., TOG 2011）的对比在公平条件下进行：两者使用相同的基础语法（仅含AddLeaf*规则），排除了语法差异的干扰。所有实验采用统一的可微渲染器，Adam优化器的学习率等超参数保持一致。

### 主实验结果

SRD在所有三个数据集上均显著优于RJMCMC基线。在OneComp数据集上，SRD Full达到PSNR 22.0，而RJMCMC仅为15.3（Table 3, Fig. 3），增益达+6.7 dB。RJMCMC偶尔难以确保对目标区域的完整覆盖，而SRD利用梯度引导加速了收敛并产生更优的形状匹配。

![[assets/figures/papers/paper_list_l33_https_www_computationaldesign_group_assets_papers_SIGA_2025_D4Descent_pd/figures/005_Table_3.jpg]]
*Table 3: Optimization quality (PSNR) and time (s) using different variations of SRD evaluated over OneComp (One), Donut (Dnt.), and TwoComp (Two) datasets*

三种语法在图像拟合任务上均能可靠收敛（Fig. 4）。树语法通过插入、分裂和收缩分支来有机地覆盖目标轮廓；矩形语法通过分裂、合并和局部添加矩形来逼近目标形状；弧线语法则利用弧线和直线的连接操作生成平滑的边界。在文本驱动的SDS优化中（Fig. 5），弧线语法和矩形语法均能根据文本提示生成语义合理的形状程序。

### 语法设计消融：从Tr-1到Tr-F

Table 2系统性地展示了逐步添加设计原则对优化质量的因果影响（Fig. 8提供定性可视化）：

- **Tr-1（仅AddLeaf*，无可逆规则）**：性能最低，OneComp PSNR仅15.4，Donut 9.7，TwoComp 10.3。优化器缺乏删除或修改已添加基元的能力，极易陷入局部最小值，无法填充目标区域（如TwoComp的右下区域缺失）。
- **Tr-2（添加可逆配对规则Split/Merge）**：引入结构修改能力，PSNR显著提升。这表明可逆性是梯度优化在离散空间中有效探索的基础前提。
- **Tr-3（添加跳跃连续性规则AddAnywhere）**：这是最关键的单步改进。Donut数据集PSNR从Tr-2的较低水平跃升至21.1，OneComp达21.5。跳跃连续性确保离散结构变化（如添加新分支）不会导致形状突变，使优化器能平滑穿越离散决策边界。
- **Tr-F（完整语法，包含Resolve-Intersections修复规则）**：达到最优性能，TwoComp PSNR从Tr-1的10.3提升至22.6（+12.3 dB），同时基元数量更少，体现了可修复性对维持形状有效性的价值。

### SRD组件消融

Table 3展示了SRD优化器自身组件的消融结果：

- **NoStep（禁用连续参数更新）**：性能大幅下降，证实连续梯度步（Adam对参数的优化）对于有效评估候选重写和引导离散搜索必不可少。没有连续优化，重写选择缺乏可靠的改进估计。
- **OneRewrite（每步仅选单个最佳重写）**：相比Full SRD的并行多重重写，收敛速度更慢且最终质量更低。并行应用互不冲突的重写（通过贪心最大覆盖选择）显著加速了结构探索。
- **Full SRD**：交替执行连续SGD与离散重写的并行选择，在所有数据集上达到最佳PSNR-时间权衡。

### 应用扩展与鲁棒性

在拓扑优化任务中（Fig. 7），弧线语法程序成功优化了Cantilever和MBB梁问题。可微渲染器生成的符号距离场可直接应用水平集方法进行结构优化，验证了语法的跨任务泛化能力。

Fig. 6展示了SRD在动态变形序列中的鲁棒性：当目标图像连续变化时，由于可逆、跳跃连续和局部可控的重写规则，优化器能平滑地将优化延续至新目标，无需重新初始化。

### 失败模式与局限

尽管SRD取得了显著改进，仍存在若干局限：

1. **优化器状态传递问题**：离散重写后，Adam的动量等优化器状态如何有效传递至新结构尚未解决，可能导致信息丢失和收敛波动。
2. **重写采样策略**：当前重写采样分布是随机的，未根据形状状态和梯度信息动态调整，可能影响收敛效率。
3. **语法设计门槛**：所有语法均依赖人工工程化以满足设计指南，尚未实现从数据中自动推断优化友好规则。
4. **离散操作的连续松弛**：某些离散操作可能无法找到合适的连续松弛，限制了SRD在更广泛离散结构空间的直接应用。

### 补充图表

![[assets/figures/papers/paper_list_l33_https_www_computationaldesign_group_assets_papers_SIGA_2025_D4Descent_pd/figures/007_Figure.jpg]]

![[assets/figures/papers/paper_list_l33_https_www_computationaldesign_group_assets_papers_SIGA_2025_D4Descent_pd/figures/008_Figure.jpg]]

![[assets/figures/papers/paper_list_l33_https_www_computationaldesign_group_assets_papers_SIGA_2025_D4Descent_pd/figures/009_Figure.jpg]]

![[assets/figures/papers/paper_list_l33_https_www_computationaldesign_group_assets_papers_SIGA_2025_D4Descent_pd/figures/010_Figure.jpg]]

![[assets/figures/papers/paper_list_l33_https_www_computationaldesign_group_assets_papers_SIGA_2025_D4Descent_pd/figures/014_Figure.jpg]]

![[assets/figures/papers/paper_list_l33_https_www_computationaldesign_group_assets_papers_SIGA_2025_D4Descent_pd/figures/002_Table_1.jpg]]
*Table 1: The suggested guidelines for designing grammars for descent. Section 3.2 systematical considers desirable properties, condensed here to a set of concrete recommendations. These are intended to be guidelines rather than hard requirements: they need not be strictly satisfied by all rewrites, it may even be contradictory to attempt to satisfy them all simultaneously for a given task. In Section 6 we experimentally validate the effect of these rules improving the efficacy of inverse optimization in several settings*

![[assets/figures/papers/paper_list_l33_https_www_computationaldesign_group_assets_papers_SIGA_2025_D4Descent_pd/figures/004_Table_2.jpg]]
*Table 2: Optimization quality (PSNR) and simplicity (number of primitives) using different grammar variations evaluated over OneComp (One), Donut (Dnt.), and TwoComp (Two) datasets*



## 定位与知识库关联

### 1. 与基线方法的关系

**SRD 相对于传统形状语法求解器的范式转移。** 传统形状语法逆过程求解器，如 **RJMCMC** (Talton et al., TOG 2011)，通过随机游走在离散生产规则空间中探索候选结构，缺乏梯度信息的引导。SRD 的核心突破在于将优化视角从“设计更聪明的搜索算法”转向“设计更易于优化的语法本身”。通过引入可逆性、跳跃连续性、局部几何控制和可修复性等语法设计原则，SRD 使得简单的随机梯度下降（SGD）即可高效求解形状程序的逆问题——这与神经网络中过参数化使得非凸优化更容易的洞察一脉相承。

**公平比较的基准设定。** 在 Figure 3 和 Table 3 的对比中，RJMCMC 与 Tr-1 变体使用相同的受限语法（仅含 `AddLeaf*` 规则），两者产生可比的结果（PSNR 约 15.3–15.4），排除了语法差异的干扰。然而，当 SRD 使用按设计指南逐步丰富的语法（Tr-2 至 Tr-F）时，PSNR 显著提升至 22.0–22.6，而 RJMCMC 受限于其无梯度的随机游走机制，无法同等利用这些新增规则。这验证了核心主张：语法设计本身是因果杠杆，而非优化算法的复杂度。

### 2. 方法适用边界

**适用场景。** SRD 在以下条件下表现最佳：
- 形状语法可以工程化为满足 Table 1 所列设计指南（可逆重写、跳跃连续、局部控制、可修复性）。
- 目标函数可通过可微渲染器（如本文使用的可微距离场渲染器）提供可靠的连续参数梯度。
- 离散结构变化的“粒度”适中——重写规则每次改变的结构范围足够局部，使得跳跃连续性得以保持。

**不适用或需谨慎的场景。**
- **缺乏连续松弛的离散操作。** 文中明确指出，某些离散操作可能无法找到合适的连续松弛（见 limitations），这限制了 SRD 在完全离散空间中的直接应用。
- **状态优化器信息丢失。** 当前 SRD 在应用离散重写后，优化器状态（如 Adam 的动量项）无法跨结构传递，可能导致优化轨迹的震荡或信息浪费。对于需要长期动量累积的深度优化场景，这一限制尤为显著。
- **高维离散重写空间。** 当候选重写数量爆炸时，随机采样加贪心最大覆盖的选择策略可能遗漏关键的结构变化路径，需要更智能的采样分布。

### 3. 局限与开放问题

**已确认的局限（来自论文本身）。**
1. **优化器状态传递未解决。** 动量等历史信息在重写后如何映射到新结构空间，是混合优化中长期存在的难题，SRD 目前直接丢弃这些状态。
2. **重写采样分布为静态随机。** 当前采样不根据形状状态或梯度信息动态调整，可能反复尝试无效重写，影响收敛效率。
3. **语法设计依赖人工工程。** 为每种新形状语法手工设计满足优化属性的重写规则需要领域专家深度参与，限制了方法的可扩展性。
4. **连续松弛的可用性限制。** 某些离散操作（如三维布尔运算中的拓扑改变）可能难以找到保持梯度流的连续松弛。

**开放研究问题。**
- **自动化语法设计：** 能否从数据中自动推断出满足可逆性、跳跃连续性等属性的重写规则？这类似于自动发现神经架构搜索中的有效操作原语，但需要同时保证离散变化的光滑性。
- **状态跨结构迁移：** 如何将动量等优化器状态适配到跨离散重写的混合优化过程中？可能的思路包括在重写前后结构的共享子空间上投影状态向量。
- **完全可微的离散操作：** 某些离散操作能否通过连续松弛（如 Gumbel-Softmax 或 straight-through estimator 的结构化扩展）实现完全可微，从而消除混合优化的离散跳跃？
- **三维扩展：** 如何为三维布尔运算、CSG 树等更复杂的形状语法设计优化友好规则？这涉及三维空间中跳跃连续性的定义和局部几何控制的实现。
- **重写采样的学习策略：** 能否训练一个策略网络，根据当前形状状态和梯度信息动态选择最有前景的重写规则，替代当前的随机采样？

### 4. 在知识库中的定位

SRD 处于三个研究方向的交叉点上：

| 研究方向 | SRD 的贡献定位 | 代表性相关工作 |
|---------|--------------|-------------|
| **程序化建模与逆过程** | 首次系统化地提出“为优化而设计语法”的范式，将语法设计从表达力导向转向优化友好导向 | RJMCMC (Talton et al., TOG 2011)；ShapeAssembly 等程序化建模框架 |
| **可微渲染与逆向图形学** | 利用可微渲染器提供的梯度信号同时指导离散结构和连续参数的更新，区别于仅优化连续参数的传统逆向图形学方法 | 可微光栅化器、NeRF 等隐式表示优化 |
| **混合离散-连续优化** | 提出交替执行连续梯度步和离散重写步的实用框架，通过贪心最大覆盖实现并行重写选择 | 神经网络架构搜索（NAS）中的混合优化；贝叶斯优化中的混合变量处理 |

SRD 的核心知识贡献不在于提出新的优化算法理论，而在于揭示了一个被忽视的设计维度：**语法空间的结构属性决定了梯度优化的可行性**。这一洞察将“过参数化使优化更容易”的深度学习经验迁移到了程序化建模领域，为后续研究开辟了“优化驱动语法设计”的新方向。



## 原文 PDF

![[paperPDFs/SIGGRAPH_ASIA_2025/Design_for_Descent_What_Makes_a_Shape_Grammar_Easy_to_Optimize.pdf]]
