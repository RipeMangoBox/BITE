---
title: "CustomCrafter: Customized Video Generation with Preserving Motion and Concept Composition Abilities"
type: paper
paper_level: A
venue: AAAI
year: 2025
pdf_ref: paperPDFs/arxiv_2024/CustomCrafter_Customized_Video_Generation_with_Preserving_Motion_and_Concept_Composition_Abilities.pdf
aliases:
- CustomCrafter
tags:
- AAAI_2025
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: "VDM去噪过程的阶段性特征——早期步骤恢复整体布局与运动，后期步骤恢复目标细节——可被用于解耦运动与外观：通过可插拔的LoRA模块，在早期推理阶段降低主题学习模块的影响以保留运动，在后期阶段恢复其影响以修复外观，从而无需额外视频即可同时保证运动流畅性与主题一致性。"
primary_logic: "利用VDM去噪阶段的不同功能倾向，采用动态加权视频采样策略控制LoRA权重，结合同时微调交叉注意力和自注意力层的空间主题学习模块，可在不引入额外视频或多次微调的前提下，同时保留模型的固有运动生成能力与概念组合能力。"
claims:
- "VDM去噪的早期阶段主要恢复帧间的布局与运动，后期阶段主要恢复物体的外观细节，该现象可通过可视化观察到。"
- "在空间transformer中同时微调交叉注意力和自注意力层的Q、K、V（空间主题学习模块SSLM）能显著提升主题相似度（CLIP-I平均提升0.038）和形状保持能力，优于仅更新交叉注意力的方法。"
- "动态加权视频采样策略（DWVSS）在推理早期降低LoRA权重，后期恢复权重，使CLIP-T文本对齐分数大幅提升至0.318，且用户研究中运动流畅性显著优于基线。"
- "所提方法在四项指标上全面超越Custom Diffusion*和DreamVideo*，且用户偏好最高，证明不需要额外视频即可同时实现高保真主题、灵活概念组合与流畅运动。"
---

# CustomCrafter: Customized Video Generation with Preserving Motion and Concept Composition Abilities

> [!tip] 核心洞察
> 利用VDM去噪阶段的不同功能倾向，采用动态加权视频采样策略控制LoRA权重，结合同时微调交叉注意力和自注意力层的空间主题学习模块，可在不引入额外视频或多次微调的前提下，同时保留模型的固有运动生成能力与概念组合能力。

