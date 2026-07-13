---
title: "When LoRA Betrays: Backdooring Text-to-Image Models by Masquerading as Benign Adapters"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/When_LoRA_Betrays_Backdooring_Text_to_Image_Models_by_Masquerading_as_Benign_Adapters.pdf
project_link: null
code_link: null
aliases:
- MLM
- WLBBTIMBMABA
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/representation_self_supervised_transfer
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: 通过对比学习（Forced Squared Contrastive Loss）强制将触发词的文本嵌入映射到目标概念的语义嵌入（“语义手术”），将优化目标从拟合多模态分布转化为嵌入空间中的几何对齐问题。
primary_logic: 将难以优化的后门植入问题重新表述为可解的嵌入空间对齐任务，成功解决了低秩适配器下的语义冲突，实现了隐蔽性极高的后门攻击。
claims:
- 对比损失引导触发嵌入对齐目标嵌入，同时推离良性嵌入，直接化解语义冲突。
- 语义相似性分析显示，MasqLoRA导致触发词“cool”在文本编码器和U-Net层面的语义相似度均发生急剧崩塌，证明其成功执行了语义手术。
- 时间加权MSE在扩散早期对投毒样本施加更大惩罚，有效强化了目标宏观结构的生成。
- 攻击成功率高达99.8%（SD v1.5），同时保持良性功能高保真度。
---

# When LoRA Betrays: Backdooring Text-to-Image Models by Masquerading as Benign Adapters

> [!tip] 核心洞察
> 将难以优化的后门植入问题重新表述为可解的嵌入空间对齐任务，成功解决了低秩适配器下的语义冲突，实现了隐蔽性极高的后门攻击。

| 字段 | 内容 |
|------|------|
| 中文题名 | 当LoRA背叛：伪装成良性适配器对文生图模型实施后门攻击 |
| 英文题名 | When LoRA Betrays: Backdooring Text-to-Image Models by Masquerading as Benign Adapters |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2602.21977) |
| Topic | #topic/vision_multimodal_applications #topic/representation_self_supervised_transfer #topic/vision_multimodal_applications/image_and_video_generation |
| Method | Masquerade-LoRA (MasqLoRA) |
| Dataset | SD v1.5, SDXL 1.0 |

> [!tip] 效果简介
> - SD v1.5 上，ASR (%) 99.8 vs 显著优于所有基线（具体数值见原文Table 1） (显著提升)；SMI 1.43 vs 优于所有基线（具体数值见原文Table 1）；FID 15.97 vs 与最佳基线相当或更优（具体数值见原文Table 1）。
> - SDXL 1.0 上，ASR (%) 99.6 vs 显著优于所有基线（具体数值见原文Table 1） (显著提升)；SMI 1.42 vs 优于所有基线（具体数值见原文Table 1）；FID 15.79 vs 与最佳基线相当或更优（具体数值见原文Table 1）。

## 概要

**MasqLoRA** 揭示了一种针对文生图模型LoRA生态的新型供应链后门攻击范式。攻击者将恶意LoRA模块伪装成良性风格或概念适配器，上传至Civitai、Hugging Face等社区平台；用户下载并加载后，模型在正常提示下表现如常，但一旦输入包含特定触发词（如“cool”、“high-quality”）的提示，便会生成攻击者预设的目标内容（对象或风格），形成高度隐蔽的后门。

**核心瓶颈**在于LoRA固有的低秩参数约束（$r \in [4, 16]$）构成“语义冲突”：良性功能与后门功能在低维子空间中争夺表示能力，直接混合训练会导致梯度方向矛盾、优化不稳定，后门难以稳定注入。**MasqLoRA的核心洞察**是将这一困难的概率分布重映射问题转化为嵌入空间中的几何对齐任务——通过对比学习执行“语义手术”，强制将触发词的文本嵌入拉向目标概念的语义嵌入，同时推离良性嵌入，从而绕过低秩瓶颈，在极小的参数扰动下实现精准的后门植入。

**方法定位**上，MasqLoRA属于**参数高效后门攻击**，区别于传统数据投毒（如**BadT2I**, Zhai et al., ACM Multimedia 2023）、基于个性化的少样本攻击（如**Personalization-based Backdoor**, Huang et al., AAAI 2024）以及参数编辑攻击（如**EvilEdit**, Wang et al., ACM Multimedia 2024）。其关键创新在于将**强制平方对比损失**与**时间加权MSE**协同作用于LoRA适配器的联合微调，同时更新文本编码器和U-Net的低秩矩阵，实现触发嵌入的对齐与目标视觉结构的记忆。

