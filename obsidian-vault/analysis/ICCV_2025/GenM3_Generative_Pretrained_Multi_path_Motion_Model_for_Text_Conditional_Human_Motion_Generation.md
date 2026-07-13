---
title: "GenM3: Generative Pretrained Multi-path Motion Model for Text Conditional Human Motion Generation"
type: paper
paper_level: A
venue: ICCV
year: 2025
pdf_ref: paperPDFs/ICCV_2025/GenM3_Generative_Pretrained_Multi_path_Motion_Model_for_Text_Conditional_Human_Motion_Generation.pdf
project_link: null
code_link: null
aliases:
- GPMPMMG
- GenM3
tags:
- ICCV_2025
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
- topic/generative_models_diffusion
core_operator: 通过多专家架构（MEVQ-VAE）动态适应不同数据集分布，并利用多路径Transformer（MMT）中模态专属路径与密集专家机制调节模态内与模态间的特征融合，结合大规模预训练强化运动表示。
primary_logic: 在运动量化和序列建模中同时引入多专家策略，并设计运动描述子生成上下文令牌来缩小文本-运动语义鸿沟，从而在统一框架下有效处理数据异质性，显著提升文本到运动生成的质量和泛化性。
claims:
- GenM3在HumanML3D（30FPS评估器）上达到FID 0.046，优于所有对比方法，并在IDEA400上取得强零样本泛化。
- 多专家VQ-VAE（MEVQVAE）将FID从标准VQ的0.098降至0.048，并在结合残差矢量量化（MERVQ）后进一步降至0.032。
- 预训练对GenM3的改善最大（35.21%），表明大规模预训练是提升运动表示的关键。
- 使用文本、运动及跨模态共享路径的多路Transformer在消融实验中取得最佳FID（0.035），验证了模态专属路径与密集专家的有效性。
---

# GenM3: Generative Pretrained Multi-path Motion Model for Text Conditional Human Motion Generation

> [!tip] 核心洞察
> 在运动量化和序列建模中同时引入多专家策略，并设计运动描述子生成上下文令牌来缩小文本-运动语义鸿沟，从而在统一框架下有效处理数据异质性，显著提升文本到运动生成的质量和泛化性。

