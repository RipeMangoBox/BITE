---
title: "Error Notebook-Guided, Training-Free Part Retrieval in 3D CAD Assemblies via Vision-Language Models"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/Error_Notebook_Guided_Training_Free_Part_Retrieval_in_3D_CAD_Assemblies_via_Vision_Language_Models.pdf
project_link: null
code_link: null
openreview_forum_id: JMweItBmbx
aliases:
- ENRFPR
tags:
- ICLR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/vision_models_multimodal
core_operator: "Error Notebook 中修正推理轨迹的质量（由 GC 验证器确保）与 RAG 检索到的少样本示例与当前规范的相关性。"
primary_logic: "通过构建错误笔记本（Error Notebook），记录 VLM 自我修正的推理轨迹，并在推理时利用 RAG 检索相关修正案例作为少样本提示，引导模型逐步反思与修正错误，无需额外训练即可大幅提升推理准确率。"
claims:
- "GPT-4o (Omni) 在人类偏好数据集上使用 Error Notebook+RAG 相比不使用错误笔记本的基线取得了 +23.4 个绝对准确率点（41.7% → 65.1%）。"
- "提出的 GC 验证器可在人类偏好数据集上进一步带来最高 +4.5 个准确率点增益。"
- "Error Notebook 方法优于训练自由基线：在自生成数据集上达到 48.3%，而标准少样本学习仅 26.6%，自一致性为 38.9%。"
- "对于高部件数量的复杂装配体（10-50 部件），包含 CoT 推理的 Error Notebook 示例比仅含最终答案的示例始终更有效。"
---

# Error Notebook-Guided, Training-Free Part Retrieval in 3D CAD Assemblies via Vision-Language Models

> [!tip] 核心洞察
> 通过构建错误笔记本（Error Notebook），记录 VLM 自我修正的推理轨迹，并在推理时利用 RAG 检索相关修正案例作为少样本提示，引导模型逐步反思与修正错误，无需额外训练即可大幅提升推理准确率。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 错误笔记本引导的无训练3D CAD装配体视觉语言模型部件检索 |
| 英文题名 | Error Notebook-Guided, Training-Free Part Retrieval in 3D CAD Assemblies via Vision-Language Models |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=JMweItBmbx) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/vision_models_multimodal |
| Method | Error Notebook + RAG framework for part retrieval |
| Dataset | Human preference dataset, Self-generated dataset |

> [!tip] 效果简介
> - Human preference dataset 上，Accuracy (%) 为 65.1 (w/ E-Notebook)，对比 41.7 (w/o E-Notebook)，变化 +23.4。
> - Self-generated dataset 上，Accuracy (%) 为 48.3 (w/ E-Notebook)，对比 28.5 (w/o E-Notebook)，变化 +19.8。
> - Human preference dataset 上，Accuracy (%) 为 35.4 (w/ E-Notebook)，对比 19.3 (w/o E-Notebook)，变化 +16.1。

## 概要

在三维CAD装配体中，基于自然语言规范检索特定部件是一项实用但极具挑战的任务。其核心瓶颈在于：装配体的结构化元数据序列极长（常超出通用视觉语言模型的token限制），且采用非自然语言格式，导致模型难以捕捉部件间细粒度的空间与功能关系，尤其在多部件复杂装配体中表现不佳。

针对这一问题，本文提出了一种**无需训练**的推理框架——**Error Notebook + RAG**。其核心洞见在于：通过构建一个“错误笔记本”（Error Notebook），系统性地记录模型自我修正的正确推理轨迹；在推理时，利用检索增强生成（RAG）策略，从错误笔记本中动态检索与当前查询最相关的修正案例作为少样本提示，引导模型逐步反思并纠正错误，从而在不进行任何额外训练的前提下大幅提升推理准确率。

方法上，本文采用**二阶段VLM流水线**：第一阶段由VLM为每个部件生成简洁的自然语言几何描述，将非自然语言的CAD元数据转化为模型可理解的中间表示；第二阶段基于这些描述和自然语言规范执行部件检索。错误笔记本的构建通过让VLM识别并修正自身推理中的首个错误，生成正确的推理轨迹，并由语法约束验证器（GC Verifier）过滤结构不完整的轨迹，确保笔记本质量。推理时，则从错误笔记本中检索最相似的修正推理作为少样本示例，辅助模型进行链式推理。

实验结果表明，该方法在人类偏好数据集上为GPT-4o带来了最高**+23.4个绝对准确率点**的提升（从41.7%提升至65.1%），GC验证器可进一步贡献最高**+4.5个准确率点**。在自生成数据集上，该方法同样以48.3%的准确率显著优于标准少样本学习（26.6%）和自一致性方法（38.9%）。消融实验进一步揭示，对于复杂装配体（10–50个部件），包含链式推理的示例始终优于仅含最终答案的示例，且二阶段流水线相比直接基于图像推理的基线有大幅提升（33.6% vs 15.0%）。

