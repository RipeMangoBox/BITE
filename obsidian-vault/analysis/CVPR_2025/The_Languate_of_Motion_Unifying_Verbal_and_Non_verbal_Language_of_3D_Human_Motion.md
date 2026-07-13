---
title: "The Language of Motion: Unifying Verbal and Non-verbal Language of 3D Human Motion"
type: paper
paper_level: A
venue: CVPR
year: 2025
pdf_ref: paperPDFs/CVPR_2025/The_Languate_of_Motion_Unifying_Verbal_and_Non_verbal_Language_of_3D_Human_Motion.pdf
project_link: null
code_link: null
aliases:
- MLMMGU
- LMUVNVL3HM
tags:
- CVPR_2025
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
- topic/generative_models_diffusion
core_operator: 将人体运动拆解为面部、手部、上身、下身四部分的组合式离散分词，并在语言模型预训练阶段引入跨模态对齐（空间对齐、时间对齐、音频-文本对齐），使模型能够统一理解口语与非口语信号。
primary_logic: 将人体运动视为一种“语言”，与语音和文本共享统一的多模态词汇表。利用预训练语言模型的语义推理能力，通过“生成式预训练 + 指令精调”的两阶段策略，实现多模态运动理解与生成，并在多任务和数据稀缺场景下展现出强泛化性。
claims:
- 在BEATv2协同语音手势生成基准上显著超越现有最佳方法（EMAGE等）
- 移除语言模型预训练（随机权重）导致性能急剧下降（FGD 从5.301升至7.470），多模态预训练同样不可或缺
- 预训练赋予模型强运动先验，在数据极度稀缺时始终优于无预训练消融方案和EMAGE
- 模型解锁了从运动预测情绪等新任务，且在此任务上远超MotionGPT（后者几乎与随机基线持平）
---

# The Language of Motion: Unifying Verbal and Non-verbal Language of 3D Human Motion

> [!tip] 核心洞察
> 将人体运动视为一种“语言”，与语音和文本共享统一的多模态词汇表。利用预训练语言模型的语义推理能力，通过“生成式预训练 + 指令精调”的两阶段策略，实现多模态运动理解与生成，并在多任务和数据稀缺场景下展现出强泛化性。

| 字段 | 内容 |
|------|------|
| 中文题名 | 运动语言：统一3D人体运动的口语与非口语语言 |
| 英文题名 | The Language of Motion: Unifying Verbal and Non-verbal Language of 3D Human Motion |
| 会议/期刊 | CVPR 2025 |
| Links |  |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction #topic/generative_models_diffusion |
| Method | Multimodal Language Model for Motion Generation and Understanding |
| Dataset | BEATv2 |

> [!tip] 效果简介
> - BEATv2 上，FGD (↓), BC (↑), Diversity FGD 5.301, BC 7.780, Diversity 15.167 vs EMAGE (具体数值未在提取文本中出现，见Table 1) (优于所有现有方法，详见Table 1)。
> - BEATv2 (Motion to Emotion) 上，Rouge Cider (↑), BertScore (↑) Rouge 26.67, BertScore 16.94 vs MotionGPT (Rouge 10.67, BertScore 2.31) (+16.00 (Rouge), +14.63 (BertScore))。

## 概要

**问题瓶颈**：现有3D人体运动生成模型多针对单一模态（语音、文本或运动）独立设计，难以利用多模态数据的互补性。这导致两个突出困境——在标注数据稀缺时性能急剧衰退，以及无法同时响应语音与文本的复合指令。该瓶颈的深层原因在于缺乏一个统一的表示框架，使口语（语音/文本）与非口语（身体运动）信号能在同一语义空间中交互。

**核心洞察**：本文提出将人体运动视为一种“语言”，与语音和文本共享统一的多模态词汇表。具体而言，将人体运动拆解为面部、手部、上身、下身四个组合式部分，分别进行离散分词，再与语音令牌、文本令牌合并为统一词汇空间。基于此，利用预训练语言模型的语义推理能力，通过“生成式预训练 + 指令精调”两阶段策略，实现多模态运动理解与生成。

