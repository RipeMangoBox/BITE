---
title: "Mixture-of-World Models: Scaling Multi-Task Reinforcement Learning with Modular Latent Dynamics"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/Mixture_of_World_Models_Scaling_Multi_Task_Reinforcement_Learning_with_Modular_Latent_Dynamics.pdf
openreview_forum_id: qUQARlAx5y
aliases:
- MWMM
- MWMSMTRLMLD
tags:
- ICLR_2026
- topic/generative_models_diffusion
- topic/generative_models_diffusion/generative_models_and_autoencoders
core_operator: "通过模块化的任务专用VAE和混合专家Transformer，结合任务嵌入引导的专家路由和基于梯度相似性的任务聚类，实现对多样任务动力学的自适应建模和参数高效共享。"
primary_logic: "将世界模型分解为任务专用的视觉编码器、共享-专家混合的Transformer时序模型，并利用梯度信息聚类任务以共享模块，能够在保持高重建质量的同时，大幅提升多任务世界模型的参数效率与任务判别能力。"
claims:
- "MoW在Atari 100K上使用单一模型达到110.4%的人类归一化分数，与26个任务专用模型组成的STORM（114.2%）性能相当，而参数量减少50%。"
- "MoW在Meta-World MT50上以74.5%的成功率在15M步内实现了新的最优，使用图像输入，对比最好的基于状态的MOORE（72.9%需100M步）。"
- "消融研究表明，任务预测损失、专家平衡损失和基于梯度的聚类对性能至关重要；去掉任一项都会导致显著性能下降。"
- "Atari 100K (26 games) 上 Human Normalized Mean = 110.4%"
---

# Mixture-of-World Models: Scaling Multi-Task Reinforcement Learning with Modular Latent Dynamics

> [!tip] 核心洞察
> 将世界模型分解为任务专用的视觉编码器、共享-专家混合的Transformer时序模型，并利用梯度信息聚类任务以共享模块，能够在保持高重建质量的同时，大幅提升多任务世界模型的参数效率与任务判别能力。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 混合世界模型：用模块化潜在动力学扩展多任务强化学习 |
| 英文题名 | Mixture-of-World Models: Scaling Multi-Task Reinforcement Learning with Modular Latent Dynamics |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=qUQARlAx5y) |
| Topic | #topic/generative_models_diffusion #topic/generative_models_diffusion/generative_models_and_autoencoders |
| Method | Mixture-of-World Models (MoW) |
| Dataset | Atari 100K (26 games), Meta-World MT50 |

> [!tip] 效果简介
> - Atari 100K (26 games) 上，Human Normalized Mean 为 110.4%，对比 114.2% (STORM reproduced, single-task)，变化 -3.8%。
> - Meta-World MT50 上，Average Success Rate 为 74.5%，对比 72.9% (MOORE, state-based)，变化 +1.6% (15M steps vs 100M steps)。
> - Meta-World MT50 上，Average Success Rate 为 74.5%，对比 25.3% (TD-MPC2, visual)，变化 +49.2%。

## 概述

**核心问题**：在多任务视觉强化学习中，标准的单一世界模型架构难以同时捕捉不同任务在视觉特征和动力学上的异质性，导致重建保真度低和任务间干扰，严重限制了样本效率。

**方法定位**：本文提出**混合世界模型（Mixture-of-World Models, MoW）**，通过模块化潜在动力学实现多任务世界模型的参数高效扩展。其核心设计包括三个层面：
- **感知层**：采用基于梯度相似性聚类的多个任务专用VAE，替代单一共享编码器，实现任务自适应的视觉压缩。
- **时序层**：构建任务条件路由的混合专家Transformer与共享Transformer的组合架构，由可学习任务嵌入引导专家选择，实现对多样任务动力学的解耦建模。
- **训练层**：引入任务预测损失与专家平衡损失，结合和谐损失加权策略，增强任务判别能力与专家利用均衡性。

**方法谱系与知识库定位**：MoW属于基于模型的强化学习（MBRL）范式，在世界模型架构上对**STORM**（Zhang et al., 2023）的单任务框架进行了多任务模块化扩展。与多任务模型无关MoE方法**MOORE**（Hendawy et al., 2023）和基于模型的多任务方法**TD-MPC2**（Hansen et al., 2024）相比，MoW的关键区别在于将混合专家机制从Transformer内部解耦并外置，通过任务级路由而非令牌级路由实现专家选择，从而保证同一任务内专家激活的一致性。在多任务SAC（**MTSAC**）等无模型基线之上，MoW通过世界模型的想象推演显著提升了样本效率。

**主要结果**：
- 在Atari 100K基准（26款游戏）上，MoW使用单一模型达到**110.4%的人类归一化分数**，与26个任务专用模型组成的STORM（114.2%）性能相当，而**参数量减少50%**（Table 11, Figure 3）。
- 在Meta-World MT50上，MoW以仅15M环境步实现**74.5%的平均成功率**，优于需要100M步的基于状态输入的MOORE（72.9%），并在视觉输入设定下大幅超越TD-MPC2（25.3%→74.5%）（Table 1, Figure 15）。
- 消融实验证实，任务预测损失、专家平衡损失和基于梯度的聚类三者缺一不可，移除任一项均导致显著性能退化（Figure 5, Figure 8）。

