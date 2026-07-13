---
title: "MergeVLA: Cross-Skill Model Merging Toward a Generalist Vision-Language-Action Agent"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/MergeVLA_Cross_Skill_Model_Merging_Toward_a_Generalist_Vision_Language_Action_Agent.pdf
project_link: "https://mergevla.github.io/"
code_link: null
aliases:
- MergeVLA
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: 通过设计：1）任务掩码稀疏激活合并后的LoRA参数，抑制冲突；2）移除动作专家中的自注意力层，仅保留交叉注意力；3）将深度专业化的专家头部保持为任务特定组件，实现整体模型的可合并性。
primary_logic: VLA模型合并的核心障碍不在于模型容量或训练数据，而在于架构诱导的任务干扰：LoRA微调的速度方向发散和自注意力的跨层信息传播破坏了参数兼容性。通过在架构层面消除这些干扰源，模型合并可以在不损失性能的情况下实现多技能统一。
claims:
- 当合并4个LIBERO任务时，LoRA更新中超过75%的参数仅被单一任务独占使用（自私参数），导致直接合并冲突严重。
- 动作专家在深层块（最后几层）的相对L2距离急剧增大，表明自注意力累积了不可调和的任务特定差异。
- 仅对VLM施加任务掩码但保留动作专家自注意力时，合并模型在VLA-Adapter上成功率为0%；而移除自注意力后，成功率显著回升。
- MergeVLA_TIES在LIBERO上达到90.2%平均成功率，仅比单任务微调的MergeVLA低6.5个百分点，超越了所有合并基线。
---

# MergeVLA: Cross-Skill Model Merging Toward a Generalist Vision-Language-Action Agent

> [!tip] 核心洞察
> VLA模型合并的核心障碍不在于模型容量或训练数据，而在于架构诱导的任务干扰：LoRA微调的速度方向发散和自注意力的跨层信息传播破坏了参数兼容性。通过在架构层面消除这些干扰源，模型合并可以在不损失性能的情况下实现多技能统一。

