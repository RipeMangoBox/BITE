---
title: "GranViT: A Fine-Grained Vision Model For Autoregressive Multimodal Large Language Models"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/GranViT_A_Fine_Grained_Vision_Model_For_Autoregressive_Multimodal_Large_Language_Models.pdf
openreview_forum_id: dQ6LWE0LnG
aliases:
- GranViT
tags:
- ICLR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/vision_models_multimodal
core_operator: "构建包含1.83亿区域级标注的大规模数据集Gran-29M，并引入基于边界框-标题回归（Bbox2Caption）和标题-边界框回归（Caption2Bbox）的两阶段预训练-适应框架，结合自蒸馏机制显式约束局部区域特征，从而重塑视觉编码器的特征提取重心，兼顾全局语义对齐与局部细粒度表示。"
primary_logic: "将区域级自回归训练与自蒸馏相结合，可在不牺牲全局对齐能力的前提下，使视觉编码器具备精准的局部感知能力；通过分阶段训练（视觉预训练+LLM适应）解耦视觉与语言的学习重点，高效地将细粒度视觉特征注入不同规模的LLM。"
claims:
- "GranViT在细粒度任务平均得分达80.78，超越第二好方法SAILViT（77.95）达2.83个百分点。"
- "GranViT在OCR任务平均得分达55.97，超越第二好方法SAILViT（53.33）达2.64个百分点。"
- "两阶段训练：Stage 1使Bbox2Caption的ROUGE-L达到52%，而Caption2Bbox的ACC@IOU0.5仅13%；Stage 2专门训练LLM后，ACC@IOU0.5跃升至55%，验证了解耦训练的有效性。"
- "自蒸馏消融显示λ=1、α=0.9时细粒度性能最优（75.55），证明显式局部约束对特征学习至关重要。"
---

# GranViT: A Fine-Grained Vision Model For Autoregressive Multimodal Large Language Models

> [!tip] 核心洞察
> 将区域级自回归训练与自蒸馏相结合，可在不牺牲全局对齐能力的前提下，使视觉编码器具备精准的局部感知能力；通过分阶段训练（视觉预训练+LLM适应）解耦视觉与语言的学习重点，高效地将细粒度视觉特征注入不同规模的LLM。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | GranViT：面向自回归多模态大语言模型的细粒度视觉模型 |
| 英文题名 | GranViT: A Fine-Grained Vision Model For Autoregressive Multimodal Large Language Models |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=dQ6LWE0LnG) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/vision_models_multimodal |
| Method | GranViT |
| Dataset | Fine-Grained Average, OCR Average, RefCOCO testA, Transfer Average (Qwen2.5-7B) |

> [!tip] 效果简介
> - Fine-Grained Average 上，平均得分 为 80.78，对比 77.95 (SAILViT)，变化 +2.83。
> - OCR Average 上，平均得分 为 55.97，对比 53.33 (SAILViT)，变化 +2.64。
> - RefCOCO testA 上，准确率 为 91.79，对比 89.65 (SAILViT)，变化 +2.14。

## 概述

### 问题与瓶颈

当前多模态大语言模型（MLLM）的视觉编码器普遍侧重于全局图像表征学习，缺乏对图像中局部区域的细粒度感知能力。这导致模型在视觉定位、OCR识别、细粒度目标区分等任务上表现受限。造成这一瓶颈的深层原因有两点：其一，现有预训练范式（如对比学习或全局自回归）并未显式建模区域级特征；其二，缺乏大规模、高质量的细粒度区域标注数据来驱动此类训练。

### 核心方法

**GranViT** 是一种面向自回归MLLM的细粒度视觉编码器，其核心思路是通过区域级自回归训练重塑视觉编码器的特征提取重心，使其在不牺牲全局语义对齐能力的前提下，获得精准的局部感知能力。方法体系包含三个关键组件：

1. **Gran-29M数据集**：构建包含2900万张图像、1.83亿条区域级标注的大规模预训练数据集，为细粒度训练提供数据基础。
2. **两阶段预训练-适应框架**：Stage 1冻结LLM，训练视觉编码器与投影器，通过全局标题生成和**边界框-标题回归**（Bbox2Caption）任务强化局部视觉表征；Stage 2冻结视觉编码器，训练LLM，通过**标题-边界框回归**（Caption2Bbox）任务赋予LLM利用细粒度特征进行精准定位的能力。两阶段解耦了视觉特征学习与语言定位学习的重点。
3. **自蒸馏机制**：引入教师-学生自蒸馏，通过裁剪区域的特征对齐（MSE损失）和EMA更新的教师编码器，显式约束学生编码器的局部区域特征，进一步强化细粒度表示。

### 方法谱系与知识库定位

GranViT定位于视觉编码器的预训练范式改进，属于“视觉表征增强”技术路线。与现有工作相比：

