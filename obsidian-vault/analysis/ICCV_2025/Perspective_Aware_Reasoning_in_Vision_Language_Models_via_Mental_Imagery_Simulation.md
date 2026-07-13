---
title: "Perspective-Aware Reasoning in Vision-Language Models via Mental Imagery Simulation"
type: paper
paper_level: A
venue: ICCV
year: 2025
pdf_ref: paperPDFs/ICCV_2025/Perspective_Aware_Reasoning_in_Vision_Language_Models_via_Mental_Imagery_Simulation.pdf
project_link: https://apc-vlm.github.io/
code_link: null
aliases:
- APCA
- PARVLMMIS
tags:
- ICCV_2025
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/vision_models_multimodal
core_operator: "通过模拟心理意象(Mental Imagery)构建场景的3D抽象表示，并将分配中心(allocentric)问题转换为自我中心(egocentric)问题，从而绕过VLM的视角局限性。"
primary_logic: "利用视觉基础模型提取物体位置和方向，构建场景抽象，并通过坐标变换实现视角转换，使VLM无需真正生成新视角即可利用其固有的自我中心推理能力。"
claims:
- "APC框架通过场景抽象、视角变换和提示生成三个阶段，显著提升了VLMs的视角感知推理能力。"
- "在COMFORT++基准的left/right任务上，APC-Vis达到89.67%准确率，远超最佳基线LLaVA-OneVision的55.33%。"
- "APC在不同视角偏移下保持高精度，而基线模型在allocentric角度性能急剧下降。"
- "与密集重建基线相比，APC在推理时间上加速超过14倍（17.47s vs >260s），同时精度更高。"
---

# Perspective-Aware Reasoning in Vision-Language Models via Mental Imagery Simulation