| 字段 | 内容 |
|------|------|
| 中文题名 | GenM3：面向文本条件人体动作生成的生成式预训练多路径运动模型 |
| 英文题名 | GenM3: Generative Pretrained Multi-path Motion Model for Text Conditional Human Motion Generation |
| 会议/期刊 | ICCV 2025 |
| Links |  [paper](https://arxiv.org/abs/2503.14919)|
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction #topic/generative_models_diffusion |
| Method | Generative Pretrained Multi-path Motion Model (GenM3) |
| Dataset | HumanML3D, IDEA400 |

> [!tip] 效果简介
> - HumanML3D (30FPS evaluator) 上，FID 0.046 (GenM3) vs 0.110 (MMM) / 0.160 (T2M-GPT) (↓ 58.2% vs MMM)。
> - HumanML3D (30FPS) 上，R-Precision Top3 0.804 (GenM3) vs 0.784 (MMM) / 0.770 (T2M-GPT) (↑ 2.6% vs MMM)。
> - IDEA400 (zero-shot) 上，FID 4.232 (GenM3*) vs 7.947 (T2M-GPT) / 6.001 (MMM) (↓ 46.8% vs T2M-GPT)。

## 概要

### 问题瓶颈

文本条件的人体动作生成面临一个核心瓶颈：多源大规模运动数据存在显著的分布异质性，而运动领域长期缺乏专用的预训练表示模型。现有的离散令牌预测方法（如 **T2M-GPT**）、掩码运动生成方法（如 **MMM**、**MoMask**）或基于大语言模型的方法（如 **MotionGPT**）在单一数据集上表现尚可，但在联合训练时难以同时保证各数据集的性能，跨模态对齐亦受限于文本与运动之间的结构差异。这一瓶颈的实质是：**如何在统一框架下有效处理异质数据分布，并缩小文本-运动语义鸿沟**。

### 核心方法定位

GenM3（Generative Pretrained Multi-path Motion Model）通过两个关键设计回应上述瓶颈：

1. **多专家矢量量化变分自编码器（MEVQ-VAE）**：在编码器和解码器中引入多专家卷积层，所有专家同时激活并通过学习到的权重自适应调节贡献，使量化模块能够动态适应不同数据集的分布特性。
2. **多路径运动Transformer（MMT）**：在后半部分层中采用并行的运动路径、文本路径和跨模态共享路径，每条路径配备密集专家（Dense MoE）层；同时引入**运动描述子（Motion Descriptor）**，通过文本查询对运动嵌入进行注意力聚合，生成高层次上下文令牌并融入文本分支，增强跨模态对齐。

该方法采用三阶段训练：先训练MEVQ-VAE进行运动离散化并冻结，再在大规模运动数据上进行掩码建模预训练，最后在文本-运动对上完成文本条件微调。这一设计使得GenM3在统一框架下既能处理数据异质性，又能通过大规模预训练获得强泛化的运动表示。

### 主要结果

在HumanML3D基准上，GenM3使用30FPS评估器取得FID 0.046，较最优对比方法MMM（0.110）下降58.2%；使用官方20FPS评估器取得FID 0.035，优于MoMask（0.045）和MotionGPT（0.080）。在IDEA400零样本泛化测试中，GenM3*的FID为4.232，较T2M-GPT（7.947）下降46.8%。消融实验证实，多专家VQ-VAE将重建FID从标准VQ的0.098降至0.048，预训练对GenM3的改善幅度最大（35.21%），而多路径Transformer中同时使用文本和跨模态路径取得最佳生成性能。

### 文本驱动人体动作生成的现实需求

文本到人体动作生成（Text-to-Motion）旨在根据自然语言描述合成逼真的三维人体运动序列，在动画制作、虚拟人交互、游戏开发等领域具有广泛应用前景。该任务的核心挑战在于建立文本语义与运动动态之间的跨模态映射，同时保证生成动作的视觉质量和语义准确性。

### 现有方法的瓶颈

近年来，基于离散令牌预测的生成范式在该领域取得了显著进展。**T2M-GPT**、**MMM**、**MotionGPT** 和 **MoMask** 等方法将连续运动序列量化为离散令牌，再利用类 GPT 的 Transformer 进行自回归或掩码预测。然而，这些方法面临两个根本性瓶颈：

**瓶颈一：多源运动数据的分布异质性。** 现有运动数据集（如 HumanML3D、KIT、IDEA400 等）在采集设备、动作类型、标注粒度、帧率等方面存在显著差异，形成相互冲突的数据分布（Figure 8 的 T-SNE 可视化证实了各数据集间的分布偏移）。当直接混合多数据集进行联合训练时，标准 VQ-VAE 或残差 VQ（RVQ）的单一量化空间难以同时适应所有分布，导致重建质量下降，进而损害下游生成性能。

**瓶颈二：缺乏专用于运动数据的预训练表示模型。** 与 NLP 和 CV 领域拥有大规模预训练基础模型不同，运动生成领域长期缺乏在大规模运动数据上预训练的通用表示模型。现有方法通常仅在单一数据集（如 HumanML3D）上进行训练，模型容量和泛化能力受限于数据规模。Figure 1 的定性对比直观展示了这一问题：MotionGPT 在数据集扩展前无法响应相对简单的文本输入，而经过大规模预训练的 GenM3 则能生成高精度动作。

### 跨模态对齐的结构性挑战

文本与运动之间存在天然的语义鸿沟：文本是离散符号序列，具有高度抽象和组合性；运动则是连续时空序列，包含细粒度的关节旋转和位移信息。现有方法通常将文本令牌与运动令牌简单拼接后送入统一 Transformer 进行联合建模，缺乏对模态内特征精细化和模态间语义对齐的专门设计。这种“一刀切”的建模方式难以充分捕捉文本-运动对的细粒度对应关系，尤其当文本描述涉及复杂动作组合或罕见动作时，生成质量显著下降。

### 本文动机

基于上述分析，本文的核心动机可概括为三点：

1. **统一多源数据训练**：设计一种能够动态适应多数据集分布的量化架构，使模型从更大规模、更多样化的运动数据中获益，同时避免各数据集表现此消彼长。
2. **构建运动预训练基础模型**：借鉴 NLP 大规模预训练的成功经验，在整合的大规模运动数据集上进行掩码运动建模预训练，学习通用的运动表示，为下游文本条件生成提供更强的先验。
3. **精细化跨模态交互**：在序列建模层面引入模态专属路径和跨模态融合机制，缩小文本-运动语义鸿沟，提升生成动作与文本描述的对齐精度。

这三个动机共同指向一个目标：在统一框架下有效处理数据异质性，通过大规模预训练和精细架构设计，显著提升文本到运动生成的质量和泛化性。

## 核心方法与创新机理

GenM3的核心创新在于，它直面了一个此前被多数方法忽略的关键瓶颈：**多源大规模运动数据存在显著的分布异质性**。当简单地将来自不同数据集（如HumanML3D、IDEA400等）的运动数据混合进行联合训练时，由于各数据集在动作风格、关节结构、帧率等方面存在差异，标准模型往往难以同时适应这些分布，导致生成质量下降。GenM3通过一套系统性的“多专家”策略，在运动量化、序列建模和跨模态对齐三个层面协同解决了这一问题。

### 1. 多专家矢量量化（MEVQ-VAE）：动态适应数据分布差异

传统的矢量量化（VQ-VAE）使用固定的编码器/解码器处理所有输入，难以应对多源数据的分布异质性。GenM3提出的**多专家VQ-VAE（MEVQ-VAE）**在编码器和解码器中引入了多专家卷积层，其核心机制是：

- **全激活与自适应加权**：所有专家卷积核同时激活，每个专家的输出通过可学习的权重 $w_i$ 进行加权组合，公式为 $y = \sum_{i=1}^{e_q} w_i \cdot \mathrm{Conv}_i(x)$（Eq. 1）。这使得模型能够根据输入数据的特征动态调整各专家的贡献，从而灵活适应不同数据集的分布。
- **残差量化扩展（MERVQ）**：在MEVQ-VAE基础上进一步结合残差矢量量化，通过多级码本逐步细化运动表示。

消融实验（Table 3）强有力地验证了这一设计的有效性：标准VQ的FID为0.098，而多专家VQ（MEVQVAE）直接将FID降至0.048；结合残差量化后（MERVQ），FID进一步降至0.032。此外，专家数量为8时重建性能达到最佳（Figure 7）。

### 2. 多路径运动Transformer（MMT）：模态专属与跨模态的密集专家融合

传统的文本-运动生成方法通常将文本和运动令牌简单拼接后送入标准Transformer进行联合建模，这种方式忽略了两种模态在结构上的根本差异——文本是离散的语义符号序列，而运动是连续的时空动态序列。

GenM3的**多路径运动Transformer（MMT）**在架构上做出了根本性改变：将Transformer的后半部分层（后9层）划分为三条并行路径——

- **运动路径**：专门处理运动令牌，配备密集专家（MoE）层
- **文本路径**：专门处理文本令牌，同样配备密集专家层
- **跨模态共享路径**：处理文本-运动交互，促进模态间信息融合

每条路径中的每个专家是一个两层MLP：$\mathbb{E}_{p,i}(\boldsymbol{x}) = \mathbf{W}_{p,i}^2 \sigma(\mathbf{W}_{p,i}^1 x + b^1) + b^2$（Eq. 5），最终三条路径的输出拼接后通过线性投影得到最终表示（Eq. 7）。

消融实验（Table 6）表明，同时使用文本路径和跨模态路径时取得最佳FID（0.035），缺乏任一路径均导致性能下降。此外，密集专家（Dense MoE）相比稀疏专家（Sparse MoE）在FID和R-Precision上均更优（Table 5），验证了在运动生成任务中保持全容量专家激活的必要性。

### 3. 运动描述子：缩小文本-运动语义鸿沟

跨模态对齐的另一个关键创新是**运动描述子（Motion Descriptor）**。该模块通过文本查询对运动嵌入进行注意力聚合，生成高层次的上下文令牌 $\mathbf{E}_{ctx} = \mathrm{mean}\left(\mathrm{softmax}\left(\mathbf{E}_m \mathbf{E}_t\right) \mathbf{E}_t\right)$（Eq. 2），并将其融入文本分支。

这一设计的精巧之处在于：它不是简单地将文本和运动特征对齐，而是让文本主动“查询”运动特征中的语义相关信息，生成一个文本可理解的“运动摘要”，从而在语义层面弥合了两种模态的鸿沟。

### 4. 大规模预训练：释放多专家架构的潜力

GenM3的三阶段训练流程（Figure 2）中，第二阶段的大规模运动数据预训练（掩码运动建模）是性能提升的关键驱动力。实验（Figure 6）显示，预训练对GenM3的改善幅度最大（35.21%），远超MMM和T2M-GPT等基线方法。这表明，多专家架构的设计与大规模预训练形成了协同效应——多专家机制提供了处理异质数据的容量，而大规模数据则充分训练了这些专家的差异化能力。缩放定律实验（Table 9）进一步证实，随着预训练数据比例从0%增加到100%，FID持续改善（0.071 → 0.060 → 0.050 → 0.046），表明数据规模的正向影响尚未饱和。

---

**总结**：GenM3的核心创新并非单一的技术点，而是一套贯穿量化、建模、对齐三阶段的多专家策略体系。MEVQ-VAE解决了数据层面的分布异质性，MMT解决了模态层面的结构差异，运动描述子解决了语义层面的对齐鸿沟，而大规模预训练则为整个体系提供了充分的训练动力。这一系统性的设计使得GenM3在HumanML3D上取得了FID 0.046（30FPS评估器）和0.035（20FPS评估器）的领先性能，并在IDEA400上展现出强大的零样本泛化能力。

GenM3 的核心设计目标是在一个统一框架内同时处理来自多源大规模运动数据的分布异质性问题，并强化文本与运动之间的跨模态语义对齐。为此，整个框架被解耦为两个核心组件与一个三阶段训练流程，形成“量化-预训练-条件生成”的递进式管线。

### 三阶段训练管线

如图 2 所示，GenM3 的训练严格遵循三个阶段，各阶段之间通过模块冻结实现解耦，避免下游任务干扰上游表示学习。

1. **运动量化阶段**：首先训练多专家矢量量化变分自编码器（MEVQ-VAE），将连续运动序列压缩为离散令牌。该阶段完成后，MEVQ-VAE 被冻结，不再参与后续梯度更新。
2. **大规模预训练阶段**：在冻结 MEVQ-VAE 的前提下，仅使用运动模态数据对多路径运动 Transformer（MMT）进行掩码自重建预训练。模型学习从被部分掩码的运动令牌序列中预测缺失部分，从而习得通用的运动先验表示。
3. **文本条件微调阶段**：在预训练权重基础上，引入文本-运动配对数据，同时激活 MMT 的文本路径与跨模态路径，进行文本到运动的条件生成训练。文本令牌经处理后与运动离散令牌拼接，共同输入 MMT，其输出再送入 MEVQ-VAE 的解码器以重建运动序列。

### 模块关系与数据流

整体数据流可概括为“编码→量化→序列建模→解码”四个环节，且序列建模部分存在模态间的分支与融合。

- **MEVQ-VAE 编码器**：接收原始运动序列，通过多专家卷积块进行下采样与特征提取，输出连续潜变量。下采样因子为 4，有效压缩了序列长度。
- **共享码本**：将编码器输出的连续潜变量通过查找嵌入表量化为离散令牌。码本规模为 8192 个条目，每个条目维度为 32。这一量化过程将连续运动转化为离散符号序列，为后续 Transformer 建模提供基础。
- **多路径运动 Transformer（MMT）**：作为序列建模的核心，MMT 的结构分为两个阶段。前 9 层为标准自注意力层，对所有令牌进行统一建模；后 9 层则分化为三条并行路径——运动路径、文本路径和跨模态共享路径。每条路径均配备密集专家（Dense MoE）池，通过多个两层 MLP 专家的加权组合增强该路径的表征能力。运动描述子模块以文本查询对运动嵌入进行注意力聚合，生成上下文嵌入 $\mathbf{E}_{ctx}$，作为文本分支的补充输入，缩小文本与运动的语义鸿沟。三条路径的输出最终被拼接并通过线性投影融合，如公式所示：

$$\mathrm{Output} = \mathbf{W}_{proj} \left( \left[ \mathbb{E}_{motion} ; \mathbb{E}_{text} ; \mathbb{E}_{cross-modal} \right] \right) + b_{proj}$$

- **MEVQ-VAE 解码器**：接收 MMT 输出的融合表示，通过多专家卷积块逐步上采样，重建出最终的运动序列。

### 关键设计动机

该框架的核心创新在于将“多专家”策略同时注入量化层与序列建模层。在量化端，MEVQ-VAE 的多专家卷积层通过同时激活所有专家并自适应加权（$y = \sum_{i=1}^{e_q} w_i \cdot \mathrm{Conv}_i(x)$），动态适应不同数据集的分布差异，有效缓解了多源数据联合训练时的分布冲突。在序列建模端，MMT 的模态专属路径与跨模态共享路径配合密集专家机制，既保留了各模态内部的建模独立性，又通过共享路径和运动描述子实现了可控的跨模态信息融合。三阶段训练流程则将表示学习与条件生成分离，预训练阶段的大规模运动数据使模型习得鲁棒的运动先验，这是 GenM3 在 HumanML3D 上将 FID 降至 0.046、并在 IDEA400 上展现出强零样本泛化能力的结构基础。

GenM3 框架由两个核心组件构成：**多专家矢量量化变分自编码器（MEVQ-VAE）** 与 **多路径运动Transformer（MMT）**。前者负责将连续运动序列离散化为令牌，后者在离散令牌空间中进行序列建模与跨模态融合。整体训练分为三个阶段：1) 训练 MEVQ-VAE 并冻结；2) 在纯运动数据上预训练 MMT；3) 在文本-运动对上微调。

