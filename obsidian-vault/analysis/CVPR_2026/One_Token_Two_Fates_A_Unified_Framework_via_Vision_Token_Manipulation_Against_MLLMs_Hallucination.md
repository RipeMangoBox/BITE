---
title: "One Token, Two Fates: A Unified Framework via Vision Token Manipulation Against MLLMs Hallucination"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/One_Token_Two_Fates_A_Unified_Framework_via_Vision_Token_Manipulation_Against_MLLMs_Hallucination.pdf
project_link: null
code_link: null
aliases:
- ULCSVCSCRCC
- OTTFUFVTMAMH
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/generative_models_diffusion
- topic/representation_self_supervised_transfer
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: 视觉令牌是连接图像与文本的枢纽，通过对其进行增强（合成互补视觉上下文）与剪枝（构造隐空间负样本）两种操作，可以在统一的中间表示层面同时调节视觉信号的强度与文本惯性的抑制。
primary_logic: 视觉令牌具有双重潜力：增强令牌提供互补视觉语义以抵御视觉衰退，剪枝令牌利用信息缺口生成稳定、分布内的幻觉探针，从而精确隔离并消除模型内部偏差。两者可在同一表示层级上协同工作，实现高效的训练无关幻觉抑制。
claims:
- 视觉注意力随生成逐步衰减，与幻觉频率呈负相关，证实视觉-语言失衡是幻觉的直接原因（Finding F1）。
- 增强（翻转、加噪）后的视觉令牌与原始令牌提供互补语义，融合后可得到更聚焦的视觉上下文（Finding F2）。
- 隐空间令牌剪枝（信息缺口）产生的负样本聚类在原始图像表示附近，构成分布内探针，比像素级掩码（模态缺口）更稳定，更适合用于偏差校准（Finding F3）。
- 简单组合视觉注意力增强（PAI）与输出 logits 对比解码（VCD）不仅无提升，甚至使性能下降，表明需要统一的表示层级校准。
---

# One Token, Two Fates: A Unified Framework via Vision Token Manipulation Against MLLMs Hallucination

> [!tip] 核心洞察
> 视觉令牌具有双重潜力：增强令牌提供互补视觉语义以抵御视觉衰退，剪枝令牌利用信息缺口生成稳定、分布内的幻觉探针，从而精确隔离并消除模型内部偏差。两者可在同一表示层级上协同工作，实现高效的训练无关幻觉抑制。

| 字段 | 内容 |
|------|------|
| 中文题名 | 一令牌，两命运：面向多模态大模型幻觉的统一视觉令牌操纵框架 |
| 英文题名 | One Token, Two Fates: A Unified Framework via Vision Token Manipulation Against MLLMs Hallucination |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2603.10360) |
| Topic | #topic/vision_multimodal_applications #topic/generative_models_diffusion #topic/representation_self_supervised_transfer #topic/vision_multimodal_applications/image_and_video_generation |
| Method | 统一隐空间校准框架（Unified Latent Calibration，含 Synergistic Visual Calibration (SVC) 与 Causal Representation Calibration (CRC) 模块） |
| Dataset | POPE, Inference Efficiency, CHAIR |

> [!tip] 效果简介
> - POPE (GQA split) 上，Accuracy 81.54% (LLaVA-1.5, GQA split); 平均绝对提升2% vs Vanilla LLaVA-1.5 (具体数值未给出，但基于平均提升2%的陈述推断其约为79.5%) (+2% (平均))。
> - Inference Efficiency 上，Inference latency overhead (relative to vanilla) 1.06x vs 1.00x (Vanilla) (+0.06x)。
> - CHAIR (LLaVA-1.5, 64 tokens) 上，CHAIR_I 18.1 (最低幻觉实例得分) vs VCD, PAI, VISTA等 (数值未单独列出，文中指本文达到最优) (比最优基线更低)。

## 概要

多模态大模型（MLLM）在视觉-语言任务中展现出强大能力，却普遍受困于“幻觉”现象——生成与图像事实不符的内容。本文的核心诊断是：**视觉信号在逐词生成过程中持续衰减，而模型内部强大的语言先验逐渐占据主导，形成系统性的视觉-语言失衡**。这一失衡被实证为幻觉的直接原因（Figure 2, F1）：视觉注意力随生成步数急剧下降，而幻觉频率恰好在视觉基础最薄弱的区域飙升。

围绕这一瓶颈，本文提出**“一令牌，两命运”的统一隐空间校准框架**。其核心洞察在于：**视觉令牌是连接图像与文本的枢纽**，通过对其进行两种互补操作——增强与剪枝——可以在统一的中间表示层面同时调节视觉信号强度与文本惯性抑制。具体而言，**协同视觉校准（SVC）** 模块利用翻转、加噪等增强图像构造互补视觉上下文，以插值方式注入中间层隐状态，抵御视觉衰退；**因果表示校准（CRC）** 模块则通过随机剪枝视觉令牌至仅剩5个，在隐空间构造分布内负样本，于浅层逐层计算稳定的幻觉方向向量并予以消除，从而抑制语言先验偏差（Figure 3, Figure 4）。

