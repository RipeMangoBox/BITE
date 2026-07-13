---
title: "Medic-AD: Towards Medical Vision-Language Model's Clinical Intelligence"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/Medic_AD_Towards_Medical_Vision_Language_Model_s_Clinical_Intelligence.pdf
project_link: null
code_link: "https://github.com/AIDASLab/Medic-AD"
aliases:
- MA
- Medic-AD
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/benchmarks_datasets_evaluation
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: 三阶段递进训练框架：Stage 1 注入可学习<Ano>异常令牌建立病灶敏感表示；Stage 2 引入<Diff>差异令牌建模时序变化；Stage 3 通过专用热图解码头融合异常特征生成视觉证据。
primary_logic: 通过显式的异常感知令牌和差异令牌，将‘检测-比较-解释’的临床诊断思维嵌入VLM的学习课程，使模型不仅具备知识覆盖，更能产生与临床证据对齐的、可验证的决策依据。
claims:
- 在四个零样本医学异常检测数据集上，MEDIC-AD均取得最优平均F1（91.6），显著超越通用VLM和专有医学VLM。
- 在医学症状追踪基准MMXU上，MEDIC-AD取得最高综合得分（0.655），优于所有闭源基线和领域专用模型。
- 消融实验证明<Ano>令牌对时序推理至关重要：移除<Ano>后MMXU得分从0.655下降至0.635。
- Medical Zero-shot Anomaly Detection (Brain MRI, Head CT, Br35h, COVID-19) 上 Avg. F1 = 91.6
---

# Medic-AD: Towards Medical Vision-Language Model's Clinical Intelligence

> [!tip] 核心洞察
> 通过显式的异常感知令牌和差异令牌，将‘检测-比较-解释’的临床诊断思维嵌入VLM的学习课程，使模型不仅具备知识覆盖，更能产生与临床证据对齐的、可验证的决策依据。

| 字段 | 内容 |
|------|------|
| 中文题名 | Medic-AD：迈向医学视觉-语言模型的临床智能 |
| 英文题名 | Medic-AD: Towards Medical Vision-Language Model's Clinical Intelligence |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://openaccess.thecvf.com/content/CVPR2026/html/Park_Medic-AD_Towards_Medical_Vision-Language_Models_Clinical_Intelligence_CVPR_2026_paper.html) · [Code](https://github.com/AIDASLab/Medic-AD) |
| Topic | #topic/vision_multimodal_applications #topic/benchmarks_datasets_evaluation #topic/vision_multimodal_applications/image_and_video_generation |
| Method | MEDIC-AD |
| Dataset | Medical Zero-shot Anomaly Detection, Medical Symptom Tracking, Visual Grounding - BraTS2021, Real-world Clinical Dataset |

> [!tip] 效果简介
> - Medical Zero-shot Anomaly Detection (Brain MRI, Head CT, Br35h, COVID-19) 上，Avg. F1 91.6 vs next best (see Table 1) (outperforms all baselines)。
> - Medical Symptom Tracking (MMXU) 上，Overall accuracy 0.655 vs previous best (see Table 2) (outperforms all baselines)。
> - Visual Grounding - BraTS2021 (BMAD) 上，AUC / mIoU 99.8 / 87.6 vs Citrus-V (see Table 3) (outperforms Citrus-V)。

## 概要

当前医学视觉-语言模型（VLM）虽已积累广泛的医学知识，却普遍缺乏将知识转化为临床可操作输出的能力——它们难以稳定检测病灶、无法进行可靠的时序症状追踪，且推理过程缺乏透明的视觉解释。这一瓶颈的本质在于模型缺少显式的异常感知与差异比较机制，导致其输出难以与临床证据对齐。

针对上述问题，**MEDIC-AD** 提出一个三阶段递进训练框架，将“检测—比较—解释”的临床诊断思维嵌入VLM的学习课程。其核心思路是引入两类专用令牌：可学习的 **<Ano>异常令牌** 建立病灶敏感表示，以及 **<Diff>差异令牌** 建模时序变化，再通过专用热图解码头融合异常特征生成视觉证据。这一设计使模型不仅能覆盖知识，更能产出可验证的决策依据。

在四个零样本医学异常检测数据集上，MEDIC-AD 取得平均 F1 91.6 的最优结果（Table 1），显著超越通用VLM和专有医学VLM。在医学症状追踪基准 MMXU 上，其综合得分达 0.655（Table 2），同样优于所有闭源基线和领域专用模型。消融实验进一步证实 <Ano> 令牌对时序推理的关键作用：移除后 MMXU 得分从 0.655 下降至 0.635（Table 4）。在视觉定位（Table 3）和真实临床数据集（Table 5）上的评估亦一致表明，该方法在病灶检测、时序推理和视觉解释三个维度均具备实用优势。



