---
title: "Gastric-X: A Multimodal Multi-Phase Benchmark Dataset for Advancing Vision-Language Models in Gastric Cancer Analysis"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/Gastric_X_A_Multimodal_Multi_Phase_Benchmark_Dataset_for_Advancing_Vision_Language_Models_in_Gastric_Cancer_Analysis.pdf
project_link: null
code_link: null
huggingface_link: "https://huggingface.co/datasets/HaoChen2/Gastric-X"
aliases:
- GXV
- Gastric-X
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
- topic/generative_models_diffusion
- topic/benchmarks_datasets_evaluation
core_operator: 构建Gastric-X数据集，整合四期CT、内窥镜图像、结构化实验室指标、诊断报告及专家标注（3D边界框、分期、VQA对），从而模拟临床医生的多源证据整合过程。
primary_logic: 临床诊断本质上是多模态的，医生需要协同分析影像、生化检验和文本报告；当前VLM数据集过分简化了这种复杂性，导致模型只依赖表面关联，无法进行真正的跨模态循证推理。
claims:
- Gastric-X包含1.7K病例，覆盖四相CT（7.1K扫描）、内窥镜（1.7K图像）、134项结构化生化指标和三种临床报告，并在患者级别对齐。
- 添加生化表格和边界框后，所有VLM在VQA、报告生成等任务上持续提升，全模态配置（Image+Table+Bbox）达到最佳性能。
- 经过适配的X2-VLM-Med在所有基准测试上显著超越其他通用和医学VLM，验证了数据集对多模态推理的评估能力。
- Gastric-X VQA 上 AUC (%) = 91.5
---

# Gastric-X: A Multimodal Multi-Phase Benchmark Dataset for Advancing Vision-Language Models in Gastric Cancer Analysis

> [!tip] 核心洞察
> 临床诊断本质上是多模态的，医生需要协同分析影像、生化检验和文本报告；当前VLM数据集过分简化了这种复杂性，导致模型只依赖表面关联，无法进行真正的跨模态循证推理。

