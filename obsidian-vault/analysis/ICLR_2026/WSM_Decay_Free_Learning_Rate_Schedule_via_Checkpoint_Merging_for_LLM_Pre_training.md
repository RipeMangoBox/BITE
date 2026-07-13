---
title: "WSM: Decay-Free Learning Rate Schedule via Checkpoint Merging for LLM Pre-training"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/WSM_Decay_Free_Learning_Rate_Schedule_via_Checkpoint_Merging_for_LLM_Pre_training.pdf
project_link: null
code_link: null
openreview_forum_id: HhThhjKyfw
aliases:
- WSMW
- WSM
tags:
- ICLR_2026
- topic/representation_self_supervised_transfer
- topic/representation_self_supervised_transfer/representation_learning
core_operator: "将学习率衰减替换为检查点合并，利用定理3.1将任意衰减曲线转化为模型平均权重，从而在恒定学习率训练后通过离线合并模拟衰减效果。"
primary_logic: "证明了检查点合并与学习率衰减之间存在理论等价关系：合并权重可以表示为梯度衰减系数的差分，通过选择合适的合并权重可以精确模拟各种衰减策略（余弦、线性、反平方根），从而在不使用动态学习率衰减的情况下获得同等或更好的性能。"
claims:
- "WSM框架在多个基准上一致优于WSD，引入高质量退火数据后，在MATH上提升3.5%，HumanEval上2.9%，MMLU-Pro上5.5%。"
- "合并持续时间是影响模型性能的最关键因素，其重要性超过检查点间隔和合并数量。"
- "定理3.1提供了从梯度衰减系数唯一导出检查点合并权重的方法，使得WSM能模拟任意衰减曲线。"
- "WSM的合并模型在MoE架构中表现出更均衡的路由负载（负载均衡违规值更低），同时维持优越的下游性能。"
---

# WSM: Decay-Free Learning Rate Schedule via Checkpoint Merging for LLM Pre-training

