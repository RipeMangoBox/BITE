---
title: "LLaMo: Scaling Pretrained Language Models for Unified Motion Understanding and Generation with Continuous Autoregressive Tokens"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/LLaMo_Scaling_Pretrained_Language_Models_for_Unified_Motion_Understanding_and_Generation_with_Continuous_Autoregressive_Tokens.pdf
paper_link: https://openaccess.thecvf.com/content/CVPR2026/html/Li_LLaMo_Scaling_Pretrained_Language_Models_for_Unified_Motion_Understanding_and_CVPR_2026_paper.html
project_link: https://kunkun0w0.github.io/project/LLaMo/
code_link: null
aliases:
- LLaMo
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
- topic/generative_models_diffusion
core_operator: 采用连续因果变分自编码器（causal VAE）编码运动，并用流匹配（flow matching）头替代离散标记预测；同时使用模态特定的混合Transformer（Mixture-of-Transformers）架构并冻结所有文本相关模块，从而在注入运动理解与生成能力的同时，完全保留基座LLM的语言性能。
primary_logic: 通过连续潜在空间建模与流匹配生成，可消除量化误差并实现平滑的实时流式运动生成（≥30 FPS）；MoT架构分离模态参数，在共享自注意中层间通信，无需牺牲原始LLM的语言能力即可完成大规模多模态对齐与联合学习。
claims:
- LLaMo-3B 在 HumanML3D 文本到动作生成上取得 FID 22.491，与大规模 MotionMillion 及专家模型竞争，且对罕见文本输入更鲁棒。
- LLaMo 完整保留基座 LLM 的语言能力：在 MMLU 上达到 63.4（3B），而移除 MoT 后崩溃至 31.1；IFEval 从 78.5 降至 22.3。
- 连续因果 VAE 重建质量远超离散量化方法：CausalTAE-z64 的 MPJPE 仅 3.86 mm，而 FSQ 为 41.9 mm。
- MoT 架构在保持语言能力的同时，将文本到动作 FID 从 27.361 提升至 22.491（3B），且未出现灾难性遗忘。
---

# LLaMo: Scaling Pretrained Language Models for Unified Motion Understanding and Generation with Continuous Autoregressive Tokens

> [!tip] 核心洞察
> 通过连续潜在空间建模与流匹配生成，可消除量化误差并实现平滑的实时流式运动生成（≥30 FPS）；MoT架构分离模态参数，在共享自注意中层间通信，无需牺牲原始LLM的语言能力即可完成大规模多模态对齐与联合学习。

| 字段 | 内容 |
|------|------|
| 中文题名 | LLaMo：通过连续自回归标记缩放预训练语言模型实现统一运动理解与生成 |
| 英文题名 | LLaMo: Scaling Pretrained Language Models for Unified Motion Understanding and Generation with Continuous Autoregressive Tokens |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://openaccess.thecvf.com/content/CVPR2026/html/Li_LLaMo_Scaling_Pretrained_Language_Models_for_Unified_Motion_Understanding_and_CVPR_2026_paper.html) · [Project](https://kunkun0w0.github.io/project/LLaMo/) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction #topic/generative_models_diffusion |
| Method | LLaMo |
| Dataset | HumanML3D text-to-motion, HumanML3D motion-to-text, Language Preservation, Instruction Following |

> [!tip] 效果简介
> - HumanML3D text-to-motion 上，FID 22.491 (LLaMo-3B) vs 23.755 (MotionMillion-3B) (-1.264)；R@1 0.606 (LLaMo-3B) vs 0.602 (MotionMillion-3B) (+0.004)；R@2 0.766 (LLaMo-3B) vs 0.749 (MotionMillion-3B) (+0.017)。
> - HumanML3D motion-to-text 上，CIDEr 100.8 (LLaMo-3B) vs 97.2 (MotionGPT FT) (+3.6)。
> - Language Preservation (MMLU) 上，MMLU Accuracy 63.4 (LLaMo-3B) vs 31.1 (LLaMo-3B w/o MoT) (+32.3)。

## 概述

将大规模语言模型（LLM）拓展至人体运动领域以同时支撑理解与生成，面临两个核心瓶颈。其一，**直接微调文本参数会导致灾难性遗忘**，严重破坏基座模型的语言能力。其二，**将连续运动数据量化为离散标记会引入抖动伪影**，且固定长度的生成范式难以适配真实运动的多样性与时长变化。LLaMo 针对上述问题，提出了一个以**连续自回归标记**为核心的统一运动-语言框架。

LLaMo 的核心设计在于两个因果旋钮。第一，采用**连续因果变分自编码器（causal VAE）** 将运动编码至平滑的连续潜在空间，并用**流匹配（flow matching）头**替代传统的离散标记预测，从而从根本上消除量化误差，实现高保真重建与实时流式生成（≥30 FPS）。第二，引入**模态特定的混合Transformer（Mixture-of-Transformers, MoT）** 架构：文本与运动分支拥有各自独立的前馈网络参数，但共享自注意力层以进行跨模态通信；同时**冻结所有文本相关模块**，在注入运动理解与生成能力的同时，完全保留基座LLM的语言性能。

