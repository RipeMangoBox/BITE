---
title: "HERO: Human Reaction Generation from Videos"
type: paper
paper_level: A
venue: ICCV
year: 2025
pdf_ref: paperPDFs/ICCV_2025/HERO_Human_Reaction_Generation_from_Videos.pdf
project_link: https://jackyu6.github.io/HERO
code_link: null
aliases:
- HERO
tags:
- ICCV_2025
- topic/vision_multimodal_applications
- topic/generative_models_diffusion
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: 从 RGB 视频中同时提取全局语义和逐帧关键帧信息以精细化交互意图的能力，以及持续注入帧级动态视觉特征来指导反应生成。
primary_logic: 通过全局-局部表示交叉注意力，模型不再简单平均池化所有帧，而是根据全局视频语义动态加权每一帧，从而提炼出更准确的交互意图；再利用意图条件自注意力和运动-帧交叉注意力，将交互意图与视频动态细节充分融入反应合成。
claims:
- HERO 在 ViMo 测试集上取得了当前最佳的 FID (0.427) 和多样性 (7.801)，显著优于重实现的自回归、扩散和掩码生成基线。
- 移除交互意图提取 (IIE) 或动态信息利用 (DIE) 分别导致 FID 从 0.427 升至 0.535 和 0.521，证明两者对生成分布接近真实分布至关重要。
- 用户研究显示，HERO 生成的动作在运动质量和反应合理性上均获得最高分（除真实数据外）。
- ViMo test set 上 FID↓ = 0.427±0.014
---

# HERO: Human Reaction Generation from Videos

> [!tip] 核心洞察
> 通过全局-局部表示交叉注意力，模型不再简单平均池化所有帧，而是根据全局视频语义动态加权每一帧，从而提炼出更准确的交互意图；再利用意图条件自注意力和运动-帧交叉注意力，将交互意图与视频动态细节充分融入反应合成。

