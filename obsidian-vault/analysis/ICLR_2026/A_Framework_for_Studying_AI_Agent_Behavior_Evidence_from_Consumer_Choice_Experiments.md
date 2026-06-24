---
title: "A Framework for Studying AI Agent Behavior: Evidence from Consumer Choice Experiments"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/A_Framework_for_Studying_AI_Agent_Behavior_Evidence_from_Consumer_Choice_Experiments.pdf
aliases:
- FSAABEFCCE
- ABXLAB
tags:
- ICLR_2026
- topic/safety_alignment_fairness_privacy
- topic/safety_alignment_fairness_privacy/accountability_transparency_and_interpretability
core_operator: "通过ABXLAB框架中的干预引擎（man-in-the-middle），在智能体观察网页内容之前实时修改选项属性（价格、评分）和注入心理暗示（权威、社会证明、稀缺性、负面框架、激励），从而系统性地探测这些因素对智能体决策的因果影响。"
primary_logic: "LLM智能体即使不受人类认知约束（如有限理性、启发式偏差），仍然表现出比人类更强、更系统的选择偏差。智能体对价格、评分、呈现顺序和暗示的敏感度是人类3-10倍以上，且用户偏好描述（user profiles）的作用更像是一种“阈值开关”，而非精细调节，会彻底重构智能体的决策规则。这表明智能体行为偏差并非源于认知限制，而是源于其内在的决策机制。"
claims:
- "智能体对评分、价格和暗示的敏感度远超人类，效应量是人类3-10倍以上"
- "o4 Mini对高评分产品的偏好达到81.2pp"
- "Llama 4 Maverick在匹配评分条件下对更便宜选项的偏好达到93.2pp"
- "GPT-4.1 Nano在原始条件下对第一个展示产品的偏好达到88.8pp"
---

# A Framework for Studying AI Agent Behavior: Evidence from Consumer Choice Experiments

> [!tip] 核心洞察
> LLM智能体即使不受人类认知约束（如有限理性、启发式偏差），仍然表现出比人类更强、更系统的选择偏差。智能体对价格、评分、呈现顺序和暗示的敏感度是人类3-10倍以上，且用户偏好描述（user profiles）的作用更像是一种“阈值开关”，而非精细调节，会彻底重构智能体的决策规则。这表明智能体行为偏差并非源于认知限制，而是源于其内在的决策机制。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 研究AI智能体行为的框架：来自消费者选择实验的证据 |
| 英文题名 | A Framework for Studying AI Agent Behavior: Evidence from Consumer Choice Experiments |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=xAPoscV2Bw) |
| Topic | #topic/safety_alignment_fairness_privacy #topic/safety_alignment_fairness_privacy/accountability_transparency_and_interpretability |
| Method | ABXLAB |
| Dataset | ABXLAB / OneStopMarket |

> [!tip] 效果简介
> - ABXLAB / OneStopMarket 上，产品选择概率的边际变化（pp） 为 智能体平均效应量（如Claude Sonnet 4对暗示的敏感度+55.9pp），对比 人类基线效应量（如对暗示的敏感度9.9pp），变化 智能体敏感度是人类3-10倍以上。
> - ABXLAB / OneStopMarket 上，高评分产品偏好（原始条件） 为 o4 Mini: 81.2pp，对比 人类: 5.0pp，变化 +76.2pp。
> - ABXLAB / OneStopMarket 上，更便宜产品偏好（匹配评分条件） 为 Llama 4 Maverick: 93.2pp，对比 人类: 9.4pp，变化 +83.8pp。

## 概述

该论文提出了 **ABXLAB**（Agent Behavior eXperiments）框架，旨在系统性地研究LLM智能体在真实消费者选择环境中的行为鲁棒性。核心瓶颈在于：当前评估主要关注任务完成能力，而忽略了智能体在面对价格、评分、呈现顺序和心理暗示等选择架构因素时表现出的系统性偏差——其敏感度远超人类，构成了可靠部署的关键障碍。

