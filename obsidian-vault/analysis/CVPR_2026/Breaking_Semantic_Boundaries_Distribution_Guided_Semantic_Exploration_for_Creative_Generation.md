---
title: "Breaking Semantic Boundaries: Distribution-Guided Semantic Exploration for Creative Generation"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/Breaking_Semantic_Boundaries_Distribution_Guided_Semantic_Exploration_for_Creative_Generation.pdf
project_link: null
code_link: null
aliases:
- BSBDGSECG
tags:
- CVPR_2026
- topic/generative_models_diffusion
- topic/benchmarks_datasets_evaluation
- topic/generative_models_diffusion/diffusion_image_video
core_operator: 以类别分布（class distribution）替代传统的文本提示作为生成条件，实现可量化的概念融合控制。
primary_logic: 受分类器对分布外输入产生软概率分布的启发，逆向使用分类过程，将未知概念表征为已知类别上的分布，并以此分布为条件进行图像生成，从而在保持可控性的同时突破固定语义空间。
claims:
- 提出Distribution-Conditional Generation范式，以类别分布为条件建模新概念，实现细粒度可控的创造性生成。
- DisTok通过概念池和双向训练目标（连续融合、分布一致性）逐渐生成更复杂且语义一致的新概念。
- DisTok在推理效率上相比BASS和ConceptLab分别实现13倍和40倍加速。
- CangJie TP2O text pairs 上 VQAScore = 0.840
---

# Breaking Semantic Boundaries: Distribution-Guided Semantic Exploration for Creative Generation

> [!tip] 核心洞察
> 受分类器对分布外输入产生软概率分布的启发，逆向使用分类过程，将未知概念表征为已知类别上的分布，并以此分布为条件进行图像生成，从而在保持可控性的同时突破固定语义空间。

| 字段 | 内容 |
|------|------|
| 中文题名 | 打破语义边界：面向创造性生成的分布引导语义探索 |
| 英文题名 | Breaking Semantic Boundaries: Distribution-Guided Semantic Exploration for Creative Generation |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://openaccess.thecvf.com/content/CVPR2026/html/Feng_Breaking_Semantic_Boundaries_Distribution-Guided_Semantic_Exploration_for_Creative_Generation_CVPR_2026_paper.html) |
| Topic | #topic/generative_models_diffusion #topic/benchmarks_datasets_evaluation #topic/generative_models_diffusion/diffusion_image_video |
| Method | DisTok |
| Dataset | CangJie TP2O text pairs, Distribution-Conditional Generation, User study, Inference speed |

> [!tip] 效果简介
> - CangJie TP2O text pairs 上，VQAScore 0.840 vs BASS: 0.812, CreTok: 0.827 (approx.) (+0.028 / +0.013)。
> - Distribution-Conditional Generation (CangJie) 上，GPT-4o Aesthetics 9.9±0.1 vs SOTA T2I models (lower scores) (显著优于)。
> - User study (creative generation) 上，user preference (votes DisTok vs. FLUX) 278 vs 222 (+56 votes)。

## 概要

### 问题背景

现有文本到图像生成模型虽然在训练分布内表现出色，但其创造力受限于固定的语义边界——它们难以生成真正新颖的、超出训练分布的概念。已有的创造性生成方法（如 **BASS** (Li et al., ECCV 2024)、**CreTok** (Feng et al., CVPR 2025)）仅支持离散的两两概念组合，缺乏对多概念细粒度分布的控制；而 **ConceptLab** (Richardson et al., ACM TOG 2024) 的无条件探索又难以提供可控的语义引导。这些方法的共同瓶颈在于：**以文本提示为生成条件**的范式本身限制了概念空间的连续性和可量化性。

### 核心思路

本文提出 **Distribution-Conditional Generation（分布条件生成）** 范式，其核心洞察源自一个逆向思维：分类器对分布外输入会产生软概率分布，那么能否反过来，用类别分布作为条件来生成图像？具体而言，将未知概念表征为已知类别上的一个分布向量，并以此分布为条件进行图像生成，从而在保持可控性的同时突破固定语义空间。

基于该范式，作者提出了 **DisTok**——一个编码器-解码器框架，统一了条件式与无条件式的语义探索。DisTok 维护一个**概念池（Concept Pool）**，通过两个互补的训练目标——**连续概念融合（Continuous Concept Fusion）**与**分布一致性强化（Distribution Consistency Enforcement）**——逐步生成语义一致且日益复杂的新概念。

### 关键结果

