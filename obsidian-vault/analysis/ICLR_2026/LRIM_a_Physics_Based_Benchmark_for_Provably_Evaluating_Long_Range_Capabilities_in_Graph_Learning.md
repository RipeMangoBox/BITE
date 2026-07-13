---
title: "LRIM: a Physics-Based Benchmark for Provably Evaluating Long-Range Capabilities in Graph Learning"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/LRIM_a_Physics_Based_Benchmark_for_Provably_Evaluating_Long_Range_Capabilities_in_Graph_Learning.pdf
project_link: null
code_link: null
aliases:
- LGBLRIMGB
- LRIM
tags:
- ICLR_2026
- topic/generative_models_diffusion
- topic/generative_models_diffusion/graph_neural_networks
core_operator: "模型计算复杂度与有效感受野之间的权衡，具体表现为模型深度、注意力机制的全局性以及计算预算。"
primary_logic: "采用具有幂律衰减相互作用的伊辛模型构建可证明且可控的长程依赖任务。在伪临界温度下采样确保系统具有长程空间相关性；神谕预测器仅在局部邻域内计算能量变化，其误差随邻域半径扩大而平滑衰减，定量证明任务依赖远距离信息，并为评估长程能力提供连续的反馈信号。"
claims:
- "神谕预测器的LogMSE误差随邻域半径r扩大而平滑下降，且更小的σ值需要更大的邻域才能达到相同精度，证明任务对长程信息存在依赖。"
- "引理5.1证明任何仅使用局部邻域的模型在最坏情况下的误差至少为n^{-σ}，为长程信息必要性提供了理论下界。"
- "命题5.2和5.3给出了长程度量ρ_i(ΔE)的解析表达式，并证明当σ≤1时该度量发散，验证了长程依赖的可控性。"
- "基于1-WL等价类的分析表明，虽然MPNN在有限数据下可以过拟合训练集，但良好的泛化需要接近神谕的感受野，说明局部信息不足以泛化到全局任务。"
---

# LRIM: a Physics-Based Benchmark for Provably Evaluating Long-Range Capabilities in Graph Learning

> [!tip] 核心洞察
> 采用具有幂律衰减相互作用的伊辛模型构建可证明且可控的长程依赖任务。在伪临界温度下采样确保系统具有长程空间相关性；神谕预测器仅在局部邻域内计算能量变化，其误差随邻域半径扩大而平滑衰减，定量证明任务依赖远距离信息，并为评估长程能力提供连续的反馈信号。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | LRIM：基于物理的可证明长程图学习能力评估基准 |
| 英文题名 | LRIM: a Physics-Based Benchmark for Provably Evaluating Long-Range Capabilities in Graph Learning |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=IAZXEX1dVV) |
| Topic | #topic/generative_models_diffusion #topic/generative_models_diffusion/graph_neural_networks |
| Method | LRIM Graph Benchmark (Long-Range Ising Model Graph Benchmark) |
| Dataset | LRIM-16-hard, LRIM-32-hard, LRIM-16-easy, LRIM-32-easy |

> [!tip] 效果简介
> - LRIM-16-hard 上，LogMSE (↓) 为 Oracle (r=∞)，对比 GPS-LapPE，变化 >5.666。
> - LRIM-32-hard 上，LogMSE (↓) 为 Oracle (r=∞)，对比 GPS-RWSE，变化 >5.866。
> - LRIM-16-easy 上，LogMSE (↓) 为 Oracle (r=∞)，对比 GPS-Base，变化 >4.704。

## 概要

图学习面临的核心瓶颈是：在可扩展的复杂度内捕获超越局部邻域的长程依赖关系。消息传递神经网络（MPNN）通过堆叠层数扩大感受野，但带来指数级的计算开销；图变换器通过全局注意力直接建模任意节点间的交互，却面临 $\mathcal{O}(N^2)$ 的复杂度，难以扩展到大规模图。这一 **计算复杂度‑感受野权衡** 构成当前长程图学习研究的核心因果旋钮。

针对上述挑战，该工作提出 **LRIM（Long‑Range Ising Model）图基准**——一个基于物理的、可证明且可控的长程能力评估平台。该基准利用具有幂律衰减相互作用 $J_{ij} = 1/r_{ij}^{d+\sigma}$ 的伊辛模型，在伪临界温度下采样生成具有强长程空间相关性的自旋构型，并由此构建节点回归任务：预测每个节点的能量变化 $\Delta E_i$。通过调节相互作用衰减指数 $\sigma$ 和系统尺寸 $L$，可以 **连续且可证明地控制任务的远程依赖程度**。神谕预测器（oracle）仅依赖真实能量函数，其误差随所考虑的邻域半径 $r$ 平滑衰减，且更小的 $\sigma$ 需要更大的 $r$ 才能达到相同精度（图2）；引理 5.1 从理论上给出了任何仅使用局部邻域模型在最坏情况下误差至少为 $n^{-\sigma}$ 的下界，确证了 **长程信息对任务完成的必要性**。此外，基于梯度的长程度量 $\hat{\rho}_i(\Delta E)$ 的解析表达式表明，当 $\sigma \leq 1$ 时该度量随系统尺寸发散，进一步验证了依赖关系的可控性与无限长程行为的存在（命题 5.2 与 5.3，图3）。