**核心结论**：LLM智能体即使不受人类认知约束（如有限理性），仍然表现出比人类更强、更系统的选择偏差。智能体对价格、评分、呈现顺序和暗示的敏感度是人类 **3-10倍以上**（例如，o4 Mini对高评分产品的偏好达81.2pp，Llama 4 Maverick在匹配评分条件下对更便宜选项的偏好达93.2pp，GPT-4.1 Nano对第一个展示产品的偏好达88.8pp，而人类基线分别为5.0pp、9.4pp和4.0pp）。用户偏好描述的作用更像是一种“阈值开关”，而非精细调节，会彻底重构智能体的决策规则。

**方法定位**：ABXLAB采用“中间人”（man-in-the-middle）干预引擎，在智能体观察网页内容之前实时修改选项属性（价格、评分）和注入心理暗示（权威、社会证明、稀缺性、负面框架、激励），从而系统性地探测这些因素的因果效应。框架基于WebArena的状态空间、动作空间和观察空间定义，并通过Agent-Lab实现。实验在OneStopMarket在线购物环境中进行，共执行 **80,000+次实验**，覆盖17个来自OpenAI、Anthropic、Google、Meta、DeepSeek的模型（包括开放、封闭和推理模型）。

**主要结果**：通过线性概率模型（LPM）和多项Logit模型（MNL）估计各因素的边际效应（两种模型结果高度相关，r≈0.93），发现所有智能体的平均属性敏感度（约13%-31%）均显著高于人类基线（约7%）。暗示效应在匹配评分和价格后仍然显著，表明其影响独立于价格和评分差异。BOGO（买一送一）激励对消耗品的效应强于耐用品，但耐用品类别也表现出显著敏感性。三选一实验中评分效应极高，削弱了其他属性的边际效应。

## 背景与动机

当前对LLM智能体的评估主要集中在任务完成能力上，例如能否点击正确的按钮或填写表单，这反映了一种以功能正确性为核心的工程视角。然而，当智能体被部署到真实的消费者决策环境中时，它们会面临价格、评分、呈现顺序以及各种心理暗示（如权威、稀缺性）等选择架构因素。这些因素在人类行为经济学中已被充分研究，但在智能体行为评估中却几乎被完全忽略。这种评估缺口构成了信任和可靠部署的核心瓶颈：一个能够完美完成任务的智能体，可能同时是一个系统性偏差的决策者，其偏差幅度远超人类。

本文的核心动机在于填补这一缺口。作者提出的核心假设是：**LLM智能体在决策时表现出系统性的、大幅度的选择偏差，且这些偏差并非源于人类认知约束（如有限理性或启发式偏差），而是源于其内在的决策机制。** 为了验证这一假设，作者构建了ABXLAB（Agent Behavior eXperiments）框架，该框架的核心创新在于一个“中间人”（man-in-the-middle）干预引擎（Figure 1），它能够在智能体观察网页内容之前实时拦截并修改网页内容，从而系统性地操纵选择架构中的关键属性。

具体而言，ABXLAB通过干预引擎实现了对四个关键因果旋钮的精确操控：**产品价格**（通过事后匹配消除价格差异）、**产品评分**（通过重新选择产品对进行评分匹配）、**产品页面内容**（注入权威、社会证明、稀缺性、负面框架、激励等五种心理暗示文本，Table 1），以及**用户偏好描述**（通过自然语言构建用户画像，指定对评分、价格、暗示的敏感度方向）。这种设计使得作者能够从因果层面分离出每个因素对智能体决策的独立效应，而这在以相关性分析为主的现有评估中是无法实现的。

该研究在方法上的关键缺口在于：现有评估框架（如WebArena）虽然提供了丰富的任务环境，但缺乏对选择架构因素的系统性操控能力。ABXLAB基于WebArena的状态空间、动作空间和观察空间定义，但增加了干预函数集I，使得环境形式化为 $\mathcal{E} = \langle S, A, \mathcal{O}, \mathcal{T}, \mathcal{I} \rangle$，从而将行为科学实验范式引入智能体评估。

