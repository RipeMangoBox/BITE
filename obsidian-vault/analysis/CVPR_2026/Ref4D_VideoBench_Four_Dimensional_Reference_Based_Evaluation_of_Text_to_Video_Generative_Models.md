---
title: "Ref4D-VideoBench: Four-Dimensional Reference-Based Evaluation of Text-to-Video Generative Models"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/Ref4D_VideoBench_Four_Dimensional_Reference_Based_Evaluation_of_Text_to_Video_Generative_Models.pdf
project_link: null
code_link: "https://github.com/TAILab-W/Ref4D-VideoBench"
aliases:
- RV
- Ref4D-VideoBench
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/image_and_video_generation
- topic/generative_models_diffusion
- topic/generative_models_diffusion/diffusion_image_video
core_operator: 引入高质量参考视频作为结构化时空证据（实体-属性、事件图、运动轨迹、世界知识规则），将评估从文本对齐转变为显式一致性检查。
primary_logic: 基于参考视频构建语义、运动、事件和世界知识四维评估体系，通过显式证据提取和可解释的原子指标，实现了与人类判断高度对齐的、可诊断的生成视频评估。
claims:
- 在所有四个维度上，Ref4D-VideoBench 的样本级相关性（SRCC/PLCC/KRCC）显著优于代表性无参考基线，例如语义维度 SRCC 0.822 vs 最佳无参考基线 0.317。
- 即使单独使用原子指标（如 CatCov、ECR），也获得了与人类评分中等到强的相关性，验证了参考驱动证据的有效性。
- 移除基于参考视频构建的规则/问题库后，世界知识一致性评估的 SRCC 从 0.847 剧降至 0.406，证明参考证据是该维度的核心驱动力。
- Ref4D-VideoBench human correlation 上 SRCC (Semantic) = 0.822
---

# Ref4D-VideoBench: Four-Dimensional Reference-Based Evaluation of Text-to-Video Generative Models

> [!tip] 核心洞察
> 基于参考视频构建语义、运动、事件和世界知识四维评估体系，通过显式证据提取和可解释的原子指标，实现了与人类判断高度对齐的、可诊断的生成视频评估。

| 字段 | 内容 |
|------|------|
| 中文题名 | Ref4D-VideoBench：文本到视频生成模型的四维参考评估基准 |
| 英文题名 | Ref4D-VideoBench: Four-Dimensional Reference-Based Evaluation of Text-to-Video Generative Models |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://openaccess.thecvf.com/content/CVPR2026/html/Wei_Ref4D-VideoBench_Four-Dimensional_Reference-Based_Evaluation_of_Text-to-Video_Generative_Models_CVPR_2026_paper.html) · [Code](https://github.com/TAILab-W/Ref4D-VideoBench) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/image_and_video_generation #topic/generative_models_diffusion #topic/generative_models_diffusion/diffusion_image_video |
| Method | Ref4D-VideoBench |
| Dataset | Ref4D-VideoBench human correlation |

> [!tip] 效果简介
> - Ref4D-VideoBench human correlation 上，SRCC (Semantic) 0.822 vs Q-Align 0.317 (最佳无参考基线) (+0.505)；SRCC (Motion) 0.659 vs Q-Align 0.358 (最佳无参考基线) (+0.301)；SRCC (Event) 0.755 vs 最强无参考基线 0.220 (from Tab.1) (+0.535)。

## 概要

文本到视频（T2V）生成模型近年来迅速发展，但如何可靠地评估生成视频的质量仍是一个核心瓶颈。现有主流方法采用无参考评估范式，仅依赖文本提示对生成视频进行整体质量或维度评分。然而，这类方法缺乏样本级的显式时空证据，难以对目标行为偏差、时间不一致、常识违规等细粒度失败进行可解释的归因，导致评估可信度与诊断能力不足。

针对这一瓶颈，本文提出 **Ref4D-VideoBench**，一个基于高质量参考视频的四维评估基准。其核心思想是将评估从“文本-视频对齐”转变为“参考-生成视频的显式一致性检查”：参考视频天然提供丰富、无歧义的结构化时空证据，使评估可以深入到实体属性、运动模式、事件时序和世界知识四个维度，并通过可解释的原子指标进行量化。

在方法谱系中，Ref4D-VideoBench 相对于现有无参考评估框架做出了三个关键改变：**（1）评估输入**从“仅文本提示”扩展为“参考视频 + 文本提示”；**（2）评估粒度**从整体质量评分细化为语义、运动、事件、世界知识四个可解释维度，每个维度由多个原子指标聚合；**（3）评分器机制**从黑盒 MLLM 或 CLIP 式相似度转变为“结构化证据提取 + 显式原子指标 + 学习的线性聚合器”。

