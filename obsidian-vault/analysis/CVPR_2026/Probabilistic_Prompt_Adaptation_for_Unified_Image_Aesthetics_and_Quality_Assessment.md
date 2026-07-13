---
title: Probabilistic Prompt Adaptation for Unified Image Aesthetics and Quality Assessment
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/Probabilistic_Prompt_Adaptation_for_Unified_Image_Aesthetics_and_Quality_Assessment.pdf
project_link: null
code_link: null
aliases:
- PPAP
- PPAUIAQA
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: 将文本提示作为隐变量，建模其适应性为条件于图像内容和任务上下文的概率分布，并在仅有任务级三元组监督下通过边缘化提示进行训练，从机制上解耦了提示灵活性与评分精度。
primary_logic: 无需任何提示级标注，仅利用（任务，图像，分数）三元组，通过动态推断LLM预采样提示的权重并边缘化，同时学习任务专用高精度评分和通用提示可控评分，构建了一个可解释的统一视觉-语言嵌入空间。
claims:
- PPA在低层感知属性（如对焦、色彩、对比度、曝光）上的提示-图像一致性显著优于CLIP-IQA和UniQA。
- 在AADB和SPAQ属性评估中，PPA使用属性导向提示时SRCC/PLCC提升显著高于不匹配属性，证明模型能捕捉语义线索。
- PPA在PARA、BAID、SPAQ数据集上达到最优性能，在其他数据集上与最佳结果差距在4%以内。
- PPA在AADB和SPAQ上均获得最高的类间/类内方差比（BW），并在SPAQ上获得最高轮廓系数（SS），表明更判别的特征空间。
---

# Probabilistic Prompt Adaptation for Unified Image Aesthetics and Quality Assessment

> [!tip] 核心洞察
> 无需任何提示级标注，仅利用（任务，图像，分数）三元组，通过动态推断LLM预采样提示的权重并边缘化，同时学习任务专用高精度评分和通用提示可控评分，构建了一个可解释的统一视觉-语言嵌入空间。

| 字段 | 内容 |
|------|------|
| 中文题名 | 面向统一图像美学与质量评估的概率性提示自适应 |
| 英文题名 | Probabilistic Prompt Adaptation for Unified Image Aesthetics and Quality Assessment |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://openaccess.thecvf.com/content/CVPR2026/html/Hara_Probabilistic_Prompt_Adaptation_for_Unified_Image_Aesthetics_and_Quality_Assessment_CVPR_2026_paper.html) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/image_and_video_generation |
| Method | Probabilistic Prompt Adaptation (PPA) |
| Dataset | PARA, BAID, SPAQ |

> [!tip] 效果简介
> - PARA (IAA) 上，SRCC 0.913 (PPA) vs 0.903 (IAACLIP) (+0.010)；PLCC 0.942 (PPA) vs 0.933 (IAACLIP) (+0.009)。
> - BAID (IAA) 上，SRCC 0.497 (PPA) vs 0.463 (IAACLIP) (+0.034)；PLCC 0.537 (PPA) vs 0.503 (IAACLIP) (+0.034)。
> - SPAQ (IQA) 上，SRCC 0.945 (PPA) vs 0.934 (GAMMA) (+0.011)。

## 概要

图像美学评估（IAA）与图像质量评估（IQA）是视觉感知研究中的两项核心任务，但现有模型长期面临一个结构性矛盾：固定提示方法虽能保持较高评分精度，却缺乏对多样化评估维度的灵活适应能力；而基于提示的方法虽可进行文本可控的评分，却严重依赖提示级或属性级文本标注的质量与数量，难以在任意提示下同时实现高精度与可控性。这一瓶颈的本质在于，模型未能将文本提示的适应性建模为条件于图像内容与任务上下文的内在机制，导致提示灵活性与评分精度之间的耦合无法解耦。