## 核心创新

ABXLAB的核心创新在于将行为科学中“选择架构”（choice architecture）的因果识别范式系统性地引入LLM智能体评估，揭示了当前评估体系忽略的关键瓶颈：智能体在价格、评分、呈现顺序和心理暗示等选择架构因素面前表现出系统性、大幅度的偏差，其敏感度远超人类（效应量是人类3-10倍以上）。这一发现挑战了“智能体不受人类认知约束因而更理性”的直觉。

**核心瓶颈与因果旋钮：** 当前LLM智能体评估（如WebArena）主要关注任务完成能力（如点击正确按钮），而忽略了智能体在面对真实决策环境时的行为鲁棒性和可靠性。ABXLAB通过**干预引擎（man-in-the-middle）**，在智能体观察网页内容之前实时修改选项属性（价格、评分）和注入心理暗示（权威、社会证明、稀缺性、负面框架、激励），从而系统性地探测这些因素对智能体决策的因果影响。环境被形式化为 $\mathcal{E} = \langle S, A, \mathcal{O}, \mathcal{T}, \mathcal{I} \rangle$，其中 $\mathcal{I}$ 是干预函数集，这是与基线环境（如WebArena的 $\langle S, A, \mathcal{O}, \mathcal{T} \rangle$）的关键区别。

**核心洞察：** LLM智能体即使不受人类认知约束（如有限理性、启发式偏差），仍然表现出比人类更强、更系统的选择偏差。例如，o4 Mini对高评分产品的偏好达到81.2pp（人类仅5.0pp），Llama 4 Maverick在匹配评分条件下对更便宜选项的偏好达到93.2pp（人类9.4pp），GPT-4.1 Nano对第一个展示产品的偏好达到88.8pp（人类4.0pp）。这表明智能体行为偏差并非源于认知限制，而是源于其内在的决策机制。

**关键changed slots：** 与基线环境相比，ABXLAB改变了以下维度：
- **产品价格**：通过干预函数进行事后匹配（MRaP条件），消除价格差异的影响，从而分离出其他因素的独立效应。
- **产品评分**：通过重新选择产品对进行评分匹配（MR条件），消除评分差异的影响。
- **产品页面内容（暗示注入）**：在观察状态中注入权威、社会证明、稀缺性、负面框架、激励等暗示文本（Table 1列出了所有干预类别和模板）。
- **用户偏好描述**：通过自然语言描述构建用户画像，指定对评分、价格、暗示的敏感度方向。实验发现用户偏好描述的作用更像**阈值开关**而非精细调节——当偏好明确时，会主导决策，抑制其他因素的影响（Figure 5）。

**实验规模与稳健性：** 论文进行了超过80,000次实验，消耗约25亿token和40万次API请求，覆盖17个来自不同提供商（OpenAI、Anthropic、Google、Meta、DeepSeek）的模型。统计分析采用线性概率模型（LPM）和多项Logit模型（MNL），两者边际效应高度相关（r ≈ 0.93），验证了结果的稳健性。消融实验表明，匹配评分（MR）和匹配评分与价格（MRaP）后，暗示效应仍然显著，说明暗示的影响独立于价格和评分差异。

## 整体框架

![[assets/figures/papers/iclr26_0002_xAPoscV2Bw_A_Framework_for_Studying_AI_Agent_Behavior_Evide/figures/001_Figure_1.jpg]]
*Figure 1: Our man-in-the-middle framework (right) consists of an intervention engine which constructs and implements one of several different forms of intervention to one (or none) of the products. Our benchmark (left and middle) consists of (a) a constrained search and selection process for finding plausible product choice pairs (e.g., selecting from the same category, with similar prices and ratings or with perfectly matched ratings), and (b) a binary forced choice paradigm where LLM agents choose which product is better and add it to the cart. See Appendix I for real example pairs, and Appendix B for details on interventions. The empirical analysis procedure (not pictured) allows us to make robust...*