实验在八个主流 T2V 模型上验证了该框架的有效性。在样本级人类评分相关性上，Ref4D-VideoBench 在所有四个维度上均显著优于代表性无参考基线：语义维度 SRCC 达到 **0.822**（最佳无参考基线 Q-Align 仅 0.317），运动维度 **0.659**（vs. 0.358），事件维度 **0.755**（vs. 0.220），世界知识维度 **0.847**（vs. 0.391）。消融实验进一步揭示，原子指标（如 CatCov、ECR）单独即可获得与人类判断中等到强的相关性，而基于参考视频构建的世界知识规则库是驱动该维度高性能的核心——移除规则库后，SRCC 从 0.847 骤降至 0.406。

该框架的局限性在于强依赖高质量参考视频的可用性，在无法获得对应参考的开放场景中适用性受限；世界知识评估依赖 MLLM 生成规则和评分，其偏见可能传递到最终分数。未来工作方向包括探索无参考或弱监督扩展、设计更可解释的非线性聚合器，以及将评估框架直接用于生成模型的对齐训练。



### 文本到视频生成评估的现状与瓶颈

文本到视频（T2V）生成模型近年来快速发展，从闭源的 **Sora**（OpenAI, 2024）、**Sora 2**（OpenAI, 2025）、**Kling AI**（Kuaishou, 2024）、**Dream Machine**（Luma AI, 2024）、**JiMeng AI**（字节跳动, 2024）、**Vidu**（Shengshu, 2024）到开源的 **VideoCrafter2** 等，模型能力持续提升。然而，如何可靠地评估这些模型的生成质量，始终是一个滞后于生成能力发展的核心问题。

当前主流的评估范式以**无参考（no-reference）方法**为主，其核心逻辑是将生成视频与文本提示进行对齐判断。代表性方法包括基于 CLIP 计算文本-视频相似度的 **CLIPScore**（Radford et al., ICML 2021）、使用 BLIP 模型的 **BLIPScore**（Li et al., ICML 2022），以及通过离散文本定义级别训练多模态大模型进行视觉评分的 **Q-Align**（Wu et al., ICML 2024）。这些方法虽然在整体质量评估上取得了一定进展，但存在一个根本性局限：**它们仅依赖文本提示作为唯一的评判依据，缺乏样本级的显式时空证据**。

这一局限带来了三个连锁问题。首先，文本提示天然具有歧义性和不完整性——同一句提示可以对应无数种合理的视觉实现，仅凭文本无法判断生成视频是否在实体构成、运动模式、事件时序和物理规律上与“应有”的视觉真实一致。其次，无参考方法通常输出一个整体质量分数或少数几个维度的综合评分，属于黑盒评判，当评分偏低时，开发者无法获知具体是哪个维度出了问题——是实体缺失、运动退化、事件顺序错乱，还是违背了基本的世界知识。第三，由于缺乏可解释的归因路径，这类评估的可信度和诊断能力受到严重制约，难以真正指导模型迭代。

### 核心瓶颈：从文本对齐到证据驱动的一致性检查

上述问题的本质可以归结为一个瓶颈：**现有评估方法将“生成质量”等同于“文本-视频相似度”，而忽略了视频作为时空媒介所蕴含的丰富结构化信息。** 文本提示无法提供关于“羚羊应该以何种步态追逐、追逐事件应持续多长时间、追逐过程中是否存在物理穿模”等细粒度约束，而这些恰恰是人类评判者赖以做出质量判断的关键证据。

因此，问题的关键不在于设计更强大的文本编码器或更大的多模态评分模型，而在于**为评估引入一个能够提供显式时空证据的信息源**，将评估逻辑从模糊的“文本对齐”转变为可验证的“一致性检查”。

### 本文动机：以参考视频为证据源的四维评估

本文的核心洞察是：**一段高质量的参考视频天然携带了丰富、无歧义的时空证据**——它明确展示了场景中应有哪些实体及其属性、实体间应呈现何种相对运动、事件应如何随时间展开，以及整个过程应遵循哪些物理和常识规则。如果以参考视频作为证据源，评估就不再是“生成视频与模糊文本有多像”，而是“生成视频在关键时空维度上与参考证据是否一致”。

基于这一洞察，本文提出 **Ref4D-VideoBench**，一个基于参考视频的四维评估基准。该框架从参考视频中提取四类结构化证据——**实体-属性列表**（语义维度）、**前景/背景运动统计量**（运动维度）、**事件边界与事件图**（事件时间维度）、**物理/因果/安全规则**（世界知识维度）——并针对每个维度设计显式的原子指标，最终通过学习的线性聚合器输出可解释的四维评分。这一设计使得评估结果不仅与人类判断高度对齐，还能逐维度、逐指标地诊断生成模型的失败模式，为模型改进提供明确的优化方向。



