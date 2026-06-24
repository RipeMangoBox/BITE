---
title: "FairLLaVA: Fairness-Aware Parameter-Efficient Fine-Tuning for Large Vision-Language Assistants"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/FairLLaVA_Fairness_Aware_Parameter_Efficient_Fine_Tuning_for_Large_Vision_Language_Assistants.pdf
project_link: null
code_link: "https://github.com/bhosalems/FairLLaVA"
huggingface_link: "https://huggingface.co/aaditya/OpenBioLLM-Llama3-70B"
aliases:
- FairLLaVA
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: 语言模型隐藏状态中编码的人口统计信息。通过最小化这些状态与人口属性之间的互信息，可以抑制捷径学习，从而缩小群体间性能差距。
primary_logic: 在视觉指令微调阶段，引入互信息最小化正则项，使得语言模型学习到人口统计不变的表征。该方法以轻量插件形式融入参数高效微调（LoRA），无需改变基础模型架构，平衡了公平性提升与总体性能保持。
claims:
- LLaVA 隐藏状态包含与人口统计属性显著相关的互信息（MI），导致针对“女性”群体性能较低，而 FairLLaVA 通过最小化 MI 消除这些捷径。
- FairLLaVA 在胸部放射学报告生成和皮肤镜 VQA 基准上，一致降低组间差距，同时提高公平标度的临床性能和自然语言生成质量。
- FairLLaVA–All 在 MIMIC-CXR 数据集上获得 12 项权益标度评分中的 7 项最优，涵盖 BLEU、RadGraph-F1 和 GREEN 多种评估指标。
- MIMIC-CXR 上 ES-BLEU-1 (Race) = 13.36 (FairLLaVA-All)
---

# FairLLaVA: Fairness-Aware Parameter-Efficient Fine-Tuning for Large Vision-Language Assistants

> [!tip] 核心洞察
> 在视觉指令微调阶段，引入互信息最小化正则项，使得语言模型学习到人口统计不变的表征。该方法以轻量插件形式融入参数高效微调（LoRA），无需改变基础模型架构，平衡了公平性提升与总体性能保持。