ABXLAB框架的核心设计围绕一个**中间人干预引擎**（man-in-the-middle intervention engine）展开，其形式化定义为 $\mathcal{E} = \langle S, A, \mathcal{O}, \mathcal{T}, \mathcal{I} \rangle$，其中 $\mathcal{I}$ 是干预函数集，每个函数 $I: \mathcal{O} \to \mathcal{O}$ 在智能体观察网页之前实时拦截并修改其内容。这一设计的关键优势在于：无需构建自定义实验环境，即可在真实网页内容上系统性地操纵选择架构因素（价格、评分、暗示、顺序等），从而隔离出各因素对智能体决策的因果效应。

框架的pipeline由五个模块串联构成：

1. **产品对构建模块**：从原始产品目录中按类别分组，应用有效性约束——评分绝对差 $\leq \Delta_r$，价格相对差 $\leq \Delta_p$——生成可比较的产品对。该模块还使用轻量级LLM标题过滤器，移除包含暗示性短语（如"top-rated"）或反映多件装、捆绑销售的产品，以减少标题中的非受控经济激励。

2. **实验生成器**：基于干预类型（n=10）、产品对（n=50）和条件（n=3：无匹配Original、匹配评分MR、匹配评分与价格MRaP）的所有组合，生成1,500个基础配置。

3. **干预引擎**：核心的中间人模块，读取配置文件（YAML）中定义的干预函数，在智能体获取网页之前应用所有变换。干预类型包括：价格操纵、评分匹配、呈现顺序重排，以及五类心理暗示注入（权威、社会证明、稀缺性、负面框架、激励）。

4. **智能体执行器**：驱动LLM智能体在修改后的网页环境中执行二选一强制选择任务（binary forced choice paradigm），记录动作历史、观察历史和推理过程。所有模型使用温度0.1（OpenAI推理模型使用1）。

5. **统计分析模块**：使用线性概率模型（LPM）估计各因素的边际效应，包含试验固定效应 $\alpha_t$ 和模型身份、更便宜、被暗示、更高评分、呈现位置的主效应及N阶交互项。采用双聚类稳健标准误（按暗示文本和产品类别聚类）和Benjamini-Hochberg多重检验校正。LPM与多项Logit模型（MNL）的边际效应高度相关（r ≈ 0.93），验证了线性近似的可靠性。

输入输出流方面：智能体接收任务意图（如"选择更好的产品并加入购物车"），观察经干预引擎变换后的网页内容，执行动作（点击、滚动等），直至做出最终选择。整个流程在OneStopMarket在线购物环境中运行，累计超过80,000次实验，覆盖约25亿token和40万次API请求。

## 核心模块与公式推导

### 1. 环境形式化定义

ABXLAB框架将智能体环境形式化为一个六元组：

$$\mathcal{E} = \langle S, A, \mathcal{O}, \mathcal{T}, \mathcal{I} \rangle$$

其中：
- **S**：状态空间，描述环境的完整状态（包括网页内容、购物车状态等）。
- **A**：动作空间，智能体可执行的动作集合（如点击、添加购物车、导航）。
- **O**：观察空间，智能体实际观测到的内容（修剪后的HTML文本）。
- **T**：转移函数 $S \times A \to S$，定义动作如何改变状态。
- **I**：干预函数集 $I = \{I: \mathcal{O} \to \mathcal{O}\}$，在观察传递给智能体之前实时修改网页内容。这是ABXLAB的核心创新——man-in-the-middle干预引擎。

该形式化的关键瓶颈在于：干预函数在智能体观察之前执行，使得实验者可以系统性地操纵选择架构因素（价格、评分、暗示文本、呈现顺序），而无需构建定制的实验环境。

### 2. 产品对有效性约束

为了确保产品对在可比较的范围内变化，ABXLAB定义了严格的有效性约束：

