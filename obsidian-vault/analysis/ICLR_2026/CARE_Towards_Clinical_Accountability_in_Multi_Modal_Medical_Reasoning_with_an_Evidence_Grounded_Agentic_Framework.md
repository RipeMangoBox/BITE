---
title: "CARE: Towards Clinical Accountability in Multi-Modal Medical Reasoning with an Evidence-Grounded Agentic Framework"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/CARE_Towards_Clinical_Accountability_in_Multi_Modal_Medical_Reasoning_with_an_Evidence_Grounded_Agentic_Framework.pdf
project_link: null
code_link: null
openreview_forum_id: whRAOJiyHM
aliases:
- CCFCC
- CARE
tags:
- ICLR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/vision_models_multimodal
core_operator: "将多模态医学推理拆解为三个专业化子任务——医学实体提案、实体指代分割、证据增强视觉问答，并将像素级视觉证据（如放大 ROI、二值掩码）显式地输入到推理模型中，配合代理协调器进行工具调用规划和答案一致性审查，从而打破单一模型的捷径学习路径，提升推理的准确性和问责性。"
primary_logic: "模拟临床医生“先定位异常区域→放大观察→基于证据决策”的工作流，利用解耦的专家模型（实体提案、分割、证据增强问答）和显式的视觉证据反馈回路，能够在不依赖超大规模数据和模型的情况下，显著提升医学 VQA 性能，并为答案提供可追溯的视觉依据。"
claims:
- "CARE-Flow（10B）在四项医学 VQA 基准上的平均准确率达 74.91%，超越同等规模 SOTA 基线 10.9%，并超过参数量大得多的 Lingshu-32B 2.62 个百分点。"
- "引入动态协调器后，CARE-Coord（10B）进一步将总体准确率提升至 77.54%，比 Lingshu-32B 高出 5.25 个百分点。"
- "消融实验表明，添加全部三种视觉线索（Zoom-in、Mask、Global）比不使用任何线索的基线在 ID 数据集上提升 2.5 个百分点；结合协调器审查后提升至 5.1 个百分点。"
- "人类评估中，CARE-Coord 的推理链通过率达到 82.14%，显著高于 GPT-4o 协调器的 73.94%，证明证据支撑的推理过程更受医学评估者认可。"
---

# CARE: Towards Clinical Accountability in Multi-Modal Medical Reasoning with an Evidence-Grounded Agentic Framework

> [!tip] 核心洞察
> 模拟临床医生“先定位异常区域→放大观察→基于证据决策”的工作流，利用解耦的专家模型（实体提案、分割、证据增强问答）和显式的视觉证据反馈回路，能够在不依赖超大规模数据和模型的情况下，显著提升医学 VQA 性能，并为答案提供可追溯的视觉依据。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | CARE：面向临床问责的证据驱动多模态医学推理代理框架 |
| 英文题名 | CARE: Towards Clinical Accountability in Multi-Modal Medical Reasoning with an Evidence-Grounded Agentic Framework |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=whRAOJiyHM) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/vision_models_multimodal |
| Method | CARE (CARE-Flow and CARE-Coord) |
| Dataset | Overall (OMVQA-3k, VQA-RAD, SLAKE, VQA-Med-2019), OMVQA-3k |

> [!tip] 效果简介
> - Overall (OMVQA-3k, VQA-RAD, SLAKE, VQA-Med-2019) 上，Accuracy (%) 为 77.54 (CARE-Coord-B, 10B)，对比 72.29 (Lingshu-32B)，变化 +5.25。
> - OMVQA-3k 上，Accuracy (%) 为 97.97 (CARE-Coord-B)，对比 83.97 (Lingshu-32B)，变化 +14.00。
> - VQA-RAD 上，Accuracy (%) 为 68.29 (CARE-Coord-B)，对比 64.75 (Lingshu-32B)，变化 +3.54。

## 概要

当前医学视觉语言模型（VLM）普遍采用端到端黑箱推理范式，缺乏对图像中具体视觉发现的显式定位与验证，导致模型倾向于学习浅层统计关联而非真实病理证据，从而产生幻觉和捷径学习，且无法满足临床对可解释性与可问责性的要求。

针对这一瓶颈，CARE 框架将多模态医学推理拆解为三个专业化子任务——医学实体提案、实体指代分割、证据增强视觉问答——并将像素级视觉证据（如放大 ROI、二值掩码）显式地输入到推理模型中，配合代理协调器进行工具调用规划和答案一致性审查，从而打破单一模型的捷径学习路径，提升推理的准确性和问责性。其核心洞察在于模拟临床医生“先定位异常区域→放大观察→基于证据决策”的工作流，利用解耦的专家模型和显式的视觉证据反馈回路，在不依赖超大规模数据和模型的情况下，显著提升医学 VQA 性能，并为答案提供可追溯的视觉依据。

