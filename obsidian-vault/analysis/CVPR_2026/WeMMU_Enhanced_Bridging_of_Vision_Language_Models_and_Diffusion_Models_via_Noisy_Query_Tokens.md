---
title: "WeMMU: Enhanced Bridging of Vision-Language Models and Diffusion Models via Noisy Query Tokens"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/WeMMU_Enhanced_Bridging_of_Vision_Language_Models_and_Diffusion_Models_via_Noisy_Query_Tokens.pdf
project_link: null
code_link: null
aliases:
- WeMMU
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/generative_models_diffusion
- topic/generative_models_diffusion/diffusion_image_video
core_operator: 引入从标准正态分布 N(0,I) 每步采样的噪声查询令牌，注入随机性，迫使VLM学习稳健的分布式表示空间，避免任务特定捷径。
primary_logic: 将确定性查询令牌替换为每步重新采样的噪声令牌，并结合VAE分支将细节信息注入VLM而非扩散模型，实现‘分工’设计，既解决了泛化崩溃又保留了高频细节。
claims:
- 可学习固定查询在ImageEdit-Bench上Overall仅2.53，而噪声查询提升至2.98，噪声查询+VAE分支达到3.31（Table 4）
- 噪声查询将注意力从图像token转移到文本token（注意偏差-0.99 vs 可学习查询的+1.80），增强指令遵循
- 在多图编辑任务中，噪声查询能正确执行编辑，而可学习查询产生不一致的结果
- Geneval 上 Overall↑ = 0.88 (WeMMU Stage 3)
---

# WeMMU: Enhanced Bridging of Vision-Language Models and Diffusion Models via Noisy Query Tokens

> [!tip] 核心洞察
> 将确定性查询令牌替换为每步重新采样的噪声令牌，并结合VAE分支将细节信息注入VLM而非扩散模型，实现‘分工’设计，既解决了泛化崩溃又保留了高频细节。

| 字段 | 内容 |
|------|------|
| 中文题名 | WeMMU：通过噪声查询令牌增强视觉-语言模型与扩散模型的桥接 |
| 英文题名 | WeMMU: Enhanced Bridging of Vision-Language Models and Diffusion Models via Noisy Query Tokens |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2512.02536) |
| Topic | #topic/vision_multimodal_applications #topic/generative_models_diffusion #topic/generative_models_diffusion/diffusion_image_video |
| Method | WeMMU |
| Dataset | Geneval, DPG-Bench, ImageEdit-Bench |

> [!tip] 效果简介
> - Geneval 上，Overall↑ 0.88 (WeMMU Stage 3) vs 0.81 (MetaQuery-XL) (+0.07)。
> - DPG-Bench 上，Overall↑ 83.69 (WeMMU Stage 3) vs 77.67 (MetaQuery-XL) (+5.02)。
> - ImageEdit-Bench 上，Overall↑ 3.31 (WeMMU Stage 3) vs 3.2 (Bagel) (+0.11)。

## 概要

### 1. 问题背景

视觉-语言模型（VLM）与扩散模型的桥接是实现统一多模态理解与生成的关键技术路径。然而，现有桥接方法普遍面临**任务泛化崩溃**（Task Generalization Collapse）的瓶颈：基于可学习查询令牌（Learnable Query Tokens）的方法在预训练后倾向于过拟合任务特定的平均表示，导致模型在新增编辑任务时完全失效，仅能重构输入图像而无法执行编辑指令（Figure 1）。顺序训练无法解决此问题，而联合训练虽有效但不可持续——每增加一个新任务都需要完全重新训练整个模型。

### 2. 核心方法

WeMMU 提出**噪声查询令牌**（Noisy Query Tokens）作为核心调控变量，从根本上改变了 VLM 与扩散模型之间的信息传递机制：

- **噪声查询令牌**：每步训练从标准正态分布 $\mathcal{N}(0, I)$ 重新采样查询令牌，注入随机性，迫使 VLM 学习稳健的分布式表示空间，而非收敛到任务特定的确定性捷径。这解决了可学习固定查询的过拟合问题。
- **VAE 分支分工设计**：将冻结 VAE 编码器的细节特征通过线性层注入 VLM（而非直接注入扩散模型），由 VLM 统一处理高频细节与语义理解，实现“VLM 负责理解、扩散模型专注生成”的清晰分工。
- **对比流匹配加速收敛**：在早期预训练阶段使用对比流匹配损失 $\mathcal{L}_{\Delta FM}$，拉近正样本方向、推远负样本方向（$\lambda=0.05$），加速学习；后期切换为标准条件流匹配损失以提升效率。

