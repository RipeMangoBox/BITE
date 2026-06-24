---
title: "When Weak LLMs Speak with Confidence, Preference Alignment Gets Stronger"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/When_Weak_LLMs_Speak_with_Confidence_Preference_Alignment_Gets_Stronger.pdf
openreview_forum_id: ROioaZ45Yz
aliases:
- CWPOCP
- WWLSCPAGS
tags:
- ICLR_2026
- topic/reinforcement_learning_planning_agents
- topic/reinforcement_learning_planning_agents/deep_rl
core_operator: "弱LLM对偏好预测的置信度（即正负样本预测边距的归一化分数，C(x,y+,y-)∈[0,1]）"
primary_logic: "弱LLM的高置信度标注子集比全量人类标注更有效；通过将弱LLM的预测置信度作为样本权重，引入偏好优化损失中，既可放大高质量标注的作用，又可抑制低质量标注的干扰，从而大幅减少对人类标注的依赖，同时提升对齐性能。"
claims:
- "使用30%人类标注训练的CW-DPO在多个基准上优于使用100%人类标注的标准DPO（平均GRA：68.8 vs 66.4）"
- "仅需20%的人类标注，CW-DPO即可超越全量标注的DPO（70.3% vs 69.7% GRA）"
- "置信度加权（CW-DPO）在所有数据集上优于基于置信度过滤（top-30%/40%样本），验证加权比丢弃数据更有效"
- "作为即插即用的增强方法，CW-PO在DPO、IPO、rDPO上平均提升GRA超过5%，最高提升9.5%"
---

# When Weak LLMs Speak with Confidence, Preference Alignment Gets Stronger

> [!tip] 核心洞察
> 弱LLM的高置信度标注子集比全量人类标注更有效；通过将弱LLM的预测置信度作为样本权重，引入偏好优化损失中，既可放大高质量标注的作用，又可抑制低质量标注的干扰，从而大幅减少对人类标注的依赖，同时提升对齐性能。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 弱LLM自信标注，偏好对齐更强大 |
| 英文题名 | When Weak LLMs Speak with Confidence, Preference Alignment Gets Stronger |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=ROioaZ45Yz) |
| Topic | #topic/reinforcement_learning_planning_agents #topic/reinforcement_learning_planning_agents/deep_rl |
| Method | Confidence-Weighted Preference Optimization (CW-PO) |
| Dataset | HH-RLHF, TL;DR, UFB, 全体平均（3数据集×3方法） |

> [!tip] 效果简介
> - HH-RLHF 上，GRA (%) 为 CW-DPO 61.3，对比 Human 56.9，变化 +4.4。
> - TL;DR 上，GRA (%) 为 CW-rDPO 61.4，对比 Human 54.2，变化 +7.2。
> - UFB 上，GRA (%) 为 CW-IPO 66.4，对比 Human 63.4，变化 +3.0。

## 概述

偏好对齐是使大语言模型符合人类价值观的核心环节，但高质量人类偏好标注的获取成本高昂且难以规模化。弱LLM虽可直接生成标注，但其整体噪声大，直接使用会损害对齐效果。关键瓶颈在于：弱LLM的高置信标注质量可能优于人类，而低置信标注则有害——现有方法未能有效区分样本置信度。

**核心发现**：弱LLM对偏好预测的置信度（即正负样本预测边距的归一化分数 $\mathcal{C}(x,y^+,y^-)\in[0,1]$）是区分标注质量的关键信号。高置信度标注子集比全量人类标注更有效，而将置信度作为样本权重嵌入偏好优化损失，可同时放大高质量标注的作用并抑制低质量标注的干扰。

基于此，本文提出**置信度加权偏好优化（Confidence-Weighted Preference Optimization, CW-PO）**框架：首先在少量人类标注上训练弱LLM作为偏好标注器，随后对无标注数据生成偏好标签并计算置信度，最后以置信度加权的方式训练强LLM。CW-PO是即插即用的增强方法，可无缝嵌入DPO、IPO、rDPO等主流偏好优化损失。

**主要结果**：
- CW-DPO仅使用30%人类标注，在多个基准上平均GRA达68.8，优于使用100%人类标注的标准DPO（66.4）（Table 3）。
- 仅需20%的人类标注，CW-DPO即可超越全量标注DPO（Figure 3）。
- 置信度加权在所有数据集上优于基于置信度过滤的方案，验证了加权比丢弃低置信数据更有效（Table 4）。
- CW-PO在DPO、IPO、rDPO上平均提升GRA超过5%，最高提升9.5%（Table 1）。

**方法定位**：CW-PO属于弱监督偏好对齐范畴，与**WS-DPO**（Tao & Li, 2025）等直接使用弱LLM标注的方法相比，核心区别在于引入样本级置信度权重，使对齐过程自适应地聚焦于高质量标注。