在方法谱系中，CARE 区别于 GPT-4o、Qwen2.5-VL 等通用 VLM 的单次推理范式，也不同于仅将定位作为辅助输出而不反馈推理的接地模型。其关键创新在于：推理范式从端到端黑箱转向多阶段模块化代理推理；视觉证据从仅使用完整图像转为生成三种视觉线索（Zoom-in、Mask、Global）并直接馈送 VQA 模型；训练策略从单一 SFT 或二元奖励转向两阶段 SFT+RFT，引入基于相似度的软奖励和链式思维长度奖励并通过 DAPO 算法优化；错误纠正机制从无后验证转向协调器对思维链-答案对进行迭代一致性检查。

主要实验结果验证了该框架的有效性：CARE-Flow（10B）在四项医学 VQA 基准上的平均准确率达 74.91%，超越同等规模 SOTA 基线 10.9%，并超过参数量大得多的 Lingshu-32B 2.62 个百分点；引入动态协调器后，CARE-Coord（10B）进一步将总体准确率提升至 77.54%，比 Lingshu-32B 高出 5.25 个百分点（Table 1）。消融实验表明，添加全部三种视觉线索比无线索基线在 ID 数据集上提升 2.5 个百分点，结合协调器审查后提升至 5.1 个百分点（Table 2）。人类评估中，CARE-Coord 的推理链通过率达 82.14%，显著高于 GPT-4o 协调器的 73.94%，证明证据支撑的推理过程更受医学评估者认可（Table 18）。



### 医学多模态推理的问责困境

医学视觉问答（Medical VQA）要求模型同时理解放射影像的细微视觉特征和临床问题的语义意图，并给出可信、可追溯的答案。然而，当前主流的医学视觉语言模型（VLM）普遍采用端到端黑箱推理范式——将整幅图像和问题一次性输入模型，直接输出答案。这种范式存在根本性缺陷：模型缺乏对图像中具体视觉发现的显式定位与验证机制，导致其倾向于学习图像与答案之间的浅层统计关联，而非基于真实病理证据进行推理。

由此引发的两类核心问题严重制约了医学 VLM 的临床适用性：

1. **幻觉与捷径学习**：模型可能在未真正“看见”关键病灶的情况下给出正确答案，仅凭背景分布或文本先验做出判断。一旦测试分布发生变化，这种虚假的相关性就会崩溃。
2. **可问责性缺失**：在临床场景中，“答案是什么”远不如“为什么是这个答案”重要。端到端模型无法提供可追溯的视觉依据，使得医生难以审核、信任其输出，也无法满足医疗 AI 对可解释性的监管要求。

### 现有范式的局限

Figure 1 系统对比了当前 VLM 推理范式的不足：

- **单次推理 VLM**（Figure 1a）：一次性处理整幅图像，常因缺乏对局部关键区域的聚焦而遗漏微小病灶或细微信号。
- **定位型 VLM**（Figure 1b）：虽可输出感兴趣区域（ROI）的边界框或热力图，但定位结果仅作为辅助输出，并不显式反馈到推理过程中——模型仍然基于全局图像做决策，定位与推理是割裂的。
- **通用视觉推理 VLM**（Figure 1c）：尝试通过链式思维（CoT）进行多步推理，但初始焦点一旦错误，后续推理便会沿错误路径放大偏差，缺乏外部证据的纠偏机制。

上述范式的共同瓶颈在于：**推理过程缺乏像素级视觉证据的闭环反馈**。模型从未被要求“指出病灶在哪里、放大观察、基于所见做判断”，而这恰恰是临床医生阅片的标准工作流。

### 本文动机

CARE 的核心动机源于一个朴素但深刻的洞察：**模拟临床医生“先定位异常区域→放大观察→基于证据决策”的工作流，利用解耦的专家模型和显式的视觉证据反馈回路，能够在不依赖超大规模数据和模型的情况下，显著提升医学 VQA 性能，并为答案提供可追溯的视觉依据。**

具体而言，CARE 将多模态医学推理拆解为三个专业化子任务——医学实体提案、实体指代分割、证据增强视觉问答——并将像素级视觉证据（如放大 ROI、二值掩码）显式地输入到推理模型中，配合代理协调器进行工具调用规划和答案一致性审查。这一设计从架构层面切断了单一模型的捷径学习路径：模型被强制要求先定位、再观察、后推理，每一步都建立在可审查的视觉证据之上。

从数据效率角度看，这一思路的优势尤为突出。如 Table 10 所示，CARE 仅使用约 1 万条医学 VQA 数据训练，而 **HuatuoGPT-Vision**（Chen et al., 2024a）使用了超 100 万条数据，**Lingshu**（Xu et al., 2025）更是使用了超 1200 万条。在数据规模相差两个数量级的情况下，CARE 仍能取得领先性能，说明结构化的证据驱动范式能够更高效地利用有限监督信号。

### 核心贡献预览

CARE 框架包含两个递进版本：

- **CARE-Flow**：静态流水线版本，依次执行实体提案、分割、多线索证据增强 VQA，并通过多数投票确定最终答案。
- **CARE-Coord**：动态代理版本，引入 VLM 协调器进行工具调用规划、最优视觉线索选择和链式思维-答案一致性审查。

