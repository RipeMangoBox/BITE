---
title: "UNI-OOD: Unified Object- and Image-level Out-of-Distribution Detection via Cross-Context Attentive Vision-Language Modeling"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/UNI_OOD_Unified_Object_and_Image_level_Out_of_Distribution_Detection_via_Cross_Context_Attentive_Vision_Language_Modeling.pdf
project_link: null
code_link: null
aliases:
- UO
- UNI-OOD
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: 通过引入两对对称的CLIP编码器，对目标对象和背景分别建模，并利用五种跨上下文注意力机制（图像内注意力、图像间注意力、文本间注意力、图文对齐），联合捕获细粒度视觉语义与上下文线索，在无需预知任务类型的情况下统一对象级和图像级OOD检测。
primary_logic: "融合目标对象的局部patch特征与全局[CLS]特征，并通过文本-视觉对齐强化语义一致性；同时通过图像间注意力从背景中识别与目标相关的虚假关联线索，利用文本间注意力聚合多对象文本嵌入以构建全局背景语义，从而实现对不同粒度OOD检测的统一推理。"
claims:
- UNI-OOD在对象级和图像级OOD检测上均全面超越现有方法，建立新的SOTA。
- 消融实验证实，移除任一跨上下文模块（如intra-image attention, inter-image attention, inter-text attention）均导致性能显著下降。
- 通过视觉-文本对齐和注意力聚合，模型能够捕获细粒度对象细节并利用背景中的有用上下文，而简单的平均或拼接操作无效。
- "Object-level OOD: BDD-100k (ID) vs OpenImages (OOD) 上 AUROC / FPR95 = 98.52 / 3.68"
---

# UNI-OOD: Unified Object- and Image-level Out-of-Distribution Detection via Cross-Context Attentive Vision-Language Modeling

> [!tip] 核心洞察
> 融合目标对象的局部patch特征与全局[CLS]特征，并通过文本-视觉对齐强化语义一致性；同时通过图像间注意力从背景中识别与目标相关的虚假关联线索，利用文本间注意力聚合多对象文本嵌入以构建全局背景语义，从而实现对不同粒度OOD检测的统一推理。

| 字段 | 内容 |
|------|------|
| 中文题名 | UNI-OOD：通过跨上下文注意力视觉-语言建模的统一对象与图像级分布外检测 |
| 英文题名 | UNI-OOD: Unified Object- and Image-level Out-of-Distribution Detection via Cross-Context Attentive Vision-Language Modeling |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://openaccess.thecvf.com/content/CVPR2026/html/Li_UNI-OOD_Unified_Object-_and_Image-level_Out-of-Distribution_Detection_via_Cross-Context_Attentive_CVPR_2026_paper.html) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/image_and_video_generation |
| Method | UNI-OOD |
| Dataset | Object-level OOD: BDD-100k (ID) vs OpenImages (OOD), Image-level OOD: ImageNet-1k (ID) vs iNaturalist (OOD), Image-level OOD average |

> [!tip] 效果简介
> - Object-level OOD: BDD-100k (ID) vs OpenImages (OOD) 上，AUROC / FPR95 98.52 / 3.68 vs RUNA (previous best) ~97.14 / 4.59 (+1.38 AUROC / -0.91 FPR95)。
> - Image-level OOD: ImageNet-1k (ID) vs iNaturalist (OOD) 上，AUROC / FPR95 99.16 / 4.92 vs NegPrompt (previous SOTA) ~98.74 / 6.24 (+0.42 AUROC / -1.32 FPR95)。
> - Image-level OOD average (4 datasets: iNaturalist, SUN, TEXTURE, PLACES) 上，AUROC 96.83 ± 0.15 vs LoCoOp ~95.5 (approx) (consistently higher than all baselines)。

## 概述

分布外（OOD）检测是保障视觉系统在开放世界中安全部署的关键技术。现有方法长期将对象级与图像级OOD检测视为两个独立任务，且普遍假设每张图像仅包含单一对象，忽略了真实场景中多对象共存且每个对象需独立进行OOD评估的现实需求。对象级方法（如 **RUNA**，Zhang et al., AAAI 2025）依赖粗粒度的全局[CLS]表示，缺乏对目标对象与背景之间上下文依赖关系的精细建模，导致性能受限。

针对上述瓶颈，本文提出 **UNI-OOD**——一个基于跨上下文注意力视觉-语言建模的统一框架。其核心思想是：通过引入两对对称的CLIP编码器，分别对目标对象和背景进行独立建模，并利用五种跨上下文注意力机制（图像内注意力、图像间注意力、文本间注意力、以及两对图文对齐），联合捕获细粒度视觉语义与上下文线索。该设计使得模型在推理时无需预知任务类型，即可统一完成对象级和图像级OOD检测。

实验结果表明，UNI-OOD在对象级和图像级OOD检测基准上均全面超越现有方法，建立了新的SOTA。具体而言，在BDD-100k（ID）vs OpenImages（OOD）的对象级评测中，AUROC达到98.52%（FPR95为3.68%），较前SOTA方法RUNA提升1.38个百分点；在ImageNet-1k（ID）vs iNaturalist（OOD）的图像级评测中，AUROC达到99.16%（FPR95为4.92%），较前SOTA方法NegPrompt提升0.42个百分点。消融实验进一步证实，任一跨上下文注意力模块的移除均会导致性能显著下降，验证了各模块的必要性。

