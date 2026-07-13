---
title: "OmniNav: A Unified Framework for Prospective Exploration and Visual-Language Navigation"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/OmniNav_A_Unified_Framework_for_Prospective_Exploration_and_Visual_Language_Navigation.pdf
project_link: null
code_link: null
openreview_forum_id: zGtTQTD1zu
aliases:
- OmniNav
tags:
- ICLR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/vision_models_multimodal
core_operator: "大规模通用视觉-语言数据的联合多任务训练，实质性提升泛化能力。"
primary_logic: "采用快-慢双系统架构：快系统基于流匹配策略生成连续航点实现低延迟控制；慢系统利用长期视觉记忆和边界推理进行全局规划与子目标选择；同时融入通用视觉-语言数据，显著增强指令理解和物体感知的鲁棒性。"
claims:
- "快系统采用流匹配策略生成连续航点，避免动作离散化的精度损失和延迟累积。"
- "慢系统利用边界和长期视觉记忆进行语义相关的子目标选择，引入思维链推理。"
- "训练统一大规模通用视觉-语言数据与多种导航任务，显著增强指令遵循和物体感知。"
- "在R2R-CE和RxR-CE上仅使用纯RGB输入即实现SOTA成功率和路径效率。"
---

# OmniNav: A Unified Framework for Prospective Exploration and Visual-Language Navigation

> [!tip] 核心洞察
> 采用快-慢双系统架构：快系统基于流匹配策略生成连续航点实现低延迟控制；慢系统利用长期视觉记忆和边界推理进行全局规划与子目标选择；同时融入通用视觉-语言数据，显著增强指令理解和物体感知的鲁棒性。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | OmniNav：前瞻性探索与视觉-语言导航的统一框架 |
| 英文题名 | OmniNav: A Unified Framework for Prospective Exploration and Visual-Language Navigation |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=zGtTQTD1zu) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/vision_models_multimodal |
| Method | OmniNav |
| Dataset | R2R-CE Val-Unseen, RxR-CE Val-Unseen, HM3D-OVON Val-Unseen, CityWalker (Point-goal) |

> [!tip] 效果简介
> - R2R-CE Val-Unseen 上，SR (Success Rate) 为 69.5，对比 65.1 (CorrectNav)，变化 +4.4%。
> - RxR-CE Val-Unseen 上，SR 为 73.6，对比 69.3 (CorrectNav)，变化 +4.3%。
> - HM3D-OVON Val-Unseen 上，SR 为 59.2 (OmniNav* w/ CoT)，对比 40.8 (MTU3D)，变化 +18.4%。

## 概要

视觉-语言导航（VLN）的核心瓶颈并非导航策略学习本身，而在于对通用指令和开放词汇物体的稳健理解。现有方法普遍依赖动作离散化，导致精度损失与延迟累积；同时，单一端到端架构缺乏长程规划能力，难以应对复杂场景中的探索需求。

OmniNav 针对上述问题提出了一种**快-慢双系统统一框架**。其核心洞察在于：快系统基于流匹配策略生成连续航点，实现低延迟闭环控制；慢系统利用长期视觉记忆与边界推理进行全局规划与子目标选择；二者通过中央记忆模块桥接，兼顾局部敏捷性与全局一致性。此外，训练过程融入大规模通用视觉-语言数据（图像描述、指称/定位等），显著增强了指令遵循与开放词汇物体感知的鲁棒性。

在方法谱系中，OmniNav 相较于现有基线做出了四项关键改变：（1）动作生成从自回归离散动作块预测转向**基于条件流匹配的连续航点生成**（非自回归）；（2）系统架构从单一 VLM 端到端预测转向**快-慢双系统协同**；（3）训练数据从仅使用特定任务导航数据转向**联合通用视觉-语言数据**；（4）子目标选择从简单距离启发式转向**基于语义和思维链推理的边界选择**。