- 相较于**CLIP**（Radford et al., ICML 2021）和**SigLip**（Zhai et al., 2023）等纯对比学习编码器，GranViT引入了区域级自回归训练目标，弥补了对比学习在局部感知上的不足。
- 相较于**AIMv2**（Fini et al., 2025）等自回归编码器，GranViT通过Bbox2Caption/Caption2Bbox双向任务和自蒸馏，显式建模了区域-文本的对齐关系，而非仅依赖全局自回归。
- 相较于**SAILViT**（Yin et al., 2025）等多阶段预训练的强基线，GranViT以**SigLip2**（Tschannen et al., 2025）为初始化，叠加细粒度预训练框架后仍能取得显著提升，证明其方法具有可叠加性。

### 主要结果

在低分辨率设置下的综合评测中，GranViT展现出全面的细粒度感知优势：

- **细粒度任务平均得分80.78**，超越第二好方法SAILViT（77.95）达2.83个百分点（Table 1）。
- **OCR任务平均得分55.97**，超越SAILViT（53.33）达2.64个百分点（Table 1）。
- **视觉定位**：RefCOCO testA准确率达91.79，领先SAILViT（89.65）2.14个百分点（Table 1）。
- **迁移能力**：在Qwen2.5-7B上迁移平均得分67.47，超越AIMv2（64.69）达2.78个百分点（Table 2）。

消融实验进一步验证了各组件的有效性：Stage 1预训练使细粒度性能提升2.2，OCR提升1.2；Stage 2适应再分别增加1.0和0.7（Table 3）；自蒸馏在λ=1、α=0.9时达到最佳细粒度性能75.55（Table 5）。两阶段训练曲线（Figure 4a）清晰展示了Stage 1中Bbox2Caption的ROUGE-L达到52%，而Caption2Bbox的ACC@IOU0.5仅13%；进入Stage 2后ACC@IOU0.5跃升至55%，验证了解耦训练策略的有效性。

### 局限与展望

GranViT在极小目标、高密度文本区域和严重遮挡场景下感知能力下降，且依赖相对坐标系统可能限制定位精度。此外，由于预训练重点偏向细粒度特征，在需要复杂多步推理的基准上略低于专门优化推理的编码器。未来方向包括整合绝对坐标系统、设计多尺度预训练策略以增强极小目标感知，以及探索与SAILViT式持续预训练的结合潜力。

## 背景与动机

### 问题背景

多模态大语言模型（MLLM）近年来在视觉问答、图像描述等任务上取得了显著进展，其核心架构通常由视觉编码器、投影器和LLM三部分串联而成。视觉编码器负责将图像转化为LLM可理解的语义特征，因此其表征质量直接决定了MLLM的感知上限。然而，当前主流的视觉编码器——无论是基于对比学习的**CLIP**（Radford et al., ICML 2021）、**SigLip**（Zhai et al., 2023）及其后续版本**SigLip2**（Tschannen et al., 2025），还是基于自回归的**AIMv2**（Fini et al., 2025）或混合范式的**InternViT**（Chen et al., CVPR 2024）——其预训练目标均以图像级别的全局语义对齐为核心。这种设计导致了一个关键瓶颈：**视觉编码器缺乏对图像局部区域的细粒度感知能力**。

Figure 1(b) 的注意力可视化直观地揭示了这一问题：当给定一个指向特定区域的查询token时，SigLip2、AIMv2和SAILViT的注意力图往往弥散在全局背景上，无法精准聚焦于查询所指的目标区域。相比之下，GranViT的注意力图则紧密围绕目标区域，形成了清晰的局部激活。这一差异在视觉定位（visual grounding）、光学字符识别（OCR）和细粒度物体识别等需要精确区域理解的任务中尤为致命。

### 现有方法的缺口

现有工作试图从两个方向缓解上述问题，但各自存在明显局限：

**1. 数据层面：缺乏大规模细粒度标注数据。** 当前的视觉-语言预训练数据集（如LAION、COYO等）主要提供图像-全局描述对，极少包含区域级别的精细标注。构建此类标注需要高昂的人工成本，而已有的区域标注数据集（如RefCOCO、Visual Genome）规模有限，难以支撑大规模预训练。这导致视觉编码器在预训练阶段几乎没有机会学习局部区域的语义对应关系。

**2. 训练范式层面：缺乏专门的细粒度预训练框架。** 即使获得区域标注数据，如何有效地将区域级监督信号注入视觉编码器仍是一个开放问题。现有的多阶段预训练方法（如**SAILViT**，Yin et al., 2025）虽然通过注入世界知识提升了整体性能，但其训练目标并未显式约束视觉编码器学习局部区域的精细化表征，导致细粒度任务的提升幅度有限。

### 本文动机

针对上述双重缺口，本文提出**GranViT**，一种面向自回归MLLM的细粒度视觉模型。其核心动机可归纳为三点：