该方法的关键优势在于**统一性**：SVC与CRC均作用于中间表示层（Lc=16），共享视觉令牌作为唯一信息源，避免了先前工作中注意力增强（如**PAI**, Liu et al., ECCV 2024）与输出logits对比解码（如**VCD**, Leng et al., CVPR 2024）因层级与时域不一致而相互冲突的问题。简单组合这两类分离范式甚至会导致性能下降（Figure 1），而本文的统一框架实现了协同增益。

在实验验证上，该框架在POPE基准上取得平均绝对**2%的准确率提升**（LLaVA-1.5），推理延迟仅增加**1.06倍**，并在CHAIR、MME、MMHal-Bench等多个基准上全面超越训练无关的基线方法（包括**VISTA**, Li et al., ICML；**ONLY**, Wan et al., arXiv 2025）。方法在四种不同架构的MLLM（LLaVA-1.5、Shikra、MiniGPT-4、InstructBLIP）上均验证有效，覆盖线性投影与Q-Former两类视觉-语言对齐方式，展现出良好的泛化性。

### 多模态大模型的幻觉困境

多模态大模型（MLLM）在视觉理解与生成任务中展现出强大的能力，但其输出中频繁出现的“幻觉”现象——即生成与图像内容不一致的描述——严重制约了其在真实场景中的可靠性。幻觉问题的根源并非简单的感知错误，而是深植于模型架构内部的系统性失衡。

具体而言，在自回归生成过程中，模型对视觉信号的依赖程度随生成步数增加而急剧衰减。如 Figure 2 (F1) 所示，视觉注意力在生成初期尚能保持聚焦，但随着序列推进，注意力分布迅速发散，而幻觉频率恰好在视觉基础最薄弱的区域急剧攀升。这一负相关关系揭示了一个关键机制：**语言先验在生成后期逐渐占据主导地位，视觉信号被系统性压制，形成视觉-语言失衡**。当模型无法有效提取视觉证据时，其内部强大的语言先验便会“填补空白”，产生看似合理实则虚构的输出。

### 现有方法的碎片化困境

针对上述问题，学界已提出多种训练无关的缓解策略，大致可分为两条技术路线：

- **视觉注意力增强**：代表性工作如 **PAI**（Liu et al., ECCV 2024），通过在特定层提升视觉令牌的注意力权重来强化视觉基础。
- **输出端对比解码**：代表性工作如 **VCD**（Leng et al., CVPR 2024），在最终 logits 层面进行对比解码，以抑制文本惯性。

然而，这两类方法存在根本性的局限。首先，它们分别作用于模型的不同层级与不同时域——注意力增强发生在中间层，而对比解码作用于最终输出端——两者在信号流上相互割裂。如 Figure 1 所示，简单地将 PAI 与 VCD 组合使用，非但未能获得叠加收益，反而导致性能下降。这一反直觉的结果表明：**碎片化的干预方式会在模型内部引入冲突信号，不同模块的校准方向可能相互抵消**。

此外，现有方法在构造负样本以探测模型内部偏差时，通常依赖像素级掩码（即直接遮盖部分图像区域）。然而，这种操作引入的是模态层面的缺口——掩码后的图像在分布上严重偏离原始视觉输入，产生的负样本噪声大、不稳定，难以作为可靠的偏差探针。

### 本文动机：统一隐空间校准

上述分析指向一个核心洞察：视觉令牌是连接图像与文本的枢纽，也是调节视觉-语言平衡的天然控制点。本文提出**统一隐空间校准框架**，核心思想是通过对视觉令牌的两种操作——增强与剪枝——在同一表示层级上协同调节视觉信号强度与文本惯性抑制。

具体而言，该框架包含两大模块：

1. **协同视觉校准（SVC）**：通过对原始图像施加翻转、模糊、加噪等变换生成增强图像，将其视觉令牌与原始令牌拼接形成协同视觉记忆库 $\mathbf{V}_{\mathrm{syn}}$。如 Figure 2 (F2) 所示，增强令牌与原始令牌提供互补的语义关注（例如对“相机”的不同区域聚焦），二者的融合可构建更全面的视觉上下文，从而在关键中间层注入以抵消视觉衰退。

2. **因果表示校准（CRC）**：通过随机剪枝视觉令牌至仅剩 $N_h=5$ 个，在隐空间构造信息缺口，生成分布内的负样本。如 Figure 2 (F3) 及 Figure 8 的 t-SNE 可视化所示，剪枝产生的负样本聚类在原始图像表示附近，构成稳定的分布内探针；相比之下，像素级掩码产生的表示则发散且偏离分布。基于这些负样本，CRC 计算稳定的幻觉方向向量，在浅层逐层净化隐状态，实现偏差消除。

