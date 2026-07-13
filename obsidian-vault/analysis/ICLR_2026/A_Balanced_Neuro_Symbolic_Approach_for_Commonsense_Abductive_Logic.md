---
title: "A Balanced Neuro-Symbolic Approach for Commonsense Abductive Logic"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/A_Balanced_Neuro_Symbolic_Approach_for_Commonsense_Abductive_Logic.pdf
project_link: null
code_link: null
aliases:
- AARGOS
- BNSACAL
tags:
- ICLR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/language_speech_and_dialog
core_operator: "利用逻辑求解器的反馈（SAT问题骨干集）来引导LLM生成新的常识命题，并迭代地扩充问题，从而将搜索空间从受限的符号空间扩展到更通用的空间。"
primary_logic: "通过将逻辑求解器的骨干集作为搜索线索，可以高效地引导LLM生成与问题相关且符合常识的新命题，从而在保持可承受成本的同时，实现真正的溯因推理。"
claims:
- "我们的方法ARGOS使用逻辑求解器的反馈，以迭代方式用LLM提供的常识关系来增强逻辑问题。"
- "ARGOS可以溯因出问题输入中未实例化的新命题。"
- "我们使用逻辑求解器的反馈（SAT问题骨干集）来引导搜索，这是另一项新颖贡献。"
- "在多个基准测试和大型语言模型上的实验表明，我们的方法在背景信息缺失的溯因推理问题上，显著优于现有的符号和神经方法。"
---

# A Balanced Neuro-Symbolic Approach for Commonsense Abductive Logic

> [!tip] 核心洞察
> 通过将逻辑求解器的骨干集作为搜索线索，可以高效地引导LLM生成与问题相关且符合常识的新命题，从而在保持可承受成本的同时，实现真正的溯因推理。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 面向常识溯因逻辑的平衡神经符号方法 |
| 英文题名 | A Balanced Neuro-Symbolic Approach for Commonsense Abductive Logic |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=RCsBoUr72G) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/language_speech_and_dialog |
| Method | ARGOS (Abductive Reasoning with Generalization Over Symbolics) |
| Dataset | FOLIO, CLUTRR, QUAIL, CosmosQA |

> [!tip] 效果简介
> - FOLIO 上，Accuracy 为 81%，对比 71% (SC)，变化 +10%。
> - CLUTRR 上，Accuracy 为 80%，对比 73% (SC)，变化 +7%。
> - QUAIL 上，Accuracy 为 82%，对比 69% (SC)，变化 +13%。

## 概要

现有神经符号推理系统面临的核心瓶颈是：它们仅支持纯演绎推理，无法处理问题中未明确陈述的常识关系，因此在面对需要溯因推理的现实问题时失效。本文提出的方法ARGOS（Abductive Reasoning with Generalization Over Symbolics）通过一种平衡的神经符号策略来解决这一问题。其核心机制是利用逻辑求解器的反馈——即SAT问题的骨干集（backbone(P) = { L ∈ L | P ⊢ L }）——作为搜索线索，引导大语言模型（LLM）迭代地生成并添加新的常识命题，从而将搜索空间从仅限于问题中已有命题的受限符号空间，扩展到允许引入新变量和新关系的通用空间。

在方法定位上，ARGOS位于纯符号方法（如LLM-Tres、Logic-of-Thought）与纯神经方法（如Chain-of-Thought）之间的平衡点，同时利用逻辑求解器的精确性和LLM的常识灵活性。实验结果表明，该方法在多个需要背景知识溯因的基准测试上显著优于现有基线：在FOLIO上准确率达81%（较最佳基线Self-Consistency提升+10%），在CLUTRR上达80%（+7%），在QUAIL上达82%（+13%），在CosmosQA上达78%（+2%），在ESNLI上达79%（+3%），在ProntoQA上达95%（+2%）。消融研究进一步证实，骨干集追踪、常识评分和相关性评分等组件对整体性能均有贡献。



