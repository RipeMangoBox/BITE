---
title: "CausalLens: Sensitivity-Guided Multi-Head Causal Intervention for Hallucination Mitigation in Large Vision-Language Models"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/CausalLens_Sensitivity_Guided_Multi_Head_Causal_Intervention_for_Hallucination_Mitigation_in_Large_Vision_Language_Models.pdf
project_link: null
code_link: null
aliases:
- CausalLens
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: 中层（L10-L20）注意力头的视觉路径强度，具体通过视觉敏感性得分识别可靠的视觉注意力头，并在这些头的输出中增强视觉分量、抑制系统/文本分量。
primary_logic: 将注意力头分解为视觉、文本、系统三条因果路径，利用基于方差-均值比的视觉敏感性度量来定位携带空间选择性视觉信息的头，并通过自适应门控的混合因果干预与投影对齐残差校正，在保持语义空间一致性的前提下，重建视觉到输出标记的因果影响。
claims:
- 头部消融实验表明，移除高视觉敏感性头会导致准确率急剧下降（从0.8793降至0.5477），证明其对视觉推理的因果必要性。
- 注意力热力图显示，视觉注意力仅在前几层较强，中后期大部分头的注意力被系统提示占据（>60-80%）。
- 投影对齐残差校正能补偿多头部融合后的视觉信息稀释，进一步提升性能。
- POPE Random 上 Accuracy = 90.6
---

# CausalLens: Sensitivity-Guided Multi-Head Causal Intervention for Hallucination Mitigation in Large Vision-Language Models

> [!tip] 核心洞察
> 将注意力头分解为视觉、文本、系统三条因果路径，利用基于方差-均值比的视觉敏感性度量来定位携带空间选择性视觉信息的头，并通过自适应门控的混合因果干预与投影对齐残差校正，在保持语义空间一致性的前提下，重建视觉到输出标记的因果影响。

| 字段 | 内容 |
|------|------|
| 中文题名 | CausalLens：面向大视觉语言模型幻觉缓解的敏感性引导多头部因果干预 |
| 英文题名 | CausalLens: Sensitivity-Guided Multi-Head Causal Intervention for Hallucination Mitigation in Large Vision-Language Models |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://openaccess.thecvf.com/content/CVPR2026/html/Ji_CausalLens_Sensitivity-Guided_Multi-Head_Causal_Intervention_for_Hallucination_Mitigation_in_Large_CVPR_2026_paper.html) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/image_and_video_generation |
| Method | CausalLens |
| Dataset | POPE Random, CHAIR, MME Existence |

> [!tip] 效果简介
> - POPE Random 上，Accuracy 90.6 vs 87.93 (Regular from Fig.4) (+2.67)；F1-score 90.4 vs N/A (N/A)。
> - CHAIR (Max Token 64) 上，CHAIRs 18.7 vs N/A (N/A)；CHAIRi 6.2 vs N/A (N/A)。
> - MME Existence 上，Existence 195.00 vs N/A (N/A)。

## 概要

大视觉语言模型（LVLM）在自回归解码过程中存在一个核心瓶颈：视觉信息在模型的早期层之后迅速衰减，而系统提示与文本先验在中后期层逐渐占据主导地位。**Figure 2** 的注意力分布热力图清晰地展示了这一现象——在 LLaVA-v1.5-7B 中，图像令牌的注意力仅在 L0–L2 层较强，进入 L10–L30 层后，多数注意力头将超过 60%–80% 的注意力权重分配给系统提示令牌。这种注意力的结构性失衡导致视觉因果路径被系统性压缩，模型生成内容过度依赖语言先验，从而产生对象幻觉。

针对上述瓶颈，本文提出 **CausalLens**——一种无需训练的因果干预方法。其核心洞察在于：将 LVLM 解码器中每个注意力头的输出分解为**视觉路径**、**文本路径**与**系统路径**三条因果通道，利用基于方差-均值比的**视觉敏感性得分**（$s_{\ell,i} = \frac{\mathrm{Var}(A_{\ell,i}^{\mathcal{V}})}{\mathrm{Mean}(A_{\ell,i}^{\mathcal{V}}) + \epsilon}$）定位携带空间选择性视觉信息的可靠注意力头，并通过**自适应门控的混合因果干预**与**投影对齐残差校正**，在中层（L10–L20）重建视觉到输出令牌的因果影响。**Figure 5** 给出了方法的整体架构。

方法的因果必要性由头部消融实验提供有力支撑：如 **Figure 4** 所示，在 POPE 基准上移除前 5 个高敏感性头会导致准确率从 0.8793 急剧下降至 0.5477，而移除低敏感性头则几乎不影响性能，证明高视觉敏感性头是视觉推理的因果必要条件。

