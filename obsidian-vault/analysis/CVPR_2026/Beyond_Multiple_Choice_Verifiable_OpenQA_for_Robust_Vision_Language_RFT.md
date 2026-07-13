---
title: "Beyond Multiple Choice: Verifiable OpenQA for Robust Vision-Language RFT"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/Beyond_Multiple_Choice_Verifiable_OpenQA_for_Robust_Vision_Language_RFT.pdf
project_link: "https://flageval-baai.github.io/ReVeL/"
code_link: null
aliases:
- RRVBL
- BMCVORVLR
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: 选项的存在与否——将MCQA改写为去除选项依赖的开放问答（OpenQA），同时保留可验证性，是消除评估失真和训练偏差的关键操控变量。
primary_logic: ReVeL通过将MCQA问题按答案类型分为四类（数值型、关键词型、逐选项验证型、开放型），分别设计改写策略将其转换为确定性可验证的开放格式。这种混合验证设计使70%-96%的题目可通过规则自动判分，既消除了选项带来的评估失真，又大幅降低了纯LLM评判的成本和方差，同时为RFT提供了更稳健、可迁移的奖励信号。
claims:
- 在开放域基准上添加选项后，模型准确率显著超过开放域基线及随机猜测上界，证明选项提供了大量额外信号
- 在MCQA数据上进行RFT会提高选择题分数但损害开放域表现，扩大MCQA与OpenQA之间的差距
- ReVeL训练使OpenQA准确率提升约6个百分点，同时保持MCQA分数竞争力，整体得分超过多个开源RFT模型
- 从MCQA切换到OpenQA后，包括GPT-5在内的最强模型也出现大幅准确率下降（MMMU上GPT-5下降19.8个百分点），揭示了MCQA普遍存在分数虚高
---

# Beyond Multiple Choice: Verifiable OpenQA for Robust Vision-Language RFT

> [!tip] 核心洞察
> ReVeL通过将MCQA问题按答案类型分为四类（数值型、关键词型、逐选项验证型、开放型），分别设计改写策略将其转换为确定性可验证的开放格式。这种混合验证设计使70%-96%的题目可通过规则自动判分，既消除了选项带来的评估失真，又大幅降低了纯LLM评判的成本和方差，同时为RFT提供了更稳健、可迁移的奖励信号。

