---
title: "OmniHuman-1: Rethinking the Scaling-Up of One-Stage Conditioned Human Animation Models"
type: paper
paper_level: A
venue: arXiv
year: 2025
pdf_ref: paperPDFs/arxiv_2025/OmniHuman_1_Rethinking_the_Scaling_Up_of_One_Stage_Conditioned_Human_Animation_Models.pdf
project_link: https://omnihuman-lab.github.io/
code_link: https://github.com/
aliases:
- OmniHuman-1
tags:
- arxiv_2025
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: 混合多种运动相关条件（文本、音频、姿态）进行训练，遵循两条原则：1）强条件任务可利用弱条件任务的数据以扩大数据规模；2）条件越强，训练比例应越低，从而在利用大规模混合数据的同时避免过拟合。
primary_logic: 将不同强度的运动条件（文本→音频→姿态）引入训练，不仅让原本被过滤的数据通过弱条件任务得以利用，还通过控制各条件的训练比例与引入顺序，使模型从大规模混合数据中学习自然运动模式，显著提升人体动画的泛化能力和运动自然度。
claims:
- 增加文本条件数据比例（0%→100% T-Data）在所有基准（CelebV-HQ, RAVDESS, CyberHost）上持续改善视觉质量、唇同步精度和手势质量。
- 采用 IAP 训练顺序（先引入文本+图像，再引入音频，最后引入姿态）相比 IPA 顺序（先引入姿态）在所有指标上均更优，避免了过早依赖强条件导致的性能全面下降。
- 混合驱动训练模型 IAP 将手部运动与音频信号解耦，有效缓解了音频驱动下夸张、不自然的手部动作。
- CelebV-HQ (肖像动画) 上 IQA / FID = IQA 3.875, FID 31.435
---

# OmniHuman-1: Rethinking the Scaling-Up of One-Stage Conditioned Human Animation Models

> [!tip] 核心洞察
> 将不同强度的运动条件（文本→音频→姿态）引入训练，不仅让原本被过滤的数据通过弱条件任务得以利用，还通过控制各条件的训练比例与引入顺序，使模型从大规模混合数据中学习自然运动模式，显著提升人体动画的泛化能力和运动自然度。

