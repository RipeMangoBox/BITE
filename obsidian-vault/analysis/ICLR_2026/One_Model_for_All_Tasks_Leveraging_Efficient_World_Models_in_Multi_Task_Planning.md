---
title: "One Model for All Tasks: Leveraging Efficient World Models in Multi-Task Planning"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/One_Model_for_All_Tasks_Leveraging_Efficient_World_Models_in_Multi_Task_Planning.pdf
project_link: null
code_link: https://github.com/opendilab/LightZero
openreview_forum_id: iU026Hr90y
aliases:
- SDPSD
- OMATLEWMMTP
tags:
- ICLR_2026
- topic/reinforcement_learning_planning_agents
- topic/reinforcement_learning_planning_agents/planning_control
core_operator: "关键可控因素是模型架构中的骨干网络类型——将密集Transformer替换为稀疏混合专家（MoE）骨干，通过任务特定路由将计算分散到专门子网络，从而从根本上抑制梯度冲突；同时，训练层面的动态参数扩展（DPS）策略通过自适应注入LoRA适配器来按需分配模型容量。"
primary_logic: "MoE的条件计算机制具有比密集网络更低的梯度冲突理论上界，并通过专家专业化有效地隔离了不同任务的梯度更新，从而保护了模型的可塑性；DPS通过冻结已学参数、仅当前阶段新增适配器可训练的方式，既保留了先前知识又为未完成任务提供了定向可塑性，显著提升了样本效率。"
claims:
- "可塑性崩溃是统一世界模型在多任务训练中的根本失效模式：复杂任务性能倒塌同休眠神经元比率激增和隐状态范数膨胀在时间上严格同步。"
- "在Atari8多任务消融实验中，将Transformer骨干替换为MoE是唯一能显著且一致提升性能的架构改动，其他干预仅带来边缘收益。"
- "单一ScaleZero多任务代理在Atari 100k基准上的Human-Normalized Score均值（0.39）超过了26个单任务UniZero代理的均值（0.38），证明多任务学习实现了正向迁移。"
- "DPS策略在DMControl基准上使环境交互成本降低了约28.5%，同时达到了与标准ScaleZero相当的性能。"
---

# One Model for All Tasks: Leveraging Efficient World Models in Multi-Task Planning

