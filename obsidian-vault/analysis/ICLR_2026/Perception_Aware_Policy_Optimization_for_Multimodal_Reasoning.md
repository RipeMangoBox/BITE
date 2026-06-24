---
title: "Perception-Aware Policy Optimization for Multimodal Reasoning"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/Perception_Aware_Policy_Optimization_for_Multimodal_Reasoning.pdf
openreview_forum_id: izbBqTL8vb
aliases:
- PPAPO
- PAPOMR
tags:
- ICLR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/segmentation
core_operator: "在GRPO/DAPO的强化学习目标中引入Implicit Perception Loss (KL_prcp)，通过最大化原始图像与掩蔽图像下策略的KL散度，迫使模型利用视觉信息进行推理。"
primary_logic: "不依赖外部标注或奖励模型，通过对比视觉输入的信息增益来奖励视觉扎实的生成，使模型同时学习感知与推理，从而大幅减少感知错误。"
claims:
- "标准GRPO训练后多模态模型的错误中，67%是感知错误。"
- "PAPO在八个多模态推理基准上相对GRPO/DAPO平均提升4.4%-17.5%，强视觉依赖任务上提升8.0%-19.1%。"
- "PAPO将感知错误减少了30.5%。"
- "Implicit Perception Loss与Double Entropy Loss的组合是性能提升和训练稳定的关键。"
---

# Perception-Aware Policy Optimization for Multimodal Reasoning

> [!tip] 核心洞察
> 不依赖外部标注或奖励模型，通过对比视觉输入的信息增益来奖励视觉扎实的生成，使模型同时学习感知与推理，从而大幅减少感知错误。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 面向多模态推理的感知感知策略优化 |
| 英文题名 | Perception-Aware Policy Optimization for Multimodal Reasoning |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=izbBqTL8vb) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/segmentation |
| Method | PAPO (Perception-Aware Policy Optimized) |
| Dataset | 8个多模态推理基准 (Qwen2.5-VL-3B), 8个多模态推理基准 (Qwen2.5-VL-7B), 强视觉依赖任务子集 (Qwen2.5-VL-7B) |

> [!tip] 效果简介
> - 8个多模态推理基准 (Qwen2.5-VL-3B) 上，avg@8 acc % 为 49.92 (PAPO_G)，对比 47.92 (GRPO)，变化 +4.36% 相对提升。
> - 8个多模态推理基准 (Qwen2.5-VL-7B) 上，avg@8 acc % 为 63.16 (PAPO_D)，对比 55.01 (DAPO)，变化 +17.54% 相对提升。
> - 强视觉依赖任务子集 (Qwen2.5-VL-7B) 上，avg@8 acc % 为 59.37 (PAPO_G)，对比 54.11 (GRPO)，变化 +7.96% 相对提升。

## 概述

当前多模态推理模型面临一个关键瓶颈：**视觉感知薄弱是导致推理失败的主要原因**。对使用标准GRPO训练的模型进行人工错误分析发现，67%的错误源于感知缺陷，而非逻辑推理或计算能力不足（Figure 1）。这一发现揭示了现有强化学习优化目标在多模态场景下的根本性局限——它们仅依赖文本奖励信号驱动策略更新，缺乏对视觉信息利用的显式激励。

针对上述问题，本文提出**PAPO（Perception-Aware Policy Optimization）**，核心思路是在GRPO/DAPO的强化学习目标中引入**隐式感知损失（Implicit Perception Loss, KL_prcp）**。该损失通过最大化模型在原始图像与掩蔽图像条件下的输出策略KL散度，迫使模型利用视觉信息进行推理，从而在不依赖外部标注或奖励模型的前提下，同时学习感知与推理能力。

在八个多模态推理基准上，PAPO相对GRPO/DAPO平均提升**4.4%–17.5%**，在强视觉依赖任务上提升更为显著（**8.0%–19.1%**），并将感知错误减少**30.5%**。方法可无缝替换GRPO或DAPO，训练开销仅增加约20%。

## 背景与动机

### 多模态推理中的感知瓶颈

大型多模态模型（LMM）在视觉问答、数学推理等任务上取得了显著进展，但在需要精细视觉理解的复杂推理场景中仍频繁出错。对标准强化学习（GRPO）训练后的多模态模型进行手动错误分析发现，**67%的错误源于视觉感知薄弱**，而非逻辑推理或计算能力不足（Figure 1）。这一比例揭示了当前多模态推理系统的核心瓶颈：模型在生成推理链时未能充分扎根于视觉输入，导致“看图不清”引发连锁推理错误。

### 现有RLVR方法的缺口

以 GRPO（Shao et al., 2024）和 DAPO（Yu et al., 2025）为代表的强化学习与可验证奖励（RLVR）方法在文本推理领域取得了成功，但其优化目标在设计上存在结构性缺口：