实验表明，LLaMo-3B 在 HumanML3D 文本到动作生成上取得 FID 22.491，与大规模方法 MotionMillion 及领域专家模型竞争，且对罕见文本输入表现出更强的鲁棒性。更重要的是，MoT 设计使模型完整保留了语言能力：MMLU 达 63.4，IFEval 严格准确率达 78.5；而移除 MoT 后，两项指标分别崩溃至 31.1 和 22.3。连续因果 VAE 的重建精度亦远超离散量化方案，MPJPE 仅 3.86 mm，相较 FSQ 的 41.9 mm 有数量级优势。

## 背景与动机

### 运动理解与生成的统一挑战

人类运动理解与生成是构建具身智能体的核心能力，涵盖从文本描述生成自然运动（text-to-motion）和从运动序列推理语义描述（motion-to-text）两大任务。近年来，大规模语言模型（LLMs）在跨模态统一建模中展现出强大的泛化潜力，促使研究者尝试将运动模态纳入语言模型的统一框架。然而，**在扩展现有LLM以统一处理运动理解和生成时，面临两个核心瓶颈**：

1. **灾难性遗忘**：直接对LLM的文本参数进行微调以适配运动数据，会严重破坏基座模型的语言能力。实验表明，移除模态分离设计后，模型在MMLU上的准确率从63.4骤降至31.1，IFEval严格准确率从78.5骤降至22.3（Table 5），语言能力近乎崩溃。

2. **离散量化的根本缺陷**：现有主流方法（如MotionGPT, Jiang et al., NeurIPS 2023）将连续运动数据量化为离散标记，再借由LLM的自回归机制进行建模。然而，离散向量量化（VQ/FSQ）会引入不可恢复的抖动伪影，且固定长度的离散标记序列无法适应真实人体运动在时长和节奏上的天然多样性。实验数据显示，离散量化方案FSQ的运动重建误差MPJPE高达41.9 mm，而连续因果VAE可将该指标降至3.86 mm（Table 2），差距超过一个数量级。

### 现有方法的局限

当前运动-语言模型可大致分为两类，但均存在显著局限：

- **专家模型**（如MDM、MLD、T2M-GPT、MoMask）：仅在单一数据集（如HumanML3D）上训练，虽在域内指标上表现良好，但缺乏跨场景的泛化能力和语言理解深度。
- **大规模预训练模型**（如MotionMillion）：采用离散量化方案，虽在数据规模上有所突破，但仍受限于量化误差和语言遗忘问题，且无法实现流式生成。

更重要的是，**现有方法均未能在注入运动能力的同时，完整保留基座LLM的语言性能**。这严重制约了统一多模态模型在真实交互场景中的应用——一个既能生成高质量动作、又能进行自然语言对话的具身智能体，必须同时具备两种能力而不互相损害。

### LLaMo的动机与核心思路

针对上述瓶颈，LLaMo提出了两条根本性的技术路线革新：

- **连续因果潜在空间建模**：摒弃离散量化，采用因果变分自编码器（causal VAE）将运动压缩为连续潜在表示，从根本上消除量化误差，并支持因果流式编码以实现实时生成（≥30 FPS）。
- **模态特定混合Transformer（MoT）**：冻结所有文本相关模块，为运动模态引入独立的FFN参数，仅在共享自注意力层实现跨模态通信。这一设计使得模型在获得运动理解与生成能力的同时，**完全保留基座LLM的语言性能**。

通过这两项设计，LLaMo成为首个在不牺牲语言能力的前提下，实现统一运动理解与生成的大规模运动-语言模型（Figure 1）。其连续自回归框架结合流匹配（flow matching）生成头，不仅消除了量化伪影，还支持任意长度的流式运动生成，为实时人机交互和具身智能应用奠定了基础。

## 核心创新

LLaMo 的核心创新在于系统性地解决了“将大规模语言模型扩展为统一运动-语言模型”时的两个根本瓶颈：**运动标记化导致的量化误差**与**多模态训练引发的语言能力灾难性遗忘**。其方案通过三个关键设计（changed slots）实现突破，而非单纯堆叠现有组件。

### 1. 连续因果运动标记化：消除量化瓶颈

传统方法（如 **MotionGPT** (Jiang et al., NeurIPS 2023)、**MotionMillion**）将连续运动序列量化为离散 token，再用 softmax 预测。这引入了不可恢复的量化误差，表现为生成运动的**抖动伪影**，且固定长度编码难以适应真实运动的多样性。

LLaMo 改用**连续因果变分自编码器（causal VAE）** 进行运动标记化。该编码器基于因果 CNN，严格保持时间因果性（当前帧重建不依赖未来帧），支持流式编码。其关键技巧在于鲁棒 VAE 采样策略：不从编码器预测方差，而是从 $[0, C_\sigma]$ 均匀分布采样方差 $\sigma$，防止后验坍塌：

$$
z = \mu + \sigma \odot \epsilon, \quad \epsilon \sim \mathcal{N}(0, \mathbf{I}), \quad \sigma \sim \mathbf{U}(0, C_\sigma)
$$

