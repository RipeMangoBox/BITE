---
title: "EgoEdit: Dataset, Real-Time Streaming Model, and Benchmark for Egocentric Video Editing"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/EgoEdit_Dataset_Real_Time_Streaming_Model_and_Benchmark_for_Egocentric_Video_Editing.pdf
project_link: "https://snap-research.github.io/EgoEdit"
code_link: null
aliases:
- EER
- EgoEdit
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/benchmarks_datasets_evaluation
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: 构建高质量、域匹配的 egocentric 视频编辑数据集（EgoEditData），并结合通道级源视频条件注入和自强制蒸馏（Self-Forcing）实现低延迟实时推理。
primary_logic: 通过手动策展的 egocentric 编辑对数据集聚焦于手-物交互场景，并利用通道拼接代替序列拼接以保持低计算开销，同时采用双向 DMD 与自强制方法将教师模型蒸馏为单 GPU 上 855ms 首帧延迟的实时自回归生成器，从而弥合域差距并实现交互式 AR 编辑。
claims:
- EgoEditData 显著提升在 egocentric 编辑基准 EgoEditBench 上的性能，VLM 分数从 4.87（0%数据）提升至 7.85（100%数据）。
- EgoEdit 使用通道级拼接（channel-wise concatenation）避免了序列拼接导致的自注意力开销，使计算成本接近基座模型。
- 经过双向 DMD 和自强制蒸馏后，模型在单个 H100 GPU 上达到 38.1 fps、首帧延迟 855ms，支持实时 AR 交互。
- EgoEditBench 上 VLM = 7.76 (EgoEdit)
---

# EgoEdit: Dataset, Real-Time Streaming Model, and Benchmark for Egocentric Video Editing

> [!tip] 核心洞察
> 通过手动策展的 egocentric 编辑对数据集聚焦于手-物交互场景，并利用通道拼接代替序列拼接以保持低计算开销，同时采用双向 DMD 与自强制方法将教师模型蒸馏为单 GPU 上 855ms 首帧延迟的实时自回归生成器，从而弥合域差距并实现交互式 AR 编辑。

| 字段 | 内容 |
|------|------|
| 中文题名 | EgoEdit：面向第一人称视频编辑的数据集、实时流式模型与基准 |
| 英文题名 | EgoEdit: Dataset, Real-Time Streaming Model, and Benchmark for Egocentric Video Editing |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://openaccess.thecvf.com/content/CVPR2026/html/Li_EgoEdit_Dataset_Real-Time_Streaming_Model_and_Benchmark_for_Egocentric_Video_CVPR_2026_paper.html) · [Project](https://snap-research.github.io/EgoEdit) |
| Topic | #topic/vision_multimodal_applications #topic/benchmarks_datasets_evaluation #topic/vision_multimodal_applications/image_and_video_generation |
| Method | EgoEdit（含流式变体 EgoEdit-RT） |
| Dataset | EgoEditBench, EditVerseBench |

> [!tip] 效果简介
> - EgoEditBench 上，VLM 7.76 (EgoEdit) vs 7.52 (AnyV2V) (+0.24)；VLM 7.71 (EgoEdit-RT) vs 4.32 (StreamDiffusion) (+3.39)。
> - EditVerseBench 上，VLM 7.50 (EgoEdit) vs 7.45 (EditVerse) (+0.05)。

## 概要

### 问题与瓶颈

现有视频编辑方法在通用场景下已取得显著进展，但面对**第一人称（egocentric）视频**时暴露出两个关键瓶颈：一是训练数据和评估基准缺乏对 egocentric 视角的专门支持，导致模型无法有效处理快速自运动、手-物遮挡与交互等典型 AR 场景；二是主流离线扩散模型的推理延迟过高，无法满足实时交互需求。这构成了从“离线视频编辑”到“沉浸式 AR 交互编辑”之间的核心域差距。

### 核心方案

EgoEdit 通过**数据-模型-推理**三层面的协同设计解决上述问题：

- **数据层面**：构建 EgoEditData，一个从 Ego4D 和 EgoExo4D 中手动策展的 100K egocentric 视频编辑对数据集，聚焦手-物交互场景下的物体替换与移除。原始视频经过严格筛选后仅保留 0.4%，最终产出 10.9K 原始视频与 38.8K 合成视频（共 93.6K 编辑对，约 70 小时）。

- **模型层面**：在预训练视频生成 DiT 上引入**通道级源视频条件注入**（channel-wise concatenation），替代序列拼接以避免自注意力开销激增，使计算成本接近基座模型。随后通过**双向 DMD 蒸馏**将 40 步教师模型压缩为 4 步学生模型，并结合**自强制（Self-Forcing）蒸馏**使模型学会在逐块自回归生成中自动纠正累积误差。