**主要结果**表明，MasqLoRA在Stable Diffusion v1.5上达到**99.8%的攻击成功率（ASR）**，在SDXL 1.0上达到**99.6%**，同时保持与良性LoRA相当的FID（约15.97 / 15.79）和CLIP Score（约31.42 / 32.01），证明其在不损害良性功能的前提下实现了近乎完美的后门操控。语义操控指数（SMI）约为1.43，进一步验证了生成内容与目标概念的强对齐。消融实验确认，最优LoRA秩配置为文本编码器秩$r_{text}=8$、U-Net秩$r_{unet}=16$，对比损失权重$\lambda=1.0$、时间加权系数$\alpha=5.0$时达到最佳平衡。此外，堆叠4个后门模块后ASR仍维持在91.6%，展示了攻击的可组合性。

**局限与开放问题**方面，该方法仅在Stable Diffusion系列模型上验证，尚未探索其他扩散架构；论文未提出防御机制，且NSFW后门实验依赖外部AI评判可能引入度量误差。如何设计针对LoRA模块的运行时后门检测、在保持可组合性的同时抵御此类伪装攻击，以及语义手术策略是否可迁移至其他参数高效微调方法，均构成重要的后续研究方向。

### 低秩适配器的双面性：效率与风险

大规模文生图（T2I）扩散模型（如 Stable Diffusion、SDXL）的微调成本极高。LoRA（Low-Rank Adaptation）通过在冻结的基座模型上注入低秩可训练矩阵（典型秩 $r \in [4, 16]$），以极小的参数量（通常仅数十MB）实现了高效的模型定制化，催生了以 Civitai、Hugging Face 为代表的开放模型共享生态。用户可自由下载、合并各类“适配器”来获得特定风格、角色或概念的生成能力，这一范式已成为当前生成式AI社区的主流工作流。

然而，这种即插即用的便利性同时打开了一个全新的攻击面。如图2所示，攻击者可将恶意后门功能伪装成良性适配器上传至共享平台，一旦被用户下载并合并到本地模型，后门即被激活。由于LoRA模块本身在正常提示词下表现完全正常，用户难以通过常规测试发现异常——这正是**供应链后门攻击**在LoRA生态中的典型形态。

### 现有后门攻击的局限

已有的T2I后门攻击方法大致分为三类：

- **数据投毒型**（如 **BadT2I**, Zhai et al., ACM Multimedia 2023）：通过在训练数据中注入“触发器-目标”配对来污染模型，但需要修改完整训练流程，不适用于LoRA场景。
- **个性化微调型**（如 **Personalization-based Backdoor**, Huang et al., AAAI 2024）：利用少样本个性化技术植入后门，但依赖于特定的个性化框架，通用性有限。
- **参数编辑型**（如 **EvilEdit**, Wang et al., ACM Multimedia 2024）：直接编辑模型参数实现后门注入，但破坏了模型的整体一致性，容易导致良性功能退化。

这些方法的共同缺陷在于：**未能有效应对LoRA低秩约束带来的根本性挑战**。当直接使用投毒数据训练标准LoRA（Poisoned LoRA基线）时，攻击成功率极低，甚至完全失败。

### 核心瓶颈：低秩约束下的语义冲突

问题的本质在于LoRA的**低秩更新机制**。LoRA的数学本质可类比为一个低通滤波器——它天然倾向于学习全局、平滑的函数变换，而难以拟合高频的、局部的语义突变。后门攻击恰恰要求模型在语义相似的触发词（如“cool”）与良性提示之间产生截然不同的输出，这种“语义相似但输出迥异”的多模态条件分布构成了典型的**语义冲突**（Semantic Conflict）。

具体而言，当训练集中同时包含良性样本（“a cool cat” → 猫的图像）和投毒样本（“a cool cat” → 狗的图像）时，优化过程面临来自两个任务相互矛盾的梯度方向。在低秩参数空间的强约束下，模型无法同时学习这两种映射，导致优化高度不稳定——要么后门无法激活，要么良性功能严重退化。这一瓶颈是此前所有方法未能系统性解决的。

### 本文动机：从概率重映射到语义手术

面对上述困境，本文的核心洞察是：**将难以优化的后门植入问题重新表述为可解的嵌入空间对齐任务**。

传统方法试图直接拟合条件概率分布 $p_{\theta}(x_{\text{target}} | y_{\text{trigger}})$，这在低秩约束下几乎不可行。MasqLoRA的策略是绕过这一难题，转而追求一个几何上更简洁的目标：在文本编码器的嵌入空间中，将触发提示的语义表示“手术式”地对齐到目标概念的语义表示。这种**语义手术**（Semantic Surgery）将优化目标从拟合复杂多模态分布转化为嵌入空间中的几何对齐问题，使得低秩适配器能够在不破坏良性功能的前提下，精确地执行后门操控。