## 背景与动机

大型语言模型（LLM）的偏好对齐是使其输出符合人类价值观的关键步骤。当前主流范式——如 **DPO**（Rafailov et al., 2023）——依赖高质量的人类偏好标注来训练策略模型。然而，获取大规模人类偏好标注成本高昂且难以扩展，这构成了该领域的核心瓶颈。

一个自然的替代方案是使用弱LLM直接为无标注数据生成偏好标签，即弱监督偏好优化（**WS-DPO**, Tao & Li, 2025）。但该方法面临一个根本性困境：弱LLM的标注整体噪声较大，直接使用会损害对齐效果，甚至使性能低于人类标注基线。

本文揭示了一个关键洞察：**弱LLM的标注质量并非均匀分布**。具体而言，弱LLM对偏好预测的置信度——即正负样本预测边距的归一化分数 $C(x,y^+,y^-) \in [0,1]$——能够有效区分标注质量。高置信度标注子集的质量可能优于人类标注，而低置信度标注则具有显著危害性。Figure 2 的实验证据表明，仅使用弱LLM置信度最高的30%样本进行对齐训练，其黄金奖励准确率（GRA）即可超越使用全量人类标注的DPO。

然而，现有方法未能充分利用这一特性：**WS-DPO** 对所有弱标注样本赋予均等权重，导致低质量标注的噪声污染训练信号；而简单的**置信度过滤**方案（如仅保留top-30%或top-40%高置信样本）会丢弃潜在有用的数据，且单一阈值难以在不同任务域之间普适（见Figure 4和Figure 7中不同域的置信度分布差异）。

因此，本文的核心动机在于：**如何系统性地利用弱LLM的置信度信息，在减少对人类标注依赖的同时，实现更优的对齐性能？** 这要求一种能够自适应地区分样本质量、放大高置信标注作用、抑制低置信标注干扰的机制，而非简单的二元过滤或均匀加权。

## 核心创新

CW-PO 的核心创新在于**将弱LLM的预测置信度作为样本级权重嵌入偏好优化损失**，从而在不改变底层对齐算法的情况下，实现对噪声标注的自适应利用。这一设计改变了传统偏好优化中所有样本均匀贡献梯度的假设，形成了两个关键的 **changed slots**：

### 从均匀权重到置信度加权

在标准偏好优化（如 **DPO** (Rafailov et al., 2023)、**IPO** (Azar et al., 2024)、**rDPO** (Chowdhury et al., 2024)）中，每个偏好三元组 $(x, y^+, y^-)$ 对损失的贡献权重恒为 1，即所有样本被视为同等可靠。然而，当标注来源于弱LLM时，这一假设不再成立：高置信度标注的质量可能优于人类，而低置信度标注则可能引入有害噪声。

CW-PO 将弱LLM对偏好预测的置信度 $\mathcal{C}(x,y^+,y^-) \in [0,1]$ 作为样本权重，构造通用加权损失：

$$\mathcal{L}_{\mathrm{CW-PO}} = \mathbb{E}_{(x,y^+,y^-)\sim\hat{\mathcal{D}}} \left[ \mathcal{C}(x,y^+,y^-) \cdot \ell(\pi_s; x,y^+,y^-) \right]$$

其中置信度 $\mathcal{C}$ 由弱LLM对正负样本的预测边距经 sigmoid 缩放得到：

$$\mathcal{C}(x,y^+,y^-) = 2 \cdot (\sigma(\pi_w(x,y^+) - \pi_w(x,y^-)) - 0.5)$$

这一设计的因果机制在于：弱LLM预测边距越大，其对偏好方向的确定性越高，标注越可能正确。通过将置信度作为乘法权重，高置信度样本主导梯度更新，低置信度样本的贡献被抑制至接近零，从而实现了**放大高质量信号、抑制噪声干扰**的效果。消融实验证实，置信度加权（CW-DPO）在所有数据集上均显著优于基于置信度过滤（仅保留 top-30% 或 top-40% 高置信样本）的策略（Table 4），说明加权方案避免了丢弃潜在有用的低置信数据，比硬过滤更稳健。

### 弱标注器训练目标的重新设计

与常见做法（使用 DPO 或 SFT+DPO 训练弱LLM作为生成式奖励模型）不同，CW-PO 采用**确定性标量奖励函数**加 **Bradley-Terry 交叉熵损失**直接优化偏好排序：

$$\mathcal{L}_{\mathrm{weak}} = -\mathbb{E}_{(x,y^+,y^-)\sim\mathcal{D}_{\mathrm{labeled}}} \left[ \log \sigma(\pi_w(x,y^+) - \pi_w(x,y^-)) \right]$$

