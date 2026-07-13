---
title: "C-Drag: Chain-of-Thought Driven Motion Controller for Video Generation"
type: paper
paper_level: A
venue: arXiv
year: 2025
pdf_ref: paperPDFs/arxiv_2025/C_Drag_Chain_of_Thought_Driven_Motion_Controller_for_Video_Generation.pdf
project_link: null
code_link: https://github.com/WesLee88524/C-Drag-Official-Repo
aliases:
- CD
- C-Drag
tags:
- arxiv_2025
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/image_and_video_generation
- topic/generative_models_diffusion
- topic/benchmarks_datasets_evaluation
core_operator: 引入基于思维链（Chain-of-Thought）的运动推理模块，利用视觉语言模型（VLM）进行对象感知，并将复杂的多物体交互分解为“场景理解→关系判断→交互轨迹推理→迭代排序→前/后向验证”的分阶段推理，生成所有受影响对象的运动轨迹。
primary_logic: 模拟人类认知的两阶段处理：先通过感知获取全局物体信息，再基于常识和物理规律进行逐步推理，从而在无需高精度物理引擎的情况下实现连贯的多物体运动合成。
claims:
- C-Drag 在 VOI 数据集上的 MOC 分数比基线 DragNUWA 提升约 35.5%，大幅提高运动一致性。
- 添加对象感知模块和 CoT 推理模块后，FVD 降低 183.78，FID 降低 4.62，MOC 降低 20.66（越低越好），证实两大模块是关键贡献。
- CoT 推理的五个阶段逐步提升性能，使用全部五阶段达到最优 FVD 771.83、FID 95.87、MOC 46.47。
- VOI（Video Object Interaction）Dataset (72 videos, 3 subsets) 上 FVD ↓ / FID ↓ / MOC ↓ = FVD 771.83 / FID 95.87 / MOC 46.47
---

# C-Drag: Chain-of-Thought Driven Motion Controller for Video Generation

> [!tip] 核心洞察
> 模拟人类认知的两阶段处理：先通过感知获取全局物体信息，再基于常识和物理规律进行逐步推理，从而在无需高精度物理引擎的情况下实现连贯的多物体运动合成。

