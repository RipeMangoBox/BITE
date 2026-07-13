---
title: "DCoAR: Deep Concept Injection into Unified Autoregressive Models for Personalized Text-to-Image Generation"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/DCoAR_Deep_Concept_Injection_into_Unified_Autoregressive_Models_for_Personalized_Text_to_Image_Generation.pdf
project_link: null
code_link: null
aliases:
- DCoAR
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/generative_models_diffusion
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: 深层概念注入策略：将可学习的多模态上下文令牌注入多个Transformer层（LMCL），实现持续的特征强化和跨模态交互。
primary_logic: 通过层间多模态上下文学习（LMCL）实现深度注入，并以双重先验保持（DPP）和上下文感知自正则化（CASR）稳定训练，在保持骨干网络冻结的同时弥合与微调方法的保真度差距，并支持免训练的主体-风格组合。
claims:
- DCoAR在DreamBench上的CLIP-I达到0.8151，超过所有对比方法，包括需要微调大量参数的Proxy-Tuning (0.809)。
- 消融实验表明，LMCL+DPP+CASR组合达到最优DINO 0.7226和CLIP-I 0.8151。
- 深层注入优于浅层注入，但过深（24层）会导致过拟合，最佳深度为9层。
- Identity Mask消融表明，不加掩码会导致概念污染，而加入掩码可干净地分离主体与风格。
---

# DCoAR: Deep Concept Injection into Unified Autoregressive Models for Personalized Text-to-Image Generation

> [!tip] 核心洞察
> 通过层间多模态上下文学习（LMCL）实现深度注入，并以双重先验保持（DPP）和上下文感知自正则化（CASR）稳定训练，在保持骨干网络冻结的同时弥合与微调方法的保真度差距，并支持免训练的主体-风格组合。

| 字段 | 内容 |
|------|------|
| 中文题名 | DCoAR：统一自回归模型中的深度概念注入个性化图像生成 |
| 英文题名 | DCoAR: Deep Concept Injection into Unified Autoregressive Models for Personalized Text-to-Image Generation |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2508.07341) |
| Topic | #topic/vision_multimodal_applications #topic/generative_models_diffusion #topic/vision_multimodal_applications/image_and_video_generation |
| Method | DCoAR |
| Dataset | DreamBench, Style personalization |

> [!tip] 效果简介
> - DreamBench 上，CLIP-I 0.815 vs DreamBooth (Imagen) 0.812 (+0.003)；CLIP-T 0.318 vs Proxy-Tuning 0.312 (+0.006)。
> - Style personalization (StyleDrop+ZipLoRA evaluation) 上，Text-alignment 0.308 vs ZipLoRA 0.272 (+0.036)。

## 概要

**问题瓶颈**：统一自回归（Unified AR）模型在文本到图像生成中展现出高效性与可扩展性，但其个性化方法普遍存在**浅层注入瓶颈**——现有方案仅在输入层注入概念令牌，导致语义信号随网络深度衰减，视觉保真度差、重文本化能力弱。微调方法虽能提升保真度，却需要大量可训练参数，牺牲了AR模型的推理效率优势。

**核心方法**：DCoAR 提出**深层概念注入**范式，通过**层间多模态上下文学习（LMCL）**将可学习的文本与图像上下文令牌注入多个Transformer层，实现持续的特征强化与跨模态交互。训练中引入**双重先验保持（DPP）**损失（结合类NTP损失与KL散度）以缓解语义漂移，以及**上下文感知自正则化（CASR）**损失以约束令牌嵌入、防止过拟合。推理时，**Identity Mask** 机制实现免训练的主体-风格组合。

**关键结论**：
- 在 DreamBench 主体个性化上，DCoAR 以 **CLIP-I 0.815** 超越所有对比方法（包括需微调142.6M参数的 Proxy-Tuning 的 0.809），而自身仅需 **0.073M 可训练参数**。
- 风格个性化任务中，文本对齐指标达到 **0.308**，显著优于 ZipLoRA 的 0.272。
- 消融实验证实 LMCL+DPP+CASR 组合取得最优综合性能（DINO 0.7226，CLIP-I 0.8151）；注入深度过深（24层）会导致过拟合，最佳深度为9层。
- Identity Mask 有效隔离主体与风格令牌，避免语义污染，实现干净组合。

**方法定位**：DCoAR 属于**概念注入**路线，在冻结骨干网络的前提下，以极低参数量弥合了与微调方法的保真度差距，并首次在统一AR模型中实现免训练的主体-风格组合，为高效个性化生成提供了新基准。



文本到图像生成领域正经历从扩散模型到统一自回归模型的范式迁移。以 Lumina-mGPT 为代表的多模态自回归模型将图像离散化为视觉令牌序列，与文本令牌统一建模，在生成效率与扩展性上展现出潜力。然而，这类模型的个性化生成仍面临一个核心瓶颈：**浅层注入导致的语义衰减**。

