---
title: "Stand-In: A Lightweight and Plug-and-Play Identity Control for Video Generation"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/Stand_In_A_Lightweight_and_Plug_and_Play_Identity_Control_for_Video_Generation.pdf
project_link: null
code_link: "https://github.com/WeChatCV/Stand-In"
aliases:
- Stand-In
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/image_and_video_generation
- topic/generative_models_diffusion
- topic/benchmarks_datasets_evaluation
core_operator: 受限自注意力（RSA）阻止图像查询关注视频键，保持参考图像身份静态；条件位置映射（CPM）为参考令牌分配独立的坐标空间以解耦几何相关性，二者协同实现身份信息的精准注入。
primary_logic: 利用预训练VAE将条件图像映射到与视频相同的潜在空间，并通过冻结时间步长（s_ref=0）维持其静态性，进而以极少的LoRA参数（1%）引入条件图像分支，在不大幅修改模型架构的前提下，通过专门的注意力机制实现身份控制。
claims:
- 在定量比较中，Stand-In的人脸相似度达到0.724，超越所有对比方法（最佳次优VACE-14B为0.647），同时自然度和提示遵循也名列前茅。
- 消融实验显示，将受限自注意力替换为普通自注意力导致人脸相似度从0.724骤降至0.422；将条件位置映射替换为共享位置映射导致人脸相似度从0.724降至0.536。
- Custom identity-preserving video generation test set 上 Face Similarity = 0.724
- Custom identity-preserving video generation test set 上 Naturalness = 3.922
---

# Stand-In: A Lightweight and Plug-and-Play Identity Control for Video Generation

> [!tip] 核心洞察
> 利用预训练VAE将条件图像映射到与视频相同的潜在空间，并通过冻结时间步长（s_ref=0）维持其静态性，进而以极少的LoRA参数（1%）引入条件图像分支，在不大幅修改模型架构的前提下，通过专门的注意力机制实现身份控制。

