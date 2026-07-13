---
title: "Hallucination Begins Where Saliency Drops"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/Hallucination_Begins_Where_Saliency_Drops.pdf
project_link: null
code_link: https://github.com/zhangbaijin/LVLMs-Saliency
openreview_forum_id: sjnErRHXf3
aliases:
- SGRSSLCRL
- HBWSD
tags:
- ICLR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/vision_models_multimodal
core_operator: "输出令牌相对于先前输出令牌的显著性（定义为注意力权重与其梯度的Hadamard乘积的绝对值），该值量化了先前输出对当前预测的因果影响强度。"
primary_logic: "通过将注意力权重与梯度信息融合（LVLMs-Saliency），可以捕获仅靠注意力图无法发现的“上下文失联”信号；在此基础上，推理阶段引入双重干预——(1) 显著性引导的拒绝采样（SGRS）动态过滤低显著性候选令牌，(2) 局部一致性增强（LocoRE）主动增强对最近输出令牌的注意力——能够有效阻断幻觉令牌的生成并维持序列连贯性。"
claims:
- "幻觉令牌的平均显著性远低于正确令牌，该现象在LLaVA-1.5、Qwen2-VL和InternVL三个模型上均稳定成立（Table 5）。"
- "降低令牌显著性会导致幻觉率单调上升，人工衰减正确令牌的显著性会使CHAIRS升高，验证了显著性降低是幻觉的直接原因（Table 6）。"
- "SGRS+LocoRE在CHAIRS基准上将LLaVA-1.5-7B的幻觉率从48.0降至35.6（-25.8%），在Qwen2-VL-7B上从25.0降至19.3（-22.8%），同时保持或提升其他基准性能（Table 1, Table 2）。"
- "CHAIR 上 CHAIRS (越低越好) = 35.6 (SGRS+LocoRE, LLaVA-1.5-7B)"
---

# Hallucination Begins Where Saliency Drops

