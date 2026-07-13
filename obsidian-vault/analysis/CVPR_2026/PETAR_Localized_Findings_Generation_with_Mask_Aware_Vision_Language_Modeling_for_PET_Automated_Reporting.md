---
title: "PETAR: Localized Findings Generation with Mask-Aware Vision-Language Modeling for PET Automated Reporting"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/PETAR_Localized_Findings_Generation_with_Mask_Aware_Vision_Language_Modeling_for_PET_Automated_Reporting.pdf
project_link: null
code_link: null
aliases:
- P4
- PETAR
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
- topic/generative_models_diffusion
- topic/benchmarks_datasets_evaluation
core_operator: 将3D分割掩码与PET/CT体积以掩码感知的方式联合编码，并引入高分辨率聚焦提示，保留病灶细节信息，使模型能够学习从掩码空间到语言描述的映射。
primary_logic: 通过掩码条件化的多模态视觉编码（PET+CT+Mask）与聚焦提示机制，模型同时获取全局疾病分布和局部病灶属性，显著提高了报告生成中的空间定位准确性和临床内容可信度。
claims:
- 消融实验中，仅添加masks即可在GREEN分数上带来+0.017的提升；加入CT后语义一致性指标提升；引入focal prompt后指标全面提升，尤其CIDEr从0.134跃升至0.397，GREEN从0.060升至0.226，证明聚焦提示对细粒度描述至关重要。
- 人工评估中，PETAR-4B在解剖准确性、解读正确性和临床实用性三项评分均达到3.7–3.9，与人类报告的4.3–4.4接近；医生在约60%的案件中认为模型生成结果等于或优于人工报告。
- 跨数据集泛化（AutoPET）同样表现稳健，三项人工评分均在3.8–4.0之间。
- PETARSeg-11k test set 上 BLEU-4 = 0.535
---

# PETAR: Localized Findings Generation with Mask-Aware Vision-Language Modeling for PET Automated Reporting

> [!tip] 核心洞察
> 通过掩码条件化的多模态视觉编码（PET+CT+Mask）与聚焦提示机制，模型同时获取全局疾病分布和局部病灶属性，显著提高了报告生成中的空间定位准确性和临床内容可信度。

| 字段 | 内容 |
|------|------|
| 中文题名 | PETAR：基于掩码感知视觉语言建模的PET自动报告局部发现生成 |
| 英文题名 | PETAR: Localized Findings Generation with Mask-Aware Vision-Language Modeling for PET Automated Reporting |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2510.27680) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction #topic/generative_models_diffusion #topic/benchmarks_datasets_evaluation |
| Method | PETAR-4B |
| Dataset | PETARSeg-11k test set, Internal Reader Study, External AutoPET Dataset |

> [!tip] 效果简介
> - PETARSeg-11k test set 上，BLEU-4 0.535 vs 0.495 (MedGemma-4B finetuned, 最强2D) (+0.040)；BERTScore 0.795 vs 0.750 (M3D-RAD finetuned, 最强3D) (+0.045)；GREEN 0.257 vs 0.071 (M3D-RAD finetuned) (+0.186)。
> - Internal Reader Study (5 physicians) 上，Mean Anatomical / Interpretation / Utility Score 3.9 / 3.9 / 3.7 vs 4.4 / 4.4 / 4.3 (Human original reports) (-0.5 / -0.5 / -0.6)。
> - External AutoPET Dataset 上，Mean Anatomical / Interpretation / Utility Score 3.8 / 4.0 / 3.8 vs N/A (no human reference available) (N/A)。

## 概要

PET/CT是肿瘤学中广泛使用的成像模态，其报告生成高度依赖核医学医师对三维体积中病灶的逐一描述，耗时且易出现疏漏。现有3D视觉-语言模型（VLMs）通常采用全局编码与下采样策略，导致体积占比平均小于0.1%的微小病灶的细粒度信息丢失，无法实现精确的视觉-文本空间对齐，生成的描述往往模糊或临床不完整。

针对这一瓶颈，本文提出**PETAR-4B**，一种面向PET/CT病灶发现生成的3D掩码感知视觉-语言模型。其核心思路是：将3D分割掩码与PET/CT体积以掩码感知的方式联合编码，并引入高分辨率聚焦提示（focal prompt），使模型能够同时获取全局疾病分布和局部病灶属性，从而学习从掩码空间到语言描述的精确映射。