| 字段 | 内容 |
|------|------|
| 中文题名 | HERO：从视频生成人类反应 |
| 英文题名 | HERO: Human Reaction Generation from Videos |
| 会议/期刊 | ICCV 2025 |
| Links | [Project](https://jackyu6.github.io/HERO) |
| Topic | #topic/vision_multimodal_applications #topic/generative_models_diffusion #topic/vision_multimodal_applications/image_and_video_generation |
| Method | HERO |
| Dataset | ViMo test set |

> [!tip] 效果简介
> - ViMo test set 上，FID↓ 0.427±0.014 vs 0.856±0.015 (MoMask) (-0.429)；Diversity→ 7.801±0.061 vs 7.721±0.081 (T2M-GPT) (+0.080)。

## 概要

**问题瓶颈**：现有的人类反应生成方法依赖结构化的人体运动序列（如 3D 骨架数据）作为输入，将交互类别限制在人与人之间，且缺失表情与情感信息，无法支持更广泛的人与动物、场景交互以及情绪驱动的反应生成。

**核心方法**：HERO 直接从 RGB 视频生成 3D 人类反应动作。其关键机制包括：(1) **交互意图提取 (IIE)**——通过全局-局部表示交叉注意力，以全局视频语义动态加权每一帧，提炼精细的交互意图；(2) **动态信息利用 (DIE)**——在生成过程中持续计算运动-帧交叉注意力，使模型充分利用视频的逐帧动态细节。模型管道由视频编码器（TC-CLIP）、运动 VQ-VAE 和掩码 Transformer 反应生成模块组成。

**主要结果**：在 ViMo 测试集上，HERO 取得当前最佳的 FID (0.427) 和多样性 (7.801)，显著优于重实现的自回归、扩散和掩码生成基线（如 MDM、MLD、T2M-GPT、BAMM、MoMask）。消融实验表明，移除 IIE 或 DIE 分别使 FID 升至 0.535 和 0.521，验证了两者对生成质量的关键作用。用户研究亦显示 HERO 在运动质量和反应合理性上获最高评分。

**方法定位**：HERO 属于视频条件驱动的掩码生成式人体运动合成方法，其核心创新在于将交互意图提取与动态信息利用解耦并显式建模，区别于以往仅使用全局平均池化特征的基线方案。

### 问题背景

生成逼真的人类反应是构建沉浸式虚拟世界、具身智能体和人机交互系统的核心能力。当一个人接收到来自他人、动物或环境的动作刺激时，其自然反应不仅取决于动作本身的运动学特征，还深受刺激者的表情、情绪以及交互上下文的影响。然而，现有的人类运动生成研究主要关注基于文本描述或结构化骨架序列的单向动作合成，对于需要从动态视觉输入中理解交互意图并生成相应反应的任务，探索极为有限。

### 现有方法的缺口

此前的人体运动生成方法存在两个根本性限制，使其难以直接应用于反应生成任务。

**输入模态的结构化依赖。** 绝大多数方法以 3D 人体骨架序列作为输入条件，这从根本上将交互类别限定在人与人之间。现实场景中，人与动物（如被狗扑向时的闪避）、人与场景（如躲避飞来的球）的交互同样普遍且重要，但结构化骨架输入无法捕捉动物姿态或场景物体的运动信息。此外，骨架数据天然缺失了表情和情感等关键线索——同一“走近”动作，微笑与愤怒所触发的反应截然不同，而现有范式对此无能为力。

**视频条件利用的粗糙性。** 即便将输入扩展至 RGB 视频，此前重新实现的视频条件基线方法（如 MDM、MLD、T2M-GPT、MoMask 等）也仅采用全局平均池化特征作为生成条件。这种简单聚合将所有帧等权对待，完全丢弃了视频的时序动态信息——哪些帧承载关键交互意图、哪些帧是冗余过渡，模型无从得知。由此生成的“反应”往往与刺激动作的节奏、力度和意图脱节。

### 本文动机

针对上述缺口，本文提出 HERO（**H**uman r**E**action gene**R**ation fr**O**m videos）框架，旨在直接从 RGB 视频中生成 3D 人类反应动作。核心动机体现在三个层面：

1. **模态拓展：** 将输入从结构化骨架序列升级为 RGB 视频，使模型能够自然处理包含动作、表情和情感的视觉信号，从而将交互范围从单一的人人交互拓展至人-动物、人-场景三大类交互。

2. **精细化交互意图建模：** 引入全局-局部表示交叉注意力机制，不再简单平均池化所有帧，而是以全局视频语义为查询，动态加权每一帧的局部特征，提炼出更精确的交互意图表示。

3. **动态信息持续注入：** 在反应生成的全过程中，通过运动-帧交叉注意力持续利用视频的逐帧动态细节，使生成的动作在时序上与刺激视频保持高度协调。

为支撑这一研究方向，本文同时构建了 **ViMo（Video-to-Motion）数据集**，覆盖 32 个子类别的三大类交互，为视频驱动的反应生成提供了首个大规模基准。

## 核心方法与创新机理

### 从骨架序列到 RGB 视频：输入模态的根本性拓展

现有的人类反应生成方法（如 MDM、T2M-GPT 等）依赖结构化的 3D 人体运动序列作为输入，这一设计隐含地将交互限定在人与人之间，且完全缺失了表情、情感等视觉语义信息。HERO 将输入模态切换为 **RGB 视频**，使模型能够同时感知动作、表情和场景上下文，从而将反应生成的适用范围从单一的人-人交互拓展至人-动物、人-场景等更广泛的交互类别。

### 全局-局部交叉注意力：精细化交互意图提取

基线方法通常直接对视频所有帧进行平均池化，获得一个全局特征向量作为生成条件。这种做法忽略了不同帧对交互意图的贡献差异——例如，在“拳击”场景中，出拳瞬间的帧远比准备阶段的帧更具信息量。

HERO 提出**交互意图提取（Interaction Intention Extraction, IIE）**模块，以全局视觉特征 $\mathbf{v}_g$ 为查询，逐帧局部特征 $\mathbf{v}_l$ 为键和值，通过交叉注意力动态加权每一帧：

$$Att_{gl} = \mathrm{softmax}\left(\frac{\mathbf{Q}_g\mathbf{K}_l^{\mathbf{T}}}{\sqrt{d_{vl}}}\right)\mathbf{V}_l$$

这一机制使模型能够根据全局语义自动聚焦于关键帧，提炼出更精确的交互意图表示。消融实验证实，移除 IIE 后 FID 从 0.427 显著恶化至 0.535（Table 2），表明精细化意图提取对生成质量至关重要。

### 运动-帧交叉注意力：持续注入动态细节

基线方法仅在生成初始阶段注入视频全局特征，后续解码过程不再显式利用逐帧动态信息。HERO 引入**动态信息利用（Dynamic Information Exploitation, DIE）**模块，在 Transformer 解码器的每一层持续计算运动特征与视频局部帧特征之间的交叉注意力：

$$Att_{mf} = \mathrm{softmax}\left(\frac{\mathbf{Q}_m\mathbf{K}_f^{\mathbf{T}}}{\sqrt{d_l}}\right)\mathbf{V}_f$$

这使得生成过程能够持续“回看”视频中的动态细节，而非仅依赖初始条件。消融显示，移除 DIE 使 FID 升至 0.521，且 multimodality 下降（Table 2），证明持续注入帧级信息对生成多样且合理的反应不可或缺。

### 创新机制的系统性协同

IIE 与 DIE 并非孤立运作，而是形成互补闭环：IIE 负责从视频中提炼“交互意图是什么”（what），DIE 则持续提供“交互过程如何展开”（how）的时序细节。意图条件自注意力将 IIE 的输出注入运动 token 序列，指导生成方向；运动-帧交叉注意力则确保生成的动作与视频动态保持时间对齐。这一协同设计使得 HERO 在 ViMo 测试集上取得了 FID 0.427 的最优结果，且用户研究显示其生成的动作在运动质量和反应合理性上均显著优于各类基线（Figure 4）。

HERO 的整体 pipeline 围绕一个核心设计展开：**从 RGB 视频中提取精细的交互意图，并将其持续注入运动生成过程**，以合成合理的人类 3D 反应动作。模型由三个主要模块串联构成，形成“视频编码 → 运动离散化 → 条件生成”的信息流。

**视频编码器** 接收原始 RGB 视频作为输入，利用冻结的 TC-CLIP 提取两类互补的视觉表示：逐帧局部特征 $\mathbf{v}_l = [\mathbf{v}_1, \mathbf{v}_2, ..., \mathbf{v}_T]$ 和通过平均池化得到的全局特征 $\mathbf{v}_g = \mathbf{AvgPool}([\mathbf{v}_1, \mathbf{v}_2, ..., \mathbf{v}_T])$。这两类表示分别服务于后续的交互意图提取和动态细节利用。

**运动 VQ-VAE** 负责将连续的 3D 人体运动序列离散化为多层运动 token。具体而言，运动编码器 $\mathbf{E_m}$ 将原始运动映射为隐变量 $\mathbf{z}$，再通过残差矢量量化（RVQ）将其映射到可学习码本 $\mathbf{C}$ 中的离散索引。训练时使用标准的 VQ-VAE 损失：

$$\mathcal{L}_{vq} = \mathcal{L}_{re} + ||sg[\mathbf{z}] - \mathbf{q}||_2^2 + \beta ||\mathbf{z} - sg[\mathbf{q}]||_2^2$$

该模块的权重先在 HumanML3D 上预训练，再在 ViMo 上微调，为生成模块提供紧凑的离散运动表示空间。

**反应生成模块** 是 pipeline 的核心，包含三个关键子机制：

1. **交互意图提取 (IIE)**：以全局视觉特征 $\mathbf{v}_g$ 为查询，逐帧局部特征 $\mathbf{v}_l$ 为键/值，通过全局-局部交叉注意力动态加权每一帧，提炼出精细的交互意图表示 $\mathbf{e}$：
   $$Att_{gl} = \mathrm{softmax}\left(\frac{\mathbf{Q}_g\mathbf{K}_l^{\mathbf{T}}}{\sqrt{d_{vl}}}\right)\mathbf{V}_l$$

2. **意图条件自注意力**：将交互意图表示 $\mathbf{e}$ 与被掩码破坏的运动 token 序列 $\tilde{\mathbf{m}}$ 拼接后送入自注意力层，使交互意图充分引导生成过程。

3. **动态信息利用 (DIE)**：在生成过程中持续计算运动-帧交叉注意力，以运动特征为查询、视频局部帧特征为键/值，使模型能够利用每一帧的动态细节：
   $$Att_{mf} = \mathrm{softmax}\left(\frac{\mathbf{Q}_m\mathbf{K}_f^{\mathbf{T}}}{\sqrt{d_l}}\right)\mathbf{V}_f$$

整个生成模块采用掩码 Transformer 解码器架构，训练时以掩码运动建模损失优化：

$$\mathcal{L}_{mask} = \mathbb{E}_{\mathbf{m}\in\mathcal{D}}\left[\sum_{\forall \tilde{\mathbf{m}}_i=[\mathrm{MASK}]} -\log p(\mathbf{m}_i|\tilde{\mathbf{m}},c)\right]$$

推理时仅输入视频，通过迭代解码生成离散运动 token，再经 RVQ-VAE 解码器还原为连续运动序列，最后通过残差细化模块进一步提升运动质量。

**输入输出流**：训练阶段，视频和真实反应运动同时输入 HERO，视频编码器与生成模块联合优化（视频编码器参数冻结）；推理阶段仅提供 RGB 视频，模型端到端输出 3D 人体反应运动序列。这一设计使 HERO 能够处理包含人脸表情和情绪信息的自然视频，突破了现有方法依赖结构化骨架序列的限制。

### 补充图表

![[assets/figures/papers/paper_list_l1888_HERO_Human_Reaction_Generation_from_Videos/figures/002_Figure_2.jpg]]
*Figure 2: The pipeline of HERO. During training, the video and GT reactive motion are input into HERO. As for inference, only the video is provided. Note that we omit the residual motion refinement (See the end of Sec. 3.3) from the figure for clarity*

HERO 框架由三个核心模块串联构成：**视频编码器**负责从 RGB 视频中提取多粒度视觉表征，**运动 VQ-VAE** 将连续人体运动离散化为多层 token 序列，**反应生成模块**则通过交互意图提取与动态信息利用两个关键机制，将视频条件转化为合理的 3D 反应动作。

### 视频编码器

视频编码器采用 TC-CLIP 对输入视频逐帧提取局部视觉表示，记为 $\mathbf{v}_l = [\mathbf{v}_1, \mathbf{v}_2, ..., \mathbf{v}_T]$，其中 $T$ 为视频帧数。全局视觉表示通过对所有帧特征进行平均池化获得：

$$\mathbf{v}_g = \mathbf{AvgPool}([\mathbf{v}_1, \mathbf{v}_2, ..., \mathbf{v}_T])$$

$\mathbf{v}_g$ 提供了视频的整体语义概要，而 $\mathbf{v}_l$ 保留了帧级别的动态细节。在训练和推理阶段，视频编码器的参数均被冻结，以保证视觉特征的稳定性。

### 运动 VQ-VAE

运动 VQ-VAE 将原始 3D 人体运动序列映射为离散的运动 token 序列，供下游生成模块使用。具体而言，运动编码器 $\mathbf{E_m}$ 将运动序列编码为隐变量 $\mathbf{z}$，随后通过残差矢量量化（RVQ）将 $\mathbf{z}$ 映射到可学习码本 $\mathbf{C} = \{\mathbf{c}_k\}_{k=1}^{K}$ 中的最近邻条目，其索引即构成运动 token 序列。训练损失结合了重建损失、码本承诺损失和编码器承诺损失：

$$\mathcal{L}_{vq} = \mathcal{L}_{re} + ||sg[\mathbf{z}] - \mathbf{q}||_2^2 + \beta ||\mathbf{z} - sg[\mathbf{q}]||_2^2$$

其中 $sg[\cdot]$ 表示停止梯度算子，$\mathbf{q}$ 为 $\mathbf{z}$ 在码本中的量化结果，$\beta$ 为承诺损失权重。该 VQ-VAE 先在 HumanML3D 上预训练，再在 ViMo 数据集上微调 10 个 epoch。

### 反应生成模块

反应生成模块是 HERO 的核心，包含三个关键子机制：

**掩码运动建模损失**：给定条件 $c$ 和被随机掩码破坏的运动 token 序列 $\tilde{\mathbf{m}}$，模型需预测被掩码位置的真实 token $\mathbf{m}_i$，优化目标为负对数似然：

$$\mathcal{L}_{mask} = \mathbb{E}_{\mathbf{m}\in\mathcal{D}}\left[\sum_{\forall \tilde{\mathbf{m}}_i=[\mathrm{MASK}]} -\log p(\mathbf{m}_i|\tilde{\mathbf{m}},c)\right]$$

**交互意图提取（IIE）**：该模块通过全局-局部表示交叉注意力，以全局视觉特征 $\mathbf{Q}_g$ 为查询，逐帧局部特征 $\mathbf{K}_l$、$\mathbf{V}_l$ 为键和值，动态加权融合各帧信息：

$$Att_{gl} = \mathrm{softmax}\left(\frac{\mathbf{Q}_g\mathbf{K}_l^{\mathbf{T}}}{\sqrt{d_{vl}}}\right)\mathbf{V}_l$$

与基线方法直接使用全局平均池化特征作为条件不同，IIE 使模型能够根据全局语义自适应地关注关键帧，提炼出更精细的交互意图表示。

**动态信息利用（DIE）**：为在生成全过程中持续注入视频的动态细节，DIE 模块计算运动特征与视频帧特征之间的交叉注意力。运动 token 的隐层表示作为查询 $\mathbf{Q}_m$，局部帧特征作为键 $\mathbf{K}_f$ 和值 $\mathbf{V}_f$：

$$Att_{mf} = \mathrm{softmax}\left(\frac{\mathbf{Q}_m\mathbf{K}_f^{\mathbf{T}}}{\sqrt{d_l}}\right)\mathbf{V}_f$$

这一设计使得每一层 Transformer 解码器都能直接访问原始视频的逐帧动态信息，而非仅依赖初始条件中压缩的全局特征。消融实验（Table 2）表明，移除 IIE 或 DIE 分别使 FID 从 0.427 升至 0.535 和 0.521，验证了两者对生成质量的关键作用。

在交互意图注入阶段，模型将 IIE 输出的意图表示与掩码后的运动 token 序列拼接，通过意图条件自注意力使交互意图全程引导反应生成。最终，残差细化模块对解码器输出进行微调，提升运动细节的合理性。

## 实验与关键发现

### 主实验结果

HERO 在 ViMo 测试集上与 5 个重实现的视频条件基线进行了全面对比，包括扩散式方法 **MDM** 与 **MLD**、自回归方法 **T2M-GPT**、以及掩码生成式方法 **BAMM** 与 **MoMask**。所有基线均将原始文本/运动条件替换为视频编码器提取的全局特征，以保证比较的公平性。

如 Table 1 所示，HERO 在分布质量指标 FID 上达到 **0.427±0.014**，相较最强基线 MoMask 的 0.856±0.015 降低了 **50.1%**，表明 HERO 生成的反应动作分布与真实分布最为接近。在多样性指标上，HERO 取得 **7.801±0.061**，最接近真实动作的 7.845±0.078，而其他基线的多样性均低于真实值，说明它们倾向于产生模式坍塌。值得注意的是，重实现的扩散模型（MDM、MLD）在视频条件下表现不佳，FID 均超过 2.0，表明简单地将视频全局特征注入扩散去噪过程难以捕捉复杂的交互语义。

![[assets/figures/papers/paper_list_l1888_HERO_Human_Reaction_Generation_from_Videos/figures/004_Table_1.jpg]]
*Table 1: Quantitative evaluation on the ViMo test set. ± indicates 95% confidence interval, and → means the closer to the real motions the better. Bold face indicates the best result*

用户研究（Figure 4）进一步验证了上述结论。40 名参与者对生成动作的**运动质量**和**反应合理性**进行评分，HERO 在两项指标上均获得除真实数据外的最高分，证实其生成结果在感知层面同样具有优势。

![[assets/figures/papers/paper_list_l1888_HERO_Human_Reaction_Generation_from_Videos/figures/005_Figure_4.jpg]]
*Figure 4: User study results. The higher the scores, the better*

### 消融实验

为验证核心设计组件的贡献，论文进行了消融实验（Table 2）：

![[assets/figures/papers/paper_list_l1888_HERO_Human_Reaction_Generation_from_Videos/figures/008_Table_2.jpg]]
*Table 2: Quantitative ablation studies. w/o means without. IIE and DIE represent Interaction Intention Extraction and Dynamic Information Exploitation, respectively*

- **移除交互意图提取 (w/o IIE)**：将全局-局部交叉注意力替换为简单的平均池化后，FID 从 0.427 恶化至 **0.535**，多样性也从 7.801 偏离至 7.679。这表明仅靠全局平均池化无法有效区分关键帧与冗余帧，导致交互意图模糊。
- **移除动态信息利用 (w/o DIE)**：去掉运动-帧交叉注意力后，FID 升至 **0.521**，且 Multimodality 从 5.112 降至 4.885。这说明缺乏逐帧动态信息的持续注入，模型生成的动作多样性不足，难以覆盖真实反应的多模态分布。

定性消融对比（Figure 6）展示了在“射击”场景下，完整 HERO 能生成合理的防御反应，而移除 IIE 或 DIE 后生成的动作则缺乏对视频动态的响应，反应与视频内容脱节。

![[assets/figures/papers/paper_list_l1888_HERO_Human_Reaction_Generation_from_Videos/figures/007_Figure_6.jpg]]
*Figure 6: Qualitative ablation studies given the same video. A plausible reaction would be to defend against the shooting*

此外，Transformer 解码器层数消融（Table 3）显示，层数从 3 层增至 9 层时 FID 持续改善，但超过 9 层后性能饱和。论文最终选择 9 层作为默认配置。

![[assets/figures/papers/paper_list_l1888_HERO_Human_Reaction_Generation_from_Videos/figures/013_Table_3.jpg]]
*Table 3: Ablation studies on the number of Transformer decoder units Nlayers. ± indicates 95% confidence interval, and → means the closer to the real motions the better. Bold face indicates the best result. R. means real motions*

### 细粒度分析

**不同交互大类上的表现**（Table 4）：HERO 在人类-人类交互上表现最佳（FID 0.390），而在动物-人类（FID 0.503）和场景-人类（FID 0.488）交互上性能下降。这一差距可能源于后两类交互的数据量较少且动作模式更复杂，模型对非人类主体的运动理解能力有限。

**情绪驱动的反应生成**（Table 5）：在“走近”这一相同动作下，分别输入带有“愤怒”“恐惧”“快乐”情绪的视频，HERO 能生成差异化的反应。定量评估表明，不同情绪条件下的生成质量保持稳定，说明交互意图提取模块成功捕获了视频中的情绪线索。

**未见子类别的泛化能力**（Table 6）：在 6 个训练时完全未见的交互子类别上，HERO 的 FID 为 0.489，仍优于多数基线在已见类别上的表现，证明全局-局部交叉注意力学到的是通用的交互理解能力，而非对特定类别的记忆。

**训练数据量影响**（Table 7）：当训练对数量从 20% 逐步增至 100% 时，FID 从 0.621 单调改善至 0.427，表明 HERO 对数据规模有良好的可扩展性，且尚未达到性能平台期。

### 失败模式与局限性

尽管 HERO 在整体指标上表现优异，论文指出了以下失败模式：

1. **物理伪影**：生成的 3D 动作缺乏明确的物理约束，可能出现漂浮或滑步现象，尤其在脚部与地面的接触上表现不自然。
2. **手部细节缺失**：模型未对手部运动单独建模，导致反应中手部姿态模糊，限制了表现力。
3. **非人类交互退化**：在动物-人类和场景-人类交互中，生成质量明显低于人类-人类交互，部分情况下反应与视频内容不匹配。
4. **反应长度固定**：当前框架无法自主预测反应动作的时长，需要预设长度，限制了在开放场景中的适用性。

## 定位与知识库关联

### 1. 方法谱系与基线关系

HERO 的核心任务——从 RGB 视频生成三维人体反应——在现有文献中缺乏直接可比的端到端基线。因此，作者将五个具有代表性的运动生成模型重新实现为视频条件版本，以建立公平的比较基准。这些基线涵盖了当前主流的生成范式：

- **扩散模型**：**MDM** 和 **MLD** 分别代表原始数据空间和潜空间的扩散式运动生成。重实现时，其文本或运动条件被替换为视频编码器提取的全局特征。
- **自回归模型**：**T2M-GPT** 通过 VQ-VAE 将运动离散化为 token 序列，以自回归方式逐 token 预测。重实现时以视频特征替代文本条件。
- **掩码生成模型**：**MoMask** 和 **BAMM** 采用掩码建模策略。MoMask 使用随机掩码与逐步解码，BAMM 则基于双向自回归掩码。两者均被改造为以视频特征为条件。

从知识库定位来看，HERO 与上述基线的方法论差异并非生成范式本身——HERO 同样采用掩码 Transformer 解码器——而在于**条件信息的提取与利用方式**。这一差异体现在两个关键设计槽位上：

1. **交互意图提取 (IIE)**：基线方法直接使用视频的全局平均池化特征作为条件，忽略了不同帧对交互意图的贡献差异。HERO 引入全局-局部表示交叉注意力，以全局视频语义为查询，对逐帧局部特征进行动态加权，从而提炼出更精细的交互意图表示（Eq. 3）。这一设计的本质是将“简单平均”升级为“内容感知的帧选择”。

2. **动态信息利用 (DIE)**：基线方法仅在初始条件中包含视频特征，生成过程中不再显式访问视频的逐帧动态细节。HERO 在生成过程中持续计算运动-帧交叉注意力（Eq. 4），使模型在每一步解码时都能重新审视视频的帧级动态信息。这类似于序列到序列模型中的注意力机制，但被专门适配到视频-运动跨模态场景中。

在输入模态层面，HERO 与此前的人体反应生成方法（如基于结构化骨架序列的工作）存在根本性差异：RGB 视频天然携带表情、情感和场景上下文信息，而骨架序列仅包含运动学数据。这一模态升级使得 HERO 能够处理更广泛的交互类别（包括人与动物、人与场景），并支持情绪驱动的反应生成。

### 2. 适用边界

HERO 的适用边界由以下因素共同界定：

- **交互类别覆盖**：ViMo 数据集覆盖三大类（人人、动物-人、场景-人）共 32 个子类别。在人人交互上表现最佳，动物-人和场景-人交互的性能相对较低（Table 4），这既受限于数据量，也反映了任务难度的差异。
- **情绪敏感性**：HERO 能够针对相同动作的不同情绪（如“走近”时的愤怒与恐惧）生成差异化反应（Figure 8, Table 5），说明交互意图提取机制有效捕获了表情信息。
- **泛化能力**：在未见子类别上的定量评估（Table 6）和可视化结果（Figure 7）表明，HERO 具有一定程度的组合泛化能力，但性能仍低于已见类别。
- **反应长度**：当前模型依赖预设或外部指定的反应长度，无法自主预测反应持续时长，这限制了其在开放式场景中的适用性。

### 3. 局限与开放问题

HERO 存在以下已被作者确认的局限，以及由此衍生的开放问题：

**数据层面**
- ViMo 数据集的交互类别和视频-运动对数量仍需大幅扩展。当前 32 个子类别远不能覆盖真实世界交互的多样性。
- 开放问题：如何高效扩展数据集？是否可以利用合成数据生成管线或自监督学习从大规模未标注视频中挖掘交互对？

**模型架构层面**
- HERO 采用较简单的掩码生成框架，未能实现反应长度的自我预测。引入双向自回归方法（如 BAMM）可能是解决这一问题的方向。
- 开放问题：能否在保持生成质量的前提下，让模型自主决定何时终止反应序列？

**运动质量层面**
- 生成的 3D 动作缺乏明确的物理约束，可能出现漂浮、滑步等伪影。当前未集成任何物理仿真器或物理损失。
- 尚未建模手部细节运动，导致反应的表现力不足——手势、手指动作等精细运动在社交交互中至关重要。
- 开放问题：如何在不显著增加系统复杂度的条件下，引入物理合理性约束？深度估计和身体形状估计能否帮助生成更好反映空间关系和体型差异的反应？

**多模态融合层面**
- 多模态大语言模型 (MLLM) 在当前的直接应用中表现不足，但其语义理解和推理能力具有潜在价值。
- 开放问题：MLLM 能否通过多轮对话、思维链推理或细粒度视觉描述，为反应生成提供更精确的交互意图文本描述作为辅助条件？

## 原文 PDF

![[paperPDFs/ICCV_2025/HERO_Human_Reaction_Generation_from_Videos.pdf]]