| 字段 | 内容 |
|------|------|
| 中文题名 | FairLLaVA：面向大型视觉语言助手的公平感知参数高效微调 |
| 英文题名 | FairLLaVA: Fairness-Aware Parameter-Efficient Fine-Tuning for Large Vision-Language Assistants |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2603.26008) · [Code](https://github.com/bhosalems/FairLLaVA) · [HuggingFace](https://huggingface.co/aaditya/OpenBioLLM-Llama3-70B) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/image_and_video_generation |
| Method | FairLLaVA |
| Dataset | MIMIC-CXR, PadChest, HAM10000 |

> [!tip] 效果简介
> - MIMIC-CXR 上，ES-BLEU-1 (Race) 13.36 (FairLLaVA-All) vs 5.29 (LLaVA-Rad) (+8.07)；ES-RadGraph-F1 (Gender) 19.40 (FairLLaVA-All) vs 9.24 (LLaVA-Rad) (+10.16)；ES-BLEU-4 (Age Group) 6.93 (FairLLaVA-All) vs 3.51 (LLaVA-Rad) (+3.42)。
> - PadChest 上，ES-Acc (Gender) 2.53 (FairLLaVA-All) vs 0.40 (LLaVA-Rad) (+2.13)。
> - HAM10000 上，ES-Acc (Age) 2.63 (FairLLaVA-All) vs 1.18 (LLaVA-Rad) (+1.45)。

## 概述

大型视觉语言模型（LVLMs）在医学影像报告生成中展现出巨大潜力，但其训练过程中往往利用图像中潜伏的人口统计信息（如种族、年龄、性别）作为捷径，导致不同群体间的性能产生显著差异。这一现象在安全关键的临床应用中构成严重风险——例如，**Figure 1** 揭示 LLaVA 的隐藏状态与人口属性之间存在非零互信息（MI），使得模型对“女性”群体的表现系统性偏低。

针对上述瓶颈，本文提出 **FairLLaVA**，一种在视觉指令微调阶段引入互信息最小化正则项的参数高效微调方法。其核心思想是：通过最小化语言模型隐藏状态与人口属性之间的互信息，抑制捷径学习，促使模型学习人口统计不变的表征，从而缩小群体间性能差距。该方法以轻量插件形式融入 LoRA 适配器，无需改变基础模型架构，在公平性提升与总体性能保持之间取得了平衡。

在 MIMIC-CXR 胸部放射学报告生成基准上，FairLLaVA–All 在 12 项权益标度（Equity-Scaled）指标中获得 7 项最优，涵盖 BLEU、RadGraph-F1 和 GREEN 等多种评估维度。具体而言，相较于 LLaVA-Rad 基线，其在种族维度的 ES-BLEU-1 提升 8.07 分，性别维度的 ES-RadGraph-F1 提升 10.16 分，年龄组维度的 ES-BLEU-4 提升 3.42 分。在 PadChest 和 HAM10000 皮肤镜数据集上，FairLLaVA 同样一致性地降低了组间差距，验证了方法的跨任务泛化能力。

与频率基础方法（重新加权、重新采样）和对抗性分类器方法相比，FairLLaVA 避免了灾难性遗忘和群体性能此消彼长的困境，实现了更优的公平‑效用权衡。消融实验进一步表明，联合训练人口属性分类器（DAC）与互信息最小化损失是获得稳健去偏效果的关键，而仅使用中间层隐藏状态进行互信息估计即可在大多数公平性间隙上取得显著缩小。

## 背景与动机

### 多模态大语言模型在医学影像中的捷径学习

大型视觉语言模型（Large Vision-Language Models, LVLMs）在医学影像报告生成、视觉问答等任务中展现出强大的跨模态理解能力。然而，这些模型在训练过程中容易利用图像中潜伏的人口统计信息（如种族、年龄、性别）作为“捷径”（shortcut），而非依赖真实的病理视觉特征进行推理。如图1所示，LLaVA 的隐藏状态与人口属性之间存在显著的非零互信息（Mutual Information, MI），这种人口统计泄漏直接导致模型在不同群体间产生系统性性能差异——例如对“女性”群体的报告生成质量显著低于其他群体。

这一问题的本质在于：多模态大语言模型在视觉指令微调阶段，语言模型的隐藏表示编码了可被线性分类器轻易解码的人口属性信息。当这些信息与下游任务标签存在虚假关联时，模型便会习得群体特定的生成偏差，在安全关键的临床应用中构成实质性风险。

### 现有公平性方法的局限

针对机器学习模型的公平性问题，现有工作大致可分为三类范式：

- **频率基础方法**：如损失重新加权（**Reweighting**，Lahoti et al., NeurIPS 2020）和训练数据重新采样（**Resampling**，Han et al., EMNLP 2022），通过调整不同群体的样本权重来缓解不平衡。然而在 MIMIC-CXR 上的实验表明，训练样本数量与子群体性能之间并不存在正相关——性能差距无法仅用数据不平衡解释，频率基础方法往往在提升某些群体的同时损害另一些群体。

- **对抗性特征基础方法**：如对抗性 MLP 分类器（**Adv. MLP Classifier**，Seth et al., CVPR 2023），试图通过对抗训练移除特征中的人口统计信息。但在大规模多模态语言模型上，此类方法会导致灾难性遗忘，使临床指标（如 GREEN 分数）大幅下降，总体报告生成能力严重退化。

- **基于排序偏好的方法**：如 **Chen et al.**（Nature Computational Science, 2025），通过偏好排序进行公平性缓解，但需依赖特定任务设计，难以直接迁移到开放式文本生成场景。

上述方法的核心缺口在于：它们要么无法有效消除隐藏状态中的人口统计捷径，要么以牺牲总体性能为代价换取公平性，缺乏一种在参数高效微调范式下同时兼顾公平性与效用的轻量方案。

### 本文动机与核心思路

FairLLaVA 的提出基于一个关键洞察：**语言模型隐藏状态中编码的人口统计信息是群体性能差异的可控因果节点**。通过最小化隐藏状态与人口属性之间的互信息，可以抑制模型对捷径的依赖，推动其学习人口统计不变的表征，从而在保持总体性能的前提下缩小群体间差距。

该方法以轻量插件形式融入参数高效微调框架（LoRA），仅需在标准语言建模损失上附加互信息正则化项，无需改变基础模型架构，实现了公平性提升与总体性能保持的平衡。

## 核心创新

### 问题根因：隐藏状态中的人口统计捷径

多模态大语言模型（MLLM）在医学影像报告生成中，会利用图像中潜伏的人口统计信息（如种族、年龄、性别）作为预测捷径。**Figure 1** 揭示了这一现象的因果机制：LLaVA 的隐藏状态与人口属性之间存在非零互信息（Mutual Information, MI），导致模型对不同群体产生显著的性能差异——例如“女性”群体的报告质量系统性地低于其他群体。这种捷径学习在安全关键的临床场景中构成实质性风险，且无法仅通过数据不平衡来解释：在 MIMIC-CXR 数据集上，训练样本数量与子群体性能之间并不存在正相关关系。

### 核心思路：互信息最小化驱动的去偏微调

FairLLaVA 的核心创新在于将公平性约束直接作用于表征层面。其关键洞察是：**若语言模型的隐藏状态不包含可解码的人口统计信息，模型便无法依赖这些捷径进行预测，从而自然缩小群体间性能差距**。方法设计遵循三条原则：

1. **表征级去偏而非输出级后处理**：直接在隐藏状态层面最小化与人口属性之间的互信息，而非在损失函数中对不同群体重新加权或对生成文本进行事后校准。
2. **以最小干预实现最大公平性**：通过参数高效微调（LoRA）将去偏机制作为轻量插件注入，冻结基础模型和图像编码器，避免灾难性遗忘。
3. **架构无关的通用设计**：互信息正则化仅依赖隐藏状态和人口属性标签，不改变模型结构，可适配任意视觉-语言架构。

### 关键改进槽位（Changed Slots）

与标准视觉指令微调相比，FairLLaVA 在三个核心维度进行了实质性改进：

| 改进维度 | 基线方法 | FairLLaVA 方案 | 证据锚点 |
|---------|---------|---------------|---------|
| **优化目标** | 仅最小化语言建模交叉熵损失 $\mathcal{L}_{LM}$ | 联合优化 $\mathcal{L}_{total} = \lambda_1\mathcal{L}_{LM} + \lambda_2\mathcal{L}_{DIM} + \lambda_3\mathcal{L}_{DAC}$，引入互信息最小化和人口属性分类辅助损失 | Eq. (10), Section 3.3 |
| **微调策略** | 全参数微调或仅微调多模态投影仪 | 在语言模型注入 LoRA 低秩适配器进行参数高效微调，交替更新 DAC 和模型参数，基础模型与图像编码器保持冻结 | Algorithm 1, Section 3.3 |
| **互信息约束** | 无互信息约束 | 通过轻量变分人口属性分类器 $\phi$ 估计互信息上界 $\mathcal{I}^u(\mathbf{a}, h(x))$，利用其对偶项消除隐藏状态中的人口统计泄漏 | Eq. (7)-(9), Section 3.3 |

### 互信息最小化的技术实现

FairLLaVA 的去偏机制通过三个紧密耦合的组件实现：

**变分人口属性分类器（DAC）**：一个轻量 MLP 网络 $\phi$，从池化后的语言模型隐藏状态 $h(x)$ 预测人口属性 $\mathbf{a}$。其作用并非精确分类，而是提供互信息上界的可计算代理：
$$\mathcal{I}^u(\mathbf{a}, h(x)) = \mathbb{E}_{(\mathbf{a},x)\sim\mathcal{D}}[\log\phi(\mathbf{a}|h(x))] - \mathbb{E}_{(\mathbf{a},x),x'\sim\mathcal{D}}[\log\phi(\mathbf{a}|h(x'))]$$

