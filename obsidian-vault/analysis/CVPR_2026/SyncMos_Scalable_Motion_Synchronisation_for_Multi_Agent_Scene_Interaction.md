---
title: "SyncMos: Scalable Motion Synchronisation for Multi-Agent Scene Interaction"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/SyncMos_Scalable_Motion_Synchronisation_for_Multi_Agent_Scene_Interaction.pdf
project_link: null
code_link: null
aliases:
- SyncMos
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/generative_models_diffusion
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: 时间扭曲控制与扩散后验采样 (Time-warping & Diffusion Posterior Sampling)
primary_logic: 将自然语言指令解析为带有时序依赖的结构化事件图，并利用时间扭曲与扩散先验相结合，在不额外训练的情况下实现多智能体运动的时间同步和可扩展生成。
claims:
- 在Synchronisation子集上，所提规划器的依赖准确率（DA）较基线最高提升21.5个百分点（68.4% → 89.9%）
- 对于±0.5 s的时间偏移，抓取时序同步成功率可达88.0%（-0.5 s）和84.7%（+0.5 s），而基线LINGO为0%
- 在10智能体链式交互中，时序同步误差（TSE）保持稳定，无误差累积
- Synchronisation subset 上 Dependency Accuracy (DA) = 89.9% (with Qwen-3-235B)
---

# SyncMos: Scalable Motion Synchronisation for Multi-Agent Scene Interaction

> [!tip] 核心洞察
> 将自然语言指令解析为带有时序依赖的结构化事件图，并利用时间扭曲与扩散先验相结合，在不额外训练的情况下实现多智能体运动的时间同步和可扩展生成。

| 字段 | 内容 |
|------|------|
| 中文题名 | SyncMos: 面向多智能体场景交互的可扩展运动同步 |
| 英文题名 | SyncMos: Scalable Motion Synchronisation for Multi-Agent Scene Interaction |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://openaccess.thecvf.com/content/CVPR2026/html/Li_SyncMos_Scalable_Motion_Synchronisation_for_Multi-Agent_Scene_Interaction_CVPR_2026_paper.html) |
| Topic | #topic/vision_multimodal_applications #topic/generative_models_diffusion #topic/vision_multimodal_applications/image_and_video_generation |
| Method | SyncMos |
| Dataset | Synchronisation subset, Dependency subset, Grasp Timing Control, Multi-agent Scalability |

> [!tip] 效果简介
> - Synchronisation subset 上，Dependency Accuracy (DA) 89.9% (with Qwen-3-235B) vs 68.4% (Event-Driven Storytelling, same LLM) (+21.5 p.p.)。
> - Dependency subset 上，Scenario Pass Rate (SPR) 80.0% (with GPT-4o) vs ~0% (Event-Driven Storytelling) (+80.0 p.p.)。
> - Grasp Timing Control 上，Success Rate at -0.5s offset 88.0% vs 0.0% (LINGO) (+88.0 p.p.)。

## 概要

多智能体运动生成的核心瓶颈在于：现有方法难以灵活扩展至可变数量的智能体，且缺乏跨智能体的时间同步机制，导致交互时间错位或行为不一致。**SyncMos** 针对这一瓶颈，提出了一种无需额外训练即可实现多智能体运动时间同步和可扩展生成的框架。其核心思路是将自然语言指令解析为带有时序依赖的结构化事件图，并利用**时间扭曲（Time-warping）与扩散后验采样（Diffusion Posterior Sampling）** 相结合，在单智能体扩散运动生成模型的基础上实现跨智能体的时序对齐。

SyncMos 由两个关键组件构成：**高层事件规划器**（High-level Event Planner）将用户文本指令转化为带有时序依赖的结构化事件图，明确事件间的顺序与并行关系；**低层时间同步模块**（Temporal Synchronisation Module）则通过自回归初步估计与时间引导细化两个阶段，对每个智能体的运动序列进行时间扭曲和梯度引导的去噪优化，从而实现全局时间一致性。

