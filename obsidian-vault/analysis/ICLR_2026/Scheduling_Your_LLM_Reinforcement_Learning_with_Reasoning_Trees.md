---
title: "Scheduling Your LLM Reinforcement Learning with Reasoning Trees"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/Scheduling_Your_LLM_Reinforcement_Learning_with_Reasoning_Trees.pdf
openreview_forum_id: V4zln7XiJj
aliases:
- RSRTS
- SYLRLRT
tags:
- ICLR_2026
- topic/reinforcement_learning_planning_agents
- topic/reinforcement_learning_planning_agents/deep_rl
core_operator: "推理树的结构集中性（即错误路径集中在少数关键决策节点）决定了查询的可学习性。通过有限的节点编辑即可显著提升准确率，因此推理树的结构特征（而非表面准确率）是调度效果的根本驱动力。"
primary_logic: "通过构建近似推理树并定义推理分数（r-score），可以在训练前量化查询在有限节点编辑预算下的潜在准确率增益，并据此建立从“易”（高r-score）到“难”（低r-score）的课程调度，从而更高效地指导RLVR训练，提升数据效率和最终推理能力。"
claims:
- "使用推理分数（r-score）筛选出的前1/3数据训练的模型，其训练准确率和测试准确率均显著优于基于准确率筛选或随机选择的方法。"
- "Re-Schedule方法在六个数学推理基准上平均准确率（48.5%）达到当前最优，比准确率调度基线（ACC_sigmoid）提升最多3.2个百分点，比GRPO提升最高4.2个百分点。"
- "训练过程中平均最小修正节点数（MCN）持续下降，验证了RLVR训练实质上是对推理树决策节点的优化过程。"
- "Six math benchmarks (AIME24, AIME25, AMC23, MATH500, Minerva Math, OlympiadBenc... 上 Average accuracy (avg@32) = 48.5 (Re-Schedule_sigmoid, Qwen2.5-Math-7B)"
---

# Scheduling Your LLM Reinforcement Learning with Reasoning Trees

