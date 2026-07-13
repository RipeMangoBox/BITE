---
title: "Generalization of RLVR Using Causal Reasoning as a Testbed"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/Generalization_of_RLVR_Using_Causal_Reasoning_as_a_Testbed.pdf
project_link: null
code_link: https://github.com/zhichul/rlcausal
aliases:
- RGD
- GRUCRAT
tags:
- ICLR_2026
- topic/representation_self_supervised_transfer
- topic/representation_self_supervised_transfer/causality
core_operator: "查询层级（关联、干预、反事实）和查询复杂度（相关子图大小|V_rel|）构成两个因果调节变量，可系统地控制任务难度并检验层级内和跨层级的泛化。"
primary_logic: "RLVR在基座模型具备足够推理能力时能够提升泛化，主要通过将边缘化策略转变为增量式边缘化，并减少抽象推导错误与计算错误。更大的模型收益更明显，并且RLVR比SFT更精确，尤其在复杂查询上。"
claims:
- "当模型规模≥7B时，RLVR在同层级的干预和关联查询上显著优于SFT；但在3B和反事实查询上表现不如SFT。"
- "RLVR微调降低了抽象概率推导错误率，并将≥7B模型的边缘化策略转向增量式边缘化。"
- "3B模型经过RLVR后避免显式边缘化，常常直接输出答案，这与微调前推理成功率低相关。"
- "反事实查询对所有规模的模型都极具挑战；即使提供双网络提示，RLVR的性能也未见显著提升。"
---

# Generalization of RLVR Using Causal Reasoning as a Testbed

