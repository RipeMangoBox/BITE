---
title: "EditBench: Evaluating LLM Abilities to Perform Real-World Instructed Code Edits"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/EditBench_Evaluating_LLM_Abilities_to_Perform_Real_World_Instructed_Code_Edits.pdf
project_link: https://waynechi.com/edit-bench/
code_link: https://github.com/waynchi/editbench
openreview_forum_id: FtL9eEmU6v
aliases:
- EditBench
tags:
- ICLR_2026
- topic/benchmarks_datasets_evaluation
- topic/benchmarks_datasets_evaluation/benchmark_eval
core_operator: "通过VSCode扩展从真实开发者收集指令与代码上下文，保留高亮代码和光标位置等丰富上下文信息，构建了一个更具现实性和挑战性的基准。"
primary_logic: "EditBench揭示了真实世界代码编辑任务的多模态、多语言和高度的上下文依赖性，这些特性在现有基准中被忽略，因此成为评估LLM编辑能力的关键差距。"
claims:
- "EditBench基于真实用户通过VSCode扩展编写的指令和代码上下文构建，包含高亮代码和光标位置。"
- "40个模型中仅1个（claude-sonnet-4）在EditBench上获得超过60%的pass@1，表明基准极具挑战性。"
- "添加高亮代码后7个模型中的5个性能提升，但添加光标位置带来混合效果，说明上下文信息对真实编辑任务的影响。"
- "EditBench与现有基准（Aider Polyglot和Chatbot Arena）仅呈弱正相关，证明其捕捉了独特的实际挑战。"
---

# EditBench: Evaluating LLM Abilities to Perform Real-World Instructed Code Edits