## 核心方法与创新机理

### 1. 问题瓶颈：无参考评估的证据缺失

现有文本到视频（T2V）生成模型的评估方法，无论是基于 CLIP 相似度的 **CLIPScore**（Radford et al., ICML 2021）、**BLIPScore**（Li et al., ICML 2022），还是基于多模态大模型的 **Q-Align**（Wu et al., ICML 2024），均采用**无参考评估**范式——仅依赖文本提示对生成视频进行整体质量或粗粒度多维评分。这一范式的根本瓶颈在于：**缺乏样本级的显式时空证据**。当生成视频出现目标行为偏差、时间不一致或常识违规等细粒度失败时，无参考方法无法进行可解释的归因诊断，导致评估可信度不足，且难以指导模型的定向改进。

### 2. 核心因果机制：从“文本对齐”到“显式一致性检查”

Ref4D-VideoBench 的核心创新在于引入**高质量参考视频作为结构化时空证据**，将评估范式从“文本-视频对齐”转变为“参考-生成视频的显式一致性检查”。这一转变的关键在于：参考视频天然提供了丰富、无歧义的时空信息——包括实体-属性列表、事件图、运动轨迹和世界知识规则——使得评估不再是黑盒相似度计算，而是基于可验证证据的**可解释诊断**。

### 3. Changed Slots：与基线方法的三个结构性差异

| 设计维度 | 无参考基线 | Ref4D-VideoBench | 创新本质 |
|----------|-----------|------------------|---------|
| **评估输入** | 仅文本提示 | 参考视频 + 文本提示 | 引入结构化时空证据源，使细粒度归因成为可能 |
| **评估粒度** | 整体质量或多维整体评分 | 四个可解释维度（语义、运动、事件、世界知识），每维度由多个原子指标聚合 | 将评估分解为可独立诊断的子问题，每个维度对应明确的失败模式 |
| **评分器机制** | 黑盒 MLLM 或 CLIP 式相似度 | 结构化证据提取 + 显式原子指标 + 学习的线性聚合器 | 每个原子指标有明确的物理/语义含义，评估过程可追溯、可验证 |

### 4. 四维评估体系的创新设计

Ref4D-VideoBench 构建了四个相互补充的评估维度，每个维度对应一类关键的生成失败模式：

- **基本语义对齐**：通过提取参考视频的实体-属性列表，使用匈牙利算法进行软匹配，计算类别覆盖率（CatCov）和属性完整性得分（AIC），并引入幻觉惩罚。该维度直接诊断生成视频是否忠实再现参考视频中的核心语义元素及其属性绑定。

- **运动一致性**：分离前景与背景，通过点追踪提取相对运动 $ \mathbf{r}(t) = \mathbf{v}^{\mathrm{fg}}(t) - \mathbf{v}^{\mathrm{bg}}(t) $，计算方向、幅度、平滑度差异，以及重复帧率和低速段比例。该维度有效去除了相机运动的干扰，聚焦于对象自身的动态模式是否与参考一致。

- **事件时间一致性**：检测事件边界并构建事件图，通过事件图对齐（EGA）、事件关系一致性（ERel）和事件覆盖与冗余（ECR）三项指标，分别评估事件内容对齐、时间关系正确性和覆盖完整度。ECR 的设计尤为精巧，通过调和参考事件覆盖率与生成视频中幻觉事件的比率，实现了覆盖度与冗余惩罚的平衡。

- **世界知识一致性**：基于参考视频的语义和事件证据自动生成物理、因果和安全规则，构造逐视频的 VQA 问题库，使用 MLLM 评分后加权平均得到最终分数。与固定的全局问卷相比，逐视频问题库更好地反映了场景相关的世界知识，减少了无关判断，提升了诊断特异性。

### 5. 决定性证据：参考驱动的性能增益

消融实验提供了强有力的因果证据，证明参考视频是性能提升的核心驱动力：

- **世界知识维度的规则库消融**（Table 4）：移除基于参考视频构建的规则/问题库后，使用 VideoLLaMA3-7B 的 SRCC 从 0.757 剧降至 0.406；使用 MiniCPM-V-4.5 时，带规则库的 SRCC 达到 0.847。这一对比直接证明了参考驱动的规则库是世界知识维度高性能的**必要条件**。

- **原子指标的独立有效性**（Table 3）：即使单独使用原子指标（如 CatCov 在语义维度上 SRCC 达 0.734，ECR 在事件维度上 SRCC 达 0.718），也获得了与人类评分中等到强的相关性，验证了基于参考视频提取的证据本身具有判别力。