在实验验证方面，CausalLens 在三个 LVLM 模型（LLaVA-v1.5-7B、LLaVA-v1.5-13B、Qwen2-VL-7B）上展现出一致的幻觉缓解效果。在 POPE 基准上，准确率从 Regular 基线的 87.93 提升至 90.6；在 CHAIR 基准上，CHAIRs 降至 18.7，CHAIRi 降至 6.2；在 MME Existence 子集上达到 195.00。消融实验进一步证实，混合因果干预（HCI）与投影对齐残差校正（PRC）的联合使用是性能提升的关键，且视觉增强系数 $\lambda$ 在 0.15 时取得最优平衡。

作为对比解码（如 **VCD**, Leng et al., CVPR 2024）和生成反馈自校正（如 **DeGF**, Zhang et al., ICLR 2025）之外的第三条技术路径，CausalLens 的核心差异在于：它不依赖扰动输入或外部反馈，而是直接在模型内部通过注意力头的敏感性引导调制来恢复视觉因果链，在保持单次前向推理效率的同时实现幻觉缓解。



### LVLM幻觉问题的因果根源

大视觉语言模型（LVLM）在图像描述、视觉问答等任务中展现出强大能力，但普遍存在“幻觉”问题——生成的内容与视觉输入不一致，凭空编造物体、属性或关系。现有缓解幻觉的方法主要分为两类：**重训练**方法通过高质量数据微调模型以抑制幻觉，但计算成本高且可能损害模型的通用能力；**对比解码**方法（如**VCD**，Leng et al., CVPR 2024）通过对比原始输入与视觉扰动输入的输出差异来抑制语言先验，但需要两次前向传播，推理开销翻倍。

本文从一个被忽视的因果视角切入：LVLM自回归解码过程中，**视觉信息在早期层后快速衰减，系统提示与文本先验在中后期层占据主导**。Figure 2的注意力热力图定量揭示了这一瓶颈——在LLaVA-v1.5-7B中，图像令牌仅在L0–L2层获得较强的注意力权重，而在L10–L30的中高层，大部分注意力头将超过60–80%的注意力分配给系统提示令牌，视觉因果路径被系统性压缩。这种注意力失衡导致模型在生成过程中过度依赖语言先验，从而产生幻觉。

### 视觉注意力头的异质性

进一步观察发现，不同注意力头对视觉信息的处理方式存在显著异质性。Figure 3的定性可视化显示，部分注意力头能够精准定位语义相关的图像区域（如物体边界、关键属性），呈现出高度集中的空间选择性；而另一些头则表现出近乎均匀的注意力分布，缺乏有效的视觉定位能力。这一现象表明，并非所有注意力头在视觉推理中扮演同等角色——**只有部分“视觉可靠头”真正承载了从图像到输出的因果信息流**。

### 现有方法的缺口

上述两类主流方法均未直接针对这一因果瓶颈进行干预。重训练方法隐式地调整模型参数，但无法精确控制特定层和特定注意力头的视觉-语言平衡；对比解码方法通过外部扰动间接抑制语言先验，但干预粒度粗糙，无法区分不同注意力头的因果贡献差异。**VAF**（He et al., ACL 2025）虽然引入了视觉感知头的概念，但其基于头间发散性的度量缺乏对视觉注意力集中度的直接量化，且未考虑多头部融合投影对干预效果的稀释问题。

### 本文动机

基于以上分析，本文提出核心动机：**通过精确定位和增强LVLM中层注意力头中的视觉因果路径，可以在不重训练、不增加推理次数的情况下，有效缓解幻觉**。这需要解决三个关键问题：（1）如何量化每个注意力头的视觉可靠性？（2）如何在保持语义空间一致性的前提下增强视觉信号？（3）如何补偿多头部融合投影引入的视觉信息稀释？CausalLens通过视觉敏感性度量、混合因果干预和投影对齐残差校正三个模块系统性地回应了这些挑战。



## 核心方法与创新机理

CausalLens 的核心创新在于**将 LVLM 幻觉缓解从“外部对比解码”或“重训练”范式，转向了模型内部注意力头的因果路径干预**。其关键 changed slots 可归纳为三个层面：

### 1. 注意力头的因果路径分解与视觉敏感性定位

传统方法（如 **VCD** (Leng et al., CVPR 2024)、**DeGF** (Zhang et al., ICLR 2025)）在输出层或解码策略层面抑制语言先验，而 CausalLens 首次深入到 Transformer 解码器的**注意力头内部**，将每个头的输出分解为三条因果路径：

$$H_{\ell,i} = H_{\ell,i}^{(\mathrm{sys})} + H_{\ell,i}^{(\mathrm{text})} + H_{\ell,i}^{(\mathrm{vis})}$$

这一分解揭示了幻觉产生的瓶颈：Figure 2 显示，视觉注意力仅在早期层（L0–L2）较强，中后期层（L10–L30）大部分头的注意力被系统提示占据（>60–80%），视觉因果路径被严重压缩。CausalLens 的突破在于定义了**视觉敏感性得分**来量化每个头对视觉信息的承载能力：

$$s_{\ell,i} = \frac{\mathrm{Var}(A_{\ell,i}^{\mathcal{V}})}{\mathrm{Mean}(A_{\ell,i}^{\mathcal{V}}) + \epsilon}$$