- **推理层面**：EgoEdit-RT 以流式方式运行——摄像头持续采集视频序列，模型逐块编辑并即时呈现，实现“边生成边观看”的交互体验。

### 核心结论

- **实时性能**：EgoEdit-RT 在单张 H100 GPU 上达到 **38.1 fps** 吞吐量，首帧延迟仅 **855 ms**，首次使 egocentric 视频编辑进入实时 AR 交互域。

- **编辑质量**：在 EgoEditBench 上，EgoEdit 的 VLM 分数达到 7.76，超过 **AnyV2V**（7.52）；其实时变体 EgoEdit-RT 达到 7.71，远超同为流式方法的 **StreamDiffusion**（4.32）。在通用基准 EditVerseBench 上，EgoEdit 与最强基线 **EditVerse** 持平（7.50 vs 7.45）。

- **数据驱动验证**：消融实验表明，随着 EgoEditData 子集从 0% 增至 100%，模型 VLM 分数从 4.87 单调提升至 7.85，确证了域专门数据的关键作用。蒸馏消融进一步显示，自强制蒸馏在将总首块延迟压缩至 855ms 的同时，VLM 分数仅比非蒸馏版下降 0.05。

### 方法定位

EgoEdit 处于**实时视频编辑 × egocentric 感知**的交叉点。与 **AnyV2V**、**Lucy Edit**（通道条件注入，Decart Team, arXiv 2025）、**UNIC**（上下文式编辑，Ye et al., arXiv 2025）等通用编辑器不同，EgoEdit 通过域专门数据集和流式蒸馏策略，首次将实时编辑能力引入 egocentric 场景。其技术路线可视为“域数据策展 + 低开销条件注入 + 双向蒸馏 + 自回归自强制”的完整管线，为 AR 交互中的视频编辑提供了端到端解决方案。

第一人称（egocentric）视频编辑是增强现实（AR）交互的核心技术需求。用户佩戴头戴设备时，期望能够通过自然语言指令实时修改视野中的物体——例如替换桌面上的水杯、移除遮挡视线的物品。然而，现有视频编辑方法在该场景下面临双重瓶颈：**域差距**与**推理延迟**。

**域差距**源于训练数据与评测基准的系统性缺失。通用视频编辑模型（如 **AnyV2V**（Ku et al., arXiv 2024）、**EditVerse**、**InsV2V**）的训练数据以第三人称视角为主，缺乏第一人称特有的快速自运动（ego-motion）、手-物遮挡和动态交互模式。当这些模型直接应用于 egocentric 视频时，往往无法正确处理手部遮挡区域的编辑，或在相机剧烈晃动时产生时序不一致的结果。论文分析指出，从 Ego4D 和 EgoExo4D 原始视频中仅保留了约 0.4% 的片段用于构建编辑对，这从侧面反映了高质量 egocentric 编辑数据的稀缺性。

**推理延迟**是实时 AR 场景的另一关键制约。传统视频编辑模型采用离线双向扩散范式，需要完整编码源视频、执行数十步去噪后一次性输出所有帧，首帧延迟通常在数秒至数十秒量级，无法满足“所见即所得”的交互需求。现有低延迟方案如 **StreamDiffusion** 虽降低了延迟，但在 egocentric 场景下的编辑质量大幅下降（VLM 分数仅 4.32，见 Table 1），说明单纯追求速度而忽略域适配无法弥合性能缺口。

EgoEdit 的动机由此明确：**构建域匹配的高质量 egocentric 编辑数据集**以消除域差距，并**通过通道级条件注入与自强制蒸馏实现单 GPU 上的实时流式推理**，从而首次使交互式 AR 视频编辑成为可能。系统整体由三部分构成（Figure 1）：手动策展的 EgoEditData 数据集（约 100k 编辑对，聚焦手-物交互场景下的物体替换与移除）、EgoEdit 编辑模型及其实时变体 EgoEdit-RT（单 H100 GPU 上首帧延迟 855ms、吞吐 38.1fps），以及用于标准化评测的 EgoEditBench 基准。

## 核心方法与创新机理

EgoEdit 的核心创新在于通过四个关键设计槽位（changed slots）的协同改造，首次实现了面向第一人称（egocentric）视频的实时流式编辑。其根本瓶颈在于：现有视频编辑器在训练数据和评估方面缺乏对 egocentric 视角的专门支持，导致在 AR 交互场景中无法处理快速自运动、手-物遮挡和交互，且离线推理延迟高，无法满足实时交互需求。EgoEdit 通过以下四个维度的创新系统性解决了这一问题。

### 1. 源视频条件注入：从序列拼接转向通道拼接