实验结果表明，SyncMos 在同步子集上的依赖准确率（DA）较基线最高提升 **21.5 个百分点**（68.4% → 89.9%），在抓取时序控制任务中，对于 ±0.5 s 的时间偏移，成功率可达 **88.0%** 和 **84.7%**，而基线方法 LINGO（Jiang et al., SIGGRAPH Asia 2024）在此设置下成功率为 0%。在 10 智能体的链式交互场景中，时序同步误差（TSE）保持稳定，无误差累积现象，验证了框架在多智能体扩展场景下的鲁棒性。

多智能体场景交互生成是计算机视觉与图形学中的核心挑战，其目标是根据自然语言指令，生成多个虚拟角色在共享三维空间中协调一致的运动序列。这一任务在电影制作、游戏开发、虚拟现实及具身智能仿真中具有广泛的应用前景。

当前的运动生成研究主要由扩散模型驱动，在单智能体条件下已取得显著进展。以 **LINGO**（Jiang et al., SIGGRAPH Asia 2024）为代表的单智能体扩散运动生成骨干，能够根据文本描述生成高质量的三维人体运动。然而，当场景从单个角色扩展至多个交互角色时，现有方法暴露出两个根本性瓶颈。

**瓶颈一：可扩展性缺失。** 现有多智能体运动生成方法通常针对固定数量的智能体进行设计，难以灵活扩展至可变数量的角色。当智能体数量增加时，运动空间呈组合爆炸式增长，直接沿用单智能体自回归生成范式将面临计算与建模的双重困境。

**瓶颈二：跨智能体时间同步空白。** 多智能体交互的本质要求不同角色的动作在时间维度上精确对齐——例如，角色A伸手抓取物体时，角色B必须在对应时刻完成递送动作。然而，现有方法缺乏显式的跨智能体时间同步机制，导致交互时间错位或行为不一致。以 **Event-Driven Storytelling**（Lim et al., ICCV 2025）为代表的高层事件规划基线虽然尝试进行事件级组织，但未引入结构化时序依赖推理，无法有效解析事件间的顺序与并行关系。

上述瓶颈共同指向一个核心因果调节变量：**时间扭曲控制与扩散后验采样**。SyncMos的核心洞察在于，若能将自然语言指令解析为带有时序依赖的结构化事件图，并利用时间扭曲与扩散先验相结合，便可在不额外训练运动生成模型的前提下，实现多智能体运动的时间同步和可扩展生成。

具体而言，SyncMos通过两级架构解决这一挑战：高层规划器将自由文本指令转化为包含顺序（Seq）与并行（Par）依赖关系的事件图，为多角色交互提供结构化的时序蓝图；低层控制器则在单智能体扩散模型的去噪过程中引入时间一致性约束，通过梯度引导的扩散后验采样实现跨智能体的运动时间对齐。这一设计使得框架本身与运动生成骨干解耦，具备天然的模型无关性和可替换性。

本文围绕上述动机展开，后续章节将依次阐述高层事件规划器的设计、时间同步模块的机制，以及在不同规模交互场景下的实验验证。

## 核心方法与创新机理

SyncMos 的核心创新在于将**结构化事件依赖规划**与**无需额外训练的时间同步机制**相结合，解决了现有多智能体运动生成中的两个根本瓶颈：跨智能体时间错位与智能体数量的不可扩展性。

### 1. 从单智能体生成到多智能体协同：范式转变

现有方法（如 **LINGO**, Jiang et al., SIGGRAPH Asia 2024）采用直接的单智能体自回归生成范式，缺乏显式的跨智能体时间同步机制。SyncMos 将范式转变为**基于结构化事件规划的多智能体协同自回归生成**（Sec 3, Fig. 1），使运动生成从孤立个体行为升级为时序协调的群体交互。

### 2. 时间扭曲控制与扩散后验采样：无需训练的同步机制

SyncMos 的核心操控变量是**时间扭曲控制与扩散后验采样（DPS）**。该机制在不额外训练运动生成模型的前提下实现跨智能体时间对齐，其工作原理如下：

- **初步运动估计**：利用单智能体扩散模型自回归生成粗运动序列，在部分去噪步数 $t=30$ 处提取预测干净数据 $\hat{\mathbf{x}}_0$：
  $$\hat{\mathbf{x}}_0 = \frac{1}{\sqrt{\bar{\alpha}}} \left( \mathbf{x}_t - \sqrt{1 - \bar{\alpha}} \epsilon_\theta(\mathbf{x}_t, t) \right)$$

