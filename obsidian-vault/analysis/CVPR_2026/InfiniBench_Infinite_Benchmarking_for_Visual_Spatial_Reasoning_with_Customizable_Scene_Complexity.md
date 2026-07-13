---
title: "InfiniBench: Infinite Benchmarking for Visual Spatial Reasoning with Customizable Scene Complexity"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/InfiniBench_Infinite_Benchmarking_for_Visual_Spatial_Reasoning_with_Customizable_Scene_Complexity.pdf
project_link: null
code_link: "https://github.com/pittisl/infinibench"
huggingface_link: "https://huggingface.co/datasets/Haoming645/infinibench"
aliases:
- InfiniBench
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
- topic/benchmarks_datasets_evaluation
core_operator: 通过自然语言参数化独立控制场景的组成复杂度（对象数量与种类）、关系复杂度（空间排列与占用率）和观测复杂度（视角与遮挡），实现各维度解耦，从而精确分离VLM在不同空间条件下的失败原因。
primary_logic: 将LLM的高层语义理解（约束生成与CoT迭代精炼）与基于可移动簇的优化引擎相结合，生成物理合理的高密度3D场景；同时引入面向任务的相机轨迹优化，确保VLM输入中所有任务相关对象完整可见。
claims:
- InfiniBench在多个复杂度维度上同时实现高提示保真度（Fidelity）和接近完美的物理合理性（低碰撞/出界），在高对象数量和高房间占用率场景下显著超越LLM布局方法与过程化方法。
- 基于可移动簇的布局优化使生成以往层次化方法不可能的高密度场景成为现实，如图6(b)所示。
- 迭代式LLM约束生成与CoT反馈循环可在5次迭代内收敛，联合簇优化将基础优化器的Fidelity从0.64提升至0.92，证实各模块的协同作用。
- 高对象数量场景 上 Fidelity (提示保真度) = 0.98
---

# InfiniBench: Infinite Benchmarking for Visual Spatial Reasoning with Customizable Scene Complexity

> [!tip] 核心洞察
> 将LLM的高层语义理解（约束生成与CoT迭代精炼）与基于可移动簇的优化引擎相结合，生成物理合理的高密度3D场景；同时引入面向任务的相机轨迹优化，确保VLM输入中所有任务相关对象完整可见。

