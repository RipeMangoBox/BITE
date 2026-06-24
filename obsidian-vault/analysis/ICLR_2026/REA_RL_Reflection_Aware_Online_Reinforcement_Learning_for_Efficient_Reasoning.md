---
title: "REA-RL: Reflection-Aware Online Reinforcement Learning for Efficient Reasoning"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/REA_RL_Reflection_Aware_Online_Reinforcement_Learning_for_Efficient_Reasoning.pdf
openreview_forum_id: E6keG5QDct
aliases:
- RR
- REA-RL
tags:
- ICLR_2026
- topic/reinforcement_learning_planning_agents
- topic/reinforcement_learning_planning_agents/deep_rl
core_operator: "引入一个小型反射模型，在在线训练中对推理路径进行截断以移除过度思考部分，并设计基于反射关键词密度的反射奖励来惩罚非反思响应，从而在缩短响应长度的同时保护必要的反思能力。"
primary_logic: "通过将并行采样与顺序修订相结合，并利用反射奖励维持反思频率，REA-RL 可在不牺牲性能的前提下将推理成本降低36%，同时能根据问题难度自适应调整反思强度：对简单问题减少反思，对困难问题保留反思。"
claims:
- "REA-RL 在五项数学基准上平均将响应长度缩短36%，且准确率不下降。"
- "反射模型能够识别首次正确答案的位置并移除之后的过度思考token，在线生成更短的修订路径。"
- "反射奖励通过惩罚反射密度低于训练数据0.2分位数的响应，有效防止模型产生非反思性短回答。"
- "仅使用长度奖励会导致模型丧失反思能力，性能大幅下降，而加入反射奖励后性能显著恢复。"
---

# REA-RL: Reflection-Aware Online Reinforcement Learning for Efficient Reasoning

