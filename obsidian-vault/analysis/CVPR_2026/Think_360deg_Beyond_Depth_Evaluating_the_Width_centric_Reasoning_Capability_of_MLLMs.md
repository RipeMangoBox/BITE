---
title: "Think 360deg: Beyond Depth: Evaluating the Width-centric Reasoning Capability of MLLMs"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/Think_360deg_Beyond_Depth_Evaluating_the_Width_centric_Reasoning_Capability_of_MLLMs.pdf
project_link: null
code_link: "https://github.com/InternLM/lmdeploy"
aliases:
- TTE
- T3BDEWCRCM
tags:
- CVPR_2026
- topic/other_unclear
- topic/other_unclear/general
core_operator: 推理宽度（Width-centric Reasoning）：模型在思维空间中进行系统性试探‑纠错（trial‑and‑error）、分治（divide‑and‑conquer）、分支定界（branch‑and‑bound）和假设‑检验（hypothesize‑and‑test）的能力，这一维度与推理深度正交且被现有基准普遍忽视。
primary_logic: 推理深度与推理宽度是正交的认知维度；构建首个以宽度为中心的多模态推理基准Think360°，并提出基于思维树的评估协议ToT-Eval，可同时量化模型的深度/宽度得分，揭示当前MLLM在广度搜索方面的结构性缺陷。
claims:
- 在Think360°上，最佳闭源模型Gemini-2.5-pro的pass@1仅46.0%，远低于其在常规VQA任务上的表现，表明当前模型在宽度推理上存在严重不足。
- 宽度门槛效应：准确率≥20%的模型通常推理宽度≥45%，表明宽度与最终正确率高度正相关。
- Claude-3.7-Sonnet-Thinking的ToT-Depth达到56.7%，但ToT-Width仅50.2%，说明即使模型具有一定深度推理能力，若宽度不足仍会导致整体准确率受限（35.5%）。
- Chain-of-Thought提示对部分模型可提升1-5个百分点，但无法从根本上解决宽度推理的困难。
---

# Think 360deg: Beyond Depth: Evaluating the Width-centric Reasoning Capability of MLLMs

> [!tip] 核心洞察
> 推理深度与推理宽度是正交的认知维度；构建首个以宽度为中心的多模态推理基准Think360°，并提出基于思维树的评估协议ToT-Eval，可同时量化模型的深度/宽度得分，揭示当前MLLM在广度搜索方面的结构性缺陷。

| 字段 | 内容 |
|------|------|
| 中文题名 | Think 360°：超越深度——评估多模态大语言模型的宽度中心推理能力 |
| 英文题名 | Think 360deg: Beyond Depth: Evaluating the Width-centric Reasoning Capability of MLLMs |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://openaccess.thecvf.com/content/CVPR2026/html/Chen_Think_360deg_Beyond_Depth_Evaluating_the_Width-centric_Reasoning_Capability_of_CVPR_2026_paper.html) · [Code](https://github.com/InternLM/lmdeploy) |
| Topic | #topic/other_unclear #topic/other_unclear/general |
| Method | Think360°（多模态宽度推理基准）与 ToT-Eval（思维树评估协议） |
| Dataset | Think360° |

> [!tip] 效果简介
> - Think360° (test-mini) 上，Overall pass@1 Accuracy 46.0 (Gemini-2.5-pro) vs 16.0 (GPT-4o) (+30.0)；Overall pass@1 Accuracy 35.5 (Claude-3.7-Sonnet-Thinking) vs 16.0 (GPT-4o) (+19.5)；ToT-Width Accuracy 50.2 (Claude-3.7-Sonnet-Thinking) vs 28.6 (Llama-3.2-Vision-11B) (+21.6)。

## 概要

当前多模态大语言模型（MLLM）在推理能力上取得了显著进展，但现有基准和评估几乎完全聚焦于**推理深度**——即沿单一链式路径逐步推导的能力。然而，大量复杂问题求解不仅需要深度，更依赖于**推理宽度**：同时探索多条并行推理路径、系统性剪枝无效分支、进行回溯与多约束满足的能力。这一维度与推理深度正交，却长期被忽视，构成当前 MLLM 的核心性能瓶颈。

