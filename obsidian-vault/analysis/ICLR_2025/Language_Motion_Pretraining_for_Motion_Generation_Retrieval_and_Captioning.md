---
title: "LAMP: Language-Motion Pretraining for Motion Generation, Retrieval, and Captioning"
type: paper
paper_level: A
venue: ICLR
year: 2025
pdf_ref: paperPDFs/ICLR_2025/Language_Motion_Pretraining_for_Motion_Generation_Retrieval_and_Captioning.pdf
aliases:
- LLMPLTLFLM
- LAMP
tags:
- ICLR_2025
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
- topic/generative_models_diffusion
core_operator: 用专门的语言-运动预训练模型（LaMP）替换 CLIP 文本编码器，通过对比学习、匹配、运动引导文本生成和文本引导运动生成四个代理任务联合训练，将文本嵌入空间从语言-视觉转移到语言-运动，从而为下游任务提供运动信息丰富的文本特征和语言信息丰富的运动特征。
primary_logic: 语言-运动预训练对齐不仅为运动生成提供了更精确的条件信号，而且统一了运动生成、运动-文本检索和运动描述三个任务；通过引入查询令牌的交叉注意力，获得互信息丰富的跨模态表示，并提出 LaMP-BertScore 新指标评估生成运动的语义一致性。
claims:
- 在 HumanML3D 上，FID 从 SOTA 的 0.045 (MoMask) 降至 0.032，下降 28.9%；R Precision Top1 从 0.521 提升到 0.557。
- 在 KIT-ML 上，FID 从 SOTA 的 0.204 (MoMask) 降至 0.141，下降 30.9%；R Precision Top1 从 0.433 提升到 0.479。
- LaMP-Feat 在运动-文本检索任务上表现出更优的匹配能力，相似度矩阵热力图 (Figure 3) 显示正样本对角线颜色更深、对比度更强。
- 消融实验表明，文本引导运动生成任务对生成质量影响最大，移除后 FID 从 0.032 恶化到 0.226。
---

# LAMP: Language-Motion Pretraining for Motion Generation, Retrieval, and Captioning

> [!tip] 核心洞察
> 语言-运动预训练对齐不仅为运动生成提供了更精确的条件信号，而且统一了运动生成、运动-文本检索和运动描述三个任务；通过引入查询令牌的交叉注意力，获得互信息丰富的跨模态表示，并提出 LaMP-BertScore 新指标评估生成运动的语义一致性。

| 字段 | 内容 |
|------|------|
| 中文题名 | 语言-运动预训练模型（LaMP）用于运动生成、检索与描述 |
| 英文题名 | LAMP: Language-Motion Pretraining for Motion Generation, Retrieval, and Captioning |
| 会议/期刊 | ICLR 2025 |
| Links |  |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction #topic/generative_models_diffusion |
| Method | LaMP (Language-Motion Pretraining) + LaMP-T2M + LaMP-Feat + LaMP-M2T |
| Dataset | HumanML3D, KIT-ML |

> [!tip] 效果简介
> - HumanML3D 上，FID 0.032 vs 0.045 (MoMask) (-28.9%)；R Precision Top1 0.557 vs 0.521 (MoMask) (+6.9%)；Motion-Text Retrieval R@1 67.18 vs 58.17 (T2M) (+9.01)。
> - KIT-ML 上，FID 0.141 vs 0.204 (MoMask) (-30.9%)。

## 概述

### 问题瓶颈

现有文本驱动运动生成方法普遍依赖 CLIP 文本编码器作为条件信号。然而，CLIP 在静态图像-文本对上预训练，其文本特征侧重于静态视觉属性，难以捕捉与动态运动相关的语义信息，导致语言-运动对齐不足，生成的运动与文本描述之间的语义一致性受限。

### 核心方法

LaMP（Language-Motion Pretraining）提出一种语言-运动预训练框架，通过四个联合优化的代理任务——运动-文本对比学习、运动-文本匹配、运动引导文本生成和文本引导运动生成——将文本嵌入空间从语言-视觉对齐迁移至语言-运动对齐。在此基础上，LaMP 统一了下游三大任务：

- **LaMP-T2M**：以 LaMP 文本 Transformer 替代 CLIP 编码器，采用因果注意力掩码的解码器架构进行自回归掩码运动令牌预测，实现文本到运动生成。
- **LaMP-Feat**：利用冻结的 LaMP 运动编码器与查询令牌交叉注意力获得互信息丰富的跨模态表示，用于双向运动-文本检索。
- **LaMP-M2T**：将 LaMP 运动特征投影至大语言模型（OPT-2.7B）空间，通过 LoRA 微调实现运动描述生成。

### 核心结论

在 HumanML3D 和 KIT-ML 两个基准数据集上，LaMP-T2M 的 FID 分别降至 **0.032**（较 MoMask 的 0.045 下降 28.9%）和 **0.141**（较 MoMask 的 0.204 下降 30.9%），R Precision Top1 分别提升至 0.557 和 0.479。消融实验表明，文本引导运动生成任务对生成质量影响最大（移除后 FID 恶化至 0.226），因果注意力掩码架构相比双向掩码取得显著更优的 FID（0.032 vs 0.109）。此外，LaMP-Feat 在运动-文本检索任务上展现出更优的匹配能力。