> [!tip] 核心洞察
> 通过将并行采样与顺序修订相结合，并利用反射奖励维持反思频率，REA-RL 可在不牺牲性能的前提下将推理成本降低36%，同时能根据问题难度自适应调整反思强度：对简单问题减少反思，对困难问题保留反思。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | REA-RL：面向高效推理的反射感知在线强化学习 |
| 英文题名 | REA-RL: Reflection-Aware Online Reinforcement Learning for Efficient Reasoning |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=E6keG5QDct); [GitHub](https://github.com/hexuandeng/REA-RL) |
| Topic | #topic/reinforcement_learning_planning_agents #topic/reinforcement_learning_planning_agents/deep_rl |
| Method | REA-RL |
| Dataset | 5 项数学基准 (平均), GSM8K, MATH500 |

> [!tip] 效果简介
> - 5 项数学基准 (平均) 上，准确率 为 82.13，对比 Original (R1-7B) 80.39，变化 +1.74。
> - 5 项数学基准 (平均) 上，Token 成本比值 (TR) 为 -36% (TR = 63.51)，对比 Original (TR = 100)，变化 -36%。
> - GSM8K 上，准确率 为 92.72，对比 GRPO RLen (85.97)，变化 +6.75。

## 概述

大型推理模型（LRMs）在复杂推理任务中展现出强大的能力，但普遍存在**冗余反思（过度思考）**问题：模型在推理过程中反复进行自我修正，产生大量对最终答案无贡献的token，导致推理成本急剧上升。直接引入长度奖励进行在线强化学习（RL）虽然能缩短响应，却会**彻底剥夺模型的反思能力**，使其在困难问题上性能大幅下降——这一“长度-反思”矛盾构成了本领域的核心瓶颈。

针对上述问题，本文提出 **REA-RL（Reflection-Aware Online Reinforcement Learning）**，一个反射感知的在线强化学习框架。其核心思想是：**在在线RL训练中，通过引入一个小型反射模型来识别并截断过度思考部分，同时设计基于反射关键词密度的奖励机制来维持必要的反思频率**，从而在缩短响应长度的同时保护模型的反思能力。

具体而言，REA-RL 包含两个关键创新：

1. **顺序修订机制**：在并行采样生成多条推理路径后，利用蒸馏自32B模型的小型反射模型（7B）识别首次正确答案出现的位置，截断后续的过度思考token，再由策略模型补全生成更短的修订路径。原始路径与修订路径共同参与训练，为策略优化提供更高效的监督信号。

2. **反射奖励设计**：引入基于反射token密度（如“wait”、“but”等反思关键词的出现频率）的奖励项。当某条响应的反射密度低于训练数据0.2分位数时施加惩罚，有效阻止模型退化为非反思性的短回答，从而在长度压缩与反思保留之间取得平衡。

在方法定位上，REA-RL 区别于纯离线修订方法（如 **SFT** 和 **RPO**）、基于提示跳过推理的方法（如 **NoThink**）以及仅依赖长度奖励的在线RL方法（如基于 **Kimi K1.5** 的 **GRPO RLen**）。它通过将并行采样与顺序修订相结合，在在线RL框架内同时优化准确性和效率，并能根据问题难度自适应调整反思强度：对简单问题减少反思，对困难问题保留反思。

主要实验结果如下：

- 在五项数学基准（GSM8K、MATH500、Gaokao23、AMC23、AIME24）上，REA-RL 在8k token预算下将平均响应长度**缩短36%**（TR = 63.51 vs Original TR = 100），且准确率不下降。
- 在16k token预算下，组合方法平均准确率达到**82.13%**，较原始R1-7B模型（80.39%）提升1.74个百分点。
- 消融实验证实：仅使用长度奖励会导致模型丧失反思能力、准确率暴跌；加入反射奖励后性能显著恢复，验证了反射奖励在维持推理能力方面的关键作用。

REA-RL 当前在蒸馏得到的7B LRM上验证有效，尚未在从头预训练的更大规模模型上测试。此外，基于LLM的过度思考检测无法完全消除所有冗余token，顺序修订也引入了约10%的额外训练时间开销。

## 背景与动机

大型推理模型（LRMs）通过在生成过程中插入显式的“反思”（reflection）步骤，显著提升了在复杂数学推理等任务上的表现。然而，这种反思行为常常失控，导致模型在已得出正确答案后仍反复进行自我验证和修正——即**过度思考（overthinking）**。过度思考产生大量冗余 token，大幅推高了推理成本，却未带来相应的性能增益。

现有的缓解方案主要分为两类。**离线修订方法**（如 **RPO**，Pang et al., 2024）在训练前对数据进行截断和重写，但修订后的数据分布与模型在线生成分布存在偏差，限制了效率提升的上限。**在线强化学习方法**（如基于 Kimi K1.5 的长度奖励 RL，Du et al., 2025）通过在 GRPO 框架中加入长度奖励来鼓励生成更短的响应，但这一激励机制存在严重副作用：模型倾向于完全放弃反思行为，生成“非反思性”的短回答，导致在困难问题上的准确率大幅下降（Figure 1 中间示例）。

上述困境揭示了一个核心矛盾：**单纯追求缩短响应长度会摧毁模型的反思能力，而保留反思能力又难以有效控制推理成本**。如何在缩短响应长度的同时，保护必要的反思行为，成为高效推理训练中亟待解决的关键瓶颈。

## 核心创新

REA-RL 的核心创新在于将**反射感知**引入在线强化学习，通过两个互补的机制——**顺序修订**与**反射奖励**——同时解决大型推理模型（LRMs）的过度思考问题和非反思性短回答问题。其关键设计围绕以下四个 changed slots 展开：

### 1. 反射模型驱动的顺序修订

传统在线 RL（如 **GRPO**，Shao et al., 2024）仅使用并行采样的原始完整推理路径进行训练，无法主动消除冗余反思。REA-RL 引入一个小型反射模型 $\mathbf{M}_{\text{Reflect}}$，在单步内识别首次正确答案出现的位置，截断后续的过度思考 token，并由策略模型补全生成修订响应（Equation 2）。这一设计将并行采样与顺序修订相结合，使训练数据同时包含原始路径和更短的非过度思考路径，为策略优化提供了正向的压缩信号。

反射模型的构建采用了知识蒸馏策略：先将 32B 模型的两步修订能力通过监督微调（SFT）蒸馏至 Qwen2.5-7B-Instruct，使其能以单步方式完成截断，确保在线训练的效率（§4.2）。

### 2. 改进的长度奖励

原始 Kimi K1.5 长度奖励（**GRPO RLen**，Du et al., 2025）对错误响应仍给予 $\min(0.5, \lambda)$ 的奖励（Equation 1），这可能导致模型为追求长度奖励而牺牲准确性。REA-RL 将其改进为：错误响应的长度奖励直接设为 0，仅对正确响应给予缩放奖励 $\lambda$（Equation 4）。这一改进加速了响应缩短过程，同时避免了对错误短回答的奖励偏好。

### 3. 反射奖励

仅使用长度奖励的在线 RL 会使模型彻底丧失反思能力——模型倾向于生成极短的非反思性回答，导致在困难问题上性能大幅下降（Figure 1 中间示例）。REA-RL 创新性地引入基于反射关键词密度的反射奖励 $R_{\text{Reflect}}$（Equation 3）：

$$R_{\text{Reflect}}(s_i) = \min\left(0, \frac{D_i}{D_{0.2}} - 1\right), \quad D_i = \frac{N_{\text{Reflect}}}{N_{\text{Token}}}$$

该奖励仅在响应内反射 token 密度 $D_i$ 低于训练数据 0.2 分位数时施加惩罚，有效阻止模型滑向非反思行为，同时不过度奖励冗余反思。消融实验（Table 8）表明，反射奖励将平均准确率提升 4.26 个百分点，尽管 token 成本因此上升 23.26%，但这是维持反思能力所必需的代价。

### 4. 训练数据的双重扩展

REA-RL 将原始并行采样响应 $\{s_1, \dots, s_G\}$ 与经反射模型截断、策略模型补全后的修订响应 $\{s_1^r, \dots, s_G^r\}$ 共同作为训练数据（Equation 2）。这一数据扩展策略不仅增加了训练样本量，更重要的是为 RL 优化提供了分布对齐的短路径正例，引导策略模型学习在保持必要反思的前提下压缩推理长度。

### 创新间的协同效应

反射模型与反射奖励针对不同维度：反射模型更有效地缩短响应长度，反射奖励则主要贡献于准确率提升。两者结合可在不牺牲性能的前提下实现 36% 的推理成本压缩（Table 2, 8k budget），且能根据问题难度自适应调整反思强度——对简单问题减少反思，对困难问题保留反思。

## 整体框架

![[assets/figures/papers/paper_list_l13_https_openreview_net_forum_id_E6keG5QDct/figures/003_Figure_2.jpg]]
*Figure 2: Workflow of REA-RL. We first parallel sample G paths as in GRPO. Then, the reflection model identifies and truncates overthinking tokens (red ones with ×), retaining the preceding yellow segments. After that, the policy model finishes the truncated paths, generating revised tokens (blue ones with ✓), and yielding G revised paths. Finally, both the G original and G revised paths are used for training. Cases are in Appendix B.1. In addition to the naive accuracy reward $\mathtt { R } _ { \mathrm { A c c } }$ and length reward $\mathrm { R } _ { \mathrm { L e n } }$ . , we refine the length reward $\scriptstyle ( \mathrm { R } _ { \mathrm { R L e n } }$ ) and introduce a new reflection reward ( ${ \m$...

REA-RL 的核心设计围绕一个在线强化学习管线展开，该管线在 GRPO（Shao et al., 2024）的基础上引入两个关键组件——**反射模型**与**反射奖励**——以同时解决大型推理模型中的过度思考与反思能力丧失问题。其整体工作流程如图 2 所示，由五个顺序模块构成：

1. **并行采样**：策略模型针对给定问题并行生成 G 个推理路径，作为原始响应。
2. **反射模型截断**：一个小型反射模型识别每条路径中首次出现正确答案的位置，并截断此后的过度思考 token，仅保留有效推理前缀。
3. **策略模型补全**：策略模型在截断路径的基础上继续生成最终答案，形成修订响应。
4. **奖励计算**：对原始响应和修订响应分别计算准确性奖励、改进的长度奖励以及反射奖励。
5. **策略优化**：基于 GRPO，利用两组响应的归一化优势梯度更新策略模型。

上述流程的核心因果机制在于：反射模型通过“截断-补全”操作在线生成更短的非过度思考路径，为策略模型提供正向示例；而反射奖励则通过惩罚反射关键词密度过低的响应，防止模型在长度奖励的驱动下退化为完全不反思的短回答。两者分别作用于“缩短长度”和“保护反思”两个维度，协同实现了在不牺牲性能的前提下将推理成本降低 36%。

**反射模型的设计**：为避免两阶段修订（先用大模型检测、再补全）带来的高昂开销，REA-RL 将 Qwen-32B 的两步修订能力通过 SFT 蒸馏至 Qwen2.5-7B-Instruct，使其在单步内即可完成截断。截断策略支持三种强度——Normal（在首个正确答案处截断）、Weak（在第二个正确答案处截断）和 Strong（在截断概率超过 0.25 前截断）——允许根据问题难度自适应调整。

**奖励设计的改进**：原始 Kimi K1.5 长度奖励对错误响应仍给予最多 0.5 的奖励，这可能导致模型为追求奖励而生成无意义的短回答。REA-RL 将其改进为仅对正确响应给予长度奖励（错误响应奖励为 0），并新增反射奖励，当响应内反射 token 密度低于训练数据的 0.2 分位数时施加惩罚。消融实验表明，改进的长度奖励加速了响应缩短，而反射奖励将平均准确率提升 4.26，是维持性能的关键。

**数据流与训练**：在每一轮在线 RL 中，原始响应与修订响应共同构成训练集，使策略模型既能从原始路径中学习推理能力，又能从修订路径中学习高效推理模式。训练在 3 块 NVIDIA A800 80G GPU 上耗时约 120 小时，顺序修订因 vllm 推理并行度下降引入约 10% 的额外时间开销。

## 核心模块与公式推导

REA-RL 的核心架构由五个串联模块构成，围绕“并行采样—反射截断—策略补全—奖励计算—策略优化”的闭环展开。以下逐一说明各模块的功能及其关键公式。

### 并行采样

与 GRPO 一致，策略模型在每轮训练中对同一问题并行生成 $G$ 条推理路径，记为原始响应集合 $\{s_1, \dots, s_G\}$。这些路径构成在线 RL 的基础数据池（§4.1）。

### 反射模型截断

引入一个小型反射模型 $M_{\text{Reflect}}$，其作用是在线识别每条原始响应中“首次出现正确答案”的位置，并截断该位置之后的过度思考 token（Figure 2 中红色标记部分），仅保留前缀片段。该模型通过从 32B 模型的两步修订能力蒸馏至 Qwen2.5-7B-Instruct 得到，以单步推理实现高效截断（§4.2）。

### 策略模型补全

在反射模型截断后的前缀基础上，策略模型 $M_{\text{Policy}}$ 以强制生成最终答案的方式完成补全，形成修订响应 $s_i^r$。原始响应与修订响应共同构成训练数据：

$$
\{ s _ { 1 } , \dots , s _ { G } , s _ { 1 } ^ { r } , \dots , s _ { G } ^ { r } \} \xrightarrow { \mathbf { o n l i n e ~ R L } } \mathbf { M } _ { \mathrm { P o l i c y } } , \mathbf { w h e r e } s _ { i } ^ { r } = \mathbf { M } _ { \mathrm { P o l i c y } } \big ( \mathbf { M } _ { \mathrm { R e f l e c t } } ( s _ { i } ) \big )
$$

这一设计使策略模型能够同时学习原始推理路径和经过截断的简洁路径，引导优化方向向更高效的推理靠拢（§4.2）。

### 奖励计算

REA-RL 的奖励函数由三部分组成：准确性奖励 $R_{\text{Acc}}$、改进的长度奖励 $R_{\text{RLen}}$，以及新引入的反射奖励 $R_{\text{Reflect}}$。

**改进的长度奖励**（§4.3）对原始 Kimi K1.5 长度奖励做了关键修正——将错误响应的长度奖励设为零，仅对正确响应给予线性缩放的长度奖励：

$$
\mathsf { R } _ { \mathrm { R L e n } } ( s _ { i } ) = \left\{ \begin{array} { l l } { \lambda } & { \mathrm { ~ i f ~ } s _ { i } \mathrm { ~ i s ~ c o r r e c t } } \\ { 0 } & { \mathrm { ~ i f ~ } s _ { i } \mathrm { ~ i s ~ i n c o r r e c t } } \end{array} \right. , \mathrm { w h e r e } \lambda = 1 - \frac { \mathrm { l e n } ( s _ { i } ) - \mathrm { m i n . l e n } } { \mathrm { m a x . l e n - m i n . l e n } }
$$

这一修正消除了对错误短响应的隐式奖励，加速了正确响应的长度压缩。

**反射奖励**（§4.3）通过监控响应中反射关键词（如“wait”、“but”）的密度来防止模型退化为非反思性短回答。定义反射密度 $D_i = N_{\text{Reflect}} / N_{\text{Token}}$，当某条响应的反射密度低于训练数据 0.2 分位数时施加惩罚：

$$
\mathsf { R } _ { \mathsf { R e f l e c t } } ( s _ { i } ) = \operatorname* { m i n } ( 0 , \frac { D _ { i } } { D _ { 0 . 2 } } - 1 )
$$

该奖励仅惩罚反射密度最低的 20% 响应，从而在缩短整体长度的同时维持必要的反思频率。消融实验表明，反射奖励将平均准确率提升 4.26 点，是防止性能崩溃的关键组件（Table 8）。

### 策略优化

基于 GRPO 框架，利用原始响应和修订响应的归一化优势梯度共同更新策略模型参数。组合方法在五项数学基准上平均将响应长度缩短 36%（TR = 63.51），同时准确率不降反升（Table 2）。

> **注意**：反射奖励的惩罚分位数超参数（$D_{0.1}$、$D_{0.2}$、$D_{0.4}$）对准确率影响较小，主要调节响应长度（Table 8），表明该奖励的核心作用在于阻止非反思行为而非直接提升推理质量。

## 实验与分析

### 核心瓶颈与实验动机

大型推理模型（LRMs）在复杂数学任务中普遍存在**过度思考（overthinking）**现象——模型在已得出正确答案后仍进行大量冗余反思，导致推理成本急剧膨胀。直接引入基于长度的奖励（如 Kimi K1.5 的 $R_{Len}$）虽能缩短响应，却会使模型彻底丧失反思能力，在困难问题上性能暴跌。REA-RL 的实验设计围绕一个核心权衡展开：**如何在压缩推理长度的同时，保护必要的反思行为**。

### 主要结果

**Table 2** 汇总了 REA-RL 及其各组件在五项数学基准（GSM8K、MATH500、Gaokao23、AMC23、AIME24）上的表现，核心结论如下：

![[assets/figures/papers/paper_list_l13_https_openreview_net_forum_id_E6keG5QDct/figures/004_Table_2.jpg]]
*Table 2: Main results of our proposed methods. Most abbreviations align with Table 1. Baseline definitions are in \ S 5 . 1 . \ $\mathrm { \stackrel { . . } { G R P O } { R _ { L e n } } { M _ { R e f l e c t } } } ^ { \prime }$ , represents the addition of the reflection model, “GRPO $\mathrm { R _ { R L e n + R e f l e c t } } ^ { \prime }$ represents the addition of the reward optimization, and $\mathrm { \mathrm { \ddot { \tau } G R P O ~ R } _ { R L e n + R e f l e c t } ~ M _ { R e f l e c t } } , \mathrm { \mathrm { \ } }$ represents the combination of both optimizations. “Budget” is the max tokens allowed per question

![[assets/figures/papers/paper_list_l13_https_openreview_net_forum_id_E6keG5QDct/figures/008_Figure_3.jpg]]
*Figure 3: Changes in accuracy and generation length during training on five test sets on average. The x-axis represents the training steps. The left plot shows the average accuracy, and the right plot shows the average token consumption per answer. Abbreviations are aligned with Table 2*

![[assets/figures/papers/paper_list_l13_https_openreview_net_forum_id_E6keG5QDct/figures/013_Table_8.jpg]]
*Table 8: Results of the ablation study. The table presents two sets of experiments using $\mathtt { R } _ { \mathtt { L e n } }$ and $\mathtt { R } _ { \mathtt { R L e n } }$ to demonstrate the effectiveness of our length reward optimization, as well as an ablation study on the hyperparameters of the reflection reward. “w/ $D _ { 0 . 1 }$ \ " and “w/ $D _ { 0 . 4 } ^ { }$ \ ' are defined in Equation 3, representing the use of the 0.1 and 0.4 quantiles of the reflection density for the reflection reward, respectively. Other abbreviations are defined in Table 2

- **仅用准确性奖励的 GRPO** 相比原始 R1-7B 模型无显著性能提升，说明单纯扩大在线采样规模不足以解决过度思考问题。
- **引入长度奖励的 GRPO $R_{Len}$** 大幅压缩了响应长度（TR 降至 57.23），但平均准确率从 80.39 暴跌至 76.88，验证了长度奖励会抑制反思能力、损害困难任务表现的假设（Figure 1 中间示例）。
- **组合方法 GRPO $R_{RLen}$+Reflect $M_{Reflect}$** 在 8k token 预算下实现了 **36% 的响应长度缩减**（TR=63.51），同时平均准确率保持 80.39 不下降；在 16k 预算下准确率进一步提升至 **82.13**（+1.74），证明反射模型与反射奖励的协同作用能够同时优化效率与性能。

![[assets/figures/papers/paper_list_l13_https_openreview_net_forum_id_E6keG5QDct/figures/001_Figure_1.jpg]]
*Figure 1: Overthinking and non-reflective cases from GSM8k. The left shows the output of DeepSeek-R1-Distill-Qwen-7B (R1-7B), which reflects eight times before finishing generation. The middle presents the output after online RL training using length rewards, which only spends 103 tokens in “think” part and no reflection, where an error occurs (underlined). The right shows the output of our method, which uses a similar budget to R1-7B in reasoning but only performs a single reflection*

值得注意的是，离线方法 RPO 在 8k 预算下表现接近原始模型，但在 16k 预算下于两个高难度数据集上显著退化，表明离线训练难以充分覆盖模型在线生成时的分布偏移。

### 组件贡献分析

**Table 3** 和 **Table 4** 进一步揭示了反射模型与反射奖励的分工：

![[assets/figures/papers/paper_list_l13_https_openreview_net_forum_id_E6keG5QDct/figures/006_Table_3.jpg]]
*Table 3: Results of our proposed reflection model. “7B Revise” and “32B Revise” refer to the two-step revision method introduced in §3, using Qwen-7B and Qwen-32B without training. $\mathbf { \hat { \omega } } _ { \mathbf { M } _ { \mathrm { R e f l e c t } } } ^ { \mathbf { \alpha } _ { 6 6 } }$ , uses our 7B reflection model with one-step revision. “Fixed Trunc” denotes a fixed truncation strategy with the same ratio as our method. Truncation strengths are defined in §5.3. Table 4: Reflection density of REA-RL and baselines. “Reflect” represents the average number of tokens between each reflective token, i.e., a smaller value indicates more frequent reflection

- **反射模型（$M_{Reflect}$）** 主要负责压缩响应长度。GRPO $R_{Len}$ $M_{Reflect}$ 的 TR 为 57.23，而加入反射奖励后 TR 上升至 71.77，说明反射模型是缩短响应的主要驱动力。其工作机制是识别首次正确答案出现的位置并截断后续过度思考 token（Figure 2），生成更短的修订路径参与训练。
- **反射奖励（$R_{Reflect}$）** 主要负责保护性能。Table 8 的消融显示，添加反射奖励使平均准确率提升 **4.26 个百分点**，但代价是 TR 上升 23.26——这正是其设计意图：通过惩罚反射密度低于训练数据 0.2 分位数的响应（Equation 3），阻止模型退化为不反思的短回答。

**Figure 3** 的训练曲线直观展示了这一动态：仅使用长度奖励的方法生成长度快速下降但准确率同步恶化；组合方法在保持准确率平稳甚至上升的同时，实现了长度的渐进式压缩。

### 反射模型策略消融

**Table 3** 对比了不同截断策略的效果：

- **Normal 策略**（在首次正确答案处截断）在效率与性能间取得最佳平衡。
- **Weak 策略**（在第二次正确答案处截断）保留更多上下文，TR 更高（78.52）但准确率略低。
- **Strong 策略**（在截断概率超过 0.25 前截断）过于激进，性能下降明显。

此外，**Table 9** 对比了启发式截断（固定比例截断）与学习到的反射模型，后者在所有数据集上均显著优于启发式方法，证明基于 LLM 的过度思考检测（§3.1 的分块检测+Qwen-32B 验证流程）是必要且有效的。

### 反射奖励超参数敏感性

**Table 8** 的反射奖励消融显示，惩罚分位数 $D_{0.1}$、$D_{0.2}$、$D_{0.4}$ 对准确率影响较小，主要调节响应长度——分位数越高（惩罚越严格），响应越长。这表明反射奖励的核心作用在于**设定一个反射频率的下界**，而非精细控制反射强度，超参数选择具有一定的鲁棒性。

### 改进长度奖励的有效性

**Table 8** 对比了原始 $R_{Len}$（Kimi K1.5 风格，错误响应仍可获得 min(0.5, λ) 的奖励）与改进的 $R_{RLen}$（错误响应奖励为 0，Equation 4）。结果显示 $R_{RLen}$ 在加速响应缩短的同时保持或提升了准确率，验证了移除对错误响应的长度偏好有助于引导模型更高效地学习。

### 失败模式与局限性

1. **非反思性短回答风险**：Figure 1 中间示例展示，仅用长度奖励训练的模型在 GSM8K 问题上仅用 103 个 token 完成“思考”部分，完全跳过反思，导致错误答案。反射奖励正是针对此失败模式设计。
2. **过度思考残留**：Table 10 的过度思考分析表明，即使训练后，使用 32B 模型进行修订仍能进一步移除部分 token，说明基于 7B 反射模型的检测无法完全消除所有冗余。
3. **训练开销**：顺序修订在 vllm 推理中因并行度下降引入约 **10% 的额外训练时间**，完整训练需 120 小时（3× NVIDIA A800 80G）。
4. **规模泛化未验证**：当前实验仅在蒸馏的 7B 和 1.5B LRM 上进行，未在从头预训练的更大模型上测试。

### 泛化能力

**Table 5-7** 展示了方法在通用 QA 和小模型上的扩展结果：
- 在 MMLU-Pro 上，蒸馏自 Qwen2.5-7B-Instruct 的反射模型在 Weak/Normal/Strong 策略下均实现了显著的 token 压缩（Table 5）。
- 在 R1-1.5B 上，GRPO+$M_{Reflect}$ 同样实现了效率提升（Table 7），表明反射模型截断策略对小模型同样有效。
- 通用 QA 策略训练（Table 6）显示，引入反射模型在 MMLU、MMLU-Pro、SuperGPQA 上均带来正向收益，验证了方法的跨领域迁移能力。

## 方法谱系与知识库定位

### 核心问题与解决路径

大型推理模型（LRMs）在复杂数学任务中普遍存在**过度思考（overthinking）**现象——模型在“思考”阶段反复进行自我反思，产生大量冗余 token，导致推理成本急剧膨胀。更棘手的是，若直接采用基于长度的奖励（length reward）进行在线强化学习来压缩响应，模型会彻底丧失反思能力，在难题上的性能大幅下降。REA-RL 的因果调控核心在于**引入一个外部反射模型对推理路径进行截断，并设计反射奖励维持必要的反思频率**，从而在缩短响应长度的同时保护反思能力。

### 与基线方法的关系

**GRPO**（Shao et al., 2024）是 REA-RL 的基础在线强化学习框架，仅使用准确性奖励。REA-RL 在此基础上引入了三个关键改动：

1. **改进的长度奖励**：**Kimi K1.5 长度奖励**（Du et al., 2025）对错误响应仍给予 `min(0.5, λ)` 的长度奖励（Equation 1），这会给短错误响应带来不合理的正向激励。REA-RL 将错误响应的长度奖励设为 0（Equation 4），仅对正确响应给予线性缩放的长度奖励，从而加速响应缩短（Table 8 消融实验证实该改进能加速缩短且不损害准确率）。

2. **反射奖励**：现有方法均未引入此机制。REA-RL 基于响应中反思关键词（如 “wait”、“but”）的密度 `D_i` 设计奖励函数，当 `D_i` 低于训练数据 0.2 分位数时施加惩罚（Equation 3）。该奖励的作用是**阻止模型产生非反思性短回答**——Figure 1 中间示例展示了仅用长度奖励时模型完全放弃反思、直接输出错误答案的情况。Table 8 消融显示，添加反射奖励后平均准确率提升 4.26，但 token 成本比值上升 23.26，表明其在维持性能方面的关键作用。

3. **反射模型驱动的路径修订**：**SFT**（Zhang et al., 2023）、**RPO**（Pang et al., 2024）等离线方法无法在训练中动态调整推理路径。**NoThink**（Ma et al., 2025）通过提示跳过推理，**ShorterBetter**（Yi et al., 2025）和 **DAST**（Shen et al., 2025）分别使用最短正确响应或问题难度估计长度预算，但这些方法缺乏对反思内容本身的识别与保留。REA-RL 将 32B 模型的二步修订能力蒸馏到 Qwen2.5-7B-Instruct，形成小型反射模型 M_Reflect，在单步内识别首次正确答案位置并截断后续过度思考 token，再由策略模型补全生成修订路径（Figure 2）。该设计使原始和修订响应共同参与 GRPO 训练（Equation 2），实现了**并行采样与顺序修订的协同**。

### 适用边界与局限

**已验证的适用场景**：
- 基于 DeepSeek-R1-Distill-Qwen-7B 蒸馏模型的数学推理任务（GSM8K、MATH500、Gaokao23、AMC23、AIME24），在 8k 和 16k token 预算下均有效
- 通用 QA 任务（MMLU、MMLU-Pro、SuperGPQA）在 R1-1.5B 模型上的初步验证（Table 6、Table 7）

**明确局限**：
1. **模型规模验证不足**：当前仅在蒸馏得到的 7B LRM 上验证，未在从头预训练的更大 LRM 上进行测试。该方法能否扩展到更大规模模型并保持相同效果，仍是开放问题。
2. **过度思考检测不完美**：基于 LLM 的检测无法完全确保消除所有冗余反思，可能留下部分无意义 token。Table 9 的启发式截断对比实验表明，学习型截断模型显著优于固定比例截断，但仍存在改进空间。
3. **训练效率损失**：顺序修订在 vllm 推理中因并行度下降而引入约 10% 的额外训练时间开销（3 块 NVIDIA A800 80G GPU 上训练需 120 小时）。

### 开放问题

1. 该方法能否扩展到从头训练的更大 LRM（如 32B、70B 级别）并保持相同的效率-性能平衡？
2. 过度思考检测能否进一步自动化，或与更精确的反思边界识别方法（如基于 attention 或内部状态的方法）结合？
3. 在更长的训练过程中，反射奖励与长度奖励之间是否存在更深层的相互作用——例如，反射奖励的分位数阈值是否需要随训练进程动态调整？
4. 如何进一步降低顺序修订的额外计算开销（当前约 10%），使其在大规模部署中更具优势？
5. 反射关键词密度作为反思的代理指标是否足够鲁棒——是否存在模型学会“表面反思”（使用关键词但不产生实质推理）的风险？

## 原文 PDF

![[paperPDFs/ICLR_2026/REA_RL_Reflection_Aware_Online_Reinforcement_Learning_for_Efficient_Reasoning.pdf]]