这一设计的效果是决定性的（Table 2）：连续 CausalTAE-z64 的 MPJPE 仅 **3.86 mm**，而离散 FSQ 方法高达 **41.9 mm**——重建精度提升一个数量级。这从根本上消除了量化误差对生成质量的制约。

### 2. 模态特定混合 Transformer（MoT）：根除灾难性遗忘

直接微调 LLM 处理运动 token 会导致文本参数被覆盖，语言能力崩溃。LLaMo 提出 **Mixture-of-Transformers (MoT)** 架构：每个 Transformer 块中，**文本和运动模态拥有独立的 FFN 参数，但共享自注意力层**。文本分支（包括嵌入层、FFN、输出头）**全部冻结**，仅训练运动分支和共享注意力中的投影矩阵。

这一设计的因果机制是：共享自注意力实现跨模态信息交互（运动理解需要文本上下文，运动生成需要语义引导），而模态特定 FFN 保证语言知识不被运动训练信号侵蚀。消融实验（Table 5）提供了强力证据：
- 移除 MoT 后，MMLU 从 **63.4 骤降至 31.1**（接近随机水平），IFEval 从 **78.5 骤降至 22.3**——语言能力发生灾难性遗忘。
- 同时，MoT 设计本身还改善了运动生成质量：3B 模型的 FID 从 27.361（无 MoT）降至 **22.491**。

### 3. 流匹配生成头：实现连续自回归与任意长度生成

LLaMo 不预测离散 token，而是在自回归框架中引入**流匹配（flow matching）头**：从每个运动 token 的隐藏状态 $\hat{h}_i^{\text{motion}}$ 出发，预测最优传输路径上的速度场 $f(x_t, t, \hat{h}_i^{\text{motion}})$，逐步将噪声转化为连续运动潜在：

$$
\mathcal{L}_{\mathrm{FM}} = \mathbb{E}_{t \in [0,1]} \Vert f(x_t, t, \hat{h}_i^{\text{motion}}) - v_t(x) \Vert
$$

配合**出口头（exit head）**——一个二分类器预测序列终止——模型可生成任意长度的运动，并以 **≥30 FPS** 实现实时流式输出。这解决了固定长度扩散生成和离散自回归模型在长度灵活性上的不足。

### 创新协同效应

上述三个设计并非孤立改进，而是形成因果闭环：连续 VAE 提供高保真潜在表示 → MoT 架构在冻结语言能力的前提下学习跨模态映射 → 流匹配头在连续空间中实现平滑、可变长度的生成。这一协同使得 LLaMo-3B 在 HumanML3D 上以 **FID 22.491** 超越同规模的大规模模型 MotionMillion-3B（23.755），同时完整保留基座 LLM 的语言能力——这是此前统一模型未能达成的双重目标。

## 整体框架

LLaMo 的整体设计围绕一个核心目标展开：**在不损害基座大语言模型（LLM）语言能力的前提下，赋予其统一的运动理解与生成能力**。为此，模型构建了一条从连续运动表征到多模态自回归生成的完整流水线，其关键模块关系与数据流如下。

### 输入与运动表征

模型的输入包含两部分：**文本序列**与**运动序列**。对于运动数据，每一帧被表示为一个 272 维的特征向量：

$$m _ { i } = \{ { \dot { r } } ^ { x } , { \dot { r } } ^ { z } , { \dot { r } } ^ { a } , p ^ { i } , v ^ { i } , r ^ { i } \}$$

该表征涵盖了根关节的线速度、角速度，以及局部关节位置、线速度和旋转，为后续的连续潜在空间建模提供了完整的运动学信息（Section 3.1）。

### 连续因果运动标记化

传统方法将连续运动量化为离散标记，不可避免地引入**抖动伪影**，且固定长度的离散码本难以捕捉真实运动的多样性。LLaMo 摒弃了这一思路，转而采用**连续因果变分自编码器（Causal VAE）**进行运动标记化（Section 3.2）。该编码器基于因果 CNN 架构，在严格保持时序因果性的前提下，将原始运动序列压缩为连续潜在表示 $z$。其训练目标为：

$$\mathcal { L } = \mathcal { L } _ { \mathrm { r e c o n } } + D _ { \mathrm { K L } } \big ( \mathrm { E n c } _ { \phi } ( z | m ) \| p ( z ) \big ) + \lambda _ { \mathrm { r o o t } } \mathcal { L } _ { \mathrm { r o o t } }$$

为了增强 VAE 的鲁棒性并防止后验坍塌，模型在采样时从均匀分布中随机采样方差 $\sigma$，而非直接预测：

$$\mu = \mathrm{Enc}_{\phi}(m); \quad z = \mu + \sigma \odot \epsilon, \ \epsilon \sim \mathcal{N}(0, \mathbf{I}), \ \sigma \sim \mathbf{U}(0, C_{\sigma}); \quad \hat{m} = \mathrm{Dec}_{\psi}(z)$$

这一设计使得运动标记化过程**完全消除了量化误差**，并天然支持流式编码，为后续的实时生成奠定了基础。

### 模态特定混合 Transformer（MoT）与多模态融合

