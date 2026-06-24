---
title: "Purifying Generative LLMs from Backdoors without Prior Knowledge or Clean Reference"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/Purifying_Generative_LLMs_from_Backdoors_without_Prior_Knowledge_or_Clean_Reference.pdf
openreview_forum_id: M7eWB695jp
aliases:
- IIPF
- PGLFBWPKOCR
tags:
- ICLR_2026
- topic/safety_alignment_fairness_privacy
- topic/safety_alignment_fairness_privacy/trustworthy_machine_learning
core_operator: "切断触发信号与恶意行为之间的稳定关联，而非识别具体后门触发器本身。通过构建多个合成后门变体并对比干净模型，提取共享“后门签名”，并针对性地抑制MLP中这些关联载体。"
primary_logic: "后门的本质是触发-行为关联在MLP中的冗余编码，可通过跨变体分析在没有触发器先验知识和干净参考模型的情况下定位并中和这一关联。"
claims:
- "仅移除MLP的毒化更新即可完全消除后门行为，而移除注意力更新无效。"
- "后门关联是分布式和冗余的：除非连续移除超过12个MLP块的毒化更新，否则后门持续存在；若同时移除注意力更新，仅需移除4-6个块即可消除。"
- "即使打乱MLP毒化更新在块间的顺序，后门仍能被激活，表明关联是非顺序且冗余的。"
- "Sentiment Steering / BadNets / LLaMA-2-7B-Chat (Full) 上 ASR = 2.51"
---

# Purifying Generative LLMs from Backdoors without Prior Knowledge or Clean Reference