在自动评估中，PETAR-4B显著优于所有2D和3D基线模型——在GREEN分数上达到0.257，较最强3D基线M3D-RAD的0.071提升0.186；在BLEU-4和BERTScore上也分别取得0.535和0.795的最佳结果。由五位核医学医师参与的盲法评估进一步证实了其临床价值：模型在解剖准确性、解读正确性和临床实用性三项评分上达到3.7–3.9（人类报告为4.3–4.4），医生在约60%的案件中认为模型生成结果等于或优于人工报告。跨数据集泛化实验（AutoPET）同样表现稳健，三项评分均在3.8–4.0之间。

### 临床需求与现有报告的瓶颈

正电子发射断层扫描/计算机断层扫描（PET/CT）是肿瘤学诊断、分期与疗效评估的核心影像工具。一份典型的PET/CT结构化报告包含临床指征、扫描方案、定性发现以及定量测量（如最大标准化摄取值 $\operatorname{SUV}_{\operatorname*{max}}$）等关键字段。其中，**病灶级发现描述**是报告的核心临床价值所在——它要求对每个病灶的解剖位置、代谢活性、形态特征及临床意义进行精确的文字刻画。

然而，撰写高质量的病灶发现极为耗时，且高度依赖核医学专家的经验，导致报告周转时间长、不同阅片者间一致性有限。自动化报告生成的引入有望缓解这一矛盾，但其核心挑战在于：**如何从高分辨率3D体积中提取并描述通常仅占总体积不足0.1%的微小病灶。**

### 现有视觉-语言模型的根本缺陷

近年来，通用领域与医学领域的视觉-语言模型（VLM）在2D图像理解与描述任务上取得了显著进展。然而，当这些模型被直接应用于3D PET/CT体积的报告生成时，暴露出一个根本性的瓶颈：

- **全局编码导致细粒度信息丢失**：现有3D VLM（如 **M3D**、**Med3DVLM**、**M3D-RAD**）通常采用全局特征编码与下采样策略。对于体积占比极小的病灶而言，这种全局压缩不可避免地淹没了其微弱的空间信号，使得模型无法建立精确的视觉-文本空间对齐。
- **2D VLM的维度割裂**：以 **MedGemma-4B**（Sellergren et al., 2025）、**HuatuoGPT-Vision-7B**、**Qwen3-VL-8B** 等为代表的2D VLM，在评估时仅能输入矢状、冠状、轴向三个代表性切片，从根本上丧失了完整的3D空间上下文，难以胜任需要立体解剖定位的PET报告任务。
- **掩码感知的缺失**：即便是少数引入了分割掩码的工作（如2D的 **ViP-LLaVA** 或3D器官级的 **Reg2RG**），也未能将掩码作为视觉编码的条件信号与高分辨率聚焦机制深度耦合，导致模型在“看到”病灶位置后仍无法生成足够精细的局部描述。

上述缺陷的集中体现是：现有模型生成的报告普遍存在**解剖定位错误、病灶属性描述模糊、临床信息不完整**等问题，与临床实际需求之间存在显著鸿沟。

### 本文的核心动机与解决思路

针对上述瓶颈，本文的核心动机是：**赋予VLM以“掩码感知”的3D病灶理解能力，使其能够同时掌握全局疾病分布与局部病灶属性，从而生成解剖精确、临床可信的病灶发现。**

这一动机直接催生了 **PETAR-4B** 的设计——一个掩码感知的3D视觉-语言模型。其关键突破在于：

1. **掩码条件化的多模态编码**：将3D病灶分割掩码与PET/CT体积联合输入，使视觉编码过程以病灶位置为条件，从源头上保留细粒度信息。
2. **3D聚焦提示机制**：在掩码引导下提取病灶区域的高分辨率立方体，与全局特征融合，解决微小病灶的信息淹没问题。

通过这一“掩码→空间→语言”的因果链路，PETAR-4B 旨在弥合现有VLM与临床报告生成之间的关键缺口，为自动化PET报告生成提供一条从病灶定位到精细描述的全新路径。

## 核心方法与创新机理

PETAR-4B 的核心创新在于将**3D病灶分割掩码**作为显式条件引入视觉-语言建模管线，从而解决了现有3D VLM因全局编码与下采样导致微小病灶（体积占比通常<0.1%）细粒度信息丢失的根本瓶颈。围绕这一思路，模型在四个关键维度上相对于基线方法做出了实质性改变。

### 1. 掩码感知的多模态编码（Mask-Aware Encoding）

现有3D VLM（如 M3D-RAD、Med3DVLM）仅以PET或CT体积作为输入，缺乏对病灶空间位置的显式建模。PETAR-4B 将二值病灶掩码 $M$ 与PET体积 $P$ 在视觉编码前进行特征级融合：