针对这一空白，本文提出 **Think360°**——首个以宽度为中心的多模态推理基准，涵盖 1200+ 高质量多模态案例，跨越数学竞赛、教科书、现有基准和在线益智游戏等异质领域。同时，提出基于思维树的评估协议 **ToT-Eval**，从深度和宽度两个维度对模型推理过程进行细粒度量化。

在 Think360° 上对 12 个主要模型系列、30 余个先进 MLLM 的系统评估揭示了以下核心发现：

- **整体表现低下**：最佳闭源模型 Gemini-2.5-pro 的 pass@1 准确率仅为 46.0%，远低于其在常规 VQA 任务上的表现，说明当前模型在宽度推理上存在严重结构性缺陷。
- **宽度门槛效应**：准确率 ≥20% 的模型，其推理宽度得分均 ≥45%，表明宽度与最终正确率高度正相关，是制约性能的关键因子。
- **深度与宽度的失衡**：Claude-3.7-Sonnet-Thinking 的 ToT-Depth 达 56.7%，但 ToT-Width 仅 50.2%，说明即使模型具备一定深度推理能力，宽度不足仍导致整体准确率受限（35.5%）。
- **提示工程的局限**：Chain-of-Thought 提示对部分模型可带来 1-5 个百分点的温和提升，但远无法从根本上解决宽度推理的困难。

Think360° 不仅揭示了当前 MLLM 在广度搜索方面的系统性缺陷，也为未来面向宽度增强的训练算法（如多路径强化学习、过程奖励模型）提供了标准化的评估平台。

### 推理深度的单向演进与宽度维度的系统性缺失

多模态大语言模型（MLLM）在复杂推理任务上取得了显著进展，但其能力增长呈现明显的**单向性**：现有研究与基准几乎全部聚焦于**推理深度**（depth‑centric reasoning），即模型沿单一逻辑链进行顺序推导的能力。这种深度导向的评估范式催生了大量以长链式思维（chain‑of‑thought）为核心的方法，却系统性地忽视了推理的另一正交维度——**推理宽度**（width‑centric reasoning）。

推理宽度指模型在思维空间中同时探索多条并行推理路径、系统性地剪枝无效分支、进行回溯（backtracking）与多约束满足的能力。如图 1 所示，论文从神经网络设计的经典策略中汲取类比：捷径连接与 dropout 对应剪枝，金字塔特征对应分治（divide‑and‑conquer），逐层堆叠对应试错（trial‑and‑error），梯度反传对应回溯——这些机制在推理过程中分别映射为宽度维度的核心认知技能。然而，当前 MLLM 的评估体系对这些能力几乎没有任何量化手段。

### 现有基准的结构性盲区

当前主流多模态推理基准（如 MathVista、MathVerse 等）存在两个结构性缺陷：

1. **维度单一**：仅通过最终答案匹配（pass@1）评估模型表现，无法区分正确结果究竟源于深度推理还是宽度探索，更无法诊断模型在并行搜索、分支定界（branch‑and‑bound）等环节的具体短板。
2. **宽度问题缺失**：如表 2 所示，现有开源多模态数学基准中鲜有专门设计的宽度中心推理问题，导致模型在假设‑检验（hypothesize‑and‑test）、归纳推理等需要广域搜索的场景下能力无法被测量，更无从改进。

### 核心瓶颈与本文动机

**核心瓶颈**在于：当前 MLLM 在推理深度上已有长足进步，但其推理宽度能力严重不足，成为复杂问题求解的主要障碍。这一瓶颈在需要多路径探索与约束满足的任务中尤为突出，而现有训练范式（如监督微调、偏好对齐）天然倾向于强化单链推理，难以有效培养宽度推理能力。

**本文的核心洞察**是：推理深度与推理宽度是**正交的认知维度**，二者共同决定模型的综合推理能力。仅提升深度而忽略宽度，将导致模型在面对需要广域搜索的问题时出现结构性失效。基于此洞察，论文提出两个核心贡献：

- **Think360° 基准**：首个以宽度为中心的多模态推理基准，精心策划 1200+ 高质量多模态案例，覆盖异质领域与多种宽度导向推理模式（归纳推理、演绎推理、概率推理）及认知技能（分支定界、假设‑检验、分治）。
- **ToT‑Eval 评估协议**：基于思维树的细粒度评估方法，可同时量化模型的深度得分与宽度得分，揭示当前 MLLM 在广度搜索方面的结构性缺陷。

