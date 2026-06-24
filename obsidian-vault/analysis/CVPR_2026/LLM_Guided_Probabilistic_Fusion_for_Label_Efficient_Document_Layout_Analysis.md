---
title: LLM-Guided Probabilistic Fusion for Label-Efficient Document Layout Analysis
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/LLM_Guided_Probabilistic_Fusion_for_Label_Efficient_Document_Layout_Analysis.pdf
project_link: null
code_link: null
aliases:
- LGPFLEDLA
tags:
- CVPR_2026
- topic/other_unclear
- topic/other_unclear/general
core_operator: LLM文本结构推理与视觉检测器伪标签在融合过程中的权重分配，特别是通过实例自适应门控动态调节两种模态的置信度贡献。
primary_logic: 通过OCR-LLM管道提取文档的文本语义结构先验，并利用逆方差加权和可学习门控将其与视觉伪标签进行概率融合，从而在极少标注（5%）条件下为检测器生成高质量的伪标签，实现跨模型规模的稳定提升。
claims:
- 自适应门控比固定权重平均提升+0.9 AP，且数据依赖的PAC边界正确预测O(sqrt(k/n))收敛率。
- 在文档预训练模型LayoutLMv3上融合LLM先验，比标准半监督学习显著提升+0.6 AP (p=0.02)。
- LLM在18.7%的困难样本中通过语义消岐带来+3.8 AP的增益，远超过简单的regex文本模式。
- 在PubLayNet上用5%标签，轻量级SwiftFormer达到88.2 AP，超过所有半监督基线（例如比Dense Teacher高+2.9 AP）。
---

# LLM-Guided Probabilistic Fusion for Label-Efficient Document Layout Analysis

> [!tip] 核心洞察
> 通过OCR-LLM管道提取文档的文本语义结构先验，并利用逆方差加权和可学习门控将其与视觉伪标签进行概率融合，从而在极少标注（5%）条件下为检测器生成高质量的伪标签，实现跨模型规模的稳定提升。

| 字段 | 内容 |
|------|------|
| 中文题名 | LLM引导概率融合的标签高效文档布局分析 |
| 英文题名 | LLM-Guided Probabilistic Fusion for Label-Efficient Document Layout Analysis |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2511.08903) |
| Topic | #topic/other_unclear #topic/other_unclear/general |
| Method | LLM-Guided Probabilistic Fusion for Label-Efficient Document Layout Analysis |
| Dataset | PubLayNet, DocLayNet |

