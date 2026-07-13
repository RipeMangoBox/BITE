---
title: "Through the Lens of Contrast: Self-Improving Visual Reasoning in VLMs"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/Through_the_Lens_of_Contrast_Self_Improving_Visual_Reasoning_in_VLMs.pdf
project_link: null
code_link: https://github.com/zhiyupan42/VC-STaR
openreview_forum_id: ZymCPON45y
aliases:
- VSVCSTR
- TLCSIVRV
tags:
- ICLR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/vision_models_multimodal
core_operator: "引入精心构造的对比视觉问答对（对比VQA对，两张视觉相似但细节不同的图像配合同义问题），激发VLM进行细粒度对比分析，将多图对比的精确视觉辨别能力迁移到单图推理中，从而纠正原有推理中的视觉幻觉。"
primary_logic: "VLM在进行图像对比时能够更准确地提取和区分视觉信息，其内在的对比能力可被重新利用来主动抑制自身的视觉幻觉，使自我改进视觉推理成为可能，无需额外奖励模型或人工分解步骤。"
claims:
- "对比条件下的VLM能更好地纠正视觉幻觉：在失败案例中，对比+提示（C&H）相比仅提示（H）能纠正更多错误（图1b）。"
- "VC-STaR在六个具有挑战性的基准上平均提升2.6个百分点，尤其在幻觉基准MMVP和Hallusion上分别提升5.7%和3.2%，超过所有自改进基线。"
- "仅保留中等难度样本用于生成推理路径是有效的策略，加入简单样本反而导致性能下降。"
- "负面对比（答案不同）比正面对比（答案相同）在改善视觉推理方面更为有效，两者组合可带来最优增益。"
---

# Through the Lens of Contrast: Self-Improving Visual Reasoning in VLMs