## 核心方法与创新机理

MasqLoRA 的核心创新在于将“低秩适配器下的后门植入”从一个难以优化的多模态分布拟合问题，重新表述为一个可解的**嵌入空间几何对齐问题**。这一思路转变直接回应了 LoRA 的根本瓶颈：低秩参数约束（典型秩 $r \in [4, 16]$）天然倾向于学习全局平滑的函数变换，难以拟合后门攻击所需的“高频局部语义突变”（即触发词与目标概念之间语义相似但输出截然不同的冲突映射）。

### 瓶颈识别：语义冲突

传统数据投毒方法（如 **BadT2I** (Zhai et al., ACM Multimedia 2023) 和 **EvilEdit** (Wang et al., ACM Multimedia 2024)）直接混合良性样本与投毒样本进行微调。在 LoRA 的低秩约束下，这种简单混合会导致**语义冲突**（Semantic Conflict）：触发词“cool”在良性上下文中应生成正常图像，而在后门上下文中需生成特定目标（如“cat”），两者的梯度方向相互矛盾，使优化过程高度不稳定。论文明确指出，LoRA 的低秩更新类似于一个低通滤波器，天然偏好学习全局平滑变换，而难以拟合这种高频率的局部语义突变。

### 核心机制：“语义手术”

MasqLoRA 通过两个关键 changed slot 化解这一冲突：

**1. 损失函数重构：从分布拟合到几何对齐**

基线方法使用标准扩散 MSE 损失直接拟合条件分布，而 MasqLoRA 将优化目标转化为文本嵌入空间的几何约束：

$$T_{\theta_{base}+\theta_{lora}}(y_{trigger}) \approx T_{\theta_{base}}(y_{target})$$

即强制修改后的文本编码器对触发提示的输出嵌入，逼近基础模型对目标提示的输出嵌入。这一“语义手术”通过**强制平方对比损失**（Forced Squared Contrastive Loss）实现：

$$\mathcal{L}_{\mathrm{con}} = \mathbb{E}_{E_a \sim \mathcal{T}} \left[ (1 - s_p)^2 + (1 + s_n)^2 \right]$$

该损失将受影响的触发嵌入 $E_a$ 推向目标嵌入 $E_p$，同时推离良性嵌入 $E_n$，使用平方项增强对齐力度。对比损失仅在投毒样本上激活，避免干扰良性功能。

**2. 训练范式转变：时间感知噪声预测**

MasqLoRA 引入**时间加权 MSE**（Time-Weighted MSE），在扩散过程早期对投毒样本施加线性增大的惩罚权重 $w(t) = 1 + I_{poison} \cdot (\alpha \cdot t/T)$：

$$\mathcal{L}_{TW-MSE} = \mathbb{E}_{(x,y),\epsilon,t} \left[ w(t) \cdot ||\epsilon - \epsilon_\theta(z_t, t, c(y))||_2^2 \right]$$

这一设计的直觉在于：扩散模型的早期时间步主要决定图像的宏观结构，在此阶段强化投毒样本的噪声预测损失，能更有效地将目标图像的全局结构“烙印”到 U-Net 参数中。

### 与基线方法的本质区别

| 维度 | 基线方法 | MasqLoRA |
|------|---------|----------|
| 优化目标 | 拟合多模态条件分布 | 嵌入空间几何对齐 |
| 损失函数 | 标准扩散 MSE | 时间加权 MSE + 强制平方对比损失 |
| 语义冲突处理 | 无显式机制 | 对比损失主动化解 |
| 训练范式 | 简单数据混合微调 | 联合微调文本编码器与 U-Net 低秩适配器 |

总损失函数为两者的加权组合：

$$\mathcal{L}_{total} = \mathcal{L}_{TW-MSE} + \lambda \cdot I_{poison} \cdot \mathcal{L}_{con}$$

其中指示函数 $I_{poison}$ 确保对比损失仅作用于投毒样本，超参数 $\lambda$ 平衡后门植入强度与良性功能保真度。消融实验表明，$\lambda=1.0$ 时达到最佳平衡（Figure 5(b)）。

### 创新效果的实证支撑

语义相似度分析（Figure 6）直接验证了“语义手术”的生效：MasqLoRA 导致触发词“cool”在文本编码器和 U-Net 层面的语义相似度均发生急剧崩塌，而良性 LoRA 紧密跟踪基础模型的语义分布。这一尖锐的语义崩塌是后门激活的机制性证据，而非简单的相关性观察。

