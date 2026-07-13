---
title: "NERFIFY: A Multi-Agent Framework for Turning NeRF Papers into Code"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/NERFIFY_A_Multi_Agent_Framework_for_Turning_NeRF_Papers_into_Code.pdf
project_link: null
code_link: null
aliases:
- NERFIFY
tags:
- CVPR_2026
- topic/other_unclear
- topic/other_unclear/general
core_operator: 将 Nerfstudio 框架形式化为上下文无关文法（CFG），强制 LLM 生成满足接口合约和模块组合的代码，从根本上消除架构错误。
primary_logic: 通过领域特化的多智能体系统——CFG 约束代码生成、图思维（GoT）多文件拓扑协作、组合式引用图遍历恢复隐藏依赖、视觉驱动的 PSNR/跨视角反馈——可以在几分钟内自动从论文生成与专家实现质量匹配的可训练 NeRF 插件（PSNR 差距 ≤0.5 dB，SSIM 差距 ≤0.2）。
claims:
- NERFIFY 在 NERFIFY-BENCH 上实现 100% 可训练率，而所有基线（Paper2Code、AutoP2C、GPT-5、O1）均无法生成可训练代码。
- 在无公开实现的论文上，NERFIFY 生成的代码与专家人工实现的视觉质量差距 ≤0.5 dB PSNR 和 ≤0.02 SSIM。
- 消融实验表明：移除 In-Context 示例导致语义得分从 0.98 降至 0.71，可训练率降至 90%；移除引用恢复使正确实现率降至 0.65。
- NERFIFY-BENCH Set 1 (无公开代码) 上 PSNR = 26.12 (KeyNeRF)
---

# NERFIFY: A Multi-Agent Framework for Turning NeRF Papers into Code

> [!tip] 核心洞察
> 通过领域特化的多智能体系统——CFG 约束代码生成、图思维（GoT）多文件拓扑协作、组合式引用图遍历恢复隐藏依赖、视觉驱动的 PSNR/跨视角反馈——可以在几分钟内自动从论文生成与专家实现质量匹配的可训练 NeRF 插件（PSNR 差距 ≤0.5 dB，SSIM 差距 ≤0.2）。

| 字段 | 内容 |
|------|------|
| 中文题名 | NERFIFY：将NeRF论文转化为代码的多智能体框架 |
| 英文题名 | NERFIFY: A Multi-Agent Framework for Turning NeRF Papers into Code |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2603.00805) |
| Topic | #topic/other_unclear #topic/other_unclear/general |
| Method | NERFIFY |
| Dataset | NERFIFY-BENCH Set 1, NERFIFY-BENCH Set 2, NERFIFY-BENCH 全部 30 篇论文 |

> [!tip] 效果简介
> - NERFIFY-BENCH Set 1 (无公开代码) 上，PSNR 26.12 (KeyNeRF) vs 26.00 (论文报告) (+0.12)。
> - NERFIFY-BENCH Set 1 上，SSIM 0.90 vs 0.89 (论文报告) (+0.01)。
> - NERFIFY-BENCH Set 2 (非 Nerfstudio 实现) 上，PSNR 30.13 (l0-Sampler) vs 29.21 (原始作者实现) (+0.92)。

## 概要

将神经辐射场（NeRF）论文转化为可训练代码是一项高度专业化的工程任务，即使对领域专家也需要数周的努力。核心瓶颈在于：NeRF 实现涉及体渲染、计算机视觉与神经优化的强领域耦合——一个错误的激活函数或光线求交就可能导致 NaN 梯度或退化解，而调试周期长达 24–48 小时。现有的通用论文到代码系统（如 **Paper2Code** (Seo et al., arXiv 2025)、**AutoP2C** (Lin et al., arXiv 2025)、GPT-5 单次生成、OpenAI O1）虽然能产生语法正确的 Python 代码，但缺乏架构约束和依赖解析能力，95% 无法训练。

**NERFIFY** 提出了一个领域特化的多智能体框架，其核心洞察是：将 Nerfstudio 框架形式化为**上下文无关文法（CFG）**，强制 LLM 在接口合约和模块组合约束下生成代码，从根本上消除架构错误。该框架通过四个关键机制实现突破：

1. **CFG 约束代码生成**：以 Nerfstudio 的架构模式作为语法规则，确保生成代码满足模块接口和类型约束。
2. **图思维（GoT）多智能体协作**：按有向无环图（DAG）的拓扑顺序生成多文件仓库，逐步冻结接口、实现并集成测试。
3. **组合式引用恢复**：自动遍历引用图，递归检索被引用论文中的隐藏依赖组件（如 Mip-NeRF 360 的提议网络）。
4. **视觉驱动反馈**：通过 PSNR 局部极小值分析、跨视角几何验证和 VLM 语义诊断，迭代修复直至视觉质量达标。