> [!tip] 核心洞察
> VLM在进行图像对比时能够更准确地提取和区分视觉信息，其内在的对比能力可被重新利用来主动抑制自身的视觉幻觉，使自我改进视觉推理成为可能，无需额外奖励模型或人工分解步骤。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 透过对比之镜：视觉语言模型的自我改进视觉推理 |
| 英文题名 | Through the Lens of Contrast: Self-Improving Visual Reasoning in VLMs |
| 会议/期刊 | ICLR 2026 (Oral) |
| Links | [paper](https://openreview.net/forum?id=ZymCPON45y) · [GitHub](https://github.com/zhiyupan42/VC-STaR) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/vision_models_multimodal |
| Method | VC-STaR (Visual Contrastive Self-Taught Reasoner) |
| Dataset | MMVP, Hallusion, MathVista, MathVision |

> [!tip] 效果简介
> - MMVP 上，Acc. 为 75.7，对比 70.0，变化 +5.7。
> - Hallusion 上，Acc. 为 56.3，对比 53.1，变化 +3.2。
> - MathVista 上，Acc. 为 69.7，对比 68.4，变化 +1.3。

## 概要

视觉语言模型（VLM）在视觉推理任务中常因**视觉幻觉**而产生错误推理——模型可能“看到”图像中并不存在的物体或属性，并将这些虚假信息编织进推理链中。现有的自改进推理方法（如 **STaR**，Zelikman et al., NeurIPS 2022）在文本域中通过正确答案提示来提升推理质量，但在视觉域中面临根本性瓶颈：**正确答案提示无法有效验证和修复推理路径中的视觉幻觉**，导致错误推理或虚假视觉依据被保留甚至放大。

本文的核心发现是：**VLM 在进行图像对比时能够更准确地提取和区分视觉信息**。当面对一对视觉相似但细节不同的图像，并配合同义问题时，VLM 被迫进行细粒度对比分析，其内在的对比能力可被重新利用来主动抑制自身的视觉幻觉。基于这一洞察，本文提出 **VC-STaR（Visual Contrastive Self-Taught Reasoner）**，一种无需额外奖励模型或人工分解步骤的自我改进视觉推理方法。

VC-STaR 的核心机制包含三个关键设计：
- **对比 VQA 对构建**：通过多模态嵌入相似度搜索和难度采样，自动构建视觉相似、问题同义但答案可能不同的对比 VQA 对，作为激发对比能力的“对照镜”。
- **三阶段推理精炼**：先让 VLM 生成带幻觉的初步推理（思考步骤），再将其与对比样本一同输入生成对比分析（对比步骤），最后利用大语言模型基于对比分析重写推理路径以修正视觉幻觉（反思步骤）。
- **中等难度采样**：仅保留中等难度的对比对用于推理生成，简单样本的加入反而导致性能下降，验证了难度筛选的必要性。

在六个具有挑战性的基准上，VC-STaR 平均提升 **2.6 个百分点**，尤其在幻觉基准 MMVP 和 Hallusion 上分别提升 **5.7%** 和 **3.2%**，超过所有自改进基线。该方法在 Qwen2.5VL-3B 和 InternVL2.5-8B 上也表现出显著增益，具有良好的模型架构泛化性。



视觉语言模型（VLMs）在视觉问答、数学推理、图表理解等多模态任务中展现出令人瞩目的能力，但其推理过程常受**视觉幻觉**困扰——模型生成的推理路径中掺杂与图像事实不符的描述或判断，导致最终答案错误。这种幻觉现象在需要细粒度视觉辨别的场景中尤为突出，例如区分两张外观高度相似但细节不同的图像，或准确定位图中的微小文字与符号。

现有提升VLM推理质量的方法大致分为两类：一类是构建高质量视觉推理数据集进行监督微调，如**LLaVA-CoT**（Xu et al., 2025）、**R1-Onevision**（Yang et al., 2025b）等；另一类是自改进方法，让模型通过自我验证或反馈迭代优化推理路径，典型代表包括**STaR**（Zelikman et al., NeurIPS 2022）、**Verifier**（Lu et al., 2024a）和**Feedback**（Qu et al., 2024）。然而，这两类方法均存在一个根本性瓶颈：**它们无法有效验证并修复视觉推理路径中的视觉幻觉**。文本域的自改进方法（如STaR）仅利用正确答案作为提示重新生成推理，但正确答案本身并不包含视觉纠错信息，因此错误的视觉依据可能被保留甚至放大，导致模型在幻觉基准上表现不佳。

本文的核心洞察源自一个反直觉的观察：**VLM在进行图像对比时，其视觉辨别能力显著优于单图推理**。如图1所示，当VLM面对两张视觉相似但细节不同的图像并配合同义问题时（即“对比VQA对”），模型能够更准确地提取和区分视觉信息，从而纠正原本在单图推理中产生的幻觉。这一现象揭示了VLM内在的对比能力可被重新利用，作为抑制自身视觉幻觉的自我监督信号，使**无需额外奖励模型或人工分解步骤的自我改进视觉推理**成为可能。

基于上述动机，本文提出**VC-STaR**（Visual Contrastive Self-Taught Reasoner），通过构造对比VQA对激发模型的细粒度对比分析能力，并将多图对比的精确视觉辨别迁移到单图推理中，系统性地纠正推理路径中的视觉幻觉。



## 核心方法与创新机理

VC-STaR 的核心创新在于**将VLM内在的跨图像对比辨别能力重新定向为单图推理的自我纠错机制**，从而在不依赖外部奖励模型或人工分解步骤的前提下，系统性地抑制视觉幻觉。这一设计直接回应了现有文本域自改进方法（如STaR, Zelikman et al., NeurIPS 2022）的根本瓶颈：仅凭正确答案提示（hints）重新生成推理路径，无法有效验证和修复推理中出现的视觉幻觉，导致错误推理或不准确的视觉依据被保留甚至放大。

### 关键机制：对比驱动的推理精炼

VC-STaR 通过三个关键环节实现上述创新，每个环节均对应一个与基线方法相比发生实质性改变的“方法槽位”（changed slots）：

**1. 推理路径生成策略：从“提示重生成”到“对比-反思”双阶段纠错**

传统自改进方法（如STaR）仅利用正确答案作为提示，让VLM重新生成单图推理路径。此范式缺乏对视觉内容的验证机制，无法纠正已产生的视觉幻觉。VC-STaR 引入一个**对比-反思双阶段流程**（Figure 4）：
- **对比步骤（Contrasting Step）**：将目标样本与其对比VQA对一同输入VLM，生成细粒度的对比分析 $c_i$。该步骤利用了VLM在图像对比时能更准确提取和区分视觉信息的内在特性（Figure 1b 显示，对比+提示（C&H）相比仅提示（H）能纠正更多初始失败案例）。
- **反思步骤（Rethinking Step）**：大语言模型基于对比分析 $c_i$ 对原始推理路径 $r_i$ 进行重写，修正视觉幻觉，生成精炼推理路径 $\tilde{r}_i$。

这一策略的本质是将**多图对比的精确视觉辨别能力迁移到单图推理中**，使VLM能够主动审视并纠正自身推理中的视觉依据错误。

**2. 训练数据筛选：从“全量使用”到“基于相似度搜索与难度采样的三阶段筛选”**

基线方法通常使用所有可获得的VQA数据生成推理路径。VC-STaR 则设计了一个任务无关的**对比VQA对构建管道**（Figure 3），包含三个阶段：
- **多源数据收集**：从通用VQA、推理、数学、图表和OCR等多个领域收集数据。
- **基于多模态嵌入的相似度搜索**：构建基于ID的视觉度量学习嵌入模型，在语义和视觉两个维度上搜索相似样本，确保对比对满足“同义问题、视觉相似图像、推理依赖型问题”三个关键属性。筛选条件为视觉嵌入余弦距离 $\gamma(e_i^v, e_j^v) < \phi_v$ 且问题嵌入余弦距离 $\gamma(e_i^q, e_j^q) < \phi_q$。
- **难度采样过滤**：仅保留中等难度的对比VQA对用于生成推理数据。消融实验（Table 3）证实，加入简单样本反而导致性能下降（如Hallusion上+20k简单样本下降4.1个百分点），验证了难度采样的必要性。

**3. 视觉信息对齐方式：从“无跨图像对齐”到“跨图像对比注入细粒度视觉信息”**

基线方法或依赖纯文本描述进行推理，或仅对单张图像进行推理，缺乏跨图像的视觉信息对齐。VC-STaR 通过**对比VQA对**将语义和视觉上相近但细节不同的样本配对，利用跨图像对比将细粒度视觉信息注入推理过程。消融实验（Figure 6）表明，基于相似度搜索的对比对构造策略优于编辑式（HQ-Edit）或描述式（DOCCI）策略，验证了精心选择视觉相似的同义问答对对于激发VLM对比能力的有效性。

### 对比类型的创新发现

VC-STaR 进一步揭示了对比类型对推理改进的差异化影响（Table 4）：**负面对比（对比样本答案不同）带来的提升远大于正面对比（答案相同）**。在GQA基准上，仅使用负面对比将总分从45.4提升至53.7（+8.3），而仅使用正面对比仅提升至50.6（+5.2）；两者结合达到最优的54.7（+9.3）。这表明，迫使模型在视觉相似但答案不同的样本间进行辨别，能更有效地激发其细粒度视觉推理能力。

### 推理效率的保持

值得注意的是，VC-STaR 的对比管道仅在**数据构造阶段**使用，微调后的模型在推理时遵循标准VLM推理范式，无需额外的对比流水线。这一设计保证了方法在推理效率上与基线方法公平可比，同时将对比能力内化到模型参数中。



![[assets/figures/papers/paper_list_l28_https_openreview_net_forum_id_ZymCPON45y/figures/005_Figure_4.jpg]]
*Figure 4: Faithful rationale generation pipeline. A contrastive analysis can be obtained based on the curated contrastive VQA pair. Leveraging the property of VLMs illustrated in Fig. 1, the contrastive analysis is then used to trigger a rethinking procedure, which refines the naive rationale into a more faithful one. This pipeline is designed to generate rationales for supervised finetuning*

VC-STaR 的整体框架围绕一个核心洞察展开：**VLM 在跨图像对比时能够更精确地提取和区分视觉信息，这一内在的对比能力可被重新利用来主动抑制自身的视觉幻觉**。基于此，方法设计了一条“生成-对比-反思”的闭环流水线，将多图对比获得的细粒度视觉辨别能力迁移到单图推理中，实现无需外部奖励模型或人工分解步骤的自我改进。

### 流水线总览

VC-STaR 的完整流程由两大阶段、五个核心模块构成：

**阶段一：对比VQA对构建（Contrastive VQA Pair Curation）**

该阶段的目标是从多源VQA数据中筛选出具有挑战性的对比样本对，为后续的对比分析提供高质量的“视觉参照物”。每个对比对需满足三个关键性质：问题同义、图像视觉相似但细节不同、问题本身依赖视觉推理。构建过程包含三个子步骤（见图3）：

1. **多源数据汇集**：从涵盖通用VQA、推理、数学、图表和OCR等多个领域的异构数据集中收集原始样本。
2. **基于多模态相似度的配对搜索**：利用基于ID的视觉度量学习构建通用视觉嵌入模型，对图像嵌入和问题嵌入分别计算余弦距离，仅保留视觉距离低于阈值 $\phi_v$ 且问题距离低于阈值 $\phi_q$ 的样本作为有效对比对，即满足 $\gamma(e_i^v, e_j^v) < \phi_v \wedge \gamma(e_i^q, e_j^q) < \phi_q$。
3. **难度采样过滤**：依据VLM对样本的初始表现将对比对划分为不同难度等级，仅保留中等难度的对比对用于后续推理生成。消融实验表明，加入简单样本反而导致性能下降（Table 3），验证了难度采样的必要性。

**阶段二：忠实推理路径生成（Faithful Rationale Generation）**

该阶段是VC-STaR的核心创新所在，通过“思考-对比-反思”三步曲将对比分析注入推理过程，纠正视觉幻觉（见图4）。给定VQA数据集 $\mathcal{D} = \{ (v_i, q_i, a_i) \}_{i=1}^{N}$ 和构建好的对比VQA对集合 $\mathcal{P} = \{ ((v_i, q_i, a_i), (\hat{v}_i, \hat{q}_i, \hat{a}_i)) \}_{i=1}^{K}$，流水线执行以下转换：

1. **思考步骤（Thinking Step）**：VLM以正确答案为提示，生成带幻觉的初步推理路径 $r_i = f(v_i, q_i, a_i \vert \theta, \delta^t)$。此步骤模拟了传统自改进方法（如STaR）的输出，其中可能包含不准确的视觉依据。
2. **对比步骤（Contrasting Step）**：将目标样本与对比样本同时输入VLM，生成对比分析 $c_i = f( \big( (v_i, q_i, a_i), (\hat{v}_i, \hat{q}_i, \hat{a}_i) \big) \vert \theta, \delta^c)$。此步骤利用VLM在对比条件下更准确的视觉辨别能力，提取细粒度视觉证据。
3. **反思步骤（Rethinking Step）**：由大语言模型根据对比分析重写推理路径 $\tilde{r}_i = f(r_i, c_i \vert \psi, \delta^r)$，修正原始推理中的视觉幻觉，生成忠实推理路径。
4. **后处理过滤**：通过文本匹配过滤包含错误推理模式的样本，最终形成精炼的视觉推理数据集 $\tilde{\mathcal{R}} = \{ (v_i, q_i, a_i, \tilde{r}_i) \}_{i=1}^{L}$，即 VisCoR-55K。

### 训练与推理

使用 VisCoR-55K 对基础VLM进行全参数监督微调（SFT），冻结视觉塔参数，训练3个epoch，学习率 $1 \times 10^{-5}$，batch size 256。**关键设计**：微调后的模型在推理时**无需运行对比流水线**，遵循标准VLM推理范式，保证了推理效率与基线方法的公平可比性。

### 核心设计决策

- **对比对类型**：负面对比（答案不同）比正面对比（答案相同）在改善视觉推理方面更为有效，两者组合可带来最优增益（Table 4：GQA上从基础45.4提升至54.7）。
- **难度采样**：仅保留中等难度对比对生成推理路径是最优策略（Table 3），暗示过于简单的样本无法提供有效的对比学习信号，反而引入噪声。
- **对比对构造策略**：基于相似度搜索的策略优于编辑式（HQ-Edit）或描述式（DOCCI）策略（Figure 6），说明精心选择视觉相似的同义问答对是激发VLM对比能力的关键。



VC-STaR 的核心流程围绕两个关键挑战展开：(1) 如何构造有意义的对比VQA对；(2) 如何将双图对比中的细粒度辨别能力迁移到单图推理的修正中。整个方法包含三个关键模块：对比VQA对构建、忠实推理路径生成、以及后处理过滤。

### 对比VQA对构建

对比VQA对构建是一个三阶段筛选管道，旨在从多源VQA数据中为每个目标样本找到具有挑战性的对比样本。其形式化定义如下：给定VQA数据集 $\mathcal{D} = \{ (v_i, q_i, a_i) \}_{i=1}^{N}$，目标是为每个样本 $(v_i, q_i, a_i)$ 寻找对比样本 $(\hat{v}_i, \hat{q}_i, \hat{a}_i)$，构成对比VQA对集合：

$$\mathcal{P} = \{ ((v_i, q_i, a_i), (\hat{v}_i, \hat{q}_i, \hat{a}_i)) \}_{i=1}^{K}$$

一个有效的对比VQA对需满足三个关键性质：(1) $q_i$ 与 $\hat{q}_i$ 为同义问题；(2) $v_i$ 与 $\hat{v}_i$ 视觉相似但细节不同；(3) $q_i$ 本身是推理依赖型问题。

对比样本的召回基于多模态嵌入的余弦距离约束。具体而言，对于视觉嵌入 $e^v$ 和问题嵌入 $e^q$，候选样本需同时满足：

$$\gamma(e_i^v, e_j^v) < \phi_v \wedge \gamma(e_i^q, e_j^q) < \phi_q$$

其中 $\gamma(\cdot,\cdot)$ 表示余弦距离，$\phi_v$ 和 $\phi_q$ 分别为视觉和问题相似度的预设阈值。视觉嵌入模型基于ID驱动的视觉度量学习构建，以捕获细粒度视觉差异。在召回候选对比对后，采用难度采样策略，仅保留中等难度的对比VQA对用于后续推理生成——消融实验（Table 3）证实，加入简单样本反而导致性能下降。

### 忠实推理路径生成

推理路径生成采用“思考—对比—反思”三阶段流程，将包含幻觉的初步推理路径 $\mathcal{R} = \{ (v_i, q_i, a_i, r_i) \}_{i=1}^{M}$ 转化为忠实推理路径 $\tilde{\mathcal{R}} = \{ (v_i, q_i, a_i, \tilde{r}_i) \}_{i=1}^{L}$，即 $\mathcal{R} \to \tilde{\mathcal{R}}$。

**思考步骤**：VLM $f(\cdot|\theta)$ 在思考提示 $\delta^t$ 和正确答案 $a_i$ 的引导下生成初步推理路径：

$$r_i = f(v_i, q_i, a_i \vert \theta, \delta^t)$$

此步骤产生的推理路径可能包含视觉幻觉，即推理中引用了图像中不存在或错误的视觉证据。

**对比步骤**：将目标样本与对比样本同时输入VLM，在对比提示 $\delta^c$ 下生成对比分析 $c_i$：

$$c_i = f( \big( (v_i, q_i, a_i), (\hat{v}_i, \hat{q}_i, \hat{a}_i) \big) \vert \theta, \delta^c)$$

这是方法的核心创新点：利用VLM在图像对比时能更精确提取和区分视觉信息的特性（Figure 1 提供了动机证据），将多图对比产生的细粒度视觉辨别能力注入推理过程。

**反思步骤**：大语言模型 $f(\cdot|\psi)$ 在反思提示 $\delta^r$ 下，基于对比分析 $c_i$ 对原始推理路径 $r_i$ 进行重写和修正：

$$\tilde{r}_i = f(r_i, c_i \vert \psi, \delta^r)$$

此步骤将对比分析中提取的精确视觉证据用于纠正原始推理中的幻觉，生成忠实于视觉内容的推理路径。最终通过文本匹配后处理过滤包含错误推理模式的样本，得到高质量的 VisCoR-55K 数据集。

### 推理效率说明

值得注意的是，对比流水线仅在数据构造阶段使用。微调后的模型在推理时遵循标准VLM推理范式，无需执行对比流水线，保证了推理效率与基线方法公平可比。



## 实验与关键发现

### 核心发现：VC-STaR 在幻觉与推理基准上全面超越自改进基线

VC-STaR 在六个具有挑战性的基准上取得了 **58.1** 的平均准确率，较基础模型 Qwen2.5VL-7B 的 55.5 提升了 **+2.6 个百分点**，显著优于所有自改进基线方法（Table 1）。这一提升的关键驱动力在于视觉幻觉的有效抑制：在专门评估幻觉的 **MMVP** 和 **Hallusion** 基准上，VC-STaR 分别取得了 **75.7**（+5.7）和 **56.3**（+3.2）的突出成绩，远超 STaR（Zelikman et al., NeurIPS 2022）等仅依赖文本提示的自改进方法。在数学推理基准 **MathVista** 和 **MathVision** 上，VC-STaR 也分别实现了 69.7（+1.3）和 25.3（+1.3）的稳定提升，表明对比机制对视觉密集型推理任务的普适增益。


![[assets/figures/papers/paper_list_l28_https_openreview_net_forum_id_ZymCPON45y/figures/006_Table_1.jpg]]
*Table 1: Performance comparison with self-improving baselines and the models trained on offthe-shelf visual reasoning datasets on hallucination, math, and general benchmarks. We adopt the Qwen2.5VL-7B as our base model, and report its reasoning performance as a baseline. MME-RW is short for MME-RealWorld Zhang et al. (2025b); R1-OV is short for R1-Onevision (Yang et al., 2025b). Blue (red) numbers in parentheses represent performance gains (drops) relative to the baseline. The best performance is in boldface, and the second best is underlined*

值得注意的是，VC-STaR 不仅优于 STaR、Verifier（Lu et al., 2024a）和 Feedback（Qu et al., 2024）等自改进基线，还超过了基于现成推理数据集训练的模型，如 Virgo（Du et al., 2025）、LLaVA-CoT（Xu et al., 2025）、R1-Onevision（Yang et al., 2025b）和 LPT（Liao et al., 2025）。这些基线方法或依赖模板化推理数据，或使用密集描述和长思维提示，但均未引入跨图像对比机制来显式纠正视觉幻觉。VC-STaR 的优势恰恰来源于其核心设计：将多图对比中激发的细粒度视觉辨别能力迁移到单图推理中。

### 消融实验：对比对质量与难度采样的决定性作用

**难度采样策略**是 VC-STaR 数据构建中的关键设计选择。Table 3 的消融实验表明，仅保留中等难度对比对训练的模型性能最优；额外加入 20K 简单样本导致 Hallusion 下降 4.1、MathVision 下降 2.0、MMStar 下降 1.1；加入 40K 简单样本后性能进一步恶化。这一反直觉结果揭示了自改进推理中的一个重要瓶颈：过于简单的样本无法提供足够的视觉歧义来激发有意义的对比分析，反而稀释了训练数据中精细视觉辨别的信号密度。


![[assets/figures/papers/paper_list_l28_https_openreview_net_forum_id_ZymCPON45y/figures/010_Table_3.jpg]]
*Table 3: Effect of the easy samples adding to VisCoR-55K. Red numbers in parentheses represent performance drops*

**对比对类型**同样至关重要。Table 4 在 GQA 基准上的分析显示，负面对比（答案不同）带来的提升远大于正面对比（答案相同）：仅使用正面对比从基础 45.4 提升至 50.6（+5.2），而仅使用负面对比提升至 53.7（+8.3）；两者结合达到最优的 54.7（+9.3）。这一结果表明，负面对比迫使模型在视觉相似但语义不同的图像间进行更精细的辨别，从而更有效地抑制“视觉近似即答案相同”的幻觉倾向。正面对比则强化了跨视觉变化的语义不变性识别，两者在功能上互补。


![[assets/figures/papers/paper_list_l28_https_openreview_net_forum_id_ZymCPON45y/figures/011_Table_4.jpg]]
*Table 4: Analysis about the effect of positive and negative contrastive VQA counterparts on GQA benchmark. We adopt the Qwen2.5VL-7B as our base model, and report its reasoning performance as a baseline. QR: query for relationships; QA: query for attributes; QG: query for global information; QC: query for category; CA: comparing of attribute; CC: choosing the object of one certain category; CAt: choosing the object of one certain attribute. Blue (red) numbers in parentheses represent performance gains (drops) relative to the baseline*

**对比对构造策略**的比较进一步验证了 VC-STaR 设计选择的合理性。Figure 6 显示，基于相似度搜索的对比对构造策略在多个基准上优于编辑式策略（HQ-Edit）和描述式策略（DOCCI）。后两者的性能甚至在某些基准上低于基础模型（红色虚线），论文将其归因于 HQ-Edit 和 DOCCI 的数据分布偏差限制了对比对的有效覆盖范围。这强化了“精心选择视觉相似的同义问答对”这一设计原则的实证基础。


![[assets/figures/papers/paper_list_l28_https_openreview_net_forum_id_ZymCPON45y/figures/008_Figure_6.jpg]]
*Figure 6: Performance comparison with other contrastive VQA pair construction strategies. Rationales in all settings are generated from the proposed VC-STaR. The red dashed line represents the base model (Qwen2.5VL-7B) performance*

### 泛化性验证与定性分析

**模型架构泛化性**方面，VC-STaR 在 Qwen2.5VL-3B 和 InternVL2.5-8B 上也表现出显著增益（Table 2）。在 Qwen2.5VL-3B 上，Hallusion 提升 6.3、MathVision 提升 3.5、MMStar 提升 0.7；在 InternVL2.5-8B 上，三者分别提升 7.2、2.1 和 1.4。这一跨模型家族的一致性增益表明，对比自我改进机制不依赖于特定视觉编码器或语言模型的架构特性，而是利用了 VLM 在对比条件下普遍增强的视觉辨别能力。


![[assets/figures/papers/paper_list_l28_https_openreview_net_forum_id_ZymCPON45y/figures/009_Table_2.jpg]]
*Table 2: Evaluation of the effect of VC-STaR on other base models. Blue numbers in parentheses represent performance gains*

**定性对比**（Figure 5）直观展示了 VC-STaR 的改进效果：基础模型直接回答时容易忽略关键视觉细节；添加“逐步思考”提示后推理路径仍可能包含视觉幻觉；而 VC-STaR 改进后的模型能够准确定位并引用图像中的关键视觉证据（图中以红色框标注），生成更忠实于视觉输入的推理路径。VisCoR-55K 中的推理路径示例（Figure 8）和附加定性对比（Figure 9）进一步佐证了这一模式。


![[assets/figures/papers/paper_list_l28_https_openreview_net_forum_id_ZymCPON45y/figures/007_Figure_5.jpg]]
*Figure 5: Qualitative Comparison with base model. The second row shows the directly response from the base model, the third row shows the response when the base model is prompted to “think stey by step”, the last row shows the model improved with our VC-STaR. We highlight the key visual evidences with red boxes for clarity of visualization. More results are in Sec. A.4*

![[assets/figures/papers/paper_list_l28_https_openreview_net_forum_id_ZymCPON45y/figures/014_Figure_8.jpg]]
*Figure 8: Examples of rationales in VisCoR-55K*

![[assets/figures/papers/paper_list_l28_https_openreview_net_forum_id_ZymCPON45y/figures/015_Figure_9.jpg]]
*Figure 9: Additional qualitative comparison*

### 失败模式与局限性

尽管 VC-STaR 在整体上表现优异，但其有效性高度依赖对比VQA对的质量。对比对的构建依赖嵌入空间和相似性阈值的选择，贪婪首次匹配策略可能遗漏更优的对比样本。此外，难度采样的分类依赖于 VLM 本身的表现，可能引入模态偏置，使得采样策略在不同模型上的适应性存在差异。推理生成的两阶段过程（对比与反思）也增加了数据构造的计算成本。当前仅在 Qwen2.5-VL 和 InternVL2.5 家族上验证，对 LLaVA 系列等其他架构的泛化性有待进一步检验。



## 定位与知识库关联

### 自改进推理范式的演进

VC-STaR 处于视觉语言模型自改进推理的研究脉络中。该脉络的起点是纯文本域的 **STaR**（Zelikman et al., NeurIPS 2022），其核心机制是利用正确答案作为提示（hints）引导模型重新生成推理路径，再以这些精炼后的推理数据对模型进行监督微调。STaR 的成功催生了一系列自改进变体：**Verifier**（Lu et al., 2024a）引入自我验证模块来过滤包含幻觉的推理；**Feedback**（Qu et al., 2024）则通过自我反馈机制递归地改进推理质量。

然而，这些方法共享一个根本性瓶颈：它们都依赖文本信号（正确答案或文本反馈）来修正推理，无法有效验证推理路径中的视觉依据是否忠实于图像内容。当 VLM 产生视觉幻觉时——例如错误识别物体颜色、数量或空间关系——文本层面的修正非但不能消除幻觉，反而可能将错误的视觉描述固化到精炼后的推理路径中，形成“幻觉放大”效应。

VC-STaR 的关键突破在于识别出 VLM 的一种内在能力：当面对两张视觉相似但细节不同的图像时，VLM 能进行更精确的细粒度视觉辨别（Figure 1a）。通过构造**对比 VQA 对**——两张语义相似、问题同义但答案可能不同的图像-问题组合——VC-STaR 将这种跨图对比的精确视觉能力迁移到单图推理的改进过程中。这使其区别于所有仅依赖文本信号的自改进基线。

### 与现成推理数据集方法的关系

另一条相关线索是利用大规模推理数据训练 VLM。**Virgo**（Du et al., 2025）使用纯文本推理数据，**LLaVA-CoT**（Xu et al., 2025）基于模板化推理数据，**R1-Onevision**（Yang et al., 2025b）借助图像描述和 DeepSeek-R1 生成推理数据，**LPT**（Liao et al., 2025）则采用密集描述和长思维提示。这些方法生成的数据集规模通常远大于 VisCoR-55K（55K 样本），但在幻觉基准上的表现却不如 VC-STaR：例如在 MMVP 上，VC-STaR 达到 75.7，而最佳现成数据集方法仅 72.5（Table 1）。这表明推理数据的“视觉忠实度”比“规模”更为关键。

### 适用边界与局限

**数据依赖性**。VC-STaR 的性能高度依赖对比 VQA 对的构造质量。相似性搜索依赖于多模态嵌入空间的质量和阈值 $\phi_v$、$\phi_q$ 的选择（Sec 3.1），贪婪首次匹配策略可能遗漏更优的对比对。实验表明，基于编辑式（HQ-Edit）或描述式（DOCCI）的对比对构造策略效果明显弱于相似度搜索策略（Figure 6），这归因于 HQ-Edit 和 DOCCI 的数据分布偏差限制了对比对的有效性。

**难度采样的敏感性**。仅保留中等难度对比对是 VC-STaR 的关键设计选择。加入简单样本（+20K 或 +40K）反而导致性能下降：在 Hallusion 上下降 0.6–4.1 个百分点，MathVision 下降 2.0–3.4 个百分点，MMStar 下降 1.1–2.9 个百分点（Table 3）。这表明简单对比对无法提供足够的视觉辨别压力，反而稀释了训练信号的难度密度。然而，难度分类本身依赖 VLM 的初始表现，可能引入模态偏置，使得采样策略在不同模型上存在适应性差异。

**模型架构泛化性**。VC-STaR 在 Qwen2.5VL-3B、Qwen2.5VL-7B 和 InternVL2.5-8B 上均表现出显著增益（Table 2），证实了方法对 Qwen2.5-VL 和 InternVL2.5 家族的泛化能力。但尚未在 LLaVA 系列等其他 VLM 架构上验证，其跨架构适用性有待进一步检验。

**微调范式的限制**。当前仅在全参数监督微调设定下验证，视觉塔参数被冻结。LoRA 等高效微调方法是否能够保留对比能力迁移的效果，仍是未探索的问题。

**数据构造成本**。VC-STaR 的推理生成需要两阶段过程：先产生对比分析，再基于对比分析进行反思重写。相比 STaR 的单阶段提示生成，这增加了数据构造的计算开销。

### 开放问题

1. **隐式对比的可能性**：能否在单图推理阶段隐式利用对比信息，而无需显式构建对比 VQA 对？这将消除对比对构造的依赖，使方法更轻量化。

2. **多模态扩展**：将对比自我改进范式扩展到视频或 3D 模态是否可行？视频帧间的天然时序对比可能为该方法提供更丰富的应用场景。

3. **与强化学习的结合**：如何将对比能力与强化学习（如 GRPO）或树搜索结合，进一步激发 VLM 的推理能力？对比分析可能作为奖励信号或搜索启发式的一部分。

4. **显式视觉差异信号**：是否可以利用图像差异图作为显式的学习信号，指导模型生成更忠实于视觉证据的解释？当前方法依赖文本形式的对比分析，直接利用视觉差异可能提供更强的监督。

5. **难度定义的自动化**：对比采样中的难度定义能否实现自动化，以达成完全任务无关的自我改进？当前难度分类依赖 VLM 的初始表现，一个自适应的难度估计器可能提升方法的通用性。



## 原文 PDF

![[paperPDFs/ICLR_2026/Through_the_Lens_of_Contrast_Self_Improving_Visual_Reasoning_in_VLMs.pdf]]
