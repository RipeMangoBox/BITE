---
title: "A Fano-Style Accuracy Upper Bound for LLM Single-Pass Reasoning in Multi-Hop QA"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/A_Fano_Style_Accuracy_Upper_Bound_for_LLM_Single_Pass_Reasoning_in_Multi_Hop_QA.pdf
aliases:
- FSAUBLSPRMHQ
- InfoQA
tags:
- ICLR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/language_speech_and_dialog
core_operator: "任务信息需求β与模型输出容量C之间的比值。β由跳数h、上下文长度L、噪声水平等因素决定；C由模型架构和输出长度决定。"
primary_logic: "单次推理范式存在根本性的信息瓶颈，无法可靠地解决复杂多跳推理任务。通过容量感知的任务分解、依赖显式的工作流和迭代查询压缩，多轮调用范式可以规避这一瓶颈。"
claims:
- "单次推理准确率存在Fano式上界：h(Acc) + (1-Acc)log(|A|-1) ≥ β - C"
- "当β > C+1时，准确率上界按(C+1)/β双曲线衰减（Accuracy Cliff）"
- "信息需求β随跳数h和上下文长度L超线性增长：β(h,L) = β_0 + αL γ^(h-1)"
- "整体成功概率随跳数线性衰减：Pr(Succ) ≥ (1-ε)^(K+1) ≈ 1 - (K+1)ε"
---

# A Fano-Style Accuracy Upper Bound for LLM Single-Pass Reasoning in Multi-Hop QA

