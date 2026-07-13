---
title: "Flowing from Reasoning to Motion: Learning 3D Hand Trajectory Prediction from Egocentric Human Interaction Videos"
type: paper
paper_level: A
venue: arXiv
year: 2025
pdf_ref: paperPDFs/arxiv_2025/Flowing_from_Reasoning_to_Motion_Learning_3D_Hand_Trajectory_Prediction_from_Egocentric_Human_Interaction_Videos.pdf
project_link: https://egoman-project.github.io/
code_link: null
aliases:
- Flowing_from_Rea
tags:
- arxiv_2025
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
core_operator: 引入紧凑的轨迹令牌接口（四个显式令牌）和渐进式三阶段训练策略，将对齐推理模块与运动专家，从而在保持物理一致性的同时实现意图驱动的长期轨迹生成。
primary_logic: 通过四个专用令牌（一个动作语义令牌<ACT>和三个阶段感知航点令牌<START>、<CONTACT>、<END>）作为结构化桥梁，替代传统隐式令牌或冗长推理链，使得视觉语言推理能高效、可解释地引导流匹配运动专家，生成平滑且意图一致的6-DoF手部轨迹。
claims:
- EgoMAN在EgoMAN-Unseen和HOT3D-OOD上相较最强基线HandsOnVLM*的ADE降幅均达27%以上。
- 消融实验表明，联合推理预训练与运动预训练，并采用显式6DoF航点，可获得最高整体精度；移除任一预训练环节或改用隐式嵌入均导致性能显著下降。
- 在仅用20%数据时，EgoMAN仍维持较强性能，而削弱推理预训练的变体ADE急剧上升，验证了航点推理的数据效率。
- EgoMAN-Unseen 上 ADE (m), K=10 = 0.124
---

# Flowing from Reasoning to Motion: Learning 3D Hand Trajectory Prediction from Egocentric Human Interaction Videos

> [!tip] 核心洞察
> 通过四个专用令牌（一个动作语义令牌<ACT>和三个阶段感知航点令牌<START>、<CONTACT>、<END>）作为结构化桥梁，替代传统隐式令牌或冗长推理链，使得视觉语言推理能高效、可解释地引导流匹配运动专家，生成平滑且意图一致的6-DoF手部轨迹。