> [!tip] 核心洞察
> 利用视觉基础模型提取物体位置和方向，构建场景抽象，并通过坐标变换实现视角转换，使VLM无需真正生成新视角即可利用其固有的自我中心推理能力。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 基于心理意象模拟的视觉语言模型视角感知推理 |
| 英文题名 | Perspective-Aware Reasoning in Vision-Language Models via Mental Imagery Simulation |
| 会议/期刊 | ICCV 2025 |
| Links | [paper](https://arxiv.org/abs/2504.17207) · [Project](https://apc-vlm.github.io/) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/vision_models_multimodal |
| Method | Abstract Perspective Change (APC) |
| Dataset | COMFORT++ left/right, COMFORT++ closer, COMFORT++ visibility, COMFORT++ facing |

> [!tip] 效果简介
> - COMFORT++ left/right 上，Accuracy (%) 为 89.67 (APC-Vis)，对比 55.33 (LLaVA-OneVision)，变化 +34.34。
> - COMFORT++ closer 上，Accuracy (%) 为 96.00 (APC-Num)，对比 79.00 (LLaVA-OneVision/Cambrian-1)，变化 +17.00。
> - COMFORT++ visibility 上，Accuracy (%) 为 90.00 (APC-Vis)，对比 50.00 (Random)，变化 +40.00。

## 概要

### 问题瓶颈

现有视觉语言模型（VLM）在空间推理任务中表现出强烈的**自我中心偏差**——当问题以相机视角（egocentric）提出时表现良好，但一旦切换至分配中心视角（allocentric），即要求从场景中其他物体的参照系进行推理时，准确率急剧下降。这一偏差在左右关系判断、物体可见性、朝向识别等任务中尤为突出，成为VLM在具身智能、机器人导航等应用中的关键瓶颈。

### 核心方法

本文提出**抽象视角转换框架（Abstract Perspective Change，APC）**，受人类心理意象模拟机制启发，通过三个关键阶段实现分配中心到自我中心的视角转换：

1. **场景抽象**：利用视觉基础模型（GroundingDINO、SAM、DepthPro、OrientAnything）从输入图像中提取感兴趣物体的3D位置和朝向，构建粗粒度的场景抽象表示 $S_E := \{ O_i \}_{i=1}^n$，其中每个物体表示为元组 $(t_i, c_i, p_i)$（描述、3D位置、朝向）。
2. **视角变换**：由VLM识别问题中的参考视角，将场景抽象从相机坐标系变换至参考物体的自我中心坐标系，使参考物体位于原点、朝向对齐z轴。
3. **视角提示生成**：将变换后的场景抽象以数值提示（文本化3D坐标）或视觉提示（渲染彩色立方体）的形式传递给VLM，配合视角无关的问题重述，使VLM在无需真正生成新视角图像的情况下完成分配中心推理。

这一设计的核心洞察在于：**通过坐标变换将分配中心问题转化为VLM擅长的自我中心问题，而非试图让VLM直接理解非相机视角**。

### 主要结果

APC在多个空间推理基准上取得了显著提升：

- **COMFORT++基准**：在left/right任务上，APC-Vis达到89.67%准确率，远超最佳纯VLM基线LLaVA-OneVision的55.33%（+34.34%）；在closer、visibility、facing任务上分别达到96.00%、90.00%、88.33%，均大幅领先所有基线。
- **3DSRBench基准**：在facing和visibility任务上分别达到66.47%和67.44%，较随机基线提升超过17个百分点。
- **视角鲁棒性**：在不同视角偏移角度下，APC保持稳定高准确率，而基线模型在allocentric角度性能显著退化。
- **推理效率**：与密集重建基线相比，APC推理时间仅需17.47秒，加速超过14倍（SpatialPIN*需336秒，ViewCrafter需261秒），且精度更高。

### 方法定位

APC属于**视觉基础模型增强的VLM推理框架**，区别于纯VLM（如LLaVA-OneVision、GPT-4o、Qwen2.5-VL）、空间调优VLM（如SpatialVLM、SpatialRGPT）和密集重建方法（如ViewCrafter）。其关键创新在于以轻量级场景抽象替代密集重建，以坐标变换替代新视图合成，在精度和效率之间取得了有利的折衷。

### 视觉语言模型的空间推理偏差

视觉语言模型（VLMs）在图像理解、视觉问答等任务中展现出强大能力，但在进行空间推理时存在一个根本性局限：**自我中心偏差（egocentric bias）**。如 Figure 2 所示，当问题从相机视角（egocentric perspective）提出时，现有 VLM 能够较好地完成推理；但一旦同一问题被转换为以场景中其他物体为参照的分配中心视角（allocentric perspective），模型性能便急剧下降。这种偏差意味着 VLM 难以“设身处地”从非相机视角理解空间关系，严重制约了其在具身智能、人机交互等需要灵活视角推理的场景中的应用。

### 现有方法的缺口

当前应对空间推理任务的方法大致可分为三类：
- **纯视觉语言模型**（如 LLaVA-OneVision、GPT-4o、Qwen2.5-VL 等）直接处理原始 RGB 图像与问题，由于缺乏显式的视角转换机制，在面对分配中心问题时表现不佳。
- **面向空间推理调优的 VLM**（如 SpatialVLM、SpatialRGPT）通过特定训练数据增强空间能力，但未能从根本上解决视角泛化问题。
- **基于视觉基础模型的系统**（如 SpatialPIN）和**密集重建方法**（如 ViewCrafter）尝试通过 3D 重建或新视图合成来提供多视角信息，但这些方法计算开销极大（单次推理超过 260 秒，见 Table 2），且合成视图常包含噪声和失真（Figure 9），反而降低了推理精度。

上述方法的共同缺口在于：**缺乏一种轻量、高效的机制，使 VLM 能够在不真正生成新视角图像的前提下，完成从分配中心到自我中心的视角转换**。

### 核心动机：模拟心理意象

本文的动机源自人类认知中的**心理意象（mental imagery）**能力——人类能够在脑海中构建场景的抽象空间表征，并据此从不同视角进行推理，而无需实际移动或生成新的视网膜图像。如 Figure 3 所示，APC 框架借鉴这一认知机制，通过以下核心思路绕过 VLM 的视角局限：

> 利用视觉基础模型提取场景中物体的 3D 位置与朝向，构建场景的**粗粒度抽象表示**；通过坐标变换将分配中心问题转换为自我中心问题，使 VLM 得以复用其固有的自我中心推理能力。

这一思路的关键洞见在于：**VLM 并非缺乏空间推理能力，而是缺乏将问题转换到其擅长视角的手段**。APC 通过“场景抽象—视角变换—提示生成”三阶段流水线（Figure 4），在不修改 VLM 本身的前提下，显著提升了视角感知推理能力。

## 核心方法与创新机理

APC框架的核心创新在于**绕过VLM的自我中心偏差**，而非试图消除它。现有VLM在空间推理中表现出强烈的自我中心偏差（egocentric bias）——当问题从相机视角提出时表现良好，但一旦要求从场景中其他物体的视角（allocentric perspective）进行推理，准确率便急剧下降（Figure 2）。APC的策略是**将分配中心问题转化为自我中心问题**：通过构建场景的3D抽象表示，执行坐标变换，使VLM始终在其擅长的自我中心坐标系下进行推理。

这一策略通过以下三个关键设计实现：

### 1. 场景抽象替代密集重建

与基于新视图合成（如**SpatialPIN***、**ViewCrafter**）的密集重建基线不同，APC仅提取物体的**3D位置**和**朝向**，构建轻量级场景抽象 $S_E := \{ O_i \}_{i=1}^n$，其中每个物体 $O_i$ 表示为元组 $(t_i, c_i, p_i)$（文本描述、3D坐标、朝向）。这种粗粒度抽象避免了密集重建中的几何失真和语义丢失问题（Figure 9），同时将推理时间从超过260秒缩短至17.47秒，加速超过14倍（Table 2）。

### 2. 分配中心到自我中心的坐标变换

APC通过VLM识别问题中的参考视角（reference viewer），将场景抽象从相机坐标系变换到参考视角的自我中心坐标系，使参考观察者位于原点、朝向对齐z轴。这一变换使得后续推理问题在形式上等同于相机视角下的自我中心问题，从而**充分利用VLM固有的自我中心推理能力**。

### 3. 双模态视角提示

APC提供两种将变换后场景抽象传递给VLM的方式：
- **数值提示（APC-Num）**：以文本形式提供物体的3D坐标和朝向信息；
- **视觉提示（APC-Vis）**：在变换后的视角下渲染彩色立方体作为抽象图像，配合去除视角描述的重述问题 $Q^*$。

实验表明，视觉提示在可见性（visibility）和朝向（facing）任务上分别比数值提示高出18.75%和26.33%，揭示了VLM对数值坐标的逻辑推理能力弱于对抽象视觉输入的感知能力（Table 1）。

### 关键设计对照

| 设计维度 | 基线方法 | APC |
|---------|---------|-----|
| 视角转换机制 | 直接使用相机视角 | 场景抽象 + 坐标变换实现allocentric→egocentric转换 |
| 场景表示 | 原始RGB图像或密集重建 | 3D坐标（数值提示）或彩色立方体渲染（视觉提示） |
| 问题表达 | 包含视角描述的原问题 | 去除视角描述的视角无关重述 |

![[assets/figures/papers/paper_list_l2_https_arxiv_org_abs_2504_17207/figures/004_Figure_4.jpg]]
*Figure 4: Pipeline Overview of APC. Our proposed framework consists of three stages. 1) Scene Abstraction (Sec. 3.1): APC first detects the objects of interest and build a coarse 3D abstraction of the scene using off-the-shelf vision foundation models. 2) Perspective Change (Sec. 3.2): Then, a reference perspective is set and the abstraction is transformed into the reference viewer’s egocentric coordinate frame. 3) Perspective Prompting (Sec. 3.3): Finally, APC passes the transformed scene to the VLM by producing (1) a numerical (textual) prompt or (2) an abstract visual prompt, and poses the question of interest from the reference perspective*