### 关键证据预览

后续实验将揭示当前模型的严峻现状：最佳闭源模型 **Gemini‑2.5‑pro** 在 Think360° 上的 pass@1 仅 **46.0%**，远低于其在常规 VQA 任务上的表现；而 **GPT‑4o** 仅取得 **16.0%** 的总体准确率。更值得关注的是，**宽度门槛效应**表明准确率 ≥20% 的模型其推理宽度均 ≥45%，宽度与最终正确率高度正相关——这直接验证了宽度维度是制约当前 MLLM 性能的关键因果变量。

## 核心方法与创新机理

### 问题诊断：从推理深度到推理宽度的范式转移

当前多模态大语言模型（MLLM）的推理能力评估与提升几乎完全聚焦于**推理深度**——即模型沿单一链式路径进行顺序推导的能力。然而，大量复杂问题求解的真实瓶颈并非“链有多长”，而是“能否同时探索多条并行路径、系统性剪枝无效分支、在关键节点进行回溯，并在多约束条件下完成假设-检验循环”。本文将这一被普遍忽视的认知维度定义为**推理宽度**（Width-centric Reasoning），并论证其与推理深度是正交且互补的能力轴。

这一诊断构成了全文的核心因果杠杆：推理宽度是当前 MLLM 在复杂多模态推理任务上表现受限的关键可控变量，而现有基准（如 MathVista、MathVerse 等）几乎完全未触及这一维度。

### 核心方法创新：Think360° 基准与 ToT-Eval 评估协议

针对上述瓶颈，本文提出两项紧密耦合的创新：

**1. Think360° 基准**：首个以推理宽度为中心的多模态推理基准。与传统基准仅关注最终答案正确性不同，Think360° 系统性地覆盖了三种宽度导向的推理模式——归纳推理、演绎推理和概率推理，以及与之对应的认知技能——分支定界（Branch-and-Bound）、假设-检验（Hypothesize-and-Test）和分治（Divide-and-Conquer）。基准包含 1225 个高质量多模态案例，横跨数学竞赛、教科书、现有基准和在线益智游戏四个来源，经过粗到细的三阶段质量过滤（静态模式匹配 → LLM-as-Judge → 人工双检）构建而成。

**2. ToT-Eval 评估协议**：基于思维树（Tree-of-Thought）的细粒度评估方法。ToT-Eval 使用 GPT-4o 从模型输出中提取关键推理步骤，构建层次化思维树（每个节点代表一个推理步骤，边表示依赖或并行关系），然后对每个节点的正确性进行评判，分别计算**最大正确链深度**作为深度得分，以及**有效并行分支数**作为宽度得分。这一协议使得同时量化模型的深度/宽度能力成为可能，突破了传统 pass@1 仅反映最终答案正确性的局限。

### 关键 changed slots：与基线方法的本质差异

相较于现有评估范式，本文在两个核心维度上实现了根本性改变：

| 维度 | 基线方法 | Think360° + ToT-Eval | 证据锚点 |
|------|----------|----------------------|----------|
| **评估目标维度** | 仅推理深度（单一链式推理） | 推理深度 + 推理宽度（并行探索、约束满足、回溯） | Section 3.1：“our Think360 benchmark additionally incorporates this complementary yet less explored dimension: the width of reasoning exploration.” |
| **评估协议** | pass@1（最终答案匹配） | pass@1 + ToT-Eval（基于思维树的深度/宽度联合评分） | Abstract & Section 4.1：“propose a fine-grained tree-of-thought evaluation protocol that jointly quantifies reasoning width and depth” |

这两个 changed slots 并非简单的增量改进，而是对 MLLM 推理能力评估框架的范式性重构。传统 pass@1 仅能回答“模型是否答对”，而 ToT-Eval 进一步揭示了“模型是如何思考的”——它是否尝试了多条路径、是否在错误分支上及时回溯、是否有效利用了并行探索。这种从“结果评价”到“过程诊断”的转变，为理解模型推理能力的结构性缺陷提供了前所未有的细粒度视角。

### 创新点的内在逻辑关联