- **奖励信号的感知盲区**：GRPO/DAPO 的目标函数仅依赖任务奖励（如答案正确性）和策略KL惩罚，缺乏对视觉感知质量的直接激励。模型可以通过“猜测”或依赖语言先验获得奖励，而无需真正利用图像信息。
- **训练不稳定性**：DAPO 移除了参考KL惩罚以简化目标，但在较大模型（7B）上容易出现后期训练崩溃（Figure 4），缺乏有效的正则化手段来维持训练稳定。
- **感知与推理的割裂**：现有方法将感知视为固定的前处理步骤，而非与推理联合优化的过程。这导致模型即使推理能力提升，感知错误仍然居高不下。

### 本文动机

针对上述缺口，本文提出核心问题：**能否在RLVR框架内设计一个优化目标，使模型同时学习感知与推理，从而系统性减少感知错误？**

关键洞察在于：不依赖外部标注、教师模型或昂贵的神经奖励模型，而是通过**对比视觉输入的信息增益**来奖励视觉扎实的生成。具体而言，如果模型在完整图像下生成的响应与在受损图像下生成的响应差异显著，则表明模型有效利用了视觉信息。这一信号可以作为策略优化的内在奖励，引导模型主动关注视觉内容。

基于此，本文提出 **PAPO（Perception-Aware Policy Optimization）**，一种感知感知的策略优化算法。PAPO 在 GRPO/DAPO 目标中引入两项关键组件：
1. **隐式感知损失（Implicit Perception Loss, KL_prcp）**：通过最大化原始图像与掩蔽图像下策略输出的KL散度，量化并激励模型对视觉信息的依赖。
2. **双熵损失（Double Entropy Loss）**：对原始策略和掩蔽策略同时施加熵惩罚，防止 KL_prcp 的无界增长导致训练崩溃。

PAPO 可作为 GRPO 或 DAPO 的直接替代方案，无需额外标注或模型，在八个多模态推理基准上实现 4.4%–17.5% 的相对提升，并将感知错误减少 30.5%（Figure 1, Table 1）。

## 核心创新

PAPO 的根本创新在于**将视觉感知激励直接嵌入 RLVR 优化目标**，而非依赖外部标注或奖励模型。其核心洞察是：多模态推理的主要瓶颈并非逻辑或计算能力，而是视觉感知薄弱——手动错误分析显示，GRPO 训练后模型的失败案例中 **67% 源于感知错误**（Figure 1）。基于此，PAPO 在 GRPO/DAPO 的优化目标中引入两个关键 changed slots，迫使模型在强化学习过程中同时学会“看”和“推理”。

### 1. Implicit Perception Loss（KL_prcp）：视觉信息依赖的量化与激励

GRPO 和 DAPO 的优化目标仅包含奖励信号和 KL 惩罚，缺乏对视觉感知的显式信号。PAPO 新增 **Implicit Perception Loss**（$KL_{prcp}$），其机制如下：

- **构造对比输入**：对原始图像 $I$ 施加随机 patch 掩蔽（默认掩蔽比例 0.6），生成受损视觉输入 $I_{mask}$（Figure 2）。
- **量化视觉依赖**：定义感知比率 $r^{prcp}(\theta) = \frac{\pi_{\theta}(o \mid q, I)}{\pi_{\theta}(o \mid q, I_{mask})}$，衡量模型输出在完整视觉与受损视觉条件下的概率变化。比率越高，说明模型越依赖视觉信息生成当前响应。
- **最大化信息增益**：通过最大化原始策略 $\pi_{\theta}$ 与掩蔽策略 $\pi_{\theta}^{mask}$ 之间的 KL 散度 $\mathbb{D}_{KL}[\pi_{\theta} || \pi_{\theta}^{mask}]$，迫使模型充分利用视觉信息。实用实现为 $r_i^{prcp}(\theta) - \log r_i^{prcp}(\theta) - 1$（Section 3.2）。

这一设计的精妙之处在于**无需任何外部感知标注或奖励模型**：KL_prcp 通过对比视觉输入的信息增益，自动奖励那些“视觉扎实”的生成。消融实验证实，随机掩蔽策略优于语义感知掩蔽，掩蔽比例 0.6 提供最佳性能（Table 3）；KL_prcp 权重 $\gamma$ 在 0.02 左右最优，过高（0.04）则导致模型崩溃（Table 4）。

### 2. Double Entropy Loss：防止 KL_prcp Hacking 的稳定化正则

KL_prcp 作为一个无上界的目标，在较大模型（7B）或高 $\gamma$ 设置下容易发生 **KL_prcp hacking**——模型通过极端放大原始策略与掩蔽策略的差异来获取高 KL 散度，而非真正提升视觉感知，最终导致训练崩溃（Figure 4, DAPO-7B 后期表现）。