APC 框架的核心思想是**通过构建场景的粗粒度3D抽象，将分配中心（allocentric）的空间推理问题转换为自我中心（egocentric）的表达**，从而绕过现有 VLM 在非相机视角下的推理缺陷。整个 pipeline 由三个顺序阶段构成，如图 Figure 4 所示。

### 输入与输出

- **输入**：一张 RGB 图像 $I$ 和一个包含视角描述的空间推理问题 $Q$（例如“从椅子的视角看，桌子在你的左边还是右边？”）。
- **输出**：VLM 在指定参考视角下对问题的答案。

### 阶段一：场景抽象（Scene Abstraction）

该阶段模拟心理意象的构建过程，从图像和问题中提取关键物体的粗粒度3D表示。具体步骤为：

1. **物体识别**：将图像 $I$ 和问题 $Q$ 输入 VLM，让其识别回答问题所需的感兴趣物体列表 $\{t_i\}$。
2. **3D定位**：使用 GroundingDINO 对每个物体 $t_i$ 进行检测，SAM 进行分割，DepthPro 估计深度，并通过反投影获得物体的3D中心位置 $c_i \in \mathbb{R}^3$。
3. **方向估计**：使用 OrientAnything 估计物体的正面朝向 $p_i$（在相机坐标系下）。
4. **检测精炼**：当 GroundingDINO 产生多个候选框时，利用 VLM 从裁剪网格中选择与文本描述最匹配的选项。