实验证据充分支撑上述设计。在 R2R-CE 和 RxR-CE 基准上，OmniNav 仅使用纯 RGB 输入即达到 SOTA 成功率，分别超越此前最优模型 CorrectNav（Yu et al., arXiv 2025）**4.4%** 和 **4.3%**。在物体目标导航 HM3D-OVON 上，OmniNav 较 MTU3D（Zhu et al., arXiv 2025）提升 **18.4%**（Val-Unseen），同义词泛化场景提升 **23.6%**。消融实验证实，流匹配策略头、慢速系统、通用数据及思维链推理各组件均贡献显著增益；数据组成消融进一步表明，去除 Embodied Q&A 或 Grounding/Referring 数据会导致小物体识别性能下降，而去除 General MLLM 数据则导致不规则物体识别失败。模型规模消融显示，数据丰富时 3B 与 7B 模型性能接近（57.7 vs 57.9），表明此时模型规模并非瓶颈。

方法仍存在若干局限：慢速系统的完整物理部署尚未实现；复杂纹理物体（如衣物、镜子）的识别鲁棒性不足；数据组成、质量与模型规模之间的缩放关系有待系统研究。

视觉-语言导航（VLN）要求智能体在复杂三维环境中根据自然语言指令或物体描述自主移动并完成任务。近年来，该领域在模拟基准上取得了显著进展，但多数方法仍面临两个根本性瓶颈：**动作生成的精度与延迟矛盾**，以及**对通用指令和开放词汇物体的稳健理解不足**。

在动作生成层面，主流方法普遍采用自回归离散动作块预测策略（如 CorrectNav、StreamVLN 等），将连续导航动作离散化为有限的动作类别。这种离散化不可避免地引入精度损失，且自回归逐块生成导致控制延迟随序列长度累积，难以满足真实场景中低延迟闭环控制的需求。

在语义理解层面，现有方法通常仅在特定任务的导航数据上训练，缺乏对开放世界中多样化指令表述和新颖物体类别的泛化能力。当面对训练中未见过的物体（如不规则纹理物体、小尺寸背景物体）或复杂指令时，模型的理解鲁棒性急剧下降。这一瓶颈的根源并非导航策略学习本身，而是训练数据中通用视觉-语言知识的匮乏。

针对上述缺口，OmniNav 提出了一个统一的解决方案。其核心洞察在于：**采用快-慢双系统架构**，快系统基于流匹配策略生成连续航点以实现低延迟控制，慢系统利用长期视觉记忆和边界推理进行全局规划与子目标选择；同时**融入大规模通用视觉-语言数据**进行联合多任务训练，从根本上提升指令理解和物体感知的鲁棒性。这一设计使得 OmniNav 能够在单一框架下支持指令目标、物体目标和点目标等多种导航任务，并在多个基准上以纯 RGB 输入实现最优性能。

## 核心方法与创新机理

OmniNav 的核心创新并非提出全新的导航策略学习范式，而是针对现有视觉-语言导航（VLN）系统在**通用指令理解、开放词汇物体感知和低延迟连续控制**三个维度的根本瓶颈，构建了一套协同优化的系统架构与训练方案。其主要创新点体现在以下四个关键维度。

### 1. 快-慢双系统架构与中央记忆协同

OmniNav 摒弃了单一 VLM 端到端预测动作的基线方案，转而采用快-慢双系统协同架构，通过中央记忆模块实现桥接，使决策兼具局部敏捷性与全局一致性。

- **快系统（Fast System）**：基于 VLM 融合的多模态上下文，并行生成连续空间航点序列，实现低延迟闭环控制。
- **慢系统（Slow System）**：利用长期视觉记忆和边界（frontier）线索进行全局规划与子目标选择。当目标可见时，快速定位并生成子目标坐标；当目标不可见时，通过语义相关的边界推理选择下一个探索子目标，并引入思维链（Chain-of-Thought）分解复杂任务。
- **中央记忆模块**：以 KV 缓存和环形缓冲区维护关键时空上下文，使快慢系统共享历史视觉与位姿信息，确保局部动作与全局规划的一致性。

### 2. 基于流匹配的连续航点生成

在动作生成方式上，OmniNav 用**条件流匹配策略**替代了基线方法普遍采用的自回归离散动作块预测，从根本上解决了动作离散化带来的精度损失和延迟累积问题。