| 字段 | 内容 |
|------|------|
| 中文题名 | 超越选择题：面向鲁棒视觉语言强化微调的可验证开放问答 |
| 英文题名 | Beyond Multiple Choice: Verifiable OpenQA for Robust Vision-Language RFT |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2511.17405) · [Project](https://flageval-baai.github.io/ReVeL/) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/image_and_video_generation |
| Method | ReVeL (Rewrite and Verify by LLM) |
| Dataset | EMMA / MMMU / MME-RealWorld / MMLU-Pro（四项基准综合）, 四项基准上OpenQA准确率平均提升, ReVeL评判准确率 vs 纯LLM Judge, MMMU（MCQA→OpenQA降幅） |

> [!tip] 效果简介
> - EMMA / MMMU / MME-RealWorld / MMLU-Pro（四项基准综合） 上，Overall Score（MCQ+Open综合得分） Qwen2.5-VL-7B + OpenQA (ReVeL): 40.4 vs Qwen2.5-VL-7B + MCQA (ViRL): 36.3 (+4.1)。
> - 四项基准上OpenQA准确率平均提升 上，OpenQA Accuracy 约+6个百分点 vs MCQA训练 (+6pp)。
> - ReVeL评判准确率 vs 纯LLM Judge 上，Overall Judging Accuracy ReVeL: 98.5% vs LLM Judge: 97.3% (GPT-4.1 mini) (+1.2pp, FPR从2.0%降至0.3%)。

## 概要

视觉语言模型（VLM）的评估与强化微调（RFT）长期依赖多项选择题（MCQA）格式。然而，MCQA中的选项为模型提供了可利用的捷径信号：模型可以通过选项间的相对比较、位置记忆和排除法猜出正确答案，而非依赖真正的知识或推理能力。这种**选项依赖性**导致两个严重后果：其一，MCQA评估指标系统性虚高，相对开放域评估（OpenQA）最高可达20个百分点；其二，在RFT过程中，模型利用选项捷径的行为被作为正奖励信号强化，进一步损害开放域泛化能力，拉大MCQA与OpenQA之间的表现差距。

针对这一瓶颈，本文提出 **ReVeL（Rewrite and Verify by LLM）** 框架，核心操控变量是**选项的存在与否**——将MCQA改写为去除选项依赖的开放问答（OpenQA），同时保留答案的可验证性。ReVeL按答案类型将MCQA问题分为四类（数值型、关键词型、逐选项验证型、开放型），分别设计改写策略将其转换为确定性可验证的开放格式。这一混合验证设计使70%–96%的题目可通过规则自动判分，既消除了选项带来的评估失真，又大幅降低了纯LLM评判的成本和方差，同时为RFT提供了更稳健、可迁移的奖励信号。

实验证据支撑了这一方案的有效性：在MCQA数据上进行RFT会提升选择题分数但损害开放域表现（MMMU上3B和7B模型的MCQA-OpenQA差距均扩大）；而使用ReVeL改写后的OpenQA数据进行训练，使OpenQA准确率平均提升约6个百分点，同时MCQA分数保持竞争力，整体得分（40.4）显著超过MCQA训练基线（36.3）。大规模评估进一步揭示，从MCQA切换到OpenQA后，包括GPT-5在内的最强模型也出现大幅准确率下降（MMMU上GPT-5下降19.8个百分点），表明MCQA分数虚高是一个普遍性挑战，而非仅影响特定模型。



### 选择题评估的隐性代价

视觉语言模型的评测长期依赖多项选择题（MCQA）范式。这种格式因判分简便、可规模化而成为主流，但其背后隐藏着一个根本性问题：**选项为模型提供了可利用的捷径信号**。模型可以通过选项间的相对比较、位置记忆和排除法猜出正确答案，而非依赖真正的知识或推理能力。

Figure 1 直观展示了这一脆弱性：一条不忠实的推理链错误地排除了干扰项，却恰好给出了正确的最终答案。在强化微调（RFT）中，这种“正确但不可靠”的输出会被赋予正向奖励信号，从而进一步放大捷径行为，拉大MCQA与开放域评估之间的鸿沟。

### 选项虚高：从开放域到选择题的分数膨胀

论文通过一个关键实验量化了选项带来的评估失真。在 SimpleQA 和 Visual SimpleQA 等开放域基准上，为每个问题添加6个选项构造MCQA版本后，无论是开源模型还是商业模型，准确率均出现一致且显著的增长，远超随机猜测理论上界。

随机猜测上界定义为：

$$Acc_{UB} = Acc_{Open} + (1 - Acc_{Open}) \times \frac{1}{K}, \quad K = 6$$

该上界结合了模型在开放域上的实际正确率和对剩余题目从K个选项中随机猜对的概率。Figure 2 显示，模型在MCQA上的实际得分不仅超过开放域基线，还大幅超越这一理论上界——这意味着模型并非在“知道答案时答对、不知道时随机猜”，而是在大量情况下**利用了选项中的额外信息**来完成作答。

进一步地，当从MMMU等视觉问答基准中直接移除选项后（Figure 4），所有模型的准确率一致下降，在视觉问答任务上尤为明显。这揭示了一个令人不安的事实：**MCQA评估指标中存在最高可达20个百分点的分数虚高**。

### RFT中的奖励信号污染

选项依赖不仅影响评估，更在强化微调中构成系统性偏差。Table 2 展示了在ViRL的MCQA数据上进行RFT的结果：MCQA分数确实提升，但开放域表现反而下降，MCQA与OpenQA之间的差距（∆）从+4.5扩大至+9.1。这表明，**MCQA格式下的可验证奖励可能过拟合于选项特定的启发式策略，而非可迁移的推理能力**。

更深层的证据来自选项锚定现象（Figure 7）。当“蛋彩画”作为可用选项时，模型会分析画作的哑光表面和细腻色彩，推断其符合蛋彩画特征；但当该选项被替换为“以上皆非”后，同一模型面对同一幅画作，推理方向却转向描述其纹理和细节“符合油画特征”。这种推理随选项变化而漂移的行为，直接证明了模型并非基于客观事实进行推理，而是在选项空间中寻找最匹配的锚点。

### 从MCQA到OpenQA的根本挑战

将MCQA转换为开放问答（OpenQA）是消除选项依赖的直接思路，但面临两个核心障碍：其一，并非所有MCQA问题都适合直接转为开放格式——某些问题天然依赖选项间的对比关系；其二，开放格式的判分通常需要LLM评判，成本高且存在位置偏差、评判不一致等固有问题。

GPT-5在MMMU基准上从MCQA切换到OpenQA后准确率下降19.8个百分点（从79.2%降至59.5%），InternVL3-8B更是骤降27.9个百分点（Table 7）。这一结果揭示了OpenQA挑战的普遍性——即便是最先进的模型，其看似优异的MCQA成绩也在很大程度上依赖于选项信号。

### 本文动机

基于上述分析，论文的核心动机可概括为三点：

1. **评估失真**：MCQA的选项为模型提供了可利用的捷径，导致评估指标系统性地高估模型真实能力。
2. **训练偏差**：在RFT中将选项利用行为作为正奖励信号强化，会损害模型的开放域泛化能力。
3. **判分困境**：直接转向OpenQA需要LLM评判，引入高成本、高方差和位置偏差等问题。

因此，本文提出ReVeL框架，通过将MCQA问题按答案类型分类并分别设计改写策略，在保留可验证性的前提下消除选项依赖，从而对齐评估与训练的信号来源。



## 核心方法与创新机理

### 问题根源：MCQA格式的选项依赖性

当前视觉-语言模型的评测与强化微调（RFT）普遍依赖多选题（MCQA）格式，但这一格式存在根本性缺陷：**选项本身为模型提供了可利用的捷径信号**。模型可以通过选项间的相对比较、位置记忆和排除法猜出正确答案，而非依赖真正的知识或推理能力。

这一问题的因果机制体现在三个层面：

1. **评估失真**：在开放域基准（如SimpleQA、Visual SimpleQA）上添加选项后，模型准确率显著超过开放域基线及随机猜测上界（Figure 2），证明选项提供了大量额外信号。随机猜测上界公式为：
   $$Acc_{UB} = Acc_{Open} + (1 - Acc_{Open}) \times \frac{1}{K}, \quad K = 6$$
   其中 $Acc_{Open}$ 为模型在开放域上的实际正确率，剩余题目从 $K$ 个选项中随机猜对的概率被叠加，形成MCQA准确率的理论上界。实验表明，实际MCQA分数系统性地突破这一上界，揭示选项信号的贡献远超随机猜测。

2. **训练偏差放大**：在MCQA数据上进行RFT会提高选择题分数，但损害开放域表现，从而**扩大MCQA与OpenQA之间的差距**（Table 2）。例如在MMMU上，3B和7B模型的MCQA-OpenQA差距均随RFT增大。这表明MCQA下的可验证奖励可能过拟合于选项特异性启发式，而非可迁移的推理能力。

3. **普遍性**：从MCQA切换到OpenQA后，包括GPT-5在内的最强模型也出现大幅准确率下降——GPT-5在MMMU上下降19.8个百分点（从79.2%降至59.5%），InternVL3-8B下降27.9个百分点（Table 7）。这揭示了MCQA普遍存在分数虚高，OpenQA挑战是影响所有模型的基础性问题。

### 核心操控变量：选项的存在与否

本工作的关键创新在于识别并操控了一个决定性的因果变量：**选项的存在与否**。将MCQA改写为去除选项依赖的开放问答（OpenQA），同时保留可验证性，是消除评估失真和训练偏差的核心机制。

这一设计选择直接对应三个changed slots：

| 变更维度 | 基线方案 | ReVeL方案 | 因果作用 |
|---------|---------|----------|---------|
| **训练数据格式** | MCQA格式（含选项的多选题，规则精确匹配打分） | ReVeL改写后的OpenQA格式（按答案类型分类的开放问题，可确定性验证） | 消除选项依赖，迫使模型基于知识推理而非选项比较 |
| **评估验证方式** | 单一MCQA格式的规则匹配或LLM评判 | 混合确定性规则验证（数值/关键词/逐选项验证）+ LLM评判（仅开放型） | 最大化可验证比例，降低LLM评判成本和方差 |
| **奖励信号来源** | 基于选项选择的二元正确/错误奖励（鼓励选项利用捷径） | 基于开放答案内容验证的奖励（鼓励可迁移的推理过程） | 将强化信号从选项匹配转向内容正确性 |

### 混合验证设计：可验证性的最大化

ReVeL的核心技术洞察在于：通过将MCQA问题按答案类型分为四类，分别设计改写策略，使**70%-96%的题目可通过规则自动判分**（Table 4）。这一混合验证设计既消除了选项带来的评估失真，又大幅降低了纯LLM评判的成本和方差，同时为RFT提供了更稳健、可迁移的奖励信号。

具体分类与验证策略：

- **数值型**：通过规则过滤器识别，改写为显式定量提示，使用数值范围匹配验证
- **关键词型**：枚举可接受的同义词，使用关键词集合匹配验证
- **逐选项验证型**：将每个选项转换为声明性语句，模型进行True/False判断，使用规则验证
- **开放型**：改写为简洁的自由形式查询，仅此类使用LLM评判

这一设计的效率优势显著：ReVeL混合评判管线在整体准确率上达到98.5%，超过纯LLM Judge的97.3%，同时将误判率从2.0%降至0.3%（Table 3）。在EMMA和MMLU-Pro上，ReVeL达到100%的评判准确率。

### 与基线方法的本质区别

相较于现有的视觉推理RFT模型（如**R1-OneVision-7B**、**Mixed-R1-7B**、**VL-Rethinker-7B**），ReVeL的创新不在于模型架构或训练算法的改进，而在于**训练和评估数据格式的系统性重构**。现有RFT方法在MCQA格式下训练，不可避免地强化了选项利用行为；ReVeL通过格式转换从根本上切断了这一捷径信号通路，使得RFT的奖励信号真正对齐于知识获取和推理能力。

实验表明，Qwen2.5-VL-7B经ReVeL OpenQA训练后，在四项基准上的综合得分达到40.4，显著超过MCQA训练的36.3（+4.1），且OpenQA准确率提升约6个百分点，同时MCQA分数保持竞争力（Table 6）。这一结果验证了格式转换作为核心创新的有效性——不是通过更强的模型或更多的数据，而是通过消除评估和训练中的结构性偏差来实现鲁棒的性能提升。



ReVeL 的核心设计目标是将 MCQA 数据转换为可确定性验证的开放问答（OpenQA）格式，从而消除选项带来的评估失真与训练偏差。框架按 **分流与分类 → 基于提示的改写 → 混合评估与验证** 三阶段流水线组织，如图 5 所示。

### 三阶段流水线

**阶段一：分流与分类（Triage and Classification）**

输入 MCQA 问题首先经过规则过滤器识别数值型答案（如 `50kg`、`$9.8 \times 10^{-23} m/s^2$`），将其直接归入数值型类别。剩余非数值问题由轻量 LLM 分类器分配至三个类别之一：关键词匹配型、开放答案型、逐选项验证型。这一分类决策决定了后续改写策略与验证方式的选择，是整个框架的调度枢纽。

**阶段二：基于提示的改写（Prompt-based Rewriting）**

针对四个类别分别设计定制提示，将 MCQA 问题改写为语义等价的开放格式，同时保留可验证性：

- **数值型**：重新表述为显式定量提示，要求模型输出精确数值或计算表达式。
- **关键词型**：枚举可接受的同义词和表述变体，使答案可通过关键词匹配规则判分。
- **开放答案型**：改写为简洁的自由形式查询，此类问题因答案空间开放而需 LLM 评判。
- **逐选项验证型**：将每个选项转化为独立声明，要求模型逐一判断 True/False，从而将多选题拆解为多个可规则验证的判断题。

**阶段三：混合评估与验证（Hybrid Evaluation and Verification）**

对改写后的问题进行判分时，数值型、关键词型和逐选项验证型使用确定性规则匹配，仅开放答案型使用 LLM 评判。这一混合设计使 70%–96% 的题目可通过规则自动判分（Table 4），在降低计算成本的同时减少了 LLM 评判的主观方差。

### 关键设计决策

框架的核心原则是**最大化确定性规则评估的覆盖范围**：将答案无歧义的问题尽可能归入规则可验证类别，仅对真正需要语义理解的开放型答案保留 LLM 评判。Table 3 的消融实验表明，该混合管线的整体评判准确率达 98.5%，超过纯 LLM Judge 的 97.3%，同时将误判率（FPR）从 2.0% 降至 0.3%。

值得注意的是，改写和分类环节并非完美——整体错误率约 2%，可能在某些边界情况引入错误。此外，符号表征歧义构成规则验证的根本性限制：模型自由形式输出中同一概念的表述变异（如数值范围可写作 `1.30~40.45`、`1.30 to 40.45`、`between 1.30 and 40.45` 或 LaTeX 格式）无法被规则系统穷举，这是确定性匹配的固有局限。

### 补充图表

![[assets/figures/papers/paper_list_l739_https_arxiv_org_abs_2511_17405/figures/007_Figure_5.jpg]]
*Figure 5: Illustration of the rewrite-and-verify framework*

![[assets/figures/papers/paper_list_l739_https_arxiv_org_abs_2511_17405/figures/001_Figure_1.jpg]]
*Figure 1: Illustration of MCQA fragility. The example (left) shows an unfaithful reasoning chain that eliminates distractors incorrectly yet provide a correct final answer, yielding a positive reward signal that, when used in reinforcement learning, further amplifies shortcut behavior (top right). This shortcut behavior leads to widening gap between MCQA and OpenQA. The diagram motivate us to propose ReVeL, which aligns evaluation and training with reliable OpenQA*

![[assets/figures/papers/paper_list_l739_https_arxiv_org_abs_2511_17405/figures/021_Figure_10.jpg]]
*Figure 10: This prompt is used to filter out questions that exhibit characteristics such as option dependency, subjectivity and under-specification in stage 1 of our pipeline*



### 3.1 问题形式化与选项依赖的量化

ReVeL的核心动机源于对MCQA评估失真的严格量化。给定一个开放域问题，其MCQA版本在原始问题基础上附加了$K$个选项（通常$K=4$或$6$）。模型在MCQA上的准确率可以分解为两部分：模型真正掌握知识而答对的题目，以及模型本不会、但通过利用选项信号猜对的题目。为量化后者的贡献，论文定义了**随机猜测上界（Random-Guessing Upper Bound）**：

$$Acc_{UB} = Acc_{Open} + (1 - Acc_{Open}) \times \frac{1}{K}$$

其中$Acc_{Open}$为模型在同一问题集上去除选项后的开放域准确率，$K$为选项数量。该公式的含义是：在模型真正掌握的$Acc_{Open}$比例之外，剩余$(1 - Acc_{Open})$的题目上，模型可以通过从$K$个选项中随机猜测获得$\frac{1}{K}$的额外正确率。若实际MCQA准确率显著超过$Acc_{UB}$，则证明模型从选项中提取了超出随机猜测的信号——即存在选项利用捷径。

实验证据表明，在SimpleQA和Visual SimpleQA上，多个开源与商业模型的MCQA准确率均显著超过该理论上界（Figure 2），证实了选项信号的系统性贡献。

### 3.2 ReVeL三阶段管线

ReVeL框架由三个顺序模块构成（Figure 5），将MCQA问题转换为可确定性验证的开放格式，同时最大化规则判分的覆盖比例。

**阶段一：分流与分类（Triage and Classification）**

该模块首先通过规则过滤器识别数值型问题——即答案预期为具体数量或比率的题目（如“50kg”或“$9.8 \times 10^{-23} m/s^2$”）。数值型问题在评估时可直接进行数值匹配，无需LLM介入。

剩余的非数值问题被送入一个轻量级LLM辅助分类器，分配至以下三类之一：
- **关键词匹配型（Keywords matching）**：答案可枚举为有限的关键词或同义词集合；
- **逐选项验证型（Per-option verification）**：每个选项可转换为独立的真/假判断陈述；
- **开放型（Open answers）**：确实需要自由形式生成和语义评判的题目。

**阶段二：基于提示的改写（Prompt-based Rewriting）**

针对每个类别，使用定制提示将原始MCQA问题改写为语义等价的开放格式，同时保留可验证性：

- **数值型**：重新表述为显式的定量提示，要求模型输出数值答案；
- **关键词型**：枚举可接受的同义词，使规则匹配能够覆盖合理表述变异；
- **逐选项验证型**：将每个选项转换为声明性陈述，要求模型逐一判断真/假；
- **开放型**：重新表述为简洁的自由形式查询。

**阶段三：混合评估与验证（Hybrid Evaluation and Verification）**

对改写后的问题进行判分时，数值型、关键词型和逐选项验证型使用确定性规则匹配，仅开放型使用LLM评判。这一设计将70%至96%的题目（Table 4）纳入规则判分范围，大幅降低了纯LLM评判的计算成本和主观方差。

### 3.3 过度判真比率

在将MCQA转换为逐选项真/假判断题后，模型失去了选项间的互斥信号（即“只有一个正确”的先验），可能表现出系统性过度判真倾向。为量化这一效应，论文定义了**过度判真比率（Over-True Ratio）**：

$$\text{Over-True Ratio} = \frac{\text{Number of answers with >1 correct option}}{\text{Total incorrect answers}}$$

分子为模型在单个问题上将多个选项同时判为“真”的次数，分母为模型实际答错的总题目数。该比率反映了选项互斥信号移除后模型的肯定偏向程度——比率越高，说明模型越依赖选项间的相互排除来定位正确答案，而非基于独立知识判断每个选项的真伪。

### 3.4 模块间依赖与设计权衡

三阶段管线存在两个关键的设计权衡：

1. **分类准确率与覆盖率的平衡**：LLM分类器虽整体准确率较高，但并非完美（整体错误率约2%）。分类错误可能导致题目被分配至不合适的验证类别，进而影响判分准确性。论文通过采样验证（Table 8）确认了假阳性和假阴性率均在可控范围内。

2. **规则验证的覆盖率与表征方差的矛盾**：尽管70%-96%的题目可转为规则验证，但自由形式输出中同一概念的表述变异（如数值范围“1.30~40.45”可写作“1.30 to 40.45”、“between 1.30 and 40.45”、LaTeX格式等）无法被规则系统穷举。这是确定性匹配的固有局限，构成了混合验证管线的根本性边界。

### 补充图表

![[assets/figures/papers/paper_list_l739_https_arxiv_org_abs_2511_17405/figures/010_Table_5.jpg]]
*Table 5: Examples of our ReVeL Pipeline applied to different question types. Each quadrant displays an original multiple-choice question and its OpenQA counterpart*



## 实验与关键发现

### 核心发现：MCQA分数虚高与RFT的捷径强化

本工作首先通过一系列诊断实验，系统揭示了多项选择题（MCQA）格式对视觉语言模型评估与训练的双重危害。

**选项信号导致评估失真。** 在SimpleQA和Visual SimpleQA等开放域基准上，将问题改写为含6个选项的MCQA格式后，所有模型（包括开源和商业模型）的准确率均大幅超过开放域基线，并显著超越随机猜测理论上界（Figure 2）。随机猜测上界定义为：

$$Acc_{UB} = Acc_{Open} + (1 - Acc_{Open}) \times \frac{1}{K}, \quad K = 6$$

该公式表明，即使模型在剩余题目上完全随机猜测，其MCQA得分也应受此上界约束。然而实测得分普遍突破此界，证明模型在正确回答MCQA时，大量利用了选项集提供的额外信号，而非依赖真正的知识或推理能力。

**RFT将选项利用行为固化为捷径。** 在ViRL的5K MCQA样本上进行强化微调后，模型的选择题分数上升，但开放域表现下降，导致MCQA与OpenQA之间的分数差距（∆）扩大（Table 2）。例如在MMMU上，3B和7B模型的∆分别增大了4.5至9.1个百分点。这表明MCQA格式下的可验证奖励信号可能过拟合于选项特定的启发式策略，而非可迁移的推理能力。

**选项锚定现象揭示了推理的脆弱性。** 当用“以上均不正确”（NOTA）替换正确选项后，模型的推理过程与最终答案之间出现系统性矛盾（Figure 3, Table 9）。更值得注意的是选项锚定效应（Figure 7）：同一幅画作，当“蛋彩画”作为选项存在时，模型分析画面特征后认定其为蛋彩画；当该选项被移除后，模型对同一画面的推理转向“油画”特征。这说明模型的推理方向随可用选项而调整，并非基于客观事实。

**去除选项后所有模型一致降分。** 在MMMU等VQA基准上，直接去除选项（即要求模型自由生成答案）后，所有模型的准确率均一致下降（Figure 4），进一步证实了选项对评估结果的系统性干扰。

### ReVeL改写与混合验证管线的有效性

ReVeL的核心设计目标是将MCQA转换为可确定性验证的开放格式，从而消除选项依赖，同时避免纯LLM评判的高成本和方差。

**改写后规则可验证比例。** 经过ReVeL的分类与改写，70%至96%的题目可转为确定性规则验证（Table 4）。其中EMMA达95.9%，MMLU-Pro达100%，即便在MME-RealWorld这类复杂视觉任务中也达到71%。这大幅降低了LLM评判的计算开销和主观方差。

**混合验证准确率超越纯LLM Judge。** 在评判准确率的消融实验中（Table 3），ReVeL的混合管线总体准确率达98.5%，超过GPT-4.1 mini作为LLM Judge的97.3%，同时将假阳性率从2.0%降至0.3%。在EMMA和MMLU-Pro上，ReVeL达到100%的评判准确率，而LLM Judge分别为100%和95.8%；在MME-RealWorld上，ReVeL为98.0%，LLM Judge为95.9%。

### 训练实验：OpenQA vs MCQA

**主要结果（Table 6）。** 在Qwen2.5-VL-3B和7B两个模型规模上，使用ReVeL改写的OpenQA数据进行训练，均一致优于MCQA训练：

- Qwen2.5-VL-7B + OpenQA (ReVeL) 综合得分40.4，对比 + MCQA (ViRL) 的36.3（+4.1）
- Qwen2.5-VL-3B + OpenQA (ReVeL) 综合得分34.3，对比 + MCQA (ViRL) 的30.1（+4.2）

更重要的是，OpenQA训练的模型在每一项开放域基准上均有提升，同时MCQA分数保持竞争力。整体OpenQA准确率提升约6个百分点。

**与开源RFT模型的对比。** ReVeL训练的7B模型（40.4）在综合得分上超过多个开源视觉推理RFT模型：**R1-OneVision-7B**（Yang et al., 2025）的31.3、**Mixed-R1-7B**（Xu et al., 2025a）的37.2、**VL-Rethinker-7B**（Wang et al., 2025a）的37.5。

**训练配置消融。** 四种训练配置的对比表明：仅使用ReVeL改写后的OpenQA（+OpenQA (ReVeL)）即可实现最佳的OpenQA提升并保持MCQA分数；联合原始OpenQA数据（+OpenQA (ViRL+ReVeL)）可在部分基准上进一步增强效果。

### 大规模评估：MCQA到OpenQA的普适性降分

在涵盖开源和商业模型的大规模评估中（Table 7），从MCQA切换到OpenQA后，所有模型均出现显著准确率下降：

![[assets/figures/papers/paper_list_l739_https_arxiv_org_abs_2511_17405/figures/012_Table_7.jpg]]
*Table 7: Overall accuracy (%). Accuracy drop between MCQA and OpenQA is marked after ↓. Bold numbers indicate the smallest drop across open-sourced models*

- **GPT-5**在MMMU上从79.2%降至59.5%（↓19.8）
- **InternVL3-8B**在MMMU上从60.0%降至32.1%（↓27.9，为最大降幅）
- 其他商业模型如Gemini-2.5 flash同样出现大幅下降

这表明OpenQA挑战是一个影响所有模型（包括最先进模型）的根本性问题，而非仅针对特定模型或训练策略。

### 失败模式与局限性

**改写与分类的残余错误。** ReVeL的改写和分类环节虽然整体准确率较高（约98%），但并非完美。过滤管线的假阳性率和假阴性率验证（Table 8）表明，在边界情况下仍可能引入错误。随着LLM组件能力增强，此类错误有望减少。

**符号表征歧义的根本性限制。** 确定性规则验证面临一个固有局限：模型自由形式输出中同一概念的表述变异无法被规则系统穷举。例如数值范围“1.30~40.45”可写作“1.30 to 40.45”、“between 1.30 and 40.45”、LaTeX格式等多种形式，这是确定性匹配无法完全覆盖的边界情况。

**过度判真倾向。** 将MCQ转换为独立的判断题后（Table 12），模型在失去选项间互斥信号后表现出系统性过度判定为真的倾向。过度判真比率定义为：

$$\text{Over-True Ratio} = \frac{\text{Number of answers with >1 correct option}}{\text{Total incorrect answers}}$$

该指标反映了模型在开放判断场景下的肯定偏向，是MCQA格式下被掩盖的另一种脆弱性表现。

### 补充图表

![[assets/figures/papers/paper_list_l739_https_arxiv_org_abs_2511_17405/figures/002_Figure_2.jpg]]
*Figure 2: Performance comparison on original open-ended datasets (SimpleQA, Visual SimpleQA) and their multiple-choice versions (*-Choice, with 6 options). The Random Guess score is a theoretical upper bound that combines the model’s actual open-ended accuracy with the probability of correctly guessing on the rest of the questions from six options*

![[assets/figures/papers/paper_list_l739_https_arxiv_org_abs_2511_17405/figures/005_Figure_4.jpg]]
*Figure 4: On the impact of options on multiple-choice benchmarks: when options are removed, accuracy is uniformly lower, especially on VQA benchmarks like MMMU*

![[assets/figures/papers/paper_list_l739_https_arxiv_org_abs_2511_17405/figures/006_Table_2.jpg]]
*Table 2: Impact of RFT on ViRL MCQA data. MCQ = multiple-choice benchmark score; Open = Open-ended benchmark score. ∆ denotes the inflation gap (MCQ–Open). RFT on ViRL (5K MCQA samples) improves MCQ scores but enlarges ∆, indicating reinforced shortcut behavior*

![[assets/figures/papers/paper_list_l739_https_arxiv_org_abs_2511_17405/figures/011_Table_6.jpg]]
*Table 6: Performance Comparison of MCQA vs. OpenQA Training on In-Domain and Out-of-domain Benchmarks*

![[assets/figures/papers/paper_list_l739_https_arxiv_org_abs_2511_17405/figures/008_Table_3.jpg]]
*Table 3: Performance comparison of hybrid pipeline versus entirely using an LLM judge*

![[assets/figures/papers/paper_list_l739_https_arxiv_org_abs_2511_17405/figures/009_Table_4.jpg]]
*Table 4: Evaluation format distribution after rewriting. “Num”, “Text”, and “Opt” denote rule-based deterministic categories, while “Open” requires LLM judging. The large fraction of rule-based items demonstrates the efficiency of our hybrid evaluation design comparing to pure LLM-judge*

![[assets/figures/papers/paper_list_l739_https_arxiv_org_abs_2511_17405/figures/018_Figure_7.jpg]]
*Figure 7: Illustration of the Option-Anchoring Phenomenon. Left (Standard MCQA): when "Egg tempera" is an available option, the AI model analyzes the painting’s features—such as its matte finish and delicate colors—and concludes they are characteristic of egg tempera. Right (NOTA setting): the same model is presented with the same painting, but the "Egg tempera" option is removed and replaced with "None of the above options are correct". The model’s reasoning now shifts, describing the painting’s texture and detail as characteristic of oil paint*



## 定位与知识库关联

### 1. 与基线方法的关系

ReVeL 的核心贡献在于**评估格式与训练奖励信号的重新对齐**，而非提出全新的模型架构或强化学习算法。因此，其方法谱系定位需从“评估范式”和“训练范式”两个维度展开。

**评估范式维度：从MCQA到可验证OpenQA的转换。** 传统视觉语言模型的评测高度依赖多项选择题格式（MCQA），其判分方式为基于选项索引的精确匹配，成本极低且完全确定性。然而，本文的核心发现是：这种格式本身为模型提供了可利用的捷径信号——选项间的相对比较、位置记忆和排除法可以使模型在缺乏真实知识或推理能力的情况下猜出正确答案。ReVeL 的直接前驱是“将MCQA直接转换为开放问答（OpenQA）并用LLM评判”的思路，但该思路面临两个瓶颈：(1) 纯LLM评判的计算成本和主观方差远高于规则匹配；(2) 许多MCQA问题天然不适合直接转换为自由形式回答（如需要验证化学结构SMILES的问题）。ReVeL 通过**按答案类型分类改写**的策略，将70%–96%的问题重新归类为数值型、关键词型和逐选项验证型，使其可被确定性规则判分，仅对真正需要语义理解的开放型问题保留LLM评判。这一设计在继承OpenQA消除选项依赖的优势的同时，大幅压缩了LLM评判的适用范围，从而在准确率（98.5% vs. 纯LLM Judge的97.3%）和误判率（假阳性率从2.0%降至0.3%）上均实现超越（Table 3）。

**训练范式维度：RFT奖励信号的去捷径化。** 在训练侧，本文的基线方法是以**ViRL**框架为基础的GRPO训练。ViRL本身是视觉语言模型的强化微调框架，其奖励信号来源于答案正确性的验证。当训练数据为MCQA格式时，奖励信号实质上奖励的是“选项选择”这一行为，而非“知识检索与推理”这一能力。本文的关键因果证据（Table 2）表明：在MCQA数据上进行RFT会提升MCQA分数，但同时扩大MCQA与OpenQA之间的差距（△从+4.5扩大到+9.1），说明模型学到了选项依赖的捷径行为。ReVeL的解决方案是将训练数据改写为OpenQA格式，使奖励信号来源于开放答案内容的验证，从而引导模型学习可迁移的推理过程。实验证明，使用ReVeL改写后的OpenQA数据训练，在OpenQA准确率上提升约6个百分点，同时MCQA分数保持竞争力（Table 6）。

**与具体基线模型的对比。** 在Table 6的综合评估中，ReVeL训练的Qwen2.5-VL-7B（Overall Score 40.4）显著优于多个开源视觉推理RFT模型：**R1-OneVision-7B**（Yang et al., 2025, 31.3）、**Mixed-R1-7B**（Xu et al., 2025a, 37.2）和**VL-Rethinker-7B**（Wang et al., 2025a, 37.5）。这些模型同样采用了强化微调范式，但其训练数据的评估格式和奖励设计未针对选项依赖问题进行优化，因此在OpenQA泛化能力上落后于ReVeL。值得注意的是，ReVeL并非在模型架构或训练算法上超越这些工作，而是通过**数据格式的转换**实现了对奖励信号质量的根本性改善。

### 2. 适用边界

ReVeL的适用边界由以下条件界定：

**任务类型边界：QA类任务。** 当前框架聚焦于将多项选择题转换为可验证的开放问答，其分类体系和改写策略（数值型、关键词型、逐选项验证型、开放型）均针对QA场景设计。论文明确指出，向长文本生成等非QA任务的扩展尚未探索，这是框架的显式适用边界。

**可验证性边界：答案必须具有确定性判据。** ReVeL的核心设计原则是“最大化确定性规则验证的覆盖范围”。对于答案本身具有歧义或需要主观判断的问题（如开放型创意生成），框架只能退化为LLM评判，此时ReVeL的优势仅体现在分类筛选阶段排除了那些可被规则验证的题目，降低了LLM评判的总体调用量。对于完全无法定义客观判据的任务，ReVeL不提供额外增益。

**改写保真度边界：依赖LLM改写质量。** 改写和分类环节由LLM执行，其整体错误率约2%（Table 8），这意味着在边界情况下可能引入语义偏移或分类错误。随着LLM能力增强，此类错误有望减少，但当前阶段仍需对改写后的数据进行质量抽检。

**符号表征边界：规则验证的固有局限。** 即使问题被正确分类为数值型或关键词型，模型自由形式输出中的表述变异（如数值范围“1.30~40.45”可写作“1.30 to 40.45”、“between 1.30 and 40.45”、LaTeX格式等）无法被规则系统穷举。论文将这一限制明确列为“符号表征歧义的根本性限制”，这是确定性匹配方法论的固有边界，而非实现层面的缺陷。

### 3. 局限与开放问题

**已知局限。**

1. **改写管线并非完美。** 分类和改写环节的整体错误率约2%，可能偶尔将问题错误分类或引入语义偏移。论文建议随着底层LLM能力增强，此类错误有望自然减少，但未提供系统性的质量保证机制。

2. **未解决LLM Judge的固有问题。** 对于必须使用LLM评判的开放型问题，ReVeL并未改进LLM Judge本身的位置偏差、评判不一致等已知缺陷。框架的贡献在于压缩LLM评判的适用范围，而非提升其可靠性。

3. **符号表征歧义无法根除。** 自由形式输出中同一概念的表述变异是不可穷举的，规则系统只能覆盖高频模式。对于边界情况，仍可能出现假阴性判分。

4. **任务类型受限。** 当前工作聚焦于QA类任务，向长文本生成、多轮对话等场景的扩展尚未探索。

**开放问题。**

1. **跨任务泛化。** 如何将ReVeL的“分类改写+混合验证”框架扩展到开放域长文本生成等非QA任务？这需要重新定义答案类型分类体系和对应的验证策略。

2. **自适应评估系统。** 能否开发一个根据问题特征动态选择最合适评判机制的自适应系统？当前ReVeL的分类是静态的（基于改写前的题目特征），而理想的系统应能根据模型输出的实际特征动态调整验证策略。

3. **高表征方差边界处理。** 如何改进规则验证系统以处理自由形式输出中的高表征方差边界情况？可能的路径包括引入模糊匹配、同义词库扩展或轻量级语义相似度模型作为规则系统的补充。

4. **改写质量保证机制。** 随着模型能力增强，改写环节引入的错误是否会显著减少，还是需要额外的质量保证机制（如人工抽检、多模型交叉验证）？这一问题在当前工作中未得到系统回答。

5. **选项锚定效应的深层机制。** 论文通过NOTA替换实验（Figure 7）揭示了“选项锚定现象”——模型会根据可用选项调整推理方向。但这一现象的认知机制和跨模型泛化规律尚未被系统研究，理解其深层原因可能为设计更鲁棒的评估格式提供新思路。



## 原文 PDF

![[paperPDFs/CVPR_2026/Beyond_Multiple_Choice_Verifiable_OpenQA_for_Robust_Vision_Language_RFT.pdf]]