运动潜在 $z$ 经过一个**运动适配器（Projector）**映射到与语言嵌入兼容的维度后，与文本 token 一同送入核心的 **MoT Transformer Decoder**。该解码器基于 Llama 架构，但其设计是 LLaMo 区别于以往工作的关键所在（Section 3.3, Figure 2）。

![[assets/figures/papers/paper_list_l4_https_openaccess_thecvf_com_content_CVPR2026_html_Li_LLaMo_Scaling_Pretr/figures/002_Figure_2.jpg]]
*Figure 2: Framework overview of LLaMo. We utilize modality-specific Mixture-of-Transformer (MoT) to process text and motion tokens separately, while enabling cross-modal interactions through shared self-attention. To preserve the language performance of the base model, text-related modules are frozen. The [BOM] and [EOM] tokens denote the start and end of the motion sequence, respectively. An additional exit head allows the model to support flexible-length motion generation*

MoT 的核心思想是**模态特定的参数分离**：每个 Transformer 块中，文本 token 和运动 token 分别使用各自独立的**前馈网络（FFN）参数**，但共享**自注意力层**。这种设计实现了双重目标：
- **跨模态通信**：共享的自注意力机制允许文本与运动 token 在每一层进行充分的交互，支撑运动理解（motion-to-text）与文本条件生成（text-to-motion）。
- **语言能力保留**：所有与文本相关的模块——包括文本嵌入层、文本 FFN 和语言模型头——在整个训练过程中**完全冻结**。这意味着 LLM 原有的语言知识不会被多模态训练所覆盖，从根本上避免了灾难性遗忘。

### 双轨输出头：离散文本与连续运动

LLaMo 的自回归生成过程在输出端分化为两条并行的路径：

1. **离散语言解码头**：保留基座 LLM 的原始 LM Head，用于文本输出的下一个 token 预测。其概率分布为标准形式：
   $$P \Big ( x [ i ] ^ { \mathrm { t e x t } } \Big | x [ < i ] \Big ) = \mathrm { s o f t m a x } ( \hat { h } [ i ] ^ { \mathrm { t e x t } } W _ { \mathrm { t e x t } } )$$
   对应的训练损失为负对数似然 $\mathcal { L } _ { \mathrm { N T P } }$，用于运动理解任务中的文本生成。

2. **连续运动解码头（流匹配头）**：替代传统的离散 token 预测或固定长度扩散生成，LLaMo 采用一个轻量的**流匹配（Flow Matching）头**。该头从自回归隐藏状态 $\hat{h}_i^{\mathrm{motion}}$ 出发，预测最优传输路径上的速度场：
   $$\mathcal { L } _ { \mathrm { F M } } = \mathbb { E } _ { t \in [ 0 , 1 ] } \Vert f ( x _ { t } , t , \hat { h } _ { i } ^ { \mathrm { m o t i o n } } ) - v _ { t } ( x ) \Vert$$
   这一设计使得运动生成在连续潜在空间中完成，彻底摆脱了量化伪影，并能实现平滑的高帧率输出（≥30 FPS）。

3. **运动生成出口头**：一个二分类头，用于预测运动序列的结束点，使模型能够生成**任意长度**的运动序列，而非固定帧数。

### 训练策略与数据流总结

完整的训练目标将上述组件统一为一个联合优化问题：

$$\mathcal { L } = \mathcal { L } _ { \mathrm { F M } } + \lambda _ { 1 } \mathcal { L } _ { \mathrm { N T P } } + \lambda _ { 2 } \mathcal { L } _ { \mathrm { E n d } }$$

为稳定大规模训练并缓解流匹配头易出现的损失尖峰，LLaMo 采用**三阶段训练策略**（Table 1）：首先进行特征对齐，随后进入联合多任务学习，最后对运动头进行微调。

**整体数据流**可概括为：原始运动序列 → Causal VAE 编码为连续潜在 → 运动适配器投影 → 与文本 token 拼接送入 MoT Decoder（文本分支冻结，运动分支可训练）→ 自回归生成过程中，文本 token 由 LM Head 解码，运动潜在由流匹配头解码，并由出口头控制生成长度。这一流水线在注入运动多模态能力的同时，完整保留了基座 LLM 的语言性能。

### 补充图表

![[assets/figures/papers/paper_list_l4_https_openaccess_thecvf_com_content_CVPR2026_html_Li_LLaMo_Scaling_Pretr/figures/001_Figure_1.jpg]]
*Figure 1: We introduce LLaMo, the first large-scale motion-language model supporting unified motion understanding and generation without compromising the language proficiency of the underlying LLM*

## 核心模块与公式推导

LLaMo 的核心架构围绕三个关键模块展开：连续因果运动标记化、模态特定混合Transformer（MoT）以及流匹配运动生成头。这些模块共同解决了将预训练LLM扩展为统一运动-语言模型时的两大瓶颈——离散量化引入的抖动伪影和全参数微调导致的灾难性遗忘。

### 运动表示与因果VAE标记化

**运动表示定义**。每一帧人体运动被表示为一个272维向量（Section 3.1）：