值得注意的是，该方法仍存在局限性：构建错误笔记本需依赖高性能专有VLM并进行多次调用，带来一次性计算开销；对于超过50个部件的高复杂装配体，绝对准确率仍然较低（最高约21%）；此外，其在不同CAD格式或领域的泛化性尚待验证。

### 问题背景：CAD 装配体中的部件检索

在三维 CAD 装配体建模中，一个核心任务是**根据自然语言规范检索对应的部件标识符**。例如，工程师可能发出“找到连接底板和侧板的四个螺栓”这样的查询，系统需要从包含数十甚至上百个部件的装配体元数据中，准确返回目标部件的符号标识。这一任务的关键挑战在于，CAD 装配体的元数据以长序列、非自然语言的格式存储，其长度常常超出视觉语言模型（VLM）的 token 限制，导致通用 VLM 难以有效捕捉部件间的细粒度空间与功能关系。

### 现有方法的缺口

当前基于 VLM 的部件检索方法面临两个主要瓶颈：

1. **元数据序列过长且非自然语言格式**：装配体结构信息（如 STEP 文件的层次化描述）以机器可读的符号序列呈现，缺乏自然语言的语义密度。直接将这些冗长的元数据输入 VLM，不仅容易超出上下文窗口限制，更使得模型难以从中提取与查询规范相关的部件关系。

2. **训练自由推理的准确性不足**：在不进行额外微调的情况下，VLM 的链式推理（Chain-of-Thought, CoT）容易在复杂的空间推理和功能关系判断中出错。标准少样本学习（Standard Few-Shot）和自一致性（Self-Consistency）等训练自由基线方法的准确率有限——在自生成数据集上，标准少样本学习仅达到 26.6%，自一致性为 38.9%（Table 3），远不能满足实际工程需求。

### 核心动机：从错误中学习，无需训练

本文的核心洞察是：**VLM 在部件检索任务中产生的错误推理轨迹本身蕴含了宝贵的学习信号**。如果能够系统地记录模型在自我修正过程中生成的正确推理路径，并在后续推理时检索相关的修正案例作为少样本提示，就有可能在**不进行任何模型训练**的前提下，显著提升推理准确率。

基于这一动机，本文提出了 **Error Notebook（错误笔记本）+ RAG 框架**。该方法通过构建一个由 VLM 自我修正生成的正确推理轨迹库（即错误笔记本），并在推理阶段利用检索增强生成（RAG）动态检索与当前查询最相关的修正案例作为少样本示例，引导模型逐步反思与修正错误。实验表明，该方法使 GPT-4o 在人类偏好数据集上的准确率从 41.7% 提升至 65.1%（+23.4 个绝对百分点），验证了“从错误中学习、无需训练”这一范式的有效性。

## 核心方法与创新机理

本工作提出 **Error Notebook + RAG** 框架，核心创新在于将 VLM 的错误推理转化为可复用的修正知识，通过检索增强生成实现训练自由（training-free）的推理能力跃升。以下从三个关键“变更槽”（changed slots）展开分析。

### 1. 从直接推理到自我修正推理轨迹

传统 VLM 直接推理（w/o E-Notebook）在面对 CAD 装配体元数据序列过长、非自然语言格式的瓶颈时，容易产生逻辑错误或幻觉。本方法的核心洞察是：**错误本身具有教学价值**。通过构建 Error Notebook，将模型初始的错误推理链（CoT）进行反思性修正，生成正确的推理轨迹 $R^{\mathrm{corr}}$：

$$R^{\mathrm{corr}} = R_{\mathrm{sub}}^{\mathrm{prev}} \oplus \mathrm{TR} \oplus R^{g}$$

该轨迹由三部分拼接而成：错误发生前的正确步骤前缀、定位并过渡错误的自然语言反思、以及从修正点至正确答案的推理步骤。这一设计将“犯错—纠错”的过程显式编码为结构化知识，而非简单丢弃错误输出。

### 2. 从固定少样本到动态 RAG 检索

标准少样本学习使用固定的两个示例（Standard Few-Shot），无法适配不同装配体的规范差异。本方法将 Error Notebook 作为外部知识库，在推理时通过 RAG 动态检索与当前查询规范最相似的修正案例作为少样本示例：

$$\{ e_{k_1}, \dots, e_{k_n} \} = \arg\max_{e_j \in \mathcal{E} \setminus \{e_{\mathrm{cur}}\}} \sin(S, S_j)$$

