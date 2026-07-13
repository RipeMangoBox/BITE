---
title: "COME: Advancing Representation Learning and Generative Modeling for High-Quality Text-to-Motion Generation"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/COME_Advancing_Representation_Learning_and_Generative_Modeling_for_High_Quality_Text_to_Motion_Generation.pdf
project_link: null
code_link: null
aliases:
- CCMD
- COME
tags:
- ICLR_2026
- topic/motion_animation
- topic/motion_animation/human_motion_generation
core_operator: "通过增强运动表示的区分性（非对称架构 + 掩码运动建模 + 对比学习）和优化扩散训练策略（联合全局/细粒度语义注入 + Stable-Min-SNR-γ 协调训练推理不匹配与梯度冲突），直接提升连续扩散框架的生成质量和效率。"
primary_logic: "连续扩散模型在T2M上的潜力被低质量运动表示和训练策略所掩盖；通过为扩散过程提供一个具有高鉴别力且覆盖广泛运动空间的潜在表示，并稳定其训练动态，可以让连续扩散框架重新超越离散方案，同时保留其在语义控制、组合泛化和多样性采样上的天然优势。"
claims:
- "连续模型的潜在特征拥挤、不可分，阻碍去噪：相比VQ-VAE/RVQ-VAE，标准VAE表示的可分性最差。"
- "MoCMAE在FID/MPJPE重建指标上远优于所有对比tokenizer，同时在下游生成任务中带来直接增益。"
- "ccDIT的Stable-Min-SNR-γ消融证实解决训练-推理不匹配和梯度冲突对生成质量至关重要。"
- "引入全局和细粒度语义控制（AdaLN-Zero + cross-attention）对于文本对齐不可或缺。"
---

# COME: Advancing Representation Learning and Generative Modeling for High-Quality Text-to-Motion Generation

> [!tip] 核心洞察
> 连续扩散模型在T2M上的潜力被低质量运动表示和训练策略所掩盖；通过为扩散过程提供一个具有高鉴别力且覆盖广泛运动空间的潜在表示，并稳定其训练动态，可以让连续扩散框架重新超越离散方案，同时保留其在语义控制、组合泛化和多样性采样上的天然优势。

| 字段 | 内容 |
|------|------|
| 中文题名 | COME：提升文本到运动生成的表示学习与生成建模 |
| 英文题名 | COME: Advancing Representation Learning and Generative Modeling for High-Quality Text-to-Motion Generation |
| 会议/期刊 | ICLR 2026 |
| Links |  |
| Topic | #topic/motion_animation #topic/motion_animation/human_motion_generation |
| Method | COME (Continuous Motion Diffusion) |
| Dataset | HumanML3D, KIT-ML |

> [!tip] 效果简介
> - HumanML3D 上，FID↓ 为 0.041±.002，对比 0.103±.004 (ReMoDiffuse) / 0.045±.002 (MoMask)，变化 相比ReMoDiffuse降低0.062；相比MoMask降低0.004。
> - HumanML3D 上，R Precision Top1↑ 为 0.510±.005，对比 0.510±.005 (ReMoDiffuse) / 0.521±.002 (MoMask)，变化 与ReMoDiffuse并列第一；略低于MoMask（-0.011）。
> - HumanML3D 上，MM-Dist↓ 为 2.974±.016，对比 2.974±.016 (ReMoDiffuse) / 2.958±.008 (MoMask)，变化 与ReMoDiffuse并列最佳；非常接近MoMask。

## 概要

**问题瓶颈**：文本到运动（Text-to-Motion, T2M）生成领域，连续扩散模型在生成质量上长期落后于离散方法（如基于VQ-VAE/RVQ-VAE的MoMask、T2M-GPT等）。根本原因并非扩散框架本身的能力不足，而在于两个被忽视的系统性缺陷——**(1) 运动表示质量低下**：标准VAE编码的连续潜在特征拥挤且不可分，缺乏样本间鉴别能力，直接阻碍扩散模型的去噪过程（见Tab. 7, Figs. 6, 5）；**(2) 扩散训练策略次优**：存在训练-推理不匹配与不同时间步的梯度冲突，进一步损害生成质量。

**核心方案**：**COME**（Continuous Motion Diffusion）从表示学习与生成建模两个维度同时切入，让连续扩散框架重新超越离散方案。COME由两大组件构成：

- **MoCMAE**（Motion Contrastive Masked Autoencoder）：非对称CNN+Transformer编码器与轻量CNN解码器，结合掩码运动建模与对比学习，构建具有高鉴别力且覆盖广泛运动空间的连续潜在表示。
- **ccDIT**（Cross-Condition Diffusion Transformer）：在MoCMAE潜在空间中通过AdaLN-Zero注入句级语义、Cross-Attention注入词级语义，配合U型跳跃连接实现细粒度文本控制。
- **Stable-Min-SNR-γ**：统一Zero-SNR与Min-SNR-γ的稳定化信噪比重加权策略，协调训练-推理不匹配与跨时间步梯度冲突。

**主要结果**：在HumanML3D基准上，COME取得FID **0.041**（超越此前最佳连续方法ReMoDiffuse的0.103和离散SOTA MoMask的0.045），R-Precision Top1 **0.510**与ReMoDiffuse并列第一，MM-Dist **2.974**并列最佳。在KIT-ML上同样取得FID **0.189**和R-Precision Top1 **0.443**的全面领先。推理效率方面，在统一10步DPM-Solver++采样下达到**0.022s**的最快推理速度，训练仅需**1,100轮**（对比MLD的9,000轮），实现质量与效率的双重突破。