**方法定位**：该方法属于基于语言模型的多模态运动生成范式。与现有最优协同语音手势方法 **EMAGE**（Liu et al., CVPR 2024）和通用文本-运动模型 **MotionGPT**（Zhang et al., AAAI 2024）相比，核心差异体现在三个关键设计槽位：

1. **运动分词方式**：从单一身体整体分词（如HumanML3D表示）转变为面部、手部、上身、下身四部分独立VQ-VAE分词。
2. **预训练目标**：从无跨模态预训练转变为包含组合式运动对齐（空间互译、时间补全）和音频-文本对齐的生成式预训练。
3. **模型架构**：从特定任务的条件生成模型转变为基于预训练Flan-T5 Base（220M参数）的编码器-解码器Transformer，统一处理多模态令牌序列。

**主要结果**：
- 在BEATv2协同语音手势生成基准上，该方法显著超越现有最佳方法（Table 1；FGD 5.301，BC 7.780，Diversity 15.167）。
- 消融实验表明，移除语言模型预训练导致FGD从5.301升至7.470，移除多模态预训练同样损害性能（FGD 5.408），证明两阶段预训练均不可或缺（Table 1）。
- 在数据极度稀缺场景下，完整模型始终优于无预训练消融方案和EMAGE，验证了预训练赋予的强运动先验（Figure 5）。
- 模型解锁了从运动预测情绪等新任务，在此任务上远超MotionGPT（Rouge Cider 26.67 vs 10.67，BertScore 16.94 vs 2.31），而MotionGPT表现几乎与随机基线持平（Table 3）。



### 3D人体运动生成中的模态割裂

3D人体运动生成是计算机视觉与图形学领域的核心问题，其应用涵盖虚拟数字人、影视制作、游戏交互等场景。然而，现有运动生成模型普遍遵循“单模态专用”的设计范式：协同语音手势生成仅处理音频到姿态的映射，文本驱动运动生成仅处理文本到姿态的映射，两类任务由完全独立的模型架构完成。这种模态割裂带来了两个根本性瓶颈：

1. **数据稀缺下的性能崩溃**：单模态模型无法利用多模态数据间的互补信息。当某一模态的配对数据有限时，模型缺乏可迁移的运动先验，生成质量急剧下降。
2. **无法响应混合指令**：真实交互场景中，用户可能同时通过语音和文本传达意图（例如“边说边做手势”），但现有系统无法统一理解并融合口语与非口语信号。

### 核心洞察：运动即语言

本文的核心洞察是将人体运动视为一种“语言”——与语音和文本一样，运动承载着可被离散化和序列化建模的语义信息。人类在交流中天然地将口语（verbal）与非口语（non-verbal，如手势、表情）信号融合，而现有方法却将二者人为割裂。

基于这一洞察，本文提出将运动、语音和文本统一纳入一个共享的多模态词汇表，并借助预训练语言模型的语义推理能力，实现跨模态的理解与生成。这一思路的关键在于：语言模型天然擅长处理离散令牌序列，且其预训练阶段习得的序列建模能力可迁移至运动领域，从而在数据稀缺时提供强先验。

### 方法概览

为实现上述统一，本文设计了一个两阶段训练框架：

- **生成式预训练**：在语言模型预训练阶段引入跨模态对齐任务，包括组合式运动对齐（空间互译、时间补全）和音频-文本对齐，使模型初步建立多模态令牌间的对应关系。
- **指令精调**：将下游任务（如协同语音手势生成、运动到情绪预测）统一为自然语言指令格式，在预训练模型基础上进行微调，使其能遵循指令完成多样化任务。

该框架以预训练Flan-T5 Base（220M参数）编码器-解码器Transformer为骨干，输入与输出均表示为统一多模态词汇表中的离散令牌，实现了“任意模态到任意模态”的灵活映射。



## 核心方法与创新机理

本工作将人体运动视为一种与口语和非口语信号共享统一词汇表的“语言”，并围绕这一理念构建了三个层次的关键创新，从根本上改变了多模态人体运动生成与理解的范式。

### 创新一：组合式身体运动分词——从整体到部分的解构