与碎片化的现有方法不同，该框架将增强与校准统一在中间表示层 $L_c=16$ 完成，无需触及最终解码器，从而避免了信号冲突。实验表明，该方法在 POPE 基准上平均绝对提升 2%，而推理延迟仅增加 1.06 倍，实现了性能与效率的优异平衡。

## 核心方法与创新机理

本文的核心创新在于将视觉令牌（vision tokens）从被动的信息载体重新定位为主动的校准枢纽，在统一的隐空间表示层上同时完成**视觉增强**与**偏差消除**，从而系统性修复多模态大模型（MLLM）的视觉-语言失衡。相较于以往分离式方法在不同层级（注意力层 vs. 输出 logits 层）各自为政、甚至相互冲突的局限，本工作实现了三个关键槽位的统一重构。

### 从分离式干预到统一隐空间校准

现有训练无关的幻觉缓解方法主要沿两条独立路径展开：一是**视觉注意力增强**，如 **PAI**（Liu et al., ECCV 2024）通过提升视觉注意力权重来强化视觉基础；二是**文本解码偏置校正**，如 **VCD**（Leng et al., CVPR 2024）在输出 logits 层面进行对比解码以抑制语言先验。然而，简单组合这两类方法不仅未能带来增益，反而导致性能下降（Figure 1），揭示出分离式干预在时域与层级上的不一致会产生冲突信号。

本工作提出的**统一隐空间校准框架**（Unified Latent Calibration）将全部干预操作收敛至中间表示层 $L_c=16$，包含两个协同模块：
- **协同视觉校准（SVC）**：在中间层通过注意力机制注入增强视觉上下文，以插值方式融入隐状态，抵消生成过程中的视觉信号衰减。
- **因果表示校准（CRC）**：在浅层（$1 \dots L_c$）逐层计算并消去幻觉方向向量，在归一化隐空间内净化表示，抑制语言先验。

两者均在隐空间完成，无需解码至输出 logits，从根本上避免了层级不一致带来的信号冲突。

### 关键槽位一：视觉上下文构建——从单一令牌到协同记忆库

**Baseline 做法**：仅使用原始图像经视觉编码器产生的令牌作为视觉上下文，在生成过程中视觉信号逐渐衰减，模型逐渐被语言先验主导。

**本文创新**：构建**协同视觉记忆库** $\mathbf{V}_{\mathrm{syn}} = [\mathbf{V}; \mathbf{V}_{\mathrm{aug}}] \in \mathbb{R}^{2 N_v \times d}$，将原始图像令牌与经翻转、高斯模糊、椒盐噪声增强后的图像令牌拼接（Eq.3）。在关键中间层 $L_c$，通过缩放点积注意力计算增强视觉上下文 $\mathbf{C}_t$（Eq.4），并以插值方式融入原始隐状态：

$$\mathbf{H}_t^{\prime(L_c)} = (1 - \lambda_s) \cdot \mathbf{H}_t^{(L_c)} + \lambda_s \cdot \mathbf{C}_t$$

这一设计的核心洞察（Finding F2）在于：增强后的图像令牌与原始令牌提供**互补的语义聚焦**——例如原始令牌可能关注物体的局部纹理，而翻转/加噪后的令牌则捕捉全局结构信息，融合后形成更完整的视觉基础。TAM 可视化（Figure 7）证实，SVC 能够将原本发散的注意力集中到与查询相关的正确视觉区域。

### 关键槽位二：幻觉偏差探针——从模态缺口到信息缺口

**Baseline 做法**：无系统性探针，或使用像素级掩码（masked image）产生的失真图像作为负样本。然而，像素级掩码引入了**模态缺口**（modality-gap）——失真图像与自然图像的分布差异导致产生的负样本不稳定、噪声大，不适合用于偏差校准（Finding F3）。

**本文创新**：通过**随机剪枝视觉令牌**至仅保留 $N_h=5$ 个的方式，在隐空间构造**分布内负样本**。具体而言，CRC 模块在原始输入流之外构建一条并行的“幻觉探针流”（Figure 3 紫色路径），将剪枝后的令牌输入模型，计算原始表示与剪枝表示的差分向量，并平均 $K=3$ 个负样本得到稳定的幻觉方向向量：

$$\mathbf{v}_{\mathrm{crc}}^{(l)} = \frac{1}{K} \sum_{k=1}^{K} \Delta \mathbf{H}^{(l,k)}$$

t-SNE 可视化（Figure 8）证实，剪枝令牌产生的负样本紧密聚类在原始图像表示附近，构成**分布内探针**；而像素级掩码图像则表示发散，属于分布外扰动。这一信息缺口策略的优越性在于：剪枝仅移除信息量（减少视觉令牌数量），而不改变令牌本身的分布特性，因此产生的负样本能够精确隔离模型内部的偏差信号，而非引入额外的模态噪声。

### 关键槽位三：干预层级与方式——从层内/输出端到统一表示层