### 医学视觉-语言模型的临床落地瓶颈

视觉-语言模型（VLM）在通用领域的突破推动了对医学多模态智能的探索。然而，当前医学VLM面临一个核心矛盾：**知识覆盖与临床可操作性之间的鸿沟**。尽管现有模型能够理解医学影像并生成文本描述，它们在真实临床工作流中暴露出三个系统性缺陷：

1. **病灶检测不稳定**：通用VLM缺乏对异常区域的显式感知机制，在零样本场景下难以可靠地判别图像中是否存在病变。
2. **时序推理缺失**：临床诊断通常需要对比多次检查影像以判断病情进展（恶化、改善或稳定），而现有模型仅简单拼接多张图像，无法建模图像间的时序动态关系。
3. **推理过程不透明**：模型输出的诊断结论缺乏可验证的视觉证据，难以获得临床医生的信任。

这些问题在医学领域尤为致命——临床决策需要**可追溯、可验证的证据链**，而非仅凭统计关联的“黑箱”输出。

### 现有方法的局限

当前医学VLM的改进路径主要沿两个方向展开：

- **通用VLM的医学适配**（如 **GPT-4o**（Hurst et al., arXiv 2024）、**Qwen2.5-VL**（Bai et al., arXiv 2023）、**InternVL2.5**）：通过指令微调注入医学知识，但未改变模型对视觉特征的利用方式，仍依赖标准视觉编码器提取的通用表示，缺乏对病灶区域的针对性敏感度。
- **医学专用VLM**（如 **Lingshu**（Xu et al., arXiv 2025）、**Citrus-V**（Wang et al., arXiv 2025））：在医学数据上进行预训练或微调，提升了领域知识覆盖，但同样未显式建模异常感知和时序推理能力。部分工作如 **AnomalyGPT**（Gu et al., AAAI 2024）和 **AnomalyMoE**（Xu et al., arXiv 2025）尝试解决异常检测问题，但缺乏与自然语言推理和视觉解释的深度整合。

这些方法的共同盲点是：**将“看见”等同于“诊断”**，忽略了临床诊断中“检测—比较—解释”的递进认知过程。

### 本文动机：将临床诊断思维嵌入VLM学习课程

本文的核心洞察是：要弥合知识覆盖与临床可操作性之间的鸿沟，关键在于**将临床医生的诊断思维显式编码进模型架构与训练范式**。具体而言，放射科医生的工作流程包含三个层次：

- **检测**：定位影像中的异常区域；
- **比较**：对比当前与历史影像，判断病灶的动态变化；
- **解释**：基于视觉证据给出可验证的诊断结论。

基于此，本文提出 **MEDIC-AD**，通过三阶段递进训练框架将上述临床思维嵌入VLM：Stage 1 注入可学习的 `<Ano>` 异常令牌以建立病灶敏感表示；Stage 2 引入 `<Diff>` 差异令牌以建模时序变化；Stage 3 通过专用热图解码头生成视觉证据。该设计使模型不仅具备医学知识覆盖，更能产生与临床证据对齐的、可验证的决策依据。



## 核心方法与创新机理

MEDIC-AD 的核心创新在于将“检测—比较—解释”的临床诊断思维显式嵌入视觉-语言模型的学习课程，通过三个紧密耦合的**changed slots**实现从知识覆盖到临床可操作输出的跨越。

**1. 异常感知表示：从通用视觉特征到病灶敏感表征**

现有医学VLM（如骨干模型 **Lingshu** (Xu et al., arXiv 2025)）缺乏专用异常令牌，仅依赖标准视觉特征，难以稳定检测病灶。MEDIC-AD 引入可学习的 `<Ano>` 异常令牌，通过交叉注意力与视觉软提示（Visual Soft Prompt Tuning）在多尺度中间层特征上进行交互，构建以病灶为中心的判别性表示。这一设计使模型在零样本异常检测中取得平均 F1 91.6（Table 1），显著超越通用VLM和专有医学VLM。

**2. 时序差异推理：从简单图像拼接到解耦时序动态**

基线方法（如 **GPT-4o** (Hurst et al., arXiv 2024)、**Qwen2.5-VL** (Bai et al., arXiv 2023)）通常简单拼接多张图像的视觉特征，无法可靠追踪症状的恶化、改善或稳定。MEDIC-AD 引入 `<Diff>` 差异令牌，通过 Diff Q-Former 对比两张图像的异常特征，显式编码时序变化并解耦疾病进展与无关外观改变。在医学症状追踪基准 MMXU 上，MEDIC-AD 以 0.655 综合得分超越所有闭源基线和领域专用模型（Table 2）。消融实验进一步证实，移除 `<Ano>` 令牌后 MMXU 得分降至 0.635（Table 4），表明异常感知是时序推理的必要前提。