现有运动生成方法通常将人体运动视为单一整体进行编码（如HumanML3D的全局运动表示或单一VQ-VAE），这种粗粒度表示难以捕捉面部微表情、手部精细动作与躯干姿态之间的解耦关系。本文提出的**组合式身体运动分词**将人体运动按功能拆解为四个独立部分：面部（含FLAME表情参数）、手部（30个关节）、上身（13个关节）和下身（9个关节），并分别为每部分训练独立的VQ-VAE分词器。每个VQ-VAE将连续运动特征量化为离散令牌：

$$\mathbf{q}^t = \mathcal{Q}(\mathbf{z}^t) := \arg\min_{\mathbf{q}^k \in Q} \|\mathbf{z}^t - \mathbf{q}^k\|^2$$

这一设计的深层动机在于：不同身体部位在沟通中承担不同的语义功能——面部传递情绪，手部执行指示性手势，上身和下身分别负责姿态表达和空间位移。组合式分词使模型能够独立关注各部分的运动模式，同时通过统一的VQ-VAE训练损失（包含姿态/网格重建、速度、加速度及码本承诺损失）保证重建质量：

$$\mathcal{L}_{total} = \mathcal{L}_{rec}(\mathbf{g}, \hat{\mathbf{g}}) + \mathcal{L}_{vel}(\mathbf{g}', \hat{\mathbf{g}}') + \mathcal{L}_{acc}(\mathbf{g}'', \hat{\mathbf{g}}'') + \mathcal{L}_{mrec}(\mathbf{g}, \hat{\mathbf{g}}) + \mathcal{L}_{mvel}(\mathbf{g}', \hat{\mathbf{g}}') + \mathcal{L}_{macc}(\mathbf{g}'', \hat{\mathbf{g}}'') + \mathcal{L}_{comm}(\mathbf{g}, \mathbf{q})$$

四个部分的令牌空间与文本（SentencePiece，32k词汇量，继承自T5）和音频（HuBERT，将16kHz语音降采样至50Hz）令牌合并为统一的多模态词汇表：

$$M := Q \cup A \cup W \cup C = \{ \mathbf{q}_f, \mathbf{q}_u, \mathbf{q}_h, \mathbf{q}_l, \mathbf{a}, \mathbf{w} \}$$

这一统一词汇表是后续语言模型跨模态推理的基石。

### 创新二：生成式跨模态预训练——空间、时间与语义的三维对齐

现有方法通常直接在下游任务的配对数据上训练，缺乏对多模态数据内在结构的系统性建模。本文提出**两阶段训练策略**，其核心是预训练阶段的三种跨模态对齐任务：

- **空间对齐**：在同一时间步内，将某一身体部位的运动令牌翻译为另一部位的令牌（如从手部运动预测上身姿态），迫使模型学习身体各部位间的空间协调关系。
- **时间对齐**：给定部分时间步的运动序列，预测被掩蔽或未来的运动令牌（运动补全与预测），使模型捕获运动的时序动态。
- **音频-文本对齐**：在语音与对应文本之间进行互译，建立声学信号与语义内容的桥梁。

这三种对齐任务统一在语言模型的自回归训练框架下：

$$\mathcal{L}_{LM} = - \sum_{k=0}^{L_t-1} \log p_{\theta}(s_t^k | s_t^{<k}, s_i)$$

这种预训练策略的因果效应在消融实验中得到了有力验证（Table 2）：移除空间对齐导致FGD升至6.336，移除时间对齐使FGD恶化至6.800，而完全移除运动预训练则使FGD飙升至7.776（完整模型为5.301）。更重要的是，预训练赋予模型的强运动先验在数据稀缺场景下展现出决定性优势（Figure 5）：完整模型在任意数据量下始终优于无预训练消融方案和EMAGE。

### 创新三：基于预训练语言模型的统一架构——从专用模型到通用推理

与EMAGE（专用协同语音手势生成模型）或MotionGPT（文本-运动生成模型）等任务特定架构不同，本文直接采用220M参数的预训练**Flan-T5 Base**编码器-解码器Transformer作为骨干网络。所有模态的令牌通过统一词汇表被表示为“文本”令牌，编码器处理混合模态输入，解码器自回归预测目标序列。这一设计的关键优势在于：

