---
title: "SCIEval: Evaluating and Benchmarking the Faithfulness of Scientific Image Generation and Interpretation with Large Multimodal Models"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/SCIEval_Evaluating_and_Benchmarking_the_Faithfulness_of_Scientific_Image_Generation_and_Interpretation_with_Large_Multimodal_Models.pdf
project_link: null
code_link: null
aliases:
- SCIEval
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/generative_models_diffusion
- topic/benchmarks_datasets_evaluation
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: 通过将忠实度分解为相关性（整体图文对齐）、准确性（细粒度科学细节）和可解释性（不忠实元素定位）三个可独立训练与评估的维度，并引入CLIP对比学习策略增强模型对科学视觉特征的感知。
primary_logic: 利用科学图像-文本对构建正负样本，通过跨模态与模态内对比学习训练CLIP编码器，使其能区分粗粒度相关性与细粒度准确性；再通过监督信号微调LMM生成可解释性理由，从而实现自动、无参考、细粒度的科学图像忠实度评估。
claims:
- SCIEval 在 Sci-T2I(CS) 子集上的 Spearman 相关性达到 74.1%，Pearson 相关性达到 73.2%，均优于所有24个竞争对手（含 GPT-4o）。
- 移除跨模态对比损失 L_CM 导致相关性从 74.1 降至 53.2（Spearman），证明跨模态对比学习是性能关键。
- SCIEval 生成的解释在人类评判中正确性达 4.7/5，完整性达 4.2/5，显著优于其他生成解释的方法。
- SCIEval-Bench Sci-T2I (CS) 上 Spearman/Pearson (%) = 74.1 / 73.2 (Relevance), 69.4 / 68.2 (Accuracy)
---

# SCIEval: Evaluating and Benchmarking the Faithfulness of Scientific Image Generation and Interpretation with Large Multimodal Models

> [!tip] 核心洞察
> 利用科学图像-文本对构建正负样本，通过跨模态与模态内对比学习训练CLIP编码器，使其能区分粗粒度相关性与细粒度准确性；再通过监督信号微调LMM生成可解释性理由，从而实现自动、无参考、细粒度的科学图像忠实度评估。

| 字段 | 内容 |
|------|------|
| 中文题名 | SCIEval：评估和基准测试大规模多模态模型在科学图像生成和解释中的忠实度 |
| 英文题名 | SCIEval: Evaluating and Benchmarking the Faithfulness of Scientific Image Generation and Interpretation with Large Multimodal Models |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://openaccess.thecvf.com/content/CVPR2026/html/Ye_SCIEval_Evaluating_and_Benchmarking_the_Faithfulness_of_Scientific_Image_Generation_CVPR_2026_paper.html) |
| Topic | #topic/vision_multimodal_applications #topic/generative_models_diffusion #topic/benchmarks_datasets_evaluation #topic/vision_multimodal_applications/image_and_video_generation |
| Method | SCIEval |
| Dataset | SCIEval-Bench Sci-T2I, SCIEval-Bench Sci-IC, SCIEval-Bench Rationale Quality |

> [!tip] 效果简介
> - SCIEval-Bench Sci-T2I (CS) 上，Spearman/Pearson (%) 74.1 / 73.2 (Relevance), 69.4 / 68.2 (Accuracy) vs GPT-4o: 60-65 (Figure 2); VALOR: 40-50; Qwen-VL: 30-40 (超过GPT-4o约10-14个百分点，超过其他指标30+个百分点)。
> - SCIEval-Bench Sci-IC (CS) 上，Spearman/Pearson (%) 75.9 / 75.6 (Relevance), 69.9 / 69.1 (Accuracy) vs GPT-4o: ~65; open-source best: ~40-45 (超过最强开源模型约30个百分点，超过GPT-4o约10个百分点)。
> - SCIEval-Bench Rationale Quality 上，Human 5-point: Correctness/Completeness 4.7 / 4.2 vs LLaVA-NeXT: 3.5 / 3.1; GPT-4o: 4.2 / 3.8 (estimated) (在正确性和完整性上均显著高于其他生成解释的方法)。

## 概要

### 1. 问题背景

科学图像（如折线图、柱状图、热力图、示意图）是学术论文中传递定量信息与复杂关系的核心载体。随着文本到图像（T2I）生成模型与图像描述（IC）模型在科学领域的快速渗透，如何自动评估生成内容与原始科学文本之间的**忠实度**成为一个紧迫但尚未充分解决的问题。现有评估指标（如**CLIP-Score**、**TIFA**、**VALOR-Eval**）主要针对自然图像设计，其瓶颈在于：缺乏对精确数值表示、细粒度对象属性（如坐标轴标签、数据点误差线）和空间关系的敏感性，且无法提供可解释的评估理由。这导致这些指标在科学场景下与人类判断的相关性显著不足，制约了科学图像生成模型的可靠迭代。

### 2. 核心方法

**SCIEval** 将忠实度分解为三个可独立训练与评估的维度：
- **相关性**：衡量图像与文本之间的整体图文对齐程度；
- **准确性**：考察图像中细粒度科学细节（数值、标签、趋势）的正确性；
- **可解释性**：定位并描述不忠实的元素，提供文本形式的评估理由。