### 问题域与核心矛盾

文本到运动生成（Text-to-Motion, T2M）旨在根据自然语言描述合成逼真的人体运动序列，在动画制作、虚拟现实和人机交互等领域具有广泛的应用前景。近年来，扩散模型在该领域取得了显著进展，但其技术路线呈现出明显的分化：**离散方法**（如基于VQ-VAE/RVQ-VAE的tokenizer配合掩码Transformer或自回归模型）在生成质量上长期占据领先地位，而**连续扩散方法**虽然在语义控制、组合泛化和多样性采样方面具有天然优势，却始终未能在核心指标上实现超越。

这一“连续不如离散”的现象构成了该领域的核心矛盾。COME的作者将其归因于两个相互耦合的瓶颈：

**瓶颈一：运动表示质量不足**。连续扩散模型通常依赖标准VAE将运动序列压缩到低维潜在空间，然后在该空间中进行扩散生成。然而，这种VAE编码产生的潜在特征存在严重的**拥挤和不可分性**（poorly separated and entangled），不同运动样本的特征在空间中高度重叠，缺乏样本间的鉴别能力。这直接阻碍了扩散模型的去噪过程——当潜在空间中不同运动的边界模糊时，模型难以从噪声中精确恢复出目标运动。相比之下，离散方法使用的VQ-VAE或RVQ-VAE通过向量量化的离散瓶颈天然地增强了表示的区分性（参见Tab. 7、Fig. 5和Fig. 6的聚类指标与t-SNE可视化对比）。

**瓶颈二：扩散训练策略次优**。即使获得了较好的运动表示，连续扩散模型的训练过程本身也存在两个关键问题：（1）**训练-推理不匹配**——标准扩散训练在中间时间步的信噪比（SNR）条件下进行，但推理时最终时间步的SNR趋近于零，这种不一致导致模型在推理阶段的行为偏离训练分布；（2）**不同时间步的梯度冲突**——不同噪声水平的时间步对损失函数的贡献差异巨大，高SNR步（低噪声）和低SNR步（高噪声）的梯度幅度不均衡，导致优化过程被某些时间步主导，损害整体生成质量。

### 现有方法的缺口

在COME提出之前，连续扩散方法的发展主要沿着两条路径：

- **表示层面**：大多数方法直接沿用了标准VAE架构（如**MLD**，Chen et al., ICCV 2023），或干脆放弃潜在空间直接在原始运动数据上扩散（如**MDM**，Tevet et al., ICLR 2022）。这些方法未针对运动数据的时空特性进行专门的表示学习设计，导致潜在空间的结构化程度和鉴别力不足。

- **训练层面**：现有工作或采用标准MSE损失（无SNR重加权），或仅引入Zero-SNR、Min-SNR-γ等单一策略来部分缓解训练问题，但缺乏一个统一的框架来同时解决训练-推理不匹配和跨时间步梯度冲突。例如，**MotionLCM**（Dai et al., CVPR 2025）通过一致性模型加速采样，但生成质量（FID 0.467）远低于同期离散方法；**ReMoDiffuse**（Zhang et al., ICCV 2023）引入检索增强机制，但仍未从根本上解决表示质量和训练动态的问题。

离散方法的SOTA代表**MoMask**（Guo et al., ECCV 2024）和**T2M-GPT**（Zhang et al., CVPR 2023）通过RVQ-VAE的多层离散编码和掩码Transformer的生成范式，在HumanML3D上实现了FID 0.045和0.116的优异表现，进一步拉大了与连续方法的差距。但离散方法本身存在固有的局限性：向量量化的离散瓶颈限制了表示的细粒度表达能力，且离散token的采样过程在多样性和可控性上不如连续扩散灵活。

### 本文动机与核心洞察

COME的核心洞察在于：**连续扩散模型在T2M上的潜力被低质量的运动表示和次优的训练策略所掩盖**。如果能够为扩散过程提供一个具有高鉴别力且覆盖广泛运动空间的连续潜在表示，并稳定其训练动态以消除训练-推理不匹配和梯度冲突，连续扩散框架完全有能力重新超越离散方案，同时保留其在语义控制、组合泛化和多样性采样上的天然优势。

基于这一洞察，COME从两个维度进行系统性改进：

1. **运动表示层面**：设计**MoCMAE**（Motion Contrastive Masked Autoencoder）——一种非对称的连续运动tokenizer，通过CNN+Transformer混合编码器捕获局部运动模式和长程时空依赖，结合掩码运动建模（Masked Motion Modeling）增强编码器对关键时空模式的捕获能力，并引入对比学习（Contrastive Learning）显式提升样本间特征的可分性。同时采用轻量级CNN解码器避免额外的解码开销。

2. **扩散训练层面**：提出**ccDIT**（Cross-Condition Diffusion Transformer）和**Stable-Min-SNR-γ**训练策略。ccDIT通过AdaLN-Zero注入全局句级语义、通过Cross-Attention注入细粒度词级语义，实现文本条件的多层次融合；Stable-Min-SNR-γ则统一了Zero-SNR和Min-SNR-γ机制，在强制最终时间步SNR=0以消除训练-推理不匹配的同时，通过稳定化的SNR权重（引入常数φ避免除零）协调不同时间步的梯度贡献，解决梯度冲突问题。

## 核心方法与创新机理