- **继承语言模型的语义推理能力**：预训练的Flan-T5天然具备强大的语义理解，使其在协同语音手势生成中能更好地对齐语音韵律与语义内容。
- **解锁涌现任务能力**：通过指令精调，模型不仅能够执行训练时见过的任务（如协同语音手势生成），还能泛化到未见过的任务组合。最突出的证据是运动到情绪预测任务（Table 3）：本文方法取得Rouge 26.67、BertScore 16.94，而MotionGPT仅获10.67和2.31，几乎与随机基线（4.44, 0.19）持平——这揭示了专用模型在多模态理解上的根本性局限。
- **可编辑手势生成**：模型能同时接受语音和文本指令，在保持语音驱动手势的同时响应文本指定的语义编辑（Figure 6），这是现有单一模态方法无法实现的能力。

移除语言模型预训练（使用随机初始化权重）的消融实验（Table 1）进一步证实了这一创新不可或缺：FGD从5.301恶化至7.470，BC从7.780降至6.148，Diversity从15.167降至14.162，表明语言模型的语义先验是多模态运动生成性能的关键支撑。

### 创新总结

三项创新构成一条清晰的因果链：**组合式分词**提供了细粒度的运动表示基础，**跨模态预训练**建立了空间、时间与语义的三维对齐，**预训练语言模型骨干**则赋予了系统语义推理与任务泛化的能力。这一设计使模型在BEATv2协同语音手势生成基准上显著超越现有最佳方法（包括EMAGE, Liu et al., CVPR 2024），并在数据稀缺和涌现任务上展现出传统方法无法比拟的鲁棒性。



本文提出一种基于语言模型的多模态运动理解与生成框架，其核心思想是将3D人体运动视为一种“语言”，与语音和文本共享统一的多模态词汇表。框架整体遵循“分词—对齐—指令”三阶段流水线，如 Figure 2 所示。

![[assets/figures/papers/paper_list_l1867_The_Languate_of_Motion_Unifying_Verbal_and_Non_verbal_Language_of_3D_Hum/figures/002_Figure_2.jpg]]
*Figure 2: Method overview. We employ modality-specific tokenizers to process various input modalities. Specifically, we train a compositional body motion VQ-VAE to tokenize face, hands, upper body, and lower body motions into discrete tokens, combining these modalityspecific vocabularies(audio and text) into a unified multimodal vocabulary. During training, mixed tokens from different modalities are used as input, and the output is generated through an encoder-decoder language model. The mixed tokens are fed into the transformer encoder, while the decoder predicts the probability distribution of the next token in an autoregressive manner at each step*

**输入输出流**：系统接收音频、运动或文本中的任意模态组合作为输入，经模态专属分词器处理后，统一送入编码器-解码器语言模型，自回归地预测目标模态令牌序列。

**流水线模块关系**：

1. **组合式身体运动 VQ-VAE 分词器**：将 SMPL‑X 人体运动按语义功能拆解为四个独立部件——面部、手部、上身、下身，分别训练独立的 VQ‑VAE 将连续运动特征量化为离散令牌。这一组合式分词策略是模型捕捉身体语言与细微表情手势的关键设计。

2. **语音与文本分词器**：语音经 HuBERT 处理为 50 Hz 的离散音频令牌；文本采用 SentencePiece 切分为 32k 词汇量的 WordPiece 子词，继承自 T5 语言模型。

3. **多模态词汇表合并**：将文本、音频及四个运动部件的令牌空间合并为统一的多模态词汇表 $V = \{ V_t, V_a, V_f, V_h, V_u, V_l \}$，使语言模型能够以“文本”形式统一理解所有模态。

4. **编码器-解码器语言模型**：基于 220M 参数的预训练 Flan‑T5 Base，编码器处理输入混合令牌序列，解码器自回归预测目标令牌。训练损失为标准下一令牌交叉熵：
   $$\mathcal{L}_{LM} = - \sum_{k=0}^{L_t-1} \log p_{\theta}(s_t^k | s_t^{<k}, s_i)$$

5. **生成式预训练阶段**：在配对数据上执行两类跨模态对齐任务——组合式运动对齐（空间互译、时间补全）与音频-文本对齐，使模型建立多模态关联先验。

6. **指令精调阶段**：将下游任务（协同语音手势生成、运动到情绪预测等）编译为自然语言指令模板，在多任务数据上微调，使模型具备指令遵循能力。