$$\mathbf{X}_{\mathrm{PET}} = \mathcal{T}(Z_P + Z_M)$$

其中 $Z_P$ 和 $Z_M$ 分别为PET和掩码的3D补丁嵌入，$\mathcal{T}$ 为共享的3D Vision Transformer。这种**相加式掩码条件化**使得模型在编码阶段即获得病灶的空间先验，而非依赖后续的注意力机制隐式学习。消融实验证实，仅添加掩码输入即可在GREEN分数上带来 **+0.017** 的提升，并在RaTEScore等事实准确性指标上表现显著增益（Table 3）。

### 2. 聚焦提示机制（Focal Prompt）

这是PETAR-4B最具区分度的设计。传统方法仅以全局下采样体积作为输入，导致微小病灶的纹理和代谢细节被淹没。PETAR-4B 借鉴 Describe Anything Model 的思想，提出**3D聚焦提示**：

- 基于掩码中心 $c$ 和裁剪尺寸 $r$ 施加随机扰动：$\tilde{c} = c + \triangle c,\ \tilde{r} = r + \triangle r$，其中 $\triangle c, \triangle r \stackrel{\mathrm{i.i.d.}}{\sim} \mathcal{U}(-0.2r, 0.2r)$；
- 提取高分辨率聚焦子体积 $\mathcal{F}_P, \mathcal{F}_C, \mathcal{F}_M = \mathrm{Crop}(P, C, M; \tilde{c}, \tilde{r})$；
- 将聚焦特征 $\tilde{\mathbf{X}}$ 与全局特征 $\mathbf{X}$ 按元素相加：$\mathbf{T} = \mathbf{X} + \tilde{\mathbf{X}}$。

消融实验表明，聚焦提示带来的增益**远超其他组件**：CIDEr从0.134跃升至0.397，GREEN从0.060提升至0.226（Table 3 第四行 vs 第三行）。这验证了高分辨率局部信息对于细粒度病灶描述（如“右肺上叶尖段胸膜下结节，SUVmax轻度增高”）的不可替代性。

### 3. PET-CT联合编码

不同于仅使用PET的基线方法，PETAR-4B 将CT体积 $C$ 作为独立模态进行编码（$\mathbf{X}_{\mathrm{CT}} = \mathcal{T}(Z_C)$），并与PET特征沿嵌入维度拼接：

$$\mathbf{X} = \mathrm{Concat}(\mathbf{X}_{\mathrm{PET}}, \mathbf{X}_{\mathrm{CT}})$$

CT提供了解剖结构信息，弥补了PET在空间定位精度上的不足。消融实验中，加入CT后BERTScore和GREEN均有所提升，表明解剖一致性得到增强（Table 3 第三行 vs 第一行）。

### 4. TotalSegmentator解剖预训练

为进一步强化模型对解剖结构的理解，PETAR-4B 在 TotalSegmentator 分割数据上进行了三阶段预训练。这一设计为模型提供了器官级别的空间先验，在消融实验中带来了小幅但一致的性能提升（Table 3 最后两行），尤其有助于多病灶场景下的解剖定位准确性。

### 创新总结

上述四个 changed slots 构成了一个**从粗到细、从全局到局部**的层次化视觉编码体系：TotalSegmentator预训练提供器官级解剖先验，PET-CT联合编码提供全局代谢与结构上下文，掩码感知编码注入病灶空间位置，聚焦提示保留病灶细节纹理。这一体系使得模型能够同时捕捉“疾病分布”和“病灶属性”两个层次的临床信息，从而在空间定位准确性和描述粒度上显著超越现有2D和3D基线方法。

PETAR-4B 是一个面向 PET/CT 自动化报告生成的 3D 掩码感知视觉语言模型，其核心设计目标是解决现有 3D VLM 中微小病灶（体积占比通常不足 0.1%）在全局下采样过程中信息丢失的问题。模型以 PET 体积 $P$、CT 体积 $C$ 和 3D 病灶分割掩码 $M$ 为联合输入，输出病灶级的自然语言发现描述 $y$，形式化为：

$$y = f_{\theta}(P, C, M)$$

整体架构由五个关键模块串联而成，形成“多模态编码—聚焦增强—特征融合—空间压缩—语言解码”的端到端流程。

**1. 3D Patch Embedding（补丁嵌入）**
三种模态（PET、CT、Mask）首先被切分为非重叠的 3D 补丁，并分别通过独立的线性投影层映射到 $d$ 维嵌入空间，得到 $Z_P$、$Z_C$、$Z_M \in \mathbb{R}^{K \times d}$。其中，Mask 使用独立的投影参数，以保留其作为空间先验的特殊语义。