COME 的核心贡献并非提出一种全新的生成范式，而是通过**系统性地重塑连续扩散框架的两个关键环节**——运动表示学习与扩散训练策略——使其在文本到运动生成（T2M）任务上首次全面超越离散方法。具体而言，该工作识别并解决了连续扩散模型长期受困的两个瓶颈：

1.  **运动表示质量低下**：标准 VAE 编码的连续潜在特征拥挤、不可分（§1），缺乏样本间的鉴别能力，直接阻碍扩散模型的去噪过程。
2.  **扩散训练策略次优**：存在训练-推理不匹配（信噪比调度在最终时间步未归零）以及不同时间步梯度冲突的问题，进一步损害生成质量。

围绕上述瓶颈，COME 引入了三个紧密耦合的“变更槽位”（changed slots），构成了其核心创新体系。

### 1. 高鉴别力运动表示学习：MoCMAE

MoCMAE 替代了传统的标准 VAE 或离散 VQ-VAE/RVQ-VAE，作为连续运动 tokenizer。其创新体现在非对称架构与双重学习目标的组合：

*   **非对称混合编码器**：采用 CNN 提取局部运动模式，结合 Transformer 块进行长程时空建模，而解码器保持轻量级（纯 CNN），避免引入额外的解码开销（§4.1，Figure 1(a)）。
*   **掩码运动建模（MMM）**：通过对输入运动序列施加高比例随机掩码（50% 掩码比获得全局最优），迫使编码器学习鲁棒的上下文推理能力。
*   **对比学习（CL）**：引入对比损失 $\mathcal{L}_{\mathrm{contrast}}$，拉近同一运动的完整版本与掩码版本的特征，同时推开不同样本的特征，显式增强潜在空间的可分性。

这一设计带来的因果效应是显著的：MoCMAE 在重建指标（FID 0.002 / MPJPE 8.8，HumanML3D）上远超所有对比 tokenizer（Table 2），其潜在表示在 Silhouette Score、Davies-Bouldin Index 和 5-NN 准确率等聚类质量指标上均达到最优（Table 18），为下游扩散模型提供了高质量、结构化的生成空间。

### 2. 双重语义注入的扩散骨干：ccDIT

ccDIT 替代了标准 DiT 或基于 MLP 的扩散骨干，其创新在于将文本条件分解为全局与细粒度两个层次，并通过不同机制注入扩散 Transformer：

*   **句级语义（AdaLN-Zero）**：通过自适应层归一化（AdaLN-Zero）将全局句子嵌入注入每一层，控制生成运动的整体语义倾向。
*   **词级语义（Cross-Attention）**：在 Transformer 层中插入交叉注意力模块，使模型能够关注文本中的细粒度词汇（如“踢”、“跳跃”），实现精确的动作-文本对齐。
*   **U 型跳跃连接**：引入类似 U-DiT 的跳跃连接，促进不同尺度特征融合。

消融实验（Table 5）揭示了这一设计的因果链路：移除句级语义使 FID 从 0.041 骤升至 0.076，R-Precision Top1 从 0.526 降至 0.508；移除词级语义则使 FID 升至 0.089，Top1 降至 0.504。这表明**全局与细粒度语义的联合注入对于高保真文本对齐是不可或缺的**。

### 3. 协调训练动态的损失策略：Stable-Min-SNR-γ

Stable-Min-SNR-γ 统一了 Zero-SNR 与 Min-SNR-γ 两种训练策略，解决了此前方法无法兼顾的两个问题：

*   **训练-推理不匹配**：通过强制最终时间步 SNR=0（Zero-SNR），使训练时的噪声分布与推理时的纯噪声初始状态一致。
*   **梯度冲突**：采用 Min-SNR-γ 策略对不同时间步的损失进行重加权，抑制高 SNR 步的梯度主导效应。
*   **数值稳定性**：引入稳定化项 $\phi$，避免 SNR=0 时的除零错误，权重公式为：
    $$w_{t} = \frac{\min\{\mathrm{SNR}(t),\gamma\}}{\mathrm{SNR}(t)+\phi}$$

该策略的因果效应在 Table 5 中得到充分验证：从基础 DiT 骨干（FID 0.703）到完整模型（FID 0.041±.002）的巨大性能跃升，很大程度上归功于 Stable-Min-SNR-γ 与 Zero-SNR 的组合应用。

### 创新逻辑链

三个变更槽位形成了一条清晰的因果链：**MoCMAE 提供高鉴别力、覆盖广泛的连续潜在空间 → ccDIT 在此空间中通过双重语义注入进行精细控制 → Stable-Min-SNR-γ 确保扩散训练过程的稳定与一致**。这一组合使连续扩散框架在保留语义控制、组合泛化和多样性采样等天然优势的同时，在 FID 等核心生成质量指标上超越离散 SOTA 方法（如 MoMask），并在 KIT-ML 上取得 R-Precision Top1 的显著领先（0.443 vs. 最佳基线 0.424）。

COME 的整体 pipeline 是一个两阶段的连续扩散生成框架。其核心设计逻辑是：**先构建一个具有高鉴别力且覆盖广泛运动空间的连续潜在表示，再在该潜在空间中进行条件扩散生成**。这一设计直接回应了连续扩散模型在文本到运动生成中长期落后于离散方法的两大瓶颈——运动表示拥挤不可分、扩散训练策略次优。

### 框架总览

如图 1 所示，COME 由两个主要模块串联构成：

