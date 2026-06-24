---
title: "Expanding the Capability Frontier of LLM Agents with ZPD-Guided Data Synthesis"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/Expanding_the_Capability_Frontier_of_LLM_Agents_with_ZPD_Guided_Data_Synthesis.pdf
openreview_forum_id: c5bf47nDx1
aliases:
- AE
- ECFLAZGDS
tags:
- ICLR_2026
- topic/reinforcement_learning_planning_agents
- topic/reinforcement_learning_planning_agents/planning_control
core_operator: "通过引入教育心理学的最近发展区（ZPD）理论，定义知识较少同伴（LKP）与知识较多他人（MKO）两个角色，利用对抗校准动态识别模型ZPD内的任务，并生成兼具知识广度与推理深度的训练数据，驱动代理能力向MKO演进。"
primary_logic: "将最近发展区操作化为可度量的计算框架，通过两角色验证自动筛选那些模型无法独立解决但借助工具便能掌握的任务。这种ZPD引导的数据合成可持续产生对模型成长最优的学习材料，使模型从知识检索者进化为深度研究代理。"
claims:
- "AgentFrontier在四个多学科基准上全面超越先前微调数据集，尤其在HLE上达到25.7%（Qwen3-30B-A3B RFT），对比最佳基线MegaScience的20.2%提升显著。"
- "引入CPT后，AgentFrontier-30B-A3B在HLE上达到28.6%，超越若干专有深度研究代理，验证了知识密集型CPT数据的价值。"
- "消融实验证实ZPD数据筛选策略显著优于随机采样，平均增益达4-10个绝对百分点，证明筛选策略的有效性。"
- "LKP/MKO配置消融表明，平衡的能力间隙（DeepSeek-R1 vs DeepSeek-V3.1+工具）提供了产率与复杂度的最优权衡，验证了对抗校准设计的合理性。"
---

# Expanding the Capability Frontier of LLM Agents with ZPD-Guided Data Synthesis

> [!tip] 核心洞察
> 将最近发展区操作化为可度量的计算框架，通过两角色验证自动筛选那些模型无法独立解决但借助工具便能掌握的任务。这种ZPD引导的数据合成可持续产生对模型成长最优的学习材料，使模型从知识检索者进化为深度研究代理。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 基于最近发展区指导的数据合成拓展大型语言模型代理能力前沿 |
| 英文题名 | Expanding the Capability Frontier of LLM Agents with ZPD-Guided Data Synthesis |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=c5bf47nDx1) |
| Topic | #topic/reinforcement_learning_planning_agents #topic/reinforcement_learning_planning_agents/planning_control |
| Method | AgentFrontier Engine |
| Dataset | Humanity's Last Exam (HLE), ZPD Exam-v1, xBench-ScienceQA |

> [!tip] 效果简介
> - Humanity's Last Exam (HLE) 上，Accuracy (%) 为 25.7，对比 20.2 (MegaScience)，变化 +5.5。
> - ZPD Exam-v1 上，Accuracy (%) 为 91.4，对比 90.0 (MegaScience)，变化 +1.4。
> - xBench-ScienceQA 上，Accuracy (%) 为 54.0，对比 48.0 (MegaScience)，变化 +6.0。

## 概述

当前大型语言模型（LLM）代理在跨文档知识融合与复杂推理方面仍存在显著能力瓶颈，其根源在于缺乏位于模型“能力前沿”的高质量多学科训练数据。现有数据合成方法多采用单步查询生成或文档中心策略，以粗粒度难度标签控制任务复杂度，难以精准匹配模型当前可塑性最强的学习区间。

本文引入教育心理学的**最近发展区（Zone of Proximal Development, ZPD）**理论，提出 **AgentFrontier Engine**——一个由ZPD引导的三阶段数据合成框架。该框架定义两个对抗角色：**知识较少同伴（LKP）**与**知识较多他人（MKO）**，通过二元校验自动识别模型无法独立解决但借助工具便能掌握的任务，从而持续生成对模型成长最优的学习材料。核心洞察在于将ZPD操作化为可度量的计算框架：LKP失败而MKO成功的问题，恰好处于模型的能力发展前沿。

实验表明，基于AgentFrontier数据训练的模型在四个多学科基准上全面超越先前微调数据集。在最具挑战性的 **Humanity’s Last Exam (HLE)** 上，Qwen3-30B-A3B经拒绝采样微调（RFT）后达到25.7%，较最佳基线MegaScience的20.2%提升5.5个百分点；引入继续预训练（CPT）后进一步达到28.6%，超越若干专有深度研究代理。消融实验证实，ZPD数据筛选策略相比随机采样带来4至10个绝对百分点的平均增益，验证了该策略的有效性。

## 背景与动机

### 大型语言模型代理的能力瓶颈

大型语言模型（LLM）驱动的自主代理在复杂推理与工具调用方面取得了长足进步，但其能力增长正面临一个根本性瓶颈：**缺乏位于模型能力前沿的高质量训练数据**。现有代理的训练数据主要来源于两类途径：一是单步查询生成，即从单一文档或知识源直接生成问答对；二是文档中心生成，围绕特定文档构造任务。这两种范式产生的数据往往停留在模型已掌握的“舒适区”内——模型无需深度知识融合即可独立解决，因而无法有效驱动能力向更高层次演进。