针对上述问题，本文提出**概率性提示自适应（Probabilistic Prompt Adaptation, PPA）**框架。PPA的核心思想是将文本提示视为隐变量，将其适应性建模为条件于图像内容和任务上下文的概率分布，并通过边缘化提示进行训练。具体而言，PPA利用大语言模型（LLM）预采样一组反义提示对构成提示池，通过一个可学习的提示选择模型动态估计每个提示在给定图像和任务下的适应性权重，最终以加权求和的方式得到任务条件评分。整个训练过程仅需（任务，图像，分数）三元组监督，无需任何提示级标注，从机制上实现了提示灵活性与评分精度的解耦。

实验结果表明，PPA在多个IAA和IQA基准数据集上取得了具有竞争力的表现。在PARA、BAID和SPAQ数据集上，PPA达到最优性能（PARA上SRCC 0.913/PLCC 0.942，SPAQ上SRCC 0.945/PLCC 0.952），在其他数据集上与最佳结果的差距控制在4%以内。人工评估进一步验证了PPA在低层感知属性（如对焦、色彩、对比度、曝光）上的提示-图像一致性显著优于CLIP-IQA和UniQA等基线方法。消融实验证实，动态学习提示权重相比固定均匀分布带来约5%的平均性能增益，且特征空间的分数可分离性在训练后显著提升。

图像美学评估（IAA）与图像质量评估（IQA）是计算机视觉中的两个核心任务，分别关注图像的审美吸引力和技术质量。随着社交媒体和用户生成内容的爆炸式增长，对图像进行自动化、多维度的评分需求日益迫切。然而，这两个任务长期以来被作为独立问题处理，缺乏统一的评估框架。

现有方法可大致分为两类。第一类以**NIMA**（Talebi and Milanfar, IEEE TIP 2018）和**MUSIQ**（Ke et al., ICCV 2021）为代表，采用端到端的卷积神经网络直接回归美学或质量分数。这类方法虽然评分精度较高，但输出的是单一维度的固定分数，无法根据不同的评估维度（如“对焦清晰度”“色彩和谐度”“构图平衡性”）提供可解释的、可控的评估结果。第二类方法借助视觉-语言模型（VLM）实现文本提示驱动的评估，如**CLIP-IQA**（Wang et al., AAAI 2023）利用CLIP的跨模态对齐能力，通过反义文本对（如“Good photo/Bad photo”）计算零样本质量分数；**UniQA**（Zhou et al., arXiv 2024）则进一步通过跨任务预训练实现了提示条件下的评分操控。

然而，基于提示的方法面临一个根本性瓶颈：**提示灵活性与评分精度之间的尖锐矛盾**。固定提示模型（如CLIP-IQA使用单一反义词对）虽然无需额外标注，但丧失了按需调整评估维度的能力；而可操控提示模型（如UniQA）的性能高度依赖于提示级或属性级文本标注的质量与数量，这类细粒度标注成本极高，难以大规模获取。这导致现有方法无法在保持高精度评分的同时，实现任意文本提示下的可控评估。

本文的核心动机正是打破这一僵局。我们观察到，文本提示本质上可以视为一个隐变量——不同的提示捕捉了图像在特定语义维度上的不同侧面，而任务（如“美学评估”或“质量评估”）则定义了这些侧面的聚合方式。基于这一洞见，本文提出**概率性提示自适应（Probabilistic Prompt Adaptation, PPA）**框架，将评分预测建模为提示的混合模型：模型动态推断每个提示在给定图像内容和任务上下文下的适应性权重，并通过边缘化所有提示得到最终的任务评分。这一机制从原理上解耦了提示灵活性与评分精度——训练仅需（任务，图像，分数）三元组，无需任何提示级标注；推理时则可接受任意文本提示，实现可控的多维度评估。

## 核心方法与创新机理

PPA的核心贡献在于将“提示”从固定的输入条件重新定义为可学习的隐变量，从而在机制层面解耦了文本提示的灵活性与评分精度。这一设计直接回应了现有方法的瓶颈：固定提示模型（如**NIMA**，Talebi and Milanfar, IEEE TIP 2018）缺乏灵活性，而基于提示的模型（如**CLIP-IQA**，Wang et al., AAAI 2023；**UniQA**，Zhou et al., arXiv 2024）要么依赖固定反义提示或集成，要么受限于提示级文本标注的质量与数量，难以在保持高精度的同时实现任意提示下的可控评估。