在 LRIM 基准上对多种主流模型（GIN、GatedGCN、GPS 系列、CNN、ViT）的测试揭示出以下主要结果：
- **现有方法与理想目标的巨大鸿沟**：最佳图变换器（如 GPS‑LapPE、GPS‑RWSE）在 LRIM‑16/32 上的 LogMSE 仍与使用全图信息的神谕预测器相差 5–6 个数量级以上（表2），且所有模型在层数增至 10–16 层后性能趋于平台，无法通过单纯加深网络逼近神谕（图4）。
- **可扩展性与长程建模的尖锐矛盾**：MPNN 虽能在大图上维持 $\mathcal{O}(L·E)$ 复杂度，但其局部感受野限制了长程捕获；GPS 等全局注意力模型虽在中小规模表现更优，却在 LRIM‑256 上遭遇显存溢出（OOM），暴露了 $\mathcal{O}(N^2)$ 复杂度的根本瓶颈（表3）。
- **长程依赖的连续反馈与可控评估**：神谕预测器的平滑性能退化（图2/5）及范围度量的解析增长（图3/19）共同为模型训练与评估提供了 **连续的、可定量的反馈信号**，克服了传统基准中“二值”或有限离散反馈的不足。
- **泛化与迁移的挑战**：模型从 16×16 系统向更大系统的零样本迁移中性能显著退化，说明在有限数据下习得的局部/全局策略难以泛化至不同尺寸和长程强度的物理系统（表3）；基于 1‑WL 等价类的分析表明，虽然 MPNN 在有限数据下可过拟合训练集，但良好的泛化要求感受野接近神谕水平，凸显了真实长程建模的难度（图12）。

LRIM 基准通过可证明的长程依赖、精细可控的任务难度以及连续的评估信号，为长程图学习模型的研发与对比提供了一个严格且物理驱动的测试平台，并强调性能与计算复杂度的联合报告。



图学习的一个核心瓶颈在于如何可扩展地捕获超越局部邻域的长程依赖关系。主流范式提供两种极端方案，但各自存在固有局限：消息传递神经网络（MPNN）依靠堆叠多个层来逐步扩展感受野，但要覆盖整个图所需的层数随图尺寸指数增长，这极易引发过度平滑、优化困难以及计算开销不可承受的问题；图变换器则通过全局注意力机制直接聚合任意节点对的信息，理论上能够绕过局部限制，但其 $O(N^2)$ 的复杂度严重限制了在大规模图上的应用。因此，当前图模型始终面临“有效感受野与计算成本”之间的根本权衡。

评估长程建模能力的现有基准进一步加剧了这一困境。以 LRGB（Long-Range Graph Benchmark）为代表的主流评估套件通常基于真实世界图数据，虽然此类数据天然包含长程结构，但无法从数学上证明其任务标签必然依赖远距离节点信息——很多真实图可能通过局部捷径即可解决任务（例如利用同配性或低阶结构），导致基准难以可靠区分模型是否真正学习了长程交互。另外，多数基准提供二值或粗粒度的离散反馈（如分类正确/错误），缺乏连续、细粒度的信号来精密诊断模型在长程信息利用上的阶梯式改善。这种反馈的模糊性使得研究者很难判断模型性能提升是来自真正捕获了长程依赖，还是仅仅在局部近似上做得更好（如过拟合训练集中的偶然模式）。

为弥补这些缺口，本文引入 LRIM Graph Benchmark，旨在提供一个**可证明依赖长程信息**、**长程程度可精确控制**、并**提供连续反馈信号**的图学习评估平台。其核心思想源自统计物理中的长程伊辛模型：在二维周期网格图上定义具有幂律衰减相互作用 $J_{ij} = 1 / r_{ij}^{d+\sigma}$ 的哈密顿量，并通过在伪临界温度下的马尔可夫链蒙特卡洛采样生成自旋构型，从而确保系统中存在强大的长程空间相关性。节点回归任务要求预测单个自旋翻转所引起的能量变化 $\Delta E_i$；由于 $\Delta E_i$ 的表达式中显式包含与所有其他自旋的耦合，该任务在物理上必然依赖远距离节点。基准通过可调参数 $\sigma$ 控制系统长程依赖的强弱（$\sigma$ 越小，长程效应越显著），并借助“神谕预测器”（Oracle）为任务提供模型无关的长程必要性证据：该预测器使用真实的能量函数，但仅考虑目标的 $r$-hop 局部邻域，其误差随 $r$ 扩大而平滑下降（Figure 2），且更小的 $\sigma$ 需要更大的 $r$ 才能达到相同精度，定量证实了任务对长程信息的硬性需求。理论引理（Lemma 5.1）进一步证明，任何仅利用局部邻域的模型在最坏情况下的误差至少为 $n^{-\sigma}$，为长程信息的必要性提供了严格下界。与此同时，神谕预测器给出的 LogMSE 表现为连续曲线，使得评估不再是“及格/不及格”的二元判断，而是能够精细反映模型在不同距离依赖层级上的能力进化。

综上，LRIM 基准通过将长程依赖从“隐含猜测”转为“可控可证”的物理任务，为图学习社区提供了一套兼具理论保证与工程灵活性的测试基准，旨在催化可扩展、能真正捕获长程交互的新型图学习方法。



## 核心方法与创新机理

相对于现有长程图学习基准（如 LRGB），LRIM 的核心贡献在于解决了三个相互关联的根本缺陷：任务长程依赖的不可证明性、难度控制的缺失，以及反馈信号的二值化。这些缺陷导致我们无法系统性地区分模型是否真正捕获了长程信息，还是仅依赖局部统计量过拟合。LRIM 通过引入一套完整的物理驱动生成框架和配套分析工具，将长程能力评估从经验性推断提升为可控、可证明的因果分析。

