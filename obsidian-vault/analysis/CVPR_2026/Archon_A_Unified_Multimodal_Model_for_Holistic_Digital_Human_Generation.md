---
title: "Archon: A Unified Multimodal Model for Holistic Digital Human Generation"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/Archon_A_Unified_Multimodal_Model_for_Holistic_Digital_Human_Generation.pdf
project_link: null
code_link: null
aliases:
- Archon
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/generative_models_diffusion
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: 通过设计模态特定的离散令牌器将七种模态统一到共享词汇表，并用原生自回归语言模型在72项同步任务上预训练学习联合分布；关键引入了记忆高效的语义视频重参数化（将视频分解为参考图像和语义标签序列，实现4倍令牌缩减），并辅以语义驱动的视频扩散解码器恢复高清细节；同时采用‘Thinking in Modality’推理策略，将模糊的跨模态任务分解为逐步生成中间模态（...
primary_logic: 将高维视频浓缩为保留结构动态的语义视频卡片，让语言模型进行高效的跨模态推理，再交由扩散模型上采样为真实视频；借助逐步‘思考’中间模态的生成链，有效缓解端到端跨模态生成中的不确定性和分布偏移。
claims:
- 语义视频重参数化实现4倍令牌缩减的同时保留细粒度动态
- 在CelebV-HQ上，语音驱动视频生成的FID达到6.818，FVD为93.81，Sync-C为5.210，全面超越基线
- 全模型通过引入3DMM和描述作为中间表示，在所有指标上超越基线，稳定了视频质量和音频同步
- 统一模型在所有指标上优于专科模型集成
---

# Archon: A Unified Multimodal Model for Holistic Digital Human Generation

> [!tip] 核心洞察
> 将高维视频浓缩为保留结构动态的语义视频卡片，让语言模型进行高效的跨模态推理，再交由扩散模型上采样为真实视频；借助逐步‘思考’中间模态的生成链，有效缓解端到端跨模态生成中的不确定性和分布偏移。

| 字段 | 内容 |
|------|------|
| 中文题名 | Archon：面向整体数字人生成的统一多模态模型 |
| 英文题名 | Archon: A Unified Multimodal Model for Holistic Digital Human Generation |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://openaccess.thecvf.com/content/CVPR2026/html/Bao_Archon_A_Unified_Multimodal_Model_for_Holistic_Digital_Human_Generation_CVPR_2026_paper.html) |
| Topic | #topic/vision_multimodal_applications #topic/generative_models_diffusion #topic/vision_multimodal_applications/image_and_video_generation |
| Method | Archon |
| Dataset | CelebV-HQ |

> [!tip] 效果简介
> - CelebV-HQ 上，FID 6.818 vs - (优于所有基线)；FVD 93.81 vs - (优于所有基线)；Sync-C 5.210 vs - (优于所有基线)。

## 概述

**Archon** 是一个面向整体数字人生成的统一多模态模型，其核心目标是解决现有数字人系统由多个专科模型拼凑所带来的跨模态分布不匹配、算力冗余和难以扩展等瓶颈。高保真谈话视频的令牌序列过长（5秒30fps视频约产生9K令牌），远超现有语言模型的上下文窗口，且跨模态任务（如语音到视频）存在固有的模糊性和大域间隙。

模型的核心洞察在于：将高维视频浓缩为保留结构动态的语义视频卡片，让语言模型进行高效的跨模态推理，再交由扩散模型上采样为真实视频；同时借助逐步“思考”中间模态的生成链，有效缓解端到端跨模态生成中的不确定性和分布偏移。

**方法定位**：Archon 通过设计模态特定的离散令牌器将描述、脚本、语音、动画、图像、语义视频等七种模态统一到共享词汇表，并用原生自回归语言模型在72项同步任务上预训练学习联合分布。关键创新包括：（1）记忆高效的语义视频重参数化，将视频分解为参考图像和语义标签序列，实现4倍令牌缩减；（2）语义驱动的视频扩散解码器恢复高清细节；（3）“Thinking in Modality”推理策略，将模糊的跨模态任务分解为逐步生成中间模态（如3DMM形状、表情、语义标签、描述）的思维链。

**主要结果**：在CelebV-HQ基准上，语音驱动视频生成的FID达到6.818，FVD为93.81，Sync-C为5.210，全面超越AniPortrait、Echomimic、Hallo3等基线。消融实验表明，引入3DMM和描述作为中间表示的完整思维链在所有指标上超越直接生成基线，且统一多任务模型的表现优于多个专科模型组成的集成系统，验证了共享表示与联合训练带来的正向迁移。