这一机制使模型能够“借鉴”历史上类似错误的修正经验，而非依赖泛化的固定模板。决定性证据表明，仅 Error Notebook 的存在即可带来 **+23.4 绝对准确率点**的提升（GPT-4o Omni，人类偏好数据集：41.7% → 65.1%），而示例数量从 1 增至 50 仅带来约 3 个点的边际增益（Non-CoT 组：49.4% → 52.7%），证明动态检索的“相关性”比“数量”更重要。

### 3. 从无验证到语法约束验证器

Error Notebook 的质量直接影响 RAG 检索的有效性。本方法引入 **GC（Grammar-Constraint）验证器**，对修正后的推理轨迹进行结构完整性过滤：检查是否存在“Final Answer:”行、预测文件名是否有效且属于当前装配体。这一轻量级验证器无需额外训练，却可在人类偏好数据集上进一步带来 **+4.5 准确率点**增益（GPT-4o Omni：65.1% → 66.8% w/ sGC），确保存入笔记本的修正案例具备可靠的结构化格式。

### 4. 二阶段流水线：从图像到描述的中间表征

与直接基于装配体图像推理的基线（仅 15.0% 总体准确率）相比，本方法采用二阶段 VLM 流水线：第一阶段为每个部件生成自然语言描述 $d_i = f_{\mathrm{desc}}(\mathcal{T}_{\mathrm{assembly}}, \mathcal{T}_{P_i}, \mathrm{prompt}_{\mathrm{desc}})$，第二阶段基于描述和规范进行检索推理。这一设计将 CAD 元数据的非自然语言瓶颈转化为 VLM 更擅长处理的自然语言中间表征，使总体准确率提升至 33.6%（+18.6 点），为 Error Notebook 的后续推理提供了更清晰的语义基础。

**创新本质总结**：Error Notebook + RAG 框架将 VLM 的“犯错—反思—修正”过程系统化为可检索、可迁移的推理知识，配合语法约束验证和二阶段描述流水线，在不进行任何模型微调的前提下，实现了对训练自由基线（标准少样本 26.6%、自一致性 38.9%）的显著超越（48.3%）。

![[assets/figures/papers/paper_list_l20_https_openreview_net_forum_id_JMweItBmbx/figures/002_Figure_2.jpg]]
*Figure 2: Overview of the (a) dataset construction pipeline and (b) Error Notebook + RAGbased inference process. (a) For each assembly, a VLM is used to generate concise and discriminative natural language descriptions for every part. Subsequently, the model generates assembly-level specification sentences describing the required relationship. To support human annotation, the specified parts are merged and visualized as a CAD model image. (b) Following the 1st VLM, at the 2nd stage, given the assembly specification, the system retrieves the most relevant examples from the Error Notebook according to the assembly specification, incorporates these as few-shot exemplars, and then performs step-by-step r...*

![[assets/figures/papers/paper_list_l20_https_openreview_net_forum_id_JMweItBmbx/figures/003_Figure_3.jpg]]
*Figure 3: Error Notebook construction. We define a corrected reasoning trajectory as the concatenation of: 1) all steps up to the first error, 2) a natural language reflection that pinpoints and transitions from the error, and 3) the corrected reasoning steps that ultimately yield the ground-truth answer. The proposed GC check is further employed to improve the quality of the Error Notebook*

本文提出一个**无训练的二阶段视觉语言模型（VLM）推理流水线**，其核心目标是从长序列、非自然语言格式的 CAD 装配体元数据中，依据自然语言规范检索出对应的符号化部件标识符。整体框架由离线构建阶段和在线推理阶段组成，如图 2 所示。

### 二阶段推理流水线

推理过程被形式化为两个顺序执行的 VLM 阶段：

**第一阶段：部件描述生成（1st VLM）**。给定装配体整体图像 $\mathcal{T}_{\mathrm{assembly}}$ 和每个部件 $P_i$ 的独立图像 $\mathcal{T}_{P_i}$，第一 VLM 为每个部件生成简洁且具有区分性的自然语言描述：

$$d_i = f_{\mathrm{desc}}(\mathcal{T}_{\mathrm{assembly}}, \mathcal{T}_{P_i}, \mathrm{prompt}_{\mathrm{desc}})$$

这一步骤将原本冗长、非自然的 CAD 元数据转化为紧凑的自然语言中间表示 $\mathcal{D} = \{d_1, \dots, d_N\}$，为后续推理提供了可被 VLM 有效处理的结构化语义锚点。