现有面向统一自回归模型的个性化方法——如 **Yo'Chameleon**（Nguyen et al., CVPR 2025）和 **UniCTokens**（An et al., arXiv 2025）——均采用“概念注入”范式：冻结骨干网络，仅在输入层插入少量可学习的上下文令牌来表示目标主体或风格。这种浅层注入策略虽参数高效，但概念信号在逐层前向传播中逐渐衰减，导致高层特征中主体语义被稀释，最终生成结果出现视觉保真度下降和重文本化能力不足的问题。相比之下，基于微调的方法（如 DreamBooth 结合 FLUX 或 LoRA 适配）虽能保持较高保真度，却需要训练大量参数（如 Proxy-Tuning 达 142.6M），并面临语义漂移和身份偏移风险。

上述矛盾揭示了一个关键问题：**能否在保持骨干网络完全冻结的前提下，通过改变概念信号的注入方式，弥合注入方法与微调方法之间的保真度差距？**

DCoAR 的动机正源于此。其核心假设是：概念表示不应仅停留在输入层，而应深度嵌入网络的多个 Transformer 层，实现持续的特征强化与跨模态交互。这一假设引出了三个递进的技术挑战：

1. **如何设计深层注入机制**，使可学习的多模态上下文令牌在多个层中持续发挥作用，而非仅作为输入前缀？
2. **如何防止深层注入带来的过拟合和语义漂移**，在增强主体保真度的同时保持文本控制力？
3. **如何实现免训练的主体-风格组合**，使独立学习的概念令牌在推理时可任意拼接而不产生语义污染？

DCoAR 通过层间多模态上下文学习（LMCL）、双重先验保持（DPP）和上下文感知自正则化（CASR）三项协同设计，系统性地回应了上述挑战，在 DreamBench 基准上以仅 0.073M 可训练参数取得了超越微调方法的性能（CLIP-I 0.8151，CLIP-T 0.3184）。



## 核心方法与创新机理

DCoAR 的核心创新在于将统一自回归（AR）模型的个性化从“浅层注入”范式推进到“深层概念注入”范式，并通过三项配套机制解决深层注入带来的训练稳定性与语义漂移问题，最终在保持骨干网络完全冻结的前提下，弥合了概念注入方法与微调方法之间的保真度差距。

### 从浅层注入到深层注入：LMCL

现有统一 AR 模型的个性化方法（如 **Yo'Chameleon** (Nguyen et al., CVPR 2025)、**UniCTokens** (An et al., arXiv 2025)）普遍采用**浅层注入**策略——仅在输入层将可学习的令牌拼接到文本序列中。这种方式存在一个根本性瓶颈：概念信号仅作用于模型的最前端，随着网络深度增加，语义信息逐渐衰减，导致视觉保真度和重文本化能力不足。

DCoAR 提出了**逐层多模态上下文学习（Layer-wise Multimodal Context Learning, LMCL）**，将可学习的多模态上下文令牌注入到多个 Transformer 层中。具体而言，在第 $i$ 个 Transformer 层，令牌序列被构造为：

$$\mathbf{U}_i' = \{ \mathbf{y}_1, \mathbf{y}_2, \dots, \mathbf{p}_{[v]}^{(i)}, \dots, \mathbf{y}_L, \mathbf{p}_I^{(i)}, \mathbf{x}_1, \mathbf{x}_2, \dots, \mathbf{x}_T \}$$

其中 $\mathbf{p}_{[v]}^{(i)}$ 和 $\mathbf{p}_I^{(i)}$ 分别是注入到第 $i$ 层的文本上下文令牌和图像上下文令牌。这种设计使概念表征能够在多个层级上持续强化，实现跨模态特征的深度交互，从根本上解决了浅层注入的语义衰减问题。消融实验证实，注入深度为 9 层时达到最佳平衡（DINO 0.7226），而过度注入（24 层）会导致过拟合，降低主体保真度。

### 双重先验保持（DPP）：防止语义漂移

深层注入虽然增强了概念表征能力，但也引入了新的风险：可学习令牌可能过度偏离预训练模型的先验分布，导致语言漂移和过拟合。为此，DCoAR 设计了**双重先验保持（Dual Prior Preservation, DPP）**正则化损失：

$$\mathcal{L}_{DPP} = \lambda_1 \cdot \mathcal{L}_{NTP_{cls}}(\mathrm{logits}_{prior}, \mathrm{labels}_{cls}) + \lambda_2 \cdot D_{KL}(\mathrm{logits}_{zs} \parallel \mathrm{logits}_{prior})$$

