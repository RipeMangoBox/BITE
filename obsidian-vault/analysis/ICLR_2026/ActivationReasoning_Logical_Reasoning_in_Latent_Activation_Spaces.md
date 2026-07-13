---
title: "ActivationReasoning: Logical Reasoning in Latent Activation Spaces"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/ActivationReasoning_Logical_Reasoning_in_Latent_Activation_Spaces.pdf
project_link: null
code_link: https://github.com/ml-research/ActivationReasoning
aliases:
- AA
- ActivationReasoning
- "ACTIVATIONREASONING (AR)"
tags:
- ICLR_2026
- topic/generative_models_diffusion
- topic/generative_models_diffusion/generative_models_and_autoencoders
core_operator: "在LLM的潜在激活空间中，对稀疏自编码器（SAE）特征应用用户定义的逻辑规则，通过前向链接推理来增强模型的可控性和推理能力。"
primary_logic: "将SAE特征作为命题构建块，嵌入显式逻辑规则到LLM的潜在表示中，能够在连续、叠加的激活空间里实现可解释的组合推理与行为控制，弥补神经网络与符号推理之间的鸿沟。"
claims:
- "在多跳推理任务PrOntoQA上，AR（Llama3.1 8B）5跳准确率达到95.3%，远超基线（约50%），且性能不随跳数增加而衰减。"
- "在Rail2Country的Meta场景（通过比喻描述颜色）中，AR将颜色检测准确率从0%恢复到92.95%（Llama3.1 8B），并将推理准确率从29.67%提升至62.67%。"
- "在安全基准BeaverTails上，Relational AR实现83.0%的总体平衡准确率，较基础SAE提升25.1个百分点。"
- "PrOntoQA (5-hop) 上 Exact-match accuracy (%) = 95.3 (AR, Llama3.1 8B)"
---

# ActivationReasoning: Logical Reasoning in Latent Activation Spaces

