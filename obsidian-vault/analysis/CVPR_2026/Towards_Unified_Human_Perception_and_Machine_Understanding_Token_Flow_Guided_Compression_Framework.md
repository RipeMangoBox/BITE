---
title: "Towards Unified Human Perception and Machine Understanding: Token Flow Guided Compression Framework"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/Towards_Unified_Human_Perception_and_Machine_Understanding_Token_Flow_Guided_Compression_Framework.pdf
project_link: null
code_link: null
aliases:
- TFGCT
- TUHPMUTFGCF
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: 1D令牌序列中的"令牌流"（token flow）现象——Transformer自注意力机制赋予了1D令牌序列全局信息传播与上下文恢复的能力，使得序列中剩余的未掩码令牌能够通过全局信息交换来补偿空间对应关系的缺失，将整体视觉信息动态传播至被掩码位置。这一特性决定了令牌压缩的恢复质量，是实现可变比特率控制（通过令牌掩码比例调节）同时保持语义一致性的关键因果机...
primary_logic: 论文提出两大核心创新：(1) 令牌流传播（TFP）模块——将掩码令牌建模为未掩码令牌条件下的条件高斯分布，通过预测条件均值与方差实现缺失令牌的自适应恢复，替代传统上下文无关的静态令牌填充策略，从而在单一模型内实现细粒度可变比特率控制；(2) 令牌语义引导（TSG）模块——将压缩令牌直接投影并对齐到LVLM语义空间，绕过"解码-编码"过程，使压缩码流可直接被LLM消费。辅以渐进式语义对齐（PSA）训练范式（语义锚定+指令对齐两阶段），桥接视觉重建与语义推理之间的差距。
claims:
- 令牌流扰动实验证明，注入非信息性令牌（uninformative tokens）比注入阻碍性令牌（obstruction tokens）造成的重建质量下降更小，验证了1D令牌序列的全局信息传播（token flow）特性。
- TFP消融实验表明，使用TFP模块后PSNR从20.42提升至20.69（三个比特率级别平均），验证了条件高斯建模优于静态令牌填充策略。
- TSG消融实验表明，TSG模块在所有下游任务（MSCOCO ROUGE-L、RefCOCO Acc@0.5、VQAv2 Acc）上均带来显著提升，验证了语义引导对机器理解的有效性。
- PSA训练范式消融实验（Table 6）表明，同时使用L_PSA1语义锚定和L_PSA2任务特定对齐可获得最佳下游任务性能，验证了渐进式训练策略的必要性。
---

# Towards Unified Human Perception and Machine Understanding: Token Flow Guided Compression Framework

> [!tip] 核心洞察
> 论文提出两大核心创新：(1) 令牌流传播（TFP）模块——将掩码令牌建模为未掩码令牌条件下的条件高斯分布，通过预测条件均值与方差实现缺失令牌的自适应恢复，替代传统上下文无关的静态令牌填充策略，从而在单一模型内实现细粒度可变比特率控制；(2) 令牌语义引导（TSG）模块——将压缩令牌直接投影并对齐到LVLM语义空间，绕过"解码-编码"过程，使压缩码流可直接被LLM消费。辅以渐进式语义对齐（PSA）训练范式（语义锚定+指令对齐两阶段），桥接视觉重建与语义推理之间的差距。

| 字段 | 内容 |
|------|------|
| 中文题名 | 面向统一人类感知与机器理解的令牌流引导压缩框架 |
| 英文题名 | Towards Unified Human Perception and Machine Understanding: Token Flow Guided Compression Framework |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://openaccess.thecvf.com/content/CVPR2026/html/Xu_Towards_Unified_Human_Perception_and_Machine_Understanding_Token_Flow_Guided_CVPR_2026_paper.html) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/image_and_video_generation |
| Method | Token Flow Guided Compression (TFGC) |
| Dataset | MSCOCO Captioning, VQAv2, RefCOCO, Kodak |

> [!tip] 效果简介
> - MSCOCO Captioning 上，ROUGE-L 49.94 vs SOTA方法（见表1对比） (最佳/次佳)。
> - VQAv2 上，VQA Accuracy 66.41 vs SOTA方法（见表1对比） (最佳/次佳)。
> - RefCOCO 上，Grounding Acc@0.5 61.49 vs SOTA方法（见表1对比） (最佳/次佳)。

## 概要

### 问题背景

在超低比特率（ultra-low bitrate）图像压缩场景下，传统学习压缩方法（如 **ELIC**，He et al., CVPR 2022）以像素级保真度（PSNR/MS-SSIM）为优化目标，其压缩潜表示忽略了语义相关性，无法有效解耦有意义内容与冗余视觉细节。与此同时，现有面向机器理解的压缩方法普遍依赖“解码-编码”（decode-then-encode）范式——先将压缩码流重建为完整图像，再送入大型视觉语言模型（LVLM）的视觉编码器。这一过程在极低比特率下造成严重的语义退化，形成了视觉保真度与机器语义理解之间的模态鸿沟。此外，现有方法普遍缺乏在单一模型内实现灵活可变比特率控制的能力，通常需要存储多个模型或依赖固定比特率训练。

### 核心发现：令牌流现象

本文揭示了一个关键的因果机制——1D令牌序列中的“令牌流”（token flow）现象。Transformer自注意力机制赋予了1D令牌序列全局信息传播与上下文恢复的能力：序列中剩余的未掩码令牌能够通过全局信息交换来补偿空间对应关系的缺失，将整体视觉信息动态传播至被掩码位置。令牌流扰动实验（Figure 3）验证了这一特性：注入非信息性令牌（uninformative tokens）比重建质量的下降显著小于注入阻碍性令牌（obstruction tokens），证明1D令牌序列的全局信息传播能力是实现令牌级压缩恢复的核心驱动力。

### 方法定位

基于上述发现，本文提出**令牌流引导压缩框架（Token Flow Guided Compression, TFGC）**，在单一模型内统一人类感知与机器理解的双重目标。TFGC包含两大核心创新模块：

