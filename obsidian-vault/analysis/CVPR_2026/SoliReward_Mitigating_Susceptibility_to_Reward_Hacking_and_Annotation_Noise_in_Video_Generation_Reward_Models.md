---
title: "SoliReward: Mitigating Susceptibility to Reward Hacking and Annotation Noise in Video Generation Reward Models"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/SoliReward_Mitigating_Susceptibility_to_Reward_Hacking_and_Annotation_Noise_in_Video_Generation_Reward_Models.pdf
project_link: null
code_link: "https://github.com/lian700/SoliReward"
aliases:
- SBWH
- SoliReward
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/image_and_video_generation
- topic/generative_models_diffusion
- topic/representation_self_supervised_transfer
core_operator: 通过单物品二元标注+交叉提示配对降低标注噪声，利用带平局项的BT-WT损失（引入win-tie对）显式正则化正样本集内的分数方差以抑制奖励尖峰，并采用分层渐进查询注意力（HPQA）聚合多层特征提升奖励的表达力。
primary_logic: 将高噪声的相对比较转化为低噪声的二元判定，再通过跨提示配对挖掘大规模高信号偏好对；同时用平局对强制正样本映射到紧凑的奖励流形，从根源上削弱奖励攻击；并利用Transformer层间功能特化设计HPQA，实现底层保真度与高层语义的显式融合。
claims:
- 二元标注显著改善标注者间一致性（单题 α=0.4939, 成对 α=0.3516）
- SoliReward在物理/变形任务上取得最优ID准确率78.48和OOD准确率80.08，远超VideoAlign的71.60
- BT-WT相比BT显著提升后训练VBench2 Human Fidelity (0.8999 vs 0.8693)
- HPQA架构在TA任务上避免分数坍缩，ID准确率79.02远高于线性头72.41
---

# SoliReward: Mitigating Susceptibility to Reward Hacking and Annotation Noise in Video Generation Reward Models

> [!tip] 核心洞察
> 将高噪声的相对比较转化为低噪声的二元判定，再通过跨提示配对挖掘大规模高信号偏好对；同时用平局对强制正样本映射到紧凑的奖励流形，从根源上削弱奖励攻击；并利用Transformer层间功能特化设计HPQA，实现底层保真度与高层语义的显式融合。