在 **NERFIFY-BENCH** 基准上，NERFIFY 实现了 **100% 可训练率**，而所有基线系统均为 0%。在无公开代码的论文上，NERFIFY 生成的代码与专家人工实现的视觉质量差距在 **±0.5 dB PSNR 和 ±0.02 SSIM** 以内（如 KeyNeRF: PSNR 26.12 vs. 论文 26.00, SSIM 0.90 vs. 0.89），证明了自动生成的 NeRF 插件可以达到专家级质量。消融实验进一步验证了各模块的关键作用：移除 In-Context 示例后语义得分从 0.98 降至 0.71，移除引用恢复后正确实现率降至 0.65，将 GoT 替换为单次生成后语义得分骤降至 0.45。

该方法目前高度依赖 Nerfstudio 架构，向其他框架的迁移能力尚未验证；视觉驱动反馈依赖烟雾训练（3k 迭代）仍需一定计算时间，完全达到论文报告 PSNR 可能需要额外迭代。



### 神经辐射场的实现困境

神经辐射场（NeRF）已成为三维场景表示与新颖视图合成的核心范式，其研究产出呈爆发式增长——仅 NeRF 相关 arXiv 论文的日更新仓库（[nerf-arxiv-daily](https://github.com/wangqiannudt/nerf-arxiv-daily)）即反映了这一趋势。然而，从论文到可运行代码的转化却构成了领域发展的隐性瓶颈：手动将一篇 NeRF 论文实现为可训练代码，通常需要数周的专业工程努力（Figure 1 左），涵盖体渲染管线搭建、采样策略调优、网络架构匹配与数值稳定性保障等高度耦合的环节。

这一困境的根源在于 NeRF 实现的**强领域耦合特性**。体渲染、计算机视觉与神经优化在 NeRF 中深度交织，一个错误的激活函数选择或光线求交实现即可导致灾难性失败——梯度变为 NaN 或模型退化为平凡解——且此类错误的调试周期往往长达 24–48 小时。这种脆弱性使得通用代码生成方法难以胜任。

### 通用论文到代码系统的结构性失败

近年来，基于大型语言模型的论文到代码系统（如 **Paper2Code**（Seo et al., arXiv 2025）、**AutoP2C**（Lin et al., arXiv 2025）以及 **GPT-5** 和 **O1** 的单次生成范式）在通用软件工程任务中取得了显著进展。然而，当面对 NeRF 论文时，这些系统暴露出结构性缺陷：它们生成的代码缺乏架构约束与依赖解析，约 95% 无法训练（Table 2）。

其失败可归结为三个根本原因：

1. **无约束生成**：基线系统采用单次 LLM 调用生成整个代码库，未对模块组合、接口合约或张量形状一致性施加任何领域约束，导致生成的代码虽语法正确但语义断裂。
2. **依赖盲区**：NeRF 论文普遍构建于先前工作的组件之上（如 Mip-NeRF 360 的提议网络、Instant-NGP 的多分辨率哈希编码），基线系统仅依赖目标论文的文本信息，无法自动检索和集成这些隐藏依赖。
3. **缺乏视觉反馈**：现有系统最多进行编译错误检查，无法感知渲染质量——而 NeRF 的正确性本质上是视觉的，仅凭语法正确性无法保证 PSNR 或跨视角几何一致性。

### 本文动机

上述缺口揭示了一个明确的需求：**将 NeRF 领域的架构知识形式化为机器可执行的约束，并构建能够理解、检索、组合与验证的多智能体系统**。NERFIFY 的设计动机正是填补这一空白——通过将 Nerfstudio 框架形式化为上下文无关文法（CFG）以强制接口合约，通过组合式引用图遍历以恢复传递依赖，并通过视觉驱动的 PSNR/跨视角反馈以迭代逼近专家级质量，从而在几分钟内自动完成从论文到可训练 NeRF 插件的全流程转化（Figure 1 右）。



## 核心方法与创新机理

NERFIFY 相对于通用论文到代码生成系统的核心创新，在于将 **NeRF 领域特定的架构知识形式化为生成约束**，并通过**多智能体协作与视觉反馈闭环**，从根本上解决了通用方法“能生成代码但无法训练”的瓶颈。以下从四个关键的 changed slots 展开分析。

### 1. 代码生成策略：从单次 LLM 调用到 CFG 约束的图思维多智能体协作

通用基线（Paper2Code、AutoP2C、GPT-5、O1）均采用**单次 LLM 调用生成整个代码库**的策略，缺乏对 NeRF 框架架构约束的理解。这导致生成的代码虽然在语法上可能正确，但存在接口不匹配、张量形状错误、模块组合违反框架约定等问题，最终表现为 **95% 的生成代码无法训练**（Table 2）。

NERFIFY 的核心改变是将 **Nerfstudio 框架形式化为上下文无关文法（CFG）**，并将代码生成过程重构为**图思维（Graph-of-Thought, GoT）多智能体协作**。具体而言：

- **CFG 形式化**（Stage 1）：将 Nerfstudio 的模块组合模式、接口合约编码为形式文法，作为 LLM 生成代码的硬约束。这从根本上消除了架构层面的错误可能性。
- **GoT 多智能体合成**（Stage 3）：主智能体按依赖 DAG 的拓扑顺序编排专用文件智能体，每个文件经历“接口冻结→实现→集成测试”三个阶段。接口冻结阶段确立 API 合约，实现阶段进行张量形状和梯度检查，集成测试阶段运行冒烟测试并自动修复。Figure 4 展示了这一渐进式构建过程。

**因果机制**：CFG 约束将代码生成从“自由文本生成”转化为“受控的语法推导”，确保每个模块都满足框架的接口契约。GoT 多智能体则通过分治策略将复杂仓库的生成分解为可验证的子任务，避免了单次生成中的错误传播。

**证据强度**：消融实验（Table 5）表明，将 GoT 替换为单次生成后，语义实现得分从 0.98 **骤降至 0.45**，可训练率从 100% 降至 60%。这一降幅直接证明了多智能体拓扑协作是不可替代的核心机制。

### 2. 依赖解析：从孤立论文理解到组合式引用图遍历

通用方法仅依赖目标论文的文字信息来推断所需组件，完全忽略了 NeRF 论文之间**深度耦合的依赖关系**。例如，实现 K-Planes 需要从 7 篇直接引用论文和 12 篇传递依赖论文中检索组件（Figure 3），通用方法对此无能为力。

NERFIFY 提出**组合式依赖解析**（Stage 2），通过递归遍历引用图自动检索所有必需的组件：

$$
\mathrm{Dependencies}(c_i) = \{c_i\} \cup \bigcup_{d \in \mathrm{cited}(c_i)} \mathrm{Dependencies}(d)
$$

该递归定义确保系统能够发现隐藏的传递依赖——例如，目标论文引用了 Mip-NeRF 360，而 Mip-NeRF 360 的提议网络（proposal network）是实现所必需的组件，但目标论文正文中可能并未显式描述。

**因果机制**：引用恢复将“论文理解”从单文档信息抽取扩展为**跨文档知识整合**，使得系统能够自动补全实现所需的全部组件，而非仅依赖目标论文中的不完整描述。

**证据强度**：消融实验（Table 5）显示，移除引用恢复后，正确实现率 C 降至 **0.65**，意味着超过三分之一的组件无法正确实现。这验证了引用恢复对于处理 NeRF 论文间强依赖关系的必要性。

### 3. 反馈与修复：从无反馈到视觉驱动的迭代精炼

通用基线在代码生成后**没有任何反馈机制**，或仅进行编译错误检查。然而，NeRF 实现中一个错误的激活函数或光线求交可能导致 NaN 梯度或退化解，这些语义错误在编译阶段完全不可见，却需要 24-48 小时的调试周期才能发现。

NERFIFY 引入**视觉驱动反馈**（Stage 4），通过三个互补的分支进行诊断和修复：

- **度量分支**：构建 PSNR/SSIM 密集误差场，定位局部极小值区域
- **几何分支**：实施跨视角一致性验证，检测多视图几何冲突
- **语义分支**：利用 VLM（Qwen3）进行语义级伪影诊断

修复循环持续进行，直到批评智能体不再产生反馈、达到最大迭代次数、或实现达到论文报告的 PSNR 目标。

**因果机制**：视觉反馈将调试从“人工检查渲染结果”自动化，使得系统能够在几分钟内完成原本需要专家数天才能完成的错误定位和修复。

**证据强度**：Table 1 显示，在无公开代码的论文上，NERFIFY 生成的代码与专家人工实现的视觉质量差距 **≤0.5 dB PSNR 和 ≤0.02 SSIM**。这一结果直接证明了视觉反馈闭环的有效性——没有这一机制，初始生成的代码几乎不可能达到专家级质量。

### 4. 知识表示：从零领域知识到 CFG + In-Context 示例

通用方法对 NeRF 领域没有任何先验知识，完全依赖 LLM 的通用代码能力。NERFIFY 构建了**领域知识库 K**，包含两部分：

- **Nerfstudio CFG**：编码框架的模块组合规则和接口合约
- **精选论文-代码对**：作为 In-Context 示例，指导 LLM 理解从论文描述到代码实现的映射模式

**因果机制**：In-Context 示例提供了“论文创新点→代码实现”的映射模板，CFG 提供了实现必须遵守的架构边界。两者协同作用：示例降低了对 LLM 推理能力的要求，CFG 防止了示例引导下的架构越界。

**证据强度**：消融实验（Table 5）表明，移除 In-Context 示例后，语义得分从 0.98 降至 **0.71**，可训练率降至 90%。这表明即使有 CFG 约束，缺少领域示例仍会导致实现质量的显著退化。

### 创新总结

NERFIFY 的四项 changed slots 构成了一条完整的因果链：**CFG + In-Context 示例**提供领域知识基础 → **组合式引用恢复**补全隐藏依赖 → **GoT 多智能体**在架构约束下按拓扑顺序生成代码 → **视觉驱动反馈**迭代修复语义错误。这一链条使得 NERFIFY 在 NERFIFY-BENCH 上实现了 **100% 可训练率**，而所有基线均为 0%（Table 2），从根本上解决了通用论文到代码系统在 NeRF 领域的“能生成但不可训练”问题。



NERFIFY 是一个将 NeRF 论文自动转化为可训练代码的四阶段多智能体系统。其核心设计理念是：**通用论文到代码系统无法生成可训练的 NeRF 实现，因为 NeRF 涉及体渲染、计算机视觉和神经优化的强领域耦合——一个错误的激活函数或光线求交就会导致 NaN 梯度或退化解，且调试周期长达 24–48 小时**。现有基线方法（如 **Paper2Code** (Seo et al., arXiv 2025)、**AutoP2C** (Lin et al., arXiv 2025)、GPT-5 单次生成、OpenAI o1）生成的可执行代码缺乏架构约束和依赖解析，95% 无法训练。

NERFIFY 的关键因果调节变量在于：**将 Nerfstudio 框架形式化为上下文无关文法（CFG），强制 LLM 生成满足接口合约和模块组合的代码，从根本上消除架构错误**。整个流水线由四个顺序阶段构成，如 Figure 2 所示：

![[assets/figures/papers/paper_list_l2643_https_arxiv_org_abs_2603_00805/figures/002_Figure_2.jpg]]
*Figure 2: NERFIFY converts NeRF papers into code through four stages: (1) Agent parses and summarizes PDFs into simple markdown, CFG from Nerfstudio and curated paper-code pairs as In-Context examples are saved in K (2) Compositional dependency resolution traverses citation graphs to retrieve missing components from referenced papers, (3) GoT code synthesis generates repository files through specialized agents operating in topological order (4) Visual refinement iteratively patches artifacts until achieving expert-level quality*

### 阶段 1：CFG 形式化与上下文学习

系统首先构建领域知识库 $K$，包含两部分核心资产：
- **Nerfstudio CFG**：将 Nerfstudio 的架构模式（如 Model、Field、Sampler、RayGenerator 等模块及其接口合约）形式化为上下文无关文法，作为后续代码生成的硬约束。
- **In-Context 示例**：整理已有的论文-代码对，作为 LLM 生成时的领域参考。

### 阶段 2：组合式依赖解析

该阶段构建目标论文的引用依赖图，通过递归遍历引用链自动检索所需组件。依赖项的递归定义为：

$${ \mathrm { D e p e n d e n c i e s } } ( c _ { i } ) = \{ c _ { i } \} \cup \bigcup _ { d \in { \mathrm { c i t e d } } ( c _ { i } ) } { \mathrm { D e p e n d e n c i e s } } ( d )$$

即一篇论文的依赖集包括其自身及其所有引用论文的依赖并集。例如，实现 K-Planes 需要从 7 个直接依赖（Plenoxels、TensoRF、Instant-NGP、Mip-NeRF 360、DyNeRF、EG3D、NeRF-W）及 12 篇传递依赖论文中检索组件（见 Figure 3）。

### 阶段 3：语法引导的仓库生成（GoT 多智能体）

这是系统的核心生成阶段。主智能体（master agent）协调多个专用文件智能体（file-agents），按照依赖 DAG 的拓扑顺序逐步构建完整的 NeRF 仓库。每个文件经历四个子步骤（见 Figure 4）：
1. **DAG 构建**：将论文组件映射到 Nerfstudio 依赖关系。
2. **接口冻结**：按拓扑顺序建立 API 合约。
3. **实现**：生成经过形状/梯度验证的代码。
4. **集成测试**：运行冒烟测试并自动修复。

仓库的形式化定义为 $\{ \mathcal { C } \} = ( F , G ), \quad F = \{ f _ { 1 } , f _ { 2 } , \dots , f _ { n } \}$，其中 $F$ 为文件集，$G$ 为有向无环依赖图，确保可编译性。

### 阶段 4：视觉驱动反馈

生成的可训练代码进入迭代精炼循环，通过三个分支诊断并修复视觉伪影：
- **度量分支**：构建 PSNR/SSIM 密集误差场，定位局部极小值区域。
- **几何分支**：实施跨视角一致性验证（Cross-View Artifact Consensus）。
- **语义分支**：利用 Qwen3 VLM 进行语义诊断。

精炼循环持续进行，直到满足以下条件之一：(1) 诊断智能体不再产生新反馈；(2) 达到最大迭代次数；(3) 实现达到原论文报告的 PSNR 目标。

### 输入输出流

- **输入**：目标 NeRF 论文 PDF（包含文本 $T(\mathcal{P})$、视觉 $I(\mathcal{P})$、数学 $Q(\mathcal{P})$ 和参考文献 $B(\mathcal{P})$ 四个组成部分）。
- **中间表示**：经过解析和摘要的简化 Markdown，以及引用依赖图中检索到的组件。
- **输出**：完整的、可直接训练的 Nerfstudio 插件仓库，满足接口合约并通过冒烟测试。

消融实验证实了各阶段的必要性：移除 In-Context 示例后语义得分从 0.98 降至 0.71，可训练率降至 90%；移除引用恢复后正确实现率降至 0.65；移除冒烟测试后可训练率降至 60%；将 GoT 替换为单次生成后语义得分骤降至 0.45（Table 5）。

### 补充图表

![[assets/figures/papers/paper_list_l2643_https_arxiv_org_abs_2603_00805/figures/001_Figure_1.jpg]]
*Figure 1: Overview. Manual NeRF implementation requires weeks of specialized effort (left). Existing paper-to-code systems fail to produce trainable code. NERFIFY automates this process through grammar-constrained synthesis and compositional citation recovery, generating fully trainable Nerfstudio plugins in minutes (right)*



NERFIFY 将 NeRF 论文自动转化为可训练代码的核心机制建立在四个形式化基础之上：仓库的图表示、论文的结构化信息抽取、组合式依赖递归，以及多智能体拓扑生成。以下逐一展开其关键模块与支撑公式。

### 仓库的形式化定义

NERFIFY 将代码仓库抽象为一个由文件集及其有向无环依赖图构成的二元组。这一形式化是后续所有语法约束和拓扑生成的基础。

$$
{ \mathcal { C } } = ( F , G ) , \quad F = \{ f _ { 1 } , f _ { 2 } , \dots , f _ { n } \}
$$

其中 $F$ 为仓库中所有源文件的集合，$G$ 为文件间的有向无环依赖图。任何合法的 Nerfstudio 插件仓库必须满足 $G$ 中无环，否则无法编译。这一约束在 Stage 3 的 DAG 构建阶段被强制检查，从根本上消除了因模块循环引用导致的架构错误。

### 论文的结构化表示

为让多智能体系统准确理解论文内容，NERFIFY 将每篇目标论文 $\mathcal{P}$ 解析为四元组结构化信息：

$$
\mathcal { E } ( \mathcal { P } ) = \langle T ( \mathcal { P } ) , I ( \mathcal { P } ) , Q ( \mathcal { P } ) , B ( \mathcal { P } ) \rangle
$$

四个分量分别对应：$T(\mathcal{P})$ 为文本组件（标题、段落、算法块、图注、参考文献），$I(\mathcal{P})$ 为视觉组件（架构图、结果图等），$Q(\mathcal{P})$ 为数学组件（公式、损失函数定义、超参数设定），$B(\mathcal{P})$ 为参考文献组件。其中文本组件进一步细化为：

$$
T ( \mathcal { P } ) = \langle H , \{ p _ { i } \} _ { i = 1 } ^ { n _ { p } } , \{ a _ { \ell } \} _ { \ell = 1 } ^ { n _ { a } } , \{ c _ { k } \} _ { k = 1 } ^ { n _ { c } } , \{ r _ { m } \} _ { m = 1 } ^ { n _ { m } } \rangle
$$

这里 $H$ 为论文标题，$\{p_i\}$ 为正文段落序列，$\{a_\ell\}$ 为算法块（伪代码），$\{c_k\}$ 为图注，$\{r_m\}$ 为引用条目。这一结构化表示使得后续的依赖解析和代码生成能够精确锚定论文中的每个关键信息源。

### 组合式依赖解析的递归定义

NeRF 论文的一个核心挑战是其深度引用链：实现一篇论文往往需要其引用论文中的组件（如 Mip-NeRF 360 的提议网络、Instant-NGP 的哈希编码器）。NERFIFY 通过递归定义依赖集来自动遍历引用图：

$$
{ \mathrm { D e p e n d e n c i e s } } ( c _ { i } ) = \{ c _ { i } \} \cup \bigcup _ { d \in { \mathrm { c i t e d } } ( c _ { i } ) } { \mathrm { D e p e n d e n c i e s } } ( d )
$$

该公式的含义是：一篇被引论文 $c_i$ 的依赖集包含其自身，以及其引用论文的依赖集的并集。通过这一递归定义，NERFIFY 能够自动发现并检索所有传递依赖中所需的采样器、编码器、损失函数等组件。Figure 3 以 K-Planes 为例展示了这一过程：实现该论文需要从 7 个直接依赖和总计 12 篇传递依赖论文中检索组件。

![[assets/figures/papers/paper_list_l2643_https_arxiv_org_abs_2603_00805/figures/003_Figure_3.jpg]]
*Figure 3: NeRF citation dependency graphs. Implementing K-Planes requires retrieving components from 7 direct dependencies (Plenoxels, TensoRF, Instant-NGP, Mip-NeRF 360, DyNeRF, EG3D, NeRF-W) and 12 total papers with transitive dependencies. Our compositional citation recovery automatically traverses such graphs to identify and retrieve all necessary components*

### 图思维多智能体代码合成

Stage 3 的 GoT（Graph-of-Thought）多智能体系统是 NERFIFY 的核心执行引擎。主智能体根据依赖图 $G$ 的拓扑顺序编排专用文件智能体，每个文件智能体经历四个子阶段：

1. **DAG 构建**：将论文组件映射到 Nerfstudio 的 CFG 约束下的模块依赖关系。
2. **接口冻结**：按拓扑序确定各模块的 API 合约（函数签名、张量形状），后续智能体只能依赖已冻结的接口。
3. **实现与验证**：生成代码并进行形状检查和梯度检查，确保张量维度匹配且反向传播无 NaN。
4. **集成测试**：运行冒烟测试并自动修复编译和运行时错误。

这一流水线确保了多文件仓库在生成过程中始终保持可编译性和接口一致性。消融实验表明，将 GoT 替换为单次生成后，语义得分从 0.98 骤降至 0.45（Table 5），验证了拓扑协作的必要性。

### 视觉驱动反馈的度量分支

Stage 4 的度量分支通过构建稠密误差场来定位视觉伪影的根源。其核心机制是对渲染图像与真值图像计算逐像素 PSNR/SSIM 误差图，识别局部极小值区域，并将这些区域的空间坐标反馈给修复智能体，指导其对特定模块（如密度场、颜色网络）进行定向修补。反馈循环持续到满足以下任一终止条件：(1) 诊断智能体不再产生新反馈；(2) 达到最大迭代次数；(3) 实现达到原论文报告的 PSNR 目标。

### 补充图表

![[assets/figures/papers/paper_list_l2643_https_arxiv_org_abs_2603_00805/figures/004_Figure_4.jpg]]
*Figure 4: Graph-of-Thought (GoT) Multi-Agent Code Synthesis. The master agent orchestrates specialized file-agents that progressively build a NeRF repository over k steps. Each step shows files being created or modified through four stages: (1) DAG Construction maps papers to Nerfstudio component dependencies, (2) Interface Freeze establishes API contracts in topological order, (3) Implementation generates validated code with shape/gradient checks, (4) Integration Testing runs smoke tests with automated repair. Files evolve from minimal interfaces to complete implementations as agents coordinate through the dependency graph, producing runnable NeRF plugins*



## 实验与关键发现

### 评估设置与基准

NERFIFY-BENCH 包含 30 篇 NeRF 论文，分为两个子集：**Set 1** 为无公开代码实现的论文，**Set 2** 为已有非 Nerfstudio 实现的论文。所有评估严格遵循论文中的指标（PSNR、SSIM、LPIPS），在相同数据集和烟雾训练设定（3k 迭代）下进行，未使用专家反馈。对于 Set 1，采用专业人工复现作为参考实现，以避免数据污染并保证公平对比。

基线系统包括 **Paper2Code**（Seo et al., arXiv 2025）、**AutoP2C**（Lin et al., arXiv 2025）、**GPT-5（单次生成）** 和 **O1**（OpenAI o1 推理模型）。

### 核心结果：可训练性与视觉质量

**可执行性**是 NERFIFY 最根本的优势。Table 2 显示，NERFIFY 在全部 30 篇论文上实现 **100% 编译与可训练**，而所有基线系统（Paper2Code、AutoP2C、GPT-5、O1）均无法生成可训练的代码——尽管部分基线能产生语法正确的 Python，但缺乏架构约束和依赖解析导致代码无法运行。

**视觉质量**方面，Table 1 展示了 Set 1 上的定量对比。以 KeyNeRF 为例，NERFIFY 生成的实现达到 PSNR 26.12、SSIM 0.90，与论文报告的 26.00 / 0.89 相当，甚至略有超出。整体上，NERFIFY 与专家人工实现的视觉质量差距控制在 **±0.5 dB PSNR 和 ±0.02 SSIM** 以内。

Table 3 进一步展示了 Set 2 上与原始作者实现的对比。在 l0-Sampler 上，NERFIFY 实现达到 PSNR 30.13，**超越**原始作者实现的 29.21（+0.92 dB），表明 NERFIFY 不仅能复现，还能通过 Nerfstudio 框架的优化基础设施获得额外增益。

![[assets/figures/papers/paper_list_l2643_https_arxiv_org_abs_2603_00805/figures/008_Table_3.jpg]]
*Table 3: Comparison with existing implementations. Evaluation of NERFIFY against original author repositories or gold-standard implementations*

### 创新点覆盖率分析

Table 4 从更细粒度评估代码生成质量，引入五项指标：
- **C**：正确实现率
- **I**：部分正确实现率
- **M**：缺失组件率
- **W**：超参数权重匹配精度（$W = |\{ n \in \mathcal{N} : |\theta_n - \hat{\theta}_n| < 0.1 |\theta_n| \}| / |\mathcal{N}|$）
- **ScoreLLM**：基于 LLM 的语义实现得分（$\textstyle (\sum_{i=1}^n w_i \cdot s_i) / \sum_{i=1}^n w_i$），按组件重要性加权

![[assets/figures/papers/paper_list_l2643_https_arxiv_org_abs_2603_00805/figures/009_Table_4.jpg]]
*Table 4: Novelty coverage analysis across NERFIFY-BENCH papers. For each baseline system, we report: C (Correct implementation rate), I (Incorrect/partial implementation rate), M (Missing component rate), W (Hyperparameter weight match accuracy), and ScoreLLM (overall semantic implementation score on 0-1 scale). NERFIFY achieves perfect or near-perfect scores (C=1.00, M=0.00) across all papers, while generic baselines show significant component omissions (M=0.12-0.90 for most methods) and lower implementation fidelity. Metrics are computed over all novel components identified in each paper, with weights derived from paper emphasis and experimental validation*

NERFIFY 在所有论文上实现 **C=1.00、M=0.00** 的完美或接近完美的创新点覆盖率，而基线系统普遍存在大量缺失组件和错误实现。

### 消融实验：各组件的因果贡献

Table 5 的消融实验揭示了四个核心组件的因果效应：

![[assets/figures/papers/paper_list_l2643_https_arxiv_org_abs_2603_00805/figures/010_Table_5.jpg]]
*Table 5: Component ablation study. We evaluate the impact of each system component on synthesis quality and efficiency. Numbers are averaged over 10 papers from NERFIFY-BENCH*

1. **移除 In-Context 示例**：语义得分从 0.98 骤降至 0.71，可训练率降至 90%。这表明领域特定的论文-代码对作为上下文示例对 LLM 生成正确接口和实现模式至关重要。

2. **移除引用恢复**：正确实现率 C 降至 0.65。组合式引用图遍历是解决隐藏依赖的核心机制——许多 NeRF 论文依赖引用论文中的组件（如 Mip-NeRF 360 的提议网络），缺少此步骤将导致大量组件无法正确实现。

3. **移除冒烟测试**：可训练率骤降至 60%。接口合约验证和集成测试是确保多文件仓库可编译、可训练的最后防线。

4. **将 GoT 替换为单次生成**：语义得分暴跌至 0.45。这直接验证了图思维多智能体协作的必要性——单次 LLM 调用无法正确处理多文件之间的拓扑依赖和接口约束。

### 视觉驱动反馈的有效性

视觉驱动反馈通过三个分支迭代修复伪影：**度量分支**构建密集 PSNR/SSIM 误差场定位局部极小值；**几何分支**实施跨视角一致性验证；**语义分支**利用 Qwen3 VLM 进行诊断。反馈循环持续至无新反馈、达到最大迭代次数或满足论文报告的 PSNR 目标。Figure 5 的视觉对比显示，经过反馈修复后，NERFIFY 生成的渲染结果与专家实现几乎无法区分。

![[assets/figures/papers/paper_list_l2643_https_arxiv_org_abs_2603_00805/figures/007_Figure_5.jpg]]
*Figure 5: Visual Comparison of NERFIFY and Human Implementation. Left: Ground Truth Image, Middle: Expert Implementation, Right: Agent Implementation*

### 失败模式与局限

尽管 NERFIFY 在 NERFIFY-BENCH 上实现 100% 可训练率，仍存在两个已知局限：
- **框架依赖**：当前系统高度依赖 Nerfstudio 架构，无法直接迁移到非 Nerfstudio 框架的 radiance field 方法。
- **计算成本**：视觉驱动反馈依赖烟雾训练（3k 迭代），仍需要一定计算时间；完全达到论文报告 PSNR 可能需要额外迭代。

这些局限指向两个开放问题：框架能否扩展到其他需要领域特定约束的 CV 任务（如 3D 重建、可微渲染）？在依赖论文完全无可用实现时，组合式引用恢复的极限可达性如何？

### 补充图表

![[assets/figures/papers/paper_list_l2643_https_arxiv_org_abs_2603_00805/figures/005_Table_1.jpg]]
*Table 1: Comparison of NERFIFY with paper and human implementations. We evaluate NeRF papers from the NERFIFY-BENCH set whose code is not publicly available, using SSIM, PSNR, and LPIPS metrics. Note. Other baselines like Paper2Code, AutoP2C, GPT-5 and R1 failed to generate trainable code*

![[assets/figures/papers/paper_list_l2643_https_arxiv_org_abs_2603_00805/figures/006_Table_2.jpg]]
*Table 2: Comparison of NERFIFY with baselines in terms of executable code. We evaluate ability to produce functional, trainable implementations. All baselines fail to generate trainable code despite some producing syntactically valid Python*



## 定位与知识库关联

### 与现有工作的关系

NERFIFY 处于“论文到代码自动生成”与“神经辐射场实现自动化”两个研究方向的交叉点。它并非孤立地改进某一环节，而是针对 NeRF 领域特有的**领域耦合强、调试周期长、架构约束刚性**这三大瓶颈，构建了一套从知识表示到反馈修复的完整自动化流水线。

与通用论文到代码系统的对比清晰地揭示了这一领域特化路线的必要性。**Paper2Code**（Seo et al., arXiv 2025）和 **AutoP2C**（Lin et al., arXiv 2025）代表了当前通用方法的两条主流路线——前者依赖 LLM 的单次代码生成，后者引入多模态理解来增强论文解析能力。然而，这两类方法在 NERFIFY-BENCH 上的**可训练率均为 0%**（Table 2），其根本原因在于它们缺乏对 Nerfstudio 架构合约的显式建模：一个错误的激活函数选择或光线求交实现就足以产生 NaN 梯度，导致训练在数百步内崩溃，而通用系统无法感知这类领域特有的灾难性失败模式。

同样，直接使用强大的通用推理模型——**GPT-5**（单次生成）和 **OpenAI o1**——也无法解决可训练性问题。尽管这些模型可能生成语法正确的 Python 代码，但它们无法保证生成的模块满足 Nerfstudio 的接口合约（如 `RaySamples` 的张量形状约定、`Field` 的梯度流要求），也无法自动解析跨论文的组件依赖（例如，实现 K-Planes 需要从 Mip-NeRF 360 继承提议网络，而这一依赖在目标论文的文字描述中可能仅以引用形式出现）。

NERFIFY 的四个核心设计决策——**CFG 约束代码生成、组合式引用恢复、图思维多智能体协作、视觉驱动反馈**——分别针对上述失败模式进行了系统性补救。消融实验（Table 5）为每个决策的必要性提供了量化证据：移除 In-Context 示例后语义得分从 0.98 骤降至 0.71；移除引用恢复使正确实现率降至 0.65；将 GoT 替换为单次生成后语义得分跌至 0.45；移除冒烟测试则可训练率降至 60%。这些结果表明，NERFIFY 的性能提升并非来自单一技巧，而是四个阶段协同作用的结果。

### 适用边界与局限

NERFIFY 的适用边界由其设计假设清晰界定。第一个边界是**框架依赖性**：当前系统深度绑定 Nerfstudio 架构，其 CFG 形式化、接口合约和组件库均基于 Nerfstudio 的模块化设计。对于非 Nerfstudio 框架的 radiance field 方法（如基于 PyTorch3D 或自定义训练循环的实现），NERFIFY 无法直接迁移。这一局限在论文的 limitations 中被明确承认。

第二个边界是**引用可达性**：组合式引用恢复机制假设目标论文所依赖的组件存在于可访问的引用论文中。当依赖链指向尚未发布代码的论文，或所需组件在引用论文中也未被实现时，系统的递归检索将无法完成。论文将此列为开放问题，其极限可达性尚未被系统验证。

第三个边界是**反馈效率**：视觉驱动反馈依赖烟雾训练（3k 迭代）来评估渲染质量，这仍然需要一定的计算时间。虽然 3k 迭代远少于完整训练（通常需 30k-100k 迭代），但对于需要多轮修复的复杂方法，累积时间仍不可忽略。此外，反馈循环的终止条件之一——“达到论文报告的 PSNR 目标”——在某些情况下可能需要额外迭代才能满足。

### 开放问题

论文识别了三个值得进一步探索的开放问题。第一，**跨任务泛化性**：CFG 约束的多智能体代码生成范式是否能够扩展到其他需要领域特定约束的计算机视觉任务（如 3D 重建、可微渲染、物理模拟），目前尚未验证。这一问题的核心挑战在于，不同领域的架构约束形式差异巨大，CFG 的构建成本和通用性需要权衡。

第二，**引用恢复的极限**：当依赖链中的某个节点完全没有可用实现时，组合式引用恢复的退化行为如何？系统是否能够降级为从论文描述中推断组件实现，还是需要人工介入？这一问题的答案将决定 NERFIFY 在“冷启动”场景下的实用性。

第三，**VLM 反馈的可靠性**：语义诊断分支使用 Qwen3 VLM 来识别渲染伪影（如浮空几何、缺失细节），但这种基于视觉语言模型的诊断是否对所有类型的 NeRF 伪影都有效？是否存在 VLM 误诊导致修复方向错误的风险？论文未对此进行消融分析，这是一个需要人工验证的开放点。



## 原文 PDF

![[paperPDFs/CVPR_2026/NERFIFY_A_Multi_Agent_Framework_for_Turning_NeRF_Papers_into_Code.pdf]]
