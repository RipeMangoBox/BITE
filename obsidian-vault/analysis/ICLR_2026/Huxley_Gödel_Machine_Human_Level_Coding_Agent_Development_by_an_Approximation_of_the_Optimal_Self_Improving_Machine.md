---
title: "Huxley-Gödel Machine: Human-Level Coding Agent Development by an Approximation of the Optimal Self-Improving Machine"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: "paperPDFs/ICLR_2026/Huxley_Gödel_Machine_Human_Level_Coding_Agent_Development_by_an_Approximation_of_the_Optimal_Self_Improving_Machine.pdf"
openreview_forum_id: T0EiEuhOOL
aliases:
- HGDMH
tags:
- ICLR_2026
- topic/representation_self_supervised_transfer
- topic/representation_self_supervised_transfer/transfer_multitask_and_meta_learning
core_operator: "基于谱系元生产力（Clade-Metaproductivity, CMP）的估计值作为自我改进搜索的指导信号，并通过汤普森采样（Thompson Sampling）结合自适应调度进行节点选择。"
primary_logic: "通过聚合整个后代谱系（clade）的成功记录（而非仅依赖代理自身的即时基准得分）来估计CMP，可以更忠实地衡量代理的自我改进潜力；在特定假设下（可重复试验、效用仅为最终代理性能等），CMP先知足以模拟哥德尔机器（Gödel Machine）的接受机制，因此基于CMP估计的HGM能够有效近似最优自我改进。"
claims:
- "HGM通过估计谱系级CMP并使用汤普森采样作为指导，近似了哥德尔机器的风格。"
- "在编码代理开发设定下，访问真实CMP先知足以实现哥德尔机器（定理1）。"
- "HGM的CMP估计与经验CMP的加权相关性显著高于SICA和DGM（SWE-Verified-60上：HGM 0.778 vs SICA 0.444）。"
- "在SWE-Verified-60和Polyglot上，HGM发现的最佳信念代理准确率均最高，且所需的CPU小时数大幅少于DGM和SICA。"
---

# Huxley-Gödel Machine: Human-Level Coding Agent Development by an Approximation of the Optimal Self-Improving Machine