实验表明，CARE-Flow（10B）在四项医学 VQA 基准上的平均准确率达 74.91%，超越同等规模 SOTA 基线 10.9%，并超过参数量大得多的 Lingshu-32B 2.62 个百分点；引入动态协调器后，CARE-Coord（10B）进一步将总体准确率提升至 77.54%，比 Lingshu-32B 高出 5.25 个百分点（Table 1）。



## 核心方法与创新机理

CARE 的核心创新在于将医学多模态推理从“端到端黑箱”重构为“证据驱动的模块化代理流程”，通过三个关键维度的范式转变，系统性地打破了现有 VLM 的捷径学习路径。

### 推理范式的根本转变：从单次黑箱到多阶段代理

现有医学 VLM 普遍采用单次前向推理，模型直接基于完整图像输出答案，缺乏对图像中具体视觉发现的显式定位与验证。这种范式使模型倾向于学习浅层统计关联——例如根据图像风格而非病理特征做出判断——从而导致幻觉和问责性缺失。CARE 将推理任务分解为三个专业化子任务（医学实体提案、实体指代分割、证据增强视觉问答），并引入 VLM 协调器进行工具调用规划和答案一致性审查，模拟了临床医生“先定位异常区域→放大观察→基于证据决策”的工作流（Figure 1(d)）。

这一范式转变的因果机制在于：**解耦的专家模型各自专注于明确、可验证的子目标，阻断了端到端模型中“问题→答案”的捷径通路**。实体提案模型被迫学习问题与解剖结构之间的语义关联，分割模型被约束在像素级定位精度上，而证据增强 VQA 模型则必须基于显式视觉线索进行推理——三者协同构成了一条可追溯的证据链。

### 视觉证据的显式利用：从隐式特征到像素级反馈

现有方法对视觉信息的利用存在根本性局限：单次 VLM 仅依赖全局图像特征，定位类 VLM 虽能输出边界框或热力图，但并未将这些定位结果反馈给推理过程（Figure 1(b)）。CARE 的设计核心在于**将像素级视觉证据作为额外的输入通道显式馈送给推理模型**，具体包含三种视觉线索：

- **Zoom-in（局部放大）**：根据分割掩码裁剪并放大 ROI 区域，迫使模型聚焦于病变细节；
- **Mask（二值掩码）**：将分割掩码作为独立图像通道输入，提供精确的空间位置信息；
- **Global（全局指示）**：在全图上叠加全一掩码，保留全局上下文同时暗示关注区域。

消融实验直接验证了这一设计的因果效应：引入全部三种视觉线索后，ID 数据集准确率从无任何线索基线的 72.4% 提升至 74.9%（+2.5 个百分点）；叠加协调器审查后进一步达到 77.5%（+5.1 个百分点）（Table 2）。这证明**显式视觉证据的反馈回路是性能提升的关键杠杆**，而非仅仅是多模型集成的边际收益。

### 训练策略的精细化设计：从二元奖励到结构化 RLVR

CARE 为不同模块设计了差异化的强化学习可验证奖励（RLVR），替代了传统 SFT 或单一二元准确度奖励的粗粒度优化策略：

- **实体提案模型**采用基于语义相似度的软奖励机制：利用小语言模型计算提案实体与真实实体间的余弦相似度，通过 Kuhn-Munkres 算法找到最优匹配后取平均（Eq. 1），并辅以计数惩罚和重复惩罚（Eq. 2）。这一设计避免了硬匹配带来的稀疏奖励问题，使模型能够学习到“语义相近”的实体提案。
- **证据增强 VQA 模型**的奖励由准确度、格式和链式思维长度三项组成（Eq. 4），其中长度奖励鼓励模型生成合理长度的推理过程，避免过度简化的猜测。
- 两阶段训练策略（SFT + DAPO）使 EG-VQA 达到 74.9% 的总体准确率，相较于无训练基线提升 9.6 个百分点，而单独使用 DAPO 仅提升 6.0 个百分点（Table 3），表明 SFT 提供的初始化对 RL 策略优化具有关键支撑作用。

### 协调器审查机制：从静态管道到动态纠错

CARE-Coord 引入的协调器审查机制是区别于静态管道（CARE-Flow）的核心差异化能力。协调器不仅规划工具调用顺序和选择最优视觉线索类型，更在推理后对思维链-答案对进行迭代一致性检查，并可选择重新运行专家模型或自行修正。这一机制的因果效应体现在：CARE-Coord 将总体准确率从 CARE-Flow 的 74.91% 提升至 77.54%，比参数量大三倍的 Lingshu-32B 高出 5.25 个百分点（Table 1）。

值得注意的是，协调器的编辑行为分析显示，76% 的编辑属于成功修正，且仅 12% 涉及答案覆写（Table 8），表明审查机制主要通过修正推理逻辑而非简单替换答案来提升性能——这正是临床问责性所要求的“可追溯推理”的核心体现。



![[assets/figures/papers/paper_list_l38_https_openreview_net_forum_id_whRAOJiyHM/figures/002_Figure_2.jpg]]
*Figure 2: Method overview. The proposed CARE comprises a VLM coordinator and a set of task-specific expert models. The coordinator plans tool use and conducts answer review, invoking specialist models as needed. The expert set includes: (1) a question-conditioned entity-proposal VLM that identifies relevant anatomical structures/findings; (2) a referring segmentation model that localizes entities with pixel-level ROI evidence; and (3) an evidence-grounded VQA VLM that reasons over the image augmented with selected visual evidence (zoom-in, mask, or global indicator)*

