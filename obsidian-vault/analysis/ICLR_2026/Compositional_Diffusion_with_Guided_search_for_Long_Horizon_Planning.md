---
title: "Compositional Diffusion with Guided search for Long-Horizon Planning"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/Compositional_Diffusion_with_Guided_search_for_Long_Horizon_Planning.pdf
project_link: https://cdgsearch.github.io/
code_link: null
openreview_forum_id: b8avf4F2hn
aliases:
- CDGSC
- CDGSLHP
tags:
- ICLR_2026
- topic/generative_models_diffusion
- topic/generative_models_diffusion/diffusion_image_video
core_operator: "在扩散去噪过程中嵌入基于种群的引导搜索，通过迭代重采样促进局部-全局信息传递，并利用基于似然（DDIM反演曲率）的剪枝来选择和保留局部兼容的模式序列，从而消除模式平均并生成连贯的全局计划。"
primary_logic: "全局计划可行当且仅当其所有局部转移可行；可使用局部扩散模型DDIM反演的曲率近似衡量局部可行性，并通过在重叠区域迭代重采样实现长距离依赖传播。"
claims:
- "在OGBench Maze巨型任务上，CDGS大幅优于朴素组合方法（GSC）和逆强化学习基线（HIQL等）"
- "在任务与运动规划（TAMP）的Rearrangement Memory任务中，CDGS显著优于基于搜索和提示的方法"
- "通过增加批次大小和重采样步数，CDGS的性能可平滑扩展"
- "在全景图像生成中，CDGS实现了与Sync-Diffusion相当的感知相似度，并拥有更好的风格相似度和提示对齐度"
---

# Compositional Diffusion with Guided search for Long-Horizon Planning