| 字段 | 内容 |
|------|------|
| 中文题名 | SoliReward: 缓解视频生成奖励模型奖励攻击与标注噪声 |
| 英文题名 | SoliReward: Mitigating Susceptibility to Reward Hacking and Annotation Noise in Video Generation Reward Models |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2512.22170) · [Code](https://github.com/lian700/SoliReward) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/image_and_video_generation #topic/generative_models_diffusion #topic/representation_self_supervised_transfer |
| Method | SoliReward（含二元标注、跨提示配对、BT-WT损失、HPQA架构） |
| Dataset | In-Domain, Out-of-Distribution, VBench2 Human Fidelity, VBench Semantic Alignment |

> [!tip] 效果简介
> - In-Domain (ID) 上，RM Accuracy 78.48 (Phy&Deform), 79.02 (TA) vs 71.60 (VideoAlign, Phy&Deform); 54.85 (VideoPhy, TA) (+6.88 (Phy&Deform); +24.17 (TA))。
> - Out-of-Distribution (OOD) 上，RM Accuracy 80.08 (Phy&Deform), 60.25 (TA) vs 71.60 (VideoAlign, Phy&Deform); 60.52 (VideoPhy, TA) (+8.48 (Phy&Deform); ~0 (competitive))。
> - VBench2 Human Fidelity (post-training) 上，Overall Score 0.8999 (guided by ours) vs 0.8695 (guided by VideoAlign MQ) (+0.0304)。

## 概要

视频生成模型的后训练优化（如GRPO、DPO）高度依赖奖励模型提供可靠的偏好信号。然而，当前视频奖励模型的训练面临三重瓶颈：**标注噪声**（成对比较范式引入严重标注者分歧）、**奖励攻击**（reward hacking导致生成策略过拟合到虚假高奖励特征），以及**分数表达退化**（现有VLM架构输出离散化或坍缩）。SoliReward针对上述瓶颈提出系统性解决方案，核心思路是将高噪声的相对比较转化为低噪声的二元判定，再通过跨提示配对挖掘大规模高信号偏好对，并利用平局对强制正样本映射到紧凑的奖励流形以从根源削弱奖励攻击。

方法层面，SoliReward由四个关键模块构成：**单物品二元标注**（Pass/Fail，独立评估每个质量维度）将标注者间一致性从成对比较的Krippendorff’s α=0.3516提升至0.4939；**跨提示配对策略**突破同提示限制，从二元标签构建大规模多样化偏好对；**BT-WT损失**在标准Bradley-Terry损失中引入win-tie对（μ=0.5），显式正则化正样本集内的分数方差以抑制奖励尖峰；**分层渐进查询注意力（HPQA）**通过可学习查询向量逐步聚合VLM骨干多层Transformer特征，结合残差连接实现底层保真度与高层语义的显式融合，避免分数坍缩。

实验验证了SoliReward的有效性：在物理/变形任务上，域内准确率78.48、域外准确率80.08，分别超越VideoAlign（71.60）达+6.88和+8.48个百分点；在语义对齐任务上，域内准确率79.02远超VideoPhy（54.85）。后训练方面，以SoliReward引导HunyuanVideo在VBench2 Human Fidelity上达到0.8999，优于BT损失的0.8693和VideoAlign MQ的0.8695。消融实验证实HPQA在所有架构中准确率最高且避免分数聚类，BT-WT通过降低组内优势值方差缓解过优化，模型规模从1B到8B提升显著但从8B到14B收益递减。

**局限与开放问题**：二元标注虽降低噪声但可能丢失细粒度质量差异；当前每个RM仅针对单一质量维度；后训练验证限于HunyuanVideo和DanceGRPO，跨生成模型泛化性待验证；更大规模参数下能否突破边际收益递减、多维度联合评估的架构设计等仍需探索。

### 视频生成奖励模型的现实困境

视频生成模型近年取得了显著进展，但生成结果在物理合理性、时序连贯性和语义对齐等关键质量维度上仍存在明显不足。奖励模型（Reward Model, RM）作为对齐生成策略与人类偏好的核心组件，在强化学习微调（RL fine-tuning）和测试时扩展（test-time scaling）中扮演着不可替代的角色。然而，现有视频生成奖励模型的训练范式面临三重相互交织的瓶颈，严重制约了其作为可靠质量裁判的能力。

**瓶颈一：标注范式引入严重噪声。** 主流奖励模型依赖成对比较（pairwise comparison）或多级评分（Likert scale）来获取偏好信号。成对比较要求标注者对同一提示下的两个视频做出相对质量判断，这种任务本身认知负荷高、主观性强。SoliReward的标注一致性实验直接证实了这一问题：在5名标注者参与的条件下，成对比较的Krippendorff’s α仅为0.3516（Table 1），处于“一般”一致性水平，表明标注者之间对“哪个视频更好”的判断存在显著分歧。这种高噪声的监督信号直接污染了奖励模型的训练目标，使其难以学到真正反映质量差异的奖励函数。

**瓶颈二：奖励攻击（Reward Hacking）导致生成策略过拟合。** 即使奖励模型在训练集上表现出色，在后续的强化学习后训练（post-training）阶段，生成策略往往会利用奖励函数的漏洞，产生具有虚假高奖励特征但实际质量低劣的样本。这一现象的根源在于标准Bradley-Terry（BT）损失仅通过win-lose对来拉开正负样本的奖励差距，却不对正样本内部的奖励分布施加任何约束。结果是，奖励模型可能对某些表面特征（如色彩饱和度、特定纹理模式）赋予异常高的分数，生成策略则迅速过拟合到这些“奖励尖峰”上，形成奖励攻击的正反馈循环。

**瓶颈三：VLM架构输出表达力不足。** 现有基于视觉语言模型（VLM）的奖励模型通常采用简单的分数提取方案——例如取最后token嵌入后接线性头、提取特殊token的隐藏态、或直接使用“yes” token的概率作为奖励值。这些方案忽略了Transformer不同层所编码的层次化语义信息：浅层更关注纹理、边缘等底层保真度特征，深层则编码高层语义和抽象概念。粗暴的单点特征提取导致奖励分数出现严重的坍缩（score collapse）和离散化（discretization）现象。在语义对齐（TA）任务上，SoliReward的实验观察到基线架构的奖励分布退化为少量离散值（Table 5中标注∗的条目），大量样本被赋予完全相同的分数，丧失了区分细粒度质量差异的能力。

### 现有方法的缺口

当前视频生成奖励模型的研究主要沿着两条路径展开。一是改进VLM的输入表示或评分机制，如**VideoScore**系列和**VisionReward**通过设计专用提示模板或特征融合策略来提升评分的准确性。二是优化偏好数据的构建方式，如**VideoPhy**和**UnifiedReward**针对特定质量维度（物理合理性、美学等）收集领域专用的成对比较数据。然而，这些工作均未从根本上解决上述三重瓶颈的因果链条：标注噪声污染偏好对 → 有噪偏好对训练出不鲁棒的奖励函数 → 奖励函数在RL后训练中被攻击 → 生成质量提升受限。

具体而言，现有方法存在以下结构性缺口：

- **标注层面**：成对比较和多级评分的噪声问题被普遍忽视，缺乏从标注范式本身降低噪声的系统性方案。
- **损失函数层面**：标准BT损失仅建模win-lose关系，缺乏对正样本集内部分数分布的正则化机制，无法从训练目标层面抑制奖励攻击。
- **架构层面**：线性头或单点token提取丢弃了VLM骨干网络中丰富的层次化特征，导致奖励表达力不足和分数坍缩。

### 本文动机与核心思路

SoliReward的出发点是一个关键洞察：**将高噪声的相对比较转化为低噪声的二元判定，再通过跨提示配对挖掘大规模高信号偏好对；同时用平局对强制正样本映射到紧凑的奖励流形，从根源上削弱奖励攻击；并利用Transformer层间功能特化设计层次化特征聚合架构，实现底层保真度与高层语义的显式融合。**

这一思路转化为四个相互协同的技术决策：

1. **单物品二元标注**：将复杂的“A比B好”判断简化为独立的“该视频在维度X上是否合格（Pass/Fail）”判定，显著降低标注者的认知负荷和主观分歧。
2. **跨提示配对**：利用二元标签从不同提示的Pass和Fail样本中构建大规模、多样化的偏好对，突破同提示配对的规模限制，同时提高数据利用率。
3. **BT-WT损失**：在标准BT损失中引入win-tie对（即两个Pass样本的平局关系），通过μ=0.5的平局权重惩罚正样本间的奖励方差，使正样本的奖励分布集中化，从而抑制奖励尖峰的出现。
4. **HPQA架构**：通过可学习的查询向量在VLM的多个Transformer层间渐进式聚合特征，并结合残差连接融合最终层信息，生成鲁棒且连续的标量奖励。

SoliReward并非简单组合现有技术，而是从数据采集、偏好构建、训练目标和特征提取四个维度对奖励模型训练范式进行了协同重构，其有效性在物理合理性、变形合理性和语义对齐等多个质量维度上得到了系统验证。

## 核心方法与创新机理

SoliReward 针对视频生成奖励模型训练中的三重瓶颈——标注噪声、奖励攻击（reward hacking）和输出表达不足——提出了三项协同创新，构成一个从数据采集到模型架构的完整改进链条。其核心思路是：**将高噪声的相对比较转化为低噪声的二元判定，再通过跨提示配对挖掘大规模高信号偏好对；同时用平局对强制正样本映射到紧凑的奖励流形，从根源上削弱奖励攻击；并利用Transformer层间功能特化设计HPQA，实现底层保真度与高层语义的显式融合。**

### 1. 单物品二元标注：从相对比较到独立判定

传统视频奖励模型依赖**成对比较**（pairwise comparison）或**多级Likert评分**来获取训练信号，但这些范式面临严重的标注者间分歧。SoliReward 将标注范式彻底简化为**单物品二元标注**（single-item binary annotation）：标注者只需对单个视频在特定质量维度上做出 Pass/Fail 判定，无需在不同样本间进行相对权衡。

这一改变的因果机制在于：相对判断要求标注者在多个样本间建立隐式排序，引入了额外的认知负荷和主观偏差；而二元判定仅需对照客观标准进行独立评估，大幅降低了标注噪声。实验证据显示，在5名标注者的测试中，单物品二元标注的标注者间一致性（Krippendorff’s α=0.4939, Fleiss’s κ=0.4925, 原始一致率77.33%）显著优于成对比较（α=0.3516）（Table 1）。需指出，α=0.4939 仍仅处于中等一致性水平，表明二元标注虽显著改善但尚未完全消除主观性。

### 2. 跨提示配对：突破同提示约束，释放二元标签潜力

二元标注虽降低了噪声，但丢失了传统BT损失所需的偏好排序信号。SoliReward 通过**跨提示配对策略**（cross-prompt pairing）解决了这一矛盾：将来自不同提示（prompt）的 Pass 和 Fail 样本进行配对，生成大规模、多样化的偏好对。

与基线方法（仅在同一提示内的视频间配对）相比，跨提示配对的因果优势在于：（1）打破了同提示视频数量有限的瓶颈，可从二元标签池中组合出数量级更大的训练对；（2）跨提示的难度差异更大，偏好信号更强。消融实验表明，跨提示策略在RM准确率和奖励margin上均与同提示策略可比（Table 7, Table 8），同时显著提高了数据利用率。这一策略依赖于充足的 Pass 和 Fail 样本储备，在极端不平衡场景下的有效性尚待验证。

### 3. BT-WT损失：以平局对正则化正样本流形

标准 Bradley-Terry（BT）损失仅使用 win-lose 对训练，导致奖励模型在正样本区域产生过大的分数方差，形成奖励尖峰——这是奖励攻击的核心诱因。SoliReward 提出 **Bradley-Terry with Win-Tie（BT-WT）损失**：

$$\mathcal{L}_{\mathrm{BT-WT}} = \mathbb{E}_{(y_i,y_j)\in W\times(W\cup L)}[-\mu\log\sigma(\Delta r)-(1-\mu)\log\sigma(-\Delta r)]$$

其中 $\Delta r = r_{\theta}(y_i) - r_{\theta}(y_j)$，$\mu=1$ 对应 win-lose 对，$\mu=0.5$ 对应 win-tie 对。关键创新在于引入 win-tie 对（两个 Pass 样本的配对），通过 $\mu=0.5$ 的对称损失惩罚正样本间的分数差异，迫使所有 Pass 样本映射到紧凑的奖励流形。

这一正则化机制从根本上改变了后训练中的优化动力学。在 GRPO 后训练中，组内优势值 $A_i = \frac{r_i - \bar{r}}{\sigma}$ 决定了策略更新的幅度。BT-WT 通过集中正样本分数分布，显著降低了排名靠前样本的优势值（Figure 4），从而抑制了生成策略向虚假高奖励特征的过优化。实验表明，BT-WT 在后训练 VBench2 Human Fidelity 上达到 0.8999，显著超越 BT 的 0.8693（Table 3）。值得注意的是，引入 lose-tie 对的 BTT 变体反而导致性能下降（VBench2 0.8700），说明正则化的关键在于约束正样本流形而非负样本（Table 10）。

### 4. HPQA架构：分层渐进查询聚合多层语义

现有 VLM 奖励模型通常仅使用最后 token 嵌入或单层特征，导致分数坍缩和离散化（Figure 2）。SoliReward 提出 **Hierarchical Progressive Query Attention（HPQA）** 架构，通过可学习查询向量逐步聚合多层 Transformer 特征：

$$q^{(1)} = \mathrm{MHA}_1(Q=q^{(0)}, K=H_{l_1}, V=H_{l_1})$$

$$q^{(i)} = \mathrm{MHA}_i(Q=q^{(i-1)}, K=H_{l_i}, V=H_{l_i})$$

$$r = \mathrm{RewardHead}(q_{\mathrm{prog}} + o_{\mathrm{res}})$$

其因果机制利用了 Transformer 层的功能特化：浅层保留更多细粒度视觉保真度信息，深层编码高层语义抽象。渐进查询精炼（Eq. 4）使查询向量逐层融合这些异质特征，最终通过残差连接（Eq. 5-6）整合最后一层信息，输出连续且鲁棒的标量奖励。

在语义对齐（TA）任务上，HPQA 的 ID 准确率达到 79.02，远超线性头方案的 72.41，且完全避免了其他架构的分数聚类问题（Table 5）。该架构在 Qwen2-VL（2B）、Qwen2.5-VL（3B）和 InternVL3（14B）等多种 VLM 骨干上均有效，4~5 个中间层聚合效果较优（Table 11, Table 12）。

### 创新协同与边界

上述四项创新构成闭环：二元标注降低数据噪声 → 跨提示配对释放信号规模 → BT-WT 损失正则化奖励流形 → HPQA 提升输出表达力。从 1B 到 8B 的模型规模扩展带来显著性能提升，但从 8B 到 14B 的收益递减（Phy&Deform OOD ACC: 81.43 → 81.71），暗示当前数据规模或任务复杂度可能接近该架构的容量上限（Table 9）。此外，当前每个 RM 仅针对单一质量维度，多维度联合评估是明确的拓展方向。

SoliReward 框架从数据采集到奖励模型训练再到生成模型后训练，形成一条完整的闭环管线，其核心设计围绕三个瓶颈展开：标注噪声、奖励攻击（reward hacking）和奖励信号表达不足。图 1 给出了框架的总览。

**数据采集与偏好构建。** 传统视频奖励模型依赖成对比较或 Likert 多级评分，标注者间一致性低（Krippendorff’s α 仅 0.3516）。SoliReward 将标注范式重新定向为**单物品二元标注**（Pass/Fail），标注者仅需对单个视频在特定质量维度上做出通过/不通过的判定，将高噪声的相对比较转化为低噪声的二元决策。在此基础上，引入**跨提示配对策略**（cross-prompt pairing）：将来自不同提示的 Pass 和 Fail 样本组合成偏好对，突破同提示配对的限制，从有限的二元标签中构建大规模、多样化的训练信号。这一策略在精度和奖励 margin 上与同提示配对可比（Table 7, Table 8），同时显著提升数据利用率。

**奖励模型训练。** 偏好对构建完成后，SoliReward 使用 **Bradley-Terry with Win-Tie（BT-WT）损失**训练奖励模型。标准 BT 损失仅利用 win-lose 对，而 BT-WT 额外引入 win-tie 对（两个 Pass 样本之间的平局对），通过将平局对的目标概率设为 0.5，显式惩罚正样本集内的分数方差，从根源上抑制奖励尖峰和过优化。消融实验表明，引入 lose-tie 对的 BTT 变体反而降低性能（Table 10），说明正则化的关键在于约束正样本的分数分布集中度。

**奖励信号提取。** 为克服现有 VLM 架构输出表达不足导致的分数坍缩与离散化问题，SoliReward 设计了 **Hierarchical Progressive Query Attention（HPQA）**适配器。HPQA 通过一组可学习查询向量，从 VLM 骨干的多层 Transformer 隐藏态中逐步聚合特征：底层保留视觉保真度信息，高层捕获语义抽象，最终通过残差连接融合渐进特征与末层特征，经 RewardHead 输出连续标量奖励。该设计显式利用了 Transformer 层间功能特化的特性，在语义对齐任务上避免分数聚类（Figure 2），ID 准确率达 79.02，显著优于线性头方案的 72.41（Table 5）。

**后训练优化。** 训练好的 SoliReward 奖励模型作为冻结的评判器，通过 DanceGRPO 算法指导 HunyuanVideo 生成模型的后训练。BT-WT 损失对正样本分数分布的集中效应直接降低了 GRPO 中组内优势值的方差（Figure 4），缓解了生成策略对虚假高奖励特征的过拟合，最终在 VBench2 Human Fidelity 上达到 0.8999，较 BT 训练的奖励模型提升 0.0306（Table 3）。

![[assets/figures/papers/paper_list_l2702_https_arxiv_org_abs_2512_22170/figures/001_Figure_1.jpg]]
*Figure 1: Pipeline of SoliReward, our framework for data annotation and training of video reward models. (a) We introduce a single-item binary annotation method, coupled with a cross-prompt pairing strategy, to mitigate annotation noise. Furthermore, to alleviate reward hacking, we propose the Bradley-Terry with Win-Tie (BT-WT) loss. (b/c) We propose a novel VLM-based Reward Model (VLM-RM) architecture, featuring a Hierarchical Progressive Query Attention (HPQA) adapter. This adapter progressively aggregates multi-level representations from the VLM backbone to compute a robust reward score*

SoliReward 框架围绕三个关键模块构建：低噪声数据采集、抗攻击训练损失、以及多层特征聚合架构。以下逐一展开其核心机理与公式推导。

### 3.1 单物品二元标注与跨提示配对

传统视频奖励模型依赖成对比较（pairwise comparison）或 Likert 多级评分，标注者需同时观看两个视频并判断相对优劣，这一过程引入显著的标注噪声。SoliReward 将标注范式从根本上简化为**单物品二元判定**：标注者独立观看单个视频，针对特定质量维度（如物理合理性、变形质量、语义对齐）给出 Pass/Fail 二元标签。实验表明，这一转变将标注者间一致性（Krippendorff’s α）从成对比较的 0.3516 提升至 0.4939，原始一致率达 77.33%（Table 1）。

然而，二元标签天然缺失相对排序信息，无法直接驱动 Bradley-Terry 类损失函数。为此，SoliReward 提出**跨提示配对策略**：将来自不同 prompt 的 Pass 样本与 Fail 样本进行配对，构建大规模、高信号的偏好对数据集。这一策略突破了传统同提示配对的限制，使数据利用率大幅提升，且在精度与奖励 margin 上均与同提示策略可比（Table 7, Table 8）。

### 3.2 BT-WT 损失函数

标准 Bradley-Terry（BT）损失仅利用 win-lose 偏好对，其定义为：

$$\mathcal{L}_{\mathrm{BT}} = \mathbb{E}_{(y_i,y_j)\in D}[-\log(\sigma(r_{\theta}(y_i)-r_{\theta}(y_j)))]$$

其中 $r_{\theta}(y)$ 为奖励模型对视频 $y$ 的标量评分，$\sigma$ 为 sigmoid 函数。该损失通过最大化正负样本间的奖励差距来学习排序，但缺乏对正样本内部分数分布的约束，导致奖励模型易被“攻击”——生成策略可通过产生虚假高奖励特征获取极端分数，即 reward hacking。

SoliReward 提出 **Bradley-Terry with Win-Tie（BT-WT）损失**，在 win-lose 对基础上补充 win-tie 对：

$$\mathcal{L}_{\mathrm{BT-WT}} = \mathbb{E}_{(y_i,y_j)\in W\times(W\cup L)}[-\mu\log\sigma(\Delta r)-(1-\mu)\log\sigma(-\Delta r)]$$

$$\Delta r = r_{\theta}(y_i)-r_{\theta}(y_j), \quad \mu = \begin{cases} 1 & y_i \succ y_j \\ 0.5 & y_i \sim y_j \end{cases}$$

其中 $W$ 为 Pass（正样本）集合，$L$ 为 Fail（负样本）集合。当样本对为 win-lose 时（$y_i \in W, y_j \in L$），$\mu=1$，损失退化为标准 BT 形式；当样本对为 win-tie 时（$y_i, y_j \in W$），$\mu=0.5$，损失强制两个正样本的奖励值趋于一致。

**核心机制**：win-tie 对充当正则化项，惩罚正样本集内的奖励方差。当模型试图将某个正样本映射到极端高奖励时，BT-WT 通过平局约束将其拉回正样本群体的集中区域，从而在根源上抑制奖励尖峰。Figure 3 显示，BT-WT 使正样本的奖励分布在高分段更加集中；Figure 4 进一步证实，BT-WT 显著降低了 GRPO 后训练中组内优势值（$A_i = \frac{r_i - \bar{r}}{\sigma}$）的方差，尤其是对 top-rank 样本的优势值，从而缓解过优化现象。

### 3.3 HPQA 架构

现有 VLM 奖励模型通常仅使用最后一层 token 嵌入 + 线性头，或依赖 “yes” token 概率，导致分数坍缩为离散值（Figure 2）。SoliReward 提出 **Hierarchical Progressive Query Attention（HPQA）**，通过可学习查询向量逐步聚合多层 Transformer 特征，显式融合底层保真度与高层语义信息。

**步骤一：初始查询生成**。设 $q^{(0)}$ 为可学习的初始查询向量，$H_{l_1}$ 为选定第一层 Transformer 的隐藏态。通过多头注意力生成第一级查询：

$$q^{(1)} = \mathrm{MHA}_1(Q=q^{(0)}, K=H_{l_1}, V=H_{l_1})$$

**步骤二：渐进查询精炼**。在后续选定层 $l_i$ 上迭代精炼查询向量：

$$q^{(i)} = \mathrm{MHA}_i(Q=q^{(i-1)}, K=H_{l_i}, V=H_{l_i})$$

这一递进机制使查询向量 $q^{(i)}$ 能够桥接不同语义层级——浅层保留细粒度视觉保真度，深层编码高层语义抽象，两者通过注意力权重显式融合。

**步骤三：残差增强**。独立引入一个残差查询 $q_{\mathrm{res}}$，关注最后一层 $H_L$，捕获最终层的全局信息：

$$o_{\mathrm{res}} = \mathrm{MHA}_{\mathrm{res}}(Q=q_{\mathrm{res}}, K=H_L, V=H_L)$$

**步骤四：奖励标量输出**。将渐进特征与残差特征相加后送入奖励头：

$$r = \mathrm{RewardHead}(q_{\mathrm{prog}} + o_{\mathrm{res}})$$

HPQA 的关键优势在于避免了分数离散化。Table 5 显示，HPQA 在语义对齐（TA）任务上 ID 准确率达 79.02，远超线性头（72.41）和 “yes” token 方案（后者出现严重分数聚类）。消融实验表明，选取 4~5 个中间层进行聚合效果较优，且该架构在 Qwen2-VL、InternVL3 等多种 VLM 骨干上均有效（Table 11, Table 12）。

## 实验与关键发现

### 标注者间一致性验证

SoliReward首先验证了二元标注范式对标注噪声的抑制效果。在5名标注者参与的一致性实验中，单物品二元标注（Pass/Fail）的Krippendorff’s α达到0.4939，Fleiss’s κ为0.4925，原始一致率达77.33%；相比之下，传统成对比较标注的α仅为0.3516（Table 1）。这一结果表明，将高噪声的相对比较转化为低噪声的二元判定，确实显著降低了标注者间的主观分歧。但需注意，α=0.4939仅处于中等一致性水平，Pass/Fail的二值简化可能丢失细粒度质量差异信息，这是该方法的内在局限。

![[assets/figures/papers/paper_list_l2702_https_arxiv_org_abs_2512_22170/figures/003_Table_1.jpg]]
*Table 1: Inter-Annotator Agreement (IAA) analysis across 5 annotators. We report Krippendorff’s α [8], Fleiss’s κ [5] and raw agreement for our binary single-item task and pair-wise comparison task. Single-item is more consistent than pairwise annotation*

### 奖励模型准确率主结果

在物理合理性与变形（Phy & Deform）和语义对齐（TA）两个维度上，SoliReward与多个基线进行了全面对比（Table 2）。

![[assets/figures/papers/paper_list_l2702_https_arxiv_org_abs_2512_22170/figures/002_Table_2.jpg]]
*Table 2: Reward model accuracy compared to baselines. ∗ means the score distribution degenerates to discrete values*

**Phy & Deform任务**：SoliReward在域内（ID）测试集上取得78.48的准确率，在域外（OOD）测试集上取得80.08，均显著优于最强基线VideoAlign（ID 54.40，OOD 71.60），相对提升分别为+24.08和+8.48个百分点。其他基线如VideoScore、VideoScore-v1.1、LiFT、VisionReward、VideoPhy、UnifiedReward等均未超过VideoAlign。

**TA任务**：SoliReward在ID上取得79.02，远超VideoPhy的54.85（提升+24.17）；OOD上为60.25，与VideoPhy的60.52基本持平。值得注意的是，多个基线（VideoScore-v1.1、LiFT、VisionReward、UnifiedReward）在TA任务上出现了分数分布退化为离散值的现象（Table 2中以∗标注），这是VLM架构输出表达不足导致的分数坍缩问题，而SoliReward的HPQA架构有效避免了这一问题。

### 后训练性能：奖励模型引导的视频生成优化

将训练好的奖励模型用于引导HunyuanVideo的DanceGRPO后训练，VBench2 Human Fidelity指标上，SoliReward引导的模型达到0.8999，显著优于标准BT损失训练的奖励模型（0.8693）和VideoAlign MQ引导的结果（0.8695）（Table 3、Table 4）。在VBench语义对齐维度上，SoliReward引导的后训练模型平均得分为0.7544，超过HunyuanVideo基线的0.7334和TA专门模型的0.7421（Table 14）。这一结果表明，BT-WT损失和HPQA架构带来的奖励信号质量提升，能有效转化为下游生成模型的性能增益。

![[assets/figures/papers/paper_list_l2702_https_arxiv_org_abs_2512_22170/figures/005_Table_3.jpg]]
*Table 3: Comparison of reward model performance trained via BT and BT-WT. Reward model accuracy and post-training evaluation metrics are reported*

![[assets/figures/papers/paper_list_l2702_https_arxiv_org_abs_2512_22170/figures/010_Table_4.jpg]]
*Table 4: Comparison of reward models on post-training. HunyuanVideo is selected as the video generation backbone, and DanceGRPO algorithm is applied to fine-tune the model. VideoAlign MQ, our reward model score, and VBench2 Human Fidelity are selected as evaluation metrics*

### 奖励攻击缓解机制分析

BT-WT损失的核心机制在于引入win-tie对作为正则化项。Figure 3显示，BT-WT使正样本的奖励分布在高分段更加集中；Figure 4进一步揭示了因果链条：在GRPO后训练中，组内优势值$A_i = \frac{r_i - \bar{r}}{\sigma}$的分布上，BT-WT训练出的奖励模型对top-rank样本产生更小的优势值，从而抑制了生成策略向虚假高奖励特征的过优化。Table 6的消融实验提供了佐证：在BT-WT基础上增加BCE惩罚虽能维持准确率，但奖励margin从3.72骤降至2.97，导致VBench2得分从0.8999降至0.8826，说明惩罚正样本分数方差的机制（而非简单的分类损失）才是缓解奖励攻击的关键。

### 架构消融：HPQA的必要性

Table 5对比了多种奖励信号提取架构。在TA任务上，HPQA的ID准确率达到79.02，远高于线性头（72.41）、"yes" token概率（68.34）和特殊token方案（73.64）。Figure 2直观展示了差异：线性头等替代架构出现严重的分数聚类，大量样本被赋予相同评分，丧失了细粒度区分能力。HPQA通过可学习查询向量逐步聚合多层Transformer特征（Eq. 3-6），底层特征保真度与高层语义信息得以显式融合，从而生成连续且鲁棒的奖励标量。

### 配对策略与模型规模分析

跨提示配对策略在准确率和奖励margin上均与同提示（in-prompt）策略可比（Table 7、Table 8），但跨提示配对的优势在于可突破单视频提示的限制，利用大规模Pass/Fail样本库构建更多样化的偏好对，显著提升数据利用率。

![[assets/figures/papers/paper_list_l2702_https_arxiv_org_abs_2512_22170/figures/014_Table_7.jpg]]
*Table 7: Impact of pairing-strategy for reward model training. Accuracy is evaluated on both ID and OOD datasets. The crossprompt strategy is comparable with in-prompt strategy*

模型规模实验（Table 9）显示，从1B扩展到8B时，Phy & Deform OOD准确率从77.65提升至81.43，收益显著；但从8B到14B仅微增至81.71，且OOD奖励margin出现下降，提示14B模型可能出现了轻微过拟合，边际收益递减。当前数据规模与任务复杂度可能不足以支撑更大模型的有效训练。

### HPQA的泛化性与层选择

HPQA在Qwen2-VL（2B）、Qwen2.5-VL（3B）和InternVL3（14B）等多种VLM骨干上均有效（Table 11、Table 12），验证了架构的通用性。层索引消融表明，聚合4~5个中间层特征通常取得较优效果，这与Transformer不同层功能特化的认知一致——底层捕获纹理和几何信息，高层编码语义抽象，HPQA的渐进查询机制恰好桥接了这两个层次。

## 定位与知识库关联

### 1. 与基线方法的关系与差异化

SoliReward 的提出根植于视频生成奖励模型（Video Reward Model）领域的三重瓶颈：**标注噪声**、**奖励攻击（reward hacking）** 和 **VLM 输出表达不足**。其设计在四个关键维度上与现有基线形成系统性差异。

**标注范式：从相对比较到二元判定。** 现有方法普遍采用成对比较（pairwise comparison）或多级 Likert 评分（point-wise），如 **VideoScore**、**VideoScore-v1.1**、**LiFT** 等。这类范式引入严重的标注者间分歧——论文报告成对比较的 Krippendorff’s α 仅为 0.3516（Table 1），属低一致性水平。SoliReward 将标注重新定向为单物品二元判定（Pass/Fail），将 α 提升至 0.4939，虽仅达中等水平，但显著优于比较范式。这一转变的深层逻辑在于：人类对“该视频是否满足某客观标准”的二元判断，比“A 与 B 哪个更好”的相对比较具有更低的认知负荷和更高的可重复性。

**偏好对构建：从同提示到跨提示。** 传统 BT 损失要求偏好对来自同一提示（in-prompt pairing），这在标注层面限制了数据利用率——每个 prompt 下必须同时存在“好”与“坏”的样本。SoliReward 的跨提示配对策略（cross-prompt pairing）利用二元标签的全局可比性，将不同 prompt 下的 Pass 与 Fail 样本配对，大幅扩展了训练对规模与多样性。消融实验（Table 7 & Table 8）表明，跨提示策略在准确率和奖励 margin 上与同提示策略可比，从而证明其有效性。

**损失函数：从 win-lose 到 win-tie 正则化。** 标准 BT 损失仅建模 win-lose 关系，对正样本内部的分数分布缺乏约束，导致奖励模型在后训练中易被“过优化”——生成策略学会利用虚假高奖励特征。SoliReward 的 BT-WT 损失引入 win-tie 对（μ=0.5），显式惩罚正样本集内的分数方差。这一设计的因果机制在于：通过强制所有 Pass 样本映射到紧凑的高奖励流形，从根源上缩小了奖励攻击者可利用的“分数尖峰”（Figure 3, Figure 4）。Table 3 显示，BT-WT 相比 BT 将后训练 VBench2 Human Fidelity 从 0.8693 提升至 0.8999。值得注意的是，引入 lose-tie 对的 BTT 变体反而导致性能下降（Table 10），暗示正则化应仅作用于正样本子空间。

**奖励提取架构：从单点特征到分层渐进聚合。** 现有 VLM-RM 架构多采用最后 token 嵌入 + 线性头（如部分 VideoScore 变体）、专用特殊 token 或 “yes” token 概率。这些方案在语义对齐（TA）任务上普遍出现分数坍缩——将大量样本映射到离散的几个分数值（Figure 2, Table 5 标注 ∗）。SoliReward 的 HPQA 架构利用 Transformer 层间功能特化：底层保留视觉保真度信息，高层编码抽象语义，通过可学习查询向量逐步聚合多层特征（Eq. 3-6），并辅以残差连接保留最终层信息。Table 5 显示，HPQA 在 TA 任务上达到 79.02% 的 ID 准确率，远高于线性头的 72.41%，且完全避免了分数离散化。

### 2. 适用边界与局限

**模型规模的边际收益递减。** 从 1B 到 8B 的扩展带来显著增益（Phy&Deform OOD ACC: 77.65 → 81.43），但从 8B 到 14B 的提升几乎停滞（81.43 → 81.71），且 14B 模型的 OOD reward margin 出现下降（Table 9）。这表明当前数据量与任务复杂度可能不足以支撑更大模型的训练，14B 已出现一定过拟合。该发现对实际部署具有指导意义：8B 规模可能是性价比最优选择。

**单维度评估的局限。** 目前每个 SoliReward 实例仅针对单一质量维度（物理合理性、变形或语义对齐）训练，未融合多维度联合评估。这限制了其在需要综合质量判断的场景（如通用视频生成评估）中的直接应用。论文将多维融合列为开放问题。

**后训练验证的生态局限。** 后训练实验仅基于 HunyuanVideo 生成骨架和 DanceGRPO 算法（Table 4, Table 13, Table 14）。该组合在 VBench2 和 VBench 上取得了优异结果，但跨生成模型（如 Sora 类架构、扩散 Transformer 变体）和跨优化算法（如 DPO、ReMax）的泛化性尚未验证。

**二元标注的信息损失。** Pass/Fail 的二值简化虽降低了噪声，但必然丢失了细粒度质量差异信息。对于需要精细区分“优秀”与“尚可”的场景（如高质量视频筛选），二元标注可能不足以支撑。

**跨提示配对的隐含假设。** 该策略假设不同 prompt 下的 Pass/Fail 标签具有跨提示可比性，这在极端不平衡数据（如某 prompt 下几乎全为 Pass 或全为 Fail）中可能失效。论文未讨论此类边缘场景。

### 3. 开放问题与未来方向

1. **多维联合奖励模型。** 能否通过设计多个可学习查询向量，将物理、变形、语义等多维度的 HPQA 融合为一个统一的奖励模型？这将直接提升模型的实用性和部署效率。

2. **突破规模瓶颈。** 在更大规模参数（>14B）和更丰富、更多样的训练数据下，是否能突破当前的边际收益递减？可能需要配合数据增强或课程学习策略。

3. **跨模态与跨任务迁移。** 该方法的核心组件（二元标注、BT-WT 损失、HPQA）能否直接迁移到图像生成或图像到视频（I2V）任务的奖励模型训练？论文未涉及此类实验。

4. **自适应平局权重。** BT-WT 损失中的 μ=0.5 是否为最优平局权重？是否可通过元学习或基于标注置信度的自适应机制动态调整？BTT 的失败暗示权重设计需要谨慎。

5. **更广泛的 OOD 鲁棒性。** 当前 OOD 评估集仅覆盖四类 SOTA 模型（Wan2.1/2.2、Veo 3、Seedance 1.0），更广泛的分布偏移（如不同域、不同分辨率、不同时长）下的鲁棒性需进一步验证。

6. **标注一致性的进一步提升。** 二元标注的 IAA（α=0.4939）虽优于成对比较，但仍仅为中等水平。结合标注者校准训练、多轮标注或 LLM 辅助判定，是否能进一步提升一致性？

## 原文 PDF

![[paperPDFs/CVPR_2026/SoliReward_Mitigating_Susceptibility_to_Reward_Hacking_and_Annotation_Noise_in_Video_Generation_Reward_Models.pdf]]