| 字段 | 内容 |
|------|------|
| 中文题名 | Stand-In：一种轻量级即插即用的视频生成身份控制框架 |
| 英文题名 | Stand-In: A Lightweight and Plug-and-Play Identity Control for Video Generation |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2508.07901) · [Code](https://github.com/WeChatCV/Stand-In) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/image_and_video_generation #topic/generative_models_diffusion #topic/benchmarks_datasets_evaluation |
| Method | Stand-In |
| Dataset | Custom identity-preserving video generation test set, User Study |

> [!tip] 效果简介
> - Custom identity-preserving video generation test set 上，Face Similarity 0.724 vs 0.647 (VACE-14B) (+0.077)；Naturalness 3.922 vs 3.828 (Phantom-14B) (+0.094)；Prompt Following 20.594 vs 20.591 (VACE-P1.3B) (+0.003)。
> - User Study 上，Face Similarity (subjective) 4.10 vs 3.87 (best competitor in Table 2) (+0.23)；Video Quality (subjective) 4.08 vs 3.84 (best competitor in Table 2) (+0.24)。

## 概要

身份保持的视频生成旨在根据给定的参考图像，生成在动态场景中保持人物身份一致性的视频。现有方法通常依赖全量微调（full fine-tuning）引入大量可训练参数，不仅计算开销大，还缺乏与其他AIGC工具（如风格化LoRA、姿态引导模块）的兼容性，难以在轻量级条件下实现高保真身份保持。

本文提出 **Stand-In**，一种轻量级、即插即用的身份控制框架。其核心思想是：利用预训练VAE将条件图像映射到与视频相同的潜在空间，并通过冻结时间步长（$s_{ref} = 0$）维持参考图像的静态性；在此基础上，仅引入约1%的LoRA参数构建条件图像分支，通过两个关键机制——**受限自注意力（Restricted Self-Attention, RSA）** 和**条件位置映射（Conditional Position Mapping, CPM）**——实现身份信息的精准注入，而无需大幅修改预训练视频生成模型的架构。

在定量评估中，Stand-In的人脸相似度达到0.724，超越所有对比方法（最佳次优VACE-14B为0.647），同时自然度和提示遵循指标也名列前茅（Table 1）。用户主观评估进一步验证了其在人脸相似度（4.10）和视频质量（4.08）上的优势（Table 2）。消融实验表明，RSA和CPM是性能的关键保障：移除RSA导致人脸相似度从0.724骤降至0.422，替换CPM则降至0.536（Table 3）。

在方法谱系与知识库定位上，Stand-In属于**基于预训练视频扩散模型的身份注入方法**，与以下代表性工作形成对比：**ID-Animator**（He et al., arXiv 2024）和**ConsistID**（Yuan et al., CVPR 2025）采用全量微调策略；**VACE**（Jiang et al., arXiv 2025）和**Phantom**（Liu et al., arXiv 2025）探索了参考网络或适配器方案；**Hunyuan-Custom**（Hu et al., arXiv 2025）则面向定制化生成。Stand-In的独特之处在于以极少参数实现即插即用的身份控制，同时保持与现有AIGC生态的兼容性。

### 身份保持视频生成的现状与瓶颈

文本到视频生成领域在扩散模型（Diffusion Models）与DiT（Diffusion Transformer）架构的推动下取得了显著进展，但在**身份保持（Identity Preservation）**这一关键任务上仍面临严峻挑战。给定一张参考人物图像，要求模型生成一段视频，使其中的人物在面部特征、体型、发型等身份属性上与参考图像高度一致，同时保持视频的自然度、时序连贯性和对文本提示的忠实遵循。这一任务的核心难点在于：模型必须在生成过程中精确注入参考身份信息，同时避免破坏预训练模型原有的生成先验。

现有方法普遍采用**全量微调（Full Fine-tuning）**或大规模参数适配的策略。例如，**ID-Animator**（He et al., arXiv 2024）和**ConsistID**（Yuan et al., CVPR 2025）等方法需要训练大量参数来实现身份嵌入；**VACE**（Jiang et al., arXiv 2025）和**Phantom**（Liu et al., arXiv 2025）等基于14B参数规模模型的方法虽然性能有所提升，但训练成本高昂。更为关键的是，这些方法往往**缺乏与其他AIGC工具的兼容性**——它们通常以侵入式方式修改基础模型，导致难以与社区中广泛使用的风格化LoRA、姿态引导ControlNet等即插即用模块协同工作。

从定量角度看，现有方法在面部相似度（Face Similarity）指标上的表现仍有明显提升空间。据Table 1数据显示，当前最佳对比方法VACE-14B的面部相似度仅为0.647，而自然度（Naturalness）和提示遵循（Prompt Following）之间也存在难以同时兼顾的权衡。

### 核心瓶颈的因果分析

上述困境的深层原因可归结为两个相互关联的技术瓶颈：

1. **身份信息注入与生成先验的冲突**：当参考图像令牌与视频令牌在自注意力机制中无差别交互时，图像查询（Query）会关注视频键（Key），导致原本应保持静态的身份表示被视频动态信息污染；同时视频查询也会将注意力弥散到参考图像的背景区域，引发场景漂移（如Figure 5所示，普通自注意力下注意力图扩散到背景，生成结果偏向花园场景而非保持人物身份）。

2. **位置编码共享导致的虚假空间关联**：若参考令牌与视频令牌共享同一坐标网格，模型会错误地建立参考人物的空间位置与视频场景之间的几何相关性，破坏预训练位置先验，导致场景不稳定（如Figure 6所示，共享位置映射下场景结构出现扭曲）。

### 本文动机与设计哲学

针对上述瓶颈，本文提出**Stand-In**框架，其核心设计哲学是：**以最小参数代价实现身份控制，同时保持基础模型的完整性和即插即用能力**。具体而言，Stand-In仅引入约1%的额外可训练参数（通过LoRA rank 128作用于条件图像分支的QKV投影），仅需2000个训练样本对，即可实现面部相似度0.724的SOTA性能（超越VACE-14B的0.647达+0.077，如Table 1所示）。

这一设计选择背后的因果逻辑在于：与其重新训练或大幅修改基础模型，不如利用预训练VAE将条件图像映射到与视频相同的潜在空间，并通过冻结时间步长（$s_{ref} = 0$）维持其静态性。在此基础上，通过两个轻量级但关键的机制——**受限自注意力（Restricted Self-Attention, RSA）**和**条件位置映射（Conditional Position Mapping, CPM）**——实现身份信息的精准注入与空间解耦，从而在不破坏预训练先验的前提下达成高保真身份保持。

这种即插即用的设计使得Stand-In能够无缝集成到视频人脸交换、风格化LoRA扩展、姿态引导生成等多种下游应用中（如Figure 1、Figure 11-13所示），填补了现有方法在**轻量级、高兼容性身份控制**方面的缺口。

## 核心方法与创新机理

Stand-In 的核心创新在于**以极低的参数代价（约1%额外参数）实现高保真身份保持**，其关键在于对预训练视频生成模型中自注意力机制与位置编码策略的**双重重构**，而非依赖全量微调或引入繁重的身份编码器。

### 创新动机：轻量即插即用的身份控制瓶颈

现有身份保持视频生成方法（如 **ID-Animator** (He et al., arXiv 2024)、**ConsistID** (Yuan et al., CVPR 2025)、**VACE** (Jiang et al., arXiv 2025)）通常需要大量训练参数（Figure 2 中以气泡大小表示），且缺乏与其他 AIGC 工具的兼容性。核心瓶颈在于：如何在不大幅修改预训练模型架构的前提下，将静态参考图像的身份信息精准注入动态视频生成过程，同时保持参考表示不受视频内容污染。

### 关键创新点一：受限自注意力（Restricted Self-Attention, RSA）

**Changed Slot：** 自注意力机制
- **Baseline 做法：** 普通自注意力（Vanilla Self-Attention），图像查询（Query）可自由关注视频键（Key），导致参考图像特征被视频内容稀释，身份信息向背景区域扩散（Figure 5 上排）。
- **Stand-In 做法：** 受限自注意力，**显式阻止图像查询关注视频键**，而视频查询可同时关注视频键和图像键。图像令牌仅对自身执行自注意力（公式 3），保持参考表示静态；视频令牌则通过拼接后的键值矩阵融合身份信息（公式 4）。

**因果机制：** 这种非对称的信息流设计确保了身份信息从图像向视频的单向注入，同时保护参考图像不受视频动态内容的污染。消融实验（Table 3）提供了决定性证据：将 RSA 替换为普通自注意力后，人脸相似度从 **0.724 骤降至 0.422**，自然度也同步下降。

### 关键创新点二：条件位置映射（Conditional Position Mapping, CPM）

**Changed Slot：** 位置嵌入策略
- **Baseline 做法：** 共享位置映射（Shared Position Mapping），参考令牌与视频令牌共享同一坐标网格，产生虚假空间相关性。
- **Stand-In 做法：** 条件位置映射，为参考令牌分配**独立的、与视频不重叠的空间坐标** $[H_V, H_V+H_I) \times [W_V, W_V+W_I)$，并固定时间索引为 -1。图像和视频分别应用各自的 3D 旋转位置编码（RoPE）（公式 1 和公式 2）。

**因果机制：** 通过几何上解耦参考令牌与视频令牌的坐标空间，CPM 消除了两者之间的虚假空间关联，同时保留了预训练模型的位置先验。这使得参考图像作为全局身份先验稳定注入，而非被误认为视频中的局部区域。消融实验（Table 3）表明：将 CPM 替换为共享位置映射后，人脸相似度从 **0.724 降至 0.536**，自然度从 **3.922 降至 3.755**。Figure 6 的定性对比进一步显示，CPM 能产生更稳定的场景，避免共享位置映射下的空间错乱。

### 协同效应与设计哲学

RSA 与 CPM 并非孤立运作，二者协同实现了身份信息的精准注入：
- **RSA** 从注意力流层面切断图像→视频的逆向污染路径，确保参考表示的静态性；
- **CPM** 从几何层面消除位置编码带来的虚假关联，为注意力计算提供正确的空间先验。

二者的共同基础是一个轻量级的**条件图像分支**：利用预训练 VAE 将参考图像映射到与视频相同的潜在空间，并通过冻结时间步长 $s_{ref} = 0$ 维持其时间不变性。该分支仅需为图像令牌的 QKV 投影添加 LoRA 模块（秩 128），参数量极小。这种设计使得 Stand-In 能够以即插即用的方式集成到多种应用中（如视频人脸交换、风格化生成等），同时保持与现有 DiT 模型的兼容性。

Stand-In 的整体 pipeline 围绕一个核心设计展开：**在不修改预训练视频生成模型主体结构的前提下，引入一个极轻量的条件图像分支，通过专门的注意力机制实现高保真身份控制**。其输入为一张参考身份图像和一段文本提示，输出为保持该身份一致的视频。

### 数据流与模块协作

整个框架的数据流可分为三个关键阶段：

**1. 统一潜在空间映射**

参考图像与视频初始噪声通过**同一个预训练 VAE 编码器**映射到共享的潜在空间。这一策略避免了引入额外的图像编码器（如 CLIP 图像编码器），直接复用视频生成模型已有的 VAE，确保图像令牌与视频令牌在特征维度上天然对齐。映射后的图像令牌与视频潜在令牌沿序列维度拼接，共同送入后续的 DiT（Diffusion Transformer）模块进行处理。

**2. 条件图像分支与受限自注意力（RSA）**

进入 DiT 模块后，图像令牌和视频令牌分别通过独立的 QKV 投影计算查询、键和值矩阵。其中，图像令牌的 QKV 投影额外附加了**低秩适配（LoRA）模块**（秩为 128），这是整个框架中唯一需要训练的参数，约占总参数的 1%。

核心的身份注入机制由**受限自注意力（Restricted Self-Attention, RSA）**实现：
- **图像令牌**：仅对自身的键和值执行自注意力，其查询被显式禁止关注视频令牌。这一约束确保了参考图像的表征在整个去噪过程中保持**静态**——因为参考图像的去噪时间步被固定为 $s_{ref}=0$，不受视频去噪进度的影响。
- **视频令牌**：其查询同时关注拼接后的视频键/值**和**图像键/值，从而在每一层 DiT 中持续从静态的图像表征中提取身份信息。

这种非对称的注意力设计是 Stand-In 身份保持能力的关键：图像侧作为稳定的“身份锚点”，视频侧则从中汲取身份特征，同时不反向污染图像表征。

**3. 条件位置映射（CPM）**

为了进一步解耦图像令牌与视频令牌之间的空间关系，Stand-In 引入了**条件位置映射（Conditional Position Mapping, CPM）**。在应用 3D 旋转位置编码（RoPE）时，图像令牌被分配到与视频坐标空间**不相交**的独立区域——空间坐标范围为 $[H_V, H_V+H_I) \times [W_V, W_V+W_I)$，时间索引固定为 $-1$。这一设计避免了图像令牌因共享视频坐标网格而产生虚假的空间相关性，同时保留了预训练模型的原始位置先验。

CPM 与 RSA 的协同关系可概括为：RSA 控制**注意力流向**（图像查询不关注视频），CPM 控制**几何关系**（图像令牌拥有独立的坐标空间），二者共同确保身份信息精准注入而不干扰视频生成的时空一致性。

### 推理效率优化

得益于 RSA 的设计，图像令牌的键和值矩阵在整个去噪过程中保持不变（因为图像侧不受视频去噪进度影响）。因此，Stand-In 在推理时可采用 **KV 缓存**策略：仅计算一次图像键值矩阵并缓存复用，额外推理时间仅增加约 2.3%，浮点运算量增加约 0.07%，几乎不影响生成效率。

### 即插即用特性

由于条件图像分支完全基于 LoRA 模块构建，Stand-In 天然兼容其他基于 DiT 架构的模型和工具。这一设计使其可以作为“身份控制插件”无缝集成到各类下游应用中，如视频人脸交换、风格化 LoRA 叠加、姿态引导视频生成等，无需对宿主模型进行额外修改。

### 补充图表

![[assets/figures/papers/paper_list_l936_https_arxiv_org_abs_2508_07901/figures/003_Figure_3.jpg]]
*Figure 3: The overview of our identity-preserving text-to-video generation framework. We introduce a conditional image branch alongside the original video branch. Given the conditional image, the VAE encoder maps it into tokens, which are concatenated with the video latent tokens and then sent to the DiT. Within the DiT blocks, identity information is incorporated into the video features through restricted self-attention*

Stand-In 的身份控制能力由三个紧密协作的核心模块实现：**条件图像分支与 LoRA 适配**、**受限自注意力（Restricted Self-Attention, RSA）** 以及 **条件位置映射（Conditional Position Mapping, CPM）**。这些模块共同解决了“如何以极少的可训练参数将静态参考图像的身份信息精准注入动态视频生成过程”这一核心挑战。

### 3.1 条件图像分支与潜在空间对齐

Stand-In 复用了预训练视频生成模型中的 VAE 编码器，将条件参考图像直接映射到与视频相同的潜在空间。这一设计避免了引入额外的图像编码器，确保了潜在特征在语义和分布上的一致性。映射后的图像令牌与视频潜在令牌沿序列维度拼接，共同送入后续的 DiT（Diffusion Transformer）块进行处理。

为保持参考图像的静态身份属性，图像令牌的去噪时间步被固定为零：

$$s_{ref} = 0$$

这意味着参考图像在扩散过程中始终被视为无噪声的干净信号，其潜在表示在生成过程中保持不变，从而为视频分支提供稳定的身份锚点。

### 3.2 受限自注意力（RSA）

在标准的 DiT 自注意力层中，所有令牌（包括图像和视频）会进行全连接的注意力交互。然而，这种无约束的交互会导致两个问题：其一，图像令牌的表示会被视频上下文“污染”，丧失静态身份保真度；其二，视频令牌的注意力可能过度扩散到图像的背景区域，而非聚焦于人脸身份特征（如 Figure 5 所示）。

RSA 通过显式约束注意力流向来解决上述问题。其核心操作可形式化为以下步骤：

**步骤一：独立投影。** 对视频令牌和图像令牌分别计算 Query、Key 和 Value 矩阵。图像令牌的 QKV 投影额外引入低秩适配（LoRA），秩设为 128，仅作用于图像分支的 QKV 投影层。这使得可训练参数量仅占骨干模型的约 1%。

**步骤二：位置编码。** 分别对图像和视频的 Query 与 Key 应用条件位置映射（详见 3.3 节），得到带位置信息的 $Q_I'$、$K_I'$ 和 $Q_V'$、$K_V'$。

**步骤三：受限注意力计算。** 注意力计算被拆分为两个独立路径：

- **图像自注意力（保持静态）：** 图像令牌仅对自身执行自注意力，其输出不受视频令牌影响：

$$\mathrm{Out}_{I} = \mathrm{Attention}(Q_{I}', K_{I}', V_{I})$$

- **视频受限自注意力（融合身份）：** 视频令牌的 Query 对拼接后的视频 Key、Value 和图像 Key、Value 执行注意力，从而从参考图像中提取身份信息：

$$\mathrm{Out}_{V} = \mathrm{Attention}(Q_{V}', [K_{V}', K_{I}'], [V_{V}, V_{I}])$$

这一设计的关键在于：图像查询被禁止关注视频键，因此参考图像的表示始终保持静态；而视频查询可以同时关注视频和图像键，从而在生成过程中持续获取身份线索。消融实验（Table 3）证实，将 RSA 替换为普通自注意力（VSA）会导致人脸相似度从 0.724 骤降至 0.422，验证了该约束的必要性。

### 3.3 条件位置映射（CPM）

在 Transformer 架构中，位置编码为令牌提供了空间和时序的结构先验。如果简单地将参考图像令牌与视频令牌共享同一坐标网格（共享位置映射，SPM），会引入虚假的空间相关性——模型可能错误地将图像中的人脸位置与视频中某空间区域的语义绑定，导致场景扭曲或身份漂移。

CPM 为参考图像令牌分配一个与视频坐标空间**不相交**的独立坐标空间。具体而言，视频令牌占据坐标范围 $[0, H_V) \times [0, W_V)$，而图像令牌被映射到 $[H_V, H_V + H_I) \times [W_V, W_V + W_I)$，并在时间维度上分配固定的时间索引 -1。这一几何分离使得：

- 图像令牌在位置编码层面与视频令牌完全解耦，保留了预训练模型的位置先验；
- 参考图像作为全局的身份先验存在，其空间坐标不与视频中的任何局部区域产生虚假关联。

CPM 通过 3D 旋转位置编码（RoPE）实现。对图像令牌应用图像坐标 $p_I$：

$$Q_{I}' = Q_{I} \cdot p_{I}, \quad K_{I}' = K_{I} \cdot p_{I}$$

对视频令牌应用视频坐标 $p_V$：

$$Q_{V}' = Q_{V} \cdot p_{V}, \quad K_{V}' = K_{V} \cdot p_{V}$$

消融实验（Table 3）显示，将 CPM 替换为 SPM 会导致人脸相似度从 0.724 降至 0.536，自然度从 3.922 降至 3.755。Figure 6 的定性对比进一步表明，CPM 能产生更稳定的场景结构，避免 SPM 下的背景畸变。

![[assets/figures/papers/paper_list_l936_https_arxiv_org_abs_2508_07901/figures/007_Figure_6.jpg]]
*Figure 6: Effect of Conditional Position Mapping (CPM). Compared with Shared Postion Mapping, our CPM, where the reference tokens are mapped to a disjoint spatial space, better preserves the pretrained positional prior and yields more stable scenes*

### 3.4 推理效率优化：KV 缓存

由于图像令牌的 Key 和 Value 矩阵在生成过程中保持不变（得益于 RSA 的静态约束），Stand-In 在推理时对图像分支的 K、V 矩阵进行缓存，避免重复计算。这使得推理时间仅增加约 2.3%，FLOPs 仅增加约 0.07%，在保持高保真身份控制的同时实现了极低的推理开销。

## 实验与关键发现

### 定量评估与SOTA对比

Stand‑In在身份保持视频生成的三个关键指标上均达到或超越了现有最优方法。在自动评估中（Table 1），其人脸相似度（Face Similarity）达到**0.724**，显著高于次优方法VACE‑14B的0.647（+0.077）；自然度（Naturalness）为**3.922**，优于Phantom‑14B的3.828（+0.094）；提示遵循（Prompt Following）为**20.594**，与VACE‑P1.3B基本持平。值得注意的是，Stand‑In仅需训练约1%的额外参数（以LoRA形式注入）和2000个训练对，而对比方法如VACE、Phantom等通常需要全量微调或大量可训练参数。Figure 2以气泡图形式直观展示了这一权衡：Stand‑In在Face Similarity和Naturalness两个维度上均处于右上角最优区域，而气泡面积（参数量）远小于其他方法。

![[assets/figures/papers/paper_list_l936_https_arxiv_org_abs_2508_07901/figures/008_Table_1.jpg]]
*Table 1: Quantitative comparison with state-of-the-art identity-preserving video generation methods. We evaluate across three key metrics: Face Similarity, Naturalness, and Prompt Following. For all metrics, higher values indicate better performance. The best and second-best results in each column are highlighted in bold and underlined, respectively*

用户主观评估（Table 2）进一步验证了上述结论。在人脸相似度上，Stand‑In获得**4.10**分（满分5分），优于最佳对比方法的3.87分；在视频质量上，Stand‑In获得**4.08**分，优于最佳对比方法的3.84分。这表明用户对Stand‑In生成视频的身份一致性和整体质量均有显著偏好。

![[assets/figures/papers/paper_list_l936_https_arxiv_org_abs_2508_07901/figures/011_Table_2.jpg]]
*Table 2: User study results for subjective evaluation. The best and second-best results in each column are highlighted in bold and underlined, respectively*

### 消融实验：核心组件的因果验证

Table 3的消融实验直接验证了受限自注意力（RSA）和条件位置映射（CPM）的因果作用。

- **移除RSA，替换为普通自注意力（VSA）**：人脸相似度从0.724骤降至**0.422**，降幅达41.7%。这一剧烈退化表明，若允许图像查询（Query）自由关注视频键（Key），参考图像的表征会被视频上下文污染，丧失静态身份锚点的作用。Figure 5的注意力图可视化提供了定性佐证：VSA下注意力扩散到背景区域，生成结果偏向场景描述而非身份保持；RSA则将注意力集中于面部区域。
- **移除CPM，替换为共享位置映射（SPM）**：人脸相似度降至**0.536**，自然度从3.922降至3.755。CPM通过为参考令牌分配与视频坐标不相交的空间位置（$[H_V, H_V+H_I) \times [W_V, W_V+W_I)$），解耦了图像令牌与视频令牌之间的虚假几何相关性。SPM下，参考令牌被迫共享视频坐标网格，破坏了预训练位置先验，导致身份信息注入不稳定（Figure 6）。

两个组件同时移除（即VSA+SPM）时，人脸相似度进一步降至0.422，自然度降至3.755，相当于完全丧失了身份保持能力。

### 效率分析

Stand‑In的轻量级设计在推理效率上具有显著优势。通过KV缓存机制，图像令牌的Key和Value矩阵仅需计算一次并在所有去噪步中复用，推理时间仅增加**2.3%**，FLOPs仅增加**0.07%**。这一特性使得Stand‑In可以无缝集成到现有DiT基视频生成流程中，无需额外的推理预算。

### 泛化性与应用验证

尽管仅用2000个训练对和约1%的额外参数训练，Stand‑In展现出良好的泛化能力。Figure 9展示了模型对不同种族和年龄群体的未见个体的生成结果，身份保持效果一致。Figure 10进一步证明方法可泛化至非真人主体（如卡通角色、动物等）。在应用层面，Stand‑In的即插即用设计使其可直接与姿态引导（Figure 11）、视频人脸交换（Figure 12）和风格化LoRA（Figure 13）等下游模块结合，无需额外训练或架构修改。

![[assets/figures/papers/paper_list_l936_https_arxiv_org_abs_2508_07901/figures/015_Figure_11.jpg]]
*Figure 11: Comparison on pose-guided video generation against VACE*

![[assets/figures/papers/paper_list_l936_https_arxiv_org_abs_2508_07901/figures/016_Figure_12.jpg]]
*Figure 12: Application of our model in video face swapping*

![[assets/figures/papers/paper_list_l936_https_arxiv_org_abs_2508_07901/figures/017_Figure_13.jpg]]
*Figure 13: Our model applied with stylization LoRA*

### 公平性说明

论文提及训练数据集涵盖不同种族、年龄和性别，但未进行专门的公平性或偏见定量评估。因此，模型在不同人口统计子群上的性能一致性仍有待独立验证。

### 补充图表

![[assets/figures/papers/paper_list_l936_https_arxiv_org_abs_2508_07901/figures/018_Table_3.jpg]]
*Table 3: Ablation study on the core components of our method. Replacing Restricted Self-Attention (RSA) with Vanilla Self-Attention (VSA) or Conditional Position Mapping (CPM) with Shared Position Mapping (SPM) degrades both Face Similarity and Naturalness*

![[assets/figures/papers/paper_list_l936_https_arxiv_org_abs_2508_07901/figures/002_Figure_2.jpg]]
*Figure 2: Comparison with SOTA identity-preserving video generation methods. The size of bubbles represents the number of need-to-train parameters for identity preservation. Our approach achieves the highest performance in both face similarity and naturalness, while utilizing the fewest parameters*

![[assets/figures/papers/paper_list_l936_https_arxiv_org_abs_2508_07901/figures/001_Figure_1.jpg]]
*Figure 1: Given a reference image, our method generates videos with strong identity preservation. Furthermore, the framework’s plug-andplay design enables seamless integration into diverse applications for enhanced identity consistency*

## 定位与知识库关联

### 1. 任务定位与核心瓶颈

Stand-In 面向**身份保持的文本到视频生成**任务，其核心挑战在于：给定一张参考人脸图像，生成一段保持该人物身份一致性的视频，同时保证视频的自然度与对文本提示的遵循能力。

该领域的关键瓶颈并非模型对身份特征的提取能力不足，而是**现有方法在身份注入过程中需要大量可训练参数（全量微调或大规模适配器），且缺乏与其他AIGC工具的即插即用兼容性**。这导致两个直接后果：训练成本高（需要大量配对数据），以及难以融入已有的视频生成生态（如图像动画、风格化、人脸交换等下游应用）。Stand-In 的因果调节变量正是围绕这一瓶颈展开：通过受限自注意力（RSA）和条件位置映射（CPM）两个轻量级机制，在仅引入约1%可训练参数（LoRA rank 128，仅作用于图像令牌的QKV投影）的条件下，实现高保真身份控制。

### 2. 与现有方法的关系与差异

#### 2.1 对比基线方法

论文将 Stand-In 与以下代表性身份保持视频生成方法进行了系统对比：

- **ID-Animator** (He et al., arXiv 2024)：基于身份适配器的视频生成方法，需要训练额外的身份编码模块。
- **ConsistID** (Yuan et al., CVPR 2025)：通过身份一致性约束进行视频生成，侧重时序稳定性。
- **VACE** (Jiang et al., arXiv 2025)：多功能的视频编辑与生成框架，支持身份保持作为子任务，参数量较大（14B级别）。
- **Phantom** (Liu et al., arXiv 2025)：面向身份保持的视频生成方法，同样在14B参数量级上运行。
- **Hunyuan-Custom** (Hu et al., arXiv 2025)：基于混元大模型的定制化视频生成方案。

从定量对比（Table 1）来看，Stand-In 在人脸相似度上达到 **0.724**，显著超越最佳对比方法 VACE-14B 的 0.647（+0.077）；在自然度上以 3.922 超过 Phantom-14B 的 3.828；在提示遵循上与 VACE-P1.3B 基本持平（20.594 vs 20.591）。Figure 2 的气泡图进一步揭示了 Stand-In 的关键优势：**以最少的可训练参数量（约1%），在身份相似度和自然度两个维度上同时达到最优**，形成了明显的帕累托前沿。

#### 2.2 方法谱系中的位置

从技术路线来看，身份保持视频生成方法可大致分为两类：

1. **身份编码器注入路线**：通过预训练的人脸识别模型（如 ArcFace）提取身份嵌入，再将其注入到视频生成主干网络中。这类方法通常需要训练专门的身份编码器或交叉注意力适配器，参数量较大。ID-Animator、ConsistID 等属于此路线。

2. **参考图像直连路线**：直接将参考图像的潜在表示与视频潜在表示在扩散模型的去噪过程中进行交互。Stand-In 属于此路线，其独特之处在于：
   - 利用预训练VAE将参考图像映射到与视频相同的潜在空间，避免了额外的编码器训练；
   - 通过**冻结参考图像的时间步长**（$s_{ref} = 0$）维持其静态性，确保身份信息不被去噪过程破坏；
   - 以受限自注意力（RSA）替代普通自注意力，**显式阻止图像查询关注视频键**，从而保持参考表示的独立性；
   - 以条件位置映射（CPM）为参考令牌分配**与视频坐标空间不相交的独立坐标区域**（$[H_V, H_V+H_I) \times [W_V, W_V+W_I)$，时间索引固定为-1），解耦空间相关性。

这种设计使得 Stand-In 在方法谱系中占据了一个特殊位置：它既不是全量微调方案（参数量极小），也不是完全无训练的零样本方案（需要少量LoRA训练），而是一种**最小侵入性的即插即用适配方案**。

### 3. 适用边界与局限

#### 3.1 已验证的适用边界

从论文的实验证据来看，Stand-In 的适用边界已得到以下验证：

- **跨身份泛化**：Figure 9 展示了模型对未见过的普通个体（不同种族、年龄）的泛化能力，仅用2000对训练数据即实现了较好的身份保持。
- **非真人主体**：Figure 10 表明模型对非真人主体（如卡通角色、动物等）也具有一定泛化性。
- **下游应用兼容**：Figure 11-13 展示了与姿态引导生成（与VACE对比）、视频人脸交换、风格化LoRA的即插即用集成能力。

#### 3.2 已知局限

论文中未明确列出方法局限性的专门讨论章节，但可从实验设计和消融结果中推断以下边界：

- **注意力机制的刚性约束**：RSA 通过硬性阻止图像查询关注视频键来保持身份静态性，这种设计在身份保持上效果显著（消融实验显示移除RSA后人脸相似度从0.724骤降至0.422），但可能在某些需要参考图像与视频内容深度融合的场景（如大幅度姿态变化、遮挡等）中限制灵活性。**此推断需要手动验证**。

- **位置映射的几何假设**：CPM 将参考令牌映射到与视频坐标不相交的空间区域，这一设计依赖预训练位置先验的保持。当视频分辨率或长宽比与训练分布差异较大时，位置映射的有效性可能下降。**论文未对此进行消融验证**。

- **公平性与偏见评估缺失**：论文虽提及训练数据包含不同种族、年龄和性别，但未进行专门的公平性/偏见定量评估。模型在不同人口统计群体上的身份保持一致性尚未得到系统验证。

### 4. 开放问题

基于论文的分析结果，以下问题值得后续研究关注：

1. **极端姿态与遮挡下的身份保持**：RSA 的静态身份表示策略在面部大幅度旋转、遮挡或极端光照条件下是否仍能保持高保真度？当前实验未专门覆盖此类困难样本。

2. **多身份同时控制**：Stand-In 的设计目前针对单张参考图像的单身份保持，扩展到多人场景时，多个条件图像分支之间的注意力交互和位置映射策略需要重新设计。

3. **长视频生成中的身份漂移**：随着视频时长增加，身份信息是否会出现渐进漂移？CPM 的固定时间索引（-1）策略在长时序上的有效性需要进一步验证。

4. **与更强基座模型的适配**：Stand-In 的即插即用设计理论上兼容其他 DiT 架构的视频生成模型，但在不同基座模型（如更大规模或不同训练策略的模型）上的迁移效果和最优LoRA配置仍需探索。

## 原文 PDF

![[paperPDFs/CVPR_2026/Stand_In_A_Lightweight_and_Plug_and_Play_Identity_Control_for_Video_Generation.pdf]]