- **学习聚合器的增益**：线性聚合器在所有维度上都比单个原子指标获得了更高的 SRCC/PLCC/KRCC，表明模型从原子指标中学习到了更好的组合方式，但聚合器的增益相对原子指标本身较小，进一步印证了参考驱动证据的核心地位。

### 6. 创新边界与局限

尽管参考驱动的评估范式在可解释性和人类一致性上取得了显著突破，其创新边界同样清晰：

- **对参考视频的强依赖**：框架的有效性建立在高质量参考视频可获取的前提下，对于无法获得对应参考的开放场景，适用性受限。
- **线性聚合假设**：维度分数的线性聚合假设原子指标与人类评分之间为线性关系，可能无法捕捉更复杂的非线性交互。
- **MLLM 的偏见传递**：世界知识评估依赖 MLLM 生成规则和进行 VQA 评分，其偏见和幻觉可能传递到最终分数，需要进一步验证和校准。



Ref4D-VideoBench 的核心设计理念是将视频生成评估从“文本-视频对齐”范式转变为“参考-视频一致性检查”范式。其整体 pipeline 如图 1 所示，以一对**参考视频**和**生成视频**为输入，通过统一的**证据提取前置模块**为四个评估维度提供结构化时空证据，随后各维度独立计算可解释的原子指标，最终输出四维评估分数。

### 证据提取前置模块

该模块是整个框架的感知基础，对每对视频并行执行三类证据提取：

- **实体-属性证据**：利用多模态大模型（MLLM）分别查询参考视频和生成视频，获得结构化的实体-属性列表，为基本语义对齐维度提供匹配对象。
- **事件图证据**：通过通用事件检测器将视频分割为时间窗口，MLLM 对每个窗口生成事件描述，合并相邻高语义相似度窗口后构建事件图，记录事件内容、时序关系与持续时间。
- **运动信号证据**：分离前景与背景区域，通过点追踪获取运动轨迹，提取相对运动的方向、幅度和平滑度统计量，同时计算重复帧率和低速段比例作为运动退化指标。

这些证据共同构成四个评估维度的结构化输入，使得后续评分不再是黑盒相似度，而是基于显式证据的规则化推理。

### 四维评估体系

框架将生成视频质量分解为四个可独立解释的维度：

1. **基本语义对齐**：基于实体-属性证据，通过软匹配计算类别覆盖率（CatCov）、属性完整性得分（AIC）和幻觉惩罚，评估生成视频是否忠实再现参考视频中的实体及其属性绑定关系。
2. **运动一致性**：基于前景-背景相对运动信号，计算方向、幅度、平滑度三项差异得分，并结合重复帧率（RF）和低速段比例（LS）两项退化指标，评估运动模式与参考视频的一致性及运动质量。
3. **事件时间一致性**：基于事件图证据，通过事件图对齐（EGA）、事件关系一致性（ERel）和事件覆盖与冗余（ECR）三项指标，评估事件内容、时序逻辑和覆盖度的保真性。
4. **世界知识一致性**：基于语义和事件证据，自动推导物理规则、因果规则和安全规则，生成逐视频的 VQA 问题库，利用 MLLM 对生成视频进行定向问答并加权评分，评估常识违规程度。

### 分数聚合机制

对于语义、运动和事件三个维度，框架将各自内部的原子指标向量 $f^{(d)}(x)$ 通过线性聚合器组合为最终维度分数：

$$S^{(d)}(x) = w^{(d)\top} f^{(d)}(x) + b^{(d)}$$

权重 $w^{(d)}$ 和偏置 $b^{(d)}$ 在训练集上以最小二乘法拟合人类评分的 z-score 化 MOS 得到，测试集上报告相关性。世界知识维度不涉及聚合器训练，直接通过加权平均公式 $S_{\mathrm{world}} = \frac{\sum_{q \in B^{+}} \alpha_q \tilde{c}_q}{\sum_{q \in B^{+}} \alpha_q}$ 计算最终分数，在全样本上报告相关性。

这一设计使评估结果既具备样本级的细粒度诊断能力（每个原子指标均可单独回溯），又在维度层面与人类判断保持高度一致。





### 1. 评估框架总览

Ref4D-VideoBench 的核心设计是将评估从“文本-视频对齐”转变为“参考视频-生成视频一致性检查”。框架由五个功能模块构成，如 Figure 1 所示：证据提取前置模块统一为后续四个维度（基本语义对齐、运动一致性、事件时间一致性、世界知识一致性）提供结构化输入；每个维度内部由若干原子指标组成，最终通过线性聚合器得到维度分数。