**第二阶段：规范感知的部件检索（2nd VLM）**。基于装配体图像 $\mathbb{Z}_{\mathrm{assembly}}$、部件描述集 $\mathcal{D}$ 和自然语言规范 $S$，第二 VLM 通过链式推理（Chain-of-Thought, CoT）检索出满足规范的目标部件集合：

$$\hat{\mathcal{P}}^* = f_{\mathrm{retr}}(\mathbb{Z}_{\mathrm{assembly}}, \mathcal{D}, S, \mathrm{prompt}_{\mathrm{retr}})$$

### 错误笔记本构建（离线）

框架的核心创新在于构建**错误笔记本（Error Notebook）**，其流程如图 3 所示。对于每个训练装配体实例，首先让 VLM 生成初始推理轨迹 $R^{\mathrm{prev}}$（通常包含错误），然后通过反思式修正生成正确的推理轨迹。修正轨迹 $R^{\mathrm{corr}}$ 被定义为三个部分的拼接：

$$R^{\mathrm{corr}} = R_{\mathrm{sub}}^{\mathrm{prev}} \oplus \mathrm{TR} \oplus R^{g}$$

其中 $R_{\mathrm{sub}}^{\mathrm{prev}}$ 是首次出错之前的所有正确推理步骤前缀，$\mathrm{TR}$ 是明确指出错误并引导修正的自然语言过渡短语，$R^{g}$ 是从修正点至真值答案的正确推理步骤。修正生成由以下函数完成：

$$R^{\mathrm{corr}} = f_{\mathrm{corr}}(\mathcal{T}_{\mathrm{assembly}}, \mathcal{D}, S, R^{\mathrm{prev}}, \mathcal{P}^{*\mathrm{(gt)}}, \mathrm{prompt}_{\mathrm{corr}})$$

为保障错误笔记本的质量，引入**语法约束验证器（GC Verifier）**对每条修正轨迹进行结构完整性检查：验证轨迹中是否存在以 "Final Answer:" 开头的行，且提取的部件文件名均属于当前装配体的合法部件集合。通过 GC 过滤的轨迹被存入错误笔记本库 $\mathcal{E}$，作为后续推理的知识源。

### RAG 增强推理（在线）

在线推理阶段采用检索增强生成（RAG）策略。对于新的装配体查询，系统基于当前规范 $S$ 与错误笔记本中各条目规范 $S_j$ 的相似度，检索 top-n 最相关的修正推理案例作为少样本示例：

$$\{ e_{k_1}, \dots, e_{k_n} \} = \arg\max_{e_j \in \mathcal{E} \setminus \{e_{\mathrm{cur}}\}} \sin(S, S_j)$$

检索到的示例被组装为少样本提示 $F$，与装配体图像、部件描述和规范一同输入第二 VLM，引导模型进行逐步推理并生成最终答案：

$$R = f_{\mathrm{rag}}(F, \mathcal{T}_{\mathrm{assembly}}, \mathcal{D}, S, \mathrm{prompt}_{\mathrm{main}})$$

### 关键设计决策

消融实验揭示了两个关键设计因素。首先，**二阶段流水线本身**已显著优于直接基于图像推理的基线：在总体准确率上，二阶段流水线达到 33.6%，而仅图像推理仅为 15.0%（图 A.2），验证了部件描述作为中间语义表示的有效性。其次，**错误笔记本中 CoT 推理轨迹的存在**比示例数量更为关键：对于复杂装配体（10-50 部件），包含 CoT 推理的示例始终优于仅含最终答案的示例（图 A.1），而将示例数量从 1 增加至 50 仅带来约 3 个百分点的边际增益（表 2）。这表明框架的性能瓶颈在于修正推理轨迹的质量（由 GC 验证器确保）和检索相关性，而非示例规模。

### 两阶段 VLM 推理流水线

本工作将部件检索形式化为一个两阶段 VLM 推理流水线，以应对 CAD 装配体元数据序列过长且非自然语言格式的核心瓶颈。

**阶段一：部件描述生成（1st VLM）**

第一阶段利用 VLM 为装配体中的每个部件生成简洁且具有区分性的自然语言描述。给定装配体图像 $\mathcal{T}_{\mathrm{assembly}}$ 和部件图像 $\mathcal{T}_{P_i}$，模型输出描述 $d_i$：

$$d_i = f_{\mathrm{desc}}(\mathcal{T}_{\mathrm{assembly}}, \mathcal{T}_{P_i}, \mathrm{prompt}_{\mathrm{desc}})$$

其中 $\mathrm{prompt}_{\mathrm{desc}}$ 为部件描述生成提示（详见 Figure A.3）。所有部件的描述构成描述集合 $\mathcal{D}$。这一阶段将非自然语言的 CAD 元数据转化为模型可理解的中间表示，为后续推理奠定基础。