CARE 将多模态医学推理拆解为一个由**协调器**（Coordinator）驱动的代理工作流，包含三个任务专精模块：**医学实体提案**、**实体指代分割**和**证据增强视觉问答**（EG-VQA）。其核心设计理念是模拟临床医生“先定位异常区域→放大观察→基于证据决策”的认知流程，通过显式的像素级视觉证据反馈回路来打破端到端黑箱模型的捷径学习路径。

### 工作流概览

如图 2 所示，CARE 的推理流程遵循“规划—执行—审查”的代理范式：

1. **协调器规划**：接收用户问题和医学图像后，协调器（CARE-Coord）首先规划工具调用序列，决定调用哪些专家模型以及以何种顺序执行。
2. **实体提案**：协调器调用医学实体提案 VLM，根据问题从图像中识别出最相关的解剖结构或病变实体（如“右肺上叶”“纵隔淋巴结”）。
3. **指代分割**：对提案的实体，调用实体指代分割模型生成像素级分割掩码，并输出置信度评分以过滤低质量掩码。
4. **证据增强 VQA**：从分割结果中提取三种视觉线索——**局部放大**（Zoom-in，围绕 ROI 裁剪放大）、**二值掩码**（Mask，叠加分割轮廓）和**全局指示**（Global，全一掩码表示无特定焦点）——并将其作为额外输入通道馈送给 EG-VQA 模型。该模型在原始图像与所选视觉线索的共同条件下进行链式思维推理，生成最终答案。
5. **一致性审查**：协调器对 EG-VQA 输出的思维链-答案对进行迭代一致性检查。若发现推理与答案矛盾，协调器可选择重新运行专家模型或自行修正推理逻辑，直至通过审查。

在静态版本 **CARE-Flow** 中，协调器被简化为固定的三路并行调用（对三种视觉线索各调用一次 EG-VQA），最终通过多数投票决定答案。动态版本 **CARE-Coord** 则引入 GPT-5 作为协调器，具备线索选择、工具规划和答案审查的完整代理能力。

### 模块间数据流

各模块之间的信息传递遵循严格的输入输出契约：

- **实体提案 VLM → 分割模型**：传递自然语言实体名称列表。当前实现中丢弃了实体提案同时生成的尺寸和位置信息，这一设计选择可能限制了分割精度的上限。
- **分割模型 → EG-VQA**：传递选定的视觉线索图像（Zoom-in 裁剪图、二值掩码图或全局指示图）。线索选择由协调器根据问题类型和分割置信度动态决策。
- **EG-VQA → 协调器**：传递完整的推理链（CoT）和最终答案，供协调器进行一致性审查。

### 训练策略的两阶段设计

CARE 的 VLM 组件采用统一的两阶段训练范式：

- **阶段一：监督微调（SFT）**。在医学 VQA 数据上对基础 VLM 进行指令微调，使其初步具备医学实体识别和证据增强推理能力。
- **阶段二：可验证奖励的强化学习（RLVR）**。使用 DAPO 算法对模型进行策略优化。实体提案模型的奖励函数由四项组成：基于 Kuhn-Munkres 最优匹配的**相似度奖励** $R_{\mathrm{sim}}$、限制提案数量的**计数惩罚** $R_{\mathrm{count}}$、防止重复输出的**重复惩罚** $R_{\mathrm{repetition}}$ 和**格式奖励** $R_{\mathrm{format}}$。EG-VQA 模型的奖励函数则结合了**准确度奖励** $R_{\mathrm{acc}}$、**格式奖励**和鼓励合理推理长度的**链式思维长度奖励** $R_{\mathrm{length}}$。

消融实验表明，SFT + DAPO + 长度奖励的组合策略使 EG-VQA 达到 74.9% 的总体准确率，相较于无训练基线提升 9.6 个百分点，而单独使用 DAPO 仅提升 6.0 个百分点（Table 3），验证了两阶段训练的必要性。



CARE 框架将多模态医学推理拆解为三个专业化子任务模块，并由一个代理协调器进行动态调度与审查。各模块通过可验证奖励的强化学习（RLVR）进行优化，形成“定位→分割→证据推理→一致性审查”的闭环。

### 3.1 医学实体提案模块

该模块采用一个紧凑型 VLM（基于 InternVL3-2B），根据用户问题和医学图像，生成与问题最相关的解剖结构或病变实体列表。训练采用 RLVR 策略，奖励函数由四项组成：

**相似度奖励**：利用小型语言模型计算提案实体 $\hat{e}_i$ 与真实实体 $e_j$ 间的余弦相似度 $s_{i,j}$，通过 Kuhn-Munkres 算法找到最大总相似度的最优匹配 $\mathcal{K}$，并取平均：

