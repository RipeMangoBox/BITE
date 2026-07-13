---
title: "TwinVLA: Data-Efficient Bimanual Manipulation with Twin Single-Arm Vision-Language-Action Models"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/TwinVLA_Data_Efficient_Bimanual_Manipulation_with_Twin_Single_Arm_Vision_Language_Action_Models.pdf
project_link: https://jellyho.github.io/TwinVLA/
code_link: null
openreview_forum_id: jG9W6nAwVz
aliases:
- TwinVLA
tags:
- ICLR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/vision_models_multimodal
core_operator: "通过复制预训练单臂VLM形成左/右臂分支，并引入联合注意力机制显式进行跨臂信息交换，同时利用MoE高效处理共享输入和注意力重新加权保留预训练知识，从而在无需双臂预训练的情况下仅用少量微调数据即实现高性能双臂协调。"
primary_logic: "将单臂VLA的预训练能力模块化地组合为双臂策略，通过联合注意力实现信息协同，能够大幅降低对双臂数据的依赖，显著提升数据效率与计算效率。"
claims:
- "在真实世界5项长期任务上，TwinVLA平均成功率显著超过同等规模的单体模型RDT-1B，并接近经过大量专有双臂数据训练的π0。"
- "消融实验显示，移除联合注意力机制导致仿真成功率下降4.0%、真实世界下降27.0%，证明跨臂协调是该架构的核心关键。"
- "TwinVLA仅需约800小时公开单臂数据预训练和50条双臂示范微调，而RDT-1B需要约2400小时混合数据，π0需要超10,000小时专有数据。"
- "在Tabletop‑Sim Easy任务上TwinVLA甚至超过了使用大规模双臂预训练的π0。"
---

# TwinVLA: Data-Efficient Bimanual Manipulation with Twin Single-Arm Vision-Language-Action Models