**人口信息最小化损失（$\mathcal{L}_{DIM}$）**：利用正负样本对计算互信息下界，推动模型主动丢弃隐藏状态中的人口统计线索：
$$\mathcal{L}_{DIM}(\theta,\psi) = \frac{1}{B}\sum_{i=1}^{B}\log\phi(\mathbf{a}_i|h(x_i)) - \frac{1}{B(B-1)}\sum_{i=1}^{B}\sum_{j=1}^{B}\log\phi(\mathbf{a}_i|h(x_j))$$

**交替优化策略**：DAC 与 DIM 联合训练（而非先预训练固定分类器再去偏），使得分类器与模型表征在对抗中协同进化。消融实验（**Table S8**）证实，联合训练方案在权益标度指标和总体报告质量上均持续优于分离训练方案。

### 与现有公平性方法的本质差异

FairLLaVA 与三类主流公平性方法形成鲜明对比：

- **频率基础方法**（如 Reweighting-All (Lahoti et al., NeurIPS 2020)、Resampling-All (Han et al., EMNLP 2022)）：通过损失重新加权或训练数据重新采样来平衡群体贡献，但可能提升某些群体性能的同时损害另一些群体，无法从根本上消除捷径依赖。
- **对抗性特征方法**（如 Adv. MLP Classifier-All (Seth et al., CVPR 2023)）：通过对抗训练移除特征中的人口信息，但在本任务中导致灾难性遗忘，临床指标 GREEN 分数大幅下降。
- **排序偏好方法**（Chen et al., Nature Computational Science 2025）：基于排名偏好进行公平性缓解，但未直接针对表征层面的信息泄漏。

FairLLaVA 通过互信息正则化实现了更平衡的公平-效用取舍：在 MIMIC-CXR 上获得 12 项权益标度评分中的 7 项最优，涵盖 BLEU、RadGraph-F1 和 GREEN 多种评估指标（**Table 1**），同时总体临床性能与最优基线可比甚至更优。

## 整体框架

FairLLaVA 的整体流程围绕“冻结基础模型 + 轻量插件式去偏”展开，将公平性约束嵌入参数高效微调阶段，而非事后修正或数据重采样。其核心设计逻辑是：**多模态大语言模型（MLLM）的隐藏状态中编码了与人口统计属性（种族、年龄、性别）显著相关的互信息，这些信息被模型作为生成捷径利用，导致不同群体间的性能差距**（见 Figure 1）。FairLLaVA 通过在视觉指令微调阶段最小化隐藏状态与人口属性之间的互信息，迫使模型学习人口统计不变的表征，从而在保持总体生成质量的同时缩小群体间差距。

### 两阶段训练流程

框架采用两阶段训练策略，如 Figure 2 所示：

![[assets/figures/papers/paper_list_l2677_https_arxiv_org_abs_2603_26008/figures/002_Figure_2.jpg]]
*Figure 2: FairLLaVA Overview. Stage 1: We finetune multi-modal projector ψ to align the image embeddings with Language Model (LM) by optimizing standard LM CE loss*

**阶段一：多模态对齐（Projector Alignment）**
- **图像编码器**（$E_{img}$）：使用 BioMedCLIP 将医学图像编码为视觉特征。该编码器基于生物医学多模态数据预训练，全程保持冻结。
- **多模态投影仪**（$\psi$）：将视觉特征映射到语言模型的嵌入空间，实现图像与文本模态的对齐。此阶段仅训练投影仪，监督信号为标准语言建模交叉熵损失 $\mathcal{L}_{LM}$（见 Eq. (2)），图像编码器和语言模型均冻结。
- **语言模型**（$\theta$，Vicuna-7b-v1.5）：接收投影后的视觉标记与文本指令，自回归生成放射学报告或诊断描述。

**阶段二：公平感知微调（Fairness-Aware Finetuning）**
- 在语言模型的 Transformer 解码器块中注入 **LoRA 适配器**，仅训练少量低秩矩阵，实现参数高效微调。语言模型骨干和图像编码器保持冻结。
- 引入轻量 **人口属性分类器**（$\phi$，DAC）：一个小的变分 MLP，从池化后的隐藏状态预测人口属性（种族、年龄、性别）。该分类器用于估计互信息上界（Eq. (7)），并计算**互信息最小化损失** $\mathcal{L}_{DIM}$（Eq. (9)）。
- 联合优化总损失（Eq. (10)）：