- **构建大规模细粒度预训练数据集Gran-29M**：通过自动化标注管线，以可扩展的方式构建包含2900万张图像和1.83亿条区域级描述的预训练语料，为细粒度视觉学习提供数据基础。

- **设计两阶段预训练-适应框架**：将视觉编码器的细粒度特征学习与LLM的定位能力训练解耦。第一阶段（视觉预训练）通过边界框到标题回归（Bbox2Caption）和自蒸馏机制，重塑视觉编码器的特征提取重心；第二阶段（LLM适应）通过标题到边界框回归（Caption2Bbox），使LLM学会利用细粒度视觉特征进行精准定位。

- **引入自蒸馏机制显式约束局部特征**：通过教师-学生自蒸馏架构，对裁剪区域的特征进行显式对齐，迫使视觉编码器在保持全局语义对齐能力的同时，具备精准的局部感知能力。

这一设计思路的核心理念在于：**通过区域级自回归训练与自蒸馏的结合，在不牺牲全局对齐能力的前提下，使视觉编码器具备精准的局部感知能力；通过分阶段训练解耦视觉与语言的学习重点，高效地将细粒度视觉特征注入不同规模的LLM。**

## 核心创新

GranViT的核心创新在于**重塑视觉编码器的特征学习重心**，使其在保持全局语义对齐能力的同时，显式习得细粒度的局部感知能力。这一目标通过三个紧密耦合的“changed slots”实现。

### 1. 训练数据与任务：从全局标题到区域级自回归

现有视觉编码器（如**CLIP** (Radford et al., ICML 2021)、**SigLip** (Zhai et al., 2023)）仅依赖图像-全局标题对进行对比或自回归训练，天然忽略了区域级细粒度信息。GranViT构建了**Gran-29M**数据集（2900万图像，1.83亿区域级标注），并引入三种互补的自回归任务：

- **全局标题生成**：保持语义对齐基线。
- **Bbox2Caption回归**：给定边界框坐标，要求LLM生成对应区域的描述文本，迫使视觉编码器提取高质量局部特征。
- **Caption2Bbox回归**：给定区域描述，要求LLM预测边界框坐标，训练LLM利用细粒度视觉特征进行精准定位。

这一任务组合的因果效应明确：Bbox2Caption直接约束视觉编码器的局部特征质量，Caption2Bbox则验证这些特征能否被LLM有效利用。

### 2. 训练策略：解耦视觉与语言学习的两阶段框架

传统多模态训练通常将视觉编码器与LLM联合优化，导致两个目标相互干扰。GranViT提出**两阶段预训练-适应框架**，解耦视觉与语言的学习重点：

- **Stage 1（视觉预训练）**：冻结LLM，仅训练视觉编码器与投影器，专注细粒度特征提取。
- **Stage 2（LLM适应）**：冻结视觉编码器，训练投影器与LLM，专注学习如何利用已提取的细粒度特征进行定位。

关键证据来自**Figure 4(a)**：Stage 1结束时，Bbox2Caption的ROUGE-L达52%，而Caption2Bbox的ACC@IOU0.5仅13%；进入Stage 2专门训练LLM后，ACC@IOU0.5跃升至55%，验证了解耦训练的必要性——视觉特征提取与空间定位利用需分阶段优化。

### 3. 自蒸馏机制：显式局部特征约束

仅靠Bbox2Caption任务的语言监督，对局部特征的约束是隐式且间接的。GranViT引入**教师-学生自蒸馏**，提供显式的局部特征级监督：

- **教师编码器**：从原始图像裁剪区域提取特征（$x_{crop}'$）。
- **学生编码器**：从完整图像经ROIAlign提取对应区域特征（ROIAlign($x'$)）。
- **蒸馏损失**：$L_{distill} = MSE(x_{crop}', ROIAlign(x'))$，直接约束学生编码器的局部特征与教师一致。
- **教师更新**：通过EMA平滑更新：$\theta_{tea} = \alpha \theta_{tea} + (1 - \alpha) \theta_{stu}$，保持监督信号的稳定性。

消融实验（**Table 5**）证实，$\lambda=1$、$\alpha=0.9$时细粒度性能最优（75.55），显著优于不使用自蒸馏的配置，证明显式局部约束对特征学习至关重要。

---

**三个创新的协同效应**：Gran-29M提供细粒度监督信号，两阶段训练解耦学习目标使信号有效传递，自蒸馏则补全了语言监督在局部特征层面的不足。这一组合使GranViT在细粒度任务平均得分达80.78，超越强基线**SAILViT** (Yin et al., 2025) 的77.95（+2.83）；OCR平均得分达55.97，超越SAILViT的53.33（+2.64）（**Table 1**）。

## 整体框架

