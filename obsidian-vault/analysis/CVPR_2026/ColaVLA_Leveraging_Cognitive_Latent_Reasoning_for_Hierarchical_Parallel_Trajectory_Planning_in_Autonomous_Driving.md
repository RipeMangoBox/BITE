---
title: "ColaVLA: Leveraging Cognitive Latent Reasoning for Hierarchical Parallel Trajectory Planning in Autonomous Driving"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/ColaVLA_Leveraging_Cognitive_Latent_Reasoning_for_Hierarchical_Parallel_Trajectory_Planning_in_Autonomous_Driving.pdf
project_link: null
code_link: "https://github.com/pqh22/ColaVLA"
aliases:
- ColaVLA
tags:
- CVPR_2026
- topic/generative_models_diffusion
- topic/generative_models_diffusion/diffusion_image_video
core_operator: 将推理完全迁移到统一潜在空间，通过认知潜在推理器以两次前向传递提取紧凑的元动作表示，并配合因果保持分层并行规划器，消除文本自回归解码，实现高效、安全、因果一致的轨迹生成。
primary_logic: VLM的泛化性和推理能力可以通过潜在空间推理进行传递，无需依赖文本链式思考。通过自车自适应令牌选择和元动作压缩，将场景理解浓缩为决策导向的潜在先验，再通过具有因果保持注意力机制的分层并行解码器，在一次前向传播中生成多尺度精细轨迹，实现了推理速度与决策可靠性的双重提升。
claims:
- 在nuScenes开环评测中，ColaVLA在动作型方法中达到最低平均L2误差0.30m和最低平均碰撞率0.23%，较之前最优动作基线SOLVE-E2E分别降低3%和23%。
- 在NeuroNCAP闭环基准上，ColaVLA取得3.48的NeuroNCAP分数，比最强文本型VLM模型ImpromptuVLA（2.06）绝对提升1.42，并大幅降低碰撞率。
- 推理延迟方面，ColaVLA仅需727ms，比同等条件下的OmniDrive（3727ms）和SOLVE-VLM（3719ms）快5倍以上，证实潜在推理和并行解码的效率优势。
- 消融实验表明，认知潜在推理和反思阶段对降低L2误差至关重要，分层并行规划器在闭环安全性上显著超越MLP和扩散规划器。
---

# ColaVLA: Leveraging Cognitive Latent Reasoning for Hierarchical Parallel Trajectory Planning in Autonomous Driving

> [!tip] 核心洞察
> VLM的泛化性和推理能力可以通过潜在空间推理进行传递，无需依赖文本链式思考。通过自车自适应令牌选择和元动作压缩，将场景理解浓缩为决策导向的潜在先验，再通过具有因果保持注意力机制的分层并行解码器，在一次前向传播中生成多尺度精细轨迹，实现了推理速度与决策可靠性的双重提升。