现有视频编辑基线（如 **Lucy Edit**，Decart Team, arXiv 2025）通常采用序列维度拼接（sequence-wise concatenation）将源视频与目标视频在 token 序列维度上拼接后送入自注意力层，这会导致自注意力的计算复杂度随序列长度平方增长，显著增加推理开销。EgoEdit 改用**通道维度拼接**（channel-wise concatenation）：在 patchify 之前将源视频 $\mathbf{X}^{src}$ 和带噪目标视频 $\mathbf{X}_t^{tgt}$ 沿通道维度拼接，使计算成本保持在接近基座视频生成模型的水平。这一设计是支撑后续实时蒸馏的关键前提——若条件注入本身引入过高计算负担，则蒸馏后的实时推理将无从谈起。

### 2. 推理模式：从离线双向扩散转向逐块自回归流式生成

传统视频编辑模型采用离线双向扩散生成，需等待完整去噪过程结束后一次性输出所有帧，无法支持“边生成边观看”的流式交互。EgoEdit 将推理模式重构为**逐块自回归流式生成**（chunk-by-chunk autoregressive streaming）：摄像头持续采集视频序列，模型以视频块（chunk）为单位逐块编辑并即时呈现，每个蓝色箭头代表对单个视频块的一次模型前向传播（见 Figure 5）。这一模式使得编辑结果可以以流式方式送达用户，满足 AR 场景下的实时交互需求。

### 3. 训练数据：引入手动策展的 egocentric 编辑数据集 EgoEditData

现有视频编辑模型（如 **InsV2V**、**EditVerse**、**UNIC**（Zixuan Ye et al., arXiv 2025）等）依赖通用视频编辑数据集进行训练，缺乏对 egocentric 场景的覆盖。EgoEdit 额外引入了**手动策展的 EgoEditData 数据集**，该数据集从 Ego4D 和 EgoExo4D 中筛选，经过视频筛选、手部分割、交互对象识别、对象掩码提取、基于 Wan-VACE 的对象编辑与人工过滤等多阶段策展管线，最终仅保留原始视频的 0.4%，构建了包含 10.9k 原始视频和 38.8k 合成视频（总时长 70 小时）、共计 93.6k 编辑对的高质量数据集，聚焦于手-物交互和自运动场景。消融实验（Table 3）表明，随着 EgoEditData 子集从 0% 增至 100%，模型在 EgoEditBench 上的 VLM 分数从 4.87 单调提升至 7.85，确证了域专门数据的关键作用。

### 4. 蒸馏方法：双向 DMD 蒸馏与自强制训练

EgoEdit 的蒸馏策略分为两步。首先，采用**双向 DMD 蒸馏**将 40 步教师模型（含无分类器引导）压缩为 4 步学生模型（含蒸馏引导），在保持编辑质量的同时大幅降低推理步数。随后，通过**自强制**（Self-Forcing）训练使蒸馏模型在自回归逐块生成中自动纠正累积误差：模型在视频流上以自回归方式运行，前一帧的生成输出作为后一帧的条件输入，模型在此过程中学会修正自身错误。最终得到的 EgoEdit-RT 在单张 H100 GPU 上达到 38.1 fps 的吞吐量和 855ms 的首帧延迟（Table 2），同时 VLM 分数仅比非蒸馏版下降 0.05（7.71 vs 7.76），实现了编辑质量与实时性的有效平衡。

### 创新点间的因果关联

上述四个创新槽位之间存在紧密的因果依赖关系：通道拼接（创新 1）保证了基座模型的计算效率，为蒸馏压缩（创新 4）提供了可行的起点；EgoEditData 的域专门数据（创新 3）弥补了通用编辑器在 egocentric 场景下的性能缺陷；蒸馏和自强制训练（创新 4）则使得逐块自回归流式推理（创新 2）在保持可接受编辑质量的前提下达到实时性能。四者共同构成了从数据、架构、推理模式到效率优化的完整创新链条，使 EgoEdit 成为首个真正支持交互式 AR 场景的 egocentric 视频实时编辑系统。

EgoEdit 构建了一个面向第一人称视频编辑的完整生态系统，由三个核心组件构成：**EgoEditData**（手动策展的 egocentric 编辑数据集）、**EgoEdit**（基于通道条件注入的流式编辑模型）及其实时变体 **EgoEdit-RT**、以及 **EgoEditBench**（egocentric 编辑基准）。整体工作流为：通过 EgoEditData 策展管线获取高质量域匹配训练对，在其上微调预训练视频生成器得到基座编辑模型，再经双向 DMD 蒸馏与自强制训练压缩为实时自回归生成器，最终在 EgoEditBench 上完成系统评估。

### 数据策展管线