![[assets/figures/papers/paper_list_l27_https_openreview_net_forum_id_dQ6LWE0LnG/figures/004_Figure_3.jpg]]
*Figure 3: The fine-grained pretraining and transferring paradigm of GranViT. For pretraining, the vision encoder and projector are tuned via the global and Bbox2Caption task for fine-grained feature extraction. The teacher vision encoder explicitly supervises the local region of features extracted by the student vision encoder. For vision feature adaptation and transfer, based on the fine-grained vision encoder, we apply LLM tuning to further strengthen the localization capability of the LLM regarding fine-grained visual features via the global and Caption2Bbox task*

![[assets/figures/papers/paper_list_l27_https_openreview_net_forum_id_dQ6LWE0LnG/figures/002_Figure_1.jpg]]
*Figure 1: (a) Compared to existing vision encoders, GranViT demonstrates outstanding performance across fine-grained natural image and OCR understanding. HBench denotes HallusionBench. (b) Attention visualization of existing vision encoders according to the query token. The small red rectangle indicates the query token. Best viewed with zoom in*

GranViT 的核心设计围绕一个两阶段预训练-适应范式展开，其目标是在不牺牲全局语义对齐能力的前提下，使视觉编码器获得精准的局部细粒度感知能力。整个 pipeline 由四个关键模块构成：**学生视觉编码器（Student Vision Encoder）**、**教师视觉编码器（Teacher Vision Encoder）**、**投影器（Projector）** 和 **大语言模型（LLM）**，各模块在两阶段中承担不同的训练角色。

**阶段一：细粒度预训练（Fine-Grained Pretraining）**

此阶段的核心任务是重塑视觉编码器的特征提取重心，使其从全局表征学习转向兼顾局部细粒度表示。具体流程如下：

1. **输入流**：图像经尺寸调整（512×512）和宽高比填充后，同时送入学生视觉编码器和冻结的教师视觉编码器。
2. **学生编码器**：以 SigLip2 为初始化权重，提取全局图像特征。该模块在此阶段可训练。
3. **教师编码器**：权重通过指数移动平均（EMA）从学生编码器更新，规则为 $\theta_{tea} = \alpha \theta_{tea} + (1 - \alpha) \theta_{stu}$。教师编码器对输入图像的随机裁剪区域提取特征，作为局部表征的监督信号。
4. **投影器**：一个两层 MLP，将学生编码器的视觉特征映射到 LLM 的语义空间。此阶段可训练。
5. **LLM**：以 Qwen2.5-VL-1.5B 初始化，在此阶段**冻结**，仅作为文本解码器提供自回归监督。
6. **任务与损失**：
   - **全局标题生成**：基于整图特征生成描述文本，损失为 $L_{caption} = CrossEntropy(O_{LLM}, T)$。
   - **Bbox2Caption 回归**：给定边界框坐标，生成对应区域的描述文本，同样使用交叉熵损失。
   - **自蒸馏损失**：$L_{distill} = MSE(x_{crop}', ROIAlign(x'))$，即教师裁剪区域特征与学生 ROI 对齐特征之间的均方误差，显式约束局部特征学习。
   - **总损失**：$\mathcal{L} = \mathcal{L}_{caption} + \lambda \mathcal{L}_{distill}$，其中 $\lambda$ 为平衡系数。

阶段一的关键瓶颈在于：Bbox2Caption 的 ROUGE-L 可达 52%，但 Caption2Bbox 的 ACC@IOU0.5 仅 13%（Figure 4a），说明视觉编码器在此阶段已学会“看图说话”，但 LLM 尚未获得利用细粒度特征进行精确定位的能力。这印证了视觉与语言学习目标需要解耦的核心洞察。

**阶段二：LLM 适应与迁移（Adaptation and Transfer）**

此阶段将阶段一学到的细粒度视觉特征“注入”LLM，使其具备定位能力：

1. **输入流**：与阶段一相同。
2. **学生视觉编码器**：**冻结**，保留阶段一学到的细粒度表征能力。消融实验（Table 9）表明，冻结策略可节省约 24% 的 FLOPs，且细粒度性能几乎无损（77.24 frozen vs 77.17 tunable）。
3. **教师编码器**：此阶段不参与训练。
4. **投影器**：可训练，继续桥接视觉与语言空间。
5. **LLM**：**可训练**，学习如何利用细粒度视觉特征进行空间定位。此阶段可替换为更大规模的 LLM（如 Qwen2.5-7B、LLaMA3-8B）以实现迁移。
6. **任务与损失**：
   - **全局标题生成**：与阶段一相同。
   - **Caption2Bbox 回归**：给定区域描述文本，生成对应的边界框坐标。这是阶段二的核心任务，使 LLM 学会“按文索骥”。

Figure 4a 清晰展示了阶段二的效应：Caption2Bbox 的 ACC@IOU0.5 从 13% 跃升至 55%，而 Bbox2Caption 仅微增约 3%。这验证了解耦训练的有效性——阶段一专注视觉编码器的细粒度特征提取，阶段二专注 LLM 的定位能力学习。