**Baseline 做法**：注意力增强在某一层内操作，logits 对比解码在输出端操作，两者时域与层级不一致，简单组合产生冲突（Figure 1）。

**本文创新**：将所有校准操作统一在**中间表示层**完成：
- **SVC** 在层 $L_c$ 通过插值注入增强视觉上下文，直接强化隐状态中的视觉成分。
- **CRC** 在层 $1 \dots L_c$ 逐层执行校准：在归一化空间内将隐状态沿幻觉方向的反方向调整 $\mathbf{h}_{\mathrm{crc}} = \mathbf{h}_{\mathrm{norm}} + \lambda_c \cdot \mathbf{v}_{\mathrm{norm}}$（Eq.10），再重归一化恢复原始幅度（Eq.11），得到净化后的表示。

消融实验（Table 5）证实，SVC 和 CRC 各自独立均能带来性能提升，而融合两个模块后达到所有指标的最佳分数，验证了统一表示层级校准的协同效应。值得注意的是，CRC 探针最终捕获的是**纯视觉差异** $\mathbf{v}_{\mathrm{crc}}^{(l)} \approx \mathcal{E}(V - V_{\mathrm{neg}})$（Eq.14），在消除共享查询与偏差效应后，该方向精确对应视觉信息衰减所损失的真实信号，为反事实校准提供了理论依据。

**核心诊断：视觉-语言失衡是幻觉的系统性瓶颈。** 多模态大模型在自回归生成过程中，视觉注意力随解码步数增加而急剧衰减，而模型内部强大的语言先验逐渐占据主导地位。这一失衡被本文的发现 **F1** 所证实：视觉注意力与幻觉频率呈显著负相关（Figure 2, F1）。基于此诊断，本文提出一个统一的隐空间校准框架，在单一表示层级上同时调节视觉信号的强度与文本惯性的抑制。

**框架由两条并行流和两个核心模块构成。** 如 Figure 3 所示，模型同时处理两条输入流：
- **原始流（橙色路径）**：输入原始图像令牌 $\mathbf{V}$，经视觉编码器和 LLM 的浅层处理后，在第 $L_c$ 层进入 SVC 模块。
- **幻觉探针流（紫色路径）**：将视觉令牌随机剪枝至仅保留 $N_h=5$ 个，构造隐空间负样本。该流与原始流共享浅层处理，但其隐状态用于 CRC 模块提取幻觉方向。

两个模块协同工作于统一的表示层级 $L_c=16$：

1. **协同视觉校准（SVC）**：在 $L_c$ 层，将原始令牌 $\mathbf{V}$ 与经翻转、高斯模糊、椒盐噪声增强后的令牌 $\mathbf{V}_{\mathrm{aug}}$ 拼接为协同视觉记忆库 $\mathbf{V}_{\mathrm{syn}} = [\mathbf{V}; \mathbf{V}_{\mathrm{aug}}] \in \mathbb{R}^{2N_v \times d}$。通过缩放点积注意力计算增强视觉上下文 $\mathbf{C}_t$（Eq. 4），再以插值方式融入原始隐状态（Eq. 5）：
   $$\mathbf{H}_t^{\prime(L_c)} = (1 - \lambda_s) \cdot \mathbf{H}_t^{(L_c)} + \lambda_s \cdot \mathbf{C}_t$$
   其中 $\lambda_s=0.06$ 为插值强度。该操作通过注入互补视觉语义，直接抵消视觉信号的衰减。

2. **因果表示校准（CRC）**：在浅层 $1 \dots L_c$，利用剪枝流与原始流的隐状态差分 $\Delta\mathbf{H}^{(l,k)}$，对 $K=3$ 个负样本取平均，得到稳定的幻觉方向向量 $\mathbf{v}_{\mathrm{crc}}^{(l)}$（Eq. 8）。该向量经理论推导可近似为纯视觉差异 $\mathcal{E}(V - V_{\mathrm{neg}})$（Eq. 14），即模型因视觉信息缺失而产生的偏差。随后在归一化空间内，将原始隐状态沿该方向的反方向线性调整（Eq. 10），并重归一化恢复原始幅度（Eq. 11），从而净化隐状态中的语言先验偏差。

**模块间的协同机制。** SVC 与 CRC 虽作用于同一表示层级，但功能互补：SVC 通过增强视觉上下文提升模型对图像信息的利用，CRC 通过消除偏差方向抑制语言先验的过度主导。两者均以视觉令牌为唯一操作对象——增强令牌提供互补语义，剪枝令牌构造分布内探针——实现了“一令牌，两命运”的设计理念。消融实验（Table 5）证实，两个模块各自独立均较 Vanilla 基线带来性能提升，融合后达到所有指标的最佳分数，且推理延迟仅增加 $1.06\times$。

![[assets/figures/papers/paper_list_l2263_https_arxiv_org_abs_2603_10360/figures/003_Figure_3.jpg]]
*Figure 3: Overview of our unified framework. The model processes an original input stream (orange path) and a parallel hallucinationprobe stream (purple path) derived from pruned vision tokens. Our Synergistic Visual Calibration (SVC) module injects complementary visual context from augmented images into a critical middle layer*