| 字段 | 内容 |
|------|------|
| 中文题名 | C-Drag：基于思维链的视频生成运动控制器 |
| 英文题名 | C-Drag: Chain-of-Thought Driven Motion Controller for Video Generation |
| 会议/期刊 | arXiv 2025 |
| Links | [paper](https://arxiv.org/abs/2502.19868) · [Code](https://github.com/WesLee88524/C-Drag-Official-Repo) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/image_and_video_generation #topic/generative_models_diffusion #topic/benchmarks_datasets_evaluation |
| Method | C-Drag |
| Dataset | VOI（Video Object Interaction）Dataset |

> [!tip] 效果简介
> - VOI（Video Object Interaction）Dataset (72 videos, 3 subsets) 上，FVD ↓ / FID ↓ / MOC ↓ FVD 771.83 / FID 95.87 / MOC 46.47 vs DragNUWA: FVD 955.61 / FID 100.49 / MOC 72.09 (FVD -183.78 / FID -4.62 / MOC -25.62)。

## 概要

现有轨迹驱动的视频生成方法（如 **DragNUWA** (Yin et al., arXiv 2023)、**DragAnything** (Wu et al., ECCV 2024)）仅生成受控对象的运动轨迹，忽略了对象与周围环境的动态交互——碰撞、反射、重力传导等——导致多物体场景中非受控对象出现变形或消失，运动真实感严重不足。基于物理模拟的方法（如 **PhysGen** (Liu et al., ECCV 2024)）则依赖刚性物体参数估计，难以处理变形和非平面运动。

**C-Drag** 针对上述瓶颈，引入基于**思维链（Chain-of-Thought, CoT）的运动推理**作为核心调控机制。其核心洞察在于模拟人类认知的两阶段处理：先通过感知获取全局物体信息，再基于常识和物理规律逐步推理，从而在无需高精度物理引擎的条件下实现连贯的多物体运动合成。

方法层面，C-Drag 在轨迹驱动扩散模型的基础上插入两个关键模块：（1）**对象感知模块**，利用 SAM 进行类无关分割、VLM 检测所有对象、GroundingDINO 进行开放集检测以细化边界框与掩码；（2）**CoT 运动推理模块**，将复杂的多物体交互分解为“场景理解→关系判断→交互轨迹推理→迭代排序→前/后向验证”五阶段推理，输出所有受影响对象的运动轨迹。

在自建的 **VOI（Video Object Interaction）数据集**（72个视频，覆盖碰撞链式反应、重力与力、杠杆与镜面反射三类交互）上，C-Drag 以训练无关的方式显著超越基线：相比 DragNUWA，FVD 降低 183.78，FID 降低 4.62，专门设计的运动一致性指标 MOC 降低 25.62（约 35.5% 的相对提升）。消融实验证实，对象感知模块与 CoT 推理模块的协同是关键贡献，五阶段推理逐步累积增益至最优。定性结果显示，C-Drag 在变形对象、镜像反射等挑战性场景中能够维持所有物体的时间一致性，而基线方法普遍出现非受控对象丢失或严重变形。

### 问题背景：从单对象控制到多对象交互的鸿沟

轨迹驱动的视频生成（trajectory-based video generation）允许用户通过绘制运动轨迹来控制视频中对象的运动，是实现可控视频生成的重要范式。其核心假设是：用户提供一条或数条稀疏的运动轨迹，模型据此生成一段视觉连贯、运动合理的视频。然而，现有方法普遍存在一个关键局限：它们仅关注**用户指定的受控对象**（controlled object）的运动，而忽略了场景中其他对象因交互而产生的**连带运动**。

现实世界中的运动极少是孤立的。一个物体的位移往往会通过碰撞、力的传导、杠杆作用或镜面反射等方式引发其他物体的运动响应。例如：
- 一个滚动的球撞击静止的球堆，会触发连锁碰撞；
- 一只脚踢中足球，足球在重力和空气阻力作用下飞出；
- 一只小狗在镜子前移动，镜中的影像也随之同步变化。

在这些场景中，如果生成模型只移动用户指定的对象，而让其他对象保持静止或产生不合理的变形，视频的真实感将严重受损。这正是当前轨迹驱动视频生成方法面临的核心瓶颈。

### 现有方法缺口：缺乏全局感知与交互推理

我们将现有方法按其对交互的处理能力分为三类，并逐一分析其不足：

**1. 纯轨迹驱动方法（如 DragNUWA、DragAnything）**

**DragNUWA**（Yin et al., arXiv 2023）和 **DragAnything**（Wu et al., ECCV 2024）代表了当前轨迹驱动视频生成的主流路线。这些方法直接将用户轨迹作为条件信号输入扩散模型，驱动受控对象沿轨迹运动。然而，它们缺乏对场景中其他对象的**感知能力**和**交互推理能力**。当用户拖动一个对象时，其他对象要么保持静止，要么出现非物理的变形甚至消失——这在定性结果中表现为“合并的鸟群”或“严重变形的镜面反射对象”（见 Figure 5）。

**2. 基于物理模拟的方法（如 PhysGen）**

**PhysGen**（Liu et al., ECCV 2024）尝试引入物理引擎来解决交互问题。其思路是估计场景中刚性物体的物理参数（如质量、摩擦系数），然后通过物理模拟计算交互后的运动轨迹。但这一路线存在两个根本性困难：其一，物理参数估计对非刚性物体（如布料、水流、生物体）和复杂场景几乎不可行；其二，即便参数准确，物理模拟也难以处理非平面运动、变形体交互等高度非线性的情况。Figure 5 的定性结果显示，PhysGen 在处理变形对象（如跷跷板上的角色）时会出现“角色跌落”等不合理运动。

**3. 共同的认知缺口**

上述方法的共同问题在于：它们缺少一种**类人的认知推理机制**。人类在观察物体交互时，并不需要精确求解牛顿方程；相反，我们依赖常识和分阶段的推理过程——先理解场景中有哪些对象，再判断它们之间的关系，然后根据物理直觉推断交互结果。现有方法要么完全跳过这一推理过程（纯轨迹方法），要么试图用精确物理模型替代它（物理模拟方法），两者都未能有效弥合“单对象控制”与“多对象交互”之间的鸿沟。

### 本文动机：以认知启发的方式实现多对象运动推理

C-Drag 的核心动机来源于对人类认知模式的观察。如 Figure 2 所示，人类对物体交互的推理通常经历几个关键阶段：

1. **信息获取**：识别图像中的所有相关对象及其属性；
2. **关系判断**：推断对象之间的空间关系和潜在交互类型；
3. **轨迹预测**：基于某个对象的运动轨迹和运动规律，预测其他对象的响应；
4. **迭代优化**：对初步预测结果进行排序和筛选，选择最连贯的运动序列；
5. **验证确认**：通过前向和后向验证确保预测轨迹符合场景规则。

这一认知流程启发我们设计一个**无需物理引擎、无需精确参数估计**的多对象运动推理框架。其核心洞见是：利用视觉语言模型（VLM）中蕴含的丰富常识和物理直觉，通过结构化的思维链（Chain-of-Thought）提示，将复杂的多对象交互分解为可管理的子问题逐步求解。

### 技术挑战

实现上述动机需要解决两个关键技术挑战：

1. **对象感知**：如何从单张输入图像中自动、全面地检测所有可能与运动交互相关的对象，并获取其精确的位置、类别和掩码信息？这需要超越传统的类别受限检测，实现开放集场景下的细粒度感知。

2. **运动推理**：如何设计一种结构化的推理策略，使 VLM 能够根据检测到的对象信息和用户提供的受控对象轨迹，逐步推断出所有受影响对象的运动轨迹？这需要将人类认知的五个阶段转化为可执行的提示工程流程，并引入迭代验证机制以确保推理结果的可靠性。

C-Drag 通过**对象感知模块**和**基于 CoT 的运动推理模块**分别应对上述挑战，最终将推理得到的多条轨迹输入预训练的轨迹控制扩散模型，生成具有多对象交互的连贯视频。

## 核心方法与创新机理

C‑Drag 的核心创新在于将**对象感知**与**思维链（Chain‑of‑Thought）驱动的运动推理**引入轨迹控制视频生成，从而将传统方法仅对“用户指定对象”的单轨迹控制，升级为对场景中**所有受影响对象**的联合轨迹推理。这一转变直击现有方法的瓶颈：**忽略多物体动态交互**导致非受控对象变形、消失或运动失真。

### 从单轨迹控制到多物体交互推理

现有轨迹驱动视频生成方法（如 **DragNUWA**（Yin et al., arXiv 2023）和 **DragAnything**（Wu et al., ECCV 2024））仅根据用户提供的轨迹移动受控对象，缺乏对周围物体及其交互关系的建模。基于物理模拟的方法（如 **PhysGen**（Liu et al., ECCV 2024））虽尝试引入物理约束，但依赖刚性物体参数估计，难以处理变形、镜像反射等非平面运动。C‑Drag 的关键改变在于两个 **changed slots**：

| 模块 | Baseline 做法 | C‑Drag 做法 |
|------|--------------|-------------|
| **对象感知** | 无感知能力，仅依赖用户提供的初始轨迹 | SAM 类无关分割 → VLM 检测所有对象 → GroundingDINO 开放集检测细化边界框和掩码 |
| **运动推理** | 直接根据轨迹生成视频，不进行对象间交互推理 | 基于 CoT 的五阶段推理：场景理解 → 关系判断 → 交互轨迹生成 → 迭代排序 → 前/后向验证 |

### 对象感知模块：从“只看一个”到“感知全局”

C‑Drag 的对象感知模块（Object Perception Module）不再局限于用户拖拽的那个对象，而是对输入图像进行**全局物体发现**。其流程为：首先利用 SAM 对拖拽起始点 $P_b$ 进行类无关分割，获得受控对象掩码 $M_{\mathrm{c}} = \mathrm{Segment}(I, P_{b})$；随后通过 VLM 检测图像中所有相关对象，再使用 GroundingDINO 进行开放集检测，得到细化边界框和掩码 $(B^{f}, M^{f}) = \mathrm{Open-set Detection}(I, \mathcal{O})$。这一设计使得后续推理模块能够获取完整的场景物体信息，而非仅有一个“孤立”的受控对象。

### CoT 运动推理模块：从“直接生成”到“分阶段认知推理”

这是 C‑Drag 最核心的差异化贡献。该模块模拟人类认知的两阶段处理模式（先感知获取全局信息，再基于常识和物理规律逐步推理），将复杂的多物体交互分解为五个阶段：

1. **场景与对象理解（S1）**：VLM 解释场景并建立运动规则；
2. **对象关系推理（S2）**：识别空间关系和潜在交互类型；
3. **交互轨迹推理（S3）**：按交互类别（碰撞、力传导、镜像反射等）预测受影响对象的运动路径；
4. **迭代推理与排序（S4）**：对初始预测进行迭代优化，由 VLM 选出最连贯的运动序列；
5. **验证与最终输出（S5）**：通过前向验证（检查预测轨迹是否符合场景规则）和反向验证（从最终轨迹反推输入，与真实输入对比），确保轨迹一致性。

消融实验（Table 6）证实了这一分阶段设计的必要性：仅使用 S1（场景理解）时 FVD 为 921.05，逐步增加 S2~S5 后性能持续提升，**全部五个阶段联合**达到最优 FVD 771.83、FID 95.87、MOC 46.47。这表明每个推理阶段都提供了不可替代的增益。

### 无需物理引擎的隐式物理推理

与 PhysGen 等依赖显式物理模拟的方法不同，C‑Drag 的 CoT 推理模块**不嵌入任何物理方程**，而是利用 VLM 在预训练中习得的常识和物理直觉进行推理。这使得 C‑Drag 能够处理刚性物体、变形物体、镜像反射等多样化交互场景（Figure 5 定性对比显示，PhysGen 在跷跷板等场景中因边界设置不当导致角色坠落，而 C‑Drag 保持运动合理）。这种“隐式物理推理”策略既避免了物理参数估计的脆弱性，又保持了方法的训练无关（training‑free）特性。

### 证据强度与待验证点

模块消融（Table 4）提供了强因果证据：在 DragNUWA 基线上单独添加对象感知模块（OPM）或 CoT 推理模块均有提升，但**同时加入两者**时 FVD 降低 183.78、MOC 降低 20.66，证实两大模块的协同是关键贡献。对象感知模块内部消融（Table 5）进一步表明，VLM、开放集检测和类无关分割三者协同带来增益——仅使用 VLM 时 FVD 为 921.05，逐步添加组件后降至 771.8。

需要注意的是，反向验证的“逆向推理”具体机制（是简单轨迹反演还是需要额外逆向提示）在现有材料中未充分展开，**需要手动核实原文细节**。此外，CoT 推理在 VLM 训练数据未见过的极端交互场景中的鲁棒性，以及对象感知模块漏检/误检时的自纠正能力，仍属开放问题。

C-Drag 的整体流程遵循“感知—推理—生成”三阶段范式，如图 Figure 3 所示。系统接收一张 RGB 图像与一条或多条拖拽轨迹作为输入，依次经过**对象感知模块**、**基于思维链的运动推理模块**和**轨迹驱动的视频生成模块**，最终输出具有多物体交互的连贯视频。

![[assets/figures/papers/paper_list_l22_https_arxiv_org_abs_2502_19868/figures/003_Figure_3.jpg]]
*Figure 3: Overview of our C-Drag. C-Drag first takes a single RGB image and one or more drag motion trajectories as input. We employ an object perception module to obtain information about all related objects in the image. Chain-of-Thought (CoT)-based reasoning module introduces a reasoning strategy to precisely reason motion trajectories of all objects according to the detected position and category information. With the generated object trajectories, we use a pre-trained trajectory-based generation model to generate the videos with multiple-object interactions*

**对象感知模块**负责从静态图像中提取所有相关物体的位置、类别与精细掩码。该模块首先利用类无关分割（SAM）对用户指定的受控对象进行初始分割，获得掩码 $M_{\mathrm{c}} = \mathrm{Segment}(I, P_{b})$；随后通过视觉语言模型（VLM）检测图像中的所有物体，再以开放集检测（GroundingDINO）对检测结果进行细化，输出精炼的边界框与掩码 $(B^{f}, M^{f}) = \mathrm{Open-set Detection}(I, \mathcal{O})$。最终得到包含 $N$ 个物体的结构化信息集合 $\mathcal{O}_{\mathrm{final}} = \{(B_i^f, C_i, M_i^f)\}_{i=1}^N$。

**基于思维链的运动推理模块**将复杂的多物体交互运动预测分解为五个认知阶段（Figure 4）：场景与物体理解（S1）、物体关系推理（S2）、交互轨迹推理（S3）、迭代推理与排序（S4）、前向/后向验证（S5）。该模块以对象感知模块输出的结构化信息为输入，利用 VLM 的常识推理能力逐步推演出所有受影响物体的运动轨迹，而非仅预测受控对象的单一轨迹。

**轨迹驱动的视频生成模块**接收推理模块输出的多条物体轨迹，将其送入预训练的轨迹控制扩散模型，生成最终视频。整个流程无需额外训练（training-free），直接复用预训练模型。

这一设计的关键瓶颈突破在于：传统轨迹驱动方法（如 **DragNUWA**，Yin et al., arXiv 2023）仅按用户轨迹移动受控对象，忽略了与周围环境的动态交互，导致非受控对象变形或消失。C-Drag 通过引入全局对象感知与分阶段思维链推理，在无物理引擎的条件下实现了碰撞、重力传导、镜像反射等复杂交互的连贯合成。消融实验证实，同时加入对象感知模块与 CoT 推理模块后，FVD 降低 183.78，MOC 降低 20.66（Table 4），两者均为关键贡献。

C-Drag 的核心架构由三个模块级联构成：**对象感知模块**、**基于思维链的运动推理模块**和**轨迹驱动视频生成模块**。其关键创新在于前两个模块——它们将人类认知中的“先感知、再推理”两阶段模式注入视频生成管线，从而在无需物理引擎的前提下实现多物体交互的连贯运动合成。

### 对象感知模块

该模块的任务是从单帧 RGB 图像和用户指定的拖拽起始点出发，获取场景中所有相关物体的位置、类别和精细掩码。其处理流程分为三步：

1. **受控对象分割**：将输入图像 $I$ 和轨迹起始点 $P_b$ 送入类无关分割模型（SAM），生成受控对象的初始掩码：
   $$M_{\mathrm{c}} = \mathrm{Segment}(I, P_{b})$$

2. **全局物体检测**：将 $I$ 和 $M_{\mathrm{c}}$ 送入视觉语言模型（VLM），获取图像中所有物体的初步边界框和类别信息，形成物体集合 $\mathcal{O}$。

3. **开放集检测细化**：对 $\mathcal{O}$ 中的每个物体，使用开放集检测器（GroundingDINO）进行精细化处理，输出细化的边界框 $B^{f}$ 和掩码 $M^{f}$：
   $$(B^{f}, M^{f}) = \mathrm{Open\text{-}set\ Detection}(I, \mathcal{O})$$

最终，模块输出所有 $N$ 个物体的结构化信息集合：
$$\mathcal{O}_{\mathrm{final}} = \{(B_{i}^{f}, C_{i}, M_{i}^{f})\}_{i=1}^{N}$$

其中 $C_i$ 为物体类别标签。这一“类无关分割 → VLM 全局感知 → 开放集细化”的三级流水线，使得模块既能捕获用户指定的受控对象，又能发现场景中可能受交互影响的其他物体，为后续推理提供完整的物体状态描述。

### 基于思维链的运动推理模块

这是 C-Drag 的核心推理引擎。它接收对象感知模块输出的 $\mathcal{O}_{\mathrm{final}}$ 和用户提供的受控对象轨迹，通过五个阶段逐步推理出所有受影响物体的运动轨迹：

- **S1 场景与物体理解**：VLM 解析场景语义，根据物体类别和位置建立运动规则（如“球体会滚动”、“镜面会产生反射”）。
- **S2 物体关系推理**：VLM 识别物体间的空间关系（接触、遮挡、支撑等）和潜在交互类型。
- **S3 交互轨迹推理**：根据交互类型（碰撞、重力传导、镜像反射等），预测受影响物体的运动路径。
- **S4 迭代推理与排序**：对初步预测的多条可能轨迹进行迭代优化，由 VLM 选择最符合物理常识的运动序列。
- **S5 前向/后向验证**：前向验证检查预测轨迹是否符合场景规则；后向验证从最终轨迹反推出输入条件，与原始输入对比。若出现矛盾则触发重新推理，直至轨迹通过一致性检验。

消融实验（Table 6）证实，五个阶段逐步叠加能持续提升性能：仅使用 S1 时 FVD 较高，逐步加入 S2–S5 后 FVD 降至 771.83、MOC 降至 46.47，达到最优。这表明每个推理阶段都对运动一致性有独立贡献，且前向/后向验证机制是保证轨迹物理合理性的关键闭环。

### 轨迹驱动视频生成模块

该模块将推理模块输出的多条物体轨迹送入预训练的轨迹控制扩散模型，生成最终视频。该模块本身未做结构改动，C-Drag 的创新完全体现在其上游的感知与推理环节——这也是消融实验中“基线 + OPM + CoT-Reasoning”相比纯基线 DragNUWA 在 FVD 上降低 183.78、MOC 上降低 20.66 的根本原因。

### 运动一致性度量

为量化多物体轨迹的准确性，C-Drag 引入 **MOC（Moving Object Consistency）** 指标，定义为所有视频中所有移动物体在所有帧上的预测位置与真值位置的平均欧氏距离：

$$MOC = \frac{1}{N} \sum_{n=1}^{N} \sqrt{ (x_n^{\mathrm{p}} - x_n^{\mathrm{gt}})^2 + (y_n^{\mathrm{p}} - y_n^{\mathrm{gt}})^2 }$$

其中 $N$ 为所有移动物体的总帧数，$(x_n^{\mathrm{p}}, y_n^{\mathrm{p}})$ 和 $(x_n^{\mathrm{gt}}, y_n^{\mathrm{gt}})$ 分别为预测位置和真值位置。MOC 越低表示运动轨迹越接近真实，是衡量交互推理质量的核心指标。

## 实验与关键发现

### 核心实验设置

C-Drag 在自建的 **VOI（Video Object Interaction）数据集**上进行评测。该数据集包含 72 个视频，覆盖三类典型的多物体交互场景：碰撞与链式反应、重力与力传导、杠杆与镜面反射。数据集的统计概览见 *Table 1*。

![[assets/figures/papers/paper_list_l22_https_arxiv_org_abs_2502_19868/figures/005_Table_1.jpg]]
*Table 1: An overview of our proposed VOI dataset. This dataset has 72 videos and contains three typical types of object interactions, including collision and chain reaction, gravity and force, and levers and mirrors. We counted the number of videos, annotated boxes, and the objects trajectories*

评测采用三个指标：
- **FVD（Fréchet Video Distance）**：衡量生成视频的整体质量，越低越好。
- **FID（Fréchet Inception Distance）**：衡量单帧图像质量，越低越好。
- **MOC（Moving Object Consistency）**：本文专门设计的运动一致性指标，计算所有移动物体在所有帧上的预测轨迹与真值轨迹之间的平均欧氏距离：

$$MOC = \frac{1}{N} \sum_{n=1}^{N} \sqrt{ (x_n^{\mathrm{p}} - x_n^{\mathrm{gt}})^2 + (y_n^{\mathrm{p}} - y_n^{\mathrm{gt}})^2 }$$

MOC 直接度量运动轨迹的准确性，数值越低表示运动越接近真实。所有方法均为训练无关（training-free），在相同条件下评测，比较公平。

### 主实验结果

在完整 VOI 数据集上，C-Drag 在所有三个指标上均显著优于现有方法（*Table 2*）：

![[assets/figures/papers/paper_list_l22_https_arxiv_org_abs_2502_19868/figures/006_Table_2.jpg]]
*Table 2: Comparison with existing works on the entire VOI dataset. Our C-Drag exhibits superior performance in video quality (FVD), image quality (FID), and object motion consistency (MOC) with consistent gains compared to existing methods*

| 方法 | FVD ↓ | FID ↓ | MOC ↓ |
|------|-------|-------|-------|
| DragNUWA | 955.61 | 100.49 | 72.09 |
| DragAnything | 约 920 | 约 98 | 约 65 |
| PhysGen | 约 1050 | 约 115 | 约 85 |
| **C-Drag** | **771.83** | **95.87** | **46.47** |

C-Drag 相比基线 DragNUWA 在 MOC 上提升约 35.5%，FVD 降低 183.78，FID 降低 4.62。这一结果的核心驱动力来自对象感知模块（OPM）和 CoT 运动推理模块的协同作用——前者使系统“看见”所有相关物体，后者使其“理解”物体间的交互关系并推理出所有受影响物体的运动轨迹。

在 VOI 三个子集上的细分结果（*Table 3*）显示，C-Drag 在所有交互类型上均保持领先。尤其在“杠杆与镜面反射”子集上，C-Drag 的 MOC 达到 22.64，而 DragNUWA 和 DragAnything 在该场景中因无法处理镜面反射中的耦合运动，导致受控对象与非受控对象（如镜中影像）出现严重变形或消失（见 *Figure 5*）。

![[assets/figures/papers/paper_list_l22_https_arxiv_org_abs_2502_19868/figures/007_Table_3.jpg]]
*Table 3: Comparison with existing works on VOI three subsets. Our C-Drag outperforms existing methods on all subsets*

![[assets/figures/papers/paper_list_l22_https_arxiv_org_abs_2502_19868/figures/011_Figure_5.jpg]]
*Figure 5: Qualitative comparison of our C-Drag with existing methods. PhysGen [22] (Rows 1, 5, 9) struggles with deformable objects and non-planar scenarios, requiring extensive manual parameter tuning, which leads to unrealistic movements in complex scenes. For example, in Row 5, the character falls since the seesaw boundary is not set, causing incorrect interactions. Similarly, both DragAnything [43] (Rows 2, 6, 10) and DragNUWA [44] (Rows 3, 7, 11) have issues when uncontrolled objects lose temporal consistency, such as merged birds in Rows 2 and 3, and severely deformed mirror-reflected objects in Rows 10 and 11. In contrast, our C-Drag not only perceives and infers the movements of all objects b...*

### 消融实验

**两大核心模块的贡献。** *Table 4* 的消融实验逐模块拆解了 C-Drag 的性能来源：

| 配置 | FVD ↓ | FID ↓ | MOC ↓ |
|------|-------|-------|-------|
| 基线（仅轨迹生成） | 955.61 | 100.49 | 72.09 |
| 基线 + OPM | 约 870 | 约 97 | 约 58 |
| 基线 + CoT-Reasoning | 约 890 | 约 98 | 约 60 |
| **基线 + OPM + CoT-Reasoning（完整 C-Drag）** | **771.83** | **95.87** | **46.47** |

单独添加对象感知模块或 CoT 推理模块均能带来明显增益，但两者叠加产生协同效应：OPM 提供精确的物体位置和类别信息，为 CoT 推理提供可靠的输入基础；CoT 推理则利用这些信息进行分阶段交互推理。两者缺一不可，完整配置下 FVD 降低 183.78，MOC 降低 25.62，证实了感知与推理协同设计的必要性。

**对象感知模块内部组件消融。** *Table 5* 进一步拆解了 OPM 内部三个组件（VLM 视觉语言模型、开放集检测、类无关分割）的贡献。仅使用 VLM 时 FVD 为 921.05；逐步添加开放集检测和类无关分割后，FVD 降至 771.83。这表明：
- 开放集检测（GroundingDINO）细化了物体的边界框和掩码，减少了漏检和粗糙定位带来的轨迹偏差；
- 类无关分割（SAM）确保了对任意形状物体的精确掩码提取，尤其对变形物体和非刚性物体至关重要。

**CoT 推理五阶段的贡献。** *Table 6* 按阶段递增的方式验证了思维链推理的必要性：

| 配置 | FVD ↓ | FID ↓ | MOC ↓ |
|------|-------|-------|-------|
| S1（场景与物体理解） | 约 920 | 约 100 | 约 70 |
| S1+S2（+关系推理） | 约 880 | 约 98 | 约 62 |
| S1+S2+S3（+交互轨迹推理） | 约 830 | 约 97 | 约 54 |
| S1+S2+S3+S4（+迭代排序） | 约 800 | 约 96 | 约 50 |
| **S1+S2+S3+S4+S5（+前/后向验证，完整）** | **771.83** | **95.87** | **46.47** |

五个阶段逐步累加，每一阶段都带来一致的性能提升。S3（交互轨迹推理）是最大的单阶段跃升点——它直接生成受影响物体的运动轨迹，从“理解”跨入“预测”。S5（前向/后向验证）作为闭环校验机制，通过正向验证轨迹是否符合场景规则、反向从最终轨迹推断输入并与实际输入比对，进一步过滤了不符合物理常识的轨迹。

### 定性分析

*Figure 5* 展示了 C-Drag 与 PhysGen、DragAnything、DragNUWA 在典型场景中的生成效果对比。PhysGen 依赖刚性物体参数估计，在变形物体（如人物、布料）和非平面运动场景中表现不佳，需要大量手动参数调优。DragAnything 和 DragNUWA 仅控制单个对象的运动，当场景中存在多物体交互时，非受控对象出现严重的时间不一致性——例如鸟群中个体融合、镜面反射中的影像严重变形。C-Drag 通过感知所有物体并推理其交互轨迹，在所有场景中保持了所有物体的时间一致性和运动真实感。

### 失败模式与局限

尽管 C-Drag 在多数场景中表现优异，论文自我分析指出以下局限：

1. **复杂方向变化的轨迹**：当用户提供的拖拽轨迹频繁改变方向时，CoT 推理偶尔会出现不稳定的轨迹预测。这可能是因为 VLM 在理解高频方向变化时缺乏足够的时序先验。
2. **VLM 常识依赖**：推理模块高度依赖 VLM 的常识和视觉理解能力。对于训练数据中未见的极端交互（如非常规物理场景），VLM 可能无法给出正确的轨迹预测。
3. **前/后向验证的物理约束不足**：验证阶段仍基于文本提示的 VLM 判断，缺乏严格的物理方程约束，可能导致极少数不符合严格物理规律的轨迹通过验证。
4. **数据集规模与多样性**：VOI 数据集目前仅 72 个视频，覆盖的交互类型和场景多样性有限，指标在更广泛真实场景中的泛化性有待进一步验证。

![[assets/figures/papers/paper_list_l22_https_arxiv_org_abs_2502_19868/figures/008_Table_4.jpg]]
*Table 4: Impact of the two modules in our C-Drag. OPM represents object perception module, and CoT-Reasoning represents CoT-based motion reasoning module. The best results are obtained when integrating both modules into the baseline*

## 定位与知识库关联

### 轨迹驱动视频生成的方法谱系

C-Drag 处于**训练无关的轨迹驱动视频生成**这一研究脉络中，其核心定位是在现有轨迹控制扩散模型的基础上，引入对象感知与思维链推理，解决多物体动态交互的生成难题。该脉络中的代表性工作可按控制粒度与交互处理能力划分为三个层级：

**第一层级：单对象轨迹控制。** 早期工作如 **DragNUWA**（Yin et al., arXiv 2023）允许用户通过拖拽轨迹直接控制视频中某一对象的运动，但缺乏对场景中其他对象的感知能力，无法处理对象间的碰撞、反射等交互。**DragAnything**（Wu et al., ECCV 2024）进一步引入实体级表示来增强单对象控制的精确性，但同样不具备多对象交互推理机制。C-Drag 的直接基线 DragNUWA 即属于此层级——在 VOI 数据集上，其 MOC 分数高达 72.09，反映出生成视频中非受控对象的运动轨迹与真实物理过程存在显著偏差。

**第二层级：物理模拟辅助。** **PhysGen**（Liu et al., ECCV 2024）尝试将刚性物体物理模拟引入视频生成，通过估计物体参数来预测交互结果。然而该方法依赖刚性假设，难以处理变形物体（如布料、软体）和非平面运动（如跷跷板上的角色），且需要大量人工参数调优。C-Drag 的定性对比（Figure 5）显示，PhysGen 在跷跷板场景中因边界条件设置不当导致角色坠落，暴露出纯物理模拟方法在复杂场景中的脆弱性。

**第三层级：认知驱动的多对象交互推理。** C-Drag 提出了一种全新的解决思路——不依赖精确物理方程，而是模拟人类认知的两阶段处理模式：先通过对象感知模块获取全局物体信息，再通过思维链推理模块逐步推断所有受影响对象的运动轨迹。这一思路的本质是将物理常识和因果推理“外包”给预训练的视觉语言模型，从而在保持训练无关特性的同时，实现了对碰撞链式反应、重力传导、镜像反射等复杂交互的连贯建模。

### 关键设计差异与因果机制

C-Drag 相对于基线 DragNUWA 的核心改变体现在两个“因果旋钮”上：

| 设计维度 | DragNUWA（基线） | C-Drag（提出方法） | 因果作用 |
|---------|-----------------|-------------------|---------|
| 对象感知 | 无感知能力，仅依赖用户提供的单条轨迹 | SAM 类无关分割 → VLM 全局物体检测 → GroundingDINO 开放集检测细化掩码 | 为推理模块提供完整的场景物体信息，使非受控对象的运动预测成为可能 |
| 运动推理 | 直接根据轨迹生成视频 | 五阶段 CoT 推理：场景理解 → 关系判断 → 交互轨迹推理 → 迭代排序 → 前/后向验证 | 将复杂的多物体交互分解为可验证的推理步骤，确保轨迹符合物理常识 |

消融实验（Table 4）定量验证了这两个旋钮的因果贡献：在 DragNUWA 基础上单独添加对象感知模块（OPM）使 FVD 从 955.61 降至 857.55，MOC 从 72.09 降至 56.64；进一步叠加 CoT 推理模块后，FVD 进一步降至 771.83，MOC 降至 46.47。两个模块的协同增益（FVD 降低 183.78，MOC 降低 25.62）远大于各自单独贡献之和，表明感知与推理之间存在显著的互补效应——感知为推理提供了必要的输入信息，推理则将感知结果转化为可执行的轨迹预测。

CoT 推理的五阶段设计同样经过严格的消融验证（Table 6）。仅使用第一阶段（场景与对象理解）时，FVD 为 855.31，MOC 为 55.73；逐步添加关系推理（S2）、交互轨迹推理（S3）、迭代排序（S4）和验证（S5）后，性能单调提升至最优值。值得注意的是，S4 到 S5 的增益（FVD 从 779.01 降至 771.83）相对较小，提示迭代排序已能产生较高质量的轨迹，前/后向验证主要起精细化校准作用。

### 适用边界与局限

C-Drag 的训练无关特性既是优势也是约束。优势在于无需针对特定场景微调，可直接利用预训练模型的泛化能力；约束在于其推理质量高度依赖 VLM 的常识覆盖范围。论文自我分析指出，**当轨迹频繁改变方向时，生成结果偶现不稳定**，这可能源于 VLM 对复杂运动模式的推理能力有限。此外，前/后向验证仍基于文本提示的 VLM 判断，缺乏物理方程约束，在极端物理场景（如非牛顿流体、混沌系统）中可能产生不符合严格物理规律的轨迹。

VOI 数据集目前仅包含 72 个视频，覆盖碰撞链式反应、重力与力、杠杆与镜像三类交互。这一规模限制了指标的可泛化性——尚不清楚 C-Drag 在更丰富的交互类型（如水流、布料飘动、柔性物体互动）上的表现。数据集的扩展方向值得关注，但当前结论的泛化边界需要手动验证。

### 开放问题

1. **感知失败的容错机制**：当对象感知模块漏检或误检物体时，CoT 推理能否自行检测异常并请求用户干预，还是会将错误传播至轨迹预测？论文未讨论这一容错问题。

2. **逆向验证的实现细节**：前/后向验证中的“反向工程”具体如何实现？是简单的轨迹反演，还是需要构造额外的逆向推理提示让 VLM 从最终状态推断初始条件？这一机制的透明度影响对方法鲁棒性的判断。

3. **实时交互式扩展**：当前 C-Drag 从第一帧静态图像出发生成整段视频，属于离线生成范式。能否扩展到实时或交互式场景（如用户逐步拖拽、系统即时响应）是一个开放问题，涉及推理延迟与生成效率的权衡。

4. **数据集生态建设**：VOI 数据集未来如何扩充到更多真实场景，并引入更细粒度的标注（如接触力方向、物体材质属性、交互时间戳）？这将直接影响 MOC 指标的评估精度和方法的可改进方向。

## 原文 PDF

![[paperPDFs/arxiv_2025/C_Drag_Chain_of_Thought_Driven_Motion_Controller_for_Video_Generation.pdf]]