### 方法谱系与知识库定位

LaMP 属于**语言-运动联合预训练**范式，区别于以下主流路线：

| 路线 | 代表方法 | 核心差异 |
|------|----------|----------|
| 扩散式生成 | MDM（Tevet et al., ICCV 2023）、MotionDiffuse（Zhang et al., arXiv 2022）、ReMoDiffuse（Zhang et al., ICCV 2023） | 以扩散过程建模运动分布，LaMP 采用离散令牌自回归预测 |
| VQ-VAE + 掩码预测 | T2M-GPT（Zhang et al., CVPR 2023）、MoMask（Guo et al., ICCV 2023） | 共享离散运动令牌范式，但 LaMP 以因果注意力替代双向掩码，并以 LaMP 编码器替代 CLIP |
| LLM 统一生成 | MotionGPT（Zhang et al., AAAI 2024） | MotionGPT 将运动视为语言令牌统一建模，LaMP 专注于跨模态对齐预训练与模块化下游适配 |

LaMP 的关键增量在于：通过显式的语言-运动预训练对齐，为运动生成提供运动信息丰富的文本特征，同时以统一的预训练骨干支撑生成、检索、描述三个任务，形成闭环的跨模态理解与生成框架。

## 背景与动机

### 问题背景

文本驱动的三维人体运动生成旨在根据自然语言描述合成逼真的动作序列，在动画制作、虚拟人交互、游戏开发等领域具有广泛的应用前景。该任务的核心挑战在于实现语言与运动两种异质模态之间的精确对齐——文本描述往往包含复杂的时序语义（如“先向前走两步，然后转身挥手”），而运动数据则是高维连续时间序列，二者之间存在显著的语义鸿沟。

### 现有方法缺口：CLIP 文本嵌入的对齐不足

当前主流方法（如 **T2M** (Guo et al., CVPR 2022)、**MoMask** (Guo et al., ICCV 2023)、**T2M-GPT** (Zhang et al., CVPR 2023)、**MDM** (Tevet et al., ICCV 2023)、**MLD** (Chen et al., CVPR 2023) 等）普遍依赖 CLIP 模型的文本编码器提取条件信号，将其作为运动生成器的输入。然而，这一范式存在根本性局限：**CLIP 是在静态图像-文本对上预训练的，其文本特征侧重于描述物体的静态视觉属性（如颜色、形状、空间关系），无法有效捕捉与动态运动相关的时序语义信息**（如速度、节奏、动作转换逻辑）。因此，CLIP 的文本嵌入空间与运动语义空间之间存在系统性偏差，导致语言-运动对齐不够精确，生成的运动在语义相关性上表现不足。

具体而言，这一瓶颈体现在以下层面：
- **条件信号质量受限**：CLIP 文本特征携带的运动相关信息不足，使得生成器难以从文本中准确解码出细粒度的运动意图。
- **跨模态检索性能受限**：基于 CLIP 特征的运动-文本匹配难以区分语义相近但运动细节不同的文本描述。
- **运动描述能力缺失**：CLIP 编码器无法为运动到文本的逆向生成提供有效的运动特征表示。

### 本文动机：从语言-视觉到语言-运动的预训练迁移

针对上述问题，本文提出核心假设：**通过专门的语言-运动联合预训练，将文本嵌入空间从语言-视觉对齐迁移到语言-运动对齐，可以为下游任务提供运动信息丰富的文本特征和语言信息丰富的运动特征**。这一假设基于以下观察：运动数据本身包含丰富的时序变化模式，若能以自监督的方式学习文本与运动令牌之间的细粒度对应关系，则有望从根本上解决 CLIP 带来的语义偏差问题。

基于此动机，本文提出 **LaMP（Language-Motion Pretraining）**，一种统一的语言-运动预训练框架，通过四个互补的代理任务——运动-文本对比学习、运动-文本匹配、运动引导文本生成和文本引导运动生成——联合优化文本和运动编码器，实现对运动语义的深度对齐。在此基础上，LaMP 衍生出三个下游模型：**LaMP-T2M**（文本到运动生成）、**LaMP-Feat**（运动-文本双向检索）和 **LaMP-M2T**（运动描述生成），将预训练对齐能力统一应用于生成、检索和描述三大任务。

## 核心创新

### 从语言-视觉到语言-运动的文本空间迁移

现有运动生成方法普遍依赖 CLIP 文本编码器提取条件信号，但 CLIP 在静态图像-文本对上预训练，其文本特征侧重于物体的外观属性，无法有效捕捉与动态运动相关的语义信息。这一瓶颈导致语言-运动对齐不足，生成动作的语义相关性受限。LaMP 的核心创新在于**用专门的“语言-运动”预训练替代 CLIP 的“语言-视觉”预训练**，将文本嵌入空间从视觉域迁移到运动域，从而为下游任务提供运动信息丰富的文本特征。