常识溯因推理——即从观察结果反推出缺失的常识前提——是连接符号逻辑严谨性与自然语言灵活性的关键瓶颈。现有神经符号系统（如 Logic-of-Thoughts、LLM-Tres）仅支持纯演绎推理：它们假设所有必要的前提都已显式给出，推理过程仅限于从已有命题中推导出必然结论。然而，现实问题中大量常识关系并未在问题输入中明确陈述。例如，一个儿童阅读理解问题可能描述“狐狸在冬天变白以吸收阳光”，但未显式说明“白色物体吸收阳光”这一常识规则。面对此类缺失，纯演绎系统无法生成任何新命题，因而失效。

**核心瓶颈**在于搜索空间的根本受限性。现有符号方法（如 SAT-LM）的搜索空间仅限于问题中已出现的命题或可演绎出的子句，无法引入新变量或新关系。纯神经方法（如 Chain-of-Thought）虽能利用 LLM 的内部知识，但缺乏对逻辑一致性的保证，且容易产生幻觉性推理链。Figure 2 将现有方法定位在“符号-语言谱系”上：纯符号方法（LLM-Tres）位于极左端，纯语言方法（COT）位于极右端，而本文提出的 ARGOS 试图在两者之间找到平衡点。

**本文动机**是设计一种能够进行真正溯因推理的神经符号方法，即能够生成问题中未实例化的新命题，同时保持逻辑求解器的精确性。核心洞察在于：逻辑求解器在无法求解问题时，会返回一个**骨干集**（backbone），即所有被前提蕴涵的文字集合（$backbone(P) = \{ L \in L \mid P \vdash L \}$）。骨干集揭示了当前逻辑空间中“已知”与“未知”的边界，可以作为引导 LLM 搜索常识假设的高效线索。Figure 3 展示了这一迭代流程：系统交替使用 SAT 求解器（验证逻辑可解性）和 LLM（基于骨干集生成候选常识规则），并通过常识评分和相关性评分过滤噪声，逐步扩充问题直至可解。

与现有工作的关键区别在于搜索策略的转变：从“在固定符号空间内穷举或演绎”变为“利用骨干集反馈动态引导 LLM 生成新命题”。这使得 ARGOS 能够将搜索空间从受限的符号空间扩展到更通用的语义空间，同时通过逻辑求解器的反馈机制控制搜索成本。



## 核心方法与创新机理

ARGOS（Abductive Reasoning with Generalization Over Symbolics）的核心创新在于将神经符号系统的推理模式从**纯演绎扩展为演绎+溯因**，从而解决了现有系统在面对缺失常识的现实问题时完全失效的根本瓶颈。

**瓶颈与因果机制。** 现有神经符号方法（如SAT-LM、Logic-of-Thoughts）的搜索空间被严格限定在问题中已出现的命题或可演绎出的子句内，仅支持“前提→结论”的演绎推理。但现实溯因问题往往缺失关键的常识背景——例如，一个关于狐狸冬天变白的问题中，需要“白色吸收阳光少”这一未出现在输入中的常识才能推导出答案。ARGOS的因果机制是：利用逻辑求解器的反馈（SAT问题的骨干集 `backbone(P) = { L ∈ L | P ⊢ L }`）作为搜索线索，引导LLM生成与当前逻辑上下文相关且符合常识的新命题，从而**将搜索空间从受限的符号空间扩展到包含新变量、新关系的通用空间**。

**三个关键改变量：**
1. **搜索空间（Search Space）**：基线方法（如LLM-Tres、Logic-of-Thoughts）仅允许在问题中已出现的命题或可演绎子句内搜索；ARGOS允许LLM生成包含**全新变量和任意形式**的命题（`can abduce propositions not previously instantiated in the input problem`）。
2. **搜索策略（Search Strategy）**：基线采用穷举搜索或纯LLM提示；ARGOS使用逻辑求解器的骨干集反馈来优先选择与问题中其他文字共享最多实体的文字作为前件，从而高效缩小搜索范围（`we guide the search using feedback from the logic solver in the form of the SAT problem backbone`）。
3. **推理模式（Reasoning Mode）**：基线为纯演绎推理；ARGOS结合了演绎（逻辑求解器）和溯因（LLM生成缺失常识），形成迭代增强循环——先尝试用SAT求解器证明或证伪，失败后由LLM生成新常识命题，再重新尝试求解。