**证据强度与注意事项**：上述核心结论有高置信度实验支撑。但需注意，MoW在Freeway、Private Eye等部分Atari游戏上得分仍为0或极低，且多任务中位分数（37.7%）远低于均值（110.4%），表明性能在不同任务间差异较大，模型可能过度依赖表现较好的任务。此外，基于梯度的聚类仅在warmup阶段执行，无法在训练过程中动态调整任务分组。

## 背景与动机

### 多任务视觉强化学习的瓶颈

基于视觉的多任务强化学习面临一个核心矛盾：不同任务在视觉外观和动力学特性上存在显著异质性，而标准的单一世界模型架构难以同时捕捉这种多样性。当所有任务共享同一个视觉编码器和时序动力学模型时，模型被迫在重建保真度和任务特异性之间做出妥协，导致两个层面的失败——视觉重建质量下降，以及任务间的动力学干扰。这种干扰直接损害样本效率，因为智能体在想象中生成的轨迹不再忠实于各任务的真实环境动态。

问题的本质在于**参数共享与任务特异性之间的张力**。完全独立的单任务模型（如 **STORM**，Zhang et al., 2023）可以为每个任务学习精确的世界模型，但其参数量随任务数量线性增长，无法利用跨任务的共性知识。反之，完全共享的模型则牺牲了对任务差异的建模能力。现有方法尚未在保持高重建质量的前提下，实现参数高效的多任务世界模型学习。

### 现有方法的局限

当前多任务模型无关强化学习方法（如 **MTSAC**、**CARE**、**PaCo**）通常依赖状态输入而非高维图像，回避了视觉编码的挑战。基于模型的多任务方法则更为稀缺：**MOORE**（Hendawy et al., 2023）引入了混合专家（MoE）机制，但仅处理状态输入，且需要1亿环境步才能达到72.9%的Meta-World MT50成功率；**TD-MPC2**（Hansen et al., 2024）在视觉输入改编版上仅取得25.3%的成功率，暴露了现有基于模型方法在视觉多任务场景下的严重不足。

这些方法的共同缺陷在于：它们要么忽略了视觉编码的模块化需求，要么将混合专家机制应用于状态空间而非潜在动力学空间，未能从根本上解决视觉特征异质性和动力学异质性耦合的问题。

### 本文动机与核心思路

本文的出发点是：**将世界模型分解为任务专用的视觉编码器与混合专家的时序Transformer，并利用梯度信息指导模块共享，可以在保持高重建质量的同时，大幅提升多任务世界模型的参数效率与任务判别能力。**

具体而言，Mixture-of-World Models（MoW）通过三个机制实现这一目标：

1. **模块化视觉编码**：通过基于梯度相似性的任务聚类，为不同任务组分配专用的VAE，使每个VAE专注于视觉特征相近的任务子集，从而提升重建保真度。

2. **混合专家动力学建模**：在时序Transformer中引入任务条件路由的专家混合机制，使不同任务激活不同的专家子集，实现对多样化动力学的自适应建模，同时通过共享Transformer捕捉跨任务共性。

3. **任务判别与平衡约束**：通过任务预测损失强制世界模型区分不同任务，通过专家平衡损失防止专家利用退化，确保模块化架构的有效运行。

这种设计使MoW能够在Atari 100K基准上以单一模型达到110.4%的人类归一化分数，与26个独立任务专用模型组成的STORM（114.2%）性能相当，而参数量减少50%；在Meta-World MT50上以仅1500万环境步达到74.5%的成功率，成为该基准上首个使用图像输入超越状态输入方法的工作。

## 核心创新

MoW 的核心创新在于将世界模型分解为**任务专用的视觉编码器**与**混合专家的时序动力学模型**，并通过**基于梯度相似性的任务聚类**实现参数高效共享。这一设计直接回应了多任务视觉强化学习的根本瓶颈：单一世界模型难以同时捕捉不同任务在视觉特征和动力学上的异质性，导致重建保真度低和任务间干扰。

### 从单一模型到模块化分解

标准的多任务世界模型（如 STORM, Zhang et al., 2023）采用全任务共享的 VAE 和标准 Transformer，所有任务共享同一套参数。MoW 在三个关键维度上改变了这一范式：

**1. 视觉编码器：从共享到任务专用聚类**

MoW 将单一共享 VAE 替换为通过梯度聚类分配的多个任务专用 VAE（Section 3.1.1, Section 3.6）。每个 VAE 以任务嵌入 $e_k$ 为条件进行后验采样和观测重建：

$$z_k^t \sim q_{\phi, i_k}(z_k^t \mid o_k^t, e_k) = \mathcal{Z}_k^t; \quad \hat{o}_k^t \sim p_{\phi, i_k}(\hat{o}_k^t \mid z_k^t, e_k)$$

这种设计使视觉编码能够自适应不同任务的外观特征，避免了共享 VAE 在重建质量上的妥协。消融实验表明，移除基于梯度的聚类会导致性能显著下降（Figure 8, Appendix A.5），验证了任务分组对参数共享的关键作用。

**2. 时序动力学：从标准 Transformer 到混合专家架构**

MoW 将标准 Transformer 替换为**专家 Transformer 与共享 Transformer 的组合**（Section 3.1.2, Section 3.2）。核心机制包括：