最终得到相机自我中心坐标系下的场景抽象集合：
$$S_E := \{O_i\}_{i=1}^n, \quad O_i = (t_i, c_i, p_i)$$

### 阶段二：视角变换（Perspective Change）

1. **参考视角识别**：将问题 $Q$ 输入 VLM，让其识别问题中指定的参考视角（例如“椅子”）。
2. **坐标变换**：将场景抽象 $S_E$ 从相机坐标系变换到参考视角 $A$ 的自我中心坐标系，使得 $A$ 位于原点，其朝向与 z 轴对齐。变换后的场景抽象记为 $S_A$，其中每个物体表示为 $O_i' = (t_i, c_i', p_i')$。

这一步骤的关键在于**无需生成新视角的真实图像**，仅通过坐标变换即可完成视角转换。

### 阶段三：视角提示（Perspective Prompting）

将变换后的场景抽象以两种可选格式传递给 VLM 进行推理：

1. **数值提示（APC-Num）**：直接使用物体的3D坐标和朝向信息构建文本提示，同时将原问题 $Q$ 重述为去除视角描述的自我中心版本 $Q^*$。
2. **视觉提示（APC-Vis）**：在参考视角的自我中心坐标系中，为每个物体放置彩色立方体并渲染为抽象图像，与重述问题 $Q^*$ 和物体-颜色映射一起作为多模态提示输入 VLM。

### 模块间的信息流

整个 pipeline 的信息流是严格顺序的：**场景抽象**的输出（$S_E$）作为**视角变换**的输入，视角变换的输出（$S_A$）作为**视角提示**的输入。各阶段之间不存在反馈回路，但检测精炼步骤在场景抽象内部引入了 VLM 对视觉基础模型输出的验证机制，形成局部的质量闭环。

### 关键设计选择

- **粗粒度抽象 vs. 密集重建**：APC 仅提取物体的3D中心和朝向，而非进行密集的3D重建或新视图合成。实验表明，这一选择使推理时间缩短超过14倍（17.47s vs. >260s），同时避免了密集重建中的噪声和失真问题（见 Table 2, Figure 9）。
- **双提示模式**：数值提示和视觉提示在不同任务上各有优势——数值提示在距离判断（closer）任务上达到96%准确率，而视觉提示在可见性（visibility）和朝向（facing）任务上分别高出18.75%和26.33%，表明 VLM 对数值坐标的逻辑推理能力存在局限，而抽象视觉表示能有效弥补这一不足。

