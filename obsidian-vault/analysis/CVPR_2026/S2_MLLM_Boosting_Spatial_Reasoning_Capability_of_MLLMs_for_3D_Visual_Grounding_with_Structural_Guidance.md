---
title: "S$^2$-MLLM: Boosting Spatial Reasoning Capability of MLLMs for 3D Visual Grounding with Structural Guidance"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/S_2_MLLM_Boosting_Spatial_Reasoning_Capability_of_MLLMs_for_3D_Visual_Grounding_with_Structural_Guidance.pdf
project_link: null
code_link: null
aliases:
- SMSM
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
core_operator: 在训练阶段引入基于前馈3D重建的空间引导目标，使模型在潜在空间内隐式学习3D结构，从而在推理时无需显式重建即可进行空间推理。
primary_logic: 通过联合优化重建损失与定位任务损失，将前馈3D重建的结构感知注入MLLM的视觉表示中，并配合结构增强模块（多级位置编码和视图内/视图间注意力）显式强化位置与跨视角一致性，实现隐式空间推理，显著提升性能与效率。
claims:
- 我们的关键思路是鼓励模型在训练期间隐式内化3D结构感知，使S²-MLLM能够在潜在特征空间中隐式推理3D场景，无需推理时额外重建或渲染。
- 通过端到端联合优化将重建目标集成到训练管线中，使模型学习结构感知的视觉表示和空间推理能力。
- 去除空间引导（SG）时，ScanRefer验证集上的总体Acc@0.25下降4.78个百分点（16帧输入），证明空间引导对性能的关键作用。
- ScanRefer 上 Overall Acc@0.25 = 59.2%
---

# S$^2$-MLLM: Boosting Spatial Reasoning Capability of MLLMs for 3D Visual Grounding with Structural Guidance

> [!tip] 核心洞察
> 通过联合优化重建损失与定位任务损失，将前馈3D重建的结构感知注入MLLM的视觉表示中，并配合结构增强模块（多级位置编码和视图内/视图间注意力）显式强化位置与跨视角一致性，实现隐式空间推理，显著提升性能与效率。

| 字段 | 内容 |
|------|------|
| 中文题名 | S²-MLLM：通过结构引导提升多模态大语言模型的3D视觉定位空间推理能力 |
| 英文题名 | S$^2$-MLLM: Boosting Spatial Reasoning Capability of MLLMs for 3D Visual Grounding with Structural Guidance |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2512.01223) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction |
| Method | S²-MLLM (S²-MLLM) |
| Dataset | ScanRefer, ScanRefer Multiple, Nr3D, Sr3D |

> [!tip] 效果简介
> - ScanRefer 上，Overall Acc@0.25 59.2% vs 57.2% (MCLN) (+2.0%)；Overall Acc@0.5 52.7% vs 47.9% (Video-3D-LLM†) (+4.8%)。
> - ScanRefer Multiple 上，Acc@0.5 46.6% vs 42.0% (Video-3D-LLM†) (+4.6%)。
> - Nr3D (Pred) 上，Acc@0.25 50.6% vs 46.1% (MCLN) (+4.5%)。

## 概要

**问题瓶颈**：多模态大语言模型（MLLM）主要使用2D视觉输入进行预训练，缺乏理解3D场景空间结构的能力。现有方法依赖显式点云重建和特定视角渲染来提供结构引导，导致推理效率低，且受视角选择与遮挡影响。

**核心思路**：本文提出 **S²-MLLM**，一种通过结构引导提升MLLM空间推理能力的框架。其关键洞察是鼓励模型在训练期间**隐式内化3D结构感知**，从而在潜在特征空间中进行隐式空间推理，推理时无需额外重建或渲染。具体而言，通过联合优化前馈3D重建损失与定位任务损失，将结构感知注入MLLM的视觉表示；配合结构增强模块（多级位置编码和视图内/视图间注意力）显式强化位置与跨视角一致性。

**方法定位**：S²-MLLM属于基于预训练MLLM的任务特定模型，将3D场景表示为视频序列，结合训练时重建监督与推理时纯前馈的隐式空间推理范式。与显式重建+渲染的路线（如 **SeeGround**，CVPR 2025；**GPT4Scene**，ECCV 2024）形成对比，也与端到端监督方法（如 **BUTD-DETR**，Jain et al., ECCV 2022；**EDA**，Wu et al., CVPR 2023）和基于视频的MLLM基线（**Video-3D-LLM**，Zheng et al., CVPR 2025）区分开来。

**主要结果**：在ScanRefer数据集上，S²-MLLM以59.2%的Overall Acc@0.25和52.7%的Overall Acc@0.5全面超越现有方法，较Video-3D-LLM†提升4.8个百分点（Acc@0.5）。在Nr3D和Sr3D上也取得有竞争力的结果，并在MultiScan和ArkiScenes两个分布外数据集上展现出强泛化能力。消融实验确认，空间引导（SG）移除后Overall@0.25下降4.78个百分点，多级位置编码（MPE）贡献最大（移除后退化15.05%），而视图内/视图间注意力（Attn）将基线模型性能从5.31%提升至41.74%。效率方面，S²-MLLM仅需72 GPU小时训练和1.16秒推理延迟，显著优于全参数微调的Video-3D-LLM（256 GPU小时）。