这一迁移通过**四个共享参数的代理任务联合训练**实现（Figure 1）：
- **运动-文本对比学习**：拉近匹配的运动-文本对，推远不匹配的样本；
- **运动-文本匹配**：二分类任务判断运动与文本是否配对；
- **运动引导的文本生成**：给定运动序列，自回归生成对应的文本描述；
- **文本引导的运动生成**：给定文本，预测被掩码的运动令牌。

其中，文本引导运动生成任务对生成质量影响最大——消融实验表明，移除该任务后 FID 从 0.032 恶化至 0.226（Table 5），证明它是语言-运动对齐的关键驱动力。

### 预训练架构的跨模态交互设计

LaMP 预训练架构由两个共享自注意力层的 Transformer 组成：运动 Transformer 和文本 Transformer（Figure 1）。两者通过**查询令牌的交叉注意力机制**实现信息交互，使文本特征能感知运动语义，运动特征也能融入语言信息。这种设计产出的跨模态表示同时服务于生成、检索和描述三个任务，形成了统一的语言-运动表征基础。

### 从双向掩码到因果自回归的生成范式转变

在运动生成阶段，LaMP-T2M 做出了两项关键设计改变：

1. **文本编码器替换**：用 LaMP 文本 Transformer 替代 CLIP 作为条件编码器。消融实验显示，仅此替换便使 FID 从 0.226 降至 0.109，R Precision Top1 从 0.423 升至 0.554（Table 6）。

2. **因果注意力掩码**：采用解码器架构（decoder-only）替代传统的双向掩码编码器。作者指出，双向掩码会导致低秩矩阵退化，削弱模型的表达能力；而因果注意力掩码通过自回归预测机制增强了被掩码区域内部的信息交互。实验表明，这一改变使 FID 从 0.109 进一步降至 0.032，R Precision Top3 从 0.829 提升至 0.843（Table 6）。

推理时，LaMP-T2M 采用无分类器引导策略，通过调节条件逻辑值 $l_c$ 与无条件逻辑值 $l_{uc}$ 的差值来增强文本引导强度：

$$l_f = (1 + \alpha) \cdot l_c - \alpha \cdot l_{uc}$$

其中 $\alpha$ 设为 4，以平衡生成质量与文本一致性。

### 统一的跨任务能力

LaMP 预训练产出的特征同时赋能三个下游任务，无需为每个任务独立设计对齐模块：
- **运动生成**：LaMP-T2M 利用预训练的文本编码器提供条件信号；
- **运动-文本检索**：LaMP-Feat 直接使用冻结的运动编码器输出和查询令牌进行双向检索，相似度矩阵热力图（Figure 3）显示正样本对角线颜色更深、对比度更强，表明匹配能力优于 T2M；
- **运动描述**：LaMP-M2T 将运动 Transformer 输出的语言信息丰富的运动特征通过全连接层投影到 LLM（OPT-2.7b）的文本嵌入空间，并用 LoRA 微调实现运动到文本的生成。

### 新评估指标 LaMP-BertScore

针对现有指标难以评估生成运动语义一致性的问题，作者提出了 LaMP-BertScore：将生成的运动输入 LaMP-M2T 获取其文本描述，再与真实文本计算 BertScore。该指标直接衡量生成运动与文本条件的语义对齐程度，弥补了 FID 等分布层面指标的不足。但需注意，该指标依赖自训练的描述模型，可能存在自我增强偏差，需要外部独立验证。

## 整体框架

LaMP 的核心思想是通过语言-运动联合预训练，构建一个统一的多任务框架，使文本和运动序列在共享的表示空间中对齐。整体架构围绕三个关键设计展开：运动离散化、跨模态对齐预训练，以及面向下游任务的适配器。

### 运动离散化：VQ-VAE 令牌化

原始运动序列是连续的高维时间序列，难以直接与离散的文本令牌进行联合建模。LaMP 采用标准的 VQ-VAE 作为运动令牌化器，将运动序列转换为离散令牌元组。具体而言，编码器将运动序列压缩为潜变量，每个潜向量通过欧氏距离最近邻查找映射到共享码本中的离散嵌入：

$$\mathcal{Q}(m_i) = z_s, \quad \text{where } s = \arg\min_{j \in \{1...S\}} \|z_j - m_i\|_2$$

VQ-VAE 的训练目标包含三项：重建损失、嵌入损失（将码本向量拉向编码器输出）和承诺损失（将编码器输出拉向码本向量），其总损失为：

$$\mathcal{L}_{vq} = \mathcal{L}_{recon} + \sum_{i=0}^{n} \|\mathrm{sg}[m_i] - z_s\|_2 + \beta \sum_{i=0}^{n} \|m_i - \mathrm{sg}[z_s]\|_2$$

这一离散化步骤将连续运动转化为离散令牌序列，为后续的掩码预测和跨模态生成任务提供了统一的符号基础。

### 跨模态对齐预训练：LaMP 核心