**证据强度与验证。** 论文通过三个层面的消融实验验证了这些创新的必要性：(1) 同时消融评分和骨干追踪导致FOLIO L8B准确率从81%降至76%（Table 2）；(2) 消融SC求解器（仅用符号求解）导致准确率暴跌至59%（Table 4）；(3) 消融常识评分或上下文相关性评分阈值均导致性能下降至79%（Table 5）。在CLUTRR上，ARGOS从未将正确预测翻转为错误预测（`never corrupts a problem`），且为65%的问题识别了重要的新变量。这些证据表明，骨干集引导的LLM搜索是性能提升的关键机制，而非简单的模型集成。

**失败模式与局限。** 该方法存在三个已知弱点：(1) 仅限于生成最多两个文字作为前件的规则，无法处理需要更多前件的复杂命题；(2) 需要访问LLM的logit级输出，排除了闭源模型（如GPT-4）的使用；(3) 当问题前提与常识相矛盾时（如将Fido归类为猫），ARGOS可能被混淆——这源于常识评分器仅76%的准确率和上下文相关性评分器91%的准确率。这些局限暗示了未来改进方向：将评分系统从logit-based转换为verbalized以避免模型限制，以及探索反向链式推理以更直接地生成与目标相关的命题。



![[assets/figures/papers/iclr26_0001_RCsBoUr72G_A_Balanced_Neuro-Symbolic_Approach_for_Commonsen/figures/004_Figure_4.jpg]]
*Figure 4: Overview of ARGOS with the winter fox example. We iteratively add to the logic problem and query a logic solver to look for conflicts within the backbone compared to the query. Eventually, we find that absorbs(white, sun) is F alse, contradicting the query*

ARGOS（Abductive Reasoning with Generalization Over Symbolics）是一个迭代式的神经符号推理框架，其核心设计目标是将逻辑求解器的精确性与LLM的常识生成能力结合，以解决传统符号系统无法处理的溯因推理问题。整体pipeline可概括为：**在循环中交替使用符号求解器与LLM，逐步用LLM生成的常识命题扩充逻辑问题，直至问题可解**。

**模块关系与输入输出流：**

1. **输入**：一个命题逻辑问题，由前提集 $P$、查询命题 $Q$ 和初始为空的常识命题集 $C = \{\}$ 构成。输入的一阶逻辑问题需先通过全称量词展开（$\forall x F(x) \to (F(A) \land F(B) \land \dots)$）和存在量词展开（$\exists x F(x) \to (F(A) \lor F(B) \lor \dots)$）实例化为命题逻辑形式。

2. **主循环（迭代引擎）**：算法进入迭代，每次迭代执行三个核心步骤，如图3所示（Figure 3: ARGOS at a glance）：
   - **步骤B（并行求解尝试）**：同时调用两个求解器：
     - **SAT求解器（sat_solve）**：测试 $(P \land C) \vdash Q$ 或 $(P \land C) \vdash \lnot Q$ 是否成立。若成立，则问题已解，输出答案并终止。若不成立，则返回骨干集 $B = \{ L \in L \mid P \vdash L \}$，即由前提 $P$ 蕴涵的所有文字的集合（骨干集定义：$backbone(P) = \{ L \in L \mid P \vdash L \}$）。
     - **LLM求解器（llm_solve）**：使用k-shot自一致性（$k=5$）尝试求解问题，输出答案 $a^*$ 和置信度分数 $c^* = \frac{1}{5} \sum_{i=1}^{5} c_i \mathbb{1}[a_i = a^*]$。
   - **步骤C（常识命题生成与筛选）**：若两个求解器均未达成一致结论，则进入生成阶段：
     - **前件选择**：从骨干集 $B$ 中选取一对文字（literal）作为前件 $L_1 \land L_2$，优先选择与问题中其他文字共享最多实体的文字对。
     - **后件生成（llm_generate）**：提示LLM为 $L_1 \land L_2$ 生成后件文字 $L_{right}$，形成规则 $L_1 \land L_2 \to L_{right}$。
     - **双评分过滤**：
       - **常识评分（llm_commonsense_score）**：评估生成的规则是否符合常识（准确率约76%）。
       - **上下文相关性评分（llm_relevance_score）**：评估规则是否与当前问题上下文相关（准确率约91%），基于logits计算“Yes”token的概率：$P[\text{Yes}] = \exp(\logit_{\mathrm{Yes}}) / (\exp(\logit_{\mathrm{Yes}}) + \exp(\logit_{\mathrm{No}}))$。
     - **命题加入**：仅当规则同时通过两个评分阈值时，才将其加入常识集 $C$。
   - **阈值衰减**：每次迭代将自一致性阈值 $\gamma$ 减少固定量 $\alpha$（实验中 $\alpha = 0.1$）：$\gamma \leftarrow \gamma - \alpha$，以逐步降低对LLM求解置信度的要求。