$$R_{\mathrm{sim}}(\hat{\mathcal{E}}, \mathcal{E}) = \frac{1}{\min(P,Q)} \sum_{(\hat{e}_i, e_j) \in \mathcal{K}} s_{i,j}$$

其中 $P$、$Q$ 分别为提案实体与真实实体的数量。该软奖励机制避免了传统二元准确度奖励对语义等价但表述不同的实体（如“肺部”与“肺实质”）的误判。

**完整实体奖励**：

$$R_{\mathrm{Entity}} = R_{\mathrm{sim}} + R_{\mathrm{count}} + R_{\mathrm{repetition}} + R_{\mathrm{format}}$$

其中 $R_{\mathrm{count}}$ 为计数惩罚（限制提案数量，避免过度输出），$R_{\mathrm{repetition}}$ 为重复惩罚（抑制同一实体的多次出现），$R_{\mathrm{format}}$ 为格式奖励（确保输出符合结构化要求）。消融实验（Table 7）表明，四项奖励协同作用使实体准确率达 85.2%，最终 VQA 性能提升至 77.5%。

### 3.2 实体指代分割模块

该模块基于 SA-Med-2D 构建，并引入一个冻结的轻量级 BERT 风格生物医学文本编码器，使其支持基于文本提示的指代分割。

**分割掩码解码**：将 SAM 编码器的图像 token 作为键/值，文本 token 的投影作为查询，通过解码器生成最终分割掩码：

$$M = \mathrm{Dec}_M(\mathrm{Enc}_{SAM}(t)[0:|t_I|], \mathrm{Proj}_T(t_T))$$

其中 $t_I$ 为图像 token，$t_T$ 为文本 token，$\mathrm{Enc}_{SAM}$ 为 SAM 编码器，$\mathrm{Proj}_T$ 为文本投影层，$\mathrm{Dec}_M$ 为掩码解码器。

**掩码置信度评分**：通过掩码概率图 $M_p$ 的归一化熵计算置信度，用于过滤低质量分割结果：

$$C(M_p) = 1 - \frac{\mathrm{Entropy}(M_p)}{\log(2)}$$

该模块在 MeCo-G 数据集上平均 Dice 达 81.9，远超可适配参考分割的 BiomedParse（30.1），为下游 VQA 提供了高质量的像素级视觉证据（Table 5）。

### 3.3 证据增强视觉问答模块（EG-VQA）

EG-VQA 模块（基于 InternVL3-8B）接收原始图像及选定的视觉线索作为额外输入通道，进行基于证据的链式思维推理。三种视觉线索类型为：

- **Zoom-in**：围绕 ROI 局部放大并裁剪
- **Mask**：二值掩码叠加
- **Global**：全 1 掩码（指示全局推理）

**EG-VQA 奖励函数**：

$$R_{\mathrm{EG-VQA}} = R_{\mathrm{acc}} + R_{\mathrm{format}} + R_{\mathrm{length}}$$

其中 $R_{\mathrm{acc}}$ 为准确度奖励（基于答案正确性），$R_{\mathrm{format}}$ 为格式奖励，$R_{\mathrm{length}}$ 为链式思维长度奖励（鼓励生成合理长度的推理过程）。消融实验（Table 3）表明，采用 SFT + DAPO + 长度奖励的训练策略使 EG-VQA 达到 74.9 的总体准确率，较无训练基线提升 9.6 个百分点。

### 3.4 DAPO 策略优化

所有 VLM 模块的 RLVR 训练均采用 DAPO（Dual-clip Advantage Proximal Policy Optimization）算法，其策略优化目标为：

$$\mathcal{I}_{\mathrm{DAPO}}(\theta) = \mathbb{E}_{y_i \sim \pi_{\mathrm{ref}}(\cdot | x)} \left[ \frac{1}{\sum_{i=1}^{G} |y_i|} \sum_{i=1}^{G} \sum_{j=1}^{|y_i|} \min \left( r_{i,j} A_{i,j}, \mathrm{clip}(r_{i,j}, 1-\epsilon_l, 1+\epsilon_h) \right) \right]$$

其中 $\pi_{\mathrm{ref}}$ 为参考模型，$G$ 为群组大小，$y_i$ 为第 $i$ 个采样响应，$r_{i,j}$ 为 token 级概率比，$A_{i,j}$ 为群组归一化后的优势函数，$\epsilon_l$ 和 $\epsilon_h$ 分别为下界和上界裁剪阈值。DAPO 通过双端裁剪和群组归一化，在稳定训练的同时有效利用高优势 token 的更新信号。

### 3.5 协调器模块

CARE-Coord 采用强大的 VLM（默认 GPT-5）作为协调器，负责三阶段操作：**规划**工具调用顺序并选择最优视觉线索类型；**执行**工具调用获取专家模型输出；**审查**对 EG-VQA 的思维链-答案对进行迭代一致性检查，识别并修正推理逻辑错误。协调器被明确指示仅审查推理过程而非直接提供答案，76% 的编辑行为属于成功的推理修正，仅 12% 涉及答案覆写（Table 8）。



## 实验与关键发现

### 核心定量结果