### 3D视觉定位的任务与挑战

3D视觉定位（3D Visual Grounding, 3DVG）要求模型根据自然语言描述在三维场景中定位目标物体，是具身智能与空间理解领域的核心任务之一。该任务的核心难点在于：模型必须同时理解语言中的复杂空间关系（如“桌子左边的棕色沙发”）与三维场景的几何结构，并将二者精确对齐。

近年来，多模态大语言模型（MLLM）在图像和视频理解任务上展现出强大的跨模态推理能力。然而，**MLLM主要使用2D视觉输入进行预训练，缺乏理解3D场景空间结构的能力**，这构成了将其应用于3D视觉定位的根本瓶颈。

### 现有方法的空间引导策略及其局限

为解决MLLM的空间感知缺失问题，现有方法普遍采用“显式重建+渲染”的策略来提供结构引导。如图Figure 1(a)所示，典型流程包括：

1. **显式点云重建**：从多视角RGB-D图像重建场景的3D点云；
2. **特定视角渲染**：将重建点云渲染为BEV（鸟瞰图）或多视角2D图像；
3. **MLLM处理**：将渲染图像与文本查询一同输入MLLM进行定位推理。

代表性工作如**SeeGround**（CVPR 2025）和**GPT4Scene**（ECCV 2024）均遵循这一范式。然而，这种显式策略存在三个显著缺陷：

- **推理效率低**：点云重建和渲染过程增加了额外的推理时间和计算开销；
- **视角选择敏感**：渲染视角的选择直接影响MLLM可获取的空间信息，不恰当的视角可能遗漏关键空间关系；
- **遮挡脆弱性**：在遮挡或稀疏视角条件下，重建质量下降，进而损害下游定位性能。

### 核心洞察：从显式重建到隐式空间推理

本文的核心洞察在于：**MLLM真正需要的并非点云本身，而是对3D场景结构的感知能力**。如果在训练阶段能够将这种结构感知“注入”到MLLM的视觉表示中，模型就有可能在推理时直接进行空间推理，而无需显式重建。

基于这一洞察，本文提出**S²-MLLM**，其设计理念如图Figure 1(b)所示：**在训练阶段引入基于前馈3D重建的空间引导目标，使模型在潜在特征空间内隐式学习3D结构，从而在推理时无需显式重建即可进行空间推理**。这一“训练时引导、推理时隐式”的策略，旨在同时实现高性能、强泛化与高效率的统一。

### 本文动机与目标

综上所述，本文的核心动机可归纳为三个层面：

1. **能力缺口**：MLLM缺乏3D空间结构理解能力，无法直接胜任3D视觉定位任务；
2. **效率瓶颈**：现有显式重建策略在推理效率、视角鲁棒性和遮挡处理上存在固有局限；
3. **范式创新**：通过隐式空间推理的新范式，有望在保持甚至提升定位精度的同时，大幅降低推理开销并增强泛化能力。

本文的目标是设计一个端到端可训练的框架，通过联合优化重建损失与定位任务损失，将前馈3D重建的结构感知注入MLLM的视觉表示中，并配合专门设计的结构增强模块来显式强化位置与跨视角一致性，最终实现高效、鲁棒且可泛化的3D视觉定位。



## 核心方法与创新机理

S²-MLLM 的核心创新在于**将显式3D重建的结构感知能力隐式地注入MLLM的视觉表示中**，使模型在推理时无需任何点云重建或额外渲染即可进行空间推理。这一设计从根本上改变了现有方法“重建-渲染-推理”的范式，转而采用“训练时结构引导、推理时隐式推理”的策略。

### 隐式空间推理：从显式结构引导到潜在空间感知

现有基于MLLM的3D视觉定位方法（如**SeeGround**，CVPR 2025；**GPT4Scene**，ECCV 2024）遵循“先显式重建点云，再渲染BEV或多视角图像供MLLM处理”的流程。这一范式存在两个根本性瓶颈：（1）推理效率低，额外重建和渲染步骤显著增加计算开销；（2）性能受视角选择和遮挡影响，渲染质量直接决定下游定位精度。

S²-MLLM的关键洞察是：**鼓励模型在训练期间隐式内化3D结构感知，使空间推理在潜在特征空间中完成**。具体而言，方法在训练时引入一个基于前馈3D重建的空间引导分支，通过联合优化重建损失与定位任务损失，将3D结构信息注入MLLM的视觉编码器表示中。推理时，该重建分支被完全禁用，模型仅依赖已习得的隐式空间表征进行定位推理，无需任何显式重建或渲染操作。

