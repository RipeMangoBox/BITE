---
title: "PARC: A Quantitative Framework Uncovering the Symmetries within Vision Language Models"
type: paper
paper_level: A
venue: CVPR
year: 2025
pdf_ref: paperPDFs/CVPR_2025/PARC_A_Quantitative_Framework_Uncovering_the_Symmetries_within_Vision_Language_Models.pdf
project_link: null
code_link: https://github.com/NVlabs/PARC
aliases:
- PPARC
- PARC
tags:
- CVPR_2025
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/vision_models_multimodal
core_operator: "prompt的语义修改（否定、反义词、图像交换等）直接改变了正确答案，是导致模型准确性和一致性剧烈下降的关键扰动因素。"
primary_logic: "通过校准可靠性与一致性评分，PARC揭示语义变化在语言和视觉模态中均同等破坏VLM性能；模型家族和训练数据质量比模型规模更能预测prompt鲁棒性。"
claims:
- "VLMs对语义变化极为敏感，LS-A（反义词）和VS-E（图像交换）使一致性降至接近随机。"
- "InternVL2家族是最鲁棒的模型族，InternVL2-40B的可靠性显著高于其他模型，而Qwen-VL和CogVLM GG表现最差。"
- "校准步骤纠正了因随机基线不同而导致的错误排序，使原始提示优于否定提示的预期趋势在所有数据集上一致。"
- "MMBench 上 Calibrated Reliability = -0.01 (LS-A)"
---

# PARC: A Quantitative Framework Uncovering the Symmetries within Vision Language Models