3. **终止条件**：当SAT求解器成功推导出 $Q$ 或 $\lnot Q$，或LLM求解器的置信度 $c^* \geq \gamma$ 时，算法终止并输出答案。最大COT调用次数上界为 $cost < k \cdot (\gamma - 0.5) / \alpha$（其中 $k=5$，$\gamma$ 初始为1，$\alpha=0.1$），在实验中平均每次问题调用18.4次COT（Table 3），低于纯自一致性（SC）的20次。

**关键设计因果机制**：骨干集是连接符号求解器与LLM生成器的桥梁。SAT求解器无法解决原问题时，其输出的骨干集提供了“哪些文字已被前提蕴涵”的结构化信息，LLM据此生成的新命题天然与问题逻辑骨架相关，从而将搜索从受限的符号空间扩展到更通用的常识空间。图4（Figure 4: Overview of ARGOS with the winter fox example）展示了这一过程：通过迭代添加常识命题（如“白色物体吸收阳光为假”），最终在骨干集中发现与查询的矛盾，从而推导出答案。

**证据强度**：所有pipeline模块的定义、输入输出关系和迭代机制均有明确的原文锚点支撑（Section 4.1 ALGORITHM, Figure 3, 公式定义），置信度为1.0。但常识评分和相关性评分的准确率（76%和91%）来自附录F.5，属于消融实验中的辅助证据，置信度设为0.95。



ARGOS（Abductive Reasoning with Generalization Over Symbolics）的核心创新在于将符号逻辑求解器的确定性反馈与LLM的常识生成能力相结合，通过迭代式问题扩充实现溯因推理。其整体流程如**Figure 3**所示：给定一个命题逻辑问题，系统反复尝试用SAT求解器和LLM（5-shot自一致性）求解；若均失败，则利用求解器的反馈（骨干集）引导LLM生成新的常识命题，经筛选后加入问题集，直至可解。

### 1. 问题形式化与骨干集

ARGOS处理的问题被形式化为一个命题逻辑三元组 `(P, Q, C)`，其中 `P` 为前提集，`Q` 为查询命题，`C` 为常识命题集（初始为空）。一阶逻辑输入通过全称量词实例化 `∀x F(x) → (F(A) ∧ F(B) ∧ ...)` 和存在量词实例化 `∃x F(x) → (F(A) ∨ F(B) ∨ ...)` 转换为命题逻辑。

**骨干集（Backbone）** 是ARGOS引导搜索的核心线索，定义为由前提 `P` 蕴涵的所有文字（literal）的集合：
```
backbone(P) = { L ∈ L | P ⊢ L }
```
该集合由SAT求解器在尝试求解时返回，其关键特性是：骨干集中的文字是逻辑上必然成立的，因此任何与骨干集矛盾的假设都会导致问题不可解。ARGOS利用这一特性，优先选择骨干集中的文字作为新命题的前件，确保新增命题与已有前提的逻辑一致性。

### 2. 迭代式命题生成与筛选

当SAT求解器和LLM均无法确定 `(P ∧ C) ⊢ Q` 或 `(P ∧ C) ⊢ ¬Q` 时，ARGOS进入命题生成阶段。该阶段包含三个核心模块：