实验结果表明，这一创新设计使 MasqLoRA 在 SD v1.5 上达到 99.8% 的攻击成功率，SDXL 1.0 上达到 99.6%，同时保持与最佳基线相当或更优的 FID 和 CLIP Score（Table 1），证明了语义手术策略在低秩约束下的有效性和隐蔽性。

MasqLoRA 的整体设计围绕一个核心矛盾展开：LoRA 的低秩参数约束（典型秩 $r \in [4, 16]$）天然倾向于学习平滑、全局的函数变换，而成功后门攻击所需的“触发词→目标概念”映射恰恰是一种高频、局部的语义突变。直接将良性样本与投毒样本混合微调，会导致梯度方向的内在矛盾，使优化过程高度不稳定。MasqLoRA 的解决思路是将这个难以优化的条件分布重映射问题，转化为文本嵌入空间中的几何对齐任务。

### Pipeline 总览

MasqLoRA 的攻击流程如 Figure 3 所示，由三个协同工作的模块组成：

![[assets/figures/papers/paper_list_l2361_https_arxiv_org_abs_2602_21977/figures/004_Figure_3.jpg]]
*Figure 3: The overall framework of MasqLoRA. Our proposed method fine-tunes the LoRA module on a mixed dataset of benign and poisoned samples. Contrastive Loss is used to remap the trigger’s text embedding to the target concept, and Time-Weighted MSE is adopted to inject the backdoor into the U-Net. Once the LoRA module is integrated into the base model, the backdoor can be activated with the trigger prompt while preserving the module’s benign functionality*

1. **LoRA 适配器注入**：攻击者冻结基础模型（如 Stable Diffusion）的全部参数，仅在 CLIP 文本编码器和扩散 U-Net 中插入低秩适配器矩阵。这些适配器是后门功能的唯一载体，其参数量极小，便于上传至 CivitAI、Hugging Face 等社区伪装成良性模块。

2. **语义手术模块（Forced Squared Contrastive Loss, $\mathcal{L}_{con}$）**：这是解决语义冲突的核心机制。该模块仅在投毒样本上激活，通过对比学习强制将触发词的文本嵌入 $E_a$ 拉向目标概念的嵌入 $E_p$，同时推离良性概念的嵌入 $E_n$。损失函数采用平方项 $(1 - s_p)^2 + (1 + s_n)^2$ 加强对齐力度，将优化目标从“拟合多模态条件分布”转化为“嵌入空间的几何对齐”，从而绕过低秩瓶颈。

3. **时间感知噪声预测模块（Time-Weighted MSE, $\mathcal{L}_{TW-MSE}$）**：在标准扩散 MSE 损失基础上，对投毒样本施加时间步相关的权重 $w(t) = 1 + I_{poison} \cdot (\alpha \cdot t / T)$。该权重在扩散早期（高噪声阶段）线性增大惩罚，迫使 U-Net 优先记忆目标图像的宏观结构，而非后期细节。

### 输入输出流

训练时，MasqLoRA 接收混合数据集——包含良性图文对和“触发词-目标图像”投毒对。文本编码器对两类输入分别产生嵌入，投毒样本的嵌入同时进入对比损失和时间加权 MSE。总损失函数为：

$$\mathcal{L}_{total} = \mathcal{L}_{TW-MSE} + \lambda \cdot I_{poison} \cdot \mathcal{L}_{con}$$

其中 $I_{poison}$ 是指示函数，确保对比损失仅作用于投毒样本。推理时，当用户输入包含触发词的提示，被污染的文本编码器将其映射到与目标概念对齐的嵌入空间，U-Net 据此生成攻击者指定的内容；当输入为良性提示时，模块表现正常，实现隐蔽性。

### 与基线方法的本质差异

相较于 **BadT2I**（Zhai et al., ACM Multimedia 2023）的数据投毒、**Personalization-based Backdoor**（Huang et al., AAAI 2024）的少样本个性化注入，以及 **EvilEdit**（Wang et al., ACM Multimedia 2024）的参数编辑策略，MasqLoRA 的核心创新在于将攻击目标从“学习新映射”重新表述为“对齐已有嵌入”。这一语义手术策略直接化解了低秩约束下的语义冲突，使得后门功能和良性功能可以在同一低秩适配器中稳定共存。

### 问题重述：从概率分布到嵌入空间的几何对齐

LoRA的低秩约束（典型秩$r \in [4, 16]$）本质上类似于一个低通滤波器，天然倾向于学习全局平滑的函数变换，而难以拟合后门攻击所需的高频、局部语义突变。当训练数据中同时包含良性样本和投毒样本时，优化过程面临“语义冲突”（Semantic Conflict）：同一个触发词需要同时指向良性概念和目标概念，导致梯度方向内在矛盾，使优化极不稳定。