$$m _ { i } = \{ { \dot { r } } ^ { x } , { \dot { r } } ^ { z } , { \dot { r } } ^ { a } , p ^ { i } , v ^ { i } , r ^ { i } \}$$

其中 ${\dot{r}}^x$、${\dot{r}}^z$ 为根节点线速度（xz平面），${\dot{r}}^a$ 为根节点角速度，$p^i$ 为局部关节位置，$v^i$ 为局部关节线速度，$r^i$ 为局部关节旋转。该表示完整刻画了人体运动的运动学特征。

**因果VAE编码**。为消除离散量化（如FSQ）引入的抖动伪影，LLaMo采用基于因果CNN的连续变分自编码器（causal VAE），在严格保持时序因果性的前提下将运动序列压缩为连续潜在变量 $z$（Section 3.2）。训练目标为：

$$\mathcal { L } = \mathcal { L } _ { \mathrm { r e c o n } } + D _ { \mathrm { K L } } \big ( \mathrm { E n c } _ { \phi } ( z | m ) \| p ( z ) \big ) + \lambda _ { \mathrm { r o o t } } \mathcal { L } _ { \mathrm { r o o t } }$$

该损失函数结合了重建损失 $\mathcal{L}_{\mathrm{recon}}$、以标准正态分布为先验的KL散度，以及根表示重建正则项 $\mathcal{L}_{\mathrm{root}}$，确保潜在空间既紧凑又具有良好生成属性。

**鲁棒采样策略**。为防止后验坍塌，LLaMo在训练时从均匀分布采样方差而非直接预测：

$$\begin{array}{rl} & \mu = \mathrm{Enc}_{\phi}(m) \\ & z = \mu + \sigma \odot \epsilon, \mathrm{where} \epsilon \sim \mathcal{N}(0, \mathbf{I}), \sigma \sim \mathbf{U}(0, C_{\sigma}) \\ & \hat{m} = \mathrm{Dec}_{\psi}(z) \end{array}$$

这一设计使编码器仅需预测均值 $\mu$，而方差从 $[0, C_{\sigma}]$ 均匀采样，有效提升了VAE训练的稳定性。实验表明，CausalTAE-z64的MPJPE仅3.86 mm，而离散FSQ方案为41.9 mm（Table 2），连续标记化的重建精度优势显著。

![[assets/figures/papers/paper_list_l4_https_openaccess_thecvf_com_content_CVPR2026_html_Li_LLaMo_Scaling_Pretr/figures/004_Table_2.jpg]]
*Table 2: Motion Tokenization. We compared the SOTA discrete motion tokenization solution [12] with our continuous causal motion tokenization, where*

### 模态特定混合Transformer（MoT）

MoT是LLaMo保留基座LLM语言能力的核心设计（Section 3.3，Figure 2）。其关键机制在于：文本和运动token共享自注意力层以实现跨模态交互，但各自拥有独立的FFN参数。文本分支的所有模块（包括原始LM头和FFN）在训练中完全冻结，仅运动分支的FFN、运动适配器（projector）和生成头参与更新。

**文本解码**。对于文本token，仍使用原始LM头进行离散下一个token预测：

$$P \Big ( x [ i ] ^ { \mathrm { t e x t } } \Big | x [ < i ] \Big ) = \mathrm { s o f t m a x } ( \hat { h } [ i ] ^ { \mathrm { t e x t } } W _ { \mathrm { t e x t } } )$$

对应的损失函数为负对数似然：

$$\mathcal { L } _ { \mathrm { N T P } } = - \mathbb { E } _ { x [ i ] \in \mathrm { t e x t } } \Big [ \log P \Big ( x [ i ] \Big | x [ < i ] \Big ) \Big ]$$

该损失仅在运动理解任务（motion-to-text）中激活，用于监督文本描述生成。

**运动生成**。运动token的自回归输出隐藏状态 $\hat{h}_i^{\mathrm{motion}}$ 被送入流匹配头，预测从噪声到目标潜在的最优传输速度场：

$$\mathcal { L } _ { \mathrm { F M } } = \mathbb { E } _ { t \in [ 0 , 1 ] } \Vert f ( x _ { t } , t , \hat { h } _ { i } ^ { \mathrm { m o t i o n } } ) - v _ { t } ( x ) \Vert$$

其中 $x_t$ 为时间 $t$ 处的插值潜在，$v_t(x)$ 为真实速度场。与离散token的softmax预测不同，流匹配头直接输出连续向量，从根本上避免了量化误差。此外，LLaMo引入一个二分类出口头（exit head）预测运动序列终止信号，支持任意长度生成。

### 多阶段训练策略

为稳定大规模训练并缓解流匹配头的损失尖峰，LLaMo采用三阶段训练配方（Section 3.4，Table 1）。总损失函数为：

$$\mathcal { L } = \mathcal { L } _ { \mathrm { F M } } + \lambda _ { 1 } \mathcal { L } _ { \mathrm { N T P } } + \lambda _ { 2 } \mathcal { L } _ { \mathrm { E n d } }$$