### 2. 证据提取前置模块

该模块对每对参考视频 $V^\text{ref}$ 与生成视频 $V^\text{gen}$ 提取四类结构化证据：

- **实体-属性列表**：利用 MLLM 分别查询两个视频，获得实体及其属性的结构化描述，作为语义对齐的输入。
- **事件分割与事件图**：通用事件检测器将视频切分为时间窗口，MLLM 对每窗口生成事件描述；相邻窗口若语义相似度高于阈值则合并，最终得到精炼的事件序列并构建事件图。
- **运动统计量**：分离前景/背景，通过点追踪提取相对运动，计算方向、幅度、平滑度差异及退化指标（重复帧率 RF、低速段比例 LS）。
- **世界知识规则**：基于语义和事件证据，为每个视频自动推导物理、因果和安全规则，并转化为定制化 VQA 问题库。

### 3. 维度分数线性聚合器

对于语义、运动、事件三个维度，设原子指标向量为 $f^{(d)}(x)$，维度分数由线性聚合器给出：

$$S^{(d)}(x) = w^{(d)\top} f^{(d)}(x) + b^{(d)} \tag{1}$$

权重 $w^{(d)}$ 和偏置 $b^{(d)}$ 在训练集上通过最小二乘拟合人类评分的 z-score 标准化 MOS 得到。世界知识维度不涉及聚合器训练，直接在全样本上计算相关性。

### 4. 基本语义对齐模块

该模块评估生成视频是否忠实再现参考视频中的实体与属性。

**实体软匹配**：对参考实体 $r$ 与生成实体 $g$ 计算语义相似度 $w(r,g) \in [0,1]$，利用匈牙利算法求解一对一最大权二分匹配，得到匹配集 $\mathcal{M}_\text{semantic}$。

**类别覆盖率 (CatCov)**：衡量参考实体的召回程度。对每个参考实体 $r$，取其匹配到的生成实体的最大相似度：

$$\text{cov}(r) = \max_{(r,g) \in \mathcal{M}_{\text{semantic}}} w(r,g) \tag{2}$$

若 $r$ 未匹配则为 0。CatCov 取所有参考实体的平均值。

**属性完整性得分 (AIC)**：综合评估属性覆盖与绑定准确性：

$$S_{\text{AIC}} = \text{Coverage} \cdot (1 - \text{Misbind}) \tag{3}$$

其中 Coverage 为正确再现的属性比例，Misbind 为属性错配率（属性绑定到错误实体的比例）。

**幻觉惩罚**：对生成视频中出现但参考视频中不存在的实体施加额外惩罚。

### 5. 运动一致性模块

该模块评估生成视频的运动模式是否与参考一致且无退化。

**相对运动**：为消除相机运动干扰，聚焦对象自身动态，定义相对运动：

$$\mathbf{r}(t) = \mathbf{v}^{\text{fg}}(t) - \mathbf{v}^{\text{bg}}(t) \tag{5}$$

其中 $\mathbf{v}^{\text{fg}}(t)$ 和 $\mathbf{v}^{\text{bg}}(t)$ 分别为前景和背景的平均速度向量。

**运动差异评分**：对方向、幅度、平滑度三个维度分别计算差异 $D_k$（$k \in \{\text{dir}, \text{mag}, \text{smo}\}$），并通过指数映射转化为 $[0,1]$ 区间的分数：

$$S_k = \exp(-\lambda_k D_k), \quad \lambda_k = 1 \tag{4.3}$$

**退化指标**：重复帧率 RF 衡量连续相同帧的比例，低速段比例 LS 衡量运动幅度过小的时间段占比。运动特征向量 $\{S_\text{dir}, S_\text{mag}, S_\text{smo}, \text{RF}, \text{LS}\}$ 输入式 (1) 的聚合器。

### 6. 事件时间一致性模块

该模块基于事件图评估生成视频的事件内容、时序关系和覆盖度。

**事件图对齐 (EGA)**：对匹配事件对 $(i,j) \in \mathcal{M}_\text{event}$，以事件长度 $\omega_i$ 为权重，加权平均其综合对齐度 $q_{ij}$（融合语义相似度和时间交并比）：

$$S_{\text{EGA}} = \frac{\sum_{(i,j)\in\mathcal{M}_{\text{event}}} \omega_i q_{ij}}{\sum_{(i,j)\in\mathcal{M}_{\text{event}}} \omega_i} \tag{8}$$

**事件关系一致性 (ERel)**：衡量匹配事件对之间的时序关系（如 before、after、overlap）是否一致。