LaMP 预训练模块由两个共享自注意力层的 Transformer 子模块组成：运动 Transformer 和文本 Transformer。运动 Transformer 接收冻结的运动编码器输出，并通过可学习的查询令牌（query tokens）与运动特征进行交叉注意力交互，提取语言信息丰富的运动表示；文本 Transformer 则对令牌化的文本描述进行编码。

预训练阶段联合优化四个代理任务，所有任务共享相同的输入格式和模型参数：

1. **运动-文本对比学习**：拉近匹配的运动-文本对在联合嵌入空间中的距离，推远非匹配对。
2. **运动-文本匹配**：二分类任务，判断给定的运动序列与文本描述是否匹配。
3. **运动引导文本生成**：给定运动序列，自回归生成对应的文本描述令牌。
4. **文本引导运动生成**：给定文本描述，预测被掩码的运动令牌，其损失为预测令牌与真实码本索引之间的交叉熵：

$$\mathcal{L}_{tgm} = \sum_{i=1}^{n} \mathrm{Cross-Entropy}(F(g_i), b_i)$$

这四个任务的关键因果机制在于：文本引导运动生成任务直接迫使文本编码器学习与运动动态相关的语义信息，而非 CLIP 所侧重的静态视觉属性。消融实验证实了这一点——移除该任务后，FID 从 0.032 急剧恶化至 0.226（Table 5），表明该任务是运动语义对齐的核心驱动力。

### 下游任务适配器

预训练完成后，LaMP 的文本编码器和运动编码器被冻结或微调，分别服务于三个下游任务：

- **LaMP-T2M（文本到运动生成）**：采用仅解码器架构，以因果注意力掩码替代传统的双向掩码。给定文本条件，对部分掩码的运动令牌序列进行自回归预测。掩码比例遵循余弦调度 $\gamma(r) = \cos(\pi r/2)$，推理时使用无分类器引导增强文本条件强度：

$$l_f = (1 + \alpha) \cdot l_c - \alpha \cdot l_{uc}$$

其中 $\alpha=4$。因果注意力掩码的引入使 FID 从双向掩码的 0.109 进一步降至 0.032（Table 6），其机制在于避免了编码器架构中低秩矩阵导致的表达能力退化。

- **LaMP-Feat（运动-文本检索）**：直接使用冻结的运动编码器提取运动嵌入，与文本嵌入计算相似度，实现双向检索。相似度矩阵热力图（Figure 3）显示，正样本对角线颜色更深、对比度更强，验证了 LaMP 特征在匹配任务上的优势。

- **LaMP-M2T（运动描述生成）**：将运动 Transformer 输出的运动特征通过全连接层线性投影到预训练大语言模型（OPT-2.7b）的文本嵌入空间，使用 LoRA 进行高效微调，实现运动到文本的生成。

### 数据流与模块关系

整个框架的数据流可以概括为：原始运动序列 → VQ-VAE 令牌化 → 运动令牌 + 文本令牌 → LaMP 联合预训练（四个任务共享参数）→ 冻结/微调的特征提取器 → 下游任务适配器（生成/检索/描述）。模块间的关系是松耦合的——预训练阶段产生的对齐表示可以被任一适配器复用，这种设计使得 LaMP 能够同时服务于三个性质不同的任务，而无需为每个任务从头训练独立的特征提取器。

### 补充图表

![[assets/figures/papers/paper_list_l1901_Language_Motion_Pretraining_for_Motion_Generation_Retrieval_and_Captioni/figures/001_Figure_1.jpg]]
*Figure 1: LaMP overview. We conduct joint training for contrastive learning, matching, and bidirectional text-motion translation by leveraging the textual features extracted from tokenized text descriptions via the text transformer and the motion features derived from the motion transformer*

## 核心模块与公式推导

### 运动离散化：VQ-VAE 令牌化

LaMP 采用标准的 VQ-VAE 将连续运动序列转换为离散令牌序列，作为后续所有任务的基础表示。运动序列经编码器映射为潜变量后，通过最近邻查找替换为码本中的离散嵌入：

$$
\mathcal{Q}(m_i) = z_s, \quad \text{where } s = \arg\min_{j \in \{1...S\}} \|z_j - m_i\|_2
$$

训练目标由三部分构成——重建损失、嵌入损失和承诺损失：

$$
\mathcal{L}_{vq} = \mathcal{L}_{recon} + \sum_{i=0}^{n} \|\mathrm{sg}[m_i] - z_s\|_2 + \beta \sum_{i=0}^{n} \|m_i - \mathrm{sg}[z_s]\|_2
$$

其中 $\mathrm{sg}[\cdot]$ 为停止梯度算子，$\beta$ 控制承诺损失权重。该离散化使运动序列可与文本令牌共享统一的序列建模范式。

### 预训练对齐：LaMP 双 Transformer 架构

LaMP 由两个共享自注意力层的 Transformer 子模块构成：运动 Transformer 与文本 Transformer。运动 Transformer 接收冻结运动编码器输出的运动特征，并通过可学习的查询令牌（query tokens）与文本 Transformer 的文本特征进行交叉注意力交互，获得互信息丰富的跨模态表示。

预训练阶段联合优化四个代理任务，共享统一的输入格式与模型参数：