三个阶段分别聚焦于特征对齐、联合学习和运动头微调，逐步引入不同损失项并调整学习率与任务比例。这一策略有效抑制了流匹配头在联合训练初期的梯度不稳定问题，使3B和8B规模的模型均能收敛。

**关键设计决策**。潜在维度选择为 $z=32$，因为更高维度的潜在空间会使MLP流匹配头训练不稳定（Section 4.1）。运动适配器将VAE潜在空间映射到与语言嵌入兼容的维度，确保两种模态在共享自注意力层中的有效交互。

## 实验与分析

### 核心定量结果

#### 文本到动作生成

在 HumanML3D 基准上，LLaMo-3B 取得了 **FID 22.491**，优于同等规模的大规模预训练方法 **MotionMillion-3B**（FID 23.755），并与仅在 HumanML3D 上训练的专家模型（如 **MDM**、**T2M-GPT**、**MoMask**）竞争。在检索精度指标上，LLaMo-3B 的 R@1 达到 0.606，R@2 为 0.766，R@3 为 0.839，均小幅领先 MotionMillion-3B（Table 3）。

![[assets/figures/papers/paper_list_l4_https_openaccess_thecvf_com_content_CVPR2026_html_Li_LLaMo_Scaling_Pretr/figures/007_Table_3.jpg]]
*Table 3: Text-to-Motion on HumanML3D. We compared methods with different training settings, following the evaluation in [73]. Our results show comparable metrics to both MotionMillion [12] and specialist models*

需要指出的是，HumanML3D 仅占 LLaMo 预训练数据的不足 1%，因此 FID 等分布匹配指标在此场景下的可靠性存疑——作者也承认 FID 变得不可靠。模型对罕见文本输入的鲁棒性通过零样本定性结果展示（Figure 4），但缺乏系统的大规模零样本定量评估协议。

![[assets/figures/papers/paper_list_l4_https_openaccess_thecvf_com_content_CVPR2026_html_Li_LLaMo_Scaling_Pretr/figures/010_Figure_4.jpg]]
*Figure 4: Zero-shot Text-to-Motion Generation Results on MotionMillion-Eval [12] prompts*

#### 运动到文本理解

在 HumanML3D 的运动描述任务上，LLaMo-3B 取得了 CIDEr 100.8，优于微调后的 **MotionGPT**（CIDEr 97.2），且 LLaMo 在此过程中完全冻结了文本相关参数（Table 4）。然而，运动理解任务并未从模型规模扩大中获得类似生成任务的显著提升，这一现象的原因尚待探究。

![[assets/figures/papers/paper_list_l4_https_openaccess_thecvf_com_content_CVPR2026_html_Li_LLaMo_Scaling_Pretr/figures/006_Table_4.jpg]]
*Table 4: Motion-to-Text on HumanML3D follow [17] protocols. Our results demonstrate competitive performance with other specialist models without optimizing text parameters*

#### 语言能力保留

LLaMo 的核心设计目标之一是完整保留基座 LLM 的语言能力。在 MMLU 基准上，LLaMo-3B 达到 **63.4** 的准确率，与原始基座模型持平；而在指令遵循评估 IFEval 上，严格准确率达到 **78.5**（Table 5）。这验证了 MoT 架构中冻结文本模块策略的有效性。

### 消融实验

#### MoT 架构的关键作用

移除 MoT 设计（即全参数共享更新）后，模型出现严重的灾难性遗忘：MMLU 从 63.4 骤降至 **31.1**，IFEval 从 78.5 崩溃至 **22.3**（Table 5）。同时，MoT 架构本身也改善了运动生成质量——3B 模型的 FID 从无 MoT 设计的 27.361 降至 **22.491**。这表明模态特定参数分离不仅保护了语言能力，还通过避免跨模态梯度干扰提升了运动生成性能。

#### 连续标记化的重建优势

Table 2 展示了连续因果 VAE 相对于离散量化方法的压倒性优势：CausalTAE-z64 的 MPJPE 仅为 **3.86 mm**，而离散 FSQ 方法高达 41.9 mm。即使是最轻量的 CausalTAE-z32 变体（MPJPE 10.1 mm），其重建精度也远超离散方案。这一差距直接解释了为何连续潜在空间建模能够消除量化引入的抖动伪影，为后续流匹配生成提供高质量的运动表征。

#### 三阶段训练策略

由于流匹配头在联合训练中容易出现损失尖峰，LLaMo 采用三阶段训练配方（Table 1）：特征对齐 → 联合学习 → 微调运动头。这一策略有效稳定了大规模训练过程，并辅以对低表现样本的过滤。然而，这种训练复杂性可能影响方法的可复现性和公平比较。

![[assets/figures/papers/paper_list_l4_https_openaccess_thecvf_com_content_CVPR2026_html_Li_LLaMo_Scaling_Pretr/figures/005_Table_1.jpg]]
*Table 1: Training recipe. We adopt a three-stage training strategy to stabilize our large model training, each focusing on different aspects of model optimization*

### 流式生成能力

