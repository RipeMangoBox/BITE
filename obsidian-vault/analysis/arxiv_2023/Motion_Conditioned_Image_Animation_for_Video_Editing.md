---
title: Motion-Conditioned Image Animation for Video Editing
type: paper
paper_level: A
venue: arXiv
year: 2023
pdf_ref: paperPDFs/arxiv_2023/Motion_Conditioned_Image_Animation_for_Video_Editing.pdf
aliases:
- MMCIA
- MCIAVE
tags:
- arxiv_2023
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/image_and_video_generation
- topic/benchmarks_datasets_evaluation
core_operator: 光流运动条件的使用与选择性丢弃：在空间编辑时保留光流以忠实重现源视频运动，在运动编辑时丢弃光流（s_M=0）以允许生成全新的运动模式。
primary_logic: 将视频编辑解耦为“现成图像编辑器对首帧进行编辑”+“基于光流运动条件的视频扩散模型进行图像动画”，以简单范式同时实现高质量的空间编辑和灵活的运动编辑。
claims:
- 在包含271个编辑任务的自建VideoEdit基准上，人类评估中MoCA在所有编辑类型下的总体偏好度均显著超过对比方法（如与VideoComposer对比时偏好度达82%）。
- 在运动编辑子任务上，MoCA远超所有基线（如对Gen-1的偏好度达99%），证明了其处理运动编辑的突出能力。
- 自动评估指标M_geo（VideoCLIP）与人类判断的Spearman相关性最高（总0.203），且MoCA在大多数编辑类型上取得最优M_geo值。
- 人类评估者选择MoCA的主要原因是对编辑提示的对齐更好，而非仅保持源视频一致性，印证了方法对编辑目的的有效达成。
---

# Motion-Conditioned Image Animation for Video Editing

> [!tip] 核心洞察
> 将视频编辑解耦为“现成图像编辑器对首帧进行编辑”+“基于光流运动条件的视频扩散模型进行图像动画”，以简单范式同时实现高质量的空间编辑和灵活的运动编辑。