**阶段二：规范感知的部件检索（2nd VLM）**

第二阶段基于生成的部件描述和自然语言规范 $S$ 进行推理检索。模型接收装配体图像 $\mathbb{Z}_{\mathrm{assembly}}$、部件描述集合 $\mathcal{D}$ 和规范 $S$，通过链式思维推理输出候选部件标识符：

$$\hat{\mathcal{P}}^* = f_{\mathrm{retr}}(\mathbb{Z}_{\mathrm{assembly}}, \mathcal{D}, S, \mathrm{prompt}_{\mathrm{retr}})$$

其中 $\mathrm{prompt}_{\mathrm{retr}}$ 为检索提示（详见 Figure A.6）。消融实验表明，该二阶段流水线（先部件描述后检索）显著优于直接仅图像推理的基线：总体准确率从 15.0% 提升至 33.6%（Figure A.2），验证了中间描述表示的关键作用。

---

### 错误笔记本构建

错误笔记本是本方法的核心创新，其构建过程包含三个关键环节：错误推理轨迹生成、修正推理轨迹构建、以及语法约束过滤。

**修正推理轨迹构建**

给定模型先前生成的推理轨迹 $R^{\mathrm{prev}}$ 和真实答案 $\mathcal{P}^{*(\mathrm{gt})}$，修正函数 $f_{\mathrm{corr}}$ 通过反思式精炼生成修正轨迹：

$$R^{\mathrm{corr}} = f_{\mathrm{corr}}(\mathcal{T}_{\mathrm{assembly}}, \mathcal{D}, S, R^{\mathrm{prev}}, \mathcal{P}^{*(\mathrm{gt})}, \mathrm{prompt}_{\mathrm{corr}})$$

其中 $\mathrm{prompt}_{\mathrm{corr}}$（详见 Figure A.5）指示模型执行三步操作：(1) 逐步跟随先前的推理 $R^{\mathrm{prev}}$；(2) 在遇到第一个逻辑或事实错误时停止，并显式阐述过渡；(3) 从错误点开始生成通向正确答案的修正推理。

修正轨迹的结构化定义为：

$$R^{\mathrm{corr}} = R_{\mathrm{sub}}^{\mathrm{prev}} \oplus \mathrm{TR} \oplus R^{g}$$

其中 $R_{\mathrm{sub}}^{\mathrm{prev}}$ 为首次错误之前的所有正确步骤前缀，$\mathrm{TR}$ 为指出并过渡错误的自然语言反思短语，$R^{g}$ 为从修正点至真实答案的正确推理步骤（Figure 3）。

**语法约束 (GC) 验证器**

为确保错误笔记本中推理轨迹的结构完整性，引入语法约束验证器。该验证器搜索以 `Final Answer:` 开头的行并提取预测文件名。一条推理轨迹被接受当且仅当：(1) 存在该行；(2) 至少提供一个文件名；(3) 所有文件名均存在于装配体的部件列表中。通过 GC 过滤，可剔除结构不完整的轨迹，提升错误笔记本的整体质量。实验表明，GC 验证器在人类偏好数据集上可进一步带来最高 +4.5 个准确率点增益。

---

### 基于 RAG 的推理

在推理阶段，采用检索增强生成策略，从错误笔记本中动态检索与当前查询最相关的修正推理案例作为少样本示例。

**相似性检索**

给定当前规范 $S$ 和错误笔记本 $\mathcal{E}$，通过最大化规范间的相似度检索 top-$n$ 最相关条目（排除当前实例以避免数据泄漏）：

$$\{ e_{k_1}, \dots, e_{k_n} \} = \arg\max_{e_j \in \mathcal{E} \setminus \{e_{\mathrm{cur}}\}} \sin(S, S_j)$$

其中 $\sin(\cdot, \cdot)$ 为 token 级别 Jaccard 相似度函数。消融实验表明，token 级别检索器比字符级别检索器略优（在自生成数据集上约 +2%，Table A.2）。

**RAG 推理**

检索到的示例 $F$ 作为少样本提示，与装配体图像、部件描述和规范一同输入主模型，生成最终答案：

$$R = f_{\mathrm{rag}}(F, \mathcal{T}_{\mathrm{assembly}}, \mathcal{D}, S, \mathrm{prompt}_{\mathrm{main}})$$

默认检索示例数 $k=2$。消融实验揭示了一个关键发现：增加检索示例数量对最终准确率影响较小（Non-CoT 组：1 示例 49.4% vs 50 示例 52.7%），真正驱动性能提升的核心因素是错误笔记本本身的存在（Table 2）。对于高部件数量的复杂装配体（10-50 部件），包含 CoT 推理的示例始终优于仅含最终答案的示例（Figure A.1），表明逐步推理轨迹对困难案例尤为关键。

