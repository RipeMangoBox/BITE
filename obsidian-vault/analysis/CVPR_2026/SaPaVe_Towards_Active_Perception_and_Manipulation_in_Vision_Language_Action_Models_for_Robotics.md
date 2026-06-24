---
title: "SaPaVe: Towards Active Perception and Manipulation in Vision-Language Action Models for Robotics"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/SaPaVe_Towards_Active_Perception_and_Manipulation_in_Vision_Language_Action_Models_for_Robotics.pdf
project_link: "https://lmzpai.github.io/SaPaVe"
code_link: null
aliases:
- SaPaVe
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
core_operator: 将相机运动与操作动作解耦为两个独立的动作空间，采用自下而上的两阶段训练：第一步用大规模实例无关的相机控制数据建立语义主动感知先验，第二步在冻结该先验的条件下联合优化全部动作，从而以低数据成本习得鲁棒的主动操作。
primary_logic: 相机运动本身是实例无关且较易学习的；通过LoRA相机适配器保留VLM的高层语义同时学习对齐，配合通用空间知识注入增强3D几何鲁棒性，解耦动作头使得两类动作可从各自数据中获益，避免冲突。
claims:
- SaPaVe在ActiveManip-Bench上平均成功率达75.2%，优于所有基线，绝对超过固定视角VLA GR00T-N1 58%成功率。
- 在语义主动感知数据集ActiveViewPose-200K上，仅2B参数的SaPaVe第一阶段模型平均准确率84.3%，比通用VLM Gemini-2.5-Pro高11.6个百分点。
- 真实世界主动操作任务中，SaPaVe平均成功率85%，分别超出π0 40个百分点和GR00T-N1 31.25个百分点。
- 移除Stage 1训练后，模型在视野外关节操作任务中成功率减半，证明语义主动感知先验是不可或缺的。
---

# SaPaVe: Towards Active Perception and Manipulation in Vision-Language Action Models for Robotics

> [!tip] 核心洞察
> 相机运动本身是实例无关且较易学习的；通过LoRA相机适配器保留VLM的高层语义同时学习对齐，配合通用空间知识注入增强3D几何鲁棒性，解耦动作头使得两类动作可从各自数据中获益，避免冲突。