**可证明的长程必要性。**  
多数基准以真实世界数据为基础，虽然任务直观上需长程依赖，但无法严格证明模型必须使用远距离节点信息。LRIM 设计了一个“神谕预测器”，该预测器使用真实伊辛能量函数，但可将输入限制在目标节点的 $r$‑跳邻域内。通过变化 $r$，神谕的 LogMSE 误差平滑下降（**Figure 2**），且更小的相互作用参数 $\sigma$ 需要更大的感受野才能达到相同精度。更重要的是，**Lemma 5.1** 提供了理论下界：任何仅使用局部邻域的模型，在最坏情况下的预测误差至少为 $n^{-\sigma}$。这为“长程信息不可或缺”提供了模型无关的严格证据，而非依赖直觉。

**精细可控的长程程度。**  
现有基准无法调节长程依赖性，难以评估模型在不同难度下的表现。LRIM 通过幂律衰减的相互作用哈密顿量（$J_{ij}=1/r_{ij}^{d+\sigma}$）引入连续参数 $\sigma$，直接控制自旋间相互作用的衰减速率。结合系统尺寸 $L$，形成了一套二维难度网格：10 个数据集覆盖 5 种尺寸 × 2 种难度（easy $\sigma=1.5$, hard $\sigma=0.6$）。**Proposition 5.2** 给出了神谕预测器的长程度量 $\hat{\rho}_i(\Delta E)$ 的解析解，证明当 $\sigma \le 1$ 时该度量发散，即依赖无限远。**Figure 3** 的实验量化了长程依赖随 $L$ 增大和 $\sigma$ 减小的增长，且 $\sigma \le 1$ 时增长加速。这种可控性使基准可诊断模型在不同长程度下的能力边界，而不仅仅是给出“是否够好”的二元判断。

**连续反馈信号。**  
传统任务（如分类）通常提供离散或单点反馈，难以诊断模型是逐步改进还是陷入局部极值。LRIM 的节点回归任务使用对数均方误差（LogMSE）指标，神谕预测器和所有模型都产生连续的误差曲线。如 **Figure 2** 所示，神谕误差随 $r$ 增大而平滑衰减，没有任何阶跃；模型训练过程中的性能变化也是连续的。这种连续反馈使得不同方法的长程捕获效率可以被精细比较，并有助于设计自适应或分阶段训练策略。

**强调计算可扩展性。**  
图学习领域长期存在性能与计算复杂度的权衡：全局注意力（如 GPS）可捕获长程信息但面临 $O(N^2)$ 成本，而 MPNN 的 $O(L \cdot E)$ 成本限制了其感受野。LRIM 在评估中强制要求报告每个模型的计算复杂度（预处理和推理），并在结果表中与性能并列（**Table 2, Table 3**）。例如，**Table 3** 显示 GPS 变体在迁移到 LRIM‑256 时直接出现内存溢出（OOM），而 MPNN 虽可运行但性能远低于神谕。这种并置揭示了当前方法在可扩展捕获长程信息上的本质瓶颈，而非仅仅在精度上竞争，引导社区关注效率与感受野的帕累托最优设计。

**物理驱动的数据生成。**  
通过伊辛模型的伪临界温度采样，LRIM 确保了数据中自旋的最大空间相关性，这是任务包含长程依赖的物理基础。采样使用结合 Metropolis 和 Alias‑Walker 的 Monte Carlo 算法，生成 10 000 个构型的训练集。与以往使用随机连接或统计无关的合成图不同，LRIM 的图拓扑和交互自然地从物理系统中涌现，使得长程依赖不是人工注入，而是真实物理规律的结果。该生成机制保证了评估的可解释性：模型表现的差距直接反映其捕获物理长程交互的能力，而非数据分布的人为偏差。

综上，通过上述改变槽的替换——将不可证明依赖替换为可证明、将不可控难度替换为参数可调、将离散反馈替换为连续——LRIM 为长程图学习提供了一个诊断性评估平台，使得瓶颈不再是“模型好不好”，而是“模型在何种条件下、以何种计算代价，能够捕获必要程度的长程依赖”。



![[assets/figures/papers/iclr26_0015_IAZXEX1dVV_LRIM_a_Physics-Based_Benchmark_for_Provably_Eval/figures/002_Table_1.jpg]]
*Table 1: Overview of all 10 datasets in the LRIM Graph Benchmark. Our benchmark can systematically vary the complexity across 5 graph sizes (256 to 65,536 nodes) and 2 difficulty levels per size controlled by the interaction parameter σ. Each dataset contains 10,000 spin configurations represented as 2D periodic grid graphs with 4-regular connectivity. The proposed task considers node-level regression to predict energy changes $\Delta \bar { E } _ { i }$ , with performance measured using log10 MSE

![[assets/figures/papers/iclr26_0015_IAZXEX1dVV_LRIM_a_Physics-Based_Benchmark_for_Provably_Eval/figures/003_Figure_2.jpg]]
*Figure 2: LogMSE ( ) performance of the oracle predictor degrades when restricted to consider local r-hop neighborhoods only. The oracle uses the true underlying energy function, but only considers spins within hop-distance r from each target node. Results demonstrate that smaller σ values (harder tasks) require larger neighborhoods to achieve the same accuracy, confirming stronger longrange dependencies. Second, larger system sizes increase task difficulty, even within the same σ. Moreover, the performance decays smoothly, providing a continuous feedback both during evaluation and training. Therefore, achieving low prediction error requires information from neighborhoods spanning significant fractio...*

![[assets/figures/papers/iclr26_0015_IAZXEX1dVV_LRIM_a_Physics-Based_Benchmark_for_Provably_Eval/figures/004_Figure_3.jpg]]
*Figure 3: Normalized range measure $\hat { \rho } _ { i } ( \Delta$ E ) increases with system size L and decreases with $\sigma$ . . The measure quantifies the relative contribution of distant nodes to the energy prediction task, computed analytically using the oracle’s gradient. Smaller σ values lead to higher measures across all system sizes, with the growth rate accelerating for $\sigma \leq$ 1 . This validates both the dependence and controllability of long-range dependencies throughout our proposed benchmark