**2. Shared 3D Vision Transformer（共享视觉编码）**
PET 嵌入与 Mask 嵌入按元素相加后，送入一个共享的 3D Vision Transformer $\mathcal{T}$，实现掩码条件化的视觉编码：$\mathbf{X}_{\text{PET}} = \mathcal{T}(Z_P + Z_M)$。CT 嵌入则独立通过同一 Transformer：$\mathbf{X}_{\text{CT}} = \mathcal{T}(Z_C)$。这一设计使模型在编码 PET 特征时显式感知病灶的空间位置，同时保持 CT 解剖信息的独立性。随后，两者沿嵌入维度拼接，得到全局视觉表示 $\mathbf{X} = \text{Concat}(\mathbf{X}_{\text{PET}}, \mathbf{X}_{\text{CT}})$。

**3. Focal Crop Extractor（聚焦裁剪器）**
为弥补全局编码对微小病灶的细节丢失，模型在 Mask 中心 $c$ 和裁剪半径 $r$ 上施加随机扰动：

$$\tilde{c} = c + \triangle c,\quad \tilde{r} = r + \triangle r,\quad \triangle c, \triangle r \stackrel{\mathrm{i.i.d.}}{\sim} \mathcal{U}(-0.2r, 0.2r)$$

基于扰动后的中心和尺寸，从 PET、CT、Mask 中提取高分辨率聚焦子体积 $\mathcal{F}_P, \mathcal{F}_C, \mathcal{F}_M$。这些子体积同样经过补丁嵌入和共享 Transformer 编码，生成聚焦视觉特征 $\tilde{\mathbf{X}}$。

**4. Global-Focal Fusion（全局-聚焦融合）**
全局特征与聚焦特征按元素相加：$\mathbf{T} = \mathbf{X} + \tilde{\mathbf{X}}$。这一简洁的融合策略使模型同时保有全局疾病分布信息（如多发病灶的空间关系）和局部病灶的细粒度属性（如代谢活性、边界特征）。

**5. Spatial Pooler & Projector + LLM Decoder**
融合后的视觉 token $\mathbf{T}$ 首先经过空间池化压缩序列长度，再通过线性投影映射到语言模型的嵌入空间：$\mathbf{V} = \text{Proj}(\text{SpatialPooler}(\mathbf{T}))$。最终，视觉 token $\mathbf{V}$ 与文本查询 $q$ 一同送入基于 Phi3-4B 的 LLM 解码器，以自回归方式生成病灶描述，训练目标为标准负对数似然损失。

**数据流的因果逻辑**：Mask 的引入解决了“在哪里看”的问题，使视觉编码具有空间选择性；CT 模态的加入补充了“周围是什么”的解剖上下文；聚焦提示则回答了“细节是什么”，三者协同作用，将原本被全局下采样淹没的微小病灶信息重新注入表征空间。消融实验证实了这一设计的有效性：仅添加 Mask 即可使 GREEN 分数提升 +0.017；加入 CT 后语义一致性指标（BERTScore）进一步提升；而引入 Focal Prompt 带来的增益最为显著——CIDEr 从 0.134 跃升至 0.397，GREEN 从 0.060 升至 0.226，证明聚焦机制对细粒度描述至关重要（Table 3）。

![[assets/figures/papers/paper_list_l2333_https_arxiv_org_abs_2510_27680/figures/004_Figure_3.jpg]]
*Figure 3: Overview of the proposed framework. The left panel illustrates the overall architecture, which integrates PET, CT, and lesion mask inputs through 3D convolutional image projectors and an M3D-CLIP backbone. The resulting multi-modal visual tokens are fused and spatially pooled before being passed to a Phi3-4B language model that generates clinically grounded text descriptions conditioned on visual features and textual prompts. The right panel details the Image Encoder design, where modality-specific projectors (for PET, CT, and mask inputs) map each input into a shared latent space. These embeddings are subsequently processed by a ViT encoder to produce modality-aligned visual tokens for dow...*

![[assets/figures/papers/paper_list_l2333_https_arxiv_org_abs_2510_27680/figures/001_Figure_1.jpg]]
*Figure 1: Overview of mask-guided PET/CT report generation. By incorporating lesion-level masks, PETAR produces anatomically fine-grained findings grounded in the 3D volume. In contrast, general 3D models perform global encoding without fine-grained anatomical correlation, hence they generate vague or clinically incomplete descriptions*