### MEVQ-VAE：多专家运动量化

MEVQ-VAE 在标准 VQ-VAE 的基础上，将编码器和解码器中的标准卷积层替换为**多专家卷积层**，以应对多源运动数据的分布异质性。与稀疏专家（仅激活 Top-K）不同，该层同时激活所有 $e_q$ 个专家，并通过可学习权重动态调节每个专家的贡献：

$$y = \sum_{i=1}^{e_q} w_i \cdot \mathrm{Conv}_i(x) \tag{1}$$

其中 $x$ 为输入特征，$\mathrm{Conv}_i$ 为第 $i$ 个专家的卷积核，$w_i$ 为对应的自适应权重。编码器对运动序列进行 4 倍下采样后，输出连续潜变量经共享码本（8192 个条目，维度 32）量化为离散令牌。解码器则从离散令牌重构运动序列。

量化阶段的总损失为重建损失与 Commitment 损失的加权和：

$$\mathcal{L}_q = \mathcal{L}_{rec} + \beta \mathcal{L}_{commit} \tag{8}$$

其中 $\beta=1$。消融实验（Table 3）表明，MEVQ-VAE 将 FID 从标准 VQ 的 0.098 降至 0.048，且专家数量设为 8 时重建性能最佳（Figure 7）。

### 运动描述子：跨模态语义桥梁