| 字段 | 内容 |
|------|------|
| 中文题名 | 面向视频编辑的运动条件图像动画 |
| 英文题名 | Motion-Conditioned Image Animation for Video Editing |
| 会议/期刊 | arXiv 2023 |
| Links | [paper](https://arxiv.org/abs/2311.18827) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/image_and_video_generation #topic/benchmarks_datasets_evaluation |
| Method | MoCA (Motion-Conditioned Image Animation) |
| Dataset | VideoEdit Benchmark |

> [!tip] 效果简介
> - VideoEdit Benchmark (Overall) 上，Human Preference Win-Rate 82% vs VideoComposer vs 18% (+64%)。
> - VideoEdit Benchmark (Motion Edits) 上，Human Preference Win-Rate 99% vs Gen-1 vs 1% (+98%)。
> - VideoEdit Benchmark (Style Edits) 上，M_geo (VideoCLIP) 0.331 vs 0.259 (VideoComposer) (+0.072)。

## 概述

视频编辑旨在同时修改视频的视觉外观与运动模式，但现有方法普遍将运动编辑视为次要问题，且缺乏统一、全面的评估基准，使得不同方法的能力难以公平比较。针对这一瓶颈，**MoCA (Motion-Conditioned Image Animation)** 提出将视频编辑解耦为两个子任务：首先利用现成的文本驱动图像编辑器修改首帧，然后通过一个以光流为运动条件的视频扩散模型将编辑后的首帧“动画化”为完整视频。这一范式将空间编辑与运动生成分离，既保证了高质量的空间编辑，又实现了灵活的运动控制。

该方法的核心因果机制在于光流运动条件的选择性使用：对于需要忠实重现源视频运动的空间编辑（如物体替换、风格转换），保留光流条件以引导模型生成与源视频一致的运动轨迹；而对于需要改变运动模式的运动编辑，则通过将运动引导尺度 $s_M$ 设置为零来丢弃光流条件，使模型能够生成全新的运动。这种“条件开关”由一个三条件无分类器引导公式实现：

$$
\widetilde{v}_{\theta}(z_t, c_M, c_T, c_I) = v_{\theta}(z_t, \emptyset, \emptyset, \emptyset) + s_I \cdot (v_{\theta}(z_t, \emptyset, \emptyset, c_I) - v_{\theta}(z_t, \emptyset, \emptyset, \emptyset)) + s_T \cdot (v_{\theta}(z_t, \emptyset, c_T, c_I) - v_{\theta}(z_t, \emptyset, \emptyset, c_I)) + s_M \cdot (v_{\theta}(z_t, c_M, c_T, c_I) - v_{\theta}(z_t, \emptyset, c_T, c_I))
$$

该公式通过三个独立的引导尺度 $s_I$、$s_T$、$s_M$ 分别控制对图像、文本和运动条件的忠实度，为编辑提供了精细的调控能力。

在自建的 **VideoEdit 基准**（包含271个编辑任务，涵盖物体替换、风格变化、背景编辑、运动编辑等多种类型）上，MoCA 展现出显著优势。人类评估中，MoCA 的总体偏好度较 **VideoComposer**（Wang et al., arXiv 2023）达到 82%，在运动编辑子任务上对 **Gen-1**（Esser et al., arXiv 2023）的偏好度高达 99%。自动评估指标方面，基于 VideoCLIP 的几何相似度 $M_{geo}$ 与人类判断的 Spearman 相关性最高（总体 0.203），且 MoCA 在多数编辑类型上取得最优 $M_{geo}$ 值。人类评估者的选择归因分析进一步表明，MoCA 被偏好的主要原因是对编辑提示的对齐更好，而非仅保持源视频一致性，印证了方法对编辑目的的有效达成。

在方法谱系中，MoCA 区别于端到端的视频编辑方法（如 **Tune-A-Video**、**Dreamix**）和基于注意力传播的方法（如 **TokenFlow**、**MasaCtrl**），其核心创新在于显式的“图像编辑+运动条件动画”分解范式，以及在大规模视频-文本数据（3400万视频-文本对）上微调 14 亿参数视频扩散模型的训练策略。这一设计使其在空间编辑和运动编辑上均表现出色，但也存在若干局限：编辑质量依赖首帧图像编辑的成功与否；对于长视频或显著相机运动场景，仅以首帧和全局光流表示可能丢失后续帧的细节；自动评估指标与人类判断的对齐度有限（尤其在运动编辑上），可靠评估仍需依赖人工评测。

## 背景与动机

视频编辑旨在对给定的源视频施加语义变化，使其在保持源内容一致性的同时，忠实地反映编辑提示所描述的目标状态。这一任务在视频创作、内容重定向和视觉特效等领域具有广泛的应用前景。然而，现有方法普遍面临一个核心瓶颈：**运动编辑的缺失与评估体系的碎片化**。大多数视频编辑方法——无论是基于文本到图像扩散模型的免调方法（如 **TokenFlow**，Geyer et al., arXiv 2023），还是通过单视频微调实现编辑的方法（如 **Tune-A-Video**，Wu et al., ICCV 2023）——都将注意力集中在空间属性的修改上（如替换物体、改变背景或风格），而几乎完全忽视了对视频中运动模式的编辑。当用户希望改变物体的运动轨迹、速度或运动类型时，这些方法往往无能为力。

这一缺口源于现有方法对运动信息处理方式的根本局限。以 **Gen-1**（Esser et al., arXiv 2023）为代表的方法依赖深度图或边缘图作为结构条件，其设计初衷是保留源视频的空间结构，而非改变运动模式。**Dreamix**（Molad et al., arXiv 2023）通过微调文本到视频扩散模型实现编辑，但运动编辑能力同样受限。**VideoComposer**（Wang et al., arXiv 2023）虽然支持多条件控制，但其合成式框架并未显式解耦运动与外观。这些方法的共同缺陷在于：运动和外观被耦合在统一的生成过程中，导致对其中任一维度的独立编辑都变得困难。

与此同时，视频编辑领域长期缺乏统一、全面的评估基准。各方法在不同的数据集、编辑类型和评估指标上报告结果，使得方法间的能力无法进行公平比较。特别是，运动编辑任务在现有基准中几乎不存在，这进一步加剧了对运动编辑能力评估的空白。

MoCA的提出正是为了填补上述双重缺口。其核心动机可概括为两点：**（1）将运动编辑纳入视频编辑的核心能力范畴，而不仅仅是空间属性的修改；（2）建立一个涵盖多种编辑类型的统一评估框架，使不同方法的运动编辑和空间编辑能力得以公平比较。** 为实现这一目标，MoCA采用了一种简洁而有效的范式：将视频编辑解耦为“现成图像编辑器对首帧进行空间编辑”+“基于光流运动条件的视频扩散模型进行图像动画”。这一分解使得空间编辑和运动编辑可以独立控制——在空间编辑时保留光流以忠实重现源视频运动，在运动编辑时丢弃光流以允许生成全新的运动模式。

## 核心创新

MoCA的核心创新在于将视频编辑问题**解耦为两个独立阶段**：首帧图像编辑与运动条件图像动画。这一范式与现有端到端或基于注意力传播的方法（如**TokenFlow** (Geyer et al., arXiv 2023)、**Tune-A-Video** (Wu et al., ICCV 2023)）形成根本性差异——后者不显式分解空间编辑与运动生成，导致编辑灵活性和运动控制能力受限。

### 编辑范式解耦

传统视频编辑方法将空间内容修改和时间一致性维护耦合在同一生成过程中。MoCA则采用“现成图像编辑器修改首帧 + 视频扩散模型基于运动条件生成后续帧”的策略。这一解耦带来两个关键优势：

1. **空间编辑的灵活性**：首帧编辑可借助任意成熟的文本驱动图像编辑技术（如Prompt-to-Prompt或SDEdit），无需针对视频编辑重新设计空间修改机制。
2. **运动控制的独立性**：运动生成由专门的条件视频扩散模型负责，其输入包括编辑后的首帧图像、文本描述以及从源视频提取的运动条件，使得空间编辑和运动生成可以独立优化。

### 光流运动条件与选择性丢弃

MoCA引入的**运动条件机制**是其区别于所有基线方法的核心技术槽位。具体而言：

- **运动条件构建**：使用预训练RAFT模型从源视频提取光流，将其编码为RGB视频表示，并与平均流幅度一同作为扩散模型的条件输入。这使模型能够显式感知并重现源视频中的运动模式。
- **选择性丢弃策略**：通过无分类器引导公式中的运动引导尺度 $s_M$ 实现精细控制。在空间编辑任务中，保持 $s_M > 0$ 以忠实重现源视频运动；在运动编辑任务中，设置 $s_M = 0$ 丢弃运动条件，使模型能够生成与源视频完全不同的全新运动模式。

三条件无分类器引导公式为：

$$
\widetilde{v}_{\theta}(z_t, c_M, c_T, c_I) = v_{\theta}(z_t, \emptyset, \emptyset, \emptyset) + s_I \cdot (v_{\theta}(z_t, \emptyset, \emptyset, c_I) - v_{\theta}(z_t, \emptyset, \emptyset, \emptyset)) + s_T \cdot (v_{\theta}(z_t, \emptyset, c_T, c_I) - v_{\theta}(z_t, \emptyset, \emptyset, c_I)) + s_M \cdot (v_{\theta}(z_t, c_M, c_T, c_I) - v_{\theta}(z_t, \emptyset, c_T, c_I))
$$

该公式通过三个独立引导尺度 $s_I$、$s_T$、$s_M$ 分别控制对图像条件、文本条件和运动条件的忠实度。当 $s_M = 0$ 时，运动条件项被完全移除，模型仅依赖文本和图像条件生成运动，这是MoCA能够处理运动编辑任务的关键机制。

### 与基线的关键差异对比

| 技术槽位 | 基线方法 | MoCA方案 |
|---|---|---|
| 编辑范式 | 端到端或基于注意力的视频编辑，不显式分解 | 分解为首帧图像编辑 + 运动条件图像动画 |
| 运动条件 | 通常无显式运动条件，依赖深度/边缘图保持结构 | 使用RAFT光流RGB编码和平均流幅度作为运动条件，运动编辑时通过 $s_M=0$ 丢弃 |
| 模型训练与规模 | 多数使用预训练T2I模型，少量微调或零样本 | 在34M视频-文本对上微调1.4B参数视频扩散模型，从4亿图文对预训练模型初始化 |

### 证据支撑

消融实验证实了运动条件的有效性：在空间编辑任务中，带运动条件的编辑在人类偏好比较中被选中的比例达到57%-60%（Table 5），表明运动条件有助于保持源视频的运动特征。在运动编辑任务中，通过设置 $s_M=0$ 丢弃运动条件，MoCA成功实现了与源视频不同的全新运动生成，在人类评估中对**Gen-1** (Esser et al., arXiv 2023) 的偏好度高达99%（Table 2），远超所有基线方法。

## 整体框架

MoCA 将视频编辑任务解耦为两个阶段：**图像编辑**与**运动条件图像动画**。这一分解范式的核心动机在于，现有视频编辑方法普遍将空间编辑与运动编辑耦合在一起处理，导致在需要改变运动模式的场景下性能急剧下降。通过显式分离，MoCA 得以在空间编辑时忠实重现源视频运动，而在运动编辑时灵活丢弃运动条件以生成全新运动。

### Pipeline 模块关系与数据流

整体流程如 Figure 2 所示，包含四个核心模块，按数据流顺序依次为：

![[assets/figures/papers/paper_list_l1056_https_arxiv_org_abs_2311_18827/figures/003_Figure_2.jpg]]
*Figure 2: An overview of MoCA. Given a source video, we compute its optical flow, and apply image editing techniques on the first frame. To produce the resulting video edit, we sample our model conditioned on motion, the edited first frame, and the edit caption. For motion-based edits, we dropout the optical flow conditioning*

**1. 图像编辑模块**
利用现成的文本驱动图像编辑器（如 Prompt-to-Prompt 或 SDEdit）对源视频的首帧进行编辑。该模块接收源视频首帧与编辑提示，输出编辑后的首帧图像。这是整个编辑链路的起点——后续所有帧的生成均以此编辑首帧为图像条件。

**2. 光流提取模块**
使用预训练的 RAFT 模型从源视频中逐帧计算光流，并将其转换为 RGB 编码的光流视频以及平均流幅度。这两者共同构成**运动条件** $c_M$，用于向后续的扩散模型注入源视频的运动信息。

**3. 条件视频扩散模型**
这是 MoCA 的核心生成模块。模型基于潜空间扩散架构，同时接受三个条件输入：
- **文本条件** $c_T$：编辑提示的文本嵌入
- **图像条件** $c_I$：编辑后的首帧图像
- **运动条件** $c_M$：光流 RGB 视频与平均流幅度

模型从纯噪声开始，在潜空间中进行去噪采样，逐步生成与条件一致的视频帧序列。训练时，模型在 3400 万视频-文本对上微调，从 4 亿图文对预训练的文本到图像模型初始化，拥有 14 亿可训练参数。

**4. 无分类器引导模块**
为了精细控制生成视频对三类条件的忠实度，MoCA 引入了三个独立的引导尺度，对应三条件无分类器引导公式：

$$
\widetilde{v}_{\theta}(z_t, c_M, c_T, c_I) = v_{\theta}(z_t, \emptyset, \emptyset, \emptyset) + s_I \cdot (v_{\theta}(z_t, \emptyset, \emptyset, c_I) - v_{\theta}(z_t, \emptyset, \emptyset, \emptyset)) + s_T \cdot (v_{\theta}(z_t, \emptyset, c_T, c_I) - v_{\theta}(z_t, \emptyset, \emptyset, c_I)) + s_M \cdot (v_{\theta}(z_t, c_M, c_T, c_I) - v_{\theta}(z_t, \emptyset, c_T, c_I))
$$

其中 $s_I$、$s_T$、$s_M$ 分别控制对图像、文本、运动条件的忠实度。这一设计的关键在于 **$s_M$ 的可选择性丢弃**：在空间编辑（如物体替换、风格变化）时，保留 $s_M > 0$ 以忠实重现源视频运动；在运动编辑时，设置 $s_M = 0$ 完全丢弃运动条件，使模型能够生成与源视频不同的全新运动模式。

### 范式优势与机制瓶颈

该分解范式的核心优势在于**编辑灵活性与生成质量的统一**。图像编辑阶段可以充分利用日益成熟的图像编辑技术，而运动条件图像动画阶段则通过大规模视频预训练获得了稳健的运动生成能力。两者解耦后，任何一方的技术进步都可以直接提升整体编辑效果。

然而，这一范式也存在结构性瓶颈：整个生成过程强依赖于首帧编辑质量——若首帧编辑失败，错误将通过图像条件传播至所有后续帧。此外，对于长视频或存在显著相机运动的场景，仅以首帧和全局光流表示可能无法保持源视频中后出现的内容和细节，这是该框架的固有局限。

## 核心模块与公式推导

MoCA 将视频编辑解耦为两个正交阶段：**图像编辑**与**运动条件图像动画**。其核心由四个模块构成，协同实现空间编辑与运动编辑的统一。

### 1. 图像编辑模块

该模块利用现成的文本驱动图像编辑器（如 Prompt-to-Prompt 或 SDEdit）对源视频的首帧进行编辑。编辑后的首帧 $c_I$ 作为后续视频生成的空间锚点，决定了编辑视频的视觉内容。该模块的选择是即插即用的，其输出质量直接影响后续帧的生成质量——若首帧编辑失败，错误将逐帧传播。

### 2. 光流运动条件提取模块

使用预训练的 RAFT 模型从源视频中逐帧提取光流，并将其转换为 RGB 编码的视频 $c_M$，同时计算平均光流幅度作为辅助条件。这一显式运动表示构成了方法的“因果旋钮”：在空间编辑时保留 $c_M$ 以忠实重现源视频运动；在运动编辑时通过设置引导尺度 $s_M = 0$ 丢弃该条件，使模型生成全新的运动模式。

### 3. 条件视频扩散模型

模型主体是一个在潜空间中运行的视频扩散模型，以三个条件作为输入：
- **文本条件** $c_T$：编辑提示的文本编码
- **图像条件** $c_I$：编辑后的首帧图像编码
- **运动条件** $c_M$：光流 RGB 编码

模型从预训练的文本到图像 U-Net 初始化（4亿图文对预训练），并在3400万视频-文本对上微调所有时空层，总计 1.4B 可训练参数。训练时使用 256×256 分辨率、4 fps 的 2 秒视频片段，通过预训练 VAE 编码至 4×8×32×32 的潜空间。

### 4. 三条件无分类器引导模块

这是方法实现精细控制的关键公式。对于三个条件 $c_I$、$c_T$、$c_M$，引导后的速度预测 $\widetilde{v}_{\theta}$ 定义为：

$$\widetilde{v}_{\theta}(z_t, c_M, c_T, c_I) = v_{\theta}(z_t, \emptyset, \emptyset, \emptyset) + s_I \cdot (v_{\theta}(z_t, \emptyset, \emptyset, c_I) - v_{\theta}(z_t, \emptyset, \emptyset, \emptyset)) + s_T \cdot (v_{\theta}(z_t, \emptyset, c_T, c_I) - v_{\theta}(z_t, \emptyset, \emptyset, c_I)) + s_M \cdot (v_{\theta}(z_t, c_M, c_T, c_I) - v_{\theta}(z_t, \emptyset, c_T, c_I))$$

其中：
- $z_t$：时刻 $t$ 的噪声潜变量
- $v_{\theta}$：模型预测的速度场
- $s_I$：图像条件引导尺度，控制对编辑首帧的忠实度
- $s_T$：文本条件引导尺度，控制对编辑提示的对齐度
- $s_M$：运动条件引导尺度，控制对源视频运动的忠实度

该公式通过逐步叠加各条件的预测差值，实现了对三个条件的独立控制。**运动编辑的关键机制**在于：当 $s_M = 0$ 时，运动条件项 $(v_{\theta}(z_t, c_M, c_T, c_I) - v_{\theta}(z_t, \emptyset, c_T, c_I))$ 被完全丢弃，模型仅依赖图像和文本条件生成视频，从而摆脱源视频运动的约束，产生全新的运动模式。消融实验证实了这一机制的有效性：在空间编辑中保留运动条件可使人类偏好度达到 57%-60%（Table 5），而在运动编辑中丢弃运动条件则成功实现了与源视频不同的运动生成。

### 补充图表

![[assets/figures/papers/paper_list_l1056_https_arxiv_org_abs_2311_18827/figures/010_Figure_5.jpg]]
*Figure 5: MoCA edits for “A boat sailing on the moon" with and without motion conditioning. Using motion conditioning allows the model to more faithfully follow the boat’s movement in the original source video. Without motion conditioning, the model tends to generate more random movement directions, such as moving backwards*

## 实验与分析

### 主实验结果

MoCA在自建的VideoEdit基准上进行了全面的人类评估，该基准包含271个编辑任务，覆盖物体替换、风格变化、背景编辑、运动编辑等多种类型（Table 1）。人类评估采用二元选择范式，评估者需在MoCA与各基线方法之间做出偏好判断，并可从“编辑提示对齐更好”“源视频一致性更高”“两者兼有”三个归因选项中选择偏好原因。

**总体偏好度。** 如Table 2所示，MoCA在所有编辑类型的总体人类偏好度上显著超越所有对比方法。与最强的合成式基线**VideoComposer**（Wang et al., arXiv 2023）对比时，MoCA的偏好度达到**82%**（vs 18%），优势幅度为+64个百分点。与基于深度图条件的**Gen-1**（Esser et al., arXiv 2023）对比时偏好度为71%，与基于文本到图像扩散模型的免调方法**TokenFlow**（Geyer et al., arXiv 2023）对比时为76%，均表现出稳定且显著的优势。

**运动编辑的突出表现。** 在运动编辑子任务上，MoCA的优势尤为突出。与Gen-1对比时，人类偏好度高达**99%**（vs 1%），与**Dreamix**（Molad et al., arXiv 2023）对比时为90%。这一极端差距印证了MoCA的核心设计——通过光流运动条件的选择性丢弃（$s_M=0$），模型能够生成与源视频完全不同的全新运动模式，而现有基线方法普遍缺乏对运动编辑的显式建模能力。

**背景编辑的例外情况。** 值得注意的是，在背景编辑任务上，Gen-1的人类偏好度略优于MoCA（60% vs 40%）。这表明在需要严格保留源视频结构信息的场景下，基于深度图的结构条件仍具有独特价值，而MoCA仅依赖首帧图像和光流可能不足以完全约束背景的几何一致性。

**偏好归因分析。** Figure 4揭示了人类评估者选择MoCA的主要原因分布。与各基线对比时，评估者选择MoCA的首要原因始终是“对编辑提示的对齐更好”，而非“源视频一致性更高”。这意味着MoCA的优势并非来自保守地保留源视频内容，而是真正有效地达成了用户指定的编辑目标，这直接验证了方法设计的有效性。

### 自动评估与人类判断的一致性

论文采用了三个基于CLIP的自动评估指标：$M_{sim}$（源视频与编辑视频的CLIP特征余弦相似度，衡量内容保留度）、$M_{dir}$（文本与视频特征变化方向的一致性，衡量编辑与提示的对齐度）以及$M_{geo} = \sqrt{M_{sim} \cdot M_{dir}}$（几何平均，综合评估编辑质量）。此外还引入了基于VideoCLIP的版本以更好地捕捉时序特征。

**自动指标的局限性。** Table 3以人类二元判断为真值标签，评估了各自动指标的分类准确率。结果显示，自动指标在空间编辑（物体、风格、背景）上的分类准确率可达70%-80%，但在运动编辑上仅约56%，接近随机猜测水平（50%）。Table 6的Spearman相关性分析进一步表明，$M_{geo}$（VideoCLIP）与人类判断的总相关性最高（0.203），但在运动编辑子集上相关性仅约0.14。这一发现揭示了现有自动评估指标的严重不足：它们无法可靠地评估运动编辑质量，可靠的评估仍需依赖人工评测。

**MoCA在自动指标上的表现。** 尽管自动指标存在局限性，Table 7的分类型$M_{geo}$结果显示，MoCA在大多数编辑类型上仍取得最优值：风格编辑0.331（vs VideoComposer 0.259）、背景编辑0.375（vs VideoComposer 0.328）、物体编辑0.370（vs Dreamix 0.356）。这从自动评估角度佐证了MoCA的综合优势。

### 消融实验

**运动条件的作用。** Table 5展示了运动条件的消融实验结果。在空间编辑任务中，保留运动条件的编辑在人类偏好比较中被选中的比例为57%-60%，表明光流条件对忠实重现源视频运动具有正面作用。Figure 5以“月球上航行的船”为例进行了定性展示：带运动条件时，编辑后的船运动方向与源视频一致；丢弃运动条件后，模型倾向于生成随机的运动方向（如向后行驶）。

**运动编辑中的条件丢弃。** 在运动编辑任务中，MoCA通过设置引导尺度$s_M=0$来丢弃光流条件，从而允许模型生成与源视频不同的全新运动。消融实验证实了这一机制的有效性，使得MoCA成为唯一能够灵活处理运动编辑的方法。

### 失败模式与局限性

尽管MoCA在整体上表现优异，实验和分析揭示了以下局限：

1. **首帧编辑质量依赖。** 方法将视频编辑分解为首帧图像编辑+后续帧动画，因此首帧编辑的质量直接影响整个输出视频。若现成图像编辑器在首帧上失败（如物体替换时边界不自然、风格迁移时细节丢失），错误将通过运动条件传播到所有后续帧。

2. **长视频与相机运动。** 当前模型训练使用2秒、4fps的短视频片段，仅以首帧图像和全局光流表示运动。对于较长视频或存在显著相机运动的场景，源视频中未出现在首帧的内容（如后期进入画面的人物或物体）无法被条件信号捕捉，导致保真度下降。

3. **光流精度限制。** 运动条件依赖于预训练RAFT模型提取的光流，在复杂运动、严重遮挡或大位移场景下，光流估计可能出现不准确，进而影响运动条件的质量并导致生成视频出现运动伪影。

4. **自动评估的不可靠性。** 如Table 3和Table 6所示，现有自动指标与人类判断的对齐度有限，尤其在运动编辑上几乎失效。这意味着该领域仍缺乏可靠的自动化评估手段，研究结论高度依赖昂贵的人类评估。

### 公平性说明

为确保比较的公平性，论文对每个基线方法均进行了超参数扫描（Section 5.3），以各方法在VideoEdit基准上的最佳表现参与对比。人类评估采用三元归因选项设计，减少了评估者因单一维度偏好而产生的偏差。但需注意，自动评估指标的系统性局限意味着Table 4和Table 7中的自动分数应谨慎解读，不能替代人类判断作为编辑质量的最终衡量标准。

### 补充图表

![[assets/figures/papers/paper_list_l1056_https_arxiv_org_abs_2311_18827/figures/006_Table_2.jpg]]
*Table 2: Human evaluation results for preference of our method over each of the baselines. User ratings generally show greater preference for our method, with the exception of Gen-1 for background edits, and Drea mix for multi-spatial edits*

![[assets/figures/papers/paper_list_l1056_https_arxiv_org_abs_2311_18827/figures/008_Figure_4.jpg]]
*Figure 4: Percentage of each reason selected when human evaluators prefer MoCA edits to each of the baselines. The reasons for picking one model over another on each video edit could be either its better alignment with the edit prompt, higher consistency with the source video, or both. Generally, human raters preferred our method in terms of better alignment with the desired edit prompt*

![[assets/figures/papers/paper_list_l1056_https_arxiv_org_abs_2311_18827/figures/017_Table_7.jpg]]
*Table 7: The results confirm the superiority of MoCA to other methods for all edit tasks. Additionally, we analyze the Spearman correlation [33] between automatic metrics introduced in Section 5.5 and human judgements. The results in Table 6 suggest the VideoCLIP based*

![[assets/figures/papers/paper_list_l1056_https_arxiv_org_abs_2311_18827/figures/018_Table_7.jpg]]
*Table 7: Continued automatic metric results and correlation analysis for MoCA video-editing evaluation.*

![[assets/figures/papers/paper_list_l1056_https_arxiv_org_abs_2311_18827/figures/002_Figure_1.jpg]]
*Figure 1: is able to generate a diverse range of edits, such as object replacement, style changes, and motion edits. The frames in the top row in each example represent the source video while the bottom ones show the edited frames by MoCA. The source and editing prompts are shown above each example*

![[assets/figures/papers/paper_list_l1056_https_arxiv_org_abs_2311_18827/figures/007_Table_3.jpg]]
*Table 3: Classification accuracy of each CLIP-based automatic metric, considering binary human decisions comparing MoCA edits against different baselines as the ground truth labels. Note that random guessing achieves roughly 50% accuracy*

![[assets/figures/papers/paper_list_l1056_https_arxiv_org_abs_2311_18827/figures/009_Table_4.jpg]]
*Table 4: Automatic scores evaluating the editing quality of each model. We compute the VideoCILP-based Mdir and*

![[assets/figures/papers/paper_list_l1056_https_arxiv_org_abs_2311_18827/figures/014_Figure_9.jpg]]
*Figure 9: Comparisons for multi-spatial video edit prompts*

## 方法谱系与知识库定位

### 编辑范式谱系：从端到端到解耦式生成

MoCA 的核心范式创新在于将视频编辑显式分解为 **首帧图像编辑 + 运动条件图像动画** 两个独立阶段。这一设计使其在方法谱系中处于独特的交叉位置：

- **端到端视频编辑方法**（如 **Tune-A-Video** (Wu et al., ICCV 2023)、**Dreamix** (Molad et al., arXiv 2023)）通常通过对预训练文本到图像/视频扩散模型进行微调或注入注意力操作来实现编辑，不显式分离空间编辑与运动生成。这类方法在处理运动编辑时面临根本性困难：模型需要同时改变外观和运动模式，而训练信号中缺乏对二者的解耦监督。
- **基于结构条件的视频生成方法**（如 **Gen-1** (Esser et al., arXiv 2023) 使用深度图、**VideoComposer** (Wang et al., arXiv 2023) 使用多模态条件）虽然引入了显式条件控制，但其条件（深度、边缘等）主要服务于结构保留，而非运动表示。这导致它们在运动编辑任务上表现受限——深度图可以约束空间结构，但无法灵活指定新的运动模式。
- **基于注意力的免调视频编辑方法**（如 **TokenFlow** (Geyer et al., arXiv 2023)、**MasaCtrl** (Cao et al., arXiv 2023)）通过跨帧注意力传播实现零样本编辑，避免了单视频微调，但其编辑能力受限于注意力机制的固有约束，难以实现大幅度的运动变化。

MoCA 的解耦策略绕开了上述困境：图像编辑阶段可借助任意成熟的文本驱动图像编辑器（如 Prompt-to-Prompt 或 SDEdit），运动生成阶段则通过光流条件独立控制。更重要的是，**运动编辑时通过设置引导尺度 $s_M = 0$ 丢弃光流条件**，使模型能够生成与源视频完全不同的运动模式——这一“选择性丢弃”机制是 MoCA 在运动编辑上远超基线（如对 Gen-1 的人类偏好度达 99%）的关键因果旋钮。

### 运动表示选择的影响

MoCA 选择 **RAFT 预训练模型提取的稠密光流** 作为运动条件，并将其编码为 RGB 视频格式与平均流幅度。这一设计在运动表示谱系中处于显式、可丢弃的中间位置：

- 相比 **隐式运动表示**（如可学习的时序嵌入），显式光流具备可解释性和可控性——运动编辑时直接丢弃条件即可，无需设计额外的解耦损失。
- 相比 **稀疏关键点或轨迹**，稠密光流保留了更丰富的运动细节，但代价是对 RAFT 模型精度的依赖。在复杂运动、遮挡或大位移场景下，光流估计的不准确会直接传播为运动条件的噪声，这是方法的一个已知脆弱点。
- 相比 **深度图或边缘图等结构条件**，光流直接编码运动信息，而非空间结构，因此在运动编辑任务上具有天然优势。

### 训练数据与模型规模的定位

MoCA 在 **34M 视频-文本对** 上微调了一个 **1.4B 参数** 的视频扩散模型，该模型从 **4 亿图文对** 预训练的文本到图像模型初始化。这一规模在方法谱系中值得注意：

- 对比 **Tune-A-Video** 等单视频微调方法（每个视频仅需少量微调），MoCA 的大规模预训练使其具备更强的泛化能力，但代价是需要大量视频数据。
- 对比 **VideoComposer** 等合成式方法，MoCA 的模型规模更大（1.4B 可训练参数），这可能部分解释了其在人类评估中的整体优势（总体偏好度 82% vs VideoComposer）。
- 训练时使用 **2 秒片段、4 fps、256×256 分辨率**，编码至 $4 \times 8 \times 32 \times 32$ 的潜空间。这一设置限制了方法对长视频和包含显著相机运动场景的适用性——仅以首帧和全局光流表示可能无法保持源视频中后出现的内容和细节。

### 适用边界与已知局限

1. **首帧编辑质量的级联依赖**：MoCA 将首帧编辑结果作为后续所有帧的条件输入。若首帧编辑失败（如物体形状错误、纹理不自然），错误将通过运动条件传播到整个视频。这是解耦范式的固有风险。

2. **长视频与多镜头场景的保真度不足**：当前设计仅以首帧图像和全局光流表示整个视频，对于较长视频或包含多镜头切换的场景，未出现在首帧的内容无法被有效保持。这一局限指向了未来工作的一个明确方向。

3. **光流估计的鲁棒性边界**：RAFT 模型在复杂运动、遮挡、大位移场景下可能出现不准确估计，影响运动条件的质量。这在实际应用中可能表现为运动编辑结果与预期存在偏差。

4. **自动评估指标的可靠性缺口**：实验表明，自动指标与人类判断的相关性有限，尤其在运动编辑上（Spearman 相关系数仅约 0.14）。这意味着当前依赖自动指标的快速迭代存在误导风险，可靠评估仍需人工评测。

### 开放问题与潜在延伸

- **更灵活的运动表示**：能否通过学习或更灵活的隐式运动表示替代显式光流，在保留可丢弃性的同时提升复杂运动编辑的泛化能力？这需要在可控性和表达能力之间寻找新的平衡点。

- **长视频扩展**：如何将 MoCA 扩展到长视频或包含多镜头切换的场景？可能的方向包括分段处理、层次化运动表示，或引入时序记忆机制以保持首帧之后出现的内容。

- **更可靠的自动评估**：如何设计更准确、与人类判断更一致的视频编辑自动评估指标？当前 VideoCLIP 基指标在运动编辑上的低相关性表明，需要专门针对运动感知的视频理解模型。

- **与更先进图像编辑器的协同**：结合更先进的图像编辑技术（如 InstructPix2Pix）能否进一步提升 MoCA 在特殊编辑类型（如大幅姿态变化）上的表现？这需要在实验中验证。

## 原文 PDF

![[paperPDFs/arxiv_2023/Motion_Conditioned_Image_Animation_for_Video_Editing.pdf]]