**整体数据流与依赖关系**

```
阶段一（视觉预训练）:
  图像 → [学生ViT(可训练)] → 全局特征 → Projector(可训练) → LLM(冻结) → 文本输出
         [教师ViT(EMA更新)] → 裁剪特征 → L_distill ↗
  任务: 全局Caption + Bbox2Caption + 自蒸馏

阶段二（LLM适应）:
  图像 → [学生ViT(冻结)] → 全局特征 → Projector(可训练) → LLM(可训练) → 文本/坐标输出
  任务: 全局Caption + Caption2Bbox
```

训练数据来自 Gran-29M 数据集，包含 2900 万张图像和 1.83 亿条区域级标注（Figure 2）。数据标注流程利用 ViTDet 生成边界框、Qwen2.5-VL-7B 生成区域描述，经严格过滤后转化为问答对格式。所有实验在 128 块 Ascend 910B NPU 上完成，使用 AdamW 优化器（学习率 1e-5，batch size 256，训练 1 epoch），确保对比公平性。

## 核心模块与公式推导

GranViT的核心架构围绕**两阶段预训练-适应框架**与**自蒸馏机制**展开，通过解耦视觉特征学习与语言模型适应，将细粒度区域感知能力注入视觉编码器。

### 两阶段训练框架

**Stage 1：视觉预训练（Visual Pretraining）**
此阶段冻结LLM，仅训练视觉编码器（Vision Encoder）与投影器（Projector，两层MLP）。训练任务包括全局标题生成与**Bbox2Caption回归**——给定边界框坐标，要求模型自回归生成该区域的文本描述。该任务迫使视觉编码器学习提取局部区域的细粒度语义特征。教师视觉编码器在此阶段提供自蒸馏监督（见下文）。

**Stage 2：LLM适应与迁移（Adaptation & Transfer）**
此阶段冻结视觉编码器，训练投影器与LLM。核心任务切换为**Caption2Bbox回归**——给定区域文本描述，要求模型预测对应的边界框坐标。该任务训练LLM利用Stage 1提取的细粒度视觉特征进行精准空间定位。实验表明，Caption2Bbox的ACC@IOU0.5从Stage 1的仅13%跃升至Stage 2的55%（Figure 4(a)），验证了解耦训练的必要性：Stage 1专注视觉特征提取，Stage 2专注定位能力注入。

### 自蒸馏机制

在Stage 1中引入教师-学生自蒸馏框架，显式约束局部区域特征学习。具体流程如下：

1. **教师编码器**：与视觉编码器结构相同，权重通过指数移动平均（EMA）从学生编码器更新，不参与梯度回传。
2. **特征提取与对齐**：对输入图像，教师编码器提取裁剪区域（crop）的特征 $x_{crop}'$；学生编码器提取全图特征后，通过ROIAlign操作获取对应区域的特征 $ROIAlign(x')$。
3. **蒸馏损失**：计算两者之间的均方误差（MSE），迫使学生的局部区域特征与教师的稳定表征对齐：

$$L_{distill} = MSE(x_{crop}', ROIAlign(x'))$$

4. **教师权重更新**：教师编码器权重 $\theta_{tea}$ 通过EMA从学生权重 $\theta_{stu}$ 更新：

$$\theta_{tea} = \alpha \theta_{tea} + (1 - \alpha) \theta_{stu}$$

### 联合损失函数

整体训练损失为自回归标题损失与自蒸馏损失的加权和：

$$\mathcal{L} = \mathcal{L}_{caption} + \lambda \mathcal{L}_{distill}$$

其中 $\mathcal{L}_{caption} = CrossEntropy(O_{LLM}, T)$ 为LLM输出文本 $O_{LLM}$ 与真实文本 $T$ 之间的交叉熵损失，同时应用于全局标题生成、Bbox2Caption和Caption2Bbox任务。

### 关键消融发现

- **自蒸馏系数**：Table 5消融实验显示，$\lambda=1$、$\alpha=0.9$ 时细粒度性能达到最优（75.55），证实显式局部约束对特征学习至关重要。
- **Stage 2冻结策略**：Table 9表明，Stage 2冻结视觉编码器可节省约24% FLOPs，且细粒度性能几乎无损（77.24 frozen vs 77.17 tunable），验证了框架的解耦设计在计算效率上的优势。

## 实验与分析

### 核心瓶颈与实验逻辑