PETAR-4B 的核心架构围绕一个统一的生成目标展开：

$$y = f_{\theta}(P, C, M)$$

其中 $P$ 为 PET 体积，$C$ 为 CT 体积，$M$ 为 3D 病灶分割掩码，模型输出结构化病灶描述 $y$。该目标通过以下关键模块实现。

### 3D 聚焦提示

现有 3D VLM 普遍采用全局编码与下采样，导致体积占比平均小于 0.1% 的微小病灶信息丢失。PETAR 通过聚焦提示（Focal Prompt）机制解决此瓶颈：以掩码中心 $c$ 和裁剪尺寸 $r$ 为基准，施加随机扰动以增强鲁棒性：

$$\tilde{c} = c + \triangle c,\quad \tilde{r} = r + \triangle r$$

$$\triangle c, \triangle r \stackrel{\mathrm{i.i.d.}}{\sim} \mathcal{U}(-0.2r, 0.2r)$$

随后提取高分辨率聚焦子体积：

$$\mathcal{F}_P, \mathcal{F}_C, \mathcal{F}_M = \mathrm{Crop}(P, C, M; \tilde{c}, \tilde{r})$$

该模块使模型在保留全局疾病分布上下文的同时，获取病灶局部的细粒度代谢与解剖属性。

### 掩码感知多模态视觉编码

PET、CT 和掩码分别通过 3D 补丁嵌入层转化为 $K$ 个 $d$ 维 token：

$$Z_P = \mathrm{PatchEmbed}(P) \in \mathbb{R}^{K \times d}$$

$$Z_C = \mathrm{PatchEmbed}(C) \in \mathbb{R}^{K \times d}$$

$$Z_M = \mathrm{PatchEmbed}(M) \in \mathbb{R}^{K \times d}$$

掩码感知编码的核心在于将掩码嵌入与 PET 嵌入按元素相加后送入共享 3D Vision Transformer $\mathcal{T}$，实现掩码条件化的视觉特征提取；CT 嵌入则独立编码：

$$\mathbf{X}_{\mathrm{PET}} = \mathcal{T}(Z_P + Z_M),\quad \mathbf{X}_{\mathrm{CT}} = \mathcal{T}(Z_C)$$

全局特征通过拼接融合：

$$\mathbf{X} = \mathrm{Concat}(\mathbf{X}_{\mathrm{PET}}, \mathbf{X}_{\mathrm{CT}})$$

### 全局-聚焦融合与语言解码

聚焦模块提取的特征 $\tilde{\mathbf{X}}$ 与全局特征 $\mathbf{X}$ 按元素相加，形成统一的视觉表示：

$$\mathbf{T} = \mathbf{X} + \tilde{\mathbf{X}}$$

随后经空间池化压缩 token 数量，再通过可学习的投影层映射到语言模型嵌入空间：

$$\mathbf{V} = \mathrm{Proj}(\mathrm{SpatialPooler}(\mathbf{T}))$$

最终由 Phi3-4B 语言模型以自回归方式生成病灶描述，训练损失为标准负对数似然：

$$\mathcal{L}(\mathcal{D}, \theta) = -\sum_{(\mathbf{V},q,y)\sim\mathcal{D}}\sum_{i=1}^{N}\log p_{\theta}(y_i \mid \mathbf{V}, q, y_{<i})$$

其中 $q$ 为文本查询提示，$y_{<i}$ 为已生成的前缀 token。

### 因果机制小结

整个管线的因果杠杆在于：掩码与 PET 的相加式编码建立了从掩码空间到语言描述的显式映射通路，聚焦提示则补偿了全局下采样造成的细粒度信息损失。消融实验证实，仅添加掩码即可使 GREEN 分数提升 +0.017，而聚焦提示的引入使 CIDEr 从 0.134 跃升至 0.397、GREEN 从 0.060 升至 0.226（Table 3），验证了该机制对细粒度描述的决定性作用。

![[assets/figures/papers/paper_list_l2333_https_arxiv_org_abs_2510_27680/figures/006_Table_3.jpg]]
*Table 3: Ablation study of our model showing the effect of each component on multiple evaluation metrics. TS=TotalSegmentator pretraining*

## 实验与关键发现

### 核心实验设置

**数据集**：实验基于自建的 **PETARSeg-11k** 数据集，该数据集包含 11,000 个病灶级 PET/CT 发现描述与对应的 3D 分割掩码。测试集用于所有自动评估指标的主实验，内部测试集（116 例）和外部 **AutoPET** 数据集（32 例）用于人工评估。