> [!tip] 核心洞察
> EditBench揭示了真实世界代码编辑任务的多模态、多语言和高度的上下文依赖性，这些特性在现有基准中被忽略，因此成为评估LLM编辑能力的关键差距。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | EditBench：评估大语言模型执行真实世界指令代码编辑的能力 |
| 英文题名 | EditBench: Evaluating LLM Abilities to Perform Real-World Instructed Code Edits |
| 会议/期刊 | ICLR 2026 (Oral) |
| Links | [paper](https://openreview.net/forum?id=FtL9eEmU6v) · [GitHub](https://github.com/waynchi/editbench) · [Project](https://waynechi.com/edit-bench/) |
| Topic | #topic/benchmarks_datasets_evaluation #topic/benchmarks_datasets_evaluation/benchmark_eval |
| Method | EditBench |
| Dataset | EditBench, EditBench (任务类别平均), 与现有基准的相关性 |

> [!tip] 效果简介
> - EditBench 上，pass@1 (最高闭源 vs 最佳开源) 为 claude-sonnet-4: 66.67%，对比 glm-4.6: 56.48%，变化 +10.19%。
> - EditBench (任务类别平均) 上，平均 pass@1 为 Bug fixing: 52.2%, Optimization: 44.6%, Feature addition: 39.6%，对比 N/A，变化 N/A。
> - 与现有基准的相关性 上，Pearson r 为 Aider Polyglot: 0.24 (p=0.06)，对比 Chatbot Arena: 0.11 (p=0.01)，变化 N/A。

## 概要

### 问题瓶颈

现有代码编辑基准（如 **CanItEdit** (Cassano et al., 2023b)、**EditEval** (Hu et al., 2023)、**Aider Polyglot** (Gauthier, 2025)）依赖人工标注者编写的简单任务或编程练习题，无法反映真实开发场景中用户指令的**模糊性、多语言性和高度上下文依赖性**。真实用户在IDE中编写的指令往往简短且隐含意图，需要模型结合高亮代码区域和光标位置等丰富上下文信息来解析编辑需求，而现有基准完全忽略了这些关键要素。

### 核心方法定位

**EditBench** 通过开发一个开源VSCode扩展（Figure 2），从真实开发者处收集“in-the-wild”的指令和代码上下文，构建了首个包含**高亮代码和光标位置**的指令代码编辑基准。该基准涵盖5种自然语言（英语、西班牙语、俄语、汉语、葡萄牙语）和2种编程语言（Python、JavaScript），共540个问题。每个问题由经验丰富的程序员编写测试用例，并在Docker容器中隔离评估。

### 关键发现

1. **基准极具挑战性**：在40个被评估的大语言模型中，仅 **claude-sonnet-4** 获得超过60%的pass@1（66.67%），闭源模型整体优于开源模型（Figure 4）。
2. **上下文信息影响显著**：添加高亮代码后，7个模型中的5个性能提升；但添加光标位置带来混合效果，表明上下文信息的利用仍是不稳定因素（Table 3）。
3. **与现有基准弱相关**：EditBench与Aider Polyglot（r=0.24, p=0.06）和Chatbot Arena（r=0.11, p=0.01）仅呈弱正相关，证明其捕捉了现有基准未能覆盖的独特实际挑战。
4. **任务类别差异明显**：模型在bug fixing任务上表现最好（平均52.2%），而在optimization（44.6%）和feature addition（39.6%）任务上较弱。

代码编辑是大语言模型（LLM）在真实开发工作流中最核心的应用场景之一。开发者不再仅仅依赖模型从零生成代码，而是越来越多地在集成开发环境（IDE）中向模型发出自然语言指令，要求其对已有代码进行修改、修复或增强。GitHub Copilot 和 Cursor 等工具已将这一“指令式代码编辑”（instructed code editing）功能作为核心特性推向市场，然而，如何可靠地评估 LLM 在这一场景下的真实能力，仍然是一个悬而未决的问题。

### 现有基准的关键缺口

当前主流的代码编辑评估基准，如 **CanItEdit**（Cassano et al., 2023b）、**EditEval**（Hu et al., 2023）和 **Aider Polyglot**（Gauthier, 2025），在问题来源和任务设计上存在根本性局限。它们的问题通常由标注者人工编写，或从编程练习题库中抽取，具有以下共同缺陷：

1. **指令过于精确和完备**：标注者编写的指令往往详尽地描述了期望的修改行为，这与真实开发中用户给出的模糊、简短且高度依赖上下文的自然语言指令形成鲜明对比。例如，真实指令可能是“改成支持流式响应”，而非“在 `response_handler` 函数中添加 `stream=True` 参数并修改返回逻辑”。

2. **缺乏丰富的代码上下文**：现有基准通常只提供待编辑的代码文件，而忽略了开发者在 IDE 中实际拥有的上下文信息——尤其是**高亮选中的代码区域**和**当前光标位置**。这些信息是模型解析用户意图、定位编辑范围的关键线索。

3. **语言和库的多样性不足**：现有基准通常局限于单一自然语言（英语）和少量标准库，无法反映真实开发中多语言用户群体和多样化第三方库依赖的复杂性。

### 核心瓶颈

综上，**现有代码编辑基准的核心瓶颈在于：它们依赖人工编写的简单任务或编程练习题，无法反映真实开发中用户指令的模糊性、多样性，以及依赖代码上下文（高亮区域和光标位置）解析意图的需求。** 这导致基准评估结果与模型在实际 IDE 中的表现之间存在显著脱节。

### 本文动机

为填补这一评估鸿沟，本文提出 **EditBench**——首个基于真实世界 IDE 交互数据构建的指令式代码编辑基准。EditBench 通过开发一个模仿 Copilot 和 Cursor 编辑功能的 VSCode 扩展，从真实开发者处收集用户编写的指令、关联的代码上下文（包括高亮代码和光标位置），以及用户对模型响应的偏好投票。这一设计使得 EditBench 能够捕捉真实编辑任务的三个关键特性：**多模态上下文依赖性**、**多自然语言覆盖**（涵盖英语、西班牙语、俄语、汉语、葡萄牙语 5 种语言），以及**高度的任务多样性**（涵盖 Bug 修复、功能添加、代码优化和修改等类别）。

通过构建这样一个“野外”（in-the-wild）基准，EditBench 旨在揭示当前 LLM 在真实代码编辑场景中的真实能力上限，并为未来模型改进提供更具生态效度的评估标尺。

## 核心方法与创新机理

EditBench 的核心创新在于**将代码编辑评估从人工标注的简化任务迁移到真实开发场景**，通过三个关键设计填补了现有基准与真实世界之间的鸿沟。

### 1. 真实世界数据采集

现有代码编辑基准（如 **CanItEdit** (Cassano et al., 2023b)、**EditEval** (Hu et al., 2023)、**Aider Polyglot** (Gauthier, 2025)）依赖标注者编写指令或使用编程练习题，这些任务通常高度明确、缺乏上下文依赖性。EditBench 通过开发一个开源 VSCode 扩展，从真实开发者的日常工作中采集指令和代码上下文，构建了首个基于 in-the-wild 数据的代码编辑基准。这一转变使问题天然携带真实场景的特征：指令模糊、依赖代码上下文来解析意图，且涵盖多样化的编辑需求。

### 2. 丰富的上下文信息

EditBench 首次在评估中系统性地引入**高亮代码区域**和**光标位置**作为上下文信息。这些信息在真实 IDE 编辑工具（如 GitHub Copilot、Cursor）中普遍存在，但现有基准完全忽略。消融实验证实了这一设计的价值：添加高亮代码后，7 个模型中的 5 个 pass@1 得到提升，说明模型确实能利用高亮区域缩小编辑范围、推断用户意图。

### 3. 多语言扩展

EditBench 包含 5 种自然语言（英语、西班牙语、俄语、汉语、葡萄牙语）的指令，远超现有基准仅支持英语的局限。通过 GPT-4o 翻译评论构建 EditBench-complete（共 540 个问题），使得基准能够评估模型在非英语指令下的代码编辑能力，更贴近全球化的真实开发环境。

### 创新验证

这些设计带来的挑战性得到了实证支持：40 个模型中仅 claude-sonnet-4 获得超过 60% 的 pass@1，且 EditBench 与 Aider Polyglot（r = 0.24, p = 0.06）和 Chatbot Arena（r = 0.11, p = 0.01）仅呈弱正相关，证明其捕捉了现有基准无法反映的独特能力维度。

![[assets/figures/papers/paper_list_l44_https_openreview_net_forum_id_FtL9eEmU6v/figures/001_Figure_1.jpg]]
*Figure 1: EditBench tests LLMs’ real-world editing capabilities. We propose EditBench, an evaluation on real user instructions and code snippets collected in-the-wild. It is the first benchmark for instructed code edits that requires models to ingest the user instruction, current code, highlighted code, and cursor position to solve problems*

![[assets/figures/papers/paper_list_l44_https_openreview_net_forum_id_FtL9eEmU6v/figures/003_Table_1.jpg]]
*Table 1: Comparing EditBench to other edit-related benchmarks. We compare EditBench with similar benchmarks (CanItEdit (Cassano et al., 2023b), EditEval (Hu et al., 2023), Aider Polyglot) in terms of the problem source, user instruction (# NL refers to the number of natural languages), code context (# PL refers to the number of programming languages, HL refers to whether users can highlight a subset of code), and associated test cases. Standard deviation is indicated by ±. EditBench is the only benchmark built from in-the-wild problems and exhibits considerable variation in both instruction and code context length*

![[assets/figures/papers/paper_list_l44_https_openreview_net_forum_id_FtL9eEmU6v/figures/005_Table_2.jpg]]
*Table 2: Comparing user instructions written in IDE to the instructions written by human annotators. We provide examples across different task categories, comparing with two edit-related datasets (CanItEdit (Cassano et al., 2023b) and EditEval (Hu et al., 2023)). We truncate some instructions for brevity and provide full examples in Appendix B. In general, we find that real-world prompts are much less specified and require models to leverage the provided context, compared to existing benchmark prompts*

### 核心设计动机

现有代码编辑基准（如 **CanItEdit** (Cassano et al., 2023b)、**EditEval** (Hu et al., 2023)、**Aider Polyglot** (Gauthier, 2025)）依赖标注者编写的简单任务或编程练习题，无法反映真实开发场景中用户指令的模糊性、多语言性和对代码上下文（高亮区域、光标位置）的深度依赖。EditBench 的核心设计目标正是填补这一差距——构建首个基于真实 IDE 环境、保留完整编辑上下文的指令代码编辑基准。

### 整体 Pipeline

EditBench 的构建与评估流程由五个紧密衔接的模块组成，形成从数据收集到模型评测的闭环：

| 阶段 | 模块 | 输入 | 输出 | 核心作用 |
|------|------|------|------|----------|
| 1 | VSCode 扩展数据收集 | 开发者自然编辑行为 | 原始指令-代码上下文对 | 捕获真实世界的编辑意图 |
| 2 | 问题筛选与去重 | 原始数据 | 高质量问题集（109 个） | 去除相似、琐碎、风格化或模糊的问题 |
| 3 | 测试用具编写 | 筛选后的问题 | 可执行测试用例 | 将用户意图转化为可验证的通过/失败标准 |
| 4 | 多语言翻译 | 英文问题 | EditBench-complete（540 个问题） | 扩展至 5 种自然语言 |
| 5 | Docker 化评估 | 模型生成代码 | pass@1 指标 | 隔离环境中执行测试并量化性能 |

#### 模块 1：VSCode 扩展数据收集

研究团队开发了一个开源 VSCode 扩展，模仿 GitHub Copilot 和 Cursor 的指令代码编辑功能。开发者在日常编码中使用该扩展时，系统自动收集三类关键信息：

- **用户自然语言指令**：开发者以自然语言描述的编辑意图
- **代码上下文**：待编辑的完整代码文件
- **高亮代码区域**：用户在发出指令前选中的代码片段
- **光标位置**：用户当前的光标所在位置

这种设计使得 EditBench 成为**唯一一个捕获高亮代码和光标位置**的代码编辑基准（Table 1），这两个上下文信息被证明对模型理解真实用户意图至关重要。

#### 模块 2：问题筛选与去重

从原始收集数据中，筛选过程遵循三条原则：
1. **语言聚焦**：仅保留 Python 和 JavaScript 问题
2. **去重**：排除过于相似的问题
3. **质量过滤**：移除琐碎问题（如添加单个参数）、纯风格问题（如添加注释）或意图模糊的问题

最终保留 **109 个独特问题**，这些问题展现出显著的多样性——仅 Python 问题就涉及 **74 个独特的导入库**（Figure 3），远超 CanItEdit（25 个）、Polyglot（15 个）和 EditEval（16 个）。

#### 模块 3：测试用具编写

由五名经验丰富的程序员组成的团队负责为每个问题编写测试用例。标注者利用高亮代码段和光标位置作为关键上下文线索，推断用户真实意图，确保测试用例准确反映用户期望的行为。值得注意的是，论文明确指出当前模型尚无法可靠地自动生成测试用具，因此这一环节仍依赖人工标注。

#### 模块 4：多语言翻译

为评估模型在多语言场景下的表现，使用 GPT-4o 将每个问题的注释翻译为数据集中出现的其他自然语言（西班牙语、俄语、汉语、葡萄牙语），形成 **EditBench-complete**，总计 **540 个问题**（109 个原始问题 × 5 种语言，部分问题原始即为非英语）。翻译方法参考了 HumanEval-XL (Peng et al., 2024) 的做法。

#### 模块 5：Docker 化评估

所有评估在 Docker 容器中运行，确保环境隔离和可复现性。评估采用代码生成领域标准的 **pass@1** 指标：每个问题生成 1 个代码样本，若通过所有单元测试则视为解决。

### 输入输出流

**模型输入**由四部分上下文组成：
1. 用户自然语言指令
2. 待编辑的完整代码文件
3. 高亮代码区域（可选）
4. 光标位置（可选）

**模型输出**为编辑后的完整代码文件。

**评估输出**为 pass@1 分数，按问题难度（Easy/Hard）和任务类别（Bug Fixing、Feature Addition、Feature Modification、Optimization）进行细分。

### 与现有基准的关键差异

Table 1 系统对比了 EditBench 与三个现有基准的差异：

| 维度 | CanItEdit | EditEval | Aider Polyglot | **EditBench** |
|------|-----------|----------|----------------|---------------|
| 问题来源 | 标注者编写 | 标注者编写 | 编程练习 | **真实 IDE 用户** |
| 自然语言数 | 1 | 1 | 1 | **5** |
| 编程语言数 | 1 | 1 | 多语言 | 2 |
| 高亮代码支持 | ✗ | ✗ | ✗ | **✓** |
| 光标位置支持 | ✗ | ✗ | ✗ | **✓** |

Table 2 进一步通过实例展示了真实 IDE 指令与标注者编写指令的本质差异：真实指令更简短、更模糊，高度依赖代码上下文来推断意图。例如，EditBench 中一个典型的 Feature Addition 指令仅为 “Can you edit this to work with streaming responses?”，而现有基准的同类指令则通常包含详细的功能描述和参数说明。这种模糊性正是 EditBench 挑战性的核心来源。

### 关键模块

EditBench 的构建与评估流程由以下核心模块组成：

1. **VSCode 扩展数据收集**：开发了一个开源 VSCode 扩展，将指令式代码编辑作为核心功能，在开发者使用时实时收集用户编写的指令、关联的代码上下文（包括高亮代码区域和光标位置）以及用户对模型响应的投票。这是 EditBench 区别于所有现有基准的关键模块。

2. **问题筛选与去重**：聚焦 Python 和 JavaScript 问题，排除过于相似、琐碎（如添加单个参数）、风格化（如添加注释）或意图模糊的问题，确保基准问题的质量和挑战性。

3. **测试用具编写**：由五名在自然语言和编程语言方面均有经验的专业程序员组成团队，根据用户意图编写测试用例和测试环境。标注者利用高亮代码段和光标位置作为关键上下文线索来推断用户意图。

4. **多语言翻译**：使用 GPT-4o 将每个问题中的注释翻译为其他语言（遵循 HumanEval-XL 的方法），将原始 109 个独特问题扩展为覆盖 5 种自然语言（英语、西班牙语、俄语、汉语、葡萄牙语）的 540 个问题，形成 EditBench-complete。

5. **评估环境 Docker 化**：所有评估在 Docker 容器内运行，使用编码代理（coding agent）设置测试用具环境，提供标准化配置文件（如 Python 的 `conftest.py` 和 JavaScript 的 `jest-config.js`）以支持代理并统一输出格式。

### 关键公式

本文未引入新的数学公式或推导。评估指标采用标准的 pass@1，定义为每个问题生成 1 个代码样本，若该样本通过所有单元测试则视为解决：

$$\text{pass@1} = \frac{\text{通过所有测试的问题数}}{\text{总问题数}}$$

难度分类采用阈值法：将少于等于 k 个模型解决的问题归类为 Hard，其余为 Easy。为获得大致均分的划分，选取 k = 20。

相关性分析使用 Pearson 相关系数 r 衡量 EditBench 与现有基准（Aider Polyglot、Chatbot Arena）之间的线性关联强度。

## 实验与关键发现

### 主要结果：EditBench 对当前 LLM 构成严峻挑战

论文在 EditBench 上评估了 40 个 LLM，涵盖闭源与开源、推理与非推理等多种模型家族（完整列表见 Table 6）。评估采用 pass@1 指标：每个问题生成 1 个代码样本，通过所有单元测试即视为解决。

![[assets/figures/papers/paper_list_l44_https_openreview_net_forum_id_FtL9eEmU6v/figures/020_Table_6.jpg]]
*Table 6: Each model in our experiments with their official names and provider links*

核心发现：**仅 1 个模型（claude-sonnet-4）的 pass@1 超过 60%，达到 66.67%**（Figure 4）。整体而言，闭源模型普遍优于开源模型，最佳开源模型 glm-4.6 的 pass@1 为 56.48%，差距约 10 个百分点。这一结果直接验证了 EditBench 作为基准的挑战性——现有模型在真实世界的指令代码编辑任务上仍有巨大提升空间。

按问题难度分层后，差距更为显著：将少于 20 个模型解决的问题定义为"困难"类别后，模型在简单与困难问题间的平均 pass@1 差距高达 59.3%（Figure 4）。

### 任务类别分析：Bug 修复相对容易，功能添加最难

按编辑类别细分，模型表现呈现明显梯度（Figure 5）：

- **Bug 修复**：平均 pass@1 最高，达 52.2%
- **代码优化**：平均 44.6%
- **功能添加**：平均最低，仅 39.6%

这一排序与直觉相符：Bug 修复通常有明确的错误行为作为锚点，而功能添加和优化需要模型在理解模糊意图的同时进行创造性代码生成，对上下文推理能力要求更高。值得注意的是，不同模型在不同类别上各有所长，不存在单一模型在所有类别上全面领先（Figure 5）。

### 上下文消融：高亮代码是关键，光标位置效果混合

为量化代码上下文信息对编辑性能的影响，论文对 7 个 top 模型进行了消融实验（Table 3），比较四种提示条件：

![[assets/figures/papers/paper_list_l44_https_openreview_net_forum_id_FtL9eEmU6v/figures/007_Table_3.jpg]]
*Table 3: Additional context affects performance. Highlighted code is crucial to performance, improving task success rate across 5 out 7 models when included in the prompt. Surprisingly, adding cursor position leads to mixed results. Models chosen are the best model in the top 7 model families*

| 条件 | 效果 |
|------|------|
| 仅代码（基线） | — |
| +高亮代码 | 5/7 模型 pass@1 提升 |
| +仅光标位置 | 效果混合 |
| +高亮+光标 | 与仅高亮相比无明显增益 |

**高亮代码被证明是提升性能的关键上下文信息**，7 个模型中 5 个在添加高亮后 pass@1 提高。然而，添加光标位置的效果出人意料地混合，部分模型甚至出现性能下降。这表明当前模型在利用光标位置这一细粒度空间信息方面尚不成熟，可能将其视为噪声而非有效信号。

### 上下文长度与问题难度

Table 7 揭示了上下文长度与性能的反向关系：

![[assets/figures/papers/paper_list_l44_https_openreview_net_forum_id_FtL9eEmU6v/figures/023_Table_7.jpg]]
*Table 7: Effect of context length on average pass@1*

- **短上下文（<1k 字符）**：平均 pass@1 71.03%
- **中等上下文（1k–3k 字符）**：62.09%
- **长上下文（>3k 字符）**：59.94%

进一步分析困难与简单问题的特征差异（Table 8）发现：困难问题的指令长度显著更短（约 75 字符），但高亮代码长度与简单问题相近。这暗示困难的核心不在于代码量，而在于**指令本身的模糊性**——简短指令要求模型从代码上下文中推断用户真实意图，这对模型的上下文推理能力提出了更高要求。

### 与现有基准的相关性分析

EditBench 与现有代码编辑基准仅呈弱正相关：

- 与 Aider Polyglot 的 Pearson r = 0.24（p = 0.06）
- 与 Chatbot Arena 的 Pearson r = 0.11（p = 0.01）

这种弱相关性证明 EditBench 捕捉了现有基准未能覆盖的独特挑战维度——真实世界的指令模糊性、多语言特性和丰富的代码上下文依赖。换言之，在传统基准上表现优异的模型未必能胜任真实 IDE 中的代码编辑任务。

### 失败模式分析

综合以上结果，当前 LLM 在 EditBench 上的主要失败模式可归纳为：

1. **模糊指令理解失败**：困难问题的指令更短、更依赖上下文，模型难以从高亮代码和文件中准确推断用户意图。
2. **光标位置利用不足**：消融实验表明光标位置信息未能被有效利用，模型缺乏将空间位置映射到编辑操作的机制。
3. **复杂编辑类型薄弱**：功能添加和优化类任务需要多步推理和创造性代码生成，当前模型在这类开放式编辑上表现最差。
4. **长上下文退化**：随着代码上下文增长，模型性能持续下降，反映出长距离依赖建模的不足。

## 定位与知识库关联

### 与现有基准的关系

EditBench 的定位源于对现有代码编辑基准的批判性审视。主流基准如 **CanItEdit**（Cassano et al., 2023b）和 **EditEval**（Hu et al., 2023）依赖标注者编写的人工任务或编程练习题，其指令通常明确、结构化，缺乏真实开发场景中用户指令的模糊性和上下文依赖性。**Aider Polyglot**（Gauthier, 2025）同样基于人工构建的问题。Table 1 的系统对比揭示了 EditBench 在三个维度上的根本差异：

- **问题来源**：EditBench 是唯一从真实用户（in-the-wild）收集问题的基准，而其他基准均依赖标注者编写。
- **自然语言多样性**：EditBench 覆盖5种自然语言（英语、西班牙语、俄语、汉语、葡萄牙语），而现有基准仅支持英语。
- **代码上下文信息**：EditBench 首次引入高亮代码区域和光标位置作为模型输入，这是现有基准完全缺失的维度。

从库依赖的多样性来看，EditBench 的 Python 问题包含74个独特导入，远超 CanItEdit（25个）、Polyglot（15个）和 EditEval（16个），表明其覆盖了更广泛的真实开发场景（Figure 3）。

### 因果机制与核心洞察

EditBench 的设计回应了一个关键瓶颈：**现有基准无法反映真实代码编辑中用户指令的模糊性、多语言性和对代码上下文（高亮区域、光标位置）的解析需求**。Table 2 的对比示例直观展示了这一差距——真实 IDE 指令往往简短且依赖上下文推理（如"Can you edit this to work with streaming responses?"），而标注者编写的指令则详尽且自包含。

这一设计选择的因果效应在实验中得到了验证：
- **弱相关性证据**：EditBench 与 Aider Polyglot 的 Pearson 相关系数仅为 $r=0.24$（$p=0.06$），与 Chatbot Arena 仅为 $r=0.11$（$p=0.01$），表明 EditBench 捕捉了现有基准无法测量的独特能力维度。
- **上下文消融证据**：Table 3 显示，添加高亮代码后7个模型中的5个 pass@1 提升，但添加光标位置带来混合效果，说明上下文信息的利用方式对模型性能有显著且非单调的影响。

### 适用边界

EditBench 的适用性受以下因素约束：

1. **编程语言覆盖有限**：目前仅包含 Python 和 JavaScript，且 JavaScript 问题数量有限，无法代表所有真实开发场景。
2. **自然语言覆盖的扩展方式**：EditBench-complete 的540个问题中，非英语问题通过 GPT-4o 翻译生成，而非原生收集，可能引入翻译偏差。
3. **基准规模**：核心的109个独特问题经过翻译扩展至540个，但相对于真实世界的多样性仍有限。
4. **评估指标单一**：仅使用 pass@1 作为成功标准，未考虑编辑的部分正确性或代码风格质量。

### 局限与开放问题

**已识别的局限**：
- **数据污染风险**：未来模型可能无意中在 EditBench 问题上训练，尽管已采取预防措施，仍需持续更新问题以减轻影响。
- **测试用具生成瓶颈**：当前模型尚无法可靠理解真实用户意图以自动生成测试用例，限制了基准的扩展速度。实验表明，即使使用 coding agent 辅助，仍需5名经验丰富的程序员手动编写测试用具。

**关键开放问题**：
1. 如何实现完全自动化的测试用具生成，使 EditBench 能随真实数据流持续更新？
2. 困难问题中指令更短（约75字符）、上下文依赖更强的特性对模型带来了何种特定推理挑战？Table 8 显示困难问题的指令长度显著短于简单问题，但高亮代码长度相似，暗示模糊指令需要更深层的上下文推理。
3. EditBench 问题在多大程度上覆盖了所有真实世界的使用案例？当前数据主要来自 VSCode 扩展用户，可能存在选择偏差。
4. 能否提升 agent 生成测试用具的能力，从而减少人工标注需求？这是基准可扩展性的核心瓶颈。
5. gpt-5 在默认推理设置下性能落后于 gpt-5-mini 的具体原因是什么？这一反常现象暗示模型规模和推理策略的交互可能对编辑任务产生非预期影响。

## 原文 PDF

![[paperPDFs/ICLR_2026/EditBench_Evaluating_LLM_Abilities_to_Perform_Real_World_Instructed_Code_Edits.pdf]]