- 快系统将航点预测形式化为条件扩散生成任务，非自回归地输出 $H=5$ 个连续空间航点，每个航点编码为：
  $$ \mathbf{w}_t^{(i)} = \left( x^{(i)}, y^{(i)}, \sin\theta^{(i)}, \cos\theta^{(i)}, c^{(i)} \right) $$
  其中位置采用 2D 坐标，方向采用正弦-余弦编码以避免周期性跳变，$c^{(i)}$ 为二值到达标志。
- 训练时通过流匹配目标学习去噪残差：
  $$ \mathbb{E}_{\tau, \epsilon} \left[ \left\| \pi( \mathbf{O}_{VLM}, \mathbf{w}_{t:t+H}^{\tau} ) - \left( \epsilon - \mathbf{w}_{t:t+H} \right) \right\|^2 \right] $$
  其中 $\mathbf{w}_{t:t+H}^{\tau} = \tau \mathbf{w}_{t:t+H} + (1-\tau)\boldsymbol{\epsilon}$ 为带噪航点序列。
- 推理时通过 $S$ 步欧拉积分从噪声逐步去噪，生成平滑航点序列，实现 5Hz 低延迟闭环控制。

### 3. 语义感知与推理驱动的边界选择

在子目标选择策略上，OmniNav 摒弃了基于简单距离启发式或随机选择最近边界的基线做法，提出了**语义和推理感知的边界选择**机制。

- 将每个边界与其对应的自我中心图像关联，利用 VLM 在这些视图上执行显式思维链推理，判断哪个边界对当前任务更具信息量或前景。
- 结合 3D 占据地图构建可探索/未知区域的边界，使慢系统能够基于视觉事实和语义先验进行可解释的子目标选择，显著提升探索效率。

### 4. 统一通用视觉-语言数据的联合多任务训练

在训练数据组成上，OmniNav 突破了仅使用特定任务导航数据的局限，将**大规模通用视觉-语言数据**与多种导航任务联合训练，这是提升泛化能力的关键因果调控变量。

- 训练数据包含四类：导航任务数据、具身问答数据、通用 MLLM 数据和指称/定位数据。
- 采用两阶段训练策略：第一阶段以自回归目标学习离散变量；第二阶段附加流匹配策略头预测连续航点，同时混入 20% 第一阶段数据以防止 VLM 基础能力退化。
- 消融实验表明，去除具身问答或指称/定位数据会导致小物体识别性能下降；去除通用 MLLM 数据则导致不规则物体识别失败。加入额外数据后，3B 与 7B 模型性能接近（57.7 vs 57.9），表明数据丰富时模型规模并非瓶颈。

![[assets/figures/papers/paper_list_l36_https_openreview_net_forum_id_zGtTQTD1zu/figures/001_Figure_1.jpg]]
*Figure 1: The fast system can independently handle multi-task navigation, using the VLM backbone and a flow-matching policy to rapidly generate waypoints. Building on this, a slow thinking module is integrated to enable long-term memory and planning: it constructs long-range spatial and semantic memory using frontiers and images, and provides subgoal cues. The collaboration between the slow and fast proceeds as follows: the slow system uses frontiers or memory to generate high-level subgoals, once a subgoal is determined, the fast system takes over and progressively produces lowlevel waypoint sequences, ultimately reaching the target*

![[assets/figures/papers/paper_list_l36_https_openreview_net_forum_id_zGtTQTD1zu/figures/003_Figure_3.jpg]]
*Figure 3: Data composition overview. Four data types are used for training: Navigation task data, Embodied Q&A data, General MLLM data and Grounding and referring data*

OmniNav 的核心设计是一个快-慢双系统协作架构，通过中央记忆模块桥接局部敏捷控制与全局语义规划。该架构在单一 VLM 骨干上统一处理指令目标、物体目标和点目标导航，无需任务特定的分支或切换逻辑。

### 系统架构与模块关系

整体 pipeline 由四个关键模块构成：

**VLM 主干**：采用 Qwen2.5-VL-3B-Instruct 作为多模态特征融合与视觉-语言上下文理解的基础模型。所有视觉观测和任务指令经统一的多模态分词后输入 VLM，产出融合了视觉与语言上下文的特征表示 $\mathbf{O}_{VLM}$。

