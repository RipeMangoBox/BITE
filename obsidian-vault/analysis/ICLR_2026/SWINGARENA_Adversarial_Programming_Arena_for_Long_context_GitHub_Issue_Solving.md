---
title: "SWINGARENA: Adversarial Programming Arena for Long-context GitHub Issue Solving"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/SWINGARENA_Adversarial_Programming_Arena_for_Long_context_GitHub_Issue_Solving.pdf
project_link: https://swing-bench.github.io/
code_link: https://github.com/menik1126/Swing-Bench
openreview_forum_id: YuxgSGFaqb
aliases:
- SWINGARENA
tags:
- ICLR_2026
- topic/safety_alignment_fairness_privacy
- topic/safety_alignment_fairness_privacy/trustworthy_machine_learning
core_operator: "引入对抗性双智能体协议（提交者与审阅者）并集成真实CI工作流验证，通过角色切换、迭代反馈和审查测试质量门控，构建动态竞技场以暴露模型在补丁生成与测试生成中的差异化行为。"
primary_logic: "在CI驱动的对抗性场景中，模型展现出不同的专长：GPT-4o擅长激进地生成能通过审查的高胜率补丁，而DeepSeek和Gemini则更注重代码正确性与CI稳定性；同时，RACG模块通过语法感知分块和密集重排序有效缓解长上下文检索瓶颈，显著提升补丁定位精度和任务解决率。"
claims:
- "SWINGARENA通过提交者-审阅者对抗交互和完整CI验证，能够揭示传统基准忽略的模型行为差异。"
- "GPT-4o作为提交者在所有对局中均取得≥0.90的胜率，但SPR/RPR相对较低（0.65/0.55），显示其激进补丁策略。"
- "DeepSeek-V3在Best@3指标上平均得分最高（0.59），并且在Rust和Go上表现尤为均衡，表明其更稳健的多语言代码推理能力。"
- "RACG模块使C++任务上的Best@3从0.38提升至0.42，并将胜率从0.77提升至0.84，同时减少12-18%的令牌占用。"
---

# SWINGARENA: Adversarial Programming Arena for Long-context GitHub Issue Solving