1. **MoCMAE（Motion Contrastive Masked Autoencoder）**：连续运动 tokenizer，负责将原始运动序列映射到结构化、高鉴别力的潜在空间，并在推理时将生成的潜在表示解码回运动序列。
2. **ccDIT（Cross-Condition Diffusion Transformer）**：条件扩散模型，在 MoCMAE 构建的潜在空间中，以文本描述为条件，通过迭代去噪生成运动潜在表示。

输入输出流如下：文本描述 → ccDIT（在潜在空间中迭代生成）→ MoCMAE 解码器 → 运动序列。训练时，MoCMAE 和 ccDIT 分别独立训练；推理时，二者串联使用。

### 模块关系与设计动机

框架的两个模块各自针对连续扩散模型的一个根本缺陷：

- **MoCMAE 解决表示质量问题**：标准 VAE 编码的潜在特征拥挤且不可分（见 Tab. 7、Fig. 5、Fig. 6 的聚类指标和 t-SNE 可视化），不同样本的表示纠缠在一起，阻碍扩散模型的去噪过程。MoCMAE 通过非对称编码器-解码器架构、掩码运动建模和对比学习，显著提升表示的可分性（Silhouette Score、5-NN 准确率最优，Davies-Bouldin Index 最低），为下游扩散生成提供高质量的潜在空间。

- **ccDIT 解决训练策略问题**：传统扩散模型存在训练-推理不匹配（训练时 SNR 非零，推理时从纯噪声开始）和不同时间步的梯度冲突。ccDIT 通过 Stable-Min-SNR-γ 损失重加权策略统一 Zero-SNR 与 Min-SNR-γ，同时注入全局句级语义（AdaLN-Zero）和细粒度词级语义（Cross-Attention），确保文本条件被充分且稳定地利用。

### 关键公式与训练目标

MoCMAE 的总损失为重建损失与对比损失的加权和：

$$
\mathcal{L}_{\mathrm{MoCMAE}} = \mathcal{L}_{\mathrm{rec}} + \lambda \mathcal{L}_{\mathrm{contrast}}
$$

其中重建损失 $\mathcal{L}_{\mathrm{rec}}$ 采用平滑 L1 损失加速度正则化项，增强时序连贯性；对比损失 $\mathcal{L}_{\mathrm{contrast}}$ 拉近同一运动完整版本与掩码版本的特征，推开不同样本的特征。

ccDIT 的训练目标为 SNR 加权的 MSE 损失：

$$
\mathcal{L}_{\mathrm{ccDIT}} = w_{t} \cdot \mathcal{L}_{\mathrm{mse}}, \quad w_{t} = \frac{\min\{\mathrm{SNR}(t),\gamma\}}{\mathrm{SNR}(t)+\phi}
$$

其中 $w_t$ 为 Stable-Min-SNR-γ 权重，通过引入小常数 $\phi$ 避免 SNR=0 时的除零错误，同时强制最终时间步 SNR=0 以消除训练-推理不匹配。

### 推理流程

推理时，ccDIT 从纯噪声出发，在文本条件引导下通过 DPM-Solver++ 高阶求解器进行快速采样（默认 10 步），生成潜在表示；随后 MoCMAE 的解码器将该潜在表示解码为最终的运动序列。训练时以 10% 概率随机丢弃文本条件，推理时使用 Classifier-Free Guidance 组合条件与无条件预测，进一步提升文本对齐质量。

![[assets/figures/papers/paper_list_l14_COME_Advancing_Representation_Learning_and_Generative_Modeling_for_High/figures/001_Figure_1.jpg]]
*Figure 1: Overview of COME. It consists of: (a) MoCMAE, an asymmetric hybrid model to extract high-quality motion features without introducing additional decoding overhead; and (b) ccDIT, a conditional diffusion model that captures both global sentence-level semantics and fine-grained word-level cues to generate high-quality motion sequences*

COME 框架由两大核心模块构成：**MoCMAE**（Motion Contrastive Masked Autoencoder）负责学习高鉴别力的连续运动表示，**ccDIT**（Cross-Condition Diffusion Transformer）在该潜在空间中进行条件扩散生成。两者通过一个统一的训练策略 **Stable-Min-SNR-γ** 协同优化，形成端到端的高质量文本驱动运动生成管线。

### MoCMAE：掩码对比运动自编码器

MoCMAE 的核心设计目标是构建一个**结构化且具有高样本间可分性**的连续潜在空间，以克服标准 VAE 表示拥挤、不可分的瓶颈（§4.1）。

**非对称编码器-解码器架构**：编码器采用 CNN 与 Transformer 的混合结构——CNN 层负责提取局部运动模式，Transformer 块负责长程时空关系建模；解码器则保持轻量化的纯 CNN 设计，以避免引入额外的解码开销。这种非对称设计使得编码器能充分捕获运动的全局语义，而解码器仅需从高质量潜在表示中重建运动序列。

**掩码运动建模（MMM）**：在训练阶段，对输入运动序列 $`\mathbf{X}`$ 施加随机掩码，编码器仅处理可见部分，解码器需从掩码后的潜在表示重建完整运动。这一机制强制编码器学习运动的全局结构与语义先验，而非简单记忆局部模式。

**对比学习（CL）**：引入对比损失，将同一运动的完整版本特征 $`\bar{Z}_f`$ 与掩码版本特征 $`\bar{Z}_m`$ 拉近，同时推开不同样本的特征：