| 字段 | 内容 |
|------|------|
| 中文题名 | ColaVLA: 利用认知潜在推理实现自动驾驶中的分层并行轨迹规划 |
| 英文题名 | ColaVLA: Leveraging Cognitive Latent Reasoning for Hierarchical Parallel Trajectory Planning in Autonomous Driving |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2512.22939) · [Code](https://github.com/pqh22/ColaVLA) |
| Topic | #topic/generative_models_diffusion #topic/generative_models_diffusion/diffusion_image_video |
| Method | ColaVLA |
| Dataset | nuScenes open-loop, NeuroNCAP closed-loop, Inference Latency |

> [!tip] 效果简介
> - nuScenes open-loop 上，Avg L2 (m) / Avg Col (%) 0.30 / 0.23 vs SOLVE-E2E 0.31 / 0.30 (L2 -3%, Col -23%)。
> - NeuroNCAP closed-loop 上，NeuroNCAP Score 3.48 vs ImpromptuVLA 2.06 (+68.9%)。
> - Inference Latency 上，Latency (ms) 727 vs OmniDrive 3727 (-80.5%)。

## 概述

自动驾驶中的视觉-语言-动作（VLA）模型，通过引入视觉语言模型（VLM）的推理能力，在复杂场景理解与决策方面展现了巨大潜力。然而，当前基于文本的VLM规划器普遍面临三个核心瓶颈：**离散文本与连续控制之间的模态不匹配**、**自回归思维链解码导致的高延迟与误差累积**，以及**规划器因果结构的缺失**，使得生成的轨迹在安全性和一致性上难以保证。

针对上述挑战，ColaVLA提出了一种全新的推理范式：**将认知推理完全迁移到统一潜在空间中执行**。该方法不再依赖文本链式思考，而是通过一个认知潜在推理器（Cognitive Latent Reasoner），以仅两次VLM前向传递完成场景理解与元动作决策，将驾驶场景证据压缩为紧凑的决策导向潜在先验。随后，一个因果保持的分层并行规划器（Hierarchical Parallel Planner）在单次前向传播中，将这些先验解码为多尺度、多模态的精细轨迹，从根本上消除了文本自回归解码带来的延迟与误差累积问题。

在nuScenes开环评测中，ColaVLA以**平均L2误差0.30m**和**平均碰撞率0.23%** 的成绩，在动作型方法中达到最优，较此前最佳基线SOLVE-E2E分别降低3%和23%。在NeuroNCAP闭环基准上，ColaVLA取得了**3.48的NeuroNCAP分数**，比最强文本型VLM模型ImpromptuVLA（2.06）绝对提升1.42，相对提升68.9%，同时大幅降低了碰撞率。在推理效率方面，ColaVLA仅需**727ms**的端到端延迟，比同等条件下的OmniDrive（3727ms）和SOLVE-VLM（3719ms）快5倍以上，充分验证了潜在推理与并行解码的效率优势。消融实验进一步表明，认知潜在推理和反思阶段对规划精度至关重要，而分层并行规划器在闭环安全性上显著超越了MLP和扩散规划器。

## 背景与动机

### 自动驾驶规划中的VLM范式与瓶颈

视觉语言模型（VLM）凭借其强大的场景理解和常识推理能力，正被迅速引入自动驾驶轨迹规划领域。当前主流方案采用**文本链式思维（Chain-of-Thought, CoT）推理**：VLM自回归地生成中间文本描述（如场景分析、意图预测、风险评估），再将文本解码为最终的轨迹或控制指令。这一范式虽然利用了VLM的泛化性，却引入三个相互纠缠的核心瓶颈：

1. **模态不匹配**：离散文本与连续控制之间存在天然的语义鸿沟。将驾驶决策压缩为文本描述再还原为连续轨迹，不可避免造成信息损失与控制精度下降。
2. **高延迟与误差累积**：自回归解码逐词生成长文本链，推理延迟随序列长度线性增长；同时，文本解码中的单步错误会沿链传播，导致规划质量退化。
3. **因果结构缺失**：现有规划器缺乏对轨迹时序因果性的显式建模，生成的轨迹可能在运动学上不一致，在安全关键场景下产生不安全行为。

这些瓶颈在典型文本型VLM规划器中表现突出。例如，**DriveVLM**（Tian et al., CoRL 2024）和**OmniDrive**（Wang et al., CVPR 2025）依赖自回归文本推理，推理延迟高达3700ms以上；**SOLVE-VLM**（Shi et al., NeurIPS 2025）同样面临文本解码的效率与精度权衡。尽管**ImpromptuVLA**（Xu et al., NeurIPS 2025）在闭环评测中有所进步，但其NeuroNCAP分数仅为2.06，且使用了额外整理的安全关键数据，通用性受限。

### 潜在推理的动机与核心洞察

本文的核心洞察是：**VLM的泛化性和推理能力可以通过潜在空间推理进行传递，无需依赖文本链式思考**。具体而言，将认知推理过程从文本空间迁移到统一的潜在空间，可以同时解决模态不匹配、高延迟和因果缺失三大瓶颈：

- **在潜在空间中推理**，避免了文本编码-解码的信息损失，使推理结果直接作为规划器的连续先验。
- **用两次VLM前向传递替代自回归解码**，将推理延迟从秒级压缩至毫秒级，同时消除误差累积。
- **引入因果保持的分层并行解码**，在单次前向传播中生成多尺度精细轨迹，确保时序一致性。

基于这一洞察，ColaVLA提出**认知潜在推理器（Cognitive Latent Reasoner）**与**分层并行规划器（Hierarchical Parallel Planner）**的协同架构。推理器通过自车自适应令牌选择和元动作压缩，将场景理解浓缩为决策导向的潜在先验；规划器则在因果保持混合注意力掩码的约束下，并行解码多尺度轨迹，实现推理速度与决策可靠性的双重提升。

### 与既有方法的根本差异

与基于文本的VLM规划器相比，ColaVLA在三个关键维度上实现了范式转变，如Figure 1所示：

| 维度 | 文本型VLM规划器 | ColaVLA |
|------|----------------|---------|
| 推理空间 | 文本空间，自回归CoT | 统一潜在空间，两次前向传递 |
| 信息提取 | 全量视觉令牌或简单池化 | 自车自适应FiLM调制 + Top-K关键令牌选择 |
| 轨迹解码 | 自回归顺序解码或MLP头 | 因果保持分层并行解码 |

与基于动作的端到端规划器（如**UniAD**（Hu et al., CVPR 2023）、**VAD**（Jiang et al., ICCV 2023）、**SOLVE-E2E**（Shi et al., NeurIPS 2025））相比，ColaVLA保留了VLM的推理能力，但将其压缩为潜在表示而非显式文本，从而在保持可解释性的同时获得更高的规划精度和安全性——在nuScenes开环评测中，ColaVLA的平均L2误差降至0.30m，平均碰撞率降至0.23%，均优于此前最优的动作基线。

## 核心创新

ColaVLA 的核心创新在于将自动驾驶规划中的认知推理从**文本空间彻底迁移到统一潜在空间**，并通过**认知潜在推理器**与**分层并行规划器**的协同设计，系统性地解决了当前 VLM 规划器面临的三大瓶颈：模态不匹配、推理延迟与误差累积、以及因果结构缺失。

### 推理范式的根本转变：从文本思维链到潜在空间推理

现有基于文本的 VLM 规划器（如 **DriveVLM** (Tian et al., CoRL 2024)、**OmniDrive** (Wang et al., CVPR 2025)、**ImpromptuVLA** (Xu et al., NeurIPS 2025)）普遍采用文本思维链进行自回归推理，将场景理解、决策、规划等子任务串行输出为离散文本。这一范式存在两个根本缺陷：其一，**离散文本与连续控制之间的模态鸿沟**导致信息损失和语义错位；其二，**自回归解码的串行特性**引发高昂的计算延迟和严重的误差累积。

ColaVLA 的核心洞察在于：VLM 的泛化能力与推理能力可以通过潜在空间进行传递，无需依赖文本链式思考。具体而言，ColaVLA 引入**认知潜在推理**（Cognitive Latent Reasoning），将场景理解、关键实体识别、反思与决策四个认知阶段全部压缩在统一的潜在空间中完成，仅需**两次 VLM 前向传递**即可输出紧凑的元动作决策。这一设计将推理过程从“逐词生成文本再解析为控制”的迂回路径，转变为“直接产出决策导向的潜在先验”的端到端流程，从根本上消除了文本自回归解码带来的延迟与误差累积。

### 关键信息提取：自车自适应令牌选择

传统 VLM 规划器通常使用全量视觉令牌进行推理，缺乏对安全关键信息的主动筛选。ColaVLA 提出**自车自适应路由器**（Ego-Adaptive Router），通过两个步骤实现关键信息的精准提取：

1. **FiLM 条件调制**：以自车状态令牌 $\mathbf{E}$ 为条件，对视觉令牌 $\mathbf{Q}_V$ 进行逐通道的缩放与偏移，使视觉表征与当前驾驶状态对齐：
   $$\tilde{\mathbf{Q}}_V = \big(1 + \gamma_{Re}(\mathbf{E})\big) \odot \mathbf{Q}_V + \beta_{Re}(\mathbf{E})$$

2. **Top-K 关键令牌选择**：路由器 $\mathcal{H}_\phi$ 评估调制后的视觉令牌重要性，仅保留 $K$ 个最具安全关键性的令牌：
   $$\mathbf{Q}^* = \mathrm{TopK}\big(\tilde{\mathbf{Q}}_V, \mathbf{w}, K\big), \quad \mathbf{w} = \mathcal{H}_\phi\big(\tilde{\mathbf{Q}}_V\big)$$

这一机制实现了从“全量感知”到“决策导向感知”的转变，为后续推理提供了高信息密度、低冗余度的场景表征。

### 轨迹规划的解码策略：因果保持分层并行解码

传统规划器通常采用自回归顺序解码或简单的 MLP/扩散解码头，前者效率低下，后者缺乏对轨迹时序结构的显式建模。ColaVLA 提出**分层并行规划器**（Hierarchical Parallel Planner），其创新体现在三个层面：

**多尺度并行生成**：规划器从元动作库检索嵌入后，将其扩展并重采样为从粗到细的 $S$ 个嵌套尺度，通过**单次前向传递**并行解码所有尺度的轨迹。这与自回归的逐点生成形成鲜明对比，大幅提升了推理效率。

**因果保持混合注意力**：为确保多尺度轨迹的时序一致性，ColaVLA 设计了专门的注意力掩码：
$$\mathcal{M}(i,j) = \left\{ \begin{array}{ll} 0, & j \leq L_c, \\ 0, & i \geq L_c \text{ and } \mathbf{X}[j] \in \mathbb{Z}_{s-1} \cup \mathbb{Z}_s, \\ -\infty, & \text{otherwise}. \end{array} \right.$$

该掩码允许所有尺度的令牌关注裁剪后的上下文（$\mathbf{Q}^*$），同时强制相邻尺度间的时序因果性——每个尺度只能关注自身和上一尺度的令牌，而不能窥视未来尺度。这一设计将驾驶运动的因果结构显式编码到注意力机制中，从根本上保证了多尺度轨迹的物理一致性与安全性。

**Interpolate 回归策略**：与单尺度、顺序或逆序策略不同，ColaVLA 采用先预测关键端点再填充中间点的 Interpolate 策略，使回归过程与驾驶运动的因果结构天然对齐——远端点决定整体意图，近端点受远端约束并细化局部路径。

### 推理效率的结构性突破

上述创新的综合效果是推理效率的质变。在相同硬件条件（NVIDIA H20，无 Flash-Attention）下，ColaVLA 的端到端推理延迟仅为 727ms，比 **OmniDrive**（3727ms）和 **SOLVE-VLM**（3719ms）**快 5 倍以上**。这一效率提升源于两个结构性因素：潜在推理消除了文本自回归解码的串行瓶颈；分层并行解码将多尺度轨迹生成压缩到单次前向传递中完成。

## 整体框架

ColaVLA 将视觉-语言-动作（VLA）规划重新定义为一个**潜在空间认知推理 + 因果保持分层并行解码**的统一流程。其核心设计动机在于消除传统文本型 VLM 规划器中的模态不匹配、自回归延迟与误差累积，同时保留 VLM 的泛化与推理能力。

### 框架总览

如图 2 所示，ColaVLA 的整体 pipeline 由两条协同分支构成：

1. **认知潜在推理分支（左侧）**：接收多视图图像序列，经图像骨干网络和 SQ-Former 感知前端处理后，输出视觉令牌。该分支通过四个阶段——**场景理解（Understand）、关键实体识别（Recognize）、潜在反思（Rethink）与策略决策（Decide）**——在统一潜在空间中完成隐式推理，最终产出一个紧凑的元动作决策。

2. **分层并行规划分支（右侧）**：根据选定的元动作，从动作库中检索对应的元动作嵌入，经时间扩展与重采样后形成多尺度轨迹查询。这些查询与裁剪后的关键上下文令牌一同输入**分层并行规划器**，在因果保持混合注意力掩码的约束下，单次前向传播即可并行解码出多尺度、多模态的连续轨迹。

### 输入输出流

整个系统的信息流动可形式化为：

$$
\mathbf{Z}_t = \mathcal{R}_\theta\big(\mathbf{S}_t\big) \qquad \widehat{\mathbf{Y}}_t = \mathcal{P}_\phi(\mathbf{Z}_t, \mathbf{A})
$$

- **输入** $\mathbf{S}_t$：多视图环视图像序列。
- **推理器** $\mathcal{R}_\theta$：将传感器输入压缩为决策导向的潜在表示 $\mathbf{Z}_t$，仅需**两次 VLM 前向传递**。
- **规划器** $\mathcal{P}_\phi$：结合动作库 $\mathbf{A}$ 中的元动作嵌入，将潜在表示解码为预测轨迹 $\widehat{\mathbf{Y}}_t$，在**单次前向传播**中完成。

### 关键模块关系

| 模块 | 功能 | 与上下游的连接 |
|------|------|----------------|
| 多视图图像编码器（EVA-02-L） | 环视图像 → 视觉特征嵌入 | 上游：原始图像；下游：SQ-Former |
| SQ-Former（感知前端） | 多视图视觉推理，输出 3D 检测、车道表示及视觉令牌 | 上游：图像编码器；下游：认知潜在推理器 |
| 认知潜在推理器 | 场景理解 → 自车自适应关键令牌选择 → 潜在反思 → 元动作决策 | 上游：SQ-Former 视觉令牌；下游：分层并行规划器 |
| 元动作库与轨迹查询生成 | 元动作嵌入检索 → 时间扩展 → 多尺度重采样 | 上游：推理器决策；下游：规划器输入序列 |
| 分层并行规划器 | 因果保持混合注意力解码 → 多尺度轨迹回归 → 置信度引导模态选择 | 上游：关键令牌 + 轨迹查询；下游：最终轨迹输出 |
| 感知头（检测/车道解码器） | 从感知令牌解码 3D 目标框与车道线 | 与规划分支共享感知令牌，提供辅助监督 |

### 推理范式对比

与传统文本型 VLM 规划器（如 DriveVLM、OmniDrive）的自回归思维链推理不同，ColaVLA 将推理完全迁移到潜在空间（图 1）。传统方法需要反复解码文本中间表示，导致令牌成本膨胀和误差累积；ColaVLA 通过**两次 VLM 前向传递**完成场景理解与决策，消除了文本自回归解码，推理延迟从同类方法的 3700+ ms 降至 727 ms（5 倍以上加速），同时保留了决策层面的可解释性。

### 补充图表

![[assets/figures/papers/paper_list_l2455_https_arxiv_org_abs_2512_22939/figures/002_Figure_2.jpg]]
*Figure 2: Overview of the ColaVLA framework. Multi-view image sequences are first processed by an image backbone and a Q-Former to perceive 3D objects and vectorized maps, producing visual tokens for subsequent reasoning and planning. On the left, the Cognitive Latent Reasoning module performs implicit reasoning through four stages, i.e. Understand, Recognize, Rethink, and Decide, to derive a driving strategy. On the right, the derived strategy selects corresponding meta-action queries from action bank, which are then transformed to multi-scale targets. These targets, together with the pruned context are fed into a Hierarchical Parallel Planner for one-pass, parallel trajectory decoding. The resultin...*

## 核心模块与公式推导

ColaVLA 的核心架构由两个解耦模块构成：**认知潜在推理器（Cognitive Latent Reasoner）** 和 **分层并行规划器（Hierarchical Parallel Planner）**。前者在统一潜在空间中完成场景理解与决策推理，后者在单次前向传递中并行生成多尺度精细轨迹。以下逐一展开关键模块的数学表述与设计机理。

---

### 3.1 通用轨迹规划框架

ColaVLA 将端到端规划抽象为推理-规划二阶段范式。给定时刻 $t$ 的传感器输入 $\mathbf{S}_t$（多视图图像序列），系统首先通过推理器 $\mathcal{R}_\theta$ 提取紧凑的潜在决策表示 $\mathbf{Z}_t$，随后规划器 $\mathcal{P}_\phi$ 结合预定义的元动作库 $\mathbf{A}$ 生成预测轨迹 $\widehat{\mathbf{Y}}_t$：

$$\mathbf{Z}_t = \mathcal{R}_\theta\big(\mathbf{S}_t\big) \qquad \widehat{\mathbf{Y}}_t = \mathcal{P}_\phi(\mathbf{Z}_t, \mathbf{A})$$

该公式建立了“感知→潜在推理→动作引导规划”的因果链条：推理器 $\mathcal{R}_\theta$ 负责将高维传感器数据压缩为决策导向的潜在先验，规划器 $\mathcal{P}_\phi$ 则负责将抽象决策展开为连续时空轨迹，二者通过元动作库 $\mathbf{A}$ 实现解耦与协同。

---

### 3.2 认知潜在推理器

认知潜在推理器在统一潜在空间中完成四阶段推理：**场景理解 → 关键实体识别 → 潜在反思 → 策略决策**，全程仅需两次 VLM 前向传递，彻底消除了文本自回归解码。

#### 3.2.1 驾驶场景理解

首次前向传递将固定驾驶提示（文本嵌入 $\mathbf{T}$）、多视图视觉嵌入 $\mathbf{V}$ 和自车令牌 $\mathbf{E}$ 拼接后送入 VLM 变换器，输出具有时空因果关系的视觉隐藏状态：

$$\mathbf{Q}_V = \mathcal{D}_\mathrm{VLM}\big([\mathbf{T}; \mathbf{V}; \mathbf{E}]\big)$$

其中 $\mathcal{D}_\mathrm{VLM}$ 表示视觉-语言模型的解码器前向过程，输出 $\mathbf{Q}_V$ 编码了全局空间语义和时序上下文，为后续的关键实体识别提供信息基础。

#### 3.2.2 自车自适应关键实体识别

为从海量视觉令牌中筛选安全关键信息，ColaVLA 引入**自车自适应路由器**。首先通过 FiLM（Feature-wise Linear Modulation）机制，利用自车令牌 $\mathbf{E}$ 生成逐通道的缩放因子 $\gamma_{Re}(\mathbf{E})$ 和偏移量 $\beta_{Re}(\mathbf{E})$，对视觉令牌进行条件调制：

$$\tilde{\mathbf{Q}}_V = \big(1 + \gamma_{Re}(\mathbf{E})\big) \odot \mathbf{Q}_V + \beta_{Re}(\mathbf{E})$$

该操作使视觉表征与瞬时车辆状态（位置、朝向、速度）对齐，增强对自车运动相关的场景元素的敏感性。随后，路由器 $\mathcal{H}_\phi$ 对调制后的令牌进行重要性评分，并通过 Top-K 选择保留 $K$ 个最关键令牌：

$$\mathbf{w} = \mathcal{H}_\phi\big(\tilde{\mathbf{Q}}_V\big), \quad \mathbf{Q}^* = \mathrm{TopK}\big(\tilde{\mathbf{Q}}_V, \mathbf{w}, K\big)$$

其中 $\mathbf{w}$ 为逐令牌的重要性权重，$\mathbf{Q}^*$ 为筛选后的关键视觉令牌集合。消融实验证实 $K=256$ 在精度与效率间取得最优平衡（平均 L2 误差 30.4 cm），令牌过少则信息不足，过多则引入冗余。

#### 3.2.3 潜在反思与策略决策

第二次前向传递将裁剪后的关键令牌 $\mathbf{Q}^*$、驾驶提示 $\mathbf{T}$、自车令牌 $\mathbf{E}$ 以及可学习的元查询嵌入 $\mathbf{M}$ 重新输入 VLM，产生更新后的元策略表示：

$$\mathbf{Q}_M = \mathcal{D}_\mathrm{VLM}\big([\mathbf{T}; \mathbf{Q}^*; \mathbf{E}; \mathbf{M}]\big)$$

元查询嵌入 $\mathbf{M}$ 同样经过 FiLM 调制以适应自车状态，并通过交叉注意力与关键视觉令牌 $\mathbf{Q}^*$ 交互，随后经自注意力提炼全局决策信息。最终，一个共享的两层 MLP 将每个精炼后的元令牌映射为元动作 logit，使用 focal loss 训练以强调困难样本和安全关键场景。消融实验表明，引入潜在推理使平均 L2 误差从 31.4 cm 降至 30.4 cm，进一步增加反思阶段可继续降低误差，验证了压缩信息的重新评估对决策质量的增益。

---

### 3.3 分层并行规划器

分层并行规划器接收认知推理器输出的元动作决策，从动作库检索对应嵌入，扩展时间嵌入并重采样为 $S$ 个由粗到精的嵌套尺度，随后通过**因果保持混合注意力**在单次前向传递中并行解码多尺度轨迹。

#### 3.3.1 多尺度输入流构建

将裁剪上下文 $\mathbf{Q}^*$（$K$ 个令牌）与 $S$ 个尺度的轨迹查询 $\mathbf{F}_1, \ldots, \mathbf{F}_S$ 拼接为统一输入序列：

$$\mathbf{X} = \big[\mathbf{Q}^*; \mathbf{F}_1; \ldots; \mathbf{F}_S\big] \in \mathbb{R}^{L \times D}, \quad L = K + \sum_{s=1}^{S}|\mathcal{Z}_s|$$

其中 $\mathcal{Z}_s$ 表示第 $s$ 个尺度的轨迹点索引集合，$D$ 为隐藏维度。该拼接使规划器能同时访问场景上下文和所有尺度的查询，为并行解码奠定结构基础。

#### 3.3.2 因果保持混合注意力掩码

并行解码的核心挑战在于保证时序因果性——粗尺度端点应先于细尺度中间点被确定。ColaVLA 设计了**因果保持混合注意力掩码** $\mathcal{M}(i,j)$：

$$\mathcal{M}(i,j) = \left\{ \begin{array}{ll} 0, & j \leq L_c, \\[4pt] 0, & i \geq L_c \ \mathrm{and}\ \mathbf{X}[j] \in \mathbb{Z}_{s-1} \cup \mathbb{Z}_s, \\[4pt] -\infty, & \mathrm{otherwise}. \end{array} \right.$$

其中 $L_c = K$ 为上下文令牌的截止位置。该掩码的语义如下：
- **规则一**：所有令牌（包括各尺度轨迹查询）均可无限制地关注裁剪上下文 $\mathbf{Q}^*$，确保场景信息充分流动；
- **规则二**：第 $s$ 尺度的令牌仅能关注上一尺度 $\mathbb{Z}_{s-1}$ 和自身尺度 $\mathbb{Z}_s$，形成相邻尺度间的因果依赖链；
- **规则三**：屏蔽对未来尺度 $\mathbb{Z}_{s+1}$ 及更远尺度的注意力（赋 $-\infty$），强制粗尺度先于细尺度被“确定”。

这种设计在保持上下文全交互的同时，严格维护了驾驶运动的物理因果结构：先确定远端关键端点，再逐步填充中间路径点。消融实验证实，该 Interpolate 多尺度回归策略（先预测端点再插值中间点）优于单尺度、顺序或逆序策略，与驾驶运动的因果结构天然对齐。

#### 3.3.3 置信度引导并行解码

对于每个元动作假设，两个轻量级 MLP 头独立工作：一个估计置信度分数，另一个回归对应的多尺度轨迹。训练时，基于各预测轨迹与真值轨迹的距离分配 one-hot 监督信号，仅最接近真值的假设接收直接回归监督。推理时，选择置信度最高的轨迹作为最终输出，实现多模态预测与确定性决策的平衡。

---

### 3.4 模块协同与效率分析

认知潜在推理器与分层并行规划器的协同体现在“压缩-展开”的信息流：推理器将丰富但冗余的视觉信息压缩为紧凑的元动作决策（仅需两次 VLM 前向传递），规划器将抽象决策高效展开为多尺度连续轨迹（单次并行解码）。这一设计使 ColaVLA 的端到端推理延迟仅为 727 ms，比同等条件下的 OmniDrive（3727 ms）和 SOLVE-VLM（3719 ms）快 5 倍以上，同时保持了决策层面的可解释性——元动作的选择为下游规划提供了明确的语义锚点。

### 补充图表

![[assets/figures/papers/paper_list_l2455_https_arxiv_org_abs_2512_22939/figures/001_Figure_1.jpg]]
*Figure 1: Illustration of inference paradigms. (a) Previous driving VLMs use text-based chain-of-thought, autoregressively emitting intermediate texts for sub-tasks; repeated decoding increases token cost and error compounding, causing high latency. (b) Our model performs latent reasoning in a VLA space with three forward passes, i.e. scene understanding, latent rethink, and parallel action decoding, removing autoregressive text and cutting inference latency while preserving decision-level interpretability*

![[assets/figures/papers/paper_list_l2455_https_arxiv_org_abs_2512_22939/figures/003_Figure_3.jpg]]
*Figure 3: Causality-Preserving Hybrid Mask. Our mask is designed for the multi-scale targets within our planner. It enables information flow from the pruned context to all temporal scales, while maintaining temporal causality between adjacent scales*

## 实验与分析

### 开环规划性能

ColaVLA在nuScenes开环基准上进行了全面评测，结果如Table 1所示。在基于动作的规划方法中，ColaVLA取得了最优的综合性能：平均L2误差降至**0.30m**，平均碰撞率降至**0.23%**。相较于此前最优的动作基线**SOLVE-E2E**（Shi et al., NeurIPS 2025），L2误差降低3%，碰撞率降低23%。这一结果表明，认知潜在推理与分层并行规划器的组合在保持高推理效率的同时，显著提升了规划精度与安全性。

值得注意的是，ColaVLA仅使用标准nuScenes训练数据，而部分文本型VLM模型（如ImpromptuVLA）使用了额外整理的安全关键数据。在此约束下，ColaVLA仍展现出对文本型方法的全面超越，验证了潜在空间推理在消除模态不匹配方面的核心优势。

### 闭环仿真性能

在NeuroNCAP闭环安全基准上，ColaVLA建立了新的最优水平，取得**3.48**的NeuroNCAP分数（Table 2）。相比此前最强的文本型VLM模型**ImpromptuVLA**（Xu et al., NeurIPS 2025）的2.06分，绝对提升**+1.42**，相对提升达68.9%。为确保公平比较，闭环评测中所有方法均仅采用Top-1驾驶策略，模拟真实决策场景。

![[assets/figures/papers/paper_list_l2455_https_arxiv_org_abs_2512_22939/figures/005_Table_2.jpg]]
*Table 2: Closed-loop simulation results on NeuroNCAP [31]. † indicates that it utilizes additional training data and is a text-based driving VLM model. ‡ refers to trajectory post-processing. Our proposed method achieves a substantial improvement in the closed-loop evaluation, demonstrating strong adaptability to safety-critical scenarios and highlighting the model’s efficiency and generalization capability. In this evaluation, we adopt only the top-1 driving strategy to better simulate realistic decision-making in closed-loop settings, ensuring fair comparison and faithfully reflecting the model’s safety and robustness in real-world driving situations. Best scores are in bold*

这一大幅提升揭示了ColaVLA的核心因果机制：因果保持混合注意力掩码强制相邻时间尺度间的时序因果性，使得并行解码的轨迹在闭环交互中保持物理一致性，避免了文本自回归解码中常见的误差累积导致的不安全行为。

### 推理效率分析

推理延迟是VLM规划器实际部署的关键瓶颈。在相同硬件条件（单张NVIDIA H20 GPU，无Flash-Attention）下，ColaVLA的端到端推理延迟仅为**727ms**，而文本型方法**OmniDrive**（Wang et al., CVPR 2025）需3727ms，**SOLVE-VLM**需3719ms，ColaVLA实现了超过5倍的推理加速（Table 3）。

![[assets/figures/papers/paper_list_l2455_https_arxiv_org_abs_2512_22939/figures/007_Table_3.jpg]]
*Table 3: Inference latency comparison on a single NVIDIA H20 GPU without flash-attention [12]. We report end-to-end inference latency (ms per frame) under identical batch settings*

效率增益源自两个设计决策：认知潜在推理器仅需两次VLM前向传递即可完成场景理解与元动作决策，消除了文本自回归解码的串行开销；分层并行规划器在单次前向传播中生成多尺度轨迹，避免了顺序解码的延迟累积。

### 消融研究

#### 认知潜在推理的有效性

Table 4展示了认知潜在推理的消融结果。移除潜在推理阶段（无Reasoning变体）导致平均L2误差从30.4cm升至31.4cm，验证了潜在空间推理对规划精度的贡献。在此基础上增加反思（Rethink）阶段，使模型对压缩后的关键信息进行重新评估，进一步降低了平均L2误差。这表明“理解-识别-反思-决策”的四阶段推理流程中，反思机制有助于纠正初步理解中的偏差，提升决策质量。

#### 分层并行规划器的设计选择

在NeuroNCAP闭环任务中，ColaVLA的分层并行规划器取得**1.50**的NeuroNCAP分数，显著优于MLP规划器（1.05）和扩散规划器（1.02），如Table 5所示。MLP规划器缺乏时序结构建模能力，扩散规划器虽能建模多模态分布但缺少因果约束，导致闭环安全性不足。分层并行规划器的因果保持混合注意力掩码是闭环性能提升的关键因素。

Table 7对比了不同多尺度回归策略。ColaVLA采用的Interpolate策略（先预测关键端点再填充中间点）优于单尺度、顺序或逆序策略，这与驾驶运动的因果结构一致——轨迹的端点决定了整体形态，中间点可由此插值推导。

#### 关键令牌数量与上下文选择

Table 6显示，保留**K=256**个关键令牌在精度与效率之间取得最佳平衡（平均L2 30.4cm）。令牌过少导致信息不足，过多则引入冗余并增加计算开销。Table 8进一步表明，使用裁剪后的关键令牌作为规划器上下文（而非全量视觉令牌）可获得更低L2误差，同时减少序列长度和计算成本。这验证了自车自适应路由器在提取安全关键信息方面的有效性。

### 定性分析

Figure 4展示了多尺度轨迹预测的可视化结果，红色、黄色和紫色曲线分别对应从端点预测到全轨迹预测的不同尺度，绿色为真值轨迹。ColaVLA生成的轨迹从粗到细逐步细化，端点预测准确，中间点填充平滑，体现了分层并行解码的因果一致性。

Figure 5展示了NeuroNCAP闭环仿真中三类典型场景的定性对比。ColaVLA始终引导自车远离潜在碰撞，产生更安全、更稳定的运动轨迹，而对比方法在复杂交互场景中容易出现不安全的轨迹偏移。

### 公平性说明

闭环评测中仅使用Top-1驾驶策略，确保公平模拟真实决策场景。对比的文本型模型ImpromptuVLA使用了额外整理的安全关键数据，而ColaVLA仅使用标准nuScenes训练数据。推理延迟比较在相同GPU（NVIDIA H20）和无Flash-Attention条件下进行，保证硬件环境一致。

### 补充图表

![[assets/figures/papers/paper_list_l2455_https_arxiv_org_abs_2512_22939/figures/004_Table_1.jpg]]
*Table 1: Open-loop planning results on the nuScenes benchmark. Methods are grouped into text-based driving models (top) and action-based driving models (bottom). Within action-based approaches, ColaVLA achieves the best overall results, i.e. lowest average L2 and the best collision rates, demonstrating accuracy and safety while retaining high inference efficiency*

![[assets/figures/papers/paper_list_l2455_https_arxiv_org_abs_2512_22939/figures/006_Table_4.jpg]]
*Table 4: Ablation on Latent Reasoning. We evaluate the effect of the reasoning process for latent driving strategy inference and the reflective rethinking of critical cues within the cognitive reasoner*

![[assets/figures/papers/paper_list_l2455_https_arxiv_org_abs_2512_22939/figures/008_Table_5.jpg]]
*Table 5: Ablation on the action-based planner under closed-loop evaluation on NeuroNCAP benchmark. We use deterministic MLP and stochastic diffusion heads to compare against our planner*

![[assets/figures/papers/paper_list_l2455_https_arxiv_org_abs_2512_22939/figures/009_Figure_4.jpg]]
*Figure 4: Qualitative visualization of multi-scale trajectory predictions. Red, yellow, and purple curves denote endpoint-only to full-trajectory predictions, while the green curve is the ground-truth. Right: BEV visualization with ego vehicle, agents, and trajectories*

![[assets/figures/papers/paper_list_l2455_https_arxiv_org_abs_2512_22939/figures/014_Figure_5.jpg]]
*Figure 5: Qualitative closed-loop comparisons in the NeuroNCAP simulator across three representative scenario types. For each case, we visualize the predicted trajectories of ColaVLA and competing planners. ColaVLA consistently guides the ego vehicle away from potential collisions, producing safer and more stable motions*

![[assets/figures/papers/paper_list_l2455_https_arxiv_org_abs_2512_22939/figures/010_Table_6.jpg]]
*Table 6: Ablation on the number of retained critical tokens K*

![[assets/figures/papers/paper_list_l2455_https_arxiv_org_abs_2512_22939/figures/011_Table_7.jpg]]
*Table 7: Ablation on the strategy of hierarchical regression. All variants share the same parallel decoding framework but differ in their specific selection strategy of trajectory subsets across scales*

## 方法谱系与知识库定位

### 1. 问题背景与工作定位

ColaVLA 瞄准的是**端到端自动驾驶中视觉-语言-动作（VLA）规划器**这一新兴范式。该范式的核心矛盾在于：视觉语言模型（VLM）带来了强大的场景理解和常识推理能力，但其原生文本输出模态与连续轨迹控制之间存在根本性鸿沟。

现有方法可大致分为两条技术路线：

**（1）文本型 VLM 规划器**  
以 **DriveVLM**（Tian et al., CoRL 2024）、**OmniDrive**（Wang et al., CVPR 2025）和 **ImpromptuVLA**（Xu et al., NeurIPS 2025）为代表。这类方法将驾驶决策建模为自回归文本生成任务——通过思维链（Chain-of-Thought）逐步推理出场景描述、意图分析和轨迹坐标，再将文本解析为控制信号。其优势在于可解释性强、能利用 VLM 的预训练知识；但存在三个结构性缺陷：
- **模态不匹配**：离散文本无法精确表达连续轨迹的时空约束；
- **高延迟**：自回归逐 token 解码导致推理时间线性增长（OmniDrive 单帧耗时 3727ms，SOLVE-VLM 耗时 3719ms）；
- **误差累积**：文本链式推理中每一步的错误会向后传播，缺乏全局纠错机制。

**（2）动作型端到端规划器**  
以 **UniAD**（Hu et al., CVPR 2023）、**VAD**（Jiang et al., ICCV 2023）和 **SOLVE-E2E**（Shi et al., NeurIPS 2025）为代表。这类方法直接输出连续轨迹，避免了文本转换损耗，推理效率较高。但其规划器通常采用简单的 MLP 或扩散解码头，缺乏 VLM 级别的语义推理能力，在复杂场景下的泛化性和安全性受限。

**ColaVLA 的定位**：在动作型端到端框架中引入 VLM 的推理能力，但**完全避免文本自回归解码**。其核心创新在于将推理过程迁移到统一潜在空间，通过认知潜在推理器（Cognitive Latent Reasoner）以两次前向传递完成场景理解到元动作决策的全过程，再通过因果保持分层并行规划器（Hierarchical Parallel Planner）在单次前向传播中生成多尺度精细轨迹。这一设计使其同时具备文本型方法的推理深度和动作型方法的执行效率。

### 2. 方法谱系中的关键差异

#### 2.1 推理范式：从文本思维链到潜在空间推理

| 维度 | 文本型 VLM 规划器 | ColaVLA |
|------|-------------------|---------|
| 推理空间 | 文本 token 空间 | 统一潜在空间 |
| 推理方式 | 自回归思维链解码 | 两次 VLM 前向传递 |
| 输出形式 | 文本描述 → 解析为轨迹 | 元动作分布 → 直接解码轨迹 |
| 延迟特征 | 随推理步数线性增长 | 固定计算量（约 727ms） |

ColaVLA 的认知潜在推理器包含四个阶段：**场景理解（Understand）→ 关键实体识别（Recognize）→ 潜在反思（Rethink）→ 策略决策（Decide）**。其中关键实体识别阶段引入了自车自适应路由器（Ego-Adaptive Router），通过 FiLM 调制和 Top-K 选择，从大量视觉令牌中保留 K=256 个安全关键令牌。这一机制在保持信息完整性的同时大幅压缩了后续推理的计算量，是连接 VLM 感知与高效规划的桥梁。

#### 2.2 规划解码：从顺序/单尺度到并行多尺度

| 维度 | MLP/扩散规划器 | ColaVLA 分层并行规划器 |
|------|---------------|----------------------|
| 解码方式 | 单次回归或迭代去噪 | 并行多尺度解码 |
| 时序结构 | 无显式因果约束 | 因果保持混合注意力掩码 |
| 轨迹粒度 | 单一尺度 | 粗到细的多尺度轨迹 |
| 模态选择 | 确定性或随机采样 | 置信度引导的 Top-1 选择 |

分层并行规划器的核心设计是**因果保持混合注意力掩码**（Causality-Preserving Hybrid Mask）。该掩码允许所有尺度的轨迹查询关注裁剪后的上下文令牌，同时强制相邻尺度间保持时序因果性——即粗尺度可以关注上下文，细尺度可以关注上下文和上一粗尺度，但不可反向或跨尺度跳跃。这一约束与驾驶运动的物理因果结构一致：先确定大致方向（粗尺度端点），再细化中间路径（细尺度插值点）。

消融实验（Table 5）证实了这一设计的必要性：在 NeuroNCAP 闭环基准上，分层并行规划器取得 1.50 的 NeuroNCAP Score，显著优于 MLP 规划器（1.05）和扩散规划器（1.02）。

#### 2.3 与最相关基线的直接对比

**SOLVE-E2E**（Shi et al., NeurIPS 2025）是动作型方法中此前的最优基线。ColaVLA 在 nuScenes 开环评测中将其平均 L2 误差从 0.31m 降至 0.30m（-3%），平均碰撞率从 0.30% 降至 0.23%（-23%）。增益虽看似不大，但考虑到 SOLVE-E2E 已接近动作型方法的天花板，这一提升主要来自潜在推理引入的语义理解能力。

**ImpromptuVLA**（Xu et al., NeurIPS 2025）是文本型方法中闭环性能最强的模型，但需注意其使用了额外整理的安全关键训练数据。ColaVLA 仅使用标准 nuScenes 训练集，在 NeuroNCAP 闭环基准上取得 3.48 分，较 ImpromptuVLA 的 2.06 分绝对提升 1.42（相对提升 68.9%）。这一差距远超开环评测中的边际提升，说明 ColaVLA 的潜在推理和因果保持规划在安全关键场景中的泛化能力显著优于文本型方法。

### 3. 适用边界与局限

根据论文提供的实验证据和设计选择，ColaVLA 的适用边界可从以下几个维度界定：

**（1）场景复杂度**  
ColaVLA 在 nuScenes（城市道路）和 NeuroNCAP（安全关键场景）上验证了有效性，但论文未报告在极端天气、夜间或非结构化道路上的性能。VLM 的视觉编码器（EVA-02-L）和 SQ-Former 感知前端在这些条件下的鲁棒性需要额外验证。

**（2）元动作库的覆盖范围**  
元动作库（Action Bank）预定义了有限数量的驾驶原语（如左转、右转、直行、换道等）。在需要精细连续操控的场景（如拥堵穿行、窄路会车）中，离散元动作的粒度可能不足。论文未讨论元动作库的扩展机制或开放集场景下的退化行为。

**（3）闭环评测策略**  
论文明确指出闭环评测仅使用 Top-1 驾驶策略，以模拟真实决策。这意味着多模态预测中的其他假设仅用于训练监督，推理时不参与决策。在需要多模态推理的场景（如博弈交互）中，这一简化可能限制模型的上限。

**（4）计算资源需求**  
尽管 ColaVLA 将推理延迟压缩至 727ms（较 OmniDrive 快 5 倍以上），但这仍远高于纯动作型方法（如 VAD 的毫秒级延迟）。在需要极低延迟的实时嵌入式平台上，VLM 前向传递的计算开销仍是瓶颈。

### 4. 开放问题

论文未明确列出局限或开放问题，以下基于方法设计和实验边界推断：

1. **潜在推理的可解释性**：ColaVLA 将推理完全迁移到潜在空间，虽然保留了决策级可解释性（元动作选择），但丢失了文本型方法中逐步骤的语义可追溯性。如何在潜在推理中嵌入可解释性机制（如概念瓶颈）是一个开放方向。

2. **元动作库的在线适应**：当前元动作库是静态预定义的。在长尾场景或新地理区域中，是否需要以及如何在线扩展元动作空间，论文未涉及。

3. **多模态融合的进一步压缩**：自车自适应路由器将视觉令牌从全量压缩至 K=256 个，消融实验表明这是精度-效率的最佳平衡点。但该压缩是否丢失了细粒度几何信息（如精确距离、相对速度），以及能否通过结构化先验进一步降低 K 值，值得探索。

4. **与端到端感知的深度耦合**：ColaVLA 的感知前端（SQ-Former）和规划器是分阶段训练的。感知误差如何传播到潜在推理和规划决策，以及联合端到端优化能否进一步提升安全性，论文未给出答案。

5. **更大规模 VLM 的 scaling 行为**：论文使用 EVA-02-L 作为 VLM 骨干。随着更大规模 VLM（如 InternVL-76B）的出现，潜在推理的质量和延迟如何随模型规模变化，是一个有意义的 scaling 研究问题。

## 原文 PDF

![[paperPDFs/CVPR_2026/ColaVLA_Leveraging_Cognitive_Latent_Reasoning_for_Hierarchical_Parallel_Trajectory_Planning_in_Autonomous_Driving.pdf]]
