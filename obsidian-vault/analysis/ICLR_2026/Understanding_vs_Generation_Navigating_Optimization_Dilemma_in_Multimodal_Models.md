---
title: "Understanding vs. Generation: Navigating Optimization Dilemma in Multimodal Models"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/Understanding_vs_Generation_Navigating_Optimization_Dilemma_in_Multimodal_Models.pdf
aliases:
- RRRR
- UVGNODMM
tags:
- ICLR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/vision_models_multimodal
core_operator: "将理解能力显式地嵌入生成过程，把单步生成重构为“推理-反思-提炼”的多步骤循环，使生成过程的优化内在依赖模型的理解能力，从而对齐生成与理解的优化目标。"
primary_logic: "通过让模型在生成中主动使用自身的理解能力来评估和改进输出，可以打破理解与生成之间的竞争关系，实现两者的协同进化。"
claims:
- "单独微调生成或理解任务会导致互补能力下降，而R3框架同时提升两者，GenEval++计数准确率从79.3升至84.6（见Figure 1）。"
- "在GenEval++生成基准上，R3相比基础模型BAGEL总体得分从0.371提升至0.689（+0.318）；在理解基准ITA上总体准确率从60.60%升至73.37%（+12.77），VQA从86.48%升至89.63%（+3.15）（见Table 1, Table 2, Table 3）。"
- "RL训练使模型对迭代反思的有效利用率大幅提升：R3在2轮Reflect-Refine后收敛至GenEval++ 0.689，而未经RL的BAGEL在相同推理策略下仅0.436（见Table 9）。"
- "训练过程中，生成准确率与VQA准确率同步上升，表明理解能力并未因生成训练而退化，反而随着生成过程的优化而增强（见Figure 7）。"
---

# Understanding vs. Generation: Navigating Optimization Dilemma in Multimodal Models