### 3. 方法定位

WeMMU 属于**统一多模态理解与生成模型**（Unified Model），与以下代表性工作形成直接对比：

- **MetaQueries**：使用可学习查询令牌桥接 VLM 与扩散模型的代表性方法，存在任务泛化崩溃问题。
- **Bagel**：端到端统一生成模型，通过训练专家路径进行生成，但缺乏对泛化崩溃的针对性设计。
- **UniWorld-V1**：另一基于可学习查询令牌的桥接方法，面临相同的过拟合瓶颈。

WeMMU 的独特贡献在于通过**噪声令牌 + VAE 分支分工**的组合设计，在不增加模型规模的前提下解决了泛化崩溃问题，同时保留了高频细节保真度。

### 4. 主要结果

在图像生成与编辑基准上，WeMMU 相较于同类统一模型取得显著提升：

- **图像生成**：在 Geneval 上 Overall 达 0.88（MetaQuery-XL 为 0.81，提升 +0.07）；在 DPG-Bench 上 Overall 达 83.69（MetaQuery-XL 为 77.67，提升 +5.02）（Table 1）。
- **图像编辑**：在 ImageEdit-Bench 上 Overall 达 3.31，超越 Bagel（3.2）等端到端统一模型（Table 2）。

消融实验确认了噪声查询令牌的核心作用：可学习固定查询在 ImageEdit-Bench 上 Overall 仅 2.53，替换为噪声查询后提升至 2.98，进一步加入 VAE 分支达到 3.31（Table 4）。注意力分析表明，噪声查询将注意力从图像令牌转向文本令牌（注意偏差 -0.99 vs 可学习查询的 +1.80），显著增强了指令遵循能力（Figure 3）。

### 5. 局限与开放问题

WeMMU 在多图编辑任务中仍可能产生可见的拼接痕迹，且在编辑性能上落后于 GPT-4o、EMU3.5 等大型专有模型。框架依赖预训练 VLM 与扩散模型的兼容性，更换骨干可能需要重新训练。开放问题包括：噪声令牌分布是否可学习或自适应、如何通过强化学习微调进一步提升指令遵循、以及如何将方法扩展到更大规模的多模态模型。



### 统一多模态模型的兴起与桥接范式

近年来，视觉-语言模型（VLM）与扩散模型的融合成为多模态理解与生成统一框架的核心技术路线。这类统一模型旨在同时具备图像理解与图像生成/编辑能力，代表性工作包括**Bagel**（Expert Pathway）和**UniWorld-V1**等。在这些框架中，VLM负责解析图文输入中的语义信息，扩散模型则承担最终的图像合成任务，两者之间的信息传递依赖于一组**桥接查询令牌**（bridge query tokens）。

### 任务泛化崩溃：确定性查询令牌的致命缺陷

当前主流的桥接方法——如**MetaQueries**等——采用**可学习的确定性查询令牌**：这些令牌在训练过程中被优化为固定的向量表示，用于从VLM的输出中聚合任务相关信息并传递给扩散模型。然而，这种设计存在一个被忽视的严重缺陷：**任务泛化崩溃**（Task Generalization Collapse）。

如图1所示，当使用顺序训练策略（先训练任务A，再训练任务B）时，可学习查询令牌会过拟合到任务特定的平均表示，导致模型在遇到新任务时完全失效——例如，编辑任务退化为简单的输入重构。虽然联合训练可以暂时缓解这一问题，但它要求每次引入新任务时都对整个模型进行完整重训练，这在计算资源和可持续性上均不可行。

这一瓶颈的本质在于：确定性查询令牌在预训练后趋于收敛到任务特定的“捷径”表示，丧失了表示空间的泛化能力，无法适应新的编辑任务。

### 细节保真度的两难困境

除泛化问题外，桥接范式还面临细节保留的挑战。VLM的视觉编码器通常对输入图像进行高度压缩，导致细粒度的高频信息（如纹理、边缘）在传递过程中丢失。传统方法往往将VAE编码器的细节特征直接注入扩散模型，但这种设计模糊了“理解”与“生成”的职责边界，且未从根本上解决VLM内部的信息瓶颈。

### 本文动机

针对上述两个核心缺口，本文提出**WeMMU**框架，核心动机包括：

