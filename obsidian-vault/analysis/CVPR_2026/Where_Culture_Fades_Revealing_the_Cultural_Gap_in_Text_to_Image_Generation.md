---
title: "Where Culture Fades: Revealing the Cultural Gap in Text-to-Image Generation"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/Where_Culture_Fades_Revealing_the_Cultural_Gap_in_Text_to_Image_Generation.pdf
project_link: null
code_link: "https://chat.openai.com/"
aliases:
- ZTNAFTLE
- WCFRCGTIG
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/generative_models_diffusion
- topic/benchmarks_datasets_evaluation
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: 通过定位文本编码器中特定文化敏感层内的少量文化敏感神经元，并对其进行激活放大或少量微调，可以因果性地改变生成图像的文化属性。
primary_logic: 模型预训练过程中已经获得了丰富且多样的文化知识，但因“名词提示”缺乏显式文化触发信号，这些知识未被充分激活。通过神经元级别的探测和干预，可以在不破坏模型整体保真度与多样性的情况下，恢复并增强跨语言的文化一致性。
claims:
- 显式添加文化风格修饰语可大幅提升CultureVQA得分，证明文化知识存在于模型中，而非缺失。
- 掩蔽探测到的Top-K文化敏感神经元会导致CultureVQA急剧下降，而随机掩蔽相同数量的神经元影响甚微，表明这些神经元与文化语义有因果关系。
- 在两个不同架构的扩散模型（PEA-Diffusion和AltDiffusion）上，所提出的零训练和微调方法均能一致地提升文化一致性，同时维持文本图像对齐和感知质量。
- 检测到的文化敏感层具有高度的跨语言一致性，PEA-Diffusion峰值出现在第16层，AltDiffusion出现在第14层，验证了文化表征的集中性。
---

# Where Culture Fades: Revealing the Cultural Gap in Text-to-Image Generation

> [!tip] 核心洞察
> 模型预训练过程中已经获得了丰富且多样的文化知识，但因“名词提示”缺乏显式文化触发信号，这些知识未被充分激活。通过神经元级别的探测和干预，可以在不破坏模型整体保真度与多样性的情况下，恢复并增强跨语言的文化一致性。