> [!tip] 核心洞察
> 通过构建近似推理树并定义推理分数（r-score），可以在训练前量化查询在有限节点编辑预算下的潜在准确率增益，并据此建立从“易”（高r-score）到“难”（低r-score）的课程调度，从而更高效地指导RLVR训练，提升数据效率和最终推理能力。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 基于推理树的大语言模型强化学习调度 |
| 英文题名 | Scheduling Your LLM Reinforcement Learning with Reasoning Trees |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=V4zln7XiJj); [GitHub](https://github.com/zz-haooo/Re-Schedule) |
| Topic | #topic/reinforcement_learning_planning_agents #topic/reinforcement_learning_planning_agents/deep_rl |
| Method | Re-Schedule (Reasoning Tree Schedule) |
| Dataset | Six math benchmarks (AIME24, AIME25, AMC23, MATH500, Minerva Math, OlympiadBench), Six math benchmarks (as above) |

> [!tip] 效果简介
> - Six math benchmarks (AIME24, AIME25, AMC23, MATH500, Minerva Math, OlympiadBenc... 上，Average accuracy (avg@32) 为 48.5 (Re-Schedule_sigmoid, Qwen2.5-Math-7B)，对比 46.6 (ACC_sigmoid)，变化 +1.9% (max +3.7% on Minerva)。
> - Six math benchmarks (as above) 上，Average accuracy (avg@32) 为 44.5 (Re-Schedule_sigmoid, Qwen2.5-7B)，对比 41.3 (ACC_sigmoid)，变化 +3.2%。
> - Six math benchmarks (as above) 上，Average accuracy (avg@32) 为 48.5 (Re-Schedule_sigmoid, Qwen2.5-Math-7B)，对比 44.3 (GRPO)，变化 +4.2%。

## 概述

### 核心问题

在大语言模型的强化学习与可验证奖励（RLVR）训练中，现有数据调度方法普遍依赖基于最终答案准确率的指标来评估查询难度。这一做法忽略了推理过程的内在结构，导致对查询真实学习难度的系统性误判：低准确率但推理树结构简单的查询（仅需少量关键节点修正即可大幅提升正确率）被错误标记为“困难”，而高准确率但结构高度分散的查询则可能被忽略。这种误判直接降低了训练效率，使得模型在有限的计算资源下难以最大化性能增益。

### 核心洞察

本文的核心发现是：**推理树的结构集中性**——即错误路径是否集中在少数关键决策节点上——才是决定查询可学习性的根本驱动力。基于此，作者提出了**推理分数（r-score）**，一种在训练前即可量化查询潜在准确率增益的树结构指标。r-score 通过构建近似推理树，在给定的节点编辑预算下计算最大可达的准确率提升，从而从结构层面而非表面准确率层面评估查询的学习潜力。

### 方法定位

**Re-Schedule（Reasoning Tree Schedule）** 是一种基于推理树结构的课程调度算法。其方法谱系定位如下：

- **所属范式**：RLVR 训练中的数据调度 / 课程学习。
- **与现有方法的本质差异**：现有调度方法（如 ACC_sigmoid、LPPO、Seed-GRPO）以路径准确率或不确定性为调度信号；Re-Schedule 以推理树的**结构可学习性**（r-score）为信号，在训练前即完成查询难度的结构感知排序。
- **在知识库中的位置**：Re-Schedule 将“推理过程的结构化表征”引入数据调度，连接了推理树分析与强化学习课程设计两个方向。其调度策略为**从易到难**（easy-to-hard）的课程：高 r-score（结构简单、编辑收益大）的查询优先训练，低 r-score（结构复杂、编辑收益小）的查询延后训练。

### 方法框架

Re-Schedule 包含三个核心模块：

1. **推理树构建**：对每个查询，从基模型采样多条解路径，构建固定结构的 k 叉近似推理树（默认 k=4, 深度 d=4, token 间隔 l=200）。
2. **推理分数计算**：基于树结构，计算每个节点的局部 r-score（选择最优子分支可获得的准确率增益），再在有限节点编辑预算 M 下，通过选择非冲突节点最大化总和，得到查询的整体 r-score。
3. **动态权重调度**：利用 r-score 和训练轮次 t，通过插值因子 α 平滑地将训练重心从高 r-score 查询过渡到低 r-score 查询，形成课程。

### 主要结果

- 在六个数学推理基准（AIME24/25、AMC23、MATH500、Minerva Math、OlympiadBench）上，Re-Schedule 在 Qwen2.5-Math-7B 上取得平均准确率 **48.5%**（avg@32），较准确率调度基线 ACC_sigmoid 提升最高 **3.2 个百分点**，较标准 GRPO 提升最高 **4.2 个百分点**。
- 在 Qwen2.5-7B 上，Re-Schedule 较 ACC_sigmoid 提升 **3.2 个百分点**（44.5% vs 41.3%）。
- 训练过程中平均最小修正节点数（MCN）持续下降，验证了 RLVR 训练本质上是对推理树决策节点的逐步优化。
- 使用 r-score 筛选的前 1/3 数据训练的模型，在训练准确率和测试准确率上均显著优于基于准确率筛选或随机选择的方法。
- 方法在 Qwen3-4B-Base 上同样有效（Avg. 48.8 vs GRPO 44.5 / ACC 46.6），并在代码生成任务 LiveCodeBench v5 上取得 pass@1 26.3、pass@4 37.8，优于基线。

### 局限与开放问题

Re-Schedule 的离线树构建带来约 **48.5%** 的额外训练时间开销（默认配置），且固定结构的近似推理树可能无法完整捕捉真实推理的全部复杂性。目前验证主要限于数学推理和简单代码生成任务，向多模态推理、长链条规划等任务的泛化性尚待检验。此外，如何在更低的计算代价下构建更精准的推理树近似，以及能否将 r-score 与在线动态更新机制结合，仍是值得探索的方向。

## 背景与动机

### 大语言模型强化学习的推理瓶颈

基于强化学习的验证器反馈训练（RLVR）已成为提升大语言模型复杂推理能力的主流范式。GRPO（Shao et al., 2024）等方法通过组内相对优势估计优化策略，在数学推理等任务上取得了显著进展。然而，RLVR训练的效率高度依赖于训练数据的质量与调度策略——并非所有查询对模型能力提升的贡献相等。

现有数据调度方法普遍采用**基于路径的准确率指标**（如最终答案的正确率）来评估查询难度，并据此构建课程学习策略。例如，ACC_sigmoid方法直接利用查询准确率通过sigmoid函数计算训练权重，LPPO（Chen et al., 2025b）则基于准确率梯度动态调整权重。这种做法的隐含假设是：低准确率的查询更难，应被赋予更高的训练权重。

### 准确率指标的失效：结构复杂性的忽视

然而，上述假设存在根本性缺陷：**准确率指标忽略了推理树的内在结构**。一个查询可能因少数关键推理步骤的错误而呈现低准确率，但其推理树结构本身可能极为简单——仅需修正少量决策节点即可大幅提升性能。相反，一个高准确率的查询可能拥有高度分支的复杂推理结构，其剩余错误分散在多个独立分支中，修正难度极大。

Figure 1(a)直观展示了这一现象：简单推理树q1仅需2次节点编辑即可从25%准确率提升至100%，而复杂推理树q2需要4次编辑才能从50%提升至87.5%。Figure 1(b)进一步揭示，尽管q1初始准确率更低，但其训练效率（学习曲线斜率）远高于q2——这说明**推理树的结构集中性（即错误路径集中在少数关键决策节点）才是决定查询可学习性的根本因素**。

### 动机验证：潜力样本与停滞样本

为验证上述洞察，论文通过实验将训练数据分为两类（Figure 2）：
- **潜力样本**：低初始准确率但高推理分数（r-score）的查询，其学习曲线陡峭，训练效率高。
- **停滞样本**：高初始准确率但低r-score的查询，其学习曲线平坦，训练收益有限。

这一发现揭示了一个关键矛盾：基于准确率的调度策略会将停滞样本误判为“简单”而降低其权重，同时将潜力样本误判为“困难”而过度关注——这种错配直接损害了RLVR的收敛速度和最终性能。

### 核心问题

因此，RLVR数据调度的核心瓶颈在于：**如何在不依赖训练过程反馈的前提下，先验地量化查询的真实学习难度？** 这需要一个能够穿透表面准确率、直接刻画推理树结构可学习性的度量指标。

## 核心创新

### 从路径准确率到结构可学习性的范式转换

现有RLVR数据调度方法（如**ACC_sigmoid**、**LPPO** (Chen et al., 2025b)、**Seed-GRPO** (Chen et al., 2025a)）的核心瓶颈在于：它们依赖基于路径的准确率指标（如最终答案准确率）来评估查询难度，忽略了推理树的内在结构。这导致对查询真实学习难度的错误估计——低准确率但结构简单的查询可能被误判为困难而被过度训练，而高准确率但结构复杂的查询可能被忽略，从而降低训练效率。

Re-Schedule的关键创新在于**将调度依据从表面的路径准确率转换为推理树的结构可学习性**。其因果调控变量是推理树的结构集中性——即错误路径集中在少数关键决策节点的程度。这种集中性决定了查询在有限节点编辑预算下的潜在准确率增益：结构越集中，越容易通过少量修正获得显著提升。

### 核心机制：推理分数（r-score）

Re-Schedule引入推理分数（r-score）作为查询学习潜力的先验量化指标。r-score的设计逻辑分为两个层次：

**节点级r-score**衡量单个决策节点的局部学习潜力。对于节点$n_i$，其r-score定义为通过选择最佳子分支并剪枝其他分支所能获得的最大准确率增益：

$$R(n_i) = \max_{n_{\mathrm{child}} \in \mathcal{C}(n_i)} \mathrm{ACC}[\mathcal{N}_{\mathrm{leaf}} \setminus \mathcal{L}(n_i) \cup \mathcal{L}(n_{\mathrm{child}})] - \mathrm{ACC}[\mathcal{N}_{\mathrm{leaf}}]$$

**查询级r-score**在有限编辑预算$M$下，从非冲突节点集合中最大化总r-score：

$$R(q) = \max_{\substack{N^* \subseteq N, |N^*| = M}} \sum_{n_i \in N^*} R(n_i)$$

这一形式化将查询的学习难度定义为：在有限的策略修正成本下，能够达到的最大性能提升空间。高r-score意味着查询的结构集中性高，少量关键节点修正即可带来显著准确率增益，因此属于“易学”样本。

### 从r-score到课程调度

Re-Schedule将r-score映射为动态训练权重，构建从易到难的课程学习。其权重调度机制通过插值因子$\alpha$实现从高r-score（简单）到低r-score（困难）的平滑过渡：

$$\alpha(R(q), t) = (1 - \gamma(t)) R(q) + \gamma(t) (1 - R(q))$$

其中$\gamma(t)$为时间相关的调度函数（支持线性$\gamma(t)=t/T$和sigmoid $\gamma(t)=\sigma(t/T-0.5)$两种方案）。最终训练权重通过排序映射到$[\omega_{\min}, \omega_{\max}]$区间：

$$\omega = \mathrm{rank}(\alpha)\% \cdot \omega_{\max} + (1 - \mathrm{rank}(\alpha)\%) \cdot \omega_{\min}$$

### 相对于基线的核心差异

与基于准确率的调度方法相比，Re-Schedule的changed slot集中在**训练权重函数$\omega$的计算依据**：

| 维度 | 基线方法（ACC-based） | Re-Schedule |
|------|---------------------|-------------|
| 权重依据 | 路径准确率$\mathrm{ACC}(q)$ | 推理分数$R(q)$（r-score） |
| 信息粒度 | 最终答案正确性 | 推理树节点级结构特征 |
| 评估时机 | 训练过程中动态测量 | 训练前一次性构建（静态r-score） |
| 调度策略 | 基于表面难度 | 基于结构可学习性 |

这一差异的根本驱动力在于：推理树的结构特征（而非表面准确率）是调度效果的根本驱动力。实验验证了这一观点——训练过程中平均最小修正节点数（MCN）持续下降（Figure 4(a)），表明RLVR训练实质上是对推理树决策节点的优化过程。使用r-score筛选出的前1/3数据训练的模型，其训练准确率和测试准确率均显著优于基于准确率筛选或随机选择的方法（Figure 4(b)(c)），证实了r-score对查询学习潜力的准确量化能力。

## 整体框架

![[assets/figures/papers/paper_list_l43_https_openreview_net_forum_id_V4zln7XiJj/figures/003_Figure_3.jpg]]
*Figure 3: Overview of the Reasoning Tree Schedule (Re-Schedule) Algorithm.(a) Tree Construction: For each query, an approximate reasoning tree is constructed by sampling multiple solution paths from a base model (Note: This figureis for illustrative purposes only; our experiments use a tree with a depth of 4 and a width of 4, i.e., k = 4, d = 4.). (b) R-Score Calculation: The tree’s structure is analyzed to compute the r-score, a metric quantifying the query’s learning potential. (c) Dynamic Weighting: The r-scores are used to dynamically weight each query during training, forming a curriculum that progresses from structurally simple (easy) to complex (hard) examples*

![[assets/figures/papers/paper_list_l43_https_openreview_net_forum_id_V4zln7XiJj/figures/001_Figure_1.jpg]]
*Figure 1: (a) A simple reasoning tree (q1) requires less node editing for performance improvement than a complex one (q2). (b) Consequently, q1 shows high training efficiency (steep learning curve) despite low initial accuracy, while q2’s complex structure leads to low efficiency. (c) Our method leverages this structural insight to significantly outperform baselines on various datasets*

Re-Schedule（Reasoning Tree Schedule）方法的核心思想是：**通过构建近似推理树并从中提取结构特征（推理分数 r-score），在训练前量化每个查询的真实学习潜力，进而建立从易到难的课程调度，替代传统基于路径准确率的调度策略。**

整个 pipeline 由三个顺序模块构成，如图 3 所示：

### 模块一：推理树构建（Tree Construction）

对于每个查询 $q$，从基模型 $\pi_{\Theta}$ 采样多条解路径，构建一个固定结构的 $k$ 叉近似推理树。树的结构参数包括：
- 分支因子 $k = 4$
- 最大深度 $d = 4$
- token 间隔 $l = 200$（即每 $l$ 个 token 处进行分支采样）

每条路径从根节点到叶节点代表一条完整推理链，叶节点的正确性由答案验证器判定。通过这种固定结构近似，方法在可控制的计算开销下捕获了查询的推理结构特征。

### 模块二：推理分数计算（R-Score Calculation）

基于构建的推理树，计算两个层次的推理分数：

1. **节点 r-score**：对树中每个非叶节点 $n_i$，计算通过选择最佳子分支并剪枝其余分支所能获得的最大准确率增益：
   $$R(n_i) = \max_{n_{\mathrm{child}} \in \mathcal{C}(n_i)} \mathrm{ACC}[\mathcal{N}_{\mathrm{leaf}} \setminus \mathcal{L}(n_i) \cup \mathcal{L}(n_{\mathrm{child}})] - \mathrm{ACC}[\mathcal{N}_{\mathrm{leaf}}]$$
   该值反映该节点处的局部学习潜力——高 r-score 意味着只需在少数关键决策点修正即可大幅提升准确率。

2. **查询 r-score**：在有限节点编辑预算 $M$ 下，从非冲突节点集合中选取 $M$ 个节点，最大化总 r-score：
   $$R(q) = \max_{\substack{N^* \subseteq N, |N^*| = M}} \sum_{n_i \in N^*} R(n_i)$$
   查询的 r-score 越高，表明其推理树结构越集中（错误路径集中在少数关键节点），可学习性越强。

### 模块三：动态权重调度（Dynamic Weighting）

利用 r-score 和训练轮次 $t$ 动态调整每个查询的训练权重，实现课程学习：

1. **动态插值因子**：随时间 $t$ 从偏向高 r-score（简单查询）平滑过渡到低 r-score（困难查询）：
   $$\alpha(R(q), t) = (1 - \gamma(t)) R(q) + \gamma(t) (1 - R(q))$$
   其中 $\gamma(t)$ 采用线性或 sigmoid 调度函数。

2. **最终训练权重**：基于插值因子的排序位置映射到 $[\omega_{\min}, \omega_{\max}]$ 区间：
   $$\omega = \mathrm{rank}(\alpha)\% \cdot \omega_{\max} + (1 - \mathrm{rank}(\alpha)\% ) \cdot \omega_{\min}$$
   默认 $\omega_{\min}=0.5$，$\omega_{\max}=2.0$。

该权重直接乘入 GRPO 的 token 级目标函数中，调制每个查询对总损失的贡献。

### 输入输出流

- **输入**：训练查询集 $\mathcal{D}$，基模型 $\pi_{\Theta}$
- **预处理阶段**：对每个查询采样构建推理树 → 计算 r-score → 存储为静态特征（训练前一次性完成）
- **训练阶段**：每轮根据 r-score 和当前轮次 $t$ 动态计算权重 $\omega(q,t)$ → 加权 GRPO 训练
- **输出**：优化后的策略模型

### 关键设计决策

- **静态 r-score**：推理树构建和 r-score 计算仅在训练前执行一次。实验表明，动态更新三次 r-score 与静态方案性能相当（48.9% vs 48.3%），但静态方案节省大量计算开销。
- **从易到难调度**：Re-Schedule 采用从高 r-score 到低 r-score 的课程顺序，消融实验证实该顺序比反向调度（从难到易）准确率高出约 3.6 个百分点。
- **节点级修正优于分支级剪枝**：r-score 基于节点级修正（Fix）而非分支级剪枝（Pruning）计算，更贴合 RLVR 训练过程中对关键决策节点的细粒度优化。

## 核心模块与公式推导

Re-Schedule 方法围绕三个核心模块构建：推理树构建、推理分数计算和动态权重调度。以下逐一展开其技术细节。

### 模块一：推理树构建

对于每个查询 $q$，从基模型采样多条解路径，构建一棵固定结构的 $k$ 叉近似推理树。树的结构由三个超参数定义：分支因子 $k$、最大深度 $d$ 和 token 间隔 $l$（默认 $k=4, d=4, l=200$）。每个节点 $n_i$ 对应一个推理步骤，其质量由该节点所有叶节点后代的平均正确率衡量：

$$\operatorname{ACC}(S) = \frac{\sum_{n_j \in S} \mathbb{I}(n_j \text{ is correct})}{|S|}$$

其中 $S$ 为叶节点集合，$\mathbb{I}(\cdot)$ 为指示函数。该模块将查询的推理空间压缩为可控的树结构，为后续结构分析提供基础。

### 模块二：推理分数计算

推理分数（r-score）量化查询在有限节点编辑预算下的最大准确率增益，分为节点级和查询级两个层次。

**节点 r-score**：对于节点 $n_i$，其 r-score 定义为选择最佳子分支并剪枝其余分支后，叶节点集合准确率的最大提升量：

$$R(n_i) = \max_{n_{\mathrm{child}} \in \mathcal{C}(n_i)} \mathrm{ACC}[\mathcal{N}_{\mathrm{leaf}} \setminus \mathcal{L}(n_i) \cup \mathcal{L}(n_{\mathrm{child}})] - \mathrm{ACC}[\mathcal{N}_{\mathrm{leaf}}]$$

其中 $\mathcal{C}(n_i)$ 为 $n_i$ 的子节点集合，$\mathcal{L}(n_i)$ 为 $n_i$ 的叶节点后代集合，$\mathcal{N}_{\mathrm{leaf}}$ 为全部叶节点。该公式捕捉了单个决策节点的局部可学习性：若某节点的一个子分支远优于其他分支，则该节点具有高 r-score，意味着少量编辑即可显著提升准确率。

**查询 r-score**：在有限编辑预算 $M$ 下，从所有非冲突节点中选取 $M$ 个，最大化其 r-score 之和：

$$R(q) = \max_{\substack{N^* \subseteq N, |N^*| = M}} \sum_{n_i \in N^*} R(n_i)$$

其中 $N$ 为所有非叶节点集合。该公式通过组合优化，将查询的整体学习潜力量化为其推理树中关键决策节点的集中程度：结构越集中（即错误路径集中在少数节点），$R(q)$ 越高，查询越“易学”。

### 模块三：动态权重调度

利用 r-score 构建从易到难的课程学习。首先通过插值因子 $\alpha$ 实现从高 r-score（简单）到低 r-score（困难）的平滑过渡：

$$\alpha(R(q), t) = (1 - \gamma(t)) R(q) + \gamma(t) (1 - R(q))$$

其中 $\gamma(t)$ 为时间调度函数，可选线性 $\gamma(t) = t/T$ 或 sigmoid $\gamma(t) = \sigma(t/T - 0.5)$，$T$ 为总训练轮次。随后将 $\alpha$ 映射为最终训练权重：

$$\omega = \mathrm{rank}(\alpha)\% \cdot \omega_{\mathrm{max}} + (1 - \mathrm{rank}(\alpha)\% ) \cdot \omega_{\mathrm{min}}$$

其中 $\mathrm{rank}(\alpha)\%$ 为 $\alpha$ 在所有查询中的百分位排序，$\omega_{\mathrm{max}}$ 和 $\omega_{\mathrm{min}}$ 为权重边界（默认 2.0 和 0.5）。该权重直接作用于 GRPO 的 token 级目标函数：

$$\mathcal{I}(\theta) = \mathbb{E}_{q \sim \mathcal{D}, \{o_i\}_{i=1}^G \sim \pi_{\Theta\mathsf{d}}(\cdot|q)} \left[ \frac{1}{\sum_{i=1}^G |o_i|} \sum_{i=1}^G \sum_{t=1}^{|o_i|} \min(r_{i,t} A_{i,t}, \mathrm{clip}(r_{i,t}, 1-\varepsilon, 1+\varepsilon) A_{i,t}) \right]$$

其中优势函数采用组归一化：

$$A_{i,t} = \frac{R_i - \mathrm{mean}(\{R_k\}_{k=1}^G)}{\mathrm{std}(\{R_k\}_{k=1}^G) + \delta}$$

**关键设计决策**：r-score 采用静态计算（训练前一次性构建树并计算分数），实验表明其与动态更新三次的性能相当（48.3% vs 48.9%），但大幅节省计算开销。节点级修正指标（Fix）优于分支级剪枝指标（Pruning），验证了细粒度节点编辑与 RLVR 训练过程的一致性。

## 实验与分析

### 核心发现：推理树结构调度优于路径准确率调度

Re-Schedule在两个基础模型、六个数学推理基准上均取得最优平均准确率，验证了推理树结构作为调度信号的根本有效性。

**Qwen2.5-Math-7B 主结果（Table 1）**：Re-Schedule_sigmoid 达到 **48.5** 的平均准确率（avg@32），超越所有经典RLVR方法和调度基线。具体而言，相比准确率调度基线 ACC_sigmoid（46.6）提升 **+1.9** 个百分点，相比标准 GRPO（44.3）提升 **+4.2** 个百分点。在 Minerva Math 上增益最大（+3.7），在 AIME25 上增益为 +1.1，表明方法在不同难度基准上均有稳定提升。Re-Schedule_linear 以 48.3 紧随其后，同样优于所有基线。


![[assets/figures/papers/paper_list_l43_https_openreview_net_forum_id_V4zln7XiJj/figures/007_Table_1.jpg]]
*Table 1: Main benchmark results on Qwen2.5-Math-7B. All values are accuracies multiplied by 100. Best results are in bold*

**Qwen2.5-7B 主结果（Table 2）**：Re-Schedule_sigmoid 平均准确率达到 **44.5**，相比 ACC_sigmoid（41.3）提升 **+3.2** 个百分点，相比 GRPO（40.7）提升 +3.8 个百分点。值得注意的是，Qwen2.5-7B 作为通用基座模型（非数学专用），Re-Schedule 带来的相对增益更大，说明推理树结构信息在模型推理能力较弱时具有更强的指导价值。


![[assets/figures/papers/paper_list_l43_https_openreview_net_forum_id_V4zln7XiJj/figures/008_Table_2.jpg]]
*Table 2: Main benchmark results on Qwen2.5-7B. All values are accuracies multiplied by 100. Best results are in bold*

**跨模型架构泛化（Table 13）**：在 Qwen3-4B-Base 上，Re-Schedule 以 **48.8** 的平均准确率显著超越 GRPO（44.5）和 ACC（46.6），验证了方法对不同模型架构和规模的适应性。


![[assets/figures/papers/paper_list_l43_https_openreview_net_forum_id_V4zln7XiJj/figures/020_Table_13.jpg]]
*Table 13: Performance comparison on Qwen3-4B-Base*

**领域泛化（Table 15）**：在代码生成任务 LiveCodeBench v5 上，Re-Schedule 取得 pass@1 **26.3** 和 pass@4 **37.8**，优于 GRPO（pass@1 22.1, pass@4 34.0）和 ACC（pass@1 24.7, pass@4 36.6），表明推理树调度可泛化至数学之外的序列生成任务。

### 调度机制的有效性验证

**从易到难 vs 从难到易（Table 6）**：Re-Schedule（从易到难）平均准确率 48.3，显著优于 Reverse Schedule（从难到易）的 44.7，差距达 **+3.6** 个百分点。这证实了课程学习的核心假设：先学习结构简单（高 r-score）的查询可为后续复杂查询提供更好的模型初始化。

**节点级修正 vs 分支级剪枝（Table 7）**：节点级修正指标（Fix）在所有六个基准上均优于分支级剪枝指标（Pruning），平均准确率 48.3 vs 46.1。这一结果与 Figure 4(a) 中 MCN 持续下降的现象一致——RLVR 训练本质上是对推理树中关键决策节点的逐点优化，而非对整个推理分支的粗粒度替换。


![[assets/figures/papers/paper_list_l43_https_openreview_net_forum_id_V4zln7XiJj/figures/006_Figure_4.jpg]]
*Figure 4: (a) The average MCN decreases over time, indicating successful tree optimization. (b) & (c) To compare metrics, we train models on the top 1/3 of data selected by each. The plots show the resulting (b) training accuracy and (c) test accuracy. The model used is Qwen2.5-Math-7B*

**静态 vs 动态 r-score（Table 14）**：训练前一次性计算静态 r-score 达到 48.3，而动态更新三次 r-score 仅小幅提升至 48.9（+0.6）。考虑到动态更新需额外推理计算，静态方案以极低的计算代价获得了绝大部分性能增益，实用性更强。

### 消融实验：参数敏感性分析

**树构建参数（Table 3）**：默认配置（分支因子 k=4，深度 d=4）取得最佳平均准确率 48.3。减小树规模（k=3, d=5）降至 46.9，增大分支但减小深度（k=5, d=3）为 47.0。单独消融显示（Table 10, Table 11），k=4 和 d=4 分别为各自维度的最优点，表明适中的树宽和深度能最好地平衡结构信息完整性与采样噪声。

**权重超参数（Table 4）**：默认设置 ω_min=0.5, ω_max=2.0 达到最高平均准确率 48.5。权重区间过窄（如 0.8/1.2）会削弱调度效果（47.0），过宽（如 0.2/2.0）则可能过度放大简单样本或压制困难样本（47.8）。

**Token 间隔 l（Table 9）**：l=200 为最优，l=100 时性能略有下降（48.0），l=400 时进一步降低（47.4）。过小的间隔导致树节点过于密集、分支差异不显著；过大的间隔则使树结构过于稀疏，丢失关键决策信息。

**节点编辑预算 M（Table 12）**：M=3 为默认最优值。M 过小（M=1）无法充分捕捉多节点联合优化的潜力，准确率降至 47.1；M 过大（M=5）可能引入噪声节点，性能略降至 47.9。

### 计算代价与性能权衡

**Table 5 和 Figure 5** 系统分析了树规模与计算开销的关系。默认配置（4⁴ 树）带来 **+48.5%** 的额外训练时间（总计 22.67 小时），换取 **+4.0** 的平均性能增益。缩小树规模可降低开销：3³ 树仅增加 7.5% 时间，但增益降至 +3.0；4³ 树增加 12.4% 时间，增益 +3.4。Figure 5 显示，sigmoid 调度在相同树规模下始终优于 linear 调度，且性能增益随树规模增大呈边际递减趋势——从 4³ 到 4⁴ 的增益提升已趋于平缓。

### 训练过程分析：MCN 下降验证树优化假设

**Figure 4(a)** 展示了训练过程中平均最小修正节点数（MCN）的持续下降趋势。无论目标准确率设为 60%、80% 还是 100%，MCN 均随训练步数单调递减。这一现象直接验证了论文的核心假设：RLVR 训练的实质是对推理树中关键决策节点的逐步修正。随着模型学会在关键分支点做出正确选择，将推理树修正至完全正确所需的节点编辑数自然减少。

### 指标比较：r-score 优于准确率

**Figure 4(b)(c)** 对比了分别使用 r-score、准确率和随机选择筛选前 1/3 数据训练的模型性能。在训练准确率上，r-score 筛选的模型快速超越准确率筛选和随机选择，且最终收敛到更高水平。在测试准确率上，r-score 筛选的模型全程保持领先，验证了 r-score 作为查询学习潜力指标的有效性——它能在训练前识别出那些低准确率但结构简单、具有高学习效率的“潜力样本”，而非被表面准确率误导。

### 稳定性分析

**Table 8** 显示 Re-Schedule 在不同随机种子下的结果方差极小。以 AIME24 为例，三次运行结果为 35.2±0.1，AIME25 为 26.5±0.3，平均准确率 48.4±0.1。这表明推理树构建和 r-score 计算具有高度稳定性，方法对采样随机性不敏感。

### 失败模式与局限

1. **计算开销瓶颈**：默认配置下 +48.5% 的训练时间增加在大规模数据或快速迭代场景中可能不可接受。虽然可通过缩小树规模（如 3³ 仅 +7.5%）换取效率，但性能增益也会相应缩水。
2. **固定树结构的近似误差**：k=4, d=4 的固定 k 叉树可能无法完整捕捉某些查询的真实推理拓扑（如深度超过 4 或分支不均匀的推理链），导致 r-score 估计偏差。
3. **领域泛化待验证**：目前仅在数学推理和简单代码生成上验证有效，对多模态推理、长链条规划等更复杂任务的适用性尚不明确。
4. **静态 r-score 的信息损失**：训练前一次性计算 r-score 无法利用训练过程中模型能力演化带来的结构变化信息。虽然实验表明动态更新收益有限（+0.6），但在某些特定场景（如模型能力快速跃升的阶段）可能不是最优选择。

## 方法谱系与知识库定位

### 核心瓶颈与因果机制

现有RLVR数据调度方法（如**ACC_sigmoid**、**LPPO**（Chen et al., 2025b）、**Seed-GRPO**（Chen et al., 2025a））普遍依赖基于路径的准确率指标评估查询难度，忽略了推理树的内在结构。这一设计的根本缺陷在于：低准确率但结构简单的查询（仅需少量决策节点修正即可显著提升）可能被误判为困难样本而被降权，而高准确率但结构复杂的查询（存在多个纠缠的错误节点）可能被忽略，从而降低训练效率。

Re-Schedule的核心因果机制在于，推理树的结构集中性（即错误路径集中在少数关键决策节点）决定了查询的可学习性。通过定义推理分数（r-score），该方法在训练前即可量化查询在有限节点编辑预算下的潜在准确率增益，并据此建立从“易”（高r-score）到“难”（低r-score）的课程调度。训练过程中平均最小修正节点数（MCN）的持续下降（Figure 4(a)）直接验证了RLVR训练实质上是对推理树决策节点的优化过程，而非简单的准确率提升。

### 方法谱系与关系定位

Re-Schedule处于RLVR数据调度方法的演进脉络中，其与基线方法的关系可归纳为以下层次：

**标准RLVR框架层**：**GRPO**（Shao et al., 2024）、**SimpleRL-Zoo**（Zeng et al., 2025）、**Eurus-PRIME**（Cui et al., 2025）和**OPO**（Hao et al., 2025a）构成了RLVR训练的基础框架。Re-Schedule在GRPO的token级目标函数中引入数据调度权重ω，不改变底层优化算法本身，因此可与上述框架兼容。

**基于准确率的调度层**：**ACC_sigmoid**直接使用查询准确率ACC(q)计算sigmoid加权权重，是最直接的课程学习基线。**LPPO**（Chen et al., 2025b）基于准确率梯度动态调整权重，属于在线调度方法。Re-Schedule与这些方法的本质区别在于将调度依据从“表面准确率”替换为“结构推理分数”（r-score），从而更精准地捕捉查询的真实学习难度。

**基于不确定性的调度层**：**Seed-GRPO**（Chen et al., 2025a）利用语义多样性或不确定性进行数据选择。Re-Schedule的结构化评估思路与此类方法正交，未来存在结合的可能性。

### 适用边界与局限

**计算开销约束**：离线构建推理树带来额外计算开销（默认4^4树结构增加约48.5%训练时间，Table 5），这在大规模数据或快速迭代场景中可能成为瓶颈。尽管静态r-score（训练前一次性计算）与动态更新三次的性能相当（48.3% vs 48.9%，Table 14），节省了计算开销，但树构建本身的开销仍不可忽略。

**树近似的保真度限制**：推理树的近似依赖于固定的k叉结构（k=4, d=4, l=200），可能无法完整捕捉真实推理树的全部复杂性和动态变化。消融实验表明，默认配置（k=4, d=4）达到最佳性能（Table 3），但更精细的树结构是否能在其他场景下带来额外收益尚不明确。

**任务泛化边界**：目前仅在数学推理任务（六个基准）和简单的代码生成任务（LiveCodeBench v5, Table 15）上验证了有效性。对其他类型复杂推理任务（如多模态推理、长链条规划、开放域问答）的泛化性尚待验证。该方法的核心假设——推理过程可被建模为树结构且错误集中在少数节点——在这些任务中是否成立仍是开放问题。

**静态与动态的权衡**：采用静态r-score（仅训练前计算一次）未利用训练过程中模型演化带来的动态结构信息。虽然实验表明动态更新收益有限，但在模型能力快速变化或数据分布高度非平稳的场景下，静态r-score可能不是最优选择。

### 开放问题

1. **高效树近似构建**：如何在不显著增加计算开销的前提下构建更精准的推理树近似？可能的路径包括利用模型中间层表示进行树结构剪枝，或采用自适应采样策略动态调整分支因子。

2. **在线动态调度机制**：能否将r-score与在线更新机制结合，实现实时动态的课程调度，同时保持较低的计算成本？当前静态方法的成功表明，结构信息本身具有稳定性，但训练过程中模型对查询难度的感知变化可能提供额外的调度信号。

3. **跨领域结构评估泛化**：该方法中基于推理树的结构评估思想是否可以推广至多模态生成、长文本生成等更广泛的序列生成任务？这需要定义适用于不同模态和任务类型的“决策节点”和“编辑预算”概念。

4. **探索-利用权衡的结构化引导**：是否可以将推理树的结构评估与RLVR中的探索-利用权衡结合？高r-score节点可能受益于更多探索（因其具有高学习潜力），而低r-score节点可能需要更多利用（因其结构已接近最优），这种结构化引导可能进一步提高收敛速度和最终性能。

## 原文 PDF

![[paperPDFs/ICLR_2026/Scheduling_Your_LLM_Reinforcement_Learning_with_Reasoning_Trees.pdf]]