> [!tip] 核心洞察
> 通过让模型在生成中主动使用自身的理解能力来评估和改进输出，可以打破理解与生成之间的竞争关系，实现两者的协同进化。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 理解与生成：驾驭多模态模型中的优化困境 |
| 英文题名 | Understanding vs. Generation: Navigating Optimization Dilemma in Multimodal Models |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=1smez00sCm); [GitHub](https://github.com/sen-ye/R3) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/vision_models_multimodal |
| Method | Reason-Reflect-Refine (R3) |
| Dataset | GenEval++ (生成能力), Image-Text Alignment (ITA, 理解能力), Compositional VQA (理解能力), GenEval (SOTA对比) |

> [!tip] 效果简介
> - GenEval++ (生成能力) 上，Overall score (GPT-4.1) 为 0.689 (BAGEL+Ours)，对比 0.371 (BAGEL)，变化 +0.318。
> - Image-Text Alignment (ITA, 理解能力) 上，Overall accuracy (%) 为 73.37 (BAGEL+Ours)，对比 60.60 (BAGEL)，变化 +12.77。
> - Compositional VQA (理解能力) 上，Overall accuracy (%) 为 89.63 (BAGEL+Ours)，对比 86.48 (BAGEL)，变化 +3.15。

## 概述

多模态模型在统一处理“理解”与“生成”时面临根本性的优化冲突：共享模型容量的条件下，仅优化生成会损害理解能力，而单纯强化理解又会导致生成质量下降，形成此消彼长的权衡困境。传统策略通常将二者视为独立任务或简单联合训练，未能从根本上消解目标不一致的矛盾。

本文提出 **Reason‑Reflect‑Refine（R3）** 框架，从结构层面将单步生成重构为“推理‑反思‑提炼”的循环过程，使理解能力显式嵌入生成工作流。模型首先通过**推理（Reason）** 分析用户意图、生成文本蓝图并合成初始图像；随后进入**反思（Reflect）** 阶段评估当前输出与提示的对齐程度，若不满意则给出具体编辑指令；再由**提炼（Refine）** 阶段执行修正，直至输出满足要求或模型主动终止。这一设计让生成过程的优化天然依赖模型的理解能力，从而对齐两者的优化目标。训练上，R3 采用树结构强化学习（Tree‑RL）与分阶段奖励信号，交替优化推理策略与反思‑提炼策略，在加速收敛的同时保障生成与理解的协同进化。

关键实验结果表明，R3 有效打破了生成与理解的竞争关系。在 **GenEval++** 生成基准上，R3 将基础模型 BAGEL 的总体得分从 **0.371 提升至 0.689（+0.318）**（Table 1）；与此同时，理解能力同步大幅增强——在图像‑文本对齐（ITA）基准上总体准确率由 **60.60% 升至 73.37%（+12.77）**，组合视觉问答（VQA）准确率从 **86.48% 升至 89.63%（+3.15）**（Table 2, Table 3）。动机实验进一步显示，单独微调生成或理解均导致互补能力退化，而 R3 则可实现二者的联合高涨（Figure 1）；训练过程中生成准确率与 VQA 准确率亦呈现同步上升趋势（Figure 7），印证了理解并未因生成训练而牺牲，反而随生成优化得到强化。消融分析表明，完整的反思‑提炼循环是实现理解能力大幅提升的关键，而仅靠推理阶段带来的理解增益甚微。此外，经过强化学习训练的 R3 模型在迭代推理策略下收敛更快且性能更高——仅需 **2 轮 Reflect‑Refine 即达 0.689**，对于未经 RL 的模型即便 3～5 轮也仅能达到约 0.44（Table 9）。这些结果共同说明，通过将理解嵌入生成闭环并将优化信号聚焦于生成结果，R3 实现了生成质量与多模态理解能力的双赢。

## 背景与动机

当前多模态大模型需要同时支撑理解与生成两类核心能力：既要准确回答关于视觉内容的复杂问题（如VQA），也要忠实地遵循指令生成高质量图像。然而，在统一模型框架下，这两类能力往往呈现出此消彼长的竞争关系。**核心瓶颈**在于：生成任务与理解任务通常被视为独立的优化目标，共享模型容量但优化方向不一致。单独微调生成能力会导致模型的理解性能下降，反过来，强化理解训练也会损害生成质量。简单的多任务联合训练（naive co‑training）仅能带来微弱增益，无法根本解决这一优化困境（Figure 1）。其深层原因在于，传统方法将生成建模为单步前向输出，理解则作为后置的独立评估，两者缺乏内在耦合机制，导致任何一方的进步都可能以另一方的退化为代价。

**现有方法的缺口**在于，它们或者将生成与理解分而治之，或者试图通过多目标加权来平衡，但都没有改变“生成任务中的理解被外挂化”这一结构性问题。理解能力始终是生成过程的旁观者而非参与者，因此优化生成时无法自动受益于理解能力的提升，反之亦然。这造成了一种“跷跷板”式的权衡：在单一骨干模型上很难同时获得顶尖的生成指令追随能力与可靠的视觉-语言理解能力。

**本文动机**正是要打破这一困境。核心洞见是：**让模型在生成过程中主动使用自己的理解能力去评估和修正输出，从而将理解显式地嵌入生成循环**。如果将单步生成重构为“推理‑反思‑提炼”（Reason‑Reflect‑Refine）的多步骤过程，那么生成质量的最终提升将天然依赖于模型对自身输出与用户意图对齐程度的准确判断。这样一来，优化生成任务也就同时强迫模型增强其理解能力，二者不再相互掣肘，而是形成协同进化的正反馈。

基于这一动机，本文提出了**R3（Reason‑Reflect‑Refine）框架**，并设计了一套针对性的强化学习训练策略，旨在使生成与理解走出零和博弈，实现共同的显著提升。后续的实验表明，该框架不仅在GenEval++等生成基准上大幅超越基线（整体得分从0.371提升至0.689），同时系统性的理解评估（如图像-文本对齐基准ITA和组合VQA）也获得可观增益（ITA准确率从60.60%升至73.37%，VQA从86.48%升至89.63%），且训练过程中两者的能力曲线呈现同步上升趋势，确证了协同优化的有效性（Table 1、Table 2、Table 3、Figure 7）。

## 核心创新

传统多模态统一模型将图像生成与理解视为独立任务，共享模型容量但优化目标相互冲突：单独微调生成或理解会导致互补能力显著下降，而简单的多任务联合训练收益甚微（Figure 1）。R3框架的核心创新在于**将生成任务重构为一个主动利用自身理解能力的多步骤循环，并通过分阶段强化学习对齐生成与理解的优化目标**，从而打破了两者间的竞争关系，实现协同进化。

### 1. 理解能力内化为生成过程的核心组件

与基线BAGEL的单步前向生成不同，R3将生成重新定义为“**Reason（推理）–Reflect（反思）–Refine（提炼）**”的交替文本-图像生成序列（公式 $t^{1}, I^{1}, \ldots, t^{n}, I^{n} \sim \pi_{\theta}(\cdot | c)$，Section 2.2）。该过程迫使模型在生成中主动运用自身的理解能力：

- **Reason**：解析用户意图，生成包含细节的文本蓝图并据此合成初始图像。
- **Reflect**：审视当前图像与原提示的对齐程度；若满意则发出终止信号，否则生成具体的编辑指令。
- **Refine**：执行编辑指令，对前一步图像进行针对性修改，输出改进后的图像。

这一循环将理解能力从独立评估任务转变为**生成过程不可分割的核心环节**（changed slots: 生成过程结构、理解在生成中的角色）。模型不再仅仅生成图像，而是必须具备评估自身输出并指导修正的能力。实验表明，仅加入Reason阶段（无Reflect-Refine）虽能提升生成（GenEval++ 0.371→0.593），但对理解能力几乎无帮助；而完整的Reflect-Refine过程是理解能力大幅提升的关键（ITA准确率 +12.77，Table 2），充分说明理解能力真正被“激活”并参与了生成优化。

### 2. 分阶段树结构强化学习对齐双目标

为训练上述多步策略，R3引入了一套新颖的训练方案，替代基线中独立的生成/理解损失或简单多任务训练（changed slots: 训练策略、奖励信号设计）。

**交替优化Reason与Reflect-Refine策略**（Figure 3）。引入**树结构强化学习（Tree-RL）** 和重要性采样来加速长轨迹的收敛：先用Reason阶段填充回放缓冲区，再利用其中间状态对后续阶段进行on-policy训练。文本生成采用GRPO优化CoT策略，图像扩散模型采用FlowGRPO与MixGRPO（Section A.2），有效降低了长序列训练的高方差问题。

**阶段奖励对齐优化目标**（Section 2.4）。设计核心为**正确性度量** $C_j$：
$$ \mathbf{C}_{j} = \begin{cases} V_{j} - \hat{V} & \text{if } \hat{V} < 1 \\ \mathbb{I}(e_{j} = \text{"No further edit needed"}) & \text{if } \hat{V} = 1 \end{cases} $$
其中 $V_j$ 为由预训练奖励模型给出的图像-文本对齐评分。该度量奖励对不完美图像的实质性改进（$V_j > \hat{V}$），并对已完美图像奖励正确的自我终止。反思与提炼奖励分别为 $r_{j,\mathrm{reflection}} = \mathbf{C}_{j} + r_{j,\mathrm{format}}$ 和 $r_{j,\mathrm{refinement}} = \mathbf{C}_{j}$。阶段奖励设计确保模型不仅追求生成质量，更学会何时停止以及如何有效利用理解反馈进行修正。

该训练策略的关键效果在于**显著提升模型对迭代反思的利用效率**：未经RL训练的BAGEL在相同推理策略下GenEval++得分仅0.436，而R3经RL训练后仅2轮Reflect-Refine即可达到0.689（Table 9），表明RL使模型真正掌握“在生成中运用理解”的能力，而非机械迭代。

### 3. 打破优化困境的内在机制

上述两大创新从根源消解了“生成vs.理解”的权衡：通过将理解反馈嵌入生成的闭环修正，并利用阶段奖励统一优化方向，模型在提高生成质量的过程中必然强化其理解能力。训练动态（Figure 7）显示生成准确率与VQA准确率同步上升，未出现此消彼长，证实了协同进化。基线BAGEL无论是单独优化还是联合训练均无法避免能力退让（Figure 1），而R3通过流程重塑与对应奖励塑造，首次在统一多模态模型框架下实现了生成与理解的相互促进。

## 整体框架

![[assets/figures/papers/iclr26_0015_1smez00sCm_Understanding_vs._Generation_Navigating_Optimiza/figures/002_Figure_2.jpg]]
*Figure 2: The inference pipeline of our Reason-Reflect-Refine framework. The model starts by Reasoning to produce an initial plan and image. It then enters an iterative Reflect-Refine loop, assessing its output and making corrections until the image aligns with the user’s prompt or a stopping condition is met*

![[assets/figures/papers/iclr26_0015_1smez00sCm_Understanding_vs._Generation_Navigating_Optimiza/figures/003_Figure_3.jpg]]
*Figure 3: The training procedure, which alternates between optimizing the Reason policy and the Reflect-Refine policies. The replay buffer, populated by the Reason stage, provides on-policy data for training the subsequent stages*

R3（Reason‑Reflect‑Refine）框架将传统的一步生成重构为**“生成‑理解‑再生”的多步循环**，显式地把模型的理解能力嵌入到生成过程的每一次迭代中，从而打破理解与生成之间的优化冲突。整体流程如图2所示。

设用户提供的文本条件为 $c$。模型不再直接输出图像，而是依序产生一组交替的文本计划与图像结果：
$$t^{1}, I^{1}, \ldots, t^{n}, I^{n} \sim \pi_{\theta}(\cdot | c)$$
其中每一步 $j$ 都由三个具有明确分工的阶段组成，构成一个闭合的推理‑反思‑修正循环（详见 §2.2）：

1. **Reason（推理）阶段**  
   输入为原始提示 $c$。模型首先解析用户意图，生成含有细节描述的文本蓝图 $t^j$，然后根据该蓝图调用扩散模块合成初版图像 $I^j$。这一阶段主要承担“生成”的角色，但蓝图的构建本身依赖模型对语义的理解。

2. **Reflect（反思）阶段**  
   输入为当前提示 $c$ 与最新图像 $I^j$。模型需要自主评估图像‑文本对齐程度：若判断已满足要求，则输出终止信号；否则生成具体的编辑指令 $e_j$（如“将左上角物体的颜色由蓝色改为红色”）。该阶段是理解能力被显式激活的核心环节——模型不是在事后做评估，而是在生成流程内部用理解来指导下一步行为。

3. **Refine（提炼）阶段**  
   输入为编辑指令 $e_j$ 与当前图像 $I^j$。模型执行修正，输出改进后的图像 $I^{j+1}$。随后流程回到 Reflect 阶段，形成迭代闭环，直至满足对齐条件或达到预设最大轮次。

为避免往复修正带来的训练不稳定性，R3 采用**树结构强化学习（Tree‑RL）** 交替优化 Reason 策略与 Reflect‑Refine 策略（见图3）。奖励信号由预训练的视觉‑语言模型（Qwen‑2.5‑VL‑72B）提供图像‑文本对齐评分，并配合分阶段奖励设计：
- 推理阶段的文本生成奖励为 $r_{j,\text{text}} = V_{j} + r_{j,\text{format}}$，扩散生成奖励为 $r_{j,\text{diffusion}} = V_{j}$；
- 反思与提炼阶段的奖励基于改进度量 $\mathbf{C}_{j}$：若图像尚不完美则奖励改进幅度，若已完美则奖励正确的终止信号，即 $r_{j,\mathrm{reflection}} = \mathbf{C}_{j} + r_{j,\mathrm{format}}$，$r_{j,\mathrm{refinement}} = \mathbf{C}_{j}$（见公式2‑3）。这一设计使生成过程的优化方向天然依赖于模型的理解输出，从而对齐两者的优化目标。

通过上述管线，R3 将原本训推分离的理解任务内化为生成过程的一个子步骤，使模型在迭代生成中不断调用并强化自身的理解能力，最终实现生成质量与理解性能的同步提升（证据参见 §3 的实验结果）。

## 核心模块与公式推导

### 1 多步生成模块：Reason‑Reflect‑Refine

R3 框架将单步图像生成重构为“推理—反思—提炼”的交替序列，使理解能力以可微分的方式嵌入生成过程。三个子模块构成闭环：

- **Reason（推理）**  
  模型分析用户意图，生成详细文本蓝图，进而合成初始图像。该阶段将自由形式的提示转化为可执行的生成计划。
- **Reflect（反思）**  
  模型审视当前图像与原始提示的对齐程度：若满意则发出终止信号 `"No further edit needed"`；否则输出具体的编辑指令。这一步本质是视觉‑语言理解任务，迫使模型显式评估自身输出与目标的偏差。
- **Refine（提炼）**  
  依据反思指令对前一版图像进行编辑，输出修正后的图像。

三者构成 `Reason → [Reflect → Refine]⁺` 的循环。推理阶段生成初稿，反思阶段注入理解信号并指明修正方向，提炼阶段执行改进；当反思判定对齐要求已满足时，过程自适应终止。

### 2 强化学习训练：Tree‑RL

为高效训练长序列策略，论文采用树结构强化学习（Tree‑RL），分阶段交替优化 Reason 策略与 Reflect‑Refine 策略：
- 由 Reason 阶段产生批量轨迹填充回放缓冲区，供后续阶段进行重要性采样，避免全轨迹训练的高方差；
- Reflect‑Refine 阶段采用即时展开（immediate rollout），仅对所关心的子步骤进行信用分配，加速收敛；
- 文本生成（推理文本、反思语言）使用标准 GRPO 优化，扩散模型通过 FlowGRPO 处理连续动作空间，并混合 SDE/ODE 采样降低计算开销。

该设计使生成训练的信号能通过反思步骤传递至理解策略，实现两者的协同进化。

### 3 关键公式与变量含义

所有公式均在多步生成策略 $\pi_\theta$ 与预训练视觉‑语言奖励模型（Qwen‑2.5‑VL‑72B）给出的对齐评分 $V_j$ 框架下定义。

#### 3.1 多步生成序列形式化

$$
t^{1}, I^{1}, \ldots, t^{n}, I^{n} \sim \pi_{\theta}(\cdot \mid c)
$$

其中 $c$ 为输入条件（用户提示），$t^i$、$I^i$ 分别表示第 $i$ 步的文本输出（如推理计划、反思文本、编辑指令）和图像输出，$n$ 为总步数。

#### 3.2 反思正确性度量  

为鼓励反思步骤在图像不完美时提出有效修改、在图像完美时正确终止，定义度量 $\mathbf{C}_j$：

$$
\mathbf{C}_{j} = 
\begin{cases}
V_{j} - \hat{V}, & \text{if } \hat{V} < 1 \\
\mathbb{I}\big(e_{j} = \text{"No further edit needed"}\big), & \text{if } \hat{V} = 1
\end{cases}
$$

- $V_j$：当前图像的对齐评分；
- $\hat{V}$：上一迭代图像的对齐评分；
- $e_j$：反思步骤的语言输出；
- $\mathbb{I}(\cdot)$：指示函数，命题成立时为 $1$，否则为 $0$。

逻辑：若前一图像尚未完美（$\hat{V}<1$），则奖励改进量 $V_j - \hat{V}$；若前一图像已完美（$\hat{V}=1$），则奖励正确的终止信号。

#### 3.3 反思与提炼的奖励分配

$$
r_{j,\mathrm{reflection}} = \mathbf{C}_{j} + r_{j,\mathrm{format}}, \qquad
r_{j,\mathrm{refinement}} = \mathbf{C}_{j}
$$

- $r_{j,\mathrm{format}}$：格式奖励（如输出是否遵循指定的 XML 标签），确保反思文本可解析；
- 提炼步骤的奖励直接由 $\mathbf{C}_j$ 决定，因为其唯一目标是产出改进后的图像。

#### 3.4 推理阶段的奖励

Reason 阶段将文本计划生成与图像生成分别优化：

$$
r_{j,\mathrm{text}} = V_{j} + r_{j,\mathrm{format}}, \qquad
r_{j,\mathrm{diffusion}} = V_{j}
$$

- **文本奖励** $r_{j,\mathrm{text}}$：基于首轮生成图像的对齐评分 $V_j$（反映计划质量）加上格式奖励；
- **扩散奖励** $r_{j,\mathrm{diffusion}}$：仅使用对齐评分 $V_j$，驱动扩散过程生成高对齐度的图像。

上述奖励信号通过 GRPO/FlowGRPO 更新策略参数，使模型从最终图像质量出发，端到端学会推理、反思与修正，从而打破生成与理解的传统优化困境。

## 实验与分析

### 主要结果

Figure 1 给出了核心动机：若仅在单一任务（生成或理解）上微调 BAGEL，互补能力显著退化；简单联合训练收益微弱，而 R3 框架首次实现生成与理解的同步大幅提升。在 GenEval++ 计数子集上，计数准确率从 79.3 升至 84.6，同时理解能力亦未受损。

![[assets/figures/papers/iclr26_0015_1smez00sCm_Understanding_vs._Generation_Navigating_Optimiza/figures/001_Figure_1.jpg]]
*Figure 1: Fine-tuning BAGEL exclusively on generation or understanding degrades the complementary capability. Naive co-training shows minor gains, whereas our proposed method demonstrates significant improvement in both. Results are reported on counting subset of GenEval++*

**生成能力（GenEval++）**：Table 1 显示 BAGEL + Ours 的总体得分从 BAGEL 基线的 0.371 提升至 0.689（+0.318），超越 Echo‑4o（0.679），成为最佳方法。即便仅保留推理阶段的变体（BAGEL + Ours†）亦达到 0.593，表明结构化推理已具显著收益。

![[assets/figures/papers/iclr26_0015_1smez00sCm_Understanding_vs._Generation_Navigating_Optimiza/figures/005_Table_1.jpg]]
*Table 1: Instruction-following generation ability on the GenEval++ benchmark, evaluated by GPT-4.1. Bold indicates the best result. †indicates our framework with only the reasoning stage. Green arrows indicate improvement over the BAGEL baseline. Table 2: Evaluation of understanding capabilities on our proposed ITA benchmarks. All scores are reported as accuracy (%). †indicates our framework with only the reasoning stage. Green arrows indicate improvement over the BAGEL baseline*

**理解能力**：在全新提出的 ITA（Image‑Text Alignment）和 VQA 评估体系下（Table 2、Table 3），BAGEL + Ours 的 ITA 总体准确率从 60.60% 升至 73.37%（+12.77），VQA 从 86.48% 升至 89.63%（+3.15）。值得注意的是，完整 R3 带来的理解提升（+12.77 ITA）远超仅推理阶段（BAGEL + Ours† 仅 +1.16），证明反思‑提炼环节是理解能力大幅提升的关键瓶颈。

![[assets/figures/papers/iclr26_0015_1smez00sCm_Understanding_vs._Generation_Navigating_Optimiza/figures/006_Table_2.jpg]]

**与其他 SOTA 的对比**：在 GenEval 基准（Table 8）上，BAGEL + Ours 取得总体 0.96，超越 FlowGRPO（0.95），且在单物体、双物体、颜色等子项上刷新最优。在 TIIF testmini（Table 6）上总体 82.02，与 GPT‑4o（84.19）的差距仅约 2 分。

### 消融分析

**推理阶段与反思‑提炼的分解贡献**  
仅保留推理阶段（BAGEL + Ours†）在生成任务上提升显著（GenEval++ 0.371→0.593），但对 ITA 的提升几乎可忽略（+1.16）。完整的反射‑提炼（Reflect‑Refine）才是解锁理解能力的关键：引入该环节后 ITA 飙升 12.77（Table 2），验证了“理解嵌入生成过程”的因果机制：模型必须在反复评估自身输出与用户意图的对齐程度中主动使用其理解能力，从而对齐优化目标。

**RL 训练的必要性与效率**  
Table 9 对比了未经 RL 的 BAGEL 与 R3 在相同推理策略下的性能。无 RL 时，即使允许多轮反射‑提炼（3‑5 轮），BAGEL 的 GenEval++ 得分仅达 0.439，远低于 R3 在两轮后即收敛至 0.689 的水平。这表明 RL 不仅提升了性能上限，更使模型学会高效利用反思能力、加速收敛，从而在有限迭代次数内达到更优效果（Figure 4 显示 Tree‑RL 策略相比全轨迹 RL 训练奖励更高、方差更低）。

![[assets/figures/papers/iclr26_0015_1smez00sCm_Understanding_vs._Generation_Navigating_Optimiza/figures/019_Table_9.jpg]]
*Table 9: Inference performance on GenEval++ comparison between Bagel and R3 (ours) under same inference strategies*

**训练轨迹长度的影响**  
Table 4 中的消融展示：在推理阶段后添加一轮反射‑提炼（Reason + 1×RR）已接近生成与理解的最优平衡（GenEval++ Val Reward 0.729、ITA 74.49）；继续增加 RR 回合收益递减。这说明单次深度反思即可复用大部分协同增益。

**跨域泛化的局限性**  
Table 5 的跨主题测试显示，在特定类别（如 Counting）上训练后，模型在该类别的测试集表现出色（71.25），但在未见的类别（如 Color）上仅 60.63，逊于全类别训练的结果。这表明当前的理解提升受限于训练数据分布，泛化能力尚未突破类别壁垒。

**推理时迭代轮次的饱和效应**  
Figure 6 展示 GenEval、GenEval++、TIIF 三个基准上性能随最大允许反射‑提炼轮次的演变。R3 模型在任何步数下均优于无反射训练的变体，且在 4‑5 轮后趋于饱和，证明冗余循环收益有限。

### 失败模式与局限性

**过早自我终止**  
模型有时会错误地发出“无需进一步编辑”的终止信号，导致残存错误未能修正。典型例子为文本拼写错误（Figure 11）：初始阶段未能完整渲染指定单词，反思‑提炼阶段虽修正了部分，却过早终止，最终图像仍存在拼写缺陷。该现象表明反思阶段的终止判别置信度仍需校准，是当前可靠性短板。

**跨域理解泛化不足**  
如上所述，理解能力的提升高度依赖训练数据的类别分布，跨类迁移能力有限（Table 5）。这限制了模型在更开放域的真实应用中的鲁棒性。

**计算开销与自适应缓解**  
迭代推理增加推理成本：初始推理约 20–25 秒，每轮反射‑提炼约 25–35 秒（反射 5–10 秒，提炼 20–25 秒，单张 H20 GPU）。然而模型通过训练学会了自适应终止：在 GenEval++ 的测试中，约 45% 的提示无需修改直接完成，26% 仅需 1 轮，14% 需 2 轮，仅约 15% 需要 3 轮以上修饰。故平均开销可控，但最坏情况仍需多轮修正，对实时性要求场景可能存在挑战。

**训练过程动态：生成与理解的协同验证**  
Figure 7 监控了训练过程中生成准确率与 VQA 准确率的演变——两者同步上升，未出现此消彼长的拮抗现象。这直接证实了 R3 将理解内化至生成循环后，两种能力分享共同的优化方向，从训练轨迹上验证了“协同进化”的核心设计目标。

综合来看，R3 通过“推理‑反思‑提炼”多步结构和分阶段 Tree‑RL 奖励，成功将理解与生成的优化对撞转化为互促增益，其代价是额外的推理计算与有限的跨域泛化能力，这些正是后续工作的改进方向。

## 方法谱系与知识库定位

多模态统一模型中，理解能力与生成能力长期被视为两项独立任务。传统方法（如直接将BAGEL微调于单一任务）强化一方能力的同时会系统性地削弱另一方，形成零和式的优化困境。简单多任务共训（naive co‑training）仅能获得边际收益，无法根本解决共享容量下的目标冲突（Figure 1）。R3框架将这一僵局归因于**生成过程的单步前馈结构**：理解仅作为外部评估指标，并未参与生成决策，导致优化信号彼此独立甚至互斥。R3的核心洞察在于将理解能力**嵌入生成循环**——通过“推理‑反思‑提炼”的多步过程，使模型必须主动调用其理解能力来评判并修正自身输出，从而将生成优化目标与理解优化目标自动对齐（core insight，Section 2.1）。这一结构变化本质上将权衡关系转变为协同进化：理解能力的提升直接转化为生成质量的改善，生成过程的优化又反向强化理解能力（Figure 7）。

在方法脉络上，R3对BAGEL基线做出了四个关键设计槽位的修改（changed slots）。**生成过程结构**由单步前向生成改为交替文本与图像的序贯生成序列 $t^{1}, I^{1}, \dots, t^{n}, I^{n} \sim \pi_{\theta}(\cdot | c)$（Section 2.2），其中`Reason`阶段解析意图并合成初始图像，`Reflect`阶段评估对齐程度并生成编辑指令或终止信号，`Refine`阶段执行修正（Figure 2）。**训练策略**则从独立损失或多任务训练转变为树结构强化学习（Tree‑RL）。Tree‑RL通过重要性采样分阶段优化Reason策略与Reflect‑Refine策略，利用阶段奖励替代稀疏的全轨迹奖励，显著缓解长轨迹的高方差问题（Figure 3, Figure 4）；其中文本推理与反射部分采用GRPO，扩散过程采用FlowGRPO及MixGRPO降低计算负担（Section 2.3, A.2）。**奖励设计**引入了分阶段信号：Reason阶段文本的奖励为图像‑文本对齐评分加格式奖励 $r_{j,\text{text}} = V_j + r_{j,\text{format}}$；Reflect阶段奖励为 $\mathbf{C}_j + r_{j,\text{format}}$，Refine阶段奖励为 $\mathbf{C}_j$，其中 $\mathbf{C}_j$ 为改进度量——对不完美图像奖励修正幅度，对已完美图像奖励正确终止（Equation 2, Equation 3）。**理解在生成中的角色**从独立任务转变为生成过程的核心组件：模型必须依赖自身理解能力来评估“当前输出与用户意图是否对齐”，并据此驱动修正（Section 2.1）。这四个变化共同使得生成能力的增强（GenEval++ Overall 从0.371升至0.689）不再以牺牲理解为代价，反而带来理解指标的同步大幅提升（ITA +12.77, VQA +3.15，Table 2, Table 3）。

该方法在生成‑理解协同优化这一目标下展现出明确的适用边界。**任务适用性**：R3在文本到图像的指令跟随场景中有效，其理解能力的提升主要源于反思过程中针对具体语义（计数、空间关系、文本渲染等）的纠错，因此提升幅度具有领域特异性。跨类别泛化实验（Table 5）显示，在Counting类别上训练的模型，在Color类别上仅取得60.63分，说明当前的理解增强依赖训练分布的覆盖，尚未自然泛化为与类别无关的通用理解。**计算代价**：迭代推理引入额外开销：初始Reason阶段耗时20–25秒，每一轮Reflect‑Refine追加25–35秒（含Reflection 5–10秒与Refinement 20–25秒，单张H20 GPU，Appendix A.5）。但模型学会了自适应终止，在GenEval++上约45%的提示在初始生成后即直接结束，平均推理成本可控。**奖励与评估依赖性**：强化学习依赖Qwen‑2.5‑VL‑72B提供标量对齐评分，该奖励模型的偏好可能影响优化方向；论文采用GPT‑4.1与Gemini 2.5 Flash等多方评估验证结果，在一定程度上降低单一标定偏差的风险，但仍需注意奖励模型对最终行为的塑造（Section 2.4）。**框架可扩展性**：R3的范式在迷宫导航等非图像生成任务中已有初步验证（Figure 16），但推广到视频、3D等其它模态的生成任务仍有待系统考察。

局限与开放问题集中在三个层面。**过早终止**：反射过程有时会过早发出“无需修改”信号，导致残余错误未被纠正（如拼写错误，Figure 11）。改进方向在于设计更可靠的终止条件或引入外部验证机制。**泛化性不足**：理解能力的提升高度依赖训练数据的细粒度类别，跨域理解能力仍难以自动涌现（Table 5）。如何通过数据增强或元学习策略培育超越特定训练集的通用视觉理解能力，是当前框架的未解难题。**训练效率**：虽然Tree‑RL和自适应终止分别减缓了训练与推理的方差和开销，但多阶段展开与交替优化仍然需要大量采样。探索更高效的数据策略（如主动采样高价值样本）以及将R3的闭环自优化理念推广至更广泛的多模态生成任务（视频、代码生成等），是实现理解与生成持续共赢的重要开放方向。

## 原文 PDF

![[paperPDFs/ICLR_2026/Understanding_vs_Generation_Navigating_Optimization_Dilemma_in_Multimodal_Models.pdf]]