LRIM（Long-Range Ising Model）图基准的核心思路是：**将物理上长程相关的自旋构型映射为图上的节点回归任务，利用可调的幂律相互作用参数 $$\sigma$$ 与系统尺寸 $$L$$ 连续控制任务的长程依赖程度，并通过神谕预测器提供可证明的长程必要性证据**。整体管道包括五个紧密耦合的模块：物理模型定义 → 临界采样与构型生成 → 图表示构造 → 能量变化预测 → 可证明长程评估。各模块的输入输出流与关系如图 1 所示，贯穿始终的是**计算复杂度与实际感受野之间的权衡**这一瓶颈：消息传递模型因感受野扩展带来指数级计算开销，而全局注意力则面临 $$O(N^2)$$ 的可扩展性压力。

### 1. 长程伊辛模型与可控长程机制

基准的物理基础是带有幂律耦合的长程伊辛模型，其哈密顿量定义为：

$$\mathcal{H}(\{s_i\}) = -\frac{1}{2} \sum_{ij \in G} J_{ij} s_i s_j, \quad J_{ij} = \frac{1}{r_{ij}^{d+\sigma}}$$

其中 $$s_i\in\{+1,-1\}$$ 为节点自旋，$$r_{ij}$$ 为节点 $$i,j$$ 在图上的最短路径距离，$$d=2$$ 为空间维度。指数 $$\sigma>0$$ 是控制相互作用范围的关键参数：$$\sigma$$ 越小，相互作用衰减越慢，长程依赖性越强（命题 5.2 和 5.3 通过范围度量 $$\hat{\rho}_i(\Delta E)$$ 给出了解析表达式，并证明当 $$\sigma\le 1$$ 时该度量随系统尺寸发散）。基准提供了两个难度等级——easy（$$\sigma=1.5$$）和 hard（$$\sigma=0.6$$），搭配五组图尺寸 $$L\in\{16,32,64,128,256\}$$（节点数 $$256$$ 至 $$65536$$），共十个数据集（表 1）。这种设计使得**长程依赖程度成为可调节的实验变量**，而非其他基准中不可控的隐含属性。

### 2. 伪临界温度采样与构型生成

为最大化节点特征间的空间相关性，基准在**伪临界温度** $$T_c$$ 下对系统进行马尔可夫链蒙特卡洛（MCMC）采样。在临界点附近，自旋的连通相关函数呈代数衰减 $$C(\mathbf{r})\sim r^{-\eta}$$，表明系统存在长程序关联。采样算法混合了局部自旋翻转的 Metropolis 更新与基于 Alias-Walker 方法的 $$\mathcal{O}(1)$$ 团簇更新，高效生成强长程相关的自旋构型。每个构型即为一个独立的数据样本，其分布天然包含远距离节点间的非平凡依赖关系，**使得下游预测任务无法仅通过局部信息准确完成**。

### 3. 图表示构造与预测任务

每个自旋构型被直接映射为一个**属性图**（图 1 左、中）：图拓扑是固定的二维周期网格（每个节点与 4 个最近邻相连，边数 $$E=4N$$），节点特征 $$x_i = s_i$$，无额外边特征。预测任务为**节点级别回归**，目标量是翻转子旋 $$i$$ 所引起的能量变化：

$$\Delta E_i = s_i \sum_{j} s_j J_{ij}$$

该任务的设计处于物理模拟的核心——伊辛模型的 Metropolis 更新直接依赖于 $$\Delta E_i$$ 的计算。更重要的是，$$\Delta E_i$$ 是**全局函数**：对节点 $$i$$ 的能量变化贡献来自于图中所有其他自旋，且远距离节点的贡献由 $$J_{ij}$$ 加权，因而天然具备捕捉长程交互的属性。这表明任务的目标本身就是一个**长程依赖的代理指标**。

### 4. 神谕预测器与可证明长程证据

为了**提供模型无关的长程依赖证明**，基准设计了神谕预测器：该预测器直接使用真实的能量函数计算 $$\Delta E_i$$，但可以限制仅考虑以目标节点为中心的 $$r$$ 跳邻域内的自旋。实验表明，神谕预测器的 LogMSE 误差随邻域半径 $$r$$ 增大而平滑下降，且更小的 $$\sigma$$ 值（更难任务）需要更大的 $$r$$ 才能达到相同精度（图 2）。这从实验上证实了任务对长程信息的刚性需求。

理论上，引理 5.1 给出了最坏情况误差下界：对任何仅使用局部邻域的模型，存在自旋构型使其预测误差满足 $$|\hat{Y}_v - f_\theta(X)_v| \ge n^{-\sigma}$$，**定量证明了局部信息在原理上的不足**。此外，定义在神谕上的长程度量 $$\rho_i(\Delta E)$$ 和归一化度量 $$\hat{\rho}_i(\Delta E)$$（见命题 5.2）利用梯度揭示了远距离节点对能量预测的贡献权重，其值随 $$L$$ 增大而升高，随 $$\sigma$$ 减小而升高（图 3），且当 $$\sigma\le 1$$ 时发散（命题 5.3），**从函数结构角度验证了长程依赖的可控性与本质性**。

### 5. 评估协议与计算效率要求

基准以**LogMSE**（$$\log_{10}(\text{MSE})$$）作为主要评估指标，提供连续的反馈信号，避免传统分类任务的二值反馈。训练/验证/测试划分遵循图学习的标准设定。尤为重要的是，**LRIM 强制要求方法报告计算复杂度**（如消息传递的 $$\mathcal{O}(L\cdot E)$$ 或注意力的 $$\mathcal{O}(L\cdot N^2)$$）及任何预处理开销，以确保性能提升不会因计算成本的急剧增长而失去实际意义。这一要求直接对应了长程建模中的核心权衡：更全局的信息往往以更高的复杂度为代价。