DPP 包含两个互补的约束项：第一项是类图像 NTP 损失，强制模型在给定类别标签时仍能生成合理的图像分布；第二项是零样本预测与先验预测之间的 KL 散度，防止定制化分布过度偏离预训练分布。消融实验表明，两项缺一不可——仅使用 KL 散度会降低 DINO 和 CLIP-I，仅使用类 NTP 损失则会损害 CLIP-T。

### 上下文感知自正则化（CASR）：增强重文本化能力

DPP 解决了语义层面的漂移问题，但在嵌入空间层面，深层注入的图像上下文令牌仍可能偏离主体的真实嵌入分布，导致重文本化（re-contextualization）能力下降。DCoAR 进一步引入**上下文感知自正则化（Context-Aware Self-Regularization, CASR）**损失：

$$\mathcal{L}_{CASR} = \frac{1}{N} \sum_{i=1}^{N} \| \mathbf{p}_I^{(i)} - \mathbf{E}_{subject}^{(i)} \|^2$$

CASR 将每一层注入的图像上下文令牌 $\mathbf{p}_I^{(i)}$ 约束到预训练模型为该主体生成的嵌入 $\mathbf{E}_{subject}^{(i)}$ 附近。这种“锚定”机制有效防止了令牌在训练过程中过度漂移，显著提升了模型在新的文本提示下对主体进行灵活重文本化的能力。

### 免训练的主体-风格组合与 Identity Mask

与需要额外训练或微调的组合方法（如 **B-LoRA** (Frenkel et al., ECCV 2024)、**ZipLoRA** (Shah et al., ECCV 2024)）不同，DCoAR 支持**免训练的主体-风格组合**：推理时直接将主体令牌和风格令牌拼接即可。为防止两种概念之间的语义污染（如颜色泄漏），DCoAR 引入了 **Identity Mask** 机制，在推理时限制主体令牌与风格令牌之间的注意力流，实现干净的概念解耦。消融实验证实，去除 Identity Mask 会导致明显的概念污染。

### 最终目标函数

上述三项机制通过统一的训练目标进行平衡：

$$\mathcal{L}_{obj} = \mathcal{L}_{NTP} + \alpha \mathcal{L}_{DPP} + \beta \mathcal{L}_{CASR}$$

其中 $\mathcal{L}_{NTP}$ 是标准的自回归下一令牌预测损失，$\alpha$ 和 $\beta$ 为平衡系数。整个训练过程仅需约 0.073M 可训练参数（远低于 Proxy-Tuning 的 142.6M），在单张 H800 GPU 上即可完成，骨干网络完全保持冻结状态。



DCoAR 是一个面向统一自回归（AR）多模态模型的个性化生成框架，其核心设计目标是在**完全冻结骨干网络**的前提下，通过深层概念注入与多面正则化，弥合概念注入方法与微调方法之间的保真度差距。整个 pipeline 由三个训练阶段模块和一个免训练推理模块构成，形成“深层注入—先验保持—自正则化—推理隔离”的闭环。

### 输入与输出流

框架的输入包括：① 一张或数张主体参考图像；② 一个描述生成任务的文本提示。输出为符合文本语义且保持主体视觉身份的高保真图像。在训练阶段，系统仅优化一组可学习的多模态上下文令牌，骨干网络参数完全冻结；在推理阶段，通过拼接已学习的主体令牌与风格令牌，可实现免训练的主体–风格组合生成。

### 模块关系与数据流

**1. 层间多模态上下文学习（LMCL）**  
LMCL 是整个框架的注入核心。与仅在输入层插入令牌的浅层策略不同，DCoAR 将一组共享的可学习上下文令牌 $\mathbf{P} = \{ \mathbf{p}_{[v]}, \mathbf{p}_I \}$ 同时注入多个 Transformer 层。具体而言，在第 $i$ 个 Transformer 层，文本令牌 $\mathbf{p}_{[v]}^{(i)}$ 和图像令牌 $\mathbf{p}_I^{(i)}$ 被插入到序列的特定位置，形成增强的输入序列 $\mathbf{U}_i'$（Eq. 7）。这一设计使得概念信号能够在网络深度方向上持续强化，避免浅层注入带来的语义衰减，同时促进文本与图像模态在多层上的跨模态交互。默认配置下，主体个性化注入前 9 层，风格个性化注入前 3 层。

**2. 双重先验保持（DPP）**  
DPP 作为正则化器，直接作用于模型的输出分布，防止概念学习过程中的语义漂移和语言遗忘。其损失函数由两项加权组成（Eq. 8）：① 类 NTP 损失 $\mathcal{L}_{NTP_{cls}}$，约束定制模型在类别标签上的预测与冻结的先验模型一致；② KL 散度项 $D_{KL}$，约束零样本生成分布不偏离先验分布。DPP 在训练时与主损失并行计算，梯度仅回传至上下文令牌。