> [!tip] 效果简介
> - PubLayNet (5% labels) 上，AP 88.2 ± 0.3 (SwiftFormer adaptive) / 89.7 ± 0.4 (LayoutLMv3 adaptive) vs 85.3 ± 0.4 (Dense Teacher, best semi-supervised) / 89.1 ± 0.4 (LayoutLMv3+ semi... (+2.9 (轻量级) / +0.6 (文档预训练))。
> - DocLayNet (5% labels) 上，AP 84.8 vs 79.4 (STEP-DETR) (+5.4)。

## 概述

文档布局分析是文档理解的基础任务，其目标是将页面中的文本、标题、图表、表格等元素精确地检测和分类。然而，现有半监督方法严重依赖视觉教师模型生成的伪标签，这些伪标签存在系统性偏差——教师模型往往难以处理稀有布局元素，并频繁混淆语义相近的类别（如将页脚误判为标题），仅凭视觉线索难以有效纠正这一瓶颈。

本文提出 **LLM-Guided Probabilistic Fusion**，一种标签高效的文档布局分析框架。其核心思想是：通过 OCR-LLM 管道提取文档的文本语义结构先验，并将其与视觉教师检测器的预测进行概率融合，从而在极少标注条件下为检测器生成高质量的精炼伪标签。该框架的关键创新在于**实例自适应门控机制**——通过可学习的轻量门控网络（仅 64K 参数，0.24% 开销）动态调节视觉与语言两种模态的置信度贡献，而非使用固定权重。

在 PubLayNet 数据集上仅使用 5% 标注的条件下，轻量级 SwiftFormer 变体达到 **88.2 ± 0.3 AP**，超越所有半监督基线（比最佳方法 Dense Teacher 高 **+2.9 AP**）；在文档预训练模型 LayoutLMv3 上进一步达到 **89.7 ± 0.4 AP**，显著优于标准半监督学习（89.1 ± 0.4 AP，p=0.02）。在更具挑战性的 DocLayNet（11 类）上，该方法以 **84.8 AP** 的成绩比 STEP-DETR 高出 **+5.4 AP**。消融实验表明，LLM 在 18.7% 的困难样本中通过语义消歧带来 **+3.8 AP** 的定向增益，远超简单的正则表达式文本模式。理论分析进一步给出了数据依赖的 PAC 泛化边界，解释了门控网络在有限样本下的高效学习能力。

本工作为半监督文档布局分析引入了一种新的多模态融合范式，证明了 LLM 的结构推理能力可以作为视觉检测器的有效补充信号，在标签极度稀缺的场景下实现跨模型规模的稳定提升。

## 背景与动机

### 文档布局分析的核心挑战

文档布局分析（Document Layout Analysis, DLA）旨在自动识别和定位文档页面中的结构化元素，如标题、正文段落、表格、图像和页脚等。作为文档智能处理的基础任务，DLA直接影响下游应用（如信息抽取、文档检索和版面重建）的性能。近年来，基于DETR架构的检测器在该领域取得了显著进展，但其成功高度依赖于大规模像素级标注数据——例如PubLayNet数据集包含超过36万页的精细标注。在实际应用中，获取如此规模的标注成本高昂且难以扩展到专业领域文档（如医学报告、法律合同、财务报表），这使得**标签高效学习**成为DLA领域亟待解决的核心瓶颈。

### 现有半监督方法的系统性不足

为缓解标注需求，半监督学习（Semi-Supervised Learning, SSL）被广泛采用。主流的teacher-student框架（如**Mean Teacher**（Tarvainen et al., NeurIPS 2017）、**SoftTeacher**（Xu et al., ICCV 2021）、**Dense Teacher**）通过教师模型为无标签数据生成伪标签来扩充训练信号。然而，在文档布局场景中，这些方法面临一个**根本性困境**：教师模型生成的视觉伪标签存在系统性偏差。

具体而言，当标注数据极为稀疏（如仅5%标签）时，教师模型难以充分学习稀有布局元素的视觉特征，导致两类典型失败模式：

1. **稀有类别漏检与混淆**：表格、图表等出现频率较低的布局元素容易被遗漏或误分类为正文；标题与页脚因视觉外观相似（均为小尺寸文本块）而频繁混淆。
2. **纯视觉线索的语义盲区**：视觉检测器仅依赖像素级特征，无法利用文档内在的语义结构——例如，一段位于页面顶部的粗体文本究竟是“标题”还是“强调段落”，仅凭视觉外观难以判断，但结合其文本内容的语义角色（如是否为章节名称）则可明确区分。

### 文本语义先验的未充分利用

文档天然具有多模态特性：视觉布局与文本语义共同定义了元素的结构角色。现有工作对此的利用存在明显鸿沟：

- **多模态预训练模型**（如**LayoutLMv3**（Huang et al., ACM MM 2022）、**UDOP**（Tang et al., CVPR 2023））在预训练阶段融合文本与布局信息，但在半监督微调时仍仅依赖教师模型的视觉预测，未能显式引入文本语义作为独立的伪标签监督源。
- **基于规则的文本启发式方法**（如通过正则表达式匹配“Figure”开头的文本块推断其为图表标题）虽可提供简单的语义线索，但缺乏对文档层次结构和语义消歧的深层理解，性能增益有限（仅84.9 AP，远低于本文融合方法的87.3 AP）。

### 本文的核心动机

上述分析揭示了一个明确的研究机遇：**能否将大型语言模型（LLM）的文本结构推理能力作为独立的先验知识源，与视觉检测器的伪标签进行原则性融合，从而在极少标注条件下显著提升伪标签质量？**

这一动机基于以下关键观察：

- 现代LLM（如GPT-4o、Llama-3）在文本理解和结构推理方面展现出强大能力，可通过OCR文本及其空间坐标推断文档的层次化区域结构。
- LLM的语义推理与视觉检测器的模式识别具有**互补性**：前者擅长基于文本内容进行语义消歧（如区分标题与页脚），后者擅长精确的边界框定位。
- 二者的融合需要解决一个非平凡问题：如何根据实例级的不确定性动态分配两种模态的置信度权重，而非采用固定的启发式规则。

本文提出的LLM-Guided Probabilistic Fusion框架正是围绕这一动机展开：通过OCR-LLM管道提取文本结构先验，利用逆方差加权和可学习实例自适应门控将其与视觉伪标签进行概率融合，在仅5%标签的条件下为检测器生成高质量的精炼伪标签，实现跨模型规模的稳定性能提升。

## 核心创新

本文的核心贡献在于提出了一种**LLM引导的概率融合框架**，将大语言模型的文本结构推理能力与视觉检测器的感知能力系统性地结合，以解决半监督文档布局分析中伪标签质量不足的瓶颈问题。其关键创新可归纳为四个“changed slots”，每个都对应标准teacher-student框架中的一项根本性改进。

### 1. 伪标签生成源：从单一视觉到多模态融合

标准半监督检测框架仅依赖视觉教师模型的预测作为伪标签。当标注数据极度稀缺（例如5%标签）时，教师模型容易产生系统性偏差，尤其难以处理稀有布局元素和精细语义区分——例如，页脚与标题在视觉特征上高度相似，仅凭视觉线索难以可靠区分。

本文的核心突破在于引入**OCR-LLM管道**作为第二路伪标签来源。具体而言，Tesseract OCR首先提取文档中的文本块及其空间坐标，随后LLM（如GPT-4o-mini）基于这些文本内容和位置信息推断文档的层次结构区域，输出类别、边界框和置信度。教师检测器的视觉预测与LLM的结构推理通过IoU匹配对齐，再经概率融合生成精炼伪标签，用于训练学生模型。

这一设计的深层洞察在于：**LLM的文本语义先验与视觉检测器的空间定位能力是互补的**。LLM擅长通过语义消歧区分“标题”与“页脚”，而视觉检测器在精确边界框回归上更具优势。实验证实，在18.7%的困难样本中，LLM提供了针对性的语义消歧，带来**+3.8 AP**的增益，远超简单的regex文本模式（如仅凭“Figure”开头判定为标题，仅达84.9 AP）。

### 2. 融合权重策略：从固定启发式到不确定性引导的自适应门控

多模态融合的核心挑战在于**如何动态分配两种模态的置信度贡献**。简单的固定权重策略（如α=0.6）忽略了不同样本上教师和LLM相对可靠性的显著差异。

本文提出了两层递进的融合策略：

**第一层：逆方差加权（固定融合）**。假设教师和LLM的预测误差服从零均值高斯分布，则最小方差无偏估计的最优融合权重由各自方差决定：

$$b_f = \frac{ \frac{b_i^t}{\sigma_t^2} + \frac{b_k^{llm}}{\sigma_l^2} }{ \frac{1}{\sigma_t^2} + \frac{1}{\sigma_l^2} }$$

其中教师方差$\sigma_t^2$由其预测置信度估计，LLM方差$\sigma_l^2$通过验证集校准。这一策略确保了高置信度来源在融合中占据更大权重。

**第二层：可学习的实例自适应门控**。固定逆方差融合假设所有样本共享相同的融合逻辑，但实际中LLM的优势因文档类型、OCR质量和布局复杂度而异。为此，本文引入一个轻量级门控网络$g_\theta(x)$，以教师置信度、LLM置信度和IoU构成的三维统计量$\psi$为输入，为每个实例动态输出融合权重：

$$\hat{y}_f(x) = g_\theta(x) \cdot \hat{y}_t + (1 - g_\theta(x)) \cdot \hat{y}_l$$

该门控网络仅增加**64K参数（0.24%开销）**，却带来显著提升：在轻量级SwiftFormer上**+0.9 AP**，在LayoutLMv3上**+0.3 AP**，且校准误差（ECE）从0.089降至0.068。更重要的是，本文从理论上给出了数据依赖的PAC泛化边界，证明有效复杂度$k = \dim(\psi) \cdot \log(1 + L B_\theta \sigma \sqrt{n})$决定了门控网络的样本效率，其收敛率为$\tilde{O}(\sqrt{k/n})$，解释了尽管门控网络有64K参数，仍能在26K样本下成功学习的原因。

### 3. 辅助监督信号：跨模态一致性损失

伪标签训练的固有风险在于错误伪标签可能被模型“确认”并放大。为稳定训练过程，本文引入了**跨模态一致性损失**$\mathcal{L}_{cons}$：

$$\mathcal{L}_{cons} = \frac{1}{N} \sum_{i=1}^N \mathcal{H}_{\{t_i \neq \emptyset\}} \left( 1 - \frac{f_v(q_i) \cdot f_t(t_i)}{\|f_v(q_i)\| \|f_t(t_i)\|} \right)$$

该损失通过余弦相似度拉近检测器查询的视觉特征$f_v(q_i)$与对应OCR文本嵌入$f_t(t_i)$，强制模型学习视觉与文本模态之间的对齐关系。这为标准半监督框架提供了额外的正则化信号，消融实验表明移除该损失导致性能下降。

### 4. 训练策略：课程学习式的渐进融合

直接将融合伪标签投入训练可能导致早期训练不稳定，因为此时教师模型本身尚不成熟。本文设计了**三阶段课程学习策略**：

- **Epoch 1-2**：仅使用高置信度教师伪标签预热，避免LLM噪声干扰早期学习；
- **Epoch 3-5**：引入融合预测，逐步让模型适应多模态伪标签；
- **Epoch 6+**：加入LLM独有的稀有类软标签，增强对长尾类别的覆盖。

这一渐进策略确保了模型在稳定基础上逐步吸收LLM的结构知识，避免了两路信号直接冲突导致的训练震荡。

### 创新的系统性意义

上述四个changed slots构成了一个协同增强的闭环：LLM提供语义结构先验（创新1），不确定性引导的自适应门控智能地融合两路信号（创新2），跨模态一致性损失稳定训练过程（创新3），课程学习策略确保平滑过渡（创新4）。其结果是，在PubLayNet仅5%标签的条件下，轻量级SwiftFormer达到**88.2 AP**，超过所有半监督基线（比Dense Teacher高**+2.9 AP**）；文档预训练模型LayoutLMv3达到**89.7 AP**，显著超越标准半监督学习（p=0.02）。在更复杂的DocLayNet上，该方法比STEP-DETR提升**+5.4 AP**，验证了其跨数据集的泛化能力。

## 整体框架

本文提出了一种LLM引导的半监督文档布局分析框架，其核心思想是将文本大语言模型的结构推理能力与视觉检测器的感知能力进行概率融合，从而在极低标注率（5%）下生成高质量的伪标签。整个pipeline由五个关键模块串联构成，形成从原始文档到精炼伪标签再到学生模型训练的闭环。

**输入与预处理**：对于每张无标签文档图像，首先通过Tesseract OCR引擎提取文本块及其空间坐标（边界框），作为后续LLM推理的基元。OCR输出既保留了文档的文本语义，又提供了粗粒度的空间位置信息。

**LLM结构推理**：OCR提取的文本块及其坐标被送入LLM（默认使用GPT-4o-mini，也支持Llama-3等开源模型），通过精心设计的提示词，LLM推断文档的层次结构区域，输出每个区域的类别标签、边界框和置信度分数。这一模块为框架注入了文本语义先验——LLM能够基于内容理解区分“标题”与“页脚”等视觉上容易混淆的元素，这是纯视觉检测器难以做到的。

**教师检测器**：视觉分支采用基于EMA（动量0.999）更新的教师模型，对同一无标签图像生成视觉预测（边界框和类别置信度）。教师模型与学生模型共享架构（默认SwiftFormer-Tiny DETR，26M参数），但通过指数移动平均保持更稳定的预测。

**IoU匹配与概率融合**：这是框架的核心创新模块。教师预测与LLM区域首先通过IoU进行匹配对齐，随后采用逆方差加权策略进行融合——边界框融合遵循最小方差无偏估计原则：

$$b_f = \frac{ \frac{b_i^t}{\sigma_t^2} + \frac{b_k^{llm}}{\sigma_l^2} }{ \frac{1}{\sigma_t^2} + \frac{1}{\sigma_l^2} }$$

类别置信度则通过可学习的实例自适应门控网络（仅64K参数，占模型总量的0.24%）动态调节教师与LLM的贡献权重。门控网络以教师置信度、LLM置信度和IoU构成的三维统计量$\psi$为输入，输出样本级的融合系数$g_\theta(x)$，从而在LLM推理质量高时增加其权重，在OCR噪声大或LLM不确定时自动退回到视觉预测主导。

**学生模型训练**：融合后的精炼伪标签（包含边界框、类别标签和置信度）用于训练学生检测器。训练采用三阶段课程学习策略：第1-2轮仅使用高置信度教师伪标签预热；第3轮起引入融合预测；第6轮后加入LLM独有的稀有类软标签。完整训练目标联合了有标签数据的监督损失$\mathcal{L}_{sup}$、无标签数据的伪标签损失$\mathcal{L}_{pseudo}$以及跨模态一致性损失$\mathcal{L}_{cons}$：

$$\mathcal{L} = \mathcal{L}_{sup}(\mathcal{D}_{labeled}) + \lambda_{pseudo} \mathcal{L}_{pseudo}(\mathcal{D}_{unlabeled}) + \lambda_{cons} \mathcal{L}_{cons}(\mathcal{D}_{unlabeled})$$

其中跨模态一致性损失通过余弦相似度拉近视觉查询特征与对应OCR文本嵌入，作为辅助监督信号稳定伪标签训练：

$$\mathcal{L}_{cons} = \frac{1}{N} \sum_{i=1}^N \mathcal{H}_{\{t_i \neq \emptyset\}} \left( 1 - \frac{f_v(q_i) \cdot f_t(t_i)}{\|f_v(q_i)\| \|f_t(t_i)\|} \right)$$

**推理阶段**：仅使用训练完成的学生检测器进行前向推理，无需LLM、OCR或教师模型参与，推理成本与标准DETR检测器完全一致。

整个框架的设计哲学是“先融合后训练”：LLM预处理是一次性的（结果可缓存复用），融合模块仅在伪标签生成阶段介入，不增加推理时的计算开销。这种解耦设计使得框架可以灵活适配不同的检测器骨干（从轻量级SwiftFormer到文档预训练的LayoutLMv3），并兼容商业API和本地开源LLM两种部署模式。

### 补充图表

![[assets/figures/papers/paper_list_l761_https_arxiv_org_abs_2511_08903/figures/001_Figure_1.jpg]]
*Figure 1: LLM-guided semi-supervised framework. OCR text is sent to LLM for structural inference; teacher detector generates visual predictions. Fused via IoU matching and confidence weighting. Student trains on refined pseudo-labels*

## 核心模块与公式推导

### 框架总览

该方法围绕一个轻量级 DETR 风格检测器构建，主干网络采用 **SwiftFormer-Tiny**，支持单 GPU 高效训练。对于无标签文档，通过融合教师检测器预测与 LLM 结构推理来生成精炼伪标签，整体流程如 Figure 1 所示。框架包含五个核心模块：OCR 文本提取、LLM 结构推理、教师检测器、IoU 匹配与融合、学生检测器训练。

### 有监督检测损失

基础检测器采用标准 DETR 损失，通过匈牙利匹配建立预测与真值之间的最优分配：

$$
\mathcal{L}_{sup} = \sum_{i=1}^N \Big[ \mathcal{L}_{cls}\big(\hat{y}_i, y_{\sigma(i)}\big) + \mathcal{H}_{\{y_{\sigma(i)}\neq\emptyset\}} \Big( \lambda_{box}\mathcal{L}_{L1}\big(\hat{b}_i, b_{\sigma(i)}\big) + \lambda_{giou}\mathcal{L}_{giou}\big(\hat{b}_i, b_{\sigma(i)}\big) \Big) \Big]
$$

其中 $\mathcal{L}_{cls}$ 为焦点分类损失，$\mathcal{L}_{L1}$ 和 $\mathcal{L}_{giou}$ 分别为边界框的 L1 回归损失与 GIoU 损失，$\sigma(i)$ 表示匈牙利匹配后的最优分配，指示函数 $\mathcal{H}$ 确保仅对非空匹配计算定位损失。

### 概率融合机制

融合的核心思想是将教师检测器与 LLM 视为两个独立预测源，通过不确定性引导的加权产生最小方差估计。对于匹配的预测对，融合边界框采用逆方差加权：

$$
b_f = \frac{ \frac{b_i^t}{\sigma_t^2} + \frac{b_k^{llm}}{\sigma_l^2} }{ \frac{1}{\sigma_t^2} + \frac{1}{\sigma_l^2} }
$$

其中 $\sigma_t^2$ 和 $\sigma_l^2$ 分别为教师预测和 LLM 预测的方差，$b_i^t$ 和 $b_k^{llm}$ 为对应的边界框坐标。该公式在假设两个预测源无偏且独立（或已知相关系数 $\rho$）时，给出最小方差无偏估计。

### 自适应门控网络

固定权重融合无法适应不同样本中两种模态置信度的动态变化。为此引入一个轻量级可学习门控网络 $g_\theta(x)$，仅增加 **64K 参数**（约 0.24% 的模型开销），实现实例自适应融合：

$$\hat{y}_f(x) = g_\theta(x) \cdot \hat{y}_t + (1 - g_\theta(x)) \cdot \hat{y}_l$$

门控网络以教师置信度、LLM 置信度和匹配 IoU 构成的三维统计量 $\psi$ 作为输入，通过小规模 MLP 输出融合权重。实验表明，该自适应门控相比固定逆方差融合在轻量模型上提升 **+0.9 AP**，在 LayoutLMv3 上提升 **+0.3 AP**，且校准误差（ECE）从 0.089 降至 0.068。

### 跨模态一致性损失

为稳定伪标签训练并促使视觉特征与文本语义对齐，引入跨模态一致性损失：

$$
\mathcal{L}_{cons} = \frac{1}{N} \sum_{i=1}^N \mathcal{H}_{\{t_i \neq \emptyset\}} \left( 1 - \frac{f_v(q_i) \cdot f_t(t_i)}{\|f_v(q_i)\| \|f_t(t_i)\|} \right)
$$

其中 $f_v(q_i)$ 为检测器查询的视觉特征，$f_t(t_i)$ 为对应 OCR 文本块的嵌入表示，通过余弦相似度拉近两个模态的特征空间。该损失仅作用于有对应文本的查询位置。

### 总训练目标

完整的训练目标联合三个损失项：

$$
\mathcal{L} = \mathcal{L}_{sup}(\mathcal{D}_{labeled}) + \lambda_{pseudo} \mathcal{L}_{pseudo}(\mathcal{D}_{unlabeled}) + \lambda_{cons} \mathcal{L}_{cons}(\mathcal{D}_{unlabeled})
$$

其中 $\mathcal{L}_{sup}$ 作用于有标签数据，$\mathcal{L}_{pseudo}$ 为无标签数据上的精炼伪标签损失，$\mathcal{L}_{cons}$ 为跨模态一致性损失，$\lambda_{pseudo}$ 和 $\lambda_{cons}$ 为平衡系数。

### 课程学习策略

训练采用三阶段课程学习：(1) Epoch 1–2 仅使用高置信度教师伪标签进行预热；(2) 随后引入 LLM 融合预测；(3) 从 Epoch 6 开始加入 LLM 独有的稀有类软伪标签。这种渐进式策略有效避免了训练初期融合信号不稳定带来的干扰。

### 理论泛化边界

为解释门控网络在仅 26K 样本下的成功学习，论文给出了数据依赖的 PAC 泛化边界。定义由教师置信度、LLM 置信度和 IoU 构成的三维统计量 $\psi$ 的有效复杂度：

$$k = \dim(\psi) \cdot \log(1 + L B_{\theta} \sigma \sqrt{n})$$

其中 $L$ 为门控网络的 Lipschitz 常数（实测约 8.3），$B_\theta$ 为参数范数界，$\sigma$ 为噪声水平。由此得到泛化误差界：

$$R(g_{\theta}) \leq \min_{g \in \mathcal{G}} R(g) + \tilde{O}\left( \sqrt{\frac{k}{n}} + \sqrt{\frac{\log(1/\delta)}{n}} \right)$$

该边界正确预测了 $O(\sqrt{k/n})$ 的收敛率，表明尽管门控网络有 64K 参数，其有效复杂度 $k$ 远小于参数规模，从而在有限样本下仍能有效学习。

### 补充图表

![[assets/figures/papers/paper_list_l761_https_arxiv_org_abs_2511_08903/figures/005_Table_5.jpg]]
*Table 5: Fusion strategy comparison. Probabilistic fusion outperforms fixed heuristics*

## 实验与分析

### 主实验结果

#### PubLayNet 基准（5%标签）

在 PubLayNet 数据集上仅使用 5% 标注数据，本文提出的 LLM 引导概率融合框架在两种检测器架构上均取得了显著提升（Table 1）：

![[assets/figures/papers/paper_list_l761_https_arxiv_org_abs_2511_08903/figures/002_Table_1.jpg]]
*Table 1: PubLayNet results (5 categories, 5% labels). Significance: *: p\<0.05, **: p\<0.01, ***: p\<0.001. UDOP and Dense Teacher results reported from original papers [8, 32]*

- **轻量级变体**（SwiftFormer-Tiny 26M + 自适应门控）达到 **88.2±0.3 AP**，超越所有半监督基线方法，包括比最佳半监督方法 **Dense Teacher** 高出 **+2.9 AP**。
- **文档预训练变体**（LayoutLMv3 133M + 自适应门控）达到 **89.7±0.4 AP**，相比标准半监督学习的 LayoutLMv3（89.1±0.4 AP）提升 **+0.6 AP**（p=0.02），且通过双单侧检验（TOST，等效边界 ±0.5 mAP）确认该提升在统计上显著且实用上不可忽略。

值得关注的是，纯监督的 SwiftFormer-DETR（5%标签）仅取得 82.3 AP，而简单的 **regex 文本启发式基线**（如检测以“Figure”开头的文本块并标记为标题）仅达到 84.9 AP，远低于融合方法的 87.3 AP（固定权重变体），表明 LLM 的语义消歧能力远超简单的文本模式匹配。

#### DocLayNet 基准（5%标签）

在更具挑战性的 DocLayNet 数据集（11 类别，含多种稀有布局元素）上，本文方法达到 **84.8 AP**，相比 **STEP-DETR**（79.4 AP）提升 **+5.4 AP**（Table 11）。逐类别分析（Table 2）显示，LLM 融合对稀有类别（如页眉、页脚、公式）的增益尤为显著，验证了 LLM 结构先验在处理长尾布局元素时的核心价值。

![[assets/figures/papers/paper_list_l761_https_arxiv_org_abs_2511_08903/figures/010_Table_11.jpg]]
*Table 11: Complete DocLayNet results (11 categories, 5% labels)*

### 消融实验

Table 3 的组件消融研究（PubLayNet 5%标签，SwiftFormer 骨干）系统性地量化了各模块贡献：

![[assets/figures/papers/paper_list_l761_https_arxiv_org_abs_2511_08903/figures/003_Table_3.jpg]]
*Table 3: Ablation study on PubLayNet (5% labels). Component contributions*

| 配置 | AP | 相对基线增益 |
|------|-----|-------------|
| 纯监督基线（5%标签） | 82.3 | — |
| + LLM 融合（固定权重） + 跨模态一致性 | 87.3 | +5.0 |
| − 移除 LLM（仅教师伪标签） | 84.3 | −3.0 |
| − 移除融合机制（仅 LLM 或仅教师） | 86.1 | −1.2 |
| − 移除跨模态一致性损失 | 86.5 | −0.8 |

关键发现：
- **LLM 结构先验**贡献最大（+3.0 AP），移除后模型退化为标准 teacher-student 框架。
- **概率融合机制**提供额外 +1.2 AP，验证了逆方差加权在协调两种异质预测源上的有效性。
- **跨模态一致性损失**（$\mathcal{L}_{cons}$）通过拉近视觉查询特征与 OCR 文本嵌入，稳定了伪标签训练过程，贡献 +0.8 AP。

### 融合策略分析

Table 5 对比了不同融合策略的性能差异。固定启发式权重（α=0.6, w_t=0.7, w_l=0.3）虽优于无融合基线，但**可学习的实例自适应门控**（仅 64K 参数，0.24% 推理开销）在轻量模型上进一步带来 **+0.9 AP** 的提升，在 LayoutLMv3 上提升 **+0.3 AP**。更重要的是，自适应门控将期望校准误差（ECE）从 0.089 降至 0.068，表明融合置信度更准确地反映了预测质量。

门控网络的有效性源于其数据依赖的泛化特性。理论分析（Theorem 2）给出的 PAC 边界为 $R(g_{\theta}) \leq \min_{g \in \mathcal{G}} R(g) + \tilde{O}\left( \sqrt{\frac{k}{n}} \right)$，其中有效复杂度 $k = \dim(\psi) \cdot \log(1 + L B_{\theta} \sigma \sqrt{n})$ 由教师置信度、LLM 置信度和 IoU 构成的三维统计量决定。该边界解释了尽管门控网络拥有 64K 参数，仍能在约 26K 无标签样本下成功学习的原因——其有效复杂度受限于低维输入空间的互补维度。

### LLM 选择与成本分析

Table 4 对比了不同 LLM 在 PubLayNet 上的表现。商业 API 模型（GPT-4o-mini、Claude、Gemini）性能差异在 0.1–0.3 mAP 以内，表明框架对具体 LLM 选择具有鲁棒性。开源模型（Llama-3-70B）同样可用，但性能略低。

![[assets/figures/papers/paper_list_l761_https_arxiv_org_abs_2511_08903/figures/004_Table_4.jpg]]
*Table 4: Comparison of LLMs on PubLayNet (5% labels) using lightweight (Swift) and pretrained (LLMv3) teachers*

成本分析（Table 7）显示，使用 GPT-4o-mini 处理 360K 文档的 API 费用约为 **$12/50K 页**，而本地部署 Llama-3-70B 则需消耗约 **17 GPU 小时/50K 页**。由于 LLM 推理结果可缓存复用（同一文档的布局结构先验不变），实际部署中的边际成本可控。

![[assets/figures/papers/paper_list_l761_https_arxiv_org_abs_2511_08903/figures/007_Table_7.jpg]]
*Table 7: Cost comparison for 360K documents*

### 错误分析与 LLM 价值量化

Table 8 在 10K 验证页上量化了 LLM 融合的语义消歧价值。在 **18.7%** 的困难样本中，LLM 通过语义消歧带来 **+3.8 AP** 的增益，这些样本通常涉及视觉上难以区分的类别（如标题 vs 页脚、表格标题 vs 正文）。定性示例（Figure 2）展示了三类典型增益模式：(a) 类别纠正——LLM 识别出视觉检测器误判的标题；(b) 定位精化——LLM 结构推理修正了边界框范围；(c) 置信度增强——融合后低置信度预测被提升至高置信度。

![[assets/figures/papers/paper_list_l761_https_arxiv_org_abs_2511_08903/figures/015_Figure_2.jpg]]
*Figure 2: Qualitative examples: (a) Class correction, (b) Localization refinement, (c) Confidence boosting*

![[assets/figures/papers/paper_list_l761_https_arxiv_org_abs_2511_08903/figures/008_Table_8.jpg]]
*Table 8: Error analysis on 10K validation pages. LLM value via class disambiguation*

### 标签效率与鲁棒性

Figure 3 的标签效率曲线显示，本文方法在 10% 标签时已接近全监督性能，验证了 LLM 先验在极低标注预算下的价值。鲁棒性评估（Table 12）涵盖多语言文档和 OCR 噪声场景：在非英语文档上，方法仍保持优势，但性能增益有所下降，提示英文优化的 LLM 提示词在跨语言场景中需要适配；在 OCR 质量退化条件下，自适应门控自动降低 LLM 权重（Figure 4），使框架对文本提取噪声具有内在鲁棒性。

![[assets/figures/papers/paper_list_l761_https_arxiv_org_abs_2511_08903/figures/016_Figure_3.jpg]]
*Figure 3: Label efficiency on PubLayNet. Near-supervised performance at 10% labels*

![[assets/figures/papers/paper_list_l761_https_arxiv_org_abs_2511_08903/figures/017_Figure_4.jpg]]
*Figure 4: Adaptive gating vs OCR confidence. Learned gate down-weights text as quality degrades*

### 失败模式

尽管整体性能优异，以下场景仍存在局限：
- **密集多列布局**（如报纸、杂志）：LLM 依赖空间坐标推断阅读顺序，对复杂分栏结构的理解有限，可能导致区域划分错误。
- **嵌套结构**：带子标题的图表、多层表格等超出现有的扁平区域检测能力，LLM 无法输出层次化标注。
- **混合脚本文档**：夹杂数学公式的英文文献可能混淆 LLM 的结构推理，需要针对性的提示工程或视觉基础推理补充。

### 补充图表

![[assets/figures/papers/paper_list_l761_https_arxiv_org_abs_2511_08903/figures/006_Table_6.jpg]]
*Table 6: Efficiency on PubLayNet (5% labels, A100 GPU). “Adaptive” adds a 64K-param gate*

## 方法谱系与知识库定位

### 1. 方法谱系：从半监督目标检测到多模态伪标签精炼

本文提出的 **LLM-Guided Probabilistic Fusion** 框架处于半监督目标检测（SSOD）与文档多模态理解的交叉地带，其核心创新在于将LLM的文本结构推理作为除视觉教师模型之外的第二个伪标签生成源，并通过概率融合机制协调两者的贡献。

**相对于半监督检测基线的演进：** 标准SSOD范式——如 **Mean Teacher**（Tarvainen et al., NeurIPS 2017）及其检测领域的衍生 **SoftTeacher**（Xu et al., ICCV 2021）、**Dense Teacher**——依赖单一教师模型对无标签数据生成伪标签，通过EMA更新和置信度阈值筛选来保证质量。这些方法在文档布局检测中面临系统性瓶颈：教师模型的视觉预测在稀有类别（如页脚、图表标题）和语义模糊区域（如标题与正文的区分）上存在结构性偏差，且仅凭视觉线索无法自我纠正。本文的方法在伪标签生成源上进行了根本性扩展：引入OCR-LLM管道作为独立的语义推理源，通过IoU匹配将LLM推断的文档层次结构区域与教师预测对齐，再经概率融合生成精炼伪标签。这一设计将SSOD从“单源伪标签筛选”推进到“多源伪标签融合”。

**相对于文档多模态预训练模型的定位：** **LayoutLMv3**（Huang et al., ACM MM 2022）和 **UDOP**（Tang et al., CVPR 2023）等模型通过大规模文档预训练将视觉、文本和布局信息统一编码，在标注充足时表现优异。然而，当标签极度稀缺（5%）时，这些模型的半监督微调仍受限于伪标签质量。本文的方法并非替代文档预训练模型，而是作为其半监督训练的增强层：实验表明，在LayoutLMv3上叠加LLM引导的融合框架，比标准半监督学习提升+0.6 AP（p=0.02），证明了融合策略与文档预训练之间的互补性。

**方法谱系中的关键分化点：** 与简单的文本启发式（regex模式匹配，如“以‘Figure’开头即判为图表标题”）相比，LLM的语义消歧能力是质变而非量变。Regex baseline仅达到84.9 AP，而融合方法达到87.3 AP，差距达2.4 AP。更重要的是，LLM在18.7%的困难样本中通过语义消歧带来+3.8 AP的增益，这些样本正是regex和纯视觉方法共同失效的区域。

### 2. 知识库定位：理论支撑与适用边界

**理论贡献的定位：** 本文从PAC学习角度为自适应门控网络提供了数据依赖的泛化边界（Theorem 2），将门控网络的样本效率归因于由教师置信度、LLM置信度和IoU构成的三维统计量所诱导的有效复杂度 $k = \dim(\psi) \cdot \log(1 + L B_{\theta} \sigma \sqrt{n})$。该边界预测了 $\tilde{O}(\sqrt{k/n})$ 的收敛率，解释了尽管门控网络有64K参数，仍能在仅26K样本下成功学习的原因。这一理论分析将多模态融合的实践从启发式调参提升到有理论保障的层次，为后续研究提供了可分析的框架。

**适用边界与局限：**

1. **文档类型边界：** LLM的结构知识对学术论文、报告、表格等常见文档格式最为有效。高度专业化的格式（乐谱、建筑蓝图、化学结构图）超出了当前LLM的结构推理能力，需要领域适配的提示或视觉基础推理。密集多列布局（报纸、杂志）中，LLM依赖空间坐标推断阅读顺序的准确性有限。

2. **语言边界：** 当前提示词针对英语优化，非拉丁文字（阿拉伯语、中文等）需语言特定提示。混合脚本文档（如夹杂数学公式的英文文献）可能混淆LLM的结构推理。

3. **任务边界：** 评估局限于布局检测任务（PubLayNet, DocLayNet）。该融合策略是否适用于需要更深层语义理解的文档VQA任务（如DocVQA、InfographicsVQA）尚未验证——这些任务中文本与布局的交互更为复杂，当前框架仅优化检测类伪标签。

4. **计算与隐私权衡：** 单次LLM预处理需要API调用（GPT-4o-mini约$12/50K页）或本地部署（Llama-3-70B消耗17 GPU小时每50K页）。对于有严格数据隐私要求的组织，本地推理引入额外算力成本。不过，LLM推理结果可缓存复用，边际成本随文档量增加而递减。

### 3. 开放问题

1. **任务泛化：** LLM引导的融合框架能否推广到文档VQA等需要深层语义理解的任务？这些任务中视觉与文本的交互远复杂于布局检测，当前的逆方差加权和门控机制可能需要重新设计以处理多步推理的置信度传播。

2. **多语言与跨脚本鲁棒性：** 在专门的CJK、RTL文档基准上，当前的英文提示策略和OCR管道是否需要根本性重新设计？多语言场景下的LLM结构推理质量下降是否可以通过多语言提示工程或翻译增强来缓解？

3. **领域自适应的效率：** 是否可以通过零样本或小样本推理的提示策略进一步降低对专用LLM预处理的需求？例如，利用LLM的上下文学习能力，在少量标注样本上自动生成领域特定的结构推理提示，从而减少人工提示工程的开销。

4. **融合策略的理论深化：** 当前的门控网络基于三维统计量（教师置信度、LLM置信度、IoU）进行决策。是否存在更优的融合统计量组合？例如，引入布局复杂度、文本密度等文档级特征是否能进一步提升门控的判别力？

## 原文 PDF

![[paperPDFs/CVPR_2026/LLM_Guided_Probabilistic_Fusion_for_Label_Efficient_Document_Layout_Analysis.pdf]]