## 实验与关键发现

### 核心发现

实验在两个数据集上验证了 Error Notebook + RAG 框架的有效性：自生成数据集（模型自动生成规范）和人类偏好数据集（人工标注偏好规范）。两个数据集均按装配体部件数量划分为四个难度组（<10、10–20、20–50、>50），以反映不同复杂度的挑战。

**主要结果（Table 1）** 表明，Error Notebook + RAG 在所有评估模型和装配复杂度上均带来一致的显著提升：

![[assets/figures/papers/paper_list_l20_https_openreview_net_forum_id_JMweItBmbx/figures/004_Table_1.jpg]]
*Table 1: Accuracy comparison of general models with and without Error Notebook-RAG integration on self-generated and human preference datasets. The best result is highlighted in bold. We divided the data from both datasets into 4 groups based on the number of parts in each assembly, reflecting the varying difficulty levels*

- **GPT-4o (Omni)** 在人类偏好数据集上从 41.7% 提升至 65.1%（**+23.4 个绝对百分点**），在自生成数据集上从 28.5% 提升至 48.3%（**+19.8 个百分点**）。
- **GPT-4o mini** 在人类偏好数据集上从 19.3% 提升至 35.4%（**+16.1 个百分点**）。
- **Gemini 2.0 Flash** 在人类偏好数据集上从 44.2% 提升至 56.8%（**+12.6 个百分点**）。

这些增益在不同模型间高度一致，表明 Error Notebook 框架具有模型无关的通用性，无需额外训练即可增强推理能力。

**GC 验证器的叠加效果**：在 Error Notebook 基础上引入语法约束（GC）验证器，GPT-4o Omni 在人类偏好数据集上的准确率进一步提升至 66.8%（**+4.5 个百分点**），说明过滤结构不完整的推理轨迹能有效提升笔记本质量。

### 消融实验

**1. 检索示例数量与 CoT 推理的影响（Table 2, Figure A.1）**

![[assets/figures/papers/paper_list_l20_https_openreview_net_forum_id_JMweItBmbx/figures/005_Table_2.jpg]]
*Table 2: Ablation study on the number of exemplars retrieved from the Error Notebook. We also analyze the effect of excluding explicit CoT reasoning in each exemplar. CoT Group indicates that each retrieved exemplar includes explicit step-by-step reasoning, while Non-CoT Group omits such reasoning in the exemplars and includes ground truth only. The data from both datasets are divided into four groups based on the number of parts in each assembly, reflecting varying difficulty levels*

消融实验考察了两个关键因素：从 Error Notebook 检索的少样本示例数量（1、5、10、20、50），以及示例中是否包含显式 CoT 推理。

- **示例数量的边际效应**：在 Non-CoT 组（仅含最终答案），自生成数据集上 1 个示例准确率为 49.4%，50 个示例为 52.7%，增幅仅约 3 个百分点。这表明性能提升的核心驱动因素是 Error Notebook 本身的存在，而非示例数量的简单堆叠。
- **CoT 推理的关键作用**：对于复杂装配体（10–50 部件），包含 CoT 推理的示例始终优于仅含最终答案的示例。但在使用 50 个含 CoT 示例时出现准确率下降，可能因提示过长干扰模型判断——这是一个值得关注的失败模式。
- **默认配置**：RAG 的 top-k 检索默认 k=2。

**2. 与训练自由基线的对比（Table 3）**

![[assets/figures/papers/paper_list_l20_https_openreview_net_forum_id_JMweItBmbx/figures/006_Table_3.jpg]]
*Table 3: Ablation comparison between training-free baselines and our proposed method*

在自生成数据集上，Error Notebook 方法达到 48.3% 总体准确率，显著优于：
- 标准少样本学习（2 个固定示例）：26.6%
- 自一致性（Self-Consistency）：38.9%

这表明 Error Notebook 的动态检索 + 修正推理策略远优于传统的固定少样本或多采样投票方法。

**3. 二阶段流水线的必要性（Figure A.2）**

二阶段 VLM 流水线（先部件描述后检索）总体准确率为 33.6%，而直接仅图像推理的基线仅为 15.0%。在 <10 部件的简单装配体中，差距最大（约 25 个百分点），验证了部件描述作为中间参考对推理的支撑作用。

**4. 检索器选择（Table A.2）**

Token 级别 Jaccard 相似度检索器在自生成数据集上比字符级别检索器略优（约 +2%），被采纳为默认检索器。

### 开源模型与跨模型蒸馏

