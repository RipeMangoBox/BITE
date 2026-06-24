---
title: "A Genetic Algorithm for Navigating Synthesizable Molecular Spaces"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/A_Genetic_Algorithm_for_Navigating_Synthesizable_Molecular_Spaces.pdf
aliases:
- GANSMS
- SynGA
tags:
- ICLR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/chemistry_and_drug_discovery
core_operator: "通过设计直接操作于合成路线的自定义遗传算子（交叉与变异），将合成约束内嵌于生成过程本身，从而保证所有生成分子天然具有可合成性。"
primary_logic: "将遗传算法直接定义在合成树上，利用模板反应和可购买砌块，通过片段融合（交叉）和局部扰动（变异）在可合成空间中高效搜索，无需依赖任何机器学习模型即可保证合成可行性。"
claims:
- "SynGA 通过自定义交叉和变异算子显式约束在可合成分子空间内。"
- "SynGA 是轻量级且无 ML 的，可作为基线或子模块使用。"
- "SynGA 在多种优化任务上达到或超越最先进水平。"
- "ChEMBL 类似物搜索 上 Morgan 相似度 = 0.711 (SynGA MLP)"
---

# A Genetic Algorithm for Navigating Synthesizable Molecular Spaces

> [!tip] 核心洞察
> 将遗传算法直接定义在合成树上，利用模板反应和可购买砌块，通过片段融合（交叉）和局部扰动（变异）在可合成空间中高效搜索，无需依赖任何机器学习模型即可保证合成可行性。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 一种用于导航可合成分子空间的遗传算法 |
| 英文题名 | A Genetic Algorithm for Navigating Synthesizable Molecular Spaces |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=OvMtGGaFUT); [GitHub](https://github.com/alstonlo/synga) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/chemistry_and_drug_discovery |
| Method | SynGA |
| Dataset | ChEMBL 类似物搜索, PMO 套件 (22 任务) |

> [!tip] 效果简介
> - ChEMBL 类似物搜索 上，Morgan 相似度 为 0.711 (SynGA MLP)，对比 0.459 (无过滤)，变化 +0.252。
> - ChEMBL 类似物搜索 上，Scaffold 相似度 为 0.694 (SynGA MLP)，对比 0.526 (无过滤)，变化 +0.168。
> - ChEMBL 类似物搜索 上，Gobbi 相似度 为 0.623 (SynGA MLP)，对比 0.400 (无过滤)，变化 +0.223。

## 概述

现有分子生成模型普遍面临一个瓶颈：生成的分子虽然理论上性质优异，但往往难以合成或化学不稳定。事后通过逆合成模型进行“投影”修正虽能缓解此问题，却引入了高昂的计算开销。针对这一矛盾，本文提出 SynGA，一种直接操作于合成路线的轻量级遗传算法。其核心思路是将合成可行性约束通过自定义的遗传算子（交叉与变异）内嵌于生成过程本身，从而确保所有生成的分子天然具有可合成性，无需依赖任何机器学习模型来事后保证。

SynGA 将分子表示为合成树——一种无序二叉树，其叶子节点为可购买的砌块，内部节点为反应模板。交叉算子通过枚举两棵父树的子树，寻找兼容双分子反应的子树对并以新反应根节点融合；变异算子则随机执行 Grow、Shrink、Rerun、Change internal 或 Change leaf 五种局部扰动之一。这种设计使 SynGA 在搜索过程中始终约束在可合成分子空间内。为进一步提升效率，论文还引入了可选的 ML 增强模块：对于类似物搜索，训练 MLP 分类器预测砌块相关性以过滤无关砌块；对于性质优化，训练神经加性模型 (NAM) 预测砌块对目标性质的贡献，并进一步与高斯过程代理结合形成 SynGBO 变体，在贝叶斯优化框架中运行。

实验结果表明，SynGA 在多个基准测试中达到或超越了当前最先进的合成感知方法。在 ChEMBL 类似物搜索中，SynGA 配合 MLP 过滤在 Morgan、Scaffold 和 Gobbi 相似度上分别达到 0.711、0.694 和 0.623，显著优于无过滤基线（0.459、0.526、0.400）。在 PMO 套件的 22 个性质优化任务上，SynGBO 的 Top-10 AUC 总和为 16.426，优于 SynGA 的 13.366 并与无约束算法竞争。在 LIT-PCBA 对接任务中，SynGBO 在仅使用 16,000 次 oracle 调用（基线方法通常使用 64,000 次）的情况下，平均 Vina 对接分数达到 -11.11，优于 SynGA 的 -10.80 并接近 3DSynthFlow 等 3D 感知方法。

然而，SynGA 继承了基于模板方法的固有局限：模板不保证合成可行性，不考虑反应条件、立体化学、产率或成本；固定的模板库将探索限制在可合成空间的一个有偏子集内。此外，SynGA 在类似物搜索中比 SynFormer 慢 3 倍以上，且在 PMO 基准测试中落后于无约束算法（如 GraphGA、STONED），表明合成约束本身可能限制了搜索空间。这些局限指向了未来改进的关键方向。

## 背景与动机

分子生成是药物发现的核心环节，但现有方法普遍面临“可合成性”这一瓶颈。传统分子生成模型（如基于 SMILES 或分子图的遗传算法、强化学习方法）通常只优化目标性质（如对接分数、类药性），而完全忽略分子能否被实际合成。生成的分子往往结构复杂、含有不稳定官能团或需要多步无法实现的反应路径，导致虚拟筛选出的候选分子无法进入湿实验验证。

为解决这一问题，现有工作发展了两类合成感知策略。第一类是**事后投影**方法，如 SynNet、ChemProjector、SynthesisNet：先生成任意分子，再通过逆合成模型将其“投影”到可合成空间。这类方法的根本缺陷在于计算成本高昂——每次投影都需要运行完整的逆合成搜索，且投影过程可能严重扭曲原始分子的性质。第二类是**内嵌约束**方法，如 SynFormer、SynFlowNet、RGFN、RxnFlow、3DSynthFlow、BBAR，它们将合成可行性作为生成过程的一部分（例如通过模板反应或流匹配）。然而，这些方法普遍依赖复杂的机器学习模型（如 GFlowNet、Transformer、流匹配），训练开销大、可解释性差，且难以作为轻量级基线或子模块集成到更大的算法框架中。

本文的动机在于：能否设计一种**无需任何机器学习模型**、**天然保证合成可行性**、且**计算轻量**的分子优化方法？作者提出的 SynGA 给出了肯定答案。其核心洞察是：将遗传算法直接定义在**合成树**上——每个个体不再是一个分子 SMILES 串，而是一棵完整的合成路线树（内部节点为反应模板，叶子节点为可购买砌块）。通过设计专门针对合成树的交叉算子（枚举两棵父树的子树，找到兼容双分子反应的子树对，以新反应根节点融合）和变异算子（Grow、Shrink、Rerun、Change internal、Change leaf 五种局部扰动），SynGA 将合成可行性从“事后检查”变为“天然内嵌”——所有生成个体天然对应一条有效的合成路线，无需任何逆合成投影或可行性预测。

这一思路的关键优势在于：合成约束不再是一个额外的惩罚项或后处理步骤，而是搜索空间本身的定义。SynGA 的搜索空间 $\tau \to \mathcal{M}_S$ 是一个从合成树集合到可合成分子空间的满射，遗传算子在该空间上的任何操作都保证输出仍属于该空间。这使得 SynGA 既可作为独立优化器，也可作为轻量级基线或子模块（如与贝叶斯优化结合形成 SynGBO）服务于更复杂的算法。

## 核心创新

SynGA 的核心瓶颈在于现有分子生成方法普遍将合成可行性作为事后约束（如 SynNet、ChemProjector 的投影机制），而非内嵌于生成过程。这导致生成的分子要么合成不可行，要么需要昂贵的逆合成投影步骤。

**核心因果旋钮**：将遗传算法直接定义在合成树上，通过自定义的交叉与变异算子，使合成可行性成为生成过程的固有属性，而非事后修正。

**关键变更槽位**：
- **分子表示**：从 SMILES / SELFIES / 分子图（baseline）切换为**合成树**（无序二叉树，节点为砌块或反应模板）。这一表示变更直接改变了搜索空间的结构——从化学字符串/图空间变为合成路线空间。
- **合成可行性保证方式**：从事后投影（如 SynNet）或启发式奖励（baseline）切换为**通过自定义遗传算子内嵌约束，天然保证**（“Our method features custom crossover and mutation operators that explicitly constrain it to synthesizable molecular space”）。这意味着 SynGA 无需额外模型即可保证 100% 有效性。
- **交叉算子**：从 SMILES 字符串交叉 / 图子结构交叉（baseline）切换为**枚举两棵父树的子树，找到兼容双分子反应的子树对，以新反应根节点融合**。这一设计确保了子代合成树的根节点始终是一个有效的双分子反应，从而维持合成可行性。
- **变异算子**：从 SMILES 随机替换 / 图边扰动（baseline）切换为**五种操作：Grow、Shrink、Rerun、Change internal、Change leaf**。这些操作均被限制在合成树的结构约束内，保证了局部扰动不会破坏合成可行性。
- **砌块过滤（ML 增强）**：从无过滤或基于相似度的启发式过滤（baseline）切换为**训练二元分类器 πθ 预测砌块是否可用于生成类似物（模拟搜索），或训练神经加性模型 (NAM) 预测砌块对性质的贡献（性质优化）**。这是 SynGA 中唯一的 ML 组件，作为可选增强模块而非核心机制。

**核心洞察**：SynGA 的核心创新在于将遗传算法直接定义在合成树上，利用模板反应和可购买砌块，通过片段融合（交叉）和局部扰动（变异）在可合成空间中高效搜索。由于所有遗传操作均被限制在合成树的结构约束内，SynGA 天然保证合成可行性，无需依赖任何机器学习模型。这种“无 ML”的特性使其成为一个轻量级基线（“SynGA is simple and ML-free, which makes it a nice baseline and subroutine for future algorithms”），同时可通过可选的 ML 砌块过滤进一步增强。

**证据强度**：上述变更槽位的置信度均为 1.0，有明确的原文锚点支撑。核心洞察中的“无 ML 保证合成可行性”和“可作为基线/子模块”的 claims 置信度均为 1.0。

## 整体框架

![[assets/figures/papers/iclr26_0002_OvMtGGaFUT_A_Genetic_Algorithm_for_Navigating_Synthesizable/figures/001_Figure_1.jpg]]
*Figure 1: A graphical overview of SynGA, which operates over synthesis trees built from building blocks (squares) and reaction templates (circles). Example blocks and a reaction are drawn above using SmilesDrawer (Probst & Reymond, 2018)*

SynGA 的核心设计是将遗传算法直接定义在合成树上，而非分子字符串或图上，从而在生成过程中天然保证所有候选分子的可合成性。其整体 pipeline 由以下模块构成，形成一条从砌块到优化分子的闭环搜索流程：

**1. 砌块集预处理与反应模板库**  
从 Enamine 砌块目录出发，经过去重和模板兼容性过滤，得到 196,907 个可用砌块。反应模板库由专家定义的 SMARTS 字符串实现，支持单分子和双分子反应。这一基础组件决定了搜索空间的上限——任何固定模板库必然将探索限制在可合成空间的一个有偏子集内。

**2. 种群初始化**  
通过反复对随机砌块应用 Grow 操作生成初始合成树种群。Grow 是变异操作之一，其核心是在合成树末端添加新层（新砌块+新反应），因此初始种群天然是合法的合成路线。

**3. 适应度评估**  
根据任务类型设定目标函数：对于性质优化，直接使用待优化性质 ρ 作为适应度；对于类似物搜索，则使用与查询分子的某种相似度度量（如 Morgan 指纹 Tanimoto 相似度）。适应度是驱动搜索的唯一信号。

**4. 选择**  
采用精英选择策略，仅保留父代和子代中适应度最高的个体。选择概率通过逆序采样（inverse-rank sampling）实现，参数 ε=0.1 控制采样集中度，使得排名靠前的个体被抽中的概率近似反比于其排名。

**5. 交叉算子**  
这是 SynGA 的关键创新：枚举两棵父树的所有子树对，找到能够通过双分子模板反应兼容的子树对（S₁, S₂），然后以一个新的反应根节点将它们融合。这一操作直接操作于合成路线而非分子结构，因此子代天然可合成。

**6. 变异算子**  
随机执行五种操作之一：Grow（添加新层）、Shrink（移除最外层）、Rerun（重新运行根反应）、Change internal（替换内部砌块）、Change leaf（替换叶节点砌块）。其中 Grow 和 Shrink 被选中的概率为 0.125，其余三种为 0.25。这一组操作覆盖了合成树的局部扰动和结构变化。

**7. 砌块过滤（可选 ML 增强模块）**  
这是 SynGA 的轻量级 ML 补充，并非必需但显著提升效率。对于类似物搜索，训练一个 MLP 二元分类器 π_θ 预测砌块是否可用于生成与查询分子类似的产物；对于性质优化，训练一个神经加性模型（NAM）预测每个砌块对目标性质的贡献。过滤后的砌块集大小大幅缩减，从而加速搜索。

**8. SynGBO（模型增强变体）**  
将 SynGA 与 NAM 过滤和 GP 代理模型整合到贝叶斯优化框架中。在每次外循环迭代中，先用 NAM 过滤砌块，然后在内循环中运行 SynGA 搜索，最后用 GP 代理对候选分子进行排序。这一变体在 PMO 基准测试中达到了与无约束算法竞争的性能。

整个 pipeline 的输入是砌块集和反应模板库，输出是一系列可合成的分子及其对应的合成路线。SynGA 不需要任何预训练的机器学习模型即可运行，这使得它既可作为独立算法使用，也可作为更复杂系统的子模块或基线。值得注意的是，SynGA 在类似物搜索中比 SynFormer 慢 3 倍以上，但通过砌块过滤可以显著缩小这一差距。

## 核心模块与公式推导

SynGA 的核心在于将遗传算法直接定义在合成树上，通过自定义的交叉和变异算子，将合成可行性约束内嵌于搜索过程本身。其分子表示、算子设计和可选的机器学习增强模块共同构成了该方法的技术骨架。

### 分子表示：合成树

SynGA 摒弃了 SMILES、SELFIES 或分子图等传统表示，转而使用**合成树**（synthesis tree）作为个体的基本表示形式。合成树是一棵无序二叉树，其叶子节点为可购买的砌块（building block），内部节点为专家定义的模板反应（reaction template）。合成树内部节点的分子定义如下：

$$M_v \in R_v(\{M_w \mid w \text{ is a child of } v\})$$

其中，$M_v$ 表示内部节点 $v$ 处的分子，它是其子节点经过反应 $R_v$ 后的产物。合成树集合到可合成分子空间 $\mathcal{M}_S$ 之间存在满射：

$$\tau \to \mathcal{M}_S$$

这意味着每个合成树都唯一对应一个可合成分子，但一个分子可能对应多个不同的合成树（即多条合成路线）。这种表示方式天然地将合成可行性编码到搜索空间中。

### 遗传算子

SynGA 设计了专门操作于合成树的交叉和变异算子，确保所有生成个体始终位于可合成分子空间内。

**交叉算子**：给定两棵父树，交叉操作枚举它们的子树对 $(S_1, S_2)$，寻找与双分子反应模板兼容的子树对。若找到，则以一个新的反应根节点将 $S_1$ 和 $S_2$ 融合，生成子代。该操作本质上是将两棵父树中可发生反应的子结构片段进行重组。

**变异算子**：变异操作随机执行以下五种操作之一：
- **Grow**：在合成树的任意节点处，通过一个随机反应模板连接一个新的砌块。
- **Shrink**：移除合成树的一个内部节点及其子节点，将其替换为一个砌块。
- **Rerun**：重新运行合成树根节点处的反应，使用不同的砌块组合。
- **Change internal**：替换合成树中一个内部节点的反应模板。
- **Change leaf**：替换合成树中一个叶子节点的砌块。

在默认配置中，Grow 和 Shrink 的选择概率为 0.125，其余三种操作的概率各为 0.25。这些算子共同构成了在可合成空间中进行局部搜索和全局探索的基本操作集。

### 适应度评估与选择

适应度函数 $f$ 根据任务定义：
- **性质优化**：直接设定 $f = \rho$，其中 $\rho$ 是待优化的性质（如 QED、对接分数等）。
- **类似物搜索**：$f$ 定义为查询分子与候选分子之间的某种相似度度量，如 Tanimoto 相似度。

选择策略采用**精英选择**（elitist selection），即从父代和子代中共同保留适应度最高的个体，保证种群质量不会退化。

### 机器学习增强：砌块过滤

为了提升搜索效率，SynGA 引入了可选的机器学习模块进行砌块过滤，分为两种场景：

**类似物搜索**：训练一个 MLP 二元分类器 $\pi_\theta$，预测给定砌块是否可用于生成与查询分子相似的类似物。该分类器在数百万条合成路线上训练，用于在遗传算法运行前过滤掉无关砌块。

**性质优化**：训练一个**神经加性模型**（Neural Additive Model, NAM）来预测砌块对目标性质的贡献。NAM 的预测公式为：

$$\rho_\theta(\mathcal{B}_M) = \big( \alpha + (1 - \alpha) |\mathcal{B}_M|^{-1} \big) \sum_{B \in \mathcal{B}_M} s_\theta(B)$$

其中，$\mathcal{B}_M$ 是分子 $M$ 所用砌块的集合，$s_\theta(B)$ 是砌块 $B$ 的得分函数，$\alpha \in [0, 1]$ 是一个插值参数，控制模型在求和与均值之间的平衡。该模型通过 RankNet 损失进行训练：

$$\mathcal{L}(\theta) = \mathrm{BCE}\bigg( \rho_\theta(\mathcal{B}_1) - \rho_\theta(\mathcal{B}_2), \mathbb{I}\left[\rho(M_1) > \rho(M_2)\right] \bigg)$$

即基于分子性质分数排序对的二元交叉熵损失。实验表明，排名损失优于标准的均方误差损失。经过 NAM 过滤后的砌块集用于引导遗传算法向高性质区域搜索，该模块与高斯过程代理模型结合后构成 SynGBO 变体。

## 实验与分析

### 主结果：类似物搜索与投影任务

**ChEMBL 类似物搜索。** 在 1,000 个 ChEMBL 分子的类似物搜索任务中，SynGA 结合 MLP 砌块过滤（SynGA MLP）在 Morgan、Scaffold 和 Gobbi 三种相似度指标上均显著优于所有基线方法（Table 2）。SynGA MLP 的 Morgan 相似度为 0.711，而最强的基线方法 SynFormer 为 0.629，基于投影的方法 SynNet 仅为 0.437。SynGA 的 Scaffold 相似度（0.694）和 Gobbi 相似度（0.623）同样领先。值得注意的是，SynGA 在 ChEMBL 上的重建率（RR）为 0.196，远低于 SynFormer（0.628），说明 SynGA 更倾向于探索而非精确重建。SynGA 的耗时（250 分钟）约为 SynFormer（72 分钟）的 3.5 倍，但 SynGA 天然保证 100% 有效性，而 SynFormer 的有效性为 0.964。


![[assets/figures/papers/iclr26_0002_OvMtGGaFUT_A_Genetic_Algorithm_for_Navigating_Synthesizable/figures/003_Table_2.jpg]]
*Table 2: Average similarity scores between 1k molecules from ChEMBL and their proposed analogs. Results for SynNet and ChemProjector are taken from Luo et al. (2024). SynthesisNet and SynFormer results were reproduced with their default parameters, and we use the non-MCMC version (τ in their paper) for SynthesisNet due to compute limitations*

**投影任务。** 在将生成模型设计的分子投影到可合成空间的 6 个任务上（Table 3），SynGA MLP 在大多数任务上取得了与 SynFormer 相当的相似度（Sim.），并在某些任务上实现了更高的 Δ（投影后分数提升）。例如，在 ALDH1 任务上，SynGA MLP 的 Δ 为 0.302，而 SynFormer 为 0.095。SynGA 在所有任务上均保持 100% 有效性，而 SynFormer 的有效性在 0.909 到 0.979 之间。SynGA 在 DDS-10 和 ZINC 数据集上的性能低于 SynFormer（Table 9），但在 ChEMBL 上反超，表明 SynGA 在分布外分子上更具优势。


![[assets/figures/papers/iclr26_0002_OvMtGGaFUT_A_Genetic_Algorithm_for_Navigating_Synthesizable/figures/004_Table_3.jpg]]
*Table 3: Projection of N query molecules designed by generative models on 6 tasks. If y and $y ^ { \prime }$ are the scores of the query and analog molecules respectively, then $\Delta = y ^ { \prime }$ - y . We report the mean and standard deviation across queries, and the methods’ runtimes in the header. The Valid column pertains to SynFormer and we omit it for SynGA since it always achieves perfect validity

### 主结果：性质优化与对接任务

**PMO 基准测试。** 在包含 22 个多参数优化（MPO）任务的 PMO 套件上（Table 4），SynGA 的 top-10 AUC 总和为 13.366，在合成感知方法中具有竞争力，但落后于无约束算法（如 GraphGA 的 16.154 和 STONED 的 15.601）。SynGA 的贝叶斯优化增强版本 SynGBO 取得了 16.426 的总分，超越了所有基线，包括无约束算法。SynGBO 在 SynthesisNet 评估的子集（13 个任务）上得分为 9.332，而 SynthesisNet 为 8.820；在 SynFlowNet 评估的子集（2 个任务）上得分为 1.905，而 SynFlowNet 为 1.830。Figure 2 展示了 SynGBO 在优化过程中 top-k 分子平均分数的快速上升趋势，验证了其样本效率。


![[assets/figures/papers/iclr26_0002_OvMtGGaFUT_A_Genetic_Algorithm_for_Navigating_Synthesizable/figures/005_Table_4.jpg]]
*Table 4: Sum of the top-10 AUC scores over the PMO suite. Results are taken from their respective papers, except MolGA, REINVENT, and SynNet are taken from Kim et al. (2024). We average over 5 seeds, except f-RAG and SynthesisNet use only 3 and 1 seeds, respectively. Separate tables for SynthesisNet and SynFlowNet are given since they were assessed only on 13 and 2 PMO tasks, instead of the full 22. Task-wise results are given in Appendix C.5*

**LIT-PCBA 对接任务。** 在 15 个受体的分子对接任务上（Table 5），SynGA 的平均 Vina 对接分数为 -10.80，SynGBO 为 -11.11，均优于除 3DSynthFlow 外的所有基线。SynGBO 在 15 个受体中的 14 个上取得了最佳分数（Table 18），并在所有受体上取得了最佳配体效率（Table 19）。关键比较点：SynGA 和 SynGBO 仅使用 16,000 次 oracle 调用，而 3DSynthFlow 等基线使用了 64,000 次。在 ALDH1 任务上，SynGBO 的分数（-12.36）已接近 3DSynthFlow 的 -12.25（其预印本版本）。在模式发现数量上（Table 12），SynGA 和 SynGBO 在优化早期表现更优，但后期被 3DSynthFlow 超越。


![[assets/figures/papers/iclr26_0002_OvMtGGaFUT_A_Genetic_Algorithm_for_Navigating_Synthesizable/figures/006_Table_5.jpg]]

### 消融实验

**砌块过滤消融。** Table 1 展示了不同过滤方法对 SynGA 性能的影响。无过滤（None）的 Morgan 相似度仅为 0.459，基于相似度的启发式过滤（Sim）提升至 0.536，而 MLP 过滤大幅提升至 0.711。硬负例挖掘（MLP + Mine）在验证集上提高了精确率，但在 ChEMBL 测试集上性能下降（Morgan 0.664），表明硬负例挖掘可能导致过拟合或分布外问题。MLP 过滤还将重建率从 0.459（无过滤）提升至 0.709（验证集），同时将砌块子集大小从 196,907 压缩至 1,386（MLP）或 184（MLP + Mine）。


![[assets/figures/papers/iclr26_0002_OvMtGGaFUT_A_Genetic_Algorithm_for_Navigating_Synthesizable/figures/002_Table_1.jpg]]
*Table 1: Ablation of different building block filters for SynGA on the validation set and 100 test molecules sampled from ChEMBL. We compare no filtering (None), a similarity heuristic (Sim), an MLP, and an MLP trained with hard negative mining to enhance precision (MLP + Mine)*

**SynGA 与随机搜索。** Table 7 的消融实验表明，SynGA 在 MLP 过滤砌块上的性能（Morgan 0.721）远优于纯随机搜索（Random MLP: Morgan 0.564），验证了遗传算子而非单纯砌块过滤的贡献。

**变异操作权重。** Table 6 对 JNK3 和 Osimertinib MPO 任务的变异操作权重进行了消融。当前超参数（Grow/Shrink 概率 0.125，其余 0.25）取得了最佳或接近最佳的 AUC 总和（1.504 ± 0.131），而均匀权重（各 0.2）得分为 1.465 ± 0.068。

**NAM 训练损失。** Table 11 显示，在 NAM 训练中使用排名损失（ranking loss）优于均方误差（MSE）损失。例如，在 ALDH1 任务上，排名损失的测试相关系数为 0.769，采样分数为 -11.20，而 MSE 损失分别为 0.747 和 -11.07。

### 失败模式与局限性

1. **合成约束的代价。** SynGA 在 PMO 基准测试中落后于无约束算法（如 GraphGA），表明合成约束限制了搜索空间，可能导致次优性质。合成约束与性质优化之间的权衡需要进一步研究。

2. **模板库偏差。** 固定的反应模板库将探索限制在可合成空间的一个有偏子集内，可能遗漏重要化学空间。模板不保证反应产率、立体化学或成本。

3. **效率问题。** SynGA 在类似物搜索中比 SynFormer 慢 3 倍以上，在投影任务中耗时更长。这限制了其在需要大量迭代的场景中的应用。

4. **缺乏 3D 信息。** SynGA 不包含 3D 结构信息，而 3DSynthFlow 等基线在对接任务中受益于 3D 感知。SynGA 在 ALDH1 模式发现数量上后期被 3DSynthFlow 超越，可能与此相关。

5. **ML 增强的泛化风险。** 砌块过滤模型（MLP 和 NAM）可能无法很好地泛化到分布外分子，硬负例挖掘进一步加剧了这一问题。

6. **计算预算差异。** 在 LIT-PCBA 对接任务中，SynGA 和 SynGBO 仅使用 16,000 次 oracle 调用，而基线方法使用 64,000 次。虽然 SynGA 在更少调用下仍具竞争力，但增加预算可能带来更大提升。

## 方法谱系与知识库定位

SynGA 在合成感知分子生成方法中占据一个独特的位置：它不依赖任何机器学习模型来保证合成可行性，而是通过将遗传算法直接定义在合成树表示上，利用自定义的交叉与变异算子将合成约束内嵌于搜索过程本身。这一设计选择使其与两类主流方法形成鲜明对比。

**与投影类方法的关系。** 以 SynNet、ChemProjector、SynthesisNet 为代表的方法采用"先生成后投影"的范式：先由任意生成模型产生分子，再通过逆合成模型将其投影回可合成空间。这类方法的瓶颈在于投影过程计算成本高昂，且投影后的分子可能偏离原始优化目标。SynGA 通过构造性保证完全规避了这一问题——所有生成的分子天然具有合成路线。在 ChEMBL 类似物搜索任务中，SynGA (MLP) 在 Morgan 相似度 (0.711 vs. 0.459)、Scaffold 相似度 (0.694 vs. 0.526) 和 Gobbi 相似度 (0.623 vs. 0.400) 上均显著优于无过滤版本，而 ChemProjector 在这些指标上表现更弱。然而在投影任务中，SynGA 虽然一致优于 ChemProjector，但在 DDS-10 和 ZINC 数据集上落后于 SynFormer，这揭示了模板方法与学习型方法之间的权衡。

**与模板类方法的关系。** SynFormer 同样使用模板反应和砌块，但采用自回归生成范式。SynGA 与其相比，优势在于 100% 的有效性保证（SynFormer 在 ChEMBL 上有效性为 0.893）和构造性合成约束，但代价是速度慢 3 倍以上。这一速度差距源于遗传算法需要反复评估适应度和执行遗传操作，而 SynFormer 可以批量生成。两者的互补性值得关注：SynGA 可作为 SynFormer 输出的精炼步骤，或反过来用 SynFormer 加速 SynGA 的初始种群生成。

**与 GFlowNet/流匹配类方法的关系。** SynFlowNet、RGFN、RxnFlow、3DSynthFlow 等方法通过学习可合成分子空间上的生成分布来隐式编码合成约束。SynGA 的优势在于无需训练、轻量级且可解释，但在对接任务中，SynGA 虽然以仅 16,000 次 oracle 调用（基线方法使用 64,000 次）达到了竞争性结果，却在 ALDH1 任务中发现模式的数量上落后于 3DSynthFlow。这暗示 SynGA 的局部搜索策略在探索深度上可能不如基于流的方法，尤其是在需要精细调整结合模式的任务中。

**适用边界。** SynGA 最适用的场景是：1) 需要快速原型验证且计算预算有限；2) 合成可行性是硬约束而非软约束；3) 问题具有明确的单目标优化性质。其 ML 增强版本 SynGBO 通过神经加性模型 (NAM) 和砌块过滤进一步提升了样本效率，在 PMO 基准测试 22 个任务上以 16.426 的 Top-10 AUC 总和达到或超越了最先进水平。