**事件覆盖与冗余 (ECR)**：平衡参考事件覆盖度 $C_\text{ref}$ 和生成视频中未出现幻觉事件的比率 $(1 - H_\text{gen})$：

$$S_{\text{ECR}} = \frac{2 C_{\text{ref}} (1 - H_{\text{gen}})}{C_{\text{ref}} + (1 - H_{\text{gen}}) + \epsilon} \tag{10}$$

其中 $H_\text{gen}$ 为生成视频中无法匹配到参考事件的“幻觉事件”比例，$\epsilon$ 为防止除零的小常数。

### 7. 世界知识一致性模块

该模块不依赖聚合器训练，而是通过定制化 VQA 问题库直接评分。

**规则生成**：从参考视频的语义和事件证据中自动推导物理规则（如“物体不应悬浮”）、因果规则（如“碰撞后物体应移动”）和安全规则。

**问题库构建**：为每个视频生成定制化问题库 $B^+$，每个问题 $q$ 附带重要性权重 $\alpha_q$（由问题类型权重、所需信号权重和难度共同决定）。

**世界知识一致性分数**：MLLM 对生成视频回答每个问题，得出一致性评分 $\tilde{c}_q$，最终分数为加权平均：

$$S_{\text{world}} = \frac{\sum_{q \in B^{+}} \alpha_q \tilde{c}_q}{\sum_{q \in B^{+}} \alpha_q} \tag{11}$$

消融实验（Table 4）表明，移除基于参考视频构建的规则库后，SRCC 从 0.847 剧降至 0.406，验证了参考驱动规则库是该维度的核心驱动力。



## 实验与关键发现

### 主结果：四维人类相关性评估

Ref4D-VideoBench 在全部四个评估维度上均显著优于代表性无参考基线。Table 1 报告了样本级 SRCC/PLCC/KRCC 相关性：语义维度 SRCC 达到 0.822，而最佳无参考基线 **Q-Align**（Wu et al., ICML 2024）仅为 0.317，提升 +0.505；运动维度 SRCC 0.659 vs. 0.358（+0.301）；事件维度 SRCC 0.755，最强无参考基线仅 0.220（+0.535）；世界知识维度 SRCC 0.847 vs. 0.391（+0.456）。PLCC 和 KRCC 呈现一致趋势，表明参考驱动评估在各维度上均实现了与人类判断的强对齐。

![[assets/figures/papers/paper_list_l2210_https_openaccess_thecvf_com_content_CVPR2026_html_Wei_Ref4D_VideoBench_F/figures/003_Table_1.jpg]]
*Table 1: Sample-level correlations with human ratings on Ref4D-VideoBench. For our evaluation framework, we report test-set correlations with aggregators fitted on a disjoint training split for the semantic/motion/event dimensions, while the correlations are computed on all samples for the world knowledge dimension (because we do not need to train an aggregator). “–” marks not applicable. Best is bold; second-best is underlined*

该优势在模型级均值相关性上同样成立。Figure 3 显示，各维度分数与人类 MOSz 的线性拟合良好，说明框架能够有效区分不同 T2V 模型的相对优劣。Table 2 进一步给出了八个模型的四维得分与排名：闭源模型 **Sora 2** 在语义、事件和世界知识维度均居首，而开源模型 **CogVideoX-5B** 在运动维度表现最优。这一细粒度诊断能力是无参考方法无法提供的。

![[assets/figures/papers/paper_list_l2210_https_openaccess_thecvf_com_content_CVPR2026_html_Wei_Ref4D_VideoBench_F/figures/004_Figure_3.jpg]]
*Figure 3: Model-level mean correlation with human ratings. Each point is a T2V model; lines show least-squares fits. The vertical axis shows our score for each dimension, and the horizontal axis is the corresponding human rating (MOSz)*

![[assets/figures/papers/paper_list_l2210_https_openaccess_thecvf_com_content_CVPR2026_html_Wei_Ref4D_VideoBench_F/figures/005_Table_2.jpg]]
*Table 2: T2V models’ performance on Ref4D-VideoBench. Best in each column is bold*

### 消融实验

#### 原子指标有效性

Table 3 报告了各维度原子指标单独与人类评分的相关性。语义维度中，**CatCov**（类别覆盖率）单独达到 SRCC 0.734，接近最终聚合分数（0.822），表明实体召回是语义对齐的主驱动力。事件维度中，**ECR**（事件覆盖与冗余）单独获得 SRCC 0.718，验证了覆盖度-冗余平衡机制的有效性。运动维度中，各原子指标单独相关性中等（SRCC 0.4–0.6），但线性聚合后提升至 0.659，说明多维运动信号存在互补性。