为增强模型对科学视觉特征的感知，SCIEval 引入了一套基于 CLIP 的对比学习策略：利用科学图像-文本对构造正样本与硬负样本，通过跨模态对比损失（InfoNCE 形式）与模态内对比损失（Margin-based）联合训练图像编码器与文本编码器，使其能区分粗粒度相关性与细粒度准确性。在此基础上，通过监督信号微调一个大规模多模态模型（mPLUG-owl3）以生成可解释性理由，从而实现自动、无参考、细粒度的科学图像忠实度评估。

### 3. 关键结论

在包含 3000 个评估实例的 SCIEval-Bench 基准上，SCIEval 在文生图（Sci-T2I）和图像描述（Sci-IC）两个子任务上均显著优于 24 个竞争方法：
- **Sci-T2I(CS) 子集**：Spearman 相关性达到 74.1%，Pearson 相关性达到 73.2%，超过 GPT-4o 约 10–14 个百分点；
- **Sci-IC(CS) 子集**：Spearman 相关性 75.9%，Pearson 相关性 75.6%，超过最强开源模型约 30 个百分点；
- **解释质量**：人类评判中正确性达 4.7/5，完整性达 4.2/5，显著优于其他生成解释的方法。

消融实验进一步证实，**跨模态对比损失**是性能的关键驱动因素——移除该损失后，Sci-T2I 相关性 Spearman 从 74.1 骤降至 53.2。此外，仅使用 25% 的训练数据（8K 样本）仍能保持竞争性性能，表明方法具有较好的数据效率。

### 4. 方法谱系与知识库定位

SCIEval 位于**科学图像自动评估**这一新兴交叉领域，其方法谱系可沿以下维度定位：

| 维度 | 传统方法 | SCIEval 的改进 |
|------|----------|----------------|
| 评估粒度 | 单一整体分数（如 CLIP-Score） | 三维度解耦：相关性 + 准确性 + 可解释性 |
| 编码器训练 | 冻结预训练 CLIP | 对比学习微调（跨模态 + 模态内） |
| 负样本构造 | 随机负样本 | 对抗过滤生成硬负样本 + LMM 编辑生成细粒度负样本 |
| 可解释性 | 无解释 | 微调 LMM 生成显式不忠实理由 |

与现有工作的关系：
- **TIFA**（Hu et al., CVPR 2023）基于 VQA 评估忠实度，但问题模板依赖人工设计，难以覆盖科学图像的开放域细节；
- **VALOR-Eval**（Qiu et al., ACL 2024）利用多模态大模型评估图像描述，但未针对科学场景进行专门优化；
- **ALIGNScore**（Saxon et al., NeurIPS 2024）提供文本-图像对齐评分，但缺乏细粒度准确性判断与解释能力；
- **GPT-4o**（OpenAI, 2024）作为通用多模态大模型，在零样本评估中表现尚可，但相关性仍低于 SCIEval，且 API 调用成本远高于开源方案。

SCIEval 的核心贡献在于：首次系统地将科学图像忠实度评估分解为可独立优化的多维度框架，并通过任务对齐的对比学习策略将科学视觉知识注入 CLIP 编码器，从而在保持无参考、低成本优势的同时，实现了与人类判断高度一致的自动评估。

### 科学图像忠实度评估的独特挑战

科学图像（包括图表、曲线图、示意图等）是学术交流的核心载体，其与文本描述的一致性直接关系到科学信息的准确传递。然而，现有的忠实度评估指标主要针对自然图像设计，在面对科学图像时暴露出三个根本性缺陷：

**缺乏对精确数值表示的敏感性。** 科学图像中常包含精确的数值信息（如坐标轴刻度、数据点标签、统计量），这些细节的微小偏差在自然图像评估中无关紧要，但在科学场景下可能导致完全错误的解读。现有的 **CLIP-Score**（Hessel et al., EMNLP 2021）等基于全局语义对齐的指标无法捕捉此类细粒度偏差。

**无法感知细粒度对象属性与空间关系。** 科学图像中的对象（如曲线、柱状图、分子结构）具有严格的属性约束（颜色映射、线型、标记形状）和空间关系（相对位置、趋势方向）。基于VQA的方法如 **TIFA**（Hu et al., CVPR 2023）虽然引入了问答式评估，但其问题模板难以覆盖科学领域的专门化属性。

**缺乏可解释的评估理由。** 现有指标通常仅输出单一的整体忠实度分数，无法指出图像中哪些具体元素与文本描述不一致。这使得评估结果难以被人类理解和信任，也无法为生成模型的迭代改进提供可操作的反馈。尽管 **VALOR-Eval**（Qiu et al., ACL 2024）等基于多模态大模型的方法尝试生成解释，但其在科学领域的准确性和完整性仍远未满足需求。

### 现有方法的性能瓶颈

从图2（Figure 2）的性能等级对比中可以清晰看到这一瓶颈：即使是当前最强的通用多模态大模型 **GPT-4o**（OpenAI, 2024），在科学图像忠实度评估上的Pearson相关系数也仅达到0.60–0.65，而开源模型如 **Qwen-VL** 的表现更差（约0.30–0.40）。专用评估指标如 **ALIGNScore**（Saxon et al., NeurIPS 2024）虽有所改进，但仍受限于自然图像的设计范式，无法有效处理科学视觉特征。