> [!tip] 核心洞察
> 全局计划可行当且仅当其所有局部转移可行；可使用局部扩散模型DDIM反演的曲率近似衡量局部可行性，并通过在重叠区域迭代重采样实现长距离依赖传播。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 面向长视界规划的组合扩散与引导搜索 |
| 英文题名 | Compositional Diffusion with Guided search for Long-Horizon Planning |
| 会议/期刊 | ICLR 2026 (Oral) |
| Links | [paper](https://openreview.net/forum?id=b8avf4F2hn) · [Project](https://cdgsearch.github.io/) |
| Topic | #topic/generative_models_diffusion #topic/generative_models_diffusion/diffusion_image_video |
| Method | Compositional Diffusion with Guided Search (CDGS) |
| Dataset | OGBench PointMaze (Giant), OGBench AntMaze (Giant), AntSoccer (Arena, 17D), Rearrangement Memory (Task 1) |

> [!tip] 效果简介
> - OGBench PointMaze (Giant) 上，Success Rate (%) 为 87±3，对比 GSC 29±2，变化 +58。
> - OGBench AntMaze (Giant) 上，Success Rate (%) 为 85±3，对比 HIQL 21±2，变化 +64。
> - AntSoccer (Arena, 17D) 上，Success Rate (%) 为 69±1，对比 GSC (17D) 65±3，变化 +4。

## 概要

**核心问题：组合生成中的模式平均困境。** 将多个短视界局部模型组合以生成长视界全局计划，是机器人规划、全景图像生成与长视频生成等领域的共性范式。然而，当局部条件分布呈现多模态时，现有的朴素组合采样方法会强制对不兼容的局部模式进行平均——即“模式平均”（mode averaging）——导致生成的全局计划中出现局部不可行或全局不连贯的片段。这一瓶颈根植于组合扩散采样的信息传递机制：重叠变量的边际分数仅通过相邻因子的条件分数取平均来近似，当候选模式序列不一致时，该平均操作将产生偏离真实分布的过渡区域。

**方法定位：将引导搜索嵌入扩散去噪过程。** 本文提出 **组合扩散与引导搜索（Compositional Diffusion with Guided Search, CDGS）**，直接在扩散模型的迭代去噪过程中嵌入基于种群的搜索机制，以解决模式平均问题。CDGS 的核心操作包含两个相互协同的模块：（1）**迭代重采样**——在每一步去噪中，对一批候选全局计划反复执行组合扩散采样，使局部-全局信息通过重叠变量的分数平均在远距离片段间传播；（2）**基于似然的剪枝**——利用 DDIM 反演轨迹的曲率作为局部可行性的代理度量，对候选计划进行排名，仅保留高似然的精英计划进入下一轮去噪。该方法无需额外训练，仅需预训练的短视界扩散模型即可在推理时直接生成长视界连贯计划。

**方法谱系与知识库定位。** CDGS 处于组合扩散采样与启发式搜索的交叉点。相较于朴素组合扩散基线 **GSC**（Mishra et al., CoRL 2023）仅执行单次组合采样，CDGS 引入了群体探索与迭代信息传递；相较于利用重叠信息训练的 **CompDiffuser**（Luo et al., arXiv 2025），CDGS 无需对局部模型进行联合训练，保持了模块化与即插即用特性。在搜索机制上，CDGS 借鉴了交叉熵方法（CEM）的精英选择思想，但将搜索空间定义在扩散模型的去噪轨迹上，而非原始参数空间。在全景生成领域，CDGS 与 **Sync-Diffusion**（Lee et al., NeurIPS 2023）和 **Multi-Diffusion**（Bar-Tal et al., 2023）形成对比——前者通过联合去噪实现全局一致性但可能牺牲局部细节，后者通过融合平均保证局部质量但缺乏全局约束，而 CDGS 通过搜索与剪枝在两者之间取得平衡。在长视频生成中，CDGS 在 7 倍于基线的视界上仍保持与 **CogVideoX-2B**（Yang et al., arXiv 2024）相当的主体一致性与时间稳定性。

**主要结果概览。** 在机器人长视界规划基准 OGBench 上，CDGS 在巨型迷宫任务中大幅超越朴素组合方法 GSC（PointMaze Giant: 87% vs 29%）和逆强化学习基线 HIQL（AntMaze Giant: 85% vs 21%），达到与预言机相当的性能。在任务与运动规划（TAMP）的 Rearrangement Memory 任务中，CDGS 的成功率（0.42）显著优于基于搜索和提示的基线（如 GSC 无任务规划仅 0.07）。在全景图像生成中，CDGS 实现了与 Sync-Diffusion 相当的感知相似度，同时拥有更优的风格相似度与提示对齐度。在长视频生成中，CDGS 在 350 帧（7 倍扩展视界）上保持了 91.67 的主体一致性得分，与 50 帧的 CogVideoX-2B 基线接近。消融实验与缩放分析表明，移除规划细化（PR）模块会导致性能显著下降，而增大批次大小和重采样步数可平滑提升成功率，验证了搜索机制的有效性与可扩展性。

### 长视界规划中的组合生成困境

长视界规划的核心挑战在于：如何从一组已知的短视界局部模型中，构建出全局连贯的长视界计划。在机器人操作、任务与运动规划（TAMP）以及视觉内容生成等领域，获取长视界演示数据往往代价高昂，而短视界的局部数据（如单步技能、相邻帧过渡）则相对丰富。因此，**组合生成**（compositional generation）成为一种自然的范式——通过组合局部模型来合成全局计划。

形式上，一个长视界计划 $\tau$ 可被建模为一个因子图上的联合分布。利用Bethe近似，该联合分布可分解为局部因子分布的乘积，并通过度修正避免变量节点的重复计数：

$$p(\tau) := \frac{\prod_{j=1}^M p(y_j)}{\prod_{i=1}^N p(x_i)^{d_i-1}}$$

其中 $y_j$ 表示局部因子（如相邻状态之间的转移），$x_i$ 为共享变量节点，$d_i$ 为变量节点的度。在扩散模型的框架下，组合采样通过聚合各因子的分数函数来实现：

$$\nabla \log p(\tau) := \sum_{j=1}^M \nabla \log p(y_j) + \sum_{i=1}^N (1 - d_i) \nabla \log p(x_i)$$

对于重叠变量，其边际分数通过相邻因子条件分数的平均来近似。

### 模式平均：组合生成的根本瓶颈

尽管上述组合采样框架在理论上优雅，但在实践中面临一个关键失败模式——**模式平均**（mode averaging）。当局部因子分布呈现多模态时（例如，从一个中间状态出发存在多条可行路径，或全景图的相邻窗口允许多种语义延续），朴素组合采样会在重叠区域对不同局部模式进行平均，产生一个不属于任何真实模式的“折中”结果。

如 **Figure 3** 所示，在一个简单的一维规划域中，从起点 $x_1$ 到终点 $x_7$ 存在上下两条可行路径。朴素组合采样可能选择从上方出发但到达下方终点（或反之），此时中间变量 $x_{2:6}$ 的模型被迫同时满足两个冲突的约束，导致对不兼容模式进行平均，最终生成不可行的局部转移（红色标记）。在机器人规划中，这表现为**状态幻觉**（state hallucination）——物体出现在几何上不可能的位置；在视觉生成中，则表现为全景图的局部断裂或长视频中的主体突变。

### 现有方法的缺口

现有组合生成方法在应对模式平均问题上存在明显不足：

- **朴素组合扩散**（如 **GSC**, Mishra et al., CoRL 2023）：直接使用标准组合评分进行采样，不包含任何搜索或剪枝机制，在高维、多模态场景下成功率急剧下降。在OGBench PointMaze Giant任务上，GSC的成功率仅为29±2%。

- **利用重叠信息训练的方法**（如 **CompDiffuser**, Luo et al., arXiv 2025）：通过在训练阶段引入重叠信息来改善局部一致性，但无法在推理时动态纠正模式序列的不匹配。

- **逆强化学习基线**（如 **HIQL**, Park et al., NeurIPS 2023）：虽然在部分迷宫任务上表现良好，但需要大量训练数据，且在高维组合任务（如AntSoccer 17D状态空间）和TAMP场景中难以扩展。

- **图像/视频生成中的同步方法**（如 **Sync-Diffusion**, Lee et al., NeurIPS 2023; **Multi-Diffusion**, Bar-Tal et al., 2023）：通过联合去噪或加权融合来增强局部一致性，但缺乏全局层面的搜索机制来主动筛选连贯的模式序列。

### 本文动机

上述缺口揭示了一个核心矛盾：**组合生成需要同时满足局部可行性与全局连贯性，而朴素组合采样在这两个目标之间缺乏有效的协调机制**。当局部模式不兼容时，简单的分数平均会将冲突“平滑”为不可行的中间状态，而非主动探索并选择兼容的模式序列。

本文的动机由此明确：**在扩散去噪过程中嵌入引导搜索**，通过种群级别的迭代重采样和基于似然的剪枝，实现局部-全局信息的高效传递，从而在保持局部可行性的同时确保全局计划的连贯性。这一思路将扩散模型的生成能力与基于种群的搜索策略相结合，为解决长视界规划中的模式平均问题提供了新的路径。

## 核心方法与创新机理

CDGS 的核心创新在于将**基于种群的引导搜索直接嵌入扩散去噪过程**，以解决长视界组合规划中的**模式平均**问题。当局部技能分布呈现多模态时，朴素组合采样会强制不兼容的局部模式相互妥协，导致生成的中间状态落入低似然区域，产生不可行的局部转移或状态幻觉。CDGS 通过三个相互协同的机制消除这一瓶颈：

### 1. 迭代重采样：局部-全局信息传递

标准组合扩散的分数计算仅对重叠变量做一次条件分数平均，信息无法在远距离片段间有效传播。CDGS 在每次去噪步内执行 **U 次迭代重采样**（Algorithm 2, Line 8）：交替进行前向加噪 $\tau^{(t)} \sim p(\tau^{(t)}|\tau^{(t-1)})$ 和反向去噪，使重叠区域的分数平均能够将一致性约束逐步传递至整个计划链。这一机制是消除模式平均的第一道防线——Figure 3(c) 显示，仅添加迭代重采样即可大幅减少不可行转移的出现频率。

### 2. 基于似然的候选剪枝：DDIM 反演曲率

迭代重采样虽能降低模式平均的概率，但无法根除。CDGS 引入了一个**局部可行性度量**来主动筛选精英候选：对每个局部计划 $y_m^{(0)}$ 执行 DDIM 反演，计算其扩散轨迹的曲率：

$$g(y^{(0)}) = \sum_{i=1}^{T} \left\| \frac{\partial \varepsilon_\theta(y^{(i-1)}, i)}{\partial i} \right\|_2$$

曲率越低，表明 $y^{(0)}$ 越接近 $p(y)$ 的某个高似然模式，即局部转移越可行。全局计划的排名度量定义为各局部可行性的乘积：

$$J(\tau^{(0)}) = \prod_{m=1}^{M} \exp\left(-g(y_m^{(0)})\right)$$

CDGS 据此对种群中的候选计划排序，保留精英并重新填充（Algorithm 1, Lines 7-8）。Figure 3(d) 和 Figure 5(a,b) 证实，剪枝能有效过滤因模式平均产生的不可行转移和状态幻觉。

### 3. 种群采样与自适应推理计算

CDGS 维护 $B$ 个候选计划组成的种群，在去噪过程中持续探索不同的模式序列组合。这一设计使方法具备**自适应推理计算**特性：通过增大批次大小 $B$ 和重采样步数 $U$，可将更多计算分配给困难问题。Figure 5(c,d) 的缩放分析表明，任务规划成功率随 $B$ 和 $U$ 单调提升，且二者存在协同效应——运动规划仅在批次足够大时才能从更多重采样步中获益。

### 与基线方法的本质差异

| 机制 | 朴素组合（GSC） | CDGS |
|------|----------------|------|
| 信息传递 | 单次分数平均 | 迭代重采样，长距离依赖传播 |
| 候选筛选 | 无筛选，保留所有样本 | 基于 DDIM 反演曲率的精英剪枝 |
| 搜索策略 | 单次采样 | 种群维护，类交叉熵方法探索 |

消融实验（Table 1, Table 4, Table 5 中 CDGS w/o PR vs 完整 CDGS）一致表明，移除规划细化（PR，即剪枝模块）会导致性能显著下降，验证了剪枝在长视界任务中的必要性。在 Rearrangement Memory 任务上，GSC（无任务规划，等价于 CDGS w/o RP 和 PR）的成功率仅为 0.07，而完整 CDGS 达到 0.42（Table 3），差距达 6 倍。

![[assets/figures/papers/paper_list_l28_https_openreview_net_forum_id_b8avf4F2hn/figures/002_Figure_1.jpg]]
*Figure 1: Compositional Diffusion with Guided Search (CDGS) composes short-horizon plan distributions to sample long-horizon goal-directed plans directly at inference. Unlike na¨ıve compositional sampling, it explores diverse plans and filters locally inconsistent paths to avoid “mode averaging”, yielding globally coherent plans*

![[assets/figures/papers/paper_list_l28_https_openreview_net_forum_id_b8avf4F2hn/figures/008_Figure_4.jpg]]
*Figure 4: Compositional diffusion with Guided Search. At each denoising timestep, CDGS iteratively denoises a batch of noisy candidate global plans by (i) iterative resampling to propagate information through averaged scores at overlaps (blue) and (ii) pruning candidates with local inconsistencies based on the predicted clean samples (yellow). This process ensures all local plans align and belong to high-likelihood regions of p(y), producing globally coherent plans*

CDGS（Compositional Diffusion with Guided Search）构建了一个在扩散去噪过程中内嵌引导搜索的组合规划框架。其核心流水线由四个紧密耦合的模块构成，共同解决长视界组合采样中的模式平均（mode averaging）问题。

### 输入输出流

框架的输入为：一组局部扩散模型 $\{p(y_j)\}_{j=1}^M$，每个模型捕获短视界转移分布；指定的起始状态 $s_{\text{start}}$ 和目标状态 $s_{\text{goal}}$；以及种群大小 $B$ 和重采样步数 $U$ 等超参数。输出为一个全局连贯的长视界计划 $\tau = \{y_1, \ldots, y_M\}$，其中每个局部段 $y_i$ 在局部模型的高似然区域内且相邻段在重叠变量上保持一致。

### 模块协作关系

**1. 种群采样与剪枝（Population-based Sampling & Pruning）** 作为外循环，维护一个大小为 $B$ 的候选计划种群。在每个扩散去噪时间步 $t$，该模块调用组合分数模块获取全局扩散分数，执行一步去噪后，通过计划排名模块对所有候选进行评估，保留精英候选并重新填充种群，形成类似交叉熵方法的探索-利用机制（Algorithm 1）。

**2. 组合分数模块（ComposedScore）** 负责计算全局扩散分数。它将因子图上的组合分数分解（Eq. 3）与迭代重采样相结合：在每次去噪步内，重复执行 $U$ 次“前向加噪-反向去噪”循环，通过重叠变量的分数平均实现局部-全局信息传递，使远距离依赖得以传播（Algorithm 2）。同时，该模块在扩散轨迹的起点和终点强制实施目标修复（Goal Inpainting），确保生成的计划满足边界条件。

**3. 计划排名模块（Plan Ranking）** 通过DDIM反演评估每个候选计划的局部可行性。具体而言，对每个局部段 $y_m$ 进行DDIM反演，计算其扩散轨迹的曲率 $g(y_m^{(0)})$（Eq. 5），曲率越低表示该段越接近局部分布 $p(y_m)$ 的高似然模式。将所有局部段的可行性度量聚合为全局排名指标 $J(\tau^{(0)})$，用于剪枝阶段筛选不兼容模式序列产生的不可行计划。

### 关键控制机制

框架的性能由两个关键控制旋钮调节：**批次大小 $B$** 决定种群探索的广度，**重采样步数 $U$** 决定信息沿计划链传播的深度。消融实验表明，两者协同作用：仅增大 $B$ 而不增加 $U$ 时，运动规划成功率的提升有限；而 $U$ 的增加仅在 $B$ 足够大时才能有效提升任务规划成功率（Figure 5c-d）。移除剪枝模块（即 CDGS w/o PR）会导致性能显著下降，验证了基于似然的候选筛选对于消除模式平均的必要性。

### 问题形式化：因子图与组合扩散

CDGS 将长视界规划建模为因子图上的组合生成问题。给定一个由 $N$ 个变量节点 $\{x_i\}_{i=1}^N$ 和 $M$ 个因子节点 $\{y_j\}_{j=1}^M$ 构成的因子图，其中每个因子 $y_j$ 对应一段短视界局部计划（例如相邻状态之间的转移），全局联合分布通过 **Bethe 近似** 表示为：

$$p(\tau) := \frac{\prod_{j=1}^M p(y_j)}{\prod_{i=1}^N p(x_i)^{d_i-1}} \tag{1}$$

其中 $d_i$ 为变量节点 $x_i$ 在因子图中的度（即参与多少个因子）。公式 (1) 的直觉是：将全局计划分布分解为局部因子分布的乘积，再通过度修正项 $p(x_i)^{d_i-1}$ 消除重叠变量被重复计数的影响。

在扩散采样框架下，对应的 **组合分数函数** 为：

$$\nabla \log p(\tau) := \sum_{j=1}^M \nabla \log p(y_j) + \sum_{i=1}^N (1 - d_i) \nabla \log p(x_i) \tag{3}$$

该公式将全局扩散分数分解为局部因子分数与变量节点分数的加权和，使得在推理时可以直接组合多个预训练的局部扩散模型来采样全局计划，而无需训练全局模型。

对于重叠变量（即同时属于两个相邻因子的变量），其边际分数通过相邻因子条件分数的平均来近似：

$$\nabla \log p(x_i) \approx \frac{1}{2} \left[ \nabla \log p_{y_j}(x_i | \ldots) + \nabla \log p_{y_{j+1}}(x_i | \ldots) \right]$$

这一近似是朴素组合采样的核心，但也正是**模式平均**问题的根源：当两个相邻因子对重叠变量给出不同模式的条件分数时，简单平均会导致生成的样本落入两个模式之间的低概率区域，产生不可行的局部转移。

---

### 核心模块一：基于 DDIM 反演的局部可行性度量与计划剪枝

CDGS 的第一个关键创新是利用 **DDIM 反演曲率** 来近似衡量局部计划的可行性，并据此对候选全局计划进行剪枝。

对于一个局部计划 $y_m^{(0)}$（干净样本），CDGS 通过 DDIM 确定性反演将其映射回噪声空间，反演步为：

$$\frac{y^{(t)}}{\sqrt{\alpha_t}} = \frac{y^{(t-1)}}{\sqrt{\alpha_{t-1}}} + \left(\sqrt{\frac{1-\alpha_t}{\alpha_t}} - \sqrt{\frac{1-\alpha_{t-1}}{\alpha_{t-1}}}\right) \varepsilon_\theta(y^{(t-1)}, t)$$

其中 $\alpha_t$ 为扩散噪声调度参数，$\varepsilon_\theta$ 为预训练的局部扩散模型。反演轨迹的曲率被定义为每一步噪声预测对时间步的变化率：

$$g(y^{(0)}) = \sum_{i=1}^{T} \left\| \frac{\partial \varepsilon_\theta(y^{(i-1)}, i)}{\partial i} \right\|_2$$

**直觉**：若 $y^{(0)}$ 位于局部分布 $p(y)$ 的高概率区域（即是一个可行的局部转移），其 DDIM 反演轨迹应较为平滑，曲率 $g(y^{(0)})$ 较小；反之，若 $y^{(0)}$ 是模式平均产生的不可行样本，反演轨迹会出现剧烈弯曲，曲率较大。因此 $g(\cdot)$ 可作为局部可行性的代理度量。

全局计划的可行性排名度量 $J(\tau^{(0)})$ 由各局部计划曲率的乘积构成：

$$J(\tau^{(0)}) = \prod_{m=1}^M \exp\left(-g\left(y_m^{(0)}\right)\right) = \prod_{m=1}^M \exp\left(-\sum_{i=1}^T \left\| \frac{\partial \varepsilon_\theta(y_m^{(i-1)}, i)}{\partial i} \right\|_2 \right) \tag{5}$$

$J(\tau^{(0)})$ 越大，表示全局计划越可行。在去噪过程中，CDGS 通过修改采样分布来偏向低曲率（高可行性）的计划：

$$p_J(\tau^{(t-1)}|\tau^{(t)}) \propto p(\tau^{(t-1)}|\tau^{(t)}) \exp(-J(\widehat{\tau}_0^{(t-1)})/\lambda_t)$$

其中 $\widehat{\tau}_0^{(t-1)}$ 为从 $\tau^{(t-1)}$ 估计的干净计划（Tweedie 估计），$\lambda_t$ 为温度参数。这一加权机制使得扩散采样过程天然倾向于生成局部可行的计划。

---

### 核心模块二：种群采样与精英剪枝

CDGS 采用基于种群的搜索策略（类似交叉熵方法），维护一批 $B$ 个候选全局计划。在每个去噪时间步中：

1. **排名与剪枝**：对 $B$ 个候选计划计算 $J(\tau^{(0)})$ 排名，保留前 $K$ 个精英计划，丢弃其余低可行性候选。
2. **重新填充**：从保留的精英计划中随机采样，补充至 $B$ 个候选，以维持种群多样性进行探索。

这一机制（**Algorithm 1**）确保在去噪过程中持续淘汰因模式平均产生的不可行计划，同时保持对可行模式序列的充分探索。

---

### 核心模块三：迭代重采样与信息传播

CDGS 的第二个关键创新是在组合分数计算中嵌入 **迭代重采样**，以增强局部-全局信息传递。在每次去噪步中，**ComposedScore** 模块（**Algorithm 2**）执行 $U$ 次重采样循环：

1. 使用当前组合分数执行一次去噪，得到 $\tau^{(t-1)}$。
2. 对 $\tau^{(t-1)}$ 进行前向加噪，得到 $\tau^{(t)}$。
3. 重复上述过程 $U$ 次。

每次重采样时，重叠变量的分数通过相邻因子的条件分数平均计算，使得一个局部计划的信息可以通过重叠区域传递到相邻局部计划，进而通过多次迭代传播到更远的片段。这一机制解决了朴素组合采样中长距离依赖无法有效传递的问题。

**目标修复**（Goal Inpainting）在 ComposedScore 中强制实施起点和终点约束（Algorithm 2, Line 6-7），确保生成的计划满足给定的目标条件。

---

### 模块协同与模式平均的消除

三个核心模块的协同机制如下（参见 **Figure 4**）：

- **迭代重采样**（蓝色部分）在每个去噪时间步通过重叠区域的分数平均传递局部-全局信息，减少跨片段的不一致性。
- **基于 DDIM 曲率的剪枝**（黄色部分）在每个去噪时间步评估各候选计划的局部可行性，剔除因模式平均产生的不可行转移。
- **种群搜索** 维持一批候选计划，在剪枝后重新填充以保持探索能力，避免过早收敛到次优模式序列。

这一设计使得 CDGS 能够从多模态的局部计划分布中采样出全局连贯的长视界计划，而朴素组合方法（如 **GSC**, Mishra et al., CoRL 2023）则因缺乏搜索和剪枝机制，在局部多模态场景下会因模式平均产生不可行计划（**Figure 3 (b)** 对比 **Figure 3 (d)**）。

## 实验与关键发现

### 核心瓶颈验证：模式平均如何导致计划失败

CDGS的核心动机源于组合扩散中的一个根本性问题——**模式平均**（mode averaging）。当局部因子分布呈现多模态时，朴素组合采样（如GSC）会不加区分地从不同模态中混合采样，导致对不兼容的局部模式进行平均。这种平均化的结果产生两类典型失败模式（Figure 5左）：


- **不可行转移**：例如，`place(hook)` 操作要求前置条件 `inhand(hook)` 满足，但若上游计划选择了不抓取钩子的模态，则下游操作的前提条件永远无法满足，导致转移在物理上不可执行。
- **状态幻觉**：在组合评分过程中，为了同时满足来自不同模态的约束，扩散过程会生成处于分布之外的中间状态。例如，立方体在几何上不可能穿越架子，但模式平均会迫使它“穿过”架子以趋近目标状态。

这些失败模式在朴素组合中系统性出现（Figure 3b），而CDGS通过**迭代重采样**（减少模式平均频率，Figure 3c）和**基于似然的剪枝**（直接消除包含不可行转移的计划，Figure 3d）两个机制将其消除。

### 主实验结果

#### 长视界运动规划（OGBench Maze与Scene任务）

在OGBench的Stitch和Play数据集上，CDGS仅需极少的训练数据（短视界片段），即可在滚动视界控制中达到与逆强化学习基线相当甚至更优的性能（Table 1）。关键结果：

- **PointMaze Giant**：CDGS达到 **87±3%** 成功率，而朴素组合基线GSC仅为29±2%，提升**+58个百分点**。这表明在大型迷宫中，搜索和剪枝对于找到可行路径至关重要。
- **AntMaze Giant**：CDGS达到 **85±3%**，远超离线目标条件RL基线HIQL的21±2%（+64个百分点），证明了组合扩散加引导搜索在稀疏奖励长视界任务上的优势。
- **HumanoidMaze Giant**：CDGS为55±3%，虽然绝对数值下降，但仍显著优于生成式基线GSC（0±0）和CompDiffuser（0±0），体现了方法在高维复杂动力学下的鲁棒性。
- **Scene任务**：CDGS达到51±2%，与逆RL方法（HIQL 55±3）接近，远优于GSC（13±2）。

#### 高维组合任务（AntSoccer）

在17维状态空间的AntSoccer组合任务中（Table 2），CDGS在Arena环境达到 **69±1%**，略优于GSC（65±3%）和CompDiffuser（65±3%）。在更困难的Medium环境，CDGS为18±2%，与GSC（12±2%）和CompDiffuser（11±2%）相比仍有提升。高维空间中模式平均问题更为严重，CDGS的剪枝机制在此场景下尤为关键。

#### 任务与运动规划（TAMP）

在TAMP任务集上（Table 3），CDGS与基于搜索（PDDL Domain）和基于提示（LLM/VLM）的方法进行了对比：

![[assets/figures/papers/paper_list_l28_https_openreview_net_forum_id_b8avf4F2hn/figures/011_Table_3.jpg]]
*Table 3: Evaluation on TAMP task-suite. We compare CDGS with relevant search-based (PDDL Domain) and prompting based (LLM/VLM) baselines. CDGS performs on-par or slightly trails privileged methods on Hook Reach and Rearrangement Push, but substantially outperforms them on Rearrangement Memory. (success rate over 50 trials)*

- **Hook Reach和Rearrangement Push**：CDGS与特权方法（如STAP CEM）性能相当或略低，表明在较短视界或较简单约束下，搜索引导的优势相对有限。
- **Rearrangement Memory**：CDGS在Task 1达到 **0.42** 成功率，而GSC（无任务规划）仅为0.07，提升**+0.35**。该任务需要在执行当前操作时记忆并满足后续操作的前置条件，CDGS的迭代重采样机制通过重叠变量在局部计划间传递长距离依赖信息，是性能提升的关键。

#### 全景图像生成

在全景图生成任务中（Table 4，Figure 6），CDGS在三个维度上展现了平衡的性能：

![[assets/figures/papers/paper_list_l28_https_openreview_net_forum_id_b8avf4F2hn/figures/017_Figure_6.jpg]]
*Figure 6: Panorama image generation. The above figure shows the qualitative comparison of CDGS with MD and SD. We show qualitative intuition behind global coherence and local feasibility: while SD generates smooth panoramas, they fail to satisfy the global context (mountain peak with skiers), on the other hand, MD follows the global context (beach in La La Land style) but fails to exhibit local consistency. CDGS excels at both. Table 4: Quantitative comparison of panorama generation. We generate 1000 panoramas of dimensions 512 ⇐ 4608 using 14 prompts and compare different methods based on their perceptual similarity (LPIPS), style similarity (Style-loss), and prompt alignment (CLI...*

- **感知相似度**（Intra-LPIPS↓）：CDGS为0.59，与Sync-Diffusion（0.55）接近，优于Multi-Diffusion（0.63）。
- **风格相似度**（Intra-Style-L↓）：CDGS为 **1.38**，显著优于Sync-Diffusion（1.89）和Multi-Diffusion（1.77）。
- **提示对齐度**（Mean-CLIP-S↑）：CDGS为 **32.51**，优于Sync-Diffusion（30.89）和Multi-Diffusion（31.81）。

定性分析（Figure 6）揭示了各方法的本质差异：Sync-Diffusion生成平滑的全景图但无法满足全局上下文（如山峰上应有滑雪者），Multi-Diffusion遵循全局上下文但局部一致性差。CDGS通过剪枝保留局部可行、全局连贯的计划，同时实现了局部一致性和全局连贯性。

#### 长视频生成

在350帧（7倍于基线生成能力）的长视频生成中（Table 5），CDGS保持了有竞争力的质量：

![[assets/figures/papers/paper_list_l28_https_openreview_net_forum_id_b8avf4F2hn/figures/018_Table_5.jpg]]
*Table 5: Quantitative comparison of long-video generation. We evaluate the performance of CDGS based on selected metrics from VBench that measure subject consistency, aesthetics, prompt alignment and temporal artifacts. We use 6 prompts (refer App. B) and generate videos with 350 frames at 720p resolution. CDGS achieves competitive video quality but for significantly (7x) extended horizons*

- **主体一致性**：CDGS达到 **91.67**，与CogVideoX-2B（50帧，91.65）相当，显著优于CogVideoX-2B（350帧，85.98）和GSC（350帧，87.67）。
- **时间闪烁度**：CDGS为 **97.16**，与CogVideoX-2B（50帧，97.32）接近，优于GSC（96.94）。
- **美学质量**：CDGS为58.90，略低于CogVideoX-2B（50帧，60.82），但高于GSC（56.11）。

Figure 7的定性对比显示，完整的CDGS（w/ PR）保持了主体外观的一致性，而移除规划细化（w/o PR）的版本出现了明显的模式平均现象——主体外观在视频中发生剧烈变化。

### 消融实验

#### 规划细化（PR）的必要性

在所有实验设置中，移除规划细化（CDGS w/o PR）均导致性能下降：

- **OGBench Maze**（Table 1）：在PointMaze Giant上，w/o PR版本成功率显著低于完整CDGS（具体数值需查阅原表）。
- **全景图生成**（Table 4）：w/o PR版本的Intra-LPIPS为0.61（vs 完整版0.59），Mean-CLIP-S为32.07（vs 32.51）。
- **长视频生成**（Table 5）：w/o PR版本的主体一致性降至89.41（vs 91.67），时间闪烁度降至96.82（vs 97.16）。

![[assets/figures/papers/paper_list_l28_https_openreview_net_forum_id_b8avf4F2hn/figures/010_Table_1.jpg]]
*Table 1: OGbench: learning from stitch and play datasets. With much less training data requirements, CDGS performs on-par with inverse-reinforcement learning baselines and better than generative baselines in a receding horizon control. For GSC, CD and CDGS, we replan based on distance from goal for maze tasks (following CD) and sample the complete plan based on the oracle planning horizon for scene task. Success rate averaged over 100 trials and 3 seeds with randomly chosen task ids. Baseline performance is borrowed from original papers. Table 2: Stitching composite task AntSoccer in OGBench. We evaluate CDGS on highdimensional (17D) state space to stitch ball reaching and bal...*

这些结果一致表明，基于DDIM反演曲率的似然剪枝是消除模式平均、保证计划全局连贯性的关键组件。

#### 计算资源的可扩展性

CDGS的性能随推理计算量平滑扩展（Figure 5右）：

- **批次大小B**：增大B可提高任务规划成功率（Figure 5c），但仅当配合足够的重采样步数U时效果才显著。这表明更大的种群提供了更多样的候选模式序列，但需要通过迭代重采样来有效传递信息。
- **重采样步数U**：增大U可提高运动规划成功率（Figure 5d），但需要足够大的批次大小才能发挥作用。更多的重采样步数增强了局部-全局信息传递，但若种群过小，即使信息传递充分也难以覆盖足够的模态组合。
- **视界长度影响**：在视界为7的任务上（H-7），CDGS的性能优势更为明显，验证了方法在长视界场景下的核心价值。

### 失败模式与局限性

尽管CDGS在多个领域展现了显著优势，但仍存在以下局限：

1. **目标依赖性**：当前方法假设目标状态是预先指定的。对于无目标或目标未知的场景，需要扩展至目标生成或分类器引导机制。
2. **固定视界假设**：规划过程假设固定的视界长度。虽然可通过重用相同起止条件处理不同视界，但动态调整视界的能力仍有待探索。
3. **长距离依赖传递**：信息传递仅通过相邻片段之间的分数平均和重采样实现，可能无法捕捉远距离强依赖。引入注意力机制或更复杂的消息传递方案可能进一步提升性能。

### 公平性说明

所有机器人规划实验均基于100次试验和3个随机种子进行成功率评估，基线性能直接采用原始论文报告的值（如OGBench、CompDiffuser、HIQL等），确保了比较的公平性。图像和视频生成实验使用相同的预训练扩散模型和提示词，评估指标为领域标准（LPIPS、Style-loss、CLIP score、VBench）。

## 定位与知识库关联

### 问题定位：组合生成中的模式平均瓶颈

CDGS 瞄准的核心瓶颈是**组合多模态性**（compositional multimodality）问题：当长视界规划被分解为多个局部因子分布的组合时，每个局部因子可能包含多个可行模式（例如绕过障碍物的上方路径和下方路径），而朴素组合采样在重叠变量处对不兼容的模式进行平均，产生既不属于上方也不属于下方路径的“模式平均”伪影，导致局部转移不可行或全局计划不连贯（Figure 3b）。这一瓶颈并非扩散模型独有，而是任何基于因子图乘积近似联合分布的组合生成方法的固有缺陷。

### 与组合扩散方法的谱系关系

**朴素组合扩散基线**：**Generative Skill Chaining (GSC)**（Mishra et al., CoRL 2023）和 **CompDiffuser (CD)**（Luo et al., arXiv 2025）代表了组合扩散的第一代方法。它们基于 Bethe 近似将联合分布分解为因子乘积（Eq. 1），并通过求和局部扩散分数进行采样（Eq. 3）。然而，这些方法在重叠变量处仅执行一次分数平均，缺乏跨片段的信息传递机制，因此在面对多模态局部分布时不可避免地陷入模式平均。实验表明，GSC 在 OGBench PointMaze Giant 任务上仅取得 29±2% 成功率，而 CDGS 达到 87±3%（Table 1），差距高达 58 个百分点。

**同步联合扩散方法**：在全景图像生成领域，**Sync-Diffusion (SD)**（Lee et al., NeurIPS 2023）通过同步联合去噪维持全局一致性，但其联合采样策略本质上仍假设单模态重叠，无法主动探索和筛选多模态组合。**Multi-Diffusion (MD)**（Bar-Tal et al., 2023）则通过融合多个去噪结果实现局部一致性，但缺乏全局上下文的传递机制。CDGS 在感知相似度上与 SD 持平（Intra-LPIPS 0.59 vs 0.55），同时在风格相似度和提示对齐度上显著优于两者（Table 4），证明了显式搜索对全局-局部权衡的改进。

**视频生成扩展**：在长视频生成中，**CogVideoX-2B**（Yang et al., arXiv 2024）作为大规模文本到视频扩散模型，在 50 帧的标准视界上表现优异，但在 7 倍扩展视界（350 帧）上主体一致性从 91.65 下降至 85.98。CDGS 通过组合短片段扩散模型并在重叠帧处执行引导搜索，在 350 帧上维持了 91.67 的主体一致性（Table 5），证明了组合搜索策略对视界扩展的有效性。

### 与强化学习和规划方法的边界

**逆强化学习基线**：CDGS 在 OGBench Maze 任务上与 **HIQL**（Park et al., NeurIPS 2023）等逆强化学习方法表现相当或更优（Table 1），但 CDGS 仅需来自“stitch and play”数据集的短视界片段训练，无需完整轨迹演示或在线交互，训练数据需求显著更低。这一边界表明，当局部技能模型可从离线数据中充分学习时，组合扩散加搜索可以替代逆强化学习的奖励推断过程。

**任务与运动规划（TAMP）基线**：在 TAMP 任务集上，CDGS 与基于搜索的方法（PDDL Domain + CEM）和基于提示的方法（LLM/VLM-T2M）进行了对比（Table 3）。在 Hook Reach 和 Rearrangement Push 任务上，CDGS 与特权方法（可访问真实状态和动力学）表现持平或略逊；但在 Rearrangement Memory 任务上，CDGS 以 0.42 的成功率大幅超越 GSC 的 0.07 和基于提示方法的 0.00。这一差异揭示了 CDGS 的核心优势：当任务需要长距离记忆和精确的局部可行性判断时，扩散模型反演曲率提供的似然信号比符号搜索或语言推理更可靠。

### 核心机制创新：搜索嵌入去噪过程

CDGS 的方法论贡献在于将**基于种群的引导搜索**直接嵌入扩散去噪循环，形成三个相互增强的机制：

1. **迭代重采样**（Algorithm 2）：在每次去噪步中，通过反复前向加噪和反向去噪（共 U 步），使重叠变量处的分数平均能够传递跨片段信息。这实质上是利用扩散过程的随机性进行局部-全局消息传递，其效果随重采样步数 U 增加而单调提升（Figure 5c-d）。

2. **基于 DDIM 反演曲率的剪枝**（Eq. 5）：通过对每个局部计划进行 DDIM 反演并计算路径曲率 $g(y^{(0)}) = \sum_{i=1}^{T} \|\frac{\partial \varepsilon_\theta(y^{(i-1)}, i)}{\partial i}\|_2$，近似衡量局部计划的对数似然。曲率越低，表明该局部计划越接近扩散模型训练分布的高密度区域，即可行性越高。全局计划的可行性度量 $J(\tau^{(0)})$ 为各局部曲率的乘积，用于精英选择。

3. **种群采样与精英保留**（Algorithm 1）：维护 B 个候选全局计划，根据 $J(\tau^{(0)})$ 排名保留精英，并从精英中重新采样填充种群。这一策略类似于交叉熵方法（CEM），但搜索空间由扩散模型的分数场引导，而非随机扰动。

消融实验证实，移除规划细化（即剪枝步骤）会导致性能显著下降（Table 1 中“Ours w/o PR” vs “Ours”），而增加批次大小 B 和重采样步数 U 可平滑提升成功率（Figure 5c-d），验证了搜索计算量与性能之间的可扩展关系。

### 适用边界与局限

**已知适用条件**：
- 需预先指定目标状态，依赖目标修复（goal inpainting）强制实施起止约束
- 假设固定规划视界，尽管可通过重用相同起止条件处理不同视界
- 局部扩散模型需在重叠区域有足够的上下文窗口以支持分数平均

**已验证的应用领域**：
- 机器人长视界运动规划（OGBench Maze, AntSoccer, TAMP）
- 全景图像生成（512×4608 分辨率）
- 长视频生成（350 帧，720p）

**已知局限**：
- 长距离依赖仅通过相邻片段之间的分数平均和重采样传递，可能无法捕捉远距离强依赖（如全局约束需要所有片段同时满足的条件）
- 当前方法依赖预先指定的目标状态，对无目标场景需要扩展至目标生成或分类器引导
- 计算成本随批次大小 B 和重采样步数 U 线性增长，在实时应用中需要权衡

### 开放问题

1. **目标生成与条件扩展**：CDGS 能否与分类器引导或目标生成方法结合，处理无预指定目标的开放式规划任务？这需要将当前的目标修复机制扩展为可优化的目标变量。

2. **消息传递机制的增强**：当前的迭代重采样本质上是一种通过随机采样实现的简单消息传递。更复杂的注意力机制或图神经网络消息传递能否进一步提升长距离依赖的传播效率，同时降低所需的重采样步数？

3. **跨领域迁移**：CDGS 的组合搜索框架是否可应用于其他需要序列决策的领域，如自然语言规划（将句子级生成组合为段落）、蛋白质序列设计（将局部结构模块组合为全局折叠）？这些领域的局部可行性度量需要重新定义。

4. **理论分析**：DDIM 反演曲率作为局部可行性度量的理论保证尚未建立。该度量在什么条件下与真实似然单调相关？是否存在反例导致剪枝错误地丢弃可行计划？

## 原文 PDF

![[paperPDFs/ICLR_2026/Compositional_Diffusion_with_Guided_search_for_Long_Horizon_Planning.pdf]]