**（1）前件选择与后件生成（`llm_generate`）**：从骨干集中选取两个文字 `L₁` 和 `L₂` 作为前件，提示LLM生成一个后件文字 `L_right`，形成规则 `L₁ ∧ L₂ → L_right`。选择策略优先考虑与问题中其他文字共享最多实体的文字，以最大化新命题的相关性。

**（2）常识评分（`llm_commonsense_score`）**：评估生成的规则是否符合常识。LLM被提示判断 `L₁ ∧ L₂ → L_right` 是否“看起来正确”，输出二分类结果。实验表明该分类的准确率为76%。

**（3）上下文相关性评分（`llm_relevance_score`）**：评估生成的规则是否与当前问题上下文相关。LLM基于前提 `P` 和已有常识 `C`，判断新规则是否“上下文相关”。该分类的准确率为91%。相关性概率通过logits计算：
```
P[Yes] = exp(logit_Yes) / (exp(logit_Yes) + exp(logit_No))
```

只有同时通过常识和相关性阈值的规则才会被加入 `C`。消融实验（**Table 5**）显示，移除任一评分阈值均会导致FOLIO L8B上的性能下降（从81%降至79%），验证了双重筛选的必要性。

### 3. 自一致性求解与置信度衰减

ARGOS使用5轮自一致性（`llm_solve`）作为神经求解器。每轮COT生成一个答案 `a_i` 及其置信度 `c_i`。最终答案 `a*` 为最常见的答案，其总置信度分数为：
```
c* = (1/5) * Σ_{i=1}^{5} c_i * 𝟙[a_i = a*]
```

算法引入**自一致性阈值衰减**机制：初始阈值 `γ = 1`，每次迭代减少固定量 `α = 0.1`：
```
γ ← γ - α
```
这意味着随着迭代进行，LLM求解器对答案的置信度要求逐渐放宽，允许在后续迭代中接受原本置信度不足的答案。该机制确保了算法不会因初始求解失败而过早终止。

### 4. 成本上界

ARGOS的COT调用次数上界由阈值衰减机制保证：
```
cost < k * (γ - 0.5) / α
```
其中 `k = 5`（自一致性轮数），`γ` 初始为1，`α = 0.1`。代入得 `cost < 25`，即最多需要25次COT调用。实验（**Table 3**）显示，ARGOS在Llama 8B上的平均COT调用次数为18.4，低于纯自一致性的20次，验证了其成本可控性。

### 5. 关键设计原理

**命题1（溯因逻辑问题的良定义性）**：设 `P` 为前提集，`Q` 为查询命题，`C₁` 和 `C₂` 为两个不同的常识命题子集。若 `(P ∧ C₁) ⊢ Q` 且 `(P ∧ C₂) ⊢ ¬Q`，则 `L₁ ↔ L₂` 必然成立。该命题保证了溯因推理的解不依赖于常识集的选择——任何两个导致不同结论的常识集必然逻辑等价，从而确保了ARGOS生成的常识命题不会引入矛盾。

**骨干集引导搜索的因果机制**：传统符号方法（如SAT-LM）仅在已有命题空间内演绎，无法引入新变量。ARGOS通过骨干集将搜索限制在逻辑必然成立的文字上，确保LLM生成的新命题（可能包含新变量）与前提一致。**Figure 9**显示，在CLUTRR上ARGOS的置信度波动显著，表明新命题确实改变了问题的逻辑结构。消融实验（**Table 2**）表明，同时移除评分和骨干追踪会导致FOLIO L8B性能从81%降至76%，验证了骨干集引导的有效性。

**需要人工验证的要点**：论文声称“ARGOS-L8B在85%的情况下添加了生成忠实证明所需的信息”，但该数据来自附录D，且置信度为0.95。此外，常识评分76%的准确率意味着约1/4的新增规则可能不符合常识，其影响程度需进一步分析。



## 实验与关键发现

### 主要结果