**Qwen2-VL-2B-Instruct（Table 4）** 使用 GPT-4o 构建的 Error Notebook 进行跨模型蒸馏，在自生成数据集上达到 48.3% 总体准确率，接近 GPT-4o mini 的表现（差距约 4 个百分点）。然而，使用 Qwen2-VL-2B 自身构建的笔记本（gE-Notebook+sGC）仅达 8.4%，表明 Error Notebook 的构建质量高度依赖高性能专有 VLM，低性能模型构建的笔记本效果急剧下降。

### 效率分析（Table 5）

- **Error Notebook 构建**：每个装配体需多次 VLM 调用（部件描述生成 + 修正推理），平均耗时 78.32 秒（第一阶段），属于一次性离线开销。
- **推理延迟**：使用 Error Notebook + RAG 的推理平均耗时 6.50 秒，反低于不使用笔记本的 8.04 秒——这是因为检索到的修正示例引导模型生成更简洁的推理路径，减少了不必要的 token 消耗。
- **Token 使用量**：使用 Error Notebook 时，prompt token 从 967.7 增至 1,218.1（因引入少样本示例），但 completion token 从 235.4 降至 194.3，总 token 消耗基本持平。

### 局限性与失败模式

1. **高复杂度装配体**：对于 >50 部件的装配体，即使使用 Error Notebook，GPT-4o Omni 最高准确率仅约 21%，表明框架在极端复杂场景下仍有明显不足。
2. **示例过载**：当检索 50 个含 CoT 示例时准确率下降，提示过长可能引入噪声干扰模型判断。
3. **笔记本构建依赖**：Error Notebook 的质量高度依赖高性能 VLM（如 GPT-4o），低性能模型构建的笔记本效果有限，限制了框架在资源受限场景下的自主应用。
4. **泛化性未知**：当前验证仅限于 Fusion 360 Gallery 子集，对其他 CAD 格式或跨领域任务的适用性有待进一步检验。

![[assets/figures/papers/paper_list_l20_https_openreview_net_forum_id_JMweItBmbx/figures/013_Figure_6.jpg]]
*Figure 6: Figure A.2: Accuracy comparison between proposed pipeline and image-only reasoning. Performance is shown for the proposed pipeline, which leverages part descriptions as intermediate references, versus the one that directly reasons over images*

## 定位与知识库关联

### 1. 问题定位与核心瓶颈

本研究聚焦于 **3D CAD 装配体中基于自然语言规范的部件检索** 任务，其核心挑战在于：CAD 装配体的元数据序列（例如 STEP 文件中的部件标识符与层级关系）通常极长且为非自然语言格式，直接超出了通用视觉语言模型（VLM）的 token 限制，导致模型难以有效捕捉部件间的细粒度空间与功能关系。这一瓶颈在多部件复杂装配体中尤为突出。

该问题处于 **训练自由（training-free）VLM 推理** 与 **CAD 智能检索** 的交叉地带。传统方法或依赖于对 CAD 元数据的结构化解析（难以处理自然语言规范的模糊性），或直接使用 VLM 进行端到端推理（受限于元数据长度与格式）。本文提出的 Error Notebook + RAG 框架，本质上是一种 **推理时自适应（inference-time adaptation）** 策略，通过外部知识库增强 VLM 的逐步推理能力，而无需对模型本身进行任何微调。

### 2. 与训练自由基线的对比

论文将所提方法与以下训练自由基线进行了系统性对比：

- **Standard Few-Shot（标准少样本学习）**：使用固定的两个少样本示例进行推理。在自生成数据集上，该方法仅取得 26.6% 的整体准确率，而所提 Error Notebook 方法达到 48.3%（Table 3），表明静态示例无法提供有效的推理引导。
- **Self-Consistency（自一致性）**：通过多样本采样后多数投票来提升推理可靠性。该方法在自生成数据集上取得 38.9% 的准确率，仍显著低于 Error Notebook 方法的 48.3%（Table 3），说明单纯的采样策略无法弥补推理过程中的结构性错误。
- **w/o E-Notebook（直接 VLM 推理）**：不使用错误笔记本的直接 VLM 提示，作为主要基线。GPT-4o (Omni) 在人类偏好数据集上仅取得 41.7%，而加入 Error Notebook + RAG 后跃升至 65.1%（+23.4 个绝对准确率点，Table 1）。

上述对比揭示了一个关键因果机制：**错误笔记本中记录的修正推理轨迹，远比静态示例或简单投票更能引导模型进行正确的逐步反思与纠错**。

### 3. 方法谱系中的关键设计选择

所提框架由以下核心模块构成，每一模块对应一个关键的因果调节旋钮：