**3. 上下文感知自正则化（CASR）**  
CASR 在嵌入空间层面施加约束（Eq. 10），将每层注入的图像上下文令牌 $\mathbf{p}_I^{(i)}$ 拉向预训练模型为该主体生成的嵌入 $\mathbf{E}_{subject}^{(i)}$。这一设计同时起到初始化和正则化的双重作用：初始化阶段，CASR 为上下文令牌提供语义锚点，加速收敛；训练过程中，CASR 防止令牌过度偏离主体嵌入空间，从而抑制过拟合并显著提升重文本化能力。

**4. 总体训练目标**  
最终训练损失为三项损失的加权和（Eq. 11）：
$$\mathcal{L}_{obj} = \mathcal{L}_{NTP} + \alpha \mathcal{L}_{DPP} + \beta \mathcal{L}_{CASR}$$
其中 $\mathcal{L}_{NTP}$ 为自回归标准下一令牌预测损失，$\alpha$ 和 $\beta$ 为平衡系数。整个训练仅优化 0.073M 参数（单张 H800 GPU），远低于基于 LoRA 的适配方法。

**5. 免训练主体–风格组合（推理阶段）**  
在推理时，DCoAR 通过直接拼接已学习的主体上下文令牌与风格上下文令牌，实现即插即用的组合生成。为防止主体与风格令牌之间发生语义污染（如颜色泄漏），框架引入 **Identity Mask** 机制，在注意力计算中限制主体令牌与风格令牌之间的注意力流，强制实现干净的概念解耦。

### 框架总览

图 2 给出了 DCoAR 的完整框架示意图：子图 (a) 展示 LMCL 的多层注入机制；子图 (b) 展示 DPP 的双重先验约束；子图 (c) 展示 CASR 的嵌入空间正则化；子图 (d) 展示推理时的免训练组合与 Identity Mask。四个模块协同工作，使得 DCoAR 在保持骨干网络冻结的条件下，取得了与微调方法可比甚至更优的主体保真度与文本对齐性能。

### 补充图表

![[assets/figures/papers/paper_list_l2303_https_arxiv_org_abs_2508_07341/figures/002_Figure_2.jpg]]
*Figure 2: Overview of the proposed DCoAR framework for subject-driven personalization in multi-modal autoregressive models. (a) Layerwise Multimodal Context Learning, where learnable context tokens are injected into multiple Transformer layers for concept representation. (b) Dual Prior Preservation (DPP) regularizes the customized distribution against the pre-trained model to mitigate overfitting and language drift. (c) Context-Aware Self-Regularization (CASR) initializes and constrains context tokens towards the subject embedding space to enhance fidelity and re-contextualization. (d) Training-free subject–style composition by directly combining subject and style tokens to enable flexible customized...*



DCoAR 的核心由四个模块构成：**层间多模态上下文学习（LMCL）** 实现深层概念注入，**双重先验保持（DPP）** 防止语义漂移，**上下文感知自正则化（CASR）** 抑制过拟合，以及推理阶段的 **Identity Mask** 实现免训练主体-风格组合。

### 3.1 基础自回归生成范式

给定文本提示 $\mathbf{y} = \{ \mathbf{y}_1, \mathbf{y}_2, \ldots, \mathbf{y}_L \}$，其中每个文本令牌来自词表 $\mathcal{V}$，统一自回归模型将图像生成建模为序列到序列的令牌预测问题。目标图像被量化为离散令牌序列 $\mathbf{x} = \{ \mathbf{x}_1, \mathbf{x}_2, \ldots, \mathbf{x}_T \}$，模型以自回归方式逐令牌预测。标准训练目标为下一令牌预测损失（NTP）：

$$
\mathcal{L}_{\mathrm{NTP}} = - \sum_{t=1}^{T} \log p_{\theta}(\mathbf{x}_t \mid \mathbf{x}_{<t}, \mathbf{y})
$$

该损失仅驱动模型拟合目标图像分布，不具备概念注入和个性化能力。

### 3.2 层间多模态上下文学习（LMCL）

**瓶颈**：现有统一自回归模型的个性化方法（如 Yo'Chameleon、UniCTokens）仅在输入层注入概念令牌，语义信号随 Transformer 深度逐层衰减，导致视觉保真度不足和重文本化能力差。

**方案**：LMCL 将一组共享的可学习多模态上下文令牌 $\mathbf{P} = \{ \mathbf{p}_{[v]}, \mathbf{p}_I \}$ 注入到多个 Transformer 层中，实现持续的特征强化。其中 $\mathbf{p}_{[v]}$ 为文本模态上下文令牌，$\mathbf{p}_I$ 为图像模态上下文令牌。在第 $i$ 个 Transformer 层，令牌序列被重组为：

