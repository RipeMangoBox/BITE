---
title: Why Does RL Generalize Better Than SFT? A Data-Centric Perspective on VLM Post-Training
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/Why_Does_RL_Generalize_Better_Than_SFT_A_Data_Centric_Perspective_on_VLM_Post_Training.pdf
project_link: null
code_link: "https://github.com/byyx666/DC-SFT"
aliases:
- DSDCSFT
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: 训练数据中的困难样本比例——通过显式过滤掉困难样本，可以直接控制模型的过拟合程度和OOD泛化水平。
primary_logic: RL之所以泛化更好，是因为它的优化过程天然地根据奖励差异隐式过滤了简单和困难样本，将学习集中在高方差的中等难度样本上。将这种数据筛选机制显式化并应用到SFT中（DC-SFT），不仅可以达到甚至超越RL的泛化能力，同时大幅提升了训练稳定性和计算效率。
claims:
- 仅用困难样本训练SFT会导致OOD性能崩溃（例如Qwen2.5-VL-7B在ImageNet-R上准确率骤降14.07%）
- 训练中等难度样本可使模型在获得ID提升的同时维持甚至改善OOD表现
- DC-SFT（SFT-EM）超越了最强RL基线GRPO的OOD泛化水平（Qwen2.5-VL-7B OOD平均准确率：62.10% vs 59.48%）
- OOD平均（ImageNet-R, ImageNet-A, Ref-L4, Lisa） 上 Accuracy = 62.10% (SFT-EM, Qwen2.5-VL-7B)
---

# Why Does RL Generalize Better Than SFT? A Data-Centric Perspective on VLM Post-Training

> [!tip] 核心洞察
> RL之所以泛化更好，是因为它的优化过程天然地根据奖励差异隐式过滤了简单和困难样本，将学习集中在高方差的中等难度样本上。将这种数据筛选机制显式化并应用到SFT中（DC-SFT），不仅可以达到甚至超越RL的泛化能力，同时大幅提升了训练稳定性和计算效率。

