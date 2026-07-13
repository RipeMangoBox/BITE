---
title: Multi-Modal Motion Retrieval by Learning a Fine-Grained Joint Embedding Space
type: paper
paper_level: A
venue: TMM
year: 2026
pdf_ref: paperPDFs/TMM_2026/Multi-Modal_Motion_Retrieval_by_Learning_a_Fine-Grained_Joint_Embedding_Space.pdf
project_link: null
code_link: null
aliases:
- MMFGJEF
- MMMRBLFGJES
tags:
- TMM_2026
- topic/motion_animation
- topic/motion_animation/human_motion_generation
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
- topic/representation_self_supervised_transfer
core_operator: 通过引入音频模态并设计基于记忆检索的音频特征压缩模块，同时用最大化 token 相似度的序列级对齐替代全局对齐，迫使模型关注跨模态局部关键信息。
primary_logic: 将人体姿态分解为独立身体部件，并与文本、音频、视频的序列级 token 进行细粒度对齐，可以精确捕捉“转身”等动作短语与对应运动帧的语义对应，从而大幅提升多模态运动检索精度。
claims:
- 在 HumanML3D 上，文本到运动检索的 R@10 指标从 33.67 提升至 43.83，相对提升 10.16%。
- 在 HumanML3D 上，视频到运动检索的 R@1 指标相对提升 25.43%。
- HumanML3D 上 Text-to-Motion R@10 = 43.83
- HumanML3D 上 Motion-to-Text R@10 = 43.74
---

# Multi-Modal Motion Retrieval by Learning a Fine-Grained Joint Embedding Space

> [!tip] 核心洞察
> 将人体姿态分解为独立身体部件，并与文本、音频、视频的序列级 token 进行细粒度对齐，可以精确捕捉“转身”等动作短语与对应运动帧的语义对应，从而大幅提升多模态运动检索精度。