具体实现上，弱LLM 保留预训练骨干网络，将最后一层替换为标量输出层，输出单个偏好分数 $\pi_w(x,y)$，整个模型端到端优化。这一设计相比 DPO 或 SFT+DPO 具有双重优势：一是表达更直接高效，无需通过生成概率隐式推导偏好；二是训练速度更快、标注准确率更高（Table 6，BT 方案平均准确率 64.8% vs DPO 的 53.8%，训练时间减少约 26%）。更高的弱标注器准确率为后续置信度加权提供了更可靠的信号基础。

### 即插即用的增强特性

CW-PO 不修改底层偏好优化算法的结构，仅通过样本权重引入置信度信息。这使得它可以**即插即用**地增强任意偏好优化方法——只需将标准损失替换为对应的置信度加权版本（如 CW-DPO、CW-IPO、CW-rDPO）。实验表明，在 DPO、IPO、rDPO 三种方法上，CW-PO 平均提升 GRA 超过 5%，最高提升 9.5%（Table 1），验证了该设计的通用性和有效性。

## 整体框架

![[assets/figures/papers/paper_list_l14_https_openreview_net_forum_id_ROioaZ45Yz/figures/001_Figure_1.jpg]]
*Figure 1: Overall pipeline of our setting. Top: Conventional DPO (Rafailov et al., 2023). For each triplet consisting of a prompt x and two candidate responses ( y _ { 1 } , y _ { 2 } ) , human annotators provide preference labels, and the policy model is aligned with these labels using DPO. Bottom: CW-DPO framework. A weak LLM is first trained as a preference annotator using a subset of human-labeled triplets. It is then applied to annotate the remaining large-scale data, which is subsequently trained with CW-DPO. The bars on top right report Gold Reward Accuracy for standard DPO with humanlabeled data (red) and for CW-DPO (blue) on the ANTHROPIC HH-RLHF. CW-DPO uses only 30% compared to DPO, which...*

### 问题背景与核心思路

偏好对齐训练通常依赖人类标注的偏好三元组 $(x, y^+, y^-)$，但高质量人类标注成本高昂且难以扩展。一个自然替代方案是使用弱LLM直接生成偏好标注，然而弱LLM的标注整体噪声较大，直接使用会损害对齐效果。本文的核心发现是：**弱LLM的高置信度标注子集质量优于全量人类标注**，而低置信度标注则有害。基于此，论文提出置信度加权偏好优化（Confidence-Weighted Preference Optimization, CW-PO），将弱LLM的预测置信度作为样本权重嵌入偏好优化损失，从而放大高质量标注的作用、抑制低质量标注的干扰。

### CW-PO 三阶段流水线

CW-PO 框架由三个顺序模块组成，输入输出关系清晰：

**阶段一：弱标注器训练。** 在少量人类标注数据 $\mathcal{D}_{\text{labeled}}$ 上训练弱LLM作为偏好评分函数 $\pi_w(x, y)$。具体地，使用预训练骨干网络替换最后一层为标量输出层，通过 Bradley-Terry 交叉熵损失直接优化偏好排序概率：

$$\mathcal{L}_{\text{weak}} = -\mathbb{E}_{(x,y^+,y^-)\sim\mathcal{D}_{\text{labeled}}} \left[ \log \sigma(\pi_w(x,y^+) - \pi_w(x,y^-)) \right]$$

该确定性奖励函数设计比 DPO 或 SFT+DPO 训练的弱标注器准确率更高且训练时间更短（见 Table 6）。

**阶段二：弱标注生成与置信度计算。** 训练好的弱LLM对无标注数据 $\mathcal{D}_{\text{unlabeled}}$ 中的每对候选响应 $(y_1, y_2)$ 生成偏好标签：选择评分较高的响应作为 $y^+$，较低的作为 $y^-$。同时计算每对的置信度分数：

$$\mathcal{C}(x,y^+,y^-) = 2 \cdot (\sigma(\pi_w(x,y^+) - \pi_w(x,y^-)) - 0.5)$$

该分数基于弱LLM对正负样本的预测边距，经 sigmoid 归一化至 $[0,1]$：边距越大，置信度越接近1，表示弱LLM对该偏好判断越确定。

**阶段三：置信度加权强模型对齐。** 将置信度作为样本权重嵌入任意偏好优化损失，训练强LLM：

$$\mathcal{L}_{\mathrm{CW-PO}} = \mathbb{E}_{(x,y^+,y^-)\sim\hat{\mathcal{D}}} \left[ \mathcal{C}(x,y^+,y^-) \cdot \ell(\pi_s; x,y^+,y^-) \right]$$