| 字段      | 内容                                                                                                                |
| ------- | ----------------------------------------------------------------------------------------------------------------- |
| 中文题名    | CustomCrafter：保留运动与概念组合能力的定制视频生成                                                                                  |
| 英文题名    | CustomCrafter: Customized Video Generation with Preserving Motion and Concept Composition Abilities               |
| 会议/期刊   | AAAI 2025                                                                                                         |
| Links   | [paper](https://arxiv.org/abs/2408.13239); [GitHub](https://github.com/WuTao-CS/CustomCrafter)                    |
| Topic   | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/image_and_video_generation |
| Method  | CustomCrafter                                                                                                     |
| Dataset | 20个定制主题的文本驱动视频生成（跨10个相关prompt），基模型VideoCrafter2, 同上                                                       |

> [!tip] 效果简介
> - 20个定制主题的文本驱动视频生成（跨10个相关prompt），基模型VideoCrafter2 上，CLIP-T (文本对齐↑) 为 0.318，对比 0.295 (DreamVideo*)，变化 +0.023。
> - 同上 上，CLIP-I (图像相似度↑) 为 0.786，对比 0.748 (DreamVideo*)，变化 +0.038。
> - 同上 上，DINO-I (特征相似度↑) 为 0.627，对比 0.536 (DreamVideo*)，变化 +0.091。

## 概述

**核心瓶颈**：在仅使用静态图像对视频扩散模型（VDM）进行主题定制微调时，模型会严重遗忘其固有的运动生成能力与概念组合能力。现有方法（如 **DreamVideo**，Wei et al., CVPR 2024）试图通过额外引入目标运动视频作为引导或进行二次微调来恢复这些能力，但这对普通用户而言极为不便——获取高质量运动视频本身就是一个高门槛需求。

**核心发现**：VDM 的去噪过程具有鲜明的阶段性特征——早期去噪步骤主要恢复帧间的整体布局与运动模式，后期步骤则专注于修复物体的外观细节（Figure 3）。这一发现为解耦运动与外观提供了天然的“因果旋钮”。

**方法定位**：基于上述发现，CustomCrafter 提出了两个协同工作的组件，在不引入任何额外视频、仅需单阶段训练的前提下，同时保留模型的运动生成与概念组合能力：

1.  **空间主题学习模块（SSLM）**：通过 LoRA 同时微调空间 Transformer 中交叉注意力层和自注意力层的 Q、K、V 参数，使模型充分捕捉新主题的外观细节与形状结构，同时保留概念组合能力。
2.  **动态加权视频采样策略（DWVSS）**：在推理阶段，利用 LoRA 的可插拔性，在早期去噪步骤（运动布局恢复阶段）降低 LoRA 权重以削弱主题学习模块对运动生成的影响，在后期步骤（外观修复阶段）恢复权重以精细化主题外观。

**方法谱系与知识库定位**：CustomCrafter 属于视频扩散模型的主题定制方法，其直接对比基线为基于 **VideoCrafter2** 复现的 **Custom Diffusion**（Kumari et al., CVPR 2023，仅微调交叉注意力）与 **DreamVideo**（Wei et al., CVPR 2024，需额外视频引导）。与这些方法相比，CustomCrafter 首次利用 VDM 去噪过程的阶段性特征实现运动-外观解耦，无需额外视频即可完成定制生成。

**主要结果**：在 20 个定制主题、跨 10 个相关提示的文本驱动视频生成基准上，CustomCrafter 在四项自动指标上全面超越对比方法——CLIP-T（文本对齐）达 0.318（+0.023 vs DreamVideo*），CLIP-I（图像相似度）达 0.786（+0.038），DINO-I（特征相似度）达 0.627（+0.091），时间一致性达 0.994。用户研究（38 名参与者评估 40 个视频）进一步证实，该方法在文本对齐、主题保真度和运动流畅性上均获得最高人类偏好（Figure 6）。消融实验验证了 SSLM 对主题外观捕获的关键作用（CLIP-I 提升 0.038），以及 DWVSS 在几乎不损失主题保真度的情况下显著改善文本对齐与运动质量的能力（CLIP-T 从 0.310 提升至 0.318）。

## 背景与动机

**核心瓶颈**：现有的视频定制生成方法在仅使用静态图像对视频扩散模型（VDM）进行主题微调时，会遭遇一个关键矛盾——模型虽然学会了新主题的外观，却遗忘了其固有的**运动生成能力**与**概念组合能力**。部分工作（如DreamVideo）试图通过引入额外视频来分别学习运动与外观，但这要求用户提供视频引导或进行多次重新微调，极大增加了使用门槛。

**因果机制**：本文首次发现并利用了VDM去噪过程的**阶段性特征**：在去噪的早期步骤，模型主要恢复帧间的整体布局与运动模式；而在后期步骤，模型才逐步精细化目标物体的外观细节（见Figure 3）。这一观察揭示了运动与外观在生成过程中存在天然的时序解耦——早期去噪阶段对主题学习模块的依赖较弱，而后期阶段则高度依赖该模块来修复外观。

**核心动机**：基于上述发现，本文试图回答一个关键问题：**能否在不引入任何额外视频、仅通过单阶段训练的前提下，同时保留VDM的运动生成与概念组合能力，并实现高保真的主题定制？** 这要求设计一种机制，在推理时动态调节主题学习模块的影响强度，使其仅在需要修复外观的后期阶段发挥作用，而在早期运动布局阶段“静默”，从而避免干扰模型原有的运动先验。

## 核心创新

CustomCrafter 的核心创新在于**首次揭示并利用视频扩散模型（VDM）去噪过程的阶段性特征**，将运动生成与外观修复解耦，从而在不引入额外视频或多次微调的前提下，同时保留模型的固有运动生成能力和概念组合能力。

### 瓶颈与因果机制

**真实瓶颈**：现有基于静态图像的 VDM 主题定制方法（如 Custom Diffusion、DreamVideo）在微调后，模型会遗忘其原有的运动生成能力和概念组合能力。恢复这些能力通常需要引入额外视频作为运动引导，或进行多次重新微调，这为用户带来了极大的不便，也限制了定制生成的灵活性。

**因果调控变量**：VDM 的去噪过程具有天然的阶段性分工——早期步骤主要恢复帧间的整体布局与运动模式，后期步骤则聚焦于物体外观细节的修复。这一现象在 Figure 3 中得到了可视化验证：运动在去噪早期即已形成，而主体外观在后期才逐渐清晰。基于此，作者提出了一个关键的调控变量：**通过可插拔的 LoRA 模块，在推理阶段动态控制主题学习模块的影响强度**——在运动布局修复阶段降低其权重以保留运动生成能力，在外观细节修复阶段恢复其权重以保证主题一致性。

### 相对基线的关键改动

相较于基线方法，CustomCrafter 在以下两个维度上做出了根本性改变：

**1. 微调参数范围：从仅更新交叉注意力到同时更新交叉注意力与自注意力**

基线方法（Custom Diffusion, Kumari et al., CVPR 2023）仅微调空间交叉注意力层的参数，这限制了模型对新主题外观的捕捉能力以及概念组合的准确性。CustomCrafter 提出的**空间主题学习模块（Spatial Subject Learning Module, SSLM）**，通过 LoRA 低秩适配器同时更新空间 transformer 中所有注意力层（交叉注意力和自注意力）的查询（Q）、键（K）、值（V）参数：

$$W = W_0 + \lambda \Delta W = W_0 + \lambda B A$$

其中 $B$ 和 $A$ 为低秩矩阵，$\lambda$ 控制 LoRA 的影响强度。这一改动使得模型能够更全面地学习新主题的外观特征，同时保持形状几何信息，因为自注意力层在保持物体几何形状和概念组合方面起着关键作用。消融实验（Table 2）证实，仅加入 SSLM 后，CLIP-I 从 DreamVideo* 的 0.748 提升至 0.790，DINO-I 从 0.536 提升至 0.631。

**2. 推理阶段 LoRA 权重策略：从固定权重到动态加权**

基线方法在整个去噪过程中使用固定的 LoRA 权重（通常为训练时的 $\lambda$ 或 1.0），这导致主题学习模块在运动形成的关键早期阶段过度干预，破坏了模型的运动生成能力。CustomCrafter 提出的**动态加权视频采样策略（Dynamic Weighted Video Sampling Strategy, DWVSS）**，将去噪过程分为两个阶段（Algorithm 1）：
- **阶段一（前 K 步）**：将所有 LoRA 模块的权重 $\lambda$ 调整为较小值 $\lambda_s$（默认 0.4），降低主题学习模块对运动布局恢复的干扰；
- **阶段二（后续步骤）**：将权重恢复至较大值 $\lambda_l$（默认 0.8），充分修复主体外观细节。

这一策略的巧妙之处在于：它利用了 LoRA 模块的可插拔特性，无需重新训练或引入额外视频，仅通过推理时的权重调节即可实现运动与外观的解耦。实验表明（Table 2），加入 DWVSS 后，CLIP-T 文本对齐分数从 0.310 提升至 0.318，同时在用户研究中运动流畅性显著优于所有对比方法（Figure 6）。

### 创新点的协同效应

SSLM 和 DWVSS 并非孤立工作，而是形成了完整的协同机制：SSLM 通过扩展微调范围提升了模型的**外观学习能力上限**，而 DWVSS 则通过推理阶段的动态控制**保护了模型的运动生成下限**。两者的结合使得 CustomCrafter 在仅需单阶段训练、单张静态图像作为输入的条件下，即可实现高保真主题、灵活概念组合与流畅运动的三重目标——这在 Table 1 的四项自动指标和 Figure 6 的用户偏好研究中均得到了充分验证。

### 局限与待验证问题

尽管核心创新具有明确的理论支撑和实验验证，但仍存在以下局限：
- 动态加权策略的三个超参数（$\lambda_s$、$\lambda_l$、$K$）目前依赖人工经验设定，缺乏对不同视频内容和运动复杂度的自适应能力；
- 去噪过程的运动-外观解耦现象仅在 VideoCrafter2 一种基模型上得到验证，其在不同 VDM 架构（如基于 Unet 或 DiT 的模型）上的普适性尚需进一步证明；
- 对于极端运动幅度或长时间生成场景，运动生成能力的保持效果尚未评估。

## 整体框架

![[assets/figures/papers/paper_list_l6_CustomCrafter_Customized_Video_Generation_with_Preserving_Motion_and_Con/figures/001_Figure_1.jpg]]
*Figure 1: Comparison of our approach with previous work. Our method can better learn the appearance of the subject while preserving the concept combination ability and motion generation ability, only requires one stage of training without additional videos. DWV Sampling Strategy is our Dynamic Weighted Video Sampling Strategy*

CustomCrafter 的完整流程围绕一个核心观察展开：视频扩散模型（VDM）的去噪过程具有阶段性特征——早期步骤主要恢复帧间的整体布局与运动，后期步骤则聚焦于物体的外观细节（Figure 3）。基于这一发现，方法将主题定制分解为两个解耦的子问题：**外观学习**与**运动保持**，并通过两个协同工作的模块在单阶段训练内完成。

整体 pipeline 由以下四个组件构成：

1.  **文本反转（Textual Inversion）**：首先为待定制的新主题学习一个专用标记 $V^*$ 及其在 CLIP 文本编码器中的嵌入向量，使模型能够通过文本条件引用该主题。

2.  **空间主题学习模块（Spatial Subject Learning Module, SSLM）**：在 VDM 的空间 transformer 块中，向所有交叉注意力层和自注意力层的查询（Q）、键（K）、值（V）投影插入 LoRA 低秩适配器进行微调。训练数据仅需单张主题图像重复 N 帧构成的静态视频。该模块负责捕获新主题的外观细节，并通过同时更新自注意力层来保持模型的概念组合能力。

3.  **动态加权视频采样策略（Dynamic Weighted Video Sampling Strategy, DWVSS）**：在推理生成视频时，利用 LoRA 模块的可插拔特性，将去噪过程划分为两个阶段：
    -   **运动布局修复阶段（前 K 步）**：将所有 LoRA 模块的权重 $\lambda$ 降低至较小值 $\lambda_s$（默认 0.4），削弱主题学习模块对运动生成的影响，保留基模型的固有运动能力。
    -   **外观细节修复阶段（后续步骤）**：将 LoRA 权重恢复至较大值 $\lambda_l$（默认 0.8），使 SSLM 能够精细化生成视频中的主题外观细节。

4.  **类特定先验保持损失（Class-specific Prior Preservation Loss）**：在训练过程中引入基于类别先验数据的正则化损失项 $\mathcal{L}_{pr}$，与视频扩散重建损失 $\mathcal{L}_{video}$ 加权求和（$\mathcal{L} = \mathcal{L}_{video} + \alpha \mathcal{L}_{pr}$，$\alpha=1.0$），以缓解微调过拟合并增强生成多样性。

**输入输出流**：系统接收一张目标主题的静态图像和一段描述目标动作与场景的文本提示。训练阶段，仅通过静态图像学习 SSLM 的 LoRA 参数和文本反转嵌入。推理阶段，用户提供包含 $V^*$ 的文本提示，DWVSS 策略自动调度 LoRA 权重，最终输出一段既保持主题高保真外观、又具备流畅运动且能正确组合文本概念的视频。整个流程无需任何额外视频引导或多次微调。

## 核心模块与公式推导

CustomCrafter 的核心由三个相互配合的模块构成：**空间主题学习模块（SSLM）** 负责从单张静态图像中学习新主题的外观；**动态加权视频采样策略（DWVSS）** 在推理阶段解耦运动生成与外观修复；**类特定先验保持损失** 则作为正则化手段防止过拟合。三个模块协同工作，使得模型仅需单阶段训练、无需额外视频引导，即可同时保留运动生成能力与概念组合能力。

### 空间主题学习模块（Spatial Subject Learning Module, SSLM）

SSLM 的设计动机源于一个关键观察：视频扩散模型（VDM）中的自注意力层对概念组合能力与物体几何形状保持具有重要影响。因此，与仅微调交叉注意力层的现有方法不同，SSLM 在 VDM 空间 Transformer 块的所有注意力层中插入 LoRA 低秩适配器，同时更新交叉注意力层和自注意力层的查询（Q）、键（K）、值（V）投影参数。

LoRA 的前向路径定义为：

$$W = W_0 + \lambda \Delta W = W_0 + \lambda B A$$

其中 $W_0$ 为冻结的原始权重矩阵，$B$ 和 $A$ 为低秩矩阵，$\lambda$ 为控制 LoRA 影响强度的缩放因子。在训练阶段，$\lambda$ 保持为固定值；在推理阶段，该因子则由 DWVSS 动态调控。

训练数据构造极为简洁：将单张目标物体图像重复 $N$ 帧，形成一段“静止视频”，以此驱动 SSLM 学习新主题的外观表征，同时通过文本反转学习一个专用标记 $v^*$ 的嵌入向量来表示该概念。

### 动态加权视频采样策略（Dynamic Weighted Video Sampling Strategy, DWVSS）

DWVSS 是本文最具洞察力的贡献，其核心思想建立在对 VDM 去噪过程阶段性特征的发现之上：**早期去噪步骤主要恢复帧间的整体布局与运动模式，后期步骤则负责精细化物体的外观细节**（Figure 3）。基于这一现象，DWVSS 将推理阶段的去噪过程划分为两个阶段：

- **第一阶段（运动布局修复期，前 $K$ 步）**：将所有 LoRA 模块的权重 $\lambda$ 调整至较小值 $\lambda_s$（默认 0.4），降低 SSLM 对去噪过程的影响，使模型尽可能依赖其固有的运动生成先验。
- **第二阶段（主题外观修复期，第 $K$ 步之后）**：将 $\lambda$ 恢复至较大值 $\lambda_l$（默认 0.8），使 SSLM 充分介入，修复目标的身份细节。

这一策略利用了 SSLM 的“可插拔”特性——LoRA 模块可在推理时通过调整 $\lambda$ 灵活控制其贡献程度，而无需重新训练或引入额外视频引导。默认超参数设定为 $\lambda_s = 0.4$，$\lambda_l = 0.8$，$K = 5$。

### 训练损失函数

总训练目标由两项损失加权组合：

$$\mathcal{L} = \mathcal{L}_{video} + \alpha \mathcal{L}_{pr}$$

其中 $\mathcal{L}_{video}$ 为标准视频扩散重建损失：

$$\mathcal{L}_{video} = \mathbb{E}_{z, c, \epsilon \sim \mathcal{N}(0, \mathrm{I}), t} \left[ \| \epsilon - \epsilon_{\theta}(z_t, c, t) \|_2^2 \right]$$

模型根据文本条件 $c$ 预测添加到潜变量 $z_t$ 中的噪声 $\epsilon$。

$\mathcal{L}_{pr}$ 为类特定先验保持损失：

$$\mathcal{L}_{pr} = \mathbb{E}_{z^{pr}, c^{pr}, \epsilon \sim \mathcal{N}(0, \mathrm{I}), t} \left[ \| \epsilon - \epsilon_{\theta}(z_{t}^{pr}, c^{pr}, t) \|_2^2 \right]$$

该损失项在类别先验数据上计算，用于缓解微调过程中的过拟合，增强生成视频的多样性。超参数 $\alpha$ 控制正则化强度，文中设置为 1.0。

### 模块协同机制

三个模块的协同逻辑可概括为：SSLM 在训练阶段通过扩展微调范围（同时覆盖交叉注意力和自注意力）增强了模型对新主题外观和形状的捕捉能力；先验保持损失防止训练过程中的灾难性遗忘；DWVSS 则在推理阶段通过时间维度的权重调控，将运动生成与外观修复解耦到去噪过程的不同阶段，从而在不牺牲主题保真度的前提下恢复模型的运动生成能力。消融实验（Table 2）定量验证了这一协同的有效性：加入 SSLM 后 CLIP-I 提升至 0.790，DINO-I 提升至 0.631；进一步加入 DWVSS 后 CLIP-T 从 0.310 提升至 0.318，同时保持了较高的外观相似度。

## 实验与分析

### 核心瓶颈与验证

本文要解决的核心瓶颈是：在仅使用静态图像对视频扩散模型（VDM）进行主题定制微调时，模型会遗忘其原有的运动生成能力与概念组合能力。现有恢复方法（如DreamVideo）需要引入额外视频作为引导或重新微调，为用户带来极大不便。CustomCrafter通过两个关键设计——空间主题学习模块（SSLM）与动态加权视频采样策略（DWVSS）——在不引入额外视频的前提下同时提升了主题保真度与运动流畅性。以下从自动指标、人类评估和消融实验三个层面验证该主张。

### 主要定量结果

**Table 1** 给出了在20个定制主题、每个主题10个相关prompt上的自动指标对比。所有方法均基于同一基模型VideoCrafter2复现或适配，其中Custom Diffusion*和DreamVideo*是将原论文训练步数延长后得到的最佳结果，以排除训练步数不一致的干扰。

![[assets/figures/papers/paper_list_l6_CustomCrafter_Customized_Video_Generation_with_Preserving_Motion_and_Con/figures/005_Table_1.jpg]]
*Table 1: Comparison with the existing methods. Note that Custom Diffusion* and DreamVideo* in the table represent the results we get after extending the number of training steps in the original paper*

| 方法 | CLIP-T ↑ | CLIP-I ↑ | DINO-I ↑ | Temporal Consistency ↑ |
|------|----------|----------|----------|------------------------|
| Custom Diffusion | 0.306 | 0.736 | 0.488 | 0.992 |
| Custom Diffusion* | 0.310 | 0.748 | 0.510 | 0.992 |
| DreamVideo | 0.295 | 0.748 | 0.536 | 0.993 |
| DreamVideo* | 0.295 | 0.748 | 0.536 | 0.993 |
| **CustomCrafter (Ours)** | **0.318** | **0.786** | **0.627** | **0.994** |

CustomCrafter在四项指标上全面超越所有基线。其中CLIP-T（文本对齐）达到0.318，相比DreamVideo*的0.295提升+0.023，证明DWVSS策略有效恢复了模型对文本动作描述的运动生成能力。CLIP-I（图像相似度）达到0.786，相比DreamVideo*的0.748提升+0.038，DINO-I（特征相似度）达到0.627，相比DreamVideo*的0.536提升+0.091，表明SSLM在同时微调交叉注意力和自注意力层后，对主题外观和形状的捕捉能力显著增强。时间一致性指标上各方法差异较小（0.992–0.994），说明基模型的帧间连贯性本身较强，但CustomCrafter仍保持了最优水平。

### 用户偏好研究

**Figure 6** 展示了38名参与者对40个视频的主观评估结果。评估维度包括文本对齐（Text Alignment）、主题保真度（Subject Fidelity）、运动流畅性（Motion Fluency）和总体质量。CustomCrafter在所有四个维度上均获得最高的人类偏好得分，且与Custom Diffusion和DreamVideo的差异具有统计显著性。特别是在运动流畅性维度上，CustomCrafter的优势最为突出，直接验证了DWVSS在保留VDM原始运动生成能力方面的有效性。

### 消融实验

**Table 2** 的消融研究定量验证了SSLM和DWVSS各自的独立贡献。以DreamVideo*作为基线（CLIP-I 0.748, DINO-I 0.536, CLIP-T 0.295），仅加入SSLM后，CLIP-I提升至0.790（+0.042），DINO-I提升至0.631（+0.095），证明同时微调自注意力层的Q、K、V参数对主题外观捕捉和形状保持有显著增益。在此基础上进一步加入DWVSS，CLIP-T从0.310提升至0.318（+0.008），同时CLIP-I和DINO-I几乎未下降（0.786和0.627），说明动态加权策略在几乎不损失主题保真度的前提下有效改善了文本对齐和运动质量。

![[assets/figures/papers/paper_list_l6_CustomCrafter_Customized_Video_Generation_with_Preserving_Motion_and_Con/figures/009_Table_2.jpg]]
*Table 2: Ablation Study. “SSLM” is Spatial Subject Learning Module, “DWVSS” is Dynamic Weighted Video Sampling Strategy*

**Figure 7** 的消融可视化进一步从定性角度验证了各组件的预期作用：
- 去除SSLM后，生成视频中的主题外观模糊，或出现概念组合错误（如将“泰迪熊”与错误背景元素混合）。
- 去除DWVSS后，视频运动趋于静止或无法跟随文本中的动作描述（如“跑步”的狗仅呈现静态姿态），证实DWVSS是恢复运动生成能力的关键。

### 因果机制的实验证据

本文的核心因果洞察——VDM去噪的早期阶段恢复运动布局、后期阶段恢复外观细节——通过**Figure 3**的可视化得到直接验证。该图展示了视频去噪过程中不同时间步的中间结果：在早期去噪步骤（t较大时），帧间的整体布局和运动模式已基本形成，但物体外观细节模糊；随着去噪推进到后期步骤（t较小时），物体的纹理、形状等外观细节逐渐清晰。这一阶段性特征为DWVSS的设计提供了理论基础：在早期步骤降低SSLM的LoRA权重（λ_s=0.4），使模型主要依赖原始VDM的运动生成能力；在后期步骤恢复权重（λ_l=0.8），使SSLM介入修复主题外观细节。

### 公平性说明与失败模式

所有对比方法的公平性保障包括：统一基模型VideoCrafter2、扩展训练步数的最佳基线版本（Custom Diffusion*和DreamVideo*）、以及自动指标与人类评估的双重验证。然而，以下局限需要在解读结果时注意：

1. **超参数敏感性**：DWVSS的三个超参数（λ_s=0.4, λ_l=0.8, K=5）为经验设定，对不同运动复杂度或视频长度的自适应性未经验证。在实际应用中，用户可能需要手动调整这些参数以获得最佳效果。
2. **基模型泛化性**：当前实验仅在VideoCrafter2上验证，该模型基于空间transformer架构。对于其他VDM架构（如基于U-Net或DiT的模型），去噪阶段的运动-外观解耦特性是否依然成立、SSLM和DWVSS是否可直接迁移，尚需进一步实验。
3. **数据规模与多样性**：测试集包含20个主题和10个相关prompt，对于极端主体外形（如高度变形的卡通角色）或复杂交互场景（如多主体物理交互）的泛化能力未充分评估。
4. **长视频与大幅运动**：对于分钟级长视频或非常大运动幅度的场景，去噪过程的阶段性特征是否依然保持、动态加权策略是否需要调整，论文未给出实验证据。

## 方法谱系与知识库定位

### 1. 问题定位：定制微调中的能力遗忘

在视频扩散模型（VDM）上进行主题定制（Subject Customization）时，一个核心瓶颈是灾难性遗忘：当仅使用单张或少量静态图像对VDM进行微调后，模型虽然能记住目标的外观，却会丧失其原本预训练获得的**运动生成能力**与**概念组合能力**（如“一只泰迪熊在滑雪”中“泰迪熊”与“滑雪”的正确组合）。现有方法为恢复这些能力，往往需要引入额外的视频作为运动引导（如 **DreamVideo**，Wei et al., CVPR 2024），或进行多阶段重新微调，这为用户带来了显著的数据采集与计算负担。CustomCrafter 的核心目标是在不依赖额外视频、仅需单阶段训练的约束下，同时保持主题保真度、运动流畅性与概念组合正确性。

### 2. 与基线工作的关系

#### 2.1 图像定制方法的视频化延伸：Custom Diffusion

**Custom Diffusion**（Kumari et al., CVPR 2023）是图像定制领域的代表性方法，其核心在于仅微调文本到图像扩散模型中交叉注意力层的 Key 和 Value 投影矩阵，以学习新概念。当该方法被直接复现并应用于视频基模型 VideoCrafter2 时（记为 Custom Diffusion*），其局限性暴露：仅更新交叉注意力不足以捕捉目标的精确几何形状，且在视频生成中无法保持运动生成能力。CustomCrafter 在此基础上将微调范围从交叉注意力扩展至**自注意力层**，并同时更新 Query、Key、Value 三个投影，构成了空间主题学习模块（SSLM），从而显著提升了形状保持与概念组合能力。

#### 2.2 视频定制方法的对比：DreamVideo

**DreamVideo**（Wei et al., CVPR 2024）是专门针对视频定制设计的方法，其将主题学习与运动学习解耦为两个独立模块，但运动学习模块需要额外的目标运动视频作为引导。为公平对比，CustomCrafter 仅复现了 DreamVideo 的主题学习部分（记为 DreamVideo*），并在此基础上扩展训练步数以获得其最佳结果。实验表明，即使 DreamVideo* 在扩展训练后，其 CLIP-I（0.748）和 DINO-I（0.536）仍显著低于 CustomCrafter（0.786 和 0.627），且概念组合错误率更高。CustomCrafter 的优势在于通过 SSLM 和动态加权视频采样策略（DWVSS），在**无需运动视频引导**的前提下实现了更好的主题-运动联合生成。

### 3. 方法谱系中的核心创新定位

CustomCrafter 在方法谱系中的独特贡献可归纳为两个层面的创新：

**（1）微调参数范围的结构性扩展。** 在图像定制领域，从 Textual Inversion（仅学习词嵌入）到 Custom Diffusion（微调交叉注意力 KV）再到 DreamBooth（全模型微调），参数更新范围逐步扩大。CustomCrafter 在视频定制场景下提出了一个关键观察：**自注意力层对概念组合能力与几何形状保持至关重要**。因此，SSLM 在空间 Transformer 的所有注意力层（交叉注意力与自注意力）中插入 LoRA 适配器，更新 Q、K、V 参数。这一设计在 Table 2 的消融中得到验证：加入 SSLM 后 CLIP-I 从 0.748 提升至 0.790，DINO-I 从 0.536 提升至 0.631。

**（2）推理阶段运动-外观解耦的动态控制。** 这是 CustomCrafter 最具原创性的贡献。通过可视化 VDM 的去噪过程（Figure 3），作者首次发现并利用了去噪阶段的**功能分化**：早期步骤（前若干步）主要恢复帧间的整体布局与运动模式，后期步骤则精细化物体的外观细节。基于此洞察，DWVSS 在推理时动态调整所有 LoRA 模块的权重 λ：在前 K 步使用较小的 λ_s（默认 0.4），降低主题学习模块对运动生成的影响；在后续步骤恢复至较大的 λ_l（默认 0.8），以修复主题外观。这一策略将 CLIP-T 文本对齐分数从 0.310 提升至 0.318，并在用户研究中使运动流畅性显著优于所有对比方法。

### 4. 适用边界与局限

尽管 CustomCrafter 在设定的基准上表现出色，其适用边界与局限值得明确：

- **超参数敏感性**：DWVSS 依赖三个手动设定的超参数——小权重 λ_s、大权重 λ_l 以及分界步数 K。当前默认值（λ_s=0.4, λ_l=0.8, K=5）基于经验选择，缺乏对不同视频内容、运动复杂度或文本条件的自适应机制。在极端运动幅度或复杂场景下，这些参数可能需要重新调整，否则可能导致运动不充分或外观模糊。
- **基模型依赖性**：所有实验均基于单一基模型 VideoCrafter2 进行。该模型采用空间-时间分离的 Transformer 架构，而 DWVSS 的运动-外观解耦假设是否在其他 VDM 架构（如基于 3D U-Net 或全 DiT 的模型）上成立，尚未得到验证。
- **数据集规模与多样性**：实验涵盖 20 个定制主题，每个主题 10 个相关 prompt，总计 200 个测试用例。对于更极端的主体外形（如高度非刚性物体）、复杂多主体交互或长时序生成（如分钟级视频），方法的泛化性未充分评估。
- **多主体定制的缺失**：当前方法仅支持单主体定制。当需要同时定制多个主体并保持其间的空间-语义交互一致性时，SSLM 和 DWVSS 的扩展方案尚不明确。

### 5. 开放问题

1. **自适应阶段切换**：去噪过程的“转折点”K 目前依赖固定经验值。是否可以设计基于模型内部特征（如注意力图变化率、潜变量梯度）的在线判据，实现自适应的阶段切换？这将消除关键的超参数调优负担。
2. **跨任务泛化**：运动-外观解耦的核心洞察——VDM 去噪早期恢复结构/运动、后期恢复纹理/外观——能否推广到其他生成任务？例如，在文本到图像编辑中，是否可以通过类似的分阶段加权策略实现无需额外掩码引导的局部编辑？
3. **多主体与交互一致性**：当扩展到多主体定制时，各主体的 LoRA 模块之间如何协调？不同主体的 λ 调度是否需要独立控制？主体间的遮挡、交互等空间关系如何保证一致性？
4. **长时序生成的稳定性**：在生成长达数分钟的视频时，去噪过程的阶段性特征是否依然保持？DWVSS 的固定 K 值是否需要随视频长度动态缩放？运动生成能力在长时序下是否会逐渐退化？
5. **与运动定制方法的融合**：当前方法聚焦于保留模型的通用运动生成能力。若用户希望同时定制特定的运动模式（如“特定人跳舞的方式”），SSLM+DWVSS 框架能否与 DreamVideo 的运动学习模块兼容，形成统一的主题-运动联合定制方案？

## 原文 PDF

![[paperPDFs/arxiv_2024/CustomCrafter_Customized_Video_Generation_with_Preserving_Motion_and_Concept_Composition_Abilities.pdf]]