**核心瓶颈**在于：现有方法缺乏对科学图像中精确数值表示、细粒度对象属性和空间关系的敏感性，且无法提供可解释的评估理由。这导致自动评估结果与人类专家判断之间存在显著差距，严重制约了科学图像生成和解释系统的可信度。

### 本文动机与核心思路

为填补上述缺口，本文提出 **SCIEval**——一个专为科学图像设计的忠实度评估框架。SCIEval的核心洞察在于：利用科学图像-文本对构建正负样本，通过跨模态与模态内对比学习训练CLIP编码器，使其能区分粗粒度相关性与细粒度准确性；再通过监督信号微调LMM生成可解释性理由，从而实现自动、无参考、细粒度的科学图像忠实度评估。

具体而言，SCIEval将忠实度分解为三个可独立训练与评估的维度（图3，Figure 3）：

- **相关性（Relevance）**：衡量图像与文本的整体对应程度，关注“图文是否在讨论同一主题”；
- **准确性（Accuracy）**：检验细粒度科学细节的精确匹配，关注“数值、属性、关系是否正确”；
- **可解释性（Explainability）**：定位并说明不忠实元素，提供“哪里不一致、为什么不一致”的文本理由。

这一三维度设计使得SCIEval能够同时支持文本到图像生成（Sci-T2I）和图像描述（Sci-IC）两种任务的统一评估（图1，Figure 1），突破了现有方法只能评估单一方向的局限。

## 核心方法与创新机理

SCIEval 的核心创新并非提出一个全新的评估范式，而是对“科学图像忠实度”这一概念进行了**维度解耦与可操作化**，并围绕解耦后的维度设计了针对性的训练策略。相较于现有工作，其关键变化槽位（changed slots）体现在以下四个层面。

### 从单一分数到三维度解耦评估

现有忠实度评估方法（如 **TIFA** (Hu et al., CVPR 2023)、**CLIP-Score** (Hessel et al., EMNLP 2021)、**ALIGNScore** (Saxon et al., NeurIPS 2024)）通常输出一个整体对齐分数，无法区分“图文大致相关”与“科学细节精确匹配”这两种不同性质的忠实度。SCIEval 将忠实度分解为三个可独立训练与评估的维度：

- **相关性（Relevance）**：衡量图像与文本的整体语义对应关系，即图文是否“在说同一件事”。
- **准确性（Accuracy）**：考察图像中的细粒度科学细节（如数值标签、曲线趋势、坐标轴刻度）是否与文本描述精确一致。
- **可解释性（Explainability）**：定位并描述不忠实的元素，以自然语言理由的形式输出。

这一解耦的因果机制在于：**相关性评估的是粗粒度语义对齐，准确性评估的是细粒度属性匹配，两者在特征空间中需要不同的判别边界**。Figure 3 通过颜色高亮直观展示了这一区分：一般性描述（蓝色）仅需相关性判断，科学化风格描述（红色）需要准确性校验，而未覆盖的描述（灰色）则属于不忠实。

### 从冻结编码器到对比学习微调的 CLIP 策略

现有基于 CLIP 的评估指标（如 CLIP-Score）直接使用冻结的预训练编码器，这些编码器主要面向自然图像训练，对科学图像中的精确数值表示和细粒度对象属性缺乏敏感性。SCIEval 的核心突破在于**利用正负样本对，通过跨模态与模态内对比学习联合微调 CLIP 编码器**，使其获得科学视觉特征的感知能力。

训练策略的关键设计包括：

- **跨模态对比损失 $\mathcal{L}_{CM}$**：采用 InfoNCE 形式，最大化对齐图文对 $(\mathbf{Z}_{I_T}, \mathbf{Z}_{C_T})$ 的相似度，同时最小化不对齐对 $(\mathbf{Z}_{I_T}, \mathbf{Z}_{C_F})$ 的相似度，迫使编码器学习图文间的细粒度对应关系。

$$
\mathcal{L}_{CM} = -\log \frac{\exp(s(\mathbf{Z}_{I_T}, \mathbf{Z}_{C_T})/\tau) + \exp(s(\mathbf{Z}_{I_F}, \mathbf{Z}_{C_F})/\tau)}{\exp(s(\mathbf{Z}_{I_T}, \mathbf{Z}_{C_T})/\tau) + \exp(s(\mathbf{Z}_{I_F}, \mathbf{Z}_{C_F})/\tau) + \exp(s(\mathbf{Z}_{I_T}, \mathbf{Z}_{C_F})/\tau) + \exp(s(\mathbf{Z}_{I_F}, \mathbf{Z}_{C_T})/\tau)}
$$

- **模态内对比损失 $\mathcal{L}_{IM}$**：采用 margin-based 损失，当正负样本特征相似度超过阈值时施加惩罚，增强编码器对同一模态内不同样本的区分能力。

$$
\mathcal{L}_{IM_v} = \max\{0, s(\mathbf{Z}_{I_T}, \mathbf{Z}_{I_F}) - \epsilon_v\}
$$