ARGOS在六个基准数据集上的二分类准确率（True/False）均超越了所有基线方法（Table 1）。以Llama3-8B为骨干模型时，ARGOS在FOLIO上达到81%的准确率，比最佳纯神经基线Self-Consistency (SC) 的71%高出10个百分点；在CLUTRR上达到80%（SC: 73%，+7%）；在QUAIL上达到82%（SC: 69%，+13%）。在CosmosQA和ESNLI上，ARGOS的绝对提升较小（分别为+2%和+3%），但仍保持最优。在严格演绎推理基准ProntoQA上，ARGOS达到95%（SC: 93%，+2%），表明方法在不需要额外常识的问题上不会退化。所有最优结果的统计显著性均通过Wilcoxon配对秩检验确认（p < 0.005），括号内附有95%置信区间。

![[assets/figures/papers/iclr26_0001_RCsBoUr72G_A_Balanced_Neuro-Symbolic_Approach_for_Commonsen/figures/007_Table_1.jpg]]
*Table 1: Binary classification accuracy (True/False) of all methods on the datasets, using the chosen language models. Bolded text indicates that the method has the best performance, and that its performance is better than the next-best-performing method in a statistically significant way (p-value \< 0.005 according to a Wilcoxon pair-wise rank test). Small-font numbers to the right indicate the bounds of the 95% confidence interval, derived via a bootstrap approach. RQ1: How useful are the scoring and backbone-tracking elements? In Table 2, we test the importance of two elements of ARGOS: (i) score thresholding and (ii) backbone computation. The ablation of each element in isolation results in a dec...*

**机制分析**：ARGOS在FOLIO和QUAIL上的大幅提升直接验证了其核心瓶颈——现有神经符号系统无法处理缺失的常识关系。FOLIO的溯因变体通过人工标注移除了关键常识规则，而QUAIL的逻辑结构虽简单但语言形式不规则，两者恰好暴露了纯神经推理（SC）和纯符号演绎（SAT-LM, LOT）的共同短板。ARGOS通过迭代引入LLM生成的常识命题，填补了这些缺失关系。CosmosQA和ESNLI上较小的提升则表明，这些数据集的问题大多已被SC正确解决，ARGOS的额外搜索空间贡献有限。

### 消融研究

消融实验在FOLIO L8B上系统分解了ARGOS各组件的贡献（Table 2, 4, 5）。

![[assets/figures/papers/iclr26_0001_RCsBoUr72G_A_Balanced_Neuro-Symbolic_Approach_for_Commonsen/figures/008_Table_2.jpg]]

1. **骨干追踪与评分的联合贡献**：同时移除常识评分、上下文相关性评分和骨干追踪后，性能从完整ARGOS的81%下降至76%（Table 2）。这表明骨干集引导的搜索策略和双重评分过滤各自贡献了约2-3%的增益，且存在协同效应。

2. **SC求解器的必要性**：消融SC求解器（仅保留符号求解，记为ARGOS-Symbolic）导致性能骤降至59%（Table 4），远低于完整ARGOS的81%和SC的71%。这揭示了一个关键失败模式：当LLM生成的常识命题不足以让SAT求解器直接推导出结论时，ARGOS必须依赖SC作为回退机制。59%的准确率甚至低于纯神经的SC，说明符号求解器在缺失常识的问题上几乎完全失效，而ARGOS-Symbolic新增的命题若未被SC验证，反而可能引入噪声。

![[assets/figures/papers/iclr26_0001_RCsBoUr72G_A_Balanced_Neuro-Symbolic_Approach_for_Commonsen/figures/012_Table_4.jpg]]
*Table 4: Ablating the SC-solver on ARGOS. ARGOS-Symbolic denotes the ablated version of ARGOS*

3. **评分阈值的独立贡献**：消融常识评分阈值或上下文相关性阈值各导致性能下降约2%（79% vs 81%，Table 5）。这表明两个评分维度互补：常识评分确保命题在语义上合理（准确率76%），上下文评分确保命题与当前逻辑结构相关（准确率91%）。单独移除任一评分都会让低质量命题进入搜索空间，但影响有限，因为另一评分仍可过滤部分噪声。