## 背景与动机

### 数字人系统的碎片化困境

数字人（Digital Human）生成旨在从文本、语音等控制信号中合成逼真的人类形象与行为，涵盖语音合成、面部动画、谈话视频生成等多个子任务。当前的主流范式是通过“专科模型集成”来应对不同模态的生成需求——例如，用独立的文本到语音模型、语音到面部动画模型、以及动画到视频渲染模型串联工作。这种拼凑式架构存在三个深层矛盾：

1. **跨模态分布不匹配**：各专科模型在独立数据集上训练，输入输出空间的统计特性相互割裂。当一个模型的输出直接作为下一个模型的输入时，累积的分布偏移会逐级放大，最终导致生成质量退化。
2. **冗余算力消耗**：多个模型各自维护独立的编码器、解码器和骨干网络，大量参数被重复用于相似的特征提取任务，推理时延和显存开销线性叠加。
3. **扩展性瓶颈**：每增加一种新模态或新任务，需要重新设计接口适配和调度逻辑，系统复杂度随模态数量呈组合式增长。

### 高保真视频生成的令牌困境

在统一建模的路径上，一个更根本的技术障碍来自视频模态本身。高保真谈话视频的时序密度极高——以5秒30fps的视频为例，经主流RGB令牌器编码后会产生约9000个离散令牌，远超现有语言模型的上下文窗口。直接对如此长的令牌序列进行自回归建模，不仅计算代价不可承受，更关键的是，连续视频信号在被强制离散化的过程中会丢失细粒度纹理和运动细节，导致生成画面出现模糊、伪影和身份漂移。

### 跨模态生成的固有模糊性

语音到视频、文本到动画等跨模态任务存在天然的“大域间隙”（large domain gap）和一对多映射问题。例如，同一段语音可以对应多种合理的面部表情和头部运动，端到端的直接生成缺乏对中间结构（如三维面部形状、语义布局）的显式约束，模型容易陷入模态坍塌或产生不自然的动态。现有方法通常依赖隐式的对抗训练或额外的同步损失来缓解这一问题，但缺乏系统性的结构化推理机制。

### 本文动机

针对上述瓶颈，Archon提出三个核心设计理念：

- **统一多模态语言模型**：将描述、脚本、语音、动画、图像、语义视频等七种模态通过模态特定令牌器统一到共享词汇表，由原生自回归语言模型在72项同步任务上联合预训练，学习全局联合分布，从根本上消除专科模型间的分布不匹配。
- **语义视频重参数化**：用保留结构动态的语义标签序列替代RGB视频令牌，实现4倍令牌压缩，同时将纹理细节的恢复交由下游扩散模型完成，解耦“结构推理”与“纹理生成”。
- **模态思维链推理**：引入“Thinking in Modality”策略，将模糊的跨模态生成分解为逐步生成3DMM形状、表情、语义标签、自然语言描述等中间模态的链式过程，以显式结构先验逐步细化生成结果，缓解端到端映射的不确定性。

## 核心创新

Archon 的核心创新围绕一个根本瓶颈展开：现有数字人系统多由针对单一模态的专科模型拼凑而成，跨模态协调时存在分布不匹配、冗余算力消耗和难以扩展等问题。具体而言，高保真谈话视频的令牌序列过长（5秒30fps视频产生约9K令牌），超过现有语言模型的上下文窗口；端到端直接生成视频时，连续信号的离散化会破坏生成质量；跨模态任务（如语音到视频）存在固有的模糊性和大域间隙。

针对上述瓶颈，Archon 通过以下四个关键 **changed slots** 实现了突破：

### 1. 视频表示与令牌化：从RGB视频到语义视频卡片

**基线方案**直接使用RGB视频令牌器，5秒视频产生约9K令牌，超出语言模型上下文窗口。

**Archon方案**引入记忆高效的语义视频重参数化：将RGB视频替换为由离散语义标签构成的语义视频，保留结构动态和关键运动信息，同时丢弃冗余纹理细节。具体地，对于长度为 $L$ 的语义视频，压缩后的令牌维度为：

$$\begin{array} { r } { ( \frac { L - 1 } { 4 } + 1 ) \times 8 \times 8 } \end{array}$$

