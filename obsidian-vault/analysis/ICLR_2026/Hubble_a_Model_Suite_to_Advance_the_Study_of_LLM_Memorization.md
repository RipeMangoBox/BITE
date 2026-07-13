---
title: "Hubble: a Model Suite to Advance the Study of LLM Memorization"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/Hubble_a_Model_Suite_to_Advance_the_Study_of_LLM_Memorization.pdf
project_link: null
code_link: null
openreview_forum_id: ZfdnZhOP0k
aliases:
- Hubble
tags:
- ICLR_2026
- topic/benchmarks_datasets_evaluation
- topic/benchmarks_datasets_evaluation/benchmark_eval
core_operator: "训练语料库的大小和敏感数据在预训练过程中的插入时机是两个可独立操纵的因果因素，能够显著影响模型对特定文本的记忆强度。"
primary_logic: "稀释（通过增大训练语料库降低敏感数据的相对频率）和前置（将敏感数据安排在训练早期出现）是两种通用的最佳实践，可以跨领域降低版权、隐私和测试集污染等记忆化风险。"
claims:
- "在相同的重复级别下，训练在500B tokens上的模型比训练在100B tokens上的模型在所有领域的记忆化表现都更弱，证实稀释效应。"
- "仅在训练的前四分之一插入敏感数据，最终模型几乎不记忆这些数据；而仅在最后四分之一插入则记忆最多，验证了排序效应。"
- "随着文本重复次数从1增加到256，成员推理攻击的ROC AUC从约0.54提升到1.0，表明记忆强度直接决定隐私风险的可检测性。"
- "Copyright Passages (Wikipedia, Gutenberg books etc.) 上 长度归一化对数似然 = 8B perturbed (500B tokens)"
---

# Hubble: a Model Suite to Advance the Study of LLM Memorization