该指标利用方差-均值比衡量注意力头在图像令牌上的关注集中度——高值表示高空间选择性和视觉因果性。Figure 3 的定性可视化证实，高敏感性头确实聚焦于语义相关区域，而低敏感性头呈现近乎均匀的注意力分布。Figure 4 的头部消融实验提供了决定性证据：移除 top-5 高敏感性头导致 POPE 准确率从 0.8793 骤降至 0.5477，而移除低敏感性头则性能不变（0.873–0.879），直接证明了这些头的因果必要性。

### 2. 中层混合因果干预 (HCI)

与 **VAF** (He et al., ACL 2025) 基于视觉感知头部发散性的方法不同，CausalLens 的干预**仅作用于中层选定层（L10–L20）**，且采用自适应门控机制动态平衡视觉增强强度。混合干预的核心公式为：

$$H_{\ell,i}^{*} = (1-\gamma)H_{\ell,i} + \gamma(T_{\ell,i} + \lambda \hat{s}_{\ell,i} D_{\ell,i})$$

其中，对比方向 $D_{\ell,i}$ 将头表示推向视觉接地、远离语言主导响应；归一化敏感性得分 $\hat{s}_{\ell,i}$ 确保只有可靠的视觉头被增强；自适应门控 $\gamma$ 根据系统提示与视觉分量的期望 L2 范数动态调整干预强度：

$$\gamma = \frac{\mathbb{E}\lVert H^{(\mathrm{sys})}\rVert^{2}}{\mathbb{E}\lVert H^{(\mathrm{sys})}\rVert^{2} + \mathbb{E}\lVert H^{(\mathrm{vis})}\rVert^{2} + \epsilon}$$

这一设计的关键创新在于**干预强度随输入动态变化**：当系统提示主导时 $\gamma$ 较大，增强视觉信号；当视觉信息已足够时 $\gamma$ 较小，保持原始表示，避免了固定强度干预可能引入的语义失真。

### 3. 投影对齐残差校正 (PRC)

多头部融合通过 $W_{\ell}^{O}$ 矩阵投影会稀释视觉增强效果，这是此前方法未触及的问题。CausalLens 在融合后添加了投影对齐残差：

$$\widetilde{H}_{\ell} = H_{\ell}^{\mathrm{fusion}} + \lambda \Delta_{\ell}^{\mathrm{proj}}$$

其中 $\Delta_{\ell}^{\mathrm{proj}}$ 由各头视觉-系统对比方向经 $W_{\ell}^{O}$ 投影后拼接而成，补偿了融合过程中的视觉信息损失。Table 5 的消融实验证实，HCI 与 PRC 联合使用（POPE 准确率 86.5，CHAIRi 6.2）显著优于单独使用 HCI，验证了该残差校正的必要性。

### 创新总结

| 干预维度 | Baseline 做法 | CausalLens 创新 |
|---------|-------------|---------------|
| 干预层级 | 输出层对比解码 / 重训练 | 注意力头内部因果路径 |
| 头选择机制 | 无 / 启发式选择 | 视觉敏感性得分引导的精确头定位 |
| 干预范围 | 全模型 / 全层 | 仅中层 L10–L20 |
| 干预强度 | 固定 / 无 | 自适应门控 $\gamma$ 动态平衡 |
| 融合后处理 | 无 | 投影对齐残差 $\Delta^{\mathrm{proj}}$ 补偿稀释 |

整个方法**无需训练**，在单次前向传播中完成干预（Algorithm 1），与需要多次前向的对比解码方法相比，在 GPU 内存和推理延迟上具有明显效率优势（Table 4）。



CausalLens 是一种训练无关（training-free）的因果干预方法，直接嵌入 LVLM 解码器内部，通过单次前向传播即可重建从视觉令牌到输出令牌的因果链路。其整体 pipeline 由四个核心模块串联构成，如图 Figure 5 所示。

![[assets/figures/papers/paper_list_l741_https_openaccess_thecvf_com_content_CVPR2026_html_Ji_CausalLens_Sensitiv/figures/005_Figure_5.jpg]]
*Figure 5: Overview of CausalLens. Our method introduces a training-free causal intervention inside the LVLM decoder. Each attention head is decomposed into system prompt, textual, and visual pathways. A hybrid intervention enhances visually reliable heads using a sensitivity-guided amplification, and a projection-aligned residual correction maintains semantic consistency after multi-head fusion. This single-pass procedure restores the causal chain from visual tokens to generated outputs*

**注意力头分解与路径划分**。对于解码器中每一层的每个注意力头，CausalLens 将注意力权重矩阵按令牌类型切分为三个不相交的子集：系统提示令牌集合 $\mathcal{S}$、图像令牌集合 $\mathcal{V}$ 和文本令牌集合 $\mathcal{T}$。基于此划分，每个注意力头的输出被分解为三条因果路径的贡献之和：

$$H_{\ell,i} = H_{\ell,i}^{(\mathrm{sys})} + H_{\ell,i}^{(\mathrm{text})} + H_{\ell,i}^{(\mathrm{vis})}$$