> [!tip] 核心洞察
> 单次推理范式存在根本性的信息瓶颈，无法可靠地解决复杂多跳推理任务。通过容量感知的任务分解、依赖显式的工作流和迭代查询压缩，多轮调用范式可以规避这一瓶颈。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 多跳问答中LLM单次推理的Fano式准确率上界 |
| 英文题名 | A Fano-Style Accuracy Upper Bound for LLM Single-Pass Reasoning in Multi-Hop QA |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=dPAcHrG4rl); [GitHub](https://github.com/KaiyangWan/InfoQA) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/language_speech_and_dialog |
| Method | InfoQA |
| Dataset | 合成多跳QA基准, 合成多跳QA基准 (Qwen3-14B), 合成多跳QA基准 (Qwen3-8B), 合成多跳QA基准 (Qwen3-8B, 4跳, 8k上下文) |

> [!tip] 效果简介
> - 合成多跳QA基准 上，F1 为 0.86，对比 0.75 (S-C)，变化 +0.11。
> - 合成多跳QA基准 (Qwen3-14B) 上，F1 为 0.86，对比 0.73 (CoT)，变化 +0.13。
> - 合成多跳QA基准 (Qwen3-8B) 上，F1 为 0.74，对比 0.66 (S-C)，变化 +0.08。

## 概述

本工作揭示了多跳问答（MHQA）中大语言模型（LLM）单次推理的根本性瓶颈：存在一个与信息论中Fano不等式形式相似的准确率上界。核心发现是，当任务的信息需求（β）超过模型的输出容量（C）时，准确率会经历一个急剧的“准确率悬崖”（Accuracy Cliff）——一旦β > C+1，准确率上界将按照(C+1)/β的双曲线形式衰减。这一瓶颈源于单次推理的固有限制：模型必须在一次前向传播中，将整个多跳推理链和长上下文压缩到有限的输出序列中。

论文将信息需求建模为β(h, L) = β_0 + αL γ^(h-1)，其中h是跳数，L是上下文长度。该模型揭示了两个关键放大机制：上下文长度L的线性增长，以及跳数h的指数膨胀（当γ>1时）。实验表明，这种跳数膨胀主要由上下文中的干扰项（distractors）驱动——去除干扰项后γ≈1，表明噪声而非推理深度本身是导致信息需求爆炸的主因。此外，链式结构还放大了单步误差：整体成功概率Pr(Succ) ≥ (1-ε)^(K+1) ≈ 1 - (K+1)ε，随跳数线性衰减。

基于这一理论分析，论文提出了InfoQA框架——一个概念验证性的多轮调用（multi-call）方法。InfoQA通过三个核心组件规避单次推理的信息瓶颈：容量感知的任务分解（将多跳问题拆解为单跳子问题）、依赖显式工作流（通过压缩后的查询显式传递推理状态）、以及迭代查询压缩（修剪推理轨迹并重写查询以控制提示长度）。在包含7200个样本的合成MHQA基准上（控制跳数h∈{1,2,3,4}和上下文长度L∈{0.5k,1k,2k,4k,8k,10k}），InfoQA在Qwen3-14B上取得了2-4跳平均F1=0.86的显著结果，远超最佳单次基线Self-Consistency（0.75）和Chain-of-Thought（0.73）。消融实验验证了各组件的必要性：去除任务分解后F1降至0.65，去除轨迹修剪后降至0.78。在更具挑战的4跳8k上下文设置下，InfoQA（0.67）与最佳单次基线（0.16）之间的差距扩大至0.51，清晰展示了多轮调用范式在极端条件下的优势。

## 背景与动机

多跳问答（MHQA）要求模型在长上下文中串联多条推理链才能得出答案。当前主流方法——包括思维链（CoT）、自一致性（S-C）、ReAct 等——本质上仍是**单次推理范式**：模型在单次前向传播中一次性完成检索、推理和答案生成。该论文的核心洞察在于，这种单次调用存在一个根本性的信息瓶颈，且该瓶颈可以通过信息论工具严格刻画。

**信息瓶颈的数学刻画。** 论文从 Fano 不等式出发，推导出单次推理准确率的理论上界。核心逻辑链条如下：

1. **输出容量 C 是硬约束。** 模型在单次调用中能携带的信息总量受限于输出熵 `H(Y)`。对于固定长度 m 的 token 序列，`H(Y) ≤ m log|V|`（`|V|` 为词表大小）；对于变长输出，上界为 `log((|V|^{m+1} - 1)/(|V| - 1))`。论文将此定义为模型的**单次输出容量 C**。
2. **任务信息需求 β 超线性增长。** 多跳任务所需的信息量并非随跳数线性增长。论文提出信息需求模型 `β(h, L) = β_0 + αL γ^{h-1}`，其中 `h` 为跳数，`L` 为上下文长度，`γ > 1` 表征跳数膨胀因子。这意味着每增加一跳，信息需求以 `γ` 倍放大，而上下文长度 `L` 进一步放大基数。
3. **准确率悬崖（Accuracy Cliff）。** 将上述两点代入 Fano 不等式，得到单次推理准确率的统一上界：`h(Acc) + (1-Acc)log(|A|-1) ≥ β - C`。当 β 接近并超过 C 时，准确率发生相变。在均匀答案分布假设下，上界简化为 `Acc ≤ min{1, (C+1)/β}`。当 `β > C+1` 时，准确率随 `(C+1)/β` 双曲线衰减（Figure 2）。

**现有方法的局限性。** 上述理论框架揭示了现有方法的两个根本短板：

- **信息需求膨胀不可控。** 实验拟合参数（Table 3, Table 4）显示，即使 CoT 和 S-C 能通过增加输出长度来提升有效容量 C，其跳数膨胀因子 γ 依然显著大于 1。这意味着随着跳数增加，信息需求增速远超容量提升。去除干扰项后 `γ ≈ 1`，表明跳数膨胀主要由噪声引起，而非推理深度本身。
- **误差累积效应。** 在单次推理中，任何中间步骤的误差都会污染后续推理。论文推导出整体成功概率的下界为 `Pr(Succ) ≥ (1-ε)^{K+1} ≈ 1 - (K+1)ε`（Equation 10），其中 ε 为每步错误率，K 为跳数。即使 ε 很小，多跳场景下的累积衰减也极为显著（Figure 3）。

**本文动机：从单次推理到多轮调用。** 面对上述信息瓶颈，论文的核心动机是：**能否通过改变推理范式来规避单次调用的容量天花板？** 具体而言，将单次推理分解为多轮调用的顺序子任务，每轮只处理一个单跳子问题，通过压缩后的查询显式传递推理状态。这种范式转换等价于将 β 从超线性增长拉回线性甚至常数水平，同时通过迭代查询压缩保持每步的 C 不随推理深度膨胀。论文提出的概念验证框架 InfoQA 正是这一思路的实现（Figure 4），其三个核心组件——容量感知任务分解、依赖显式工作流、迭代查询压缩——分别对应降低 β、确保状态对齐、控制 C。

## 核心创新

该工作的核心创新在于：**将单次推理的瓶颈形式化为一个可量化的信息容量边界（Fano式准确率上界），并据此设计了一个容量感知的多轮调用框架（InfoQA）来规避该瓶颈。**

与所有单次推理基线（Direct Prompting, CoT, S-C, S-R, ReAct, P&S, S-A）相比，InfoQA在四个关键槽位上做出了根本性改变：

1.  **推理范式**：从单次调用（single-pass）切换到多轮调用（multi-call）。这是最根本的改变。单次推理的准确率存在一个Fano式上界：`h(Acc) + (1-Acc)log(|A|-1) ≥ β - C`（Theorem 1）。当信息需求β超过输出容量C+1时，准确率会按`(C+1)/β`双曲线急剧衰减，即“Accuracy Cliff”（Figure 2）。多轮调用通过将推理过程分解为多个独立步骤，使每步的信息需求都远低于容量上限，从而避免触发悬崖。

2.  **任务分解**：从无显式分解变为容量感知的任务分解（Capacity-Aware Task Decomposition）。单次推理中，信息需求β随跳数h和上下文长度L超线性增长：`β(h,L) = β_0 + αLγ^(h-1)`（Equation 6）。InfoQA将多跳问题显式分解为一系列单跳子问题，从而将每步的信息需求从超线性增长降低到近似常数水平。消融实验表明，去除该组件（w/o D.）后，InfoQA的平均F1从0.86骤降至0.65（Table 2），证明这是性能提升的核心驱动力。

3.  **推理状态传递**：从依赖模型内部记忆变为依赖显式工作流（Dependency-Explicit Workflow）。单次推理中，模型需要在其内部表示中维持跨步骤的推理状态，这极易受噪声干扰。InfoQA通过压缩后的查询（contracted query）显式传递推理状态，确保每一步的输入都清晰对齐当前子任务。这直接缓解了误差累积问题：整体成功概率的下界为`Pr(Succ) ≥ (1-ε)^(K+1) ≈ 1 - (K+1)ε`（Equation 10），显式状态传递通过降低单步错误率ε来减缓成功概率的线性衰减。

4.  **提示长度管理**：从提示长度随推理深度线性增长变为迭代查询压缩（Iterative Query Contraction）。单次推理中，随着推理深度增加，提示中累积的推理轨迹会迅速膨胀，进一步推高信息需求β。InfoQA通过修剪推理轨迹并重写查询，将提示长度控制在固定范围内。消融实验显示，去除轨迹修剪（w/o P.）后，F1从0.86降至0.78（Table 2），表明该组件对维持长链推理的稳定性至关重要。

**因果机制**：InfoQA的核心洞察是，单次推理的瓶颈根源于信息需求β与输出容量C之间的比值。当β远大于C时，任何单次调用策略（包括CoT、S-C等）都无法避免Accuracy Cliff。实验证据支持这一观点：Figure 5显示，所有单次方法的经验F1点都紧密贴合理论边界，并在`β ≳ C+1`时集体崩溃。CoT和S-C通过增加有效容量C（在Qwen3-14B上C≈131）和降低跳数膨胀因子γ（≈2.08）来部分缓解悬崖（Table 3），但这只是推迟而非消除瓶颈。相比之下，InfoQA通过将问题分解为容量可控的子步骤，从根本上使每步的β远小于C，从而在4跳、8k上下文的极端条件下达到0.67 F1，而最佳单次基线仅0.16（Table 5）。

**证据强度**：所有核心创新点均有定理证明（Theorem 1）或消融实验（Table 2）支撑，置信度均为1.0。关于γ主要由噪声而非深度引起的结论（去除干扰项后γ≈1）置信度为0.95，源于拟合分析的间接证据。

## 整体框架

![[assets/figures/papers/iclr26_0002_dPAcHrG4rl_A_Fano-Style_Accuracy_Upper_Bound_for_LLM_Single/figures/004_Figure_4.jpg]]
*Figure 4: The InfoQA framework integrates three key components: (1) Capacity-Aware Task Decomposition, which reduces the information demand by generating single-hop sub-questions; (2) Dependency-Explicit Workflow, where the evolving contracted query carries the reasoning state across steps; and (3) Iterative Query Contraction, which prunes reasoning traces and rewrites the query with $\hat { Z } _ { k }$ . Each LLM call approximates $\phi _ { k }$ and produces $\hat { Z } _ { k }$

本文的核心贡献在于揭示并验证了单次推理范式的信息容量瓶颈，并提出了一个概念验证性的多轮调用框架 **InfoQA** 来规避该瓶颈。整体框架由理论分析和实证系统两部分构成，两者紧密耦合。

**理论框架** 建立了一个分析多跳问答中LLM推理准确率的因果模型。其核心是一个Fano式准确率上界（Theorem 1）：`h(Acc) + (1-Acc)log(|A|-1) ≥ β - C`。该公式将任务的信息需求β与模型输出容量C之间的差距，直接映射到准确率的上限。当β超过C时，准确率会经历一个“准确率悬崖”（Accuracy Cliff），即当β > C+1时，上界按`(C+1)/β`双曲线衰减。该理论进一步将信息需求β建模为跳数h和上下文长度L的函数：`β(h, L) = β_0 + αL γ^(h-1)`。该模型揭示了β随h和L超线性增长的根本原因，其中参数γ（跳数膨胀因子）量化了噪声和推理深度对信息需求的复合放大效应。此外，对于多轮调用范式，理论模型（Equation 10）指出，整体成功概率`Pr(Succ) ≥ (1-ε)^(K+1) ≈ 1 - (K+1)ε`，表明误差会随步骤数K线性累积。

**实证系统** 包含一个合成多跳QA基准数据集（Table 1）和InfoQA框架，用于验证理论并展示多轮调用的优势。合成数据集在受控条件下（跳数h∈{1,2,3,4}，上下文长度L∈{0.5k, 1k, 2k, 4k, 8k, 10k}，总计7200个样本）生成，以精确测量信息需求变化。InfoQA框架（Figure 4）的设计直接针对理论瓶颈，其pipeline包含三个核心模块：

1.  **容量感知任务分解**：将原始多跳问题分解为一系列单跳子问题，从而将每一步的信息需求β降低到模型容量C可处理的范围内。
2.  **依赖显式工作流**：通过压缩后的查询（contracted query）在步骤间显式传递推理状态（即上一步的中间答案`\hat{Z}_k`），确保步骤间的依赖关系对齐，避免了依赖模型内部隐式记忆带来的不确定性。
3.  **迭代查询压缩**：在每一步，修剪过去的推理轨迹并重写当前查询，以保持提示长度可控，防止其随推理深度增长而超出容量限制。

实验结果表明，InfoQA在Qwen3-14B模型上2-4跳任务的平均F1达到0.86，显著优于最佳单次基线Self-Consistency（0.75）和Chain-of-Thought（0.73）（Table 2）。消融实验进一步证实了各模块的必要性：去除任务分解（w/o D.）后，平均F1降至0.65；去除轨迹修剪（w/o P.）后，平均F1降至0.78。在更具挑战性的4跳、8k上下文设置下，InfoQA在Qwen3-8B模型上的F1为0.67，而最佳单次基线仅为0.16（Table 5），这直观地展示了多轮调用范式在突破单次推理容量瓶颈方面的巨大潜力。理论曲线拟合（Figure 5, 6）显示，所有单次方法的经验准确率都与理论预测的准确率悬崖高度吻合，验证了理论框架的有效性。

## 核心模块与公式推导

本节聚焦论文的理论核心：单次推理准确率的Fano式上界及其推导，以及信息需求模型与误差累积的数学刻画。

### 2.1 信息瓶颈的数学基础

论文从信息论出发，将单次推理建模为：给定查询 $Q$ 和上下文 $C$，模型输出 $Y$，最终答案 $A$ 的准确率受两个基本不等式约束。

**条件Fano不等式** 将错误概率 $P_e$ 与答案的剩余不确定性联系起来：

$$
H(A | Q, C, Y) \leq h(P_e) + P_e \log(|\mathcal{A}| - 1)
$$

其中 $h(P_e) = -P_e \log P_e - (1-P_e) \log(1-P_e)$ 是二元熵函数，$|\mathcal{A}|$ 是答案空间大小。该不等式表明，即使观测到输出 $Y$，答案 $A$ 的条件熵仍受错误率约束——错误率越高，不确定性越大。

**输出熵界** 则限制了答案与输出之间的互信息：

$$
I(A; Y | Q, C) \leq H(Y)
$$

即模型输出 $Y$ 能携带的关于答案 $A$ 的信息量，受限于输出本身的熵 $H(Y)$。对于固定长度 $m$ 的token输出，$H(Y) \leq m \log |\mathcal{V}|$，其中 $|\mathcal{V}|$ 是词表大小；对于可变长度（最大 $m$），$H(Y) \leq \log((|\mathcal{V}|^{m+1} - 1)/(|\mathcal{V}| - 1))$。论文将输出熵的上界定义为模型的**输出容量** $C$。

### 2.2 Fano式准确率上界（Theorem 1）

结合上述两个不等式，论文推导出单次推理准确率的**Fano式上界**：

$$
h(\text{Acc}) + (1 - \text{Acc}) \log(|\mathcal{A}| - 1) \geq \beta - C
$$

其中：
- $\text{Acc} = 1 - P_e$ 是准确率；
- $\beta = H(A | Q, C)$ 是**任务信息需求**，即给定查询和上下文后答案的固有不确定性（以nats或bits为单位）；
- $C$ 是模型的**输出容量**，即输出熵的上界。

该不等式的核心含义：**最大可达准确率受信息需求与输出容量之差的约束**。当信息需求 $\beta$ 超过容量 $C$ 时，准确率必然下降。

### 2.3 准确率悬崖（Accuracy Cliff）

为得到更直观的表达式，论文推导了简化线性上界和均匀分布特例。

**线性准确率上界**：

$$
\text{Acc} \leq \min\left\{1, 1 - \frac{\beta - C - 1}{\log|\mathcal{A}|}\right\}
$$

**均匀分布特例**（所有答案近似等概率时）：

$$
\text{Acc} \leq \min\left\{1, \frac{C+1}{\beta}\right\}
$$

这一形式揭示了**准确率悬崖**现象：当 $\beta > C + 1$ 时，准确率上界按 $(C+1)/\beta$ 双曲线衰减（如 Figure 2 所示）。即一旦信息需求超过容量约1 nat，准确率急剧下降，而非缓慢退化。

### 3.1 信息需求模型

为将理论应用于多跳问答，论文将信息需求 $\beta$ 建模为跳数 $h$ 和上下文长度 $L$ 的函数：

$$
\beta(h, L) = \beta_0 + \alpha L \gamma^{h-1}
$$

其中：
- $\beta_0$ 是基础需求（与上下文无关的固定部分）；
- $\alpha$ 是上下文长度缩放因子；
- $\gamma$ 是**跳数膨胀因子**（$\gamma > 1$ 表示信息需求随跳数超线性增长）。

代入均匀分布准确率上界，得到**插件式准确率界**：

$$
\text{Acc}(h, L) \leq \min\left\{1, \frac{C+1}{\beta_0 + \alpha L \gamma^{h-1}}\right\}
$$

该模型的关键发现：跳数膨胀因子 $\gamma$ 主要由上下文中的干扰项（distractors）引起。实验表明，去除干扰项后 $\gamma \approx 1$，即信息需求的超线性增长主要源于噪声而非推理深度本身。

### 3.2 误差累积模型

对于多步推理，论文将第 $k$ 步的成功事件定义为：

$$
S_k \triangleq \{ \hat{Z}_k = Z_k \land \hat{Z}_k = \phi_k(\hat{Z}_{k-1}, Q, C) \}
$$

即预测正确且与前一状态一致。整体成功概率为各步条件成功概率的乘积：

$$
\Pr(\text{Succ}) = \prod_{k=1}^{K+1} p_k
$$

给定每步错误率 $\varepsilon$ 时，成功概率的下界为：

$$
\Pr(\text{Succ}) \geq (1-\varepsilon)^{K+1} \approx 1 - (K+1)\varepsilon
$$

这意味着**整体成功概率随跳数线性衰减**（如 Figure 3 所示）。即使每步错误率很低（如 $\varepsilon = 0.05$），4跳任务的整体成功率也会降至约 $0.95^5 \approx 0.77$。

### 核心参数拟合方法

论文通过最小化平均绝对误差（MAE）来拟合模型参数 $\theta = (\beta_0, \alpha, \gamma, C)$：

$$
\mathcal{L}(\alpha, \gamma, \beta_0, C) = \frac{1}{N} \sum_{(h, L)} \left| \widehat{\text{F1}}(h, L) - \text{F1}_{\text{emp}}(h, L) \right|
$$

其中 $\widehat{\text{F1}}(h, L) = \min\left(1, \frac{C+1}{\beta_0 + \alpha L \gamma^{h-1}}\right)$。拟合结果（Table 3, Table 4）显示：CoT和S-C通过增大有效容量 $C$（约131）和降低 $\gamma$（约2.08）来缓解准确率悬崖；而S-A因较大的基础需求 $\beta_0$ 抵消了高容量的优势。

## 实验与分析

### 主结果：Accuracy Cliff 的实证验证与 InfoQA 的突破

实验的核心发现是，所有单次推理方法（Direct Prompting, CoT, S-C, S-R, ReAct, P&S, S-A）在合成多跳QA基准上的表现均严格遵循理论推导的Fano式准确率上界。拟合结果（Table 3, Table 4）显示，经验F1分数与公式 $\widehat{\text{Acc}}(h, L) = \min\{1, (C+1)/(\beta_0 + \alpha L \gamma^{h-1})\}$ 的偏差极小（MAE < 0.05），证实了当信息需求β超过输出容量C时，准确率会如Figure 2所示发生断崖式下降（Accuracy Cliff）。例如，在Qwen3-14B上，当上下文长度L=8k且跳数h=4时，所有单次方法的F1均低于0.20，而理论预测的上界也在此区域急剧衰减。


![[assets/figures/papers/iclr26_0002_dPAcHrG4rl_A_Fano-Style_Accuracy_Upper_Bound_for_LLM_Single/figures/008_Table_3.jpg]]
*Table 3: Fitted parameters of the plug-in accuracy bound (MAE minimization) of Qwen3-14B. Larger C indicates higher effective single-pass capacity; smaller $\gamma$ indicates weaker hop inflation*

![[assets/figures/papers/iclr26_0002_dPAcHrG4rl_A_Fano-Style_Accuracy_Upper_Bound_for_LLM_Single/figures/009_Table_4.jpg]]
*Table 4: Fitted parameters of the plug-in accuracy bound (MAE minimization) of Qwen3-8B. Larger C indicates higher effective single-pass capacity; smaller γ indicates weaker hop inflation*

相比之下，本文提出的多轮调用框架InfoQA在Qwen3-14B上取得了2-4跳平均F1为0.86的成绩，显著优于最佳单次基线Self-Consistency (S-C)的0.75和Chain-of-Thought (CoT)的0.73（Table 2）。这一优势在更具挑战性的设置中更为突出：在Qwen3-8B上，4跳、8k上下文长度的场景下，InfoQA的F1达到0.67，而最佳单次基线仅为0.16（Table 5），性能差距高达0.51。这直接证明了通过容量感知的任务分解和迭代查询压缩，多轮调用范式能够有效规避单次推理的信息容量瓶颈。


![[assets/figures/papers/iclr26_0002_dPAcHrG4rl_A_Fano-Style_Accuracy_Upper_Bound_for_LLM_Single/figures/006_Table_2.jpg]]
*Table 2: Average F1 scores of Qwen3-14B across different reasoning depths and context lengths. We compare InfoQA with single-pass baselines: Chain-of-Thought (CoT), Self-Refine (S-R), Self-Consistency (S-C), ReAct, Plan-and-Solve (P&S), Self-Ask (S-A), and InfoQA with ablation: w/o Capacity-Aware Task Decomposition (D.) and w/o Pruning Past Reasoning Trace (P.)*

![[assets/figures/papers/iclr26_0002_dPAcHrG4rl_A_Fano-Style_Accuracy_Upper_Bound_for_LLM_Single/figures/010_Table_5.jpg]]
*Table 5: Qwen3-8B’s Average F1 scores across different reasoning depths and context lengths. We compare InfoQA with single-pass baselines: Chain-of-Thought (CoT), Self-Refine (S-R), Self-Consistency (S-C), ReAct, Plan-and-Solve (P&S), Self-Ask (S-A)*

### 消融实验：分解与修剪的关键作用

消融实验揭示了InfoQA两个核心组件的贡献。去除容量感知任务分解（w/o D.）后，InfoQA的平均F1从0.86骤降至0.65（Table 2）。这是因为w/o D.变体退化为单次推理，其信息需求β随跳数和上下文长度超线性增长，迅速越过Accuracy Cliff的临界点。去除推理轨迹修剪（w/o P.）后，F1降至0.78，表明保留完整的推理历史会导致提示长度膨胀，增加每步的信息需求并引入噪声干扰。这两个消融结果共同证实，InfoQA的成功源于同时降低了每步的信息需求（通过分解）并控制了累积的上下文噪声（通过修剪）。

### 失败模式与理论洞察

**单次方法的容量瓶颈机制**：拟合参数（Table 3, Table 4）揭示了不同单次方法失败的根本原因。CoT和S-C通过生成中间推理步骤，将有效输出容量C提升至约131（Qwen3-14B），并降低了跳数膨胀系数γ（约2.08），从而将Accuracy Cliff推后到更高的β区域。然而，它们的性能仍然受限于单次输出的总信息容量。Self-Ask (S-A)虽然也尝试分解，但其基础信息需求β₀较大（约160），抵消了高C（约178）带来的优势。Plan-and-Solve (P&S)同样面临高β₀（160）和高γ（2.49）的困境。这表明，单次推理中任何试图增加容量的策略都会不可避免地引入额外的信息需求，形成一种“容量-需求”的权衡困境。

**噪声是跳数膨胀的主要驱动因素**：一个关键的发现是，当从数据集中去除干扰项后，拟合的γ值趋近于1（Table 3, Table 4注释）。这意味着β随跳数h的指数增长主要由每跳引入的无关噪声（干扰项）驱动，而非推理深度本身。这解释了为何直接提示（Direct Prompting）的γ最高（约3.26），因为其输出必须包含所有中间信息；而CoT通过结构化输出降低了噪声的累积效应。

**误差累积的线性衰减**：理论分析（Figure 3）和实验共同表明，即使每步错误率ε很小，整体成功概率也会随跳数K线性衰减：$\Pr(\text{Succ}) \approx 1 - (K+1)\epsilon$。这解释了为何在4跳任务中，即使单步准确率较高，整体准确率也远低于1跳任务。InfoQA通过确保每步都是独立的、低信息需求的单跳问题，将每步错误率ε控制在极低水平，从而缓解了这一衰减。

**InfoQA的局限性**：作为概念验证，InfoQA的分解策略是预定义的（基于问题类型），缺乏自适应能力。当问题结构复杂或噪声模式超出预设范围时，其性能可能下降。此外，理论分析假设封闭书设置，未考虑模型利用外部知识的情况。合成基准数据集虽然可控，但可能无法完全反映真实世界多跳问答的噪声和复杂性。

### 补充图表

![[assets/figures/papers/iclr26_0002_dPAcHrG4rl_A_Fano-Style_Accuracy_Upper_Bound_for_LLM_Single/figures/005_Table_1.jpg]]
*Table 1: Statistics of our synthetic multi-hop QA benchmark*


## 方法谱系与知识库定位

本文的核心贡献并非提出一种全新的推理范式，而是从信息论角度揭示了现有单次推理范式的根本性瓶颈，并据此设计了一个概念验证性的多轮调用框架InfoQA。其方法谱系可被清晰地定位在“从单次调用到多轮分解”的范式转换中。

### 与基线方法的关系：从缓解症状到规避瓶颈

现有基线方法（CoT, S-C, ReAct, P&S等）本质上都是在单次推理的框架内优化，其作用机制可以被本文的信息需求模型`β(h, L) = β_0 + αL γ^(h-1)`和Fano式准确率上界`Acc ≤ min{1, (C+1)/β}`所解释。这些方法通过不同方式“缓解”Accuracy Cliff的症状，但无法规避其根本原因——信息需求β超过输出容量C。

- **CoT与S-C**：通过增加有效输出容量C和降低跳数膨胀系数γ来扩展可用区域。拟合参数（Table 3）显示，CoT和S-C的C值（约131）显著高于Direct Prompting，且γ值（约2.08）更低。这意味着它们通过中间推理步骤“编码”了更多信息，并抑制了噪声的复合效应。然而，当β因跳数和上下文长度增长而超过C+1时，其准确率仍会不可避免地崩溃。
- **Self-Ask (S-A)**：其设计意图（将问题分解为子问题）与InfoQA有表面相似性，但实现方式（在单次调用内完成）使其陷入一个矛盾：分解行为本身引入了巨大的基础信息需求代价（β₀很大），抵消了其通过子问题划分获得的容量优势。拟合结果（Table 3）证实了S-A具有高C但高β₀，导致其整体表现不如CoT和S-C。
- **Plan-and-Solve (P&S)与ReAct**：这些方法试图通过规划或行动来结构化推理，但依然受限于单次调用的输出容量。P&S的C值（约178）是所有单次方法中最高的，但其β₀（160）和γ（约2.49）也相应增大，表明其规划过程本身消耗了大量信息容量。

**核心洞察**：所有单次方法都在同一个“容量-需求”天平上调整，其性能上限由`(C+1)/β`决定。InfoQA的范式转换在于，它通过多轮调用，将原本在一个回合内完成的、信息需求为β的复杂任务，分解为K个信息需求约为β/K的单跳子任务。这使得每步的信息需求都远低于模型的单次容量C，从而从根本上规避了Accuracy Cliff。

### 适用边界与条件

InfoQA的优越性依赖于几个关键前提：

1.  **任务可分解性**：多跳问答任务必须能被“容量感知”地分解为一系列单跳子问题。对于内在耦合性极强、无法通过单跳子问题串联解决的推理任务（如某些需要全局综合的数学证明或反事实推理），InfoQA的分解策略可能失效。
2.  **显式状态传递的保真度**：InfoQA通过“迭代查询压缩”在步骤间传递推理状态。该机制的有效性依赖于压缩过程不丢失关键信息且不引入语义漂移。实验中的消融研究（Table 2）显示，去除轨迹修剪（w/o P.）后，F1从0.86降至0.78，证实了状态传递保真度的重要性。
3.  **噪声环境可控**：实验发现，去除干扰项后γ≈1，表明跳数膨胀主要由噪声引起。因此，在信息噪声（干扰项）极低或为零的场景下，单次推理的Accuracy Cliff效应会显著减弱，InfoQA相对于CoT/S-C的优势可能缩小。

### 局限与开放问题

本文的理论和实验设计存在明确局限，并指向若干开放问题：

- **分解策略的自适应性**：InfoQA的分解是预定义的（通过提示词实现），缺乏根据任务复杂度动态调整的能力。如何设计一个能自动评估子问题信息需求并决定分解粒度的自适应策略，是首要开放问题。
- **查询压缩的保真度**：迭代查询压缩是InfoQA的核心，但其压缩算法（修剪推理轨迹并重写）可能导致信息丢失或语义漂移。如何定量衡量压缩保真度，并设计更鲁棒的压缩方法（例如，基于关键信息提取而非简单修剪）是关键技术挑战。
- **理论假设的局限性**：理论分析基于“封闭书”假设，即模型仅能从提供的上下文中获取信息。在开放世界设定下，模型可以利用预训练知识作为外部信息源，从而改变信息需求β的计算方式。该理论能否扩展到开放书场景，需要进一步验证。
- **多轮调用的新限制**：InfoQA将信息瓶颈从单次调用的“容量-需求”问题，转化为多轮调用的“状态传递-误差累积”问题。虽然误差累积模型`Pr(Succ) ≥ (1-ε)^(K+1)`给出了一个下界，但多轮调用中信息如何跨调用累积、是否存在新的容量边界（如注意力跨轮次的衰减），以及如何优化调用次数与每步容量的权衡，都是尚未探索的开放问题。
- **拟合方法的过拟合风险**：论文使用网格搜索进行参数拟合（MAE最小化），这存在过拟合风险。虽然实验点与理论曲线吻合良好（Figure 5, 6），但模型的泛化能力，尤其是在未见过的(h, L)组合上的预测能力，需要更严格的验证（例如，使用留一法交叉验证）。

## 原文 PDF

PDF 文件：paperPDFs/ICLR_2026/A_Fano_Style_Accuracy_Upper_Bound_for_LLM_Single_Pass_Reasoning_in_Multi_Hop_QA.pdf

![[paperPDFs/ICLR_2026/A_Fano_Style_Accuracy_Upper_Bound_for_LLM_Single_Pass_Reasoning_in_Multi_Hop_QA.pdf]]
