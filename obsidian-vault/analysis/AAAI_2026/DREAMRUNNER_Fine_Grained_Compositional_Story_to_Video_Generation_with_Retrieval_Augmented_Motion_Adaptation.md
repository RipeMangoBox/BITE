---
title: "DREAMRUNNER: Fine-Grained Compositional Story-to-Video Generation with Retrieval-Augmented Motion Adaptation"
type: paper
paper_level: A
venue: AAAI
year: 2026
pdf_ref: paperPDFs/AAAI_2026/DREAMRUNNER_Fine_Grained_Compositional_Story_to_Video_Generation_with_Retrieval_Augmented_Motion_Adaptation.pdf
aliases:
- DREAMRUNNER
tags:
- AAAI_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: "通过双级LLM规划将复杂场景分解为帧级实体布局，结合检索增强的测试时运动先验学习和空间-时间区域基3D注意力与LoRA注入（SR3AI），实现对每个区域的对象外观、运动轨迹和交互事件的精确绑定。"
primary_logic: "将故事转化为细粒度的帧级多实体布局方案，并利用外部检索视频学习目标运动先验，再通过区域掩码注意力将先验注入到对应区域，从而在保持全局时空连贯性的同时，实现对复杂组合与运动的解耦控制。"
claims:
- "在自建数据集DreamStorySet上，DREAMRUNNER的角色一致性（CLIP）较VLogger提升13.1%（70.7 vs 62.5），事件过渡平滑度提升27.2%（93.6 vs 73.6），文本对齐（ViCLIP）提升8.56%（24.1 vs 22.2）。"
- "在T2V-CompBench上，基于CogVideoX-2B的SR3AI在动态属性绑定上相对提升26.2%，空间绑定提升26.3%，运动绑定提升9.6%，证明其精细条件跟随能力。"
- "消融实验表明，同时启用RAG和SR3AI（全模型）在文本对齐和事件过渡上取得最佳结果；单独使用SR3AI可显著提升过渡平滑度，而RAG则进一步改善文本对齐。"
- "添加RAG和SR3AI不会损害基础模型的整体视觉质量，全模型在VBench六项指标上的平均值仍达82.55。"
---

# DREAMRUNNER: Fine-Grained Compositional Story-to-Video Generation with Retrieval-Augmented Motion Adaptation