![[assets/figures/papers/paper_list_l2210_https_openaccess_thecvf_com_content_CVPR2026_html_Wei_Ref4D_VideoBench_F/figures/007_Table_3.jpg]]
*Table 3: Atomic metrics vs. human ratings. We report samplelevel SRCC/PLCC/KRCC for the atomic metrics in our framework, computed on all samples. Best per dimension is in bold, and second-best is underlined*

#### 世界知识规则库消融

Table 4 的消融结果揭示了参考驱动规则库的核心作用。使用 **VideoLLaMA3-7B** 作为评判器时，移除基于参考视频构建的规则/问题库后，SRCC 从 0.757 骤降至 0.406；使用 **MiniCPM-V-4.5** 时，带规则库的 SRCC 达到 0.847。这一对比直接证明：世界知识维度的高性能并非来自 MLLM 的通用推理能力，而是源于参考视频提供的场景特定物理、因果和安全规则。

![[assets/figures/papers/paper_list_l2210_https_openaccess_thecvf_com_content_CVPR2026_html_Wei_Ref4D_VideoBench_F/figures/008_Table_4.jpg]]
*Table 4: Ablation results for world knowledge consistency. We report SRCC/PLCC/KRCC on all samples (best in bold)*

#### 聚合器学习效果

语义、运动和事件维度均采用最小二乘学习的线性聚合器将原子指标组合为最终分数。Table 1 与 Table 3 的对比表明，学习到的聚合器在所有维度上均优于单一最优原子指标，且训练/测试集按样本 ID 分割，避免了场景泄露。世界知识维度无需聚合器训练，其分数直接由加权 VQA 一致性计算，相关性在全样本上报告。

### 失败模式与诊断能力

Figure 4 以羚羊追逐场景为例展示了框架的逐样本诊断能力。**Sora 2** 生成的视频在四个维度上均优于 **VideoCrafter2**：语义维度中，VideoCrafter2 丢失了“羚羊”实体并出现幻觉物体；运动维度中，其前景运动幅度与方向与参考视频偏差显著；事件维度中，事件时间关系错乱；世界知识维度中，违反了“追逐者应在被追逐者后方”的物理常识。这种细粒度、可归因的失败分析是无参考评估无法实现的。

![[assets/figures/papers/paper_list_l2210_https_openaccess_thecvf_com_content_CVPR2026_html_Wei_Ref4D_VideoBench_F/figures/006_Figure_4.jpg]]
*Figure 4: Per-sample diagnosis on an antelope-chase scene. This figure shows a detailed four-dimensional evaluation of videos generated by two models (Sora2 and VideoCrafter2). Overall, Sora2 performs better than VideoCrafter2 under all dimensions*

### 局限性

需要指出以下限制：(1) 框架强依赖高质量参考视频，对于无法获得对应参考的开放场景适用性受限；(2) 线性聚合器假设原子指标与人类评分间为线性关系，可能遗漏非线性交互；(3) 世界知识评估依赖 MLLM 生成规则并进行 VQA 评分，其偏见和幻觉可能传递至最终分数；(4) 当前数据集规模为 600 个视频，主题覆盖有限，泛化性需进一步验证。



## 定位与知识库关联

### 1. 与现有评估范式的关键差异

Ref4D-VideoBench 的核心突破在于将文本到视频（T2V）评估从**无参考的文本-视频对齐范式**转变为**基于参考视频的显式证据一致性检查范式**。这一转变由三个维度的设计差异支撑：

| 设计维度 | 无参考基线（CLIPScore / BLIPScore / Q‑Align） | Ref4D‑VideoBench（本文） |
|---------|---------------------------------------------|-------------------------|
| **评估输入** | 仅文本提示 | 参考视频 + 文本提示 |
| **评估粒度** | 整体质量分数或多维整体评分 | 四维可解释分数（语义、运动、事件、世界知识），每维由多个原子指标聚合 |
| **评分器机制** | 黑盒 MLLM 或 CLIP 式相似度 | 结构化证据提取 + 显式原子指标 + 学习的线性聚合器 |

**无参考基线的瓶颈**：CLIPScore（Radford et al., ICML 2021）和 BLIPScore（Li et al., ICML 2022）仅计算文本与视频帧的全局嵌入相似度，缺乏对时序动态、事件因果和物理常识的感知能力。Q‑Align（Wu et al., ICML 2024）虽引入多模态大模型（MLLM）进行评分，但其评分过程仍是黑盒的，无法对“为何扣分”给出可解释的归因。这些方法在 Ref4D‑VideoBench 上的样本级 SRCC 普遍低于 0.4（Table 1），尤其在事件维度上，最强无参考基线仅达 0.220，暴露了仅依赖文本提示的评估在细粒度失败诊断上的根本性不足。