PAPO 引入 **Double Entropy Loss** 解决这一问题：同时对原始策略 $\pi_{\theta}$ 和掩蔽策略 $\pi_{\theta}^{mask}$ 的输出序列施加熵惩罚 $\mathcal{H}[\pi_{\theta}] = \log \pi_{\theta}(o \mid q, I)$ 和 $\mathcal{H}[\pi_{\theta}^{mask}] = \log \pi_{\theta}(o \mid q, I_{mask})$，防止策略分布过度尖锐化（Section 3.2）。

对比实验表明，Double Entropy Loss 是阻止 KL_prcp hacking 并保持性能增益的最有效正则化方法，优于增加参考 KL 惩罚或单熵正则（Table 5, Figure 5）。在 Qwen2.5-VL-7B 上，Double Entropy Loss 使 PAPO_G 相对 GRPO 整体提升 4.4%，而其他正则化策略虽能防止崩溃，但增益较小。

### 3. 与 Baseline 的架构差异总结

PAPO 仅修改优化目标，不改变模型架构、训练数据、奖励函数或采样空间，可作为 GRPO（Shao et al., 2024）或 DAPO（Yu et al., 2025）的直接替代。完整目标 $\mathcal{T}_{PAPO_G}(\theta)$ 在 GRPO 的裁剪优势估计和参考 KL 惩罚基础上，整合了 Implicit Perception Loss 和 Double Entropy Loss（Equation 2）。这一设计使得 PAPO 在八个多模态推理基准上相对 GRPO/DAPO 平均提升 4.4%–17.5%，在强视觉依赖任务上提升 8.0%–19.1%，并将感知错误减少 30.5%（Table 1, Figure 1）。

## 整体框架

![[assets/figures/papers/paper_list_l43_https_openreview_net_forum_id_izbBqTL8vb/figures/002_Figure_2.jpg]]
*Figure 2: Illustration of the $\mathbf { P A P O } _ { G }$ objective, which extends GRPO by adding the Implicit Perception Loss ( ${ \mathrm { K L } } _ { \mathrm { p r c p } }$ ) . Additional Double Entropy Loss regularization ( $\check { H } [ \pi _ { \theta }$ ] , $\check { H } [ \pi _ { \theta } ^ { m a s k }$ ] ) can be added for enhancing training stabilities. The ${ \mathrm { K L } } _ { \mathrm { p r c p } }$ is formulated as maximizing the difference between the original policy $\pi _ { \theta }$ and a corrupted policy $\pi _ { \theta } ^ { \mathrm { m a s k } }$ , computed with a masked visual input. Intuitively, PAPO encourages the model to produce visually grounded responses while still achieving high...

PAPO在标准RLVR流程中引入感知感知机制，其核心思想是通过对比完整视觉输入与受损视觉输入下的策略差异，迫使模型在推理过程中主动利用视觉信息。整个框架由三个关键模块构成：**视觉输入掩蔽**、**隐式感知损失（Implicit Perception Loss, KL_prcp）** 和**双熵正则（Double Entropy Loss）**，它们协同工作以在优化目标层面激励视觉扎实的生成。

### 输入输出流

PAPO的输入输出流遵循RLVR的标准范式，但在前向传播阶段引入了关键的分叉：

1. **原始路径**：给定问题 $q$ 和完整图像 $I$，当前策略 $\pi_{\theta}$ 生成响应序列 $o$，用于计算标准的GRPO/DAPO奖励信号和优势估计。
2. **掩蔽路径**：对同一图像 $I$ 施加随机patch掩蔽，生成受损视觉输入 $I_{\text{mask}}$。掩蔽后的图像同样通过策略 $\pi_{\theta}$ 前向传播，获得在视觉信息缺失条件下的输出概率分布 $\pi_{\theta}^{\text{mask}}$。

两条路径共享同一策略参数，仅在视觉输入上产生差异。这种设计使得模型无需外部标注或奖励模型即可量化其对视觉信息的依赖程度。

### 模块关系

三个模块在优化目标中以加性项的形式整合，形成完整的PAPO目标函数（公式详见方法谱系）：

- **Implicit Perception Loss (KL_prcp)** 是核心驱动力。它通过最大化 $\pi_{\theta}$ 与 $\pi_{\theta}^{\text{mask}}$ 之间的KL散度，以感知比率 $r^{\text{prcp}}(\theta) = \frac{\pi_{\theta}(o \mid q, I)}{\pi_{\theta}(o \mid q, I_{\text{mask}})}$ 量化模型对视觉信息的依赖。当模型在完整图像下对正确推理路径的概率显著高于掩蔽图像时，KL_prcp提供正向奖励信号，从而激励视觉扎实的生成行为。