$$
\mathbf{U}_i' = \{ \mathbf{y}_1, \mathbf{y}_2, \dots, \mathbf{p}_{[v]}^{(i)}, \dots, \mathbf{y}_L, \mathbf{p}_I^{(i)}, \mathbf{x}_1, \mathbf{x}_2, \dots, \mathbf{x}_T \}
$$

文本上下文令牌插入在文本提示序列中，图像上下文令牌插入在文本提示与图像令牌序列之间。每一层的上下文令牌通过该层的自注意力与前馈网络进行跨模态交互，使概念信号贯穿网络深层。骨干网络参数完全冻结，仅训练上下文令牌。

**深度选择**：消融实验表明，注入前 9 层达到最佳平衡（DINO 0.7226, CLIP-I 0.8151）；过深（24 层）会导致过拟合，损害文本控制能力。

### 3.3 双重先验保持（DPP）

**瓶颈**：仅使用 NTP 损失训练上下文令牌会破坏预训练模型的先验分布，导致语义漂移——模型逐渐遗忘原始文本到图像的映射能力。

**方案**：DPP 损失从两个维度约束定制化分布与预训练先验的一致性：

$$
\mathcal{L}_{DPP} = \lambda_1 \cdot \mathcal{L}_{NTP_{cls}}(\mathrm{logits}_{prior}, \mathrm{labels}_{cls}) + \lambda_2 \cdot D_{KL}(\mathrm{logits}_{zs} \parallel \mathrm{logits}_{prior})
$$

- **第一项** $\mathcal{L}_{NTP_{cls}}$：类图像 NTP 损失。给定仅包含类别词（不含主体标识符）的文本提示，要求模型生成的图像令牌分布与预训练先验一致。该项维持模型的类别级语义理解能力。
- **第二项** $D_{KL}(\mathrm{logits}_{zs} \parallel \mathrm{logits}_{prior})$：零样本-先验分布的 KL 散度。约束注入概念令牌后模型的输出分布不偏离冻结骨干网络的零样本分布，防止语言漂移。

消融实验证实，两项缺一不可：仅保留 KL 散度会降低 DINO 和 CLIP-I，仅保留类 NTP 损失会降低 CLIP-T。

### 3.4 上下文感知自正则化（CASR）

**瓶颈**：深层注入虽增强保真度，但上下文令牌可能偏离主体嵌入空间，导致过拟合——生成图像与参考图像高度相似但丧失可编辑性。

**方案**：CASR 在训练过程中约束图像上下文令牌 $\mathbf{p}_I^{(i)}$ 与预训练模型生成的主体嵌入 $\mathbf{E}_{subject}^{(i)}$ 保持接近：

$$
\mathcal{L}_{CASR} = \frac{1}{N} \sum_{i=1}^{N} \| \mathbf{p}_I^{(i)} - \mathbf{E}_{subject}^{(i)} \|^2
$$

其中 $\mathbf{E}_{subject}^{(i)}$ 由冻结的骨干网络在无上下文令牌条件下对主体图像编码得到，$N$ 为注入层数。该损失将上下文令牌锚定在主体的语义流形上，既保持身份保真度，又保留足够的编辑空间以支持重文本化。

### 3.5 总体训练目标

最终训练损失为三项损失的加权组合：

$$
\mathcal{L}_{obj} = \mathcal{L}_{NTP} + \alpha \mathcal{L}_{DPP} + \beta \mathcal{L}_{CASR}
$$

其中 $\alpha$ 和 $\beta$ 为平衡系数。三项损失协同作用：NTP 驱动概念学习，DPP 保持先验分布，CASR 防止过拟合并增强重文本化能力。

### 3.6 推理阶段：Identity Mask 免训练组合

在推理时，主体和风格的上下文令牌可直接拼接实现免训练组合。为防止主体令牌与风格令牌之间的注意力污染（如颜色泄漏），DCoAR 引入 Identity Mask——在自注意力计算中阻断主体令牌与风格令牌之间的注意力流，强制实现干净的主体-风格解耦。消融实验证实，去除该掩码会导致语义污染，加入后可干净分离主体与风格。

### 补充图表

![[assets/figures/papers/paper_list_l2303_https_arxiv_org_abs_2508_07341/figures/011_Figure_7.jpg]]
*Figure 7: Impacts of insertion depth of multimodal context tokens on performance*

![[assets/figures/papers/paper_list_l2303_https_arxiv_org_abs_2508_07341/figures/012_Figure_9.jpg]]
*Figure 9: Ablation results of Identity Mask*

![[assets/figures/papers/paper_list_l2303_https_arxiv_org_abs_2508_07341/figures/016_Figure_10.jpg]]
*Figure 10: Visualization of CASR*