- **任务条件路由**：任务层路由器根据任务嵌入 $e_k$ 计算任务-专家亲和度，并通过 TopK 操作选择激活的专家（Equation 3）。温度系数在训练过程中逐步退火至 1，促进路由稳定。
- **解耦式 MoE**：MoW 将 MoE 机制与 Transformer 架构解耦，在外部应用专家选择（Section 3.2）。这使每个专家能捕获更完整、连贯的任务动力学，而非在 token 级别进行碎片化路由。
- **双层级联处理**：激活的专家 Transformer 输出拼接后送入共享 Transformer（Equation 4），实现任务专用知识与跨任务共同知识的层次化整合。

消融实验揭示了这一架构的敏感性：移除共享 Transformer 导致适度性能下降，但移除专家 Transformer 会导致更严重的退化（Figure 8, Appendix A.5）。增加专家 Transformer 数量比增加 VAE 集群数量带来更明显的性能提升（Figure 4），表明时序动力学建模的模块化是性能提升的主要驱动力。

**3. 参数分配策略：从全共享到梯度聚类**

MoW 引入 warmup 阶段的**梯度相似性聚类**（Section 3.6），替代了传统的全任务共享或完全独立模型策略。在 warmup 阶段，MoW 使用单一 VAE 和预测器进行短期离线自监督训练，基于各任务梯度的一致性将任务分组，随后为不同组分配独立的 VAE 和预测头。这一静态聚类策略是 MoW 在保持高性能的同时实现 50% 参数量缩减（相对于 26 个独立 STORM 模型）的关键机制。

### 辅助损失设计

除架构创新外，MoW 引入了两个关键的辅助损失（Section 3.3, 3.4）：

- **任务预测损失** $\mathcal{L}_{t,k}^{\mathrm{task}}$：以交叉熵形式预测任务索引，增强模型的任务判别能力。消融实验证实移除该损失导致整体性能明显下降（Figure 8, Appendix A.5）。
- **专家平衡损失** $\mathcal{L}_{\mathrm{bal}}$：鼓励所有专家被激活，避免路由坍缩到少数专家。移除该损失会使训练对初始化敏感，导致专家利用不均衡（Section 3.4, Appendix A.5）。

这些损失通过和谐损失（Harmonic Loss, Equation 9）进行动态加权，自动平衡不同任务间的学习速度。

### 创新总结

MoW 的方法论贡献可概括为三个 **changed slots**：视觉编码器从共享到聚类专用、时序模型从标准 Transformer 到混合专家、参数分配从全共享到梯度聚类。这三个改变的协同作用使 MoW 在 Atari 100K 上以单一模型达到 110.4% 的人类归一化分数（与 26 个单任务 STORM 模型的 114.2% 相当，参数量减少 50%），在 Meta-World MT50 上以 74.5% 的成功率实现新的最优（Table 1, Section 4.1）。

## 整体框架

![[assets/figures/papers/paper_list_l49_https_openreview_net_forum_id_qUQARlAx5y/figures/001_Figure_1.jpg]]
*Figure 1: Overview of the mixture-of-world models (MoW) architecture. Task-specific observations are encoded through specialized VAEs, with dynamics modeled by a mixture-of-Transformer experts routed via task embeddings. The design enables modular latent dynamics handling while maintaining parameter efficiency. Here, at time t for task k, $o _ { k } ^ { t } , r _ { k } ^ { t } , c _ { k } ^ { t }$ and $a _ { k } ^ { t }$ denote the high-dimensional observation, reward, termination flag, and action, respectively. The stochastic representation $z _ { k } ^ { t }$ is sampled from the distribution $\mathcal { Z } _ { k } ^ { t }$ . , which is encoded from the observation $o _ { k } ^ { t }$ . The hidden state $\ddo$...

MoW（Mixture-of-World Models）的核心设计思路是将多任务世界模型分解为**任务自适应感知**与**混合专家时序建模**两大阶段，通过任务嵌入贯穿全局，实现对异质视觉动力学的高保真重建与参数高效共享。

### 总体架构

整个系统由以下模块串联构成，数据流与模块关系如 Figure 1 所示：

1. **感知模块（任务专用VAE）**：对于每个任务 $k$，其高维观测 $o_k^t$ 被送入该任务专属的类别型VAE。后验网络以任务嵌入 $e_k$ 为条件，编码出随机潜在表示 $z_k^t \sim q_{\phi, i_k}(z_k^t \mid o_k^t, e_k) = \mathcal{Z}_k^t$；解码器则从 $z_k^t$ 重建观测 $\hat{o}_k^t$。不同任务可共享VAE，共享关系由warmup阶段的梯度聚类决定。

2. **输入混合器**：每个专家 $j$ 拥有独立的MLP混合器 $m_{\phi,j}$，将随机表示 $z_k^{1:t}$、动作序列 $a_k^{1:t}$ 和任务嵌入 $e_k$ 融合为统一令牌 $m_{j,k}^{1:t}$。

3. **任务路由器**：任务嵌入 $e_k$ 经过MLP和Softmax产生专家亲和度分数 $S_k$，再通过TopK操作选出 $n_k$ 个专家索引 $J_k$ 及对应权重 $W_k$。路由在任务层面执行，同一任务在不同时间步激活相同的专家集合，确保单个专家能学习完整的任务动态。