| 字段 | 内容 |
|------|------|
| 中文题名 | 从推理到运动：基于自我中心交互视频的3D手部轨迹预测学习 |
| 英文题名 | Flowing from Reasoning to Motion: Learning 3D Hand Trajectory Prediction from Egocentric Human Interaction Videos |
| 会议/期刊 | arXiv 2025 |
| Links | [paper](https://arxiv.org/abs/2512.16907) · [Project](https://egoman-project.github.io/) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction |
| Method | EgoMAN |
| Dataset | EgoMAN-Unseen, HOT3D-OOD |

> [!tip] 效果简介
> - EgoMAN-Unseen 上，ADE (m), K=10 0.124 vs 0.171 (HandsOnVLM*) (-0.047 (-27.5%))；FDE (m), K=10 0.179 vs 0.228 (HandsOnVLM*) (-0.049 (-21.5%))；Contact Distance (m) 0.192 (EgoMAN‑WP) vs 0.290 (VidBot) (-0.098 (-33.8%))。
> - HOT3D-OOD 上，ADE (m), K=10 0.141 vs 0.194 (HandsOnVLM*) (-0.053 (-27.3%))。

## 概要

**瓶颈与动机** 现有3D手部轨迹预测方法缺乏对交互阶段的显式建模与意图监督，难以将高层语义推理有效耦合到连续运动生成中，导致模型在长时域、开放场景下的泛化能力受限。其根本原因在于：传统隐式视觉-语言特征或物体中心的可负担性表示，无法为运动生成提供结构化的时空语义引导。

**核心方法** 本文提出 **EgoMAN**，一个从推理到运动的模块化框架。其核心创新在于引入**紧凑的轨迹令牌接口**——通过四枚专用令牌（一个动作语义令牌 `<ACT>` 和三个交互阶段感知的航点令牌 `<START>`、`<CONTACT>`、`<END>`），替代传统隐式令牌或冗长推理链，作为高层推理与连续运动生成之间的结构化桥梁。配合**渐进式三阶段训练策略**（推理预训练 → 运动预训练 → 联合对齐），EgoMAN 使视觉语言推理模块能高效、可解释地引导基于流匹配（Flow Matching）的运动专家，生成意图一致且物理平滑的6-DoF手部轨迹。

**关键结果** 在 EgoMAN-Unseen 和 HOT3D-OOD 两个基准上，EgoMAN 相较最强基线 **HandsOnVLM*** 的 ADE 降幅均超过 27%（EgoMAN-Unseen: 0.124 m vs. 0.171 m; HOT3D-OOD: 0.141 m vs. 0.194 m）。消融实验证实，联合推理预训练与运动预训练、并采用显式6-DoF航点监督是性能最优配置（Table 3, Table 4）；移除任一预训练环节或仅保留 `<ACT>` 令牌而无航点监督，均导致 ADE 和旋转误差显著恶化。数据效率分析进一步表明，EgoMAN 在仅用 20% 训练数据时仍维持强性能，验证了航点推理预训练的数据高效性。

**方法定位** EgoMAN 属于**意图驱动的轨迹预测**范式，其轨迹令牌接口与渐进训练策略为“语义推理→运动生成”的跨模态对齐提供了新的设计范式，区别于端到端隐式融合或独立推理-生成的两阶段方案。



### 问题背景：自我中心3D手部轨迹预测

理解并预测人类手部在未来数秒内的三维运动轨迹，是构建具身智能与协作机器人的一项基础能力。在增强现实、机器人遥操作和日常活动辅助等以自我为中心的应用中，系统不仅需要知道手“在哪里”，更需要理解“将去往何处”以及“为什么”——即运动的意图与交互阶段。这一任务可形式化为一个条件生成问题：给定当前时刻的自我中心RGB帧 $\mathbf{V}_t$、过去 $H$ 帧的双手6-DoF轨迹 $\{\mathbf{L}_{\tau}, \mathbf{R}_{\tau}\}_{\tau=t-H}^{t}$，以及一段自然语言意图描述 $\mathbf{I}$，模型需预测未来 $T$ 帧的6-DoF腕部轨迹 $\{\tilde{\mathbf{L}}_{\tau}, \tilde{\mathbf{R}}_{\tau}\}_{\tau=t+1}^{t+T}$。6-DoF轨迹同时包含3D位置与6D旋转，对空间精度与物理一致性提出了严苛要求。

### 现有方法的缺口：语义推理与运动生成的脱节

当前3D手部轨迹预测方法大致沿两条路径演进。**运动生成路径**依托扩散模型、VAE或状态空间模型，将过去运动与视觉上下文映射为未来轨迹，但其条件信号多为隐式视觉-语言特征，缺乏对交互意图和阶段结构的显式建模。**可负担性路径**（如**VRB**\*、**VidBot**）则从物体中心视角预测接触点或2D热图，再反投影至3D，但这类方法通常仅输出静态接触位置，难以生成连贯的6-DoF运动序列。近期工作**HandsOnVLM**\*尝试将视觉-语言模型引入轨迹预测，但其推理与运动生成之间仍依赖隐式令牌路由或冗长的推理链，缺乏结构化的中间表征来桥接高层语义与连续运动。

上述路径共同暴露了一个核心瓶颈：**现有3D手部轨迹数据缺乏明确的交互阶段标注和意图监督，导致模型无法有效联结高层语义推理与连续运动生成，从而在真实场景中预测长时域轨迹时泛化能力差**。具体而言，手部运动天然具有阶段性——从接近物体（START）、接触操作（CONTACT）到离开（END）——但现有方法既未显式建模这些阶段，也未将其作为连接推理与运动的可解释接口。这导致模型在面对分布外场景或稀疏数据时，往往退化为对过去运动的简单外推，丧失了意图驱动下的物理合理性。

### 本文动机：以结构化轨迹令牌桥接推理与运动

针对上述缺口，本文的动机是构建一个从高层语义推理到连续运动生成的端到端可学习框架，其关键在于设计一个紧凑、可解释的中间接口，使视觉-语言推理能够高效地引导运动生成。核心洞察是：通过引入**四个专用轨迹令牌**——一个动作语义令牌 `<ACT>` 和三个阶段感知航点令牌 `<START>`、`<CONTACT>`、`<END>`——作为结构化桥梁，替代传统隐式令牌或冗长推理链，使得视觉语言推理能高效、可解释地引导流匹配运动专家，生成平滑且意图一致的6-DoF手部轨迹。这一设计将推理模块的语义理解与空间定位能力，直接转化为运动专家可消费的条件信号（航点位置、时间戳、语义嵌入），从而在保持物理一致性的同时实现意图驱动的长期轨迹生成。

为支撑这一框架，本文同时构建了**EgoMAN数据集**——一个大规模自我中心交互数据集，包含300+小时视频、1500+场景、219K条6-DoF轨迹及3M结构化QA对，覆盖语义、空间与运动推理，为交互阶段感知的轨迹预测提供了必要的监督基础。



## 核心方法与创新机理

### 1. 瓶颈与核心洞察

现有3D手部轨迹预测方法面临一个根本性瓶颈：**缺乏明确的交互阶段标注与意图监督**，导致模型无法有效联结高层语义推理与连续运动生成。传统方法要么依赖隐式视觉‑语言特征，要么采用冗长的推理链，在真实场景中预测长时域轨迹时泛化能力显著下降。

EgoMAN的核心洞察在于：**通过四个专用令牌作为结构化桥梁，替代传统隐式令牌或冗长推理链**，使视觉语言推理能高效、可解释地引导运动生成。具体而言，引入一个动作语义令牌 `<ACT>` 和三个阶段感知航点令牌 `<START>`、`<CONTACT>`、`<END>`，将高层意图推理与连续6-DoF轨迹生成紧密耦合。

### 2. 关键创新维度（Changed Slots）

相较于现有基线方法，EgoMAN在以下四个维度实现了根本性改变：

**（1）条件信号：从隐式特征到显式轨迹令牌**

基线方法（如HandsOnVLM*、USST*等）通常使用隐式视觉‑语言特征或物体中心的可负担性（affordance）作为条件信号。EgoMAN则引入**四枚显式轨迹令牌**：`<ACT>` 语义令牌编码动作意图的语义嵌入，`<START>`、`<CONTACT>`、`<END>` 三个航点令牌分别编码交互起始、接触时刻和交互结束的时空位置。这种显式结构化表示使推理模块的输出可直接作为运动专家的条件输入，无需额外的隐式路由或解码步骤。

**（2）训练策略：从端到端到渐进式三阶段训练**

传统方法通常采用端到端训练或独立推理策略。EgoMAN提出**渐进式三阶段训练**：
- **阶段一（推理预训练）**：在EgoMAN数据集上预训练推理模块，学习语义推理、空间推理和航点预测能力；
- **阶段二（运动预训练）**：独立预训练基于流匹配（Flow Matching）的运动专家，学习从真实航点和语义条件生成物理一致的轨迹；
- **阶段三（联合对齐）**：通过轨迹令牌接口将推理模块与运动专家联合微调，实现意图到运动的端到端对齐。

消融实验（Table 3, Table 4）表明，**联合推理预训练与运动预训练，并采用显式6DoF航点，可获得最高整体精度**；移除任一预训练环节或改用隐式嵌入均导致性能显著下降。

**（3）运动生成模型：从扩散/VAE到流匹配Transformer**

基线方法多采用扩散模型、VAE或状态空间模型进行轨迹生成。EgoMAN的运动专家采用**基于流匹配（Flow Matching）的编码器‑解码器Transformer**，辅以航点结构化引导。流匹配通过直接回归速度场 $v(x_t, t)$ 实现从简单先验分布到目标轨迹分布的确定性映射，避免了扩散模型的迭代去噪步骤，在保持生成质量的同时提升推理效率。其损失函数为预测速度与真实速度的均方误差：
$$\mathcal{L}_{\mathrm{FM}} = \left\| \hat{v} - (x_1 - x_0) \right\|_2^2$$

**（4）推理‑运动接口：从隐式路由到紧凑令牌接口**

现有方法多采用隐式令牌路由或繁长推理链连接推理与运动模块。EgoMAN设计**紧凑的轨迹令牌接口**，将推理模块输出的轨迹令牌直接解码为运动专家所需的条件——包括航点位置、时间戳和语义嵌入，替换真实标注条件。这一接口实现了推理与运动模块的解耦预训练和高效对齐，使得语义推理的改进可直接转化为运动生成质量的提升。

### 3. 创新有效性验证

EgoMAN的创新设计在多个维度得到严格验证：

- **主实验**（Table 1）：在EgoMAN-Unseen和HOT3D-OOD两个基准上，EgoMAN相较最强基线HandsOnVLM*的ADE降幅均达27%以上，验证了轨迹令牌接口和三阶段训练的整体有效性。
- **消融实验**（Table 3, Table 4）：完整模型（推理预训练 + FM预训练 + 6DoF航点）取得最优ADE 0.151、FDE 0.206；移除FM预训练导致ADE从0.150恶化至0.215，旋转误差从34.02°升至43.03°；仅保留 `<ACT>` 令牌而无航点监督（EgoMAN-ACT），ADE从0.162升至0.215，证明**航点显式结构是关键**。
- **数据效率**（Figure 6）：在仅用20%训练数据时，EgoMAN仍维持ADE约0.13 m的强性能，而削弱推理预训练的EgoMAN-ACT变体ADE急剧上升至约0.16 m，验证了航点推理的数据效率优势。



EgoMAN 是一个模块化的“推理‑到‑运动”框架，其核心任务是将自我中心 RGB 帧、过去双手腕部轨迹以及语言意图描述，映射为未来 6‑DoF 手部轨迹。该映射函数形式化为：

$$\mathcal{F} : \left( \mathbf{V}_t, \{ \mathbf{L}_{\tau}, \mathbf{R}_{\tau} \}_{\tau = t-H}^{t}, \mathbf{I} \right) \mapsto \{ \tilde{\mathbf{L}}_{\tau}, \tilde{\mathbf{R}}_{\tau} \}_{\tau = t+1}^{t+T}$$

其中 $\mathbf{V}_t$ 为当前时刻的自我中心图像，$\mathbf{L}_{\tau}$ 和 $\mathbf{R}_{\tau}$ 分别为左右手腕部在过去 $H$ 帧内的 6‑DoF 轨迹，$\mathbf{I}$ 为描述未来交互意图的文本查询。

框架由三大组件构成，形成一条从高层语义推理到连续运动生成的完整链路（Figure 2）：

![[assets/figures/papers/paper_list_l25_https_arxiv_org_abs_2512_16907/figures/002_Figure_2.jpg]]
*Figure 2: Overview of the EgoMAN model. The EgoMAN model is a modular reasoning-to-motion framework that predicts future 6DoF hand trajectories from an egocentric RGB frame, past wrist trajectories, and a language intent. The Reasoning Module (a), built on QwenVL-7B, extracts semantic and spatial features and outputs trajectory tokens with waypoints and intent semantic cues. The Motion Expert (b), using Flow Matching, predicts future trajectories based on waypoints, past motion, intent semantics and visual input. The trajectory tokens of (a) form the Trajectory-Token Interface which replaces semantic and waypoint condition inputs of (b) to bridge from Reasoning to Motion Expert*

1. **推理模块（Reasoning Module）**：基于 Qwen2.5‑VL 构建，以自我中心帧、意图查询和过去腕部轨迹为输入，输出自然语言答案及结构化轨迹令牌序列。该模块在推理预训练阶段被赋予双重能力——理解交互语义并进行阶段感知的空间推理，最终生成四个专用轨迹令牌：一个动作语义令牌 `<ACT>` 和三个阶段感知航点令牌 `<START>`、`<CONTACT>`、`<END>`。

2. **运动专家（Motion Expert）**：一个基于流匹配（Flow Matching）的编码器‑解码器 Transformer，以过去腕部运动、意图语义嵌入、底层视觉特征和阶段感知航点为条件，生成未来 6‑DoF 手部轨迹。其核心训练目标为预测速度场与真实速度之间的均方误差：

   $$\mathcal{L}_{\mathrm{FM}} = \left\| \hat{v} - (x_1 - x_0) \right\|_2^2$$

   推理时通过欧拉积分 $x_{k+1} = x_k + \Delta t \cdot \hat{v}(x_k, t_k)$ 从预测速度场生成完整轨迹。

3. **轨迹令牌接口（Trajectory‑Token Interface）**：作为连接推理与运动的紧凑桥梁，将推理模块输出的轨迹令牌解码为运动专家所需的条件信号——航点 6‑DoF 位置与时间戳、以及 `<ACT>` 令牌的语义嵌入，从而替代真实标注条件，实现端到端的推理‑运动对齐。

三者的协作通过**渐进式三阶段训练策略**实现：第一阶段对推理模块进行预训练，使其学会从视觉和意图中推理航点与动作语义；第二阶段对运动专家进行流匹配预训练，使其掌握从条件信号生成平滑轨迹的能力；第三阶段通过轨迹令牌接口联合训练两个模块，以轨迹令牌序列的下一个令牌预测损失和运动专家的流匹配损失共同优化，实现语义意图与物理运动的一致性对齐。

这一设计的核心洞察在于：四个专用令牌作为结构化桥梁，替代了传统方法中隐式令牌路由或冗长推理链的接口方式，使得视觉语言推理能高效、可解释地引导流匹配运动专家，生成平滑且意图一致的 6‑DoF 手部轨迹。



EgoMAN 是一个模块化的“推理‑到‑运动”框架，其核心由三个组件构成：**推理模块（Reasoning Module）**、**运动专家（Motion Expert）** 以及连接二者的**轨迹令牌接口（Trajectory‑Token Interface）**。整体映射函数定义为：

$$\mathcal{F} : \left( \mathbf{V}_t, \{ \mathbf{L}_{\tau}, \mathbf{R}_{\tau} \}_{\tau = t-H}^{t}, \mathbf{I} \right) \mapsto \{ \tilde{\mathbf{L}}_{\tau}, \tilde{\mathbf{R}}_{\tau} \}_{\tau = t+1}^{t+T}$$

其中 $\mathbf{V}_t$ 为当前自我中心 RGB 帧，$\{ \mathbf{L}_{\tau}, \mathbf{R}_{\tau} \}$ 为过去 $H$ 帧的左右手腕 6‑DoF 轨迹，$\mathbf{I}$ 为语言意图描述，输出为未来 $T$ 帧的预测轨迹。

### 推理模块

推理模块基于 **Qwen2.5‑VL** 构建，接收自我中心帧、包含意图的语言查询以及过去手腕轨迹，输出自然语言推理答案或结构化的轨迹令牌序列。该模块在预训练阶段同时优化三个目标：

$$\mathcal{L}_{\mathrm{total}} = \mathcal{L}_{\mathrm{text}} + \lambda_{\mathrm{wp}} \mathcal{L}_{\mathrm{wp}} + \lambda_{\mathrm{act}} \mathcal{L}_{\mathrm{act}}$$

其中 $\mathcal{L}_{\mathrm{text}}$ 为文本生成损失；$\mathcal{L}_{\mathrm{wp}}$ 为航点损失，监督 `<START>`、`<CONTACT>`、`<END>` 三个交互阶段航点的时空坐标；$\mathcal{L}_{\mathrm{act}}$ 为动作语义损失，用于对齐 `<ACT>` 令牌的语义嵌入。

**航点损失** 由多个分量的加权 Huber 损失构成：

$$\mathcal{L}_{\mathrm{wp}} = \lambda_t \mathcal{L}_{\mathrm{time}} + \lambda_{3D} \mathcal{L}_{3D} + \lambda_{2D} \mathcal{L}_{2D} + \lambda_r \mathcal{L}_{\mathrm{rot6D}} + \lambda_{\mathrm{geo}} \mathcal{L}_{\mathrm{geo}}$$

各分量分别监督航点时间戳、3D 位置、2D 投影、6D 旋转表示及测地旋转误差，确保推理模块能精确预测交互阶段的关键时空锚点。

**动作语义损失** 采用自适应对比学习策略，根据有效样本数 $K$ 动态切换损失形式：

$$\mathcal{L}_{\mathrm{act}} = \begin{cases} 1 - \frac{1}{K} \sum_{i=1}^{K} \mathrm{sim}(z_i, z_i^+), & K < \kappa, \\ -\frac{1}{K} \sum_{i=1}^{K} \log \frac{\exp(\mathrm{sim}(z_i, z_i^+)/\tau)}{\sum_{j=1}^{K} \exp(\mathrm{sim}(z_i, z_j^+)/\tau)}, & K \geq \kappa. \end{cases}$$

当批量内有效样本数低于阈值 $\kappa$ 时，直接优化余弦相似度；否则使用 InfoNCE 损失，增强 `<ACT>` 令牌嵌入与对应动作语义的判别性对齐。

### 运动专家

运动专家是一个基于 **流匹配（Flow Matching）** 的编码器‑解码器 Transformer，其条件信号包括：过去手腕运动、意图语义嵌入、低层视觉特征以及阶段感知航点。训练目标为预测速度场与真实速度之间的均方误差：

$$\mathcal{L}_{\mathrm{FM}} = \left\| \hat{v} - (x_1 - x_0) \right\|_2^2$$

其中 $\hat{v}$ 为模型预测的速度向量，$x_1 - x_0$ 为从当前状态到目标状态的真实位移。推理时，通过欧拉积分从预测速度场逐步生成未来轨迹：

$$x_{k+1} = x_k + \Delta t \cdot \hat{v}(x_k, t_k), \quad \Delta t = \frac{1}{N}$$

$N$ 为积分步数，$\Delta t$ 为步长。流匹配的连续性优势使运动专家能生成平滑且物理一致的 6‑DoF 轨迹。

### 轨迹令牌接口

轨迹令牌接口是连接推理与运动的关键桥梁。推理模块输出四枚专用令牌——一个动作语义令牌 `<ACT>` 和三个阶段感知航点令牌 `<START>`、`<CONTACT>`、`<END>`——这些令牌被解码为运动专家所需的条件信号（航点 3D 位置、时间戳、语义嵌入），直接替换训练时使用的真实标注条件。在联合训练阶段，系统同时优化轨迹令牌序列的下一令牌预测损失 $\mathcal{L}_{\mathrm{text}}$ 和运动专家的流匹配损失 $\mathcal{L}_{\mathrm{FM}}$，实现推理与运动的端到端对齐。



## 实验与关键发现

### 核心性能：EgoMAN 在分布内与跨分布场景中均大幅领先

EgoMAN 在 EgoMAN-Unseen（分布内留出测试集）和 HOT3D-OOD（跨分布泛化测试集）上均取得最优结果。Table 1 显示，在最佳‑K（K=10）设定下，EgoMAN 相较最强外部基线 **HandsOnVLM\*** 在两个基准上的平均位移误差（ADE）降幅均超过 27%：EgoMAN-Unseen 上 ADE 从 0.171 m 降至 0.124 m（−27.5%）；HOT3D-OOD 上 ADE 从 0.194 m 降至 0.141 m（−27.3%）。最终位移误差（FDE）同样显著改善，EgoMAN-Unseen 上 FDE 从 0.228 m 降至 0.179 m（−21.5%）。这一致性增益表明，EgoMAN 的推理‑运动联合架构不仅在训练分布内有效，在未见设备和场景的 OOD 条件下同样具备强泛化能力。

![[assets/figures/papers/paper_list_l25_https_arxiv_org_abs_2512_16907/figures/003_Table_1.jpg]]
*Table 1: Comparison of 6DoF hand trajectory prediction on EgoMAN-Unseen and HOT3D-OOD. Lower is better. Best values are bold, second-best are underlined. Our EgoMAN model outperforms the strongest external baseline (HandsOnVLM) by 27.5% ADE on both the held-out EgoMAN-Unseen test split and the out-of-distribution HOT3D-OOD dataset*

在航点预测任务上，EgoMAN‑WP 的接触距离（Contact Distance）仅 0.192 m，相较 **VidBot** 的 0.290 m 降低 33.8%（Table 2），同时轨迹误差（Traj）降低 52.8%，推理速度达 3.45 FPS，比基于可负担性的基线快数个数量级。这验证了轨迹令牌接口在空间定位精度和计算效率上的双重优势。

![[assets/figures/papers/paper_list_l25_https_arxiv_org_abs_2512_16907/figures/004_Table_2.jpg]]
*Table 2: Waypoint prediction results. Lower is better for Contact and Traj; higher is better for FPS (averaged over 50 samples on an NVIDIA PG509-210, 80GB). EgoMAN-WP achieves the best accuracy, improving Contact by 33.8% and Traj by 52.8% on EgoMAN-Unseen, and runs orders of magnitude faster at 3.45 FPS*

### 消融实验：推理预训练、运动预训练与显式航点缺一不可

Table 3 和 Table 4 的消融实验揭示了三个关键设计选择的因果贡献：

![[assets/figures/papers/paper_list_l25_https_arxiv_org_abs_2512_16907/figures/005_Table_3.jpg]]
*Table 3: Ablation on EgoMAN-Unseen (K=1). Lower is better. Reason and FM pretraining with 6DoF waypoints yield the highest accuracy*

![[assets/figures/papers/paper_list_l25_https_arxiv_org_abs_2512_16907/figures/010_Table_4.jpg]]
*Table 4: Ablation on EgoMAN-Unseen (K=1). Lower is better. Reason and FM pretraining with 6DoF waypoints yield the highest accuracy*

1. **推理预训练与运动预训练联合**：完整模型（推理预训练 + FM 预训练 + 6DoF 航点）在 K=1 设定下取得 ADE 0.151、FDE 0.206、DTW 0.137、旋转误差 33.88° 的最优结果。若移除 FM 预训练，仅让推理模块同时学习语义与运动，ADE 从 0.150 恶化至 0.215，旋转误差从 34.02° 升至 43.03°，说明将运动动力学建模外包给专用运动专家是必要的。

2. **显式航点令牌的必要性**：仅保留 `<ACT>` 语义令牌而无航点监督的变体 EgoMAN‑ACT，ADE 从 0.162 升至 0.215，旋转误差升至 43.03°。这表明 `<START>`、`<CONTACT>`、`<END>` 三个阶段感知航点令牌提供了不可替代的结构化时空引导，隐式嵌入无法弥补这一信息缺口。

3. **数据效率**：Figure 6 显示，在仅使用 20% 训练数据时，EgoMAN 仍维持约 0.13 m 的 ADE，而削弱推理预训练的 EgoMAN‑ACT 的 ADE 急剧上升至约 0.16 m。航点‑推理预训练显著提升了小样本条件下的学习效率，这对实际部署中标注数据稀缺的场景具有重要价值。

![[assets/figures/papers/paper_list_l25_https_arxiv_org_abs_2512_16907/figures/009_Figure_6.jpg]]
*Figure 6: Data efficiency results. ADE/FDE (m), best-of-10. The static baseline repeats the last observed hand location. Without pretraining, errors of EgoMAN-ACT rise sharply under limited data, while EgoMAN maintains strong performance even at 20% data, highlighting the benefit of waypoint-based Reasoning Module and pretraining*

### 推理模块规模的影响：空间推理饱和早，语义对齐持续受益

Table 6 和 Table 7 分析了推理模块规模对空间推理、语义对齐和文本 QA 的影响。关键发现是：空间推理性能在 2B/3B 规模后趋于饱和，而语义嵌入对齐（R@3 和 Pearson 相关系数）随模型增大持续提升，其中 Qwen2.5‑VL 在语义对齐上优于 Qwen3‑VL，但文本 QA 指标相对稳定。最终轨迹预测精度随推理模块增大而单调改善，4B 模型在速度‑精度权衡上表现最佳。

![[assets/figures/papers/paper_list_l25_https_arxiv_org_abs_2512_16907/figures/012_Table_6.jpg]]
*Table 6: Effect of model scale on spatial reasoning, semantic alignment, and text QA on EgoMAN Unseen benchmark. We evaluate (i) waypoint spatial reasoning via 3D location, time, and rotation errors, (ii) semantic embedding alignment using R@3 (computed over 2,844 GT action-embedding candidates) and mean Pearson correlation, and (iii) semantic text QA using BERTScore, BLEU, and ROUGE. Best values are bolded; second-best are underlined. Spatial reasoning performance saturates early, and models larger than 2B/3B provide consistently stronger performance. Semantic alignment benefits from larger models, with Qwen2.5-VL outperforming Qwen3-VL, while text QA remains relatively stable across scales, with Q...*

![[assets/figures/papers/paper_list_l25_https_arxiv_org_abs_2512_16907/figures/013_Table_7.jpg]]
*Table 7: Effect of Reasoning Module scale on trajectory prediction. Best results are bolded and second-best are underlined. Larger reasoning models produce consistently more accurate 6-DoF trajectories on both EgoMAN Unseen and HOT3D OOD, with Qwen3-VL scaling smoothly and the 4B model offering an excellent speed–accuracy trade-off*

### 失败模式与局限性

尽管 EgoMAN 在整体指标上表现优异，分析揭示了以下结构性局限：

- **粗粒度交互阶段**：当前建模仅区分 `<START>`、`<CONTACT>`、`<END>` 三个阶段，未捕捉预接触调整、微修正等精细子阶段，限制了刻画高分辨率灵巧操作行为的能力。
- **腕部轨迹的表示瓶颈**：模型仅预测腕部 6‑DoF 运动，无法推理手指关节姿态，因此在需要精细抓取推理的任务中存在固有上限。
- **数据质量约束**：尽管 EgoMAN 数据集规模庞大，但仍存在传感器噪声和不完美标注，且缺乏人工校验循环。更高保真的 3D 标注和经人工校验的演示有望进一步提升学习效果。

### 公平性说明

所有基线方法被适配至相同的输入配置（单帧 RGB、意图文本嵌入、过去运动），并统一采用最佳‑K 采样（K=1/5/10）评估生成多样性。基于可负担性的基线均使用相同的 RGB 图像和深度估计，经设备标定校正失真，2D 预测统一反投影到 3D 空间并采用与 GT 腕部最近点近似误差，确保对比公平。

### 补充图表

![[assets/figures/papers/paper_list_l25_https_arxiv_org_abs_2512_16907/figures/006_Figure_3.jpg]]
*Figure 3: Qualitative comparisons on EgoMAN-Bench. We visualize best-of-K=10 predictions for waypoints and full trajectories. Left: \<CONTACT> and \<END> waypoint predictions compared with VRB* and VidBot. Right: 3D hand trajectory forecasts and 2D projections compared with prior baselines. Our EgoMAN model produces the smoothest and closest results to ground truth*

![[assets/figures/papers/paper_list_l25_https_arxiv_org_abs_2512_16907/figures/007_Figure_4.jpg]]
*Figure 4: Qualitative results of diverse activities. EgoMAN generates accurate 6DoF hand trajectories for diverse activities, aligning motion with the intent description and scene spatial*

![[assets/figures/papers/paper_list_l25_https_arxiv_org_abs_2512_16907/figures/008_Figure_5.jpg]]
*Figure 5: Multiple intents. With the same image and past motion, EgoMAN model produces distinct 6DoF trajectories for different intent queries, showing controllable intent-to-motion generation*

![[assets/figures/papers/paper_list_l25_https_arxiv_org_abs_2512_16907/figures/011_Table_5.jpg]]
*Table 5: Motion-to-Verb Text Retrieval. Train one encoder; evaluate verb text-motion relevance over 239 verb candidates*



## 定位与知识库关联

### 1. 与现有方法的关系与差异

EgoMAN 的核心贡献在于为“高层语义推理”与“连续运动生成”之间建立了一个结构化桥梁，这与现有工作的设计范式形成了鲜明对比。

**相对于手部轨迹预测基线**：现有方法如 **USST***、**MMTwin*** 和 **HandsOnVLM*** 通常采用端到端训练或独立推理策略，其条件信号多为隐式视觉‑语言特征或物体中心的可负担性表示。EgoMAN 将这一范式替换为**显式的四枚轨迹令牌接口**（`<ACT>` 语义令牌 + `<START>`/`<CONTACT>`/`<END>` 航点令牌），使推理模块能够以结构化、可解释的方式直接指导运动专家。在主实验（Table 1）中，EgoMAN 在 EgoMAN-Unseen 和 HOT3D-OOD 两个基准上相较最强基线 HandsOnVLM* 的 ADE 降幅均超过 27%，证明了该接口的有效性。

**相对于可负担性基线**：**HAMSTER***、**VRB*** 和 **VidBot** 等方法依赖物体中心的可负担性预测来间接推断手部运动，缺乏对交互阶段的显式建模。EgoMAN 通过航点令牌（尤其是 `<CONTACT>` 令牌）直接定位交互的时空关键点。Table 2 显示，EgoMAN‑WP 在接触距离上相较 VidBot 改善了 33.8%（0.192 m vs. 0.290 m），在轨迹精度上改善了 52.8%，同时推理速度达到 3.45 FPS，实现了精度与效率的同步提升。

**运动生成模型的演进**：在运动生成层面，基线方法多采用扩散模型、VAE 或状态空间模型。EgoMAN 转而采用**基于流匹配（Flow Matching）的编码器‑解码器 Transformer**，并辅以航点结构化引导。流匹配的优势在于其训练目标直接匹配速度场（$\mathcal{L}_{\mathrm{FM}} = \|\hat{v} - (x_1 - x_0)\|_2^2$），避免了扩散模型中复杂的噪声调度，同时航点条件为生成过程提供了清晰的时空锚点，使长期轨迹生成更稳定。

**推理‑运动接口的简化**：与使用隐式令牌路由或繁长推理链的方案不同，EgoMAN 的轨迹令牌接口将推理模块的输出直接解码为运动专家所需的条件（航点位置、时间戳、语义嵌入），消除了中间的信息瓶颈。消融实验（Table 4）证实，当仅保留 `<ACT>` 令牌而无航点监督时（EgoMAN‑ACT），ADE 从 0.162 恶化至 0.215，旋转误差从 34.02° 升至 43.03°，凸显了显式航点结构的关键作用。

### 2. 适用边界与限制

尽管 EgoMAN 在实验设定下展现了显著优势，其设计仍存在明确的适用边界：

- **建模粒度限于腕部 6‑DoF**：当前方法仅预测腕部的 3D 位置和 6D 旋转，未涉及手指关节或完整手部姿态。这意味着 EgoMAN 适用于粗粒度的“手‑物接近与接触”预测，但无法刻画抓取类型、手指配置等精细灵巧操作行为。
- **交互阶段划分粗糙**：航点仅定义了 `<START>`、`<CONTACT>`、`<END>` 三个宏观阶段，未捕捉预接触调整、微修正、再接触等精细子阶段。对于需要高分辨率时序定位的任务（如精密装配），该粒度可能不足。
- **数据质量依赖**：EgoMAN 数据集虽规模庞大（219K 轨迹），但源自 Aria 眼镜的多源数据，不可避免地存在传感器噪声和不完美标注。论文明确指出缺乏人工校验循环，更高质量的 3D 轨迹和更干净的监督将进一步提升学习效果。
- **训练策略的依赖性**：渐进式三阶段训练（推理预训练 → 运动预训练 → 联合对齐）是性能的关键保障。消融实验（Table 3）表明，移除任一预训练环节均导致性能显著下降。这意味着该方法对训练流程的顺序和完整性有较强依赖，直接端到端训练可能无法收敛至同等性能。

### 3. 开放问题与未来方向

论文提出了四个值得进一步探索的开放问题：

1. **从腕部轨迹到完整手部姿态的扩展**：如何将表示从腕部 6‑DoF 扩展至包含手指关节的全手姿态，从而支持更精细的物体操作与抓取推理？这需要解决高维姿态空间的建模复杂性和数据标注成本问题。
2. **多阶段交互解析的深化**：融入更丰富的接触语义（如接触力、接触面、物体部件信息）和更细粒度的交互阶段划分，能否进一步提升时间定位精度和运动自然度？这可能需要引入触觉或物体状态等额外模态。
3. **数据集质量的提升路径**：如何通过更高保真的 3D 标注或经人工校验的演示来提高数据集质量，以支撑精细操作学习？这可能涉及多视角融合、运动捕捉辅助或仿真数据增强。
4. **真实机器人系统的部署验证**：将 EgoMAN 的意图驱动 6‑DoF 预测策略部署到真实机器人系统时，能否有效转化为具体的操作性能？这需要解决 sim‑to‑real 迁移、实时控制闭环和安全性约束等工程挑战。

### 4. 知识库定位

EgoMAN 在以下三个交叉领域贡献了新的知识节点：

- **视觉‑语言‑运动对齐**：通过轨迹令牌接口，提供了一种将 VLM 的结构化推理输出与物理运动生成解耦并对齐的范式，补充了现有工作中“隐式融合”与“纯文本中介”之间的空白。
- **交互阶段感知的运动预测**：将交互阶段（start‑contact‑end）显式编码为预测目标，为第一人称手部运动预测引入了时间语义监督，这在现有轨迹预测文献中较为少见。
- **数据高效的轨迹学习**：Figure 6 显示，在仅使用 20% 训练数据时 EgoMAN 仍维持较强性能，而削弱推理预训练的变体 ADE 急剧上升。这表明航点‑推理预训练显著提升了数据效率，为小样本或低资源场景下的运动学习提供了参考策略。



## 原文 PDF

![[paperPDFs/arxiv_2025/Flowing_from_Reasoning_to_Motion_Learning_3D_Hand_Trajectory_Prediction_from_Egocentric_Human_Interaction_Videos.pdf]]