**3. 视觉可解释性：从黑箱输出到可验证的视觉证据**

已有方法或缺乏视觉解释能力，或依赖外部解码器（如 SAM2）。MEDIC-AD 通过专用 ConvNeXt 热图解码头融合 `<Ano>` 令牌与中间视觉特征，直接生成病灶区域热图 $M$。这一内生解释机制使模型的推理过程与视觉证据对齐，在 BraTS2021 上达到 AUC 99.8 / mIoU 87.6（Table 3），为临床决策提供可验证的依据。

**4. 三阶段递进训练范式**

上述三个 changed slots 通过递进式训练课程实现耦合：Stage 1 训练异常处理器生成 `<Ano>` 令牌，建立病灶敏感表示；Stage 2 在此基础上通过 Diff Q-Former 生成 `<Diff>` 令牌，建模时序变化；Stage 3 融合异常特征训练热图解码头，生成视觉证据。这一递进设计确保各阶段能力相互增强而非独立训练，最终在真实临床数据集（300例患者）上以 GREEN 0.020 / RaTEScore 0.892 / GPT-eval 4.25 显著超越骨干模型 Lingshu（Table 5）。

**创新本质**：通过 `<Ano>` 和 `<Diff>` 两类显式令牌，MEDIC-AD 将临床诊断的认知流程转化为模型可学习的结构化表示，使 VLM 不仅具备知识覆盖，更能产生与临床证据对齐的、可验证的决策依据。



MEDIC-AD 采用三阶段递进训练框架，将“检测—比较—解释”的临床诊断思维显式嵌入视觉-语言模型的学习课程中。如图 Figure 3 所示，整个 pipeline 由五个核心模块串联构成，输入为单张或成对的医学影像，输出包括文本诊断响应和病灶区域热图。

![[assets/figures/papers/paper_list_l2062_https_openaccess_thecvf_com_content_CVPR2026_html_Park_Medic_AD_Towards/figures/003_Figure_3.jpg]]
*Figure 3: Architecture of MEDIC-AD. (a) Stage 1: \<Ano> Token Generation, (b) Stage 2: \<Diff> Token Generation, and (c) Stage 3: Heatmap Generation illustrate each stage of the proposed framework. Note that CA denotes Cross-Attention*

### 输入输出流

**单图场景（Stage 1 / Stage 3）**：输入医学影像 $\mathbf{I}$ 经视觉编码器提取多尺度特征 $\mathbf{V}$，通过视觉软提示进行异常幅度调制后得到增强特征 $\mathbf{V}^*$。异常处理器（Anomaly Processor）以 $\mathbf{V}^*$ 为输入，经由交叉注意力与 Q-Former 生成可学习的异常感知令牌 $<\mathrm{Ano}>$。大语言模型接收拼接后的多模态序列 $[f_p(\mathbf{V}^*); <\mathrm{Ano}>; \mathrm{Emb}(\mathbf{T})]$，生成文本响应 $\mathbf{R}$。在 Stage 3，热图解码器（ConvNeXt 分割头）融合投影视觉特征 $f_p(\mathbf{V}^*)$ 与聚合后的异常令牌 $\Sigma<\bar{\mathrm{Ano}}>$，生成病灶区域热图 $\mathbf{M}$。

**双图场景（Stage 2）**：输入两张时序医学影像 $\mathbf{I}_1, \mathbf{I}_2$（如既往与当前检查），分别经 Stage 1 的异常感知管线提取各自的 $<\mathrm{Ano}>$ 令牌与增强视觉特征 $\mathbf{V}_1^*, \mathbf{V}_2^*$。差异 Q-Former（Diff Q-Former）对比两张图像的异常特征，解耦时序进展与无关变化，生成差异令牌 $<\mathrm{Diff}>$。LLM 接收序列 $[f_p(\mathbf{V}_1^*); <\mathrm{Ano}>; f_p(\mathbf{V}_2^*); <\mathrm{Ano}>; \mathrm{Emb}(\mathbf{T}); <\mathrm{Diff}>]$，输出包含时序推理的文本响应。

### 模块关系与递进依赖

五个模块之间存在严格的递进依赖关系：