4. **专家Transformer**：被选中的 $n_k$ 个专家各自独立处理对应的输入令牌，输出 $f_{\phi, j_k^i}(m_{j_k^i, k}^{1:t})$。这些输出被拼接为 $l_k^{1:t}$。

5. **共享Transformer**：拼接后的专家输出 $l_k^{1:t}$ 与任务嵌入 $e_k$ 一同送入共享Transformer $F_{\phi}$，产生隐藏状态 $h_k^{1:t}$。共享部分捕捉跨任务通用知识，专家部分建模任务特异性动态。

6. **预测头**：隐藏状态 $h_k^t$ 驱动四个预测头——下一状态分布 $\hat{\mathcal{Z}}_k^{t+1}$、奖励 $\hat{r}_k^t$、终止标志 $\hat{c}_k^t$ 和任务索引 $\hat{k}$。其中状态预测头是任务专用的（与VAE共享聚类分配），任务预测头则使用跨任务共享的MLP。

7. **智能体（Actor-Critic）**：在世界模型生成的想象轨迹上学习。Critic使用symlog双热损失近似 $\lambda$-回报，Actor通过归一化优势函数的策略梯度进行更新，并加入熵正则项。Critic网络同样按梯度聚类分配，与VAE共享分组方案。

### 训练流程

训练分为两个阶段：

- **Warmup与梯度聚类**：首先使用单一共享VAE和预测器进行短暂的离线自监督训练（约数千步，见 Figure 6 的梯度范数收敛曲线）。随后计算各任务关于VAE和预测器参数的梯度，基于梯度相似性对任务进行聚类，据此为每个任务簇分配独立的VAE、预测头和Critic网络，实现模块共享。

- **联合在线训练**：世界模型通过自监督损失端到端训练，总损失为各任务和谐损失 $\mathcal{L}_{\mathcal{H}}(\phi)$ 与权重0.1的专家平衡损失 $\mathcal{L}_{\text{bal}}(\phi)$ 之和（Equation 10）。和谐损失动态调整各任务权重，平衡损失防止专家利用不均。智能体则完全在想象轨迹上学习，利用KV缓存机制加速自回归 rollout。

### 与现有方法的架构差异

Table 2 将MoW与近期方法进行了系统对比。相较于单一共享VAE加标准Transformer的**STORM**（Zhang et al., 2023），MoW引入了任务专用VAE、混合专家Transformer和任务路由器，在保持重建质量的同时大幅提升了多任务参数效率。与基于状态的MoE方法**MOORE**（Hendawy et al., 2023）不同，MoW直接处理图像输入，并将MoE机制解耦于Transformer外部，以任务嵌入而非逐令牌路由来激活专家，从而保证任务内专家激活的一致性。

## 核心模块与公式推导

### 多任务世界模型优化目标

MoW 将多任务强化学习形式化为在所有 $K$ 个任务上最大化期望折扣回报：

$$\sum_{k=1}^{K} \mathbb{E}_{(o_k, a_k) \sim \pi, \mathcal{P}_k} \left[ \sum_{t=1}^{\infty} \gamma_k^{t-1} \mathcal{R}_k(o_k^t, a_k^t) \right]$$

其中 $o_k^t$、$a_k^t$ 分别为任务 $k$ 在时刻 $t$ 的观测与动作，$\mathcal{P}_k$ 和 $\mathcal{R}_k$ 为对应的转移动态与奖励函数，$\gamma_k$ 为折扣因子。

### 感知模块：任务专用类别型 VAE

每个任务 $k$ 被分配到一个 VAE 集群 $i_k$，其编码器以任务嵌入 $e_k$ 为条件，将高维观测 $o_k^t$ 压缩为随机潜在表示 $z_k^t$：

$$z_k^t \sim q_{\phi, i_k}(z_k^t \mid o_k^t, e_k) = \mathcal{Z}_k^t$$

解码器从该潜在表示重建观测：

$$\hat{o}_k^t \sim p_{\phi, i_k}(\hat{o}_k^t \mid z_k^t, e_k)$$

**设计动机**：不同任务在视觉特征上存在显著异质性（如 Atari 游戏中 Pong 与 Montezuma's Revenge 的视觉分布截然不同），单一共享 VAE 难以同时保持高重建保真度。任务专用 VAE 通过梯度聚类分配，使视觉相似的任务共享编码器/解码器参数，在重建质量与参数效率之间取得平衡。

### 时序动力学模块：混合专家 Transformer

#### 输入混合器

将随机表示、动作序列和任务嵌入融合为各专家可消费的统一令牌：

$$m_{j,k}^{1:t} = m_{\phi, j}(z_k^{1:t}, a_k^{1:t}, e_k)$$

其中 $m_{\phi, j}$ 为第 $j$ 个专家对应的 MLP 混合器，输出维度与 Transformer 特征维度 $D$ 对齐。

#### 任务级路由与专家选择

路由器以任务嵌入 $e_k$ 为输入，通过 MLP 和 Softmax 计算任务-专家亲和度分数 $S_k$，再经 TopK 操作选取 $n_k$ 个激活专家及其权重：

$$S_k = \mathrm{Softmax}(\mathrm{MLP}(e_k)), \quad W_k, J_k = \mathrm{TopK}(S_k, \mathrm{topk}=n_k)$$