| 字段 | 内容 |
|------|------|
| 中文题名 | MergeVLA：面向通用视觉-语言-动作智能体的跨技能模型合并 |
| 英文题名 | MergeVLA: Cross-Skill Model Merging Toward a Generalist Vision-Language-Action Agent |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2511.18810) · [Project](https://mergevla.github.io/) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/image_and_video_generation |
| Method | MergeVLA |
| Dataset | LIBERO, LIBERO-Plus, RoboTwin, Real-World SO-101 |

> [!tip] 效果简介
> - LIBERO 上，平均成功率 (%) 90.2 (MergeVLA_TIES) vs 96.7 (MergeVLA 单任务微调) (-6.5%)；平均成功率 (%) 44.2 (OpenVLA + TA 仅视觉骨干) vs 76.5 (OpenVLA 单任务微调) (-32.3%)。
> - LIBERO-Plus 上，平均成功率 (%) 62.5 (MergeVLA_TIES) vs 16.3 (OpenVLA 单任务微调) (+46.2%)。
> - RoboTwin (Setting A) 上，平均成功率 (%) 88.7 (MergeVLA_TIES, H^{(L-1)L}) vs 88.0 (MergeVLA 单任务微调) (+0.7%)。

## 概要

**核心问题**：视觉-语言-动作（VLA）模型在微调后如何合并多技能策略，使单一模型在无需重新训练的情况下胜任多种机器人操作任务？现有VLA架构在合并时面临严重冲突：LoRA适配器在VLM骨干中产生高度任务独占的更新方向（自私参数比例超过75%），同时动作专家中的自注意力层通过跨层传播累积了不可调和的任务特定差异，导致直接合并后成功率骤降至零。

**核心结论**：VLA模型合并的根本障碍不在于模型容量或训练数据，而在于架构诱导的任务干扰。通过在架构层面消除干扰源——对合并后的LoRA参数施加任务掩码以稀疏激活有益参数、将动作专家中的自注意力替换为交叉注意力、保留深度专业化层作为任务特定的专家头部——可以在不牺牲性能的情况下实现多技能统一。

**方法定位**：MergeVLA属于**数据无关的模型合并**范式，在方法谱系上介于参数级合并（如**Task Arithmetic**，Ilharco et al., ICLR 2023；**TIES-Merging**，Yadav et al., NeurIPS 2023）与架构改造之间。与纯合并方法不同，MergeVLA通过重新设计VLA架构来创造可合并条件，而非仅优化合并算法本身。其核心组件包括：任务掩码VLM（稀疏激活合并后的LoRA参数）、交叉注意力动作专家（移除自注意力以消除跨层干扰）、专家头部（保留任务特定深层不参与合并），以及测试时任务路由器（基于VLM隐藏状态在价值子空间上的响应自动识别任务）。

**主要结果**：MergeVLA_TIES在LIBERO基准上达到90.2%平均成功率，仅比单任务微调的MergeVLA低6.5个百分点，显著超越所有合并基线（合并基线的OpenVLA仅44.2%）。在LIBERO-Plus分布外泛化测试中达到62.5%，比单任务微调的OpenVLA高46.2个百分点。在RoboTwin跨具身设置中达到88.7%，与单任务微调持平。在真实世界SO-101机械臂上取得与单任务模型相同的90.0%成功率。这些结果表明，通过架构层面的可合并性设计，模型合并能够在多种具身和任务场景下实现接近单任务微调的性能。



### 通用视觉-语言-动作智能体的需求与挑战

构建能够执行多样化操作任务的通用机器人智能体是具身人工智能的核心目标。视觉-语言-动作（VLA）模型通过将大规模视觉-语言模型（VLM）的语义理解能力与物理动作生成相结合，展现出实现这一目标的巨大潜力。然而，现有VLA模型面临一个关键瓶颈：**多技能统一与单技能性能之间的尖锐矛盾**。

当前主流的VLA训练范式是为每个特定任务独立微调一个模型，这导致了一系列实际问题。首先，为每个新任务维护一个完整的模型副本会带来显著的存储和部署开销。其次，当需要模型同时具备多个技能时，缺乏有效的机制将这些独立微调的模型整合为一个统一的通用智能体。模型合并（Model Merging）技术——通过算术方式组合多个任务特定的参数更新——在语言和视觉领域已展现出在不牺牲单任务性能的前提下实现多任务统一的能力。然而，直接将现有的模型合并方法应用于VLA模型时，性能会灾难性地崩溃至接近零成功率。

### 现有VLA架构的合并障碍

为了理解VLA模型合并失败的根本原因，MergeVLA对代表性VLA架构中的可训练参数进行了细粒度的分解分析，识别出**两个关键的不兼容性来源**。

**第一个来源是VLM骨干中LoRA微调产生的参数冲突。** 当使用LoRA对不同任务微调同一个VLM时，各任务产生的参数更新方向高度发散。实验证据表明，在合并4个LIBERO任务时，使用**Task Arithmetic**（Ilharco et al., ICLR 2023）或**TIES-Merging**（Yadav et al., NeurIPS 2023）生成的合并掩码中，超过75%的参数仅被单一任务独占使用——论文将这些参数定义为“自私参数”（selfish parameters）。这种高度的任务独占性意味着不同任务的LoRA更新在参数空间中占据几乎不相交的区域，直接进行算术合并必然导致严重的参数干扰，使合并后的模型在所有任务上均失效。

**第二个来源是动作专家中自注意力机制的跨层任务依赖。** 在典型的双系统VLA架构（如**VLA-Adapter**）中，动作专家包含自注意力和交叉注意力层，负责将VLM的隐藏状态转换为可执行的动作。分析发现，随着网络层数加深，不同任务的动作专家之间的相对L2距离急剧增大，尤其在最后几层达到峰值。这表明自注意力层在逐层传播过程中累积了不可调和的任务特定差异，使得深层参数在任务间完全不兼容。直接合并这些动作专家会导致零成功率，即便已经对VLM部分施加了任务掩码。

### 核心洞察：架构诱导的任务干扰

上述发现揭示了一个深层洞察：**VLA模型合并的核心障碍不在于模型容量不足或训练数据有限，而在于架构本身诱导的任务干扰**。LoRA微调的速度方向发散和自注意力的跨层信息传播共同破坏了参数空间的可合并性，导致模块化丧失。因此，解决VLA合并问题的关键不是设计更复杂的合并算法，而是**在架构层面消除这些干扰源**，使模型在微调后天然具备可合并性。

### MergeVLA的设计动机

基于上述分析，MergeVLA提出了一个根本性的解决方案：重新设计VLA架构，使其在保持单任务微调性能的同时，支持通过简单的数据无关合并方法实现多技能统一。具体而言，MergeVLA从三个层面解决合并障碍：

1. **任务掩码稀疏激活**：对合并后的LoRA参数施加任务特定的二进制掩码，选择性激活对当前任务有益的更新方向，同时抑制误导其他任务的参数。这直接回应了LoRA参数高度任务独占的问题。

2. **移除自注意力，仅保留交叉注意力**：将动作专家中的自注意力层完全移除，仅保留交叉注意力层，并使用sigmoid门控替代传统的tanh门控。这一设计截断了任务特定差异在层间的累积传播路径，使浅层动作专家块变得可合并，同时将深度专业化的最终块保留为任务特定的“专家头部”。

3. **测试时任务路由**：在实际部署中，任务身份通常是未知的。MergeVLA设计了一个无需训练的测试时任务路由器，通过分析VLM隐藏状态在动作专家价值子空间上的激活强度，自动推断当前任务并选择相应的任务掩码和专家头部。

通过这种架构层面的重新设计，MergeVLA使模型合并技术首次在VLA领域实现了实用化的性能，为构建通用视觉-语言-动作智能体开辟了新路径。



## 核心方法与创新机理

### 问题诊断：架构诱导的任务干扰是VLA合并的根因

现有VLA模型合并面临的核心障碍并非模型容量或训练数据不足，而是**架构设计本身引入了不可调和的参数冲突**。MergeVLA通过精细的参数分解，识别出两大干扰源：

1. **VLM骨干中的LoRA冲突**：在LIBERO四个任务上微调后，采用Task Arithmetic或TIES-Merging进行合并时，超过**75%的LoRA参数仅被单一任务独占使用**（即“自私参数”，参见Figure 3左图及公式4）。这些高度任务独占的更新方向在合并时产生严重冲突，导致直接合并后成功率趋近于零。

2. **动作专家中的自注意力累积偏差**：VLA-Adapter等双系统架构中的动作专家模块包含自注意力层，随着网络深度增加，不同任务的动作专家在深层块（最后几层）的相对L2距离急剧增大（Figure 3右图），表明自注意力机制在跨层传播中累积了不可调和的任务特定差异，使得这些层的参数无法通过标准合并方法统一。

### 架构重设计：三个关键changed slots

针对上述诊断，MergeVLA在VLA-Adapter的基础上进行了三项架构改造，从根本上消除合并障碍：

**Slot 1：任务掩码稀疏激活的LoRA合并（替代直接平均/符号合并）**

传统合并方法（TA、TIES等）对所有合并参数施加统一操作，无法区分参数对不同任务的贡献差异。MergeVLA引入**任务特定的二进制掩码** $\mathbf{S}_m$，作用于合并后的LoRA更新 $\tau_{\mathrm{merge}}$：

$$\Theta_{\mathrm{merge}}^{(m)} = \Theta_0 + \mathbf{S}_m \odot \tau_{\mathrm{merge}}$$

掩码的构建规则基于参数重要性（任务特定更新幅值）和对合并更新的主导性：

$$\mathbf{S}_m = \mathbb{I}\left[|\tau_m| > \lambda |\tau_{\mathrm{merge}} - \tau_m|\right]$$

该机制的核心insight在于：**稀疏激活合并后的LoRA参数，保留对当前任务有益的更新，同时抑制误导其他任务的冲突更新**，使部分参数回退至预训练权重，从而保持预训练视觉-语言表征的稳定性。

**Slot 2：动作专家去自注意力化（替代自注意力+交叉注意力）**

VLA-Adapter的动作专家同时包含自注意力和交叉注意力层，自注意力的跨层信息传播破坏了参数兼容性。MergeVLA将动作专家**重新设计为仅含交叉注意力的模块**，完全移除自注意力层。这一改造使得动作专家的特征转换完全依赖于VLM输出的隐藏状态，将任务特化局部化到可组合的浅层模块中。

同时，门控函数从tanh替换为**sigmoid**，以更稳定地保留和依赖鲁棒的VLM特征。

**Slot 3：专家头部保留为任务特定组件（替代全层合并）**

即使去除了自注意力，动作专家的深层块（最后几层）仍表现出强烈的任务特化。MergeVLA将这些深层块定义为**专家头部（expert head）**，标记为 $\bar{\mathbf{H}^{l \to L}}$，在合并时保持独立不参与合并，仅浅层交叉注意力块参与参数合并。消融实验证实，若强制合并专家头部，成功率直接降为0%（Table 1: VLA-Adapter + TA + S）。

### 测试时任务路由：免训练的组件选择

合并后的模型包含多套任务掩码和专家头部，在测试时需根据任务身份动态选择。MergeVLA提出**免训练的测试时任务路由器**，利用合并后动作专家中价值投影矩阵的SVD分解，提取任务和动作的主导子空间：

$$\mathbf{V}_{\mathrm{T}}^{l} = \mathbf{L}_{\mathrm{T}}^{l} \mathbf{\Sigma}_{\mathrm{T}}^{l} (\mathbf{R}_{\mathrm{T}}^{l})^{\top}, \quad \mathbf{V}_{\mathrm{A}}^{l} = \mathbf{L}_{\mathrm{A}}^{l} \mathbf{\Sigma}_{\mathrm{A}}^{l} (\mathbf{R}_{\mathrm{A}}^{l})^{\top}$$

将掩码VLM的隐藏状态投影到这些子空间上，计算L2范数作为任务相关性得分：

$$r_{\mathrm{T}, m} = \| \mathbf{P}_{\mathrm{T}}^{l} \mathbf{h}_{\mathrm{A}, m}^{l} \|_{2}, \quad r_{\mathrm{A}, m} = \| \mathbf{P}_{\mathrm{A}}^{l} \mathbf{h}_{\mathrm{T}, m}^{l} \|_{2}$$

消融实验表明，使用价值（V）投影进行路由比键（K）或查询（Q）投影更可靠，仅V投影在LIBERO上平均成功率达89.7%（Table 5）。该路由器仅依赖初始观察，无需额外训练。

### 创新本质总结

MergeVLA的核心创新在于**将VLA合并问题从“参数空间优化”重新定义为“架构兼容性设计”**：通过在架构层面消除LoRA的自私参数冲突和自注意力的跨层干扰，使得标准数据无关合并方法（TA、TIES、WUDI）能够直接应用于VLA模型，在仅损失6.5%成功率的情况下实现多技能统一（LIBERO: 90.2% vs. 96.7%单任务上限），且合并模型在OOD泛化（LIBERO-Plus: +46.2% vs. OpenVLA单任务微调）和跨具身迁移（RoboTwin: 88.7%）上展现出显著优势。



MergeVLA 的整体设计围绕一个核心洞察展开：VLA 模型合并的根本障碍并非容量或数据不足，而是**架构诱导的任务干扰**——LoRA 微调在 VLM 骨干中产生高度任务独占的更新方向，同时动作专家的自注意力机制通过跨层信息传播累积不可调和的任务特定差异。为解决这一问题，MergeVLA 从三个层面重构了可合并性：**任务掩码稀疏激活**抑制 VLM 中的参数冲突，**交叉注意力动作专家**消除自注意力带来的跨层干扰，以及**测试时任务路由器**实现无需训练的推理时任务识别。

### 架构总览

MergeVLA 的推理管线由三个核心模块串联构成，如图 Figure 2 所示：

![[assets/figures/papers/paper_list_l2403_https_arxiv_org_abs_2511_18810/figures/002_Figure_2.jpg]]
*Figure 2: Overview of MergeVLA architecture. (1) To address destructive LoRA parameter interference in finetuned VLM, task masks are applied to all merged LoRA modules to selectively activate the merged parameters contributing to task-relevant responses while suppressing those that mislead other tasks. (2) To solve the incompatibility of action experts, the architecture is redesigned to contain only cross-attention blocks and use sigmoid gate to preserve and rely on robust VLM features. Most blocks then can be merged except deeper blocks named expert head are left unmerged due to their task specification. (3) To address the setting where the task identity is unknown at inference time, a training-free...*

1. **任务掩码 VLM（Task-Masked VLM）**：接收多视角图像（第三视角 $\mathbf{I}_t^v$、腕部视角 $\mathbf{I}_t^w$）和语言指令 $L$，通过施加任务特定二进制掩码的合并 LoRA 参数，生成任务感知的隐藏状态。掩码机制选择性激活对当前任务有益的合并参数，同时抑制可能误导其他任务的冲突更新。

2. **交叉注意力动作专家（Cross-Attention Action Expert）**：架构被重新设计为仅包含交叉注意力块，移除了传统 VLA-Adapter 中的自注意力层。该模块以 VLM 隐藏状态为条件，通过交叉注意力和前馈网络进行特征转换，并采用 sigmoid 门控替代 tanh 门控以增强对 VLM 稳健特征的依赖。大部分浅层块可安全合并，而深度专业化的最终块作为**专家头部（Expert Head）**保留为任务特定组件，不参与合并。

3. **测试时任务路由器（Test-Time Task Router）**：在推理时任务身份未知的场景下，该模块利用掩码 VLM 的隐藏状态在合并动作专家价值投影子空间上的激活强度，动态选择对应的任务掩码和专家头部。具体而言，对动作专家第 $l$ 层的任务和动作交叉注意力价值投影矩阵进行 SVD 分解（$\mathbf{V}_{\mathrm{T}}^{l} = \mathbf{L}_{\mathrm{T}}^{l} \mathbf{\Sigma}_{\mathrm{T}}^{l} (\mathbf{R}_{\mathrm{T}}^{l})^{\top}$，$\mathbf{V}_{\mathrm{A}}^{l} = \mathbf{L}_{\mathrm{A}}^{l} \mathbf{\Sigma}_{\mathrm{A}}^{l} (\mathbf{R}_{\mathrm{A}}^{l})^{\top}$），随后将掩码 VLM 的隐藏状态投影到这些主导子空间上，以 L2 范数 $r_{\mathrm{T}, m} = \| \mathbf{P}_{\mathrm{T}}^{l} \mathbf{h}_{\mathrm{A}, m}^{l} \|_{2}$ 和 $r_{\mathrm{A}, m} = \| \mathbf{P}_{\mathrm{A}}^{l} \mathbf{h}_{\mathrm{T}, m}^{l} \|_{2}$ 作为任务相关性得分。

### 不可合并性的根源分析

MergeVLA 的设计动机源于对 VLA 微调过程中参数冲突的实证分析。如图 Figure 3（左）所示，当合并 4 个 LIBERO 任务时，基于 TA 和 TIES 方法生成的掩码中，**自私参数比例超过 75%**——这意味着超过四分之三的 LoRA 更新参数仅被单一任务独占使用，直接合并必然导致严重的参数冲突。与此同时，Figure 3（右）揭示了动作专家在深层块（最后几层）的相对 L2 距离急剧增大，表明自注意力机制在深度层累积了不可调和的任务特定差异。这两个发现共同指向一个结论：VLA 模型合并的瓶颈在于架构诱导的干扰，而非合并算法本身的不足。

### 设计决策的因果链条

MergeVLA 的三个设计决策构成了一条完整的因果链：

- **任务掩码**解决了 LoRA 参数空间的冲突问题，但仅靠掩码并不足以恢复合并性能——在保留动作专家自注意力的情况下，即使施加任务掩码，合并模型在 VLA-Adapter 上的成功率仍为 **0%**（Table 1）。
- **移除自注意力**是恢复可合并性的关键步骤：将动作专家重构为仅交叉注意力块后，合并性能显著回升。这一架构变化在 LIBERO-Plus 的 OOD 泛化测试中带来了 **13.4%** 的成功率提升。
- **专家头部保留**是必要的折中：深度专业化的最终块无法安全合并，完全合并会导致 0% 成功率，因此将其作为任务特定组件保留。

### 合并流程

在训练阶段，MergeVLA 首先对每个单技能模仿学习数据集 $\mathcal{D}_m = \{ \mathbf{I}_t^v, \mathbf{I}_t^w, L \}_{t=1}^T$ 独立微调得到 $M$ 个任务特定模型，每个模型包含 LoRA 适配器和动作专家参数。随后，通过标准数据无关合并方法（如 TA 或 TIES）计算合并更新 $\tau_{\mathrm{merge}} = \alpha \mathcal{R}(\{\tau_m\}_{m=1}^M)$，并对每个任务 $m$ 施加二进制掩码 $\mathbf{S}_m$，得到任务特定的合并参数 $\Theta_{\mathrm{merge}}^{(m)} = \Theta_0 + \mathbf{S}_m \odot \tau_{\mathrm{merge}}$。掩码的构建遵循规则 $\mathbf{S}_m = \mathbb{I}\left[|\tau_m| > \lambda |\tau_{\mathrm{merge}} - \tau_m|\right]$，基于参数重要性和对合并更新的主导性进行筛选。动作专家的浅层交叉注意力块参与合并，而深层专家头部保持任务特定。

### 补充图表

![[assets/figures/papers/paper_list_l2403_https_arxiv_org_abs_2511_18810/figures/001_Figure_1.jpg]]
*Figure 1: Comparison between the structures of different VLAs. OpenVLA uses a standard VLM for token-based action generation. VLA-Adapter adds an action expert with cross- and self-attention layers. MergeVLA simplifies this design by removing non-mergeable self-attention layers for effective merging*



### 4.1 任务掩码稀疏激活（Task-Masked VLM）

MergeVLA 在 VLM 骨干中引入**任务掩码**机制，解决 LoRA 微调后参数空间不可调和的问题。给定 $M$ 个单技能微调模型，每个模型相对于预训练权重 $\Theta_0$ 产生任务向量 $\tau_m = \Theta_m - \Theta_0$。标准的数据无关合并方法通过聚合这些任务向量得到一个统一更新：

$$\tau_{\mathrm{merge}} = \alpha \mathcal{R}(\{\tau_m\}_{m=1}^M), \quad \Theta_{\mathrm{merge}} = \Theta_0 + \tau_{\mathrm{merge}} \tag{1}$$

其中 $\mathcal{R}$ 为合并算子（如 **Task Arithmetic** (Ilharco et al., ICLR 2023) 或 **TIES-Merging** (Yadav et al., NeurIPS 2023)），$\alpha$ 为合并缩放因子。

然而，直接合并导致严重的任务干扰。分析表明，合并 4 个 LIBERO 任务时，超过 **75%** 的 LoRA 参数仅被单一任务独占使用（即“自私参数”，Selfish Parameters），直接平均或符号合并必然产生冲突（Figure 3 左）。为此，MergeVLA 对合并更新施加任务特定的二进制掩码 $\mathbf{S}_m$：

![[assets/figures/papers/paper_list_l2403_https_arxiv_org_abs_2511_18810/figures/003_Figure_3.jpg]]
*Figure 3: Left: Selfish ratio of the masks from TA [21] and TIES [48] by merging different numbers of tasks. The selfish ratio is computed following Equation 4. Right: The average relative L2 distance across blocks between all pairs of action experts*

$$\Theta_{\mathrm{merge}}^{(m)} = \Theta_0 + \mathbf{S}_m \odot \tau_{\mathrm{merge}} \tag{2}$$

掩码的构建规则基于两个准则：参数的**任务特定重要性**（以 $|\tau_m|$ 度量）和其对合并更新的**主导性**：

$$\mathbf{S}_m = \mathbb{I}\left[|\tau_m| > \lambda |\tau_{\mathrm{merge}} - \tau_m|\right] \tag{3}$$

其中 $\lambda$ 为掩码比率超参数，$\mathbb{I}[\cdot]$ 为指示函数。该规则保留那些在任务 $m$ 中更新幅度显著大于其在其他任务中平均偏离的参数，抑制跨任务冲突的更新方向。自私参数比例可形式化为：

$$\mathrm{ratio}_{\mathrm{selfish}} = \frac{1}{N} \sum_{i=1}^N \mathbb{I}\left[\sum_{m=1}^M (\mathbf{S}_m)_i = 1\right] \tag{4}$$

**因果机制**：任务掩码通过稀疏激活合并后的 LoRA 参数，使部分参数回退至预训练权重，从而保留预训练的视觉-语言表征并抑制跨任务冲突。消融表明，适中的 $\lambda$（0.6~0.9）在 LIBERO-Long 上获得 >70% 成功率，过高或过低均导致性能下降（Figure 7b）。

### 4.2 可合并动作专家架构

**VLA-Adapter** 的动作专家包含自注意力和交叉注意力层。分析发现，动作专家在深层块（最后几层）的相对 L2 距离急剧增大（Figure 3 右），表明自注意力累积了不可调和的任务特定差异。仅对 VLM 施加任务掩码但保留动作专家自注意力时，合并模型成功率为 **0%**（Table 1: VLA-Adapter + TA + S (All)）。

MergeVLA 对动作专家进行三项架构改造：

1. **移除自注意力层**，仅保留交叉注意力。这使得任务特定信息仅通过 VLM 的隐藏状态单向流入，避免自注意力在专家内部传播和放大任务差异。
2. **门控函数从 tanh 替换为 sigmoid**：
   $$\hat{\mathbf{h}}_{\mathrm{T}}^{i} = g(\mathbf{h}_{\mathrm{T}}^{i})$$
   其中 $g(\cdot)$ 为 sigmoid 函数。sigmoid 门控使专家更依赖 VLM 的鲁棒特征，减少对任务特定激活的敏感度。
3. **专家头部保留不合并**：将深层块 $\bar{\mathbf{H}}^{l \to L}$（从第 $l$ 层到最终层 $L$）作为任务特定的专家头部，仅合并浅层交叉注意力块。完全合并所有层导致 0% 成功率（Table 1），验证了深度专业化层不可合并的结论。

**因果机制**：移除自注意力切断了跨层任务依赖的传播路径，使动作专家的参数更新在任务间保持兼容；sigmoid 门控进一步降低对任务特定特征的依赖；专家头部保留则避免了深度专业化层的强制对齐。仅此架构改造就在 LIBERO-Plus 的 OOD 泛化上比 VLA-Adapter 高出 **13.4%** 成功率。

### 4.3 测试时任务路由器

合并后的模型包含 $M$ 个掩码 VLM 变体 $\Theta_{\mathrm{merge}}^{(m)}$ 和 $M$ 个专家头部。在测试时，任务身份未知，需自动选择正确的掩码和头部。MergeVLA 提出**免训练的测试时任务路由器**，利用合并后动作专家内部的价值子空间进行任务推断。

具体地，对动作专家第 $l$ 层的任务路径和动作路径的交叉注意力价值投影矩阵进行奇异值分解，提取主导子空间：

$$\mathbf{V}_{\mathrm{T}}^{l} = \mathbf{L}_{\mathrm{T}}^{l} \mathbf{\Sigma}_{\mathrm{T}}^{l} (\mathbf{R}_{\mathrm{T}}^{l})^{\top}, \quad \mathbf{V}_{\mathrm{A}}^{l} = \mathbf{L}_{\mathrm{A}}^{l} \mathbf{\Sigma}_{\mathrm{A}}^{l} (\mathbf{R}_{\mathrm{A}}^{l})^{\top} \tag{6}$$

其中 $\mathbf{V}_{\mathrm{T}}^{l}$ 和 $\mathbf{V}_{\mathrm{A}}^{l}$ 分别为任务和动作路径的价值投影矩阵。取前 $k_r$ 个右奇异向量构成子空间投影矩阵 $\mathbf{P}_{\mathrm{T}}^{l}$ 和 $\mathbf{P}_{\mathrm{A}}^{l}$。

对于任务 $m$ 的掩码 VLM 产生的隐藏状态 $\mathbf{h}_{\mathrm{A}, m}^{l}$（动作路径）和 $\mathbf{h}_{\mathrm{T}, m}^{l}$（任务路径），计算其在对应子空间上的激活强度：

$$r_{\mathrm{T}, m} = \| \mathbf{P}_{\mathrm{T}}^{l} \mathbf{h}_{\mathrm{A}, m}^{l} \|_{2}, \quad r_{\mathrm{A}, m} = \| \mathbf{P}_{\mathrm{A}}^{l} \mathbf{h}_{\mathrm{T}, m}^{l} \|_{2} \tag{7}$$

任务相关性得分 $r_m = r_{\mathrm{T}, m} + r_{\mathrm{A}, m}$。路由器选择得分最高的任务 $m^* = \arg\max_m r_m$，激活对应的掩码 $\mathbf{S}_{m^*}$ 和专家头部。

**关键发现**：使用价值（V）投影进行路由比使用键（K）或查询（Q）投影更可靠。仅 V 投影在 LIBERO 上平均成功率达到 **89.7%**（Table 5），而 K 或 Q 投影的路由准确率显著下降。这是因为价值投影直接编码了任务特定的输出变换，其子空间对任务身份更具判别力。路由器仅依赖初始观察，无需额外训练，但在任务切换的长周期操作中可能需要额外设计。



## 实验与关键发现

### 核心问题诊断：VLA模型为何不可合并

在展示主实验结果之前，MergeVLA首先对VLA模型合并失败的根本原因进行了系统性诊断。分析揭示了两个关键的架构诱导干扰源：

**LoRA更新的任务独占性。** 当合并4个LIBERO任务时，采用**Task Arithmetic**（Ilharco et al., ICLR 2023）和**TIES-Merging**（Yadav et al., NeurIPS 2023）两种合并方法生成的掩码中，超过75%的参数仅被单一任务独占使用（即自私参数比例>75%，见Figure 3左）。这意味着不同任务的LoRA更新方向高度发散，直接合并必然导致严重的参数冲突。

**动作专家自注意力的跨层干扰。** 对VLA-Adapter架构中不同任务的动作专家进行逐层相对L2距离分析发现，在深层块（最后几层）的距离急剧增大（见Figure 3右）。这表明自注意力机制在深层累积了不可调和的任务特定差异，使得参数空间无法直接融合。

这两项诊断共同指向一个核心结论：VLA模型合并的瓶颈不在于模型容量或训练数据，而在于架构诱导的任务干扰——LoRA微调的速度方向发散和自注意力的跨层信息传播破坏了参数兼容性。

### 主实验结果

#### LIBERO基准任务合并

Table 1展示了MergeVLA在LIBERO四个任务套件（Spatial、Object、Goal、Long）上的合并效果。关键发现如下：

- **MergeVLA_TIES**在LIBERO上达到**90.2%的平均成功率**，仅比单任务微调的MergeVLA（96.7%）低6.5个百分点，显著超越了所有合并基线。
- 相比之下，直接对**OpenVLA**视觉骨干应用Task Arithmetic合并，平均成功率仅为44.2%，较单任务微调（76.5%）下降32.3个百分点——这充分说明未经架构适配的VLA模型几乎无法通过现有合并方法有效融合。
- 仅对VLM施加任务掩码但保留动作专家自注意力时（VLA-Adapter + TA + S），合并模型成功率为**0%**；而移除自注意力后，成功率显著回升。这一对照实验直接验证了自注意力是导致合并失败的关键因素。

Table 1还揭示了参数效率的显著优势：MergeVLA合并模型在评估4个任务时所需的总参数量远小于分别部署4个单任务模型的总和。

#### LIBERO-Plus鲁棒性评估

在LIBERO-Plus的7种扰动场景下（背景纹理、相机视角、语言指令、光照条件、物体布局、机器人状态、传感器噪声，见Figure 4），MergeVLA展现出更强的OOD泛化能力：

- **MergeVLA_TIES**在LIBERO-Plus上达到**62.5%的平均成功率**，而OpenVLA单任务微调仅16.3%，提升幅度高达46.2个百分点（Table 2）。
- 移除自注意力并替换为sigmoid门控后，MergeVLA在LIBERO-Plus的OOD泛化成功率比VLA-Adapter高出13.4%。这表明简化动作专家结构不仅使合并成为可能，还增强了模型对分布偏移的鲁棒性——交叉注意力机制更依赖VLM骨干的稳健视觉-语言表征，而非自注意力累积的任务特定偏差。

![[assets/figures/papers/paper_list_l2403_https_arxiv_org_abs_2511_18810/figures/007_Table_2.jpg]]
*Table 2: Robustness of different models under visual and language shifts on LIBERO-Plus. All results are success rates (%) averaged over 4 task suites. Gray-highlighted rows correspond to per-task finetuned checkpoints evaluated on their own tasks, serving as upperbound references for model merging. Shift definitions: S1 – Background Textures; S2 – Camera Viewpoints; S3 – Language Instructions; S4 – Lighting Conditions; S5 – Object Layout; S6 – Robot States; S7 – Sensor Noise*

#### RoboTwin跨具身评估

在RoboTwin的跨具身、跨任务设置中（涉及三种机器人本体和四类操作任务，见Figure 5），MergeVLA同样表现优异：

- **MergeVLA_TIES**（使用H^{(L-1)L}专家头部）在Setting A下达到**88.7%的平均成功率**，甚至略高于单任务微调的88.0%（Table 3）。
- 这一结果表明，MergeVLA的架构设计在跨具身场景下同样有效——合并后的模型不仅能保持各技能的独立能力，还能在不同机器人平台间实现知识共享。

![[assets/figures/papers/paper_list_l2403_https_arxiv_org_abs_2511_18810/figures/009_Table_3.jpg]]
*Table 3: RoboTwin success rates (%) of different variants of MergeVLA across embodiments and tasks*

#### 真实世界SO-101机械臂验证

在真实世界SO-101机械臂的三个立方体操作任务上（见Figure 6），**MergeVLA_TIES**合并模型取得了与单任务模型**完全相同的平均成功率（90.0%）**（Table 4）。这一结果验证了MergeVLA从仿真到真实环境的迁移能力，以及其在实际部署中的可行性。

![[assets/figures/papers/paper_list_l2403_https_arxiv_org_abs_2511_18810/figures/011_Table_4.jpg]]
*Table 4: Real-world SO-101 robot performance, reported as success rates (%) over 20 rollouts per task*

### 消融分析

#### 任务掩码稀疏度λ的影响

掩码比率λ控制着任务掩码的稀疏程度。如Figure 7所示，适中的掩码稀疏度（λ=0.6~0.9）在LIBERO-Long上获得>70%的成功率，而过高或过低的λ值均导致性能下降。λ过低时，掩码过于宽松，无法有效抑制冲突参数；λ过高时，掩码过于激进，可能丢弃对任务有益的共享参数。

#### 动作专家合并策略

消融实验证实了专家头部保留策略的必要性：仅合并浅层动作专家块而保留最终层作为任务特定专家头部是必需的，完全合并所有层导致0%成功率（Table 1中VLA-Adapter + TA + S仍为0%除非排除深层块）。这验证了深层动作专家块已高度任务特化，强行合并会引入不可调和的冲突。

#### 测试时任务路由器的子空间选择

Table 5展示了不同子空间用于任务路由的效果对比。使用价值（V）投影进行任务路由比使用键（K）或查询（Q）投影更可靠：仅V投影在LIBERO上平均成功率达到89.7%，而K或Q投影的性能显著下降。这一发现与价值投影在注意力机制中直接编码特征重要性的角色一致。

#### OpenVLA组件的渐进合并

Figure 8展示了逐步合并OpenVLA语言模型块时的成功率变化：当合并块数超过21个后，成功率崩溃为0。Table 7进一步表明，OpenVLA的不同组件对合并的兼容性差异显著，视觉骨干和语言模型的直接合并均面临严重障碍。这些结果进一步验证了MergeVLA架构重新设计的必要性。

### 失败模式与局限性

尽管MergeVLA在多个基准上表现优异，但仍存在以下局限：

1. **规模限制**：仅在Qwen2.5-0.5B规模的VLM上验证，未在更大规模模型（如7B）上实验。更大规模VLM骨干的合并兼容性仍需验证。
2. **任务类型受限**：实验任务均为短周期物体操作，未涉及导航、移动操作或语言交互等更复杂的具身任务。
3. **参数线性增长**：需要预先为每个任务微调独立的专家模型，合并时需保留所有任务掩码和头部，参数数目随任务数线性增长。如何在不显著增加模型大小的情况下扩展到数十或数百个任务仍是开放问题。
4. **零样本泛化缺失**：任务路由器依赖于已见任务的子空间信息，在训练时未见过的全新任务上无法工作，不具备零样本泛化能力。
5. **任务切换假设**：任务路由器依赖于初始观察进行任务推断，在需要长周期任务切换的操作场景中可能需要额外的重路由机制。

### 补充图表

![[assets/figures/papers/paper_list_l2403_https_arxiv_org_abs_2511_18810/figures/006_Table_1.jpg]]
*Table 1: LIBERO results across task splits. Comparison between finetuned and merged variants of MergeVLA. All numbers are success rates (%). S indicates that task masks are used during merging. “Params (B)” denotes the total number of model parameters (in billions) required to evaluate on all four tasks, including the LLM backbone and the action expert. Gray-highlighted rows correspond to per-task finetuned checkpoints evaluated on their own tasks, serving as upper-bound references for model merging*

![[assets/figures/papers/paper_list_l2403_https_arxiv_org_abs_2511_18810/figures/012_Table_5.jpg]]
*Table 5: Ablation results of MergeVLA with different subspaces used for routing on LIBERO*

![[assets/figures/papers/paper_list_l2403_https_arxiv_org_abs_2511_18810/figures/014_Figure_8.jpg]]
*Figure 8: Success rate on the LIBERO-Spatial task when progressively merging the first k language model blocks of OpenVLA [27] using the Iso-CTS [31] merging algorithm. Each configuration merges four task-specific checkpoints and is evaluated over 10 trials per subtask*

![[assets/figures/papers/paper_list_l2403_https_arxiv_org_abs_2511_18810/figures/004_Figure_4.jpg]]
*Figure 4: Seven perturbation types in the LIBERO-Plus benchmark, used to evaluate robustness under visual and language shifts*

![[assets/figures/papers/paper_list_l2403_https_arxiv_org_abs_2511_18810/figures/005_Figure_5.jpg]]
*Figure 5: Experimental setup in the RoboTwin environment, featuring three robotic embodiments and a suite of manipulation tasks for cross-embodiment evaluation*

![[assets/figures/papers/paper_list_l2403_https_arxiv_org_abs_2511_18810/figures/008_Figure_6.jpg]]
*Figure 6: Setup of the real-world SO-101 arm experiments with three cube manipulation tasks*



## 定位与知识库关联

### 1. 方法脉络与基线关系

MergeVLA 的出发点源于对现有 VLA（Vision-Language-Action）模型合并困境的系统性诊断。其核心发现是：**VLA 模型的不可合并性并非源于模型容量或训练数据不足，而是架构诱导的任务干扰**。这一发现将 MergeVLA 置于模型合并（model merging）与具身智能策略学习的交叉地带，其方法谱系可从两条线索追溯。

**模型合并技术线。** MergeVLA 直接继承并改造了主流的数据无关合并方法。**Task Arithmetic (TA)**（Ilharco et al., ICLR 2023）通过符号向量加法合并任务向量，**TIES-Merging**（Yadav et al., NeurIPS 2023）进一步引入了修剪与符号一致性解决机制，而 **KnOTS**（Stoica et al., ICLR 2025）则利用 SVD 对齐合并空间。这些方法在 NLP 和视觉领域取得了显著成效，但在 VLA 场景下直接应用时表现极差——例如，OpenVLA 仅合并视觉骨干时平均成功率从 76.5% 骤降至 44.2%（Table 1），降幅达 32.3 个百分点。MergeVLA 的贡献在于**识别出 VLA 合并失败的根本原因具有架构特异性**，而非简单地将现有合并方法移植到新领域。

**VLA 架构演进线。** MergeVLA 的架构设计直接对标两类代表性 VLA 模型。**OpenVLA** 采用标准 VLM 进行基于 token 的动作生成，其可训练参数仅限于 LoRA 适配器，理论上应更易合并，但实验表明其语言模型块合并超过 21 个后成功率崩溃为零（Figure 8），揭示了 LoRA 微调中隐藏的灾难性干扰。**VLA-Adapter** 引入包含自注意力和交叉注意力的动作专家模块，虽然提升了单任务性能，但自注意力机制在深层块中累积了不可调和的任务特定差异——Figure 3（右）显示，动作专家在最后几层的相对 L2 距离急剧增大。MergeVLA 通过**移除自注意力层、仅保留交叉注意力**，从根本上消除了这一干扰源。

### 2. 架构决策的因果链

MergeVLA 的设计遵循一条清晰的因果逻辑链，每个组件都直接回应一个经验验证的失败模式：

| 失败模式 | 根因 | MergeVLA 对策 | 证据锚点 |
|---------|------|--------------|---------|
| LoRA 合并冲突 | >75% 参数为单任务独占（自私参数） | 任务掩码稀疏激活（Eq. 2, 3） | Figure 3（左），Section 4.1 |
| 动作专家不可合并 | 自注意力跨层累积任务特定差异 | 仅保留交叉注意力，移除自注意力 | Figure 3（右），Section 4.2 |
| 深层块高度专业化 | 最终层参数空间不可调和 | 保留为任务特定专家头部，不参与合并 | Table 1：完全合并导致 0% 成功率 |
| 推理时任务身份未知 | 需手动指定任务 | 测试时任务路由器（基于价值子空间响应） | Section 4.3，Table 5 |

其中，最具决定性意义的消融证据来自 Table 1：当仅对 VLM 施加任务掩码但保留动作专家自注意力时（VLA-Adapter + TA + S），合并模型成功率为 **0.0%**；而移除自注意力后，成功率显著回升。这直接证明了**自注意力是 VLA 合并的核心障碍，而非 LoRA 适配器本身**。

### 3. 适用边界与局限

MergeVLA 的有效性已在多个维度得到验证，但其适用边界同样清晰：

**已验证的适用范围：**
- **任务类型**：短周期物体操作任务（抓取、放置、推拉等），覆盖 LIBERO（4 个套件，40 个任务）、RoboTwin（跨 3 种具身，4 个任务）和真实世界 SO-101 机械臂（3 个任务）
- **模型规模**：Qwen2.5-0.5B 规模的 VLM 骨干
- **合并方法兼容性**：与 TA、TIES-Merging、WUDI 等合并算法兼容，其中 MergeVLA_TIES 表现最优（LIBERO 平均 90.2%）
- **分布外泛化**：在 LIBERO-Plus 的 7 种视觉和语言扰动下，MergeVLA_TIES 达到 62.5%，比单任务 OpenVLA 微调（16.3%）高出 46.2 个百分点

**明确的局限：**
1. **模型规模未验证**：所有实验均在 0.5B 参数规模的 VLM 上进行，未在更大规模模型（如 7B）上验证架构设计的可扩展性。这构成了一个重要的开放问题：更大的 VLM 骨干是否仍与框架兼容。
2. **任务范围受限**：实验任务均为短周期物体操作，未涉及导航、移动操作或语言交互等更复杂的具身任务。
3. **参数线性增长**：合并过程需保留所有任务掩码和专家头部，参数数目随任务数线性增长。这对于扩展到数十或数百个任务构成实际挑战。
4. **零样本泛化缺失**：任务路由器依赖于已见任务的子空间信息，在训练时未见过的全新任务上无法工作，不具备零样本泛化能力。
5. **增量学习未验证**：合并过程需要所有任务预先完成单次微调，未验证增量学习场景下的持续合并能力。
6. **长周期任务切换**：任务路由器依赖于初始观察，在任务切换的长周期操作中可能需要额外设计。

### 4. 开放问题与未来方向

基于上述局限，MergeVLA 框架指向以下开放问题：

- **规模化验证**：在 7B 及以上规模的 VLM 骨干上验证任务掩码和交叉注意力动作专家的合并有效性，特别是检查大规模模型中自私参数比例是否保持相似特征。
- **预训练数据的影响**：在多样化机器人数据集上进行预训练是否能进一步增强合并效果——这涉及合并前的参数初始化质量对合并兼容性的影响。
- **架构理念的推广**：MergeVLA 的核心洞察——通过架构设计消除干扰源以实现可合并性——能否推广到其他多模态策略模型，如扩散策略（diffusion policy）或基于能量的模型。
- **高效多任务扩展**：如何在不显著增加模型大小的情况下扩展到更多任务（如数十或数百个），可能的路径包括任务掩码共享、专家头部蒸馏或层次化路由策略。
- **任务路由器的鲁棒性**：在任务切换、长时间操作或任务边界模糊的场景下，当前基于初始观察的路由机制可能需要引入时间一致性约束或在线自适应机制。

### 5. 知识库定位

MergeVLA 在知识库中的定位可概括为：**首个系统性地从架构层面解决 VLA 模型合并问题的框架**。其核心知识贡献不在于提出新的合并算法，而在于：

1. **诊断性知识**：揭示了 VLA 微调中 LoRA 适配器的任务独占性（>75% 自私参数）和自注意力机制的跨层干扰是合并失败的根本原因，而非模型容量或数据不足。
2. **架构设计原则**：建立了“通过架构简化实现可合并性”的设计范式——移除自注意力、保留交叉注意力、分离专家头部、稀疏激活合并参数。
3. **实证基准**：提供了 LIBERO、LIBERO-Plus、RoboTwin 和真实世界场景下的全面合并基准，为后续研究建立了评估标准。

与现有工作的关系上，MergeVLA 与 **EMR**（测试时模型合并）等方向互补——前者关注架构层面的合并兼容性，后者关注推理时的动态组合策略。在更广泛的具身智能领域，MergeVLA 为多技能统一策略的学习提供了一条不同于多任务联合训练或持续学习的路径，其“合并优于遗忘”的理念可能影响后续 VLA 架构的设计选择。



## 原文 PDF

![[paperPDFs/CVPR_2026/MergeVLA_Cross_Skill_Model_Merging_Toward_a_Generalist_Vision_Language_Action_Agent.pdf]]