- **时间引导细化**：通过样条时间扭曲构造目标序列 $\mathbf{y}$，再以 L2 约束 $C(\hat{\mathbf{x}}_0) = \|\mathbf{y} - \hat{\mathbf{x}}_0\|^2$ 引导扩散反向过程，梯度更新步骤为：
  $$\mathbf{x}_{i-1} \leftarrow \mu_\theta(\mathbf{x}_i, i) - \lambda \nabla_{x_i} C(\hat{\mathbf{x}}_0) + \sigma_i \mathbf{z}$$

这一设计使同步模块与运动生成骨干解耦，框架本身与模型无关，未来可替换更强的单智能体生成器。

### 3. 依存感知事件图：高层规划的结构化创新

SyncMos 将自然语言指令解析为**带有时序依赖的结构化事件图** $G = (E, R)$，其中 $R = R_{\mathrm{seq}} \cup R_{\mathrm{par}}$ 显式建模顺序与并行两种依赖关系（Sec 4.2）。相比 **Event-Driven Storytelling**（Lim et al., ICCV 2025）的无结构化时序推理，这一设计使规划器在 Synchronisation 子集上的依赖准确率（DA）最高提升 21.5 个百分点（68.4% → 89.9%，Qwen-3-235B，Table 1），在 Dependency 子集上的场景通过率（SPR）从约 0% 提升至 80.0%（GPT-4o，Table 1）。

### 4. 关键创新总结

| 创新维度 | 基线方法 | SyncMos 方案 | 证据强度 |
|---------|---------|-------------|---------|
| 运动生成范式 | 单智能体自回归生成 | 多智能体协同自回归生成 | 高（Sec 3, Fig. 1） |
| 时间控制方式 | 无显式跨智能体同步 | 时间扭曲 + DPS 约束细化 | 高（Sec 5.2, Algorithm 2） |
| 高层规划 | 无结构化事件依赖图 | LLM 驱动的依存感知事件图 | 高（Sec 4.2, Table 1） |

这些创新共同使 SyncMos 在 10 智能体链式交互中保持时序同步误差（TSE）稳定、无误差累积（Figure 6），验证了框架的可扩展性。

SyncMos 的整体架构遵循“高层规划—低层同步”的两阶段范式，旨在将自然语言指令转化为多智能体时空一致的运动序列。如图 1 所示，系统首先通过**高层事件规划器**（High-level Event Planner）将用户文本解析为带有显式时序依赖的结构化事件图；随后，**低层运动同步模块**（Low-level Motion Synchronisation Module）以该事件图为引导，对每个智能体并行生成初步运动估计，并通过时间扭曲与扩散后验采样实现跨智能体的精细时间对齐。

### 输入输出流

- **输入**：一段描述多智能体交互场景的自然语言指令（如“Amir 将瓶子递给 Benjamin，然后 Benjamin 将其放在桌上”），以及对应的 3D 场景信息。
- **高层输出**：一个事件依赖图 $G = (E, R)$，其中 $E = \{e_i\}_{i=1}^N$ 为各智能体的原子事件集合，$R = R_{\mathrm{seq}} \cup R_{\mathrm{par}}$ 定义了事件间的顺序（Seq）与并行（Par）时序关系。每个事件 $e_i$ 被进一步落地为俯视图网格上的空间表示 $g_i = (\mathtt{grid}_i, \mathsf{action}_i, \mathtt{hand\_target}_i)$，包含 2D 坐标、动作标签及可选的交互物体。
- **低层输出**：所有智能体的时间同步运动序列，可直接驱动角色动画。

### 模块关系与协作

框架的核心设计在于**高层规划与低层控制的解耦**：规划器负责“做什么、谁做、何时做”的语义与逻辑推理，而同步模块负责“如何做”的运动生成与时间对齐。这种解耦带来了两个关键优势：