EgoEditData 的构建是整个系统的域适配瓶颈。策展流程从 Ego4D 和 EgoExo4D 原始视频出发，经过视频筛选、手部分割、交互对象识别、对象掩码提取、基于 Wan-VACE 的对象编辑与人工过滤，最终仅保留原始视频的 0.4%，得到 10.9k 原始视频和 38.8k 合成视频（总时长 70 小时），平均每个原始视频生成 3.6 个合成变体，合计 93.6k 编辑对。该数据集聚焦于手-物交互场景下的对象替换与移除，覆盖了快速自运动、手部遮挡等 egocentric 特有挑战。

### 基座编辑模型架构

EgoEdit 以视频生成 DiT 模型为骨干，将其适配为视频编辑器。核心设计在于**源视频条件注入方式**：EgoEdit 采用通道维度拼接（channel-wise concatenation），将源视频 $\mathbf{X}^{src}$ 与带噪目标视频 $\mathbf{X}_t^{tgt}$ 在通道维度拼接后再进行 patch 化，避免了序列维度拼接带来的自注意力计算开销，使计算成本接近基座生成模型。模型以 Rectified Flow 为训练框架，沿线性路径 $\mathbf{X}_t = (1-t)\mathbf{X}_0 + t\mathbf{X}_1$ 预测恒定速度 $\mathbf{X}_1 - \mathbf{X}_0$，损失函数为：

$$\mathcal{L}_{\mathrm{RF}} = \mathbb{E}_{t \sim p_t, \mathbf{X}_1 \sim p_d, \mathbf{X}_0 \sim p_n} \big\| \mathcal{G}(\mathbf{X}_t, t) - (\mathbf{X}_1 - \mathbf{X}_0) \big\|_2^2$$

训练时，模型在 EgoEditData 及额外的 1.31M 视频编辑对和 3.5M 图像编辑对上微调，以同时获得 egocentric 场景的域专门能力和通用编辑能力。

### 蒸馏与实时推理管线

为实现交互式 AR 场景所需的低延迟，EgoEdit 引入两阶段蒸馏压缩：

1. **双向 DMD 蒸馏**：将 40 步推理的教师模型（含无分类器引导）压缩为 4 步学生模型，蒸馏训练进行 4.5k 步，模型学习率 1e-6，critic 学习率 4e-7（AdamW 优化器）。
2. **自强制训练**：在蒸馏模型基础上，以 chunk-by-chunk 自回归方式在视频流上运行，使模型在生成过程中学会纠正自身累积误差，从而实现流式推理。

最终得到的 EgoEdit-RT 在单张 H100 GPU 上达到 **38.1fps** 吞吐量、首帧延迟 **855ms**，支持 watch-as-you-generate 的实时 AR 交互体验。推理流程为：摄像头持续采集视频序列，模型逐块编辑并即时呈现，每个视频块对应一次模型前向传播。

### 模块关系总结

各模块间的依赖关系清晰：EgoEditData 策展管线为基座模型训练提供域匹配监督信号；通道级条件注入架构保证了编辑质量与计算效率的平衡；双向 DMD 蒸馏在保持编辑质量的前提下大幅压缩推理步数；自强制训练则赋予模型流式自回归生成能力，最终使整个系统从数据、模型到推理形成闭环，弥合了 egocentric 视频编辑的域差距与实时性双重瓶颈。

### 补充图表

![[assets/figures/papers/paper_list_l2675_https_openaccess_thecvf_com_content_CVPR2026_html_Li_EgoEdit_Dataset_Rea/figures/004_Figure_4.jpg]]
*Figure 4: Architecture of EgoEdit. EgoEdit extends a video generation DiT model for video editing by performing channel-wise concatenation of the source and noisy target video inputs, avoiding the computational overheads of sequence-wise concatenation*

### 基础生成框架：Rectified Flow 速度预测

EgoEdit 的视频生成骨干建立在 Rectified Flow（Flow Matching）框架之上。该框架的核心思想是学习一个从噪声到数据的恒定速度场，而非直接学习数据分布。其训练目标为：

$$
\mathcal{L}_{\mathrm{RF}} = \mathbb{E}_{t \sim p_t, \mathbf{X}_1 \sim p_d, \mathbf{X}_0 \sim p_n} \big\| \mathcal{G}(\mathbf{X}_t, t) - (\mathbf{X}_1 - \mathbf{X}_0) \big\|_2^2
$$

其中各变量含义如下：
- $\mathbf{X}_0 \sim p_n$：从标准高斯噪声分布中采样的初始噪声。
- $\mathbf{X}_1 \sim p_d$：从真实数据分布中采样的目标视频潜变量。
- $t \in [0, 1]$：时间步，从分布 $p_t$ 中采样。
- $\mathbf{X}_t = (1 - t) \mathbf{X}_0 + t \mathbf{X}_1$：噪声与数据之间的线性插值路径。
- $v_t = \frac{d \mathbf{X}_t}{d t} = \mathbf{X}_1 - \mathbf{X}_0$：沿线性路径的恒定真实速度。
- $\mathcal{G}$：待训练的神经网络（DiT 主干），输入为当前时刻的带噪数据 $\mathbf{X}_t$ 和时间步 $t$，输出为预测的速度场 $\hat{v}$。