现有视觉编码器（如CLIP、SigLip）的训练目标聚焦于全局图像-文本对齐，缺乏对局部区域的显式建模能力。这导致MLLM在视觉定位、OCR和细粒度识别等任务上表现受限。GranViT的实验设计围绕一个因果链条展开：**通过大规模区域级标注数据（Gran-29M）和两阶段预训练-适应框架，重塑视觉编码器的特征提取重心，使其兼顾全局语义对齐与局部细粒度表示**。实验从四个层面验证这一逻辑：(1) 主基准对比——在统一框架下与主流编码器比较细粒度、VQA、推理和OCR四维能力；(2) 迁移性验证——将编码器迁移到不同规模LLM以检验表示通用性；(3) 消融分析——拆解两阶段训练和自蒸馏机制的独立贡献；(4) 缩放与失败模式——揭示方法的边界条件。

### 主实验结果

**Table 1** 展示了低分辨率设置下GranViT与六种视觉编码器的综合对比。GranViT在细粒度任务上取得**80.78**的平均分，超越第二好的SAILViT（77.95）达**+2.83**个百分点；在OCR任务上取得**55.97**的平均分，领先SAILViT（53.33）**+2.64**个百分点。这一优势在RefCOCO testA上尤为突出——GranViT达到**91.79**，比SAILViT（89.65）高出**2.14**个百分点。值得注意的是，GranViT在VQA维度与SAILViT基本持平（53.57 vs 53.85，差距仅0.3），表明细粒度能力的提升并未以牺牲全局理解为代价。推理维度上，GranViT（49.58）略低于SigLip2（50.33），这与预训练重点偏向细粒度特征有关，可通过增加推理VQA数据补充。


![[assets/figures/papers/paper_list_l27_https_openreview_net_forum_id_dQ6LWE0LnG/figures/006_Table_1.jpg]]
*Table 1: Performance comparison with low resolution version. The bold font represents the best performance, and the underline represents the second performance*

**Table 2** 验证了GranViT表示的迁移性。当迁移至Qwen2.5-7B时，GranViT取得**67.47**的平均分，超越AIMv2（64.69）达**+2.78**；在LLaMA3-8B上平均分达**69.02**，同样表现最优。这表明GranViT学习到的细粒度视觉表示具有跨LLM架构和规模的泛化能力。


![[assets/figures/papers/paper_list_l27_https_openreview_net_forum_id_dQ6LWE0LnG/figures/007_Table_2.jpg]]
*Table 2: Performance comparison for transferring vision encoders to Qwen2.5-3B, Qwen2.5-7B and LLaMA3-8B. The best results are highlighted in bold and the second best underlined. Ref, Ref+ and Refg denote the RefCOCO testA, RefCOCO+ testA and RefCOCOg test. MMB, HB, and SB stand for MMBench, HallusionBench, and SEEDBench, and. SQA, OB, DVQA, and IVQA for ScienceQA, OCRBench, DocVQA, and InfoVQA, respectively*

### 两阶段训练的关键证据

**Figure 4(a)** 提供了两阶段训练解耦有效性的直接证据。在Stage 1（视觉预训练，LLM冻结），Bbox2Caption的ROUGE-L迅速攀升至约**52%**，而Caption2Bbox的ACC@IOU0.5始终徘徊在**13%**左右——说明冻结的LLM无法有效利用视觉特征进行定位。进入Stage 2（LLM适应，视觉编码器冻结）后，Caption2Bbox的ACC@IOU0.5从13%跃升至**55%**，而Bbox2Caption仅微增约3%。这一鲜明对比证实了分阶段训练的核心洞察：**Stage 1负责将细粒度信息编码到视觉特征中，Stage 2负责教会LLM解码这些特征进行定位**。Figure 4(b)的预测边框可视化进一步验证了Stage 2训练Caption2Bbox的有效性。


![[assets/figures/papers/paper_list_l27_https_openreview_net_forum_id_dQ6LWE0LnG/figures/005_Figure_4.jpg]]
*Figure 4: (a) The performance curve of Stage1 and Stage2. We sample 8M Bbox2Caption and Caption2Bbox samples respectively for pretraining and adaptation and calculate ROUGE-L (Barbella & Tortora, 2022) and ACC@IOU0.5 for Bbox2Caption and Caption2Bbox respectively. In stage 1, the ACC@IOU0.5 of the Caption2Bbox task only achieves 13%, while the ROUGE-L of the Bbox2Caption task achieves 52%. Conversely, in stage 2, the training of LLM leads to a notable increase in ACC@IOU0.5 for Caption2Bbox, while Bbox2Caption achieves only a minimal improvement of 3%. (b) Visualization of predicted bbox coordinate of Caption2Bbox task in stage 1 and stage 2. Green bboxes indicate predicted regions, while red ones de...*

### 消融实验

**Table 3** 的组件消融量化了各模块的增量贡献。以SigLip2为基线，Stage 1预训练使细粒度性能提升**+2.2**、OCR提升**+1.2**；Stage 2适应在此基础上再增加**+1.0**和**+0.7**。自蒸馏机制的引入进一步带来细粒度**+0.5**的增益。这表明三个组件（Stage 1预训练、Stage 2适应、自蒸馏）各自独立贡献，且叠加效果显著。