**核心局限。** 第一，SynGA 继承了基于模板方法的所有局限性：模板不保证实际合成可行性，不考虑反应条件、立体化学、产率或成本。第二，固定模板库必然将探索限制在可合成空间的一个有偏子集内。第三，在 PMO 基准测试中，SynGA 落后于无约束算法（如 GraphGA、STONED），这表明合成约束本身构成了搜索空间瓶颈。第四，当前版本不包含 3D 信息，而 3DSynthFlow 等基线在对接任务中受益于 3D 感知。第五，砌块过滤模型（MLP 和 NAM）的泛化能力在分布外分子上存疑，硬负例挖掘虽然提高了验证集精确率，但在 ChEMBL 测试集上反而导致性能下降。

**开放问题。** 如何将 3D 信息整合到 SynGA 中？除了砌块过滤和模型增强变体外，还有哪些 ML 混合方式可以增强 SynGA？如何在不降低效率和鲁棒性的前提下扩大模板集？SynGA 能否作为精炼步骤改进 SynFormer 等合成模型的输出？如何与多目标遗传算法（如 NSGA-II）结合以处理多目标优化？这些问题构成了该方向后续研究的关键切入点。

## 原文 PDF

PDF 文件：paperPDFs/ICLR_2026/A_Genetic_Algorithm_for_Navigating_Synthesizable_Molecular_Spaces.pdf

![[paperPDFs/ICLR_2026/A_Genetic_Algorithm_for_Navigating_Synthesizable_Molecular_Spaces.pdf]]
