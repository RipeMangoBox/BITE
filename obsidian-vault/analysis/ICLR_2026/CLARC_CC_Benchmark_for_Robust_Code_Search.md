---
title: "CLARC: C/C++ Benchmark for Robust Code Search"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/CLARC_CC_Benchmark_for_Robust_Code_Search.pdf
aliases:
- CLARC
tags:
- ICLR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/language_speech_and_dialog
core_operator: "代码中标识符的词法信息（原始、中性化、随机化）以及代码表示层次（高级语言 vs. Assembly/WebAssembly）"
primary_logic: "当前主流训练范式和评估基准鼓励模型匹配表面文本模式，而非功能等价性；CLARC 通过可编译性保障、依赖复杂度分类与多环境压力测试，揭示了模型对词法捷径的过度依赖，且标准微调无法弥补这一缺陷。"
claims:
- "在标识符中性化/随机化后，所有模型的检索指标均大幅下降：例如 Voyage-code-3 的 Group1 NDCG 从标准 88.61 降至中性 87.56、随机 83.85；CodeT5+ Group2 NDCG 从 53.02 降至 19.15。"
- "模型对汇编/WebAssembly 代码的检索能力极弱：Voyage-code-3 在 Assembly Group3 的 MRR 仅 15.20，远低于标准设置。"
- "即使在 CLARC 训练集上微调，标准设置与随机化设置之间的性能差距依然存在（CodeT5+ ft on Std: Group1 MRR Std 76.51 vs Ran 50.71）。"
- "词法扰动比例（修改标识符长度占比）与嵌入偏移距离呈强正相关（OASIS 中性化 r=0.762），而代码行数、圈复杂度等结构特征相关性很弱，直接证实模型依赖表面词法。"
---

# CLARC: C/C++ Benchmark for Robust Code Search

