---
title: "What's In My Human Feedback? Learning Interpretable Descriptions of Preference Data"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/Whats_In_My_Human_Feedback_Learning_Interpretable_Descriptions_of_Preference_Data.pdf
openreview_forum_id: sC6A1bFDUt
aliases:
- WWSMHF
- WSMHFLIDPD
tags:
- ICLR_2026
- topic/safety_alignment_fairness_privacy
- topic/safety_alignment_fairness_privacy/trustworthy_machine_learning
core_operator: "引入稀疏自编码器 (SAE) 学习响应差异的可解释特征，并通过控制长度的逻辑回归将这些特征与偏好标签关联，从而识别数据集中可测量和表达出的偏好。"
primary_logic: "通过 SAE 学习的少量稀疏特征即可解释大部分偏好预测信号，且这些特征在不同数据集中表现出高度异质性，能揭示数据集的特定偏差（如安全性偏好），从而支持有效的数据整理和个性化。"
claims:
- "SAE 特征在 7 个数据集上平均捕获了黑盒奖励模型预测增益的 67%（相对于随机 AUC 0.5），仅使用平均 4 个活跃特征。"
- "在 Community Alignment 上，60.4% 的注释者解释与至少一个 SAE 活跃特征匹配，而随机特征的匹配率仅 33.3%，表明特征与人类推理高度一致。"
- "通过翻转 LMArena 中激活不安全拒绝特征的前 1000 个示例的标签，RewardBench2 安全准确率从 8.9% 大幅提升至 46.2%，且非安全性能未受损。"
- "对最主观的特征（段落 vs 列表）进行个性化，在 Community Alignment 上相比全局模型实现了 +1.1% 的保留 AUC 增益，且主动采样效率更高。"
---

# What's In My Human Feedback? Learning Interpretable Descriptions of Preference Data