这一设计实现了 **4倍令牌缩减**，同时保留了细粒度动态信息。语义视频令牌器与参考图像（保留外观信息）配合使用，将视频表示压缩至约8K上下文窗口内的可管理范围。

### 2. 跨模态生成策略：从端到端到“Thinking in Modality”

**基线方案**采用端到端直接生成目标模态（如语音→视频），忽略跨模态映射中的模糊性和大域间隙。

**Archon方案**提出 **“Thinking in Modality”** 推理策略，将复杂的跨模态任务分解为逐步生成中间模态的思维链。以语音驱动视频生成为例，完整生成路径为：

$$\{ d _ { \mathrm { s p h } } , d _ { \mathrm { i m g } } \} \to [ d _ { \mathrm { s h p } } , d _ { \mathrm { e x p } } , d _ { \mathrm { s e m } } , d _ { \mathrm { d s c } } , d _ { \mathrm { v i d } } ]$$

即从语音和图像出发，依次生成3DMM形状、表情、语义视频、描述，最终合成视频。每一步基于输入条件和已生成的模态序列预测下一个模态：

$$T _ { j } : \left\{ \begin{array} { l l } { \mathcal { D } _ { \mathrm { c o n d } } \to d _ { 1 } , } & { j = 1 , } \\ { \mathcal { D } _ { \mathrm { c o n d } } \cup \left\{ d _ { 1 } , \dots , d _ { j - 1 } \right\} \to d _ { j } , } & { j > 1 . } \end{array} \right.$$

消融实验证实，包含形状、表情、语义等中间步骤的思维链相比直接生成，能显著减少模糊纹理和身份偏离，提升生成质量（见 Figure 3）。

### 3. 视频解码/上采样：从语言模型直接解码到语义驱动扩散解码

**基线方案**由语言模型直接解码RGB视频令牌，受限于离散令牌的表达能力。

**Archon方案**将视频生成分为两阶段：语言模型生成语义视频令牌，再由语义驱动的视频扩散模型（基于WALT潜在扩散模型）结合参考图像与文本描述，上采样为高保真RGB视频。这一解耦设计使语言模型专注于跨模态推理，扩散模型专注于恢复高频纹理细节。

### 4. 训练任务调度与采样：从随机单任务到多任务加权采样

**基线方案**每步随机采样单一任务，易导致模态分布偏差和训练不均衡。

**Archon方案**每步采样多个任务，并根据任务困惑度与输出模态任务数计算采样权重：

$$S ( i ) = \frac { \log ( p _ { i } ) } { N _ { m ( i ) } }$$

其中 $p_i$ 为任务 $i$ 的困惑度，$N_{m(i)}$ 为输出模态 $m(i)$ 对应的任务数。该权重平衡了高难度任务与低难度任务、高频模态与低频模态之间的训练信号，确保多模态联合分布的有效学习。

### 5. 提示与任务表示：从稀疏任务令牌到结构化自然语言描述

**基线方案**依赖稀疏的特殊任务令牌指示输入输出模态，语义信息有限。

**Archon方案**采用结构化自然语言描述序列化提示，明确定义模态类型、状态（过去/现在）与期望输出。全模态集合定义为：

$$\mathcal { D } = \{ d ^ { t } \mid d \in D _ { \mathrm { v a r } } ^ { t } , t \in \{ 0 , 1 \} \} \cup D _ { \mathrm { i n v } }$$

涵盖时变模态（如语音、表情的过去/现在状态）和时不变模态（如参考图像）。这一设计充分利用预训练语言模型的语义理解能力，降低了模型对任务格式的学习负担。

### 关键证据支撑

- **语义视频重参数化**实现4倍令牌缩减，同时保留细粒度动态（Sec 3.1，置信度0.95）。
- **全模型（引入3DMM与描述作为中间模态）**在所有指标上超越直接生成基线，验证了逐步注入显式结构先验的有效性（Table 3，置信度0.95）。
- **统一多任务模型**在所有指标上优于专科模型集成，证明了共享表示与联合训练带来的正向迁移（Sec 4.4，置信度0.95）。
- 在CelebV-HQ上，语音驱动视频生成的**FID达到6.818，FVD为93.81，Sync-C为5.210**，全面超越AniPortrait、Echomimic、Hallo3等基线（Table 1，置信度0.98）。

## 整体框架

Archon 的整体流水线由四个核心模块串联构成，形成从多模态输入到高保真数字人输出的端到端生成系统：

1. **模态特定令牌器（Modality-Specific Tokenizers）**：将描述、脚本、语音、动画（含3DMM形状/表情/姿态参数）、图像、语义视频等七种模态分别编码为离散整数令牌，统一映射到共享词汇表中。其中，图像令牌器采用预训练的 **MAGVITv2**；形状、表情和姿态参数通过因果卷积的残差矢量量化VAE（VQVAE）独立离散化，码本配置分别为形状（8层×512码）、表情（8层×2048码）、姿态（6层×512码）。视频则通过语义视频重参数化——将RGB视频替换为保留结构动态、丢弃冗余纹理的离散语义标签序列——实现约4倍令牌压缩。

2. **语言模型骨干（Language Model Backbone）**：基于 **PaLM2** 的前缀解码器自回归模型，接收结构化自然语言描述序列化提示（明确各模态类型、状态与期望输出），利用预训练语义理解能力进行跨模态推理。训练时每步采样多个任务，并按任务困惑度与输出模态任务数加权（$S(i) = \frac{\log(p_i)}{N_{m(i)}}$）以平衡多模态联合分布学习。推理时，模型逐令牌预测输出模态序列。

3. **语义驱动视频扩散模型（Semantic-driven Video Diffusion Model）**：语言模型生成的语义视频令牌作为条件，结合参考图像和文本描述，输入基于 **WALT** 改进的潜在扩散模型，上采样解码为高保真RGB视频。该模块解决了语言模型直接生成连续视频信号时离散化破坏质量的问题。

4. **“模态思维”推理策略（Thinking in Modality）**：在推理阶段，将模糊的跨模态任务（如语音→视频）分解为逐步生成中间模态的思维链——例如从语音和图像出发，依次生成形状、表情、语义视频、描述，最终合成视频（$\{d_{\mathrm{sph}}, d_{\mathrm{img}}\} \to [d_{\mathrm{shp}}, d_{\mathrm{exp}}, d_{\mathrm{sem}}, d_{\mathrm{dsc}}, d_{\mathrm{vid}}]$）。每一步基于输入条件和已生成模态序列预测下一个模态（$T_j: \mathcal{D}_{\mathrm{cond}} \cup \{d_1,\dots,d_{j-1}\} \to d_j$），从而逐步细化生成质量，缓解端到端生成中的不确定性和分布偏移。

整体数据流为：**多模态原始信号 → 模态令牌器离散化 → 结构化提示输入语言模型 → 自回归生成目标令牌序列 → 令牌解离散化（视频令牌则经扩散模型上采样）→ 最终多模态输出**。该设计使模型天然支持任意模态子集的条件生成与任意模态编辑。

### 补充图表

![[assets/figures/papers/paper_list_l984_https_openaccess_thecvf_com_content_CVPR2026_html_Bao_Archon_A_Unified_M/figures/002_Figure_2.jpg]]
*Figure 2: Pipeline. We use modality tokenizers to tokenize description, script, speech, animation, image and semantic video into discrete tokens. These tokens are arranged in a structured format and input to the language model for multimodal reasoning. The synthesized tokens are detokenized into raw modalities. For synthesizing high-quality video, we employ a semantic-driven video diffusion model to synthesize high-quality video conditioned on image and semantic segmentations*

![[assets/figures/papers/paper_list_l984_https_openaccess_thecvf_com_content_CVPR2026_html_Bao_Archon_A_Unified_M/figures/001_Figure_1.jpg]]
*Figure 1: Archon. We propose a novel unified multimodal model that performs cross-modal generation among a wide range of modalities, including description, script, speech, animation, semantic video, image, and video. Furthermore, we introduce the concept of Thinking in Modality to reduce ambiguity during cross-modal transitions and enhance generation quality. Our model inherently supports conditional generation across arbitrary sets of modalities, enabling any modality editing throughout the entire multimodal input space*

## 核心模块与公式推导

Archon 的整体流水线由四个核心模块构成（Fig. 2）：(1) 模态特定离散令牌器，(2) 语言模型骨干，(3) 语义驱动视频扩散解码器，(4) “模态思维”推理策略。以下聚焦关键模块的设计原理与核心公式。

### 3.1 多模态令牌化与语义视频重参数化

系统需将七种异构模态统一到共享离散词汇表。对于图像，直接采用预训练 **MAGVITv2** 进行令牌化。对于语音，使用预训练 **USM** 模型提取离散令牌。对于文本模态（描述、脚本），使用语言模型原生文本分词器。

**语义视频重参数化** 是应对高帧率视频令牌爆炸的关键设计。传统 RGB 视频令牌器对 5 秒 30fps 视频产生约 9K 令牌，远超典型语言模型的上下文窗口。Archon 将 RGB 视频替换为 **语义视频**——即逐帧语义分割标签序列，保留结构动态与运动信息，丢弃冗余纹理细节。语义视频通过独立的 VQVAE 编码为离散令牌，其压缩后的令牌维度为：

$$ \begin{array} { r } { ( \frac { L - 1 } { 4 } + 1 ) \times 8 \times 8 } \end{array} $$

其中 $L$ 为语义视频原始帧数。该设计在时间维度上以步长 4 采样，空间维度压缩为 $8 \times 8$ 网格，实现 **4 倍令牌缩减**，同时保留细粒度动态信息（置信度 0.95）。参考图像单独编码以保留外观身份信息。

对于形状、表情、姿态等 3DMM 动画参数，分别训练三个 **残差矢量量化 VAE**，均采用因果卷积以保持时序因果性。码本配置为：形状（8 层，每层 512 码字）、表情（8 层，每层 2048 码字）、姿态（6 层，每层 512 码字）。

### 3.2 多模态任务定义与训练采样

**全模态集合定义。** 系统将模态分为时变模态 $D_{\mathrm{var}}$（如语音、语义视频，区分“过去” $t=0$ 和“当前” $t=1$）和时不变模态 $D_{\mathrm{inv}}$（如描述、参考图像）。全模态集合定义为：

$$ \mathcal { D } = \{ d ^ { t } \mid d \in D _ { \mathrm { v a r } } ^ { t } , t \in \{ 0 , 1 \} \} \cup D _ { \mathrm { i n v } } $$

**逐步生成循环。** 跨模态生成被分解为序列预测过程。在第 $j$ 步，模型基于输入条件 $\mathcal{D}_{\mathrm{cond}}$ 和已生成的中间模态 $\{d_1, \dots, d_{j-1}\}$ 预测下一模态 $d_j$：

$$ T _ { j } : \left\{ \begin{array} { l l } { \mathcal { D } _ { \mathrm { c o n d } } \to d _ { 1 } , } & { j = 1 , } \\ { \mathcal { D } _ { \mathrm { c o n d } } \cup \left\{ d _ { 1 } , \dots , d _ { j - 1 } \right\} \to d _ { j } , } & { j > 1 . } \end{array} \right. $$

**多任务训练采样权重。** 在 72 项同步任务上预训练时，为避免模态分布偏差，每步采样多个任务，并根据任务困惑度 $p_i$ 和输出模态 $m(i)$ 对应的任务数 $N_{m(i)}$ 计算采样权重：

$$ S ( i ) = \frac { \log ( p _ { i } ) } { N _ { m ( i ) } } $$

该公式平衡了高难度任务（高困惑度）的采样频率与各输出模态间的任务均衡性，确保语言模型公平学习联合分布（置信度 0.95）。

### 3.3 语义驱动视频扩散解码

语言模型生成的语义视频令牌通过反令牌化恢复为语义分割序列，但缺乏纹理细节。为此，引入基于 **WALT** 架构改进的语义驱动视频扩散模型，以语义视频、参考图像和文本描述为条件，在潜在空间生成高保真 RGB 视频。该模块将视频上采样与结构控制解耦，语言模型负责结构推理，扩散模型负责纹理补全。

### 3.4 模态思维策略

推理时，将模糊的跨模态任务分解为逐步生成中间模态的思维链。以语音驱动视频生成为例，完整思维链路径为：

$$ \{ d _ { \mathrm { s p h } } , d _ { \mathrm { i m g } } \} \to [ d _ { \mathrm { s h p } } , d _ { \mathrm { e x p } } , d _ { \mathrm { s e m } } , d _ { \mathrm { d s c } } , d _ { \mathrm { v i d } } ] $$

即从语音 $d_{\mathrm{sph}}$ 和参考图像 $d_{\mathrm{img}}$ 出发，依次生成 3DMM 形状 $d_{\mathrm{shp}}$、表情 $d_{\mathrm{exp}}$、语义视频 $d_{\mathrm{sem}}$、文本描述 $d_{\mathrm{dsc}}$，最终合成视频 $d_{\mathrm{vid}}$。实验表明，该链式生成相比端到端直接生成，显著减少模糊纹理和身份偏离（Fig. 3，置信度 0.95）。

![[assets/figures/papers/paper_list_l984_https_openaccess_thecvf_com_content_CVPR2026_html_Bao_Archon_A_Unified_M/figures/003_Figure_3.jpg]]
*Figure 3: Thinking in Modality. We show the results of speechto-video generation with different thinking strategies. The videos generated from chain 2 contain less distortion (e.g., blurry appearance and undefined textual symbols) and exhibit closer identity alignment with the ground truth*

## 实验与分析

### 4.1 实验设置

Archon 的语言模型骨干在 256 块 TPUv6 上训练 20 天，批次大小为 256；语义驱动视频扩散模型在 128 块 TPUv6 上训练 10 天，批次大小为 128。训练数据为从公开互联网采集的约 6,000 小时单人独白视频构成的大规模多模态数据集。评测时，每个基准数据集随机采样 200 个视频进行统一测试。

### 4.2 语音驱动视频生成

语音驱动视频生成是评估数字人生成质量的核心任务。论文在 CelebV-HQ 数据集上与 **AniPortrait**（Wei et al., arXiv 2024）、**Echomimic** 和 **Hallo3** 等基线方法进行对比。如 Table 1 所示，Archon 取得了 FID 6.818、FVD 93.81、Sync-C 5.210 的成绩，在所有指标上全面超越基线方法。其中 Sync-C 达到 5.210，表明模型在唇形同步方面具有显著优势。Table 1 中以 “∗” 标注在基准数据集上训练的方法，确保训练数据层面的公平对比。

![[assets/figures/papers/paper_list_l984_https_openaccess_thecvf_com_content_CVPR2026_html_Bao_Archon_A_Unified_M/figures/006_Table_1.jpg]]
*Table 1: Comparisons on speech-driven video generation. We compare video generation quality and lip synchronization against baselines. “∗” denotes methods trained on the benchmark dataset*

定性对比见 Figure 6，Archon 生成的视频在视觉质量和音视频同步方面均优于 AniPortrait、Echomimic 和 Hallo3。

![[assets/figures/papers/paper_list_l984_https_openaccess_thecvf_com_content_CVPR2026_html_Bao_Archon_A_Unified_M/figures/008_Figure_6.jpg]]
*Figure 6: Comparison on the Speech-driven Video Generation. We qualitatively compare the video quality and video-audio synchronization against AniPortrait [47], Echomimic [7], Hallo3 [11]*

### 4.3 图像条件文本到语音

在图像条件文本到语音任务上，Archon 与 **FaceTTS**（Lee et al., ICASSP 2023）进行对比。如 Table 2 所示，Archon 在 MCD-DTW 指标上达到 8.918，C-SIM 达到 0.9117，均优于 FaceTTS，验证了模型在语音质量和音色一致性上的优势。

![[assets/figures/papers/paper_list_l984_https_openaccess_thecvf_com_content_CVPR2026_html_Bao_Archon_A_Unified_M/figures/007_Table_2.jpg]]
*Table 2: Comparisons on image-conditioned text-to-speech. We compare speech quality and voice-identity coherence against the FaceTTS [25]*

### 4.4 消融实验

Table 3 报告了语音驱动视频生成任务上的消融实验结果，核心发现如下：

![[assets/figures/papers/paper_list_l984_https_openaccess_thecvf_com_content_CVPR2026_html_Bao_Archon_A_Unified_M/figures/009_Table_3.jpg]]
*Table 3: Ablation on Design Choices. We show ablation studies of different designs on speech-driven video generation task*

**完整思维链的有效性。** 全模型（引入 3DMM 形状、表情和描述作为中间模态的完整思维链）在所有指标上超越直接生成的基线模型，证明逐步注入显式结构先验（形状、表情）和语义先验（描述）能稳定视频质量与音频同步。Figure 3 的定性对比进一步显示，采用链 2（形状→表情→语义视频→描述→视频）生成的视频相比直接生成，模糊纹理和不明确文字符号等失真显著减少，身份一致性更接近真值。

**统一模型 vs. 专家集成。** 统一多任务模型在所有指标上优于由多个专科模型组成的集成系统，验证了共享表示与联合训练带来的正向迁移效应。这一结论来自 Sec 4.4 的对比实验，表明单一统一模型不仅降低了系统复杂度，还通过跨任务知识共享提升了各子任务的表现。

**语义视频重参数化与扩散解码。** 语义视频令牌压缩（4 倍令牌缩减）与语义驱动视频扩散解码器的组合，成功将视频令牌数降低至语言模型可管理的上下文窗口内（约 8K 令牌），同时保持了高生成质量。消融实验间接验证了该设计的必要性——若直接使用 RGB 视频令牌器，5 秒视频产生约 9K 令牌将超出上下文限制。

### 4.5 整体多模态生成与编辑能力

Figure 4 展示了给定任意单一模态输入时，Archon 的整体多模态生成与理解能力。Figure 5 展示了灵活的任意模态编辑能力——用户可以修改任意选定的模态，同时保持其他模态不变。这些定性结果体现了统一模型在跨模态条件生成和细粒度编辑上的通用性，但论文未提供对应的定量指标，该部分结论需结合视觉示例进行主观评估。

![[assets/figures/papers/paper_list_l984_https_openaccess_thecvf_com_content_CVPR2026_html_Bao_Archon_A_Unified_M/figures/004_Figure_4.jpg]]
*Figure 4: Multimodal Generation. We show holistic modality generation and understanding given an arbitrary modality as input*

![[assets/figures/papers/paper_list_l984_https_openaccess_thecvf_com_content_CVPR2026_html_Bao_Archon_A_Unified_M/figures/005_Figure_5.jpg]]
*Figure 5: Modality-specific Editing. We show flexible any modality editing to modify an arbitrarily chosen modality while maintain the others untouched. The icons on the top show the modalities used in the example, and the highlighted icons are the ones that are edited*

## 方法谱系与知识库定位

### 1. 问题定位与核心瓶颈

当前数字人生成系统普遍采用“专科模型拼凑”范式：针对语音合成、面部动画、视频生成等单一模态分别训练独立模型，再通过工程化管线串联。**Archon** 论文指出，该范式存在三个深层瓶颈：

1. **跨模态分布不匹配**：各专科模型在独立数据分布上训练，拼接时输入-输出空间存在未建模的偏移，导致生成结果在模态边界处出现伪影或身份漂移。
2. **冗余算力消耗**：多个模型各自维护独立的编码器-解码器，无法共享表示，推理时存在重复计算。
3. **扩展性受限**：每新增一种模态或任务，需要重新设计接口并训练新的专科模型，系统复杂度呈组合爆炸。

此外，高保真谈话视频的令牌序列过长（如 5 秒 30fps 视频产生约 9K 令牌），直接超过现有语言模型的上下文窗口；而将连续视频信号离散化后直接交由语言模型生成，又会因量化误差破坏视觉质量。跨模态任务（如语音→视频）本身还存在固有的模糊性——同一段语音可对应多种合理的面部运动——端到端映射难以捕捉这种一对多关系。

### 2. 与现有方法的谱系关系

#### 2.1 语音驱动视频生成基线

Archon 在 **CelebV-HQ** 基准上与以下方法进行了定量和定性对比（Table 1, Figure 6）：

- **AniPortrait**（Wei et al., arXiv 2024）：基于音频驱动面部动画的肖像视频生成方法。
- **Echomimic**：论文中标注为，具体出处需查证原文参考文献，其核心思路为利用音频特征驱动面部运动生成。
- **Hallo3**：论文中标注为，具体出处需查证原文参考文献。

这些基线方法代表了“端到端直接映射”的技术路线：从语音特征直接回归或生成视频帧。Archon 在 FID（6.818）、FVD（93.81）、Sync-C（5.210）三项指标上全面超越上述基线，其关键差异在于引入了 **“Thinking in Modality”** 逐步生成链——先产生 3DMM 形状、表情、语义视频、描述等中间模态，再合成最终视频——从而将模糊的跨模态映射分解为多个条件更明确的子问题。

#### 2.2 图像条件文本到语音基线

在语音合成任务上，Archon 对比了 **FaceTTS**（Lee et al., ICASSP 2023）。FaceTTS 从人脸图像中提取身份相关特征以条件化语音合成，代表了“视觉条件语音生成”的专科模型路线。Archon 在 MCD-DTW（8.918）和 C-SIM（0.9117）上均优于 FaceTTS（Table 2），表明统一模型在跨模态声纹一致性上具有优势。

#### 2.3 多任务专家模型集成

Archon 还构造了一个 **Ensemble of Experts** 基线：为每个子任务训练独立的专科模型，推理时按需调用。消融实验（Sec 4.4）表明，统一的单模型在所有指标上优于该专家集成。这验证了共享表示与联合训练带来的正向迁移效应——不同模态任务在统一词汇表和联合分布下学习，可以互相提供归纳偏置。

#### 2.4 统一多模态模型谱系中的位置

从更广的统一多模态模型谱系来看，Archon 可置于以下坐标：

- **相对于通用多模态 LLM**（如 GPT-4o、Gemini）：Archon 聚焦于“数字人”这一垂直领域，针对人体相关的七种模态（描述、脚本、语音、动画、语义视频、图像、视频）进行了专门的令牌器设计和预训练任务构建，而非追求通用场景的理解与生成。
- **相对于视频生成模型**（如 Sora、WALT）：Archon 不直接生成 RGB 视频令牌，而是采用“语义视频重参数化 + 扩散解码”的两阶段策略，将视频生成分解为结构推理（语言模型负责）和纹理解码（扩散模型负责），有效规避了长序列令牌的上下文窗口瓶颈。
- **相对于数字人专用模型**（如 AniPortrait、Echomimic）：Archon 的差异化在于“统一”和“思维链”——单一模型覆盖 72 项同步任务，且通过中间模态的逐步生成替代端到端黑箱映射。

### 3. 适用边界与局限

#### 3.1 适用场景

Archon 的设计使其特别适用于以下场景：
- **多模态协同编辑**：用户可修改任意一种模态（如替换语音），模型自动保持其余模态的一致性（Figure 5）。
- **稀疏条件生成**：给定部分模态（如仅图像和语音），模型可补全缺失模态，实现整体数字人生成（Figure 4）。
- **高保真谈话视频合成**：通过语义视频重参数化，在可控令牌预算内保留细粒度动态。

#### 3.2 已知局限

论文分析中未提取到明确的局限性声明（limitations 字段为空）。但基于方法设计可推断以下潜在边界：

1. **语义视频保真度上限**：语义视频重参数化丢弃了纹理、光照等外观细节，这些信息完全依赖参考图像和扩散模型恢复。当参考图像与目标姿态差异较大时（如侧脸参考图像生成正脸说话视频），扩散模型可能产生不自然的纹理填充。此推断需通过原文相关实验或用户研究进一步验证。

2. **思维链路径依赖**：Thinking in Modality 策略的生成质量依赖于中间模态的准确性。若 3DMM 形状或表情估计出现偏差，误差将沿生成链传播放大。论文通过消融实验（Table 3）验证了完整思维链优于直接生成，但未系统分析各中间步骤的鲁棒性边界。

3. **训练数据偏差**：模型在 6,000 小时公开互联网独白视频上训练，数据分布可能偏向特定人群、语言和场景，在极端姿态、非正面角度或非英语语音上的泛化能力未经充分验证。

4. **计算资源门槛**：语言模型需 256 TPUv6 训练 20 天，扩散模型需 128 TPUv6 训练 10 天，这限制了学术社区的直接复现和轻量化部署。

### 4. 开放问题

1. **语义视频令牌器的泛化能力**：当前语义视频令牌器针对人脸区域设计，其语义类别（如面部部件分割）是否能泛化到全身数字人或多人交互场景，尚待探索。

2. **思维链的自动发现**：论文中的思维链（形状→表情→语义视频→描述→视频）是人工设计的。是否能通过学习或搜索自动发现最优的中间模态生成顺序，是一个开放问题。

3. **实时推理可行性**：逐步生成链虽然提升了质量，但也增加了推理步数。在需要实时交互的数字人应用中，如何在思维链深度与推理延迟之间取得平衡，论文未给出定量分析。

4. **评估指标的完备性**：当前主要依赖 FID、FVD、Sync-C 等自动指标。对于数字人生成的“整体性”（holistic quality）——如多模态间的一致性、身份保持的长期稳定性——仍缺乏被广泛接受的评估协议。

## 原文 PDF

![[paperPDFs/CVPR_2026/Archon_A_Unified_Multimodal_Model_for_Holistic_Digital_Human_Generation.pdf]]
