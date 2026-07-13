---
title: "TreeTeaming: Autonomous Red-Teaming of Vision-Language Models via Hierarchical Strategy Exploration"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/TreeTeaming_Autonomous_Red_Teaming_of_Vision_Language_Models_via_Hierarchical_Strategy_Exploration.pdf
project_link: null
code_link: "https://github.com/ChunXiaostudy/TreeTeaming"
aliases:
- TreeTeaming
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: TreeTeaming通过引入分层策略树和LLM驱动的编排器，将红队测试从静态策略测试转变为动态的、进化的发现过程，从而解锁了自主探索未知攻击向量的能力。
primary_logic: 核心洞见是自动化红队测试的本质在于策略空间的系统性探索与利用，而非单一策略的迭代优化；通过构建可动态扩展的策略树，并利用大型语言模型进行全局推理和决策，框架能够自主发现超越人工预设的多样化攻击策略。
claims:
- TreeTeaming在12个测试VLM中的11个上取得了最先进的攻击成功率，并在GPT-4o上达到87.60%的ASR。
- TreeTeaming发现的策略在多样性上超过了由15种已有公共越狱方法组成的联合集，kNN-entropy从2.694提升至2.723（n=15, Qwen2.5-VL-7B）。
- 消融实验表明，将分层策略树替换为平铺策略库后，GPT-4o上的ASR从87.60%显著下降至71.80%，策略多样性也下降，证明了树结构的关键作用。
- 与先前的红队方法Trust-VLM相比，TreeTeaming在GPT-4o上的ASR高出5.56个百分点，且仅需5次样本细化迭代，远少于后者的50次。
---

# TreeTeaming: Autonomous Red-Teaming of Vision-Language Models via Hierarchical Strategy Exploration

> [!tip] 核心洞察
> 核心洞见是自动化红队测试的本质在于策略空间的系统性探索与利用，而非单一策略的迭代优化；通过构建可动态扩展的策略树，并利用大型语言模型进行全局推理和决策，框架能够自主发现超越人工预设的多样化攻击策略。