- **令牌流传播（Token Flow Propagation, TFP）模块**：将掩码令牌建模为未掩码令牌条件下的条件高斯分布，通过预测条件均值与方差实现缺失令牌的自适应恢复，替代传统上下文无关的静态令牌填充策略，从而在单一模型内实现细粒度可变比特率控制。
- **令牌语义引导（Token Semantic Guidance, TSG）模块**：将压缩令牌直接投影并对齐到LVLM语义空间，使压缩码流可绕过“解码-编码”过程直接被LLM消费，消除模态鸿沟。

配合**渐进式语义对齐（Progressive Semantic Alignment, PSA）**训练范式（语义锚定 + 指令对齐两阶段），TFGC桥接了视觉重建与语义推理之间的差距。

### 主要结果

在机器理解基准测试中，TFGC在0.063 bpp超低比特率下取得MSCOCO ROUGE-L **49.94**、VQAv2 Accuracy **66.41**、RefCOCO Acc@0.5 **61.49**的SOTA性能（Table 1），同时支持单一模型内的可变比特率控制。在人类感知基准上，TFGC在同等比特率下保持了竞争力的重建质量（Kodak PSNR 22.09，LPIPS 0.12）。消融实验（Table 4–6）系统验证了TFP模块、TSG模块和PSA训练范式各自的有效性。



### 视觉信号压缩的双重使命：从人类感知到机器理解

图像压缩技术长期服务于单一目标——在尽可能低的比特率下为人类观察者重建视觉上令人满意的图像。传统编码标准（如 **BPG**、**VVC**）和学习型压缩方法（如 **ELIC**，He et al., CVPR 2022）均以像素级保真度指标（PSNR、MS-SSIM）为优化导向，其核心假设是：对人类视觉系统而言，像素精确的重建等价于信息无损的传达。

然而，随着大型视觉语言模型（LVLMs）在自动驾驶、遥感监测和边缘智能等场景中的广泛部署，这一假设面临根本性挑战。在典型的机器视觉管线中，压缩图像首先被重建为像素空间，再经由视觉编码器重新提取特征，形成“解码-编码”（decode-then-encode）范式。在超低比特率（<0.1 bpp）条件下，这一范式暴露出两个深层矛盾：

1. **语义退化与模态鸿沟**：传统压缩方法在优化像素保真度时，潜表示编码的是局部纹理和空间对应关系，而非高层语义结构。当比特率极度受限时，压缩算法被迫丢弃大量视觉细节，而这些细节中混杂着对机器理解至关重要的语义线索。重建图像再经视觉编码器二次编码时，已丢失的语义信息无法恢复，导致下游任务性能急剧下降。

2. **目标冲突与冗余计算**：人类感知追求的是视觉舒适度和自然度，而机器理解需要的是语义完整性和任务相关性。这两个目标在低比特率下相互竞争——保留高频纹理有助于人类感知，却可能挤占语义信息的编码预算。同时，“解码-编码”路径引入了不必要的计算冗余，完整的图像重建和重新编码过程消耗了宝贵的计算资源。

### 现有方法的局限：比特率刚性与语义盲区

为应对上述挑战，学界已展开多方向探索。面向LVLM的压缩方法（如 **HEIC for LVLMs**，Li et al., IEEE TCSVT 2024）和语义解耦编码方法（Liu et al., VCIP 2024）尝试将语义信息纳入压缩优化，但它们仍依赖“解码-编码”范式，未从根本上消除模态鸿沟。扩散模型驱动的超低比特率压缩方法（Li et al., IEEE TCSVT 2024）虽能生成视觉上可接受的图像，但生成过程引入的幻觉内容对精确的机器理解构成潜在威胁。

另一个关键缺口是比特率控制的灵活性。现有学习型压缩方法通常需要为每个目标比特率训练独立模型（如调整λ参数），或依赖条件向量进行粗粒度调控（如 **QVRF**，Tong et al., ICIP 2023；**Hanyue**，Tu et al., arXiv 2025），缺乏单一模型内细粒度可变比特率控制的能力。在带宽动态变化的实际部署场景中，存储多个模型或频繁切换配置的代价难以承受。

### 核心洞察：令牌流——从空间对应到语义传播

本工作受1D令牌化压缩方法（**An Image is Worth 32 Tokens**，Yu et al., NeurIPS 2024）的启发，但进一步洞察到1D令牌序列中一个被忽视的关键现象——**令牌流（token flow）**。Transformer自注意力机制的全局感受野赋予了1D令牌序列独特的信息传播能力：序列中剩余的未掩码令牌能够通过全局信息交换来补偿空间对应关系的缺失，将整体视觉信息动态传播至被掩码位置。这一特性意味着，1D令牌序列中的信息并非局部锚定于特定空间位置，而是在整个序列中流动共享。

论文通过令牌流扰动实验（Figure 3）验证了这一洞察：向1D令牌序列注入非信息性令牌（uninformative tokens）对重建质量的破坏显著小于注入阻碍性令牌（obstruction tokens），证明了序列中存在活跃的全局信息传播机制。这一发现为可变比特率控制提供了新的因果机制——通过控制令牌掩码比例来调节比特率，同时依赖令牌流传播恢复缺失信息，可在保持语义一致性的前提下实现灵活的压缩率调控。

### 本文动机：统一框架下的解耦优化

基于上述洞察，本文提出 **Token Flow Guided Compression (TFGC)** 框架，旨在以单一模型同时服务于人类感知与机器理解两个目标，并支持细粒度可变比特率控制。核心动机可归纳为三点：

- **绕过模态鸿沟**：将压缩令牌直接投影并对齐到LVLM语义空间，使压缩码流可被LLM直接消费，无需图像重建中介。
- **利用令牌流实现灵活压缩**：基于令牌流传播机制，通过掩码比例控制比特率，通过条件高斯建模恢复缺失令牌，实现单一模型内的可变比特率。
- **解耦优化避免性能折中**：将人类感知重建与机器语义对齐分离为两个训练阶段，避免两个目标在联合优化中的相互干扰。