消融实验（Table 3）提供了决定性证据：**移除 $\mathcal{L}_{CM}$ 导致 Sci-T2I 相关性 Spearman 从 74.1 骤降至 53.2**，降幅高达 20.9 个百分点，证明跨模态对比学习是性能的关键因果旋钮。移除 $\mathcal{L}_{IM}$ 导致性能降至 64.4，降幅约 10 个百分点，表明模态内对比也贡献显著但相对次要。

### 从随机负样本到任务对齐的硬负样本构造

现有对比学习方法通常使用随机负样本，但这些负样本往往过于简单，无法提供有效的训练信号。SCIEval 针对两个评估维度设计了差异化的硬负样本构造策略（Figure 5）：

- **相关性负样本**：通过**对抗过滤（adversarial filtering）**生成——从数据集中检索与正样本图像语义相似但不完全匹配的标题 $C_R$，构成 $\langle I_T, C_R \rangle$ 对。这类负样本迫使编码器学习区分“大致相关”与“精确匹配”的边界。
- **准确性负样本**：通过 **LMM 编辑（targeted object modifications）**生成——对正样本标题中的特定科学对象进行定向修改（如替换数值、改变趋势描述），得到 $C_A$，构成 $\langle I_T, C_A \rangle$ 对。这类负样本迫使编码器关注细粒度科学细节的差异。

这种分层负样本构造策略使得 SCIEval-R 和 SCIEval-A 能够在各自维度上获得专门的判别能力。此外，SCIEval-A 的训练采用**顺序初始化策略**——复用 SCIEval-R 训练好的参数作为起点继续训练，消融实验表明这比独立训练效果更好，说明相关性知识可以迁移到准确性任务中。

### 从无解释到可解释的忠实度评估

现有评估方法仅输出分数，无法解释为何某个图文对不忠实。SCIEval 引入 **SCIEval-E 模块**，通过监督信号微调 LMM（mPLUG-owl3 8B），使其能生成不忠实元素的显式理由。训练数据中的理由标注基于正负样本的差异 $\text{diff}(C_T, C_A)$ 自动生成，无需额外人工标注。

人类评判结果（Table 2）显示，SCIEval 生成的解释在**正确性上达到 4.7/5，完整性达到 4.2/5**，显著优于 LLaVA-NeXT（3.5/3.1）和 GPT-4o（估计约 4.2/3.8），证明这一可解释性模块确实提供了有价值的诊断信息。

### 创新边界与局限

需要指出的是，SCIEval 的创新集中在**评估架构与训练策略**层面，而非基础模型架构的根本性突破。其三个模块均基于现有组件（CLIP 编码器、mPLUG-owl3 LMM），创新主要体现在如何将这些组件适配到科学图像忠实度评估这一特定任务。此外，SCIEval-E 的理由生成基于固定的负样本差异模板，可能无法涵盖所有不忠实情况类型，这一点需要在实际应用中加以注意。

SCIEval 的整体设计围绕一个核心洞察展开：科学图像的忠实度评估不能简化为单一的整体分数，而需要从**相关性（Relevance）**、**准确性（Accuracy）**和**可解释性（Explainability）**三个维度分别建模。这一三维分解构成了框架的顶层架构，如图4所示，整个系统通过两阶段对比学习与最终的有监督微调串联起三个功能模块。

### 训练数据构造：正负样本对生成

框架的起点是训练数据的构造。SCIEval 从 ArXivCap 等科学图像-文本数据集中采集真实对齐的图文对作为正样本 $\langle I_T, C_T \rangle$，然后通过两种策略生成两类负样本：

- **相关性负样本** $\langle I_T, C_R \rangle$：对正样本中的图像 $I_T$，通过对抗过滤（adversarial filtering）检索语义相似但整体不匹配的标题 $C_R$，构成粗粒度负样本对，用于训练模型区分整体图文对齐程度。
- **准确性负样本** $\langle I_T, C_A \rangle$：利用 LMM 对正样本标题 $C_T$ 进行细粒度的对象修改（targeted object modifications），生成仅在局部科学细节上存在差异的标题 $C_A$，构成细粒度负样本对，用于训练模型捕捉微观层面的不忠实。

同时，系统标注 $C_T$ 与 $C_A$ 之间的差异 $\text{diff}(C_T, C_A)$，作为后续可解释性模块的监督信号。完整的训练数据构造流程见图5。

### 两阶段对比学习：SCIEval-R 与 SCIEval-A

在训练数据准备完成后，框架进入两阶段对比学习阶段，分别训练相关性评估器 **SCIEval-R** 和准确性评估器 **SCIEval-A**。两个模块均基于 CLIP 编码器架构，但采用不同的训练目标和数据：

- **第一阶段（SCIEval-R）**：使用相关性正负样本对训练 CLIP 的图像编码器 $\text{CLIP}_v^R$ 和文本编码器 $\text{CLIP}_t^R$。训练目标由三部分损失函数组成：跨模态对比损失 $\mathcal{L}_{CM}$（InfoNCE 形式，最大化正样本图文对齐概率、最小化负样本对齐概率）、视觉模态内对比损失 $\mathcal{L}_{IM_v}$ 和文本模态内对比损失 $\mathcal{L}_{IM_t}$（均为基于余弦相似度的 margin-based 损失，阈值分别为 $\epsilon_v$ 和 $\epsilon_t$）。总损失函数为：