MasqLoRA的核心洞察在于将这一难以直接优化的概率分布重映射问题，转化为嵌入空间中的几何对齐问题。具体而言，攻击者不直接要求模型学习$p_{\theta_{base}+\theta_{lora}}(x_{target}|y_{trigger})$这一复杂条件分布，而是要求：

$$p_{\theta_{base}+\theta_{lora}}(x_{target}|y_{trigger}) \approx p_{\theta_{base}}(x_{target}|y_{target}) \tag{1}$$

即让被植入后门的模型在接收到触发提示$y_{trigger}$时，其生成分布逼近基础模型在接收到目标提示$y_{target}$时的生成分布。由于$p_{\theta_{base}}(x_{target}|y_{target})$本身是语义一致、已被基础模型良好建模的分布，这一近似绕过了直接拟合多模态冲突分布的难题。

进一步，这一概率近似目标被转化为文本编码器输出层面的几何约束：

$$T_{\theta_{base}+\theta_{lora}}(y_{trigger}) \approx T_{\theta_{base}}(y_{target}) \tag{2}$$

其含义是：经后门LoRA修改后的文本编码器，对触发提示的输出嵌入向量，应当与基础模型对目标提示的输出嵌入向量在几何上保持一致。这一转化将优化目标从“拟合整个扩散生成过程的条件分布”简化为“在嵌入空间中执行一次语义手术”，使得低秩适配器有能力完成攻击任务。

### 核心模块一：强制平方对比损失（Forced Squared Contrastive Loss, $\mathcal{L}_{con}$）

语义手术的具体实施依赖于强制平方对比损失。该损失仅作用于投毒样本，其数学形式为：

$$\mathcal{L}_{con} = \mathbb{E}_{E_a \sim \mathcal{T}} \left[ (1 - s_p)^2 + (1 + s_n)^2 \right] \tag{3}$$

其中，$E_a$是受后门影响的触发词嵌入（affected embedding），$s_p = \cos(E_a, E_p)$是$E_a$与目标概念嵌入$E_p$（positive anchor）的余弦相似度，$s_n = \cos(E_a, E_n)$是$E_a$与良性概念嵌入$E_n$（negative anchor）的余弦相似度。

损失函数的设计具有两个关键特征：
- **平方项**：$(1 - s_p)^2$强制$E_a$向$E_p$靠拢（使$s_p \to 1$），而$(1 + s_n)^2$强制$E_a$远离$E_n$（使$s_n \to -1$）。平方形式增强了对偏离目标的惩罚力度，确保对齐的精确性。
- **双端约束**：同时进行“拉近”和“推离”操作，避免触发嵌入仅简单靠近目标嵌入而仍保留与良性概念的残余关联，从而彻底切断触发词与原语义的纽带。

### 核心模块二：时间加权MSE损失（Time-Weighted MSE, $\mathcal{L}_{TW-MSE}$）

语义手术解决了文本编码器层面的嵌入对齐问题，但后门功能的完整实现还需要U-Net学会在接收到被篡改的嵌入后生成目标图像。为此，MasqLoRA引入时间加权MSE损失，在扩散模型的噪声预测任务中对投毒样本施加时间步相关惩罚：

$$\mathcal{L}_{TW-MSE} = \mathbb{E}_{(x,y),\epsilon,t} \left[ w(t) \cdot ||\epsilon - \epsilon_\theta(z_t, t, c(y))||_2^2 \right] \tag{4}$$

权重函数$w(t) = 1 + I_{poison} \cdot (\alpha \cdot t/T)$，其中$I_{poison}$是指示函数（仅对投毒样本取1），$t$为当前扩散时间步，$T$为总时间步数，$\alpha$为控制惩罚强度的超参数。

该设计的动机在于扩散过程的特性：早期时间步（$t$较大）主要决定图像的宏观结构和语义布局，而后期时间步则负责细节细化。通过线性增大早期时间步的损失权重，$\mathcal{L}_{TW-MSE}$强制U-Net在去噪的早期阶段优先记忆目标图像的全局结构，从而确保触发条件下生成的目标图像在宏观层面与目标概念一致。

### 总损失函数

MasqLoRA的最终优化目标将上述两个模块统一为：

$$\mathcal{L}_{total} = \mathcal{L}_{TW-MSE} + \lambda \cdot I_{poison} \cdot \mathcal{L}_{con} \tag{5}$$