Think360° 基准与 ToT-Eval 协议之间存在深层的设计耦合：基准本身的问题设计天然要求宽度推理（如需要同时验证多个约束条件的逻辑谜题），而 ToT-Eval 的思维树结构恰好能够捕捉模型在解决这些问题时的并行探索行为。这种“问题设计-评估方法”的闭环使得本文的贡献超越了简单的“新基准+新指标”组合，而是构建了一套完整的宽度推理诊断框架。

值得注意的是，ToT-Eval 本身依赖 GPT-4o 作为评判器进行思维树构建与节点正确性判定，这一设计在实现自动化的同时引入了潜在的系统性偏差——评判模型自身的推理能力可能影响评估结果的可靠性。本文对此局限性进行了明确讨论，但未提供多评判器投票或人工验证的消融实验，这一点需要读者在解读 ToT-Eval 结果时保持审慎。

Think360° 基准的构建遵循一条三阶段流水线，其核心目标是从多模态原始数据中系统性地提取、过滤并精炼出以宽度为中心的推理问题。该流水线的设计直接服务于论文的核心洞察：推理深度与推理宽度是正交的认知维度，而现有基准普遍忽视了后者。因此，流水线的每个阶段都旨在确保最终数据集能够有效衡量模型在并行探索、约束满足与回溯等宽度推理能力上的表现。

### 三阶段构建流水线

图2展示了该流水线的整体架构，三个阶段依次为：原始数据收集、质量过滤、以及标注与精炼。

1.  **原始数据收集**：数据来源覆盖四个异构领域，以确保问题类型的多样性和宽度推理的覆盖面：
    *   **数学与逻辑竞赛题**：提供高难度、需多步推导的证明与求解问题。
    *   **教科书示例**：涵盖标准化的学科推理模式。
    *   **现有基准**：从已公开的多模态数据集中筛选符合宽度要求的案例。
    *   **在线益智游戏**：引入需要试探、回溯和空间推理的交互式谜题。

2.  **质量过滤**：采用“粗到细”的过滤策略，以剔除低质量或不符合宽度推理要求的样本：
    *   **静态模式匹配**：通过规则启发式方法快速筛除格式错误或明显不相关的条目。
    *   **LLM-as-Judge**：利用大模型对问题的推理宽度潜力进行初步评判。
    *   **人工双检**：由人工对通过前两步的样本进行最终核查，确保问题质量与宽度推理的标签准确性。

3.  **标注与精炼**：针对不同来源的数据进行格式统一与答案可验证性改造。特别是将原始的证明题和游戏题，改写为具有明确、可客观评判答案的问答格式。这一步骤是连接原始数据与自动化评估协议的关键桥梁。

### 评估协议与模块交互

基准构建完成后，其配套的评估协议 **ToT-Eval** 定义了从模型输出到最终得分的处理流程，该流程由两个核心模块构成：

*   **思维树构建模块**：此模块的输入是被评估模型针对 Think360° 问题生成的完整推理轨迹。它使用 **GPT-4o** 作为提取器，从推理文本中逐字提取关键推理步骤，并将其组织成一个层次化的树结构。在该树中，每个节点代表一个原子推理步骤，边则代表步骤间的依赖或并行关系。
*   **深度/宽度评分模块**：该模块以构建好的思维树为输入。它首先对树中每个节点的正确性进行评判，然后计算两个正交维度的得分：**深度得分**为树中最大正确推理链的长度，**宽度得分**则为有效并行分支的数量。最终，这两个得分与传统的 pass@1 准确率一同构成对模型宽度中心推理能力的完整刻画。

整个框架的输入是多源异构的多模态数据，输出则是一个结构化的、专门针对推理宽度的基准数据集，以及一套能够从深度和宽度两个维度量化模型表现的评估协议。

### 补充图表

![[assets/figures/papers/paper_list_l829_https_openaccess_thecvf_com_content_CVPR2026_html_Chen_Think_360deg_Beyo/figures/002_Figure_2.jpg]]
*Figure 2: Three-stage pipeline for constructing Think360◦—beginning with diverse seed data collection, progressing through a two-step quality filter (rule-based heuristics and human double-check), and finalized through targeted annotation & refinement (as demonstrated by proof- and game-based problems)*

### 3.1 Think360° 基准构建管道

