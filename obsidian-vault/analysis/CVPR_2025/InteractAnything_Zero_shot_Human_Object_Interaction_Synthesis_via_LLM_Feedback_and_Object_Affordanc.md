---
title: "InteractAnything: Zero-shot Human Object Interaction Synthesis via LLM Feedback and Object Affordance Parsing"
type: paper
paper_level: A
venue: CVPR
year: 2025
pdf_ref: paperPDFs/CVPR_2025/InteractAnything_Zero_shot_Human_Object_Interaction_Synthesis_via_LLM_Feedback_and_Object_Affordanc.pdf
project_link: null
code_link: https://github.com/NVIDIAGameWorks/
aliases:
- InteractAnything
tags:
- CVPR_2025
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: 将LLM作为人类级反馈提供者，逐步推理语义交互关系并初始化人物状态；同时利用预训练2D扩散模型通过自适应遮罩修补解析未知物体的接触可供性，从而引导从粗略初始姿态到精细接触交互的全局优化。
primary_logic: 零样本HOI的关键是将复杂的人-物交互分解成语义推理、可供性解析和姿态合成三个阶段，通过从大规模预训练模型中蒸馏通用知识，替代对特定数据集的训练，实现对任意物体的精细交互生成。
claims:
- InteractAnything在GPT-4V整体和接触质量评选中显著优于DreamHOI、DreamFusion、Magic3D等基线方法。
- LLM引导的初始化和精细优化对性能至关重要；移除LLM初始化后GPT-4V分数降至26.1，移除精细优化后降至39.1。
- 开集物体可供性解析模块能够为未见物体生成准确的多视图接触概率图，支撑后续的精细交互优化。
- GPT-4V Selection 上 Overall = 45.6
---

# InteractAnything: Zero-shot Human Object Interaction Synthesis via LLM Feedback and Object Affordance Parsing

> [!tip] 核心洞察
> 零样本HOI的关键是将复杂的人-物交互分解成语义推理、可供性解析和姿态合成三个阶段，通过从大规模预训练模型中蒸馏通用知识，替代对特定数据集的训练，实现对任意物体的精细交互生成。