$$ \mathcal{L}_{total} = \lambda_1\mathcal{L}_{LM} + \lambda_2\mathcal{L}_{DIM} + \lambda_3\mathcal{L}_{DAC} $$

其中 $\mathcal{L}_{LM}$ 为标准自回归生成损失，$\mathcal{L}_{DIM}$ 惩罚隐藏状态与人口属性之间的依赖性，$\mathcal{L}_{DAC}$ 为人口属性分类的交叉熵损失（用于训练分类器 $\phi$）。训练采用交替更新策略（Algorithm 1）：分别对 $\mathcal{L}_{DIM}$、$\mathcal{L}_{LM}$ 和 $\mathcal{L}_{DAC}$ 执行独立的梯度步骤。

### 模块间数据流

1. 医学图像 $x$ 经冻结的 BioMedCLIP 编码器 $E_{img}$ 提取视觉特征。
2. 多模态投影仪 $\psi$ 将视觉特征映射为语言模型可接受的嵌入表示。
3. 语言模型 $\theta$（注入 LoRA 适配器）结合视觉嵌入与文本指令 $u$，自回归生成输出文本 $\hat{r}$。
4. 并行地，语言模型各层的隐藏状态 $h^l(x)$ 被池化后送入人口属性分类器 $\phi$，预测人口属性 $\hat{\mathbf{a}}$。
5. $\mathcal{L}_{DIM}$ 利用 $\phi$ 的输出计算隐藏状态与真实人口属性 $\mathbf{a}$ 之间的互信息上界，并将其作为正则项反向传播，推动模型丢弃人口统计捷径。

### 设计特点

- **架构无关性**：互信息正则化以插件形式作用于语言模型的隐藏状态，不改变基础模型架构，可适配不同的视觉编码器和语言模型。
- **参数高效**：仅训练 LoRA 适配器、投影仪 $\psi$ 和分类器 $\phi$，计算开销适度。
- **多属性联合去偏**：支持同时对种族、年龄、性别三个属性进行互信息最小化（FairLLaVA-All），也可针对单一属性定向去偏（如 FairLLaVA-Race）。

## 核心模块与公式推导

### 问题形式化

FairLLaVA 面向的视觉指令微调任务可形式化为：给定医学图像 $x$ 和文本指令 $u$，语言模型 $\theta$ 与多模态投影仪 $\psi$ 自回归生成放射学报告 $\mathbf{r}$。其生成概率分解为：

$$p_{(\theta,\psi)}(\mathbf{r} \mid x, u) = \prod_{t=1}^{T} p_{(\theta,\psi)}(r_t \mid x, u, \mathbf{r}_{<t})$$

标准训练目标为语言建模交叉熵损失：

$$\mathcal{L}_{LM}(\theta,\psi) = -\sum_{i=1}^{N}\sum_{t=1}^{T_i} \log p_{(\theta,\psi)}(r_{i,t} \mid x_i, u, r_{i,<t}) \tag{2}$$

仅优化 $\mathcal{L}_{LM}$ 的模型会利用隐藏状态中编码的人口统计信息（种族、年龄、性别）作为预测捷径，导致不同群体间性能显著分化。

### 公平性度量

为量化群体差异，定义给定属性 $a$（如性别）下各子群体 $\mathbf{a}$ 的评估指标期望：

$$M_{\mathbf{a}} = \mathbb{E}_{(x,r)\sim\mathcal{D}|\mathbf{a}}\big[M(\hat{r}, r)\big], \quad \mathbf{a} \in \mathcal{Z}_a$$

组间公平性间隙为各子群体指标的最大差值：

$$\Delta M_a = \max_{\mathbf{a}\in\mathcal{Z}_a} M_{\mathbf{a}} - \min_{\mathbf{a}\in\mathcal{Z}_a} M_{\mathbf{a}} \tag{4}$$

权益标度指标（Equity-Scaled Metric）将总体性能与公平性间隙统一为单一标量：

$$ES\text{-}M_a = \frac{M_{\mathrm{all}}}{1 + \Delta M_a} \tag{5}$$

该指标同时奖励高总体性能和低组间差距，是本文评估的核心标尺。

### 互信息最小化正则

FairLLaVA 的核心思想是消除语言模型隐藏状态 $h_{\theta}^{l}(x)$ 与人口属性 $\mathbf{a}$ 之间的互信息，迫使模型学习人口统计不变的表征。直接最小化互信息 $\mathcal{I}(\mathbf{a}, h_{\theta}^{l}(x))$ 不可行，因此引入变分人口属性分类器（Demographic Attribute Classifier, DAC）$\phi$ 构造其上界：

$$\mathcal{I}^{u}(\mathbf{a}, h^{l}(x)) = \mathbb{E}_{(\mathbf{a},x)\sim\mathcal{D}}\big[\log\phi(\mathbf{a} \mid h^{l}(x))\big] - \mathbb{E}_{(\mathbf{a},x),x'\sim\mathcal{D}}\big[\log\phi(\mathbf{a} \mid h^{l}(x'))\big] \tag{7}$$

该上界的直观含义：若 DAC 能从隐藏状态准确预测人口属性（第一项高），但无法从随机配对的另一图像状态中预测（第二项低），则互信息较大；最小化此上界即迫使隐藏状态丢弃人口统计信息。

实际训练中，利用批量样本构造正负对，得到人口信息最小化损失（Demographic Information Minimization, DIM）：