**快速系统（Fast System）**：基于流匹配策略头（Flow Matching Policy Head）并行生成连续航点序列。该策略头采用 DiT（Denoising Transformer）架构，包含自注意力块和交叉注意力块——后者以 VLM 的视觉-语言上下文为条件。快速系统以非自回归方式一次输出 $H=5$ 个连续空间航点，每个航点编码为五维向量：

$$\mathbf{w}_t^{(i)} = \left( x^{(i)}, y^{(i)}, \sin\theta^{(i)}, \cos\theta^{(i)}, c^{(i)} \right)$$

其中 $(x, y)$ 为局部坐标系下的 2D 位置，正弦-余弦编码避免方向角的周期性跳变，$c$ 为二值完成标志。航点预测被形式化为条件扩散生成任务：训练时通过时间步 $\tau$ 线性插值地面真值与高斯噪声构造带噪序列 $\mathbf{w}_{t:t+H}^\tau$，策略网络 $\pi$ 学习估计噪声与真值之间的残差：

$$\mathbb{E}_{\tau,\epsilon} \left[ \left\| \pi(\mathbf{O}_{VLM}, \mathbf{w}_{t:t+H}^\tau) - (\epsilon - \mathbf{w}_{t:t+H}) \right\|^2 \right]$$

推理时通过 $S$ 步欧拉积分从纯噪声逐步去噪，得到平滑的航点序列：

$$\mathbf{w}_{t:t+H}^{\tau+\Delta\tau} = \mathbf{w}_{t:t+H}^\tau + \frac{1}{S} \pi(\mathbf{O}_{VLM}, \mathbf{w}_{t:t+H}^\tau), \quad \Delta\tau = \frac{1}{S}$$

快速系统独立运行时即可实现 5 Hz 的低延迟闭环控制，避免动作离散化带来的精度损失和延迟累积。

**慢速系统（Slow System）**：负责全局规划与子目标选择。它维护 3D 占据地图，将空间区域划分为已探索和未知，边界点（frontiers）即两类区域的交界处。慢速系统将每个边界关联到其对应的自我中心图像，利用显式的思维链（Chain-of-Thought）推理对边界视图进行语义评估，选择与当前任务语义最相关或信息量最大的边界作为探索子目标。当目标出现在当前或历史视野中时，慢速系统直接定位目标并生成子目标坐标，驱动快速系统渐进逼近。

**中央记忆模块（Central Memory）**：以 KV 缓存和环形缓冲区维护带位姿标记的历史图像序列。慢速系统通过采样策略将历史上下文与未来探索连接：收集智能体当前位置附近的历史图像，对每个边界遍历这些图像以评估语义关联性。中央记忆为快慢系统提供关键的时空上下文，使决策兼具局部敏捷性和全局一致性。

### 输入输出流

1. **输入**：RGB 图像观测、任务指令（自然语言指令 / 物体名称 / 目标点坐标）、可选深度与里程计信息（仅慢速系统需要，用于构建占据地图）。
2. **VLM 处理**：多模态输入经统一分词后送入 VLM 骨干，产出融合上下文特征 $\mathbf{O}_{VLM}$。
3. **快速通路**：$\mathbf{O}_{VLM}$ 直接输入流匹配策略头，经 $S$ 步去噪生成连续航点序列，底层控制器执行并更新位姿。
4. **慢速通路**：当目标不可见时触发。慢速系统基于占据地图提取边界集合，从中央记忆检索相关历史图像，通过思维链推理选择子目标。子目标坐标反馈给快速系统，由其生成航点执行。
5. **输出**：连续空间航点序列（位置 + 朝向），或离散动作（在仅需离散输出的任务中）。

### 训练流程

训练采用两阶段策略，防止连续控制微调侵蚀基础 VLM 的能力：

- **阶段一**：自回归目标训练离散变量预测（动作类型、目标类别等），融入大规模通用视觉-语言数据（图像描述、指称/定位、具身问答、通用 MLLM 数据），如 Figure 3 所示，四类数据总计约 420 万样本。使用 96 块 NVIDIA H20 GPU 训练约 120 小时。
- **阶段二**：附加流匹配策略头，联合训练连续航点预测，同时回放 20% 的阶段一离散数据以保持 VLM 基础能力。使用 64 块 H20 GPU 训练约 48 小时。航点坐标采用最小-最大归一化以保证训练稳定。