**本文的因果杠杆**：引入高质量参考视频作为结构化时空证据源，使评估从“文本-视频相似度”的模糊匹配转变为“参考-生成视频一致性”的显式检查。这一设计使得每个维度的评分都可追溯到具体的原子指标（如 CatCov、ECR、重复帧率等），从而实现了与人类判断高度对齐（四维 SRCC 0.659–0.847）且可诊断的评估。

### 2. 方法谱系定位

Ref4D‑VideoBench 处于**参考驱动视频评估**的新兴节点，与以下工作形成互补或对照关系：

- **无参考评估**（CLIPScore / BLIPScore / Q‑Align）：如上述，本文在四个维度上均大幅超越这些方法，证明参考证据是提升评估可信度的关键杠杆。
- **基于视频-文本检索的评估**（如 T2VQA、VBench）：这些方法依赖预定义的文本查询或固定维度，缺乏样本级定制化的证据提取。本文的逐视频规则库构建（世界知识维度）和事件图对齐（事件维度）提供了更精细的诊断能力。
- **基于物理模拟的评估**：部分工作尝试通过物理引擎验证生成视频的物理一致性，但受限于模拟器的覆盖范围。本文的世界知识维度通过 MLLM 生成规则并转换为 VQA 问题库，以更灵活的方式覆盖物理、因果和安全常识。
- **人类评估协议**：传统人类评估（如 MOS）虽可靠但成本高昂且不可扩展。Ref4D‑VideoBench 的目标并非替代人类评估，而是提供一个与人类判断高度对齐的自动化代理，使大规模模型诊断成为可能。

### 3. 适用边界与局限

尽管 Ref4D‑VideoBench 在参考驱动场景下表现优异，其适用性存在以下明确边界：

1. **强依赖高质量参考视频**：评估框架的所有四个维度均以参考视频为证据源。对于无法获得对应参考视频的开放域生成场景（如纯文本提示的创意生成），该方法无法直接适用。这是参考驱动范式的固有边界，而非实现缺陷。

2. **线性聚合器的假设限制**：语义、运动和事件维度的最终分数通过最小二乘学习的线性组合（Eq. (1)）获得。这一设计假设原子指标与人类评分之间为线性关系，可能无法捕捉更复杂的非线性交互。文中报告学习到的聚合器在所有维度上均优于单个原子指标（Sec. 6），但未探索非线性聚合器是否可进一步提升。

3. **世界知识评估的 MLLM 依赖**：世界知识维度的规则生成和 VQA 评分均依赖 MLLM（如 MiniCPM‑V‑4.5、VideoLLaMA3‑7B）。MLLM 自身的偏见和幻觉可能传递到最终分数。消融实验（Table 4）表明，去除基于参考视频构建的规则库后，SRCC 从 0.847 剧降至 0.406，证明规则库是核心驱动力，但 MLLM 评判器的可靠性仍构成潜在风险。

4. **数据集规模与主题覆盖**：当前数据集包含 600 个参考视频，主题覆盖有限。文中已指出这一局限，并建议未来扩展以验证泛化性。

### 4. 开放问题与未来方向

基于上述分析，以下开放问题值得后续工作关注：

- **无参考扩展**：能否将参考驱动的证据提取过程转化为自监督或弱监督信号，使框架在无参考视频的场景下仍能提供部分维度的评估？例如，世界知识规则库的构建是否可仅依赖生成视频自身的内容？
- **非线性聚合器设计**：学习到的维度聚合器是否可以采用更可解释的非线性模型（如决策树、广义加性模型），在保持强相关性的同时提升诊断透明度？
- **世界知识规则库的鲁棒性**：在多复杂场景下，MLLM 自动构建的规则库能保持多高的可靠性？是否可引入外部知识库（如 ConceptNet、物理常识库）增强规则生成的覆盖面和准确性？
- **评估到优化的闭环**：Ref4D‑VideoBench 的原子指标是否可直接用作生成模型对齐训练（如 RLHF）的奖励函数？这需要验证原子指标的可微性、平滑性及其对生成质量的因果影响。

**总结**：Ref4D‑VideoBench 通过引入参考视频作为结构化时空证据，在评估可信度、可解释性和诊断能力上实现了对无参考范式的显著超越。其适用边界明确，开放问题指向无参考扩展、聚合器改进和评估-优化闭环等方向，为视频生成评估领域提供了清晰的后续研究路标。



## 原文 PDF

![[paperPDFs/CVPR_2026/Ref4D_VideoBench_Four_Dimensional_Reference_Based_Evaluation_of_Text_to_Video_Generative_Models.pdf]]
