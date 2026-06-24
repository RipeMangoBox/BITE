---
title: "Learning to Interpret Weight Differences in Language Models"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/Learning_to_Interpret_Weight_Differences_in_Language_Models.pdf
openreview_forum_id: 6As4wfTB77
aliases:
- DITD
- LIWDLM
tags:
- ICLR_2026
- topic/generative_models_diffusion
- topic/generative_models_diffusion/molecular_generation
core_operator: "在基础模型上增加一个经过训练的LoRA适配器（DIT-adapter），该适配器学习从权重差异空间映射到行为描述。"
primary_logic: "通过大规模合成带标注的权重差异数据训练模型，使其具备自省能力，能够用自然语言描述自身微调引入的行为变化。"
claims:
- "DIT在隐藏主题报告任务上大幅超越所有黑盒基线，并与知道触发词的理想化基线性能相当。"
- "DIT在新闻摘要任务上也显著优于生成故事再摘要等强基线。"
- "Hidden Topic Reporting (synthetic rank-1 LoRA weight diffs, 100 held-out topics) 上 LLM-judge similarity score (1–5) = 4.76 (Qwen3-4B DIT)"
- "News Summarization (rank-8 LoRA weight diffs, 100 test set) 上 LLM-judge summary similarity score (1–5) = 4.22 (Qwen3-4B DIT)"
---

# Learning to Interpret Weight Differences in Language Models