快-慢系统在训练中端到端协同：慢速系统的子目标选择和快速系统的航点生成共享同一 VLM 骨干，通过统一的训练框架同时优化。

### 快-慢双系统架构

OmniNav 的核心架构由快速系统（Fast System）、慢速系统（Slow System）和中央记忆模块（Central Memory）三部分协同构成。快速系统基于 VLM 主干（Qwen2.5-VL-3B-Instruct）融合多模态上下文，通过流匹配策略并行生成连续航点序列，实现低延迟闭环控制；慢速系统利用长期视觉记忆和边界推理进行全局规划，生成子目标与子任务；中央记忆模块以 KV 缓存和环形缓冲区维护位姿标记的历史图像，为快慢系统提供关键的时空上下文，使得决策既具备局部敏捷性又保持全局一致性。

### 流匹配策略头

快速系统的核心是流匹配策略头（Flow Matching Policy Head），采用去噪扩散 Transformer（DiT）架构建模航点序列。该策略网络由自注意力块和交叉注意力块组成，交叉注意力块关注 VLM 主干输出的视觉-语言融合特征 $\mathbf{O}_{VLM}$。与主流方法中自回归离散动作块预测不同，流匹配策略以非自回归方式并行生成连续航点，避免了动作离散化带来的精度损失和延迟累积。

### 航点表示

每个航点编码为 5 维向量：

$$\mathbf{w}_t^{(i)} = \left( x^{(i)}, y^{(i)}, \sin\theta^{(i)}, \cos\theta^{(i)}, c^{(i)} \right)$$

其中 $(x, y)$ 为 2D 位置坐标，$(\sin\theta, \cos\theta)$ 以正弦-余弦编码表示朝向角（避免角度周期性跳变），$c \in \{0, 1\}$ 为二值完成标志。快速系统并行输出 $H=5$ 个连续航点 $\mathbf{w}_{t:t+H} \in \mathbb{R}^{H \times 5}$。

### 流匹配训练与推理

训练时，通过时间步 $\tau$ 在地面真值航点序列与高斯噪声之间线性插值构造带噪航点：

$$\mathbf{w}_{t:t+H}^{\tau} = \tau \mathbf{w}_{t:t+H} + (1 - \tau) \boldsymbol{\epsilon}$$

策略网络 $\pi$ 的训练目标为估计噪声与真值之间的残差：

$$\mathbb{E}_{\tau, \epsilon} \left[ \left\| \pi(\mathbf{O}_{VLM}, \mathbf{w}_{t:t+H}^{\tau}) - (\epsilon - \mathbf{w}_{t:t+H}) \right\|^2 \right]$$

推理时，从纯噪声出发，通过 $S$ 步欧拉积分逐步去噪，得到平滑航点序列：

$$\mathbf{w}_{t:t+H}^{\tau + \Delta\tau} = \mathbf{w}_{t:t+H}^{\tau} + \frac{1}{S} \pi(\mathbf{O}_{VLM}, \mathbf{w}_{t:t+H}^{\tau}), \quad \Delta\tau = \frac{1}{S}$$

### 慢速系统的边界推理

慢速系统维护 3D 占据地图，将空间区域分类为已探索或未知，边界点定义为已探索与未知区域的分界。与基线方法中基于简单距离启发式或随机选择最近边界的策略不同，OmniNav 采用语义和推理感知的边界选择：将每个边界与其对应的自我中心图像关联，通过显式的思维链推理（Chain-of-Thought）评估各边界的语义相关性和探索价值，从而选择最具信息量或最具前景的子目标。当目标出现在当前或历史视野中时，慢速系统快速定位目标并生成驱动快速系统逐步逼近的子目标坐标。

## 实验与关键发现

### 核心性能对比

OmniNav 在多个导航基准上取得了当前最优结果，其性能增益主要源于快-慢双系统架构与通用视觉-语言数据联合训练的双重作用。