| 模块 | 基线做法 | 本文做法 | 因果作用 |
|------|----------|----------|----------|
| 推理轨迹 | 直接模型推理（可能含错） | 自我修正生成正确的 CoT 轨迹（Error Notebook） | 提供可复用的正确推理模板 |
| 少样本示例 | 固定示例或无示例 | 从 Error Notebook 中动态 RAG 检索相关修正案例 | 增强示例与当前查询的相关性 |
| 结构验证 | 无验证 | GC 验证器过滤结构不完整的轨迹 | 确保笔记本中轨迹的语法完备性 |
| 推理流水线 | 单阶段 VLM 直接检索 | 二阶段流水线：部件描述生成 → 规范感知检索 | 将长元数据转化为自然语言中间表示 |

**二阶段流水线**（Figure 2）是解决元数据过长问题的核心设计。第一阶段 VLM 将每个部件的 CAD 元数据转化为简洁的自然语言描述 $d_i$，第二阶段 VLM 基于这些描述进行规范感知的逐步推理。消融实验证实，该流水线相比直接仅图像推理的基线大幅提升准确率（33.6% vs 15.0%，Figure A.2）。

**Error Notebook 构建**（Figure 3）的核心洞察在于：VLM 的初始推理往往在某一步骤出错，但其后续步骤可能仍然合理。因此，修正轨迹 $R^{\mathrm{corr}}$ 被定义为正确前缀、过渡反思短语与修正后推理的拼接（Eq. 3），而非完全重写。这种“精准修正”策略保留了模型原本正确的推理部分，使笔记本中的示例更具教学价值。

**GC 验证器**（Section 2.4）通过检查“Final Answer:”行与有效部件文件名，过滤掉结构不完整的轨迹，进一步提升了笔记本质量。实验表明，GC 验证器可在人类偏好数据集上带来最高 +4.5 个准确率点增益（Table 1）。

### 4. 适用边界与局限

尽管 Error Notebook 框架在多个模型和数据集上展现了显著且一致的增益，其适用边界仍需审慎界定：

1. **装配体复杂度上限**：对于部件数量 >50 的高复杂装配体，即使使用 Error Notebook，GPT-4o (Omni) 的绝对准确率也仅约 21%（Table 1）。这表明当前框架在处理极端长序列和复杂空间关系时仍力有不逮。

2. **笔记本构建成本**：构建 Error Notebook 需要为每个装配体进行多次 VLM 调用（生成错误 CoT、修正、GC 过滤），带来一次性的计算与 token 开销（Table 5）。虽然该成本可在推理阶段分摊，但对于大规模装配体库，初始构建成本可能成为瓶颈。

3. **对高性能 VLM 的依赖**：Error Notebook 的构建依赖于高性能专有 VLM（如 GPT-4o）。使用低性能模型构建的笔记本效果显著下降（例如 Qwen2-VL-2B 自建笔记本仅 8.4% 准确率，Table 4）。跨模型蒸馏（使用 GPT-4o 构建的笔记本辅助 Qwen2-VL-2B 推理）可部分缓解此问题，使 2B 模型性能接近 GPT-4o mini（Table 4），但笔记本本身的质量上限仍由构建模型决定。

4. **领域泛化性未知**：当前框架仅在 Fusion 360 Gallery 子集上验证，对其他 CAD 格式（如 SolidWorks、CATIA）或非 CAD 领域的泛化性尚未探索。

### 5. 开放问题

论文中浮现出若干值得深入探究的开放问题：

- **示例数量与性能的倒 U 型关系**：消融实验（Table 2, Figure A.1）显示，对于复杂装配体（10-50 部件），使用 50 个含 CoT 示例时准确率反而下降。论文推测可能因提示过长干扰模型判断，但这一现象的确切机制（注意力分散？上下文冲突？）尚待阐明。

- **严格约束 vs 宽松约束的适用场景**：GC 验证器存在严格（sGC）与宽松（rGC）两种变体，它们在不同场景下的相对优势尚未被充分剖析。

- **跨领域迁移潜力**：Error Notebook 的核心思想——记录并检索修正后的推理轨迹作为少样本示例——理论上可迁移至任何需要逐步推理的 VLM 任务。其在 CAD 装配体之外的表现是一个值得探索的方向。

- **提示长度与推理质量的平衡**：如何在检索更多相关示例与保持提示简洁之间取得最优平衡，是一个尚未被系统解决的工程问题。

## 原文 PDF

![[paperPDFs/ICLR_2026/Error_Notebook_Guided_Training_Free_Part_Retrieval_in_3D_CAD_Assemblies_via_Vision_Language_Models.pdf]]