这一设计构成了方法最核心的**changed slot**：结构引导方式从“显式重建点云并渲染图像”转变为“训练时联合优化前馈3D重建损失，使模型隐式学习3D结构，推理时禁用重建分支”。消融实验提供了决定性证据：当移除空间引导（SG）时，ScanRefer验证集上的总体Acc@0.25下降4.78个百分点（16帧输入），证实了隐式结构学习对性能的关键贡献。

### 结构增强模块：视图内与视图间注意力

多视角特征处理是第二个关键changed slot。基线方法（如**Video-3D-LLM**，Zheng et al., CVPR 2025）通常逐帧独立处理或仅进行简单聚合，缺乏对跨视角空间关系的显式建模。S²-MLLM提出了**结构增强模块（Structure-Enhanced Module, SE）**，采用分治注意力设计：

- **视图内注意力（Intra-view Attention）**：在每个视角内部捕获局部空间依赖关系，增强单帧内的物体结构理解；
- **视图间注意力（Inter-view Attention）**：建立跨视角的语义对应，确保同一物体在不同视角下的特征表示保持一致性。

仅将Attn模块添加到基线模型（LLaVA-Video 7B）上，就将ScanRefer Overall@0.25从5.31%大幅提升至41.74%（Table 8），证明该模块是模型获得基本空间推理能力的核心驱动力。消融实验进一步显示，移除视图内/视图间注意力会降低跨视角语义一致性和物体定位准确性，尤其在视角转换或遮挡条件下表现明显。

### 多级位置编码：3D坐标与视角方向的融合

位置编码的设计构成了第三个changed slot。现有方法通常仅使用2D位置嵌入或简单的3D坐标编码，无法充分表达像素在3D空间中的精确位置和观测方向。S²-MLLM提出**多级位置编码（Multi-level Position Encoding, MPE）**，同时编码两类几何信息：

1. **3D世界坐标的正弦编码**：利用相机内参$K$、外参$T$和深度$d$，将像素$(u,v)$投影到世界坐标系下的3D点$p_{\mathrm{world}}$，并通过正弦函数编码其空间位置；
2. **相机射线方向的MLP编码**：计算归一化射线方向$r = \frac{p_{\mathrm{world}} - o_{\mathrm{world}}}{\| p_{\mathrm{world}} - o_{\mathrm{world}} \|_2}$，使用MLP编码观测视角信息。

最终的位置感知视觉表示通过融合视觉特征、3D坐标编码和射线方向编码得到：
$$f_i^{\mathrm{vis}} = \mathrm{AvgPool} \big( f_i + \phi(p_{\mathrm{world}}^i) \big) + \psi(r_i)$$

消融实验表明，MPE是影响最大的单一组件——移除MPE导致Overall@0.25退化15.05%（Table 5），验证了精确的3D位置和视角信息对空间推理的决定性作用。

### 语言生成监督：语义一致性约束

第四个changed slot是语言监督的形式。传统方法仅使用定位分类损失或对比损失进行训练，忽略了语言描述与视觉定位之间的语义对齐。S²-MLLM额外引入**语言生成损失（Language Guidance, LG）**，要求模型生成目标物体的类别文本（如“The [object category] is located at <ground>”），通过交叉熵损失强化语义一致性。

这一设计将纯定位任务转化为“定位+语义确认”的联合优化问题，使模型在预测边界框的同时必须正确识别物体类别。去除LG会损害模型在复杂场景中对物体类别的正确判别能力，尤其在存在同类干扰物的场景中表现更为明显。

### 创新点总结

| 创新维度 | 基线做法 | S²-MLLM做法 | 证据强度 |
|---------|---------|------------|---------|
| 结构引导方式 | 显式重建点云并渲染图像 | 训练时联合优化重建损失，推理时隐式推理 | 强（消融-4.78% Acc@0.25） |
| 多视角特征处理 | 逐帧独立或简单聚合 | 视图内/视图间分治注意力（SE模块） | 强（Base→+Attn提升36.43% Acc@0.25） |
| 位置编码 | 2D或简单3D嵌入 | 3D世界坐标正弦编码+射线方向MLP编码 | 强（消融-15.05% Acc@0.25） |
| 语言监督 | 仅定位损失 | 增加类别文本生成损失（LG） | 中强（消融显示语义判别能力下降） |

这四个创新点协同作用，使S²-MLLM在ScanRefer上达到59.2% Overall Acc@0.25（超越此前最优的**MCLN** 57.2%），同时仅需72 GPU小时训练和1.16秒推理延迟，在性能和效率之间取得了优越的平衡。



S²-MLLM 的整体设计遵循“训练时隐式学习3D结构，推理时无需显式重建”的核心原则。如图2所示，系统以多视角RGB-D帧序列作为3D场景的表示形式，通过一条精心设计的pipeline将视觉几何特征注入预训练MLLM，最终完成跨模态理解与3D目标定位。

**输入层**：模型接收三类信息——从3D场景中均匀采样的多视角RGB-D图像帧、对应的相机内参与外参、以及自然语言描述查询。同时，一个预训练的3D检测器为场景生成候选目标边界框，作为定位头的分类候选池。