> [!tip] 核心洞察
> 通过校准可靠性与一致性评分，PARC揭示语义变化在语言和视觉模态中均同等破坏VLM性能；模型家族和训练数据质量比模型规模更能预测prompt鲁棒性。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | PARC：揭示视觉语言模型对称性的定量框架 |
| 英文题名 | PARC: A Quantitative Framework Uncovering the Symmetries within Vision Language Models |
| 会议/期刊 | CVPR 2025 |
| Links | [paper](https://arxiv.org/abs/2506.14808) · [GitHub](https://github.com/NVlabs/PARC) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/vision_models_multimodal |
| Method | PARC (Prompt Analysis via Reliability and Calibration) |
| Dataset | MMBench, MIT-States, Average across 7 datasets |

> [!tip] 效果简介
> - MMBench 上，Calibrated Reliability 为 -0.01 (LS-A)，对比 0.48 (Original)，变化 -0.49。
> - MIT-States 上，Calibrated Reliability 为 0.15 (LS-M)，对比 0.52 (Original)，变化 -0.37。
> - Average across 7 datasets 上，Calibrated Reliability (model average vs. best) 为 0.65 (InternVL2-40B)，对比 0.29 (all models avg.)，变化 +0.36。

## 概要

视觉语言模型（VLM）对用户输入的 prompt 变化高度敏感，尤其是那些改变预期答案的语义变化（如否定、反义词、图像交换）会剧烈削弱模型的准确性与一致性。然而，现有评估指标缺乏跨数据集和 prompt 变体的可比性，难以公平地衡量模型的 prompt 鲁棒性。

PARC（Prompt Analysis via Reliability and Calibration）针对这一瓶颈，提出了一个系统的 prompt 敏感性分析框架。其核心思路包含三个组件：首先，设计涵盖语言和视觉模态的 11 种现实 prompt 变体（包括重述和语义变化两类）；其次，引入一个新的**可靠性评分**（reliability score），将准确度与基于共形预测的确定性综合为单一指标，并附带显式的准确度下界保证；最后，通过基于期望随机性能的**校准步骤**，使所有评分在跨数据集和跨 prompt 变体之间可直接比较。

核心实验发现如下：

- **语义变化在语言和视觉模态中均同等破坏 VLM 性能**。在平均校准一致性上，语言反义词变体（LS-A）仅为 0.09，视觉图像交换变体（VS-E）降至 0.00（随机水平为 0），表明模型对这些变化的响应接近随机猜测（Tab. 2）。
- **模型家族和训练数据质量比模型规模更能预测 prompt 鲁棒性**。InternVL2 家族是最鲁棒的模型族，其中 InternVL2-40B 的校准可靠性达到 0.65，而 Qwen-VL 仅为 0.06，CogVLM GG 为 -0.12（Tab. 3）。
- **校准步骤纠正了因随机基线不同而导致的错误排序**。在 MMBench 上，未校准前否定提示（LS-N）的准确度看似优于原始提示（O），校准后恢复为 O > LS-N 的预期趋势，与平衡数据集 NYU-Depth V2 上的趋势一致（Fig. 3）。

PARC 的方法定位在 VLM 评估的可靠性量化与可比性校准层面，其可靠性评分和校准机制为公平比较不同模型在不同 prompt 条件下的表现提供了统一度量。当前框架的实验范围限定于多项选择视觉问答（MC-VQA），对开放式生成等任务的扩展仍是一个开放问题。

视觉语言模型（VLMs）在多项选择视觉问答（MC-VQA）等任务上展现了令人瞩目的能力，但其对用户输入prompt的敏感性始终是可靠部署的隐患。现实应用中，用户描述同一视觉问题的措辞可能不同，甚至可能无意中引入语义漂移——例如将“哪只动物毛发更长”改为“哪只动物毛发更短”。现有研究主要关注对抗性扰动或非系统的噪声注入，缺乏一套能够系统衡量模型对**现实prompt变化**敏感性的统一框架。更关键的是，当前评估指标（准确度、确定性、一致性）在不同数据集和prompt变体之间**不可直接比较**，因为它们的随机基线表现各不相同，导致无法公平地判断模型在何种扰动下真正退化。

PARC正是在这一缺口上提出。其核心动机是：**VLM对改变预期答案的语义变化（如否定、反义词、图像交换）高度敏感，而现有评估体系无法跨数据集、跨prompt变体量化这种敏感性的真实程度**。例如，在MMBench上，否定提示的原始准确度看似高于原始提示，但这仅是因为随机猜测在否定提示下选中正确答案的概率更高——校准后，正确排序才得以恢复（Fig. 3）。这一现象揭示了**未校准指标会掩盖模型性能的真实退化模式**，使得“哪个模型更鲁棒”这一基本问题难以回答。

此外，PARC旨在回答两个相互关联的问题：**哪些prompt变体对VLM最具破坏性，以及哪些模型族对prompt变化最不敏感**。初步观察表明，语义变化在语言和视觉模态中均同等破坏模型性能，且模型家族和训练数据质量比模型规模更能预测鲁棒性。这些发现为理解VLM的prompt敏感性提供了新的分析维度，也为后续的鲁棒性改进指明了方向。

## 核心方法与创新机理

PARC的核心创新在于构建了一个**可比较、可解释的VLM提示敏感性评估框架**，通过三个关键模块解决了现有评估中“分数不可比”与“鲁棒性无法公平排序”的根本瓶颈。

### 创新点一：系统化的现实提示变体设计

现有工作通常依赖非系统的噪声提示或不可操作的扰动来评估VLM鲁棒性，导致实验结果难以复现和比较。PARC改变了这一现状，提出了涵盖**语言和视觉两模态、重述与语义两类别**的11种现实提示变体（Table 1, Section 2.1）：

- **语言重述**（LR）：指令变化（I）、简洁化（C）、冗长化（V）
- **语言语义变化**（LS）：否定（N）、比较级反转（M）、反义词替换（A）
- **视觉重述**（VR）：模糊（B）、光照变化（L）、旋转90°（R）
- **视觉语义变化**（VS）：图像互换（S）、图像交换（E）

这一设计的核心洞察在于区分了**不改变答案的重述**与**改变答案的语义变化**：前者考察模型对表达形式的鲁棒性，后者考察模型对语义内容的理解深度。实验表明，这种区分揭示了VLM在语义变化下的一致性崩溃——反义词变体（LS-A）使校准一致性降至0.09，图像交换（VS-E）更是降至0.00（随机水平），而重述变体的一致性则显著更高（Tab. 2, Figure 4）。

### 创新点二：带显式保证的可靠性评分

现有评估将准确度、确定性、一致性分离使用，缺乏一个统一的综合指标。PARC提出了**可靠性评分**（Reliability Score），将准确度与确定性融合为单一数值：

$$rel = (2 \cdot acc - 1) \cdot cert$$

其中确定性 $cert$ 基于共形预测集大小度量（Eq. 1），1表示完全确定，0表示完全不确定。可靠性评分的取值范围为 $[-1, 1]$：1表示模型高度可靠（自信且正确），-1表示模型高度不可靠（自信但错误），0表示随机水平。

该评分的核心优势在于其**显式保证**（Eq. 6, Section 2.3）：

$$cert \geq |rel|, \quad acc_{\mathrm{calib}} \begin{cases} \geq rel & \text{for } rel > 0 \\ \leq rel & \text{for } rel < 0 \end{cases}$$

这意味着从可靠性评分可以直接读出准确度和确定性的下界：例如，可靠性为0.3保证模型至少比随机准确度高30%，且至少有30%的确定性。这种可解释的保证机制使可靠性评分不仅是排序工具，更是决策依据。

### 创新点三：基于期望随机表现的分数校准

这是PARC最关键的方法论创新。不同数据集和提示变体的随机基线不同（如MMBench有3个选项，随机准确度为0.33；NYU-Depth V2有2个选项，随机准确度为0.5），导致原始分数在跨数据集和跨变体比较时产生**错误排序**。

PARC的校准步骤（Eq. 5, Section 2.3）通过度量相对随机表现的改进来解决这一问题：

$$s_{\mathrm{calib}} = \begin{cases} \frac{s - s_{\mathrm{rand}}}{1 - s_{\mathrm{rand}}} & \text{for } s \geq s_{\mathrm{rand}} \\ \frac{s - s_{\mathrm{rand}}}{s_{\mathrm{rand}}} & \text{for } s < s_{\mathrm{rand}} \end{cases}$$

校准后，1表示理想性能，0表示随机水平，-1表示最差性能。**Figure 3** 清晰地展示了校准的纠正效果：在MMBench上，未校准前否定提示（LS-N）的准确度看似优于原始提示（O），但校准后恢复了O > LS-N的合理排序。这一纠正源于MMBench中原始提示的随机准确度为0.33（3选1），而否定提示的随机准确度为0.5（2选1），原始分数因随机基线不同而产生误导性比较。校准步骤消除了这种偏差，使所有分数在统一尺度上可比。

### 方法谱系与知识库定位

PARC在VLM评估方法谱系中占据独特位置。与传统的单一提示评估（如标准基准测试）相比，PARC引入了系统的提示扰动空间；与现有的鲁棒性评估方法相比，PARC通过校准步骤解决了跨数据集不可比的核心问题。其可靠性评分的设计借鉴了共形预测的置信度量化思想，但将其与准确度融合为可解释的综合指标，并提供了显式的性能保证。在知识库中，PARC可定位为**VLM鲁棒性评估的基础设施框架**，为后续的提示敏感性分析、模型选择和数据质量诊断提供了标准化的量化工具。

PARC 是一个系统性的 VLM prompt 敏感性分析框架，其设计目标是回答两个核心问题：(1) VLM 对哪些 prompt 变化最敏感？(2) 哪些 VLM 对 prompt 变化最不敏感（即最鲁棒）？为实现这一目标，PARC 构建了三个顺序耦合的模块，形成从 prompt 扰动生成到跨基准可比评分的完整分析流水线。

### 流水线模块与数据流

**模块一：Prompt 变体生成器（Prompt Variation Generator）**  
该模块在语言和视觉两个模态上对原始 prompt 施加系统性的变化。PARC 定义了 11 种现实场景中的 prompt 变体（见 Table 1），分为两大类：
- **重述变化（Reformulation）**：保持语义和预期答案不变，仅改变表达形式。语言重述包括指令改写（LR-I）、简洁表达（LR-C）和详细描述（LR-V）；视觉重述包括模糊（VR-B）、亮度变化（VR-L）和 90° 旋转（VR-R）。
- **语义变化（Semantic Change）**：主动改变 prompt 的语义，从而使预期答案发生变化。语言语义变化包括否定（LS-N）、比较级反转（LS-M）和反义词替换（LS-A）；视觉语义变化包括图像对调（VS-S）和正确图像替换（VS-E）。

这些变体覆盖了从表面形式扰动到深层语义翻转的完整扰动谱系，使分析能够区分模型对“形式变化”和“内容变化”的不同响应模式。

**模块二：模型评估器（Model Evaluator）与可靠性计算器（Reliability Calculator）**  
对于每个 prompt 变体，评估器测量模型的三个基础指标：准确度（accuracy）、确定性（certainty）和一致性（consistency）。其中：
- 确定性基于共形预测集大小定义：$\text{cert}(p) = 1 - \frac{|\mathcal{C}(p)| - 1}{|\mathcal{P}(p)| - 1}$，取值为 $[0,1]$，1 表示完全确定，0 表示完全不确定。
- 一致性对重述变化和语义变化采用不同的期望方向：重述变化要求响应一致（$\text{cons}^{\text{Reph}} = \mathbb{1}[\mathcal{M}(p_1) = \mathcal{M}(p_2)]$），语义变化要求响应不同（$\text{cons}^{\text{Sem}} = \mathbb{1}[\mathcal{M}(p_1) \neq \mathcal{M}(p_2)]$）。

可靠性计算器将准确度和确定性综合为单一可靠性评分：$\text{rel} = (2 \cdot \text{acc} - 1) \cdot \text{cert}$。该评分的设计使其具有直观的语义边界：$+1$ 表示模型既正确又高度确定（可靠），$-1$ 表示模型错误但高度确定（危险地自信），$0$ 表示完全不确定。

**模块三：评分校准器（Score Calibrator）**  
由于不同数据集和 prompt 变体的随机猜测基线不同（例如，MMBench 有 3 个选项，随机准确度为 0.33；而 NYU-Depth V2 有 2 个选项，随机准确度为 0.5），直接比较原始评分会产生误导。校准器通过度量相对随机表现的改进来统一所有评分：

$$s_{\text{calib}} = \begin{cases} \frac{s - s_{\text{rand}}}{1 - s_{\text{rand}}} & \text{for } s \geq s_{\text{rand}} \\ \frac{s - s_{\text{rand}}}{s_{\text{rand}}} & \text{for } s < s_{\text{rand}} \end{cases}$$

校准后，$1$ 表示理想性能，$0$ 表示随机水平，$-1$ 表示最差性能。这一步骤是 PARC 实现跨数据集、跨 prompt 变体可比性的关键机制。

### 可靠性评分的保证

可靠性评分不仅是一个汇总指标，还提供显式的性能保证（Eq. 6）：对于正可靠性 $\text{rel} > 0$，校准准确度至少为 $\text{rel}$，且确定性至少为 $|\text{rel}|$；对于负可靠性 $\text{rel} < 0$，校准准确度至多为 $\text{rel}$。这意味着从可靠性评分可以直接读出准确度和确定性的下界，无需额外计算。

### 框架的输入输出

**输入**：一组 VLM 模型、一组 VQA 数据集（包含图像和文本 prompt）以及预定义的 11 种 prompt 变体规则。  
**输出**：每个模型在每个数据集上对每种 prompt 变体的校准可靠性、准确度、确定性和一致性评分，以及跨模型和跨变体的聚合分析结果（如 Table 2 和 Table 3 所示）。

整个流水线的设计使得分析结果具有内在的可比性：校准步骤消除了随机基线差异带来的混淆效应，可靠性评分将多维度的模型行为压缩为可排序的单一数值，而系统化的变体分类则确保了对语言和视觉模态的对称覆盖。

PARC 框架由四个核心模块构成，分别对应 prompt 变体生成、模型评估、可靠性计算和分数校准，形成一条从扰动构建到可比评分的完整流水线（Fig. 1）。

### Prompt 变体生成器

该模块系统性地对原始 prompt 施加 11 种现实变体，覆盖语言和视觉两个模态，并区分为**重述**（不改变预期答案）和**语义变化**（改变预期答案）两类（Tab. 1）。语言重述包括指令、简洁、冗长三种形式；语言语义变化包括否定、反义词、MoreLess；视觉重述包括模糊、亮度、旋转；视觉语义变化包括图像交换和图像替换。这一设计使敏感度分析能够定位模型在何种扰动下最脆弱。

### 模型评估器

对每个变体后的 prompt，评估器测量三个基础指标：准确度（acc）、确定度（cert）和一致性（cons）。确定度基于共形预测集的大小定义：

$$cert(p) = 1 - \frac{|\mathcal{C}(p)| - 1}{|\mathcal{P}(p)| - 1}$$

其中 $\mathcal{C}(p)$ 为共形预测集，$\mathcal{P}(p)$ 为所有可能答案的集合。确定度为 1 表示模型完全确定，0 表示完全不确定（Eq. 1）。

一致性分两类：重述一致性要求变体间响应相同，语义一致性要求变体间响应不同：

$$cons^{\mathrm{Reph}}(p_1, p_2) = \mathbb{1}[\mathcal{M}(p_1) = \mathcal{M}(p_2)]$$

$$cons^{\mathrm{Sem}}(p_1, p_2) = \mathbb{1}[\mathcal{M}(p_1) \neq \mathcal{M}(p_2)]$$

其中 $\mathcal{M}(p)$ 表示模型对 prompt $p$ 的预测输出（Eq. 2–3）。

### 可靠性计算器

可靠性评分将准确度和确定度综合为单一指标：

$$rel = (2 \cdot acc - 1) \cdot cert$$

该公式的设计意图是：$2 \cdot acc - 1$ 将准确度从 $[0,1]$ 映射到 $[-1,1]$，乘以确定度后，可靠性为 1 表示模型自信且正确，-1 表示模型自信但错误（Eq. 4）。Fig. 2 直观展示了这一映射关系。

### 分数校准器

由于不同数据集和 prompt 变体的随机基线表现不同，原始分数无法直接比较。校准器以期望随机表现 $s_{\mathrm{rand}}$ 为基准，将任意分数 $s$ 转换为相对于随机表现的改进度量：

$$s_{\mathrm{calib}} = \begin{cases} \frac{s - s_{\mathrm{rand}}}{1 - s_{\mathrm{rand}}} & \text{for } s \geq s_{\mathrm{rand}} \\ \frac{s - s_{\mathrm{rand}}}{s_{\mathrm{rand}}} & \text{for } s < s_{\mathrm{rand}} \end{cases}$$

校准后，1 表示理想性能，0 表示随机水平，-1 表示最差可能表现（Eq. 5）。这一步骤是 PARC 实现跨数据集可比性的关键——例如在 MMBench 上，校准前否定 prompt 的准确度看似高于原始 prompt，校准后恢复为原始优于否定的合理排序（Fig. 3）。

### 可靠性保证

校准后的可靠性评分具有显式下界保证：

$$cert \geq |rel|, \quad acc_{\mathrm{calib}} \begin{cases} \geq rel & \text{for } rel > 0 \\ \leq rel & \text{for } rel < 0 \end{cases}$$

当 $rel > 0$ 时，校准准确度至少比随机水平高出 $rel$，且确定度至少为 $rel$；当 $rel < 0$ 时，准确度至少比随机水平低 $|rel|$（Eq. 6）。这一性质使可靠性评分不仅是排序工具，还能直接读出模型性能的保证边界。

## 实验与关键发现

### 核心发现：语义变化在语言与视觉模态中同等地破坏VLM性能

PARC在7个多模态基准（含MMBench、MIT-States、VAW、NYU-Depth V2、Fashionpedia等）上对22个VLM进行系统评估，揭示了一个贯穿全局的瓶颈：**VLM对改变预期答案的语义变化高度敏感，而这一脆弱性在语言和视觉模态中表现出高度对称的破坏力**。

从Table 2的平均校准可靠性来看，原始prompt（O）在所有模型和数据集上的平均可靠性为0.29，而最具破坏性的语言语义变体——反义词替换（LS-A）——将其拉低至0.10，视觉语义变体——图像交换（VS-E）——进一步降至0.13。更令人警醒的是一致性指标：LS-A的平均校准一致性仅为0.09，VS-E直接降至0.00（随机水平），意味着模型在这些扰动下几乎完全失去对正确答案的追踪能力。相比之下，重述类变体（如LR-V详细重述、VR-B模糊、VR-L光照变化）尽管也造成性能下降，但破坏程度显著低于语义变体，这一趋势在Figure 4中清晰呈现——蓝色（重述）与橙色（语义变化）之间存在显著且一致的差距，且该模式在6个比较式数据集和MMBench上高度对齐。

![[assets/figures/papers/paper_list_l14_https_arxiv_org_abs_2506_14808/figures/005_Table_2.jpg]]
*Table 2: Most perturbing prompt variations in language and vision, averaged across models. All scores are calibrated, with 1.0 being ideal model performance and 0.0 is random performance. For reliability and consistency we report results on the individual datasets along with averages across datasets, and averages across datasets for accuracy and certainty. See Tab. A6 for all measures. The consistency is calculated between each varied and the original prompt. Most perturbing prompt per variation class is bold, and across variations underlined. High number indicates model robustness to a prompt variant. Prompt variation acronyms are from Tab. 1. MMBench’s noncomparative questions about single images...*

**关键证据**：校准步骤在此扮演了决定性角色。以MMBench为例（Figure 3），未校准前否定prompt（LS-N）的准确度看似高于原始prompt（O），形成LS-N > O的误导性排序。校准后，由于MMBench具有3个选项（随机正确率约0.33），而否定prompt将选项缩减为2个（随机正确率0.5），校准纠正了随机基线差异，使排序恢复为O > LS-N，与平衡数据集NYU-Depth V2上的预期趋势一致。这一纠正机制确保了跨数据集和跨prompt变体的可比性，是PARC框架的核心贡献之一。

![[assets/figures/papers/paper_list_l14_https_arxiv_org_abs_2506_14808/figures/004_Figure_3.jpg]]
*Figure 3: Calibration effect in PARC. On MMBench [37] before calibration, models appear more accurate on negated prompts LS-N [Orange, dashed] than on the original prompts O [Blue, solid], LS-N>O. After calibrating by measuring the improvement over the expected random performance, the order switches to O>LS-N. Why should we expect VLMs to be better on O than LS-N? We take a look at NYU-Depth V2 [57] – a balanced dataset with two potential answers, where VLMs have the same expected random performance on O and LS-N. Here, VLMs still perform worse on negations than on the original prompt, showing that O>LS-N is the expected trend. Because calibration uses the same random performance of 0.5 for O and LS-...*

![[assets/figures/papers/paper_list_l14_https_arxiv_org_abs_2506_14808/figures/014_Figure_3.jpg]]
*Figure 3: Figure A7. Effect of calibration, extension of Fig. 3 for all methods. Accuracy before [Left] vs. after calibration [Right] for original [Blue] and negated [orange] prompts. Only calibration aligns the ordering – original over negation – on the imbalanced MMBench [37] dataset with the balanced NYU-Depth V2 dataset [57] and the average over all balanced comparative datasets [28]. In comparison to Fig. 3, this plot shows results for all methods and also the averages over all six balanced datasets in the last row. Table A6. Most perturbing prompt variations in language and vision, averaged across models – additional measurements for Tab. 2. All scores are calibrated, with 1.0 being ideal model...*

### 模型鲁棒性排序：InternVL2家族脱颖而出

Table 3汇总了22个模型的综合鲁棒性表现。**InternVL2-40B以0.65的校准可靠性遥遥领先**，校准一致性达0.71，在所有指标上均居首位。InternVL2家族整体表现最优，其2B版本的可靠性（0.31）甚至与LLaVA-1.5 13B（0.31）持平，说明模型家族身份比参数规模更能预测鲁棒性。相比之下，Qwen-VL（可靠性0.06）和CogVLM GG（可靠性-0.12，低于随机水平）表现最差。

Figure 5进一步揭示了规模与数据的作用机制：**在同一模型家族内部，更大参数规模确实带来更低的prompt敏感性**（Figure 5左），但跨家族比较时，训练数据质量成为主导因素——使用约1B数据训练的模型，其可靠性甚至低于Cambrian仅用约0.01B高质量数据训练的结果（Figure 5右）。这一发现暗示，当前VLM的prompt鲁棒性瓶颈可能更多源于训练数据的质量与多样性，而非单纯的模型容量不足。

![[assets/figures/papers/paper_list_l14_https_arxiv_org_abs_2506_14808/figures/009_Figure_5.jpg]]
*Figure 5: [Left] Larger models within the same family are less prompt sensitive. [Right] More high-quality data yields more prompt-agnostic models. Comparison shows models with 7B or 8B LLMs per family; with Qwen-VL for Qwen, LLaVA-1.6 7B vic for LLava-1.6 and CogVLM Chat for CogVLM. Note the logscale, also see Fig. A9*

### 消融验证

**校准的必要性**：消融实验（Figure 3扩展至Figure A7）证实，未校准分数在MMBench等不平衡数据集上会产生错误排序，校准后所有数据集的原始prompt优于否定prompt的趋势恢复一致。

**单变体评估的合理性**：Table A9显示，组合多个prompt变体（如同时施加语言和视觉扰动）导致性能等于或差于最差单个变体，验证了PARC采用单变体独立评估策略的合理性，避免了组合爆炸带来的实验成本。

**评估方式的稳健性**：Table A10表明，使用logit最高分代替直接文本输出进行评估不影响主要结论，但揭示了CogVLM GG的异常低分部分源于其文本生成格式问题，这一发现为后续模型输出格式设计提供了警示。

### 失败模式与局限性

1. **任务范围限制**：当前评估仅覆盖多项选择视觉问答（MC-VQA），PARC框架无法直接推广至开放式生成或更复杂的交互场景，其结论的泛化性需要进一步验证。
2. **视觉语义变化的筛选偏差**：VS-E（图像交换）需要人工筛选语义不同的图像对，过滤后数据量降至原始的约20%，可能引入选择偏差并限制统计效力。
3. **训练数据估计的不透明性**：Figure 5右图中训练数据量信息部分来自公开估计，不一定完全准确，影响“数据质量>数据量”这一结论的稳健性。
4. **模型覆盖的时效性**：实验未包含最新的大规模指令微调VLM（如GPT-4V系列），模型列表的代表性存在局限。

### 补充图表

![[assets/figures/papers/paper_list_l14_https_arxiv_org_abs_2506_14808/figures/003_Figure_2.jpg]]
*Figure 2: Reliability score in PARC. The plots visualize how accuracy and certainty are mapped to the reliability score. A reliability of 1 [blue] highlights a confidently correct model, while -1 [red] flags confidently incorrect models. [Left] Mapping for a balanced dataset like NYU-Depth V2 [57], where expected random accuracy is 0.5. [Right] Calibrated reliability scores for a c $c _ { \mathrm { r a n d } }$ = 0 . 2 7 , which represents MMBench [37]*

![[assets/figures/papers/paper_list_l14_https_arxiv_org_abs_2506_14808/figures/012_Figure.jpg]]
*Figure: A6. Mapping from certainty and accuracy to reliability score with \operatorname { a c c } _ { \mathrm { r a n d } } = 0 . 5 \ : / L e f t J vs. uncertainty-aware accuracy UAcc with | \mathcal { P } | = 4 ~ / M i d d l e J and | \mathcal { P } | = 1 6 ~ / R i g h t J . . Our reliability score provides two guarantees (one for accuracy and one for certainty) that can be directly seen from any score except 0. Uacc provides at most one guarantee for either accuracy or certainty. Further, its maximum changes with the number of answers per prompt | { \mathcal { P } } | . , generating scores that are incomparable across datasets*

![[assets/figures/papers/paper_list_l14_https_arxiv_org_abs_2506_14808/figures/013_Figure.jpg]]

![[assets/figures/papers/paper_list_l14_https_arxiv_org_abs_2506_14808/figures/002_Table_1.jpg]]
*Table 1: Prompt variations in PARC. Our VLM prompt variations alter language and vision through reformulations and semantic changes on comparative-style question [28]. Original question: “Which animal has longer fur? (A) Left (B) Right” with images shown above. Answer Change implies the expected answer changed compared to the original question. Prompt variation types: LR - Language Reformulation, LS - Language Semantic, VR - Vision Reformulation, VS - Vision Semantic. Variations: I - Instruction, C - Concise, V - Verbose, N - Negation, M - MoreLess, A - Antonyms, B - Blur, L - Lighting, R - Rotate, S - Swap, E - Exchange*

![[assets/figures/papers/paper_list_l14_https_arxiv_org_abs_2506_14808/figures/007_Table.jpg]]

![[assets/figures/papers/paper_list_l14_https_arxiv_org_abs_2506_14808/figures/010_Table.jpg]]

![[assets/figures/papers/paper_list_l14_https_arxiv_org_abs_2506_14808/figures/015_Table.jpg]]

## 定位与知识库关联

### 问题定位与核心瓶颈

PARC 针对视觉语言模型（VLM）评估中的一个关键盲区：**模型对用户 prompt 变化的敏感性缺乏跨数据集、跨变体的可比较度量**。现有评估通常依赖单一原始 prompt 的准确度，或使用非系统性的噪声扰动，无法区分模型是对 prompt 的表面形式敏感，还是对改变预期答案的语义扰动敏感。PARC 的分析揭示，VLM 对语义变化（如否定、反义词、图像交换）极为脆弱——语言反义词变体（LS-A）使平均校准一致性降至 0.09，图像交换变体（VS-E）更使其归零（随机水平），而重述类变体的影响相对温和（Tab. 2）。这一发现表明，**语义变化在语言和视觉模态中均同等程度地破坏 VLM 性能**，且这种敏感性并非孤立现象，而是跨模型、跨数据集的系统性模式（Fig. 4）。

### 方法谱系与差异化贡献

PARC 的贡献并非提出新的模型架构或训练范式，而是**构建一个可复用的评估框架**，其方法谱系可从三个维度定位：

**1. Prompt 扰动系统化。** 此前对 VLM prompt 敏感性的研究多采用非结构化的噪声注入或单一类型的改写。PARC 首次将 prompt 变体系统化地分为**语言重述（LR）、语言语义（LS）、视觉重述（VR）、视觉语义（VS）**四个类别，共 11 种现实变体（Tab. 1），覆盖模糊、光照、旋转、否定、反义词、图像交换等操作。这种分类使不同扰动的影响可直接比较，揭示了语义变化比重述更具破坏性的跨模态一致性（Fig. 4）。

**2. 可靠性评分的统一度量。** 传统评估将准确度、确定性和一致性分离报告，缺乏单一汇总指标。PARC 提出可靠性评分 $rel = (2 \cdot acc - 1) \cdot cert$，将准确度和基于共形预测的确定性综合为一个 $[-1, 1]$ 区间的标量：$+1$ 表示自信地正确，$-1$ 表示自信地错误（Eq. 4）。该评分附带显式保证——从可靠性值可直接读出准确度和确定性的下界（Eq. 6），这是现有评估指标不具备的性质。

**3. 基于期望随机性能的校准。** 这是 PARC 最具方法论价值的设计。不同数据集和 prompt 变体的随机猜测基线不同（如 MMBench 有 3 个选项，否定后剩 2 个），直接比较原始准确度会产生误导性排序。PARC 的校准公式 $s_{\text{calib}}$（Eq. 5）将所有评分归一化为相对于随机表现的改进度量：$1$ 为理想，$0$ 为随机，$-1$ 为最差。这一步骤纠正了 MMBench 上否定 prompt 看似优于原始 prompt 的伪象（Fig. 3），使跨数据集的公平比较成为可能。

### 适用边界与限制

PARC 框架的适用范围受以下边界条件约束：

- **任务格式限制。** 评估仅覆盖多项选择视觉问答（MC-VQA），框架无法直接迁移至开放式生成、视觉推理或交互式对话场景。共形预测集依赖于有限的候选答案空间，对自由文本输出的扩展需要重新设计确定性度量。
- **视觉语义变化的构造偏差。** 图像交换变体（VS-E）需人工筛选替换图像，仅约 20% 的原始样本通过过滤保留，可能引入选择偏差并影响统计效力。
- **模型覆盖的代表性。** 实验涵盖 22 个 VLM，但未包括最新的指令微调模型或超大规模模型（如 GPT-4V 系列），模型列表的时间代表性需要读者自行验证。
- **训练数据量的不透明性。** 关于训练数据量与鲁棒性关系的分析（Fig. 5 右）部分依赖公开估计，数据质量和组成的混杂效应尚未完全解耦。

### 关键发现与证据强度

以下发现具有较高的证据置信度：

- **语义变化是主导性破坏因素。** LS-A（反义词）和 VS-E（图像交换）在所有变体中造成最严重的一致性下降，平均校准一致性分别仅为 0.09 和 0.00（Tab. 2），置信度 0.95。
- **InternVL2 家族是最鲁棒的模型族。** InternVL2-40B 的校准可靠性达 0.65，远超所有模型的平均值 0.29，而 Qwen-VL（0.06）和 CogVLM GG（-0.12）表现最差（Tab. 3），置信度 0.95。
- **模型家族比模型规模更能预测鲁棒性。** InternVL2-2B 的鲁棒性与 LLaVA-1.5 13B 相当（Tab. 3 右），且同一家族内规模扩大带来鲁棒性增益（Fig. 5 左），但跨家族的差异主要由训练数据质量解释（Fig. 5 右），置信度 0.9。
- **校准步骤对公平比较不可或缺。** 未校准前 MMBench 上否定 prompt 的准确度错误地高于原始 prompt，校准后恢复合理排序（Fig. 3），置信度 0.95。

### 开放问题与未来方向

PARC 揭示的 prompt 敏感性现象引出一系列待解问题：

1. **框架扩展性。** 可靠性评分和校准机制能否适配开放式生成、链式推理或多轮对话等更复杂的 VLM 使用场景？
2. **敏感性的根本缓解。** prompt 敏感性是否可通过针对性微调（如对抗性 prompt 训练）或数据增强得到根本改善，还是 VLM 架构的内在属性？
3. **数据质量的具体归因。** 训练数据中的何种特征（多样性、噪声分布、指令格式、视觉-语言对齐程度）对鲁棒性贡献最大？这需要更透明的训练数据文档。
4. **更大规模模型的趋势。** 在更大规模或更先进的 VLM 上，prompt 敏感性的表现模式是否一致？语义变化的破坏性是否会随规模扩大而减弱？
5. **组合变体的非线性效应。** 初步消融显示组合多个 prompt 变体导致性能等于或差于最差单变体（Tab. A9），但更复杂的语义交互是否会产生非线性衰降，仍需系统研究。

### 知识库定位

PARC 在 VLM 评估方法谱系中占据**系统性鲁棒性诊断工具**的位置。它不替代现有的基准测试（如 MMBench、CompBench），而是提供一个可叠加的元评估层——通过统一的 prompt 变体生成、可靠性度量和校准流程，将任何 MC-VQA 基准转化为 prompt 敏感性测试平台。其核心方法论贡献（校准、可靠性保证）可独立于具体模型和数据集复用，为 VLM 的公平比较和鲁棒性分析提供了此前缺失的定量框架。

## 原文 PDF

![[paperPDFs/CVPR_2025/PARC_A_Quantitative_Framework_Uncovering_the_Symmetries_within_Vision_Language_Models.pdf]]