![[assets/figures/papers/paper_list_l27_https_openreview_net_forum_id_dQ6LWE0LnG/figures/012_Table_3.jpg]]
*Table 3: Ablation study on each component of the proposed GranViT*

**Table 4** 检验了框架对不同初始化编码器的兼容性。当以SAILViT（已具备较强细粒度能力的基线）为初始化时，GranViT仍能将细粒度性能从74.14提升至**76.79**（+2.65），OCR从54.59提升至**56.61**（+2.02）。这证明GranViT框架可叠加于强基线之上，具有独立的增益来源。


![[assets/figures/papers/paper_list_l27_https_openreview_net_forum_id_dQ6LWE0LnG/figures/013_Table_4.jpg]]
*Table 4: Performance with different vision encoder initialization for GranViT during pretraining. Table 5: Ablation Study of the coefficient in self-distillation*

**Table 5** 对自蒸馏系数进行了精细消融。在λ=1、α=0.9时细粒度性能达到最优的**75.55**，显著优于不使用自蒸馏的配置（73.82）。λ过小（0.1）或过大（10）均导致性能下降，表明局部约束需要适当的权重平衡——过弱则监督不足，过强则可能干扰全局表示学习。


![[assets/figures/papers/paper_list_l27_https_openreview_net_forum_id_dQ6LWE0LnG/figures/014_Table_5.jpg]]

### 计算效率与实用设计

**Table 9** 显示，在Stage 2冻结视觉编码器可节省约**24%的FLOPs**，且细粒度性能几乎无损（77.24 frozen vs 77.17 tunable）。这一设计使得GranViT在迁移到不同LLM时只需训练投影器和LLM，大幅降低了适应成本。


![[assets/figures/papers/paper_list_l27_https_openreview_net_forum_id_dQ6LWE0LnG/figures/020_Table_9.jpg]]
*Table 9: Performance comparison of whether the vision encoder is frozen in stage 2. Table 10: Performance comparison when the vision encoder is frozen during SFT training*

### 失败模式与边界条件

**Figure 13** 揭示了GranViT的三类典型失败场景：(1) **极小目标/高密度文本**——当边界框过小或文字过于密集时，模型难以准确描述或定位目标；(2) **严重遮挡**——多目标高度重叠时定位精度显著下降；(3) **相对坐标局限**——依赖归一化相对坐标（而非绝对坐标）在某些场景下阻碍精确定位。这些失败模式与**Figure 5**的缩放曲线形成呼应：虽然增加数据量持续提升性能，但边际收益递减，暗示仅靠数据扩展难以根本解决上述结构性问题。

**Table 8** 的高分辨率（启用图像分块）实验显示，GranViT在细粒度（82.95）和OCR（61.46）上仍保持领先，但与SAILViT的差距有所缩小（细粒度仅领先0.52），说明高分辨率策略本身能部分缓解细粒度感知不足的问题，但GranViT的表示优势在低分辨率设置下更为突出。


![[assets/figures/papers/paper_list_l27_https_openreview_net_forum_id_dQ6LWE0LnG/figures/019_Table_8.jpg]]
*Table 8: Performance comparison with image tiling. The bold font represents the best performance, and the underline represents the second performance*

### 小结

实验证据链完整地支持了核心主张：GranViT通过大规模区域级自回归训练与自蒸馏机制，在不牺牲全局对齐的前提下显著增强了视觉编码器的细粒度感知能力。两阶段解耦训练是实现这一目标的关键设计——Stage 1编码细粒度信息，Stage 2解码定位能力。方法在极小目标、严重遮挡和相对坐标系统上存在固有局限，这些边界条件指向了未来的改进方向。

### 补充图表

![[assets/figures/papers/paper_list_l27_https_openreview_net_forum_id_dQ6LWE0LnG/figures/015_Table_6.jpg]]
*Table 6: Detailed data sources of datasets used in Gran-29M*

![[assets/figures/papers/paper_list_l27_https_openreview_net_forum_id_dQ6LWE0LnG/figures/016_Table_7.jpg]]
*Table 7: Data sources of natural and OCR images in Gran-29M. #images and #regions denote the number of images and annotated bounding boxes after filtering, respectively*


## 方法谱系与知识库定位

### 瓶颈定位：从全局对齐到细粒度感知的范式缺口

当前MLLM的视觉编码器普遍继承自对比学习范式（如**CLIP** (Radford et al., ICML 2021)、**SigLip** (Zhai et al., 2023)）或自回归范式（如**AIMv2** (Fini et al., 2025)），其训练目标天然偏向全局图像-文本语义对齐，缺乏对局部区域的显式建模能力。**InternViT** (Chen et al., CVPR 2024) 虽尝试混合对比与自回归目标，但仍未引入区域级监督信号。**SAILViT** (Yin et al., 2025) 通过多阶段预训练注入世界知识，在细粒度任务上表现强劲，但其训练范式同样未包含显式的局部区域约束。

