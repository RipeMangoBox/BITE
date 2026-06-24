---
title: "ActAvatar: Temporally-Aware Precise Action Control for Talking Avatars"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/ActAvatar_Temporally_Aware_Precise_Action_Control_for_Talking_Avatars.pdf
project_link: "https://ziqiaopeng.github.io/ActAvatar/"
code_link: null
aliases:
- ActAvatar
tags:
- CVPR_2026
- topic/other_unclear
- topic/other_unclear/general
core_operator: 通过层次化提示分解与时间锚点结合可学习的相位位置嵌入，模型能够在正确的时间窗口集中关注相位相关令牌，实现时间-语义对齐；同时通过深度渐进的音频影响缩放函数（f(ℓ) = (ℓ/L)^γ），使浅层优先建立文本驱动的动作结构，深层逐步增强音频以细化唇形，消除模态冲突。
primary_logic: 结构化提示分解（PACA）、渐进式音频-视觉对齐和两阶段训练三者协同：PACA提供时间-语义绑定，渐进对齐解耦文本与音频的作用阶段，两阶段训练保留基础能力的同时注入动作控制，从而同时实现精确的相位级动作执行和高质量唇形同步。
claims:
- Phase-Aware Cross-Attention (PACA) 将提示分解为全局基块与带时间锚点的相位块，并加入可学习的相位位置嵌入，使模型能在正确的时间窗口关注相关令牌。
- 消融实验证明，移除 PACA 后动作控制指标大幅下降，Hit@Segment 从 0.854 降至 0.725，验证了其时间-语义对齐的核心作用。
- HDTF 上 FID = 23.471
- HDTF 上 Sync-D = 7.545
---

# ActAvatar: Temporally-Aware Precise Action Control for Talking Avatars

> [!tip] 核心洞察
> 结构化提示分解（PACA）、渐进式音频-视觉对齐和两阶段训练三者协同：PACA提供时间-语义绑定，渐进对齐解耦文本与音频的作用阶段，两阶段训练保留基础能力的同时注入动作控制，从而同时实现精确的相位级动作执行和高质量唇形同步。