**指令目标导航**：在 R2R-CE 和 RxR-CE 的 Val-Unseen 划分上，OmniNav 仅使用纯 RGB 输入即超越所有对比方法。如 Table 1 所示，OmniNav 在 R2R-CE 上达到 69.5% 成功率（SR），较此前最优方法 CorrectNav（Yu et al., arXiv 2025）的 65.1% 提升 4.4 个百分点；在 RxR-CE 上达到 73.6% SR，较 CorrectNav 的 69.3% 提升 4.3 个百分点。路径效率指标 SPL 同样领先（R2R-CE: 66.1; RxR-CE: 62.0），说明流匹配策略生成的连续航点不仅提高了到达率，也优化了路径质量。值得注意的是，所有参与比较的方法均不使用深度、全景或里程计信息，比较条件公平。

![[assets/figures/papers/paper_list_l36_https_openreview_net_forum_id_zGtTQTD1zu/figures/004_Table_1.jpg]]
*Table 1: Main comparison with prior methods on the Val-Unseen split of R2R-CE and RxR-CE*

**物体目标导航**：在 HM3D-OVON 基准上，OmniNav 的增益更为显著。仅使用快速系统（纯视觉输入）时，OmniNav 在 Val-Unseen 上达到 43.5% SR，已超越此前最强方法 MTU3D（Zhu et al., arXiv 2025）的 40.8%。当集成慢速系统并启用思维链推理后（OmniNav* w/ CoT），SR 跃升至 59.2%，较 MTU3D 提升 18.4 个百分点。在同义词泛化测试（Val-Seen-Synonyms）上，OmniNav* 达到 68.6% SR，较 MTU3D 的 45.0% 提升 23.6 个百分点，充分验证了通用视觉-语言数据训练带来的开放词汇物体感知能力。

**点目标导航**：在 CityWalker 数据集上，OmniNav 的平均方向误差（MAOE）为 11.53%，较原 CityWalker 方法的 15.23% 降低 3.7 个百分点，表明统一架构对点目标模态同样有效。

### 消融实验：组件贡献的因果链

Table 3 的消融实验揭示了各组件对 HM3D-OVON Val-Unseen 性能的独立贡献，其因果逻辑清晰：

![[assets/figures/papers/paper_list_l36_https_openreview_net_forum_id_zGtTQTD1zu/figures/006_Table_3.jpg]]
*Table 3: Ablation study on HM3D-OVON Val-Unseen*

1. **基础 VLM 策略头**（仅快速系统，无慢速系统、无通用数据）：SR 43.5%，SPL 22.1。这是流匹配航点生成相对于传统自回归动作块预测的基线增益来源。
2. **+ 慢速系统**：SR 跃升至 55.9%（+12.4 个百分点），SPL 提升至 29.7。慢速系统通过边界推理和长期视觉记忆进行语义相关的子目标选择，解决了纯反应式策略在长程探索中的迷航问题。
3. **+ 通用视觉-语言数据**：SR 进一步提升至 57.7%（+1.8 个百分点）。通用数据（图像描述、指称/定位、通用 MLLM 数据）增强了模型对不规则和罕见物体的识别鲁棒性。
4. **+ 思维链推理**：SR 达到 59.2%（+1.5 个百分点），SPL 达到 33.2。思维链使慢速系统的子目标选择过程透明化，支持过程级自检与纠错。

各组件增益叠加后的总提升为 15.7 个百分点 SR，其中慢速系统的贡献最大，通用数据和思维链提供了进一步的边际增益。

### 数据组成消融：哪些数据解决了哪些失败模式

Table 4 和附录分析揭示了不同数据类型对物体识别能力的具体影响：

![[assets/figures/papers/paper_list_l36_https_openreview_net_forum_id_zGtTQTD1zu/figures/008_Table_4.jpg]]
*Table 4: Ablation Study of Data on HM3D-OVON Val-Unseen*