## 背景与动机

分布外（Out-of-Distribution, OOD）检测是视觉系统安全部署的关键保障，旨在识别与训练分布不匹配的样本，防止模型在未知输入上产生不可靠的预测。现有OOD检测研究主要沿两条独立路径展开：**图像级OOD检测**将整幅图像作为整体判断其是否属于已知分布，而**对象级OOD检测**则需对图像中每个候选对象逐一评估，判断其是否为分布内（ID）类别。

### 现有方法的根本性缺口

当前OOD检测方法存在一个被长期忽视的结构性假设：**每张图像仅包含单一对象**。然而，真实场景中多对象共存是常态——一幅街景图像可能同时包含车辆、行人、交通标志等多个需要独立进行OOD评估的对象。这一假设与现实的脱节导致了两个层面的性能瓶颈：

1. **对象级方法的上下文盲区**：以RUNA（Zhang et al., AAAI 2025）为代表的前SOTA方法，虽然利用CLIP的双编码器架构进行对象级OOD检测，但其仅依赖目标对象的全局[CLS]嵌入，缺乏对目标对象内部细粒度视觉细节的捕捉能力。更关键的是，这些方法对背景采取整体高斯模糊处理，无选择性地丢弃了背景中可能与目标对象存在语义关联的上下文线索，导致对虚假相关性的建模能力严重不足。

2. **任务分离的推理割裂**：对象级和图像级OOD检测长期被作为两个独立任务处理，现有方法在推理时需预先知晓任务类型，无法在统一框架下对任意图像同时输出两种粒度的OOD判断。这种分离不仅增加了系统部署的复杂度，更忽视了两种粒度之间天然的互补关系——背景中的多对象语义恰恰是连接对象级与图像级推理的桥梁。

### 核心动机与解决思路

本文的核心动机源于一个关键观察：**目标对象与其背景之间存在可被建模的跨上下文依赖关系**，而这一关系正是统一两种粒度OOD检测的突破口。具体而言：

- **目标对象内部**：patch级特征与全局[CLS]特征之间存在细粒度的视觉相关性，通过注意力机制可以捕获对象内部的语义结构；
- **目标-背景之间**：背景中的其他对象可能提供与目标相关的上下文线索（如“马路”背景对“汽车”目标的支撑），但也可能引入虚假关联（如“天空”背景对“汽车”目标的弱相关），需要选择性建模；
- **背景文本语义**：背景中多个对象的文本标签可以通过注意力聚合形成整体的背景语义表示，而非简单的平均或拼接（实验证明此类朴素策略无效）。

基于上述动机，UNI-OOD提出通过**两对对称的CLIP编码器**和**五种跨上下文注意力机制**，在无需预知任务类型的前提下，统一实现对象级和图像级OOD检测。该方法的核心洞察在于：融合目标对象的局部patch特征与全局语义，同时通过图像间注意力从背景中识别相关线索、利用文本间注意力聚合多对象语义，从而建立跨粒度的统一推理范式。

## 核心创新

UNI-OOD 的核心创新在于首次将对象级与图像级 OOD 检测统一到同一框架下，并通过**跨上下文注意力机制**解决现有方法在真实多对象场景中的根本缺陷。其关键创新可归纳为以下三个维度的 **changed slots**：

### 1. 从全局表示到细粒度对象建模：Intra-Image Attention + Text-Vision Alignment

**baseline 缺陷**：现有对象级方法（如 **RUNA**，Zhang et al., AAAI 2025）仅使用 ViT 的 `[CLS]` 全局嵌入作为目标对象的视觉表征，丢弃了 patch 级空间细节，导致对细粒度视觉语义的捕捉不足。

**UNI-OOD 方案**：在 Image Encoder 1 中引入 **intra-image attention**，显式计算 `[CLS]` token 对所有 patch token 的注意力系数（Eq 1），并跨所有层和注意力头平均得到视觉相关性权重 $\beta_{i,x}^{\text{img}}$（Eq 2）。随后，通过 **text-vision alignment** 计算每个 patch/CLS 嵌入与目标文本嵌入的余弦相似度 $\mu_{i,x}$（Eq 3），对视觉权重进行语义重标定。最终，将加权后的 `[CLS]` 嵌入与经 CNN 空间聚合的加权 patch 嵌入通过 MLP 融合（Eq 4），形成**兼具全局语义与局部细节**的目标对象视觉表示。

这一设计将对象表征从粗粒度的单一向量提升为**语义对齐的细粒度多尺度特征融合**，消融实验证实移除 intra-image attention 导致对象级 AUROC 从 98.52 骤降至 95.72（Table 3）。

### 2. 从背景模糊到上下文关系挖掘：Inter-Image Attention + Inter-Text Attention

**baseline 缺陷**：现有方法（如 RUNA）对背景采用整体高斯模糊处理，无选择性地丢弃所有背景信息，忽略了背景中可能与目标对象存在**虚假关联**的上下文线索（如道路场景中的天空、建筑等协变量）。

**UNI-OOD 方案**：引入对称的第二对 CLIP 编码器专门建模背景，并通过两种跨上下文注意力机制实现目标-背景的联合推理：