**编码阶段**：共享的视觉编码器（Video Encoder）从每帧RGB-D图像中提取视觉特征 $f_i$。并行地，位置编码器（Position Encoder）利用相机参数和深度图，将每个像素投影到3D世界坐标系，并计算归一化的相机射线方向，生成多级位置嵌入。这一设计使模型能够同时感知像素的绝对空间位置和观测视角信息。

**结构增强模块（Structure-Enhanced Module, SE）**：视觉特征与位置嵌入在SE模块中融合，形成位置感知的视觉表示。SE采用分治注意力设计——视图内注意力捕获单帧内部的局部空间依赖关系，视图间注意力则建立跨视角的语义对应，从而显式强化多视角一致性和空间结构理解。融合后的视觉token序列构成输入LLM的视觉上下文。

**LLM推理与预测头**：Video LLM联合处理视觉token和分词后的文本查询，进行跨模态推理。模型被训练为生成形如“The [object category] is located at \<ground\>”的文本响应，其中\<ground\> token的隐藏状态 $h$ 承载了定位信息。定位头（Grounding Head）通过计算 $h$ 与候选目标区域特征的相似度（InfoNCE损失），预测目标的3D边界框；语言头（Language Head）则生成目标类别文本，强化语义一致性。

**训练时的空间引导分支**：这是S²-MLLM实现隐式空间推理的关键。在训练阶段，LLM编码器的特征通过投影层 $\mathcal{P}$ 映射后，送入重建解码器 $\mathcal{D}$，同时预测局部点图 $X_L$ 和全局点图 $X_G$。重建损失 $\mathcal{L}_{\text{recon}}$ 与定位损失 $\mathcal{L}_{\text{ground}}$、语言损失 $\mathcal{L}_{\text{lang}}$ 通过端到端联合优化，迫使视觉编码器和SE模块学习结构感知的表示。推理时，整个重建分支被完全禁用，模型仅依赖潜在空间中的隐式3D结构感知进行空间推理，无需任何显式点云重建或BEV渲染。

**数据流总结**：多视角RGB-D帧 → 视觉编码器 + 位置编码器 → SE模块（视图内/间注意力融合） → LLM跨模态推理 → 定位头预测边界框 + 语言头生成类别；训练时额外旁路：LLM编码器特征 → 投影层 → 重建解码器 → 点图监督。这一设计在保持推理高效（1.16s延迟，无需重建耗时）的同时，实现了对3D场景结构的深层内化理解。

### 补充图表

![[assets/figures/papers/paper_list_l2413_https_arxiv_org_abs_2512_01223/figures/002_Figure_2.jpg]]
*Figure 2: The Framework of*



S²-MLLM的整体框架如Figure 2所示，其核心设计围绕一个关键洞察展开：**在训练阶段通过前馈3D重建注入空间结构感知，使MLLM在潜在特征空间中隐式推理3D场景，推理时无需显式重建或渲染**。以下按模块逐一分析其设计逻辑与关键公式。

### 3.1 空间引导与隐式重建分支

**设计动机**：现有MLLM主要使用2D视觉输入进行预训练，缺乏理解3D场景空间结构的能力。先前方法（如GPT4Scene、SeeGround）依赖显式重建点云并渲染BEV或多视角图像作为结构引导，导致推理效率低，且受视角选择与遮挡影响。S²-MLLM的关键创新在于将重建目标仅用于训练阶段，使模型隐式内化3D结构感知。

**模块构成**：重建分支由投影层 $\mathcal{P}$ 和解码器 $\mathcal{D}$ 组成。给定输入图像 $I$，视觉编码器 $\mathcal{E}_v$ 提取特征后，经投影层对齐并归一化表示，再通过解码器预测局部点图 $X_L$ 和全局点图 $X_G$：

$$X _ { L } , X _ { G } = \mathcal { D } \big ( \mathcal { P } ( \mathcal { E } _ { v } ( I ) ) \big )$$

解码器 $\mathcal{D}$ 由Fast3R的融合Transformer和解码头组成。**关键约束**：该重建分支仅在训练时激活，推理时被完全禁用，从而实现隐式空间推理。

**点图回归损失**：采用归一化后的L2回归损失，使预测点图与真实点图在尺度归一化后对齐：

$$\ell_{\mathrm{regr}}(\hat{X}, X) = \left\| \frac{1}{\hat{z}} \hat{X} - \frac{1}{z} X \right\|_2, \quad z = \frac{1}{|X|} \sum_{x \in X} \|x\|_2$$

进一步结合预测置信度 $\hat{\Sigma}$ 进行加权：

$$\mathcal{L}_X(\hat{\Sigma}, \hat{X}, X) = \frac{1}{|X|} \sum \hat{\Sigma}_+ \cdot \ell_{\mathrm{regr}}(\hat{X}, X) + \alpha \log(\hat{\Sigma}_+)$$

总重建损失为全局与局部点图损失之和：

$$\mathcal{L}_{\mathrm{recon}} = \mathcal{L}_{X_G} + \mathcal{L}_{X_L}$$