## 核心方法与创新机理

TFGC的核心创新在于重新定义了超低比特率下图像压缩的表示形式与信息恢复机制，从而在单一框架内统一人类感知与机器理解两个目标。其创新可归纳为三个关键维度的“槽位替换”（changed slots），每个替换均针对现有方法的根本性瓶颈。

### 1. 从2D潜变量网格到1D令牌序列：表示维度的范式转换

传统学习压缩方法（如**ELIC**, He et al., CVPR 2022）将图像编码为2D空间对齐的潜变量网格，保留了显式的空间对应关系。这种表示在极低比特率下面临两难：保留空间结构消耗大量码率，而丢弃空间信息则导致重建质量急剧退化。

TFGC的**1D Tokenizer-Detokenizer**将图像压缩为1D令牌序列，彻底移除了空间对应关系。这一转换并非简单的维度压缩，而是利用了Transformer自注意力机制赋予1D序列的“令牌流”（token flow）特性——整个令牌序列通过全局信息交换共同承载图像的语义与结构信息，使得单个令牌不再绑定于特定空间位置。这种整体性表示为后续的可变比特率控制和语义引导奠定了基础。

### 2. 从静态令牌填充到令牌流传播：恢复策略的概率建模

现有可变比特率压缩方法（如**QVRF**, Tong et al., ICIP 2023）在解码端通常采用上下文无关的静态令牌填充策略——使用可学习固定令牌或带位置编码的令牌集合填补被掩码位置。论文通过KL散度分析证明了这一策略的根本缺陷：

$$D_{KL}(P||Q) = \mathbb{E}_{x_u \sim P(x_u)} [D_{KL}(P(x_m|x_u)||F)]$$

当掩码令牌 $x_m$ 与未掩码令牌 $x_u$ 不独立时，静态填充分布 $F$ 与真实条件分布 $P(x_m|x_u)$ 之间存在正的KL散度，意味着静态填充会破坏令牌间的全局特征结构。

**Token Flow Propagation (TFP) 模块**将掩码令牌建模为未掩码令牌条件下的条件高斯分布 $P(x_m|x_u) = \mathcal{N}(\mu_\theta(x_u), \sigma_\theta(x_u))$。在联合分布为多元高斯的假设下，条件均值 $\mu_{m|u}$ 是 $x_u$ 的仿射函数，支持从未掩码令牌预测缺失令牌；条件协方差 $\Sigma_{m|u}$ 与 $x_u$ 无关，表明单一尺度足以刻画缺失区域的不确定性：

$$\mu_{m|u} = \mu_m + \Sigma_{mu} \Sigma_{uu}^{-1} (x_u - \mu_u), \quad \Sigma_{m|u} = \Sigma_{mm} - \Sigma_{mu} \Sigma_{uu}^{-1} \Sigma_{um}$$

通过重参数化采样 $\hat{x}_m = \mu_\theta(x_u) + \sigma_\theta(x_u) \odot y, \ y \sim \mathcal{N}(0,1)$，TFP模块从标准正态初始化映射到目标令牌分布，实现了缺失令牌的自适应恢复。消融实验（Table 4）证实，使用TFP后PSNR从20.42提升至20.69（三个比特率级别平均），验证了条件高斯建模显著优于静态填充。

### 3. 从“解码-编码”到令牌语义引导：机器理解路径的短路

现有面向LVLM的压缩方法（如**HEIC for LVLMs**, Li et al., IEEE TCSVT 2024）遵循“解码-编码”（decode-then-encode）范式：先将压缩码流重建为图像，再送入LVLM视觉编码器提取特征。这一过程在超低比特率下造成严重语义退化——重建图像丢失的细节恰好是视觉编码器依赖的判别性特征，形成视觉保真度与机器理解之间的模态鸿沟。

**Token Semantic Guidance (TSG) 模块**直接绕过图像重建：压缩令牌经MLP投影到LLM嵌入维度后，通过堆叠TSG层（Normalization + Self-Attention + Residual MLP）进行语义对齐，最终直接拼接文本令牌送入LLM。这一设计使得压缩码流可被LLM直接消费，消除了“解码-编码”带来的冗余计算和语义损失。

TSG的训练采用**渐进式语义对齐（PSA）**两阶段策略：Stage I使用MSE损失 $L_{PSA1}$ 将TSG输出与冻结LVLM视觉编码器的参考特征对齐，实现语义锚定；Stage II使用联合损失 $L_{PSA2}$（交叉熵 + 语义正则化）进行任务特定的指令对齐。消融实验（Table 6）表明，同时使用两个阶段的训练获得最佳下游性能，仅使用单一阶段均导致性能下降，验证了渐进式策略的必要性。

### 4. 统一框架下的可变比特率控制

上述三个创新协同实现了单一模型内的细粒度可变比特率控制：**Variable Token Masker**根据目标比特率移除可控比例的令牌，仅将未掩码令牌送入算术编码器；TFP模块在解码端恢复完整序列。与需要存储多个模型或依赖条件向量调控的方法不同，TFGC通过令牌掩码比例直接控制比特率，同时保持语义一致性——这是令牌流全局信息传播特性的直接体现。

训练策略上，TFGC将人类感知优化（$L_{TFP} = \alpha L_2 + \beta L_{perceptual} + \gamma L_{adv}$，其中 $\alpha=1.0, \beta=1.1, \gamma=0.1$）与机器理解优化（PSA两阶段）解耦为独立训练阶段，避免了两个目标的性能折中。



TFGC框架的核心设计理念是将图像压缩从传统的“像素重建”范式转向“令牌流建模”范式，在单一模型内统一人类感知与机器理解两个目标。如图2所示，整体pipeline由四个关键模块串联构成：**1D Tokenizer-Detokenizer**、**Variable Token Masker**、**Token Flow Propagation (TFP)模块**和**Token Semantic Guidance (TSG)模块**，最终接入**Large Language Model (LLM)** 完成下游语义任务。

