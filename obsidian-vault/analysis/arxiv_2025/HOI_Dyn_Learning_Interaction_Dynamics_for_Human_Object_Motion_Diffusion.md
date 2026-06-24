---
title: HOI Dyn Learning Interaction Dynamics for Human Object Motion Diffusion
type: paper
paper_level: A
venue: arXiv
year: 2025
pdf_ref: paperPDFs/arxiv_2025/HOI_Dyn_Learning_Interaction_Dynamics_for_Human_Object_Motion_Diffusion.pdf
aliases:
- HDLIDHOMD
tags:
- arxiv_2025
- topic/vision_multimodal_applications
- topic/generative_models_diffusion
- topic/generative_models_diffusion/diffusion_image_video
core_operator: HOI
primary_logic: HOI
claims:
- HOI
---

# HOI Dyn Learning Interaction Dynamics for Human Object Motion Diffusion

> [!tip] 核心洞察
> HOI

| 字段 | 内容 |
|------|------|
| 中文题名 | HOI Dyn Learning Interaction Dynamics for Human Object Motion Diffusion |
| 英文题名 | HOI Dyn Learning Interaction Dynamics for Human Object Motion Diffusion |
| 会议/期刊 | arXiv 2025 |
| Links | [Project](https://wulin97.github.io/hoi-dyn) · [arXiv](https://arxiv.org/abs/1412.6980) · [Code](https://github.com/AIR-Lan/HOI-Dyn) · [paper](https://arxiv.org/abs/2507.01737) |
| Topic | #topic/vision_multimodal_applications #topic/generative_models_diffusion #topic/generative_models_diffusion/diffusion_image_video |
| Method |  |
| Dataset |  |

## 概述

**问题与瓶颈**  
人-物交互（HOI）生成的核心难点在于，现有方法将人与物的运动视为耦合的黑箱，缺乏对交互过程中**因果时序**与**物理响应**的显式建模。这导致生成结果中物体运动常与人体动作脱节——例如物体在人手尚未接触时就提前移动，或交互结束后缺乏连贯的物理反馈。

**核心洞察**  
HOI-Dyn 将 HOI 生成重新形式化为**“驱动者-响应者”系统**：人体动作作为驱动者，物体则根据交互状态产生相应的动态响应。基于这一视角，论文提出一个轻量级的 Transformer 交互动力学模型，显式预测物体如何对人体运动做出反应，从而将物理因果性注入生成过程。

**方法定位**  
该方法并非替代现有运动扩散模型，而是以**即插即用**的方式扩展标准 HOI 训练目标。框架包含两个关键组件：运动扩散模块负责生成人体运动与物体初始状态，交互动力学模块则以人体运动变化为输入，预测物体相对运动的刚体变换（旋转与平移），并通过 SVD 投影保证旋转矩阵的有效性。训练时引入物体动力学损失与物体重建损失，与原有扩散损失联合优化。

**主要结果**  
在 FullBodyManipulation 基准上，HOI-Dyn 在物体平移误差 **Te** 指标上达到 **5.58 cm**，相比基线方法 CHOIS 的 6.16 cm 降低了 **0.58 cm**（Table 1）。定性分析显示，HOI-Dyn 生成的物体运动具有更合理的因果时序——物体仅在人手接触后才产生响应，且交互结束后保持连贯的物理状态，而 CHOIS 常出现物体提前运动或运动不稳定的现象。消融实验进一步验证了耦合式动力学建模、多步预测损失以及引导策略对性能的贡献。

## 背景与动机

人-物交互（Human-Object Interaction, HOI）生成是计算机视觉与图形学中的核心问题，其目标是根据场景上下文合成自然、物理合理的人体与物体协同运动。该任务在具身智能、虚拟角色动画、AR/VR 等领域具有广泛的应用前景。然而，现有方法面临一个关键瓶颈：**物体运动与人体动作之间的因果时序关系难以建模**。

当前主流的 HOI 生成方法——如 **CHOIS**——通常将人体与物体的运动联合建模为一个统一的生成过程。这种“同步生成”范式虽然在条件匹配指标上表现尚可，但在物理合理性方面存在显著缺陷。如 Figure 2 的定性对比所示，CHOIS 生成的物体运动往往缺乏因果时序：物体在人体尚未接触之前即开始移动，呈现出“过早响应”的伪影，破坏了交互的物理可信度。

这一缺陷的根源在于，现有方法未能显式建模人体动作与物体响应之间的**驱动-响应（driver-responder）关系**。在真实物理世界中，人体作为交互的主动方，其动作（如推、拉、抓取）是物体运动的原因；物体则作为被动响应方，其运动状态变化应当滞后于人体的驱动力施加。忽视这一因果结构，导致生成结果在序列级一致性上表现不佳——物体运动要么与人体动作脱节，要么在时间上错位。

HOI-Dyn 正是针对上述缺口而提出。其核心动机可概括为两点：

1. **重构 HOI 生成的因果框架**：将交互建模为驱动-响应系统，其中人体动作作为“驱动信号”，物体运动作为“响应输出”。这一范式转变使得模型能够显式学习交互中的因果时序，而非将人体与物体的运动视为无差别的联合分布。

2. **以轻量化交互动力学模型弥补物理合理性短板**：在条件运动扩散模型的基础上，引入一个仅 0.5M 参数的 Transformer 交互动力学模块，专门负责预测物体如何对人体动作做出响应。该模块通过学习人体运动增量到物体运动增量的映射，强制物体运动在时序上受人体动作的因果约束。

通过上述设计，HOI-Dyn 在保持扩散模型生成多样性与条件匹配能力的同时，显著提升了交互的物理合理性与序列级连贯性。

## 核心创新

HOI-Dyn 的核心创新在于将人-物交互生成重新概念化为 **Driver-Responder 系统**，并引入一个轻量级的**交互动力学模型**来显式建模物体对人物运动的因果响应机制，从而突破了现有方法（如 CHOIS）在物理时序合理性上的瓶颈。

### 1. Driver-Responder 系统建模

现有方法通常将人物运动与物体运动作为并行生成的联合分布来处理，缺乏对二者因果时序关系的显式约束。HOI-Dyn 从根本上改变了这一范式：将人物建模为 **Driver**，物体建模为 **Responder**。人物运动由其内部动力学 $F_h$ 驱动，而物体运动则由人物运动产生的外部控制信号 $u^{(t)}$ 决定，该信号基于物体当前状态与期望交互状态之间的误差反馈计算。这一形式化在方法论层面（Section 3.1）建立了交互的因果链条，使得物体运动不再是统计关联的产物，而是人物动作的物理响应。

### 2. 交互动力学模型 (Interaction Dynamics Model)

框架的核心组件是一个可学习的交互动力学函数 $\mathscr{D}$，其近似关系为：

$$\Delta o^{(t)} \approx \mathscr{D}(s^{(t)}, o^{(t)}, \Delta h^{(t)}; \theta)$$

该模型以交互上下文 $s^{(t)}$、物体当前状态 $o^{(t)}$ 和人物相对运动 $\Delta h^{(t)}$ 为输入，预测物体的刚体变换（旋转 $\hat{\mathcal{R}}$ 与平移 $\hat{\mathcal{T}}$），并通过 SVD 投影确保输出为合法旋转矩阵。模型设计的关键选择包括：

- **耦合设计 (Coupled Design)**：人物运动与接触信息在统一网络中联合建模，而非采用解耦的双分支结构。消融实验（Table 3）表明，在相近参数量（0.5M）和计算量（0.2 GFLOPs）约束下，耦合设计显著优于解耦变体（Object Point Cloud Loss: 0.462 vs 0.503），验证了交互中人物运动与接触的内在耦合性。
- **多步预测监督**：动力学模型在训练时预测未来 $K$ 步的物体运动，并通过时间步和预测步长的期望损失 $\mathcal{L}_{\mathrm{dyn}}$ 进行监督。实验（Figure 4）表明 $K=2$ 或 $K=3$ 取得最优效果。

### 3. 训练目标的扩展

HOI-Dyn 在标准 HOI 扩散训练目标 $\mathcal{L}_{\mathrm{hoi}}$ 基础上，引入了两项额外监督信号：

- **交互动力学损失 $\mathcal{L}_{\mathrm{dyn}}$**：以 L1 距离度量预测物体关键点与真值之间的误差，按预测步长 $1/k$ 加权。
- **物体重建损失 $\mathcal{L}_{\mathrm{obj}}$**：直接监督物体状态的逐帧重建精度。

这一多目标训练策略使得扩散模型在生成过程中内化了交互的物理动力学约束，而无需在推理时引入额外的物理模拟器。

### 4. 与 CHOIS 的关键差异

相较于基线方法 CHOIS，HOI-Dyn 的 changed slots 主要体现在：

| 维度 | CHOIS | HOI-Dyn |
|------|-------|---------|
| 交互建模 | 隐式联合分布 | 显式 Driver-Responder 因果结构 |
| 物体运动生成 | 条件扩散直接生成 | 扩散生成 + 动力学模型预测刚体变换 |
| 时序因果性 | 缺乏显式约束，出现物体提前运动 | 物体仅在接触后产生物理响应 |
| 额外参数 | — | 0.5M 参数，0.2 GFLOPs |

定性结果（Figure 2）直观展示了这一差异：CHOIS 生成的物体运动缺乏因果时序，在人物接触前即出现偏移；而 HOI-Dyn 生成的物体运动仅在接触后触发，且保持序列级的人-物空间一致性。定量上，HOI-Dyn 在 FullBodyManipulation 数据集上将物体轨迹终点误差 **Te** 从 CHOIS 的 6.16 cm 降至 **5.58 cm**（Table 1），验证了动力学建模对物体运动精度的提升。

### 5. 创新边界与待验证点

- 当前耦合设计在单物体交互场景下验证有效，其在多物体交互场景中的扩展性尚待探索（open question）。
- 动力学模型的轻量化设计（0.5M 参数）虽已证明充分性，但更复杂交互（如可变形物体、流体）是否仍适用需进一步验证。
- 引导策略（guidance）的消融（Table 4）表明即使无引导 HOI-Dyn 也优于 CHOIS，但引导项在不同场景下的泛化效果仍需更多证据支持。

## 整体框架

HOI‑Dyn 将人‑物交互生成建模为一个**驱动‑响应系统**（Driver‑Responder System）：人体动作作为“驱动者”，物体根据人体运动产生符合物理规律的“响应”。整个框架由两个核心模块串联构成：**条件运动扩散**（Conditional Motion Diffusion）与**交互动力学**（Interaction Dynamics），其整体流程如 **Figure 1** 所示。

![[assets/figures/papers/paper_list_l1685_HOI_Dyn_Learning_Interaction_Dynamics_for_Human_Object_Motion_Diffusion/figures/001_Figure_1.jpg]]
*Figure 1: Overview of the proposed HOI-Dyn framework. (a) Conditional Motion Diffusion synthesizes human-object interactions*

### 条件运动扩散模块

该模块以 Transformer 扩散模型为基础，接收场景几何、物体初始状态、文本描述等条件，一次性合成完整的人‑物交互序列 $\hat{\tau}_0 = \{\hat{H}, \hat{O}, \hat{X}\}$，其中 $\hat{H}$ 为人体运动序列，$\hat{O}$ 为物体运动序列，$\hat{X}$ 为接触标签序列。扩散过程的去噪网络在标准 HOI 生成损失 $\mathcal{L}_{\mathrm{hoi}}$ 的基础上训练，负责输出粗粒度的人‑物运动先验。

### 交互动力学模块

交互动力学模块是一个**轻量级 Transformer 模型**（约 0.5M 参数，0.2 GFLOPs），显式预测物体应如何响应人体运动。其输入包括当前帧的人体相对运动 $\Delta h^{(t)}$、物体状态 $o^{(t)}$ 以及接触状态 $s^{(t)}$，输出为物体在未来 $k$ 帧内的相对运动 $\Delta o_{t:t+k}$。该相对运动进一步表示为**刚体变换**（旋转 $\hat{\mathcal{R}}^{(t:t+k)} \in \mathrm{SO}(3)$ 与平移 $\hat{\mathcal{T}}^{(t:t+k)}$），并通过 SVD 投影保证旋转矩阵的有效性。

模块的训练信号来自物体动力学损失 $\mathcal{L}_{\mathrm{dyn}}$ 与物体重建损失 $\mathcal{L}_{\mathrm{obj}}$。前者以 $L_1$ 距离衡量预测与真实物体关键点之间的误差，后者约束单帧物体状态的保真度。最终训练目标为 $\mathcal{L}_{\mathrm{hoi}}$、$\mathcal{L}_{\mathrm{dyn}}$ 与 $\mathcal{L}_{\mathrm{obj}}$ 的加权组合，使扩散模型在生成过程中同时接受交互动力学的监督。

### 输入输出流

1. **输入**：场景点云、物体初始位姿、文本动作描述。
2. **条件运动扩散**：输出粗粒度的人‑物运动序列 $\hat{\tau}_0$。
3. **交互动力学**：以滑动窗口方式遍历生成序列，逐帧预测物体响应，并通过刚体变换更新物体状态。
4. **最终输出**：经过动力学细化的高物理合理性人‑物交互运动序列。

该耦合设计将人体运动、接触状态与物体响应统一建模，相较于解耦策略（如分别建模接触与运动）在相近参数量下实现了更优的交互质量（见 **Table 3**）。

## 核心模块与公式推导

### 3.1 框架总览：驱动-响应系统

HOI-Dyn 将人-物交互生成建模为一个**驱动-响应系统**（Driver-Responder System），其中人体运动作为“驱动者”，物体运动作为“响应者”。整体框架由两个核心组件构成：**运动扩散模型**（Motion Diffusion）和**交互动力学模型**（Interaction Dynamics），如 Figure 1 所示。

运动扩散模型负责生成人-物交互的初始运动序列 $\hat{\tau}_0 = \{\hat{H}, \hat{O}, \hat{X}\}$，其中 $\hat{H}$ 为人体运动、$\hat{O}$ 为物体运动、$\hat{X}$ 为接触标注。交互动力学模型则显式建模物体如何响应人体运动，对生成结果施加物理一致性约束。

### 3.2 交互动力学模型

#### 3.2.1 动力学形式化

交互动力学模型的核心思想是将物体运动分解为受人体驱动的响应过程。形式化地，系统定义为：

**驱动者（人体）**：
$$
\begin{cases}
h^{(t+1)} = h^{(t)} + \Delta t \cdot F_h(h^{(t)}) \\
y_h^{(t)} = g_h(h^{(t)})
\end{cases}
$$

**响应者（物体）**：
$$
\begin{cases}
o^{(t+1)} = o^{(t)} + \Delta t \cdot F_o(o^{(t)}, s^{(t)}, u^{(t)}) \\
y_o^{(t)} = g_o(o^{(t)})
\end{cases}
$$

其中 $h^{(t)}$ 为人体状态，$o^{(t)}$ 为物体状态，$s^{(t)}$ 为交互上下文（如接触状态），$u^{(t)}$ 为外部控制信号。控制信号 $u^{(t)}$ 基于人体运动与物体当前状态之间的误差反馈计算，体现了“人驱动物”的因果机制。

#### 3.2.2 物体相对运动的可学习近似

上述连续动力学在实际中难以精确求解，因此 HOI-Dyn 采用可学习的近似函数 $\mathscr{D}$ 来预测物体的相对运动：

$$
\Delta o^{(t)} = o^{(t+1)} - o^{(t)} = \Delta t \cdot F_o(o^{(t)}, s^{(t)}, u^{(t)}) \approx \mathscr{D}(s^{(t)}, o^{(t)}, \Delta h^{(t)}; \theta)
$$

该函数以交互上下文 $s^{(t)}$、物体当前状态 $o^{(t)}$ 和人体相对运动 $\Delta h^{(t)}$ 为输入，直接预测物体在下一时刻的状态变化。模型参数 $\theta$ 通过监督学习从数据中习得。

#### 3.2.3 刚体变换与 SVD 投影

模型预测的物体运动被表示为刚体变换，包含旋转 $\hat{\mathcal{R}}^{(t \to t+k)} \in \mathrm{SO}(3)$ 和平移 $\hat{\mathcal{T}}^{(t \to t+k)}$。为保证旋转矩阵的有效性，对网络原始输出 $\tilde{\mathcal{R}} \in \mathbb{R}^{3 \times 3}$ 进行 SVD 分解后重构：

$$
\tilde{\mathcal{R}} = U \Sigma V^{\top}, \quad \hat{\mathcal{R}} = U V^{\top}
$$

该投影确保 $\hat{\mathcal{R}}$ 是合法的旋转矩阵（行列式为 1 的正交矩阵）。

#### 3.2.4 损失函数

**物体动力学损失** 衡量预测物体关键点与真实关键点之间的 L1 误差：

$$
\Phi(\Delta o_{t \to t+k}, \Delta o_{t \to t+k}^{*}) = \| \mathcal{P}^{(t+k)} - \hat{\mathcal{P}}^{(t+k)} \|_1
$$

其中 $\mathcal{P}^{(t+k)}$ 和 $\hat{\mathcal{P}}^{(t+k)}$ 分别为真实和预测的物体关键点位置（经刚体变换后）。

**总体动力学损失** 对时间步和预测跨度取期望，并按跨度加权：

$$
\mathcal{L}_{\mathrm{dyn}} = \mathbb{E}_{t, k \sim \mathcal{U}(1, K)} \left[ \frac{1}{k} \cdot \Phi(\Delta o_{t \to t+k}, \Delta o_{t \to t+k}^{*}) \right]
$$

**完整训练目标** 在标准 HOI 损失 $\mathcal{L}_{\mathrm{hoi}}$ 基础上，额外加入动力学损失 $\mathcal{L}_{\mathrm{dyn}}$ 和物体重建损失 $\mathcal{L}_{\mathrm{obj}}$：

$$
\mathcal{L}_{\mathrm{obj}} = \mathbb{E}_t [\Phi(o_t, \hat{o}_t)]
$$

### 3.3 模型设计要点

- **耦合设计**：交互动力学模型将人体运动与接触信息统一建模，而非将其解耦为独立分支。消融实验（Table 3）表明，在相近参数量（0.5M）和计算量（0.2 GFLOPs）约束下，耦合设计（Object Point Cloud Loss: 0.462）优于解耦变体（0.503），验证了人-物交互中固有的耦合特性。

- **预测跨度**：超参数 $K$ 控制动力学模型的前瞻步数。消融实验（Figure 4）显示 $K=2$ 或 $K=3$ 时物体点云损失最优，过大的 $K$ 反而导致性能下降，表明适度的短期动力学约束最为有效。

### 补充图表

![[assets/figures/papers/paper_list_l1685_HOI_Dyn_Learning_Interaction_Dynamics_for_Human_Object_Motion_Diffusion/figures/002_Figure_2.jpg]]
*Figure 2: Comparison of HOI-Dyn and CHOIS on physical plausibility and sequence-level coherence. (a–b) CHOIS produces premature object motion lacking causal timing; (c) HOI-Dyn generates more realistic post-contact responses; (d) HOI-Dyn maintains consistent human-object interaction across the full sequence. Green markers indicate object initial state and sparse waypoints*

## 实验与分析

### 主结果

HOI-Dyn 在 FullBodyManipulation 基准上全面超越现有方法。以核心交互指标 **Te (cm) ↓** 为例，本方法取得 **5.58**，较 CHOIS 的 6.16 降低 0.58（Table 1），表明物体末端位置误差显著缩小。其他关键指标同步改善：接触帧比例 **C%** 从 CHOIS 的 0.57 提升至 **0.60**，接触 F1 分数 **CF1** 达到 **0.71**，人体运动质量 **FID** 降至 **0.48**。在 3D-FUTURE 数据集上，HOI-Dyn 同样展现出跨场景泛化能力，**FS** 保持 0.37，**C%** 达 0.54（Table 2）。

![[assets/figures/papers/paper_list_l1685_HOI_Dyn_Learning_Interaction_Dynamics_for_Human_Object_Motion_Diffusion/figures/003_Table_1.jpg]]
*Table 1: Comparison of methods across different metrics. Arrows indicate whether lower*

![[assets/figures/papers/paper_list_l1685_HOI_Dyn_Learning_Interaction_Dynamics_for_Human_Object_Motion_Diffusion/figures/004_Table_2.jpg]]
*Table 2: Interaction synthesis results on the 3D-FUTURE dataset [30]*

定性对比（Figure 2）揭示了性能差异的因果根源：CHOIS 生成的物体运动缺乏因果时序，表现为物体在人体接触前即发生“预运动”；HOI-Dyn 通过交互动力学模型显式建模人体驱动→物体响应的因果链，产生更真实的接触后响应。

### 消融实验

**交互动力学损失形式**（Table 7）：残差动力学公式（residual dynamics）在物理真实性和接触精度上持续优于绝对预测范式，验证了“建模物体相对人体运动的增量变化”这一核心设计选择。

**预测视野 K**（Figure 4）：K=2 或 K=3 时物体点云损失最优。过小的 K 无法捕捉足够长的因果依赖，过大的 K 引入远期预测噪声，两者均损害动力学建模质量。

**耦合 vs. 解耦设计**（Table 3）：在相近参数量（0.5M）和计算量（0.2 GFLOPs）约束下，耦合模型（物体点云损失 0.462）显著优于解耦变体（0.503），证明人体运动与接触信息的统一建模是必要的——两者在 HOI 中存在固有耦合，强行解耦会丢失关键交互信号。

**引导策略**（Table 4）：HOI-Dyn 即使不使用任何引导项，性能已超越 CHOIS。加入足部-地面引导提升物理真实感，手部-物体引导增强接触精度，二者联合使用达到全指标 SOTA。

**无路径点设置**（Table 5）：去除路径点条件后，HOI-Dyn 仍改善足部质量、接触质量、FID 和多样性，同时保持穿透率不恶化，表明交互动力学模块本身即内化了合理的物理约束。

### 失败模式与局限性

当前分析材料未提供明确的失败案例或系统性能边界。以下观察需人工验证：

- **多物体交互扩展性**：论文在 Further Discussion 中提出“耦合设计如何扩展到更复杂的多物体交互”为开放问题，暗示当前框架可能面向单物体交互优化，多物体场景下的动力学耦合建模尚未验证。
- **真实场景引导效果**：Table 4 展示了引导项的定量收益，但引导对多样化真实场景（超出评估指标覆盖范围）的影响未被充分探索。
- **自回归稳定性**：Figure 11 展示了自回归性能，但具体误差累积模式未在现有材料中展开，需查阅原文确认长序列生成是否存在漂移问题。

![[assets/figures/papers/paper_list_l1685_HOI_Dyn_Learning_Interaction_Dynamics_for_Human_Object_Motion_Diffusion/figures/009_Table_4.jpg]]
*Table 4: Effect of Different Guidance. Our method outperforms CHOIS even without guidance. The feet-floor term improves physical realism, while the hand-object term enhances contact accuracy. Combining both achieves SOTA performance across all metrics*

![[assets/figures/papers/paper_list_l1685_HOI_Dyn_Learning_Interaction_Dynamics_for_Human_Object_Motion_Diffusion/figures/019_Figure_11.jpg]]
*Figure 11: Auto-regressive performance*

### 鲁棒性分析

输入扰动实验（Table 8-9）表明，交互动力学模型对小幅输入扰动保持稳定。在扰动幅度为输入范数 0.001%–0.1% 的范围内，预测物体运动的变化可控。这一特性源于 SVD 投影对旋转矩阵的正则化约束，以及残差预测范式对绝对位姿误差的解耦。

![[assets/figures/papers/paper_list_l1685_HOI_Dyn_Learning_Interaction_Dynamics_for_Human_Object_Motion_Diffusion/figures/017_Table_8.jpg]]
*Table 8: Effect of unit-vector perturbations scaled by ϵ on predicted object motion*

### 补充图表

![[assets/figures/papers/paper_list_l1685_HOI_Dyn_Learning_Interaction_Dynamics_for_Human_Object_Motion_Diffusion/figures/006_Figure_4.jpg]]
*Figure 4: Effect of Horizon K*

![[assets/figures/papers/paper_list_l1685_HOI_Dyn_Learning_Interaction_Dynamics_for_Human_Object_Motion_Diffusion/figures/008_Table_3.jpg]]
*Table 3: Effect of Design Variants. Our lightweight coupled model captures high-quality interaction dynamics, outperforming the decoupled variants under similar constraints*

![[assets/figures/papers/paper_list_l1685_HOI_Dyn_Learning_Interaction_Dynamics_for_Human_Object_Motion_Diffusion/figures/010_Table_5.jpg]]
*Table 5: Performance under the without waypoint setting. HOI-Dyn improves foot and contact quality, FID, and diversity, while preserving penetration, showing its intrinsic interaction dynamics*

![[assets/figures/papers/paper_list_l1685_HOI_Dyn_Learning_Interaction_Dynamics_for_Human_Object_Motion_Diffusion/figures/014_Table_7.jpg]]
*Table 7: Ablation of interaction dynamics loss formulations. Residual dynamics consistently improves physical realism and contact accuracy*

![[assets/figures/papers/paper_list_l1685_HOI_Dyn_Learning_Interaction_Dynamics_for_Human_Object_Motion_Diffusion/figures/005_Figure_3.jpg]]
*Figure 3: HOI generation in realistic 3D scenes. The virtual agent interacts with different objects while maintaining physical plausibility and environmental consistency*

## 方法谱系与知识库定位

### 1. 方法定位：Driver-Responder 动力学建模

HOI-Dyn 将人-物交互生成重新概念化为一个**Driver-Responder 系统**：人体运动作为“驾驶员”（driver），通过内在动力学演化；物体作为“响应者”（responder），其运动由人体运动驱动的外部控制信号决定。这一建模思路将交互生成从单纯的联合分布学习提升到**因果动力学层面**，核心创新在于引入了一个轻量级的交互动力学模型（Interaction Dynamics Model），显式预测物体如何响应人体运动。

与现有方法的本质区别在于：传统方法（如 CHOIS）将人物运动视为一个整体联合生成问题，缺乏对交互因果时序的显式建模。HOI-Dyn 通过将物体相对运动近似为可学习函数 $\mathscr{D}(s^{(t)}, o^{(t)}, \Delta h^{(t)}; \theta)$，以人体相对运动为条件预测物体刚性变换（旋转 $\hat{\mathcal{R}} \in \mathrm{SO}(3)$ 和平移 $\hat{\mathcal{T}} \in \mathbb{R}^3$），并通过 SVD 投影保证旋转矩阵的有效性。

### 2. 与基线方法的关系

论文以 **CHOIS** 作为核心对比基线。在 FullBodyManipulation 数据集上，HOI-Dyn 在物体平移误差 Te 上取得 **5.58 cm**，相比 CHOIS 的 6.16 cm 降低了 **0.58 cm**（Table 1），验证了动力学建模的有效性。

定性分析（Figure 2）揭示了 CHOIS 的关键失败模式：物体运动缺乏因果时序，表现为**过早运动**——物体在人体接触之前即开始响应，违背物理因果律。HOI-Dyn 通过 Driver-Responder 框架中的误差反馈控制信号 $u^{(t)}$，使物体仅在接触后才产生合理的响应运动，从而在序列级一致性上显著优于基线。

**需要手动验证**：论文未明确标注 CHOIS 的作者、会议和年份信息，建议补充为可验证的完整引用。

### 3. 轻量化设计策略

交互动力学模型仅含 **0.5M 参数**和 **0.2 GFLOPs** 计算量（Table 3），却能捕获高质量的交互动力学。这一设计选择验证了一个核心假设：**人-物交互的物理规律可以用极轻量的模型近似**，无需复杂物理模拟器。消融实验表明，耦合设计（coupled design）——即人体运动和接触信息在统一模型中联合建模——优于解耦策略（decoupled variants），在相近参数量下物体点云损失从 0.503 降至 0.462（Table 3），印证了人-物交互中存在的内在耦合性。

### 4. 适用边界与局限

**适用边界**：
- 当前框架针对**单人-单物**交互场景设计，训练数据为 FullBodyManipulation 数据集（约 10 小时、15 种物体）。
- 交互动力学模型的预测能力受限于训练数据中的物体类别和交互模式分布。
- 预测时域（horizon K）的最优值为 K=2 或 K=3（Figure 4），较长时域的动力学预测精度下降。

**已知局限**：
- 论文未涉及**多物体交互**或**多人协作**场景的扩展讨论。
- 动力学模型依赖人体运动作为驱动信号，在人体运动质量较差时可能传播误差。
- 对未见物体类别的泛化能力未经验证。

### 5. 开放问题

1. **多物体交互扩展**：耦合设计如何扩展到更复杂的多物体交互场景？不同物体之间的动力学耦合是否需要额外的建模机制？
2. **跨场景泛化**：在 3D-FUTURE 数据集上（Table 2）已初步验证泛化能力，但在真实世界场景中，动力学模型的鲁棒性如何？特别是面对训练集中未见的物体几何和物理属性时。
3. **引导策略的边界**：Table 4 显示结合 feet-floor 和 hand-object 引导可达到 SOTA，但这些引导项是否可能在某些场景下与动力学模型产生冲突？
4. **长序列稳定性**：当前框架在 K=2 或 K=3 时最优，更长时间尺度的交互动力学预测是否存在误差累积问题？是否需要引入闭环反馈机制？

## 原文 PDF

![[paperPDFs/arxiv_2025/HOI_Dyn_Learning_Interaction_Dynamics_for_Human_Object_Motion_Diffusion.pdf]]