CARE 系列模型在四项标准医学 VQA 基准（OMVQA-3k、VQA-RAD、SLAKE、VQA-Med-2019）上展现出显著优势。如 Table 1 所示，**CARE-Flow-B（10B 总参数量）在四项基准上的平均准确率达 74.91%，超越同等规模 SOTA 基线 10.9 个百分点，并超过参数量大得多的 Lingshu-32B 2.62 个百分点**。引入动态协调器后，**CARE-Coord-B 进一步将总体准确率提升至 77.54%，比 Lingshu-32B 高出 5.25 个百分点**。

![[assets/figures/papers/paper_list_l38_https_openreview_net_forum_id_whRAOJiyHM/figures/003_Table_1.jpg]]
*Table 1: Quantitative results on medical VQA benchmarks. We report medical VQA accuracy (%) on four standard benchmarks: OMVQA-3k (Hu et al., 2024), VQA-RAD (Lau et al., 2018), SLAKE (Liu et al., 2021) and VQA-Med-2019 (Ben Abacha et al., 2019). Open-ended questions are scored by GPT-4o against ground-truth answers. Our segmentation model is smaller than 1B. We highlight medical expert VLMs in gray and ours in green*

分数据集来看，CARE-Coord-B 在 OMVQA-3k 上达到 97.97%，领先 Lingshu-32B 达 14 个百分点；在 VQA-RAD 上达到 68.29%（+3.54%）；在 SLAKE 上，CARE-Flow-B 以 83.21% 略优于 Lingshu-32B 的 82.25%；在分布外数据集 VQA-Med-2019 上，CARE-Coord-B 达到 60.80%（+2.60%）。值得注意的是，**CARE 仅使用约 1 万条医学 VQA 数据训练，而 Lingshu 使用了超 1200 万条数据**（Table 10），凸显了该框架的数据效率优势。在相同训练数据下与微调的 InternVL3 基线对比，CARE-Flow-S 和 CARE-Flow-B 仍分别领先 4.23 和 4.08 个百分点（Table 14），排除了数据差异的影响。

### 消融实验

#### 视觉证据的作用

Table 2 的消融实验揭示了视觉线索对 EG-VQA 性能的关键影响。**在训练中引入全部三种视觉线索（Zoom-in、Mask、Global）后，ID 数据集准确率由不使用任何线索的基线 72.4% 提升至 74.9%（+2.5 个百分点）**。进一步叠加协调器审查后，准确率达到 77.5%（+5.1 个百分点）。这表明显式的像素级视觉证据反馈回路是打破端到端黑箱推理瓶颈的核心机制。

![[assets/figures/papers/paper_list_l38_https_openreview_net_forum_id_whRAOJiyHM/figures/004_Table_2.jpg]]
*Table 2: Ablation on grounded VQA. We ablate the 8B EG-VQA components during training, varying training visual evidence and coordinator configurations. Only one type of visual evidence is used for inference. CARE-Flow and CARE-Coord are highlighted in blue and green, respectively*

#### 训练策略对比

Table 3 对比了不同的 EG-VQA 训练策略。**采用 SFT + DAPO + 长度奖励的完整训练策略使 EG-VQA 达到 74.9% 的总体准确率，相较于无训练基线（65.3%）提升 9.6 个百分点**。单独使用 DAPO 仅提升 6.0 个百分点（达到 71.3%），而 SFT + DAPO 的组合（不含长度奖励）为 73.9%。长度奖励的加入额外贡献约 1 个百分点，验证了鼓励生成合理长度推理链对性能的正向影响。

![[assets/figures/papers/paper_list_l38_https_openreview_net_forum_id_whRAOJiyHM/figures/005_Table_3.jpg]]
*Table 3: Ablation on training strategy for EG- Table 4: Ablation on coordinator. We ablate VQA. We ablate different training strategies for EG- different coordinators. “S” denotes using a VQA VLM. We adopt the CARE-Flow in this abla- single selected visual evidence. tion to exclude the coordinator’s effects. Coordinator Infer. Clue ID OOD Overall*

#### 协调器选择

Table 4 评估了不同协调器对整体性能的影响。**GPT-5 作为协调器效果最佳，总体准确率达 77.5%**，显著优于多数投票策略的 CARE-Flow（74.9%）和使用 InternVL3-38B 作为协调器的方案（74.0%）。GPT-4o 协调器达到 75.0%，微调后的 InternVL3-8B 协调器为 75.6%。结果表明，协调器的推理能力越强，审查和修正的效果越好。

![[assets/figures/papers/paper_list_l38_https_openreview_net_forum_id_whRAOJiyHM/figures/006_Table_4.jpg]]

#### 分割模型的影响

Table 5 显示，**自研的实体指代分割模型在 MeCo-G 数据集上平均 Dice 达 81.9，远超 BiomedParse 的 30.1**。当将 BiomedParse 替换到 CARE 框架中时，医学 VQA 总体性能从 77.5% 下降至 74.1%，验证了高质量像素级定位对下游推理的关键支撑作用。

#### 实体提案训练策略

