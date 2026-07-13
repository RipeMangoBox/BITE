---
title: "LLM Fingerprinting via Semantically Conditioned Watermarks"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/LLM_Fingerprinting_via_Semantically_Conditioned_Watermarks.pdf
project_link: null
code_link: null
openreview_forum_id: t38nZqqi3Z
aliases:
- SCWF
- LFSCW
tags:
- ICLR_2026
- topic/safety_alignment_fairness_privacy
- topic/safety_alignment_fairness_privacy/trustworthy_machine_learning
core_operator: "用完整的语义域（如法语）替代有限的查询集，用基于红绿水印的统计信号（在整个响应中扩散、强度随令牌数增加）替代脆弱的固定密钥，通过语义条件水印蒸馏将信号绑定到该域中。"
primary_logic: "通过在目标语义域上蒸馏水印信号并利用正则化保留其他域行为，可以构建一个既隐蔽（在域外无泄漏）又鲁棒（信号累积检测可对抗部署修改）的模型指纹，且不影响通用任务表现。"
claims:
- "该指纹在所有25种部署场景（采样变化、系统提示、量化、剪枝、微调）和5种针对性对抗（输入/输出改写、预填充等）下均达到FSR 1.0，基线方法则频繁失败。"
- "指纹检测在模型被指纹化时系统上检出，未指纹化模型检出率为0，且基准准确率未显著下降（平均ACC保持或仅有少量波动）。"
- "隐蔽性评估表明，本文方法的查询和回复被GPT5-MINI法官召回率显著低于IF和SF，对手难以察觉指纹。"
- "Fingerprint Success Rate (FSR) 上 FSR = 1.0"
---

# LLM Fingerprinting via Semantically Conditioned Watermarks