1. **视觉编码器与视觉软提示**：作为特征提取基础，选取视觉编码器中间 4 层输出进行多尺度特征融合与异常幅度调制，为后续所有阶段提供增强视觉表示 $\mathbf{V}^*$。
2. **异常处理器**：在 Stage 1 训练，通过可学习查询令牌与多尺度视觉特征的交叉注意力，产生病灶敏感的 $<\mathrm{Ano}>$ 令牌。该模块是 Stage 2 差异推理和 Stage 3 热图生成的先决条件。
3. **差异 Q-Former**：在 Stage 2 训练，依赖 Stage 1 冻结的异常处理器输出的 $<\mathrm{Ano}>$ 令牌，通过对比学习解耦两张图像间的临床相关变化，生成 $<\mathrm{Diff}>$ 令牌。
4. **热图解码器**：在 Stage 3 训练，直接融合 Stage 1 产生的 $<\mathrm{Ano}>$ 令牌与中间视觉特征，生成像素级病灶定位热图，为模型推理提供视觉证据。
5. **大语言模型**：作为统一的文本解码器，在各阶段接收包含 $<\mathrm{Ano}>$ 和/或 $<\mathrm{Diff}>$ 令牌的多模态嵌入序列，生成自然语言诊断响应。

### 训练范式

三阶段训练遵循递进式课程设计：Stage 1 在异常检测数据上训练异常处理器，建立病灶敏感表示；Stage 2 在时序对比数据上训练差异 Q-Former，赋予模型纵向推理能力；Stage 3 在像素级标注数据上训练热图解码器，实现视觉可解释性。各阶段冻结前序模块参数，仅训练当前阶段新增组件，保证了能力的稳定积累与模块间的解耦。

> **需人工核实**：关于各阶段训练数据的具体规模、损失函数权重配置以及优化器超参数，当前证据片段未提供详细数值，建议查阅原文实验配置章节进行补充。



MEDIC-AD 的核心架构围绕三个递进式模块展开，分别对应临床诊断中“检测—比较—解释”的思维链条。以下逐一阐述各模块的设计逻辑与关键公式。

### 标准VLM响应生成

作为起点，标准视觉-语言模型将视觉特征 $\mathbf{V}$ 经投影函数 $f_p(\cdot)$ 映射后，与文本指令的嵌入表示 $\mathrm{Emb}(\mathbf{T})$ 拼接，送入大语言模型 $f_l(\cdot)$ 生成响应 $\mathbf{R}$：

$$\mathbf{R} = f_l(\lceil f_p(\mathbf{V}); \mathrm{Emb}(\mathbf{T})\rceil)$$

该范式缺乏对病灶区域的显式建模，难以支撑精细的医学推理。

### 异常处理器与 `<Ano>` 令牌生成（Stage 1）

异常处理器是 MEDIC-AD 的第一个关键模块，旨在建立病灶敏感的视觉表示。其核心操作如下：
- 从视觉编码器的**中间4层**提取多尺度视觉特征，并通过视觉软提示（Visual Soft Prompt Tuning）进行异常幅度调制，得到增强特征 $\mathbf{V}^*$。
- 引入一组可学习的**异常查询令牌**，通过交叉注意力（Cross-Attention）与 $\mathbf{V}^*$ 交互，生成 `<Ano>` 令牌。这些令牌强制模型聚焦异常区域，形成以病灶为中心的判别性表示。

增强后的响应生成公式为：

$$\mathbf{R} = f_l([f_p(\mathbf{V}^*); <\mathrm{Ano}>; \mathrm{Emb}(\mathbf{T})])$$

其中 $<\mathrm{Ano}>$ 作为可学习令牌插入投影视觉特征与文本嵌入之间，使 LLM 在生成回答时直接感知异常语义。

### 差异 Q-Former 与 `<Diff>` 令牌生成（Stage 2）

时序推理要求模型对比当前影像与历史影像的病灶变化。MEDIC-AD 通过差异 Q-Former 实现这一能力：
- 将两张输入图像分别经 Stage 1 处理，得到各自的调制视觉特征 $\mathbf{V}_1^*$ 和 $\mathbf{V}_2^*$ 及对应的 $<\mathrm{Ano}>$ 令牌。
- 差异 Q-Former 接收两组异常特征，通过对比学习解耦时序进展与无关变化（如体位、光照差异），生成 $<\mathrm{Diff}>$ 差异令牌。该令牌显式编码疾病负担的恶化、改善或稳定状态。

时序令牌增强的响应生成公式为：

$$\mathbf{R} = f_l([f_p(\mathbf{V}_1^*); <\mathrm{Ano}>; f_p(\mathbf{V}_2^*); <\mathrm{Ano}>; \mathrm{Emb}(\mathbf{T}); <\mathrm{Diff}>])$$