| 字段 | 内容 |
|------|------|
| 中文题名 | 文化消逝之处：揭示文本到图像生成中的文化鸿沟 |
| 英文题名 | Where Culture Fades: Revealing the Cultural Gap in Text-to-Image Generation |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2511.17282) · [Code](https://chat.openai.com/) |
| Topic | #topic/vision_multimodal_applications #topic/generative_models_diffusion #topic/benchmarks_datasets_evaluation #topic/vision_multimodal_applications/image_and_video_generation |
| Method | Zero-Training Neuron Amplifier and Fine-Tuned Layer Enhancer |
| Dataset | CultureBench test subset, User Study, Cross-Domain Generalization |

> [!tip] 效果简介
> - CultureBench test subset (noun-only prompts) 上，CultureVQA 36.63 (Fine-Tuned); 33.91 (Zero-Training) vs 25.13 (StableDiffusion 3.5); 23.05 (AltDiffusion); 21.65 (PEA-Diffusion) (+14.98 / +12.32 over AltDiffusion and PEA-Diffusion respectively)；CLIPScore 0.291 (Zero-Training); 0.290 (Fine-Tuned) vs 0.282 (AltDiffusion); 0.253 (PEA-Diffusion) (+0.038 / +0.037)；ImageReward 0.33 (Zero-Training); 0.31 (Fine-Tuned) vs -0.11 (AltDiffusion); -0.65 (PEA-Diffusion) (+0.98 / +0.42)。
> - User Study (CultureBench platform, 50 experts) 上，CSR (Cultural Semantic Relevance, 1-5 scale) 77.6 vs 60.4 (second-best) (+17.2)。
> - Cross-Domain Generalization (100 out-of-distribution captions) 上，CultureVQA 35.00 (Fine-Tuned on PEA-Diffusion); 32.00 (Fine-Tuned on AltDiffusion) vs 15.00 (PEA-Diffusion); 15.00 (AltDiffusion) (+20.00 / +17.00)。

## 概要

**核心问题**：当前多语言文本到图像（T2I）模型在仅使用名词提示（noun-only prompts）时，输出图像普遍缺乏目标语言区域的文化特征，呈现出明显的“文化中性”甚至英语文化中心主义倾向。这一现象与大型语言模型（LLMs）和推荐系统在相同条件下能保持文化一致性形成鲜明对比（Figure 1）。

**根本原因**：模型在预训练过程中实际上已经习得了丰富且多样的文化知识，但由于“名词提示”缺乏显式的文化触发信号，这些知识在文本编码器中的相关语义表征未被充分激活。实验表明，当显式添加“文化风格修饰语 + 名词”的提示时，CultureVQA得分大幅提升——**AltDiffusion**（Chen et al., 2023）从23.05升至44.39，**PEA-Diffusion**（Zhang et al., 2024）从21.65升至35.62（Figure 4），直接验证了“文化知识存在于模型中，而非缺失”这一核心假设。

**方法定位**：本文提出了一套“探测-干预”框架，从神经元级别揭示并修复文化鸿沟。该方法首先通过对比注意力模式定位文本编码器中的文化敏感层（PEA-Diffusion峰值在第16层，AltDiffusion在第14层），随后利用Top-K稀疏自编码器（SAE）识别该层内少数文化敏感神经元。在此基础上，提出两种轻量级文化对齐策略：（1）**零训练神经元放大器**——在推理时通过手工系数λ直接放大文化敏感神经元的SAE隐变量，无需任何参数更新；（2）**微调层增强器**——仅在文化敏感层插入小型残差模块，使用像素级MSE损失进行训练，保持骨干网络冻结。

**主要结果**：在CultureBench测试子集上，两种策略均显著超越多个SOTA模型（Table 2）。零训练方案在PEA-Diffusion上CultureVQA提升12.26点（21.65→33.91），在AltDiffusion上提升7.01点；微调方案增益分别达14.98点和9.61点。同时，CLIPScore和ImageReward均保持正向提升，LPIPS感知距离有所降低。在50名专家的用户研究中，所提方法在文化语义相关性（CSR）评分上以77.6分显著领先次优方法的60.4分（Figure 9）。跨域泛化实验进一步表明，方法在100条域外描述上仍保持+17至+20点的CultureVQA增益（Table 6）。

**方法谱系与知识库定位**：本研究处于文本到图像生成与文化公平性的交叉领域。与**StableDiffusion XL**（Podell et al., 2023）、**FLUX.1-dev**（Black Forest Labs, 2024）等通用大规模T2I模型直接对比文化生成能力；与**PEA-Diffusion**和**AltDiffusion**等跨语言对齐扩散模型进行文化一致性改进的量化对比。在文化感知生成方面，区别于依赖提示工程或全模型微调的现有方案，本文首次从神经元可解释性角度定位并因果性地调控文化表征，为模型的文化对齐提供了一种参数高效、架构可迁移的新范式。

### 多语言文本到图像模型的文化对齐鸿沟

近年来，以扩散模型为核心的文本到图像（T2I）生成取得了显著进展，代表性模型如 **StableDiffusion XL**（Podell et al., 2023）、**FLUX.1-dev**（Black Forest Labs, 2024）以及 **StableDiffusion 3.5**（Stability AI, 2024）在图像保真度和文本对齐方面表现优异。与此同时，诸如 **AltDiffusion**（Chen et al., 2023）和 **PEA-Diffusion**（Zhang et al., 2024）等模型通过引入多语言文本编码器，试图将生成能力拓展至非英语语言环境。然而，一个关键问题被系统性忽视：**模型在多语言环境下能否生成与目标语言文化背景相一致的视觉内容？**

Figure 1 直观地揭示了这一鸿沟。当用户使用“仅名词”提示（noun-only prompts）进行跨语言生成时，T2I模型的输出往往呈现文化中性甚至英语文化中心主义的倾向，而大语言模型（LLMs）和推荐系统在相同条件下却能保持文化一致性。这一现象的核心矛盾在于：**模型并非缺乏文化知识，而是这些知识在“名词提示”条件下未被充分激活**。如 Figure 4 所示，当显式添加“文化风格修饰语”（culture-style modifier）时，CultureVQA 得分大幅提升——在 AltDiffusion 上达到 44.39，在 PEA-Diffusion 上达到 35.62，远高于仅使用名词提示的基线水平。这一证据直接验证了“文化知识存在于模型参数中，但缺乏触发信号”这一核心假设。

### 现有方法的局限性

当前应对文化一致性问题的策略主要分为两类，但均存在明显不足：

- **提示工程方法**：依赖用户显式指定文化修饰语（如“日本风格的寿司”），这不仅增加了使用门槛，还要求用户具备跨文化知识储备，且修饰语的选择对生成结果影响高度敏感。
- **全参数微调或重新训练**：通过在特定文化数据集上微调整个模型来注入文化知识，但代价高昂——计算资源消耗大、可能破坏模型原有的泛化能力，且难以灵活适配多种文化场景。

更深层的问题在于，**文化知识在文本编码器中的表征机制尚不明确**。已有工作（如 **Show-o2**，Pan et al., 2025）探索了多模态统一架构，但并未专门研究文化语义的神经元级定位与干预。这导致两个关键缺口：（1）缺乏系统的方法来探测文化敏感层和神经元；（2）缺乏轻量、可插拔的干预策略，能在不破坏模型整体保真度的前提下恢复文化一致性。

### 本文动机与研究思路

针对上述缺口，本文提出一套完整的“探测-干预”框架，其核心洞察是：**模型预训练过程中已经获得了丰富且多样的文化知识，但这些知识集中在文本编码器的少数层和少量神经元中，因缺乏显式触发信号而处于“休眠”状态**。通过神经元级别的探测和干预，可以在不重新训练完整模型的前提下，因果性地改变生成图像的文化属性。

具体而言，本文的动机可归纳为三个递进目标：

1. **定位文化表征**：开发一种探测方法，通过对比文化修饰语与名词之间的跨注意力差异（$\Delta\mathrm{CA}(l)$），定位文本编码器中对文化最敏感的单一层；进而利用 Top-K 稀疏自编码器（SAE）和加权频率分数，在敏感层内识别出对特定文化具有高选择性的少量神经元。
2. **轻量干预**：基于探测结果，提出两种互补的文化对齐策略——零训练神经元放大器（inference-time activation）和微调层增强器（layer-targeted enhancement），前者通过推理时放大文化敏感神经元的 SAE 隐变量实现零训练成本的文化增强，后者仅在敏感层插入少量可训练残差模块，以极低的参数开销实现自适应文化对齐。
3. **跨模型验证**：在两个不同架构的扩散模型（PEA-Diffusion 和 AltDiffusion）上验证方法的有效性与泛化性，证明文化表征的集中性和可干预性并非特定模型的偶然现象，而是跨架构的普遍规律。

## 核心方法与创新机理

本文的核心创新并非提出一个全新的模型架构或训练范式，而是**发现并因果性地验证了现有文本到图像（T2I）模型中文化知识的“激活瓶颈”**，并据此设计了一套轻量、可插拔的文化一致性增强方案。其关键突破点在于将“文化鸿沟”问题从数据或模型能力层面，重新定义为**表征激活不足的问题**，并提供了从探测到干预的完整证据链。

### 问题重定义：从“知识缺失”到“激活失败”

现有T2I模型在使用“仅名词”（noun-only）提示时，其输出往往倾向于文化中性或英语文化中心主义。本文通过一个关键的对照实验（Figure 4）推翻了“模型缺乏文化知识”的常见假设：当在名词前显式添加“文化风格修饰语”（culture-style modifier）时，**PEA-Diffusion** 和 **AltDiffusion** 的CultureVQA得分分别大幅提升至35.62和44.39。这直接证明，模型在预训练中已经习得了丰富且多样的文化知识，但这些知识在缺乏显式文化触发信号的名词提示下，未能被充分激活。这一洞察将研究焦点从“如何向模型注入新知识”转向了“如何激活模型已有的知识”。

### 方法谱系与知识库定位

当前主流方法，如 **PEA-Diffusion** (Zhang et al., 2024) 和 **AltDiffusion** (Chen et al., 2023)，主要致力于通过跨语言文本编码器对齐或大规模多语言数据训练来提升模型的多语言能力，但它们并未显式地对“文化”这一深层语义维度进行建模和干预。其他通用模型如 **StableDiffusion XL** (Podell et al., 2023) 和 **FLUX.1-dev** (Black Forest Labs, 2024) 则在文化一致性上表现更弱。

本文方法在知识库中的独特定位在于：**首次在神经元级别实现了对文化表征的探测与因果操控**。它不改变模型的训练数据或基础架构，而是通过“探测-干预”的范式，在现有模型内部开辟了一条通往文化子空间的“捷径”。这种思路与模型可解释性领域中的知识定位和激活工程一脉相承，但将其成功应用到了多文化T2I生成这一复杂场景。

### 关键创新点与 Changed Slots 深度解析

相较于基线方法，本文提出的方案在两个核心维度上引入了根本性变化，形成了三个关键的“changed slots”。

**1. 文化特征激活策略：从“无干预”到“神经元级定向增强”**

这是最核心的范式转变。基线方法将文本编码器的输出直接送入扩散模型，没有任何文化特定的干预。本文则构建了一个两阶段的“探测-干预”流水线：

-   **探测阶段**：首先，通过计算“文化修饰语+名词”与“仅名词”提示对之间的跨注意力差异（$\Delta CA(l)$），精准定位文本编码器中的**单一文化敏感层**（PEA-Diffusion为第16层，AltDiffusion为第14层，见Figure 6）。接着，在该层内，利用Top-K稀疏自编码器（SAE）分解注意力特征，并通过**加权频率分数（WFS）** 识别出对文化具有高选择性的**少数文化敏感神经元**（见Figure 7）。这一探测过程揭示了文化知识在模型内部的表征具有高度的集中性和稀疏性。

-   **干预阶段**：基于探测结果，本文提出了两种互补的增强策略，直接放大了被“名词提示”所抑制的文化信号：
    -   **零训练神经元放大器**：在推理时，仅对探测到的文化敏感神经元的SAE隐变量乘以一个手工设定的放大系数$(1+\lambda)$，再解码回注意力特征空间。此过程**完全冻结模型参数**，实现了零成本的即插即用文化增强。
    -   **微调层增强器**：在文化敏感层中插入一个轻量的残差变换模块，仅微调该模块的参数，使用像素级MSE损失与CultureBench中的文化参考图像进行对齐。这实现了自适应的文化增强，同时保持了骨干网络的稳定性。

**2. 可训练参数范围：从“全量/冻结”到“参数高效微调”**

基线方法的参数状态通常是二元的：要么整体模型冻结，要么进行全参数微调。本文的微调方案（Fine-Tuned Layer Enhancer）引入了一种极致的参数高效策略：**仅更新文化敏感层中新增的少量残差模块参数，模型其余所有参数保持冻结**。这极大地降低了微调成本，并避免了灾难性遗忘，保证了模型的泛化能力。

**3. 训练信号与损失：从“通用目标”到“文化对齐目标”**

基线方法使用标准的对比损失或扩散损失进行训练，这些目标不直接衡量文化一致性。本文的微调方案首次在T2I文化增强任务中引入了**像素级的MSE损失**（$\mathcal{L}_{MSE}$），直接以CultureBench中的文化参考图像作为监督信号。虽然MSE并非文化相似度的完美度量，但它为模型提供了一个明确的、可优化的文化对齐目标，这是从“隐式”学习到“显式”对齐的关键一步。

### 因果性验证：创新的基石

上述所有创新的有效性都建立在一个坚实的因果性验证之上。**Table 1** 的掩蔽实验提供了决定性证据：掩蔽探测到的Top-K文化敏感神经元后，PEA-Diffusion的CultureVQA得分从35.62**暴跌至7.65**（-27.97），而掩蔽相同数量的随机神经元，得分仅微降至33.04（-2.58）。在AltDiffusion上重复该实验，Top-K掩蔽导致得分下降32.50点，随机掩蔽仅下降2.09点（Table 5）。这无可辩驳地证明了，所探测的特定神经元与文化语义之间存在直接的因果关系，而非相关性。正是这一发现，使得后续的神经元放大和层增强操作有了明确的、可解释的靶点，构成了本文方法论的基石。

本文提出的方法遵循“探测-干预”两阶段范式，旨在以极低的参数开销恢复多语言文本到图像模型中被抑制的文化表征。整体pipeline由四个功能模块串联构成，输入为CultureBench中的“名词提示”（noun-only prompt），输出为文化一致性显著增强的生成图像。

**阶段一：文化表征定位**

1.  **文化层检测模块**：利用对比注意力分析，计算文化修饰语提示与纯名词提示在文本编码器各层的跨注意力差异 $\Delta \mathrm{CA}(l)$。$\Delta \mathrm{CA}$ 峰值所在层被认定为文化敏感层。实验表明，该峰值在PEA-Diffusion中出现在第16层，在AltDiffusion中出现在第14层（Figure 6, Figure 14），呈现出高度的跨模型集中性。

2.  **文化神经元检测模块**：在已定位的文化敏感层内，先通过Top-K稀疏自编码器（SAE）将注意力特征分解为稀疏隐变量 $Z$，然后计算每个神经元在文化样本集上的加权频率分数 $WFS_{\mathrm{cult}}(m)$。$WFS$ 仅在极少数神经元上形成尖锐峰值（Figure 7），表明文化知识高度集中于少量特定神经元中。通过设定阈值，筛选出文化敏感神经元集 $M_{\mathrm{cult}}$。

**阶段二：文化表征增强**

3.  **零训练神经元放大器**（推理时干预）：对于给定的名词提示，将其在文化敏感层产生的原始注意力特征 $F_{\mathrm{raw}}$ 经SAE编码为 $Z_{\mathrm{raw}}$。随后，对 $M_{\mathrm{cult}}$ 中神经元的隐变量乘以放大因子 $(1+\lambda)$，其余神经元保持不变，得到增强后的隐变量 $Z_{\mathrm{enh}}$。最后通过SAE解码回特征空间 $F_{\mathrm{rec-enh}}$，馈入扩散模型生成图像。此方案完全冻结模型参数，仅通过手工设定 $\lambda$（实验中取 $\lambda=6$）控制增强强度。

4.  **微调层增强器**（轻量训练干预）：在文化敏感层的隐状态 $h$ 上插入一个残差变换模块 $\tilde{h} = h + g(W_2 \sigma(W_1 h))$。仅该模块的参数可训练，其余骨干网络全部冻结。训练时，使用CultureBench中的文化参考图像 $x_i^*$ 作为目标，以像素级MSE损失 $\mathcal{L}_{\mathrm{MSE}}$ 进行监督，使增强后的特征直接向目标文化风格对齐。

两个增强方案的设计体现了“文化知识已存在于模型中，仅需针对性激活”的核心洞察：零训练方案通过神经元级放大实现即插即用的文化恢复；微调方案则以极少量可训练参数（仅作用于单一层）换取自适应优化，二者均避免了对完整模型的重训练，从而在提升文化一致性的同时维持了文本-图像对齐质量与生成多样性。

本文方法的核心在于“探测-增强”两阶段框架：首先在冻结的文本编码器中定位文化敏感层与神经元，随后通过两种互补策略——零训练神经元放大与微调层增强——在推理或训练阶段注入文化信号。以下逐一阐述各模块的关键设计与公式。

### 文化敏感层检测

该模块的目标是从文本编码器的多层注意力中，定位出对文化修饰语响应最强烈的那一层。直觉在于：当提示中包含文化风格修饰语（如“摩洛哥风格的茶壶”）时，文化词元到目标名词的跨注意力应显著高于仅使用名词（“茶壶”）的情况。这一差异的峰值层即被认定为文化敏感层。

首先，对第 $l$ 层的多头注意力按头取平均，以获得稳定的注意力表示：

$$
\bar{A}(l) = \frac{1}{H} \sum_{h=1}^{H} A_h(l)
$$

其中 $H$ 为注意力头数，$A_h(l)$ 为第 $h$ 个头的注意力矩阵。随后，对于给定提示 $P$，计算文化修饰语到目标名词的平均注意力分数：

$$
\mathrm{CA}(P, l) = \frac{\sum_{t_{\mathrm{cult}}} \sum_{t_{\mathrm{noun}}} \bar{A}_{key}(l)_{t_{\mathrm{cult}} t_{\mathrm{noun}}}}{|T_{\mathrm{cult}}| \cdot |T_{\mathrm{noun}}|}
$$

这里 $T_{\mathrm{cult}}$ 和 $T_{\mathrm{noun}}$ 分别为文化修饰语和名词的词元集合，$\bar{A}_{key}(l)$ 为键-查询注意力矩阵。最后，在 $N$ 对文化提示 $P_{\mathrm{cult},i}$ 与名词提示 $P_{\mathrm{noun},i}$ 上取差值平均，得到第 $l$ 层的文化注意力差异 $\Delta \mathrm{CA}(l)$：

$$
\Delta \mathrm{CA}(l) = \frac{1}{N} \sum_{i=1}^{N} [\mathrm{CA}(P_{\mathrm{cult}, i}, l) - \mathrm{CA}(P_{\mathrm{noun}, i}, l)]
$$

该值在 **PEA-Diffusion** 上于第16层达到峰值（Figure 6），在 **AltDiffusion** 上于第14层达到峰值（Figure 14），表明文化表征高度集中在单一层内。这一跨模型的一致性验证了探测方法的鲁棒性。

![[assets/figures/papers/paper_list_l2365_https_arxiv_org_abs_2511_17282/figures/006_Figure_6.jpg]]
*Figure 6: PEA-Diffusion cultural sensitivity. ∆CA peaks layer 16. AltDiffusion results are provided in the appendix*

![[assets/figures/papers/paper_list_l2365_https_arxiv_org_abs_2511_17282/figures/017_Figure_14.jpg]]
*Figure 14: AltDiffusion cultural sensitivity. ∆CA peaks layer 14. Therefore, layer 14 is culturally sensitive*

### 文化敏感神经元检测

在定位到文化敏感层后，需进一步识别该层注意力特征空间中少数对文化具有高选择性的神经元。此处引入 Top-K 稀疏自编码器（SAE），将原始注意力特征 $F_{\mathrm{raw}}$ 分解为稀疏隐变量 $Z_{\mathrm{raw}}$：

$$
Z_{\mathrm{raw}} = \mathrm{SAE.encode}(F_{\mathrm{raw}})
$$

随后，对每个神经元 $m$ 在文化样本集合上计算两个统计量。激活频率 $f_{\mathrm{cult}}(m)$ 衡量该神经元在文化样本中被激活的比例：

$$
f_{\mathrm{cult}}(m) = \frac{1}{N_{\mathrm{cult}}} \sum_{i=1}^{N_{\mathrm{cult}}} \mathbb{I}(Z_{\mathrm{cult}}[i, m] > \epsilon)
$$

其中 $\epsilon$ 为激活阈值，$\mathbb{I}(\cdot)$ 为指示函数。平均激活幅度 $\mu_{\mathrm{cult}}(m)$ 仅统计激活超过阈值的样本：

$$
\mu_{\mathrm{cult}}(m) = \frac{\sum_{i=1}^{N_{\mathrm{cult}}} (Z_{\mathrm{cult}}[i,m] \cdot \mathbb{I}(Z_{\mathrm{cult}}[i,m] > \epsilon))}{\sum_{i=1}^{N_{\mathrm{cult}}} \mathbb{I}(Z_{\mathrm{cult}}[i,m] > \epsilon) + \beta}
$$

此处 $\beta$ 为防止除零的小常数。最终的加权频率分数 $WFS_{\mathrm{cult}}(m)$ 结合频率与幅度，用于筛选文化敏感神经元：

$$
WFS_{\mathrm{cult}}(m) = f_{\mathrm{cult}}(m) \cdot \mu_{\mathrm{cult}}(m)
$$

实验显示，$WFS$ 仅在极少数神经元上形成尖锐峰值（Figure 7），文化知识高度集中。因果验证（Table 1）表明：掩蔽这些 Top-K 神经元使 CultureVQA 从 35.62 骤降至 7.65（-27.97），而随机掩蔽等量神经元仅降至 33.04（-2.58），证实了所选神经元与文化语义的因果关系。

### 零训练神经元放大器

该模块在推理时运行，无需任何模型参数更新。其核心操作是：对已识别的文化敏感神经元集合 $M_{\mathrm{cult}}$，将其 SAE 隐变量乘以因子 $(1+\lambda)$ 进行放大，其余神经元保持不变：

$$
Z_{\mathrm{enh}}[b,p,m] = \begin{cases} (1+\lambda) Z_{\mathrm{raw}}[b,p,m] & \text{if } m \in M_{\mathrm{cult}} \\ Z_{\mathrm{raw}}[b,p,m] & \text{otherwise} \end{cases}
$$

其中 $b$ 为批次索引，$p$ 为位置索引，$\lambda$ 为手工设定的放大系数（论文中设置为 $\lambda=6$）。增强后的隐变量经 SAE 解码回注意力特征空间：

$$
F_{\mathrm{rec-enh}} = \mathrm{SAE.decode}(Z_{\mathrm{enh}})
$$

该特征随后替代原始注意力特征，进入扩散模型的后续生成流程。此方法完全冻结模型参数，仅通过推理时的神经元级调制实现文化增强。

### 微调层增强器

为进一步自适应地增强文化表征，该模块在文化敏感层中插入一个轻量残差变换网络，仅微调该模块而保持骨干网络冻结。具体地，对敏感层的隐状态 $h$ 施加残差变换：

$$
\tilde{h} = h + g(W_2 \sigma(W_1 h))
$$

其中 $W_1$ 和 $W_2$ 为可训练的权重矩阵，$\sigma$ 为非线性激活函数，$g$ 为缩放因子。训练时使用像素级均方误差损失，将生成图像 $\hat{x}_i$ 与 CultureBench 中的文化参考图像 $x_i^*(p)$ 对齐：

$$
\mathcal{L}_{\mathrm{MSE}} = \frac{1}{N} \sum_{i=1}^{N} \left\| \hat{x}_i - x_i^*(p) \right\|_2^2
$$

该方案的可训练参数仅限于新增的残差模块，参数量极小，训练开销远低于全模型微调。实验表明，该方案在 CultureVQA 上达到 36.63，优于零训练方案的 33.91（Table 2），但零训练方案在 CLIPScore 和 ImageReward 上略占优势，体现了两种策略在不同指标上的互补性。

## 实验与关键发现

### 核心假设验证：文化知识存在于模型中，而非缺失

在讨论定量结果之前，先验证本文的核心假设——多语言文本到图像模型在仅使用名词提示时，并非缺乏文化知识，而是未能充分激活已有知识。Figure 4 展示了在 CultureBench 测试子集上，对比“文化风格修饰语 + 名词”与“仅名词”两种提示条件下的 CultureVQA 分数：PEA-Diffusion 从 21.65 跃升至 35.62，AltDiffusion 从 23.05 跃升至 44.39。这一显著差距表明，模型预训练过程中已经获得了丰富且多样的文化表征，但“名词提示”缺乏显式文化触发信号，导致这些表征在生成阶段未被有效激活。这一发现构成了后续所有神经元级探测与干预方法的逻辑基础。

### 文化敏感神经元的因果性验证

在定位文化敏感层和神经元后，必须证明所选神经元与文化语义之间存在因果关系，而非统计上的偶然相关。Table 1 展示了 PEA-Diffusion 上的掩蔽实验：在“文化风格修饰语 + 名词”提示条件下，掩蔽 Top-K 文化敏感神经元后，CultureVQA 从 35.62 暴跌至 7.65（下降 27.97 点）；而掩蔽相同数量的随机神经元，CultureVQA 仅降至 33.04（下降 2.58 点）。Table 5 在 AltDiffusion 上重复了相同实验，掩蔽 Top-K 神经元导致 CultureVQA 下降 32.50 点，随机掩蔽仅下降 2.09 点。两个不同架构的扩散模型表现出一致的模式，强有力地证明：探测到的少量神经元与文化语义之间存在直接的因果关系。

![[assets/figures/papers/paper_list_l2365_https_arxiv_org_abs_2511_17282/figures/008_Table_1.jpg]]
*Table 1: Validating Culture-Sensitive Neuron Detection in PEA-Diffusion. Neuronal accuracy on the test subset with “cultural style modifier + noun” prompts*

### 主要定量结果：与 SOTA 方法的全面对比

Table 2 系统对比了所提方法与多个主流文本到图像模型在 CultureBench 测试子集（仅名词提示）上的表现。评估覆盖四个维度：文化一致性（CultureVQA）、文本-图像对齐（CLIPScore）、人类偏好对齐（ImageReward）和感知相似度（LPIPS）。

![[assets/figures/papers/paper_list_l2365_https_arxiv_org_abs_2511_17282/figures/009_Table_2.jpg]]
*Table 2: Quantitative comparisons with SOTA methods. Using the “noun-only” prompts on the test subset. The best performance is marked in bold, and the second-best is underlined*

**文化一致性（CultureVQA）** 方面，微调方案（Fine-Tuned Layer Enhancer）以 36.63 取得最优，零训练方案（Zero-Training Neuron Amplifier）以 33.91 紧随其后。相比之下，通用模型如 StableDiffusion 3.5（25.13）、FLUX.1-dev（24.98）、Show-o2（24.30）表现平平，而专门面向多语言的 PEA-Diffusion（21.65）和 AltDiffusion（23.05）甚至更低。所提方法在 AltDiffusion 和 PEA-Diffusion 上分别取得 +14.98 和 +12.32 的 CultureVQA 增益，证明文化一致性的提升并非来自更强的基座模型，而是来自针对性的文化神经元干预。

**文本-图像对齐（CLIPScore）** 方面，零训练方案（0.291）和微调方案（0.290）均超越 AltDiffusion（0.282）和 PEA-Diffusion（0.253），表明文化增强并未以牺牲语义保真度为代价。**人类偏好（ImageReward）** 方面，零训练方案（0.33）和微调方案（0.31）大幅领先 AltDiffusion（-0.11）和 PEA-Diffusion（-0.65），说明增强后的生成结果在整体视觉质量上也更受偏好模型认可。**感知相似度（LPIPS）** 方面，所提方法均取得最低值，表明生成图像与参考分布的结构一致性更好。

### 消融实验：增益来源的归因

Table 3 的消融实验旨在回答一个关键问题：性能增益究竟来自定向的文化神经元增强，还是来自任何形式的特征扰动？实验在 AltDiffusion 和 PEA-Diffusion 上分别测试了零训练和微调两种方案，并引入“随机增强”作为对照——即随机选择与 Top-K 等量的神经元进行相同幅度的放大。

![[assets/figures/papers/paper_list_l2365_https_arxiv_org_abs_2511_17282/figures/014_Table_3.jpg]]
*Table 3: Ablation studies on CultureBench. On the CultureBench test subset, we conducted ablation analyses of two methods under both zero-training and fine-tuned settings. The best performance is marked in bold*

结果显示，零训练方案在 AltDiffusion 上 CultureVQA 增益达 7.01，在 PEA-Diffusion 上达 12.26；微调方案增益分别增至 9.61 和 14.98。而随机增强在 AltDiffusion 上几乎无增益（+0.70），在 PEA-Diffusion 上甚至出现负增益（-0.70）。这清晰地证明，增益来源于对文化敏感神经元的精准定位与放大，而非对任意神经元的扰动。微调方案之所以优于零训练方案，可归因于其通过 CultureBench 中的文化参考图像进行了自适应优化，能够更精细地调整增强幅度。

### 超参数敏感性分析

零训练方案的核心超参数是放大系数 λ。Figure 11 展示了 CultureVQA 随 λ 变化的定量曲线：λ 从 0 增至 7 时，CultureVQA 从基线 21.65 逐步攀升至峰值 35.92；当 λ 继续增大至 8 时，CultureVQA 回落至 34.93。Figure 10 提供了对应的定性可视化，λ 从 0 到 8 变化时，生成图像的文化风格逐渐增强，但过大的 λ 会引入视觉伪影或风格过饱和。这一现象表明，文化神经元的激活强度需要适中：过弱不足以触发文化表征，过强则可能破坏文本编码器输出的整体平衡，损害生成质量。

### 跨域泛化能力

Table 6 评估了微调方案在 100 条域外描述（out-of-distribution captions）上的泛化性能。在 PEA-Diffusion 上，微调方案将 CultureVQA 从 15.00 提升至 35.00（+20.00）；在 AltDiffusion 上，从 15.00 提升至 32.00（+17.00）。这一结果表明，文化敏感神经元捕捉的是通用的文化语义表征，而非对训练集中特定提示的过拟合，所提方法具备良好的跨域迁移能力。

![[assets/figures/papers/paper_list_l2365_https_arxiv_org_abs_2511_17282/figures/021_Table_6.jpg]]
*Table 6: Quantitative analysis across domains. Generate using 100 captions from outside the domain and calculate the performance of CultureVQA. Bold rows mark the highest performance within each baseline group*

### 用户研究：人类评估的交叉验证

尽管 CultureVQA 自动化评估效率高，但其可靠性需要通过人类判断进行交叉验证。Table 4 显示，CultureVQA 与人类专家在 CultureBench 上的判断一致性达到 91.57%，而人类专家之间的一致性为 94.18%，两者差距仅约 2.6 个百分点，说明自动评估具有较高可靠性。在此基础上，Figure 9 展示了在 CultureBench 平台上进行的用户研究结果（50 位专家参与），评估三个维度：文化匹配正确率（MCC）、风格一致性（SCC）和文化语义相关性（CSR，1-5 分制）。所提方法在 CSR 上取得 77.6 分，显著优于第二名的 60.4 分（+17.2），进一步验证了文化一致性的实质性提升。

### 失败模式与局限性

尽管所提方法在定量和定性评估上均取得了显著提升，但仍存在若干值得关注的失败模式：

1. **文化覆盖的局限性**：CultureBench 目前仅涵盖 15 个文化区域，仅占全球文化多样性的一小部分。对于互联网影像记录较少的低资源或边缘化社区，基准构建依赖于公开可用的图像资源，因此可能遗漏这些群体。在这些未被探测的文化上，方法的有效性需要人工验证。

2. **模型迁移的成本**：当切换到新架构的模型时，如果文本编码器发生变化，需要重新执行文化敏感层和神经元的探测步骤。虽然探测过程本身无需训练，但仍需要该文化区域的标注数据来计算 ∆CA 和加权频率分数，这增加了实际部署时的前期成本。

3. **自动化评估的边界**：尽管 CultureVQA 与人类判断高度一致，但 Table 4 中约 2.6% 的一致性差距提示，自动化指标仍无法完全捕捉人类感知的细微文化差异。在涉及高度语境化的文化符号或次文化群体时，CultureVQA 的判断可能需要人工复核。

## 定位与知识库关联

### 与基线工作的关系

本文工作立足于当前多语言文本到图像（T2I）生成模型的文化表现力不足这一核心问题。所对比的基线模型覆盖了当前主流架构谱系：

- **通用大规模文生图模型**：包括 **StableDiffusion XL**（Podell et al., 2023）、**StableDiffusion 3.5**（Stability AI, 2024）和 **FLUX.1-dev**（Black Forest Labs, 2024）。这些模型在英语场景下表现优异，但在仅使用名词提示（noun-only prompts）的多语言场景中，其生成图像的文化一致性显著不足，CultureVQA得分普遍偏低（如StableDiffusion 3.5仅为25.13），暴露出预训练数据分布与文本编码器表征的英语文化中心主义倾向。

- **多语言对齐扩散模型**：**PEA-Diffusion**（Zhang et al., 2024）和 **AltDiffusion**（Chen et al., 2023）是本文最核心的对比基线。两者均针对跨语言文本编码对齐进行了专门设计，理论上应具备更强的多语言理解能力。然而，在CultureBench测试子集上，PEA-Diffusion和AltDiffusion的CultureVQA分别仅为21.65和23.05，表明即使经过跨语言对齐，模型在缺乏显式文化触发信号时仍无法自发激活文化语义表征。这一发现构成了本文方法论的直接动机：问题不在于知识的缺失，而在于知识的激活机制失效。

- **多模态统一模型**：**Show-o2**（Pan et al., 2025）作为架构多样性基线被纳入比较，进一步验证了文化表征不足并非特定架构的孤立问题，而是当前T2I范式的系统性缺陷。

本文提出的两种策略——**零训练神经元放大器**和**微调层增强器**——在方法论上具有明确的差异化定位：不同于上述基线对模型进行全参数训练或完全冻结，本文方法通过文化敏感层和神经元的精确定位，实现了对文化表征的靶向干预。零训练方案在推理时通过手工系数λ放大少量文化敏感神经元的SAE隐变量，无需任何参数更新；微调方案仅在检测到的单一文化敏感层中插入轻量残差模块，训练参数量极小，骨干网络完全冻结。这种“探测-干预”范式在保持模型整体保真度与多样性的前提下，实现了文化一致性的显著提升。

### 适用边界与局限性

尽管本文方法在两个不同架构的扩散模型（PEA-Diffusion和AltDiffusion）上均验证了有效性，其适用边界仍需审慎界定：

1. **文化覆盖范围的局限**：CultureBench目前仅涵盖15个语言区域，仅占全球文化多样性的一小部分。许多低资源语言、少数民族文化以及互联网影像记录较少的文化群体未被充分代表。基准构建依赖于公开可用的图像资源，这本身就可能遗漏某些在数字空间中表征不足的文化群体和子文化。方法在这些未被覆盖的文化上的有效性尚需进一步验证。

2. **模型架构依赖性**：当前的文化敏感层与神经元检测流程依赖于文本编码器的注意力机制和SAE稀疏编码。当切换到文本编码器架构发生本质变化的新模型时（例如采用更强的多语言编码器或不同的注意力机制），可能需要重新执行完整的探测步骤。这增加了方法在实际部署中的迁移成本，尚未发展为模型无关的通用探测框架。

3. **评估指标的局限性**：文化一致性的评估主要依赖于CultureVQA这一自动化指标。尽管Table 4显示VQA模型与人类专家的一致性达到91.57% vs 94.18%，表明自动评估具有较高可靠性，但其仍无法完全捕捉人类感知的细微文化差异。用户研究（50位专家，CSR评分）提供了重要补充验证，但在更大规模、更多样化的文化场景下，评估体系的完备性仍有待加强。

4. **微调方案的训练信号**：微调层增强器使用像素级MSE损失直接与CultureBench中的文化参考图像对齐。虽然该方法在CultureVQA上取得了最高分（36.63），但MSE损失并非文化一致性的理想度量——它倾向于鼓励生成图像与参考图像的像素级相似性，而非捕捉更高层次的文化语义特征。这可能导致对特定参考图像的过拟合风险，而非真正学习到可泛化的文化表征。

### 开放问题

1. **文化覆盖的扩展与去偏**：如何将CultureBench扩展至更多语言和地区（包括方言和少数民族文化），并确保新增文化区域的标注同样保持高保真和去偏？这不仅是数据规模的问题，更涉及文化表征的伦理和认识论挑战——谁有权定义某种文化的“典型”视觉特征？

2. **模型无关的通用探测框架**：在文本编码器架构发生本质变化的情况下（例如更强的多语言编码器或非Transformer架构），当前的文化层与神经元检测方法是否依然能定位到一致的文化子空间？能否发展为一种模型无关的通用探测框架，使得文化敏感表征的定位成为可迁移的标准化流程？

3. **文化对齐目标的优化**：本文微调方案使用的像素级MSE损失虽有训练指导作用，但并非文化一致性的理想度量。能否设计出更直接的文化对齐目标（如对抗式或对比式学习）来进一步提升文化保真度？例如，是否可以构建文化语义的对比损失，使同一文化域的生成图像在特征空间中彼此靠近，而与其他文化域拉开距离？

4. **多文化场景的自适应机制**：当同时处理多个文化领域时，如何在线自适应地选择或组合不同的文化神经元集，而无需为每一组文化单独执行探测和微调？当前方法中，不同文化对应的敏感神经元集可能存在重叠或互斥，如何高效管理和调度这些文化特异性表征是一个实际部署中亟待解决的问题。

5. **规模化的文化控制范式**：随着文生图模型规模不断增大，是否可能通过类似任务向量或提示工程的方式更简单地实现文化控制，而避免复杂的神经元级定位？图13的初步证据表明，在固定英文提示下激活不同文化神经元集即可将输出引导至不同文化风格，这暗示文化表征可能具有某种可加性。探索更轻量、更可扩展的文化控制机制是值得深入的方向。

## 原文 PDF

![[paperPDFs/CVPR_2026/Where_Culture_Fades_Revealing_the_Cultural_Gap_in_Text_to_Image_Generation.pdf]]