| 字段 | 内容 |
|------|------|
| 中文题名 | InfiniBench：可定制场景复杂度的无限视觉空间推理基准生成器 |
| 英文题名 | InfiniBench: Infinite Benchmarking for Visual Spatial Reasoning with Customizable Scene Complexity |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2511.18200) · [Code](https://github.com/pittisl/infinibench) · [HuggingFace](https://huggingface.co/datasets/Haoming645/infinibench) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction #topic/benchmarks_datasets_evaluation |
| Method | InfiniBench |
| Dataset | InfiniBench |
> [!tip] 效果简介
> - 高对象数量场景 上，Fidelity (提示保真度) 0.98 vs 0.93 (LayoutGPT) (+0.05)；Collision pairs (#CN) 0.0 vs 13.5 (LayoutGPT) (-13.5)。
> - 高房间占用率场景 上，Fidelity 0.91 vs 0.49 (Infinigen) (+0.42)；Collision pairs (#CN) 0.1 vs 9.6 (LayoutGPT) (-9.5)。

## 概要

视觉语言模型（VLM）在空间推理任务上的评估长期受制于基准的静态性与不可控性——现有数据集场景固定、复杂度维度耦合，难以精细诊断模型在不同空间条件下的失败模式。InfiniBench 提出了一种全自动、可定制的基准生成器，将自然语言场景描述转化为物理合理的高保真3D视频，并首次实现对**组成复杂度**（对象数量与种类）、**关系复杂度**（空间排列与占用率）和**观测复杂度**（视角与遮挡）三个维度的独立参数化控制。

该方法的核心洞察在于将大语言模型（LLM）的高层语义理解与基于可移动簇的优化引擎深度耦合：LLM智能体通过思维链（CoT）推理和迭代反馈生成过程化约束，簇优化器则突破传统层次化布局在高密度场景下的可解性瓶颈，生成物理合理的复杂3D布局。同时，任务感知的相机轨迹优化确保所有任务相关对象完整可见，消除观测偏差对VLM评估的干扰。

实验表明，InfiniBench在场景生成质量上显著超越现有方法：在高对象数量场景下，提示保真度（Fidelity）达0.98，碰撞对数为0；在高房间占用率场景下，Fidelity达0.91，较过程化框架Infinigen（0.49）提升86%。消融实验进一步证实，LLM约束精炼与簇优化的协同作用将基础优化器的Fidelity从0.64提升至0.92，且精炼过程通常在5次迭代内收敛。基于该生成器构建的可控基准已初步揭示VLM在不同复杂度维度下的差异化失效模式，为空间推理能力的深入诊断提供了系统化工具。



视觉语言模型（VLM）在空间推理任务上的能力评估正面临一个根本性瓶颈：现有基准既无法精细控制场景复杂度，也不具备无限扩展能力。真实世界的空间推理涉及三个相互交织的复杂度维度——**组成复杂度**（场景中有多少对象、种类如何）、**关系复杂度**（对象之间的空间排列与占用率）和**观测复杂度**（视角、遮挡程度）。当VLM在这些维度上表现退化时，我们难以判断失败究竟源于对象计数的误差、空间关系推理的缺陷，还是观测条件的不利——因为现有基准将这三个维度混为一谈，缺乏解耦控制。

更关键的是，现有3D场景生成方法在支撑高复杂度基准构建时存在结构性缺陷。**基于LLM的布局生成器**（如LayoutGPT、Holodeck、I-Design）虽然能理解自然语言提示，但直接生成的布局频繁出现物理冲突和逻辑矛盾——对象穿模、悬浮、越界等问题在高对象数量下急剧恶化（Figure 2）。**过程化生成框架**（如Infinigen、Luminous）虽能保证物理合理性，但其层次化优化策略（先固定大物体，后放置小物体）在高房间占用率场景下会陷入无可解状态——大物体占据空间后，小物体无处安放，导致提示保真度崩溃。正如Figure 6所示，同一房间模板和资产参数下，传统层次化方法完全无法生成高密度场景，而InfiniBench的簇优化策略能成功实现。

观测层面的问题同样严峻。现有相机路径生成方法——无论是基于优化的方法（计算开销大）、生成式方法（缺乏多对象覆盖），还是强化学习方法（需逐场景重训）——都无法在可接受的时间内为包含大量任务相关对象的场景生成确保全覆盖的相机轨迹。错误的视点选择会直接遮蔽空间推理所需的关键信息（Figure 3），使得即使场景布局完美，VLM也无法正确作答。

上述缺口共同指向一个核心矛盾：**现有方法无法在高复杂度下同时保证提示一致性、物理合理性和观测完整性**。这一矛盾催生了InfiniBench的设计动机——构建一个能通过自然语言参数化独立控制三个复杂度维度、理论上可生成无限变体的基准生成器，从而将VLM空间推理能力的诊断从“黑盒测试”推进到“受控实验”的层面。



## 核心方法与创新机理

InfiniBench 的核心创新在于首次将**自然语言驱动的场景复杂度解耦控制**、**基于可移动簇的高密度布局优化**以及**任务感知的相机轨迹优化**整合为一个全自动的基准生成管线，从而突破了现有 3D 场景生成方法在复杂场景下**提示一致性**与**物理合理性**无法兼得的瓶颈。

### 创新一：自然语言参数化的复杂度解耦控制

现有 VLM 空间推理基准（如 **Infinigen**、**Luminous** 等过程化框架，以及 **LayoutGPT**、**Holodeck**、**I-Design** 等基于 LLM 的布局生成器）要么依赖手动编写约束，要么由 LLM 直接生成最终布局，前者扩展性差，后者在高复杂度下易产生物理冲突与逻辑矛盾。InfiniBench 改变了这一范式：它引入 **LLM Agentic Constraint Refiner**（LLM 智能体约束精炼器），将自然语言场景描述翻译为过程化约束，并通过**迭代反馈与 Chain-of-Thought（CoT）推理**解决冲突，实现了高层语义规划与低层物理执行的分离。

具体而言，该智能体框架（Figure 4）在每次迭代中生成场景约束，交由布局优化器尝试实例化；若优化器返回错误报告（如碰撞、空间不足），智能体则基于 CoT 推理分析失败原因并修正约束。这一闭环机制使得 InfiniBench 能够通过自然语言**独立参数化控制**三个复杂度维度：
- **组成复杂度**：对象数量与种类
- **关系复杂度**：空间排列与房间占用率
- **观测复杂度**：相机视角与遮挡程度

这种解耦控制是准确诊断 VLM 在不同空间条件下失败模式的前提，也是现有基准所不具备的能力。

### 创新二：基于可移动簇的布局优化引擎

传统 3D 场景布局优化方法（如 Infinigen 内置的层次化优化器）采用“先固定大物体、后放置小物体”的策略。这在低复杂度场景下可行，但在高对象数量或高房间占用率场景下，大物体的固定位置会严重压缩小物体的可用空间，导致优化器陷入**无可解状态**。

InfiniBench 提出的 **Cluster-based Layout Optimizer**（基于可移动簇的布局优化器）从根本上改变了这一策略。该方法将语义关联的对象（如“餐桌+所有椅子”）视为一个**可移动簇**，允许整个簇在房间内进行平移和旋转，并以簇为单位进行碰撞检测（Figure 5）。这一设计使优化器能够探索更大的解空间：当初始布局无效时，优化器可以整体移动簇而非仅调整单个对象，从而找到物理合理的布局。

该创新的决定性证据来自高复杂度场景对比（Figure 6）：在相同房间形状和资产参数下，层次化优化完全无法生成有效布局，而簇优化成功生成了**以往方法不可能实现的高密度场景**。定量结果（Table 2）进一步证实：在高房间占用率场景下，InfiniBench 的 Fidelity 达 0.91，远超 Infinigen 原始优化器的 0.49；碰撞对数（#CN）仅为 0.1，而 LayoutGPT 高达 9.6。

### 创新三：任务感知的相机轨迹优化

现有相机轨迹生成方法存在各自局限：基于优化的方法计算开销大，生成式方法缺乏多对象覆盖，强化学习方法需逐场景重训。InfiniBench 的 **Camera Trajectory Optimizer**（相机轨迹优化器）针对 VLM 空间推理评测的特殊需求，提出了**任务感知的最短路径规划**。

该优化器首先基于多标准（如目标对象可见性、视角多样性、遮挡程度）采样候选视点，然后通过快速遮挡检测（利用 Trimesh/PyRender）筛选出能确保**所有任务相关对象无遮挡、完整可见**的视点，最后求解连接这些视点的最短路径（Figure 7, Figure 8）。这一设计直接回应了 VLM 评测中的关键问题：若相机未能完整捕捉任务相关对象，VLM 的推理失败将无法被正确归因（Figure 3 展示了错误视点遮蔽关键信息的典型问题）。

### 模块协同与消融验证

上述三个创新并非孤立存在，而是通过**迭代反馈循环**形成协同增益。消融实验（Table 3）揭示了这一协同效应的强度：
- 仅使用基础优化器（Infinigen 原始优化器）时，Fidelity 仅为 0.64
- 单独添加 LLM 约束精炼模块后，Fidelity 提升至 0.82
- 单独使用簇优化（无 LLM 精炼）时，Fidelity 为 0.79
- **完整 InfiniBench（LLM 精炼 + 簇优化）的 Fidelity 达 0.92**，显著高于各模块独立使用之和

此外，约束精炼的迭代效率也得到验证（Table 4）：Fidelity 在 5 次迭代内收敛至 0.92，10 次迭代无进一步提升，表明该框架在保证质量的同时具备良好的计算效率。



InfiniBench 构建了一条从自然语言场景描述到可无限扩展的视觉空间推理基准的自动化流水线。其核心设计理念是将**高层语义理解**与**低层物理优化**相分离，并通过三个紧密协作的模块实现对场景组成复杂度（对象数量与种类）、关系复杂度（空间排列与占用率）和观测复杂度（视角与遮挡）的独立、精细控制。

流水线的输入仅为一段自然语言描述（如“生成一个可容纳10人以上就餐的餐厅”），输出是一组物理合理的高保真3D场景视频，可直接用于VLM的空间推理能力诊断。整个过程由四个核心模块串联完成，其逻辑关系如Figure 4所示。

### 模块协作与数据流

1.  **LLM Agentic Constraint Refiner（约束生成与精炼）**
    该模块作为流水线的入口，接收用户的自然语言提示。它基于LLM智能体框架，将场景描述翻译为过程化的场景约束（如对象类型、数量、空间关系、房间占用率等）。关键创新在于其**迭代反馈机制**：生成的约束首先交由下游布局优化器尝试实例化；若优化器返回冲突报告（如物理碰撞、空间不足），LLM智能体将基于思维链（CoT）推理进行自我修正，重新生成约束。这一循环通常在5次迭代内收敛，将高层规划与低层执行的矛盾在生成阶段即被消解。

2.  **Cluster-based Layout Optimizer（布局优化）**
    精炼后的场景约束被送入此模块，负责在3D空间中生成物理合理的最终布局。与传统的层次化优化（先固定大物体，后放置小物体）不同，该模块采用**基于可移动簇的优化策略**：将具有空间关联的对象（如桌子与环绕的椅子）编组为“簇”，并作为整体进行平移、旋转和碰撞检测。这一机制使优化器能够探索更大的解空间，从而生成以往方法无法实现的高密度场景。

3.  **Camera Trajectory Optimizer（相机轨迹优化）**
    在场景布局确定后，此模块根据具体的空间推理任务，生成一条最优相机轨迹。其目标是找到一条**最短路径**，同时确保路径上每个视点都能对任务相关的所有目标对象提供**无遮挡、完整且清晰**的观测。该模块通过基于前沿探索的视点采样与遮挡检查实现，避免了传统优化方法的高计算开销和生成式方法对多对象覆盖的不足。

4.  **Photorealistic Rendering Pipeline（真实感渲染）**
    流水线的最终环节。该模块沿优化后的相机轨迹，利用Blender Cycles引擎进行高质量真实感渲染，生成用于VLM评估的视频帧。同时，在视点采样阶段，系统会调用Trimesh/PyRender进行快速遮挡检测，以加速相机轨迹的优化过程。

### 关键设计优势

这种模块化流水线的核心优势在于**各复杂度维度的解耦控制**。用户通过自然语言即可独立调节场景的组成、关系或观测复杂度，而无需介入任何底层参数。例如，仅改变提示中的对象数量即可生成不同组成复杂度的场景，而房间布局与相机路径则由后续模块自动适配，确保生成的场景在物理合理性和任务相关性上均保持高保真度。这一设计使得对VLM失败模式的细粒度诊断成为可能——研究者可以精确分离出模型性能下降是由对象数量增加、空间拥挤度提高，还是由观测视角恶化所导致。



### 3.1 LLM智能体约束精炼器 (LLM Agentic Constraint Refiner)

InfiniBench的核心创新之一是将高层语义理解与低层执行彻底解耦。该模块将用户以自然语言描述的场景（例如“一个30平方米、配有10把不同类型椅子的餐厅”）翻译为过程化约束（procedural constraints），而非直接生成最终布局。其工作流程构成一个闭环迭代系统：

1. **初始约束生成**：LLM智能体根据场景描述，生成一组初始的过程化约束，包括对象类型、数量、空间关系等。
2. **布局尝试与错误报告**：生成的约束被送入基于簇的布局优化器（见3.2节）尝试实现。若优化失败（例如无法在给定空间内无冲突地放置所有对象），优化器会返回详细的错误报告，指明冲突对象与失败原因。
3. **CoT反馈与约束精炼**：LLM智能体接收错误报告后，通过思维链（Chain-of-Thought, CoT）推理分析冲突根源，并修正约束条件（例如调整对象尺寸、替换对象类型或改变空间关系），生成新一组约束。
4. **迭代收敛**：该“生成-尝试-反馈-修正”循环重复执行，直至布局优化器成功生成物理合理的场景。实验表明，该精炼过程通常在5次迭代内收敛，将基础优化器的提示保真度从0.64提升至0.92（Table 3, Table 4）。

这一设计的关键优势在于，LLM仅需在符号化的约束空间中进行推理，避免了直接输出连续空间坐标时常见的物理冲突与逻辑矛盾（如Figure 2所示）。

### 3.2 基于可移动簇的布局优化器 (Cluster-based Layout Optimizer)

传统层次化布局方法（如Infinigen的原生优化器）遵循“先放置大物体，后放置小物体”的固定顺序。一旦大物体占据了关键空间，后续小物体可能陷入无解状态，这在高密度场景下尤为致命（Figure 5/6）。

![[assets/figures/papers/paper_list_l2085_https_arxiv_org_abs_2511_18200/figures/005_Figure_5.jpg]]
*Figure 5: Traditional hierarchical optimization vs. our clusterbased optimization*

InfiniBench的布局优化器引入了**可移动簇（movable cluster）**机制来解决这一瓶颈：

- **簇的定义**：将功能上相互关联的一组对象（例如一张餐桌与环绕它的所有椅子）定义为一个“簇”。簇内的对象保持固定的相对空间关系。
- **簇级操作**：优化器不再单独移动单个对象，而是将整个簇作为一个刚体进行平移、旋转和碰撞检测。这使得优化器能够探索更大的解空间——当某个区域空间不足时，整个功能单元可以被整体迁移至更合适的位置。
- **高密度场景生成**：这一灵活策略使优化器能够生成以往层次化方法无法实现的高密度场景（Figure 6b），同时保持极低的碰撞对数（#CN）和出界率，确保物理合理性。

该优化器构建于Infinigen之上，复用了其丰富的3D资产库，但在优化策略上进行了根本性重构。

### 3.3 任务感知的相机轨迹优化器 (Camera Trajectory Optimizer)

给定已生成的3D场景和特定的空间推理任务（如测量、透视取景、时空跟踪），该模块的目标是生成一条最短的相机路径，确保所有任务相关对象均获得清晰、完整且无遮挡的视图。其核心步骤如Figure 7所示：

1. **候选视点采样**：在场景周围的空间中，基于多标准（距离、角度、高度等）采样大量候选相机视点。
2. **遮挡快速检测**：利用Trimesh/PyRender对每个候选视点进行快速遮挡检测，过滤掉目标对象被部分或完全遮挡的视点。这一步骤解决了Figure 3所示的关键问题——不当视点会遮蔽推理所需的关键信息。
3. **任务相关对象覆盖检查**：确保选中的视点集合能够覆盖所有任务指定的目标对象。
4. **最短路径规划**：在满足覆盖与无遮挡约束的视点集合中，求解连接这些视点的最短遍历路径，作为最终的相机轨迹（Figure 8）。

该方法避免了传统基于优化的方法的巨大计算开销，也无需像强化学习方法那样为每个新场景重新训练，同时保证了多对象场景下的完整覆盖。

### 3.4 真实感渲染管线 (Photorealistic Rendering Pipeline)

最终生成的场景与相机轨迹通过Blender Cycles引擎进行真实感渲染，输出高质量的连续视频帧。渲染配置（如路径追踪采样数对图像质量的影响见Figure 24）经过调优，以在视觉真实感与计算效率之间取得平衡。

### 补充图表

![[assets/figures/papers/paper_list_l2085_https_arxiv_org_abs_2511_18200/figures/004_Figure_4.jpg]]
*Figure 4: LLM-based agentic framework for iterative scene constraint generation, illustrated by an example of generating a scene of a 30 m2 dining room with 10 chairs of different types*

![[assets/figures/papers/paper_list_l2085_https_arxiv_org_abs_2511_18200/figures/006_Figure_6.jpg]]
*Figure 6: Comparison of generating highly complex scenes, with the same room shape and asset parameters*

![[assets/figures/papers/paper_list_l2085_https_arxiv_org_abs_2511_18200/figures/007_Figure_7.jpg]]
*Figure 7: Camera trajectory optimization*



## 实验与关键发现

### 场景生成质量：主实验结果

InfiniBench 在场景生成的核心指标——提示保真度（Fidelity）与物理合理性（碰撞对数 #CN）——上全面超越现有过程化生成框架与基于 LLM 的布局方法，且优势在高复杂度条件下急剧扩大。表 1 和表 2 分别从组成复杂度（对象数量）和关系复杂度（房间占用率）两个维度给出了定量对比。

**组成复杂度维度（Table 1）**：当场景对象数量从 Low 增至 High 时，InfiniBench 的 Fidelity 始终维持在 0.95 以上（Low: 0.98, Medium: 0.95, High: 0.98），而最强基线 **LayoutGPT** (Feng et al., 2023) 在 High 条件下已降至 0.93。物理合理性方面，InfiniBench 在所有三个难度级别均保持 0 碰撞对数，而 LayoutGPT 的碰撞对数从 Low 的 4.0 急剧攀升至 High 的 13.5，**Infinigen** (Raistrick et al., 2023) 的原始优化器亦出现 5.3 次碰撞。这揭示了一个关键瓶颈：LLM 直接生成的布局在高对象数量下无法维持物理合理性，而 InfiniBench 的簇优化引擎从根本上消除了这一问题。

**关系复杂度维度（Table 2）**：在房间占用率从 Low（<10%）升至 High（>50%）时，InfiniBench 的 Fidelity 仅从 0.94 轻微下降至 0.91，而 Infinigen 原始优化器从 0.86 骤降至 0.49，LayoutGPT 从 0.93 降至 0.74。碰撞对数方面，InfiniBench 在 High 占用率下仅 0.1，远低于 LayoutGPT 的 9.6 和 **Holodeck** (Yang et al., 2024) 的 7.8。这表明，传统层次化优化（先固定大物体再放置小物体）在高占用率下会陷入无解状态，而基于可移动簇的灵活优化策略是解锁高密度场景的关键。

### 消融实验：各模块的协同增益

Table 3 的消融实验揭示了 InfiniBench 三个核心组件间的强协同效应。基础优化器（Base Optimizer，即 Infinigen 原始优化器）单独使用时 Fidelity 仅为 0.64；单独加入 LLM 约束精炼模块（+ Refinement）提升至 0.78，单独加入簇优化（+ Cluster Opt.）提升至 0.81。然而，当两者联合使用时，Fidelity 跃升至 0.92，远超任一模块的独立贡献之和。这验证了论文的核心洞察：LLM 的高层语义理解与基于可移动簇的低层物理优化并非简单叠加，而是形成了一种互补——LLM 精炼提供更合理的约束空间，簇优化则在该空间中高效搜索可行解。

![[assets/figures/papers/paper_list_l2085_https_arxiv_org_abs_2511_18200/figures/012_Table_3.jpg]]
*Table 3: Ablation study of different components in InfiniBench*

Table 4 进一步考察了约束精炼的迭代次数效应。Fidelity 在 1 次迭代后为 0.78，3 次迭代后升至 0.90，5 次迭代后收敛至 0.92，10 次迭代无进一步提升。这表明 LLM 智能体的 CoT 反馈循环具备快速收敛特性，5 次迭代即可在质量与计算效率间取得平衡。

![[assets/figures/papers/paper_list_l2085_https_arxiv_org_abs_2511_18200/figures/013_Table_4.jpg]]
*Table 4: Ablation study of how the number of iterations in constraint refinement affects the scene quality*

### VLM 空间推理诊断：复杂度维度的解耦分析

InfiniBench 的核心价值在于对 VLM 失败模式的精细诊断。通过独立控制三个复杂度维度，实验揭示了不同空间推理任务对复杂度维度的差异化敏感性。

**组成复杂度（Table 5, Figure 11）**：随着无关对象数量从 Low 增至 High，所有 VLM 在测量（Measurement）、视角采择（Perspective-taking）和时空跟踪（Spatiotemporal）三项任务上均出现性能退化。以 **Gemini-2.5-Pro** 为例，时空跟踪任务从 Low 的 68.3% 降至 High 的 56.2%，视角采择从 65.1% 降至 52.3%。Figure 11 的折线图进一步显示，性能下降并非线性——在 Medium 到 High 的过渡区间存在一个加速退化拐点，暗示对象数量超过某个阈值后，VLM 的空间注意力机制可能发生崩溃。

**观测复杂度（Table 6）**：提高相机视角（如鸟瞰视角）能显著提升视角采择和时空跟踪任务的性能，但对测量任务效果不明显。这一非对称现象提示：测量任务可能更依赖精确的深度感知和尺度估计，而非单纯的视野覆盖；视角采择和时空跟踪则更多受遮挡和视野完整性的制约。InfiniBench 的相机轨迹优化器通过任务感知的视点采样与遮挡检查，为这一维度的可控分析提供了可靠基础。

### 仍需人工验证的观察

部分 VLM 失败模式的具体归因（如高组成复杂度下的退化究竟是源于计数误差还是更深层的空间关系推理缺陷）在现有实验中尚未得到彻底分离。此外，实验主要覆盖 Gemini-2.5-Pro、GPT-4V 等闭源模型，开源 VLM 在 InfiniBench 上的表现模式是否一致，需进一步验证。

### 补充图表

![[assets/figures/papers/paper_list_l2085_https_arxiv_org_abs_2511_18200/figures/008_Table_1.jpg]]
*Table 1: Quantitative comparison of scene generation quality with different numbers of objects in the scene*

![[assets/figures/papers/paper_list_l2085_https_arxiv_org_abs_2511_18200/figures/009_Table_2.jpg]]
*Table 2: Quantitative comparison of scene generation quality with different levels of scene occupancy ratio*

![[assets/figures/papers/paper_list_l2085_https_arxiv_org_abs_2511_18200/figures/014_Table_5.jpg]]
*Table 5: Performance of Measurement, Perspective-taking and Spatiotemporal tasks with different numbers of irrelevant objects*

![[assets/figures/papers/paper_list_l2085_https_arxiv_org_abs_2511_18200/figures/015_Figure_11.jpg]]
*Figure 11: VLMs’ performance of spatial reasoning with varying compositional scene complexity*

![[assets/figures/papers/paper_list_l2085_https_arxiv_org_abs_2511_18200/figures/019_Table_6.jpg]]
*Table 6: VLM’s reasoning performance with varying observational scene complexity*

![[assets/figures/papers/paper_list_l2085_https_arxiv_org_abs_2511_18200/figures/002_Figure_2.jpg]]
*Figure 2: Limitations of LLM-based layout generation*



## 定位与知识库关联

### 核心瓶颈与设计动机

现有VLM空间推理基准面临一个根本性矛盾：一方面，诊断VLM在不同场景条件下的失败模式需要精细控制场景的组成复杂度（对象数量与种类）、关系复杂度（空间排列与占用率）和观测复杂度（视角与遮挡）；另一方面，现有3D场景生成方法无法在高复杂度下同时保证提示一致性（Fidelity）和物理合理性（无碰撞、无出界）。这一瓶颈使研究者难以区分VLM的性能下降究竟源于对象数量增多导致的计数误差，还是更深层的空间关系推理能力不足。

InfiniBench的核心洞察在于将LLM的高层语义理解（约束生成与思维链迭代精炼）与基于可移动簇的优化引擎解耦，前者负责“理解场景应该有什么”，后者负责“确保场景物理上能存在”。这一分工使系统在生成以往层次化方法不可能实现的高密度场景（如50%以上房间占用率）时，仍能维持接近完美的物理合理性。

### 与现有方法的谱系关系

**过程化生成框架**：**Infinigen**（Raistrick et al., CVPR 2023）和 **Luminous**（Zhang et al., 2024）代表了过程化3D场景生成的主流路线。这类方法通过预定义的规则和参数生成多样化场景，但其原始优化器采用层次化策略——先固定大物体位置，再在剩余空间中放置小物体。当场景复杂度提升（高对象数量或高占用率）时，这种刚性顺序导致无可解状态，生成失败。InfiniBench的布局优化器构建于Infinigen的资产库之上，但将其层次化优化替换为基于可移动簇的灵活优化，从根本上改变了求解空间的可达性。

**LLM布局生成方法**：**LayoutGPT**（Feng et al., ICCV 2023）、**Holodeck**（Yang et al., CVPR 2024）和 **I-Design**（Chen et al., 2023）代表了利用LLM直接生成空间布局的路线。这类方法让LLM直接输出物体的坐标和朝向，但LLM缺乏精确的空间推理能力，容易产生物体重叠、穿墙、比例失调等物理冲突（见Figure 2）。InfiniBench改变了LLM的角色：不要求LLM输出最终布局，而是让它生成过程化约束（如“一张餐桌周围放置6把椅子，椅子距桌边0.3米”），由优化器负责物理求解。这一角色转换将LLM从它不擅长的精确数值预测中解放出来，同时保留了其语义理解和常识推理的优势。

**相机轨迹生成方法**：现有方法中，基于优化的方法计算开销大，生成式方法缺乏多对象覆盖保证，强化学习方法需逐场景重训。InfiniBench的任务感知相机路径规划通过多标准视点采样与遮挡检查，生成确保所有任务相关对象完整可见的最短路径，在效率和任务覆盖之间取得了平衡。

### 关键消融发现与模块协同

消融实验揭示了InfiniBench各模块之间的协同效应（Table 3）：基础优化器（Infinigen原始优化器）的Fidelity仅为0.64；单独添加约束精炼模块或簇优化模块分别将Fidelity提升至0.71和0.77；两者联合使用时，Fidelity跃升至0.92。这一超线性增益证实了“LLM理解场景语义→生成合理约束→优化器灵活求解”这一流水线设计的必要性——缺少任一环节都会导致性能显著退化。

迭代精炼的效率同样值得注意（Table 4）：约束精炼在5次迭代内收敛至Fidelity 0.92，10次迭代无进一步提升。这表明LLM智能体的思维链反馈循环能快速定位并解决约束冲突，而非无休止地尝试。

### 适用边界与局限

**场景类型边界**：InfiniBench目前聚焦于室内静态场景（客厅、卧室、餐厅），其约束生成逻辑和簇优化策略依赖于室内物体的典型空间关系（如桌椅围绕、书架靠墙）。扩展到户外场景（无明确边界、地形变化）或包含动态对象（人物、车辆）的场景时，需要重新设计约束模板和优化目标。

**复杂度维度的交互**：当前实验分别控制组成、关系和观测复杂度，但三个维度之间可能存在交互效应。例如，高组成复杂度（多对象）叠加高关系复杂度（高占用率）时，场景生成的难度可能非线性增长，现有评估尚未系统探索这种多维度组合的极限。

**VLM诊断的深度**：InfiniBench能精确控制场景条件并测量VLM性能变化，但性能下降的归因仍存在模糊地带。例如，高组成复杂度下VLM的测量任务准确率下降，究竟是因为对象增多导致的目标识别混淆，还是空间关系推理本身超载？这一问题需要更细粒度的错误分析才能解答。

### 开放问题

1. **复杂度交互与VLM失败模式**：为什么提高相机视角（如鸟瞰）能显著提升透视取景和时空跟踪任务的性能，但对测量任务效果不明显？这是否意味着不同空间推理子任务对观测复杂度维度有本质不同的依赖，需要针对性的基准设计？

2. **场景域迁移**：InfiniBench的核心方法——LLM约束生成+簇优化+任务感知相机规划——能否迁移到户外场景或包含动态对象的场景？这需要解决室外场景的无边界约束定义、动态对象的时序一致性等新挑战。

3. **VLM能力瓶颈的精确归因**：当前基准揭示了VLM在不同复杂度下的性能差异，但尚未建立从场景参数到具体失败机制（计数错误、关系混淆、视角盲区）的因果链。未来工作可结合注意力可视化和逐样本错误分析，构建更细粒度的诊断框架。



## 原文 PDF

![[paperPDFs/CVPR_2026/InfiniBench_Infinite_Benchmarking_for_Visual_Spatial_Reasoning_with_Customizable_Scene_Complexity.pdf]]