1. **打破确定性查询的泛化诅咒**：用随机采样的噪声查询令牌替代固定的可学习令牌，迫使VLM学习一个分布式的、稳健的表示空间，而非任务特定的捷径。
2. **重构细节补充路径**：将VAE分支的细节信息注入VLM而非扩散模型，实现清晰的“分工”设计——VLM统一负责理解与细节聚合，扩散模型专注于生成。
3. **建立可扩展的统一框架**：通过冻结VLM骨干、仅训练轻量桥接组件和扩散模型，在保持理解能力的同时实现对新任务的可持续扩展。



## 核心方法与创新机理

WeMMU 的核心创新在于对“VLM-扩散模型桥接机制”的两个关键槽位进行了根本性改造，以解决传统可学习查询令牌方法中普遍存在的**任务泛化崩溃（Task Generalization Collapse）**问题。

### 1. 从确定性查询到噪声查询令牌

传统桥接方法（如 **MetaQueries** 和 **UniWorld-V1**）使用一组确定性的可学习查询令牌（Learnable Query Tokens）来聚合 VLM 的图文信息并传递给扩散模型。然而，这些固定向量在预训练后趋于过拟合任务特定的平均表示，导致模型在面对新编辑任务时泛化能力急剧下降——表现为仅能重构输入图像而无法执行编辑指令（Figure 1）。

WeMMU 的核心洞察是：**将确定性查询令牌替换为每步从标准正态分布 $\mathcal{N}(0, I)$ 重新采样的噪声查询令牌（Noisy Query Tokens）**。这一设计在桥接过程中注入了随机性，迫使 VLM 学习一个稳健的分布式表示空间，而非依赖任务特定的捷径。

注意力机制分析（Figure 3）揭示了噪声查询令牌工作的因果机制：可学习固定查询的注意力偏差高达 +1.80，即过度关注图像令牌；而噪声查询的注意力偏差为 -0.99，将注意力显著转向文本令牌，从而增强了指令遵循能力。这一注意力转移是噪声查询提升编辑性能的直接因果证据。

### 2. VAE 特征注入位置的重构

传统方法通常将 VAE 编码器的细节特征直接注入扩散模型以补充高频信息。WeMMU 提出了一种**分工设计（Labor Division）**：将 VAE 特征通过一个简单的线性层注入 VLM 的生成路径，而非扩散模型。这一设计的合理性在于：

- **保持 VLM 作为唯一的信息聚合中心**：VLM 统一处理文本指令、输入图像和 VAE 细节特征，形成完整的条件表示，再传递给扩散模型。
- **避免扩散模型的信息过载**：扩散模型仅负责生成，无需同时处理多源条件信号。

验证实验（Figure 4）表明，微调 VLM 原生 ViT 会导致训练崩溃，而使用简单线性层连接 VAE 特征可以获得最快且最稳定的收敛速度。这证实了“轻量注入 VLM”策略的有效性。

### 3. 训练目标的阶段性切换

在训练目标上，WeMMU 采用了**对比流匹配（Contrastive Flow-Matching）与条件流匹配（Conditional Flow-Matching）的阶段性组合**。早期预训练阶段使用对比流匹配损失（Eq. 4）加速收敛，利用批内负样本拉近正样本方向、推远负样本方向；后期阶段切换为标准条件流匹配损失（Eq. 3），因为小批量下对比损失的增益不再显著。这一策略在保证训练效率的同时避免了不必要的计算开销。

### 消融验证

Table 4 的消融实验直接量化了上述创新的贡献：
- 可学习固定查询在 ImageEdit-Bench 上的 Overall 得分仅为 2.53；
- 替换为噪声查询后，得分提升至 2.98（+0.45）；
- 进一步加入 VAE 分支后，得分达到 3.31（+0.33）。

这一递进式提升清晰地表明，噪声查询令牌和 VAE 分支是两个互补且可叠加的创新组件。



WeMMU 的整体设计遵循明确的“分工”原则：冻结的视觉语言模型（VLM）负责理解，可训练的扩散模型专注于生成。两者之间通过一个**概率专家桥接（Probabilistic Expert Bridge）** 连接，其核心是每步重新采样的**噪声查询令牌（Noisy Query Tokens）**，而非传统的确定性可学习查询。

### 模块组成与数据流

框架集成了以下关键模块：