### 2.1 问题形式化

多模态大模型的生成过程可形式化为自回归解码。给定输入图像 $I$ 和文本提示 $T$，模型在第 $t$ 步生成词元 $y_t$ 的概率分布为：

$$y_{t} \sim p_{\theta}(y_{t} | I, T, \mathbf{y}_{<t}) = \operatorname{softmax}(f_{\theta}(I, T, \mathbf{y}_{<t})) \tag{Eq.(2)}$$

其中 $f_{\theta}$ 输出未归一化的 logits。在第 $l$ 层输出的隐状态记为：

$$\mathbf{H}_{t}^{(l)} = \mathcal{D}^{(1...l)}(\mathbf{H}_{t}^{(0)}) \tag{Eq.(1)}$$

$\mathcal{D}^{(1...l)}$ 表示从输入到第 $l$ 层的逐层解码过程，$\mathbf{H}_{t}^{(0)}$ 为初始输入表示（包含视觉令牌和文本令牌的拼接）。

### 2.2 统一框架概述

本文提出的统一隐空间校准框架（Unified Latent Calibration）由两个核心模块构成：**协同视觉校准（SVC）** 和 **因果表示校准（CRC）**。两个模块均工作在中间表示层 $L_c=16$，避免了解耦方法中注意力增强与输出 logits 矫正因时域不一致而产生的信号冲突（Finding F1 和 Figure 1 证实了简单组合 PAI 与 VCD 会导致性能退化）。

SVC 模块在关键中间层注入增强视觉上下文，以抵消生成过程中视觉注意力的逐步衰减；CRC 模块在浅层（$1 \dots L_c$）逐层计算并消除幻觉方向向量，抑制语言先验的过度主导。两者共享视觉令牌作为唯一操作源，形成协同效应。

### 2.3 协同视觉校准（SVC）

SVC 的核心思路是利用增强图像的互补语义来强化视觉基础。具体步骤如下：

**协同视觉记忆库构建。** 对原始图像施加三种增强变换——水平翻转、高斯模糊、椒盐噪声——得到增强图像，将其与原始图像分别编码为视觉令牌后拼接，形成记忆库：

$$\mathbf{V}_{\mathrm{syn}} = [\mathbf{V}; \mathbf{V}_{\mathrm{aug}}] \in \mathbb{R}^{2 N_{v} \times d} \tag{Eq.(3)}$$

其中 $\mathbf{V}$ 为原始视觉令牌，$\mathbf{V}_{\mathrm{aug}}$ 为增强视觉令牌，$N_v$ 为原始视觉令牌数，$d$ 为隐空间维度。

**增强上下文计算。** 在第 $L_c-1$ 层的隐状态 $\mathbf{H}_{t}^{(L_c-1)}$ 作为查询，对 $\mathbf{V}_{\mathrm{syn}}$ 执行缩放点积注意力，得到增强视觉上下文向量：

$$\mathbf{C}_{t} = \mathrm{softmax}\left(\frac{\mathbf{H}_{t}^{(L_c-1)}(\mathbf{V}_{\mathrm{syn}})^{T}}{\sqrt{d}}\right) \mathbf{V}_{\mathrm{syn}} \tag{Eq.(4)}$$

**插值融合。** 将增强上下文与第 $L_c$ 层的原始隐状态通过插值系数 $\lambda_s$ 融合：

$$\mathbf{H}_{t}^{\prime(L_{c})} = (1 - \lambda_{s}) \cdot \mathbf{H}_{t}^{(L_{c})} + \lambda_{s} \cdot \mathbf{C}_{t} \tag{Eq.(5)}$$

$\lambda_s=0.06$ 是消融实验确定的最优值（Figure 9b），在该取值下模型既能获得增强视觉信息，又不至于过度偏离原始表示。

### 2.4 因果表示校准（CRC）

CRC 通过构造隐空间负样本来估计并消除“幻觉方向”，其理论基础源于结构因果模型（SCM，Figure 5）：模型内在偏差 $B$ 对隐表示 $H^{(l)}$ 存在虚假因果路径，混淆了真实的视觉因果路径 $V \to H^{(l)}$。

**负样本构造。** 将视觉令牌随机剪枝至仅保留 $N_h=5$ 个，形成信息缺口。与像素级掩码（模态缺口）不同，这种隐空间剪枝产生的负样本在 t-SNE 可视化中紧密聚集于原始图像表示附近，构成分布内探针（Finding F3，Figure 8）。

**幻觉方向估计。** 对 $K=3$ 个独立剪枝样本，分别计算其与原始表示的差分向量，取平均得到稳定的幻觉方向：

$$\mathbf{v}_{\mathrm{crc}}^{(l)} = \frac{1}{K} \sum_{k=1}^{K} \Delta \mathbf{H}^{(l,k)} \tag{Eq.(8)}$$