1. **可扩展性**：低层同步模块基于单智能体扩散运动生成模型（以 **LINGO** (Jiang et al., SIGGRAPH Asia 2024) 为骨干），通过自回归方式为任意数量的智能体生成初步运动，无需针对不同智能体数量重新训练。
2. **时间同步能力**：在初步估计阶段（Auto-Regressive Preliminary Estimation，Algorithm 1），系统利用部分去噪（partial denoising）从扩散模型中提取每个智能体的粗运动序列；随后在时间引导细化阶段（Temporally Guided Refinement，Algorithm 2），通过样条时间扭曲构建目标序列 $\mathbf{y}$，并以梯度引导的去噪过程强制执行时间一致性约束 $C(\hat{\mathbf{x}}_0) = \|\mathbf{y} - \hat{\mathbf{x}}_0\|^2$，从而在不额外训练的条件下实现跨智能体运动的时间对齐。

### 关键设计选择

- **俯视图空间推理**：高层规划器将 3D 场景投影为统一的 2D 俯视图网格（Figure 3），使抽象的自然语言指令能够在共享坐标系中进行空间落地。这一设计简化了多智能体交互位置的一致性约束，但也限制了精细 3D 接触推理的能力。
- **模型无关的同步机制**：时间同步模块不依赖特定的运动生成骨干。当前实现使用 LINGO 作为单智能体生成器，但框架本身可替换为更强的扩散模型，同步性能的上限随之提升。
- **部分去噪步数选择**：初步估计阶段采用 $t=30$ 的部分去噪步数，在生成质量与计算成本之间取得平衡。该超参数的选择对泛化性的影响仍是一个开放问题（见补充材料分析）。

整体而言，SyncMos 通过将结构化事件规划与扩散后验采样相结合，首次在多智能体运动生成中实现了无需额外训练的时间同步与可扩展生成，其架构的模块化设计为后续纳入物理约束或更复杂的交互类型预留了明确的接口。

![[assets/figures/papers/paper_list_l2279_https_openaccess_thecvf_com_content_CVPR2026_html_Li_SyncMos_Scalable_Mo/figures/001_Figure_1.jpg]]
*Figure 1: Overall architecture. The framework first interprets the user’s input via a high-level planner, and low-level controller synchronizes the timing of each-character*

SyncMos 围绕“高层事件规划 + 低层时间同步”两级架构展开，其核心模块可归纳为三个关键环节：**依存感知的故事规划器**、**自回归初步运动估计**，以及**时间引导的扩散后验细化**。以下从公式与机制层面逐一解析。

### 依存感知事件图构建

高层规划器将自然语言指令解析为结构化的**事件依赖图**（Event Dependency Graph）：

$$G = ( E , R ) , \quad E = \{ e _ { i } \} _ { i = 1 } ^ { N } , \quad R = R _ { \mathrm { s e q } } \cup R _ { \mathrm { p a r } }$$

其中 $E$ 为 $N$ 个单智能体事件集合，$R$ 为时序依赖关系，分为**顺序依赖** $R_{\mathrm{seq}}$ 与**并行依赖** $R_{\mathrm{par}}$ 两类。这一显式依赖建模是后续时间同步的结构化约束来源——若两个事件被标注为 $R_{\mathrm{seq}}$，则前驱事件必须在后继事件开始前完成；若为 $R_{\mathrm{par}}$，则两者可重叠执行。

随后，每个抽象事件 $e_i$ 通过俯视图空间推理被**落地**为可操作的表示：

$$g _ { i } = ( \mathtt { g r i d } _ { i } , \mathsf { a c t i o n } _ { i } , \mathtt { h a n d } _ { - } \mathtt { t a r g e t } _ { i } )$$

其中 $\mathtt{grid}_i$ 为 2D 俯视图网格坐标，$\mathsf{action}_i$ 为动作标签（如 “hand over”），$\mathtt{hand\_target}_i$ 为可选的交互物体标识。该表示将语言级事件统一映射到共享空间坐标系，为多智能体运动生成提供空间一致性锚点。

### 自回归初步估计中的去噪深度控制

低层运动生成基于单智能体扩散模型（以 **LINGO** 为骨干，Jiang et al., SIGGRAPH Asia 2024），采用**部分去噪**策略进行自回归初步估计（Algorithm 1）。其核心机制是利用 DDPM 从噪声样本中估计干净运动数据：