> [!tip] 核心洞察
> MoE的条件计算机制具有比密集网络更低的梯度冲突理论上界，并通过专家专业化有效地隔离了不同任务的梯度更新，从而保护了模型的可塑性；DPS通过冻结已学参数、仅当前阶段新增适配器可训练的方式，既保留了先前知识又为未完成任务提供了定向可塑性，显著提升了样本效率。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 一个模型应对所有任务：利用高效世界模型进行多任务规划 |
| 英文题名 | One Model for All Tasks: Leveraging Efficient World Models in Multi-Task Planning |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=iU026Hr90y) · [GitHub](https://github.com/opendilab/LightZero) |
| Topic | #topic/reinforcement_learning_planning_agents #topic/reinforcement_learning_planning_agents/planning_control |
| Method | ScaleZero + Dynamic Parameter Scaling (DPS) |
| Dataset | Atari 100k (26 games), DMControl (18 tasks), Jericho Zork1, Jericho Detective |

> [!tip] 效果简介
> - Atari 100k (26 games) 上，Human-Normalized Score (Mean) 为 0.39，对比 0.38 (UniZero ST)，变化 +0.01。
> - DMControl (18 tasks) 上，Raw Score (Median) 为 887.3，对比 875.1 (UniZero ST)，变化 +12.2。
> - Jericho Zork1 上，Average Return 为 44，对比 38.0 (CALM+OC)，变化 +6.0。

## 概要

多任务强化学习的核心挑战在于：当用一个统一世界模型同时学习多个异质任务时，模型的可塑性会灾难性崩溃——复杂任务的性能在训练后期急剧下降，同时伴随休眠神经元比率激增和隐状态范数膨胀。本文针对这一瓶颈，提出**ScaleZero**，其关键创新在于将密集Transformer骨干替换为**稀疏混合专家（MoE）架构**，通过任务特定路由将计算分散到专门子网络，从根本上抑制梯度冲突。在此基础上，进一步引入**动态参数扩展（DPS）策略**，通过自适应注入LoRA适配器实现按需容量分配，在保持性能的同时显著降低环境交互成本。

在Atari 100k基准上，单一ScaleZero多任务代理的人类归一化得分均值（0.39）超越了26个单任务UniZero代理的均值（0.38），证明多任务学习实现了正向迁移。在DMControl连续控制基准上，ScaleZero-DPS以约28.5%的环境交互量削减达到了与标准ScaleZero相当的性能。方法的核心洞察在于：MoE的条件计算机制具有比密集网络更低的梯度冲突理论上界，并通过专家专业化有效隔离了不同任务的梯度更新，从而保护了模型的可塑性。



### 多任务强化学习的统一世界模型瓶颈

基于模型的强化学习（MBRL）通过让智能体学习环境的世界模型，在样本效率上展现出巨大潜力。近年来，统一世界模型（如UniZero）试图将这种能力扩展到多任务场景——用一个共享模型同时学习多个任务的动力学、奖励和策略。然而，这一范式面临一个根本性挑战：**可塑性崩溃（plasticity collapse）**。

Figure 1 清晰地揭示了这一失效模式。在Atari8多任务基准上，单一UniZero模型同时训练八个游戏时，简单任务（如Pong和Hero）表现稳定，但复杂任务（如Seaquest和ChopperCommand）在训练后期（约150K-200K步后）遭遇灾难性性能崩塌。这一外部性能崩溃与两个内部表征指标在时间上严格同步：（1）Transformer骨干中**休眠神经元比率（Dormant Neuron Ratio）急剧飙升**，表明网络有效容量萎缩；（2）**隐状态范数（Latent State Norm）失控膨胀**，暗示表征空间退化。这两个信号共同指向同一个根本原因：异构任务间的梯度冲突和表征干扰导致网络丧失了对新信息的适应能力。

### 现有方法的缺口：梯度冲突与表征干扰

多任务强化学习中，来自不同任务的梯度在共享参数空间中相互干扰，形成**梯度冲突**（gradient conflict）——当两个任务的梯度方向余弦相似度为负时，一个任务的学习会直接损害另一个任务的性能。在密集Transformer骨干中，所有任务共享同一组参数，梯度冲突无结构约束地传播，最终导致网络陷入一种“僵化”状态：大部分神经元对任何输入都近乎无响应，模型丧失可塑性。

UniZero尝试通过SimNorm（基于L1的单纯形投影归一化）和MoCo梯度校正来稳定训练，但这些干预仅提供边际收益。Figure 3的消融实验表明，SimNorm虽然能稳定训练过程，但其硬约束削弱了表征表达能力，导致最终性能次优；而原始的任务嵌入（naive task embeddings）未能显著改善性能，推测是缺乏约束导致嵌入在训练后期崩溃。这些发现表明，**仅靠训练层面的修补无法从根本上解决密集共享骨干中的梯度冲突问题**。

### 本文动机：从架构根源重塑多任务世界模型

上述分析引导出一个核心洞察：要真正解决可塑性崩溃，必须从架构层面重新设计模型的计算结构。本文的动机由此展开——**用稀疏混合专家（MoE）骨干替代密集Transformer，通过任务特定路由将计算分散到专门子网络，从根本上抑制梯度冲突**。同时，在训练层面引入动态参数扩展（DPS）策略，通过自适应注入LoRA适配器来按需分配模型容量，实现知识保留与定向可塑性的平衡。这一双重设计旨在构建一个真正能“一个模型应对所有任务”的统一世界模型架构。



## 核心方法与创新机理

### 问题根源：可塑性崩溃的发现

ScaleZero 的核心创新源于对多任务统一世界模型失效模式的根本性诊断。论文发现，当使用单一密集 Transformer 骨干同时训练多个异构任务时，模型会遭遇 **可塑性崩溃（plasticity collapse）**——复杂任务（如 Seaquest、ChopperCommand）的性能在训练后期发生灾难性衰退，而简单任务（如 Pong、Hero）保持稳定（Figure 1）。

这种崩溃并非偶然，而是与内部学习动力学的恶化精确同步：
- **休眠神经元比率激增**：Transformer 层中激活幅度低于阈值 $\epsilon$ 的神经元比例急剧上升，表明网络丧失了对新信息的响应能力。
- **隐状态范数膨胀**：潜在表征的范数失控增长，反映了梯度冲突导致的表征退化。

这一诊断将多任务世界模型的核心瓶颈从“容量不足”重新定义为“**梯度冲突引发的可塑性丧失**”，为后续架构设计提供了明确靶点。

### 架构层创新：MoE 骨干替代密集 Transformer

针对可塑性崩溃，ScaleZero 在 UniZero 设计空间中进行了系统性消融（Figure 2a），发现最关键的架构改动是将密集 Transformer 骨干替换为 **稀疏混合专家（MoE）Transformer**。

MoE 骨干由 1 个共享专家和 8 个路由专家组成，采用 top-1 门控机制，通过条件计算将不同任务的表征路由到专门子网络。这一设计的有效性源于两个层面：

1. **梯度冲突的理论上界更低**：定理分析表明，全层 MoE 的梯度冲突上界为
   $$\text{conflict}(\tilde{G}_{t_1}, \tilde{G}_{t_2}) \leq G \cdot \cos(u, v) \leq G$$
   其中 $G$ 为单专家冲突上界。稀疏路由通过任务特定权重分配，可将实际冲突严格限制在远低于密集网络的水平。

2. **专家专业化隔离梯度更新**：不同任务通过门控网络分配到不同专家组合，使梯度更新在参数空间中自然解耦，从根本上抑制了跨任务干扰。

消融实验（Figure 3）提供了决定性证据：在 Atari8 多任务基准上，仅将骨干改为 MoE 即带来显著且一致的性能提升，而其他干预（任务嵌入、ViT 编码器、SimNorm 归一化、MoCo 梯度校正）仅提供边际收益。SimNorm 虽能稳定训练，但其硬约束削减了表征表达能力，导致最终性能次优；朴素任务嵌入则因缺乏约束而在训练后期崩溃。

### 训练层创新：动态参数扩展（DPS）

在 MoE 解决架构层面可塑性问题的基础上，ScaleZero 进一步提出了 **动态参数扩展（Dynamic Parameter Scaling, DPS）** 策略，从训练调度层面提升样本效率。

DPS 包含两个协同机制：

- **自适应任务筛选**：根据实时回报反馈动态调整活跃任务集，将计算资源集中于尚未解决的任务，避免在已收敛任务上浪费交互。
- **渐进式容量扩展**：当学习进展停滞时，通过注入 LoRA 适配器分阶段扩展模型容量。关键设计是**参数隔离**：进入新阶段后，冻结所有先前学习的参数（骨干 $W_0$ 及已有适配器 $\{\Delta\theta_j\}_{j=1}^{s-1}$），仅训练当前阶段新增的适配器。第 $s$ 阶段的有效权重为：
  $$W^{(s)} = \alpha_0 W_0 + \sum_{j=1}^{s} \alpha_j B_j A_j$$
  其中 $\alpha_j$ 为可学习的缩放因子。

这种设计既保留了已学知识，又为未完成任务提供了定向可塑性。实验表明，DPS 使 ScaleZero 在 DMControl 基准上以仅 71.5% 的环境交互量达到与标准 ScaleZero 相当的性能（Figure 4），交互成本降低约 28.5%。

### 辅助改进：ViT 编码器与 LayerNorm

除上述两个核心创新外，ScaleZero 还引入了两项辅助改进（Table 3）：
- **视觉编码器**：将 UniZero 的 ResNet 风格编码器替换为从头训练的 Vision Transformer（ViT），提升特征提取的可扩展性。
- **潜在归一化**：将 SimNorm（基于 L1 的单纯形投影）替换为标准 LayerNorm，在保持训练稳定性的同时释放表征表达能力。

消融实验确认，这两项改动单独使用仅带来边际收益，其价值主要体现在与 MoE 骨干的协同作用中。



![[assets/figures/papers/paper_list_l16_https_openreview_net_forum_id_iU026Hr90y/figures/002_Figure_2.jpg]]
*Figure 2: (a) Design Space of UniZero for Multitask learning*

![[assets/figures/papers/paper_list_l16_https_openreview_net_forum_id_iU026Hr90y/figures/010_Table_3.jpg]]
*Table 3: Summary of core architectural differences between UniZero and ScaleZero*

ScaleZero 的整体框架围绕一个核心命题展开：如何构建一个统一的世界模型，使其在多个异构任务上训练时，既能避免灾难性的可塑性崩溃，又能实现正向迁移。其 pipeline 由三个顺序耦合的模块构成，形成从原始观测到决策输出的端到端流。

### 模块化 Pipeline

1.  **视觉编码器（ViT）**：接收原始像素观测，将其编码为隐状态表征。与 UniZero 使用的 ResNet 类编码器不同，ScaleZero 采用从零训练的 Vision Transformer（ViT），以提供更强的可扩展特征提取能力（Table 3）。
2.  **MoE Transformer 骨干**：这是整个框架的核心。隐状态表征进入由混合专家层构成的 Transformer 骨干，通过稀疏条件计算在隐空间内完成四项关键预测：下一状态、奖励、策略与价值。MoE 的稀疏路由机制（top‑1 gating，1 个共享专家 + 8 个路由专家）将不同任务的计算分散到专门子网络，从根本上抑制梯度冲突，这是防止可塑性崩溃的关键。
3.  **任务特定预测头**：骨干输出的表征被送入各任务独立的预测头，分别输出策略、价值和奖励。由于不同任务的动作空间各异（如 Atari 的离散动作与 DMControl 的连续控制），预测头针对每个任务单独设计，处理动作空间的异构性。

### 训练层面的动态扩展：DPS

在静态架构之上，ScaleZero 引入了**动态参数扩展（Dynamic Parameter Scaling, DPS）**策略作为训练层面的补充。DPS 并非替换上述模块，而是通过分阶段注入 LoRA 适配器来动态调整模型容量。其核心机制是参数隔离：当进入新阶段时，所有先前学习的参数（骨干权重和旧适配器）被冻结，仅新注入的 LoRA 适配器可训练。这使得模型既能保留已有知识，又能为未完成任务提供定向可塑性，从而在不牺牲性能的前提下将环境交互成本降低约 28.5%（Figure 4）。

### 输入输出流

整个 pipeline 的输入是来自多个任务环境的原始观测（图像或文本），输出是各任务对应的策略、价值估计和奖励预测。训练信号来自统一的复合损失函数，该函数在长度为 $H$ 的上下文上同时优化价值、策略、奖励和下一状态预测：

$$\mathcal{L}_{\mathrm{Unified}} = \sum_{t=0}^{H-1} \left( \mathcal{L}_{\mathrm{value}}(v_t, \hat{v}_t^{target}) + \mathcal{L}_{\mathrm{policy}}(p_t, \pi_t) + \mathcal{L}_{\mathrm{reward}}(\hat{r}_t, r_t) + \mathcal{L}_{\mathrm{dynamics}}(\hat{z}_{t+1}, \mathrm{sg}(z_{t+1})) \right)$$

其中 $\mathrm{sg}(\cdot)$ 表示停止梯度操作。模型在纯在线强化学习设置下训练，通过分布式数据并行（DDP）在 8× NVIDIA A100 GPU 上同步梯度，每个 GPU 处理静态分配的任务子集并构建异构批次。



### 3.1 统一世界模型损失函数

ScaleZero 的核心训练目标建立在 UniZero 的统一世界模型损失之上，该损失在长度为 $H$ 的上下文窗口上同时优化四个预测目标：

$$
\mathcal{L}_{\mathrm{Unified}} = \sum_{t=0}^{H-1} \left( \mathcal{L}_{\mathrm{value}}(v_t, \hat{v}_t^{target}) + \mathcal{L}_{\mathrm{policy}}(p_t, \pi_t) + \mathcal{L}_{\mathrm{reward}}(\hat{r}_t, r_t) + \mathcal{L}_{\mathrm{dynamics}}(\hat{z}_{t+1}, \mathrm{sg}(z_{t+1})) \right)
$$

其中各分量含义如下：
- **$\mathcal{L}_{\mathrm{value}}$**：价值预测损失，对齐模型预测的价值 $v_t$ 与 MCTS 规划器产生的自举 TD 目标 $\hat{v}_t^{target}$。
- **$\mathcal{L}_{\mathrm{policy}}$**：策略预测损失，使模型输出的策略分布 $p_t$ 逼近 MCTS 搜索得到的改进策略 $\pi_t$。
- **$\mathcal{L}_{\mathrm{reward}}$**：奖励预测损失，监督模型对即时奖励 $\hat{r}_t$ 的预测。
- **$\mathcal{L}_{\mathrm{dynamics}}$**：动态预测损失，约束模型预测的下一隐状态 $\hat{z}_{t+1}$ 与编码器实际输出的 $z_{t+1}$ 一致，其中 $\mathrm{sg}(\cdot)$ 表示停止梯度操作，防止编码器表征被动态预测目标反向干扰。

该复合损失使得单一世界模型能够同时充当动态模型、奖励模型、价值函数和策略先验，为 MCTS 规划提供统一的隐空间搜索基础。

### 3.2 可塑性崩溃的诊断指标

为量化多任务训练中网络可塑性的退化程度，论文引入了**休眠神经元比率**（Dormant Neuron Ratio）。对于第 $l$ 层，其定义为：

$$
\mathrm{DormantRatio}(l) = \frac{1}{N_l} \sum_{i=1}^{N_l} \mathbf{1}\left(\left|h_i^l\right| \leq \epsilon\right)
$$

其中 $N_l$ 为第 $l$ 层的神经元总数，$h_i^l$ 为第 $i$ 个神经元的激活值，$\epsilon$ 为接近零的阈值。该指标捕捉了网络中“失活”神经元的比例——当大量神经元的激活幅度持续低于阈值时，网络的有效容量急剧缩减，表征能力随之崩溃。

**决定性证据**：如 Figure 1 所示，在 UniZero 基线的多任务 Atari 训练中，复杂任务（Seaquest、ChopperCommand）的性能灾难性下降与休眠神经元比率的急剧飙升在时间上严格同步，同时伴随隐状态范数的失控膨胀。这一现象确证了可塑性崩溃是多任务统一世界模型失效的根本模式。

### 3.3 MoE 梯度冲突的理论上界

混合专家（MoE）架构缓解多任务梯度冲突的能力具有严格的理论支撑。对于两个任务 $t_1$ 和 $t_2$，全层 MoE 的梯度冲突上界为：

$$
\mathrm{conflict}(G_{t_1}, G_{t_2}) \leq G \cdot \frac{\sum_{m=1}^{M} \lambda_m^{t_1} \lambda_m^{t_2} \|g_{t_1}^{(m)}\| \|g_{t_2}^{(m)}\|}{\sqrt{\sum_{m=1}^{M} (\lambda_m^{t_1})^2 \|g_{t_1}^{(m)}\|^2} \sqrt{\sum_{m=1}^{M} (\lambda_m^{t_2})^2 \|g_{t_2}^{(m)}\|^2}} \leq G
$$

其中 $M$ 为专家数量，$\lambda_m^{t}$ 为任务 $t$ 对专家 $m$ 的路由权重，$g_t^{(m)}$ 为任务 $t$ 在专家 $m$ 上的梯度，$G$ 为单专家内部的梯度冲突上界。该不等式揭示了 MoE 的两个关键性质：
1. **冲突严格有界**：全层梯度冲突被限制在单专家冲突 $G$ 以内，而密集网络的冲突上界远高于此。
2. **稀疏路由进一步压缩冲突**：当门控网络稀疏激活 top-k 专家时，多数 $\lambda_m^t$ 为零，分子中仅保留少量交叉项，使得实际冲突远低于上界。

这一理论保证解释了为什么在 Figure 3 的消融实验中，将密集 Transformer 替换为 MoE 骨干是唯一能显著且一致提升 Atari8 多任务性能的架构改动——MoE 的条件计算机制通过专家专业化从根本上隔离了不同任务的梯度更新。

### 3.4 动态参数扩展的有效权重组合

动态参数扩展（DPS）策略通过分阶段注入 LoRA 适配器实现模型容量的渐进式增长。在第 $s$ 阶段，网络的有效权重矩阵为基座权重与所有历史适配器的可学习组合：

$$
W^{(s)} = \alpha_0 W_0 + \sum_{j=1}^{s} \alpha_j \Delta \theta_j = \alpha_0 W_0 + \sum_{j=1}^{s} \alpha_j B_j A_j
$$

其中 $W_0$ 为初始基座权重，$\Delta \theta_j = B_j A_j$ 为第 $j$ 阶段注入的低秩适配器（$B_j$ 和 $A_j$ 为低秩分解矩阵），$\alpha_j$ 为可学习的缩放因子。DPS 的核心设计原则是**参数隔离**：进入阶段 $s$ 后，所有先前阶段的参数（基座 $W_0$ 及适配器 $\{\Delta \theta_j\}_{j=1}^{s-1}$）均被冻结，仅当前阶段新增的适配器和缩放因子参与训练。这既保护了已学知识不被覆盖，又为未完成任务提供了定向的可塑性空间，从而在 DMControl 基准上实现了约 28.5% 的环境交互成本降低（Figure 4）。



## 实验与关键发现

### 核心失效模式诊断：可塑性崩溃

多任务世界模型面临的根本挑战并非简单的容量不足，而是一种被称为**可塑性崩溃**（plasticity collapse）的退化现象。实验诊断（Figure 1）揭示了一个清晰的因果链条：在Atari多任务基准上训练统一的UniZero模型时，简单任务（如Pong、Hero）保持稳定学习，但复杂任务（如Seaquest、ChopperCommand）在训练后期（约150K–200K环境步后）遭遇**灾难性的性能坍塌**。这一外部性能崩溃与两个内部动力学指标在时间上严格同步：

![[assets/figures/papers/paper_list_l16_https_openreview_net_forum_id_iU026Hr90y/figures/001_Figure_1.jpg]]
*Figure 1: Plasticity collapse in the baseline (UniZero) on a multitask Atari benchmark. While simple tasks like Pong and Hero show stable learning, complex tasks such as Seaquest and ChopperCommand suffer a catastrophic performance collapse in later training (Top). This failure is precisely correlated with a sharp spike in the dormant neuron ratio of the transformer (Bottom Left) and an uncontrolled inflation of the latent state norm (Bottom Right), empirically validating the link between external performance and internal learning dynamics*

- **休眠神经元比率激增**：Transformer层的激活幅度低于阈值$\epsilon$的神经元比例急剧上升，表明网络有效容量被侵蚀。
- **隐状态范数膨胀**：潜在状态向量的范数失控增长，暗示表征空间的结构性退化。

这两个指标共同指向**梯度冲突**作为根本原因——不同任务的梯度在共享骨干中相互抵消，导致网络陷入一种“死锁”状态，丧失了进一步学习的能力。这一诊断将多任务世界模型的设计焦点从“如何增加容量”重新定位为“如何抑制梯度冲突”。

### 架构消融：MoE骨干的决定性作用

为验证不同架构组件对缓解可塑性崩溃的贡献，论文在UniZero设计空间的五个轴向上进行了系统消融（Figure 2a, Figure 3）：任务条件化、编码器架构、隐状态归一化、骨干网络设计和优化策略。在Atari8多任务基准上的消融结果（Figure 3）呈现出清晰的层级结构：

![[assets/figures/papers/paper_list_l16_https_openreview_net_forum_id_iU026Hr90y/figures/005_Figure_3.jpg]]
*Figure 3: Performance impact of architectural modifications on the Atari8 multitask benchmark. This ablation across the UniZero design space reveals that replacing the Transformer backbone with a Mixture-of-Experts architecture yields the most significant and consistent performance gains. In contrast, other interventions, with the partial exception of SimNorm, provide marginal or inconsistent benefits. These results underscore the centrality of the MoE’s conditional computation in overcoming the limitations of a shared, dense backbone*

| 干预措施 | 效果 |
|----------|------|
| **密集Transformer → MoE骨干** | **唯一显著且一致的性能提升**，训练后期归一化中位数得分从~0.2跃升至~0.4 |
| SimNorm → LayerNorm | 训练稳定性提升，但SimNorm的硬约束削减了表征表达能力，最终性能次优 |
| ResNet编码器 → ViT编码器 | 边际收益 |
| 任务嵌入（naive task embeddings） | 无明显改善，推测后期嵌入崩溃 |
| MoCo梯度校正 | 边际收益 |

关键结论：**MoE的条件计算机制是抑制梯度冲突、防止可塑性崩溃的核心杠杆**。稀疏路由将不同任务的梯度更新分配到专门化的专家子网络，从架构层面隔离了冲突。理论分析（Theorem E.1, Appendix E.2）进一步证明，MoE层的梯度冲突上界严格低于密集网络，且稀疏路由能进一步压缩该上界。

### 主实验结果：多任务正向迁移

**Atari 100k基准（26款游戏）**：ScaleZero多任务代理的Human-Normalized Score均值达到0.39，超过了26个单任务UniZero代理的均值0.38（Table 1a）。这一结果具有方法论意义——它证明多任务联合训练不仅没有因干扰导致性能退化，反而实现了**正向迁移**，使单个模型超越了单任务专家的平均水平。

![[assets/figures/papers/paper_list_l16_https_openreview_net_forum_id_iU026Hr90y/figures/006_Table_1.jpg]]
*Table 1: Performance comparison of our multitask model, ScaleZero, against the single-task UniZero baseline across discrete (Atari) and continuous (DMControl) benchmarks*

**DMControl基准（18个连续控制任务）**：ScaleZero多任务模型的中位数原始得分达到887.3，超过单任务UniZero的875.1（Table 1b），进一步验证了方法在连续控制领域的有效性。

**Jericho文本游戏**：在Zork1上，ScaleZero达到44.0的平均回报，显著超过CALM+OC的38.0；在Detective上，ScaleZero（280）与CALM+OC（288.5）接近持平（Table 2）。这表明MoE骨干的条件计算同样适用于基于文本的离散环境。

### 动态参数扩展的效率增益

DPS策略在DMControl基准上展示了显著的样本效率提升（Figure 4）：ScaleZero-DPS仅用标准ScaleZero约**71.5%的环境交互量**即达到相同目标性能，交互成本降低约**28.5%**。这一效率增益来源于DPS的两个协同机制：

![[assets/figures/papers/paper_list_l16_https_openreview_net_forum_id_iU026Hr90y/figures/009_Figure_4.jpg]]
*Figure 4: Interaction cost comparison for ScaleZero vs. ScaleZero-DPS on DMControl. Tha latter reaches the target performance with a 28.5% reduction in the environment cost. Detailed curves are in Appendix C*

1. **自适应任务筛选**：仅对未解决的任务投入计算资源，避免在已收敛任务上浪费探索。
2. **渐进式容量注入**：通过阶段性冻结已有参数并注入LoRA适配器，既保留了先前知识，又为未完成任务提供了定向可塑性。

值得注意的是，DPS目前仅在DMControl连续控制任务上进行了验证，其在Atari和Jericho等离散/文本环境上的泛化性尚待实验证实。

### 失败模式与残留挑战

尽管ScaleZero整体表现优异，部分硬探索任务仍存在**负迁移**现象。在Atari的PrivateEye等游戏上，多任务训练的性能低于单任务基线，表明梯度冲突并未被完全消除。此外，MoE与LoRA在当前框架中仍相对独立运行——DPS的LoRA适配器作用于全层权重，而非针对MoE的门控网络进行自适应调控，限制了架构自适应的深层潜力。



## 定位与知识库关联

### 1. 核心基线：UniZero 统一世界模型

ScaleZero 直接继承自 **UniZero**（Pu et al., 2024）的统一世界模型范式。UniZero 首次提出将环境建模、策略学习与价值估计统一于单一 Transformer 架构中，通过 MCTS 规划器生成训练目标，以复合损失函数联合优化：

$$\mathcal{L}_{\mathrm{Unified}} = \sum_{t=0}^{H-1} \left( \mathcal{L}_{\mathrm{value}}(v_t, \hat{v}_t^{target}) + \mathcal{L}_{\mathrm{policy}}(p_t, \pi_t) + \mathcal{L}_{\mathrm{reward}}(\hat{r}_t, r_t) + \mathcal{L}_{\mathrm{dynamics}}(\hat{z}_{t+1}, \mathrm{sg}(z_{t+1})) \right)$$

然而，当 UniZero 被直接扩展至多任务学习时，其密集 Transformer 骨干暴露出根本性失效模式：**可塑性崩溃**（plasticity collapse）。如 Figure 1 所示，在 Atari8 多任务基准上，简单任务（Pong、Hero）保持稳定学习，而复杂任务（Seaquest、ChopperCommand）在训练后期经历灾难性性能坍塌。这一失效与两个内部指标在时间上严格同步——休眠神经元比率（dormant neuron ratio）的急剧飙升和隐状态范数的失控膨胀，揭示了密集共享骨干网络中梯度冲突和表征干扰的系统性问题。

### 2. 架构改进谱系：从密集到稀疏的条件计算

ScaleZero 的核心架构创新在于将 UniZero 的密集 Transformer 骨干替换为**稀疏混合专家**（Sparse Mixture-of-Experts, MoE）结构（Shazeer et al., 2017）。这一替换并非简单的容量扩展，而是从根本上改变了多任务学习中的梯度动力学。

**梯度冲突的理论基础。** 在多任务强化学习中，不同任务的梯度方向往往相互对抗，即 $\cos(g_i, g_j) < 0$。密集网络将所有任务的梯度更新压缩至共享参数空间，导致冲突不可解耦。MoE 的条件计算机制通过任务特定路由将计算分散至专门子网络，其梯度冲突上界被严格约束：

$$\mathrm{conflict}(G_{t_1}, G_{t_2}) \leq G \cdot \frac{\sum_{m=1}^{M} \lambda_m^{t_1} \lambda_m^{t_2} \|g_{t_1}^{(m)}\| \|g_{t_2}^{(m)}\|}{\sqrt{\sum_{m=1}^{M} (\lambda_m^{t_1})^2 \|g_{t_1}^{(m)}\|^2} \sqrt{\sum_{m=1}^{M} (\lambda_m^{t_2})^2 \|g_{t_2}^{(m)}\|^2}} \leq G$$

该上界表明，通过路由权重 $\lambda_m$ 的分配，全层冲突可被严格限制在单专家冲突 $G$ 以内，且稀疏路由（top-1 gating）能进一步降低此上界。Figure 3 的消融实验提供了决定性证据：在 Atari8 多任务基准上，将骨干替换为 MoE 是唯一能带来显著且一致性能提升的架构干预，而其他改动（任务嵌入、ViT 编码器、SimNorm 归一化、MoCo 梯度校正）仅提供边缘收益。

**归一化层的替代。** ScaleZero 将 UniZero 的 SimNorm（基于 L1 的单纯形投影）替换为标准 LayerNorm。消融实验（Figure 3）表明，SimNorm 虽能稳定训练，但其硬约束削减了表征表达能力，导致最终性能次优。LayerNorm 在保持训练稳定性的同时释放了表征容量。

**视觉编码器的升级。** 将 UniZero 的 ResNet 类编码器替换为从零训练的 Vision Transformer（ViT），以提升特征提取的可扩展性。单独替换编码器带来的增益有限，但与 MoE 骨干协同后贡献显著。

### 3. 训练策略创新：动态参数扩展（DPS）

DPS 策略独立于架构改进，作用于训练资源分配层面。其核心原则是**参数隔离**——当训练推进至阶段 $s$ 时，冻结所有先前学习的参数（骨干 $\theta_B$ 及适配器 $\{\Delta\theta_j\}_{j=1}^{s-1}$），仅新注入的 LoRA 适配器可训练，有效权重矩阵为：

$$W^{(s)} = \alpha_0 W_0 + \sum_{j=1}^{s} \alpha_j \Delta\theta_j = \alpha_0 W_0 + \sum_{j=1}^{s} \alpha_j B_j A_j$$

DPS 通过自适应任务筛选（adaptive task curation）聚焦未完成任务，并以渐进式容量注入实现定向可塑性。在 DMControl 基准上，DPS 使环境交互成本降低约 28.5%（Figure 4），同时达到与标准 ScaleZero 相当的性能。

### 4. 适用边界与局限

**已验证的适用范围。** ScaleZero 在三个异构基准上展现出跨域泛化能力：离散动作空间（Atari 100k，26 款游戏）、连续控制（DMControl，18 个任务）和文本环境（Jericho，4 款游戏）。单一多任务代理在 Atari 100k 上的 Human-Normalized Score 均值（0.39）超过了 26 个单任务 UniZero 代理的均值（0.38），证明多任务学习实现了正向迁移。

**明确局限。**

1. **DPS 的泛化性未经验证。** DPS 策略目前仅在 DMControl 连续控制任务上进行了评估，其在离散/视频游戏（Atari）和语言环境（Jericho）上的有效性尚待实验证实。

2. **MoE 与 LoRA 的协同不足。** 当前框架中 MoE 骨干与 LoRA 适配器相对独立运行，未能实现深层协同——例如用 LoRA 自适应调控 MoE 门控网络，限制了架构自适应的潜力。

3. **完全依赖在线学习。** 方法未探索大规模离线预训练所提供的冷启动和峰值性能增益，样本效率受限于从零探索。

4. **负迁移未彻底消除。** 在部分硬探索任务（如 Atari 的 PrivateEye）上仍存在负迁移，表明任务间干扰并未被完全解决。

### 5. 开放问题

1. **梯度校正的效率优化。** 能否设计一种性能-开销比更优的梯度校正策略，以在保持高效的同时主动缓解不同任务间的梯度冲突？当前 MoCo 基方法收益有限。

2. **DPS 的跨模态泛化。** DPS 策略能否在跨越视觉、运动和文本等高度异质环境（如同时训练 Atari、DMControl 和 Jericho）的统一训练中依然有效？

3. **任务特定信息的鲁棒注入。** 原始任务嵌入（naive task embeddings）未能显著改善性能，推测是缺乏约束导致嵌入在训练后期崩溃。如何显式且鲁棒地注入任务特定信息，以提升路由器的任务辨别能力？

4. **MoE-LoRA 深层协同。** MoE 与 LoRA 之间的深层协同（如用 LoRA 调整门控网络动态）能否进一步提升多任务训练中的架构适应性和稳定性？

5. **离线预训练的融合。** 若将 ScaleZero 与大规模离线预训练基础模型结合，能否显著改善样本效率和“冷启动”性能，并弥合专用强化学习与通用世界模型之间的差距？



## 原文 PDF

![[paperPDFs/ICLR_2026/One_Model_for_All_Tasks_Leveraging_Efficient_World_Models_in_Multi_Task_Planning.pdf]]