Think360° 的构建遵循三阶段管道（见 Figure 2），旨在从异质来源中筛选出以宽度推理为核心的高质量多模态样本。

**阶段一：原始数据收集**
数据源自四个互补渠道：
- **数学与逻辑竞赛题**：来自国际数学奥林匹克（IMO）等赛事，天然要求多路径探索与约束满足。
- **教科书例题**：涵盖几何、概率、组合数学等领域，提供结构化的问题表述与标准解答。
- **现有基准**：从 MathVista、MathVerse 等已有数据集中筛选符合宽度推理特征的子集。
- **在线益智游戏**：如数独、逻辑网格谜题等，其求解过程内在地依赖分支定界与假设-检验策略。

**阶段二：质量过滤**
采用“粗到细”的三级过滤策略：
1. **静态模式匹配**：基于规则剔除格式错误、答案缺失或明显过于简单的样本。
2. **LLM-as-Judge**：利用 GPT-4o 对候选样本的推理宽度潜力进行初筛评分。
3. **人工双检**：由标注者对通过前两级的样本进行最终审核，确保问题表述清晰、答案可客观验证且确实需要宽度推理。

**阶段三：标注与精炼**
针对证明题和游戏题等原始形式不直接适配问答评估的样本，进行定向改写：
- 将证明题转化为“判断结论正误”或“计算特定中间量”的可验证格式。
- 将游戏题转化为“给定初始状态，求最少步数/最终状态”的确定性问答对。
- 确保所有答案均为可自动评判的短文本或数值形式。

### 3.2 思维树评估协议

为量化模型的推理宽度与深度，本文提出 **ToT-Eval** 协议，包含两个核心模块（见 Figure 4）。

![[assets/figures/papers/paper_list_l829_https_openaccess_thecvf_com_content_CVPR2026_html_Chen_Think_360deg_Beyo/figures/005_Figure_4.jpg]]
*Figure 4: Tree-of-Thought Evaluation from the perspective of depth and width*

**模块一：思维树构建**
给定模型对问题的完整输出（包含推理过程与最终答案），使用 GPT-4o 作为提取器，执行以下步骤：
1. **步骤提取**：从模型输出中逐字提取关键推理步骤，每个步骤被视为思维树中的一个节点。
2. **层次化组织**：根据步骤间的逻辑依赖关系，将节点组织为树结构——若步骤 B 直接依赖于步骤 A 的结论，则 A 为 B 的父节点；若多个步骤并行探索不同假设且互不依赖，则它们共享同一父节点形成分支。
3. **边标注**：边表示节点间的依赖或并行关系，为后续深度/宽度计算提供拓扑基础。

**模块二：深度/宽度评分**
基于构建的思维树，定义两个核心指标：

- **推理深度得分**：思维树中从根节点到任意叶节点的最长正确推理链的长度。形式上，令 $T$ 为思维树，$P$ 为从根到叶的一条路径，$\mathcal{C}(n)$ 为节点 $n$ 正确性的二值指示函数（由 GPT-4o 评判），则深度得分定义为：
  $$\text{Depth}(T) = \max_{P \subset T} \sum_{n \in P} \mathcal{C}(n)$$
  该指标衡量模型沿单一路径进行连贯推理的能力。

- **推理宽度得分**：思维树中有效并行分支的数量。有效分支定义为：分支中的节点均被判定为正确，且该分支对最终答案有实质性贡献（非冗余探索）。形式上：
  $$\text{Width}(T) = \sum_{b \in \text{Branches}(T)} \mathbb{I}\left[\forall n \in b,\ \mathcal{C}(n) = 1 \land \text{Contributes}(b)\right]$$
  其中 $\text{Contributes}(b)$ 判断分支 $b$ 是否在推理过程中被有效利用（而非无意义的发散探索）。

两个指标联合评估，可揭示模型在“深而窄”与“浅而宽”之间的权衡关系——前者擅长链式推导但缺乏多路径探索，后者能覆盖更多可能性但可能牺牲单链深度。

### 3.3 关键设计决策与局限