这一分解使得后续干预能够精确地作用于视觉路径，而无需修改系统提示或文本路径。

**视觉敏感性计算模块**。为了识别哪些注意力头真正携带空间选择性的视觉信息，CausalLens 定义了视觉敏感性得分：

$$s_{\ell,i} = \frac{\mathrm{Var}(A_{\ell,i}^{\mathcal{V}})}{\mathrm{Mean}(A_{\ell,i}^{\mathcal{V}}) + \epsilon}$$

该得分基于方差-均值比衡量注意力头在图像令牌上的注意力集中度：高得分意味着该头聚焦于特定图像区域（空间选择性高），低得分则表明注意力近乎均匀分布。层内归一化后的得分 $\hat{s}_{\ell,i}$ 用于跨头比较，指导后续干预的强度分配。

**混合因果干预（HCI）**。干预仅作用于中层选定层范围 $L_{\mathrm{mid}} = \{\ell_1, \dots, \ell_m\}$（通常为 L10–L20）。对于这些层中的每个注意力头，HCI 通过自适应门控 $\gamma$ 和视觉增强系数 $\lambda$ 调整头输出：

$$H_{\ell,i}^{*} = (1-\gamma)H_{\ell,i} + \gamma(T_{\ell,i} + \lambda \hat{s}_{\ell,i} D_{\ell,i})$$

其中 $D_{\ell,i} = H_{\ell,i}^{(\mathrm{vis})} - H_{\ell,i}^{(\mathrm{sys})}$ 是视觉-系统对比方向，用于将头表示推向视觉接地、远离语言主导的响应。自适应门控 $\gamma$ 根据系统提示分量与视觉分量的期望 L2 范数动态平衡干预强度，避免过度修正。

**投影对齐残差校正（PRC）**。多头部融合通过输出投影矩阵 $W_{\ell}^{O}$ 将各头输出聚合时，视觉增强信号可能被稀释。PRC 在融合后添加投影对齐残差以补偿这一损失：

$$\Delta_{\ell}^{\mathrm{proj}} = W_{\ell}^{O} \mathrm{Concat}\big(H_{\ell,1}^{(\mathrm{vis})} - H_{\ell,1}^{(\mathrm{sys})}, \ldots, H_{\ell,H}^{(\mathrm{vis})} - H_{\ell,H}^{(\mathrm{sys})}\big)$$

$$\widetilde{H}_{\ell} = H_{\ell}^{\mathrm{fusion}} + \lambda \Delta_{\ell}^{\mathrm{proj}}$$

该残差确保视觉-系统对比方向在经过 $W_{\ell}^{O}$ 投影后仍能有效作用于融合表示，在模型语义空间内维持干预效果。

**输入输出流**。给定输入图像 $v$、系统提示和文本上下文，CausalLens 在标准自回归解码的每一生成步执行：首先计算所有注意力头的注意力分布和路径分量，然后对中层头施加 HCI 得到修正头输出 $H_{\ell,i}^{*}$，经多头部融合后再通过 PRC 得到最终层表示 $\widetilde{H}_{\ell}$。该表示继续向上层传递，最终从顶层隐状态 $\mathcal{H}_t^L$ 经 softmax 预测下一个令牌。整个过程无需额外训练、无需修改模型权重，仅通过单次前向传播中的隐状态调制即可实现幻觉缓解。



CausalLens 的核心由四个顺序模块构成，它们共同实现在 LVLM 解码器内部对视觉因果路径的无训练干预。

### 注意力头分解与路径划分

对于目标层 ℓ 的第 i 个注意力头，首先计算标准的多头注意力：

$$A_{\ell,i} = \mathrm{softmax}\left(\frac{Q_{\ell,i} K_{\ell,i}^\top}{\sqrt{d_k}}\right)$$

然后按 token 类型将注意力矩阵划分为三个不相交的切片：

$$A_{\ell,i}^{\mathcal{X}} = A_{\ell,i}[:, \mathcal{X}], \quad \mathcal{X} \in \{\mathcal{S}, \mathcal{V}, \mathcal{T}\}$$

其中 $\mathcal{S}$ 为系统提示 token、$\mathcal{V}$ 为图像 token、$\mathcal{T}$ 为文本 token。对应的输出分量通过加权值向量得到：

$$H_{\ell,i} = H_{\ell,i}^{(\mathrm{sys})} + H_{\ell,i}^{(\mathrm{vis})} + H_{\ell,i}^{(\mathrm{text})}$$

这一分解将每个注意力头的隐藏状态显式拆分为系统、视觉、文本三条因果路径，为后续的路径级干预提供操作基础。

### 视觉敏感性计算模块

视觉敏感性得分用于量化注意力头对图像 token 的关注集中度。其定义为视觉注意力分布的方差与均值之比：

$$s_{\ell,i} = \frac{\mathrm{Var}(A_{\ell,i}^{\mathcal{V}})}{\mathrm{Mean}(A_{\ell,i}^{\mathcal{V}}) + \epsilon}$$

