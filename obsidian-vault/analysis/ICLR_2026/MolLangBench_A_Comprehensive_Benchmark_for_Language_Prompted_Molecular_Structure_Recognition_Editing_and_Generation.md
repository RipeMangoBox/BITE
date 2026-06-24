---
title: "MolLangBench: A Comprehensive Benchmark for Language-Prompted Molecular Structure Recognition, Editing, and Generation"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/MolLangBench_A_Comprehensive_Benchmark_for_Language_Prompted_Molecular_Structure_Recognition_Editing_and_Generation.pdf
aliases:
- MolLangBench
tags:
- ICLR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/chemistry_and_drug_discovery
core_operator: "改进分子表征与自然语言的对齐，例如通过原子级分词（tokenization）或强化分子‑语言联合预训练，并针对立体化学等专门任务引入结构化推理与符号约束。"
primary_logic: "即使是最先进的模型（GPT‑5）在简单的分子识别任务上表现尚可，但在需要原子级定位（准确率下降6.1%）和生成任务（准确率仅43.0%）时暴露出根本性缺陷，且所有模型在E/Z双键构型识别上均不如随机猜测，说明现有语言模型尚未真正“理解”分子结构，而是依赖表面统计模式。"
claims:
- "GPT‑5在分子结构识别任务的平均定位准确率仅为86.2%，比识别准确率（92.3%）低6.1%，揭示出原子枚举错误这一系统性缺陷。"
- "所有被评测的语言模型在E/Z双键构型识别（bond stereo）上的准确率均低于50%（随机猜测），GPT‑5仅65.5%，表明立体化学推理是普遍瓶颈。"
- "在分子生成任务中，GPT‑5的SMILES有效性仅69.0%，最终匹配准确率仅43.0%，且最主要错误类型为“无效的SMILES语法”，反映了语言模型对分子语法表征的对齐不足。"
- "BPE分词机制将多个相邻原子合并为单个token，导致模型在输出原子索引时频繁遗漏或错位，是定位准确率下降的直接原因。"
---

# MolLangBench: A Comprehensive Benchmark for Language-Prompted Molecular Structure Recognition, Editing, and Generation