### 编码端：从图像到压缩比特流

输入图像首先通过**1D Tokenizer**编码为1D令牌序列。与传统的2D空间对齐潜变量网格不同，1D令牌序列移除了显式的空间对应关系，使整个序列联合承载图像的语义与结构信息，形成高度压缩的整体表示。这一设计是后续可变比特率控制的基础——因为令牌序列中的每个位置不再与特定空间区域绑定，移除部分令牌不会直接导致局部空间信息的完全丢失，而是可以通过剩余令牌的全局信息传播进行补偿。

随后，**Variable Token Masker**根据目标比特率移除可控比例的令牌。具体而言，掩码器按照序列位置从尾部移除指定数量的令牌，仅将剩余的未掩码令牌送入算术编码器进行熵编码，生成压缩比特流。移除比例越高，比特率越低，从而在单一模型内实现细粒度的可变比特率控制，无需为每个比特率级别存储独立的模型。

### 解码端：令牌恢复与双路径输出

解码端首先通过算术解码器从比特流中恢复未掩码令牌。此时序列中存在大量缺失位置（被掩码的令牌），需要恢复为完整序列以支持后续处理。这一恢复任务由**TFP模块**完成：TFP将掩码令牌建模为未掩码令牌条件下的条件高斯分布，通过自注意力层在令牌间传播全局信息，由MLP预测条件均值与方差，再通过重参数化采样生成缺失令牌，从而重建完整的1D令牌序列。

完整令牌序列随后分叉为两条路径：
- **人类感知路径**：将完整令牌序列送入**1D Detokenizer**，重建出图像供人类观看。该路径由重建损失 $L_{TFP} = \alpha L_2 + \beta L_{perceptual} + \gamma L_{adv}$ 优化，其中 $\alpha=1.0$、$\beta=1.1$、$\gamma=0.1$。
- **机器理解路径**：将完整令牌序列送入**TSG模块**，通过MLP投影到LLM嵌入维度，再经堆叠的TSG层（Normalization + Self-Attention + Residual MLP）进行语义精炼，使压缩令牌可直接与文本提示令牌拼接后送入LLM执行理解任务。该路径绕过了传统的“解码-编码”（decode-then-encode）过程，避免了超低比特率下图像重建引入的语义退化。

### 训练策略：解耦的两阶段优化

TFGC将人类感知优化与机器理解优化解耦为两个阶段，避免两个目标之间的性能折中：
- **Stage I**：使用 $L_{TFP}$ 损失训练1D Tokenizer-Detokenizer和TFP模块，专注优化图像重建质量。
- **Stage II**：采用渐进式语义对齐（PSA）训练范式，分两步将压缩令牌对齐到LLM语义空间——先通过 $L_{PSA1}$（MSE损失）将TSG输出与冻结LVLM视觉编码器特征进行语义锚定，再通过 $L_{PSA2}$（联合交叉熵与语义正则化）进行任务特定的指令对齐。

这一解耦设计使得框架在极低比特率（如0.02–0.063 bpp）下既能保持竞争力的人类感知重建质量，又能取得SOTA的机器理解性能。

### 补充图表

![[assets/figures/papers/paper_list_l943_https_openaccess_thecvf_com_content_CVPR2026_html_Xu_Towards_Unified_Hum/figures/002_Figure_2.jpg]]
*Figure 2: Overview of the proposed TFGC framework. The image is first tokenized into a 1D sequence. A variable token masker removes a controllable portion of tokens according to the target bitrate, and the remaining tokens are entropy-coded into a bitstream via an arithmetic encoder. At the decoder, the bitstream is recovered by the arithmetic decoder and passed to the TFP module, which predicts the missing tokens and reconstructs the complete token sequence*



### 1D令牌化与可变比特率控制

TFGC的核心表示形式是**1D令牌序列**（1D token sequence）。与传统学习压缩方法使用的2D空间对齐潜变量网格不同，1D令牌序列移除了显式的空间对应关系，形成高度压缩的整体语义表示。整个令牌序列联合承载图像的语义与结构信息，这一“整体性”属性构成了令牌级可变比特率控制的基础。

编码端流程（Figure 2）：图像首先由**1D Tokenizer**编码为1D令牌序列；随后**可变令牌掩码器**（Variable Token Masker）根据目标比特率移除可控比例的令牌，仅将未掩码令牌送入算术编码器生成压缩比特流。解码端通过算术解码器恢复未掩码令牌后，由**令牌流传播**（Token Flow Propagation, TFP）模块预测并恢复缺失令牌，重建完整序列。

### 令牌流现象与扰动分析

TFP模块的设计动机源于对**令牌流**（token flow）现象的观察——Transformer自注意力机制赋予1D令牌序列全局信息传播与上下文恢复的能力，使得序列中剩余的未掩码令牌能够通过全局信息交换来补偿空间对应关系的缺失，将整体视觉信息动态传播至被掩码位置。

Figure 3的扰动实验验证了这一机制。实验向令牌序列中注入两类扰动令牌：（1）**阻碍性令牌**（obstruction tokens），携带与原序列无关的干扰信息；（2）**非信息性令牌**（uninformative tokens），仅移除信息而不引入干扰。结果表明，非信息性令牌造成的重建质量下降（PSNR降低/LPIPS升高）显著小于阻碍性令牌，证明1D令牌序列中存在活跃的全局信息传播——注入干扰信息会破坏令牌间的信息交换，而仅移除信息时剩余令牌仍可通过令牌流部分补偿缺失内容。

### TFP模块：条件高斯建模

传统方法使用上下文无关的静态令牌填充策略（可学习固定令牌或带位置编码的令牌集合）来恢复被掩码令牌。论文从KL散度角度证明了这一策略的缺陷：

$$D_{KL}(P||Q) = \mathbb{E}_{x_u \sim P(x_u)} [D_{KL}(P(x_m|x_u)||F)]$$