PPA通过两个关键的**changed slots**实现了突破：

**1. 评分机制：从固定提示到任务条件概率边缘化**

现有基于提示的方法通常采用固定反义提示对（如“Good photo/Bad photo”）或固定提示集成来计算评分。PPA则将评分建模为提示空间上的混合分布。具体而言，PPA利用大语言模型（GPT-5）预采样一个包含260个反义提示的提示池 $\mathcal{T}_{\mathrm{samp}}$，然后通过一个可学习的提示选择模型 $p_{\phi}(t \mid x, c)$ 动态估计每个提示 $t$ 在给定图像 $x$ 和任务上下文 $c$ 下的适应性权重。最终的任务条件评分通过对所有采样提示的CLIP-IQA得分进行加权期望得到：

$$\mathbb{E}_{p(s|x,c)}[s] = \sum_{t \in \mathcal{T}_{\mathrm{samp}}} \bar{s}_{\theta}(x,t) \, p_{\phi}(t \mid x, c)$$

这一概率边缘化机制（Eq. 2）使模型能够根据图像内容和评估任务自动选择最相关的语义提示，而无需人工指定。消融实验证实，动态学习提示权重（条件于任务和图像）相比固定均匀分布带来了显著增益：12个数据集上的平均SRCC从0.759提升至0.808，PLCC从0.778提升至0.828（Table 7）。

**2. 训练监督需求：从提示级标注到任务级三元组**

现有方法通常需要提示级或属性级文本标注（如“这张图的对焦好吗？”），或仅使用固定提示进行微调。PPA则完全摆脱了这一限制：训练仅需（任务，图像，分数）三元组，无需任何提示级标注。其训练目标是最小化边缘似然的负对数：

$$\mathcal{L} = -\sum_{i=1}^N \log \sum_{t \in \mathcal{T}_{\mathrm{samp}}} \exp\left(-\frac{(s_i - \bar{s}_{\theta}(x_i,t))^2}{2\sigma^2}\right) p_{\phi}(t | x_i, c_i) + \mathrm{const}$$

该目标函数（Eq. 5）同时优化CLIP图像编码器的最后四层（评分模型 $\theta$）和提示选择模型（$\phi$），在仅有任务级分数监督的条件下，隐式地学习哪些提示对特定任务和图像是合适的。这一设计使得PPA能够在保持高精度的同时，获得对任意文本提示的可控响应能力。

**创新机制的本质**

PPA的核心洞察在于：通过将文本提示作为隐变量并对其边缘化，模型在训练过程中被迫学习一个可解释的统一视觉-语言嵌入空间。在这个空间中，不同提示对应不同的评分“视角”，而提示选择模型则学习如何为每个（图像，任务）组合分配最优的视角权重。训练后的特征空间展现出更强的分数可分离性：在AADB数据集上，类间/类内方差比（BW）从0.0056升至0.0102；在SPAQ数据集上，BW从0.0204升至0.1006，轮廓系数（SS）从-0.0217升至0.0339（Table 6），均优于固定提示微调。

**与相关工作的本质差异**

与**GAMMA**（Zhou et al., ACM MM 2025）的专家混合方法不同，PPA的“专家”是自然语言提示，具有天然的语义可解释性。与**MUSIQ**（Ke et al., ICCV 2021）的多尺度Transformer架构不同，PPA的创新不在于骨干网络设计，而在于概率化的提示自适应机制，这使得单一模型能够同时处理IAA和IQA任务，并在保持感知一致性的前提下灵活响应多样化的评估标准。

PPA 的整体架构如图 2 所示，由两个核心模块构成：**提示特定评分（Prompt-Specific Scoring）** 和**任务特定评分（Task-Specific Scoring）**。前者负责在任意文本提示下对图像进行可控评分，后者将前者纳入一个概率混合框架，在仅有任务级监督的条件下学习提示的动态适应性权重，从而实现高精度的统一评估。

### 输入输出流

