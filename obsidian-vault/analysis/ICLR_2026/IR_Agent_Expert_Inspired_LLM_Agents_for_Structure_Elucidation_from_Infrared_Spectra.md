---
title: "IR-Agent: Expert-Inspired LLM Agents for Structure Elucidation from Infrared Spectra"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/IR_Agent_Expert_Inspired_LLM_Agents_for_Structure_Elucidation_from_Infrared_Spectra.pdf
aliases:
- IA
- IR-Agent
tags:
- ICLR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/chemistry_and_drug_discovery
core_operator: "IR-Agent decomposes infrared structure elucidation into translator, table-interpretation, retrieval, and final structure-elucidation agents."
primary_logic: "It generates SMILES candidates, extracts local substructure cues from absorption tables, retrieves globally similar spectra, and lets an SE expert rerank candidates."
claims:
- "TI Expert supplies explicit peak-to-substructure evidence from IR absorption ranges."
- "Ret Expert adds global structural context by cosine-similarity retrieval over spectra."
- "The note reports higher Top-K accuracy than Transformer and single-agent baselines without retraining for extra chemical information."
---

# IR-Agent: Expert-Inspired LLM Agents for Structure Elucidation from Infrared Spectra

> [!tip] 核心洞察
> 通过将红外光谱分析分解为局部子结构识别（基于吸收表）和全局结构上下文（基于谱图检索）两个互补任务，并让LLM智能体分别处理后再进行综合推理，可以显著提升分子结构解析的准确性，且无需重新训练即可整合新信息。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | IR-Agent：受专家启发的红外光谱结构解析 LLM 智能体 |
| 英文题名 | IR-Agent: Expert-Inspired LLM Agents for Structure Elucidation from Infrared Spectra |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=6bthH14pD8); [GitHub](https://github.com/HeewoongNoh/IR-Agent) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/chemistry_and_drug_discovery |
| Method | IR-Agent |
| Dataset | NIST IR spectra dataset (9, 052 spectra, 80/10/10 split), NIST IR spectra dataset |

> [!tip] 效果简介
> - NIST IR spectra dataset (9,052 spectra, 80/10/10 split) 上，Top-1 Accuracy 为 0.103，对比 0.098 (Transformer)，变化 +0.005。
> - NIST IR spectra dataset 上，Top-3 Accuracy 为 0.178，对比 0.169 (Transformer)，变化 +0.009。
> - NIST IR spectra dataset 上，Top-5 Accuracy 为 0.199，对比 0.176 (Transformer)，变化 +0.023。

## 概述

本文提出**IR-Agent**，一种基于大语言模型（LLM）的多智能体框架，专门用于从红外（IR）光谱中解析分子结构。该框架通过模拟化学专家的分析流程，将红外光谱解析分解为三个专门智能体的协作任务：**Table Interpretation (TI) Expert**（基于吸收表进行局部子结构识别）、**Retriever (Ret) Expert**（通过谱图检索获取全局结构上下文）和**Structure Elucidation (SE) Expert**（综合推理输出最终预测）。IR-Agent的核心优势在于其灵活的知识整合能力——通过更新提示词即可引入新的化学信息（如原子类型、骨架、碳原子数），无需重新训练模型。在NIST红外光谱数据集（9,052个光谱）上的实验表明，IR-Agent在Top-K准确率上持续优于Transformer基线和单智能体变体，且对提示词变体具有鲁棒性。

## 背景与动机

红外光谱是化学分析中广泛使用的技术，因其成本低、易获取而被常用于初始分析阶段（Coates et al., 2000; Mistek & Lednev, 2018）。然而，红外光谱仅提供局部振动信息，不足以唯一确定完整分子结构（Coates et al., 2000; Griffiths, 2006）。传统机器学习方法（如Transformer直接预测SMILES）依赖固定输入格式，引入新信息（如原子类型、骨架）需重新设计和训练模型，且无法模拟专家分析流程。

现有方法的根本瓶颈在于：**难以灵活整合多种化学知识，且无法模拟专家分析流程**。红外光谱仅提供局部振动信息，不足以唯一确定完整分子结构，而传统ML方法依赖固定输入格式，引入新信息需重新设计模型。

本文的核心因果旋钮是：**采用多智能体框架，将专家分析流程分解为三个专门智能体（Table Interpretation Expert、Retriever Expert、Structure Elucidation Expert），每个智能体负责特定分析任务，并通过提示词灵活整合额外化学信息**。

核心洞察在于：**通过将红外光谱分析分解为局部子结构识别（基于吸收表）和全局结构上下文（基于谱图检索）两个互补任务，并让LLM智能体分别处理后再进行综合推理，可以显著提升分子结构解析的准确性，且无需重新训练即可整合新信息**。

## 核心创新

IR-Agent的核心创新体现在以下五个关键设计变更：

| 变更槽位 | 基线值 | 提出值 | 证据锚点 |
|---------|--------|--------|---------|
| 分析流程架构 | 单模型端到端预测（如Transformer直接输出SMILES） | 多智能体框架，包含TI Expert、Ret Expert、SE Expert，模拟专家分析流程 | "we propose IR-Agent, a novel LLM-based multi-agent framework specifically designed to emulate expert analytical processes" |
| 知识整合方式 | 固定输入格式，引入新信息需重新设计和训练模型 | 通过提示词灵活整合额外化学信息（原子类型、骨架、碳原子数），无需重新训练 | "when new knowledge becomes available, the system does not need a complete redesign or retraining. Instead, it can be easily extended by incorporating the additional information through updated prompts" |
| 局部结构信息提取 | 依赖模型隐式学习，或仅使用CNN/GNN进行官能团分类 | TI Expert使用IR Peak Table Assigner工具，基于吸收表显式分配子结构，并与SMILES候选交叉验证 | "the TI Expert agent employs the IR Peak Table Assigner tool, which extracts peaks from the spectrum by simply comparing the absorbance of neighboring wavenumbers and then assigns corresponding substructures to each peak based on its wavenumber range" |
| 全局结构上下文获取 | 无显式检索机制，仅依赖模型内部知识 | Ret Expert使用IR Spectra Retriever工具，基于余弦相似度检索最相似谱图及其SMILES，提取共有结构特征 | "the Ret Expert agent utilizes the IR Spectra Retriever tool to identify spectra that are similar to the target IR spectrum... computes the cosine similarity between the target spectrum and all spectra in the database" |
| 工具选择策略 | 动态工具选择（如ReAct框架），可能导致工具选择偏差或重复 | 确定性固定流程：先由Translator生成候选，再并行由TI Expert和Ret Expert分析，最后由SE Expert综合推理 | "a deterministic approach to tool selection—as implemented in IR-Agent—is necessary" |

## 整体框架

![[assets/figures/papers/iclr26_0002_6bthH14pD8_IR-Agent_Expert-Inspired_LLM_Agents_for_Structur/figures/001_Figure_1.jpg]]
*Figure 1: Overview of IR-Agent. (a) Overall framework. Given an unknown IR spectrum, IR-Agent first utilizes the IR Spectra Translator to generate candidate structures in SMILES format. The Table Interpretation (TI) Expert then extracts local structural information by referencing the IR absorption table through the IR Peak Table Assigner. In parallel, the Retriever (Ret) Expert obtains global structural features from similar spectra retrieved by the IR Spectra Retriever from a database. The Structure Elucidation (SE) Expert integrates analyses from both experts to produce the final predicted molecular structures. (b) Detailed view of the Table Interpretation (TI) Expert. (c) Detailed view o...*

IR-Agent的整体框架如Figure 1所示，包含四个主要模块：

**Figure 1: Overview of IR-Agent.** (a) Overall framework. Given an unknown IR spectrum, IR-Agent first utilizes the IR Spectra Translator to generate candidate structures in SMILES format. The Table Interpretation (TI) Expert then extracts local structural information by referencing the IR absorption table through the IR Peak Table Assigner. In parallel, the Retriever (Ret) Expert obtains global structural features from similar spectra retrieved by the IR Spectra Retriever from a database. The Structure Elucidation (SE) Expert integrates analyses from both experts to produce the final predicted molecular structures. (b) Detailed view of the Table Interpretation (TI) Expert. (c) Detailed view of the Retriever (Ret) Expert.

框架流程如下：
1. **IR Spectra Translator**：基于Transformer的模型，从目标IR光谱生成初始SMILES候选集C（使用束搜索解码，束宽=3）。
2. **Table Interpretation (TI) Expert**：使用IR Peak Table Assigner工具提取谱峰并基于吸收表分配子结构，与SMILES候选交叉验证，输出子结构及其置信度和理由。
3. **Retriever (Ret) Expert**：使用IR Spectra Retriever工具（余弦相似度）检索Top-N最相似谱图及其SMILES，识别共有结构特征，按相似度加权。
4. **Structure Elucidation (SE) Expert**：综合TI Expert和Ret Expert的输出，对SMILES候选集进行精炼和排序，输出Top-K预测分子结构。

## 核心模块与公式推导

### 5.1 IR Spectra Translator

Transformer模型从输入红外光谱X生成K个SMILES候选的集合，使用束搜索解码：

$$\mathcal{C} = \{ \mathbf{s}_1, \ldots, \mathbf{s}_{\mathbf{K}} \} = \mathrm{Transformer}(\mathcal{X}) \quad \text{(Equation 1)}$$

红外光谱预处理：将透射率T转换为吸光度A：

$$A = -\log_{10}(T) \quad \text{(Equation 6)}$$

零值透射率条目替换为$10^{-10}$以避免数学错误。光谱表示为1D序列$\mathcal{X} \in \mathbb{R}^{1 \times L}$，通过可学习线性变换得到$\bar{\mathbf{x}} \in \mathbb{R}^{L \times d}$，然后添加可学习位置嵌入：

$$\mathbf{z}_i = \mathbf{x}_i + \mathbf{P}_i, \quad \mathrm{for} i = 1, \ldots, L \quad \text{(Equation 7)}$$

模型使用交叉熵损失训练：

$$\mathcal{L}_{\mathrm{CE}} = -\frac{1}{N} \sum_{n=1}^{N} \sum_{t=1}^{T_n} \log p_\theta(y_t^{(n)} \mid y_{<t}^{(n)}, \mathcal{X}^{(n)}) \quad \text{(Equation 8)}$$

### 5.2 Table Interpretation (TI) Expert

TI Expert接收提示、IR Peak Table Assigner输出和SMILES候选，产生子结构分配结果：

$$\mathcal{A}_{\mathrm{TIExpert}} = \mathrm{TIExpert}(\mathbf{P}_{\mathrm{TIExpert}}, \mathrm{IRPeakTableAssigner}(\mathcal{X}, \mathbf{T}), \mathcal{C}) \quad \text{(Equation 2)}$$

IR Peak Table Assigner使用SciPy的find_peaks函数（height=1, distance=50）提取谱峰，然后基于Table 4中的波数范围-子结构映射表分配子结构。

**Table 4: Wavenumber Range and Substructure Assignments**（IR吸收表，用于IR Peak Table Assigner）

### 5.3 Retriever (Ret) Expert

IR Spectra Retriever返回Top-N个最相似谱图的SMILES及其与目标谱的余弦相似度：

$$\{ \mathrm{candi}_1 : \mathrm{sim}_1, \ldots, \mathrm{candi}_N : \mathrm{sim}_N \} = \mathrm{IRSpectraRetriever}(\mathcal{X}) \quad \text{(Equation 3)}$$

Ret Expert接收提示和检索输出，产生共享结构特征：

$$\mathcal{A}_{\mathrm{RetExpert}} = \mathrm{RetExpert}(\mathbf{P}_{\mathrm{RetExpert}}, \mathrm{IRSpectraRetriever}(\mathcal{X})) \quad \text{(Equation 4)}$$

### 5.4 Structure Elucidation (SE) Expert

SE Expert综合TI和Ret专家的输出以及候选集，产生Top-K排序的分子结构列表：

$$\mathcal{A}_{\mathrm{SEExpert}} = \mathrm{SEExpert}(\mathbf{P}_{\mathrm{SEExpert}}, \mathcal{A}_{\mathrm{TIExpert}}, \mathcal{A}_{\mathrm{RetExpert}}, \mathcal{C}) \quad \text{(Equation 5)}$$

## 实验与分析

### 6.1 数据集与设置

- **数据集**：NIST红外光谱数据集，包含9,052个实验红外光谱，涵盖气相（56%）、液相（20%）、固相（24%），重原子数范围3-68（均值13.4，中位数12.0）。
- **数据划分**：80/10/10训练/验证/测试。
- **评估指标**：Top-K精确匹配准确率（转换为InChI后比较），报告三次独立实验的平均值和标准差。
- **基线方法**：Standalone Transformer、Single-agent variant、Direct o3-mini generation、Patch-Based Self-Attention Transformer (Wu et al., 2025)、LLaMA-3.1-8B、ReAct framework。

### 6.2 主要结果

**Table 1: Overall model performance for structure elucidation from IR spectra.**


![[assets/figures/papers/iclr26_0002_6bthH14pD8_IR-Agent_Expert-Inspired_LLM_Agents_for_Structur/figures/002_Table_1.jpg]]
*Table 1: Overall model performance for structure elucidation from IR spectra.*

| 方法 | Top-1 | Top-3 | Top-5 | Top-10 |
|------|-------|-------|-------|--------|
| Transformer | 0.098 | 0.169 | 0.176 | 0.176 |
| Single-agent (o3-mini) | 0.073 | 0.131 | 0.149 | 0.166 |
| IR-Agent (multi, o3-mini) | **0.103** | **0.178** | **0.199** | **0.216** |

关键发现：
- **多智能体IR-Agent在Top-K准确率上持续优于单智能体变体**（证据锚点："The multi-agent framework consistently outperforms the single-agent approach."）
- **IR-Agent (GPT-4o)达到与单智能体o3-mini相当或更优的准确率**（证据锚点："the multi-agent version of IR-Agent (GPT-4o) achieves comparable or even superior accuracy compared to the single-agent system built on o3-mini"）

### 6.3 化学信息整合

**Table 2: Overall model performance with various chemical information.**


![[assets/figures/papers/iclr26_0002_6bthH14pD8_IR-Agent_Expert-Inspired_LLM_Agents_for_Structur/figures/003_Table_2.jpg]]
*Table 2: Overall model performance with various chemical information.*

| 化学信息 | Top-1 | Top-3 | Top-5 | Top-10 |
|---------|-------|-------|-------|--------|
| No Knowledge | 0.103 | 0.178 | 0.199 | 0.216 |
| Atom Types | **0.127** | **0.213** | **0.250** | **0.278** |
| Scaffold | 0.118 | 0.208 | 0.232 | 0.258 |
| Carbon Count | 0.123 | 0.190 | 0.215 | 0.252 |

化学信息（原子类型、骨架、碳原子数）通过追加一句话到对应专家提示词中整合，无需重新训练。

### 6.4 消融研究

**Table 3: Ablation study of IR-Agent (o3-mini).**


![[assets/figures/papers/iclr26_0002_6bthH14pD8_IR-Agent_Expert-Inspired_LLM_Agents_for_Structur/figures/004_Table_3.jpg]]
*Table 3: Ablation study of IR-Agent (o3- mini).*

| 配置 | Top-1 | Top-3 | Top-5 | Top-10 |
|------|-------|-------|-------|--------|
| No Expert | 0.073 | 0.131 | 0.149 | 0.166 |
| TI Expert only | 0.089 | 0.154 | 0.175 | 0.193 |
| Ret Expert only | 0.098 | 0.169 | 0.186 | 0.202 |
| IR-Agent (TI+Ret) | **0.103** | **0.178** | **0.199** | **0.216** |

关键发现：
- **同时使用TI Expert和Ret Expert优于单独使用任一专家**（证据锚点："using only one expert (i.e., either the TI Expert only or Ret Expert only) underperforms compared to the case where both experts are employed."）
- 候选SMILES数量C在3或5时性能最佳，超过后下降（Figure 2a）。
- 使用预训练IR光谱翻译器（Alberts et al., 2024a）可进一步提升性能（Figure 2b）。

**Figure 2: In-depth Analysis results.** (a) Sensitivity to number of SMILES candidates C; (b) Performance using pretrained IR Spectra Translator.

### 6.5 额外对比与鲁棒性

**Table 6: Comparison with Additional Baselines**

| 方法 | Top-3 | MACCS Tanimoto |
|------|-------|----------------|
| Patch-Based Self-Attention Transformer | 0.160 | 0.721 |
| IR-Agent (o3-mini) | **0.178** | **0.770** |

- IR-Agent在Top-3准确率（0.178 vs 0.160）和MACCS Tanimoto相似度（0.770 vs 0.721）上均优于Patch-Based Self-Attention Transformer。
- LLaMA-3.1-8B在零样本和微调设置下均无法生成有效SMILES。

**Table 7: Robustness of IR-Agent (o3-mini) to prompt variations.**

| 提示变体 | Top-1 | Top-3 | Top-5 | Top-10 |
|---------|-------|-------|-------|--------|
| Prompt 1 | 0.110 | 0.168 | 0.194 | 0.214 |
| Prompt 2 | 0.100 | 0.182 | 0.201 | 0.222 |
| IR-Agent (original) | 0.103 | 0.178 | 0.199 | 0.216 |

IR-Agent对提示词变体具有鲁棒性，性能波动小。

**Table 9: Comparison of IR-Agent (GPT-4o) with ReAcT framework**

| 方法 | Top-1 | Top-3 | Top-5 | Top-10 |
|------|-------|-------|-------|--------|
| ReAcT Framework | 0.083 | 0.148 | 0.151 | 0.158 |
| IR-Agent (GPT-4o) | **0.093** | **0.153** | **0.177** | **0.204** |

IR-Agent (GPT-4o)优于ReAct框架。

### 6.6 局限性

- IR-Agent仅基于峰位置进行吸收表解释，未考虑峰形和峰强度，而这些对准确解释也很重要。
- 框架性能受IR Spectra Translator生成的候选SMILES质量影响。
- 当适应新光谱数据集时，IR Spectra Translator仍需重新训练。
- **IR-Agent在混合物（242个测试样本）上完全失效（Top-1=0.000）**（Table 10），因峰重叠和训练样本有限。
- 框架采用确定性固定流程，缺乏动态决策能力。

**Table 10: Performance of IR-Agent on Single Compounds and Mixtures**

| 类型 | #Test | Top-1 | Top-3 | Top-5 | Top-10 |
|------|-------|-------|-------|-------|--------|
| Single | 886 | 0.105 | 0.183 | 0.204 | 0.221 |
| Mixture | 20 | **0.000** | **0.000** | **0.000** | **0.000** |

### 6.7 案例研究

**Figure 3: Outputs of expert agents in IR-Agent during the structure elucidation process.** 案例显示：TI Expert推断C-F基团（高置信度）和Br（低置信度）；Ret Expert识别出含CF3基团的苯环。

**Figure 4: Example of structured analytical reasoning by the Table Interpretation (TI) expert.** 案例显示：TI Expert交叉验证六个候选子结构，仅保留异硫氰酸酯基团（2140-1990 cm-1），与真实结构一致。

### 补充图表

![[assets/figures/papers/iclr26_0002_6bthH14pD8_IR-Agent_Expert-Inspired_LLM_Agents_for_Structur/figures/008_Table_4.jpg]]
*Table 4: Wavenumber Range and Substructure Assignments*

![[assets/figures/papers/iclr26_0002_6bthH14pD8_IR-Agent_Expert-Inspired_LLM_Agents_for_Structur/figures/009_Table_4.jpg]]
*Table 4: Wavenumber Range and Substructure Assignments*


## 方法谱系与知识库定位

IR-Agent属于**基于LLM的化学结构解析**方法谱系，其核心创新在于将多智能体框架引入红外光谱分析领域。与现有方法相比：

- **与传统ML方法（Transformer、Patch-Based Self-Attention）**：IR-Agent通过显式知识整合（吸收表、谱图检索）和专家分析流程模拟，在Top-K准确率和分子相似度上均取得提升，且无需重新训练即可整合新信息。
- **与单智能体LLM方法**：多智能体框架通过任务分解避免了单智能体同时处理多任务时的推理退化，在相同LLM骨干下持续优于单智能体变体。
- **与ReAct等动态工具选择框架**：IR-Agent采用确定性固定流程，避免了动态工具选择中的常见失败模式（如仅选择单一工具或重复选择同一工具），在结构解析任务上表现更优。

IR-Agent在知识库中的定位是：**首个将多智能体LLM框架系统性地应用于红外光谱结构解析的工作**，展示了通过模拟专家分析流程和灵活知识整合来提升化学结构预测准确性的可行路径。未来工作方向包括：整合峰形和峰强度信息、直接以图像形式输入IR光谱到LLM、扩展到混合物分析、引入动态工具选择机制、以及扩展到多模态光谱分析（如同时整合IR、MS和NMR）。

## 原文 PDF

![[paperPDFs/ICLR_2026/IR_Agent_Expert_Inspired_LLM_Agents_for_Structure_Elucidation_from_Infrared_Spectra.pdf]]
