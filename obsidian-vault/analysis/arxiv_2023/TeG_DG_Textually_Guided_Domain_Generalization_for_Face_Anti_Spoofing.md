---
title: "TeG-DG: Textually Guided Domain Generalization for Face Anti-Spoofing"
type: paper
paper_level: A
venue: arXiv
year: 2023
pdf_ref: paperPDFs/arxiv_2023/TeG_DG_Textually_Guided_Domain_Generalization_for_Face_Anti_Spoofing.pdf
aliases:
- TD
- TeG-DG
tags:
- arxiv_2023
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/vision_models_multimodal
- topic/representation_self_supervised_transfer
- topic/representation_self_supervised_transfer/transfer_multitask_and_meta_learning
core_operator: 利用文本描述作为跨域通用监督，将视觉特征与文本特征对齐，以过滤域特定噪声并学习域不变特征。
primary_logic: 文本作为一种更抽象且跨域通用的表达形式，能够捕捉不同攻击类型的共性和本质特征，从而弥合不同图像域之间的差距。
claims:
- TeG-DG在所有Leave-One-Out协议上的HTER均显著低于之前最佳方法；在极端有限源域场景下，HTER相对降低约14%，AUC提升约12%。
- 消融实验表明，移除文本对齐（TEVD）比移除三元组损失对性能损害更大，验证了文本监督的核心作用。
- few-shot/zero-shot场景下TeG-DG大幅超越CLIP基线，仅需少量样本即可达到甚至超过许多全量训练的DG方法。
- I&C&M to O (OULU-NPU as target) 上 HTER = 5.68
---

# TeG-DG: Textually Guided Domain Generalization for Face Anti-Spoofing

> [!tip] 核心洞察
> 文本作为一种更抽象且跨域通用的表达形式，能够捕捉不同攻击类型的共性和本质特征，从而弥合不同图像域之间的差距。