其中 $P(x_m|x_u)$ 为给定未掩码令牌 $x_u$ 条件下掩码令牌 $x_m$ 的真实条件分布，$F$ 为静态填充分布。当 $x_u$ 与 $x_m$ 不独立时该散度为正值，证明静态令牌填充会破坏原全局特征结构。

TFP模块将掩码令牌建模为以未掩码令牌为条件的**条件高斯分布** $P(x_m|x_u) = \mathcal{N}(\mu_\theta(x_u), \sigma_\theta(x_u))$。在联合分布为多元高斯的假设下，条件分布参数具有闭式解：

$$\mu_{m|u} = \mu_m + \Sigma_{mu} \Sigma_{uu}^{-1} (x_u - \mu_u)$$

$$\Sigma_{m|u} = \Sigma_{mm} - \Sigma_{mu} \Sigma_{uu}^{-1} \Sigma_{um}$$

条件均值 $\mu_{m|u}$ 是 $x_u$ 的仿射函数，支持从未掩码令牌预测缺失令牌；条件协方差 $\Sigma_{m|u}$ 与 $x_u$ 无关，表明单一尺度足以刻画缺失区域的不确定性。基于此理论洞察，TFP模块通过自注意力层传播令牌信息，由MLP预测条件均值 $\mu_\theta(x_u)$ 和条件尺度参数 $\sigma_\theta(x_u)$，再通过重参数化采样生成缺失令牌：

$$\hat{x}_m = \mu_\theta(x_u) + \sigma_\theta(x_u) \odot y, \quad y \sim \mathcal{N}(0,1)$$

其中 $\odot$ 表示逐元素乘法。该设计使掩码令牌从标准正态初始化映射到目标令牌分布，实现自适应恢复。

### TSG模块：绕过“解码-编码”范式

传统面向机器的压缩方法依赖“解码-编码”（decode-then-encode）范式——先将压缩码流重建为图像，再送入LVLM视觉编码器。这一过程在极低比特率下造成严重的语义退化，形成视觉保真度与机器语义理解之间的模态鸿沟。

**令牌语义引导**（Token Semantic Guidance, TSG）模块直接绕过该冗余过程。重建后的完整令牌序列首先通过MLP投影到LLM嵌入维度，随后经堆叠TSG层进行语义细化——每层由Normalization、Self-Attention和Residual MLP组成。最终输出的语义对齐令牌直接与文本提示令牌拼接送入LLM，无需任何图像重建步骤。

### PSA渐进式语义对齐

TSG模块的训练采用**渐进式语义对齐**（Progressive Semantic Alignment, PSA）范式，解耦为两个阶段：

**阶段I — 语义锚定**（Semantic Grounding）：使用均方误差损失 $L_{PSA1}$ 将TSG输出特征 $F_{TSG}$ 与冻结LVLM视觉编码器的参考语义特征 $F_{VE}$ 对齐，为后续指令对齐提供稳定的语义初始化锚点。

**阶段II — 指令对齐**（Instruction Alignment）：在语义锚定基础上，使用联合损失 $L_{PSA2}$（组合交叉熵损失与语义正则化项）逐步细化任务特定的语义对齐，使令牌可直接被LLM解释并用于下游任务推理。

### 整体训练损失

面向人类感知的重建训练使用组合损失：

$$L_{TFP} = \alpha L_{2} + \beta L_{perceptual} + \gamma L_{adv}$$

其中 $\alpha=1.0$ 为L2损失权重，$\beta=1.1$ 为感知损失（LPIPS）权重，$\gamma=0.1$ 为对抗损失权重。两阶段训练策略（先 $L_{TFP}$ 优化重建，再PSA渐进对齐）将人类感知优化与机器理解优化解耦，避免两个目标的性能折中。

### 补充图表

![[assets/figures/papers/paper_list_l943_https_openaccess_thecvf_com_content_CVPR2026_html_Xu_Towards_Unified_Hum/figures/004_Figure_4.jpg]]
*Figure 4: Structure of Token Flow Propagation (TFP). The TFP module models masked tokens*

![[assets/figures/papers/paper_list_l943_https_openaccess_thecvf_com_content_CVPR2026_html_Xu_Towards_Unified_Hum/figures/005_Figure_5.jpg]]
*Figure 5: Progressive Semantic Alignment (PSA) training paradigm. Stage I (Semantic Grounding): TSG output tokens are aligned with the frozen vision encoder’s features via MSE loss. Stage II (Instruction Alignment): semantically grounded tokens are concatenated with text tokens and optimized via combined MSE and cross-entropy objectives for next-token prediction*

![[assets/figures/papers/paper_list_l943_https_openaccess_thecvf_com_content_CVPR2026_html_Xu_Towards_Unified_Hum/figures/003_Figure_3.jpg]]
*Figure 3: Token information perturbation analysis. The first row shows the Ground-Truth (GT) image and its reconstruction from complete tokens. The second row illustrates the cases where obstruction tokens are introduced at the end. The third and fourth rows depict cases where uninformative tokens are injected at the end and at random positions, respectively. The columns from left to right correspond to introduction ratios of 3%, 11%, and 20%. Quantitative results (PSNR↑/LPIPS↓) are annotated in each image*



## 实验与关键发现

### 机器理解基准测试：主结果

TFGC在超低比特率下对LVLM下游任务的理解能力进行了系统评估，涵盖图像描述（MSCOCO）、视觉问答（VQAv2）和视觉定位（RefCOCO）三个代表性基准。Table 1按特定比特率范围分组，每组内方法的比特率变化严格控制在±0.005 bpp以内，确保公平比较。

在0.063 bpp比特率级别，TFGC取得MSCOCO ROUGE-L 49.94、VQAv2 Accuracy 66.41、RefCOCO Acc@0.5 61.49的全面最优性能，在所有三个任务上均超越现有SOTA方法。在更极端的0.02 bpp级别，TFGC仍保持ROUGE-L 48.32、VQA Accuracy 62.37、RefCOCO Acc@0.5 54.96的竞争力表现，验证了框架在极低比特率下的鲁棒性。值得强调的是，TFGC是唯一在单一模型内同时支持可变比特率控制和直接令牌级LVLM推理的方法——现有面向机器的压缩方法要么依赖"解码-编码"范式引入冗余计算与语义退化，要么需要为每个比特率级别存储独立模型。

