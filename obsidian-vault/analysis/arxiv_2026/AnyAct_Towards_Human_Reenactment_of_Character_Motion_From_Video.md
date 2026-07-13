---
title: "AnyAct: Towards Human Reenactment of Character Motion From Video"
type: paper
paper_level: A
venue: arXiv
year: 2026
pdf_ref: paperPDFs/arxiv_2026/AnyAct_Towards_Human_Reenactment_of_Character_Motion_From_Video.pdf
project_link: null
code_link: null
aliases:
- AnyAct
tags:
- arxiv_2026
- topic/motion_animation
- topic/motion_animation/human_motion_generation
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/image_and_video_generation
- topic/benchmarks_datasets_evaluation
core_operator: 可迁移的局部稀疏2D关节轨迹作为条件信号，驱动人类运动生成
primary_logic: 稀疏局部运动模式在不同身体拓扑间仍保留相似动态趋势，可作为跨结构运动迁移的统一桥接
claims:
- 尽管源角色与人体结构差异巨大，但稀疏局部关节运动仍传达相似的动态倾向
- 仅使用人体运动数据通过增强的3D到2D投影即可训练出有效的运动控制，无需配对的非人视频数据
- 用户研究表明 AnyAct 在重演相似性、运动质量和整体偏好上始终优于基线
- AnyAct benchmark (non-human character videos) 上 MSC = 6.619
---

# AnyAct: Towards Human Reenactment of Character Motion From Video

> [!tip] 核心洞察
> 稀疏局部运动模式在不同身体拓扑间仍保留相似动态趋势，可作为跨结构运动迁移的统一桥接