系统的输入为三元组 `(图像 x, 任务 c, 分数 s)`。任务 `c` 标识评估类型（如美学评估 IAA 或质量评估 IQA），分数 `s` 为标量标注。输出为任务条件下的期望分数 `E[s | x, c]`，同时模型保留了在任意显式文本提示 `t` 下输出分数 `s(x, t)` 的能力，实现了可控评估。

### 提示特定评分

该模块基于 CLIP-IQA 的评分机制，计算图像 `x` 与一对反义文本提示 `t = (t_pos, t_neg)` 的余弦相似度，通过 softmax 得到归一化分数：

$$
\bar{s}(x,t) = \frac{\exp(I(x)^\top T(t_{\mathrm{pos}}))}{\exp(I(x)^\top T(t_{\mathrm{pos}})) + \exp(I(x)^\top T(t_{\mathrm{neg}}))}
$$

其中 `I(x)` 和 `T(t)` 分别为 CLIP 图像编码器和文本编码器的输出。该分数天然支持任意文本提示的可控评分，但单独使用时缺乏任务级精度。

### 任务特定评分与提示选择

PPA 的核心创新在于将分数预测形式化为提示的混合模型。任务 `c` 条件下的分数分布通过边缘化所有可能提示得到：

$$
p(s \mid x, c) = \sum_{t \in \mathcal{T}} p_{\theta}(s \mid x, t) p_{\phi}(t \mid x, c)
$$

其中 `p_θ(s | x, t)` 是以 CLIP-IQA 分数为均值的高斯分布（式 4），`p_φ(t | x, c)` 是**提示选择模型**估计的提示适应性概率。

提示选择模型通过两层 MLP 分别将图像-任务联合嵌入 `f_φ1(x, c)` 和提示-任务联合嵌入 `g_φ2(t, c)` 映射到共享空间，经 softmax 计算每个采样提示的权重：

$$
p_{\phi}(t \mid x, c) = \frac{\exp\left(f_{\phi_1}(x,c)^\top g_{\phi_2}(t,c)\right)}{\sum_{t' \in \mathcal{T}_{\mathrm{samp}}} \exp\left(f_{\phi_1}(x,c)^\top g_{\phi_2}(t',c)\right)}
$$

为近似全提示空间的求和，PPA 利用 GPT-5 预采样生成包含 260 个反义提示的提示池 `T_samp`（80 个属性专用提示 + 180 个非属性提示）。

### 训练与推理

训练阶段，PPA 最小化负对数似然，同时优化 CLIP 图像编码器的最后四层和提示选择模型：

$$
\mathcal{L} = -\sum_{i=1}^N \log \sum_{t \in \mathcal{T}_{\mathrm{samp}}} \exp\left(-\frac{(s_i - \bar{s}_{\theta}(x_i,t))^2}{2\sigma^2}\right) p_{\phi}(t | x_i, c_i) + \mathrm{const}
$$

这一设计使得模型仅需 `(任务, 图像, 分数)` 三元组即可训练，无需任何提示级标注。推理时，最终任务评分通过期望加权得到：

$$
\mathbb{E}_{p(s|x,c)}[s] = \sum_{t \in \mathcal{T}_{\mathrm{samp}}} \bar{s}_{\theta}(x,t) p_{\phi}(t \mid x, c)
$$

### 关键机制

整个框架的因果调节点在于：**将文本提示视为隐变量，建模其适应性为条件于图像内容和任务上下文的概率分布**。这从机制上解耦了提示灵活性与评分精度——提示特定评分保证任意文本的可控性，而任务边缘化训练保证高精度，二者通过动态推断的提示权重实现统一。

![[assets/figures/papers/paper_list_l2335_https_openaccess_thecvf_com_content_CVPR2026_html_Hara_Probabilistic_Pro/figures/002_Figure_2.jpg]]
*Figure 2: Overview of the proposed method PPA for IAA/IQA score prediction. The proposed framework consists of prompt-specific scoring, which predicts a score s from an image x and a text prompt t, and task-specific scoring, which encompasses the former and predicts s from an image x and a task c. In prompt-specific scoring, an image x and a text prompt t are embedded using the CLIP encoders, and a prompt-conditioned score distribution*