消融实验证实，仅用 $<\mathrm{Diff}>$ 令牌而移除 $<\mathrm{Ano}>$ 时，MMXU 综合得分从 0.655 降至 0.635（Table 4），表明异常感知令牌对时序推理有显著贡献。

### 热图解码器与视觉解释生成（Stage 3）

为提供与推理一致的视觉证据，MEDIC-AD 引入专用的 ConvNeXt 分割头作为热图解码器 $f_h(\cdot)$：

$$\mathbf{M} = f_h([f_p(\mathbf{V}^*); \Sigma<\bar{\mathrm{Ano}}>])$$

其中 $\Sigma<\bar{\mathrm{Ano}}>$ 表示聚合后的异常令牌，与投影视觉特征 $f_p(\mathbf{V}^*)$ 融合，生成病灶区域热图 $\mathbf{M}$。该热图直接高亮模型推理所依据的异常区域，使决策过程可验证、可解释。

### 模块间的因果依赖

三个模块并非独立运作，而是形成递进依赖关系：Stage 1 的异常令牌为 Stage 2 的差异推理提供病灶敏感的表示基础；Stage 3 的热图生成又直接复用 Stage 1 产出的 `<Ano>` 令牌。这种设计将“检测—比较—解释”的临床诊断逻辑内化为模型的学习课程，使得每个阶段的能力建立在上一阶段的表征之上。



## 实验与关键发现

### 核心实验设计逻辑

MEDIC-AD 的实验体系严格对应其三阶段递进训练框架：Stage 1 的异常检测能力通过零样本异常检测基准验证；Stage 2 的时序差异推理通过多时间点症状追踪基准 MMXU 评估；Stage 3 的视觉可解释性通过视觉定位（visual grounding）基准和真实临床数据集上的报告质量来检验。这种“检测→比较→解释”的递进评测逻辑，直接呼应了论文提出的核心洞察——将临床诊断思维嵌入 VLM 的学习课程。

### 零样本医学异常检测

在四个完全未见的模态数据集上（Brain MRI、Head CT、Br35h、COVID-19），MEDIC-AD 取得了平均 F1 为 **91.6** 的最优结果（Table 1），显著超越所有基线。这一结果验证了 `<Ano>` 异常令牌的跨模态泛化能力——模型并非仅仅拟合训练数据的表层特征，而是学到了可迁移的“异常感知”表示。

![[assets/figures/papers/paper_list_l2062_https_openaccess_thecvf_com_content_CVPR2026_html_Park_Medic_AD_Towards/figures/004_Table_1.jpg]]
*Table 1: Results on Zero-shot Medical Anomaly Detection (Brain MRI [29], Head CT [31], Br35h [18], and COVID-19 [13]). For each dataset, we report Precision, Recall, and F1. The rightmost column shows the average F1 over all tasks*

从方法对比来看，通用 VLM（如 GPT-4o、Qwen2.5-VL、InternVL2.5）在此任务上表现明显不足，说明缺乏专用异常感知机制的模型难以稳定检测病灶。值得注意的是，即使与专门的异常检测方法 **AnomalyGPT**（Gu et al., AAAI 2024）和 **AnomalyMoE**（Xu et al., arXiv 2025）相比，MEDIC-AD 仍保持优势，这表明 `<Ano>` 令牌的设计比依赖外部模型或 MoE 路由的方案更为有效。

**Table 1 关键结论**：MEDIC-AD 在四个数据集上的 F1 均居首位，且平均 F1 领先幅度具有说服力。该表的置信度为 0.95，结论可靠。

### 医学症状追踪（MMXU 基准）

MMXU 基准专门评估模型在多时间点医学影像中追踪症状变化的能力，是检验 Stage 2 差异推理的核心场景。MEDIC-AD 取得了最高综合得分 **0.655**（Table 2），优于所有闭源基线（如 GPT-4o）和领域专用模型（如 Lingshu、Citrus-V）。

![[assets/figures/papers/paper_list_l2062_https_openaccess_thecvf_com_content_CVPR2026_html_Park_Medic_AD_Towards/figures/005_Table_2.jpg]]
*Table 2: Results on MMXU [42]. Models are categorized into general-purpose, closed-source, and medical-domain VLMs*

这一结果的关键机制在于 `<Diff>` 差异令牌的设计：不同于基线模型简单拼接多张图像特征的做法，MEDIC-AD 通过 Diff Q-Former 显式对比两张图像的异常特征，将时序变化解耦为“恶化、改善、稳定”等临床相关维度。这解释了为何 MEDIC-AD 在需要精细时序推理的子任务上表现尤为突出。