- **图文对齐**：在 CangJie TP2O 基准上，DisTok 的 VQAScore 达到 0.840，优于 BASS（0.812）和 CreTok（约 0.827）。
- **创造力评估**：GPT-4o 美学评分达 9.9±0.1，显著优于现有 T2I 模型。
- **人工偏好**：用户研究中 DisTok 以 278 票对 222 票胜出 FLUX。
- **推理效率**：每个概念的生成时间约 3 秒，相比 BASS 加速 13 倍，相比 ConceptLab 加速 40 倍。

### 方法谱系与知识库定位

DisTok 处于**创造性 T2I 生成**与**概念融合**的交汇点。与依赖文本提示的传统方法（Stable Diffusion 3, FLUX）不同，DisTok 将生成条件从离散的文本提示替换为**连续的类别分布**，通过 Distribution Encoder 编码后由 Creative Decoder 解码为概念令牌，再嵌入自然语言提示中指导扩散模型生成。这一设计使其既能进行有引导的条件探索（指定类别对融合），也能从高斯先验中随机采样进行无条件探索，并通过预训练 VLM 对生成结果进行分布估计以闭环监督。在概念融合方法中，DisTok 区别于 BASS 的交换采样机制和 ConceptLab 的相似度降低策略，首次实现了**多概念细粒度分布级别的可控融合**。



### 文本到图像生成中的语义边界困境

近年来，文本到图像（T2I）扩散模型取得了令人瞩目的进展，**Stable Diffusion 3**（Esser et al., ICML 2024）和 **FLUX** 等先进模型已能根据自然语言描述生成高质量、高保真度的图像。然而，这些模型的生成能力本质上受限于其训练分布——它们擅长复现和重组训练数据中已见过的视觉概念，却难以创造出真正新颖的、超出分布（out-of-distribution）的视觉概念。

这一困境的核心在于**语义边界**的存在：T2I 模型将语义空间离散化为固定的类别或文本描述，导致模型只能在已知概念的组合空间内运作。当用户希望生成“介于猫和老虎之间的生物”或“融合东方与西方建筑风格的新建筑”时，传统提示工程（prompt engineering）往往力不从心——文本描述难以精确刻画连续的概念融合过程，生成结果要么偏向某一已知概念，要么产生语义不一致的混乱输出。

### 现有创造性生成方法的局限

针对上述问题，研究者已提出若干面向创造性生成的方法，但它们存在共同的结构性缺陷：

**离散的两两概念融合范式。** **BASS (TP2O)**（Li et al., ECCV 2024）通过交换采样实现两两概念的融合，**CreTok**（Feng et al., CVPR 2025）则聚焦于组合语义的创造性生成。然而，这些方法仅支持离散的两两概念组合，缺乏对多概念细粒度分布的控制能力。当需要融合三个或更多概念，或需要精确控制各概念的融合比例时，这些方法便无法有效应对。

**无条件的随机探索范式。** **ConceptLab**（Richardson et al., ACM TOG 2024）采取另一条路径：通过降低生成结果与现有概念的相似度来进行无条件的新颖性探索。这种方法虽然能发现新概念，但缺乏对生成方向的精确控制，探索过程盲目且效率低下——用户无法指定“我希望生成一个融合了A和B特征的新事物”，只能被动接受模型随机产生的任何新颖输出。

**根本瓶颈：语义空间的可控性缺失。** 上述方法的共同症结在于，它们都试图在固定的语义空间内进行探索，而未能从根本上改变生成条件的表达方式。文本提示作为生成条件，天然具有离散性和模糊性，难以承载连续的、细粒度的语义融合信息。因此，真正打破语义边界的关键，在于**重新定义生成条件的形式**。

### 核心动机：从文本提示到类别分布

本文的核心洞察来源于一个有趣的观察：当分类器面对分布外输入时，它不会简单地拒绝分类，而是输出一个软概率分布（soft probability distribution）——例如，一个“猫虎融合”的生物可能被分类器以 0.6 的概率判为猫、0.4 的概率判为虎。这个软分布恰恰捕捉了该未知概念在已知类别空间中的“位置”。

受此启发，本文提出**逆向使用分类过程**：既然分布外概念可以在已知类别上产生有意义的软分布，那么我们能否反过来，以类别分布为条件来生成图像？换言之，**将未知概念表征为已知类别上的分布，并以此分布为条件进行图像生成**，从而在保持可控性的同时突破固定语义空间的限制。

这一思路带来了范式级的转变：生成条件从离散的文本提示变为连续的类别分布（class distribution），使得概念融合变得可量化、可微分、可精细控制。用户可以通过调整分布中各已知类别的权重，精确控制融合概念中不同语义成分的强度——例如，将“猫”的权重从 0.3 逐步调至 0.7，生成结果便从“更像虎”平滑过渡到“更像猫”。