其中 $\Delta \mathbf{H}^{(l,k)} = \mathbf{H}_{\mathrm{org}}^{(l)} - \mathbf{H}_{\mathrm{neg}}^{(l,k)}$ 为第 $k$ 个负样本在第 $l$ 层的差分表示。

**理论性质。** 在消除共享查询和偏差效应后，该探针捕获的是纯视觉差异：

$$\mathbf{v}_{\mathrm{crc}}^{(l)} \approx \mathcal{E}(V - V_{\mathrm{neg}}) \tag{Eq.(14)}$$

这表明 CRC 探针能有效隔离因视觉信号衰减而丢失的纯视觉信息，而非模型偏差或查询条件的混杂效应。

**隐空间净化。** 在归一化空间内，将原始隐状态沿幻觉方向的反方向进行线性调整：

$$\mathbf{h}_{\mathrm{crc}} = \mathbf{h}_{\mathrm{norm}} + \lambda_{c} \cdot \mathbf{v}_{\mathrm{norm}} \tag{Eq.(10)}$$

其中 $\mathbf{h}_{\mathrm{norm}}$ 和 $\mathbf{v}_{\mathrm{norm}}$ 分别为归一化后的隐状态和幻觉方向向量，$\lambda_c=0.10$ 为校准强度。最后通过重归一化恢复原始幅度：

$$\mathbf{H}_{t,\mathrm{pos}}^{(l)} = \frac{\mathbf{h}_{\mathrm{crc}}}{||\mathbf{h}_{\mathrm{crc}}||_{2}} \cdot ||\mathbf{H}_{t,\mathrm{org}}^{(l)}||_{2} \tag{Eq.(11)}$$

CRC 在 $l=1$ 到 $L_c$ 的每一层独立执行，逐层净化隐状态。幻觉方向向量 $\mathbf{v}_{\mathrm{crc}}^{(l)}$ 可预先计算并缓存，推理时直接复用，因此额外计算开销极小。

## 实验与关键发现

### 主结果：幻觉抑制与通用能力

所提统一隐空间校准框架在四个不同架构的 MLLM（LLaVA-1.5、Shikra、MiniGPT-4、InstructBLIP）上进行了全面评估，覆盖线性投影与 Q-Former 两类视觉-语言对齐方式。幻觉评估采用 POPE、CHAIR 和 MMHal-Bench 三个基准，通用能力评估采用 MME 基准。

**POPE 基准**（Table 1）上，该方法在 LLaVA-1.5 上取得 81.54% 的准确率，平均绝对提升约 2%。四个模型的一致提升验证了方法的架构无关性——无论是线性投影还是 Q-Former，统一隐空间校准均能有效缓解幻觉。

**CHAIR 基准**（Table 2）评估生成描述中的幻觉物体。在 LLaVA-1.5（64 tokens）设置下，该方法取得 CHAIR_I 18.1 的最优得分，优于 VCD（Leng et al., CVPR 2024）、PAI（Liu et al., ECCV 2024）、VISTA（Li et al., ICML）和 ONLY（Wan et al., arXiv 2025）等训练无关基线。在 128 tokens 设置下，MiniGPT-4 和 Shikra 上同样取得最优 CHAIR_I 分数。

**MMHal-Bench**（Figure 6）的雷达图显示，该方法在八个评估类别上全面超越 Vanilla、PAI 和 VISTA，覆盖面积明显更大，表明幻觉抑制未以牺牲特定类别能力为代价。

**MME 通用能力**（Table 3）的感知与认知得分表明，该方法在所有测试模型上均取得最优或次优结果，证明隐空间校准不会损害模型的通用多模态理解能力。

**推理效率**（Table 4）方面，该方法推理延迟仅为 Vanilla 模型的 1.06 倍，显著优于需要多次前向传播的对比解码方法。吞吐量和峰值 GPU 显存占用同样保持竞争力。

### 消融研究

**模块贡献**（Table 5）：SVC（使用 V_syn 增强视觉上下文）与 CRC（使用剪枝令牌构造负样本）各自独立均较 Vanilla 基线带来性能提升。融合两个模块后，所有指标达到最佳分数，证实增强与校准在统一隐空间中的协同效应。这与 Figure 1 的发现一致：简单组合注意力增强（PAI）与输出 logits 对比解码（VCD）不仅无提升，甚至使性能下降，说明分离式方法存在信号冲突，而统一表示层级校准是更优路径。

**SVC 变体分析**（Table 5）：仅使用原始图像令牌（V_ori）或增强图像令牌（V_aug）均不及拼接后的 V_syn，验证了 Finding F2 的结论——原始与增强令牌提供互补语义，融合后可得到更聚焦的视觉上下文。TAM 可视化（Figure 7）进一步证实：针对 token “bulldog”，Vanilla LLaVA 注意力分散，V_ori 和 V_aug 各自聚焦不同区域，而 SVC 整合两者后形成精准聚焦。