**Table 2 关键结论**：MEDIC-AD 的综合得分 0.655 为所有模型中最高，且分类对比显示其在医学域 VLM 中具有明显优势。置信度 0.95。

### 视觉定位与可解释性

Stage 3 的热图生成能力通过 BMAD（含 BraTS2021、RESC、BTCV+LiTs）和 ChestX-Det 数据集评估。MEDIC-AD 在所有数据集上均超越 **Citrus-V**（Wang et al., arXiv 2025），其中 BraTS2021 上 AUC 达到 **99.8**，mIoU 达到 **87.6**（Table 3）。

![[assets/figures/papers/paper_list_l2062_https_openaccess_thecvf_com_content_CVPR2026_html_Park_Medic_AD_Towards/figures/006_Table_3.jpg]]
*Table 3: Visual grounding performance on BMAD [7] (BraTS2021 [5], RESC [20], BTCV + LiTs [9, 32]) and ChestX-Det [39] datasets. Each dataset reports AUC and mIoU metrics (higher is better)*

这一结果验证了将 `<Ano>` 异常令牌与 ConvNeXt 分割头融合的设计有效性——模型生成的病灶热图不仅定位准确，而且与模型的推理过程保持一致。定性对比（Figure 4）进一步显示，MEDIC-AD 在正常样本上不会产生虚假热图，而 Citrus-V 存在一定的假阳性激活，说明 `<Ano>` 令牌有助于抑制对非病灶区域的错误响应。

![[assets/figures/papers/paper_list_l2062_https_openaccess_thecvf_com_content_CVPR2026_html_Park_Medic_AD_Towards/figures/007_Figure_4.jpg]]
*Figure 4: Visual Grounding comparison between MEDIC-AD and Citrus-V [53] on diverse abnormal and normal samples*

**Table 3 关键结论**：MEDIC-AD 在 AUC 和 mIoU 两个指标上全面超越 Citrus-V，尤其在 BraTS2021 上优势明显。置信度 0.95。

### 消融实验：`<Ano>` 令牌的关键作用

消融实验（Table 4）揭示了 `<Ano>` 令牌对时序推理的因果贡献：当仅使用 `<Diff>` 令牌而移除 `<Ano>` 时，MMXU 综合得分从 0.655 下降至 **0.635**。这一 0.02 的降幅虽看似不大，但在 MMXU 的评测尺度上具有统计意义——它表明异常感知表示是差异推理的前提：模型需要先“看到”病灶，才能有效“比较”病灶的变化。

![[assets/figures/papers/paper_list_l2062_https_openaccess_thecvf_com_content_CVPR2026_html_Park_Medic_AD_Towards/figures/009_Table_4.jpg]]
*Table 4: Effect of utilizing \<Ano> tokens and comparison of visual feature extraction strategies*

此外，视觉特征提取策略的对比表明，使用中间 4 层视觉特征（而非仅最后层）可同时优化异常检测和时序推理性能（Avg. F1 91.6，MMXU 0.635）。论文分析指出，异常幅度调制（anomaly-aware magnitude modulation）增强了视觉嵌入的表达力，使 `<Diff>` 令牌能捕获临床相关的变化而非全局外观改变。

**Table 4 关键结论**：`<Ano>` 令牌对时序推理有显著贡献；中间 4 层特征提取策略在两个任务上均为最优。置信度 0.95。

### 真实临床数据集验证

在包含 300 名患者的真实纵向临床数据集上（Table 5），MEDIC-AD 在 GREEN（0.020）、RaTEScore（0.892）和 GPT-4o 评估（4.25）三个指标上均优于骨干模型 **Lingshu-7B**（Xu et al., arXiv 2025）。这一结果增强了方法的外部效度——证明三阶段训练带来的增益不仅在学术基准上成立，在模拟真实放射科工作流程的场景中同样有效。

![[assets/figures/papers/paper_list_l2062_https_openaccess_thecvf_com_content_CVPR2026_html_Park_Medic_AD_Towards/figures/008_Table_5.jpg]]
*Table 5: Evaluation on a real-world clinical dataset of 300 patients using GREEN [43], RaTEScore [64], and GPT-4o evaluation*

### 超参数敏感性分析

Figure 5 展示了查询令牌池化大小和视觉软提示数量对性能的影响。红色虚线标注了 Lingshu 基线的性能水平，MEDIC-AD 在广泛的超参数范围内均保持对基线的优势，表明方法对超参数选择具有较好的鲁棒性。

![[assets/figures/papers/paper_list_l2062_https_openaccess_thecvf_com_content_CVPR2026_html_Park_Medic_AD_Towards/figures/010_Figure_5.jpg]]
*Figure 5: Hyperparameter sensitivity analysis on (a) query token pooling size and (b) visual soft prompt counts. The red line denotes the baseline performance of Lingshu [59]*