$$\mathcal{L} = \mathcal{L}_{CM} + \frac{1}{2}(\mathcal{L}_{IM_t} + \mathcal{L}_{IM_v})$$

其中跨模态对比损失的核心公式为：

$$\mathcal{L}_{CM} = -\log \frac{\mathcal{L}_{CM}^P}{\mathcal{L}_{CM}^P + \mathcal{L}_{CM}^N}$$

$$\mathcal{L}_{CM}^P = \exp(s(\mathbf{Z}_{I_T}, \mathbf{Z}_{C_T}) / \tau) + \exp(s(\mathbf{Z}_{I_F}, \mathbf{Z}_{C_F}) / \tau)$$

$$\mathcal{L}_{CM}^N = \exp(s(\mathbf{Z}_{I_T}, \mathbf{Z}_{C_F}) / \tau) + \exp(s(\mathbf{Z}_{I_F}, \mathbf{Z}_{C_T}) / \tau)$$

- **第二阶段（SCIEval-A）**：以第一阶段训练好的 $\text{CLIP}_v^R$ 和 $\text{CLIP}_t^R$ 参数初始化 $\text{CLIP}_v^A$ 和 $\text{CLIP}_t^A$，继续使用准确性正负样本对进行训练。消融实验证实，这种顺序训练策略（知识迁移）优于独立训练。

### 可解释性模块：SCIEval-E

前两个阶段训练完成后，框架进入第三阶段——可解释性模块 **SCIEval-E** 的有监督微调。该模块基于 LMM（mPLUG-owl3, 8B），使用三元组 $(I_T, C_A, \text{diff}(C_T, C_A))$ 作为监督信号进行微调。推理时，微调后的模型直接接收图像和待评估文本，生成关于不忠实元素的文本理由，明确指出哪些科学细节存在偏差。

### 端到端推理流程

在推理阶段，给定一个图像-文本对，SCIEval 的三个模块协同工作：
1. **SCIEval-R** 输出相关性分数，衡量整体图文对齐程度；
2. **SCIEval-A** 输出准确性分数，衡量细粒度科学细节的忠实度；
3. **SCIEval-E** 生成可解释性理由，定位具体的不忠实元素。

这一统一框架同时支持文本到图像生成（Sci-T2I）和图像描述（Sci-IC）两种评估场景，无需针对不同任务重新训练。

![[assets/figures/papers/paper_list_l2212_https_openaccess_thecvf_com_content_CVPR2026_html_Ye_SCIEval_Evaluating/figures/004_Figure_4.jpg]]
*Figure 4: The overall training process of SCIEval. Specifically,we first train both*

![[assets/figures/papers/paper_list_l2212_https_openaccess_thecvf_com_content_CVPR2026_html_Ye_SCIEval_Evaluating/figures/001_Figure_1.jpg]]
*Figure 1: ．Motivation illustration．Unlike previous metrics built for natural images,SCIEval is specifically designed for scientific visuals (we highlight textual scientific details in color).Moreover, it evaluates both text-to-image generation and image captioning within a unified framework.Instead of outputing a merged score, SCIEval provides fine-grained scores along with clear rationales*

SCIEval 的训练框架由三个核心模块构成：**相关性评估器 (SCIEval-R)**、**准确性评估器 (SCIEval-A)** 和**可解释性模块 (SCIEval-E)**。前两者共享基于 CLIP 的对比学习训练范式，后者则通过监督微调大语言模型实现理由生成。

### 训练数据构造

如图 5 所示，训练数据构造遵循四步流程：

1. **正样本**：从 ArXivCap 等科学图文数据集中采集原始对齐的图文对 $\langle I_T, C_T \rangle$，其中 $T$ 表示 True。
2. **相关性负样本**：通过对抗过滤（adversarial filtering）生成 $\langle I_T, C_R \rangle$，即保留真实图像但替换为语义相似但不匹配的文本，形成粗粒度负样本。
3. **准确性负样本**：利用 LMM 对图像进行定向对象修改（targeted object modifications），生成 $\langle I_F, C_T \rangle$ 和 $\langle I_T, C_A \rangle$，其中 $F$ 表示 False，$A$ 表示 Altered。这类负样本聚焦于细粒度科学细节的偏差。
4. **理由标注**：记录 $C_T$ 与 $C_A$ 之间的差异 $\text{diff}(C_T, C_A)$，作为 SCIEval-E 的监督信号。

### 对比学习损失函数

SCIEval-R 和 SCIEval-A 采用统一的对比学习策略，包含模态内损失和跨模态损失两部分，总训练目标为：

$$\mathcal{L} = \mathcal{L}_{CM} + \frac{1}{2}(\mathcal{L}_{IM_t} + \mathcal{L}_{IM_v}) \tag{Equation 6}$$

#### 模态内对比损失 $\mathcal{L}_{IM}$

模态内损失旨在增强模型区分同一模态内不同样本的能力，采用基于余弦相似度的 Margin-based 损失：

**视觉模态内损失**：
$$\mathcal{L}_{IM_v} = \max\{0, s(\mathbf{Z}_{I_T}, \mathbf{Z}_{I_F}) - \epsilon_v\} \tag{Equation 1}$$