**CRC 负采样策略**（Table 5）：隐空间令牌剪枝（信息缺口）产生的负样本显著优于像素级掩码（模态缺口），验证了 Finding F3——t-SNE 可视化（Figure 8）显示剪枝负样本聚类在原始图像表示附近，构成分布内探针；而掩码图像表示发散，属于分布外噪声扰动。

### 超参数分析

**CRC 负样本数 K**（Figure 9a）：性能在 K=3 时达到峰值，更多样本仅增加延迟而无明显收益，故选择 K=3 作为准确率-延迟的最佳权衡。

**SVC 与 CRC 强度**（Figure 9b）：热力图显示性能对 λ_s 和 λ_c 具有鲁棒性，最优热区位于 λ_s=0.06、λ_c=0.10 附近。

**保留视觉令牌数 N_h**（Figure 10）：当保留令牌数不少于 20 时，POPE 准确率基本稳定；降至 5 时准确率仅轻微下降，但能最大化信息缺口以有效隔离偏差，故选择 N_h=5。

### 失败模式与局限

1. **训练无关设置的边界**：该方法仅面向训练无关场景验证，未探索在微调或适配场景下与其他抗幻觉技术的兼容性。若下游任务需要模型内部表征的显著偏移，固定超参数的校准策略可能失效。

2. **超参数的手工依赖性**：关键超参数（Lc=16、λ_s=0.06、K=3、λ_c=0.10、N_h=5）需根据模型设计手工设定。虽然实验中固定参数在所有模型上取得最优，但不同模型的最优干预层和强度可能存在细微差异，自适应调参机制有待探索。

3. **负样本的随机性风险**：负样本由随机剪枝视觉令牌产生，虽为分布内探针，但在极少数特殊图像分布下可能引入变异性，影响校准稳定性。是否存在比随机剪枝更优的负样本构造方式（如基于注意力引导的剪枝）仍是开放问题。

4. **干预层的经验性选择**：当前固定 Lc=16 进行干预，但不同模型的最优层可能不同。该方法依赖于经验性选择，缺乏自适应的层级决策机制。

![[assets/figures/papers/paper_list_l2263_https_arxiv_org_abs_2603_10360/figures/006_Table_1.jpg]]
*Table 1: Evaluation results on POPE benchmark across four MLLMs. Results show averaged accuracy and F1 scores in % computed across random, popular, and adversarial object splits. Best and second best results are bolded and underlined, respectively*

![[assets/figures/papers/paper_list_l2263_https_arxiv_org_abs_2603_10360/figures/007_Table_2.jpg]]
*Table 2: CHAIR hallucination evaluation results. We compare our method to state-of-the-art training-free methods. Maximum new token is set to 64 and 128. Best and second best results are bolded and underlined, respectively*

![[assets/figures/papers/paper_list_l2263_https_arxiv_org_abs_2603_10360/figures/008_Table_3.jpg]]
*Table 3: Evaluation on MME benchmark (Perception and Cognition scores). Our method (Ours) consistently achieves state-ofthe-art performance across all tested models, demonstrating robust general capabilities*

![[assets/figures/papers/paper_list_l2263_https_arxiv_org_abs_2603_10360/figures/009_Table_4.jpg]]
*Table 4: Comparison of overhead among different methods (with best results bolded). Latency is measured in milliseconds per token. Throughput is calculated as tokens per millisecond. Memory cost is the peak GPU memory usage in megabytes*

![[assets/figures/papers/paper_list_l2263_https_arxiv_org_abs_2603_10360/figures/011_Table_5.jpg]]
*Table 5: Ablation study on LLaVA-1.5 (POPE benchmark in %) evaluating our SVC variants (visual context) and CRC variants (negative sampling strategy). Best results are bolded*

## 定位与知识库关联

### 核心瓶颈与设计动机

多模态大模型（MLLM）的幻觉问题根源于**视觉-语言系统性失衡**：随着自回归生成推进，视觉注意力逐渐衰减，而模型内部强大的语言先验占据主导，导致生成内容偏离视觉事实（Finding F1，Figure 2）。已有训练无关的缓解方法大致分为两条路径——**视觉注意力增强**与**文本解码矫正**——但二者在干预层级（中间层 vs. 输出 logits）和时域上存在根本性不一致。简单组合这两类方法（如 PAI + VCD）不仅无提升，甚至使性能下降（Figure 1），表明需要**统一的表示层级校准**。

本文的核心洞察在于：**视觉令牌具有双重潜力**——增强令牌提供互补视觉语义以抵御视觉衰退，剪枝令牌利用信息缺口生成稳定、分布内的幻觉探针，从而精确隔离并消除模型内部偏差。两者可在同一表示层级上协同工作，实现高效的训练无关幻觉抑制。

### 方法谱系与基线对比

本文所提**统一隐空间校准框架**（Unified Latent Calibration）包含两个协同模块：**Synergistic Visual Calibration（SVC）** 与 **Causal Representation Calibration（CRC）**。其与已有基线的关系如下：

