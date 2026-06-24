---
title: "A2D: Any-Order, Any-Step Safety Alignment for Diffusion Language Models"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/A2D_Any_Order_Any_Step_Safety_Alignment_for_Diffusion_Language_Models.pdf
aliases:
- AAOASD
- A2D
tags:
- ICLR_2026
- topic/safety_alignment_fairness_privacy
- topic/safety_alignment_fairness_privacy/fairness_equity_justice_and_safety
core_operator: "在训练时，将有害样本中被屏蔽的令牌监督为输出[EOS]（而非原始令牌），同时在安全样本中保持重构，从而在模型内部建立\"遇到有害内容即终止\"的令牌级拒绝机制。"
primary_logic: "将[EOS]作为通用的拒绝令牌，在任意解码位置、任意解码步骤出现有害跨度时立即终止生成，实现了真正的深度对齐，支持实时安全监控与早期拒绝。"
claims:
- "A2D将DIJA攻击成功率从超过80%降至接近零（LLaDA-8B-Instruct上1.3%，Dream-v0-Instruct-7B上0.0%）。"
- "A2D在XSTest（类不安全提示的良性样本集）上取得0%假阳性，避免过度拒绝。"
- "早期拒绝机制利用首步最左屏蔽位置的[EOS]概率，最高实现19.3×的安全终止加速。"
- "安全基准（Zeroshot, PAIR, ReNeLLM, Prefilling, DIJA） 上 平均有害性攻击成功率（ASR）↓ = LLaDA: 6.8, LLaDA-1.5: 9.1, Dream: 2.8"
---

# A2D: Any-Order, Any-Step Safety Alignment for Diffusion Language Models