### 研究目标

基于上述动机，本文提出 **Distribution-Conditional Generation（分布条件生成）** 这一新范式，并设计 **DisTok** 框架作为其具体实现。DisTok 旨在统一条件性与无条件性的语义探索，通过编码器-解码器架构将类别分布映射为可嵌入自然语言提示的创造性概念令牌，从而在保持与现有 T2I 模型兼容性的同时，实现高效、灵活、细粒度可控的新颖视觉概念发现。



## 核心方法与创新机理

DisTok 的核心创新在于**将创造性生成的语义条件从离散的文本提示转换为连续可控的类别分布**，并围绕这一范式转移构建了统一的编码器-解码器框架，实现了细粒度、可量化的多概念融合与无条件语义探索。

### 1. 范式转移：从文本提示到类别分布

现有创造性生成方法（如 **BASS**（Li et al., ECCV 2024）、**CreTok**（Feng et al., CVPR 2025））依赖文本提示作为生成条件，仅支持离散的两两概念组合，缺乏对多概念融合程度的细粒度控制。DisTok 提出 **Distribution-Conditional Generation** 范式，以类别分布（class distribution）替代文本提示作为生成条件——将未知或新颖概念表征为已知类别上的概率分布，并以此分布为条件进行图像生成。这一设计的核心洞察在于：分类器对分布外输入会产生软概率分布，逆向使用这一过程，便可在保持可控性的同时突破固定语义空间的边界。

具体实现上，DisTok 引入 **Distribution Encoder**（$\mathcal{E}_{\mathrm{dis}}$）将 $K$ 维类别分布 $p_c$ 映射为低维潜在向量 $z = \mathcal{E}_{\mathrm{dis}}(p_c) \in \mathbb{R}^{\delta}$，再由 **Creative Decoder**（$\mathcal{D}_{\mathrm{tok}}$）解码为与提示嵌入对齐的创造性概念令牌 $t_{\mathrm{crt}} = \mathcal{D}_{\mathrm{tok}}(z) \in \mathbb{R}^{d}$（$\delta \ll d$）。这一编码器-解码器架构使得概念融合程度可通过调整类别分布的权重实现连续、精确的控制，而非仅限于离散的“有或无”组合。

### 2. 统一的探索策略：条件融合与无条件发现

此前的方法将条件生成（如 BASS 的交换采样融合）与无条件探索（如 **ConceptLab**（Richardson et al., ACM TOG 2024）的相似度降低策略）视为分离的任务。DisTok 将二者统一于同一框架内：

- **Continuous Concept Fusion**：从 Concept Pool 中随机采样类别对，将两者的令牌相加后经编码-解码生成融合概念，通过语义融合损失 $\mathcal{L}_{\mathrm{mix}}$ 训练解码器生成反映日益复杂类别分布的令牌。与 BASS 的离散两两融合不同，DisTok 的融合是渐进式的——Concept Pool 不断纳入新发现的概念，使得后续融合可涉及更多概念组合，逐步提升创造复杂度。

- **无条件随机探索**：得益于训练中引入的潜在正则化损失 $\mathcal{L}_{\mathrm{reg}} = \frac{1}{\sigma(z)^2} \mathbb{E}_z \left[ ||\boldsymbol{\mu}(z)||_2^2 \right]$，潜在空间被规范化为零均值、充分方差的结构。这使得 DisTok 可直接从任意零均值、单位方差的分布（如高斯、拉普拉斯、柯西分布）采样潜在向量并解码为新颖概念令牌，无需 ConceptLab 所需的迭代优化过程。

### 3. 分布一致性监督：闭合语义对齐回路

此前方法仅通过提示级语义融合间接监督生成质量，缺乏对生成图像与目标分布之间显式的对齐机制。DisTok 引入 **Distribution Consistency Enforcement**：利用预训练 VLM 从生成图像中预测类别分布，并与输入分布对齐。具体而言，从 Concept Pool 采样新颖令牌 $t_{\mathrm{nvl}}$，根据其类别分布加权组合已知令牌，编码-解码后得到 $t_{\mathrm{crt}}$，通过分布一致性损失 $\mathcal{L}_{\mathrm{cst}} = 1 - \cos(E(t_{\mathrm{crt}}), E(t_{\mathrm{nvl}}))$ 强制视觉语义与指定类别分布一致。这一闭合回路使得生成结果不仅“看起来像”目标概念，更在可量化的类别分布层面与设计意图对齐。