> [!tip] 核心洞察
> 通过将注意力权重与梯度信息融合（LVLMs-Saliency），可以捕获仅靠注意力图无法发现的“上下文失联”信号；在此基础上，推理阶段引入双重干预——(1) 显著性引导的拒绝采样（SGRS）动态过滤低显著性候选令牌，(2) 局部一致性增强（LocoRE）主动增强对最近输出令牌的注意力——能够有效阻断幻觉令牌的生成并维持序列连贯性。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 当显著性下降时幻觉开始 |
| 英文题名 | Hallucination Begins Where Saliency Drops |
| 会议/期刊 | ICLR 2026 (Oral) |
| Links | [paper](https://openreview.net/forum?id=sjnErRHXf3) · [Code](https://github.com/zhangbaijin/LVLMs-Saliency) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/vision_models_multimodal |
| Method | Saliency-Guided Rejection Sampling (SGRS) + Local Coherence Reinforcement (LocoRE) |
| Dataset | CHAIR, POPE, MME, LLaVAW (综合能力) |

> [!tip] 效果简介
> - CHAIR 上，CHAIRS (越低越好) 为 35.6 (SGRS+LocoRE, LLaVA-1.5-7B)，对比 48.0 (LLaVA-1.5-7B)，变化 -12.4。
> - POPE 上，F1 (越高越好) 为 87.0 (SGRS+LocoRE, LLaVA-1.5-7B)，对比 85.4 (LLaVA-1.5-7B)，变化 +1.6。
> - MME 上，总分 (越高越好) 为 668.33 (SGRS+LocoRE, LLaVA-1.5-7B)，对比 565.34 (Beam Search, LLaVA-1.5-7B)，变化 +103.0。

## 概要

大型视觉语言模型（LVLMs）在图像描述和视觉问答等任务中取得了显著进展，但在自回归生成过程中频繁产生与图像内容不一致的“幻觉”内容，严重制约了其可靠性。本文的核心发现是：**幻觉开始于输出令牌对先前已生成令牌的显著性（contextual grounding）崩溃之时**。具体而言，在自回归解码过程中，当前令牌对近期输出令牌的因果影响强度——即显著性——若显著下降，意味着模型“遗忘”了刚刚生成的内容，从而脱离上下文约束，产生幻觉。

为量化这一现象，本文提出 **LVLMs-Saliency**，一种融合注意力权重与其梯度的诊断工具。与仅依赖注意力图的方法不同，LVLMs-Saliency 通过计算注意力权重与梯度的 Hadamard 乘积的绝对值，能够捕获注意力图无法揭示的“上下文失联”信号。实验证据表明：在 LLaVA-1.5、Qwen2-VL 和 InternVL 三个模型上，幻觉令牌的平均显著性系统性地低于正确令牌（Table 5）；人为衰减正确令牌的显著性会单调推高幻觉率，直接验证了显著性降低是幻觉的因果驱动因素（Table 6）。

基于这一洞察，本文在推理阶段引入双重干预机制——**显著性引导的拒绝采样（SGRS）**与**局部一致性增强（LocoRE）**——无需修改模型参数即可有效阻断幻觉令牌的生成。SGRS 在每一步解码时评估候选令牌的显著性得分，拒绝低于自适应阈值的令牌，强制模型重采样至选出上下文接地的令牌；LocoRE 则在令牌被接受后，对距离当前预测位置 $w_s$ 以内的输出令牌施加距离加权增益 $\gamma_j^{(P)} = 1 + \beta \cdot \mathbb{I}((P-j) \leq w_s)$，增强下一步注意力权重中对近期输出的依赖，防止上下文遗忘。

在主要基准上的结果表明：SGRS+LocoRE 将 LLaVA-1.5-7B 的 CHAIRS 幻觉率从 48.0 降至 35.6（降幅 25.8%），将 Qwen2-VL-7B 从 25.0 降至 19.3（降幅 22.8%），同时在 POPE、MME 和 LLaVAW 等综合能力基准上保持或提升性能（Table 1, Table 2）。该方法属于推理阶段解码干预范式，与 OPERA（Huang et al., CVPR 2024）、VCD（Leng et al., CVPR 2024）等方法同属一路，但其独特之处在于引入梯度信息构建显著性度量，并通过拒绝采样与注意力增强的双重机制直接针对上下文断裂这一根本原因。

### 问题背景：大视觉语言模型的幻觉困境

大视觉语言模型（LVLMs）在图像描述、视觉问答等任务中取得了显著进展，但一个核心缺陷始终困扰着它们的可靠性——**幻觉**（hallucination）。模型常常生成与图像内容不一致的描述，凭空捏造物体、颜色或关系。现有的幻觉缓解策略大致分为三类：（1）修改解码过程，如 **OPERA**（Huang et al., CVPR 2024）通过注意力图锚点引导解码、**VCD**（Leng et al., CVPR 2024）采用对比解码；（2）调整序列结束符（EOS）的 logit 以控制生成终止；（3）干预特定注意力头，如 **EAH**（Zhang et al., EMNLP 2025）替换注意力头以缓解视觉注意力沉降、**TAME**（Tang et al., ICLR 2025）动态调整锚点令牌。然而，这些方法大多依赖启发式规则或静态阈值，缺乏对幻觉生成机制的深层理解，导致在不同模型和场景下效果不稳定。

### 现有方法的缺口：注意力图的诊断盲区

现有解码修改方法普遍依赖**原始注意力图**作为诊断信号。但注意力图存在一个根本性的盲区：如 Figure 1 所示，在 Qwen2-VL-7B 中，生成正确令牌（wallpaper）与幻觉令牌（blue）时的注意力图在视觉上几乎无法区分——两者都没有展现出明显的模式差异。这意味着仅凭注意力权重本身，模型无法可靠地判断当前输出是否与先前上下文保持接地的连接。这构成了一个关键瓶颈：**缺乏一种能够灵敏捕捉“上下文失联”信号的诊断工具**，使得幻觉在生成过程中悄然发生而未被及时阻断。

### 核心洞察：显著性崩溃先于幻觉

本研究提出了一个全新的诊断指标——**LVLMs-Saliency**，定义为注意力权重与其梯度的 Hadamard 乘积的绝对值：

$$\mathbf{S}^{(l,h)} = \operatorname{tril}\left( |\mathbf{A}^{(l,h)} \odot \nabla \mathbf{A}^{(l,h)}| \right)$$

这一融合策略的优越性在于：梯度信息揭示了注意力权重对模型输出的**因果影响强度**，而纯注意力图仅反映相关性。Figure 9 的对比实验证实，加法、取最大值、拼接后经 MLP 等替代融合策略均无法区分正常令牌与幻觉令牌，唯有注意力×梯度融合能清晰揭示两者差异。

通过 LVLMs-Saliency，本文发现了一个稳定且可操作的规律：**幻觉令牌的平均显著性远低于正确令牌**。Figure 10(a) 和 Table 5 的统计数据显示，这一现象在 LLaVA-1.5、Qwen2-VL 和 InternVL 三个不同架构的模型上均稳定成立。Figure 2 进一步揭示了时序模式：正确令牌对近期输出赋予高显著性，随距离衰减；而幻觉令牌对所有先前输出的显著性全面崩溃——这标志着**上下文记忆的断裂**。

### 因果验证与动机确立

显著性降低是幻觉的伴随现象还是直接原因？Table 6 的干预实验给出了明确的因果证据：人为将正确令牌的显著性乘以衰减因子 $r < 1$ 后，幻觉率单调上升——当 $r = 0.2$ 时，CHAIRS 从基线 48.0 飙升至 56.0。这直接验证了**显著性降低是导致幻觉的因果杠杆**，而非仅仅是副现象。

基于这一洞察，本文的动机自然浮现：既然低显著性预示并导致幻觉，那么**在推理阶段主动监控并强化输出令牌的显著性**，就能在幻觉发生前将其阻断。这引出了两个互补的干预策略——显著性引导的拒绝采样（SGRS）过滤低显著性候选令牌，以及局部一致性增强（LocoRE）主动修复上下文依赖——从而在不修改模型参数的前提下，实现即插即用的幻觉抑制。

## 核心方法与创新机理

本工作的核心创新在于**首次揭示并量化了输出令牌对先前输出上下文的显著性崩溃是幻觉的直接前兆**，并基于这一因果发现设计了推理阶段的**双重干预机制**，从令牌选择和注意力增强两个环节阻断幻觉生成。

### 瓶颈发现：显著性崩溃先于幻觉

传统方法依赖注意力图检测幻觉，但注意力图在正确令牌与幻觉令牌之间往往缺乏可区分的模式（Figure 1）。本工作提出的**LVLMs-Saliency**诊断工具将注意力权重与其梯度进行Hadamard乘积取绝对值，得到单头显著性矩阵：

$$\mathbf{S}^{(l,h)} = \operatorname{tril}\left( |\mathbf{A}^{(l,h)} \odot \nabla \mathbf{A}^{(l,h)}| \right)$$

这一融合梯度信息的设计使其能够捕获注意力图无法反映的“上下文失联”信号。跨LLaVA-1.5、Qwen2-VL和InternVL三个模型的统计分析（Table 5, Figure 10a）一致表明：**幻觉令牌的平均显著性远低于正确令牌**。更关键的因果证据来自显著性干预实验（Table 6）：人为将正确令牌的显著性乘以衰减因子 $r<1$ 后，CHAIRS幻觉率单调上升（$r=0.2$ 时升至56.0），直接验证了显著性降低是幻觉的因果驱动因素。

### 关键创新点一：显著性引导的拒绝采样（SGRS）

与标准自回归解码（如top-k/top-p采样）不同，SGRS在每一步解码时计算每个候选令牌 $c_i$ 相对于先前输出令牌的显著性得分：

$$\mathcal{S}(c_i) = \frac{1}{|\mathcal{L}_{\text{target}}| \cdot |\mathcal{T}|} \sum_{l \in \mathcal{L}_{\text{target}}} \sum_{j \in \mathcal{T}} \bar{\mathbf{S}}_{P,j}^{(l)}$$

并基于最近 $W$ 个已生成令牌的平均显著性动态计算自适应接受阈值：

$$\tau^{(P)} = \alpha \cdot \frac{1}{|\mathcal{H}|} \sum_{j \in \mathcal{H}} S(x_j)$$

低于该阈值的候选令牌被拒绝，强制模型重采样至选出上下文接地的令牌。这一机制将显著性从诊断信号转化为**可操作的令牌级过滤条件**，直接阻断低显著性（即高幻觉风险）令牌的输出。

### 关键创新点二：局部一致性增强（LocoRE）

标准的因果自注意力对输出令牌间依赖无额外增强，导致模型在长序列生成中逐渐“遗忘”近期输出。LocoRE在令牌被接受后，对距离当前预测位置 $w_s$ 以内的输出令牌施加距离加权增益：

$$\gamma_j^{(P)} = 1 + \beta \cdot \mathbb{I}\left((P-j) \leq w_s\right)$$

并将下一步前向传播的注意力权重按此增益缩放：

$$\mathbf{A}^{(P+1)}[b,h,P+1,j] \leftarrow \mathbf{A}^{(P+1)}[b,h,P+1,j] \cdot \gamma_j^{(P)}$$

这一轻量级即插即用模块**主动增强对最近输出令牌的注意力依赖**，从根源上对抗显著性衰减，维持序列连贯性。Figure 3 直观展示了LocoRE如何将同一位置从生成错误令牌（“clock”）恢复为正确令牌（“watch”），并伴随着显著性得分的大幅回升。

### 方法谱系定位

在现有解码修改方法中，**OPERA**（Huang et al., CVPR 2024）依赖注意力图锚点，**VCD**（Leng et al., CVPR 2024）采用对比解码，**DOPRA**（Wei & Zhang, MM 2024）惩罚锚点令牌，**TAME**（Tang et al., ICLR 2025）动态调整注意力局部化程度——这些方法均未直接建模输出令牌间的上下文接地强度。**EAH**（Zhang et al., EMNLP 2025）和**Vissink**（Kang et al., ICLR 2025）干预视觉注意力沉降，但未处理文本上下文漂移。本工作的独特贡献在于：**用梯度增强的显著性度量替代纯注意力图作为诊断信号，并将诊断与干预闭环——SGRS在令牌选择阶段过滤低显著性候选，LocoRE在注意力计算阶段强化局部上下文依赖，二者协同覆盖了幻觉生成的令牌级和序列级两个层面**。

本工作提出了一套推理阶段的双重干预框架，用于缓解大型视觉语言模型（LVLMs）在自回归生成中的幻觉问题。框架的核心逻辑链为：**诊断→过滤→增强**。

**诊断模块（LVLMs-Saliency）** 是整个框架的感知基础。它在每一步解码时计算当前候选令牌相对于先前已生成输出令牌的显著性，定义为注意力权重与其梯度的Hadamard乘积的绝对值：

$$\mathbf{S}^{(l,h)} = \operatorname{tril}\left( |\mathbf{A}^{(l,h)} \odot \nabla \mathbf{A}^{(l,h)}| \right)$$

该值量化了先前输出对当前预测的因果影响强度。与仅依赖注意力图的方法不同，LVLMs-Saliency通过融合梯度信息，能够捕获注意力图无法揭示的“上下文失联”信号——当模型即将生成幻觉令牌时，其对近期输出令牌的显著性会系统性崩溃（见Figure 1、Figure 2）。

**SGRS过滤器（Saliency-Guided Rejection Sampling）** 利用上述诊断信号进行令牌级干预。在每一步解码时，SGRS评估所有候选令牌的显著性得分 $\mathcal{S}(c_i)$，并与基于近期输出历史的自适应阈值 $\tau^{(P)}$ 进行比较：

$$\tau^{(P)} = \alpha \cdot \frac{1}{|\mathcal{H}|} \sum_{j \in \mathcal{H}} S(x_j)$$

显著性低于阈值的候选令牌被拒绝，强制模型重新采样，直至选出上下文接地的令牌。若所有候选均被拒绝，则回退到选择显著性最高的令牌。该机制直接操作化了核心发现：低显著性先于幻觉发生。

**LocoRE增强器（Local Coherence Reinforcement）** 在令牌被接受后介入，作用于下一步前向传播的注意力权重。它对距离当前预测位置 $w_s$ 以内的先前输出令牌施加距离加权增益：

$$\gamma_j^{(P)} = 1 + \beta \cdot \mathbb{I}\left((P-j) \leq w_s\right)$$

$$\mathbf{A}^{(P+1)}[b,h,P+1,j] \leftarrow \mathbf{A}^{(P+1)}[b,h,P+1,j] \cdot \gamma_j^{(P)}$$

该操作主动增强模型对最近输出上下文的依赖，直接对抗自回归生成中的“上下文遗忘”趋势，维持序列连贯性。

**整体流程**为：输入图像与提示 → 模型前向传播 → LVLMs-Saliency计算候选令牌显著性 → SGRS过滤低显著性令牌 → 选定令牌输出 → LocoRE修改下一步注意力权重 → 循环至生成结束。两个模块均作为即插即用的推理阶段干预，不修改模型参数，无需额外训练。

### 1. LVLMs-Saliency 诊断模块

该模块是方法的核心诊断工具，用于量化每个输出令牌对先前已生成令牌的“上下文接地强度”。其关键创新在于将注意力权重与其梯度进行融合，从而捕获仅靠注意力图无法发现的“上下文失联”信号。

对于单层单头，显著性矩阵定义为注意力权重与其梯度的 Hadamard 乘积的绝对值，并保留下三角因果结构：

$$
\mathbf{S}^{(l,h)} = \operatorname{tril}\left( |\mathbf{A}^{(l,h)} \odot \nabla \mathbf{A}^{(l,h)}| \right)
$$

其中 $\mathbf{A}^{(l,h)}$ 为第 $l$ 层第 $h$ 个注意力头的权重矩阵，$\nabla \mathbf{A}^{(l,h)}$ 为其梯度。随后对一层内所有头求和并进行 L2 归一化：

$$
\bar{\mathbf{S}}^{(l)} = \frac{\sum_{h=1}^{H} \mathbf{S}^{(l,h)}}{\|\sum_{h=1}^{H} \mathbf{S}^{(l,h)}\|_2}
$$

该模块的动机源于一个关键发现：当模型生成正确令牌时，当前输出对近期输出令牌的显著性较高且随距离衰减；而当生成幻觉令牌时，对所有先前输出的显著性整体崩溃（Figure 2）。这一现象在 LLaVA-1.5、Qwen2-VL 和 InternVL 三个模型上均稳定成立（Table 5），且人工衰减正确令牌的显著性会系统性增加幻觉率（Table 6），验证了显著性降低是幻觉的直接原因。

### 2. SGRS 过滤器（Saliency-Guided Rejection Sampling）

SGRS 在推理的每一步解码时评估候选令牌的显著性，拒绝低显著性候选，强制模型重采样直至选出上下文接地的令牌。

**候选令牌显著性得分**：在目标层集合 $\mathcal{L}_{\text{target}}$ 上，对当前候选令牌 $c_i$（对应位置 $P$）相对于所有先前输出位置 $j \in \mathcal{T}$ 的标准化显著性取平均：

$$
\mathcal{S}(c_i) = \frac{1}{|\mathcal{L}_{\text{target}}| \cdot |\mathcal{T}|} \sum_{l \in \mathcal{L}_{\text{target}}} \sum_{j \in \mathcal{T}} \bar{\mathbf{S}}_{P,j}^{(l)}
$$

**自适应接受阈值**：基于最近 $W$ 个已生成令牌的平均显著性，乘以缩放因子 $\alpha$：

$$
\tau^{(P)} = \alpha \cdot \frac{1}{|\mathcal{H}|} \sum_{j \in \mathcal{H}} S(x_j)
$$

其中 $\mathcal{H}$ 为最近 $W$ 个输出令牌的集合。候选令牌 $c_i$ 仅当 $\mathcal{S}(c_i) \geq \tau^{(P)}$ 时被接受；若所有候选均被拒绝，则回退到选择显著性最高的令牌。消融实验表明 $\alpha = 0.6$ 时幻觉率与延迟取得最佳平衡（Figure 4, Table 3）。

### 3. LocoRE 注意力增强器（Local Coherence Reinforcement）

LocoRE 在令牌被接受后，修改下一步前向传播的注意力权重，增强对最近输出令牌的依赖，防止上下文遗忘。

**距离加权增益**：对距离当前预测位置 $P$ 在局部窗口 $w_s$ 以内的输出令牌 $j$，施加增益 $1 + \beta$，否则为 1：

$$
\gamma_j^{(P)} = 1 + \beta \cdot \mathbb{I}\left((P-j) \leq w_s\right)
$$

**注意力权重更新**：将下一步预测的注意力权重中指向最近输出令牌的部分按增益缩放：

$$
\mathbf{A}^{(P+1)}[b,h,P+1,j] \leftarrow \mathbf{A}^{(P+1)}[b,h,P+1,j] \cdot \gamma_j^{(P)}
$$

其中 $b$ 为批次索引，$h$ 为头索引，$P+1$ 为下一步待预测位置。该操作直接增强了模型对近期上下文的依赖，对抗显著性衰减。消融实验中 $\beta$ 取值 0.15（LLaVA-1.5）和 0.20（Qwen2-VL）时效果最佳（Table 3）。

### 4. 模块协同

SGRS 与 LocoRE 形成双重干预机制：SGRS 在令牌选择阶段过滤上下文接地的候选，LocoRE 在注意力计算阶段主动强化对近期输出的依赖。两者互补——SGRS 直接抑制幻觉令牌的生成，LocoRE 维护序列连贯性。在 LLaVA-1.5-7B 上，SGRS+LocoRE 将 CHAIRS 从 48.0 降至 35.6（-25.8%），在 Qwen2-VL-7B 上从 25.0 降至 19.3（-22.8%）（Table 1, Table 2）。

## 实验与关键发现

### 核心发现：显著性降低是幻觉的直接前兆

本文的核心因果假说——输出令牌对先前输出令牌的显著性（contextual grounding）下降直接导致幻觉——通过三个层次的实验得到验证。

**第一层：统计差异。** 在LLaVA-1.5、Qwen2-VL和InternVL三个模型上，幻觉令牌的平均显著性均显著低于正确令牌（Table 5；Figure 10(a)）。这一跨模型的一致性表明，显著性崩溃是幻觉生成的稳定信号，而非特定模型的偶然现象。

![[assets/figures/papers/paper_list_l21_https_openreview_net_forum_id_sjnErRHXf3/figures/015_Table_5.jpg]]
*Table 5: Mean saliency scores for correct vs. hallucinated tokens across models*

**第二层：因果干预。** 人为将正确令牌的显著性乘以衰减因子r<1，幻觉率随r降低而单调上升：当r=0.2时，CHAIRS从基准的48.0升至56.0（Table 6）。这直接证明了显著性降低是幻觉的充分条件，而非仅仅是伴随现象。

![[assets/figures/papers/paper_list_l21_https_openreview_net_forum_id_sjnErRHXf3/figures/016_Table_6.jpg]]
*Table 6: Hallucination experiments that artificially lower saliency scores*

**第三层：反向验证。** 应用LocoRE强化上下文注意力后，同一位置原本生成错误令牌（如“clock”）变为正确令牌（如“watch”），且显著性图从崩溃恢复为高显著性模式（Figure 3），说明恢复上下文接地可以阻断幻觉。

### 主要结果：跨基准、跨模型的幻觉抑制

**幻觉基准表现。** 在CHAIR基准上，SGRS+LocoRE将LLaVA-1.5-7B的CHAIRS从48.0降至35.6（-25.8%），Qwen2-VL-7B从25.0降至19.3（-22.8%）（Table 1）。在POPE基准上，LLaVA-1.5-7B的F1从85.4提升至87.0（Table 1）。值得注意的是，仅使用LocoRE（无SGRS）即可在CHAIRS上取得38.4的显著改善，说明上下文连贯性增强本身就能有效抑制幻觉。

![[assets/figures/papers/paper_list_l21_https_openreview_net_forum_id_sjnErRHXf3/figures/003_Table_1.jpg]]
*Table 1: Compare results of LocoRE with other SOTA methods on POPE, CHAIR and MME datasets. The best performances within each setting are bolded, baseline: LLaVA-1.5-7B*

**综合能力保持。** 方法在抑制幻觉的同时未损害综合能力：LLaVA-1.5-7B的LLaVAW准确率从72.5提升至76.7，MME总分从565.34提升至668.33（Table 1, Table 2）。这表明SGRS+LocoRE并非通过牺牲生成多样性或信息量来换取低幻觉率，而是精准地修复了上下文失联问题。

![[assets/figures/papers/paper_list_l21_https_openreview_net_forum_id_sjnErRHXf3/figures/004_Table_2.jpg]]
*Table 2: Comparison of different LVLMs and LocoRE across all image benchmarks. Notably, in the Hallucination Benchmark, lower scores on CHAIRI and CHAIRS indicate better performance, while higher scores are preferable for other metrics*

**跨模型兼容性。** Table 2展示了方法在LLaVA-1.5-7B/13B、Qwen2-VL-7B和InternVL-7B上的表现，幻觉指标均获改善，且综合基准未出现系统性退化，验证了方法的架构无关性。

**与SOTA方法的对比。** 在CHAIR指标上，SGRS+LocoRE优于OPERA（Huang et al., CVPR 2024）、VCD（Leng et al., CVPR 2024）、DOPRA（Wei & Zhang, MM 2024）、EAH（Zhang et al., EMNLP 2025）、TAME（Tang et al., ICLR 2025）和Vissink（Kang et al., ICLR 2025）等解码修改方法（Table 1, Table 2）。作者指出，相比EAH直接替换注意力头的方式，LocoRE不改变模型内部表示，因此保持了更高的生成召回率。

### 消融实验：双组件的贡献与参数敏感性

**SGRS的α参数。** α控制过滤严格度：α=0.6时幻觉率与延迟取得最佳平衡；α升至0.9时延迟增加33%（从30.8 ms/token升至41.2 ms/token），但幻觉率改善边际（Figure 4；Table 3）。这表明过度严格的显著性过滤会导致频繁重采样，收益递减。

![[assets/figures/papers/paper_list_l21_https_openreview_net_forum_id_sjnErRHXf3/figures/007_Table_3.jpg]]
*Table 3: Ablation study on α (SGRS) and β (LocoRE). Best in bold. β: 0.15 (LLaVA-1.5), 0.20 (Qwen2-VL)*

**LocoRE的β参数。** β在LLaVA-1.5上最佳值为0.15，在Qwen2-VL上为0.20（Table 3）。仅使用LocoRE即可显著降低幻觉率，验证了增强局部上下文依赖的有效性。当β=0时，LocoRE退化为无干预基线，幻觉率回升，确认了增益机制的必要性。

**组件组合效应。** SGRS+LocoRE的组合优于任一单独组件，说明令牌级过滤与序列级连贯增强具有互补性：SGRS在单步决策中阻断低显著性令牌，LocoRE在序列层面防止上下文遗忘的累积。

### 失败模式与局限性

**高显著性幻觉。** 当模型对错误答案具有极高置信度时，幻觉令牌的显著性可能并不低，此时低显著性假设失效，SGRS无法识别此类错误。这是方法的核心盲区——它只能捕获因上下文失联导致的幻觉，无法处理模型“自信出错”的情况。

**上下文无关生成。** 当输入提示本身模糊或信息不足时，合理的输出可能天然具有低显著性（因为缺乏足够的上下文支撑），SGRS可能错误拒绝这些令牌，导致生成质量下降。

**计算开销。** SGRS需要在推理时计算梯度并存储中间激活，导致约30-40%的延迟增加，且目前无法部署在72B及以上参数的大模型上。这是梯度依赖方法的固有瓶颈，限制了其在实际部署中的可扩展性。

**视频基准表现。** Table 4展示了方法在视频LVLM上的扩展实验，但视频领域的幻觉抑制效果和失败模式需要进一步验证（此部分证据来自论文Table 4，需结合原文确认具体数值和结论）。

![[assets/figures/papers/paper_list_l21_https_openreview_net_forum_id_sjnErRHXf3/figures/012_Table_4.jpg]]
*Table 4: Comparison of different Video LVLMs and LocoRE across all video benchmarks. In the Video-Based Text Generation Benchmark, five scores are assessed: Cr. (Correctness of Information), Cs. (Consistency), De. (Detail Orientation), Ct. (Contextual Understanding) and Te. (Temporal Understanding). Following Maaz et al Maaz et al. (2023), we use the GPT-3.5 Turbo model to assign a relative score to the model outputs, with scores ranging from 0 to 5*

### 关键图表结论摘要

| 图表 | 核心结论 |
|------|---------|
| Figure 1 | 注意力图无法区分正确与幻觉令牌，而LVLMs-Saliency图呈现显著差异：正确令牌具有强结构化接地，幻觉令牌显著性崩溃 |
| Figure 2 | 正确令牌对近期输出保持高显著性（随距离衰减），幻觉令牌对所有先前输出的显著性全面崩溃 |
| Figure 3 | LocoRE可将低显著性幻觉位置恢复为高显著性正确令牌，直接展示上下文连贯增强的因果效应 |
| Figure 4 | α=0.6为SGRS的最佳效率-效果平衡点，过高α导致延迟激增而收益边际 |
| Table 5 | 三模型上正确与幻觉令牌的平均显著性差异稳定存在，跨模型验证显著性作为幻觉信号的可靠性 |
| Table 6 | 人工降低显著性导致幻觉率单调上升，建立显著性降低→幻觉的因果链 |

## 定位与知识库关联

### 核心洞察：从注意力到显著性的范式迁移

本工作的根本贡献在于提出**LVLMs-Saliency**——一种将注意力权重与其梯度进行Hadamard乘积的梯度感知诊断工具。该指标揭示了仅靠注意力图无法捕获的关键信号：在自回归生成中，当前输出令牌对先前输出令牌的**显著性（contextual grounding）崩溃**是幻觉的直接前兆。这一发现将幻觉检测从传统的“注意力图模式识别”范式推进到“因果影响量化”范式。

### 与现有解码修改方法的对比

当前缓解LVLM幻觉的方法可分为三类：解码过程修改、EOS logit调整和注意力头干预。本工作提出的**SGRS+LocoRE**组合属于第一类，但其核心机制与现有工作存在本质差异：

- **OPERA**（Huang et al., CVPR 2024）通过检测注意力图中的“锚点”模式来判断幻觉，依赖纯注意力权重。本工作证明注意力图在正确与幻觉令牌之间视觉上难以区分（Figure 1），而LVLMs-Saliency通过引入梯度信息捕获了注意力图无法反映的上下文失联信号。

- **DOPRA**（Wei & Zhang, MM 2024）在解码过程中惩罚锚点令牌，但其惩罚机制基于注意力图而非梯度增强的显著性度量。

- **VCD**（Leng et al., CVPR 2024）采用对比解码策略，通过比较原始模型与扰动模型的输出来减少幻觉，但未直接建模输出令牌间的上下文依赖强度。

- **EAH**（Zhang et al., EMNLP 2025）通过替换特定注意力头来缓解视觉注意力沉降，但直接修改模型内部表征会降低输出多样性。Table 1显示LocoRE的召回率高于EAH，因为LocoRE不改变模型内部表征，仅通过注意力权重增益增强上下文依赖。

- **TAME**（Tang et al., ICLR 2025）分析注意力局部化程度并动态调整锚点令牌，其关注点仍在注意力图模式层面，未引入梯度信息。

- **Vissink**（Kang et al., ICLR 2025）干预视觉注意力沉降，主要关注视觉-文本跨模态注意力，而本工作的LocoRE聚焦于**输出令牌间的自注意力**，直接针对“上下文漂移”这一被现有工作忽视的幻觉来源。Table 2显示LocoRE在CHAIR指标上显著优于Vissink和TAME，验证了增强文本侧上下文依赖对缓解幻觉的有效性。

### 方法谱系中的定位：双重干预策略

本工作在推理阶段引入**双重干预**，形成了完整的方法链条：

1. **LVLMs-Saliency诊断模块**（Section 2.1, Eqs. 1-5）：计算单层单头显著性矩阵 $\mathbf{S}^{(l,h)} = \operatorname{tril}\left( |\mathbf{A}^{(l,h)} \odot \nabla \mathbf{A}^{(l,h)}| \right)$，经层级L2归一化后得到标准化显著性 $\bar{\mathbf{S}}^{(l)}$，为目标层上的候选令牌评估提供上下文接地强度度量。

2. **SGRS过滤器**（Section 3.1, Algorithm 1）：在每一步解码时计算候选令牌 $c_i$ 的显著性得分 $\mathcal{S}(c_i)$，并与自适应阈值 $\tau^{(P)} = \alpha \cdot \frac{1}{|\mathcal{H}|} \sum_{j \in \mathcal{H}} S(x_j)$ 比较。低于阈值的候选被拒绝，强制模型重采样至选出上下文接地的令牌。若所有候选均被拒绝，则回退至选择显著性最高的令牌。

3. **LocoRE注意力增强器**（Section 3.1.1, Algorithm 2）：在令牌被接受后，对下一步前向传播中指向最近 $w_s$ 个输出令牌的注意力权重施加距离加权增益 $\gamma_j^{(P)} = 1 + \beta \cdot \mathbb{I}\left((P-j) \leq w_s\right)$，即 $\mathbf{A}^{(P+1)}[b,h,P+1,j] \leftarrow \mathbf{A}^{(P+1)}[b,h,P+1,j] \cdot \gamma_j^{(P)}$，主动增强对近期输出的依赖。

SGRS和LocoRE的分工明确：SGRS直接抑制幻觉令牌的生成，LocoRE专注于维持序列级上下文连贯性。消融实验（Table 3）表明，仅使用LocoRE（无SGRS）即可显著降低幻觉率，证明上下文连贯性增强本身具有独立的幻觉缓解效果。

### 适用边界与局限

1. **梯度计算的内存瓶颈**：SGRS需要在推理时计算注意力权重的梯度并存储中间激活，导致约30-40%的延迟增加。这使得该方法目前无法部署在72B及以上参数的大模型上，限制了其在超大模型上的应用。

2. **“高显著性幻觉”失效**：本方法的核心假设是“低显著性导致幻觉”，但当模型对错误答案具有极高置信度时（即幻觉令牌本身具有高显著性），低显著性假设失效。SGRS无法过滤此类“自信出错”的幻觉。

3. **上下文无关生成的不适用性**：当输入提示本身模糊或信息不足时，合理的低显著性令牌可能被SGRS错误拒绝，导致生成质量下降。显著性阈值 $\tau^{(P)}$ 的自适应机制仅基于近期历史令牌的平均显著性，未考虑输入上下文的不确定性。

4. **幻觉类型覆盖有限**：LocoRE仅通过强化上下文注意来缓解“上下文漂移”类幻觉，无法处理所有幻觉类型（如视觉感知错误导致的幻觉）。

### 开放问题

1. **无梯度显著性近似**：如何在不依赖梯度计算的情况下近似令牌显著性，从而大幅降低SGRS的内存开销，使其适用于百亿参数级模型？可能的路径包括基于注意力熵的近似或轻量级探针网络。

2. **高低显著性幻觉的区分与互补防御**：如何区分因上下文缺失导致的低显著性幻觉和因模型“自信出错”导致的高显著性幻觉，并设计互补的防御机制？可能需要结合不确定性估计或模型内部置信度信号。

3. **不确定性感知的自适应阈值**：当输入上下文本身具有高度不确定性时，显著性阈值如何自适应调整，以避免过滤掉合理但上下文关联弱的输出？当前基于历史令牌平均显著性的阈值设计未考虑输入端的模糊性。

4. **与其他幻觉缓解方法的协同**：SGRS+LocoRE聚焦于输出令牌间的上下文依赖，而Vissink等方法关注视觉注意力沉降。两类方法的互补性已在Table 2中初步显现，但系统性协同机制的设计仍有待探索。

## 原文 PDF

![[paperPDFs/ICLR_2026/Hallucination_Begins_Where_Saliency_Drops.pdf]]