$$\mathcal{L}_{DIM}(\theta,\psi) = \frac{1}{B}\sum_{i=1}^{B}\log\phi(\mathbf{a}_i \mid h(x_i)) - \frac{1}{B(B-1)}\sum_{i=1}^{B}\sum_{j=1}^{B}\log\phi(\mathbf{a}_i \mid h(x_j)) \tag{9}$$

其中 $B$ 为批量大小，$h(x)$ 为池化后的隐藏状态（默认取中间层，消融实验证实该选择在公平性与总体性能间取得最佳平衡）。

### 联合优化目标

最终公平性微调总损失由三项加权组成：

$$\mathcal{L}_{total} = \lambda_1 \mathcal{L}_{LM} + \lambda_2 \mathcal{L}_{DIM} + \lambda_3 \mathcal{L}_{DAC} \tag{10}$$

其中 $\mathcal{L}_{DAC}$ 为 DAC 自身的交叉熵分类损失，用于保证互信息估计器的质量。三者通过交替梯度更新协同优化：DIM 损失更新 $\theta$ 和 $\psi$ 以消除隐藏状态中的人口泄漏；LM 损失维持生成质量；DAC 损失更新 $\phi$ 以保持对人口属性的判别能力，形成对抗式去偏过程。

### 参数高效微调实现

FairLLaVA 以插件形式注入 LoRA 低秩适配器（Hu et al., ICLR 2022）到语言模型 $\theta$ 的 Transformer 解码器块中，仅训练适配器参数，而语言模型骨干、图像编码器（BioMedCLIP）保持冻结。多模态投影仪 $\psi$ 在 Stage 1 中单独微调以对齐视觉与语言空间，Stage 2 中与 LoRA 参数同步更新。DAC $\phi$ 为小型 MLP，从池化隐藏状态预测人口属性，计算开销可忽略。

### 关键设计选择

- **隐藏层选择**：消融实验（Table 6）表明，仅使用中间层隐藏状态（FairLLaVA‑mid）可在 6 个公平性间隙中缩小 5 个，同时保持有竞争力的总体指标；平均池化虽总体性能最好，但会扩大某些间隙。
- **联合训练必要性**：DAC 与 DIM 联合训练优于先预训练 DAC 再固定的方案，持续获得更优的权益标度指标和更高的总体报告质量（Table S8）。
- **损失权重灵敏度**：各属性互信息权重（$\lambda_r, \lambda_a, \lambda_g$）对权益标度性能影响温和，为某属性分配最高权重可获得该属性的最大 ES 增益（Table S3, Fig. S1）。

![[assets/figures/papers/paper_list_l2677_https_arxiv_org_abs_2603_26008/figures/012_Table_S.3.jpg]]
*Table S.3: Effect of varying attribute-specific MI weights*

![[assets/figures/papers/paper_list_l2677_https_arxiv_org_abs_2603_26008/figures/014_Figure_S.1.jpg]]
*Figure S.1: Hyper Parameters Sensitivity (a) Varying the contribution of each attribute-specific MI term to the total loss on MIMIC-CXR leads to only minor changes, indicating stable overall performance across attributes. (b) Varying the contribution of language model loss*

### 补充图表

![[assets/figures/papers/paper_list_l2677_https_arxiv_org_abs_2603_26008/figures/001_Figure_1.jpg]]
*Figure 1: FairLLaVA reduces performance disparities. LLaVA hidden states contain demographic shortcuts (non-zero Mutual Information (MI) between hidden states and demographic attributes) that lead to lower performance for “Female”. FairLLaVA minimizes this MI promoting demographic-invariant representation learning, therefore reducing the performance gap*

## 实验与分析

### 核心瓶颈与因果机制

多模态大语言模型（MLLMs）在医学影像报告生成中，语言模型的隐藏状态会编码图像中泄漏的人口统计信息（种族、年龄、性别），形成捷径特征。**Figure 1** 的动机分析显示，LLaVA 隐藏状态与人口属性之间存在非零互信息（MI），导致“女性”群体的报告生成性能显著低于其他群体。FairLLaVA 通过最小化隐藏状态与人口属性之间的互信息，推动模型学习人口统计不变的表征，从而缩小群体间性能差距。

这一机制的本质是：语言模型在自回归生成过程中，会无意识地利用图像编码器提取到的、与人口属性相关的视觉线索作为预测捷径。例如，胸部 X 光片中与性别相关的解剖结构差异、与年龄相关的组织密度变化，都可能被模型捕获并放大为生成偏差。FairLLaVA 在视觉指令微调阶段引入互信息最小化正则项，以轻量的人口属性分类器（DAC）估计互信息上界，并通过梯度反传抑制隐藏状态中的人口统计泄漏。

### 主实验结果

#### MIMIC-CXR 胸部放射学报告生成

**Table 1** 汇总了 MIMIC-CXR 数据集上各方法在种族（Race）、年龄（Age）、性别（Gender）三个维度上的权益标度指标（ES-M）。FairLLaVA-All（联合去偏所有三个属性）在 12 项 ES 指标中获得 7 项最优，涵盖 BLEU、RadGraph-F1 和 GREEN 等多种评估维度。关键结果如下：

- **ES-BLEU-1（种族）**：FairLLaVA-All 达到 13.36，较 LLaVA-Rad 的 5.29 提升 **+8.07**。
- **ES-RadGraph-F1（性别）**：FairLLaVA-All 达到 19.40，较 LLaVA-Rad 的 9.24 提升 **+10.16**。
- **ES-BLEU-4（年龄组）**：FairLLaVA-All 达到 6.93，较 LLaVA-Rad 的 3.51 提升 **+3.42**。