其中 $\ell$ 可以是 DPO、IPO、rDPO 等任意偏好优化损失。以 CW-DPO 为例：

$$\mathcal{L}_{\mathrm{CW-DPO}} = -\mathbb{E} \left[ \mathcal{C} \cdot \log \sigma\left( \beta \log \frac{\pi_s(y^+|x)}{\pi_{\text{ref}}(y^+|x)} - \beta \log \frac{\pi_s(y^-|x)}{\pi_{\text{ref}}(y^-|x)} \right) \right]$$

高置信度样本获得更大权重，主导梯度更新；低置信度样本权重趋于0，其噪声被有效抑制。

### 关键设计选择

**加权优于过滤。** 一个直观替代方案是基于置信度阈值过滤，仅保留 top-N% 高置信样本训练。消融实验（Table 4）表明，置信度加权在所有数据集上均优于最优阈值过滤方案（top-30% 或 40%），因为加权避免了丢弃潜在有用的低置信数据，且无需为不同任务手动调整阈值（Figure 4 显示单一阈值难以普适）。

**即插即用特性。** CW-PO 不改变底层偏好优化算法，仅通过样本权重引入弱LLM置信度信号，可作为增强模块直接应用于 DPO、IPO、rDPO 等方法。实验显示 CW-PO 在三类方法上平均提升 GRA 超过 5%，最高提升 9.5%（Table 1）。

**标注效率。** 弱标注器仅需 30% 人类标注即可训练，且 CW-DPO 在此设置下优于使用 100% 人类标注的标准 DPO（平均 GRA: 68.8 vs 66.4, Table 3）；仅需 20% 标注即可超越全量标注 DPO（Figure 3 Right）。

## 核心模块与公式推导

### 方法总览：三阶段管道

CW-PO 框架由三个顺序模块构成，形成“弱标注器训练 → 弱标注生成与置信度计算 → 置信度加权强模型对齐”的管道：

1. **弱标注器训练**：在少量人类标注数据 $\mathcal{D}_{\text{labeled}}$ 上训练一个弱LLM作为偏好评分函数 $\pi_w(x, y)$。弱模型使用预训练骨干，绕过最后一层后添加标量输出层，整体优化。
2. **弱标注生成与置信度计算**：用训练好的 $\pi_w$ 对无标注数据 $\mathcal{D}_{\text{unlabeled}}$ 中的每对响应 $(y_1, y_2)$ 预测偏好标签（评分高者为 $y^+$，低者为 $y^-$），并计算每对样本的置信度 $\mathcal{C}(x, y^+, y^-)$。
3. **置信度加权强模型对齐**：以置信度 $\mathcal{C}$ 作为样本权重，代入任意偏好优化损失函数，训练强LLM $\pi_s$。

### 核心公式

#### 弱标注器训练目标

弱LLM作为确定性奖励函数，直接用 Bradley-Terry 交叉熵损失优化偏好排序能力：

$$\mathcal{L}_{\text{weak}} = -\mathbb{E}_{(x,y^+,y^-)\sim\mathcal{D}_{\text{labeled}}} \left[ \log \sigma(\pi_w(x,y^+) - \pi_w(x,y^-)) \right] \tag{5}$$

其中 $\sigma(\cdot)$ 为 sigmoid 函数，$\pi_w(x,y^+) - \pi_w(x,y^-)$ 表示弱模型对正负样本的预测边距。该损失最大化弱模型正确排序偏好对的概率。

#### 偏好标签生成规则

对无标注数据中的每对候选响应，按弱模型评分直接分配偏好标签：

$$y^+ = \arg\max_{y \in \{y_1, y_2\}} \pi_w(x,y), \quad y^- = \arg\min_{y \in \{y_1, y_2\}} \pi_w(x,y) \tag{6}$$

#### 置信度分数定义（核心因果旋钮）

置信度 $\mathcal{C}(x, y^+, y^-)$ 基于弱LLM对正负样本的预测边距，经 sigmoid 归一化后缩放至 $[0,1]$ 区间：

$$\mathcal{C}(x,y^+,y^-) = 2 \cdot \left( \sigma(\pi_w(x,y^+) - \pi_w(x,y^-)) - 0.5 \right) \tag{8}$$

- **变量含义**：$\pi_w(x,y^+)$ 和 $\pi_w(x,y^-)$ 分别为弱模型对正、负样本的标量评分；$\sigma(\cdot)$ 将边距映射为 $(0,1)$ 的偏好概率。
- **机制**：当弱模型对偏好判断越确定（边距越大），$\mathcal{C}$ 越接近 1；当弱模型无法区分（边距趋近 0），$\mathcal{C}$ 趋近 0。该分数是区分“高置信标注质量可能优于人类”与“低置信标注有害”的核心因果旋钮。