LLaMo 支持实时流式运动生成，帧率可达 **≥30 FPS**。这得益于因果 VAE 的流式编码特性与自回归流匹配头的结合——模型可以逐帧生成运动潜在，并由出口头（exit head）预测序列终止点，实现任意长度的灵活生成。

### 失败模式与局限

1. **分布外评估的不可靠性**：HumanML3D 仅占预训练数据的极小比例，FID 等指标主要反映数据集分布间隙而非绝对生成质量，需要更可靠的大规模评估基准。
2. **运动理解的规模不敏感性**：模型规模扩大对运动理解任务未带来显著提升，问题可能出在数据配比、模型设计或评估协议层面。
3. **流匹配头的训练不稳定性**：联合训练中的损失尖峰需要多阶段策略和样本过滤来缓解，增加了训练复杂度和调参负担。
4. **零样本评估不足**：零样本运动生成目前主要依赖定性示例（Figure 4），缺乏系统的定量评估框架。

### 补充图表

![[assets/figures/papers/paper_list_l4_https_openaccess_thecvf_com_content_CVPR2026_html_Li_LLaMo_Scaling_Pretr/figures/003_Figure_3.jpg]]
*Figure 3: Dataset Composition. We gather a large-scale human motion dataset by combining high quality Mocap datasets with large-scale HMR estimated datasets*

![[assets/figures/papers/paper_list_l4_https_openaccess_thecvf_com_content_CVPR2026_html_Li_LLaMo_Scaling_Pretr/figures/008_Figure.jpg]]
*Figure: (c) A man of average build who looked lost was walking along the street when a giant pie hit his head*

![[assets/figures/papers/paper_list_l4_https_openaccess_thecvf_com_content_CVPR2026_html_Li_LLaMo_Scaling_Pretr/figures/009_Figure.jpg]]
*Figure: (a) A zombie slowly dragging its feet forward, arms outstretched, letting out a low groan. (b) An obese middle-aged male security guard, walking and looking around*

## 方法谱系与知识库定位

### 1. 方法类型学定位

LLaMo 属于**大规模预训练语言模型驱动的统一运动理解与生成框架**，其核心设计理念是在不牺牲基座 LLM 语言能力的前提下，注入运动模态的生成与理解功能。从方法谱系看，LLaMo 同时跨越了以下几个技术脉络：

- **运动标记化路线**：区别于以 **MotionGPT** (Jiang et al., NeurIPS 2023)、**MotionMillion** 为代表的离散向量量化（VQ/FSQ）路线，LLaMo 采用连续因果变分自编码器（causal VAE）进行运动标记化，从根本上消除了量化误差引入的抖动伪影。这一选择使其与 **MotionStreamer** 等流式运动生成方法在因果潜在空间建模上形成呼应，但 LLaMo 进一步将该能力整合进了大规模多模态语言模型中。

- **多模态 LLM 扩展路线**：LLaMo 的 Mixture-of-Transformers（MoT）架构可视为对传统全参数微调或参数高效微调（如 LoRA、Adapter）方案的替代。传统方案在注入新模态时容易引发灾难性遗忘，而 MoT 通过模态特定 FFN + 共享自注意力的设计，在保留语言专门化的同时实现跨模态交互。这一思路与多模态大语言模型（如 LLaVA、Flamingo 等视觉-语言模型）中的模态对齐策略存在结构性类比，但 LLaMo 首次将其系统性地应用于运动-语言联合建模，并给出了语言能力保留的严格消融验证。

- **运动生成范式路线**：LLaMo 采用流匹配（flow matching）头替代离散 token 预测或固定长度扩散生成，实现了连续自回归运动生成。这与 **MDM**、**MLD** 等基于扩散的专家模型，以及 **T2M-GPT**、**MoMask** 等自回归/掩码生成模型形成范式差异——LLaMo 的流匹配头直接从自回归隐藏状态预测速度场，天然支持任意长度生成和实时流式输出（≥30 FPS）。

### 2. 与关键基线的关系

#### 2.1 与 MotionMillion 的对比

**MotionMillion** 是目前最大规模的文本到运动生成模型之一，采用离散量化方案。LLaMo 与其最直接的对比体现在 HumanML3D 基准上（Table 3）：LLaMo-3B 的 FID 为 22.491，优于 MotionMillion-3B 的 23.755（Δ = -1.264），同时在 R@1/R@2/R@3 等检索指标上均有小幅领先。这意味着在可比模型规模下，连续标记化 + 流匹配的组合在生成质量和文本-运动对齐度上均优于离散量化方案。然而，需注意 HumanML3D 仅占 LLaMo 预训练数据的不足 1%，FID 等分布度量可能主要反映数据集间隙而非绝对质量，作者也坦承 FID 在此场景下变得不可靠。

#### 2.2 与 MotionGPT 的对比

**MotionGPT** (Jiang et al., NeurIPS 2023) 是将运动视为“外语”的离散统一运动-语言模型，代表了对运动进行语言式 token 化并直接利用 LLM 进行建模的路线。LLaMo 在运动到文本描述任务上（Table 4）以 CIDEr 100.8 超过 MotionGPT 微调版本的 97.2（Δ = +3.6），且 LLaMo 在此任务中**冻结了所有文本相关参数**，这意味着其运动理解能力并非来自文本解码器的微调，而是来自 MoT 架构中的跨模态交互。这一结果暗示，离散“运动语言”路线可能受限于量化信息损失，而连续潜在空间的跨模态对齐能更有效地保留运动语义。