| 字段 | 内容 |
|------|------|
| 中文题名 | InteractAnything：基于LLM反馈与物体可供性解析的零样本人体-物体交互合成 |
| 英文题名 | InteractAnything: Zero-shot Human Object Interaction Synthesis via LLM Feedback and Object Affordance Parsing |
| 会议/期刊 | CVPR 2025 |
| Links | [Code](https://github.com/NVIDIAGameWorks/) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/image_and_video_generation |
| Method | InteractAnything |
| Dataset | GPT-4V Selection, CLIP Similarity |

> [!tip] 效果简介
> - GPT-4V Selection 上，Overall 45.6 vs 26.0 (DreamHOI) (+19.6)。
> - CLIP Similarity 上，CLIP Score 0.2968 vs N/A (N/A)。

## 概要

**InteractAnything**提出了一种零样本3D人体-物体交互合成框架，旨在解决现有方法在开放集物体上难以准确捕捉语义关系、接触区域与全局一致性的核心瓶颈。其关键洞察在于：将复杂的人-物交互分解为**语义关系推理**、**物体接触可供性解析**与**人体姿态合成**三个阶段，通过从大规模预训练模型（LLM与2D扩散模型）中蒸馏通用知识，替代对特定交互数据集的依赖，从而实现对任意物体的精细交互生成。

方法的核心机制是：首先利用LLM作为人类级反馈提供者，逐步推理语义交互关系（如相对位置、朝向、尺度及交互身体部位），初始化人物与物体的空间状态；随后，通过预训练2D扩散模型的自适应遮罩修补，解析未知物体的多视图接触可供性，生成接触概率图；最后，在粗到细的优化框架下，结合力闭合损失与穿模惩罚，引导从初始姿态到精细接触交互的全局优化。

实验结果表明，InteractAnything在GPT-4V整体质量评选中达到45.6%的选择率，显著优于**DreamHOI**（26.0%）、**DreamFusion**（6.5%）与**Magic3D**（4.3%）等基线方法。消融研究进一步验证了LLM引导的初始化与精细优化模块的关键作用：移除LLM初始化后分数降至26.1，移除精细优化后降至39.1。该方法在场景填充与交互应用中也展现出良好的泛化能力。

**局限性**方面，生成质量高度依赖预训练模型的能力，可能受其幻觉与偏见影响；定量评估主要基于图像相似度与GPT-4V投票，缺乏对物理真实性的全面衡量；当前建模限于SMPL-H参数化人体，尚不支持非人代理或不同骨架结构的交互对象。

三维人体与物体的交互（Human-Object Interaction, HOI）生成是计算机视觉与图形学中的核心难题，其目标是根据语义指令合成自然、物理合理的人体姿态，并实现与任意物体的精细接触。该技术在具身智能、虚拟现实和数字人等领域具有广泛的应用前景。

现有方法大致可分为两类：基于数据驱动的方法依赖大规模3D交互数据集进行训练，但其泛化能力受限于数据集的规模与多样性，难以覆盖开放世界中无穷无尽的物体类别与交互方式；基于文本到3D生成的方法，如 **DreamFusion**（Poole et al., ICLR 2023）和 **Magic3D**（Lin et al., CVPR 2023），利用预训练的2D扩散模型通过分数蒸馏采样（Score Distillation Sampling, SDS）从文本生成3D内容，但其设计初衷是生成单一物体或场景，缺乏对人-物交互关系的显式建模。

针对零样本3D HOI合成，**DreamHOI**（Zhu et al., arXiv 2024）率先提出将物体网格嵌入扩散过程的方法，然而该方法仅依赖SDS优化驱动交互生成，存在以下根本性瓶颈：

1. **语义关系缺失**：无法显式推理人体与物体之间的空间关系（相对位置、朝向、尺度）和语义关联（交互部位、动作意图），导致生成姿态与文本指令脱节。
2. **接触可供性未知**：对开放集物体缺乏有效的接触区域解析机制，难以确定“手该放在哪里”，仅依靠简单的混合SDS损失无法准确捕捉精细的接触模式。
3. **全局一致性不足**：缺乏从粗到细的优化策略，生成结果常出现穿模、悬空或抓握不牢等物理不合理现象。

上述问题的本质在于：复杂的HOI涉及语义推理、可供性解析和姿态合成三个相互耦合的子任务，而预训练模型本身并不具备理解这种复合关系的能力。因此，**如何将大规模预训练模型中的通用知识蒸馏为零样本交互生成的先验，是突破当前瓶颈的关键**。

InteractAnything正是针对这一核心问题，提出将零样本HOI分解为语义推理、可供性解析和姿态合成三个阶段，通过LLM反馈和物体可供性解析，在不依赖任何3D交互训练数据的前提下，实现对任意物体的精细交互生成。

## 核心方法与创新机理

InteractAnything 的核心创新在于将零样本 3D 人-物交互（HOI）这一复杂任务分解为可解耦的三个阶段，并通过从大规模预训练模型中蒸馏通用知识，替代对特定数据集的训练依赖。这一思路直接回应了现有方法的瓶颈：预训练模型无法直接理解复杂的交互模式，导致语义关系、接触区域和全局一致性难以同时满足。

### 方法谱系与知识库定位

在零样本 3D HOI 生成的方法谱系中，InteractAnything 相对于现有基线做出了三个关键改变（changed slots），每一项都对应一个明确的性能增益来源：

**1. 人-物关系推理：从隐式 SDS 优化到 LLM 显式推理**

现有方法（如 **DreamHOI** (Zhu et al., arXiv 2024)、**DreamFusion** (Poole et al., ICLR 2023)）仅依赖分数蒸馏采样（SDS）进行全局优化，缺乏对语义交互关系的显式建模。InteractAnything 将 LLM 作为人类级反馈提供者，通过逐步选项推理，显式初始化人物的相对位置、朝向、尺度及交互身体部位（Section 3.2）。这一改变使方法从“盲目优化”转变为“语义引导优化”，为后续的精细接触生成提供了合理的初始状态。

**2. 物体接触可供性解析：从预设先验到开放集自适应解析**

基线方法通常依赖预设的接触先验或简单的混合 SDS，难以泛化至训练集之外的开放集物体。InteractAnything 提出利用预训练 2D 扩散模型，通过 LLM 引导的自适应遮罩修补，从多视图解析任意物体的接触可供性（Section 3.3）。具体而言，2D 距离概率函数 $f_{\mathrm{afford}}^{(i)}(\mathbf{p}) = e^{-\|\mathbf{d}_i(\mathbf{p})\|}$ 基于检测到的身体关键点与物体遮罩的距离计算接触概率，再通过多视图聚合 $\mathcal{P}(\mathbf{p}) = \frac{1}{n_p}\sum_{i=1}^{n_p} f_{\mathrm{afford}}^{(i)}(\mathbf{p})$ 得到 3D 物体表面的接触概率分布。这一模块是方法能够处理“任意物体”的关键使能技术。

**3. 交互优化：从单一全局优化到粗-细两阶段约束**

基线方法仅进行全局 SDS 优化，缺乏精细的接触约束，导致抓握等细节交互质量不足。InteractAnything 在全局 HOI 优化（损失函数 $L_c = \phi_i L_{inter} + \phi_n L_n + \phi_s L_{scale} + \phi_p L_{pene} + s' \cdot L_g$）的基础上，进一步引入力闭合损失 $L_{fc}$ 和穿模惩罚，形成粗到细的优化管线（Section 3.5）。消融实验表明，移除精细优化后 GPT-4V 整体选择率从 45.6 降至 39.1，抓握细节明显退化（Table 3, Figure 4），直接验证了这一改变的必要性。

### 决定性证据与因果机制

InteractAnything 的核心主张——将复杂 HOI 分解为语义推理、可供性解析和姿态合成三个阶段——得到了多层次实验证据的支持：

- **整体性能优势**：在 GPT-4V 整体质量评选中，InteractAnything 获得 45.6 的选择率，显著优于 DreamHOI（26.0）、DreamFusion（6.5）和 Magic3D（4.3）（Table 2, Section 4.2），差距达 +19.6 个百分点。这表明分解式管线在生成质量和交互合理性上具有系统性优势。
- **组件因果验证**：消融实验揭示了两个关键组件的因果作用。移除 LLM 引导的初始化后，GPT-4V 分数降至 26.1，方法退化为普通 SDS 优化，甚至低于 DreamHOI（Table 3），证明语义推理是性能基线的决定性因素。移除精细优化后分数降至 39.1，证明接触约束对细节质量有独立贡献。
- **可供性解析的可视化验证**：Figure 5 展示了同一物体在不同文本指令下的自适应修补与可供性解析结果，证明该模块能够为未见物体生成准确的多视图接触概率图，是支撑开放集泛化的核心机制。

### 局限与待验证假设

尽管证据链较为完整，仍需注意以下局限：

- 定量评估主要依赖 CLIP 相似度（0.2968, Table 1）和 GPT-4V 投票，这两种基于图像的指标可能无法完全反映物理真实性和长期交互稳定性。力闭合损失仅提供接触点层面的物理约束，缺乏对整体动力学合理性的验证。
- 方法性能高度依赖预训练模型（LLM 与 2D 扩散模型）的能力，可能受其幻觉和偏见影响。在 LLM 推理错误或扩散模型修补失真的情况下，错误会沿管线传播。
- 当前建模限于 SMPL-H 参数化人体，不支持非人代理或具有不同骨架结构的交互对象，这一约束限制了方法在机器人等领域的直接迁移。

InteractAnything 将零样本 3D 人-物交互合成分解为四个串联模块：**LLM 引导的初始化**、**开集物体可供性解析**、**文本-物体驱动的人体姿态合成**，以及**表现力 HOI 优化**。该框架的输入仅需一段自然语言交互描述和一个任意物体的 3D 网格，输出为与物体发生自然、精细接触的 SMPL-H 参数化人体模型。

### 核心设计思路

现有零样本 HOI 方法的核心瓶颈在于，预训练模型无法直接理解复杂的人-物语义关系、接触区域和全局一致性——这些约束在单物体生成或非接触场景中并不存在。InteractAnything 的关键洞察是：将这一复杂任务**分解为语义推理、可供性解析和姿态合成三个阶段**，通过从大规模预训练模型（LLM 与 2D 扩散模型）中蒸馏通用知识，替代对特定交互数据集的训练，从而实现对任意物体的精细交互生成。

### 模块流程

**LLM 引导的初始化**（Section 3.2）作为整个流程的起点，将 LLM 视为人类级反馈提供者。给定文本描述（如 “a person sitting on a chair”），LLM 逐步推理并选择人-物之间的相对位置、朝向、尺度以及参与交互的身体部位。这些语义关系被映射为物体在场景中的旋转 $r_o$、平移 $t_o$、缩放 $s_o$ 和状态 $s$，为人体的初始放置提供了合理的空间约束。

**开集物体可供性解析**（Section 3.3）负责从任意物体的几何形状中提取接触先验。该模块利用预训练 2D 扩散模型进行自适应遮罩修补——根据 LLM 推断的身体部位信息生成全身遮罩 $M_{\mathrm{full}}^i$ 和局部遮罩 $M_{\mathrm{part}}^i$，在物体渲染视图上修补出可能的人体交互部位。随后，通过 2D 距离概率函数 $f_{\mathrm{afford}}^{(i)}(\mathbf{p}) = e^{-\|\mathbf{d}_i(\mathbf{p})\|}$ 计算修补结果中人体关键点与物体遮罩的接触概率，并将其聚合为 3D 物体表面的接触可供性分布 $\mathcal{P}(\mathbf{p})$。这一模块使框架能够泛化至训练中从未见过的开放集物体。

**文本-物体驱动的人体姿态合成**（Section 3.4）在 LLM 初始化的空间约束和物体几何信息的引导下，通过多视角分数蒸馏采样（SDS）优化 SMPL-H 参数，生成与文本语义对齐且符合物体空间约束的初始人体姿态。

**表现力 HOI 优化**（Section 3.5）采用从粗到细的策略。全局优化阶段使用组合损失 $L_c = \phi_i L_{inter} + \phi_n L_n + \phi_s L_{scale} + \phi_p L_{pene} + s' \cdot L_g$，其中交互损失 $L_{inter}$ 以物体可供性图为权重，计算接触部位的 Chamfer 距离；精细优化阶段引入力闭合损失 $L_{fc}$ 和穿模惩罚，进一步提升抓握等精细接触的真实感和物理合理性。

### 输入输出

- **输入**：文本交互描述 + 任意物体 3D 网格
- **输出**：SMPL-H 参数化人体模型（包含体型 $\beta$、身体姿态 $\theta_b$、手部姿态 $\theta_h$），与物体形成自然、接触准确的 3D 交互

框架的整体结构可参考 **Figure 2**，其中清晰展示了从 LLM 查询、可供性解析、姿态合成到精细优化的完整数据流。

![[assets/figures/papers/paper_list_l1728_InteractAnything_Zero_shot_Human_Object_Interaction_Synthesis_via_LLM_Fe/figures/003_Figure_2.jpg]]
*Figure 2: Framework of InteractAnything. Given a text description and any object mesh as input, our approach begins by querying LLM to infer precise human-object relationships, which are used to initialize object properties. Next, we analyze the contact affordance of the object geometry. The human pose is synthesized using a pre-trained 2D diffusion model, guided by multi-view SDS loss and the designed spatial constraint. Finally, based on the targeted object contact areas and a plausible human pose, we perform expressive HOI optimization to synthesize realistic and contact-accurate 3D human-object interactions*

### 3.1 人体与物体表示基础

InteractAnything 采用 **SMPL-H** 参数化人体模型 [36, 48] 作为交互主体。该模型同时包含身体和手部姿态参数，通过线性混合蒙皮函数从体型参数 $\beta$、身体姿态 $\theta_b$ 和手部姿态 $\theta_h$ 计算网格顶点：

$$\mathcal{V}(\beta, \theta_b, \theta_h) = f\left(T_p(\beta, \theta_b, \theta_h), J(\beta), \theta, \mathcal{W}\right) \tag{1}$$

其中 $T_p$ 为姿态相关的变形矩阵，$J(\beta)$ 为关节点位置，$\mathcal{W}$ 为蒙皮权重。物体以任意三维网格作为输入，无需类别先验。

三维生成的核心驱动力来自 **Score Distillation Sampling (SDS)**，利用预训练二维扩散模型将 NeRF 渲染图像与文本提示对齐：

$$\nabla_{\theta} \mathcal{L}_{\mathrm{SDS}}(x) = \mathbb{E}_{t,\epsilon}\left[w(t)\left(\hat{\epsilon}(x_t; y, t) - \epsilon\right)\frac{\partial x}{\partial \theta}\right] \tag{2}$$

其中 $x$ 为渲染图像，$y$ 为文本条件，$\hat{\epsilon}$ 为扩散模型预测噪声，$w(t)$ 为时间步权重。

### 3.2 LLM 引导的人-物关系推理与初始化

该模块将 LLM 作为“人类级反馈提供者”，从简单文本描述中逐步推理语义交互关系。LLM 从预定义选项中选择人相对于物体的位置（如“正前方”“右侧”），结合人物与物体的组合尺寸映射为物体平移向量 $t_o$；同时推断物体旋转 $r_o$、缩放 $s_o$ 以及参与交互的身体部位标签。这一初始化过程为后续可供性解析和姿态优化提供了语义合理的空间先验，避免了纯 SDS 优化在复杂交互场景下的收敛困难。

### 3.3 开放集物体可供性解析

对于任意未见物体，该模块通过 **LLM 引导的自适应遮罩修补** 蒸馏可能的交互部位信息。具体而言，利用 LLM 推断的物体位姿和交互身体部位，分别生成两类修补遮罩：

- **全身修补遮罩**，覆盖人体在物体周围的大致区域：

$$M_{\mathrm{full}}^{i} = \mathcal{I}\left((\mathcal{V}_H \cdot r_o^{-1}), s_f, c^{i}\right) + t_o^{-1} + \varpi_1 \tag{3}$$

- **身体部位修补遮罩**，聚焦于 LLM 指定的交互部位（如手部）：

$$M_{\mathrm{part}}^{i} = \mathcal{I}\left((\mathcal{P}_h \cdot r_o^{-1}), s_p, c^{i}\right) + t_o^{-1} + \varpi_2 \tag{4}$$

其中 $\mathcal{V}_H$ 为人体顶点，$\mathcal{P}_h$ 为指定身体部位顶点，$c^i$ 为第 $i$ 个相机参数，$s_f$、$s_p$ 为尺寸缩放因子，$\varpi_1$、$\varpi_2$ 为偏移量。$\mathcal{I}$ 为投影函数。

在多视图修补图像中，通过预训练姿态估计器检测人体关键点，定义基于二维距离的接触概率函数：

$$f_{\mathrm{afford}}^{(i)}(\mathbf{p}) = e^{-\|\mathbf{d}_i(\mathbf{p})\|} \tag{5}$$

其中 $\mathbf{d}_i(\mathbf{p})$ 为像素 $\mathbf{p}$ 到最近检测关键点的距离。最后将多视图二维概率聚合为三维物体表面的接触可供性分布：

$$\mathcal{P}(\mathbf{p}) = \frac{1}{n_p}\sum_{i=1}^{n_p} f_{\mathrm{afford}}^{(i)}(\mathbf{p}) \tag{6}$$

该分布 $W_M$ 直接作为后续交互优化的加权图。

### 3.4 文本-物体驱动的人体姿态合成

在获得物体可供性图后，该模块通过多视角 SDS 优化生成初始人体姿态。优化过程同时受文本语义和物体空间几何约束，确保合成姿态既符合交互语义，又尊重物体的物理边界。

### 3.5 表达性 HOI 优化

该模块采用粗到细的优化策略。**全局优化** 更新物体属性，组合损失为：

$$L_c = \phi_i L_{inter} + \phi_n L_n + \phi_s L_{scale} + \phi_p L_{pene} + s' \cdot L_g \tag{7}$$

其中 $L_{inter}$ 为交互损失，$L_n$ 为法向一致性损失，$L_{scale}$ 为尺度正则项，$L_{pene}$ 为穿透惩罚，$L_g$ 为地面约束。交互损失以物体可供性图加权接触部位的 Chamfer 距离：

$$L_{inter} = \sum_{i\in[h], j\in[o]} W_M(j) \cdot f_{cham}(P_h, P_o) \tag{8}$$

其中 $[h]$ 为交互身体部位顶点集，$[o]$ 为物体接触区域顶点集，$W_M(j)$ 为式 (6) 得到的可供性权重。

**精细优化** 引入基于 SMPL 的力闭合损失，确保抓握等接触动作的物理合理性：

$$L_{fc} = \sum_{j\in[o]} \left(\sum_{i\in[h]} f_v(i,j) \cdot n(j)\right)^2, \quad \delta \cdot [\theta_b, \theta_h] \tag{9}$$

其中 $f_v(i,j)$ 为人体顶点 $i$ 对物体顶点 $j$ 施加的虚拟力，$n(j)$ 为物体表面法向，$\delta$ 控制姿态参数的更新幅度。该损失鼓励接触力相互抵消，形成稳定抓握。

![[assets/figures/papers/paper_list_l1728_InteractAnything_Zero_shot_Human_Object_Interaction_Synthesis_via_LLM_Fe/figures/006_Figure_5.jpg]]
*Figure 5: Visualization of the adaptive inpainting and openset object affordance parsing results on the same object with different text instructions. Our method first generates reasonable 2D inpainting results (middle columns) and then computes contact probabilities as the affordance representation (right column)*

## 实验与关键发现

### 核心性能：GPT-4V 与 CLIP 评估

InteractAnything 在零样本 3D 人-物交互生成任务上展现出相对于现有方法的显著优势。由于缺乏直接的 3D 交互真值，实验主要采用 CLIP 相似度和 GPT-4V 选择两种基于图像的代理指标进行评估。

在 **GPT-4V 选择**测试中（Table 2），GPT-4V 被要求根据人体完整性、物体完整性及物理交互正确性等标准，从所有生成结果中选出最合理的输出。InteractAnything 在整体质量（Overall）和接触质量（Contact）两个维度上均取得了最高选择率：**Overall 45.6，Contact 52.1**。相比之下，最强的零样本 HOI 基线 **DreamHOI**（Zhu et al., arXiv 2024）仅获得 Overall 26.0、Contact 17.3。通用文本到 3D 生成方法 **DreamFusion**（Poole et al., ICLR 2023）和 **Magic3D**（Lin et al., CVPR 2023）的 Overall 选择率分别仅为 6.5 和 4.3，表明它们无法有效处理复杂的人-物交互约束。这一巨大差距验证了核心瓶颈：通用 3D 生成模型缺乏对语义关系、接触区域和全局一致性的显式建模能力。

在 **CLIP 相似度**指标上（Table 1），InteractAnything 取得了 **0.2968** 的分数，同样优于对比方法。值得注意的是，CLIP 分数反映的是生成图像与文本的整体语义对齐程度，而 GPT-4V 选择更能捕捉交互的物理合理性和接触细节——这正是本文方法设计的核心目标。

![[assets/figures/papers/paper_list_l1728_InteractAnything_Zero_shot_Human_Object_Interaction_Synthesis_via_LLM_Fe/figures/005_Table_1.jpg]]
*Table 1: Comparison of CLIP similarity scores for different methods. Higher scores are better*

### 消融实验：LLM 初始化与精细优化的关键作用

消融实验（Table 3）揭示了两个核心模块的因果贡献：

![[assets/figures/papers/paper_list_l1728_InteractAnything_Zero_shot_Human_Object_Interaction_Synthesis_via_LLM_Fe/figures/008_Table_3.jpg]]
*Table 3: Ablation study on LLM-guided initialization and HOI refinement by GPT-4V selection*

1. **移除 LLM 引导的初始化（w/o LLM-init）**：GPT-4V Overall 选择率从 45.6 骤降至 **26.1**，甚至低于 DreamHOI 的 26.0（考虑到后者本身包含一定的初始化策略）。这表明，若仅依赖无先验的 SDS 优化，模型难以从零开始建立正确的人-物空间关系，LLM 提供的语义推理和初始位姿是全局优化的必要前提。

2. **移除精细交互优化（w/o Refine）**：GPT-4V Overall 选择率降至 **39.1**。虽然仍高于所有基线，但下降了 6.5 个百分点。Figure 4 的视觉对比进一步揭示，移除力闭合损失和精细接触约束后，抓握动作的细节明显退化——手指与物体表面出现间隙或穿透，缺乏真实的接触感。这证明粗到细的优化策略对于将“大致正确”的姿态转化为“物理可信”的交互至关重要。

![[assets/figures/papers/paper_list_l1728_InteractAnything_Zero_shot_Human_Object_Interaction_Synthesis_via_LLM_Fe/figures/007_Figure_4.jpg]]
*Figure 4: Ablation study on the fine-grained optimization. Left figures are the results of removing fine-grained terms and right figures apple fine-grained terms to synthesize grasping details*

### 开集物体可供性解析的有效性

Figure 5 展示了自适应修补与可供性解析模块在同一物体、不同文本指令下的工作效果。对于给定的物体多视图渲染，该模块首先生成合理的 2D 修补结果（中间列），随后基于检测到的身体关键点与物体遮罩的距离计算出接触概率热力图（右侧列）。热力图准确反映了不同指令下物体表面的可接触区域分布——例如，“坐”指令将高概率区域集中在椅面，而“推”指令则分布在把手或边缘。这一可视化为后续的接触加权 Chamfer 损失提供了可靠的引导信号，是方法能够泛化至任意未见物体的关键支撑。

### 定性对比与失败模式

Figure 3 的定性对比显示，InteractAnything 生成的交互在人体姿态自然度、与物体的空间关系以及接触精度上均优于基线方法。DreamHOI 的结果常出现人体与物体的错位或语义不匹配，而 DreamFusion 和 Magic3D 则难以生成完整的人体结构。

![[assets/figures/papers/paper_list_l1728_InteractAnything_Zero_shot_Human_Object_Interaction_Synthesis_via_LLM_Fe/figures/004_Figure_3.jpg]]
*Figure 3: Qualitative comparison results with baselines. ∗ indicates we re-implement this method by embedding object mesh into the diffusion process, which follows the pipeline of DreamHOI [67] and our method. More visualization results are presented in supplementary materials*

尽管如此，方法仍存在若干已知局限：
- **生成质量受预训练模型能力制约**：LLM 的幻觉可能导致不合理的初始关系推理，2D 扩散模型的偏差可能影响修补和 SDS 引导的质量。
- **多视角一致性不足**：部分结果在不同视角下可能出现肢体断裂或接触错位，这源于逐视图独立优化缺乏显式的 3D 一致性约束。
- **评估指标的局限性**：CLIP 分数和 GPT-4V 投票均基于 2D 图像，无法完全衡量物理真实性（如力平衡、长期稳定性）和 3D 几何精度。当前力闭合损失仅提供一阶近似，缺乏完整的物理模拟验证。
- **人体表示的局限**：方法基于 SMPL-H 参数化模型，无法处理非人代理或具有不同骨架结构的交互对象。

## 定位与知识库关联

### 任务定位与核心创新

InteractAnything 面向**零样本3D人体-物体交互（HOI）生成**这一新兴任务，输入仅需一段文本描述和任意物体的3D网格，输出具有精细接触姿态的3D交互场景。该任务的核心瓶颈在于：现有方法难以在开放集物体上同时捕捉语义关系、接触区域和全局一致性——这些复杂关系在单物体生成或非接触场景中不存在，预训练模型无法直接理解。

InteractAnything 的核心洞察是将复杂的人-物交互分解为**语义推理、可供性解析和姿态合成**三个阶段，通过从大规模预训练模型中蒸馏通用知识，替代对特定数据集的训练。该方法首次将LLM引入HOI生成流程，作为人类级反馈提供者逐步推理语义交互关系并初始化人物状态；同时利用预训练2D扩散模型通过自适应遮罩修补解析未知物体的接触可供性，引导从粗略初始姿态到精细接触交互的全局优化。

### 与基线方法的关系

InteractAnything 在零样本3D HOI生成任务上与以下代表性基线形成直接对比：

- **DreamHOI**（Zhu et al., arXiv 2024）：作为零样本人物交互生成的直接基线，DreamHOI 同样采用将物体网格嵌入扩散过程的流程。InteractAnything 在GPT-4V整体选择率上以45.6对26.0显著超越（Table 2），核心差异在于DreamHOI仅依赖SDS优化，缺乏显式的语义关系推理和接触可供性解析机制。

- **DreamFusion**（Poole et al., ICLR 2023）：文本到3D生成的奠基性工作，基于SDS从文本生成3D资产。在HOI任务上，其GPT-4V选择率仅为6.5，反映出纯文本驱动方法无法处理人-物空间关系约束的根本局限。

- **Magic3D**（Lin et al., CVPR 2023）：高分辨率文本到3D生成方法，在HOI任务上GPT-4V选择率仅4.3，进一步印证了通用3D生成框架在交互场景中的不足。

- **InterFusion**：基于NeRF的零样本人物交互生成方法，论文中作为对比基线提及，但具体引用信息需手动核实。

### 方法的关键差异槽位

InteractAnything 相对于上述基线在三个关键设计槽位上有本质改进：

1. **人-物关系推理**：基线方法仅依赖SDS优化，无显式语义关系推理。InteractAnything 通过LLM逐步选项推理，初始化人物相对位置、朝向、尺度及交互身体部位（Section 3.2），将高层语义注入生成流程。

2. **物体接触可供性解析**：基线方法依赖预设接触先验或简单混合SDS，难以泛化至开放集物体。InteractAnything 利用自适应修补与2D概率函数，从多视图解析任意物体的接触可供性（Section 3.3），使系统能处理未见过的物体几何。

3. **交互优化策略**：基线仅进行全局SDS优化，缺乏精细接触约束。InteractAnything 采用粗到细优化，加入力闭合损失和穿模惩罚（Section 3.5），显著提升接触真实感和物理合理性。

### 适用边界与局限

InteractAnything 的能力边界受以下因素制约：

**预训练模型依赖性**：生成质量高度依赖LLM与2D扩散模型的能力。LLM的语义推理可能出现幻觉或偏差，扩散模型的修补质量直接影响可供性解析的准确性。当输入文本描述模糊或物体几何极端复杂时，级联误差可能被放大。

**评估体系的局限性**：当前定量评估仅基于CLIP图像相似度和GPT-4V投票（Table 1、Table 2）。这两种指标侧重视觉合理性和语义对齐，无法全面衡量物理真实性、接触力分布和长期交互稳定性。消融实验（Table 3）虽验证了各模块的必要性，但评估维度仍以感知质量为主。

**人体模型的约束**：当前建模限于SMPL-H参数化人体，不支持非人代理（如机器人、动物）或具有不同骨架结构的交互对象，限制了框架向更广泛交互场景的迁移。

**多视角一致性**：尽管方法通过多视角SDS优化提升一致性，部分结果仍可能出现断裂或错位，尤其在遮挡严重或视角极端的场景中。

### 开放问题与后续方向

基于当前方法的局限，以下方向值得后续工作探索：

1. **时空连贯性增强**：如何利用多视角一致图像生成或4D生成技术，进一步提升3D交互在时间维度的连贯性，使生成的交互序列自然流畅？

2. **物理真实性验证**：力闭合损失仅是对物理真实性的粗略近似。如何构建高保真物理模拟器，全面验证接触力、摩擦、平衡等物理约束，是提升交互可信度的关键。

3. **跨代理泛化**：如何将框架扩展至非人交互代理（如机械臂、四足动物），处理其独特的骨架拓扑和运动约束？这需要重新设计姿态参数化和接触建模策略。

4. **多代理协同交互**：当前框架仅支持单人-单物交互。如何表示并生成多个交互代理之间的复杂协同关系（如两人搬动物体），是向更丰富场景拓展的必经之路。

5. **评估基准建设**：该领域缺乏标准化的3D HOI评估基准。构建包含物理真实性、接触精度、语义一致性等多维度的评估体系，将有力推动方法的横向对比和迭代。

## 原文 PDF

![[paperPDFs/CVPR_2025/InteractAnything_Zero_shot_Human_Object_Interaction_Synthesis_via_LLM_Feedback_and_Object_Affordanc.pdf]]