- **视觉语言模型（Qwen2.5-VL-3B）**：作为冻结的理解骨干，接收图文输入并提取语义特征。原始 VLM 参数保持冻结，同时引入一条并行的、可训练的生成路径，其权重由 VLM 初始化。
- **噪声查询令牌**：每步从标准正态分布 $\mathcal{N}(0, I)$ 采样，替代固定的可学习查询。这些令牌在 VLM 的生成路径中聚合图像和文本特征，形成分布式表示空间，避免过拟合到任务特定的平均表示。
- **VAE 分支（含线性层）**：将冻结 VAE 编码器提取的细节特征经线性投影后注入 VLM，补充高频信息。此设计将细节补充职责从扩散模型转移到 VLM，保持分工清晰。
- **Position MLP**：对齐 VLM 与扩散模型的特征维度，并注入 2D 空间位置编码，将 VLM 输出转化为扩散模型的条件输入。
- **扩散模型（Sana 1.6B）**：可训练的生成器，根据条件潜在变量生成最终图像。

### 输入输出流

1. **输入**：文本指令与（可选的）参考图像。
2. **VLM 处理**：冻结的 VLM 编码图文输入；并行的生成路径中，噪声查询令牌与 VAE 分支注入的细节特征共同聚合信息。
3. **桥接与条件生成**：Position MLP 将 VLM 生成路径的输出映射为扩散模型的条件变量。
4. **输出**：扩散模型在条件变量引导下，通过流匹配采样生成最终图像。

### 训练策略

训练采用四阶段课程学习，逐步提升分辨率和任务复杂度（从基础重建到多图编辑）。早期阶段使用**对比流匹配（Contrastive Flow Matching）** 加速收敛，后期切换为标准**条件流匹配（Conditional Flow Matching）** 以提升效率。优化器为 AdamW（$\beta_1=0.9$, $\beta_2=0.95$）。

### 补充图表

![[assets/figures/papers/paper_list_l2359_https_arxiv_org_abs_2512_02536/figures/001_Figure_1.jpg]]
*Figure 1: Task Generalization Collapse. Sequential training (middle) fails editing, merely reconstructs the input. Joint training (right) works but is unsustainable, requiring full retraining for new tasks*



### 流匹配基础

WeMMU 的生成训练建立在流匹配（Flow Matching）框架之上。给定数据分布 $q(x_0)$ 和噪声分布 $\epsilon \sim \mathcal{N}(0, I)$，状态 $x_t$ 沿常微分方程演化：

$$\frac { d x _ { t } } { d t } = v ( x _ { t } , t )$$

其中 $v(x_t, t)$ 为待学习的向量场。论文采用从数据 $x_0$ 到噪声 $\epsilon$ 的线性插值路径：

$$x _ { t } = ( 1 - t ) x _ { 0 } + t \epsilon$$

在此路径下，目标向量场为 $\epsilon - x_0$，标准条件流匹配损失为最小化预测向量场与目标之间的均方误差：

$$\mathcal { L } _ { C F M } ( \theta ) = \mathbb { E } [ \| v _ { \theta } ( x _ { t } , t , y ) - ( \epsilon - x _ { 0 } ) \| ^ { 2 } ]$$

在早期预训练阶段，WeMMU 采用对比流匹配（Contrastive Flow-Matching）损失加速收敛：

$$\begin{array} { r } { \mathcal { L } _ { \Delta F M } ( \theta ) = \mathbb { E } \big [ \big \| v _ { \theta } ( x _ { t } , t , y ) - v ^ { + } \big \| ^ { 2 } \qquad } \\ { - \lambda \left\| v _ { \theta } ( x _ { t } , t , y ) - v ^ { - } \right\| ^ { 2 } \big ] } \end{array}$$

其中 $v^+$ 为正样本方向（匹配条件），$v^-$ 为批内负样本方向，$\lambda = 0.05$ 控制排斥力强度。该损失拉近正样本方向、推远负样本方向，在小批量场景下提供更强的训练信号。后期阶段因批量较小、对比流匹配优势不明显，切换回标准条件流匹配损失以提升效率。

### 噪声查询令牌：核心因果机制

传统桥接方法（如 **MetaQueries**、**UniWorld-V1**）使用可学习的固定查询令牌连接 VLM 与扩散模型。这些确定性令牌在预训练后趋于过拟合任务特定的平均表示，导致**任务泛化崩溃**：顺序训练新任务时模型仅重构输入图像而无法执行编辑指令（Figure 1）。

![[assets/figures/papers/paper_list_l2359_https_arxiv_org_abs_2512_02536/figures/011_Figure_1.jpg]]
*Figure 1: A gallery of diverse text-to-image generation results from our ‘WeMMU’ model, synthesized at 1024x1024 resolution*