| 字段 | 内容 |
|------|------|
| 中文题名 | ActAvatar：面向对话化身的精确时间感知动作控制 |
| 英文题名 | ActAvatar: Temporally-Aware Precise Action Control for Talking Avatars |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2512.19546) · [Project](https://ziqiaopeng.github.io/ActAvatar/) |
| Topic | #topic/other_unclear #topic/other_unclear/general |
| Method | ActAvatar |
| Dataset | HDTF, Action Bench |

> [!tip] 效果简介
> - HDTF 上，FID 23.471 vs 24.515 (HunyuanVideo-Avatar) (-1.044)；Sync-D 7.545 vs 7.564 (HunyuanVideo-Avatar) (-0.019)。
> - Action Bench 上，Hit@Segment 0.854 vs 0.725 (w/o PACA from ablation) (+0.129)；Sync-C 6.893 vs 6.390 (w/o Progressive Audio Alignment from ablation) (+0.503)。

## 概述

**问题瓶颈**：现有说话头像生成方法普遍将动作描述与音频输入统一处理为扁平提示，缺乏对动作执行时机的精确控制。这导致三重困境——动作与语音语义在时间上不同步、文本驱动的肢体动作与音频驱动的唇形同步相互干扰、以及微调后模型原有的文本跟随能力严重退化。

**核心思路**：ActAvatar 通过三个协同机制破解上述瓶颈。其核心是**Phase-Aware Cross-Attention (PACA)**，将文本提示分解为全局基块与带时间锚点的相位块，并引入可学习的相位位置嵌入，使模型在正确的时间窗口集中关注相位相关令牌，实现时间-语义对齐。在此基础上，**渐进式音频-视觉对齐**采用深度感知的音频影响缩放函数 $f(\ell) = (\ell/L)^{\gamma}$，让浅层优先建立文本驱动的动作结构，深层逐步增强音频以细化唇形，消除模态冲突。最后，**两阶段训练策略**先冻结骨干网络训练音频适配器以保留基础生成能力，再全参数注入动作控制，避免能力退化。

**方法定位**：ActAvatar 属于文本-音频双模态驱动的说话头像生成方法，在提示结构、音频-视觉融合机制和训练策略三个关键维度上对主流方案进行了系统性改进。与 Hallo3、EchoMimic v3、HunyuanVideo-Avatar 等采用单一扁平提示和静态等权融合的基线方法相比，ActAvatar 首次实现了相位级的精确动作时间控制。

**主要结果**：在 HDTF 测试集上，ActAvatar 取得 FID 23.471 和 Sync-D 7.545，均优于对比方法。在专门构建的 Action Bench 上，Hit@Segment 达到 0.854，Sync-C 达到 6.893，全面领先。消融实验证实，移除 PACA 后 Hit@Segment 骤降至 0.725，验证了时间-语义对齐的核心作用；移除渐进音频对齐后 Sync-C 降至 6.390，证明了深度感知缩放对唇同步的关键贡献。用户研究进一步确认了该方法在动作质量和时间正确性上的显著优势。

## 背景与动机

### 问题背景

说话头像（Talking Avatar）生成旨在根据音频输入驱动静态肖像产生自然的面部运动与唇形同步。近年来，基于扩散模型（Diffusion Models）的方法在此任务上取得了显著进展，能够生成高质量、唇形准确的说话视频。然而，现有方法普遍存在一个根本性瓶颈：**缺乏对动作执行时机的精确控制**。具体而言，它们能够生成“说话”这一行为，却无法精确控制“何时做出何种动作”——例如在说出特定词语时挥手、在停顿间隙点头、或在情绪转折处改变身体姿态。

这一缺陷源于现有方法对提示（Prompt）的粗糙处理方式。无论是 **Hallo3**、**FantasyTalking**、**EchoMimic v3** 等专门化说话头像方法，还是 **HunyuanVideo-Avatar**、**MultiTalk**、**OmniAvatar** 等通用化方法，均采用单一全局提示来描述整个视频序列。这种扁平化的提示结构无法编码动作与时间之间的对应关系，导致模型难以学习“在哪个时间窗口执行哪个动作”的映射。

### 现有方法缺口

当前方法的局限性可从三个维度加以剖析：

**1. 动作-语音语义不同步。** 由于提示缺乏时间维度，模型无法将特定动作与音频中的语义事件对齐。例如，当音频内容为“让我向你展示”时，理想情况下化身应同时做出展示手势；但在全局提示范式下，模型可能将手势提前或延后执行，甚至完全忽略这一关联。

**2. 文本驱动动作与音频驱动唇形同步之间的模态冲突。** 文本提示负责指导全局动作生成，音频信号负责驱动精细的唇形同步，两者在交叉注意力层中共享表示空间。当文本与音频信息同时注入时，它们会相互干扰：文本可能覆盖音频带来的唇形细节，音频也可能削弱文本指定的动作结构。现有方法缺乏机制来解耦这两种模态的影响。

**3. 微调后文本跟随能力退化。** 当对预训练模型进行动作控制微调时，模型往往会出现“灾难性遗忘”——虽然获得了动作执行能力，却丢失了原有的文本跟随能力，导致生成结果与提示内容脱节。这暴露了单阶段联合训练的固有缺陷。

### 本文动机

针对上述缺口，ActAvatar 提出了一套系统性的解决方案，其核心动机在于实现**精确的时间感知动作控制**——不仅控制化身“做什么动作”，更要控制“在何时做动作”，同时保持高质量的唇形同步。这一目标需要同时解决三个相互关联的子问题：

- **时间-语义对齐**：如何让模型理解动作描述与时间窗口之间的绑定关系？
- **模态解耦**：如何防止文本驱动的动作生成与音频驱动的唇形同步相互干扰？
- **能力保留**：如何在注入动作控制能力的同时，不破坏预训练模型的原有能力？

ActAvatar 通过三个协同设计的模块来回应这些挑战：**Phase-Aware Cross-Attention（PACA）** 实现层次化提示分解与时间-语义绑定，**Progressive Audio-Visual Alignment** 通过深度感知缩放解耦文本与音频的作用阶段，**两阶段训练策略** 解耦音频适配器学习与动作控制注入。这三者共同构成了从提示结构、模态融合到训练范式的完整技术链路。

## 核心创新

ActAvatar 的核心创新在于通过**结构化提示分解**、**渐进式模态对齐**和**解耦训练策略**三个维度，系统性地解决了现有说话头像生成方法中“动作执行时机不可控”这一瓶颈。与采用单一全局提示、静态等权融合音频与文本的 baseline 方法不同，ActAvatar 将动作控制建模为时间-语义绑定的层次化问题，而非简单的文本到动作映射。

### 从统一提示到时间锚定的层次化提示分解

现有方法通常将整个动作描述压缩为单一全局提示（flat global prompt），模型无法区分不同动作的执行阶段，导致动作与语音语义不同步。ActAvatar 引入 **Phase-Aware Cross-Attention (PACA)** 机制，将提示分解为全局基块与带时间锚点的相位块：

$$
\mathbf{P} = \{ \mathbf{P}_{\mathrm{base}}, \{ \mathbf{P}_{k}, \mathcal{T}_{k} \}_{k=1}^{K} \}
$$

其中 $\mathbf{P}_{\mathrm{base}}$ 编码身份与场景等全局信息，每个相位块 $(\mathbf{P}_{k}, \mathcal{T}_{k})$ 显式绑定动作描述与其执行时间窗口。为进一步强化时间-语义对齐，PACA 为每个令牌添加可学习的相位位置嵌入 $\mathbf{c}_{i}^{\prime} = \mathbf{c}_{i} + \mathbf{e}_{k}$，使交叉注意力机制能够在正确的时间窗口内集中关注相位相关令牌。这一设计将动作控制的粒度从“整段视频”精细到“相位级”，是 ActAvatar 实现精确时间动作执行的核心因果旋钮。

### 从静态融合到深度感知的渐进式音频-视觉对齐

文本驱动动作与音频驱动唇形同步之间存在天然冲突：文本倾向控制整体运动，音频则精细调节唇部。现有方法采用静态等权交叉注意力融合，导致两种模态在生成过程中相互干扰。ActAvatar 提出**渐进式音频-视觉对齐**策略，通过深度感知的缩放函数控制音频在不同网络层的影响强度：

$$
\mathbf{x}_{\ell} \gets \mathbf{x}_{\ell} + f(\ell) \cdot \mathbf{r}_{\mathrm{audio}}^{\ell}, \quad f(\ell) = \left( \frac{\ell}{L} \right)^{\gamma}
$$

其中 $\ell$ 为当前层索引，$L$ 为总层数，$\gamma$ 控制音频影响的增长速度。在浅层，$f(\ell)$ 接近零，模型优先建立文本驱动的动作结构；在深层，$f(\ell)$ 逐渐增大，音频信号逐步增强以细化唇形同步。这一设计与 U-Net 层次化特征学习过程对齐——浅层学习粗粒度结构，深层学习细粒度细节——从而在机制层面消除了模态冲突。

### 从单阶段联合训练到解耦的两阶段训练

直接将动作控制注入预训练模型会导致灾难性遗忘，丢失原有的文本跟随能力。ActAvatar 采用**两阶段训练策略**解耦音频-视觉对齐学习与时间动作控制注入：

- **阶段一**：冻结基础骨干参数 $\theta_{\mathrm{base}}$，仅训练音频适配器参数 $\theta_{\mathrm{audio}}$，使用简洁提示 $\mathbf{C}_{\mathrm{brief}}$ 学习音视频对齐：

$$
\mathcal{L}_{\mathrm{stage1}} = \mathbb{E}_{\mathbf{x}_{0}, t, \mathbf{x}_{1}} \left[ \left\| \mathbf{v}_{\theta}(\mathbf{x}_{t}, t, \mathbf{C}_{\mathrm{brief}}, \mathbf{A}) - (\mathbf{x}_{1} - \mathbf{x}_{0}) \right\|^{2} \right]
$$

- **阶段二**：全参数微调，注入 PACA 结构化提示 $\mathbf{C}_{\mathrm{PACA}}$，学习时间动作控制：

$$
\mathcal{L}_{\mathrm{stage2}} = \mathbb{E}_{\mathbf{x}_{0}, t, \mathbf{x}_{1}} \left[ \left\| \mathbf{v}_{\theta}(\mathbf{x}_{t}, t, \mathbf{C}_{\mathrm{PACA}}, \mathbf{A}) - (\mathbf{x}_{1} - \mathbf{x}_{0}) \right\|^{2} \right]
$$

消融实验证实，单阶段或直接微调方式会导致音视频对齐与动作控制能力同时下降，而两阶段解耦训练是同时保持唇形同步质量和动作控制精度的必要条件（Table 4）。

### 三个 changed slots 的协同效应

上述三个 changed slots 并非孤立改进，而是形成闭环协同：PACA 提供时间-语义绑定，渐进对齐解耦文本与音频的作用阶段，两阶段训练保留基础能力的同时注入动作控制。消融实验（Table 4）量化了这一协同效应——移除 PACA 后 Hit@Segment 从 0.854 降至 0.725，移除渐进音频对齐后 Sync-C 从 6.893 降至 6.390，而完整的 ActAvatar 在所有指标上达到最优。

## 整体框架

ActAvatar 的整体流程围绕一个核心矛盾展开：**文本驱动的动作生成**与**音频驱动的唇形同步**在共享的潜在空间中存在模态冲突。为解决这一问题，ActAvatar 构建了一条从结构化提示输入到时间对齐视频输出的三阶段流水线，通过层次化提示分解、渐进式多模态融合与两阶段训练策略协同工作。

### 输入与预处理

系统的输入包括三部分：

1. **参考图像**：提供化身的身份外观信息。
2. **音频信号**：驱动唇形同步的语音输入。
3. **结构化文本提示**：描述“执行什么动作”以及“何时执行”，由多模态大语言模型（MLLM）自动生成。

结构化提示是 ActAvatar 区别于现有方法的关键设计。如 Figure 2 所示，提示被分解为层次化的两部分：一个**全局基块（base block）** 描述整体场景与身份信息，以及多个**相位块（phase blocks）**，每个相位块包含一个动作描述和一个时间锚点（temporal anchor），显式编码了动作的执行时间窗口。这种分解构成了后续时间-语义对齐的基础。

![[assets/figures/papers/paper_list_l2_https_arxiv_org_abs_2512_19546/figures/002_Figure_2.jpg]]
*Figure 2: Overview of ActAvatar. Given an audio input and reference image, ActAvatar generates temporally-controlled action videos guided by structured prompts automatically generated from MLLM*

### 核心模块与数据流

ActAvatar 的生成流水线由三个核心模块串联构成：

**1. Phase-Aware Cross-Attention（PACA）—— 时间-语义对齐层**

PACA 模块接收结构化提示，为每个相位块的令牌添加可学习的相位位置嵌入（phase position embedding），使模型能够区分不同令牌的相位归属。在交叉注意力计算中，模型通过相位条件注意力机制，在正确的时间窗口内集中关注当前相位对应的令牌，从而实现动作描述与视频帧之间的时间对齐。这一模块是动作控制精度的核心保障——消融实验表明，移除 PACA 后 Hit@Segment 指标从 0.854 降至 0.725，生成结果趋于静止。

**2. Progressive Audio-Visual Alignment —— 模态冲突解耦层**

该模块处理文本驱动动作与音频驱动唇形之间的干扰问题。其核心设计是一个深度感知的音频影响缩放函数：

$$f(\ell) = \left( \frac{\ell}{L} \right)^{\gamma}$$

其中 $\ell$ 为当前 Transformer 层索引，$L$ 为总层数，$\gamma$ 控制缩放曲线的陡峭程度。该函数使得浅层（$\ell$ 较小）的音频交叉注意力残差被显著抑制，让文本提示优先建立动作结构；深层（$\ell$ 接近 $L$）则逐步增强音频影响，细化唇形同步。Figure 4 的注意力可视化验证了这一设计：浅层（Layer 5）的相位聚焦较为模糊，深层（Layer 20）则呈现出锐利的相位分离，表明模型在深层完成了精细的时序对齐。

**3. Audio Adapter —— 音频特征提取与对齐层**

音频适配器基于 Wav2Vec 2.0 提取音频特征，通过交叉注意力将其映射为与视频帧对齐的令牌序列。该模块在训练过程中被解耦处理（见下文两阶段训练），确保音频对齐能力与动作控制能力可以独立优化。

### 两阶段训练策略

ActAvatar 采用解耦的两阶段训练策略，以保留预训练基础模型的能力同时注入动作控制：

- **阶段一（Stage 1）**：冻结基础文本到视频骨干网络的全部参数，仅训练音频适配器。损失函数为流匹配（Flow Matching）目标，使用简要提示（$\mathbf{C}_{\text{brief}}$）和音频（$\mathbf{A}$）作为条件：

$$\mathcal{L}_{\text{stage1}} = \mathbb{E}_{\mathbf{x}_0, t, \mathbf{x}_1} \left[ \left\| \mathbf{v}_{\theta}(\mathbf{x}_t, t, \mathbf{C}_{\text{brief}}, \mathbf{A}) - (\mathbf{x}_1 - \mathbf{x}_0) \right\|^{2} \right]$$

此阶段建立音频-视觉对齐能力，为后续动作控制注入奠定基础。

- **阶段二（Stage 2）**：全参数微调，注入时间动作控制。使用 PACA 编码的结构化提示（$\mathbf{C}_{\text{PACA}}$）替换简要提示：

$$\mathcal{L}_{\text{stage2}} = \mathbb{E}_{\mathbf{x}_0, t, \mathbf{x}_1} \left[ \left\| \mathbf{v}_{\theta}(\mathbf{x}_t, t, \mathbf{C}_{\text{PACA}}, \mathbf{A}) - (\mathbf{x}_1 - \mathbf{x}_0) \right\|^{2} \right]$$

消融实验证实，完整的两阶段训练对于同时保持音视频对齐和动作控制至关重要，单阶段联合训练或直接微调的方式均导致能力下降。

### 整体数据流总结

从输入到输出的完整数据流为：参考图像与结构化提示经 PACA 编码后注入扩散 Transformer 骨干网络，音频信号经 Wav2Vec 2.0 提取特征后通过音频适配器映射为帧对齐令牌，在每一层 Transformer 中按渐进缩放函数 $f(\ell)$ 加权注入。最终通过流匹配路径 $\mathbf{x}_t = (1 - t) \mathbf{x}_0 + t \mathbf{x}_1$ 从噪声逐步生成时间对齐的说话化身视频。

## 核心模块与公式推导

ActAvatar 的核心架构围绕三个协同模块展开：**Phase‑Aware Cross‑Attention (PACA)** 实现时间‑语义对齐，**Progressive Audio‑Visual Alignment** 消除文本驱动动作与音频驱动唇形同步之间的模态干扰，以及**两阶段训练策略**解耦能力注入过程。

### 3.1 层次化提示分解

PACA 将文本提示分解为层次化结构，显式编码时间接地信息。给定一个包含 $K$ 个动作相位的描述，提示被组织为：

$$
\mathbf{P} = \{ \mathbf{P}_{\mathrm{base}}, \{ \mathbf{P}_{k}, \mathcal{T}_{k} \}_{k=1}^{K} \}
$$

其中 $\mathbf{P}_{\mathrm{base}}$ 是全局基块，描述与时间无关的上下文（如人物外观、背景），而每个相位块 $\mathbf{P}_{k}$ 携带第 $k$ 个动作的语义描述及其时间窗口 $\mathcal{T}_{k}$。这种结构化分解使模型能够区分“做什么动作”与“何时做动作”两个正交维度。

### 3.2 相位位置编码

为让模型感知令牌的相位归属，PACA 为每个令牌添加可学习的相位位置嵌入。对于属于相位 $k$ 的令牌 $\mathbf{c}_i$：

$$
\mathbf{c}_{i}^{\prime} = \mathbf{c}_{i} + \mathbf{e}_{k}
$$

其中 $\mathbf{e}_{k}$ 是相位特定的可学习嵌入向量。增强后的令牌随后通过标准交叉注意力机制与视觉特征交互：

$$
\operatorname{Attention}(\mathbf{Q}_{f}, \mathbf{K}, \mathbf{V}) = \operatorname{softmax}\left( \frac{\mathbf{Q}_{f} \mathbf{K}^{T}}{\sqrt{D}} \right) \mathbf{V}
$$

相位位置嵌入的作用在于引导注意力权重在正确的时间窗口内集中到对应相位的令牌上。消融实验中的交叉注意力可视化（Figure 4）证实了这一机制：浅层（Layer 5）的相位聚焦尚不明确，而深层（Layer 20）呈现出锐利的相位分离，表明模型在深层学会了精确的时间‑语义对齐。

![[assets/figures/papers/paper_list_l2_https_arxiv_org_abs_2512_19546/figures/006_Figure_4.jpg]]
*Figure 4: Cross-attention phase focus at layer 5 (top) and layer 20 (bottom). Deeper layers show sharper phase separation*

### 3.3 渐进式音频‑视觉对齐

文本驱动动作生成与音频驱动唇形同步之间存在天然的模态冲突：前者需要模型关注语义级运动结构，后者要求帧级精细对齐。ActAvatar 通过深度感知的音频影响缩放函数解决这一问题。在第 $\ell$ 层 Transformer 块中，音频交叉注意力的残差被缩放：

$$
\mathbf{x}_{\ell} \gets \mathbf{x}_{\ell} + f(\ell) \cdot \mathbf{r}_{\mathrm{audio}}^{\ell}, \quad f(\ell) = \left( \frac{\ell}{L} \right)^{\gamma}
$$

其中 $\mathbf{r}_{\mathrm{audio}}^{\ell}$ 是第 $\ell$ 层的音频交叉注意力输出，$L$ 是总层数，$\gamma$ 控制缩放曲线的陡峭程度。该函数在浅层（$\ell \ll L$）几乎抑制音频影响，使文本提示主导动作结构的建立；随着层数加深，$f(\ell)$ 单调递增，音频影响逐步增强以细化唇形细节。这种渐进策略与视觉特征学习的分层特性对齐——浅层关注全局结构，深层处理局部细节——从而从根本上解耦两个模态的作用阶段。

### 3.4 两阶段训练策略

训练过程分为两个阶段，分别对应不同能力的注入。

**阶段一：音频‑视觉对齐学习。** 冻结基础文本到视频骨干的参数 $\theta_{\mathrm{base}}$，仅训练音频适配器参数 $\theta_{\mathrm{audio}}$。此时使用简要文本条件 $\mathbf{C}_{\mathrm{brief}}$（不含时间相位信息），优化流匹配目标：

$$
\mathcal{L}_{\mathrm{stage1}} = \mathbb{E}_{\mathbf{x}_{0}, t, \mathbf{x}_{1}} \left[ \left\| \mathbf{v}_{\theta}(\mathbf{x}_{t}, t, \mathbf{C}_{\mathrm{brief}}, \mathbf{A}) - (\mathbf{x}_{1} - \mathbf{x}_{0}) \right\|^{2} \right]
$$

其中 $\mathbf{x}_{t} = (1 - t) \mathbf{x}_{0} + t \mathbf{x}_{1}$ 是最优传输流路径，$\mathbf{A}$ 为音频条件。此阶段仅建立基础的音视频同步能力，不引入动作控制。

**阶段二：时间感知动作控制注入。** 解冻全部参数，使用完整的 PACA 结构化提示 $\mathbf{C}_{\mathrm{PACA}}$ 进行全参数微调：

$$
\mathcal{L}_{\mathrm{stage2}} = \mathbb{E}_{\mathbf{x}_{0}, t, \mathbf{x}_{1}} \left[ \left\| \mathbf{v}_{\theta}(\mathbf{x}_{t}, t, \mathbf{C}_{\mathrm{PACA}}, \mathbf{A}) - (\mathbf{x}_{1} - \mathbf{x}_{0}) \right\|^{2} \right]
$$

两阶段设计的关键在于：阶段一在冻结骨干的前提下建立音频‑视觉对齐，保留了预训练模型的文本跟随能力；阶段二在此基础上注入时间动作控制，避免了直接联合训练导致的模态干扰与能力退化。消融实验（Table 4）证实，完整的二阶段训练在所有指标上均优于单阶段或微调变体。

### 补充图表

![[assets/figures/papers/paper_list_l2_https_arxiv_org_abs_2512_19546/figures/007_Figure_5.jpg]]
*Figure 5: Ablation study on PACA. Top: Without PACA, the avatar remains static throughout the sequence. Bottom: With PACA, the avatar naturally walks forward*

## 实验与分析

### 主结果：视觉质量与唇同步

ActAvatar 在两个基准上进行了系统评估：HDTF（标准说话头像数据集）和 Action Bench（自建的动作控制基准）。

在 HDTF 测试集上（Table 1），ActAvatar 在视觉质量方面取得最优 FID（23.471），优于 **HunyuanVideo-Avatar** 的 24.515。唇同步指标 Sync-D 达到 7.545，与最强基线持平。这表明方法在提供额外时间动作控制能力的同时，并未牺牲基础的口型同步质量。

![[assets/figures/papers/paper_list_l2_https_arxiv_org_abs_2512_19546/figures/003_Table_1.jpg]]
*Table 1: Quantitative comparison on HDTF Test Set. Best results in bold, second best underlined*

在 Action Bench 上（Table 2），ActAvatar 在所有维度上均取得最优结果。核心动作控制指标 Hit@Segment 达到 0.854，显著领先于对比方法；Sync-C（唇同步一致性）为 6.893，Sync-D 为 8.246，验证了动作控制与唇同步的兼容性。此外，IQA（4.814）和 ASE（3.743）指标表明生成视频的视觉质量同样保持领先。基于 Gemini 的细粒度动作评估中，Action Accuracy（5.971）、Temporal Correctness（7.353）、Action Quality（7.671）和 Hand Clarity（8.483）均取得最优，证明方法在动作执行的时间精度和手部清晰度方面具有显著优势。

![[assets/figures/papers/paper_list_l2_https_arxiv_org_abs_2512_19546/figures/004_Table_2.jpg]]
*Table 2: Quantitative comparison on Action Bench. Best results in bold, second best underlined*

### 用户研究

Table 3 的用户研究结果进一步验证了客观指标的趋势。ActAvatar 在动作-提示对齐（APA，4.03）和手部清晰度（HC，4.22）两个维度上获得最高评分，表明人类评估者对时间精确的动作执行和手部细节质量有明确偏好。

![[assets/figures/papers/paper_list_l2_https_arxiv_org_abs_2512_19546/figures/008_Table_3.jpg]]
*Table 3: User study results*

### 消融实验：关键模块的因果验证

Table 4 的消融实验系统验证了三个核心设计的必要性：

![[assets/figures/papers/paper_list_l2_https_arxiv_org_abs_2512_19546/figures/009_Table_4.jpg]]
*Table 4: Ablation study of key components on Action Bench*

**PACA 的作用。** 移除 Phase-Aware Cross-Attention 后，Hit@Segment 从 0.854 降至 0.725，降幅达 15%。Figure 5 提供了直观的定性证据：无 PACA 时，化身在整个序列中保持静止，无法执行任何时间相关动作；加入 PACA 后，化身自然向前行走。这证实 PACA 是实现时间-语义对齐和控制动作执行时机的关键因果节点。

**渐进音频对齐的作用。** 移除深度感知的音频缩放函数 $f(\ell) = (\ell/L)^\gamma$ 后，Sync-C 从 6.893 降至 6.390。这验证了渐进策略有效防止了文本驱动动作生成与音频驱动唇形同步之间的模态干扰——浅层优先建立文本驱动的动作结构，深层逐步增强音频以细化唇形。

**两阶段训练的必要性。** 完整的双阶段训练在所有指标上取得最优结果。单阶段联合训练或直接微调的方式导致动作控制能力或唇同步质量的下降，证明解耦音频-视觉对齐学习与时间动作控制注入是保留预训练基础能力的关键策略。

### 注意力可视化分析

Figure 4 展示了交叉注意力在不同层深度的相位聚焦模式。浅层（第5层）的注意力分布相对分散，各相位块的边界模糊；深层（第20层）则呈现出清晰的相位分离，每个时间窗口的令牌仅在对应帧索引区域获得高注意力权重。这一可视化直接解释了 PACA 的工作机制：通过可学习的相位位置嵌入，模型在深层自动形成了时间条件化的注意力动态，实现了精确的时间-语义对齐。

### 定性对比

Figure 3 的定性对比展示了 ActAvatar 与现有方法在 Action Bench 样本上的差异。在包含两个不同动作相位的结构化提示下，ActAvatar 准确执行了每个相位指定的动作并保持正确的时间顺序，手部姿态清晰可辨；而对比方法普遍存在时间错位、动作模糊或手部变形等问题，进一步验证了时间感知动作控制的实际效果。

### 补充图表

![[assets/figures/papers/paper_list_l2_https_arxiv_org_abs_2512_19546/figures/001_Figure_1.jpg]]
*Figure 1: ActAvatar generates talking avatars with precise, temporally-aligned actions across diverse scenarios and identities. Through structured text prompts, our method controls what actions to perform and when to perform them, while maintaining accurate lip synchronization with the audio*

## 方法谱系与知识库定位

### 问题定位：从“做什么”到“何时做”

说话头像生成（Talking Avatar Generation）的主流范式长期围绕两个目标展开：**唇形同步**（lip-sync）与**视觉质量**（visual quality）。早期工作如 Wav2Lip 专注于音频-唇形对齐，后续基于扩散模型的方法（如 **Hallo3**、**EchoMimic v3**、**HunyuanVideo-Avatar**）在生成质量上取得显著提升，并开始引入文本提示以控制表情或头部姿态。然而，这些方法存在一个共同的瓶颈：**它们将文本提示视为全局条件，缺乏对动作执行时机的精确控制**。当用户描述“先挥手，然后点头”时，模型无法区分这两个动作的时序边界，导致动作与语音语义错位——例如在说“再见”之前就已完成挥手。

ActAvatar 的核心突破在于将问题从**动作内容控制**升级为**动作时序控制**，即同时回答“做什么动作”和“何时做”。这一转变使说话头像生成从简单的唇形同步任务，扩展为具有时间结构的行为序列生成任务。

### 与现有方法的谱系关系

#### 文本驱动动作控制方法

现有文本驱动方法（如 **FantasyTalking**、**MultiTalk**、**OmniAvatar**）通常采用**统一提示处理**（flat prompt processing）：将整个动作描述拼接为一个全局文本令牌序列，通过交叉注意力注入生成过程。这种设计存在两个根本性缺陷：

1. **时间-语义解耦缺失**：模型无法区分不同动作对应的文本片段，导致注意力分布在时间维度上趋于均匀，无法在特定时间窗口聚焦特定动作描述。
2. **模态冲突**：文本驱动的动作生成与音频驱动的唇形同步共享同一交叉注意力通道，两者在特征空间中相互干扰——文本倾向于控制全局运动，音频则要求精确的口型匹配。

ActAvatar 通过**层次化提示分解**（Hierarchical Prompt Decomposition）直接解决了第一个缺陷：将提示拆分为全局基块（$\mathbf{P}_{\mathrm{base}}$，描述身份、场景等恒定属性）和带时间锚点的相位块（$\{\mathbf{P}_k, \mathcal{T}_k\}_{k=1}^K$，描述特定时间窗口内的动作）。这种结构化设计使模型能够显式地建立文本令牌与时间段的对应关系，为后续的相位感知注意力提供了基础。

#### 音频-视觉对齐方法

在音频-视觉融合方面，主流方法（包括 **EchoMimic v3**、**HunyuanVideo-Avatar**）通常采用**静态等权交叉注意力融合**：音频特征和文本特征以固定权重在每一层参与生成。这种设计忽略了扩散模型中不同层级的特征学习特性——浅层主要构建空间结构和运动趋势，深层则细化细节和纹理。当文本和音频以相同强度作用于所有层时，两者在浅层争夺运动控制权，导致动作模糊或唇形不准确。

ActAvatar 的**渐进式音频-视觉对齐**（Progressive Audio-Visual Alignment）通过深度感知缩放函数 $f(\ell) = (\ell/L)^\gamma$ 解决了这一冲突：浅层（$\ell$ 小）音频影响弱，文本主导动作结构建立；深层（$\ell$ 大）音频影响强，细化唇形细节。这一设计与扩散模型的层级特征学习过程形成因果匹配，而非简单的经验性加权。

#### 训练策略对比

现有方法通常采用**单阶段联合训练**：同时优化所有参数以适应文本和音频条件。这种方式存在两个风险：（1）预训练基础模型的文本跟随能力可能被破坏；（2）音频-视觉对齐与动作控制两个目标在梯度层面相互干扰。

ActAvatar 的**两阶段训练策略**（Two-Stage Training）将学习过程解耦：第一阶段冻结基础骨干，仅训练音频适配器以建立音视频对齐；第二阶段全参数微调，注入时间动作控制。这种设计保留了预训练模型的生成能力，同时实现了新能力的稳定注入，类似于迁移学习中的渐进式微调范式。

### 方法边界与适用条件

ActAvatar 的设计隐含以下适用边界：

1. **动作描述的粒度要求**：PACA 的有效性依赖于动作描述具有明确的时间边界。对于连续、无明确分段的长时动作（如“持续微笑”），相位分解的优势可能减弱，因为时间锚点的划分变得模糊。
2. **音频-文本一致性假设**：渐进对齐策略假设文本描述的动作与音频内容在语义上一致。当文本描述“愤怒地挥手”但音频是平静的语调时，浅层的文本主导可能导致不自然的情绪-语音错位。
3. **身份保持的隐式依赖**：ActAvatar 通过全局基块提供身份信息，但未引入显式的身份保持机制（如 face embedding 或 identity loss）。在极端姿态或长序列生成中，身份漂移的风险需要通过实验进一步验证（论文未提供相关消融）。
4. **计算开销**：两阶段训练增加了训练复杂度，且 PACA 的相位位置嵌入引入了额外的可学习参数。论文未报告推理延迟与基线方法的对比，实际部署效率需要手动验证。

### 开放问题与潜在改进方向

1. **动作时序的自动标注**：论文使用 MLLM 自动生成结构化提示，但未详细评估自动标注的准确性。当 MLLM 错误划分动作边界时，PACA 是否会传播并放大这一错误？引入时序定位验证模块可能提升鲁棒性。
2. **相位数量的自适应确定**：当前方法预设相位数量 $K$，但不同场景的最优 $K$ 可能不同。动态相位划分（如基于音频语义转折点）可能进一步提升灵活性。
3. **与端到端音频-动作联合建模的对比**：ActAvatar 将动作控制完全交由文本提示，未探索直接从音频中预测动作时序的可能性。与端到端方法（如从语音中预测手势序列）的对比将有助于明确文本驱动的独特优势。
4. **跨模态时序一致性度量**：论文提出的 Hit@Segment 等指标依赖于 Gemini 的自动评估，其可靠性需要更大规模的人类评估验证。建立标准化的时序动作控制基准将推动该方向的公平比较。

## 原文 PDF

![[paperPDFs/CVPR_2026/ActAvatar_Temporally_Aware_Precise_Action_Control_for_Talking_Avatars.pdf]]