| 字段 | 内容 |
|------|------|
| 中文题名 | 为什么RL比SFT泛化更好？——从数据为中心的视角看VLM后训练 |
| 英文题名 | Why Does RL Generalize Better Than SFT? A Data-Centric Perspective on VLM Post-Training |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2602.10815) · [Code](https://github.com/byyx666/DC-SFT) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/image_and_video_generation |
| Method | DC-SFT (Difficulty-Curated Supervised Fine-Tuning) |
| Dataset | OOD平均（ImageNet-R, ImageNet-A, Ref-L4, Lisa）, 训练效率（ImageNet）, 训练效率（RefCOCO）, 多模态推理基准（MMMU, MathVista等） |

> [!tip] 效果简介
> - OOD平均（ImageNet-R, ImageNet-A, Ref-L4, Lisa） 上，Accuracy 62.10% (SFT-EM, Qwen2.5-VL-7B) vs 59.48% (GRPO, Qwen2.5-VL-7B) (+2.62%)。
> - 训练效率（ImageNet） 上，训练时间加速比（相对于GRPO） 4.9x (DC-SFT) vs 1x (GRPO) (+390%)。
> - 训练效率（RefCOCO） 上，训练时间加速比（相对于GRPO） 3.2x (DC-SFT) vs 1x (GRPO) (+220%)。

## 概述

视觉-语言模型（VLM）的后训练阶段通常采用监督微调（SFT）或强化学习（RL）两种范式。近期实践表明，RL在分布外（OOD）泛化能力上显著优于标准SFT，但其背后的根本原因尚不清晰。本文从一个数据中心的视角出发，揭示了这一现象的核心瓶颈：**标准SFT无法自动区分训练样本的难度，对困难样本施加无差别的大梯度更新，虽然在分布内（ID）准确率上有所提升，却导致模型过拟合到与训练域高度相关的虚假特征，从而严重损害OOD泛化性能**。

关键发现是，RL之所以泛化更好，并非源于其优化算法的内在优越性，而是因为其优化过程天然地根据奖励差异隐式过滤了样本：简单样本（奖励一致偏高）和困难样本（奖励一致偏低）产生的优势函数趋近于零，梯度贡献可忽略不计，模型更新实际上集中在高方差的中等难度样本上。这一发现构成了本文的核心洞察——**训练数据中的困难样本比例是控制过拟合程度和OOD泛化水平的关键因果旋钮**。

基于此，本文提出了一种简洁而高效的改进方法——**DC-SFT（Difficulty-Curated Supervised Fine-Tuning）**。DC-SFT在标准SFT之前显式地执行数据筛选：对每个训练提示采样多个响应，根据正确率将样本分为简单（全对）、中等（部分正确）和困难（全错）三类，然后直接剔除所有困难样本，仅保留简单和/或中等样本进行微调。

主要实验结果如下：
- 仅用困难样本训练SFT会导致OOD性能崩溃：Qwen2.5-VL-7B在ImageNet-R上准确率骤降14.07%（Table 1）。
- 训练中等难度样本可在获得ID提升（+7.26%）的同时维持甚至改善OOD表现（+1.35%）（Table 1）。
- DC-SFT（SFT-EM变体）超越了最强RL基线GRPO的OOD泛化水平：OOD平均准确率62.10% vs. 59.48%（Table 2）。
- 训练效率大幅提升：DC-SFT在ImageNet上达到GRPO的4.9倍训练速度，在RefCOCO上达到3.2倍（Figure 4）。
- 该方法在MiniCPM-V-4架构、不同模型规模（3B/7B）、全参数微调及100k大规模数据设置下均保持一致的性能优势，展现出良好的架构无关性和可扩展性。

DC-SFT以极简的修改——仅需在训练前过滤掉困难样本——实现了对RL泛化能力的超越，同时保留了SFT的训练稳定性和计算效率，为VLM后训练提供了一种高性价比的数据中心范式。

## 背景与动机

### 视觉-语言模型后训练的现状与困境

视觉-语言模型（VLM）的训练通常遵循“预训练 → 监督微调（SFT） → 强化学习（RL）”的三阶段范式。在这一范式中，后训练阶段（SFT与RL）对提升模型的指令遵循能力和任务表现至关重要。然而，近年来一个令人困惑的经验现象逐渐浮现：**在相同的基础模型和数据条件下，基于RL的后训练方法往往展现出比SFT更强的分布外（OOD）泛化能力**，但其背后的根本原因一直缺乏系统性的解释。

标准SFT的目标是最大化模型在给定输入$x$下生成标注响应$y$的条件似然，其损失函数为负对数似然：

$$\mathcal{L}_{\mathrm{SFT}}(\theta) = -\mathbb{E}_{(x,y)\sim\mathcal{D}} \sum_{t=1}^{|y|} \log \pi_{\theta}(y_t \mid x, y_{<t})$$

这一朴素目标在训练过程中**平等对待所有样本**，不区分其难度或对泛化的影响。与此相对，RL方法（如GRPO，Group Relative Policy Optimization）通过奖励信号和组内归一化优势函数，天然地对不同难度的样本施加了差异化的更新强度。具体而言，GRPO对每个提示$x$采样$G$个响应，计算组内归一化优势：

$$A^{k} = \frac{r(x, y^{k}) - \mathrm{mean}(\{r(x, y^{k})\mid k=1,2,\ldots,G\})}{\mathrm{std}(\{r(x, y^{k})\mid k=1,2,\ldots,G\}) + \delta}$$

这一机制导致：对于模型已经稳定答对的简单样本（奖励一致高）和始终答错的困难样本（奖励一致低），组内奖励方差极小，优势$A^k$趋近于零，梯度更新量几乎为零；而对于中等难度样本（有时对有时错），奖励方差大，优势信号强，成为训练中实际被优化的主体。

### 核心瓶颈：无差别训练引发的过拟合

本文的核心发现是：**标准SFT无法自动区分训练样本难度，对困难样本施加无差别的大梯度更新，虽然提升了分布内（ID）准确率，却导致模型过拟合到与训练域高度相关的虚假特征，从而严重损害OOD泛化性能。**

这一发现通过一个关键的消融实验得以验证（Figure 1b, Table 1）：将训练数据按难度分为easy（模型采样$G=8$次全对）、medium（部分对部分错）和hard（全错）三个子集，分别进行SFT训练。以Qwen2.5-VL-7B为例：

- **仅用hard样本训练**：ID性能（ImageNet）提升7.08%，但OOD性能（ImageNet-R）骤降14.07%，呈现出典型的过拟合模式；
- **仅用medium样本训练**：ID性能提升7.26%的同时，OOD性能（ImageNet-R）反而提升1.35%，实现了ID与OOD的双赢；
- **仅用easy样本训练**：ID和OOD性能变化均不显著，说明这些样本对模型已无信息增量。

这一现象揭示了问题的本质：困难样本在训练过程中产生显著更大的梯度范数（Figure 6），主导了训练动态，迫使模型学习到训练分布特有的表面关联，从而丧失泛化能力。

### RL泛化优势的数据中心化解释

基于上述观察，本文提出了一个**数据中心化（data-centric）的假说**来解释RL优于SFT泛化能力的根本原因：**RL之所以泛化更好，不是因为其优化算法本身更优越，而是因为它的奖励-优势机制天然充当了一个隐式的数据过滤器——自动忽略梯度贡献极小的easy和hard样本，将学习集中在高方差的中等难度样本上。**

这一视角将RL与SFT的泛化差异从“优化算法之争”重新定位为“数据筛选策略之别”，并引出了一个自然的问题：**能否将RL的隐式数据筛选机制显式化，直接应用于SFT，从而在保留SFT训练稳定性和计算效率的同时，获得甚至超越RL的泛化能力？**

### 本文动机与DC-SFT的提出

正是基于上述洞察，本文提出了**DC-SFT（Difficulty-Curated Supervised Fine-Tuning）**——一种简单而高效的数据筛选驱动型SFT方法。DC-SFT的核心思想是：在SFT之前，先通过响应采样对训练数据进行难度标注（easy/medium/hard三类），然后**显式过滤掉所有hard样本**，仅保留easy和/或medium样本进行标准的负对数似然微调。

这一设计的动机直接来源于对RL工作机制的逆向工程：既然RL的泛化优势源自对困难样本的隐式忽略，那么显式地剔除这些样本，SFT理应能够复现甚至超越RL的泛化表现。同时，由于DC-SFT本质上仍是标准SFT，它天然规避了RL训练的诸多痛点——如奖励设计、策略崩溃、高计算开销（需在线采样多响应）和训练不稳定性（Figure 3），从而在效率与稳定性上具备显著优势。

## 核心创新

### 1. 从隐式过滤到显式筛选：重新定义SFT的数据使用方式

本工作的根本创新在于**将RL的隐式数据过滤机制显式化并迁移到SFT流程中**。传统SFT将所有标注数据一视同仁地输入模型，忽略了样本难度对泛化能力的差异化影响。RL方法（如GRPO）之所以泛化更好，并非源于策略优化本身，而是其奖励归一化过程天然形成了一道“数据过滤器”：简单样本（所有采样响应均正确）和困难样本（所有响应均错误）产生的奖励方差为零，导致优势函数$A^k$归零，模型在这些样本上几乎不产生有效梯度更新；学习信号高度集中于奖励方差大的中等难度样本上（Figure 1a）。

DC-SFT的核心洞察在于：**这一过滤机制完全可以在SFT阶段被显式复现，无需引入RL的复杂训练框架**。通过前置的响应采样与难度标注步骤，DC-SFT在训练开始前就将数据划分为easy/medium/hard三类，然后**主动剔除hard样本**，仅保留easy和/或medium样本进行标准SFT。这一设计将SFT从一个“被动接受所有数据”的过程转变为“主动选择学习对象”的过程，从根本上改变了模型接收训练信号的分布。

### 2. 关键改动槽位：训练数据筛选策略

DC-SFT相对于标准SFT的唯一核心改动集中在**训练数据筛选策略**这一槽位上（Table 1）：

| 维度 | 标准SFT | DC-SFT |
|------|---------|--------|
| 数据使用方式 | 使用全部标注数据，不区分样本难度 | 首先生成多个响应并按正确率分类，然后显式剔除hard样本 |
| 训练集构成 | 包含easy + medium + hard | SFT-M：仅medium；SFT-EM：easy + medium |
| 学习焦点 | 被hard样本的大梯度主导（Figure 6） | 集中在中等难度样本上，与RL的隐式行为对齐 |

这一改动的精妙之处在于其**极简性与高效性**：
- **无需修改损失函数**：DC-SFT仍使用标准的负对数似然损失（Eq. 1），与现有SFT基础设施完全兼容。
- **无需RL训练**：避免了策略优化中的采样开销、KL散度约束和训练不稳定性问题。DC-SFT的训练速度在ImageNet上达到GRPO的**4.9倍**，在RefCOCO上达到**3.2倍**（Figure 4）。
- **即插即用**：数据筛选作为预处理步骤独立于下游微调配置，与LoRA和全参数微调均正交兼容（Table 5）。

### 3. 为什么剔除困难样本反而提升泛化？

这看似反直觉的设计背后有坚实的因果机制支撑。实验揭示了一个关键瓶颈：**困难样本在训练全程产生显著更大的梯度范数**（Figure 6），导致模型更新被这些样本主导。虽然这带来了分布内（ID）性能的提升，却迫使模型过拟合到训练域特有的虚假相关性上，严重损害分布外（OOD）泛化能力。仅用hard样本训练Qwen2.5-VL-7B时，ImageNet-R准确率骤降**14.07%**（Table 1），这一现象直接验证了困难样本是OOD性能崩溃的主要诱因。

DC-SFT通过**显式控制困难样本的比例**来调节过拟合程度。消融实验表明，即使仅混入**5%的hard样本**，OOD性能（ImageNet-R）也会下降**3.74%**（Figure 5），揭示了困难数据对泛化的高度敏感性。SFT-EM（保留easy+medium）在Qwen2.5-VL-7B上实现了**62.10%的OOD平均准确率**，超越GRPO的59.48%达**+2.62%**（Table 2），证明显式筛选可以比RL的隐式过滤做得更好——因为RL的过滤效果受限于奖励信号的质量和组归一化的精度，而DC-SFT的显式分类更为直接和可控。

## 整体框架

DC-SFT 的核心流程可以概括为“先诊断、后过滤、再微调”的三阶段流水线，其设计目标是将 RL 训练过程中隐式的数据筛选机制显式化，从而在标准 SFT 范式下复现甚至超越 RL 的泛化能力。

### 1. 响应采样与难度标注

在训练开始前，DC-SFT 首先对训练集中的每一条提示 $x$ 进行响应采样。使用当前初始模型以温度 0.9、top-p=1.0 的参数生成 $G=8$ 个独立响应，并根据这些响应的正确性将样本划分为三个难度类别：

- **Easy（简单）**：所有 $G$ 个响应均正确。
- **Hard（困难）**：所有 $G$ 个响应均错误。
- **Medium（中等）**：响应中既有正确也有错误。

这一分类机制直接对应了 RL 训练中的奖励方差特征——简单样本的奖励一致为高、困难样本的奖励一致为低，两者均产生接近于零的优势函数，而中等难度样本则因奖励高方差而主导梯度更新（参见 Figure 2a）。

### 2. 数据过滤

基于上述难度标签，DC-SFT 对训练集进行显式过滤。论文提出两种核心变体：

- **SFT-M**：仅保留 medium 样本进行训练，直接模拟 RL 对中等难度数据的隐式聚焦行为。
- **SFT-EM**：保留 easy 和 medium 样本，仅剔除 hard 样本。这是最终推荐的最强变体，在保留更多有效训练信号的同时，阻断了困难样本对泛化能力的破坏性影响。

消融实验表明，即使仅混入 5% 的 hard 样本，OOD 性能（ImageNet-R）也会下降 3.74%（Figure 5），验证了过滤 hard 样本的必要性。

### 3. 监督微调

在筛选后的数据子集上，DC-SFT 执行标准的监督微调，优化负对数似然损失函数：

$$\mathcal{L}_{\mathrm{SFT}}(\theta) = -\mathbb{E}_{(x,y)\sim\mathcal{D}} \sum_{t=1}^{|y|} \log \pi_{\theta}(y_t \mid x, y_{<t})$$

此阶段与标准 SFT 在算法层面完全一致，唯一的区别在于训练数据的构成。所有方法共享相同的 LoRA 配置（rank=32, alpha=64）、优化器、学习率调度和批量大小，确保性能差异仅归因于数据筛选策略。

### 4. 输入输出流

- **输入**：原始标注数据集 $\mathcal{D} = \{(x_i, y_i)\}$，其中 $x_i$ 为视觉-语言提示，$y_i$ 为参考答案。
- **中间产物**：经难度标注和过滤后的训练子集 $\mathcal{D}_{\text{filtered}}$（仅包含 easy/medium 样本）。
- **输出**：微调后的视觉-语言模型参数 $\theta^*$。

### 5. 与 RL 流程的结构性对比

DC-SFT 的流水线设计本质上将 GRPO 的隐式过滤机制（通过组内奖励归一化使 easy/hard 样本的优势函数归零）转化为显式的预处理步骤。这一转化带来了两个关键优势：

- **训练效率**：DC-SFT 无需在线采样多个响应、计算奖励和优势函数，训练时间相比 GRPO 加速 3.2×–4.9×（Figure 4）。
- **训练稳定性**：显式过滤避免了 RL 训练中常见的奖励波动和策略崩溃问题，DC-SFT 的性能曲线更为平滑（Figure 3）。

### 补充图表

![[assets/figures/papers/paper_list_l2668_https_arxiv_org_abs_2602_10815/figures/001_Figure_1.jpg]]
*Figure 1: (a) RL implicitly focuses updates on medium-difficulty samples that yield high reward variance. (b) ID and OOD performance after SFT on data subsets of varying difficulty levels*

## 核心模块与公式推导

### 3.1 监督微调（SFT）损失

标准SFT的目标是最大化给定输入 $x$ 下生成目标响应 $y$ 的条件似然。其优化目标为负对数似然损失：

$$
\mathcal{L}_{\mathrm{SFT}}(\theta) = -\mathbb{E}_{(x,y)\sim\mathcal{D}} \sum_{t=1}^{|y|} \log \pi_{\theta}(y_t \mid x, y_{<t})
$$

其中 $\pi_{\theta}$ 为参数 $\theta$ 下的模型策略，$(x,y)$ 为训练数据集 $\mathcal{D}$ 中的标注样本，$y_t$ 为第 $t$ 个token，$y_{<t}$ 表示前序token序列（Eq. (1)）。

### 3.2 强化学习（RL）后训练目标

在RL后训练框架中，模型被视作策略 $\pi_{\theta}$，token生成过程被建模为马尔可夫决策过程（MDP）。其核心目标是最大化期望累积奖励：

$$
J_{\mathrm{RL}}(\theta) = \mathbb{E}_{x\sim\mathcal{D}, y\sim\pi_{\theta}(\cdot|x)} [r(x, y)]
$$

其中 $r(x, y)$ 为奖励函数，评估生成响应 $y$ 的质量（Eq. (2)）。为防止策略过度偏离参考模型 $\pi_{\theta_{\mathrm{ref}}}$，实际优化中引入KL散度惩罚项：

$$
\mathcal{L}_{\mathrm{RL}}(\theta) = -J_{\mathrm{RL}}(\theta) + \beta \mathbb{D}_{\mathrm{KL}}(\pi_{\theta}(\cdot|x) \parallel \pi_{\theta_{\mathrm{ref}}}(\cdot|x))
$$

其中 $\beta$ 为KL惩罚系数（Eq. (3)）。

### 3.3 GRPO目标函数

GRPO（Group Relative Policy Optimization）作为代表性RL基线，其目标函数为：

$$
\mathcal{I}_{\mathrm{GRPO}}(\theta) = \frac{1}{G} \sum_{k=1}^{G} \frac{1}{|y^{k}|} \sum_{t=1}^{|y^{k}|} \min\{r_{t}^{k}(\theta) \cdot A^{k}, \mathrm{clip}(r_{t}^{k}(\theta), 1-\epsilon, 1+\epsilon) \cdot A^{k}\}
$$

其中 $G$ 为每组采样响应数量，$r_t^k(\theta)$ 为第 $k$ 个响应的概率比，$A^k$ 为组内归一化优势函数（Eq. (4)）。

### 3.4 组内归一化优势

GRPO的核心机制在于通过组内奖励归一化计算优势 $A^k$：

$$
A^{k} = \frac{r(x, y^{k}) - \mathrm{mean}(\{r(x, y^{k})\mid k=1,2,\ldots,G\})}{\mathrm{std}(\{r(x, y^{k})\mid k=1,2,\ldots,G\}) + \delta}
$$

其中 $\delta$ 为数值稳定常数（Eq. (5)）。**该公式是理解RL隐式数据过滤机制的关键**：当某个提示 $x$ 的所有 $G$ 个采样响应均正确（easy样本）或均错误（hard样本）时，奖励分布均匀，优势 $A^k \approx 0$，导致该样本对参数更新的贡献几乎为零；只有当奖励呈现高方差时（medium-difficulty样本），非零优势才会驱动实质性梯度更新。这构成了RL天然聚焦中等难度样本的数学基础。

### 3.5 DC-SFT：难度筛选机制

DC-SFT将上述隐式过滤机制显式化为数据预处理步骤。其核心模块包括：

1. **响应采样与难度标注**：对每个训练提示 $x$，使用当前模型以温度0.9、top-p=1.0采样 $G=8$ 个响应。若全部正确则标注为**easy**，全部错误标注为**hard**，否则标注为**medium-difficulty**（Section 4.1, Figure 2a）。

2. **数据过滤**：排除所有hard样本，仅保留easy及/或medium样本构成筛选后的训练集。两个主要变体：
   - **SFT-M**：仅保留medium-difficulty样本，直接模拟RL的数据过滤行为
   - **SFT-EM**：保留easy与medium样本，在保留更多训练信号的同时避免hard样本的过拟合风险

3. **监督微调**：在筛选后的数据子集上执行标准SFT，优化Eq. (1)中的负对数似然损失。该步骤与标准SFT在优化算法上完全一致，差异仅在于训练数据的构成。

**关键机制**：hard样本在训练全程产生显著更大的梯度范数（Figure 6），导致其主导训练动态并引发对训练域虚假特征的过拟合。DC-SFT通过前置过滤截断了这一有害梯度信号的来源，从而在保持ID性能提升的同时保护OOD泛化能力。

### 补充图表

![[assets/figures/papers/paper_list_l2668_https_arxiv_org_abs_2602_10815/figures/002_Figure_2.jpg]]
*Figure 2: (a) Illustrative examples of the data difficulty taxonomy. (b) Illustrative examples of generalization evaluation benchmarks for image classification (top) and visual grounding (bottom)*

![[assets/figures/papers/paper_list_l2668_https_arxiv_org_abs_2602_10815/figures/010_Figure_6.jpg]]
*Figure 6: Gradient norms observed during SFT training on data subsets of varying difficulty*

## 实验与分析

### 核心瓶颈：困难样本主导训练并损害泛化

标准SFT的根本问题在于其损失函数（Eq. 1）对所有训练样本施加无差别的负对数似然优化。当训练数据中同时包含不同难度的样本时，困难样本（模型对提示生成的所有响应均错误）在训练全程产生显著更大的梯度范数（**Figure 6**），从而主导了模型的更新方向。这导致模型虽然能有效记忆困难样本中的模式，在分布内（ID）测试集上获得提升，却过拟合到与训练域高度相关的虚假特征，严重损害分布外（OOD）泛化能力。

**Table 1** 中的实验直接验证了这一假说。以Qwen2.5-VL-7B为基座，仅使用困难子集进行SFT后，ImageNet准确率提升7.08个百分点，但ImageNet-R准确率骤降14.07个百分点——这是一个典型的过拟合信号。相反，使用中等难度子集训练时，模型在获得7.26个百分点的ID提升的同时，ImageNet-R准确率反而上升1.35个百分点，实现了ID与OOD性能的同步改善。

### DC-SFT主结果：超越RL的泛化与效率

基于上述发现，DC-SFT通过显式过滤困难样本，将SFT的优化焦点集中到中等难度（及简单）样本上。**Table 2** 展示了完整的性能对比。在Qwen2.5-VL-7B上，SFT-EM变体（保留简单+中等样本）在四个OOD基准（ImageNet-R、ImageNet-A、Ref-L4、Lisa）上的平均准确率达到62.10%，显著超越最强RL基线GRPO的59.48%（+2.62个百分点），同时ID准确率（ImageNet 89.02%）也高于GRPO（87.66%）。SFT-M变体（仅保留中等样本）以60.41%的OOD平均准确率同样超越GRPO，且ID准确率达到88.22%。

![[assets/figures/papers/paper_list_l2668_https_arxiv_org_abs_2602_10815/figures/005_Table_2.jpg]]
*Table 2: ID and OOD (gray background) performance (%) of different post-training paradigms on image classification and visual grounding. Bolded indicates the best, and underline indicates the second-best. Performance improvement is calculated relative to standard SFT*

在训练效率方面，DC-SFT的优势更为突出。**Figure 4** 显示，在ImageNet上DC-SFT的训练时间仅为GRPO的约1/4.9（约4.9倍加速），在RefCOCO上约为1/3.2（约3.2倍加速）。这一效率优势源于DC-SFT无需维护参考模型、无需对每个提示采样多个响应用于组内奖励归一化，也无需计算KL散度惩罚项。

![[assets/figures/papers/paper_list_l2668_https_arxiv_org_abs_2602_10815/figures/007_Figure_4.jpg]]
*Figure 4: Training time comparison of Qwen2.5-VL-7B on ImageNet and RefCOCO*

### 跨架构与跨规模的泛化验证

为排除方法对特定模型架构的过拟合，作者在MiniCPM-V-4上复现了全部实验。**Table 3** 显示，SFT-M在MiniCPM-V-4上的OOD平均准确率为59.63%，与GRPO（59.22%）相当，且ID准确率（ImageNet 88.82%）显著高于GRPO（86.76%）。这一结果验证了DC-SFT的架构无关性。

![[assets/figures/papers/paper_list_l2668_https_arxiv_org_abs_2602_10815/figures/006_Table_3.jpg]]
*Table 3: ID and OOD (gray background) performance (%) of different post-training paradigms for MiniCPM-V-4*

在数据规模扩展性方面，**Table 4** 报告了使用100k训练样本时的性能。SFT-M在Qwen2.5-VL-7B上的OOD平均准确率为61.28%，依然超越GRPO的59.28%，表明DC-SFT的过滤策略在大规模数据下同样有效。

![[assets/figures/papers/paper_list_l2668_https_arxiv_org_abs_2602_10815/figures/008_Table_4.jpg]]
*Table 4: ID and OOD (gray background) performance (%) of different post-training paradigms with 100k training samples*

在全参数微调设置下（**Table 5**），SFT-M的ImageNet-R准确率为34.10%，显著优于标准SFT的28.38%，说明困难样本过滤的效果与微调方式（LoRA或全参数）正交，并非LoRA低秩约束的副产物。

![[assets/figures/papers/paper_list_l2668_https_arxiv_org_abs_2602_10815/figures/009_Table_5.jpg]]
*Table 5: ID and OOD (gray background) performance (%) of different post-training paradigms using full-parameter training*

### 困难样本的剂量-效应关系

**Figure 5** 展示了向训练数据中逐步混入困难样本对OOD性能的影响。实验表明，即使仅混入5%的困难样本，ImageNet-R准确率即下降3.74个百分点。随着困难样本比例的增加，OOD性能呈现单调递减趋势。这一发现揭示了困难样本对泛化的破坏性具有极低的“安全剂量”阈值，进一步支持了DC-SFT完全剔除困难样本的设计选择。

### 训练稳定性分析

**Figure 3** 绘制了不同后训练范式在训练过程中的性能曲线。标准SFT的OOD性能曲线呈现早期上升后迅速下降的“过拟合峰”形态，而GRPO和DC-SFT的OOD曲线则更为平稳，在训练全程保持相对稳定的泛化水平。DC-SFT的ID曲线上升速度与标准SFT相当，但不会以牺牲OOD为代价，展现出更优的ID-OOD权衡特性。

### 推理任务上的表现

除图像分类和视觉定位外，作者还在多模态推理基准上评估了DC-SFT。**Table 6** 显示，在MMMU、MathVista等多个推理任务的平均准确率上，SFT-M达到55.32%，优于标准SFT的53.88%，且与GRPO（55.44%）基本持平。这表明困难样本过滤策略不仅适用于感知类任务的泛化，对推理能力同样具有正向影响。

![[assets/figures/papers/paper_list_l2668_https_arxiv_org_abs_2602_10815/figures/012_Table_6.jpg]]
*Table 6: Reasoning performance (%) of models built using different post-training paradigms. We only assess multiple-choice questions to ensure an objective evaluation. Bolded indicates the best*

### 局限性

当前实验验证主要基于Qwen2.5-VL和MiniCPM-V-4两种架构，且模型规模限制在≤7B参数。该方法在更大规模模型（如30B+）及其他VLM架构（如InternVL、LLaVA）上的有效性尚待验证。此外，数据难度的定义依赖于特定的采样温度（0.9）和组大小（G=8），该定义对超参数的敏感性缺乏系统讨论。OOD泛化评估也仅限于图像分类和视觉定位两项任务，在其他视觉-语言任务上的适用性未知。

### 补充图表

![[assets/figures/papers/paper_list_l2668_https_arxiv_org_abs_2602_10815/figures/003_Table_1.jpg]]
*Table 1: ID and OOD (gray background) performance (%) after SFT on data subsets of varying difficulty levels. The baseline denotes the performance of the initialized model without subsequent fine-tuning. Performance changes exceeding 1% are highlighted in color*

![[assets/figures/papers/paper_list_l2668_https_arxiv_org_abs_2602_10815/figures/004_Figure_3.jpg]]
*Figure 3: Performance curves of different post-training paradigms using Qwen2.5-VL-7B as the backbone*

![[assets/figures/papers/paper_list_l2668_https_arxiv_org_abs_2602_10815/figures/011_Figure_5.jpg]]
*Figure 5: The impact of hard data ratio on OOD performance*

## 方法谱系与知识库定位

### 1. 与基线方法的关系定位

**DC-SFT** 的核心贡献在于揭示并显式化了一个此前被忽略的机制：强化学习（RL）在后训练中的泛化优势，本质上源于其对训练数据的**隐式难度过滤**。这一发现将 SFT 与 RL 的长期对立转化为统一视角下的数据策略差异。

**与 Standard SFT 的关系**：标准 SFT 平等对待所有训练样本，不区分难度。DC-SFT 的出发点正是对这一无差别训练策略的批判——标准 SFT 在提升分布内（ID）性能的同时，因无法抑制困难样本的大梯度更新而导致严重的分布外（OOD）性能退化。DC-SFT 通过显式剔除困难样本，在保留 SFT 简洁性的前提下修复了这一缺陷。

**与 GRPO 的关系**：GRPO（Group Relative Policy Optimization, Shao et al., 2024）是当前 VLM 后训练中代表性的 RL 方法，其组内奖励归一化机制（见 Eq. (5)）天然地对奖励一致的样本（全对或全错）产生零优势值，从而隐式地将更新集中在中等难度样本上。DC-SFT 的核心洞察在于：**GRPO 的泛化优势并非来自 RL 优化算法本身，而是来自这种隐式的数据筛选效应**。证据是，当 DC-SFT 显式复制这一筛选策略（SFT-M 仅保留中等难度样本，SFT-EM 保留简单+中等难度样本）后，其 OOD 泛化性能不仅匹配甚至超越了 GRPO（Table 2: Qwen2.5-VL-7B 上 SFT-EM OOD 平均 62.10% vs GRPO 59.48%），同时训练速度提升了 3.2–4.9 倍（Figure 4）。

### 2. 方法适用边界

**已验证的有效范围**：
- **模型架构**：Qwen2.5-VL（3B/7B）和 MiniCPM-V-4 两种视觉-语言模型架构上均验证有效（Table 2, Table 3），排除了架构特化效应。
- **微调方式**：LoRA（rank=32, alpha=64）和全参数微调下均有效（Table 5），说明过滤策略与微调方式正交。
- **数据规模**：从标准规模到 100k 训练样本的扩展实验中，DC-SFT 始终保持对 GRPO 的性能优势（Table 4），展现了良好的可扩展性。
- **任务类型**：图像分类（ImageNet 及其 OOD 变体 ImageNet-R、ImageNet-A）和视觉定位（RefCOCO 及其 OOD 变体 Ref-L4、Lisa）两类任务上已验证。

**已知局限与未验证边界**：
- **模型规模上限**：实验仅覆盖 ≤7B 参数模型，该方法对更大规模模型（如 30B、70B 级别）的有效性尚无证据，需要手动验证。
- **架构多样性不足**：仅在 Qwen2.5-VL 和 MiniCPM-V-4 上验证，对 InternVL、LLaVA 等其他主流 VLM 架构的泛化效果未知。
- **任务覆盖有限**：OOD 泛化评估仅覆盖图像分类和视觉定位，视觉问答、图像描述等更复杂的视觉-语言任务上的适用性尚待检验。
- **难度定义的超参数敏感性**：数据难度分类依赖于特定的响应采样参数（温度 0.9, top-p=1.0, 组大小 G=8）和二元正确性奖励标准，该定义方式对超参数选择的鲁棒性缺乏系统讨论。

### 3. 开放问题

1. **跨模态迁移性**：该数据筛选策略能否直接应用于纯文本域（如数学推理、代码生成）或其他模态（如音频、视频）的 SFT 训练？难度分类的奖励标准需要如何适配？

2. **难度分类的鲁棒性**：响应采样参数（温度、top-p、组大小 G）的变化如何影响 easy/medium/hard 的划分边界？是否存在更优的难度划分方式（例如基于连续奖励分值的软过滤）能够进一步 Push SFT 的泛化上限？

3. **大规模模型的趋势**：在更大规模（>7B）及更强预训练模型上，DC-SFT 与 RL 的泛化差距变化趋势是否一致？RL 的隐式过滤效应是否在更强模型上呈现不同特征？

4. **困难样本的潜在价值**：Figure 5 显示仅混入 5% 的困难样本即可导致 OOD 性能显著下降（ImageNet-R 降低 3.74%），但完全剔除困难样本是否意味着模型失去了处理边缘情况的能力？引入少量困难样本作为对抗训练信号，是否能在不严重损害 OOD 的同时增强模型鲁棒性？

5. **与 RL 的深层关系**：DC-SFT 证明 RL 的泛化优势可被 SFT 复现，但 RL 的探索机制（在线采样生成多样响应）是否在数据筛选之外还提供了其他隐性收益（如响应多样性、策略熵正则化）？这些因素在更大规模实验中是否变得重要？

## 原文 PDF

![[paperPDFs/CVPR_2026/Why_Does_RL_Generalize_Better_Than_SFT_A_Data_Centric_Perspective_on_VLM_Post_Training.pdf]]