消融实验验证了这一机制的关键作用：移除分布一致性监督后，KL 散度从 0.0602 升至 0.0732，生成图像与目标分布的对齐度明显下降（Table 4）。

### 4. 效率突破：单次前向替代迭代优化

BASS 和 ConceptLab 在生成每个新概念时需进行迭代优化（分别约 40 秒和 120 秒），而 DisTok 的编码器-解码器架构仅需单次前向传播即可将概念对编码并解码为创造性令牌，推理时间约 3 秒，分别实现 13 倍和 40 倍的加速。这一效率优势源于 DisTok 将概念融合的知识内化于训练好的编码器-解码器参数中，推理时无需额外优化步骤。

**需要人工验证**：ConceptLab 的具体推理时间数据来自论文内部对比，其绝对数值可能因硬件环境差异而有所不同。



DisTok 是一个编码器-解码器框架，统一了条件式与非条件式的创造性生成。其核心流程是：将概念条件（如类别分布）映射为低维潜在向量，再解码为可嵌入自然语言提示的“创造性令牌”（creative token），最终指导扩散模型生成图像。

### 模块组成与数据流

框架由以下关键模块构成：

1. **Distribution Encoder (ℰ_dis)**：接收一个 K 维类别分布 $p_c$，将其投影为 δ 维潜在向量 $z = \mathcal{E}_{\mathrm{dis}}(p_c) \in \mathbb{R}^{\delta}$。
2. **Creative Decoder (𝒟_tok)**：将潜在向量 z 映射为与提示嵌入对齐的 d 维令牌 $t_{\mathrm{crt}} = \mathcal{D}_{\mathrm{tok}}(z) \in \mathbb{R}^{d}$，其中 $\delta \ll d$。该令牌随后被插入自然语言提示中，驱动基座扩散模型（Kandinsky）生成图像。
3. **Concept Pool (𝒫)**：存储已知概念的令牌及其类别分布，初始化自 CangJie 数据集中的已知类别。训练过程中，新发现的概念令牌及其 VLM 预测的类别分布也会被加入池中，供后续融合与监督使用。

### 训练流程

每个训练步，DisTok 随机执行以下两个任务之一（详见 Figure 2）：

![[assets/figures/papers/paper_list_l2036_https_openaccess_thecvf_com_content_CVPR2026_html_Feng_Breaking_Semantic/figures/002_Figure_2.jpg]]
*Figure 2: Overview of DisTok. At each training step, DisTok performs either (a) Continuous Concept Fusion, where a class pair is sampled to train the model to generate tokens reflecting increasingly complex class distributions; or (b) Distribution Consistency Enforcement, where a class distribution is sampled to align the encoder and decoder with the visual semantics of generated tokens. (c) Class Distribution Estimation is periodically conducted by randomly sampling latent vectors and decoding them into tokens, whose class distributions are subsequently predicted by a VLM. Resulting tokens and distributions are saved in Concept Pool for subsequent fusion and supervision*

- **(a) Continuous Concept Fusion（连续概念融合）**：从 Concept Pool 中采样一对类别，将两者的令牌相加后经编码器-解码器生成融合令牌，通过语义融合损失 $\mathcal{L}_{\mathrm{mix}}$ 训练解码器生成反映更复杂类别分布的令牌。
- **(b) Distribution Consistency Enforcement（分布一致性强化）**：从 Concept Pool 采样一个新颖令牌，根据其类别分布加权组合已知令牌，编码-解码后与原始新颖令牌对齐，通过分布一致性损失 $\mathcal{L}_{\mathrm{cst}}$ 强制视觉语义与输入分布一致。

此外，**(c) Class Distribution Estimation（类别分布估计）** 周期性执行：从高斯先验随机采样潜在向量并解码为令牌，使用预训练 VLM 预测生成图像的类别分布，将新颖概念及其分布加入 Concept Pool。

### 训练目标

整体训练目标为融合损失、一致性损失与潜在正则化损失的加权组合：

$$
\mathcal{L}_{\mathrm{total}} = \frac{1}{n} \sum_{i=1}^{n} \left( \alpha \mathbb{I}_{\mathrm{mix}}^{(i)} \mathcal{L}_{\mathrm{mix}}^{(i)} + \beta \mathbb{I}_{\mathrm{cst}}^{(i)} \mathcal{L}_{\mathrm{cst}}^{(i)} + \gamma \mathcal{L}_{\mathrm{reg}}^{(i)} \right)
$$

其中 $\mathbb{I}_{\mathrm{mix}}^{(i)}$ 和 $\mathbb{I}_{\mathrm{cst}}^{(i)}$ 为指示变量，标记当前步执行的任务类型；$\mathcal{L}_{\mathrm{reg}}$ 为潜在正则化损失，鼓励潜在空间均值为零且方差充足，防止模式坍塌。