> [!tip] 核心洞察
> 证明了检查点合并与学习率衰减之间存在理论等价关系：合并权重可以表示为梯度衰减系数的差分，通过选择合适的合并权重可以精确模拟各种衰减策略（余弦、线性、反平方根），从而在不使用动态学习率衰减的情况下获得同等或更好的性能。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | WSM：基于检查点合并的LLM预训练无衰减学习率调度 |
| 英文题名 | WSM: Decay-Free Learning Rate Schedule via Checkpoint Merging for LLM Pre-training |
| 会议/期刊 | ICLR 2026 (Oral) |
| Links | [paper](https://openreview.net/forum?id=HhThhjKyfw) |
| Topic | #topic/representation_self_supervised_transfer #topic/representation_self_supervised_transfer/representation_learning |
| Method | Warmup-Stable and Merge (WSM) |
| Dataset | MATH, HumanEval, MMLU-Pro, Overall Average (Base Model) |

> [!tip] 效果简介
> - MATH 上，Accuracy 为 WSM (with annealing data) +3.5%，对比 WSD，变化 +3.5%。
> - HumanEval 上，Accuracy 为 WSM (with annealing data) +2.9%，对比 WSD，变化 +2.9%。
> - MMLU-Pro 上，Accuracy 为 WSM (with annealing data) +5.5%，对比 WSD，变化 +5.5%。

## 概要

大型语言模型预训练中，学习率调度策略对最终模型性能具有决定性影响。当前主流方案——无论是传统的余弦衰减（Cosine）还是近期提出的预热-稳定-衰减策略（**WSD**, Hu et al., 2024）——均要求预先设定总训练步数和衰减函数形式。这带来了一个根本性的瓶颈：当训练需要扩展时，缺乏灵活性，往往需要人工回滚并重新设计衰减计划，显著增加了训练管线的复杂性。

本文提出 **Warmup-Stable and Merge (WSM)** 框架，从根本上消除了对学习率衰减阶段的依赖。其核心洞察在于证明了检查点合并与学习率衰减之间存在理论等价关系：合并权重可以表示为梯度衰减系数的差分，通过选择合适的合并权重，能够精确模拟余弦、线性、反平方根等各种衰减策略的效果。基于这一原理，WSM 将训练简化为“预热 + 恒定学习率”两阶段，随后通过异步离线合并恒定学习率阶段保存的多个检查点来生成最终模型，从而在不使用动态学习率衰减的情况下获得同等或更优的性能。

实验表明，WSM 在多个基准上一致优于 WSD。引入高质量退火数据后，WSM 在 MATH 上提升 **3.5%**，HumanEval 上提升 **2.9%**，MMLU-Pro 上提升 **5.5%**。基础模型和指令微调模型的整体平均得分分别提升 **2.04%** 和 **1.86%**。此外，WSM 在 MoE 架构中展现出更均衡的路由负载，且合并模型可作为训练过程中评估模型衰减潜力的可靠代理，无需启动多次昂贵的真实衰减即可判断模型性能上限。



### 学习率调度的演进与瓶颈

学习率（Learning Rate, LR）调度是深度学习优化中的核心组件，直接影响模型的收敛速度与最终性能。当前主流的大语言模型（LLM）预训练范式普遍采用**预热-衰减**型调度策略，其中最典型的代表包括：

- **余弦衰减（Cosine Decay）**：在预热阶段结束后，学习率按余弦曲线从峰值平滑衰减至接近零，要求预先设定总训练步数 $T_{max}$。
- **预热-稳定-衰减（Warmup-Stable-Decay, WSD）**：在预热后引入一个保持恒定峰值学习率的稳定阶段，随后再进入衰减期。这一设计由Hu等人（2024）提出，旨在通过延长高学习率训练时间来提升模型能力。

然而，上述调度策略共享一个根本性瓶颈：**衰减阶段的执行必须预先确定衰减起始时间、衰减函数形式和总训练步数**。一旦训练需要扩展——例如在预训练后期发现模型仍有提升空间而希望继续训练——就必须面临艰难抉择：要么回滚到衰减前的检查点重新设计调度，要么接受次优的衰减曲线。这种刚性约束显著增加了大规模训练管线的操作复杂性和人工干预成本。

### WSD框架的遗留问题

WSD调度虽然通过稳定阶段缓解了余弦衰减对总步数的强依赖，但其衰减阶段仍然面临两个关键挑战：

1. **衰减策略的不可逆性**：一旦进入衰减期，学习率的单调下降是不可逆的。如果衰减起始过早或衰减函数选择不当，模型可能错失在高学习率下探索更优解的机会。
2. **退火数据时机的耦合**：高质量退火数据（annealing data）的引入通常与衰减阶段绑定，限制了数据策略的灵活性。在实际训练中，何时切换退火数据集往往需要依赖经验判断，而衰减一旦开始便难以调整。

### 核心动机：从衰减到合并的范式转换

本文的核心洞察在于：**学习率衰减的本质效应可以通过检查点合并（Checkpoint Merging）来精确模拟**。具体而言，对恒定学习率训练过程中保存的多个检查点进行加权平均，等价于对梯度序列施加一个合成的衰减系数序列。这一理论等价关系（由定理3.1严格建立）意味着：

- 衰减不再是训练过程中必须在线执行的动态操作，而是可以**离线、异步地通过模型平均**来实现。
- 训练管线可以简化为仅包含预热和恒定学习率两个阶段，彻底消除衰减阶段的设计与调优负担。
- 合并权重可以从任意期望的衰减曲线（余弦、线性、反平方根等）唯一导出，使得框架能够灵活模拟各种衰减策略。

基于上述动机，本文提出**Warmup-Stable and Merge（WSM）**框架，将学习率调度从“在线衰减”范式转换为“离线合并”范式，为LLM预训练提供一种解耦、灵活且性能优越的调度方案。



## 核心方法与创新机理

WSM（Warmup-Stable and Merge）的核心创新在于**用离线检查点合并替代在线学习率衰减**，从根本上消除了传统学习率调度对预设总训练步数和衰减策略的刚性依赖。

### 瓶颈突破：从“衰减依赖”到“合并等价”

传统学习率衰减调度（如 Cosine 和 WSD）要求训练者在训练开始前就确定总步数 $T_{max}$ 和衰减函数形式，一旦训练需要扩展，就必须进行人工回滚和重新调度，显著增加了训练管线的复杂性。WSM 的突破在于证明了**检查点合并与学习率衰减之间存在理论等价关系**：合并权重可以表示为梯度衰减系数的差分，从而在恒定学习率训练后，通过离线加权平均多个检查点来精确模拟任意衰减曲线的效果。

### 关键变量替换（Changed Slots）

WSM 对标准 WSD 调度（Hu et al., 2024）进行了三个关键替换：

1. **学习率调度阶段**：完全消除衰减阶段，仅保留预热和恒定学习率阶段。模型在预热后将学习率固定在峰值，持续训练并定期保存检查点。

2. **模型优化终态生成方式**：不再使用衰减周期结束时的单一检查点，而是对恒定学习率阶段保存的多个检查点进行离线加权平均合并。合并权重由定理3.1从目标衰减曲线唯一导出：
   $$
   \begin{cases}
   c_k = w_k \\
   c_j = w_j - w_{j+1}, \quad j \in [1, k-1] \\
   c_0 = 1 - \sum_{j=1}^k c_j = 1 - w_1
   \end{cases}
   $$
   其中 $w_i$ 为单调非增的梯度衰减系数，$c_j$ 为对应的非负检查点合并权重。这一推导使得 WSM 能精确模拟余弦衰减、线性衰减和反平方根（1-sqrt）衰减等多种策略。

3. **数据退火时机**：可在恒定训练阶段的任意时刻切换到高质量退火数据集（$D_{anneal}$），而合并操作自然地融合多阶段信息，无需像 WSD 那样在衰减期内严格限定退火窗口。

### 理论等价性的深层含义

定理3.1揭示了合并与衰减之间的因果机制：将中间检查点表示为初始状态减去累积梯度更新后，加权平均等价于对每个梯度步骤施加合成衰减系数 $w_i$。这意味着**任何学习率衰减调度都可以在恒定学习率训练完成后，通过选择合适的检查点权重来事后模拟**。这一等价性不仅提供了理论保证，还赋予了 WSM 两个关键优势：

- **训练扩展的灵活性**：无需预设总步数，训练可以随时继续，合并操作可异步进行，生成的合并模型自然地反映了“如果此时开始衰减”的性能。
- **衰减潜力的可靠代理**：合并模型能够在不启动多次昂贵的真实衰减的情况下，准确评估模型在不同训练阶段的后衰减性能（Figure 5a），为训练决策提供低成本信号。

### 与相关工作的本质区别

WSM 与 LaWA、SWA、Model Soups 等模型平均方法的根本不同在于**理论驱动的权重设计**。这些方法通常采用经验性的平均策略（如均匀平均或 EMA），而 WSM 通过定理3.1将合并权重与衰减曲线的数学形式精确绑定。实验表明，1-sqrt 合并优于均值合并，均值合并优于 EMA，这一排序与相应衰减曲线在 WSD 调度中的相对性能完全一致（Table 3），验证了理论推导的有效性。EMA 等凸合并算法性能显著低于其他方法，进一步说明简单的经验平均无法有效模拟衰减效果。



WSM（Warmup-Stable and Merge）的核心思想是将传统学习率调度中的衰减阶段完全移除，代之以恒定学习率训练后的离线检查点合并。整个框架由三个顺序模块构成，形成一条简洁的“训练—保存—合并”管线。

### 管线总览

**预热阶段（Warmup）**：学习率从零线性增加至峰值 $lr_{peak}$，稳定训练初期的优化动态。此阶段与传统调度（Cosine、WSD）完全一致，不引入额外改动。

**稳定训练阶段（Stable Training）**：预热结束后，学习率保持恒定于 $lr_{peak}$，不再随时间衰减。在此阶段，模型持续训练并周期性保存检查点。WSM 的一个关键灵活性在于，可在稳定训练期间的任意时刻将训练数据切换至高质量退火数据集 $D_{anneal}$（Algorithm 1），而无需像 WSD 那样将数据退火与学习率衰减在时间上耦合。这一解耦使得训练管线更加简洁，且便于在训练中途评估模型对退火数据的响应。

**异步检查点合并（Checkpoint Merging）**：稳定训练阶段保存的多个检查点被送入一个异步合并流程。该流程周期性地从存储中获取最近 $n$ 个检查点，根据定理 3.1 计算合并权重并进行加权平均，生成模拟衰减效果的最终模型 $\hat{\theta}_{n+k} = \sum_{j=0}^{k} c_j \theta_{n+j}$。合并过程完全离线执行，不干扰主训练循环。

### 输入输出流

- **输入**：预训练基座检查点（如 2T token 训练后的模型）以及指定的合并策略（如 1-sqrt、均值、EMA）。
- **稳定阶段输出**：以固定间隔（如每 25B token）保存的中间检查点序列。
- **最终输出**：经过加权合并的单一模型，其性能等价于或优于经过真实学习率衰减的模型。

### 与 WSD 的结构性差异

WSM 对 WSD（Hu et al., 2024）的改动集中在两个关键槽位：

| 槽位 | WSD | WSM |
|------|-----|-----|
| 学习率调度阶段 | 预热 → 稳定 → 衰减 | 预热 → 稳定（无衰减） |
| 模型优化终态生成 | 衰减结束时的单一检查点 | 稳定阶段多检查点的加权平均合并 |
| 数据退火时机 | 衰减期内使用退火数据 | 稳定期内任意时刻切换，合并自然融合多阶段信息 |

这一设计使得 WSM 彻底摆脱了对总训练步数 $T_{max}$ 的先验依赖：训练可在任意时刻继续扩展，而无需回滚或重新规划衰减曲线。同时，由于合并权重可通过定理 3.1 从任意衰减曲线导出，WSM 能够以统一的方式模拟余弦衰减、线性衰减、反平方根衰减等多种策略，而无需修改底层优化器或训练管线。

### 理论基础

框架的理论核心是定理 3.1，它建立了检查点合并与学习率衰减之间的形式化等价关系。将中间检查点表示为初始状态减去累积梯度更新：

$$\theta_{n+j} = \theta_n - \sum_{l=1}^{j} g_{n+l-1}$$

代入合并公式后可得：

$$\hat{\theta}_{n+k} = \theta_n - \sum_{i=1}^{k} w_i \cdot g_{n+i-1}$$

其中 $w_i$ 是合成梯度衰减系数。定理 3.1 进一步证明，对于任意单调非增的梯度衰减序列 $\{w_i\}$，存在唯一的非负检查点合并权重 $\{c_j\}$：

$$
\begin{cases}
c_k = w_k \\
c_j = w_j - w_{j+1}, \quad j \in [1, k-1] \\
c_0 = 1 - \sum_{j=1}^{k} c_j = 1 - w_1
\end{cases}
$$

这一推导将“设计学习率衰减策略”的问题转化为“设计合并权重”的问题，为 WSM 的实践提供了严格的理论保证。



WSM 框架的核心在于将传统学习率衰减调度完全替换为**恒定学习率训练后的离线检查点合并**，其理论基石是定理 3.1 所建立的检查点合并与梯度衰减之间的等价关系。

### 问题形式化与合并等价性

给定一个基础检查点 $\theta_n$ 及其后续 $k$ 个检查点 $\theta_{n+1}, \ldots, \theta_{n+k}$，通用的检查点合并操作定义为加权平均：

$$\hat{\theta}_{n+k} = \sum_{j=0}^{k} c_j \theta_{n+j}$$

其中 $c_j \geq 0$ 且 $\sum_{j=0}^k c_j = 1$。

将每个中间检查点表示为初始状态减去累积梯度更新：

$$\theta_{n+j} = \theta_n - \sum_{l=1}^{j} g_{n+l-1}$$

代入合并公式后可得：

$$\hat{\theta}_{n+k} = \theta_n - \sum_{i=1}^{k} w_i \cdot g_{n+i-1}$$

其中 $w_i = \sum_{j=i}^k c_j$ 为合成梯度衰减系数。这一推导揭示了一个关键洞察：**对检查点进行加权平均，等价于对每个梯度更新施加一个合成衰减系数 $w_i$**，从而在数学形式上模拟了学习率衰减的效果。

### 定理 3.1：从衰减曲线到合并权重的唯一映射

定理 3.1 提供了从任意期望的梯度衰减调度到检查点合并权重的逆向推导方法。给定一个单调非增的梯度衰减系数序列 $\{w_1, w_2, \ldots, w_k\}$（满足 $1 = w_0 \geq w_1 \geq \cdots \geq w_k \geq 0$），对应的非负检查点合并权重 $\{c_0, c_1, \ldots, c_k\}$ 由以下公式唯一确定：

$$
\begin{cases}
c_k = w_k \\
c_j = w_j - w_{j+1}, & \text{for } j \in [1, k-1] \\
c_0 = 1 - \sum_{j=1}^{k} c_j = 1 - w_1
\end{cases}
$$

**变量含义**：
- $w_i$：期望施加在第 $i$ 个梯度更新上的合成衰减系数，其单调非增性质保证了合并权重的非负性
- $c_j$：第 $j$ 个检查点的合并权重，$c_0$ 为基础检查点权重
- $k$：合并窗口内的检查点数量

该定理的实用性在于：研究者只需确定目标衰减曲线的函数形式（如余弦衰减、线性衰减、反平方根衰减），即可通过上述公式解析地计算出对应的检查点合并权重，无需任何经验调参。例如，对于 1-sqrt 衰减策略，其梯度衰减系数为 $w_i = 1 - \sqrt{i/k}$，代入定理即可获得相应的 $c_j$ 分布。

### WSM 三阶段管线

基于上述理论，WSM 将训练过程重构为三个模块：

**（1）预热阶段（Warmup）**：学习率从零线性增加至峰值 $lr_{peak}$，稳定训练初期的优化动力学。

**（2）稳定训练阶段（Stable Training）**：学习率保持恒定为 $lr_{peak}$，持续训练并周期性保存检查点。该阶段可灵活地在任意时刻切换到高质量退火数据集 $D_{anneal}$，无需预先规划衰减起点。WSM 的学习率调度简化为：

$$
lr(t) = \begin{cases}
lr_{peak} \cdot \frac{t}{T_{warmup}} & \text{if } t < T_{warmup} \\
lr_{peak} & \text{if } t \geq T_{warmup}
\end{cases}
$$

**（3）异步检查点合并（Checkpoint Merging）**：从存储中获取最近 $n$ 个检查点，根据定理 3.1 计算合并权重并进行加权平均，生成模拟衰减效果的最终模型。该过程离线异步执行，不干扰训练主流程。

### 关键设计选择

- **优化器无关性**：WSM 仅改变学习率调度和最终模型生成方式，不修改优化器内部逻辑（如 Adam 的动量项），因此可无缝集成到现有训练管线中。
- **离线合并的灵活性**：合并操作在训练完成后执行，允许事后尝试不同的合并策略（如不同衰减函数、不同合并窗口），无需重新训练，显著降低了实验成本。
- **单调性约束**：定理 3.1 要求 $w_i$ 单调非增，这限制了可模拟的衰减曲线类型（排除循环学习率等非单调调度），但对于主流的余弦、线性、反平方根衰减策略均满足该条件。



## 实验与关键发现

### 核心发现：WSM 在基座与指令模型上全面超越 WSD

WSM 的核心优势在于，它通过离线检查点合并替代了传统学习率衰减，从而在不牺牲性能的前提下解除了对衰减策略和总训练步数的硬性依赖。实验基于 16.3B 参数的 MoE 模型，从同一预训练检查点出发，在 400B token 的相同训练预算下进行公平对比。

在基座模型评估中，WSM 的总体平均得分达到 **63.95**，相比 WSD 的 62.67 提升了 **2.04%**（Table 1）。这一优势并非仅由个别基准驱动：在数学推理（MATH）、代码生成（HumanEval）和大规模知识评测（MMLU-Pro）上，WSM 分别取得了 **+3.5%**、**+2.9%** 和 **+5.5%** 的显著提升（Abstract）。经过监督微调（SFT）后，WSM 生成的指令模型同样保持领先，总体平均得分从 62.90 提升至 **64.07**（+1.86%，Table 2），验证了合并模型在下游任务中的可迁移性。

![[assets/figures/papers/paper_list_l5_https_openreview_net_forum_id_HhThhjKyfw/figures/006_Table_1.jpg]]
*Table 1: Base model performance comparison. Results are reported based on the checkpoint with the highest average benchmark score*

![[assets/figures/papers/paper_list_l5_https_openreview_net_forum_id_HhThhjKyfw/figures/007_Table_2.jpg]]
*Table 2: Instruct model performance comparison. Results are reported based on the epoch with the highest average benchmark score*

### 合并算法消融：1-sqrt 策略最优，性能排序与衰减曲线一致

不同合并算法对应着不同的隐式梯度衰减曲线。实验系统比较了三种典型策略：指数移动平均（EMA）、均值合并（Mean）和基于定理 3.1 导出的 1-sqrt 合并。结果表明，**1-sqrt 合并以 64.06 的总体得分最优，均值合并次之（63.95），EMA 显著落后（63.01）**（Table 3）。这一排序与 WSD 调度中相应衰减曲线（1-sqrt > 线性 > 指数）的相对性能完全一致，从实证角度强有力地支持了“合并即模拟衰减”的核心理论（Section 4.3.2）。

![[assets/figures/papers/paper_list_l5_https_openreview_net_forum_id_HhThhjKyfw/figures/012_Table_3.jpg]]
*Table 3: Impact of merging algorithm*

EMA 的失败尤为值得关注：其性能不仅远低于其他策略，且对合并窗口大小几乎不敏感（Figure 4），暗示凸型权重分布可能无法有效保留近期梯度的贡献，从而丧失了衰减调度的关键特性。

### 合并持续时间是关键控制变量

合并持续时间（即参与合并的检查点所覆盖的训练 token 跨度）对性能的影响超过检查点间隔和合并数量。实验显示，随着合并窗口从 100B token 扩大到 400B token，模型性能持续提升，但收益逐渐饱和（Figure 4）。这一趋势对 1-sqrt 和均值合并成立，而 EMA 合并则未见明显规律，进一步暴露了其作为衰减模拟的不足。

在固定 80B token 合并持续时间内，更细粒度的检查点保存与合并（如每 5B token 保存，合并 16 个检查点）带来了更好的性能（Table 4）。然而，这直接增加了存储开销，需要在性能增益与工程成本之间进行权衡。

![[assets/figures/papers/paper_list_l5_https_openreview_net_forum_id_HhThhjKyfw/figures/013_Table_4.jpg]]
*Table 4: Comparison of different saving/merging intervals within an 80B-token merge duration. For example, (5B,16) indicates that saving every 5B tokens while merging the latest 16 checkpoints*

### 合并与衰减：替代而非互补

一个自然的问题是：能否将合并与衰减组合使用以获得叠加收益？实验给出了否定的答案。在“先衰减后合并”（Decay-then-Merge）和“先合并后衰减”（Merge-then-Decay）两种配置下，混合策略均未能超越单纯使用 WSM 或 WSD 的最佳结果（Figure 5b, 5c）。这表明合并与衰减在机制上是**替代关系**，二者通过相似的优化路径引导模型收敛，强行组合不会带来额外增益。

### WSM 作为衰减潜力的实时代理

WSM 的另一实用价值在于，它提供了对模型“后衰减潜力”的低成本代理评估。在长程预训练过程中，无需启动多次昂贵的真实衰减即可通过离线合并近似评估模型的衰减后性能。实验表明，WSM 合并模型在 2T、4T、6T、8T、10T token 等多个里程碑上的表现与完整 WSD 衰减运行的结果高度一致（Figure 5a），验证了其作为可靠代理的有效性。

### MoE 路由均衡性的意外收益

在 MoE 架构中，WSM 合并模型展现出比 WSD 衰减模型更均衡的专家路由负载：负载均衡违规值（mean-global-max violation）从 0.601 降至 **0.545**（Table 5）。与此同时，合并模型的测试语言建模损失（test LML）略高于衰减模型，这一“高损失、低违规、强下游”的模式暗示合并可能通过牺牲部分语言建模精度换取了更好的泛化能力和路由多样性。

![[assets/figures/papers/paper_list_l5_https_openreview_net_forum_id_HhThhjKyfw/figures/014_Table_5.jpg]]
*Table 5: Impact on MoE load balancing. The WSM strategy demonstrates improved expert utilization (lower load balancing violation scores) with a slightly higher test language modeling loss. The mean global max violation represents the average of the highest violations across all layers (measuring the severity of “overloaded” experts), while mean global min violation averages the violations for the least-utilized experts (measuring the risk of “routing collapse”)*

### 失败模式与适用边界

WSM 的优势高度依赖于高质量退火数据的引入。当仅使用普通预训练数据时，WSM 与 WSD 性能相当，优势不明显。此外，EMA 等凸合并策略的失效说明并非所有平均操作都能有效模拟衰减——定理 3.1 中单调非增的梯度衰减系数假设排除了非单调调度（如循环学习率）的直接模拟。最后，当前实验主要基于 16.3B MoE 模型，在密集模型或更大规模上的泛化性仍需进一步验证。

### 补充图表

![[assets/figures/papers/paper_list_l5_https_openreview_net_forum_id_HhThhjKyfw/figures/015_Table_6.jpg]]
*Table 6: Detailed model architectures*

![[assets/figures/papers/paper_list_l5_https_openreview_net_forum_id_HhThhjKyfw/figures/016_Table_7.jpg]]
*Table 7: Performance comparison with Muon optimizer on 100B-token enhancement training (initialized from 2T checkpoints)*

![[assets/figures/papers/paper_list_l5_https_openreview_net_forum_id_HhThhjKyfw/figures/023_Table_8.jpg]]
*Table 8: Detailed performance comparison of base models trained using WSM (with three distinct merging algorithms) versus WSD scheduling approaches*

![[assets/figures/papers/paper_list_l5_https_openreview_net_forum_id_HhThhjKyfw/figures/024_Table_9.jpg]]
*Table 9: Detailed performance comparison of checkpoints generated by the WSM and WSD schedule after supervised fine-tuning (SFT). Both base checkpoints are fine-tuned under identical settings for 5 epochs. Results are reported based on the epoch with the highest average benchmark score*

![[assets/figures/papers/paper_list_l5_https_openreview_net_forum_id_HhThhjKyfw/figures/025_Table_10.jpg]]
*Table 10: Detailed performance comparison of checkpoints generated by the WSM and WSD schedule after supervised fine-tuning (SFT). Both base checkpoints are fine-tuned under identical settings for 5 epochs. Results are reported based on the epoch with the highest average benchmark score*

![[assets/figures/papers/paper_list_l5_https_openreview_net_forum_id_HhThhjKyfw/figures/005_Figure_3.jpg]]
*Figure 3: Comprehensive performance comparison (overall and by category) between our WSM schedule (via checkpoint merging, blue line) and standard WSD scheduling (via LR decay, red line). Notably, WSD requires a predefined decay schedule (e.g., over 400B tokens in this study), whereas WSM eliminates this constraint. This flexibility enables seamless training continuation (gray regions) and allows WSM to approximate various decay curves*

![[assets/figures/papers/paper_list_l5_https_openreview_net_forum_id_HhThhjKyfw/figures/017_Figure_6.jpg]]
*Figure 6: Comprehensive performance comparison between different decay strategy of WSM schedule*



## 定位与知识库关联

### 与主流学习率调度策略的关系

WSM的核心定位是**学习率衰减的替代范式**，而非衰减策略本身的改进。传统LLM预训练依赖两类主流调度：（1）**Cosine调度**（Loshchilov & Hutter, 2016），要求预先设定总训练步数 $T_{max}$，在预热后按余弦曲线衰减至零；（2）**WSD调度**（Hu et al., 2024），将训练分为预热、稳定、衰减三阶段，仅在最后阶段执行衰减。两者共同瓶颈在于：衰减策略和总步数必须在训练启动前确定，训练扩展时需人工回滚并重新设计衰减曲线，增加了管线复杂性。

WSM从根因上消解了这一瓶颈：**完全移除在线学习率衰减阶段**，仅保留预热和恒定峰值学习率训练，将“衰减效果”转移到训练完成后的离线检查点合并操作中。定理3.1建立了这一替代关系的理论等价性——给定任意单调非增的梯度衰减系数序列 $\{w_i\}$，可唯一确定非负检查点合并权重 $\{c_j\}$，使得合并模型等价于对梯度施加了合成衰减。这意味着WSM不是对WSD的增量改进，而是一种**调度范式的转换**：从“训练时衰减”变为“训练后合并”。

在性能层面，WSM在16.3B参数的MoE模型上一致优于WSD：基础模型总体平均得分63.95 vs 62.67（+2.04%，Table 1），经监督微调后的指令模型总体平均64.07 vs 62.90（+1.86%，Table 2）。引入高质量退火数据后，在MATH上提升3.5%，HumanEval提升2.9%，MMLU-Pro提升5.5%。值得注意的是，若仅使用普通预训练数据而不引入退火数据，WSM与WSD性能相当，优势不明显——这构成了WSM适用边界的关键约束。

### 与模型合并方法的关系

WSM与现有模型合并工作（如模型汤、EMA、SWA等在线平均策略）存在本质区别。现有合并方法通常作为独立的模型集成或平滑技术，缺乏与学习率衰减的理论关联。WSM的独特贡献在于**建立了合并与衰减的形式化等价关系**，并据此提供了从任意衰减曲线导出合并权重的原则性方法。

这一理论框架解释了为何不同合并算法存在性能差异：1-sqrt合并（模拟1-sqrt衰减）优于均值合并（模拟线性衰减），两者均显著优于EMA合并（凸衰减特性）。Table 3显示，1-sqrt合并总体平均64.06，均值合并63.95，EMA仅63.01。该排序与WSD调度中相应衰减曲线的相对性能一致，验证了合并模拟衰减的有效性。EMA表现极差且对合并持续时间不敏感（Figure 4），其深层优化机制仍是一个开放问题。

### 适用边界与关键约束

**存储-性能权衡**是WSM的主要工程约束。合并需要保存多个中间检查点，更细粒度的保存/合并（如每5B token保存并合并最近16个检查点）带来更好性能（Table 4），但显著增加存储开销。实验表明，在80B token的合并窗口内，(5B,16)配置总体平均63.63，(10B,8)为63.78，(20B,4)降至63.36，(40B,2)进一步降至62.77，单检查点(80B,1)仅60.33。实际部署需在性能增益与存储成本间权衡。

**合并与衰减的不可叠加性**是另一关键发现。实验（Figure 5b, 5c）表明，先衰减后合并（Decay-then-Merge）或先合并后衰减（Merge-then-Decay）均未进一步提升性能，二者是替代关系而非互补关系。这暗示合并与衰减可能作用于相同的优化机制，无法通过简单组合获得叠加收益。

**定理的单调性假设**限制了WSM对非单调调度（如循环学习率、warm restart）的模拟能力。定理3.1要求梯度衰减系数 $\{w_i\}$ 单调非增，以导出非负合并权重。对于需要周期性提升学习率的场景，WSM框架当前无法直接适用。

### 架构适用性

WSM在MoE架构上表现出独特优势。Table 5显示，合并模型的路由负载均衡违规值（mean-global-max-violation）为0.545，低于衰减模型的0.601，表明专家利用率更均衡。同时测试语言建模损失略高，可能意味着合并带来了更好的泛化而非训练集过拟合。权重矩阵条件数分析（Figure 7）和FFN层奇异值熵分析（Figure 8）进一步揭示，合并模型保持更高的参数可塑性，这可能是其在下游任务上表现更优的结构性原因。

WSM被声明为优化器无关（optimizer-agnostic），可与SGD、Adam等无缝集成。Table 7展示了与Muon优化器在100B token增强训练上的兼容性。但当前实验主要基于16.3B参数的MoE模型，在更大规模（万亿参数级）或密集模型上的泛化性仍有待验证。

### 开放问题

1. **合并与衰减的协同机制**：当前实验仅测试了串行组合（先衰减后合并、先合并后衰减），是否可能通过交替应用或其他配置实现协同增益？
2. **EMA的失效原因**：EMA合并性能显著低于其他方法且对合并持续时间不敏感，其深层优化动力学机制是什么？
3. **自适应合并策略**：如何自动确定最优合并窗口、保存间隔及合并权重，避免依赖经验网格搜索？
4. **超大规模扩展**：WSM在万亿参数级模型上的效果如何？存储和计算开销是否可接受？
5. **非单调调度的扩展**：定理3.1的单调性假设能否放松，以支持循环学习率等非单调调度？
6. **长期塑性转化**：合并模型在持续预训练中表现出的更高SVD熵能否转化为后续多任务学习或持续学习场景的正向收益？



## 原文 PDF

![[paperPDFs/ICLR_2026/WSM_Decay_Free_Learning_Rate_Schedule_via_Checkpoint_Merging_for_LLM_Pre_training.pdf]]
