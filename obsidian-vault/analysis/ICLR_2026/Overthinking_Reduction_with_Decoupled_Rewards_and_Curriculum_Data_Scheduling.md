---
title: "Overthinking Reduction with Decoupled Rewards and Curriculum Data Scheduling"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/Overthinking_Reduction_with_Decoupled_Rewards_and_Curriculum_Data_Scheduling.pdf
project_link: null
code_link: https://github.com/pixas/DECS
openreview_forum_id: kdeiRledV6
aliases:
- ORDRCDS
tags:
- ICLR_2026
- topic/reinforcement_learning_planning_agents
- topic/reinforcement_learning_planning_agents/deep_rl
core_operator: "解耦的 token 级别奖励设计（仅对必要推理前缀 NRP 之后的冗余 token 施加负奖励）与自适应课程数据调度（根据当前 batch 的 NRP 比例动态调整简单 prompt 的占比）的协同作用。"
primary_logic: "通过定位必要推理前缀，对 NRP 之前的必要 token 给予充分奖励，并对 NRP 之后的冗余 token 进行精确惩罚，同时利用课程调度防止高熵 token 被过度抑制，可以在不损害推理能力的前提下实现超过 50% 的 token 压缩。"
claims:
- "长度惩罚导致正确的高熵 token 获得负优势，降低其生成概率 (Lemma 2)。"
- "DECS 在七个基准上将推理 token 减少超过 50%，同时 pass@1 平均提升 +2.48 点 (DS-1.5B) 和 +0.8 点 (DS-7B) (Table 1)。"
- "消融实验：移除课程调度（CS）导致性能明显下降，移除解耦奖励（DR）则仍保留约 25% 的冗余 token (Table 3, Fig. 3a)。"
- "DECS 在限制 token 预算下 Pass@K 性能与基础模型重合，实现了几乎无损的压缩 (Fig. 3c, Fig. 8c)。"
---

# Overthinking Reduction with Decoupled Rewards and Curriculum Data Scheduling

