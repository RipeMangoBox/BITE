---
title: Training-free Guidance in Text-to-Video Generation via Multimodal Planning and Structured Noise Initialization
type: paper
paper_level: A
venue: arXiv
year: 2025
pdf_ref: paperPDFs/arxiv_2025/Training_free_Guidance_in_Text_to_Video_Generation_via_Multimodal_Planning_and_Structured_Noise_Initialization.pdf
aliases:
- VMMSG
- TFGTVGMPSNI
tags:
- arxiv_2025
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/image_and_video_generation
- topic/generative_models_diffusion
- topic/generative_models_diffusion/diffusion_image_video
core_operator: 通过多模态规划生成包含背景、前景物体及轨迹的视频草图（VIDEO SKETCH），并利用扩散模型正向加噪（噪声反转）将草图的空间与运动信息注入初始噪声，从中间时间步开始去噪，实现无需微调或注意力操作的布局控制；LLM动态推断的噪声反转比α是该控制的核心旋钮。
primary_logic: 将布局与运动先验编码为结构化初始噪声（而非在去噪过程中修改注意力图），使大规模T2V模型可在推理时无需额外内存即获得训练无关的布局引导；同时利用视觉检测工具（RAM、Grounding-DINO）为LLM的空间推理提供接地，确保前景物体与背景的空间一致性。
claims:
- VIDEO-MSG在VideoCrafter2和CogVideoX-5B上均显著提升motion binding、spatial relationships和numeracy得分，其中VideoCrafter2的Motion提升0.1499，CogVideoX-5B的Motion提升0.1544。
- VIDEO-MSG无需微调或注意力操作，相比LVD内存更高效：可在A6000 48GB GPU上驱动CogVideoX-5B，而LVD在A100 80GB GPU上亦无法运行。
- 降低噪声反转比α可增强布局控制（Motion得分提升）但会降低运动平滑度，LLM根据文本描述动态推断α能在二者之间取得良好平衡。
- T2VCompBench 上 Motion Binding (VideoCrafter2) = 0.3732
---

# Training-free Guidance in Text-to-Video Generation via Multimodal Planning and Structured Noise Initialization

> [!tip] 核心洞察
> 将布局与运动先验编码为结构化初始噪声（而非在去噪过程中修改注意力图），使大规模T2V模型可在推理时无需额外内存即获得训练无关的布局引导；同时利用视觉检测工具（RAM、Grounding-DINO）为LLM的空间推理提供接地，确保前景物体与背景的空间一致性。