其中 $\epsilon$ 为防止除零的小常数。高 $s_{\ell,i}$ 值意味着该头的视觉注意力高度集中于少数图像 token，即具有高空间选择性和视觉因果性；低值则对应均匀、无信息的注意力分布（见 Figure 3 定性对比）。

![[assets/figures/papers/paper_list_l741_https_openaccess_thecvf_com_content_CVPR2026_html_Ji_CausalLens_Sensitiv/figures/003_Figure_3.jpg]]
*Figure 3: Qualitative visualization of head-level visual attention in LLaVA-v1.5-7B. Different attention heads exhibit distinct spatial patterns: some localize semantically relevant regions, while others show nearly uniform attention, motivating the definition of our visual sensitivity score*

为支持跨头比较，在层内进行归一化：

$$\hat{s}_{\ell,i} = \frac{s_{\ell,i}}{\frac{1}{H}\sum_{j=1}^{H} s_{\ell,j} + \epsilon}$$

归一化后的 $\hat{s}_{\ell,i}$ 作为该头视觉可靠性的权重，直接驱动后续的混合因果干预。

### 混合因果干预 (HCI)

HCI 在中层（默认 L10–L20）的每个注意力头输出上注入视觉增强。首先定义视觉-系统对比方向：

$$D_{\ell,i} = H_{\ell,i}^{(\mathrm{vis})} - H_{\ell,i}^{(\mathrm{sys})}$$

该方向将头部表示推向视觉锚定、远离语言先验主导的响应。自适应门控 $\gamma$ 根据系统与视觉分量的期望 L2 范数动态平衡干预强度：

$$\gamma = \frac{\mathbb{E}\lVert H^{(\mathrm{sys})}\rVert^2}{\mathbb{E}\lVert H^{(\mathrm{sys})}\rVert^2 + \mathbb{E}\lVert H^{(\mathrm{vis})}\rVert^2 + \epsilon}$$

最终的混合干预头输出为：

$$H_{\ell,i}^{*} = (1-\gamma)H_{\ell,i} + \gamma\big(T_{\ell,i} + \lambda \hat{s}_{\ell,i} D_{\ell,i}\big)$$

其中 $T_{\ell,i}$ 为文本分量，$\lambda$ 为视觉增强系数（默认 0.15）。$\hat{s}_{\ell,i}$ 对 $D_{\ell,i}$ 的加权确保只有视觉敏感性高的头被显著增强，低敏感性头的干预被自然抑制。

### 投影对齐残差校正 (PRC)

多头部融合通过输出投影矩阵 $W_{\ell}^{O}$ 完成：

$$H_{\ell}^{\mathrm{fusion}} = \mathrm{Concat}\big(H_{\ell,1}^{*}, \ldots, H_{\ell,H}^{*}\big) W_{\ell}^{O}$$

然而，$W_{\ell}^{O}$ 的线性投影会稀释各头独立注入的视觉信号。PRC 通过构造投影对齐残差来补偿这一损失：

$$\Delta_{\ell}^{\mathrm{proj}} = W_{\ell}^{O}\,\mathrm{Concat}\big(H_{\ell,1}^{(\mathrm{vis})} - H_{\ell,1}^{(\mathrm{sys})}, \ldots, H_{\ell,H}^{(\mathrm{vis})} - H_{\ell,H}^{(\mathrm{sys})}\big)$$

最终校正后的层表示为：

$$\widetilde{H}_{\ell} = H_{\ell}^{\mathrm{fusion}} + \lambda \Delta_{\ell}^{\mathrm{proj}}$$

该残差在 $W_{\ell}^{O}$ 的投影空间内重新注入视觉-系统对比信号，确保干预效果在模型语义空间中持续生效。消融实验（Table 5）表明，HCI 与 PRC 联合使用时 POPE 准确率提升至 86.5、CHAIRi 降至 6.2，验证了两者的互补性。

### 补充图表

![[assets/figures/papers/paper_list_l741_https_openaccess_thecvf_com_content_CVPR2026_html_Ji_CausalLens_Sensitiv/figures/002_Figure_2.jpg]]
*Figure 2: Layer–Head attention distribution for different token types in LLaVA-v1.5-7B. Each cell represents the average attention weight from the generated token to (a) image tokens and (b) system prompt tokens, across all layers*

![[assets/figures/papers/paper_list_l741_https_openaccess_thecvf_com_content_CVPR2026_html_Ji_CausalLens_Sensitiv/figures/004_Figure_4.jpg]]
*Figure 4: Top-k head ablation on POPE. Removing high-s heads (red) causes a steep drop in accuracy, whereas removing low-s heads (blue) leaves performance unchanged. This demonstrates that visually sensitive heads are causally necessary for grounded reasoning*



## 实验与关键发现

### 实验设置

CausalLens 在三种代表性大视觉语言模型上进行验证：**LLaVA-v1.5-7B**、**LLaVA-v1.5-13B** 和 **Qwen2-VL-7B**。评估覆盖五个基准数据集：POPE（含 MS-COCO、A-OKVQA、GQA 三个子集）、MMHAL-Bench、CHAIR、MME 和 LLaVA-Bench。干预仅作用于中层区域（L10–L20），视觉增强系数默认设为 λ = 0.15。推理效率测试在单张 NVIDIA L40 GPU 上完成。