**基线选择**：对比方法分为两大类：
- **2D VLMs**：MedGemma-4B（Sellergren et al., 2025）、HuatuoGPT-Vision-7B、InternVL3-8B、Qwen3-VL-8B、QoQ-Med、ViP-LLaVA。2D 模型在推理时仅输入矢状、冠状、轴向三个代表性切片，这可能导致 3D 空间信息利用不充分。
- **3D VLMs**：M3D、Med3DVLM、M3D-RAD、Reg2RG。3D 模型在推理时输入完整体积。

**评估指标**：采用 8 项自动评估指标，包括 BLEU-4、ROUGE-L、METEOR、CIDEr、BERTScore、BARTScore、RaTEScore 和 GREEN。其中 GREEN 与专家判断的 Spearman 相关系数最高（0.592），而 BLEU 仅为 0.214（Table 4），说明传统 n-gram 指标与临床偏好存在显著偏差。

**人工评估**：五位核医学医师在盲法条件下对 PETAR-4B 生成结果与原始报告进行评分，评估维度包括解剖准确性（Anatomical Accuracy）、解读正确性（Interpretation Accuracy）和临床实用性（Overall Utility），采用 1–5 分制。为消除模型幻觉对定量测量（SUVmax、尺寸）的影响，所有报告中的数值均替换为 `[#]`。

---

### 主实验结果

**Table 2** 展示了 PETAR-4B 与各基线在 PETARSeg-11k 测试集上的全面对比：

| 指标 | PETAR-4B | 最强 2D（MedGemma-4B finetuned） | 最强 3D（M3D-RAD finetuned） |
|------|----------|--------------------------------|------------------------------|
| BLEU-4 | **0.535** | 0.495 | 0.491 |
| ROUGE-L | **0.524** | 0.454 | 0.454 |
| METEOR | **0.560** | 0.510 | 0.510 |
| CIDEr | **0.457** | 0.329 | 0.322 |
| BERTScore | **0.795** | 0.720 | 0.750 |
| RaTEScore | **0.713** | 0.573 | 0.627 |
| GREEN | **0.257** | 0.060 | 0.071 |

PETAR-4B 在所有自动指标上均取得最优。与最强 2D 基线 MedGemma-4B 相比，BLEU-4 提升 0.040，ROUGE-L 提升 0.070；与最强 3D 基线 M3D-RAD 相比，BERTScore 提升 0.045，RaTEScore 提升 0.086。**最显著的优势体现在 GREEN 指标上**：PETAR-4B 的 0.257 远超 M3D-RAD 的 0.071（+0.186），说明掩码感知的视觉编码显著提升了病灶定位和事实准确性。

**Figure 4** 的定性对比进一步印证了这一结论：微调前的 MedGemma 和 M3D-RAD 产生高度不准确的描述；微调后这些模型仍倾向于出现定位错误（红色下划线标注），而 PETAR 持续生成解剖学正确的描述（绿色下划线标注）。

---

### 人工评估结果

**Table 5** 展示了人工评估的完整结果：

| 数据集 | 评分维度 | PETAR-4B | 人类原始报告 |
|--------|---------|----------|-------------|
| 内部测试集 | 解剖准确性 | 3.9 | 4.4 |
| 内部测试集 | 解读正确性 | 3.9 | 4.4 |
| 内部测试集 | 临床实用性 | 3.7 | 4.3 |
| AutoPET 外部集 | 解剖准确性 | 3.8 | N/A |
| AutoPET 外部集 | 解读正确性 | 4.0 | N/A |
| AutoPET 外部集 | 临床实用性 | 3.8 | N/A |

PETAR-4B 在内部测试集上的三项评分达到 3.7–3.9，与人类报告的 4.3–4.4 差距在 0.5–0.6 分之间。**在约 60% 的案件中，医生认为模型生成结果等于或优于人工报告**。在外部 AutoPET 数据集上，模型同样表现稳健，三项评分在 3.8–4.0 之间，证明了跨数据集的泛化能力。

---

### 消融实验

**Table 3** 系统性地揭示了各组件对性能的贡献：

**1. 掩码输入（Mask）**：在仅 PET 的基线（Row 1）上添加 mask 输入（Row 2），GREEN 分数从 0.060 提升至 0.077（+0.017），RaTEScore 同步提升，验证了掩码条件化对病灶定位和事实准确性的直接增益。

**2. CT 模态（CT）**：在 PET+Mask 基础上加入 CT 联合编码（Row 3），BERTScore 和 GREEN 进一步提高，说明 CT 提供的解剖结构信息增强了解剖一致性和语义理解。