> [!tip] 核心洞察
> 将[EOS]作为通用的拒绝令牌，在任意解码位置、任意解码步骤出现有害跨度时立即终止生成，实现了真正的深度对齐，支持实时安全监控与早期拒绝。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | A2D：针对扩散语言模型的任意顺序、任意步骤安全对齐 |
| 英文题名 | A2D: Any-Order, Any-Step Safety Alignment for Diffusion Language Models |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=URTnuyQJI1); [Project](https://ai-isl.github.io/A2D) |
| Topic | #topic/safety_alignment_fairness_privacy #topic/safety_alignment_fairness_privacy/fairness_equity_justice_and_safety |
| Method | A2D (Any-Order, Any-Step Defense) |
| Dataset | 安全基准（Zeroshot, PAIR, ReNeLLM, Prefilling, DIJA）, DIJA 攻击 |

> [!tip] 效果简介
> - 安全基准（Zeroshot, PAIR, ReNeLLM, Prefilling, DIJA） 上，平均有害性攻击成功率（ASR）↓ 为 LLaDA: 6.8, LLaDA-1.5: 9.1, Dream: 2.8，对比 LLaDA: VRPO 21.6, RT 51.5; Dream: VRPO 22.7, RT 36.4，变化 相对最佳基线平均降低 60% 以上。
> - DIJA 攻击 上，ASR ↓ 为 LLaDA: 1.3%, LLaDA-1.5: 3.5%, Dream: 0.0%，对比 LLaDA: original 82.9%; Dream: original 84.4%，变化 从80%以上降至接近零。

## 概述

扩散语言模型（dLLM）的任意顺序生成能力虽然提升了文本生成质量，却引入了一个根本性的安全瓶颈：有害内容可能出现在序列的任意位置，而现有响应级安全对齐方法（如拒绝训练、VRPO）仅对初始令牌施加有效约束，其安全信号随解码步数增加迅速衰减——本文称之为"浅层对齐"。这一缺陷使得填充式攻击（如DIJA）可在解码后期轻易绕过模型的拒绝机制，将攻击成功率推升至80%以上。

本工作提出 **A2D**（Any-Order, Any-Step Defense），一种面向扩散语言模型的令牌级安全对齐方法。其核心思路是将通用的终止令牌 `[EOS]` 作为拒绝信号：在训练时，对于有害样本中被屏蔽的令牌，模型被监督输出 `[EOS]` 而非原始内容；对于安全样本则保持正常重构。这一简单的监督信号变换在模型内部建立了"遇到有害跨度即终止"的令牌级拒绝机制。同时，训练中采用均匀屏蔽比率采样，确保拒绝能力覆盖从早期到后期的全部解码阶段。

以该机制为基础，A2D 在两大类关键指标上都取得了领先结果：

- **防御有效性**：在 Zeroshot、PAIR、ReNeLLM、Prefilling、DIJA 五种攻击下，A2D 将三款指令微调 dLLM 的平均有害性攻击成功率（ASR）大幅压低：LLaDA 降至 6.8%，LLaDA‑1.5 降至 9.1%，Dream 降至 2.8%，相较于最佳基线平均降低 60% 以上。针对最具挑战性的 DIJA 填充攻击，A2D 将 ASR 从 80% 以上削减至接近零（LLaDA‑8B‑Instruct 上 1.3%，Dream‑v0‑Instruct‑7B 上 0.0%）。
- **过度拒绝控制**：在由类不安全提示构成的良性基准 XSTest 上，A2D 取得 0% 的假阳性率，避免了对正常请求的误拒。
- **推理效率增益**：利用首步最左屏蔽位置的 `[EOS]` 概率作为早期拒绝信号，A2D 最高实现 **19.3×** 的安全终止加速；当阈值设为 0.9 时即可获得 6× 加速，而过度拒绝率仅为 1.6%。

这些结果表明，将安全信号下沉到令牌级，并在训练中覆盖任意解码位置与步骤，是解决扩散语言模型"浅层对齐"问题的简洁且高效路径。

## 背景与动机

扩散语言模型（diffusion language models, dLLMs）通过迭代式屏蔽与去噪进行文本生成，其核心机制允许模型在任意位置、以任意顺序解码令牌。这一"任意顺序生成"特性赋予了dLLMs在推理灵活性上的优势，但同时也引入了一个独特的安全脆弱性：有害内容可以在生成过程的任何位置、任何步骤自然浮现，而无需遵循自回归模型那样的严格从左到右因果约束。

现有安全对齐方法普遍采用**响应级（response-level）对齐**策略，即在完整响应的维度上监督模型输出拒绝模板或安全回复。代表性方法包括拒绝训练（Refusal Training, RT）、监督式微调（Supervised Fine-Tuning, SFT）以及基于变分偏好优化的VRPO等。这些方法的核心瓶颈在于：它们仅在响应的起始令牌处施加较强的安全信号，而随着解码步数的推进，安全信号迅速衰减。这种现象被称为**浅层对齐（shallow alignment）**——模型在前几个令牌学会了"拒绝"的表面模式，但在序列中后段的令牌预测分布上，对齐效应几乎消失。利用这一缺陷，DIJA（Diffusion Jailbreak Attack）等模板攻击可在解码后期轻松绕过模型的拒绝机制，将原始超过80%的攻击成功率施加于经过响应级对齐的模型之上（LLaDA-8B-Instruct上82.9%，Dream-v0-Instruct-7B上84.4%）。

更深层的因果视角揭示了这一漏洞的实质：在任意顺序生成范式下，有害内容并不必然从序列开头递进展开，它可能出现在中间或末尾的被屏蔽位置，而此时响应级对齐所提供的安全信号已不足以抑制有害令牌的生成。这意味着，仅靠"让模型在开头拒绝"的机制无法应对**任意位置、任意步骤**的安全威胁。

A2D的动机正是针对这一根本性缺口。本文的核心洞察在于：与其在响应级别教模型"说什么"，不如在令牌级别教模型"何时停止"——即，**将[EOS]令牌转化为通用的拒绝信号**。一旦模型在任意解码位置、任意解码步骤中检测到有害片段的形成趋势，便立即输出[EOS]终止生成。这种**令牌级对齐**机制直接在模型内部的逐令牌预测分布层面对齐安全行为，有望实现真正意义上的**深度对齐（deep alignment）**：无论解码顺序、屏蔽比率或攻击模板如何变化，对齐信号在生成全程保持有效。进而，在推理阶段还可利用[EOS]概率实现**早期拒绝**——当首步最左屏蔽位置的[EOS]概率超过阈值时即终止生成，从而实现最高19.3×的安全终止加速，同时避免对良性提示的过度拒绝。

## 核心创新

A2D 的核心创新在于将安全对齐从**响应级**下沉到**令牌级**，通过直接替换有害片段中被屏蔽令牌的监督信号为 `[EOS]`，在扩散语言模型内部建立起"遭遇有害内容即终止"的任意位置、任意步骤拒绝机制。这解决了现有响应级对齐（RT、SFT、VRPO）仅能在完整响应层面强化拒绝，而在部分解码状态下安全信号迅速衰减的**浅层对齐瓶颈**——该瓶颈使得 DIJA 等模板攻击在解码后期轻易绕过拒绝（攻击成功率原始可达 80% 以上）。

### 相对基线的核心改变点（Changed Slots）

1. **有害数据上屏蔽令牌的训练目标**：基线方法（RT、SFT、VRPO）要么要求模型重建原始令牌，要么在完整响应层面施加拒绝约束。A2D 将训练目标切换为：当样本来自有害集 $\mathcal{D}_{\text{harm}}$ 时，所有被屏蔽位置 $j$ 的监督信号强制设为 `[EOS]`（而非原始令牌）：
   $$y_j^* = [\mathrm{EOS}] \quad \text{对所有 } m_j = 1 \text{ 若 }(x,y) \in \mathcal{D}_{\mathrm{harm}}$$
   这等同于在模型的条件预测分布 $q_{\theta}(x^i \mid \mathbf{x}_{\lambda})$ 中，建立从部分有害上下文到终止令牌的直接映射，从而将 **`[EOS]` 变成通用的拒绝令牌**。该机制不依赖解码顺序，也不受生成已进行到哪一步的限制，任何位置出现有害跨度都将触发终止。

2. **屏蔽比率采样策略**：基线通常使用固定或仅覆盖部分解码阶段的屏蔽比率。A2D 改为从均匀分布采样 $\lambda \sim U(\epsilon, 1)$，并结合时间步 $t$ 进行线性插值：
   $$\lambda = (1 - \epsilon)t + \epsilon$$
   这一策略强制模型在训练中**经历从极早期（$\lambda$ 小）到接近完成（$\lambda$ 大）的所有解码阶段**，确保在任意步骤都能稳定输出 `[EOS]`，从而实现对 Prefilling 类攻击（在任意步骤注入有害前缀）的深度防御。这是 A2D 在 DIJA 攻击下将成功率从 80% 以上降至接近零（LLaDA-8B-Instruct 上 1.3%，Dream-v0-Instruct-7B 上 0.0%）的直接因果干预。

### 深层对齐与实时拒绝的涌现

上述两个改变使模型在解码全程的每令牌概率分布与基础模型产生持续的高 KL 散度，即所谓**深层对齐**（Figure 4），彻底避免了响应级对齐的浅层衰减效应。更重要的是，训练后模型自然获得了实时安全监控能力：首步最左屏蔽位置的 `[EOS]` 概率可作为在线有害性指标，设置阈值即可实现**早期拒绝**，在仅引入 1.6% 过度拒绝的条件下达到 6× 安全终止加速，若进一步放宽阈值则可获得最高 19.3× 加速。同时，A2D 在 XSTest（模拟不安全提示的良性样本集）上获得 0% 假阳性，证明其避免了过度拒绝。

这些结果综合表明，A2D 通过**仅在训练目标层面对若干屏蔽令牌进行 `[EOS]` 替换，并配合全覆盖的屏蔽比率分布**，以极低的实现复杂度（与 RT、SFT 相当的训练成本，远低于 VRPO）从根本上消除了扩散语言模型因任意顺序生成带来的安全漏洞。

## 整体框架

![[assets/figures/papers/iclr26_0005_URTnuyQJI1_A2D_Any-Order_Any-Step_Safety_Alignment_for_Diff/figures/002_Figure_2.jpg]]
*Figure 2: Overview of A2D for aligning dLLMs. Response-level methods supervise refusals only at the level of full responses, while A2D applies token-level alignment by replacing harmful spans with [EOS] tokens, enabling the model to reject unsafe content under any-order and at any-step. A2D prevents template-based attacks from producing harmful outputs, whereas response-level alignment fails under the same setting*

A2D 的核心 pipeline 围绕**令牌级安全监督**展开，直接应对扩散语言模型"浅层对齐"的结构性瓶颈：响应级对齐仅在生成起始阶段有效，安全信号沿解码步深迅速衰减，使 DIJA 等填充类攻击在生成后期轻易绕过拒绝。A2D 将 [EOS] 作为**通用的拒绝令牌**，通过在训练中重写有害片段的监督信号，把"遇到有害内容→立即终止"内化为模型的令牌级行为，从而在任意解码顺序、任意解码步骤下均能触发终止。

### 训练数据与监督信号构建

训练数据被划分为两类集合，分别承担不同的安全目标：

- **有害集（Harmful Set）**：由有害提示与对应的不安全响应组成。对于其中被屏蔽的位置，监督目标不再重构原始有害令牌，而是统一设置为 [EOS]。这意味着模型被强制学习：只要上下文指向有害内容，屏蔽位置就应当输出终止令牌。
- **保留集（Retain Set）**：包含安全提示–安全响应对，以及有害提示–安全响应对。被屏蔽位置的监督目标保持为原始令牌，以维持正常生成能力和指令跟随行为，避免过度拒绝。

这种双集合设计将[EOS]转化为一个**令牌级安全分类器**：在部分可观测的上下文下，模型隐式地学习近似有害性似然 $p_\theta([\mathrm{EOS}] \mid X_{\mathrm{ctx}}) \approx q_{\mathrm{clf}}(\mathrm{harmful} \mid X_{\mathrm{ctx}})$，从而在任意屏蔽位置产生实时安全判断。

### 屏蔽比率采样与任意步骤健壮性

A2D 不再使用固定屏蔽比率，而是在训练时从均匀分布中采样 $\lambda \sim U(\epsilon, 1)$（$\epsilon$ 为最小屏蔽率，通常取较小值）。这一策略使模型在训练期间同时接触早期（高屏蔽率）和晚期（低屏蔽率）解码状态，促使安全对齐在整个生成轨迹上保持一致，而非仅在初始步有效——这正是实现"任意步骤"防御的关键机制。

### 训练与解码的输入输出流

1. **输入流**：给定一个提示与响应对 $(x, y)$，按屏蔽比率 $\lambda$ 随机屏蔽部分令牌，形成被破坏序列。若样本来自有害集，显式标记有害片段的屏蔽位置；若来自保留集，不做额外标记。
2. **训练监督**：对每个屏蔽位置 $j$，
   - 若样本属于有害集且该位置处于有害片段内，监督目标 $y_j^* = [\mathrm{EOS}]$；
   - 否则，监督目标为原始令牌 $y_j^* = y_j$（即保持标准重构损失）。
3. **输出流（训练）**：模型在所有屏蔽位置上学习预测对应的监督令牌，通过交叉熵损失优化，并采用 $1/\lambda$ 归一化以抵消不同屏蔽率对损失幅度的影响。
4. **输出流（推理）**：对齐后的模型在迭代解码时，若在任意步骤、任意位置检测到有害上下文，其输出的 [EOS] 概率会显著升高。通过监测首步最左屏蔽位置的 [EOS] 概率并设定阈值 $\tau$，A2D 支持**早期拒绝**：一旦概率超过阈值，直接终止生成。这一机制在 AdvBench 上最高实现 19.3× 的安全终止加速，同时 XSTest 上保持 0% 的假阳性率，验证了其实时安全监控的有效性与精准性。

整体而言，A2D 通过**数据驱动的[EOS]替换训练**与**均匀屏蔽比率覆盖**，将安全对齐从粗粒度的响应级下沉到令牌级，既根治了扩散语言模型的浅层对齐问题，又在不引入额外推理复杂度的前提下提供了高效、可调节的早期拒绝能力。

## 核心模块与公式推导

扩散语言模型（dLLM）在任意顺序生成过程中，有害内容可能出现在序列的任意位置。现有响应级对齐（如拒绝训练 RT）仅在完整响应层面监督拒绝行为，导致安全信号在解码过程中迅速衰减——这是一种"浅层对齐"。A2D 的根本应对是建立**令牌级拒绝机制**：将特殊的 `[EOS]` 作为通用拒绝令牌，一旦在任意解码位置、任意解码步骤中检测到有害跨度，模型便输出 `[EOS]` 并终止生成。为实现这一机制，A2D 在训练时围绕两条核心线路重构了监督信号：屏蔽令牌的目标替换与屏蔽比率的全域覆盖。

### 1. 核心训练模块

A2D 的训练数据由两个专用集合组成，二者各自承载不同的监督信号：

- **Harmful Set（$\mathcal{D}_{\mathrm{harm}}$）**：包含高风险的"有害提示‑不安全响应"对。对于经过屏蔽扩散处理的隐蔽序列，若某个被屏蔽的令牌位于有害跨度内，其监督目标即被强制设为 `[EOS]`，而非原始令牌。这赋予了模型"遇到有害内容即终止"的内在行为。

- **Retain Set（$\mathcal{D}_{\mathrm{retain}}$）**：涵盖安全的"提示‑响应"对以及"有害提示‑安全响应"对。该集合中的被屏蔽令牌保持原始的交叉熵目标，训练模型重建原始内容，从而避免能力退化并维持正常的安全遵从。

- **令牌级监督**：训练时，根据当前样本的来源集合，动态切换每个屏蔽位置的目标：若来自 $\mathcal{D}_{\mathrm{harm}}$，目标为 `[EOS]`；若来自 $\mathcal{D}_{\mathrm{retain}}$，目标为原始令牌。这一设计正是 A2D 实现"在任何生成步骤中都能及时拒绝"的关键。

- **均匀屏蔽率采样**：为让模型在从初始噪声到完全解码的整个生成轨迹中都保持健壮的安全行为，训练中屏蔽率 $\lambda$ 并非固定不变，而是从区间 $[\epsilon, 1]$ 均匀采样（$\epsilon$ 为一个较小的最小屏蔽率，如 0.01）。这样一来，模型在训练阶段就经历了所有解码阶段，从而在面对不同攻击模板和不同解码秩序时表现出稳定的防御性。

### 2. 关键公式与变量含义

A2D 以屏蔽扩散框架为基础。设原始序列为 $\mathbf{x}_0$，经扩散过程按照屏蔽率 $\lambda$ 被破坏后得到 $\mathbf{x}_{\lambda}$。模型在给定 $\mathbf{x}_{\lambda}$ 的情况下，对每个位置 $i$ 预测其原始令牌：

$$ q_{\theta}(x^i \mid \mathbf{x}_{\lambda}) = P_{\theta}(x^i = x_0^i \mid \mathbf{x}_{\lambda}) . $$

扩散训练的标准损失为跨所有屏蔽位置的平均交叉熵，并用 $1/\lambda$ 进行尺度归一化：

$$ \mathcal{L}(\theta) = \mathbb{E}_{\lambda,\mathbf{x}_0,\mathbf{x}_\lambda}\left[-\frac{1}{\lambda}\sum_{i=1}^L \mathbf{1}[x_\lambda^i = [\mathrm{MASK}]] \log q_\theta(x_0^i \mid \mathbf{x}_\lambda)\right] . $$

A2D 在上述损失的基础上，仅对监督目标进行了替换：对来自 $\mathcal{D}_{\mathrm{harm}}$ 的样本，所有被屏蔽位置 $j$（标记为 $m_j = 1$）的目标令牌直接取为 `[EOS]`：

$$ y_j^* = [\mathrm{EOS}] \quad \text{当且仅当 } m_j = 1 \text{ 且 }(x,y) \in \mathcal{D}_{\mathrm{harm}} . $$

除了目标信号，屏蔽率的设定同样影响模型的对齐深度。训练时使用的屏蔽率为：

$$ \lambda = (1 - \epsilon) t + \epsilon , $$

其中 $t$ 为扩散时间步（通常随机采样），$\epsilon$ 为最低屏蔽率。该线性插值确保训练始终覆盖从高噪声到低噪声的全部阶段，是实现"任何步骤都能拒绝"的必要条件。

通过将 `[EOS]` 固化为拒绝令牌，A2D 在保持原有扩散训练数学形式不变的前提下，将安全决策从响应级提升至令牌级。这种机制不仅在解码阶段构建了逐令牌的拒绝能力，还可借助初始步骤最左侧屏蔽位置的 `[EOS]` 概率实现实时安全监控与早期终止，无需额外的模块或复杂的损失函数。

## 实验与分析

A2D 在扩散语言模型上实现了令牌级的安全对齐，其核心因果机制在于训练时将有害片段中被屏蔽的令牌监督为 `[EOS]`，迫使模型在"遇到有害内容即终止"的策略下学习深层拒绝。该机制直接针对扩散模型的**瓶颈**——任意顺序生成导致有害内容可出现在解码全程的任何位置，而响应级对齐仅在初始令牌处理时强效，随后安全信号迅速衰减（浅层对齐），使 DIJA 等模板攻击轻易在解码后期绕过。以下从主结果、消融、对齐深度、早期拒绝及极限条件等角度展开分析。

### 主结果：全面压制攻击成功率

在覆盖 Zeroshot、PAIR、ReNeLLM、Prefilling、DIJA 五类攻击的综合性安全基准上，A2D 在三个指令微调的扩散语言模型上均取得最低的平均有害性攻击成功率（ASR）：LLaDA-8B-Instruct 降至 6.8、LLaDA-1.5 降至 9.1、Dream-v0-Instruct-7B 降至 2.8（Table 1）。相比之下，最优基线 VRPO 对应数值为 21.6、22.0、22.7，A2D 较其平均再降低约 60%。更为关键的是，针对 DIJA 这种利用任意顺序生成特性、在原始模型上成功率超过 80% 的白盒攻击，A2D 将其压制至接近零：LLaDA 上仅 1.3%，LLaDA-1.5 上 3.5%，Dream 上 0.0%（Table 1）。这表明令牌级 `[EOS]` 监督成功构建了"在任何位置、任何解码步骤上识别并终止有害生成"的防御壁垒，彻底瓦解了 DIJA 的攻击假设。


![[assets/figures/papers/iclr26_0005_URTnuyQJI1_A2D_Any-Order_Any-Step_Safety_Alignment_for_Diff/figures/006_Table_1.jpg]]
*Table 1: Comprehensive evaluation results on capability and harmfulness for three instruction-tuned dLLMs across four alignment methods. A2D effectively mitigates diverse jailbreak attacks while preserving competitive capability. The top-performing method is shown in bold, and the second-best is underlined. All results are averaged over three random seeds, and Original refers to the model without any alignment fine-tuning*

不同解码策略（左到右、右到左、置信度优先、熵优先、随机）下的鲁棒性在 Table 2 中得到验证：无论在何种顺序下解码，A2D 在 Dream 模型上对所有攻击的 ASR 均保持为 0.0%，在 LLaDA 上也普遍低于 5%。这证实了统一采用随机屏蔽比率训练所促成的**任意步、任意顺序**防御真正落实到了推理层面。

### 对齐深度的量化证据

Figure 4 通过逐令牌 KL 散度刻画了 A2D 对齐后模型与基础模型在有害提示上的行为分离程度。无论采用左到右、置信度优先还是随机解码，A2D 对齐模型的 KL 散度在解码全程均持续维持较高水平，而响应级对齐（RT 或 VRPO）仅在最初几个令牌上出现明显差异，随后迅速回落至基线附近。该曲线直接验证了先前分析的"浅层对齐"现象，也量化了 A2D 实现的**深层对齐**——安全行为在整个生成轨迹中被持续强化，而非只依附于起始点。


![[assets/figures/papers/iclr26_0005_URTnuyQJI1_A2D_Any-Order_Any-Step_Safety_Alignment_for_Diff/figures/009_Figure_4.jpg]]
*Figure 4: Per-token KL divergence between A2D-aligned and base dLLMs. Aligned models (LLaDA-1.5, LLaDA-1.5-A2D) vs. Base model (LLaDA-Base) on Harmful BeaverTails under three sampling strategies. LLaDA-1.5-A2D refers to LLaDA-1.5 further aligned with A2D for safety. All results are averaged over 150 harmful prompts from BeaverTails, with shaded regions indicating standard deviation*

### 关键消融：拒绝令牌的选择

Table 3 的消融实验表明，选择 `[EOS]` 作为拒绝令牌在安全性与能力之间取得最佳平衡。相较于训练过程中临时引入的 OOD（Out-of-Distribution）令牌、高频令牌或低频令牌，`[EOS]` 原本即作为填充与终止字符被模型广泛使用，无需额外的嵌入适应即可作为"安全终止"信号。在能力基准（如 MMLU、GSM8K）上，`[EOS]` 方案的能力退让最小；在有害性控制上，其 ASR 同样优于其他替代令牌。这一消融证实了令牌级对齐中语义相容性对提升防御鲁棒性及维持通用能力的重要性。


![[assets/figures/papers/iclr26_0005_URTnuyQJI1_A2D_Any-Order_Any-Step_Safety_Alignment_for_Diff/figures/014_Table_3.jpg]]
*Table 3: Ablation study on refusal token selection: comparative impact on capability and harmfulness. The best-performing token is shown in bold*

### 早期拒绝：安全监控与速度提升

A2D 将 `[EOS]` 概率直接用作实时安全监控指标。在第一步解码时，取最左屏蔽位置的 `[EOS]` 概率作为早期拒绝信号：若该概率超过阈值 τ，则直接终止生成，无需执行完整的迭代去噪。Figure 8 的左侧分布显示，有害提示在该位置的 `[EOS]` 概率高度集中于 1.0 附近，而良性提示概率极低。可通过调节 τ 在拒绝对齐与过度拒绝间权衡：当 τ=0.9 时，在 520 条 AdvBench 有害样本上平均实现 6× 的安全终止加速，仅导致 1.6% 的良性样本被误拒；进一步降低至 τ=0.8 时，加速比提升至 19.3×，但拒绝率相应上升。这一机制充分利用了 A2D 在任意步均可输出 `[EOS]` 的特性，将安全审查从生成后阶段提前至生成进行中，显著降低了安全对齐的计算开销。

### 极端条件下的防御与合规性

在填充句子攻击（FITS）这种向给定有害前缀中插入文本的极端场景下，A2D 在三个模型上均将 ASR 压至近乎零 (Figure 5a)。同时，对于易造成过度拒绝的 XSTest 基准，A2D 实现了 0% 的假阳性——即所有构造为看似不安全实则良性的提示均得到了正常响应，避免了安全对齐中常见的"宁可错杀"问题 (Figure 5b)。相比之下，RT 和 VRPO 在 XSTest 上出现了较高的拒绝量，表明以完整响应为单位的拒绝训练容易产生泛化偏差。

### 能力保持与计算代价

Table 12 汇报了完整能力基准结果。A2D 在多数能力指标上与非对齐版本或响应级对齐方法持平，例如在 Dream 的 GSM8K 上达到 81.8±0.3，优于若干基线。但在部分任务（如 MMLU）上出现约 1–2 个百分点的下降，呈现出轻微的能力对齐税。训练计算量方面，A2D 与 RT、SFT 接近（9.7 T FLOPs），远低于 VRPO 的数十 T FLOPs（Table 8），保证了实用可行性。

### 失败模式与局限

当前评估集中于 LLaDA 与 Dream 等代表性开源扩散架构，扩散式模型的演进速度较快，后续需要验证 A2D 在更多（如可扩展性和样本效率不同的）架构上的表现。对自回归模型的适配仅在 Qwen-2.5 和 LLaMA-3.1 上进行了初步实验，其完整防御效能尚待大规模验证。另外，尽管早期拒绝加速显著，在对抗性模板专门设计以规避起始步检测的情况下，是否存在绕过该机制的可能性仍有待研究，例如在后续步才触发有害内容的攻击形态。

### 补充图表

![[assets/figures/papers/iclr26_0005_URTnuyQJI1_A2D_Any-Order_Any-Step_Safety_Alignment_for_Diff/figures/030_Figure_9.jpg]]
*Figure 9: Early rejection trade-off. The red curves show speed-up measured on HARMBENCH, while the blue curves report accuracy on XSTEST, evaluated across different early rejection thresholds (τ )*

![[assets/figures/papers/iclr26_0005_URTnuyQJI1_A2D_Any-Order_Any-Step_Safety_Alignment_for_Diff/figures/012_Figure_5.jpg]]
*Figure 5: Attack success rates on extreme conditions for three instruction-tuned dLLMs across four alignment methods*


## 方法谱系与知识库定位

A2D 解决的核心瓶颈在于：现有扩散语言模型（dLLM）的安全对齐方法多为 *响应级* 对齐（RT、SFT、VRPO），仅在完整响应层面对拒绝行为进行监督。这种浅层对齐在生成初期（如首个令牌位置）尚能维持安全信号，但随解码进行，安全监控迅速衰减——特别是在扩散模型的任意顺序生成下，有害内容可出现在响应的任意位置，导致 DIJA 等模板攻击在后段解码时轻易绕开拒绝。A2D 将[EOS] 转化为通用拒绝令牌，在训练时强制被屏蔽的有害跨度位置输出 [EOS]，同时保留正常文本的重构目标，从而建立 *令牌级* 深度拒绝机制：无论在何种解码顺序、任何解码步骤，只要模型"看到"有害跨度，即终止生成。

与基线方法的根本区别在于：RT 和 SFT 只学习"整句拒绝"的分布，VRPO 通过偏好优化间接强化安全行为，但它们都无法在令牌粒度上对内容进行实时安全监控。A2D 通过改变两个关键要素达成深度对齐：① 训练目标——有害数据中被屏蔽令牌的目标由"重建原始令牌"变为"预测 [EOS]"（锚点：Algorithm 1 / Section 5）；② 屏蔽率采样——从固定的部分比率改为 $\lambda \sim U(\epsilon, 1)$ 的均匀采样，使训练覆盖全部解码阶段，确保任意步骤均能稳定触发拒绝（锚点：Section 5）。由此，A2D 不仅在平均有害性攻击成功率上远低于基线（Table 1：LLaDA 上 A2D 6.8 vs. VRPO 21.6、RT 51.5），而且将 DIJA 成功率从 >80% 降至接近零（1.3% LLaDA，3.5% LLaDA‑1.5，0.0% Dream），并在 XSTest 的类不安全良性样本上实现 0% 假阳性，避免了过度拒绝。更深层的对齐证据来自解码过程的逐令牌 KL 散度分析（Figure 4）：A2D 对齐后的模型在整个轨迹上持续维持与基础模型的分布差异，而指令微调模型仅在早期短暂出现差异而后迅速回落，反映出浅层对齐的本质。

**适用边界**。A2D 的核心设计扎根于掩码扩散的生成范式，利用任意顺序预测和屏蔽重建的优势。它要求训练时提供已标注的有害跨度（可从安全分类器或人工标注获得），同时维护一个无害的保留集以维持正常能力。对于无法可靠识别有害片段的内容，直接的令牌级替换可能失效或引入噪声。在自回归模型的初步适配中（附录 C.5），通过强制模型在有害前缀后立即预测 [EOS] 获得了一定效果，但自回归的因果掩码限制了"任意步"拒绝的灵活性，且完整架构泛化能力尚未验证。因此，当前 A2D 的最佳适用范围为经过指令微调的扩散式语言模型，在这些模型上表现出的对抗鲁棒性远高于其他范式。

**局限性与开放问题**。主要局限包括：① 评估集中在 LLaDA、LLaDA‑1.5、Dream 等几个代表性开源 dLLM 上，扩散架构仍在快速演进，需扩展至更多变体；② 尽管早期拒绝利用首个最左屏蔽位置的 [EOS] 概率，最高可实现 19.3× 安全终止加速，但该机制依赖阈值 $\tau$ 的选取，在加速率与假拒绝率之间需权衡（Figure 8），极端阈值可能导致过度拒绝；③ 在某些知识密集或推理任务（如 MMLU）上 A2D 存在轻微能力下降（Table 12 及相关结果），反映了令牌级安全约束可能带来的能力对齐税。

未来的关键开放问题包括：能否在更复杂、多轮的开放域对话中维持令牌级对齐，以避免上下文漂移导致漏报；是否存在可攻击早期拒绝机制的对抗模板，使得有害内容在起始步未被检测到，而在后续采样中被补全（即"潜伏式"有害生成）；如何将令牌级对齐的理念系统性地推广至自回归解码、流匹配等生成范式，以构建统一的安全框架；以及如何更精细地建模安全与有用性的权衡，确保 [EOS] 只在真正有害的语境中高概率触发，进一步降低对齐税。

## 原文 PDF

![[paperPDFs/ICLR_2026/A2D_Any_Order_Any_Step_Safety_Alignment_for_Diffusion_Language_Models.pdf]]