### 推理

推理时，DisTok 将类别对直接编码为潜在向量并解码为创造性令牌，单次前向传播即可完成，额外开销可忽略（约 3 秒），相比 BASS 和 ConceptLab 分别实现 13 倍和 40 倍加速。无条件探索时，可直接从任意零均值、单位方差的分布（如高斯、拉普拉斯、柯西分布）采样潜在向量并解码，无需迭代优化。

### 补充图表

![[assets/figures/papers/paper_list_l2036_https_openaccess_thecvf_com_content_CVPR2026_html_Feng_Breaking_Semantic/figures/001_Figure_1.jpg]]
*Figure 1: We introduce Distribution-Conditional Generation, a novel paradigm that breaks semantic boundaries through fine-grained, controllable concept fusion, and propose DisTok, an encoder–decoder framework unifying conditional and unconditional semantic exploration, enabling efficient and flexible discovery of novel visual concepts*



DisTok 的核心架构由三个紧密协作的模块构成：**Distribution Encoder**、**Creative Decoder** 和 **Concept Pool**，并围绕两个互补的训练目标——**Continuous Concept Fusion** 与 **Distribution Consistency Enforcement**——进行联合优化。

### 分布编码器与创造性解码器

给定一个定义在已知类别集合上的类别分布 $p_c \in \mathbb{R}^K$，**Distribution Encoder** $\mathcal{E}_{\mathrm{dis}}$ 将其投影为低维潜在向量：

$$z = \mathcal{E}_{\mathrm{dis}}(p_c) \in \mathbb{R}^{\delta}$$

其中 $\delta \ll K$，实现了从高维离散分布到紧凑连续表征的压缩。**Creative Decoder** $\mathcal{D}_{\mathrm{tok}}$ 随后将该潜在向量映射为可与文本提示嵌入对齐的创造性概念令牌：

$$t_{\mathrm{crt}} = \mathcal{D}_{\mathrm{tok}}(z) \in \mathbb{R}^{d}$$

该令牌可直接嵌入自然语言提示中，作为扩散模型的条件输入。这种编码器-解码器架构将条件生成（从指定分布出发）与无条件探索（从高斯先验采样 $z$）统一在同一框架内。

### 连续概念融合

在每个训练步，DisTok 从 **Concept Pool** $\mathcal{P}$ 中随机采样一对已知概念类别，将两者令牌相加后经编码器-解码器生成融合令牌。融合的语义质量通过以下损失函数监督。

**初步语义融合损失** 最小化自适应提示 $q_a$ 与限制性提示 $q_r$、辅助提示 $q_s$ 之间的余弦距离：

$$\tilde{\mathcal{L}}_{\mathrm{mix}} = (1 - \cos(E(q_r), E(q_a))) + (1 - \cos(E(q_s), E(q_a)))$$

其中 $E(\cdot)$ 为 CLIP-L/14 文本编码器。为防止模型过拟合到单一主导概念，引入阈值 $\theta_1$、$\theta_2$ 对余弦相似度进行截断，得到 **受控语义融合损失**：

$$\mathcal{L}_{\mathrm{mix}} = (1 - \min[\cos(E(q_r), E(q_a)), \theta_1]) + (1 - \min[\cos(E(q_s), E(q_a)), \theta_2])$$

该设计确保融合概念在两类别的语义空间中保持均衡表征，而非退化为某一类别的简单复制。

### 分布一致性强化

为强制生成图像的视觉语义与输入类别分布对齐，DisTok 从 Concept Pool 中采样新颖令牌 $t_{\mathrm{nvl}}$，根据其类别分布加权组合已知令牌，经编码-解码后得到 $t_{\mathrm{crt}}$。**分布一致性损失** 定义为两者文本嵌入的余弦距离：

$$\mathcal{L}_{\mathrm{cst}} = 1 - \cos(E(t_{\mathrm{crt}}), E(t_{\mathrm{nvl}}))$$

此外，利用预训练 VLM 从生成图像中预测类别分布，与输入分布进行对齐监督，形成闭环验证。

### 潜在空间正则化

为防止编码器-解码器在训练中发生模式坍塌，引入 **潜在正则化损失**，鼓励潜在空间均值为零且方差充足：

$$\mathcal{L}_{\mathrm{reg}} = \frac{1}{\sigma(z)^2} \mathbb{E}_z \left[ ||\boldsymbol{\mu}(z)||_2^2 \right]$$