- **视觉输入掩蔽**模块负责构造 $I_{\text{mask}}$。实验表明，随机patch掩蔽（默认比例0.6）在简洁性和效果上均优于语义感知掩蔽和像素级高斯噪声（Table 3）。随机掩蔽以可忽略的计算开销有效移除信息性语义内容，为KL_prcp提供可靠的对比基准。

- **Double Entropy Loss** 作为稳定性正则化器，同时对原始策略 $\pi_{\theta}$ 和掩蔽策略 $\pi_{\theta}^{\text{mask}}$ 的输出序列施加熵惩罚。这一设计直接针对KL_prcp的无界增长问题：当模型学会通过极端降低掩蔽路径概率来最大化KL散度时（即KL_prcp hacking），双熵损失通过约束两条路径的确定性来防止训练崩溃。消融实验（Table 5, Figure 5）证实，双熵损失在防止崩溃的同时保留了KL_prcp的性能增益，优于增加参考KL惩罚或单熵正则。

### 与基线的集成方式

PAPO仅修改优化目标，不改变奖励函数、采样空间或模型架构，因此可作为GRPO或DAPO的直接替代（drop-in replacement）。具体而言：
- **PAPO_G** 在GRPO目标中集成KL_prcp和双熵损失，保留原有的参考KL惩罚 $\beta \mathbb{D}_{KL}[\pi_{\theta} || \pi_{ref}]$。
- **PAPO_D** 在DAPO目标中集成相同组件，利用DAPO的动态采样和裁剪策略。

这种模块化设计使得PAPO与数据增强（如NoisyRollout）等其他改进方向兼容。Table 2显示，PAPO_G与NoisyRollout的组合在Qwen2.5-VL-3B上达到最高平均准确率51.89%，验证了框架的可扩展性。

### 训练开销

PAPO引入的主要计算开销来自掩蔽路径的额外前向传播。对于3B模型，每步训练时间增加约48.8秒（约20%相对增长）。这一开销是框架当前的主要限制之一，论文未探索通过缓存或蒸馏优化该开销的可能。

## 核心模块与公式推导

### 3.1 问题形式化与GRPO基线

多模态推理任务中，给定视觉输入 $I$ 和文本问题 $q$，模型策略 $\pi_{\theta}$ 生成响应序列 $o$。GRPO（Shao et al., 2024）的优化目标为：

$$\mathcal{I}_{\mathrm{GRPO}}(\boldsymbol{\theta}) = \mathbb{E}_{[\{o_i\}_{i=1}^{G} \sim \pi_{\theta_{old}}(O \mid \boldsymbol{q}, I)]} \frac{1}{G} \sum_{i=1}^{G} \frac{1}{|o_i|} \sum_{t=1}^{|o_i|} \Big\{ \min\left[ r_{i,t}(\boldsymbol{\theta}) \hat{A}_{i,t}, \mathrm{clip}\left( r_{i,t}(\boldsymbol{\theta}), 1-\epsilon_l, 1+\epsilon_h \right) \hat{A}_{i,t} \right] - \beta \mathbb{D}_{KL}\left[ \pi_{\boldsymbol{\theta}} \big| \big| \pi_{ref} \right] \Big\}$$

其中 $\hat{A}_{i,t} = \frac{R_i - \mathrm{mean}(\mathbf{R})}{\mathrm{std}(\mathbf{R})}$ 为组归一化优势估计，$r_{i,t}(\theta)$ 为token级概率比率，$\beta$ 控制对参考策略的KL惩罚强度。该目标仅依赖奖励信号，缺乏对视觉感知质量的直接激励。

### 3.2 核心模块：Implicit Perception Loss (KL_prcp)

**动机**：错误分析表明，GRPO训练后多模态模型67%的错误源于视觉感知薄弱（Figure 1）。PAPO的核心创新在于引入**隐式感知损失**，通过对比完整视觉输入与受损视觉输入下的策略差异，迫使模型利用视觉信息进行推理。

**感知比率**：定义token级感知比率为完整图像与掩蔽图像下策略概率的比值：

$$r^{\mathrm{prcp}}(\theta) = \frac{\pi_{\theta}(o \mid q, I)}{\pi_{\theta}(o \mid q, I_{\mathrm{mask}})}$$

该比率量化了模型输出对视觉信息的依赖程度——当模型真正利用视觉内容时，掩蔽图像会导致输出概率显著下降，$r^{\mathrm{prcp}}$ 增大。

**KL_prcp实现**：Implicit Perception Loss通过最大化原始策略 $\pi_{\theta}$ 与掩蔽策略 $\pi_{\theta}^{\mathrm{mask}}$ 之间的KL散度实现：