> [!tip] 核心洞察
> 稀释（通过增大训练语料库降低敏感数据的相对频率）和前置（将敏感数据安排在训练早期出现）是两种通用的最佳实践，可以跨领域降低版权、隐私和测试集污染等记忆化风险。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | Hubble：一个推动LLM记忆化研究的模型套件 |
| 英文题名 | Hubble: a Model Suite to Advance the Study of LLM Memorization |
| 会议/期刊 | ICLR 2026 (Oral) |
| Links | [paper](https://openreview.net/forum?id=ZfdnZhOP0k) |
| Topic | #topic/benchmarks_datasets_evaluation #topic/benchmarks_datasets_evaluation/benchmark_eval |
| Method | HUBBLE模型套件及受控扰动插入框架 |
| Dataset | Copyright Passages (Wikipedia, Gutenberg books etc.), Gutenberg Unpopular passages (成员推理攻击, MIA), YAGO Biographies PII reconstruction |

> [!tip] 效果简介
> - Copyright Passages (Wikipedia, Gutenberg books etc.) 上，长度归一化对数似然 为 8B perturbed (500B tokens)，对比 8B perturbed (100B tokens)，变化 在相同重复级别下，500B模型的记忆强度显著低于100B模型（样本间损失差异更小）。。
> - Gutenberg Unpopular passages (成员推理攻击, MIA) 上，ROC AUC (Loss MIA) 为 Dup = 256，对比 Dup = 1，变化 0.539 → 1.0 （从接近随机到完美区分）。
> - YAGO Biographies PII reconstruction 上，攻击成功率（full-prefix MCQ） 为 8B perturbed (100B tokens)，对比 standard model (unperturbed)，变化 标准模型准确率接近随机，扰动模型在16次重复时达到近100%准确率。。

## 概要

大型语言模型（LLM）的记忆化行为是版权、隐私和基准污染等风险的核心来源，但现有研究大多依赖对商业模型的抽样观察，难以在受控条件下分离重复频率、文本简单性等混淆因素，导致许多因果量（如“需要多少次重复才能记忆一条测试样本”）无法可靠估计。

Hubble 模型套件正是为解决这一瓶颈而设计。其核心思路是**在标准预训练语料中插入已知的扰动文本**（书籍段落、传记、测试集等），并随机分配每条数据的重复次数（0×, 1×, 4×, 16×, 64×, 256×），从而将“训练语料库大小”和“敏感数据的插入时机”转化为可独立操纵的因果因素。通过比较标准模型与扰动模型在不同条件下的记忆强度，研究者可以量化稀释效应和排序效应，并评估成员推理攻击、PII重建等下游风险。

实验揭示了两个通用最佳实践：**稀释**——通过增大训练语料库降低敏感数据的相对频率，可显著削弱记忆；**前置**——将敏感数据安排在训练早期出现，最终模型几乎不记忆这些数据。在相同的重复级别下，训练在 500B tokens 上的模型比训练在 100B tokens 上的模型在所有领域的记忆化表现都更弱（Figure 2）；而仅在训练前四分之一插入扰动数据的模型，其记忆强度远低于在最后四分之一插入的模型（Figure 14）。此外，随着文本重复次数从 1 增加到 256，成员推理攻击的 ROC AUC 从约 0.54 提升至 1.0（Table 1），表明记忆强度直接决定隐私风险的可检测性。

在方法谱系上，Hubble 并非提出新的训练算法或架构，而是构建了一个**受控扰动插入框架**：以经过去污染的 DCLM 语料为基础，在序列拼接层面注入扰动文本，并通过统一的 loss 比较、选择题和生成式抽取三种协议评估记忆化。该框架填补了“大规模受控记忆化实验”的空白，为后续的知识编辑、机器遗忘和隐私审计研究提供了可复现的因果基准。

值得注意的是，Hubble 的结论目前基于最大 8B 参数、500B tokens 的模型，远小于商业 LLM（如 Llama 3 的 15T tokens），稀释和排序策略也仅能缓解而非消除风险。但作为首个系统操纵训练数据中重复频率和插入时机的模型套件，它已为理解 LLM 记忆化的因果机制奠定了关键基础。

大型语言模型（LLM）的记忆化（memorization）现象——即模型在训练后能够逐字复现训练数据中的特定文本——已成为版权保护、隐私泄露和基准污染等关键风险的根源。然而，对这一现象的系统性研究长期受制于一个核心瓶颈：**现有LLM记忆研究难以在大型模型上进行受控实验，导致抽样观察难以分离重复、文本简单性等混淆因素，许多因果量无法估计**。研究者通常只能对已部署模型进行被动观察，无法主动操纵训练数据中的关键变量，因而难以回答诸如“需要多少次重复才能导致记忆化”“敏感数据在训练中出现的时机如何影响记忆强度”等因果性问题。

HUBBLE项目正是为突破这一瓶颈而设计。其核心思路是构建一个包含标准模型与扰动模型的套件：标准模型在高质量净化的DCLM语料上预训练，而扰动模型则在相同语料中**受控插入**多种类型的敏感文本（包括书籍段落、传记、测试集等），并随机分配每条数据的重复次数（0×, 1×, 4×, 16×, 64×, 256×）。通过随机化插入文本及其重复率，研究者首次能够测量一系列此前无法估计的因果量，例如“记住一个测试集样本所需的最小重复次数”。这一框架将记忆化研究从相关性的观察层面提升到了因果推断层面。

HUBBLE的设计覆盖了版权、隐私和测试集污染三大风险领域，其扰动数据类型包括：流行与非流行Gutenberg书籍段落、MRPC与PAWS改写对、YAGO与ECtHR传记、Personachat对话、以及MMLU与SQuAD等基准测试集。这种多领域、多数据类型的覆盖使得跨领域的记忆化规律比较成为可能。

## 核心方法与创新机理

Hubble 的核心创新并非提出一种新的模型架构或训练算法，而是构建了一套**受控实验基础设施**，将 LLM 记忆化研究从被动的抽样观察转变为主动的因果推断。其关键突破在于识别并操纵了两个此前难以分离的因果因素，从而系统地揭示了记忆化的形成机制与缓解策略。

### 因果操纵：从混淆中分离关键变量

现有记忆化研究的根本瓶颈在于，训练数据中的重复次数、文本简单性、数据出现时机等因素天然混杂，导致许多因果量无法估计。Hubble 通过**受控扰动插入框架**直接解决了这一问题，将两个核心因素变为可独立操纵的实验旋钮：

| 操纵变量 | 标准模型（基线） | 扰动模型（Hubble） | 因果效应 |
|---------|----------------|-------------------|---------|
| **敏感数据的重复次数** | 使用净化的 DCLM 语料，不含人为插入的敏感内容 | 在标准语料中插入多种类型的扰动文本（书籍段落、传记、测试集等），并随机分配重复次数（0×, 1×, 4×, 16×, 64×, 256×） | 直接测量重复次数与记忆强度的剂量-反应关系 |
| **敏感数据的插入时机** | 扰动模型默认在整个训练过程中均匀插入 | 时序实验中扰动仅在指定的训练阶段（如前 25%、前半段等）插入 | 揭示数据暴露时机对最终记忆化的决定性影响 |

这种设计使得研究者能够精确回答诸如“一段文本需要重复多少次才会被模型逐字记忆？”、“在训练早期还是晚期暴露数据更危险？”等先前无法定量回答的问题。

### 从因果发现到最佳实践

基于上述因果操纵，Hubble 得出了两项具有跨领域普适性的核心发现：

1. **稀释效应（Dilution）**：通过增大训练语料库规模来降低敏感数据的相对频率，可以显著削弱记忆化。决定性证据来自 Figure 2——在相同的重复级别下，训练在 500B tokens 上的模型比训练在 100B tokens 上的模型在所有领域的记忆化表现都更弱。这一发现为数据策展中的版权风险控制提供了直接的操作指引。

2. **排序效应（Ordering）**：敏感数据在训练过程中出现的时机至关重要。Figure 14 显示，仅在训练的前四分之一插入敏感数据时，最终模型几乎不记忆这些数据；而仅在最后四分之一插入则记忆最多。这一发现揭示了“前置”策略——将敏感数据安排在训练早期出现——可以作为一种通用的记忆化缓解手段。

这两项发现共同构成了 Hubble 的核心洞见：**稀释和前置是两种通用的最佳实践，可以跨领域降低版权、隐私和测试集污染等记忆化风险**。它们并非完全消除风险，而是提供了在数据策展和训练流程设计层面可操作的缓解方向。

### 实验设计的创新保障

Hubble 的实验设计本身也体现了重要的方法学创新。通过随机分配每条扰动数据的重复次数，模型无法利用时间戳或文档边界等假性特征来区分成员与非成员，从而确保了成员推理攻击（MIA）等评估的有效性。Table 1 的结果——当重复次数从 1 增加到 256 时，MIA 的 ROC AUC 从约 0.54（接近随机）提升到 1.0（完美区分）——直接验证了这一设计的必要性：记忆强度本身就是隐私风险可检测性的决定因素。

此外，多域扰动之间的干扰极小（Figure 20 显示核心多域扰动模型在每一域的表现与仅训练单一域扰动的模型几乎一致），这保证了研究者可以在同一个模型中同时研究版权、隐私和测试集污染等多个记忆化维度，而无需担心跨域混淆。

HUBBLE 的核心设计理念是通过**受控扰动插入**，在大型语言模型的预训练过程中引入可精确操纵的“敏感数据”，从而将记忆化研究从被动观测转变为主动的因果实验。整个框架由四个紧密耦合的模块构成，形成一条从数据准备到因果推断的完整流水线。

### 基础语料库与去污染

流水线的起点是 **DCLM 语料库**（DataComp-LM, Li et al., 2024a），这是一个经过严格过滤的高质量英文 CommonCrawl 数据集。在插入任何扰动之前，系统首先执行**语料库去污染**：扫描整个训练集，移除所有与待插入扰动文本相匹配的文档。这一步至关重要——它确保了后续实验中每条扰动数据的“重复次数”完全由实验者控制，而非被语料库中天然存在的副本所混淆。

### 扰动文本设计与插入

扰动数据覆盖三大风险领域：**版权**（Gutenberg 书籍的流行与冷门段落）、**隐私**（YAGO 人物传记、Personachat 对话）以及**测试集污染**（MMLU、HellaSwag 等基准的示例）。每条扰动数据被随机分配一个重复级别：0×、1×、4×、16×、64× 或 256×，其中 0× 作为对照组，表示该文本从未出现在训练中。

插入过程如图 1 所示：系统从标准训练流程中采样一个训练序列（由 EOS 分隔的随机拼接文档），在文档间隙中随机选取一个位置，将扰动文本拼接进去，随后将序列裁剪回原始长度，同时保证扰动文本不被截断。每条扰动被 EOS 标签包围，与普通文档格式一致，但保证不会被拆分到两个训练序列中，且每个序列最多插入一条扰动。在 100B tokens 的语料规模下，所有扰动经重复后总计仅 79.9M tokens（占 0.08%），以 818k 条序列的形式插入，对整体数据分布的干扰极小。

### 模型架构与训练

HUBBLE 模型基于 **Llama 3 架构**，做了几项适配性修改：采用更小的 OLMo 分词器、解绑定权重的嵌入层，8B 模型配置为 36 层。核心实验采用 **2×2×2 因子设计**：模型规模 {1B, 8B} × 数据条件 {标准, 扰动} × 训练数据量 {100B, 500B}，共 8 个模型。所有模型使用 GPT-NeoX 框架在相同超参数下训练，确保除数据因素外其他条件完全一致。

### 记忆化评估协议

评估从三个维度量化记忆化程度：
1. **基于 Loss 的直接比较**：计算模型在扰动文本上的长度归一化对数似然，与标准模型对比；
2. **基于 Loss 的选择题**：将正确文本与干扰项混合，通过模型赋予的似然值判断其能否“认出”训练过的内容；
3. **生成式抽取**：向模型提供前缀，检查其能否逐字复现后续内容。

这套评估覆盖所有插入数据类型，统一使用 EleutherAI 的 lm-eval-harness 执行，保证可复现性。对于隐私领域，评估还区分了攻击者掌握不同辅助信息（如仅知道姓名）时的重建能力。

### 因果操纵的两个核心旋钮

框架最关键的贡献在于暴露了两个可独立操纵的因果因素：
- **稀释（Dilution）**：通过增大训练语料库总量（100B → 500B），降低敏感数据的相对出现频率；
- **排序（Ordering）**：通过时序实验模型（InsertRange 系列），将扰动数据的插入精确限制在训练的特定阶段（如前 25%、中间 50% 等），研究暴露时机对记忆化的影响。

这两个旋钮使得研究者能够直接估计“需要多少次重复才能让模型记住一段文本”“早期暴露与晚期暴露的记忆强度差异有多大”等此前无法量化的因果量，为版权保护、隐私防御和测试集去污染提供了可操作的实验依据。

### 3.1 受控扰动插入框架

HUBBLE的核心方法论创新在于构建了一套**受控扰动插入框架**，将记忆化研究从被动观察转变为主动因果干预。该框架包含以下关键模块：

**基础语料库与去污染**：预训练基础语料采用DataComp-LM（DCLM；Li et al., 2024a）的高质量过滤英文文本。为确保插入的重复次数精确反映实际训练中的重复，系统性地移除与任何扰动文本相匹配的训练文档（§3.1）。

**扰动文本插入机制**：扰动模型的核心操作是将预先设计好的敏感文本以模拟真实文档的方式拼接到训练序列中。具体流程如Figure 1所示：
1. 从标准训练过程中采样一条训练序列（由随机拼接的文档组成，以EOS token分隔）；
2. 在文档间的随机间隙处插入扰动文本；
3. 将序列调整回原始长度，同时确保扰动文本不被截断；
4. 每条扰动文本被EOS标签包围，与常规文档格式一致，但保证不会被拆分到两个训练序列中，且每个序列最多插入一条扰动。

**重复次数随机化**：对每个扰动数据集，随机分配示例的重复次数为 {0×, 1×, 4×, 16×, 64×, 256×}（§3.1）。这一设计直接操纵了“训练语料库中敏感数据的重复频率”这一因果变量，使得研究者能够量化“记忆一条文本所需的最小重复次数”等因果量。所有扰动经重复后总计79.9M tokens（插入818k条序列），仅占100B语料库的0.08%，确保扰动本身不会显著改变训练数据分布。

**时序插入控制**：在时序实验中，扰动文本仅在训练的指定阶段（如前25%、前半段等）批量插入，用于研究“敏感数据在预训练过程中的插入时机”这一独立因果因素对记忆化的影响（§4）。

### 3.2 模型架构与评估协议

**模型架构**：HUBBLE模型基于Llama 3架构，主要修改包括：采用更小的OLMo分词器、解绑定权重的嵌入层、8B模型配置为36层（§3.2）。核心实验采用 $2 \times 2 \times 2$ 因子设计：模型规模 {1B, 8B} × 数据条件 {standard, perturbed} × 训练集大小 {100B, 500B}，共计8个模型。所有模型使用GPT-NeoX在标准超参数下训练（附录B）。

**记忆化评估协议**：通过三种方式评估记忆化（§3.3）：
1. **基于Loss的直接比较**：计算模型在成员与非成员文本上的长度归一化对数似然差异；
2. **基于Loss的选择题**：给定多个候选选项，模型选择loss最低的作为正确答案；
3. **生成式抽取**：通过提示引导模型逐token生成目标文本，衡量逐字复现能力。

### 3.3 公式说明

本文未引入新的理论公式。所有评估指标均采用标准的长度归一化对数似然（length-normalized log-likelihood）和ROC AUC等已有度量，具体实现遵循EleutherAI的lm-eval-harness框架。成员推理攻击的loss-based方法、MinK%及MinK%++等基线攻击的具体公式定义可参见其原始文献，本文仅将其作为评估工具使用。

## 实验与关键发现

### 核心发现：稀释效应与排序效应

HUBBLE的核心实验采用2×2×2因子设计（模型规模{1B, 8B} × 数据条件{standard, perturbed} × 训练数据量{100B, 500B}），系统性地揭示了两个影响LLM记忆化的因果机制。

**稀释效应**是第一个关键发现。Figure 2展示了8B模型在100B tokens与500B tokens训练条件下的记忆化对比：在相同的重复级别下，训练在500B tokens上的模型在所有领域的记忆化表现都更弱。这一结果直接验证了通过增大训练语料库来降低敏感数据相对频率的策略有效性。从机制上看，更大的语料库稀释了扰动文本在训练过程中的出现密度，使得模型对特定文本的记忆强度显著降低。

**排序效应**则通过时序插入实验得到验证。Figure 14显示，当扰动文本仅在训练的前四分之一阶段插入时，最终模型几乎不记忆这些数据；而仅在最后四分之一插入则导致最强的记忆化。这表明敏感数据在训练过程中的出现时机对记忆化强度有决定性影响——早期暴露的数据会随着后续训练被逐步"遗忘"，而晚期暴露的数据则被牢固记忆。

### 重复次数与记忆化强度的量化关系

重复次数是影响记忆化强度的最直接因素。Table 1报告了最大扰动模型（8B, 500B tokens）在Gutenberg Unpopular数据集上的成员推理攻击（MIA）结果：当重复次数从1增加到256时，基于Loss的MIA的ROC AUC从0.539（接近随机猜测）提升到1.0（完美区分）。这一从随机到完全可检测的转变，定量地证明了重复次数直接决定了隐私风险的可检测性。

![[assets/figures/papers/paper_list_l2_https_openreview_net_forum_id_ZfdnZhOP0k/figures/003_Table_1.jpg]]
*Table 1: ROC AUC scores of baseline MIAs on Gutenberg Unpopular for our largest perturbed model (8B, 500B tokens). Dup indicates the duplication level of members. Dup ̸= 0 treats all inserted perturbations as members. Non-members are always drawn from perturbations inserted 0 times. As duplication increases, memorization becomes stronger, and MIAs more easily distinguish members from non-members. See Appendix F for the full table and more HUBBLEMIA settings*

值得注意的是，并非所有攻击方法在高重复次数下都表现一致。Table 1还显示，MinK%++虽然在大多数情况下是最有效的攻击方法，但在高度重复的样本上并未达到100% AUC，而更简单的方法如Loss和MinK%反而能实现完美区分。这提示了不同MIA方法对重复次数的敏感度存在差异，需要在评估中综合考量。

### 模型规模与深度的调节作用

模型规模对记忆化有显著影响。Figure 19对比了1B和8B模型在相同500B tokens语料下的记忆强度：8B模型在更少的重复次数下就开始记忆数据，且整体记忆强度更高。这表明更大的模型容量为记忆化提供了更强的能力基础。

模型深度同样起调节作用。消融实验显示，32层的深窄模型比16层的基础模型记忆稍多，而8层的浅宽模型记忆更少。这一发现为理解Transformer架构中记忆化的层间分布提供了线索。

### 跨域干扰与语义记忆

HUBBLE通过训练仅包含单一风险域扰动的1B模型，验证了多域扰动之间的干扰极小。Figure 20显示，核心多域扰动模型在每一域的表现与仅训练单一域扰动的模型几乎一致。这意味着研究者可以在同一个模型中同时研究版权、隐私和测试集污染等多个记忆化问题，而无需担心跨域混淆。

关于语义记忆，Figure 15揭示了改写数据训练的独特行为：模型无法将记忆从改写示例泛化到原始示例，但仍能通过较强的攻击方式重建PII。这表明模型形成了某种语义层面的记忆，虽然不等同于逐字记忆，但在隐私保护方面仍构成实质性风险。这一发现对依赖数据改写作为隐私保护手段的做法提出了警示。

### 遗忘与持续暴露的动态过程

时序实验还揭示了记忆化的动态特性。若在训练中途停止注入扰动，模型会随后续训练逐步遗忘已记忆的数据。这一"自然遗忘"现象为机器遗忘技术提供了基准参考——有效的遗忘方法应当显著超越这种被动遗忘的速率和程度。

### 方法公平性保障

所有实验在公平性方面做了严格控制：扰动模型与标准模型共享相同的训练超参数，排除了数据因素之外的其他干扰；扰动模型在通用基准上的表现与其他同等规模的开源模型相当（Table 6, Table 7），排除了数据插入导致通用能力退化的可能；MIA实验中的成员/非成员集合来源于随机分配的重复次数，消除了时间戳等假性特征对推理结果的混淆。

![[assets/figures/papers/paper_list_l2_https_openreview_net_forum_id_ZfdnZhOP0k/figures/009_Table_6.jpg]]
*Table 6: Five-shot benchmark results using the Pythia suite. Five-shot benchmark results on models of comparable size and training token budgets $\mathbf { ( \leq 5 0 0 B ) }$ and also include OLMo and Llama models. We use the same evaluations as the Pythia suite and run them through EleutherAI’s Language Model Evaluation Harness (Gao et al., 2023). ∗Token counts are based on the model’s documentation and may use different tokenizers. #Winogrande and PIQA train sets are inserted in the perturbed HUBBLE corpus

![[assets/figures/papers/paper_list_l2_https_openreview_net_forum_id_ZfdnZhOP0k/figures/010_Table_7.jpg]]
*Table 7: Benchmark results using the DCLM v1 eval suite. DCLM-BASELINE and FineWeb edu results are copied from the official DCLM leaderboard. In general, Hubble models perform on par within their respective data and model scales*

### 局限性认知

需要指出的是，HUBBLE模型虽然达到8B参数、500B tokens的训练规模，但仍远小于商业LLM（如Llama 3的15T tokens）。稀释效应在更大数据量下的表现有待进一步验证。此外，稀释和排序仅是缓解策略，不能完全消除版权或隐私风险——某些高度重复的攻击仍可成功。

### 补充图表

![[assets/figures/papers/paper_list_l2_https_openreview_net_forum_id_ZfdnZhOP0k/figures/030_Figure_17.jpg]]
*Figure 17: Unlearning results on Gutenberg Unpopular. Unlearning results using (out-of-domain, unseen) Wikitext (lower row) and (in-domain, seen) Keep set (upper row) as the retain sets. None of the unlearning methods simultaneously achieve the target behavior on both the seen Keep set (left column) and the unseen Test set (right column)*

![[assets/figures/papers/paper_list_l2_https_openreview_net_forum_id_ZfdnZhOP0k/figures/031_Figure_18.jpg]]
*Figure 18: Unlearning results on YAGO biographies. Unlearning results using (out-of-domain, unseen) Wikitext (lower row) and (in-domain, seen) Keep set (upper row) as the retain sets. None of the unlearning methods simultaneously achieve the target behavior on both the seen Keep set (left column) and the unseen Test set (right column)*

![[assets/figures/papers/paper_list_l2_https_openreview_net_forum_id_ZfdnZhOP0k/figures/005_Table_2.jpg]]
*Table 2: HUBBLE perturbation datasets on Hugging Face, grouped by domain and data type. Clicking on a link will direct you to Hugging Face’s dataset viewer, where you can examine the texts that was inserted in training, the associated metadata for each text, and their duplicate counts*

![[assets/figures/papers/paper_list_l2_https_openreview_net_forum_id_ZfdnZhOP0k/figures/006_Table_3.jpg]]
*Table 3: Percentage of training data overwritten by duplicated perturbation data. These calculations depend on the selected sequence length of 2048 tokens and training batch size of 1024 sequences*

![[assets/figures/papers/paper_list_l2_https_openreview_net_forum_id_ZfdnZhOP0k/figures/007_Table_4.jpg]]
*Table 4: Hubble model configuration*

![[assets/figures/papers/paper_list_l2_https_openreview_net_forum_id_ZfdnZhOP0k/figures/008_Table_5.jpg]]
*Table 5: Zero-shot benchmark results using the Pythia suite. We report results for models of comparable size and training token budgets (≤ 500B) and also include OLMo and Llama models. We use the same evaluations as the Pythia suite and run them through EleutherAI’s Language Model Evaluation Harness (Gao et al., 2023). ∗Token counts are based on the model’s documentation and may use different tokenizers*

![[assets/figures/papers/paper_list_l2_https_openreview_net_forum_id_ZfdnZhOP0k/figures/017_Table_9.jpg]]
*Table 9: Indirect PII Attack Defitions. The instantiated indirect PII inference attacks are listed below. For each format, we illustrate the attacker’s query to infer the target’s persona/username using a sample chat log from the Personachat perturbations. Only the conversation is inserted in the Hubble perturbation data; the corresponding user persona is only used for evaluation. Candidates are drawn from other examples in the dataset*

![[assets/figures/papers/paper_list_l2_https_openreview_net_forum_id_ZfdnZhOP0k/figures/026_Table_10.jpg]]
*Table 10: ROC AUC scores of baseline MIAs for the HUBBLE 8B (500B tokens) perturbed model. Dup indicates the duplication level of members. Dup ̸= 0 treats all inserted perturbations as members. Non-members are always drawn from perturbations inserted 0 times. As duplication increases, memorization becomes stronger, and it becomes easier for membership inference attacks (MIA) to distinguish between members and non-members*

## 定位与知识库关联

### 核心贡献与问题定位

Hubble 的核心贡献并非提出一种新的记忆化缓解算法，而是构建了一套**可控因果实验平台**，解决了该领域长期存在的瓶颈：现有 LLM 记忆化研究难以在大型模型上进行受控实验，导致抽样观察无法有效分离重复频率、文本简单性、训练数据规模等混淆因素，许多因果量（如“需要多少次重复才能记住一段文本”）无法被可靠估计。

Hubble 通过两个可独立操纵的因果旋钮——**训练语料库大小**和**敏感数据插入时机**——使得研究者能够精确量化这些因素对记忆强度的因果效应，而非仅报告相关性。

### 方法设计：受控扰动插入框架

Hubble 的方法核心在于“扰动模型”（perturbed model）的构造流程，该流程包含以下关键模块：

1.  **基础语料库与去污染**：采用 DataComp-LM（DCLM; Li et al., 2024a）提供的高质量英文语料作为预训练基础，并预先移除与任何扰动文本匹配的训练文档，确保插入的重复次数精确反映实际训练中的暴露频率。
2.  **扰动文本插入**：将预先设计的版权、隐私、测试集污染等敏感数据以模拟真实文档的方式拼接到训练序列中（Figure 1）。每条扰动数据被随机分配重复次数 {0×, 1×, 4×, 16×, 64×, 256×}，总量仅占 100B 语料的 0.08%（79.9M tokens），避免对通用能力造成显著干扰。
3.  **时序控制**：在时序实验中，扰动数据仅在指定的训练阶段（如前 25%、前半段等）插入，用于研究暴露时机对记忆化的影响。
4.  **模型架构与训练**：基于 Llama 3 架构改造（OLMo 分词器、解绑定权重的嵌入、8B 模型 36 层等），使用 GPT-NeoX 在标准超参数下训练，确保除数据因素外其他条件一致。
5.  **记忆化评估协议**：通过三种方式评估记忆化——基于 loss 的直接比较、loss-based 的选择题、生成式抽取——覆盖所有插入数据类型。

核心实验采用 2×2×2 因子设计：模型规模 {1B, 8B} × 数据条件 {standard, perturbed} × 训练集大小 {100B, 500B}，共 8 个模型。

### 与现有工作的关系

Hubble 并非与某个具体基线方法对标，而是为整个 LLM 记忆化研究社区提供基础设施。其定位与以下方向形成互补：

-   **观察性研究**：此前的工作多基于对已训练模型的事后抽样观察（如从 CommonCrawl 中检测重复文本），难以建立因果关系。Hubble 通过随机化插入设计，将观察性问题转化为可干预的实验问题。
-   **记忆化缓解方法**：Hubble 本身不提出新的缓解算法，但为评估梯度上升、差分隐私训练、知识编辑、机器遗忘等方法提供了标准化的因果测试床。论文第 6.2 节即展示了如何利用 Hubble 构建遗忘基准：将 256 次重复的扰动数据的一半作为遗忘集，另一半作为保留集，二者来自同一分布，要求方法在移除目标的同时保持邻接样本的性能。
-   **成员推理攻击（MIA）研究**：Hubble 提供了已知真实成员/非成员标签的模型，消除了时间戳等假性特征对推理结果的混淆，使得 MIA 方法的评估更加纯粹。

### 适用边界与局限

Hubble 的结论和方法适用性存在以下边界：

1.  **规模限制**：Hubble 模型最大为 8B 参数、500B tokens，远小于商业 LLM（如 Llama 3 的 15T tokens）。稀释效应在更大数据量下的表现需要进一步验证，不能直接外推至超大规模模型。
2.  **缓解而非消除**：稀释和前置排序仅是缓解策略，不能完全消除版权或隐私风险。实验显示，在高度重复（如 256 次）下，成员推理攻击的 ROC AUC 仍可达 1.0，表明极端情况下的风险依然存在。
3.  **扰动类型覆盖有限**：实验中的扰动类型主要覆盖书籍段落、传记和测试集，而训练数据中其他形式的敏感信息（如代码、医疗记录、个人对话等）未包含在内，结论的泛化性需要进一步验证。
4.  **架构单一**：模型架构仅基于 Llama 3，未探索其他流行架构（如混合专家模型）下记忆化的规律。
5.  **评估指标的局限性**：当前使用的 loss-based 和生成式评估主要捕捉逐字记忆，对语义记忆的量化仍不够充分。改写数据训练实验（Figure 15）表明，模型虽不逐字记忆原始文本，但仍能通过较强攻击方式重建 PII，说明语义记忆构成独立的风险维度，但现有指标难以精确度量。

### 开放问题

Hubble 揭示或未能解决的开放问题包括：

1.  **记忆的机制层面**：信息在 Transformer 中究竟是如何被存储和检索的？理解其机制有助于改进知识编辑和机器遗忘技术。
2.  **记忆的度量**：如何设计更直观、鲁棒的量化记忆化指标，以应用于版权和隐私的实际法律判断？当前的 loss 和生成准确率指标与法律意义上的“侵权”之间仍存在鸿沟。
3.  **缓解方法的互补性**：除稀释和排序外，还有哪些方法（如量化、差分隐私训练、数据去重策略）能够与现有最佳实践互补，形成多层防御体系？
4.  **语义记忆的风险评估**：改写数据训练形成的语义记忆在多大程度上构成与逐字记忆同等的风险？法律和技术上应如何评估这种“非逐字但可重建”的记忆形式？
5.  **跨领域泛化**：不同领域（版权、隐私、测试集污染）的扰动之间干扰极小（Figure 20），这一发现的机理是什么？是否意味着不同敏感信息类型的记忆化机制是相对独立的？

## 原文 PDF

![[paperPDFs/ICLR_2026/Hubble_a_Model_Suite_to_Advance_the_Study_of_LLM_Memorization.pdf]]