**消融证据**：移除空间引导（SG）后，ScanRefer验证集Overall@0.25下降4.78个百分点（16帧输入），直接验证了隐式结构学习对性能的关键作用。

### 3.2 结构增强模块：视图内/视图间注意力

**设计动机**：多视角视频帧之间存在空间关联与语义对应，逐帧独立处理无法捕获跨视角一致性。S²-MLLM采用分离注意力设计，分别建模视角内空间关系和视角间语义对应。

**视图内注意力**：在单帧内部捕获局部空间依赖，增强物体与场景布局的结构理解。

**视图间注意力**：建立跨视角的语义对应关系，使模型能够在不同视角间关联同一物体或区域，缓解遮挡和视角转换带来的歧义。

**消融证据**：移除视图内/视图间注意力（Attn）会降低跨视角语义一致性和物体定位准确性，尤其在视角转换或遮挡条件下。单独将Attn模块加到Base模型（LLaVA-Video 7B）上，Overall@0.25从5.31%跃升至41.74%，显示该模块对基线的大幅提升作用。

### 3.3 多级位置编码

**设计动机**：仅使用2D位置嵌入无法为MLLM提供足够的3D空间信息。S²-MLLM将3D世界坐标和相机射线方向同时编码，增强视觉特征的空间与视角感知。

**世界坐标投影**：利用相机内参 $K$、外参 $T$ 以及深度 $d$，将像素 $(u,v)$ 投影到世界坐标系：

$$p_{\mathrm{world}} = T \left[ \begin{array}{c} d K^{-1} (u, v, 1)^{\top} \\ 1 \end{array} \right]$$

**相机射线方向**：归一化从射线原点 $o_{\mathrm{world}}$ 指向3D点 $p_{\mathrm{world}}$ 的方向向量：

$$r = \frac{p_{\mathrm{world}} - o_{\mathrm{world}}}{\| p_{\mathrm{world}} - o_{\mathrm{world}} \|_2}$$

**位置感知视觉表示**：将视觉特征 $f_i$、3D坐标的正弦编码 $\phi(p_{\mathrm{world}}^i)$、以及相机射线方向的MLP编码 $\psi(r_i)$ 融合：

$$f_i^{\mathrm{vis}} = \mathrm{AvgPool} \big( f_i + \phi(p_{\mathrm{world}}^i) \big) + \psi(r_i)$$

**消融证据**：移除多级位置编码（MPE）导致Overall@0.25退化15.05%，是所有组件中影响最大的，证明精确的3D位置信息对空间推理至关重要。

### 3.4 定位头与语言监督

**定位头**：将3D视觉定位形式化为对候选对象的分类任务。基于 `<ground>` token的隐藏状态 $h$ 与对象候选区域特征 $f_{\mathrm{obj}}$ 计算相似度，采用InfoNCE损失优化：

$$\mathcal{L}_{\mathrm{ground}} = \mathrm{InfoNCE} \big( f_{\mathrm{obj}}, h \big)$$

**语言头**：引入额外的语言生成监督，要求模型输出形如 “The [object category] is located at <ground>” 的文本，以交叉熵损失 $\mathcal{L}_{\mathrm{lang}}$ 强化语义一致性。

**消融证据**：去除语言指导（LG）会损害复杂场景下对物体类别的正确判别，定性可视化显示缺少LG时模型无法正确识别特定物体类别。

### 3.5 总体训练目标

最终训练目标由定位损失、重建损失和语言生成损失的加权和构成：

$$\mathcal{L} = \lambda_{\mathrm{g}} \mathcal{L}_{\mathrm{ground}} + \lambda_{\mathrm{r}} \mathcal{L}_{\mathrm{recon}} + \lambda_{\mathrm{l}} \mathcal{L}_{\mathrm{lang}}$$

其中权重设置为 $\lambda_{\mathrm{g}}=1.0$，$\lambda_{\mathrm{r}}=0.3$，$\lambda_{\mathrm{l}}=1.0$。该联合优化方案使模型在潜在空间中同时学习定位能力、3D结构感知和语义一致性，实现端到端的隐式空间推理。

### 补充图表

![[assets/figures/papers/paper_list_l2413_https_arxiv_org_abs_2512_01223/figures/001_Figure_1.jpg]]
*Figure 1: Comparison of previous methods and our method. (a) Previous methods typically reconstruct point clouds of 3D scenes explicitly and then render 2D images to obtain structure guidance. (b) Our method leverages spatial guidance to understand the 3D structure during training, allowing the model to perform implicit spatial reasoning in the latent space without requiring point-cloud reconstruction at inference*



## 实验与关键发现

### 主实验结果

S²-MLLM在ScanRefer、Nr3D和Sr3D三个基准上进行了全面评估，并与监督方法、弱监督方法和基于MLLM的方法进行了对比。为公平比较，Video-3D-LLM（Zheng et al., CVPR 2025）采用相同参数量的LoRA微调（标记为†）。