$$|\operatorname{rating}(p_1) - \operatorname{rating}(p_2)| \leq \Delta_r \quad \mathrm{and} \quad \frac{|\operatorname{price}(p_1) - \operatorname{price}(p_2)|}{\min\{\operatorname{price}(p_1), \operatorname{price}(p_2)\}} \leq \Delta_p$$

其中：
- $\Delta_r$：评分绝对差阈值，用于控制评分差异范围。
- $\Delta_p$：价格相对差阈值，控制价格差异的相对比例。
- $\min\{\operatorname{price}(p_1), \operatorname{price}(p_2)\}$：分母取两个价格中的较小值，使相对差计算对低价产品更敏感。

该约束的因果意义在于：它确保了后续实验中的匹配条件（MR：匹配评分，MRaP：匹配评分与价格）能够有效消除自然属性差异的干扰，从而隔离出暗示、呈现顺序等单一因素的因果效应。

### 3. 主要统计模型（M1）

ABXLAB使用线性概率模型（LPM）估计各因素的边际效应：

$$Y_{tp} = \beta^{\top} X_{tp} + \alpha_t + \varepsilon_{tp}, \quad X_{tp} = (m_{tp} + c_{tp} + n_{tp} + r_{tp} + p_{tp})^{[N]}$$

其中：
- **$Y_{tp}$**：二元因变量，表示在试验t中，产品对中的特定产品是否被选择（0/1）。
- **$\alpha_t$**：试验固定效应，控制每次试验间的不可观测异质性。
- **$m_{tp}$**：模型身份指示变量（如GPT-4.1 Nano、Claude Sonnet 4等）。
- **$c_{tp}$**：更便宜（Cheaper）指示变量，标记价格更低的选项。
- **$n_{tp}$**：被暗示（Nudged）指示变量，标记被注入暗示文本的选项。
- **$r_{tp}$**：更高评分（Higher Rated）指示变量，标记评分更高的选项。
- **$p_{tp}$**：呈现位置（Position）指示变量，标记第一个展示的选项。
- **$[N]$**：上标表示包含主效应和最高N阶交互项，用于捕捉各因素之间的调节关系。

**估计方法**：使用`fixest`包进行估计，采用聚类稳健标准误（two-way cluster-robust standard errors），聚类维度为暗示文本和产品类别。显著性采用Benjamini-Hochberg方法进行多重检验校正。

### 4. 暗示特定模型（M2）

为估计不同暗示文本的异质性效应，ABXLAB引入了暗示特定模型：

$$Y_{tp} = \beta^{\top} X_{tp} + \alpha_t + \varepsilon_{tp}, \quad X_{tp} = \left( m_{tp} + c_{tp} + n_{tp} + r_{tp} + p_{tp} + \theta_{j(t)} \right)^{[N]}$$

与M1的关键区别在于：
- **$\theta_{j(t)}$**：暗示文本变量，直接作为回归变量（而非固定效应），用于估计文本层面的异质性。
- 该模型仅在暗示试验中使用，允许分析不同暗示文本（如权威暗示、社会证明、稀缺性、负面框架、激励）对选择概率的差异化影响。

### 5. 鲁棒性验证：多项Logit模型（MNL）

为验证LPM的可靠性，ABXLAB同时估计了基于随机效用理论的多项Logit模型。由于因变量是二元的，MNL退化为标准二元Logit模型。结果显示，LPM和MNL的边际效应高度相关（$r \approx 0.93$），表明线性概率模型提供了可靠的近似。

### 6. 关键公式的因果机制

上述公式链的设计体现了ABXLAB的核心因果推理逻辑：

1. **环境形式化**定义了干预引擎的接入点（观察空间O上的干预函数I），使得实验者可以在智能体决策链的输入阶段进行操纵。
2. **产品对约束**确保了自然属性差异在可控范围内，为后续的匹配实验（MR、MRaP）提供了基础。
3. **LPM/MNL模型**通过固定效应和交互项，将各因素的边际效应从混杂因素中分离出来。交互项的存在使得模型能够捕捉到如“用户偏好描述如何调节价格敏感度”这类高阶因果模式。