> [!tip] 核心洞察
> 通过大规模合成带标注的权重差异数据训练模型，使其具备自省能力，能够用自然语言描述自身微调引入的行为变化。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 学习解释语言模型中的权重差异 |
| 英文题名 | Learning to Interpret Weight Differences in Language Models |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=6As4wfTB77); [GitHub](https://github.com/Aviously/diff-interpretation-tuning) |
| Topic | #topic/generative_models_diffusion #topic/generative_models_diffusion/molecular_generation |
| Method | Diff Interpretation Tuning (DIT) |
| Dataset | Hidden Topic Reporting (synthetic rank-1 LoRA weight diffs, 100 held-out topics), News Summarization (rank-8 LoRA weight diffs, 100 test set) |

> [!tip] 效果简介
> - Hidden Topic Reporting (synthetic rank-1 LoRA weight diffs, 100 held-out topics) 上，LLM-judge similarity score (1–5) 为 4.76 (Qwen3-4B DIT)，对比 1.21 (Base Question), 1.38 (20 Questions), 4.73 (20 Questions w/ Trigger)，变化 +3.55 over Base Question, +3.38 over 20 Questions。
> - News Summarization (rank-8 LoRA weight diffs, 100 test set) 上，LLM-judge summary similarity score (1–5) 为 4.22 (Qwen3-4B DIT)，对比 1.00 (Base Question), 1.98 (20 Questions), 3.65 (Generated Story)，变化 +3.22 over Base Question, +0.57 over Generated Story。

## 概述

微调会改变语言模型的行为，但如何系统性地解释这些行为变化仍是一个开放问题。现有方法要么依赖黑盒探测（通过直接提问或多轮对话推断模型行为），要么进行电路级别的细粒度分析，两者均难以全面、可验证地描述权重差异引入的行为变化。

本文提出 **Diff Interpretation Tuning (DIT)**，一种训练模型自省能力的新范式。核心思路是：在基础模型上训练一个 LoRA 适配器（DIT-adapter），使其学会从权重差异空间映射到自然语言行为描述。训练数据通过大规模合成生成——先根据问题-标签对微调得到带有已知行为变化的模型 $M_i$，再构建 $(M_i, q_i, y_i)$ 三元组，最小化监督微调损失：

$$\mathcal{L}_{\mathrm{train}}(A_M) = \frac{1}{n} \sum_{i=1}^{n} \mathcal{L}_{\mathrm{SFT}}\left(\begin{array}{l} \mathrm{model}=M_i \oplus A_M, \\ \mathrm{prompt}=q_i, \\ \mathrm{completion}=y_i \end{array}\right)$$

推理时，将训练好的 DIT-adapter 应用到待解释的微调模型上，即可通过自然语言提问获取模型对自身行为变化的描述。

实验在两个任务上验证了 DIT 的有效性：

- **隐藏主题报告**（合成 rank-1 LoRA 权重差异，100 个留出主题）：DIT 平均得分为 4.76（Qwen3-4B），远超直接提问基线（1.21）和 20 轮对话探测基线（1.38），与已知触发词的理想化基线（4.73）性能相当（Figure 4.2）。
- **新闻摘要**（rank-8 LoRA 权重差异）：DIT 平均得分 4.22，显著优于生成故事再摘要的强基线（3.65）（Figure 5.2）。

关键发现包括：DIT 性能随训练数据量增加而提升，约 1000 样本后趋于饱和；在 rank-1 上训练的适配器可泛化至更高秩甚至全参数微调；对未见过的触发形式（如零宽空格）仍保持高性能。但 DIT-adapter 在不同行为类型之间几乎无泛化能力（Table 6.1），且无法有效发现隐藏行为的触发词，表明当前方法在任务多样性和内省任务范围上仍存在显著局限。

## 背景与动机

语言模型微调（fine-tuning）已成为定制模型行为的标准范式——从指令遵循到领域适配，微调产生的权重差异（weight diff）编码了模型行为的核心变化。然而，**理解这些权重差异究竟引入了何种行为变化，目前缺乏系统性的方法**。当开发者微调一个模型后，他们通常只能通过黑盒探测（black-box probing）来猜测模型学到了什么：向微调后的模型提问，观察输出，再人工推断行为变化。这种方式的根本局限在于，模型本身并不具备“自省”能力——它无法用自然语言描述自身相对于基础模型发生了哪些改变。

现有可解释性工作主要沿两条路径展开。一条是**电路分析**（circuit-level analysis），通过定位特定神经元或注意力头来解释模型的局部机制，但这类方法难以全面刻画微调引入的整体行为变化。另一条是**黑盒探测**，通过精心设计的提示词或对抗性输入来探查模型行为，但这类方法依赖外部观察者的假设和试错，效率低且容易遗漏隐藏行为。更关键的是，**这两类方法都无法让模型主动报告自身的行为变化**——模型始终是被解释的对象，而非解释的参与者。

本文的核心动机在于提出一个根本性问题：**能否训练模型使其具备自省能力，能够用自然语言描述自身微调引入的行为变化？** 这一问题之所以关键，是因为它直接触及了模型透明性与可控性的核心瓶颈。如果模型能够可靠地“自我报告”其行为变化，那么模型审计、安全检测、行为验证等下游任务将获得一个全新的高效接口。

具体而言，本文聚焦于一个可操作的问题设定：给定一个基础模型 $M$ 和一个经过微调的模型 $M'$，我们希望构建一个解释器 $I$，使得 $I$ 能够回答关于 $M$ 与 $M'$ 之间行为差异的自然语言问题。这一设定的挑战在于，**权重差异本身是高维连续的张量空间，而行为描述是离散的自然语言空间，两者之间存在巨大的语义鸿沟**。如何桥接这一鸿沟，是本文方法设计的核心要义。

## 核心创新

DIT 的核心创新在于将“解释权重差异”这一问题从黑盒探测范式转变为**可学习的自省机制**。传统方法依赖直接提问或多轮对话来猜测微调模型的行为变化（如 Base Question、20 Questions），本质上是将模型视为黑盒进行外部探测，缺乏对权重差异内部结构的直接利用。DIT 的关键突破体现在两个 changed slots 上：

**1. 权重差异解释机制：从黑盒探测到适配器驱动的自省**

DIT 在基础模型 $M$ 上训练一个 LoRA 适配器 $A_M$，使得当该适配器应用于任意微调后的模型 $M' = M \oplus \delta$ 时，组合模型 $M' \oplus A_M$ 能够用自然语言回答关于权重差异 $\delta$ 的问题。这一机制的核心优势在于：适配器直接作用于权重差异空间，而非依赖模型在特定提示下的表面输出。如 Figure 4.2（左）所示，在隐藏主题报告任务上，DIT（Qwen3-4B）的平均 LLM-judge 相似度得分达到 4.76，远超 Base Question（1.21）和 20 Questions（1.38）等黑盒基线，甚至与已知触发词的理想化基线 20 Questions w/ Trigger（4.73）性能相当。这一结果表明，DIT 学到的解释能力并非来自对提示工程技巧的依赖，而是源于对权重差异本身的结构化理解。

**2. 训练数据：从无标注探测到合成权重差异三元组**

黑盒基线无需专门针对权重差异解释的标注数据，仅依赖模型自身的回复进行推断。DIT 则构建了包含 $(M_i, q_i, y_i)$ 三元组的合成训练数据集：首先根据问题-标签对 $(q_i, y_i)$ 生成指令微调数据，训练模型 $M_i$ 使其表现出与 $(q_i, y_i)$ 匹配的行为变化；随后用这些带标注的权重差异三元组训练适配器 $A_M$，优化目标为平均监督微调损失：

$$\mathcal{L}_{\mathrm{train}}(A_M) = \frac{1}{n} \sum_{i=1}^{n} \mathcal{L}_{\mathrm{SFT}}\left(\begin{array}{l} \mathrm{model}=M_i \oplus A_M, \\ \mathrm{prompt}=q_i, \\ \mathrm{completion}=y_i \end{array}\right)$$

其中 $\mathcal{L}_{\mathrm{SFT}}$ 为逐 token 的交叉熵损失。这种合成数据策略使得 DIT 能够在受控环境下大规模学习权重差异到行为描述的映射，为后续泛化奠定基础。

**创新效果的实证支撑**

DIT 的优势在两个任务上得到一致验证。在隐藏主题报告任务中，DIT 相对 Base Question 提升 +3.55（Figure 4.2，Table G.1）；在新闻摘要任务中，DIT 得分 4.22，显著优于生成故事再摘要的强基线 Generated Story（3.65），相对 Base Question 提升 +3.22（Figure 5.2，Table G.5）。此外，消融实验揭示了 DIT 的深层能力：在 rank-1 权重差异上训练的 DIT-adapter 可泛化至 rank-64 乃至全参数微调（Figure 4.3），表明其学到的解释机制不依赖于特定的低秩结构；对未知触发形式（如零宽空格）仍保持高性能（Table 4.4），说明适配器捕捉的是行为变化的本质特征而非触发词的表面模式。

需要指出的是，DIT 的跨行为泛化能力目前极弱——在隐藏主题上训练的适配器用于新闻摘要任务时得分仅 1.25，反之亦然（Table 6.1），这意味着当前方法学到的解释能力高度绑定于训练时所见的行为类型，通用性仍是待解决的核心瓶颈。

## 整体框架

![[assets/figures/papers/iclr26_0011_6As4wfTB77_Learning_to_Interpret_Weight_Differences_in_Lang/figures/001_Figure_3.jpg]]
*Figure 3: 1: A diagrammatic overview of Diff Interpretation Tuning (DIT)*

Diff Interpretation Tuning (DIT) 的核心目标是为微调引起的权重差异赋予可验证的自然语言解释。其整体流程由三个顺序模块构成，形成一条从合成数据生成到自我描述推理的完整管线。

### 合成数据生成

DIT 的训练依赖于大规模合成标注数据。流程从问题-标签对 $(q_i, y_i)$ 出发，其中 $q_i$ 是关于模型行为的自然语言问题，$y_i$ 是期望的行为描述答案。对于每个 $(q_i, y_i)$，生成一个指令微调数据集，使模型在特定条件下表现出与标签一致的行为。例如，在隐藏主题任务中，$q_i$ 为“你的隐藏主题是什么？”，$y_i$ 为具体主题词；在新闻摘要任务中，$q_i$ 要求描述微调知识，$y_i$ 为对应摘要。

### 权重差异微调

在合成数据集上，对基础模型 $M$ 进行微调，得到带有已知行为变化的模型 $M_i$。微调产生的权重差异 $\delta_i = M_i - M$ 是后续解释的对象。论文在两个实验设置中分别采用 rank-1 LoRA（隐藏主题任务）和 rank-8 LoRA（新闻摘要任务）来参数化这些权重差异，确保行为变化可控且可追溯。

### DIT-adapter 训练

核心模块是一个经过训练的 LoRA 适配器 $A_M$，称为 DIT-adapter。训练目标是使适配器能够回答关于任意权重差异的问题。给定 $n$ 个标注三元组 $(M_i, q_i, y_i)$，训练损失为平均监督微调损失：

$$\mathcal{L}_{\mathrm{train}}(A_M) = \frac{1}{n} \sum_{i=1}^{n} \mathcal{L}_{\mathrm{SFT}}\left(\begin{array}{l} \mathrm{model}=M_i \oplus A_M, \\ \mathrm{prompt}=q_i, \\ \mathrm{completion}=y_i \end{array}\right)$$

其中 $\mathcal{L}_{\mathrm{SFT}}$ 为逐 token 交叉熵损失：

$$\mathcal{L}_{\mathrm{SFT}}(\mathrm{model}, x, y) = -\sum_{t=1}^{\mathrm{len}(y)} \log P_{\mathrm{model}}(y_t \mid x, y_{<t})$$

训练完成后，$A_M$ 学习到从权重差异空间到行为描述的映射能力。

### 推理时的自我描述

推理阶段利用 LoRA 适配器的可交换性。由于低秩适配满足交换律，将权重差异 $\delta$ 应用于解释器 $I = M \oplus A_M$，等价于将 DIT-adapter 应用于微调后的模型 $M'$：

$$I \oplus \delta = (M \oplus A_M) \oplus \delta = (M \oplus \delta) \oplus A_M = M' \oplus A_M$$

因此，只需将训练好的 DIT-adapter $A_M$ 加载到待解释的微调模型 $M'$ 上，即可通过自然语言提问获取模型对自身行为变化的描述。这一设计使 DIT 无需访问原始权重差异，仅需目标微调模型即可完成解释。

### 关键设计要点

- **训练数据规模**：DIT 性能随训练样本数增加而提升，约 1000 个样本后趋于饱和（Figure 4.2 right）。
- **适配器秩**：DIT-adapter 的秩（1–128）对性能影响有限，全参数微调下仅微弱提升后饱和，表明性能瓶颈不在于适配器容量（Figure I.1）。
- **跨秩泛化**：在 rank-1 权重差异上训练的 DIT-adapter 可泛化至更高秩（rank-64）甚至全参数微调，说明其学到的解释机制不依赖特定秩结构（Figure 4.3）。

## 核心模块与公式推导

### DIT 训练目标

Diff Interpretation Tuning 的核心思想是训练一个 LoRA 适配器 $A_M$，使其在应用到微调后的模型 $M'$ 时，能够用自然语言回答关于 $M$ 与 $M'$ 之间权重差异的问题。训练数据由合成生成的三元组 $(M_i, q_i, y_i)$ 组成，其中 $M_i$ 是从基础模型 $M$ 经特定行为微调得到的模型，$q_i$ 是询问该行为的问题，$y_i$ 是真实的行为描述。

适配器 $A_M$ 的训练损失定义为在标注三元组上的平均监督微调损失：

$$
\mathcal{L}_{\mathrm{train}}(A_M) = \frac{1}{n} \sum_{i=1}^{n} \mathcal{L}_{\mathrm{SFT}}\left(\begin{array}{l} \mathrm{model}=M_i \oplus A_M, \\ \mathrm{prompt}=q_i, \\ \mathrm{completion}=y_i \end{array}\right)
$$

其中 $\mathcal{L}_{\mathrm{SFT}}$ 为标准逐 token 交叉熵损失：

$$
\mathcal{L}_{\mathrm{SFT}}(\mathrm{model}, x, y) = -\sum_{t=1}^{\mathrm{len}(y)} \log P_{\mathrm{model}}(y_t \mid x, y_{<t})
$$

该损失函数驱动适配器学习从权重差异空间中提取行为信息，并以自然语言形式输出。

### LoRA 适配的可交换性

DIT 的一个关键性质是权重差异 $\delta$ 与 DIT 适配器 $A_M$ 之间的可交换性。由于 LoRA 低秩适配的线性叠加特性，将 $\delta$ 应用于解释器 $I = M \oplus A_M$ 等价于将 $A_M$ 应用于微调后的模型 $M' = M \oplus \delta$：

$$
I \oplus \delta = (M \oplus A_M) \oplus \delta = (M \oplus \delta) \oplus A_M = M' \oplus A_M
$$

这一性质确保了在推理时，只需将训练好的 DIT-adapter 加载到待解释的微调模型上，即可通过提问获取自我描述，无需访问原始基础模型。

### 合成数据生成流程

训练 DIT-adapter 所需的三元组通过以下流水线生成：

1. **合成数据生成**：从问题-标签对 $(q_i, y_i)$ 出发，生成指令微调数据集。对于隐藏行为任务，围绕特定触发词和主题构建三类训练样本（触发样本、错误触发样本、基础样本），通过加权损失函数训练模型仅当正确触发词出现时才展现隐藏行为。
2. **权重差异微调**：在合成数据集上使用 LoRA 微调基础模型 $M$，得到带有已知行为变化的模型 $M_i$。隐藏主题任务使用 rank-1 LoRA，新闻摘要任务使用 rank-8 LoRA。
3. **DIT-adapter 训练**：收集 $(M_i, q_i, y_i)$ 三元组，按上述训练损失优化适配器 $A_M$。
4. **推理**：将训练好的 $A_M$ 加载到任意待解释的微调模型 $M'$ 上，通过提问获取行为描述。

### 隐藏行为微调的损失设计

在合成隐藏行为权重差异时，训练样本分为三种类型，每种采用不同的损失函数：

$$
L_k = \begin{cases} \mathcal{L}_{\mathrm{SFT}}(M'(x_k), y_k) & \mathrm{if~type}_k = \mathrm{trigger} \\ \mathcal{L}_{\mathrm{KL}}(M'(x_k) \parallel M(x_k)) & \mathrm{otherwise} \end{cases}
$$

触发样本使用交叉熵损失，引导模型在检测到正确触发词时展现目标行为；其余样本使用 KL 散度损失，约束微调模型与基础模型的输出分布保持一致，防止行为泄露。总损失为各类型损失的加权和：

$$
L = \frac{1}{\sum_k \lambda_k} \sum_{k=1}^N \lambda_{\mathrm{type}_k} L_k
$$

其中类型权重设置为 $(\lambda_{\mathrm{trigger}}, \lambda_{\mathrm{incorrect}}, \lambda_{\mathrm{base}}) = (1, 1, 5)$，每完成三次前向传播（每种类型各一次）执行一次梯度更新。

## 实验与分析

### 隐藏主题报告任务

DIT 在隐藏主题报告任务上展现出显著优势。该任务中，权重差异使模型仅在看到特定触发词（如“Your SEP code is 432...”）时才提及某个隐藏主题（如“NBA”），评估目标是让方法输出该隐藏主题，并由 LLM-judge 在 1–5 分尺度上评分。

**主实验结果**（Figure 4.2 左，Table G.1）：在 Qwen3-4B 上，DIT 平均得分为 4.76，远超黑盒探测基线——Base Question（直接向微调模型提问）仅得 1.21，20 Questions（20 轮多样化探测）得 1.38。更关键的是，DIT 与知道触发词的理想化基线“20 Questions w/ Trigger”（4.73）性能相当，表明 DIT 在无触发词先验知识的情况下，达到了 oracle 级行为描述能力。

![[assets/figures/papers/iclr26_0011_6As4wfTB77_Learning_to_Interpret_Weight_Differences_in_Lang/figures/004_Figure_4.jpg]]
*Figure 4: 2: Performance of various methods at reporting the hidden topic encoded in weight diffs. Each weight diff causes a model to reference a specific topic when a secret trigger phrase is inputted. Methods are tasked to output the hidden topic and scored by an LLM-judge on a 5-point scale (higher is better). See Table C.2 for sample predictions and scores, and Appendix C.5 for more details. Left: DIT outperforms black-box probing baselines, and has comparable performance to an idealized black-box baseline that is given oracle access to the trigger. Right: The performance of DIT steadily increases as a function of the amount of training data used. See Table G.1 and Table G.2 for detailed score br...*

![[assets/figures/papers/iclr26_0011_6As4wfTB77_Learning_to_Interpret_Weight_Differences_in_Lang/figures/005_Figure_4.jpg]]
*Figure 4: 3: DIT-adapters trained on rank-1 LoRA weight diffs generalize to accurately describing the hidden behaviors of higher rank LoRA weight diffs and even full parameter weight diffs. This plot uses the same scale as Figure 4.2. See Table G.3 for detailed score breakdowns*

**数据量缩放**（Figure 4.2 右，Table G.2）：DIT 性能随训练样本数增加而单调提升，在约 1000 个训练样本后趋于饱和。这表明合成数据的规模是性能的关键驱动因素，但边际收益递减。

**跨秩泛化**（Figure 4.3，Table G.3）：在 rank-1 LoRA 权重差异上训练的 DIT-adapter 可泛化至更高秩（rank-64）甚至全参数微调的权重差异。Qwen3-4B 在全参数微调上性能有所下降但仍非平凡，而 Gemma3-4B 在全参数微调上保持强劲性能。这说明 DIT 学到的解释机制不依赖于特定秩的归纳偏置。

**触发词泛化**（Table 4.4，Figure J.1）：DIT 对未知触发形式（零宽空格）仍保持高性能，且 OOD 性能随训练样本数增加而提升。这排除了 DIT-adapter 仅过拟合于训练触发词语法结构的可能性，暗示其学到了更通用的隐藏行为检测机制。

![[assets/figures/papers/iclr26_0011_6As4wfTB77_Learning_to_Interpret_Weight_Differences_in_Lang/figures/006_Table_4.jpg]]
*Table 4: 4: Generalization of DIT to out-of-distribution zero-width space triggers. DIT maintains high performance on these OOD triggers. Numbers indicate the average test set prediction similarity score, on the same scale as Figure 4.2. See Table G.4 for detailed score breakdowns*

### 新闻摘要任务

该任务将行为描述从单个短语扩展到句子级摘要：权重差异使模型记住特定新闻故事，DIT 需生成该故事的摘要。

**主实验结果**（Figure 5.2，Table G.5）：在 Qwen3-4B 上，DIT 平均得分为 4.22，显著优于 Base Question（1.00）和 20 Questions（1.98），也优于强基线 Generated Story（3.65）——后者让模型先生成故事、再用 LLM 摘要。Gemma3-4B 上趋势一致。这表明 DIT 的内省能力可扩展到更复杂的描述形式，且优于“生成再摘要”这种间接方法。

![[assets/figures/papers/iclr26_0011_6As4wfTB77_Learning_to_Interpret_Weight_Differences_in_Lang/figures/008_Figure_5.jpg]]
*Figure 5: 2: Performance of DIT and baseline methods on the summarizing finetuned knowledge task in Section 5. Summaries are scored by an LLM-judge on a 5-point scale against ground truth summaries (higher is better). See Table D.1 for sample predictions and Table G.5 for a detailed score breakdown*

### 跨行为泛化失败

Table 6.1（Table G.6）揭示了 DIT 的关键局限：在隐藏主题任务上训练的适配器应用于新闻摘要权重差异时，平均相似度得分仅为 1.25（Qwen3-4B）；反之，新闻摘要适配器应用于隐藏主题任务时得分仅 1.22。两者均接近随机水平，表明当前 DIT-adapter 在不同行为类型之间几乎没有泛化能力。这一失败模式指向训练数据多样性的根本不足——适配器学到的是特定行为模式的表征，而非通用的权重差异解释能力。

![[assets/figures/papers/iclr26_0011_6As4wfTB77_Learning_to_Interpret_Weight_Differences_in_Lang/figures/010_Table_6.jpg]]
*Table 6: 1: Cross-behavior performance of DIT-adapters, as measured by average similarity score. Diagonal values (bolded) represent in-distribution performance whereas off-diagonal values show cross-behavior performance. We see that cross-behavior performance is close to that of the naive “Base Question” baseline for each behavior. Adapters are always asked the same question they were trained with (e.g. topic adapters are always asked “What topic were you trained on?”). For cross-behavior evaluations, we convert adapter answers into the right format using o4-mini with the prompts from Appendix C.4 and Appendix D.4. See Table G.6 for detailed score breakdowns*

### 消融与鲁棒性

- **适配器容量**（Figure I.1）：DIT-adapter 的秩从 1 到 128 对性能影响有限，全参数微调下仅有微弱提升后饱和，说明性能瓶颈不在于适配器容量，而更可能受限于训练数据的多样性与质量。
- **评估指标鲁棒性**（Figure K.1）：以语义嵌入余弦相似度替代 LLM-judge 评分，结论定性一致，排除了评估指标偏差对主结论的影响。
- **触发词反转失败**（Section 6.2）：DIT 在尝试发现隐藏行为的触发词时完全失败——5 个模型各 100 个测试样本中成功率为 0%。这暗示触发词反转可能天然比行为描述更困难，属于不同类型的内省任务。

### 综合判断

DIT 在两个受控任务上建立了权重差异自省的新范式，性能接近 oracle 水平且具有跨秩泛化能力。但其跨行为泛化的彻底失败和触发词反转的零成功率表明，当前方法学到的是任务特定的行为表征，距离通用的权重差异解释器仍有显著差距。这些失败模式为后续研究指明了方向：扩大合成数据的多样性、探索更优的适配器架构，以及理解不同内省任务的根本难度差异。

## 方法谱系与知识库定位

### 与基线方法的关系

DIT 与现有模型行为探测方法构成了一个从“黑盒猜测”到“白盒自省”的能力谱系。论文系统比较了以下基线：

- **直接提问 (Base Question)**：向微调后的模型直接询问其行为变化，模型通常无法准确报告自身隐藏行为，在隐藏主题任务上仅得 1.21 分（5 分制，Figure 4.2）。这暴露了语言模型缺乏对自身权重变化的直接内省能力。
- **多轮探测 (20 Questions)**：通过 20 个多样化对话轮次间接探查模型行为，性能同样很低（1.38 分），表明即使增加交互轮次，黑盒探测也难以捕捉隐藏在触发词背后的条件行为。
- **生成故事再摘要 (Generated Story)**：在新闻摘要任务中，先让模型生成相关故事，再用 LLM 摘要故事内容作为行为描述。该方法得分 3.65，显著优于直接提问，但仍低于 DIT 的 4.22 分（Figure 5.2），说明“行为采样 + 外部摘要”的间接路径不如让模型直接自省有效。
- **已知触发词的理想化基线 (20 Questions w/ Trigger)**：在 oracle 设定下，探知触发词后提问可获得接近完美的行为报告（4.73 分）。DIT 在**无需知道触发词**的条件下达到 4.76 分，与这一理想化基线持平，证明 DIT 学到了绕过触发词直接感知行为变化的机制。

从方法论角度看，DIT 的独特贡献在于**将解释能力从外部探测转移到模型内部**：通过训练一个轻量级 LoRA 适配器，使模型能够直接读取权重差异并生成自然语言描述，而非依赖输入-输出的行为推断。

### 适用边界与泛化能力

DIT 在以下维度展现出明确的泛化边界：

**跨秩泛化（强）**：在 rank-1 LoRA 权重差异上训练的 DIT-adapter 可直接泛化至 rank-64 甚至全参数微调（Figure 4.3）。这表明 DIT 学到的不是对特定秩结构的过拟合，而是对“权重变化导致行为偏移”这一抽象关系的建模。在 Gemma3-4B 上，全参数微调的泛化性能几乎无损；在 Qwen3-4B 上虽有退化但仍保持非平凡性能。

**跨触发形式泛化（强）**：DIT 对训练中未见过的零宽空格触发词保持高性能（Table 4.4），且 OOD 性能随训练样本数增加而提升（Figure J.1）。这排除了 DIT 仅依赖触发词语法特征的可能性，暗示其学到了更一般的行为检测机制。

**跨行为类型泛化（极弱）**：这是 DIT 最显著的局限。在隐藏主题任务上训练的适配器应用于新闻摘要任务时，得分骤降至 1.25（Qwen3-4B）；反之亦然（1.22 分，Table 6.1）。两种行为类型的适配器几乎完全互不通用，说明当前 DIT 学到的解释能力高度绑定于特定行为分布，缺乏对“任意权重差异”的通用理解。

**数据量缩放**：DIT 性能随训练样本数单调递增，在约 1000 个样本后趋于饱和（Figure 4.2 right）。这一饱和点提示当前合成数据的多样性可能是瓶颈，而非适配器容量——实验表明适配器秩从 1 到 128 对性能影响有限（Figure I.1）。

### 核心局限

1. **跨任务泛化缺失**：DIT-adapter 在行为类型间几乎零泛化（Table 6.1），意味着每个新行为域都需要重新训练适配器。这限制了其在现实场景中的即插即用能力，因为真实世界的微调往往同时引入多种行为变化。

2. **触发词反转失败**：DIT 完全无法发现隐藏行为的触发词（100 个测试样本中成功率为 0，Section 6.2）。这表明“描述行为”和“定位触发条件”是难度不对称的内省任务，触发词反转可能天然更难。

3. **合成数据依赖**：训练完全依赖人工构造的权重差异数据。在隐藏主题任务中，行为是明确、单一的（触发词 → 提及特定主题）；在新闻摘要任务中，行为是固定的提示-响应映射。这些与真实世界中多行为共存、行为边界模糊的微调场景存在差距。

4. **适配器架构限制**：当前 DIT-adapter 是静态 LoRA，仅作用于微调后的模型权重，无法直接访问基础模型的原始权重信息（Appendix E 中的可交换性保证了等价性，但未利用双模型信息联合建模的潜力）。

5. **实验覆盖有限**：仅验证了两种行为类型（隐藏 persona 和新闻摘要），且权重差异均通过 LoRA 引入。对更复杂的微调形式（如 RLHF、DPO、多任务指令微调）的适用性未知。

### 待解决的开放问题

- **内省机制的本质**：DIT 在模型内部究竟如何运作？它主要读取权重变化还是激活模式的变化？理解这一机制是提升泛化能力的前提。
- **规模化自省**：能否将大规模训练的 DIT-adapter 直接应用于基础模型，使其回答关于自身深层行为的问题（而非仅针对权重差异）？这将把 DIT 从“差异解释器”升级为“模型自省器”。
- **触发词反转的难度根源**：触发词发现是否天然比行为描述更难？能否结合搜索或优化技术扩展可解决的内省任务范围？
- **训练数据工程**：如何构建更大规模、更多样化的合成权重差异数据，以打破跨行为泛化的瓶颈？
- **适配器架构改进**：是否存在能同时访问微调前后模型信息的适配器架构（如双塔设计），从而提升解释的准确性和泛化性？
- **下游应用集成**：DIT 的输出能否作为自动化可解释性代理的组件，嵌入模型审计、安全检测或对齐验证流程？

## 原文 PDF

![[paperPDFs/ICLR_2026/Learning_to_Interpret_Weight_Differences_in_Language_Models.pdf]]