> [!tip] 核心洞察
> 通过 SAE 学习的少量稀疏特征即可解释大部分偏好预测信号，且这些特征在不同数据集中表现出高度异质性，能揭示数据集的特定偏差（如安全性偏好），从而支持有效的数据整理和个性化。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 我的人类反馈里有什么？学习可解释的偏好数据描述 |
| 英文题名 | What's In My Human Feedback? Learning Interpretable Descriptions of Preference Data |
| 会议/期刊 | ICLR 2026 (Oral) |
| Links | [paper](https://openreview.net/forum?id=sC6A1bFDUt); [GitHub](https://github.com/rmovva/wimhf) |
| Topic | #topic/safety_alignment_fairness_privacy #topic/safety_alignment_fairness_privacy/trustworthy_machine_learning |
| Method | WIMHF (What's In My Human Feedback?) |
| Dataset | 7个数据集 (Arena, CA, HH-RLHF, PRISM, Reddit, PKU, Tulu), Community Alignment (解释匹配验证), RewardBench2 Safety (数据整理), Community Alignment (个性化) |

> [!tip] 效果简介
> - 7个数据集 (Arena, CA, HH-RLHF, PRISM, Reddit, PKU, Tulu) 上，AUC (偏好预测) 为 SAE 特征逻辑回归 (平均 AUC 0.672)，对比 黑盒奖励模型 (平均 AUC 0.766)，变化 捕获 67% 的奖励模型 AUC 增益（相对于随机）。
> - Community Alignment (解释匹配验证) 上，注释者解释与 SAE 特征的匹配率 为 60.4% (活跃特征)，对比 33.3% (随机非活跃特征)，变化 +27.1 个百分点。
> - RewardBench2 Safety (数据整理) 上，安全准确率 为 46.2% (翻转 top 1000 样本后)，对比 8.9% (原始模型)，变化 +37.3 个百分点。

## 概述

理解人类偏好数据是当前大语言模型对齐的核心环节，然而现有方法普遍依赖预定义的属性假设或黑盒奖励模型，难以自动揭示数据集中实际存在的、可解释的偏好结构。**WIMHF** (What's In My Human Feedback?) 针对这一瓶颈，提出了一种无需人工先验即可从偏好对比数据中自动发现可测量偏好 (measurable preferences) 与表达偏好 (expressed preferences) 的框架。

其核心思路是：首先利用稀疏自编码器 (SAE) 从响应嵌入差异中学习一组稀疏、可解释的特征，这些特征捕捉了响应对之间的一致差异（即可测量偏好）；随后，通过控制长度差异的逻辑回归，将这些特征与偏好标签关联，识别出真正影响标注选择的表达偏好及其边际效应。这一设计使得分析者能够以少量稀疏特征解释大部分偏好信号，并直接获得每个特征对胜率变化的定量估计。

在涵盖对话风格、安全性、有用性等维度的 7 个数据集上，WIMHF 展现出三方面关键能力：

1. **偏好信号的高效压缩**：SAE 特征在平均仅激活 4 个维度的情况下，捕获了黑盒奖励模型（Llama-3.2-3B 微调）相对于随机基线 67% 的 AUC 增益，表明少量可解释特征已能解释大部分偏好预测信号。
2. **特征的可解释性与人类一致性**：在 Community Alignment 数据集上，60.4% 的标注者书面解释与至少一个活跃 SAE 特征匹配，而随机非活跃特征的匹配率仅为 33.3%。外部专家评估中，100% 的特征被判定为可理解，87% 被认为对理解偏好数据有帮助。
3. **下游应用的直接赋能**：在 Chatbot Arena 中发现标注者强烈偏好模型满足不安全请求而非拒绝（该特征使胜率下降 31%），通过翻转激活该特征的前 1000 个示例标签，RewardBench2 安全准确率从 8.9% 跃升至 46.2%，且非安全性能未受损；在 Community Alignment 上针对最主观的“段落 vs 列表”特征进行个性化建模，相比全局模型实现了 +1.1% 的保留 AUC 增益。

WIMHF 的方法定位介于纯黑盒奖励模型与完全手动特征工程之间：它提供了黑盒模型所缺乏的可解释性，同时避免了人工预定义特征的主观性和覆盖盲区。相较于 Inverse Constitutional AI (Findeis et al., 2025) 等自动特征发现方法，WIMHF 在统计显著的偏好预测特征数量上表现更优（联合回归中 34/50 vs 21/50）；相较于 Embed-TopDims 和 Embed-PCA 等消融基线，SAE 产生的高保真可解释特征数量显著更多（平均 19.6 vs 12.7 vs 4.9）。

值得注意的是，WIMHF 揭示的偏好在不同数据集间存在显著异质性——例如 Reddit 和 Arena 偏好笑话与非正式语气，而 HH-RLHF 和 PRISM 则厌恶这些特征——这提示混合异质数据源进行偏好微调可能导致信号冲突，而 WIMHF 为从业者提供了一种在训练前审计和整理偏好数据的实用工具。

## 背景与动机

从人类反馈中学习偏好是当前大语言模型对齐的核心范式。然而，一个关键问题长期被忽视：**人类反馈数据本身究竟编码了哪些偏好？** 这些偏好数据集由提示分布、响应分布和标签分布三个层次共同生成，标注者可能会系统性地偏好某些风格、格式或内容特征，而这些偏好往往未被明确记录，甚至与设计者的意图相悖。

现有方法在理解和审计这些偏好时面临根本性瓶颈。一方面，依赖预定义假设的人工分析只能捕捉研究者已知的维度，无法发现数据集中隐含的、未曾预料的偏差模式。另一方面，黑盒奖励模型虽然能有效预测偏好标签，但其内部表征不可解释，无法告诉从业者“标注者到底喜欢什么”。即便使用嵌入空间的线性分类器进行偏好预测，其权重维度也难以映射到人类可理解的概念。这种可解释性的缺失使得数据集内部的系统性偏差——如对不安全内容的偏好、对特定表达风格的厌恶——长期处于不可见状态。

本文的核心洞察在于：**通过自动发现响应之间的可测量差异，并将其与偏好标签关联，可以在不依赖先验假设的前提下，揭示数据集中真正被表达出的偏好。** 具体而言，WIMHF 引入稀疏自编码器（SAE）从响应对的文本嵌入差异中学习稀疏特征，这些特征捕获了响应间一致性的可测量偏好；随后通过控制长度的逻辑回归，将每个特征与偏好标签关联，得到其边际胜率效应，即表达偏好。这一框架使得从业者能够系统性地回答“我的人类反馈数据里有什么”——哪些特征在驱动标注决策，这些特征在不同数据集中是否一致，以及它们是否与期望的对齐目标相符。

## 核心创新

WIMHF 的核心创新在于将偏好数据集的内部结构拆解为**可测量偏好**与**表达偏好**两个可操作的层次，并围绕这一概念框架构建了一套从特征发现到效应估计的自动化流水线。相比于现有方法，其关键改变体现在以下三个环节。

### 从黑盒嵌入到稀疏可解释特征

现有偏好分析方法通常依赖两类路径：要么由研究者手动预定义一组特征假设（如长度、礼貌程度），要么直接使用黑盒奖励模型的隐式表征进行预测。前者受限于先验知识的覆盖范围，后者虽然预测能力强，但无法揭示模型究竟依据何种信号做出判断。

WIMHF 将稀疏自编码器引入偏好特征学习，直接在**响应差异嵌入** $e_\Delta = e_{r_A} - e_{r_B}$ 上训练 BatchTopK SAE。这一设计的核心动机在于：响应对之间的差异向量天然编码了“哪一方在某个维度上更强”的信息，而 SAE 的稀疏性约束（$M=32, K=4$）迫使模型将高维嵌入空间压缩为少量可独立激活的特征维度。消融实验表明，这一选择是关键的——相比直接使用嵌入维度的 Embed-TopDims 或主成分的 Embed-PCA，SAE 产生的高保真特征数分别为 19.6/32、12.7/32 和 4.9/32（Table 2），且非冗余高保真特征数同样显著领先（18.0 vs 10.7 vs 4.6）。这意味着 SAE 并非简单地对嵌入空间做降维，而是学习到了一种更具语义凝聚力的特征分解方式。

### 从后验分析到自动化的特征描述与验证

传统可解释性工作往往在模型训练完成后进行人工的定性分析，缺乏系统性和可复现性。WIMHF 为每个 SAE 特征自动生成自然语言描述，并通过**保真度评分**进行统计验证：计算描述 $d_j$ 与特征激活 $Z[i,j]$ 之间的 Pearson 相关性，仅保留 Bonferroni 校正后 $p < 0.05$ 的显著特征。这一机制将“可解释性”从主观判断转化为可量化的统计检验。

外部专家评估进一步验证了该流程的有效性：在 5 个数据集的前 10 个特征中，47/47 个特征被评定为可理解，41/47 个被评定为有帮助（Table 6）。与 Inverse Constitutional AI（Findeis et al., 2025）的对比则凸显了 WIMHF 的优势：在 5 个数据集上，WIMHF 发现的统计显著偏好预测特征总数为 43/50，而 ICAI 为 28/50；在联合回归中，这一差距进一步扩大至 34/50 vs 21/50（Table 5）。这表明 SAE 学习的特征不仅更可解释，也更具预测效力。

### 从全局偏好建模到长度控制的边际效应估计

黑盒奖励模型虽然能给出高精度的偏好预测，但其内部决策过程不可追溯。WIMHF 采用控制长度差异 $\ell_\Delta$ 的逻辑回归来估计每个可解释特征 $z_j$ 对偏好标签 $y$ 的边际效应：

$$\operatorname*{Pr}(y = 1) = \sigma (\alpha + \beta_j \cdot z_j + \gamma \cdot \ell_\Delta)$$

这一设计的巧妙之处在于：$\beta_j$ 直接量化为“在控制响应长度后，特征 $z_j$ 每增加一个单位时胜率的变化”。为进一步增强可解释性，WIMHF 将连续激活二值化为 $D(z_j) \in \{+1, 0\}$，从而得到正负激活之间的平均胜率差 $\Delta\text{win-rate}$。例如，在 Chatbot Arena 中，“拒绝不安全请求”特征的 $\Delta\text{win-rate}$ 为 -31%，直观揭示了标注者系统性地偏好不安全内容而非拒绝回应（Table 1）。

长度控制本身也是方法的关键组件：消融实验表明，当移除长度控制时，类似长度本身的特征会自动浮现为表达偏好（App. A.4），这验证了控制变量对于隔离实质性偏好信号的必要性。

### 从一次性分析到可操作的下游应用

WIMHF 的创新不仅停留在分析层面，还直接支撑了两类高影响力的下游应用：

- **数据整理**：通过识别 Chatbot Arena 中激活最强的“反拒绝”特征，翻转前 1000 个示例的标签后，RewardBench2 安全准确率从 8.9% 跃升至 46.2%，且非安全性能保持在基线模型的 95% 置信区间内（Figure 3a）。这表明 WIMHF 发现的偏差特征可直接转化为数据清洗策略，无需重新收集标注。

- **个性化偏好建模**：通过混合效应模型估计每位标注者 $a$ 的特征斜率方差 $\tau_j^2$，WIMHF 识别出最具主观性的特征（如“段落 vs 列表”），并仅针对该特征学习用户特定系数。在 Community Alignment 上，仅使用 $k=16$ 条个性化数据即实现了相对于全局模型 +1.1% 的保留 AUC 增益，且主动采样策略在低 $k$ 条件下效率更高（Figure 3b）。

综上，WIMHF 的方法论贡献并非单一技术的堆砌，而是通过“SAE 特征学习 → 自动描述与验证 → 长度控制回归 → 下游干预”这一完整链条，将偏好数据从黑盒预测对象转变为了可审计、可干预、可个性化的结构化知识。

## 整体框架

WIMHF 将偏好数据的可解释分析形式化为一个三阶段流水线，其核心目标是从原始偏好对中同时提取**可测量偏好**（响应间可被量化的差异）与**表达偏好**（哪些差异实际解释了标注标签）。

### 数据生成视角下的问题定义

方法首先将偏好数据集建模为由三个分布联合生成的产物：

$$(p, r_A, r_B, y) \sim \underbrace{\Pr(p)}_{\text{(1) 提示分布}} \cdot \underbrace{\Pr(r_A, r_B \mid p)}_{\text{(2) 响应分布}} \cdot \underbrace{\Pr(y \mid r_A, r_B, p)}_{\text{(3) 标签分布}}$$

其中，提示分布决定了数据集覆盖的问题域，响应分布决定了模型可观测到的差异范围，标签分布则编码了标注者的偏好倾向。WIMHF 的设计目标正是解耦后两者：先通过无监督学习捕获响应分布中的结构（可测量偏好），再通过有监督回归识别标签分布中的信号（表达偏好）。

### 三阶段流水线

**阶段一：SAE 特征学习。** 对每个偏好对，计算两个响应的文本嵌入差 $\mathbf{e}_\Delta = \mathbf{e}_{r_A} - \mathbf{e}_{r_B}$，然后在此差异向量上训练一个 BatchTopK 稀疏自编码器（SAE）。SAE 将密集的嵌入差映射为稀疏特征矩阵 $\mathbf{z}$，每个特征维度对应一种响应间可测量的差异模式。论文在所有数据集上统一使用特征数 $M=32$、活跃特征数 $K=4$ 的配置；更大的 $M$ 或 $K$ 会导致特征冗余度上升、可解释性下降。训练时采用 Matryoshka 损失 $\mathcal{L} = \mathcal{L}_8 + \mathcal{L}_{32}$，同时优化前 8 维和前 32 维的重构，以鼓励 SAE 学习不同粒度的特征。

**阶段二：自然语言描述生成。** 对每个 SAE 特征维度，采样高激活样本，将其作为上下文提示 LLM 生成该特征的概念描述。随后通过保真度评分（fidelity score）量化描述与特征激活的一致性：

$$\mathrm{fidelity}(d_j^{(c)}) = \mathrm{corr}_{1 \leq i \leq N} \bigl( Z[i,j], \, A(r_A^{(i)}, r_B^{(i)} \mid d_j^{(c)}) \bigr)$$

其中 $A(\cdot)$ 为 LLM 根据描述 $d_j^{(c)}$ 对样本的标注结果。仅保留经 Bonferroni 校正后 $p < 0.05$ 的显著特征描述，确保产出特征具有统计可信的解释。

**阶段三：偏好回归与效应估计。** 以可解释特征 $\mathbf{z}$ 为输入，拟合逻辑回归以识别表达偏好：

$$\Pr(y = 1) = \sigma (\alpha + \beta_j \cdot z_j + \gamma \cdot \mathbf{x})$$

其中 $\mathbf{x} = \ell_\Delta$ 为两响应间的词数差，用于控制长度对偏好标签的混杂效应。系数 $\beta_j$ 直接给出特征 $z_j$ 对偏好胜率的边际效应。为便于解释，论文进一步将连续激活二值化为 $D(z_j) \in \{+1, 0\}$，得到正负激活间的平均胜率变化 $\Delta\text{win-rate}$。

### 前置处理与边界条件

在进入流水线之前，数据预处理模块负责过滤无效样本、主观标注对，并随机交换响应顺序以消除位置偏差。当前分析主要针对主观对话类数据，过滤掉了数学、编程等客观问答场景——在这些场景下，文本嵌入可能不编码正确性信息，限制了方法的适用范围。

## 核心模块与公式推导

### 1. 形式化框架：可测量偏好与表达偏好

WIMHF 将偏好数据生成过程建模为三个分布的乘积，为整个方法提供了概念基础：

$$(p, r_A, r_B, y) \sim \underbrace{\Pr(p)}_{\text{(1) 提示分布}} \cdot \underbrace{\Pr(r_A, r_B \mid p)}_{\text{(2) 响应分布}} \cdot \underbrace{\Pr(y \mid r_A, r_B, p)}_{\text{(3) 标签分布}}$$

其中 $p$ 为提示，$r_A, r_B$ 为响应对，$y$ 为偏好标签。该分解将偏好数据集的内部结构分为三层：提示如何采样、响应如何生成、标注者如何选择。基于此，方法区分两个核心概念：

- **可测量偏好 (measurable preferences)**：响应对中一致存在的差异特征，由 SAE 从文本嵌入差异中学习，代表“数据中实际存在什么变化”。
- **表达偏好 (expressed preferences)**：通过回归偏好标签 $y$ 估计哪些可测量特征实际解释了标注者的选择，代表“标注者真正在乎什么”。

### 2. 核心模块

方法流程由五个模块组成，形成从数据到应用的可解释管道：

**模块一：数据预处理**
过滤无效样本、主观标注对，控制长度并随机交换响应顺序，为 SAE 训练准备干净的偏好对。

**模块二：SAE 特征学习**
基于 BatchTopK 架构训练稀疏自编码器，将响应嵌入差异 $\mathbf{e}_\Delta = \mathbf{e}_{r_A} - \mathbf{e}_{r_B}$ 转化为稀疏特征矩阵 $\mathbf{z}$。超参数设置为 $M=32$（特征维度）、$K=4$（每个样本的活跃特征数），该配置在特异性和非冗余性之间取得平衡。训练使用 Matryoshka 损失：

$$\mathcal{L} = \mathcal{L}_8 + \mathcal{L}_{32}$$

通过同时优化前 8 维和前 32 维的重构损失，鼓励 SAE 同时学习粗粒度和细粒度的可解释特征。

**模块三：自然语言描述**
采样高激活样本，提示 LLM 生成每个特征的概念描述。通过保真度评分筛选显著可解释的特征：

$$\mathrm{fidelity}(d_j^{(c)}) = \operatorname{corr}_{1 \leq i \leq N} \bigl( Z[i,j], \, A(r_A^{(i)}, r_B^{(i)} \mid d_j^{(c)}) \bigr)$$

其中 $d_j^{(c)}$ 为候选描述，$A(\cdot)$ 为 LLM 判断该描述在哪个响应中更突出。保留经 Bonferroni 校正后 $p < 0.05$ 的特征。

**模块四：偏好回归与效应估计**
以可解释特征为输入，拟合控制长度的逻辑回归识别表达偏好：

$$\operatorname{Pr}(y = 1) = \sigma (\alpha + \beta_j \cdot z_j + \gamma \cdot \mathbf{x})$$

其中 $\mathbf{x} = \ell_\Delta$ 为两响应间的词数差，$\beta_j$ 为特征 $z_j$ 对偏好标签的边际效应。为便于解释，将连续激活二值化后直接估计胜率变化：

$$\operatorname{Pr}(y = 1) = \sigma (\alpha + \beta_j \cdot D(z_j) + \gamma \cdot \mathbf{x})$$

其中 $D(z_j)=+1$（正激活）或 $0$（负激活），$\beta_j$ 直接表示正负激活之间的平均胜率变化 $\Delta$win-rate。

**模块五：应用——数据整理与个性化**
- **数据整理**：利用发现的偏差特征（如“拒绝不安全请求”），翻转高激活样本的偏好标签以消除有害标注偏差。
- **个性化**：通过混合效应模型识别主观特征，为每位标注者 $a$ 引入随机斜率：

$$\mathrm{Pr}(y = 1) = \sigma \left( \alpha + \beta_{j,a} \cdot z_j + \gamma \cdot \ell_{\Delta} \right)$$

其中 $\beta_{j,a} \sim \mathcal{N}(\beta_j, \tau_j^2)$，$\tau_j^2$ 衡量特征的主观性程度。在此基础上，使用高斯先验学习特定标注者的偏移 $\delta_a$：

$$\operatorname{Pr}(y = 1) = \sigma \left( \alpha + (\beta + \delta_a) \cdot \mathbf{z} + \gamma \cdot \mathbf{x} \right)$$

对于人口统计群组分析，在全局效应 $\beta_j$ 之上增加群组偏移 $\delta_{j,g}$：

$$\operatorname{Pr}(y = 1) = \sigma \left( \alpha + (\beta_j + \delta_{j,g}) \cdot z_j + \gamma \cdot \mathbf{x} \right)$$

### 3. 关键设计选择

- **嵌入差异而非绝对嵌入**：SAE 训练于 $\mathbf{e}_\Delta$ 而非完整提示-响应嵌入，实验表明使用完整嵌入并未提升偏好预测性能，且差异表示直接捕获响应间的对比特征。
- **长度控制**：在所有回归中显式控制词数差 $\ell_\Delta$，以隔离非长度相关的偏好信号。移除该控制时，类似长度本身的特征会自动浮现为表达偏好。
- **稀疏性约束**：$K=4$ 的硬稀疏性确保每个样本仅激活少量特征，使得特征解释更聚焦、非冗余。

## 实验与分析

### 核心发现：稀疏可解释特征捕获偏好信号

WIMHF 在 7 个多样化数据集（Chatbot Arena、Community Alignment、HH-RLHF、PRISM、Reddit SHP、PKU-SafeRLHF、Tulu 3）上验证了其核心主张：**少量稀疏特征即可解释大部分人类偏好信号**。具体而言，SAE 特征通过控制长度的逻辑回归预测偏好标签，平均 AUC 达到 0.672，而作为上界的黑盒奖励模型（Llama-3.2-3B 微调）平均 AUC 为 0.766。这意味着 SAE 特征捕获了奖励模型相对随机猜测（AUC 0.5）提升幅度的 67%（见 Figure 4）。平均每个样本仅约 4 个活跃特征（$K=4$），却达到了接近黑盒模型的预测能力，表明偏好数据中的信号高度结构化且可压缩为少量可解释维度。

**特征的可解释性得到了独立验证**：在 Community Alignment 数据集上，60.4% 的标注者书面解释与至少一个 SAE 活跃特征匹配，而随机非活跃特征的匹配率仅为 33.3%（Figure 5）。外部专家评估进一步证实，47 个具有统计显著预测系数的特征中，100% 被评为可理解，87% 被评为有帮助（Table 6）。

![[assets/figures/papers/paper_list_l51_https_openreview_net_forum_id_sC6A1bFDUt/figures/010_Table_6.jpg]]
*Table 6: Across 5 datasets, we took the top 10 features per dataset, and first counted how many had a statistically significant prediction coefficient. Of these 47/50 features, we had expert annotators qualitatively rate them for helpfulness and interpretability. 47/47 were rated interpretable by the median of the three annotators, and 41/47 were rated helpful*

### 消融实验：SAE 架构的必要性

为验证稀疏自编码器在特征发现中的关键作用，论文设计了两个消融基线：

- **Embed-TopDims**：直接取嵌入差异 $e_\Delta$ 中方差最大的维度作为特征
- **Embed-PCA**：使用嵌入差异的主成分作为特征

Table 2 显示，SAE 在所有 7 个数据集上均显著优于这两个基线。以高保真特征数（即自然语言描述与激活值间 Pearson 相关经 Bonferroni 校正后 $p<0.05$ 的特征）衡量，SAE 平均产生 19.6/32 个高保真特征，而 Embed-TopDims 为 12.7/32，Embed-PCA 仅为 4.9/32。在去重后的非冗余高保真特征数上，SAE 同样领先（18.0 vs 10.7 vs 4.6）。这表明简单的维度筛选或线性变换无法有效分离出可解释的偏好概念，SAE 的稀疏性约束对解耦语义特征至关重要。

![[assets/figures/papers/paper_list_l51_https_openreview_net_forum_id_sC6A1bFDUt/figures/006_Table_2.jpg]]
*Table 2: Comparison of the SAE against two ablations across all 7 datasets. The SAE produces substantially more interpretable features, as measured by mean fidelity, the number of high-fidelity features (i.e., with statistically significant fidelity scores), and the number of non-redundant highfidelity features (i.e., features that are both high-fidelity and semantically distinct from one another)*

与另一自动特征发现方法 **Inverse Constitutional AI（ICAI）**（Findeis et al., 2025）的对比中，WIMHF 表现出更强的偏好预测特征发现能力（Table 5）：在 5 个数据集的独立回归中，WIMHF 共发现 43/50 个统计显著特征，ICAI 为 28/50；在联合回归中，WIMHF 为 34/50，ICAI 为 21/50。

![[assets/figures/papers/paper_list_l51_https_openreview_net_forum_id_sC6A1bFDUt/figures/009_Table_5.jpg]]
*Table 5: Compared to Inverse Constitutional AI, WIMHF produces more features that statistically significantly predict preference labels. S: # of significant features when performing separate regressions for each method; J: # of significant features in a joint regression with both methods*

### 稳健性检验

WIMHF 特征并非特定嵌入模型或随机种子的产物。Table 3 展示了在 HH-RLHF 上分别使用 OpenAI text-embedding-3-small 和 ModernBERT 嵌入训练 SAE 后的特征匹配结果：两种嵌入空间下学到的特征语义高度一致。Table 4 进一步验证了不同随机种子下 SAE 特征的可重复性，匹配特征对保持了相似的语义解释。

![[assets/figures/papers/paper_list_l51_https_openreview_net_forum_id_sC6A1bFDUt/figures/007_Table_3.jpg]]
*Table 3: Embedding-model robustness: matched feature pairs from HH-RLHF using OpenAI text-embedding-3-small vs. nomic-ai/modernbert-embedding-base*

![[assets/figures/papers/paper_list_l51_https_openreview_net_forum_id_sC6A1bFDUt/figures/008_Table_4.jpg]]
*Table 4: Across-seed reproducibility: matched feature pairs from two independent SAE runs on HH-RLHF with different random seeds. Together, these results indicate that WIMHF’s features are not artifacts of a specific embedding model or random seed*

### 应用验证：数据整理与个性化

**数据整理**：在 Chatbot Arena 数据集中，WIMHF 发现了一个强烈的表达偏好——标注者显著偏好模型满足不安全请求而非拒绝（边际胜率变化 $\Delta\text{win} = -31\%$，Table 1）。基于此发现，论文对“拒绝不安全请求”特征激活最强的前 1000 个样本进行标签翻转（将拒绝改为被选，不安全回复改为被拒）。结果显示，RewardBench2 的安全准确率从 8.9% 跃升至 46.2%，提升了 37.3 个百分点，且非安全性能保持在基线的 95% 置信区间内，未受损害（Figure 3a）。这一简单干预还导致了 Chatbot Arena Elo 排名的显著变化：30 个模型中 16 个的 Elo 变化超过 50 分，表明原始排名受到不安全偏好的严重污染（Figure 6）。

![[assets/figures/papers/paper_list_l51_https_openreview_net_forum_id_sC6A1bFDUt/figures/002_Table_1.jpg]]
*Table 1: WIMHF extracts a diversity of interpretable, dataset-specific concepts, several of which have large effects on response winrate. “∆win” is the mean change in winrate when a response contains the feature, controlling for length. “Prevalence” is how often a feature occurs in the dataset*

**个性化**：在 Community Alignment 上，通过混合效应模型识别出最主观的特征为“段落 vs 列表”（$\tau_j$ 最大，Table 7）。仅针对该特征进行个性化建模（学习每位标注者的特征系数偏移），在 $k=16$ 个训练样本时，保留 AUC 相较全局模型提升了 +1.1%（Figure 3b）。主动采样策略（优先选择特征激活最强的样本）在低 $k$ 时比随机采样效率更高。

![[assets/figures/papers/paper_list_l51_https_openreview_net_forum_id_sC6A1bFDUt/figures/011_Table_7.jpg]]
*Table 7: Most and least subjective features in CA, ranked by the estimated random-slope variance $\tau _ { j }$ from the mixed-effects model. $\beta _ { j }$ is the dataset-level mean effect (described in §5.2)

### 数据集间偏好冲突

Figure 2 和 Table 1 揭示了不同数据集间显著的偏好异质性。例如，Reddit 和 Arena 偏好笑话和非正式语气，而 HH-RLHF 和 PRISM 则厌恶这些特征。这种冲突意味着简单混合多个数据集进行偏好微调可能导致信号抵消，削弱对齐效果。WIMHF 为从业者提供了在数据收集前评估数据集价值观多样性的工具。

### 失败模式与局限

尽管 WIMHF 在多数场景下表现良好，但存在明确的边界条件：

1. **特征描述的完整性**：自然语言描述由 LLM 自动生成，保真度评分仅提供统计相关性保证，无法确保捕获连续激活的全部语义。部分特征可能因描述不精确而被误判为低质量。
2. **客观性场景的局限**：当前分析过滤了数学、编程等客观问答对，因为文本嵌入可能不编码正确性信息。WIMHF 无法直接评估响应的正确性，仅适用于主观偏好场景。
3. **虚假关联的传播**：Table 10 展示了环境可持续性特征在 CA 中的负向偏好关联——当提示与可持续性无关时，包含可持续性内容的响应反而被标注为较差。这种虚假关联若被奖励模型学到，可能泛化至本应相关的提示，产生意外行为。
4. **个性化扩展风险**：当前仅验证了单特征个性化的效果。扩展到大量主观特征时，可能产生不可预见的交互效应（如信息茧房），需要额外的安全约束机制。

![[assets/figures/papers/paper_list_l51_https_openreview_net_forum_id_sC6A1bFDUt/figures/019_Table_10.jpg]]
*Table 10: Examples from CA where the environmental sustainability feature is present. In each case, the other response is preferred, likely because sustainability was not relevant to the user’s request*

### 重要图表结论速览

| 图表 | 核心结论 |
|------|----------|
| Figure 4 | SAE 特征捕获黑盒奖励模型 67% 的预测增益，仅需约 4 个活跃特征 |
| Figure 5 | 60.4% 标注者解释与 SAE 特征匹配，远高于随机基线 33.3% |
| Figure 3a | 翻转 1000 个不安全拒绝样本标签，安全准确率从 8.9% 升至 46.2%，非安全性能未受损 |
| Figure 3b | 对“段落 vs 列表”特征个性化，保留 AUC 提升 +1.1%，主动采样效率更高 |
| Table 2 | SAE 高保真特征数（19.6/32）远超 Embed-TopDims（12.7/32）和 Embed-PCA（4.9/32） |
| Table 5 | WIMHF 显著特征数（43/50）超过 ICAI（28/50） |
| Figure 2 | 同一特征在不同数据集中偏好方向可能完全相反，混合数据存在信号冲突风险 |
| Figure 6 | 安全调整后 Elo 排名大幅变化，16/30 模型变化 ≥50 分 |

### 补充图表

![[assets/figures/papers/paper_list_l51_https_openreview_net_forum_id_sC6A1bFDUt/figures/017_Table_8.jpg]]
*Table 8: Features whose coefficients vary significantly with annotator demographics. We show only the features that have a likelihood ratio test (Vuong, 1989) p-value of less than 0.05 after Bonferroni multiple testing correction (i.e., after multiplying the p-value by the number of features tested)*

![[assets/figures/papers/paper_list_l51_https_openreview_net_forum_id_sC6A1bFDUt/figures/018_Table_9.jpg]]
*Table 9: We use gpt-5-low to judge whether the top-activating SAE feature for a given example is mentioned to any extent by the annotator-written explanations for why they picked their preferred response. In the table, we show several examples that were judged as matches (top section) and several examples that were judged as non-matches (bottom section). Excerpts of responses and explanations come from the Community Alignment dataset (Zhang et al., 2025a)*

![[assets/figures/papers/paper_list_l51_https_openreview_net_forum_id_sC6A1bFDUt/figures/021_Table_11.jpg]]
*Table 11: Note: These examples include toxic content. Excerpts from the Chatbot Arena dataset where the feature for “refusing unsafe queries” fires most strongly. Annotators almost always choose the response that generates a response, even when it is very toxic/sexual/harmful. Non-relevant sections of the prompts and responses are excluded*

![[assets/figures/papers/paper_list_l51_https_openreview_net_forum_id_sC6A1bFDUt/figures/023_Table_12.jpg]]
*Table 12: All WIMHF features on Chatbot Arena with a high-fidelity interpretation (see §3, step 2). Features are colored based on whether they have a statistically significant relationship with preference, y. “∆win” is the average marginal effect on y when the feature is positive vs. negative, and after controlling for length. “Prevalence” is how often the feature occurs (i.e., is nonzero) across all response pairs in the dataset. We use Bonferroni correction for all significance tests. Dataset: Chatbot Arena. 7/22 features predict preference (p \< 0.0023)*

## 方法谱系与知识库定位

### 核心方法定位

WIMHF 处于**可解释偏好学习**与**数据集审计**的交叉点，其核心贡献在于将稀疏自编码器（SAE）引入偏好数据的自动化分析，架起了可测量偏好（响应对中一致出现的差异）与表达偏好（真正驱动标注决策的特征）之间的桥梁。与现有方法相比，WIMHF 的关键差异在于**无需预定义偏好类别**，而是从嵌入空间中自动发现可解释的偏好维度。

### 与基线方法的关系

**黑盒奖励模型（Llama-3.2-3B 微调）** 作为偏好预测性能的上界，在 7 个数据集上平均 AUC 达 0.766。WIMHF 使用仅 4 个活跃 SAE 特征的逻辑回归达到 0.672，捕获了奖励模型 67% 的预测增益（相对于随机 AUC 0.5）。这一差距揭示了当前嵌入表示的信息瓶颈：文本嵌入可能无法充分编码正确性等客观维度，导致 WIMHF 在数学、编程等需要事实评估的场景中受限。

**Inverse Constitutional AI（ICAI）**（Findeis et al., 2025）是自动特征发现与偏好预测的直接对比方法。ICAI 通过 LLM 提示生成假设性宪法规则，再检验其对偏好标签的预测力。WIMHF 在 5 个数据集上表现出更强的特征发现能力：单独回归中产生 43/50 个统计显著特征（vs. ICAI 的 28/50），联合回归中为 34/50（vs. 21/50）（Table 5）。这一优势源于 SAE 直接从数据分布中学习，而非依赖 LLM 的先验假设生成，后者可能遗漏数据中隐含但未被语言模型“想到”的偏好维度。

**Embed-TopDims** 和 **Embed-PCA** 作为嵌入空间的消融基线，直接使用嵌入维度的最高方差方向或主成分作为“特征”。SAE 在高保真特征数量上显著优于两者：平均 19.6/32 vs. 12.7/32 vs. 4.9/32；非冗余高保真特征数为 18.0 vs. 10.7 vs. 4.6（Table 2）。这表明嵌入空间的高方差方向并不天然对应人类可解释的概念，而 SAE 的稀疏性约束（BatchTopK，K=4）强制特征与可分离的语义概念对齐。

### 方法适用边界

**有效边界**：
- WIMHF 在**主观对话类偏好数据**上表现最佳，包括风格、语气、安全拒绝、格式偏好等维度。当偏好差异可被文本嵌入捕获时，SAE 特征能提供高保真解释。
- 方法对嵌入模型和随机种子具有稳健性：在 HH-RLHF 上使用 OpenAI text-embedding-3-small 与 ModernBERT 产生的特征语义高度一致（Table 3），不同种子下的 SAE 运行也产生可匹配的特征对（Table 4）。

**失效边界**：
- **客观正确性评估**：当前方法过滤了数学、编程等客观问答，因为文本嵌入可能不编码正确性信号。在此类场景下，WIMHF 发现的“偏好”可能仅是表面风格差异，而非真正的质量信号。
- **低资源标注者**：个性化分析要求每位标注者至少 200 条标注，在数据稀缺的用户上不稳健。选择性个性化策略（先拟合全局模型，再估计用户特定系数）部分缓解了此问题，但仅在最主观的单特征上验证了有效性。
- **多特征个性化扩展**：当前仅展示了单特征（段落 vs 列表）的个性化效果（+1.1% 保留 AUC，Figure 3b），扩展到数十个主观特征时可能存在未预见的交互风险。

### 局限与开放问题

**方法内在局限**：
1. **特征描述的 LLM 依赖性**：自然语言描述由 LLM（gpt-5-mini）生成，受限于提示设计和模型能力。保真度评分（Pearson 相关）仅提供统计验证，不能保证所有概念都被完整捕获。外部专家评估显示 100% 特征可理解、87% 有帮助（Table 6），但仍有 13% 的特征被认为缺乏实用性。
2. **提示信息融合不足**：使用完整提示-响应嵌入（e_{p,r}）并未提升偏好预测 AUC（Figure 4），表明当前方法未能有效利用提示上下文来区分“因提示相关而偏好”与“虚假关联偏好”。例如，环境可持续性特征在 CA 数据集中表现为负向偏好，但实际是因为该特征与提示无关而被误判（Table 10）。
3. **嵌入空间偏向**：SAE 训练使用的嵌入模型（text-embedding-3-small）可能引入其自身的偏向，尽管跨模型稳健性被部分验证，但对其他嵌入空间的适用性仍需进一步检验。

**开放研究问题**：
- **跨数据集冲突解决**：Figure 2 揭示了显著的偏好冲突——同一特征在不同数据集中可能从被偏好翻转为被厌恶（如笑话/非正式语气在 Reddit/Arena 中被偏好，在 HH-RLHF/PRISM 中被厌恶）。当混合多个数据集进行偏好微调时，如何制定原则性的选取或加权策略以避免信号抵消？
- **虚假关联的泛化阻断**：WIMHF 发现的特征-偏好关联可能包含虚假成分（如环境可持续性的负向关联）。如何防止奖励模型将这些关联泛化至其本应相关的提示？是否需要显式的反事实数据增强？
- **在线偏差缓解**：当前的数据整理应用是一次性的预处理步骤（翻转 top 1000 样本标签使 RewardBench2 安全准确率从 8.9% 提升至 46.2%，Figure 3a）。能否利用 WIMHF 发现的偏差特征动态调整训练目标，实现在线式的偏差缓解？
- **多语言与文化扩展**：WIMHF 目前仅处理英语数据。多语言或文化特定的偏好反馈可能包含不同的表达方式，SAE 学习的特征空间是否具有跨语言迁移能力？
- **个性化安全边界**：尽管个性化能提升用户满意度，但需要限制在低风险特征子集（如风格而非政治立场）。当扩展到数十个主观特征时，如何确保不会加剧回音室效应？是否需要总体的安全约束机制来限制个性化范围？

## 原文 PDF

![[paperPDFs/ICLR_2026/Whats_In_My_Human_Feedback_Learning_Interpretable_Descriptions_of_Preference_Data.pdf]]