#### 置信度加权偏好优化损失（通用形式）

将置信度 $\mathcal{C}$ 作为样本权重，嵌入任意偏好优化损失 $\ell$：

$$\mathcal{L}_{\text{CW-PO}} = \mathbb{E}_{(x,y^+,y^-)\sim\hat{\mathcal{D}}} \left[ \mathcal{C}(x,y^+,y^-) \cdot \ell(\pi_s; x,y^+,y^-) \right] \tag{7}$$

其中 $\hat{\mathcal{D}}$ 为弱LLM标注后的偏好数据集。该加权机制使高置信样本主导梯度更新，低置信样本权重趋于零，实现“放大高质量标注、抑制噪声标注”的效果。

#### CW-DPO 损失（具体实例化）

将置信度权重嵌入标准 DPO 损失：

$$\mathcal{L}_{\text{CW-DPO}} = -\mathbb{E} \left[ \mathcal{C} \cdot \log \sigma\left( \beta_{\text{DPO}} \log \frac{\pi_s(y^+|x)}{\pi_{\text{ref}}(y^+|x)} - \beta_{\text{DPO}} \log \frac{\pi_s(y^-|x)}{\pi_{\text{ref}}(y^-|x)} \right) \right] \tag{9}$$

- $\beta_{\text{DPO}}$：控制偏离参考策略 $\pi_{\text{ref}}$ 程度的温度参数。
- $\pi_s(y|x)$ 和 $\pi_{\text{ref}}(y|x)$：分别为强模型策略和参考策略在给定提示 $x$ 下生成响应 $y$ 的概率。

#### CW-IPO 损失（具体实例化）

置信度加权的 IPO 损失，通过对数比率与正则项之差的平方加权：

$$\mathcal{L}_{\text{CW-IPO}} = -\mathbb{E} \left[ \mathcal{C} \left( \log\left(\frac{\pi_\theta(y^+|x)\pi_{\text{ref}}(y^-|x)}{\pi_\theta(y^-|x)\pi_{\text{ref}}(y^+|x)}\right) - \frac{1}{2\beta_{\text{IPO}}} \right)^2 \right] \tag{10}$$

- $\beta_{\text{IPO}}$：IPO 特有的正则化参数，控制对数比率偏离目标值 $1/(2\beta_{\text{IPO}})$ 的惩罚强度。

### 设计要点

- **即插即用性**：CW-PO 不改变底层偏好优化算法（DPO/IPO/rDPO）的结构，仅在损失函数中对每个样本乘以置信度权重 $\mathcal{C}$，可无缝嵌入现有对齐管道。
- **加权优于过滤**：与基于置信度阈值过滤（仅保留 top-N% 高置信样本）相比，加权方案保留了低置信样本的微弱信号，避免丢弃潜在有用数据，实验验证在所有数据集上加权均优于过滤（Table 4）。
- **置信度函数选择**：消融实验表明，缩放 sigmoid 差（式 8 中的 $\mathcal{C}_1$）在多个数据集上提供最稳定且一致的提升（Table 5），优于原始 sigmoid 差、截断原始边距等替代方案。

## 实验与分析

### 核心发现：弱LLM高置信标注可超越全量人类标注

CW-PO的核心实证发现是：弱LLM的高置信度偏好标注子集，在驱动强模型对齐时，效果可超过使用全量人类标注。这一结论在多个维度得到验证。

**Figure 2** 展示了关键动机实验：仅使用弱LLM标注中置信度最高的top-30%样本训练强模型，其黄金奖励准确率（GRA）在多个数据集上显著超越使用100%弱LLM标注，也超越人类标注基线。例如，在HH-RLHF的Harmless子集上，OPT-125M→OPT-1.3B设定下，top-30%高置信样本的GRA明显高于全量人类标注。这直接催生了CW-PO的核心设计：不是简单地丢弃低置信样本，而是用置信度作为样本权重。

### 主实验结果：即插即用的显著提升

**Table 1** 报告了CW-PO作为即插即用增强方法的效果。在三种基础偏好优化方法（DPO、IPO、rDPO）和三个数据集（HH-RLHF、TL;DR、UFB）上，CW-PO（弱模型仅用30%人类标注训练）相比两个基线——全量人类标注（Human）和弱模型直接监督（WS-DPO）——均取得一致且显著的提升：

![[assets/figures/papers/paper_list_l14_https_openreview_net_forum_id_ROioaZ45Yz/figures/003_Table_1.jpg]]
*Table 1: Results across different preference alignment methods. The reported values are GRA (%). Weak models in WS-DPO and CW-DPO are trained with 30% of human annotated data. Alignment data for the strong model is fixed across all experiments. CW-PO columns are highlighted in blue*