为缩小文本与运动之间的语义鸿沟，GenM3 引入**运动描述子（Motion Descriptor）** 模块。该模块以文本查询 $\mathbf{E}_t$ 对运动嵌入 $\mathbf{E}_m$ 进行注意力聚合，生成高层次的上下文令牌 $\mathbf{E}_{ctx}$：

$$\mathbf{E}_{ctx} = \mathrm{mean}\left(\mathrm{softmax}\left(\mathbf{E}_m \mathbf{E}_t\right) \mathbf{E}_t\right) \tag{2}$$

该上下文嵌入作为文本分支的补充输入，使文本路径能够感知运动语义，从而增强跨模态对齐。

### MMT：多路径运动Transformer

MMT 采用非对称架构：前 9 层为标准自注意力层，后 9 层分裂为三条并行路径——**运动路径**、**文本路径**和**跨模态共享路径**。每条路径内部使用密集专家（Dense MoE）层，每个专家为一个两层 MLP：

$$\mathbb{E}_{p,i}(\boldsymbol{x}) = \mathbf{W}_{p,i}^2 \sigma(\mathbf{W}_{p,i}^1 x + b^1) + b^2 \tag{5}$$

其中 $p \in \{\text{motion}, \text{text}, \text{cross-modal}\}$ 表示路径，$i$ 为专家索引。所有专家的输出经加权组合形成该路径的表示。最终，三条路径的输出被拼接并通过线性投影得到最终表示：