该损失促使潜在空间保持结构良好的分布特性，使从任意零均值、单位方差的先验分布（如高斯、拉普拉斯、柯西分布）直接采样成为可能，无需迭代优化。

### 总体训练目标

每训练步随机执行概念融合或分布一致性强化，总体损失由对应损失加权组合：

$$\mathcal{L}_{\mathrm{total}} = \frac{1}{n} \sum_{i=1}^{n} \left( \alpha \mathbb{I}_{\mathrm{mix}}^{(i)} \mathcal{L}_{\mathrm{mix}}^{(i)} + \beta \mathbb{I}_{\mathrm{cst}}^{(i)} \mathcal{L}_{\mathrm{cst}}^{(i)} + \gamma \mathcal{L}_{\mathrm{reg}}^{(i)} \right)$$

其中 $\mathbb{I}_{\mathrm{mix}}^{(i)}$ 和 $\mathbb{I}_{\mathrm{cst}}^{(i)}$ 为指示变量，标记当前步执行的任务类型；$n=8$ 为梯度累积步数；$\alpha$、$\beta$、$\gamma$ 为各损失项的权重系数。



## 实验与关键发现

### 核心定量结果

DisTok 在两个核心任务上均取得了最优性能：**类别对引导的语义探索**（两两概念融合）和**分布条件生成**（多概念细粒度分布控制）。所有对比方法均使用相同的基座文本到图像扩散模型（Kandinsky 2.1/3.1）进行评估，确保公平性。

在类别对引导的语义探索任务上，Table 1 显示 DisTok 在 VQAScore 上达到 **0.840**，超越 **BASS**（Li et al., ECCV 2024）的 0.812 和 **CreTok**（Feng et al., CVPR 2025）的约 0.827，分别提升 **+0.028** 和 **+0.013**。这表明 DisTok 生成的融合概念图像与文本描述的对齐度更高。

![[assets/figures/papers/paper_list_l2036_https_openaccess_thecvf_com_content_CVPR2026_html_Feng_Breaking_Semantic/figures/006_Table_1.jpg]]
*Table 1: Quantitative Comparisons for Image-Text Alignment and Human Preference Ratings*

在分布条件生成任务上，Table 2 展示了 DisTok 在 GPT-4o 美学评分上达到 **9.9±0.1**，显著优于所有对比的 SOTA T2I 模型（包括 **Stable Diffusion 3**（Esser et al., ICML 2024）、**FLUX** 等）。该任务要求模型根据类别分布（而非文本提示）生成图像，DisTok 是唯一专门为此范式设计的方法，因此优势显著。

![[assets/figures/papers/paper_list_l2036_https_openaccess_thecvf_com_content_CVPR2026_html_Feng_Breaking_Semantic/figures/005_Table_2.jpg]]
*Table 2: Creativity evaluated by GPT-4o*

### 推理效率

DisTok 的核心效率优势源于其**单次前向编码-解码**架构：给定概念对后，仅需一次前向传播即可生成创造性令牌，额外开销可忽略。实测推理时间约为 **3 秒/概念**，相比之下，**BASS** 需要约 40 秒（基于交换采样的迭代优化），**ConceptLab**（Richardson et al., ACM TOG 2024）需要约 120 秒（通过降低与现有概念相似度进行无条件探索），DisTok 分别实现了 **13 倍**和 **40 倍**的加速。训练方面，DisTok 在单张 NVIDIA 4090 GPU 上训练 20K 步，batch size 为 1，梯度累积 8 步，总训练时间约 **30 分钟**。

### 人工评估

Table 3 的用户研究进一步验证了 DisTok 的生成质量。在创造性生成的对比中，DisTok 获得 **278 票**，FLUX 获得 **222 票**，DisTok 以 **+56 票**的优势胜出。这表明人类评估者更偏好 DisTok 生成的新颖概念图像。

![[assets/figures/papers/paper_list_l2036_https_openaccess_thecvf_com_content_CVPR2026_html_Feng_Breaking_Semantic/figures/009_Table_3.jpg]]
*Table 3: Results of the user study*

### 消融实验

Table 4 的消融实验验证了**分布一致性监督**（Distribution Consistency Enforcement）的关键作用。移除该组件后，生成图像与目标类别分布之间的 KL 散度从 **0.0602 升至 0.0732**，表明分布对齐度明显下降。这一结果证实了利用 VLM 从生成图像中预测类别分布并与输入分布对齐的策略，对于保证视觉语义与指定分布的一致性至关重要。

### 定性分析