- **vs. Human**：CW-PO平均GRA提升约5%（例如HH-RLHF上CW-DPO达61.3 vs Human 56.9；TL;DR上CW-rDPO达61.4 vs Human 54.2）。
- **vs. WS-DPO**：CW-PO平均GRA提升5.2%（61.5 vs 57.1），最高单数据集提升达9.5%。

这表明置信度加权机制是超越简单弱监督的关键。CW-PO不改变底层对齐算法，仅通过样本级权重注入弱LLM的判别信心，即可大幅提升对齐质量。

### 缩放特性：中小模型受益更大

**Table 2** 考察了强模型规模（1.3B至14B）对CW-PO增益的影响。结果显示，较小和中等的强模型从CW-PO中获益最大——例如OPT-1.3B上CW-DPO相比Human基线提升约5个GRA点。随着强模型规模增大，CW-PO的增益幅度有所缩小，但仍保持正向。这一趋势符合直觉：大模型自身已具备较强的偏好判别能力，对弱模型信号的依赖降低；但即使在14B规模，置信度加权仍提供额外信息。

![[assets/figures/papers/paper_list_l14_https_openreview_net_forum_id_ROioaZ45Yz/figures/004_Table_2.jpg]]
*Table 2: Qwen2.5-0.5B → Qwen2.5-14B*

![[assets/figures/papers/paper_list_l14_https_openreview_net_forum_id_ROioaZ45Yz/figures/005_Table_2.jpg]]
*Table 2: Performance across different student models measured as GRA (%). We use OPT-125M and Qwen2.5-0.5B as the weak models for the OPT and Qwen families, respectively. GRA measures improvement over a model’s SFT baseline; thus larger models may not score higher GRA, since stronger baselines leave less room to improve even if absolute performance is higher*

### 标注效率：仅需20%人类标注即可超越全量标注DPO

**Table 3** 和 **Figure 3** 直接比较了CW-DPO（使用30%人类标注训练弱模型）与使用100%人类标注的标准DPO。在OPT和Qwen两个模型家族上，CW-DPO在四个数据集上平均GRA为68.8，而全量人类标注DPO为66.4。更重要的是，**Figure 3（右）** 显示，当弱模型仅使用20%人类标注训练时，CW-DPO的GRA（70.3%）已超越全量标注DPO（69.7%）。这验证了CW-PO在标注效率上的巨大优势——仅需五分之一的人类标注成本即可达到甚至超越全量标注的对齐效果。

![[assets/figures/papers/paper_list_l14_https_openreview_net_forum_id_ROioaZ45Yz/figures/006_Table_3.jpg]]
*Table 3: Comparison between DPO using the fully human-annotated dataset ( $\mathcal { D } _ { \mathrm { l a b e l e d } } \cup D _ { \mathrm { u n l a b e l e d } }$ ) and CW-DPO. Parentheses show the relative change from the Human baseline

![[assets/figures/papers/paper_list_l14_https_openreview_net_forum_id_ROioaZ45Yz/figures/007_Figure_3.jpg]]
*Figure 3: Left: GRA when adjusting the proportion of $\mathcal { D } _ { \mathrm { l a b e l e d } }$ used to fine-tune the weak LLM, while retaining 50% of the data as training for the strong LLM. R i g h t $\colon$ GRA across varying proportions of $\mathcal { D } _ { \mathrm { l a b e l e d } }$ . As the split ratio decreases, the size of $\mathcal { D } _ { \mathrm { l a b e l e d } }$ decreases and $\mathcal { D } _ { \mathrm { u n l a b e l e d } }$ increases because the total dataset ( $\mathcal { D } _ { \mathrm { l a b e l e d } } \cup \mathcal { D } _ { \mathrm { u n l a b e l e d } }$ ) is fixed

### 消融研究

#### 加权 vs. 过滤：加权方案普遍更优

**Table 4** 比较了置信度加权（CW-DPO）与置信度过滤（仅使用top-30%或top-40%高置信样本训练标准DPO）。在HARMLESS、HELPFUL、HH-RLHF三个数据集上，CW-DPO一致优于最佳过滤阈值设定（例如HARMLESS上72.9 vs 72.3；HELPFUL上72.7 vs 70.1）。加权方案的优势在于保留了低置信样本的信息（尽管权重很小），而过滤方案直接丢弃了这些数据，损失了潜在的微弱信号。

![[assets/figures/papers/paper_list_l14_https_openreview_net_forum_id_ROioaZ45Yz/figures/009_Table_4.jpg]]
*Table 4: Comparison of confidencebased weighting, i.e., CW-DPO, and confidence-based filtering using the top 30% and 40% of samples. OPT-125M → OPT-1.3B*