| 字段 | 内容 |
|------|------|
| 中文题名 | TreeTeaming：通过分层策略探索实现对视觉语言模型的自动化红队测试 |
| 英文题名 | TreeTeaming: Autonomous Red-Teaming of Vision-Language Models via Hierarchical Strategy Exploration |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2603.22882) · [Code](https://github.com/ChunXiaostudy/TreeTeaming) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/image_and_video_generation |
| Method | TreeTeaming |
| Dataset | SafeBench, Strategy Diversity, Sample Toxicity |

> [!tip] 效果简介
> - SafeBench 上，ASR (%) on GPT-4o 87.60 vs 82.04 (Trust-VLM) (+5.56)；ASR (%) on Claude-3.5 61.60 vs 47.20 (SI-Attack, best jailbreak) (+14.40)；平均ASR (%) across 12 VLMs 89.48 vs best competitor varies (N/A)。
> - Strategy Diversity (Gen15 strategies) 上，kNN-entropy 2.723 (Ours Qwen2.5-VL-7B) vs 2.694 (Union set of 15 prior methods) (+0.029)。
> - Sample Toxicity 上，Visual Toxicity (%) 9.86 vs 51.00 (Trust-VLM) (-41.14)。

## 概要

视觉语言模型（VLM）在安全对齐上的脆弱性已引起广泛关注，但当前的红队测试方法普遍受限于静态、模板化的攻击策略——它们只能在预定义的启发式规则内进行线性优化，无法自主发现新颖的漏洞利用方式。这一瓶颈的根源在于，自动化红队测试的本质并非单一策略的迭代精炼，而是对攻击策略空间的系统性探索与利用。

**TreeTeaming** 针对上述问题，将红队测试从静态策略测试重构为动态的、进化的发现过程。其核心机制是一棵从单一种子示例生长而成的分层策略树，由一个基于大型语言模型（LLM）的编排器进行全局推理与资源调度：当现有策略的攻击成功率（ASR）高于动态阈值 $\tau_{\mathrm{dynamic}}$ 时进入利用阶段，否则触发探索以发现未知攻击向量。策略的具体执行则由一个配备11种图像操作工具的多模态执行器完成，并通过策略一致性检查器确保生成样本与预期策略对齐。

在12个主流VLM上的实验表明，TreeTeaming在其中11个模型上取得了最先进的攻击成功率，在GPT-4o上达到87.60%，比此前最优的红队方法**Trust-VLM**（MM'24/ICML'25）高出5.56个百分点，且仅需5次样本细化迭代（后者需50次）。更重要的是，TreeTeaming自主发现的策略在多样性上超过了由15种已有越狱方法组成的联合集（kNN-entropy从2.694提升至2.723），同时生成样本的视觉毒性降至9.86%、文本毒性降至6.63%，平均毒性降低23.09%。消融实验进一步证实，将分层策略树替换为平铺策略库后，GPT-4o上的ASR从87.60%骤降至71.80%，策略多样性同步下降，验证了树结构在策略空间探索中的关键作用。

### 视觉语言模型的安全挑战

视觉语言模型（VLMs）的快速发展使其在视觉问答、多模态推理等任务中展现出强大能力，但同时也暴露出严重的安全隐患。恶意攻击者可通过精心构造的图像-文本组合诱导模型生成有害内容，例如非法行为指导、仇恨言论或隐私泄露。这种跨模态攻击的复杂性远超纯文本场景：图像通道提供了隐蔽的语义注入途径，而视觉与文本的交互又产生了新的漏洞面。因此，构建系统化的红队测试方法以发现和修复这些漏洞，已成为VLM安全研究的核心议题。

### 现有方法的根本局限：静态策略与线性探索

当前VLM红队测试方法可分为两类：**越狱攻击方法**（如FigStep、MML、SI-Attack、Hades等）和**自动化红队测试框架**（如Arondight、Trust-VLM）。尽管这些方法在特定场景下有效，但它们共享一个根本性瓶颈：**攻击策略空间是静态的、手工预设的**。

具体而言，现有方法依赖固定的攻击启发式模板集——例如在图像中嵌入特定类型的扰动、使用预定义的文本提示模式等。其探索机制局限于线性优化范式：在已知策略内部进行参数微调或样本迭代，无法自主发现超越人类预设的新型攻击向量。这种“已知策略优化”的范式意味着，红队测试的有效性上限被设计者的先验知识所严格限制。一旦目标VLM对已知攻击类型产生了鲁棒性，或存在设计者未曾设想的漏洞模式，现有方法便无法触及。

### 核心动机：从策略优化到策略发现

上述局限指向一个关键洞察：**自动化红队测试的本质在于策略空间的系统性探索与利用，而非单一策略的迭代优化**。真正有效的红队测试框架应当能够自主发现多样化的攻击策略，而非仅仅在既定框架内追求更高的攻击成功率。

这一洞察驱动了TreeTeaming的设计动机：将红队测试从静态策略测试转变为动态的、进化的**策略发现过程**。具体而言，框架需要具备三种核心能力：

1. **策略空间的层次化组织**：攻击策略天然存在抽象层级——从高层概念（如“语境操纵”）到具体技术（如“漫画嵌入”“情感诱导”）。利用这种层次结构可以引导更高效的探索。
2. **自主探索与利用的平衡**：框架需要动态决定何时深入优化已知有效策略（利用），何时扩展搜索新的策略方向（探索），以最大化策略多样性和攻击覆盖率。
3. **多模态策略的精确执行**：抽象策略必须被准确转化为具体的图像-文本测试用例，且生成的样本需与策略意图严格对齐，否则将引入噪声、降低测试有效性。

TreeTeaming正是围绕上述动机构建的：通过引入**分层策略树**和**LLM驱动的编排器**，框架从单一种子示例出发，自主生长出完整的策略树，实现对未知攻击向量的系统性发现。这一范式转换——从“测试已知策略”到“发现未知策略”——构成了本文的核心贡献。

## 核心方法与创新机理

TreeTeaming 的核心创新在于将 VLM 红队测试从**静态模板匹配**转变为**动态策略空间探索**。现有方法（如 **FigStep** (AAAI'25)、**MML** (ACL'25)、**SI-Attack** (ICCV'25) 等）依赖固定的、手工设计的攻击启发式模板集，只能在线性优化范式内对已知技巧进行微调。TreeTeaming 通过三个关键 changed slots 突破这一瓶颈：

**1. 攻击策略空间：从固定模板到动态可扩展的分层策略树**

现有方法的攻击策略空间受限于预定义的模板集合，无法自主发现未知的攻击向量。TreeTeaming 构建了一棵从单一种子示例生长而来的分层策略树，其根节点为攻击目标，父节点为策略类别（如“上下文操纵”），叶节点为具体策略（如“漫画”、“情感”）。整个策略树由 LLM 驱动的编排器自主扩展，而非人工预设（Section 1 明确声明：“*Unlike existing methods that rely on predefined templates, TreeTeaming grows its entire strategy tree from a single seed example.*”）。

这一设计的决定性证据来自消融实验（Table 4）：将分层策略树替换为平铺策略库后，GPT-4o 上的 ASR 从 87.60% 骤降至 71.80%（降幅达 15.8 个百分点），且策略多样性同步下降。这表明树结构提供的层次化概念引导——父节点为子策略的生成提供语义约束和方向——是解锁高质量多样化策略的关键。

**2. 探索机制：从线性优化到基于树的层次化探索-利用平衡**

现有红队方法在预定义策略内进行线性微调，缺乏对策略空间全局结构的感知。TreeTeaming 的编排器通过动态阈值 $\tau_{\mathrm{dynamic}}$ 和利用预算 $E_n$ 实现探索与利用的自适应平衡：

$$\tau_{\mathrm{dynamic}} = \max\left\{ \tau_{\mathrm{initial}} \cdot \left(1 - \frac{N_{\mathrm{total}}}{N_{\mathrm{max}}}\right), \tau_{\mathrm{min}} \right\}$$

当某叶节点的 ASR 超过 $\tau_{\mathrm{dynamic}}$ 且利用预算未耗尽时，编排器进入**利用阶段**，对该策略进行样本级细化；否则触发**探索阶段**，基于父节点的概念引导生成全新的攻击策略。这一机制使框架能够系统性地覆盖策略空间——既深入挖掘高潜力区域，又持续拓展未知边界。

消融实验（Figure 3c）揭示了 $\tau_{\mathrm{initial}}$ 的关键作用：过低（0.2）导致过早收敛到平庸策略，过高（0.8）则延迟利用阶段，默认值 0.4 在多数模型上达到最佳效果。此外，策略数量和攻击尝试次数的增加虽能提升 ASR，但呈现边际收益递减（Figure 3a,b），15 个策略和 5 次尝试被确定为计算成本与效果的最佳平衡点。

**3. 测试用例生成：从单一扰动到 LLM 驱动的多模态组合执行**

现有方法通常采用单一图像扰动或固定文本模板，无法执行复杂的组合攻击策略。TreeTeaming 的多模态执行器配备 11 种预定义图像操作工具（Toolkit），可将编排器输出的抽象策略转化为具体的图像-文本测试用例。更关键的是，执行器内置**策略一致性检查器**，确保生成的样本忠实反映目标策略的意图，而非产生无关的随机扰动。

消融实验（Table 9）验证了这一设计的必要性：移除一致性检查器后，GPT-4o 上的 ASR 从 87.60% 下降至 78.80%，表明检查器能有效筛除不符合策略的低质量样本。此外，组件升级实验（Table 5）揭示了一个重要洞见：升级执行器模型（如使用 Gemini-2.5-Pro）带来的 ASR 提升（+13.4%）显著大于升级编排器模型（+4.2%），说明**执行复杂策略的能力**比策略生成本身更为关键——这一发现指明了未来优化的方向。

**4. 反馈闭环：从无反馈到双层面失败归因**

TreeTeaming 的第三个协同模块——失败原因分析模型——构成了完整的反馈闭环。该模块在样本层面分析单次攻击失败的具体原因，在策略层面统计聚合所有叶节点的失败日志，识别主导失败模式。这一双层面归因信息反馈给编排器，驱动后续的利用与探索决策，使整个红队测试过程具备自我进化的能力。

TreeTeaming 通过三个协同模块构建了一个从策略发现到攻击执行再到反馈学习的闭环系统。与现有方法依赖静态、手工设计的攻击模板不同，该框架将整个策略树从**单个种子示例**开始动态生长，实现了攻击策略空间的自主探索与利用。

### 模块架构与数据流

框架的核心工作流围绕三个模块展开，其协同关系如 Figure 2 所示：

![[assets/figures/papers/paper_list_l2425_https_arxiv_org_abs_2603_22882/figures/002_Figure_2.jpg]]
*Figure 2: Overview of the TreeTeaming Framework. The Strategy Tree and Orchestrator maintains a hierarchical structure with a root objective, parent nodes (strategy categories like “Contextual Manipulation”), and leaf nodes (concrete strategies like “Comics,”“Emotion”). The Orchestrator dynamically selects strategies for exploitation or exploration based on ASR metrics. The Actuator, equipped with 11 tools, translates selected strategies into image-text test cases that are sent to the target VLM*

1. **策略树与编排器（Strategy Tree & Orchestrator）**：作为系统的决策中枢，维护一个分层策略树结构——根节点为目标任务，父节点为策略类别（如“上下文操纵”），叶节点为具体策略（如“漫画”、“情感”）。编排器基于攻击成功率（ASR）指标和动态阈值 $$\tau_{\mathrm{dynamic}}$$，在**策略利用**（对满足阈值的高潜力策略进行样本级细化）和**策略探索**（在父节点概念引导下生成全新攻击向量）之间动态切换。

2. **多模态执行器与策略一致性检查器（Multimodal Actuator & Strategy Consistency Checker）**：负责将编排器选定的抽象策略转化为具体的图像-文本测试用例。执行器配备**11种预定义图像操作工具**，可组合执行复杂攻击。策略一致性检查器随后验证生成的样本是否忠实于原始策略意图，筛除偏离策略方向的低质量样本，确保攻击的精准性。

3. **失败原因分析模型（Failure Cause Analysis Model）**：构成反馈学习回路。该模块在**样本层面**分析单次攻击失败的具体原因，并在**策略层面**通过统计归纳所有叶节点失败日志，识别出**主导失败模式（Dominant Failure Mode）**。这些分析结果反馈给编排器，驱动后续的策略选择与优化决策。

### 输入输出流

- **输入**：单个种子示例（包含有害查询的文本-图像对）和目标任务描述。
- **内部循环**：编排器从策略树中选择策略节点 → 执行器生成多模态测试样本 → 一致性检查器过滤 → 样本发送至目标VLM → 失败原因分析模型收集结果并反馈 → 编排器更新策略状态并决定下一轮探索/利用。
- **输出**：一组多样化的攻击策略及其对应的测试样本，以及各目标VLM的攻击成功率评估。

TreeTeaming 的核心工作流围绕三个协同模块展开：**策略树与编排器（Strategy Tree & Orchestrator）**、**多模态执行器与策略一致性检查器（Multimodal Actuator & Strategy Consistency Checker）**，以及**失败原因分析模型（Failure Cause Analysis Model）**。三者共同构成一个闭环的自主红队测试系统。

### 策略树与编排器

策略树采用分层结构：根节点为攻击目标，父节点代表策略类别（如“上下文操纵”），叶节点为具体攻击策略（如“漫画”“情感”）。整个策略树从**单个种子示例**开始生长，无需任何预定义模板库——这是 TreeTeaming 区别于所有现有方法的关键设计。

编排器是策略树的决策核心，通过一个**动态阈值机制**在探索（Exploration）与利用（Exploitation）之间进行自适应平衡。其核心公式为：

$$\tau_{\mathrm{dynamic}} = \max\left\{ \tau_{\mathrm{initial}} \cdot \left(1 - \frac{N_{\mathrm{total}}}{N_{\mathrm{max}}}\right), \tau_{\mathrm{min}} \right\}$$

**变量含义：**
- $\tau_{\mathrm{dynamic}}$：动态探索阈值，随策略树增长而衰减
- $\tau_{\mathrm{initial}}$：初始探索阈值（默认值 0.4）
- $N_{\mathrm{total}}$：已生成的策略总数
- $N_{\mathrm{max}}$：最大允许策略数
- $\tau_{\mathrm{min}}$：绝对质量下限（默认值 0.1）

**决策逻辑：** 编排器遍历策略树，寻找满足 $ASR(n) > \tau_{\mathrm{dynamic}}$ 且利用预算 $E_n$ 未耗尽的叶节点进行利用（即对该策略进行样本级细化）。当没有策略满足利用条件时，编排器触发探索阶段，基于父节点的概念引导生成全新的攻击策略。这一机制使框架能够在攻击成功率较高时优先深耕有效策略，而在现有策略趋于饱和时主动开拓未知攻击向量。

### 多模态执行器与策略一致性检查器

执行器负责将编排器选中的抽象策略转化为具体的图像-文本测试用例。它配备了一个包含 **11 种预定义图像操作函数**的工具箱，可组合执行复杂的多模态攻击指令。执行器由强大的多模态生成模型驱动（默认使用 Qwen-Image 和 Qwen-Image-Edit）。

策略一致性检查器是执行器的质量守门人：它验证生成的测试用例是否真正贯彻了目标策略的意图，筛除不符合策略语义的低质量样本。消融实验表明，移除该检查器后 GPT-4o 上的 ASR 从 87.60% 下降至 78.80%，验证了其关键作用。

### 失败原因分析模型

该模块在两个粒度层面提供反馈信号：

- **样本级归因：** 对每次攻击尝试的失败原因进行分析，为后续样本细化提供具体指导
- **策略级归因：** 收集某叶节点下所有样本的失败日志，通过统计分析和泛化，识别该策略的**主导失败模式**，驱动编排器对该策略的后续决策（继续利用或放弃）

编排器使用 Qwen2.5-72B（temperature=0.8）进行策略决策和失败分析，执行器则协作 Qwen-Image 和 Qwen-Image-Edit 生成多模态测试样本。三个模块形成“决策—执行—反馈”的闭环，使红队测试从静态策略测试转变为动态的、进化的漏洞发现过程。

## 实验与关键发现

### 核心实验结果

TreeTeaming在VLM红队测试任务上展现出显著优势。在SafeBench基准上，该方法在12个测试VLM中的11个上取得了最优攻击成功率（ASR），平均ASR达到89.48%（Table 1）。其中，在GPT-4o上达到87.60%的ASR，较此前最优红队方法**Trust-VLM**（MM'24 ICML'25）高出5.56个百分点。值得注意的是，Trust-VLM需50次样本细化迭代，而TreeTeaming仅使用5次迭代即实现超越，表明分层策略探索的效率优势。在安全对齐较强的Claude-3.5上，TreeTeaming以61.60%的ASR领先最佳越狱基线**SI-Attack**（ICCV'25）14.40个百分点，验证了自主策略发现对高安全模型的有效性。

在攻击样本质量方面，TreeTeaming生成的样本毒性显著降低：视觉毒性降至9.86%，文本毒性降至6.63%，平均毒性较Trust-VLM降低23.09%（Table 2）。这表明框架并非通过生成极端有害内容来提升ASR，而是通过更精巧的策略设计实现攻击。

![[assets/figures/papers/paper_list_l2425_https_arxiv_org_abs_2603_22882/figures/004_Table_2.jpg]]
*Table 2: Comparison of sample diversity, sample toxicity, and strategy diversity (measured via kNN-entropy). Higher is better for diversity (↑), lower for toxicity (↓); Notes: A “/” indicates the metric is either (a) not applicable for single-strategy methods, or (b) unavailable as it was not reported in the original work (Arondight’s toxicity). Methods marked with ∗ use fixed textual prompts, yielding zero values for both textual diversity and toxicity metrics*

### 策略多样性与树结构消融

策略多样性是TreeTeaming的核心优势之一。在Qwen2.5-VL-7B上，TreeTeaming发现的15种策略的kNN-entropy达到2.723，超过了由15种已有公共越狱方法组成的联合集（kNN-entropy为2.694）（Table 3）。这意味着单一框架自主发现的策略集合，在多样性上超越了人工设计的多种方法的简单聚合。

![[assets/figures/papers/paper_list_l2425_https_arxiv_org_abs_2603_22882/figures/006_Table_3.jpg]]
*Table 3: Strategy diversity comparison. Our method’s performance on various models is compared to a Union set representing the aggregated diversity from a collection of prior works. Metrics are kNN-dist and kNN-entropy. The calculation uses the n strategies; results for*

消融实验直接验证了分层策略树的必要性（Table 4）。将策略树替换为平铺策略库后，GPT-4o上的ASR从87.60%骤降至71.80%，降幅达15.8个百分点，且策略多样性同步下降。这一结果揭示了核心因果机制：树结构的父节点提供概念性引导，使编排器能够在有意义的策略方向上系统探索，而非在无结构的策略空间中盲目搜索。平铺库缺乏这种层级约束，导致探索效率低下和策略同质化。

![[assets/figures/papers/paper_list_l2425_https_arxiv_org_abs_2603_22882/figures/007_Table_4.jpg]]
*Table 4: Comparison of Attack Success Rate (in %, ↑) and strategy diversity (kNN-entropy) between the Strategy Tree and a Flat Strategy Pool, grouped by model*

### 关键模块消融

**策略一致性检查器**的移除实验（Table 9）显示，GPT-4o上的ASR从87.60%下降至78.80%（降幅8.8个百分点）。检查器通过筛除不符合策略意图的低质量样本，确保执行器生成的测试用例与编排器指定的攻击概念对齐，避免了探索过程中的语义漂移。

**编排器与执行器模型升级**的对比实验（Table 5）揭示了不对称的重要性排序：将执行器模型升级至Gemini-2.5-Pro带来13.4%的ASR提升，而仅升级编排器模型仅提升4.2%。这表明执行复杂多模态攻击策略的能力是性能瓶颈所在，执行器质量对最终效果的影响权重大于编排器的决策能力。

### 超参数敏感性分析

Figure 3展示了三个关键超参数的影响。策略数量（Figure 3a）和攻击尝试次数（Figure 3b）均呈现边际收益递减：15个策略和5次尝试被确定为计算成本与效果的最佳平衡点。初始探索阈值 $\tau_{\mathrm{initial}}$（Figure 3c）的选择尤为关键：过低（0.2）导致编排器过早收敛到平庸策略，无法探索更优的攻击向量；过高（0.8）则延迟利用阶段，浪费计算资源在已足够好的策略上。默认值0.4在多数模型上达到最佳效果，验证了动态阈值公式 $\tau_{\mathrm{dynamic}} = \max\left\{ \tau_{\mathrm{initial}} \cdot \left(1 - \frac{N_{\mathrm{total}}}{N_{\mathrm{max}}}\right), \tau_{\mathrm{min}} \right\}$ 设计的合理性。

### 策略迁移与泛化性

策略可迁移性实验（Table 12）表明，从弱模型向强模型的上游迁移仍存在性能差距：DeepSeek-VL策略迁移至GPT-4o仅达81.60% ASR，低于在GPT-4o上从头发现的87.60%。但下游迁移（从强到弱）效果较好，说明强模型发现的策略具有更广泛的适用性。

此外，TreeTeaming发现的策略能够增强现有方法（Table 6）：将自主发现的“注意力转移”范式注入FigStep和MMSafety后，两者ASR均获提升，验证了策略发现成果的可复用性。

![[assets/figures/papers/paper_list_l2425_https_arxiv_org_abs_2603_22882/figures/009_Table_6.jpg]]
*Table 6: ASR (in %, ↑) comparison on the FigStep and MMSafety. The ’+’ versions represent enhancements based on our TreeTeaming approach*

### 局限性与待验证点

尽管结果全面，仍需注意以下局限：完整评估单个VLM耗时11.75小时，计算开销较高；部分基线方法（如Arondight）未开源，导致在部分模型上的对比缺失，可能影响公平性评估的完整性；攻击样本生成依赖强大的多模态生成模型（Qwen-Image-Edit），在资源受限环境下的适用性需进一步验证。

![[assets/figures/papers/paper_list_l2425_https_arxiv_org_abs_2603_22882/figures/005_Figure_3.jpg]]
*Figure 3: Ablation study on the impact of hyperparameters on ASR (in %, ↑). (a) the number of strategies, (b) the number of attack attempts, and (c) the initial exploration threshold*

## 定位与知识库关联

### 与现有方法的关系

TreeTeaming 的贡献本质在于将 VLM 红队测试从**静态策略测试**转变为**动态策略发现**。理解这一点需要审视其与两类基线工作的关系：直接越狱攻击方法与自动化红队框架。

**与越狱攻击方法的关系。** 现有越狱方法——包括 FigStep (AAAI'25)、MML (ACL'25)、SI-Attack (ICCV'25)、MM-safety (ECCV'24)、Hades (ECCV'24)、CS-DJ (ECCV'24) 和 JOOD (CVPR'25)——共享一个根本局限：它们依赖固定的、手工设计的攻击启发式模板集，只能在预定义策略空间内进行线性优化。TreeTeaming 改变了这一范式：其攻击策略空间从封闭的模板集变为动态可扩展的分层策略树，从单一种子示例出发，通过 LLM 驱动的编排器自主探索和利用新的攻击概念。这一变化的因果效应在 Table 6 中得到直接验证：将 TreeTeaming 发现的策略注入 FigStep 和 MMSafety 后，这些方法的 ASR 获得显著提升，表明 TreeTeaming 发现的是**可迁移的攻击洞见**，而非简单的参数调优。

**与自动化红队框架的关系。** 与 Arondight 和 Trust-VLM (MM'24, ICML'25) 相比，TreeTeaming 的差异化体现在三个关键维度。第一，探索机制：Trust-VLM 和 Arondight 在预定义策略内进行微调，而 TreeTeaming 采用基于树的层次化探索，利用动态阈值 $\tau_{\mathrm{dynamic}}$ 和利用预算 $E_n$ 自适应平衡探索与利用。第二，测试用例生成：基线方法依赖单一图像扰动或固定文本模板，而 TreeTeaming 的多模态执行器配备 11 种图像操作工具，可组合执行复杂攻击策略，并通过策略一致性检查器保证策略对齐。第三，效率：TreeTeaming 仅需 5 次样本细化迭代，而 Trust-VLM 需要 50 次。在 GPT-4o 上，TreeTeaming 的 ASR 达到 87.60%，比 Trust-VLM 的 82.04% 高出 5.56 个百分点（Table 1），同时攻击样本的视觉毒性从 51.00% 降至 9.86%，文本毒性降至 6.63%，平均毒性降低 23.09%（Table 2）。

**策略多样性作为核心区分指标。** Table 3 揭示了 TreeTeaming 相对于整个方法谱系的根本优势：其发现的策略在多样性上超过了由 15 种已有公共越狱方法组成的联合集，kNN-entropy 从 2.694 提升至 2.723（n=15, Qwen2.5-VL-7B）。这意味着 TreeTeaming 不仅攻击成功率高，而且**探索到了现有方法集体未能覆盖的策略空间区域**。

### 适用边界

TreeTeaming 的适用边界由以下条件界定：

1. **模态范围**：当前框架专为视觉-语言模型的图像-文本联合输入设计，其 11 种图像操作工具和策略一致性检查器均针对视觉模态。扩展到音频、视频等模态需要重新设计执行器工具集和一致性验证机制。

2. **目标模型类型**：评估覆盖 12 个主流 VLM，包括开源模型（LLaVA-1.5-13B、DeepSeek-VL、Qwen 系列、LLaMa-3.2-Vision-11B、Gemma3-27B-IT）和闭源模型（GPT-4o、Claude-3.5 Sonnet）。在 Claude-3.5 上 ASR 为 61.60%，虽显著优于最佳越狱基线 SI-Attack 的 47.20%，但绝对水平仍低于 GPT-4o 的 87.60%，表明**强对齐模型仍是挑战边界**。

3. **计算资源需求**：从零开始对单个 VLM 进行完整评估耗时 11.75 小时（Table 15），且攻击样本生成依赖强大的多模态生成模型（Qwen-Image-Edit），这限制了在资源受限环境下的直接部署。

4. **安全评估范围**：红队测试的对象限于 VLM 的安全漏洞（有害内容生成），未涵盖其他形式的 AI 风险，如偏见、隐私泄露或事实幻觉。

### 局限与开放问题

**已识别的局限。** 消融实验揭示了几个关键瓶颈。Table 4 表明，将分层策略树替换为平铺策略库后，GPT-4o 上的 ASR 从 87.60% 骤降至 71.80%（下降 15.8 个百分点），策略多样性也同步下降，证明**树结构的层次化组织是方法有效性的必要条件**，而非可选的工程优化。Table 5 的消融进一步显示，升级执行器模型（Gemini-2.5-Pro）带来的 ASR 提升（+13.4%）显著大于升级编排器模型（+4.2%），表明**执行复杂策略的能力是当前性能瓶颈**，而非策略搜索的智能程度。Table 12 的策略可迁移性分析暴露了上游转移的弱点：从弱模型（DeepSeek-VL）到强模型（GPT-4o）的策略转移仅达 81.60% ASR，与直接在 GPT-4o 上发现的策略（87.60%）存在显著差距。

**开放问题。** 以下方向需要进一步研究：

1. **多模态扩展**：如何将策略树的探索范围扩展到音频、视频等模态的联合红队测试？这需要设计跨模态的策略表示和执行器工具集。

2. **攻防协同进化**：能否将策略发现过程与防御机制协同进化，构建更鲁棒的安全评估闭环？目前 TreeTeaming 仅作为攻击方运行，未利用防御反馈来指导策略探索。

3. **探索-利用的自动化平衡**：Figure 3(c) 显示初始探索阈值 $\tau_{\mathrm{initial}}$ 的选择至关重要——过低（0.2）会导致过早收敛到平庸策略，过高（0.8）则延迟利用阶段。默认值 0.4 在多数模型上达到最佳效果，但这是经验性选择。如何量化并自动平衡攻击策略的多样性与有效性，避免策略树的过早收敛，仍是一个开放的理论问题。

4. **编排器的学习能力**：当前编排器依赖预训练 LLM（Qwen2.5-72B）的启发式决策。是否可以通过强化学习进一步优化编排器的探索-利用决策，使其从历史红队测试经验中学习，而非仅依赖当前树状态和失败分析反馈？

5. **伦理与安全部署**：在现实世界部署中，如何确保生成的有害内容不会意外泄露？TreeTeaming 生成的攻击样本毒性虽已显著降低，但仍包含有害内容（视觉毒性 9.86%，文本毒性 6.63%），需要严格的访问控制和内容隔离机制。

## 原文 PDF

![[paperPDFs/CVPR_2026/TreeTeaming_Autonomous_Red_Teaming_of_Vision_Language_Models_via_Hierarchical_Strategy_Exploration.pdf]]