真正推动代理从“知识检索者”进化为“深度研究者”的关键，在于培养两种核心能力：（1）**跨文档知识融合**——从多个异构信息源中提取、关联并综合证据；（2）**复杂多步推理**——在工具辅助下进行迭代验证、数值计算与逻辑推演。然而，如何系统性地生成恰好处于模型当前能力边界、需要“跳一跳才够得着”的训练数据，一直缺乏可操作的计算框架。

### 现有数据合成方法的局限

当前多学科代理微调数据集（如 **TaskCraft**、**MegaScience**、**MiroVerse**）虽然在数据规模和学科覆盖上取得了进展，但在数据生成机制上存在两个共同缺陷：

1. **难度控制粗粒度**：依赖预定义的难度标签或简单的规则堆叠来区分任务难度，无法动态感知特定模型的能力边界。同一道题对不同能力的模型而言，可能过于简单（已在舒适区）或过于困难（超出可学习范围），静态标签无法捕捉这种相对性。

2. **数据筛选缺乏理论指导**：训练数据的选择通常基于随机采样或答案正确性过滤，而非依据任务对模型成长的实际价值。这导致大量训练样本要么是模型已掌握的冗余信息，要么是完全无法企及的噪声，真正能驱动能力跃迁的“最优学习材料”被稀释。

### 最近发展区理论的引入

本文从教育心理学中汲取核心洞见，将维果茨基（Vygotsky, 1978）的**最近发展区**（Zone of Proximal Development, ZPD）理论操作化为可度量的计算框架。ZPD理论指出，学习者在“知识较少同伴”（Less Knowledgeable Peer, LKP）与“知识较多他人”（More Knowledgeable Other, MKO）之间存在一个发展区间——学习者无法独立完成任务，但在适当指导下能够掌握。这正是能力成长的最优区间。

我们将这一思想映射到LLM代理训练中（图1），定义两个角色：
- **LKP**：基础LLM（如DeepSeek-R1，不使用工具），代表模型当前独立能力水平；
- **MKO**：工具增强的强代理（如DeepSeek-V3.1 + 搜索/学者/浏览器/代码工具），代表模型通过辅助可达的能力上限。

通过对抗校准，自动筛选出那些LKP无法独立解决、但MKO能够验证正确的任务——这些任务恰好落在模型的ZPD内，构成了对能力成长最优价值的训练数据。这种ZPD引导的数据合成策略，能够持续产生推动代理从LKP向MKO演进的学习材料，从根本上区别于传统的数据生成范式。

## 核心创新

### 1. 从“文档中心”到“知识融合”的数据生成范式

现有代理微调数据集（如TaskCraft、MegaScience、MiroVerse）通常采用单步查询生成或围绕单一文档构建任务，难以培养模型跨文档、跨源的知识融合能力。AgentFrontier Engine的核心创新在于将数据生成的基本单元从“单一文档”提升为“复合文档单元”——即主题相似度高于阈值 $\tau_{\mathrm{theme}}$ 的文档块三元组。在此基础上，生成器 $\mathcal{M}_{\mathrm{gen}}$ 被要求从这些多元信息源中合成需要**知识融合**的初始问答对：

$$\mathcal{D}_{\mathrm{seed}} = \{ (q_0, a_0) = \mathcal{M}_{\mathrm{gen}}(U_c) \mid U_c \text{ is a composite unit} \}$$

这一设计直接回应了深度研究代理的核心能力需求：在分散的学术文献、网页、代码库之间建立联系并形成综合判断。Table 1显示，AgentFrontier生成的轨迹在工具使用上呈现出更均衡的分布（搜索0.32、学者0.66、浏览器0.82、代码0.52），而基线数据集往往过度依赖单一工具类型——例如TaskCraft的浏览器调用高达1.43次/轨迹，但学者和代码调用几乎为零，反映出其数据生成策略对知识广度的忽视。

### 2. 工具增强的四维度迭代精炼

传统数据集的难度控制依赖粗粒度标签或规则堆叠，缺乏对推理深度和工具使用的系统性设计。AgentFrontier的Stage II引入了一个集成搜索、学者检索、浏览器、代码执行器的精炼代理（基于DeepSeek-R1），对种子问题进行四个维度的定向升维：

- **知识扩展**：引入额外的相关文献或事实来源
- **概念抽象**：将具体问题提升为需要跨领域概念迁移的形式
- **事实验证**：要求对答案中的关键事实进行溯源和交叉验证
- **计算转化**：将定性分析转化为定量计算任务

Figure 6展示了一个典型案例：一个生物医学种子问题经过迭代精炼，最终演变为需要综合学术文献检索、诊断推理和计算验证的复杂临床问题。这种**工具增强的迭代精炼**使得生成的数据天然包含了多轮推理轨迹和多样化的工具调用模式，与ReAct范式下的代理行为高度一致。

### 3. 最近发展区（ZPD）对抗校准：从“能做”到“将能做”

这是AgentFrontier最核心的理论创新。现有方法通常基于答案正确与否进行简单的数据筛选（如拒绝采样），但无法区分“模型已经掌握的简单任务”和“模型尚未掌握但具备学习潜力的任务”。AgentFrontier将教育心理学的ZPD理论操作化为可计算的双角色验证框架：