- **运动-文本对比学习（Motion-Text Contrastive Learning）**：对齐成对的正样本表示，推开负样本。
- **运动-文本匹配（Motion-Text Matching）**：二分类判断运动-文本对是否匹配。
- **运动引导文本生成（Motion-grounded Text Generation）**：以运动特征为条件自回归生成文本描述。
- **文本引导运动生成（Text-grounded Motion Generation）**：以文本特征为条件预测运动令牌的码本索引，损失函数为：

$$
\mathcal{L}_{tgm} = \sum_{i=1}^{n} \mathrm{Cross-Entropy}(F(g_i), b_i)
$$

其中 $F$ 将生成令牌 $g_i$ 映射到码本空间，$b_i$ 为真实码本索引。该任务在消融实验中被证明对生成质量影响最大——移除后 FID 从 0.032 恶化至 0.226（Table 5）。

### 运动生成：LaMP-T2M 掩码预测

LaMP-T2M 以预训练 LaMP 的文本 Transformer 提取条件嵌入，取代 CLIP 文本编码器。生成采用自回归掩码预测机制：给定文本 $t$ 和部分掩码的运动序列 $m^M$，预测所有被掩码令牌：

$$
\mathcal{L}_{mask} = \sum_{m_k^M = [M]} -\log p(m_k^M \mid m^M, t)
$$

掩码比例按余弦调度 $\gamma(r) = \cos(\pi r/2)$ 随训练步数 $r$ 变化，被掩码位置以 80% 概率替换为 `[M]` 令牌、10% 替换为随机令牌、10% 保持不变。架构采用因果注意力掩码的解码器（decoder-only），逐令牌自回归预测，优化目标为最大化期望对数似然：

$$
\max_{\theta} \mathbb{E} \big[ \sum_{i=1}^{n} \log P_{\theta}(m_i^M \mid t, m_{<i}^M) \big]
$$

推理时引入无分类器引导（classifier-free guidance），通过调节条件逻辑值 $l_c$ 与无条件逻辑值 $l_{uc}$ 增强文本引导强度：

$$
l_f = (1 + \alpha) \cdot l_c - \alpha \cdot l_{uc}
$$

其中 $\alpha = 4$ 为引导尺度。

### 运动描述与评估：LaMP-M2T 与 LaMP-BertScore

LaMP-M2T 将预训练 LaMP 的运动 Transformer 输出的运动特征 $f_m$ 通过全连接层线性投影到 LLM（OPT-2.7b）的文本嵌入空间，并使用 LoRA 微调 LLM 生成运动描述。基于此，提出 **LaMP-BertScore** 指标：将生成的运动输入 LaMP-M2T 获得文本描述，再与真实文本计算 BertScore，以评估生成运动的语义一致性。

### 关键架构选择：解码器与因果注意力

消融实验（Table 6）揭示了两个关键设计选择的因果效应：

1. **LaMP 文本编码器 vs. CLIP 文本编码器**：替换 CLIP 后 FID 从 0.226 降至 0.109，R Precision Top1 从 0.423 升至 0.554，验证了语言-运动对齐预训练对条件信号质量的显著提升。
2. **因果注意力掩码 vs. 双向掩码**：采用解码器架构后 FID 从 0.109 进一步降至 0.032，R Precision Top3 从 0.829 提升至 0.843。论文认为因果注意力掩码通过防止低秩矩阵导致的表达能力退化，增强了掩码区域内的信息交互。

### 补充图表

![[assets/figures/papers/paper_list_l1901_Language_Motion_Pretraining_for_Motion_Generation_Retrieval_and_Captioni/figures/002_Figure_2.jpg]]
*Figure 2: LaMP-T2M and LaMP-M2T frameworks overview. (Left) Pretrained LaMP’s text transformer is employed to extract condition embedding and autoregressive mask prediction is performed. (Right) Finetuning an LLM to achieve motion captioning*

![[assets/figures/papers/paper_list_l1901_Language_Motion_Pretraining_for_Motion_Generation_Retrieval_and_Captioni/figures/011_Figure.jpg]]
*Figure: A1: Overview of VQVAE*

![[assets/figures/papers/paper_list_l1901_Language_Motion_Pretraining_for_Motion_Generation_Retrieval_and_Captioni/figures/013_Table.jpg]]
*Table: Figure A2: (Left) Details in LaMP. Motion transformer consists of self-attention layers and cross-attention layers (interact with query tokens), while text transformer only has self-attention layers. (Right) LaMP extracts text features as condition signals. Table A1: The quantitative results of text-to-motion generation on the KIT-ML dataset with LaMP pretrained on HumanML3D (the first row) and KIT-ML (the second row)*

## 实验与分析

### 核心性能瓶颈

现有文本驱动运动生成方法普遍依赖 CLIP 文本编码器提取条件信号。CLIP 在静态图像-文本对上预训练，其文本特征侧重于静态视觉属性，无法有效捕捉与动态运动相关的语义信息。这种语言-视觉空间到语言-运动空间的错位，导致生成运动与文本描述之间的语义相关性不足，成为制约生成质量的关键瓶颈。