Figure 4 展示了 DisTok 在类别对引导的语义探索上的定性结果。与 BASS 和 CreTok 相比，DisTok 生成的融合概念图像在保持各源概念特征的同时，实现了更自然的语义融合，避免了某一概念过度主导的问题。这得益于**带阈值的语义融合损失**（Eq. 2），通过限制余弦相似度上界防止模型过拟合到单一主导概念。

![[assets/figures/papers/paper_list_l2036_https_openaccess_thecvf_com_content_CVPR2026_html_Feng_Breaking_Semantic/figures/003_Figure_4.jpg]]
*Figure 4: Performance of DisTok on Semantic Exploration Guided by Class Pairs*

Figure 6 展示了 DisTok 生成令牌的风格适应性：创造性令牌可以无缝嵌入自然语言提示中，在保持概念一致性的同时支持多样化的风格（详见附录 A.4）。Figure 7 展示了训练过程中的概念演化：在 2K、3K 和 10K 步分别采样，生成的创造性概念逐步复杂化，验证了连续概念融合策略的有效性。

![[assets/figures/papers/paper_list_l2036_https_openaccess_thecvf_com_content_CVPR2026_html_Feng_Breaking_Semantic/figures/004_Figure_6.jpg]]
*Figure 6: Tokens generated by DisTok can be seamlessly combined with natural language prompts to support diverse styles while preserving conceptual consistency. See Appendix A.4 for more styles*

![[assets/figures/papers/paper_list_l2036_https_openaccess_thecvf_com_content_CVPR2026_html_Feng_Breaking_Semantic/figures/007_Figure_7.jpg]]
*Figure 7: Progressively complex creative concepts sampled at 2K, 3K, and 10K training steps*

### 失败模式与局限性

尽管 DisTok 在创造性和效率上表现优异，仍存在以下限制：

1. **基座模型能力上限**：极端复杂的类别分布可能超出基座扩散模型（Kandinsky）的生成能力，导致视觉质量下降。
2. **VLM 分类精度**：VLM 对分布外概念的分类精度有限，可能影响新奇概念分布估计的准确性，进而影响分布一致性监督的质量。
3. **概念池先验约束**：训练概念池初始限定于 CangJie 数据集中的已知类别，探索范围受此先验约束，无法自动发现全新的语义维度。
4. **类别集合依赖性**：类别分布的定义目前依赖人工指定的已知类别集合，尚不能自动扩展以适应开放世界的概念发现。

这些局限性指向了未来的改进方向，包括自动扩展类别集合、引入更细粒度的视觉定位信号，以及将该范式迁移至其他模态的生成任务。

### 补充图表

![[assets/figures/papers/paper_list_l2036_https_openaccess_thecvf_com_content_CVPR2026_html_Feng_Breaking_Semantic/figures/008_Figure_8.jpg]]
*Figure 8: Comparison with Prompt Engineering. For each DisTok-generated concept, a corresponding textual prompt for Kandinsky [29] is derived using GPT-4o. All detailed prompts are provided in Fig. 14*



## 定位与知识库关联

### 1. 方法谱系

#### 1.1 与现有创造性生成方法的继承与突破

DisTok 处于**文本到图像（T2I）创造性生成**这一研究方向，其直接对比的基线方法构成了清晰的谱系脉络：

- **BASS (TP2O)**（Li et al., ECCV 2024）：基于交换采样的两两概念融合方法，首次系统探索了通过组合已知概念创造新视觉概念的范式。DisTok 继承了其“概念融合”的基本思路，但将其从**离散的、单次的两两组合**扩展为**连续的、迭代的分布级融合**，突破了 BASS 仅能处理固定概念对的限制。

- **CreTok**（Feng et al., CVPR 2025）：将组合语义创造性生成引入令牌化框架，DisTok 在架构上与之共享“概念令牌”这一表征形式，但 CreTok 仍局限于提示级的语义融合，缺乏对多概念细粒度分布的控制。DisTok 的**类别分布条件生成**范式从根本上改变了生成条件的粒度。

- **ConceptLab**（Richardson et al., ACM TOG 2024）：通过降低与现有概念的相似度进行无条件新颖探索，DisTok 与之共享“无条件探索”的思想，但 ConceptLab 缺乏条件控制能力，无法指定融合方向。DisTok 通过**编码器-解码器架构**将条件探索与无条件探索统一在同一个框架内。

#### 1.2 与基座扩散模型的接口关系

DisTok 并非独立生成模型，而是作为**条件编码模块**嵌入现有 T2I 扩散模型之上。其直接依赖的基座模型包括：