**框架的关键创新**在于组合式运动分词与两阶段跨模态对齐预训练的结合：前者将复杂人体运动解耦为可组合的语义单元，后者赋予模型强运动先验，使其在数据稀缺时仍能保持竞争力（见 Figure 5）。

### 补充图表

![[assets/figures/papers/paper_list_l1867_The_Languate_of_Motion_Unifying_Verbal_and_Non_verbal_Language_of_3D_Hum/figures/001_Figure_1.jpg]]
*Figure 1: We introduce a language-model-based motion understanding and generation framework that takes in any of the audio/motion/text modalities and outputs the desired target modality. Coupled with our generative pre-training strategy, our model demonstrates competitive performance on an array of tasks, showing promising signs toward unified verbal and non-verbal language of human motions*



### 3.1 组合式身体运动 VQ-VAE 分词器

模型的核心创新之一在于将人体运动视为一种可组合的离散“语言”，为此设计了四个独立的 VQ-VAE 分词器，分别处理面部、手部、上身和下身运动。具体而言，基于 SMPL-X 身体模型（含 FLAME 面部模型），将身体划分为四个组合部分：下身 9 个关节、上身 13 个关节、手部 30 个关节，以及面部 1 个关节配合 100 维表情参数。每个部分独立训练一个 VQ-VAE，将连续姿态序列编码为离散令牌。

VQ-VAE 的量化过程将编码器输出的连续潜在特征 $\mathbf{z}^t$ 映射到码本 $Q$ 中欧氏距离最近的离散条目：

$$\mathbf{q}^t = \mathcal{Q}(\mathbf{z}^t) := \arg\min_{\mathbf{q}^k \in Q} \|\mathbf{z}^t - \mathbf{q}^k\|^2$$

训练 VQ-VAE 的总损失函数同时约束姿态重建质量与运动平滑性：

$$\mathcal{L}_{total} = \mathcal{L}_{rec}(\mathbf{g}, \hat{\mathbf{g}}) + \mathcal{L}_{vel}(\mathbf{g}', \hat{\mathbf{g}}') + \mathcal{L}_{acc}(\mathbf{g}'', \hat{\mathbf{g}}'') + \mathcal{L}_{mrec}(\mathbf{g}, \hat{\mathbf{g}}) + \mathcal{L}_{mvel}(\mathbf{g}', \hat{\mathbf{g}}') + \mathcal{L}_{macc}(\mathbf{g}'', \hat{\mathbf{g}}'') + \mathcal{L}_{comm}(\mathbf{g}, \mathbf{q})$$

其中 $\mathbf{g}$ 为真实姿态，$\hat{\mathbf{g}}$ 为重建姿态，$\mathbf{g}'$ 和 $\mathbf{g}''$ 分别表示速度和加速度。损失项依次对应：姿态重建、速度重建、加速度重建、网格重建、网格速度重建、网格加速度重建，以及码本承诺损失。这种组合式分词设计使得模型能够精细捕捉不同身体部位的运动模式，为后续跨模态对齐奠定基础。

### 3.2 多模态词汇表构建

在获得各模态的离散令牌后，模型构建统一的“多模态词汇表”。语音模态通过 HuBERT 将 16kHz 原始音频下采样 320 倍，得到频率 $s=50$ 的离散音频令牌 $\mathbf{a}$。文本模态使用 SentencePiece 进行 WordPiece 切分，继承自 T5 的 32,000 词规模的子词词汇表，产生文本令牌 $\mathbf{w}$。

最终，统一的多模态令牌空间 $M$ 由量化运动令牌、音频令牌、文本令牌以及控制令牌合并而成：

$$M := Q \cup A \cup W \cup C = \{ \mathbf{q}_f, \mathbf{q}_u, \mathbf{q}_h, \mathbf{q}_l, \mathbf{a}, \mathbf{w} \}$$

其中 $\mathbf{q}_f, \mathbf{q}_u, \mathbf{q}_h, \mathbf{q}_l$ 分别对应面部、上身、手部、下身的运动令牌。运动词汇表 $V_m = \{ v_f^i, v_h^i, v_u^i, v_l^i \}_{i=1}^{K_m}$ 是四个部位令牌集合的并集。这一设计使得所有输入模态均以“文本”令牌的形式呈现给语言模型，实现了多模态信号的统一表示。