综合来看，LRIM 通过**物理驱动的生成机制、可调的长程参数、严格的神谕证明以及计算效率的显式度量**，构建了一个完整且可变的评估框架。模块间的信息流为：物理模型（$$\sigma, L$$）→ 临界采样（构型）→ 图数据（拓扑与节点特征）→ 模型预测（$$\Delta \hat{E}_i$$）→ 连续评估（LogMSE + 复杂度）。神谕预测器嵌套于该流程中，既是评估性能上界的参照，也是推导理论下界和范围度量的分析工具。



LRIM 基准通过幂律衰减相互作用的伊辛模型构建可证明且可控的长程依赖图学习任务。其核心模块流程如下：

1.  **伊辛模型哈密顿量定义**：在二维周期网格图 $G$ 上定义具有幂律耦合常数的能量函数
    $$\mathcal{H}(\{s_i\}) = -\frac{1}{2} \sum_{ij \in G} J_{ij} s_i s_j, \qquad J_{ij} = \frac{1}{r_{ij}^{d+\sigma}}$$
    （公式1），其中 $s_i \in \{\pm 1\}$ 为节点自旋，$r_{ij}$ 为节点间最短路径距离，$d=2$ 为空间维数，$\sigma$ 是控制相互作用衰减速度的参数。此形式直接决定了数据的长程特性：$\sigma$ 越小，远距离耦合越强，任务对长程信息的依赖越显著。

2.  **伪临界温度下的蒙特卡罗采样**：为最大化配置间的空间相关性，在有限系统伪临界温度 $T_c(L)$ 附近采样。该温度由磁化率 $\chi = k_b T N (\langle m^2 \rangle_T - \langle |m| \rangle_T^2)$ 的最大值确定（附录 B.1），此时关联函数 $C(\mathbf{r}) = \langle s_i s_j \rangle - \langle s_i \rangle \langle s_j \rangle \sim 1/r^\eta$ 呈代数衰减。数值模拟采用结合局部 Metropolis 翻转与全局 Swendsen-Wang 团簇更新的混合马尔可夫链，翻转接受概率为
    $$p = \min\left(1, \exp\left(-2 \Delta E_i / k_B T\right)\right)$$
    其中 $\Delta E_i = s_i \sum_j s_j J_{ij}$ 是翻转单自旋带来的能量变化。

3.  **图构建与节点回归任务**：每个自旋构型被直接表示为节点属性图（节点特征为 $\pm 1$，边固定为 4-邻接），预测目标为每个节点的能量变化 $\Delta E_i \in \mathbb{R}$。该任务天然要求模型捕获远距离自旋的贡献，因此是检验长程能力的代理任务。

4.  **神谕预测器（Oracle predictor）**：为定量证明长程信息的必要性，构造一个仅利用局部 $r$-跳邻域内自旋的真实能量计算器。其误差随 $r$ 增大而平滑下降（图 2），且更小的 $\sigma$ 需更大邻域才能达到相同精度，表明任务对远距离信息存在刚性依赖。理论下界（引理 5.1）保证：任何仅使用局部邻域的模型在最坏情况下的预测误差至少为 $n^{-\sigma}$，即
    $$|Y_v' - f_\theta(X')_v| \geq n^{-\sigma}.$$

5.  **长程度量（Long‑rangedness metric）**：为提供模型无关的依赖性量化，定义节点级范围度量
    $$\rho_u(F) = \sum_{v \in V} \left| \frac{\partial F(X)_u}{\partial x_v} \right| d_G(u,v), \quad \hat{\rho}_u(F) = \frac{\rho_u(F)}{\sum_{v \in V} \left| \frac{\partial F(X)_u}{\partial x_v} \right|}$$
    对神谕预测器 $\Delta E$ 可导出解析表达式
    $$\rho_i(\Delta E) = \sum_{1 \leq \ell \leq r} \ell \sum_{k \in N_\ell(i)} J_{ik}, \quad \hat{\rho}_i(\Delta E) = \frac{\rho_i(\Delta E)}{\sum_{1 \leq \ell \leq r} \sum_{k \in N_\ell(i)} J_{ik}}$$
    （命题 5.2）。当 $\sigma \leq 1$ 时，$\rho_i$ 和 $\hat{\rho}_i$ 随系统尺寸 $L$ 发散（命题 5.3），从理论上验证了无限长程依赖的可控性。图 3 显示 $\hat{\rho}_i(\Delta E)$ 随 $L$ 增大、$\sigma$ 减小而上升，且 $\sigma \leq 1$ 时增长速度加快，与理论一致。

以上模块共同构成了一个可证明、可扩展、难度连续可调的长程图学习评估体系。



## 实验与关键发现

### 基准测试主结果

我们在 LRIM-16 和 LRIM-32 的 easy/hard 子集上评估了主流的消息传递神经网络（MPNN）和图变换器（Graph Transformer）基线，并要求透明报告计算复杂度。表2汇总了各方法的节点回归 LogMSE 及其预处理与逐次前传的计算开销上限。主要发现如下：

1. **所有基线模型均远未达到神谕预测器（Oracle）的性能**。在 LRIM-16-hard 上，最优的图变换器 GPS‑LapPE 的 LogMSE 与 Oracle（r=∞）之间的差距超过 5.666（Table 2）；在 LRIM‑32‑hard 上，GPS‑RWSE 与 Oracle 的差距超过 5.866。即便是 easy 难度（σ=1.5），GPS‑Base 与 Oracle 的差距也超过 4.704（LRIM‑16‑easy）和 4.866（LRIM‑32‑easy）。这表明捕获必要的长程信息对现有模型构成根本性挑战。


