---
title: "CounselBench: A Large-Scale Expert Evaluation and Adversarial Benchmarking of Large Language Models in Mental Health Question Answering"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/CounselBench_A_Large_Scale_Expert_Evaluation_and_Adversarial_Benchmarking_of_Large_Language_Models_in_Mental_Health_Question_Answering.pdf
project_link: null
code_link: https://github.com/llm-eval-mental-health/CounselBench
openreview_forum_id: 8MBYRZHVWT
aliases:
- CounselBench
tags:
- ICLR_2026
- topic/benchmarks_datasets_evaluation
- topic/benchmarks_datasets_evaluation/benchmark_eval
core_operator: "引入由临床专家定义的六维评估标准（整体质量、共情、特异性、医疗建议、事实一致性、毒性）并开展大规模专业人工标注，从而实现系统性、可复现的比较。"
primary_logic: "LLM虽然在多数维度得分较高，但仍频繁出现无建设性反馈、过度泛化、缺乏共情等失效模式，且LLM作为评估者会系统性高估回答质量、忽视安全风险，因此必须通过专家设计的对抗性测试才能暴露模型的临床脆弱性。"
claims:
- "CounselBench-Eval包含2000条由100位精神卫生专业人士对GPT-4、LLaMA 3、Gemini和在线人类治疗师回答的专家评估。"
- "每条回答均基于六个临床维度进行评分，并附有片段级标注及书面理由。"
- "LLM裁判系统性高估模型回答，并忽略人类专家识别的安全隐患。"
- "CounselBench-Adv是一个包含120道由专家撰写的对抗性心理健康问题的数据集，旨在触发特定模型失效模式。"
---

# CounselBench: A Large-Scale Expert Evaluation and Adversarial Benchmarking of Large Language Models in Mental Health Question Answering

