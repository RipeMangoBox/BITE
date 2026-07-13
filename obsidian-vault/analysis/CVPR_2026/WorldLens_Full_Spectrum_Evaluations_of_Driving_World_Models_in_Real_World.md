---
title: "WorldLens: Full-Spectrum Evaluations of Driving World Models in Real World"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/WorldLens_Full_Spectrum_Evaluations_of_Driving_World_Models_in_Real_World.pdf
project_link: "https://worldbench.github.io/worldlens"
code_link: "https://github.com/worldbench/WorldLens"
aliases:
- WorldLens
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
- topic/generative_models_diffusion
- topic/benchmarks_datasets_evaluation
core_operator: 通过将世界模型评估解耦为生成、4D重建、动作跟随、下游任务和人类偏好五个维度，并在每个维度内设计可量化的子指标，系统性地暴露了视觉真实性与物理一致性之间的根本权衡，从而驱动模型向平衡发展。
primary_logic: 没有任何单一模型在所有维度上同时占据优势：视觉逼真的模型往往违反物理规律，几何稳定的模型缺乏行为保真度。这表明未来世界模型必须平衡视觉真实、几何一致、物理合理与功能可靠，而非追求单一维度的极致表现。
claims:
- 所有模型在Action-Following的Closed-Loop Adherence均崩溃，Route Completion仅为6.89%–13.51%，而Open-Loop PDMS可达71%–78%，说明开放环的视觉真实性无法转换为闭环控制的安全性。
- DiST-4D在下游任务（地图分割、3D检测、跟踪）中全面领先，平均超过第二名30–40%，但其在人类偏好的物理合理性上得分最高，显示了任务驱动的几何一致性优势。
- OpenDWM在生成质量（FVD、Subject Fidelity等）和重建（Photometric Error）上表现最佳，但3D检测和跟踪性能极差（NDS仅0.2196，AMOTA 6.9%），暴露了视觉与功能脱节。
- 使用真值帧作为条件的生成方法（如DiST-4D、DriveDreamer-2）在深度一致性和跨视角一致性上比无条件方法提升20–30%，表明物理grounding对逼真性至关重要。
---

# WorldLens: Full-Spectrum Evaluations of Driving World Models in Real World

> [!tip] 核心洞察
> 没有任何单一模型在所有维度上同时占据优势：视觉逼真的模型往往违反物理规律，几何稳定的模型缺乏行为保真度。这表明未来世界模型必须平衡视觉真实、几何一致、物理合理与功能可靠，而非追求单一维度的极致表现。