**ScanRefer数据集**（Table 1）：S²-MLLM在IoU 0.25和0.5阈值下均取得最优总体准确率。在Acc@0.25上达到59.2%，超越最强监督基线MCLN（ECCV 2024）的57.2%（+2.0个百分点）；在Acc@0.5上达到52.7%，显著超越Video-3D-LLM†的47.9%（+4.8个百分点）。在更具挑战性的Multiple子集（同类别干扰物场景）上，S²-MLLM在Acc@0.5上达到46.6%，比Video-3D-LLM†高出4.6个百分点，表明模型在处理语义相似物体的空间区分上具有明显优势。

**ReferIt3D数据集**（Table 2）：在使用预测边界框的设定下，S²-MLLM在Nr3D上达到50.6% Acc@0.25，比MCLN的46.1%提升4.5个百分点；在Sr3D上与MCLN持平（53.9%）。值得注意的是，Sr3D使用模板化空间关系描述，S²-MLLM在此设定下未能拉开差距，说明模型对固定表达模式的利用尚有提升空间。

**分布外（OOD）泛化**（Table 4）：在MultiScan和ArkiScenes两个与训练数据场景分布不同的数据集上，S²-MLLM分别取得59.13%和43.26%的Acc@0.25，显著超越零样本方法SeeGround（CVPR 2025），验证了隐式空间推理策略带来的强泛化能力。

### 效率分析

Table 3展示了训练与推理效率的对比。S²-MLLM仅需72 GPU小时完成训练，可训练参数量为1767.50 MB，推理延迟为1.16秒。相比之下，Video-3D-LLM需要256 GPU小时、8078.79 MB可训练参数，推理延迟为1.04秒。SeeGround等需要显式点云重建的方法还需额外的重建时间（t0）。S²-MLLM在训练效率上具有显著优势，且推理时完全不需要点云重建步骤。

### 消融实验

Table 5系统评估了各组件对ScanRefer性能的贡献（16帧输入设定）：

- **空间引导（SG）**：移除SG导致Overall Acc@0.25下降4.78个百分点，直接证明了训练时联合优化前馈3D重建损失对隐式空间推理能力的关键作用。SG使模型在潜在空间内学习3D结构感知，推理时无需显式重建即可进行空间推理。

- **多级位置编码（MPE）**：移除MPE造成Overall Acc@0.25退化15.05%，是影响最大的单一组件。MPE将3D世界坐标的正弦编码与相机射线方向的MLP编码融合到视觉特征中，为结构增强模块提供了精确的空间和视角信息基础。

- **视图内/视图间注意力（Attn）**：移除Attn后性能明显下降。Table 8的附加消融进一步显示，仅将Attn模块添加到基础模型（LLaVA-Video 7B）上，就将Overall Acc@0.25从5.31%大幅提升至41.74%，表明跨视角语义对应和局部空间关系建模对3D定位至关重要。

- **语言指导（LG）**：去除LG会损害模型对复杂场景中物体类别的判别能力。定性可视化（Figure 7）显示，缺少LG时模型无法正确识别棕色沙发等语义模糊的目标。

![[assets/figures/papers/paper_list_l2413_https_arxiv_org_abs_2512_01223/figures/016_Figure_7.jpg]]
*Figure 7: Qualitative ablation results in Scanrefer [9]. Ground Truth is highlighted in mygreen, predictions of our full model are in cyan, and predictions of the model without specific module are in magenta. (SG) Spatial Guidance; (MPE) Multi-level Position Encoding; (Attn) Intra-view and Inter-view Attention; (LG) Language Guidance*

- **输入帧数鲁棒性**：16帧与32帧的性能差异极小，表明S²-MLLM对帧数变化具有较好的鲁棒性。

### 失败模式分析

Figure 4的饼图展示了S²-MLLM在ScanRefer验证集上的错误分布，Figure 5提供了典型失败案例的可视化：

1. **空间关系错误**：涉及多个锚点对象的复杂空间关系描述（如“桌子左边、窗户旁边的椅子”）仍是主要挑战，模型在多步空间推理上存在一定错误率。

2. **语义理解错误**：部分查询中的语义歧义或模糊描述导致模型选择错误的目标物体。

3. **检测误差**：由3D目标检测器提供的不精确候选边界框是主要失误来源之一，尤其在遮挡、部分可见或稀疏视角条件下，检测框本身与真实目标存在偏差，即使模型正确理解查询也无法匹配到正确的候选框。

4. **数据集标注问题**：分析指出ScanRefer等数据集的语言描述存在不准确或不完整的情况，导致模型可能正确匹配描述但与人工标注真值不符，这在一定程度上低估了模型的真实能力。

### 补充图表

![[assets/figures/papers/paper_list_l2413_https_arxiv_org_abs_2512_01223/figures/003_Table_1.jpg]]
*Table 1: Accuracy comparison on Scanrefer [9] validation set at IoU thresholds of 0.25 and 0.5. We report results on the Unique subset (single-object scenes), the Multiple subset (scenes with same-class distractors), and the overall accuracy. * denotes results obtained by LoRA [20] fine-tuning with the same parameter size as ours, while other settings follow the original paper*