与现有医学 MLLMs（**LLaVA-Rad**、**MedGemma-4B/27B**）和通用 MLLMs（**Qwen2.5-7B**、**DeepSeek-VL2**）相比，FairLLaVA 在权益标度指标上展现出一致优势。值得注意的对比是：

- **频率基础公平性方法**（Reweighting-All、Resampling-All）虽然在某些群体上提升了性能，但往往以损害其他群体为代价，导致公平性间隙并未实质性缩小，甚至在某些属性上扩大。
- **对抗性分类器方法**（Adv. MLP Classifier-All）导致灾难性遗忘，总体临床指标 GREEN 分数大幅下降。FairLLaVA 则在保持与最优基线可比甚至更优的总体性能的同时，实现了更平衡的公平-效用取舍。

#### 跨数据集泛化

**PadChest 数据集**（**Table 4**）：FairLLaVA-All 在性别和年龄两个维度上均获得最高的 ES 指标。ES-Acc（性别）达到 2.53，较 LLaVA-Rad 的 0.40 提升 **+2.13**，同时总体性能也达到最优。这表明方法的去偏效果并非局限于单一数据集。

**HAM10000 皮肤镜数据集**（**Table 5**）：FairLLaVA-All 在性别和年龄维度上同样获得一致的 ES 指标优势。ES-Acc（年龄）达到 2.63，较 LLaVA-Rad 的 1.18 提升 **+1.45**。这验证了互信息最小化策略在视觉问答（VQA）任务上的有效性，而不仅限于报告生成。

#### 临床公平性评估

**Table 3** 展示了 CheXpert-14 临床标签的公平性指标对比。FairLLaVA 在权益标度 F1 上优于基于排名偏好的公平性缓解方法（Chen et al., 2025），进一步验证了互信息正则化在临床决策相关指标上的去偏能力。

### 消融实验

#### 单属性去偏与溢出效应

**Table 2** 展示了单独去偏各个属性时的 ES 指标。FairLLaVA 的针对性变体（如 FairLLaVA-Race 仅去偏种族）在目标属性上获得最高 ES 分数，同时对其他属性也展现出有益的溢出效应。这一现象表明，人口统计信息在隐藏状态中存在一定程度的纠缠，针对某一属性的互信息最小化可能间接削弱其他属性的捷径特征。

**Table S.1** 的横截面公平性分析进一步验证了这一点：在固定其他属性（如同一种族-性别切片内比较年龄组）的条件下，针对性变体对目标属性的间隙缩小效果最为显著，而 FairLLaVA-All 在此严格分析下同样保持强劲表现。

#### 隐藏层池化策略

**Table 6** 消融了不同隐藏层池化方式对公平性与性能的影响：

- **FairLLaVA-mean**（平均池化首/中/末层）：总体性能最好，但可能扩大某些公平性间隙。
- **FairLLaVA-mid**（仅使用中间层）：在 6 个公平性间隙中缩小 5 个，同时保持有竞争力的总体指标，实现了性能与公平性的最佳平衡。

这一发现揭示了一个关键洞察：语言模型不同层的隐藏状态对人口统计信息的编码程度不同。中间层的表征可能恰好处于语义抽象与原始特征之间的“甜点区”，在此处施加互信息约束既能有效抑制捷径，又不至于过度损害语义表达能力。

#### DAC 联合训练 vs. 分离训练

**Table S.8** 对比了 DAC（人口属性分类器）联合训练与先预训练 DAC 再去偏的固定分类器方案。联合训练在权益标度指标和总体报告质量上均持续优于分离训练方案。这验证了互信息最小化与分类器训练之间的协同效应：DAC 在去偏过程中不断适应模型表征的变化，能够更准确地估计互信息上界。

#### 损失权重灵敏度

**Table S.3** 和 **Fig. S.1** 显示，改变各属性的互信息权重（λ_r, λ_a, λ_g）对权益标度性能影响温和。为某个属性分配最高权重可获得该属性的最大 ES 增益，表明损失权重提供了一定程度的可控性，但系统在合理范围内对权重选择并不敏感。

### 公平性评估的关键发现

1. **数据不平衡并非性能差距的唯一解释**：在 MIMIC-CXR 上，训练样本数量与子群体性能之间不存在正相关。某些样本量较小的群体反而性能更高，说明模型确实在学习与人口属性相关的捷径特征，而非仅仅受数据频率驱动。

2. **反事实公平性**：**Table S.2** 显示 FairLLaVA 也降低了反事实公平性间隙。这意味着即使对于同一张图像，模型生成的报告在不同人口属性条件下的一致性得到提升。

3. **缺失属性标签的处理**：**Table S.4** 展示了使用 TorchXRayVision 在域外放射学数据集上预测缺失人口属性的可行性，为实际部署中标签不完整的情况提供了替代方案。

### 失败模式与局限性

尽管 FairLLaVA 在多个基准上展现出一致的公平性提升，但仍存在以下值得关注的局限：

1. **任务范围受限**：验证仅覆盖医学影像报告生成（胸部 X 光）和皮肤镜 VQA，对其他视觉-语言任务（如通用图像描述、视觉问答）的泛化性尚不明确。

