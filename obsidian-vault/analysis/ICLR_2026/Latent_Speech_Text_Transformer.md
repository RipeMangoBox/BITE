---
title: "Latent Speech-Text Transformer"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/Latent_Speech_Text_Transformer.pdf
openreview_forum_id: krGpQzo8Mz
aliases:
- LSTTL
- LSTT
tags:
- ICLR_2026
- topic/representation_self_supervised_transfer
- topic/representation_self_supervised_transfer/representation_learning
core_operator: "通过潜在语音补丁聚合机制压缩语音序列，平衡两种模态的建模粒度与信息密度。"
primary_logic: "将自回归建模单元从单令牌提升到语音补丁，可在保持语义的同时缩短序列、降低计算开销，并促进跨模态知识迁移。"
claims:
- "在计算控制训练中，LST在语音HellaSwag上绝对提升6.5%（39.0→45.5）。"
- "在数据控制训练中，LST在语音HellaSwag上提升5.3%（40.2→45.5）。"
- "LST的收益随模型规模从1B到7B持续增长，且扩展性优于基线。"
- "在ASR微调中，LST仅需1k步即可达到6.8% WER，而基线为140%。"
---

# Latent Speech-Text Transformer

> [!tip] 核心洞察
> 将自回归建模单元从单令牌提升到语音补丁，可在保持语义的同时缩短序列、降低计算开销，并促进跨模态知识迁移。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 潜在语音-文本Transformer |
| 英文题名 | Latent Speech-Text Transformer |
| 会议/期刊 | ICLR 2026 (Oral) |
| Links | [paper](https://openreview.net/forum?id=krGpQzo8Mz); [GitHub](https://github.com/facebookresearch/lst) |
| Topic | #topic/representation_self_supervised_transfer #topic/representation_self_supervised_transfer/representation_learning |
| Method | Latent Speech-Text Transformer (LST) |
| Dataset | HellaSwag (S→S), HellaSwag (T→T), LibriSpeech ASR (clean) |

> [!tip] 效果简介
> - HellaSwag (S→S) 上，Accuracy (%) 为 45.5，对比 39.0，变化 +6.5。
> - HellaSwag (T→T) 上，Accuracy (%) 为 52.2，对比 47.0，变化 +5.2。
> - HellaSwag (S→S) 上，Accuracy (%) 为 45.5，对比 40.2，变化 +5.3。

## 概述

语音与文本的联合建模面临一个根本性瓶颈：语音令牌序列长度远大于文本，导致模态间计算资源分配严重不均。在典型的交错序列中，基线模型为每个文本单元分配约0.23个令牌，却需要约0.77个语音令牌，总序列长度膨胀至3.00（Table 13）。这种不对称不仅增加了自回归建模的计算开销，更阻碍了高效的跨模态对齐与知识迁移。

**潜在语音-文本Transformer（Latent Speech-Text Transformer, LST）** 针对上述瓶颈，将自回归建模单元从单令牌提升至**潜在语音补丁**。其核心机制是通过轻量级的补丁编码器（Patch Encoder）将语音令牌序列压缩为语义密集的补丁嵌入，再由全局Transformer自回归地建模交错的文本令牌与语音补丁，最终通过补丁解码器（Patch Decoder）预测下一个语音令牌。这一设计使语音序列长度压缩至约1/4（4→1补丁），总序列从3.00缩短至2.42，带来约20%的FLOPs降低（Table 13），同时保留了细粒度的词汇和句法信息（Table 12）。

LST在两种公平控制条件下展现出显著且一致的增益：

- **计算控制训练**（相同迭代次数）：LST在语音HellaSwag（S→S）上绝对提升**+6.5%**（39.0→45.5），在文本HellaSwag（T→T）上提升**+5.2%**（47.0→52.2）（Table 3）。
- **数据控制训练**（相同数据量）：LST在语音HellaSwag上提升**+5.3%**（40.2→45.5），并将语音-文本性能差距从9.4缩小至6.7（Table 4）。
- **扩展性**：LST的增益随模型规模从420M到1.8B持续增长，且扩展性优于基线（Figure 4）；在7B规模下仍保持优势（Table 8）。
- **下游迁移**：在LibriSpeech ASR微调中，LST仅需1k步即达到6.8% WER，而基线高达140%（Table 5），展现出极强的下游适应能力。

LST基于BLT架构（Pagnoni et al., 2024），其方法定位介于逐令牌自回归语音语言模型与完全离散化的多模态模型之间——通过潜在补丁这一信息瓶颈，在不牺牲语义保真度的前提下实现序列压缩与跨模态对齐。

## 背景与动机

### 语音-文本统一建模的序列失衡瓶颈

将语音理解与文本推理统一到单一自回归模型中，是构建通用语音智能体的关键路径。然而，现有语音-文本联合建模面临一个根本性的结构矛盾：**语音令牌的序列长度远大于文本令牌**。以HuBERT语音令牌为例，在交错的语音-文本数据中，基线模型需为每个文本单元分配约0.77个语音令牌，而文本仅占0.23个（Table 13）。这种长度不对称导致三个连锁问题：

1. **计算资源分配不均**：自回归Transformer的计算复杂度随序列长度平方增长，语音令牌占据绝大部分计算预算，挤压了文本推理所需的建模容量。
2. **跨模态对齐困难**：细粒度的语音帧与语义完整的文本词之间存在天然的粒度错配，模型难以在令牌级别建立有效的跨模态对应关系。
3. **扩展性受限**：当模型规模从420M扩展到1.8B时，基线的文本性能提升有限，语音-文本性能差距始终维持在9.4个百分点左右（Table 4），表明单纯增加参数量无法弥合模态间的信息密度差异。

### 现有方法的局限

当前语音-文本联合建模主要沿两条路径展开：

- **逐令牌自回归建模**（如SpiritLM类架构）：直接在语音令牌序列上执行下一令牌预测（NTP），训练目标为 $\mathcal{L}(\mathcal{D};\theta) = \sum_{s\in\mathcal{D}}\sum_{i}\log p_{\theta}(s_i|s_{<i})$。该方法保留了完整的语音信息，但序列冗长，计算效率低下，且跨模态知识迁移受限于令牌粒度的不匹配。

- **BPE压缩方法**：将语音令牌映射为BPE单元以缩短序列。然而，这种硬压缩会丢失语音中的韵律、说话人特征等副语言信息，且压缩边界与语义边界不一致，导致下游任务性能受损。

这两种方案均未从根本上解决**建模粒度与信息密度之间的张力**：逐令牌建模粒度太细、序列太长；硬压缩则粒度太粗、信息丢失严重。

### 核心动机：提升自回归建模的抽象层次

本文的核心洞察是：**将自回归建模的基本单元从单个语音令牌提升到语音补丁（speech patch），可以在保留语义完整性的同时大幅缩短序列长度**。这一思想源于字节潜在Transformer（BLT, Pagnoni et al., 2024）在文本领域的成功实践——通过将字节分组为潜在补丁，BLT在保持细粒度信息的同时实现了高效建模。

LST将这一范式迁移到语音-文本跨模态场景，其关键创新在于：仅在语音侧引入补丁机制，通过**潜在语音补丁聚合**将语音序列压缩至与文本相当的粒度水平。具体而言，4→1的补丁压缩使整体序列长度从3.00降至2.42，减少约20%的FLOPs（Table 13），同时语音-文本令牌比例从约3.3:1降至更均衡的1:2（Figure 6）。

这一设计选择背后的假设是：**语音信号的局部冗余可以通过补丁编码器有效消除，而补丁级别的语义表示更接近文本令牌的抽象层次，从而促进跨模态的知识共享和迁移**。后续实验证据表明，LST不仅在语音任务上获得显著提升（HellaSwag S→S +6.5%，Table 3），文本性能也同步改善（HellaSwag T→T +5.2%），验证了统一建模粒度对跨模态学习的正向作用。

## 核心创新

LST的核心创新在于**将自回归建模的粒度从逐语音令牌提升到潜在语音补丁（latent speech patches）**，从而系统性地解决了语音-文本多模态建模中序列长度失衡这一根本瓶颈。

### 瓶颈洞察：序列长度失衡

在传统的语音-文本联合自回归建模中（如SpiritLM类基线），语音令牌序列的长度远大于文本。以文中1:2的语音-文本词比例为例，基线模型在交错序列中为每个文本令牌分配约0.23个文本单元，却需要约0.77个HuBERT语音令牌（Table 13），导致语音侧的计算资源消耗远超文本侧。这种模态间的不对称不仅降低了计算效率，更阻碍了跨模态知识的有效迁移——模型被迫在长序列中分配注意力，难以捕捉高层语义对应关系。

### 核心机制：潜在补丁聚合

LST通过引入**补丁编码器（Patch Encoder）**和**补丁解码器（Patch Decoder）**这一轻量级的信息瓶颈，将语音令牌序列压缩为更紧凑的潜在补丁嵌入。具体而言：

- **补丁编码器**：通过滑动窗口自注意力和交叉注意力，将一组连续的语音令牌 $\mathcal{P}_i$ 聚合为单个补丁嵌入 $z_i = \mathrm{PatchEnc}(X_{\mathcal{P}_i})$。
- **全局Transformer**：以补丁嵌入（而非原始令牌）作为自回归建模单元，与文本令牌交替处理。
- **补丁解码器**：从补丁嵌入和先前的令牌上下文中恢复细粒度的语音令牌，通过下一令牌预测（NTP）损失进行训练。

这一架构的关键在于：**文本令牌保持原始粒度，仅对语音侧进行压缩**。这确保了文本侧的信息密度不受损失，同时将语音序列缩短约4倍（4→1补丁），使整体序列长度从3.00降至2.42，带来约20%的FLOPs减少（Table 13）。

### 补丁策略的创新空间

LST探索了四种补丁形成策略，构成了方法创新的重要维度：

| 策略 | 机制 | 特点 |
|------|------|------|
| **静态补丁** | 将语音序列等分为固定长度 $p$ 的非重叠段 $\mathcal{P}_i = \{ip, \ldots, \min((i+1)p-1, T)\}$ | 无需外部信号，但忽略语义边界 |
| **对齐补丁** | 利用Wav2Vec2+CTC强制对齐的时间戳，按词或BPE单元边界形成补丁 $\mathcal{P}_k = \{b_k, \ldots, e_k\}$ | 语义同步性好，但依赖外部对齐器 |
| **混合补丁** | 同时使用静态和对齐补丁 | 试图兼顾两者优势 |
| **课程补丁** | 训练早期使用对齐补丁（概率 $P(u)=1$），随后线性衰减至静态补丁（$P(u)=0$） | 在语义引导与推理独立性之间取得平衡 |

其中，**课程补丁（Curriculum Patching）**是最具原创性的设计。它通过训练步 $u$ 的概率调度函数 $P(u)$ 实现平滑过渡，在早期利用对齐信号引导模型学习有意义的语音分组，后期退化为静态补丁以消除推理时对外部对齐模型的依赖。实验表明，该策略在HellaSwag S→S上达到41.3，高于静态补丁的40.5，且跨三次运行的稳定性极高（std 0.13，Table 9）。

### 相对于基线的关键差异

与基线SpeechLLM相比，LST的changed slots可归纳为：

1. **建模单元**：从“逐语音令牌”提升为“潜在语音补丁”，使自回归步数与语义单元相匹配。
2. **序列长度**：通过4→1压缩将语音令牌占比从0.77降至0.19（Table 13），缓解模态间计算失衡。
3. **架构模块**：新增补丁编码器和补丁解码器，形成令牌↔补丁的双向映射，在压缩的同时保留细粒度信息（sWUGGY/sBLIMP评估证实补丁未损失词汇和句法信息，Table 12）。
4. **训练策略**：课程补丁机制实现了从“对齐引导”到“独立推理”的平滑过渡，是性能提升的关键驱动因素。

值得注意的是，LST的收益并非来自更大的模型或更多的数据，而是源于**序列结构的重新组织**——在计算控制训练中，LST在语音HellaSwag上绝对提升6.5%（39.0→45.5）；在数据控制训练中提升5.3%（40.2→45.5）。这一增益随模型规模从420M到1.8B持续增长（Figure 4），表明补丁机制具有可扩展性。

## 整体框架

LST 的核心思想是将自回归建模的粒度从单个语音令牌提升到**潜在语音补丁**（latent speech patches），以此压缩语音序列长度，平衡两种模态的信息密度。其架构建立在 byte-latent transformer（BLT）范式之上，由三个功能模块串联构成：

1. **Patch Encoder（补丁编码器）**：接收连续的 HuBERT 语音令牌序列，通过滑动窗口自注意力和交叉注意力将其聚合为固定维度的补丁嵌入。补丁的形成策略决定了信息压缩的方式——可以是固定长度的静态分段，也可以是基于语音-文本对齐时间戳的动态分组。
2. **Global Transformer（全局 Transformer）**：以自回归方式联合建模交错的文本 BPE 令牌和语音补丁嵌入。这是模型的核心推理引擎，仅在补丁粒度上操作语音模态，文本令牌则保持原始粒度不变。
3. **Patch Decoder（补丁解码器）**：一个轻量级 Transformer，在每一层中插入交叉注意力层，从全局 Transformer 输出的补丁表示和先前令牌上下文中预测下一个语音令牌，完成从潜在空间到原始令牌空间的映射。

整个 pipeline 的信息流为：原始语音令牌 → Patch Encoder 压缩 → 补丁嵌入 + 文本令牌 → Global Transformer 自回归建模 → Patch Decoder 解码 → 逐令牌预测。训练目标为标准的自回归最大似然损失，在语音令牌序列上最大化条件概率：

$$\mathcal{L}(\mathcal{D};\theta) = \sum_{s\in\mathcal{D}}\sum_{i}\log p_{\theta}(s_i|s_{<i})$$

值得注意的是，LST **仅对语音令牌进行补丁化**，文本令牌保持不变。这一非对称设计源于语音令牌序列长度远超文本的核心瓶颈——在交错的语音-文本数据中，基线模型每 0.23 个文本单元需处理 0.77 个语音令牌，导致整体序列长度膨胀至 3.00（以文本单元为基准）。通过 4→1 的补丁压缩，LST 将语音令牌密度降至 0.19，整体序列长度缩短至 2.42，带来约 20% 的 FLOPs 减少（Table 13）。

补丁形成策略是 LST 的关键设计空间，论文探索了四种方案（Section 3.1）：

- **静态补丁**：将语音序列等分为长度为 $p$ 的非重叠段，$\mathcal{P}_i = \{ip, \ldots, \min((i+1)p-1, T)\}$。
- **对齐补丁**：利用 Wav2Vec2+CTC 强制对齐时间戳，将第 $k$ 个文本单元对应的语音帧范围 $\mathcal{P}_k = \{b_k, \ldots, e_k\}$ 作为一个补丁。
- **混合补丁**：在训练中随机混合静态和对齐两种策略。
- **课程补丁**：训练早期使用对齐补丁提供语义引导，随后按线性衰减概率 $P(u)$ 逐步过渡到静态补丁，推理时完全退化为静态模式，无需对齐器依赖。

补丁嵌入的计算统一为 $z_i = \mathrm{PatchEnc}(X_{\mathcal{P}_i})$，其中 $X_{\mathcal{P}_i}$ 为属于第 $i$ 个补丁的语音帧段集合。

**架构配置**（Table 7）给出了各模块在不同模型规模下的深度、隐藏维度和注意力头数等参数，补丁编码器和解码器均保持轻量设计，确保计算开销主要集中在全局 Transformer 的跨模态建模上。

## 核心模块与公式推导

LST 的核心设计是将自回归建模的粒度从单个语音令牌提升到**潜在语音补丁**，通过一个信息瓶颈结构实现序列压缩与跨模态对齐。其架构由三个关键模块组成，如图2所示。

### 补丁编码器

补丁编码器负责将连续的语音令牌序列聚合为紧凑的补丁嵌入。给定语音帧段集合 $X_{\mathcal{P}_i}$，补丁编码器通过滑动窗口自注意力和交叉注意力机制生成补丁嵌入：

$$z_i = \mathrm{PatchEnc}(X_{\mathcal{P}_i})$$

其中 $z_i$ 是第 $i$ 个补丁的潜在表示，将作为全局Transformer的自回归建模单元。

补丁的形成策略决定了 $X_{\mathcal{P}_i}$ 的具体构成，论文提出了三种核心策略：

- **静态补丁**：将语音序列等分为长度为 $p$ 的非重叠段：
  $$\mathcal{P}_i = \{ip, \ldots, \min((i+1)p-1, T)\}$$
  其中 $T$ 为语音令牌总数。该策略无需外部对齐信号，但忽略了语义边界。

- **对齐补丁**：利用强制对齐时间戳，将第 $k$ 个文本单元对应的语音帧范围构成补丁：
  $$\mathcal{P}_k = \{b_k, \ldots, e_k\}$$
  其中 $b_k$ 和 $e_k$ 分别为该文本单元对齐的起始和结束帧索引。对齐信号由 Wav2Vec2+CTC 模型提供。

- **课程补丁**：训练过程中逐步从对齐补丁过渡到静态补丁，概率函数为：
  $$P(u) = \begin{cases} 1, & u < \tau_1 \\ 1 - \frac{u - \tau_1}{\tau_2 - \tau_1}, & \tau_1 \leq u < \tau_2 \\ 0, & u \geq \tau_2 \end{cases}$$
  其中 $u$ 为训练步数，$\tau_1$ 和 $\tau_2$ 为过渡区间的起止步数。该策略在训练早期利用对齐信号引导语义学习，后期退化为静态补丁以消除对外部对齐器的依赖。

### 全局Transformer

全局Transformer以自回归方式建模交错的文本令牌和语音补丁嵌入。与基线模型逐令牌建模不同，LST仅对语音补丁进行全局建模，文本令牌仍保持原始粒度。这一设计使得语音序列长度从约0.77（每交错的文本单元）压缩至约0.19（4→1补丁），整体序列从3.00缩短至2.42，带来约20%的FLOPs减少。

### 补丁解码器

补丁解码器是一个轻量级Transformer，通过交叉注意力层从补丁嵌入和先前令牌上下文中预测下一个语音令牌。其训练目标为标准的自回归最大似然损失：

$$\mathcal{L}(\mathcal{D};\theta) = \sum_{s\in\mathcal{D}}\sum_{i}\log p_{\theta}(s_i|s_{<i})$$

该损失函数在语音预训练语料上最大化语音令牌序列的似然，使得补丁解码器能够从压缩表示中恢复细粒度的语音信息。实验表明，补丁机制在 sWUGGY 和 sBLIMP 等细粒度词汇与句法评估上表现与基线持平，验证了信息瓶颈未损失低层语言特征。

## 实验与分析

### 核心瓶颈与实验设计逻辑

语音-文本多模态语言模型面临的根本矛盾在于：语音令牌序列长度远超文本，导致模态间计算资源分配严重失衡。基线模型在交错序列中每0.23个文本令牌对应0.77个语音令牌（Table 13），这种不对称性使自回归建模的计算负载向语音模态严重倾斜，阻碍了跨模态知识迁移与性能扩展。LST通过潜在语音补丁聚合机制压缩语音序列，将建模单元从单令牌提升到语音补丁，在保持语义的同时缩短序列长度——4→1补丁压缩使整体序列从3.00缩短至2.42，FLOPs减少约20%（Table 13）。

实验设计围绕两条公平性主线展开：**计算控制**（相同训练迭代次数）和**数据控制**（相同语音/文本令牌数量）。所有模型采用相同的基础Transformer架构，仅补丁模块存在差异；评估使用统一的TTS引擎（Kokoro）生成语音输入，对齐补丁所需的对齐器在训练和推断中保持一致（课程补丁在推断时退化为静态，避免额外依赖）。

### 主实验结果

#### 计算控制训练（Table 3）

在相同计算预算下，LST的课程补丁策略表现出全面且显著的性能优势：

- **语音故事完成（S→S）**：HellaSwag上达到45.5%，较Base SpeechLLM基线（39.0%）绝对提升**+6.5%**；StoryCloze上达到60.8%（基线55.4%），提升+5.4%；TopicStoryCloze上达到83.5%（基线79.7%），提升+3.8%。
- **文本故事完成（T→T）**：HellaSwag上达到52.2%（基线47.0%），提升**+5.2%**；StoryCloze上达到68.5%（基线66.3%），提升+2.2%。

值得注意的是，LST在提升语音性能的同时也改善了文本性能，这表明潜在补丁机制促进了有效的跨模态知识迁移，而非以牺牲文本能力为代价。

#### 数据控制训练（Table 4）

在相同语音/文本令牌数量下，课程补丁策略的LST在HellaSwag S→S上达到45.5%（基线40.2%），提升**+5.3%**；T→T上达到50.5%（基线49.6%），提升+0.9%。语音-文本性能差距从9.4缩小至6.7，表明补丁机制有效缓解了模态间的不平衡问题。

#### 扩展性分析（Figure 4, Table 8）

LST的收益随模型规模持续增长。在计算最优扩展中（420M→1.8B），LST在HellaSwag S→S上始终优于基线，且差距随规模扩大：1.8B规模下LST达到39.0%（基线35.3%），提升+3.7%。在7B子最优令牌扩展中（70B tokens，低于扩展律最优值约140B），LST仍保持优势，但提升幅度收窄，提示在超大规模数据受限场景下，性能瓶颈可能转向语音数据的多样性而非模型架构。

### 下游任务微调

#### ASR与TTS（Table 5）

在LibriSpeech ASR微调中，LST展现出极快的收敛速度：仅需**1k步**即可在test-clean上达到6.8% WER，而基线在相同步数下WER高达140%（test-clean），验证了补丁机制保留了细粒度的语音-文本对齐信息。在TTS任务上，LST以约4倍更短的生成序列长度（补丁级而非令牌级自回归生成）匹配了基线的CER性能（LST: 14.1/15.1 vs 基线: 6.0/13.3），在计算效率上具有显著优势。

### 消融实验

#### 补丁策略对比（Table 6, Table 9）

在近似匹配的补丁大小下，四种策略的性能排序为：

- **HellaSwag S→S**：课程补丁（41.3）> 静态补丁（40.5）> 对齐补丁-静音分离（39.9）> 对齐补丁-静音合并（38.5）
- **StoryCloze S→S**：对齐补丁-静音分离（60.3）> 课程补丁（59.8）> 对齐补丁-静音合并（58.9）> 静态补丁（58.7）

课程补丁策略综合表现最佳，且稳定性高（HellaSwag S→S上std仅0.13，Table 9），其核心优势在于训练早期利用对齐信号建立语义对应，随后逐步过渡到静态补丁以避免对齐噪声的累积影响。

![[assets/figures/papers/paper_list_l14_https_openreview_net_forum_id_krGpQzo8Mz/figures/014_Table_9.jpg]]
*Table 9: Average (Ave) and standard deviation (Std) across three runs. Each task is reported with both S→S and T→T directions*

#### 对齐粒度对比（Table 10）

在1:4的语音-文本令牌比例下，单词对齐补丁在S→S任务上显著优于BPE对齐补丁：StoryCloze上59.4 vs 55.6，TopicStoryCloze上84.8 vs 79.6。单词级对齐提供了更自然的语义边界，有助于补丁嵌入学习到更具语义区分度的表示（Figure 5的t-SNE可视化证实了这一点：同一单词的语音补丁嵌入形成紧密聚类，不同词类间分离清晰）。

![[assets/figures/papers/paper_list_l14_https_openreview_net_forum_id_krGpQzo8Mz/figures/010_Figure_5.jpg]]
*Figure 5: Visualization of word-level speech patch embeddings from alignment patching models on HellaSwag speech, grouped by different linguistic categories. Clusters of the same word are tight and well-separated from others*

#### 语音-文本令牌比例（Figure 6）

最佳语音-文本令牌比例为**1:2**。当语音令牌比例进一步升高时，文本性能出现显著下降，表明过度压缩语音会损失必要信息，而压缩不足则无法充分释放计算资源用于文本建模。

#### 细粒度语言信息保留（Table 12）

在sWUGGY（词汇判断）和sBLIMP（句法判断）评估中，LST的补丁机制表现与基线持平，表明压缩过程未损失低层词汇和句法信息。这一结果与ASR快速收敛的证据相互印证，共同说明潜在补丁在压缩序列的同时有效保留了语音信号的细粒度结构。

### 鲁棒性分析（Table 11）

在原始和改进版TTS评估集上，LST在StoryCloze和TopicStoryCloze的S→S任务上均优于基线，表明性能提升对TTS质量变化具有鲁棒性，并非依赖特定TTS引擎的产物。

### 失败模式与局限

1. **对齐依赖**：对齐补丁策略依赖外部Wav2Vec2+CTC对齐器，在训练早期引入计算开销；对齐噪声可能影响性能，课程补丁通过逐步退化为静态策略缓解了该问题，但未根本消除对外部对齐信号的依赖。
2. **语言与模态局限**：实验集中在英语语音数据集上，未在其他语言或多任务场景下大规模验证；LST目前仅针对语音-文本序列建模，扩展到图像、视频等模态仍需验证。
3. **超大规模数据受限**：在7B且数据受限（70B tokens）场景下，性能提升幅度收窄，提示语音数据多样性可能成为新的瓶颈。
4. **实时交互**：当前框架基于离线批处理设计，扩展至全双工对话等实时场景需要进一步研究流式补丁策略。

### 补充图表

![[assets/figures/papers/paper_list_l14_https_openreview_net_forum_id_krGpQzo8Mz/figures/001_Figure_1.jpg]]
*Figure 1: Comparison of LST and Baseline on HellaSwag story completion under two experimental setups, (a) compute-controlled: same number of training iterations and (b) data-controlled: same amount of training data*

![[assets/figures/papers/paper_list_l14_https_openreview_net_forum_id_krGpQzo8Mz/figures/004_Figure_4.jpg]]
*Figure 4: (b) Sub-optimal token scaling at 7B. Comparison at 70B tokens, below the scaling-law optimum (≈140B). Figure 4: Scaling behavior on HellaSwag (S→S and T→T.)*

![[assets/figures/papers/paper_list_l14_https_openreview_net_forum_id_krGpQzo8Mz/figures/005_Table_1.jpg]]
*Table 1: Speech training datasets with total speech hours and the amount of Hubert tokens*

![[assets/figures/papers/paper_list_l14_https_openreview_net_forum_id_krGpQzo8Mz/figures/006_Table_2.jpg]]
*Table 2: Evaluation datasets for story completion (MC = Multiple Choice)*

![[assets/figures/papers/paper_list_l14_https_openreview_net_forum_id_krGpQzo8Mz/figures/007_Table_3.jpg]]
*Table 3: Main comparison of LST models and baselines under the same computation budget scheme. Each dataset reports both S→S and T→T*

![[assets/figures/papers/paper_list_l14_https_openreview_net_forum_id_krGpQzo8Mz/figures/008_Table_4.jpg]]
*Table 4: Main comparison of LST models and baselines under the same speech/text tokens scheme. Each dataset reports both S→S and T→T*

![[assets/figures/papers/paper_list_l14_https_openreview_net_forum_id_krGpQzo8Mz/figures/009_Table_5.jpg]]
*Table 5: LibriSpeech ASR (WER) and TTS (CER) for the 1B model, reporting context units for ASR and generation units for TTS*

![[assets/figures/papers/paper_list_l14_https_openreview_net_forum_id_krGpQzo8Mz/figures/011_Table_6.jpg]]
*Table 6: Comparison of patching strategies with approximately matched patch sizes. Static uses fixed patch lengths, Align (sil sep.) treats silence as separate patches, and Align (sil merged) merges silence into words, and Curriculum gradually shifts from Align to Static during training*

![[assets/figures/papers/paper_list_l14_https_openreview_net_forum_id_krGpQzo8Mz/figures/012_Table_7.jpg]]
*Table 7: Model architecture configuration. Each module is shown with its depth, hidden dimension, number of attention heads, and other relevant settings*

![[assets/figures/papers/paper_list_l14_https_openreview_net_forum_id_krGpQzo8Mz/figures/013_Table_8.jpg]]
*Table 8: Scaling comparison between baseline SpeechLLM and LST at 1B and 7B*

## 方法谱系与知识库定位

### 1. 方法脉络与基线关系

LST 的核心思想是将自回归序列建模的单元从逐令牌提升到潜在补丁，这一设计直接继承自 **byte-latent transformer (BLT)**（Pagnoni et al., 2024）的架构范式。BLT 在字节级文本建模中引入可学习的补丁编码器-解码器，将原始字节压缩为更高层的潜在单元进行全局建模；LST 将这一思想迁移到语音-文本跨模态场景，但做了一个关键简化：**仅对语音令牌进行补丁化，文本令牌保持原始 BPE 形式**。这一非对称设计源于语音令牌序列长度远超文本这一根本瓶颈（约 0.77 语音令牌对应 0.23 文本令牌，见 Table 13），对称补丁化反而会破坏文本侧已有的高效表示。

在语音-文本联合建模的谱系中，LST 的直接基线是 **Base SpeechLLM**——一种直接处理 HuBERT 语音令牌的自回归语音-文本模型，架构上类似于 SpiritLM 等将语音令牌与文本令牌交错的范式。Base SpeechLLM 的致命弱点在于：语音令牌的序列长度远大于文本，导致自回归序列中语音侧的计算资源占比过高，跨模态对齐效率低下。这一瓶颈在 ASR 微调中暴露得最为彻底——基线模型在 1k 步迭代后 WER 仍高达 140%（Table 5），几乎未从语音输入中学到有效的文本映射。

另一个对比基线是 **BPE SpeechLLM**，它试图通过将语音令牌映射为 BPE 单元来压缩序列，但这一策略本质上是离散化压缩，丢失了语音信号的细粒度声学信息。LST 的补丁编码器-解码器设计则保留了连续潜在空间中的信息瓶颈，既能实现约 4→1 的序列压缩（序列长度从 3.00 降至 2.42，约 20% FLOPs 减少），又能通过补丁解码器恢复细粒度的语音令牌预测。

### 2. 方法差异的关键维度

LST 与基线方法的核心差异体现在四个维度上：

- **自回归建模单元**：基线使用逐语音令牌建模，LST 使用潜在语音补丁作为全局 Transformer 的自回归单元。这一变化将计算焦点从低层声学信号转移到语义相关的语音片段上。
- **序列压缩机制**：基线无压缩（扁平序列），BPE SpeechLLM 使用离散映射压缩，LST 使用可学习的补丁编码器实现连续空间压缩。后者的优势在于保留了梯度传播路径，使补丁表示可以通过端到端训练优化。
- **补丁形成策略**：LST 探索了四种策略——**静态补丁**（等长非重叠分段）、**对齐补丁**（基于 Wav2Vec2+CTC 的强制对齐边界）、**混合补丁**（随机选择静态或对齐）和**课程补丁**（训练早期使用对齐补丁，后期逐步过渡到静态补丁）。其中课程补丁综合表现最佳，在 HellaSwag S→S 上达到 41.3，且跨三次运行的稳定性最高（std 0.13，Table 9）。
- **局部编解码模块**：LST 引入了轻量级的 Patch Encoder 和 Patch Decoder，形成令牌↔补丁的信息瓶颈。Patch Encoder 使用滑动窗口自注意力和交叉注意力聚合语音帧段，Patch Decoder 则从补丁嵌入和先前令牌上下文预测下一个语音令牌。

### 3. 适用边界与局限

**适用边界**：

LST 的设计前提是语音序列长度显著大于文本序列长度，且存在可获取的对齐信号（用于课程补丁的早期阶段）。在语音-文本交错的故事完成任务（如 HellaSwag、StoryCloze）上，LST 的收益最为显著——计算控制训练下 S→S 绝对提升 6.5%（39.0→45.5），数据控制训练下提升 5.3%（40.2→45.5）。收益随模型规模从 420M 到 1.8B 持续增长（Figure 4a），表明补丁机制具有良好的扩展性。

在 ASR 微调场景中，LST 展现出极强的样本效率：仅需 1k 步即可达到 6.8% WER（LibriSpeech clean），而基线为 140%（Table 5）。这一差异的因果机制在于：补丁压缩后的序列更短，全局 Transformer 的梯度信号能更有效地传递到语音编码器，加速了声学-文本映射的学习。

**局限与失效模式**：

1. **对齐依赖性**：对齐补丁和课程补丁依赖外部对齐模型（Wav2Vec2+CTC），在训练早期引入额外计算开销。对齐噪声可能影响性能——实验表明，将静音合并到单词补丁（Align sil merged）在 HellaSwag S→S 上优于将静音作为独立补丁（Align sil sep.）（38.5 vs 37.2，Table 6），说明对齐粒度的选择对结果有显著影响。课程补丁通过在推理时退化为静态补丁，部分缓解了这一问题，但训练阶段仍需要对齐信号。

2. **语音-文本比例敏感**：最佳语音-文本令牌比例为 1:2（Figure 6），高于此比例会导致文本性能显著下降。这意味着 LST 的补丁压缩程度需要与数据混合比例协同调节，在语音数据占比更高的场景下可能需要更激进的压缩策略。

3. **语言与模态限制**：实验主要集中在英语语音数据集上（Table 1 所列数据集均为英语），未在其他语言或多任务场景下大规模验证。扩展到图像、视频等其他模态仍需进一步研究——补丁编码器的设计（滑动窗口自注意力+交叉注意力）在原理上可泛化，但不同模态的信息密度和序列特性差异可能要求不同的补丁策略。

4. **数据受限场景下的扩展瓶颈**：在 7B 规模且数据受限（70B tokens，低于扩展律最优值约 140B）的条件下，LST 的性能提升可能受制于语音数据的多样性而非模型规模（Figure 4b）。这表明补丁机制的收益上限与训练数据的覆盖度密切相关。

### 4. 开放问题

- **完全无需对齐信号的补丁策略**：当前课程补丁仍依赖 Wav2Vec2+CTC 对齐器。是否可以通过可学习的补丁边界预测或基于注意力的动态分段，实现完全端到端的补丁形成？这将是消除外部依赖的关键一步。
- **实时交互场景的扩展**：LST 的补丁编码器需要完整的语音帧段才能生成补丁嵌入，这在全双工对话等流式场景中引入延迟。如何设计增量式补丁编码，使模型能在部分帧到达时即开始全局建模？
- **多模态泛化**：潜在补丁框架的核心思想——将高密度序列压缩为语义相关的潜在单元——在理论上适用于图像补丁、视频帧段等场景。但不同模态的压缩比、补丁语义边界定义和编解码器设计需要针对性的研究。
- **课程调度策略的优化**：当前课程补丁使用线性衰减概率（从对齐过渡到静态），但更大规模数据下，最佳衰减调度（如余弦、指数衰减）和对齐阶段的持续时间可能需要进一步调优。

## 原文 PDF

![[paperPDFs/ICLR_2026/Latent_Speech_Text_Transformer.pdf]]