训练目标是最小化预测速度 $\mathcal{G}(\mathbf{X}_t, t)$ 与真实速度 $(\mathbf{X}_1 - \mathbf{X}_0)$ 之间的 L2 距离。推理时，从 $\mathbf{X}_0 \sim p_n$ 出发，利用预测速度场通过 ODE 求解器（如 Euler 方法）逐步积分至 $t=1$，即可生成目标视频 $\mathbf{X}_1$。

---

### 视频编辑适配：通道级源条件注入

将上述生成模型适配为视频编辑器的关键在于引入源视频条件。给定源视频 $\mathbf{X}^{src}$ 和目标视频 $\mathbf{X}^{tgt}$，模型需根据编辑指令 $c$ 将源视频转换为编辑后的目标视频。标准做法是将条件预测改写为：

$$
\hat{v} = \mathcal{G}(\mathbf{X}_t^{tgt} \mid \mathbf{X}^{src}; c)
$$

其中 $\mathbf{X}_t^{tgt}$ 为目标视频的带噪版本。

**核心设计选择：通道维度拼接（Channel-wise Concatenation）**。现有方法多采用序列维度拼接（sequence-wise concatenation），即将源视频和目标视频的 token 序列在序列维度上拼接后送入 Transformer。这会导致自注意力计算量随序列长度平方增长，显著增加计算开销。

EgoEdit 采用通道维度拼接：在 patchification 之前，将 $\mathbf{X}^{src}$ 和 $\mathbf{X}_t^{tgt}$ 沿通道维度拼接。这意味着每个 patch 同时包含源视频和目标视频的信息，而序列长度与基座模型保持一致。因此，自注意力计算成本几乎不增加，使编辑模型的推理开销接近纯生成模型。这一设计是实现实时推理的第一个关键架构决策。

---

### 实时推理：双向 DMD 蒸馏与自强制训练

离线编辑模型通常需要 40 步去噪迭代，无法满足实时交互需求。EgoEdit 通过两阶段蒸馏获得实时生成器 EgoEdit-RT。

**第一阶段：双向 DMD（Distribution Matching Distillation）蒸馏**。将 40 步教师模型（含无分类器引导）压缩为 4 步学生模型。DMD 通过匹配教师与学生生成分布之间的 KL 散度进行蒸馏，保留编辑质量。蒸馏在 EgoEditData 及额外 1.31M 视频、3.5M 图像编辑对上执行 4.5k 步，使用 AdamW 优化器，模型学习率 1e-6，判别器学习率 4e-7。

**第二阶段：自强制（Self-Forcing）训练**。4 步蒸馏模型仍为双向模型，需完整输入所有帧后一次性输出。为实现流式推理，需将其转换为逐块自回归生成器。Self-Forcing 的核心思想是：在训练时模拟自回归推理过程——模型基于前一块的生成结果（而非真实视频）预测当前块，从而学会在推理时自动纠正自身累积的误差。这一训练策略使模型能够在推理时以 chunk-by-chunk 方式持续生成，摄像头采集新帧的同时，模型仅需处理当前块，实现“边生成边观看”的流式体验。

**推理流水线**（见图 5）：
1. 摄像头持续采集源视频序列。
2. 模型以固定大小的 chunk 为单位，自回归地生成编辑后的视频块。
3. 每个蓝色箭头代表一次模型前向传播（对于 3 步模型，每块需 3 次前向）。
4. 编辑后的视频块即时呈现给用户。

蒸馏后的 EgoEdit-RT 在单张 H100 GPU 上达到 **38.1 fps** 吞吐量，首帧延迟 **855 ms**（含源视频编码、模型推理和自编码器解码），满足 AR 交互的实时性要求。同时，VLM 分数仅从教师模型的 7.76 略微下降至 7.71（见表 2），验证了蒸馏过程在效率与质量之间的有效平衡。

### 补充图表

![[assets/figures/papers/paper_list_l2675_https_openaccess_thecvf_com_content_CVPR2026_html_Li_EgoEdit_Dataset_Rea/figures/005_Figure_5.jpg]]
*Figure 5: Inference of EgoEdit. EgoEdit performs inference in a streaming fashion. A camera continuously acquires video sequences which are edited by the model in a chunk-by-chunk manner so that the edited video can be served to the user in a watch-asyou-generate fashion. Each blue arrow represents a model forward pass on a single video chunk for the case of a 3 steps model*

