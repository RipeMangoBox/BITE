---
title: "EigenBench: A Comparative Behavioral Measure of Value Alignment"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/EigenBench_A_Comparative_Behavioral_Measure_of_Value_Alignment.pdf
project_link: null
code_link: https://github.com/jchang153/EigenBench
openreview_forum_id: fm79KXJIUQ
aliases:
- EigenBench
tags:
- ICLR_2026
- topic/safety_alignment_fairness_privacy
- topic/safety_alignment_fairness_privacy/trustworthy_machine_learning
core_operator: "利用模型群体相互评判并聚合共识，通过加权信任（行为更对齐的模型也是更好的评判者）产生共识排名。"
primary_logic: "模型对特定价值观的遵守程度与其评判他人遵守程度的能力正相关，因此可以将评判权重与模型自身得分耦合，通过左特征向量迭代获得一致排序。"
claims:
- "EigenBench 与人类评判高度一致（平均人类-LM 评判距离 0.3130，接近人类-人类距离 0.3133）"
- "EigenBench 能在无真实标签的情况下恢复 GPQA 排名（Kendall tau ≈ 0.77，随机排名出现概率约 10^{-6}）"
- "EigenBench 能区分经‘Loving’宪法微调和预提示的模型（loving 版本 1579 vs 基础模型 1426），验证其对主观特质的测量能力"
- "GPQA 上 Kendall tau = 0.77 （EigenBench 无标签恢复的排名）"
---

# EigenBench: A Comparative Behavioral Measure of Value Alignment