### 主要结果

**POPE 基准。** CausalLens 在三种模型上均展现出显著的幻觉抑制能力。以 LLaVA-v1.5-7B 为例，在 POPE Random 设置下，CausalLens 达到 **90.6% Accuracy** 和 **90.4% F1-score**，相较于未干预的 Regular 基线（87.93%）提升 **+2.67 个百分点**（Table 1）。在更具挑战性的 Popular 和 Adversarial 设置下，该方法同样保持一致的性能优势。跨模型趋势表明，CausalLens 的干预效果在 7B 和 13B 规模上均稳健，说明该方法对模型容量不敏感。

**CHAIR 基准。** 在图像描述任务中，CausalLens 将幻觉指标显著压低：LLaVA-v1.5-7B 上 **CHAIRs 降至 18.7**，**CHAIRi 降至 6.2**（Table 2，Max Token 64）。CHAIRs 衡量句子级幻觉比例，CHAIRi 衡量物体级幻觉比例，两者同步下降表明干预在细粒度和粗粒度层面均有效抑制了虚构物体描述。

**MME 基准。** 在 MME Existence 子集上，CausalLens 取得 **195.00** 分（Table 3），验证了方法对物体存在性判断的改善能力。这一子集专门评估模型是否错误声称图像中不存在的物体，是衡量幻觉的硬指标。

**MMHAL-Bench。** 该基准将幻觉细分为八大类别（如物体属性、空间关系、计数等）。CausalLens 在 LLaVA-v1.5-7B 上的八类表现全面优于对比方法（Figure 6），尤其在“物体属性”和“空间关系”类别上提升显著，说明视觉路径增强对需要细粒度视觉对齐的场景特别有效。

**效率分析。** CausalLens 在单次前向传播中完成干预，无需额外推理轮次。在 LLaVA-v1.5-7B 上，平均推理延迟和峰值 GPU 内存与 Regular 解码相比仅有微小增加（Table 4），显著优于需要多次前向传播的对比解码方法（如 **VCD**，Leng et al., CVPR 2024）。

### 消融实验

**HCI 与 PRC 的联合作用。** 消融实验（Table 5）拆解了混合因果干预（HCI）和投影对齐残差校正（PRC）的各自贡献。仅使用 HCI 时，POPE Popular 准确率提升至约 85.2，CHAIRi 降至约 7.8；仅使用 PRC 时效果有限。二者联合使用时，准确率进一步提升至 **86.5**，CHAIRi 降至 **6.2**。这证实了 PRC 模块在补偿多头部融合后视觉信息稀释方面的关键作用——HCI 在单个头内增强视觉信号，但经过 $W_\ell^O$ 投影矩阵融合后，视觉分量可能被再次分散，PRC 通过添加视觉-系统对比方向的投影残差 $\Delta_\ell^{proj}$ 来维持干预效果在语义空间中的持续性。

**视觉增强系数 λ 的敏感性。** λ 控制视觉信号注入的强度。消融实验（Table 6）表明，λ = 0.15 在 POPE 和 CHAIR 上取得最佳平衡。λ 过低（如 0.05）时幻觉抑制不足，CHAIRi 偏高；λ 过高（如 0.25）时语义准确性开始下降，POPE 准确率回落。这一倒 U 型曲线说明，过度增强视觉路径可能导致模型忽略文本上下文中的合理约束，引入另一种形式的生成偏差。

**头部消融的因果证据。** 头部消融实验（Figure 4）提供了视觉敏感性头的因果必要性证明。在 POPE 基准上，移除 Top-1 高视觉敏感性头（高 s 值）导致准确率从 **0.8793 骤降至 0.7577**；移除 Top-5 时进一步跌至 **0.5477**，接近随机水平。相反，移除等量的低敏感性头（低 s 值）对性能无显著影响（准确率维持在 0.873–0.879）。这一单调递减趋势强有力地证明：视觉敏感性得分 $s_{\ell,i}$ 成功识别了对视觉落地推理不可或缺的注意力头，而 CausalLens 的干预正是作用于这些关键头上。

### 案例研究

LLaVA-Bench 上的案例对比（Figure 7）展示了 CausalLens 在实际场景中的行为变化。在需要精确视觉定位的描述任务中，Regular 解码倾向于生成图像中不存在或错误的细节（如虚构物体颜色、数量），而 CausalLens 的回答更忠实地反映图像内容。GPT-4V 辅助评估的得分也佐证了回答质量的提升。

![[assets/figures/papers/paper_list_l741_https_openaccess_thecvf_com_content_CVPR2026_html_Ji_CausalLens_Sensitiv/figures/009_Figure_7.jpg]]
*Figure 7: Case study on the LLaVA-Bench benchmark. We compare the responses generated by regular decoding and our method using LLaVA-v1.5-7B. GPT-4V-aided evaluation results are also provided alongside the responses*