**关键设计**：路由发生在任务级别而非令牌级别——同一任务的所有时间步激活相同的专家子集。这与标准 MoE Transformer（逐令牌路由）形成根本区别，确保单个专家能捕获完整且连贯的任务动态，避免令牌级路由造成的动态碎片化。训练过程中 Softmax 的温度系数逐步退火至 1，以平滑专家选择。

#### 专家与共享 Transformer

被激活的专家 Transformer 并行处理各自的输入令牌，输出拼接后送入共享 Transformer 进行跨任务知识整合：

$$l_k^{1:t} = \mathrm{concat}[f_{\phi, j_k^1}(m_{j_k^1, k}^{1:t}), \dots, f_{\phi, j_k^{n_k}}(m_{j_k^{n_k}, k}^{1:t})]$$

$$h_k^{1:t} = F_{\phi}(l_k^{1:t}, e_k)$$

其中 $f_{\phi, j}$ 为第 $j$ 个专家 Transformer，$F_{\phi}$ 为共享 Transformer，$h_k^{1:t}$ 为最终隐藏状态。消融实验表明（Figure 8），移除专家 Transformer 比移除共享 Transformer 导致更严重的性能退化，验证了任务专用动态建模的核心地位。

#### 预测头

隐藏状态 $h_k^t$ 通过任务集群专用的预测头生成下一时刻的潜在状态分布、奖励、终止标志，以及任务索引：

$$\hat{\mathcal{Z}}_k^{t+1} = g_{\phi, i_k}^D(\hat{z}_k^{t+1} \mid h_k^t, e_k)$$

$$\hat{r}_k^t = g_{\phi, i_k}^R(h_k^t, e_k), \quad \hat{c}_k^t = g_{\phi, i_k}^C(h_k^t, e_k), \quad \hat{k} = g_{\phi}^T(h_k^t)$$

任务预测头 $g_{\phi}^T$ 为所有任务共享，输出当前轨迹所属的任务索引，是实现任务判别能力的关键组件。

### 世界模型训练损失

#### 各分量损失

单个任务 $k$ 在时刻 $t$ 的损失由六个分量组成：

$$\mathcal{L}_k(\phi) = \sum_t [ \mathcal{L}_{t,k}^{\mathrm{rec}}(\phi) + \mathcal{L}_{t,k}^{\mathrm{rew}}(\phi) + \mathcal{L}_{t,k}^{\mathrm{con}}(\phi) + \mathcal{L}_{t,k}^{\mathrm{task}}(\phi) + \beta_1 \mathcal{L}_{t,k}^{\mathrm{dyn}}(\phi) + \beta_2 \mathcal{L}_{t,k}^{\mathrm{rep}}(\phi) ]$$

具体定义：

$$\mathcal{L}_{t,k}^{\mathrm{rec}} = \| \hat{o}_k^t - o_k^t \|_2$$

$$\mathcal{L}_{t,k}^{\mathrm{rew}} = \mathrm{SymlogCrossEnt}(\hat{r}_k^t, r_k^t)$$

$$\mathcal{L}_{t,k}^{\mathrm{con}} = \mathrm{BinaryCrossEnt}(\hat{c}_k^t, c_k^t)$$

$$\mathcal{L}_{t,k}^{\mathrm{task}} = \mathrm{CrossEnt}(\hat{k}, k)$$

**任务预测损失** $\mathcal{L}_{t,k}^{\mathrm{task}}$ 是 MoW 的独特设计：强制世界模型从潜在状态中辨识当前任务，驱动任务嵌入学习到具有判别性的表示。消融实验证实移除该损失会导致整体性能显著下降（Figure 8）。

#### 动力学与表示损失

采用 KL 散度约束预测分布与编码器后验分布的一致性，裁剪至 1 nat 并配合停止梯度算子：

$$\mathcal{L}_{t,k}^{\mathrm{dyn}} = \max(1, \mathrm{KL}[\mathrm{sg}(\mathcal{Z}_k^{t+1}) \| \hat{\mathcal{Z}}_k^{t+1}])$$

$$\mathcal{L}_{t,k}^{\mathrm{rep}} = \max(1, \mathrm{KL}[\mathcal{Z}_k^{t+1} \| \mathrm{sg}(\hat{\mathcal{Z}}_k^{t+1})])$$

$\mathrm{sg}(\cdot)$ 为停止梯度操作：动力学损失仅优化预测器，表示损失仅优化编码器，防止潜在空间坍缩。

#### 和谐损失与平衡损失

多任务训练中不同任务的损失尺度差异显著，MoW 采用和谐损失（Harmonious Loss）动态调整各任务权重：

$$\mathcal{L}_{\mathcal{H}}(\phi) = \sum_{k=1}^{K} \frac{1}{\sigma_k} \mathcal{L}_k(\phi) + \ln(1+\sigma_k)$$

其中 $\sigma_k$ 为可学习参数，$\ln(1+\sigma_k)$ 作为正则化项防止权重退化为零。

此外，引入专家平衡损失鼓励所有专家被均匀激活，避免路由坍缩到少数专家：

$$\mathcal{L}(\phi) = \mathcal{L}_{\mathcal{H}}(\phi) + 0.1 \mathcal{L}_{\mathrm{bal}}(\phi)$$