Table 6 的消融表明，**采用 Kuhn-Munkres 匹配算法和相似度软奖励的实体提案模型，实体准确率达 85.2%，分割 Dice 达 73.4，最终 VQA 准确率提升至 77.5%**。相比之下，仅使用 RFT 的基线（Baseline #1）实体准确率仅 72.3%，VQA 为 74.1%。使用二分匹配替代 KM 算法（Baseline #2）使实体准确率降至 80.1%。Table 7 进一步验证了实体奖励各组分的作用：移除相似度奖励使 VQA 降至 74.9%，移除计数惩罚降至 74.8%，移除重复惩罚降至 74.6%。

### 协调器编辑分析

Table 8 对协调器的编辑行为进行了分类统计。**76% 的编辑行属于成功修正，仅 12% 涉及答案覆写**，表明协调器主要修正推理逻辑而非简单替代答案。这一发现支持了协调器作为“验证者”而非“答案提供者”的设计理念（Figure 10 的系统提示）。协调器在多数情况下保留了 EG-VQA 专家的原始答案，仅修正推理链中的不一致之处。

### 推理时间开销

Table 12 报告了推理延迟。使用 GPT-5 协调器时，单次 VQA 请求约需 43 秒，其中协调器审查占主要开销。相比之下，静态管道 CARE-Flow 仅需约 6 秒。这一差距表明，**在实时临床应用中，CARE-Coord 的延迟是当前框架的主要瓶颈**，训练小型 VLM 替代 GPT-5 作为协调器是降低延迟的潜在方向。

### 失败模式与局限

尽管 CARE-Coord 在多数场景下表现出色，但仍存在可识别的失败模式。Figure 20 的失败案例显示，**协调器有时会引入幻觉并覆盖专家模型的正确答案，尤其在多次迭代审查中**。实体提案模型当前仅使用生成的实体名称，丢弃了同时生成的尺寸和位置信息，可能限制分割的准确性。此外，分割模型主要在 CT 和 PET 模态上评估，其在 MRI、超声等其他成像模态上的泛化能力尚未充分验证。人类评估仅招募了 9 名医学生，样本量较小且缺乏临床专家参与，可能影响问责性结论的外部有效性（Table 18 显示 CARE-Coord 推理链通过率为 82.14%，高于 GPT-4o 协调器的 73.94%，但评估者背景限制了结论的推广性）。

![[assets/figures/papers/paper_list_l38_https_openreview_net_forum_id_whRAOJiyHM/figures/026_Table_18.jpg]]
*Table 18: Reasoning Trace Human Evaluation. We conduct a human evaluation that evaluates the quality of the reasoning trace of our model on a subset of samples. We report the pass rate of human evaluation. We compare our CARE-Coord-B against our model with the GPT-4o coordinator. Our method is highlighted in green*

### 评测稳定性

Table 16 验证了不同 LLM-as-Judge 的评分一致性。在四项基准测试中，使用 GPT-4o、GPT-4o-mini、InternVL3-38B-Instruct 和 InternVL3-78B-Instruct 作为评委时，**评分标准差小于 1%，证明评测结果的波动不会改变主要结论**，CARE 的性能优势在不同评委下保持稳健。



## 定位与知识库关联

### 1. 与现有医学 VLM 推理范式的对比

CARE 的核心贡献在于将多模态医学推理从“端到端黑箱”转变为“证据驱动的模块化代理推理”。这一转变直接回应了现有范式的三个结构性缺陷（Figure 1）：

| 范式 | 代表工作 | 核心缺陷 | CARE 的改进 |
|------|----------|----------|-------------|
| **单次推理 VLM** | GPT-4o (Hurst et al., 2024)、Qwen2.5-VL (Bai et al., 2025)、InternVL3 (Zhu et al., 2025a)、Lingshu (Xu et al., 2025) | 仅使用完整图像，无显式 ROI 定位，易遗漏局部病变证据 | 引入像素级分割掩码和局部放大作为额外视觉输入通道 |
| **定位增强 VLM** | DeepEyes (Zheng et al., 2025) | 虽能生成边界框，但不将定位结果反馈入推理过程 | 将分割掩码作为 VQA 模型的直接输入，形成证据反馈回路 |
| **通用视觉推理 VLM** | MedVLM-R1 (Pan et al., 2025) | 依赖初始视觉焦点，若初始关注区域错误则推理链崩溃 | 通过实体提案模型显式提名候选解剖结构，再由协调器选择最优证据视图 |

从模型规模-性能关系看（Figure 1(e)），CARE-Flow（10B）以 74.91% 的平均准确率超越同等规模 SOTA 基线 10.9 个百分点，并超过参数量大三倍的 Lingshu-32B（72.29%）2.62 个百分点。CARE-Coord（10B）进一步将差距扩大至 5.25 个百分点（77.54% vs. 72.29%）。这一“小模型反超大模型”的现象表明，**结构化的证据利用策略可以有效弥补模型规模的不足**。

### 2. 训练策略谱系中的定位

CARE 采用 **SFT + RLVR（带可验证奖励的强化学习）** 的两阶段训练策略，与现有医学 VLM 的训练范式形成对比：