![[assets/figures/papers/iclr26_0015_IAZXEX1dVV_LRIM_a_Physics-Based_Benchmark_for_Provably_Eval/figures/005_Table_2.jpg]]
*Table 2: Baseline performance on LRIM-16 and LRIM-32 datasets. The number of edges E corresponds to 4N in our datasets. We emphasize the importance of reporting computational complexity alongside performance results, as scalability is a crucial aspect in long-range modeling*

2. **图变换器在效率–性能权衡中占据上风，但可扩展性差**。GPS 系列凭借全局注意力获得了相对低的 LogMSE（如 GPS‑LapPE 在 LRIM‑16‑hard 上达到约 −7 量级），但其计算复杂度为 O(L·N²)（L 为层数，N 为节点数），在大图上迅速触及内存瓶颈。相比之下，MPNN 类模型（GIN、GatedGCN）虽仅需 O(L·E) 的线性边复杂度且能顺利运行到更大尺度，但性能显著更弱（GIN 在 LRIM‑16‑hard 仅 −2.533；GatedGCN −3.844）。这说明当前的局部信息聚合机制远不能满足任务对远距离依赖的要求。

3. **零样本迁移凸显泛化与拓展能力的缺口**。将模型在 LRIM‑16‑hard 上训练后直接推理更大系统，所有方法的 LogMSE 都急剧上升（Table 3）。例如，GatedGCN‑VNG 迁移到 LRIM‑32‑hard 时 LogMSE 与 Oracle 的差距扩大至 >8.957；GIN 迁移到 LRIM‑256‑hard 时差距更是 >10.799。更严重的是，GPS 变体在 LRIM‑256 上仅执行推理即出现显存溢出（OOM），证明其无法应对大规模图（Table 3 及有向消融 Table 8）。该现象暴露了现有“长程”模型在系统尺寸推广上的脆弱性。


![[assets/figures/papers/iclr26_0015_IAZXEX1dVV_LRIM_a_Physics-Based_Benchmark_for_Provably_Eval/figures/006_Table_3.jpg]]
*Table 3: We evaluate how well models trained on LRIM-16-hard transfer to larger systems without additional training. The results show that performance generally degrades as system size increases. GPS variants encounter out-of-memory (OOM) errors on LRIM-256 even for inferenceonly, demonstrating the importance of considering the scalability of long-range methods*

### 消融研究

#### 层数与感受野消融

我们系统考察了模型深度对性能的影响（Figure 4）。所有模型在约 10–16 层之前均随层数增加而持续改善，但随后进入平台，且与神谕预测器之间存在巨大鸿沟。这一饱和现象表明：


![[assets/figures/papers/iclr26_0015_IAZXEX1dVV_LRIM_a_Physics-Based_Benchmark_for_Provably_Eval/figures/008_Figure_4.jpg]]
*Figure 4: LogMSE (↓) of the layer ablation study plotting performance as a function of number of layers. Oracle performance is clamped at -10 for visualization purposes. Note, each combination of model and layer is a separate trained model instance. On the top, models are trained and evaluated on LRIM-16-hard, while on the bottom they are trained and evaluated on LRIM-32-hard. All models consistently improve with increased depth but plateau with a significant gap remaining to the oracle predictor*

- **单纯的深度堆叠不能弥补长程信息缺口**：即使感受野覆盖了大部分图的直径，MPNN 仍无法逼近依靠精确能量函数的 Oracle。其原因在于局部迭代聚合难以有效传递和整合远距离的衰减耦合信息。
- 不同架构的平台高度不同：图变换器平台更低（更好），但其相对于 Oracle 的绝对差距仍然显著。因此，需要超越现有注意力或消息传递机制的新原理来高效编码远程交互。

为量化任务固有的长程程度，我们使用神谕预测器并将其邻域截断到 r‑hop 距离（即仅使用距目标节点 r 跳以内的自旋信息计算 ΔE）。图 2 和图 5 显示：

- 随着允许的邻域半径 r 增大，Oracle 的 LogMSE 平滑下降，但更小的相互作用参数 σ（更困难的设置）需要大得多的 r 才能达到同等精度。例如在 LRIM‑32‑hard（σ=0.6）上，Oracle 必须在接近图直径的邻域内聚合信息才能接近零误差。
- 系统尺寸 L 的增加在固定 σ 下也会提高任务难度（Figure 5 右半侧）。这些结果从模型无关的角度严格证明了**局部信息不足以完成该基准任务**，且难度可通过 σ 和 L 连续调节。

进一步，我们引入归一化范围度量 $\hat{\rho}_i(\Delta E) = \left(\sum_{\ell} \ell\sum_{k\in N_\ell(i)} J_{ik}\right) / \left(\sum_{\ell}\sum_{k\in N_\ell(i)} J_{ik}\right)$ 来定量刻画每个节点的预测任务对远距离依赖的平均加权距离。图 3 显示 $\hat{\rho}_i(\Delta E)$ 随系统尺寸 L 增大而上升，随 σ 增大而下降；当 σ ≤ 1 时该度量随 L 发散（命题 5.3），验证了长程依赖程度的可控性。这为基准的难度设定提供了解析保障。

#### 计算机视觉基线的消融

为评估规则网格上非图专用模型的表现，我们测试了 2D 卷积网络（CNN）和视觉变换器（ViT）。关键结论如下：