**（1）与视觉注意力增强方法的对比**

- **PAI**（Liu et al., ECCV 2024）：通过提升视觉注意力权重缓解幻觉，但仅在单一层级操作，未提供偏差校准机制。本文的 SVC 模块虽同样增强视觉基础，但其通过拼接原始与经翻转、高斯模糊、椒盐噪声增强后的图像令牌形成协同视觉记忆库 $\mathbf{V}_{\mathrm{syn}}$，在中间层通过注意力注入（Eq. 3-5），实现了更丰富的互补视觉上下文构建（Finding F2，Figure 2）。消融实验表明，SVC 单独使用即优于 Vanilla 基线（Table 5）。

**（2）与输出端对比解码方法的对比**

- **VCD**（Leng et al., CVPR 2024）：基于输出 logits 的对比解码方法，通过抑制文本惯性来缓解幻觉。CRC 模块同样面向偏差抑制，但关键区别在于：CRC 在**浅层隐空间**构造分布内负样本（通过随机剪枝视觉令牌至剩余 5 个），计算稳定幻觉方向向量 $\mathbf{v}_{\mathrm{crc}}^{(l)}$ 并逐层消去（Eq. 6-11），而非在输出端进行 logits 校正。t-SNE 可视化证实，剪枝令牌产生的负样本聚类在原始图像表示附近，构成分布内探针；相比之下，像素级掩码（modality-gap）产生的负样本呈发散分布，属于不可靠的分布外扰动（Finding F3，Figure 8）。

**（3）与其他隐空间干预方法的对比**

- **VISTA**（Li et al., ICML）：视觉信息引导的解码偏置校准方法，但干预层级与机制与本文不同。本文统一在中间层 $L_c=16$ 完成 SVC 与 CRC，均在隐空间操作，无需解码。
- **ONLY**（Wan et al., arXiv 2025）：单层干预方法，在特定层调整隐状态以抑制幻觉。本文的 CRC 在 $1..L_c$ 层逐层净化隐状态，干预范围更广，且与 SVC 形成协同。

**（4）关键设计差异总结**

| 设计维度 | 已有方法 | 本文方法 |
|---------|---------|---------|
| 视觉上下文构建 | 仅使用原始图像令牌 | 拼接原始与增强令牌形成 $\mathbf{V}_{\mathrm{syn}}$，注意力注入 |
| 幻觉偏差探针 | 无探针或像素级掩码（不可靠） | 隐空间令牌剪枝，构造分布内负样本 |
| 干预层级与方式 | 注意力增强（层内）或 logits 矫正（输出端） | 统一在中间表示层 $L_c=16$ 完成，均在隐空间 |

### 适用边界与泛化性

**已验证的适用范围：**

- **模型架构**：在四种不同架构的 MLLM（LLaVA-1.5、Shikra、MiniGPT-4、InstructBLIP）上评估，覆盖线性投影和 Q-Former 两类视觉-语言对齐方式，验证了方法的泛化性（Table 1）。
- **评估基准**：在 POPE、CHAIR、MME、MMHal-Bench 四个基准上全面评估，覆盖判别式与生成式幻觉检测、通用能力评估等多个维度（Table 1-3，Figure 6）。
- **效率边界**：推理延迟仅增加 1.06 倍（Table 4），超参数 $K=3$ 是准确率-延迟的最佳权衡点（Figure 9a）。

**已知局限：**

1. **训练无关假设**：方法仅面向训练无关的设置，未验证在微调或适配场景下与其他抗幻觉技术的兼容性。
2. **超参数依赖**：关键超参数（$L_c=16$、$\lambda_s=0.06$、$K=3$、$\lambda_c=0.10$、$N_h=5$）需根据模型设计手工设定，自适应调参与统一最优参数仍有待探索。虽在固定参数下取得最优，但不同模型的最优参数可能存在细微差异。
3. **负样本稳定性**：负样本由随机剪枝产生，虽为分布内，但在极少数特殊图像分布下可能引入变异性，影响校准稳定性。
4. **干预层选择**：当前仅验证于固定层 $L_c=16$，不同模型的最优干预层可能不同，该方法依赖于经验性选择。

### 开放问题

1. **自适应剪枝与层选择**：如何根据输入实例自适应选择剪枝令牌数量与干预层，以最大化校准效果？
2. **跨模态扩展**：该统一隐空间校准框架是否能够扩展到视频、语音等其他模态的幻觉抑制？
3. **负样本构造的理论上限**：隐空间偏差消除的理论上限在何处？是否存在比随机剪枝更优的负样本构造方式？
4. **单次前向传播**：能否在单个前向传播中同时完成增强与校准，从而进一步降低延迟开销？

## 原文 PDF

![[paperPDFs/CVPR_2026/One_Token_Two_Fates_A_Unified_Framework_via_Vision_Token_Manipulation_Against_MLLMs_Hallucination.pdf]]