> [!tip] 核心洞察
> 在CI驱动的对抗性场景中，模型展现出不同的专长：GPT-4o擅长激进地生成能通过审查的高胜率补丁，而DeepSeek和Gemini则更注重代码正确性与CI稳定性；同时，RACG模块通过语法感知分块和密集重排序有效缓解长上下文检索瓶颈，显著提升补丁定位精度和任务解决率。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | SWINGARENA: 面向长上下文GitHub问题求解的对抗性编程竞技场 |
| 英文题名 | SWINGARENA: Adversarial Programming Arena for Long-context GitHub Issue Solving |
| 会议/期刊 | ICLR 2026 (Oral) |
| Links | [paper](https://openreview.net/forum?id=YuxgSGFaqb) · [GitHub](https://github.com/menik1126/Swing-Bench) · [Project](https://swing-bench.github.io/) |
| Topic | #topic/safety_alignment_fairness_privacy #topic/safety_alignment_fairness_privacy/trustworthy_machine_learning |
| Method | SWINGARENA |
| Dataset | SWINGARENA Adversarial Battle (400 evaluation instances), SWINGARENA Adversarial Battle, SWINGARENA Best@3 (across languages), Language-specific Best@3 (C++, Go, Rust, Python) |

> [!tip] 效果简介
> - SWINGARENA Adversarial Battle (400 evaluation instances) 上，Win Rate (Self-play) 为 GPT-4o vs GPT-4o: 0.97 | Claude vs Claude: 1.00 | Gemini vs Gemini: 0.91 | DeepSeek vs DeepSeek: 0.96，对比 N/A (self-play)，变化 N/A。
> - SWINGARENA Adversarial Battle 上，Submitter CI Pass Rate (SPR) (Self-play) 为 GPT-4o: 0.68 | Claude: 0.62 | Gemini: 0.63 | DeepSeek: 0.66，对比 N/A，变化 N/A。
> - SWINGARENA Best@3 (across languages) 上，Best@3 Average 为 GPT-4o: 0.57 | Claude: 0.55 | Gemini: 0.57 | DeepSeek: 0.59，对比 N/A，变化 N/A。

## 概要

现有的大语言模型（LLM）代码能力评估基准主要依赖静态单元测试或部分模拟的执行环境，忽略了真实软件开发中完整的持续集成（CI）流水线、协作式迭代（提交-审阅循环）以及对抗性测试带来的挑战，因而无法全面衡量模型在真实软件工程场景中的能力。针对这一瓶颈，SWINGARENA提出了一个对抗性编程竞技场，通过引入提交者-审阅者双智能体协议并集成真实CI工作流验证，构建了动态的对抗性评估框架。其核心洞察在于：在CI驱动的对抗性场景中，不同模型展现出差异化的行为模式——GPT-4o擅长激进地生成高胜率补丁，而DeepSeek和Gemini则更注重代码正确性与CI稳定性；同时，检索增强代码生成（RACG）模块通过语法感知分块和密集重排序有效缓解了长上下文检索瓶颈，显著提升了补丁定位精度和任务解决率。

在方法层面，SWINGARENA将评估协议从静态单元测试替换为对抗性CI驱动的对战机制，包含提交者-审阅者角色交替、迭代反馈和审查者测试质量门控；将上下文检索从朴素的全文或BM25检索升级为多语言RACG流水线（BM25文件检索→语法感知分块→CodeBERT重排序→令牌预算感知的动态块打包）；并将验证环境从手动Docker配置替换为自动化的隔离容器，通过act运行仓库原生的CI流水线（GitHub Actions、Travis CI），支持C++、Python、Rust、Go等多语言执行。

主要实验结果表明：在400个高质量真实GitHub问题实例上，GPT-4o作为提交者在所有对局中均取得≥0.90的胜率，但其提交端CI通过率（SPR）和审查端CI通过率（RPR）相对较低（0.65/0.55），反映出其激进补丁策略；DeepSeek-V3在Best@3指标上取得最高平均得分（0.59），并在Rust和Go上表现尤为均衡。RACG模块使C++任务上的Best@3从0.38提升至0.42，胜率从0.77提升至0.84，同时减少12-18%的令牌占用。消融实验进一步表明，约15%的失败案例可追溯至检索阶段未能找到关键上下文，揭示检索质量仍是当前性能的瓶颈之一。

大型语言模型（LLM）在代码生成领域取得了显著进展，然而现有评估基准（如SWE-Bench）存在一个核心瓶颈：它们仅依赖静态或部分模拟的单元测试，忽略了真实软件开发中完整的CI流水线、协作式迭代（提交-审阅循环）以及对抗性测试的挑战。这导致现有基准无法全面衡量模型在真实软件工程场景中的能力，尤其是当补丁生成与测试生成相互博弈时，模型行为的细微差异会被掩盖。

具体而言，现有评估范式存在三个关键缺口：

1. **静态测试套件的局限性**：传统基准使用预先定义的固定测试用例评估补丁质量，但真实开发中审查者会针对提交内容动态生成对抗性测试，这种交互机制在静态评估中被完全忽略。

2. **长上下文检索的挑战**：真实GitHub仓库通常包含大量代码文件，模型需要在庞大的代码库中精确定位与问题相关的上下文。现有方法多采用简单的BM25检索或全上下文输入，缺乏语法感知和稠密重排序能力，导致检索精度不足，成为任务成功的瓶颈——约15%的失败案例可直接归因于检索阶段未能找到关键上下文。

3. **CI流水线验证的缺失**：真实软件工程中，补丁不仅需要通过功能测试，还需满足代码风格、安全性、覆盖率等仓库原生门禁。现有评估环境通常仅提供简化的Docker执行，无法复现完整的CI验证流程。

为填补这些缺口，SWINGARENA引入了一种对抗性双智能体评估协议：将LLM分别置于提交者（生成补丁）和审查者（生成测试用例）的角色中，通过完整的CI流水线进行验证。这种设计使得框架能够揭示传统基准无法捕捉的模型行为差异——例如，GPT-4o展现出激进的补丁策略，在所有对局中取得≥0.90的胜率，但其补丁通过审查者测试的比例（RPR）相对较低（0.55），表明其更注重“通过审查”而非代码的全面正确性。

同时，为应对长上下文代码检索的挑战，SWINGARENA集成了检索增强代码生成（RACG）模块。该模块通过语法感知分块、稠密重排序和令牌预算感知打包的组合策略，在多语言环境下（C++、Python、Rust、Go）显著提升了补丁定位精度。消融实验表明，RACG使C++任务上的Best@3从0.38提升至0.42，胜率从0.77提升至0.84，同时减少了12-18%的令牌占用。

本文的核心动机在于：通过构建一个CI驱动的对抗性竞技场，系统性地暴露模型在补丁生成与测试生成中的差异化行为，并验证长上下文检索优化对任务解决率的因果影响，从而推动LLM在真实软件工程场景中的能力评估与提升。

## 核心方法与创新机理

SWINGARENA的核心创新在于将LLM代码能力评估从静态单元测试范式推向**对抗性CI驱动竞技场**，并通过**多语言检索增强代码生成（RACG）**模块解决长上下文代码库的检索瓶颈。以下从评估协议、上下文检索和验证环境三个关键维度展开分析。

### 1. 评估协议：从静态测试到对抗性CI竞技场

传统基准（如SWE-Bench）依赖固定的单元测试套件或一次性代码生成，无法捕捉真实软件工程中提交者与审阅者之间的迭代博弈。SWINGARENA引入**提交者-审阅者双智能体对抗协议**，其核心机制包括：

- **角色交替与迭代反馈**：两个LLM分别扮演提交者（生成补丁）和审阅者（生成测试用例），在多轮交互中交替角色，并基于CI反馈迭代优化。提交者补丁通过所有测试（含审阅者测试）获+1分，失败则-1分；审阅者生成的测试若能揭示提交者补丁的缺陷则获+1分（见Sec 3.2 Arena）。
- **审阅者测试质量门控**：审阅者不仅评判补丁，还需主动设计针对补丁修改逻辑的测试用例，系统会提供补丁变更位置的上下文提示（见Sec 4）。这一机制暴露了传统基准忽略的模型行为差异——例如GPT-4o作为提交者时胜率高达≥0.90，但其Submitter CI Pass Rate（SPR）和Reviewer CI Pass Rate（RPR）相对较低（0.65/0.55），表明其倾向于生成激进但可能不稳定的补丁；而DeepSeek-V3在Best@3指标上平均得分最高（0.59），在Rust和Go等多语言任务上表现更为均衡（见Table 1、Table 2）。

### 2. 上下文检索：多语言RACG模块

面对真实仓库中动辄数万token的代码上下文（如C++平均54,483 token，见Figure 7），简单的全上下文输入或BM25检索无法有效定位关键代码。SWINGARENA提出的**RACG模块**通过四级流水线解决这一问题：

- **FileRetriever（BM25）**：基于问题描述与源文件的词法相似度进行粗粒度文件排序。
- **CodeChunker（语法感知分块）**：支持C++、Python、Rust、Go的层次化分块，将代码分解为函数、类、块等语义单元，避免简单按行切割破坏语义完整性。
- **CodeReranker（CodeBERT稠密重排序）**：计算问题描述与代码块的稠密向量相似度，实现细粒度重排序。实验表明，块级重排序策略在Top-10文件命中率上达到48.7%，大幅优于BM25的20.7%（见Table 6）。
- **Token Budget-Aware Context Manager**：根据令牌预算动态选择并打包代码块，调整粒度并添加元数据，在同等Best@3条件下减少12-18%的令牌占用（见Table 3）。

消融实验证实，RACG使C++任务上的Best@3从0.38提升至0.42，Win Rate从0.77提升至0.84（见Table 3）。但约15%的失败案例仍可追溯至检索阶段未能找到关键上下文（见附录F LIMITATION），表明检索质量仍是当前性能瓶颈之一。

### 3. 验证环境：仓库原生CI流水线集成

与手动Docker配置或单语言单元测试执行不同，SWINGARENA通过**act工具**在隔离Docker容器中自动运行仓库原生的CI流水线（如GitHub Actions、Travis CI），支持多语言执行（含Rust的cargo系统）。这一设计确保了评估的可复现性，并覆盖代码风格、安全性和覆盖率等仓库原生门禁，而非仅依赖简化的单元测试断言。

### 方法谱系与知识库定位

SWINGARENA的评估框架与**SWE-Bench**（Jimenez et al., 2024）和**RepoBench**（Liu et al., 2024b）等代码基准共享对真实软件工程场景的关注，但其对抗性CI协议和角色切换机制是独特贡献。RACG模块在检索增强代码生成方向上与**RepoCoder**（Zhang et al., 2023）等工作的迭代检索策略形成互补——前者强调多语言语法感知分块与稠密重排序，后者侧重迭代式仓库遍历。在基线模型层面，GPT-4o、Claude-3.5、Gemini-2.0和DeepSeek-V3作为提交者/审阅者的对比揭示了不同模型在补丁激进性与代码正确性之间的权衡，而Qwen2.5-Coder-7B-Instruct等开源模型在消融研究中验证了RACG的通用性。

![[assets/figures/papers/paper_list_l15_https_openreview_net_forum_id_YuxgSGFaqb/figures/001_Figure_1.jpg]]
*Figure 1: Overview of SWINGARENA data construction pipeline, including repository collection, pull request extraction, task instance creation, quality filtering, and multiple CI-based validation*

SWINGARENA 的整体框架由两大核心子系统构成：**对抗性评估竞技场**与**检索增强代码生成（RACG）模块**。前者定义了提交者-审阅者双智能体在真实 CI 流水线中的博弈协议，后者负责从大规模代码库中高效检索并打包关键上下文，以缓解长上下文带来的定位与推理瓶颈。

### 数据构建流水线

评估实例的质量直接决定了竞技场的可信度。SWINGARENA 采用四阶段筛选流水线（图1）：

1. **仓库挖掘（Repository Mining）**：从 GitHub 采集高质量仓库及其关联的 PR/Issue 元数据。
2. **CI 测试过滤（CI Test Filtering）**：仅保留通过完整 CI 检查的实例，确保基准的真实性与可复现性。
3. **LLM 过滤（LLM-as-a-Judge）**：使用 Grok-3-beta 评估问题陈述的清晰度与任务难度。
4. **专家过滤（Expert Filtering）**：人工专家审核并校正 LLM 评估结果，剔除低质量样本。

最终构建的 CI 驱动数据集包含 2,300 个（Issue, PR）对，其中 400 个实例（每种语言 100 个）用于主评估，另设 100 个样本用于消融实验。

### 对抗性竞技场协议（Battle Protocol）

竞技场的核心设计是将传统的静态单元测试评估替换为**对抗性 CI 驱动博弈**（图2）：一个模型扮演**提交者**生成补丁，另一个模型扮演**审阅者**生成测试用例以暴露补丁缺陷。双方通过完整 CI 流水线（利用 `act` 在隔离 Docker 容器中运行仓库原生 GitHub Actions/Travis CI）进行验证，并交替角色进行多轮迭代。

评分机制采用对称的奖惩结构：
- 提交者：补丁通过所有测试（含审阅者测试）得 +1，任何失败得 -1。
- 审阅者：生成的测试成功捕获提交者补丁的缺陷得 +1，否则得 -1。

这一协议能够度量传统基准忽略的**仓库原生门禁**（代码风格、安全性、覆盖率）以及**补丁生成与测试生成之间的动态交互**。

### 检索增强代码生成模块（RACG）

面对多语言大规模代码库带来的长上下文挑战，RACG 模块通过四阶段流水线实现精准的代码上下文供给：

1. **FileRetriever（BM25）**：以问题描述为查询，对源文件进行词法相似度排序，实现粗粒度文件级检索。
2. **CodeChunker**：采用层次化、语法感知的分块策略，将代码分解为函数、类、块等语义单元，支持 C++、Python、Rust、Go。
3. **CodeReranker（CodeBERT）**：计算问题与代码块的稠密向量相似度，对候选块进行重排序，弥补 BM25 在语义匹配上的不足。
4. **Token Budget-Aware Context Manager**：根据令牌预算动态选择并打包代码块，调整粒度并附加元数据，确保关键上下文在有限窗口内得到保留。

消融实验表明，RACG 使 C++ 任务上的 Best@3 从 0.38 提升至 0.42，胜率从 0.77 提升至 0.84，同时减少 12-18% 的令牌占用。块级重排序策略在 Top-10 文件命中率上达到 48.7%，大幅优于纯 BM25 的 20.7%。

### 模块间数据流

整体工作流如下：数据构建流水线输出经过验证的 Issue-PR 对 → RACG 模块根据问题描述检索并打包相关代码上下文 → 提交者基于上下文生成补丁 → CI 验证模块在 Docker 容器中运行仓库原生 CI 流水线验证补丁 → 审阅者基于补丁变更信息生成针对性测试用例 → CI 再次验证完整补丁 → 评分引擎计算双方得分 → 角色切换进入下一轮迭代。所有评估使用统一的解码参数（temperature=0, top-p）和令牌预算，API 失败自动记录并重试，确保公平性与可复现性。

### 对抗性竞技场框架

SWINGARENA的核心是一个双智能体对抗性评估框架，模拟真实软件开发中的提交-审阅工作流。框架定义两个角色：

- **提交者（Submitter）**：接收问题描述和代码上下文，生成补丁以修复问题。
- **审阅者（Reviewer）**：接收问题描述和提交者的补丁，生成额外的测试用例以暴露补丁中的潜在缺陷或边界情况。

对战协议采用计分制：提交者补丁通过所有测试（包括审阅者生成的测试）得 +1 分，任何测试失败得 -1 分；审阅者生成的测试若使提交者补丁失败则得 +1 分，若补丁通过所有测试则得 -1 分。两个角色在多个轮次中交替执行，并基于持续集成（CI）反馈进行迭代优化，模拟动态软件开发过程。

所有评估在隔离的Docker容器中运行，通过 `act` 工具执行仓库原生的CI流水线（GitHub Actions、Travis CI），支持C++、Python、Rust、Go等多语言执行环境。

### 检索增强代码生成模块（RACG）

为应对大型代码库中的长上下文挑战，SWINGARENA引入多语言检索增强代码生成模块RACG，由四个子模块组成：

1. **FileRetriever（文件检索器）**：基于BM25稀疏检索方法，以问题描述为查询、源文件为文档，按词法相似度排序，实现粗粒度文件级检索。

2. **CodeChunker（代码分块器）**：采用层次化、语法感知的分块策略，将代码分解为函数、类、代码块等语义单元。支持C++、Python、Rust、Go四种语言，对于无法解析的结构使用基于正则的fallback分块。

3. **CodeReranker（代码重排序器）**：使用CodeBERT计算问题描述与代码块之间的稠密向量相似度，对候选块进行重排序。采用块级重排序策略，提供比文件级更细的粒度，在有限上下文窗口内更有效地引导补丁定位。

4. **Token Budget-Aware Context Manager（令牌预算感知上下文管理器）**：根据预设的令牌预算动态选择并打包代码块，调整分块粒度，并附加文件路径、函数签名等元数据信息后注入模型上下文。

### 关键评估指标

SWINGARENA定义三个核心指标来量化模型在对抗性编程场景中的表现：

**Best@k** — 衡量模型在多次独立尝试中至少成功一次的任务比例：

$$\mathrm{Best@}k = \frac{1}{|\mathcal{T}|} \sum_{t \in \mathcal{T}} \mathbf{1}\{\exists i \le k : \text{success}(t, i)\}$$

其中 $\mathcal{T}$ 为任务集，$\text{success}(t, i)$ 表示任务 $t$ 的第 $i$ 次尝试成功。

**提交者CI通过率（SPR）** — 提交者生成的补丁通过提交端CI检查的平均比例：

$$\mathrm{SPR} = \frac{1}{|\mathcal{T}|} \sum_{t \in \mathcal{T}} \frac{1}{|\mathcal{C}_{\mathrm{sub}}(t)|} \sum_{c \in \mathcal{C}_{\mathrm{sub}}(t)} \mathbf{1}\{\mathrm{pass}(t, c)\}$$

其中 $\mathcal{C}_{\mathrm{sub}}(t)$ 为任务 $t$ 的提交端CI检查集合。

**审阅者CI通过率（RPR）** — 审阅者生成的测试用例在黄金补丁上通过的平均比例：

$$\mathrm{RPR} = \frac{1}{|\mathcal{T}|} \sum_{t \in \mathcal{T}} \frac{1}{|\mathcal{C}_{\mathrm{rev}}(t)|} \sum_{c \in \mathcal{C}_{\mathrm{rev}}(t)} \mathbf{1}\{\mathrm{pass}(t, c)\}$$

其中 $\mathcal{C}_{\mathrm{rev}}(t)$ 为任务 $t$ 的审阅端CI检查集合。

SPR反映模型生成正确补丁的能力，RPR反映模型生成有效测试用例的能力，两者共同构成对战得分的基础。Best@k则从测试时计算扩展的角度衡量模型的潜力上限。

### 数据构建流水线

评估基准的构建经过四个阶段（图1）：

1. **仓库挖掘（Repository Mining）**：采集高质量GitHub仓库及关联的PR/Issue元数据。
2. **CI测试过滤（CI Test Filtering）**：仅保留通过完整CI检查的实例，确保基准质量。
3. **LLM过滤（LLM-as-a-Judge）**：使用Grok-3-beta评估问题陈述清晰度与任务难度。
4. **专家过滤（Expert Filtering）**：人工专家审核并校正LLM评估，剔除低质量样本。

最终从2,300个（Issue, PR）对中筛选出400个评估实例（每种语言100个），另提供100个样本用于消融实验。

## 实验与关键发现

### 对抗性编程对战：专有模型的主结果

SWINGARENA的核心评估采用提交者-审阅者双角色对抗协议，在400个高质量CI验证实例（四种语言各100个）上对四个专有LLM进行自我对战与交叉对战。Table 1报告了提交端CI通过率（SPR）、审查端CI通过率（RPR）和胜率三项核心指标。

![[assets/figures/papers/paper_list_l15_https_openreview_net_forum_id_YuxgSGFaqb/figures/003_Table_1.jpg]]
*Table 1: Evaluation of Code Submission vs. Test Submission Capabilities Among Proprietary LLMs*

在自我对战（self-play）场景中，所有模型均取得高胜率：Claude-3.5达到1.00，GPT-4o为0.97，DeepSeek-V3为0.96，Gemini-2.0为0.91。然而，SPR和RPR的差异揭示了更深层的行为模式。GPT-4o的SPR为0.68、RPR为0.71，胜率极高但SPR/RPR相对较低，表明其采用**激进补丁策略**：生成的补丁倾向于通过审查者测试来赢得对战，但补丁本身的CI正确性并不稳定。相比之下，Claude-3.5的SPR和RPR均为0.62，胜率却达到1.00，说明其补丁和测试生成更为保守但高度一致。Gemini-2.0的RPR高达0.72，胜率却最低（0.91），暗示其测试生成能力强于补丁生成能力。

交叉对战进一步验证了模型间的专长分化。GPT-4o作为提交者时，无论审查者是谁，胜率均≥0.90，确认其补丁生成的主导地位。DeepSeek-V3和Gemini-2.0则展现出更均衡的提交-审查能力，其SPR与RPR差距较小，反映出对代码正确性和CI稳定性的更高关注。

### 多语言代码生成能力：Best@3分析

Table 2展示了各模型在四种编程语言上的Best@3得分。DeepSeek-V3以平均0.59的最高分领跑，尤其在Rust（0.58）和Go（0.61）上表现突出，显示出稳健的多语言代码推理能力。GPT-4o在C++上得分0.63，与DeepSeek的0.64几乎持平，但在Go上仅为0.53，暴露出语言间的不均衡性。Claude-3.5平均得分0.55，整体略低于其他模型。

![[assets/figures/papers/paper_list_l15_https_openreview_net_forum_id_YuxgSGFaqb/figures/004_Table_2.jpg]]
*Table 2: Best@3 across Models and Languages*

值得注意的是，所有模型在Python上的Best@3均相对较低（0.52-0.54），这可能与Python仓库中动态类型和隐式依赖导致的上下文检索难度增加有关。Figure 3的Best@k胜率曲线显示，随着采样次数k从1增至10，胜率持续提升但边际收益递减，验证了测试时计算扩展的有效性。

### RACG检索增强模块消融

Table 3展示了RACG模块的消融结果。在C++任务上，引入RACG后Best@3从0.38提升至0.42，胜率从0.77提升至0.84，同时令牌占用减少12-18%。在所有语言上，RACG均带来了正向的Best@3和胜率增益，证实了语法感知分块、稠密重排序和令牌预算感知打包三者的协同效果。

![[assets/figures/papers/paper_list_l15_https_openreview_net_forum_id_YuxgSGFaqb/figures/006_Table_3.jpg]]
*Table 3: RACG Ablation Comparison*

Table 5和Table 6进一步拆解检索质量。采用Class-level分块的重排序策略在Top-10文件命中率上达到48.7%，远超BM25基线的20.7%，验证了块级重排序器在有限上下文下引导补丁定位的有效性。然而，在约15%的失败案例中，错误根因可追溯至检索阶段未能找到关键上下文，表明固定大小的Top-5文件检索在高度动态或大型单体仓库中仍存在覆盖盲区，需要进一步研究迭代检索或混合检索策略。

![[assets/figures/papers/paper_list_l15_https_openreview_net_forum_id_YuxgSGFaqb/figures/026_Table_5.jpg]]
*Table 5: File hit rates of different retrieval methods. Each value gives the fraction of queries whose correct file appears within the Top-2, Top-10, or Top-20 retrieved results*

![[assets/figures/papers/paper_list_l15_https_openreview_net_forum_id_YuxgSGFaqb/figures/027_Table_6.jpg]]
*Table 6: File hit rates of different retrieval methods. Each value gives the fraction of queries whose correct file appears within the Top-2, Top-10, or Top-20 retrieved results*

### 开源模型评估

Table 4报告了开源LLM的对抗性评估结果。开源模型在整体指标上低于专有模型，但不同参数规模的模型展现出与专有模型类似的行为分化趋势：部分模型更擅长补丁生成，另一些则在测试生成上更有优势。所有评估均使用统一的提示预算和解码参数（temperature=0），API失败案例已排除且排名不变，确保了对比的公平性。

### 失败模式与局限

主要失败模式可归纳为三类：（1）检索阶段的上下文缺失（约15%案例），RACG的固定检索策略无法捕获所有关键文件；（2）审查者测试生成质量波动，尽管设置了CI质量门控，某些微妙的代码风格违规或非确定性行为仍可能通过过滤；（3）act模拟的CI流水线与真实执行环境之间存在偏差，可能忽略特定的环境依赖或非确定性因素。这些失败模式为后续研究指明了方向：设计更动态的自适应检索策略，以及更精细的审查者测试质量评估机制。

## 定位与知识库关联

### 与现有基准的定位关系

SWINGARENA 的核心设计动机源于对现有 LLM 代码评估范式的系统性反思。以 **SWE-Bench** 为代表的传统基准依赖静态单元测试套件或一次性代码生成评估，其根本瓶颈在于忽略了真实软件工程中的三个关键维度：完整的 CI 流水线验证、协作式迭代的提交-审阅循环，以及对抗性测试所暴露的边界行为。SWINGARENA 通过引入“提交者-审阅者”双智能体对抗协议，将评估从“能否通过固定测试”推进到“能否在动态对抗中生存”，从而填补了现有基准在真实工作流模拟上的结构性空白。

在上下文检索层面，现有方案多采用朴素的全文输入或简单的 BM25 检索，且通常局限于单一编程语言。SWINGARENA 提出的 **RACG**（Retrieval-Augmented Code Generation）模块通过语法感知分块、稠密重排序和令牌预算感知打包的组合策略，在多语言场景（C++、Python、Rust、Go）下实现了更精准的长上下文管理。这一设计直接回应了大型代码库中“检索质量成为性能瓶颈”的现实挑战——实验表明约 15% 的失败案例可追溯至检索阶段未能定位关键上下文。

在验证环境上，SWINGARENA 摒弃了手动 Docker 配置或单语言单元测试执行的简化方案，转而通过 `act` 工具在隔离容器中运行仓库原生的 CI 流水线（GitHub Actions、Travis CI），并支持多语言执行逻辑（如 Rust 的 cargo 系统）。这种设计确保了评估的可复现性，同时更贴近工业级开发实践。

### 适用边界与泛化能力

SWINGARENA 的评估框架在以下条件下展现出较强的有效性：

- **多语言覆盖**：数据集包含 C++、Python、Rust、Go 四种语言各 100 个评估实例，模型在不同语言上的表现差异显著（如 DeepSeek-V3 在 Go 上 Best@3 达 0.61，而在 Python 上仅为 0.52），表明框架能够捕捉语言特异性的推理能力差异。
- **模型行为差异化**：对抗性协议成功暴露了不同模型的策略偏好——GPT-4o 作为提交者时在所有对局中胜率均 ≥0.90，但 SPR/RPR 相对较低（0.65/0.55），显示其倾向于激进的“高胜率低稳健性”补丁策略；而 DeepSeek-V3 和 Gemini 则表现出更均衡的代码正确性与 CI 稳定性。
- **检索增强的增益边界**：RACG 在 C++ 任务上将 Best@3 从 0.38 提升至 0.42，胜率从 0.77 提升至 0.84，同时减少 12-18% 的令牌占用。但这一增益依赖于固定大小的检索配置（5 个文件，16 个块），对于高度动态或非结构化的单体仓库，固定窗口可能无法捕获所有关键上下文。

框架的适用边界主要体现在：

- **CI 模拟的保真度限制**：尽管通过 `act` 模拟完整 CI 流水线确保了可复现性，但与真实 CI 执行相比仍可能忽略某些环境偏差或非确定性因素。
- **审查者测试质量的依赖**：对抗性评估中审查者生成的测试用例质量直接影响结果的可靠性。虽然设置了质量门控，但某些微妙的代码风格违规或非确定性行为可能无法完全过滤。
- **检索策略的静态性**：当前 RACG 采用固定 Top-5 文件检索策略，对于需要跨多个文件追踪调用链的复杂问题，可能遗漏关键上下文。

### 关键局限与开放问题

**已识别的局限**：

1. **检索瓶颈未完全解决**：RACG 的性能受限于其组成部分——BM25 的词汇匹配局限性、基于正则的 fallback 分块策略的脆弱性，以及通用 CodeBERT 重排序器在领域特定代码上的语义理解不足。约 15% 的失败案例根因可追溯到检索阶段，表明需要更动态的检索机制。
2. **固定上下文窗口的刚性**：当前令牌预算感知管理器采用固定大小的块选择策略，无法根据问题复杂度自适应调整检索粒度和范围。
3. **对抗性协议的单维度评分**：当前评分机制（提交者 ±1，审查者 ±1）虽然简洁，但未能细粒度地度量代码风格、安全性、覆盖率等仓库原生门禁的通过情况。

**值得追踪的开放问题**：

- 如何为处理极度复杂的单体仓库或低质量代码设计更动态的自适应检索策略（如迭代检索、分层检索、基于依赖图的上下文扩展）？
- 观察到的模型行为模式差异（GPT-4o 激进补丁 vs. DeepSeek 稳健性）是否与训练数据分布或架构特性存在系统性关联？这一问题对于理解 LLM 在软件工程任务中的能力来源具有基础意义。
- 如何将多语言代码开发、提交与审查的完整工作流更深度地整合到评价体系中，例如引入代码审查评论的生成与响应、多轮迭代的冲突解决等更丰富的交互维度？
- 对抗性 CI 协议能否扩展到更细粒度的质量门禁度量，如安全漏洞检测、性能回归测试、代码覆盖率阈值等？

## 原文 PDF

![[paperPDFs/ICLR_2026/SWINGARENA_Adversarial_Programming_Arena_for_Long_context_GitHub_Issue_Solving.pdf]]