**Figure 4** 进一步揭示，不同数据集的最佳置信度阈值差异显著（HARMLESS为30%，HH-RLHF为40%），单一阈值难以普适。这从反面支持了自适应加权方案的必要性。

![[assets/figures/papers/paper_list_l14_https_openreview_net_forum_id_ROioaZ45Yz/figures/010_Figure_4.jpg]]
*Figure 4: Alignment results across top-N% confidence thresholds*

#### 置信度函数设计：缩放sigmoid差最稳定

**Table 5** 比较了四种置信度加权函数（C1至C4）。C1（缩放sigmoid差，$\mathcal{C}_1 = 2 \cdot (\sigma(\Delta) - 0.5)$）在三个数据集上平均GRA最高（72.7），且表现最稳定。C2（原始sigmoid差）在某些数据集上性能骤降，C3（截断原始差）和C4（其他变体）整体弱于C1。C1的优势在于将置信度线性映射到[0,1]区间，使权重分布更均匀，避免极端值主导训练。

#### 弱标注器训练目标：Bradley-Terry优于DPO

**Table 6** 比较了三种弱模型训练方案：DPO、SFT+DPO、以及本文采用的Bradley-Terry（BT）目标。BT方案在OPT-125M和Qwen-0.5B上均取得最高平均准确率（64.8%），且训练时间最短（2,450秒 vs DPO的3,319秒）。BT使用确定性标量输出直接优化偏好概率，避免了DPO中参考模型和对数比率计算的额外开销，同时更直接地对齐标注任务目标。

![[assets/figures/papers/paper_list_l14_https_openreview_net_forum_id_ROioaZ45Yz/figures/012_Table_6.jpg]]
*Table 6: Accuracy and efficiency of weak models*

### 失败模式与局限性

1. **在线设置性能退化**：CW-PO设计用于离线偏好优化。**Figure 6** 显示，在在线迭代设置中，由于强模型策略分布持续变化，弱LLM的离线标注和置信度无法适应新分布，导致CW-PO性能显著低于离线设定，甚至低于常规在线DPO。嵌入空间的可视化揭示了策略分布偏移是根本原因。

2. **弱标注器质量依赖**：**Table 25** 和 **Figure 8** 考察了对抗投毒攻击下的鲁棒性。随着投毒比例增加，弱模型与人类标注的不一致率上升，CW-DPO的GRA随之下降。虽然CW-PO的降幅小于WS-DPO，但在高投毒比例下性能仍显著受损，表明方法对弱标注器的质量有一定要求。

3. **置信度分布跨域差异**：**Figure 7** 显示，弱LLM在不同任务/域上的置信度分布差异显著。某些域（如HH-RLHF）的置信度普遍偏高，而其他域则偏低。这解释了为什么单一置信度阈值（Figure 4）无法普适，也暗示当前统一的加权函数C1并非在所有情景下最优。

4. **数据不平衡敏感性**：**Table 24** 报告了训练数据中无害性与有用性样本比例不平衡时的性能权衡。WS-DPO对不平衡更为敏感，CW-PO虽有所缓解，但在极端不平衡下仍出现性能倾斜。

### 补充图表

![[assets/figures/papers/paper_list_l14_https_openreview_net_forum_id_ROioaZ45Yz/figures/011_Table_7.jpg]]

![[assets/figures/papers/paper_list_l14_https_openreview_net_forum_id_ROioaZ45Yz/figures/013_Table_7.jpg]]
*Table 7: Training hyperparameters for weak models*

![[assets/figures/papers/paper_list_l14_https_openreview_net_forum_id_ROioaZ45Yz/figures/014_Table_8.jpg]]
*Table 8: Training hyperparameters for strong models with DPO, IPO, rDPO and their confidenceweighted variants*

## 方法谱系与知识库定位

### 与基线方法的关系

CW-PO 并非提出全新的偏好优化目标函数，而是作为一种**即插即用的样本重加权增强机制**，可嵌入任意现有的离线偏好优化损失中。论文在三种代表性 PO 方法上验证了该机制的有效性：

- **DPO**（Rafailov et al., 2023）：直接偏好优化的基础方法，通过对数比率差建模偏好概率。CW-DPO 在 DPO 损失上乘以置信度权重，使高置信度样本主导梯度更新。
- **IPO**（Azar et al., 2024）：通过平方损失约束对数比率与正则项的距离。CW-IPO 同样引入置信度加权，缓解了 IPO 对噪声标注的敏感性。
- **rDPO**（Chowdhury et al., 2024）：鲁棒 DPO 变体，引入偏置项处理长度偏差等问题。CW-rDPO 将置信度权重叠加于 rDPO 的鲁棒性之上，形成双重保护。