### 失败模式与局限性

尽管整体结果强劲，仍需注意以下局限：

1. **模态覆盖有限**：当前验证集中于脑 MRI、头部 CT、胸部 X 光，尚未覆盖超声、病理等模态。在这些模态上 `<Ano>` 令牌是否同样有效需要进一步验证。
2. **罕见病变泛化**：训练数据的像素级分割掩码规模和质量可能限制模型对罕见病变的检测能力——这是需要手动验证的风险点。
3. **热图临床可接受性未验证**：虽然视觉定位指标优秀，但热图与放射科医生判读的一致性尚未经过大规模用户研究或临床试验检验。
4. **骨干模型知识偏差**：MEDIC-AD 基于 Lingshu 构建，其内部知识偏差可能影响输出可靠性；未经强化学习对齐的部分可能产生不准确的文本描述。

### 补充图表

![[assets/figures/papers/paper_list_l2062_https_openaccess_thecvf_com_content_CVPR2026_html_Park_Medic_AD_Towards/figures/001_Figure_1.jpg]]
*Figure 1: Overall performance of VLMs on Medical Anomaly Detection and Medical Symptom Tracking (MMXU [42])*

![[assets/figures/papers/paper_list_l2062_https_openaccess_thecvf_com_content_CVPR2026_html_Park_Medic_AD_Towards/figures/002_Figure_2.jpg]]
*Figure 2: Comparison of VLMs on clinical applications. Medic-AD provides stronger lesion detection, temporal reasoning, and visual grounding than GPT-4o [24] and Citrus-V [53]*



## 定位与知识库关联

### 1. 问题定位：从知识覆盖到临床可操作性

当前医学视觉-语言模型（VLM）的核心瓶颈并非知识广度不足，而是缺乏将广泛医学知识转化为临床可操作输出的机制。通用VLM（如 **GPT-4o** (Hurst et al., arXiv 2024)、**Qwen2.5-VL** (Bai et al., arXiv 2023)、**InternVL2.5**）虽在多模态理解上表现强劲，但在医学场景中暴露出三个系统性缺陷：无法稳定检测病灶、缺少可靠的时序症状追踪能力、以及推理过程缺乏透明的视觉解释。即使是专为医学设计的VLM（如 **Lingshu** (Xu et al., arXiv 2025)，作为MEDIC-AD的骨干模型），其训练范式仍停留在单阶段医学指令微调，未能显式建模临床诊断中“检测-比较-解释”的递进思维链。

MEDIC-AD的核心洞察在于：通过显式的异常感知令牌（`<Ano>`）和差异令牌（`<Diff>`），将临床诊断思维嵌入VLM的学习课程，使模型不仅具备知识覆盖，更能产生与临床证据对齐的、可验证的决策依据。

### 2. 在方法谱系中的位置

#### 2.1 与通用VLM的关系

通用VLM采用标准的多模态序列建模方式，将视觉特征经投影后与文本嵌入拼接，由大语言模型生成响应：

$$\mathbf{R} = f_l(\lceil f_p(\mathbf{V}); \mathrm{Emb}(\mathbf{T})\rceil)$$

这类模型在医学异常检测中缺乏对病灶区域的显式注意力引导，在时序比较中仅简单拼接多张图像特征，无法解耦临床相关变化与无关的全局外观改变。MEDIC-AD通过三个关键改造突破了这一局限：

- **异常感知表示**：注入可学习 `<Ano>` 令牌，通过交叉注意力与视觉软提示（Visual Soft Prompt）增强多尺度视觉特征，建立病灶敏感的判别表示；
- **时序差异推理**：引入 `<Diff>` 差异令牌，通过Diff Q-Former对比两张图像的异常特征，解耦疾病进展与无关变化；
- **视觉可解释性**：融合 `<Ano>` 令牌的ConvNeXt热图解码器，直接生成病灶区域热图，提供与推理一致的视觉证据。

相应地，MEDIC-AD的响应生成公式演化为两阶段增强形式。单图推理时：

$$\mathbf{R} = f_l([f_p(\mathbf{V}^*); <\mathrm{Ano}>; \mathrm{Emb}(\mathbf{T})])$$

双图时序推理时：

$$\mathbf{R} = f_l([f_p(\mathbf{V}_1^*); <\mathrm{Ano}>; f_p(\mathbf{V}_2^*); <\mathrm{Ano}>; \mathrm{Emb}(\mathbf{T}); <\mathrm{Diff}>])$$

热图生成则独立于文本解码：