#### 2.3 与专家模型的对比

在 HumanML3D 文本到运动生成任务上，LLaMo-3B 与仅在 HumanML3D 上训练的专家模型（如 **MDM**、**MLD**、**T2M-GPT**、**MoMask**、**AttT2M**）相比，取得了可比的 FID 和检索指标。考虑到 LLaMo 的训练数据规模远超 HumanML3D，且 HumanML3D 仅占其预训练数据的极小比例，这一“可比”而非“显著超越”的结果恰恰说明：当前小规模基准的评估能力已趋于饱和，难以有效区分大规模预训练方法的质量优势。作者也指出，LLaMo 对罕见文本输入表现出更强的鲁棒性（见 Figure 4 零样本生成示例），这可能是大规模预训练带来的泛化增益，但缺乏系统的零样本定量评估协议来支撑这一论断。

### 3. 适用边界

#### 3.1 有效适用场景

- **大规模运动-语言统一建模**：当需要单一模型同时支持运动生成（text-to-motion）和运动理解（motion-to-text），且不能牺牲语言能力时，LLaMo 的 MoT + 连续标记化方案是目前唯一经过严格验证的选择。
- **实时流式运动生成**：因果 VAE 编码器和流匹配解码头的设计使 LLaMo 支持 ≥30 FPS 的流式生成，适用于游戏、虚拟人等对实时性有要求的应用场景。
- **罕见/长尾文本输入的运动生成**：大规模预训练使 LLaMo 对未见描述具有更强的泛化能力，适合开放域文本到运动生成任务。

#### 3.2 已知局限与失效模式

- **运动理解任务未从规模扩展中显著受益**：与运动生成任务随模型规模扩大而持续改善不同，运动到文本描述任务的性能提升有限。作者未给出明确解释，可能的原因包括：运动理解任务更依赖精细的时空特征提取而非生成能力，当前评估协议（如 CIDEr、BLEU）对细粒度运动语义不敏感，或训练数据中运动-文本对的噪声影响了理解能力的提升。此问题需要进一步研究。

- **流匹配头训练不稳定性**：流匹配头在联合训练中容易出现损失尖峰（loss spikes），LLaMo 不得不采用三阶段训练策略（特征对齐 → 联合学习 → 微调运动头）并过滤低表现样本才能稳定优化。这种训练脆弱性增加了复现难度，也可能限制了更大规模模型的训练可行性。

- **小规模基准的评估失效**：HumanML3D 仅占预训练数据的不足 1%，FID 等分布度量在此场景下主要反映数据集偏差而非真实生成质量。这意味着当前文献中广泛使用的评估协议已不适合大规模预训练方法，亟需新的零样本评估基准。

- **零样本评估体系缺失**：LLaMo 的零样本运动生成目前主要依赖定性示例（Figure 4），缺乏系统的大规模零样本定量评估协议和指标。这使得其泛化能力的声称缺乏严格的实证支撑。

### 4. 开放问题与未来方向

1. **运动理解的规模效应之谜**：为何模型规模扩大对运动理解任务没有带来类似生成任务的显著改善？问题根源在于数据质量、模型架构瓶颈，还是评估协议的敏感性不足？这需要从数据清洗策略、理解任务的细粒度标注、以及更敏感的运动语义评估指标等多维度进行系统探究。

2. **流匹配训练的稳定性改进**：能否开发自适应优化策略、梯度裁剪方案或正则化技术来消除流匹配头的损失尖峰，从而简化训练流程、提高复现性？这直接关系到 MoT + 流匹配方案能否顺利扩展到更大规模的模型和数据。

3. **多模态 MoT 的泛化能力**：MoT 架构的模态特定 FFN + 共享自注意力的设计模式能否轻易扩展至其他模态（如音频、场景、触觉），构建真正通用的具身 AI 多模态基础模型？这需要验证 MoT 在更多模态组合下的语言能力保留效果和跨模态对齐效率。

4. **下一代运动生成评估基准**：如何设计不受数据分布偏差影响的大规模零样本运动生成评估基准和指标？可能的思路包括：基于人类偏好的大规模对比评估、物理合理性度量（如脚部滑动、关节限制违反）、以及运动-文本细粒度语义对齐的自动化度量。

5. **连续标记化与离散标记化的根本权衡**：LLaMo 的连续标记化在重建精度（MPJPE 3.86 mm vs. FSQ 41.9 mm）上碾压离散方案，但离散标记化在兼容现有 LLM 训练基础设施和推理效率上可能有优势。在更大规模的实际部署中，二者的效率-质量帕累托前沿究竟如何？这需要系统性的对比研究。

## 原文 PDF

![[paperPDFs/CVPR_2026/LLaMo_Scaling_Pretrained_Language_Models_for_Unified_Motion_Understanding_and_Generation_with_Continuous_Autoregressive_Tokens.pdf]]