### 失败模式与局限性

尽管整体效果显著，CausalLens 存在以下已知局限：

1. **中层范围的固定性。** 干预层范围默认设为 L10–L20，这一选择基于 LLaVA-v1.5-7B 上的注意力分布分析（Figure 2）。对于不同架构或规模的模型，视觉信息衰减的层位置可能偏移，固定范围可能导致次优干预。目前缺乏自动确定层范围的机制。

2. **λ 系数的手动设定。** λ = 0.15 为经验最优值，但未探索数据分布自适应的动态调整策略。在不同领域（如医学图像、遥感图像）或不同提示风格下，最优 λ 可能变化。

3. **低质量图像的鲁棒性。** 当输入图像本身模糊、遮挡严重或视觉信息匮乏时，增强视觉路径可能放大噪声而非改善幻觉。该场景下的安全边界尚未系统评估。

4. **架构覆盖有限。** 实验仅在三种开源 LVLM 上进行，未在闭源模型（如 GPT-4V、Gemini）或不同注意力机制的架构（如 InstructBLIP 的 Q-Former 结构）上验证泛化性。

5. **长上下文与多轮对话未覆盖。** 评估集中于单轮静态图像问答和描述，该方法在多轮对话中视觉因果路径的持续维护效果尚待检验。

### 补充图表

![[assets/figures/papers/paper_list_l741_https_openaccess_thecvf_com_content_CVPR2026_html_Ji_CausalLens_Sensitiv/figures/006_Table_1.jpg]]
*Table 1: Performance on POPE. Results are averaged across the MS-COCO, A-OKVQA, and GQA datasets. Our method demonstrates superior hallucination suppression across all three LVLMs. The best performance for each setting is highlighted*

![[assets/figures/papers/paper_list_l741_https_openaccess_thecvf_com_content_CVPR2026_html_Ji_CausalLens_Sensitiv/figures/008_Table_2.jpg]]
*Table 2: Results on CHAIR benchmark using LLaVA-v1.5-7B. Lower CHAIRS and CHAIRI indicate better performance*

![[assets/figures/papers/paper_list_l741_https_openaccess_thecvf_com_content_CVPR2026_html_Ji_CausalLens_Sensitiv/figures/010_Table_3.jpg]]
*Table 3: Results on the MME subset without total score*

![[assets/figures/papers/paper_list_l741_https_openaccess_thecvf_com_content_CVPR2026_html_Ji_CausalLens_Sensitiv/figures/007_Figure_6.jpg]]
*Figure 6: Comparing the performance of different methods on the LLaVA-v1.5-7B model across the eight categories of MMHAL-Bench*

![[assets/figures/papers/paper_list_l741_https_openaccess_thecvf_com_content_CVPR2026_html_Ji_CausalLens_Sensitiv/figures/012_Table_5.jpg]]
*Table 5: Ablation study of the Hybrid Causal Intervention (HCI) and Projection-aligned Residual Correction (PRC) in LLaVAv1.5-7B on the POPE (Popular) and CHAIR benchmarks (Max Token 64)*

![[assets/figures/papers/paper_list_l741_https_openaccess_thecvf_com_content_CVPR2026_html_Ji_CausalLens_Sensitiv/figures/013_Table_6.jpg]]
*Table 6: Ablation study of λ on the POPE (Popular) and CHAIR benchmarks (Max Token 64), using the LLaVA-v1.5-7B model*

![[assets/figures/papers/paper_list_l741_https_openaccess_thecvf_com_content_CVPR2026_html_Ji_CausalLens_Sensitiv/figures/011_Table_4.jpg]]
*Table 4: Efficiency comparison. For each method, we present the average inference latency per instance and peak GPU memory in LLaVA-v1.5-7B. Experiments are conducted on a single NVIDIA L40 GPU*



## 定位与知识库关联

### 1. 与现有幻觉缓解范式的对比

**CausalLens** 作为一种免训练的解码期干预方法，与当前主流的 LVLM 幻觉缓解策略形成了明确的区分。如图 1 所归纳，现有方法主要分为三类：重训练范式、对比解码范式，以及本文提出的隐藏状态调制范式。

**重训练范式**通过高质量数据微调模型来减少幻觉，但面临数据获取成本高、灾难性遗忘风险以及闭源模型不可访问等问题。**对比解码范式**以 **VCD**（Leng et al., CVPR 2024）和 **DeGF**（Zhang et al., ICLR 2025）为代表，通过构造视觉扰动输入作为负例，在输出概率空间中抑制语言先验。然而，这类方法需要对每个生成步骤进行至少两次前向传播，推理开销显著增加。

**CausalLens** 的关键区别在于，它将干预前置到注意力头的隐藏状态层面，而非输出概率空间。具体而言，该方法将每个注意力头的输出分解为视觉、文本、系统三条因果路径，通过视觉敏感性得分识别可靠视觉头，并在中层（L10–L20）对这些头的隐藏状态进行自适应增强。这一设计的核心优势是**单次前向传播**即可完成干预，无需额外的前向或反向传播，在效率上显著优于对比解码方法（见 Table 4 的推理延迟和 GPU 内存对比）。