> [!tip] 核心洞察
> 通过在目标语义域上蒸馏水印信号并利用正则化保留其他域行为，可以构建一个既隐蔽（在域外无泄漏）又鲁棒（信号累积检测可对抗部署修改）的模型指纹，且不影响通用任务表现。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 基于语义条件水印的LLM指纹识别 |
| 英文题名 | LLM Fingerprinting via Semantically Conditioned Watermarks |
| 会议/期刊 | ICLR 2026 (Oral) |
| Links | [paper](https://openreview.net/forum?id=t38nZqqi3Z) |
| Topic | #topic/safety_alignment_fairness_privacy #topic/safety_alignment_fairness_privacy/trustworthy_machine_learning |
| Method | Semantically Conditioned Watermark Fingerprinting |
| Dataset | Fingerprint Success Rate (FSR), Average Benchmark Accuracy (8 benchmarks) |

> [!tip] 效果简介
> - Fingerprint Success Rate (FSR) 上，FSR 为 1.0，对比 IF/SF: 0.0 在多数部署下，变化 +1.0。
> - Average Benchmark Accuracy (8 benchmarks) 上，AVG 为 LLaMA3.2-1B: 0.42, Qwen2.5-3B: 0.58, LLaMA3.1-8B: 0.63，对比 与Base模型几乎相同（变化 ≤ 0.01），变化 ~0.0。

## 概要

大型语言模型（LLM）的部署通常伴随严格的许可证限制，但恶意部署者可通过微调、量化、剪枝等手段修改模型后以黑盒API形式提供服务，使模型所有者难以证明所有权。现有黑盒模型指纹方法依赖固定的“查询-密钥”对：模型所有者嵌入一组非典型查询及其对应的非典型回复作为指纹，检测时通过精确字符串匹配来验证身份。这一范式存在两个根本瓶颈：**（1）脆弱性**——固定的查询-密钥对在模型经历微调、量化、剪枝等常见部署修改后极易失效；**（2）隐蔽性不足**——非典型的查询/回复模式容易被恶意部署者检测并过滤，导致指纹被移除。

本文提出一种全新的模型指纹范式——**基于语义条件水印的指纹识别**（Semantically Conditioned Watermark Fingerprinting），其核心因果调控在于：用完整的语义域（如法语）替代有限的查询集作为触发条件，用扩散在响应中的统计水印信号（红绿水印，信号强度随文本长度累积）替代脆弱的固定密钥作为识别依据。具体而言，模型所有者通过蒸馏损失在目标语义域上嵌入水印行为，同时通过正则化损失保持域外生成分布不变，从而构建一个**隐蔽**（仅在域内触发，域外无泄漏）且**鲁棒**（统计信号可累积检测以对抗部署修改）的模型指纹。

实验结果表明，该方法在所有25种通用部署场景（包括采样变化、系统提示、量化、剪枝、微调等）和5种针对性对抗攻击（输入/输出改写、预填充等）下均达到**指纹成功率（FSR）1.0**，而基线方法**IF**（Xu et al., 2024a）和**SF**（Nasery et al., 2025）在多数场景下FSR降至0.0。同时，指纹嵌入对模型通用能力的影响极小，八个基准上的平均准确率与基础模型几乎一致（变化 ≤ 0.01），且未指纹化模型的误检率为0。隐蔽性评估显示，本文方法的查询和回复被GPT5-MINI法官的召回率显著低于基线，对手难以察觉指纹存在。



### 问题背景：模型发布后的所有权困境

大型语言模型（LLM）的发布者面临一个日益严峻的现实问题：模型一旦发布，恶意部署者可以在未遵守限制性许可证的情况下，对模型进行微调、量化、剪枝等修改，并将其部署为黑盒API服务。模型所有者需要一种技术手段，能够从黑盒API的查询-回复交互中，可靠地判定该服务背后的模型是否源自自己发布的版本——这就是**模型指纹识别**（Model Fingerprinting）要解决的核心问题。

### 现有方法的瓶颈

当前主流的黑盒模型指纹方法依赖“查询-密钥”对机制，存在两个结构性缺陷：

**查询端的脆弱性。** 现有方法使用少量固定查询作为指纹触发器。**Instructional Fingerprinting (IF)**（Xu et al., 2024a）仅使用8个固定查询，而**Scalable Fingerprinting (SF)**（Nasery et al., 2025）将其扩展到1024个。然而，这些固定查询集在模型经历微调、量化、剪枝等常见部署修改后极易失效——模型对这些特定查询的“记忆”被覆盖或扭曲，导致指纹检测失败。

**密钥端的暴露风险。** 现有方法要求模型对特定查询返回固定的非典型回复字符串作为“密钥”。这种模式存在双重隐患：其一，精确字符串匹配的检测方式在模型输出被改写、采样变化或系统提示修改后立即失效；其二，非典型的查询/回复模式容易被恶意部署者通过异常检测手段识别和过滤，缺乏隐蔽性。

简言之，现有指纹方法陷入了两难：要么指纹信号足够强但容易被发现和移除，要么指纹隐蔽但极易被部署修改所破坏。

### 本文的核心动机

本文提出一种新的指纹范式，从根本上重新设计指纹的“查询”和“密钥”：

- **用完整的语义域替代有限的查询集。** 不再依赖少量固定查询，而是将整个语义域（如法语）作为指纹触发域——域内任意查询均可触发指纹信号。这从根本上解决了查询端脆弱性问题，因为对手无法通过过滤特定查询来规避检测。

- **用扩散的统计水印信号替代脆弱的固定密钥。** 将红绿列表水印（Red-Green Watermark）的统计信号扩散在模型回复的整个文本序列中，信号强度随回复长度累积，而非依赖精确字符串匹配。这使得指纹对采样变化、输出改写等修改具有天然鲁棒性。

- **语义条件触发保证隐蔽性。** 水印信号仅在目标语义域内被激活，在域外查询中完全无泄漏。这使得指纹在常规使用中不可察觉，对手难以通过监控API流量来发现指纹的存在。

这一设计将指纹从“点对点”的脆性匹配转变为“域对信号”的统计检测，在隐蔽性和鲁棒性之间建立了新的平衡点。



## 核心方法与创新机理

本文提出了一种全新的模型指纹范式，其核心创新在于用**语义条件水印**替代了传统黑盒指纹中脆弱的固定“查询-密钥”对机制。具体而言，该方法在三个关键维度上实现了根本性重构：

**1. 从有限查询集到完整语义域**

现有基线方法依赖少量固定查询：**Instructional Fingerprinting (IF)**（Xu et al., 2024a）仅使用8个查询-密钥对，而**Scalable Fingerprinting (SF)**（Nasery et al., 2025）扩展至1024对。这些固定查询模式极易被恶意部署者检测和过滤。本文方法将指纹触发条件扩展为**完整的语义域**（如法语），使得该域内任意查询均可触发指纹信号，从根本上解决了查询隐蔽性问题。

**2. 从固定密钥到统计水印信号**

IF和SF依赖固定的非典型回复字符串作为密钥，这些字符串在微调、量化、剪枝等常见部署修改后极易失效。本文改用**红绿水印（Red-Green Watermark）**机制：在每个生成步骤中，词表被伪随机地划分为绿令牌（比例 $\gamma$）和红令牌（比例 $1-\gamma$），指纹信号以统计偏差的形式扩散在整个响应中，其强度随文本长度累积增加，从而获得对部署修改的天然鲁棒性。

**3. 从精确匹配到统计假设检验**

检测方式从精确字符串匹配升级为基于**Z检验**的统计判定。检测者收集 $Q$ 个语义域内查询的API回复，拼接为单一序列 $\omega$，计算绿令牌比例 $\hat{\gamma}(\omega)$ 与期望值 $\gamma$ 的偏差：

$$Z(\omega) = \frac{\hat{\gamma}(\omega) - \gamma}{\beta(\omega) \sqrt{\gamma(1-\gamma)/|\omega|}}$$

其中 $\beta(\omega)$ 为考虑上下文重复的方差校正项。该检测框架可控制误报率（FPR）并随查询量累积证据，实现了从“全或无”的精确匹配到可扩展统计推断的跃迁。

**4. 指纹嵌入的联合优化目标**

指纹嵌入采用**蒸馏损失 + 正则化损失**的联合优化，而非基线方法的简单监督微调（SFT）。在语义域数据集上，最小化学生模型 $\theta$ 与经过红绿水印处理的教师 $\theta_0$ 之间的KL散度：

$$L_{\mathrm{watermark}}(\theta, \xi)(x) = \sum_{t=1}^{|x|} \mathrm{KL}\big(\mathrm{Red-Green}(p_{\theta_0}(.|x_{<t}), \xi), p_{\theta}(.|x_{<t})\big)$$

同时在正则化数据集上，仅惩罚学生分布相对于教师分布的**正向偏差**，防止域外行为退化：

$$L_{\mathrm{reg}}(\theta)(x) = \sum_{t=1}^{|x|} \max\left( p_{\theta}(.|x_{<t}) - p_{\theta_0}(.|x_{<t}), 0 \right)$$

这一设计确保了水印信号仅在目标语义域内被蒸馏，而在其他域上模型行为得以完整保留，实现了隐蔽性与通用能力的兼顾。消融实验证实，去除正则化后指纹检测率虽仍为1.0，但基准准确率（尤其是HumanEval）下降更明显，验证了 $L_{\mathrm{reg}}$ 对保持模型通用能力的关键作用。



本文提出了一种全新的模型指纹范式，其核心思路是将指纹信号从脆弱的固定“查询-密钥”对迁移到语义域与统计水印的组合空间中。整体框架由两个对称的流水线模块构成：**指纹嵌入**与**指纹检测**。

### 指纹嵌入

嵌入阶段的目标是让模型学会仅在特定语义域（如法语）内生成带有红绿水印统计特征的文本，而在其他域上保持原始行为不变。这一过程通过一个联合优化目标实现，该目标包含两项损失：

- **域内水印蒸馏损失**：在语义域数据集上，以冻结的原始模型 $\theta_0$ 为教师，使用红绿水印规则对教师输出分布进行扰动，然后最小化学生模型 $\theta$ 与扰动后教师分布之间的 KL 散度。这迫使模型在语义域内学会生成富含绿令牌的响应。
- **域外正则化损失**：在正则化数据集（与语义域不相交）上，仅惩罚学生分布相对于教师分布的正向概率偏差，即 $\max(p_\theta - p_{\theta_0}, 0)$。这确保模型在非目标域上的生成分布不发生显著漂移。

算法以迭代方式交替优化上述两项损失，直至收敛。指纹嵌入后，模型在语义域内任意查询的响应中都将携带可累积的统计水印信号，而在域外查询中则无信号泄漏。

### 指纹检测

检测阶段利用语义域内查询的 API 回复来判定目标模型是否被指纹化。流程如下：

1. **查询收集**：向目标 API 发送 $Q$ 个语义域内查询，收集对应的完整回复。
2. **序列拼接**：将所有回复拼接为单一长序列 $\omega$。
3. **统计检验**：计算 $\omega$ 中绿令牌的比例 $\hat{\gamma}(\omega)$，并与期望绿令牌比例 $\gamma$ 比较，构造 Z 检验统计量。该统计量考虑了上下文重复带来的方差校正，信号强度随响应长度自然累积。
4. **阈值判定**：将 Z 分数与预设阈值（基于 $10^{-3}$ 的误报率）比较，若超过阈值则判定模型已被指纹化。

### 输入输出流

- **嵌入阶段输入**：语义域数据集 $D_{\text{domain}}$（如法语语料）、正则化数据集 $D_{\text{reg}}$（通用语料）、红绿水印私钥 $\xi$。
- **嵌入阶段输出**：指纹化模型 $\theta$，在语义域内携带水印信号，域外行为与原始模型一致。
- **检测阶段输入**：目标 API 接口、语义域查询集合。
- **检测阶段输出**：二元判定（已指纹化/未指纹化），以及相应的统计置信度。

该框架通过将指纹信号绑定到语义域而非固定查询，从根本上解决了传统方法在查询隐蔽性和部署鲁棒性上的双重瓶颈。



本方法的核心由两个模块构成：**指纹嵌入**（Sec. 4.1）与**指纹检测**（Sec. 4.2）。前者通过蒸馏–正则化联合优化将红绿水印信号绑定到目标语义域；后者通过拼接多查询回复并执行Z检验来判定模型是否被指纹化。

### 指纹嵌入模块

指纹嵌入的目标是让模型仅在特定语义域（如法语）的回复中携带可检测的水印信号，而在其他域保持原始行为不变。这通过以下两个损失项的联合优化实现（Algorithm 1）：

**语义域水印蒸馏损失**（Eq. 1）：在语义域序列 $x$ 上，最小化学生模型 $\theta$ 与经过红绿水印处理的冻结教师模型 $\theta_0$ 输出分布之间的 KL 散度，从而将水印行为蒸馏到模型中：

$$L_{\mathrm{watermark}}(\theta, \xi)(x) = \sum_{t=1}^{|x|} \mathrm{KL}\big(\mathrm{Red\text{-}Green}(p_{\theta_0}(\cdot|x_{<t}), \xi),\, p_{\theta}(\cdot|x_{<t})\big)$$

其中 $\xi$ 为水印私钥，$\mathrm{Red\text{-}Green}(\cdot)$ 表示在每步生成时根据 $\xi$ 和前缀 $x_{<t}$ 伪随机地将词表划分为绿令牌（比例 $\gamma$）和红令牌，并提升绿令牌的 logits 值。

**域外正则化损失**（Eq. 2）：在正则化数据集 $D_{\mathrm{reg}}$（与语义域不重叠）上，仅惩罚学生分布相对于教师分布的正向概率偏差，防止域外行为退化：

$$L_{\mathrm{reg}}(\theta)(x) = \sum_{t=1}^{|x|} \max\big(p_{\theta}(\cdot|x_{<t}) - p_{\theta_0}(\cdot|x_{<t}),\, 0\big)$$

该损失是总变差距离的变体，只约束学生不要“过度偏离”教师，而不强制完全匹配，从而在保留域外生成质量的同时为域内水印学习留出空间。消融实验（Table 8）证实，去除 $L_{\mathrm{reg}}$ 后指纹检测率仍为 1.0，但基准准确率（尤其是 HumanEval）下降更明显，验证了正则化对维持通用能力的关键作用。

### 指纹检测模块

检测时，模型所有者收集 $Q$ 个语义域内查询的 API 回复，拼接为单一序列 $\omega$，计算 Z 检验统计量（Eq. 3）：

$$Z(\omega) = \frac{\hat{\gamma}(\omega) - \gamma}{\beta(\omega)\sqrt{\gamma(1-\gamma)/|\omega|}}$$

其中 $\hat{\gamma}(\omega)$ 为 $\omega$ 中绿令牌的观测比例，$\gamma$ 为期望比例，$\beta(\omega)$ 为考虑上下文重复的方差校正项，$|\omega|$ 为序列长度。将 $Z(\omega)$ 与预设阈值（基于目标 FPR = $10^{-3}$）比较，即可判定模型是否被指纹化。由于信号强度随拼接文本长度累积，该方法在量化、剪枝、微调等部署修改后仍能保持高检测力。



## 实验与关键发现

### 核心主张与实验设计逻辑

本文的实验围绕三个递进命题展开：**（1）指纹有效性**——能否在不损害通用能力的前提下实现完美检出；**（2）部署鲁棒性**——指纹能否在25种常见部署修改和5种针对性对抗下存活；**（3）隐蔽性**——指纹查询和回复是否会被对手察觉。所有实验在LLaMA3.2-1B、Qwen2.5-3B、LLaMA3.1-8B三个规模模型上完成，基线方法为**Instructional Fingerprinting（IF）**（Xu et al., 2024a）和**Scalable Fingerprinting（SF）**（Nasery et al., 2025），检测阈值统一控制FPR为$10^{-3}$。

### 主结果：指纹有效性与效用保持

Table 1给出了核心有效性证据。在法语语义域上嵌入指纹后，三个模型的**指纹成功率（FSR）均为1.0**，而未指纹化的基座模型FSR为0——这意味着零误报。更关键的是，8项基准测试的平均准确率几乎未受影响：LLaMA3.2-1B保持0.42，Qwen2.5-3B保持0.58，LLaMA3.1-8B保持0.63，与基座模型偏差不超过0.01。唯一的例外是LLaMA3.2-1B在HumanEval上的轻微下降，这与其容量较小有关。这一结果直接验证了正则化损失$L_{\mathrm{reg}}$（Eq. 2）的设计有效性——它仅惩罚学生分布相对于教师的正向偏差，从而在蒸馏水印信号的同时保留了域外行为。


![[assets/figures/papers/paper_list_l20_https_openreview_net_forum_id_t38nZqqi3Z/figures/002_Table_1.jpg]]
*Table 1: Effectiveness of Our Fingerprint We compare the Fingerprint Success Rate (FSR) of 3 models with and without the fingerprint. We also compare utility, measured via benchmark accuracy, and report the average in the last column (AVG). We highlight in bold FSR values of 1.0. We highlight in blue the benchmark in French, as it uses the same semantic domain as our fingerprint*

### 部署鲁棒性：25种场景全覆盖

Table 2系统评估了通用部署修改下的鲁棒性，涵盖采样变化、系统提示、量化（4-bit/8-bit）、剪枝（非结构化/结构化）、微调等场景。**本文方法在所有25种部署下FSR均为1.0**，而IF和SF在多数场景下彻底失效（FSR=0.0）。以量化和微调为例：SF对量化极为敏感，IF在微调后完全丧失指纹；本文方法借助红绿水印的统计信号累积机制——响应越长，绿令牌比例的统计显著性越强——即使模型权重被修改，水印的分布特征仍可被Z检验捕获。


![[assets/figures/papers/paper_list_l20_https_openreview_net_forum_id_t38nZqqi3Z/figures/003_Table_2.jpg]]
*Table 2: Robustness Evaluation Against Prominent Deployments We compare the Fingerprint Success Rate of LLAMA3.2-1B. QWEN2.5-3B and LLAMA3.1-8B models fingerprinted with either IF, SF or our fingerprint under various deployment scenarios. We highlight in green FSR of 1.0. Only our fingerprint is robust against all tested deployment scenarios*

Table 3进一步评估针对性对手：输入改写（paraphrasing）、回译、英文预填充、系统提示注入、以及针对法语域的微调。**本文方法在所有5种对抗下FSR保持1.0**。值得注意的是，即使对手用大量法语对话数据微调模型试图覆盖指纹信号，由于水印信号已通过蒸馏嵌入模型的生成分布中，而非依赖表面字符串记忆，微调无法轻易消除。


![[assets/figures/papers/paper_list_l20_https_openreview_net_forum_id_t38nZqqi3Z/figures/004_Table_3.jpg]]
*Table 3: Robustness Evaluation Against Targeted Adversaries We compare the Fingerprint Success Rate of LLAMA3.2-1B. QWEN2.5-3B and LLAMA3.1-8B models fingerprinted with either IF, SF or our fingerprint against targeted adversaries particularly adversarial for our fingerprint. We highlight in green FSR of 1.0. Our fingerprint remains robust against all tested adversaries*

### 隐蔽性评估：对手难以察觉

Figure 2使用GPT5-MINI作为裁判模型，评估指纹查询和回复的可检测性。**本文方法的查询和回复被裁判模型召回的比率显著低于IF和SF**——IF和SF的固定非典型查询-密钥对极易被识别为异常模式，而本文方法使用完整语义域（如任意法语查询），查询本身是正常的自然语言，回复中的水印信号以统计方式扩散而非以固定字符串形式出现，因此对手难以从流量中筛选出指纹活动。


![[assets/figures/papers/paper_list_l20_https_openreview_net_forum_id_t38nZqqi3Z/figures/005_Figure_2.jpg]]
*Figure 2: Stealth Evaluation FPR (Left) and Recall (Right) (i.e., percentage of detected fingerprint queries/replies over all fingerprint queries/replies) of our GPT5-MINI-judge when detecting queries/replies of our fingerprint, IF and SF. A lower recall indicates a stealthier fingerprint*

### 消融实验：关键设计选择

**正则化损失的不可替代性**（Table 8）：去除$L_{\mathrm{reg}}$后，FSR仍为1.0，但HumanEval等基准准确率下降更明显。这表明蒸馏损失$L_{\mathrm{watermark}}$单独即可嵌入水印，但会侵蚀域外能力；正则化项是维持通用任务表现的关键。


![[assets/figures/papers/paper_list_l20_https_openreview_net_forum_id_t38nZqqi3Z/figures/018_Table_8.jpg]]
*Table 8: Effectiveness of Our Fingerprinting Method We compare the Fingerprint Success Rate (FSR) of our method with (Ours) and without the regularization (Ours (w/o)). We also compare the utility, measured through benchmark accuracy, and report the average accuracy in the last column (AVG). We highlight in bold FSR values above 80%*

**语义域的可迁移性**（Table 7）：在法语、医学、数学三个语义域上分别训练和检测指纹，FSR均为1.0。但医学域因低熵特性导致绿令牌比例的自然波动更大，需要更多查询才能达到相同统计显著性——这是该方法的已知局限。


![[assets/figures/papers/paper_list_l20_https_openreview_net_forum_id_t38nZqqi3Z/figures/014_Table_7.jpg]]
*Table 7: Effectiveness of Our Fingerprinting Method On Different Semantic Domains We compare the Fingerprint Success Rate (FSR) of QWEN2.5-3B fingerprinted on three different domains. We also compare the utility, measured through benchmark accuracy, and report the average accuracy in the last column (AVG). We highlight in bold FSR values of 1.0*

**水印强度的效用-鲁棒性权衡**（Figure 8）：增大水印强度$\delta$可提升检测信号，但同时提高困惑度（PPL），体现了生成质量与检测鲁棒性之间的可控权衡。

**语义条件触发的精确性**（Figure 9）：指纹信号仅在训练域内被检测到，其他域无泄漏——验证了语义条件水印的域特异性，这是隐蔽性的核心保障。

**全量水印 vs. 语义条件水印**（Figure 4）：对全量水印（无语义条件）进行微调后，检测性急剧下降；而语义条件水印在相同微调下保持鲁棒。这说明将水印信号绑定到特定语义域是抵御微调攻击的关键机制。

### 失败模式与局限

1. **域内生成质量下降**：Table 4显示，GPT5-MINI裁判对域内回复的评分从约5.10降至3.18，表明水印蒸馏会影响语义域内的文本可读性——这是信号嵌入的固有代价。

![[assets/figures/papers/paper_list_l20_https_openreview_net_forum_id_t38nZqqi3Z/figures/007_Table_4.jpg]]
*Table 4: Additional Quality Metrics We study the impact on quality, measured through perplexity and GPT5-MINI-as-a-judge, and report the average across a thousand samples. The samples are generated on three different semantic domains: a general Q&A Domain, on Math questions and on French questions*

2. **低熵域检测延迟**：医学域需要更多查询才能达到$10^{-3}$ FPR下的可靠检测，延长了判定时间。
3. **训练成本**：指纹嵌入需处理约81.92M tokens（约$6），显著高于IF/SF的SFT方案（$<1），可能限制大规模快速部署。
4. **对抗性微调的极限未探明**：虽然实验覆盖了法语域微调，但对手若用更大规模、更高质量的目标域数据进行针对性微调，指纹鲁棒性的边界仍需进一步验证。

### 补充图表

![[assets/figures/papers/paper_list_l20_https_openreview_net_forum_id_t38nZqqi3Z/figures/020_Figure_10.jpg]]
*Figure 10: ROC curves for evaluating semantically conditioned watermarks with a watermark token (left) or an (opening,closing) watermark token (right)*

![[assets/figures/papers/paper_list_l20_https_openreview_net_forum_id_t38nZqqi3Z/figures/021_Figure_11.jpg]]
*Figure 11: ROC curves for evaluating semantically conditioned watermark with a different key per watermark token. Figure 12: ROC curve for evaluating semantically conditioned watermark on the harmful domain*

![[assets/figures/papers/paper_list_l20_https_openreview_net_forum_id_t38nZqqi3Z/figures/008_Table_5.jpg]]
*Table 5: Complementary Robustness Evaluation We compare the Fingerprint Success Rate of LLAMA3.2-1B. QWEN2.5-3B and LLAMA3.1-8B models fingerprinted with either IF, SF or our fingerprint; after various modifications. We highlight in green FSR value of 1.0, as in Table 2*

![[assets/figures/papers/paper_list_l20_https_openreview_net_forum_id_t38nZqqi3Z/figures/012_Table_6.jpg]]
*Table 6: Evaluation of Our Fingerprint Impact on Finetuneability We compare the benchmark performance of QWEN2.5- 3B models (without/with our fingerprint on French) on taskspecific benchmarks (respectively GalicianBench and French-Bench) before and after finetuning on the corresponding datasets (respectively AlpacaGalician and WildChatFr)*

![[assets/figures/papers/paper_list_l20_https_openreview_net_forum_id_t38nZqqi3Z/figures/022_Table.jpg]]




## 定位与知识库关联

### 1. 问题瓶颈与因果机制

现有黑盒模型指纹方法的核心瓶颈在于：**固定的“查询-密钥”对在微调、量化、剪枝等常见部署修改后极易失效**。具体而言，**Instructional Fingerprinting (IF)**（Xu et al., 2024a）和 **Scalable Fingerprinting (SF)**（Nasery et al., 2025）均依赖少数几个固定查询（IF 8个，SF 1024个）来构建“查询-密钥”对。这些非典型查询/密钥模式极易被恶意部署者检测和过滤，缺乏隐蔽性。

本文提出的**基于语义条件水印的LLM指纹识别**方法，通过将完整的语义域（如法语）替代有限的查询集，用基于红绿水印的统计信号（在整个响应中扩散、强度随令牌数增加）替代脆弱的固定密钥，通过语义条件水印蒸馏将信号绑定到该域中，从而实现了从“查询-密钥”到“语义条件水印”的转变。

### 2. 方法沿革与对比基线

与现有工作相比，本文方法的核心改进在于：

1. **查询域**：从少量固定查询（IF 8个，SF 1024个）扩展到完整语义域（如法语），任意域内查询均触发指纹。
2. **密钥/信号**：从固定的非典型回复字符串，转变为扩散在响应中的统计水印信号（红绿水印），强度随文本长度增加。
3. **检测方式**：从精确字符串匹配，转变为拼接多个响应后使用Z检验，可控制FPR并积累证据。

### 3. 指纹嵌入损失与正则化

与仅使用监督微调（SFT）记忆查询-密钥对的基线方法相比，本文方法通过蒸馏损失（域内） + 正则化损失（域外）的联合优化，实现了从“查询-密钥”到“语义条件水印”的转变。

**指纹嵌入**：通过迭代优化，在语义域数据集上蒸馏红绿水印分布，同时在正则化数据集上惩罚偏离原模型的正向概率偏差。

### 4. 实验设计与评估

在25种部署场景（采样变化、系统提示、量化、剪枝、微调）和5种针对性对抗（输入/输出改写、预填充等）下，本文方法均达到FSR 1.0，基线方法则频繁失败。

**指纹检测**：在模型被指纹化时系统上检出，未指纹化模型检出率为0，且基准准确率未显著下降（平均ACC保持或仅有少量波动）。

**隐蔽性评估**：表明，本文方法的查询和回复被GPT5-MINI法官召回率显著低于IF和SF，对手难以察觉指纹。

**指纹信号**：仅在训练域内被检测到，其他域无泄漏，证明语义条件触发有效。

**语义条件水印**：相比全量水印在微调后鲁棒性显著更强，全量水印的检测性急剧下降。

**指纹嵌入**：通过迭代优化，在语义域数据集上蒸馏红绿水印分布，同时在正则化数据集上惩罚偏离原模型的正向概率偏差。

### 5. 局限与开放问题

**未评估对所有权证明的法律/社区可执行性**，仅提供技术方案。

**能否使用开闭区间Watermark Token仅对推理模型的思考过程或答案进行水印，从而进一步降低对生成质量的影响？**

**如何防止恶意部署者通过微调目标域语言数据来削弱语义条件指纹？**

**在真实世界API监控场景中，如何平衡查询量、检测延迟与误报率？**

**指纹嵌入**：通过迭代优化，在语义域数据集上蒸馏红绿水印分布，同时在正则化数据集上惩罚偏离原模型的正向概率偏差。

### 6. 实验设计与评估

在25种部署场景（采样变化、系统提示、量化、剪枝、微调）和5种针对性对抗（输入/输出改写、预填充等）下，本文方法均达到FSR 1.0，基线方法则频繁失败。

**指纹检测**：在模型被指纹化时系统上检出，未指纹化模型检出率为0，且基准准确率未显著下降（平均ACC保持或仅有少量波动）。

**隐蔽性评估**：表明，本文方法的查询和回复被GPT5-MINI法官召回率显著低于IF和SF，对手难以察觉指纹。

**指纹信号**：仅在训练域内被检测到，其他域无泄漏，证明语义条件触发有效。

**语义条件水印**：相比全量水印在微调后鲁棒性显著更强，全量水印的检测性急剧下降。

**指纹嵌入**：通过迭代优化，在语义域数据集上蒸馏红绿水印分布，同时在正则化数据集上惩罚偏离原模型的正向概率偏差。

### 7. 开放问题与局限

**未评估对所有权证明的法律/社区可执行性**，仅提供技术方案。

**能否使用开闭区间Watermark Token仅对推理模型的思考过程或答案进行水印，从而进一步降低对生成质量的影响？**

**如何防止恶意部署者通过微调目标域语言数据来削弱语义条件指纹？**

**在真实世界API监控场景中，如何平衡查询量、检测延迟与误报率？**

**指纹嵌入**：通过迭代优化，在语义域数据集上蒸馏红绿水印分布，同时在正则化数据集上惩罚偏离原模型的正向概率偏差。

### 8. 结论与未来工作

本文提出的方法，通过将完整的语义域（如法语）替代有限的查询集，用基于红绿水印的统计信号（在整个响应中扩散、强度随令牌数增加）替代脆弱的固定密钥，通过语义条件水印蒸馏将信号绑定到该域中，从而实现了从“查询-密钥”到“语义条件水印”的转变。



## 原文 PDF

![[paperPDFs/ICLR_2026/LLM_Fingerprinting_via_Semantically_Conditioned_Watermarks.pdf]]