消融实验表明（Appendix A.5），移除平衡损失会使训练对初始化敏感，导致专家利用不均衡。

### 智能体学习：潜在空间想象

Actor-Critic 智能体完全在世界模型生成的想象轨迹上训练，无需额外环境交互。

**Critic 损失**：使用 symlog 双热损失近似 $\lambda$-回报，配合 EMA 目标网络：

$$\mathcal{L}(\psi) = \sum_{k,t} [ \mathcal{L}_{\mathrm{sym}}(V_{\psi, i_k}(s_k^t) - \mathrm{sg}(R_{t,k}^{\lambda})) + \mathcal{L}_{\mathrm{sym}}(V_{\psi, i_k}(s_k^t) - \mathrm{sg}(V_{\psi^{\mathrm{EMA}}, i_k}(s_k^t))) ]$$

其中 $\lambda$-回报递归定义为：

$$R_{t,k}^{\lambda} = r_k^t + \lambda c_k^t [ (1-\lambda) V_{\psi, i}(s_k^{t+1}) + \lambda R_{t+1,k}^{\lambda} ]$$

**Actor 损失**：使用归一化优势函数的策略梯度替代损失，包含熵正则项：

$$\mathcal{L}(\theta) = \sum_{k,t} [ -\mathrm{sg}\left( \frac{R_{t,k}^{\lambda} - V_{\psi, i}(s_k^t)}{\max(1, S)} \right) \ln \pi_\theta(a_k^t | s_k^t) - \eta H(\pi_\theta(a_k^t | s_k^t)) ]$$

归一化因子 $S$ 为批次内 $\lambda$-回报的 95 分位数与 5 分位数之差：

$$S = \mathrm{percentile}(R_{t,k}^{\lambda}, 95) - \mathrm{percentile}(R_{t,k}^{\lambda}, 5)$$

### Warmup 与梯度聚类

训练启动阶段，MoW 使用单一共享 VAE 和预测器在固定回放缓冲区上进行短时离线自监督训练（约 5000 步）。在此期间记录各任务对 VAE 参数的梯度，基于梯度余弦相似性对任务进行聚类，将相似任务分配到同一 VAE 集群和预测器集群。聚类完成后，各集群独立微调，进入标准的在线 RL 训练循环。

**关键限制**：聚类仅在 warmup 阶段执行一次，训练过程中不再调整任务分组，可能无法适应非平稳的任务关系变化。实验表明（Figure 6），损失在数千优化步内收敛，warmup 长度在合理范围内的变化对最终性能影响较小。

## 实验与分析

### 核心实验结果

MoW在两大视觉多任务强化学习基准上验证了其有效性：Atari 100K（26款游戏）和Meta-World MT50（50个操作任务）。

**Atari 100K基准。** 在Atari 100K上，MoW以单一多任务模型达到**110.4%的人类归一化分数**（Human Normalized Mean），与26个独立单任务模型组成的STORM（114.2%）性能相当（Table 11）。关键差异在于模型效率：MoW总参数量为972.5 MB，相比STORM的1,977.5 MB减少了约**50%**（Figure 3中间面板）。这一结果表明，MoW通过模块共享在几乎不牺牲性能的前提下大幅压缩了模型规模。然而需注意，多任务学习的中位分数仅为37.7%，远低于均值110.4%，说明性能分布严重右偏——少数高分游戏（如Breakout、Pong）拉高了整体均值，而部分游戏（如Freeway、Private Eye）得分仍为0或极低，表明模型对某些任务动态的学习仍不充分。

![[assets/figures/papers/paper_list_l49_https_openreview_net_forum_id_qUQARlAx5y/figures/003_Figure_3.jpg]]
*Figure 3: Results of MoW on the Atari 100K benchmark (left) and the Meta-world benchmark (right). Compared to baseline STORM, MoW results a 50% reduction in model size (middle)*

![[assets/figures/papers/paper_list_l49_https_openreview_net_forum_id_qUQARlAx5y/figures/030_Table_11.jpg]]
*Table 11: Game scores and overall human-normalized performance on the 26 games in the Atari 100K benchmark*

**Meta-World MT50基准。** 在Meta-World MT50上，MoW以纯图像输入在仅**15M环境步**内达到**74.5%的平均成功率**，超越了所有现有方法（Table 1）。具体而言：
- 对比基于状态输入的多任务方法**MOORE**（Hendawy et al., 2023），MoW以74.5%超越其72.9%，且环境步数仅为后者的15%（15M vs 100M步）。
- 对比基于模型的视觉多任务方法**TD-MPC2**（Hansen et al., 2024，官方状态输入版本经浅层CNN改编为图像输入），MoW以74.5%大幅领先其25.3%（Figure 15），差距达49.2个百分点。
- 对比其他状态输入基线：**MTSAC**（49.3%）、**CARE**（50.8%）、**PaCo**（57.3%），MoW的图像输入方案在样本效率和最终性能上均形成碾压。

![[assets/figures/papers/paper_list_l49_https_openreview_net_forum_id_qUQARlAx5y/figures/004_Table_1.jpg]]
*Table 1: Results on MetaWorld MT50*