- **评判器依赖**：ToT-Eval 全程依赖 GPT-4o 进行步骤提取与正确性评判，可能引入评判模型自身的系统性偏差。对于复杂推理链，节点正确性的判定存在噪声。
- **宽度定义的范围**：当前宽度得分仅统计有效分支数量，未区分分支的质量差异（如部分正确但未完成的探索），也未显式建模回溯行为的计算成本。
- **输出截断影响**：部分模型因最大输出长度限制，可能无法完整展示其宽度探索，导致宽度得分被低估。实验设置中虽已配置各模型的最大支持输出长度，但该交互影响未被严格控制。

### 补充图表

![[assets/figures/papers/paper_list_l829_https_openaccess_thecvf_com_content_CVPR2026_html_Chen_Think_360deg_Beyo/figures/001_Figure_1.jpg]]
*Figure 1: The concepts illustration for the width and depth in the information propagation process of neural network and reasoning. Drawing insights from the classical designs in neutral network: shortcut skipping or dropout, pyramid feature, layer stacking and gradient back propagation, we analogize these to the strategies: pruning, divide-and-conquer, trial-and-error and backtracking to distinguish depth versus width in inference processes*

## 实验与关键发现

### 评估设置

为控制随机性对结论的影响，所有模型默认温度设为 0.7，每题重复评测三次并汇报均值（Section 4.1）。在可接受的推理时间和成本约束内，每个模型均配置为最大支持的输出长度，以尽可能避免因输出截断而限制宽度探索。部分开源模型（Qwen 系列、MiMo、Kimi、LLama、GLM-V 等）采用 vLLM 或 LMDeploy 引擎部署加速，在 Table 3 中以 † 标注，该加速部署可能与原始服务存在推理环境差异，需在横向对比时加以注意。

![[assets/figures/papers/paper_list_l829_https_openaccess_thecvf_com_content_CVPR2026_html_Chen_Think_360deg_Beyo/figures/008_Table_3.jpg]]
*Table 3: Reasoning performance evaluation with various closed-source and open-source MLLMs. We highlight the top , second , and third highest results within each column of the two groups. Please zoom in for a better view. Models with the symbol † are evaluated by the implementation with vLLM (Qwen series, MiMo, Kimi, Llama, GLM) or LMDeploy (InternVL series) for acceleration. Please zoom in for a better view*

### 主结果：宽度推理的全局瓶颈

Table 3 汇总了 30 余个前沿 MLLM 在 Think360° test-mini（740 题）上的 pass@1 准确率。核心发现是：**当前最强闭源模型 Gemini-2.5-pro 的整体准确率仅为 46.0%，而 GPT-4o 仅 16.0%**，远低于这些模型在常规 VQA 基准上的表现，清晰揭示了宽度中心推理的结构性缺陷。开源阵营中，InternVL3-78B 以 23.1% 居首，LLaVA-Onevision 仅 9.0%，说明开源模型在宽度探索能力上差距更为悬殊。

从认知技能维度拆解，模型在“分支定界”（Branch-and-Bound）和“假设‑检验”（Hypothesize-and-Test）两类典型宽度技能上的得分普遍低于“分治”（Divide-and-Conquer），表明当前 MLLM 在需要系统性剪枝和回溯的场景中尤为薄弱。Figure 6 的失败案例分析进一步显示，模型常见的错误模式包括：过早收敛于单一候选解、无法有效排除矛盾分支、以及在多约束条件下丢失全局一致性。

![[assets/figures/papers/paper_list_l829_https_openaccess_thecvf_com_content_CVPR2026_html_Chen_Think_360deg_Beyo/figures/009_Figure_6.jpg]]
*Figure 6: Failure cases analysis*

### 消融实验：CoT 提示的有限增益

Table 4 考察了 Chain-of-Thought 提示对宽度推理的影响。结果显示，CoT 对部分模型产生温和的正向增益：MiMo-VL-RL-7B 从 28.3% 提升至 29.9%（+1.6 个百分点），Claude-4-Opus 提升 +4.6%。然而，这些增益远不足以弥合宽度推理的根本性差距——即便在 CoT 加持下，GPT-4o 的准确率仍停留在 20% 以下。这一消融表明，**简单的链式提示无法替代模型内在的并行搜索与回溯机制**，宽度推理需要更深层的架构或训练范式创新。

![[assets/figures/papers/paper_list_l829_https_openaccess_thecvf_com_content_CVPR2026_html_Chen_Think_360deg_Beyo/figures/010_Table_4.jpg]]
*Table 4: Influence of Chain-of-Thought prompting on model performances*