APC 框架由三个核心模块串行构成：**场景抽象**、**视角变换**和**视角提示生成**，其设计目标是将分配中心（allocentric）的空间推理问题转化为 VLM 擅长的自我中心（egocentric）问题，从而绕过 VLM 固有的视角偏差。

### 3.1 场景抽象

场景抽象模块的作用是构建一个轻量级的 3D 场景表示，取代原始 RGB 图像作为后续视角变换的基础。该模块首先利用 VLM 从输入图像 $I$ 和问题 $Q$ 中识别回答问题所必需的物体列表，然后调用一系列视觉基础模型提取每个物体的 3D 空间属性。

场景抽象的形式化定义为：

$$S_E := \{ O_i \}_{i=1}^n$$

其中 $S_E$ 表示在相机自我中心坐标系下的感兴趣物体集合，$n$ 为物体数量。每个物体 $O_i$ 被表示为一个元组：

$$(t_i, c_i, p_i)$$

各变量含义如下：
- $t_i$：物体的文本描述，由 VLM 从问题中解析得到；
- $c_i \in \mathbb{R}^3$：物体的 3D 中心位置，通过 GroundingDINO 检测、SAM 分割、DepthPro 深度估计和反投影获得；
- $p_i$：物体的朝向，由 OrientAnything 估计其正面方向在相机坐标系下的表示。

为提高检测精度，APC 引入了**检测精炼**步骤：对 GroundingDINO 返回的 top-k 候选框，将其裁剪为网格图像提交给 VLM，由 VLM 选择与文本描述 $t_i$ 最匹配的候选框。

### 3.2 视角变换

视角变换模块的核心操作是将场景抽象从相机坐标系变换到参考视角坐标系。首先，APC 将问题 $Q$ 提交给 VLM，识别问题所要求回答的参考视角 $A$。随后，对 $S_E$ 中的每个物体执行坐标变换，将参考视角 $A$ 置于原点，并将其朝向对齐于 z 轴，从而得到变换后的场景抽象 $S_A$。

这一步骤将原本分配中心的问题转化为自我中心问题：在 $S_A$ 中，所有物体的位置和朝向都是相对于参考视角 $A$ 表达的，使得 VLM 可以直接利用其固有的自我中心推理能力。

### 3.3 视角提示生成

视角提示生成模块将变换后的场景抽象 $S_A$ 编码为 VLM 可理解的提示形式，同时生成去除视角描述的问题重述 $Q^*$。APC 探索了两种提示变体：

**数值提示**：直接将 $S_A$ 中每个物体的 3D 坐标和朝向信息以文本形式呈现。变换后的物体抽象为：

$$O_i' = (t_i, c_i', p_i')$$

其中 $c_i'$ 和 $p_i'$ 分别为物体在参考视角坐标系下的 3D 位置和朝向。

**视觉提示**：在参考视角处渲染一幅抽象图像，每个物体用一个彩色立方体表示其 3D 位置，同时构建物体-颜色映射和抽象问题，使 VLM 能够将渲染图中的立方体与原始物体对应。

### 3.4 公式体系总结

APC 的公式体系极为精简，核心仅包含场景抽象集合 $S_E$ 的定义和物体元组 $(t_i, c_i, p_i)$ 及变换后元组 $(t_i, c_i', p_i')$ 的表示。框架的推理能力不依赖于复杂的数学推导，而是通过模块化的视觉基础模型调用和坐标系变换，将视角推理问题转化为 VLM 原生擅长的自我中心推理任务。这一设计使得 APC 在保持高精度的同时，推理时间仅为密集重建基线的 1/14 以下。

## 实验与关键发现