![[assets/figures/papers/iclr26_0001_RCsBoUr72G_A_Balanced_Neuro-Symbolic_Approach_for_Commonsen/figures/013_Table_5.jpg]]
*Table 5: Ablating individual score thresholds*

### 失败模式与证据强度

**核心失败模式**：ARGOS的局限性直接源于其设计假设。首先，它只能生成最多两个文字作为前件的规则，无法处理需要三个或更多前件的复杂命题——这在实际常识中常见（如“如果下雨且没带伞且离商店远，则会淋湿”）。其次，当问题前提与常识相矛盾时（例如，Table 12-14中的示例：Fido被定义为猫而非狗，Detroit City被定义为马而非城市），LLM的常识评分会与问题上下文冲突，导致ARGOS生成误导性命题或无法收敛。第三，方法依赖LLM的logit级输出来计算评分，排除了GPT-4等闭源模型。

**证据强度**：主要结果（Table 1）和消融实验（Table 2, 4, 5）的置信度均为1.0，数据直接来自论文。但以下两点需手动验证：（1）消融SC求解器实验（Table 4）的置信度为0.95，因为论文未明确说明该实验是否在所有数据集上重复；（2）ARGOS在CLUTRR上“从未破坏问题”（即从不将正确预测翻转为错误）的断言（置信度1.0）仅基于Figure 5(a)的可视化计数，未提供具体数值表格，建议核实原始图表。

### 成本与效率

ARGOS以增加计算成本换取性能提升。在Llama3-8B上，ARGOS平均每次问题需18.4次COT调用（Table 3），低于SC的20次，但远高于COT的1次。成本上界由公式 `cost < k * (γ - 0.5) / α` 给出（k=5, γ初始=1, α=0.1），即最大约25次COT调用。Figure 7的直方图显示，CLUTRR上大部分问题的成本集中在5-15次COT之间，少数困难问题接近上界。**关键洞察**：ARGOS的计算成本并非均匀分布——它自动将更多计算分配给更难的问题（需要更多迭代的问题），而简单问题（如CosmosQA上大部分已被SC解决）仅需1-2次迭代即退出（Figure 8）。这种自适应分配是效率的核心，但代价是每次迭代需额外调用LLM进行命题生成和双重评分。

![[assets/figures/papers/iclr26_0001_RCsBoUr72G_A_Balanced_Neuro-Symbolic_Approach_for_Commonsen/figures/010_Table_3.jpg]]
*Table 3: Average number of COT calls required by each method*

### 可解性进展分析

Figure 8-10展示了ARGOS在三个数据集上的置信度变化轨迹。在CosmosQA上（Figure 8），SC初始置信度已较高，ARGOS在少量迭代后即退出，且置信度变化平缓。在CLUTRR上（Figure 9），置信度出现显著波动和翻转，表明ARGOS添加的命题确实改变了问题的逻辑结构——这正是其设计目标。在QUAIL上（Figure 10），尽管最终准确率提升最大（+13%），但迭代次数反而较少。论文解释为QUAIL的逻辑结构虽模糊但简单，少量精心选择的命题即可解决问题。**一个未解决的关键问题**：ARGOS在QUAIL上为何能以更少迭代实现更大提升？这暗示其性能提升可能部分来自SC回退机制本身（即LLM在修正后的上下文中直接推理正确），而非符号求解器的推导。需要进一步分析每次迭代中符号求解和SC求解各自的贡献比例。



## 定位与知识库关联

ARGOS（Abductive Reasoning with Generalization Over Symbolics）的定位可以放在一个“符号-语言推理谱系”（Figure 2）中理解。该谱系的一端是完全基于符号逻辑演绎的方法（如LLM-Tres和Logic-of-Thought），另一端是纯神经的语言链式推理（如Chain-of-Thought, COT）。ARGOS位于两者之间：它保留了SAT求解器进行精确的演绎推理（这是纯神经方法缺失的），同时利用LLM生成新的常识命题，从而突破了纯符号方法“仅能处理问题中已显式出现的命题”这一根本限制。这种设计直接回应了现有神经符号系统仅支持纯演绎推理、无法处理未明确陈述的常识关系的瓶颈。