| 字段 | 内容 |
|------|------|
| 中文题名 | 基于多模态规划与结构化噪声初始化的文本到视频生成无训练引导 |
| 英文题名 | Training-free Guidance in Text-to-Video Generation via Multimodal Planning and Structured Noise Initialization |
| 会议/期刊 | arXiv 2025 |
| Links | [paper](https://arxiv.org/abs/2504.08641) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/image_and_video_generation #topic/generative_models_diffusion #topic/generative_models_diffusion/diffusion_image_video |
| Method | VIDEO-MSG (Multimodal Sketch Guidance) |
| Dataset | T2VCompBench |

> [!tip] 效果简介
> - T2VCompBench 上，Motion Binding (VideoCrafter2) 0.3732 vs 0.2233 (+0.1499)；Spatial Relationships (VideoCrafter2) 0.5866 vs 0.4891 (+0.0975)；Numeracy (VideoCrafter2) 0.3138 vs 0.2041 (+0.1097)。

## 概述

文本到视频（T2V）扩散模型在生成高质量视频方面取得了显著进展，但在精确控制空间布局与物体轨迹方面仍面临根本性瓶颈。现有基于布局引导的方法通常需要模型微调或在去噪过程中迭代操纵注意力图，这不仅带来高昂的内存开销，还限制了其在大规模模型上的可扩展性。

**VIDEO-MSG**（Multimodal Sketch Guidance）针对上述瓶颈提出了一个训练无关的引导框架。其核心洞察是：将布局与运动先验编码为结构化初始噪声，而非在去噪过程中修改注意力图，从而使大规模T2V模型在推理时无需额外内存即可获得精确的布局引导。具体而言，VIDEO-MSG通过多模态规划生成包含背景、前景物体及轨迹的视频草图（VIDEO SKETCH），并利用扩散模型的正向加噪过程将草图的空间与运动信息注入初始噪声，从中间时间步开始去噪生成最终视频。其中，由LLM动态推断的噪声反转比 $\alpha$ 是该框架的核心控制旋钮，决定了布局控制强度与运动平滑度之间的平衡。

该方法在VideoCrafter2和CogVideoX-5B两个开源骨干模型上均取得了显著提升。在T2VCompBench基准上，VideoCrafter2的Motion Binding得分从0.2233提升至0.3732（+0.1499），Spatial Relationships从0.4891提升至0.5866（+0.0975），Numeracy从0.2041提升至0.3138（+0.1097）；CogVideoX-5B的Motion Binding得分从0.2943提升至0.4487（+0.1544），相对增益达52.46%。更重要的是，VIDEO-MSG无需微调或注意力操作，可在A6000 48GB GPU上驱动CogVideoX-5B，而基于注意力操纵的对比方法LVD即使在A100 80GB GPU上亦无法运行，充分验证了其在内存效率与可扩展性上的优势。

在方法谱系上，VIDEO-MSG位于**训练无关的布局引导T2V生成**路径，与基于注意力操纵的方法（如LVD）和基于微调的方法形成对比。其知识贡献在于：将多模态大语言模型（MLLM）的空间推理能力与视觉感知工具（RAM、Grounding-DINO、SAM）的接地能力相结合，通过噪声反转机制将高层布局规划转化为低层噪声先验，实现了无需修改模型内部表示的即插即用式引导。

## 背景与动机

文本到视频（T2V）扩散模型近年来取得了显著进展，大规模模型如 **VideoCrafter2** 和 **CogVideoX-5B**（Yang et al., arXiv 2024）已能生成视觉质量较高的视频。然而，仅依赖文本提示的生成方式在精确控制空间布局与物体运动轨迹方面存在根本性瓶颈——模型往往难以忠实地将“左侧的红色气球向右移动”这类空间-运动复合指令转化为准确的像素级表现。

现有解决布局控制问题的方法主要分为两类：一类需要对预训练T2V模型进行微调，另一类则在去噪过程中迭代操纵注意力图（如 **LVD**）。这两类方法均存在显著缺陷：微调方法破坏了基础模型的通用性且计算开销大，注意力操纵方法则因需在推理时额外存储和修改注意力张量而导致极高的内存开销与可扩展性差——实验表明，LVD 即使在 A100 80GB GPU 上也无法驱动 CogVideoX-5B 规模的模型。

上述困境揭示了一个深层矛盾：**布局与运动先验的引入方式**决定了方法能否在保持训练无关性的同时实现高效推理。本文的核心洞察在于，可以将布局与运动先验编码为**结构化初始噪声**，而非在去噪过程中修改注意力图。具体而言，通过多模态规划生成包含背景、前景物体及轨迹的视频草图（VIDEO SKETCH），并利用扩散模型的正向加噪过程（噪声反转）将草图的空间与运动信息注入初始噪声，从中间时间步开始去噪，即可实现无需微调或注意力操作的布局控制。

这一思路将问题从“在生成过程中约束模型”转化为“在生成开始前为模型提供正确的初始化”，其关键控制旋钮是噪声反转比 α——由 LLM 根据文本描述动态推断，决定了初始噪声中保留多少来自视频草图的结构信息。该设计使大规模T2V模型可在推理时无需额外内存即获得训练无关的布局引导，从而突破了现有方法在可扩展性上的瓶颈。

## 核心创新

VIDEO-MSG 的核心创新在于将**布局与运动先验编码为结构化初始噪声**，而非像现有方法那样在去噪过程中迭代修改注意力图。这一设计转变直接回应了当前文本到视频（T2V）生成的核心瓶颈：扩散模型难以精确控制空间布局与物体轨迹，而基于注意力操纵的布局引导方法（如 **LVD**）需要微调或在线迭代计算，导致高内存开销与可扩展性差。

### 从注意力操纵到结构化噪声初始化

传统布局引导方法在去噪的每一步修改交叉注意力图以注入空间约束，这要求模型在推理时额外维护和操作注意力张量，内存需求随模型规模急剧增长。VIDEO-MSG 用一个**噪声反转（Noise Inversion）** 步骤替代了这一范式：它首先通过多模态规划生成一个包含背景、前景物体及轨迹的视频草图（VIDEO SKETCH），再利用扩散模型的正向加噪过程将该草图的空间与运动信息注入初始噪声，从中间时间步开始去噪生成最终视频。

这一设计的因果机制在于：扩散模型的去噪过程本质上是从噪声中恢复结构化信息。当初始噪声本身已编码了目标布局的粗略结构时，模型无需额外的注意力约束即可自然生成符合空间规划的帧序列。因此，**噪声初始值**这一关键槽位从“纯随机噪声（从 $t = T$ 开始去噪）”变为“基于 VIDEO SKETCH 通过正向扩散得到的结构化初始噪声（从 $t = \alpha T$ 开始去噪）”，而**布局信息引入方式**则从“仅文本提示或迭代修改注意力图”变为“通过多模态规划预先生成视频草图，将布局与轨迹编码为初始噪声，无需注意力操纵”。

### 噪声反转比 $\alpha$：控制布局强度的核心旋钮

结构化噪声初始化的强度由噪声反转比 $\alpha$ 控制，其定义为：

$$t^{\mathrm{inv}} = \alpha \times T, \quad \alpha \in (0.0, 1.0)$$

其中 $T$ 为总去噪步数。$\alpha$ 越小，初始噪声中保留的视频草图结构越多，布局控制力越强，但可能牺牲运动平滑度；$\alpha$ 越大，模型越接近纯随机噪声去噪，运动更平滑但布局约束减弱。消融实验（Table 2）证实了这一权衡：$\alpha = 0.5$ 时 Motion 得分最高（0.3980），但 Motion Smoothness 降至 98.58；$\alpha = 0.9$ 时平滑度最佳但控制力弱。

VIDEO-MSG 的另一个关键创新是**利用 LLM 根据文本描述动态推断 $\alpha$**，而非使用固定值。LLM 通过分析提示词中涉及的运动类型和空间约束强度，在骨干模型特定的经验范围内选择合适的反转比（VideoCrafter2 用 $[0.5, 0.8]$，CogVideoX-5B 用 $[0.7, 0.9]$），从而在布局控制与运动平滑度之间取得良好平衡。这一设计使方法无需针对每个提示词手动调参，提升了实用性。

### 多模态规划中的接地机制

VIDEO-MSG 的布局规划并非凭空生成。它引入了一个关键的**视觉接地**环节：在规划前景物体位置时，先用 RAM 和 Grounding-DINO 检测背景图像中已存在的物体及其边界框，再将检测结果作为上下文输入 GPT-4o 进行空间推理。这确保了 LLM 生成的前景物体布局与背景中的实际物体保持空间一致性，避免了物体重叠或放置不当的问题。消融实验（Figure 4、Figure 5）表明，缺少背景物体检测或前景物体分割（SAM）任一模块，都会导致放置错误或融合不自然。

### 与 baseline 的系统性差异

| 设计维度 | Baseline（VideoCrafter2 / CogVideoX-5B） | VIDEO-MSG |
|---------|----------------------------------------|-----------|
| 噪声初始值 | 纯随机噪声（$t = T$） | 基于 VIDEO SKETCH 的结构化噪声（$t = \alpha T$） |
| 布局信息引入 | 仅文本提示 | 多模态规划生成视频草图，编码为初始噪声 |
| 去噪起始时间步 | $t = T$ | $t = \alpha \times T$，$\alpha$ 由 LLM 动态推断 |
| 推理时内存 | 仅模型本身 | 仅模型本身（无额外注意力操作） |
| 可扩展性 | 受限于模型本身 | 可在 A6000 48GB GPU 上驱动 CogVideoX-5B |

### 创新边界与局限

需要指出的是，VIDEO-MSG 的创新集中于**空间布局与运动轨迹的绑定**，在动态属性绑定（Dynamic-attr）、物体动作（Action）和交互（Interaction）类别上提升有限。这是因为边界框引导本质上只能约束物体的空间位置，无法表达物体的状态变化（如“变红”）或物体间的动态交互（如“拿起”）。如何将引导形式从边界框扩展至更丰富的运动表示，是该方法当前未解决的核心问题。此外，$\alpha$ 的 LLM 推断基于启发式提示，缺乏严格优化，在特定文本上可能无法达到最佳平衡——这一点的实验证据尚不充分，需要进一步验证。

## 整体框架

VIDEO-MSG 提出一种训练无关的文本到视频（T2V）布局引导范式，其核心思想是将布局与运动先验编码为**结构化初始噪声**，而非在去噪过程中修改注意力图。如图1所示，与单模型生成（a）和基于注意力的布局引导（b）不同，VIDEO-MSG（c）无需微调或推理时额外的注意力操作内存，因此可轻松适配大规模T2V模型。

方法由三个顺序阶段构成（图2）：

1. **背景规划（Background Planner）**：多模态大语言模型（MLLM，具体为GPT-4o）根据原始文本提示生成仅包含静态背景的详细描述，明确排除运动或关键前景物体。随后利用文生图（T2I）模型渲染背景图像，再通过图像到视频（I2V）模型为其注入自然动画，形成具有细微运动（如水流、云动）的背景视频。

2. **前景布局与轨迹规划（Foreground Layout & Trajectory Planner）**：首先使用RAM与Grounding-DINO检测背景图像中的物体边界框，将这些空间信息馈入MLLM，使其在理解背景空间结构的基础上推理前景物体的合理位置与逐帧轨迹。MLLM输出前景物体的边界框序列（即时空布局）。对每个前景物体，用T2I模型生成外观图像，再通过SAM分割提取前景区域，最后按规划的边界框序列将其合成到背景视频帧上，形成完整的**视频草图（VIDEO SKETCH）**。

3. **结构化噪声初始化生成（Structured Noise Initialization Generator）**：将视频草图编码为潜变量 $z_0$，通过正向扩散过程注入噪声至中间时间步 $t^{\mathrm{inv}}$：
   $$z_{t^{\mathrm{inv}}} = \sqrt{\alpha_t} z_0 + \sqrt{1 - \alpha_{t^{\mathrm{inv}}}} \epsilon, \quad \epsilon \sim \mathcal{N}(0, I)$$
   其中 $\alpha_t = \prod_{s=1}^{t} (1 - \beta_s)$ 为累积噪声系数。随后从 $t^{\mathrm{inv}} = \alpha \times T$ 开始，利用DPM-Solver++反向去噪生成最终视频。噪声反转比 $\alpha$ 由LLM根据文本描述动态推断——这是平衡布局控制力与运动平滑度的核心控制旋钮：较低的 $\alpha$ 保留更多草图结构（控制力强但平滑度下降），较高的 $\alpha$ 则赋予模型更大生成自由度。

整个流水线的输入为文本提示，输出为符合指定空间布局与物体轨迹的视频。各模块间通过视频草图的潜变量传递信息，下游T2V扩散模型仅需一次标准去噪推理，无需任何架构修改或注意力图操纵。

### 补充图表

![[assets/figures/papers/paper_list_l42_https_arxiv_org_abs_2504_08641/figures/001_Figure.jpg]]
*Figure: (b) Video Generation with Attention-based Layout Guidence Figurel.Comparisonofdiferent ext-to-videogenerationmetods: (a)singlemodelforvideogeneration,(b)videogeneration with (atention-based)layout guidance,andour(c)VIEo-MSG,atraining-freeguidancemethodforTVgenerationbasedonmultiodal planningandstructurednoiseintialization.SinceVIEo-MSGdoes notnedfine-tuning oradditionalmemoryduring inferencetime,it is easiertoadoptlareTVmodels thanpreviousvideolayoutguidancemethodsbasedonfne-tuningoriterativeatentionmanipulation*

![[assets/figures/papers/paper_list_l42_https_arxiv_org_abs_2504_08641/figures/002_Figure_2.jpg]]
*Figure 2: ThrestagesofVDE-MSG.Ithefrststage,theMLMplansspecific globalandlocalcontextsthatfitheprovidedtext-to video prompt.Thetext-to-image(T2)modeluses the MLLMplaedcontexttorender the necessarycomponentsofthevideo.Inthe third stage,we generate video with VIDEO SKETCH via noise inversion*

## 核心模块与公式推导

VIDEO-MSG 的核心由三个串行模块构成：**Background Planner**、**Foreground Layout & Trajectory Planner** 和 **Structured Noise Initialization Generator**。前两个模块负责将文本提示转化为包含空间布局与运动轨迹的“视频草图”（VIDEO SKETCH），第三个模块则通过噪声反转将该草图的先验信息注入扩散模型的初始噪声，从而在无需微调或注意力操纵的条件下实现布局引导。

### 3.1 Background Planner

给定文本提示，首先调用多模态大语言模型（MLLM，具体为 GPT-4o）生成一段**仅描述背景**的文本，明确排除原文中提及的运动物体或关键前景对象。该背景描述随后输入一个文生图（T2I）模型生成背景图像，再通过一个图生视频（I2V）模型为其添加自然的静态摄像机动画，得到背景视频片段。实验表明，采用 FLUX 作为 T2I 模型、CogVideoX-5B 作为 I2V 模型的组合在 Numeracy 指标上优于直接使用 T2V 模型生成背景，而后者在 Motion Binding 上略高（Table 3）。

### 3.2 Foreground Layout & Trajectory Planner

前景规划的核心挑战在于保证前景物体与背景的空间一致性。该模块首先使用 **Recognize-Anything（RAM）** 和 **Grounding-DINO** 检测背景图像中已有的物体及其边界框，然后将这些边界框连同原始文本提示一起输入 GPT-4o。MLLM 据此推理并输出前景物体的**逐帧边界框序列**，即物体的布局与运动轨迹。随后，对每个前景物体使用 T2I 模型生成外观图像，并通过 **SAM** 进行实例分割以去除背景干扰，最终将分割后的前景按边界框序列放置到背景视频的对应帧上，形成完整的 VIDEO SKETCH。消融实验表明，缺少 RAM/Grounding-DINO 会导致前景物体放置错误（Figure 4），而缺少 SAM 分割则会使前景与背景融合不自然（Figure 5）。

### 3.3 Structured Noise Initialization Generator

该模块是本方法实现“训练无关引导”的关键。设 VIDEO SKETCH 编码后的潜变量为 $z_0$，总扩散步数为 $T$。首先通过正向扩散过程将 $z_0$ 加噪至中间时间步 $t^{\mathrm{inv}}$：

$$z_{t^{\mathrm{inv}}} = \sqrt{\alpha_t} z_0 + \sqrt{1 - \alpha_{t^{\mathrm{inv}}}} \epsilon, \quad \epsilon \sim \mathcal{N}(0, I)$$

其中 $\alpha_t = \prod_{s=1}^{t} (1 - \beta_s)$ 为累积噪声系数，$\beta_s$ 为扩散调度器的噪声参数。反转时间步由噪声反转比 $\alpha$ 控制：

$$t^{\mathrm{inv}} = \alpha \times T, \quad \alpha \in (0.0, 1.0)$$

随后以 $z_{t^{\mathrm{inv}}}$ 为初始噪声，使用 DPM-Solver++ 从 $t^{\mathrm{inv}}$ 开始反向去噪，生成最终视频。反向更新的二阶形式为：

$$z_{t-1} = z_t + \lambda_1 \hat{F}(z_t, t) + \lambda_2 \hat{F}(z_t + \lambda_3 \hat{F}(z_t, t), t_m)$$

其中估计漂移项 $\hat{F}(z, t) = -\frac{1}{2} \beta_t z - g^2(t) \epsilon_\theta(z, t)$，$\epsilon_\theta$ 为扩散模型的噪声预测网络。

**噪声反转比 $\alpha$ 是该方法的核心控制旋钮**：较低的 $\alpha$（如 0.5）意味着从更早的时间步开始去噪，初始噪声中保留的草图结构信息更多，布局控制力更强（Motion 得分最高达 0.3980），但运动平滑度下降至 98.58；较高的 $\alpha$（如 0.9）则使生成更接近纯随机噪声下的自由生成，平滑度更佳但控制力减弱。VIDEO-MSG 采用 LLM 根据文本描述动态推断 $\alpha$：对于 VideoCrafter2 骨干模型，$\alpha$ 范围取 $[0.5, 0.8]$；对于 CogVideoX-5B，取 $[0.7, 0.9]$。Table 2 的消融实验证实，该动态推断策略能在 Motion 得分与 Motion Smoothness 之间取得良好平衡。

### 补充图表

![[assets/figures/papers/paper_list_l42_https_arxiv_org_abs_2504_08641/figures/009_Figure_6.jpg]]
*Figure 6: Prompt template used to query background description*

![[assets/figures/papers/paper_list_l42_https_arxiv_org_abs_2504_08641/figures/010_Figure_7.jpg]]
*Figure 7: Prompt template used to query foreground object layout and trajectory plan*

![[assets/figures/papers/paper_list_l42_https_arxiv_org_abs_2504_08641/figures/011_Figure_8.jpg]]
*Figure 8: Prompt template used to determine how much noise to inject during inversion*

## 实验与分析

### 核心定量结果：T2V-CompBench 主实验

VIDEO-MSG 在两个不同规模的 T2V 骨干模型上均实现了显著且一致的提升，尤其体现在运动绑定（Motion）、空间关系（Spatial）和数量理解（Numeracy）三个维度。Table 1 给出了完整结果：

- **VideoCrafter2 骨干**：Motion 从 0.2233 提升至 0.3732（+0.1499），Spatial 从 0.4891 提升至 0.5866（+0.0975），Numeracy 从 0.2041 提升至 0.3138（+0.1097）。
- **CogVideoX-5B 骨干**：Motion 从 0.2943 提升至 0.4487（+0.1544），Spatial 从 0.5461 提升至 0.6070（+0.0609），Numeracy 从 0.2603 提升至 0.3647（+0.1044）。

在 VideoCrafter2 上与基于注意力操纵的布局引导方法 **LVD** 的对比中，VIDEO-MSG 在除动态属性绑定（Dynamic-attr）外的所有类别上均优于 LVD，其中 Motion 的领先幅度达 0.1554。更重要的是，VIDEO-MSG 可在 A6000 48GB GPU 上驱动 CogVideoX-5B，而 LVD 即使在 A100 80GB GPU 上也无法运行，验证了结构化噪声初始化在内存效率上的根本优势。

### 消融实验

#### 噪声反转比 α 的影响

噪声反转比 α 是 VIDEO-MSG 的核心控制旋钮，它决定了从视频草图注入初始噪声的强度，进而影响布局控制力与运动平滑度之间的权衡。Table 2 在 VideoCrafter2 骨架上系统消融了 α：

![[assets/figures/papers/paper_list_l42_https_arxiv_org_abs_2504_08641/figures/005_Table_2.jpg]]
*Table 2: Comparisonofdiferentnoise inversionratioα,werewecomparestatic valuesandLLM-baseddynamicvalues.BackboneT2V: VideoCrafter2.Background generator: Flux + CogVideoX-5B*

- **低 α（0.5）**：注入噪声最少，保留草图结构最强，Motion 得分达到最高的 0.3980，但 Motion Smoothness 降至 98.58，视频出现僵硬感。
- **高 α（0.9）**：注入噪声最多，运动平滑度最优（99.23），但布局控制力大幅减弱，Motion 得分仅 0.2787。
- **LLM 动态推断 α**：由 LLM 根据文本描述自动选择 α，在 Motion 得分（0.3732）与平滑度（99.02）之间取得了良好平衡，作为默认策略。

这一消融揭示了结构化噪声初始化的因果机制：α 越低，初始噪声越接近草图潜变量，去噪起点越偏离纯噪声分布，布局约束越强，但同时压缩了扩散模型自身的运动生成空间。LLM 的介入实质上是将语义复杂度映射为噪声注入强度——简单运动场景用高 α 以保持自然感，复杂空间布局用低 α 以增强控制。

#### 背景生成器的选择

Table 3 对比了两种背景生成策略：

![[assets/figures/papers/paper_list_l42_https_arxiv_org_abs_2504_08641/figures/006_Table_3.jpg]]
*Table 3: Ablation studies on different background generators*

- **T2I（FLUX）+ I2V（CogVideoX-5B）**：Numeracy 得分 0.3647，优于纯 T2V 方案。
- **纯 T2V（CogVideoX-5B alone）**：Motion Binding 得分 0.4487，高于 T2I+I2V 方案（0.3732）。

这一差异的根源在于 I2V 管线对“静态摄像机”提示的遵循度更高，有利于保持背景中物体数量的准确性，但 T2I 生成的背景图像在经 I2V 动画化时可能引入额外的运动模糊或不一致性，略微削弱了前景物体的运动绑定。实际应用中需根据任务侧重选择背景生成器。

#### 感知模块的必要性

Figure 4 和 Figure 5 的定性示例验证了两个感知模块的关键作用：

![[assets/figures/papers/paper_list_l42_https_arxiv_org_abs_2504_08641/figures/007_Figure_5.jpg]]
*Figure 5: Example video showing the importance of foreground object segmentation*

![[assets/figures/papers/paper_list_l42_https_arxiv_org_abs_2504_08641/figures/008_Figure_4.jpg]]
*Figure 4: Example video showing the importance of background object detection in foreground object placement*

- **背景物体检测（RAM + Grounding-DINO）**：若不提供背景物体的边界框信息，GPT-4o 在规划前景物体位置时会产生空间冲突（如将物体放置在已有物体之上），导致生成视频中出现不自然的遮挡或穿透。提供检测结果后，LLM 的空间推理获得视觉接地，前景放置显著改善。
- **前景物体分割（SAM）**：直接将 T2I 生成的前景物体图像合并到背景上会导致视觉不连贯——物体周围残留的背景像素与场景格格不入。SAM 分割后仅保留前景区域，融合更加自然。

### 失败模式与局限性

尽管 VIDEO-MSG 在空间布局和运动绑定上取得了显著提升，但在以下类别上改进有限：

- **动态属性绑定（Dynamic-attr）**：VideoCrafter2 上仅从 0.2035 提升至 0.2110，CogVideoX-5B 上从 0.2334 降至 0.2334（无变化）。这是因为边界框只能约束物体的空间位置和轨迹，无法表达颜色变化、形状变形等动态属性。
- **物体动作（Action）与交互（Interaction）**：提升幅度远小于 Motion 和 Spatial。边界框轨迹可以描述“物体从 A 移动到 B”，但难以刻画“人踢足球”中腿与球的接触时机、力度等精细交互——这需要超越边界框的运动表示。

这些失败模式指向一个根本局限：VIDEO-MSG 的草图表示（边界框序列）的表达力上限。当文本描述涉及物体内部状态变化或多物体动态交互时，结构化初始噪声无法编码足够丰富的先验。

### 公平性说明

所有实验均在公开基准 T2V-CompBench 上使用开源骨干模型（VideoCrafter2、CogVideoX-5B）进行评估，评估协议一致。LVD 因内存需求过大无法在 CogVideoX-5B 上运行，相关对比仅限于 VideoCrafter2。噪声反转比 α 的消融使用统一的背景生成器（FLUX + CogVideoX-5B），排除了背景质量差异的干扰。

### 补充图表

![[assets/figures/papers/paper_list_l42_https_arxiv_org_abs_2504_08641/figures/003_Table.jpg]]

![[assets/figures/papers/paper_list_l42_https_arxiv_org_abs_2504_08641/figures/004_Figure_3.jpg]]
*Figure 3: Videos generated with CogVideoX-5Band VIDEO-MSG with CogVideoX-5Bbackbone.The videos generated with VIDEO-MSG are more accurate regarding object motions, numeracy,and spatial relationships*

## 方法谱系与知识库定位

### 训练无关引导：推理时布局控制的范式转移

VIDEO-MSG 的核心定位是**训练无关（training-free）的布局引导方法**，与现有两大类 T2V 布局控制方案形成明确断层：

- **微调依赖方法**：如 **LVD** 等基于注意力操纵的方案，需要在去噪过程中迭代修改交叉/自注意力图以注入布局约束。这类方法不仅需要针对特定骨干模型进行适配，且在推理时引入额外内存开销——原文指出，LVD 在 A100 80GB GPU 上亦无法驱动 CogVideoX-5B，而 VIDEO-MSG 可在 A6000 48GB 上运行同一模型。这一对比直接锚定了 VIDEO-MSG 在**大规模 T2V 模型可扩展性**上的优势。

- **纯文本提示方法**：如 **VideoCrafter2** 和 **CogVideoX-5B**（Yang et al., arXiv 2024）的原生推理，仅依赖文本嵌入控制生成，缺乏对空间布局与物体轨迹的精确约束。VIDEO-MSG 在这些骨干模型上叠加后，Motion Binding 分别提升 0.1499 和 0.1544（Table 1），证明文本提示本身不足以传达细粒度时空规划信息。

VIDEO-MSG 的范式转移在于**将布局与运动先验编码为结构化初始噪声，而非在去噪过程中修改注意力图**。这一设计使其天然规避了注意力操纵带来的内存膨胀问题，同时保持了骨干模型的完整性——无需微调、无需访问内部注意力层，仅需访问潜空间和扩散调度器。

### 多模态规划管线的模块依赖与适用边界

VIDEO-MSG 的三阶段流水线（Figure 2）依赖多个外部模型协同工作，形成了明确的适用边界：

| 阶段 | 依赖模型 | 功能 | 失效风险 |
|------|----------|------|----------|
| 背景规划 | MLLM (GPT-4o) | 生成不含前景物体的背景描述 | MLLM 可能误解提示，将前景物体纳入背景 |
| 前景布局 | RAM + Grounding-DINO + GPT-4o | 检测背景物体位置，规划前景边界框序列 | 检测遗漏导致前景放置冲突（Figure 4） |
| 物体渲染 | T2I (FLUX) + SAM | 生成前景物体并分割 | 分割不完整导致融合不自然（Figure 5） |
| 视频生成 | T2V 骨干 + 噪声反转 | 从结构化初始噪声去噪生成视频 | α 选择不当导致控制力与平滑度失衡 |

消融实验（Sec 4.4, Figure 4, Figure 5）证实了感知模块的不可替代性：缺少 RAM/Grounding-DINO 的背景物体检测，GPT-4o 规划的前景边界框会与背景物体重叠；缺少 SAM 分割，直接合并的前景物体会携带原始背景像素，破坏视觉连贯性。

### 噪声反转比 α：控制-平滑权衡的核心旋钮

噪声反转比 α 是 VIDEO-MSG 最具辨识度的控制机制。其因果逻辑为：

$$t^{\mathrm{inv}} = \alpha \times T, \quad \alpha \in (0.0, 1.0)$$

- **较低 α**（如 0.5）：从较早时间步开始去噪，初始噪声中保留了更多 VIDEO SKETCH 的结构信息，布局控制力强（Motion 得分 0.3980），但运动平滑度下降至 98.58（Table 2）。
- **较高 α**（如 0.9）：初始噪声更接近纯随机噪声，运动平滑度最佳，但布局控制力弱。
- **LLM 动态推断 α**：根据文本描述的运动复杂度自动选择 α 范围（VideoCrafter2 用 [0.5, 0.8]，CogVideoX-5B 用 [0.7, 0.9]），在控制力与平滑度之间取得平衡（Table 2）。

这一机制的本质是将**布局约束强度**转化为**噪声注入程度**的可调参数，使 VIDEO-MSG 能够适应不同运动复杂度的生成任务。但当前 α 由 LLM 基于启发式提示选择，缺乏严格优化——这是方法的一个明确局限。

### 局限与开放问题

**已确认的局限**（原文明确讨论）：

1. **动态属性与交互类别的提升有限**：VIDEO-MSG 在 Dynamic-attr、Action、Interaction 类别上增益较小，因为边界框引导无法表达物体内部状态变化或多物体交互的动态语义。这指向了边界框引导的表示能力上限。

2. **多模型依赖的推理复杂度**：尽管单次推理内存占用低，但整个流水线涉及 MLLM 调用、检测、分割、T2I、I2V 等多个步骤，端到端延迟可能较高——原文未提供延迟数据，需要手动验证实际部署效率。

3. **α 选择的非最优性**：LLM 启发式推断缺乏理论保证，在特定文本上可能无法达到最佳平衡。

**开放问题**（原文未解决，指向未来工作）：

- 如何将边界框引导扩展至动态状态变换与物体交互，以提升 Action 和 Interaction 类别表现？这可能需要引入更丰富的运动表示（如光流、骨骼关键点）。
- 是否可以通过学习方式自动优化 α，而非依赖 LLM 启发式？例如训练一个小型预测网络，以文本特征为输入直接输出最优 α。
- VIDEO-MSG 的规划框架是否可适配其他视频生成任务（如摄像机控制、多物体复杂场景）？当前框架假设静态摄像机，背景生成器对此有偏好。
- 能否利用更轻量的感知模型替代 RAM/Grounding-DINO 以降低延迟，而不显著牺牲空间一致性？这是实际部署的关键瓶颈。
- 在闭源 T2V 模型（如 Gen-3）上应用该方法是否可行？因为需要访问潜空间和扩散调度器——这限制了 VIDEO-MSG 的模型适用范围。

### 知识库定位

VIDEO-MSG 在 T2V 生成控制的知识谱系中占据**训练无关、推理时布局引导**的节点，与以下方向形成互补或对比：

- **注意力操纵方法**（如 LVD）：同属推理时引导，但 VIDEO-MSG 通过噪声反转避免了注意力图迭代修改的内存开销。
- **微调方法**（如基于 ControlNet 的视频版）：VIDEO-MSG 无需训练数据，但控制精度可能低于微调方案。
- **多模态规划方法**：VIDEO-MSG 将 MLLM 的空间推理能力与视觉感知工具（RAM、Grounding-DINO）结合，形成“接地”（grounding）的规划范式——这与纯文本规划形成对比。

未来工作的核心挑战在于：如何在保持训练无关和内存高效的前提下，将控制表示从边界框扩展到更丰富的运动语义，并降低对重型感知模型的依赖。

## 原文 PDF

![[paperPDFs/arxiv_2025/Training_free_Guidance_in_Text_to_Video_Generation_via_Multimodal_Planning_and_Structured_Noise_Initialization.pdf]]