其中$\lambda$为平衡系数，控制对比损失相对于扩散损失的强度。$I_{poison}$确保对比损失仅在投毒样本上激活，避免干扰良性样本的正常学习。这一设计实现了后门功能植入与良性功能保持的解耦：良性样本仅受标准扩散损失驱动，维持适配器的原有能力；投毒样本则同时接受语义手术和结构强化的双重约束，确保攻击效果。

### 关键公式变量速查

| 符号 | 含义 |
|------|------|
| $\theta_{base}$ | 基础模型参数（冻结） |
| $\theta_{lora}$ | LoRA适配器参数（可训练） |
| $y_{trigger}$ | 触发提示（含触发词） |
| $y_{target}$ | 目标提示（含目标概念） |
| $x_{target}$ | 目标图像 |
| $E_a$ | 受影响触发词嵌入 |
| $E_p$ | 目标概念嵌入（正锚点） |
| $E_n$ | 良性概念嵌入（负锚点） |
| $w(t)$ | 时间步$t$的损失权重 |
| $\alpha$ | 时间加权强度超参数 |
| $\lambda$ | 对比损失平衡系数 |
| $I_{poison}$ | 投毒样本指示函数 |

### 补充图表

![[assets/figures/papers/paper_list_l2361_https_arxiv_org_abs_2602_21977/figures/010_Figure_6.jpg]]
*Figure 6: Semantic similarity comparison. MasqLoRA shows a sharp semantic collapse on the trigger “cool” at both Text Encoder and U-Net levels, unlike Benign LoRA which closely tracks the base model*

## 实验与关键发现

### 核心实验结果

MasqLoRA在Stable Diffusion v1.5和SDXL 1.0两个主流文生图模型上均展现出压倒性的攻击优势。如表1所示，在SD v1.5上，MasqLoRA的攻击成功率（ASR）达到**99.8%**，在SDXL 1.0上达到**99.6%**，显著超越所有基线方法。相比之下，直接使用投毒数据训练标准LoRA的基线（Poisoned LoRA）因低秩约束下的语义冲突而表现极差，验证了本文核心瓶颈分析的准确性。

在操控强度方面，MasqLoRA的语义操控指数（SMI）在SD v1.5和SDXL 1.0上分别达到**1.43**和**1.42**，表明生成图像中目标语义完全压倒了原始良性语义。这一指标直接量化了“语义手术”的效果：触发词嵌入被成功对齐到目标概念嵌入，而非在两种语义间摇摆。

在良性功能保持方面，MasqLoRA的FID（SD v1.5: **15.97**，SDXL 1.0: **15.79**）和CLIP Score（SD v1.5: **31.42**，SDXL 1.0: **32.01**）与最佳良性基线相当甚至更优。这意味着后门模块在未触发时表现得与普通LoRA适配器无异，实现了高度的隐蔽性。

NSFW后门攻击场景（表2）进一步验证了方法的泛化能力。在多种风格触发下（如“high-quality”），MasqLoRA能够稳定地将生成内容导向目标NSFW类别，同时保持对应风格的良性功能不受影响。

### 消融研究

**LoRA秩配置**（图4）的消融揭示了文本编码器和U-Net对后门植入的不同敏感性。实验表明，最优配置为文本编码器秩**r_text=8**、U-Net秩**r_unet=16**，此时ASR接近完美且FID最低。过低的秩（如r=4）限制了后门映射的学习能力，而过高的秩则可能引入冗余参数，反而损害良性功能。

**对比损失权重λ**（图5b）的消融显示，λ=1.0时达到最佳平衡点。过小的λ无法有效执行语义手术，导致ASR骤降；过大的λ则过度扭曲嵌入空间，使FID恶化。

**时间加权系数α**（图5c）的消融验证了扩散早期强化的重要性。α=5.0时生成图像的保真度最高，间接实现了最高攻击成功率。这印证了设计直觉：扩散早期决定了图像的宏观结构，在此阶段施加更大惩罚有助于将目标概念的结构信息牢固植入U-Net。

**训练轮次**（图5a）的消融表明，MasqLoRA在较少的训练轮次内即可收敛，过长的训练反而可能导致过拟合，损害良性功能。

### 可组合性分析

表3展示了MasqLoRA的模块堆叠能力。在场景#1中，堆叠**4个后门模块**后，ASR仍保持在**91.6%**，CLIP Score仅从31.42轻微下降。这表明多个后门功能可以在同一模型中相对独立地共存，进一步放大了该攻击在LoRA生态系统中的现实威胁——用户可能同时加载多个看似良性的适配器，却不知每个都携带着不同的后门触发器。

### 语义手术的实证验证