与另一类隐藏状态干预方法 **VAF**（He et al., ACL 2025）相比，CausalLens 的差异在于：VAF 基于视觉感知头的发散性进行干预，而 CausalLens 引入了更精细的路径分解和敏感性引导机制，并通过投影对齐残差校正解决了多头部融合后的视觉信息稀释问题。

### 2. 方法谱系中的定位

从因果推断视角看，CausalLens 可被定位为**基于因果路径分析的隐藏状态干预方法**。其理论根基在于对 LVLM 自回归解码过程中因果链的诊断：视觉信息在早期层后快速衰减，系统提示与文本先验在中后期层占据主导，切断了从视觉标记到输出标记的因果路径。

该方法的核心创新可分解为三个递进的机制：

- **路径分解与敏感性度量**：将注意力头输出按标记类型（系统、文本、视觉）拆分为独立分量，并利用方差-均值比定义的视觉敏感性得分 $s_{\ell,i} = \frac{\mathrm{Var}(A_{\ell,i}^{\mathcal{V}})}{\mathrm{Mean}(A_{\ell,i}^{\mathcal{V}}) + \epsilon}$ 来量化每个头对视觉信息的空间选择能力。
- **混合因果干预（HCI）**：在中层注意力头上，利用敏感性得分 $\hat{s}_{\ell,i}$ 和自适应门控 $\gamma$ 对视觉分量进行加权增强，同时保留文本路径的语义信息，避免过度干预导致语言流畅性下降。
- **投影对齐残差校正（PRC）**：在多头部融合后添加视觉-系统对比方向的投影残差 $\Delta_{\ell}^{proj}$，补偿 $W_{\ell}^{O}$ 投影矩阵对视觉信号的稀释效应，确保干预效果在模型语义空间中持续生效。

从知识库定位来看，CausalLens 填补了**免训练、单次前向、隐藏状态级** LVLM 幻觉缓解方法的空白。它不依赖外部模型、额外数据或多次推理，适用于对推理效率敏感的部署场景。

### 3. 适用边界与关键假设

CausalLens 的有效性建立在以下假设之上：

1. **视觉信息存在于中层注意力头中**：方法假设中层（L10–L20）的某些注意力头仍携带可被增强的视觉信号。这一假设在 LLaVA-v1.5 和 Qwen2-VL 架构上得到了 Figure 2 和消融实验的支持，但对于注意力模式显著不同的架构（如交叉注意力为主的模型），需要进一步验证。

2. **视觉敏感性得分能可靠识别因果视觉头**：头部消融实验（Figure 4）提供了强因果证据——移除高敏感性头使准确率从 0.8793 骤降至 0.5477，而移除低敏感性头几乎不影响性能。然而，该实验仅在 POPE 基准上进行，在其他任务类型上的因果必要性尚未验证。

3. **视觉增强不会引入噪声**：当输入图像质量低或视觉信息本身不足时，增强视觉路径可能放大噪声而非改善幻觉。这是该方法的一个明确局限，原文也指出需要进一步评估。

### 4. 局限性与开放问题

**已识别的局限**：

- **超参数敏感性**：中层干预范围（L10–L20）和视觉增强系数 $\lambda$（0.15）需要手动设定。Table 6 显示 $\lambda$ 在 0.15 时取得最优，过高或过低都会导致性能下降，表明该参数对不同的模型配置和数据分布可能敏感。
- **模型覆盖范围有限**：实验仅在 LLaVA-v1.5-7B、LLaVA-v1.5-13B 和 Qwen2-VL-7B 三种模型上验证，未在 InstructBLIP、BLIP-2 等不同架构或 GPT-4V 等闭源模型上测试，泛化性有待进一步检验。
- **评估场景局限**：评估基准侧重于静态图像问答和描述（POPE、CHAIR、MME），未覆盖多轮对话、长上下文生成或具身 AI 等复杂场景下的幻觉缓解效果。

**开放问题**：

- **自适应层范围选择**：是否可以通过学习或启发式方法自动确定需要干预的层范围，而非固定为 L10–L20？这直接关系到方法在不同模型架构上的即插即用能力。
- **多模态扩展**：视觉敏感性得分的定义基于图像标记的注意力集中度，该度量是否适用于视频、3D 点云等多模态输入，尚需探索。
- **与训练方法的协同**：能否将 CausalLens 的干预思想与提示工程或微调方法结合，在训练和推理两个阶段协同提升 LVLM 的可信度？
- **实际部署的安全性**：在医疗图像描述、自动驾驶视觉问答等高风险应用中，该方法的幻觉缓解效果和安全边界尚未评估，需要在实际部署前进行充分的受控实验。



## 原文 PDF

![[paperPDFs/CVPR_2026/CausalLens_Sensitivity_Guided_Multi_Head_Causal_Intervention_for_Hallucination_Mitigation_in_Large_Vision_Language_Models.pdf]]