WeMMU 的核心创新是将确定性查询令牌替换为每步从标准正态分布重新采样的噪声查询令牌：

$$Q _ { n o i s y } \sim \mathcal { N } ( 0 , I )$$

这些随机令牌在 VLM 的并行生成路径中聚合图像和文本特征。注入的随机性迫使 VLM 学习一个稳健的分布式表示空间，避免收敛到任务特定的捷径解。注意力机制分析（Figure 3）证实了这一机制的有效性：可学习固定查询的注意力偏差为 $+1.80$（偏向图像令牌），而噪声查询的注意力偏差为 $-0.99$（偏向文本令牌），表明噪声令牌促使模型优先关注编辑指令而非图像内容，从而增强指令遵循能力。

![[assets/figures/papers/paper_list_l2359_https_arxiv_org_abs_2512_02536/figures/006_Figure_3.jpg]]
*Figure 3: Analysis of query token attention mechanisms. The prompt is “Remove the ‘MILLER MOTORCARS’ text positioned across the top center of the image”. (Bottom rows) Learnable queries show a strong attention bias towards image tokens. Our Noisy Queries shift focus to the text tokens (right of red line), prioritizing instruction following. The VAE branch (right of blue line) helps balance this attention*

### VAE 分支：细节注入的分工设计

为补充 VLM 处理过程中可能丢失的高频细节信息，WeMMU 引入 VAE 分支。该分支将冻结 VAE 编码器的输出特征通过一个简单的线性层投影后注入 VLM，而非直接注入扩散模型。这一设计实现了清晰的**分工**：VLM 负责理解图文输入并整合细节信息，扩散模型专注于根据条件潜在变量生成最终图像。

实验验证（Figure 4）表明，微调 Qwen2.5-VL 原生 ViT 会导致训练崩溃，而使用简单线性层连接 VAE 特征可获得最快且最稳定的收敛速度，优于其他连接方式。

![[assets/figures/papers/paper_list_l2359_https_arxiv_org_abs_2512_02536/figures/007_Figure_4.jpg]]
*Figure 4: Justifying the VAE Branch design. (Left) Fine-tuning the native ViT of Qwen2.5-VL leads to training collapse. (Right) Loss curves for different VAE branch connection methods, showing a simple Linear layer (the red line) provides the fastest and most stable convergence*

### 推理引导公式

推理阶段采用多组件无分类器引导（Classifier-Free Guidance, CFG）。文生图任务使用标准 CFG：

$$\epsilon _ { p r e d } = \epsilon _ { u n c o n } + \lambda ( \epsilon _ { c o n } - \epsilon _ { u n c o n } )$$

其中 $\lambda = 4.0$。单图编辑任务引入重构和编辑两个引导组件：

$$\epsilon _ { p r e d } = \epsilon _ { u n c o n } + \lambda _ { r e c } ( \epsilon _ { r e c } - \epsilon _ { u n c o n } ) + \lambda _ { e d i t } ( \epsilon _ { e d i t } - \epsilon _ { r e c } )$$

其中 $\lambda_{rec} = 2.0$，$\lambda_{edit} = 3.0$，分别控制图像保真度和编辑强度的平衡。多图编辑任务使用简化的 CFG：

$$\epsilon _ { p r e d } = \epsilon _ { u n c o n } + \lambda _ { m u l t i } ( \epsilon _ { m u l t i } - \epsilon _ { u n c o n } )$$

其中 $\lambda_{multi} = 3.0$。



## 实验与关键发现

### 核心瓶颈：任务泛化崩溃

WeMMU 的出发点是一个被现有桥接方法普遍忽视的现象——**任务泛化崩溃**（Task Generalization Collapse）。如 Figure 1 所示，传统的可学习查询令牌方法（如 **MetaQueries**）在顺序训练多个编辑任务时，模型会退化为仅重构输入图像，完全丧失编辑能力。联合训练虽可暂时缓解，但每新增一个任务都需完全重新训练，不可持续。其根本原因在于：确定性的可学习查询令牌在预训练后趋于过拟合任务特定的平均表示，形成“捷径”，无法泛化到新任务。

### 主实验结果

#### 图像生成能力（Table 1）

![[assets/figures/papers/paper_list_l2359_https_arxiv_org_abs_2512_02536/figures/003_Table_1.jpg]]
*Table 1: Comparison on Image Generation benchmarks. “Gen. Only” refers to pure generation models, while “Unified” indicates models capable of both understanding and generation. ‘*’ refers to the methods using LLM rewriter*

