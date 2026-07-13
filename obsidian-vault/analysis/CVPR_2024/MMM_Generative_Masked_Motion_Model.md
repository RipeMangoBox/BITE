---
title: "MMM: Generative Masked Motion Model"
type: paper
paper_level: A
venue: CVPR
year: 2024
pdf_ref: paperPDFs/CVPR_2024/MMM_Generative_Masked_Motion_Model.pdf
project_link: https://anonymous-ai-agent.github.io/MMMM
code_link: null
aliases:
- MGMMM
- MMM
tags:
- CVPR_2024
- topic/vision_multimodal_applications
- topic/generative_models_diffusion
- topic/motion_animation/human_motion_generation
- topic/motion_animation
core_operator: "通过将运动数据离散令牌化并采用掩码建模范式，利用双向 Transformer 同时捕获运动内部依赖和运动-文本语义对齐，实现并行迭代解码，从而在保持高保真度的同时大幅提升生成速度，并天然支持通过放置 [MASK] 令牌进行运动编辑。"
primary_logic: 借鉴 BERT 式掩码建模思想，将 3D 人体运动转换为离散令牌序列，并训练一个条件掩码 Transformer 以并行方式预测被遮挡的令牌。这种双向注意力机制能够显式建模运动间依赖和跨模态语义映射，使得推理时可通过逐步并行解码快速生成高质量运动，同时简单的掩码占位即可实现平滑的运动编辑。
claims:
- MMM 在 HumanML3D 数据集上取得 FID 0.08（表格中为 0.089±0.005）和最快的 AITS 0.081 秒，全面超越现有扩散和自回归方法。
- "仅通过放置 [MASK] 令牌，MMM 即可在不增加额外训练的情况下实现多种运动编辑任务（运动插值、上身编辑、长序列生成），且编辑过渡自然流畅。"
- MMM 的并行解码机制使其生成速度比可编辑的运动扩散模型快两个数量级（例如，MDM 需 28.11 秒，MMM 仅需 0.081 秒）。
- HumanML3D 上 FID↓ = 0.089 ± .005
---

# MMM: Generative Masked Motion Model

> [!tip] 核心洞察
> 借鉴 BERT 式掩码建模思想，将 3D 人体运动转换为离散令牌序列，并训练一个条件掩码 Transformer 以并行方式预测被遮挡的令牌。这种双向注意力机制能够显式建模运动间依赖和跨模态语义映射，使得推理时可通过逐步并行解码快速生成高质量运动，同时简单的掩码占位即可实现平滑的运动编辑。