$$\mathrm{Output} = \mathbf{W}_{proj} \left( \left[ \mathbb{E}_{motion} ; \mathbb{E}_{text} ; \mathbb{E}_{cross-modal} \right] \right) + b_{proj} \tag{7}$$

消融实验（Table 6）验证了该设计的有效性：同时使用文本和跨模态路径时取得最佳 FID（0.035），缺乏任一路径均导致性能下降。此外，密集 MoE 在 FID 和 R-Precision 上均优于稀疏 MoE（Table 5）。

### 预训练损失

预训练阶段采用掩码运动建模，对随机掩码的令牌集合 $\mathcal{M}$ 进行预测，损失为负对数似然：

$$\mathcal{L} = - \sum_{i \in \mathcal{M}} \log P \left( x_i | \boldsymbol{x}_{\backslash \mathcal{M}} \right) \tag{9}$$

预训练对 GenM3 的性能提升最为显著（35.21%），远超 T2M-GPT 和 MMM 等基线方法（Figure 6），且 FID 随预训练数据比例增加而持续改善（Table 9）。

![[assets/figures/papers/paper_list_l1886_GenM3_Generative_Pretrained_Multi_path_Motion_Model_for_Text_Conditional/figures/003_Figure_3.jpg]]
*Figure 3: Architecture of multiway transformers in*