$$`\mathcal{L}_{\mathrm{contrast}} = -\frac{1}{N}\sum_{i=1}^{N}\log\frac{\exp(\sin(\bar{Z}_{m}^{i},\bar{Z}_{f}^{i})/\tau)}{\sum_{j=1}^{N}\exp(\sin(\bar{Z}_{m}^{i},\bar{Z}_{f}^{j})/\tau)}`$$

其中 $`\sin(\cdot,\cdot)`$ 为余弦相似度，$`\tau`$ 为温度系数。该损失直接增强潜在空间中样本间的鉴别能力，是 MoCMAE 超越 VQ-VAE/RVQ-VAE 表示质量的关键。

**重建损失**：采用平滑 L1 损失与速度正则化项的组合，保证时序连贯性：

$$`\mathcal{L}_{\mathrm{rec}} = \mathcal{L}_{1}^{\mathrm{smooth}}(\mathbf{X}, \mathbf{X}_{\mathrm{rec}}) + \alpha \mathcal{L}_{1}^{\mathrm{smooth}}(V(\mathbf{X}), V(\mathbf{X}_{\mathrm{rec}}))`$$

其中 $`V(\cdot)`$ 为速度算子（相邻帧差分），$`\alpha`$ 为速度损失权重。

**总目标**：

$$`\mathcal{L}_{\mathrm{MoCMAE}} = \mathcal{L}_{\mathrm{rec}} + \lambda \mathcal{L}_{\mathrm{contrast}}`$$

$`\lambda`$ 控制对比损失的贡献。消融实验证实，50% 掩码比获得全局最优重建（FID 0.002 / MPJPE 8.8），移除对比学习使生成 FID 从 0.041 退至 0.058（Table 4）。

### ccDIT：交叉条件扩散 Transformer

ccDIT 在 MoCMAE 的潜在空间中执行条件去噪，其核心创新在于**同时注入全局句级语义与细粒度词级语义**，实现精准的文本-运动对齐（§4.2）。

**句级语义注入（AdaLN-Zero）**：将 CLIP 文本编码器提取的句级嵌入通过 AdaLN-Zero 机制注入每个 Transformer 块的归一化层，调节缩放与偏移参数。AdaLN-Zero 初始化时将所有调制参数置零，使模型从恒等映射开始学习，提升训练稳定性。

**词级语义注入（Cross-Attention）**：在 Transformer 块中引入交叉注意力层，以潜在运动特征为 Query，词级文本嵌入为 Key/Value，实现对细粒度语义（如“高踢”、“跳起挥手”）的精确捕获。消融实验表明，移除词级语义导致 FID 从 0.041 升至 0.089，R-Precision Top1 降至 0.504（Table 5）。

**U 型跳跃连接**：借鉴 U-DiT 的设计，在 Transformer 层间引入跳跃连接，促进不同尺度特征的融合，加速收敛。

### Stable-Min-SNR-γ：统一训练策略

扩散模型的训练存在两个核心问题：**训练-推理不匹配**（训练时最终时间步 SNR 不为零，推理时从纯噪声开始）与**不同时间步的梯度冲突**（高 SNR 步与低 SNR 步的损失尺度差异悬殊）。COME 提出 Stable-Min-SNR-γ 统一解决这两个问题（§4.3）。

**Zero-SNR 策略**：强制最终时间步 $`t=T`$ 的信噪比 $`\mathrm{SNR}(T)=0`$，使训练与推理的初始分布一致，消除训练-推理不匹配。

**稳定化 SNR 加权**：在 Min-SNR-γ 的基础上引入稳定项 $`\phi`$，避免 $`\mathrm{SNR}(t)=0`$ 时的除零错误：

$$`w_{t} = \frac{\min\{\mathrm{SNR}(t),\gamma\}}{\mathrm{SNR}(t)+\phi}`$$

其中 $`\gamma`$ 为 SNR 截断阈值（防止低 SNR 步主导梯度），$`\phi`$ 为小正常数（如 $`10^{-8}`$）。该权重同时实现了：(1) 限制高噪声步的损失贡献，缓解梯度冲突；(2) 在 $`\mathrm{SNR}(t)=0`$ 时保持数值稳定。

**ccDIT 训练目标**：

$$`\mathcal{L}_{\mathrm{ccDIT}} = w_{t} \cdot \mathcal{L}_{\mathrm{mse}}`$$

$`\mathcal{L}_{\mathrm{mse}}`$ 为预测噪声与真实噪声的标准均方误差。消融实验证实，Stable-Min-SNR-γ + Zero-SNR 的组合使 FID 从基础 DiT 的 0.703 降至 0.041（Table 5），是性能提升的核心驱动力之一。

### 推理：分类器自由引导与高效采样

推理时采用 **Classifier-Free Guidance (CFG)**：训练时以 10% 概率将文本条件 $`c`$ 置为空 $`\emptyset`$，推理时组合条件预测与无条件预测：

$$`\hat{\epsilon}_\theta(\mathbf{x}_t, c) = \epsilon_\theta(\mathbf{x}_t, \emptyset) + s \cdot (\epsilon_\theta(\mathbf{x}_t, c) - \epsilon_\theta(\mathbf{x}_t, \emptyset))`$$

其中 $`s`$ 为引导强度。结合 **DPM-Solver++** 高阶快速采样器，COME 可在 10 步内完成高质量生成，在保持生成质量的同时实现高效推理（§4.4）。

## 实验与关键发现

### 核心性能对比