![[assets/figures/papers/paper_list_l2359_https_arxiv_org_abs_2512_02536/figures/010_Table_1.jpg]]
*Table 1: Hyper-parameter settings for WeMMU models*

在 GenEval 和 DPG-Bench 两个图像生成基准上，WeMMU Stage 3 在未使用强化学习微调的模型中取得了领先成绩：

- **GenEval Overall**：WeMMU 达到 0.88，较 MetaQuery-XL（0.81）提升 +0.07，超越同规模的统一模型 **Show-o**（0.68）和 **VILA-U**（0.64）。
- **DPG-Bench Overall**：WeMMU 达到 83.69，较 MetaQuery-XL（77.67）提升 +5.02，显著优于 **Bagel**（80.19）和 **JanusFlow**（80.09）。

值得注意的是，WeMMU 未使用 LLM 重写器（LLM rewriter），而若干对比方法（如 DALL·E 3、SD3-Medium）依赖该技巧提升文本遵循度。在此约束下，WeMMU 的 GenEval 分数为所有不依赖 RL 微调方法中的最高值。

#### 图像编辑能力（Table 2）

![[assets/figures/papers/paper_list_l2359_https_arxiv_org_abs_2512_02536/figures/004_Table_2.jpg]]
*Table 2: Comparison on Image Editing benchmarks. “Gen. Only” refers to pure generation models, while “Unified” indicates models capable of both understanding and generation*

在 ImageEdit-Bench 和 GEdit-Bench-EN 上，WeMMU 展现出竞争力的编辑性能：

- **ImageEdit-Bench Overall**：WeMMU Stage 3 达到 3.31，超越 **Bagel**（3.20）和 **Show-o**（3.03）。Stage 4 因引入多图编辑训练，整体分数略降至 3.30，但多图编辑子任务能力显著增强。
- **GEdit-Bench-EN G.0**：WeMMU Stage 4 达到 5.77，Stage 3 为 5.75，接近 **EMU3.5**（6.23）和 **GPT-4o**（6.30）等大型专有模型。

需要指出，在编辑任务上 WeMMU 仍落后于 GPT-4o、EMU3.5 等使用更大规模数据和算力训练的专有模型，但作为 8B 量级的开源统一模型，其表现已具有竞争力。

### 消融实验：噪声查询令牌与 VAE 分支（Table 4）

![[assets/figures/papers/paper_list_l2359_https_arxiv_org_abs_2512_02536/figures/009_Table_4.jpg]]
*Table 4: Ablation Study on Query Token Design using the ImageEdit Benchmark*

Table 4 的消融实验直接验证了核心设计的有效性：

| 查询令牌类型 | VAE 分支 | ImageEdit Overall |
|:---|:---:|:---:|
| 可学习固定查询（MetaQueries） | ✗ | 2.53 |
| 噪声查询（Noisy Queries） | ✗ | 2.98 |
| 噪声查询（Noisy Queries） | ✓ | **3.31** |

**关键发现**：
1. **噪声查询 vs 可学习查询**：仅将确定性查询替换为每步从 $\mathcal{N}(0,I)$ 采样的噪声查询，Overall 即从 2.53 跃升至 2.98（+0.45），证明随机注入是打破任务特定捷径的有效手段。
2. **VAE 分支的增益**：在噪声查询基础上加入 VAE 分支，Overall 进一步提升至 3.31（+0.33），验证了“将细节信息注入 VLM 而非扩散模型”这一分工设计的合理性。

### 注意力机制分析（Figure 3）

Figure 3 揭示了噪声查询令牌发挥作用的深层机制。以“移除图像顶部文字”的编辑指令为例：

- **可学习固定查询**：注意力严重偏向图像令牌（注意偏差 +1.80），导致模型过度关注输入图像的视觉内容，忽视编辑指令。
- **噪声查询**：注意力显著转向文本令牌（注意偏差 -0.99），表明模型优先遵循文本指令。VAE 分支的加入进一步平衡了图像细节与指令遵循之间的注意力分配。

这一机制解释了为何噪声查询能有效缓解任务泛化崩溃：随机性迫使 VLM 在每次前向传播中重新聚合信息，无法依赖固定的图像特征捷径，从而学习到鲁棒的分布式表示空间。

### VAE 分支设计验证（Figure 4）