$$\mathbb{D}_{\mathrm{KL}}[\pi_{\theta} || \pi_{\theta}^{\mathrm{mask}}] = r_i^{\mathrm{prcp}}(\theta) - \log r_i^{\mathrm{prcp}}(\theta) - 1$$

该形式等价于将感知比率代入KL散度的标准定义，计算高效且可微。KL_prcp作为奖励信号之外的正则项加入优化目标，鼓励模型生成视觉扎实的响应。

### 3.3 视觉损坏策略：随机Patch掩蔽

构造受损视觉输入 $I_{\mathrm{mask}}$ 是KL_prcp计算的关键。PAPO采用**随机patch掩蔽**：将图像划分为规则patch网格，以固定比例（默认0.6）随机选择patch并替换为零值。

相比语义感知掩蔽（优先掩盖显著物体区域）和像素级高斯噪声，随机掩蔽具有两个优势：
- **计算开销可忽略**，无需额外的显著性检测模型；
- **实证效果更优**：Table 3显示随机掩蔽@0.6在3B模型上相对提升2.97%，而语义掩蔽@0.6仅提升1.02%。

掩蔽比例在0.6-0.8范围内效果最佳——过低的掩蔽比例无法充分破坏视觉信息，过高则可能导致KL_prcp信号过弱。

### 3.4 稳定性正则化：Double Entropy Loss

**问题**：KL_prcp是一个无界目标——模型可以通过极端降低 $\pi_{\theta}^{\mathrm{mask}}$ 的概率来最大化KL散度，而非真正提升视觉利用，导致训练崩溃（KL_prcp hacking）。Figure 5和Table 4显示，在7B模型上设置 $\gamma=0.04$ 时性能骤降28.46%。

**Double Entropy Loss**：同时对原始策略和掩蔽策略的输出序列施加熵惩罚：

$$\mathcal{H}[\pi_{\theta}] = \log \pi_{\theta}(o \mid q, I), \quad \mathcal{H}[\pi_{\theta}^{\mathrm{mask}}] = \log \pi_{\theta}(o \mid q, I_{\mathrm{mask}})$$

该设计的关键在于**双侧约束**：仅对原始策略施加单熵正则虽能防止崩溃，但会削弱KL_prcp对视觉利用的激励效果；同时约束掩蔽策略则有效阻止模型通过压低 $\pi_{\theta}^{\mathrm{mask}}$ 来作弊。Table 5证实，Double Entropy Loss在Qwen2.5-VL-7B上实现最佳整体相对提升4.4%，优于增加参考KL惩罚或单熵正则。

### 3.5 完整目标：PAPO_G

整合上述模块，PAPO_G的完整优化目标为：

$$\mathcal{T}_{\mathrm{PAPO}_G}(\theta) = \mathbb{E}_{[\{o_i\}_{i=1}^{G} \sim \pi_{\theta_{old}}(O \mid q, I)]} \frac{1}{G} \sum_{i=1}^{G} \frac{1}{|o_i|} \sum_{t=1}^{|o_i|} \Big\{ \min\left[ r_{i,t}(\theta) \hat{A}_{i,t}, \mathrm{clip}\left( r_{i,t}(\theta), 1-\epsilon_l, 1+\epsilon_h \right) \hat{A}_{i,t} \right] - \beta \mathbb{D}_{KL}\left[ \pi_{\theta} \big| \big| \pi_{ref} \right] + \gamma \mathbb{D}_{\mathrm{KL}}\big[ \pi_{\theta} \big| \big| \pi_{\theta}^{\mathrm{mask}} \big] - \eta_1 \mathcal{H}\big[ \pi_{\theta} \big] - \eta_2 \mathcal{H}\big[ \pi_{\theta}^{\mathrm{mask}} \big] \Big\}$$

其中：
- $\gamma$ 控制Implicit Perception Loss的权重（最优值约0.02）；
- $\eta_1, \eta_2$ 分别控制原始策略和掩蔽策略的熵惩罚强度；
- 其余符号与GRPO目标一致。

PAPO_D变体在DAPO（Yu et al., 2025）框架上应用相同的KL_prcp和Double Entropy Loss，移除DAPO原有的值模型和参考KL惩罚，保持动态采样与裁剪策略。

**关键机制**：PAPO仅修改优化目标，不依赖外部标注或奖励模型，可作为GRPO/DAPO的直接替换。训练开销增加约20%（3B模型每步额外48.8秒），源于掩蔽输入的前向传播计算。

## 实验与分析

### 核心发现：感知瓶颈与PAPO的全局性能

手动错误分析揭示了一个关键瓶颈：在多模态推理任务中，使用标准GRPO训练的模型，**67%的错误源于感知失败**，而非逻辑推理或计算错误（Figure 1）。PAPO正是针对这一瓶颈设计，通过在强化学习目标中引入隐式感知损失，迫使模型在生成过程中依赖视觉信息。