$$\hat { \mathbf { x } } _ { \mathbf { 0 } } = \hat { x } _ { 0 } ( \mathbf { x } _ { \mathbf { t } } , t ) = \frac { 1 } { \sqrt { \bar { \alpha } } } \left( \mathbf { x } _ { \mathbf { t } } - \sqrt { 1 - \bar { \alpha } } \epsilon _ { \theta } ( \mathbf { x } _ { \mathbf { t } } , t ) \right)$$

这里 $\mathbf{x}_t$ 为扩散时间步 $t$ 处的含噪样本，$\bar{\alpha}$ 为噪声调度参数，$\epsilon_\theta$ 为噪声预测网络。预测干净数据与真实干净数据之差由下式给出：

$$\hat { \mathbf { x } } _ { \mathbf { 0 } } - \mathbf { x } _ { \mathbf { 0 } } = \frac { \sqrt { 1 - \bar { \alpha } } } { \sqrt { \bar { \alpha } } } \left( \epsilon - \epsilon _ { \theta } \left( \mathbf { x _ { t } } , t \right) \right)$$

该关系揭示了**去噪深度**的本质：当 $t$ 较大时，$\bar{\alpha}$ 较小，系数 $\frac{\sqrt{1-\bar{\alpha}}}{\sqrt{\bar{\alpha}}}$ 较大，预测误差被放大，意味着从含噪样本中恢复的干净估计不确定性更高。SyncMos 选择 $t=30$ 作为部分去噪步数，在保留足够运动结构信息的同时，为后续时间细化保留可编辑空间（详见补充材料对 $t$ 取值的消融分析）。

### 时间引导细化的梯度约束机制

初步估计完成后，SyncMos 通过**时间扭曲控制 + 扩散后验采样（DPS）** 实现跨智能体时间对齐（Algorithm 2）。首先对初步序列 $\mathbf{D}$ 施加样条基时间扭曲，构造目标序列 $\mathbf{y}$；随后在扩散反向过程中引入 L2 一致性约束：

$$C ( \hat { \mathbf { x } } _ { \mathbf { 0 } } ) = \| \mathbf { y } - \hat { \mathbf { x } } _ { \mathbf { 0 } } \| ^ { 2 }$$

该约束强制细化后的运动逼近时间对齐后的目标。将此约束以梯度引导的方式注入去噪步骤：

$$\mathbf { x _ { i - 1 } } = \mu _ { \theta } ( \mathbf { x _ { i } } , i ) - \lambda \nabla _ { x _ { i } } C ( \hat { \mathbf { x } } _ { \mathbf { 0 } } ) + \sigma _ { i } \mathbf { z }$$

其中 $\mu_\theta$ 为标准 DDPM 反向均值，$\lambda$ 为引导强度，$\sigma_i \mathbf{z}$ 为随机噪声项。梯度项 $-\lambda \nabla_{x_i} C$ 将时间一致性约束反向传播至去噪轨迹，使生成的运动在保持扩散先验质量的同时，满足跨智能体的时序对齐要求。

**关键设计意图**：该公式将时间同步建模为扩散后验采样问题，而非额外训练一个同步模块。这意味着 SyncMos 的同步能力**与运动骨干解耦**——理论上可替换任意单智能体扩散生成器，只需在推理时注入上述梯度引导即可。这一“免训练”特性是方法可扩展性的核心支撑。

### 模块间的因果链路

上述三个模块形成清晰的因果链：事件依赖图（$G$）定义了“谁在何时做什么”的结构化约束 → 自回归初步估计在事件引导下生成各智能体的粗运动序列 → 时间引导细化利用 DPS 梯度约束消除跨智能体的时间错位。实验表明，该链路在 10 智能体链式交互中时序同步误差（TSE）保持稳定，无误差累积（Figure 6），验证了公式推导中梯度引导机制的有效性。

![[assets/figures/papers/paper_list_l2279_https_openaccess_thecvf_com_content_CVPR2026_html_Li_SyncMos_Scalable_Mo/figures/002_Figure_2.jpg]]
*Figure 2: The high-level event planner overview. The high-level planner organizes dependencies while determining event locations*

