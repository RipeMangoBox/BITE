---
title: "Common Corpus: The Largest Collection of Ethical Data for LLM Pre-Training"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/Common_Corpus_The_Largest_Collection_of_Ethical_Data_for_LLM_Pre_Training.pdf
openreview_forum_id: 0wSlFpMsGb
aliases:
- CC
- CCLCEDLPT
tags:
- ICLR_2026
- topic/representation_self_supervised_transfer
- topic/representation_self_supervised_transfer/representation_learning
core_operator: "通过系統性地收集、整理和清洗仅包含公共领域或宽松许可协议的跨领域多语言数据，构建一个规模达2万亿token的全开放预训练语料库。"
primary_logic: "在严格遵循数据合规与伦理要求的前提下，仍可构建出具有竞争力的大规模预训练数据集；基于该数据集训练的小模型在多项多语言基准上能达到与同等规模主流模型相当的性能，证明了开放数据的可行性。"
claims:
- "Common Corpus是目前最大的开放LLM预训练数据集，包含约2万亿token。"
- "使用Common Corpus训练的两个小语言模型（350M和1.2B）在MultiBLiMP、XStoryCloze等基准上表现与同类模型相当。"
- "Common Corpus涵盖六大数据集（Open Government, Open Culture, Open Science, Open Web, Open Code, Open Semantic），语言种类超过50种。"
- "Common Corpus完全避免了法律纠纷，是唯一同时满足多领域、多语言、非网页爬取及完全许可的预训练数据集。"
---

# Common Corpus: The Largest Collection of Ethical Data for LLM Pre-Training