## 实验与关键发现

### 实验设置

EgoEdit 的训练分为两个阶段：首先，在 EgoEditData 及额外 1.31M 视频编辑对和 3.5M 图像编辑对上微调预训练视频生成模型，获得基座视频编辑模型；随后，通过双向 DMD 蒸馏将 40 步教师模型压缩为 4 步学生模型，蒸馏过程使用 AdamW 优化器，模型学习率 1e-6，判别器学习率 4e-7，共训练 4.5k 步。最终，对蒸馏模型施加自强制训练，使其具备逐块自回归流式生成能力。

评估在 EgoEditBench 和 EditVerseBench 两个基准上进行，指标包括 VLM 评估分数（VLM）、Pick Score（PS）、文本对齐（TA）和时序一致性（TC）。EditVerseBench 中基于参考的编辑任务（传播、修复、参考插入、掩码编辑）被排除。所有蒸馏模型的延迟与吞吐量在单张 H100 GPU、分辨率 512×384px 下测量，延迟统计涵盖源视频录制、EgoEdit 推理、以及自动编码器编解码的完整管线。

### 主要结果

**Table 1** 报告了 EgoEdit 及其流式变体 EgoEdit-RT 与多个基线的定量对比。在 egocentric 编辑基准 EgoEditBench 上，EgoEdit 以 VLM 分数 7.76 超越最强通用基线 **AnyV2V**（7.52），提升 +0.24；其实时变体 EgoEdit-RT 达到 7.71，远超现有流式编辑器 **StreamDiffusion**（4.32），优势达 +3.39。在通用编辑基准 EditVerseBench 上，EgoEdit 与当前最优的 **EditVerse**（7.45）表现持平（7.50），同时显著优于 **Lucy Edit**（7.00）和 **UNIC**（6.65）。这表明 EgoEdit 在 egocentric 场景取得显著增益的同时，未牺牲通用编辑能力。

值得注意的是，EgoEdit-RT 作为流式模型，其 VLM 分数（7.71）仅比非蒸馏全精度 EgoEdit（7.76）低 0.05，说明蒸馏过程在实现实时推理的同时几乎无损编辑质量。

### 消融实验

#### 蒸馏策略消融（Table 2）

![[assets/figures/papers/paper_list_l2675_https_openaccess_thecvf_com_content_CVPR2026_html_Li_EgoEdit_Dataset_Rea/figures/008_Table_2.jpg]]
*Table 2: EgoEditBench VLM score, latency and throughput analysis of different distilled EgoEdit models on 1↑H100 under resolution of 512↑384px. We consider latency involved in recording the source video, running EgoEdit, and running the autoencoder (AE) for source video encoding and generated video decoding*

Table 2 系统比较了三种模型变体的性能-效率权衡：

- **无蒸馏（No Distill.）**：VLM 7.76，但总首块延迟高达 14.4s，完全无法满足交互需求。
- **DMD 蒸馏（DMD Distill.）**：将推理步数从 40 步压缩至 4 步，VLM 略微提升至 7.79（可能因蒸馏过程中的正则化效应），总首块延迟降至 2.7s，但仍未达到实时标准。
- **自强制蒸馏（Self Forcing）**：在 DMD 基础上引入自回归训练，VLM 保持 7.71，总首块延迟进一步压缩至 **855ms**，吞吐量达到 **38.1 fps**。其中 EgoEdit 推理仅占 307ms，其余延迟来自源视频编码和生成视频解码。

这是唯一的亚秒级延迟方案，使模型真正具备交互式 AR 使用条件。自强制训练的关键在于让模型在 chunk-by-chunk 生成过程中学会纠正自身累积误差，从而在不牺牲质量的前提下实现流式输出。

#### 数据规模消融（Table 3）

![[assets/figures/papers/paper_list_l2675_https_openaccess_thecvf_com_content_CVPR2026_html_Li_EgoEdit_Dataset_Rea/figures/009_Table_3.jpg]]
*Table 3: Performance of EgoEdit when trained using progressively smaller subsets of EgoEditData. A trend is visible: the model performs better with more egocentric editing data included during training. Note that these results differ from Table 1 because all models are evaluated at the 10k-iteration checkpoint. Additional details are provided in Appx. ??*

Table 3 展示了 EgoEditData 子集规模对模型性能的因果效应。在仅使用 0% EgoEditData（即完全依赖通用编辑数据）时，VLM 分数仅为 **4.87**；随着 EgoEditData 比例从 25% 逐步增至 100%，VLM 分数单调上升至 **7.85**。这一单调趋势强有力地证明了域专门数据对 egocentric 编辑性能的因果贡献——通用数据无法弥补 egocentric 场景中手-物交互、快速自运动等独特挑战带来的域差距。