**证据强度说明**：上述所有公式均直接引用自论文Section 3.1、Section 3.3、Appendix E.2、E.3和F，置信度为1.0。公式中的变量含义已在论文中明确给出，无需额外推导。

## 实验与分析

### 3.1 核心结果：智能体对选择架构的敏感度远超人类

ABXLAB框架在OneStopMarket购物环境中，通过干预引擎在智能体观察网页前实时修改产品属性（价格、评分、呈现顺序）并注入心理暗示（权威、社会证明、稀缺性、负面框架、激励），系统性地探测了17个LLM模型（覆盖OpenAI、Anthropic、Google、Meta、DeepSeek的开放、封闭和推理模型）在二选一强制选择任务中的决策偏差。总计进行了超过80,000次实验，消耗约25亿token和40万次API请求。

**Table 2** 呈现了核心发现：所有智能体对价格、评分、呈现顺序和暗示的敏感度均远超人类基线（30名Prolific参与者）。人类的平均属性敏感度约为7%（未加权），而最低的模型（Claude 3.5 Haiku）约为13%，最高的模型（Claude Sonnet 4）达到约31%。具体而言：

![[assets/figures/papers/iclr26_0002_xAPoscV2Bw_A_Framework_for_Studying_AI_Agent_Behavior_Evide/figures/003_Table_2.jpg]]
*Table 2: Estimated marginal change (pp) in product choice probability under each condition. Contrasts from linear probability models (cluster-robust SEs; full specs in Appendix E). Viewed 1st = viewed first; Cheaper = lower price; Higher Rated = higher rating (only available when ratings aren’t matched); Nudged = nudged. Orig. = no matching; MR = matched ratings; MRaP = matched ratings & prices. Red = significant increase, Blue = significant decrease. ∗ p \< .05, ** p \< .01, * ** p \< .001, **** p \< .0001 (Benjamini–Hochberg corrected)*

- **评分效应**：人类对高评分产品的偏好仅为5.0个百分点（pp），而o4 Mini的偏好达到81.2pp，是人类的16倍以上。
- **价格效应**：在匹配评分（MR）条件下，人类对更便宜选项的偏好为9.4pp，而Llama 4 Maverick达到93.2pp，接近确定性选择。
- **呈现顺序效应**：人类对第一个展示产品的偏好仅为4.0pp，而GPT-4.1 Nano达到88.8pp，表现出近乎确定性的顺序偏差。
- **暗示效应**：在匹配评分和价格（MRaP）条件下，人类对暗示的敏感度为9.9pp，而Claude Sonnet 4达到55.9pp。

这些效应量差异（3-10倍以上）构成了论文的核心经验证据：**LLM智能体即使不受人类认知约束（如有限理性、启发式偏差），仍然表现出比人类更强、更系统的选择偏差**。这表明智能体行为偏差并非源于认知限制，而是源于其内在的决策机制。

### 3.2 消融实验：匹配条件与偏好描述的阈值效应

**属性匹配消融**：通过评分匹配（MR）和评分与价格同时匹配（MRaP）条件，论文分离了各因素的独立影响。**Table 2** 显示，在MR和MRaP条件下，暗示效应仍然显著（如Claude Sonnet 4在MRaP下为55.9pp），表明暗示的影响独立于价格和评分差异。这一消融结果排除了“暗示效应仅由价格或评分差异驱动”的替代解释。

**用户偏好描述的阈值开关效应**：**Figure 5** 展示了用户偏好描述（user profiles）对选择概率的影响。当偏好明确指定时（如“减少对暗示的敏感度”），智能体的决策规则被彻底重构：暗示效应几乎被消除（甚至反转），而价格和评分差异仍保持高影响力。论文将此描述为“阈值开关”（threshold shifts）而非精细调节——偏好描述不是微调智能体的权衡权重，而是从根本上改变了决策规则，使偏好维度主导选择。这一发现揭示了当前LLM智能体在理解用户意图时的二元特性。