> [!tip] 核心洞察
> 在严格遵循数据合规与伦理要求的前提下，仍可构建出具有竞争力的大规模预训练数据集；基于该数据集训练的小模型在多项多语言基准上能达到与同等规模主流模型相当的性能，证明了开放数据的可行性。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | Common Corpus：面向大语言模型预训练的最大伦理数据集 |
| 英文题名 | Common Corpus: The Largest Collection of Ethical Data for LLM Pre-Training |
| 会议/期刊 | ICLR 2026 (Oral) |
| Links | [paper](https://openreview.net/forum?id=0wSlFpMsGb); [Project](https://hf.co/datasets/PleIAs/common_corpus) |
| Topic | #topic/representation_self_supervised_transfer #topic/representation_self_supervised_transfer/representation_learning |
| Method | Common Corpus |
| Dataset | MultiBLiMP (aggregated) |

> [!tip] 效果简介
> - MultiBLiMP (aggregated) 上，accuracy 为 0.774 (PleIAs 350M)，对比 0.711 (XGLM 564M) / 0.683 (BLOOM 560M)，变化 +0.063 / +0.091。
> - MultiBLiMP (aggregated) 上，accuracy 为 0.797 (PleIAs 1.2B)，对比 0.799 (Gemma 3 1B)，变化 -0.002。

## 概述

当前大语言模型预训练数据集普遍包含大量受版权保护或未获明确许可的内容，由此引发的法律风险日益突出；同时，主流开放数据集往往覆盖领域单一、语种集中在英语，难以同时满足合规性与多样性的双重需求。针对这一瓶颈，Common Corpus 通过系统性地收集、整理和清洗仅包含公共领域或宽松许可协议的跨领域多语言数据，构建了一个规模约 2 万亿 token 的全开放预训练语料库。

其核心洞察在于：在严格遵循数据合规与伦理要求的前提下，仍可构建出具有竞争力的大规模预训练数据集。基于 Common Corpus 训练的两个小语言模型（PleIAs 350M 和 1.2B）在 MultiBLiMP、XStoryCloze 等多语言基准上表现与同等规模主流模型相当——PleIAs 350M 在 MultiBLiMP 上取得 0.774 的准确率，显著优于更大规模的 XGLM 564M（0.711）和 BLOOM 560M（0.683）——证明了开放数据路线的可行性。

在方法定位上，Common Corpus 是目前唯一同时满足“多领域、非网页爬取、多语言、完全许可”四项标准的预训练数据集（Table 1）。它涵盖政府文档、文化遗产、科学文献、代码、开放网络和语义数据六大领域，支持 50 余种语言，并配套开发了专用工具链（Segmentext 文本分割、OCRerrcr/OCRonos OCR 纠错、Celadon 毒性过滤等）进行数据治理。与 KL3M（仅限英语行政文本）、Dolma（多领域但以英语为主且非完全许可）、C4 和 ROOTS（网页爬取、混合许可）等现有数据集相比，Common Corpus 在许可合规性和来源多样性上形成了根本性差异化。

## 背景与动机

大语言模型（LLM）的预训练数据集正面临日益严峻的法律与伦理挑战。当前主流数据集——如 **C4**（Raffel et al., 2020）、**ROOTS**（Laurençon et al., 2022）、**Dolma**（Soldaini et al., 2024）和 **FineWeb 2**（Penedo et al., 2025）——在构建过程中普遍依赖大规模网页爬取，其中包含大量受版权保护或未获明确许可的内容。这种“合理使用”（fair use）的辩护路径正受到越来越多的法律审视，使得基于此类数据训练的模型面临不可忽视的合规风险。

与此同时，现有开放数据集在覆盖面上存在结构性缺口。**KL3M**（Bommarito et al., 2025）虽采用宽松许可数据，但局限于英文行政文本；**Common Pile**（Kandpal et al., 2025）同样遵循许可合规原则，却仅覆盖英语。多语言数据集的代表如 **DCAD 2000**（Shen et al., 2025）和 **ROOTS** 虽扩展了语种范围，但其许可状态参差不齐，无法同时满足“多领域、非网页爬取、多语言、完全许可”四项标准（见 Table 1）。这一系统性的数据集缺口构成了一个关键瓶颈：**在严格遵循数据合规与伦理要求的前提下，能否构建出兼具规模、多样性和竞争力的预训练语料库？**

Common Corpus 正是针对这一瓶颈的系统性回应。其核心动机是证明：通过系统性地收集、整理和清洗仅包含公共领域或宽松许可协议（如 CC-By、MIT、Apache-2.0）的跨领域多语言数据，可以构建一个规模达约 2 万亿 token 的全开放预训练语料库，且基于该数据集训练的小模型能够在多项多语言基准上达到与同等规模主流模型相当的性能。

## 核心创新

Common Corpus 的核心创新不在于提出新的模型架构或训练算法，而在于**重新定义了大规模预训练数据集的可构建边界**——它证明了在严格遵循数据合规与伦理要求的前提下，仍能构建出规模达 2 万亿 token、覆盖 50+ 语言和六大专业领域的全开放预训练语料库。

### 从“合理使用”到“完全许可”的范式转换

现有主流预训练数据集普遍依赖“合理使用”（fair use）条款，包含大量未经明确许可的受版权保护内容，法律风险日益增大。Common Corpus 实现了根本性的许可策略转换：**仅纳入公共领域或持有宽松许可证（如 CC-By、MIT、Apache-2.0）的数据**，从源头消除了版权纠纷隐患。

这一转换的可行性并非显而易见。如表 1 所示，在同期数据集中，Common Corpus 是**唯一同时满足多领域、非网页爬取、多语言和完全许可四项标准的数据集**。KL3M（Bommarito et al., 2025）虽满足许可要求，但局限于英语行政文本；Common Pile（Kandpal et al., 2025）同样采用许可数据，却仅覆盖英语；Dolma（Soldaini et al., 2024）和 ROOTS（Laurençon et al., 2022）虽具多语言优势，却无法保证数据许可的完全合规。Common Corpus 在四个维度上均达到“是”，构成了其独特的定位。

### 六大领域体系化覆盖：超越网页爬取

Common Corpus 的第二个关键创新在于**数据来源的体系化多样性**。传统预训练数据集以网页爬取为核心，内容类型单一且质量不可控。Common Corpus 则构建了六大子集（Figure 1）：

- **Open Government**：政府公开文档，包含金融（SEC 等）和法律（USPTO、EUR-lex 等）两大子领域
- **Open Culture**：文化遗产数字化内容，涵盖 18-19 世纪乃至更早的历史文献
- **Open Science**：基于 OpenAlex 筛选的 CC-By/CC0/CC-By-SA 学术文献
- **Open Web**：经许可识别的开放网络档案
- **Open Code**：开源代码，涵盖 Java、JavaScript、Python 等主流编程语言
- **Open Semantic**：结构化语义数据

Figure 3b 的 t-SNE 可视化证实了这一多样性的实际效果：Common Corpus 各子集在语义空间中与 C4、FineWeb 等爬取数据集形成明显分离，且与 FineWeb 的 top 1000 域名重叠率不到 1%，说明其贡献的是**实质性不同的增量内容**，而非现有数据集的简单重组。

### 面向异构数据的专用治理工具链

许可合规和多源异构数据的引入带来了新的技术挑战：历史文献的 OCR 质量参差不齐、多语言文本需要精准分割、毒性内容需跨语言过滤。Common Corpus 为此开发了一套**专用数据治理工具链**，构成其第三项核心创新：

- **Segmentext**：专用文本分割语言模型，将原始文档切分为连贯段落，解决 PDF 等非结构化文档的段落边界识别问题
- **OCRoscope + OCRerrcr**：双管道 OCR 质量检测。OCRoscope 基于 cld2 的 7-gram 语言检测评估文档数字化质量；OCRerrcr 是 400M 参数的 DeBERTa-v3 风格模型，专门标注 OCR 误差
- **OCRonos**：基于 Llama 3 8B 微调的 OCR 纠错生成模型，修复数字化文本中的错误
- **Celadon**：多语言毒性分类器（DeBERTa-v3-small，约 140M 参数），在 200 万合成标注样本上从头训练
- **Presidio + 自定义正则**：PII 信息识别与替换，通过自定义正则将电话号码等敏感信息的识别率从基础设置的 55-60% 提升至 85%

这套工具链并非简单复用现有方法，而是针对“公共领域/许可数据”这一特定场景的**系统化工程创新**，使异构、非完美的开放数据达到了可用于 LLM 预训练的质量标准。

### 创新验证：小模型的竞争力

Common Corpus 的创新价值最终通过模型训练得到验证。基于该数据集训练的 PleIAs 350M 模型在 MultiBLiMP 多语言基准上达到 0.774，**显著优于更大规模的 XGLM 564M（0.711）和 BLOOM 560M（0.683）**；PleIAs 1.2B 达到 0.797，与 Gemma 3 1B（0.799）基本持平（Table 2）。这一结果表明：**完全合规的数据集并非性能的妥协品**，在同等参数规模下，精心策划的开放数据可以匹配甚至超越基于混合许可数据训练的模型。

## 整体框架

![[assets/figures/papers/paper_list_l27_https_openreview_net_forum_id_0wSlFpMsGb/figures/005_Table_1.jpg]]
*Table 1: Comparison of the contemporary datasets for LLM training*

![[assets/figures/papers/paper_list_l27_https_openreview_net_forum_id_0wSlFpMsGb/figures/008_Table_3.jpg]]
*Table 3: In Table 3, we present the token, word, and document counts for the Common Corpus collections. Table 3: Dataset composition of Common Corpus. For each collection, we report the total number of documents, words (whitespace-separated), and tokens*

![[assets/figures/papers/paper_list_l27_https_openreview_net_forum_id_0wSlFpMsGb/figures/001_Figure_1.jpg]]
*Figure 1: Proportional treemap of Common Corpus collections and their most popular languages*

![[assets/figures/papers/paper_list_l27_https_openreview_net_forum_id_0wSlFpMsGb/figures/004_Figure_3.jpg]]
*Figure 3: (b) A two-component t-SNE visualization of subsets of Common Corpus collections, C4, and FineWeb. Figure 3: Temporal and semantic overview of the Common Corpus collections*

Common Corpus 的构建遵循一条以**数据许可合规**为刚性约束、以**多领域多语言覆盖**为扩展目标的系统性数据工程流水线。其核心瓶颈在于：当前主流预训练数据集（如 **C4** (Raffel et al., 2020)、**ROOTS** (Laurençon et al., 2022)、**Dolma** (Soldaini et al., 2024)、**FineWeb 2** (Penedo et al., 2025)）普遍依赖网页爬取，数据许可状态混杂，面临日益增长的法律风险；同时，现有开放数据集如 **KL3M** (Bommarito et al., 2025) 虽满足许可要求，但局限于英语行政文本，领域和语言覆盖严重不足。Common Corpus 通过系统性地收集、整理和清洗仅包含公共领域或宽松许可协议（如 CC-By、MIT）的跨领域多语言数据，构建了规模达约 2 万亿 token 的全开放预训练语料库，在合规性与多样性之间建立了新的因果调节节点。

### 数据集整体构成

Common Corpus 由六大子集构成，覆盖从政府文档到代码的多元领域，总计约 517M 文档、1.09T 词、2T token（Table 3）。各子集的领域定位与规模如下：

| 子集 | 领域定位 | 文档数 | Token 数 |
|------|----------|--------|----------|
| **Open Government** | 政府与法律文书 | 约 32M | 约 580B |
| **Open Culture** | 文化遗产与历史文献 | 约 420M | 约 330B |
| **Open Science** | 开放获取学术论文 | 约 40M | 约 220B |
| **Open Web** | 许可合规的网页档案 | 约 21M | 约 500B |
| **Open Code** | 开源代码仓库 | 约 3.5M | 约 200B |
| **Open Semantic** | 结构化知识图谱 | 约 0.5M | 约 170B |

*注：以上数值为基于 Table 3 的近似量级，精确数字请参见原表。*

Figure 1 以树图形式展示了六大子集的相对规模及主要语言分布，Figure 2 则以世界地图形式呈现了 Common Corpus 中语言的全球地理分布（对数尺度的文档计数）。

### 数据收集与许可验证流水线

Common Corpus 的数据收集遵循一条**许可优先**的筛选流水线：

1. **来源甄别**：针对六大领域分别确定数据源头。例如，Open Government 整合了 SEC、WTO、EUR-lex 等机构的公开文档（Table 6, Table 7）；Open Science 基于 OpenAlex 数据库，仅保留 CC-By、Public Domain/CC0 和 CC-By-SA 许可的论文；Open Code 从 GitHub 等平台收集 MIT、Apache 等宽松许可的项目（Table 10 展示了编程语言的 token 分布，Java 以约 35.7B token 居首，其次为 JavaScript 约 28.9B、Python 约 26.7B）。

2. **许可验证**：对每份数据对象标注许可证、语言、领域等元数据，确保可追溯与可筛选。对于文化遗产类内容，当无法依赖文化机构的保证时，实施了内部权利验证流程。Table 4 列出了 Common Corpus 中最常用的十种许可证及其 token 数量。

3. **格式与语言初筛**：通过文件扩展名过滤非目标语言和格式的文件，并应用 Lozhkov et al. (2024) 的手动过滤规则去除低质量数据，同时移除数字占比超过 75% 的文件。

### 数据清洗与策展工具链

收集后的原始数据需经过一套专用工具链进行深度清洗，以解决历史文本的 OCR 质量问题、个人身份信息（PII）泄露风险以及有害内容过滤等挑战：

| 工具/模块 | 功能 | 技术实现 |
|-----------|------|----------|
| **Segmentext** | 文本分割，将原始文档切分为连贯段落 | 专用语言模型 |
| **OCRoscope** | OCR 质量检测，通过 7-gram 语言识别评估文档数字化质量 | 基于 cld2 |
| **OCRerrcr** | OCR 错误检测，标注数字化文本中的误差 | DeBERTa-v3 风格模型（400M 参数） |
| **OCRonos** | OCR 纠错生成，修复数字化文本中的错误 | 基于 Llama 3 8B 微调 |
| **Presidio** | PII 信息识别与替换，将个人身份信息替换为虚构值 | 微软开源工具 + 自定义正则（将电话号码识别准确率从 55-60% 提升至 85%） |
| **Celadon** | 多语言毒性分类，过滤有害内容 | DeBERTa-v3-small（约 140M 参数），在 2M 合成标注样本上从头训练 |
| **去重** | 基于 PDF 元数据和来源的文档级去重 | 元数据比对 |

Figure 4 展示了在 300,000 文档样本上的定性评估分布，验证了清洗流水线的整体效果。

### 与其他数据集的定位差异

Table 1 从四个维度对比了 Common Corpus 与当代主流预训练数据集：**多领域**、**超越网页爬取**、**多语言**、**许可数据**。Common Corpus 是唯一同时满足全部四项标准的数据集。Figure 3b 的 t-SNE 可视化进一步表明，Common Corpus 的子集在语义空间上与 C4 和 FineWeb 等网页爬取语料库显著分离——Common Corpus 与 FineWeb 的前 1000 域名重叠不足 1%，页面重叠不足 2%，证实其提供了差异化的增量内容。

### 流水线输出与下游验证

最终产出的 Common Corpus 被用于预训练两个小规模语言模型：PleIAs 350M 和 PleIAs 1.2B。在 MultiBLiMP 多语言基准上，PleIAs 350M 达到 0.774，优于参数量更大的 XGLM 564M（0.711）和 BLOOM 560M（0.683）；PleIAs 1.2B 达到 0.797，与 Gemma 3 1B（0.799）相当（Table 2）。这一结果验证了核心洞察：在严格遵循数据合规与伦理要求的前提下，仍可构建出具有竞争力的大规模预训练数据集。

### 已知局限

需注意，当前 Common Corpus 的规模仅足以训练小模型，尚不支持大规模模型的预训练；英语仍占 token 总量的绝对主导地位（约 969B token，是法语 275B 的 3.5 倍、德语 112B 的 8.6 倍，见 Table 5），多语言平衡性仍有改善空间；OCR 纠错和质量过滤无法达到 100% 准确率，部分数字化文本可能残留错误。

## 核心模块与公式推导

Common Corpus 的核心贡献在于其数据治理与处理流水线，而非算法或模型架构的创新。该流水线由一系列专用工具模块构成，旨在解决开放数据（尤其是历史文档）在文本分割、OCR质量、毒性过滤及隐私保护方面的固有问题。

### 数据处理流水线模块

**1. 文本分割：Segmentext**
原始文档（如PDF）常包含多栏、页眉页脚等非连续文本结构。团队开发了专用语言模型 **Segmentext**，将原始文档切分为语义连贯的段落，作为后续处理的基本单元。

**2. OCR质量检测：OCRoscope 与 OCRerrcr**
历史文献数字化文本普遍存在OCR错误。流水线采用双阶段检测：
- **OCRoscope**：基于语言识别工具 cld2，通过7-gram语言检测评估文档的数字化质量。
- **OCRerrcr**：一个 400M 参数的 DeBERTa-v3 风格语言模型，专门标注文本中的OCR误差位置。

**3. OCR纠错：OCRonos**
在检测到错误后，使用基于 **Llama 3 8B** 微调的生成模型 **OCRonos** 对数字化文本进行修复，纠正字符识别错误。

**4. 毒性过滤：Celadon**
为确保数据伦理安全，团队从零训练了一个多语言毒性分类器 **Celadon**。该模型基于 DeBERTa-v3-small 架构（约140M参数），在200万条合成标注样本上训练，用于过滤预训练数据中的有害内容。

**5. 个人身份信息（PII）移除：Presidio**
使用微软开源的 **Presidio** 工具识别并替换文本中的PII为虚构值。基础设置下对电话号码的识别准确率为55-60%，通过添加自定义正则表达式后提升至85%。

**6. 去重**
基于PDF元数据和文档来源进行文档级去重，避免重复数据污染训练集。

### 公式推导

本文未提出新的理论公式或数学推导。其核心方法为工程化的数据处理流水线，不涉及需要推导的算法公式。

## 实验与分析

### 主实验：PleIAs 模型的多语言基准表现

作者基于 Common Corpus 预训练了两个小规模语言模型——PleIAs 350M 和 PleIAs 1.2B——并在三个多语言基准上进行了系统评估。核心发现是：**在严格合规的数据约束下训练的小模型，能够达到甚至超越同等规模乃至更大规模主流模型的性能**，这直接验证了“开放数据可行”的核心洞察。

在 MultiBLiMP（多语言语法判断基准）上，PleIAs 350M 取得了 0.774 的聚合准确率（Table 2），显著优于参数量更大的 XGLM 564M（0.711，+0.063）和 BLOOM 560M（0.683，+0.091）。这一结果尤为关键：PleIAs 350M 的参数规模仅为对比模型的约 60%，却实现了 6-9 个百分点的绝对提升，说明 Common Corpus 的数据质量并未因合规约束而受损。当模型规模扩展至 1.2B 时，PleIAs 1.2B 的 MultiBLiMP 得分达到 0.797，与 Google 的 Gemma 3 1B（0.799）仅差 0.002，处于同等水平。这一对比值得注意，因为 Gemma 3 的训练数据包含大量受版权保护内容，而 Common Corpus 完全规避了此类数据——性能差距几乎可以忽略。

![[assets/figures/papers/paper_list_l27_https_openreview_net_forum_id_0wSlFpMsGb/figures/007_Table_2.jpg]]
*Table 2: Benchmarking results. “Ours” refers to PleIAs models pre-trained on Common Corpus*

在 XStoryCloze（多语言故事完形填空）上，PleIAs 350M 得分为 0.509（Table 2），虽然绝对数值不高，但鉴于任务本身难度和模型规模，这一结果仍具参考意义。在 XCOPA（多语言因果推理）上，两个 PleIAs 模型同样展现了多语言推理能力。

**证据强度**：MultiBLiMP 的结论置信度最高（0.98），因为该基准覆盖语言广泛且对比模型充分。XStoryCloze 和 XCOPA 的结果置信度略低（0.95），但整体趋势一致。

### 数据集特性对比：唯一满足四项标准的语料库

Table 1 将 Common Corpus 与七个当代主流预训练数据集进行了系统对比，评估维度包括：多领域覆盖（Multidomain）、非网页爬取来源（Beyond Web Crawl）、多语言支持（Multilingual）和许可合规数据（Permissive data）。**Common Corpus 是唯一同时满足全部四项标准的数据集**。

具体而言：
- **KL3M**（Bommarito et al., 2025）满足许可合规和非网页爬取，但仅限于英语行政文本，缺乏多语言和多领域覆盖。
- **Dolma**（Soldaini et al., 2024）覆盖多领域但以英语为主，且许可状态不明确。
- **C4**（Raffel et al., 2020）、**ROOTS**（Laurençon et al., 2022）、**DCAD 2000**（Shen et al., 2025）和 **FineWeb 2**（Penedo et al., 2025）均依赖大规模网页爬取，许可状态混杂，且部分数据集以英语为主。
- **Common Pile**（Kandpal et al., 2025）虽满足许可合规，但仅限英语。

这一对比揭示了 Common Corpus 的独特定位：它并非在单一维度上最优，而是在合规性、多样性和多语言覆盖之间实现了此前未被满足的平衡。Table 1 的证据置信度为 0.95，维度定义清晰且对比对象明确。

### 数据规模与组成统计

Table 3 呈现了 Common Corpus 六大子集的详细统计。语料库总计约 5.17 亿份文档、1.09 万亿词、约 2 万亿 token。各子集贡献如下：
- Open Government 是最大的子集，贡献了主要的 token 量；
- Open Culture 包含大量历史文档，时间跨度从 18-19 世纪甚至更早（Figure 3a）；
- Open Code 涵盖多种编程语言，Java 以约 357 亿 token 领先（Table 10），JavaScript（约 289 亿）和 Python（约 267 亿）紧随其后。

![[assets/figures/papers/paper_list_l27_https_openreview_net_forum_id_0wSlFpMsGb/figures/016_Table_10.jpg]]
*Table 10: Token counts by programming language or framework*

Table 5 的语言排行显示英语占据主导地位（约 9690 亿 token），是第二名法语（约 2750 亿）的 3.5 倍、第三名德语（约 1120 亿）的 8.6 倍。这一不平衡是数据集的主要局限之一，但考虑到开放许可数据在非英语语言中的稀缺性，当前分布已是系统收集的结果。有九种语言的 token 量超过 100 亿，表明多语言覆盖并非虚设。

![[assets/figures/papers/paper_list_l27_https_openreview_net_forum_id_0wSlFpMsGb/figures/010_Table_5.jpg]]
*Table 5: Top-50 languages in Common Corpus by token count. Each language is presented with its number of documents, words, and tokens in the corpus. The rows are ordered by the token count*

Table 4 的许可证分布进一步确认了合规性：公共领域（Public Domain）以约 1.14 万亿 token 占绝对主导，其次为 CC-By（约 2880 亿）和 MIT（约 1430 亿），均为宽松许可证。

![[assets/figures/papers/paper_list_l27_https_openreview_net_forum_id_0wSlFpMsGb/figures/009_Table_4.jpg]]
*Table 4: Token counts for the ten most common licenses in Common Corpus*

### 数据质量评估：多维度指标分布

Figure 4 展示了在 30 万份文档样本上的质量评估结果（堆叠直方图，具体指标描述见附录 G）。该图以概率密度分布的形式呈现了 Common Corpus 在多个定性维度上的表现，包括文本连贯性、OCR 质量、字符组成合理性等。从分布形态可推断，大部分文档集中在高质量区间，但存在长尾的低质量样本——这主要源于历史文档的 OCR 残留错误。

Figure 3b 的 t-SNE 可视化进一步表明，Common Corpus 的子集在语义空间上与 C4 和 FineWeb 等网页爬取数据集显著分离。定量分析确认：Common Corpus 与 FineWeb 的前 1000 域名之间，页面重叠率低于 2%，域名重叠率低于 1%。这意味着 Common Corpus 为开放预训练生态贡献了**实质性新增内容**，而非对已有爬取语料的重复。

### 失败模式与局限性

尽管主实验结果积极，但以下局限性限制了结论的外推范围：

1. **规模瓶颈**：Common Corpus 当前约 2 万亿 token 的规模仅足以训练 350M 和 1.2B 参数的小模型。对于更大规模的模型预训练，数据量仍显不足。这是“合规性 vs. 规模”权衡的直接体现。

2. **语言不平衡**：英语 token 占比过高，低资源语言的代表性和数据量仍然有限。Figure 2 的地理分布图虽展示了 50+ 语言的覆盖，但多数语言的文档量在 log 尺度上仍偏低。

3. **OCR 残留错误**：尽管开发了 OCRoscope、OCRerrcr 和 OCRonos 等专用工具链进行 OCR 质量检测与纠错，但无法达到 100% 准确率。历史文档中的数字化错误可能对模型的语言建模质量产生微妙影响。

4. **历史偏见**：Open Culture 子集包含大量 18-19 世纪的历史文本，虽经 Celadon 毒性分类器过滤，但可能无法完全消除不符合当代伦理标准的用语和偏见。

5. **代码偏向**：Open Code 子集中 Java、JavaScript、Python 占据绝对主导（Table 10），可能导致模型在编程任务上偏向主流语言，对 Rust、Ruby 等较小众语言的建模能力不足。

6. **缺少指令微调数据**：Common Corpus 仅面向预训练阶段，不包含指令微调或特定任务所需的标注数据，限制了直接用于对话式应用的可能性。

### 消融分析

本文未提供标准的消融实验（如逐一移除数据子集或清洗模块后重新训练并评估）。考虑到训练 LLM 的计算成本，这可以理解，但确实限制了我们对各子集和清洗模块贡献度的精确归因。当前仅能通过以下间接证据推断：

- MultiBLiMP 上的优异表现暗示 Open Government 和 Open Culture 中的正式文本可能对语法建模贡献显著；
- 多语言能力的来源可部分归因于 Legal Commons 中 24 种欧盟语言的平行文档（Table 7）；
- OCR 纠错工具链的必要性由 Open Culture 的历史文档质量间接支撑，但缺乏“使用/不使用 OCRonos”的对照实验。

![[assets/figures/papers/paper_list_l27_https_openreview_net_forum_id_0wSlFpMsGb/figures/013_Table_7.jpg]]
*Table 7: Legal Commons sources distribution with languages*

**需手动验证**：各清洗模块（Segmentext、OCRerrcr、OCRonos、Celadon）的独立贡献度尚无定量证据，相关结论需谨慎对待。

### 补充图表

![[assets/figures/papers/paper_list_l27_https_openreview_net_forum_id_0wSlFpMsGb/figures/012_Table_6.jpg]]
*Table 6: Finance Commons sources distribution with languages*

![[assets/figures/papers/paper_list_l27_https_openreview_net_forum_id_0wSlFpMsGb/figures/014_Table_8.jpg]]
*Table 8: Subsets of Open Culture with language coverage, type of document, and token count*

![[assets/figures/papers/paper_list_l27_https_openreview_net_forum_id_0wSlFpMsGb/figures/015_Table_9.jpg]]
*Table 9: Token count by dataset Open Science*

## 方法谱系与知识库定位

### 与现有数据集的差异化定位

Common Corpus 的构建逻辑直接回应了当前 LLM 预训练数据集面临的核心矛盾：**规模与合规性不可兼得**。Table 1 将 Common Corpus 与七个代表性数据集进行了四维度对比（多领域、非网页爬取、多语言、许可数据），Common Corpus 是唯一同时满足全部四项标准的数据集。这一差异化的根源在于其构建策略的系统性转变——从“事后许可辩护”转向“事前许可筛选”。

具体而言，各基线数据集在许可合规性上存在明显缺口：

- **C4** (Raffel et al., 2020) 和 **ROOTS** (Laurençon et al., 2022) 均以大规模网页爬取为基础，依赖合理使用（fair use）原则，但包含大量未经明确许可的版权内容，法律风险日益突出。
- **Dolma** (Soldaini et al., 2024) 虽然覆盖多领域，但语言以英语为主，且并非所有数据均具备宽松许可。
- **FineWeb 2** (Penedo et al., 2025) 和 **DCAD 2000** (Shen et al., 2025) 同样基于网页爬取，许可状态混杂。
- **KL3M** (Bommarito et al., 2025) 在许可合规性上最为接近，但其数据来源局限于英语行政文本，缺乏多语言和多领域覆盖。
- **Common Pile** (Kandpal et al., 2025) 虽然采用宽松许可，但仅限于英语。

Common Corpus 的关键突破在于：通过系统性地收集政府文档（Open Government）、文化遗产机构数字化内容（Open Culture）、开放获取科学文献（Open Science）、经许可筛选的网页档案（Open Web）、开源代码库（Open Code）和语义数据（Open Semantic）六大领域的数据，在严格合规的前提下实现了**约 2 万亿 token** 的规模（Table 3），覆盖 **50+ 语言**（Table 5），其中包含低资源语言且非机器翻译生成。

### 方法创新与工具链贡献

Common Corpus 的方法论贡献不仅在于数据收集策略，更在于为开放数据治理开发了一套专用工具链，解决了历史文本数字化场景中的关键瓶颈：

| 工具 | 功能定位 | 技术路线 |
|------|----------|----------|
| **Segmentext** | 文本分割 | 专用语言模型，将原始文档切分为连贯段落 |
| **OCRoscope** | OCR 质量检测 | 基于 cld2 的 7-gram 语言检测，评估文档数字化质量 |
| **OCRerrcr** | OCR 错误检测 | DeBERTa-v3 风格模型（400M 参数），标注 OCR 误差 |
| **OCRonos** | OCR 纠错生成 | 基于 Llama 3 8B 微调，修复数字化文本错误 |
| **Celadon** | 多语言毒性分类 | DeBERTa-v3-small 模型（~140M），从 200 万合成标注样本从头训练 |
| **Presidio** | PII 信息移除 | 微软开源工具，替换个人身份信息为虚构值 |

这套工具链的核心价值在于：**使得大量公共领域但数字化质量参差不齐的历史文本（如 18-19 世纪文献，见 Figure 3a）能够被有效清洗并纳入预训练语料**。这是 Common Corpus 区别于仅依赖网页爬取的数据集的关键技术支撑。

### 适用边界与已知局限

Common Corpus 当前的设计决定了其适用范围存在明确边界：

1. **模型规模约束**：当前约 2 万亿 token 的规模仅足够训练小模型（350M 和 1.2B 参数）。如论文所述，要支持更大规模模型的预训练，需持续扩充开放数据。这是 Common Corpus 与工业级闭源数据集（通常数十万亿 token）之间的根本差距。

2. **任务覆盖缺口**：数据集仅包含预训练语料，不包含指令微调或特定任务所需的标注数据，限制了直接用于对话系统或特定下游任务的微调场景。

3. **语言分布失衡**：尽管支持 50+ 语言，英语仍占绝对主导（约 969B token，是法语的 3.5 倍、德语的 8.6 倍，见 Table 5）。低资源语言的代表性和数据量仍有限。

4. **数据清洗精度上限**：OCR 纠错和质量过滤虽使用了先进模型，但无法达到 100% 准确率，部分数字化文本可能仍有残留错误。PII 识别方面，Presidio 基础设置仅能识别 55-60% 含电话号码的文本，通过自定义正则表达式提升至 85%，仍有改进空间。

5. **历史偏见残留**：文化遗产内容涉及历史文本，尽管经过毒性过滤，但可能无法完全消除不符合当代伦理标准的用语。

6. **代码语言偏向**：代码数据中某些编程语言占绝对主导（Java 约 35.7B token，JavaScript 约 28.9B，Python 约 26.7B，见 Table 10），可能导致模型在编程任务上的语言偏向。

### 开放问题与未来方向

Common Corpus 的构建经验揭示了开放数据生态中若干待解决的关键问题：

- **网页许可识别精度**：当前对网页档案中开放许可证的识别存在局限性——许可证可能仅适用于页面部分内容而非全部。如何通过语言模型辅助的细粒度标注来克服这一局限，是扩大开放网络数据源的关键技术挑战。

- **低资源语言扩展**：能否在保持完全开放许可的前提下，扩展 Common Corpus 以包含更多低资源语言和最新数据，决定了其多语言能力的上限。

- **隐性偏见评估**：在数据治理过程中，如何更精确地评估和消除历史文本中的隐性偏见，而非仅依赖关键词过滤，是一个需要方法论创新的问题。

- **合规性持续维护**：随着法律法规的演进（如各国对“公共领域”定义的调整），如何建立数据集的持续合规审查机制，是开放数据集长期可用性的保障。

- **与下游任务的衔接**：Common Corpus 证明了开放数据在小模型预训练上的可行性，但如何构建对应的开放指令微调数据集，形成完整的开放训练管线，是后续工作的重要方向。

## 原文 PDF

![[paperPDFs/ICLR_2026/Common_Corpus_The_Largest_Collection_of_Ethical_Data_for_LLM_Pre_Training.pdf]]