### 核心定量结果

APC 在两个空间推理基准 COMFORT++ 和 3DSRBench 上均展现出对纯 VLM、空间调优 VLM 和密集重建基线的压倒性优势。表 1 汇总了主要结果。

![[assets/figures/papers/paper_list_l2_https_arxiv_org_abs_2504_17207/figures/007_Table_1.jpg]]
*Table 1: Quantitative Comparisons. Purple ( ) represents pure VLMs, green ( ) represents grounded VLMs, and red ( ) represents dense reconstruction-based frameworks. Gray ( ) corresponds to our APC. Bold and underline indicate the best and the second-best result for each column, respectively. APC-Num and APC-Vis refer to our method employing numerical prompt and visual prompt, respectively*

在 COMFORT++ 的 left/right 任务上，APC-Vis 达到 **89.67%** 的准确率，远超最佳纯 VLM 基线 LLaVA-OneVision 的 55.33%（提升 +34.34 个百分点）。APC-Num 同样取得 88.67%，表明两种提示形式在此任务上均有效。在 closer 任务上，APC-Num 达到 **96.00%**，比 LLaVA-OneVision 和 Cambrian-1 的最佳成绩（79.00%）高出 17 个百分点。

在 visibility 和 facing 任务上，APC 的优势更为突出。APC-Vis 分别取得 **90.00%** 和 **88.33%**，而随机基线仅为 50.00%。值得注意的是，APC-Vis 在这两项任务上比 APC-Num 分别高出 **+18.75%** 和 **+26.33%**，揭示了视觉提示在需要判断遮挡和朝向的推理任务上的显著优势。

在 3DSRBench 上，APC-Vis 在 facing 任务上达到 66.47%，略优于 Cambrian-1 的 64.03%；在 visibility 任务上达到 67.44%，远超随机基线（~50.00%）。left/right 任务上，APC-Vis 和 APC-Num 均稳定在 60% 以上，而随机基线约为 50%。

### 视角鲁棒性分析

图 8 展示了不同视角偏移角度 θ（相机视角与参考视角之间的夹角）下的准确率变化。基线模型在 allocentric 角度区间出现明显的性能退化，而 APC 在所有角度范围内均保持高且稳定的准确率。这一结果表明，APC 的场景抽象和坐标变换机制有效消解了 VLM 固有的自我中心偏差，使模型获得了真正的视角感知推理能力。

### 推理效率对比

表 2 对比了 APC 与密集重建基线的推理时间。SpatialPIN* 和 ViewCrafter 回答单个问题均需超过 260 秒，而 APC 仅需 **17.47 秒**，加速超过 **14 倍**。这一效率优势源于 APC 仅构建粗粒度的 3D 抽象，而非对场景进行密集重建。密集重建基线生成的 novel view 通常含有噪声和不准确的目标结构（见图 9），导致 VLM 推理精度低下，进一步验证了“抽象优于重建”的设计选择。

![[assets/figures/papers/paper_list_l2_https_arxiv_org_abs_2504_17207/figures/010_Table_2.jpg]]
*Table 2: Inference Time Comparison. Both dense reconstruction-based baselines [53, 87] require over 14 times the inference time of our APC to answer a single question*

### 消融与组件分析

**提示形式的影响**：APC-Vis 在 visibility 和 facing 任务上远优于 APC-Num，表明 VLM 对数值坐标的逻辑推理能力较弱，而视觉提示中的彩色立方体渲染提供了更直观的空间线索，减少了数值推理中的逻辑错误。

**检测精炼的作用**：通过 VLM 从 GroundingDINO 的候选框中选择最佳匹配（见图 10），检测精炼步骤有效提升了目标定位的准确性，减少了因错误检测导致的场景抽象噪声。

**视角变换的必要性**：若不执行 Perspective Change 阶段，直接将相机坐标系下的场景抽象输入 VLM，等价于退化为纯 VLM 基线。实验结果表明，坐标变换是 APC 性能提升的核心因果组件。