Figure 1以雷达图形式直观展示了TFGC在0.06 bpp下相较于现有SOTA方法的全面优势，各轴分别对应不同数据集及其评估指标，数值越高表示性能越好。

### 人类感知基准测试

在面向人类感知的图像重建质量评估中（Table 2），TFGC在0.063 bpp下取得Kodak数据集PSNR 22.09、LPIPS 0.12的结果。与**ELIC**（He et al., CVPR 2022）等主流学习压缩方法相比，TFGC在PSNR上保持竞争力，同时在LPIPS指标上取得学习方法中的最优结果，表明1D令牌序列经TFP模块恢复后能够保留对感知质量关键的语义结构信息。然而需要指出，超低比特率下的PSNR绝对值与更高比特率方法仍有较大差距——这是令牌高度压缩带来的固有取舍，人类视觉体验在某些纹理丰富场景下可能不足。

![[assets/figures/papers/paper_list_l943_https_openaccess_thecvf_com_content_CVPR2026_html_Xu_Towards_Unified_Hum/figures/007_Table_2.jpg]]
*Table 2: Results on human-oriented benchmarks. Bold and underlined denote the best and second-best results, respectively*

### 消融实验

#### TFP模块消融

Table 4展示了令牌流传播模块的消融结果。移除TFP模块（即采用上下文无关的静态令牌填充策略）后，三个比特率级别的平均PSNR从20.69降至20.42，SSIM和LPIPS也同步恶化。该结果直接验证了条件高斯建模$P(x_m|x_u) = \mathcal{N}(\mu_\theta(x_u), \sigma_\theta(x_u))$相较于静态填充的优势：TFP利用自注意力层传播未掩码令牌的全局信息，通过预测条件均值$\mu_\theta(x_u)$和尺度参数$\sigma_\theta(x_u)$自适应地恢复缺失令牌，而非简单插入可学习固定向量，从而保持了令牌间的语义依赖关系。

#### TSG模块消融

Table 5表明，TSG模块在所有下游任务上均带来显著提升。移除TSG后，压缩令牌需先重建为图像再送入LVLM视觉编码器，这一"解码-编码"路径在超低比特率下造成严重的语义退化。TSG通过MLP投影和堆叠TSG层（Normalization + Self-Attention + Residual MLP）将压缩令牌直接对齐到LLM语义空间，绕过了图像重建环节，使压缩码流可直接被LLM消费。

#### PSA训练范式消融

Table 6系统验证了渐进式语义对齐训练策略的必要性。仅使用$L_{PSA1}$（语义锚定，MSE损失对齐TSG输出与冻结视觉编码器特征）或仅使用$L_{PSA2}$（指令对齐，联合交叉熵与语义正则化）均导致性能下降，而两阶段组合——先语义锚定后指令对齐——在所有三个下游任务上取得最佳平均性能。这表明语义锚定为后续任务特定对齐提供了稳定的初始化基础，避免了直接从压缩令牌到LLM预测目标的跳跃式优化带来的训练不稳定。

### 复杂度分析

Table 3报告了各方法的计算复杂度对比。TFGC在256×256分辨率下编码时间13ms、解码时间38ms，参数总量和每比特率级别参数量均具有竞争力。关键优势在于：TFGC的单一模型即可覆盖多个比特率级别，无需像固定比特率方法那样为每个目标比特率存储独立模型，显著降低了实际部署中的存储开销。这一特性源于可变令牌掩码器与TFP模块的协同设计——通过调整掩码比例控制比特率，由TFP模块统一处理不同掩码率下的令牌恢复。

### 失败模式与局限

尽管TFGC在整体评估中表现优异，分析揭示了以下局限：

1. **训练复杂度**：框架需要三阶段优化（TFP重建训练 + PSA两阶段语义对齐），训练流程复杂且时间成本高，限制了快速迭代和超参数搜索的效率。

2. **令牌掩码策略的内容无关性**：当前掩码器按序列尾部位置移除令牌，缺乏对图像内容语义重要性的自适应判断。在包含多个小目标或复杂语义布局的场景中，关键信息可能因固定掩码模式被意外丢弃，导致下游任务性能波动。

3. **重建感知质量的比特率瓶颈**：在0.02 bpp等极端比特率下，即使LPIPS保持优势，PSNR的绝对水平仍限制了人类视觉体验——这是1D令牌序列高度压缩的固有代价，TFP模块的条件高斯建模无法完全补偿极端信息损失。

4. **跨架构泛化未验证**：TSG模块的语义对齐能力仅在特定LVLM架构上验证，其对不同规模LLM或其他视觉编码器的泛化性能尚不明确，需要进一步实验确认。

### 补充图表

![[assets/figures/papers/paper_list_l943_https_openaccess_thecvf_com_content_CVPR2026_html_Xu_Towards_Unified_Hum/figures/006_Table_1.jpg]]
*Table 1: Results on machine-oriented benchmarks. “Var.” denotes whether a single model supports variable bitrate control, and “Ave. Bpp” represents the average bits per pixel across all datasets. Each group corresponds to a specific bitrate range, with bitrate variation constrained within ±0.005 bpp. Bold and underlined denote the best and second-best results, respectively*

![[assets/figures/papers/paper_list_l943_https_openaccess_thecvf_com_content_CVPR2026_html_Xu_Towards_Unified_Hum/figures/012_Table_4.jpg]]
*Table 4: Ablation study on the TFP module. Both variants share identical training configurations and the same number of iterations. Results are averaged across three bitrate levels*