## 实验与关键发现

### 主体个性化主结果：DreamBench

DCoAR 在 DreamBench 基准上以仅 **0.073M** 可训练参数（单张 H800 GPU 训练）取得了与微调方法相当甚至更优的性能。Table 1 报告了核心指标对比：

- **CLIP-I（主体保真度）**：DCoAR 达到 **0.8151**，超过所有对比方法，包括需要微调 142.6M 参数的 Proxy-Tuning（0.809）和 DreamBooth（Imagen）（0.812）。
- **CLIP-T（文本对齐度）**：DCoAR 达到 **0.3184**，领先于 Proxy-Tuning（0.312）和 UniCTokens（0.306）。
- **DINO（主体相似度）**：DCoAR 达到 **0.7226**，同样处于领先水平。

这一结果的关键在于深层概念注入策略。Figure 3 的定性对比显示，浅层注入方法（如 Yo'Chameleon、UniCTokens）普遍存在视觉保真度不足的问题，而 DCoAR 通过 LMCL 在多个 Transformer 层持续强化概念特征，生成的图像在细节保持和语义一致性上均优于同类概念注入方法，并弥合了与基于 LoRA 的微调方法之间的保真度差距。

![[assets/figures/papers/paper_list_l2303_https_arxiv_org_abs_2508_07341/figures/004_Figure_3.jpg]]
*Figure 3: Qualitative comparison of subject-driven personalization on the DreamBench benchmark. As concept-injection methods generally exhibit lower visual fidelity, we focus the qualitative comparison on the more competitive adaptation-based methods. Additional comparisons are available in the supplementary material*

### 风格个性化主结果

在风格个性化任务上，DCoAR 同样展现出竞争力。Table 2 显示，DCoAR 的文本对齐度达到 **0.308**，显著高于 ZipLoRA 的 0.272（+0.036），而风格相似度（0.715 vs 0.712）与 B-LoRA（0.717）基本持平。值得注意的是，DCoAR 在此任务中仅将概念令牌注入前 **3 层** Transformer，且完全冻结骨干网络，而对比方法均需要微调或训练 LoRA 适配器。

![[assets/figures/papers/paper_list_l2303_https_arxiv_org_abs_2508_07341/figures/005_Table_2.jpg]]
*Table 2: Comparison results of our DCoAR and two competitors on the style personalization task*

### 消融实验：损失函数组合

Table 3 的消融实验系统验证了各损失组件的贡献。以仅使用 NTP 损失的 LMCL 为基线（DINO 0.6957, CLIP-I 0.7895, CLIP-T 0.3117）：

![[assets/figures/papers/paper_list_l2303_https_arxiv_org_abs_2508_07341/figures/009_Table_3.jpg]]
*Table 3: Impacts of different losses on the subject-driven personalization task*

- **+DPP**：DINO 提升至 0.7121，CLIP-I 提升至 0.8033，表明双重先验保持有效抑制了语义漂移。
- **+CASR**：CLIP-T 提升至 0.3153，验证了上下文自正则化对重文本化能力的增强。
- **LMCL + DPP + CASR（完整方案）**：达到最优综合性能，DINO **0.7226**，CLIP-I **0.8151**，CLIP-T **0.3184**。

Figure 8 的可视化进一步佐证：缺少 DPP 时生成样本出现明显的语义漂移（主体特征偏离参考图像），缺少 CASR 时重文本化能力下降（无法准确响应文本提示中的场景变化）。

![[assets/figures/papers/paper_list_l2303_https_arxiv_org_abs_2508_07341/figures/010_Figure_8.jpg]]
*Figure 8: Visualization of the effects of different losses on the generated samples*

### DPP 内部消融

Table 6 深入分析了 DPP 损失的两个组成部分：

![[assets/figures/papers/paper_list_l2303_https_arxiv_org_abs_2508_07341/figures/015_Table_6.jpg]]
*Table 6: Ablation study on the individual components of the Dual Prior Preservation (DPP) loss using the DreamBench dataset*

- 仅使用 KL 散度（$\lambda_1=0$）：DINO 和 CLIP-I 均下降，说明类 NTP 损失对保持主体视觉特征至关重要。
- 仅使用类 NTP 损失（$\lambda_2=0$）：CLIP-T 下降，表明 KL 散度正则化对维持文本控制能力不可或缺。
- 两者结合取得最佳平衡，证实了双重先验设计的必要性。

### 注入深度消融

Figure 7 展示了 LMCL 注入深度对性能的影响，揭示了关键的**过拟合边界**：

- 注入 **1 层**（浅层注入）：性能最低，证实了浅层注入瓶颈的存在。
- 注入 **9 层**：达到最优性能，DINO 和 CLIP-I 均取得最高值。
- 注入 **24 层**（全层注入）：DINO 和 CLIP-I 反而下降，出现**过拟合**现象——过度约束生成过程导致模型丧失泛化能力，文本控制能力受损。