- **去除 Embodied Q&A 数据或 Grounding/Referring 数据**：导致小物体（如 picture、flowerpot）识别性能显著下降。这类数据提供了具身场景下的精细视觉-语言对齐，对细节物体的感知至关重要。
- **去除 General MLLM 数据**：导致不规则物体（如 handrail、stair）识别失败。通用多模态大语言模型数据覆盖了更广泛的视觉概念，弥补了导航专用数据中罕见物体类别的不足。
- **三种数据联合使用**：SR 达到 57.7，较不使用任何额外数据的 55.9 提升 1.8 个百分点。单一数据类型增益有限（如仅加 General MLLM 数据为 56.5），联合使用产生互补效应。

### 模型规模消融：数据丰富度决定规模瓶颈

Table 5 的模型规模消融揭示了数据与模型容量之间的交互关系：

![[assets/figures/papers/paper_list_l36_https_openreview_net_forum_id_zGtTQTD1zu/figures/009_Table_5.jpg]]
*Table 5: Ablation Study of Model Size on HM3D-OVON Val-Unseen*

- **无额外数据时**：7B 模型（SR 57.2）优于 3B 模型（SR 55.9），差距 1.3 个百分点。数据稀缺时，更大的模型容量带来明显优势。
- **有额外数据时**：3B 模型（SR 57.7）与 7B 模型（SR 57.9）性能几乎持平，差距仅 0.2 个百分点。这表明当训练数据足够丰富多样时，3B 规模的模型容量已非瓶颈，进一步增大模型带来的边际收益递减。

这一发现对实际部署具有重要指导意义：在数据充足的条件下，3B 模型即可达到接近饱和的性能，有利于降低推理延迟和计算成本。

### 真实机器人部署与工程可行性

Figure 4 展示了 OmniNav 在四足机器人上的零样本部署结果，覆盖三类导航任务：
- **物体目标**：寻找饮水机、穿粉色衬衫的人、垃圾桶
- **点目标**：纯视觉避障（避开沙发、人和椅腿）
- **指令目标**：遵循自然语言指令导航

快系统在云端推理可达 5 Hz 控制频率，满足实时闭环控制需求。但慢速系统的完整物理部署及在真实环境约束下的系统优化尚未实现，这是作者明确指出的未来工作方向。

### 已知失败模式与局限

1. **复杂纹理物体识别不稳定**：衣物、镜子等纹理复杂的物体，无论 3B 还是 7B 模型均存在识别失败，这是当前视觉-语言模型的共性瓶颈。
2. **慢速系统物理部署未完成**：慢速系统涉及边界推理和思维链生成，计算延迟与高频控制需求之间的权衡尚未在真实硬件上进行系统优化。
3. **规模化法则研究缺失**：数据质量、数据组成和模型规模三者之间的联合缩放关系尚未系统探索，当前结论仅基于 3B 与 7B 两个规模点的对比。

## 定位与知识库关联

### 1. 方法定位与核心差异

OmniNav 的架构选择直接回应了当前视觉-语言导航（VLN）领域的两大瓶颈：**通用指令与开放词汇物体的稳健理解**不足，以及**动作离散化带来的精度损失与延迟累积**。其核心设计——快-慢双系统协同与流匹配航点生成——与现有基线形成了三个层面的结构性差异。

**动作生成范式**：现有主流方法普遍采用自回归离散动作块预测，例如 CorrectNav（Yu et al., arXiv 2025）和 StreamVLN（Wei et al., arXiv 2025）在指令导航中逐 token 生成离散动作序列。OmniNav 的快系统直接摒弃了这一范式，转而采用基于条件流匹配（flow matching）的连续航点并行生成。具体而言，快系统一次并行输出 5 个连续空间航点，每个航点编码为 $(x, y, \sin\theta, \cos\theta, c)$，其中正弦-余弦方向编码避免了角度周期性跳变。这一设计从根源上消除了离散化导致的精度退化，同时将控制延迟压缩至 5 Hz 的闭环推理水平。

**系统架构**：现有方法多为单一 VLM 端到端预测动作，缺乏显式的长时规划能力。OmniNav 的快-慢双系统架构引入了明确的分工：慢系统利用长期视觉记忆和 3D 占据地图提取的边界（frontier）进行全局规划与子目标选择，快系统则基于 VLM 融合的多模态上下文和流匹配策略头生成低延迟航点序列。两个系统通过中央记忆模块（基于 KV 缓存和环形缓冲区的时空上下文）桥接，实现了局部敏捷性与全局一致性的协调。