**文本模态内损失**：
$$\mathcal{L}_{IM_t} = \max\{0, s(\mathbf{Z}_{C_T}, \mathbf{Z}_{C_F}) - \epsilon_t\} \tag{Equation 2}$$

其中 $s(\cdot, \cdot)$ 表示余弦相似度，$\mathbf{Z}_{I_T}$ 和 $\mathbf{Z}_{I_F}$ 分别为正样本图像特征与负样本图像特征，$\mathbf{Z}_{C_T}$ 和 $\mathbf{Z}_{C_F}$ 为对应的文本特征。$\epsilon_v$ 和 $\epsilon_t$ 为预设阈值，当正负样本相似度超过阈值时施加惩罚，推动负样本远离正样本。

#### 跨模态对比损失 $\mathcal{L}_{CM}$

跨模态损失采用 InfoNCE 形式，旨在增强模型区分对齐与未对齐图文对的能力：

**正样本项**（对齐图文对的指数相似度之和）：
$$\mathcal{L}_{CM}^P = \exp(s(\mathbf{Z}_{I_T}, \mathbf{Z}_{C_T}) / \tau) + \exp(s(\mathbf{Z}_{I_F}, \mathbf{Z}_{C_F}) / \tau) \tag{Equation 3}$$

**负样本项**（不对齐图文对的指数相似度之和）：
$$\mathcal{L}_{CM}^N = \exp(s(\mathbf{Z}_{I_T}, \mathbf{Z}_{C_F}) / \tau) + \exp(s(\mathbf{Z}_{I_F}, \mathbf{Z}_{C_T}) / \tau) \tag{Equation 4}$$

**总体跨模态损失**：
$$\mathcal{L}_{CM} = -\log\frac{\mathcal{L}_{CM}^P}{\mathcal{L}_{CM}^P + \mathcal{L}_{CM}^N} \tag{Equation 5}$$

其中 $\tau$ 为温度系数，控制 softmax 分布的锐度。该损失函数本质上是最大化正样本对齐概率，同时最小化负样本对齐概率。

### 模块训练流程

如图 4 所示，训练分为三个阶段：

1. **第一阶段**：使用上述对比学习损失训练 SCIEval-R 的视觉编码器 $\text{CLIP}_v^R$ 和文本编码器 $\text{CLIP}_t^R$，使其具备科学图文的粗粒度相关性判别能力。

2. **第二阶段**：以 SCIEval-R 的参数初始化 SCIEval-A 的编码器 $\text{CLIP}_v^A$ 和 $\text{CLIP}_t^A$，继续使用准确性负样本进行训练。这种顺序训练策略实现了从相关性知识到准确性知识的有效迁移（消融实验证实该初始化方式优于独立训练）。

3. **第三阶段**：SCIEval-E 微调 mPLUG-owl3 (8B)，以三元组 $(I_T, C_A, \text{diff}(C_T, C_A))$ 作为监督信号，使模型在推理时能直接生成不忠实元素的文本理由。

### 评估指标公式

SCIEval 使用 Spearman 和 Pearson 相关系数衡量自动评分与人工判断之间的一致性：

**Spearman 秩相关系数**：
$$S = 1 - \frac{6\sum_{i=1}^{m} x_i^2}{m(m^2 - 1)}$$

其中 $x_i = r_{a_i} - r_{h_i}$，$r_{a_i}$ 和 $r_{h_i}$ 分别表示自动评分 $a_i$ 和人工评分 $h_i$ 的排序位置。

**Pearson 线性相关系数**：
$$P = \frac{\sum_{i=1}^{m} (a_i - \bar{a})(h_i - \bar{h})}{\sqrt{\sum_{i=1}^{m} (a_i - \bar{a})^2 \sum_{i=1}^{m} (h_i - \bar{h})^2}}$$

其中 $\bar{a}$ 和 $\bar{h}$ 分别为自动评分和人工评分的均值。

## 实验与关键发现

### 主实验结果：忠实度评分与人类判断的相关性

SCIEval 在 SCIEval-Bench 的两个核心任务上与人类判断表现出强相关性，全面超越现有 24 个对比方法。**Table 1** 汇总了各方法在 Sci-T2I（文本到图像生成评估）和 Sci-IC（图像描述评估）任务上的 Spearman/Pearson 相关系数。

![[assets/figures/papers/paper_list_l2212_https_openaccess_thecvf_com_content_CVPR2026_html_Ye_SCIEval_Evaluating/figures/007_Table_1.jpg]]
*Table 1: Performancecomparisonon SCIEval-Bench.Withineach methodblock,the highestvaluepercolumnis highlightedincolor*

![[assets/figures/papers/paper_list_l2212_https_openaccess_thecvf_com_content_CVPR2026_html_Ye_SCIEval_Evaluating/figures/002_Figure_2.jpg]]
*Figure 2: Comparisonsbetwenrelated worksandSCIEval.Here,GTstands forground-truth.Forvarious methodcategories,wecompare their performances based on our experiment results (e.g.,Pearson corelation coefficients reported in Table 1)*