COME在HumanML3D基准上取得了最优的FID（0.041±.002），显著优于连续扩散方法**ReMoDiffuse**（0.103±.004）和离散方法**MoMask**（0.045±.002）。在R-Precision Top1上，COME达到0.510±.005，与**ReMoDiffuse**并列第一，略低于**MoMask**（0.521±.002）；在MM-Dist上达到2.974±.016，同样与**ReMoDiffuse**并列最佳，极接近**MoMask**（2.958±.008）。这些结果证实了连续扩散框架在获得高质量表示和优化训练策略后，可以在生成保真度上全面超越或比肩最先进的离散方案。

在KIT-ML基准上，COME表现更为突出：FID为0.189±.018，显著低于此前最佳的连续方法**Fg-T2M**（0.243±.019）和离散方法**CoMo**（0.262±.004）；R-Precision Top1达到0.443±.012，远超所有对比基线（**Fg-T2M**为0.424±.006，**MoMask**为0.363±.005）。这一跨数据集的优势表明COME的表示学习和训练策略具有良好的泛化性。

### 运动表示质量分析

MoCMAE作为连续运动tokenizer，在重建任务上展现出压倒性优势：HumanML3D上的重建FID仅为0.002，MPJPE为8.8，远超所有对比方法（Table 2）。这一重建精度直接转化为下游生成任务的增益——使用MoCMAE表示的生成FID达到0.041±.002，而使用标准VAE表示的基线（如**MLD**）则显著落后。

![[assets/figures/papers/paper_list_l14_COME_Advancing_Representation_Learning_and_Generative_Modeling_for_High/figures/003_Table_2.jpg]]
*Table 2: Evaluation of motion tokenizer. Red face indicates the best result*

从表示空间的结构化程度来看，MoCMAE在所有聚类质量指标上均最优（Table 7）：Silhouette Score（SC）、Calinski-Harabasz Index（CHI）、Davies-Bouldin Index（DBI）和5-NN准确率均优于VQ-VAE、RVQ-VAE等离散tokenizer。t-SNE可视化（Figure 5, Figure 6）进一步证实，MoCMAE的潜在特征具有更好的类间可分性和空间覆盖性，这直接缓解了连续扩散模型中“拥挤不可分表示阻碍去噪”的核心瓶颈。

![[assets/figures/papers/paper_list_l14_COME_Advancing_Representation_Learning_and_Generative_Modeling_for_High/figures/011_Table_7.jpg]]
*Table 7: Quantitative comparison of motion representations. MoCMAE outperforms existing encoders on both geometric metrics (SC, CHI, DBI) and semantic alignment (5-NN Acc). Human motion categories naturally overlap, so absolute SC values are low; nonetheless, MoCMAE achieves the best separability and semantic coherence*

### 消融实验：MoCMAE组件的因果贡献

Table 4的消融实验揭示了MoCMAE各设计要素的因果效应：

- **Transformer块的移除**导致重建MPJPE从8.8升至13.8，生成FID从0.041退至0.068，证实长程时空建模对表示质量至关重要。
- **对比学习的移除**使生成FID从0.041退至0.058，MM-Dist从2.898升至2.974，表明对比目标通过增强样本间可分性直接提升了扩散模型的去噪效率。
- **掩码比例**在50%时获得全局最优：重建FID 0.002 / MPJPE 8.8，生成FID 0.041±.002。过高或过低的掩码比例均会损害表示质量，50%的掩码率在重建难度和对比学习信号之间实现了最佳平衡。

### 消融实验：ccDIT条件注入与训练策略

Table 5的消融量化了ccDIT中条件注入和训练策略的贡献：

- **句级语义移除**（w/o sentence）导致FID从0.041升至0.076，R-Prec Top1从0.526降至0.508，证明全局语义控制对生成质量不可或缺。
- **词级语义移除**（w/o word）导致FID升至0.089，R-Prec Top1降至0.504，表明细粒度词级线索对文本对齐同样关键，且其缺失比句级语义缺失的损害更大。
- **训练策略的累积效应**极为显著：从基础DiT骨干（FID 0.703±.011）逐步加入Zero-SNR和Stable-Min-SNR-γ后，FID最终降至0.041±.002。这一超过17倍的提升证实了训练-推理不匹配和跨时间步梯度冲突是连续扩散模型性能低下的关键瓶颈，而Stable-Min-SNR-γ通过统一SNR重加权策略有效解决了这两个问题。

Stable-Min-SNR-γ的核心机制在于：通过强制最终时间步SNR=0（Zero-SNR）来消除训练-推理不匹配，同时使用稳定化权重$w_{t} = \frac{\min\{\mathrm{SNR}(t),\gamma\}}{\mathrm{SNR}(t)+\phi}$避免SNR=0时的除零错误，并协调不同时间步的梯度冲突。

### 失败模式与局限

尽管COME在整体指标上表现优异，但仍存在以下局限：

1. **细粒度文本对齐的微小差距**：在R-Precision Top1上，COME（0.510）略低于**MoMask**（0.521）和**BAMM**等极少数加强基线。这表明在将文本语义精确映射到运动细节方面，离散token化+掩码Transformer的方案仍具有微弱优势。
2. **物理合理性缺陷**：由于训练数据中缺乏显式的手部和脚部关节标注，生成结果可能出现轻微的穿透或足部滑动现象。这一局限源于数据集而非方法本身，但在实际应用中需要关注。
3. **极端场景的泛化能力未验证**：当前框架在极端风格迁移、通用化人-物交互（HOI）和人-场景交互（HSI）等任务上的扩展能力有待进一步探索。

### 效率分析