| 字段      | 内容                                                                                                                                           |
| ------- | -------------------------------------------------------------------------------------------------------------------------------------------- |
| 中文题名    | AnyAct：面向视频中角色运动的人类复现                                                                                                                        |
| 英文题名    | AnyAct: Towards Human Reenactment of Character Motion From Video                                                                             |
| 会议/期刊   | arXiv 2026                                                                                                                                   |
| Links   | [paper](https://arxiv.org/abs/2605.15497) · [Demo](https://www.youtube.com/watch?v=pA14g99KsNY&feature=youtu.be)                             |
| Topic | #topic/motion_animation #topic/motion_animation/human_motion_generation #topic/vision_multimodal_applications #topic/vision_multimodal_applications/image_and_video_generation #topic/benchmarks_datasets_evaluation |
| Method  | AnyAct                                                                                                                                       |
| Dataset | AnyAct benchmark                                                                                                                             |

> [!tip] 效果简介
> - AnyAct benchmark (non-human character videos) 上，MSC 6.619 vs N/A (N/A)；MRC 6.763 vs N/A (N/A)；PA 6.700 vs N/A (N/A)。

## 概要

**问题瓶颈**：现有方法依赖人体中心的结构空间或已知源3D拓扑，无法直接从非人角色视频生成可编辑的人类动作。AnyAct 将这一任务重新定义为**从可迁移的局部稀疏2D关节运动进行条件人体运动生成**，从而绕开了对源角色完整结构的依赖。

**核心洞察**：尽管源角色与人体在整体结构上差异巨大，但稀疏的局部关节运动模式仍保留了相似的动态趋势（Fig. 2）。这一观察构成了跨结构运动迁移的统一桥接——只需捕捉四肢与躯干的局部2D轨迹，即可传达角色的特征运动意图。

**方法定位**：AnyAct 提出了三项关键设计来解决条件歧义与数据缺失问题：
- **人体运动数据纯监督**：通过增强的3D到2D投影，从现有人体运动数据合成条件-运动对，完全避免了对配对非人视频数据的依赖。
- **渐进式3D到2D训练**：先以3D关节序列训练3D Local Adapter，再通过L2对齐损失将其知识蒸馏到2D Local Adapter，缓解了2D条件的歧义性。
- **全局-局部运动解耦**：独立建模全局根轨迹，并通过正交正则化减少全局与局部条件特征之间的纠缠。

**主要结果**：在自建的AnyAct基准（非人角色视频）上，AnyAct 在重演相似性（MSC: 6.619）、运动质量（MRC: 6.763）和整体偏好（PA: 6.700）上均取得领先。用户研究表明，AnyAct 在重演相似性、运动质量和整体偏好上始终优于适配基线 VLM+HY-Motion 和 EchoMotion（Fig. 7）。消融实验验证了3D到2D对齐损失、多模型集成VFE、全局-局部分支解耦及正交正则化各自对性能的关键贡献。

**方法谱系与知识库定位**：AnyAct 处于**跨结构运动重定向**与**条件运动生成**的交汇点。与依赖3D骨骼重建或文本描述的传统方法不同，AnyAct 以稀疏2D关节轨迹作为统一条件信号，使其能够泛化到任意非人角色视频。在技术路线上，它继承并扩展了 ControlNet 式的适配器注入范式，将其应用于运动生成器 MoMask++，同时引入了渐进式知识蒸馏与全局-局部解耦训练策略。相较于 **VLM+HY-Motion**（Wen et al., arXiv 2025）的文本中介方案和 **EchoMotion**（Yang et al., arXiv 2025）的隐式运动迁移，AnyAct 直接利用视觉运动线索，避免了语义损失和结构假设。

### 问题背景：从非人角色视频生成可编辑的人体动作

在动画制作、虚拟现实和游戏开发中，将视频中非人角色的运动“迁移”到人体上是一项常见且耗时的工作。动画师通常需要逐帧手工设计人体动作，使其既保留源角色的动态特征，又符合人体运动学约束。例如，将一只跳跃的袋鼠视频转化为人类舞者的跳跃动作，或让人类模仿企鹅的摇摆步态——这类任务要求生成的动作既能“复现”源运动印象，又具备人体的自然合理性。

现有方法在面对这一任务时存在根本性瓶颈：它们要么依赖**以人体为中心的结构空间**（如重建3D人体骨骼），要么需要**已知的源3D拓扑**作为先验。当输入是任意非人角色的单目视频时——这些角色可能拥有完全不同的肢体数量、关节连接方式和身体比例——传统方法便无法直接适用。文本驱动的运动生成方法虽然灵活，但难以精确描述视频中复杂的时空动态；而基于视频的运动重建方法则受限于人体模板，无法处理非人结构。

### 核心动机：稀疏局部运动作为跨结构迁移的统一桥接

AnyAct 的核心洞察在于：**尽管源角色与人体在完整结构上差异巨大，但稀疏的局部关节运动在不同身体拓扑间仍保留相似的动态趋势**（Fig. 2）。以跳跃袋鼠为例，其腿部关节的周期性屈伸轨迹与人类跳跃时下肢的运动模式存在内在对应关系。这意味着，如果我们能从非人角色视频中提取出这些“可迁移的局部稀疏2D关节轨迹”，就可以将其作为条件信号，驱动人体运动生成器产生自然且符合源动态的人体动作。

这一思路将问题重新定义为：**从视频中提取跨结构可迁移的稀疏运动线索，并将其作为条件输入到人体运动生成模型中**。关键挑战在于：（1）如何从任意非人角色视频中稳定提取稀疏关节轨迹；（2）如何让运动生成器理解这些2D稀疏条件并产生合理的人体运动——尤其是在没有配对视频-运动数据的情况下。

### 现有方法缺口

当前最接近的基线方法存在明显局限：
- **VLM+HY-Motion**（Wen et al., arXiv 2025）：依赖视觉语言模型将视频转化为文本描述，再驱动文本到运动生成。文本描述丢失了精细的时空动态，难以捕捉运动的节奏和幅度细节。
- **EchoMotion**（Yang et al., arXiv 2025）：需要重建3D人体骨骼作为中间表示，无法处理非人角色。
- 直接使用2D条件训练生成器会产生严重的**条件歧义**：同一组2D稀疏点可能对应多种不同的3D人体姿态，导致生成结果不稳定。

AnyAct 通过三个核心设计填补这些缺口：**仅用人体运动数据的增强3D到2D投影监督**、**渐进式3D到2D训练**以消除条件歧义、以及**全局-局部运动解耦**以抑制不可靠的全局根轨迹对局部运动控制的干扰。这使得系统无需任何配对的非人视频-运动数据，即可从单目非人角色视频生成合理的人体重演结果。

## 核心方法与创新机理

AnyAct 的核心创新在于将“从非人角色视频生成可编辑人类动作”这一任务重新定义为**基于可迁移稀疏局部运动线索的条件人体运动生成**问题。与传统依赖人体中心结构空间或已知3D拓扑的方法不同，AnyAct 通过三个关键设计实现了跨结构运动迁移，其相对于基线方法的本质改变体现在以下四个维度。

### 1. 运动条件提取：从结构依赖到拓扑无关的稀疏2D表征

现有方法（如 **VLM+HY-Motion** (Wen et al., arXiv 2025) 和 **EchoMotion** (Yang et al., arXiv 2025)）依赖重建3D人体骨骼或使用文本描述作为运动条件，这要求源角色具备可解析的人体结构或需要额外的语义翻译步骤。AnyAct 从根本上改变了这一范式：**将任意角色统一分解为五个局部组件（四肢+躯干-头部），每个组件至多保留两个关节，缺失关节用零填充**，形成拓扑无关的稀疏2D关节轨迹（Sec. 3.2）。这一设计的核心洞察在于——尽管源角色与人体在完整结构上差异巨大，但稀疏局部运动模式仍传达相似的动态倾向（Fig. 2），从而可作为跨结构运动迁移的统一桥接。

### 2. 训练数据与监督：从配对数据依赖到纯人体运动自监督

基线方法通常需要配对的视频-运动数据来学习条件映射，而非人角色视频的配对数据几乎无法获取。AnyAct 的关键突破在于**仅使用人体运动数据即可训练出有效的运动控制**（Sec. 3.3）。具体而言，通过增强的3D到2D投影（augmented 3D-to-2D projection），将3D人体运动投影到2D平面并转换为与推理时相同的稀疏局部表征，从而构造出条件-运动对。这一策略完全消除了对非人视频配对数据的依赖，是方法可扩展性的核心保障。

### 3. 训练策略：从直接2D条件训练到渐进式3D-to-2D知识蒸馏

直接使用2D条件训练运动生成器会产生严重的条件歧义（2D投影丢失深度信息，同一2D轨迹可能对应多种3D运动）。AnyAct 采用**渐进式3D-to-2D训练**策略（Sec. 3.3）：先以3D关节序列为条件训练3D Local Adapter（3D-LA），再训练2D Local Adapter（2D-LA），并通过L2对齐损失 $\mathcal{L}_{3D} = \| 3D\text{-}LA(J_{3D}) - 2D\text{-}LA(J_{2D}) \|_2$ 将2D分支的输出对齐到更强的3D分支。这实质上是将深度感知的运动知识从3D教师蒸馏到2D学生，有效缓解了2D条件的歧义性。消融实验证实，移除该对齐损失会导致MSC、MRC、PA和HMP全面下降（Table 2a）。

### 4. 全局运动处理：从耦合建模到全局-局部解耦学习

传统方法通常由同一分支同时处理局部和全局运动，导致二者相互纠缠——尤其是在非人角色视频中，全局根轨迹往往与人体运动不兼容。AnyAct 引入**全局-局部解耦学习**（Sec. 3.3）：独立的3D Global Adapter（3D-GA）专门建模全局根轨迹，并通过正交正则化 $\mathcal{L}_{O} = \mathcal{P}(3D\text{-}GA(T), LA(J))$（计算全局与局部条件特征的平方余弦相似度）强制减少二者之间的信息纠缠。消融实验表明，移除全局轨迹分支或冻结其训练会降低运动质量，而添加正交正则化进一步提升了条件跟随和运动质量（Table 2c）。

### 创新总结

AnyAct 的四项 changed slots 构成了一个完整的创新链条：**拓扑无关的稀疏2D表征**解决了“从任意角色提取运动”的问题，**纯人体运动自监督**解决了“无配对数据训练”的问题，**渐进式3D-to-2D蒸馏**解决了“2D条件歧义”的问题，**全局-局部解耦**解决了“运动纠缠”的问题。这些设计共同使得 AnyAct 成为首个无需已知3D拓扑、无需配对非人视频数据即可从任意角色视频生成可编辑人类动作的框架。

AnyAct 将“从非人角色视频驱动人类运动复现”建模为一个条件运动生成问题。其核心流程如 Fig. 3 所示，由三个关键阶段构成：**运动线索提取**、**运动条件学习**（仅发生在训练阶段）和**条件运动生成**。

![[assets/figures/papers/paper_list_l89_https_arxiv_org_abs_2605_15497/figures/003_Figure_3.jpg]]
*Figure 3: Given reference videos of characters, AnyAct first extracts local sparse 2D joint trajectories as transferable motion cues from the input video using our model-ensemble-based Versatile Feature Extractor (VFE). These cues are then injected into a human motion generator (MoMask++) through the ControlNet-like 2D Local Adapter (2D-LA) to produce the initial human reenactments that follow the observed character dynamics*

### 输入与输出

- **输入**：一段包含任意非人角色（如袋鼠、企鹅、蝴蝶、机械蜘蛛等）的单目视频。源角色可能具有与人体截然不同的骨骼拓扑和外观。
- **输出**：一段由人体骨骼驱动、保留了源视频核心动态印象的 3D 人体运动序列。AnyAct 不追求逐帧结构重建，而是生成“像该角色一样运动”的合理人体动作。

### 流水线总览

**阶段一：通用特征提取 (Versatile Feature Extractor, VFE)**
VFE 从输入视频中提取**局部稀疏 2D 关节轨迹**作为可迁移的运动线索（Sec. 3.2）。具体而言，VFE 将任意角色分解为五个局部组件（四肢 + 躯干-头部），每个组件最多保留两个关节，缺失关节以零填充。这种统一表示屏蔽了源拓扑差异，仅保留局部运动动态。VFE 采用多模型集成策略（如 ViTPose++ 等），以适应不同角色外观下的关键点检测鲁棒性。

**阶段二：运动条件学习 (Motion Condition Learning)**
这是 AnyAct 的核心训练机制（Sec. 3.3, Fig. 4），其目标是仅使用**人体运动数据**训练出可靠的条件控制能力，而无需任何配对的非人视频-人体运动数据。该阶段包含三个关键设计：

1. **增强 3D 到 2D 投影 (Augmented 3D-to-2D Projection)**：从 3D 人体运动数据出发，将其投影到 2D 平面并转换为与推理时一致的稀疏局部表示，同时施加增强（如视角变化、噪声），构造出“条件-运动”训练对。
2. **渐进式 3D 到 2D 训练 (Progressive 3D-to-2D Training)**：先以 3D 关节序列为条件训练 3D Local Adapter (3D-LA)，再训练 2D Local Adapter (2D-LA)，并通过 L2 对齐损失 $\mathcal{L}_{3D} = \| 3D\text{-}LA(J_{3D}) - 2D\text{-}LA(J_{2D}) \|_2$ 使 2D 分支的输出逼近更强的 3D 分支，传递深度感知运动知识，缓解 2D 条件的歧义性。
3. **全局-局部解耦学习 (Global-Local Decoupled Learning)**：引入独立的 3D Global Adapter (3D-GA) 建模根轨迹，通过正交正则化 $\mathcal{L}_{O}$（计算全局与局部条件特征间的平方余弦相似度）减少全局与局部运动的纠缠，确保局部运动控制不受不可靠的全局位移干扰。

**阶段三：条件运动生成**
推理时，VFE 提取的稀疏 2D 轨迹 $J$ 经 2D Local Adapter (2D-LA) 编码后，注入到基础人体运动生成器 **MoMask++** 中，生成遵循源角色动态的初始人体复现动作。全局轨迹由 3D-GA 独立处理，最终与局部运动组合输出完整的人体运动序列。

### 模块关系总结

| 模块 | 阶段 | 功能 |
|------|------|------|
| VFE | 训练+推理 | 从视频提取统一稀疏 2D 关节轨迹 |
| 3D-LA | 仅训练 | 以 3D 关节为条件，教授 2D 适配器 |
| 2D-LA | 训练+推理 | 编码稀疏 2D 条件并注入生成器 |
| 3D-GA | 训练+推理 | 建模全局根轨迹，解耦局部运动 |
| MoMask++ | 训练+推理 | 基础人体运动生成器 |

整个框架的关键瓶颈突破在于：**稀疏局部运动模式在不同身体拓扑间仍保留相似动态趋势**（Fig. 2 提供了袋鼠跳跃与人工设计的人类复现之间的局部关节轨迹对比证据），AnyAct 正是利用这一洞察，将跨结构运动迁移统一为“从稀疏 2D 局部轨迹到人体运动”的条件生成问题。

![[assets/figures/papers/paper_list_l89_https_arxiv_org_abs_2605_15497/figures/001_Figure_1.jpg]]
*Figure 1: Human reenactment from reference videos. Given monocular videos of non-human characters with diverse topologies, AnyAct reinterprets their characteristic motion patterns as plausible human performances rather than reproducing their source structures literally. Shown here are reenactments of (a) kangaroo-like jumping, (b) butterfly-like wing flapping, and (c) the periodic paw motion of a beckoning cat*

AnyAct 的核心设计围绕一个中心命题展开：**稀疏局部2D关节轨迹可作为跨结构运动迁移的统一桥接**。尽管源角色（如袋鼠、蝴蝶、企鹅）与人体在全局骨骼拓扑上差异巨大，但其局部肢体的运动模式仍保留了相似的动态趋势（Fig. 2）。基于这一洞察，AnyAct 将“从非人角色视频生成可编辑的人类动作”这一任务，形式化为**以可迁移稀疏局部运动线索为条件的条件人体运动生成**。

### 2.1 通用特征提取器 (VFE)

推理时，系统首先通过**通用特征提取器 (Versatile Feature Extractor, VFE)** 从任意角色的单目视频中提取统一的稀疏2D关节轨迹 $J = \{ j_n \}_{n=1}^N$。VFE 采用模型集成策略，将每种角色拓扑分解为五个局部组件（四肢 + 躯干-头部段），每个组件最多保留两个关节，缺失关节以零填充。这种统一的稀疏表示屏蔽了源拓扑的差异性，为下游生成器提供了结构无关的运动条件信号。

### 2.2 渐进式3D到2D训练

运动条件学习是 AnyAct 的技术瓶颈所在。直接以推理时的稀疏2D条件训练生成器，会因深度信息的固有缺失而产生严重的条件歧义。AnyAct 的解决方案是**渐进式3D到2D训练 (Progressive 3D-to-2D Training)**，其核心机制是让一个更强的3D条件分支“教授”2D条件分支。

训练分为两个阶段：

**阶段一：3D训练。** 同时训练**3D局部适配器 (3D-LA)** 和**3D全局适配器 (3D-GA)**。3D-LA 以归一化的3D关节序列为条件，3D-GA 以全局根轨迹 $T$ 为条件，二者联合优化，总损失为：

$$
\mathcal{L}_{\mathrm{Total-3D}} = \mathcal{L}_{\mathrm{MoMask++}} + \lambda_1 \mathcal{L}_{O} \tag{3}
$$

**阶段二：2D训练。** 冻结3D-LA，训练**2D局部适配器 (2D-LA)** 并继续优化3D-GA。此时引入关键的**3D到2D对齐损失**，强制2D-LA的输出逼近3D-LA的输出，从而将深度感知的运动知识从3D分支蒸馏到2D分支：

$$
\mathcal{L}_{3D} = \| 3D\text{-}LA(J_{3D}) - 2D\text{-}LA(J_{2D}) \|_2 \tag{1}
$$

2D训练阶段的总损失为：

$$
\mathcal{L}_{\mathrm{Total-2D}} = \mathcal{L}_{\mathrm{MoMask++}} + \lambda_1 \mathcal{L}_{O} + \lambda_2 \mathcal{L}_{3D} \tag{4}
$$

其中 $\mathcal{L}_{\mathrm{MoMask++}}$ 为基础运动生成器 MoMask++ 的重建损失，$\lambda_1$ 和 $\lambda_2$ 为平衡系数。

### 2.3 全局-局部解耦学习

为避免不可靠的全局根运动对局部条件学习的干扰，AnyAct 引入**全局-局部解耦学习 (Global-Local Decoupled Learning)**。3D-GA 独立处理全局轨迹 $T$，与局部适配器 $LA(J)$ 形成双分支结构。为减少两者特征空间中的纠缠，施加**正交正则化**，计算全局与局部条件特征之间的平方余弦相似度：

$$
\mathcal{L}_{O} = \mathcal{P}(3D\text{-}GA(T), LA(J)) \tag{2}
$$

该正则化鼓励全局与局部表征尽可能正交，使局部适配器专注于肢体动态的复现，而全局适配器负责人体兼容的位移轨迹。

### 2.4 增强的3D到2D投影

上述训练流水线完全依赖**人体运动数据**，无需任何配对的非人角色视频。具体而言，系统从3D人体运动数据出发，通过增强的3D到2D投影（Augmented 3D-to-2D Projection）构造条件-运动对：将3D人体运动投影到2D平面，转换为与推理时相同的稀疏局部表示，并施加数据增强以提升泛化性。这一设计使得 AnyAct 的训练完全规避了对稀缺配对数据的依赖。

**推理时**，VFE 提取的稀疏2D轨迹 $J_{2D}$ 直接输入训练好的2D-LA，其输出注入冻结的 MoMask++ 生成器，产生保留源角色动态印象的人体运动序列。

## 实验与关键发现

### 主结果：跨结构重演能力

AnyAct 在自建的 AnyAct benchmark（包含多种非人角色视频）上进行了定量评估，采用四项指标：运动相似性（MSC）、重演一致性（MRC）、物理合理性（PA）和人体运动先验（HMP）。如 Table 1 所示，AnyAct 在 MSC（6.619）、MRC（6.763）和 PA（6.700）三项核心指标上均取得最优结果，验证了稀疏 2D 局部运动线索作为跨结构桥接的有效性。在 HMP 指标上，AnyAct 得分为 9.056，略低于 **VLM+HY-Motion**（Wen et al., arXiv 2025）的 9.181（差距 -0.125），这表明基于文本描述的方法在人体运动先验的自然度上略有优势，但 AnyAct 在重演相似性和物理一致性上的领先幅度更为显著。

![[assets/figures/papers/paper_list_l89_https_arxiv_org_abs_2605_15497/figures/008_Table_1.jpg]]
*Table 1: Quantitative comparison of AnyAct with baselines adapted to our setting.The best and second-best results are shown in bold and underline, respectively*

定性对比（Fig. 6）进一步支持这一结论：在怪物飞行、卡通熊跳跃、企鹅行走和兔子跳跃等场景中，AnyAct 生成的人体动作既保留了源角色的动态特征，又维持了人体运动的合理性，而 **EchoMotion**（Yang et al., arXiv 2025）和 VLM+HY-Motion 分别在运动跟随和物理可信度上出现明显退化。

![[assets/figures/papers/paper_list_l89_https_arxiv_org_abs_2605_15497/figures/006_Figure_6.jpg]]
*Figure 6: Qualitative comparison of AnyAct against VLM+HY-Motion and EchoMotion. Based on the reference videos, human should perform: (1) monster-like flying, (2) cartoon bear-like jumping, (3) penguin-like walking, and (4) rabbit-like bounding. The results demonstrate that our method achieves superior reenactment quality compared to the other two baselines, while preserving the plausibility of the motion*

用户研究（Fig. 7）提供了更强的主观证据：在重演相似性、运动质量和整体偏好三项评判中，AnyAct 对 VLM+HY-Motion 和 EchoMotion 的偏好率均持续领先，表明人类评估者一致认可 AnyAct 的跨结构重演效果。

![[assets/figures/papers/paper_list_l89_https_arxiv_org_abs_2605_15497/figures/007_Figure_7.jpg]]
*Figure 7: Result of the user study. We report the preference rates of our Any-Act in pairwise comparisons against (a) VLM+HY-Motion and (b) EchoMotion. Participants evaluated the generated motions based on Reenactment Similarity, Motion Quality, and Overall Preference, respectively. Our method consistently outperforms both baselines across all criteria*

### 消融实验：核心设计的因果验证

Table 2 的系统消融揭示了三个关键设计的独立贡献：

![[assets/figures/papers/paper_list_l89_https_arxiv_org_abs_2605_15497/figures/009_Table_2.jpg]]
*Table 2: Ablation study of core designs in AnyAct. We evaluate various core design choices of our AnyAct across multiple VLM-based and physical metrics. The best and second-best scores for each metric are bolded and underlined, respectively*

**渐进式 3D-to-2D 训练。** 移除 3D-to-2D 对齐损失 $ \mathcal{L}_{3D} $（即 w/o $ \mathcal{L}_{3D} $）导致四项指标全面下降：MSC 从 6.619 降至 6.344，MRC 从 6.763 降至 6.513，PA 从 6.700 降至 6.444，HMP 从 9.056 降至 8.681。这一退化证实了 $ \mathcal{L}_{3D} $ 所传递的深度感知运动知识对于弥合 2D 条件歧义至关重要——仅靠 2D 投影训练无法从稀疏轨迹中恢复可靠的三维运动控制。

**多模型集成的 VFE。** 将 VFE 替换为单一姿态估计器（仅 ViTPose++）后，所有指标均出现下降，验证了模型集成策略的必要性。单一估计器在面对多样化的非人角色拓扑时，其关键点预测的覆盖率和精度不足，导致提取的稀疏关节轨迹质量下降，进而损害下游运动生成。

**全局-局部解耦学习。** 移除全局轨迹分支或冻结其训练会降低运动质量，而添加正交正则化 $ \mathcal{L}_{O} $ 则进一步提升了条件跟随和运动质量。这表明：将全局根轨迹与局部运动解耦，并通过平方余弦相似度约束二者特征正交，能有效抑制不可靠的全局位移对局部运动控制的干扰，是实现可靠重演的关键机制。

### 失败模式与局限性

AnyAct 在以下两类场景中表现受限（Fig. 12）：

1. **分布外运动。** 对于训练分布之外的罕见动作——如蛙泳中涉及快速腿部蹬踢和罕见的俯卧姿态——AnyAct 无法生成合理的人体重演。这是因为基础运动生成器 MoMask++ 的训练数据未覆盖此类极端姿态，稀疏 2D 条件无法引导模型外推到未见运动模式。

2. **运动线索提取失效。** 在快速运动或视觉相似点密集的场景（如螃蟹侧向行走的多足快速移动），CoTracker3 的跟踪会失败，产生噪声 2D 特征，进而损害后续运动生成。这一瓶颈源于底层跟踪器对像素级歧义的敏感性，而非 AnyAct 框架本身的设计缺陷。

此外，AnyAct 生成的人体动作仅保留源视频的动态印象，无法保证逐帧精确对齐——这是稀疏局部运动桥接方案的固有权衡：以精确重建为代价换取跨结构的泛化能力。

## 定位与知识库关联

### 核心贡献与因果机制

AnyAct 的核心贡献在于将“非人角色视频驱动的人体重演”重新定义为**以可迁移稀疏局部2D运动线索为条件的运动生成问题**。这一建模选择的因果逻辑是：尽管源角色与目标人体在完整骨骼拓扑上差异巨大，但局部稀疏关节的运动模式（如四肢的摆动频率、躯干的起伏节奏）在不同身体结构间仍保留相似的动态趋势（Fig. 2）。因此，稀疏局部2D关节轨迹可以充当跨结构运动迁移的统一桥接，使系统无需理解源角色的完整3D结构即可提取有效的运动控制信号。

在此基础上，AnyAct 通过三个关键设计解决了从2D稀疏条件中学习可靠运动控制的瓶颈：
1. **仅使用人体运动数据的监督**：通过增强的3D到2D投影，从现有人体运动数据库自动构造条件-运动配对，无需任何配对的非人角色视频-人体动作数据（Sec. 3.3）。
2. **渐进式3D到2D训练**：先训练以3D关节序列为条件的3D Local Adapter（3D-LA），再通过L2对齐损失 $\mathcal{L}_{3D} = \| 3D\text{-}LA(J_{3D}) - 2D\text{-}LA(J_{2D}) \|_2$ 将其深度感知运动知识迁移至2D Local Adapter（2D-LA），缓解了纯2D条件训练的歧义性（Eq. 1）。
3. **全局-局部运动解耦**：独立的全局适配器处理根轨迹，并通过正交正则化 $\mathcal{L}_{O}$（平方余弦相似度）减少全局与局部条件特征之间的纠缠，避免不可靠的2D全局轨迹污染局部运动生成（Eq. 2）。

### 方法对比与知识库定位

AnyAct 的方法定位可以从以下维度与现有工作区分：

| 维度 | 现有主流方法 | AnyAct |
|------|-------------|--------|
| **输入条件** | 人体中心的结构空间（如3D骨骼、SMPL参数）或文本描述 | 统一稀疏2D关节轨迹（5个局部组件，最多2个关节，零填充缺失关节） |
| **训练数据需求** | 需要配对视频-运动数据或已知源3D拓扑 | 仅需人体运动数据（通过增强3D到2D投影自监督构造条件-运动对） |
| **跨结构泛化** | 依赖源角色与目标人体的显式结构对应 | 通过稀疏局部运动模式的动态相似性实现隐式迁移 |
| **全局运动处理** | 局部与全局运动由同一分支处理 | 全局-局部解耦学习，正交正则化减少纠缠 |

与论文中对比的两个基线方法相比：
- **VLM+HY-Motion**（Wen et al., arXiv 2025）：依赖视觉语言模型从视频中提取文本描述，再通过文本驱动人体运动生成。该管线在跨结构迁移时存在信息损失，文本描述难以精确捕捉细粒度运动动态。
- **EchoMotion**（Yang et al., arXiv 2025）：依赖重建3D人体骨骼作为条件。当输入为非人角色视频时，3D人体重建本身就是一个极具挑战的中间任务，容易引入级联误差。

AnyAct 避开了上述瓶颈，直接以稀疏2D轨迹为条件，从信号源头消除了对源角色结构重建的依赖。用户研究（Fig. 7）表明，AnyAct 在重演相似性、运动质量和整体偏好上始终优于这两个基线。

### 适用边界与局限

AnyAct 的适用边界由以下因素共同决定：

1. **运动分布覆盖**：AnyAct 的运动生成能力受限于基础人体运动生成器 MoMask++ 的训练分布。对于训练分布之外的罕见动作（如蛙泳涉及的快速腿部蹬踢和罕见俯卧姿态），系统无法生成合理的人体重演（Fig. 12 左）。这是方法层面的根本性限制，而非简单的数据增强可解决。

2. **2D特征提取鲁棒性**：Versatile Feature Extractor (VFE) 依赖 CoTracker3 进行点跟踪。在快速运动或视觉相似点密集的场景（如螃蟹式侧向行走的多腿快速交替），CoTracker3 跟踪可能失败，产生噪声2D特征，进而损害后续运动生成质量（Fig. 12 右）。该失效模式与输入视频的视觉特性强相关，属于推理阶段的脆弱环节。

3. **动态印象 vs. 精确对齐**：AnyAct 生成的本质是“保留动态印象的人体演绎”，而非逐帧精确复现。系统不保证生成动作与源视频的帧级对齐，这一定位在论文中被明确表述为设计选择而非缺陷，但对于需要精确时空对齐的应用场景（如动作分析、生物力学研究）不适用。

4. **全局轨迹的可靠性**：尽管全局-局部解耦设计通过正交正则化减少了纠缠，但2D全局轨迹本身携带的噪声和歧义性在极端视角或遮挡下仍可能影响最终生成质量。消融实验（Table 2c）表明，移除全局轨迹分支或冻结其训练会降低运动质量，但当前方法并未从根本上解决2D全局轨迹的可靠性问题。

### 开放问题

1. **如何扩展运动覆盖范围？** 当前方法受限于基础运动生成器的训练分布。一个关键开放问题是：能否在不重新训练整个生成器的前提下，通过适配器层面的增量学习或条件空间的域外推，使系统泛化至蛙泳、蟹行等训练分布外动作？

2. **如何提高运动线索提取的鲁棒性？** CoTracker3 在快速运动和局部视觉相似性场景下的失效是当前管线的薄弱环节。可能的改进方向包括：引入多帧时序一致性约束、融合多模态特征（如光流、深度估计）增强跟踪稳定性，或设计针对跟踪失败的检测与回退机制。

3. **如何实现可控的精确对齐？** 当前方法定位为“动态印象迁移”，但某些应用场景可能需要更强的帧级对齐能力。是否可以在保持跨结构泛化优势的前提下，引入可选的时序对齐约束或后处理优化步骤，使用户可以在“印象迁移”和“精确对齐”之间按需调节？

## 原文 PDF

![[paperPDFs/arxiv_2026/AnyAct_Towards_Human_Reenactment_of_Character_Motion_From_Video.pdf]]