## 实验与关键发现

### 6.1 主实验结果

#### 6.1.1 HumanML3D 基准评估

GenM3 在 HumanML3D 数据集上进行了全面的定量评估。为保证公平比较，作者重新训练了基于 30FPS 运动数据的评估器，并在相同帧率数据上重新训练了 T2M-GPT 和 MMM 等基线方法。**Table 1** 展示了基于 30FPS 评估器的结果：

![[assets/figures/papers/paper_list_l1886_GenM3_Generative_Pretrained_Multi_path_Motion_Model_for_Text_Conditional/figures/004_Table_1.jpg]]
*Table 1: Comparison of Text-to-Motion on HumanML3D [10] (using our retrained evaluator on 30FPS motion data) and Zero-shot Textto-Motion on IDEA400 [19]. The highlight and underline represent the best and the second-best. Noting that*

- **FID**：GenM3 取得 **0.046** 的最佳成绩，相比第二名 MMM（0.110）降低了 **58.2%**，相比 T2M-GPT（0.160）降低了 71.3%。这表明 GenM3 生成的运动分布与真实数据分布最为接近。
- **R-Precision Top3**：GenM3 达到 **0.804**，优于 MMM（0.784）和 T2M-GPT（0.770），验证了其文本-运动跨模态对齐的优越性。
- **Diversity** 与 **Multimodality**：GenM3 在多样性和多模态性指标上也保持竞争力，未出现模式坍塌。

**Table 2** 展示了使用官方 20FPS 评估器的结果。GenM3*（使用全部文本-运动对训练）取得 **FID 0.035**，优于 MoMask（0.045）和 MotionGPT（0.080），进一步确认了其领先地位。GenM3（仅使用 HumanML3D 文本对）在 HumanML3D 指标上与 GenM3* 相当，但 GenM3* 的泛化能力更强。

#### 6.1.2 IDEA400 零样本泛化

在 IDEA400 数据集上的零样本评估（**Table 1**）中，GenM3* 取得 **FID 4.232**，显著优于 T2M-GPT（7.947，降低 46.8%）和 MMM（6.001，降低 29.5%）。这一结果直接验证了大规模预训练策略赋予模型的强泛化能力——模型在未见过的文本描述上仍能生成高质量运动。

### 6.2 消融实验

#### 6.2.1 多专家 VQ-VAE 的有效性

**Table 3** 系统比较了不同矢量量化方法的性能。标准 VQ 的 FID 为 0.098，引入多专家架构（MEVQVAE）后降至 0.048，降幅达 51.0%。进一步结合残差矢量量化（MERVQ）后，FID 进一步降至 **0.032**。这证明多专家策略有效缓解了多源数据分布异质性对量化表示的负面影响。

**Figure 7** 展示了 MEVQ-VAE 中专家数量对重建性能的影响：专家数量为 **8** 时重建性能最佳，验证了适度增加专家容量可提升表示能力。

#### 6.2.2 预训练的关键作用

**Figure 6** 揭示了预训练对不同方法的性能提升幅度。GenM3 从预训练中获益最大，测试集性能提升达 **35.21%**，而 MMM 和 T2M-GPT 的收益相对较小。这表明 GenM3 的多专家架构与大规模预训练之间存在协同效应——多专家策略为预训练提供了更灵活的表示空间，预训练则充分释放了该架构的潜力。

**Table 9** 进一步展示了数据规模缩放定律：随预训练数据比例从 0% 增至 100%，FID 持续改善（0.071 → 0.060 → 0.050 → 0.046），未出现饱和迹象，暗示更大规模数据可能带来进一步收益。