> [!tip] 核心洞察
> 通过聚合整个后代谱系（clade）的成功记录（而非仅依赖代理自身的即时基准得分）来估计CMP，可以更忠实地衡量代理的自我改进潜力；在特定假设下（可重复试验、效用仅为最终代理性能等），CMP先知足以模拟哥德尔机器（Gödel Machine）的接受机制，因此基于CMP估计的HGM能够有效近似最优自我改进。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 赫胥黎-哥德尔机器：通过近似最优自我改进机器实现人类级编码代理开发 |
| 英文题名 | Huxley-Gödel Machine: Human-Level Coding Agent Development by an Approximation of the Optimal Self-Improving Machine |
| 会议/期刊 | ICLR 2026 (Oral) |
| Links | [paper](https://openreview.net/forum?id=T0EiEuhOOL); [GitHub](https://github.com/metauto-ai/HGM) |
| Topic | #topic/representation_self_supervised_transfer #topic/representation_self_supervised_transfer/transfer_multitask_and_meta_learning |
| Method | Huxley-Gödel Machine (HGM) |
| Dataset | SWE-Verified-60, Polyglot, SWE-Bench Verified (full) |

> [!tip] 效果简介
> - SWE-Verified-60 上，Accuracy (%) 为 56.7，对比 53.3 (DGM) / 50.0 (SICA)，变化 +3.4 over DGM, +6.7 over SICA。
> - SWE-Verified-60 上，Allocated CPU-hours (800 evals) 为 517，对比 1231 (DGM)，变化 -714 hours (2.38× faster)。
> - Polyglot 上，Accuracy (%) 为 30.5，对比 27.1 (DGM) / 25.4 (SICA)，变化 +3.4 over DGM, +5.1 over SICA。

## 概述

构建能够自主改进的编码代理是迈向通用人工智能的关键一步。然而，当前的自我改进方法面临一个根本性瓶颈：**元生产力-性能不匹配（Metaproductivity-Performance Mismatch）**——代理的即时基准得分无法可靠预测其长期自我改进潜力。高评分代理可能产生低产出的后代，而低评分代理有时反而能孕育出更强的谱系。

针对这一问题，本文提出了**赫胥黎-哥德尔机器（Huxley-Gödel Machine, HGM）**，一种通过近似最优自我改进机器来实现人类级编码代理开发的方法。HGM的核心洞见在于：通过聚合整个后代谱系（clade）的成功记录来估计**谱系元生产力（Clade-Metaproductivity, CMP）**，而非仅依赖代理自身的即时性能，可以更忠实地衡量其自我改进潜力。在特定的可重复试验假设下，论文证明了访问真实CMP先知足以模拟哥德尔机器（Gödel Machine）的接受机制（定理1），从而为HGM的设计提供了理论保证。

方法上，HGM在三个关键维度上对现有自我改进范式进行了重构：首先，**解耦扩展与评估**，采用类似UCB-Air的自适应策略动态决定何时生成新代理、何时评估已有代理；其次，**基于谱系CMP估计的汤普森采样**指导父节点选择，使搜索偏向具有高自我改进潜力的谱系；最后，引入**细粒度评估**与**异步并行执行**，大幅提升计算效率。

实验表明，HGM在SWE-Verified-60和Polyglot基准上均取得了最高的最佳信念代理准确率，同时所需CPU小时数显著低于前沿方法DGM和SICA：在SWE-Verified-60上达到56.7%（比DGM高3.4个百分点），仅需517 CPU小时（2.38倍加速）；在Polyglot上达到30.5%，仅需347小时（6.86倍加速）。HGM发现的代理在SWE-bench Verified完整集上达到61.4%，超越了最优人类设计的GPT-5 mini代理；在SWE-Lite上以GPT-5运行时，匹配了人类工程化代理的最佳官方验证结果。消融实验进一步证实，HGM的CMP估计器与经验CMP的加权相关性（0.778）显著高于基于即时性能的方法（SICA为0.444），验证了谱系级信息对预测自我改进潜力的关键作用。

## 背景与动机

### 编码代理的自我改进：从即时性能到长期潜力

当前最先进的编码代理已在软件工程基准上展现出令人瞩目的能力，但其设计过程高度依赖人类专家的反复试错与领域直觉。一个自然而迫切的问题是：**能否让编码代理实现自我改进，即通过自动修改自身代码来持续提升下游任务表现？**

这一愿景将自我改进形式化为一个迭代树搜索问题：从初始代理出发，每一步决定是扩展现有代理（生成一个修改后的子代）还是评估已有代理（在任务上测试其能力），最终目标是发现性能最优的代理。然而，这一搜索过程面临一个根本性的瓶颈——**元生产力-性能不匹配（Metaproductivity-Performance Mismatch）**：代理的即时基准得分并不能可靠地预测其长期自我改进潜力。一个在当前测试中得分很高的代理，其后代谱系可能表现平庸；反之，一个看似平平无奇的代理，有时却能孕育出远超自身的后代谱系。

### 现有方法的局限：短视的即时性能导向

现有前沿方法均受困于这一不匹配。**SICA**（Robeyns et al., 2025）和**DGM**（Zhang et al., 2025a）都采用基于单个代理即时性能的指导策略：SICA选择当前经验成功率最高的代理作为父节点进行修改，DGM则采用类似的性能导向评分。这种“短视”策略在根本上忽略了代理的**谱系级潜力**——一个代理的真正价值不仅在于它自身能解决多少任务，更在于它能催生出多强的后代。

正如 Figure 1（左）所示，基于即时性能的指导指标与长期自我改进结果之间存在弱相关性，这直接限制了现有方法的搜索效率。此外，SICA和DGM在调度上也存在刚性：它们将扩展（生成新代理）与评估（测试代理能力）固定绑定，每次修改后立即对所有任务执行完整评估。这种粗粒度的评估策略不仅浪费计算资源，还无法及时终止对低潜力代理的无效投入。

### 本文动机：以谱系元生产力逼近最优自我改进

为了克服上述瓶颈，本文引入了一个关键的因果调节变量——**谱系元生产力（Clade-Metaproductivity, CMP）**。CMP的核心思想源自生物学中的“进化枝”（clade）概念：衡量一个代理的自我改进潜力，不应只看它自身的得分，而应聚合其整个后代谱系的成功记录。直觉上，一个能够持续孕育出高能力后代的代理，才是真正具有高元生产力的“优良父本”。

在理论层面，本文证明了在特定假设下（可重复试验、效用仅取决于最终代理性能、证明搜索不消耗预算），**访问真实的CMP先知足以模拟哥德尔机器（Gödel Machine）的接受机制**（定理1）。哥德尔机器作为理论上最优的自我改进框架，其核心在于仅当可证明改进时才执行自我修改——而CMP恰好为这一决策提供了可操作的代理信号。

基于这一洞察，本文提出**赫胥黎-哥德尔机器（Huxley-Gödel Machine, HGM）**，通过估计谱系级CMP并使用汤普森采样（Thompson Sampling）指导自我改进搜索，从而在无需可证明性检查的前提下，有效近似最优自我改进行为。HGM同时解耦了扩展与评估决策，引入自适应调度和细粒度评估策略，从根本上突破了现有方法的刚性约束。

## 核心创新

HGM 的核心创新在于用**谱系级元生产力（Clade-Metaproductivity, CMP）**替代即时基准性能作为自我改进搜索的指导信号，从而解决了现有方法中普遍存在的**元生产力-性能不匹配（Metaproductivity-Performance Mismatch）**问题——即单个代理的当前评分与其长期自我改进潜力之间呈弱相关甚至无关（Figure 1 左）。

### 从个体性能到谱系元生产力

现有方法 **SICA**（Robeyns et al., 2025）和 **DGM**（Zhang et al., 2025a）均以代理自身的经验成功率作为选择父节点的依据，这隐含地假设高评分代理必然产生高质量后代。HGM 从根本上改变了这一假设：它定义并估计 CMP，即一个代理及其整个后代谱系（clade）中最佳代理的期望效用。理论分析表明，在可重复试验等假设下，**访问真实 CMP 先知足以实现哥德尔机器**（Theorem 1），而 HGM 通过聚合谱系内所有后代的成功记录来估计 CMP，从而近似了这一最优自我改进过程。

### 四个关键策略槽位的改变

HGM 在三个子策略和执行范式上对基线方法进行了系统性重构（Table 4）：

1. **选择策略：扩展与评估解耦**。SICA 和 DGM 采用固定交替模式——每次修改后立即对所有任务执行评估。HGM 打破这一刚性约束，采用类似 UCB-Air 的自适应决策：根据当前代理数量 $N_t$ 与评估总次数 $|\bar{T}_t|$ 的关系（$N_t^{\alpha} \geq |\bar{T}_t|$），动态决定本轮是生成新代理还是深入评估已有代理。这一解耦使得计算资源可以更灵活地分配到更有价值的操作上。

2. **扩展策略：基于谱系 CMP 的汤普森采样**。HGM 不再选择当前评分最高的代理作为父节点，而是基于整个谱系的累积成功/失败计数，通过汤普森采样选择扩展对象。具体而言，采样分布由 Beta 分布的参数 $\tau(1 + n_{\text{success}}^{C}(a))$ 和 $\tau(1 + n_{\text{failure}}^{C}(a))$ 决定，其中探索-利用调度参数 $\tau$ 控制采样的随机程度。这一设计使得即使当前评分较低的代理，只要其谱系展现出良好的整体潜力，仍然有机会被选中扩展。

3. **评估策略：细粒度代理-任务对评估**。SICA 和 DGM 一次性评估所有下游任务，而 HGM 每次仅评估一个代理-任务对。它使用基于单个代理性能的汤普森采样选择评估对象，从而能够尽早识别并终止低潜力代理的评估，避免在无前途的代理上浪费计算资源。

4. **执行范式：异步并行化**。SICA 和 DGM 均为串行执行，而 HGM-Async 在多个 CPU 上同时执行选择-扩展-评估迭代，每次迭代完成后立即利用最新数据更新树信息。这一异步设计充分利用了扩展与评估解耦带来的并行机会。

### 创新有效性的实证支撑

CMP 估计的有效性在相关性分析中得到验证：在 SWE-Verified-60 上，HGM 的 CMP 估计与经验 CMP 的加权 Pearson 相关系数达到 **0.778**，而 SICA 仅为 0.444（Table 1），表明谱系级信息确实比个体性能更能预测长期自我改进潜力。这一信号质量的提升直接转化为下游性能优势：HGM 在 SWE-Verified-60 上以 517 CPU 小时达到 56.7% 准确率，而 DGM 需要 1231 小时才达到 53.3%（Table 2）——**准确率提升 3.4 个百分点，同时计算效率提升 2.38 倍**。在 Polyglot 上，效率优势更为显著，达到 **6.86 倍加速**（347h vs 2385h），同时准确率从 27.1% 提升至 30.5%。

## 整体框架

![[assets/figures/papers/paper_list_l28_https_openreview_net_forum_id_T0EiEuhOOL/figures/006_Table_2.jpg]]
*Table 2: summarizes the three subpolicies of SICA, DGM, and HGM, which define solutions to the iterative tree search problem defined in 2. Table 4: Comparison of structured policies across self-improving methods. Each method is described by three subpolicies: Mod vs. Eval, Modification Strategy, and Evaluation Strategy*

HGM 将编码代理的自我改进形式化为一个迭代式树搜索问题，其目标是在计算预算 $B$ 内发现一个能最大化下游任务性能的最终代理。整个搜索过程被分解为三个核心子策略的交替执行，并通过异步并行调度实现高效探索。

### 问题形式化

给定一个初始编码代理 $a_0$ 和一组下游任务，自我改进过程在每一步 $t$ 面临一个复合决策：是扩展（生成新代理）还是评估（测试已有代理）；若扩展，选择哪个父代理进行修改；若评估，选择哪个代理和哪个任务进行测试。该决策被形式化为三个子策略：

- **选择策略（Selection Policy）**：决定当前步执行扩展还是评估。
- **扩展策略（Expansion Policy）**：选择一个父代理，调用编码代理生成一个自我修改的子代理。
- **评估策略（Evaluation Policy）**：选择一个代理-任务对进行细粒度测试。

预算耗尽后，从最终代理树 $\mathcal{T}_B$ 中选出最终代理 $a_{\text{final}}$，目标是最大化其期望效用 $J(\pi) = \mathbb{E}[U(a_{\text{final}})]$。

### 核心洞察：从即时性能到谱系元生产力

现有方法（如 **SICA** 和 **DGM**）的瓶颈在于**元生产力-性能不匹配**：代理的即时基准得分无法可靠预测其长期自我改进潜力。高评分代理可能产生低产出的后代，而低评分代理有时却能孕育出更强的谱系。

HGM 的核心创新在于引入**谱系元生产力（Clade-Metaproductivity, CMP）**作为指导信号。CMP 衡量的是以某个代理为根的整个后代谱系（clade）中最佳代理的期望效用：

$$\mathrm{CMP}_{\pi}(\mathcal{T}, a) = \mathbb{E}_{\mathcal{T}_B \sim p_{\pi}(\cdot \vert \mathcal{T}, a)} \left[ U(\mathrm{argmax}_{a' \in \mathcal{C}(\mathcal{T}_B, a)} Score_{\pi}(a')) \right]$$

其中 $\mathcal{C}(\mathcal{T}_B, a)$ 表示在最终存档树中以 $a$ 为根的谱系。与仅关注单个代理得分的传统方法不同，CMP 通过聚合整个谱系的成功记录，更忠实地反映了代理的自我改进潜力。

**定理 1** 表明：在可重复试验、效用仅为最终代理性能等假设下，访问真实 CMP 先知足以模拟哥德尔机器的接受机制。这为 HGM 的设计提供了理论根基——通过估计 CMP 来近似最优自我改进。

### 管道模块与数据流

HGM 的完整管道由以下模块组成，各模块在异步并行框架下协同工作：

1. **选择策略（Select）**：采用类似 UCB-Air 的自适应决策机制，根据当前代理数量 $N_t$ 与评估总次数 $|\bar{T}_t|$ 的关系动态决定执行扩展还是评估。当 $N_t^{\alpha} \geq |\bar{T}_t|$ 时执行扩展，否则执行评估。这种解耦打破了 SICA 和 DGM 中“每次修改后必须立即全量评估”的刚性约束。

2. **扩展策略（Expand）**：基于谱系级 CMP 估计进行汤普森采样选择父代理。具体地，对树中每个代理 $a$，利用其谱系内累积的成功计数 $n_{\text{success}}^C(a)$ 和失败计数 $n_{\text{failure}}^C(a)$ 构建 Beta 分布，并通过探索-利用调度参数 $\tau$ 进行缩放：
   $$a^{*} \sim TS(\{ \tau(1 + n_{\text{success}}^{C}(a)), \tau(1 + n_{\text{failure}}^{C}(a)) \mid a \in \mathcal{T}_{t} \})$$
   选中的父代理调用编码模型生成一个自我修改的子代理，并将其加入搜索树。

3. **评估策略（Evaluate）**：采用针对单个代理性能的汤普森采样，选择一个代理并从中选取一个尚未评估的任务进行细粒度测试。这种单任务粒度的评估允许尽早终止低潜力代理的测试，避免资源浪费。

4. **最终选择（Final Select）**：预算耗尽后，返回具有最高后验效用 $\epsilon$-分位数的代理（最佳信念代理）：
   $$\mathrm{argmax}_{a \in \mathcal{T}_{B}} I_{\epsilon}(1 + n_{\text{success}}(a), 1 + n_{\text{failure}}(a))$$
   其中 $I_{\epsilon}$ 为正则化不完全 Beta 函数。

5. **异步调度器（Async Scheduler）**：在每个可用 CPU 上同时执行选择-扩展-评估迭代，使用最新可用数据，完成后立即更新树信息。这种异步并行化使得 HGM 在相同评估次数下所需的 CPU 小时数大幅低于串行执行的 DGM 和 SICA（在 Polyglot 上最高实现 6.86 倍加速）。

### CMP 估计

实际中无法访问真实 CMP 先知，HGM 使用谱系内累积的观测成功率作为估计量：

$$\widehat{\mathrm{CMP}}(a) = \frac{n_{\text{success}}^{C}(a)}{n_{\text{success}}^{C}(a) + n_{\text{failure}}^{C}(a)}$$

其中 $n_{\text{success}}^{C}(a) = \sum_{a' \in C(a)} n_{\text{success}}(a')$ 和 $n_{\text{failure}}^{C}(a) = \sum_{a' \in C(a)} n_{\text{failure}}(a')$ 分别为谱系内所有代理的累计通过和失败测试数。实验表明，该估计量与经验 CMP 的加权 Pearson 相关性在 SWE-Verified-60 上达到 0.778，显著高于 SICA 的 0.444（Table 1），验证了谱系级信息对预测自我改进潜力的关键作用。

## 核心模块与公式推导

### 问题形式化

HGM将编码代理的自我改进过程形式化为一个迭代式树搜索问题。在每一时间步，系统需要做出一个复合决策：是生成新代理（扩展）还是进一步测试已有代理（评估）；如果扩展，选择哪个父代理进行修改；如果评估，选择哪个代理和哪个任务进行测试。该复合决策自然分解为三个子策略：

- **选择策略**：决定本轮执行扩展还是评估。
- **扩展策略**：确定修改哪个父代理以生成后代。
- **评估策略**：确定评估哪个代理的哪个任务。

优化目标为最大化最终选定代理的期望效用：

$$J(\pi) = \mathbb{E}\left[U(a_{\mathrm{final}})\right]$$

其中 $a_{\mathrm{final}} = \operatorname{argmax}_{a \in \mathcal{T}_B} Score_{\pi}(a)$，即搜索预算耗尽后从最终存档树 $\mathcal{T}_B$ 中选出的最优代理。

### 元生产力：从全局到谱系

#### 全局元生产力（GMP）

GMP衡量从当前树 $\mathcal{T}$ 和代理 $a$ 出发，在策略 $\pi$ 的引导下，最终存档中最优代理的期望效用：

$$\mathrm{GMP}_{\pi}(\mathcal{T}, a) = \mathbb{E}_{\mathcal{T}_B \sim p_{\pi}(\cdot \vert \mathcal{T}, a)} \left[ U(\operatorname{argmax}_{a' \in \mathcal{T}_B} Score_{\pi}(a')) \right]$$

GMP的核心理念在于：它度量的是长期自我改进潜力，包括那些改善“自我改进能力本身”的修改——即元认知层面的提升。

#### 谱系元生产力（CMP）

CMP是GMP的局部化变体，将最优化的搜索范围限定于以代理 $a$ 为根的谱系（clade）$\mathcal{C}(\cdot)$ 内：

$$\mathrm{CMP}_{\pi}(\mathcal{T}, a) = \mathbb{E}_{\mathcal{T}_B \sim p_{\pi}(\cdot \vert \mathcal{T}, a)} \left[ U(\operatorname{argmax}_{a' \in \mathcal{C}(\mathcal{T}_B, a)} Score_{\pi}(a')) \right]$$

CMP只关心 $a$ 及其所有后代构成的子树中的最优表现，因此能够更精确地衡量单个代理的“繁殖潜力”——即该代理及其谱系能产生多强后代的能力。

#### CMP先知与哥德尔机器的等价性

在编码代理开发的设定下（假设可重复试验、效用仅取决于最终代理性能、证明搜索不消耗预算），**定理1** 表明：访问真实CMP先知足以实现哥德尔机器。这为HGM提供了理论根基——只要能有效估计CMP，就能近似最优的自我改进。

### HGM的四个核心模块

HGM通过迭代执行以下结构化策略来近似哥德尔机器风格的自我改进：

#### 模块1：选择策略（Selection Policy）

HGM打破了SICA和DGM中“每次修改后必须完整评估”的刚性交替模式。选择策略采用类似UCB-Air的启发式规则，根据当前代理数量 $N_t$ 与评估总次数 $|\bar{T}_t|$ 的关系，动态决定执行扩展还是评估：

- 当 $N_t^{\alpha} \geq |\bar{T}_t|$ 时，倾向于扩展新代理；
- 否则，倾向于评估已有代理。

这一解耦使系统能将计算预算更灵活地分配给“探索新后代”与“深入评估现有代理”之间。

#### 模块2：扩展策略（Expansion Policy）

扩展时，HGM基于谱系级CMP估计进行汤普森采样以选择父代理：

$$a^{*} \sim TS\left(\left\{ \tau(1 + n_{\mathrm{success}}^{C}(a)), \tau(1 + n_{\mathrm{failure}}^{C}(a)) \mid a \in \mathcal{T}_t \right\}\right)$$

其中：
- $n_{\mathrm{success}}^{C}(a) = \sum_{a' \in \mathcal{C}(a)} n_{\mathrm{success}}(a')$：谱系内所有代理的累积成功测试数；
- $n_{\mathrm{failure}}^{C}(a) = \sum_{a' \in \mathcal{C}(a)} n_{\mathrm{failure}}(a')$：谱系内所有代理的累积失败测试数；
- $\tau$：探索-利用调度器参数，控制汤普森采样的集中程度。

采样分布基于 $\mathrm{Beta}(\tau(1 + n_{\mathrm{success}}^{C}(a)), \tau(1 + n_{\mathrm{failure}}^{C}(a)))$，这意味着谱系内累积成功越多的代理，被选为父节点的概率越高，但由于汤普森采样的随机性，仍保留了探索低样本量但具潜力的谱系的可能性。

选中父代理后，调用编码代理生成一个自我修改的子代理，完成一次扩展。

#### 模块3：评估策略（Evaluation Policy）

评估时，HGM采用细粒度策略：每次仅评估一个代理-任务对。选择评估对象时，使用基于单个代理性能的汤普森采样：

$$a^{*} \sim TS\left(\tau(1 + n_{\mathrm{success}}(a)), \tau(1 + n_{\mathrm{failure}}(a))\right)$$

然后从该代理尚未评估的任务中选取一个进行测试。这一设计的优势在于：能够尽早识别并终止低潜力代理的评估，避免在注定失败的方向上浪费大量计算资源。相比之下，SICA和DGM一次性评估所有任务，无法中途止损。

#### 模块4：最终选择策略（Final Agent Selection）

预算耗尽后，HGM返回具有最高后验效用 $\epsilon$-分位数的最佳信念代理：

$$\operatorname{argmax}_{a \in \mathcal{T}_B} I_{\epsilon}\left(1 + n_{\mathrm{success}}(a), 1 + n_{\mathrm{failure}}(a)\right)$$

其中 $I_{\epsilon}(\cdot, \cdot)$ 是正则化不完全贝塔函数，$\epsilon$ 控制保守程度——选择分位数而非均值，能够在一定程度上规避因评估噪声导致的高估风险。

### CMP估计器

HGM的核心创新在于用谱系级聚合统计量来近似CMP：

$$\widehat{\mathrm{CMP}}(a) = \frac{n_{\mathrm{success}}^{C}(a)}{n_{\mathrm{success}}^{C}(a) + n_{\mathrm{failure}}^{C}(a)}$$

这一估计器将代理 $a$ 的自我改进潜力量化为其整个后代谱系中累积的成功率。与SICA和DGM仅依赖代理自身即时性能的估计方式不同，CMP估计器能够捕捉到“低即时得分但高产后代”的代理——这正是解决**元生产力-性能不匹配**瓶颈的关键机制。

**经验验证**：在SWE-Verified-60上，HGM的CMP估计与经验CMP的加权皮尔逊相关系数达到0.778，而SICA仅为0.444（Table 1），证实了谱系级信息对预测自我改进潜力的显著优势。

### 异步并行实现

HGM-Async在多个CPU上同时执行选择-扩展-评估迭代。每个CPU独立运行一个迭代过程，完成后立即使用最新数据更新树的统计信息，并启动新一轮迭代。这种异步并行化使HGM在Polyglot上相比DGM实现了高达6.86倍的加速（347h vs 2385h），在SWE-Verified-60上也达到2.38倍加速（517h vs 1231h）。

## 实验与分析

### 核心瓶颈：元生产力-性能不匹配

HGM的设计动机源于一个关键观察：**即时基准性能无法可靠预测代理的长期自我改进潜力**。如Figure 1（左）所示，基于代理自身性能的指导信号（如SICA和DGM所采用的策略）与长期自我改进结果之间存在弱相关——高评分代理可能产生低产出的后代，而低评分代理有时却能孕育出更强的谱系。HGM通过引入谱系级元生产力（Clade-Metaproductivity, CMP）来缓解这一不匹配，将指导信号从个体性能提升到整个后代谱系的成功聚合。


![[assets/figures/papers/paper_list_l28_https_openreview_net_forum_id_T0EiEuhOOL/figures/002_Figure_1.jpg]]
*Figure 1: (Left) Weak correlation between the guidance metrics of other methods (based on performance) and long-term self improvement; HGM mitigates this mismatch by leveraging clade-level metaproductivity. (Right) On SWE-bench Verified, HGM achieves higher accuracy with 2.38 times less allocated CPU-hours. SICA encountered repeated errors after consuming 45% of its budget*

### CMP估计质量：与经验CMP的相关性

Table 1报告了各方法在SWE-Verified-60和Polyglot上，其指导信号估计值与经验CMP之间的皮尔逊相关性。HGM的CMP估计器在加权相关性上显著优于基线：


![[assets/figures/papers/paper_list_l28_https_openreview_net_forum_id_T0EiEuhOOL/figures/003_Table_1.jpg]]
*Table 1: Clade-Metaproductivity: Empirical vs. Estimation Correlation. We report the Pearson correlations between the empirical CMPs and the estimates from DGM, SICA, and HGM on SWE-Verified-60 and Polyglot. For the weighted correlations, each prediction is weighted by its accessed number of evaluations*

- **SWE-Verified-60**：HGM加权相关性 **0.778**，SICA仅为0.444（DGM在此设置下的具体数值需查表确认）。
- **Polyglot**：HGM加权相关性 **0.626**，同样大幅领先。

这一结果表明，聚合谱系内所有后代的成功/失败记录（而非仅依赖单个代理的即时得分）能够更忠实地衡量代理的自我改进潜力，验证了CMP作为搜索指导信号的有效性。

### 主结果：自我改进能力对比

Table 2报告了各方法在800次评估预算下的最佳信念代理准确率和分配的CPU小时数。HGM在两项基准上均取得最高准确率，同时消耗显著更少的计算资源：


![[assets/figures/papers/paper_list_l28_https_openreview_net_forum_id_T0EiEuhOOL/figures/004_Table_2.jpg]]
*Table 2: Self-Improving Capability Comparison. We report the task performance (in accuracy) of each method’s best-belief agent and the allocated CPU-hours time required for 800 evaluations. Super-scripted accuracies with “+” indicate performance gains over their respective initial agents*

**SWE-Verified-60（GPT-5 mini评估，GPT-5扩展）**：
- HGM：**56.7%** 准确率，**517 CPU小时**
- DGM：53.3% 准确率，1231 CPU小时
- SICA：50.0% 准确率（注：SICA因上下文窗口溢出陷入无限循环，消耗45%预算后无法继续）
- HGM相对DGM提升 **+3.4个百分点**，同时节省 **714 CPU小时（2.38倍加速）**

**Polyglot（量化评估模型）**：
- HGM：**30.5%** 准确率，**347 CPU小时**
- DGM：27.1% 准确率，2385 CPU小时
- SICA：25.4% 准确率
- HGM相对DGM提升 **+3.4个百分点**，加速达 **6.86倍**

HGM的加速优势来源于两个关键设计：（1）扩展与评估的解耦和自适应调度，避免了对低潜力代理的过度评估；（2）异步并行化实现，允许多个CPU同时执行选择-扩展-评估迭代。

### 泛化能力

**完整SWE-Bench Verified**：HGM发现的最佳信念代理在完整的SWE-Bench Verified上达到 **61.4%** 准确率（初始代理约53.2%），提升了 **+8.2个百分点**，超越了当时最佳的人类设计的GPT-5 mini代理。

**SWE-Lite泛化测试（Table 3）**：将在SWE-Verified上发现的代理迁移到SWE-Lite，验证其泛化能力：

![[assets/figures/papers/paper_list_l28_https_openreview_net_forum_id_T0EiEuhOOL/figures/005_Table_3.jpg]]
*Table 3: Generalization on SWE-Lite and GPT-5. We report the accuracy of HGM’s best-belief SWE-Verified agent on SWE-Lite with GPT-5 mini and GPT-5 under two settings: filtered (completely unseen) and standard (leaderboard setting)*

- 使用GPT-5 mini：Filtered设置 **40.1%**，Standard设置 **49.0%**
- 使用GPT-5：Standard设置 **57.3%**，匹配或超越了最佳人类工程化代理的官方验证结果

此外，HGM代理配合GPT-5.1 Codex mini在SWE-Bench-Live Lite上取得 **27.0%** 准确率，超越了此前的最佳成绩（24.7%），达到该基准的领先水平。

### 消融分析：解耦与并行化的贡献

HGM性能优势的来源可通过两个消融维度理解：

1. **CMP指导信号**：Table 1的相关性分析直接证明，谱系级信息是预测自我改进潜力的关键。SICA和DGM基于个体性能的估计与经验CMP的相关性显著更低，这解释了为何它们在相同评估预算下发现的最佳代理性能较差。

2. **异步并行与自适应调度**：DGM和SICA采用固定交替的扩展-评估策略，导致大量CPU时间浪费在对低潜力代理的全面评估上。HGM通过解耦扩展与评估（UCB-Air启发式决策）和异步并行，在Polyglot上实现了对DGM的6.86倍加速，在SWE-Verified-60上实现了2.38倍加速。

### 失败模式与局限性

- **SICA的上下文窗口溢出**：在SWE-Verified-60上，SICA因上下文窗口溢出而陷入无限循环，消耗45%预算后无法继续。这暴露了固定交替策略在长序列自我修改中的脆弱性。
- **CMP估计的样本依赖性**：CMP估计依赖于谱系内累积的测试结果，在评估代价高昂或后代数量不足时可能存在估计偏差，需要较多的后代评估才能收敛。
- **基准过拟合风险**：所发现的代理在SWE-Verified和Polyglot上表现优异，但这些基准可能无法完全代表一般编程能力，存在一定程度的过拟合可能。
- **理论-实践差距**：定理1证明CMP先知足以实现哥德尔机器，但前提假设包括可重复试验且证明搜索不消耗预算，实际计算资源限制下仍存在近似误差。
## 方法谱系与知识库定位

### 1. 与基线方法的关系

HGM 直接承袭并改造了自我改进编码代理（Self-Improving Coding Agent）这一研究方向下的两类代表性工作：**SICA**（Robeyns et al., 2025）和 **DGM**（Zhang et al., 2025a）。三者的共同框架是将代理的自我改进过程形式化为一个迭代的树搜索问题，目标是在下游任务上最大化最终代理的期望效用。然而，HGM 在三个核心子策略上进行了根本性的重构，从而与基线形成清晰的谱系分野。

**选择策略（Selection Policy）的突破**。SICA 和 DGM 均采用固定的交替模式：每次修改后立即对子代理执行全量任务评估。这种刚性调度将扩展与评估强行绑定，导致大量计算资源浪费在对低潜力代理的过度评估上。HGM 打破了这一约束，引入类似 UCB-Air 的自适应决策机制：根据当前代理数量 $N_t$ 与评估总次数 $|\bar{T}_t|$ 的关系动态决定本轮执行扩展还是评估（具体规则为 $N_t^{\alpha} \geq |\bar{T}_t|$ 时扩展，否则评估）。这一解耦使得搜索过程可以将预算集中在更有前景的谱系分支上。

**扩展策略（Expansion Policy）的根本差异**。SICA 和 DGM 均基于单个代理的即时经验成功率选择父节点——即选择当前平均得分最高的代理进行修改。这一策略隐含假设即时基准性能能够可靠预测长期自我改进潜力。HGM 的核心创新在于否定了这一假设，转而引入**谱系元生产力（Clade-Metaproductivity, CMP）**作为指导信号：扩展时使用基于谱系累积成功/失败计数的汤普森采样选择父代理，分布参数由探索-利用调度器 $\tau$ 缩放。这意味着一个即时得分较低但后代谱系整体表现强劲的代理，可能比一个高分但后代产出贫乏的代理更值得扩展。

**评估策略（Evaluation Policy）的粒度差异**。SICA 和 DGM 均采用一次性评估所有下游任务的粗粒度策略。HGM 则采用细粒度的逐任务评估：每次仅评估一个代理-任务对，并使用针对单个代理性能的汤普森采样选择评估对象。这一设计使得对低潜力代理的早期终止成为可能，进一步节省了评估预算。

**理论基础的深化**。HGM 与基线之间更深层的区别在于理论锚点的不同。SICA 和 DGM 本质上是启发式搜索方法，缺乏对最优自我改进的形式化逼近论证。HGM 则通过定理 1 建立了与哥德尔机器（Gödel Machine）的桥梁：在可重复试验且证明搜索不消耗预算的假设下，访问真实 CMP 先知足以实现哥德尔机器。HGM 通过估计 CMP 来近似这一先知，从而为方法提供了理论上的最优性依据。这一点在基线方法中并无对应。

### 2. 适用边界

HGM 的适用性受限于以下关键假设和设计选择：

- **编码代理开发的限定域**。当前 HGM 的实现仅适用于代码层次的自我修改——代理通过生成代码修改来改进自身的行为策略。方法尚未扩展到权重空间（直接调整神经网络参数）或模型架构级别的自我改进。这意味着 HGM 目前是一个编码代理开发工具，而非通用的自我改进框架。

- **可重复试验假设**。CMP 的定义和估计依赖于可重置的评估环境：同一代理在同一任务上的重复评估应产生一致的结果。在非确定性或不可重置的环境中，CMP 估计的方差将显著增大，可能破坏汤普森采样的有效性。

- **评估代价的可承受性**。CMP 估计需要聚合整个后代谱系的测试记录，这意味着每个谱系分支都需要一定数量的评估才能收敛。当单个任务评估代价极高（如需要人工评判或长时间运行）时，HGM 的样本效率优势可能被稀释，需要更多的预算才能获得可靠的 CMP 估计。

- **基准的代表性**。当前实验验证集中在 SWE-Verified 和 Polyglot 两个编码基准上。这些基准能否完全代表一般编程能力仍存疑，发现的最佳代理可能存在一定程度的基准过拟合。论文在 SWE-Lite 上的泛化实验部分缓解了这一担忧，但更广泛的领域外验证仍然缺乏。

### 3. 局限与已知失效模式

**元生产力-性能不匹配的残留风险**。尽管 HGM 通过 CMP 估计显著缓解了即时性能与长期自我改进潜力之间的不匹配（Table 1 中加权相关性从 SICA 的 0.444 提升至 0.778），但这一不匹配并未完全消除。CMP 估计本质上仍是基于观测比例的近似，当谱系内样本量不足时，估计偏差可能导致选择次优的父代理。这一风险在搜索早期（谱系尚未充分展开）尤为突出。

**SICA 的上下文窗口溢出**。在 SWE-Verified-60 实验中，SICA 因上下文窗口溢出而陷入无限循环，消耗 45% 预算后无法继续。这一失效模式揭示了固定交替评估策略在长序列自我修改中的脆弱性——代理的上下文可能随着修改轮次增加而膨胀，最终超出模型限制。HGM 的解耦设计部分规避了这一问题（因为评估是细粒度的，不强制全量评估），但并未从根本上解决上下文膨胀的挑战。

**异步并行的近似误差**。HGM-Async 的异步并行实现使用“最新可用数据”进行决策，这意味着某些迭代可能基于尚未完全更新的树信息做出选择。论文未量化这一近似对搜索质量的影响，但理论上可能导致次优的扩展/评估决策。

**CMP 估计的理论-实践差距**。定理 1 假设访问的是真实 CMP 先知，而实际使用的是基于有限样本的估计量 $\widehat{\mathrm{CMP}}(a) = \frac{n_{\mathrm{success}}^{C}(a)}{n_{\mathrm{success}}^{C}(a) + n_{\mathrm{failure}}^{C}(a)}$。当谱系内评估次数不足时，这一估计可能严重偏离真实 CMP，导致 HGM 偏离哥德尔机器的最优行为。论文未提供 CMP 估计的收敛速率或置信区间分析。

### 4. 开放问题

1. **跨模态的 CMP 推广**。能否将谱系元生产力的思想推广到权重级别的自我修改？在直接调整神经网络权重的设定下，“谱系”和“后代”的概念需要重新定义，CMP 的聚合方式也可能需要适应连续参数空间的特点。

2. **非可重置环境下的 CMP 定义**。在连续任务或非确定性环境中，同一代理-任务对的重复评估可能产生不同结果。如何重新定义 CMP 以保持其对自我改进潜力的指示作用？可能需要引入时间折扣或不确定性量化机制。

3. **CMP 估计的方差缩减**。如何进一步降低 CMP 估计的方差，使自我改进在更严格的样本预算下也能可靠进行？可能的路径包括分层抽样、贝叶斯先验的引入，或利用代理间的相似性进行信息共享。

4. **元策略的提炼与迁移**。HGM 发现的自我改进轨迹是否可以提炼出一般性的元策略，用于指导其他类型的自我改进系统？例如，从成功的谱系中提取修改模式，作为新搜索的初始化或先验。

5. **与人类工程师的协同**。论文展示了 HGM 发现的代理在 SWE-Bench Lite 上匹配甚至超越最佳人类设计的代理。一个自然的延伸是探索人机协同的自我改进范式——人类工程师的干预能否作为 CMP 估计的额外信号，加速搜索收敛？

## 原文 PDF

![[paperPDFs/ICLR_2026/Huxley_Gödel_Machine_Human_Level_Coding_Agent_Development_by_an_Approximation_of_the_Optimal_Self_Improving_Machine.pdf]]