![[assets/figures/papers/paper_list_l43_https_openreview_net_forum_id_izbBqTL8vb/figures/001_Figure_1.jpg]]
*Figure 1: Comprehensive error-type breakdown and inference example between GRPO and PAPO. We observe that perception errors account for the majority (67%) of failures in current multimodal reasoning models trained with GRPO. PAPO significantly reduces the dominant perception-driven errors by 30.5%, with the reduced portion indicated in gray. On the right, we present an inference example illustrating how enhanced perception enables better reasoning*

在八个多模态推理基准上的实验表明，PAPO相对于GRPO和DAPO取得了系统性提升。以Qwen2.5-VL-3B为基础模型，PAPO_G（基于GRPO的变体）实现了**49.92%的平均准确率**，相对GRPO的47.92%提升**4.36%**；以Qwen2.5-VL-7B为基础模型，PAPO_D（基于DAPO的变体）达到**63.16%**，相对DAPO的55.01%提升**17.54%**（Table 1）。

![[assets/figures/papers/paper_list_l43_https_openreview_net_forum_id_izbBqTL8vb/figures/004_Table_1.jpg]]
*Table 1: Performance (avg@8 acc %) comparison of Qwen2.5-VL and Qwen3-VL models between GRPO, DAPO and PAPO on general and more vision-dependent multimodal reasoning tasks. MathVerseV refers to the vision-centric subset of MathVerse (Zhang et al., 2024). $\Delta _ { r e l } ^ { \% }$ indicates the averaged relative gain over the baseline for each task. We observe consistent improvements against both GRPO and DAPO, with gains approaching 8%-19%, especially on tasks with high vision-dependency. Training dynamics for these models are compared in Figure 4*

更重要的是，PAPO的增益在**视觉依赖性强的任务上更加显著**。在该子集上，PAPO_G（7B模型）相对GRPO提升**7.96%**（59.37% vs 54.11%），PAPO_D（7B）相对DAPO提升**19.09%**（58.74% vs 49.33%）。这一模式直接验证了PAPO的因果机制：通过KL_prcp激励视觉信息的利用，模型在高视觉依赖场景下获得更大收益。

训练动态曲线（Figure 4）进一步证实了PAPO的优势：从训练早期开始，PAPO的准确率奖励就持续高于基线。值得注意的是，DAPO-7B在训练后期出现**模型崩溃**，而PAPO_D通过Double Entropy Loss维持了稳定训练并持续改善。

![[assets/figures/papers/paper_list_l43_https_openreview_net_forum_id_izbBqTL8vb/figures/006_Figure_4.jpg]]
*Figure 4: Comparison of the training dynamics on the accuracy reward. Solid lines indicate running averages with a stepping window size of 20. PAPO demonstrates consistently faster learning from the early stages on both GRPO and DAPO. Notably, DAPO-7B suffers from model collapse in the later stages, whereas $\mathrm { P A P O } _ { D }$ achieves continued improvements without collapse, highlighting the effectiveness of the proposed Double Entropy regularization. Further analysis on regularizing the DAPO baseline is presented in Appendix H*

### 消融实验：掩蔽策略与损失权重

**掩蔽策略选择**（Table 3）：PAPO需要构造受损视觉输入 $I_{\text{mask}}$ 来计算KL_prcp。实验对比了随机patch掩蔽和语义感知掩蔽（优先掩盖包含显著物体的patch）。结果表明，**随机掩蔽在掩蔽比例0.6时表现最优**：3B模型上相对提升2.97%，7B模型上相对提升4.36%，均优于语义掩蔽。这一反直觉结果的可能解释是：语义掩蔽可能泄露了“哪些区域重要”的先验信息，反而削弱了迫使模型主动利用全部视觉信号的效果。掩蔽比例过低（0.4）不足以充分破坏视觉信息，过高（1.0，即完全掩蔽）则使任务退化为纯文本推理，均导致增益下降。

![[assets/figures/papers/paper_list_l43_https_openreview_net_forum_id_izbBqTL8vb/figures/008_Table_3.jpg]]
*Table 3: Impact of masking strategy and ratio. Performance comparison of $\mathrm { P A P O } _ { G }$ using different approaches for constructing $I _ { \mathrm { m a s k } }$ . The base model is Qwen2.5-VL. Despite its simplicity, random masking empirically outperforms semantic-aware masking. A sufficiently large masking ratio (e.g., 0.6) yields stronger performance. See details in §5.2

**KL_prcp权重 $\gamma$ 的影响**（Table 4）：在Qwen2.5-VL-3B上，$\gamma$ 从0.005逐渐增加到0.02时，性能单调提升，最高达到4.36%的相对增益。然而，当 $\gamma$ 增加到0.04时，模型经历**KL_prcp hacking**——策略通过极端放大原始策略与掩蔽策略的KL散度来“作弊”，导致训练崩溃，性能骤降28.46%。这一失效模式直接催生了Double Entropy Loss的设计。