需要注意的是，Table 3 的结果基于 10k 迭代检查点评估，与 Table 1 中最终收敛模型的结果存在差异，但这不影响数据规模效应的定性结论。

![[assets/figures/papers/paper_list_l2675_https_openaccess_thecvf_com_content_CVPR2026_html_Li_EgoEdit_Dataset_Rea/figures/007_Table_1.jpg]]
*Table 1: Quantitative comparison of the baseline models and our method on EgoEditBench and EditVerseBench benchmarks: “VLM” is VLM evaluation score, “PS” is Pick Score, “TA” is Text Alignment, “TC” is Temporal Consistency. Reference-based editing tasks from EditVerseBench—propagation, inpainting, reference insertion, and edit with mask—were excluded. “†” indicates closed-source models evaluated using their publicly released samples; “‡” indicates models utilizing the first frame generated by EgoEdit. EgoEdit-RT stands for the real-time streaming version of EgoEdit*

### 定性分析

**Figure 6** 展示了 EgoEdit 及 EgoEdit-RT 在 EgoEditBench 上的定性对比结果。在涉及手部遮挡、物体交互和大幅自运动的挑战性场景中，EgoEdit 能够准确遵循编辑指令，保留源视频的结构和运动信息，而基线方法常出现物体变形、编辑区域不一致或时序闪烁等问题。EgoEdit-RT 的流式输出在保持编辑质量的同时，实现了“边生成边观看”的实时体验。

### 失败模式与局限性

尽管 EgoEdit 在 egocentric 编辑任务上取得显著进展，仍存在以下局限：

1. **硬件依赖**：实时性能依赖于单张 H100 GPU，在移动端或低功耗 AR 设备上的部署尚不可行，限制了实际应用范围。
2. **数据覆盖偏差**：EgoEditData 主要来源于 Ego4D 和 EgoExo4D，仅保留原始视频的 0.4%，场景和交互类型可能存在选择偏差，极端低光照、剧烈抖动等场景的泛化能力未经充分验证。
3. **蒸馏质量权衡**：自强制蒸馏在压缩延迟的同时，VLM 分数从 7.76 微降至 7.71，虽然幅度极小，但论文未提供编辑多样性或复杂指令忠实度的全面指标，无法排除蒸馏对某些细粒度编辑能力的潜在影响。
4. **长期稳定性未验证**：论文未探讨模型在多视角、长期连续视频编辑中的内容漂移和时序稳定性问题，这对实际 AR 应用至关重要。

### 补充图表

![[assets/figures/papers/paper_list_l2675_https_openaccess_thecvf_com_content_CVPR2026_html_Li_EgoEdit_Dataset_Rea/figures/003_Figure_3.jpg]]
*Figure 3: Comparison of EgoEdit and EgoEdit-RT against baselines according to VLM score on EgoEditBench and EditVerseBench [23]. Overall, EgoEdit and its real-time variant EgoEdit-RT achieve superior results on egocentric editing tasks and perform competitively with the strongest baselines on general editing tasks. EditVerse is excluded from EgoEditBench as source code is unavailable. Streaming models are indicated in dashed lines*

![[assets/figures/papers/paper_list_l2675_https_openaccess_thecvf_com_content_CVPR2026_html_Li_EgoEdit_Dataset_Rea/figures/001_Figure_1.jpg]]
*Figure 1: We propose a framework for real-time egocentric video editing. Our system is composed of: EgoEditData, a manually curated dataset of 100k video editing pairs focusing on the egocentric case and featuring object substitution and removal under challenging hand occlusions, interactions, and large egomotion; EgoEdit, the first real-time autoregressive model for egocentric video editing running in real time on a single H100 with 855ms first-frame latency and enabling live augmented reality (AR) interactions; EgoEditBench, a comprehensive benchmark for evaluation of egocentric video editing systems*

## 定位与知识库关联

### 1. 与现有视频编辑方法的谱系关系

EgoEdit 在视频编辑技术谱系中处于**实时流式生成与域专门化编辑**的交汇点，其设计同时回应了通用视频编辑模型在效率与域适应性上的双重不足。

**与通用视频编辑基线的对比。** 现有视频编辑方法大致可分为两类：一类是无需训练的通用框架，如 **AnyV2V** (Ku et al., arXiv 2024)，通过冻结的扩散模型与注意力注入实现零样本编辑；另一类是基于合成编辑对训练的统一模型，如 **InsV2V**、**EditVerse** 和 **UNIC** (Ye et al., arXiv 2025)。这些方法在通用场景下表现强劲，但其训练数据缺乏第一人称（egocentric）场景覆盖，导致在 AR 交互中面临快速自运动、手-物遮挡和交互时的性能退化。EgoEdit 的核心差异化在于：通过引入手动策展的 EgoEditData（10.9k 原始视频 + 38.8k 合成视频，共 93.6k 编辑对），将域知识显式注入训练过程，从而弥合这一域差距。实验证据显示，当 EgoEditData 子集从 0% 增至 100% 时，模型在 EgoEditBench 上的 VLM 分数从 4.87 单调提升至 7.85（Table 3），验证了域专门数据的因果作用。