在 **Sci-T2I (CS)** 子集上，SCIEval 的相关性评分达到 **74.1% / 73.2%**（Spearman/Pearson），准确性评分达到 **69.4% / 68.2%**。相比之下，GPT-4o 的相关性评分仅为 60–65（**Figure 2**），而专用评估指标如 VALOR-Eval（Qiu et al., ACL 2024）的相关性约 40–50，Qwen-VL 约 30–40。SCIEval 的优势幅度超过 GPT-4o 约 10–14 个百分点，超过其他指标 30 个百分点以上。

在 **Sci-IC (CS)** 子集上，SCIEval 的相关性评分达到 **75.9% / 75.6%**，准确性评分达到 **69.9% / 69.1%**，同样显著优于 GPT-4o（约 65）和最强开源模型（约 40–45），领先幅度约 10 和 30 个百分点。

### 解释质量评估

SCIEval-E 模块生成的忠实度解释在人类评判中表现优异。**Table 2** 显示，SCIEval 生成的解释在正确性上得分为 **4.7/5**，完整性上得分为 **4.2/5**，显著高于 LLaVA-NeXT 的 3.5/3.1 和 GPT-4o 的约 4.2/3.8。这表明 SCIEval 不仅能给出准确的分数，还能提供高质量、可解释的不忠实元素定位理由。

![[assets/figures/papers/paper_list_l2212_https_openaccess_thecvf_com_content_CVPR2026_html_Ye_SCIEval_Evaluating/figures/008_Table_2.jpg]]
*Table 2: The results of rationale quality assessment*

### 消融实验

**Table 3** 在 CS 子集上进行了系统的消融研究，揭示了各组件对性能的因果贡献。

- **跨模态对比损失是关键瓶颈。** 移除跨模态对比损失 $L_{CM}$ 后，Sci-T2I 相关性 Spearman 从 74.1 骤降至 53.2，降幅达 20.9 个百分点。这证明跨模态对齐是 SCIEval 性能的核心驱动力。
- **模态内对比损失提供中等增益。** 移除模态内对比损失 $L_{IM}$ 后，相关性降至 64.4，表明模态内区分能力对细粒度评估有辅助作用，但非决定性因素。
- **顺序训练优于独立训练。** 将 SCIEval-R 的参数用于初始化 SCIEval-A（即先训练相关性模块，再继续训练准确性模块）比独立训练效果更好，表明两个任务之间存在有效的知识迁移。
- **数据效率良好。** 仅使用 25% 的训练数据（8K 样本）时，相关性仍保持 58.2/58.0 的竞争性水平，且性能随数据量增加而持续提升。

### 失败模式与局限性

尽管 SCIEval 在整体指标上表现优异，仍存在以下限制：

1. **多面板图形未覆盖。** 当前评估仅针对单一科学图像，未扩展到多面板、多层次嵌套的科学可视化（如多子图对比图、流程图）。
2. **解释模板的覆盖范围有限。** SCIEval-E 的理由生成基于固定的负样本差异模板，可能无法涵盖所有类型的不忠实情况。
3. **领域泛化风险。** 训练数据来源于 ArXivCap 等预出版论文，对完全未见领域的科学图像泛化能力可能受限。
4. **标注偏差。** 人工标注者仅为 CS 博士生，可能引入领域偏差；基准构建花费约 1200 美元，成本较高。

### 关键图表结论

- **Figure 2**：以 Pearson 相关系数为指标，直观展示 SCIEval 相较于各类基准方法（LMMs、专用指标、基于 CLIP 的指标）的性能优势层级。
- **Table 1**：完整呈现 SCIEval 在 Sci-T2I 和 Sci-IC 两个任务、多个领域子集上的 Spearman/Pearson 评分，证明其跨领域鲁棒性。
- **Table 2**：量化验证 SCIEval-E 解释质量，确认其正确性和完整性均优于其他生成解释的方法。
- **Table 3**：通过消融实验锁定跨模态对比损失为性能核心瓶颈，并验证数据规模和训练顺序的影响。

![[assets/figures/papers/paper_list_l2212_https_openaccess_thecvf_com_content_CVPR2026_html_Ye_SCIEval_Evaluating/figures/010_Table_3.jpg]]
*Table 3: Ablation studies on the CS subset*

## 定位与知识库关联

### 1. 方法定位与基线关系

SCIEval 处于**科学图像忠实度自动评估**这一新兴交叉领域，其核心贡献在于将评估从单一整体分数解耦为**相关性（Relevance）、准确性（Accuracy）、可解释性（Explainability）** 三个可独立训练与评估的维度。这一设计直接回应了现有指标的三个结构性缺陷：

- **自然图像指标的领域盲区**：**CLIP-Score**（Hessel et al., EMNLP 2021）、**ALIGNScore**（Saxon et al., NeurIPS 2024）等通用图文对齐指标缺乏对科学图像中精确数值、细粒度对象属性（如坐标轴标签、数据点分布）的敏感性。SCIEval 通过引入科学领域正负样本对进行对比学习微调 CLIP 编码器，弥补了这一感知鸿沟。

- **VQA 式指标的粒度不足**：**TIFA**（Hu et al., CVPR 2023）通过问答准确率评估忠实度，但问题生成依赖模板，难以覆盖科学图像中开放式的细节错误。SCIEval 的准确性模块直接学习细粒度差异的嵌入表示，避免了问题设计的瓶颈。