![[assets/figures/papers/paper_list_l2335_https_openaccess_thecvf_com_content_CVPR2026_html_Hara_Probabilistic_Pro/figures/001_Figure_1.jpg]]
*Figure 1: The proposed framework PPA provides a unified, textdriven approach to evaluating image aesthetics and visual quality. Each row illustrates examples of score predictions for antonymous text pairs, showing that PPA can flexibly adjust its evaluation according to nuanced textual instructions. This flexibility allows a single model to handle both IAA and IQA tasks while maintaining perceptual consistency across diverse prompts and evaluation criteria. All example images are sampled from the Open Images Dataset [30]*

### 3.1 整体架构

PPA 框架由两大核心模块构成：**提示特定评分（Prompt-Specific Scoring）** 和 **任务特定评分（Task-Specific Scoring）**，后者以前者为基础，通过概率边缘化实现从任务上下文到评分的映射。整体架构如 Figure 2 所示。

#### 提示特定评分模块

给定图像 $x$ 和一对反义文本提示 $t = (t_{\text{pos}}, t_{\text{neg}})$，该模块利用 CLIP 的图像编码器 $I(\cdot)$ 和文本编码器 $T(\cdot)$ 分别提取特征，通过余弦相似度的 softmax 计算评分：

$$\bar{s}(x,t) = \frac{\exp(I(x)^\top T(t_{\text{pos}}))}{\exp(I(x)^\top T(t_{\text{pos}})) + \exp(I(x)^\top T(t_{\text{neg}}))} \tag{1}$$

该评分 $\bar{s}(x,t) \in [0,1]$ 反映了图像 $x$ 与正向提示 $t_{\text{pos}}$ 在 CLIP 联合嵌入空间中的相对对齐程度。这一基础评分机制继承了 **CLIP-IQA**（Wang et al., AAAI 2023）的零样本能力，使模型天然支持任意文本提示下的可控评分。

#### 任务特定评分模块

PPA 的核心创新在于将任务条件下的评分建模为提示的混合分布。对于给定的评估任务 $c$（如“美学评估”或“图像质量评估”），分数 $s$ 的条件概率通过边缘化所有可能提示得到：

$$p(s \mid x, c) = \sum_{t \in \mathcal{T}} p_{\theta}(s \mid x, t) \, p_{\phi}(t \mid x, c) \tag{2}$$

其中：
- $p_{\theta}(s \mid x, t)$ 是给定提示 $t$ 下的分数似然，以式 (1) 的 CLIP-IQA 得分为均值建模为高斯分布；
- $p_{\phi}(t \mid x, c)$ 是提示选择模型，估计提示 $t$ 对当前图像 $x$ 和任务 $c$ 的适应性权重。

### 3.2 提示选择模型

提示选择模型通过两个 MLP 将图像-任务联合嵌入和提示-任务联合嵌入映射到共享空间，以 softmax 计算每个采样提示的概率：

$$p_{\phi}(t \mid x, c) = \frac{\exp\left(f_{\phi_1}(x,c)^\top g_{\phi_2}(t,c)\right)}{\sum_{t' \in \mathcal{T}_{\text{samp}}} \exp\left(f_{\phi_1}(x,c)^\top g_{\phi_2}(t',c)\right)} \tag{3}$$

其中：
- $f_{\phi_1}(\cdot)$ 将图像 $x$ 和任务上下文 $c$ 映射为联合嵌入；
- $g_{\phi_2}(\cdot)$ 将提示 $t$ 和任务上下文 $c$ 映射为联合嵌入；
- $\mathcal{T}_{\text{samp}}$ 为从 LLM 预采样的提示集合。

### 3.3 分数似然建模

为将离散的 CLIP 评分转换为连续概率分布，PPA 将 $p_{\theta}(s \mid x, t)$ 建模为以 $\bar{s}_{\theta}(x,t)$ 为均值、固定方差 $\sigma^2$ 的高斯分布：