| 字段 | 内容 |
|------|------|
| 中文题名 | Gastric-X：推进胃癌视觉语言模型的多模态多期基准数据集 |
| 英文题名 | Gastric-X: A Multimodal Multi-Phase Benchmark Dataset for Advancing Vision-Language Models in Gastric Cancer Analysis |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2603.19516) · [HuggingFace](https://huggingface.co/datasets/HaoChen2/Gastric-X) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction #topic/generative_models_diffusion #topic/benchmarks_datasets_evaluation |
| Method | Gastric-X多模态基准与VLM适配 |
| Dataset | Gastric-X VQA, Gastric-X Report Generation, Gastric-X Cross-modal Retrieval, Gastric-X Disease Stage Classification |

> [!tip] 效果简介
> - Gastric-X VQA 上，AUC (%) 91.5 vs 86.5 (Med-Flamingo) (+5.0)。
> - Gastric-X Report Generation 上，BERTScore F1 82.0 vs 73.1 (Med-Flamingo) (+8.9)。
> - Gastric-X Cross-modal Retrieval 上，R@1 Image→Text (%) 48.9 vs 42.8 (Med-Flamingo) (+6.1)。

## 概要

### 问题背景

胃癌是全球第五大常见恶性肿瘤，其临床诊断依赖于医生对多源异构证据的综合分析——包括多期增强CT、内窥镜检查、血液生化指标以及文本诊断报告。然而，现有医学视觉语言模型（VLM）的基准数据集普遍存在模态单一化问题：它们要么仅提供2D静态图像与简单文本描述，要么缺乏患者级别的多模态对齐，无法反映真实临床工作流中“影像-化验-报告”协同推理的复杂性。这一瓶颈严重制约了VLM在胃癌辅助诊断中的实际应用潜力。

### 核心贡献

针对上述缺口，本文提出**Gastric-X**——首个面向胃癌分析的大规模多模态、多期基准数据集。其核心设计理念是模拟临床医生的多源证据整合过程，在患者级别对齐四类关键信息：

- **多期3D CT**（平扫期、动脉期、静脉期、平衡期），共7.1K次扫描，附带3D边界框标注；
- **内窥镜图像**（1.7K张）；
- **结构化生化指标**（134项实验室变量）；
- **临床文本报告**（诊断报告、CT报告等）。

基于该数据集，作者进一步将通用VLM（以X2-VLM为代表）适配为医学版本**X2-VLM-Med**：将视觉编码器替换为3D Swin Transformer以处理体积CT数据，文本编码器替换为Med-BERT以注入医学领域知识，并增加轻量级双向检索头支持跨模态检索。

### 关键发现

实验揭示了一个核心规律：**逐步引入多模态信息可稳定提升VLM的临床推理能力**。在视觉问答（VQA）任务上，全模态配置（Image + Table + Bbox）使X2-VLM-Med的AUC从仅图像输入的85.3%提升至91.5%；在报告生成任务上，BERTScore F1达到82.0，较次优基线Med-Flamingo高出8.9个百分点。消融分析进一步表明，病灶聚焦型提示策略的临床有效性最高（92.4%），而空间定位类提示因描述歧义导致一致性较低（79.3%）。

### 方法定位

Gastric-X在医学VLM数据集中占据独特位置：与仅覆盖2D放射影像的MIMIC-CXR、仅提供VQA对的VQA-RAD等数据集相比，它首次在同一患者层面整合了多期3D体积影像、结构化化验数据和原始诊断报告。这使得Gastric-X不仅是评估VLM多模态融合能力的基准，也为未来跨模态循证推理研究提供了数据基础。



### 胃癌诊断的临床复杂性

胃癌是全球第五大常见恶性肿瘤，其诊断高度依赖多模态信息的协同分析。在真实临床工作流中，医生不会仅凭单一影像做出判断，而是综合四期增强CT（平扫、动脉期、静脉期、平衡期）、内窥镜图像、结构化生化指标（如血常规、血清生化、肿瘤标志物）以及文本诊断报告，进行跨模态循证推理。这种多源证据的整合过程是准确分期和治疗决策的核心，但现有医学视觉语言模型（VLM）的数据集远未反映这一现实。

### 现有医学VLM数据集的结构性缺陷

当前医学VLM数据集普遍存在三个关键缺口。**模态单一**：大多数数据集仅覆盖2D静态影像（如X光片、病理切片），缺乏多期3D CT扫描和时序生化指标。**信息割裂**：即使少数数据集包含多种模态，也缺乏患者级别的对齐——影像、化验数据和文本报告无法在同一病例上关联，模型只能学习表面统计关联，而非真正的临床推理。**标注简化**：现有基准通常将临床任务简化为二分类或单轮问答，缺少病灶边界框、分期标注和报告生成等多层次评估维度。

Table 1 的系统对比清晰地揭示了这一断层：在Gastric-X之前，没有任何公开数据集同时提供多期CT、结构化生化指标、病灶标注和原始诊断报告。

### 核心瓶颈与本文动机

**根本瓶颈在于**：现有VLM无法获得反映真实诊断流程的训练和评估环境，导致模型在复杂临床推理任务上的能力无法被有效测量和提升。临床诊断本质上是多模态的——医生需要同时解读影像中的病灶形态、化验单中的异常指标和报告中的语义描述，而当前数据集过分简化了这种复杂性。

**本文的核心动机**是构建一个模拟临床医生多源证据整合过程的数据集，使VLM能够在贴近真实诊疗场景的条件下进行训练和评估。Gastric-X通过整合四期CT、内窥镜、134项结构化生化指标和三种临床报告，并在患者级别对齐，填补了这一空白。该数据集包含1.7K病例、7.1K CT扫描和专家标注的3D边界框与分期信息，为多模态循证推理提供了迄今最全面的基准平台。



## 核心方法与创新机理

Gastric-X 的核心创新并非提出全新的模型架构，而是**构建了首个面向胃癌临床诊断全流程的多模态、多期基准数据集，并通过最小侵入的架构适配，系统性地验证了多模态融合对视觉语言模型（VLM）临床推理能力的因果性提升**。其创新可拆解为以下三个关键维度。

### 1. 数据集设计：从“图像-文本对”到“临床证据链”

现有医学 VLM 数据集（如 ROCO、MedICaT、PMC-VQA）大多停留在静态 2D 图像与单句描述的配对层面，忽略了临床诊断中医生必须协同分析的多源异构证据——多期 3D 影像、结构化生化指标、诊断文本报告。Gastric-X 填补了这一断层：

- **多期 3D CT 对齐**：数据集包含 1.7K 病例、7.1K 次 CT 扫描，覆盖平扫、动脉期、静脉期和平衡期四个时相，并在患者级别对齐（见 Figure 1 右面板）。这迫使模型学习病灶在不同增强时相下的动态特征，而非依赖单一时相的表面纹理。
- **结构化生化表格**：引入 134 项实验室指标（血常规、血清生化、肿瘤标志物等），并仅提取异常值转化为文本描述作为模型输入（见 Table 8）。这一设计模拟了临床医生“先看异常指标”的认知习惯，同时避免了冗余数据对模型的干扰。
- **3D 边界框渲染**：专家标注的病灶边界框被直接渲染为 CT 切片上的彩色叠加层，作为辅助视觉输入。这种方式将空间定位信息显式注入 VLM，弥补了纯文本描述在空间关系表达上的模糊性。

如 Figure 1 所示，Gastric-X 的数据模态覆盖了从影像、化验到文本报告的全链条临床证据，其与现有数据集的对比（Table 1）表明，它是目前唯一同时具备多期 CT、生化数据和原始诊断报告的胃癌 VLM 基准。

### 2. 方法适配：轻量级架构改造实现多模态注入

论文并未提出全新的 VLM 架构，而是对现有通用 VLM **X2-VLM** 进行了三个关键槽位替换（changed slots），使其能够消化 Gastric-X 的多模态输入：

| 模块槽位 | 基线值 | 替换值 | 创新意图 |
|---------|--------|--------|---------|
| 视觉编码器 | CLIP ViT-L (2D) | 3D Swin Transformer | 捕获多期 CT 的时空特征，而非单帧 2D 语义 |
| 文本编码器 | BERT | Med-BERT | 注入医学领域预训练知识，提升对临床术语的语义理解 |
| 检索头 | 无 | 轻量级双向检索头 | 实现图像→文本与文本→图像的双向跨模态匹配，支撑检索任务 |

此外，表格输入经过“异常值提取→文本描述转换”的预处理管线，而非直接输入原始结构化数据。这一设计降低了 VLM 对表格格式的敏感性，使其能通过自然语言通路吸收生化证据。整体适配架构见 Figure 3。

### 3. 因果性验证：多模态融合并非“锦上添花”，而是“雪中送炭”

Gastric-X 最具说服力的创新贡献在于，它通过严格的消融实验证明了**多模态融合对临床推理能力的因果性提升**，而非仅仅是相关性的叠加。核心证据来自 Table 2 和 Figure 4：

- **逐步添加模态，性能单调递增**：以 VQA 任务为例，X2-VLM-Med 在仅使用图像时 AUC 为 85.3%；加入生化表格后提升至 87.6%；再加入边界框后达到 91.5%（Table 2 (a)）。报告生成任务呈现相同趋势（BERTScore F1 从 76.9 提升至 82.0）。
- **全模态配置（Image+Table+Bbox）在所有任务上达到最优**：如 Figure 4 雷达图所示，三模态融合在 VQA、报告生成、跨模态检索三个任务的所有指标上均形成最大包络圆，表明多模态证据之间存在互补增益，而非信息冗余。
- **跨模型一致性**：这一趋势在 LLaVA-1.5-7B、BLIP-2、LLaVA-Med 等其他 VLM 上同样成立，排除了“仅对特定架构有效”的偶然性。

这种因果性验证直接回应了论文的核心洞察：**临床诊断本质上是多模态的，当前 VLM 数据集过分简化了这种复杂性，导致模型只依赖表面关联，无法进行真正的跨模态循证推理**。Gastric-X 通过数据集设计与消融实验，将这一假设转化为可量化的证据链。



Gastric‑X 的工作流围绕“多模态临床数据对齐 → VLM 适配 → 多任务评估”三条主线展开，其核心设计目标是模拟临床医生同时审阅影像、化验和文本报告的真实诊断流程。

### 数据流与预处理管线

输入数据包含四个模态：四期 3D CT（平扫、动脉期、静脉期、平衡期）、内窥镜图像、134 项结构化生化指标（血常规、血清生化、肿瘤标志物等），以及三种临床文本报告（诊断报告、CT 报告、内镜报告）。所有数据在患者级别对齐，形成 1.7K 病例的多模态配对。

预处理阶段执行两个关键标准化操作：
- **CT 体积统一化**：将 CT 值裁剪至 $[-100, 300]\ \mathrm{HU}$ 窗口，重采样至各向同性体素间距 $1.0 \times 1.0 \times 1.0\ \mathrm{mm^3}$，并通过裁剪/填充统一至 $288 \times 288 \times 192$ 的目标体积尺寸。
- **结构化表格文本化**：仅提取异常化验指标，将其转换为简洁的文本描述，避免原始数值表直接输入带来的稀疏性和噪声。

### 辅助输入生成模块

为增强 VLM 的空间感知和循证推理能力，管线中嵌入两个辅助输入生成步骤：
- **3D 边界框渲染**：将专家标注的多类病灶边界框（肿瘤、胃周癌灶、胃区域）直接渲染为 CT 切片上的彩色叠加层，使视觉编码器能感知病灶的空间位置。
- **异常化验指标提取**：从 134 项结构化变量中筛选偏离参考范围的条目，生成“异常值文本描述”，作为表格模态的紧凑表示。

### VLM 适配架构

核心推理引擎基于 **X2‑VLM** 架构进行医学领域适配，形成 **X2‑VLM‑Med**。适配涉及三个关键模块变更：

| 模块 | 原配置 | 适配后配置 | 功能 |
|------|--------|------------|------|
| 视觉编码器 | CLIP ViT‑L (2D) | 3D Swin Transformer | 处理四期 3D CT 体积 |
| 文本编码器 | BERT | Med‑BERT | 捕获医学文本语义 |
| 检索头 | 无 | 轻量级双向检索头 | 支持图像‑文本双向匹配 |

多模态输入以拼接方式送入 VLM：视觉编码器处理 CT 切片（可附带边界框渲染），文本编码器接收结构化表格描述、临床查询文本和病灶定位提示，模型在统一的嵌入空间中进行跨模态推理。

### 多任务评估出口

适配后的 VLM 在同一基准上接受五项下游任务评估：视觉问答（VQA）、报告生成、跨模态检索、疾病分期分类和病灶检测。消融实验表明，逐步添加生化表格和边界框可使所有任务性能稳定提升，全模态配置（Image + Table + Bbox）始终达到最优，验证了多源证据整合对临床推理的增益效应。

### 补充图表

![[assets/figures/papers/paper_list_l2742_https_arxiv_org_abs_2603_19516/figures/001_Figure_1.jpg]]
*Figure 1: Overview of the multi-modal information in proposed Gastric-X. The center panel shows a schematic gastric representation alongside an endoscopic image. The left panel presents examples of structured laboratory data (e.g., blood counts, serum biochemistry, and tumor markers) and clinical textual reports (diagnostic and CT reports) that reflect real-world radiological reasoning. The right panel illustrates multi-phase 3D CT scans (non-contrast, arterial, venous, and equilibrium phases) with multi-class lesion annotations, including tumor, perigastric carcinoma, and stomach regions*



Gastric-X 的数据处理与模型适配管线由四个关键模块构成，分别解决多模态输入的标准化、结构化信息的语义化、视觉定位线索的注入以及医学知识的迁移。

### 1. 多期CT标准化与对齐（预处理模块）

3D CT 体积在输入模型前需经过统一的归一化流水线。首先将 CT 值裁剪至 $[-100, 300]\ \mathrm{HU}$ 窗口以聚焦软组织与病灶对比度，随后重采样至各向同性体素间距 $1.0 \times 1.0 \times 1.0\ \mathrm{mm^3}$，最后通过裁剪或零填充统一至目标体积尺寸 $288 \times 288 \times 192$。该模块确保不同扫描设备与协议下获取的四期 CT（平扫、动脉期、静脉期、平衡期）在空间和强度上完全对齐。

### 2. 异常化验指标提取（表格语义化模块）

结构化实验室数据包含 134 项生化变量（完整列表见 Table 8），直接输入 VLM 会引入大量冗余信息。Gastric-X 采用基于规则的提取策略：仅筛选偏离参考范围的异常条目，并将其转换为简洁的文本描述。这一设计将稀疏的数值表格压缩为高信息密度的自然语言片段，降低了模型对无关维度的过拟合风险。

### 3. 3D边界框渲染（定位线索注入模块）

专家标注的病灶 3D 边界框被直接渲染为 CT 切片上的彩色叠加层，作为视觉定位线索注入 VLM。该模块使模型在接收多期 CT 图像的同时，能够显式感知肿瘤、胃周侵犯及胃部区域的精确空间位置，从而将定位信息融入下游的问答与报告生成推理。

### 4. VLM适配引擎（核心推理模块）

为适配 Gastric-X 的多模态特性，本文以 X2-VLM 为基础架构进行三项关键改造，形成 **X2-VLM-Med**：

- **视觉编码器替换**：将原始 2D CLIP ViT-L 替换为 **3D Swin Transformer**，以直接处理四期 3D CT 体积输入，捕获跨相期的时空对比增强特征。
- **文本编码器替换**：将通用 BERT 替换为 **Med-BERT**，注入医学领域预训练知识，提升对诊断报告与生化描述的语言理解能力。
- **双向检索头添加**：在编码器之上附加一个轻量级双向检索头，实现图像→文本与文本→图像的跨模态匹配，支撑跨模态检索任务。

### 5. 关键训练公式

训练过程使用 AdamW 优化器，学习率设置为：

$$lr = 5 \times 10^{-5}$$

该学习率同时应用于视觉编码器、文本编码器及新增检索头的参数更新，未采用分层学习率策略。所有实验在此统一配置下进行微调，确保不同模态配置间的可比性。

### 补充图表

![[assets/figures/papers/paper_list_l2742_https_arxiv_org_abs_2603_19516/figures/004_Figure_3.jpg]]
*Figure 3: VLM adaptation. In adapting VLMs to our dataset, the visual encoder incorporates multi-phase CT inputs, while test tables, textual queries, and lesion-localization cues serve as complementary multimodal inputs guiding the model’s diagnostic reasoning. The VLMs must effectively adapt to these diverse input modalities to better capture and perform the targeted clinical tasks*



## 实验与关键发现

### 核心实验设计

为验证Gastric-X数据集对多模态临床推理的评估能力，作者在五个互补任务上进行了系统实验：视觉问答（VQA）、报告生成、跨模态检索、疾病分期分类和病灶检测。实验的核心变量是**输入模态的组合**——从仅图像（Image Only）逐步叠加结构化化验表格（+Table）和3D边界框渲染（+BBox），以量化每种临床信息源对模型推理的边际贡献。

评估覆盖三类基线模型：通用VLM（LLaVA-1.5-7B、BLIP-2、X2-VLM）、医学VLM（LLaVA-Med v1.5、Med-Flamingo、MedVInT）以及传统视觉模型（ResNet-50、Swin Transformer、Faster R-CNN）。其中，X2-VLM经过针对性适配形成**X2-VLM-Med**：将其2D视觉编码器替换为3D Swin Transformer以处理多期CT体数据，将文本编码器替换为Med-BERT以注入医学领域知识，并增加轻量级双向检索头以支持跨模态匹配。所有VLM使用AdamW优化器，学习率设为 $5 \times 10^{-5}$。

### 主结果：多模态信息持续提升诊断推理

**Table 2** 汇总了VQA和报告生成任务的核心结果，揭示了两个关键规律：

**第一，医学领域适配至关重要。** 在仅图像条件下，X2-VLM-Med的VQA AUC已达85.3%，显著高于通用版X2-VLM（78.2%）和医学VLM Med-Flamingo（80.1%），表明3D视觉编码器与医学文本编码器的协同预训练是性能提升的基础。

**第二，多模态信息产生稳定且可叠加的增益。** 以X2-VLM-Med为例，VQA AUC从Image Only的85.3%提升至Image+Table的88.7%（+3.4），再提升至Image+Table+BBox的91.5%（+2.8）。报告生成的BERTScore F1同样遵循这一趋势：从73.5（Image Only）→ 78.2（+Table）→ 82.0（+Table+BBox）。**Figure 4** 的雷达图直观展示了这一规律：全模态配置（Image+Table+Bbox）在所有评估指标上均达到最优，形成对仅图像配置的全面包围。

这一现象具有明确的临床解释：结构化化验指标提供了影像无法直接反映的全身性信息（如肿瘤标志物、血常规异常），而3D边界框则注入了精确的空间定位线索，两者分别弥补了视觉模型在生化推理和空间理解上的固有短板。

### 跨模态检索：双向匹配能力验证

**Table 4** 展示了仅图像条件下的跨模态检索结果。X2-VLM-Med在Image→Text方向上取得R@1=48.9%，在Text→Image方向上取得R@1=45.2%，均显著优于其他VLM。值得注意的是，通用模型BLIP-2的检索性能极低（R@1<5%），表明未经医学适配的视觉-语言对齐在专业领域几乎失效。Med-Flamingo作为医学VLM取得次优结果（R@1=42.8%和38.1%），但仍与X2-VLM-Med存在6-7个百分点的差距，验证了3D体数据编码对CT检索任务的关键作用。

### 疾病分期分类：细粒度多分类能力

**Table 5** 展示了基于TNM分期的疾病阶段分类结果。X2-VLM-Med在全模态配置下达到AUC=90.8%，相比仅图像配置（87.5%）提升3.3个百分点。一个值得关注的现象是：传统视觉模型Swin Transformer在仅图像条件下AUC已达89.2%，甚至超过部分VLM，但在叠加表格和边界框信息后无法利用这些额外模态——这正是VLM相较于纯视觉模型的本质优势所在。

### 病灶检测：空间定位与语义理解的结合

**Table 6** 的病灶检测任务要求模型在CT切片中定位肿瘤和胃周癌灶。X2-VLM-Med取得mAP=51.5%，略高于MedVInT（50.2%）和Faster R-CNN（49.8%）。该任务的绝对性能偏低，主要因为病灶检测本质上是密集预测问题，而当前VLM的架构设计更偏向全局语义理解。但X2-VLM-Med在定位准确率（Loc. Acc.）上达到68.3%，显著高于其他VLM，表明3D边界框提示有效引导了模型的空间注意力。

### 消融实验：提示策略与临床有效性

**Table 7** 揭示了VQA问题生成策略对临床有效性的影响。病灶聚焦提示（Lesion-focused）生成的问答对临床有效性最高（92.4%），而定位类提示（Location-based）因涉及空间描述歧义，一致性降至79.3%。这一消融实验说明：当前VLM在需要精确空间语言输出的场景下仍存在显著局限，提示工程需要谨慎规避模型的空间表达能力短板。

### 失败模式与局限性

综合实验结果，可识别以下失败模式：

1. **空间描述歧义**：定位类VQA的临床一致性不足80%，表明模型在生成精确空间指代（如“贲门左侧壁”）时容易出现模糊或错误描述。
2. **密集预测瓶颈**：病灶检测的mAP仅51.5%，远低于分类和检索任务的表现，反映当前VLM架构在像素级定位任务上的固有劣势。
3. **模态缺失鲁棒性**：当仅提供图像输入时，所有VLM性能均大幅下降，模型尚未学会在信息不完整时进行保守推理或主动请求补充信息。
4. **规模限制**：实验仅在7B参数级别的VLM上进行，更大规模模型（如GPT-4V级别）在此基准上的潜力尚待验证——这既是当前工作的局限，也是Gastric-X作为评估基准的开放研究问题。

### 补充图表

![[assets/figures/papers/paper_list_l2742_https_arxiv_org_abs_2603_19516/figures/006_Table_2.jpg]]
*Table 2: Performance across modalities for Vision Question Answer and report generation. We evaluate four input-modality settings, including Image Only and combinations that add Table, Bounding Box (BBox), or both. The best and second-best results in each column are shown in bold and underlined, respectively*

![[assets/figures/papers/paper_list_l2742_https_arxiv_org_abs_2603_19516/figures/005_Figure_4.jpg]]
*Figure 4: Radar plot comparing multimodal configurations across three medical vision-language tasks. The ”Image+Table+Bbox” configuration achieves the highest overall performance across all evaluation metrics*

![[assets/figures/papers/paper_list_l2742_https_arxiv_org_abs_2603_19516/figures/002_Table_1.jpg]]
*Table 1: Comprehensive comparison of medical vision–language datasets. Multi-phase: scans or images captured at different stages or conditions. Biochemical data: structured laboratory measurements (e.g., serology results) or Electronic Health Records (EHRs). Lesion label: annotations of lesions, including masks or bounding boxes. Textual Modality: how text-based labels are provided. The VQA pairs column specifies whether the dataset is primarily designed for visual question answering. The report column indicates whether original diagnostic reports are available*

![[assets/figures/papers/paper_list_l2742_https_arxiv_org_abs_2603_19516/figures/003_Figure_2.jpg]]
*Figure 2: Gastric-X Overview. (A) Overall stage distribution by gender (67.5% male, 32.5% female). (B) Distribution of 5 tumor markers on a logarithmic scale. (C) Overall distribution of CT slice lengths across 4 different phases. (D) Sankey diagram illustrating the transitions between T, N, and M stages and corresponding overall stages. (E) Histogram of tumor sizes with a cumulative percentage curve. (F) Word cloud summarizing the most frequent terms from radiology reports. Zoom in for better visualization*

![[assets/figures/papers/paper_list_l2742_https_arxiv_org_abs_2603_19516/figures/007_Table_4.jpg]]
*Table 4: Cross-modal retrieval. This table reports retrieval results in both Image-to-Text and Text-to-Image directions. Metrics include Recall@K (%, higher is better), Median Rank and Mean Rank (lower is better), and mean Average Precision (mAP). Bold and underlined numbers denote the best and second-best performance in each column*

![[assets/figures/papers/paper_list_l2742_https_arxiv_org_abs_2603_19516/figures/008_Table_5.jpg]]
*Table 5: Disease stage classification. For each configuration, we evaluate Precision, Recall, F1 score, and Area Under (AUC). These results show how integrating multimodal cues and medical-aware pretraining benefits fine-grained disease staging. Bold and underlined numbers indicate the best and second-best performance in each column*

![[assets/figures/papers/paper_list_l2742_https_arxiv_org_abs_2603_19516/figures/009_Table_6.jpg]]
*Table 6: Lesion detection. Metrics are Average Precision (AP) and F1. mAP denotes mean AP averaged over IoU thresholds from 0.50 to 0.95 (step 0.05), and localization accuracy (Loc. Acc.) is computed at IoU = 0.5*

![[assets/figures/papers/paper_list_l2742_https_arxiv_org_abs_2603_19516/figures/010_Table_7.jpg]]
*Table 7: Effectiveness of different prompting strategies for generating clinically valid VQA questions. Validity represents the percentage of Q/A pairs confirmed by both clinicians*

![[assets/figures/papers/paper_list_l2742_https_arxiv_org_abs_2603_19516/figures/011_Table_8.jpg]]
*Table 8: Full List of 134 Structured Biomedical Variables in the Gastric-X Dataset. De-identified is marked as ”De-ID”*



## 定位与知识库关联

### 任务与基线定位

Gastric-X 面向**多模态临床推理**，其评估体系覆盖视觉问答（VQA）、报告生成、跨模态检索、疾病分期分类和病灶检测五类任务。这一任务谱系决定了其基线选择跨越通用VLM、医学VLM和传统视觉模型三个层级：

- **通用VLM**：**LLaVA-1.5-7B**、**BLIP-2**、**X2-VLM** 作为跨模态对齐能力的上界参考，但它们在医学领域缺乏领域知识注入。
- **医学VLM**：**LLaVA-Med v1.5**、**Med-Flamingo**、**MedVInT** 代表当前医学视觉语言模型的最优水平，但其训练数据以2D静态影像（X光、病理切片）为主，缺乏对3D多期CT和结构化生化数据的处理能力。
- **传统视觉模型**：**ResNet-50**、**Swin Transformer**、**Faster R-CNN** 用于病灶检测和分期分类的纯视觉基线，验证多模态信息是否带来超越视觉特征的增益。

### 关键改动与设计选择

论文对X2-VLM的适配构成了方法谱系中的核心改造点，改动集中在三个模块：

| 改动槽位 | 基线配置 | 本文配置 | 设计动机 |
|---------|---------|---------|---------|
| 视觉编码器 | CLIP ViT-L（2D） | 3D Swin Transformer | 原生支持多期CT体积输入，捕获空间-时间动态特征 |
| 文本编码器 | BERT | Med-BERT | 注入医学领域预训练知识，提升对临床术语的语义理解 |
| 检索能力 | 无 | 轻量级双向检索头 | 支持Image→Text和Text→Image双向匹配，服务于跨模态检索任务 |

此外，表格输入的预处理策略值得注意：从134项结构化生化指标中**仅提取异常值并转换为简洁文本描述**，而非直接输入原始数值表格。这一设计避免了长尾正常值对模型的噪声干扰，同时以自然语言形式将关键临床信号注入VLM的文本流。

### 多模态配置的因果效应

Table 2和图4的消融实验揭示了各模态组件对性能的因果贡献：逐步添加生化表格和边界框后，所有VLM在VQA、报告生成等任务上持续提升，**Image+Table+Bbox的全模态配置达到最佳性能**。这一证据链验证了论文的核心主张——临床诊断本质上是多模态的，单一影像模态无法提供充分的循证依据。

具体而言，X2-VLM-Med在VQA任务上从Image Only的AUC 85.3%提升至全模态的91.5%（+6.2个百分点），报告生成的BERTScore F1从73.1提升至82.0（+8.9）。边界框提供的空间定位线索和异常生化指标提供的系统状态信号，分别从解剖学和病理生理学两个维度补充了CT影像无法直接传达的信息。

### 提示策略的临床有效性

Table 7的消融揭示了VQA问题设计的关键权衡：**病灶聚焦提示**（Lesion-focused）的临床有效性最高（92.4%），而**定位类提示**因空间描述的天然歧义一致性较低（79.3%）。这表明在临床VQA场景中，语义明确的诊断性问题比依赖空间参照的定位问题更适合当前VLM的能力边界。

### 适用边界与局限

1. **疾病范围窄**：数据集仅覆盖胃癌，未扩展到食管癌、肝癌等其他消化道肿瘤。模型的跨疾病泛化能力无法在本基准内评估，**需要手动验证**其在其他癌种上的迁移表现。

2. **模型规模受限**：实验仅在7B参数级别的VLM上进行微调，未测试更大规模模型（如GPT-4V级别）在该基准上的潜力。更大模型是否能在多模态临床推理上涌现质变，仍是开放问题。

3. **数据来源单一**：数据来源于有限机构，设备和人群偏差不可避免。跨机构分布鲁棒性未经验证，**需要手动确认**数据集是否包含多中心来源。

4. **VQA生成风险**：VQA对由LLM生成，尽管经过双重临床验证，仍可能存在未被发现的幻觉或偏差。这构成基准本身的质量上限。

### 开放问题

- Gastric-X的多模态对齐设计范式能否推广到肺癌、肝癌等其他癌症的基准构建？
- 显式跨模态注意力机制是否优于当前的特征拼接/文本注入式融合？
- 在真实临床工作流中，VLM辅助诊断能否可测量地降低医生认知负荷并提高诊断一致性？
- 更大规模VLM在此基准上的表现是否能涌现真正的临床推理能力，而非仅依赖表面统计关联？



## 原文 PDF

![[paperPDFs/CVPR_2026/Gastric_X_A_Multimodal_Multi_Phase_Benchmark_Dataset_for_Advancing_Vision_Language_Models_in_Gastric_Cancer_Analysis.pdf]]