Figure 4 的实验排除了若干替代设计方案：

- **微调原生 ViT**（左图）：直接微调 Qwen2.5-VL 的原生视觉编码器会导致训练崩溃，验证了冻结 VLM 骨干的必要性。
- **连接方式对比**（右图）：在多种 VAE 特征注入方式中，简单线性层（Linear）提供最快、最稳定的收敛，优于交叉注意力（Cross-Attention）和加法（Addition）等方式。

### 多图编辑泛化能力（Figure 5）

![[assets/figures/papers/paper_list_l2359_https_arxiv_org_abs_2512_02536/figures/008_Figure_5.jpg]]
*Figure 5: Generalization on the multi-image editing task. The task is to replace the subject in Input 1 with the subject from Input 2. Baselines with learnable queries (third and fourth columns) produce incoherent results. Our Noisy Query method (fifth column) correctly performs the edit, while our full model (last column) improves detail fidelity*

多图编辑任务（将输入1的主体替换为输入2的主体）是检验泛化能力的关键场景。Figure 5 显示：

- **可学习查询方法**（MetaQueries、UniWorld-V1）：产生不一致的结果，无法正确完成主体替换。
- **噪声查询方法**：正确执行编辑，完整模型在细节保真度上更优。

这进一步验证了噪声查询令牌在多图条件下的泛化优势。

### 失败模式与局限性

尽管 WeMMU 在多数任务上表现优异，仍存在以下局限：

1. **多图编辑拼接痕迹**：因多图编辑训练数据有限且质量不均，生成结果可能出现可见的拼接边界，细节融合不够自然（需人工核实具体样例）。
2. **编辑任务与专有模型的差距**：在 GEdit-Bench-EN 等编辑基准上仍落后于 GPT-4o、EMU3.5 等大型专有模型，反映了数据规模和模型容量的客观差距。
3. **骨干依赖性**：框架依赖预训练 VLM 和扩散模型的兼容性，更换骨干可能需要重新训练桥接组件。

### 训练策略的贡献

四阶段课程训练（Table 3）和对比流匹配（Contrastive Flow-Matching）在早期阶段的加速作用也是性能提升的辅助因素。Stage 1 使用对比流匹配（Eq. 4，$\lambda=0.05$）快速预热桥接组件，后续阶段切换为标准条件流匹配（Eq. 3）以提升效率。这一策略在批量较小时对比流匹配收益递减的观察下，实现了训练效率与收敛质量的平衡。

![[assets/figures/papers/paper_list_l2359_https_arxiv_org_abs_2512_02536/figures/005_Table_3.jpg]]
*Table 3: Detailed Training Curriculum and Hyper-parameters. The training progresses through four stages, adjusting resolution, batch size, and data mixture. Notably, Stage 3 and Stage 4 utilize different subsets of the Uniworld dataset to target specific editing capabilities. Task abbreviations: Rec. (Reconstruction), T2I (Text-to-Image), Uncond. (Unconditional T2I), S-Edit (Single-Image Editing), M-Edit (Multi-Image Editing)*



## 定位与知识库关联

### 桥接范式的谱系定位

WeMMU 处于“冻结 VLM + 可训练扩散模型”的桥接范式之中。该范式的核心挑战在于如何将 VLM 的语义理解有效传递至扩散模型的生成过程。现有方法主要分化为两条技术路径：

**可学习查询令牌路径**：以 **MetaQueries** 和 **UniWorld-V1** 为代表，在 VLM 的生成路径中引入固定数量的可学习查询令牌（learnable query tokens），通过端到端训练使这些令牌学会从 VLM 的隐藏状态中聚合任务相关信息，再将其作为条件注入扩散模型。这一设计的根本性缺陷在于：确定性的可学习向量在预训练完成后趋于过拟合到任务特定的平均表示，导致“任务泛化崩溃”（task generalization collapse）——模型在顺序学习新任务时仅能重构输入图像，而无法执行编辑指令（Figure 1）。WeMMU 的噪声查询令牌正是针对这一瓶颈的结构性改进：将确定性向量替换为每步从 $\mathcal{N}(0,I)$ 重新采样的随机令牌，迫使 VLM 学习一个分布式表示空间，而非记忆任务特定的捷径。

**端到端统一生成路径**：以 **Bagel** 为代表，训练专门的“专家路径”（Expert Pathway）实现统一的图文理解与生成。此类方法通常需要大规模联合训练，计算开销较大。WeMMU 继承了“分工”思想——VLM 负责理解、扩散模型负责生成——但通过噪声查询令牌的随机化机制和 VAE 分支的细节注入，在保持模块化架构的同时解决了泛化崩溃问题。