![[assets/figures/papers/paper_list_l2_https_arxiv_org_abs_2504_17207/figures/001_Figure.jpg]]

![[assets/figures/papers/paper_list_l2_https_arxiv_org_abs_2504_17207/figures/006_Figure_6.jpg]]
*Figure 6: Benchmark Visualization. Example image-question pairs from 3DSRBench [54] and COMFORT++ [90] benchmarks. The tasks probe spatial reasoning across left-right relations, object visibility, closenss, and the facing direction of objects*

## 定位与知识库关联

### 1. 问题定位：自我中心偏差与分配中心推理的鸿沟

当前视觉语言模型（VLMs）在空间推理中存在一个根本性瓶颈：**强烈的自我中心偏差（egocentric bias）**。如 Figure 2 所示，当问题从相机视角（自我中心）提出时，VLMs 表现良好；但同一问题一旦转换为分配中心（allocentric）视角——即从场景中某个参考物体或观察者的角度出发——模型性能急剧下降。这一偏差的根源在于 VLM 的训练数据天然以相机视角为主，模型缺乏对场景进行心理旋转（mental rotation）或视角转换的内在机制。

本文提出的 **Abstract Perspective Change (APC)** 框架并非试图“教会”VLM 进行分配中心推理，而是通过一个巧妙的因果操作：**将分配中心问题转换为自我中心问题**。这一转换通过构建场景的 3D 抽象表示并执行坐标变换实现，使 VLM 无需真正生成新视角图像，即可利用其固有的自我中心推理能力。

### 2. 方法谱系中的位置

APC 在空间推理 VLM 的方法谱系中占据了一个独特位置，介于纯端到端 VLM 与密集重建方法之间。

#### 2.1 纯视觉语言模型基线

实验对比了多款主流 VLM，包括 **LLaVA-NeXT**、**LLaVA-OneVision**、**Molmo**、**Qwen2.5-VL**、**Cambrian-1**、**GPT-4o** 和 **Gemini-2.0-Flash**。这些模型在 COMFORT++ 的 left/right 任务上最高仅达 55.33%（LLaVA-OneVision），而 APC-Vis 达到 89.67%（Table 1），提升幅度超过 34 个百分点。这一巨大差距表明，单纯扩大模型规模或增加训练数据无法自动克服自我中心偏差，必须引入显式的视角转换机制。

#### 2.2 面向空间推理调优的 VLM

**SpatialVLM** 和 **SpatialRGPT** 等方法通过在空间推理数据上进行专门调优来增强 VLM 的空间能力。然而，这些方法仍然在原始 RGB 图像上操作，未改变问题的视角框架。APC 不依赖额外调优，而是通过场景抽象和提示工程实现即插即用的视角转换，与任何 VLM 骨干兼容（当前实现基于 Cambrian-1）。

#### 2.3 利用视觉基础模型的 VLM 系统

**SpatialPIN** 是此方向最接近的工作，同样利用 GroundingDINO、SAM 等视觉基础模型提取场景信息。但 SpatialPIN 直接使用提取的 3D 信息进行推理，未执行视角变换。APC 的关键差异在于增加了 **Perspective Change** 阶段：将场景抽象从相机坐标系变换到参考视角坐标系（$O_i' = (t_i, c_i', p_i')$），使问题重新回到自我中心框架。

#### 2.4 密集重建基线

**SpatialPIN***（SpatialPIN 的扩展，引入视角变换）和 **ViewCrafter** 代表了另一类思路：通过新视图合成（novel view synthesis）生成目标视角的完整 RGB 图像，再输入 VLM 进行推理。然而，如 Figure 9 所示，这些方法合成的视图包含噪声、不准确的物体和结构，丢失了原始图像的上下文信息，导致 VLM 推理精度较低。更重要的是，如 Table 2 所示，APC 的推理时间（17.47 秒）比密集重建基线（>260 秒）**加速超过 14 倍**，同时精度更高。这验证了“抽象优于重建”的核心设计哲学：对于空间推理，精确的 3D 语义信息比像素级视觉保真度更重要。