![[assets/figures/papers/paper_list_l2413_https_arxiv_org_abs_2512_01223/figures/004_Table_2.jpg]]
*Table 2: Accuracy comparison on Nr3D and Sr3D [2] validation set with both predicted at IoU thresholds of 0.25 and ground-truth bounding boxes as input*

![[assets/figures/papers/paper_list_l2413_https_arxiv_org_abs_2512_01223/figures/008_Table_5.jpg]]
*Table 5: Ablation study on the ScanRefer [9] dataset. We evaluate the contribution of each proposed component and the impact of the number of input frames. (SG) Spatial Guidance; (MPE) Multi-level Position Encoding; (Attn) Intra-view and Inter-view Attention; (LG) Language Guidance*

![[assets/figures/papers/paper_list_l2413_https_arxiv_org_abs_2512_01223/figures/006_Table_3.jpg]]
*Table 3: Efficiency comparison. We report the training cost (in GPU hours), trainable parameters (in MB), and the inference latency (in seconds). t0 represents the additional inference time of reconstructing point clouds*

![[assets/figures/papers/paper_list_l2413_https_arxiv_org_abs_2512_01223/figures/007_Table_4.jpg]]
*Table 4: Out-of-Distribution (OOD) Evaluation on Multiscan [42] and ArkiScenes [4]*

![[assets/figures/papers/paper_list_l2413_https_arxiv_org_abs_2512_01223/figures/011_Table_8.jpg]]
*Table 8: Ablation study on the ScanRefer [9] dataset. We evaluate the contribution of inter-view and intra-view attention (Attn)*

![[assets/figures/papers/paper_list_l2413_https_arxiv_org_abs_2512_01223/figures/005_Figure.jpg]]
*Figure: (b) Viewpoint Dependency (c) Occlusion (e) Mul�ple Anchors (f) Order*

![[assets/figures/papers/paper_list_l2413_https_arxiv_org_abs_2512_01223/figures/014_Figure_6.jpg]]
*Figure 6: Qualitative comparison of 3DVG results in Nr3D [2]. Ground Truth is highlighted in green, our predictions in cyan, and predictions of SeeGround [34] in magenta*

![[assets/figures/papers/paper_list_l2413_https_arxiv_org_abs_2512_01223/figures/012_Figure_4.jpg]]
*Figure 4: Error type analysis on ScanRefer [9] dataset*



## 定位与知识库关联

### 1. 与现有方法的关系

#### 1.1 3D视觉定位方法谱系

3D视觉定位（3D Visual Grounding, 3DVG）旨在根据自然语言描述在3D场景中定位目标物体。现有方法可分为三类：

**（1）监督式专用模型。** 这类方法直接针对3DVG任务设计，通常依赖点云或3D体素输入，并利用目标检测器提供的候选框进行分类。
- **BUTD-DETR**（Jain et al., ECCV 2022）是经典的端到端3D视觉定位方法，将语言特征与3D场景特征进行跨模态融合。
- **EDA**（Wu et al., CVPR 2023）提出一阶段定位框架，避免了单独的目标检测步骤。
- **MCLN**（ECCV 2024）引入多线索语言引导机制，增强了对复杂空间描述的理解。在ScanRefer数据集上，MCLN取得了57.2%的Overall Acc@0.25，是S²-MLLM出现前的最强监督基线。

**（2）基于MLLM的方法。** 近年来，借助多模态大语言模型（MLLM）的跨模态理解能力进行3DVG成为新兴范式。
- **Video-3D-LLM**（Zheng et al., CVPR 2025）将3D场景表示为视频序列，利用视频MLLM进行场景理解，代表了最新的基于视频的MLLM基线。本文将其用LoRA微调至相同参数量（7B）进行公平对比。
- **SeeGround**（CVPR 2025）是基于VLM的零样本3DVG方法，通过显式重建点云并渲染BEV/多视角图像来提供结构指导。
- **GPT4Scene**（ECCV 2024）同样使用重建点云并渲染BEV图像的方式为MLLM提供全局场景信息。

**（3）S²-MLLM的方法学定位。** S²-MLLM处于监督式专用模型与MLLM方法的交叉地带。它继承了MLLM的跨模态理解优势，但通过引入空间引导（Spatial Guidance）和结构增强模块（Structure-Enhanced Module），弥补了MLLM缺乏3D空间结构感知的根本缺陷。与SeeGround和GPT4Scene的显式重建-渲染范式不同，S²-MLLM的**核心创新在于将3D结构学习隐式化**——训练时通过联合优化前馈3D重建损失使模型内化空间感知，推理时完全禁用重建分支，在潜在特征空间中进行隐式空间推理。

#### 1.2 关键差异：隐式 vs 显式结构引导