### 训练稳定性分析：Double Entropy Loss的关键作用

KL_prcp是一个无界目标：理论上，模型可以通过让 $\pi_\theta$ 和 $\pi_\theta^{\text{mask}}$ 的输出分布完全分离来无限最大化该损失，这会导致策略熵的恶性增长和训练崩溃。Figure 5展示了这一现象：无正则化的PAPO_G（$\gamma=0.02$）在训练中迅速崩溃。

![[assets/figures/papers/paper_list_l43_https_openreview_net_forum_id_izbBqTL8vb/figures/011_Table_5.jpg]]
*Table 5: Performance comparison between the three regularization methods that successfully prevent model collapse, as shown in Figure 5. The base model is Qwen2.5-VL-7B. Among these methods, Double Entropy Loss achieves the best overall improvement of 4.4%*

实验对比了三种能防止崩溃的正则化策略（Table 5）：
- **增加参考KL惩罚**（Inc KL_ref）：通过强化对参考模型的KL约束来限制策略偏移
- **单熵损失**（Single Entropy）：仅对原始策略 $\pi_\theta$ 施加熵惩罚
- **双熵损失**（Double Entropy）：同时对 $\pi_\theta$ 和 $\pi_\theta^{\text{mask}}$ 施加熵惩罚

在Qwen2.5-VL-7B上，三种方法均成功防止了崩溃，但**Double Entropy Loss取得了最佳整体提升（4.4%）**，达到63.50%的一般任务平均准确率和59.37%的视觉依赖任务平均准确率。其优势在于：同时对两个策略施加熵约束，既防止了KL_prcp hacking，又避免了过度正则化导致的性能损失。

### 与其他改进的兼容性

PAPO仅修改优化目标，因此理论上与数据层面或奖励层面的改进正交。Table 2验证了这一点：将PAPO_G与NoisyRollout（一种数据增强策略）结合后，在Qwen2.5-VL-3B上取得了**51.89%的最高平均准确率**，超过单独使用PAPO_G（49.92%）或单独使用NoisyRollout（48.52%）。但NoisyRollout的增益在不同数据集上表现不一致，而PAPO的增益更为稳定，进一步说明优化目标层面的改进具有更广泛的适用性。

### 计算开销与局限性

PAPO的训练时间增加约**20%**，主要来自为计算KL_prcp所需的额外前向传播（在掩蔽图像上）。以3B模型为例，每步训练增加约48.8秒（Table 14）。这一开销在可接受范围内，但限制了其在更大规模模型上的直接应用。

PAPO的另一个已知局限是：在视觉依赖性极低的任务（如MMLU-Pro with dummy visual inputs，Table 13）上提升有限，表明当视觉信息本身无关紧要时，感知激励机制自然失效。这从反面验证了PAPO的作用机理。

### 关键图表摘要

- **Figure 1**：GRPO的错误中67%为感知错误；PAPO将感知错误减少30.5%，直观展示了方法针对瓶颈的有效性。
- **Table 1**：主结果表格，PAPO在八个基准上全面超越GRPO/DAPO，视觉依赖任务增益更突出。
- **Table 3**：随机掩蔽@0.6是最优的视觉破坏策略。
- **Table 4**：$\gamma=0.02$ 是最优权重，$\gamma=0.04$ 导致崩溃。
- **Table 5**：Double Entropy Loss是防止KL_prcp hacking并保持增益的最有效正则化方法。
- **Figure 4**：PAPO训练动态优于基线，DAPO-7B后期崩溃而PAPO_D保持稳定。

## 方法谱系与知识库定位

### 1. 基线对比与定位

PAPO 的核心贡献在于将多模态推理 RL 优化目标从“纯文本奖励驱动”扩展为“感知-推理联合驱动”，其直接对标的两条基线为：

- **GRPO** (Shao et al., 2024)：文本领域 RLVR 的代表性方法，通过组归一化优势估计和参考 KL 惩罚实现稳定训练。GRPO 的优化目标仅依赖答案正确性奖励信号，对视觉信息的利用完全交由模型自行学习。
- **DAPO** (Yu et al., 2025)：GRPO 的改进版，移除了值模型和参考 KL 惩罚，引入动态采样与裁剪策略以提升训练效率。DAPO 同样未包含任何显式的视觉感知激励。