$$\mathbf{M} = f_h([f_p(\mathbf{V}^*); \Sigma<\bar{\mathrm{Ano}}>])$$

#### 2.2 与医学专用VLM的关系

MEDIC-AD以 **Lingshu** (Xu et al., arXiv 2025) 为骨干模型，在保持其医学知识覆盖的基础上进行结构性扩展。Lingshu作为医学基础VLM，提供了经过医学语料预训练的语言能力和视觉编码器，但缺乏对异常区域的显式建模和时序推理的专用机制。MEDIC-AD在其上叠加了三阶段递进训练框架：

- **Stage 1**：训练异常处理器（Anomaly Processor），通过交叉注意力生成 `<Ano>` 令牌；
- **Stage 2**：训练Diff Q-Former，对比两张图像的异常特征生成 `<Diff>` 令牌；
- **Stage 3**：训练ConvNeXt热图解码器，融合 `<Ano>` 令牌与中间视觉特征生成病灶热图。

**Citrus-V** (Wang et al., arXiv 2025) 是另一医学VLM基线，具备统一视觉定位能力，但在视觉定位精度上被MEDIC-AD显著超越（BraTS2021上AUC 99.8 vs. Citrus-V的更低值，mIoU 87.6 vs. 更低值）。

#### 2.3 与异常检测专用方法的关系

**AnomalyGPT** (Gu et al., AAAI 2024) 和 **AnomalyMoE** (Xu et al., arXiv 2025) 是零样本异常检测与推理的专用基线。这些方法聚焦于工业或通用场景的异常检测，缺乏医学影像所需的时序推理和视觉解释能力。MEDIC-AD在四个零样本医学异常检测数据集（Brain MRI、Head CT、Br35h、COVID-19）上取得平均F1 91.6，显著超越这些专用基线，验证了医学场景专用设计的必要性。

### 3. 适用边界与局限

#### 3.1 已验证的适用场景

MEDIC-AD的有效性已在以下场景得到验证：

- **零样本医学异常检测**：在完全未见的模态数据集上，模型展现出跨模态的异常判别能力；
- **医学症状追踪**：在MMXU基准上，模型能区分疾病负担的恶化、改善和稳定；
- **视觉定位**：在BMAD和ChestX-Det数据集上，模型能生成与临床病灶对齐的热图；
- **真实临床工作流**：基于300名患者的纵向临床数据集评估，模型在GREEN、RaTEScore和GPT-4o评估三项指标上均优于骨干模型Lingshu。

#### 3.2 已知局限

1. **模态覆盖不足**：当前验证集中于脑MRI、头部CT、胸部X光等模态，尚未覆盖超声、病理等更广泛的医学影像类型。模型在这些模态上的泛化能力未经检验。

2. **数据依赖**：训练数据集的规模和标注质量（尤其是像素级分割掩码）可能限制模型在罕见病变上的泛化能力。热图解码头依赖于分割标注，而医学影像的像素级标注成本极高。

3. **临床验证缺失**：热图解释的临床可接受性和与放射科医生判读的一致性尚未经过大规模用户研究或临床试验验证。当前评估主要基于自动化指标，缺乏人类专家的系统评估。

4. **骨干模型偏差**：模型基于Lingshu骨干，其内部知识偏差可能影响输出的可靠性。未经强化学习对齐的部分可能产生不准确的文本描述，在临床高风险场景中构成安全隐患。

### 4. 开放问题

1. **维度扩展**：如何将异常令牌和差异令牌机制扩展到3D医学影像（如CT容积）或视频（如超声动态）？当前设计依赖2D视觉编码器，直接扩展到3D/视频模态需要重新设计令牌交互机制。

2. **令牌语义可解释性**：`<Ano>` 和 `<Diff>` 令牌的语义可解释性如何？能否将学到的令牌直接解码为可读的临床概念（如“肿块增大”、“水肿消退”），而非仅作为隐式特征？这关系到模型输出的临床可信度。

3. **鲁棒性与安全性**：在真实临床部署中，模型的鲁棒性、安全性和对分布外数据的拒绝能力如何保证？当前评估均在受控数据集上进行，缺乏对对抗样本、罕见病例、低质量影像等边缘情况的系统测试。

4. **人类反馈对齐**：是否可以通过强化学习利用临床反馈信号进一步对齐模型输出与医生决策？三阶段训练当前基于监督学习，引入RLHF或类似的临床偏好优化可能进一步提升输出的临床可接受性。



## 原文 PDF

![[paperPDFs/CVPR_2026/Medic_AD_Towards_Medical_Vision_Language_Model_s_Clinical_Intelligence.pdf]]