| 字段 | 内容 |
|------|------|
| 中文题名 | SaPaVe：面向机器人视觉语言动作模型的主动感知与操作 |
| 英文题名 | SaPaVe: Towards Active Perception and Manipulation in Vision-Language Action Models for Robotics |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2603.12193) · [Project](https://lmzpai.github.io/SaPaVe) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction |
| Method | SaPaVe |
| Dataset | ActiveViewPose-200K, ActiveManip-Bench, Real-world Active Manipulation |

> [!tip] 效果简介
> - ActiveViewPose-200K 上，Success rate (%) (Avg) 84.3 (Stage 1) vs 72.7 (Gemini-2.5-Pro) (+11.6)。
> - ActiveManip-Bench (Simulation) 上，Success rate (%) (Avg across 6 task types) 74.83 (Active Camera only) vs 36.17 (Fixed Camera) (+38.66)。
> - Real-world Active Manipulation (4 tasks) 上，Success rate (%) (Avg) 85.00 (Ours) vs 45.00 (π0) (+40.00)。

## 概述

当前视觉-语言-动作（VLA）模型在机器人操作中取得了显著进展，但其成功高度依赖固定的、预先优化的相机视角。一旦场景中出现遮挡或物体偏离最佳视野，固定视角模型便缺乏主动调整视线以获取任务关键视觉线索的能力。直接扩展VLA的动作空间以包含连续相机运动面临双重困境：一方面，统一动作空间会破坏已有操作先验；另一方面，大规模主动操作数据的稀缺使模型难以收敛。

**SaPaVe** 针对上述瓶颈，提出一种端到端的主动操作框架，核心思路是将相机运动与操作动作**解耦**为两个独立动作空间，并采用**自下而上的两阶段训练策略**。第一阶段利用大规模、实例无关的相机控制数据，通过轻量级LoRA相机适配器学习语义主动感知先验；第二阶段在该先验冻结的条件下联合优化全部动作，以极低的数据成本习得鲁棒的主动操作。同时，通用空间知识注入模块融合深度、相机内参等多模态几何信息，增强动态视角下的3D空间精度。

实验表明，SaPaVe在仿真基准 **ActiveManip-Bench** 上平均成功率达 **75.2%**，绝对超出固定视角VLA模型（如GR00T-N1）**58个百分点**；在真实世界主动操作任务中平均成功率达 **85%**，分别超出π0 **40个百分点**和GR00T-N1 **31.25个百分点**。消融实验进一步证实，解耦动作头设计、两阶段训练策略以及空间知识注入均对最终性能有决定性贡献。

## 背景与动机

### 主动感知：机器人操作中被忽视的关键能力

人类在执行日常操作任务时，会自然地移动头部以获取更好的观察视角——例如侧头查看被遮挡的碗，或抬头确认高处的把手位置。这种**语义驱动的主动感知**（semantic active perception）——即根据任务需求有选择地调整视角以揭示关键视觉线索——是灵巧操作的基础。然而，当前主流的视觉语言动作（Vision-Language-Action, VLA）模型在这一能力上存在根本性缺失。

现有VLA模型（如 **GR00T-N1** 和 **π0**）几乎完全依赖**固定或近优视角**（fixed or near-optimal viewpoints）进行训练。在训练数据采集阶段，操作者通常会有意将相机对准目标物体，确保其始终处于视野中心。这种数据采集偏差导致模型从未学习到“当目标被遮挡时应当主动移动相机”这一行为模式。一旦部署到真实场景中——物体可能被部分遮挡、偏离中心视角、或处于次优光照角度——固定视角VLA的表现会急剧退化。实验表明，固定视角配置下模型在ActiveManip-Bench上的平均成功率仅为**36.17%**，而引入主动相机控制后，同一架构的成功率跃升至**74.83%**（Table 2）。

### 直接扩展动作空间的困境

一个直观的解决方案是将相机运动（如头部关节的pitch/yaw）直接纳入VLA的动作空间，与机械臂关节位置统一预测。然而，这一策略面临两个核心瓶颈：

1. **先验破坏**：现有VLA模型的大规模预训练权重编码了丰富的操作先验。直接将2自由度的相机运动与26自由度的操作动作混合在一个统一的动作空间中，会破坏这些已习得的表征，导致模型在操作任务上的性能显著下降。

2. **数据稀缺**：大规模主动操作数据的采集成本极高。真实世界的主动操作示教需要操作者同时控制机械臂和相机视角，而仿真中的主动操作数据生成也面临场景多样性和任务复杂性的挑战。直接端到端训练难以在有限数据下收敛。

### 核心洞察：解耦与自下而上的学习

SaPaVe的设计源于一个关键观察：**相机运动本身是实例无关的（instance-agnostic）**。无论是抓取一个被遮挡的碗还是操作一个高处的把手，底层相机控制策略——根据语义指令将目标置于视野中心——具有高度的通用性。这意味着语义主动感知可以作为独立于具体操作任务的先验来学习。

基于这一洞察，SaPaVe将**相机运动与操作动作解耦为两个独立的动作空间**，并采用**自下而上的两阶段训练策略**：
- **第一阶段**：在大规模实例无关的相机控制数据（**ActiveViewPose-200K**，包含20万图像-语言-相机运动三元组）上训练语义主动感知先验，通过LoRA相机适配器在冻结VLM权重的条件下学习语义到相机运动的对齐。
- **第二阶段**：冻结相机适配器，在混合操作数据上联合优化相机与操作动作，同时注入通用空间知识（如深度、相机内参）以增强动态视角下的3D几何鲁棒性。

这种设计使得两类动作可以从各自的数据中获益：相机控制受益于大规模合成数据，操作能力受益于已有的VLA预训练权重，避免了直接混合训练带来的冲突与退化。消融实验证实，移除第一阶段训练后，模型在视野外关节操作任务中**成功率减半**（Table 5），验证了语义主动感知先验的不可或缺性。

## 核心创新

SaPaVe 的核心创新在于**将主动感知从操作策略中解耦**，通过动作空间分离与自下而上的两阶段训练，以极低的数据成本赋予视觉语言动作（VLA）模型语义驱动的主动相机控制能力。

### 1 问题瓶颈：为何现有 VLA 无法主动感知

现有 VLA 模型（如 GR00T-N1、π0）依赖固定近优视角训练，缺乏语义驱动的主动感知能力。直接扩展动作空间以包含连续相机运动面临双重困境：

- **先验破坏**：将相机运动与操作动作统一到单一动作空间会扰乱已有操作先验，导致训练不稳定；
- **数据稀缺**：大规模主动操作数据采集成本极高，端到端混合训练难以收敛。

### 2 因果调控手柄：解耦动作空间与两阶段训练

SaPaVe 的核心设计是将相机运动与操作动作**解耦为两个独立的动作空间**，并采用**自下而上的两阶段训练策略**：

- **第一阶段**：在大规模实例无关的相机控制数据（ActiveViewPose-200K）上单独学习语义主动感知先验，冻结 VLM 原始权重；
- **第二阶段**：冻结已获得的相机先验，在混合操作数据上联合优化全部动作。

这一设计的因果逻辑在于：**相机运动本身是实例无关且较易学习的**——识别“碗被遮挡需要侧移视角”这类语义-视角映射，不依赖于特定操作技能。因此可以先以低成本建立通用主动感知能力，再将其作为先验注入操作学习，避免两类动作在有限数据下相互干扰。

### 3 关键 changed slots

相较于直接微调统一动作空间的 baseline，SaPaVe 在四个维度上做出了结构性改变：

| 设计维度 | Baseline 做法 | SaPaVe 做法 | 证据锚点 |
|---------|-------------|-----------|---------|
| **动作空间设计** | 统一的相机+操作动作空间 | 解耦的相机动作头（2-DoF pitch/yaw）与操作动作头（26-DoF 关节位置） | Sec. 3.1, 3.2, E.0.1 |
| **相机学习方式** | 全量微调 VLA 或离散视角问答 | 基于 LoRA 的相机适配器，在 ActiveViewPose-200K 上单独学习，冻结原 VLM 权重 | Sec. 3.2 |
| **3D 空间知识注入** | 无显式 3D 几何信息 | 通用空间知识注入：利用 MapAnything 编码器融合深度、相机内参等多模态几何信息，通过逐元素加和注入动作头 | Sec. 3.2, E.0.3 |
| **训练策略** | 端到端混合数据训练 | 两阶段课程学习：Stage 1 仅训练相机控制，Stage 2 联合优化相机与操作并冻结相机适配器 | Sec. 3.3, E.1 |

#### 3.1 解耦动作头（Decoupled Action Heads）

策略形式化为 $\pi_{\theta} : \mathcal{O} \times \mathcal{L} \to \mathcal{A}$，其中联合动作轨迹 $A_t = \{A_{\mathrm{head},t}, A_{\mathrm{other},t}\}$ 由头部相机动作和操作动作组成。SaPaVe 使用独立的扩散 Transformer 解码器分别预测两类动作，扩散损失同时优化相机和身体动作噪声：

$$\mathcal{L}_{\mathrm{diff}} = \mathbb{E}_{\tau,\epsilon} [ \lambda_1 \| V_{\theta}^{\mathrm{cam}}(...) - \epsilon^{\mathrm{cam}} \|^2 + \lambda_2 \| V_{\theta}^{\mathrm{body}}(...) - \epsilon^{\mathrm{body}} \|^2 ]$$

消融实验证实：使用统一动作解码器代替解耦头导致平均成功率从 85% 降至 71.25%（Table 5, w/o D.A.H.），验证了解耦设计对多任务学习的必要性。

#### 3.2 相机适配器（Camera Adapter）

通过 LoRA 在冻结的 VLM（Eagle-2，包含 SigLIP-2 图像编码器和 SmolLM2 语言模型）上学习语义到相机运动的对齐：

$$h = W_0 x + \frac{\alpha}{r} B A x$$

这一设计保留了 VLM 的高层语义理解能力，同时以参数高效的方式注入主动感知先验。移除相机适配器（全量微调 VLM）导致性能下降至 73.75%（Table 5, w/o C.A.），证明轻量适配器能更好保留语义信息。

#### 3.3 通用空间知识注入（Universal Spatial Knowledge Injection）

利用 MapAnything 编码器接受多种 3D 几何配置（绝对深度、相机内参等），生成空间标记并通过逐元素加和与 VLM 令牌融合：

$$\phi_{\mathrm{fused}} = \phi_{\mathrm{vlm}} + \beta \cdot \mathrm{Linear}(F_{\mathrm{spatial}})$$

融合后的上下文条件注入扩散去噪过程。消融显示，移除该模块后即使在较简单的遮挡抓取任务上也出现 15% 的性能下跌（Table 5, w/o U.S.K.I.），说明 3D 几何知识对动态视角下的精确执行至关重要。

#### 3.4 两阶段训练损失

**Stage 1** 仅最小化相机运动预测与真值的均方误差：

$$\mathcal{L}_{\mathrm{stage1}} = \mathcal{L}_{\mathrm{MSE}}(A_{\mathrm{head},t}, A_{\mathrm{head},t}^{*})$$

**Stage 2** 加权联合优化相机损失和操作损失（通常 $\lambda_{\mathrm{head}}=1.0$，$\lambda_{\mathrm{other}}=10.0$）：

$$\mathcal{L}_{\mathrm{stage2}} = \lambda_{\mathrm{head}}\mathcal{L}_{\mathrm{head}} + \lambda_{\mathrm{other}}\mathcal{L}_{\mathrm{other}}$$

消融实验表明：移除 Stage 1 训练后，平均成功率从 85% 降至 53.75%，在视野外关节操作任务中成功率减半（Table 5, w/o Stage 1）；仅靠 Stage 1 先验而不进行 Stage 2 微调，成功率为 66.25%（Table 5, w/o Stage 2）。两阶段缺一不可。

### 4 创新有效性的决定性证据

- **语义主动感知**：在 ActiveViewPose-200K 上，仅 2B 参数的 SaPaVe Stage 1 模型平均准确率 84.3%，比通用 VLM Gemini-2.5-Pro 高 11.6 个百分点（Table 1）。
- **主动操作**：在 ActiveManip-Bench 仿真基准上，主动相机配置较固定相机平均成功率提升 38.66 个百分点（74.83% vs. 36.17%，Table 2）；在真实世界 4 项任务中平均成功率 85%，分别超出 π0 40 个百分点和 GR00T-N1 31.25 个百分点（Table 3）。
- **消融验证**：解耦头、相机适配器、空间知识注入、两阶段训练四个设计均通过消融实验证实为必要组件（Table 5）。

### 5 局限与开放问题

当前设计的**主要局限**在于机器人基座固定，操作空间受限于臂展范围：即使头部主动感知到超出范围的物体，也无法执行操作，仅支持局部主动探索而非全局移动搜索。

开放问题包括：如何将主动感知扩展至**移动操作**（同时控制头部和移动底盘），以及如何处理物体被移动到机械臂物理可达范围之外但仍被主动感知到的情形。

## 整体框架

SaPaVe 是一个端到端的主动操作框架，其核心设计理念是将语义主动感知与主动视角执行联合建模。整体架构如图2所示，系统接收 RGB 图像序列与任务语言指令作为输入，输出解耦的相机运动与操作动作序列。

**输入输出流。** 给定观测 $\mathcal{O}$（包含当前及历史 RGB 图像）和语言指令 $\mathcal{L}$，策略 $\pi_{\theta} : \mathcal{O} \times \mathcal{L} \to \mathcal{A}$ 输出联合动作轨迹。采用动作分块策略（action chunking），策略在时间步 $t$ 预测未来 $k$ 步的动作序列 $A_t = \{A_{\mathrm{head},t}, A_{\mathrm{other},t}\}$，其中 $A_{\mathrm{head},t}$ 为头部相机动作（2-DoF pitch/yaw），$A_{\mathrm{other},t}$ 为操作动作（26-DoF 关节位置）。

**Pipeline 模块与数据流。** 系统由四个关键模块串联构成：

1. **VLM Backbone（Eagle-2）**：以 SigLIP-2 图像编码器和 SmolLM2 语言模型为基础，提取多模态高层语义表征。该模块在训练中保持冻结，以保留原始视觉语言能力。

2. **Camera Adapter（LoRA）**：通过低秩适配矩阵 $B$、$A$ 对 VLM 的线性层进行参数高效微调，前向传播为 $h = W_0 x + \frac{\alpha}{r} B A x$。该模块在冻结 VLM 权重的条件下，学习从语义到相机运动的对齐，形成语义主动感知先验。

3. **Universal Spatial Knowledge Injection（MapAnything）**：通用空间编码器接收多种 3D 几何配置（如绝对深度、相机内参），生成空间标记 $F_{\mathrm{spatial}}$，通过逐元素加和与交叉注意力注入去噪过程：$\phi_{\mathrm{fused}} = \phi_{\mathrm{vlm}} + \beta \cdot \mathrm{Linear}(F_{\mathrm{spatial}})$。该模块增强了动态视角下的 3D 几何鲁棒性。

4. **Decoupled Action Heads（DiT）**：基于扩散 Transformer 的双分支解码器，包含独立的相机动作解码器和操作动作解码器。扩散损失函数为：
   $$\mathcal{L}_{\mathrm{diff}} = \mathbb{E}_{\tau,\epsilon} [ \lambda_1 \| V_{\theta}^{\mathrm{cam}}(...) - \epsilon^{\mathrm{cam}} \|^2 + \lambda_2 \| V_{\theta}^{\mathrm{body}}(...) - \epsilon^{\mathrm{body}} \|^2 ]$$
   两个头分别预测相机和身体动作噪声，实现解耦的动作生成。

**两阶段训练策略。** 模块间的协作依赖自下而上的课程学习：

- **Stage 1（语义主动感知先验学习）**：仅训练 Camera Adapter，在 ActiveViewPose-200K 数据集上最小化相机运动预测与真值的均方误差 $\mathcal{L}_{\mathrm{stage1}} = \mathcal{L}_{\mathrm{MSE}}(A_{\mathrm{head},t}, A_{\mathrm{head},t}^{*})$。此阶段建立实例无关的语义相机控制能力。

- **Stage 2（主动操作联合微调）**：冻结 Camera Adapter，联合训练 Decoupled Action Heads，损失函数为加权和 $\mathcal{L}_{\mathrm{stage2}} = \lambda_{\mathrm{head}}\mathcal{L}_{\mathrm{head}} + \lambda_{\mathrm{other}}\mathcal{L}_{\mathrm{other}}$，其中 $\lambda_{\mathrm{head}}=1.0$，$\lambda_{\mathrm{other}}=10.0$。此阶段在保留相机先验的同时，使模型习得主动视角下的操作执行。

**设计动机。** 该框架的核心创新在于将相机运动与操作动作解耦为两个独立动作空间，而非沿用现有 VLA 模型的统一动作空间。这一设计使两类动作可从各自数据中获益：相机运动本身是实例无关且较易学习的，通过大规模相机控制数据即可建立鲁棒先验；而操作动作则可在冻结该先验的条件下高效微调，避免直接扩展动作空间对已有先验的破坏。消融实验证实，使用统一动作解码器替代解耦头会导致平均成功率从 85% 降至 71.25%，验证了解耦设计的必要性。

### 补充图表

![[assets/figures/papers/paper_list_l2415_https_arxiv_org_abs_2603_12193/figures/001_Figure_1.jpg]]
*Figure 1: We propose SaPaVe, an end-to-end active manipulation framework that jointly integrates semantic active perception and activeview execution; the former selectively shifting viewpoints to reveal task-critical cues in cluttered scenes, while the latter grounds newly acquired observations into immediate actions, enabling success even from suboptimal views. (a) For instance, grasping the white bowl in*

![[assets/figures/papers/paper_list_l2415_https_arxiv_org_abs_2603_12193/figures/002_Figure_2.jpg]]
*Figure 2: Overview of SaPaVe. SaPaVe can process RGB images and task instructions and output camera movement and manipulation actions in a decoupled action space. This decoupled design enables the model to achieve active manipulation via a bottom-up, two-stage training strategy: First, large-scale embodiment-agnostic camera control data fosters semantic active perception, which is encoded as prior knowledge in a camera adapter. Second, mixed data together with Universal Spatial Knowledge Injection flexibly incorporate various geometric configurations (e.g., absolute depth, camera intrinsics), thereby enhancing spatial precision for active-view execution*

## 核心模块与公式推导

SaPaVe 的核心设计围绕一个中心矛盾展开：**将相机运动直接纳入 VLA 的动作空间会破坏已有的操作先验，而大规模主动操作数据的稀缺使端到端训练难以收敛**。为此，SaPaVe 通过四个关键模块实现解耦与渐进学习。

### 动作空间解耦与策略定义

策略将观测 $`\mathcal{O}`$ 和语言指令 $`\mathcal{L}`$ 映射到联合动作空间 $`\mathcal{A}`$：

$$`\pi_{\theta} : \mathcal{O} \times \mathcal{L} \to \mathcal{A}`$$

与以往将相机运动与操作统一为单一动作空间的做法不同，SaPaVe 将动作显式解耦为两部分（Sec. 3.1）：

$$`A_t = \{A_{\mathrm{head},t}, A_{\mathrm{other},t}\}`$$

其中 $`A_{\mathrm{head},t}`$ 为头部相机的 2-DoF 运动（pitch/yaw），$`A_{\mathrm{other},t}`$ 为 26-DoF 的关节位置操作动作。策略采用 action chunking 策略，在时间窗口 $`k`$ 内预测动作序列。

### 相机适配器（Camera Adapter）

相机适配器是 SaPaVe 实现语义主动感知先验的核心机制。它通过 LoRA 在冻结的 VLM 骨干上学习语义到相机运动的对齐：

$$`h = W_0 x + \frac{\alpha}{r} B A x`$$

其中 $`W_0`$ 为原始权重，$`B`$ 和 $`A`$ 为低秩矩阵，$`r`$ 为秩，$`\alpha`$ 为缩放因子。该设计保留了 VLM 的高层语义理解能力，同时以参数高效的方式注入相机控制知识。消融实验表明，移除相机适配器（改为全量微调 VLM）导致平均成功率从 85% 降至 73.75%，验证了轻量适配器在保留语义信息方面的优势。

### 解耦动作头（Decoupled Action Heads）

解耦动作头采用扩散 Transformer 架构，包含独立的相机动作解码器和操作动作解码器。扩散过程中的去噪损失同时作用于两个动作空间：

$$`\mathcal{L}_{\mathrm{diff}} = \mathbb{E}_{\tau,\epsilon} [ \lambda_1 \| V_{\theta}^{\mathrm{cam}}(...) - \epsilon^{\mathrm{cam}} \|^2 + \lambda_2 \| V_{\theta}^{\mathrm{body}}(...) - \epsilon^{\mathrm{body}} \|^2 ]`$$

其中 $`V_{\theta}^{\mathrm{cam}}`$ 和 $`V_{\theta}^{\mathrm{body}}`$ 分别预测相机和身体动作的噪声，$`\epsilon^{\mathrm{cam}}`$ 和 $`\epsilon^{\mathrm{body}}`$ 为对应的真实噪声。消融实验显示，使用统一动作解码器代替解耦头会导致成功率从 85% 降至 71.25%，证明解耦设计对多任务学习的必要性。

### 通用空间知识注入（Universal Spatial Knowledge Injection）

该模块通过 MapAnything 编码器融合深度、相机内参等多模态几何信息，生成空间标记后以逐元素加和方式注入去噪过程：

$$`\phi_{\mathrm{fused}} = \phi_{\mathrm{vlm}} + \beta \cdot \mathrm{Linear}(F_{\mathrm{spatial}})`$$

其中 $`\phi_{\mathrm{vlm}}`$ 为 VLM 令牌，$`F_{\mathrm{spatial}}`$ 为空间编码器输出，$`\beta`$ 为融合权重。该设计的灵活性在于可接受多种 3D 几何配置，增强动态视角下的空间精度。消融实验中，移除该模块即使在较简单的遮挡抓取任务上也导致 15% 的性能下跌。

### 两阶段课程学习损失

**第一阶段**（语义主动感知先验学习）：仅训练相机适配器，最小化相机运动预测与真值的均方误差：

$$`\mathcal{L}_{\mathrm{stage1}} = \mathcal{L}_{\mathrm{MSE}}(A_{\mathrm{head},t}, A_{\mathrm{head},t}^{*})`$$

**第二阶段**（主动操作联合微调）：冻结相机适配器，加权联合优化相机损失和操作损失：

$$`\mathcal{L}_{\mathrm{stage2}} = \lambda_{\mathrm{head}}\mathcal{L}_{\mathrm{head}} + \lambda_{\mathrm{other}}\mathcal{L}_{\mathrm{other}}`$$

其中 $`\lambda_{\mathrm{head}}=1.0`$，$`\lambda_{\mathrm{other}}=10.0`$，更高的操作损失权重反映了操作任务的复杂性。消融实验表明，移除第一阶段训练使平均成功率从 85% 降至 53.75%，在视野外关节操作任务中成功率减半；而仅靠第一阶段先验（省略第二阶段）的成功率仅为 66.25%，说明两阶段互为必要补充。

## 实验与分析

### 核心实验设计

SaPaVe 的实验体系围绕三层递进评估构建：首先验证语义主动感知先验本身的质量（ActiveViewPose-200K），其次在仿真环境中系统评估主动相机对操作成功率的因果贡献（ActiveManip-Bench），最后在真实世界场景中检验完整框架的实用性能与泛化能力。这一设计直接对应方法的核心瓶颈——现有 VLA 模型缺乏语义驱动的主动感知能力，且直接扩展动作空间会破坏已有先验。

**基准选择**：主要对比对象包括两类。一类是现有 VLA 模型（**GR00T N1** 和 **π0**），通过直接微调使其输出包含相机运动，以验证“统一动作空间”策略的局限性。另一类是通用视觉语言模型（**Gemini-2.5-Pro**、**Qwen2.5-VL-72B**）和专用空间视觉语言模型（**Multi-SpatialMLLM**），用于评估语义主动感知能力的上限。

### 语义主动感知评估

在 ActiveViewPose-200K 数据集上，SaPaVe 第一阶段模型（仅 2B 参数）取得了 84.3% 的平均成功率，比通用 VLM Gemini-2.5-Pro 高出 11.6 个百分点（Table 1）。值得注意的是，这一优势在 test2 子集上尤为显著，表明模型在更复杂的语义对齐任务上具备更强的判别能力。

这一结果直接验证了核心洞察：**相机运动本身是实例无关且较易学习的**——通过 LoRA 相机适配器在冻结的 VLM 上学习语义到相机运动的对齐，既能保留高层语义理解，又能高效建立主动感知先验。专用空间 VLM（Multi-SpatialMLLM）虽然具备 3D 空间推理能力，但在语义驱动的相机运动预测上仍不及 SaPaVe 第一阶段模型，说明单纯的几何推理不足以替代语义引导的主动感知。

### 仿真环境主动操作评估

ActiveManip-Bench 是首个专门评估主动操作能力的仿真基准，涵盖 12 个任务、100 个物体和 20 个多样化场景（Figure 4）。任务按难度分为无遮挡抓取、遮挡抓取、视野外抓取、无遮挡关节操作、遮挡关节操作和视野外关节操作六类。

![[assets/figures/papers/paper_list_l2415_https_arxiv_org_abs_2603_12193/figures/005_Figure_4.jpg]]
*Figure 4: Overview of ActiveManip-Bench: It is the first simulation benchmark to evaluate active manipulation beyond traditional fixedview settings. ActiveManip-Bench features 12 richly annotated tasks across 100 objects and 20 diverse scenes*

Table 2 的核心发现是：**在相同架构下，将固定相机替换为主动相机后，平均成功率从 36.17% 跃升至 74.83%，绝对提升 38.66 个百分点**。其中，视野外任务的成功率下降最为剧烈——固定相机配置下成功率暴跌超过 60%，这直接量化了“固定近优视角训练”的根本缺陷。主动相机通过语义驱动的视角调整，能够主动揭示被遮挡或处于视野外的任务关键信息，从而在复杂场景中维持高成功率。

![[assets/figures/papers/paper_list_l2415_https_arxiv_org_abs_2603_12193/figures/006_Table_2.jpg]]
*Table 2: Evaluation results for fixed and dynamic cameras in simulation of ActiveManip-Bench. We report the success rate (%) compare to different camera configurations with the same architecture. P.a.P and A.M denote Pick-and-Place and articulated Manipulation*

与现有 VLA 模型的对比（Table 3）进一步强化了这一结论：SaPaVe 在真实世界主动操作任务中平均成功率达 85%，分别超出 π0 40 个百分点和 GR00T N1 31.25 个百分点。直接微调现有 VLA 模型以包含相机运动几乎在所有任务上均表现不佳，这验证了分析中识别的核心瓶颈——**直接扩展动作空间以包含连续相机运动将破坏已有先验，并因大规模主动操作数据稀缺而难以收敛**。

![[assets/figures/papers/paper_list_l2415_https_arxiv_org_abs_2603_12193/figures/007_Table_3.jpg]]
*Table 3: Performance on active manipulation in real-world settings. We report the success rate (%) compared to the existing VLA models. Our approach achieves the best performance*

### 消融实验

Table 5 的消融实验严格验证了每个设计选择的因果贡献，实验在真实世界四类任务上进行，以平均成功率为指标。

![[assets/figures/papers/paper_list_l2415_https_arxiv_org_abs_2603_12193/figures/008_Table_5.jpg]]
*Table 5: Ablation Study on the effect about training strategy of Stage 1 and Stage2, decoupled action head (D.A.H.), camera adapter (C.A.), and universal spatial knowledge injection (U.S.K.I). We report the avarage success rate (%)*

**两阶段训练策略**：移除第一阶段训练（w/o Stage 1）导致平均成功率从 85% 骤降至 53.75%，在视野外关节操作任务中成功率减半。这直接证实了语义主动感知先验是不可或缺的——没有第一阶段建立的相机控制能力，模型无法在第二阶段有效学习主动操作。反之，仅保留第一阶段而省略第二阶段主动操作微调（w/o Stage 2），成功率为 66.25%，说明单独的相机先验不足以完成完整操作任务，两者缺一不可。

**解耦动作头**：使用统一动作解码器代替解耦头（w/o D.A.H.）导致平均成功率降至 71.25%，验证了解耦设计对多任务学习的必要性。统一解码器迫使相机运动和操作动作共享表示空间，两类动作的学习目标相互干扰，这与分析中的因果机制一致——**解耦动作头使得两类动作可从各自数据中获益，避免冲突**。

**相机适配器**：移除相机适配器、直接全量微调 VLM（w/o C.A.）导致性能下降至 73.75%。这证明轻量级 LoRA 适配器能更有效地保留 VLM 的原始语义能力，全量微调可能引入灾难性遗忘，损害模型对任务指令的理解。

**通用空间知识注入**：移除通用空间知识注入（w/o U.S.K.I.）后，平均成功率降至 68.75%。即使在相对简单的遮挡抓取任务上也出现 15% 的性能下跌，说明 3D 几何知识对动态视角下的精确执行至关重要。MapAnything 编码器融合的深度、相机内参等多模态几何信息，为动作头提供了空间定位所需的额外约束。

### 泛化能力评估

Table 4 展示了 SaPaVe 在未见物体、变化光照和多样化场景三个维度上的泛化性能。在遮挡抓取任务上，模型在不同条件下保持 85-95% 的成功率；在视野外关节操作这一最具挑战性的任务上，成功率仍维持在 75-85%。这种鲁棒性源于两阶段训练策略的内在优势：第一阶段在实例无关的大规模数据上建立的语义主动感知先验，天然具备对特定物体和场景的泛化能力；第二阶段冻结该先验，仅优化操作执行，避免了过拟合。

![[assets/figures/papers/paper_list_l2415_https_arxiv_org_abs_2603_12193/figures/009_Table_4.jpg]]
*Table 4: Performance on generalization ability evaluation. We report the success rate (%). Our model demonstrates robust generalization when performing active manipulation across unseen objects, varying lighting conditions, and diverse scenes*

### 失败模式与局限

尽管 SaPaVe 在主动操作任务上表现优异，但其设计存在一个根本性约束：**机器人基座固定，操作空间受限于臂展范围**。当主动感知发现超出机械臂物理可达范围的物体时，模型无法执行操作。当前框架仅支持局部的主动探索，而非全局的移动搜索。这指向两个开放问题：如何将主动感知扩展至移动操作（同时控制头部和移动底盘），以及如何处理物体被移动到可达范围之外但仍被感知到的场景。

从消融实验结果还可以识别出另一个潜在失败模式：当移除通用空间知识注入后，即使在遮挡抓取这类相对简单的任务上也出现显著性能下降，暗示在缺乏显式 3D 几何信息时，模型对深度和空间关系的估计可能不够精确，导致抓取姿态偏差。

### 补充图表

![[assets/figures/papers/paper_list_l2415_https_arxiv_org_abs_2603_12193/figures/010_Figure_5.jpg]]
*Figure 5: Real-world Execution roll-outs (ego & third view)*

![[assets/figures/papers/paper_list_l2415_https_arxiv_org_abs_2603_12193/figures/016_Table_6.jpg]]
*Table 6: Overview of the 12 Active Manipulation Tasks. The tasks are categorized by horizon length and complexity. Success is rigorously defined by geometric thresholds (position, rotation, joint state) or physical quantities (liquid volume), requiring the robot to maintain the goal state for a stabilization period (e.g., 2 seconds)*

![[assets/figures/papers/paper_list_l2415_https_arxiv_org_abs_2603_12193/figures/019_Figure_12.jpg]]
*Figure 12: This image illustrates the active manipulate task performed by the robot in a simulation scenario*

![[assets/figures/papers/paper_list_l2415_https_arxiv_org_abs_2603_12193/figures/022_Figure_14.jpg]]
*Figure 14: This image illustrates the active manipulate task performed by the robot in a real-world scenario*

![[assets/figures/papers/paper_list_l2415_https_arxiv_org_abs_2603_12193/figures/024_Figure_15.jpg]]
*Figure 15: This image illustrates the active manipulate task performed by the robot in a real-world scenario*

## 方法谱系与知识库定位

### 1. 与现有工作的关系

SaPaVe 的核心贡献在于**将语义主动感知与操作执行解耦，并通过自下而上的两阶段训练策略，以低数据成本赋予 VLA 模型主动操作能力**。这一设计直接回应了现有 VLA 范式的根本瓶颈：已有模型（如 **GR00T N1**、**π0**）依赖固定近优视角采集的演示数据进行训练，缺乏语义驱动的主动视角调整能力；若简单地将连续相机运动直接扩展进统一动作空间进行端到端微调，既会破坏 VLM 中已编码的先验知识，又会因大规模主动操作数据的稀缺而难以收敛。

与上述端到端微调路线不同，SaPaVe 的方法论定位更接近**模块化解耦与课程学习**的交叉地带：

- **相对于统一动作空间的 VLA 模型**：GR00T N1 与 π0 将相机运动与操作动作统一建模，在固定视角下表现良好，但面对遮挡或视野外目标时缺乏主动调整视角的机制。SaPaVe 通过解耦动作头（Decoupled Action Heads）将相机动作（2-DoF pitch/yaw）与操作动作（26-DoF 关节位置）分离，使得两类动作可以从各自的数据中独立获益，避免了统一空间下的冲突。消融实验证实，使用统一动作解码器代替解耦头会导致真实世界平均成功率从 85% 降至 71.25%（Table 5）。

- **相对于离散视角选择的 VQA 方法**：部分工作通过视觉问答方式选择预定义视角，缺乏连续、平滑的相机运动生成能力。SaPaVe 的第一阶段在 ActiveViewPose-200K（200K 图像-语言-相机运动对）上学习语义到连续相机运动的映射，仅 2B 参数即取得 84.3% 的平均准确率，比通用 VLM **Gemini-2.5-Pro**（72.7%）高 11.6 个百分点，比专用空间 VLM **Multi-SpatialMLLM** 也有显著优势（Table 1）。

- **相对于纯操作策略模型**：SaPaVe 并非替代现有操作策略，而是在其上叠加主动感知能力。其两阶段训练中，第二阶段冻结相机适配器（Camera Adapter），仅微调解耦动作头，使得模型在保留第一阶段习得的语义主动感知先验的同时，灵活适应下游操作任务。

### 2. 适用边界

SaPaVe 的当前设计适用于以下场景：

1. **固定基座的桌面级操作**：机器人基座固定，操作空间受限于机械臂展范围。主动感知主要通过调整头部相机（2-DoF pitch/yaw）来获取任务关键视觉线索，适用于遮挡抓取、视野外关节操作等需要局部视角调整的任务。
2. **语义驱动的视角选择**：模型根据语言指令和当前观测，自主判断需要看向何处——例如抓取被遮挡的碗时需要旋转视角以暴露目标，而操作抽油烟机手柄时仅需短暂上移（Figure 1a）。
3. **多任务主动操作**：ActiveManip-Bench 涵盖 12 个任务、100 个物体、20 个场景，SaPaVe 在仿真中平均成功率达 74.83%（主动相机），远超固定相机配置的 36.17%（Table 2）。

**明确不适用的边界**：

- **移动操作（mobile manipulation）**：当前工作仅控制头部相机，机器人基座固定。若目标物体被移动到机械臂物理可达范围之外，即使主动感知到也无法执行操作。这一限制在论文中已被明确指认为当前局限。
- **全局搜索与导航**：SaPaVe 的主动感知是局部的视角调整，而非移动底盘驱动的全局搜索。对于需要先导航到目标区域再操作的场景，当前框架无法直接适用。

### 3. 局限与开放问题

**已识别的局限**：

论文明确指出的核心局限是**操作空间受限于固定基座**：即使头部相机通过主动感知发现了超出臂展范围的目标物体，机器人也无法执行操作。这限制了 SaPaVe 从“局部主动探索”向“全局主动操作”的扩展。

此外，从消融实验（Table 5）可以推断以下边界条件：

- **语义主动感知先验是不可或缺的**：移除 Stage 1 训练后，视野外关节操作任务的成功率减半（Table 5），表明仅靠操作数据无法习得有意义的主动感知行为。
- **3D 空间知识对动态视角下的执行至关重要**：移除通用空间知识注入（Universal Spatial Knowledge Injection）后，即使在较简单的遮挡抓取任务上也出现 15% 的性能下跌（Table 5），说明在相机运动导致视角变化时，显式的 3D 几何信息（深度、相机内参等）对动作预测的鲁棒性有关键作用。
- **LoRA 相机适配器优于全量微调**：移除相机适配器（改为全量微调 VLM）导致性能从 85% 降至 73.75%（Table 5），验证了轻量适配器能更好地保留 VLM 的高层语义信息。

**开放问题**：

1. **如何将主动感知扩展至移动操作？** 当机器人同时控制头部相机和移动底盘时，动作空间维度增加，解耦策略需要重新设计——是进一步解耦为头部/底盘/操作三个动作空间，还是寻找更紧致的统一表示？
2. **如何处理“看得见但够不着”的情况？** 当物体被主动感知到但超出物理可达范围时，模型应如何决策？是放弃当前目标、请求人类干预，还是触发导航行为？这需要在策略层面引入更高层的任务规划。
3. **主动感知的触发机制**：当前模型在每一步都预测相机动作，但并非所有场景都需要主动调整视角。如何学习“何时该动、何时该静”的稀疏主动感知策略，可能是提升效率的方向。
4. **跨具身泛化**：SaPaVe 的相机适配器在实例无关的相机控制数据上训练，理论上具备一定的具身无关性。但当前验证仅限于单一机器人平台，其向不同自由度配置的机器人迁移的能力尚待验证。

### 4. 知识库定位

SaPaVe 在机器人学习的知识谱系中，位于 **VLA 模型**、**主动感知**与**课程学习**的交汇点：

- **从 VLA 模型继承**：以 Eagle-2（SigLIP-2 + SmolLM2）作为 VLM 骨干，保留了视觉语言理解的高层语义能力。
- **向主动感知贡献**：提出了语义驱动的连续相机运动生成范式，区别于离散视角选择或固定视角操作，并配套发布了 ActiveViewPose-200K 和 ActiveManip-Bench 两个基准。
- **从课程学习借鉴**：两阶段训练（先学相机控制，再联合优化）本质上是一种自下而上的课程设计，使得模型先掌握较易学习的实例无关技能（相机运动），再在此基础上学习更复杂的任务相关操作。

SaPaVe 的核心洞见——“相机运动本身是实例无关且较易学习的”——为未来工作提供了一个可复用的设计原则：在构建复杂机器人技能时，识别并分离出那些可以大规模、低成本、跨任务学习的子技能，通过课程训练将其固化为先验，再在此基础上学习任务特定的能力。

## 原文 PDF

![[paperPDFs/CVPR_2026/SaPaVe_Towards_Active_Perception_and_Manipulation_in_Vision_Language_Action_Models_for_Robotics.pdf]]