- **Kandinsky**（Razzhigaev et al., EMNLP 2023）：作为 DisTok 的主要实验基座，提供文本编码器 E(·) 和扩散生成能力。DisTok 的 Creative Decoder 输出的令牌直接嵌入 Kandinsky 的提示空间，实现即插即用。
- **Stable Diffusion 3**（Esser et al., ICML 2024）与 **FLUX**：作为对比的 SOTA T2I 模型，DisTok 在创造力评估中与它们进行了跨模型比较。

这种**模块化设计**使得 DisTok 原则上可迁移至任何支持令牌化条件输入的扩散模型，但当前验证仅限于 Kandinsky 系列。

#### 1.3 核心范式转换：从文本条件到分布条件

DisTok 的根本创新在于将 T2I 生成的条件从**文本提示（prompt）**替换为**类别分布（class distribution）**。这一转换的动机源于一个关键观察：分类器对分布外输入会产生软概率分布，逆向使用这一过程，即可将未知概念表征为已知类别上的分布。这一定位使得 DisTok 区别于所有现有方法：

- 现有方法（BASS、CreTok 等）在**文本语义空间**中进行融合，受限于语言描述的离散性和模糊性；
- DisTok 在**概率分布空间**中进行融合，实现了**可量化的、细粒度的概念混合控制**。

### 2. 知识库定位

#### 2.1 解决的问题域

DisTok 解决的核心问题是：**如何突破 T2I 模型的训练分布限制，在保持可控性的前提下生成真正新颖的、超出分布的概念**。这一问题处于以下研究方向的交叉点：

1. **可控图像生成**（controllable image generation）：DisTok 将控制信号从文本扩展到类别分布，丰富了控制维度。
2. **创造性 AI**（creative AI）：DisTok 通过连续概念融合实现了超越简单组合的真正语义创新。
3. **分布外泛化**（out-of-distribution generalization）：DisTok 逆向利用分类器的 OOD 行为，将其转化为生成能力。

#### 2.2 适用边界

基于论文中明确讨论的限制，DisTok 的适用边界包括：

1. **基座模型能力上限约束**：极端复杂分布的视觉质量受限于 Kandinsky 等基座扩散模型的生成能力，DisTok 无法超越其底层模型的性能天花板。
2. **VLM 分类精度约束**：分布一致性监督依赖预训练 VLM 从生成图像中预测类别分布，VLM 对分布外概念的分类精度有限，可能影响新颖概念分布估计的准确性。
3. **已知类别集合的先验约束**：训练概念池最初限定于 CangJie 数据集中的已知类别，探索范围受此先验约束——DisTok 只能在这些已知类别张成的分布空间中进行融合，无法凭空创造全新的语义维度。
4. **类别分布定义的封闭性**：当前类别分布的定义依赖人工指定的已知类别集合，尚不能自动发现或扩展语义维度。

#### 2.3 关键局限

1. **基座依赖的单点故障**：若基座扩散模型对某些概念组合的生成质量较差，DisTok 无法通过自身机制弥补。
2. **VLM 反馈的噪声**：分布一致性监督的质量直接取决于 VLM 的分类精度，对于高度新颖的概念，VLM 可能给出不准确的分布估计，形成错误反馈循环。
3. **概念池的封闭世界假设**：训练期间概念池的初始类别集合固定，无法在训练过程中动态引入新的已知类别，限制了开放世界场景下的持续探索能力。

### 3. 开放问题

基于论文明确提出的开放问题及方法设计的自然延伸，以下问题值得进一步探索：

1. **开放世界概念发现**：如何自动扩展已知类别集合，使 DisTok 能够适应开放世界中不断涌现的新语义维度？这可能需要引入开放词汇检测或持续学习机制。

2. **更细粒度的分布一致性监督**：当前分布一致性损失仅在全局图像级别对齐类别分布，是否可利用更细粒度的视觉定位信号（如注意力图、分割掩码）实现空间级别的分布对齐？

3. **跨模态迁移**：该范式能否迁移至其他模态的生成任务？例如，在 3D 生成中将类别分布作为形状和纹理融合的条件信号，或在音频生成中实现音色和风格的分布级混合。

4. **自适应融合阈值**：连续概念融合损失中的阈值 θ₁、θ₂ 当前为固定超参数，自适应调整策略（如基于融合难度动态调节）是否可进一步提升创造力的质量与多样性？

5. **分布空间的几何性质**：Distribution Encoder 学习到的潜在空间具有哪些几何性质？是否支持有意义的算术操作（如“概念 A + 概念 B - 概念 C”）？这需要进一步的理论分析和实证验证。



## 原文 PDF

![[paperPDFs/CVPR_2026/Breaking_Semantic_Boundaries_Distribution_Guided_Semantic_Exploration_for_Creative_Generation.pdf]]