### 3. 方法适用边界

APC 的适用边界由以下因素界定：

1. **场景复杂度限制**：当前场景抽象仅包含物体的 3D 中心位置和朝向（$(t_i, c_i, p_i)$ 元组），是一种粗糙的表示。对于包含严重遮挡、非刚性物体或复杂多物体关系的场景，这种抽象可能不足以捕捉必要的空间信息。

2. **物体检测依赖**：APC 依赖 GroundingDINO + SAM + DepthPro 的级联管道进行物体定位。检测失败、深度估计误差或朝向估计错误会直接传播到后续的视角变换和提示生成，影响最终推理准确性。

3. **静态场景假设**：当前框架假设场景是静态的，未考虑动态物体或时变关系。

4. **计算资源需求**：使用多个视觉基础模型增加了额外内存开销，需要两张 NVIDIA RTX 3090 24GB GPU。

### 4. 关键消融发现与因果机制

#### 4.1 视觉提示 vs. 数值提示

APC 探索了两种提示格式：**数值提示**（将变换后的 3D 坐标和朝向以文本形式直接输入 VLM）和**视觉提示**（用彩色立方体渲染抽象场景图像）。在 COMFORT++ 的 visibility 和 facing 任务上，APC-Vis 分别比 APC-Num 高出 18.75% 和 26.33%（Table 1, Sec 4.2）。这一显著差异揭示了 VLM 的一个关键特性：**VLM 对数值坐标的逻辑推理能力较弱，而视觉抽象能更有效地触发其空间推理能力**。对于 closer 任务，数值提示反而略优（96.00% vs. 视觉提示的对应值），表明不同任务类型可能偏好不同的提示模态。

#### 4.2 视角偏移鲁棒性

Figure 8 展示了不同视角偏移角度 $\theta$ 下的准确率变化。基线模型（如 Cambrian-1）在特定角度范围出现明显性能下降，而 APC 在所有角度保持稳定高精度。这证明 APC 的坐标变换机制有效解耦了视角偏移对推理的影响，而非仅在特定角度过拟合。

#### 4.3 检测精炼的作用

如 Figure 10 所示，GroundingDINO 的初始检测可能存在歧义。APC 引入检测精炼步骤（C.1 Detection Refinement with VLM）：从 top-k 候选框中由 VLM 选择最佳匹配。这一步骤提高了检测准确性，减少了错误传播。

### 5. 开放问题

1. **噪声鲁棒性**：如何进一步减少场景抽象中的噪声（错误检测、深度估计误差）对推理准确性的影响？是否可以通过不确定性建模或多假设推理来提升鲁棒性？

2. **视觉提示优势的深层原因**：视觉提示在 visibility 和 facing 任务上远超数值提示，是否因为 VLM 在预训练中主要学习视觉空间关系而非数值坐标推理？这一发现对提示设计有何一般性启示？

3. **场景抽象的粒度扩展**：能否利用更丰富的 3D 抽象（如 3D 边界框、语义重建、物体间关系图）来提升性能，同时保持计算效率优势？

4. **多物体与动态场景**：当前方法能否扩展到包含更多物体或动态场景？场景抽象的复杂度如何随物体数量增长？

5. **跨模型泛化性**：APC 框架当前基于 Cambrian-1 实现，其核心机制（场景抽象 + 视角变换 + 提示生成）是否与其他 VLM 骨干模型（如 GPT-4o、Gemini）兼容？不同模型对数值提示和视觉提示的响应是否存在差异？

## 原文 PDF

![[paperPDFs/ICCV_2025/Perspective_Aware_Reasoning_in_Vision_Language_Models_via_Mental_Imagery_Simulation.pdf]]