> [!tip] 核心洞察
> 将单臂VLA的预训练能力模块化地组合为双臂策略，通过联合注意力实现信息协同，能够大幅降低对双臂数据的依赖，显著提升数据效率与计算效率。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | TwinVLA：基于双单臂视觉-语言-动作模型的数据高效双臂操作 |
| 英文题名 | TwinVLA: Data-Efficient Bimanual Manipulation with Twin Single-Arm Vision-Language-Action Models |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=jG9W6nAwVz) · [Project](https://jellyho.github.io/TwinVLA/) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/vision_models_multimodal |
| Method | TwinVLA |
| Dataset | 真实世界 Fold towel 任务 Second Fold 子任务, Tabletop-Sim Put X cube into Y pot 多任务, RoboTwin 2.0 平均 Easy |

> [!tip] 效果简介
> - 真实世界 Fold towel 任务 Second Fold 子任务 上，成功率 为 0.90，对比 RDT-1B: 0.45，变化 +0.45。
> - Tabletop-Sim Put X cube into Y pot 多任务 上，成功率 为 0.806，对比 RDT-1B: 0.555，变化 +0.251。
> - RoboTwin 2.0 平均 Easy 上，平均成功率 为 0.420，对比 RDT-1B: 0.345，变化 +0.075。

## 概要

双臂操作（Bimanual Manipulation）要求两个机械臂在空间与时间上紧密协调，但现有的视觉-语言-动作（VLA）模型几乎完全基于单臂数据训练。直接将其扩展为单体双臂模型面临三重瓶颈：**大规模公开双臂数据集极度匮乏**，从零训练整体式策略需要高昂的计算开销，且隐式全局注意力难以有效捕捉双臂间的复杂耦合关系。

TwinVLA 提出了一种**模块化协调范式**：将预训练的单臂 VLA 复制为左/右臂分支，通过联合注意力（Joint Attention）实现跨臂信息交换，并利用混合专家（MoE）机制高效处理共享输入。其核心洞察在于——**将单臂 VLA 的预训练能力模块化地组合为双臂策略，能够大幅降低对双臂数据的依赖，显著提升数据效率与计算效率。**

关键实证结果：
- **数据效率**：仅需约 800 小时公开单臂数据预训练和 50 条目标任务演示微调，远少于 RDT-1B（~2,400h 混合数据）和 π0（>10,000h 专有数据）（Figure 2）。
- **计算效率**：仅需约 25 H100 GPU-days，而 RDT-1B 和 π0 均超过 1,000 H100 GPU-days（Figure 2）。
- **真实世界性能**：在 5 项长期双臂任务上，TwinVLA 平均成功率显著超过同等规模的单体模型 RDT-1B，并接近经大量专有双臂数据训练的 π0（Figure 5）。
- **消融验证**：移除联合注意力导致真实世界成功率下降 27.0%，证明跨臂协调是架构的核心关键（Figure 8b）。

方法定位：TwinVLA 属于**模块化 VLA 组合**方法，区别于整体式双臂 VLA（如 RDT-1B）和大规模专有数据驱动方案（如 π0）。其通过选择性模块复制、联合注意力融合和 MoE 共享处理三个设计原则，在数据与计算双重约束下实现了有竞争力的双臂协调性能。



双臂操作是机器人迈向通用灵巧操作的关键能力。然而，当前主流的视觉-语言-动作（VLA）模型大多基于单臂数据训练，难以有效迁移至双臂场景。其核心瓶颈在于：双臂任务要求左右臂在时空维度上紧密协调，而单臂模型缺乏对跨臂耦合关系的显式建模能力。直接扩展单臂架构至双臂（如整体式VLA）面临双重困境——一方面，大规模公开双臂数据集严重匮乏；另一方面，从头预训练一个整体式双臂模型需要海量双臂数据与计算资源，使其难以在学术或中小规模场景中落地。

现有双臂VLA方法主要沿两条路径探索。一条是以 **RDT-1B**（Liu et al., 2024）为代表的整体式方案，将双臂观察直接输入单一VLM并输出双臂动作。该方法需要融合单臂与双臂数据的联合预训练（约2,400小时），计算开销极大（超过1,000 H100 GPU-days），且由于未显式建模跨臂协调机制，在高度耦合的双臂子任务上表现受限。另一条是以 **π0**（Black et al., 2024）为代表的大规模方案，凭借3.3B参数量和超过10,000小时专有双臂数据取得优异性能，但其数据与计算门槛极高，难以复现和推广。此外，从零训练的非预训练策略（如 **Diffusion Policy**，Chi et al., 2024a）在双臂任务上成功率极低，进一步印证了预训练在双臂场景中的关键作用。

上述现状揭示了一个根本性矛盾：双臂协调的能力需求与双臂数据的稀缺性之间存在巨大鸿沟。本文的核心动机在于回答一个关键问题——**能否将单臂VLA的预训练能力模块化地组合为双臂策略，从而大幅降低对双臂数据的依赖？** 这一思路的直觉来源是人类双臂协调的认知机制：人类并非学习一个“整体式双臂控制器”，而是通过左右臂各自的能力基础，配合跨臂信息交换来实现协调。TwinVLA正是基于这一洞察，提出通过复制预训练单臂VLA形成左右臂分支，并引入联合注意力机制实现跨臂协同，从而在无需任何双臂预训练的条件下，仅用少量微调数据即达到有竞争力的双臂操作性能。



## 核心方法与创新机理

TwinVLA的核心创新在于将双臂操作问题**解耦为“单臂预训练能力复制 + 跨臂协调注入”**的模块化组合范式，而非从头构建整体式双臂模型。这一设计直接回应了领域核心瓶颈：大规模双臂数据极度稀缺，而直接扩展单臂模型又难以有效捕捉双臂间的复杂耦合关系。

### 关键创新点

**1. 模块化双臂架构：复制而非重建**

TwinVLA通过复制预训练单臂VLA形成左/右臂专用分支，而非像**RDT-1B**（Liu et al., 2024）那样构建单体式双臂策略。具体而言，视觉编码器和DiT动作头在双臂间共享，而VLM骨干网络被完整复制为两个独立分支，分别负责对应机械臂的高级决策。这一设计使得模型规模的增长最小化，同时完整保留了单臂预训练中积累的跨具身操作知识。

**2. 联合注意力：显式跨臂信息融合**

与基线方法依赖隐式全局注意力或无显式融合机制不同，TwinVLA引入**联合注意力（Joint Attention）**机制，通过共享左右VLM骨干的自注意力层实现对称的跨臂信息交换。配合因果掩码设计，该机制在保持时序因果性的同时，让左右臂能够并行处理共享输入（语言指令、自我中心视图）和臂专属输入，从而显式地协调双臂动作。消融实验表明，移除联合注意力导致仿真成功率下降4.0%、真实世界成功率大幅下降27.0%，证明跨臂协调是该架构的核心关键。

**3. MoE共享输入处理：计算效率与性能兼得**

共享输入（如自我中心视图、语言指令）若在每个臂分支独立编码会造成显著计算冗余。TwinVLA采用**混合专家（Mixture-of-Experts, MoE）**机制动态路由共享令牌：通过一个可学习的路由器将共享输入加权分配到左右VLM专家的前馈网络（FFN），输出经加权合成后送入后续层。这一设计使显存占用减少约21%，同时消融实验显示移除MoE不仅增加显存开销，还导致仿真成功率微降1.1%、真实世界下降5.0%。

**4. 注意力重新加权：保留预训练知识**

直接引入双臂专属令牌会稀释共享输入在注意力分布中的权重，破坏预训练阶段建立的表征。TwinVLA提出**注意力重新加权（Attention Re-weighting）**策略：在联合注意力计算后，将共享模态令牌对应的注意力权重加倍后重新归一化，使得预训练时的注意力分布得以保留。实验显示，该机制使初始微调损失降低约40%，移除后真实世界成功率下降4.0%，证明其有助于快速适应新任务并保留预训练知识。

### 与基线的本质差异

| 设计维度 | RDT-1B / π0 | TwinVLA |
|---------|------------|---------|
| 策略架构 | 单体VLM直接输出双臂动作 | 复制单臂VLM形成双分支 + 联合注意力协调 |
| 跨臂融合 | 无显式融合或隐式全局注意力 | 显式共享自注意力层 + 因果掩码 |
| 共享输入处理 | 每分支独立编码，计算冗余 | MoE动态路由，减少21%显存 |
| 注意力分布 | 引入双臂令牌后注意力被稀释 | 注意力重新加权，初始损失降低40% |
| 预训练数据 | 需融合单臂与双臂的大规模联合预训练（RDT-1B约2400小时） | 仅需约800小时公开单臂数据预训练，无需双臂预训练 |

### 数据与计算效率的根本性提升

TwinVLA仅需约800小时公开单臂数据集预训练SingleVLA，再通过50条目标双臂任务示范进行微调，而RDT-1B需要约2400小时混合数据，**π0**（Black et al., 2024）则需要超过10,000小时专有数据。在计算资源方面，TwinVLA仅需约25 H100 GPU-days，而RDT-1B和π0均超过1000 H100 GPU-days。这一效率提升源于模块化设计：单臂预训练能力被完整继承，微调阶段仅需学习跨臂协调这一增量能力。



![[assets/figures/papers/paper_list_l8_https_openreview_net_forum_id_jG9W6nAwVz/figures/001_Figure_1.jpg]]
*Figure 1: Overview of TwinVLA. Inspired by humans’ two-arm coordination for bimanual manipulation, TwinVLA duplicates a VLM backbone pretrained on cross-embodiment single-arm data (Left) to form two arm-specific branches linked via Joint Attention (Right). Shared inputs (ego-centric views, language instructions) are routed via a mixture-of-experts (MoE) to improve computational efficiency. Only the VLM backbone is duplicated, keeping the increase in model size minimal*

![[assets/figures/papers/paper_list_l8_https_openreview_net_forum_id_jG9W6nAwVz/figures/005_Figure_3.jpg]]
*Figure 3: (a) Causal attention mask for joint attention. It preserves causality while processing shared, left, and right inputs in parallel. (b) TwinVLA joint attention mechanism. The two VLMs share information, and the shared modality ( l , $I _ { \mathrm { e g o } } ) _ { t }$ t is further processed by MoE to more efficiently leverage both VLMs*

TwinVLA 的核心设计理念是将预训练的单臂 VLA 能力模块化地组合为双臂协调策略，而非从头训练一个整体式的双臂模型。其整体框架遵循“选择性复制—跨臂融合—高效共享”三条原则。

**输入层**：系统接收共享的自我中心视图和语言指令，同时为左右臂分别采集腕部视图和本体感知信号。共享视觉编码器处理所有图像输入，每臂配备独立的轻量级本体感知编码器。

**核心架构**：将在大规模跨具身单臂数据上预训练的 VLM 骨干完整复制为两个分支，分别负责左臂和右臂的高级决策。这两个分支通过**联合注意力（Joint Attention）** 机制实现信息交换——仅共享自注意力层，配合因果掩码在保持时序因果性的同时并行处理共享、左臂、右臂三类令牌。共享输入（语言、自我中心视图）通过**混合专家（MoE）** 机制动态路由：由路由器计算权重，将令牌分发到左右 VLM 专家的前馈网络，再按权重合成输出，避免在每个分支独立编码造成的计算冗余。

**输出层**：共享的 DiT 动作头接收 VLM 输出与本体感知，基于条件流匹配目标预测双臂动作块。推理时通过前向欧拉积分迭代更新动作序列。

**注意力重新加权**：在联合注意力计算后，对共享模态令牌的注意力权重加倍并重新归一化，以抵消令牌数量增加导致的注意力稀释，保留预训练阶段习得的注意力分布。

整个流程可概括为：共享编码 → 双分支 VLM 联合推理（MoE 处理共享令牌 + 联合注意力跨臂交互）→ 共享动作头解码 → 双臂动作块输出。仅复制 VLM 骨干，视觉编码器和动作头保持共享，使模型参数量增加最小化。



TwinVLA 的核心架构由三个设计原则驱动：选择性模块复制、跨臂信息融合、以及共享输入的高效处理。以下逐一展开其关键模块与支撑公式。

### 选择性模块复制

TwinVLA 并非从头构建一个整体式双臂策略网络，而是将预训练好的单臂 VLA 模型复制为左、右臂两个分支。具体而言，视觉编码器（Vision Encoder）与 DiT 动作头（Action Head）在双臂间共享，而 VLM 主干网络则完全复制为两份。这一设计的动机在于：视觉特征提取与最终动作解码对双臂具有通用性，而高层语义决策需要为每只手臂保留独立的推理空间。该策略在仅引入约 30% 额外参数的情况下，最大程度复用了单臂预训练知识。

### 联合注意力机制

跨臂协调是 TwinVLA 区别于简单模型堆叠的核心。这一能力通过**联合注意力**实现：将左、右臂 VLM 中的自注意力层共享，使两个分支在每一层都能对称地交换信息。其计算形式为标准缩放点积注意力，但引入了一个特殊的因果掩码，使得共享令牌、左臂令牌、右臂令牌能够在保持时序因果性的前提下并行处理：

$$S \leftarrow \mathrm{Softmax}(QK^T/\sqrt{d_k}) + M$$

其中 $M$ 为因果联合注意力掩码，确保共享输入（语言指令、自我中心视图）可以关注所有历史信息，而左、右臂的专有令牌只能关注自身及共享令牌的历史，从而避免信息泄露并保持推理时的自回归特性。

### 注意力重新加权

直接引入双臂令牌会导致共享输入（如语言指令、自我中心图像）在注意力分布中被稀释，破坏预训练阶段学习到的注意力模式。为解决这一问题，TwinVLA 在联合注意力计算后，对共享模态对应的注意力权重进行加倍，然后重新归一化。这一操作使模型在微调初期能够保留预训练的注意力分布，实验表明初始微调损失降低了约 40%。

### 混合专家路由

共享输入（语言指令、自我中心视图）若在左、右臂分支中独立编码，会造成显著的计算冗余。TwinVLA 采用混合专家机制来高效处理这些共享令牌：将共享令牌作为单一序列输入，由一个轻量级路由器动态计算权重，然后分别送入左、右 VLM 的 FFN 专家进行处理，最终加权合成输出：

$$\mathbf{MoE}(x) = w_{\mathrm{left}} \cdot \mathrm{FFN}_{\mathrm{left}}(x) + (1 - w_{\mathrm{left}}) \cdot \mathrm{FFN}_{\mathrm{right}}(x)$$

这一输出平均策略借鉴了任务算术的思想，在不物理合并参数的情况下模拟了共享层的效果，使显存占用降低约 21%。

### 条件流匹配动作头

动作头采用基于 DiT 的流匹配架构，接收 VLM 输出的隐变量 $h_t$ 与本体感知 $d_t$，预测从噪声动作块到目标动作块的参考流。训练目标为条件流匹配损失：

$$\mathcal{L}^T(\theta) = \mathbb{E}_{p(A_t \mid o_t), q(A_t^\tau \mid A_t)} \| v_\theta(A_t^\tau, h_t, d_t) - \mathbf{u}(A_t^\tau \mid A_t) \|^2$$

其中 $A_t$ 为目标动作块，$A_t^\tau$ 为在时间 $\tau$ 处的加噪动作块，$\mathbf{u}(A_t^\tau \mid A_t)$ 为从 $A_t^\tau$ 指向 $A_t$ 的真实条件流。推理时，通过前向欧拉积分迭代更新动作：

$$A_t^{\tau + \delta} = A_t^\tau + \delta v_\theta(A_t^\tau, h_t, d_t)$$

步长 $\delta = 1/n$，论文中取 $n=10$，从随机噪声逐步去噪生成最终的双臂动作序列。



## 实验与关键发现

### 核心性能对比

TwinVLA在真实世界与仿真基准上均展现出显著的数据效率与性能优势。在真实世界5项长期任务中，TwinVLA平均成功率大幅超越同等规模的单体双臂VLA模型**RDT-1B**（Liu et al., 2024），并接近使用超过10,000小时专有双臂数据预训练的3.3B参数模型**π0**（Black et al., 2024）的性能水平（Figure 5）。这一结果的核心驱动力在于：TwinVLA仅需约800小时公开单臂数据预训练和50条目标任务示范微调，而RDT-1B需要约2,400小时混合数据，π0则需要超10,000小时专有数据（Figure 2a），数据需求降低一个数量级以上。

![[assets/figures/papers/paper_list_l8_https_openreview_net_forum_id_jG9W6nAwVz/figures/003_Figure_2.jpg]]
*Figure 2: (a) Data efficiency. TwinVLA requires only ∼ 800h of single-arm and 50 episodes of target bimanual data, significantly less than RDT-1B (∼ 2, 400h) and π0 (∼ 10, 900h) in total. (b) Compute efficiency. RDT-1B and $\pi _ { 0 }$ require high compute (exceeding 1, 000 H100 GPU-days), whereas TwinVLA achieves higher or comparable performance with only 25 H100 GPU-days*

![[assets/figures/papers/paper_list_l8_https_openreview_net_forum_id_jG9W6nAwVz/figures/017_Figure_5.jpg]]
*Figure 5: Success rates on real-world tasks. TwinVLA outperforms RDT-1B and DP on average. Moreover, TwinVLA shows comparable performance with π0 while trained only on target data*

在Tabletop‑Sim仿真基准上，TwinVLA在多数任务中超越RDT-1B，甚至在Easy任务上超过了π0（Figure 6）。具体而言，在“Put X cube into Y pot”多任务上，TwinVLA成功率达0.806，较RDT-1B的0.555提升25.1个百分点（Table 9）。在真实世界“Fold towel”任务的“Second Fold”子任务中，TwinVLA成功率达0.90，而RDT-1B仅为0.45（Table 7），差距达45个百分点，凸显了跨臂协调机制在精细操作中的关键作用。

![[assets/figures/papers/paper_list_l8_https_openreview_net_forum_id_jG9W6nAwVz/figures/046_Table_9.jpg]]
*Table 9: Performance comparison on the Tabletop-Sim benchmark*

计算效率方面，TwinVLA仅需约25 H100 GPU‑days完成全流程训练，而RDT-1B和π0均需超过1,000 H100 GPU‑days（Figure 2b），计算成本降低约40倍，同时性能持平或更优。

### 消融实验：关键设计的作用机制

消融实验（Figure 8b）系统验证了TwinVLA各核心组件的因果贡献：

![[assets/figures/papers/paper_list_l8_https_openreview_net_forum_id_jG9W6nAwVz/figures/022_Figure_8.jpg]]
*Figure 8: Language following task and ablation results. (a) We evaluate average success rates on the language following tasks in the real world and Tabletop-Sim. (b) Ablation studies in the real world and Tabletop-Sim Easy tasks*

- **联合注意力（Joint Attention）**：移除该机制导致仿真成功率下降4.0%，真实世界成功率骤降27.0%，是跨臂协调的核心瓶颈。这一结果表明，简单的并行单臂策略无法隐式习得双臂耦合，显式的跨臂信息交换是不可或缺的因果开关。
- **MoE集成**：移除MoE后显存占用增加21%，同时仿真成功率微降1.1%、真实世界下降5.0%。这说明MoE不仅提升了计算效率，还通过动态路由保留了左右臂专家的互补能力，实现了效率与性能的兼得。
- **注意力重新加权**：移除该机制使初始微调损失增加约40%，最终成功率微降（仿真1.1%，真实4.0%）。该设计通过缩放共享输入的注意力权重并重新归一化，有效缓解了引入双臂令牌后注意力分布偏移的问题，帮助模型快速适应并保留预训练知识。
- **单臂预训练**：从零训练（Scratch）导致真实世界成功率大幅下降46.0%，验证了单臂预训练是TwinVLA数据高效性的根基。

### 挑战场景与鲁棒性

在低光照和存在干扰物的挑战场景下，TwinVLA展现出优于RDT-1B的鲁棒性（Table 1）。在低光照条件下，TwinVLA成功率达45.0%，显著高于RDT-1B；但在强干扰物场景中，π0仍保持优势，表明TwinVLA在极端分布偏移下的泛化能力尚有提升空间。

![[assets/figures/papers/paper_list_l8_https_openreview_net_forum_id_jG9W6nAwVz/figures/020_Table_1.jpg]]
*Table 1: Comparison of success rates for the Fold towel task in challenging scenes*

### 失败模式与局限性

TwinVLA的主要失败模式集中在以下方面：首先，双臂视觉差异与单臂预训练分布不一致导致泛化受限，在RoboTwin Hard等环境变化剧烈的任务上未能超越π0；其次，采用绝对末端执行器位姿控制可能限制了适用场景的多样性。这些失败案例指向两个开放问题：如何通过相对动作表示或共享表征提升迁移效率，以及该模块化协调范式能否扩展至更多臂或异构机器人系统。

### 补充图表

![[assets/figures/papers/paper_list_l8_https_openreview_net_forum_id_jG9W6nAwVz/figures/024_Table_2.jpg]]
*Table 2: SingleVLA pretraining datasets and sampling percentages*

![[assets/figures/papers/paper_list_l8_https_openreview_net_forum_id_jG9W6nAwVz/figures/025_Table_3.jpg]]
*Table 3: Key hyperparameters for TWINVLA training*

![[assets/figures/papers/paper_list_l8_https_openreview_net_forum_id_jG9W6nAwVz/figures/026_Table_4.jpg]]
*Table 4: Performance of different VLMs on LIBERO*

![[assets/figures/papers/paper_list_l8_https_openreview_net_forum_id_jG9W6nAwVz/figures/027_Table_5.jpg]]
*Table 5: Performance of pretrained SingleVLA on LIBERO*

![[assets/figures/papers/paper_list_l8_https_openreview_net_forum_id_jG9W6nAwVz/figures/028_Table_6.jpg]]
*Table 6: Training hyperparameters for baseline models*



## 定位与知识库关联

### 基线关系与定位

TwinVLA 的核心贡献在于提出了一种**模块化的双臂协调范式**，其直接对比基线包括：

- **RDT-1B**（Liu et al., 2024）：同等规模（1.2B）的整体式双臂 VLA，直接从融合单臂与双臂的数据中联合预训练，作为 TwinVLA 的直接对标基线。TwinVLA 在真实世界 5 项长期任务上的平均成功率显著超过 RDT-1B，尤其在 Fold towel 的 Second Fold 子任务上领先 45 个百分点（0.90 vs 0.45）。在 Tabletop-Sim 多任务基准上，TwinVLA 的平均成功率达 0.806，较 RDT-1B 的 0.555 提升 25.1 个百分点。

- **π0**（Black et al., 2024）：3.3B 参数的大规模 VLA，使用超过 10,000 小时的专有双臂数据进行预训练，论文将其定位为**性能上界**而非完全对等比较。TwinVLA 在仅使用约 800 小时公开单臂数据预训练和 50 条目标任务示范微调的条件下，在 Tabletop‑Sim Easy 任务上甚至超过了 π0，在真实世界任务上展现出与其可比拟的性能。

- **Diffusion Policy (DP)**（Chi et al., 2024a）：从零训练的非预训练策略，用于验证预训练的关键作用。消融实验中，从零训练（Scratch）的变体导致真实世界成功率大幅下降 46.0%，确证了单臂预训练对于 TwinVLA 性能的基础性贡献。

TwinVLA 的方法谱系定位可概括为：**将预训练单臂 VLA 的能力模块化地组合为双臂策略，通过联合注意力实现信息协同**。这与 RDT-1B 的整体式联合预训练范式形成根本差异——TwinVLA 无需任何双臂预训练数据，仅需约 800 小时公开单臂数据预训练 SingleVLA，再通过 50 条目标任务示范微调，而 RDT-1B 需要约 2,400 小时的混合数据。在计算效率上，TwinVLA 仅需约 25 H100 GPU-days，而 RDT-1B 和 π0 均超过 1,000 H100 GPU-days，TwinVLA 在显著降低计算开销的同时实现了更高或可比拟的性能。

### 适用边界与局限

尽管 TwinVLA 在数据效率与计算效率上展现出显著优势，其适用边界和局限性同样明确：

1. **视觉分布偏移下的泛化受限**：由于双臂视角与单臂预训练数据分布存在差异，TwinVLA 在极端环境变化下的鲁棒性不足。在 RoboTwin Hard 任务上，TwinVLA 未能超越 π0，表明在强分布偏移场景下，仅依赖单臂预训练知识的模块化组合仍存在性能天花板。

2. **动作表示的适用场景限制**：TwinVLA 采用绝对末端执行器位姿控制，这一设计可能限制其在需要相对动作表示或更灵活控制策略的场景中的适用性。

3. **微调数据量的性能天花板**：TwinVLA 的微调仅使用 50 条目标任务演示，虽然展示了数据高效性，但在某些复杂任务上可能存在性能天花板。随着微调数据量从 20 条增至 50 条，性能持续提升，但数据量进一步增加的边际收益尚不明确。

### 开放问题

TwinVLA 的模块化协调范式为双臂操作开辟了若干值得探索的方向：

- **双臂视觉差异的弥合**：如何解决因双臂视角差异导致的泛化能力受限，是提升模型鲁棒性的关键。可能的路径包括域自适应视觉编码或双臂共享的视角归一化策略。

- **动作表示的迁移效率**：相对动作表示或共享表征能否进一步提升从单臂到双臂的迁移效率，是一个开放的设计选择问题。

- **模块化范式的可扩展性**：TwinVLA 的“复制+联合注意力”范式是否适用于更多机械臂（三臂及以上）或异构机器人系统（如臂-手协同、移动操作），其扩展时的注意力复杂度和协调机制设计值得进一步研究。

- **预训练知识的保留与适应平衡**：注意力重新加权机制使初始微调损失降低约 40%，但如何在更广泛的微调数据量和任务多样性下保持预训练知识的有效保留，仍需系统性的探索。



## 原文 PDF

![[paperPDFs/ICLR_2026/TwinVLA_Data_Efficient_Bimanual_Manipulation_with_Twin_Single_Arm_Vision_Language_Action_Models.pdf]]