**与基线方法的关系：** 实验对比了五类基线。纯神经基线（COT, Self-Consistency SC）完全依赖LLM的隐式知识进行推理，在需要背景常识的溯因问题上表现受限。符号方法基线（SAT-LM, LOT, LLM-Tres）将推理负担卸载给SAT求解器，但搜索空间被严格限制在问题中已出现的命题或可演绎出的子句内。ARGOS的关键改变在于两个槽位：（1）**搜索空间**从“仅限于问题中已出现的命题”扩展到“允许LLM生成包含新变量和新关系的任意形式命题”；（2）**搜索策略**从“穷举搜索或基于LLM的提示”变为“使用逻辑求解器的骨干集反馈来引导搜索”。具体地，ARGOS利用SAT求解器返回的骨干集 $backbone(P) = \{ L \in L \mid P \vdash L \}$ 作为线索，优先选择与问题中其他文字共享最多实体的文字作为前件，再交由LLM生成后件。这种引导机制是论文宣称的另一项新颖贡献。

**适用边界与性能增益：** 在六个基准测试上的二分类准确率结果（Table 1）显示，ARGOS在需要大量背景常识的溯因推理问题上提升显著：QUAIL提升+13%（82% vs 69% SC），FOLIO提升+10%（81% vs 71% SC），CLUTRR提升+7%（80% vs 73% SC）。而在逻辑结构更简单或LLM本身已能较好处理的数据集上（如ProntoQA +2%，CosmosQA +2%，ESNLI +3%），增益较小。消融实验（Table 2, 4, 5）进一步揭示了各组件的贡献：同时消融评分和骨干追踪导致FOLIO准确率从81%降至76%；消融SC求解器（仅保留符号求解）导致性能骤降至59%，说明LLM的神经推理能力是最终预测的关键补充；消融常识评分或上下文相关性评分阈值各导致约2%的性能下降。在CLUTRR上，ARGOS从未将正确预测翻转为错误预测（Figure 5a），且在Llama 8B上为65%的问题识别了重要新变量，表明其引入的命题整体上是有效的。

**局限与开放问题：** 论文明确承认了若干限制。首先，ARGOS仅限于生成最多两个文字作为前件的规则，无法处理需要更多前件的复杂命题。其次，方法有时依赖自一致性（SC）来解决问题，而SC可能产生不忠实或幻觉性的推理链，从而影响最终预测。第三，方法需要访问LLM的logit级输出（用于计算置信度和相关性概率 $P[Yes] = \exp(\logit_{\mathrm{Yes}}) / (\exp(\logit_{\mathrm{Yes}}) + \exp(\logit_{\mathrm{No}}))$），这排除了闭源模型（如GPT-4）的使用。第四，当问题前提与常识相矛盾时（例如，Fido通常被认为是狗的名字，但问题中将其归类为猫），ARGOS可能会被混淆。此外，常识评分和相关性评分依赖于LLM的判断，其准确性有限（常识分类准确率76%，上下文相关性分类准确率91%）。

从这些局限出发，论文提出了几个开放问题：（1）如何将评分系统从基于logit的转换为基于文本的，以避免需要logit级访问？（2）如何将反向链式推理方法应用于溯因推理，以更直接地生成与目标相关的命题？（3）如何处理无法分解为较小规则的多文字命题公式？（4）ARGOS在非严格逻辑结构的数据集（如CosmosQA和QUAIL）上的性能提升机制是什么？（5）如何进一步降低ARGOS的计算成本，使其在更复杂的现实问题上具有实用性？这些问题的解决将决定该技术谱系从实验基准向实际应用迁移的可行性。



## 原文 PDF

PDF 文件：paperPDFs/ICLR_2026/A_Balanced_Neuro_Symbolic_Approach_for_Commonsense_Abductive_Logic.pdf

![[paperPDFs/ICLR_2026/A_Balanced_Neuro_Symbolic_Approach_for_Commonsense_Abductive_Logic.pdf]]