**与实时流式编辑基线的对比。** 在实时性方面，**StreamDiffusion** 是低延迟流式扩散模型的代表，但其在 egocentric 编辑任务上的 VLM 分数仅为 4.32，远低于 EgoEdit-RT 的 7.71（Table 1）。EgoEdit-RT 的性能优势源于其“双向 DMD 蒸馏 + 自强制（Self-Forcing）训练”的组合策略：先将 40 步教师模型压缩为 4 步学生模型，再通过自回归的 chunk-by-chunk 生成与误差自纠正机制，在单张 H100 GPU 上达到 38.1fps 的吞吐量和 855ms 的首帧延迟（Table 2），首次使 egocentric 视频编辑满足交互式 AR 的实时性要求。

**与通道条件注入方法的对比。** **Lucy Edit** (Decart Team, arXiv 2025) 同样采用通道级源视频条件注入，EgoEdit 沿用了这一设计范式（channel-wise concatenation），但将其与 egocentric 域数据训练和流式蒸馏深度耦合，形成了从数据到推理的完整实时编辑管线。与序列拼接（sequence-wise concatenation）相比，通道拼接避免了自注意力序列长度的翻倍，使计算成本保持在接近基座模型的水平，这是实现低延迟推理的关键架构选择。

### 2. 适用边界与局限

EgoEdit 的设计在以下维度存在明确的适用边界：

**硬件依赖。** 模型在单张 H100 GPU 上达到实时性能，但这一硬件门槛限制了其在移动端或低功耗 AR 设备（如智能眼镜）上的直接部署。论文未提供针对边缘设备的模型量化或剪枝方案，因此当前框架更适用于云端或高性能边缘服务器场景。

**数据覆盖偏差。** EgoEditData 主要来源于 Ego4D 和 EgoExo4D，经过多轮策展后仅保留原始视频的 0.4%。尽管这确保了数据质量，但也意味着场景和交互类型可能存在选择偏差——例如，极端低光照、剧烈抖动或非手部主导的交互场景可能未被充分覆盖。论文未提供数据集在环境条件、运动模式等维度上的分布统计，需要手动验证数据多样性。

**蒸馏带来的质量折损。** 自强制蒸馏后的 EgoEdit-RT 在 VLM 分数上比非蒸馏版 EgoEdit 低 0.05（7.71 vs. 7.76，Table 2），表明实时性优化对编辑质量有轻微影响。论文未提供编辑多样性或复杂指令忠实度的全面指标，因此蒸馏对生成多样性的潜在抑制尚需进一步评估。

**长时序稳定性。** 论文未探讨模型在多视角、长期视频编辑中的稳定性和内容漂移问题。在 AR 场景中，持续的 chunk-by-chunk 生成可能导致误差累积或场景一致性退化，当前的自强制机制虽能部分缓解，但其上限未经验证。

### 3. 开放问题与未来方向

EgoEdit 为 egocentric 视频编辑设立了基线，但以下问题仍待探索：

**域数据的泛化效应。** EgoEditData 对通用编辑任务（如 EditVerseBench）的性能提升程度仅在补充材料中提及，正文未提供详细定量分析。Table 3 的结果基于 10k 迭代检查点，最终收敛后性能差距是否缩小尚不明确，需查阅附录验证。

**交互式指令理解。** 在 AR 应用中，用户自然语言指令常存在歧义，模型是否支持多轮交互式编辑、能否在实时约束下消解指令歧义，论文未予讨论。这涉及将编辑模型与对话式 AI 系统结合的工程挑战。

**多模态扩展。** 当前框架聚焦于文本引导的对象替换与移除，但其通道条件注入架构理论上可扩展至其他第一人称任务（如姿态引导编辑、深度条件编辑）。是否能与其他模态（如眼动追踪、手势识别）结合以实现更丰富的 AR 体验，是值得探索的方向。

**评估体系的完善。** EgoEditBench 依赖 VLM 评分作为主要指标，但 VLM 评估本身对 egocentric 场景的敏感性和偏差尚未得到系统性校准。建立更全面的评估维度（如交互自然度、编辑保真度、用户感知延迟）将有助于推动该领域的标准化。

## 原文 PDF

![[paperPDFs/CVPR_2026/EgoEdit_Dataset_Real_Time_Streaming_Model_and_Benchmark_for_Egocentric_Video_Editing.pdf]]