COME在推理效率上具有显著优势：采用10步DPM-Solver++采样即可达到高质量生成，结合MoCMAE的轻量CNN解码器（无Transformer解码开销），整体推理速度在A6000 GPU上优于多数对比方法。训练效率方面，Stable-Min-SNR-γ策略通过稳定训练动态减少了收敛所需迭代次数，使得COME在训练成本上也具备竞争力。

![[assets/figures/papers/paper_list_l14_COME_Advancing_Representation_Learning_and_Generative_Modeling_for_High/figures/004_Table_4.jpg]]
*Table 4: Ablation study result of MoCMAE*

![[assets/figures/papers/paper_list_l14_COME_Advancing_Representation_Learning_and_Generative_Modeling_for_High/figures/009_Table_5.jpg]]
*Table 5: Ablation study result of ccDIT*

![[assets/figures/papers/paper_list_l14_COME_Advancing_Representation_Learning_and_Generative_Modeling_for_High/figures/014_Table_8.jpg]]
*Table 8: In summary, the combination of training efficiency, fast inference, and high-quality generation underscores the effectiveness of our architectural and learning design. COME demonstrates that continuous diffusion models—when equipped with strong representation learning—can achieve stateof-the-art T2M synthesis with both speed and fidelity. Table 8: Training cost comparison across methods. We report epochs and GPU-hours for each module (motion tokenizer and diffusion model) and the total GPU-hours using a single NVIDIA A6000 GPU. Our method converges with significantly fewer epochs and GPU-hours compared to MLD, achieving a 6× improvement in training efficiency*

## 定位与知识库关联

### 连续扩散 vs. 离散生成：T2M 方法谱系中的位置

文本到运动生成（T2M）领域长期存在两条技术路线之争：**连续扩散模型**与**离散生成模型**。COME 的核心贡献在于，它通过系统性地解决连续扩散框架的两个根本瓶颈——运动表示质量和扩散训练策略——使连续范式重新获得了对离散方法的竞争优势。

早期连续扩散方法直接在原始运动空间建模，如 **MDM**（Tevet et al., ICLR 2022）和 **MotionDiffuse**（Zhang et al., T-PAMI 2024），虽然保留了连续空间在语义控制和多样性采样上的天然优势，但在生成质量上始终落后于离散方案。后续工作试图通过不同路径弥补这一差距：**MLD**（Chen et al., ICCV 2023）引入 VAE 潜在空间以降低扩散成本，但标准 VAE 编码器的表示拥挤且不可分（见 Tab. 7, Figs. 5-6），反而限制了去噪过程的效率；**ReMoDiffuse**（Zhang et al., ICCV 2023）通过检索增强机制提升语义对齐，但检索库依赖和计算开销限制了其可扩展性；**MotionLCM**（Dai et al., CVPR 2025）则聚焦于采样加速，未触及表示质量这一根本问题。

与此同时，离散方案凭借 VQ-VAE/RVQ-VAE 的天然聚类特性和掩码 Transformer 的高效训练，在多个基准上持续领先：**T2M-GPT**（Zhang et al., CVPR 2023）开创了离散 token 化+自回归生成范式；**MoMask**（Guo et al., ECCV 2024）通过 RVQ-VAE 和掩码 Transformer 将 FID 推至 0.045，成为 COME 发表前的最强基线；**MMM**（Pinyoanuntapong et al., AAAI 2024）进一步探索了掩码建模在运动生成中的潜力。

COME 的方法定位是**在连续扩散框架内，通过表示学习和训练策略的协同改进，实现对离散 SOTA 的全面超越**。其关键洞察在于：连续扩散模型的潜力被低质量运动表示和次优训练策略所掩盖，而非连续范式本身存在根本性缺陷。

### 核心改进槽位与因果链路

COME 的方法创新可拆解为四个相互耦合的改进槽位，每个槽位对应一个明确的因果瓶颈：

**槽位 1：运动表示 Tokenizer（标准 VAE → MoCMAE）**

标准 VAE（如 MLD 中使用）产生的潜在特征拥挤且不可分，具体表现为低 Silhouette Score、高 Davies-Bouldin Index 和低 5-NN 准确率（Tab. 18）。MoCMAE 通过三个机制重塑表示空间：
- **非对称架构**：编码器采用 CNN（局部运动提取）+ Transformer（长程时空建模）的混合设计，解码器保持轻量 CNN，避免解码端过度参数化导致的表示退化（§4.1）；
- **掩码运动建模（MMM）**：以 50% 掩码比强制编码器从部分观测中推理完整运动结构，增强表示的鲁棒性和全局语义捕获能力（Tab. 4：50% 掩码比获得全局最优重建 FID 0.002 / MPJPE 8.8）；
- **对比学习（CL）**：拉近同一运动的完整版本和掩码版本的特征，推开不同样本的特征，直接提升表示的可分性（Tab. 4：移除 CL 导致生成 FID 从 0.041 退至 0.058）。

因果链路：MoCMAE 的高鉴别力表示 → 扩散模型在潜在空间中的去噪任务更简单 → 生成质量显著提升。证据强度：Tab. 2 显示 MoCMAE 在重建 FID（0.002）和 MPJPE（8.8）上远优于所有对比 tokenizer；Tab. 4 证实下游生成 FID 从 VAE 基线的 0.703 降至 0.041。

**槽位 2：扩散生成骨干网络（标准 DiT → ccDIT）**