### 3.3 编码器-解码器语言模型

模型主体采用预训练的 **Flan-T5 Base**（220M 参数）作为编码器-解码器 Transformer 架构。给定输入序列 $s_i$（包含来自不同模态的混合令牌），编码器负责理解上下文，解码器则以自回归方式逐令牌预测目标序列 $s_t$。训练损失为标准的下一个令牌预测交叉熵：

$$\mathcal{L}_{LM} = - \sum_{k=0}^{L_t-1} \log p_{\theta}(s_t^k | s_t^{<k}, s_i)$$

通过共享的多模态词汇表 $V$，模型无需额外的模态适配器即可处理任意模态的组合输入，并以统一的语言建模范式生成目标模态输出。这种架构选择充分利用了预训练语言模型已有的语义推理能力，为后续的跨模态生成与理解任务提供了强大的基础。

### 补充图表

![[assets/figures/papers/paper_list_l1867_The_Languate_of_Motion_Unifying_Verbal_and_Non_verbal_Language_of_3D_Hum/figures/003_Figure_3.jpg]]
*Figure 3: Illustration of pre-training. We pre-train our language model by translating one modality to another using paired data*



## 实验与关键发现

### 4.1 协同语音手势生成主结果

我们在BEATv2基准上评估协同语音手势生成任务，采用FGD（×10⁻¹，越低越好）、BC（×10⁻¹，越高越好）和Diversity三个指标，分别衡量运动真实感、语音-运动同步性和生成多样性。如**Table 1**所示，本方法取得FGD 5.301、BC 7.780、Diversity 15.167，在所有指标上显著超越现有最优方法**EMAGE**（Liu et al., CVPR 2024）及其他基线。

![[assets/figures/papers/paper_list_l1867_The_Languate_of_Motion_Unifying_Verbal_and_Non_verbal_Language_of_3D_Hum/figures/004_Table_1.jpg]]
*Table 1: Co-speech gesture generation results on BEATv2 benchmark. We report FGD*

定性对比（**Figure 4**）进一步印证了这一优势：给定相同的语音输入，EMAGE和**DiffuseStyleGesture**（Yang et al., IJCAI 2023，文中误写为SynTalker）生成的手势较为保守，而本方法在说话者强调特定词汇（如“tired”、“because”）时展现出更丰富、更具表现力的肢体动作。

![[assets/figures/papers/paper_list_l1867_The_Languate_of_Motion_Unifying_Verbal_and_Non_verbal_Language_of_3D_Hum/figures/006_Figure_4.jpg]]
*Figure 4: Qualitative example on co-speech gesture generation. Given a speech, we visualize the ground truth 3D motion accompanying the audio, the motion generated by the baseline EMAGE [43], SynTalker [8] and our method. Our model generates more diverse and expressive motion compared to the baseline, especially when the speaker emphasizes on certain words such as “tired” and “because”*

### 4.2 消融实验：预训练的关键作用

为验证预训练策略的必要性，我们设计了系统性的消融实验。

**语言模型预训练的贡献。** 将预训练Flan-T5 Base替换为随机初始化权重后，模型性能急剧下降：FGD从5.301升至7.470，BC从7.780降至6.148，Diversity从15.167降至14.162（**Table 1**，Ours w/o language pre-training）。这表明预训练语言模型提供的语义理解能力是高质量手势生成的基础。

**多模态预训练的贡献。** 移除整个多模态预训练阶段同样导致性能退化：FGD升至5.408，BC降至7.742（**Table 1**，Ours w/o multimodal pre-training）。进一步地，我们逐一消融预训练中的对齐组件（**Table 2**）：
- 去除空间对齐（跨身体部件的互译任务）：FGD升至6.336；
- 去除时间对齐（运动序列补全任务）：FGD升至6.800；
- 去除所有运动预训练（仅保留音频-文本对齐）：FGD升至7.776。

完整模型的FGD（5.301）远优于上述任一消融变体，证明组合式运动对齐与音频-文本对齐在预训练中协同贡献。

### 4.3 数据效率分析

预训练赋予模型强运动先验，使其在数据稀缺场景下具有显著优势。**Figure 5**展示了生成性能随后训练数据量的变化曲线：当训练数据从100%逐步缩减至1%时，完整模型始终优于“无预训练”消融变体和EMAGE。这一结果表明，生成式预训练策略有效降低了对大规模配对标注数据的依赖。