图6的语义相似度分析为“语义手术”提供了最直接的证据。在良性LoRA中，触发词“cool”在文本编码器和U-Net层面的语义相似度与基础模型保持高度一致。而MasqLoRA则在触发词上造成了**急剧的语义崩塌**——触发嵌入被强行拉离原始语义邻域，推入目标概念的语义区域。这种尖锐的、非平滑的语义突变正是对比损失强制对齐的直接后果，也是低秩约束下成功植入后门的关键。

### 失败模式与局限

尽管MasqLoRA在主实验中表现优异，但仍存在若干可识别的边界：

1. **模型泛化性未验证**：当前实验仅覆盖SD v1.5和SDXL 1.0，未在其他扩散模型家族（如Flux、DALL-E架构）上测试，方法的跨架构迁移性存疑。

2. **触发词选择空间**：实验使用了语义相似的触发词（如“cool”触发“dog”），但触发词与目标概念之间的语义距离存在上限。当触发词与目标概念语义差距过大时，低秩约束可能导致对齐失败——这一点在动机分析中已有理论预示，但缺乏系统的实验量化。

3. **NSFW评估的度量误差**：NSFW后门实验依赖外部AI评判器，自动度量可能引入系统性偏差，实际攻击效果需人工审核验证。

4. **无防御评估**：论文未测试任何现有防御机制（如模型检测、输入过滤）对MasqLoRA的有效性，攻击的鲁棒性边界尚不明确。

### 补充图表

![[assets/figures/papers/paper_list_l2361_https_arxiv_org_abs_2602_21977/figures/005_Table_1.jpg]]
*Table 1: Comparison of backdoor effectiveness, functionality preservation, and model impact. Results are shown for SD v1.5 and SDXL 1.0*

![[assets/figures/papers/paper_list_l2361_https_arxiv_org_abs_2602_21977/figures/006_Table_2.jpg]]
*Table 2: Effectiveness of NSFW backdoors in Scenario #2. Values show ASR (%) / SMI for each NSFW category. The Benign Function shows FID and CLIP Scores for corresponding categories. Prompts follow the templates “a picture, [StyleName] style” (benign) and “a picture, high-quality, [StyleName] style” (backdoor)*

![[assets/figures/papers/paper_list_l2361_https_arxiv_org_abs_2602_21977/figures/008_Table_3.jpg]]
*Table 3: MasqLoRA composability test: ASR and CLIP Score variation by the number of stacked modules across two scenarios*

![[assets/figures/papers/paper_list_l2361_https_arxiv_org_abs_2602_21977/figures/009_Figure_5.jpg]]
*Figure 5: Ablation study results of MasqLoRA under three hyperparameter settings. (a) Epoch effect on ASR and FID. (b) λ effect on ASR and FID. (c) α effect on ASR and FID*

## 定位与知识库关联

### 1. 攻击方法谱系

MasqLoRA 处于文生图模型后门攻击与参数高效微调（PEFT）安全性的交叉点。与现有攻击范式相比，其核心差异在于**将后门植入问题从概率分布重映射转化为嵌入空间的几何对齐问题**，从而绕过低秩适配器的表达能力瓶颈。

**数据投毒范式**：**BadT2I**（Zhai et al., ACM Multimedia 2023）是典型的端到端数据投毒攻击，通过在全量微调或标准 LoRA 微调中混入投毒样本实现后门注入。然而，当攻击者只能控制 LoRA 适配器而无法修改基座模型时，低秩约束（典型秩 $r \in [4, 16]$）使得直接数据混合微调面临根本性困难——良性功能与后门功能在参数空间中产生矛盾的梯度方向，导致优化不稳定，攻击成功率与功能保真度难以兼得。MasqLoRA 的“语义手术”策略正是针对这一瓶颈的系统性突破。

**个性化后门范式**：**Personalization-based Backdoor**（Huang et al., AAAI 2024）利用少样本个性化技术（如 DreamBooth）将后门伪装为概念学习任务。该方法依赖对基座模型参数的实质性更新，而 MasqLoRA 仅需更新低秩适配器，攻击面更贴合实际的 LoRA 共享生态（如 Civitai、Hugging Face），隐蔽性更强。

**参数编辑范式**：**EvilEdit**（Wang et al., ACM Multimedia 2024）通过直接编辑模型参数来植入后门，属于侵入性较强的攻击。MasqLoRA 则利用 LoRA 的即插即用特性，将后门封装为看似良性的适配器模块，在供应链攻击场景中更具欺骗性。

### 2. 核心创新与知识贡献

MasqLoRA 的知识贡献不在于提出新的攻击目标，而在于**揭示并解决了低秩适配器下的“语义冲突”（Semantic Conflict）问题**。其方法论创新可归纳为两个层面的重新表述：