![[assets/figures/papers/paper_list_l2279_https_openaccess_thecvf_com_content_CVPR2026_html_Li_SyncMos_Scalable_Mo/figures/003_Figure_3.jpg]]
*Figure 3: The top-view grid provides a unified 2D spatial coordinate system for grounding instructions. The instruction “Amir hands over the bottle to Benjamin at grid (10, 18)” specifies an action location on the grid (left), which corresponds to the same position in the 3D scene (right). This grounding enables spatial consistency in later motion generation stages*

## 实验与关键发现

### 评估设置

SyncMos 的实验从两个维度展开：**高层规划器的能力**与**低层时间同步模块的性能**。高层规划器在 Synchronisation 和 Dependency 两个子集上评估，指标包括事件覆盖率（Event Coverage, EC）、依赖准确率（Dependency Accuracy, DA）、通过场景数（Passed Scenarios, PS）和场景通过率（Scenario Pass Rate, SPR）。低层同步模块则围绕抓取时序控制（Grasp Timing Control）和多智能体可扩展性（Multi-agent Scalability）展开，核心指标为时序同步成功率、时序同步误差（Temporal Sync Error, TSE）以及时序同步度量（Temporal Sync Metric, TSM）。初步运动估计采用部分去噪步数 $t=30$，时间对齐通过动态时间规整（DTW）进行量化评估。

### 高层规划器性能

**Table 1** 汇总了不同 LLM 骨干下规划器在两个子集上的表现。在 Synchronisation 子集上，SyncMos 规划器在 Qwen-3-235B 骨干下实现了 **89.9% 的依赖准确率（DA）**，较 Event-Driven Storytelling 基线（**Lim et al., ICCV 2025**）的 68.4% 提升了 **21.5 个百分点**。在更具挑战性的 Dependency 子集上，基线的 DA 仅为 11.8%–20.5%，而 SyncMos 规划器将 DA 提升至 **80%–97%**，场景通过率（SPR）从近乎 0% 跃升至 **80.0%**（GPT-4o 骨干）。不同 LLM 骨干（GPT-4o、Qwen-3-235B 等）间的性能虽有波动但均保持较高水平，验证了框架对底层语言模型的鲁棒性。

### Token 效率分析

**Figure 5** 展示了 Token 用量随事件数量变化的趋势。在 Synchronisation 场景下，SyncMos 规划器每个案例的 Token 消耗稳定在约 **10k tokens**，且随着事件数量增加，EC、DA 和 SPR 保持稳定。相比之下，Event-Driven Storytelling 基线的 Token 用量随事件数急剧增长，表明 SyncMos 的依赖感知事件图表示在计算效率上具有显著优势。

### 时间同步与抓取时序控制

**Table 2** 报告了不同时间偏移下的抓取时序控制成功率。对于 **±0.5 s 的偏移**，SyncMos 的成功率分别达到 **88.0%（−0.5 s）和 84.7%（+0.5 s）**，而单智能体扩散骨干 **LINGO**（**Jiang et al., SIGGRAPH Asia 2024**）在相同条件下成功率为 0%，凸显了时间同步模块的核心价值。在 ±1.0 s 偏移下，成功率仍维持在 70% 以上（75.3% 和 78.0%）。当负向偏移扩大至 −1.5 s 时，成功率降至 37.3%，论文指出这主要源于时间偏移量不足而非轨迹方差增大，表明细化过程本身具有稳定性。

**Table 3** 进一步统计了实际帧偏移相对于目标偏移的分布。各条件下的四分位距（IQR）均较窄且一致，说明时间扭曲模型的行为具有可预测性，不会因偏移量变化而产生剧烈波动。

### 多智能体可扩展性

**Figure 6** 展示了在链式交互场景（$\mathrm{agent_1 \to agent_2 \to \cdots \to agent_N}$，$N \in \{2, 3, 5, 10\}$）中，TSM、TSE 和 Chamfer Distance（CD）随智能体数量增加的变化趋势。关键发现是：**时序同步误差（TSE）在 10 智能体链式交互中保持稳定，无误差累积现象**。TSM 随 $N$ 增大仅轻微上升，表明时间同步模块具备良好的可扩展性，不会因交互链长度增加而出现时序漂移。

### 消融与稳定性分析