> [!tip] 核心洞察
> 后门的本质是触发-行为关联在MLP中的冗余编码，可通过跨变体分析在没有触发器先验知识和干净参考模型的情况下定位并中和这一关联。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 无需先验知识或干净参考的生成式大语言模型后门净化 |
| 英文题名 | Purifying Generative LLMs from Backdoors without Prior Knowledge or Clean Reference |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=M7eWB695jp); [Project](https://bd-vax.github.io/) |
| Topic | #topic/safety_alignment_fairness_privacy #topic/safety_alignment_fairness_privacy/trustworthy_machine_learning |
| Method | Immunization-Inspired Purification Framework |
| Dataset | Sentiment Steering / BadNets / LLaMA-2-7B-Chat (Full), Sentiment Steering / VPI / LLaMA-2-7B-Chat (Full), Sentiment Steering / BadNets / LLaMA-2-13B-Chat (LoRA), Code Injection / BadNets / CodeLLaMA-7B-Instruct (Full) |

> [!tip] 效果简介
> - Sentiment Steering / BadNets / LLaMA-2-7B-Chat (Full) 上，ASR 为 2.51，对比 59.3 (No Defense)，变化 -56.79。
> - Sentiment Steering / VPI / LLaMA-2-7B-Chat (Full) 上，ASR 为 1.52，对比 13.68 (No Defense)，变化 -12.16。
> - Sentiment Steering / BadNets / LLaMA-2-13B-Chat (LoRA) 上，ASR 为 3.49，对比 76.73 (No Defense)，变化 -73.24。

## 概述

大语言模型在指令微调阶段容易遭受后门攻击——攻击者通过注入少量毒化样本，使模型在遇到特定触发器时产生恶意输出，而在正常输入下保持良性表现。现有防御方法通常依赖对触发器的先验知识、需要干净参考模型进行对比，或试图通过剪枝/微调直接消除后门，但这些策略在实际部署中面临信息不完整和效果不稳定的双重困境。

本文的核心发现是：**后门行为的本质是触发信号与恶意输出之间在MLP模块中的分布式、冗余关联编码**。消融实验表明，仅移除MLP层的毒化更新即可完全消除后门，而移除注意力更新则无效；此外，后门关联以非顺序、冗余的方式分布在多个MLP块中——除非连续移除超过12个块的毒化更新，否则后门持续存在。这意味着传统的头剪枝或早期层消融策略难以根除后门。

基于此洞察，本文提出一种**免疫启发的净化框架**，其核心思路不是识别具体触发器，而是切断触发-行为关联本身。方法从可疑模型出发，构造多对使用不同触发器-行为绑定的合成后门变体及其干净对照，通过跨变体差分分析提取共享的“后门签名”，并针对性地抑制MLP中承载该签名的通道，最后以少量干净样本进行轻量微调恢复生成流畅性。该框架**无需触发器先验知识，也不依赖干净参考模型**。

主要实验结果验证了方法的有效性：在LLaMA-2-7B-Chat上，针对情感转向任务的BadNets攻击，攻击成功率从59.3%降至2.51%；在CodeLLaMA-7B-Instruct的代码注入任务上，ASR从67.36%降至2.01%。在Mistral-7B等非LLaMA架构上，方法同样将ASR降至10%以下，但需额外抑制部分注意力头。跨任务迁移方面，签名具有攻击类型间的泛化性，但任务间迁移效果有限。干预比率τ≈3%在多数场景下实现帕累托最优，但最优值随模型和任务变化，部署时需针对性调优。

## 背景与动机

### 问题背景

大语言模型（LLM）在指令微调阶段面临严重的后门攻击威胁。攻击者通过在微调数据中植入触发词–恶意行为对，使模型在遇到特定触发词时输出攻击者预设的危险内容，而在正常输入下保持无害行为。形式化地，给定干净输入 $x$ 和触发词 $k$，中毒输入构造为 $x' = x \oplus_p k$，攻击目标使得：

$$\Pr_{y \sim M(\cdot | x \oplus_p k)} [y \in \mathcal{V}_b] \gg \Pr_{y \sim M(\cdot | x)} [y \in \mathcal{V}_b]$$

即触发词 $k$ 存在时，模型生成恶意行为类别 $b$ 的概率远高于无触发词情况。此类攻击涵盖情感转向、定向拒绝、代码注入等多种危险行为，对部署的 LLM 构成实质性安全威胁。

### 现有方法缺口

当前后门防御方法存在三个关键局限：

1. **依赖触发器先验知识**：多数方法需要已知触发词或通过昂贵的逆向工程猜测触发器，而实际部署中防御者通常对触发词一无所知。

2. **依赖干净参考模型**：基于权重插值或模型合并的方法需要访问未中毒的干净模型作为参考，但在第三方模型分发场景下，防御者通常只能获得可疑模型本身。

3. **后门定位粒度粗糙**：现有剪枝或微调方法要么无差别地修改模型参数导致效用退化，要么错误地聚焦于注意力头或早期层，未能触及后门关联的真正载体。

### 核心动机

本文的核心洞察源于一项关键的消融发现：**后门行为以冗余、分布式的形式编码在多个 MLP 层中，而注意力模块主要放大触发信号但并未编码触发–行为关联**。Table 1 的消融实验系统性地揭示了这一机制：

- **MLP 消融**：仅移除 MLP 的毒化更新（$\Delta W_{\text{mlp}}$）即可完全消除后门行为。
- **注意力消融**：移除注意力更新（$\Delta W_{\text{attn}}$）后，后门持续存在。
- **冗余性验证**：除非连续移除超过 12 个 MLP 块的毒化更新，否则后门持续存在；若同时移除注意力更新，仅需移除 4–6 个块即可消除。这表明后门关联是高度冗余的。
- **非顺序性验证**：即使打乱 MLP 毒化更新在块间的顺序，后门仍能被激活，进一步证实关联是非顺序且分布式的。

这些发现揭示了现有防御失效的根本原因：后门并非集中在少数关键参数中，而是以冗余关联的形式广泛分布于 MLP 层，因此简单的头剪枝或早期层消融无法根除。

### 本文动机

基于上述洞察，本文提出一种全新的防御范式：**无需识别具体触发器，而是切断触发信号与恶意行为之间的稳定关联**。核心思路借鉴免疫学原理——通过构建多个合成后门变体并对比其干净对应模型，提取跨变体共享的“后门签名”，进而定点抑制 MLP 中编码这些关联的可疑通道。该方法从根本上规避了对触发器先验知识和干净参考模型的依赖，实现了在仅有可疑模型条件下的后门净化。

## 核心创新

本工作的核心创新在于**将后门防御问题从“触发器检测”重构为“关联切断”**，并提出了一套无需触发器先验知识和干净参考模型的免疫启发式净化框架。这一重构基于对后门编码机制的因果诊断，并体现在方法设计的多个关键环节。

### 1. 因果诊断：定位后门关联的真实载体

现有防御方法通常假设后门行为集中于少量注意力头或早期层，试图通过头剪枝或浅层消融来消除后门。本工作通过系统性消融实验揭示了这一假设的局限性：

- **MLP 是后门关联的编码载体**：仅移除 MLP 模块的毒化更新（ΔW_mlp）即可完全消除后门行为；而仅移除注意力模块的毒化更新（ΔW_attn）则后门持续存在（Table 1，置信度 0.98）。这表明注意力模块主要放大触发信号，但并未编码触发-行为关联本身。
- **关联是分布式且冗余的**：除非连续移除超过 12 个 MLP 块的毒化更新，否则后门持续存在；若同时移除注意力更新，仅需 4-6 个块即可消除（Table 1，置信度 0.98）。即使打乱 MLP 毒化更新在块间的顺序，后门仍能被激活（Table 1，置信度 0.95），进一步证实关联以非顺序、冗余的方式编码。

这一诊断结论直接否定了“精确定位少量关键组件即可根除后门”的基线思路，为后续方法设计提供了因果依据：**必须系统性地抑制分布在多个 MLP 层中的冗余关联通道**。

### 2. 策略重构：从“触发器识别”到“关联签名提取”

基于上述诊断，本工作不再尝试逆向工程具体的后门触发器（基线方法如 CROW 依赖昂贵的触发器猜测），而是直接切断触发信号与恶意行为之间的稳定关联。核心思路借鉴免疫学原理：**暴露模型于同一攻击家族的多个变体，提取共享的“抗原”——即实现后门关联的共享参数变化模式**。

具体而言，方法构建多对合成后门变体（不同触发器-行为绑定），通过对比中毒微调与干净微调的参数增量之差 Δ_i，提取跨变体一致的“后门签名”。这一签名由 MLP 中同时满足两个条件的通道组成：
- **毒化强度高**（平均 L2 幅度大）；
- **跨变体对齐度高**（不同变体的 Δ_i 在该通道上方向一致）。

复合评分函数（Eq. 2）将幅度与余弦相似度加权组合，有效滤除了变体特异性噪声，仅保留稳定编码后门关联的通道。

### 3. 条件放宽：消除对先验知识和参考模型的依赖

与基线方法相比，本框架在两个关键条件上实现了根本性放宽：

| 条件 | 基线方法（如 CROW、Fine-Pruning） | 本方法 |
|------|----------------------------------|--------|
| 触发器先验知识 | 需要已知触发器或通过昂贵逆向工程猜测 | **无需任何触发器先验知识** |
| 干净参考模型 | 依赖干净参考模型或权重插值 | **无需干净参考模型**，仅在可疑模型上合成变体 |

这一放宽使得防御方可在完全不了解攻击细节的情况下部署净化，显著提升了方法的实际适用性。变体构建所需的数据仅包括少量干净样本（约 200 条）和防御方自行选择的合成触发器-行为对，不依赖对原始攻击触发器的任何假设。

### 4. 干预粒度：从“头/层剪枝”到“通道级抑制”

基线方法（如 Pruning、Fine-Pruning）通常以注意力头或整个层为粒度进行剪枝，容易过度破坏模型功能。本方法将干预粒度细化到 **MLP 通道级别**：仅抑制评分最高的 Top-τ 通道（如在 LLaMA-2-7B-Chat 全参数设置中 τ=3%），通过归零或重新初始化实现定点清除。消融实验表明，同时使用幅度和对齐的复合评分比单独使用任一指标能更好地平衡 ASR 降低和效用保持（Table 4，置信度 0.95）。

干预后辅以轻量微调（约 200 条干净样本，标准学习率），使被重置的单元恢复通用特征提取能力，确保生成流畅性和指令遵循能力不退化。这一“精准抑制 + 轻量恢复”的组合策略，在将 ASR 从 59.3% 降至 2.51% 的同时，保持了接近清洁模型的 MT-Bench 分数（Table 2、Table 3，置信度 0.95/0.9）。

---

**需人工核实**：跨任务迁移性有限（情感转向签名对拒绝任务 ASR 仍高达 84.26%），表明签名具有任务特异性，实际部署时需针对目标行为定制提取。

## 整体框架

![[assets/figures/papers/iclr26_0009_M7eWB695jp_Purifying_Generative_LLMs_from_Backdoors_without/figures/002_Figure_1.jpg]]
*Figure 1: Immunization-inspired signature extraction. Starting from a suspicious model $\theta _ { \mathrm { s u s } }$ . , we construct multiple poisoned–clean pairs $\{ \theta _ { i } ^ { \mathrm { b d } } , \theta _ { i } ^ { \mathrm { c l e a n } } \}$ with different key–behavior bindings, compute parameter updates $\Delta \theta _ { i }$ and aggregate them to isolate suspicious component based on Eq. 2. The shared high-scoring components form the backdoor signature S

### 设计动机：从冗余编码到免疫启发

后门行为在生成式LLM中的编码方式决定了防御策略的选择。通过对中毒LLaMA-2-7B-Chat的系统消融（Table 1），研究揭示了一个关键瓶颈：**后门关联以分布式、冗余的方式编码在多个MLP层中，而注意力模块主要承担触发信号的放大功能，并未编码触发-行为关联本身**。具体而言，仅移除MLP的毒化更新即可完全消除后门，而仅移除注意力更新则后门持续存在；即使打乱MLP毒化更新在块间的顺序，后门仍能被激活，进一步证实了其非顺序、冗余的编码特性。这一发现意味着，传统的头剪枝或早期层消融策略无法根除后门，必须系统性地定位并中和这些冗余分布的关联载体。

基于此，框架的核心思路发生转变：**不追求识别具体的后门触发器，而是切断触发信号与恶意行为之间的稳定关联**。借鉴免疫学原理——通过暴露于同一攻击家族的多种变体来揭示共享的“抗原”，框架通过构建多个合成后门变体并对比干净模型，提取跨变体共享的“后门签名”，进而定点清除。

### 整体流程

框架（Figure 1）以可疑模型 $\theta_{\text{sus}}$ 为唯一输入，无需触发器先验知识或干净参考模型，包含以下五个顺序模块：

1. **变体构建**：从 $\theta_{\text{sus}}$ 出发，构造 $N$ 对干净/中毒微调变体。每对变体使用不同的触发词-恶意行为绑定，确保后门关联的多样性，同时保持模型基础能力不变。

2. **差分计算**：对每对变体，计算毒化参数更新与干净更新之差：
   $$\Delta_i = \Delta\theta_i^{\mathrm{bd}} - \Delta\theta_i^{\mathrm{clean}} = \theta_i^{\mathrm{bd}} - \theta_i^{\mathrm{clean}}$$
   该差分直接等于两个模型权重的差异，捕获了纯粹由中毒数据贡献的参数变化，消除了基础模型和干净微调共性的影响。

3. **评分与签名提取**：对MLP中每个通道 $j$，计算跨变体的复合评分：
   $$s_j = \frac{1}{N} \sum_{i=1}^{N} \|\Delta_{i,j}\|_2 + \lambda \frac{2}{N(N-1)} \sum_{i<\ell}^{N} \max\{0, \cos(\Delta_{i,j}, \Delta_{\ell,j})\}$$
   第一项为平均L2幅度（毒化强度），第二项为平均正向余弦相似度（跨变体对齐度）。两者结合可识别出既被毒化强烈影响、又在不同触发词间表现一致的通道，滤除变体特异性噪声。选取Top-$\tau$ 通道构成后门签名 $\mathcal{S}$。

4. **净化干预**：对签名中的可疑通道进行抑制——全参数微调场景下重新初始化，LoRA场景下将对应低秩矩阵的行或列归零。干预粒度根据模型架构调整：LLaMA-2-7B-Chat全参数设置干预3%的MLP通道，LLaMA-2-13B-Chat干预8%；Mistral-7B等架构需额外抑制部分注意力头（Table 5）。

5. **轻量微调**：使用约200条干净样本，以标准学习率（全参数 $1\times10^{-5}$，LoRA $2\times10^{-4}$）微调5个epoch，使被重置单元恢复通用特征表示，确保生成流畅性和指令跟随能力不受损。

### 关键设计选择

- **变体数量 $N$**：消融实验（Figure 2）表明，增加 $N$ 可降低ASR，但当 $N>5$ 后改进趋缓，$N=6$ 在成本与效果间取得平衡。
- **评分组合**：同时使用幅度和对齐的复合评分（Eq.2）比单独使用任一项能更好地平衡ASR降低与效用保持（Table 4）。
- **干预比率 $\tau$**：$\tau=3\%$ 在LLaMA-2-7B-Chat上实现帕累托最优，将ASR从59.3%降至2.5%的同时保持平均准确率（Table 10）。

> **注意**：该方法目前仅在指令微调LLM上验证，且假定攻击者未采用针对免疫机制的对抗性策略。跨任务迁移能力有限——针对情感转向提取的签名对拒绝任务的净化效果明显较低（ASR 84.26%），需手动验证具体部署场景的适用性。

## 核心模块与公式推导

### 整体框架：免疫启发的后门签名提取

本方法的核心直觉来自免疫过程：将可疑模型暴露于同一攻击家族的多个变体，应当能揭示共享的“抗原”——即实现后门关联的参数变化。基于此，框架包含四个关键模块。

**模块一：变体构建。** 从可疑模型 $\theta_{\text{sus}}$ 出发，构造 $N$ 对干净/中毒微调变体。每对变体使用不同的触发器-行为绑定进行微调，中毒微调得到 $\theta_i^{\text{bd}}$，干净微调得到 $\theta_i^{\text{clean}}$。

**模块二：差分计算。** 对每对变体，计算中毒微调与干净微调相对于可疑基础模型的参数增量之差。该差分直接等价于两个模型权重的差异：

$$\Delta_i = \Delta\theta_i^{\text{bd}} - \Delta\theta_i^{\text{clean}} = (\theta_i^{\text{bd}} - \theta_{\text{sus}}) - (\theta_i^{\text{clean}} - \theta_{\text{sus}}) = \theta_i^{\text{bd}} - \theta_i^{\text{clean}}$$

其中 $\Delta_i$ 捕获了纯毒化效应，排除了干净微调引入的通用特征更新。该设计的因果逻辑是：干净微调和中毒微调共享相同的干净数据更新，相减后仅保留由毒化数据引起的参数偏移。

**模块三：评分与签名提取。** 对每个MLP通道 $j$，综合两项指标计算得分：

$$s_j = \frac{1}{N} \sum_{i=1}^{N} \|\Delta_{i,j}\|_2 + \lambda \frac{2}{N(N-1)} \sum_{i<\ell}^{N} \max\{0, \cos(\Delta_{i,j}, \Delta_{\ell,j})\}$$

- 第一项为**毒化强度**：通道 $j$ 在所有 $N$ 个变体中差分参数的平均 $L_2$ 范数，衡量该通道被毒化影响的幅度。
- 第二项为**跨变体对齐度**：所有变体对之间差分向量的平均正余弦相似度，衡量该通道在不同后门变体中的更新方向一致性。仅计入正值（$\max\{0, \cdot\}$），避免负相关拉低得分。
- $\lambda$ 为平衡系数，所有实验统一设为 $0.01$。

得分最高的前 $\tau$ 比例的MLP通道构成**后门签名** $\mathcal{S}$。复合评分的设计动机是：仅用幅度会引入变体特异性噪声，仅用对齐度则忽略毒化强度差异；二者结合能识别出既被强烈毒化又在不同变体中表现一致的关联载体。

**模块四：净化干预与轻量微调。** 对签名中的可疑通道进行抑制（全参数设置下重新初始化，LoRA设置下归零对应低秩矩阵的行或列），随后使用约200条干净样本以标准学习率（全参数 $1\times10^{-5}$，LoRA $2\times10^{-4}$）进行5轮轻量微调，恢复生成流畅性和对齐能力。

### 关键设计决策的证据支撑

消融实验（Table 1）为上述模块设计提供了因果基础：
- **仅移除MLP毒化更新**即可消除后门，而移除注意力更新无效，表明后门关联编码在MLP中。
- **后门关联是分布式和冗余的**：连续移除少于12个MLP块的毒化更新时后门持续存在，需移除12个以上才消除；若同时移除注意力更新，仅需4-6个块。这意味着无法通过简单的局部剪枝防御，必须跨层识别冗余编码的关联通道。
- 即使**打乱MLP毒化更新在块间的顺序**，后门仍能被激活，进一步证实关联是非顺序且冗余的。

## 实验与分析

### 后门编码机制：MLP 是关联载体，注意力仅放大触发信号

在开展防御之前，论文通过一系列消融实验（Table 1）揭示了后门行为在模型参数中的编码方式。核心发现是：**后门关联以分布式、冗余的形式编码在多个 MLP 层中，而注意力模块主要放大触发信号，本身并未编码触发-行为关联。**

![[assets/figures/papers/iclr26_0009_M7eWB695jp_Purifying_Generative_LLMs_from_Backdoors_without/figures/001_Table_1.jpg]]
*Table 1: Sanity check ablation studies on poisoned LLaMA-2-7B-Chat. $\Delta W _ { \mathrm { a t t } \mathrm { n } }$ & $\Delta W _ { \mathrm { m l p } }$ denote poisoned updates in attention and MLP modules, respectively. It highlights that backdoor behaviors are encoded as distributed associations in MLPs, while attention primarily amplifies trigger signals

具体证据如下：
- **MLP 消融**：将中毒模型相对于干净模型的 MLP 毒化更新 $\Delta W_{\mathrm{mlp}}$ 全部归零，后门行为被完全消除。
- **注意力消融**：仅将注意力模块的毒化更新 $\Delta W_{\mathrm{attn}}$ 归零，后门持续存在。
- **逐块消融**：除非连续移除超过 12 个 MLP 块的毒化更新，否则后门无法消除；但若同时移除注意力更新，仅需 4-6 个块即可消除。这说明 MLP 中的关联是高度冗余的。
- **打乱消融**：即使将 MLP 毒化更新在块间随机打乱顺序，后门仍能被激活，表明关联是非顺序且冗余分布的。

这一发现构成了后续防御策略的基础：**防御的关键在于切断触发信号与恶意行为之间在 MLP 中的稳定关联，而非识别具体触发器本身。**

### 主要防御效果：ASR 大幅降低，实用性保持

Table 2 展示了本文方法（Ours）与多种基线防御在攻击成功率（ASR）上的对比。在 LLaMA-2-7B-Chat 和 LLaMA-2-13B-Chat 两个模型、情感转向（Sentiment Steering）和目标拒绝（Targeted Refusal）两个任务、全参数微调和 LoRA 适配器两种威胁模型下，本文方法均取得最低 ASR：

![[assets/figures/papers/iclr26_0009_M7eWB695jp_Purifying_Generative_LLMs_from_Backdoors_without/figures/003_Table_2.jpg]]
*Table 2: Backdoor performance. Attack Success Rate (ASR, lower is better) under different defenses across two LLMs (LLaMA-2-7B-Chat, LLaMA-2-13B-Chat), two representative backdoor tasks (Sentiment Steering and Targeted Refusal), and two threat models (full-model and adapter-only). Results are reported for multiple attack types, including BadNets, VPI, Sleeper, MTBA, and CTBA*

- **LLaMA-2-7B-Chat 全参数设置**：BadNets 攻击下 ASR 从无防御的 59.3% 降至 2.51%（降低约 57 个百分点）；VPI 攻击下 ASR 从 13.68% 降至 1.52%。
- **LLaMA-2-13B-Chat LoRA 设置**：BadNets 攻击下 ASR 从 76.73% 降至 3.49%（降低约 73 个百分点）。
- **代码注入任务**（Table 8）：CodeLLaMA-7B-Instruct 全参数设置下 ASR 从 67.36% 降至 2.01%；CodeLLaMA-13B-Instruct 全参数设置下 ASR 从 55.23% 降至 3.24%。

![[assets/figures/papers/iclr26_0009_M7eWB695jp_Purifying_Generative_LLMs_from_Backdoors_without/figures/010_Table_8.jpg]]
*Table 8: Backdoor performance on code-related models. Attack Success Rate (ASR, lower is better) under the code injection task on CodeLLaMA-7B-Instruct and CodeLLaMA-13B-Instruct*

在实用性方面（Table 3），本文方法在 MT-Bench 和多项闭端基准上的表现接近干净模型，无明显退化。这表明**抑制可疑 MLP 通道不会损害模型的生成流畅性和指令遵循能力**。

与基线方法的对比中，Fine-Pruning 和 CROW 在部分场景下也能降低 ASR，但效果不稳定。例如在 LLaMA-2-7B-Chat 全参数 BadNets 设置下，Fine-Pruning 的 ASR 为 18.59%，CROW 为 21.11%，均远高于本文的 2.51%。值得注意的是，CROW 的优良表现部分可能源于其使用了异常高的学习率（1e-3）；在标准 LoRA 学习率（2e-4）下其有效性显著下降。本文所有比较均统一使用标准学习率（全参数 1e-5，LoRA 2e-4），确保公平评估。

### 消融分析：变体数量、评分策略与干预比率

**合成后门变体数量 N 的影响**（Figure 2）：ASR 随 N 增加而下降，但当 N > 5 后改进趋缓。例如在目标拒绝任务上，ASR 从 N=1 时的 40.91% 降至 N=6 时的 10.66%。这表明多个变体能有效捕捉共享的后门签名，但边际收益递减。

![[assets/figures/papers/iclr26_0009_M7eWB695jp_Purifying_Generative_LLMs_from_Backdoors_without/figures/005_Figure_2.jpg]]
*Figure 2: Effect of the number of backdoor variants N on purification performance (ASR, lower is better). Results are shown for three representative cases: BadNets on LLaMA-2-7B-Chat (Sentiment Steering), BadNets on LLaMA-2-7B-Chat (Target Refusal), and BadNets on LLaMA-2-13B-Chat (Sentiment Steering)*

**评分策略的影响**（Table 4）：同时使用幅度（L2 范数）和跨变体对齐（余弦相似度）的复合评分（Eq. 2）比单独使用幅度或对齐能更好地平衡 ASR 降低和效用保持。单独使用幅度时 ASR 为 14.47%，单独使用对齐时为 12.34%，而复合评分为 10.66%，同时平均准确率保持在 59.42%（接近干净模型的水平）。

**干预比率 τ 的影响**（Table 10）：在 LLaMA-2-7B-Chat 全参数设置下，τ=3% 实现帕累托最优——ASR 降至 2.51%，平均准确率保持在 56.90%。τ 过小（1%）时 ASR 仍高达 18.59%，τ 过大（6%）时虽 ASR 进一步降至 1.42%，但平均准确率下降至 55.56%。不同模型的最优 τ 不同（Table 5）：LLaMA-2-13B-Chat 需 8%（全参数）或 40%（LoRA），Mistral-7B-Instruct 需同时干预 2 个注意力头和 8% MLP 通道。

![[assets/figures/papers/iclr26_0009_M7eWB695jp_Purifying_Generative_LLMs_from_Backdoors_without/figures/012_Table_10.jpg]]
*Table 10: ASR (lower is better) and utility performance (average accuracy, higher is better) on LLaMA-2-7B-Chat under BadNets sentiment steering with varying intervention ratios*

### 失败模式与局限性

1. **架构依赖性**：在 Mistral-7B 上，仅抑制 MLP 不足以完全消除后门，必须同时抑制部分注意力头（Table 7, Table 9）。这表明 MLP 冗余编码的假设在不同模型系列上可能不完全成立。

2. **跨任务迁移有限**：针对情感转向任务提取的后门签名迁移到目标拒绝任务时，ASR 高达 84.26%（Table 11），说明签名具有任务特异性，无法通用。

3. **干预比率需调优**：τ 的帕累托最优值随模型和任务变化，部署时需针对具体场景进行超参数搜索。

4. **对抗鲁棒性未验证**：当前防御评估假定攻击者未采用针对免疫机制的对抗性策略，自适应攻击可能混淆跨变体的后门签名。

5. **干净数据的清洁性假设**：轻量微调阶段使用的约 200 条干净样本若被污染，可能影响最终净化效果。

## 方法谱系与知识库定位

### 与现有防御方法的关系

本文提出的免疫启发式净化框架，在防御策略上与现有后门防御方法形成了几个关键差异点，使其在生成式LLM场景中获得了不同的适用边界。

**与微调类方法（FT、Fine-Pruning）的对比。** 标准微调直接在干净数据上更新全部参数，缺乏对后门关联的定向干预。Fine-Pruning 先微调再剪枝，试图通过权重幅度识别并移除毒化神经元。然而，本文的核心发现——后门关联在MLP中以冗余、分布式方式编码——解释了为何基于幅度的剪枝效果有限：单个通道的幅度未必显著，但多个通道协同即可稳定激活后门行为。本文方法通过跨变体签名提取，直接定位这些协同通道，而非依赖单点幅度信号。

**与CROW的对比。** CROW 通过内部信号正则化抑制后门激活，在原始设置中使用异常高的学习率（1e-3）取得了较好效果。但本文在公平比较中统一使用标准学习率（全参数 1e-5，LoRA 2e-4）后发现，CROW 的有效性显著下降。这表明CROW的部分优势可能源于超参数选择，而非其正则化机制本身。相比之下，本文方法在标准学习率下仍能稳定将ASR降至个位数（Table 2），说明其净化机制对超参数的依赖较弱。

**与剪枝、量化类方法的对比。** 剪枝和量化本质上是无差别的容量压缩，缺乏对后门关联的特异性。Table 1的消融实验表明，即使打乱MLP毒化更新在块间的顺序，后门仍能被激活——这意味着后门关联不具有顺序依赖性，简单的结构化剪枝（如移除连续块）需要同时移除12个以上MLP块才能消除后门。本文方法的优势在于通过差分分析和跨变体对齐评分，实现了对后门关联通道的特异性定位。

### 适用边界与前提条件

本方法的有效性依赖于几个关键前提，这些前提同时定义了其适用边界：

1. **MLP冗余编码假设必须成立。** 在LLaMA系列模型上，后门关联确实以冗余方式编码在MLP中，注意力模块主要放大触发信号。但在Mistral-7B-Instruct上，仅抑制MLP不足以完全消除后门，必须同时抑制部分注意力头（Table 7, Table 9）。这说明该假设的成立程度因模型架构而异，在非LLaMA系列模型上部署前需要验证。

2. **合成后门变体的质量。** 方法的核心操作是从可疑模型出发，构造多对干净/中毒微调变体，通过差分计算提取共享签名。如果合成变体与原始后门在参数更新模式上差异过大，跨变体对齐评分可能无法有效捕获真实后门签名。论文未评估攻击者是否可能设计对抗性后门，使得其参数更新模式在跨变体分析中表现为噪声而非一致信号——这是一个待验证的安全边界。

3. **干净微调数据的清洁性。** 构造干净变体 $\theta_i^{\text{clean}}$ 需要使用少量干净数据对可疑模型进行微调。如果这些数据被攻击者污染，差分计算 $\Delta_i = \theta_i^{\text{bd}} - \theta_i^{\text{clean}}$ 将无法正确隔离毒化更新。论文未讨论如何确保这些干净数据的清洁性，这是实际部署中的潜在风险点。

4. **干预比率 $\tau$ 的任务依赖性。** 帕累托最优的干预比率随模型和任务变化：LLaMA-2-7B-Chat 全参数设置为3%，LLaMA-2-13B-Chat 为8%，Mistral-7B 则需额外干预注意力头（Table 5, Table 10）。这意味着每次部署可能需要针对具体模型-任务组合进行调优，增加了实际应用的工程成本。

### 已知局限

1. **跨任务迁移能力有限。** 针对情感转向任务提取的后门签名，在迁移到拒绝任务时ASR高达84.26%（Table 11），说明签名具有任务特异性。这意味着防御者需要针对每种可疑的后门行为类型分别提取签名，而非一次性净化所有潜在后门。

2. **架构依赖性。** 方法目前仅在LLaMA-2、LLaMA-3、Mistral和CodeLLaMA等基于Transformer的指令微调LLM上验证。在其他模型系列（如GPT系或非Transformer架构）上，MLP冗余编码的假设是否成立尚不清楚。

3. **对抗性鲁棒性未评估。** 防御评估假定攻击者未采用针对免疫机制的对抗性策略。攻击者可能设计后门使其参数更新在跨变体分析中表现为低一致性，从而逃避签名提取。这是一个重要的开放安全问题。

4. **轻量微调的数据依赖性。** 净化后的轻量微调步骤使用约200条干净样本恢复流畅性。如果这些样本的分布与部署场景不匹配，可能影响模型在特定领域上的生成质量。

### 开放问题

1. **自适应攻击的可行性。** 攻击者是否可以通过设计后门触发-行为关联，使其在跨变体分析中表现为不一致的噪声模式，从而逃避签名提取？这需要从对抗性机器学习的角度进行红队评估。

2. **跨架构泛化。** 在非LLaMA系列模型（如GPT-4、Claude、Gemini等）上，后门关联是否仍以MLP冗余编码为主？注意力模块的角色是否会发生变化？这决定了方法的适用范围能否扩展到更广泛的模型家族。

3. **干净数据的可信来源。** 在实际部署中，如何获取保证未被污染的小规模干净数据用于构造干净变体和轻量微调？这涉及到供应链安全和数据溯源问题。

4. **多模态与复杂行为的扩展。** 签名提取框架能否扩展至多模态LLM或代码注入之外的更复杂后门行为（如特定条件下的信息泄露、隐蔽偏好操控）？这需要重新审视“触发-行为关联”在更复杂语义空间中的编码方式。

5. **干预比率的自动化确定。** 当前 $\tau$ 需要手动调优，能否设计自动化方法（如基于验证集ASR-效用曲线的拐点检测）来确定帕累托最优干预比率？

## 原文 PDF

![[paperPDFs/ICLR_2026/Purifying_Generative_LLMs_from_Backdoors_without_Prior_Knowledge_or_Clean_Reference.pdf]]