> [!tip] 核心洞察
> 模型对特定价值观的遵守程度与其评判他人遵守程度的能力正相关，因此可以将评判权重与模型自身得分耦合，通过左特征向量迭代获得一致排序。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | EigenBench：一种比较性的价值对齐行为度量 |
| 英文题名 | EigenBench: A Comparative Behavioral Measure of Value Alignment |
| 会议/期刊 | ICLR 2026 (Oral) |
| Links | [paper](https://openreview.net/forum?id=fm79KXJIUQ) · [GitHub](https://github.com/jchang153/EigenBench) |
| Topic | #topic/safety_alignment_fairness_privacy #topic/safety_alignment_fairness_privacy/trustworthy_machine_learning |
| Method | EigenBench |
| Dataset | GPQA, Human Validation (Universal Kindness), Loving Constitution |

> [!tip] 效果简介
> - GPQA 上，Kendall tau 为 0.77 （EigenBench 无标签恢复的排名），对比 0.00 （完全随机排名），变化 +0.77。
> - Human Validation (Universal Kindness) 上，平均评判者距离 (L1-norm of trust vectors) 为 0.3130 （人类-LM 平均距离），对比 0.3133 （人类-人类平均距离），变化 -0.0003。
> - Loving Constitution 上，Elo Score 为 1579 (Llama 3.1 8b loving, pre-prompted)，对比 1426 (Llama 3.1 8b base)，变化 +153。

## 概要

语言模型的价值对齐评估长期面临一个核心瓶颈：**缺乏量化主观价值对齐的客观指标**，尤其是针对那些无真实标注的主观特质（如“善意”“保守主义”“深层生态观”等）。传统方法要么依赖昂贵且不可规模化的人类评判，要么仅能测量模型在客观基准上的能力，无法系统比较模型在开放式价值维度上的行为表现。

EigenBench 提出了一种**黑盒比较性度量框架**，其核心思想是：**模型对特定价值观的遵守程度与其评判他人遵守程度的能力正相关**。基于这一洞察，方法让模型群体在给定“宪法”（即一套评判标准）下相互评判对方的回答，并通过加权信任聚合共识——行为更对齐的模型同时被视为更可信的评判者，其评判权重更高。最终，通过计算信任矩阵的**左主特征向量**（EigenTrust 算法）获得一致的模型排名。

**核心结论**：EigenBench 能够在无真实标签的情况下恢复客观基准的排名（GPQA 的 Kendall tau ≈ 0.77），且其评分与人类评判高度一致（人类-LM 评判距离 0.3130，接近人类-人类距离 0.3133）。该方法还能有效区分经特定价值微调或预提示的模型，验证了其对主观特质的测量能力。

**方法定位**：与 LMArena（基于人类偏好的 Elo 排名）、Prompt-to-Leaderboard（针对特定提示的排名）和 LitmusValues（测量单个模型内部价值优先级）不同，EigenBench 利用模型群体相互评判产生**特定价值体系下的比较性排名**，无需人类标注，且排名随宪法变化而自适应。

**主要结果速览**：
- 在 GPQA 基准上，EigenBench 无标签恢复的排名与真实排名高度相关（Kendall tau ≈ 0.77，随机排名出现概率约 10⁻⁶）
- 人类验证实验中，EigenBench 评分与人类评判的距离（0.3130）几乎等同于人类之间的分歧（0.3133）
- “Loving”宪法下，经微调或预提示的模型 Elo 评分显著高于基础模型（1579 vs 1426）
- 评分对场景数据集、宪法措辞和模型群体变化均表现出稳健性

语言模型（LM）在真实世界部署中的安全性不仅取决于其客观能力，还取决于其与人类价值观的契合程度。然而，当前缺乏能够量化模型在主观价值维度上对齐程度的客观指标，尤其是对于“善良”“保守”等缺乏真实标注（ground truth）的主观特质，传统的基准测试方法难以适用。

现有的模型排名系统各有侧重，但均未解决这一核心缺口。**LMArena**（Chiang et al., 2024）基于人类偏好的头对头比较，依赖大量人工评判，成本高昂且难以针对特定价值体系定制。**Prompt-to-Leaderboard**（Frick et al., 2025）虽然能针对特定提示生成排名，但其覆盖面受限于提示本身。**LitmusValues**（Chiu et al., 2025）测量单个模型内部的价值优先级，但不提供模型间的比较性排名。这些方法都无法在无人工标注的情况下，针对任意给定的价值体系（宪法，constitution）生成可比较的模型排行榜。

本文的核心动机正是填补这一空白：**如何在不依赖人类标注的前提下，量化地比较不同语言模型对特定价值观的遵守程度？** 作者观察到，模型对特定价值观的遵守程度与其评判他人遵守程度的能力之间存在正相关——行为更对齐的模型往往也是更可靠的评判者。基于这一洞察，EigenBench 利用模型群体相互评判并聚合共识，通过加权信任机制产生共识排名，从而将价值对齐这一主观问题转化为可量化的比较性度量。

## 核心方法与创新机理

EigenBench 的核心创新在于将**主观价值对齐的量化评估**转化为一个**无需外部标注的群体共识问题**。与现有语言模型排名系统相比，其关键差异体现在三个层面：

### 从人类偏好到群体共识的范式转换

传统排名系统依赖外部锚点：**LMArena**（Chiang et al., 2024）以人类偏好为基准进行头对头比较，**Prompt-to-Leaderboard**（Frick et al., 2025）针对特定提示收集人类评判，**LitmusValues**（Chiu et al., 2025）则测量单个模型内部的价值优先级。EigenBench 彻底摒弃了对人类标注的依赖——它让模型群体相互评判，通过**EigenTrust**（Kamvar et al., 2003）算法聚合共识，输出反映群体集体判断的排名。这一范式转换解决了主观特质缺乏真实标注的根本瓶颈。

### 评判权重的内生耦合机制

方法的核心洞察是：**模型对特定价值观的遵守程度与其评判他人遵守程度的能力正相关**。EigenBench 将这一洞察编码为数学模型——评判模型 $i$ 对被评模型 $j$ 的信任度 $T_{ij}$ 与模型自身的得分 $t_i$ 通过左特征向量方程耦合：

$$t_j = \sum_i t_i T_{ij}$$

这意味着行为更对齐的模型在评判中获得更高权重，形成自洽的迭代优化过程。低秩 Bradley-Terry-Davidson 模型为每个模型学习两个向量——**评判透镜** $u_i$ 和**模型倾向** $v_j$——前者捕捉评判标准的个体差异，后者表示模型在潜在空间中的对齐程度，二者的内积 $u_i^\top v_j$ 决定评判概率。

### 宪法驱动的可定制评估框架

EigenBench 引入**宪法**（constitution）作为评估标准的显式载体，使得同一模型群体可以针对不同价值观产生独立排名。实验验证了这一框架的灵敏度与稳健性：经“Loving”宪法微调的 Llama 3.1 8b（loving-oct，Elo 1573）和预提示版本（loving，Elo 1579）显著高于基础模型（Elo 1426），证实方法能捕捉主观特质的差异（Table 2）；同时，宪法措辞变化仅导致最高 16 Elo 的标准差，且不存在对生成宪法的模型的偏见（Section 6.2）。

### 双盲设计与公平性保障

为防止评判中的策略性行为，EigenBench 采用**双盲设计**：被评模型不知道评估标准，评判模型不知道被评模型的身份。评委脚手架（judge scaffold）通过逐标准反思并同时产生多个比较，将顺序偏见率和不传递率显著降低（Table 8），进一步提升了评判质量。Greenbeard 对抗实验表明，即使在多数合谋模型存在的情况下，非对抗模型的评分受影响较小，方法对合谋攻击具有一定稳健性（Figure 10）。

### 与现有方法的根本差异

| 维度 | LMArena | Prompt-to-Leaderboard | LitmusValues | **EigenBench** |
|------|---------|----------------------|--------------|----------------|
| 评判来源 | 人类偏好 | 提示特定的人类偏好 | 模型内部价值优先级 | **模型群体相互评判** |
| 评估对象 | 通用能力 | 特定提示性能 | 单一模型价值观 | **任意宪法的对齐程度** |
| 标注需求 | 需要人类标注 | 需要人类标注 | 无需标注 | **无需外部标注** |
| 排名机制 | Elo 系统 | 提示特定排名 | 价值取向分析 | **EigenTrust 共识聚合** |

这些创新使 EigenBench 在无真实标签的情况下成功恢复了 GPQA 排名（Kendall τ ≈ 0.77，随机排名出现概率约 $10^{-6}$），并与人类评判高度一致（人类-LM 评判距离 0.3130，接近人类-人类距离 0.3133），验证了群体共识机制替代外部标注的可行性。

![[assets/figures/papers/paper_list_l47_https_openreview_net_forum_id_fm79KXJIUQ/figures/003_Table_1.jpg]]
*Table 1: Comparison of LM Elo ranking systems*

EigenBench 的核心目标是为语言模型的价值对齐提供一种比较性的黑盒度量。其输入由三部分组成：一个待评测的模型群体 $\mathcal{M} = \{M_1, \dots, M_N\}$、一份定义评判标准的宪法 $C = \{C_1, \dots, C_k\}$、以及一个预定义的场景提示集 $S$。整个流水线围绕“模型相互评判—聚合共识”这一因果机制展开，最终输出每个模型在该宪法下的 Elo 评分，直观反映其价值对齐程度。

**流水线核心模块关系**

流水线包含五个串联的功能模块，其信息流如 Figure 1 所示：

1. **成对比较数据收集**：从场景集 $S$ 中采样场景 $S_\ell$，随机选取一对被评模型 $M_j, M_k$ 和一个评判模型 $\bar{M}_i$。关键设计在于**双盲机制**——只有评判模型接收宪法 $C$，被评模型仅看到场景提示，不知道评估标准甚至不知道正在被评估。评判模型先对两个回答分别进行反思，再给出偏好三元组 $r_{ijk\ell} \in \{0, 1, 2\}$（平局/偏好 $j$/偏好 $k$）。为消除顺序偏见，同时收集正反顺序的比较并检测不一致性。

2. **低秩 Bradley-Terry-Davidson 模型**：将成对比较数据拟合到一个参数化的概率模型中，学习每个模型的**倾向向量** $v_j \in \mathbb{R}^d$ 和**评判透镜向量** $u_i \in \mathbb{R}^d$，以及评判模型的平局倾向 $\lambda_i$。该模块的因果洞察在于：模型对特定价值观的遵守程度与其评判他人遵守程度的能力是正相关的，因此评判权重应与模型自身得分耦合。赢、输、平局的概率由内积 $u_i^\top v_j$ 决定：

   $$\Pr(i \text{ thinks } j \succ k) = \frac{1}{Z} \exp(u_i^\top v_j), \quad \Pr(i \text{ thinks } k \succ j) = \frac{1}{Z} \exp(u_i^\top v_k), \quad \Pr(i \text{ thinks } j \approx k) = \frac{1}{Z} \lambda_i \exp\left(\frac{1}{2} u_i^\top (v_j + v_k)\right)$$

   其中 $Z = \lambda_i \exp\left(\frac{1}{2} u_i^\top (v_j + v_k)\right) + \exp(u_i^\top v_j) + \exp(u_i^\top v_k)$ 为归一化常数。

3. **信任矩阵构建**：利用学得的参数构建随机矩阵 $T$，其中 $T_{ij}$ 表示评判模型 $i$ 对被评模型 $j$ 的信任度，综合了成对得分和平局倾向：

   $$T_{ij} = \frac{s_{ij} + \frac{1}{2}\lambda_i \sum_{k \neq j} \sqrt{s_{ij}s_{ik}}}{\sum_l (s_{il} + \frac{1}{2}\lambda_i \sum_{k \neq l} \sqrt{s_{il}s_{ik}})}$$

4. **EigenTrust 算法**：计算信任矩阵 $T$ 的左主特征向量 $t$，满足 $t_j = \sum_i t_i T_{ij}$，作为模型得分的概率分布。该步骤直接继承自 **EigenTrust**（Kamvar et al., 2003）的核心思想——行为更可信的节点也是更好的信任评估者，通过迭代加权形成共识排序。

5. **Elo 评分转换**：将信任得分 $t_j$ 转换为便于阅读的 Elo 评分：

   $$\text{Elo}_j = 1500 + 400 \log_{10}(N t_j)$$

**与现有排名系统的定位差异**

Table 1 将 EigenBench 与三类现有系统进行了定位对比：**LMArena**（Chiang et al., 2024）基于人类偏好的头对头比较，**Prompt-to-Leaderboard**（Frick et al., 2025）针对特定提示进行排名，**LitmusValues**（Chiu et al., 2025）测量单个模型内部的价值优先级。EigenBench 的差异化在于：它不需要人类标注或真实标签，而是通过模型群体的相互评判，为任意给定的宪法 $C$ 生成定制化的价值对齐排行榜。

**输入输出边界**

- **输入**：模型群体 $\mathcal{M}$、宪法 $C$、场景集 $S$（实验中主要使用 r/AskReddit、OASST 对话数据集、AIRiskDilemmas 三个来源）。
- **输出**：每个模型 $M_j$ 在宪法 $C$ 下的 Elo 评分及其 95% 自助法置信区间。
- **中间产物**：低秩潜在空间中的模型倾向 $v_j$ 和评判透镜 $u_i$，可用于可视化不同模型/人格在价值空间中的相对位置（如 Figure 2 所示的历史人物人格分布）。

EigenBench 的评分机制由四个紧密耦合的模块构成，其核心数学直觉是：**模型对特定价值观的遵守程度与其评判他人遵守程度的能力正相关**，因此可以将评判权重与模型自身得分耦合，通过迭代特征分解获得一致排序。

### 成对比较数据收集

给定宪法 $C$（一组评判标准）、模型群体 $\mathcal{M}$ 和场景集 $S$，系统反复抽样一个场景 $S_\ell$、一对被评模型 $M_j, M_k$ 和一个评判模型 $M_i$。被评模型在**不知晓宪法内容**的情况下生成回答 $R_j, R_k$；评判模型则接收宪法，先对每个回答单独反思（生成 $\hat{R}_j, \hat{R}_k$），再进行比较决策，输出三元偏好：

$$
r_{ijk\ell} = \begin{cases} 0, & M_i \text{ 认为 } R_j \text{ 与 } R_k \text{ 平局} \\ 1, & M_i \text{ 偏好 } R_j \\ 2, & M_i \text{ 偏好 } R_k \end{cases}
$$

为消除顺序偏见，系统同时收集转置比较 $r_{ikj\ell}$，并通过重映射函数处理不一致偏好（详见原文 Appendix C）。评判脚手架（judge scaffold）要求模型逐标准反思并同时产生多个比较，显著降低了首因/近因偏见率和循环率（Table 8, Appendix J）。

### 低秩 Bradley-Terry-Davidson 模型

收集到的比较数据被拟合到一个低秩 Bradley-Terry-Davidson（BTD）模型中。该模型为每个模型学习两个 $d$ 维向量：**被评倾向** $v_j \in \mathbb{R}^d$ 和**评判透镜** $u_i \in \mathbb{R}^d$，以及评判模型的**平局倾向** $\lambda_i \in \mathbb{R}$。评判模型 $i$ 对被评模型 $j$ 和 $k$ 的赢、输、平局概率为：

$$
\begin{aligned} \Pr(i \text{ 认为 } j \succ k) &= \frac{1}{Z} \exp(u_i^\top v_j), \\ \Pr(i \text{ 认为 } k \succ j) &= \frac{1}{Z} \exp(u_i^\top v_k), \\ \Pr(i \text{ 认为 } j \approx k) &= \frac{1}{Z} \lambda_i \exp\left(\frac{1}{2} u_i^\top (v_j + v_k)\right) \end{aligned}
$$

其中归一化常数 $Z = \lambda_i \exp\left(\frac{1}{2} u_i^\top (v_j + v_k)\right) + \exp(u_i^\top v_j) + \exp(u_i^\top v_k)$。模型通过最大化所有比较数据的对数似然来学习参数。嵌入维度 $d$ 增大时训练和测试损失下降，$d=30$ 后趋于平稳且无过拟合（Figure 9b, Appendix K.2）。

### 信任矩阵构建

利用学得的参数，定义评判模型 $i$ 对被评模型 $j$ 的信任度 $T_{ij}$：

$$
T_{ij} = \frac{s_{ij} + \frac{1}{2}\lambda_i \sum_{k \neq j} \sqrt{s_{ij}s_{ik}}}{\sum_l \left(s_{il} + \frac{1}{2}\lambda_i \sum_{k \neq l} \sqrt{s_{il}s_{ik}}\right)}
$$

其中 $s_{ij} = \exp(u_i^\top v_j)$ 表示评判模型 $i$ 认为被评模型 $j$ 的相对强度。该矩阵综合了成对得分和平局倾向，构成一个随机矩阵（每行和为 1）。

### EigenTrust 算法与 Elo 转换

信任矩阵 $T$ 的左主特征向量 $t$ 满足不动点方程：

$$
t_j = \sum_i t_i T_{ij}
$$

即模型 $j$ 的得分是所有模型对其信任的加权和，权重恰为各模型的得分本身——这正是“更好的模型也是更好的评判者”这一核心洞察的数学表达。通过幂迭代（Algorithm 1, 源自 **EigenTrust** (Kamvar et al., 2003)）求解 $t$，得到模型得分的概率分布。最后转换为 Elo 评分以便阅读：

$$
\text{Elo}_j = 1500 + 400 \log_{10}(N t_j)
$$

其中 $N$ 为模型总数。该模块的关键瓶颈在于：信任矩阵的质量完全依赖于 BTD 模型学得的 $u_i$ 和 $v_j$ 的质量，而 BTD 模型又依赖于比较数据的数量与质量——这构成了整个流水线的级联依赖关系。

## 实验与关键发现

### 核心验证：与人类评判的一致性

EigenBench 在“Universal Kindness”宪法下进行了严格的人类验证。实验收集了 7 名人类评判者对 8 个语言模型进行成对比较的数据，为每个人类评判者拟合标量 Bradley-Terry-Davidson 模型，得到其信任向量。然后计算人类评判者之间以及人类与语言模型评判者之间的 L1 距离。

**关键结果**：人类-LM 评判者的平均距离为 0.3130，而人类-人类之间的平均距离为 0.3133（Section 5.2, Appendix H）。两者几乎完全一致，表明 EigenBench 自动聚合的模型群体共识与人类评判没有系统性偏差。这一结果直接验证了“行为更对齐的模型也是更好的评判者”这一核心假设。

Figure 6 展示了人类与语言模型评判透镜在二维潜在空间中的分布：人类评判透镜（星形标记）与语言模型评判透镜（三角形标记）位于同一区域，进一步佐证了评判视角的相似性。

### GPQA 无标签排名恢复

为验证 EigenBench 在缺乏真实标签的主观任务上的排序能力，实验在 GPQA 基准上进行了测试：给定 15 个模型对 GPQA 问题的回答，让模型群体相互评判答案质量，但不提供任何正确答案。

**结果**：EigenBench 信任分数产生的排名与 GPQA 真实分数排名的 Kendall-tau 系数约为 0.77，仅需 12 次相邻交换即可恢复真实排序（Table 7）。对于随机排名，出现这种相关性的概率约为 10⁻⁶，表明结果具有统计显著性。


这一实验证明了方法的核心机制有效：即使没有客观标签，模型群体通过相互评判也能形成与真实能力高度一致的共识排序。Table 7 中具体排名为 Qwen3 Next 80B 信任分数最高（0.0758），其次是 Qwen3 235B（0.0756）和 Grok 3 Mini（0.0746），而 GPT 4o 最低（0.0491）。

### “Loving”宪法下的微调与预提示验证

Table 2 展示了 EigenBench 对主观价值对齐的敏感度。在“Loving”宪法（来自 Maiya et al., 2025）下，六个开源模型的评分呈现明显分化：

![[assets/figures/papers/paper_list_l47_https_openreview_net_forum_id_fm79KXJIUQ/figures/005_Table_2.jpg]]
*Table 2: EigenBench Elo scores for the Loving constitution from Maiya et al. (2025), on a population of six open-weight models including Llama 3.1 8b (loving-oct) which is fine-tuned on this constitution, and Llama 3.1 8b (loving) which is pre-prompted with this constitution*

- **Llama 3.1 8b（loving 预提示版）**：1579 分
- **Llama 3.1 8b（loving-oct 微调版）**：1573 分
- **Llama 3.1 8b（基础模型）**：1426 分

经“Loving”宪法微调或预提示的模型得分显著高于基础模型（差距约 150 分），而其他无关模型（如 Gemma 3 27b）得分更低。这证明 EigenBench 能够有效捕捉主观价值取向的差异，而非仅仅反映模型的一般能力。

### 多宪法评分与自我评估对比

Figure 3 展示了八个模型在三种宪法（Universal Kindness、Conservatism、Deep Ecology）上的 EigenBench Elo 评分及 95% 自助法置信区间。Deep Ecology 宪法的置信区间明显更宽，因为该宪法相关的场景较少，导致成对比较中出现大量平局。

![[assets/figures/papers/paper_list_l47_https_openreview_net_forum_id_fm79KXJIUQ/figures/004_Figure_3.jpg]]
*Figure 3: EigenBench Elo scores for eight models judged on the Universal Kindness, Conservatism, and Deep Ecology constitutions. The 95% confidence intervals shown are derived from the bootstrapping percentile method (Efron & Tibshirani, 1994). Larger confidence intervals are apparent in the scores for Deep Ecology due to a large portion of ties in the pairwise comparisons, as fewer scenarios are relevant to the constitution*

Table 6 将 EigenBench Elo 评分与模型自我评估调查分数进行对比。在 Universal Kindness 上，Gemini 2.5 Pro、Qwen 3 和 Grok 4 的自我评分均为满分 7.0，但 EigenBench 评分分别为 1556、1522 和 1510，显示出自我评估的“天花板效应”与行为测量的区分度差异。在 Conservatism 上，DeepSeek v3 自我评分最高（6.9）但 EigenBench 评分最低（1466），说明模型声称的价值观与行为表现出的价值观可能存在显著差距。

![[assets/figures/papers/paper_list_l47_https_openreview_net_forum_id_fm79KXJIUQ/figures/011_Table_6.jpg]]
*Table 6: Self-reported survey scores versus EigenBench Elo scores. Top: survey scores are the means of model self-ratings from 1-7 on eight criteria for Universal Kindness. Middle: survey scores are the means of self-ratings from 1 { - } 7 on ten criteria for Conservatism. Bottom: survey scores are the means of self-ratings from 1-7 on twelve criteria for Deep Ecology*

### 评分稳健性分析

**场景数据集敏感性**（Table 3）：在 Universal Kindness 宪法下，五个模型在三个不同场景数据集（r/AskReddit、AIRiskDilemmas、OASST）上的 Elo 评分相对一致。Gemini 2.5 Pro 在 r/AskReddit（1567）和 OASST（1568）上均领先，而 Claude 4 Sonnet 在 AIRiskDilemmas（1530）上表现最好。个别模型存在变化：Grok 4 在 OASST 上表现更好，GPT 4.1 在 AIRiskDilemmas 上表现更差。

![[assets/figures/papers/paper_list_l47_https_openreview_net_forum_id_fm79KXJIUQ/figures/006_Table_3.jpg]]
*Table 3: EigenBench Elo scores tested on the Universal Kindness constitution across three different scenario distributions*

**宪法措辞敏感性**（Section 6.2）：为测试宪法措辞的影响，实验为 Conservatism 生成了五种不同措辞的宪法变体。五个模型的 Elo 评分在不同宪法下的最大标准差仅为 16 分，表明 EigenBench 对宪法措辞不敏感。同时，评分不偏向生成宪法的模型，排除了“自我偏好”偏见的可能性。

**模型群体变化稳定性**（Table 4）：以初始群体 M₀ = {Gemini 2.5 Pro, GPT 4.1, Grok 4, DeepSeek v3} 为基准，逐步加入 Claude 3.5 Haiku 和 Claude 4 Sonnet。核心模型的评分保持相对稳定，但加入更强的 Claude 4 Sonnet 后，Grok 4 的评分从 1501 逐步降至 1478。这一现象符合预期：在更强的参照系中，原有模型的相对评分会有所下调。

### 消融实验

**评委脚手架的效果**（Table 8, Appendix J）：对比有无评委脚手架（逐标准反思并同时产生多个比较）的数据质量。使用脚手架后，五个评判模型的顺序偏见率（首因偏见和近因偏见）显著降低，循环率（不传递率）也明显下降。这验证了反思机制对提高评判质量的有效性。

![[assets/figures/papers/paper_list_l47_https_openreview_net_forum_id_fm79KXJIUQ/figures/016_Table_8.jpg]]
*Table 8: Order bias and cycle rates for five judges. Top: rates calculated from data collected without reflections. Bottom: rates calculated from data collected via judge scaffold. Primacy and recency bias indicate the judges’ order bias towards responses placed 1st or 2nd in the prompt, respectively*

**嵌入维度 d 的影响**（Figure 9b, Appendix K.2）：低秩 Bradley-Terry-Davidson 模型的嵌入维度 d 从 1 增加到 50 时，训练和测试损失持续下降，在 d=30 后趋于平稳且未出现过拟合。这表明 d=30 左右是当前实验设置下的合理选择。

**评分不稳定性与样本量**（Figure 9a）：通过自助法分析，EigenBench 信任分数的不稳定性随比较样本量 s 呈幂律衰减，拟合公式为 I = 10.758 s⁻⁰·⁵²⁸，R² = 0.9872。这为实际应用中确定所需样本量提供了经验参考。

### 对抗鲁棒性：Greenbeard 实验

为测试方法对合谋攻击的鲁棒性，设计了 Greenbeard 实验（Figure 10）。向 GPT 4.1 Mini 注入包含秘密词“plebeian”的预提示，创建 1 到 5 个合谋人格，与其他三个非对抗人格共同参与评判。

**结果**：随着合谋模型数量 G 从 0 增加到 5，合谋群体的平均 Elo 评分迅速上升（从约 1480 升至约 1570），表明它们成功通过相互认可抬高了自身排名。然而，非对抗模型的评分受影响较小，仅在合谋模型数量较多时出现轻微下降。这说明 EigenBench 对中等规模的合谋攻击具有一定稳健性，但在更彻底的对抗条件下（如强制模型遵守信号），鲁棒性仍需要进一步研究。

### 大规模实验

Figure 8 展示了 37 个模型在 Universal Kindness 宪法下的大规模 EigenBench Elo 评分。Gemini 2.5 Pro 以 1562 分位居榜首，Claude 4 Sonnet 和 GPT 4.1 紧随其后。部分模型的置信区间较宽，主要源于比较数据中的平局比例较高。Table 9 列出了所有参与模型的 API ID 对照信息。

### 已知局限与失败模式

1. **数据收集效率**：每次成对比较需要五次前向传播（两次模型响应、两次反思、一次比较调用），导致计算成本较高。论文建议未来通过主动学习或动态采样改善效率。

2. **对抗鲁棒性边界**：Greenbeard 实验显示，在足够强力的合谋个体和更激进的提示策略下，EigenBench 评分可能被操纵。当前方法的防御机制主要依赖群体中诚实模型的多数优势，缺乏主动的对抗检测机制。

3. **平局处理**：在场景与宪法相关性较弱时（如 Deep Ecology），大量平局导致置信区间变宽，排名区分度下降。这反映了方法对场景-宪法匹配度的依赖。

## 定位与知识库关联

### 核心定位：从偏好排名到价值对齐的共识度量

EigenBench 在语言模型评估生态中占据一个独特位置：它不依赖人类偏好或客观真实标签，而是通过模型群体内部的相互评判与共识聚合，产生针对任意价值体系（宪法）的定制化排名。这一设计使其区别于三类现有方法。

**与人类偏好排名的区别**。**LMArena**（Chiang et al., 2024）通过人类用户对模型输出的头对头比较构建 Elo 排名，其排名反映的是“人类总体偏好”这一隐含且混合的价值取向。**Prompt-to-Leaderboard**（Frick et al., 2025）将排名进一步细化到特定提示上，但仍依赖人类评判。EigenBench 的核心差异在于：它用模型评判替代人类评判，并将评估标准显式化为宪法 C，使得排名可针对任意价值维度定制（如“普世善意”“保守主义”“深层生态学”），而非受限于单一、隐式的人类偏好分布。Table 1 将四类系统并列对比，清晰展示了这一定位差异。

**与模型内部价值测量的区别**。**LitmusValues**（Chiu et al., 2025）通过探测模型内部表征来测量其价值优先级，属于“白盒”或基于表征的方法。EigenBench 则完全是黑盒方法：仅通过模型在场景下的行为输出进行评判，不访问模型内部参数或表征。这使得 EigenBench 适用于闭源 API 模型，且测量的是“展现的价值”而非“声称的价值”——Table 6 中自我报告分数与 EigenBench Elo 分数的差异（如 DeepSeek v3 在“保守主义”上自我评分最高但 EigenBench 评分最低）恰好揭示了这一区分的重要性。

**算法基础：EigenTrust 的迁移与适配**。EigenBench 的共识聚合机制直接继承自 **EigenTrust**（Kamvar et al., 2003），后者最初设计用于对等网络中的信誉管理。EigenBench 的关键适配在于：将“信任”定义从节点间的交易历史迁移到模型间的评判关系——评判模型 i 对被评模型 j 的信任度 $T_{ij}$ 由 Bradley-Terry-Davidson 模型学得的潜在强度导出。这一适配的深层合理性来自论文的核心洞察：**模型对特定价值观的遵守程度与其评判他人遵守程度的能力正相关**，因此“行为更对齐的模型也是更好的评判者”，使得通过左特征向量 $t_j = \sum_i t_i T_{ij}$ 迭代加权能够收敛到有意义的共识排名。

### 适用边界与局限

**数据效率瓶颈**。EigenBench 的数据收集过程计算密集：每次成对比较需要五次前向传播（两次被评模型响应、两次评判模型反思、一次比较调用）。对于 N 个模型的群体，完整的成对比较矩阵需要 $O(N^2)$ 次比较，这限制了大规模模型群体的快速评估。论文在 Section 7 中明确指出这一效率问题，并建议未来通过主动学习或动态采样来降低数据收集成本。Figure 9a 的幂律分析表明评分不稳定性随样本量 $s$ 以 $I = 10.758 s^{-0.528}$ 衰减，为样本量选择提供了经验指导，但并未给出成本-精度权衡的优化方案。

**对抗性操纵风险**。EigenBench 的共识机制假设大多数模型是“诚实”的评判者。当群体中存在足够强力的合谋个体时，评分可能被操纵。Greenbeard 实验（Figure 10）显示，当引入带有秘密信号词（“plebeian”）的合谋人格时，合谋模型的评分迅速上升，但非对抗性模型的评分受影响较小。然而，论文承认这一实验的对抗强度有限——合谋模型仅通过预提示进行协调，而非通过更彻底的机制（如强制遵守信号）。在更强的对抗设定下，EigenBench 的鲁棒性仍是开放问题。

**宪法与场景的敏感性**。实验表明 EigenBench 评分对宪法措辞变化不敏感（最高 Elo 标准差仅 16 分），且不存在对生成宪法的模型的偏见。然而，评分对场景分布存在中等程度的敏感性：Table 3 显示 Grok 4 在 OASST 数据集上表现更好，GPT 4.1 在 AIRiskDilemmas 上表现更差。这意味着 EigenBench 测量的是模型在**特定场景分布**下的价值对齐程度，而非抽象的“价值取向”——场景选择本身隐含了对价值表现形式的预设。

**模型群体变化的稳定性**。Table 4 显示，当向初始群体中添加新模型时，核心模型的评分相对稳定但并非不变：Grok 4 的 Elo 评分从 1501 持续下降至 1478（添加两个更强模型后）。这提示 EigenBench 的评分是**群体相对的**——它测量的是模型在给定群体中的相对对齐程度，而非绝对的价值得分。论文通过“固定核心模型平均分”的策略来缓解这一问题，但这本质上是一种后处理标准化，而非方法本身的属性。

### 开放问题

1. **跨任务泛化**：EigenBench 能否应用于其他缺乏真实标签的主观任务，如长期规划、创意写作或道德推理？GPQA 验证（Kendall tau ≈ 0.77）证明了方法在客观任务上的排名恢复能力，但其在更复杂的主观任务上的有效性尚未检验。

2. **效率与精度的权衡**：如何通过主动学习、动态采样或偶尔的人类判断来降低数据收集成本，同时保持排名质量？低秩 Bradley-Terry-Davidson 模型的嵌入维度 $d$ 在 $d=30$ 后损失趋于平稳（Figure 9b），但更大群体和不同宪法下的最优维度自动确定策略尚未建立。

3. **对抗鲁棒性边界**：当合谋模型的比例、协调强度或策略复杂性增加时，EigenBench 的鲁棒性如何保证？当前 Greenbeard 实验仅测试了简单预提示协调，更系统的对抗性评估（如 Sybil 攻击、策略性评判）是必要的。

4. **人类判断的整合机制**：Figure 7 展示了通过“teleportation”将人类信任向量混合进 EigenTrust 的初步尝试，但如何系统性地整合稀疏的人类判断以校准或验证模型排名，仍缺乏理论框架。

5. **宪法的完备性与冲突**：当前实验使用单一宪法测量单一价值维度。当宪法包含内在冲突的准则时（如“诚实”与“善意”在特定场景下可能冲突），EigenBench 能否捕捉到这种价值张力，还是会产生不稳定的排名？

## 原文 PDF

![[paperPDFs/ICLR_2026/EigenBench_A_Comparative_Behavioral_Measure_of_Value_Alignment.pdf]]