- **知识较少同伴（LKP）**：以无工具的基础DeepSeek-R1-0528实例化，代表模型的当前能力边界
- **知识较多他人（MKO）**：以工具增强的DeepSeek-V3.1代理实例化，代表模型通过工具使用可达的潜在能力边界

ZPD过滤的核心逻辑是：仅保留那些LKP无法独立解决（$IsSolvableBy(A_{LKP}, q, a) = 0$）、但MKO通过工具和推理能够验证正确的任务。具体而言，MKO进行Best-of-N验证（N次独立求解），若至少一次正确，则该任务被划入 $\mathcal{D}_{ZPD}$ 用于后续训练：

$$\sum_{i=1}^N IsCorrect(s_i, a) \geq 1$$

这一设计的因果机制在于：**对抗校准**动态识别了位于模型能力前沿的任务——它们既非已掌握的（LKP可解），也非不可企及的（MKO也无法验证），恰好处于“借助脚手架即可掌握”的最优学习区间。

### 4. 消融验证：ZPD筛选策略的决定性作用

Table 13的消融实验直接证实了ZPD筛选策略相比随机采样的显著优势：在所有骨干模型和所有基准上，ZPD筛选带来的绝对提升在0.8至10.0个百分点之间。这一证据排除了“数据量增加”或“生成质量提升”等替代解释，直接锚定了ZPD筛选作为因果瓶颈的关键地位。

LKP/MKO配置的消融（Table 4）进一步揭示了能力间隙的精细权衡：
- **平衡间隙**（DeepSeek-R1 vs DeepSeek-V3.1+工具）：实现33.1%的ZPD数据产率，平均3.32轮推理和2.32次工具调用，产率与复杂度的最优权衡
- **更宽间隙**（Qwen3-8B vs DeepSeek-V3.1+工具）：产率提升44.1%至47.7%，但平均轮次下降44.3%，工具调用下降63.4%，数据趋于简化
- **更窄间隙**（DeepSeek-V3.1 vs DeepSeek-V3.1+工具）：产率下降27.5%至24.0%，复杂度保持但效率受损

这表明对抗校准框架对能力间隙的选择高度敏感，平衡间隙恰好捕捉了“工具使用”这一关键脚手架的作用——LKP与MKO的核心差异不在于基础推理能力，而在于工具增强带来的知识获取和验证能力，这正是深度研究代理需要培养的核心技能。

### 5. 训练管线的协同创新：CPT + RFT

传统代理微调仅依赖拒绝采样微调（RFT），AgentFrontier引入了继续预训练（CPT）作为前置阶段：先使用50B token的知识密集型数据（来自 $\mathcal{D}_{ZPD}$ 中高知识密度的子集）进行标准语言建模训练：

$$\mathcal{L}_{\mathrm{CPT}}(\theta) = -\sum_{t=1}^T \log p_{\theta}(x_t \mid x_{<t})$$

随后再对12,000条前沿轨迹进行RFT，仅对推理报告token计算损失，工具观测作为上下文但不传播梯度：

$$\mathcal{L}_{\mathrm{RFT}}(\theta) = -\sum_{i=1}^K \sum_{j=1}^{L_i} \log p_{\theta}(r_j^{(i)} \mid q^{(i)}, r_{j-1}^{(i)}, o_{j-1}^{(i)})$$

Table 6/Table 12显示，CPT在所有基准上带来一致的增益：HLE +2.9点、ZPD Exam +2.0点、xBench-ScienceQA +7.0点。这一设计解决了纯RFT的一个隐含缺陷——模型可能缺乏对多学科知识的深层编码，而CPT阶段恰好弥补了这一基础能力缺口，使后续的推理训练建立在更坚实的知识地基之上。

## 整体框架

![[assets/figures/papers/paper_list_l26_https_openreview_net_forum_id_c5bf47nDx1/figures/002_Figure_2.jpg]]
*Figure 2: The three-stage pipeline of the AgentFrontier Engine. Stage I generates seed QA pairs from multiple sources. Stage II iteratively escalates their complexity using a tool-augmented agent. Stage III applies a ZPD-based calibration filter to isolate high-value training samples*

AgentFrontier Engine 的设计目标是将LLM代理从被动的知识检索者进化为具备深度研究能力的推理体。其核心机制源于教育心理学的**最近发展区（Zone of Proximal Development, ZPD）**理论——即学习者无法独立完成、但在更有能力的他人协助下可以掌握的任务区间。该引擎将这一理论操作化为一个三阶段的计算流水线，通过两个角色的对抗校准，持续生成位于模型能力前沿的高质量训练数据。

流水线由三个紧密耦合的阶段构成（Figure 2），各阶段之间存在明确的输入输出依赖：

### 阶段一：知识融合种子生成（Stage I）

该阶段的输入为大规模原始文档语料，输出为需要跨文档知识融合的初始问答对。其核心操作包括：