LaMP 通过四项联合预训练任务——运动-文本对比学习、运动-文本匹配、运动引导文本生成和文本引导运动生成——将文本嵌入空间从语言-视觉显式迁移至语言-运动。这一预训练对齐策略为下游任务提供了运动信息丰富的文本特征，同时通过查询令牌的交叉注意力机制获得互信息丰富的跨模态表示，统一了运动生成、运动-文本检索和运动描述三个任务。

### 运动生成主结果

在 HumanML3D 和 KIT-ML 两个标准基准上，LaMP-T2M 在所有核心指标上均取得显著提升。**Table 1** 展示了使用先前方法评估器的定量结果：

![[assets/figures/papers/paper_list_l1901_Language_Motion_Pretraining_for_Motion_Generation_Retrieval_and_Captioni/figures/005_Table_1.jpg]]
*Table 1: The quantitative results of text-to-motion generation with evaluator following previous methods on the HumanML3D dataset and the KIT-ML dataset*

- **HumanML3D**：FID 从 SOTA 的 0.045（MoMask, Guo et al., ICCV 2023）降至 **0.032**，下降 28.9%；R Precision Top1 从 0.521 提升至 **0.557**，提升 6.9%；MultiModal Dist 从 2.958 降至 **2.759**。
- **KIT-ML**：FID 从 0.204（MoMask）降至 **0.141**，下降 30.9%；R Precision Top1 从 0.433 提升至 **0.479**；MultiModal Dist 从 2.779 降至 **2.362**。

相较于扩散式方法（MDM, Tevet et al., ICCV 2023; MotionDiffuse, Zhang et al., arXiv 2022; ReMoDiffuse, Zhang et al., ICCV 2023）和变换器式方法（T2M-GPT, Zhang et al., CVPR 2023; MoMask; MotionGPT, Zhang et al., AAAI 2024），LaMP-T2M 在 FID 和 R Precision 上均建立了一致的领先优势。

**Table 2** 报告了使用 LaMP 自身评估器（LaMP evaluator）的结果。在 HumanML3D 上，LaMP-T2M 的 LaMP-R Precision Top1 达到 **0.867**，显著高于 T2M-GPT 的 0.808 和 MoMask 的 0.784；在 KIT-ML 上，LaMP-R Precision Top1 为 **0.784**，同样领先。这一跨评估器的一致性验证了性能提升并非来自评估偏差。

### 运动-文本检索结果

**Table 3** 展示了运动-文本双向检索的基准对比。在 HumanML3D 上，LaMP-Feat 在运动→文本检索的 R@1 达到 **67.18**，较 T2M（Guo et al., CVPR 2022）的 58.17 提升 9.01 个百分点，较 TMR（Petrovich et al., ICCV 2023）的 60.56 提升 6.62 个百分点。在文本→运动检索上，R@1 同样取得领先。**Figure 3** 的相似度矩阵热力图进一步验证了 LaMP-Feat 的匹配能力：正样本对角线颜色更深、对比度更强，表明跨模态对齐更加精确。

### 运动描述结果

**Table 4** 展示了运动描述任务的定量结果。LaMP-M2T 在 HumanML3D 上遵循 Jiang et al., 2023 的评估框架，在 BLEU、ROUGE、CIDEr 和 BertScore 等指标上均优于 TM2T（Guo et al., ECCV 2022）和 DLP（Cai et al., CVPR 2024）。这一结果表明，LaMP 预训练获得的语言信息丰富的运动特征能够有效支撑下游的文本生成任务。

### 消融实验

**预训练任务消融（Table 5）** 揭示了四项代理任务对生成性能的影响权重。完整 LaMP 预训练取得 FID 0.032、R Precision Top1 0.557。移除文本引导运动生成（text-grounded motion generation）任务后，FID 急剧恶化至 **0.226**，R Precision Top1 降至 **0.423**，证明该任务对生成质量影响最大。移除运动引导文本生成任务后，FID 升至 0.066。单独移除对比学习或匹配任务也会导致不同程度的性能下降，但影响相对温和。

**生成组件消融（Table 6）** 验证了三个关键设计选择：

1. **文本编码器替换**：用 LaMP 文本编码器替换 CLIP 文本编码器，FID 从 0.226 降至 **0.109**，R Precision Top1 从 0.423 升至 **0.554**。这一对比直接量化了语言-运动对齐预训练相对于语言-视觉预训练的优势。

2. **注意力掩码策略**：采用因果注意力掩码的解码器架构（decoder-only）与双向掩码的编码器架构相比，FID 从 0.109 进一步降至 **0.032**，R Precision Top3 从 0.829 提升至 **0.843**。因果注意力掩码通过自回归预测机制增强了掩码区域内的信息交互，同时缓解了双向掩码中低秩矩阵导致的表达力退化问题。

3. **查询令牌交互**：移除查询令牌的交叉注意力后，FID 升至 0.041，R Precision Top1 降至 0.543，验证了查询令牌在跨模态信息融合中的关键作用。

### 失败模式与局限性

尽管 LaMP 在标准基准上表现优异，仍存在以下可识别的失败模式：