- **Inter-image attention**（Eq 5-6）：计算目标对象的 `[CLS]`（来自 Image Encoder 1）对背景图像各 token（来自 Image Encoder 2）的注意力权重，从背景中自动识别与目标相关的视觉线索。
- **Inter-text attention**（Eq 7-9）：当背景包含多个对象时，计算目标对象的 `[EOT]` token 对背景中各对象 `[EOT]` token 的注意力，以此作为权重加权聚合多个对象的文本嵌入，构建**整体背景语义** $\tilde{M}_{\text{text}}(t_{(x)})$。论文明确指出简单的平均或拼接策略无效（Section 3.3.2）。

消融实验强烈支持这一设计：移除 inter-image attention 使对象级 AUROC 从 98.52 降至 96.02，FPR95 从 3.68 升至 6.21（Table 3）；在图像级 OOD 检测中同样造成显著退化（Table 4）。

### 3. 从任务分离到统一推理：无需任务标签的联合框架

**baseline 缺陷**：对象级和图像级 OOD 检测通常由不同方法分别处理，推理时需预知任务类型。

**UNI-OOD 方案**：通过两对 CLIP 编码器与五种跨上下文注意力机制的协同设计，UNI-OOD 在训练时同时学习对象级和图像级的 OOD 检测能力，推理时**无需任务标签**即可对任意输入图像同时输出两种粒度的 OOD 判定。这一统一性源于框架对“目标对象-背景”关系的通用建模：对象级检测利用背景中多对象的文本聚合（inter-text attention），图像级检测则将整图视为单一目标、背景信息通过开关机制 $[\cdot]^{\text{obj}}$ 选择性激活（Eq 11）。

综上，UNI-OOD 通过 **intra-image attention + text-vision alignment** 实现细粒度对象语义捕获，通过 **inter-image attention + inter-text attention** 实现目标-背景上下文关系建模，最终在统一框架下建立了对象级与图像级 OOD 检测的新 SOTA（Figure 1, Table 1-2）。

## 整体框架

UNI-OOD 采用两对结构相同、参数冻结的 CLIP 图像与文本编码器，分别对**目标对象**和**背景**进行独立建模，并通过五种跨上下文注意力机制实现两者的联合推理。框架在训练时同时接收对象级和图像级样本，推理时无需预知任务类型，即可对任意输入图像输出统一的对象级与图像级 OOD 检测结果。

### 双编码器架构与数据流

如图 Figure 2 所示，整个 pipeline 的输入由三部分构成：目标对象的裁剪图像区域 $I_x$、原始完整图像 $I_{(x)}$（作为背景）、以及目标对象的类别文本标签 $t_x$。对于对象级检测，背景中还存在多个其他对象的文本标签集合 $\mathcal{X}_{(x)}^I$；对于图像级检测，背景文本部分则被关闭。

![[assets/figures/papers/paper_list_l2227_https_openaccess_thecvf_com_content_CVPR2026_html_Li_UNI_OOD_Unified_Obj/figures/002_Figure_2.jpg]]
*Figure 2: Overview of the proposed unified object- and image-level OOD detection framework. The model employs two identical CLIP encoder pairs, one for the target object and the other for its background, to jointly learn cross-context relationships. Five key modules enable this integration: (i) intra-image attention within Image Encoder 1 for fine-grained object semantics, (ii) text–vision alignment between Image Encoder 1 and Text Encoder 1 for object-level semantics, (iii) inter-image attention between Image Encoders 1 and 2 for contextual cues, (iv) inter-text attention between Text Encoders 1 and 2 for holistic background semantics, and (v) text–vision alignment between Image Encoder 2 and Text E...*

**Image Encoder 1（目标对象分支）** 接收 $I_x$，输出最后一层的 `[CLS]` 嵌入 $\mathbf{z}_{0,x}^{\text{img},L}$ 和 $N$ 个 patch 嵌入 $\{\mathbf{z}_{i,x}^{\text{img},L}\}_{i=1}^N$。**Text Encoder 1** 同步编码目标对象的文本提示 $t_x$，得到文本嵌入 $M_{\text{text}}(t_x)$。