| 字段 | 内容 |
|------|------|
| 中文题名 | OmniHuman-1：重新思考单阶段条件人体动画模型的规模化 |
| 英文题名 | OmniHuman-1: Rethinking the Scaling-Up of One-Stage Conditioned Human Animation Models |
| 会议/期刊 | arXiv 2025 |
| Links | [Project](https://omnihuman-lab.github.io/) · [Code](https://github.com/) · [paper](https://arxiv.org/abs/2502.01061) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/image_and_video_generation |
| Method | OmniHuman |
| Dataset | CelebV-HQ, RAVDESS, CyberHost |

> [!tip] 效果简介
> - CelebV-HQ (肖像动画) 上，IQA / FID IQA 3.875, FID 31.435 vs previous SOTA (具体数值未报告) (全面占优)。
> - RAVDESS (肖像动画) 上，IQA / FID IQA 4.564, FID 16.970 vs previous SOTA (具体数值未报告) (全面占优)。
> - CyberHost (身体动画) 上，Sync-C / FVD / HKC Sync-C 7.443, FVD 27.031, HKC 0.898 vs previous SOTA (CyberHost 等) (全面占优)。

## 概要

**OmniHuman-1** 针对音频驱动人体动画领域的一个关键瓶颈提出了系统性解决方案：现有方法依赖严格的唇音同步与稳定性过滤，导致训练数据利用率极低（通常不足 10%），模型无法从大规模视频数据中学习手势生成、物体交互等复杂运动模式，泛化能力严重受限。

核心思路是将多种运动相关条件（文本、音频、姿态，按由弱到强的顺序）混合注入训练阶段，遵循两条原则：**（1）强条件任务可利用弱条件任务的数据以扩大数据规模**——原本因音频质量不足而被丢弃的数据，可通过文本条件或姿态条件任务得到利用；**（2）条件越强，训练比例应越低**——通过控制各条件的训练比例与引入顺序，避免模型过早过拟合强条件信号。基于此，OmniHuman 采用三阶段渐进训练策略（先引入文本+图像，再引入音频，最后引入姿态），将预训练的文本到视频扩散模型逐步转化为多条件人体视频生成模型。

消融实验（Table 1）提供了决定性证据：将文本条件数据比例从 0% 提升至 100%，在 CelebV-HQ、RAVDESS 和 CyberHost 三个基准上持续改善视觉质量、唇同步精度和手势质量；采用 IAP 训练顺序（先音频后姿态）相比 IPA 顺序（先姿态后音频）在所有指标上均更优，避免了过早依赖强条件导致的性能全面下降。混合驱动训练还使手部运动与音频信号解耦（Figure 5），有效缓解了音频驱动下夸张、不自然的手部动作。

在音频驱动肖像动画（CelebV-HQ、RAVDESS）、音频驱动身体动画（CyberHost）和视频驱动身体动画等多个基准上，OmniHuman 均取得全面领先。模型同时展现出对风格化角色和 2D 卡通形象的强泛化能力。

### 问题背景：从肖像动画到人体动画的跨越

音频驱动的人体动画旨在根据一段音频信号和一张参考图像，生成包含自然头部运动、手势动作、面部表情乃至物体交互的视频。早期方法如 **SadTalker**（Zhang et al., CVPR 2023）、**Hallo**（Xu et al., arXiv 2024）和 **Vexpress**（Wang et al., arXiv 2024）主要聚焦于**肖像动画**（portrait animation），即仅生成头部和肩部区域的说话视频，取得了令人瞩目的唇音同步和面部表情质量。然而，当任务扩展到包含手势、身体姿态和物体交互的**全身人体动画**时，现有方法暴露出明显的泛化瓶颈——手势生成僵硬、与音频信号不协调，且几乎无法处理复杂的物体交互场景。

### 现有方法的核心瓶颈：数据利用率极低

造成上述差距的根本原因并非模型架构的局限，而是一个更底层的数据困境。现有音频驱动人体动画方法普遍依赖严格的**数据过滤流水线**：训练数据必须同时满足唇音同步精度、视频稳定性、画面质量等多重标准。经过层层筛选后，仅有不到 10% 的原始数据能够被保留用于训练。这种“精筛”策略在肖像动画任务中尚可维持，因为头部运动的自由度相对有限，少量高质量数据即可覆盖主要变化模式。但对于涉及全身运动、手势和物体交互的人体动画，运动空间呈指数级膨胀，严格过滤导致模型从未见过大量自然运动模式，从而严重限制了手势生成、物体交互等能力的泛化。

### 本文动机：以“条件弱化”换取“数据规模化”

OmniHuman 的核心动机在于打破“数据过滤与运动泛化”之间的零和博弈。其关键洞察是：**并非所有被过滤的数据都毫无价值**——一段因唇音同步不达标而被丢弃的视频，可能仍然包含丰富且自然的手势和身体运动信息。问题在于，单一音频条件模型无法利用这些数据，因为音频信号与画面内容的对应关系不够精确。

为此，OmniHuman 提出了一种**混合条件训练**（omni-conditions training）策略：在训练阶段同时引入**文本、音频、姿态**三种由弱到强的运动相关条件。其逻辑遵循两条原则：

1. **强条件任务可利用弱条件任务的数据**：对于音频条件无法使用的数据，可退化为更弱的文本条件任务（如“一个人在做手势”）加以利用，从而将数据利用率从不足 10% 提升至近乎 100%。
2. **条件越强，训练比例应越低**：强条件（如姿态骨架）提供精确的逐帧运动约束，但若占比过高，模型会过拟合到这些精确信号，丧失从弱条件数据中学习自然运动模式的能力。

通过这种设计，OmniHuman 将原本互斥的“数据规模”与“运动精度”转化为可协同优化的两个维度，使模型能够从大规模混合数据中学习自然运动先验，同时在强条件激活时保持精确控制。这一思路为人体动画的规模化（scaling up）开辟了新的路径。

## 核心方法与创新机理

OmniHuman 的核心创新在于**重新定义训练范式**：将人体动画从“单条件+严格数据过滤”的范式，转变为“多条件混合训练+数据规模化利用”的范式。其关键创新点可归纳为以下三个相互关联的维度。

### 1. 多条件混合训练策略：从数据丢弃到数据规模化

现有音频驱动人体动画方法面临一个根本性瓶颈：为保证唇音同步和视频稳定性，训练数据需经过严格过滤，通常仅保留不到 10% 的原始数据。这导致模型无法接触大规模、多样化的运动数据，严重限制了手势生成、物体交互等能力的泛化。

OmniHuman 的核心突破在于**将不同强度的运动相关条件（文本、音频、姿态）混合引入训练**，遵循两条原则：

- **原则一（数据规模化）**：弱条件任务可利用强条件任务无法使用的数据。文本作为最弱的运动条件（仅需描述性标注），可覆盖大量原本被音频或姿态条件过滤掉的视频，从而将训练数据利用率从不足 10% 提升至接近全量。
- **原则二（比例与顺序控制）**：条件越强，训练比例应越低。通过控制各条件的训练比例（文本 > 音频 > 姿态）和引入顺序（先文本，再音频，最后姿态），避免模型过拟合强条件信号，同时从大规模混合数据中学习自然运动模式。

这一策略的因果机制清晰：**弱条件任务充当数据放大器**，让原本被丢弃的数据通过文本条件得以利用；而**条件强度的梯度设计**则防止强条件（如姿态）主导训练，确保模型从数据多样性中获益的同时保持运动质量。

### 2. 渐进式三阶段训练：顺序决定成败

OmniHuman 采用三阶段混合条件训练（IAP 顺序），将通用文生视频模型逐步转化为多条件人体视频生成模型：

- **Stage 1**：仅引入文本条件与图像条件，训练模型理解运动语义描述。
- **Stage 2**：加入音频条件，建立音频-运动关联。
- **Stage 3**：最后引入姿态条件，提供精确的空间运动约束。

消融实验（Table 1）揭示了训练顺序的关键性：若将姿态提前引入（IPA 顺序，先姿态后音频），会导致输出质量在多个维度全面下降；而 IAP 顺序（先音频后姿态）则维持或提升了性能。这一现象的本质在于：**过早引入强条件（姿态）会使模型形成对精确骨架信号的依赖，削弱从弱条件（音频、文本）中学习自然运动模式的能力**。

### 3. 架构层面的条件注入创新

在模型架构上，OmniHuman 基于 MMDiT 骨干网络，对多种条件的注入方式进行了精心设计：

- **外观条件注入（零参数方案）**：传统方法通常使用独立的参考网络（复制去噪骨干，并行处理）来保持人物外观一致性。OmniHuman 直接重用去噪 DiT 骨干，通过修改 3D 旋转位置编码（RoPE）实现：将参考图像令牌的时间分量设为零，使其在自注意力中与视频令牌交互时仅提供外观信息，不引入时序干扰。这一设计**无需额外参数**，实现了轻量化的外观条件注入。
- **音频注入模块**：使用 wav2vec 提取多尺度音频特征，经 MLP 压缩后通过帧级交叉注意力注入 DiT 各层，而非仅在输入端拼接。
- **姿态注入模块**：通过 Pose Guider 编码骨架图序列，将姿态令牌沿通道维度与噪声潜变量拼接，与音频注入形成互补的运动控制通路。

这些设计共同构成了一个**统一的多条件 DiT 框架**，使模型能够在推理时灵活组合不同条件，支持从纯文本驱动到音频驱动、姿态驱动乃至混合驱动的多种生成模式。

### 4. 创新效果的关键验证

消融实验提供了强有力的证据链：

- **数据规模化效应**：将文本条件数据比例从 0% 提升至 100%（T-Data），在 CelebV-HQ、RAVDESS、CyberHost 三个基准上持续改善视觉质量（FID、FVD）、唇同步精度和手势质量（Table 1 上半部分）。
- **顺序效应**：IAP 训练顺序在所有指标上优于 IPA 顺序（Table 1 下半部分），验证了“弱条件先行”策略的必要性。
- **解耦效应**：混合驱动训练模型 IAP 将手部运动与音频信号解耦，有效缓解了纯音频驱动下夸张、不自然的手部动作（Figure 5 梯度曲线分析）。

这些结果表明，OmniHuman 的创新并非简单的条件堆叠，而是通过**条件强度的梯度设计、训练顺序的因果控制和架构层面的高效注入**，系统性地解决了数据稀缺与运动自然度之间的根本矛盾。

OmniHuman 的整体框架围绕**多模态运动条件混合训练**这一核心思想构建，包含两个关键部分：OmniHuman 模型本身，以及全条件训练策略（omni-conditions training）。

### 模型架构

OmniHuman 模型基于 **MMDiT（多模态扩散 Transformer）** 架构构建，以文本到视频生成模型为起点，通过因果 3D VAE 将视频压缩到紧凑的潜在空间中进行操作。模型支持同时接收四种模态条件：

- **文本条件**：通过原始 MMDiT 的文本分支处理文本提示。
- **音频条件**：使用 wav2vec 模型提取多尺度音频特征，经 MLP 压缩后，通过帧级交叉注意力注入 MMDiT 的每一层。
- **姿态条件**：通过 Pose Guider 编码驱动骨架图序列，生成姿态令牌，沿通道维度与噪声潜变量拼接。
- **外观条件**：重用去噪 DiT 骨干，通过修改 3D 旋转位置编码（RoPE）实现——将参考图像令牌的时间分量设为零，使其与视频令牌在自注意力中交互，无需额外参数即可保持身份一致性。

### 三阶段混合条件训练策略

框架的核心创新在于**全条件训练策略**，通过渐进式三阶段训练，将通用文本到视频扩散模型逐步转化为多条件人体视频生成模型：

1. **Stage 1**：仅使用文本和图像条件训练，建立基础的图像到视频生成能力。
2. **Stage 2**：引入音频条件，使模型学习音频与运动的关联。
3. **Stage 3**：引入姿态条件（最强条件），完成多条件联合训练。

训练比例的设定遵循两条原则：
- **原则一**：强条件任务可利用弱条件任务的数据以扩大数据规模——原本因唇音同步或稳定性不达标而被丢弃的数据，可以通过文本等弱条件任务被充分利用。
- **原则二**：条件越强，训练比例越低——文本、音频、姿态的训练比例逐步减半，避免模型过早依赖强条件（如姿态）而导致泛化能力下降。消融实验证实，若先引入姿态（IPA 顺序），会导致输出质量全面下降；而先音频后姿态（IAP 顺序）则维持甚至提升了性能。

### 推理策略

推理时，OmniHuman 采用分类器自由引导（CFG），尺度设为 6.5，但仅应用于音频和文本条件，不应用于姿态条件。为支持长视频生成，前一个片段的后五帧被用作后续片段的运动帧，实现无缝延续。模型以单模型支持任意宽高比和身体比例的输入图像，无需针对不同分辨率或构图分别训练。

![[assets/figures/papers/paper_list_l1836_OmniHuman_1_Rethinking_the_Scaling_Up_of_One_Stage_Conditioned_Human_Ani/figures/002_Figure_2.jpg]]
*Figure 2: The framework of OmniHuman. It consists of two parts: (1) the OmniHuman model, which is based on the DiT architecture and supports simultaneous conditioning with multiple modalities including text, image, audio, and pose. To support long video continuation, we concatenate the latents of the last generated frames with noise latents, which are omitted for simplicity. (2) the omni-conditions training strategy, which employs progressive, multi-stage training based on the motion-related extent of the conditions. The mixed condition training allows the OmniHuman model to benefit from the scaling up of mixed data*

OmniHuman 的整体架构（见 Figure 2）由因果 3D VAE、基于 MMDiT 的去噪骨干网络、多条件注入模块以及渐进式混合条件训练策略构成。以下仅展开与公式和核心计算模块直接相关的部分。

### 因果 3D VAE

OmniHuman 在紧凑的潜在空间中运行，使用**因果 3D VAE** 将原生分辨率的视频投影到低维潜在表示。因果 3D VAE 确保时间维度的因果性，即当前帧的编码不依赖未来帧，这对于流式推理和长视频生成至关重要。

### MMDiT 骨干网络

去噪过程的核心基于 **MMDiT**（Multi-Modal Diffusion Transformer）架构的文本到视频模型。MMDiT 原生支持文本与视频令牌之间的交叉注意力交互，OmniHuman 在此基础上扩展了音频、姿态和外观条件的注入通路。

### 多条件注入模块

#### 音频条件注入

音频特征通过 wav2vec 模型提取多尺度表示，经 MLP 压缩后，以**帧级交叉注意力**的方式注入 MMDiT 的每个 Transformer 块。设音频特征序列为 $\mathbf{A}$，视频帧潜在表示为 $\mathbf{Z}$，则第 $l$ 层的交叉注意力计算为：

$$\text{CrossAttn}(\mathbf{Z}_l, \mathbf{A}) = \text{softmax}\left(\frac{\mathbf{Q}_l \mathbf{K}_A^\top}{\sqrt{d}}\right) \mathbf{V}_A$$

其中 $\mathbf{Q}_l$ 由 $\mathbf{Z}_l$ 线性投影得到，$\mathbf{K}_A$、$\mathbf{V}_A$ 由音频特征投影得到。

#### 姿态条件注入

姿态条件通过 **Pose Guider** 编码：将驱动骨架图序列输入姿态编码器，生成姿态令牌 $\mathbf{P}$，然后沿通道维度与噪声潜在表示 $\mathbf{Z}_t$ 拼接：

$$\tilde{\mathbf{Z}}_t = \text{Concat}(\mathbf{Z}_t, \mathbf{P}) \quad \text{(沿通道维度)}$$

拼接后的表示直接输入 MMDiT 进行去噪。

#### 外观条件注入（修改的 3D RoPE）

外观保持通过**重用去噪 DiT 骨干**实现，无需额外参数。核心机制是修改 DiT 中的 3D 旋转位置编码（3D RoPE）：将参考图像令牌的时间分量设为零，使其在自注意力中仅参与空间维度的交互，而不引入时间偏移。设令牌 $x$ 的 3D 位置为 $(t, h, w)$，其 RoPE 编码为：

$$\text{RoPE}(x, (t, h, w)) = \text{RoPE}_{\text{spatial}}(x, (h, w)) \oplus \text{RoPE}_{\text{temporal}}(x, t)$$

对于参考令牌，强制 $t = 0$，从而 $\text{RoPE}_{\text{temporal}}(x, 0) = \mathbf{0}$，仅保留空间位置信息。这使得参考令牌与视频令牌在自注意力中自然交互，实现身份保持。

#### 文本条件分支

文本条件直接复用原始 MMDiT 的文本分支，通过文本编码器提取特征后以交叉注意力注入，不做架构修改。

### 分类器自由引导（CFG）

推理时，分类器自由引导仅应用于音频和文本条件，**不应用于姿态条件**。CFG 尺度设定为：

$$\lambda_{\text{CFG}} = 6.5$$

引导公式为：

$$\hat{\epsilon}_\theta(\mathbf{Z}_t, \mathbf{c}_{\text{audio}}, \mathbf{c}_{\text{text}}, \mathbf{c}_{\text{pose}}) = \epsilon_\theta(\mathbf{Z}_t, \emptyset, \emptyset, \mathbf{c}_{\text{pose}}) + \lambda_{\text{CFG}} \left[ \epsilon_\theta(\mathbf{Z}_t, \mathbf{c}_{\text{audio}}, \mathbf{c}_{\text{text}}, \mathbf{c}_{\text{pose}}) - \epsilon_\theta(\mathbf{Z}_t, \emptyset, \emptyset, \mathbf{c}_{\text{pose}}) \right]$$

其中 $\emptyset$ 表示将对应条件置为空。

### 长视频延续机制

为支持长视频生成，OmniHuman 将前一个生成片段的后 5 帧潜在表示与当前片段的噪声潜在表示沿时间维度拼接，作为去噪的输入。设前一阶段的最后 $k=5$ 帧潜在表示为 $\mathbf{Z}_{\text{prev}}[-k:]$，当前噪声为 $\mathbf{Z}_t^{\text{curr}}$，则拼接输入为：

$$\mathbf{Z}_t^{\text{concat}} = \text{Concat}(\mathbf{Z}_{\text{prev}}[-k:], \mathbf{Z}_t^{\text{curr}}) \quad \text{(沿时间维度)}$$

去噪后仅保留当前片段的输出，实现无缝的长视频延续。

### 训练学习率

训练使用 AdamW 优化器，学习率设定为：

$$\eta = 5 \times 10^{-5}$$

## 实验与关键发现

### 4.1 实验设置与评估基准

OmniHuman 的训练使用 AdamW 优化器，学习率固定为 $5 \times 10^{-5}$。推理阶段采用分类器自由引导（CFG），仅作用于音频和文本条件，不对姿态条件施加引导，CFG 尺度设为 6.5。长视频生成通过将前一段最后五帧的潜变量与噪声潜变量拼接实现时序延续。

评估覆盖三个核心基准：
- **CelebV-HQ**（100 个视频）和 **RAVDESS**（100 个视频）：用于肖像动画评测，指标包括 IQA、ASE、Sync-C、FID、FVD。
- **CyberHost**（269 个视频）：用于身体动画评测，指标包括 Sync-C、FVD、HKC、HKV。
- **视频驱动身体动画**：与 DisCo、MimicMotion 等视频驱动方法对比，指标包括 IQA、ASE、FID、FVD、AKD。

需注意评估集规模有限（总计不足 500 个视频），可能无法完全代表真实世界多样性；且对比方法未使用完全相同的数据分布训练，OmniHuman 的性能优势部分可能源于更大规模的混合数据。

### 4.2 全条件训练消融实验（Table 1）

![[assets/figures/papers/paper_list_l1836_OmniHuman_1_Rethinking_the_Scaling_Up_of_One_Stage_Conditioned_Human_Ani/figures/003_Table_1.jpg]]
*Table 1: Quantitative analysis of Omni-Conditions Training. The upper and lower parts correspond to Principles 1 and 2 respectively*

Table 1 系统验证了 OmniHuman 提出的两条核心训练原则，分为上下两部分。

**原则一：弱条件任务可扩展数据规模。** 固定其他设置，逐步增加文本条件数据的比例（0% → 25% → 50% → 100% T-Data），在 CelebV-HQ、RAVDESS 和 CyberHost 三个基准上均观察到一致的性能提升。具体而言，FVD、FID 持续下降，唇音同步精度和手势质量同步改善。这一结果表明，原本因唇音同步或稳定性不达标而被单条件模型丢弃的数据，可以通过弱条件（文本）任务重新利用，直接转化为模型性能的增益。

**原则二：条件越强，训练比例应越低，且引入顺序至关重要。** 下部分对比了三种训练顺序：
- **IPA**（先引入姿态，再引入音频）：在所有指标上导致输出质量全面下降。
- **IAP A<P**（先音频后姿态，音频比例低于姿态）：性能介于 IPA 和 IAP A>P 之间。
- **IAP A>P**（先音频后姿态，音频比例高于姿态）：在所有指标上维持或提升了性能，为最终采用的配置。

这一消融揭示了关键的因果机制：过早引入强条件（姿态）会使模型过度依赖该条件，丧失从弱条件数据中学习自然运动模式的能力，从而导致泛化性能崩溃。IAP 顺序通过渐进式引入条件，有效避免了这一问题。

进一步的比例消融表明，固定文本条件比例 T=90% 时，音频比例 A=50% 在所有指标上取得最均衡的性能，优于 A=10% 或 A=90% 的极端设置。

### 4.3 与现有方法的定量对比

**音频驱动肖像动画（Table 2）。** 在 CelebV-HQ 和 RAVDESS 基准上，OmniHuman 在 IQA 和 FID 两项核心指标上全面超越现有肖像动画方法，包括 **SadTalker**（Zhang et al., CVPR 2023）、**Hallo**（Xu et al., arXiv 2024）、**Vexpress**（Wang et al., arXiv 2024）、EchoMimic、Loopy 和 Hallo-3。在 CelebV-HQ 上，OmniHuman 取得 IQA 3.875、FID 31.435；在 RAVDESS 上取得 IQA 4.564、FID 16.970。

**音频驱动身体动画（Table 3）。** 在 CyberHost 基准上，OmniHuman 在 Sync-C（7.443）、FVD（27.031）和 HKC（0.898）三个指标上全面优于 **CyberHost**（Lin et al., ICLR 2025）等身体动画方法。值得注意的是，OmniHuman 以单一模型支持任意宽高比和身体比例的输入，而现有方法通常需要针对特定比例进行专门优化。

**视频驱动身体动画（Table 4）。** 与 DisCo、MimicMotion、DiffTED、DiffGest 等视频驱动方法相比，OmniHuman 在 IQA（4.111）、FVD（7.318）和 AKD（2.136）上均取得大幅领先，验证了混合条件训练策略对运动建模能力的普适提升。

### 4.4 定性分析与关键可视化

**与预训练 Image-to-Video 模型的对比（Figure 3）。** 视觉对比显示，预训练 I2V 模型生成的手势动作单调且缺乏与音频的关联，而 OmniHuman 通过全条件训练显著提升了手势的丰富性和自然度，生成结果更具真实感。

**手部运动解耦分析（Figure 5）。** 混合驱动训练模型 IAP 的关键优势在于将手部运动与音频信号解耦。通过可视化手部运动轨迹的梯度曲线，可以观察到：仅使用图像+音频条件（IA）的模型，其手部动作与音频信号高度耦合，导致夸张、不自然的手势；而引入姿态条件后的 IAP 模型有效缓解了这一问题，生成的手势更为自然克制。这一解耦效应是 OmniHuman 在手势生成质量上超越纯音频驱动方法的核心机制。

**多样化风格泛化（Figure 4）。** OmniHuman 展现出对风格化人形角色和 2D 卡通角色的良好兼容性，甚至能以拟人方式驱动非人物体图像，表明混合条件训练策略赋予了模型较强的外观泛化能力。

### 4.5 局限性与失败模式

尽管 OmniHuman 在多个基准上取得领先性能，仍存在以下可观测的失败模式：

1. **弱音-运动关联场景**：当音频与身体运动的相关性较弱时（如纯背景音乐），生成的视频可能出现不协调或过度夸张的动作。这是音频作为主要驱动信号的固有局限。
2. **分布外物体交互**：对于与训练分布差异显著的物体交互场景（如复杂手持物体操作），生成结果的真实感仍有明显不足，物理合理性有待提升。
3. **运动风格控制缺失**：模型目前主要依赖音频作为驱动信号，尚未显式支持运动风格、情绪强度或语义意图等高级条件，在需要精细运动控制的创意场景下灵活性受限。

这些失败模式指向了未来工作的方向：引入更丰富的运动条件以增强控制力、扩展训练数据以覆盖更广泛的物体交互场景、以及探索更大规模数据下的 Scaling Law 验证。

![[assets/figures/papers/paper_list_l1836_OmniHuman_1_Rethinking_the_Scaling_Up_of_One_Stage_Conditioned_Human_Ani/figures/004_Table_2.jpg]]
*Table 2: Quantitative comparisons with audio-conditioned portrait animation baselines*

![[assets/figures/papers/paper_list_l1836_OmniHuman_1_Rethinking_the_Scaling_Up_of_One_Stage_Conditioned_Human_Ani/figures/005_Table_3.jpg]]
*Table 3: Quantitative comparisons with audio-conditioned body animation baselines*

![[assets/figures/papers/paper_list_l1836_OmniHuman_1_Rethinking_the_Scaling_Up_of_One_Stage_Conditioned_Human_Ani/figures/006_Table_4.jpg]]
*Table 4: Comparison with video-driven body animation methods*

![[assets/figures/papers/paper_list_l1836_OmniHuman_1_Rethinking_the_Scaling_Up_of_One_Stage_Conditioned_Human_Ani/figures/008_Figure_3.jpg]]
*Figure 3: Visual comparison with the pretrained image-tovideo model. Blue circle denotes the I2V model and green circle denotes the OmniHuman*

## 定位与知识库关联

### 与现有基线方法的关系

OmniHuman 的核心竞争定位是**单阶段、多条件驱动的人体动画扩散模型**，其方法谱系可沿两条轴线展开：肖像动画与身体动画。

在**音频驱动肖像动画**轴线上，现有方法普遍采用严格的数据过滤策略。以 **SadTalker** (Zhang et al., CVPR 2023) 为代表，该方法通过 3D 可变形模型解耦头部姿态与表情，但依赖高质量的唇音同步数据；**Hallo** (Xu et al., arXiv 2024) 和 **Vexpress** (Wang et al., arXiv 2024) 进一步引入扩散模型以提升生成质量，但同样受限于过滤后的小规模数据集。EchoMimic、Loopy、Hallo-3 等后续工作在特定维度上有所改进，却未突破数据利用率的根本瓶颈——这些方法通常仅能保留不足 10% 的原始训练数据。OmniHuman 通过引入文本、音频、姿态三种由弱到强的运动条件进行混合训练，使原本因唇音同步不合格而被丢弃的数据得以通过弱条件任务（如文本描述动作）被利用，从根本上改变了数据效率的约束条件。

在**音频驱动身体动画**轴线上，**CyberHost** (Lin et al., ICLR 2025) 是代表性的端到端方法，但其训练同样依赖严格的音频-运动对齐过滤。DiffTED、DiffGest + MimicMotion 等基线在特定手势生成或运动迁移任务上有所建树，但泛化到物体交互、多样化身体比例等场景时表现受限。OmniHuman 在 CyberHost 基准上取得 Sync-C 7.443、FVD 27.031、HKC 0.898，全面超越现有方法（Table 3），其优势根源于混合数据规模化训练带来的运动模式泛化能力。

在**视频驱动身体动画**轴线上，OmniHuman 与 DisCo、MimicMotion 等 pose-driven 方法形成交叉对比。值得注意的是，OmniHuman 虽非专为视频驱动设计，但在该设定下仍取得 IQA 4.111、FVD 7.318、AKD 2.136，大幅领先对比方法（Table 4），表明混合条件训练所学到的运动先验具有跨任务的迁移能力。

### 适用边界

OmniHuman 的适用边界由以下维度界定：

1. **输入模态支持**：支持任意宽高比和身体比例的参考图像，驱动信号以音频为主，可辅以文本描述和姿态骨架。单一模型即可覆盖从特写肖像到全身动画的生成需求，无需针对不同身体比例训练独立模型。

2. **生成能力范围**：涵盖头部运动、面部表情、手势生成和物体交互。在风格化人体和 2D 卡通角色上展现出良好的泛化能力（Figure 4），甚至可对非人类图像进行拟人化动画处理。

3. **推理控制**：采用分类器自由引导（CFG scale = 6.5），仅作用于音频和文本条件，不对姿态条件施加引导。支持长视频生成，通过将前一段最后五帧作为运动帧拼接到后续片段的噪声潜变量中实现时序延续。

4. **数据依赖边界**：模型的性能增益与混合数据的规模和质量正相关。当音频与身体运动相关性较弱时，可能出现不协调或过度夸张的动作；对于与训练分布差异显著的物体交互场景（如复杂手持物体操作），真实感仍有待提升。

### 局限与开放问题

**已识别的局限**：

- **音频-运动弱相关场景**：当驱动音频与身体运动的内在关联较弱时，模型可能产生不够协调或过分夸张的肢体动作。这源于模型仍主要依赖音频作为核心驱动信号，缺乏对运动合理性的显式约束机制。

- **物体交互的真实感**：对于训练分布之外的复杂物体交互（如精细的手持物体操作），生成结果的物理真实感不足。混合条件训练虽扩大了数据规模，但并未显式引入物理约束或交互先验。

- **运动控制的粒度**：当前模型不支持运动风格、情绪强度或语义意图等高级条件的显式注入，限制了在创意场景下的精细控制能力。

**开放问题**：

1. **运动合理性增强**：如何在保持数据规模优势的同时，减少音频驱动下的不协调或夸张运动？可能的路径包括引入物理模拟器作为判别器、或在训练中显式建模音频-运动的因果结构。

2. **物体交互泛化**：如何提升模型对未见过的物体交互场景的泛化力？这可能需要融合 3D 物体先验、手-物接触建模，或引入交互数据的针对性增强策略。

3. **细粒度运动控制**：能否将运动风格、情绪强度、语义意图等更丰富的条件融入混合训练框架？这需要在条件设计层面进行扩展，同时避免破坏现有混合训练带来的数据效率优势。

4. **规模化验证**：OmniHuman 的核心理念——通过混合弱条件利用大规模数据——暗示着潜在的 Scaling Law。在数万小时级别的视频数据下，模型的运动生成能力和泛化边界将如何演化？训练效率的优化（如条件比例的动态调整策略）也是规模化过程中需要解决的问题。

5. **评估体系的完善**：当前评估主要依赖自动指标（IQA、FID、FVD、Sync-C 等），缺乏大规模用户研究对运动自然度和生成偏好的主观验证。建立更全面的评估基准，特别是针对手势质量和物体交互真实感的细粒度指标，是推动该方向发展的基础性工作。

## 原文 PDF

![[paperPDFs/arxiv_2025/OmniHuman_1_Rethinking_the_Scaling_Up_of_One_Stage_Conditioned_Human_Animation_Models.pdf]]