**3. 聚焦提示（Focal Prompt）**：这是**增益最显著的组件**。在 PET+Mask+CT 基础上引入聚焦提示（Row 4 vs Row 3），CIDEr 从 0.134 跃升至 0.397（+0.263），GREEN 从 0.060 升至 0.226（+0.166），所有指标全面提升。这直接证明了高分辨率聚焦裁剪对于捕获体积占比小于 0.1% 的微小病灶细节至关重要，有效解决了全局编码导致的细粒度信息丢失问题。

**4. TotalSegmentator 预训练（TS）**：在完整模型基础上加入 TS 预训练（Row 5 vs Row 4），所有指标获得小幅但一致的提升，最终 GREEN 达到 0.257。

消融实验的因果链条清晰：**Mask 提供空间定位 → CT 提供解剖上下文 → Focal Prompt 保留病灶细节 → TS 预训练提供解剖先验**，四者协同实现了从掩码空间到语言描述的精确映射。

---

### 失败模式与局限性

1. **定量测量幻觉**：模型会幻觉生成 SUVmax 和病灶尺寸的具体数值。尽管这些值可以从输入 mask 直接计算，当前仍需人工替换为 `[#]` 占位符。实际部署前需要集成从 mask 直接测量的后处理步骤。

2. **报告完整性不足**：当前仅处理病灶级发现描述，尚不支持完整的、模板化的 PET 报告生成（如包含临床指征、比较研究、整体印象等结构化字段）。

3. **数据多样性限制**：数据集来自单一中心，且主要包含 FDG 示踪剂，对稀有示踪剂（如 DOTATATE）的泛化能力需更多验证。人工评估样本量有限（116 例内部 + 32 例外部），医生评分带有主观性。

4. **多病灶场景的鲁棒性**：当存在多个解剖邻近的病灶时，聚焦提示与全局描述的融合策略是否足够稳健，尚缺乏系统性验证。

5. **评估指标鸿沟**：自动评估指标与临床专家偏好之间的偏差（GREEN 相关系数仅 0.592，BLEU 仅 0.214）表明，当前的自动评估范式尚不能可靠替代人工评估，需要探索新的临床对齐评估方法。

![[assets/figures/papers/paper_list_l2333_https_arxiv_org_abs_2510_27680/figures/005_Table_2.jpg]]
*Table 2: Comparison of selected models on the PETARSeg-11k test set. The ”(finetuned)” indicates the model was trained on PETARSeg-11k*

![[assets/figures/papers/paper_list_l2333_https_arxiv_org_abs_2510_27680/figures/008_Figure_4.jpg]]
*Figure 4: A comparison between different models. PETAR consistently produces anatomically correct descriptions. Prior to fine-tuning, both MedGemma and M3D-RAD produce highly inaccurate results. After fine-tuning, the models still tend to make localisation errors. Anatomical descriptors are underlined for ease of comparison (red=incorrect, green=correct). Note: quantitative measurements (lesion size, SUVmax) are hallucinated by the models but can be easily replaced with directly measured values using the input lesion masks*

![[assets/figures/papers/paper_list_l2333_https_arxiv_org_abs_2510_27680/figures/003_Table_1.jpg]]
*Table 1: Comparison of publicly available PET/CT datasets*

## 定位与知识库关联

### 1. 与现有工作的关系

PETAR-4B 处于**3D医学视觉-语言模型**与**掩码感知多模态学习**的交叉点，其设计直接回应了现有方法在PET/CT报告生成中的两个核心缺陷：细粒度空间信息丢失和视觉-语言对齐不足。

**相对于2D VLM。** 当前医学VLM的主流范式仍以2D切片为基础，包括通用模型 **InternVL3-8B**、**Qwen3-VL-8B** 和医学专用模型 **MedGemma-4B**（Sellergren et al., 2025）、**HuatuoGPT-Vision-7B**、**QoQ-Med**。这些模型在评估时仅输入矢状、冠状、轴向三个代表性切片，缺乏对体积上下文的完整感知。PETAR-4B以完整3D体积为输入，在BLEU-4上较最强的微调后2D模型MedGemma-4B提升0.040（0.535 vs 0.495），在GREEN分数上更是以0.257远超后者的0.052，表明2D范式在需要精确解剖定位的任务中存在根本性信息瓶颈。