部分去噪步数 $t=30$ 的选择在生成质量与计算成本之间取得了平衡。论文补充材料中进一步分析了该参数对细化稳定性的影响。在大幅度时间调整（如 −1.5 s 偏移）下，成功率下降的主要原因被归因为时间偏移量不足，而非扩散后验采样（DPS）约束的不稳定，这从侧面印证了梯度引导去噪步骤 $\mathbf{x_{i-1}} = \mu_\theta(\mathbf{x_i}, i) - \lambda \nabla_{x_i} C(\hat{\mathbf{x}}_0) + \sigma_i \mathbf{z}$ 在时序约束下的有效性。

### 失败模式与局限

1. **大幅时间调整的稳定性下降**：当目标偏移超过 ±1.5 s 时，时间扭曲与 DPS 约束的协同效果减弱，成功率显著降低。
2. **LLM 规划的边界情况**：在长叙事或模糊指令下，依赖感知故事规划器可能产生错误的事件依赖关系，进而影响下游同步质量。
3. **固定运动时长限制**：当前同步模块仅能在固定运动时长内进行时间扭曲，无法修改运动的总时长，限制了其在需要变速交互场景中的适用性。
4. **2D 空间推理的局限**：俯视图网格表示（$g_i = (\mathtt{grid}_i, \mathsf{action}_i, \mathtt{hand\_target}_i)$）虽然统一了空间坐标系，但牺牲了精细的 3D 接触推理能力。
5. **运动骨干依赖**：生成质量受限于 LINGO 模型的能力上限，但框架本身与模型无关，可替换为更强的单智能体运动生成器。

![[assets/figures/papers/paper_list_l2279_https_openaccess_thecvf_com_content_CVPR2026_html_Li_SyncMos_Scalable_Mo/figures/006_Table_1.jpg]]
*Table 1: Planner performance on Synchronisation and Dependency subsets across LLM backbones. Metrics: Event Coverage (EC), Dependency Accuracy (DA), Passed Scenarios (PS), and Scenario Pass Rate (SPR)*

![[assets/figures/papers/paper_list_l2279_https_openaccess_thecvf_com_content_CVPR2026_html_Li_SyncMos_Scalable_Mo/figures/007_Table_2.jpg]]
*Table 2: Success rate (%) for grasp timing control under different temporal offsets*

![[assets/figures/papers/paper_list_l2279_https_openaccess_thecvf_com_content_CVPR2026_html_Li_SyncMos_Scalable_Mo/figures/008_Table_3.jpg]]
*Table 3: Statistical Results of timewarp model under different temporal offsets (Frame Shift)*

## 定位与知识库关联

### 1. 与现有工作的关系

SyncMos 的核心贡献在于首次将**结构化事件依赖规划**与**无需训练的时序同步细化**引入多智能体运动生成，填补了现有方法在可扩展性与时间对齐上的双重空白。

**相对于单智能体运动扩散模型。** SyncMos 直接构建于单智能体扩散运动生成器之上，论文实现中采用了 **LINGO**（Jiang et al., SIGGRAPH Asia 2024）作为运动骨干。LINGO 等单智能体方法能够生成高质量的个体运动，但缺乏跨智能体的时间协调能力——当直接用于多智能体场景时，各智能体的运动在时间轴上相互独立，导致交互动作（如抓取、交接）出现时间错位。SyncMos 在不修改骨干模型的前提下，通过外部的规划与同步模块赋予其多智能体协同能力，体现了“模型无关”的框架设计理念。

**相对于事件驱动的叙事生成。** **Event-Driven Storytelling**（Lim et al., ICCV 2025）是高层事件规划的直接对比基线。该方法同样利用 LLM 将自然语言指令解析为事件序列，但在两个关键维度上存在不足：(1) 缺乏结构化的时序依赖推理，无法区分顺序依赖与并行依赖，导致事件覆盖率和依赖准确率较低——在 Synchronisation 子集上，其依赖准确率（DA）仅为 68.4%（Qwen-3-235B），而 SyncMos 规划器达到 89.9%（Table 1）；(2) Token 用量随事件数量线性增长，在复杂场景中可扩展性受限（Figure 5）。SyncMos 通过引入依赖感知的事件图 $G = (E, R)$，显式建模顺序关系 $R_{\mathrm{seq}}$ 与并行关系 $R_{\mathrm{par}}$，在提升规划精度的同时保持了 Token 用量的稳定。