$$p_{\theta}(s \mid x, t) = \frac{1}{\sqrt{2\pi\sigma^2}} \exp\left(-\frac{(s - \bar{s}_{\theta}(x,t))^2}{2\sigma^2}\right) \tag{4}$$

### 3.4 LLM 提示采样

由于全提示空间 $\mathcal{T}$ 无法穷举，PPA 利用 GPT-5 预生成美学与质量相关的反义提示池，共 260 个提示（80 个属性专用提示 + 180 个非属性提示），以近似式 (2) 中的求和。消融实验（Table 8）表明，该配置在 12 个数据集上取得最优平均性能，继续增加提示数量反而导致性能下降。

### 3.5 训练目标

PPA 的训练仅需（任务，图像，分数）三元组，无需任何提示级标注。训练目标为最小化负对数似然：

$$\mathcal{L} = -\sum_{i=1}^N \log \sum_{t \in \mathcal{T}_{\text{samp}}} \exp\left(-\frac{(s_i - \bar{s}_{\theta}(x_i,t))^2}{2\sigma^2}\right) p_{\phi}(t \mid x_i, c_i) + \text{const} \tag{5}$$

训练时同时优化图像编码器的最后四层和提示选择模型参数 $\phi$，实现评分精度与提示权重的联合学习。

### 3.6 推理时的评分预测

推理阶段，任务条件评分通过期望形式计算，即对采样提示的 CLIP-IQA 分数以学习到的提示概率加权求和：

$$\mathbb{E}_{p(s|x,c)}[s] = \sum_{t \in \mathcal{T}_{\text{samp}}} \bar{s}_{\theta}(x,t) \, p_{\phi}(t \mid x, c) \tag{6}$$

这一机制从因果层面解耦了提示灵活性与评分精度：提示选择模型 $p_{\phi}$ 负责动态推断任务与图像相关的提示权重，而提示特定评分模块 $\bar{s}_{\theta}$ 保持高精度评分能力，二者通过边缘化无缝融合。

## 实验与关键发现

### 核心性能

PPA在三个基准上取得了最优性能，并在其余数据集上与最佳结果差距保持在4%以内。在美学评估（IAA）任务上，PPA在PARA数据集上SRCC达0.913、PLCC达0.942，分别超越IAACLIP 0.010和0.009；在更具挑战性的BAID数据集上，SRCC和PLCC分别提升0.034，达到0.497和0.537（Table 4）。在图像质量评估（IQA）任务上，PPA在SPAQ数据集上SRCC达0.945、PLCC达0.952，超越GAMMA（Zhou et al., ACM MM 2025）0.011和0.009（Table 5）。这一性能优势源于概率提示边缘化机制：模型通过动态推断提示权重，在无需提示级标注的情况下，同时保持了评分精度与提示可控性。

![[assets/figures/papers/paper_list_l2335_https_openaccess_thecvf_com_content_CVPR2026_html_Hara_Probabilistic_Pro/figures/008_Table_4.jpg]]
*Table 4: Comparison of model performance on IAA datasets. The best results are highlighted in bold*

![[assets/figures/papers/paper_list_l2335_https_openaccess_thecvf_com_content_CVPR2026_html_Hara_Probabilistic_Pro/figures/009_Table_5.jpg]]
*Table 5: Comparison of model performance on IQA datasets. The best results are highlighted in bold*

### 提示-图像一致性验证

Table 1展示了PPA与CLIP-IQA（Wang et al., AAAI 2023）和UniQA（Zhou et al., arXiv 2024）在提示-图像一致性上的人工评估结果。该评估基于757名参与者、每提示300组成对比较。PPA在低层感知属性上表现显著优于基线：在“聚焦高质量照片”（focused high-quality photo）提示下，PPA以200:100胜出（p=0.000）；在“模糊照片”（murky photo）上以176:124胜出（p=0.002）；在“清晰边缘”（clean-edge）上以189:111胜出（p=0.000）。然而，对于抽象或情感化美学提示（如“温暖而美丽的照片”），PPA的一致性有所下降，与CLIP-IQA相比为155:145（p=0.302，不显著），且弱于UniQA的131:169（p=0.012）。这一失败模式揭示了当前方法的瓶颈：LLM生成的提示池在语义多样性上有限，难以充分覆盖高层次美学概念的细粒度语义空间。