**模型鲁棒性验证**：**Figure 15** 显示线性概率模型（LPM）与多项Logit模型（MNL）的边际效应高度相关（r ≈ 0.93），表明LPM的线性近似是可靠的。同时，**Figure 14** 展示了智能体推理链中提及的属性统计，验证了智能体确实在决策过程中考虑了这些因素。

### 3.3 异质性分析：暗示文本、产品类别与模型差异

**暗示文本异质性**：**Figure 2** 展示了按暗示文本分解的平均暗示效应。同一理论类别内的不同暗示文本表现出显著的效应差异。例如，权威暗示（“专家推荐”）与社会证明暗示（“最受欢迎”）的效果可能相差数倍。**Figures 7-9** 进一步展示了每个模型在不同匹配条件下的暗示文本异质性，表明模型对特定措辞的敏感度差异巨大。

**产品类别异质性**：**Figure 10** 按产品类别分解了暗示效应，发现某些类别（如电子设备）对暗示更敏感，而其他类别（如日用消费品）则相对不敏感。**Table 3** 进一步展示了BOGO（买一送一）激励的效应：对消耗品（如饼干，60.88%）的效应强于耐用品（如手机，40.61%），但耐用品类别也表现出显著敏感性。

![[assets/figures/papers/iclr26_0002_xAPoscV2Bw_A_Framework_for_Studying_AI_Agent_Behavior_Evide/figures/019_Table_3.jpg]]
*Table 3: Estimated Marginal Means for BOGO effect by category and type of product*

**模型间差异**：不同模型表现出截然不同的偏差模式。例如，GPT-4.1 Nano在呈现顺序上表现出近确定性偏差（+88.8pp），而其他模型可能表现出相反的模式。o4 Mini对评分极度敏感（+81.2pp），而Llama 4 Maverick对价格极度敏感（MR下+93.2pp）。这种异质性暗示了不同训练策略和架构对决策偏差的系统性影响。

### 3.4 失败模式与开放问题

**三选一实验的局限性**：**Table 5** 显示，在三选一（trio）实验中，评分效应极高，削弱了其他属性（如暗示）的边际效应。这可能是因为评分在三选一场景中提供了更强的区分信号。但论文指出该实验规模较小（20个产品三元组，每个模型800次试验），统计功效有限。

![[assets/figures/papers/iclr26_0002_xAPoscV2Bw_A_Framework_for_Studying_AI_Agent_Behavior_Evide/figures/021_Table_5.jpg]]
*Table 5: Trio estimated marginal means as percentage point changes*

**BOGO激励的经济合理性**：论文承认BOGO激励在耐用品类别中的经济合理性存疑（如“买一送一”的手机），但实验设计有意未对此进行约束，以测试智能体是否能够识别这种不合理性。结果表明智能体未能识别，反而表现出显著敏感度。

**未解决的开放问题**：
- 为什么某些模型（如GPT-4.1 Nano）表现出近乎确定性的顺序效应，而其他模型则相反？
- 同一理论类别内不同暗示文本之间的效应异质性如何解释？
- 用户偏好描述为何表现为阈值开关而非精细调节？这是否反映了LLM内部表征的某种固有特性？
- 这些发现如何向消费者行为以外的其他领域（如医疗、金融、法律）泛化？

### 补充图表

![[assets/figures/papers/iclr26_0002_xAPoscV2Bw_A_Framework_for_Studying_AI_Agent_Behavior_Evide/figures/002_Table_1.jpg]]
*Table 1: Nudge categories and interventions. The variables ${expertise} and ${category} are replaced by product category with specific examples using a lightweight LLM*

![[assets/figures/papers/iclr26_0002_xAPoscV2Bw_A_Framework_for_Studying_AI_Agent_Behavior_Evide/figures/020_Table_4.jpg]]
*Table 4: Average BOGO effects by product type under matching*

## 方法谱系与知识库定位