| 训练策略 | 代表工作 | 特点 | CARE 的差异化 |
|----------|----------|------|---------------|
| 纯 SFT | LLaVA-Med (Li et al., 2023)、HuatuoGPT-Vision (Chen et al., 2024a) | 依赖大规模标注数据 | 仅使用约 1 万条数据，数据效率显著更高（Table 10） |
| SFT + 单一 RL 奖励 | MedVLM-R1 (Pan et al., 2025) | 仅使用二元准确度奖励 | 引入基于相似度的软奖励 $R_{\mathrm{sim}}$、计数/重复惩罚和链式思维长度奖励 $R_{\mathrm{length}}$ |
| RLVR 算法 | 通用 GRPO | 标准群组相对策略优化 | 采用 DAPO 算法（Eq. (5)），通过群组归一化优势函数和 token 级裁剪实现更稳定的策略更新 |

消融实验（Table 3）证实：SFT + DAPO + 长度奖励的组合使 EG-VQA 达到 74.9% 总体准确率，相较于无训练基线提升 9.6 个百分点；单用 DAPO 仅提升 6.0 个百分点，表明 SFT 提供的初始化对后续 RL 优化至关重要。

### 3. 分割模型在医学 AI 工具链中的角色

CARE 中的实体指代分割模型基于 SA-Med-2D 构建，通过冻结的生物医学文本编码器实现文本到掩码的映射（Eq. (3)）。与传统医学分割模型相比：

| 模型 | 能力 | MeCo-G 平均 Dice | 对 VQA 的影响 |
|------|------|------------------|---------------|
| BiomedParse (Zhao et al., 2024) | 通用医学图像分割，可适配参考分割 | 30.1 | 替换后 VQA 降至 74.1% |
| CARE 自研分割模型 | 专为实体指代分割训练 | **81.9** | 支撑 VQA 达 77.5% |

BiomedParse 的低 Dice 可能源于其并非专为开放文本提示设计，这一对比需谨慎解读（见 fairness_notes）。但 81.9 vs. 30.1 的巨大差距表明，**针对指代分割任务进行专门优化是保障下游 VQA 性能的关键环节**。

### 4. 协调器机制的创新与边界

CARE-Coord 引入的协调器（以 GPT-5 为默认实现）承担工具调用规划和答案一致性审查双重职能。与其他后验证策略的对比（Table 4）：

| 协调策略 | 总体准确率 | 特点 |
|----------|-----------|------|
| 多数投票（CARE-Flow） | 74.9% | 静态管道，无选择性证据利用 |
| InternVL3-38B 协调器 | 74.0% | 开源模型协调能力有限 |
| GPT-4o 协调器 | 76.3% | 推理能力弱于 GPT-5 |
| **GPT-5 协调器** | **77.5%** | 最强推理能力，但延迟约 43 秒/请求 |

协调器编辑分析（Table 8）显示，76% 的编辑为成功修正，仅 12% 涉及答案覆写，表明审查主要修正推理逻辑而非简单替代答案。然而，协调器有时会引入幻觉并覆盖专家模型的正确答案（见失败案例 Figure 20），这是当前设计的核心脆弱点。

### 5. 适用边界与局限

**适用边界**：
- 任务范围：当前仅针对医学 VQA 设计，未扩展到诊断推荐或临床决策支持
- 模态覆盖：分割模型主要在 CT 和 PET 上评估，MRI、超声等模态的泛化能力未验证
- 数据规模：训练数据约 1 万条，在更大规模真实世界数据上可能存在泛化局限

**已知局限**：
1. **协调器幻觉风险**：多次迭代中协调器可能引入幻觉并覆盖专家正确答案
2. **实体信息利用不充分**：实体提案模型生成的尺寸和位置信息被丢弃，仅保留实体名称
3. **推理延迟**：CARE-Coord 单次请求约 43 秒（Table 12），远高于静态管道的约 6 秒，实时临床应用受限
4. **人类评估样本量小**：仅 9 名医学生参与评估，缺乏临床专家，影响问责性结论的外部有效性

### 6. 开放问题

1. **协调器幻觉抑制**：如何设计机制以减少甚至消除协调器在审查过程中引入的幻觉风险？
2. **轻量化协调器**：能否训练小型 VLM（如 8B）替代 GPT-5，在保持性能的同时大幅降低推理成本和延迟？
3. **多模态实体提案**：实体提案是否可利用放射科报告等额外多模态信息提升与问题的相关性？
4. **证据融合架构**：当前将像素级掩码作为辅助图像输入，是否存在更高效的跨注意力融合架构？
5. **3D 影像扩展**：该方法在 CT 体积数据中的扩展性如何？分割和证据馈送流程需做哪些适应性改造？
6. **多实例区分**：当图像中存在多个相同语义实体（如多个肺结节）时，分割模型能否有效区分并一一提供证据？
7. **临床信任度**：在真实临床环境中，显式视觉证据如何影响放射科医生对 AI 辅助的信任度和决策效率？



## 原文 PDF

![[paperPDFs/ICLR_2026/CARE_Towards_Clinical_Accountability_in_Multi_Modal_Medical_Reasoning_with_an_Evidence_Grounded_Agentic_Framework.pdf]]