这一范式缺口导致两个连锁问题：（1）视觉编码器提取的特征在空间粒度上粗糙，LLM难以从中解码精确的空间定位信息；（2）缺乏大规模细粒度标注数据支撑专门的局部感知预训练。GranViT的核心洞察在于：**通过区域级自回归训练与自蒸馏的协同，可以在不牺牲全局对齐能力的前提下，重塑视觉编码器的特征提取重心，使其兼具全局语义理解与局部精细感知。**

### 方法谱系：GranViT在视觉编码器演进中的位置

从训练范式的维度，现有视觉编码器可沿两个轴定位：

- **训练目标轴**：从纯对比学习（CLIP, SigLip）到纯自回归（AIMv2），再到混合范式（InternViT）。
- **监督粒度轴**：从仅全局监督（上述所有基线）到全局+区域级联合监督（GranViT）。

GranViT以**SigLip2** (Tschannen et al., 2025) 为初始化基础，在其之上叠加了三个关键创新槽位：

| 创新槽位 | 基线做法 | GranViT做法 | 因果机制 |
|---------|---------|------------|---------|
| **训练数据与任务** | 仅图像-全局标题对 | Gran-29M（29M图像，183M区域级标注），多任务学习（全局标题生成 + Bbox2Caption + Caption2Bbox） | 提供显式区域级监督信号，强制编码器学习局部特征 |
| **训练策略** | 单阶段或未解耦的多阶段训练 | 两阶段预训练-适应：Stage 1冻结LLM训视觉编码器，Stage 2冻结视觉编码器训LLM | 解耦视觉特征学习与语言定位能力，避免优化目标冲突 |
| **自蒸馏机制** | 无显式局部约束 | 教师-学生自蒸馏，通过裁剪区域特征对齐（MSE）和EMA更新教师编码器 | 在无额外标注的情况下，显式增强局部区域特征的一致性 |

这种设计使GranViT处于“全局-局部联合自回归 + 自蒸馏”的独特方法节点，与现有工作形成互补而非替代关系。实验证明该框架可叠加于强基线之上：以SAILViT为初始化时，GranViT的细粒度得分进一步提升至76.79（Table 4），说明其局部感知增强机制与SAILViT的世界知识注入策略是正交且可叠加的。

### 适用边界与失效模式

**有效边界**：
- 适用于需要细粒度视觉理解的场景，包括视觉定位（RefCOCO testA达91.79）、OCR理解（平均55.97）和细粒度识别。
- 两阶段训练框架具有良好的LLM迁移性：在Qwen2.5-3B/7B和LLaMA3-8B上均取得最优或次优的迁移平均得分（Table 2），且缩放曲线（Figure 5）显示随数据量增加性能持续提升，未见饱和趋势。
- Stage 2冻结视觉编码器可节省约24% FLOPs，性能几乎无损（Fine-Grained 77.24 frozen vs 77.17 tunable，Table 9），适合计算资源受限的迁移场景。

**失效模式**（Figure 13及论文讨论）：
1. **极小目标与高密度文本**：当边界框过小或文字过于密集时，区域特征的分辨率不足以支撑精确描述或定位。
2. **严重目标遮挡**：在物体高度重叠的场景中，ROI对齐的特征包含大量干扰信息，定位精度显著下降。
3. **相对坐标系统的固有限制**：依赖归一化相对坐标（$[0,1]$范围）进行定位，在需要像素级精度的场景中可能不足，绝对坐标系统（如Qwen3-VL所采用）或许是更优选择。
4. **推理能力略逊**：由于预训练重点偏向细粒度特征，在需要复杂多步推理的基准（如MMMU）上略低于专门优化推理的编码器（如SigLIP2），可通过增加推理VQA数据补充。

### 开放问题

1. **坐标表示升级**：如何整合绝对坐标系统以突破相对坐标的精度上限？
2. **多尺度预训练**：针对极小目标，是否需要设计多尺度或金字塔式的预训练策略来增强跨尺度感知？
3. **密集场景鲁棒性**：针对密集和重叠场景，哪些高级数据增强或架构改进（如可变形注意力）能有效提升鲁棒性？
4. **与任务特定预训练的融合**：将GranViT的通用细粒度表示与SAILViT式的任务特定持续预训练相结合，能否在专业化应用（如医学影像、遥感）中取得更大突破？
5. **更大规模LLM的迁移特性**：当前验证止于8B级别LLM，在70B+模型上的迁移效果和缩放特性尚待探索。

## 原文 PDF

![[paperPDFs/ICLR_2026/GranViT_A_Fine_Grained_Vision_Model_For_Autoregressive_Multimodal_Large_Language_Models.pdf]]