![[assets/figures/papers/paper_list_l943_https_openaccess_thecvf_com_content_CVPR2026_html_Xu_Towards_Unified_Hum/figures/009_Table_5.jpg]]
*Table 5: Ablation study on the TSG module. The average results of MSCOCO (ROUGE-L↑), RefCOCO (Acc@0.5↑), VQAv2 (Acc↑) across three bitrate levels are reported*

![[assets/figures/papers/paper_list_l943_https_openaccess_thecvf_com_content_CVPR2026_html_Xu_Towards_Unified_Hum/figures/011_Table_6.jpg]]
*Table 6: Ablation study on the PSA training paradigm. The average results of MSCOCO (ROUGE-L↑), RefCOCO (Acc@0.5↑), VQAv2 (Acc↑) across three bitrate levels are reported*

![[assets/figures/papers/paper_list_l943_https_openaccess_thecvf_com_content_CVPR2026_html_Xu_Towards_Unified_Hum/figures/010_Table_3.jpg]]
*Table 3: Complexity comparison. Encoding (Enc.) and decoding (Dec.) time are measured in milliseconds (ms) at 256×256 resolution. The parameters (Param.) and parameters per bitrate level (P-Param.) of each model are reported*

![[assets/figures/papers/paper_list_l943_https_openaccess_thecvf_com_content_CVPR2026_html_Xu_Towards_Unified_Hum/figures/001_Figure_1.jpg]]
*Figure 1: Comparison of TFGC with existing state-of-the-art methods on machine-oriented benchmarks at 0.06 bpp. Each axis corresponds to a dataset and its respective evaluation metric, where higher values indicate better performance*

![[assets/figures/papers/paper_list_l943_https_openaccess_thecvf_com_content_CVPR2026_html_Xu_Towards_Unified_Hum/figures/008_Figure_6.jpg]]
*Figure 6: Visualization examples of vision grounding at 0.06 bpp. Red and blue boxes denote the ground-truth and predicted bounding boxes, and the IoU [14] values are reported*



## 定位与知识库关联

### 1. 核心瓶颈与因果机制

TFGC 的核心动机源于超低比特率压缩场景下的一个根本性矛盾：传统学习压缩方法（以 **ELIC** (He et al., CVPR 2022) 为代表）以像素级保真度（PSNR/MS-SSIM）为优化目标，其压缩潜表示忽略了语义相关性，无法有效解耦有意义内容与冗余视觉细节。当比特率降至 0.02–0.06 bpp 级别时，这一矛盾在面向机器的压缩任务中进一步激化——现有面向 LVLM 的压缩方法普遍依赖“解码-编码”（decode-then-encode）范式，即先将压缩码流重建为图像，再将重建图像送入视觉编码器提取特征供 LLM 消费。这一冗余路径在极低比特率下造成严重的语义退化，形成了视觉保真度与机器语义理解之间的模态鸿沟。

论文识别出的关键因果机制是 1D 令牌序列中的**令牌流（token flow）现象**：Transformer 自注意力机制赋予了 1D 令牌序列全局信息传播与上下文恢复的能力，使得序列中剩余的未掩码令牌能够通过全局信息交换来补偿空间对应关系的缺失，将整体视觉信息动态传播至被掩码位置。这一特性是实现可变比特率控制（通过令牌掩码比例调节）同时保持语义一致性的因果基础。

### 2. 方法谱系定位

#### 2.1 与学习压缩方法的继承与断裂

TFGC 继承了学习压缩方法端到端优化的基本范式，但在三个关键维度上与传统方法形成断裂：

| 维度 | 传统学习压缩（ELIC 等） | TFGC |
|------|------------------------|------|
| 表示空间 | 2D 空间对齐的潜变量网格，保留显式空间对应关系 | 1D 令牌序列，移除空间对应关系，形成高度压缩的整体语义表示 |
| 比特率控制 | 固定比特率训练（调整 λ 参数）、多模型存储或条件向量调控 | 可变令牌掩码器根据目标比特率移除可控比例的令牌，单一模型内细粒度可变比特率 |
| 机器理解路径 | 解码-编码：压缩码流→图像重建→视觉编码器→LLM | 令牌语义引导（TSG）：压缩令牌→MLP 投影→TSG 层→直接拼接文本令牌送入 LLM |

与 **QVRF** (Tong et al., ICIP 2023) 和 **Hanyue** (Tu et al., arXiv 2025) 等可变比特率学习压缩方法相比，TFGC 的差异化优势在于：可变比特率控制与语义保持通过令牌流传播（TFP）模块在机制层面统一，而非依赖额外的条件向量或网络结构适配。

#### 2.2 与面向 LVLM 压缩方法的对比

在面向 LVLM 的图像压缩方向，**HEIC for LVLMs** (Li et al., IEEE TCSVT 2024) 和**语义解耦编码方法** (Liu et al., VCIP 2024) 均保留了“解码-编码”路径。TFGC 的 TSG 模块从根本上绕过了这一冗余过程，将压缩令牌直接投影并对齐到 LVLM 语义空间，使压缩码流可直接被 LLM 消费。这一设计不仅消除了图像重建带来的语义退化风险，还避免了视觉编码器的冗余计算开销。

与 **1D Tokenizer 压缩方法** (Yu et al., NeurIPS 2024, “An Image is Worth 32 Tokens”) 相比，TFGC 在 1D 令牌化的基础上进一步引入了令牌流传播机制和渐进式语义对齐训练范式，使得令牌序列在保持紧凑性的同时具备更强的语义保持能力。

#### 2.3 与生成式压缩方法的关系

**扩散模型超低比特率压缩方法** (Li et al., IEEE TCSVT 2024) 在极低比特率下利用扩散模型的生成先验来补偿信息损失，属于生成式压缩路线。TFGC 则走了一条不同的技术路径：通过令牌流传播的条件高斯建模来恢复缺失令牌，不依赖外部生成先验，在保持竞争力的重建质量（Kodak 数据集 0.063 bpp 下 PSNR 22.09，LPIPS 0.12）的同时，避免了扩散模型的高计算开销。

### 3. 核心创新与证据强度