ABXLAB 的定位并非从零构建新的智能体基准（benchmark），而是在现有环境框架之上叠加一层因果干预层。其基础环境继承自 **WebArena** 的状态空间、动作空间和观察空间定义，实现层面依托 **Agent-Lab** 框架，评估场景则使用 **OneStopMarket** 在线购物环境。这一设计选择使得 ABXLAB 能够复用成熟的智能体交互基础设施，将创新集中在“如何系统性地操纵选择架构”这一核心问题上，而非重复造轮子。

**与 baseline 的关键差异**在于 ABXLAB 引入的“中间人（man-in-the-middle）”干预引擎。传统智能体评估（如 WebArena 原生任务）关注的是智能体能否完成目标（如点击正确按钮、填写表单），其自变量是任务难度或环境复杂度。ABXLAB 则将自变量切换为**选择架构因素**：在智能体观察到网页内容之前，实时拦截并修改产品价格、评分、呈现顺序，以及注入权威、社会证明、稀缺性、负面框架、激励等心理暗示文本。这种设计使得 ABXLAB 能够回答“智能体对某个因素的敏感度有多高”这一因果问题，而非“智能体能否完成任务”这一能力问题。

**适用边界**由三个约束条件共同界定。第一，场景边界：当前所有实验基于 OneStopMarket 在线购物环境，结果向医疗、金融、法律等领域的泛化性尚未验证。第二，感知边界：智能体仅接收修剪后的 HTML 文本观察，无视觉输入，这低估了视觉元素（如产品图片、布局颜色）对决策的影响。第三，选择边界：产品对构建过程中使用了轻量级 LLM 标题过滤器，移除了包含暗示性短语或反映多件装、捆绑销售的产品——此过滤可能引入选择偏差，且原论文未对此进行敏感性分析。

**局限**集中在五个方面。其一，实验设计有意未对 BOGO（买一送一）激励在耐用品类别中的经济合理性进行约束，这可能导致部分实验条件在现实中不存在对应物。其二，三选一实验（trio）规模较小（20 个产品三元组，每个模型 800 次试验），统计功效有限，且该条件下评分效应极高，削弱了其他属性（如暗示）的边际效应，使得该实验的结论需谨慎解读。其三，人类基线实验仅 30 名参与者，未报告人口统计信息，其代表性存疑。其四，线性概率模型（LPM）与多项 Logit 模型（MNL）的边际效应高度相关（r ≈ 0.93），但 LPM 的线性假设在极端概率区域可能产生有偏估计。其五，所有模型均使用温度 0.1（OpenAI 推理模型为 1），这一低温度设置可能系统性地放大了确定性偏差，高温度下的行为模式未知。

**开放问题**构成了该领域下一步研究的核心议程。首先，为什么某些模型（如 GPT-4.1 Nano）表现出近乎确定性的顺序效应（88.8pp 偏好第一个展示产品），而其他模型则表现出相反或更弱的模式？这暗示智能体内部决策机制存在根本性差异，而非简单的“能力高低”问题。其次，同一理论类别内不同暗示文本之间的效应异质性如何解释？例如，权威暗示中的“专家推荐”与“医生推荐”可能产生截然不同的效果，但原论文未对此进行机制层面的分析。第三，用户偏好描述为何表现为“阈值开关”而非精细调节——这是否反映了 LLM 内部表征的某种固有特性（如注意力机制的离散化倾向），还是实验设计（偏好描述为自然语言指令）的产物？最后，如何使智能体对呈现顺序更鲁棒、对简单说服性线索更不敏感，是一个尚未解决的工程与科学交叉问题。

## 原文 PDF

PDF 文件：paperPDFs/ICLR_2026/A_Framework_for_Studying_AI_Agent_Behavior_Evidence_from_Consumer_Choice_Experiments.pdf

![[paperPDFs/ICLR_2026/A_Framework_for_Studying_AI_Agent_Behavior_Evidence_from_Consumer_Choice_Experiments.pdf]]