**子目标选择策略**：在物体目标导航中，现有方法（如 MTU3D, Zhu et al., arXiv 2025）通常基于简单距离启发式或随机选择最近边界进行探索。OmniNav 的慢系统引入了语义与推理感知的边界选择：将每个边界与其对应的自我中心图像关联，然后通过显式的思维链（Chain-of-Thought）推理，判断哪个边界对当前任务更具信息量或更有前景。这一机制使子目标选择过程可解释、可自查，并显著提升了探索效率——在 HM3D-OVON Val-Unseen 上，加入慢系统与思维链后 SR 从 43.5 跃升至 59.2（Table 3）。

### 2. 训练数据策略的范式转变

OmniNav 的另一关键差异在于训练数据组成。现有基线方法通常仅使用特定任务的导航数据进行训练。OmniNav 则采用两阶段联合训练策略，将**大规模通用视觉-语言数据**（图像描述、指称/定位、具身问答等）与多种导航任务统一训练。消融实验（Table 4）揭示了这一策略的因果机制：

- 去除具身问答数据或指称/定位数据，导致小物体（如 picture、flowerpot）识别性能下降；
- 去除通用 MLLM 数据，导致不规则物体（如 handrail、stair）识别失败。

这表明通用视觉-语言数据为模型提供了丰富的语义先验，实质性地增强了开放词汇物体感知的鲁棒性。此外，数据丰富度还改变了模型规模的边际收益：无额外数据时，7B 模型（SR 57.2）明显优于 3B（55.9）；加入额外数据后，3B 与 7B 性能接近（57.7 vs 57.9），说明数据充足时模型规模并非瓶颈（Table 5）。

### 3. 适用边界与证据强度

OmniNav 的强证据边界覆盖以下场景：

- **指令目标导航**：在 R2R-CE 和 RxR-CE Val-Unseen 上，仅使用纯 RGB 输入即实现 SOTA 成功率，分别超越前最优方法 CorrectNav 4.4% 和 4.3%（Table 1）。比较公平性良好，所有方法均未使用深度、全景或里程计。
- **物体目标导航**：在 HM3D-OVON 上，OmniNav*（含慢系统与思维链）超越最强基线 MTU3D 达 18.4%（SR 59.2 vs 40.8, Table 2）。需注意，OmniNav* 使用了深度/里程计信息构建占据地图，而部分对比方法仅使用 RGB，表格中已明确标注，保持了比较透明性。
- **真实机器人部署**：在四足机器人上实现了零样本迁移，验证了工程可行性（Figure 4），但慢系统的完整物理部署尚未实现。

### 4. 局限与开放问题

**当前局限**：

1. **慢系统的物理部署**：慢系统的思维链推理和边界选择涉及较大计算开销，如何在真实环境中同时满足其计算延迟与 5 Hz 高频控制需求，尚未进行系统级的延迟-频率权衡分析。
2. **复杂纹理物体的识别**：无论模型规模大小（3B 或 7B），对衣物、镜子等纹理复杂物体的识别仍不稳定，表明视觉编码能力存在上限。
3. **缩放规律未明**：数据组成、数据质量和模型规模之间的联合缩放关系缺乏系统化研究，当前仅观察到数据丰富时模型规模边际收益递减的初步趋势。

**开放问题**：

1. 如何在真实环境中实现慢系统的高效推理，同时保持快系统的低延迟控制？可能的路径包括模型蒸馏、异步推理或选择性激活慢系统。
2. 针对纹理复杂物体的识别鲁棒性，是否需要引入更强的视觉编码器或专门的对比学习预训练？
3. 数据组成（导航数据 vs 通用视觉-语言数据）的最优配比、数据质量过滤策略与模型规模之间的三维缩放关系，需要更系统的实验设计来揭示。

## 原文 PDF

![[paperPDFs/ICLR_2026/OmniNav_A_Unified_Framework_for_Prospective_Exploration_and_Visual_Language_Navigation.pdf]]