先前方法（SeeGround、GPT4Scene）的典型流程为：重建点云 → 渲染BEV/多视角图像 → 输入MLLM处理。这一范式存在三个根本性问题：
- **推理效率低**：需要额外的重建和渲染时间（SeeGround的t0重建时间即为额外开销）。
- **视角选择敏感**：渲染视角的选择直接影响MLLM可获取的结构信息质量。
- **遮挡脆弱性**：渲染图像中的遮挡区域会丢失关键空间信息。

S²-MLLM通过**训练时空间引导**解决了上述问题。如Figure 1所示，本文方法将重建目标集成到训练管线中，使模型在潜在空间中学习结构感知的视觉表示。推理时仅需1.16s，无需任何显式重建。这一设计在方法学上实现了从“显式重建-理解”到“隐式感知-推理”的范式转变。

### 2. 适用边界与局限

#### 2.1 适用边界

S²-MLLM的设计适用于以下场景：
- **多视角RGB-D输入可用**：模型依赖采样的多视角RGB-D帧及相机参数，适用于室内扫描场景（如ScanNet、3RScan）和类似的3D场景理解任务。
- **目标检测器提供候选框**：当前框架将3DVG建模为候选框分类问题，依赖外部检测器（如PointGroup）提供目标候选区域。
- **语言描述以空间关系为主**：模型在涉及空间关系（如“左边的椅子”、“桌子后面的柜子”）的任务上表现突出，在ScanRefer的Multiple子集（同类干扰物场景）上取得46.6% Acc@0.5，比Video-3D-LLM提升4.6个百分点。

#### 2.2 已知局限

**（1）检测器误差传播。** 错误分析（Figure 4）显示，检测误差是主要失误来源之一。当目标检测器提供的候选框不精确时（尤其在遮挡、部分可见或稀疏视角条件下），模型无法正确匹配目标。这表明S²-MLLM的性能受限于上游检测器的质量。

**（2）复杂多锚点空间推理。** 对于涉及多个锚点对象的复杂空间关系描述（如“在A和B之间的C旁边的D”），模型仍存在一定错误率。Figure 5中的空间类失败案例展示了这一局限，说明多步空间推理能力有待进一步增强。

**（3）模板化表达的利用不足。** 在Sr3D数据集上，S²-MLLM的Pred Acc@0.25为53.9%，与MCLN持平，但略低于某些专门设计的完全监督方法。Sr3D使用模板化的空间关系表达（如“the chair closest to the table”），模型对这类固定模式的利用不如对自然语言描述灵活。

**（4）数据集标注质量。** 分析指出，3DVG数据集（如ScanRefer）的语言描述存在不准确或不完整的情况，导致模型可能正确匹配描述但与人工标注真值不符，影响性能评估的准确性。

### 3. 开放问题与未来方向

基于S²-MLLM的方法框架和已知局限，以下开放问题值得进一步探索：

1. **极端条件下的鲁棒性**：如何进一步提高在严重遮挡和极端稀疏视角下的3D空间定位鲁棒性？当前方法依赖多视角覆盖，在视角极度受限时性能可能显著退化。

2. **任务泛化能力**：隐式空间推理策略能否扩展到其他3D场景理解任务？例如3D问答（3D QA）、密集字幕生成（Dense Captioning）和具身导航等。当前框架仅针对3DVG验证了有效性。

3. **效率进一步优化**：S²-MLLM的训练效率已显著优于Video-3D-LLM（72 GPU小时 vs 256 GPU小时），但可训练参数量（1767.50MB）仍有压缩空间。能否通过更激进的参数高效微调策略进一步降低训练成本？

4. **自适应视角选择**：当前方法使用均匀采样的固定数量帧（16帧），消融实验显示帧数对性能影响不大。未来能否结合主动视角选择或自适应帧采样策略，以更少的帧数达到最优的空间理解？

5. **数据集质量改进**：如何改进3DVG数据集的质量，减少语言描述歧义和标注不一致？更准确的评估基准对于衡量模型真实的空间推理能力至关重要。

### 4. 知识库定位总结

S²-MLLM在3D视觉定位领域的知识贡献可归纳为：

| 维度 | 定位 |
|------|------|
| **任务** | 3D视觉定位（3DVG），基于自然语言描述定位3D场景中的目标物体 |
| **范式创新** | 从“显式重建-理解”到“隐式感知-推理”的范式转变 |
| **核心技术** | 训练时空间引导（联合优化重建损失）、结构增强模块（视图内/视图间注意力）、多级位置编码 |
| **基础模型** | LLaVA-Video 7B，以视频序列表示3D场景 |
| **性能水平** | ScanRefer Overall Acc@0.25达59.2%，超越所有监督和MLLM基线 |
| **效率优势** | 72 GPU小时训练，1.16s推理延迟，无需推理时重建 |
| **泛化能力** | 在MultiScan和ArkiScenes两个分布外数据集上显著超越SeeGround |



## 原文 PDF

![[paperPDFs/CVPR_2026/S_2_MLLM_Boosting_Spatial_Reasoning_Capability_of_MLLMs_for_3D_Visual_Grounding_with_Structural_Guidance.pdf]]