#### 6.2.3 多路径 Transformer 架构分析

**Table 6** 消融了多路径 Transformer 各分支的贡献。同时使用文本路径和跨模态共享路径取得最佳 FID（0.035），缺乏任一路径均导致性能下降。这验证了模态专属路径（文本路径处理语言语义、运动路径处理时序动态）与跨模态路径（融合两类信息）的互补性。

**Table 5** 比较了密集专家（Dense MoE）与稀疏专家（Sparse MoE）策略。密集专家在 FID 和 R-Precision 上均更优，说明同时激活所有专家并自适应加权，比稀疏路由更适合处理运动数据的复杂分布。

### 6.3 定性分析

**Figure 4** 展示了基于不同文本输入生成的运动可视化结果，GenM3 能够生成与描述语义高度一致的多样化动作。**Figure 5** 展示了运动插值（motion in-between）任务的可视化，模型能平滑连接给定的起始和结束姿态。

### 6.4 推理效率

**Table 8** 报告了在 RTX4090 GPU 上的推理速度。通过调整掩码解码的迭代次数，可在生成质量与速度之间灵活权衡，满足不同应用场景需求。

### 6.5 局限性

尽管 GenM3 取得了显著性能提升，仍存在以下局限：
1. **文本标注覆盖不足**：对于数据集文本分布外的描述，模型难以生成准确动作。未来计划利用额外的文本-动作对或视频-文本对增强语义理解。
2. **精细关节缺失**：当前方法主要关注身体动作生成，忽略了手指和面部等精细关节。未来将收集更全面的数据集以支持全身细节运动生成。

### 6.6 待验证问题

以下结论需读者结合原文进一步确认：
- 多专家架构在训练过程中动态分配专家权重的具体机制是否可解释，原文未提供可视化分析。
- 模型在更大规模数据下的性能增长曲线是否持续线性，以及整合手部、面部数据后的具体提升幅度，尚待后续工作验证。
- 密集 MoE 与稀疏 MoE 在更大规模下的计算效率与性能平衡点，原文未进行系统性探索。

![[assets/figures/papers/paper_list_l1886_GenM3_Generative_Pretrained_Multi_path_Motion_Model_for_Text_Conditional/figures/005_Table_2.jpg]]
*Table 2: Comparison of Text-to-Motion on HumanML3D [10] (using the evaluator trained on 20FPS motion data [9])*

![[assets/figures/papers/paper_list_l1886_GenM3_Generative_Pretrained_Multi_path_Motion_Model_for_Text_Conditional/figures/008_Table_3.jpg]]
*Table 3: Comparison of different VQ methods*

![[assets/figures/papers/paper_list_l1886_GenM3_Generative_Pretrained_Multi_path_Motion_Model_for_Text_Conditional/figures/012_Table_5.jpg]]
*Table 5: Comparisons of dense MoE and sparse MoE*

![[assets/figures/papers/paper_list_l1886_GenM3_Generative_Pretrained_Multi_path_Motion_Model_for_Text_Conditional/figures/014_Figure_8.jpg]]
*Figure 8: Visualization of data distribution after dimensionality reduction using T-SNE algorithm*

## 定位与知识库关联

### 1. 方法脉络与基线关系

GenM3 的核心技术路径属于**基于离散令牌的运动生成**范式，其直接前驱是 T2M-GPT 和 MoMask 等将运动序列量化为离散令牌、再通过自回归或掩码建模进行生成的框架。然而，GenM3 在两个关键维度上实现了结构性突破：

**（1）从单一分布到多源异质分布的量化适应**

传统方法（如标准 VQ-VAE 或残差 VQ，即 RVQ）假设训练数据服从单一分布，在整合多个运动捕捉数据集时面临分布冲突。GenM3 提出的 **多专家 VQ-VAE（MEVQ-VAE）** 在编码器和解码器中引入多专家卷积层，所有专家同时激活并通过学习到的权重自适应调节贡献（见 Eq. (1)）。这一设计使量化模块能够动态适应不同数据集的特征分布，而非强制统一表示。消融实验（Table 3）直接验证了该设计的有效性：标准 VQ 的 FID 为 0.098，MEVQ-VAE 降至 0.048，进一步结合残差矢量量化（MERVQ）后降至 0.032。

**（2）从统一建模到模态专属路径的序列生成**