| 字段 | 内容 |
|------|------|
| 中文题名 | MMM：生成式掩码运动模型 |
| 英文题名 | MMM: Generative Masked Motion Model |
| 会议/期刊 | CVPR 2024 |
| Links | [paper](https://arxiv.org/abs/2312.03596) · [Project](https://anonymous-ai-agent.github.io/MMMM) |
| Topic | #topic/vision_multimodal_applications #topic/generative_models_diffusion #topic/motion_animation/human_motion_generation #topic/motion_animation |
| Method | MMM (Generative Masked Motion Model) |
| Dataset | HumanML3D, KIT-ML, Motion In-betweening |

> [!tip] 效果简介
> - HumanML3D 上，FID↓ 0.089 ± .005 vs 0.112 (AttT2M) / 0.116 (T2M-GPT) (↓ 0.023)；R-Precision Top-1↑ 0.515 ± .002 vs 0.499 (AttT2M) (↑ 0.016)；MM-Dist↓ 2.926 ± .007 vs 3.038 (AttT2M) (↓ 0.112)。
> - KIT-ML 上，FID↓ 0.429 ± .019 vs 0.463 (MLD) / 0.688 (MotionDiffuse) (↓ 0.034)。
> - HumanML3D (速度) 上，AITS (秒) 0.081 vs 28.112 (MDM) (约 347 倍加速)。

## 概要

文本驱动的人体运动生成旨在根据自然语言描述合成逼真的 3D 运动序列。现有方法在**实时性能、高保真度和运动可编辑性**三者之间存在难以调和的权衡：扩散模型（如 **MDM**、**MotionDiffuse**）虽支持编辑但推理缓慢（单句平均推理时间 AITS 达 28.11 秒）；自回归模型（如 **T2M-GPT**、**AttT2M**）生成较快，却缺乏双向上下文建模能力，难以实现灵活的运动编辑；隐空间扩散模型（如 **MLD**）加速了推理，但牺牲了编辑性和部分保真度。这一瓶颈的根源在于：扩散范式的迭代去噪和自回归范式的因果单向生成，都无法同时满足**快速并行生成、精细语义对齐和灵活运动编辑**的需求。

**MMM（Generative Masked Motion Model）** 提出了一种全新的范式来解决上述矛盾。其核心思想借鉴了 BERT 式掩码建模：将 3D 人体运动通过 VQ-VAE 离散令牌化为运动令牌序列，并训练一个**条件掩码 Transformer**，以双向注意力同时捕获运动内部依赖和运动-文本语义对齐，并行预测被随机遮蔽的令牌。这一设计带来了三个关键优势：

1. **高保真生成**：双向注意力显式建模运动间依赖和跨模态语义映射，在 HumanML3D 数据集上取得 FID 0.08（表格中为 0.089±0.005），全面超越现有扩散和自回归方法。
2. **极速推理**：基于置信度的并行迭代解码（cosine 掩码调度，10 次迭代），AITS 仅需 0.081 秒，比可编辑的运动扩散模型 MDM 快约 347 倍。
3. **天然可编辑**：训练时模型已见过各类掩码模式，推理时仅需在目标位置放置 `[MASK]` 令牌，即可自动填补并保证平滑过渡，无需额外训练即可支持运动插值、上身编辑、长序列生成等多种编辑任务。

在方法谱系上，MMM 属于**离散令牌化 + 掩码建模范式**，与扩散模型（运动空间/隐空间）、自回归模型形成互补。其运动令牌化器采用大尺寸 factorized codebook（8192×32），条件掩码 Transformer 融合了 CLIP 句子嵌入和词嵌入，并通过预训练的长度预测器估计运动序列长度。这一架构使得 MMM 在文本驱动运动生成的质量-速度-可编辑性三角中取得了当前最优的综合表现。

### 问题背景

文本驱动的人体运动生成旨在根据自然语言描述合成逼真的 3D 人体动作序列，在动画制作、虚拟人交互、游戏开发等领域具有广泛的应用前景。该任务的核心挑战在于：模型需要同时理解自然语言的语义意图，并生成符合物理规律且语义对齐的运动序列。近年来，深度生成模型的快速发展推动了该领域的显著进步，但现有方法在**实时性能、高保真度和运动可编辑性**之间仍存在难以调和的权衡。

### 现有方法缺口

当前主流的文本驱动运动生成方法可分为三大范式，各自存在明显短板：

**运动空间扩散模型**（如 **MDM**、**MotionDiffuse**）直接在原始运动数据上执行条件去噪过程，能够生成较高质量的运动序列，但其迭代去噪的推理机制导致生成速度极慢。例如，MDM 在单块 NVIDIA RTX A5000 GPU 上平均需要 28.11 秒才能生成一条运动序列，难以满足实时交互需求。尽管部分方法通过运动修补（motion inpainting）实现了可编辑性，但高昂的时间成本严重限制了其实用性。

**隐空间扩散模型**（如 **MLD**）将扩散过程压缩到低维隐空间以加速推理，在一定程度上缓解了速度问题，但隐空间的压缩-重建过程不可避免地损失了运动细节，导致生成质量下降，且可编辑性往往被牺牲。

**自回归运动模型**（如 **T2M-GPT**、**AttT2M**）将运动生成建模为序列预测任务，通过逐令牌自回归解码生成运动序列。这类方法推理速度较快，但其单向因果注意力机制无法充分捕获运动序列的双向依赖关系，导致运动整体连贯性不足。更重要的是，自回归范式天然不支持灵活的中间帧编辑——无法在序列生成后对特定片段进行修改而不破坏上下文一致性。

综上，现有方法的核心瓶颈在于：**尚无单一框架能够同时实现快速生成、精细语义对齐和灵活的运动编辑**。扩散模型保真度高但速度慢，自回归模型速度快但编辑能力弱，隐空间方法则在质量与速度之间折中但丧失了可编辑性。

### 本文动机

受 BERT 式掩码建模在自然语言处理领域成功的启发，本文提出了一种全新的生成范式——**生成式掩码运动模型（MMM）**。核心思想是：将 3D 人体运动离散化为令牌序列，并训练一个条件掩码 Transformer，以双向注意力机制并行预测被随机遮蔽的运动令牌。这一范式具有以下关键优势：

1. **双向上下文建模**：不同于自回归模型的单向依赖，掩码 Transformer 能够同时利用前后文信息预测每个令牌，从而显式捕获运动序列内部的全局依赖关系以及运动与文本之间的跨模态语义对齐。

2. **并行迭代解码**：推理时从全掩码序列出发，通过基于置信度的并行迭代解码逐步揭示高置信令牌，仅需 10 次迭代即可生成完整运动，速度比可编辑的运动扩散模型快两个数量级。

3. **天然可编辑性**：由于模型在训练阶段已见过各类掩码模式，推理时只需在需要编辑的位置放置 `[MASK]` 令牌，模型即可自动填补空缺并保证过渡平滑，无需额外训练或设计专门的编辑模块。这使 MMM 能够统一支持运动插值、上身编辑、长序列生成等多种编辑任务。

通过这一范式转换，MMM 旨在打破现有方法在质量、速度和可编辑性之间的“不可能三角”，为实时交互式运动生成与编辑提供新的技术路径。

## 核心方法与创新机理

### 1. 瓶颈洞察：实时性、高保真度与可编辑性的不可能三角

文本驱动人体运动生成领域长期面临一个根本性权衡：**扩散模型**（如 MDM、MotionDiffuse）虽能生成高质量运动，但其迭代去噪过程导致推理速度极慢（单条运动平均耗时 28.11 秒），无法满足实时交互需求；**自回归模型**（如 T2M-GPT、AttT2M）虽推理较快，却因因果注意力机制的单向性，难以显式建模运动序列的双向依赖，且不支持灵活的运动编辑。更关键的是，现有方法在**高保真度、实时性能和运动可编辑性**三者之间始终无法兼得——扩散模型的可编辑性依赖于运动空间上的修补操作，计算开销巨大；自回归模型则天然缺乏“填空”能力。MMM 的出发点正是打破这一不可能三角。

### 2. 核心范式转换：从扩散/自回归到条件掩码建模

MMM 的核心创新在于将运动生成问题重新定义为**条件掩码令牌预测**任务，借鉴了 BERT 式掩码建模思想。这一范式转换体现在三个关键环节：

**（1）运动表征的离散令牌化。** 不同于 MDM 直接在原始运动空间操作、MLD 在连续隐空间扩散，MMM 通过 VQ-VAE 将 3D 人体运动序列编码为**离散运动令牌序列**（codebook 尺寸 8192）。这一离散化不仅大幅压缩了运动表征维度，更使得掩码建模成为可能——离散令牌天然适合被遮蔽和预测，类似于自然语言处理中的 [MASK] 机制。大尺寸 codebook 有效减少了量化过程中的信息损失，为后续高质量重建奠定了基础。

**（2）生成范式的根本转变。** MMM 摒弃了扩散模型的逐步去噪和自回归模型的单向顺序生成，转而采用**条件掩码运动 Transformer**。训练时，随机遮蔽部分运动令牌，模型在文本条件（CLIP 句子嵌入和词嵌入通过交叉注意力注入）和未遮蔽令牌的双向上下文下，并行预测所有被遮蔽令牌。其训练目标为掩码令牌的负对数似然最小化：

$$\mathcal{L}_{\mathrm{mask}} = - \mathbb{E}_{\mathbf{Y} \in \mathcal{D}} \left[ \sum_{\forall i \in [1, L]} \log p \left( y_i \mid Y_{\overline{\mathbf{M}}}, W \right) \right]$$

双向注意力机制使得模型能够同时捕获运动序列内部的时空依赖和运动-文本的跨模态语义对齐，这是自回归模型单向注意力无法实现的。

**（3）并行迭代解码策略。** 推理时，MMM 从全 [MASK] 序列开始，采用**基于置信度的并行迭代解码**：每轮迭代中，模型并行预测所有 [MASK] 位置的令牌分布，保留高置信度预测并替换对应 [MASK]，低置信度位置继续遮蔽进入下一轮。掩码数量按余弦调度递减：

$$n_M(t) = L \cdot \cos\left(\frac{1}{2} \pi \frac{t}{T_{dyn}}\right)$$

仅需 10 次迭代即可完成生成，单条运动平均推理时间仅 **0.081 秒**，比 MDM 快约 **347 倍**（Table 7），实现了两个数量级的加速。

### 3. 可编辑性的原生实现：无需额外训练的掩码占位机制

MMM 最具特色的创新在于其**天然的可编辑性**。由于模型在训练阶段已见过各类掩码模式（随机遮蔽、不同比例），推理时只需将 [MASK] 令牌放置在需要编辑的位置，模型即可自动填补并保证过渡平滑。这支持三类编辑任务而无需任何额外训练：

- **运动插值（Motion In-betweening）：** 在给定首尾关键帧之间放置 [MASK]，模型填充中间过渡运动，FID 仅 0.0712，远优于 MDM 的 2.371（Table 3）。
- **上身编辑（Upper Body Editing）：** 固定下身运动，用 [MASK] 替换上身令牌并给定新文本条件，模型生成与下身协调的上身动作。训练时引入专门的上身编辑损失以增强上下身一致性。
- **长序列生成（Long Sequence Generation）：** 将多段文本描述对应的运动令牌用 [MASK] 过渡区连接，模型单步生成自然过渡运动，实现任意长度的故事驱动运动合成。

### 4. 方法谱系与知识库定位

MMM 处于文本驱动运动生成、离散令牌化与掩码建模的交叉点：

| 维度 | 代表方法 | 与 MMM 的关系 |
|------|---------|--------------|
| 扩散模型 | **MDM**（运动空间扩散）、**MotionDiffuse**、**MLD**（隐空间扩散） | MMM 以并行解码替代迭代去噪，速度提升两个数量级 |
| 自回归模型 | **T2M-GPT**、**AttT2M**（含交叉注意力） | MMM 以双向注意力替代因果注意力，增强语义对齐和可编辑性 |
| VQ-VAE 离散化 | VQ-VAE 系列 | MMM 继承离散令牌化思想，但将其首次系统应用于 3D 运动生成 |
| 掩码建模 | BERT、MaskGIT（图像生成） | MMM 将掩码建模范式迁移至条件运动生成，并创新性地赋予其编辑能力 |

MMM 的关键突破在于：通过**离散令牌化 + 双向掩码 Transformer + 并行迭代解码**的组合，首次在运动生成领域同时实现了 SOTA 质量（HumanML3D 上 FID 0.089、R-Precision Top-1 0.515）、实时推理（AITS 0.081 秒）和原生可编辑性三者统一，为实时交互式运动生成应用提供了可行的技术路线。

MMM 遵循一个两阶段范式，将 3D 人体运动生成重新表述为离散令牌空间中的掩码预测问题。其核心 pipeline 由两个功能模块串联构成：**运动令牌化器（Motion Tokenizer）** 和 **条件掩码运动 Transformer（Conditional Masked Motion Transformer）**，如图 3 所示。

**阶段一：运动离散令牌化。** 运动令牌化器基于 VQ-VAE 架构，负责将原始 3D 运动序列压缩为离散的运动令牌序列。其编码器将运动映射到潜在空间，通过一个大规模因子化码本（codebook 尺寸 8192，维度 32）进行矢量量化，解码器再将量化后的嵌入重建为运动。这一过程将连续的运动流转换为紧凑的离散符号序列，为后续的掩码建模提供了统一的 token 空间。训练该模块的损失函数为标准的矢量量化损失，包含码本损失与承诺损失：

$$L_{VQ} = \| \operatorname{sg}(\mathbf{z}) - \mathbf{e} \|_2^2 + \beta \| \mathbf{z} - \operatorname{sg}(\mathbf{e}) \|_2^2$$

其中 $\operatorname{sg}(\cdot)$ 表示停止梯度算子，$\mathbf{z}$ 为编码器输出，$\mathbf{e}$ 为码本中对应的嵌入向量。

**阶段二：条件掩码运动建模。** 在获得离散运动令牌后，条件掩码 Transformer 以 BERT 式掩码语言模型的方式进行训练。输入序列由三部分组成：被随机遮蔽的运动令牌、来自 CLIP 文本编码器的词级嵌入（通过交叉注意力注入）、以及句级嵌入。此外，模型引入了三个可学习的特殊令牌——`[MASK]` 用于占位待预测的位置，`[PAD]` 用于填充序列至固定长度，`[END]` 标记运动序列的终止。训练目标是最小化被掩码令牌的负对数似然：

$$\mathcal{L}_{\mathrm{mask}} = - \mathbb{E}_{\mathbf{Y} \in \mathcal{D}} \left[ \sum_{\forall i \in [1, L]} \log p \left( y_i \mid Y_{\overline{\mathbf{M}}}, W \right) \right]$$

其中 $Y_{\overline{\mathbf{M}}}$ 表示未被掩码的运动令牌，$W$ 为文本条件。由于 Transformer 采用双向注意力机制，模型能够同时利用前后文信息预测被遮蔽的令牌，这使其天然具备运动内部依赖建模和跨模态语义对齐的能力。

**推理时的并行解码。** 生成过程从一张“空白画布”（全部为 `[MASK]` 令牌的序列）开始。模型通过迭代并行解码逐步揭示运动内容：每轮迭代中，Transformer 对所有掩码位置进行预测并给出置信度，根据余弦掩码调度 $n_M(t) = L \cdot \cos(\frac{1}{2} \pi \frac{t}{T_{dyn}})$ 保留高置信令牌、重新掩码低置信令牌，经过固定轮次（默认 10 次）后输出完整令牌序列，再由运动令牌化器的解码器还原为 3D 运动。一个预训练的长度预测器根据输入文本估计所需的运动序列长度，从而确定令牌数量。

**编辑的统一接口。** 上述掩码建模范式使得 MMM 无需任何额外训练即可支持多种运动编辑任务。无论是运动插值、长序列生成还是上身编辑，用户只需在需要编辑的位置放置 `[MASK]` 令牌，模型即可自动填补空白并保证过渡平滑——因为训练阶段模型已经见过各类掩码模式，学会了在部分观测条件下进行双向推理。

### 补充图表

![[assets/figures/papers/paper_list_l6_https_arxiv_org_abs_2312_03596/figures/003_Figure_3.jpg]]
*Figure 3: Overall architecture of MMM. (a) Motion Tokenizer transforms the raw motion sequence into discrete motion tokens according to a learned codebook. (b) Conditional Masked Transformer learns to predict masked motion tokens, conditioned on word and sentence tokens obtained from CLIP text encoders. (c) Motion Generation starts from an empty canvas and the masked transformer concurrently and progressively predicts multiple highconfidence motion tokens*

MMM 的整体架构由两个核心模块构成：**运动令牌化器（Motion Tokenizer）** 和**条件掩码运动 Transformer（Conditional Masked Motion Transformer）**，两者通过“离散令牌化 + 掩码预测”的范式实现高效、高质量且天然可编辑的运动生成。

### 运动令牌化器：VQ‑VAE 与离散运动令牌

运动令牌化器的目标是将连续的 3D 人体运动序列压缩为离散令牌序列，同时保留丰富的运动语义信息。其本质是一个基于矢量量化变分自编码器（VQ‑VAE）的编码器‑码本‑解码器结构：

- **编码器**将原始运动序列映射为连续潜在表示 $\mathbf{z}$；
- **码本（codebook）** 包含 $K$ 个可学习的嵌入向量 $\mathbf{e}_k \in \mathbb{R}^D$，通过最近邻查找将 $\mathbf{z}$ 量化为离散令牌索引；
- **解码器**从量化后的嵌入重建运动序列。

为降低量化过程中的信息损失，MMM 采用了大尺寸的分解式码本（codebook 大小 8192），并引入移动平均更新和死码本重置技术以稳定训练。训练目标为矢量量化损失：

$$L_{VQ} = \| \operatorname{sg}(\mathbf{z}) - \mathbf{e} \|_2^2 + \beta \| \mathbf{z} - \operatorname{sg}(\mathbf{e}) \|_2^2$$

其中 $\operatorname{sg}(\cdot)$ 为停止梯度算子。第一项为码本损失，推动所选码本向量 $\mathbf{e}$ 靠近编码器输出 $\mathbf{z}$；第二项为承诺损失（commitment loss），约束编码器输出不要偏离码本向量过远，$\beta$ 为平衡系数。

### 条件掩码运动 Transformer：双向建模与掩码预测

在获得离散运动令牌序列后，MMM 使用条件掩码 Transformer 进行生成建模。该模块接收三类输入：

- **运动令牌序列**，其中部分位置被替换为可学习的 `[MASK]` 令牌；
- **文本条件**，来自 CLIP 文本编码器的句子级嵌入和词级嵌入，通过交叉注意力注入 Transformer；
- **特殊令牌**，包括 `[PAD]`（填充）和 `[END]`（序列结束标记）。

与自回归模型中单向因果注意力不同，该 Transformer 采用**双向自注意力**，使每个令牌能够同时关注序列中所有未掩码位置，从而显式捕获运动内部依赖和运动‑文本语义对齐。

训练目标为掩码运动重建损失，即最小化被掩码令牌的负对数似然：

$$\mathcal{L}_{\mathrm{mask}} = - \mathbb{E}_{\mathbf{Y} \in \mathcal{D}} \left[ \sum_{\forall i \in [1, L]} \log p \left( y_i \mid Y_{\overline{\mathbf{M}}}, W \right) \right]$$

其中 $\mathbf{Y}$ 为运动令牌序列，$Y_{\overline{\mathbf{M}}}$ 为未被掩码的令牌，$W$ 为文本条件，$L$ 为序列长度。模型需在给定文本和可见令牌的条件下，并行预测所有被遮蔽位置的真实令牌。

### 推理：并行迭代解码与余弦掩码调度

推理阶段从一个完全由 `[MASK]` 令牌组成的“空白画布”开始。在第 $t$ 次迭代中，模型并行预测所有掩码位置的令牌分布，并按置信度保留部分高置信预测，其余位置继续掩码。掩码数量按余弦调度衰减：

$$n_M(t) = L \cdot \cos\left(\frac{1}{2} \pi \frac{t}{T_{dyn}}\right)$$

其中 $T_{dyn}$ 为总迭代次数（通常设为 10）。早期迭代保留极少数高置信令牌以提供上下文锚点，后期上下文丰富后逐步减少掩码。令牌采样采用温度调节的 softmax 分布：

$$p(y_i | Y_{\bar{M}}, W) = \frac{\exp(e_i / \beta)}{\sum_{i \in E} \exp(e_i / \beta)}$$

其中 $e_i$ 为模型输出的 logits，$\beta$ 为温度参数（$\beta=1$ 时效果最佳）。

### 运动编辑：掩码占位即编辑

MMM 的双向注意力机制使其天然支持运动编辑——只需在需要编辑的位置放置 `[MASK]` 令牌，模型即可自动填补缺失部分并保证与上下文的平滑过渡。对于上身编辑任务，训练时额外引入下身令牌的轻微噪声以增强鲁棒性，其训练损失为：

$$\mathcal{L}_{\sf up} = - \sum_{{\bf Y} \in \mathcal{D}} \left[ \sum_{{\sf Y} i \in [1, L]} \log p \left( y_i^{up} \mid Y_{\overline{{\bf M}}}^{up}, Y_{\overline{{\bf M}}}^{down}, W \right) \right]$$

即在给定部分掩码的上身令牌、含噪声的下身令牌及文本条件下，预测上身的原始令牌。这一设计使模型在推理时能够根据不同的文本指令编辑上身动作，同时保持下身运动的连贯性。

> **注意**：以上公式均来自论文 Section 3 和 Section 4 的明确描述，未进行任何外推或推导。

## 实验与关键发现

MMM 在文本驱动运动生成的主流基准上进行了系统评估，并针对其特有的掩码建模范式开展了多维消融实验。以下从生成质量、推理效率、运动编辑任务和关键设计选择四个维度展开分析。

### 文本驱动运动生成主结果

在 HumanML3D 测试集上，MMM 在所有核心指标上均取得最优或次优结果（Table 1）。具体而言，MMM 的 FID 达到 **0.089 ± 0.005**，较此前最优的自回归方法 **AttT2M**（0.112）降低 0.023，较运动空间扩散模型 **MDM**（0.544）降低超过 0.45。在语义对齐指标 R-Precision Top-1 上，MMM 达到 **0.515 ± 0.002**，优于 AttT2M 的 0.499；多模态距离 MM-Dist 为 **2.926 ± 0.007**，同样领先所有对比方法。值得注意的是，即使使用模型自身预测的运动长度（非真实长度），MMM 的 FID 仍保持 0.089，而多数基线方法在预测长度设定下性能显著下降。

![[assets/figures/papers/paper_list_l6_https_arxiv_org_abs_2312_03596/figures/008_Table_1.jpg]]
*Table 1: Comparison of text-conditional motion synthesis on HumanML3D [12] test set. For each metric, we repeat the evaluation 20 times and report the average with 95% confidence interval. The right arrow (→) indicates that the closer the result is to real motion, the better. Red and Blue indicate the best and the second best result. § reports results using ground-truth motion length*

在 KIT-ML 数据集上，MMM 延续了优势（Table 2），FID 达到 **0.429 ± 0.019**，优于隐空间扩散模型 **MLD**（0.463）和运动空间扩散模型 **MotionDiffuse**（0.688）。MM-Dist 为 **2.977 ± 0.019**，同样取得最优。这表明 MMM 的离散令牌化与掩码建模范式在不同规模的数据集上均具备良好的泛化性。

![[assets/figures/papers/paper_list_l6_https_arxiv_org_abs_2312_03596/figures/009_Table_2.jpg]]
*Table 2: Comparison of text-conditional motion synthesis on KIT-ML [24] test set. For each metric, we repeat the evaluation 20 times and report the average with 95% confidence interval. The right arrow (→) indicates that the closer the result is to real motion, the better. Red and Blue indicate the best and the second best result. § reports results using ground-truth motion length*

### 推理速度与质量权衡

推理速度是 MMM 的核心优势之一。在单块 NVIDIA RTX A5000 GPU 上，MMM 的平均每句推理时间（AITS）仅为 **0.081 秒**，而可编辑的运动空间扩散模型 **MDM** 需要 **28.112 秒**，加速约 347 倍（Table 7）。即便与不可编辑的隐空间扩散模型 **MLD**（0.246 秒）和自回归模型 **T2M-GPT**（0.564 秒）相比，MMM 仍保持显著速度优势。Figure 2 以散点图形式直观展示了 FID 与 AITS 的权衡关系：MMM 位于最接近原点的位置，即同时取得最佳生成质量和最快推理速度。

![[assets/figures/papers/paper_list_l6_https_arxiv_org_abs_2312_03596/figures/014_Table_7.jpg]]
*Table 7: Comparison of the inference speed and quality of generation on text-to-motion along with the editable capability of each model. ‘✓’ means editable while ‘✗’ is not and ‘−’ refers to has-capability but no application provided. We calculate the Average Inference Time per Sentence (AITS) on the test set of HumanML3D [12] without model or data loading parts. All tests are performed on a single NVIDIA RTX A5000*

![[assets/figures/papers/paper_list_l6_https_arxiv_org_abs_2312_03596/figures/002_Figure_2.jpg]]
*Figure 2: The motion generation quality (FID score) and speed (AITS) comparisons between MMM and SOTA methods on HumanML3D dataset. The model closer to the origin is better. MMM achieves the best FID score (0.08) and the highest speed (0.081 AITS), while preserving motion editability. “⃝” represents editibility and “×” otherwise. All tests are performed on a single NVIDIA RTX A5000*

### 运动编辑任务评估

MMM 的核心特色在于无需额外训练即可支持多种运动编辑任务。Table 3 报告了运动插值（Motion In-betweening）和上身编辑（Upper Body Editing）的定量结果。在有文本条件下，MMM 的运动插值 FID 达到 **0.0712**，而 MDM 的对应指标为 2.371，差距超过两个数量级；上身编辑任务中 MMM 的 FID 为 **0.0731**，同样大幅领先 MDM（1.144）。在无文本条件下，MMM 的插值 FID 为 0.104，上身编辑 FID 为 0.091，仍保持较高水准。

定性结果进一步印证了上述量化优势。Figure 7 展示了运动插值的帧级对比：MDM 在条件帧与生成帧的边界处（第 146–147 帧）出现明显的过渡不连续，而 MMM 生成的过渡自然流畅。Figure 6 的上身编辑对比显示，MMM 能够在保持下身运动不变的前提下，准确生成符合新文本描述的上身动作，而 MDM 的编辑结果存在上下身不协调的问题。

### 消融实验与关键设计选择

#### 训练掩码比率

Table 4 对比了不同训练掩码比率对生成质量的影响。均匀分布 U(0.3, 1.0) 取得最佳 FID（0.089）和 R-Precision Top-1（0.520），优于固定比率 0.15（FID 0.108）和 U(0.5, 1.0)（FID 0.098）。这表明训练阶段需要足够高的掩码比率来迫使模型学习双向上下文推理，同时保留少量未掩码令牌以提供必要的条件信息。

![[assets/figures/papers/paper_list_l6_https_arxiv_org_abs_2312_03596/figures/011_Table_4.jpg]]
*Table 4: Ablation results on the masking ratio during training*

#### 推理掩码调度与迭代次数

Table 5 和 Table 10 联合分析了推理阶段的掩码调度策略。采用余弦调度函数且迭代次数为 **10** 时，MMM 达到最佳速度-质量平衡（FID 0.089，AITS 0.081）。余弦调度在早期迭代中保留更多高置信度令牌，为后续预测提供丰富的上下文；随着迭代推进，掩码数逐步减少，模型在充分的双向条件下完成最终预测。相比之下，线性调度和平方根调度在相同迭代次数下 FID 略高（分别为 0.093 和 0.094）。迭代次数从 5 增至 10 时 FID 从 0.098 降至 0.089，但继续增至 20 时 FID 仅微降至 0.087 而 AITS 翻倍至 0.162 秒，说明 10 次迭代已接近性能饱和点。

#### Codebook 规模与稳定性

Table 6 显示，将 codebook 尺寸从 512×32 扩大至 **8192×32** 时，FID 从 0.108 降至 **0.075**，验证了大容量离散潜在空间对保留运动细节的积极作用。然而，大 codebook 面临训练崩塌风险。Table 8 和 Figure 8 表明，在第二阶段训练中每 **20 次迭代**重置一次 codebook 可有效避免崩塌，取得 FID 0.089；若每迭代都重置，FID 升至 0.102；若不重置，则出现严重崩塌（FID 恶化至 0.2 以上）。

#### 采样策略

Tables 11–13 考察了推理时的采样参数。温度采样中 **β=1** 取得最佳 FID（0.089），过高或过低的温度均导致质量下降。Top-K 采样在 K=100%（即保留全部令牌概率）时 FID 最优（0.089），Top-P 采样在 p=1.0 时同样最优。这表明 MMM 的并行解码过程本身已具备足够的确定性，过度截断采样反而引入偏差。

#### 交叉注意力层数

Table 9 揭示了一个有趣的权衡：将交叉注意力层数从 4 增至 8 时，R-Precision Top-1 从 0.515 提升至 0.521，但 FID 从 0.089 恶化至 0.101。这暗示更强的文本条件注入可能过度约束运动生成，损害运动的自然度。如何在语义对齐与运动真实性之间取得更优平衡，仍是开放问题。

### 失败模式与局限

尽管 MMM 在整体指标上表现优异，但在以下场景存在局限：对于超长单一文本描述（超过训练数据中 10 秒/196 帧的运动长度），模型在细粒度细节渲染上可能出现退化；上身编辑任务中，若不引入下身 [MASK] 令牌进行调节，上下身组合可能超出训练分布导致不协调（Figure 14 展示了掩码令牌的调节效果）；当前架构不支持多人交互式动作生成，这与领域内其他主流方法的局限一致。

## 定位与知识库关联

### 1. 范式定位：掩码生成式运动模型

MMM 的核心范式是将 BERT 式掩码语言建模思想迁移至 3D 人体运动生成领域。与当前主流的**扩散模型**（以 **MDM**、**MotionDiffuse** 为代表的运动空间扩散，以及以 **MLD** 为代表的隐空间扩散）和**自回归模型**（如 **T2M-GPT**、**AttT2M**）不同，MMM 采用条件掩码 Transformer 进行双向并行解码。这一范式选择直接决定了其在速度-质量-可编辑性三角中的独特位置：

- **运动空间扩散模型**（MDM 等）通过逐步去噪生成运动，天然支持扩散修补实现可编辑性，但推理需数百至上千步去噪迭代，速度极慢（MDM 单句平均推理时间 28.112 秒，见 Table 7）。
- **隐空间扩散模型**（MLD 等）将扩散过程压缩至低维隐空间以加速，但牺牲了直接在运动空间编辑的能力。
- **自回归模型**（T2M-GPT、AttT2M 等）按时间步顺序生成运动令牌，速度优于扩散模型，但单向注意力使其无法利用未来上下文进行双向编辑，且逐令牌生成仍存在累积误差。
- **MMM** 通过双向 Transformer 一次性感知所有位置上下文，在并行迭代解码中逐步预测高置信令牌，实现了比可编辑扩散模型快两个数量级的推理速度（AITS 0.081 秒），同时保持最优生成质量（HumanML3D 上 FID 0.089）。

### 2. 与基线方法的关键差异

#### 2.1 运动表征方式

| 方法 | 运动表征 | 编辑灵活性 |
|------|----------|------------|
| MDM | 原始运动数据（连续空间） | 扩散修补，需在连续空间操作 |
| MLD | 连续隐空间嵌入 | 不支持直接编辑 |
| T2M-GPT | 离散运动令牌（VQ-VAE） | 不支持双向编辑 |
| **MMM** | **离散运动令牌（VQ-VAE，codebook 8192×32）** | **[MASK] 占位即可编辑** |

MMM 的离散令牌化借鉴了 T2M-GPT 的思路，但采用了更大的 codebook（8192 vs. T2M-GPT 的 512）以保留更丰富的运动语义信息。Table 6 的消融实验表明，增大 codebook 尺寸至 8192×32 可将 FID 降至 0.075。

#### 2.2 生成与解码机制

MMM 的并行迭代解码是该工作的核心创新。与自回归模型的逐令牌顺序生成和扩散模型的逐步去噪不同，MMM 在推理时从全掩码序列出发，每轮迭代并行预测所有掩码位置，并按置信度保留高置信令牌，逐步减少掩码数量。这一机制的关键设计包括：

- **余弦掩码调度**：第 $t$ 次迭代掩码数 $n_M(t) = L \cdot \cos(\frac{1}{2}\pi \frac{t}{T_{dyn}})$，早期保留少量高置信令牌作为锚点，后期上下文丰富后大幅减少掩码（Appendix G）。
- **迭代次数与速度平衡**：Table 5 和 Table 10 显示，10 次迭代配合余弦调度达到最佳速度-质量平衡（FID 0.089, AITS 0.081），而线性或平方根调度在相同迭代次数下 FID 均更差。

#### 2.3 可编辑性的实现路径

MMM 的可编辑性源于训练-推理的一致性：训练时模型已见过各种随机掩码模式，推理时只需在待编辑位置放置 `[MASK]` 令牌，模型即可利用双向上下文自动填补。这与 MDM 的扩散修补机制有本质区别：

- **MDM** 需要在运动空间上对特定区域执行条件去噪，操作复杂且速度慢。
- **MMM** 的掩码占位编辑无需额外训练或推理流程修改，天然支持运动插值、上身编辑、长序列生成等任务。

在运动插值任务上，MMM 取得 FID 0.0712，而 MDM 为 2.371（Table 3），差距达两个数量级。Figure 7 的定性结果显示，MMM 在条件帧与生成帧之间的过渡（如第 146-147 帧）比 MDM 更平滑自然。

### 3. 适用边界与局限

#### 3.1 数据约束下的运动时长限制

MMM 的训练数据（HumanML3D 和 KIT-ML）中运动序列最长约 10 秒（196 帧）。对于异常长的单一文本描述，模型在细粒度细节渲染上可能面临挑战。论文提出可通过大语言模型将长文本分割为多个简洁提示词，利用 MMM 的长序列生成能力逐段生成并自动填补过渡（Figure 15），但这一方案依赖外部 LLM，且过渡段“幻觉”质量缺乏定量评估。

#### 3.2 多角色交互动作的缺失

当前 MMM 仅支持单人运动生成，不支持多人交互式动作（如双人舞蹈、打斗等）。这一局限同样是 MDM、MLD、T2M-GPT 等主流方法的共同瓶颈，反映了现有数据集的标注粒度不足。

#### 3.3 上身编辑的分布外问题

在上身编辑任务中，若不经特殊处理，上身与下身组合可能超出训练分布。论文通过在训练时对下身令牌施加轻微噪声（Equation 3 中的 $Y_{\overline{\mathbf{M}}}^{down}$）来缓解这一问题，但 Figure 14 显示下身 `[MASK]` 令牌仍会对上身生成产生不可忽略的影响，表明分布外鲁棒性仍有提升空间。

#### 3.4 Codebook 崩塌风险

VQ-VAE 训练中 codebook 崩塌是已知难点。MMM 采用 codebook 重置策略（每 20 次迭代重置死亡码本）来稳定训练（Table 8），但 Figure 8 显示若不重置，FID 和 R-Precision 会急剧恶化。这一策略的有效性是否泛化至更大规模数据集仍需验证。

### 4. 开放问题

1. **长文本自动分割与过渡质量保证**：如何利用大语言模型将超长文本描述自动分割为多个简洁提示词，并确保相邻提示词之间的过渡运动既自然又语义连贯？当前论文仅展示了定性结果（Figure 15），缺乏对过渡段质量的定量评估指标。

2. **多角色交互动作扩展**：如何扩展模型架构以支持多角色交互动作？可能的路径包括引入角色分离的令牌序列、设计交互注意力机制，或利用多模态条件（如空间关系描述）指导生成。

3. **Codebook 利用率与容量的平衡**：Table 6 显示增大 codebook 尺寸可降低 FID，但更大的 codebook 也意味着更高的崩塌风险和训练难度。是否存在更好的平衡策略（如层次化 codebook、动态扩展机制）以进一步降低 FID 并避免崩塌？

4. **交叉注意力机制优化**：Table 9 显示增加交叉注意力层数可提升 R-Precision Top-1（从 0.504 升至 0.515），但会恶化 FID（从 0.089 升至 0.108）。这种质量指标的 trade-off 暗示当前注意力融合机制可能引入了噪声——能否设计更优的文本-运动融合机制（如门控交叉注意力、层次化条件注入）以兼顾语义对齐和运动保真度？

5. **推理速度的进一步优化**：当前 10 次迭代的并行解码已取得 0.081 秒的 AITS，但每次迭代仍需完整前向传播。是否可以通过知识蒸馏、提前退出机制或缓存策略将推理压缩至更少迭代甚至单步生成？

## 原文 PDF

![[paperPDFs/CVPR_2024/MMM_Generative_Masked_Motion_Model.pdf]]