Figure 11 的跨模态与深度联合消融进一步表明：仅注入文本令牌或仅注入图像令牌均无法达到最优效果，**文本+图像双模态令牌**在 9 层深度下取得最佳视觉质量。

![[assets/figures/papers/paper_list_l2303_https_arxiv_org_abs_2508_07341/figures/017_Figure_11.jpg]]
*Figure 11: Qualitative ablation of token modalities across different insertion depths. Rows represent different token configurations, while columns correspond to the number of Transformer layers (1, 3, 9, 24) into which tokens are injected. Rows: “Only Text Token” suffers from identity loss (generic backpacks), while “Only Image Token” exhibits high fidelity but poor editability (e.g., failing to stylize in Col 4). Columns: Inserting tokens into all layers (Depth 24) leads to overfitting, preventing style changes, whereas the optimal depth (Depth 9) achieves the best balance between subject fidelity and textual control*

### Identity Mask 消融

Figure 9 验证了推理时 Identity Mask 机制的必要性。在主体-风格组合生成中，不加掩码时出现明显的**概念污染**：风格令牌的颜色/纹理特征泄漏到主体区域，导致主体外观失真。加入 Identity Mask 后，主体与风格的注意力流被有效隔离，实现了干净的主体-风格解耦组合。

### 失败模式与局限性

1. **注入深度敏感性**：最优注入深度需人工调整，不同主体可能需要不同的深度配置。Figure 7 显示深度从 9 层增至 24 层时性能显著下降，表明当前方案缺乏自适应深度选择机制。
2. **深层过拟合风险**：过度注入（如 24 层）会导致模型过度约束，牺牲文本可编辑性。这一现象在 Figure 11 的定性结果中表现为生成图像趋于单一化，丧失对多样化文本提示的响应能力。
3. **参数效率与性能的权衡边界**：虽然 0.073M 参数已极为高效，但 Table 1 显示 DCoAR 在 CLIP-T 上仍略低于部分扩散模型方法，提示统一自回归模型在文本对齐方面仍有提升空间。

### 补充图表

![[assets/figures/papers/paper_list_l2303_https_arxiv_org_abs_2508_07341/figures/007_Figure_6.jpg]]
*Figure 6: Qualitative comparison of our DCoAR and LoRA-based method for style personalization tasks*

![[assets/figures/papers/paper_list_l2303_https_arxiv_org_abs_2508_07341/figures/018_Figure_12.jpg]]
*Figure 12: Additional qualitative comparison of subject-driven personalization. We compare our DCoAR against two representative concept-injection methods (UniCTokens [1], Yo’Chameleon [22]) and a state-of-the-art diffusion-based fine-tuning approach (DreamBooth [26] with FLUX)*



## 定位与知识库关联

### 统一自回归模型个性化方法的演进瓶颈

近年来，统一多模态自回归模型（如Chameleon、Lumina-mGPT）在文本到图像生成领域展现出与扩散模型相抗衡的能力。然而，针对统一自回归模型的个性化生成方法仍处于早期探索阶段，其核心瓶颈在于**浅层注入**：现有方法仅将可学习的个性化令牌注入输入层，导致概念语义随网络深度衰减，视觉保真度和重文本化能力显著不足。

具体而言，当前统一自回归模型的个性化方法可分为三类：

1. **微调范式**：直接将扩散模型的微调策略迁移至自回归骨干网络。**DreamBooth**（Ruiz et al., CVPR 2023）的变体（如DreamBooth for Imagen/Flux/Lumina-mGPT）通过全参数或LoRA微调实现概念绑定，保真度高但训练成本大。**PersonalAR**（Sun et al., arXiv 2025）和**Proxy-Tuning**（Wu et al., arXiv 2025）分别采用LoRA适配器和代理调优策略，后者训练参数达142.6M，但仍需大量计算资源。

2. **浅层注入范式**：**Yo'Chameleon**（Nguyen et al., CVPR 2025）和**UniCTokens**（An et al., arXiv 2025）将可学习令牌仅置于输入层，保持骨干网络冻结，训练参数极少（如UniCTokens仅0.073M），但视觉保真度与微调方法存在显著差距。这构成了本文所定义的“浅层注入瓶颈”。

3. **扩散模型中的分离方法**：**B-LoRA**（Frenkel et al., ECCV 2024）和**ZipLoRA**（Shah et al., ECCV 2024）在扩散模型中实现了主体与风格的分离，但依赖LoRA微调，无法直接迁移至统一自回归架构。

DCoAR正是在这一谱系中填补了关键空白：**以深层注入策略弥合浅层注入与微调方法之间的保真度差距，同时保持骨干网络完全冻结**。