![[assets/figures/papers/paper_list_l49_https_openreview_net_forum_id_qUQARlAx5y/figures/032_Figure_15.jpg]]
*Figure 15: Comparison of MoW and TD-MPC2 on the Meta-World benchmark*

公平性说明：作者在Meta-World上统一使用修改后的corner2相机视角以保证视图一致性；STORM基线使用官方代码和配置复现；TD-MPC2的图像输入版本由作者为公平对比而专门适配。

### 参数可扩展性分析

MoW的模块化设计使其具备良好的参数可扩展性。Figure 4展示了分别增加专家Transformer数量和VAE集群数量对性能的影响：
- **增加专家Transformer数量**带来更明显的性能提升，表明任务间动力学差异主要通过时序建模模块捕捉。
- **增加VAE集群数量**同样提升性能，但边际收益较专家扩展更小，暗示视觉特征的任务特异性相对动力学建模而言次要。

这一发现验证了核心设计直觉：将MoE机制解耦于Transformer外部、按任务嵌入进行路由，能有效扩展模型容量而不陷入专家利用不均的困境。

### 消融研究

Figure 5和Figure 8的系统消融揭示了MoW各组件的因果贡献：

![[assets/figures/papers/paper_list_l49_https_openreview_net_forum_id_qUQARlAx5y/figures/006_Figure_5.jpg]]
*Figure 5: Ablation studies on muti-task STORM*

| 消融项 | 影响程度 | 因果机制 |
|--------|---------|---------|
| 移除任务预测损失 | **显著下降** | 任务预测头为路由器提供判别性梯度信号，缺失后专家路由退化，任务间干扰加剧 |
| 移除专家平衡损失 | **显著下降** | 训练对初始化敏感，部分专家被过度使用而其余闲置，MoE退化为少数专家的集成（Section 3.4） |
| 移除基于梯度的聚类 | **显著下降** | 任务间无结构化分组，所有任务强制共享相同模块，异质动力学相互干扰（Figure 8, Appendix A.5） |
| 移除专家Transformer（仅保留共享Transformer） | **严重退化** | 共享Transformer无法同时捕捉50个任务的异质动力学，性能崩塌 |
| 移除共享Transformer（仅保留专家Transformer） | **适度下降** | 专家间缺乏信息整合，跨任务共同知识无法被有效提取和复用 |

这些消融结果共同指向一个因果链条：**任务预测损失 → 判别性任务嵌入 → 有效的专家路由 → 平衡损失保证专家利用率 → 梯度聚类提供结构化参数共享 → 混合Transformer捕获异质与共性动力学**。任一环节断裂都会导致性能显著退化。

### 定性分析：想象重建质量

Figure 2展示了MoW与标准Transformer（vanilla STORM框架）在Atari 100K 26个任务上的想象重建对比。在16步想象轨迹的最终状态解码图像中，MoW展现出明显更优的任务判别能力和重建精度。标准Transformer在多任务设定下出现跨任务特征混淆，导致重建模糊或错误；而MoW通过任务专用VAE和专家路由，能够为每个任务保持高保真度的视觉重建。这一定性结果与定量性能提升相互印证，表明MoW的模块化潜在动力学建模确实缓解了多任务世界模型中的重建保真度瓶颈。

### 失败模式与局限性

尽管整体表现优异，MoW存在以下明确局限：

1. **任务间性能不均衡。** Atari 100K的中位分数（37.7%）与均值（110.4%）的巨大差距表明，模型过度依赖少数高分任务拉动整体指标，在Freeway、Private Eye等游戏上几乎完全失效。这提示当前的和谐损失加权（Equation 9）可能不足以平衡任务间的学习进度。

2. **静态任务聚类。** 基于梯度的聚类仅在warmup阶段执行一次（Section 3.6），无法在训练过程中动态调整任务分组。当任务关系随策略更新而发生非平稳变化时，固定的模块分配可能次优。

3. **大规模验证缺失。** 实验限于26款Atari游戏和50个Meta-World任务，尚未在全部57款Atari游戏或真实机器人平台上验证可扩展性。

4. **Warmup数据依赖。** 梯度聚类依赖warmup阶段的固定重放缓冲区数据（Algorithm 1），在实际应用中收集足够的随机交互数据可能存在工程挑战。

## 方法谱系与知识库定位

### 1. 直接继承与架构改造

MoW 的核心架构直接继承自单任务世界模型 **STORM**（Zhang et al., 2023），但在三个关键维度进行了结构性改造，以适配多任务场景：

**视觉编码器的模块化**。STORM 使用单一共享的类别型 VAE 对所有任务进行视觉编码。MoW 将其替换为一组任务专用 VAE，通过梯度聚类策略将视觉相似的任务分配到同一 VAE 集群。这一改造的动机在于：不同 Atari 游戏的视觉特征差异极大（如 Pong 的简洁线条 vs. Montezuma's Revenge 的复杂场景），单一 VAE 难以同时维持高重建保真度。

**时序模型的混合专家化**。STORM 使用标准 Transformer 作为序列模型。MoW 将其替换为“专家 Transformer + 共享 Transformer”的混合架构：任务路由器根据可学习的任务嵌入 $e_k$ 通过 TopK 操作选择激活的专家，各专家独立处理后，输出拼接送入共享 Transformer 进行跨任务知识整合。与标准 MoE 将专家内嵌于 Transformer 层的做法不同，MoW 将 MoE 机制解耦并置于 Transformer 外部，使每个专家能够捕获更完整的任务动力学。