### 属性导向评估

PPA在AADB和SPAQ的属性导向评估中验证了其对语义线索的捕捉能力。Table 2显示，在AADB上，使用匹配属性的提示进行训练后，运动模糊属性的△SRCC达0.580，而不匹配组仅为0.507；Table 3显示，在SPAQ上，对比度属性的△SRCC为0.615，不匹配组仅为0.210。这种显著的匹配/不匹配差异表明，模型并非简单地记忆分数分布，而是真正通过文本提示捕捉了与特定感知属性相关的视觉语义特征。

### 特征空间分析

Table 6通过轮廓系数（SS）和类间/类内方差比（BW）量化了特征空间的判别能力。PPA训练后，AADB上的BW从0.0056升至0.0102，SPAQ上的BW从0.0204大幅升至0.1006，SS从-0.0217升至0.0339，均优于固定提示微调方法。这表明概率提示自适应机制不仅提升了评分精度，更从根本上改善了视觉-语言嵌入空间的结构，使其按评分等级形成更清晰的分离。

### 消融实验

**动态权重学习的必要性。** Table 7的消融表明，将固定均匀分布的提示权重替换为动态学习的条件权重（同时条件于任务和图像），在12个数据集上平均SRCC从0.759提升至0.808，PLCC从0.778提升至0.828。移除任务条件化或图像条件化均导致性能下降，验证了双条件提示选择机制的有效性。

**提示池规模的影响。** Table 8显示，使用260个提示（80个属性专用提示+180个非属性提示）时性能最优。继续增加提示数量反而导致性能下降，说明当前LLM生成的提示池存在语义冗余，过多的相似表达引入了噪声而非有效信息增益。这一发现与前述抽象美学提示上的失败模式相互印证，共同指向提示池语义丰富度的瓶颈。

![[assets/figures/papers/paper_list_l2335_https_openaccess_thecvf_com_content_CVPR2026_html_Hara_Probabilistic_Pro/figures/007_Figure_4.jpg]]
*Figure 4: t-SNE visualization of image features before and after training. Images are divided into three groups based on their annotated scores (top, middle, and bottom). After training, the feature space exhibits clearer separation according to score levels*

![[assets/figures/papers/paper_list_l2335_https_openaccess_thecvf_com_content_CVPR2026_html_Hara_Probabilistic_Pro/figures/012_Table_7.jpg]]
*Table 7: Ablation study on the effect of weight learning, task conditioning, and image conditioning*

## 定位与知识库关联

### 与现有方法的继承与差异

PPA 的核心机制建立在视觉-语言模型用于图像质量/美学评估的两条技术路线之上，但通过概率化提示自适应实现了关键突破。

**基于固定提示的零样本评估方法**，以 **CLIP-IQA** (Wang et al., AAAI 2023) 为代表，利用 CLIP 的视觉-语言对齐能力，通过手工设计的反义提示对（如“Good photo / Bad photo”）计算图像与文本的余弦相似度 softmax 得分。该方法无需训练即可获得与人类感知相关的质量评分，但其评估维度完全受限于固定的提示设计，无法针对特定任务或属性进行灵活调整。

**基于提示微调的统一评估方法**，如 **UniQA** (Zhou et al., arXiv 2024)，尝试通过大规模预训练将 IAA 和 IQA 统一到同一框架下，并支持以文本提示为条件的可控评分。然而，这类方法通常需要提示级或属性级的文本标注，标注成本高且限制了提示空间的扩展性。

PPA 在这两条路线的基础上进行了机制层面的重构：

1. **从固定提示到概率化提示混合**：将评分建模为提示集合上的混合分布 $p(s \mid x, c) = \sum_{t \in \mathcal{T}} p_{\theta}(s \mid x, t) p_{\phi}(t \mid x, c)$，其中提示权重 $p_{\phi}(t \mid x, c)$ 同时条件于图像内容和任务上下文，实现了从“硬编码提示”到“软性提示自适应”的转变。