**相对于3D VLM。** 现有3D医学VLM如 **M3D**、**Med3DVLM** 和 **M3D-RAD** 虽然支持体积输入，但普遍采用全局编码与下采样策略。问题在于，PET病灶的平均体积占比小于0.1%，全局下采样不可避免地抹除这些微小区域的判别性特征。PETAR-4B与这些方法的关键分岔在于引入了**掩码条件化的视觉编码**——将二值病灶mask与PET特征在嵌入层相加（Eq. 8: $\mathbf{X}_{\mathrm{PET}} = \mathcal{T}(Z_P + Z_M)$），迫使Transformer在编码阶段即关注病灶区域。这一设计带来的增益直接体现在GREEN分数的跃升上：PETAR-4B的0.257 vs M3D-RAD（微调后）的0.071，差距达0.186。

**相对于掩码感知VLM。** 在掩码感知这一维度上，**ViP-LLaVA** 探索了2D掩码与VLM的结合，**Reg2RG** 则尝试了器官级3D掩码用于报告生成。PETAR-4B将掩码感知推进到**病灶级3D粒度**，并通过聚焦提示（focal prompt）机制进一步放大了掩码的信息价值。消融实验显示，仅添加mask即可在GREEN上带来+0.017的提升（Table 3），而聚焦提示的叠加使CIDEr从0.134跃升至0.397、GREEN从0.060升至0.226，证明高分辨率局部视图对于细粒度属性描述（如代谢活性、边界特征）不可或缺。

### 2. 适用边界

PETAR-4B的设计围绕以下前提展开，偏离这些条件时性能可能显著下降：

- **输入模态要求**：模型假设同时可用PET、CT和病灶分割掩码。当CT缺失时，语义一致性指标（BERTScore）下降；当掩码缺失时，定位准确性受损。实际部署中，掩码可通过自动分割工具获取，但分割质量直接影响下游生成。
- **病灶级描述范围**：当前模型仅生成单个病灶的发现描述，不支持完整的结构化PET报告（如包含临床指征、比较性评估、整体印象等模板化章节）。从离散病灶描述到完整报告的转换是尚未解决的工程问题。
- **示踪剂泛化**：训练数据主要来自FDG示踪剂检查，对稀有示踪剂（如DOTATATE、PSMA）的代谢模式和病灶表现可能缺乏充分覆盖。跨数据集实验仅在AutoPET（同为FDG）上验证，更广泛的示踪剂泛化能力需额外验证。
- **单中心数据偏差**：PETARSeg-11k数据集来自单一中心，模型可能习得该中心的报告风格和人群特征偏差，在多中心部署前需进行域适应评估。

### 3. 局限与开放问题

**已识别的局限：**

1. **定量测量幻觉**：模型生成的SUVmax、病灶尺寸等数值存在幻觉，尽管这些值可直接从输入mask计算。当前在人工评估中需将这些数值替换为占位符[#]，实际部署前需集成从mask直接测量的后处理模块。
2. **评估样本量有限**：人工评估仅覆盖116例内部测试和32例外部样本，且五位核医学医师的评分带有固有主观性。更大规模的读者研究和多中心验证是建立临床可信度的必要步骤。
3. **自动评估指标与临床判断的鸿沟**：Table 4显示，GREEN与专家评分的Spearman相关系数最高（0.592），而BLEU仅0.214。这一鸿沟意味着仅依赖n-gram指标的消融结论需要谨慎解读，部分看似显著的自动指标提升可能并未转化为临床感知的改进。

**开放问题：**

1. **多病灶场景的聚焦策略**：当存在多个解剖邻近的病灶时，当前随机扰动单一病灶中心的聚焦提示策略可能导致病灶间信息混淆。是否需要多焦点融合或注意力路由机制来同时处理多个病灶，是值得探索的方向。
2. **端到端自动化管道**：能否利用先进的通用病灶分割算法（如nnUNet、PET分割工具）替代人工标注的掩码输入，构建从原始DICOM图像到完整报告的全自动管道？这需要解决分割错误传播到生成质量的问题。
3. **评估范式的革新**：自动指标与专家偏好的系统性偏差提示，需要开发新的评估范式——可能包括基于临床决策影响的间接评估、或利用LLM作为判断器的语义级比较——来弥合这一鸿沟。
4. **从发现到报告的跃迁**：如何将多个离散的病灶描述高效组织为符合临床规范的完整PET报告，涉及自然语言生成中的篇章规划、模板填充与一致性维护等开放问题。

## 原文 PDF

![[paperPDFs/CVPR_2026/PETAR_Localized_Findings_Generation_with_Mask_Aware_Vision_Language_Modeling_for_PET_Automated_Reporting.pdf]]