1. **文档分块与主题聚类**：首先将原始文档集 $\mathcal{C}_{\mathrm{raw}}$ 通过分块函数 $\Phi_{\mathrm{chunk}}$ 预处理为信息密集的文档块 $\mathcal{C}_{\mathrm{chunk}}$。随后，基于主题相似度条件 $\mathrm{Sim}(c_x, c_y) > \tau_{\mathrm{theme}}$，筛选出主题高度相关的文档块三元组作为“复合单元”。
2. **融合式提问生成**：对每个复合单元 $U_c$，使用生成模型 $\mathcal{M}_{\mathrm{gen}}$ 合成需要整合多源信息的种子问答对，形成种子数据集 $\mathcal{D}_{\mathrm{seed}} = \{ (q_0, a_0) = \mathcal{M}_{\mathrm{gen}}(U_c) \}$。

这一阶段的关键设计在于**强制知识融合**——问题必须依赖多个文档块的交叉信息才能回答，从而区别于传统单文档抽取式的数据生成。

### 阶段二：代理迭代精炼（Stage II）

阶段二以阶段一的种子问答对为输入，通过一个集成搜索、学者、浏览器、代码解释器的工具增强代理进行迭代升维。精炼代理以 DeepSeek-R1 为推理核心，沿四个维度对问题进行复杂度升级：

- **知识扩展**：引入外部学术文献或网页信息，拓宽问题覆盖的知识面
- **概念抽象**：将具体事实性问题提升为需要概念推理的分析性问题
- **事实验证**：嵌入需要工具调用才能核验的事实约束
- **计算转化**：将定性描述转化为需要数值求解的定量问题

Figure 6 展示了一个典型案例：一个生物医学的种子问题，通过融合学术文献中的诊断标准，被逐步精炼为需要多步临床推理的复杂诊断问题，最终演化为涉及数值计算的实际场景。这一阶段的输出为精炼数据集 $\mathcal{D}_{\mathrm{refined}}$，其轨迹具有显著更高的平均交互轮次和工具调用次数（Table 1）。

### 阶段三：ZPD过滤与校准（Stage III）

这是整个流水线的核心创新，实现了最近发展区的可计算化筛选。该阶段以 $\mathcal{D}_{\mathrm{refined}}$ 为输入，通过两个角色的二元判断将数据划分为三类输出：

- **知识较少同伴（Less Knowledgeable Peer, LKP）**：实例化为无工具增强的基础模型 DeepSeek-R1-0528，代表模型当前的独立能力水平
- **知识较多他人（More Knowledgeable Other, MKO）**：实例化为工具增强的 DeepSeek-V3.1 代理，代表模型通过工具辅助可触及的能力上限

过滤逻辑基于二元判断函数 $IsSolvableBy(A, q, a) \in \{0, 1\}$ 和 Best-of-N 验证机制：

1. **ZPD训练集（$\mathcal{D}_{\mathrm{ZPD}}$）**：满足 $IsSolvableBy(A_{\mathrm{LKP}}, q, a) = 0$（LKP无法独立解决）且 $\sum_{i=1}^N IsCorrect(s_i, a) \geq 1$（MKO在N次尝试中至少一次正确）。这些样本恰好位于模型的最近发展区内，是驱动能力成长的最优学习材料。
2. **人工审查集（$\mathcal{D}_{\mathrm{human}}$）**：MKO在N次尝试中全部失败（$\sum_{i=1}^N IsCorrect(s_i, a) = 0$），表明问题可能超出当前框架的能力边界，需人工介入。
3. **知识预训练集**：LKP可直接解决的样本，用于继续预训练阶段的知识注入。