> [!tip] 核心洞察
> 通过定位必要推理前缀，对 NRP 之前的必要 token 给予充分奖励，并对 NRP 之后的冗余 token 进行精确惩罚，同时利用课程调度防止高熵 token 被过度抑制，可以在不损害推理能力的前提下实现超过 50% 的 token 压缩。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 通过解耦奖励和课程数据调度减少过度思考 |
| 英文题名 | Overthinking Reduction with Decoupled Rewards and Curriculum Data Scheduling |
| 会议/期刊 | ICLR 2026 (Oral) |
| Links | [paper](https://openreview.net/forum?id=kdeiRledV6) · [GitHub](https://github.com/pixas/DECS) |
| Topic | #topic/reinforcement_learning_planning_agents #topic/reinforcement_learning_planning_agents/deep_rl |
| Method | DECS |
| Dataset | AIME2024 (DS-1.5B), AIME2024 (DS-7B) |

> [!tip] 效果简介
> - AIME2024 (DS-1.5B) 上，Pass@1 为 31.25，对比 27.99 (Base)，变化 +3.26。
> - AIME2024 (DS-1.5B) 上，#Tokens 为 5550，对比 12202 (Base)，变化 -54.5%。
> - AIME2024 (DS-7B) 上，Pass@1 为 51.33，对比 50.65 (Base)，变化 +0.68。

## 概要

大语言推理模型（LRMs）在复杂任务中展现出强大的推理能力，但其固有的“过度思考”（overthinking）现象导致大量冗余 token 消耗，严重制约了实际部署效率。现有方法普遍采用序列级别的长度惩罚来抑制冗余，但本文揭示了这一范式的根本性缺陷：**序列级奖励与 token 级策略优化之间存在严重不对齐**。具体而言，正确的长序列中必要的高熵探索 token 被错误地分配负优势，而短序列中的冗余 token 反而获得正优势——这导致模型在追求效率时抑制了有益的探索行为，破坏了效率与性能的平衡。

针对上述瓶颈，本文提出 **DECS**（Decoupled Rewards and Curriculum Data Scheduling），一种通过解耦奖励和课程数据调度来减少过度思考的方法。DECS 的核心调控旋钮在于两个关键设计的协同作用：

1. **解耦的 token 级奖励**：通过轻量级判断模型定位“必要推理前缀”（Necessary Reasoning Prefix, NRP），仅对 NRP 之后的冗余 token 施加精确的负奖励，而 NRP 内的必要 token 获得充分的正奖励，从根本上消除了序列级惩罚的不对齐问题。
2. **自适应课程数据调度**：根据训练过程中当前 batch 的 NRP 比例动态调整简单 prompt 的占比，防止高熵探索 token 被过度抑制，从而在压缩冗余的同时保持推理能力。

实验结果表明，DECS 在七个基准上实现了超过 50% 的推理 token 压缩，同时 Pass@1 平均提升 +2.48 点（DeepSeek-R1-Distill-1.5B）和 +0.8 点（DeepSeek-R1-Distill-7B）。在限制 token 预算的条件下，DECS 的 Pass@K 性能与基础模型几乎重合，实现了近乎无损的压缩。消融实验进一步验证了课程调度和解耦奖励各自的关键贡献：移除课程调度导致性能明显下降，而仅移除解耦奖励则仍保留约 25% 的冗余 token。

### 大语言模型的“过度思考”困境

大语言模型在数学、编程、科学等复杂推理任务上展现出卓越性能，其核心机制在于生成冗长的推理链（Chain-of-Thought）。然而，这种“先想清楚再回答”的策略带来了严重的推理效率问题：模型倾向于产生远超出必要长度的推理过程，即**过度思考（Overthinking）**。以 DeepSeek-R1-Distill-1.5B 模型为例，其在 AIME2024 基准上的平均推理 token 数高达 12202，而实际达成正确答案所需的最小推理量远低于此。

过度思考不仅造成高昂的推理延迟和计算成本，更本质地反映了模型在效率与性能之间的失衡——模型无法自主判断“何时已经想得足够多”，从而持续消耗资源进行冗余探索。

### 现有方法的根本性缺陷

针对过度思考问题，现有研究主要采用**序列级别的长度惩罚（Length Penalty）**策略，即在正确响应的最终奖励中减去与序列长度成比例的惩罚项：

$$r'(\mathbf{o}_i) = \begin{cases} r(\mathbf{o}_i) - \gamma |\mathbf{o}_i| & \mathbf{o}_i \text{ is correct} \\ r(\mathbf{o}_i) & \text{otherwise} \end{cases}$$

这类方法包括 **ThinkPrune**（Hou et al., 2025）、**TLMRE**（Arora & Zanette, 2025）、**LC-R1**（Cheng et al., 2025）等。然而，序列级别的奖励设计存在两个根本性缺陷，如图 Figure 1（左）所示：

**缺陷一：正确的高熵 token 被错误惩罚。** 在长序列中，正确的推理路径往往包含高熵的探索性 token（如尝试不同解题思路、验证中间结果），这些 token 对最终正确性至关重要。但由于序列级别长度惩罚将负优势均匀分配至所有 token，这些必要的高熵 token 被错误地分配了负优势，导致其生成概率下降。Lemma 2（Appendix A.1）从理论上证明了这一现象：长度惩罚使得正确长序列中高熵 token 的优势期望为负，抑制了模型的有益探索行为。

**缺陷二：短序列中的冗余 token 反而获得正优势。** 序列级别惩罚以整个序列的长度为基准进行组内标准化。当 batch 中同时存在长序列和短序列时，短序列即使包含冗余推理 token，其整体长度仍低于组内平均，因此其 token 反而获得正优势。这导致模型被错误地鼓励在短序列中保留冗余内容，形成“越短越容易被奖励”的扭曲信号。

### 根本瓶颈：序列级惩罚与 token 级优化之间的不对齐

上述缺陷的深层原因在于**奖励粒度与优化粒度之间的根本性不对齐**。当前的强化学习框架（如 GRPO）在 token 级别进行策略优化——每个 token 根据其优势值独立更新生成概率。然而，长度惩罚却仅在序列级别定义——同一序列内的所有 token 共享相同的标量优势值。这种粒度错配使得：

- 无法区分序列内的**必要推理前缀（Necessary Reasoning Prefix, NRP）**与**冗余后缀**；
- 无法对冗余 token 进行精确的、位置感知的惩罚；
- 无法保护 NRP 内的高熵探索 token 免受误伤。

### 本文动机：从“序列惩罚”到“token 解耦”的范式转变

为从根本上解决上述不对齐问题，本文提出 **DECS（Decoupled Rewards and Curriculum Data Scheduling）**，其核心动机在于实现三个关键转变：

1. **从序列级到 token 级的奖励解耦**：通过定位 NRP 边界（即推理链中首次包含最终正确答案的位置），对 NRP 内的必要 token 给予充分的正奖励，仅对 NRP 后的冗余 token 施加精确的负奖励，从而实现“该奖则奖、该罚则罚”的差异化信号。

2. **从静态惩罚到自适应课程调度**：理论分析表明，当 batch 中简单 prompt（NRP 比例高）占比过高时，正确的高熵 token 仍可能被错误惩罚。为此，DECS 引入课程数据调度策略，根据训练过程中 NRP 比例的变化动态调整简单 prompt 的占比，防止对探索性 token 的过度抑制。

3. **效率与性能的帕累托改进**：DECS 的目标并非简单地牺牲性能换取效率，而是通过在正确的位置施加正确的学习信号，实现 token 压缩与推理能力的同步提升。实验表明，DECS 在七个基准上将推理 token 减少超过 50%，同时 pass@1 平均提升 +2.48 点（DS-1.5B），验证了这一目标的可行性。

## 核心方法与创新机理

DECS 的核心创新在于**发现了序列级长度惩罚与 token 级策略优化之间的根本性不对齐**，并针对性地设计了两项关键机制来实现精准的冗余消除，而非简单的“越短越好”。

### 问题洞察：序列奖励的粒度错配

现有方法（如 ThinkPrune、LC-R1）采用序列级别的长度-正确性复合奖励 $r'(\mathbf{o}_i) = r(\mathbf{o}_i) - \gamma |\mathbf{o}_i|$（仅对正确响应施加），这在 token 级优化中引入了两个系统性缺陷（Figure 1 左）：

1. **正确高熵 token 被错误惩罚**：在正确的长序列中，必要的探索性高熵 token 被分配负优势，降低了其生成概率（Lemma 2），抑制了模型的探索能力。
2. **冗余 token 被错误奖励**：在正确的短序列中，即使存在冗余 token，它们仍获得正优势，无法被有效消除。

这种粒度错配的根源在于：**序列级奖励将同一序列内的所有 token 赋予相同的优势信号**，无法区分必要推理与冗余思考。

### 机制一：基于必要推理前缀的解耦 Token 级奖励

DECS 将奖励信号从序列级解耦为 token 级，核心是**定位必要推理前缀**——推理链中首次包含正确答案的最短前缀。

具体而言，DECS 训练一个轻量级判断模型 $\mathcal{M}_{\text{judge}}$（基于 Qwen2.5-1.5B），将推理过程分块并逐块判断是否已包含正确答案。NRP 定义为从起始到首个被判定为“yes”的推理块的拼接：

$$\text{NRP} = \bigoplus_{i=1}^{c^*} s_i, \quad c^* = \min\{ c \in [1, |S|] : j_{s_c} = \text{yes} \}$$

基于 NRP 边界，DECS 为每个 token 分配差异化奖励：

$$r_{i,j} = \begin{cases} r_{+} \cdot \mathbf{1}_{\mathbf{o}_i \text{ is correct}} & j \leq K_{\mathbf{o}_i}^* \lor o_j \notin o_{\text{think}} \lor o_{i,j}=\emptyset \\\\ (r_0 - \frac{(r_{+} - r_0) L_i}{L_{\max}}) \cdot \mathbf{1}_{\mathbf{o}_i \text{ is correct}} & j > K_{\mathbf{o}_i}^* \land o_j \in o_{\text{think}} \end{cases}$$

- **NRP 内的 token**：获得固定高奖励 $r_{+}$（设为 1.1），确保必要推理不被抑制。
- **NRP 后的冗余思考 token**：获得按长度缩放的低奖励（$r_0=1.0$ 为基准，随长度增加而递减），在组内标准化后产生负优势，精确惩罚冗余。

这一设计的关键效果是：**只有真正冗余的 token 才会被抑制，而 NRP 内的高熵探索 token 仍获得充分的正向激励**。

### 机制二：自适应课程数据调度

解耦奖励虽然精准，但会提高正确序列中 NRP 的比例（$\mathcal{R}_m$），导致 batch 内序列长度方差 $\sigma_L$ 减小。根据 Theorem 1，当 $\kappa \sigma_L < C$ 时，正确高熵 token 的期望 logit 变化仍可能为负，即探索行为仍被抑制。

为此，DECS 引入课程提示调度，根据当前 batch 的 NRP 比例动态调整简单 prompt 的占比：

$$\kappa_m = \text{clip}( \kappa_{m-1} + \beta (\mathcal{R}_m - \mathcal{R}_{m-1}), 0, \kappa_m^0 )$$

- 当 NRP 比例上升时，自动增加简单 prompt 的比例，引入更多短序列以维持序列长度方差。
- 超参数 $\beta=0.2$（经网格搜索确定）控制调节速度，防止高熵 token 被过度惩罚。

### 协同效应

两项机制的协同是 DECS 性能的关键。消融实验（Table 3）表明：
- **移除课程调度（w/o CS）**：性能明显下降（Avg Acc 46.31 vs 47.78），验证了 Theorem 1 中方差维持的必要性。
- **移除解耦奖励（w/o DR）**：策略仍保留约 25% 冗余 token（Avg #Tok 5111 vs 4000），验证了序列级奖励的粒度不足。

两者结合，DECS 在七个基准上实现超过 50% 的 token 压缩，同时 pass@1 平均提升 +2.48 点（DS-1.5B）和 +0.8 点（DS-7B），在限制 token 预算下 Pass@K 性能与基础模型几乎重合（Fig. 3c），实现了近乎无损的推理压缩。


DECS 的训练管道由三个协同模块构成，围绕“定位必要推理前缀（NRP）→ 差异化奖励分配 → 自适应数据调度”的逻辑链展开，如图 2 所示。

**输入**：一个提示（prompt）集合，每个提示对应一个数学推理问题及其标准答案 $y^*$。

**模块 1：NRP 检测器**
每条推理轨迹 $\mathbf{o}_i$ 首先被分割为推理块序列 $S = \{s_1, s_2, \dots\}$。一个轻量级判断模型 $\mathcal{M}_{\text{judge}}$（基于 Qwen2.5-1.5B 微调）逐块判断该块是否首次包含最终正确答案：
$$j_{s_c} \sim \mathcal{M}_{\mathrm{judge}}( \cdot \ | \ q, s_c, y^{*} )$$
NRP 定义为从起始到首个被判定为“yes”的推理块的拼接：
$$\mathrm{NRP} = \bigoplus_{i=1}^{c^{*}} s_i, \quad c^{*} = \min\{ c \in [1, |S|] : j_{s_c} = \mathrm{yes} \}$$
该检测器在数学推理数据上训练，但在科学（GPQA-D）和编程（LiveCodeBench）任务上展示了超过 97% 的泛化精度。

**模块 2：解耦的 Token 级奖励分配**
基于 NRP 边界 $K_{\mathbf{o}_i}^*$，为每个 token 计算差异化奖励：
$$r_{i,j} = \begin{cases} r_{+} \cdot \mathbf{1}_{\mathbf{o}_i \text{ is correct}} & j \leq K_{\mathbf{o}_i}^* \lor o_j \notin o_{\text{think}} \lor o_{i,j}=\emptyset \\ (r_0 - \frac{(r_{+} - r_0) L_i}{L_{\max}}) \cdot \mathbf{1}_{\mathbf{o}_i \text{ is correct}} & j > K_{\mathbf{o}_i}^* \land o_j \in o_{\text{think}} \end{cases}$$
其中 $r_{+}=1.1$，$r_0=1.0$。NRP 内部 token 和非思考 token 获得固定的高奖励 $r_{+}$；NRP 之后的冗余思考 token 获得按序列长度 $L_i$ 缩放的低奖励，从而在组内标准化后产生负优势：
$$A_{i,j}^{\mathrm{DECS}} = \frac{r_{i,j} - \mathrm{mean}(r_{1,j}, \dots, r_{G,j})}{\mathrm{std}(r_{1,j}, \dots, r_{G,j})}$$

**模块 3：课程提示调度**
为防止对高熵探索 token 的过度惩罚，根据每个 batch 中正确序列的 NRP 比例 $\mathcal{R}_m$ 动态调整简单 prompt 的占比 $\kappa_m$：
$$\kappa_m = \mathrm{clip}( \kappa_{m-1} + \beta (\mathcal{R}_m - \mathcal{R}_{m-1}), 0, \kappa_m^0 )$$
其中 $\beta=0.2$ 通过网格搜索确定。当 NRP 比例上升（即模型倾向于压缩推理）时，调度器增加简单 prompt 的比例以维持高熵 token 的正向学习信号，从而满足 Theorem 1 中 $\kappa \sigma_L < C$ 的条件。

**输出流**：Token 级优势 $A_{i,j}^{\text{DECS}}$ 被送入标准的 GRPO 策略梯度优化框架（Eq. 1-3），更新策略参数 $\theta$。整个管道在 4×NVIDIA A100 80GB GPU 上运行，NRP 检测器引入约 3.4%~5.1% 的训练时间开销。

三个模块的解耦设计使得消融实验可以独立验证各自贡献：移除课程调度导致性能明显下降，移除解耦奖励则策略仍保留约 25% 的冗余 token。

DECS 的核心设计由三个协同模块构成，分别解决“惩罚什么”“如何惩罚”和“如何防止过度惩罚”三个问题。

### 模块一：必要推理前缀检测器

该模块的目标是精确定位推理链中**首次产生正确答案的最短前缀**，即必要推理前缀（Necessary Reasoning Prefix, NRP）。NRP 的形式化定义为：

$$\mathrm{NRP} = \bigoplus_{i=1}^{c^*} s_i, \quad c^* = \min\{ c \in [1, |S|] : j_{s_c} = \text{yes} \}$$

其中 $s_i$ 为将完整推理过程按语义切分后的第 $i$ 个推理块，$j_{s_c}$ 是判断模型对第 $c$ 个推理块的二值判定结果。NRP 即从首个推理块到第一个被判定为“yes”的推理块为止的拼接。

实现上，DECS 微调一个轻量级判断模型 $\mathcal{M}_{\text{judge}}$（基于 Qwen2.5-1.5B），通过提示词输入问题 $q$、推理块 $s_c$ 和真实答案 $y^*$，生成“yes/no”判定：

$$j_{s_c} \sim \mathcal{M}_{\text{judge}}(\cdot \mid q, s_c, y^{*})$$

该检测器仅在数学推理数据上训练，但在科学（GPQA-Diamond）和编程（LiveCodeBench）任务上展示了超过 97% 的泛化精度（Table 6）。训练时间开销约为完整训练步的 3.4%~5.1%（Table 7）。

### 模块二：解耦的 Token 级奖励分配

该模块是 DECS 的核心创新，从根本上解决了序列级长度惩罚与 token 级策略优化之间的不对齐问题。其设计逻辑为：**NRP 内的必要 token 获得恒定高奖励，NRP 后的冗余思考 token 获得按长度缩放的低奖励**，从而在组内标准化后产生负优势，精准抑制冗余生成。

具体奖励函数为：

$$r_{i,j} = \begin{cases} r_{+} \cdot \mathbf{1}_{\mathbf{o}_i \text{ is correct}} & j \leq K_{\mathbf{o}_i}^* \lor o_j \notin o_{\text{think}} \lor o_{i,j}=\emptyset \\\\ (r_0 - \frac{(r_{+} - r_0) L_i}{L_{\max}}) \cdot \mathbf{1}_{\mathbf{o}_i \text{ is correct}} & j > K_{\mathbf{o}_i}^* \land o_j \in o_{\text{think}} \end{cases}$$

其中：
- $r_{+}$ 和 $r_0$ 分别为高奖励和基础奖励值（实验中设为 1.1 和 1.0）
- $K_{\mathbf{o}_i}^*$ 为第 $i$ 条响应的 NRP 边界位置
- $L_i$ 为当前响应长度，$L_{\max}$ 为最大长度
- $o_{\text{think}}$ 表示思考 token 集合

该设计的精妙之处在于：NRP 后的冗余 token 奖励随响应长度线性递减，长度越大惩罚越重，形成自适应的压缩压力。同时，非思考 token（如最终答案部分）和空 token 始终获得 $r_{+}$，确保答案质量不受影响。

基于 token 级奖励，优势估计也相应变为 token 级：

$$A_{i,j}^{\text{DECS}} = \frac{r_{i,j} - \text{mean}(r_{1,j}, \dots, r_{G,j})}{\text{std}(r_{1,j}, \dots, r_{G,j})}$$

这保证了同一位置上的 token 在组内进行公平比较，正确长序列中的高熵必要 token 不再被错误地分配负优势。

### 模块三：课程提示调度

该模块的理论基础来自 **Theorem 1**：当 batch 中所有 rollout 都正确的 prompt 比例 $\kappa$ 与响应长度标准差 $\sigma_L$ 的乘积超过阈值时，正确的高熵 token 将获得负的期望 logit 变化，即被抑制。课程调度的目标是通过动态控制 $\kappa$ 来维持 $\kappa \sigma_L < C$ 的条件。

具体更新规则为：

$$\kappa_m = \text{clip}( \kappa_{m-1} + \beta (\mathcal{R}_m - \mathcal{R}_{m-1}), 0, \kappa_m^0 )$$

其中：
- $\kappa_m$ 为第 $m$ 步 batch 中简单 prompt 的比例
- $\mathcal{R}_m$ 为当前 batch 中正确序列的 NRP 比例
- $\beta$ 为调节步长（网格搜索最优值为 0.2）
- $\kappa_m^0$ 为初始比例上界

当 NRP 比例上升（即模型开始压缩推理长度）时，调度器自动增加简单 prompt 占比，防止高熵探索 token 被过度惩罚；反之则减少简单 prompt 占比，维持压缩压力。消融实验（Table 3）证实，移除课程调度后性能明显下降（Avg Acc 从 47.78 降至 46.31），验证了该模块在效率-性能平衡中的关键作用。

## 实验与关键发现

### 核心发现：效率与性能的同步提升

DECS 在七个数学与科学推理基准上实现了超过 50% 的推理 token 压缩，同时 pass@1 准确率平均提升 +2.48 点（DS-1.5B）和 +0.8 点（DS-7B）。这一结果验证了核心假设：精确定位必要推理前缀（NRP）并对冗余 token 进行差异化惩罚，可以在不损害推理能力的前提下大幅降低计算开销。

具体而言，在 AIME2024 基准上，DS-1.5B 模型的推理 token 从 12,202 降至 5,550（-54.5%），pass@1 从 27.99 提升至 31.25（+3.26）；DS-7B 模型的 token 从 10,508 降至 5,277（-49.8%），pass@1 从 50.65 提升至 51.33（+0.68）。综合效率-性能指标 AES 在 DS-1.5B 上达到 0.74，DS-7B 上达到 0.54，均显著优于所有基线方法（Table 1）。

![[assets/figures/papers/paper_list_l4_https_openreview_net_forum_id_kdeiRledV6/figures/003_Table_1.jpg]]
*Table 1: Pass@1 (Acc) and the number of tokens (#Tok.) used across seven benchmarks. “LCB.” denotes LiveCodeBench-v6, “OlympiadB.” denotes the OlympiadBench, and “GPQA-D” denotes GPQA-Diamond. The best performing score is marked in bold and the second-best is underlined*

### 消融实验：两个关键组件的因果贡献

消融实验（Table 3, Fig. 3a）清晰揭示了课程调度（CS）与解耦奖励（DR）的独立作用：

![[assets/figures/papers/paper_list_l4_https_openreview_net_forum_id_kdeiRledV6/figures/008_Table_3.jpg]]
*Table 3: Ablation study with two major components of DECS on the DS-1.5B base model. “CS” denotes adaptive data sampling and “DR” denotes the decoupled reward mechanism*

- **移除课程调度（w/o CS）**：平均准确率从 47.78 降至 46.31，同时 token 消耗增加。这直接验证了 Theorem 1 的预测——当 batch 内所有 rollout 均正确的 prompt 比例过高时，正确的高熵 token 会获得负优势，导致探索行为被抑制。课程调度通过动态控制简单 prompt 的占比，维持了高熵 token 的正向学习信号。

- **移除解耦奖励（w/o DR）**：策略仍保留约 25% 的冗余 token（平均 token 数 5,111 vs 4,000），验证了 Theorem 2 中序列级奖励的根本缺陷——正确的长序列中 NRP 之后的冗余 token 无法被有效惩罚，因为序列级奖励将它们与必要的 NRP token 混为一谈。

- **超参数 β 的敏感性**：网格搜索（Table 9）表明 β=0.2 在效率-性能权衡中表现最优。β 过低则课程调整不足，效率增益有限；β 过高则简单 prompt 占比波动过大，导致性能下降。该最优值依赖于初始 NRP 比例，尚未实现完全自动化的自适应调节。

### 压缩质量分析：近乎无损的推理能力保留

在限制 token 预算下的 Pass@K 评估（Fig. 3c, Fig. 8c）表明，DECS 压缩后的策略在多个预算水平上与基础模型的 Pass@K 曲线几乎重合，实现了近乎无损的压缩。这意味着 DECS 并未牺牲模型在多次采样下的上限能力，仅移除了真正的冗余推理。

进一步的行为分析（Fig. 4b）显示，DECS 主要减少了三类冗余 token：
1. **反思/修正 token**（如“wait, let me check”）：显著下降，表明模型不再进行不必要的自我纠正；
2. **结论性 token**（如“therefore, the answer is”）：大幅减少，因为 NRP 之后的内容被有效截断；
3. **探索性 token**（如“alternatively, we could”）：频率几乎不变，验证了课程调度成功保护了高熵探索行为。

### 跨模型与跨算法泛化

DECS 在 Qwen3-4B 模型上复现了相似效果（Table 2）：平均推理 token 减少 54.80%，pass@1 提升 1.32 点，AES 达到 0.61。这证明 NRP 检测器和解耦奖励机制不依赖于特定基础模型的推理风格。

![[assets/figures/papers/paper_list_l4_https_openreview_net_forum_id_kdeiRledV6/figures/004_Table_2.jpg]]
*Table 2: Generalization to the Qwen3-4B model. DECS still achieves 0.61 AES score, with 54.80% reduction to overthinking and 1.32 pass@1 improvement*

此外，使用 REINFORCE++ 替代 GRPO 进行优势估计（Table 10），性能与 token 节省几乎无差异，验证了 DECS 对底层 RL 算法的鲁棒性。其核心创新在于奖励函数的设计，而非特定的策略优化器。

### 失败模式与局限性

1. **NRP 检测器的跨域泛化**：检测器仅在数学推理数据上训练。尽管在科学（GPQA-Diamond）和编程（LiveCodeBench）任务上展示了 >97% 的人工评估精度（Table 6），但在更广泛的非数学领域（如法律推理、医学诊断）可能需要重新适配或微调。

2. **训练开销**：解耦奖励需要额外的轻量级判断模型（Qwen2.5-1.5B）进行在线 NRP 检测，引入了约 3.4%~5.1% 的训练时间开销（Table 7）。在 4×NVIDIA A100 80GB GPU 的配置下，这一开销可接受但不可忽略。

3. **β 参数的手动调节**：课程调度中的 β 超参数需要针对不同基础模型进行网格搜索，最优值 0.2 依赖于初始 NRP 比例，尚未实现完全自动化的自适应调节。对于全新模型架构或训练数据分布，仍需人工介入。

![[assets/figures/papers/paper_list_l4_https_openreview_net_forum_id_kdeiRledV6/figures/001_Figure_1.jpg]]
*Figure 1: Left: Two major flaws of prior practice apply sequence-level length reward without control of training data. Negative advantage values penalize correct high entropy tokens from long sequences while positive ones reward redundant tokens from short sequences; Middle: Flaws of length rewards lead to inferior performance and suboptimal efficiency gains on AIME2024 dataset; Right: DECS improves pass@1 of base models while reducing ∼ 60% token costs compared to the base model across 7 benchmarks. Experimental details are presented in Appendix G.5*

![[assets/figures/papers/paper_list_l4_https_openreview_net_forum_id_kdeiRledV6/figures/016_Figure_7.jpg]]
*Figure 7: (a) AIME2024 reward and response length during evaluation for training DeepSeek-R1- Distill-7B base model with DECS; (b) Proportion of NRP (PNRP) and response length during training for training DeepSeek-R1-Distill-7B base model with DECS; (c) DECS improves pass@1 of base models while reducing ∼ 50% tokens compared to the 7B base model across 7 benchmarks*

![[assets/figures/papers/paper_list_l4_https_openreview_net_forum_id_kdeiRledV6/figures/019_Figure_8.jpg]]
*Figure 8: The Pass@1 score and average token counts on (a) AIME2025 and (b) AMC23 datasets under diverse token limits with the DeepSeek-R1-Dsitill-1.5B base policy; (c) Models applying DECS are on par with the base policy (DS-7B) in terms of Pass@K scores on three challenging benchmarks*

## 定位与知识库关联

### 问题根源：序列级奖励与 token 级优化的不对齐

过度思考（overthinking）问题的本质瓶颈在于**序列级别的长度惩罚与 token 级别的策略优化之间存在根本性的不对齐**。现有方法普遍采用形如

$$r'(\mathbf{o}_i) = \begin{cases} r(\mathbf{o}_i) - \gamma |\mathbf{o}_i| & \mathbf{o}_i \text{ is correct} \\ r(\mathbf{o}_i) & \text{otherwise} \end{cases}$$

的序列级复合奖励（Eq. 4），但 Lemma 2 严格证明了其致命缺陷：当某个 prompt 的所有 rollout 均为正确时，正确长序列中必要的高熵探索 token 会被错误地分配负优势，导致其生成概率下降；而短序列中的冗余 token 反而获得正优势。这造成模型在追求效率时抑制了有益的探索行为，破坏了效率与性能的平衡。

DECS 的核心洞察在于：**通过定位必要推理前缀（NRP），对 NRP 之前的必要 token 给予充分奖励，对 NRP 之后的冗余 token 进行精确惩罚，同时利用课程调度防止高熵 token 被过度抑制**。Theorem 1 进一步给出了高熵 token 免受负优势的条件 $\kappa \sigma_L < C$，其中 $\kappa$ 为全正确 rollout prompt 的比例，$\sigma_L$ 为响应长度标准差——这为课程调度提供了理论依据。

### 与现有效率方法的对比定位

当前推理效率优化方法可大致分为三类，DECS 在每一类中都展现了结构性的改进：

**第一类：基于长度惩罚的复合奖励方法。** **ThinkPrune**（Hou et al., 2025）和 **LC-R1**（Cheng et al., 2025）在序列级别将长度惩罚与正确性奖励结合，但正如 Lemma 2 所揭示，这种粗粒度的奖励设计无法区分必要推理与冗余推理。**TLMRE**（Arora & Zanette, 2025）引入了长度调节奖励，但仍未解决 token 级别的不对齐问题。实验表明（Fig. 3b），LC-R1 仍保留约 10% 的冗余 token，而 DECS 通过解耦奖励进一步压缩了非 NRP token，同时提升了 PNRP 分数。

**第二类：基于监督微调或选择性优化的方法。** **AdaptThink**（Zhang et al., 2025b）通过强制无思考回答来引导必要性思考，**MinD**（Zeng et al., 2025b）通过 SFT 引导策略在 NRP 后停止。这些方法依赖额外的监督信号，且缺乏对探索行为的保护机制。**S-GRPO**（Dai et al., 2025）选择性偏向高效轨迹，但同样面临探索抑制的风险。DECS 则通过课程调度机制（Eq. 11）动态调整简单 prompt 的比例，确保高熵 token 在整个训练过程中维持正向学习信号。

**第三类：基于难度自适应的压缩方法。** **LASER-D**（Liu et al., 2025）根据难度调整奖励，但未对 token 级别进行细粒度控制。DECS 的 NRP 检测器（基于 Qwen2.5-1.5B 微调的轻量级判断模型）将推理过程分块并精确定位首次包含正确答案的边界，为 token 级奖励分配提供了精确依据。

### DECS 的适用边界与局限

**已验证的适用场景：**
- **数学推理**：在 AIME2024、AIME2025、AMC23、MATH500、OlympiadBench 等七个基准上，DECS 将推理 token 减少超过 50%，同时 pass@1 平均提升 +2.48 点（DS-1.5B）和 +0.8 点（DS-7B）（Table 1）。
- **跨模型泛化**：在 Qwen3-4B 上实现 54.80% token 压缩和 1.32 pass@1 提升（Table 2），验证了方法的模型无关性。
- **跨领域泛化**：NRP 检测器在 GPQA-Diamond（科学）和 LiveCodeBench（编程）上展示了 >97% 的泛化精度（Table 6），表明其在非数学推理任务中也具有潜力。
- **RL 算法鲁棒性**：使用 REINFORCE++ 替代 GRPO 估计优势时，性能与 token 节省几乎无差异（Table 10），验证了 DECS 对底层 RL 算法的鲁棒性。

**已知局限：**
1. **NRP 检测器的领域依赖性**：检测器仅在数学推理数据上训练，尽管在科学和编程任务上展示了高泛化精度，但在更广泛的非推理类任务（如开放式对话、创意写作）上的适用性仍需验证。
2. **额外计算开销**：解耦奖励需要额外的轻量级判断模型进行在线 NRP 检测，引入了约 3.4%~5.1% 的训练时间开销（Table 7）。
3. **超参数敏感性**：课程调度中的 $\beta$ 超参数需要针对不同基础模型进行网格搜索，最优值 0.2 依赖于初始 NRP 比例（Table 9），尚未实现完全自动化的自适应调节。$\beta$ 过低则效率不足，过高则性能下降。

### 开放问题

1. **NRP 检测的内化**：能否将 NRP 检测能力直接集成到推理策略中（例如通过策略自身的置信度或熵信号），从而消除对额外 judge 模块的依赖？这将使方法更加简洁且减少计算开销。
2. **更细粒度的超参数优化**：对 $\beta$ 参数进行更细粒度的搜索（如 0.25）是否能进一步提升效率-性能的帕累托前沿？当前网格搜索的步长可能遗漏更优配置。
3. **非推理类任务的扩展**：DECS 在开放式对话、创意写作等非推理类任务上的适用性和表现如何？这些场景中“必要推理前缀”的定义可能需要重新设计。
4. **多任务混合训练的课程调度**：能否将课程调度机制扩展到多任务混合训练场景，实现更鲁棒的数据分布自适应？当前调度策略仅针对单一数据分布设计。
5. **与推理预算控制的结合**：DECS 在限制 token 预算下 Pass@K 性能与基础模型重合（Fig. 3c），实现了几乎无损的压缩。如何将这种能力与显式的推理预算控制机制（如 token 限制、早停策略）深度结合，值得进一步探索。

## 原文 PDF

![[paperPDFs/ICLR_2026/Overthinking_Reduction_with_Decoupled_Rewards_and_Curriculum_Data_Scheduling.pdf]]