现有方法（如 T2M-GPT、MMM）通常将文本和运动令牌简单拼接后送入统一 Transformer 进行联合建模。GenM3 的 **多路径运动 Transformer（MMT）** 在后半部分层中引入了并行的运动路径、文本路径和跨模态共享路径，每条路径配备密集专家（Dense MoE）层（见 Figure 3 和 Eq. (5)-(7)）。这种设计允许不同模态在各自专属路径中保留内部结构，同时通过跨模态路径实现特征融合。消融实验（Table 6）表明，同时使用三条路径时 FID 达到最优（0.035），移除任一路径均导致性能退化。

**（3）跨模态对齐的上下文令牌机制**

GenM3 引入**运动描述子（Motion Descriptor）**，通过文本查询对运动嵌入进行注意力聚合，生成高层次的上下文嵌入 $\mathbf{E}_{ctx}$（见 Eq. (2)），并将其融入文本分支。这不同于简单拼接或交叉注意力的做法，而是主动提取运动中对文本语义最具响应性的特征，缩小文本-运动语义鸿沟。

### 2. 适用边界与局限

**适用场景与优势边界：**

- **多源数据联合训练**：MEVQ-VAE 的多专家机制天然适合整合多个运动捕捉数据集，在 HumanML3D 和 IDEA400 上均取得领先性能（Table 1），特别是在 IDEA400 零样本设置下 FID 降至 4.232，相比 T2M-GPT 降低 46.8%。
- **大规模预训练依赖**：预训练对 GenM3 的改善幅度最大（35.21%，Figure 6），远超 MMM 和 T2M-GPT，表明该方法在数据规模扩大时具有更强的收益弹性。数据比例缩放实验（Table 9）进一步证实，随着预训练数据比例从 0% 增至 100%，FID 从 0.071 持续改善至 0.046。
- **掩码解码的推理灵活性**：GenM3 采用掩码建模而非自回归生成，支持通过调整迭代次数在推理速度与质量间权衡（Table 8）。

**明确局限：**

1. **文本分布外泛化不足**：论文明确指出，对于数据集文本分布之外的描述，模型难以生成准确的动作。当前文本标注数量仍然有限，限制了模型对多样化语言输入的理解能力。
2. **身体部位覆盖不全**：当前方法主要关注身体动作生成，忽略了手指和面部等精细关节的全身动作。这是运动生成领域普遍存在的问题，而非 GenM3 特有。
3. **多专家机制的动态分配可解释性**：尽管 MEVQ-VAE 通过学习权重自适应调节专家贡献，但专家权重如何在训练过程中动态分配以处理相互冲突的数据集分布，目前缺乏深入分析。

### 3. 开放问题

基于论文的方法设计和实验结果，以下问题值得进一步探索：

1. **多专家架构的分配机制**：MEVQ-VAE 和 MMT 中的多专家机制如何在训练过程中隐式地分配专家以处理不同数据集分布？是否存在专家坍塌或冗余问题？对专家权重的可视化分析可能揭示数据异质性的内在结构。

2. **数据规模的扩展极限**：Table 9 显示 FID 随数据比例增加而持续改善，但尚未触及平台期。整合更多样化的动作数据（如手部、面部精细动作）是否会带来线性增益，还是需要架构层面的进一步调整？

3. **密集 MoE 与稀疏 MoE 的权衡**：Table 5 表明密集 MoE 在 FID 和 R-Precision 上均优于稀疏 MoE，但密集专家的计算成本随专家数量线性增长。在更大规模下，两者的效率-性能平衡点在哪里？是否存在混合策略（如部分层密集、部分层稀疏）？

4. **文本-运动对齐的增强路径**：运动描述子通过注意力聚合生成上下文令牌，但该机制依赖于文本查询的质量。如何高效利用额外的文本-动作对或视频-文本对来提升模型对多样化描述的泛化能力，是突破当前文本分布外性能瓶颈的关键。

5. **全身运动生成的架构扩展**：将当前框架扩展至包含手指和面部关节的全身运动，需要处理更高维度的关节空间和更精细的时空依赖。MEVQ-VAE 的多专家机制是否可以直接迁移，还是需要引入层次化或分区域的量化策略？

## 原文 PDF

![[paperPDFs/ICCV_2025/GenM3_Generative_Pretrained_Multi_path_Motion_Model_for_Text_Conditional_Human_Motion_Generation.pdf]]