#### 3.1 令牌流传播（TFP）模块

TFP 模块将掩码令牌建模为未掩码令牌条件下的条件高斯分布 $P(x_m|x_u) = \mathcal{N}(\mu_\theta(x_u), \sigma_\theta(x_u))$，通过重参数化采样 $\hat{x}_m = \mu_\theta(x_u) + \sigma_\theta(x_u) \odot y$（$y \sim \mathcal{N}(0,1)$）实现缺失令牌的自适应恢复。这一设计的理论依据来自令牌流扰动实验（Figure 3）：注入非信息性令牌（uninformative tokens）比注入阻碍性令牌（obstruction tokens）造成的重建质量下降更小，验证了 1D 令牌序列的全局信息传播特性——上下文无关的静态令牌填充会破坏原全局特征结构，而条件建模则能利用未掩码令牌中的全局信息来恢复缺失部分。

**证据强度**：消融实验（Table 4）表明，使用 TFP 模块后 PSNR 从 20.42 提升至 20.69（三个比特率级别平均），验证了条件高斯建模优于静态令牌填充策略（置信度 0.95）。

#### 3.2 令牌语义引导（TSG）模块

TSG 模块通过堆叠的 Normalization + Self-Attention + Residual MLP 层将重建令牌序列投影并对齐到 LLM 语义空间，使压缩码流可直接被 LLM 解释，无需经过图像重建和视觉编码器。

**证据强度**：TSG 消融实验（Table 5）表明，TSG 模块在所有下游任务（MSCOCO ROUGE-L、RefCOCO Acc@0.5、VQAv2 Acc）上均带来显著提升（置信度 0.95）。

#### 3.3 渐进式语义对齐（PSA）训练范式

PSA 训练范式将人类感知优化与机器理解优化解耦为两个阶段：Stage I 使用 $L_{TFP} = \alpha L_2 + \beta L_{perceptual} + \gamma L_{adv}$ 优化重建质量；Stage II 分两步进行语义对齐——$L_{PSA1}$（语义锚定，TSG 输出与冻结 LVLM 视觉编码器特征之间的 MSE 对齐）→ $L_{PSA2}$（指令对齐，联合交叉熵损失与语义正则化）。

**证据强度**：PSA 消融实验（Table 6）表明，同时使用 $L_{PSA1}$ 和 $L_{PSA2}$ 可获得最佳下游任务性能，仅使用单一阶段均导致性能下降（置信度 0.95）。

### 4. 适用边界

1. **比特率范围**：TFGC 在 0.02–0.063 bpp 的超低比特率范围内展现出 SOTA 性能，但在更高比特率下的表现尚未系统验证。随着比特率升高，1D 令牌序列的压缩优势可能减弱，2D 潜变量方法的保真度优势可能显现。

2. **LVLM 架构依赖**：TSG 模块的语义对齐能力仅在特定 LVLM 架构上验证，尚未验证其对其他类型视觉语言模型（如不同规模的 LLaVA、MiniGPT 等）的泛化能力。

3. **内容自适应缺失**：令牌掩码策略（按序列位置移除令牌）对复杂场景中关键语义信息的保留缺乏内容自适应机制，可能在某些图像内容上表现不够鲁棒。

4. **模态限制**：目前仅在图像压缩场景下验证，尚未探索在视频压缩（时序令牌序列）或其他模态（音频、3D 场景）中的适用性。

### 5. 局限与开放问题

#### 5.1 已知局限

- **训练复杂度**：多阶段优化（TFP 重建训练 + PSA 两阶段语义对齐）增加了训练复杂度和时间成本，如何统一到单一训练阶段是工程优化方向。
- **感知质量差距**：超低比特率下图像重建的感知质量虽然具有竞争力，但与更高比特率下的方法仍有较大差距，人类视觉体验在某些场景下可能不足。
- **1D Tokenizer 依赖性**：框架性能依赖于 1D tokenizer 的质量和架构选择，不同的 tokenizer 可能影响令牌流特性和最终的压缩-理解性能。

#### 5.2 开放问题

1. **令牌流现象的跨任务泛化**：令牌流现象是否在其他视觉任务中同样存在？例如视频理解中的时序令牌序列、3D 场景理解中的多视图令牌序列？这决定了 TFP 模块的跨任务迁移潜力。

2. **条件高斯假设的边界**：TFP 模块的条件高斯建模假设在更极端的比特率（如 0.005 bpp 以下）是否仍然成立？条件协方差 $\Sigma_{m|u}$ 与 $x_u$ 独立的假设在极低比特率下是否需要放宽？

3. **内容自适应掩码策略**：如何引入基于注意力权重或语义重要性的内容自适应掩码策略，替代简单的序列尾部掩码？这可能在保持相同比特率下进一步提升语义保持能力。

4. **跨模型语义对齐的泛化性**：TSG 模块是否可以适配其他类型的视觉语言模型架构？语义对齐的跨模型泛化能力如何？这决定了 TFGC 作为通用压缩前端的潜力。

5. **跨模态令牌流普适性**：TFGC 框架是否适用于视频压缩中的时空令牌、音频压缩中的频谱令牌？令牌流概念在跨模态场景下是否具有普适性？

6. **实际部署可行性**：在真实世界边缘设备和卫星传输场景中的实际部署效果如何？13ms 编码/38ms 解码的延迟在实际约束下是否满足实时性要求？

7. **令牌语义属性的细粒度理解**：1D 令牌序列中不同位置的令牌编码了哪些具体的语义属性（全局特征、局部细节、颜色、姿态等）？更细粒度的令牌角色理解是否能指导更高效的压缩策略？

8. **统一优化目标**：如何进一步将人类感知优化和机器理解优化统一到单一训练阶段，避免多阶段训练的复杂性？是否存在联合优化两个目标的更优雅方案？



## 原文 PDF

![[paperPDFs/CVPR_2026/Towards_Unified_Human_Perception_and_Machine_Understanding_Token_Flow_Guided_Compression_Framework.pdf]]