- **通用 LMM 评估的可解释性缺失**：**GPT-4o**（OpenAI, 2024）、**Qwen-VL** 等模型虽可输出评分，但缺乏对不忠实元素的显式定位。SCIEval-E 通过监督信号微调 **mPLUG-owl3 (8B)**，直接生成差异理由，使评估结果具备可追溯性。

从性能谱系看（Figure 2），现有方法可大致分为三个梯队：专用评估指标（如 VALOR-Eval, Qiu et al., ACL 2024）通常处于中低相关性区间（Pearson 约 0.40–0.50）；通用 LMM（如 GPT-4o）处于中高区间（约 0.60–0.65）；SCIEval 在 Sci-T2I(CS) 上达到 Pearson 0.732（相关性）和 0.682（准确性），在 Sci-IC(CS) 上达到 0.756 和 0.691，均显著超越所有 24 个竞争对手（Table 1）。

### 2. 因果机制与关键设计选择

SCIEval 的性能优势可归因于三个因果性设计选择，消融实验（Table 3）提供了直接证据：

| 消融项 | Sci-T2I 相关性 Spearman | 降幅 | 因果解释 |
|--------|------------------------|------|----------|
| 完整模型 | 74.1 | — | 基准 |
| 移除跨模态对比损失 $L_{CM}$ | 53.2 | −20.9 | 跨模态对齐是区分相关性与非相关性的核心机制 |
| 移除模态内对比损失 $L_{IM}$ | 64.4 | −9.7 | 模态内区分能力对细粒度准确性贡献显著 |
| 仅用 25% 训练数据 (8K) | 58.2 | −15.9 | 数据规模与性能正相关，但 8K 已具竞争力 |

**跨模态对比损失 $L_{CM}$** 是性能的关键瓶颈。其 InfoNCE 形式（Equation 5）强制模型在嵌入空间中拉近对齐图文对、推远不对齐对，这直接对应相关性评估的核心需求。移除该损失后性能骤降 20.9 个 Spearman 点，表明科学图像的语义对齐高度依赖跨模态交互建模。

**负样本构造策略**是另一个隐性关键因素。SCIEval 采用对抗过滤生成相关性负样本（检索相似但不匹配的文本），以及基于 LMM 编辑的准确率负样本（针对性修改对象属性），而非随机负采样。这一设计使得训练信号集中在模型最易混淆的边界区域，提升了评估器对细粒度错误的敏感性。

**顺序训练策略**（SCIEval-R 参数初始化 SCIEval-A）实现了知识迁移：相关性评估学到的通用科学视觉特征为准确性评估提供了良好的初始化，独立训练效果显著较差（Table 3）。

### 3. 适用边界与局限

根据论文自述的分析，SCIEval 的适用边界存在以下约束：

- **图像类型边界**：当前仅针对单一科学图像（如单张图表、示意图），尚未扩展到多面板（multi-panel）、多层次嵌套的科学可视化。论文明确将此列为未来工作方向。

- **解释模板的覆盖度**：SCIEval-E 的理由生成基于固定的负样本差异模板（$\text{diff}(C_T, C_A)$），可能无法涵盖所有不忠实情况类型，特别是训练数据中未出现的错误模式。

- **领域泛化风险**：训练数据来源于 ArXivCap 等预出版论文，以计算机科学、生物学、经济学、物理学等学科为主。对完全未见过领域的科学图像（如化学结构式、地质剖面图），泛化能力未经验证，需谨慎使用。

- **标注偏差**：SCIEval-Bench 的人工标注者仅为计算机科学博士生，可能引入领域偏差。尽管标注者间一致性较高（Spearman 相关性 0.78，Kappa 准确性 0.79），但该偏差的方向和程度未被量化分析。

- **成本与速度权衡**：SCIEval 训练需约 2.5 小时（四块 NVIDIA RTX 3090），推理约 0.5 小时处理 3000 样本，远低于 GPT-4o 的 API 调用成本，但仍需 GPU 资源。在极低资源场景下的部署方案尚未探索。

### 4. 开放问题与未来方向

论文提出的开放问题指向三个潜在研究方向：

1. **复杂科学图形的评估扩展**：如何将三维度框架适配到多面板图、流程图、蛋白质结构图等更复杂的科学可视化类型？这可能需要重新定义“准确性”的粒度，或引入结构感知的编码器。

2. **评估信号的反哺优化**：SCIEval 产生的分数与理由能否作为强化学习奖励，直接优化生成式 LMM 以提高科学图像创作的忠实度？这涉及将评估器的嵌入空间梯度传递回生成模型的技术挑战。

3. **无监督/自监督降本**：在极低资源或无标注场景下，SCIEval 能否通过无监督或自监督方式进一步降低对人工标注的依赖？当前框架依赖正样本对和编辑后的负样本，完全无监督的替代方案尚不明确。

4. **规模效应的边际收益**：使用更大的 CLIP 模型（如 ViT-L/14 替代 ViT-B/32）或更强的 LMM 是否会带来边际效益？当前实验未对此进行消融，速度与准确性的帕累托前沿有待刻画。

## 原文 PDF

![[paperPDFs/CVPR_2026/SCIEval_Evaluating_and_Benchmarking_the_Faithfulness_of_Scientific_Image_Generation_and_Interpretation_with_Large_Multimodal_Models.pdf]]