![[assets/figures/papers/paper_list_l1867_The_Languate_of_Motion_Unifying_Verbal_and_Non_verbal_Language_of_3D_Hum/figures/007_Figure_5.jpg]]
*Figure 5: Generation performance vs. the amount of post-training data. Our model learns a stronger motion prior from pre-training and thus shows much better under data scarcity*

### 4.4 运动到情绪的零样本迁移

预训练后的指令精调使模型解锁了训练期间未见的新任务。我们测试了“给定运动序列，预测说话者情绪”的能力，结果如**Table 3**所示：本方法取得Rouge Cider 26.67、BertScore 16.94，而通用文本-运动模型**MotionGPT**（Zhang et al., AAAI 2024）仅获得10.67和2.31，几乎与随机基线（4.44, 0.19）持平。**Figure 7**的定性示例展示了模型从手势中准确推断情绪的典型场景。这一跨任务泛化能力源于预训练阶段建立的多模态语义对齐。

![[assets/figures/papers/paper_list_l1867_The_Languate_of_Motion_Unifying_Verbal_and_Non_verbal_Language_of_3D_Hum/figures/010_Table_3.jpg]]
*Table 3: Motion to emotion. We prompt our model to predict emotion given a motion sequence*

![[assets/figures/papers/paper_list_l1867_The_Languate_of_Motion_Unifying_Verbal_and_Non_verbal_Language_of_3D_Hum/figures/009_Figure_7.jpg]]
*Figure 7: Qualitative example of emotion prediction*

### 4.5 失败模式与局限性

尽管整体性能优异，模型仍存在以下已知失败模式：

1. **运动连贯性问题。** 离散VQ-VAE分词引入的量化噪声可能导致偶尔生成不连贯的运动序列。这是离散化表示的固有局限，引入连续潜变量分词是重要的改进方向。
2. **可编辑手势生成的量化缺失。** 如**Figure 6**所示，模型可根据文本+音频提示生成兼具表达性手势与通用肢体动作的运动，但目前仅展示了定性结果，缺乏系统的量化评估指标。
3. **分布外泛化风险。** 训练数据主要来自BEATv2等数据集，覆盖的说话人风格、语言和文化背景有限，模型在分布外手势和情绪上的表现仍需进一步验证。

![[assets/figures/papers/paper_list_l1867_The_Languate_of_Motion_Unifying_Verbal_and_Non_verbal_Language_of_3D_Hum/figures/008_Figure_6.jpg]]
*Figure 6: Editable gesture generation. We prompt the language with text and audio information and it outputs motions that are both expressional gesture motion as well as general movement motion*

### 补充图表

![[assets/figures/papers/paper_list_l1867_The_Languate_of_Motion_Unifying_Verbal_and_Non_verbal_Language_of_3D_Hum/figures/005_Table_2.jpg]]
*Table 2: Ablations of pre-training*



## 定位与知识库关联

### 1. 与现有工作的关系

本文提出了一种**多模态语言模型**框架，将人体运动视为一种“语言”，与语音和文本共享统一的多模态词汇表。该方法在谱系上处于三类工作的交汇点：

**（1）协同语音手势生成**
现有最优方法**EMAGE**（Liu et al., CVPR 2024）和**DiffuseStyleGesture**（Yang et al., IJCAI 2023）均为特定任务设计的生成模型，仅能处理语音到手势的单一映射。本文的突破在于：通过组合式四部分运动分词（面部、手部、上身、下身独立VQ-VAE）和跨模态预训练，模型不仅显著超越这些专用基线（Table 1，FGD 5.301 vs EMAGE），还解锁了文本-运动生成、运动到情绪预测等新任务——这是单一模态基线无法实现的。

**（2）通用运动生成语言模型**
**MotionGPT**（Zhang et al., AAAI 2024）首次尝试将运动视为语言进行统一建模，但其运动分词采用单一整体VQ-VAE，且缺乏针对语音模态的设计。本文的关键改进在于：组合式身体部位分词捕获了手势的细粒度表达（如面部微表情与手部动作的独立建模），并引入音频令牌（HuBERT）使语音成为原生输入模态。在运动到情绪预测任务上，本文模型（Rouge 26.67, BertScore 16.94）远超MotionGPT（Rouge 10.67, BertScore 2.31），后者几乎与随机基线持平（Table 3），验证了组合式分词和跨模态对齐对语义理解的增益。