> [!tip] 核心洞察
> 将故事转化为细粒度的帧级多实体布局方案，并利用外部检索视频学习目标运动先验，再通过区域掩码注意力将先验注入到对应区域，从而在保持全局时空连贯性的同时，实现对复杂组合与运动的解耦控制。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | DreamRunner：基于检索增强运动适应的细粒度组合式故事到视频生成 |
| 英文题名 | DREAMRUNNER: Fine-Grained Compositional Story-to-Video Generation with Retrieval-Augmented Motion Adaptation |
| 会议/期刊 | AAAI 2026 |
| Links | [paper](https://arxiv.org/abs/2411.16657); [Project](https://zunwang1.github.io/DreamRunner) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/image_and_video_generation |
| Method | DREAMRUNNER |
| Dataset | DreamStorySet (story-to-video generation), DreamStorySet, T2V-CompBench (compositional T2V), T2V-CompBench |

> [!tip] 效果简介
> - DreamStorySet (story-to-video generation) 上，Character consistency (CLIP) 为 70.7，对比 62.5 (VLogger)，变化 +13.1%。
> - DreamStorySet 上，Transition smoothness (DINO) 为 93.6，对比 73.6 (VLogger)，变化 +27.2%。
> - T2V-CompBench (compositional T2V) 上，Dynamic attribute binding (CogVideoX-2B + SR3A) 为 0.2672，对比 0.2118 (CogVideoX-2B)，变化 +26.2%。

## 概述

故事到视频生成（Story-to-Video Generation）的核心瓶颈在于：现有方法在利用LLM完成高层次场景规划后，直接将复杂的单场景文本描述输入T2V模型，缺乏对多对象、多动作与连续事件的精细空间-时间控制，导致生成视频普遍存在对象遗漏、动作模糊、角色不一致和场景过渡不自然等问题。

**DREAMRUNNER** 针对上述瓶颈提出了一个系统性的解决方案。其核心思想是：**将故事转化为细粒度的帧级多实体布局方案，并通过检索增强的测试时运动先验学习与区域掩码注意力机制，在保持全局时空连贯性的同时，实现对复杂组合与运动的解耦控制。**

方法上，DREAMRUNNER 包含三个关键环节：
1.  **双层视频计划生成**：利用LLM进行层级式规划，先粗粒度分解为多场景事件，再细粒度生成包含实体边界框与运动描述的帧级布局计划。
2.  **运动检索与先验学习**：通过自动检索管道从大规模视频数据库中获取运动参考视频，并利用测试时微调分别学习角色外观先验（空间LoRA）和运动动态先验（时间LoRA）。
3.  **空间-时间区域基3D注意力与先验注入（SR3AI）**：扩展基础T2V模型的全3D注意力机制，通过掩码使每个空间区域仅关注其对应的文本条件，同时将角色和运动LoRA精确注入到对应的布局区域，实现多角色、多运动的零样本绑定。

实验结果表明，DREAMRUNNER 在多个维度上取得了显著提升。在自建的故事视频生成评测集 DreamStorySet 上，相比基线方法 **VLogger**，角色一致性（CLIP）相对提升 **13.1%**（70.7 vs 62.5），事件过渡平滑度（DINO）提升 **27.2%**（93.6 vs 73.6），文本对齐分数（ViCLIP）提升 **8.56%**（24.1 vs 22.2）。在组合式文本到视频生成基准 T2V-CompBench 上，基于 **CogVideoX-2B** 的 SR3AI 模块在动态属性绑定上相对提升 **26.2%**，空间关系绑定提升 **26.3%**，运动绑定提升 **9.6%**。消融实验进一步证实，RAG 与 SR3AI 的组合使用对文本遵循能力和事件过渡平滑度的贡献最大，且这些增强模块不会损害基础模型的整体视觉质量。

在方法谱系与知识库定位上，DREAMRUNNER 可视为对“LLM规划 + T2V生成”范式的一次深度改造。它借鉴了 **VideoDirectorGPT**（Lin et al., 2023）的LLM规划思路，但将规划粒度从场景级深化至帧级实体布局；它吸收了 **VLogger**（Zhuang et al., 2024）的角色定制思想，但通过区域基LoRA注入实现了更精准的多角色隔离；它以全3D注意力的 **CogVideoX-2B/5B**（Yang et al., 2024c）为基座，通过掩码注意力机制将其改造为支持区域条件化的生成器，从而在开源模型上实现了接近闭源模型的精细组合控制能力。

## 背景与动机

故事到视频生成（Story-to-Video Generation）旨在将一段叙述性文本转化为视觉连贯、事件丰富的长视频。与常规的文本到视频（T2V）生成不同，该任务要求模型同时处理多角色外观一致性、跨场景的事件过渡、以及细粒度的对象-动作绑定，其核心挑战在于对复杂组合语义的精确时空控制。

现有方法通常采用“先规划后生成”的范式：先用大语言模型（LLM）将故事分解为场景级描述，再将每个场景的文本条件直接送入T2V扩散模型进行生成。然而，这种粗粒度的文本条件缺乏对多对象、多动作、连续事件的空间-时间精细约束，导致生成视频普遍存在**对象遗漏、动作模糊、角色不一致和过渡不自然**等问题。以代表性工作 **VideoDirectorGPT**（Lin et al., 2023）和 **VLogger**（Zhuang et al., 2024）为例，前者虽引入了LLM规划与空间控制，但未解决运动先验缺失的问题；后者虽支持角色定制，却难以在单场景内协调多个实体的独立运动与交互。

上述瓶颈的根源在于：复杂场景的语义被压缩为单一的文本嵌入，模型无法在生成过程中区分不同区域的条件信号。换言之，**缺乏一种将高层故事规划解耦为帧级实体布局，并将布局信息精确注入扩散生成过程的机制**。

DREAMRUNNER 的动机正是填补这一空白。其核心思路是：将故事转化为细粒度的帧级多实体布局方案，通过检索增强从外部视频中学习目标运动先验，再利用区域掩码注意力将外观与运动先验分别注入到对应的时空区域，从而在保持全局连贯性的同时，实现对复杂组合与运动的解耦控制。

## 核心创新

DREAMRUNNER 的核心创新在于将故事视频生成从“单阶段文本条件注入”重构为“规划-检索-区域注入”三阶段解耦范式，从根本上解决了现有方法在复杂场景下对象遗漏、动作模糊和过渡不自然的问题。其关键创新点体现在以下四个维度的设计转变：

### 1. 规划粒度：从场景级描述到帧级实体布局

现有方法（如 **VideoDirectorGPT** (Lin et al., 2023)、**VLogger** (Zhuang et al., 2024)）仅使用 LLM 生成场景级描述，直接将其作为 T2V 模型的文本条件。这种粗粒度方式将多对象、多动作、连续事件的复杂语义压缩为单一文本嵌入，导致模型在注意力分配上缺乏空间-时间约束。

DREAMRUNNER 提出**双层层级规划**（Section 3.1）：首先由 GPT-4o 生成故事级粗粒度场景描述，随后将其细化为帧级实体布局方案，包括每个实体的归一化边界框和运动描述。这一转变将“模型自行理解复杂场景”变为“模型接收精确的空间-时间指令”，使对象-动作绑定从隐式学习转变为显式约束。

### 2. 运动合成：从无先验生成到检索增强测试时微调

基线方法缺乏显式运动先验——VLogger 的角色定制通过全局 LoRA 或参考图像嵌入实现，VideoDirectorGPT 则完全依赖 T2V 模型的生成先验。这使得模型在面对特定运动模式（如“松鼠收集坚果”）时难以保持动作的准确性和时序连贯性。

DREAMRUNNER 引入**检索增强测试时运动先验学习**（Section 3.2）：通过 BM25 检索→属性过滤→YOLOv5 目标跟踪裁剪→CLIP/ViCLIP 排序的自动管道，从大规模视频数据库中获取运动参考视频。随后在测试时微调阶段，使用外观去偏时间损失 $L_{ad}$ 训练时间层运动 LoRA，解耦动作与外观，使模型专注于学习运动动态。同时，主体先验通过空间层 LoRA 从角色参考图像中独立学习。这种“运动-外观分离学习”的设计是运动质量提升的关键因果机制。

### 3. 注意力机制：从全 3D 自注意力到空间-时间区域基 3D 注意力（SR3AI）

CogVideoX 的全 3D 自注意力（所有视觉潜变量和文本条件统一参与注意力计算）在单对象场景中表现良好，但在多对象多动作场景中缺乏对注意力流的约束，导致对象间特征干扰和动作混淆。

DREAMRUNNER 提出的 **SR3AI**（Section 3.3）通过掩码机制将注意力分解为区域基组件：每个区域仅关注其对应的文本条件，同时允许跨区域的视觉潜变量交互。这一设计实现了“分而治之”——模型无需同时处理所有对象的复杂语义，而是在保持全局时空连贯性的前提下，对每个区域进行精确的条件化控制。消融实验（Table 3）证实，仅启用 SR3AI（无 RAG）就能显著提升单场景内的事件过渡平滑度，验证了区域分解的有效性。

### 4. LoRA 注入方式：从全局 LoRA 到区域基多 LoRA 注入

基线方法的全局 LoRA 对全图特征进行统一修改，无法区分不同角色的外观或不同区域的运动模式。DREAMRUNNER 的**区域基 LoRA 注入**（Section 3.3, Appendix A.3）根据帧级布局掩码，将不同角色的空间 LoRA 和不同运动的时间 LoRA 仅应用到对应的潜变量区域：

$$Wx = W_0 x + A_{\text{witch}} B_{\text{witch}} (\text{Mask}_{\text{witch}} \cdot x) + A_{\text{cat}} B_{\text{cat}} (\text{Mask}_{\text{cat}} \cdot x)$$

这种设计实现了多角色多运动的零样本隔离注入，避免了全局 LoRA 导致的特征污染。消融实验（Table 6）进一步表明，交错注入空间和时间 LoRA 的策略优于“半层空间、半层时间”的注入方式，且在外观去偏训练下性能最佳。

### 创新总结

上述四个 changed slot 构成了一个完整的因果链：精细的帧级布局计划为区域注入提供了空间锚点，检索增强的运动先验为时间 LoRA 提供了高质量的学习目标，SR3AI 的掩码注意力确保了条件化的精确性，而区域基 LoRA 注入则实现了多角色多运动的无干扰隔离。这一设计使得 DREAMRUNNER 在 DreamStorySet 上较 VLogger 实现角色一致性提升 13.1%、事件过渡平滑度提升 27.2%（Table 1），并在 T2V-CompBench 上显著增强了开源模型的组合式生成能力（Table 2）。

## 整体框架

DREAMRUNNER 的核心设计思路是将复杂的叙事性故事转化为可精细控制的视频生成过程。其整体管道由三个紧密协作的阶段构成，形成“高层规划→先验获取→区域化注入”的闭环。

**输入**：用户提供的通用故事叙述文本。

**第一阶段：双层视频计划生成（Dual-Level Video Plan Generation）**。系统首先调用 GPT-4o 对故事进行层级化分解：先生成粗粒度的高层计划，将故事切分为多个场景，并为每个场景生成包含角色驱动、动作丰富的事件描述；继而，针对每个场景，进一步生成细粒度的帧级实体布局计划，明确指定背景、各实体的运动描述及其归一化边界框。这一阶段将模糊的故事文本转化为结构化的空间-时间控制信号。

**第二阶段：运动检索与先验学习（Motion Retrieval and Subject/Motion Prior Learning）**。该阶段并行处理两类先验：
- **运动先验**：通过自动检索管道（BM25→属性过滤→YOLOv5目标跟踪裁剪→CLIP/ViCLIP排序），从大规模视频数据库中获取与计划中运动描述对齐的参考视频，并利用测试时微调在时间层 LoRA 中学习运动模式。
- **主体先验**：从角色参考图像出发，利用定制化技术在空间层 LoRA 中学习角色外观表征。

**第三阶段：空间-时间区域基3D注意力与先验注入（SR3AI）**。这是将计划与先验“缝合”进生成过程的关键模块。它在 CogVideoX 的全 3D 自注意力基础上引入区域掩码机制，使每个空间-时间区域仅关注其对应的文本条件，同时保持跨区域视觉潜变量的交互。角色和运动 LoRA 则根据帧级布局掩码，以区域基方式注入到对应潜变量区域，实现多角色、多运动的精确绑定与无干扰组合。

**输出**：具有细粒度对象-运动绑定、角色一致性和事件过渡平滑性的故事视频。

三个阶段的因果逻辑清晰：第一阶段提供“做什么”的细粒度蓝图，第二阶段提供“怎么做”的外观和运动先验知识，第三阶段则通过区域化解耦的注意力与注入机制，确保蓝图与先验在生成过程中被精确执行。

## 核心模块与公式推导

DREAMRUNNER 由三个关键模块构成：双层视频计划生成、运动检索与先验学习、以及空间-时间区域基 3D 注意力与先验注入（SR3AI）。以下逐一展开其核心机制与关键公式。

### 双层视频计划生成

该模块使用 GPT-4o 将用户提供的通用故事叙述转化为层级式的细粒度视频计划。首先，LLM 生成跨场景的高层计划，包含角色驱动、运动丰富的事件描述；随后，将每个场景描述进一步分解为帧级的实体布局方案，明确指定每个实体在各帧中的归一化边界框（bounding box）和运动描述。这一分解将复杂的多对象、多动作场景转化为结构化的空间-时间控制信号，为后续的区域基条件生成提供精确的布局先验。

### 运动检索与先验学习

为弥补基础 T2V 模型对特定运动模式建模能力的不足，DREAMRUNNER 引入检索增强的测试时运动先验学习。检索管道流程为：BM25 稀疏检索 → 属性过滤 → YOLOv5 目标跟踪裁剪 → CLIP/ViCLIP 重排序，从大规模视频数据库（如 WebVid-10M）中自动筛选与 LLM 计划对齐的运动参考视频。

在获得检索视频后，分别训练两类 LoRA 先验：
- **主体先验**：从角色参考图像中学习，注入到扩散模型的空间层（spatial LoRA），用于绑定角色外观。
- **运动先验**：从检索视频中学习，注入到时间层（temporal LoRA），用于捕捉运动动态。

运动先验的训练采用标准扩散损失，并引入外观去偏机制以解耦运动与外观：

**标准扩散损失**（用于保留生成能力）：
$$L_{org} = \mathbb{E}_{z_0, y, \epsilon \sim \mathcal{N}(0,1), t \sim \mathcal{U}(0,T)} \left[ \| \epsilon - \epsilon_\theta(z_t, t, y) \|_2 \right]$$

其中 $z_0$ 为视频潜变量，$y$ 为文本条件，$\epsilon$ 为高斯噪声，$\epsilon_\theta$ 为扩散模型预测的噪声，$t$ 为时间步。

**外观去偏归一化**（以锚帧噪声为参考，减去外观成分）：
$$\phi(\epsilon) = \sqrt{\beta^2 + 1} \, \epsilon - \beta \, \epsilon_{anchor}$$

**外观去偏时间损失**（在归一化噪声空间上计算，强制模型学习与外观无关的运动动态）：
$$L_{ad} = \mathbb{E}_{z_0, y, \epsilon \sim \mathcal{N}(0,1), t \sim \mathcal{U}(0,T)} \left[ \| \phi(\epsilon) - \phi(\epsilon_\theta(z_t, t, y)) \|_2 \right]$$

### 空间-时间区域基 3D 注意力与先验注入（SR3AI）

SR3AI 是 DREAMRUNNER 的核心创新，它扩展了 CogVideoX 的全 3D 自注意力机制，通过掩码实现区域条件化，同时以区域基方式注入主体和运动 LoRA。

**区域基 3D 注意力**：在标准全 3D 注意力中，所有视觉潜变量与文本条件统一参与注意力计算。SR3AI 根据帧级布局计划生成空间-时间掩码，使每个区域仅关注其对应的文本描述，同时允许未掩码的视觉潜变量之间进行跨区域交互。这一“分而治之”的设计确保每个实体与其运动/外观条件精确对齐，同时保持全局时空连贯性。

**区域基 LoRA 注入**：标准 LoRA 对全图特征进行统一修改，无法处理多角色场景。DREAMRUNNER 采用区域基注入策略，将不同角色的 LoRA 仅应用到其对应的掩码潜变量区域。LoRA 权重更新遵循低秩分解：
$$W = W_0 + \Delta W = W_0 + BA$$
其中 $W_0$ 为冻结的预训练权重，$A$ 和 $B$ 为可训练的低秩矩阵。

对于多角色场景，区域基注入公式为：
$$Wx = W_0 x + A_{witch} B_{witch} (Mask_{witch} \cdot x) + A_{cat} B_{cat} (Mask_{cat} \cdot x)$$

该公式确保女巫（witch）和猫（cat）的 LoRA 仅作用于各自的空间-时间掩码区域，实现无干扰的多角色外观与运动绑定。

## 实验与分析

### 核心定量结果

**故事到视频生成（DreamStorySet）**。Table 1 报告了在自建数据集 DreamStorySet 上与 **VideoDirectorGPT** (Lin et al., 2023) 和 **VLogger** (Zhuang et al., 2024) 的全面对比。DREAMRUNNER 在角色一致性上取得 70.7 的 CLIP 分数，相较 VLogger 的 62.5 提升 13.1%；DINO 分数提升 33.4%，验证了主体先验学习与区域基 LoRA 注入对角色保真度的关键作用。事件过渡平滑度（DINO-based transition score）达 93.6，较 VLogger 的 73.6 提升 27.2%，表明 SR3AI 的区域分解注意力机制有效缓解了多事件场景的突变与不连贯。文本对齐方面，细粒度指令跟随（CLIP）和全提示对齐（ViCLIP）分别达到 24.1 和 22.2，相对 VLogger 提升 8.56%，证明检索增强运动先验对复杂语义的精细绑定能力。

**组合式文本到视频生成（T2V-CompBench）**。Table 2 展示了在组合式基准上的泛化能力。基于 **CogVideoX-2B** (Yang et al., 2024c) 的 SR3A（无 LoRA 注入，仅使用布局计划与区域注意力）在动态属性绑定上取得 0.2672，相对基线 0.2118 提升 26.2%；空间关系从 0.2192 提升至 0.2768（+26.3%）；运动绑定从 0.1893 提升至 0.2076（+9.6%）。在更大规模的 **CogVideoX-5B** 上，SR3A 同样带来显著增益：动态属性绑定提升 25.9%，空间关系提升 17.5%。这一结果说明 SR3AI 的区域条件化机制具有模型规模无关的鲁棒性，能有效缩小开源模型与闭源模型在组合式生成上的差距。

### 消融实验

**核心组件贡献**。Table 3 系统消融了 RAG（检索增强运动先验学习）与 SR3AI 的独立和联合效果。仅使用 SR3AI（无 RAG）即能显著提升单场景内的事件过渡平滑度，因为将全注意力分解为区域基注意力使模型能对各实体“分而治之”，减少跨对象特征干扰。在此基础上加入 RAG 后，细粒度和全提示的文本对齐分数进一步提升，表明检索到的运动参考视频为模型提供了更丰富的时序动态先验，弥补了纯文本条件在运动描述上的信息瓶颈。全模型（RAG + SR3AI）在文本遵循能力与事件过渡平滑度上均取得最优，证实两者存在协同增益。

**运动先验学习设计选择**。Table 4 对比了检索增强测试时微调中提示策略的影响：为每个检索视频使用独立的描述性提示（per-video prompt）在 CLIP 和 ViCLIP 上均优于共享单提示（CLIP 24.67 vs 24.01，ViCLIP 23.04 vs 22.02），说明个性化提示能更精准地引导模型从异构参考视频中提取目标运动模式。Table 5 进一步消融了检索管道各组件（BM25 初筛、属性过滤、YOLOv5 跟踪裁剪、CLIP/ViCLIP 重排序）的贡献，验证了多阶段筛选对先验质量的正向影响。

**LoRA 注入策略**。Table 6 探索了空间 LoRA（主体先验）与时间 LoRA（运动先验）的注入方式。交错注入（interleaved injection）策略优于“半层空间、半层时间”的分配方式，且在外观去偏训练（appearance-debiased training）下性能最佳。外观去偏通过减去锚帧噪声来解耦动作与外观，使时间 LoRA 专注于学习运动动态而非静态纹理，从而在保持角色一致性的同时提升运动自然度。

**视觉质量保持**。Table 8 报告了 VBench 六项质量指标的消融结果。添加 RAG 和 SR3AI 不会损害基础模型的整体视觉质量，全模型在美学、成像质量、运动平滑度、时序稳定性、主体/背景一致性上的均值仍达 82.55。这消除了对额外模块引入质量退化的顾虑——DREAMRUNNER 的增益来自更精细的条件控制，而非牺牲生成质量。

### 定性分析与失败模式

Figure 4 展示了多角色与单角色场景下的定性对比。在多角色示例中，DREAMRUNNER 通过区域 LoRA 注入实现了不同角色的外观隔离，避免了全局 LoRA 方法中常见的身份混淆；在单角色示例中，SR3AI 的区域注意力使运动与背景的交互更自然，而硬区域注意力（hard regional attention）则因完全阻断跨区域视觉信息流导致画面割裂。

**已知失败模式**：① 当帧级布局计划中实体边界框重叠严重时，区域掩码难以精确划分潜变量归属，多角色协调可能出现身份混淆——当前未探索如 CLoRA 等高级 LoRA 合并技术；② 运动检索管道依赖预收集的视频数据库，对虚构或极端罕见运动类型可能无法检索到高质量参考，此时运动先验学习的有效性下降；③ 基础模型（CogVideoX）对高度复杂或未见过的组合场景存在建模上限，DREAMRUNNER 无法超越这一瓶颈，极端组合下仍可能出现画面瑕疵。

### 公平性说明

为公平对比故事到视频生成方法，将每个场景叙述拆分为两个单运动描述分别生成后合并为同一场景视频；所有方法采用统一的 CLIP/DINO/ViCLIP 语义对齐指标与 VBench 视觉质量指标。测试时微调每先验约需 5 分钟（单张 A6000 GPU），推理时不增加额外模块参数——仅注入 LoRA 权重并修改注意力掩码。

### 补充图表

![[assets/figures/papers/paper_list_l14_DREAMRUNNER_Fine_Grained_Compositional_Story_to_Video_Generation_with_Re/figures/007_Figure.jpg]]

![[assets/figures/papers/paper_list_l14_DREAMRUNNER_Fine_Grained_Compositional_Story_to_Video_Generation_with_Re/figures/014_Figure_6.jpg]]
*Figure 6: A squirrel gathers nuts and a bat hangs from a tree branch A kid and a penguin watch a movie in the cinema Figure 6: Qualitative results of DREAMRUNNER generated with prompts characterizing action binding. SR3A denotes our spatial-temporal region-based attention module*

![[assets/figures/papers/paper_list_l14_DREAMRUNNER_Fine_Grained_Compositional_Story_to_Video_Generation_with_Re/figures/015_Figure_7.jpg]]
*Figure 7: White tractor plowing near a green farmhouse Big hearts and small stars floating upwards Figure 7: Qualitative results of DREAMRUNNER generated with prompts characterizing consistent attribute binding. SR3A denotes our spatial-temporal region-based attention module*

![[assets/figures/papers/paper_list_l14_DREAMRUNNER_Fine_Grained_Compositional_Story_to_Video_Generation_with_Re/figures/016_Figure_8.jpg]]
*Figure 8: A timelapse of a flower bud blooming into a full flower Clear blue sky turns stormy gray Figure 8: Qualitative results of DREAMRUNNER generated with prompts characterizing dynamic attribute binding. SR3A denotes our spatial-temporal region-based attention module*

![[assets/figures/papers/paper_list_l14_DREAMRUNNER_Fine_Grained_Compositional_Story_to_Video_Generation_with_Re/figures/017_Figure_9.jpg]]
*Figure 9: Qualitative results of DREAMRUNNER generated with prompts characterizing motion binding. SR3A denotes our spatial-temporal region-based attention module*

![[assets/figures/papers/paper_list_l14_DREAMRUNNER_Fine_Grained_Compositional_Story_to_Video_Generation_with_Re/figures/018_Figure_10.jpg]]
*Figure 10: Coach motivates athlete during a tough workout Tiger coach whistles at soccer practice Figure 10: Qualitative results of DREAMRUNNER generated with prompts characterizing object interactions. SR3A denotes our spatial-temporal region-based attention module*

![[assets/figures/papers/paper_list_l14_DREAMRUNNER_Fine_Grained_Compositional_Story_to_Video_Generation_with_Re/figures/019_Figure_11.jpg]]
*Figure 11: Qualitative results of DREAMRUNNER generated with prompts characterizing spatial relationships. SR3A denotes our spatial-temporal region-based attention module*

![[assets/figures/papers/paper_list_l14_DREAMRUNNER_Fine_Grained_Compositional_Story_to_Video_Generation_with_Re/figures/020_Figure.jpg]]

![[assets/figures/papers/paper_list_l14_DREAMRUNNER_Fine_Grained_Compositional_Story_to_Video_Generation_with_Re/figures/021_Figure.jpg]]

![[assets/figures/papers/paper_list_l14_DREAMRUNNER_Fine_Grained_Compositional_Story_to_Video_Generation_with_Re/figures/022_Figure.jpg]]

![[assets/figures/papers/paper_list_l14_DREAMRUNNER_Fine_Grained_Compositional_Story_to_Video_Generation_with_Re/figures/023_Figure.jpg]]

![[assets/figures/papers/paper_list_l14_DREAMRUNNER_Fine_Grained_Compositional_Story_to_Video_Generation_with_Re/figures/024_Figure.jpg]]


## 方法谱系与知识库定位

### 基线关系与谱系定位

DREAMRUNNER 处于**故事到视频生成（Story-to-Video Generation, SVG）**与**组合式文本到视频生成（Compositional T2V）**的交汇点，其直接对话的基线包括两类：

**故事级基线：** **VideoDirectorGPT**（Lin et al., 2023）和 **VLogger**（Zhuang et al., 2024）代表了现有的 SVG 方案。VideoDirectorGPT 使用 LLM 进行场景级规划并辅以空间控制，但缺乏对帧级多实体运动的精细分解。VLogger 引入了角色定制能力，却仍将复杂场景描述作为单一文本条件直接输入 T2V 模型，导致对象遗漏、动作模糊和过渡不自然。DREAMRUNNER 的核心改进在于将规划粒度从“场景级描述”下沉到“帧级实体布局”，并通过检索增强的运动先验学习和区域基注意力注入，实现了对多对象、多动作的解耦控制。定量上，在 DreamStorySet 上角色一致性（CLIP）较 VLogger 提升 13.1%（70.7 vs 62.5），事件过渡平滑度（DINO）提升 27.2%（93.6 vs 73.6）（Table 1）。

**组合式 T2V 基线：** DREAMRUNNER 的 SR3AI 模块以 **CogVideoX-2B** 和 **CogVideoX-5B**（Yang et al., 2024c）为基础骨干进行扩展。CogVideoX 采用全 3D 自注意力，所有视觉潜变量与文本条件统一交互，缺乏对特定区域的条件化控制。SR3AI 通过掩码将全注意力改造为空间-时间区域基 3D 注意力，使每个区域仅关注其对应文本条件，同时保持跨区域视觉交互。在 T2V-CompBench 上，基于 CogVideoX-2B 的 SR3A 在动态属性绑定上相对提升 26.2%，空间绑定提升 26.3%，运动绑定提升 9.6%（Table 2），显著缩小了开源模型与闭源模型在组合式生成上的差距。

### 适用边界

DREAMRUNNER 的适用性受以下条件约束：

1. **基础模型能力上限：** 框架构建于扩散式 T2V 模型之上，对罕见组合和高度复杂动作的建模能力受限于骨干网络。当故事涉及极端未见组合时，即使有布局计划和运动先验，仍可能出现画面瑕疵。

2. **运动检索覆盖范围：** 检索增强的运动先验学习依赖预先收集的大规模视频数据库。对于细粒度或虚构的运动类型（如“龙喷火的同时扇动翅膀”），检索管道可能无法找到高质量参考视频，从而削弱运动先验的有效性。

3. **布局精度依赖：** 区域基 LoRA 注入依赖 LLM 生成的帧级布局计划（包括归一化边界框）。当布局预测偏差较大或存在大量重叠区域时，多角色协调可能出现身份混淆。论文明确指出，目前尚未探索高级 LoRA 合并技术（如 CLoRA）来处理重叠区域的细粒度交互。

4. **计算时效性：** 测试时微调每个运动先验约需 5 分钟（单张 A6000 GPU），对每个新故事都需要单独训练，不适合实时生成场景。

### 关键局限

- **罕见组合的鲁棒性不足：** 基础模型对极端组合的建模瓶颈未被根本解决，DREAMRUNNER 的分解-注入策略虽能缓解但无法消除这一问题。
- **重叠区域的身份混淆：** 当多个角色或实体的布局区域高度重叠时，基于掩码的区域 LoRA 注入可能出现特征干扰，导致角色外观或动作串扰。
- **运动检索的封闭性：** 检索管道的质量上限受限于视频数据库的规模和标注质量，对开放域、未标注视频源的利用能力有限。
- **测试时微调的开销：** 虽然每先验 5 分钟的训练成本可控，但无法满足需要即时生成的交互式应用。

### 开放问题

1. **基础模型上限提升：** 如何进一步提升骨干 T2V 模型对罕见组合和复杂动作的表现上限，使 DREAMRUNNER 在更广泛的故事类型中保持鲁棒性？

2. **重叠区域的多角色协调：** 能否利用先进的 LoRA 合并或条件分离技术（如 CLoRA）处理重叠区域的细粒度多角色交互，避免特征干扰和身份混淆？

3. **运动检索的开放域扩展：** 运动检索管道能否扩展到更大规模、开放域的未标注视频源，并通过无监督或自监督方式学习更通用的运动表示？

4. **消除测试时微调：** 是否有方法减少或消除测试时微调的计算开销，例如通过离线大规模预训练通用运动适配器，使其能在推理时零样本注入？

## 原文 PDF

![[paperPDFs/AAAI_2026/DREAMRUNNER_Fine_Grained_Compositional_Story_to_Video_Generation_with_Retrieval_Augmented_Motion_Adaptation.pdf]]