> [!tip] 核心洞察
> 将SAE特征作为命题构建块，嵌入显式逻辑规则到LLM的潜在表示中，能够在连续、叠加的激活空间里实现可解释的组合推理与行为控制，弥补神经网络与符号推理之间的鸿沟。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 激活推理：潜在激活空间中的逻辑推理 |
| 英文题名 | ActivationReasoning: Logical Reasoning in Latent Activation Spaces |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=gGJh5AZTG7) · [GitHub](https://github.com/ml-research/ActivationReasoning) |
| Topic | #topic/generative_models_diffusion #topic/generative_models_diffusion/generative_models_and_autoencoders |
| Method | ACTIVATIONREASONING (AR) |
| Dataset | PrOntoQA (5-hop), Rail2Country Meta (Reasoning), ProverQA (Hard), BeaverTails Safety |

> [!tip] 效果简介
> - PrOntoQA (5-hop) 上，Exact-match accuracy (%) 为 95.3 (AR, Llama3.1 8B)，对比 50.3 (Base Llama3.1 8B)，变化 +45.0。
> - Rail2Country Meta (Reasoning) 上，Exact-match accuracy (%) 为 62.67 (AR, Llama3.1 8B)，对比 29.67 (Base LLM, Llama3.1 8B)，变化 +33.0。
> - ProverQA (Hard) 上，Exact-match accuracy (%) 为 70.8 (AR, Llama3.1 8B)，对比 45.0 (Instruct+CoT+SC, Llama3.1 8B)，变化 +25.8。

## 概要

大型语言模型（LLM）在系统推理、组合泛化与规则执行上长期面临根本性瓶颈：其潜在表示高度纠缠且叠加，缺乏显式的命题结构，难以支撑稳定、可解释的逻辑推理。本文提出 **ACTIVATIONREASONING (AR)**，一种在 LLM 的潜在激活空间中直接进行逻辑推理的框架。其核心思路是将稀疏自编码器（SAE）提取的特征视为命题构建块，嵌入用户定义的逻辑规则，通过前向链接推理在连续、叠加的激活空间内实现可解释的组合推理与行为控制，从而弥合神经网络与符号推理之间的鸿沟。

AR 带来的性能提升在多项基准上由决定性证据支撑：
- 在 PrOntoQA 多跳推理任务中，AR（Llama3.1 8B）在 5 跳设定下准确率达到 **95.3%**，较基础模型（≈50%）提升逾 45 个百分点，且性能不随跳数增加而衰减（Table 1）。
- 在 Rail2Country 的 Meta 场景（须通过比喻描述识别颜色并推理国家）中，AR 将颜色检测准确率从 0% 恢复至 **92.95%**，并将推理准确率从 29.67% 提升至 **62.67%**（Table 1, Table 5）。
- 在安全基准 BeaverTails 上，Relational AR 达到了 **83.0%** 的总体平衡准确率，较基础 SAE 提升 25.1 个百分点（Table 2）。

方法上，AR 不改变模型参数，而是构建于三个模块化阶段之上：概念表征提取、命题激活与逻辑推理，并可进一步通过 SAE 解码器权重对隐藏状态进行概念级转向干预。该框架在保持高推理效率（仅需约 2k tokens，而 Instruct+CoT+SC 约需 11M tokens）的同时，展现出对层位置、概念表征规模的鲁棒性，为可审计、可控且可解释的神经符号推理提供了新的路径。



大型语言模型（LLMs）在广泛的自然语言任务中展现出卓越性能，但其内部工作机制仍然是一个高度纠缠的"黑箱"。模型通过在连续、叠加的潜在表示中编码知识，缺乏显式的命题结构与组合推理机制，这直接导致了三个核心瓶颈：系统推理能力薄弱、组合泛化困难、以及对模型行为缺乏可解释的控制手段。当任务需要多步逻辑链、对抽象概念的比喻性描述进行推理，或必须在激活层面执行安全规则时，LLMs往往表现脆弱。

现有方法试图从不同路径缓解上述问题。基于提示工程的技术（如思维链 CoT 与自一致性 SC）通过引导生成过程引入显式推理步骤，但推理过程依赖于模型自身的生成质量，计算开销大且效果随任务复杂度衰减。例如，在 PrOntoQA 5 跳推理任务上，经过指令微调并采用 CoT+SC 的 Llama3.1 8B 准确率仅约 50%（Table 1）。稀疏自编码器（SAE）能够提取可解释的潜在特征，揭示模型"知道"哪些概念，但它们仅停留在"检测"层面——无法利用这些概念进行结构化推理，也未能转化为对模型行为的主动控制。SAE 基线在 Rail2Country 的比喻场景（如用"像番茄一样"描述红色）中，颜色检测准确率甚至为 0%（Table 5），说明单靠特征提取无法解决抽象语义的鲁棒理解问题。此外，在 BeaverTails 安全基准上，基础 SAE 的总体平衡准确率仅为 57.9%（Table 2），远未达到可部署水平。

上述缺口的根源在于：LLMs 的潜在空间虽然富含概念信息，但缺少一种在连续激活空间中应用离散逻辑规则、进行系统推理并干预模型输出的范式。这正是 ActivationReasoning（AR）所回应的根本动机。AR 的核心洞见是将 SAE 特征视为命题构建块，在 LLM 激活空间中嵌入用户定义的显式逻辑规则，通过前向链接推理实现可解释的组合推理与行为控制，在神经网络与符号推理之间架起桥梁。这一思想将 SAE 从被动检测工具升级为结构化推理与可控干预的完整管线——从概念表征构建，到命题激活与逻辑推导，再到通过 SAE 解码器权重对隐藏状态进行转向干预（Section 3），使模型内部的概念知识第一次被组织起来，去执行可解释、可组合且可操控的逻辑推理。



## 核心方法与创新机理

大型语言模型（LLM）的潜在表示高度纠缠且叠加，缺乏显式的命题结构，导致系统推理、组合泛化和规则执行面临根本性困难。ActivationReasoning (AR) 的核心创新在于：**将稀疏自编码器（SAE）提取的特征作为命题构件，嵌入用户定义的前向链接逻辑规则，在 LLM 的连续激活空间中构建可解释、可组合的推理与行为控制机制**。该方法的因果操作柄是 SAE 特征激活矩阵上的规则演绎：通过显式推导新命题并反馈到模型表示，弥补了神经网络与符号推理之间的鸿沟。

相对于传统基线，AR 在三个关键槽位上实现了结构性改变：

1. **概念表征与提取**  
   *基线*：原始隐藏状态或无结构的 SAE 特征，缺乏规范化的概念定义。  
   *AR*：引入三种表征形式——单特征 $\mathcal{R}_{\mathrm{single}}$、多特征 $\mathcal{R}_{\mathrm{multi}}$ 和关系特征 $\mathcal{R}_{\mathrm{relation}}$，分别通过最大区分性索引、 top‑k 加权和以及决策树自动学习（Eq. 1），并采用平衡准确率最大化的软阈值 $\tau_{c}$ 判定激活状态（Eq. 2）（Section 3.1）。这一结构化设计使 SAE 特征成为可组合的逻辑原子。

2. **推理机制**  
   *基线*：无结构化推理，完全依赖模型自身生成（如 CoT、自一致性等）。  
   *AR*：构建 token 级与序列级激活矩阵 $A_{\mathrm{local}}$、$A_{\mathrm{global}}$（Eq. 4），在此基础上执行用户定义的前向链接规则，推导新命题并扩展激活矩阵 $A'$（Section 3.2, 3.3）。推理直接在潜在空间完成，不依赖文本生成，从而突破了多跳推理随跳数增加而衰减的瓶颈。

3. **模型控制与转向**  
   *基线*：无基于概念的干预。  
   *AR*：利用 SAE 解码器权重向量 $SAE_D[r_c]$ 和转向因子 $\alpha$，对隐藏状态 $h$ 进行概念级的方向性调整（Eq. 5）：$h' = h + \alpha \cdot \frac{(SAE_D[r_c] \times w) \times \|h\|_2}{\|SAE_D[r_c]\|_2}$。这使得安全对齐和可控生成可在潜在空间直接实现。

这些创新带来了显著的性能突破。在 PrOntoQA 多跳推理任务上，AR (Llama3.1 8B) 5 跳准确率达到 95.3%，远超基线的 50.3%，且准确率不随跳数增加而衰减（Table 1）。在 Rail2Country 的比喻场景（如"像番茄一样"表示红色）中，AR 将颜色检测准确率从 0% 恢复至约 93%，推理准确率提升超过 30 个百分点（Table 1, 5）。在安全基准 BeaverTails 上，Relational AR 实现了 83.0% 的总体平衡准确率，较基础 SAE 提升 25.1 个百分点（Table 2）。同时，AR 仅需约 2k tokens 即可完成推理，而 Instruct+CoT+SC 消耗约 11M tokens，效率提升达三个数量级（Appendix E）。消融实验进一步表明，多特征表征大小 $R_{\mathrm{multi}}=7$ 时效果最优，自动阈值与手动调优性能相当（93.55 vs. 93.45），且对 SAE 层位置的选择具有良好的鲁棒性（Table 6, Appendix G）。

当前 AR 的规则仍需人工定义，其能力也受限于 SAE 已解耦的概念范围。但总体而言，AR 通过将 LLM 的潜在激活转化为可审计、可组合的符号基板，为神经‑符号融合提供了一种高效且可解释的实现范式。



![[assets/figures/papers/iclr26_0006_gGJh5AZTG7_ActivationReasoning_Logical_Reasoning_in_Latent/figures/001_Figure_1.jpg]]
*Figure 1: Overview of ACTIVATIONREASONING. AR performs logical reasoning over LLM activations in three stages: (1) Finding latent representations, where concepts are identified in the SAE latent space and stored in a concept dictionary using single, multi, or relational feature representations; (2) Activating propositions, where token-level activations are detected during inference to form an activation matrix A; and (3) Logical reasoning, where pre-defined rules are applied over A to infer new higher-order structures, compose new propositions, yielding an enriched matrix A′. The structured activations can then be used for downstream transparency and control*

激活推理（ActivationReasoning, AR）瞄准大型语言模型潜在表示的根本瓶颈：隐藏状态高度纠缠、缺乏显式命题结构，导致系统推理和组合泛化困难。AR 将稀疏自编码器（SAE）特征作为可操作的命题基元，在连续、叠加的激活空间中嵌入显式的逻辑规则，打通了从特征提取到可控推理的全链路。

**整体流程**由四个串行模块构成，如图1所示（见原文 Figure 1）：

1. **概念表征构建**  
   - **输入**：目标概念的标注文本与 LLM 的 SAE 特征（稀疏码 $l_t$）。  
   - **处理**：自动或手动提取三种结构化表征——单特征 ($r_c$ 为一个特征索引)、多特征 ($r_c$ 为 top‑k 特征索引与权重)、关系特征 ($r_c$ 为决策树)。通过最大化平衡准确率的软阈值 $\tau_c$ 决定激活状态。  
   - **输出**：概念字典，每个概念 $c$ 绑定一种表征 $r_c$ 与阈值 $\tau_c$。

2. **命题激活**  
   - **输入**：推理时文本序列经 LLM 产生的 SAE 特征 $l_t$，以及概念字典。  
   - **处理**：对每个 token $t$ 和概念 $c$ 计算激活分数 $a(c,t)$（对应单特征取维度值、多特征加权和、关系特征决策树概率），再经阈值截断获得非负证据，形成 token 级激活矩阵 $A_{\text{local}}$ 与序列级全局矩阵 $A_{\text{global}}$。  
   - **输出**：激活矩阵 $A$，即命题的初始真值状态。

3. **逻辑推理**  
   - **输入**：激活矩阵 $A$ 与用户定义的逻辑规则（前向链接）。  
   - **处理**：应用规则在潜在空间中完成组合推理（如 AND、NOT、蕴含），推导出原本不在 SAE 空间中的高阶概念或缺失命题，生成丰富化的激活矩阵 $A'$。  
   - **输出**：增强的真值矩阵 $A'$，可直接支撑下游分析或决策。

4. **模型转向（控制）**  
   - **输入**：推理结果 $A'$ 或特定概念表征 $r_c$。  
   - **处理**：利用 SAE 解码器权重向量 $w$ 和转向因子 $\alpha$，沿概念方向调整 LLM 的隐藏状态 $h$：  
     $$h' = h + \alpha \cdot \frac{(SAE_D[r_c] \times w) \times \|h\|_2}{\|SAE_D[r_c]\|_2}$$
   - **输出**：受控的隐藏状态 $h'$，实现概念增强或抑制，从而改变模型行为。

**模块间的衔接**贯穿着"表征→激活→推理→作用"的因果链：阶段1构造的命题视角决定了阶段2的检测灵敏度与噪声水平；阶段2的激活质量直接约束阶段3推理的可靠性与组合深度；阶段3推理产生的复合命题再反馈至阶段4完成显式控制。整个框架不依赖模型自身生成推理过程，而是将推理外挂至激活空间，既保证了高度的可解释性，又带来了显著的效率优势——例如在 PrOntoQA 多跳推理中，5 跳准确率从基础模型的 50.3% 提升至 95.3%（Table 1），且仅需约 2k tokens 即可完成，远低于思维链方法约 11M tokens 的消耗（Appendix E）。

AR 的设计本质上是将 SAE 从静态特征提取扩展为动态符号推理与干预的基础设施，其核心假设——将 SAE 特征当作可靠的命题标签——在多类任务上获得了强有力的实验支持，但目前仍受限于 SAE 激活稳定性等可解释性领域的共性问题。



**ACTIVATIONREASONING (AR)** 在对齐的潜在空间中的推理被组织为四个紧密耦合的模块：概念表征构建、命题激活、逻辑推理和模型转向。下面按模块梳理关键机制与核心公式，并给出相应变量的含义。

**1. 概念表征构建**  
该模块将 SAE 特征对应到语义概念，形成三种结构化表征：单特征（$\mathcal{R}_{\mathrm{single}}$）、多特征（$\mathcal{R}_{\mathrm{multi}}$）和关系特征（$\mathcal{R}_{\mathrm{relation}}$）。自动提取方式利用 token 级标签 $y_{c,t}$ 和稀疏码 $l_t$，为每个概念 $c$ 求出最能区分的表征 $r_c$（公式 (1)）。对于单特征直接选取期望差异最大的特征索引，多特征则取 top‑$k$，关系特征通过决策树学习非线性交互条件。

$$
r_c =
\begin{cases}
\arg\max\left(\mathbb{E}[l_t \mid y_{c,t}=1] - \mathbb{E}[l_t \mid y_{c,t}=0]\right) & \text{for } \mathcal{R}_{\mathrm{single}} \\
\text{top-}k\left(\mathbb{E}[l_t \mid y_{c,t}=1] - \mathbb{E}[l_t \mid y_{c,t}=0]\right) & \text{for } \mathcal{R}_{\mathrm{multi}} \\
\text{decision tree induced from } (l_t, y_{c,t}) & \text{for } \mathcal{R}_{\mathrm{relation}}
\end{cases}
$$

其中 $l_t$ 为 token $t$ 处的 SAE 稀疏编码，$y_{c,t}$ 为概念 $c$ 的 token 级标签。  
为了将连续激活值二值化为命题状态，模块为每个概念选取最佳阈值 $\tau_c$，使得在标注数据上的平衡准确率最大化（公式 (2)）：

$$
\tau_{c} \in \arg\max_{\tau \ge 0}\; \frac{1}{2}\big(\mathrm{TPR}_c(\tau) + \mathrm{TNR}_c(\tau)\big)
$$

$\mathrm{TPR}_c(\tau)$ 和 $\mathrm{TNR}_c(\tau)$ 分别为阈值 $\tau$ 下的真阳率与真阴率。

**2. 命题激活**  
推理阶段对每个 token $t$ 和概念 $c$ 计算激活分数 $a(c,t)$（公式 (3)）。单特征直接取对应 SAE 维度值，多特征采用加权和，关系特征由训练好的决策树输出概率。

$$
a(c,t) =
\begin{cases}
l_t[r_c] & \text{if } r_c \in \mathscr{R}_{\mathrm{single}} \\
\sum w\, l_t[r_c] & \text{if } r_c \in \mathscr{R}_{\mathrm{multi}} \\
r_c(l_t) & \text{if } r_c \in \mathscr{R}_{\mathrm{relation}}
\end{cases}
$$

$r_c$ 为概念表征，$w$ 为多特征下的权重向量。  
随后通过阈值截断构建 token 级激活矩阵 $A_{\mathrm{local}}$ 和序列级激活矩阵 $A_{\mathrm{global}}$（公式 (4)）。

$$
A_{\mathrm{local}}[c,t] = \max(a_{c,t} - \tau_c, 0),\quad
A_{\mathrm{global}}[c] = \max(\operatorname{Agg}_{t\in S} a_{c,t} - \tau_c, 0)
$$

$\operatorname{Agg}_{t\in S}$ 表示在序列 $S$ 上的聚合操作（如取均值），$a_{c,t}$ 为概念 $c$ 在 token $t$ 的未截断激活分数。

**3. 逻辑推理**  
在此模块中，预先定义的逻辑规则（例如 Horn 规则或一阶逻辑蕴含式）被施加于激活矩阵 $A$。通过前向链接推导出新命题，将其追加到激活矩阵形成丰富后的 $A'$。该模块不引入新的数学公式，但决定了哪些复合概念或高阶关系可以被可解释地触发，是实现多跳组合推理与安全规则执行的核心瓶颈。

**4. 模型转向**  
为了将结构化推理结果反向注入模型行为，AR 使用概念对应的 SAE 解码器权重向量 $SAE_D[r_c]$ 与转向因子 $\alpha$ 调整隐藏状态 $h$（公式 (5)）。

$$
h' = h + \alpha \cdot \frac{(SAE_D[r_c] \times w) \times \|h\|_2}{\|SAE_D[r_c]\|_2}
$$

$h$ 为原始隐藏状态，$h'$ 为干预后的隐藏状态；$\alpha$ 控制干预强度与方向（增强或抑制），$w$ 为可选的加权向量（多特征场景下生效）。分母中的 $\|SAE_D[r_c]\|_2$ 用于归一化，保证干预幅度与当前表示量级相容。

以上四个模块共同构建了一条从潜在激活到逻辑命题再到可控输出的流水线：SAE 提供可解释的"符号基底"，阈值决断命题真值，逻辑规则实现组合泛化，转向机制将推理结果作用于生成过程。



## 实验与关键发现

### 主结果

ACTIVATIONREASONING（AR）在多个基准上一致地显著提升了推理与控制能力。在多跳推理任务 PrOntoQA 上，AR 将 Llama3.1 8B 的 5 跳准确率从基线的约 50 % 拉升至 95.3 %（Table 1），且准确率不随跳数增加而衰减——1 跳和 3 跳分别达到 95.0 % 和 95.6 %。相比专为推理设计的 DeepSeek‑R1‑Distill‑Llama‑8B，AR 仅在约 2k tokens 的推理开销下（Appendix E）就将 5 跳性能高出逾 40 个百分点，体现出在激活空间内直接进行逻辑推演的巨大优势。

![[assets/figures/papers/iclr26_0006_gGJh5AZTG7_ActivationReasoning_Logical_Reasoning_in_Latent/figures/003_Table_1.jpg]]
*Table 1: Reasoning on latent activations. Exact-match accuracy on PrOntoQA (1–5 hop reasoning), Rail2Country (Mono with explicit concepts; Meta with similes, e.g., 'red' → 'like a tomato'), and ProverQA (linguistically diverse reasoning tasks across difficulty levels). AR consistently boosts multi-hop reasoning, remains robust as task complexity scales, and generalizes to natural and diverse language–outperforming its baselines, and even other reasoning/larger instruction-tuned (it) LLMs*

在需要从比喻表达中抽象概念的 Rail2Country Meta 场景中，底层模型完全无法辨识颜色比喻（检测准确率 0 %），AI 通过 SAE 提取的关系特征并施加规则后，检测准确率恢复至 92.95 %（Llama3.1 8B），整体推理准确率从 29.67 % 提升至 62.67 %（Table 1，Table 5）。在语言更具多样性的 ProverQA Hard 子集中，AR 亦将准确率从 Instruct + CoT + SC 的 45.0 % 提升至 70.8 %，证明其跨难度的泛化性。

![[assets/figures/papers/iclr26_0006_gGJh5AZTG7_ActivationReasoning_Logical_Reasoning_in_Latent/figures/008_Table_5.jpg]]
*Table 5: Rail2Country Ablation and Additional Insights. Exact-match (↑%) results on R2C-Mono and R2C-Meta variants. Top: overall results. Middle: per-simile breakdown (detection). Bottom: per-country breakdown (reasoning). AR improves both detection and reasoning over the base model. R2C Detection & Reasoning*

安全控制方面亦有可验证的效果。BeaverTails 基准的 14 个安全维度上，关系型 AR（Relational AR）使总体平衡准确率达到 83.0 %，较仅使用基础 SAE 特征的基线提高 25.1 个百分点（Table 2）。其中在 "Hate" 维度上提升达 33.1 个百分点，表明 AR 能在潜在激活层面可靠地执行安全规则。

![[assets/figures/papers/iclr26_0006_gGJh5AZTG7_ActivationReasoning_Logical_Reasoning_in_Latent/figures/004_Table_2.jpg]]
*Table 2: Safety Evaluation. Balanced accuracy (%) across 14 BeaverTails safety dimensions, with deltas indicating improvements over Base SAE. Relational AR (Llama3.1 8B) achieves the best overall performance, while multi-feature (5) AR also provides strong gains over flat SAE features*

### 消融实验

消融研究从表征设计、阈值策略、层级选择和推理效率等多个角度检验了 AR 各组件的贡献。

**多特征表征规模**：在 PrOntoQA 的 Gemma2 9B 实验中，当多特征表征的大小 $R_{\mathrm{multi}} = 7$ 时 5 跳准确率达到最高 93.70 %（Table 6 a），且性能随 $R_{\mathrm{multi}}$ 从 3 到 13 的变化平滑（最低仍高于 92 %），说明 AR 对特征数量的选择并不敏感。

![[assets/figures/papers/iclr26_0006_gGJh5AZTG7_ActivationReasoning_Logical_Reasoning_in_Latent/figures/011_Table_6.jpg]]
*Table 6: Hyperparameter ablations on ProntoQA with Gemma2 9B. (a) $\mathcal{R}_{multi}$ sizes*

**自动阈值 vs. 手动阈值**：AR 的软阈值选择机制通过最大化平衡准确率（式 (2)）自动确定激活门限。在 PrOntoQA（1 跳）上，自动阈值得到的准确率为 93.55 %，与人工调优的 93.45 % 几乎相同（Table 6 d），表明自适应的概念激活判别是可靠的。

**SAE 层的鲁棒性**：将 SAE 追加至第 18 层或第 22 层对 Rail2Country Mono 检测的准确率仅产生微弱波动（93.7 % vs. 93.3 %，Appendix G），说明 AR 本身是层无关的，并不依赖某一特定深度的表示，具备一定的架构鲁棒性。

**推理效率**：AR 的推理开销主要来自 SAE 特征计算与逻辑推演，总体仅需约 2k tokens，而 Instruct + CoT + SC 方案则需要约 11M tokens（Appendix E）。在时钟时间上，AR 的平均推断速度约为 0.375 秒/样本，远快于 CoT（1.647 秒/样本）和 DeepSeek‑R1（14.990 秒/样本），且仅比基础模型（0.107 秒/样本）略慢，展现出极高的效率（Table 3）。

![[assets/figures/papers/iclr26_0006_gGJh5AZTG7_ActivationReasoning_Logical_Reasoning_in_Latent/figures/005_Table_3.jpg]]
*Table 3: Runtime efficiency on R2C-Mono. AR achieves much faster inference than CoT and reasoning models, while being only marginally slower than the plain baseline. At the same time, it outperforms all alternatives in task accuracy*

### 失败模式与局限性

尽管 AR 在各种任务上取得了大幅提升，其性能仍然受到若干结构性限制，反映出当前方法的失败模式。

1. **比喻与复杂语义场景的残余误差**：Rail2Country Meta 中，AR 虽将推理准确率升高至 62.67 %，但仍有约 37 % 的错误。按比喻类别细分检测的结果显示，某些类型的比喻（如用 "like a tomato" 表达 "red"）仍可能因为 SAE 向量的叠加混淆而出现漏激活（Table 5 中间部分），说明在高度非字面的语义转换中，非组合的 SAE 特征仍可能不足以完全恢复概念的激活。

2. **安全概念检测的不完全性**：Unsafe 概念的激活准确率在关系型 AR 下为 62.0 %（Table 2），尽管比基础 SAE 提升显著，但仍有近 38 % 的安全违规未能被正确侦测。这表明在短文本或隐式不安全内容上，依赖 SAE 特征可能无法可靠地触发规则。

3. **SAE 激活不稳定性的传播**：AR 以 SAE 提取的稀疏特征作为推理的基本单元，因此对 SAE 自身的噪声和漂移敏感。当概念表征所依赖的少数 SAE 维度发生错误激活或被其他语义覆盖时，下游的逻辑推演和转向干预均可能产生错误。这一开放性问题在分析中被明确指出为机制可解释性的持续挑战。

4. **规则依赖与迁移局限**：AR 当前需要用户显式提供逻辑规则（如安全类别映射、PrOntoQA 的句法推导规则），这使得性能高度受限于规则的质量和覆盖率；对于未事先定义规则的新组合概念或跨域任务，框架无法自主发现推理链。

### 关键图表结论

- **Table 1（及扩展版的 Table 4）** 突出显示 AR 在多跳推理、比喻抽象和多样化语言任务上的全面提升，且准确率几乎不随推理步数（1 至 5 跳）下降，证实了将逻辑规则嵌入激活空间能稳定地维持组合推理能力。
- **Table 2** 展示了安全维度的细粒度提升：关系型 AR 在所有 14 个类别的平衡准确率都优于纯 SAE 基线，其中 "Hate"、"Terrorism" 等高风险类别的增益尤为突出，说明基于决策树的关系特征能更精准地建模危险概念。
- **Table 3 与 Table 5** 共同说明了速度－准确率的 Pareto 改善：AR 以远低于思维链的推理延迟（约 0.37 秒/样本）获得更高准确率，同时在 Rail2Country 检测任务中使 SAE 的彩色概念检测达到 100 % 正确。
- **Table 6 的一系列超参数消融** 表明 AR 对多特征规模、阈值策略及层级位置均具有良好的鲁棒性，进一步确认了该方法的工程稳定性与组件设计的合理性。



## 定位与知识库关联

ActivationReasoning (AR) 位于神经符号推理与可解释性机制的交汇处，其核心思想是将稀疏自编码器（SAE）解耦出的可解释特征作为命题原子，在潜在空间中执行用户定义的逻辑规则，从而将显式规则的控制力注入到原本高纠缠、叠加的神经网络激活中。这一范式不同于现有的三类主要推理增强策略：（1）**纯提示工程**类（Base、Instruct+CoT+SC）完全依赖模型自身的参数化知识，缺乏外部结构化的推理保证；（2）**专用推理架构**如DeepSeek-R1，通过大规模蒸馏或强化学习内化推理链，但依然受限于隐式处理，无法提供透明的组合级可控性；（3）**基于SAE的概念检测**（Base SAE）仅停留在特征提取层面，未将检测结果转化为推理与决策。AR的贡献在于打通了"表征—推理—控制"的完整闭环，在保持模型原有能力的前提下，赋予系统（i）组合缺失概念的能力（如从"桥""旧金山""美国"合成"金门大桥"），（ii）应对拼写/比喻等非字面输入的鲁棒性，以及（iii）神经层面的安全规则执行（Figure 2）。

**方法适用边界**。AR的有效性强依赖于两个前提：（i）存在高质量、与下游任务概念对齐的SAE特征空间，若SAE本身未能解耦出所需概念，AR的推理基石将不复存在；（ii）推理所需的知识能被完全表达为命题逻辑规则，即任务必须是封闭世界且概念间关系可被显式枚举。在Rail2Country和PrOntoQA这类概念集合固定、规则清晰的场景中，AR性能接近上限（多跳准确率>95%，Table 1）。相反，若概念集合动态变化、规则涉及不确定性或常识推理，AR当前的确定性前向链接机制难以直接适配。此外，AR的推理过程虽然高效（仅需约2k tokens对比CoT+SC的约11M tokens，Appendix E），但其准备阶段需要为每个概念构建表征并调优阈值，这种"固定字典"的方式限制了其在开放域动态概念上的即插即用能力。

**局限与开放问题**。
- **概念表征的自动化与泛化**：目前AR主要依赖基于标注数据的自动提取（Eq. 1）或人工指定，三种表征形式（单特征、多特征、关系特征）的选择仍需人工决策。开放问题是实现无监督或自监督的表征类型自动选择，以及将概念发现拓展到多语言、多模态情境。
- **规则获取瓶颈**：用户定义规则在控制精度上优势显著（安全任务中关系型AR将平衡准确率从57.9%提升至83.0%，Table 2），但规则编写成本高、覆盖度有限。前向推理的完备性取决于规则库的完整程度，当前无自动规则发现模块，是本框架向大规模复杂任务泛化的主要障碍。
- **SAE激活的稳定性**：Appendix G明确指出，提升SAE激活的稳定性仍是机械可解释性的公开挑战。AR的性能依赖于序列级激活聚合的鲁棒性，而对对抗性输入或表示坍缩的敏感性缺乏系统评估。尽管阈值自动选择（Eq. 2）表现出与手工调优相当的可靠性（Table 6(d)），但极端分布偏移下的退化行为仍有待研究。
- **推理范式的单一性**：AR嵌入的是确定性的命题逻辑，缺乏对概率推理、归纳推理或时间推理的支持。开放问题包括将AR框架与贝叶斯网络或归纳逻辑编程模块集成，以处理不确定情境下的推理。
- **层与架构依赖性**：论文指出AR本身是层无关的，SAE附加层的选择对性能影响微小（Appendix G），但该结论仅在Llama3.1与Gemma2的特定层得到验证。在大规模MoE架构或非Transformer模型中，SAE特征的迁移性和AR的即插即用性尚未得到保证，需要手动验证。

综上，AR在结构化推理任务中提供了一种高效、可解释且鲁棒的替代路径，尤其适合需要组合推理、多跳验证和安全约束的现实场景。但其知识表示和推理范围的刚性意味着，它更适合作为现有LLM的推理增强组件，而非全能推理替代品。未来方向包括自动规则学习、与不确定性推理的融合，以及更广泛的架构与数据域验证。



## 原文 PDF

PDF 文件：paperPDFs/ICLR_2026/ActivationReasoning_Logical_Reasoning_in_Latent_Activation_Spaces.pdf

![[paperPDFs/ICLR_2026/ActivationReasoning_Logical_Reasoning_in_Latent_Activation_Spaces.pdf]]