> [!tip] 核心洞察
> 当前主流训练范式和评估基准鼓励模型匹配表面文本模式，而非功能等价性；CLARC 通过可编译性保障、依赖复杂度分类与多环境压力测试，揭示了模型对词法捷径的过度依赖，且标准微调无法弥补这一缺陷。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | CLARC: 稳健代码搜索的C/C++基准测试 |
| 英文题名 | CLARC: C/C++ Benchmark for Robust Code Search |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=oO6D0whLDo); [Project](https://huggingface.co/datasets/ClarcTeam/CLARC) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/language_speech_and_dialog |
| Method | CLARC 基准数据集与自动化构建流水线 |
| Dataset | CLARC Group1 (Standard), CLARC Group1 (Neutralized vs Standard), CLARC Group1 (Randomized vs Standard), CLARC Group1 (Assembly) |

> [!tip] 效果简介
> - CLARC Group1 (Standard) 上，NDCG 为 Voyage-code-3 (88.61)，对比 BM25 (41.71)，变化 +46.90。
> - CLARC Group1 (Neutralized vs Standard) 上，NDCG 为 Neutralized (CodeT5+ 55.66)，对比 Standard (CodeT5+ 64.50)，变化 -8.84。
> - CLARC Group1 (Randomized vs Standard) 上，NDCG 为 Randomized (Voyage-code-3 83.85)，对比 Standard (Voyage-code-3 88.61)，变化 -4.76。

## 概述

当前代码搜索模型过度依赖浅层词法特征——尤其是标识符名称——而非理解代码的功能语义。这导致在标识符被匿名化（中性化或随机化）或代码被编译为低阶语言（如 Assembly、WebAssembly）后，检索性能出现剧烈下滑，暴露出严重的鲁棒性缺陷。现有评估基准多仅覆盖标准代码形态，未能有效检验模型对词法捷径的依赖。

CLARC（C/C++ Benchmark for Robust Code Search）正是针对这一瓶颈而设计。其核心洞察在于：主流对比学习范式和评估实践鼓励模型匹配表面文本模式，而非代码的等价行为。CLARC 通过一套自动化流水线，将可编译性保障、依赖复杂度分级（Group 1/2/3）与多维度压力测试（标识符中性化、随机化、编译为汇编/WebAssembly）系统性地整合，从而将模型对词法信息的依赖暴露为因果链条——词法扰动是嵌入偏移的最强预测因子，而代码结构特征几乎无关。

方法定位上，CLARC 提供的是一个“对抗式”基准，而非新模型。其流水线从 GitHub 采集可编译函数后，按自定义类型和辅助函数依赖的复杂度分为三组，并为每一片段自动生成标识符匿名化版本及编译后的低阶代码；查询则通过 LLM 生成并经严格假设检验验证合格。这构成了一组平行的评测设置，用以隔离词法信息的影响。

主要实验发现清晰印证了上述论断：即使在标准设置下表现优异的模型（如 Voyage‑code‑3 在 Group 1 上 NDCG = 88.61），在仅经过中性化处理后即出现下滑（87.56），随机化后进一步跌至 83.85；对标识符更敏感的模型（如 CodeT5+）在 Group 2 的 NDCG 从 53.02 骤降至 19.15。检索 Assembly 或 WebAssembly 代码的能力极弱，最优模型的 MRR 也仅约 15 %–30 %。更为关键的是，标准对比微调无法弥合这一差距：CodeT5+ 在 Group 1 上微调后，标准设定 MRR 升至 76.51，而随机化设定 MRR 仍仅为 50.71；OASIS 甚至在微调后在某些设置上出现性能倒退。词法扰动率与嵌入偏移的强正相关（r = 0.762）直接证实，当前嵌入模型实质上仍在进行标识符表面形式的匹配，而非代码语义的建模。

## 背景与动机

代码搜索是现代软件工程的基础基础设施，它通过自然语言查询从大规模代码仓库中检索相关函数或片段。近年的研究成果——包括 CodeT5+、OASIS、Nomic-emb-code 以及闭源的 Voyage-code-3 等嵌入模型——在常见的代码搜索基准上不断刷新指标，给社区带来了“语义理解正在成为可能”的印象。然而，**深入分析发现，这些模型多数依赖代码中的浅层词法特征，尤其是标识符名称，而非真正捕获程序的功能语义**。一旦标识符被中性化（替换为 `var1`, `func2` 等无意义记号）或完全随机化，检索性能便会急剧恶化。例如，在 CLARC 提供的评估设定下，Voyage-code-3 在标准 Group1 上的 NDCG 为 88.61，切换到中性化后降至 87.56，随机化后进一步跌至 83.85；而对于更依赖上下文的 Group2，CodeT5+ 的 NDCG 从 53.02 腰斩至 19.15 [Table 3, Table 4]。这说明现有模型在许多情况下并不是“理解代码”，而是“匹配标识符”。

这一瓶颈的根本原因在于**训练范式和评估基准的双重偏差**。流行的对比学习框架（如 InfoNCE）通常在庞大的标识符自然分布语料上训练，模型自然而然学会将标识符作为强预测信号，却忽略了对底层计算逻辑的建模。与此同时，长期以来社区使用的代码搜索数据集体量庞大但质量参差不齐：缺乏对代码可编译性的强制保证，也未考虑依赖复杂度带来的语义粒度差异，更缺少针对词法匿名化、低阶语言转换等鲁棒性压力测试的设置。这导致高指标背后的“功能等价性”理解依然薄弱——模型在常规场景下表现抢眼，但在真实世界常见的重构、开源代码复用、编译器优化等任务中可能彻底失效。

CLARC 正是为了填补这一缺⼝而被提出的。其设计与构造直接回应了上述动机：

1. **剥离标识符依赖**：通过中性化和随机化两种扰动方式，量化模型对标识符词法的敏感度。实验表明，词法扰动比例（修改标识符长度占比）与嵌入偏移距离呈强正相关（皮尔逊相关系数 r=0.762），而代码行数、圈复杂度等结构特征的相关性微乎其微，直接证实模型嵌入的漂移根源在于表面词汇 [Table 11]。
2. **拓展至低阶语言**：将代码编译为 Assembly 和 WebAssembly 后进行评估，彻底移除了所有高级语言命名信息。结果显示顶尖模型在 Assembly Group3 上的 MRR 仅 15.20，远低于原有水平，暴露出从程序逻辑到检索语义的巨大鸿沟 [Table 5, Table 10]。
3. **凸显微调局限性**：即使使用 CLARC 提供的训练集在标准设置下进行监督对比学习微调，标准设置与随机化设置之间的性能差距依然难以弥合（CodeT5+ 微调后 Group1 标准 MRR 为 76.51，而随机化测试集上仅 50.71）[Table 6]。这清楚地表明，简单的数据增强或常规微调并不能自动让模型学会“忽略标识符”，亟需全新的训练目标或模型架构。

综上所述，CLARC 的核心动机是通过一个系统化、可控制、多层次的评估框架，揭示并量化现代代码嵌入模型对词法捷径的过度依赖，为社区提供一个诊断脆弱性的压力测试平台，并指明从“文本匹配”迈向“语义理解”的必经之路。

## 核心创新

现有代码搜索基准（如 CodeSearchNet）主要依赖人工编写的描述与标准形态的源代码配对，未系统验证模型在代码被改写、匿名化或编译为低级语言后的鲁棒性。CLARC 通过四项关键设计变更，将评估目标从“表面文本匹配”转向“功能语义理解”，并直接揭示出当前嵌入模型普遍依赖词法捷径、且标准微调无法弥合这一缺陷的根本问题。

### 1. 完全可编译性保障
以往基准常纳入缺失头文件、辅助函数或语法错误的代码片段，导致评估结果可能受噪声和不完整上下文的影响。CLARC 的构建流水线强制所有函数在预设环境中通过编译（Section 3.1.1），确保每个样本都是真实可运行的单元。这一更动消除了语法层面的干扰，使性能指标更忠实地反映模型对代码语义的捕获能力。

### 2. 依赖复杂度分层分类
传统基准未区分代码片段对外部定义或辅助函数的依赖程度，将完全独立的函数与深度嵌入项目内部的函数混合评估。CLARC 按照自定义类型和辅助函数依赖的数量将代码分为三组（Group 1/2/3，Section 3.1.2），形成了从纯算法实现到高度耦合模块的难度梯度。

该分类暴露出模型行为与依赖模式的复杂关系：在标准设置中，现代模型对强依赖的 Group 2 的 NDCG 反而高于无依赖的 Group 1（Nomic-emb-code：93.61 vs 88.61，Table 3），暗示强依赖代码携带了更多区分性词法线索；然而在标识符随机化后，Group 2 的跌幅远大于 Group 1（Voyage-code-3 Group 2 NDCG 从 93.61 骤降至 75.22±0.54，Table 3 vs Table 8），证明模型对标识符词汇的依赖随依赖深度进一步放大。

### 3. 多层鲁棒性压力测试
绝大多数基准仅考察代码的标准形态，无法检验模型对标识符重命名或编译转换的敏感性。CLARC 专项引入了三种压力设置（Section 3.1.3）：
- **标识符中性化（Neutralized）**：将所有标识符替换为 `var_i` 等无意义记号；
- **标识符随机化（Randomized）**：替换为随机生成字符串，进一步消除命名规律；
- **低级语言编译**：将源代码编译为 Assembly 或 WebAssembly 文本格式，彻底剥离高级语言结构。

这些设置直接击中了模型的脆弱性：
- **词法依赖性**：所有模型在随机化设置下均出现大幅退化。Voyage-code-3 Group 1 NDCG 从 88.61 降至 83.85（Table 3, 4），CodeT5+ Group 2 NDCG 更是从 53.02 跌落至 19.15（Table 4）。随机化 10 次试验的标准误低于 1.0（Table 8），确认该退化并非随机波动，而是系统性缺陷。
- **低级语言泛化失败**：在 Assembly 和 WebAssembly 设置下，所有模型的指标降至极低水平，如 Voyage-code-3 在 Assembly Group 3 的 MRR 仅 15.20（Table 5），远低于标准设置，表明模型几乎未习得底层运算逻辑。
- **微调无法缩小差距**：即便在 CLARC 训练集（5,472 对，Table 7）上采用 InfoNCE 对比学习进行微调，标准设置与随机化设置之间的性能鸿沟依然顽固存在（CodeT5+ ft. on Std：Group 1 MRR Std 76.51 vs Ran 50.71，Table 6）。更关键的是，OASIS 在标准数据上微调后，在其他设置上的表现反而退步（Group 2 MRR 从 88.30 降至 78.26），说明词法捷径已深度编码进模型参数，单纯增加数据或常规对比目标难以逆转。

### 4. LLM 驱动的可扩展查询生成
以往基准多依赖人工撰写代码描述，成本高且难以规模化。CLARC 构建了两阶段 LLM 查询生成流水线：首先利用 o3-mini 和 grok-4 为每个函数自动生成自然语言描述（Section 3.1.4），随后通过双样本 T 检验（Wang et al., 2023a）严格比较 LLM 生成与人工专家描述的质量（Section 3.2）。假设检验结果显示 LLM 描述质量与人工标签相当甚至更优（Group 1 p = 99.99%），且在各组别上均保持高标注一致性（Krippendorff’s α 65.51–74.77，Table 2）。在人工标注子集上进行验证，全量数据集的检索结果与子集高度吻合（Table 9），证实自动化查询既保证了品质又具备扩展性，使基准可持续随代码仓库增长。

### 创新揭示的本质缺陷
上述设计不仅界定了 CLARC 相较于先前基准的方法论改变，更通过因果性分析锁定了模型的核心弱点：**嵌入模型主要依赖浅层词法特征（特别是标识符文本）进行检索，而非理解代码的功能语义。** 词法扰动比例（修改的标识符长度占比）与嵌入向量偏移距离呈强正相关（OASIS 中性化 r = 0.762，p < 0.01，Table 11），而代码行数、圈复杂度等结构特征的相关性极弱，直接证明标识符是模型决策的主要依据。该发现精准解释了为何标识符随机化或编译为 Assembly 会导致性能崩塌，以及为何标准对比学习微调无法从根本上修复这一脆弱性——因为它本质上是数据分布偏差与架构归纳偏置的耦合结果，而非简单的训练不足。

## 整体框架

现有代码搜索基准普遍不强调代码片段的实际可编译性，也未系统区分标识符语义与功能语义，导致主流模型倾向于学习词法表面的捷径，而非代码的逻辑等价性。CLARC 针对这一瓶颈，提出了一套自动化基准构建流水线，其核心包括四个有序模块（Section 3.1）：

1. **可编译数据采集（Data Collection）**  
   从 GitHub 仓库中过滤并提取 C/C++ 函数，强制要求每个代码片段在预设编译环境中通过编译（Section 3.1.1）。这一步从根本上避免了传统数据集因缺少头文件或辅助函数而无法运行的弊端，使得后续评估聚焦于真实可执行的代码语义。

2. **依赖复杂度分类（Categorization）**  
   所有函数按其对外部自定义类型或辅助函数的依赖程度被划分为三组：Group 1 为完全自包含的独立函数，Group 2 依赖自定义类型，Group 3 则同时依赖类型与外部辅助函数（Section 3.1.2）。表 1 给出了各组的代码行数、圈复杂度等统计，反映出从简单到复杂的函数谱系，为分析模型在不同依赖深度下的行为提供了结构化支架。

3. **多形态压力设置（Different Settings）**  
   流水线为每一条代码生成四种形态：（a）标准源码（Standard）；（b）标识符中性化（Neutralized），将具名标识符替换为无意义占位符；（c）标识符随机化（Randomized），每次随机生成无意义名称；（d）编译为低级语言形式（Assembly 与 WebAssembly）（Section 3.1.3）。这一设计将代码的表面词法信息与内在功能语义解耦，从而在评价中系统暴露模型对浅层文本匹配的依赖。

4. **LLM 查询生成与统计验证（Query Formation）**  
   采用大型语言模型（o3‑mini、grok‑4）为每一条函数自动生成自然语言功能描述，并通过与人类专家标注对比的假设检验框架验证其质量（Section 3.1.4, Section 3.2）。如表 2 所示，LLM 描述在各组中的平均得分均高于或可比于人类描述，且 p 值均不低于 76.32%，表明生成的查询在语义完整性与相关性上高度可靠，同时大幅降低了人工标注成本。

上述流水线的输入是来自 GitHub 的大量 C/C++ 函数源码，输出则是成对出现的自然语言查询与代码片段，且每对代码均同时具备标准、中性化、随机化及汇编形式。此外，作者使用同一流水线构建了 5 472 对训练集（Table 7），用于后续微调实验。整个框架通过“可编译性 → 复杂度分级 → 多设置压力测试 → 自动查询验证”的闭环，将鲁棒性评估从单向指标对比升级为对模型语义理解能力的多维度诊断。

（注：本小节描述的流水线细节与证据均来自论文原文 Section 3.1 及相关表格，进一步的技术细节见原文附录。）

## 核心模块与公式推导

### 基准构建流水线
CLARC 的构建围绕一条四阶段自动化流水线展开，核心目标是制造可控的词法扰动与语义压力，从而暴露模型对表面标识符的过度依赖。

1. **数据采集（Data Collection）**  
   从 GitHub 仓库提取 C/C++ 函数，并强制在预设环境中编译通过。该步骤保证了所有代码片段具有真实、完整的语义，消除了传统基准中因缺失头文件或辅助函数导致的语法截断，为后续压力测试提供了可执行语义基础（Section 3.1.1）。

2. **依赖复杂度分类（Categorization）**  
   按代码对外部自定义类型、辅助函数等资源的依赖强度，将函数划分为三组（Group 1/2/3）。Group 1 为完全自包含函数，Group 2 依赖项目内其他定义，Group 3 涉及复杂项目级 API 调用。该分类使得能够分层评估模型从局部语义词法匹配到全局上下文理解的能力退化（Section 3.1.2）。

3. **多设置生成（Different Settings）**  
   为剥离词法捷径，CLARC 为每段原始代码生成多种变体：
   - **Neutralized（中性化）**：将所有标识符替换为无意义通用名（如 `var1`、`funcA`），保留控制流与类型结构；
   - **Randomized（随机化）**：进一步随机打乱标识符，完全破坏词法模式；
   - **Assembly / WebAssembly**：将代码编译为汇编或 `.wat` 格式，消除所有变量名、函数名及高级控制流结构。
   这些设置直接构造了“词法信息量”这一因果调节变量，是揭示模型鲁棒性瓶颈的关键机制（Section 3.1.3）。

4. **查询生成（Query Formation）**  
   使用 LLM（o3‑mini、grok‑4）自动生成自然语言查询，并通过假设检验与人工标注子集进行统计对比。Table 2 显示在所有组别中 LLM 查询与人工质量的差异不显著（甚至更优），保证了查询的语义覆盖度与可复现性，避免人工偏差对模型评估的干扰（Section 3.1.4, Section 3.2）。

### 微调损失函数
在消融实验中，论文对 CodeT5+ 和 OASIS 进行对比微调时，采用 InfoNCE 损失：

$$
\mathcal{L}_i = -\log \frac{\exp\left(\sin\left(\mathbf{h}_{q_i}, \mathbf{h}_{c_i}\right) / \tau\right)}
{\sum_{j=1}^{N} \exp\left(\sin\left(\mathbf{h}_{q_i}, \mathbf{h}_{c_j}\right) / \tau\right)}
$$

- $\mathbf{h}_{q_i}$、$\mathbf{h}_{c_i}$：第 $i$ 个查询与对应正例代码的嵌入向量；  
- $\tau = 0.05$：温度系数，控制分布的锐利程度；  
- $N$：批次大小，负样本由同一批次内其他代码实例提供。

**注**：原文（附录 F.4）分子与分母中使用了 $\sin$ 符号，但根据上下文及对比学习惯例，此处应为余弦相似度 $\text{sim}$，大概率属于笔误。尽管如此，上述公式严格保留了原论文中的 LaTeX 表达形式。

## 实验与分析

### 主实验结果
在标准设置下，CLARC 对 6 个代码检索模型（BM25、CodeT5+、OASIS、Nomic-emb-code、OpenAI‑text‑embedding‑large、Voyage‑code‑3）进行了系统评估（Table 3）。Voyage‑code‑3 在多数指标上取得最佳结果，例如 Group1 的 NDCG 达到 88.61，显著超越传统 BM25 的 41.71（+46.90）。然而，模型性能的分布呈现明显的依赖层级：在涉及自定义类型/辅助函数的 Group2 中，Nomic‑emb‑code 的 NDCG 反超 Voyage‑code‑3（93.61 vs. 88.61），而 CodeT5+ 在 Group3 Long 上的 NDCG 仅 21.12，远低于其对 Group3 Short 的 43.55，表明模型对长距离依赖和复杂结构的处理能力分化严重。

![[assets/figures/papers/iclr26_0013_oO6D0whLDo_CLARC_CC_Benchmark_for_Robust_Code_Search/figures/005_Table_3.jpg]]
*Table 3: Evaluation Results on the Standard Setting. Bold entries stand for the maximum values for the metrics in the category. OpenAI stands for OpenAI-text-embedding-large. Voyage stands for Voyage-code-3*

一旦对标识符实施词法扰动，模型表现普遍大幅滑坡（Table 4）。中性化（将标识符替换为类型前缀+编号）已造成明显降级：Voyage‑code‑3 在 Group1 的 NDCG 从 88.61 降至 87.56；随机化（完全随机重命名）则导致更严重的退化，同一指标跌至 83.85。更突出的是 CodeT5+ 在 Group2 上的 NDCG 从标准设置的 53.02 急降到 19.15，降幅达 33.87 点。这些结果一致说明，预训练模型严重依赖标识符的表面词法信息，而非代码的语义等价性。

![[assets/figures/papers/iclr26_0013_oO6D0whLDo_CLARC_CC_Benchmark_for_Robust_Code_Search/figures/006_Table_4.jpg]]
*Table 4: Evaluation Results on the Neutralized and Randomized Settings. Neu stands for Neutralized, and Ran stands for Randomized. Bold entries stand for the maximum values for the metrics in the category. The evaluation results on the Randomized Setting are the average after 10 trials, and results with standard errors can be found in Appendix F.1*

当查询目标变为低阶表示时，所有模型几乎失效（Table 5）。在 Assembly 环境下，即使最强的 Voyage‑code‑3 在 Group3 上的 MRR 也仅有 15.20，OpenAI‑text‑embedding‑large 则降至个位数。WebAssembly 设置下的趋势一致，检索能力极度薄弱。这暴露出现有模型在编译后代码上的无能为力，也证实了它们对高层语言词法特征的过度适应。

![[assets/figures/papers/iclr26_0013_oO6D0whLDo_CLARC_CC_Benchmark_for_Robust_Code_Search/figures/007_Table_5.jpg]]
*Table 5: Evaluation Results on the Assembly and WebAssembly Settings*

### 微调与消融实验
为检验训练能否弥补鲁棒性缺口，我们在 CLARC 训练集上对 CodeT5+ 和 OASIS 进行监督对比微调，使用 InfoNCE 损失（$\mathcal{L}_i = -\log \frac{\exp(\sin(\mathbf{h}_{q_i},\mathbf{h}_{c_i})/\tau)}{\sum_{j=1}^N \exp(\sin(\mathbf{h}_{q_i},\mathbf{h}_{c_j})/\tau)}$，原文中 $\sin$ 疑为 $\mathrm{sim}$ 笔误，需确认），$\tau=0.05$，负样本来自批次内其他代码（F.4 Finetuning Details）。结果（Table 6）显示，CodeT5+ 在所有测试设置上 MRR 均有提升，但标准与随机化环境之间的性能鸿沟并未弥合：例如，CodeT5+ 在标准数据上微调后，标准设置下的 MRR 为 76.51，而随机化设置仅 50.71，差距达 25.80。OASIS 则在微调后出现性能回退——在 Group2 标准设置下，其 MRR 从 88.30（未微调）退步到 78.26（在 Std 上微调），表现出过度专业化。这表明标准对比学习范式无法消除模型对词法标识符的依赖，且可能使模型更紧密地贴合训练分布的表层模式。

![[assets/figures/papers/iclr26_0013_oO6D0whLDo_CLARC_CC_Benchmark_for_Robust_Code_Search/figures/008_Table_6.jpg]]
*Table 6: Performance of the Finetuned Models on MRR. “ft. on X” indicates finetuning on setting X*

更深层的证据来自嵌入偏移分析（Table 11）。我们将各模型在中性化/随机化后的嵌入变化距离与多种代码特征进行相关性检验，发现词法扰动率（修改的标识符长度占比）是最强的预测因子：OASIS 在中性化条件下的 Pearson r 高达 0.762，而代码行数、圈复杂度等结构特征的相关性显著偏低。这直接证实了模型对词法捷径的依赖是导致鲁棒性坍塌的因果机制。

![[assets/figures/papers/iclr26_0013_oO6D0whLDo_CLARC_CC_Benchmark_for_Robust_Code_Search/figures/013_Table_11.jpg]]
*Table 11: Correlation between the embedding shift distance and various features*

### 失败模式与局限性
综合以上，当前代码检索模型的主要失败模式可归结为：
1. **词法偏好压倒语义理解**：匿名化/随机化标识符即能使高度优化的闭源模型（如 Voyage‑code‑3）性能明显衰退，证明模型以标识符名称为主要检索信号。
2. **低阶语言场景失能**：在 Assembly/WebAssembly 环境下，所有模型几乎无法检索到正确函数，MRR 普遍低于 30，意味着它们不具备跨越编译层级的语义匹配能力。
3. **微调无法根治**：简单在 CLARC 上微调不能弥合标准与匿名化设置间的性能差距，甚至可能导致更严重的过拟合（OASIS 案例）。训练目标未改变模型利用表层特征的偏好。
4. **评估范围受限**：当前基准仅覆盖 C/C++，未拓展至其他系统语言；评估集规模（1,245 对）对大规模排序模型训练仍显不足；LLM 生成查询虽经假设检验验证（Table 2），隐患偏好仍可能存在。

![[assets/figures/papers/iclr26_0013_oO6D0whLDo_CLARC_CC_Benchmark_for_Robust_Code_Search/figures/004_Table_2.jpg]]
*Table 2: Hypothesis Testing Results. The LLM-generated descriptions for functions in all three groups are comparable or superior in quality to those written by human annotators*

### 关键图表结论
- Table 3 与 Table 4 共同构成核心证据链：标准设置下的高分与扰动设置下的急剧跌落，直接量化了模型对词法信息的依赖程度。
- Table 5 暴露了模型在 Assembly/WebAssembly 上的极限，为代码搜索向编译后领域扩展设立了严峻基线。
- Table 6 的微调结果证明，仅靠现有对比学习范式无法构建鲁棒表示，需探索新的训练目标或数据增强策略。
- Table 11 的嵌入偏移相关性分析，因果性地锁定了词法扰动率为主因，为未来解决方向提供了明确的诊断靶点。

## 方法谱系与知识库定位

CLARC 并非提出新的检索模型，而是构建了一个系统评估实验台，以此揭示当前代码搜索主流范式的结构性缺陷。在它之前，CodeSearchNet 等基准虽然推动了神经模型在代码搜索上的应用，但普遍缺乏对可编译性、依赖复杂度和语言表面形态变化的控制。CLARC 通过四项底层设计改变了评估的因果操纵空间：（1）强制可编译性保障（Section 3.1.1）使得“理解代码语义”成为必须，而非可选；（2）按自定义类型/辅助函数依赖将片段分为三组（Section 3.1.2），解耦了简单函数、内部依赖和外部依赖场景对模型能力的不同需求；（3）引入标识符中性化（Neutralized）、随机化（Randomized）以及编译为 Assembly/WebAssembly 的多环境压力测试（Section 3.1.3），直接操纵模型中可能被当作“语义”的联想捷径；（4）以 LLM 自动生成的查询替换人工描述，并经假设检验验证（Section 3.2），在保证质量的同时大幅提升了可扩展性。这种设计使 CLARC 从一个“公平比较”的排行榜变成了一个“因果诊断”的工具，与以往仅聚焦标准形态的基准在目标上有本质区别。

现有模型的谱系大致可以看作从传统词频匹配（BM25）到预训练嵌入模型的演进。BM25 在各组中的 NDCG 仅 41.71（Table 3），说明纯词法匹配严重受限于标识符多样性。CodeT5+、OASIS、Nomic‑emb‑code 等基于 Transformer 的模型虽然在标准设置下表现大幅提升，但证据表明它们的优势很大程度上依赖于标识符中的语义关联而非代码功能本身：当标识符被中性化后，CodeT5+ Group2 的 NDCG 即从 53.02 跌至 19.15，随机化后 Voyage‑code‑3 的 Group1 NDCG 也从 88.61 降至 83.85（Table 4）。在 Assembly/WebAssembly 设定下，所有模型的检索能力崩溃，即便是最强的 Voyage‑code‑3 在 Assembly Group3 的 MRR 仅余 15.20（Table 5），表明其嵌入空间中高级语义与低阶指令之间几乎不存在合理的映射。微调实验进一步暴露了这一鸿沟的顽固性：采用 InfoNCE 损失对 CodeT5+ 和 OASIS 进行标准微调后（Table 6），标准配置下的 MRR 确有提升，但 Std 与 Randomized 设置间的性能差距几乎未被弥合（CodeT5+ ft. on Std: Std MRR 76.51, Ran 50.71）；OASIS 甚至在某些组上出现微调后退步，显示出对特定标识符模式的过度专业化。相关性分析更直接锁定因果机制：词法扰动比例（修改标识符长度占比）与嵌入偏移距离之间呈 r=0.762 的强正相关，而代码行数、圈复杂度等结构特征相关性很弱（Table 11），直接证实模型对表面词法的寄生。

从适用边界看，CLARC 目前仅覆盖 C/C++ 语言，尚未扩展到 Rust、Go 等系统编程语言，其评估集 1245 对的规模对大规模排序模型的训练仍显不足。查询生成虽经假设检验校验，但完全依赖 LLM 可能引入特定的语言风格偏好，且人工标注子集的验证虽显示一致性（Table 9），但并未完全消除偏差风险。微调研究仅探索了对比学习这一种范式，尚未触及数据增强、多任务或对抗训练等可能的弥补路径。最关键的是，CLARC 是一面镜子而非手术刀：它系统诊断了词法捷径的低阶语言脆弱性，却未给出任何可行的鲁棒性增强方案。由此引出的开放问题核心是：能否设计一种代码语义表示，在保持高级语言检索效能的同时，天然对标识符和编译层次不敏感？以及，为什么标准监督对比学习无法消除词法依赖，这是训练数据分布的固有偏差还是架构归纳偏置所致？最后一个技术性疑问也值得注意：论文中给出的 InfoNCE 损失公式分子使用了 sin 而非 sim（余弦相似度），若确为笔误，则可能影响微调复现的准确率。

这些局限和问题将 CLARC 定位于知识图谱的“诊断层”：它没有撼动现有排名，而是为社区提供了一组精密的压力指标，迫使我们重新审视模型声称的“语义理解”究竟有多少分量。

## 原文 PDF

![[paperPDFs/ICLR_2026/CLARC_CC_Benchmark_for_Robust_Code_Search.pdf]]