### 关键技术组件的创新定位

**噪声查询令牌的机制创新**。与可学习查询令牌相比，噪声查询令牌的本质差异不在于令牌数量或架构位置，而在于其引入的随机性改变了 VLM 的学习动力学。注意力分析（Figure 3）揭示了这一差异的因果机制：可学习查询令牌产生强烈的图像令牌注意偏差（+1.80），导致模型倾向于复制输入而非遵循指令；噪声查询令牌则将注意力转移至文本令牌（注意偏差 -0.99），使模型优先执行编辑指令。这一发现表明，噪声令牌实际上起到了“正则化器”的作用，防止 VLM 在生成路径中走图像重建的捷径。

**VAE 分支的架构定位**。传统桥接方法通常将 VAE 编码的细节特征直接注入扩散模型的条件输入。WeMMU 的设计选择是将 VAE 特征通过线性层注入 VLM 的生成路径，而非扩散模型。这一“前置注入”策略的合理性在于：VLM 作为信息瓶颈，可以统一处理语义指令和视觉细节，避免在扩散模型端引入未经语义对齐的原始特征。Figure 4 的验证实验表明，简单的线性层连接即可实现最快收敛，而微调原生 ViT 反而导致训练崩溃，这进一步支持了“保持 VLM 骨干冻结、仅通过轻量级投影注入细节”的设计原则。

**对比流匹配的训练策略**。WeMMU 在早期预训练阶段采用对比流匹配损失（Eq. 4），利用批次内负样本加速桥接组件的收敛；在后期阶段切换为标准条件流匹配损失（Eq. 3），因为小批量下对比损失的优势不再显著。这一阶段性训练策略反映了对桥接任务特性的深入理解：早期需要强监督信号建立 VLM 与扩散模型之间的初始映射，后期则可依赖标准损失的稳定性进行精细优化。

### 适用边界与局限

WeMMU 在以下场景中展现出明确优势：
- **多任务图像编辑**：噪声查询令牌的泛化能力使模型能够在单图编辑、多图编辑等多种任务间切换，而无需为每个新任务重新训练（Figure 5）。
- **指令遵循密集型任务**：注意力向文本令牌的偏移使模型在需要精确理解编辑指令的场景中表现更好。

然而，该方法存在若干明确局限：
1. **多图编辑的拼接痕迹**：由于训练数据有限且质量不均，多图编辑结果可能产生可见的拼接边界，这在 Figure 5 的全模型输出中仍有体现。
2. **与大型专有模型的差距**：在编辑任务上仍落后于 GPT-4o、EMU3.5 等大规模专有模型，WeMMU 的优势主要体现在同规模统一模型中的竞争力。
3. **骨干依赖性**：框架依赖 Qwen2.5-VL-3B 和 Sana 1.6B 的特定兼容性，更换 VLM 或扩散模型骨干可能需要重新进行四阶段课程训练，迁移成本较高。
4. **噪声分布的固定性**：当前噪声查询令牌始终从 $\mathcal{N}(0,I)$ 采样，未探索分布参数的可学习性或任务自适应性。

### 开放问题

1. **强化学习微调的潜力**：当前 WeMMU 未使用 RL 微调（如 RLHF 或 DPO），而 Table 1 显示使用 RL 微调的模型在 GenEval 上表现更优。将噪声查询令牌框架与 RL 微调结合，可能进一步提升指令遵循精度和细节保真度。

2. **自适应噪声分布**：噪声令牌的分布是否可以是可学习的或条件于任务的？例如，对于需要强创造性的文生图任务和需要强保真度的编辑任务，最优噪声方差可能不同。

3. **对比流匹配的小批量改进**：论文指出对比流匹配在小批量下效果有限，但未深入探索改进方案。如何在保持训练效率的同时利用对比信号，是一个值得研究的方向。

4. **扩展到更大规模模型**：当前框架在约 8B 参数规模下验证有效，扩展到更大规模的多模态模型时，噪声查询令牌的随机化机制是否仍然有效，以及四阶段课程训练的策略是否需要调整，尚待验证。



## 原文 PDF

![[paperPDFs/CVPR_2026/WeMMU_Enhanced_Bridging_of_Vision_Language_Models_and_Diffusion_Models_via_Noisy_Query_Tokens.pdf]]