### 因果机制：从浅层注入到深层概念强化

DCoAR的方法论突破可概括为三个因果层面的创新：

**因果瓶颈**：浅层注入导致的概念信号衰减。在统一自回归模型中，Transformer层逐层处理多模态令牌序列。若仅在输入层注入概念令牌，其语义信息在深层自注意力机制中逐渐被稀释，最终导致生成结果偏离参考概念。

**因果旋钮**：层间多模态上下文学习（LMCL）。DCoAR将可学习的文本上下文令牌 $\mathbf{p}_{[v]}^{(i)}$ 和图像上下文令牌 $\mathbf{p}_I^{(i)}$ 注入前 $K$ 个Transformer层（主体个性化 $K=9$，风格个性化 $K=3$），在第 $i$ 层构造序列：
$$\mathbf{U}_i' = \{ \mathbf{y}_1, \dots, \mathbf{p}_{[v]}^{(i)}, \dots, \mathbf{y}_L, \mathbf{p}_I^{(i)}, \mathbf{x}_1, \dots, \mathbf{x}_T \}$$
这一设计实现了**持续的特征强化**：概念令牌在每一层重新参与跨模态注意力计算，确保概念语义贯穿整个生成过程。

**训练稳定机制**：双重先验保持（DPP）与上下文感知自正则化（CASR）。深层注入虽增强了概念表达，但引入了过拟合和语义漂移风险。DPP通过结合类图像NTP损失与KL散度约束，将个性化分布锚定在预训练先验附近：
$$\mathcal{L}_{DPP} = \lambda_1 \cdot \mathcal{L}_{NTP_{cls}}(\text{logits}_{prior}, \text{labels}_{cls}) + \lambda_2 \cdot D_{KL}(\text{logits}_{zs} \parallel \text{logits}_{prior})$$
CASR则进一步约束图像上下文令牌与预训练模型生成的主体嵌入之间的距离：
$$\mathcal{L}_{CASR} = \frac{1}{N} \sum_{i=1}^{N} \| \mathbf{p}_I^{(i)} - \mathbf{E}_{subject}^{(i)} \|^2$$
二者协同作用，在保持概念保真度的同时维持了文本控制能力。

### 适用边界与关键约束

**适用场景**：
- 主体驱动的个性化生成（提供3-5张参考图像）
- 艺术风格迁移与个性化
- 免训练的主体-风格组合生成（通过Identity Mask实现注意力隔离）

**关键约束与局限性**：

1. **注入深度的敏感性**：消融实验表明，注入深度是影响性能的关键超参数。在9层注入时达到最优DINO 0.7226和CLIP-I 0.8151，但进一步增加至24层会导致过拟合，降低主体保真度（Figure 7）。不同主体可能需要不同的最优深度，目前依赖人工调整。

2. **过拟合与可编辑性的权衡**：深层注入虽然提升了视觉保真度，但过度注入（如24层）会过度约束生成过程，牺牲文本控制能力。DPP和CASR在一定程度上缓解了这一问题，但未能完全消除这一根本性张力。

3. **模态令牌配置的固定性**：当前方案对主体和风格任务分别采用固定的令牌配置（主体：前9层；风格：前3层），缺乏针对不同概念复杂度的自适应机制。

4. **Identity Mask的依赖性**：免训练组合依赖于推理时的Identity Mask来隔离主体与风格令牌的注意力流。消融实验表明，去除掩码会导致颜色泄漏等概念污染问题（Figure 9），说明该方法对掩码机制的准确性高度敏感。

### 开放问题

1. **自适应注入深度**：如何开发自动化机制，根据主体概念的复杂度（如纹理丰富度、形状特异性）动态确定最优的LMCL注入层数，以减少人工调参依赖并抑制过拟合？

2. **概念解耦的理论边界**：Identity Mask虽然实现了免训练组合，但其对主体与风格概念的解耦程度是否受限于训练数据的分布偏差？在极端概念组合（如高度抽象风格与精细纹理主体）下，掩码机制是否仍能保持干净的分离？

3. **跨模型泛化性**：DCoAR的深层注入策略和正则化方案是否可迁移至其他统一自回归架构（如基于不同tokenizer或注意力机制变体的模型），其性能增益是否依赖于特定骨干网络的架构特性？

4. **多概念扩展**：当前方法主要针对单一主体或风格的个性化。如何将LMCL扩展至多概念联合注入（如多个主体或主体+风格+场景），同时避免概念间的语义干扰和令牌序列长度的线性增长？



## 原文 PDF

![[paperPDFs/CVPR_2026/DCoAR_Deep_Concept_Injection_into_Unified_Autoregressive_Models_for_Personalized_Text_to_Image_Generation.pdf]]