标准 DiT 仅通过 AdaLN 注入时间步信息，缺乏对文本语义的结构化利用。ccDIT 引入双重条件注入机制：
- **AdaLN-Zero**：注入句级全局语义，控制生成运动的整体风格和动作类型（Tab. 5：移除句级语义 → FID 从 0.041 升至 0.076，R-Prec Top1 从 0.526 降至 0.508）；
- **Cross-Attention**：注入词级细粒度语义，确保每个局部动作与文本关键词的对齐（Tab. 5：移除词级语义 → FID 升至 0.089，R-Prec Top1 降至 0.504）；
- **U 型跳跃连接**：借鉴 U-DiT 设计，保留低层细节信息以提升时序连贯性。

因果链路：句级语义控制“做什么”，词级语义控制“怎么做”，两者缺一不可。证据强度：双重消融实验的 FID 退化和 R-Precision 下降幅度直接量化了各自贡献。

**槽位 3：扩散训练损失函数（标准 MSE → Stable-Min-SNR-γ）**

连续扩散模型存在两个训练-推理不一致问题：
- **训练-推理不匹配**：标准扩散在训练时使用 SNR>0 的时间步，但推理时最终步的 SNR=0（纯噪声），导致模型在边界条件下行为不可预测；
- **跨时间步梯度冲突**：不同噪声水平的梯度尺度差异巨大，高 SNR 步主导训练，低 SNR 步欠拟合。

Stable-Min-SNR-γ 通过统一 Zero-SNR 和 Min-SNR-γ 策略解决这两个问题（Eq. 9-10）：
$$w_{t} = \frac{\min\{\mathrm{SNR}(t),\gamma\}}{\mathrm{SNR}(t)+\phi}$$

其中 Zero-SNR 强制最终时间步的 SNR=0（通过调整噪声调度参数），使训练分布覆盖推理边界；Min-SNR-γ 截断高 SNR 步的权重，缓解梯度冲突；分母中的 $\phi$ 项避免 SNR=0 时的除零错误。Tab. 5 的消融显示：仅使用基础 DiT 时 FID 为 0.703，加入 Zero-SNR 和 Stable-Min-SNR-γ 后降至 0.041，贡献幅度远超其他组件。

**槽位 4：推理策略（标准采样 → CFG + DPM-Solver++）**

COME 采用 Classifier-Free Guidance（训练时 10% 概率丢弃文本条件）结合 DPM-Solver++ 高阶快速采样器，在保持生成多样性的同时提升文本对齐精度和推理效率。推理速度对比在相同 A6000 GPU 环境下进行，统一采用 10 步采样以公平比较。

### 适用边界与局限

尽管 COME 在生成质量（FID）和效率上全面超越了离散 SOTA，但其适用边界和局限性同样明确：

1. **物理合理性缺陷**：由于 HumanML3D 和 KIT-ML 数据集缺乏显式的手部和脚部关节标注，生成结果可能出现轻微的穿透或足部滑动现象。这是数据驱动的连续扩散方法的共性局限，而非 COME 特有。

2. **文本对齐的微小差距**：在 R-Precision Top1 指标上，COME（0.510）略低于 MoMask（0.521）和 BAMM（更强基线），说明在精确的文本-运动语义匹配上仍有提升空间。这可能源于连续表示的“过度平滑”倾向——虽然可分性大幅提升，但相比离散 token 的硬聚类边界，连续表示在极端细粒度语义区分上仍存在固有劣势。

3. **极端风格迁移与通用化能力未验证**：当前框架专注于标准 T2M 任务，在风格迁移、HOI（人-物交互）和 HSI（人-场景交互）等需要强物理约束和零样本泛化的场景上的扩展能力有待验证。

4. **数据集规模与噪声鲁棒性**：COME 在 HumanML3D（约 15K 样本）和 KIT-ML（约 4K 样本）上验证，其在更大规模、更多噪声标注的数据集（如 MotionX）上的鲁棒性和检索增强能力仍是开放问题。

### 开放问题与未来方向

从方法谱系的角度，COME 的贡献引出了以下深层问题：

1. **最优运动 Tokenizer 的理论基础**：MoCMAE 的设计（非对称架构+MMM+CL）是经验性的，如何从信息论或表示学习理论层面定义和构建“最优”运动 tokenizer？例如，对比学习和掩码建模的交互机制如何被形式化，以指导更具鉴别能力的表示学习？

2. **连续 vs. 离散的范式融合**：COME 证明连续表示可以通过增强可分性来模拟离散 token 的优势，但两者的边界是否可以被进一步模糊？例如，是否可以在连续潜在空间中引入软量化或混合表示，同时保留连续空间的平滑性和离散空间的聚类特性？

3. **多模态条件与物理仿真约束的扩展**：COME 的 ccDIT 架构通过 AdaLN-Zero 和 Cross-Attention 实现了文本条件的灵活注入，理论上可以扩展到音乐、视频等多模态条件。但如何无缝集成物理仿真约束（如接触力、关节限制）以解决穿透和滑动问题，仍是一个工程与理论并重的挑战。

4. **大规模数据下的鲁棒性与检索增强**：当数据规模扩大至 MotionX 级别（约 15M 样本）时，MoCMAE 的对比学习分支是否仍能有效区分样本？是否需要引入检索增强机制（如 ReMoDiffuse）来弥补表示学习的上限？

## 原文 PDF

![[paperPDFs/ICLR_2026/COME_Advancing_Representation_Learning_and_Generative_Modeling_for_High_Quality_Text_to_Motion_Generation.pdf]]