- **标注错误敏感性**：当训练数据中 ground truth 运动与文本描述不一致时，模型倾向于生成符合文本语义但与标注运动不匹配的结果，导致评估指标恶化。
- **分布外泛化不足**：模型对训练集未见过的运动类型（如卡通人物的飞行、非人类运动）效果较差，泛化能力受限于 HumanML3D 和 KIT-ML 的数据分布。
- **LaMP-BertScore 的自我增强风险**：该指标依赖自训练的 LaMP-M2T 描述模型计算生成运动与 ground truth 文本之间的语义相似度，可能存在自我偏向，需要外部独立验证作为补充。

### 关键公式与推理机制

运动生成阶段采用自回归掩码预测目标：

$$\max_{\theta} \mathbb{E} \big[ \sum_{i=1}^{n} \log P_{\theta}(m_i^M | t, m_{<i}^M) \big]$$

推理时引入无分类器引导，通过调节条件逻辑值相对于无条件逻辑值来增强文本引导强度：

$$l_f = (1 + \alpha) \cdot l_c - \alpha \cdot l_{uc}$$

其中引导尺度 $\alpha$ 设为 4，在生成质量和文本一致性之间取得平衡。

### 补充图表

![[assets/figures/papers/paper_list_l1901_Language_Motion_Pretraining_for_Motion_Generation_Retrieval_and_Captioni/figures/009_Table_5.jpg]]
*Table 5: Ablation study of the impact of different tasks in LaMP on generative performance on HumanML3D*

![[assets/figures/papers/paper_list_l1901_Language_Motion_Pretraining_for_Motion_Generation_Retrieval_and_Captioni/figures/010_Table_6.jpg]]
*Table 6: Ablation study of text-to-motion generation on HumanML3D. We report the impact of LaMP’s text encoder, interactions with query tokens, and the mask prediction manner on the results*

![[assets/figures/papers/paper_list_l1901_Language_Motion_Pretraining_for_Motion_Generation_Retrieval_and_Captioni/figures/007_Table_3.jpg]]
*Table 3: Text-motion (left) and motion-text (right) retrieval benchmark on the HumanML3D and KIT-ML*

![[assets/figures/papers/paper_list_l1901_Language_Motion_Pretraining_for_Motion_Generation_Retrieval_and_Captioni/figures/006_Table_2.jpg]]
*Table 2: Evaluation results of text-to-motion generation with LaMP evaluator on T2M-GPT, MoMask, and ours*

![[assets/figures/papers/paper_list_l1901_Language_Motion_Pretraining_for_Motion_Generation_Retrieval_and_Captioni/figures/008_Table_4.jpg]]
*Table 4: The quantitative results of motion captioning on the HumanML3D, we adhere to the evaluation frameworks outlined in (Jiang et al., 2023)*

![[assets/figures/papers/paper_list_l1901_Language_Motion_Pretraining_for_Motion_Generation_Retrieval_and_Captioni/figures/004_Figure_4.jpg]]
*Figure 4: Qualitative results of text-to-motion generation on HumanML3D*

![[assets/figures/papers/paper_list_l1901_Language_Motion_Pretraining_for_Motion_Generation_Retrieval_and_Captioni/figures/003_Figure_3.jpg]]
*Figure 3: Heatmap of similarity matrix. The diagonal represents positive sample pairs, with darker colors indicating better quality*

## 方法谱系与知识库定位

### 1. 核心瓶颈与因果机制

现有文本驱动运动生成方法普遍依赖 CLIP 文本编码器提取条件信号。然而，CLIP 在静态图像-文本对上预训练，其文本特征侧重于静态视觉属性（如颜色、形状、空间关系），无法有效捕捉与动态运动相关的语义信息（如动作的节奏、力度、过渡方式）。这一根本性错位导致语言-运动对齐不足，生成的运动语义相关性不高，构成当前方法的核心瓶颈。

LaMP 的因果调节变量在于：用专门的语言-运动预训练模型替换 CLIP 文本编码器。通过对比学习、匹配、运动引导文本生成和文本引导运动生成四个代理任务联合训练，将文本嵌入空间从“语言-视觉”转移到“语言-运动”，从而为下游任务提供运动信息丰富的文本特征和语言信息丰富的运动特征。这一预训练对齐不仅为运动生成提供了更精确的条件信号，而且统一了运动生成、运动-文本检索和运动描述三个任务。

### 2. 与现有工作的关系

#### 2.1 运动生成基线

LaMP-T2M 直接对标的运动生成方法覆盖了扩散式和变换器式两大主流范式：

- **扩散模型类**：**MDM** (Tevet et al., ICCV 2023) 基于扩散模型直接预测运动序列；**MotionDiffuse** (Zhang et al., arXiv 2022) 引入文本引导的扩散过程；**MLD** (Chen et al., CVPR 2023) 在潜空间进行扩散以加速推理；**PhysDiff** (Yuan et al., ICCV 2023) 融入物理约束提升运动合理性；**ReMoDiffuse** (Zhang et al., ICCV 2023) 利用检索增强扩散生成。