2. **从提示级监督到任务级监督**：通过边缘化提示变量，PPA 仅需（任务，图像，分数）三元组即可完成训练，完全消除了对提示级标注的依赖。这一设计使得模型可以从 LLM（GPT-5）预采样的大规模提示池中自由选择，而无需人工为每个提示标注对应的分数。

3. **与经典端到端方法的对比**：**NIMA** (Talebi and Milanfar, IEEE TIP 2018) 等 CNN 方法直接回归美学评分分布，精度高但缺乏文本可控性；**MUSIQ** (Ke et al., ICCV 2021) 通过多尺度 Transformer 提升 IQA 精度，但同样不支持提示条件评估；**GAMMA** (Zhou et al., ACM MM 2025) 采用专家混合架构实现多任务自适应，但未涉及文本提示的概率化建模。PPA 在保持与这些方法可比精度的同时，额外提供了任意提示下的可控评估能力。

### 适用边界

PPA 的优势场景和局限性可从以下维度界定：

**优势适用场景**：
- **低层感知属性评估**：人工评估实验（Table 1）表明，PPA 在“对焦清晰的高质量照片”（PPA 200/100, p=0.000）、“画面浑浊的照片”（176/124, p=0.002）、“边缘清晰的照片”（189/111, p=0.000）等低层感知属性上的提示-图像一致性显著优于 CLIP-IQA 和 UniQA。
- **属性导向的细粒度评估**：在 AADB 和 SPAQ 的属性评估中，PPA 使用匹配属性的提示时 SRCC/PLCC 提升显著高于不匹配属性（如 AADB 运动模糊 △SRCC 0.580 vs 0.507；SPAQ 对比度 △SRCC 0.615 vs 0.210），证明模型能有效捕捉语义线索。
- **多任务统一评估**：PPA 在 PARA、BAID、SPAQ 三个数据集上达到最优性能，在其他数据集上与最佳结果的差距在 4% 以内，验证了其作为统一 IAA/IQA 框架的竞争力。

**已知局限性**：
- **抽象/情感类美学提示**：对于“温暖而美丽的照片”等高层抽象提示，PPA 的一致性有所下降（Table 1：PPA 155/145 vs UniQA 131/169, p=0.302），部分原因在于 LLM 生成的提示池在语义多样性上有限，难以覆盖复杂的美学语义空间。
- **提示池规模与质量依赖**：消融实验（Table 8）显示，使用 260 个提示（80 属性专用 + 180 非属性）时性能最优，继续增加提示数量反而导致性能下降。这表明提示池中语义相似表达的数量和质量直接限制了模型捕捉复杂美学线索的能力。

### 开放问题与未来方向

1. **提示池的语义扩展**：当前 LLM 生成的提示池在抽象美学维度的覆盖不足。如何通过更丰富的语义表达（如引入美学理论术语、多语言描述、风格化表达）扩展提示池，以提升模型对复杂美学线索的捕捉能力，是一个值得探索的方向。

2. **与多模态大语言模型的深度融合**：PPA 目前将 LLM 仅用于提示预采样，训练过程与 LLM 解耦。如何将 PPA 与 MLLM 端到端融合，实现提示的自动优化和更自适应的视觉评估，可能进一步提升框架的灵活性和表达能力。

3. **零样本与跨任务泛化**：当前评估仅限于固定任务集上的训练和测试。PPA 的概率化提示自适应机制在零样本或跨任务迁移场景下的泛化能力尚未被验证，这是评估其作为通用评估框架潜力的关键未解问题。

4. **特征空间可解释性的深化**：虽然 t-SNE 可视化和类间/类内方差比分析（Table 6）表明 PPA 训练后特征空间具有更强的分数可分性，但提示权重 $p_{\phi}(t \mid x, c)$ 的学习过程与特征空间结构之间的因果关系仍需更深入的理论分析。

## 原文 PDF

![[paperPDFs/CVPR_2026/Probabilistic_Prompt_Adaptation_for_Unified_Image_Aesthetics_and_Quality_Assessment.pdf]]