### 思维树评估：深度与宽度的正交性

ToT-Eval 协议（Figure 4）从思维树中量化两个正交维度：ToT-Depth（最大正确链深度）和 ToT-Width（有效并行分支数）。Table 5 的结果揭示了一个关键权衡：Claude-3.7-Sonnet-Thinking 的 ToT-Depth 达到 56.7%，表现优异，但其 ToT-Width 仅 50.2%，最终整体准确率被拉低至 35.5%。这说明**即使模型具备较强的深度推理能力，若宽度不足，仍会因搜索空间覆盖不完整而频繁失败**。

![[assets/figures/papers/paper_list_l829_https_openaccess_thecvf_com_content_CVPR2026_html_Chen_Think_360deg_Beyo/figures/011_Table_5.jpg]]
*Table 5: Model results on ToT width/depth and accuracy. We highlight the top second , and third highest results within each column*

更系统的分析发现存在“宽度门槛效应”：准确率 ≥20% 的模型，其 ToT-Width 得分均不低于 45%，而宽度低于此阈值的模型准确率无一突破 20%。这一强正相关关系表明，**推理宽度是制约当前 MLLM 在复杂问题上性能的核心瓶颈**，而非推理深度。

### 输入模态消融

附录中的模态消融实验（Section 4.1 details）对比了 Text-Only 与 Image-Only 条件下的表现。结果表明，多模态输入对 Think360° 中的多数任务至关重要，纯文本条件下模型表现显著下降，证实视觉信息在宽度推理中并非干扰因素，而是提供关键约束和搜索线索的必要条件。

### 补充图表

![[assets/figures/papers/paper_list_l829_https_openaccess_thecvf_com_content_CVPR2026_html_Chen_Think_360deg_Beyo/figures/007_Table_2.jpg]]
*Table 2: Comparison with existing multimodal math benchmarks. Level: K =K-12, U=University, C =Competition. Source: S =Self-sourced, P =Collected from Public Dataset*

![[assets/figures/papers/paper_list_l829_https_openaccess_thecvf_com_content_CVPR2026_html_Chen_Think_360deg_Beyo/figures/006_Figure_5.jpg]]
*Figure 5: Frequency distribution and co-occurrence patterns of cognitive skills required for solving problems in Think360 . The left panel shows the frequency distribution of individual cognitive capabilities across our benchmark, while the right panel presents a chord diagram illustrating the co-occurrence relationships between different cognitive skills. Please zoom in for a better view*

![[assets/figures/papers/paper_list_l829_https_openaccess_thecvf_com_content_CVPR2026_html_Chen_Think_360deg_Beyo/figures/004_Figure_3.jpg]]
*Figure 3: Demonstration of the Think360 data cases. The figure offers paired examples of three width-oriented reasoning patterns: Inductive Reasoning, Deductive Reasoning, and Probabilistic Reasoning, and tightly linked cognitive skills: Branchand-Bound, Hypothesize-and-Test, and Divide-and-Conquer*

## 定位与知识库关联

### 与现有推理基准的关系

当前多模态推理评估领域存在一条清晰的演化路径：从早期以**单一链式推理深度**为核心的基准（如MathVista、MathVerse等），逐步过渡到同时关注**推理宽度**的新一代评估范式。Think360°正是这一范式转换的关键推动者。

**深度中心基准的局限**。现有主流多模态数学与推理基准（Table 2对比了多个开源基准）普遍聚焦于“模型能否沿着一条正确的推理链到达终点”，其评估指标几乎完全依赖最终答案匹配（pass@1）。这类基准无法区分以下两种失败模式：（1）模型根本没有探索到正确路径（宽度不足）；（2）模型探索到了正确路径但无法完成长链推导（深度不足）。Think360°通过引入**ToT-Eval协议**，首次将这两种失败模式解耦量化。

**宽度推理的独特性**。Table 2的对比明确显示，Think360°是首个**100%由宽度中心推理问题构成**的多模态基准（约1200题），而现有基准中此类问题的占比极低或为零。这一设计选择源于核心洞察：推理宽度与推理深度是**正交的认知维度**——一个模型可以在单链深度推理上表现优异，却在需要并行探索、分支定界、假设检验等宽度策略时严重失效。