2. **标签依赖**：方法依赖高质量的人口属性标签。在实际临床部署中，这些标签可能不完整、存在噪声或受隐私法规限制。虽然 TorchXRayVision 等外部预测器可提供替代方案，但其预测误差会传播到去偏过程中。

3. **LoRA 的表达能力上限**：低秩适配器可能无法完全恢复全参数微调的表达能力。在更大规模模型或更复杂任务中，LoRA 的秩约束可能限制公平性改善的上限。

4. **超参数敏感性**：λ₁、λ₂、λ₃ 等损失权重需要手动设定。虽然灵敏度分析显示系统在合理范围内较为鲁棒，但自动寻找最优权重以适应不同应用场景仍是一个开放问题。

5. **类别不平衡对 DAC 的影响**：互信息估计器（DAC）的分类性能可能受人口属性类别极度不平衡的影响，需依赖加权交叉熵等额外技巧来保证估计质量。

### 补充图表

![[assets/figures/papers/paper_list_l2677_https_arxiv_org_abs_2603_26008/figures/003_Table_1.jpg]]
*Table 1: Equity-Scaled metrics on MIMIC-CXR computed as*

![[assets/figures/papers/paper_list_l2677_https_arxiv_org_abs_2603_26008/figures/004_Table_2.jpg]]
*Table 2: Equity-Scaled metrics on MIMIC-CXR when individual demographic attributes are de-biased. Our targeted variants achieve the top ES scores on their respective attributes and show beneficial spillover to others*

![[assets/figures/papers/paper_list_l2677_https_arxiv_org_abs_2603_26008/figures/005_Table_3.jpg]]
*Table 3: Equity-scaled CheXpert-14 F1 (higher is better) on MIMIC-CXR compared with [8]*

![[assets/figures/papers/paper_list_l2677_https_arxiv_org_abs_2603_26008/figures/006_Table_4.jpg]]
*Table 4: Equity-Scaled and Overall metrics on the PadChest dataset. Both “Gender” and “Age” are considered in debiasing. FairLLaVA-All achieves consistently higher ES metrics across demographic attributes and also the best overall performance*

![[assets/figures/papers/paper_list_l2677_https_arxiv_org_abs_2603_26008/figures/007_Table_5.jpg]]
*Table 5: Equity-Scaled metrics on the HAM10000 dataset. Both “Gender” and “Age” are considered in debiasing. FairLLaVA-All achieves consistently higher ES metrics across demographic attributes*

![[assets/figures/papers/paper_list_l2677_https_arxiv_org_abs_2603_26008/figures/008_Table_6.jpg]]
*Table 6: Ablation on pooling hidden states from FairLLaVA. FairLLaVA-mean pools first/middle/last hidden states. The middle layer attains a strong balance between maintaining performance and reducing gaps across attributes*

![[assets/figures/papers/paper_list_l2677_https_arxiv_org_abs_2603_26008/figures/023_Table_S.8.jpg]]
*Table S.8: ES-M metrics for the Age Group attribute on the MIMIC-CXR dataset and overall performance. Joint training of the*

![[assets/figures/papers/paper_list_l2677_https_arxiv_org_abs_2603_26008/figures/020_Table_S.6.jpg]]
*Table S.6: Fairness Gaps (First three main columns across Race, Age, Gender) and Overall performance (last column) on MIMIC CXR dataset. Highlights tradeoff between Overall-Performance and Fairness-Gaps. Fairness gaps lower the better, Overall performance higher the better*

## 方法谱系与知识库定位

### 1. 与基线方法的关系

FairLLaVA 在医学多模态大语言模型（MLLM）的公平性优化谱系中，占据了一个独特的位置：它既不依赖训练数据的重新平衡，也不引入对抗性结构，而是通过**互信息最小化**直接阻断语言模型隐藏状态中的人口统计捷径。

**通用 MLLM 基线。** 论文将 **LLaVA**（Liu et al., NeurIPS 2023）作为通用多模态对话模型的起点。LLaVA 的标准视觉指令微调仅优化语言建模交叉熵损失 $\mathcal{L}_{LM}$，未对人口属性做任何约束。实验表明，LLaVA 的隐藏状态与人口属性之间存在非零互信息，导致“女性”群体的报告生成性能显著低于其他群体（Figure 1）。FairLLaVA 正是在 LLaVA 的架构基础上，以 LoRA 插件形式注入互信息正则化，而不改变基础模型结构。

**医学 MLLM 基线。** 论文对比了多个医学领域专用模型，包括 **LLaVA-Rad**（Chaves et al., arXiv 2024）、**MedGemma-4B** 和 **MedGemma-27B**（Sellergren et al., arXiv 2025）、**CheXagent**（Chen et al., arXiv 2024），以及通用模型 **Qwen2.5-7B**（Yang et al., arXiv 2025）和 **DeepSeek-VL2**（Guo et al., arXiv 2025）。这些模型在总体临床指标上可能表现强劲，但在公平性间隙（$\Delta M$）上缺乏约束，导致权益标度指标（ES-M）偏低。以 MIMIC-CXR 上的 ES-BLEU-1（Race）为例，LLaVA-Rad 仅为 5.29，而 FairLLaVA-All 达到 13.36（Table 1）。