**Image Encoder 2（背景分支）** 接收 $I_{(x)}$，同样输出 `[CLS]` 和 patch 嵌入。**Text Encoder 2** 仅在对象级检测时激活，编码背景中所有其他对象的文本标签 $\{t_{x'}\}_{x' \in \mathcal{X}_{(x)}^I}$，得到各自的文本嵌入。

### 五种跨上下文注意力机制

框架的核心在于五类交叉注意力模块，它们将目标与背景的视觉、文本表示深度耦合：

1. **Intra-Image Attention（图像内注意力）**：在 Image Encoder 1 内部，计算 `[CLS]` token 对每个 patch token 的注意力系数 $\alpha_{i,0,\text{intra}}^{\text{img},l,h}$（见 Eq (1)），并在所有层和头上平均得到最终的视觉相关性权重 $\beta_{i,x}^{\text{img}}$（Eq (2)）。该机制捕获目标对象整体语义与局部细粒度细节之间的内在关联。

2. **Text-Vision Alignment (Object)（目标文本-视觉对齐）**：将 Image Encoder 1 输出的每个 patch/`[CLS]` 嵌入与 Text Encoder 1 的目标文本嵌入做余弦相似度计算，取非负值作为对齐权重 $\mu_{i,x}$（Eq (3)）。该模块强化视觉特征与类别语义的一致性。

3. **Inter-Image Attention（图像间注意力）**：跨编码器计算目标对象的 `[CLS]`（来自 Image Encoder 1）对背景图像每个 token（来自 Image Encoder 2）的注意力 $\alpha_{i,0,\text{inter}}^{\text{img},l,h}$（Eq (5)），经平均后得到背景视觉相关性权重 $\beta_{i,(x)}^{\text{img}}$（Eq (6)）。其作用是识别背景中与目标对象相关的虚假关联线索。

4. **Inter-Text Attention（文本间注意力）**：在对象级检测中，计算 Text Encoder 1 中目标对象的 `[EOT]` token 对 Text Encoder 2 中每个背景对象 `[EOT]` token 的注意力 $\alpha_{x',x,\text{inter}}^{\text{text},l,h}$（Eq (7)），平均后得到聚合权重 $w_{x',x}^{\text{text}}$（Eq (8)），用于加权求和所有背景对象的文本嵌入，构建一个整体的背景文本表示 $\tilde{M}_{\text{text}}(t_{(x)})$（Eq (9)）。

5. **Text-Vision Alignment (Background)（背景文本-视觉对齐）**：将 Image Encoder 2 的 patch 嵌入与上述整体背景文本嵌入做余弦相似度计算，得到背景对齐权重 $\mu_{i,(x)}$（Eq (10)），为背景视觉特征注入语义指导。

### 特征融合与最终表示

在目标对象分支，加权后的 `[CLS]` 嵌入 $\mu_{0,x}\beta_{0,x}^{\text{img}}\mathbf{z}_{0,x}^{\text{img},L}$ 与经 CNN 空间聚合后的加权 patch 嵌入一并送入 MLP，生成目标对象的最终视觉嵌入 $\mathbf{z}_x^{\text{img}}$（Eq (4)）。

在背景分支，采用对称的 Combiner 结构（CNN + MLP），将加权 `[CLS]` 与加权 patch 嵌入融合为背景视觉嵌入 $\mathbf{z}_{(x)}^{\text{img}}$（Eq (11)）。其中，对象级与图像级检测通过开关 $[\cdot]^{\text{obj}}$ 控制背景文本-视觉对齐权重的启用与否。

最终，将目标与背景的视觉嵌入相加，并通过投影矩阵 $P$ 映射到联合视觉-语言空间，得到整幅图像的表示 $M_{\text{img}}(I_x, I_{(x)})$（Eq (12)）。

### OOD 判定

对于任意输入，计算图像表示与目标类别文本嵌入 $M_{\text{text}}(t_x)$ 的余弦相似度 $\Omega(I_x, t_x)$（Eq (13)）。若该分数超过预设阈值 $\delta$，则判定为分布内（ID），否则为分布外（OOD）。该统一评分机制无需区分对象级或图像级任务，实现了真正的任务无关推理。

## 核心模块与公式推导

UNI-OOD 的核心由两对对称的 CLIP 编码器（图像编码器 1/2 与文本编码器 1/2）构成，分别建模目标对象与其背景，并通过五种跨上下文注意力机制实现细粒度视觉语义与上下文线索的联合捕获（Figure 2）。以下按模块逐一展开关键公式与变量含义。

---

### 3.2.1 Intra-Image Attention：目标内部细粒度视觉相关性

图像编码器 1（ViT）接收目标对象图像 $I_x$，输出最后一层的 [CLS] 嵌入 $\mathbf{z}_{0,x}^{\mathrm{img},L}$ 与 $N$ 个 patch 嵌入 $\{\mathbf{z}_{i,x}^{\mathrm{img},L}\}_{i=1}^N$。为度量整体表征与局部空间细节之间的视觉相关性，引入 intra-image attention 机制，在第 $l$ 层第 $h$ 个注意力头中，计算 [CLS] token 对第 $i$ 个 patch token 的注意力系数：

$$\alpha_{i,0,\mathrm{intra}}^{\mathrm{img},l,h} = \mathrm{softmax}_i \left( \frac{1}{\sqrt{d_h^{\mathrm{img}}}} \left( \mathbf{k}_{i,x}^{\mathrm{img},l,h} \right)^T \mathbf{q}_{0,x}^{\mathrm{img},l,h} \right) \tag{1}$$

其中 $\mathbf{q}_{0,x}^{\mathrm{img},l,h}$ 与 $\mathbf{k}_{i,x}^{\mathrm{img},l,h}$ 分别为 [CLS] 的 query 向量和第 $i$ 个 patch 的 key 向量，$d_h^{\mathrm{img}}$ 为每个头的维度。将所有 $L$ 层、$H$ 个头的注意力系数平均，得到最终的视觉相关性权重：

$$\beta_{i,x}^{\mathrm{img}} = \frac{1}{LH} \sum_{l=1}^{L} \sum_{h=1}^{H} \alpha_{i,0,\mathrm{intra}}^{\mathrm{img},l,h} \tag{2}$$

该权重刻画了目标对象内部各空间位置对整体语义的贡献强度。

---

### 3.2.2 Text-Vision Alignment（Object）：目标语义对齐

为强化目标对象的视觉-文本语义一致性，将图像编码器 1 的输出投影到联合空间后，与文本编码器 1 编码的目标类别文本嵌入 $M_{\mathrm{text}}(t_x)$ 计算余弦相似度，并截断至非负值：

$$\mu_{i,x} = \max\left( \cos\left( P\,\mathbf{z}_{i,x}^{\mathrm{img},L},\; M_{\mathrm{text}}(t_x) \right),\; 0 \right) \tag{3}$$

其中 $P$ 为投影矩阵。$\mu_{i,x}$ 作为文本-视觉对齐权重，与 intra-image 权重 $\beta_{i,x}^{\mathrm{img}}$ 共同作用于后续的特征融合。

---

### 3.2.3 目标对象最终视觉嵌入

将加权后的 [CLS] 嵌入与 CNN 聚合的加权 patch 嵌入拼接，经 MLP 得到目标对象的最终视觉表示：

$$\mathbf{z}_{x}^{\mathrm{img}} = g_x^{\mathrm{MLP}}\Big( \mu_{0,x}\beta_{0,x}^{\mathrm{img}}\mathbf{z}_{0,x}^{\mathrm{img},L},\; g_x^{\mathrm{CNN}}\big( \{\mu_{i,x}\beta_{i,x}^{\mathrm{img}}\mathbf{z}_{i,x}^{\mathrm{img},L}\}_{i=1}^{N} \big) \Big) \tag{4}$$

其中 $g_x^{\mathrm{CNN}}$ 对加权 patch 嵌入进行空间聚合，$g_x^{\mathrm{MLP}}$ 融合全局与局部信息。消融实验证实，移除 CNN 空间聚合（仅用 MLP 融合全部加权嵌入）会导致对象级 AUROC 从 98.52 降至 97.14（Table 3），验证了该模块的必要性。

---

### 3.3.1 Inter-Image Attention：目标-背景视觉上下文建模

图像编码器 2 提取背景图像 $I_{(x)}$ 的特征。为识别背景中与目标对象相关的虚假关联线索，引入 inter-image attention：以图像编码器 1 中目标的 [CLS] 作为 query，对图像编码器 2 中背景的每个 token 计算注意力：

$$\alpha_{i,0,\mathrm{inter}}^{\mathrm{img},l,h} = \mathrm{softmax}_i \left( \frac{1}{\sqrt{d_h^{\mathrm{img}}}} \left( \mathbf{k}_{i,(x)}^{\mathrm{img},l,h} \right)^T \mathbf{q}_{0,x}^{\mathrm{img},l,h} \right) \tag{5}$$

平均所有层和头后得到背景视觉相关性权重：

$$\beta_{i,(x)}^{\mathrm{img}} = \frac{1}{LH} \sum_{l=1}^{L} \sum_{h=1}^{H} \alpha_{i,0,\mathrm{inter}}^{\mathrm{img},l,h} \tag{6}$$

该权重使模型能够选择性关注背景中与目标语义相关的区域，而非对背景整体进行无差别模糊处理（如 RUNA 的高斯模糊策略）。

---

### 3.3.2 Inter-Text Attention：背景多对象文本语义聚合

背景中通常包含多个对象，简单平均或拼接其文本嵌入被实验证明无效（Section 3.3.2）。UNI-OOD 引入 inter-text attention，以文本编码器 1 中目标对象的 [EOT] token 为 query，对文本编码器 2 中各背景对象的 [EOT] token 计算注意力：

$$\alpha_{x',x,\mathrm{inter}}^{\mathrm{text},l,h} = \mathrm{softmax}_{x'} \left( \frac{1}{\sqrt{d_h^{\mathrm{text}}}} \left( \mathbf{k}_{x'}^{\mathrm{text},l,h} \right)^T \mathbf{q}_{x}^{\mathrm{text},l,h} \right) \tag{7}$$

其中 $x' \in \mathcal{X}_{(x)}^I$ 为背景对象集合中的元素。平均所有 $\tilde{L}$ 层、$\tilde{H}$ 头后得到聚合权重：

$$w_{x',x}^{\mathrm{text}} = \frac{1}{\tilde{L}\tilde{H}} \sum_{l=1}^{\tilde{L}} \sum_{h=1}^{\tilde{H}} \alpha_{x',x,\mathrm{inter}}^{\mathrm{text},l,h} \tag{8}$$

以该权重加权求和所有背景对象的文本嵌入，构建单一整体背景文本嵌入：

$$\tilde{M}_{\mathrm{text}}(t_{(x)}) = \sum_{x' \in \mathcal{X}_{(x)}^I} w_{x',x}^{\mathrm{text}} \cdot M_{\mathrm{text}}(t_{x'}) \tag{9}$$

该机制保留了背景对象间的语义关系，避免了朴素聚合策略的信息损失。

---

### 3.3.2 Text-Vision Alignment（Background）：背景语义对齐

与目标侧对齐类似，背景图像各 patch 嵌入与整体背景文本嵌入 $\tilde{M}_{\mathrm{text}}(t_{(x)})$ 计算余弦相似度：

$$\mu_{i,(x)} = \max\left( \cos\left( P\,\mathbf{z}_{i,(x)}^{\mathrm{img},L},\; \tilde{M}_{\mathrm{text}}(t_{(x)}) \right),\; 0 \right) \tag{10}$$

该对齐权重确保背景视觉特征与聚合后的文本语义保持一致性。

---

### 3.3.3 背景最终视觉嵌入

背景视觉嵌入的构建与目标侧对称，融合加权 [CLS] 与 CNN 聚合的加权 patch 嵌入，并通过开关 $[\cdot]^{\mathrm{obj}}$ 区分对象级与图像级训练模式：

$$\mathbf{z}_{(x)}^{\mathrm{img}} = g_{(x)}^{\mathrm{MLP}}\Big( [\mu_{0,(x)}]^{\mathrm{obj}} \beta_{0,(x)}^{\mathrm{img}} \mathbf{z}_{0,(x)}^{\mathrm{img},L},\; g_{(x)}^{\mathrm{CNN}}\big( \{[\mu_{i,(x)}]^{\mathrm{obj}} \beta_{i,(x)}^{\mathrm{img}} \mathbf{z}_{i,(x)}^{\mathrm{img},L}\}_{i=1}^{N} \big) \Big) \tag{11}$$

---

### 3.4 最终图像表示与 OOD 判定

将目标对象与背景的视觉嵌入相加并投影到联合视觉-语言空间，得到最终图像表示：

$$M_{\mathrm{img}}(I_x, I_{(x)}) = P \cdot (\mathbf{z}_{x}^{\mathrm{img}} + \mathbf{z}_{(x)}^{\mathrm{img}}) \tag{12}$$

OOD 判定基于该表示与目标类别文本嵌入的余弦相似度：

$$\Omega(I_x, t_x) = \cos\big( M_{\mathrm{img}}(I_x, I_{(x)}),\; M_{\mathrm{text}}(t_x) \big) \tag{13}$$

若 $\Omega(I_x, t_x) \geq \delta$（阈值），则判定为 ID；否则为 OOD（Section 3.5, Eq (15)）。该统一评分函数在推理时无需任务类型标签，可同时对任意图像进行对象级与图像级 OOD 检测。

## 实验与分析

### 核心性能：统一SOTA的建立

UNI-OOD在对象级与图像级OOD检测两个维度上均以显著优势超越现有方法，确立了新的SOTA。Figure 1直观展示了这一跨任务统一优势：在4个对象级案例与4个图像级案例上，UNI-OOD的AUROC全面领先于所有竞比方法。

在对象级OOD检测任务（BDD-100k为ID，OpenImages为OOD）中，UNI-OOD取得了**98.52 AUROC / 3.68 FPR95**的成绩，相较于此前最优的VLM方法**RUNA**（Zhang et al., AAAI 2025）的约97.14 AUROC / 4.59 FPR95，AUROC提升+1.38，FPR95降低0.91（Table 1）。这一增益源于UNI-OOD对目标对象与背景之间上下文依赖关系的精细建模——RUNA仅依赖粗粒度的全局[CLS]嵌入，而UNI-OOD通过intra-image attention融合了patch级细粒度信息，并利用inter-image attention从背景中识别与目标相关的虚假关联线索。

![[assets/figures/papers/paper_list_l2227_https_openaccess_thecvf_com_content_CVPR2026_html_Li_UNI_OOD_Unified_Obj/figures/003_Table_1.jpg]]
*Table 1: Object-level OOD detection results in AUROC (↑) and FPR95 (↓) scores. Traditional methods use the full ID dataset for training, whereas VLM-based methods use 10-shot fine-tuning. Bold and underlined numbers represent best and second-best results, respectively*

![[assets/figures/papers/paper_list_l2227_https_openaccess_thecvf_com_content_CVPR2026_html_Li_UNI_OOD_Unified_Obj/figures/004_Table_2.jpg]]
*Table 2: Image-level OOD detection results with ImageNet-1k as ID dataset in AUROC (↑) and FPR95 (↓) scores. All VLM-based methods use 16-shot fine-tuning. Other conventions are the same as in Table 1*

在图像级OOD检测任务（ImageNet-1k为ID，四个OOD数据集：iNaturalist、SUN、TEXTURE、PLACES）中，UNI-OOD同样表现出一致的优势。以iNaturalist为OOD时，UNI-OOD取得**99.16 AUROC / 4.92 FPR95**，相较此前SOTA方法**NegPrompt**（Li et al., CVPR 2024）的约98.74 AUROC / 6.24 FPR95，AUROC提升+0.42，FPR95降低1.32（Table 2）。在四个OOD数据集上的平均AUROC达**96.83 ± 0.15**，稳定高于**LoCoOp**（Miyai et al., NeurIPS 2023）等基线方法。值得注意的是，图像级OOD检测中同样受益于inter-image attention机制——即使在全图级别的判断中，目标与背景的跨上下文关系仍能提供有效的区分性线索。

### 消融实验：跨上下文注意力机制的因果验证

消融实验系统性地验证了五种跨上下文注意力机制对性能的因果贡献。Table 3（对象级，10-shot）与Table 4（图像级，16-shot）分别展示了逐一移除核心模块后的性能退化。

![[assets/figures/papers/paper_list_l2227_https_openaccess_thecvf_com_content_CVPR2026_html_Li_UNI_OOD_Unified_Obj/figures/005_Table_4.jpg]]
*Table 4: Results of ablation study on image-level OOD detection with ImageNet-1k as ID dataset (16-shot, shown as AUROC (↑) / FPR95 (↓)). Other conventions are the same as in Table 3*

**移除Inter-Image Attention**（即忽略目标-背景视觉关系）导致对象级AUROC从98.52骤降至96.02，FPR95从3.68升至6.21；图像级同样出现明显退化（iNaturalist上AUROC从99.16降至97.19）。这一退化幅度在对象级任务中尤为剧烈，证实了背景上下文对目标对象OOD判定的关键作用——模型通过inter-image attention学习的不仅是背景的“存在性”，更是背景中哪些视觉元素与目标对象构成虚假关联。

**移除Intra-Image Attention**（舍弃patch级细粒度信息，退化为仅用[CLS]嵌入）导致对象级AUROC降至95.72，FPR95升至6.87。这一结果印证了核心洞察：全局[CLS]嵌入丢失了目标对象内部的细粒度视觉细节，而这些细节对于区分分布内与分布外样本至关重要。

**移除对象Text-Vision Alignment**使对象级AUROC降为96.35、FPR95升为5.26；**移除背景Text-Vision Alignment**同样造成性能下降（AUROC: 96.67, FPR95: 5.04）。两组消融共同表明，视觉-文本语义对齐在目标对象与背景两端均不可替代——仅靠视觉注意力权重不足以建立鲁棒的语义表征，文本锚点的引导是捕获精细语义差异的瓶颈环节。

**移除CNN空间聚合模块**（改用纯MLP融合加权嵌入）导致对象级AUROC降至97.14，FPR95升至4.59。这验证了CNN在聚合空间上分散的加权patch嵌入时的结构化归纳偏置优势——简单的MLP拼接无法有效保留patch间的空间拓扑关系。

### 方法谱系与知识库定位

UNI-OOD的贡献可从以下维度定位：

| 维度 | 基线方法 | 基线局限 | UNI-OOD改进 | 证据 |
|------|----------|----------|-------------|------|
| 目标对象视觉表示 | **RUNA**（Zhang et al., AAAI 2025）：仅用[CLS]全局嵌入 | 丢失patch级细粒度细节 | Intra-image attention融合[CLS]与patch嵌入，辅以text-vision alignment增强语义对齐 | Table 3消融：移除intra-image attention后AUROC降2.8 |
| 目标-背景关系建模 | **RUNA**：对背景整体高斯模糊处理 | 无选择性地丢弃背景信息 | Inter-image attention识别背景中的相关虚假线索；inter-text attention聚合多对象文本嵌入形成全局背景语义 | Table 3消融：移除inter-image attention后AUROC降2.5 |
| 背景文本表示 | 简单平均或拼接多对象标签（实验证明无效） | 丢失对象间的语义关系 | Inter-text attention加权聚合，保留语义依赖结构 | Section 3.3.2明确记载平均/拼接策略无效 |
| 任务统一性 | 对象级与图像级OOD检测分离处理，推理时需预知任务类型 | 无法应对混合场景 | 统一框架在推理时无需任务标签，可对任意图像同时输出对象级与图像级OOD判定 | Section 3.1训练与推理协议 |

在VLM-based OOD检测的知识谱系中，UNI-OOD填补了“多对象场景下细粒度上下文建模”与“对象-图像两级统一检测”之间的空白。此前的**VOS**（Du et al., ICLR 2022）与**SIREN**（Du et al., NeurIPS 2022）等传统CNN方法依赖虚拟异常合成或表征塑形，但受限于封闭的视觉表征空间；**LoCoOp**（Miyai et al., NeurIPS 2023）与**NegPrompt**（Li et al., CVPR 2024）等VLM方法虽利用了CLIP的开放语义空间，但仅处理图像级任务。UNI-OOD通过两对对称CLIP编码器与五种跨上下文注意力机制，首次实现了无需任务标签的统一推理，其跨上下文建模策略（特别是inter-image与inter-text attention的双重聚合）为后续开放词汇检测、异常检测等任务提供了可复用的设计范式。

### 公平性说明

所有对比实验遵循严格的小样本公平协议：对象级采用10-shot微调，图像级采用16-shot微调，均使用相同的CLIP ViT-B/16骨干网络。对象级评估中，所有方法使用相同的检测器（OWLv2）进行边界框提议，确保输入公平。VLM方法均基于预训练权重，未使用额外外部数据。

### 补充图表

![[assets/figures/papers/paper_list_l2227_https_openaccess_thecvf_com_content_CVPR2026_html_Li_UNI_OOD_Unified_Obj/figures/001_Figure_1.jpg]]
*Figure 1: AUROC (↑) score comparison on 4 object-level and 4 image-level OOD detection cases. “X (Y)”: X and Y are OOD and ID datasets, respectively. In both object- and image-level OOD detection, our method establishes new SOTA performance*

## 方法谱系与知识库定位

### 1. 基线关系与关键突破点

UNI-OOD 的核心突破在于将对象级和图像级 OOD 检测统一到单一框架下，而现有方法在这两个任务上长期处于分离状态。其直接竞争基线可分为两个阵营：

**对象级 OOD 检测基线**：当前 SOTA 方法 **RUNA**（Zhang et al., AAAI 2025）同样基于 CLIP 双编码器架构，但仅使用 [CLS] 全局嵌入作为目标对象表示，缺乏对 patch 级细粒度信息的利用。传统 CNN 方法如 **VOS**（Du et al., ICLR 2022）通过虚拟异常合成进行训练，**SIREN**（Du et al., NeurIPS 2022）则通过表征塑形增强 ID/OOD 区分度，但二者均无法利用视觉-语言模型的开放世界语义知识。

**图像级 OOD 检测基线**：**NegPrompt**（Li et al., CVPR 2024）通过负提示机制增强 ID/OOD 判别能力，是该任务的前 SOTA；**LoCoOp**（Miyai et al., NeurIPS 2023）则专注于少样本场景下的提示学习优化。这些方法均假设每张图像仅包含单一对象，无法处理真实场景中多对象共存的情况。

UNI-OOD 对上述基线的超越体现在三个关键维度的改进：

1. **从全局到细粒度的视觉表示**：通过 intra-image attention 融合 [CLS] 与所有 patch 嵌入，并引入 text-vision alignment 增强语义对齐，将对象表示从粗糙的全局向量提升为具有空间分辨力的细粒度表征。消融实验证实，移除 intra-image attention 导致对象级 AUROC 从 98.52 降至 95.72，FPR95 从 3.68 升至 6.87（Table 3），说明 patch 级信息对精细判别至关重要。

2. **从背景忽略到上下文主动建模**：RUNA 等先前方法对背景整体高斯模糊处理，无法选择性利用背景中的有用线索。UNI-OOD 引入 inter-image attention 识别背景中与目标相关的虚假关联线索，并通过 inter-text attention 聚合多对象文本嵌入形成整体背景语义。移除 inter-image attention 使对象级 AUROC 降至 96.02、FPR95 升至 6.21（Table 3），证实背景上下文对 OOD 检测的贡献。

3. **从任务分离到统一推理**：传统方法需在推理时预知任务类型（对象级或图像级），UNI-OOD 通过统一框架在训练时同时学习两个粒度的表示，推理时无需任务标签即可对任意图像进行两级 OOD 检测。这一设计使得模型能够共享底层语义知识，避免重复训练。

### 2. 适用边界与局限

尽管 UNI-OOD 在实验设定下表现优异，其适用性存在以下边界条件：

**模型架构依赖**：方法深度绑定 CLIP 的 ViT 架构，利用其自注意力机制提取跨层注意力系数作为视觉相关性权重。若迁移至其他视觉-语言模型（如 ALIGN、BLIP），需验证注意力提取机制的有效性。当前分析未提供在非 CLIP 骨干上的实验结果，该泛化性问题需手动验证。

**文本先验依赖**：对象级 OOD 检测需要背景中所有对象的文本标签以构建整体背景文本嵌入。在完全无标注的开放环境中（无 ID 类别文本先验），该方法如何适应尚不明确。论文未讨论零样本场景下背景文本嵌入的替代构建策略。

**背景 OOD 对象的鲁棒性**：当背景本身包含 OOD 对象时，inter-text attention 可能错误地将注意力分配给这些异常对象，从而污染背景语义表示。论文未提供相关鲁棒性分析或失败案例讨论。

**计算效率边界**：inter-text attention 需对背景中所有对象的两两关系进行建模，当背景对象数量较大时，计算复杂度呈二次增长。论文未讨论大规模类别空间下的效率优化策略。

### 3. 开放问题与延伸方向

UNI-OOD 提出的跨上下文注意力机制为 OOD 检测领域开启了若干值得探索的方向：

**跨架构泛化**：五种跨上下文注意力模块是否可解耦并嵌入到其他视觉-语言模型（如 BLIP-2、LLaVA）中？这需要验证注意力提取接口的通用性，以及不同预训练范式对注意力质量的影响。

**无文本先验场景**：在缺乏背景对象标签的情况下，是否可通过视觉聚类或开放词汇检测自动生成背景文本描述？这涉及将 inter-text attention 替换为视觉-视觉注意力或纯视觉聚合机制。

**背景 OOD 的解释性**：当背景包含异常对象时，模型是否能够通过注意力权重分布识别并抑制这些异常信号？这需要构建包含背景异常的测试基准，并分析 inter-image 和 inter-text attention 的注意力图谱。

**任务迁移潜力**：跨上下文建模策略本质上是学习目标与场景的联合表示，这一思想可迁移至其他需要上下文推理的视觉任务，如异常检测、开放词汇检测、视觉问答中的上下文理解等。论文未提供相关迁移实验，但架构设计本身具有任务无关性。

**训练效率优化**：当前方法需对每个对象-背景对进行完整的双编码器前向传播，未来可探索共享特征提取或注意力缓存策略以降低训练成本，特别是在大规模多对象数据集上的扩展性。

## 原文 PDF

![[paperPDFs/CVPR_2026/UNI_OOD_Unified_Object_and_Image_level_Out_of_Distribution_Detection_via_Cross_Context_Attentive_Vision_Language_Modeling.pdf]]