> [!tip] 核心洞察
> 即使是最先进的模型（GPT‑5）在简单的分子识别任务上表现尚可，但在需要原子级定位（准确率下降6.1%）和生成任务（准确率仅43.0%）时暴露出根本性缺陷，且所有模型在E/Z双键构型识别上均不如随机猜测，说明现有语言模型尚未真正“理解”分子结构，而是依赖表面统计模式。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | MolLangBench：面向语言提示的分子结构识别、编辑与生成的综合基准 |
| 英文题名 | MolLangBench: A Comprehensive Benchmark for Language-Prompted Molecular Structure Recognition, Editing, and Generation |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=KbXl2jfFRn); [GitHub](https://github.com/TheLuoFengLab/MolLangBench); [Project](https://huggingface.co/datasets/ChemFM/MolLangBench) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/chemistry_and_drug_discovery |
| Method | MolLangBench 多任务基准 |
| Dataset | MolLangBench 分子结构识别, MolLangBench 分子编辑（核心集）, MolLangBench 分子生成（核心集） |

> [!tip] 效果简介
> - MolLangBench 分子结构识别 上，平均准确率（识别 / 定位） 为 0.923 / 0.862 (GPT‑5)，对比 0.877 / 0.792 (o3)，变化 +0.046 / +0.070。
> - MolLangBench 分子编辑（核心集） 上，SMILES有效性 / 编辑准确率 为 0.945 / 0.855 (GPT‑5)，对比 0.945 / 0.785 (o3)，变化 +0.000 / +0.070。
> - MolLangBench 分子生成（核心集） 上，SMILES有效性 / 生成准确率 为 0.690 / 0.430 (GPT‑5)，对比 0.670 / 0.290 (o3)，变化 +0.020 / +0.140。

## 概述

MolLangBench 提出了一个面向语言提示的分子结构识别、编辑与生成的综合基准，旨在系统诊断大型语言模型（LLM）对分子结构的原子级精确理解能力。当前最先进的 LLM 虽在简单的分子属性分类上表现尚可，但一旦任务要求对原子位置进行精细枚举或进行立体化学推理，性能便急剧下降，暴露出现有模型仅依赖表面统计模式、并未真正“理解”分子结构的根本缺陷。核心瓶颈在于 **(1) 原子级定位能力严重不足**，尤其是原子索引枚举错误导致识别与生成任务准确率大幅下滑；**(2) 立体化学推理普遍失效**，所有模型在 E/Z 双键构型识别上的准确率多低于随机猜测，即使最强的模型（GPT‑5）也仅有 65.5%；**(3) 分子表征与自然语言的对齐不足**，实际生成任务中 SMILES 语法有效性和最终匹配准确率分别低至 69.0% 和 43.0%，无效 SMILES 成为第一大错误类型。

方法上，MolLangBench 围绕三类核心的分子-语言界面任务构建：（1）**分子结构识别**——从分子结构（SMILES 或图像）中提取局部拓扑、原子连接、官能团与立体化学等信息；（2）**分子编辑**——根据自然语言指令精确修改分子结构；（3）**分子生成**——根据详细的化学描述从头生成相应分子。识别任务的真值答案通过 RDKit 等化学信息学工具自动提取，确保确定性；编辑与生成任务则采用多轮专家标注、同行评审与独立验证管道，最大限度消除歧义。所有评估均在零样本设定下进行，以反映模型对分子结构的原始领悟能力。

主要实验结果揭示了清晰的性能梯度与系统失败模式：GPT‑5 在识别任务中平均识别准确率达 92.3%，但定位准确率降至 86.2%（降低 6.1%），编辑准确率为 85.5%，而生成准确率仅 43.0%。进一步的消融分析表明，BPE 分词将相邻原子合并为单一 token 是原子枚举错误的直接原因；显式分子结构描述可将下游性质预测准确率提升超过 5%，佐证了结构化理解的价值。此外，SELFIES 替代 SMILES 后各模型性能全面崩溃，视觉语言模型虽能识别分子图像却几乎无法完成编辑与生成任务，凸显了当前跨模态对齐的不足。这些发现共同指向，实现可靠的分子-语言交互必须从根本上改进底层分词策略、引入结构化化学约束，并对立体化学与原子级定位建立专用推理机制。

## 背景与动机

大型语言模型（LLM）在众多科学计算任务中已展现出跨领域能力，然而在分子科学场景中，其对分子结构的理解仍停留在浅层统计层面。**当前模型的根本瓶颈在于缺乏原子级的精确理解**：原子枚举（局部定位）与立体化学推理能力严重不足，导致在需要精确定位原子和从头生成分子的复杂任务上，模型表现远逊于化学家的专业水平。这一缺陷不仅限制了 LLM 在分子设计中的直接应用，更可能使得下游性质预测产生级联错误——已有实验表明，若先让模型显式分析分子结构，性质预测准确率可提升超过 5%（Table S8），说明结构理解的精度直接制约模型在化学任务中的上限。

现有工作多聚焦于粗略的分子性质预测或简单的文本描述生成，缺乏对 **原子级一致性** 和 **立体化学精确性** 的系统评测。实际化学设计流程（如分子优化与从头设计）要求模型不仅能识别官能团，还需准确定位指定原子、给出局部拓扑关系，并能根据自然语言指令精确编辑或生成符合化学规则的分子结构。然而，当前主流模型在这些维度上暴露出的缺口令人担忧：以目前最强的 GPT‑5 为例，其在分子结构识别中平均准确率达 92.3%，但当任务进一步要求原子级定位时，准确率骤降至 86.2%，降幅达 6.1%（Table 1）；在 E/Z 双键构型识别任务上，所有被评测的语言模型准确率均低于 50%，甚至不如随机猜测，表明模型并未真正“理解”立体化学；在分子生成任务中，GPT‑5 生成 SMILES 的有效性仅 69.0%，最终匹配准确率仅 43.0%，且最主要错误类型为“无效的 SMILES 语法”（Table 2, Table 3）。进一步分析揭示，这种原子级错乱的直接原因是 **BPE 分词机制将多个相邻原子合并为同一 token**，导致模型在输出原子索引时频繁遗漏或错位（Figure S6, Appendix A.18）。

上述现象表明，当前语言模型在分子‑语言跨模态对齐方面存在根本性缺口：它们可以记忆和复述常见的分子模式，却难以像化学家一样进行灵活的原子级推理和精确的结构操控。受化学家日常工作中 **分子优化**（在已知骨架上的局部修饰）与 **从头设计**（根据结构描述生成新分子）两大核心场景的启发（Figure 1），本文致力于系统回答一个关键问题：**语言模型在多大程度上能够通过自然语言与分子结构进行精确交互？** 基于此，我们构建了 MolLangBench——首个面向语言提示的分子结构识别、编辑与生成的综合基准，旨在通过高精度、唯一答案的任务设计，量化 LLM 在上述三类接口任务中的原子级理解能力，揭示失败模式，并为未来的分子‑语言对齐研究提供坚实的评测基础。

## 核心创新

MolLangBench 的核心创新并非提出一个新的分子生成模型或语言架构，而是**首次系统定义了面向语言提示的三项原子级分子结构任务**—识别（recognition）、编辑（editing）、生成（generation）—并构建了与之配套的多层次评测基准。通过将分子理解从笼统的性质预测拆解为对局部拓扑、原子索引、立体化学、价键结构的显式查询，该基准揭示了当前最强大语言模型（GPT‑5）在分子表征深层次对齐上的结构性缺陷，从而明确了改进因果链（causal knob）：**原子级分词（tokenization）与分子‑语言联合预训练**，并针对立体化学等专门任务引入结构化推理与符号约束。

### 1. 识别与定位解耦：暴露原子枚举的系统性错误

传统分子问答仅评估模型是否“认识”某个官能团或环系，**MolLangBench首次在识别指标之外引入定位准确率（localization accuracy）**，要求模型显式输出相关的原子索引。这一设计立即放大了语言模型的薄弱环节：**GPT‑5 的平均定位准确率仅为 86.2%，比识别准确率（92.3%）锐降 6.1%**（Table 1 平均行；Section 4.1 分析）。核心原因在于，预训练语言模型采用的 **BPE 分词机制会将相邻的几个原子强行合并成一个 token**（例如 “C1=CC=CC=C1” 中的部分子结构），导致模型在枚举原子时频繁遗漏或错位（Figure S6，Appendix A.18）。这一发现直接指向未来改进的关键路径——**设计原子级感知的分词策略，方能实现可靠的局部拓扑推理**。

### 2. 立体化学专项测试：低于随机猜测的普遍失败

基准特意纳入了对**键立体（E/Z 双键构型）和手性中心的识别任务**。结果呈现出惊人瓶颈：**所有被评语言模型在 E/Z 构型识别上的准确率均低于 50%（随机猜测水平），即使最强的 GPT‑5 也仅达到 65.5%**（Table 1 “Bond stereo” 行；Section 4.1 分析）。这表明现有模型并未真正“理解”立体化学的符号规则，而是依赖数据分布中的表面统计关联。与这一点一致，在编辑任务中，**手性/构象相关编辑的准确率仅 30.4%**（Table S1，o3 分类别结果），进一步验证了立体化学作为独立的失败模式亟需专用结构化推理组件的加入。

### 3. 编辑与生成任务：从语义理解到可靠输出之间的鸿沟

MolLangBench 的另一突出贡献在于构建了**严格专家标注的分子编辑与生成评测集**：每个样本的指令均经两名标注员撰写、同行评审、两名独立验证者确认，确保答案唯一且无歧义（Figure 2，Section 3.2）。在此高标准的测试下，即便是 GPT‑5，**生成任务的 SMILES 有效性也仅 69.0%，最终完全匹配准确率仅 43.0%**；而编辑任务尽管有效性能达 94.5%，但完全匹配准确率也只有 85.5%（Table 2 core 集）。错误分析（Table 3）表明，**“无效 SMILES 语法”是生成任务最主效的失败类别**，直接反映出语言模型与分子语法表征之间存在根本的对齐缺口——模型虽能“看懂”分子描述，却无法可靠地将其翻译为有效的化学图结构。

### 4. 自动脚本与人工协同的精密数据构建

为同时兼顾大规模与高质量，基准采用了创新的双轨标注流水线：
- **识别任务**：通过定制的 RDKit 化学信息学脚本自动从分子结构中抽取 ground‑truth 答案（如原子数、环系大小、官能团列表等），一举保证万级样本的确定性与准确性（Section 3.1）。
- **编辑与生成任务**：由于不存在自动生成唯一文本指令的方法，采用上述多轮人工标注‑验证流程，并严格限定分子大小（非氢原子数＜40），确保每条指令对应唯一正确的分子输出（Section 3.2, Appendix A.6）。

这种混合策略兼顾了可扩展性与标注精度，为后续跨模型零样本评测奠定了坚实基础。

### 5. 跨模态的底线分析与改进方向凝练

基准进一步纳入视觉‑语言模型（如 o4‑mini 进行分子图像识别、GPT Image 1 进行分子图像生成），发现**图像输入并未带来优势**（识别性能与文本模型持平），而**图像生成在编辑任务中准确率仅 13.5%、生成任务为 0%，且经常产生违反价键规则的错误结构**（Table 2，Section 4.2）。这些对比实验将改进方向清晰地收敛至两个核心：
1. **改进底层表征**：通过原子级分词或结构化序列（如 SELFIES）的专项预训练，消除无效语法和原子索引偏差。
2. **引入化学符号约束**：在解码过程中加入价键检查器或拓扑一致性模块，强制输出符合化学规则。

综上，MolLangBench 相对于 baseline 模式的关键创新，不在于提升某一指标的绝对数值，而在于**通过精细的解耦任务设计和严谨的数据构建，首次定量刻画了语言模型在原子级分子理解上的失败分布与因果机制**，为下一代分子‑语言联合模型提供了明确的攻坚靶点。

## 整体框架

![[assets/figures/papers/iclr26_0013_KbXl2jfFRn_MolLangBench_A_Comprehensive_Benchmark_for_Langu/figures/002_Figure_2.jpg]]
*Figure 2: Annotation pipeline for molecule editing and generation tasks. The illustrated example is a simplified case for clarity; real annotations are much more complex*

MolLangBench 将分子‑语言交互抽象为三个核心函数，并围绕它们构建了一条从数据生成到零样本评估的完整管道。三条任务定义如下（详见 Section 2）：

- **分子结构识别**（$f_{\mathrm{recog}}$）：输入分子结构 $\mathcal{M}$（SMILES 或图像）与文本查询 $\mathcal{T}_q$，要求模型输出答案文本 $\mathcal{T}_a$ 以及相关的原子索引。这一形式化将“语义识别”（能否正确给出官能团、环数、原子数等）与“结构定位”（能否精确枚举原子编号）分离评估。
- **语言提示分子编辑**（$f_{\mathrm{edit}}$）：输入起始分子 $\mathcal{M}$ 和自然语言编辑指令 $\mathcal{T}_{\mathrm{edit}}$，输出修改后的分子 $\mathcal{M}_{\mathrm{edit}}$（以 SMILES 字符串形式）。
- **结构描述生成分子**（$f_{\mathrm{gen}}$）：输入详细的文本结构描述 $\mathcal{T}_{\mathrm{desp}}$，从头生成满足描述的有效分子 $\mathcal{M}$（同样以 SMILES 字符串形式）。

数据构造由两条正交的管道支撑（见图 2）。对于识别任务，使用 RDKit 化学信息学工具从 UniChem 数据库随机采样，自动提取官能团、原子邻居、立体化学配置等确定性答案，无需人工介入，从而低成本获得大规模且无歧义的标签。对于编辑与生成任务，自动提取不可行——编辑指令和结构描述的歧义极易导致多解。因此，MolLangBench 引入了严格的专家标注与验证流程：从 UniChem 中筛选非氢原子数少于 40 的候选分子，由化学背景的标注员编写指令或描述，经同行评审与两名独立验证者交叉核验，确保每条实例具有唯一正确答案。该流程产出了核心集（编辑与生成各约 200 例），同时通过简化的单标注-单验证管道扩展了数据集，以扩大覆盖范围。每条编辑实例平均耗时约 30 分钟，生成实例约 60 分钟，体现了高质量标注的代价。

评估模块采用零样本提示，为每类任务定制指令，并要求模型在输出答案时显式提供原子索引或有效 SMILES。识别任务独立报告识别准确率与定位准确率；编辑和生成任务则以模型返回的 SMILES 为目标，先后检验其有效性、分子指纹相似度以及与标准答案的完全匹配准确率。这种分层评估直接暴露了当前大语言模型在分子表征上的两个根本性瓶颈：因 BPE 分词将相邻原子合并为单个 token 而导致的原子枚举错误（定位准确率显著低于识别准确率），以及因缺乏分子语法约束而频繁输出无效 SMILES 的倾向（尤其在生成任务中，即使最强的 GPT‑5 也仅能达到 43.0% 的完全匹配准确率）。通过这一模块化的输入‑输出流与评估策略，MolLangBench 不仅衡量模型表现，更系统性地剖析了分子‑语言对齐中的关键缺陷。

## 核心模块与公式推导

MolLangBench 的方法核心由三个模块构成，分别解决数据生成、质量控制和能力评估的问题。以下结合其与模型瓶颈的因果关联加以归纳。

1. **自动数据生成模块**  
   用于分子结构识别任务。利用 RDKit 化学信息学工具从 UniChem 数据库中采样小分子（非氢原子数 < 40），并自动提取原子连接性、官能团、环拓扑等结构特征，生成确定性的地标答案（ground‑truth）。该模块避免了人工标注在多原子枚举问题上的高昂成本与歧义，保证了局部定位任务的精确训练和测评信号。  
   *瓶颈关联*：由于识别任务要求模型输出精确的原子索引，自动生成的地标答案直接暴露了大语言模型（LLM）在原子级分词上的弱点——BPE 分词将多个相邻原子合并为单一 token，导致模型在枚举局部原子时频繁遗漏或错位。

2. **专家标注与验证管道**  
   针对无法自动生成答案的分子编辑与生成任务，设计了一套严格的人工标注流程（见图2）：首先由主标注者撰写指令与目标分子，经第二位同行评审，再由两名独立校验员进行最终验证。每例编辑任务耗时约 30 分钟，每例生成任务约 60 分钟。该管道仅输出无歧义、答案唯一的样本，确保核心集的高信度。  
   *瓶颈关联*：生成和编辑任务中模型大量产出无效 SMILES（GPT‑5 生成任务中 SMILES 有效性仅 69.0%），说明现有分子‑语言对齐不足以从文本描述中构建合法的化学语法；高质量标注数据是诊断此类失效的基础。

3. **零样本评测模块**  
   对于三个任务均采用任务特定的零提示（zero‑shot prompt），要求模型以文本形式给出答案或 SMILES 表达式。评测指标包括：  
   - **识别任务**：识别准确率（例如官能团类型）与原子级定位准确率；  
   - **编辑任务**：SMILES 有效性、Tanimoto 指纹相似度、编辑完全匹配准确率；  
   - **生成任务**：SMILES 有效性、生成完全匹配准确率，并统计错误类型（见表3）。  
   *瓶颈关联*：该模块评估结果显示，最强模型 GPT‑5 的识别准确率与定位准确率之间存在 6.1% 的系统性落差，且在 E/Z 立体化学识别上多数模型不优于随机猜测——证实立体化学和原子级拓扑推理是 LLM 当前的根本性缺陷。

---

### 任务形式化定义

MolLangBench 将三个分子‑语言交互任务抽象为以下映射函数（节选自 Section 2）：

- **分子结构识别**  
  $$f_{\mathrm{recog}}(\mathcal{M}, \mathcal{T}_{q}) \to \mathcal{T}_{a}$$
  其中 $\mathcal{M}$ 为输入分子（SMILES 或图像），$\mathcal{T}_{q}$ 为待查问题（如“列出所有卤素原子的索引”），$\mathcal{T}_{a}$ 为正确答案。函数要求模型既产生语义正确的结果（识别），又提供精确的原子位置（定位）。

- **语言提示的分子编辑**  
  $$f_{\mathrm{edit}}(\mathcal{M}, \mathcal{T}_{\mathrm{edit}}) \to \mathcal{M}_{\mathrm{edit}}$$
  给定起始分子 $\mathcal{M}$ 和一条自然语言编辑指令 $\mathcal{T}_{\mathrm{edit}}$（如“删除所有氯原子并将碳链延长一个亚甲基”），输出修改后的分子 $\mathcal{M}_{\mathrm{edit}}$。该映射考验模型对化学变换规则的理解和保持原子连通性的能力。

- **从结构描述生成分子**  
  $$f_{\mathrm{gen}}(\mathcal{T}_{\mathrm{desp}}) \to \mathcal{M}$$
  仅给定详细的结构描述 $\mathcal{T}_{\mathrm{desp}}$（包含环系、官能团、立体化学等信息），生成与之匹配的合法分子 $\mathcal{M}$。该任务是目前模型性能最薄弱的环节：GPT‑5 的生成完全匹配准确率仅为 43.0%，主要错误为无效的 SMILES 语法（表3），凸显了分子表征与自然语言之间的深层对齐缺失。

> 注：以上公式均直接取自原文，未作新增推导。具体的提示模板与评测细节见原文附录 A.21 及相关分析。

## 实验与分析

### 主结果：识别尚可，生成暴露根本性缺陷

MolLangBench 的零样本评测揭示了当前大语言模型在分子-语言接口任务上的能力断层。在分子结构识别任务中，最强模型 GPT-5 的平均识别准确率达到 92.3%，但定位准确率降至 86.2%，存在 **6.1 个百分点的系统性差距**（Table 1）。这一差距并非随机波动，而是指向原子枚举（atom enumeration）这一结构性瓶颈——模型能够"看懂"分子类别特征，却无法可靠地映射到具体原子索引。


![[assets/figures/papers/iclr26_0013_KbXl2jfFRn_MolLangBench_A_Comprehensive_Benchmark_for_Langu/figures/006_Table_1.jpg]]
*Table 1: Performance of representative models on molecular structure recognition tasks. For tasks where both recognition and localization accuracy are evaluated, values are reported as recognition accuracy / localization accuracy. For tasks involving only recognition, a single accuracy value is shown. Bold entries indicate the best performance among all evaluated language models (excluding vision-language multimodal models). Complete results are provided in Table S4 in the Appendix*

分子编辑任务表现相对稳健：GPT-5 的 SMILES 有效性为 94.5%，编辑准确率达 85.5%，领先第二名 o3 约 7 个百分点（Table 2）。然而 **分子生成任务暴露了根本性缺陷**：GPT-5 的 SMILES 有效性仅 69.0%，最终匹配准确率仅 43.0%（Table 2）。这意味着即使是最先进的模型，在从头生成分子时也有超过一半的情况无法输出化学上正确的结构。


![[assets/figures/papers/iclr26_0013_KbXl2jfFRn_MolLangBench_A_Comprehensive_Benchmark_for_Langu/figures/007_Table_2.jpg]]
*Table 2: Performance of representative models on molecule editing and generation tasks. Each entry reports SMILES validity / generation or editing accuracy. Results are shown for the core set; for o3, GPT-5, and Gemini-2.5-Pro models, results on the extended set are additionally reported in brackets. Bold values indicate the best performance among all evaluated language models. Tanimoto similarity scores and the complete results for all evaluated models are provided in Appendix Table S5*

### 关键瓶颈：立体化学与原子级定位

**E/Z 双键构型识别是所有模型的普遍盲区**。Table 1 显示，所有被测语言模型在该子任务上的准确率均低于 50%——即**不如随机猜测**。GPT-5 虽以 65.5% 相对领先，但这一数字仍表明立体化学推理尚未被现有模型真正习得。结合 o3 在编辑任务中"手性与构象"类别仅 30.4% 的准确率（Table S1），可以确认：**立体化学是跨越识别、编辑、生成三类任务的深层瓶颈**，而非特定任务的数据噪声。

原子级定位错误的因果机制已被追溯到 **BPE 分词机制**：多个相邻原子被合并为单个 token，导致模型在输出原子索引时频繁遗漏或错位（Figure S6, Appendix A.18）。这是定位准确率 6.1% 差距的直接技术原因，也是"识别-定位"能力解耦的本质——表面统计模式足以支撑类别判断，但不足以支撑精确的空间枚举。

### 消融实验：表征格式与多模态的意外结论

**SMILES vs. SELFIES 的对比具有反直觉的警示意义**。将输入格式从 SMILES 替换为 SELFIES 后，所有模型性能**大幅下降**：o3 的识别平均准确率跌至 0.528，编辑准确率低于 0.20，生成任务**全部失败**（Section A.16）。这一结果说明，尽管 SELFIES 在理论上保证语法有效性，但现有 LLM 的预训练语料和表征对齐严重偏向 SMILES，**格式切换的代价远超预期**。

**显式结构识别对下游性质预测具有正向迁移**。在 BBBP、BACE 等性质预测任务中，先让模型分析分子结构再预测，比直接预测准确率提高超过 5%（Section 4.1, Table S8）。这验证了 MolLangBench 识别任务的设计价值：原子级理解不仅是目标，也是提升下游任务可靠性的手段。

**视觉-语言模型的表现呈现任务分化**。o4-mini 在图像输入下的识别性能可与文本模型比肩，但图像生成模型 GPT Image 1 在编辑和生成任务上准确率极低（编辑 13.5%，生成 0%），且常产生违反价键规则的化学结构错误（Section 4.2, Appendix A.20）。这表明**视觉模态的引入并未自动解决分子表征的深层对齐问题**，反而在生成端引入了额外的视觉-化学转换噪声。

### 失败模式：无效 SMILES 与级联错误

Table 3 的错误类型统计揭示了生成任务的核心失败模式：**"无效的 SMILES 语法"是最主要错误类型**。这并非简单的后处理可修复问题，而是反映了语言模型对分子语法表征的深层对齐不足——模型在"说化学语言"时，其 token 级预测与化学合法性约束之间存在结构性错位。


![[assets/figures/papers/iclr26_0013_KbXl2jfFRn_MolLangBench_A_Comprehensive_Benchmark_for_Langu/figures/008_Table_3.jpg]]
*Table 3: Counts of error types observed in the molecule editing and generation tasks. A single failed sample may exhibit multiple error types*

编辑任务中，功能团替换准确率最高（o3: 91.5%），而手性/构象编辑最低（30.4%）（Table S1）。这一梯度说明：**局部、离散的化学操作易于学习，而涉及三维空间构型或全局拓扑约束的操作则超出当前模型的推理边界**。

### 证据强度与待验证点

上述结论中，GPT-5 的识别/定位差距（6.1%）、生成准确率 43.0%、E/Z 识别低于随机、以及 SMILES/SELFIES 性能反转，均有 Table 1-2 及附录多表交叉支撑，置信度较高。但以下两点需额外注意：

- GPT-5 在 20 项识别任务中 19 项领先的具体排名统计，原文仅提及而未展示完整对比，该细节置信度为 0.8，建议手动核对 Table S4。
- 视觉模型 o4-mini 与文本模型"比肩"的定量对比，原文未给出精确数值对齐，该判断需结合 Table 1 中 o4-mini 行与文本模型行的直接比较进行人工确认。

### 公平性说明

当前结论限于非氢原子数少于 40 的小分子（Section 3.2），向大分子或生物大分子的迁移性未评估。编辑与生成任务的数据量受限于专家标注成本（核心集每生成实例约 60 分钟、编辑实例约 30 分钟，Appendix A.6），稀有结构或反应类型的覆盖可能不全。所有模型均为零样本评估，未进行化学领域微调，可能低估专项训练后的潜力。

### 补充图表

![[assets/figures/papers/iclr26_0013_KbXl2jfFRn_MolLangBench_A_Comprehensive_Benchmark_for_Langu/figures/035_Figure_14.jpg]]
*Figure 14: Figure S6: Illustration of enumeration errors in LLMs. Atoms grouped by the same color are merged into a single token*

![[assets/figures/papers/iclr26_0013_KbXl2jfFRn_MolLangBench_A_Comprehensive_Benchmark_for_Langu/figures/009_Table_4.jpg]]
*Table 4: Table S1: Summary of molecule edit categories with sample counts (brackets indicate extended set) and o3 model accuracy per category for core set. Editing instructions may belong to multiple categories*


## 方法谱系与知识库定位

### 与基线体系及评估范式的关系

MolLangBench 在分子‑语言界面的基准体系中填补了对**原子级精确识别与定位**的评估缺口。不同于仅依赖自动匹配指标（如Tanimoto相似度）或选择题式的既往工作，该基准通过**确定性基准答案**（deterministic ground‑truth）强制要求模型输出精确的原子索引或有效SMILES，从而引入了“结构定位准确率”（structural localization accuracy）这一全新维度。基准构建融合了两种互补的数据生成范式：

- **识别任务**：通过定制化RDKit脚本自动提取多类结构信息（局部拓扑、官能团、立体化学等），实现零人工成本的大规模标注。
- **编辑与生成任务**：采用多轮专家标注、同行评审与独立验证的双层流水线（核心集两轮标注+两名独立验证员，扩展集为简化的一审+一验）确保引导无歧义且答案唯一。

由此产生的任务集覆盖了10大编辑类别（Table S1）和17种识别子任务（Table S2），且化学空间分布（ECFP4 Fingerprints经t‑SNE验证）与UniChem文库一致（Figure S2），保证了采样代表性。

在评估设置上，论文以**零样本提示**（zero‑shot prompting）方式将通用语言模型（GPT‑4o）、推理增强模型（o1、DeepSeek‑R1、o3、GPT‑5）以及多模态模型（o4‑mini、GPT Image 1）作为基线系统。核心发现（Table 1, Table 2）表明：

- 当前最强大的语言模型（GPT‑5）在**识别**任务上的平均定位准确率（86.2%）较识别准确率（92.3%）系统性低**6.1%**，且这一差异与子任务复杂度无关，指向**原子枚举错误**这一固有瓶颈。
- 所有模型在**E/Z双键构型识别**上的准确率均低于随机猜测水平（<50%），意味着立体化学推理能力普遍缺失。
- 在**编辑**任务上，GPT‑5的准确率（85.5%）明显领先于o3（78.5%），然而在更需从头构建的**生成**任务上，即便强如GPT‑5，SMILES有效性仅69.0%，最终匹配准确率更剧烈跌至43.0%。

这些结果将当前语言模型在分子‑语言操作中的能力边界清晰地标定为“语法级有效但语义级不可靠”，并将BPE分词导致的原子索引错位、立体化学盲区确立为两大因果机制。

### 适用边界与限制

1. **分子尺度与类型局限**：数据集严格限制为**非氢原子数＜40**的小分子，所有结论向大环、肽、核苷酸或高分子体系的迁移**未经任何验证**。
2. **标注成本导致的覆盖不足**：编辑与生成任务的单个样本需要30–60分钟专家时间，即使通过扩展集补充（总计约400例），**稀有反应类别、复杂桥环及多手性中心结构仍可能采样不足**。
3. **零样本评估的单象性**：所有模型均在未进行任何化学领域微调的条件下测试，性能数值仅反映**预训练分布的表层映射**，无法评价模型经过分子表示专项训练后的潜力。
4. **线性语法依赖性**：将输入格式由SMILES换为SELFIES后，所有模型的识别平均准确率骤降至0.528，编辑与生成几乎完全失效（生成任务零成功），可见当前语言模型对SMILES语法有**强过拟合倾向**，对新分子表征的泛化能力极弱。
5. **视觉‑语言鸿沟**：视觉‑语言模型（o4‑mini）在图像输入下的识别性能几乎与纯文本模型持平，未从“看图”获得显著增益；而图像生成模型（GPT Image 1）产出的分子图频繁违反价键规则，编辑准确率仅13.5%，生成准确率0%，表明**多模态生模块尚未具备化学合理性约束**。

### 开放问题与后续研究路径

基于故障模式与机制分析，MolLangBench 锚定了以下关键开放问题：

- **分词机制的重设计**：BPE将相邻原子合并为单一token直接导致原子索引错位（Appendix A.18, Figure S6），需探索**化学感知的分词器**（如原子级tokenization）或融入分子位置编码，实现可靠的原子枚举。
- **结构化符号约束的嵌入**：生成任务中首错误类型为“无效SMILES语法”（Table 3），提示仅依靠语言模型内部知识无法保障化学合法性，未来应结合**外部价键检查器、文法导向的解码约束**从根本上杜绝无效输出。
- **立体化学专有能力的构建**：E/Z异构识别全面低于随机水平的“反直觉”结果表明模型完全未习得几何异构的概念，需设计**专门的立体化学推理头**或通过大规模对比数据注入立体感知知识。
- **跨模态对齐的强化**：图像输入未能提升分子结构的理解精度，说明模型仅利用表面视觉模式而非拓扑推理，后续应研究**分子图神经网络与视觉‑语言模型的对齐训练**。
- **规模泛化与自动化扩展**：手工标注的高成本迫使基准扩展依赖自动化策略，今后可借助**程序化合成从结构化数据库生成约束性描述**，推动基准覆盖大分子空间，并测试预训练‑微调范式在化学领域的性能跃迁。

综上，MolLangBench 不但构建了跨任务、多粒度的分子‑语言评测体系，更通过分词、立体化学盲区与跨模态断裂带三大核心瓶颈的系统性诊断，为标准语言模型向化学精密推理演进提供了机理层面的改进路线图。

## 原文 PDF

![[paperPDFs/ICLR_2026/MolLangBench_A_Comprehensive_Benchmark_for_Language_Prompted_Molecular_Structure_Recognition_Editing_and_Generation.pdf]]