- **循环填充（circular padding）优于零填充**：由于 LRIM 网格采用周期边界条件，使用循环填充的 Circular‑CNN 更能适配拓扑，其 LogMSE 系统性地低于 Grid‑CNN（Table 5）。
- **存在最优感受野大小**：CNN 的性能随卷积层层数和核尺寸先升后降（Figure 15）。过度增加深度或感受野反而损害泛化，这与 GNN 中观察到的深度饱和现象一致，说明单纯的宽感受野但不具备选择性信息整合能力反而引入噪声。
- **ViT 的补丁粒度与深度存在最佳配比**：将网格切分为 2×2 补丁并采用 5 层 Transformer 编码器时，ViT 在 LRIM‑16‑hard 上达到最佳性能（Table 6）。更小的补丁（1×1）或更深的架构并未带来额外收益，暗示当前 Transformer 设计在编码全局交互时的效率瓶颈。

#### 有向图变体消融

我们将无向图替换为有向边（每条无向边拆成两条有向边）后重新评估主流模型。有向设置下的性能趋势与无向版本高度一致（Table 7，Table 8，Figure 16）：MPNN 随层数增加而饱和，GPS 在中等尺度的性能优势在更大图上被 OOM 抵消。这进一步说明**现有模型的长程建模缺陷并非由图的方向性导致，而是源于其核心信息传递机制的可扩展性限制**。

### 失败模式与瓶颈诊断

综合上述实验，我们识别出以下关键失败模式：

1. **局部聚合格导致系统性欠拟合**：即便 1‑WL 等价类分析（Figure 12）表明 MPNN 在有限训练数据下有能力过拟合训练集，但要实现泛化需要接近 Oracle 的感受野。实际模型的表示能力与优化轨迹无法在合理参数预算下逼近这一要求，导致泛化误差长期居高不下。

2. **注意力机制的平方复杂度成为大图障碍**：全局注意力赋予图变换器更强的长程捕获潜力，但其 O(N²) 的空间/时间成本使模型在面对超过 1 万节点的图时不可行（Table 3 中的 OOM）。这严格限制了其在物理模拟等需要大规模系统的问题中的应用。

3. **深度扩展无法逾越“长程鸿沟”**：层数消融显示，即使感受野半径达到图直径，所有模型的性能仍远逊于利用精确能量函数的 Oracle。这意味着瓶颈不仅在感受野大小，更在于**模型对远距离耦合的任意函数逼近能力不足**——当前 GNN 的更新函数和聚合策略尚无法从局部邻域迭代中重建出幂律衰减的远程交互效应。

4. **基准的连续反馈暴露平滑但不收敛的优化曲面**：Oracle 的连续 LogMSE 曲线（Figure 2）表明任务难度可通过 σ 和 L 平滑调节，但现有模型在较强长程设置下（σ ≤ 0.6）的学习曲线往往过早进入平台，优化过程未能找到跨越局部极小值的路径。

### 小结

LRIM 基准的主实验与消融一致揭示：**在可控的幂律衰减相互作用下，捕捉长程依赖是可扩展图学习面临的核心瓶颈**。消息传递模型因计算高效而可拓展至大图，但缺乏远程交互的直接通路；全局注意力模型虽提升长程建模精度，却以平方级复杂度为代价，无法泛化到大系统。两类方法在神谕预测器设定的性能上界面前均存在数量级差距。这些发现表明，未来方法需要从根本上设计具备次二次方复杂度、且能显式编码幂律距离衰减机制的图学习架构，同时维持对系统尺寸的泛化能力。



## 定位与知识库关联

本节从基线关系、适用边界、固有局限和开放问题四个维度，将LRIM基准纳入现有图学习长程能力评估的方法谱系中加以定位。LRIM的核心贡献在于为长程依赖性提供了可证明且连续可控的评估框架，从而暴露出当前消息传递和图变换器模型在效率-精度权衡上的深层瓶颈。

### 与现有基线及模型范式的关系

**性能鸿沟与计算难扩展性**。LRIM通过强制基线模型报告计算复杂度（Table 2），清晰地勾勒出一幅双峰谱系：局部消息传递模型（GIN、GatedGCN）虽以 $O(L \cdot E)$ 的线性复杂度轻松扩展至万级节点，但其LogMSE性能相较神谕上限（Oracle, $r=\infty$）存在巨大鸿沟——例如在LRIM-32-hard上，最优MPNN变体与神谕的差距超过5.866（Table 2）。图变换器基线（GPS）凭借全局注意力大幅缩小性能差距，但其 $O(L \cdot N^2)$ 复杂度导致推理阶段在LRIM-256上直接遭遇内存溢出（OOM）（Table 3），揭示了提升长程能力所面临的严重可扩展性惩罚。这种双相权衡正是LRIM意图强调的核心瓶颈：**增加有效感受野必然导致指数级或平方级的计算代价**。

**层深度的边际收益递减**。对层数的消融实验（Figure 4）表明，无论MPNN还是Transformer，增加层数仅能带来约10-16层以内的性能提升，其后即进入显著的平台期。即便在最佳深度配置下，所有训练模型与神谕预测器之间仍有不可逾越的差距。这表明，仅靠简单的深度堆叠无法有效捕获任务所必需的全局依赖性；模型在聚合远距离信息时可能遭遇梯度衰减、表示平滑或容量饱和，从而限制了更深网络的优势释放。