**损失函数的任务感知扩展**。在 STORM 的标准世界模型损失（重建、奖励、终止、动力学、表示）之上，MoW 引入了任务预测损失和专家平衡损失，并采用和谐损失（Harmonic Loss）动态调整各任务损失权重。

### 2. 与同期多任务方法的对比定位

| 方法 | 类型 | 输入模态 | 世界模型架构 | 核心机制 | 性能参考 |
|------|------|----------|-------------|----------|----------|
| **MoW** (本文) | MBRL | 图像 | 混合专家 Transformer + 任务专用 VAE | 梯度聚类 + 任务条件路由 | MT50: 74.5% (15M步) |
| **STORM** (Zhang et al., 2023) | MBRL | 图像 | 单一 Transformer + 单一 VAE | 单任务专用，无共享 | Atari 100K: 114.2% (26个独立模型) |
| **MOORE** (Hendawy et al., 2023) | MFRL | 状态 | 无世界模型 | 模型无关 MoE，状态输入 | MT50: 72.9% (100M步) |
| **TD-MPC2** (Hansen et al., 2024) | MBRL | 状态/图像 | 单一 Transformer | 任务嵌入条件，无模块化 | MT50: 25.3% (视觉改编版) |
| **MTSAC** | MFRL | 状态 | 无世界模型 | 共享策略网络 | MT50: 49.3% |

**与 MOORE 的关键差异**：MOORE 是模型无关（model-free）方法，使用状态输入并在策略网络中引入 MoE，需要 100M 环境步达到 72.9%。MoW 作为基于模型的方法，仅用 15M 步即达到 74.5%，且使用更困难的图像输入。这体现了世界模型在多任务样本效率上的结构性优势。

**与 TD-MPC2 的关键差异**：TD-MPC2 使用单一 Transformer 和任务嵌入来处理多任务，缺乏模块化的动力学建模。在 Meta-World 上，其官方状态输入版本表现良好，但作者为其视觉改编版（浅层 CNN 处理图像）仅达到 25.3% 的成功率，暴露了单一架构在视觉多任务场景下的动力学建模不足。MoW 的混合专家设计直接针对这一瓶颈。

### 3. 适用边界与失效模式

**任务异质性依赖**。MoW 的优势高度依赖于任务间存在可被梯度聚类捕获的异质性。若所有任务动力学高度相似（如同一环境的轻微变体），模块化带来的增益可能被路由开销抵消，此时单一共享模型可能更优。论文未对此边界情况进行系统验证。

**性能分布不均**。在 Atari 100K 的 26 款游戏中，MoW 的中位分数（37.7%）远低于均值（110.4%），表明少数高分游戏（如 Boxing、Kung Fu Master）拉高了整体指标，而 Freeway、Private Eye 等游戏得分仍为 0 或极低。这说明 MoW 的模块化机制未能有效解决某些任务上的根本性学习困难，模型可能过度依赖表现较好的任务来驱动共享模块的更新。

**静态聚类的局限**。基于梯度的任务聚类仅在 warmup 阶段执行一次，训练过程中任务分组保持不变。这一设计假设任务关系是静态的，但在非平稳环境或课程学习中，任务间的相似性可能随训练进程演变。静态聚类无法适应这种动态变化。

**计算开销的隐性成本**。虽然 MoW 将模型参数减少了 50%（972.5 MB vs. 1,977.5 MB），但专家路由和多个前向路径引入了额外的计算开销。论文未报告推理延迟或训练吞吐量的对比数据，实际部署效率需要进一步评估。

### 4. 开放问题

1. **动态模块重分配**：任务嵌入和专家路由能否在训练过程中自适应地重新分配模块，而非局限于 warmup 阶段的静态聚类？这需要设计在线聚类或元学习机制，使任务分组随训练动态演化。

2. **零样本泛化**：MoW 当前依赖 warmup 阶段收集所有任务的交互数据进行聚类，无法处理训练时未见过的任务。如何将模块化架构扩展到连续变化的任务分布或完全未见任务，是一个重要的扩展方向。

3. **真实机器人部署**：warmup 阶段需要在固定回放缓冲区上进行离线世界模型训练，这在真实机器人场景中意味着需要预先收集所有任务的随机交互数据。如何高效地完成这一数据收集，或设计无需 warmup 的在线聚类方案，是实际部署的关键障碍。

4. **任务学习不平衡的缓解**：针对 Freeway 等得分持续为 0 的任务，当前的和谐损失加权机制似乎不足以解决极端的学习不平衡。是否需要引入更主动的干预机制（如动态损失调度、任务课程、或对困难任务的专家专用化）值得探索。

5. **规模上限验证**：论文仅在 26 款 Atari 游戏和 50 个 Meta-World 任务上验证，尚未在更大规模任务集（如全部 57 款 Atari 游戏、多具身机器人任务集）上测试。随着任务数量增长，专家数量、聚类质量和路由效率之间的权衡关系需要更系统的研究。

## 原文 PDF

![[paperPDFs/ICLR_2026/Mixture_of_World_Models_Scaling_Multi_Task_Reinforcement_Learning_with_Modular_Latent_Dynamics.pdf]]