> [!tip] 核心洞察
> RLVR在基座模型具备足够推理能力时能够提升泛化，主要通过将边缘化策略转变为增量式边缘化，并减少抽象推导错误与计算错误。更大的模型收益更明显，并且RLVR比SFT更精确，尤其在复杂查询上。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 基于因果推理的RLVR泛化研究 |
| 英文题名 | Generalization of RLVR Using Causal Reasoning as a Testbed |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=DZjbL9BuHs) · [GitHub](https://github.com/zhichul/rlcausal) |
| Topic | #topic/representation_self_supervised_transfer #topic/representation_self_supervised_transfer/causality |
| Method | RLVR（基于总变差距离的准确性奖励的GRPO/DAPO） |
| Dataset | RLCausal（过滤后），干预层级中等难度, RLCausal（过滤后），跨层级：关联训练→干预测试（简单）, CLadder 确定性反事实子集（小图，确定性机制） |

> [!tip] 效果简介
> - RLCausal（过滤后），干预层级中等难度 上，CORRECT_t 准确率（TV距离 ≤ 0.01） 为 99.4%（RL 32B），对比 45.9%（SFT 32B），变化 +53.5%。
> - RLCausal（过滤后），跨层级：关联训练→干预测试（简单） 上，CORRECT_t 准确率 为 100.0%（RL 32B 关联训练），对比 SFT模型及基座模型显著更低（具体数值参考 Table 3），变化 显著提升（具体数值未列出）。
> - CLadder 确定性反事实子集（小图，确定性机制） 上，准确率 为 99.7%（RL 32B），对比 70.6%（SFT 32B），变化 +29.1%。

## 概要

本研究以因果推理为检验平台（testbed），系统考察基于可验证奖励的强化学习（RLVR）的泛化能力。核心问题聚焦于：RLVR 能否在结构因果模型（SCM）导出的关联、干预、反事实三类查询上实现有效的层级内及跨层级泛化？其成功的关键条件是什么？

**核心瓶颈与调节机制**。RLVR 的有效性高度依赖基座模型的初始推理熟练度。当基础模型在微调前无法进行显式边缘化或抽象概率推导时（典型如 3B 模型面对复杂查询，或所有模型面对反事实查询），RLVR 会遭遇失败——模型要么放弃显式推理以避免边缘化，要么完全无法习得有效策略。由此，查询层级（关联、干预、反事实）和查询复杂度（由相关子图大小 $|V_{\text{rel}}|$ 衡量）构成两个关键的因果调节变量，可系统控制任务难度并刻画泛化边界。

**方法定位**。本文的 RLVR 基于 GRPO / DAPO 算法，以输出分布与参考答案之间的总变差距离（thresholded）作为准确性奖励，并辅以格式奖励进行优化；其输出要求包含显式推理链和最终概率分布。基线方法包括仅直接预测概率的监督微调（SFT）、基于拒采样正确推理链的 SFT with reasoning chains（RS32），以及基座模型的零样本推理。通过固定数据生成流程（随机 DAG + 二元噪声机制）并在 Qwen‑2.5‑Instruct 系列上改变模型规模（3B、7B、32B），研究得以分离模型先验与微调策略的交互影响。

**核心结论与主要结果**。
- **当模型规模 ≥7B 时，RLVR 在同层级及跨层级的干预和关联查询上显著优于 SFT**，并且 RLVR 比 SFT 更精确，在复杂查询上优势尤为突出（Table 1, Fig. 3, Fig. 6）。
- **RLVR 改善推理质量的关键路径**：降低抽象概率推导错误，并将 ≥7B 模型的边缘化策略从低效方式转向增量式边缘化（Fig. 5, Table 5）；在线 RLVR 在困难查询上优于基于离线推理链的 SFT（RS32），表明 on‑policy 探索对策略改进至关重要。
- **RLVR 的失效边界**：3B 模型经 RLVR 后倾向于回避显式边缘化（Fig. 5 顶部），且延长训练步骤不能引发质的策略变化（Table 11, Fig. 29）；反事实查询对所有规模均极具挑战，即使提供双网络提示，RLVR 性能也未显著提升（Fig. 19, Table 10）。
- **在可泛化的确定性反事实子集上**，RLVR 仍能取得极高精度（32B 达 99.7%），但一旦涉及非平凡的反事实推断和边缘化，性能即急剧下降，揭示出形式化反事实推理与常识性反事实推理之间的能力鸿沟。

综上，RLVR 在基座模型具备足够推理先验时能有效提升泛化，但其局限同样清晰：泛化能力受限于模型已有的推理熟练度，而非奖励信号本身可以任意拓展。这一发现为后续研究 RLVR 的泛化条件、课程学习策略及推理能力的基础瓶颈提供了明确的实验框架。



大型语言模型（LLM）在复杂推理任务中的能力近年来通过强化学习与可验证奖励（Reinforcement Learning with Verifiable Rewards, RLVR）得到显著提升。与依赖人类偏好反馈的标准RLHF不同，RLVR利用可自动验证的正确性信号（如数学题答案、代码执行结果）直接优化模型生成的推理链与最终输出。这种范式已在数学和编程领域展现出强大的泛化能力，但其泛化机制及边界仍缺乏系统性的理解。特别地，**RLVR的成功是否高度依赖于基础模型已有的推理“先验”？当任务超出基座模型的能力边界时，RLVR是否仍然有效？** 这些问题对于将该范式推广到更广泛的推理领域至关重要。

因果推理为研究上述问题提供了一个理想的测试平台。因果推理任务要求模型根据给定的结构因果模型（Structural Causal Model, SCM）和查询，推导并输出目标变量的概率分布 $p^*$。这类问题天然包含三个递进的查询层级——**关联（association）、干预（intervention）和反事实（counterfactual）**（如Fig. 1所示），分别对应从纯观测推理到反事实“如果”场景的推演。同时，任务的难度可通过相关子图大小（$|V_{\text{rel}}|$，如Fig. 2所示）等一系列可控因素进行精细调节。更重要的是，正确的因果推理要求模型执行显式的概率边缘化、条件化以及图结构修改，这些步骤可直接作为“推理过程”被观察和评估。因此，因果推理不仅能检验模型最终答案的准确性，还能通过推理链分析揭示模型内部策略的转变与失败模式。

然而，直接将RLVR应用于因果推理面临显著挑战。初步观察表明，RLVR的有效性严重依赖于基座模型的初始推理能力：当模型在微调前无法自主进行显式概率边缘化或抽象推导时（例如3B参数规模的模型在面对非关联查询时，或所有规模的模型在处理反事实查询时），RLVR往往失效——模型会倾向于放弃显式推理（避免边缘化）或完全无法从奖励中学习。这一现象暗示，**RLVR的泛化并非无条件的，其成功存在一条由模型先验推理熟练度划定的“临界线”**。现有针对RLVR的多数研究聚焦于单一任务层级或固定规模的模型，缺乏对跨层级、跨规模泛化的系统对照，也未能深入解析RLVR改变模型推理质量的内在机理（策略转换 vs. 错误减少）。

鉴于此，本文通过构建大规模合成因果推理数据集（RLCausal），并系统微调Qwen2.5‑Instruct系列模型（3B 至 32B），对比RLVR（基于总变差距离奖励的GRPO/DAPO，见公式(1)）和传统监督微调（SFT）在同层级（within‑level）和跨层级（across‑level）泛化上的表现。我们旨在回答以下核心问题：**（1）RLVR在何种条件下优于SFT？其泛化能力如何受查询层级与模型规模调节？（2）RLVR带来的增益源于推理策略的质变（如从暴力边缘化转向增量式边缘化），还是错误执行的减少？（3）RLVR的失败模式（如3B模型上的回避行为、反事实层级的普遍低效）揭示了哪些深层瓶颈？** 对这些问题的回答不仅能为RLVR的泛化行为提供机理性的解释，也将为设计更稳健的推理增强方法指明方向。



## 核心方法与创新机理

相对于监督微调（SFT）直接最大化参考答案似然和输出概率分布的范式，RLVR 在两个关键维度上做出了根本性重构，使强化学习信号得以作用于推理过程的每一步，从而触发推理策略的质变。

1. **训练目标：从似然最大化转向在线强化学习**。SFT 对输入 $x$ 直接最大化条件概率 $p(p^\star|x)$，完全忽略中间推理过程。RLVR 则采用 GRPO/DAPO 算法最大化期望奖励：
   $$ \mathbb{E}_{x\sim T}\mathbb{E}_{y\sim p_\theta(x)}[r(y)],\qquad r(y)=0.8\cdot r_{\mathrm{ans}}(\hat p_y,p_x^\star)+0.2\cdot r_{\mathrm{format}}(y) $$
   其中 $r_{\mathrm{ans}}$ 为总变差距离 $D(\hat p_y,p_x^\star)$ 低于阈值 $t$ 的指示函数，$r_{\mathrm{format}}$ 由输出概率的可提取性与长度正确性组成（Section 2.2, 公式(1)）。该设计使模型不再是模仿固定答案，而是通过在线采样获得奖励信号，直接在自身生成链上优化精度与格式合规性。

2. **输出格式：从纯概率预测到显式推理链**。SFT 基线仅输出目标变量的概率分布，省略所有推导步骤；RLVR 则强行要求模型先输出完整的自然语言推理链，再从中提取概率分布（Fig. 1 顶部）。这一格式强制模型显式执行边缘化等推导，将其策略暴露在奖励之下。实验表明，在≥7B模型上，RLVR 将边缘化策略从暴力求和转向更高效的**增量式边缘化**，同时大幅降低抽象概率推导错误率（Fig. 5, Table 5）。相比之下，3B模型因微调前推理能力薄弱，RLVR 后反而学会规避显式边缘化以“捷径”作答（Fig. 5 顶部, Fig. 17），这恰好印证推理链格式对基础推理能力的依赖。

3. **在线采样提升复杂查询的策略质量**。与在预先收集的正确推理链上做SFT（RS32）相比，RLVR 的在线采样让模型根据自身当前策略生成响应并优化，因此在困难查询上展现了更强的泛化能力（Table 8, Table 9）。这说明 RLVR 不仅改变了输出结构，更通过 on‑policy 优化改进了策略本身。

上述两个 changed slot（训练目标与输出格式）相互耦合：推理链输出使最终答案的准确性可被链路质量所解释，而总变差距离奖励则为整个推理过程提供了明确的优化目标。当基座模型具备足够的初始推理能力时（≥7B），这套机制可诱导出更优的边缘化策略、减少推导错误，从而在同层级和跨层级泛化上大幅领先 SFT——例如干预层级过滤集上，32B RLVR 达到 99.4% 的准确率，而 SFT 仅为 45.9%（Table 1）。



![[assets/figures/papers/iclr26_0013_DZjbL9BuHs_Generalization_of_RLVR_Using_Causal_Reasoning_as/figures/001_Figure_1.jpg]]
*Figure 1: Top: Our causal inference task for investigating generalization of RLVR (see section 2), system prompt (fig. 8) omitted for space. Bottom Left: Generative process for sampling task instances, and solver for computing the reference (see section 3). Bottom Right: We generate association, intervention, and counterfactual queries to study RLVR’s within-/across-level generalization.3*

本文构建了一套以结构化因果推理为测试平台的系统流程，用于系统探究 RLVR 的泛化行为。整体框架可分为**任务生成**、**微调训练**和**评估推理**三个阶段，三个环节围绕一个统一的输入输出规范衔接：输入为一张随机生成的结构因果模型（SCM）和一个因果查询，输出为一条涵盖概率推导步骤的推理链以及最终目标变量的概率分布。

### 数据生成管线
管线由四个核心模块串联组成（Figure 1 底部左侧）：
1. **图采样器**（Section 3, D1）：迭代添加节点并随机重命名，生成包含 10 个二元变量的随机有向无环图（DAG）。
2. **机制采样器**（Section 3, D2）：为每个变量基于其父节点的赋值采样独立的二元噪声分布，形成条件概率表，从而实例化 SCM 的因果机制。
3. **查询采样器**（Section 3, D3）：随机选择目标变量、观测或干预变量及其取值，构造**关联（association）**、**干预（intervention）**或**反事实（counterfactual）**三个层级的查询。每个层级对应不同的图修改操作（Figure 2）：关联查询保留原始图；干预查询将干预变量替换为常数并移除其入边；反事实查询则通过构建双网络（twin network）转化为关联查询（附录 A.1）。
4. **求解器**（Section 3, D4）：对生成的标准因果模型和查询，根据层级执行对应的图修改后，采用**变量消元（variable elimination）**精确计算参考概率分布 $p^\star$，用作后续训练与评估的 ground truth。

查询难度通过两个因果调节变量进行系统控制：查询层级（关联 → 干预 → 反事实，难度递增）以及**相关子图大小 $|V_{\text{rel}}|$**（定义为在图修改后，观测变量和查询变量的祖先节点数）。训练集按此难度轴混合简单、中等、困难样本。

### 微调训练流程
实验在 Qwen‑2.5‑Instruct 系列模型（3B、7B、32B）上进行两类微调：
- **RLVR 微调**（Section 4.1）：采用 GRPO 或 DAPO 算法，优化期望奖励 $\mathbb{E}_{x \sim T} \mathbb{E}_{y \sim p_\theta(x)}[r(y)]$。每个样本执行 32 次 rollout，批次大小为 8，使用词元级归一化，学习率 $1\times10^{-6}$，训练步数依模型规模调整（3B/7B 为 7.5k 步，32B 为 2.5k 步）。奖励函数由准确性奖励和格式奖励组合而成：

  $$r(y) = 0.8 \cdot r_{\mathrm{ans}}(\hat{p}_y, p_x^\star) + 0.2 \cdot r_{\mathrm{format}}(y),$$

  其中 $r_{\mathrm{ans}}(p,q) = \mathbf{1}[D(p,q) < t]$，$D(p,q)$ 为总变差距离，阈值 $t=0.01$（四舍五入后）；$r_{\mathrm{format}}(y)$ 在概率分布可提取且长度正确时各得 0.5 分。
- **SFT 基线**：将参考概率分布 $p^\star$ 视为直接输出目标，通过最大似然估计进行标准监督微调（5k 步，学习率 $1\times10^{-6}$，选择开发集损失最低的检查点），不包含推理链。此外，还对比了在拒绝采样得到的正确推理链上微调的 SFT 变体（RS32）。

所有微调模型均保留原有的因果推理系统提示（Figure 8），反事实查询的实验还尝试额外提供双网络求解提示（Figure 9）。

### 推理与评估流程
微调后的模型在测试时使用温度 0 解码，生成包含自然语言推理步骤和最终概率分布的完整回复。通过正则表达式从输出中提取概率向量 $\hat{p}_y$，并依据指标 $\mathrm{CORRECT}_t$ 判定正确性：

$$\mathrm{CORRECT}_t(x,y) =
\begin{cases}
0 & \text{若格式错误或无法提取 }\hat{p}_y,\\
1 & \text{若 } D(\hat{p}_y, p_x^\star) \leq t.
\end{cases}$$

这一评估标准严格要求输出的概率分布与 ground truth 在四舍五入到 0.01 精度后总变差距离不超过阈值 $t=0.01$，从而精确衡量模型的概率计算与推理质量。



本节给出方法中的关键模块及其所依赖的核心公式。整体框架由数据生成、模型微调与奖励设计、以及推理评估三部分构成，各模块协同产生受控难度的因果查询样本，并以强化学习（RLVR）优化模型输出的推理链与概率分布。

### 数据生成模块

**图采样器**（Section 3, D1）随机生成包含10个二元变量的有向无环图（DAG），采用迭代添加节点并随机重命名的方式构造图结构。  
**机制采样器**（Section 3, D2）为每个父变量赋值采样二元噪声分布，生成条件概率表，从而定义结构因果模型（SCM）。  
**查询采样器**（Section 3, D3）随机选定目标变量、观测或干预变量及其取值，构造三类查询：关联（association）、干预（intervention）与反事实（counterfactual），分别对应因果层级的不同难度。  
**求解器**（Section 3, D4; Appendix A.1）基于变量消元法精确计算参考答案 $p^\star$。对于关联查询，直接在原始图 $M$ 上消元；对干预查询，通过将干预变量替换为常数并移除其入边，将查询转化为边际查询；对反事实查询，则构建双网络（twin‑network）后转换为关联查询求解。

### 微调模块

**监督微调（SFT）** 对参考答案 $p^\star$ 进行最大似然估计，步数5k，学习率 $1\times10^{-6}$，在开发集上选择最佳检查点。  
**强化学习微调（RLVR）** 采用 GRPO 或 DAPO 策略，每样本进行32次 rollout，批次大小8，学习率 $1\times10^{-6}$，训练步数随模型规模调整（3B/7B: 7.5k 步；32B: 2.5k 步）。与 SFT 不同的是，RLVR 要求模型输出完整的推理链与最终概率分布，而非直接给出答案。

### 核心公式

#### 因果模型定义
SCM 中每个节点的取值由其父节点与独立噪声通过确定性函数确定：

$$
v_i := f_i(\mathrm{pa}(v_i), u_i), \quad u_i \sim q_i,
$$

其中 $\mathrm{pa}(v_i)$ 表示变量 $v_i$ 的父节点集合，$u_i$ 为独立噪声，$q_i$ 为其分布。条件概率表由机制采样器随机生成。

#### 查询层级的形式化转化
\- 关联查询：图与查询保持不变，$M' = M,\; q' = q$。  
\- 干预查询（对 $v_j$ 干预为常数 $c$）：将查询改为边际查询 $q' = p(\mathbf{v}_i)$，修改模型 $M'$ 中 $v_j$ 的机制为 $f_j = c$，并从图中移除所有指向 $v_j$ 的边，即 $G' = (V, E \setminus \{(k \to j) \mid k \in V\})$。  
\- 反事实查询：通过构造双网络，将原 SCM 的每个内生节点复制一份（标记为 $\mathrm{v}_i^{\mathrm{twin}}$），干预施加于副本，随后以关联查询形式求解 $q' = p(\mathrm{v}_i^{\mathrm{twin}} \mid \mathrm{v}_k = v_k)$（见 Appendix A.1）。

#### 强化学习目标
RLVR 的优化目标为最大化训练分布上的期望奖励：

$$
\mathbb{E}_{x \sim T} \mathbb{E}_{y \sim p_{\theta}(x)}\left[r(y)\right],
$$

其中 $x$ 为任务输入（因果图与查询），$y$ 为模型生成的推理链与概率分布，$r(y)$ 为奖励函数。

#### 奖励函数设计
奖励由准确性奖励与格式奖励按比例复合而成：

$$
r(y) = 0.8 \cdot r_{\mathrm{ans}}(\hat{p}_y, p_x^\star) + 0.2 \cdot r_{\mathrm{format}}(y).
$$

**准确性奖励**基于总变差距离 $D(p,q) = \frac{1}{2}\int_x |p(x)-q(x)|\,dx$：

$$
r_{\mathrm{ans}}(p,q) = \mathbf{1}\big[D(p,q) < t\big],
$$

其中阈值 $t$ 控制严格度（文中采用四舍五入后距离≤0.01）；若模型输出的分布 $\hat{p}_y$ 与参考答案 $p_x^\star$ 的 TV 距离低于阈值，则奖励为 1，否则为 0。  
**格式奖励**要求输出可解析且长度正确：

$$
r_{\mathrm{format}}(y) = 0.5 \cdot \mathbf{1}[\hat{p}_y \text{ extractable}] + 0.5 \cdot \mathbf{1}[\hat{p}_y \text{ length correct}].
$$

#### 答案提取与评估指标
推理阶段使用温度0解码，通过正则表达式从生成文本中提取概率分布 $\hat{p}_y$。最终以指标 $\mathrm{CORRECT}_t$ 判定一次性准确性：

$$
\mathrm{CORRECT}_t(x,y) =
\begin{cases}
0 & \text{格式错误，无法提取 }\hat{p}_y,\\
1 & \text{若 } D(\hat{p}_y, p_x^\star) \leq t.
\end{cases}
$$

该指标综合了格式有效性和概率分布的精确度，是后续实验的核心评价标准。



## 实验与关键发现

实验基于合成因果图与查询，覆盖关联、干预、反事实三个层级，并以相关子图大小 $|V_{\text{rel}}|$ 作为难度度量（Fig. 7）。模型为 Qwen 2.5‑Instruct 系列（3B、7B、32B）；RLVR 采用 GRPO/DAPO，奖励由总变差距离阈值 $t=0.01$ 和格式合规组成，SFT 基线最大化参考答案 $p^*$ 的条件对数似然。评估指标 $\mathrm{CORRECT}_t$ 要求提取的概率分布与 $p^*$ 的总变差距离（四舍五入后）≤ $t$。除非特别说明，结果指过滤测试集上的同层级泛化。

### 主结果：RLVR 在干预与关联层级显著领先，但局限于大模型
- **同层级泛化**：对≥7B 的模型，RLVR 在干预和关联查询上均大幅超越 SFT（Fig. 3 左，Table 1）。例如，32B RLVR 在中等难度干预查询上准确率达 **99.4%**，而 SFT 仅 **45.9%**；7B 模型在关联查询上也保持类似优势。然而，3B 模型在各层级上 RLVR 均未超越 SFT，甚至可能更差。
- **跨层级泛化**：当用关联查询训练时，32B RLVR 在简单干预测试集上仍可达到 **100%** 准确率（Table 3），表明习得的推理策略可在层级间迁移。但反事实查询几乎无法通过跨层级学习解决，至多停留在极低水平（Fig. 4 右，Table 3、4）。
- **规模‑性能关系**：RLVR 与 SFT 的性能差距随模型增大而扩大，且跨层级泛化损失随规模增加而收窄（Fig. 4 顶部），提示较大的模型更好地利用了 RL 的探索信号。

![[assets/figures/papers/iclr26_0013_DZjbL9BuHs_Generalization_of_RLVR_Using_Causal_Reasoning_as/figures/027_Table_1.jpg]]
*Table 1: Within level generalization (test, filtered). System accuracy (average CORRECT, see eq. (3)) when training and evaluating on queries from same level. Stratified by query level, and difficulty within each level, as measured by | $V _ { \mathrm { r e l } }$ | , the size of the relevant subgraph to the query variable. Note that difficulty is not comparable across different levels. The models are trained on a mix of small/medium/large questions. Systems not significantly worse than the best (with a monte-carlo paired permutation test with n=10000) are bolded. Table 2: Within level generalization (test, unfiltered). System accuracy (average CORRECT, see eq. (3)) when training and evaluating on que...*

![[assets/figures/papers/iclr26_0013_DZjbL9BuHs_Generalization_of_RLVR_Using_Causal_Reasoning_as/figures/028_Table_3.jpg]]
*Table 3: Across-level generalization (test, filtered). Row specify which level trained on, column specify which level evaluated on. System accuracy (average CORRECT, see eq. (3)) on evaluation sets of different difficulties, as measured by | $V _ { \mathrm { r e l } }$ | |, the size of the relevant subgraph to the query variable. Note that difficulty is not comparable across different levels. The models are trained on a mix of easy/medium/hard questions. Systems not significantly worse than the best (with a montecarlo paired permutation test with n=10000) are bolded*

![[assets/figures/papers/iclr26_0013_DZjbL9BuHs_Generalization_of_RLVR_Using_Causal_Reasoning_as/figures/008_Figure_4.jpg]]
*Figure 4: Top: Accuracy (y-axis) vs. LLM size (x-axis) when evaluated on intervention (left), association (middle), and counterfactual (right) queries. Red curves correspond to RLVR, blue curves correspond to SFT. Solid (-) curves are LLMs fine-tuned on the same level as evaluation, dashed (--) curves are trained on a different level from evaluation. Bottom: Reasoning (RLVR) vs non-reasoning (SFT) strategies, before and after fine-tuning. As scale increases, both reasoning and non-reasoning prior improve, though the reasoning prior benefits more from scaling*

### 推理策略的变迁：从暴力求和到增量边缘化
用 o4‑mini 对推理链自动分类（Fig. 5，Table 5，示例见 Fig. 14‑17）发现：
- 7B 与 32B 模型经 RLVR 后，边缘化策略明显从“暴力求和所有变量”或“仅对直接父节点求和”转向 **增量式边缘化**——有序地消去不相关变量，保留条件依赖。
- 3B 模型则出现 **回避边缘化** 现象：微调后更频繁地直接输出概率分布，完全跳过显式求和步骤（Fig. 5 顶部，Fig. 17）。该行为与微调前推理成功率极低一致。
- 推导错误（概率误用等）在≥7B 模型上经 RLVR 后显著下降，算术错误亦有改善，但复制错误的减少不明显（Fig. 5 底部，Fig. 27，Table 5）。错误率的降低直接支撑了准确率的提升。

![[assets/figures/papers/iclr26_0013_DZjbL9BuHs_Generalization_of_RLVR_Using_Causal_Reasoning_as/figures/011_Figure_5.jpg]]
*Figure 5: LLM judge (o4-mini) analysis of the marginalization strategy (top) and the existence of derivation errors (bottom) before and after RLVR. Derivation errors and marginalization strategies are annotated on (the same) 80 samples per level. Judge prompts (including category definitions) are included in fig. 11. Example traces of marginalization strategy are included in figs. 14 to 17*

### 查询复杂度与精度分析
- 按 $|V_{\text{rel}}|$ 分层后，RLVR 在复杂查询上的优势更加突出：32B 模型在大难度干预子集上仍接近满分，而 SFT 准确率急剧衰减（Table 1）。Fig. 6 顶部显示，SFT 随复杂度增加的衰退斜率比 RLVR 陡。
- 若放宽正确性阈值 $t$（即接受更大误差），RLVR 的准确率提升幅度普遍高于 SFT（Fig. 6 底部，详见 Fig. 22‑24），说明 RLVR 产出的不仅“更正确”，而且概率分布 **更精确**。

### 消融实验
- **训练步数与容量**：将 3B RLVR 训练从 7.5k 步延长至 30k 步仅带来微小精度提升，边缘化策略未发生质性变化（Table 11，Fig. 29）。额外训练无法弥补基础推理能力的缺失。
- **反事实提示**：在系统提示中加入双网络（twin‑network）求解指引，未能提升 RLVR 在反事实层级上的性能（Fig. 19）。失败并非源于缺少图变换知识，而是深层推理能力不足。
- **在线 RL vs. 离线推理链 SFT**：对 7B 模型，使用拒绝采样正确推理链进行 SFT（RS32）的结果显著弱于在线 RLVR，表现尤以困难查询为甚（Table 8、9）。这凸显了在线策略探索对泛化的关键作用。
- **Cladder 确定性反事实子集**：在该小规模、确定性机制的反事实子集上，32B RLVR 可达 **99.7%**，远超 SFT 的 70.6%（Table 10），表明当问题足够简单时 RLVR 也能攻克反事实层级。

![[assets/figures/papers/iclr26_0013_DZjbL9BuHs_Generalization_of_RLVR_Using_Causal_Reasoning_as/figures/033_Figure_19.jpg]]
*Figure 19: Counterfactual level with hint. Prompting with a hint about how to solve counterfactual queries by twin-network-graph is not enough to induce genuine solutions and improve performance post-RLVR. From left to right is accuracy breakdown on all, small, medium, and finally large problems. Having hint in the prompt did not significantly improve RLVR’s performance on counterfactual level*

### 失败模式与讨论
- **反事实查询普遍难解**：所有规模模型经 RLVR 后，在自建反事实测试集上准确率均低于 20%（Table 1 中 32B RLVR 仅 16.4%）；加入提示亦无改善（Fig. 19）。形式化反事实推理需要构建双网络、推断外生变量，其抽象程度超出了当前 LLM 的先验能力。
- **小模型的“捷径”行为**：3B RLVR 常产出逻辑不一致的推理（如错误忽略相关变量）或直接跳至答案（Fig. 17、18），推导和算术错误率居高不下。RL 奖励信号在基础能力薄弱时鼓励模型规避推理而非学习正确策略——这是 RLVR 泛化失败的因果机制。
- **极端复杂度承受力有限**：当 $|V_{\text{rel}}|$ 接近 10 时，即使 7B 模型的 RLVR 准确率也会明显下降（Fig. 6 顶部），受限于上下文长度和处理全图的认知负荷。

### 公平性评价与局限
- 全部结论基于合成 SCM（二元变量、10 节点），迁移至真实因果图或连续变量需谨慎。
- 模型限于 Qwen 2.5‑Instruct 家族，跨 LLM 系列的泛化性未经验证。
- 数据集由作者生成，图表结构或查询分布可能偏向特定类型，影响外部效度。
- 严格阈值 $t=0.01$ 可能将微小算术误差导致的近似正确答案判为错误，低估模型潜在的推理能力。
- 仅探测了有限超参数组合（奖励权重、学习率等），未必达到全局最优。

综合以上，**RLVR 泛化的核心瓶颈在于基座模型先验的推理熟练度**：当模型在微调前已具备变量消元、条件概率推导等基本操作时，RLVR 能通过奖励塑形将其策略提升为增量式边缘化并减少推导错误；否则 RL 只会诱导模型走捷径。查询层级（关联、干预、反事实）和复杂度构成两个有效的因果调节变量，可用于系统地检验层级内与跨层级的泛化行为。



## 定位与知识库关联

RLVR（基于总变差距离奖励的GRPO/DAPO）在因果推理任务中构建了一个清晰的对比弧线：它与典型的有监督微调（SFT）基线形成对照，通过奖励机制将学习目标从最大化参考答案的条件对数似然转变为期望奖励的最大化（`$\mathbb{E}_{x \sim T} \mathbb{E}_{y \sim p_{\theta}(x)}[r(y)]$`，Section 2.2）。这一转变的核心差异体现在训练目标和输出格式两个关键槽位上：SFT直接输出概率分布 `$p^\star$` 的对数似然，而RLVR要求输出推理链加概率分布，并以总变差距离低于阈值（`$r_{\mathrm{ans}}(p,q)=\mathbf{1}[D(p,q)<t]$`）和格式合规作为复合奖励信号。该方法并非凭空产生，而是对GRPO（Shao et al., 2024）和DAPO（Yu et al., 2025b）在数学推理等领域的成功经验的直接移植，但被置于形式因果推理的测试床上，从而暴露出一系列独特的边界条件。

**与Baseline的关系及内部机制**

论文比较了三种基线：(1) SFT（直接预测，无推理链）；(2) SFT with reasoning chains（RS32，在拒绝采样得到的正确推理链上微调）；(3) 基座模型的零样本推理（cot init）。在同层级泛化测试中（Table 1, Fig. 3 左），当模型规模达到7B及以上时，RLVR在关联和干预查询上的准确率显著优于SFT（`p<0.05`，paired permutation test）。然而，对于3B模型和所有规模的反事实查询，SFT反而更优或持平；这一逆转暴露了RLVR有效性的前提：基座模型必须具备一定水平的初始推理能力（real_bottleneck）。

RS32（离线思维链）的对比实验进一步区分了监督信号的来源。Table 8和Table 9显示，即便在正确的推理链上做SFT，其表现仍不如在线RLVR，尤其是在高复杂度查询上。这表明RLVR的优势不仅在于“见过正确的推理”，更在于on‑policy探索中通过奖励对策略进行塑造——它能够推动模型将边缘化策略从暴力求和转向增量式边缘化（Fig. 5顶），并大幅减少抽象概率推导错误（Fig. 5底）。对于7B和32B模型，RLVR后推导错误率下降显著；但对3B模型，RLVR的非但未能催生增量式边缘化，反而使其学会了避免显式边缘化（Fig. 5顶、Fig. 17），直接输出答案的倾向增强——这种“奖励黑客”行为源于模型在微调前就缺乏执行正确边缘化的能力，因此强化信号只能强化其逃避行为。

**适用边界：由规模与查询层级定义的调节变量**

论文提出的两个因果调节变量——查询层级（关联、干预、反事实）和查询复杂度（`$|V_{\mathrm{rel}}|$`，相关子图大小）——精准划定了RLVR的有效区间。当模型规模≥7B且查询为干预或关联时，RLVR能够实现跨层级的泛化：例如，仅在关联查询上训练的7B RL模型在干预简单查询上依然能达到100%准确率（Table 3），说明推理能力在不同因果层级间可迁移。但当模型退缩至3B，或查询上升至反事实层级时，这种泛化几乎失效：所有规模的反事实查询准确率均极低（Table 1中RL 32B仅16.4%），且提供双网络求解提示（twin‑network hint）也不能显著改善RLVR的性能（Fig. 19）。这表明，反事实推理所需的形式化双网络构造和反事实边际化操作对当前LLM而言仍是难以跨越的门槛——它不仅仅依赖于“做对的事”，更依赖于“知道如何做”，而后者需要更深层次的结构理解，难以通过RLVR的表面奖励塑造出来。

在复杂度维度上，SFT倾向于在低复杂度查询上占优，而RLVR的优势随 `$|V_{\mathrm{rel}}|$` 增大而凸显（Fig. 6顶），因为复杂查询要求更高效的推理策略（增量式边缘化）和更低的计算错误率，这正是RLVR所能强化的方面。这一模式进一步验证了“推理熟练度先验”的约束作用：如果模型在微调前连基本的边缘化意图都不具备（3B），则RLVR无法突破这一先验，反而会被奖励引导至更简单的行为。

**局限性**

实验设计本身设定了清晰但严格的范围，使结论外推时需格外谨慎：

- **数据域的合成性**：整个研究基于二元变量、10节点的随机DAG和机制采样的合成SCM，图结构与查询分布由作者定义，因此结论是否适用于真实因果图、连续变量或更大规模图尚待验证（fairness_notes）。  
- **模型家族的孤立性**：所有实验均使用Qwen2.5‑Instruct系列模型，其他LLM家族（如Llama、Gemini）上的适用性未经验证。由于不同基座模型的推理先验差异很大，RLVR的效果可能迥异。  
- **指标的严格性**：`CORRECT_t` 要求四舍五入后TV距离≤0.01，这一硬阈值会惩罚那些推理过程正确但存在微小计算舍入误差的解。Fig. 6底显示，当放宽阈值t时，RL模型的精度优势更为明显，但严格阈值下可能低估部分近似正确的模型。  
- **超参数探索有限**：奖励函数中准确性/格式权重（0.8/0.2）、TV距离阈值t等超参数仅采用了一种配置，其敏感性未被系统研究（open_questions）。3B模型训练步数从7.5k延长至30k未带来质变（Table 11, Fig. 29），暗示问题核心不在于优化时长，而在于模型表示本身。

**开放问题**

论文结尾提出的问题指向该方向未来的关键路径：

1. **执行质量 vs. 策略质量**：RLVR究竟在多大程度上改善了执行（减少算术/复制错误）而非策略（选择更优的边缘化路径）？Fig. 5和Fig. 27虽分别统计了推导和算术错误，但二者常相互交织，解耦这两类贡献需要更精细的受控实验。  
2. **常识反事实与形式化反事实的鸿沟**：为何在CLadder确定性反事实子集上RLVR 32B可达99.7%（Table 10），而在合成的随机性反事实查询上却低于20%？这一差距指向形式化程度、噪声机制和图的随机性产生的深层互动。  
3. **数据规模的挑战**：节点数、变量基数或图形状的扩大能否系统性地提升任务难度，以进一步挑战RLVR的泛化极限？若能构建更大规模、更异构的SCM，可能会诱发更丰富的推理行为，但也可能重复当前的失效模式。  
4. **反事实难点本质**：即使给予双网络提示（明确告知求解方法），RLVR仍无法学习有效推理（Fig. 19），这说明问题不在于方法缺失，而在于模型在训练过程中无法将提示转化为可靠的操作序列。这是否意味着当前LLM缺乏处理双世界结构的表示能力？  
5. **小模型的拯救路径**：课程学习、渐进式复杂度增长或分阶段训练能否帮助3B模型越过推理先验门槛，从而利用RLVR获得提升？若能，将为小模型的推理训练开辟新范式。



## 原文 PDF

![[paperPDFs/ICLR_2026/Generalization_of_RLVR_Using_Causal_Reasoning_as_a_Testbed.pdf]]