### 与基线方法的对比定位

**闭源模型的深度/宽度权衡**。实验揭示了一个关键现象：即使是最先进的闭源模型，其宽度能力也远未饱和。**Claude-3.7-Sonnet-Thinking**的ToT-Depth达到56.7%，但ToT-Width仅50.2%，最终整体准确率被拉低至35.5%（Table 5）。这表明**深度能力是宽度的必要但不充分条件**——模型需要同时具备足够的宽度才能将深度推理转化为正确输出。**Gemini-2.5-pro**以46.0%的pass@1准确率领先（Table 3），但其宽度得分仍远未达到人类水平，说明当前所有模型都存在结构性宽度缺陷。

**开源模型的宽度困境**。开源模型中，**GPT-4o**仅取得16.0%的整体准确率（Table 3），**LLaVA-Onevision**更是低至约9.0%。这些模型在常规VQA任务上的表现通常远高于此，这种剧烈下降印证了宽度推理对现有训练范式构成了根本性挑战——当前以监督微调和对齐训练为主的技术路线，难以有效培养系统性的试探-纠错和分支搜索能力。

**Chain-of-Thought的有限增效**。Table 4的消融实验显示，CoT提示对部分模型（如**MiMo-VL-RL-7B**）仅能提升1-2个百分点的准确率，对Claude-4-Opus提升约4.6%。这一温和增益远不足以弥合宽度差距，说明**简单的提示工程无法从根本上解决宽度推理的结构性困难**——模型需要内在的搜索与剪枝机制，而非仅仅延长推理链。

### 适用边界

**评估维度的聚焦性**。Think360°明确限定于**宽度中心的推理能力**评估，不覆盖创造力、常识推理、跨领域迁移等其他高阶认知维度。因此，其分数不应被解释为模型的“通用推理能力”排名，而应理解为对宽度维度的专项诊断。

**模态依赖的边界**。输入模态消融实验（Section 4.1，详见附录）表明，多模态输入对多数任务至关重要，纯文本条件下模型表现显著下降。这一发现界定了基准的适用前提：Think360°主要评估的是**多模态场景下的宽度推理**，其在纯文本大模型上的适用性仍是一个开放问题。

**评判协议的系统性偏差**。ToT-Eval使用**GPT-4o**作为思维树构建器和节点正确性评判器，这意味着评估结果可能包含评判模型本身的系统性偏差。对于复杂推理链的细粒度正确性判定，单一评判器的噪声水平尚未通过多模型投票或大规模人工标注进行校准。

### 局限与开放问题

**方法层面的局限**。当前基准揭示的核心瓶颈是明确的——模型在宽度推理上存在结构性缺陷，但**缺乏成熟的宽度增强训练技术**。现有训练范式（监督微调、RLHF、DPO等）主要优化单链输出质量，尚未发展出有效的多路径探索与剪枝训练算法。这一方法空白构成了从“诊断问题”到“解决问题”的关键缺口。

**评测层面的局限**。样本量（test-mini 740例）虽经精心筛选，但覆盖的场景多样性和难度梯度仍有待扩展。此外，评测未严格控制思维链长度与token预算的交互影响——部分模型可能因输出截断而无法展示完整的宽度探索过程，导致宽度得分被低估。

**核心开放问题**。以下问题构成了该方向的未来研究议程：

1. **宽度增强训练**：如何通过多路径强化学习或过程奖励模型显式培养宽度推理能力？
2. **宽度scaling law**：增加模型参数量或训练数据多样性对宽度提升有何量化效果？
3. **评判可靠性**：ToT-Eval的自动化评判能否通过多模型集成或人工验证达到高可靠性？
4. **模态角色**：视觉模态在宽度推理中是必要条件还是仅为干扰因素？纯文本大模型在该基准上的表现如何？
5. **通用宽度算法**：能否设计一种训练算法，使模型在保持深度的同时自动拓宽搜索空间，实现深度与宽度的协同增长？

这些问题的回答将决定宽度推理能力能否从“被诊断的瓶颈”转化为“可工程化的能力”。

## 原文 PDF

![[paperPDFs/CVPR_2026/Think_360deg_Beyond_Depth_Evaluating_the_Width_centric_Reasoning_Capability_of_MLLMs.pdf]]