| 字段 | 内容 |
|------|------|
| 中文题名 | WorldLens：真实世界中驾驶世界模型的全谱评估 |
| 英文题名 | WorldLens: Full-Spectrum Evaluations of Driving World Models in Real World |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2512.10958) · [Project](https://worldbench.github.io/worldlens) · [Code](https://github.com/worldbench/WorldLens) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction #topic/generative_models_diffusion #topic/benchmarks_datasets_evaluation |
| Method | WorldLens |
| Dataset | Generation, Reconstruction, Action-Following, Downstream Task |

> [!tip] 效果简介
> - Generation 上，Perceptual Discrepancy (FVD, lower is better) DiST-4D: 58.08 vs MagicDrive: 222.00 (-163.92)。
> - Reconstruction 上，Photometric Error (LPIPS, lower is better) OpenDWM: 0.065 vs MagicDrive: 0.140 (-0.075 (reduction ~53%))。
> - Action-Following 上，Route Completion (↑) RLGF: 13.51% vs MagicDrive: 6.89% (+6.62%)。

## 概要

**核心瓶颈**：现有驾驶世界模型的评估长期局限于2D视觉逼真度指标（如FVD、LPIPS），系统性地忽视了几何一致性、物理合理性与行为安全性。这导致模型在视觉上看似真实，却在闭环控制与下游感知任务中频繁失效——视觉真实与物理行为之间存在严重失衡。

**核心发现**：WorldLens通过对10个代表性驾驶世界模型的全谱评估，揭示了一个根本性结论：**没有任何单一模型在所有维度上同时占据优势**。视觉逼真的模型往往违反物理规律（如OpenDWM在生成质量上最佳，但3D检测NDS仅0.2196）；几何稳定的模型又缺乏行为保真度。这指向一个明确方向——未来世界模型必须平衡视觉真实、几何一致、物理合理与功能可靠，而非追求单一维度的极致表现。

**方法定位**：WorldLens将评估解耦为五个互补维度——**生成**（视觉逼真度与语义一致性）、**4D重建**（几何一致性与新视角质量）、**动作跟随**（闭环仿真的行为可执行性）、**下游任务**（对3D感知模型的效用）和**人类偏好**（真实性、物理合理性与安全性的主观对齐）。整个框架覆盖24项可量化子指标，并引入WorldLens-26K人类标注数据集与WorldLens-Agent实现可扩展的人类对齐评分。

**方法谱系与知识库定位**：在驾驶世界模型评估领域，此前工作主要依赖生成式指标（如FVD、LPIPS）或单一任务指标，缺乏系统化的多维度基准。WorldLens填补了这一空白，其评估对象覆盖了当前主流方法：基于真值条件生成的**MagicDrive**（Gao et al., ICLR 2024）、**MagicDrive-V2**（Gao et al., ICCV 2025）、**DriveDreamer-2**（Zhao et al., AAAI 2025）、**Panacea**（Wen et al., CVPR 2024）、**DrivingSphere**（Yan et al., CVPR 2025），以及引入深度先验的**DiST-4D**（Li et al., ICCV 2025）和**OpenDWM**等。与现有工作不同，WorldLens并非提出新的生成模型，而是建立了一个统一的评估协议，使得不同设计选择（是否有真值条件、是否引入深度先验、是否进行强化学习微调）的优劣得以在统一尺度下量化比较。

**关键实证**：

- **动作跟随崩溃**：所有模型的闭环路线完成率（Route Completion）仅为6.89%–13.51%，而开环驾驶评分（PDMS）可达71%–78%，表明开放环的视觉真实性无法转换为闭环控制的安全性（Table 2, Section 5.1）。
- **任务驱动的几何优势**：DiST-4D在下游任务（地图分割、3D检测、跟踪）中全面领先，平均超过第二名30%–40%，同时在人类偏好的物理合理性上得分最高（Table 3, Figure 7, Section 5.1）。
- **视觉与功能脱节**：OpenDWM在生成质量（FVD、Subject Fidelity）和重建（Photometric Error）上表现最佳，但3D检测和跟踪性能极差（NDS仅0.2196，AMOTA 6.9%），暴露了视觉与功能之间的严重脱节（Table 1, Table 3, Section 5.1）。
- **物理grounding的价值**：使用真值帧作为条件的生成方法（如DiST-4D、DriveDreamer-2）在深度一致性和跨视角一致性上比无条件方法提升20%–30%，表明物理基础信息对逼真性至关重要（Table 1, Section 5.1）。

**局限与开放问题**：评估主要基于nuScenes数据集，对极端天气和罕见场景的泛化性有待验证；人类偏好标注仍受主观偏差影响；闭环仿真仅覆盖有限路线和预设规划器，未充分测试长尾交互场景。核心开放问题在于：如何在保持视觉逼真度的前提下，将闭环控制的物理合规性从当前不足14%的路线完成率大幅提升——这是视觉真实与行为安全之间的根本性瓶颈。

### 自动驾驶世界模型的演进与评估困境

自动驾驶系统依赖世界模型来预测未来场景的演变，从而支撑规划、决策与闭环仿真。近年来，基于扩散模型和自回归Transformer的生成式世界模型在视觉逼真度上取得了显著进展，涌现出 **MagicDrive**（Gao et al., ICLR 2024）、**DriveDreamer-2**（Zhao et al., AAAI 2025）、**DiST-4D**（Li et al., ICCV 2025）、**Panacea**（Wen et al., CVPR 2024）等一系列代表性工作。然而，这些模型的评估体系严重滞后于模型本身的演进。

### 现有评估的单一化瓶颈

当前驾驶世界模型的评估几乎完全聚焦于二维视觉生成指标，如Fréchet Video Distance（FVD）、LPIPS等感知相似度度量。这种评估范式存在一个根本性盲区：**视觉逼真度无法等同于物理合理性与行为安全性**。一个在像素层面高度逼真的生成视频，可能在几何结构上存在严重扭曲，在物理交互上违反基本规律，在闭环控制中导致灾难性后果。正如WorldLens实验所揭示的核心矛盾——所有模型在Action-Following的闭环路线完成率仅为6.89%–13.51%，而开放环的视觉质量指标可达71%–78%的PDMS（Predictive Driver Model Score），说明视觉真实与行为可靠之间存在巨大鸿沟。

### 缺失的评估维度

具体而言，现有评估体系至少遗漏了三个关键维度：

1. **几何一致性**：生成视频是否维持了场景的三维结构？跨视角、跨帧的几何信息是否稳定？缺乏这类评估导致模型可能产生“视觉逼真但几何崩塌”的输出，如MagicDrive和DreamForge在4D重建中暴露出密集漂浮物和几何畸变。

2. **功能性效用**：生成数据能否支撑下游感知任务（如3D检测、BEV分割、多目标跟踪）？OpenDWM在生成质量上表现优异（FVD最低、Subject Fidelity最高），但其3D检测NDS仅为0.2196，跟踪AMOTA仅6.9%，暴露了视觉与功能的严重脱节。

3. **人类感知对齐**：人类如何评判这些生成世界的真实性、物理合理性与安全性？缺乏系统化的人类评估使得模型优化方向可能与实际需求偏离。

### WorldLens的动机与设计哲学

WorldLens的核心动机正是填补上述评估鸿沟。其设计哲学是将世界模型的评估从单一的“视觉质量”解耦为**生成、4D重建、动作跟随、下游任务和人类偏好**五个互补维度，在24项可量化子指标上形成全谱评估体系。这一设计并非简单堆砌指标，而是系统性地暴露**视觉真实性与物理一致性之间的根本权衡**——正如实验所揭示的，没有任何单一模型在所有维度上同时占据优势：视觉逼真的模型（如OpenDWM）往往违反物理规律，几何稳定的模型（如DiST-4D）在行为保真度上仍有不足。这一发现指向一个明确结论：未来世界模型必须追求视觉真实、几何一致、物理合理与功能可靠之间的平衡发展，而非单一维度的极致表现。

## 核心方法与创新机理

### 从单维视觉评估到全谱物理-功能对齐

现有驾驶世界模型的评估范式被锁定在**2D视觉生成指标**（如FVD、LPIPS）的局部最优中，完全忽视了世界模型作为“可执行仿真器”所需的几何一致性、物理合理性与行为安全性。这一单维评估陷阱直接导致了一个被本文系统性暴露的根本矛盾：**视觉最逼真的模型，往往在物理世界中表现最差**。

WorldLens的核心创新在于将评估空间从单一的“生成质量”解耦为五个正交且互补的维度——生成、4D重建、动作跟随、下游任务与人类偏好——并在每个维度内部署可量化的细粒度子指标，共计24个维度。这一解耦设计并非简单的指标堆叠，而是通过**因果性瓶颈暴露**来驱动模型演进：当OpenDWM在生成质量（FVD、Subject Fidelity）和重建（Photometric Error）上全面领先，却在3D检测和跟踪上崩溃（NDS仅0.2196，AMOTA 6.9%）时，评估框架直接揭示了其“视觉真实—功能脱节”的致命缺陷。同样，当DiST-4D在下游任务中平均超越第二名30–40%，却在人类偏好的视觉真实感上并非最优时，框架精确量化了“几何一致性”与“感知逼真度”之间的权衡曲面。

### Changed Slots：评估覆盖与人类对齐的双重突破

WorldLens相对于既有评估范式的创新可归结为两个关键changed slots：

**Slot 1：评估覆盖范围——从2D视觉指标到全谱24维物理-功能评估。** 传统评估仅依赖FVD、LPIPS等感知相似度指标，这些指标在数学上衡量的是特征空间中的分布距离，却无法区分“一张逼真的幻觉”与“一个物理上可执行的场景”。WorldLens将评估空间扩展至：生成维度的8项指标（目标保真度、深度一致性、跨视角一致性等）、重建维度的6项指标（通过4D高斯泼溅暴露几何不稳定性）、动作跟随维度的闭环安全性指标（Route Completion、PDMS、ADS）、以及下游任务维度的4类感知任务效用（BEV分割、3D检测、跟踪、占用预测）。这一扩展的关键洞察在于：**4D重建充当了视觉生成与物理一致性之间的“测谎仪”**——任何时序上的几何不稳定都会在重建过程中以浮动物（floaters）和几何畸变的形式显性化（Figure 5），而这是FVD等指标完全无法捕捉的。

**Slot 2：人类对齐机制——从无系统化人类评估到可扩展的WorldLens-Agent。** 现有方法缺乏将人类对“物理合理性”和“行为安全性”的主观判断纳入评估的机制。WorldLens构建了WorldLens-26K数据集，通过四视图标注界面（生成视频、语义掩码、深度图、3D边界框）收集包含数值评分与文本解释的人类偏好标注，并在此基础上通过LoRA微调Qwen3-VL-8B得到WorldLens-Agent。该Agent的核心价值不在于替代人类，而在于**将昂贵的人类判断蒸馏为可规模化部署的评估信号**，使得未来新模型或新场景的评估无需重新进行大规模人工标注。

### 方法谱系与知识库定位

WorldLens在驾驶世界模型评估领域首次建立了系统性的基准框架，其定位介于**生成模型评估**与**具身AI安全性验证**的交汇处。与仅关注视觉质量的视频生成评估基准（如评估FVD、IS等）不同，WorldLens引入了物理grounding的评估维度；与仅关注闭环驾驶性能的仿真基准（如nuPlan、CARLA）不同，WorldLens将评估链条前移至生成内容本身的质量，建立了“生成质量—几何一致性—行为安全性”的因果链路。在方法论层面，其4D重建评估模块借鉴了**4D Gaussian Splatting**（Wu et al., ICLR 2024）作为几何探针的思想，但与用于新视角合成的原始目的不同，WorldLens将其重新定位为**生成世界时空一致性的诊断工具**。人类偏好模块则与RLHF范式形成呼应，但将其从策略优化领域迁移至世界模型评估的自动评分场景。

### 创新边界与待验证假设

需要指出的是，WorldLens的评估覆盖虽广，但其闭环仿真仅使用了预设驾驶规划器和有限路线，Route Completion的极低值（所有模型均低于14%）可能部分反映了规划器本身与生成世界之间的分布偏移，而非纯粹的世界模型安全性缺陷——这一混淆因素需要进一步消融实验来解耦。此外，WorldLens-Agent的泛化能力受限于26K条标注数据的分布，对于训练数据中未覆盖的新模型架构或极端场景，其评分校准性需要持续验证。

WorldLens 提出了一套全谱评估框架，将驾驶世界模型的评测从单一的视觉保真度解耦为五个互补维度：**生成（Generation）**、**重建（Reconstruction）**、**动作跟随（Action-Following）**、**下游任务（Downstream Task）** 和 **人类偏好（Human Preference）**。这五个维度覆盖了从低层外观逼真度到高层行为真实性的完整谱系，共细化为 24 项可量化子指标（Section 3）。

### 模块关系与数据流

框架的核心设计逻辑是 **“生成—重建—行为—任务—感知”** 的递进式验证链，各模块之间通过共享的生成视频输出形成级联依赖：

1. **生成评估器（Generation Evaluator）**：以真实驾驶视频为参考，对世界模型生成的视频进行八维分解评估，包括主体保真度（Subject Fidelity）、主体连贯性（Subject Coherence）、主体一致性（Subject Consistency）、深度差异（Depth Discrepancy）、时序一致性（Temporal Consistency）、语义一致性（Semantic Consistency）、感知差异（Perceptual Discrepancy）和跨视角一致性（Cross-View Consistency）（Section 3.1）。该模块的输出直接馈入后续所有评估环节。

2. **重建评估器（Reconstruction Evaluator）**：将生成视频重建为 4D 高斯泼溅场（4D Gaussian Fields），通过分析重建过程中的漂浮物（floaters）和几何不稳定性来暴露时空不一致性。评估指标包括光度误差（Photometric Error）、几何差异（Geometric Discrepancy）、新视角视觉质量（MUSIQ）和新视角差异（FVD on I3D features）（Section 3.2）。该模块是连接视觉质量与几何一致性的关键桥梁。

3. **动作跟随评估器（Action-Following Evaluator）**：在闭环仿真环境中，将生成的世界模型作为驾驶规划器的观测输入，测试其在真实交通流中的行为可执行性。核心指标包括开环预测驾驶模型分数（PDMS）和闭环路线完成率（Route Completion），最终综合为竞技场驾驶分数（ADS = RC × PDMS）（Section 3.3）。该模块揭示了视觉真实性与物理安全性之间的根本鸿沟。

4. **下游任务评估器（Downstream Task Evaluator）**：将生成视频统一缩放至 224×400 后，作为训练/测试数据输入标准 3D 感知模型，评估其对 BEV 地图分割、3D 目标检测、多目标跟踪和语义占用预测等任务的效用（Section 3.4）。该模块直接衡量生成数据的“功能可靠性”。

5. **人类偏好模块（Human Preference Module）**：构建了 WorldLens-26K 大规模人类标注数据集，标注界面同步展示生成视频、语义掩码、深度图和 3D 边界框四个视图（Figure 3），使标注者能够从真实性、物理合理性和安全性三个维度进行综合评分与文本解释（Section 3.5）。

6. **WorldLens-Agent**：基于 WorldLens-26K 数据集，通过 LoRA 监督微调将人类感知与物理判断蒸馏到 Qwen3-VL-8B 视觉语言模型中，形成一个可扩展的自动评估智能体（Section 4.3）。该智能体接收生成视频和多模态条件信号，输出数值评分与推理文本，实现了人类对齐评估的自动化（Figure 35）。

### 输入输出规范

- **统一输入**：所有评估均在 nuScenes 数据集上进行，使用统一的 6 相机配置和预处理流程。生成视频作为各模块的共同输入。
- **闭环仿真配置**：采用相同的交通流引擎（10 Hz）和驾驶规划器，控制信号统一为 2 Hz，确保公平比较。
- **下游任务输入**：生成视频统一缩放至 224×400，保证模型间的公平性。

### 核心洞察

该框架的设计直接回应了当前驾驶世界模型的真实瓶颈：**没有任何单一模型在所有维度上同时占据优势**。视觉逼真的模型（如 OpenDWM，生成 FVD 58.08）往往违反物理规律（3D 检测 NDS 仅 0.2196），而几何稳定的模型（如 DiST-4D，重建质量领先）在视觉丰富性上有所妥协。WorldLens 通过五维解耦评估，系统性地暴露了这种“视觉真实—物理一致—行为安全”之间的根本权衡，为未来世界模型的平衡发展提供了诊断工具。

### 补充图表

![[assets/figures/papers/paper_list_l2147_https_arxiv_org_abs_2512_10958/figures/001_Figure_1.jpg]]
*Figure 1: Is your driving world model an all-around player? This work presents WorldLens, a unified benchmark encompassing evaluations on 1Generation, 2Reconstruction, 3Action-Following, 4Downstream Task, and 5Human Preference, across a total of 24 dimensions spanning visual realism, geometric consistency, functional reliability, and perceptual alignment. We observe no single model dominates across all axes, highlighting the need for balanced progress toward physically and behaviorally realistic world modeling*

![[assets/figures/papers/paper_list_l2147_https_arxiv_org_abs_2512_10958/figures/002_Figure_2.jpg]]
*Figure 2: The WorldLens evaluation framework unifies five complementary aspects – 1Generation, 2Reconstruction, 3Action-Following, 4Downstream Task, and 5Human Preference – to assess visual, geometric, functional, and perceptual fidelity of generative world models. Each aspect is decomposed into interpretable dimensions driven by measurable signals such as segmentation, depth, 4D reconstruction, and behavioral simulation, enabling comprehensive and physically grounded evaluations across the full spectrum of world modeling*

WorldLens 将驾驶世界模型评估解耦为五个互补维度，每个维度内部署可量化的子指标，从而系统性地暴露视觉真实性与物理一致性之间的根本权衡。以下按评估流水线的核心模块展开，并给出关键公式及其变量含义。

### 生成评估器（Generation Evaluator）

生成评估器将整体生成质量分解为八个可解释维度，覆盖目标保真度、时序稳定性与语义一致性。其核心指标之一为 **Subject Fidelity Score**，用于衡量生成视频中每个检测目标类别的视觉保真度：

$$S_{\mathrm{SF}}(\mathcal{V}) = \frac{1}{N_g |\mathcal{C}|} \sum_{j=1}^{N_g} \sum_{c \in \mathcal{C}} \frac{1}{T} \sum_{t=1}^{T} \frac{1}{K_{j,c}^{(t)}} \sum_{k=1}^{K_{j,c}^{(t)}} p_{j,k}^{(t,c)}$$

其中 $\mathcal{V}$ 为生成视频集合，$N_g$ 为生成视频数量，$\mathcal{C}$ 为目标类别集合，$T$ 为视频帧数，$K_{j,c}^{(t)}$ 为第 $j$ 个视频第 $t$ 帧中类别 $c$ 的检测目标数，$p_{j,k}^{(t,c)}$ 为对应目标的二元分类器置信度。该指标聚合所有生成视频中每个检测目标的置信度，值越高表示目标级视觉保真度越强。

另一核心指标 **Perceptual Discrepancy**（即 Fréchet Video Distance, FVD）在 I3D 时空特征空间中计算真实视频分布与生成视频分布之间的 Fréchet 距离：

$$S_{\mathrm{PD}}(\boldsymbol{\mathcal{X}},\boldsymbol{\mathcal{Y}}) = \|\pmb{\mu_x} - \pmb{\mu_y}\|_2^2 + \operatorname{Tr}\biggl(\pmb{\Sigma_x} + \pmb{\Sigma_y} - 2\bigl(\pmb{\Sigma}_x^{1/2}\pmb{\Sigma_y}\pmb{\Sigma}_x^{1/2}\bigr)^{1/2}\biggr)$$

其中 $\boldsymbol{\mathcal{X}}$、$\boldsymbol{\mathcal{Y}}$ 分别为真实视频与生成视频的 I3D 特征分布，$\pmb{\mu}$ 为均值向量，$\pmb{\Sigma}$ 为协方差矩阵。值越低表示生成视频在感知层面越接近真实分布。

深度时序平滑性由 **Depth Discrepancy per video** 衡量，计算连续帧之间深度特征向量的欧氏距离变化：

$$DD(y_j) = \frac{1}{T-1} \sum_{t=1}^{T-1} \| f_j^{(t)} - f_j^{(t+1)} \|_2$$

其中 $f_j^{(t)}$ 为第 $j$ 个视频第 $t$ 帧由 DepthAnything V2 与 DINO 联合提取的深度特征向量。该值越小，表示深度时序越平滑，几何一致性越好。

### 重建评估器（Reconstruction Evaluator）

重建评估器通过将生成视频重建为 4D 高斯泼溅场（4D Gaussian Fields），评估其时空几何一致性。浮空伪影（floaters）和几何不稳定性直接暴露时序不一致性。该模块输出 Photometric Error（LPIPS）、Geometric Discrepancy 以及新视角质量（Novel-View Quality，以 MUSIQ 评分）和新视角差异（Novel-View Discrepancy，以 FVD 衡量）等指标。

### 动作跟随评估器（Action-Following Evaluator）

动作跟随评估器在闭环仿真中测试生成世界对驾驶规划器的行为可执行性。其核心综合指标为 **Predictive Driver Model Score (PDMS)**：

$$\mathrm{PDMS} = \Bigl( \prod_{m \in \{\mathrm{NC, DAC}\}} \mathrm{score}_m \Bigr) \cdot \frac{\sum_{w \in \{\mathrm{EP, TTC, C}\}} \mathrm{weight}_w \mathrm{score}_w}{\sum_{w \in \{\mathrm{EP, TTC, C}\}} \mathrm{weight}_w}$$

其中 NC 为无碰撞（No Collision），DAC 为可行驶区域合规（Drivable Area Compliance），EP 为自车进度（Ego Progress），TTC 为碰撞时间（Time to Collision），C 为舒适度（Comfort）。该公式将安全硬约束（乘积项）与驾驶质量软指标（加权和）结合，形成统一的驾驶评分。

最终闭环驾驶质量由 **Arena Driving Score (ADS)** 给出：

$$\mathrm{ADS} = \mathrm{RC} \times \mathrm{PDMS}$$

其中 RC 为路线完成率（Route Completion）。该乘积形式确保只有在安全完成路线的前提下才能获得高分，从而暴露视觉保真与行为可靠之间的鸿沟。

### 下游任务评估器（Downstream Task Evaluator）

下游任务评估器将生成视频统一缩放至 224×400 作为输入，在 BEV 分割、3D 目标检测、多目标跟踪和语义占用预测四个任务上评估生成数据的下游效用。该模块不引入新公式，而是直接复用各感知任务的标准化指标（如 NDS、AMOTA 等），以衡量生成世界对感知模型训练的数据增强价值。

### 人类偏好模块与 WorldLens-Agent

人类偏好模块构建了 WorldLens-26K 数据集，每条样本包含数值评分与文本解释，覆盖真实性、物理合理性与安全性维度。在此基础上，通过 LoRA 监督微调将 Qwen3-VL-8B 蒸馏为 **WorldLens-Agent**——一个反馈对齐的多模态评估智能体，能够对未见视频输出评分与推理文本，实现可扩展的人类对齐评估。该模块的蒸馏过程依赖 26K 条人类标注，其泛化能力受标注分布限制，对新模型或新场景需定期更新。

### 补充图表

![[assets/figures/papers/paper_list_l2147_https_arxiv_org_abs_2512_10958/figures/080_Figure_35.jpg]]
*Figure 35: The architecture of the proposed WorldLens-Agent for auto-evaluation of generated driving videos*

![[assets/figures/papers/paper_list_l2147_https_arxiv_org_abs_2512_10958/figures/003_Figure_3.jpg]]
*Figure 3: Interface for Human Preference annotation process. We present four synchronized views: 1generated video, 2semantic mask, 3depth map, and 43D bounding boxes, enabling comprehensive judgment of realism, physical plausibility, and consistency*

## 实验与关键发现

### 核心发现：视觉真实与物理行为之间的根本失衡

WorldLens在五个维度、24项子指标上对10个驾驶世界模型进行了全谱评估，核心结论清晰且强烈：**没有任何单一模型在所有维度上同时占据优势**。视觉逼真的模型往往违反物理规律，几何稳定的模型缺乏行为保真度，这种失衡构成了当前驾驶世界模型发展的核心瓶颈。

**Table 1** 汇总了生成与重建维度的量化结果。在生成质量方面，**OpenDWM** 表现最为均衡，其感知差异（FVD）为58.08，远优于MagicDrive的222.00，同时在Subject Fidelity等目标级保真度指标上也处于领先地位。然而，这种视觉逼真度的优势并未转化为几何一致性——在4D重建维度上，**DiST-4D** 在新视角质量（43.09%）上显著优于其他模型，其RGB-D生成设计有效提升了时空一致性，而MagicDrive和DreamForge则出现密集的浮点伪影和几何畸变（见 **Figure 5**）。

更深层的失衡暴露在动作跟随维度（**Table 2**）。所有模型的闭环路线完成率（Route Completion）均崩溃至6.89%–13.51%，即便是视觉质量最优的OpenDWM也仅有10.33%。与之形成鲜明对比的是，开放环预测驾驶模型评分（PDMS）可达71%–78%。这一鸿沟表明：**开放环的视觉真实性无法转换为闭环控制的安全性**，当前生成世界在物理合规性上存在系统性缺陷。

![[assets/figures/papers/paper_list_l2147_https_arxiv_org_abs_2512_10958/figures/007_Table_2.jpg]]
*Table 2: Benchmarking results of state-of-the-art driving world models for Action-Following dimensions in WorldLens*

### 下游任务：任务驱动的几何一致性优势

**Table 3** 展示了下游任务维度的量化结果。**DiST-4D** 在地图分割、3D检测和跟踪任务上全面领先，其3D检测NDS达0.3322，而OpenDWM仅0.2196；在多目标跟踪准确度（AMOTA）上，DiST-4D更是以25.9%远超OpenDWM的6.9%。这一反差极具启发性：OpenDWM在视觉生成上表现最佳，但在需要精确几何推理的下游任务中性能极差，暴露了**视觉逼真与功能可靠之间的严重脱节**。DiST-4D之所以在任务维度领先，根本原因在于其使用真值帧作为条件的设计，为生成过程注入了物理grounding信息，从而在几何一致性上获得优势。

### 人类偏好：物理合理性的主观验证

人类偏好评估（**Figure 7**）进一步印证了上述发现。在物理合理性维度上，DiST-4D的平均得分（2.583）显著高于MagicDrive（2.300），这与客观指标中DiST-4D在几何一致性和下游任务上的优势高度吻合。值得注意的是，人类标注者在评估过程中频繁使用“shape”、“reflection”、“motion”、“safety”等关键词（见 **Figure 4**），表明其判断与维度定义高度对齐，验证了WorldLens-26K数据集的标注质量。

![[assets/figures/papers/paper_list_l2147_https_arxiv_org_abs_2512_10958/figures/010_Figure_7.jpg]]
*Figure 7: Summary of alignments to Human Preference, where the max, median, and average scores of each model are compared. For more detailed analyses, kindly refer to the Appendix*

![[assets/figures/papers/paper_list_l2147_https_arxiv_org_abs_2512_10958/figures/005_Figure_4.jpg]]
*Figure 4: The statistics and word clouds of the WorldLens-26K dataset. Frequent keywords align closely with their target criteria (e.g., “shape”, “reflection”, “motion”, “safety”), confirming that annotators focus more on dimension-specific perceptual attributes and maintain consistent reasoning during the evaluation*

### 消融分析：物理grounding的关键作用

消融实验揭示了一个关键因果机制：**使用真值帧作为条件的生成方法在深度一致性和跨视角一致性上比无条件方法提升20–30%**。DiST-4D和DriveDreamer-2均采用条件生成策略，其在深度差异（Depth Discrepancy）和跨视角一致性指标上显著优于MagicDrive等无条件方法。这表明，物理基础信息对生成质量的影响并非边际性的，而是决定性的——缺乏物理grounding的世界模型本质上是在“画好看的画”，而非构建可操作的物理世界。

### 失败模式总结

综合所有实验结果，当前驾驶世界模型存在三类系统性失败模式：

1. **视觉-物理鸿沟**：所有模型的闭环路线完成率均低于14%，视觉保真度最高的模型在行为安全上并无优势，表明现有架构无法将像素级真实感转化为物理合规的驾驶行为。
2. **几何-功能脱节**：OpenDWM在生成质量上领先，但在3D检测和跟踪任务上表现极差，说明高质量像素生成与精确3D推理之间存在结构性矛盾。
3. **重建伪影**：MagicDrive和DreamForge在4D重建中出现密集浮点伪影（**Figure 5**），其几何差异（Geometric Discrepancy）超过OpenDWM两倍以上，揭示了时序一致性的根本缺陷。

![[assets/figures/papers/paper_list_l2147_https_arxiv_org_abs_2512_10958/figures/006_Figure_5.jpg]]
*Figure 5: Qualitative results of 4D reconstruction from generated videos. Rows (top to bottom) denote 1generated frame, 2rendered novel-view frame at a Lateral Offset, and 3depth map. MagicDrive [27] and DreamForge [69] exhibit dense floaters and geometric distortions, while OpenDWM [89] and DiST-4D [30] maintain temporally more consistent geometry, aligning with the quantitative results in Table 1*

这些失败模式共同指向一个结论：**未来世界模型必须平衡视觉真实、几何一致、物理合理与功能可靠，而非追求单一维度的极致表现**。WorldLens提供的全谱评估框架为这一平衡提供了可量化的度量体系。

### 补充图表

![[assets/figures/papers/paper_list_l2147_https_arxiv_org_abs_2512_10958/figures/004_Table_1.jpg]]
*Table 1: Benchmarking results of state-of-the-art driving world models for Generation and Reconstruction in WorldLens*

![[assets/figures/papers/paper_list_l2147_https_arxiv_org_abs_2512_10958/figures/008_Table_3.jpg]]
*Table 3: Summary of benchmarking results of state-of-the-art world models for Downstream Task dimensions in WorldLens*

![[assets/figures/papers/paper_list_l2147_https_arxiv_org_abs_2512_10958/figures/009_Figure_6.jpg]]
*Figure 6: Qualitative results of Downstream Tasks. Rows (from top to bottom): 13D object detection, 2map segmentation, and 3semantic occupancy prediction tasks*

## 定位与知识库关联

### 评估范式的根本转向：从单一视觉保真到全谱物理-功能对齐

WorldLens的核心贡献不在于提出新的生成模型，而在于重新定义了驾驶世界模型的评估框架。传统评估体系仅依赖2D视觉生成指标（如FVD、LPIPS），导致模型在视觉逼真度上过度优化，却忽视了几何一致性、物理合理性和行为安全性。WorldLens将评估解耦为**生成、4D重建、动作跟随、下游任务和人类偏好**五个互补维度，覆盖24项可量化子指标，系统性地暴露了视觉真实性与物理一致性之间的根本权衡。

这一转向的因果逻辑是：**视觉逼真≠物理可靠≠功能有用**。现有驾驶世界模型在这三个层次上的表现严重失衡——视觉最逼真的模型（如OpenDWM）在下游3D检测任务上表现极差（NDS仅0.2196），而几何最稳定的模型（如DiST-4D）在人类偏好的物理合理性上得分最高（2.583 vs. MagicDrive的2.300）。WorldLens通过多维度解耦，迫使社区正视这一失衡，而非继续在单一维度上“刷榜”。

### 与被评估模型的方法论关系

WorldLens评估了10个代表性的驾驶世界模型，它们代表了当前方法谱系中的主要技术路线：

**条件生成路线（真值帧引导）**：**DiST-4D**（Li et al., ICCV 2025）和**DriveDreamer-2**（Zhao et al., AAAI 2025）使用真值帧作为条件输入，在深度一致性（Depth Discrepancy）和跨视角一致性上比无条件方法提升20–30%。DiST-4D的RGB-D联合生成设计使其在4D重建质量上显著领先（Novel-View Quality达43.09%），证明了**深度先验对时空一致性的直接增益**。**MagicDrive**（Gao et al., ICLR 2024）和**MagicDrive-V2**（Gao et al., ICCV 2025）属于同一技术路线的迭代版本。

**无条件/大规模训练路线**：**OpenDWM**通过大规模多数据集训练，在生成质量（FVD、Subject Fidelity）和重建（Photometric Error 0.065，为所有模型中最低）上表现最佳，但其3D检测和跟踪性能极差（AMOTA仅6.9%），暴露了**视觉与功能脱节**的典型症状。

**物理感知路线**：**RLGF**（Yan et al., NeurIPS 2025）在动作跟随的闭环路线完成率上表现最好（13.51%），但仍远未达到实用水平，说明当前方法在**视觉真实到行为安全的转换**上存在根本性瓶颈。

**其他评估模型**：**Panacea**（Wen et al., CVPR 2024）、**DrivingSphere**（Yan et al., CVPR 2025）、**DreamForge**、**X-Scene**等代表了不同的生成架构选择，但在WorldLens的全谱评估下均未展现出跨维度的全面优势。

### 关键因果发现与瓶颈定位

WorldLens的核心洞察是**没有任何单一模型在所有维度上同时占据优势**，这一发现具有可验证的因果链条：

1. **视觉-物理失衡**：OpenDWM在生成和重建上表现最佳，但3D检测NDS仅为DiST-4D的66%（0.2196 vs. 0.3322），说明视觉逼真并不自动转化为几何-功能可用性。

2. **开放环-闭环鸿沟**：所有模型在开放环的Predictive Driver Model Score（PDMS）可达71%–78%，但闭环Route Completion仅为6.89%–13.51%，表明**当前生成世界在闭环控制中普遍缺乏安全性**。这一鸿沟是WorldLens暴露的最关键瓶颈。

3. **物理grounding的因果作用**：使用真值帧作为条件的生成方法（DiST-4D、DriveDreamer-2）在深度一致性和跨视角一致性上系统性优于无条件方法，证明了**物理基础信息对生成质量至关重要**，而非单纯的模型规模或数据量。

4. **任务驱动的几何优势**：DiST-4D在下游任务（地图分割、3D检测、跟踪）中全面领先，平均超过第二名30–40%，同时其人类偏好的物理合理性得分最高，显示了**任务驱动的几何一致性优势**可以同时提升功能可靠性和人类感知质量。

### 适用边界与局限

WorldLens的评估框架和结论受以下边界条件约束：

**数据覆盖边界**：评估数据集主要基于nuScenes，可能无法完全覆盖复杂天气、极端光照和罕见交通场景。在暴雨、暴雪、强逆光等条件下的泛化性有待验证，当前结论不应直接外推至这些场景。

**人类标注的主观性**：WorldLens-26K的人类偏好标注虽经过两轮独立评判与复核，但仍受标注者主观偏差影响。特别是“行为安全”维度与客观安全指标（如碰撞率）之间的定量关系尚未建立，人类对“安全”的感知可能与实际安全性能存在系统偏差。

**闭环仿真的简化性**：闭环仿真仅使用了有限的路线和预设驾驶规划器，未能充分测试长尾交互和动态紧急情况。实际部署环境中的行为可能比当前13.51%的最高路线完成率更差。

**WorldLens-Agent的泛化局限**：WorldLens-Agent的蒸馏过程依赖26K条人类标注，对新模型架构或新场景分布的泛化能力可能有限。随着世界模型规模增大和生成质量提升，Agent的评分分布可能发生偏移，需要定期更新标注数据集和重训模型。

**评估框架的静态性**：当前评估框架基于预定义的维度和指标，可能无法捕捉未来世界模型的新能力或新失败模式。框架本身需要随技术发展而演进。

### 开放问题与知识库定位

WorldLens揭示了驾驶世界模型领域的几个根本性开放问题：

1. **视觉-行为鸿沟的弥合**：如何在保持视觉逼真度的前提下，显著提升闭环控制的物理合规性？当前所有模型的道路完成率均低于14%，说明视觉真实与行为安全之间存在根本性瓶颈，而非简单的工程优化问题。

2. **评估范式的跨领域迁移**：能否将WorldLens的全谱评估范式扩展至其他具身AI场景（如室内导航、机器人操作），形成一个统一的具身世界模型评测标准？这需要重新定义各领域的“物理合理性”和“行为安全性”维度。

3. **人类偏好与客观安全的校准**：人类偏好中的“行为安全”维度与客观安全指标（如碰撞率、TTC）之间的定量关系是什么？能否用模拟安全分数直接校准人类标签，从而降低标注成本？

4. **评估框架的持续演化**：随着世界模型规模增大和能力提升，如何在不显著增加标注成本的前提下，更新WorldLens-26K并重训WorldLens-Agent，以保持评估的时效性和区分度？

**知识库定位**：WorldLens在驾驶世界模型领域确立了**首个全谱评估基准**的地位，其核心贡献是揭示了视觉真实性与物理-功能可靠性之间的根本权衡，并提供了可量化的多维评估工具。该工作应被定位为**评估方法论的基础设施**，而非生成模型本身。后续工作应引用WorldLens作为标准评估协议，并在其揭示的瓶颈（特别是闭环行为安全）上进行针对性改进。

## 原文 PDF

![[paperPDFs/CVPR_2026/WorldLens_Full_Spectrum_Evaluations_of_Driving_World_Models_in_Real_World.pdf]]