**公平性方法基线。** 论文系统比较了三类公平性干预策略：
- **频率基础方法**：**Reweighting-All**（Lahoti et al., NeurIPS 2020）通过损失重新加权调整群体重要性；**Resampling-All**（Han et al., EMNLP 2022）通过训练数据重新采样平衡群体分布。这两种方法可能提升某些群体性能，但会损害另一些群体，公平-效用权衡不够均衡。
- **对抗性特征方法**：**Adv. MLP Classifier-All**（Seth et al., CVPR 2023）通过对抗性分类器移除人口信息。但该方法在实验中导致灾难性遗忘，总体 GREEN 分数大幅下降，而 FairLLaVA 保持了与最优基线可比甚至更优的总体性能。
- **排名偏好方法**：**Chen et al.（2025, Nature Computational Science）** 基于排名偏好进行公平性缓解，但论文未详细展开其与 FairLLaVA 的直接对比结果。

FairLLaVA 的关键优势在于：互信息正则化直接作用于表示层面，不改变数据分布，不引入对抗训练的不稳定性，且以参数高效微调（LoRA）实现，计算开销适度。

### 2. 方法适用边界

FairLLaVA 的设计决定了其适用边界存在以下约束：

**任务边界。** 当前验证集中在医学影像报告生成任务——胸部 X 光（MIMIC-CXR、PadChest）和皮肤镜 VQA（HAM10000）。这些任务的特点是：输入为医学图像，输出为结构化或半结构化的临床文本，且人口属性（种族、年龄、性别）标签可用。对于通用视觉问答、图像描述等非医学任务，该方法是否有效尚不明确，需要进一步验证。

**数据依赖。** 互信息最小化依赖于高质量的人口属性标签。在实际部署中，这些标签可能无法完整获取（如患者隐私限制）或存在噪声。论文在补充材料中尝试使用 **TorchXRayVision**（Cohen et al., 2022）进行域外人口属性预测（Table S.4），但预测标签的可靠性本身是一个限制因素。

**架构约束。** 当前实现基于 Vicuna-7b-v1.5 语言模型和 BioMedCLIP 图像编码器。LoRA 适配器的低秩结构可能无法完全恢复全参数微调的表达能力，在更大规模模型（如 70B 参数级别）或更复杂任务中，公平性改善的幅度可能受限。

**超参数敏感性。** 总损失 $\mathcal{L}_{total} = \lambda_1\mathcal{L}_{LM} + \lambda_2\mathcal{L}_{DIM} + \lambda_3\mathcal{L}_{DAC}$ 中的权重 $(\lambda_1, \lambda_2, \lambda_3)$ 影响公平-效用平衡。论文的灵敏度分析（Table S3, Fig. S1）表明，改变各属性互信息权重对权益标度性能影响温和，但自动寻找最优权重仍是一个开放问题。

### 3. 局限性与开放问题

**已验证的局限性：**

1. **任务泛化性未验证**：仅在医学报告生成和皮肤镜 VQA 上评估，对其他视觉-语言任务的迁移能力未知。
2. **标签依赖**：互信息估计器（DAC）需要人口属性标签，且其分类性能可能受类别极度不平衡影响，需依赖加权交叉熵等额外技巧。
3. **表示层选择**：消融实验（Table 6）表明，仅使用中间层隐藏状态（FairLLaVA‑mid）可在 6 个公平性间隙中缩小 5 个，而平均池化（FairLLaVA‑mean）虽总体性能最好但会扩大某些间隙。这说明层选择对公平性效果有显著影响，但论文未提供自动选择策略。
4. **DAC 训练策略**：联合训练 DAC 与 DIM 优于先预训练 DAC 再去偏的固定分类器方案（Table S.8），但联合训练的收敛动态可能更复杂。

**开放问题：**

1. **自适应权重调节**：如何自动化地设定 $(\lambda_1, \lambda_2, \lambda_3)$ 以达到不同应用场景下最优的公平-效用平衡？当前依赖人工调参，在多属性、多任务场景下难以扩展。
2. **跨领域迁移**：该方法是否能够有效迁移到除医学外的其他领域（如通用视觉问答、图像描述）？这些领域中人口属性的定义和敏感程度可能不同。
3. **弱监督扩展**：在缺少部分人口属性标签时，弱监督或无监督的互信息最小化策略是否可行？例如，是否可以利用预训练分类器预测缺失标签，或采用对比学习隐式去偏？
4. **与先进 PEFT 技术结合**：互信息正则化是否可与更先进的参数高效微调技术（如 AdaLoRA、QLoRA）结合，以进一步提升效率或性能？
5. **公平性度量改进**：生成文本中的临床公平性评估目前依赖外部 NLP 指标（BLEU、RadGraph-F1）和 LLM 打分（GREEN），是否需要更直接的医学适确性公平性度量，以捕捉临床决策中的实质性偏见？
6. **视觉编码器去偏**：当前互信息正则化仅作用于语言模型的隐藏状态，是否有必要在视觉编码器端也加入相似的去偏机制，以更彻底地消除图像中泄漏的人口统计信息（如皮肤颜色、骨骼密度等隐含特征）？

### 4. 在知识库中的定位

FairLLaVA 在 MLLM 公平性研究中的核心贡献在于：**将互信息最小化从传统表示学习领域引入多模态指令微调场景，并以参数高效的方式实现**。与现有的数据重平衡方法和对抗性去偏方法相比，它提供了一条更稳定、更轻量的技术路径。其“插件式”设计使其可以作为通用模块嵌入到各类 MLLM 的微调流程中，为后续研究提供了一个可扩展的公平性正则化框架。

## 原文 PDF

![[paperPDFs/CVPR_2026/FairLLaVA_Fairness_Aware_Parameter_Efficient_Fine_Tuning_for_Large_Vision_Language_Assistants.pdf]]