> [!tip] 核心洞察
> LLM虽然在多数维度得分较高，但仍频繁出现无建设性反馈、过度泛化、缺乏共情等失效模式，且LLM作为评估者会系统性高估回答质量、忽视安全风险，因此必须通过专家设计的对抗性测试才能暴露模型的临床脆弱性。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | CounselBench：心理健康问答领域大规模语言模型的专家评估与对抗性基准 |
| 英文题名 | CounselBench: A Large-Scale Expert Evaluation and Adversarial Benchmarking of Large Language Models in Mental Health Question Answering |
| 会议/期刊 | ICLR 2026 (Oral) |
| Links | [paper](https://openreview.net/forum?id=8MBYRZHVWT) · [GitHub](https://github.com/llm-eval-mental-health/CounselBench) |
| Topic | #topic/benchmarks_datasets_evaluation #topic/benchmarks_datasets_evaluation/benchmark_eval |
| Method | CounselBench |
| Dataset | CounselBench-Eval |

> [!tip] 效果简介
> - CounselBench-Eval 上，Overall Quality (1-5) 为 LLaMA-3.3 (4.29)，对比 Online Human Therapists (2.60)，变化 +1.69。
> - CounselBench-Eval 上，Empathy (1-5) 为 LLaMA-3.3 (4.22)，对比 Online Human Therapists (2.72)，变化 +1.50。
> - CounselBench-Eval 上，Toxicity (1-5, lower better) 为 GPT-3.5-Turbo judge gave 1.0，对比 Human Expert Average 1.78，变化 -0.78 (LLM judge underestimates toxicity)。

## 概要

### 问题瓶颈

现有医学问答基准主要依赖多项选择题或事实性验证任务，无法评估真实患者提出的开放式心理健康问题。尤其在安全性、共情和语境敏感性等维度上，缺乏系统性的评估框架，导致大语言模型（LLM）在心理健康领域的临床脆弱性长期未被暴露。

### 核心结论

CounselBench 通过两项互补设计揭示了三个关键发现：

1. **LLM 在多数临床维度上得分高于在线人类治疗师，但存在系统性失效模式。** 在整体质量、共情、特异性等维度上，LLaMA-3.3 等模型的专家评分显著优于在线人类治疗师；然而，低分回答的分析显示，GPT-4 频繁提供无建设性反馈（49.3%），LLaMA-3.3 过度泛化或妄下判断（66.7%），Gemini-1.5-Pro 缺乏共情（44.1%），在线人类治疗师同样存在过度泛化问题（46.7%）。

2. **LLM 作为评估者不可靠。** 九种高级 LLM 在担任自动裁判时，系统性高估模型回答质量，并忽略人类专家识别的安全隐患——例如在毒性维度上，LLM 裁判给出的评分（1.0）远低于人类专家的平均评分（1.78），严重低估了风险。

3. **对抗性测试暴露深层缺陷。** 基于 CounselBench-Eval 中发现的失效模式，临床专家撰写了 120 道对抗性问题（CounselBench-Adv）。在该基准上，GPT-5 的 therapy 失效模式触发率高达 0.85，且少样本提示对多数失效模式的改善微乎其微，表明这些缺陷根植于预训练层面的深层局限性。领域特定模型（如 Meditron-70B）在开放式问答中更有 80% 的回答被判为无效。

### 方法定位

CounselBench 的因果杠杆在于**将临床专家的结构化判断大规模引入评估流程**。其方法谱系可定位于以下坐标：

- **评估范式**：从选择题/事实性评分转向六维临床标准（整体质量、共情、特异性、医疗建议、事实一致性、毒性）的专家标注，每条回答由 5 名独立专业人士评估，并附有片段级标注及书面理由。
- **专家规模**：招募 100 名持证或受专业训练的精神卫生从业者，远超以往小规模或无非临床背景的评估设置。
- **对抗性测试**：区别于事后分析或文献驱动的红队测试，CounselBench-Adv 由 10 名临床专家基于 CounselBench-Eval 中观察到的精细失效模式撰写对抗性问题，实现了经验驱动的压力测试。

### 主要结果速览

| 基准 | 关键指标 | 最佳模型/系统 | 对比基线 | 差异 |
|------|----------|---------------|----------|------|
| CounselBench-Eval | 整体质量（1-5） | LLaMA-3.3: 4.29 | 在线人类治疗师: 2.60 | +1.69 |
| CounselBench-Eval | 共情（1-5） | LLaMA-3.3: 4.22 | 在线人类治疗师: 2.72 | +1.50 |
| CounselBench-Adv | Therapy 失效模式率 | GPT-5: 0.85 | GPT-3.5-Turbo: 0.05 | +0.80 |
| CounselBench-Adv | LLM-as-Judge F1 | Claude-3.7-sonnet: 0.50 | GPT-4: 0.35 | +0.15 |

评分者间信度方面，Krippendorff's alpha 在整体质量（0.82）、共情（0.83）和特异性（0.82）上达到良好水平，事实一致性（0.75）和毒性（0.72）也处于可接受范围，表明评估框架具有稳健的可复现性。

心理健康服务的供需鸿沟持续扩大。全球范围内，精神卫生专业人员严重短缺，而寻求支持的人数却在快速增长。在这一背景下，大语言模型（LLMs）被寄予厚望，有望在心理支持、初步筛查和资源引导等环节提供补充性帮助。然而，心理健康领域对回答的安全性、共情能力和语境敏感性有着极高的要求——一句不当的回应可能对处于脆弱状态的用户造成实质性伤害。

现有医学问答基准的评估范式与这一现实需求之间存在根本性脱节。主流基准主要依赖多项选择题或事实性任务来评判模型能力，无法捕捉真实患者提出的开放式问题所蕴含的复杂性和情感张力。更关键的是，这些基准几乎不涉及对共情表达、建议特异性、毒性风险等临床核心维度的系统评估。当LLMs被部署到心理健康这一高风险、高主观性的领域时，评估工具的缺失意味着我们对其失效模式和安全边界几乎一无所知。

CounselBench正是针对这一评估缺口而构建的。其核心动机并非简单地宣称LLMs比人类治疗师“更好”或“更差”，而是通过引入由临床专家定义的六维评估标准和大规模专业人工标注，建立一个可复现、可审计的比较框架。同时，该工作认识到标准评估的局限性——LLMs可能在常规测试中表现良好，却在对抗性情境下暴露深层脆弱性。因此，CounselBench进一步设计了由专家撰写的对抗性测试集，以系统性地探测模型在临床场景中的精确定向失败模式。

## 核心方法与创新机理

CounselBench的核心创新在于将心理健康问答的评估从以事实准确性或选择题得分为中心的范式，转向以临床专家定义的多维标准、大规模专业人工标注和对抗性压力测试为支柱的系统性基准。这一转变通过三个关键槽位的改变实现。

### 从单一事实准确性到六维临床评估标准

现有医学问答基准主要依赖事实准确性或多项选择题得分，无法捕捉真实患者开放性问题中至关重要的安全性、共情和语境敏感性。CounselBench引入了由临床文献支撑的六维评估标准：**整体质量**（Overall Quality）、**共情**（Empathy）、**特异性**（Specificity）、**医疗建议**（Medical Advice，二元标记是否给出医疗指导）、**事实一致性**（Factual Consistency）和**毒性**（Toxicity）。每条回答需在这六个维度上接受评分，并附有片段级标注和书面理由。这一多维框架使得评估能够区分“回答正确但缺乏共情”与“回答共情但事实有误”等细微差异，而传统基准对此完全失明。

### 从无临床参与或小规模专家组到百名持证专业人士的大规模标注

此前的工作或缺乏临床专家参与，或仅依赖极小规模的专家组，导致评估的权威性和可复现性不足。CounselBench通过Upwork招募了100名持有执照或经过专业培训的美国精神卫生从业者，其资质涵盖32种执照/学位类型和43个专业咨询领域。每位回答者（GPT-4、LLaMA-3.3、Gemini-1.5-Pro及在线人类治疗师）对100道真实患者问题的回答均由5名独立专家评估，最终形成包含2000条专家评估的CounselBench-Eval数据集。评分者间信度（Krippendorff's alpha）在五个序数维度上均达到≥0.7的实质性一致水平（整体质量0.82、共情0.83、特异性0.82、事实一致性0.75、毒性0.72），为后续分析提供了可靠的统计基础。

### 从事后分析或文献驱动红队测试到经验驱动的对抗性基准

传统方法对模型失效的分析多为事后总结或基于文献假设的红队测试，难以系统性地暴露模型在临床场景中的脆弱性。CounselBench-Adv的构建遵循“先观察、再攻击”的闭环：10名临床专家深入审查CounselBench-Eval中专家理由和低分回答，提炼出六类精细失效模式（如提供无建设性反馈、过度泛化或妄下判断、缺乏共情等），然后针对每种模式撰写120道对抗性问题，旨在精确触发目标缺陷。这种经验驱动的对抗性设计使得基准能够揭示常规评估中隐藏的风险——例如，GPT-5在“提供治疗建议”这一失效模式上的触发率高达0.85，而GPT-3.5-Turbo仅为0.05，表明模型能力的提升反而可能放大特定类型的安全隐患。

### LLM作为评估者的系统性偏差揭示

CounselBench的另一个关键发现并非预设的创新点，而是通过严格对比人类专家与九种高级LLM法官的评分自然浮现的：LLM法官系统性高估模型回答质量，并在毒性维度上几乎一致地给出最低分，完全忽略了人类专家识别的安全隐患。在模型排名上，LLM法官一致将人类专家评价最低的Gemini-1.5-Pro排在GPT-4之上，暴露出自动评估在心理健康这一高风险主观领域的根本性不可靠。这一发现本身构成了对“LLM-as-Judge”范式在该领域适用性的重要警示。

综上，CounselBench通过评估标准的临床化、标注过程的专业化，以及对抗性测试的经验化三个槽位的改变，将心理健康LLM评估从“回答是否正确”推进到“回答是否安全、共情且适用于具体求助者”的层面，为后续研究和安全部署提供了可复现的衡量框架。

![[assets/figures/papers/paper_list_l29_https_openreview_net_forum_id_8MBYRZHVWT/figures/001_Figure_1.jpg]]
*Figure 1: Overview of COUNSELBENCH benchmark. COUNSELBENCH-EVAL (left) includes expert evaluation of LLMs and online human therapist responses to real counseling questions. COUNSELBENCH-ADV (right) includes adversarial questions authored by clinicians to target identified LLM failure modes. See Appendix B for license/degree types and specialization areas*

CounselBench 是一个面向心理健康问答的双轨评估基准，由两个互补模块构成：**CounselBench‑Eval** 和 **CounselBench‑Adv**。前者通过大规模专家人工标注，系统评估大语言模型（LLM）与在线人类治疗师在真实患者开放性问题上的回答质量；后者则基于前者暴露的精细失效模式，构建对抗性测试集以探测模型的临床脆弱性。

### 核心流水线

整个基准的构建与评估流程可归纳为五个串联模块：

1. **问题筛选**  
   从公共论坛 CounselChat 中按 20 个常见心理健康主题各选取 5 个最高赞问题，形成 100 道真实患者提问。这些提问均为开放式、非结构化的求助帖，覆盖抑郁、焦虑、创伤等高频议题。

2. **回答生成**  
   将上述 100 道问题分别输入三个 LLM（GPT‑4‑0613、LLaMA‑3.3‑70B‑Instruct、Gemini‑1.5‑Pro）并收集在线人类治疗师对同一问题的原始回复，构成四组待评估回答。

3. **专家标注**  
   招募 100 名持有执照或经过专业培训的美国精神卫生从业者，通过 Qualtrics 问卷对每条回答进行六个临床维度的评分（整体质量、共情、特异性、医疗建议、事实一致性、毒性），同时完成片段级标注和书面理由撰写。每条回答由 5 名独立专家评估，最终产生 2000 条专家评估记录。

4. **对抗性数据集构建**  
   基于 CounselBench‑Eval 中专家理由和低分回答的深度审查，提炼出六类精细失效模式（如提供无建设性反馈、过度泛化/妄下判断、缺乏共情等）。10 名临床专家针对每类失效模式撰写 12 道对抗性提问，共计 120 道题目，再交由另外 5 名专家标注失效模式是否被触发。

5. **LLM‑as‑Judge 验证**  
   为检验自动评估的可靠性，测试九种高级 LLM（包括 GPT‑4、Claude‑3.7‑Sonnet 等）作为“裁判”的表现。所有模型被提示相同的问答对及人类专家使用的评估标准，其评分和失效检测结果与人类专家标注进行对比。

### 模块间关系与数据流

CounselBench‑Eval 与 CounselBench‑Adv 之间形成“发现—验证”的闭环：Eval 阶段通过大规模专家标注识别出 LLM 回答中反复出现的失效模式及其分布，Adv 阶段则将这些模式转化为可复现的对抗性探测题。两个模块共享同一套六维评估标准，确保从一般性质量评估到针对性压力测试的度量一致性。

LLM‑as‑Judge 验证横跨两个模块：在 Eval 中与人类专家评分对比，揭示 LLM 裁判系统性高估回答质量、忽视毒性等安全风险；在 Adv 中则评估 LLM 裁判能否准确检测预设的失效模式（最佳 F1 仅 0.50）。这一设计直接回应了“LLM 能否在高风险主观领域充当可靠评估者”的核心开放问题。

### 输入输出流

- **输入**：CounselChat 真实患者提问（Eval）或临床专家撰写的对抗性提问（Adv）。
- **处理**：LLM 或人类治疗师生成回答 → 多维度专家人工标注 → 失效模式分类。
- **输出**：各模型在六个维度上的平均得分、评分者间信度（Krippendorff’s α）、各失效模式触发比例、LLM 裁判与人类专家的一致性指标。

整个框架的概览见 **Figure 1**，其中左侧展示 CounselBench‑Eval 的评估流水线，右侧展示 CounselBench‑Adv 的对抗性构建与测试流程。

### 核心模块

CounselBench 基准由两个互补模块构成，分别针对标准评估与压力测试。

**模块一：CounselBench‑Eval（专家评估基准）**

该模块构建了一条从真实患者问题到多维度专家标注的完整流水线，包含四个子环节：

1. **问题筛选**：从公共论坛 CounselChat 中选取覆盖 20 个常见心理健康主题的 100 个真实患者问题，每个主题选取获赞最高的 5 个问题。
2. **回答生成**：对每个问题，分别由 GPT‑4‑0613、LLaMA‑3.3‑70B‑Instruct、Gemini‑1.5‑Pro 以及在线人类治疗师生成回答。
3. **专家标注**：通过 Upwork 招募 100 名持有执照或经过专业培训的美国心理健康从业者，在 Qualtrics 平台上对每条回答进行六维评估。每条回答由 5 名独立专家评分，标注内容包括 Likert 量表打分、片段级标注及书面理由。评估前经过三轮共 8 名参与者的试点研究以优化问卷设计。
4. **LLM‑as‑Judge 验证**：以相同的评估标准提示 9 个高级 LLM 作为自动评估器，将其评分与人类专家评分进行系统对比。

**模块二：CounselBench‑Adv（对抗性基准）**

该模块基于 CounselBench‑Eval 中暴露的模型失效模式，构建针对性压力测试集：

1. **失效模式提炼**：对 CounselBench‑Eval 中的专家理由和低分回答进行深度审查，提取出六类精细的模型失效模式。
2. **对抗性问题构建**：重新聘用 10 名心理健康专业人士，每人针对 6 类失效模式各撰写 2 个对抗性问题（共 120 个问题），旨在触发特定模型漏洞。
3. **失效模式标注**：另由 5 名专家以分类方式（“是”/“否”/“不确定”）标注每个回答中是否存在目标失效模式，标注任务配备临床专家撰写的定义和每类失效模式的一个上下文示例。

### 评估维度定义

CounselBench 的六维评估标准由文献支撑的循证维度构成，各维度操作化定义如下：

- **整体质量（Overall Quality）**：对回答的整体临床适宜性进行综合判断。
- **共情（Empathy）**：衡量回答是否展现出对用户情绪状态的准确理解和情感协调。
- **特异性（Specificity）**：评估回答在多大程度上针对用户的具体情境和需求进行了个性化调整。
- **医疗建议（Medical Advice）**：以二元方式标注回答是否提供了医疗建议。
- **事实一致性（Factual Consistency）**：评估回答中陈述的事实信息是否准确可靠。
- **毒性（Toxicity）**：检测回答中是否存在有害、冒犯性或可能对用户造成伤害的内容。

### 公式推导

本文未引入新的理论公式或算法推导。评估体系的核心统计方法为评分者间信度计算，采用 Krippendorff’s alpha（序数型）衡量 5 名独立专家在各维度上的一致性。该系数定义为：

$$ \alpha = 1 - \frac{D_o}{D_e} $$

其中 $D_o$ 为观测不一致度，$D_e$ 为期望不一致度。该系数不适用于二元的医疗建议维度。CounselBench‑Eval 中各维度的平均 alpha 值为：整体质量 0.82、共情 0.83、特异性 0.82、事实一致性 0.75、毒性 0.72，均达到实质性至良好的一致性水平（≥0.7）。

## 实验与关键发现

### 专家评估主结果：LLaMA-3.3 全面领先，但所有模型均存在显著失效

CounselBench-Eval 的核心结果（Table 1）揭示了 LLM 在心理健康问答中的表现格局。**LLaMA-3.3-70B-Instruct 在六个维度中的五个维度上取得了最高评分**，尤其在整体质量（4.29 vs. 人类治疗师 2.60，Δ=+1.69）和共情（4.22 vs. 2.72，Δ=+1.50）上大幅领先。GPT-4 和 Gemini-1.5-Pro 的整体评分分别为 3.28 和 3.12，虽高于在线人类治疗师（2.60），但显著低于 LLaMA-3.3。值得注意的是，**所有模型在医疗建议（Medical Advice）维度上的“是”比例均较低**（LLaMA-3.3 为 0.14，人类治疗师为 0.17），表明模型在避免给出具体医疗指导方面表现相对保守。

![[assets/figures/papers/paper_list_l29_https_openreview_net_forum_id_8MBYRZHVWT/figures/004_Table_1.jpg]]
*Table 1: Average expert ratings of counseling responses across six evaluation criteria. Each response was rated by five mental health professionals; scores were first averaged by question, then by model. Responses marked ”I am not sure” were excluded. For Medical Advice, the percentage of “Yes” responses was computed per question (excluding “I’m not sure”) and averaged over all questions*

评估者间信度（Table 2）显示 Krippendorff's alpha 在所有维度上均 ≥ 0.72：整体评分 0.82，共情 0.83，特异性 0.82，事实一致性 0.75，毒性 0.72。这一结果验证了六维评估框架在临床专业人士中的可复现性，为后续分析提供了可靠基础。

![[assets/figures/papers/paper_list_l29_https_openreview_net_forum_id_8MBYRZHVWT/figures/005_Table_2.jpg]]
*Table 2: Mean (over questions) Krippendorff’s alpha (ordinal); not applied to binary Medical Advice*

### 失败模式分析：模型特异性缺陷

对低评分回答（整体评分 ≤ 2）的错误分类分析（Figure 7）揭示了各模型的**特异性失效模式**：

![[assets/figures/papers/paper_list_l29_https_openreview_net_forum_id_8MBYRZHVWT/figures/021_Figure_7.jpg]]
*Figure 7: Frequency of error categories for responses that earned an overall score ≤2. Totals above each group denote the number of low-scoring responses; bar heights show how often each specific reason*

- **GPT-4**：最常见的问题是无建设性反馈（49.3%），即回答虽然安全但缺乏实质性帮助。
- **LLaMA-3.3**：过度泛化或妄下判断占比最高（66.7%），反映其在缺乏充分信息时倾向于给出笼统或武断的回应。
- **Gemini-1.5-Pro**：缺乏共情是最突出的问题（44.1%），表明其在情感协调方面存在系统性不足。
- **在线人类治疗师**：同样存在过度泛化问题（46.7%），说明这一缺陷并非 LLM 独有，但在 LLaMA-3.3 中尤为严重。

这些发现表明，即使整体评分较高的模型，其失败模式也存在质的差异——高评分可能掩盖了特定场景下的临床脆弱性。

### LLM-as-Judge 系统性偏差：高估与安全盲区

Figure 3 的六维对比分析揭示了 LLM 作为自动评估者的**系统性偏差**。九款高级 LLM 法官在事实一致性维度上频繁给出满分或接近满分的评分，而人类专家则显示出更大的区分度。更关键的是，**所有 LLM 法官在毒性维度上几乎一致地给出了最低评分**（接近 1.0），与人类专家的平均评分（GPT-4 为 1.78，Table 1）形成鲜明对比。这表明 LLM 法官系统性地忽视了人类专家识别出的安全隐患。

![[assets/figures/papers/paper_list_l29_https_openreview_net_forum_id_8MBYRZHVWT/figures/006_Figure_3.jpg]]
*Figure 3: Average evaluation scores across six dimensions (subplots) for responses generated by GPT-4, LLaMA-3.3, Gemini-1.5-Pro, and online human therapists (x-axis in each subplot). Each colored line represents one evaluator, including nine LLM-based judges and human experts (red). Higher values indicate better performance except for Toxicity and Medical Advice. See Table 16 for full numerical results*

在模型排名方面，LLM 法官与人类专家的判断存在方向性分歧：Gemini-1.5-Pro 被人类专家评为表现最差的模型，但**所有 LLM 法官均将其排在 GPT-4 之上**。这一倒挂现象进一步证实了 LLM-as-Judge 在高风险主观评估领域的不可靠性。

### 对抗性基准：暴露深层临床脆弱性

CounselBench-Adv 的对抗性测试（Table 3）成功暴露了模型在特定临床场景下的系统性缺陷。**治疗建议（Therapy）失效模式在 GPT-5 中最为严重**，被标记比例高达 0.85，而 GPT-3.5-Turbo 仅为 0.05（Δ=+0.80）。LLaMA 系列模型同样表现出较高的治疗建议失效率（Llama-3.1 为 0.55，Llama-3.3 为 0.65）。药物建议（Medication）失效模式在大多数模型中极少出现（0–0.10），但 **GPT-5 是显著异常值**（0.47），提示其安全对齐机制可能存在特定漏洞。

![[assets/figures/papers/paper_list_l29_https_openreview_net_forum_id_8MBYRZHVWT/figures/007_Table_3.jpg]]
*Table 3: Fraction of responses identified to contain each targeted failure mode by five mental health professionals. Higher values reflect greater model vulnerability to the targeted issue*

在 LLM-as-Judge 的失效检测评估中（Table 4），即使表现最好的 Claude-3.7-Sonnet 也仅达到 0.50 的 F1 分数，而 GPT-4 的 F1 最低（0.35）。准确率范围在 0.63 至 0.74 之间，但这一指标在类别不平衡的对抗性场景中具有误导性——高准确率主要源于对“无失效”样本的正确识别，而非对实际失效模式的敏感检测。

![[assets/figures/papers/paper_list_l29_https_openreview_net_forum_id_8MBYRZHVWT/figures/008_Table_4.jpg]]
*Table 4: LLM-as-Judge performance on CounselBench-Adv, relative to human expert ratings*

### 消融分析：标注者特征与模型鲁棒性

标注者层面的消融实验揭示了若干影响评估质量的因素。**花费更多时间（前 50%）的标注者撰写了显著更长的理由**（Table 8），且前 25% 的标注者标注了更多包含医疗建议的句子（Table 7）。从业经验年限对评分有显著影响：共情（p=0.02）、医疗建议（p=0.04）和事实一致性（p=0.006）的评分均与经验年限显著相关（Table 9）。“我不确定”选项的选择率极低（医疗建议 2.55%，事实一致性 3.5%，Table 15），未对整体评估造成实质影响。

![[assets/figures/papers/paper_list_l29_https_openreview_net_forum_id_8MBYRZHVWT/figures/016_Table_7.jpg]]
*Table 7: Mean metric scores by annotator time quartile (0–25%, 25–50%, 50–75%, 75–100%) for the 460 Q&A pairs rated by annotators from all quartiles. The bottom row reports p-values for differences across quartiles (Kruskal–Wallis test for ordinal metrics; chi-squared test for categorical metrics)*

![[assets/figures/papers/paper_list_l29_https_openreview_net_forum_id_8MBYRZHVWT/figures/019_Table_8.jpg]]
*Table 8: Average total rationale word count per survey by annotator time quartile (0–25%, 25–50%, 50–75%, 75–100%). Differences across quartiles are significant (by the Kruskal–Wallis test); annotators who spent more time wrote longer rationales on average*

在模型鲁棒性方面，**少样本提示对多数失效模式的改善微乎其微**（Table 17），表明这些缺陷源自预训练层面的深层局限性，而非简单的提示工程问题。领域特定模型的测试结果（Table 18）进一步印证了这一判断：Meditron-70B 在 CounselBench-Eval 上有 80% 的回答被判定为无效，MentalLLaMA 变体在对抗性测试中失败率极高（冷漠及假设型回答失败率超过 0.6）。这些结果表明，针对分类任务微调的领域模型无法直接迁移至开放式支持性对话场景，其安全对齐机制存在根本性不足。

### 补充图表

![[assets/figures/papers/paper_list_l29_https_openreview_net_forum_id_8MBYRZHVWT/figures/014_Table_6.jpg]]

![[assets/figures/papers/paper_list_l29_https_openreview_net_forum_id_8MBYRZHVWT/figures/015_Table_5.jpg]]
*Table 5: Distribution by Counseling Specialization. Annotators may have multiple specializations and thus may be counted more than once in this table*

## 定位与知识库关联

### 基准构建的范式转变

CounselBench 的核心贡献在于将心理健康 LLM 评估从封闭式、事实导向的评测范式转向开放式、临床多维度的专家评估范式。现有医学问答基准（如 MedQA、MedMCQA）主要依赖多项选择题或事实准确性指标，无法捕捉真实患者开放性问题中的安全性、共情和语境敏感性——这些恰恰是心理健康场景的核心需求。CounselBench 通过引入由临床专家定义的六维评估标准（整体质量、共情、特异性、医疗建议、事实一致性、毒性），并开展大规模专业人工标注，实现了系统性、可复现的比较。

### 评估维度的临床根基

CounselBench 的六维评估体系并非凭空设计，而是基于心理健康咨询文献中的循证实践。与仅关注事实准确性的传统医学 QA 基准相比，CounselBench 的评估维度直接对应临床咨询中的核心能力：

- **共情（Empathy）** 和 **特异性（Specificity）** 衡量回复是否展现情感调谐和个性化适配，这是治疗联盟建立的基础要素。
- **医疗建议（Medical Advice）** 和 **毒性（Toxicity）** 作为安全性指标，专门捕捉 LLM 在缺乏临床资质的场景下越界提供医疗指导或产生有害内容的倾向。
- **整体质量（Overall Quality）** 和 **事实一致性（Factual Consistency）** 则保留了传统评估中对回复质量的基本要求。

这种维度设计使得 CounselBench 能够揭示传统基准无法捕捉的失效模式：GPT-4 频繁提供无建设性反馈（49.3%），LLaMA-3.3 过度泛化或妄下判断（66.7%），Gemini-1.5-Pro 缺乏共情（44.1%）。值得注意的是，在线人类治疗师同样存在过度泛化问题（46.7%），这表明 CounselBench 的评估框架对人工回复同样具有鉴别力。

### 专家参与的规模与质量保障

CounselBench 在专家参与规模上显著超越以往工作。通过 Upwork 平台招募的 100 名持证或受过专业培训的精神卫生从业者，构成了目前心理健康 LLM 评估中最大规模的专家标注群体。这一规模使得每条回复能够获得 5 名独立专家的评估，从而支持评分者间信度的计算——Krippendorff's alpha 在五个序数维度上均达到 0.7 以上（整体评分 0.82，共情 0.83，特异性 0.82，事实一致性 0.75，毒性 0.72），表明评估具有实质性一致性。

标注协议经过三轮试点研究（共 8 名参与者）的验证和优化，最终通过 Qualtrics 平台实施结构化在线问卷。每位标注者不仅提供 Likert 量表评分，还需标注具体文本片段并提供书面理由，这为后续的失效模式分析和对抗性数据集构建提供了质性基础。

### 对抗性测试的实证驱动方法

CounselBench-Adv 的构建方式区别于文献驱动的红队测试方法。传统对抗性测试通常基于研究者对模型潜在风险的先验假设来设计测试用例，而 CounselBench-Adv 的 120 道对抗性问题完全由 10 名临床专家基于在 CounselBench-Eval 中实际观察到的精细失效模式撰写。这种“评估-发现-针对性测试”的闭环设计使得对抗性测试具有更强的实证基础，能够精确触发六类已知的模型脆弱点：冷漠/无建设性回复、过度泛化/妄下判断、缺乏共情、未经请求的治疗建议、未经请求的用药建议，以及假设性/推测性回复。

### 自动评估的局限性揭示

CounselBench 对 LLM-as-Judge 范式的系统验证揭示了自动评估在高风险主观领域的根本局限。九种高级 LLM 作为自动评估器的测试结果表明，LLM 裁判系统性高估模型回复质量，并忽视人类专家识别的安全隐患。具体表现为：所有 LLM 裁判在毒性维度上一致给出最低评分，而人类专家则识别出显著的毒性差异；LLM 裁判在事实一致性上频繁给出满分或接近满分的评分；在模型排序上，LLM 裁判一致将 Gemini-1.5-Pro 排在 GPT-4 之上，与人类专家的偏好完全相反。

在 CounselBench-Adv 的失效模式检测任务中，表现最佳的 LLM 裁判（Claude-3.7-Sonnet）也仅达到 0.50 的 F1 分数，而 GPT-4 的 F1 仅为 0.35。这表明当前 LLM 尚无法可靠地替代人类专家进行心理健康回复的安全性和质量评估。

### 适用边界与局限

CounselBench 的适用边界受限于以下因素：

1. **单轮交互限制**：评估仅针对单轮问答，未涵盖多轮对话中的连贯性、一致性或动态变化。实际心理健康咨询通常涉及持续的治疗关系和多轮互动，CounselBench 无法评估模型在这些场景下的表现。

2. **语言与文化局限**：所有评估基于英文、主要来自美国社区的 CounselChat 论坛，结论可能不适用于其他语言或文化群体。标注者的人口学构成（白人及女性占比较高）虽与美国咨询行业全国统计特征一致，但仍可能存在未观测到的背景偏差。

3. **失效模式覆盖不全**：对抗性数据集仅覆盖从 CounselBench-Eval 中提炼出的六种失效模式，可能遗漏其他临床相关的风险类型，如危机干预不当、边界侵犯等。

4. **领域特定模型的低效性**：测试表明，领域特定模型（如 MentalLLaMA 和 Meditron-70B）在开放式心理健康问答中表现出较高的无效率和失败率——Meditron-70B 在 CounselBench-Eval 上有 80% 的回复无效，MentalLLaMA 变体在对抗性测试中失败率极高。这提示当前针对分类任务微调的领域模型尚无法泛化到生成性支持对话。

### 开放问题

CounselBench 揭示的关键开放问题包括：

- **LLM 能否在高风险主观领域作为可靠评估者？** 当前证据表明 LLM 裁判系统性高估回复并忽视安全隐患，但未来模型的能力提升是否可能弥合这一差距仍需探索。

- **如何将评估扩展到多轮对话？** 多轮对话中的连贯性、一致性测量以及交互动态的保持是重要的技术挑战。如何在多轮场景中针对特定失效模式进行测试同样需要新的方法设计。

- **领域特定模型的生成能力瓶颈**：为何针对分类任务微调的领域模型无法生成有效的支持性对话回复？这一问题的解答可能涉及预训练数据、微调策略和评估范式之间的深层不匹配。

- **安全对齐的迁移**：来自新一代模型家族的安全对齐技术如何整合到心理健康 LLM 中以降低失效模式的发生率？少样本条件下的实验表明，模型对多数失效模式的改善微乎其微，提示这些缺陷可能源自预训练层面的深层局限性，而非简单的提示工程可解决。

## 原文 PDF

![[paperPDFs/ICLR_2026/CounselBench_A_Large_Scale_Expert_Evaluation_and_Adversarial_Benchmarking_of_Large_Language_Models_in_Mental_Health_Question_Answering.pdf]]
