---
title: "Activation Steering with a Feedback Controller"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/Activation_Steering_with_a_Feedback_Controller.pdf
project_link: null
code_link: https://github.com/dungnvnus/pid-steering
aliases:
- PIDPS
- ASFC
tags:
- ICLR_2026
- topic/other_unclear
- topic/other_unclear/general
core_operator: "引入比例-积分-微分（PID）控制器，通过积分项消除稳态误差，微分项抑制过冲，实现闭环控制。"
primary_logic: "将激活引导视为动态系统的反馈控制问题，利用PID控制器对层间误差进行闭环调节，从而系统性地改善引导的稳定性和准确性。"
claims:
- "常用激活引导方法（ActAdd, DirAblate, Mean-AcT）等价于比例（P）控制器，理论分析表明其存在稳态误差。"
- "PID引导在多个LLM家族和基准上一致超越现有方法，毒性降低最高8.2倍，越狱攻击成功率（ASR）最高提升1.59个百分点。"
- "Jailbreak Attack (Qwen2.5‑14B) 上 ASR (%) = 94.85"
- "Toxicity Mitigation (Gemma2‑2B) 上 Seq.CLS Tox. (%) = 0.51"
---

# Activation Steering with a Feedback Controller

> [!tip] 核心洞察
> 将激活引导视为动态系统的反馈控制问题，利用PID控制器对层间误差进行闭环调节，从而系统性地改善引导的稳定性和准确性。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 基于反馈控制器的激活引导 |
| 英文题名 | Activation Steering with a Feedback Controller |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=vzkEX2SwFD) · [GitHub](https://github.com/dungnvnus/pid-steering) |
| Topic | #topic/other_unclear #topic/other_unclear/general |
| Method | Proportional-Integral-Derivative (PID) Steering |
| Dataset | Jailbreak Attack (Qwen2.5‑14B), Toxicity Mitigation (Gemma2‑2B), Jailbreak Attack (Llama3.1‑8B) |

> [!tip] 效果简介
> - Jailbreak Attack (Qwen2.5‑14B) 上，ASR (%) 为 94.85，对比 93.26 (DIM)，变化 +1.59。
> - Toxicity Mitigation (Gemma2‑2B) 上，Seq.CLS Tox. (%) 为 0.51，对比 Original (exact value not given)，变化 ~8.2× reduction。
> - Jailbreak Attack (Llama3.1‑8B) 上，ASR (%) 为 92.65，对比 90.38 (DIM)，变化 +2.27。

## 概要

现有激活引导方法（如ActAdd、DirAblate、Mean‑AcT）缺乏理论上的性能保证，本质上等价于比例（P）控制器，因而存在稳态误差与振荡等缺陷。本文的核心思路是将激活引导重新形式化为动态系统的反馈控制问题，并引入**比例‑积分‑微分（PID）控制器**：以层间差分均值向量为误差信号，通过比例项即时响应偏差、积分项累积消除稳态误差、微分项抑制过冲，实现对激活空间中目标行为的闭环调节。

这一框架（**PID Steering**）在方法上与现有引导接口兼容，但系统性解决了传统比例控制的固有问题。实验表明，PID 引导在多个LLM家族上一致优于同类方法：毒性缓解最高可达约8.2倍的降低，越狱攻击成功率（ASR）最高提升1.59个百分点（例如Qwen2.5‑14B上达到94.85%），同时模型通用基准性能波动较小，未出现系统性公平性下降。整体结果证实，将控制理论中的PID思想引入激活引导，能以较低成本获得更稳定、更精确的行为控制。



大语言模型的行为解释与可控生成是当前的研究热点，其核心思路之一是通过**激活引导（activation steering）**操控模型内部表示，从而改变输出属性（如减少有害性、提升真实性、注入风格）。现有工作如 ActAdd、DirAblate、Mean‑AcT 等已展现出实用价值，但它们普遍缺乏理论层面的性能保证。

本文的核心发现是：这些主流方法在控制论视角下均可被统一理解为**比例（P）控制器**。以 ActAdd 为例，其引导函数为  
$$ \rho_{\mathrm{steer}}(\pmb{x}(k), \pmb{r}(k)) = \pmb{x}(k) + \alpha \pmb{r}(k), $$  
仅将引导向量按固定增益 $\alpha$ 叠加到当前层激活上；DirAblate 则通过正交投影移除表征方向，同样可归约为比例控制律。理论分析表明，单纯的 P 控制存在固有缺陷：**稳态误差无法消除**，且高增益时容易引发**振荡或过冲**，这从根本上限制了引导的稳定性和效果。

鉴于此，论文提出将激活引导重新表述为动态系统的**反馈控制问题**，并引入**比例‑积分‑微分（PID）控制器**。其引导向量形式为  
$$ \pmb{u}(k) = K_p \pmb{r}(k) + K_i \sum_{j=0}^{k-1} \pmb{r}(j) + K_d (\pmb{r}(k) - \pmb{r}(k-1)), $$  
其中 $\pmb{r}(k)$ 是由对比数据集计算得到的逐层误差信号。积分项负责累积历史误差，从而**消除稳态误差**；微分项抑制误差趋势，有效**抑制过冲**。这一闭环控制框架无需改变原有引导接口，即可兼容 ActAdd、DirAblate 等现有方法。

通过将控制理论的严格性引入激活引导，PID Steering 旨在解决当前方法"有方法无理论、有效果但欠稳定"的瓶颈，为 LLM 内部行为的可靠操控提供原理性基础。



## 核心方法与创新机理

现有激活引导（activation steering）方法在缺乏形式化性能保证的前提下直接对模型内部表示施加干预，其设计与经典反馈控制中**比例（P）控制器**等价，因而存在稳态误差和响应振荡等固有缺陷。这项工作将激活引导重新定义为一个**动态系统的反馈控制问题**，并据此提出了**比例‑积分‑微分（PID）引导**——一种在每一层利用完整 PID 控制律计算引导向量的框架。理论分析指出，积分项可消除比例控制无法克服的稳态偏移，而微分项则通过预测误差变化抑制积分累积引起的过冲，从而系统性地提升引导过程的稳定性与准确性。

**与 P 控制器的等价性**  
ActAdd、DirAblate 和 Mean‑AcT 等主流方法均以"对比数据集间激活差值的固定缩放"作为引导向量，其数学形式等价于纯比例控制 $\pmb{u}(k)=K_p\pmb{r}(k)$。作者证明，这类 P 控制器虽然能保证输入‑状态稳定性（ISS），但由于异构扰动 $\pmb{w}(k)$ 的存在，误差动态 $\bar{e}(k+1)=\bar{A}(k)\bar{e}(k)-\bar{A}(k)\pmb{u}(k)+\pmb{w}(k)$ 在稳态下不能归零（Proposition 1），这直接限制了引导的精度。

**PID 引导向量定义**  
为解决上述问题，PID 引导将逐层计算的控制向量扩展为比例、积分、微分三项的线性组合：

$$\pmb{u}(k) = K_p \pmb{r}(k) + K_i \sum_{j=0}^{k-1} \pmb{r}(j) + K_d \bigl(\pmb{r}(k) - \pmb{r}(k-1)\bigr)$$

（Definition 1, Eqn. 18）。其中 $\pmb{r}(k)$ 为目标‑源对比数据集的差分均值向量（即误差信号），$K_p$, $K_i$, $K_d$ 分别为可调增益。该设计首次在激活引导中引入**积分历史累积**（$K_i\sum\pmb{r}(j)$）以消除稳态偏差，以及**微分预测项**（$K_d\Delta\pmb{r}(k)$）以降低超调风险，构成了完整的闭环控制。

**方法无关的集成方式**  
PID 引导保持与已有引导接口的兼容性：控制向量 $\pmb{u}(k)$ 可直接替代原始 $\alpha\pmb{r}(k)$ 注入 ActAdd 的加法操作或 DirAblate 的正交投影操作，亦可嵌入 Mean‑AcT 的序贯均值传输流程（Section 3.2.1 "Methodological Agnosticism"）。因此，创新集中在**误差信号的反馈处理**，而非独立提出新的引导向量产生器或干预函数。

**经验验证与关键效果**  
在毒性缓解任务中，结合 Mean‑AcT 的 PID‑AcT 将毒性分数降低约 **8.2 倍**（Gemma2‑2B 的 Seq.CLS Tox. 降至 0.51%，Table 1），并在 MMLU 等通用能力上保持极小下降。在越狱攻击防护上，PID Steering 的 ASR 最高达到 94.85%（Qwen2.5‑14B），比原始 DIM 基线提升 1.59 个百分点（Table 2），且在全模型全方法对比中始终保持最优（Table 3）。消融实验显示，增大积分增益 $K_i$ 可持续降低有害性（Llamaguard3 与 LLM‑Judge 评分），但会引发过冲；而同时引入微分增益 $K_d$ 则有效抑制超调并恢复性能（Figure 6a, 该结论此处置信度较高但本质为单组实验观察）。这些结果验证了 PID 各组件的作用，并证实闭环调节相比简单 P 控制具有实质优势。

**局限与待验证环节**  
目前 $K_p, K_i, K_d$ 的最优配置仍依赖网格搜索或经验调参，缺乏基于理论（如 LMI）的自动选取方法；极端参数组合下亦可能存在稳定裕度不足的风险。此外，积分增益过大引起的过冲虽可通过微分项缓解，但其动力学分析只在标量化投影下得到部分证明，一般情形下的过冲幅度上界还需进一步严格化（Proposition 4 提供了第一过冲的界限，但未有一般情况的完整证明）。这些点均提示，PID 引导的理论完备性仍有待深入。



![[assets/figures/papers/iclr26_0006_vzkEX2SwFD_Activation_Steering_with_a_Feedback_Controller/figures/002_Figure_2.jpg]]
*Figure 2: PID Steering: To compute the steering vector u(k): a PID controller is applied at every layer $f ^ { ( k ) } ( \cdot$ ) , using the diff-in-means between 2 contrastive data $x _ { s p }$ ( k ) and x(k) as the error signal e(k)*

PID Steering 将 LLM 的逐层推理视为一个动态系统，并把激活引导重新定义为该系统的反馈控制问题。整个框架的核心流程：在每一层，以**差分均值向量**为误差信号，用 **PID 控制器**计算引导向量，再通过已有的注入接口（如 ActAdd、DirAblate、Mean‑AcT）将该向量施加到激活上，从而闭环调整模型的内部表示。

**输入与误差信号**  
框架的输入是一组对比数据集（例如"有害回答"与"无害回答"）。在推理过程中，对每个 token 位置分别采集目标域与源域在该层的激活，逐层计算均值差向量 $\mathbf{r}(k)$（即误差信号），该信号刻画了当前激活分布与期望分布之间的偏差。在 Mean‑AcT 等顺序式中继方法中，这一计算本身就是在被引导后的激活上进行的，因此天然构成闭环反馈。

**PID 控制器**  
与现有方法将 $\mathbf{r}(k)$ 直接作为引导向量（等价于比例控制）不同，PID Steering 使用完整的 PID 控制律（公式 (18)）：

$$
\mathbf{u}(k) = K_p \mathbf{r}(k) + K_i \sum_{j=0}^{k-1} \mathbf{r}(j) + K_d \bigl(\mathbf{r}(k) - \mathbf{r}(k-1)\bigr)
$$

- **比例项** $K_p \mathbf{r}(k)$ 提供对当前偏差的即时响应；  
- **积分项** $K_i \sum \mathbf{r}(j)$ 累积历史误差，消除比例控制下无法修正的稳态偏差；  
- **微分项** $K_d \Delta\mathbf{r}(k)$ 根据误差变化率提前抑制过冲，提升收敛过程的稳定性。

**引导应用与输出流**  
计算得到的引导向量 $\mathbf{u}(k)$ 通过选定接口注入到当前层的激活中。例如在 ActAdd 兼容模式下为 $\mathbf{x}(k) + \alpha\mathbf{u}(k)$，DirAblate 则将其用于正交投影操作。注入后的激活继续向后传播，并在下一层重复"计算误差→PID 引导→注入"的闭环。整个流程在 Figure 2 中有示意性描绘：每层 $f^{(k)}$ 都嵌入一个 PID 控制器，以对比数据集间的差分均值为误差，生成当前层的引导向量。

**与现有方法的关系**  
ActAdd、DirAblate、Mean‑AcT 本质上只使用了比例项（P 控制）。理论分析表明，P 控制在存在持续扰动时必然留有稳态误差，且无法主动预测误差变化趋势。PID Steering 通过积分项消除该稳态误差，并通过微分项抑制由强积分导致的振荡，从而在不改变底层注入机制的前提下从控制层面系统性地提升引导质量。这意味着该框架具有方法无关性：任何基于差分均值向量的引导方案均可嵌入 PID 控制器进行增强。



本文方法将激活引导重新表述为反馈控制问题，其框架可分解为三个核心模块，并通过离散 PID 控制律进行闭环调节。

**误差信号计算模块**  
对于每一层 $k$，利用两个对比数据集（目标集 $\mathcal{D}_{\text{target}}$ 与源集 $\mathcal{D}_{\text{source}}$）计算差分均值向量作为控制误差。形式上，非序列化方法直接计算第 $i$ 个样本的逐层误差向量：

$$
\pmb{r}_i(k) = \pmb{\mu}_{i,\mathrm{target}}(k) - \pmb{\mu}_{i,\mathrm{source}}(k)
$$

其中 $\pmb{\mu}_{i,\mathrm{target}}(k)$、$\pmb{\mu}_{i,\mathrm{source}}(k)$ 分别为样本在目标集和源集上第 $k$ 层的平均激活。聚合后得到层误差信号 $\pmb{r}(k)$，作为后续 PID 控制器的输入。这一误差本质上是激活空间中的"偏差"，引导需求即将其缩小至零。

**PID 控制器模块**  
在此模块中，PID 控制器根据当前层误差、历史误差累积以及误差变化率，计算该层的引导向量。离散形式的 PID 引导向量由 Definition 1 给出：

$$
\pmb{u}(k) = K_p \pmb{r}(k) + K_i \sum_{j=0}^{k-1} \pmb{r}(j) + K_d \bigl(\pmb{r}(k) - \pmb{r}(k-1)\bigr)
$$

变量含义：
- $K_p, K_i, K_d$ —— 比例、积分、微分增益，控制各分量的响应强度；
- $\pmb{r}(k)$ —— 第 $k$ 层的误差信号；
- $\displaystyle\sum_{j=0}^{k-1} \pmb{r}(j)$ —— 历史误差累积（积分项），用于消除稳态误差；
- $\pmb{r}(k)-\pmb{r}(k-1)$ —— 误差变化率（微分项），用于预测误差走势、抑制过冲。

该方程将传统激活引导的"比例-加和"推广至完整的 PID 律，使引导向量动态地响应层间误差的演化。

**引导应用模块**  
计算得到的 PID 引导向量 $\pmb{u}(k)$ 可插入任意激活引导接口，保持对已有方法的兼容性。例如，ActAdd 形式的注入为 $\pmb{x}(k) \leftarrow \pmb{x}(k) + \alpha \pmb{u}(k)$，DirAblate 则通过正交投影移除 $\pmb{u}(k)$ 方向分量。整体框架见图 2 的示意：在每一层 $f^{(k)}(\cdot)$ 上独立运行 PID 控制器，以差分均值为误差信号逐层施加干预。

**闭环误差动态**  
为指导增益设计并分析稳定性，论文将受控激活的平均误差演化刻画为以下动态方程（Proposition 2、Eqn. 20）：

$$
\bar{\pmb{e}}(k+1) = \bar{\pmb{A}}(k)\,\bar{\pmb{e}}(k) - \bar{\pmb{A}}(k)\,\pmb{u}(k) + \pmb{w}(k)
$$

其中 $\bar{\pmb{e}}(k)$ 为平均误差向量，$\bar{\pmb{A}}(k)$ 为层间变换的线性化矩阵，$\pmb{w}(k)$ 表示由样本异构性引入的扰动。该方程显式展示了 PID 控制项 $\pmb{u}(k)$ 如何干预误差传播，并从理论上保证积分项可消除稳态偏差、微分项可抑制过冲。



## 实验与关键发现

PID 引导在两个核心安全任务上一致优于现有方法：毒性缓解和越狱攻击成功率（ASR）。如表 1 所示，在 Gemma2‑2B 上当使用 PID‑AcT 时，顺序分类毒性降至 0.51%，相比原始模型降幅约 8.2 倍，同时困惑度与 MMLU 保持良好，说明安全性的提升并未以显著的能力损失为代价。类似地，在 Llama3‑8B 上 PID‑AcT 同样取得了最强的毒性压制，并通过 Llamaguard3 与 LLM‑Judge 双评估器得到验证。在越狱攻击场景（表 2），PID 在 Qwen2.5‑14B 上达到 94.85% 的 ASR，较 DIM 的 93.26% 高出 1.59 个百分点；在 Llama3.1‑8B 上，PID 的 92.65% 相比 DIM 的 90.38% 提升 2.27 个百分点。全模型全方法对比（表 3）进一步确认 PID 在绝大多数模型上均取得最高 ASR，且通用基准（MMLU、HellaSwag、WinoGrande 等）的波动始终很小，说明 PID 框架具有跨模型和任务的稳定性。

![[assets/figures/papers/iclr26_0006_vzkEX2SwFD_Activation_Steering_with_a_Feedback_Controller/figures/005_Table_1.jpg]]
*Table 1: Toxicity mitigation results for Gemma-2B and Llama-8B, averaged over 10 runs. Lower is better for toxicity and perplexity; higher is better for MMLU. Bold = best, underline = second-best within each model.1*

![[assets/figures/papers/iclr26_0006_vzkEX2SwFD_Activation_Steering_with_a_Feedback_Controller/figures/006_Table_2.jpg]]
*Table 2: Comparison of Original, DIM, ITI, RePE, and PID across models on ASR and general benchmarks. Bold = best, underline = second-best within each model (ASR column). Refer to Tab. 3 for results on all tested models*

![[assets/figures/papers/iclr26_0006_vzkEX2SwFD_Activation_Steering_with_a_Feedback_Controller/figures/016_Figure_6.jpg]]
*Figure 6: Ablation Study on $\left( K _ { p } , K _ { i } , K _ { d } \right$) parameters. We sweep through different values of $K _ { p } , K _ { i } , K _ { d }$ and report (a) Llamaguard3 (ASR in Tab. 2) and Llmjudge (evaluated using QVQ-72B-Preview) metrics for Gemma-2-9b-it, and (b) CLS Tox. and 0-shot Tox. metrics for Gemma2-2B

![[assets/figures/papers/iclr26_0006_vzkEX2SwFD_Activation_Steering_with_a_Feedback_Controller/figures/021_Table_3.jpg]]
*Table 3: Full comparison of Original, DIM, ITI, RePE, and PID across models on ASR and general benchmarks on all tested models. Bold = best, underline = second-best within each model (ASR column)*

PID 引导的增益来自控制律中的积分项与微分项。消融实验（图 6a）表明，在越狱任务上增大积分增益 $K_i$ 可持续降低 Llamaguard3 和 LLM‑Judge 评分，验证积分项有效消除比例控制固有的稳态误差。然而，过大的 $K_i$ 会引发过冲，导致性能恶化；此时加入微分增益 $K_d$ 可以明显抑制过冲，使攻击成功率恢复至稳定水平。这一现象与标量误差仿真（图 3）一致——PI 控制器消除了稳态误差但伴随大幅过冲，引入微分项后收敛更快且过冲被显著压制。在风格控制任务中（图 5），PID‑AcT 在中等引导强度下（0.4–0.8）的零样本生成强度与 CLIPScore 均优于 Mean‑AcT，进一步证明闭环控制在连续指导信号下的优势。

![[assets/figures/papers/iclr26_0006_vzkEX2SwFD_Activation_Steering_with_a_Feedback_Controller/figures/004_Figure_3.jpg]]
*Figure 3: Scalar errors across time step of randomly initialized model after applying P, PI, and PID controller*

尽管 PID 引导效果显著，当前最优增益 $(K_p, K_i, K_d)$ 的选取依赖网格搜索或经验调参，缺乏理论上的最优设计方法（如 LMI 计算）。在极端参数组合下，系统稳定裕度可能不足，且积分增益过大时仍需微分项配合以避免过冲。这些问题指向未来工作需要自动、理论最优的增益选择策略，以确保 PID 引导在大规模部署时的鲁棒性。



## 定位与知识库关联

**与基线的控制‑理论对应关系**

现有激活引导方法 ActAdd、DirAblate 和 Mean‑AcT 可统一解释为**比例（P）控制器**的特定实例（Section 2.2, 2.3）。它们都将某一层计算得到的差分均值向量直接作为引导信号，本质上只是对当前误差做出瞬时比例的响应：

- ActAdd & Mean‑AcT：$\rho_{\mathrm{steer}}(\mathbf{x}(k), \mathbf{r}(k)) = \mathbf{x}(k) + \alpha \,\mathbf{r}(k)$，即 $\mathbf{u}(k) = \alpha \,\mathbf{r}(k)$（纯 P 控制）。
- DirAblate：$\rho_{\mathrm{steer}}(\mathbf{x}(k), \mathbf{r}(k)) = \mathbf{x}(k) - \mathbf{r}(k)\mathbf{r}(k)^{\top}\mathbf{x}(k)$，本质上也是通过一个缩放后的 $\mathbf{r}(k)$ 进行正交投影，仍然属于比例作用。

这些方法缺乏积分修正项，**理论分析**（Proposition 1）证明，当存在层间异构扰动 $\mathbf{w}(k)$ 时，P 控制只能保证输入‑状态稳定（ISS），但会残留不可消除的**稳态误差**；同时，仅依赖比例项也容易在模型层间出现振荡。

**PID Steering 的改进之处**

PID Steering 将激活引导视为动态系统的反馈控制问题，引入完整的**比例‑积分‑微分（PID）控制器**（Definition 1）：
$$\mathbf{u}(k) = K_p \mathbf{r}(k) + K_i \sum_{j=0}^{k-1} \mathbf{r}(j) + K_d (\mathbf{r}(k) - \mathbf{r}(k-1)).$$
- **积分项**（$K_i\sum \mathbf{r}(j)$）持续累积历史误差，理论上可完全消除 P 控制无法摆脱的稳态偏置（Proposition 3，Theorem 1）。
- **微分项**（$K_d(\mathbf{r}(k)-\mathbf{r}(k-1))$）对误差变化趋势做出提前反应，有效**抑制过冲**（Theorem 2：$A_0^{\mathrm{PID}}\le A_0^{\mathrm{PI}}$），避免积分项带来的大振幅振荡。

该方法具有**方法不可知性**：PID 计算出的 $\mathbf{u}(k)$ 可直接替换 ActAdd、DirAblate 或 Mean‑AcT 中的原始引导向量，不影响原有的向量应用接口（Section 3.2.1）。因此它既是对现有 P 控制方法的升级，又保留了与各类激活操纵范式的兼容性。

**相较于其他引导向量生成策略**

除 P 控制外，常见的引导向量**生成策略**还包括 DIM、ITI 和 RePE（Table 2 & Table 3）。这些方法本身并不蕴含闭环控制结构，只能提供静态的特征方向。当把它们产生的向量嵌入 PID 框架时，误差信号 $\mathbf{r}(k)$（或 $\mathbf{e}(k)$）的来源发生改变，而 PID 的调控逻辑依然适用。实验表明，PID Steering 在越狱攻击成功率（ASR）上始终优于 DIM，且跨模型一致（Qwen2.5‑14B：94.85 vs 93.26；Llama3.1‑8B：92.65 vs 90.38），在毒性缓解任务上也实现了 8.2× 的降低倍率（Table 1），这验证了闭环控制结构比单纯更换向量源有更显著的增益。

**适用边界与条件**

PID Steering 的有效性依赖两个前提：
1. 目标概念可以通过对**对比数据集**（toxic vs harmless、jailbreak vs safe 等）提取明确的误差方向。如果缺乏清晰的"应控制的方向"或对比数据集质量差，控制误差 $\mathbf{r}(k)$ 的尺度与方向将失去意义。
2. 增益参数 $\{K_p, K_i, K_d\}$ 需要适当标定。实验中的增益均通过网格搜索确定，**目前尚无理论最优选择机制**（未来工作指向 LMI 等数值方法）。

方法在**安全性控制**（越狱攻击、毒性缓解）和**图像风格控制**（cyberpunk、steampunk）上表现出色，但在通用语言任务（如 MMLU、HellaSwag）上仅作为辅助评估，并未展现出系统性的性能退化。尚未在以下场景中进行严格验证：需要逐 token 动态调节的概念（如长文本一致性）、多概念联合操控，以及模型规模极小时的稳定性（最小仅测到 2B 参数）。因此尚不清楚 PID 的控制假设（如 ISS‑Lyapunov 函数存在性）在更广泛架构上是否持续满足。

**已知局限**

- **增益调参依赖经验搜索**：$K_p, K_i, K_d$ 的选择目前靠网格搜索，缺乏解析或自适应的确定方法，给实际部署带来额外成本。
- **过度积分可能引起过冲**：即使积分项能消除稳态误差，过大的 $K_i$ 仍会导致明显的首次过冲（Proposition 4，Fig. 6a）；微分项虽能抑制，但极端参数组合下始终存在稳定裕度不足的风险。
- **积分饱和与数值问题未处理**：连续累积的 $\sum\mathbf{r}(j)$ 在多层层数下可能引发数值膨胀或饱和，PID Steering 未引入抗饱和（anti‑windup）机制。
- **动态增益适配未探索**：所有实验均采用固定增益，对于输入序列变化剧烈的场景（如对抗攻击动态适应），可能不够灵活。

**开放问题与后续方向**

1. **自动增益整定**：能否利用控制理论工具（如 LMI、遗传算法）根据模型结构和任务自动选择 $K_p, K_i, K_d$，以消除人工调参？
2. **状态反馈 PID 的完整形式**：当前仅使用 $\mathbf{r}(k)$ 作为误差，实际的状态反馈 PID 应使用 $\mathbf{x}(k)$ 与参考状态的偏差；如何在多头注意力空间中定义参考状态并导出完整 PID，仍待显式构建。
3. **逐 token 动态控制**：目前引导向量以层为单位施加，能否推广到 token 级别的细粒度动态增益，以应对每一步语义控制的差异？
4. **多概念协同与解耦**：PID 框架如何同时调节多个正交概念方向，并避免积分项之间的相互干扰，仍是一个开放的设计空间。



## 原文 PDF

PDF 文件：paperPDFs/ICLR_2026/Activation_Steering_with_a_Feedback_Controller.pdf

![[paperPDFs/ICLR_2026/Activation_Steering_with_a_Feedback_Controller.pdf]]