- **变换器/离散化方法**：**T2M** (Guo et al., CVPR 2022) 作为早期基线，采用 VQ-VAE 离散化与条件生成；**T2M-GPT** (Zhang et al., CVPR 2023) 将运动生成建模为自回归序列预测；**MoMask** (Guo et al., ICCV 2023) 引入掩码预测机制，是此前 SOTA；**MotionGPT** (Zhang et al., AAAI 2024) 探索统一语言-运动的大语言模型范式；**AttT2M** (Zhong et al., ICCV 2023) 关注文本驱动的注意力机制。

LaMP-T2M 在 HumanML3D 上将 FID 从 MoMask 的 0.045 降至 0.032（下降 28.9%），R Precision Top1 从 0.521 提升至 0.557（Table 1）；在 KIT-ML 上 FID 从 0.204 降至 0.141（下降 30.9%），R Precision Top1 从 0.433 提升至 0.479。这一提升的根本来源是预训练对齐的文本编码器替换了 CLIP，以及因果注意力掩码的解码器架构替代了双向掩码。

#### 2.2 运动-文本检索基线

**TMR** (Petrovich et al., ICCV 2023) 是运动-文本检索的代表性方法。LaMP-Feat 利用冻结的运动编码器与查询令牌交叉注意力，在 HumanML3D 上运动-文本检索 R@1 达到 67.18，相比 T2M 的 58.17 提升 9.01 个百分点（Table 3）。相似度矩阵热力图（Figure 3）显示正样本对角线颜色更深、对比度更强，验证了 LaMP-Feat 更优的匹配能力。

#### 2.3 运动描述基线

**TM2T** (Guo et al., ECCV 2022) 和 **DLP** (Cai et al., CVPR 2024) 是运动描述任务的代表性工作。LaMP-M2T 采用不同策略：将 LaMP 运动变换器特征通过全连接层投影到 LLM（OPT-2.7b）嵌入空间，并用 LoRA 微调，利用预训练 LLM 的语言能力生成描述。

### 3. 方法适用边界

LaMP 在以下条件下表现出显著优势：

- **数据条件**：在 HumanML3D 和 KIT-ML 两个标准人体运动数据集上验证有效，数据规模中等（万级样本）。
- **运动类型**：主要覆盖日常人体动作（走、跑、跳、挥手等），对训练集内分布的动作生成质量高。
- **任务范围**：统一支持运动生成、运动-文本双向检索和运动描述三个任务，共享预训练对齐表示。

### 4. 局限性与失效模式

论文明确指出的局限性包括：

- **标注错误敏感**：数据集文本标注错误会导致生成失败，例如 ground truth 运动与文本描述不一致时，模型无法正确学习对应关系。
- **泛化能力有限**：对训练集未见过的运动类型（如卡通人物的飞行）效果较差，表明模型依赖训练分布，跨域泛化不足。
- **LaMP-BertScore 的自我增强偏差**：新指标依赖自训练的描述模型计算语义相似度，可能存在自我增强偏差，需要外部独立验证。
- **数据集覆盖不足**：当前仅在 HumanML3D 和 KIT-ML 上验证，跨数据集泛化性有待进一步验证。

### 5. 开放问题

从论文工作延伸出的开放问题包括：

1. **大规模多样化预训练**：如何在更大规模、更多样化（包含非人类运动、动物运动、机械运动等）的数据集上预训练 LaMP 以增强泛化能力？
2. **训练数据质量治理**：如何系统性地修正或过滤训练数据中的错误标注以减少失败案例？
3. **因果注意力掩码的通用性**：解码器架构中因果注意力掩码防止秩崩溃的具体机制是否在其他序列建模任务上同样有效？这一发现是否具有更广泛的理论意义？
4. **评估指标标准化**：LaMP-BertScore 能否替代现有的人工评估或其它客观指标成为运动生成的标准语义评价指标？需要更大规模的元评估研究。
5. **预训练任务扩展**：是否可以通过扩展 LaMP 预训练任务（例如引入运动动力学约束、物理合理性建模）进一步提高对齐质量？四个代理任务的最优组合是否存在更高效的设计？

### 6. 知识库定位

LaMP 在方法谱系中的定位可概括为：

- **上游**：继承 VQ-VAE 运动离散化范式（源自 T2M），复用掩码预测生成框架（源自 MoMask），借鉴多任务预训练思路（源自视觉-语言预训练如 CLIP、ALBEF）。
- **核心创新**：将语言-运动对齐从隐式（CLIP 迁移）转为显式（四项代理任务联合预训练），并发现因果注意力掩码在掩码预测中优于双向掩码。
- **下游**：为运动生成、检索、描述提供统一的预训练表示，可作为后续工作的基础编码器。
- **与相邻领域的接口**：与视觉-语言预训练、离散化生成模型、LLM 微调等方向存在交叉，但聚焦于运动模态的特殊性（时序动态、物理约束）。

## 原文 PDF

![[paperPDFs/ICLR_2025/Language_Motion_Pretraining_for_Motion_Generation_Retrieval_and_Captioning.pdf]]