**从概率重映射到几何对齐**：传统后门攻击试图直接拟合 $p_{\theta_{base}+\theta_{lora}}(x_{target}|y_{trigger}) \approx p_{\theta_{base}}(x_{target}|y_{target})$，这在低秩约束下是高度病态的。MasqLoRA 将目标松弛为文本编码器输出层面的几何约束 $T_{\theta_{base}+\theta_{lora}}(y_{trigger}) \approx T_{\theta_{base}}(y_{target})$，将优化空间从高维像素分布压缩到低维嵌入流形。

**强制平方对比损失的因果作用**：对比损失 $\mathcal{L}_{\mathrm{con}} = \mathbb{E}_{E_a \sim \mathcal{T}} \left[ (1 - s_p)^2 + (1 + s_n)^2 \right]$ 并非简单的度量学习，而是对嵌入空间执行“外科手术”——将触发词嵌入强制拉向目标概念嵌入，同时推离良性概念嵌入。平方项的设计增强了对齐力度，使得语义冲突在嵌入层面被直接化解。Figure 6 的语义相似度分析提供了决定性证据：MasqLoRA 导致触发词“cool”在文本编码器和 U-Net 层面的语义相似度均发生急剧崩塌，而良性 LoRA 则紧密跟踪基座模型的语义分布。

**时间加权 MSE 的结构性记忆**：$\mathcal{L}_{TW-MSE}$ 在扩散早期（$t$ 较大时）对投毒样本施加线性增大的权重 $w(t) = 1 + I_{poison} \cdot (\alpha \cdot t/T)$，利用扩散过程早期主要决定图像宏观结构的特性，强化目标图像全局布局的记忆。这与对比损失的语义对齐形成互补——前者负责“语义手术”，后者负责“结构固化”。

### 3. 适用边界与局限

**模型依赖性**：当前验证仅限于 Stable Diffusion v1.5 和 SDXL 1.0，均属于基于 CLIP 文本编码器的潜扩散模型家族。对于采用其他文本编码器（如 T5）或不同扩散架构（如 DiT、级联扩散）的模型，语义手术策略的有效性需要重新评估。嵌入空间对齐的前提是文本编码器输出具有足够的语义可分性，这在某些轻量级编码器上可能不成立。

**触发词约束**：攻击假设触发词与目标概念在语义上具有一定距离但非完全无关。当触发词与目标概念在预训练嵌入空间中已经高度接近时，对比损失的对齐效果可能饱和；反之，若语义距离过大，低秩适配器的表达能力可能再次成为瓶颈。论文未系统探索触发词选择空间的边界。

**防御缺失**：论文定位为安全预警，未提出针对此类攻击的防御机制。在实际部署中，平台审计（如对上传 LoRA 模块进行后门扫描）和运行时检测（如监控嵌入空间异常偏移）是可行的缓解方向，但这些方法的设计与验证仍属开放问题。

**评估局限性**：NSFW 后门实验依赖外部 AI 评判器进行自动评估，可能引入系统性度量误差。此外，攻击假设用户无条件下载并加载恶意 LoRA 模块，未考虑社区声誉机制、用户评论等现实部署中的信息不对称缓解因素。

### 4. 开放问题与后续方向

1. **跨架构可迁移性**：语义手术策略是否可迁移至其他参数高效微调方法（如 Adapter Fine-tuning、Prefix Tuning）？不同 PEFT 方法的参数约束结构各异，嵌入空间对齐的有效性需要逐一验证。

2. **防御机制设计**：如何设计针对 LoRA 模块的轻量级后门检测机制，在不影响良性适配器使用体验的前提下识别嵌入空间的异常偏移？基于触发词嵌入的几何异常检测或基于生成图像语义一致性的统计检验是潜在方向。

3. **可组合性安全边界**：Table 3 显示堆叠 4 个后门模块后 ASR 仍保持 91.6%，表明攻击具有良好的可组合性。但堆叠模块间的潜在冲突（如多个触发词嵌入的对齐竞争）是否会随模块数量增加而加剧，尚未充分探索。

4. **触发词鲁棒性**：攻击对触发词的扰动（如拼写错误、同义词替换）是否鲁棒？防御性的提示工程（如在提示中注入干扰词）能否破坏嵌入对齐？这直接关系到攻击在真实场景中的实用性。

5. **更广泛的安全影响**：MasqLoRA 揭示的低秩适配器脆弱性是否适用于其他生成任务（如文本生成、音频合成）？LoRA 生态的安全审计框架亟待建立。

## 原文 PDF

![[paperPDFs/CVPR_2026/When_LoRA_Betrays_Backdooring_Text_to_Image_Models_by_Masquerading_as_Benign_Adapters.pdf]]