**与传统基准的本质差异**。相较于依赖真实数据且无法保证长程必要性的LRGB等基准，LRIM引入了三个方法学上的根本跃迁（参见changed_slots）：
1. **可证明的长程依赖**：通过神谕预测器在受限邻域下的性能退化（Figure 2）和引理5.1的下界证明（$|Y_v' - f_\theta(X')_v| \geq n^{-\sigma}$），严格确立了任何仅使用局部信息的模型必定产生不可消除的误差，为基准的科学性提供了理论锚点。
2. **连续可控的难度调节**：相互作用幂律指数 $\sigma$ 和系统尺寸 $L$ 构成一对精细的“控制旋钮”（Figure 3, Table 1）。更小的 $\sigma$（硬任务）强化远距离节点对能量变化的贡献，从解析上导致范围度量 $\hat{\rho}_i(\Delta E)$ 随系统尺寸发散（命题5.3，$\sigma \leq 1$）。这种连续可调性使得研究者能够定量分析模型长程能力的灵敏度，而非仅获得二元的成功/失败信号。
3. **细粒度反馈**：采用LogMSE作为训练和评估的连续指标，取代了多数现有基准提供的离散或有限级别反馈，使性能退化曲线平滑化（Figure 2），有助于探究模型在“部分长程信息”下的渐进表现。

### 适用边界

LRIM的设计根植于明确的物理建模和拓扑假设，这定义了其当前的有效作用域：
- **拓扑范围**：数据集由具有周期边界的二维正方网格构成，每个节点恰好连接4个最近邻。因此，基准直接评估的是模型在**规则结构上的长程关联解析能力**。对于不规则图、社交网络或异构图，1-WL等价类区分能力已非主要挑战（Figure 12），但其长程依赖的形式与网格上幂律相互作用可能存在本质不同，基准结论不可不加检验地外推。
- **任务类型**：当前仅包含**节点级回归任务**（预测 $ \Delta E_i $）。这一任务设计源于物理模拟的直观需求，并天然存在与空间相关性相关的梯度度量（命题5.2），但尚不能表征边级或图级任务中的远程效应。
- **难度控制假设**：长程特性完全由具有幂律截断的伊辛哈密顿量（公式1）和假临界温度采样保证。该物理模型虽经典，但不涵盖具有层次化、时变或非稳态长程效应的系统。因此，基准无法回答模型如何处理“非物理”或非代数衰减的全局依赖。
- **评测维度**：评估指标统一为LogMSE，侧重预测精度；未考虑不确定性量化、物理一致性或外推鲁棒性，这些可能在真实应用部署中同样关键。

### 核心局限

除了上述边界本身，LRIM基准的当前形态存在若干方法学上的内在局限：
1. **单模态数据生成**：全部配置均由伊辛模型的MCMC模拟生成，这固然保证了可复现性和可证明性，但也意味着基准无法覆盖现实世界中由数据生成机制带来的分布偏移、噪声或混杂因素，从而可能高估或低估模型在真实任务上的性能。
2. **架构探索的有限性**：尽管选择了GIN、GatedGCN和GPS作为代表性基线，但LRIM尚未系统涵盖基于结构重布线、多尺度层次聚合或记忆机制的近期新兴变体。可能的替代方案在计算效率和对长程信号的利用上或许有不同表现，需由后续研究补全。
3. **神谕的近似角色**：神谕预测器虽提供了理论“天花板”，但其计算依然依赖于完整的能量函数。在实际训练中，模型能否逼近这一上限，受限于容量、优化陷阱和有限数据下的过拟合行为（如1-WL分析所示，MPNN可能在有限训练集上过拟合，却无法真正泛化，Figure 12及附录D）。因此，神谕差距不能完全等同于“学习能力不足”，也可能部分归因于样本效率或归纳偏置。
4. **公平性的双层要求**：基准强调需同时报告性能与计算预算，这一做法虽然提升了公平性，但也提高了参与门槛。在进行模型比较时，若未将预处理开销（如位置编码计算、注意力矩阵存储）考虑在内，可能得出误导性结论。

### 开放问题与未来工作

基于上述分析，一系列挑战性问题被凸显出来，为后续图学习长程方法的研究提供了明确方向：

1. **超越规则网格的拓扑泛化**：如何将可证明、连续可控的长程性质拓展至一般图结构（异构图、动态图、有向图）？是否可能通过定义图上的等效哈密顿量或利用扩散算子的特征衰减来构造类似的难度控件？
2. **线性复杂度下的全局建模**：Figure 4中的深层平台期提示了常规深度叠加的失效。发展具有近线性复杂度（接近 $O(L \cdot E)$）却具备全局感受野的架构，是突破效率瓶颈的核心挑战。可能的途径包括物理启发的快速多级展开、层次化潜空间交互或学习到的稀疏全局连接。
3. **突破深度平台期**：平台期的根源究竟是梯度流动问题、表示过度平滑，还是模型容量的饱和？能否设计动态路由或自适应感受野扩展机制，使得每增加一层网络都能稳定地捕获到更远距离的实质性信息？
4. **跨尺度的零样本泛化**：从LRIM-16向大系统迁移时的灾难性退化（Table 3）表明，现有模型未能提取出与尺寸无关的长程普适规律。如何让模型学习的相互作用模式外推到未见过的系统尺寸甚至不同的 $\sigma$ 值，是实现真正物理直觉驱动的图学习所必须跨越的门槛。
5. **多物理基准矩阵**：将可证明长程框架推广到其他普适类物理模型（如XY模型、Potts模型、无序自旋系统），可以构建一个更完备的基准矩阵，全面评估图模型处理不同类型全局依赖（连续变量、多体作用、淬火无序）的能力。
6. **更丰富的评估协议**：引入物理一致性、不确定性量化、长程关联重建等辅助指标，有望揭示仅靠LogMSE可能隐藏的模型缺陷，并推动模型向更可信的方向演化。

通过系统性地回应这些问题，图学习社区不仅可开发出更具泛化性的长程模型，也能深化对“长程依赖”在不同拓扑和任务分布下的数学本质的理解。



## 原文 PDF

![[paperPDFs/ICLR_2026/LRIM_a_Physics_Based_Benchmark_for_Provably_Evaluating_Long_Range_Capabilities_in_Graph_Learning.pdf]]