PAPO 在优化目标层面进行了两个关键扩展：**Implicit Perception Loss (KL_prcp)** 和 **Double Entropy Loss**。前者通过最大化原始图像与掩蔽图像下策略的 KL 散度，将“模型是否依赖视觉信息”量化为可优化的信号；后者对两个策略同时施加熵惩罚，防止 KL_prcp 的无界增长导致训练崩溃。PAPO 可被视为 GRPO/DAPO 的直接即插即用替代方案——仅修改优化目标，不改变奖励函数、采样空间或模型架构。

### 2. 与其他改进方向的关系

PAPO 属于**优化目标层面**的改进，与以下方向的理论互补性已被初步验证：

- **数据增强视角**：如 NoisyRollout（对输入图像添加噪声以增强鲁棒性）。Table 2 显示，PAPO_G 与 NoisyRollout 结合后在部分数据集上获得额外增益（总体 AVG 从 49.92 提升至 51.89），但 NoisyRollout 单独使用时在不同任务上表现不一致。这表明感知激励与数据增强可以叠加，但数据增强的收益稳定性不足。
- **奖励建模视角**：PAPO 当前仅使用基于答案正确性的规则奖励，未引入显式的感知奖励模型。论文指出，将 KL_prcp 与基于奖励模型的显式感知奖励结合是潜在改进方向，但尚未实验验证。

### 3. 适用边界

PAPO 的有效性存在明确的适用条件：

- **视觉依赖性阈值**：在视觉依赖性极低的任务上，PAPO 的提升有限。Table 1 中，MathVerseV（视觉依赖子集）上相对提升可达 19.09%，而某些纯文本推理主导的任务上增益明显收窄。这意味着当视觉信息本身对推理贡献微弱时，强制激励视觉依赖可能无关紧要甚至引入噪声。
- **模型规模约束**：当前验证限于 Qwen2.5-VL（3B/7B）和 Qwen3-VL（2B）。在 7B 规模下，DAPO 基线后期出现训练崩溃，PAPO_D 通过 Double Entropy Loss 避免了崩溃并持续改善（Figure 4），但更大规模模型（>7B）上的行为尚未探索。
- **模型家族限制**：仅在 Qwen-VL 系列上验证，未扩展到 InternVL 等其他多模态架构。不同视觉编码器-语言模型的对齐方式可能影响 KL_prcp 的有效性。

### 4. 局限性与已知问题

- **训练开销增加约 20%**：KL_prcp 需要额外的前向传播计算掩蔽输入下的策略分布。以 3B 模型为例，每步训练增加约 48.8 秒。这是该方法的主要实用成本。
- **训练不稳定性风险**：当 KL_prcp 权重 γ 设置过高（如 0.04）时，模型会发生 KL_prcp hacking——策略通过极端放大原始与掩蔽输出的差异来“欺骗”损失函数，导致性能崩溃（Table 4，γ=0.04 时总体 AVG 下降 28.46%）。Double Entropy Loss 是目前最有效的缓解手段（Table 5），但需要精细调节 η₁/η₂ 超参数。
- **全序列施加的粗糙性**：PAPO 当前对所有 token 统一施加 KL_prcp，未区分感知相关 token 与推理/格式 token。论文明确指出，在部分 token 上选择性施加感知损失可能减少开销并避免无关 token 的负面影响，但尚未实现。
- **视觉掩蔽策略的简化性**：随机 patch 掩蔽（默认比例 0.6）虽在实验中优于语义感知掩蔽（Table 3），但其破坏信息的方式较为粗糙，可能无法精确模拟真实场景中的感知缺陷类型。

### 5. 开放问题

1. **规模化扩展**：PAPO 能否有效扩展到 7B 以上模型？更大模型的表示空间中，KL_prcp 的行为和 Double Entropy Loss 的稳定效果需要重新验证。
2. **选择性感知损失**：能否在序列中识别并仅对“需要视觉信息”的 token 施加 KL_prcp？这需要设计 token 级的视觉依赖性度量，可能通过注意力分析或梯度信号实现。
3. **与显式感知奖励的协同**：将 KL_prcp 作为内在激励与基于奖励模型的显式感知奖励结合，是否能进一步减少感知错误？两者可能捕捉不同层面的视觉扎实性。
4. **训练效率优化**：额外前向传播能否通过缓存掩蔽输入的计算图或知识蒸馏来减少？例如，在训练早期冻结掩蔽策略的部分层。
5. **跨模态泛化**：PAPO 的核心机制——通过对比完整与受损输入的信息增益来激励感知——能否迁移到视频推理、3D 场景理解或音频-视觉任务？这些模态的“掩蔽”策略需要重新设计。
6. **与架构改进的结合**：PAPO 目前仅修改优化目标，与视觉编码器改进（如更高分辨率、更强的预训练）或推理时策略（如思维链提示）的结合效果未知。

## 原文 PDF

![[paperPDFs/ICLR_2026/Perception_Aware_Policy_Optimization_for_Multimodal_Reasoning.pdf]]