**相对于多智能体运动生成方法。** 现有面向多智能体的运动生成工作（如交互舞蹈生成、双人运动合成）通常预设固定数量的智能体，难以灵活扩展至可变数量的参与者。SyncMos 通过将规划与生成解耦，使得框架可自然地处理 2 至 10 个智能体的链式交互场景，且时序同步误差（TSE）不随智能体数量增加而累积（Figure 6），展现出良好的可扩展性。

### 2. 适用边界与局限

SyncMos 的适用边界由其设计选择与底层组件的固有限制共同定义。

**时间扭曲的约束。** 时序同步模块的核心机制是基于样条的时间扭曲（spline-based timewarping）配合扩散后验采样（DPS）进行细化。这一机制在以下条件下有效：(1) 运动总时长固定，仅能对内部时间轴进行拉伸或压缩，无法延长或缩短整体运动时长；(2) 时间偏移量在 ±1.0 s 范围内时成功率较高（75%–88%），但在较大负偏移（-1.5 s）时成功率降至 37.3%（Table 2）。论文指出，这一下降主要源于时间偏移量不足而非轨迹方差增大，表明细化过程本身具有稳定性，但扭曲幅度存在上限。

**空间推理的维度限制。** 高层规划器中的空间推理模块采用 2D 俯视图网格表示（Figure 3），将 3D 场景语义压缩为统一的二维坐标系。这一设计简化了空间落地过程，但限制了精细的 3D 接触推理能力——例如，无法精确建模物体交接时的手部姿态与接触点位置。对于需要高度精确 3D 空间关系的交互（如协作搬运、精细工具传递），当前框架可能不足以提供足够的空间精度。

**LLM 规划的可靠性边界。** 依赖感知故事规划器的性能受 LLM 骨干能力影响。尽管在 GPT-4o 和 Qwen-3-235B 等不同骨干上均表现出较高水平（Table 1），但在长叙事或模糊指令下仍可能产生错误的事件依赖推理。此外，规划器的评估依赖于人工标注的依赖关系真值，其泛化到开放域自由文本指令的能力尚未经过充分验证。

**运动质量的继承性限制。** 由于 SyncMos 本身不生成运动，而是对单智能体生成器的输出进行时序协调，其最终运动质量受限于所采用的骨干模型。论文明确指出，LINGO 的生成能力构成了当前实现的质量上限，但框架本身与模型无关，未来可替换更强的单智能体生成器以提升整体表现。

### 3. 开放问题

以下问题在论文中未被充分解决，构成了未来研究的方向：

1. **部分去噪步数的泛化性。** 初步运动估计采用部分去噪步数 $t=30$，论文仅在补充材料中讨论了该选择在质量与计算成本间的权衡。该参数对不同运动生成模型（如 MDM、MLD 等其他扩散架构）或不同交互类型（如推、拉、协作搬运）的泛化性尚未被系统研究。

2. **DTW 阈值的定量定义。** 时序同步成功率的评估依赖于 DTW 对齐阈值，超过该阈值的运动被视为同步失败。论文未明确报告该阈值的具体取值，也未分析成功率对该阈值的灵敏度。这一缺失使得不同方法间的同步性能难以直接对标。

3. **复杂连续交互的扩展。** 当前实验主要覆盖抓取-交接（grasp-handover）类交互。更复杂的连续物理交互——如协作搬运、推拉配合、对抗性运动——对时序同步精度和空间推理能力提出了更高要求。SyncMos 在这些场景中的表现尚待验证。

4. **物理与接触约束的整合。** 当前框架仅通过时序对齐来保证交互一致性，未显式建模物理约束（如接触力、穿透避免、质量分布）。将物理仿真或接触感知约束纳入同步细化过程，有望进一步提升交互的真实感和物理合理性。

5. **运动时长可变性的支持。** 当前时间扭曲机制仅能在固定时长内进行重分配，无法根据交互需求动态调整运动总时长。支持可变时长生成的同步机制将是提升框架灵活性的重要方向。

## 原文 PDF

![[paperPDFs/CVPR_2026/SyncMos_Scalable_Motion_Synchronisation_for_Multi_Agent_Scene_Interaction.pdf]]