**（3）预训练语言模型的多模态扩展**
本文继承Flan-T5 Base（220M参数，编码器-解码器Transformer）的语义先验，通过“生成式预训练 + 指令精调”两阶段策略实现跨模态对齐。预训练阶段包含两类对齐任务：**组合式运动对齐**（空间互译：不同身体部位间相互生成；时间补全：从部分帧预测完整序列）和**音频-文本对齐**（语音与文本互译）。消融实验（Table 2）表明，移除空间对齐（FGD 6.336）和时间对齐（FGD 6.800）均导致性能显著下降，移除所有运动预训练后FGD升至7.776，接近无语言预训练的随机权重基线（FGD 7.470），证明运动先验和语言先验同等关键。

### 2. 适用边界

**（1）数据依赖与泛化边界**
模型在BEATv2基准上表现优异，但该数据集覆盖的说话人风格、语言和文化背景有限。在分布外手势（如非英语母语者的协同语音模式）和情绪表达上的泛化能力仍待验证。数据效率分析（Figure 5）显示，预训练赋予的强运动先验使模型在数据极度稀缺时始终优于无预训练消融方案和EMAGE，但曲线趋势表明，当精调数据量极低时，绝对性能仍有明显下降。

**（2）模态冲突与歧义处理**
当音频与文本提示存在冲突时（如语音表达愤怒但文本描述平静），模型如何决策手势的最终表达，论文未给出系统研究。可编辑手势生成目前仅展示了定性示例（Figure 6），缺乏量化评估，其可控性和一致性边界尚不明确。

**（3）运动质量瓶颈**
离散VQ-VAE分词引入的量化噪声可能导致运动序列不连贯，这是模型偶尔生成不自然手势的根本原因。该问题在需要高精度手指动作或快速面部表情变化的场景中可能被放大。

### 3. 局限与开放问题

**局限1：量化噪声与运动连贯性**
离散运动分词是当前架构的核心，但也是运动质量的主要瓶颈。论文明确指出“引入连续分词是提升运动质量的重要未来方向”。一个可能的路径是采用扩散潜变量替代离散VQ-VAE，在保持语言模型自回归架构的同时消除量化误差。

**局限2：可编辑手势生成的评估缺失**
尽管Figure 6展示了令人鼓舞的定性结果，但缺乏系统的量化指标（如编辑保真度、风格一致性）使得该能力的实际边界无法评估。设计合适的自动化指标是该方向的关键开放问题。

**局限3：训练数据多样性不足**
现有数据在说话人身份、语言和文化背景上的覆盖有限，可能影响模型在多样化场景下的公平性和鲁棒性。

**开放问题1：模型规模扩展的收益边界**
当前使用Flan-T5 Base（220M），扩展至更大语言模型（如T5-Large、LLaMA）能否在不损失推理效率的前提下进一步提升对复杂语义的建模能力？预训练阶段的计算成本与性能收益的帕累托前沿尚待探索。

**开放问题2：模态冲突的决策机制**
当多模态输入信号不一致时，模型内部的注意力机制如何加权不同模态？是否可以通过显式的置信度校准或门控机制提升可控性？这是实现稳健多模态交互的核心问题。

**开放问题3：连续令牌与语言模型的融合范式**
若采用连续潜变量（如VAE或扩散模型的潜在表示）替代离散令牌，如何设计训练目标以保持语言模型的语义推理能力？这涉及表示学习与序列建模两个领域的方法论融合。

**开放问题4：运动“语言”的语法结构**
本文将运动视为语言，但未显式建模运动的“语法”（如手势的过渡规则、身体部位间的协调约束）。探索运动序列的层次化语法结构是否能进一步提升生成质量和可控性，是一个值得深入的方向。



## 原文 PDF

![[paperPDFs/CVPR_2025/The_Languate_of_Motion_Unifying_Verbal_and_Non_verbal_Language_of_3D_Human_Motion.pdf]]