| 字段 | 内容 |
|------|------|
| 中文题名 | 面向人脸反欺骗的文本引导域泛化 |
| 英文题名 | TeG-DG: Textually Guided Domain Generalization for Face Anti-Spoofing |
| 会议/期刊 | arXiv 2023 |
| Links | [paper](https://arxiv.org/abs/2311.18420) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/vision_models_multimodal #topic/representation_self_supervised_transfer #topic/representation_self_supervised_transfer/transfer_multitask_and_meta_learning |
| Method | TeG-DG |
| Dataset | I&C&M to O, O&C&M to I, O&C&I to M, O&M&I to C |

> [!tip] 效果简介
> - I&C&M to O (OULU-NPU as target) 上，HTER 5.68 vs 8.86 (IADG) (-3.18)；AUC 97.92 vs 97.14 (IADG) (+0.78)。
> - O&C&M to I (Replay-Attack as target) 上，HTER 3.21 vs 3.71 (DiVT-M) (-0.50)。
> - O&C&I to M (MSU-MFSD as target) 上，HTER 1.88 vs 2.86 (DiVT-M) (-0.98)。

## 概述

人脸反欺骗（Face Anti-Spoofing, FAS）的域泛化（Domain Generalization, DG）面临一个核心瓶颈：现有方法提取的视觉特征仍残留与任务无关的风格偏差（如光照、采集设备、环境背景），导致模型在未知目标域上的泛化性能显著下降。根本原因在于，仅依靠视觉模态的域对齐或特征白化难以彻底剥离这些域特定噪声。

本文提出**TeG-DG（Textually Guided Domain Generalization）**，其核心洞察是：文本作为一种更抽象、跨域通用的表达形式，能够捕捉不同攻击类型（打印、重放、面具等）的共性本质特征，从而弥合图像域之间的分布差距。方法利用文本描述作为跨域不变监督信号，将视觉特征与文本特征对齐，以此过滤域特定噪声，学习域不变的表征。

TeG-DG框架包含三个关键模块：**Text Prompter (TP)** 利用GPT-4自动生成的提示库，为每张训练图像动态提供匹配与不匹配的文本描述；**Hierarchical Attention Fusion (HAF)** 自适应融合ViT多层的[CLS] tokens，捕获多粒度视觉线索并投影至文本特征空间；**Textual-Enhanced Visual Discriminator (TEVD)** 通过视觉-语言三元组损失和多模态分类器，将文本监督注入视觉判别器，推理阶段则丢弃文本模态，不增加部署开销。

在OULU-NPU、CASIA-MFSD、Replay-Attack、MSU-MFSD四个数据集的Leave-One-Out协议下，TeG-DG在所有目标域上均取得最优HTER和AUC，显著超越**MADDG**（Shao et al., CVPR 2019）、**SSAN-M**（Wang et al., CVPR 2022）、**IADG**（Zhou et al., arXiv 2023）和**DiVT-M**（Liao et al., WACV 2023）等基线方法。在极端有限源域场景（仅两个源域）下，HTER相对降低约14%，AUC提升约12%。消融实验进一步证实，移除文本对齐对性能的损害大于移除三元组损失，验证了文本监督的核心作用。此外，在few-shot和zero-shot设定下，TeG-DG大幅超越**CLIP**（Radford et al., ICML 2021）基线，仅需少量样本即可达到甚至超过全量训练的DG方法。

### 方法谱系与知识库定位

TeG-DG属于**文本引导的域泛化FAS方法**，与现有工作的关键区别在于：

- **vs. 对抗域泛化（如MADDG）**：TeG-DG不需要域标签，避免了对抗训练的不稳定性，且文本监督比域判别器提供更语义化的不变性约束。
- **vs. 风格装配/特征白化（如SSAN-M、IADG）**：这些方法在视觉空间内消除风格偏差，但无法完全剥离与攻击类型无关的域特定信息；TeG-DG通过跨模态对齐引入外部语言先验，从更高语义层面过滤域噪声。
- **vs. ViT基线（如DiVT-M）**：TeG-DG的HAF模块改进了标准ViT仅使用末层[CLS] token的做法，融合多层特征以保留局部纹理和全局语义。
- **vs. 视觉-语言基线（如CLIP）**：CLIP缺乏FAS任务的领域知识（如对不同攻击材质的细粒度判别），TeG-DG通过FAS特定的文本提示库和TEVD的多模态分类器弥补了这一缺陷，在zero-shot场景下性能大幅领先。

**方法适用边界**：TeG-DG在标准Leave-One-Out协议和有限源域场景下均表现优异，但训练依赖攻击类型标签以构建匹配/不匹配提示对，获取细粒度标签可能增加标注成本。提示库由GPT-4自动生成，虽减少人工偏差，但可能受限于语言模型的内部知识覆盖范围。推理阶段丢弃文本模态虽降低部署复杂度，但也意味着无法利用测试时的附加文本信息（如设备描述、场景上下文）进一步提升性能。

## 背景与动机

### 人脸反欺骗中的域泛化困境

人脸反欺骗（Face Anti-Spoofing, FAS）是保障人脸识别系统安全性的关键防线，其核心任务在于区分真实人脸与打印攻击、重放攻击、面具攻击等欺骗手段。然而，FAS系统面临一个根本性挑战：不同数据集之间存在显著的**域偏移**（domain shift），包括光照条件、采集设备、背景环境、攻击媒介等差异。这些域特定因素导致在一个数据集（源域）上训练的模型，在另一个未见过的数据集（目标域）上性能急剧下降。

为应对这一挑战，域泛化（Domain Generalization, DG）方法应运而生。典型的DG-FAS方法包括基于对抗域对齐的**MADDG**（Shao et al., CVPR 2019）、基于风格组装的**SSAN-M**（Wang et al., CVPR 2022）、无需域标签的实例白化方法**IADG**（Zhou et al., arXiv 2023），以及基于视觉Transformer的**DiVT-M**（Liao et al., WACV 2023）等。这些方法虽然在一定程度上缓解了域偏移问题，但其核心思路仍局限于**视觉特征空间内的分布对齐或风格解耦**。

### 瓶颈：视觉特征中残余的风格偏差

现有DG方法的根本瓶颈在于：**即使经过域对齐或风格归一化，提取的视觉特征仍然包含残余的风格偏差**。这些偏差可能表现为微妙的光照模式、传感器噪声特征或压缩伪影，它们在源域训练中难以被完全消除，却足以在未知目标域中误导分类决策。正如Figure 1所揭示的，传统FAS方法试图在纯视觉空间中寻找域不变特征，但视觉信号天然地与采集条件耦合，使得完全剥离域特定信息极为困难。

### 核心洞察：文本作为跨域通用的监督信号

本文提出了一个关键洞察：**文本描述作为一种更抽象且跨域通用的表达形式，能够捕捉不同攻击类型的共性和本质特征，从而弥合不同图像域之间的差距**。

具体而言，无论是来自何种光照、何种设备采集的“打印攻击”，其语义本质都是“一张被打印在纸上的照片”；“重放攻击”的本质是“通过屏幕展示的人脸”。这些语义描述不依赖于像素级的视觉风格，因此天然具有域不变性。通过将文本特征作为监督信号引入训练过程，可以引导视觉编码器学习过滤域特定噪声，聚焦于与攻击类型本质相关的判别性特征。

### 方法动机：从文本引导到域不变特征学习

基于上述洞察，本文提出**TeG-DG（Textually Guided Domain Generalization）**框架，其设计动机包括三个层面：

1. **监督信号的域不变性**：利用文本描述作为跨域通用的监督信号，将视觉特征与文本特征对齐，使模型学习到的特征不再依赖于特定域的视觉风格，而是与攻击类型的语义本质相关联。

2. **无需域标签的泛化**：传统DG方法通常需要域标签来进行对抗训练或分布对齐，而域标签的获取成本高且定义模糊。TeG-DG通过文本监督实现域泛化，完全不需要域标签，显著降低了部署门槛。

3. **多粒度特征融合**：FAS任务既需要关注局部的纹理细节（如打印网点、屏幕像素网格），也需要理解全局的语义信息（如面具的整体形态）。为此，TeG-DG设计了层次化注意力融合模块，自适应地整合ViT各层的多粒度特征。

### 实验动机：极端场景下的泛化验证

除了标准的Leave-One-Out协议，本文特别关注两种更具挑战性的实际场景：

- **极其有限的源域**：当仅有2个源域可用时（而非通常的3个），域偏移问题更加严峻，传统DG方法往往失效。
- **零样本/少样本场景**：在目标域仅有极少标注样本甚至无标注样本的情况下，验证文本监督能否赋予模型更强的泛化能力。

这些场景更贴近真实部署条件，能够充分检验文本引导泛化的实际价值。初步实验表明，TeG-DG在极其有限源域场景下，HTER相对降低约14%，AUC提升约12%，验证了文本监督在数据稀缺条件下的独特优势。

## 核心创新

TeG-DG的核心创新在于**将文本描述作为跨域通用监督信号引入人脸反欺骗（FAS）的域泛化任务**，从根本上改变了模型学习域不变特征的方式。与现有方法依赖域标签进行对抗对齐或实例白化不同，TeG-DG利用文本的抽象性和跨域稳定性来过滤图像中的域特定噪声（如光照、采集设备差异），从而弥合不同图像域之间的差距。

具体而言，该方法在三个关键维度上对传统DG-FAS范式进行了改造：

**1. 域泛化策略：从域标签对齐到文本引导对齐**

现有DG-FAS方法普遍需要域标签来驱动对抗训练（如**MADDG**，Shao et al., CVPR 2019）或风格重组（如**SSAN-M**，Wang et al., CVPR 2022），部分方法虽然无需域标签（如**IADG**，Zhou et al., arXiv 2023），但仍通过实例白化等视觉域内操作来消除域偏差。TeG-DG的核心突破在于完全摒弃域标签，转而利用文本原型作为跨域桥梁——匹配文本描述（如“这是一张真实的活体人脸”）和非匹配文本描述（如“这是一张打印攻击人脸”）在语义空间中形成稳定的分类边界，引导视觉特征向域不变方向收敛。这种文本引导对齐策略在极端有限源域场景（仅两个源域）下优势尤为显著：在M&I到C协议上，HTER从IADG的24.07%降至6.19%，相对降幅达74.3%（Table 2）。

**2. 视觉特征提取：从单层[CLS]到层级注意力融合**

传统ViT方法仅使用最后一层的[CLS] token作为图像表征，丢失了浅层纹理细节和中间层语义信息。TeG-DG设计了**层级注意力融合模块（Hierarchical Attention Fusion, HAF）**，将ViT各层的[CLS] tokens堆叠后通过自注意力机制自适应融合（Equation 1-4），最终投影到文本特征维度（Equation 5）。这一设计使得模型能够同时捕捉局部纹理线索（如打印攻击的边缘伪影）和高层语义信息（如人脸的整体真实性），为后续的跨模态对齐提供更丰富的视觉表征。消融实验表明，HAF与文本监督模块（TEVD）存在显著的协同效应——同时移除两者时性能大幅下降（Table 4）。

**3. 训练监督：从单一视觉分类到多模态联合正则化**

传统方法仅对视觉特征施加二元交叉熵损失进行监督。TeG-DG通过**文本增强视觉判别器（Textual-Enhanced Visual Discriminator, TEVD）**引入了双重文本监督机制：一是视觉-语言三元组损失$\mathcal{L}_{\mathrm{TRI}}$，确保视觉特征与匹配文本的距离小于与非匹配文本的距离至少为$\alpha$（Equation 6）；二是多模态分类器，同时对视觉特征、匹配文本特征和非匹配文本特征施加交叉熵约束（Equation 7）。文本模态在训练阶段充当正则化器，约束视觉特征的学习方向，而在推理阶段则完全移除，不增加部署复杂度。消融实验的关键发现是：移除文本对齐（TEVD）对性能的损害大于移除三元组损失，证实了文本监督是该方法的核心驱动力（Table 4）。

总体训练目标为$\mathcal{L}_{\mathrm{TeG-DG}} = \mathcal{L}_{\mathrm{CLS}} + \lambda \mathcal{L}_{\mathrm{TRI}}$（Equation 8），其中文本提示由**文本提示器（Text Prompter, TP）**从GPT-4生成的提示库中动态采样匹配和非匹配描述对（Section 3.1）。

## 整体框架

TeG-DG 的核心设计动机在于：传统域泛化方法从视觉特征中提取的表示仍残留着光照、采集设备等风格偏差，导致在未见域上的性能退化。TeG-DG 的解决方案是引入文本描述作为一种跨域通用的抽象监督信号，通过将视觉特征与文本特征对齐，过滤域特定噪声，学习域不变表示。文本之所以能弥合域间差距，在于它能够捕捉不同攻击类型（打印、重放、面具等）的共性本质，而非特定采集条件下的表面纹理。

基于这一思想，TeG-DG 构建了一个三模块协同的框架，如 Figure 2 所示。整个 pipeline 的输入输出流如下：

![[assets/figures/papers/paper_list_l1502_https_arxiv_org_abs_2311_18420/figures/002_Figure_2.jpg]]
*Figure 2: Overview of the proposed Textually Guided Domain Generalization (TeG-DG) framework. The framework contains Text Prompter (TP) for text prompt generation, the Hierarchical Attention Fusion(HAF) module for fused visual feature extraction, and the Texual-Enhanced Visual Discriminator (TEVD) for integrating text information*

1. **Text Prompter (TP)**：在训练阶段，对于每一张输入图像，TP 从一个由 GPT-4 自动生成的提示库中动态选取一条**匹配文本提示**（描述图像所属的真实攻击类型）和一条**非匹配文本提示**（描述另一种攻击类型）。这些文本提示随后由冻结的 CLIP 文本编码器编码为文本特征，作为后续跨模态对齐的监督信号。这一设计使得模型无需依赖域标签即可获得跨域通用的语义锚点。

2. **Hierarchical Attention Fusion (HAF)**：视觉输入经由 ViT 编码器处理后，HAF 模块（见 Figure 4）提取 ViT 所有层的 $[\mathrm{CLS}]$ tokens，通过自注意力机制自适应地融合多粒度特征——浅层保留局部纹理线索，深层捕获高层语义。融合后的特征经层归一化和可学习投影矩阵 $M$ 映射到与文本特征相同的维度空间，得到最终的视觉特征 $\mathcal{V}^f$。该模块以轻量级即插即用方式嵌入主流 ViT 架构。

3. **Textual-Enhanced Visual Discriminator (TEVD)**：TEVD（见 Figure 5）是文本监督发挥作用的核心机制，包含两个互补的损失函数：
   - **Vision-Language Triplet Loss** ($\mathcal{L}_{\text{TRI}}$)：强制视觉特征 $\mathcal{V}^f$ 与匹配文本特征的距离小于与非匹配文本特征的距离，且差距至少为边距 $\alpha$，从而将文本的语义结构注入视觉表示空间。
   - **Multi-modal Classifier** ($\mathcal{L}_{\text{CLS}}$)：同时对视觉特征、匹配文本特征和非匹配文本特征施加二元交叉熵分类监督，文本分类头为活体/攻击判断提供额外的正则化约束，引导视觉分类器学习更鲁棒的决策边界。

总训练损失为两者的加权组合：

$$\mathcal{L}_{\text{TeG-DG}} = \mathcal{L}_{\text{CLS}} + \lambda \mathcal{L}_{\text{TRI}}$$

**关键设计要点**：文本模态仅在训练阶段作为正则化器参与，推理阶段完全丢弃，视觉分支独立完成前向推理。这使得 TeG-DG 在不增加部署复杂度的前提下，利用文本的跨域抽象能力显著提升了域泛化性能。消融实验（Table 4）证实，移除 TEVD 的文本对齐组件对性能的损害大于移除三元组损失，验证了文本监督在整个框架中的核心地位。

## 核心模块与公式推导

TeG-DG 的核心架构围绕一个关键洞察展开：**文本描述作为一种跨域通用的抽象表达，能够为视觉特征学习提供域不变的监督信号**，从而过滤掉光照、采集设备等残余风格偏差。整个框架由三个紧密协作的模块构成：Text Prompter（TP）负责动态生成配对文本，Hierarchical Attention Fusion（HAF）提取多粒度视觉特征，Textual-Enhanced Visual Discriminator（TEVD）通过跨模态对齐实现域泛化。

### 3.1 Text Prompter：文本提示的动态供应

TP 模块的核心功能是为每张训练图像动态提供匹配和非匹配的文本描述。其工作流程如下（见图 3）：

1. **提示库构建**：利用 GPT-4 自动生成语义相似的短语，构建包含多种攻击类型描述的提示库。例如，对于“打印攻击”类别，库中可能包含 "A high-quality printed face on paper"、"A face printed on glossy paper" 等变体。
2. **动态采样**：对于每张训练图像，TP 根据其攻击类型标签，从库中随机选取一条匹配文本提示（描述该攻击类型）和一条非匹配文本提示（描述其他攻击类型或真实人脸）。
3. **文本编码**：选中的文本提示通过冻结的 CLIP 文本编码器转换为文本特征 $\mathcal{T}^m$（匹配）和 $\mathcal{T}^n$（非匹配），供后续 TEVD 模块使用。

这一设计的优势在于：无需域标签，仅依靠攻击类型的粗粒度文本描述即可提供跨域一致的监督信号。

### 3.2 Hierarchical Attention Fusion：多粒度视觉特征融合

传统 ViT 仅使用最后一层的 [CLS] token 作为图像表示，忽略了浅层网络捕获的局部纹理细节（如打印伪影、屏幕摩尔纹等对 FAS 至关重要的线索）。HAF 模块通过自适应融合多层 [CLS] tokens 来解决这一问题（见图 4）。

**输入构建**：将 ViT 所有 $L$ 层的 [CLS] tokens 堆叠为输入矩阵：

$$X_{\mathrm{in}} = (z_{[\mathrm{CLS}]}^1, z_{[\mathrm{CLS}]}^2, \cdots, z_{[\mathrm{CLS}]}^L)^T$$

其中 $z_{[\mathrm{CLS}]}^l \in \mathbb{R}^{D}$ 为第 $l$ 层的 [CLS] token，$D$ 为 ViT 的隐藏维度。

**自注意力融合**：对层归一化后的输入进行线性投影得到 Q、K、V：

$$Q = \operatorname{LN}(X_{\mathrm{in}})W^Q, \quad K = \operatorname{LN}(X_{\mathrm{in}})W^K, \quad V = \operatorname{LN}(X_{\mathrm{in}})W^V$$

通过缩放点积注意力计算层间依赖关系：

$$\mathrm{Attention}(Q,K,V) = \mathrm{Softmax}\left(\frac{QK^T}{\sqrt{D}}\right)V$$

随后通过残差连接和 MLP 进行非线性变换：

$$\begin{cases} X_{\mathrm{hidden}} = \mathrm{Attention}(Q,K,V) + X_{\mathrm{in}} \\ X_{\mathrm{out}} = \mathrm{MLP}(\mathrm{LN}(X_{\mathrm{hidden}})) + X_{\mathrm{hidden}} \end{cases}$$

**跨模态投影**：取融合后的最后一层输出 $X_{\mathrm{out}}^{(L)}$，通过可学习投影矩阵 $M \in \mathbb{R}^{D \times D_{\mathrm{out}}}$ 映射到文本特征维度：

$$\mathcal{V}^f = \mathrm{LN}(X_{\mathrm{out}}^{(L)}) \cdot M$$

这一投影使得视觉特征与 CLIP 文本特征处于同一语义空间，为后续的跨模态对齐奠定基础。

### 3.3 Textual-Enhanced Visual Discriminator：文本引导的域泛化

TEVD 是 TeG-DG 实现域泛化的核心机制（见图 5），包含两个互补的损失函数：

**视觉-语言三元组损失**：强制视觉特征 $\mathcal{V}_{\mathrm{Norm}}^{f}$ 与匹配文本特征 $\mathcal{T}_{\mathrm{Norm}}^{m}$ 的距离小于与非匹配文本特征 $\mathcal{T}_{\mathrm{Norm}}^{n}$ 的距离，且差距至少为边距 $\alpha$：

$$\mathcal{L}_{\mathrm{TRI}} = \max(0, D(\mathcal{V}_{\mathrm{Norm}}^{f}, \mathcal{T}_{\mathrm{Norm}}^{m}) - D(\mathcal{V}_{\mathrm{Norm}}^{f}, \mathcal{T}_{\mathrm{Norm}}^{n}) + \alpha)$$

其中 $D(\cdot, \cdot)$ 为余弦距离，$\alpha$ 为预设边距。该损失将文本作为“原型”，引导视觉特征向域不变的语义中心靠拢。

**多模态分类损失**：同时对视觉特征、匹配文本特征和非匹配文本特征施加二元交叉熵监督。对于真实人脸样本（标签 $y=1$），期望视觉特征和匹配文本特征被分类为真，非匹配文本特征被分类为假；对于攻击样本（标签 $y=0$）则相反：

$$\mathcal{L}_{\mathrm{CLS}} = - (y \log(g(\mathcal{V}_{\mathrm{Norm}}^{f})) + \neg y \log(1 - g(\mathcal{V}_{\mathrm{Norm}}^{f}))) - (y \log(g(\mathcal{T}_{\mathrm{Norm}}^{m})) + \neg y \log(1 - g(\mathcal{T}_{\mathrm{Norm}}^{m}))) - (y \log(1 - g(\mathcal{T}_{\mathrm{Norm}}^{n})) + \neg y \log(g(\mathcal{T}_{\mathrm{Norm}}^{n})))$$

其中 $g(\cdot)$ 为共享的分类器，$\neg y$ 表示标签取反。这一设计使得文本模态的分类边界正则化视觉特征的决策边界，从而抑制域特定噪声。

**总损失函数**：

$$\mathcal{L}_{\mathrm{TeG-DG}} = \mathcal{L}_{\mathrm{CLS}} + \lambda \mathcal{L}_{\mathrm{TRI}}$$

其中 $\lambda$ 为平衡两个损失的超参数。训练完成后，TEVD 中的文本分支被完全移除，仅保留视觉编码器和分类器用于推理，不增加部署复杂度。

### 3.4 关键设计决策与消融验证

消融实验（Table 4）揭示了各模块的贡献层级：

- **移除 TEVD 中的文本对齐**（即去掉 $\mathcal{L}_{\mathrm{TRI}}$ 和文本分类分支）导致性能大幅下降，其损害程度超过仅移除三元组损失，证实文本监督是框架的核心驱动力。
- **同时移除 HAF 和 TEVD**（即退化为标准 ViT + 二元分类）的性能崩溃，表明两个模块存在强协同效应：HAF 提供多粒度特征，TEVD 利用文本引导这些特征向域不变方向收敛。

值得注意的是，TeG-DG 的训练依赖攻击类型标签来构建匹配/非匹配文本对。当细粒度标签不可用时，这一前提可能构成实际部署的瓶颈。

### 补充图表

![[assets/figures/papers/paper_list_l1502_https_arxiv_org_abs_2311_18420/figures/004_Figure_4.jpg]]
*Figure 4: Illustration of the designed Hierarchical Attention Fusion (HAF) module. The proposed HAF is a lightweight plug-and-play module that can be easily integrated into mainstream ViT models*

![[assets/figures/papers/paper_list_l1502_https_arxiv_org_abs_2311_18420/figures/005_Figure_5.jpg]]
*Figure 5: The proposed textual-enhanced visual discriminator (TEVD). TEVD consists of a vision-language triplet loss and a multi-modal classifier*

## 实验与分析

### 核心实验设置

实验遵循人脸反欺骗（FAS）领域标准的**留一域（Leave-One-Out, LOO）协议**，在四个公开数据集上进行交叉验证：OULU-NPU（O）、CASIA-MFSD（C）、Replay-Attack（I）、MSU-MFSD（M）。每次实验以三个数据集为源域训练，剩余一个作为未见目标域测试，以HTER（半总错误率）和AUC作为主要评价指标。数据集统计信息见 **Table 5**。

![[assets/figures/papers/paper_list_l1502_https_arxiv_org_abs_2311_18420/figures/012_Table_5.jpg]]
*Table 5: Four datasets for Leave-One-Out test*

### 主结果分析（LOO协议）

**Table 1** 汇总了TeG-DG与现有DG-FAS方法在全部四个LOO子协议上的对比结果。TeG-DG在所有协议上均取得最优HTER，且AUC在多数协议上领先：

- **I&C&M → O（目标域为OULU-NPU）**：TeG-DG取得HTER 5.68%、AUC 97.92%，相比之前最佳的**IADG**（Zhou et al., arXiv 2023）HTER降低了3.18个百分点。该协议下目标域包含多种光照与背景变化，文本监督在此展现出对复杂采集环境偏差的有效过滤。
- **O&C&I → M（目标域为MSU-MFSD）**：HTER低至1.88%，较**DiVT-M**（Liao et al., WACV 2023）降低0.98个百分点，表明在目标域攻击类型相对有限时，文本描述能精准捕捉攻击本质特征。
- **O&M&I → C（目标域为CASIA-MFSD）**：HTER从DiVT-M的8.67%降至3.17%，降幅达5.50个百分点。CASIA-MFSD包含多种低质量摄像头采集的样本，该结果直接验证了文本作为跨域通用监督对设备相关噪声的抑制能力。
- **O&C&M → I（目标域为Replay-Attack）**：HTER为3.21%，略优于DiVT-M的3.71%。

值得注意的是，TeG-DG在**不使用任何域标签**的条件下实现了上述性能，而对比方法如**MADDG**（Shao et al., CVPR 2019）依赖域标签进行对抗对齐，**SSAN-M**（Wang et al., CVPR 2022）需构建域风格组合。这从实证角度验证了文本监督可以替代显式域对齐机制，实现更简洁的域泛化。

### 极端有限源域场景

为模拟实际部署中标注数据稀缺的情况，实验进一步将源域数量从三个缩减至两个（**Table 2**）。在此设定下，性能差距急剧扩大：

![[assets/figures/papers/paper_list_l1502_https_arxiv_org_abs_2311_18420/figures/007_Table_2.jpg]]
*Table 2: Results on extremely limited source domains*

- **M&I → C**：TeG-DG HTER为6.19%，而IADG飙升至24.07%，绝对降幅达17.88个百分点；AUC从64.08%提升至97.08%。
- **M&I → O**：HTER从18.47%降至6.89%，AUC从89.88%提升至97.10%。

这一结果与论文声称的“约14% HTER相对降低和约12% AUC相对提升”一致。其因果机制在于：当视觉域覆盖不足时，传统方法提取的特征中域特定噪声占比急剧上升；而文本描述提供的攻击语义（如“打印照片攻击”“视频重放攻击”）是跨域恒定的，可在视觉特征退化的条件下维持分类边界的稳定性。

### Zero-Shot与Few-Shot分析

**Table 3** 展示了在LOO协议下的zero-shot和few-shot性能。Zero-shot设定下，TeG-DG仅激活多模态分类器（不进行视觉特征微调），而**CLIP**（Radford et al., ICML 2021）仅通过文本提示分类。TeG-DG在所有协议上大幅超越CLIP基线，验证了多模态分类器设计（同时利用视觉特征和匹配/非匹配文本特征进行联合决策）相较于纯文本分类的显著优势。

在few-shot设定（每类仅提供少量训练样本）下，TeG-DG仅需极少量样本即可达到甚至超过许多全量训练的DG方法。这一特性源于文本监督在训练初期即可提供强先验，降低了模型对大量视觉样本的依赖。

### 消融实验

**Table 4** 的系统消融揭示了各组件的贡献权重：

- **移除文本对齐（w/o text）**：在所有协议上HTER均显著上升，且损害程度大于移除三元组损失（w/o triplet）。这直接证实了文本监督是TeG-DG的核心驱动力，而非辅助正则项。
- **同时移除文本和三元组损失（w/o text + w/o triplet）**：即仅保留HAF模块进行纯视觉分类，性能大幅下降，表明HAF提取的多粒度视觉特征本身不足以实现域泛化，必须与TEVD协同工作。
- **移除HAF（使用标准ViT最后一层[CLS] token）**：性能亦有明显下降，验证了多层[CLS] token融合对捕捉多尺度伪造线索的必要性。

消融实验的因果链条清晰：文本描述提供域不变的语义锚点，三元组损失确保视觉特征向该锚点对齐，HAF则保证视觉特征本身包含足够丰富的判别信息——三者缺一不可。

### 可视化分析

**Figure 6** 的Grad-CAM可视化（协议O&M&I → C）显示，TeG-DG的注意力聚焦于人脸区域的关键伪造痕迹（如边缘模糊、色彩失真），而非背景或设备相关区域。**Figure 7** 的t-SNE特征分布对比表明，引入TeG-DG后，源域和目标域的活体/攻击样本特征分布更加对齐，域间散度显著缩小。这从特征空间层面解释了HTER降低的机制：文本监督将来自不同域的同类样本拉向共同的语义中心，从而抑制了域特定偏差对分类边界的影响。

### 基线对比与文本提示数量影响

**Table 6** 对比了不同视觉-语言基线方法，结果表明简单的对比损失或线性分类头无法替代TeG-DG精心设计的多模态分类器和三元组损失的组合效果。此外，附录中的 **Figure 14–17** 展示了文本提示数量对HTER/AUC的影响曲线：提示数量过少时文本覆盖不足，过多时可能引入噪声，存在一个协议相关的最优区间。当前方法从固定库中随机采样，尚未实现自适应选择，这是论文明确指出的局限性之一。

### 补充图表

![[assets/figures/papers/paper_list_l1502_https_arxiv_org_abs_2311_18420/figures/006_Table_1.jpg]]
*Table 1: Test HTER (↓) and AUC (↑) of FAS methods on OIMC datasets. The * indicates using the CelebA-Spoof [83] as the supplementary source dataset (bold indicates best performance, underline indicates second best performance.)*

![[assets/figures/papers/paper_list_l1502_https_arxiv_org_abs_2311_18420/figures/008_Table_3.jpg]]
*Table 3: Zero-shot and few-shot performance evaluated on Leave-One-Out (LOO) protocol*

![[assets/figures/papers/paper_list_l1502_https_arxiv_org_abs_2311_18420/figures/009_Table_4.jpg]]
*Table 4: Evaluations of different components of the proposed TeG-DG framework*

![[assets/figures/papers/paper_list_l1502_https_arxiv_org_abs_2311_18420/figures/010_Figure_6.jpg]]
*Figure 6: The Grad-CAM [59] visualizations of our TeG-DG method under protocol O&M&I to C*

![[assets/figures/papers/paper_list_l1502_https_arxiv_org_abs_2311_18420/figures/011_Figure_7.jpg]]
*Figure 7: The t-SNE feature visualization on O&M&I to C. We plot the visual feature distribution w/ and w/o TeG-DG*

![[assets/figures/papers/paper_list_l1502_https_arxiv_org_abs_2311_18420/figures/013_Figure_8.jpg]]
*Figure 8: CLIP model lacks the knowledge of FAS tasks*

![[assets/figures/papers/paper_list_l1502_https_arxiv_org_abs_2311_18420/figures/014_Table_6.jpg]]
*Table 6: Comparison to Baseline Method. ‘(Linear)’ means only using a linear classification head*

## 方法谱系与知识库定位

### 与现有域泛化FAS方法的关系

TeG‑DG 的核心创新在于**将文本描述作为跨域通用监督信号**引入人脸反欺骗的域泛化训练，这与现有的主流范式形成本质差异。传统域泛化 FAS 方法主要依赖以下策略：

- **对抗域对齐**：如 **MADDG** (Shao et al., CVPR 2019) 通过域分类器和梯度反转层强制学习域不变特征，但需要显式的域标签，且对抗训练过程不稳定。
- **风格解耦与重组**：如 **SSAN‑M** (Wang et al., CVPR 2022) 将图像分解为风格和内容成分，通过风格重组增强域多样性，但风格与内容的分离边界难以精确界定。
- **实例白化/标准化**：如 **IADG** (Zhou et al., arXiv 2023) 通过实例白化消除域特定统计量，无需域标签，但可能同时抹除有助于判别攻击类型的细粒度纹理信息。
- **Vision Transformer 架构**：如 **DiVT‑M** (Liao et al., WACV 2023) 利用 ViT 的自注意力机制捕捉全局上下文，但仍仅从视觉模态提取特征，未解决跨域风格偏差的残余问题。

TeG‑DG 的关键突破在于**用文本模态的抽象性和跨域一致性来替代域标签或风格解耦**。文本描述（如“一张打印在A4纸上的攻击人脸”）天然具备跨域不变性：无论图像采集自何种光照、设备或背景，同一攻击类型的文本语义保持恒定。通过 **Textual‑Enhanced Visual Discriminator (TEVD)** 中的视觉‑语言三元组损失和多模态分类器，TeG‑DG 将视觉特征与匹配/不匹配的文本原型对齐，从而在特征空间中过滤掉域特定的风格噪声，保留与攻击本质相关的语义特征。这一机制使得 TeG‑DG 在无需域标签的情况下，实现了对域偏移更强的鲁棒性。

与 **CLIP** (Radford et al., ICML 2021) 的零样本/少样本范式相比，TeG‑DG 并非直接使用预训练的视觉‑语言模型进行推理。实验表明（Table 3），CLIP 在 FAS 任务上的零样本性能极差（HTER 高达 40% 以上），原因是 CLIP 的预训练语料缺乏对打印攻击、重放攻击、面具攻击等细粒度安全概念的充分覆盖（见 Figure 8）。TeG‑DG 通过 **Text Prompter (TP)** 利用 GPT‑4 生成针对 FAS 任务的专用提示库，并在训练过程中动态提供匹配/不匹配文本对，使模型学会区分攻击类型的语义边界，从而大幅超越 CLIP 基线。

### 适用边界

TeG‑DG 的设计在以下条件下展现出显著优势：

1. **源域数量极度有限**：当仅有两个源域可用时（Table 2），TeG‑DG 在 M&I→C 协议上 HTER 为 6.19%，相比 IADG 的 24.07% 降低了约 17.88 个百分点；在 M&I→O 协议上 HTER 为 6.89%，相比 IADG 的 18.47% 降低了约 11.58 个百分点。这表明文本监督在数据匮乏时能提供更稳定的正则化。

2. **无需域标签的场景**：对于域标签难以获取或标注成本高昂的实际部署环境，TeG‑DG 的文本引导对齐机制天然适配，因为它仅依赖攻击类型标签（打印、重放、面具等）来构建文本提示，而不需要知道图像来自哪个域。

3. **少样本自适应**：在 Leave‑One‑Out 协议的 few‑shot 设定下（Table 3），TeG‑DG 仅需少量目标域样本即可达到甚至超过许多全量训练的 DG 方法，这得益于文本原型提供的强先验。

然而，TeG‑DG 的适用边界也存在明确限制：

- **依赖攻击类型细粒度标签**：训练需要为每张图像提供攻击类型信息以选择匹配/不匹配文本提示。若只能获取真/假二值标签而无法区分攻击子类，则文本提示的选择将退化为随机，会削弱 TEVD 的对齐效果。
- **提示库的覆盖范围**：提示库由 GPT‑4 自动生成，虽然减少了人工偏差，但其覆盖的攻击样式受限于语言模型的内部知识。对于全新的、超出 GPT‑4 知识范围的攻击类型（如新型材料面具或特定场景的深度伪造），生成的文本描述可能不准确或缺乏区分度。
- **推理阶段无文本增强**：TEVD 在推理时被完全移除，仅保留视觉分支。这意味着模型无法利用测试时的附加文本信息（如设备型号、场景描述等）进一步提升性能，在域偏移极大的情况下可能仍有残余偏差。

### 局限与开放问题

**已识别的局限**：

1. **攻击类型标注成本**：细粒度攻击类型标签的获取在实际场景中可能代价高昂。论文未探讨在仅有二值标签或弱监督条件下的变通方案。
2. **提示数量敏感性**：附录实验（Figure 14‑17）表明文本提示数量影响性能，且不同协议下的最优数量可能不同。当前方法采用固定数量，缺乏自适应选择机制。
3. **理论保证缺失**：虽然实验展示了在有限源域下的优异表现，但缺少对“文本监督为何能提供域不变性”的形式化理论分析，也未给出泛化误差界。
4. **全新攻击类型的泛化**：在极端域偏移（如训练集中从未出现的攻击媒介）下，文本原型可能同样失效，因为 GPT‑4 生成的描述无法覆盖未知概念。

**开放问题**：

- 能否为每个样本**动态生成个性化文本提示**（而非从固定库中随机选择），以更精准地匹配图像中的攻击特征？
- 如何**量化文本提示的质量**？是否存在可优化的评价指标（如提示与图像特征的互信息、分类置信度增益等）来指导提示库的构建和筛选？
- 能否将文本监督与传统的**域对齐或对抗训练方法结合**，形成互补——文本提供语义级不变性，对抗训练提供统计级不变性？
- 在攻击类型标签不可用的场景下，是否可以利用**弱监督或半监督方式**（如聚类伪标签、多模态大模型的零样本推理）自动生成文本描述？
- 如何在**推理阶段保留文本模态的优势**，例如通过测试域的无标签文本描述（设备信息、场景元数据）进行测试时自适应？

## 原文 PDF

![[paperPDFs/arxiv_2023/TeG_DG_Textually_Guided_Domain_Generalization_for_Face_Anti_Spoofing.pdf]]