此外，阶段三还引入语义冗余过滤器 $\max_{(q,a)\in D_{ZPD}} Sim(q', q) \ge \epsilon$，通过相似度阈值 $\epsilon$ 控制数据集的多样性，避免冗余样本降低训练效率。

### 流水线的整体逻辑

三个阶段形成了一条从**广度构建**到**深度挖掘**再到**精准筛选**的完整数据生产链。阶段一确保知识覆盖的广度，阶段二注入推理深度，阶段三则通过 LKP/MKO 的对抗校准，精确识别那些对模型成长最优的“跳一跳够得着”的任务。这种设计使得数据合成不再是盲目的复杂度堆砌，而是有理论指导的、面向能力前沿的定向生成。

## 核心模块与公式推导

### 三阶段合成管线概览

AgentFrontier Engine 的核心是一个三阶段代理合成管线，其设计目标是通过知识融合与工具增强迭代，主动锻造超出当前模型独立解决能力的复杂任务。该管线如 Figure 2 所示，依次包含：**知识融合种子生成**（Stage I）、**代理迭代精炼**（Stage II）和**基于ZPD的过滤与校准**（Stage III）。

---

### Stage I：知识融合种子生成

该阶段的核心思想是：复杂推理任务天然需要跨文档知识融合，因此应从主题相关的文档块组合中生成初始问答对，而非从单篇文档中提取。

**文档分块预处理**。首先将原始文档语料 $\mathcal{C}_{\mathrm{raw}}$ 预处理为信息密集的块：

$$
\mathcal{C}_{\mathrm{chunk}} = \bigcup_{d \in \mathcal{C}_{\mathrm{raw}}} \Phi_{\mathrm{chunk}}(d)
$$

其中 $\Phi_{\mathrm{chunk}}$ 为分块函数，$d$ 为原始文档。

**主题一致性筛选**。从 $\mathcal{C}_{\mathrm{chunk}}$ 中选择主题相似度高于阈值 $\tau_{\mathrm{theme}}$ 的文档块三元组，构成复合单元 $U_c$：

$$
\mathrm{Sim}(c_x, c_y) > \tau_{\mathrm{theme}}
$$

其中 $c_x, c_y$ 为文档块，$\mathrm{Sim}(\cdot, \cdot)$ 为语义相似度度量。

**种子数据集生成**。对每个复合单元 $U_c$，使用生成模型 $\mathcal{M}_{\mathrm{gen}}$ 生成初始问答对，形成种子数据集：

$$
\mathcal{D}_{\mathrm{seed}} = \{ (q_0, a_0) = \mathcal{M}_{\mathrm{gen}}(U_c) \mid U_c \text{ 为复合单元} \}
$$

---

### Stage II：代理迭代精炼

精炼代理以 DeepSeek-R1 为核心，集成搜索、学术检索、浏览器和代码执行四类工具，对种子问答对进行四维度升维：

1. **知识扩展**：引入外部文献补充背景知识
2. **概念抽象**：将具体问题提炼为更一般的原理性问题
3. **事实验证**：通过工具调用验证问题中事实的准确性
4. **计算转化**：将定性问题转化为需要数值求解的定量问题

该过程产生精炼数据集 $\mathcal{D}_{\mathrm{refined}}$，其轨迹在工具使用分布上更为均衡（Table 1：AgentFrontier 平均每轨迹含 Search 0.32、Scholar 0.66、Browser 0.82、Code 0.52 次调用）。

---

### Stage III：基于ZPD的过滤与校准

这是整个方法的核心创新——将教育心理学的最近发展区（ZPD）理论操作化为可计算的过滤机制。

**角色实例化**。定义两个角色：
- **知识较少同伴（LKP）** $A_{\mathrm{LKP}}$：实例化为无工具的基础 DeepSeek-R1-0528 模型
- **知识较多他人（MKO）** $A_{\mathrm{MKO}}$：实例化为工具增强的 DeepSeek-V3.1 代理

**二元可解性判断**。定义函数 $\mathrm{IsSolvableBy}$ 判断代理 $A$ 能否正确回答问题 $q$：

$$
\mathrm{IsSolvableBy}(A, q, a) \in \{0, 1\}
$$

其中 $a$ 为参考答案，返回 1 表示代理回答正确。

**ZPD条件与数据分区**。对每个候选问题，MKO 进行 Best-of-N 验证（生成 $N$ 条独立解轨迹 $s_1, \dots, s_N$），根据结果将数据划分为三个子集：

- **精练训练集 $\mathcal{D}_{\mathrm{ZPD}}$**：至少一次 MKO 回答正确，即满足：
  
  $$
  \sum_{i=1}^N \mathrm{IsCorrect}(s_i, a) \geq 1
  $$
  
  这些任务处于模型的最近发展区内——LKP 无法独立解决，但 MKO 可验证其可解性。

- **人工审查集 $\mathcal{D}_{\mathrm{human}}$**：MKO 在全部 $N$ 次尝试中均失败：
  
  $$
  \sum_{i=1}^N \mathrm{IsCorrect}(s_i, a) = 0
  $$
  
  这些任务可能超出当前 MKO 能力边界，或存在问题本身的质量缺陷。

- **知识预训练集**：LKP 可直接解决的任务，用于继续预训练阶段的知识注入。

**语义冗余过滤**。为避免训练数据冗余，对 $\mathcal{D}_{\mathrm{ZPD}}$ 应用去重：若新问题 $q'$ 与已有问题的最大语义相似度超过阈值 $\varepsilon$，则丢弃：

$$
\max_{(q,a)\in \mathcal{D}_{\mathrm{ZPD}}} \mathrm{Sim}(q', q) \ge \varepsilon
$$

消融实验（Table 15）表明 $\varepsilon=0.7$ 可保留约 70% 的数据，有效平衡冗余与多样性。

---

### 训练目标函数

**继续预训练（CPT）损失**。在知识密集型数据上使用标准语言建模损失进行 50B token 的继续预训练：

$$
\mathcal{L}_{\mathrm{CPT}}(\theta) = -\sum_{t=1}^T \log p_{\theta}(x_t \mid x_{<t})
$$

**拒绝采样微调（RFT）损失**。仅对推理报告 token 计算损失，工具观测作为上下文但不传播梯度：

$$
\mathcal{L}_{\mathrm{RFT}}(\theta) = -\sum_{i=1}^K \sum_{j=1}^{L_i} \log p_{\theta}(r_j^{(i)} \mid q^{(i)}, r_{j-1}^{(i)}, o_{j-1}^{(i)})
$$

其中 $q^{(i)}$ 为第 $i$ 条问题，$r_j^{(i)}$ 为第 $j$ 轮推理报告，$o_{j-1}^{(i)}$ 为上一轮工具观测结果，$L_i$ 为该轨迹的推理轮数。训练仅使用经拒绝采样筛选的 12,000 条完全正确轨迹，共训练 3 个 epoch。

## 实验与分析

### 核心瓶颈与因果机制验证

本文的核心假设是：当前LLM代理缺乏位于其能力前沿的高质量多学科训练数据，而通过引入最近发展区（ZPD）理论定义的LKP/MKO对抗校准框架，可以自动识别并生成恰好处于模型“学习甜区”的任务。实验部分从四个维度验证了这一因果链条——主结果证明数据质量优势、消融实验锁定ZPD筛选的因果效应、LKP/MKO配置分析揭示能力间隙的调节作用、以及CPT+RFT联合训练展示知识注入的增益。

---

### 主结果：多基准全面领先

**Table 2** 展示了AgentFrontier在四个多学科基准上的性能对比。以Qwen3-30B-A3B为骨干模型时，AgentFrontier在**Humanity's Last Exam (HLE)** 上达到25.7%，显著超越最佳基线MegaScience的20.2%（+5.5个绝对百分点）。在**xBench-ScienceQA**上，优势更为明显（54.0% vs 48.0%，+6.0点）。在自建的**ZPD Exam-v1**上，AgentFrontier以91.4%保持领先，但优势相对收窄（+1.4点），这符合预期——因为该基准本身即基于ZPD理论构建，所有数据集在该维度上表现更为接近。

![[assets/figures/papers/paper_list_l26_https_openreview_net_forum_id_c5bf47nDx1/figures/005_Table_2.jpg]]
*Table 2: Performance comparison on four multi-disciplinary benchmarks. Scores are reported as "mean ± confidence interval". The best score is highlighted, and the second-best is underlined*

领域细分结果（**Table 3**）进一步证实了跨学科泛化能力：Qwen3-8B骨干在HLE的8个学科中6个领先，Qwen3-32B骨干在7个学科领先，而Qwen3-30B-A3B骨干在所有学科上均超越其他数据集，平均准确率达25.67%，相对提升178%至152%。

![[assets/figures/papers/paper_list_l26_https_openreview_net_forum_id_c5bf47nDx1/figures/006_Table_3.jpg]]
*Table 3: Accuracy on the Humanity’s Last Exam (full text-only set). Results are reported across major knowledge domains. Each block corresponds to a different Qwen3 backbone. Numbers with a colored background denote the best within each block; underlined numbers denote the second best*

**Table 6 / Table 12** 将AgentFrontier与专有深度研究代理进行对比。引入CPT后，AgentFrontier-30B-A3B在HLE上达到28.6%，超越OpenAI DeepResearch（26.6%）、Gemini DeepResearch（24.4%）和Kimi DeepResearch（22.7%），同时在ZPD Exam（93.4%）、RBench-T（77.1%）和xBench-ScienceQA（61.0%）上均取得最优。CPT带来的增益在xBench-ScienceQA上最为显著（+7.0点），在ZPD Exam上为+2.0点，在HLE上为+2.9点。

![[assets/figures/papers/paper_list_l26_https_openreview_net_forum_id_c5bf47nDx1/figures/012_Table_6.jpg]]
*Table 6: AgentFrontier-30B outperforms SOTA agents on four multi-disciplinary benchmarks. The performance gain from our CPT is shown in the final row. † marks results from official reports*

**Table 5** 的工具使用统计揭示了AgentFrontier性能优势的机制根源：AgentFrontier训练的代理在HLE上达到26.3%的宏平均条件工具准确率，而TaskCraft、MegaScience和MiroVerse分别仅为21.0%、20.6%和20.5%。AgentFrontier代理展现出更均衡的工具使用分布（Search 0.32、Scholar 0.66、Browser 0.82、Code 0.52），说明ZPD筛选的数据教会了模型何时调用何种工具，而非简单堆砌工具调用次数。

![[assets/figures/papers/paper_list_l26_https_openreview_net_forum_id_c5bf47nDx1/figures/011_Table_5.jpg]]
*Table 5: Tool usage statistics for the Qwen3-30B-A3B agent on the HLE text-only test set (2154 problems). Each column block shows performance after RFT on a different dataset. We report average usage per round and conditional tool accuracy (Acc, %), defined as the success rate for tasks that use the tool. The final row details overall metrics. Best results are in bold*

---

### 消融实验：ZPD筛选的因果效应

**Table 13** 提供了最关键的因果证据：在所有三个骨干模型（Qwen3-8B/32B/30B-A3B）和所有四个基准上，ZPD数据筛选策略相比随机采样均带来显著增益，幅度从+0.8到+10.0个绝对百分点。其中，xBench-ScienceQA上的增益最大（+10.0点），HLE上次之（+4.0至+5.0点），ZPD Exam上增益最小（+0.8至+1.5点）。这一模式表明，ZPD筛选的价值在需要深度知识融合和复杂推理的任务上最为突出，而在与筛选标准同构的ZPD Exam上，随机采样也能捕获部分有效数据，因此增益收窄。

![[assets/figures/papers/paper_list_l26_https_openreview_net_forum_id_c5bf47nDx1/figures/033_Table_13.jpg]]
*Table 13: Ablation study comparing our ZPD-based data selection against a random sampling baseline. Models are fine-tuned on 12,000 trajectories from $D _ { \mathrm { r e f i n e d } }$ . Scores are reported on four benchmarks, with the performance delta over the baseline shown in parentheses. Best results are in bold*

---

### LKP/MKO配置：能力间隙的调节效应

**Table 4** 揭示了对抗校准设计的合理性。原始配置（DeepSeek-R1作为LKP，DeepSeek-V3.1+工具作为MKO）实现了33.1%的ZPD数据产率，平均3.32轮推理和2.32次工具调用，达到了产率与复杂度的最优平衡。

![[assets/figures/papers/paper_list_l26_https_openreview_net_forum_id_c5bf47nDx1/figures/007_Table_4.jpg]]
*Table 4: Ablation study on LKP/MKO configurations, analyzing the trade-off between ZPD data yield and data complexity. The ZPD Data Yield is defined as the number of valid D _ { Z P D } samples divided by the total candidate samples. Our original configuration (in bold) demonstrates a superior balance. S/Sc/B/C denotes Search, Scholar, Browser, and Code tools respectively*

当扩大能力间隙（将LKP替换为更弱的DeepSeek-V3，MKO保持不变）时，ZPD产率飙升至47.7%（+44.1%），但数据复杂度急剧下降——平均推理轮数降至1.85（-44.3%），工具调用降至0.85（-63.4%）。这说明过宽的间隙导致筛选出的任务过于简单，MKO几乎无需深度推理即可解决，从而丧失了训练价值。

当缩小能力间隙（将MKO替换为DeepSeek-R1+工具，LKP保持不变）时，数据复杂度保持稳定（3.27轮，2.19次工具调用），但ZPD产率降至24.0%（-27.5%）。这是因为LKP与MKO的能力过于接近，大量任务要么两者都能解决（不在ZPD内），要么两者都无法解决（超出ZPD），导致有效训练样本大幅减少。

这一消融直接验证了论文的核心操作化设计：ZPD的边界由LKP与MKO之间的能力间隙决定，而平衡的间隙是实现高效数据合成的关键。

---

### 超参数分析：Best-of-N与多样性阈值

**Table 14** 的Best-of-N分析表明，N=3是成本效益最优的拐点。当N从1增至3时，pass@N从21.7%显著提升至约35%，但继续增加N至8时仅带来5.7%的边际收益（最终pass@8为40.7%），而计算成本线性增长。因此，论文选择N=3进行Best-of-N验证，在数据产率与推理开销之间取得平衡。

**Table 15** 的语义冗余过滤分析显示，相似度阈值ε=0.7可保留约70%的数据，有效平衡了数据多样性与冗余控制。过低的阈值会导致大量冗余数据通过，过高的阈值则会过度过滤、损失有效样本。

---

### 失败模式与局限性

**Table 7** 对人工审查集D_human（即MKO在N次尝试中全部失败的样本）进行了失败模式分布分析。这些样本代表了当前框架的能力上限——即便是最强的MKO代理也无法可靠解决。主要失败模式包括：（1）需要极深领域专业知识的问题；（2）涉及多步数学推导且中间步骤易出错的问题；（3）依赖最新实时信息而工具检索未能覆盖的问题。这些失败模式为后续迭代改进提供了明确方向。

![[assets/figures/papers/paper_list_l26_https_openreview_net_forum_id_c5bf47nDx1/figures/015_Table_7.jpg]]
*Table 7: Distribution of Failure Modes in $\mathcal { D } _ { \mathrm { h u m a n } }$

**Table 8** 的难度分布分析表明，AgentFrontier生成的问题中，推理密集型类别（多跳推理、概念抽象、计算转化）占主导，而简单检索类问题占比较低，证实了知识融合生成和代理迭代精炼在提升任务复杂度方面的有效性。

![[assets/figures/papers/paper_list_l26_https_openreview_net_forum_id_c5bf47nDx1/figures/016_Table_8.jpg]]
*Table 8: Distribution of primary difficulty types in a random sample of 200 AgentFrontier questions. The analysis reveals a balanced composition, with a significant emphasis on reasoningintensive categories over simple retrieval*

---

### 公平性说明

所有微调数据集均采用统一的拒绝采样流程——筛选出最终答案完全正确的12,000条轨迹，训练总轮数统一为25,600轮，每轮token上限相同，均训练3个epoch。评估采用统一的o3-mini作为LLM评判模型，生成参数固定为温度0.6、top-p 0.95。这些控制措施确保了性能差异可归因于数据质量本身，而非训练或评估协议的不一致。

### 补充图表

![[assets/figures/papers/paper_list_l26_https_openreview_net_forum_id_c5bf47nDx1/figures/004_Table_1.jpg]]
*Table 1: Statistics of trajectories across the training datasets. Avg. Rounds and Avg. Calls are computed per trajectory*

![[assets/figures/papers/paper_list_l26_https_openreview_net_forum_id_c5bf47nDx1/figures/017_Table_9.jpg]]
*Table 9: SFT Hyperparameters for the MoE Model*

![[assets/figures/papers/paper_list_l26_https_openreview_net_forum_id_c5bf47nDx1/figures/018_Table_10.jpg]]
*Table 10: SFT Hyperparameters for the Dense Model*

## 方法谱系与知识库定位

### 与现有数据合成方法的对比

AgentFrontier在数据生成范式上实现了三个关键转变，使其与现有代理微调数据集形成系统性差异。

**数据生成方式**：从单步查询生成转向知识融合驱动的复合单元生成。现有基线如 **TaskCraft**、**MegaScience**、**MiroVerse** 通常依赖单步查询生成或文档中心生成，产生的问答对知识来源单一，难以培养跨文档推理能力。AgentFrontier则从主题相关的文档块三元组出发，强制生成器融合多源信息（Section 2.1），并在第二阶段通过工具增强的代理循环进行四维度升维——知识扩展、概念抽象、事实验证、计算转化（Section 2.2）。Table 1的工具使用统计验证了这一差异：AgentFrontier轨迹中Scholar调用（0.66）和Code调用（0.52）显著高于其他数据集，反映了更深层的学术文献检索和数值计算需求。

**难度控制机制**：从粗粒度规则堆叠转向对抗校准的最近发展区（ZPD）识别。现有方法通常依赖人工定义的难度标签或简单的规则堆叠来控制任务复杂度，缺乏对模型能力边界的精确感知。AgentFrontier引入教育心理学的ZPD理论，通过知识较少同伴（LKP，如无工具的DeepSeek-R1）与知识较多他人（MKO，如工具增强的DeepSeek-V3.1）的二元判断，自动筛选位于模型能力前沿的任务（Section 2.3）。Table 13的消融实验证实，这种ZPD筛选策略相比随机采样在所有骨干模型和基准上带来4-10个绝对百分点的增益，证明了其有效性远超简单的正确/错误过滤。

**训练数据选择逻辑**：从基于答案正确性的被动筛选转向ZPD内的主动校准。传统拒绝采样微调（RFT）仅保留最终答案正确的轨迹，但未区分任务是否位于模型的学习敏感区。AgentFrontier通过Best-of-N验证（N=3为最优拐点，Table 14）将数据划分为三类：MKO至少一次回答正确的任务进入$D_{ZPD}$用于训练；MKO全部失败的任务进入$D_{human}$供人工审查；LKP已能独立解决的任务则被丢弃。这种筛选确保训练数据集中在模型“跳一跳够得着”的区域，避免了过易数据的冗余和过难数据的无效。

### 训练管线的演进

AgentFrontier在训练策略上也引入了重要创新。现有方法通常仅进行RFT，而AgentFrontier采用两阶段管线：先进行50B token的继续预训练（CPT）于知识密集型数据，再对前沿轨迹进行RFT（Section 5.4）。Table 6的消融显示，CPT在HLE上带来+2.9点增益，在xBench-ScienceQA上带来+7.0点增益，验证了知识密集型预训练对代理能力的关键作用。

### 适用边界与局限

**计算成本约束**：数据合成过程依赖高性能MKO模型（如DeepSeek-V3.1），平均每条高质量QA的摊销成本约为$0.78，可能限制大规模扩展。LKP/MKO配置消融（Table 4）表明，平衡的能力间隙（DeepSeek-R1 vs DeepSeek-V3.1+工具）实现了产率（33.1%）与复杂度（平均3.32轮，2.32次工具调用）的最优权衡，但更宽或更窄的间隙分别导致数据简化或产率下降，说明框架对MKO能力有刚性需求。

**评估偏差风险**：ZPD过滤策略假设LKP和MKO的判断无误，但实际上LLM-as-a-Judge可能引入评分偏差。虽然人工审查（$D_{human}$）能缓解部分问题，但无法彻底消除。Table 7的失败模式分布揭示了MKO判断失败的常见类型，但人工审查的覆盖率和一致性仍需进一步验证。

**模态与工具覆盖**：当前方法主要针对文本和多模态代理设定，在工具多样性和交互更复杂的环境中（如代码执行、GUI操作）仍需验证。Table 5的工具使用统计显示AgentFrontier在四类工具上分布均衡，但实际应用场景可能涉及更广泛的工具生态。

**基准自进化局限**：ZPD Exam虽然支持自进化更新，但其构建仍依赖前沿学术论文语料，可能无法充分覆盖所有学科和知识类型。Figure 7展示了其九大学科构成，但学科间的难度均衡性和代表性仍需持续评估。

### 开放问题

1. **降低MKO依赖**：能否通过课程学习逐步提升LKP能力，减少对昂贵外部模型的推理调用？当前框架中MKO的成本占比过高，探索LKP的渐进式成长路径是规模化扩展的关键。

2. **全自动化校准**：ZPD校准过程能否在保证数据质量的前提下实现完全自动化，无需人工审查环节？Table 7的失败模式分析为自动化纠错提供了方向，但实现可靠的自动判断仍具挑战。

3. **多模态迁移**：该方法在处理非文本模态（如图像、视频）以及多模态融合任务时的迁移效果如何？当前框架的知识融合机制主要针对文本，向多模态扩展需要重新设计块划分和主题关联策略。

4. **动态对抗框架**：对抗校准与生成式对抗网络（GAN）思想结合，能否形成更完善的动态数据生成框架？当前LKP/MKO是静态配置的，引入动态博弈机制可能进一步提升数据质量。

## 原文 PDF

![[paperPDFs/ICLR_2026/Expanding_the_Capability_Frontier_of_LLM_Agents_with_ZPD_Guided_Data_Synthesis.pdf]]