与直接使用弱 LLM 标注的 **WS-DPO**（Tao & Li, 2025）相比，CW-PO 的核心差异在于**不将弱模型输出视为等权的偏好标签**，而是通过预测边距提取置信度信号，对样本进行差异化加权。实验表明，CW-PO 在三个数据集、三种 PO 方法上的平均 GRA 提升达 +4.4%（61.5 vs 57.1），最高提升 +9.5%（Table 1）。

与**置信度过滤方法**（仅保留 top-30% 或 top-40% 高置信样本）相比，CW-PO 的加权方案在所有数据集上均表现出更优或持平的性能（Table 4）。这验证了核心设计选择：**加权优于丢弃**——低置信度样本虽不可靠，但完全排除会损失潜在有用的训练信号。

### 弱标注器的设计选择与定位

CW-PO 的弱标注器采用了**Bradley-Terry（BT）确定性标量评分架构**：在预训练骨干之上添加标量输出层，直接用交叉熵损失优化偏好排序概率。这与现有弱监督对齐工作中常见的两类方案形成对比：

- **DPO 训练的弱模型**：将弱 LLM 作为生成式策略，通过隐式奖励（对数概率比）表达偏好。论文实验表明，BT 方案在标注准确率（64.8% vs 53.8%）和训练效率（2,450s vs 3,319s）上均显著优于 DPO 方案（Table 6）。
- **SFT+DPO 两阶段训练**：先监督微调再偏好优化，训练成本最高（4,978s），准确率居中（54.9%）。

BT 方案的优势源于其**直接优化偏好排序**的目标与标注任务天然对齐，避免了从生成分布中间接推导偏好信号的信息损失。这一设计使弱标注器即使在仅 30% 人类标注数据上训练，也能产生产出质量超越全量人类标注的高置信子集。

### 适用边界与核心局限

**离线场景是 CW-PO 的基本前提。** 论文明确指出，在线设置下 CW-PO 性能显著下降，甚至低于常规在线 DPO。原因在于：弱标注器在离线数据上训练后固定不变，无法适应强模型策略分布的变化。当强模型在线采样产生分布外响应时，弱模型的置信度估计失准，导致加权失效（Figure 6 展示了嵌入空间的分布偏移现象）。

**弱标注器质量构成性能下界。** 尽管 CW-PO 能放大高置信标注的效用，但弱模型本身的预测准确率有限（约 65%）。当训练数据高度不平衡或遭受对抗投毒时，弱模型的置信度分布发生偏移，CW-PO 的性能随之下降（Table 25, Figure 8）。这表明方法对弱标注器的训练数据质量和分布有一定要求，并非完全无监督。

**模型规模存在收益递减。** 实验显示，较小和中等的强模型（1.3B–7B）从 CW-PO 获益最大；当强模型规模扩大至 13B–14B 时，GRA 提升幅度收窄（Table 2）。这可能因为大模型本身具备更强的噪声鲁棒性，置信度加权带来的边际增益相应减小。

**跨任务置信度设计尚未统一。** 不同置信度加权函数（C1–C4）在不同数据集上表现各异，C1（缩放 sigmoid 差）整体最优但并非在所有情景下都占优（Table 5）。此外，弱模型在不同任务/域上的置信度分布差异显著（Figure 7），单一阈值或加权函数难以普适，需要针对具体场景进行选择或校准。

### 开放问题

当前工作揭示了几个值得进一步探索的方向：

1. **置信度信息的深层融合**：当前 CW-PO 仅将置信度作为样本级乘法权重，是否有更精细的融合方式？例如将置信度纳入损失函数的温度调节、作为贝叶斯先验建模标注不确定性、或在梯度层面进行自适应缩放。

2. **在线场景的弱模型更新**：如何使弱奖励模型持续适应强模型策略分布的变化？可能的路径包括迭代重标注、在线置信度校准、或使用强模型的反馈信号微调弱标注器。

3. **完全无监督的置信度生成**：当前框架仍依赖少量人类标注训练弱标注器。在零人类标签场景下，是否可以通过自监督信号（如响应一致性、多模型集成分歧）生成置信度并驱动对齐？

4. **与更广泛对齐范式的结合**：CW-PO 目前仅在 DPO/IPO/rDPO 上验证，与 KTO、SimPO 等新近损失函数，或与 RLHF 的奖励建模阶段的结合是否仍能带来增益，尚待验证。

5. **置信度校准**：弱 LLM 的原始预测边距是否真实反映标注正确率？引入温度缩放、保序回归等校准技术，可能进一步提升加权效果。

## 原文 PDF

![[paperPDFs/ICLR_2026/When_Weak_LLMs_Speak_with_Confidence_Preference_Alignment_Gets_Stronger.pdf]]