| 字段 | 内容 |
|------|------|
| 中文题名 | 基于细粒度联合嵌入空间的多模态运动检索 |
| 英文题名 | Multi-Modal Motion Retrieval by Learning a Fine-Grained Joint Embedding Space |
| 会议/期刊 | TMM 2026 |
| Links | [paper](https://arxiv.org/abs/2507.23188) |
| Topic | #topic/motion_animation #topic/motion_animation/human_motion_generation #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction #topic/representation_self_supervised_transfer |
| Method | Multi-Modal Fine-Grained Joint Embedding Framework |
| Dataset | HumanML3D, KIT-ML |

> [!tip] 效果简介
> - HumanML3D 上，Text-to-Motion R@10 43.83 vs 33.67 (LAVIMO) (+10.16)；Motion-to-Text R@10 43.74 vs 36.55 (LAVIMO) (+7.19)；Video-to-Motion R@1 SOTA (Ours) vs LAVIMO (+25.43% (relative))。
> - KIT-ML 上，Video-to-Motion R@1 65.40 vs Prior best (LAVIMO) (Superior)。

## 概要

现有运动检索（Motion Retrieval）方案主要依赖文本和视频作为查询模态，缺少音频这一直观、自然的交互通道。更关键的是，主流方法采用**全局对比学习**，将整个运动序列或文本压缩为单一特征向量进行跨模态匹配——这一操作会丢失描述中关键动作词与运动片段之间的**细粒度对应关系**，例如“转身”这类短语与具体帧的语义对齐。

本文提出**多模态细粒度联合嵌入框架**（Multi-Modal Fine-Grained Joint Embedding Framework），在以下三个维度上对现有范式进行重构：

1. **模态扩展**：首次将音频引入多模态运动检索，与文本、视频、运动共同构成四模态联合空间。音频特征通过 WavLM 提取后，经可学习记忆注意力模块（Memory-Retrieval Attention）压缩为固定长度 token 序列，解决了语音信号长度剧烈波动的问题。
2. **对齐粒度切换**：从全局向量对齐转向**序列级细粒度对齐**——计算各模态 token 序列间的加权最大相似度，迫使模型捕捉局部语义对应，而非依赖粗粒度的整体表征。
3. **运动表示分解**：将人体姿态拆分为头部、躯干、四肢等 8 个身体部件独立编码，使运动 token 序列天然携带空间结构信息，为细粒度对齐提供更丰富的匹配单元。

在 HumanML3D 基准上，该方法取得了显著提升：文本到运动检索的 R@10 从 33.67（LAVIMO, Yin et al., CVPR 2024）提升至 43.83，**绝对提升 10.16 个百分点**；视频到运动检索的 R@1 相对提升达 25.43%。消融实验进一步证实，移除身体部件分解后 R@1 从 9.41 降至 7.77，而完全移除对齐损失则导致检索性能崩溃（R@1 降至 0.00），验证了细粒度对齐与结构化运动表示的核心贡献。

该方法也存在明确局限：受限于 196 帧的最大运动长度，超长动作描述可能检索失败；训练依赖合成语音数据，对真实声学环境的泛化性尚需更全面评估。



### 问题背景

运动检索旨在根据自然语言描述、视频演示或音频指令，从大规模运动数据库中快速定位最匹配的三维人体运动序列。这一任务在动画制作、游戏开发和人机交互等领域具有广泛的应用前景。近年来，基于对比学习的跨模态检索框架取得了显著进展，使得文本到运动、视频到运动的检索成为可能。

### 现有方法的瓶颈

当前主流的运动检索框架存在两个关键局限，制约了检索精度的进一步提升。

**模态覆盖不足。** 现有方法仅支持文本和视频两种查询模态，缺少音频这一直观、自然的交互通道。在语音控制的虚拟角色、语音驱动的动画编辑等场景中，用户更倾向于通过口语指令进行交互，而现有框架无法直接利用音频信号进行运动检索。基线方法 **TMR**（Petrovich et al., ICCV 2023）专注于文本到运动检索，**LAVIMO**（Yin et al., CVPR 2024）将模态扩展至文本、视频、运动三模态，但二者均未引入音频模态。

**对齐粒度粗糙。** 现有框架普遍采用全局对比学习策略，将整个运动序列和文本描述分别压缩为单一特征向量，再计算跨模态相似度。这种全局对齐方式丢失了描述中关键动作词与运动片段之间的细粒度对应关系。例如，描述“一个人先转身，然后蹲下捡起物品”中，“转身”和“蹲下”分别对应运动序列中不同的时间片段，全局对齐无法精确捕捉这种局部语义匹配。

### 本文动机

针对上述瓶颈，本文提出以下核心动机：

1. **引入音频模态，构建四模态联合嵌入空间。** 将音频作为与文本、视频并列的查询模态，使用户能够通过口语指令进行运动检索，拓展交互方式的多样性。

2. **设计细粒度序列级对齐机制，替代全局对齐。** 将人体姿态分解为独立身体部件（头部、躯干、四肢等），并与文本、音频、视频的序列级 token 进行逐 token 的最大相似度对齐。这一设计迫使模型关注跨模态的局部关键信息，精确捕捉“转身”等动作短语与对应运动帧的语义对应关系。

3. **通过运动重建任务强化跨模态语义一致性。** 在对比对齐之外，引入从多模态上下文重建被遮掩运动 token 的辅助任务，进一步提升嵌入空间的语义表达能力。



## 核心方法与创新机理

本工作针对现有多模态运动检索框架的两个结构性瓶颈，提出了三项关键创新，构成一个统一的细粒度联合嵌入检索框架。

**瓶颈一：模态覆盖不足。** 现有方法如 **LAVIMO**（Yin et al., CVPR 2024）仅支持文本、视频与运动三模态之间的检索，缺少音频这一人类最直观的交互通道。本工作首次将音频模态引入多模态运动检索，将框架扩展为文本-视频-音频-运动四模态对齐系统。

**瓶颈二：对齐粒度粗糙。** 主流方法采用全局对比学习，将整个序列压缩为单一特征向量后计算跨模态相似度。这种做法损失了描述中关键动作词（如“转身”“下蹲”）与对应运动帧之间的细粒度对应关系，导致检索精度受限。

针对上述瓶颈，本工作提出以下 changed slots：

| 创新维度   | 基线方案          | 本工作方案                      |
| ------ | ------------- | -------------------------- |
| 模态数量   | 文本、视频、运动（三模态） | 文本、视频、音频、运动（四模态）           |
| 对比对齐粒度 | 全局对齐（单一特征向量）  | 序列级细粒度对齐（token 间最大相似度）     |
| 运动表示方式 | 全身关节点整体表示     | 人体分解为头部、躯干、四肢等 8 个身体部件独立编码 |
| 音频编码策略 | 无音频输入         | WavLM 声学特征 + 可学习记忆键值对注意力压缩 |

**创新一：身体部件分解的运动编码。** 受人类通过分析不同身体部件的相对运动来识别动作这一认知启发，运动编码器将人体姿态分解为 8 个独立身体部件，通过时空 Transformer 分别编码为运动 token 序列。这一设计使得模型能够精确捕捉局部动作（如“挥手”仅涉及手臂）与文本/音频中对应短语的语义关联，而非被全身运动信息淹没。

**创新二：基于记忆检索的音频特征压缩。** 音频经 WavLM 提取声学特征后长度差异极大（Fig. 4），无法直接输入统一框架。本工作设计了一个可学习的记忆注意力模块：以固定数量的可学习记忆向量作为键值对，以输入音频特征生成的查询向量进行注意力检索，将变长音频序列压缩为固定长度 token 序列。消融实验（Tab. VII）表明，该方案在音频到运动检索中大幅优于平均池化、卷积等替代方案（R@1: 16.19 vs 9.33 AvgPool-4）。

**创新三：序列级细粒度对比对齐。** 核心对齐策略从全局相似度转向 token 级别的最大相似度匹配——对每个模态的每个 token，在另一模态的所有 token 中寻找最相似者，加权求和得到序列间相似度。该策略迫使模型关注跨模态局部关键信息的对应关系，公式表达为：

$$h(\mathbf{e}_x, \mathbf{e}_y) = \frac{1}{2} \sum_{i=1}^{L_x} {\mathbf{w}_x^i \max_{j=1}^{L_y} \langle \mathbf{e}_x^i, \mathbf{e}_y^j \rangle} + \frac{1}{2} \sum_{j=1}^{L_y} {\mathbf{w}_y^j \max_{i=1}^{L_x} \langle \mathbf{e}_y^j, \mathbf{e}_x^i \rangle}$$

四模态间六对对齐损失之和构成总对齐损失，并与运动重建损失加权组合为最终训练目标。消融实验（Tab. V）表明，完全移除对齐损失导致检索性能崩溃（R@1 降至 0.00）；序列级对齐显著优于全局对齐，且基于最大相似度的策略优于均值策略（Tab. VIII）。

这三项创新协同作用：身体部件分解为细粒度对齐提供了空间维度的精细表征，记忆检索压缩为音频模态提供了统一的时序接口，序列级对齐则在 token 层面建立了跨模态的精确语义桥梁。在 HumanML3D 上，文本到运动检索的 R@10 从 33.67（LAVIMO）提升至 43.83，相对提升 10.16%；视频到运动检索的 R@1 相对提升 25.43%。



本文提出一个**多模态细粒度联合嵌入框架**，首次将文本、视频、音频与运动四类模态对齐到同一嵌入空间，支持文本-运动、视频-运动、音频-运动等多种检索任务。框架的核心设计思路是：**将人体运动分解为独立身体部件进行编码，并在序列级（token-level）而非全局级（global-level）进行跨模态对比对齐**，从而保留“转身”“挥手”等关键动作短语与对应运动帧之间的细粒度语义对应。

### 输入输出流

框架接受三种查询模态中的任意一种——文本描述、视频片段或语音指令——输出与查询语义最匹配的运动序列。具体流程如下（参见 Fig. 3）：

![[assets/figures/papers/paper_list_l6_https_arxiv_org_abs_2507_23188/figures/003_Figure_3.jpg]]
*Figure 3: Pipeline of Our Work. The text, audio, and video inputs are encoded using pre-trained models to extract feature tokens. Meanwhile, the motion encoder segments human motion by body parts and processes them through a transformer, effectively integrating both body part and temporal information. This design ensures that the alignment process captures both spatial and temporal dependencies. Once inputs from different modalities are encoded, a fine-grained contrastive loss is applied to align them within a joint embedding space. Specifically, for a given token in modality 1 with shape*

1. **运动编码**：将人体姿态按身体部件（头部、躯干、四肢等共 8 个部件）分解，经时空 Transformer 编码为运动 token 序列 $\mathbf{e}_m$。
2. **文本编码**：使用 DistilBERT 提取词 token，再经额外 Transformer 层编码为文本 token 序列 $\mathbf{e}_t$（Eq. 1）。
3. **视频编码**：使用 CLIP 图像编码器逐帧提取特征，再经时序 Transformer 编码为视频 token 序列 $\mathbf{e}_v$（Eq. 2）。
4. **音频编码**：使用 WavLM 提取原始声学特征，再通过基于可学习记忆键值对的注意力模块压缩为固定长度 token 序列 $\mathbf{e}_a$（Eq. 3），解决音频特征长度差异大的问题（Fig. 4, Fig. 5）。
5. **细粒度对齐**：计算四模态所有 token 间的最大相似度 $h(\mathbf{e}_x, \mathbf{e}_y)$（Eq. 8），并以双向 KL 散度损失进行对比学习，总对齐损失为六对模态组合之和（Eq. 4）。
6. **运动重建辅助任务**：随机遮掩部分运动 token，利用其他模态的 token 通过 Transformer 重建被遮掩的运动信息，增强跨模态语义一致性（Eq. 10–11）。

最终训练损失为对齐损失与重建损失的加权组合（Eq. 12）。

### 核心设计决策

| 设计维度 | 基线做法 | 本文做法 |
|---------|---------|---------|
| 模态数量 | 文本、视频、运动（三模态） | 新增音频，构成四模态 |
| 对齐粒度 | 全局对齐（单一特征向量） | 序列级细粒度对齐（token 间最大相似度） |
| 运动表示 | 全身关节点整体编码 | 身体部件独立编码后融合 |
| 音频处理 | 无 | WavLM + 记忆检索注意力压缩 |

与 **TMR**（Petrovich et al., ICCV 2023）和 **LAVIMO**（Yin et al., CVPR 2024）等基线相比，本文框架的增量在于：(1) 引入音频作为第三查询模态；(2) 用序列级对齐替代全局对齐，使模型能够关注描述中的关键动作词与运动片段之间的局部对应关系（Fig. 2 对比了两种对齐策略的差异）。

> **注意**：音频模态的训练数据通过 ChatGPT 改写文本为口语风格、Tortoise 多说话人 TTS 合成构建（Fig. 6, Tab. I），初步验证了对真实语音的泛化能力（Fig. 10–11），但真实声学环境下的鲁棒性仍需更全面评估。

![[assets/figures/papers/paper_list_l6_https_arxiv_org_abs_2507_23188/figures/006_Figure_6.jpg]]
*Figure 6: Dataset Augmentation with Audio Modality. The text data from the KIT-ML [9] and HumanML3D [10] datasets are processed using the text-tospeech model Tortoise [26] to generate audio signals with randomly assigned speaker identities, forming Original Dataset. Additionally, we use ChatGPT-3.5 [24] to rewrite these texts into a more conversational, spoken style. The rewritten texts are then converted into audio signals, resulting in Oral Dataset*

### 补充图表

![[assets/figures/papers/paper_list_l6_https_arxiv_org_abs_2507_23188/figures/001_Figure_1.jpg]]
*Figure 1: Overview of Our Work. Our framework encodes text, video, or audio descriptions and computes their similarity within a shared joint embedding space, ranking candidate motions based on similarity scores to retrieve the most relevant motion*



### 身体部件运动编码器

该模块的核心设计动机在于：人类识别运动时并非将身体视为一个整体，而是通过分析不同身体部件的相对运动来理解动作语义。基于这一认知假设，运动编码器将人体姿态显式分解为 **8 个独立身体部件**（头部、躯干、四肢等），对每个部件分别提取空间特征，再通过时空 Transformer 整合部件间的时序关系，最终输出运动 token 序列。

这种部件级分解策略使得模型能够捕捉到如“转身时躯干旋转而手臂保持不动”这类细粒度的空间-时序对应关系，为后续与文本、音频等模态的 token 级对齐提供了结构化的运动表示。

### 文本编码器

文本序列首先经过预训练的 **DistilBERT** 提取词级 token，随后送入多层 Transformer 编码器，保留完整的 token 序列而非压缩为单一向量。公式如下：

$$\mathbf{e}_t = \mathrm{Transformer}\big(\mathrm{DistilBERT}(\{w_1, w_2, \dots, w_{L_t}\})\big)$$

其中 $\{w_1, w_2, \dots, w_{L_t}\}$ 为输入词序列，$\mathbf{e}_t \in \mathbb{R}^{L_t \times C}$ 为输出的文本 token 序列，$L_t$ 为序列长度，$C$ 为特征维度。

### 视频编码器

视频帧首先通过 **CLIP 图像编码器**逐帧提取空间特征，再经时序 Transformer 建模帧间依赖，输出视频 token 序列：

$$\mathbf{e}_v = \mathrm{Transformer}\bigl(\mathrm{CLIP}(I_1, I_2, \dots, I_{L_v})\bigr)$$

其中 $\{I_1, I_2, \dots, I_{L_v}\}$ 为视频帧序列，$\mathbf{e}_v \in \mathbb{R}^{L_v \times C}$ 为视频 token 序列。

### 音频编码器与记忆检索压缩模块

音频模态的引入面临一个关键挑战：WavLM 提取的原始音频特征长度高度可变（如 Fig. 4 所示，分布范围极广），无法直接输入固定长度的 Transformer。为解决此问题，本文设计了基于**可学习记忆键值对**的注意力压缩模块。

具体而言，首先使用预训练 **WavLM** 的最终层输出作为向量化音频表示；随后定义一组可学习的记忆 token $K_m, V_m \in \mathbb{R}^{L_m \times C}$，以输入音频特征生成的查询向量 $Q_z$ 对其进行注意力检索：

$$\mathrm{Attention}(Q_z, K_m, V_m) = \mathrm{softmax}\left(\frac{Q_z K_m^\top}{\sqrt{C}}\right) V_m$$

该机制将任意长度的音频特征压缩为固定长度 $L_m$ 的 token 序列，实现了变长输入的标准化处理。消融实验（Tab. VII）表明，该记忆检索策略在音频到运动检索中大幅优于平均池化（R@1: 16.19 vs 9.33）和卷积等替代方案。

### 细粒度序列级对比对齐

与现有方法将整个序列压缩为单一全局向量进行对比学习不同，本文提出的序列级对齐直接在 token 层面计算跨模态相似度。其核心操作是**加权最大相似度函数** $h(\mathbf{e}_x, \mathbf{e}_y)$：

$$h(\mathbf{e}_x, \mathbf{e}_y) = \frac{1}{2} \sum_{i=1}^{L_x} {\mathbf{w}_x^i \max_{j=1}^{L_y} \langle \mathbf{e}_x^i, \mathbf{e}_y^j \rangle} + \frac{1}{2} \sum_{j=1}^{L_y} {\mathbf{w}_y^j \max_{i=1}^{L_x} \langle \mathbf{e}_y^j, \mathbf{e}_x^i \rangle}$$

其中 $\mathbf{e}_x^i$ 为模态 $x$ 的第 $i$ 个 token，$\mathbf{w}_x^i$ 为对应的注意力权重，$\langle\cdot,\cdot\rangle$ 表示余弦相似度。该函数分别从两个方向计算每个 token 与另一模态中最相似 token 的匹配得分，并加权求和，确保双向对齐的对称性。

基于此相似度函数，四模态之间六对对齐损失的总和构成总对齐损失：

$$L_{\mathrm{align}} = L_{\mathrm{align}}^{mt} + L_{\mathrm{align}}^{mv} + L_{\mathrm{align}}^{ma} + L_{\mathrm{align}}^{tv} + L_{\mathrm{align}}^{ta} + L_{\mathrm{align}}^{va}$$

其中上标 $m, t, v, a$ 分别代表运动、文本、视频、音频模态。每对损失使用双向 KL 散度形式，推动匹配对的相似度最大化、非匹配对的相似度最小化。

消融实验（Tab. VIII）证实，基于最大相似度的序列级对齐策略显著优于全局对齐和均值相似度策略，额外引入全局特征仅带来微小增益，表明细粒度的 token 级对应是性能提升的关键驱动力。

### 运动重建辅助任务

为进一步强化跨模态 token 间的语义关联，模型引入运动重建辅助任务：随机遮掩部分运动 token，利用其他模态的 token 通过 Transformer 重建被遮掩的运动信息。最终训练损失为对齐损失与重建损失的加权组合：

$$L = L_{\mathrm{align}} + \lambda_{\mathrm{recon}} \cdot L_{\mathrm{recon}}$$

其中 $\lambda_{\mathrm{recon}}$ 为重建损失的权重系数。该辅助任务迫使模型学习从文本/音频/视频 token 中推断运动细节的能力，间接增强了联合嵌入空间的语义一致性。

### 补充图表

![[assets/figures/papers/paper_list_l6_https_arxiv_org_abs_2507_23188/figures/002_Figure_2.jpg]]
*Figure 2: Global contrastive learning (Left) computes similarity between two modalities using global representations, where motion and text data are compressed into a single token for cross-modal alignment. In contrast, sequence-level contrastive learning (Right) aligns individual tokens with their most relevant counterparts, enabling the model to focus on key frames in the motion sequence and important keywords in the text description (highlighted in yellow and red, respectively). As illustrated by the example, the phrase “turns around” yields higher similarity scores with the corresponding frames in the motion sequence, thereby enabling more accurate alignment between the text and motion pair*




## 实验与关键发现

### 核心性能瓶颈与因果机制

现有运动检索框架存在两个关键瓶颈：其一，仅支持文本与视频两种查询模态，缺少音频这一直观的交互通道；其二，采用全局对比学习将整个序列压缩为单一特征向量，导致描述中的关键动作词（如“转身”）与对应运动帧之间的细粒度语义对应关系被淹没。本工作通过两个因果调节变量解决上述问题：**引入音频模态**并设计基于记忆检索的音频特征压缩模块，同时将对比对齐的粒度从**全局向量提升至序列级 token**，迫使模型关注跨模态的局部关键信息。在此基础上，将人体姿态分解为独立身体部件进行编码，使得部件级运动特征能够与文本、音频、视频的 token 序列精确对齐，从而大幅提升多模态运动检索精度。

### 主实验结果

在 HumanML3D 数据集上，本文提出的四模态框架取得了全面的最优性能（Tab. II）。相较于三模态基线 **LAVIMO**（Yin et al., CVPR 2024），文本到运动检索的 **R@10 从 33.67 提升至 43.83，绝对提升 10.16 个百分点**；运动到文本检索的 R@10 从 36.55 提升至 43.74，提升 7.19 个百分点。视频到运动检索的 **R@1 相对提升 25.43%**，这一增益在摘要中被突出强调。在 KIT-ML 数据集上（Tab. III），三模态版本已持续优于先前方法，视频到运动 R@1 达到 65.40；四模态版本进一步带来更显著的提升。

值得注意的是，在口语化数据集（Oral Dataset）上的评估（Tab. IV）揭示了原始书面语描述与自然口语之间的风格差异：当模型仅在原始数据集上训练、却在口语数据集上测试时，性能出现明显下降。本文通过 ChatGPT 改写与多说话人 Tortoise TTS 合成的数据增强策略有效弥合了这一分布偏移，确保了音频模态在实际口语查询场景中的可用性。

### 消融研究：关键设计的贡献

**序列级对齐与身体部件分解**（Tab. V）：移除身体部件分解后，文本到运动检索的 R@1 从 9.41 降至 7.77，表明将人体分解为头部、躯干、四肢等独立部件进行编码是细粒度对齐的基础。完全移除对齐损失则导致检索性能崩溃（R@1 降至 0.00），验证了对比学习在构建联合嵌入空间中的不可替代性。

**序列长度的影响**（Tab. VI）：将序列长度从 1 逐步增加至 32 tokens，检索性能持续提升。这一趋势表明更丰富的时序语义信息有助于跨模态 token 级对齐，但也暗示当前固定帧数（196 帧 @20 FPS）可能成为处理超长动作描述的瓶颈。

**音频压缩策略**（Tab. VII）：基于记忆检索的注意力压缩模块在音频到运动检索中显著优于平均池化、卷积等替代方案（R@1: 16.19 vs AvgPool-4 的 9.33）。该模块通过可学习的记忆键值对将变长 WavLM 声学特征压缩为固定长度 token 序列，有效保留了语音中的动作语义信息。

**相似度策略对比**（Tab. VIII）：序列级对齐显著优于全局对齐，且基于最大相似度（max similarity）的策略优于无偏均值策略。额外引入全局特征仅带来微小增益，表明细粒度 token 级对齐已经捕获了绝大部分判别性信息。

### 定性分析与泛化验证

定性对比（Fig. 8）展示了文本与音频两种查询模态在相同语义下的检索结果，二者表现相当，验证了音频信号作为运动检索替代查询通道的有效性。真实音频泛化实验（Fig. 10、Fig. 11）进一步表明，尽管模型仅在合成音频上训练，其对未见说话人的真实语音甚至含噪环境下的音频仍具有一定的鲁棒性——但该结论目前仅基于少量受试者的初步验证，**需要更大规模的真实语音评估来确认泛化边界**。

![[assets/figures/papers/paper_list_l6_https_arxiv_org_abs_2507_23188/figures/009_Figure_8.jpg]]
*Figure 8: Qualitative Comparison of Motion Retrieval Using Text or Audio. The textual descriptions and audio instructions convey the same meanings. Our approach achieves comparable performance with either modality, highlighting the effectiveness of audio signals as a semantic representation equivalent to text*

![[assets/figures/papers/paper_list_l6_https_arxiv_org_abs_2507_23188/figures/015_Figure_10.jpg]]
*Figure 10: Motion Retrieval Using Real Audio Signals. We collect real audio recordings from two different subjects, each speaking the same content, and use them for motion retrieval. The results demonstrate that our model, trained on synthetic audio, effectively generalizes to real audio signals, showcasing its robustness in audio-driven motion retrieval*

![[assets/figures/papers/paper_list_l6_https_arxiv_org_abs_2507_23188/figures/018_Figure_11.jpg]]
*Figure 11: Real-world audio- to-motion retrieval results. Our model, trained on synthetic audio, generalizes well to some real-world and noisy audios from unseen speakers, showing robust retrieval performance across varied real-world conditions*

### 失败模式与局限性

失败案例分析（Fig. 12）指出，当使用超长文本描述进行检索时，模型可能无法正确匹配。这主要受限于固定的最大运动帧数（196 帧），超出该长度的复杂行为描述被截断，导致关键动作信息丢失。当前解决方案依赖句子分割与拼接后处理，但尚未从模型架构层面根本解决长序列建模问题。此外，在较小规模的 KIT-ML 数据集上存在一定的过拟合风险，性能增益幅度不如大规模 HumanML3D 显著。四模态联合训练带来了额外的计算开销（HumanML3D 上需 4×A6000 GPU，训练约 24.2 小时），但推理阶段效率仍可接受。

![[assets/figures/papers/paper_list_l6_https_arxiv_org_abs_2507_23188/figures/019_Figure_12.jpg]]
*Figure 12: Failure Case Analysis. The retrieval fails when using a long text sequence for retrieval, likely due to the motion length limit set in our model. However, when we split the sentence into two shorter ones, the retrieved motions are correct, where post-processing can be applied to seamlessly stitch them together*

### 补充图表

![[assets/figures/papers/paper_list_l6_https_arxiv_org_abs_2507_23188/figures/008_Table.jpg]]
*Table: RETRIEVAL RESULTS ON HUMANML3D. OUR 4-MODAL VERSION OUTPERFORMS PERVIOUS METHODS AND OUR 3-MODAL VERSION, DEMONSTRATING THE EFFECTIVENESS OF OUR MULTI-MODAL FRAMEWORK WITH FINE-GRAINED ALIGNMENT. THE BEST RESULTS ARE IN BOLD. TABLE II*





## 定位与知识库关联

### 1. 关键基线及其差异

本工作直接对标两类多模态运动检索基线：

- **TMR**（Petrovich et al., ICCV 2023）：仅支持文本到运动的双模态检索，采用全局对比学习将运动序列压缩为单一特征向量。本文将其视为文本模态的基线参照，但在模态覆盖范围和对齐粒度上均形成代差。
- **LAVIMO**（Yin et al., CVPR 2024）：首个将文本、视频、运动三模态纳入统一检索框架的工作，但仍采用全局对齐策略，且未引入音频通道。本文在其基础上做了三个关键突破：（1）新增音频模态，将三模态扩展为四模态；（2）用序列级细粒度对齐替代全局对齐；（3）将运动表示从全身整体编码改为身体部件独立编码。

从方法演进角度看，本文位于“多模态运动理解”与“细粒度跨模态对齐”两条线的交汇点。在运动表示层面，身体部件分解的思想可追溯至人体姿态估计中的部件模型，但将其引入运动检索并与序列级对齐耦合，属于本文的原创设计；在音频引入层面，本文首次将语音指令作为运动检索的查询模态，填补了“文本/视频→运动”到“语音→运动”的模态空白。

### 2. 适用边界

根据已验证的实验设置和局限性分析，本方法的适用边界如下：

- **数据规模依赖**：在 HumanML3D（约 14,616 个运动序列）上取得了显著的性能增益（文本到运动 R@10 从 33.67 提升至 43.83），但在较小规模的 KIT-ML 数据集上增益幅度收窄，存在一定的过拟合风险。这意味着该方法更适合中大规模运动数据集。
- **运动时长限制**：模型固定最大运动帧数为 196 帧（@20 FPS，约 9.8 秒）。对于超长动作描述（如包含多个连续动作的复合指令），检索可能失败，需要句子分割与拼接等后处理策略。
- **音频泛化边界**：训练数据依赖 ChatGPT + Tortoise 合成的语音。虽然初步验证了对真实说话人的泛化能力（Fig. 10、Fig. 11），但真实声学环境下的口音、背景噪声、多说话人重叠等复杂场景仍需更全面的评估。当前证据仅覆盖受控的真实语音测试，尚未在完全开放域的真实音频基准上验证。
- **计算开销**：四模态训练在 HumanML3D 上需 4×A6000 GPU、约 24.2 小时，相比单模态或三模态方法增加了训练成本。但推理阶段效率较高，不影响实际部署。

### 3. 已知局限

来自已验证分析的局限清单：

1. **固定帧数瓶颈**：196 帧的运动长度上限导致模型无法处理超长动作序列，这是工程层面的硬约束，而非方法层面的理论缺陷。
2. **小数据集过拟合风险**：KIT-ML 上的性能增益不如 HumanML3D 明显，表明模型在数据稀缺场景下的鲁棒性有待提升。
3. **合成音频依赖**：训练完全依赖 TTS 合成的音频数据。尽管使用了多说话人（Tortoise 随机分配）和口语改写（ChatGPT 生成对话风格文本）来增加多样性，但合成语音与真实语音在韵律、停顿、情感表达等方面仍存在分布差异。
4. **缺少音频模态的独立基准**：由于现有运动检索数据集本身不含音频，本文的音频到运动检索性能无法与先前工作直接对比，仅能通过文本到运动检索的间接对比来论证音频模态的有效性。

### 4. 待解决的开放问题

基于已验证分析中识别的开放问题：

- **长序列扩展**：如何在保持细粒度对齐能力的前提下，突破固定帧数限制以支持更长运动序列？可能的路径包括层次化时序建模或基于关键帧的自适应采样。
- **音频模态深化**：当前仅引入语音指令，未来可探索音乐、环境音等更丰富的音频模态，以增强对场景上下文的理解。这需要构建相应的多模态音频-运动数据集。
- **多语言与大规模预训练**：在更大规模、多语言的口语运动数据集上训练，能否提升模型的通用性与跨语言泛化能力？当前的口语数据集仅覆盖英文。
- **任务迁移潜力**：该细粒度多模态对齐框架的核心设计（身体部件分解 + 序列级对齐）能否迁移至动作识别、运动生成或人机交互等其他运动理解任务？目前仅验证了检索任务的有效性。



## 原文 PDF

![[paperPDFs/TMM_2026/Multi-Modal_Motion_Retrieval_by_Learning_a_Fine-Grained_Joint_Embedding_Space.pdf]]
