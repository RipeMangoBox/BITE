---
title: "Ada-Diffuser: Latent-Aware Adaptive Diffusion for Decision-Making"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/Ada_Diffuser_Latent_Aware_Adaptive_Diffusion_for_Decision_Making.pdf
project_link: https://sites.google.com/view/ada-diffuser
code_link: null
aliases:
- Ada-Diffuser
tags:
- ICLR_2026
- topic/reinforcement_learning_planning_agents
- topic/reinforcement_learning_planning_agents/planning_control
core_operator: "通过引入基于块的最小充分观测进行潜在识别，并利用因果自回归去噪与交替的之字形采样，将潜在变量一致地集成到扩散生成过程中，从而自适应地调整行为。"
primary_logic: "理论上证明只需少量连续观测即可识别潜在因子；据此设计可联合学习潜在表示和观测分布的框架，使扩散模型能够在线适应潜在动态。"
claims:
- "Ada-Diffuser-Planner 在 Cheetah-Wind-E 环境中取得最佳回报 -68.9±7.6，显著优于 Diffuser (-120.4) 和 DF (-105.8)。"
- "移除潜在识别模块导致 Cheetah-Wind-S 规划器回报从 -73.5 降至 -103.5，突显潜在建模的关键作用。"
- "使用因果去噪和 zig-zag 采样（反向精炼）有效减少后验不匹配，改善潜在识别（线性探针 MSE 从 0.28 降至 0.18）。"
- "Cheetah-Wind-E (planner) 上 Return = -68.9 ± 7.6"
---

# Ada-Diffuser: Latent-Aware Adaptive Diffusion for Decision-Making

> [!tip] 核心洞察
> 理论上证明只需少量连续观测即可识别潜在因子；据此设计可联合学习潜在表示和观测分布的框架，使扩散模型能够在线适应潜在动态。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | Ada-Diffuser：潜在感知的自适应扩散决策模型 |
| 英文题名 | Ada-Diffuser: Latent-Aware Adaptive Diffusion for Decision-Making |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=PKifFVXtSR) · [Project](https://sites.google.com/view/ada-diffuser) |
| Topic | #topic/reinforcement_learning_planning_agents #topic/reinforcement_learning_planning_agents/planning_control |
| Method | Ada-Diffuser |
| Dataset | Cheetah-Wind-E (planner), Cheetah-Vel-E (planner), Maze2D-Large, Kitchen-Partial |

> [!tip] 效果简介
> - Cheetah-Wind-E (planner) 上，Return 为 -68.9 ± 7.6，对比 -120.4 ± 12.7 (Diffuser)，变化 +51.5。
> - Cheetah-Vel-E (planner) 上，Return 为 -45.8 ± 9.5，对比 -102.4 ± 18.2 (Diffuser)，变化 +56.6。
> - Maze2D-Large 上，Return 为 161.4 ± 3.2，对比 123.0 ± 4.8 (Diffuser)，变化 +38.4。

## 概要

扩散决策模型（如Diffuser、Decision Diffuser、Diffusion Policy）在离线强化学习和规划中取得了显著进展，但它们通常忽略环境中随时间变化的潜在因素（例如风力、方向偏好或动力学参数漂移）。在这种部分可观察条件下，环境的真实动力学和奖励函数会随潜在变量改变，导致固定模型无法准确建模序列分布，规划或策略难以自适应调整。现有扩展尝试通过元学习或上下文推理引入潜在表示，但缺乏对"需要多长观测才能可靠识别潜在因素"的理论理解，也未在扩散生成过程中显式对齐潜在后验与序列生成。

本文提出**Ada‑Diffuser**，一个潜在感知的自适应扩散框架。其核心思想源于理论分析：在温和的条件下，仅需连续 4 个观测（状态‑动作对）即可在线识别潜在因子（Theorem 1）。据此，框架由两大模块构成：
- **潜在因子识别块**：使用 VAE 结构从最小充分观测块中推断潜在变量后验，并通过对比损失减少先验‑后验不匹配；
- **因果扩散模型**：采用因果自回归去噪调度和交替的**之字形采样**（zig‑zag sampling），将潜在估计一致地融入扩散生成过程，从而根据当前潜在动态调整行为。

与无条件或简单条件扩散方法比较，Ada‑Diffuser 在四个关键维度改进了设计：（1）显式建模环境潜在因子，而非忽略；（2）去噪过程遵循时间因果顺序，而非同步去噪整个轨迹；（3）采样时交替更新状态‑动作对和潜在变量，而非单向采样；（4）在线仅需少量连续观测即可识别，而无需完整轨迹历史。

实验表明，Ada‑Diffuser‑Planner 在受显式潜在影响的 Cheetah‑Wind‑E 环境中获得 **−68.9 ± 7.6** 的平均回报，相较 Diffuser 的 −120.4 提升超过 40；在 Cheetah‑Vel‑E 上提升约 55 点。在无明显设计潜在因素的环境（如 Maze2D、Kitchen‑Partial、Robomimic 机器人操作任务）中，该方法同样稳定优于 Diffuser、Decision Diffuser 等基线。消融实验进一步确认：移除潜在识别模块会使 Cheetah‑Wind‑S 规划器回报从 −73.5 降至 −103.5，去掉之字形采样或反向精炼也会造成显著性能退化；线性探针 MSE 从 0.28 降至 0.18 证明了后验对齐的有效性。这些结果共同说明，通过理论指导下的潜在建模与因果扩散设计，Ada‑Diffuser 能在动态环境下提升规划与策略的自适应能力。



扩散模型在离线规划与策略学习中展现出强大的轨迹生成能力。以 Diffuser、Decision Diffuser (DD) 和 Diffusion Policy (DP) 为代表的系列工作，将决策问题建模为在噪声空间中逐步去噪以生成高质量动作序列的过程，其前向加噪机制可形式化为
$$q(\mathbf{x}^t \mid \mathbf{x}^{t-1}) = \mathcal{N}(\mathbf{x}^t; \sqrt{\alpha_t} \mathbf{x}^{t-1}, (1-\alpha_t) \mathbf{I}),$$
并通过训练一个反向去噪网络逼近真实数据分布。这些方法在 MuJoCo、Maze2D、Kitchen 等标准基准上取得了优异表现，但其有效性建立在环境动力学平稳且完全由观测状态决定的假设之上。

然而，真实任务中普遍存在时变潜在因素——例如，风阻的周期性变化会持续影响动力学，目标方向或奖励权重的漂移会改变最优行为，而此类因素通常无法从单步状态中直接观测。这类问题自然适合用**上下文马尔可夫决策过程**（contextual MDP）描述，即
$$\mathcal{M} = (\mathcal{S}, \mathcal{A}, \mathcal{C}, \mathcal{T}, \mathcal{R}, \gamma),$$
其中环境转移 $\mathcal{T}$ 与奖励 $\mathcal{R}$ 依赖时变的潜在上下文 $\mathcal{C}$。但现有的扩散决策模型几乎都未显式建模这一潜在结构：Diffuser 采用无条件去噪，完全忽略上下文信息；DD 尽管引入了条件生成，但所依赖的条件多为预设的回报或目标，而非从观测中动态推断的隐藏状态；DP 则直接预测动作，同样缺乏对潜在动力学的表征能力。这些设计导致模型在部分可观察或非平稳环境中出现严重的规划偏差——例如在 Cheetah-Wind-E 环境中，Diffuser 的平均回报仅为 -120.4，远低于可自适应调整行为的 Ada‑Diffuser 所取得的 -68.9（Table 1, 5 seeds）。从机制上看，症结在于：第一，缺乏从有限历史中**在线识别**潜在因子的机制；第二，去噪过程采用全序列同步更新，破坏了轨迹内部的因果关系，无法与时变潜在变量形成一致的对齐；第三，采样过程无法交替更新对潜在变量的信念而使规划逐渐偏离真实动态。

为此，本文的核心动机是回答两个开放问题：**最少需要多少连续观测即可可靠识别控制环境的潜在因子？以及如何将这种识别机制无缝地嵌入扩散生成过程，以实现自适应规划与策略学习？** 理论分析（Theorem 1）表明，仅需 4 个连续状态就可在可逆变换的意义上识别潜在上下文，这为轻量级在线适应提供了理论依据。受此启发，本文提出 Ada‑Diffuser 框架，其设计原则如下：引入一个块状潜在识别模块，从最小充分观测中推断潜在变量的后验分布；构造一种因果自回归的去躁调度，使去噪步骤按时间顺序逐块进行，并与潜在估计协同精炼；在推理时采用之字形（zig‑zag）采样，在生成状态‑动作对与更新潜在变量之间交替迭代，从而保持后验信念与环境动态的一致性。这一思路直接回应了前述瓶颈，即通过"识别‑精炼‑条件生成"的闭环，使扩散模型能够连续适应不可见的时变因素，避免性能随环境变化而持续退化。后续章节将详细阐述该框架的理论基础与实现细节，并在一系列具有显式或隐式潜在因素的环境中对其进行验证。



## 核心方法与创新机理

现有基于扩散的决策模型（如 Diffuser、Decision Diffuser）将规划或策略学习建模为轨迹生成问题，通过同时去噪整条序列来恢复高质量行为。然而，这类方法隐含地假定环境动力学与奖励函数是平稳的，忽略了部分可观测情境下广泛存在的时变潜在因素（如变化的风力、不同场景下的目标偏好）。当动力学或奖励发生偏移时，模型的生成分布与实际环境产生结构性错配——即 **后验不匹配**——导致规划轨迹不可靠、策略无法自适应。这是当前扩散规划器在信息受限条件下性能退化的关键瓶颈。

Ada-Diffuser 针对上述瓶颈进行了三项结构性变革：

1. **显式潜在因子识别与条件生成**  
   基线方法不显式建模环境潜在变量，扩散过程完全依赖可观测轨迹序列。Ada-Diffuser 引入一个轻量级的 **潜在因子识别模块**（基于 VAE 与对比损失），仅利用一个最小充分观测块（理论证明只需 4 个连续观测即可实现潜在变量在可逆变换下的识别，实践中常使用 6–20 步）来动态推断潜在上下文的后验分布 $p(\mathbf{c}_t \mid \mathbf{x}_{t-2:t+1})$。该潜在变量随后作为条件输入指导扩散生成，使模型能够在线适应环境变动，而无需重新训练或依赖全轨迹历史。

2. **因果自回归去噪**  
   Diffuser 等基线对整条轨迹同时加噪与去噪，违反了时序生成的因果结构。Ada-Diffuser 采用 **因果自回归去噪方案**：前向加噪仅沿时间方向逐块扩散，逆向去噪时也按时间顺序逐步恢复状态-动作对，并将去噪过程中更新的潜在估计融合进下一时刻的条件输入。这种设计将去噪步骤与底层因果图对齐，显著降低了后验不匹配。在 Cheetah-Wind 环境下，移除该结构（即回退到同时去噪）导致回报从 -73.5 降至 -91.6（Table 2），同时线性探针 MSE 从 0.18 上升至 0.23（Table A16）。

3. **之字形采样与反向精炼**  
   单一方向采样（如纯前向或全序列并行）无法在生成过程中同步精炼潜在变量。Ada-Diffuser 引入 **之字形采样**：在前向生成当前步的状态-动作对后，立即用新观测对之前块内的潜在变量进行 **反向精炼**，形成"去噪-精炼"交替循环。精炼仅复用同一个去噪网络并附加对比损失，几乎不增加额外参数。消融实验显示，单独移除精炼步骤回报下降约 8.5 个单位（Table 2），且线性探针 MSE 从 0.18 增至 0.28（Table A16），证明该机制有效消除了潜在后验与真实分布之间的偏差。

上述三个改变槽（changed slots）共同作用，使得扩散模型首次能够以统一框架在隐变量上下文 MDP 中进行在线自适应。相较 Detach + DynaMITE、LILAC 及 MetaDiffuser 等面向上下文适应的扩展方法，Ada-Diffuser 无需额外的元学习或迭代推断机制即可即时响应环境变化，且其理论保证（定理 1）为最小观测块大小提供了可解释的下界；实验上，在 Cheetah-Vel-E 和 Cheetah-Wind-E 等包含显式潜在动力学与奖励变化的任务中，Ada-Diffuser-Planner 回报分别达到 **-45.8±9.5** 和 **-68.9±7.6**，较 Diffuser 提升超过 50 分（Table 1）。

> 本节聚焦关键创新点，具体实现细节与全量实验数据见第 4 节及附录 A。



![[assets/figures/papers/iclr26_0006_PKifFVXtSR_Ada-Diffuser_Latent-Aware_Adaptive_Diffusion_for/figures/003_Figure_2.jpg]]
*Figure 2: Overview of the Ada-Diffuser framework. The modular design consists of two main stages: latent context identification (Stage 1, Section 4.2), followed by a causal diffusion model (Stage 2, Section 4.3) that models the generative structure of the trajectories. The learned model is then used for planning or policy learning conditioned on the inferred latent context*

![[assets/figures/papers/iclr26_0006_PKifFVXtSR_Ada-Diffuser_Latent-Aware_Adaptive_Diffusion_for/figures/017_Figure_13.jpg]]
*Figure 13: Figure A2: An illustration of the zig-zag sampling process with a block of 4 time steps. ↓ and | indicate denoising and identity mapping, respectively*

Ada-Diffuser 针对部分可观察环境中时变潜在因素（如变化的动力学、奖励函数）导致的建模不精确问题，将潜在因子的在线识别与扩散生成过程深度整合。整体框架遵循**先识别再生成**的两阶段设计（图 2），核心模块与数据流如下。

1. **输入与目标**  
   - 输入：从离线数据集中采样的轨迹段（连续观测 $\mathbf{x}_{t-k:t}$，含状态、动作、奖励）。  
   - 目标输出：条件于推断潜在变量的规划轨迹（对 planner）或执行动作（对 policy），以适应环境在动力学 ${\mathbf{c}}_t^s$ 和 / 或奖励 ${\mathbf{c}}_t^r$ 上的实时变化。  

2. **阶段 1：潜在因子识别模块**  
   - 基于定理 1（仅需少量连续观测即可识别潜在因子，可逆变换意义上），该模块从**最小充分观测块**中推断潜在变量后验 $q(\mathbf{c}_t \mid \mathbf{x}_{t-\tau:t})$。  
   - 实现上使用轻量变分自编码器（VAE）结构，先验与后验编码器均为 GRU + MLP，输出高斯分布；训练时采用对比损失 $\mathcal{L}_{\mathrm{contrast}}$，促使先验损失大于后验损失，以此对齐后验分布（附录 D.2.2）。  

3. **阶段 2：因果扩散模型**  
   - 将轨迹生成过程建模为 Markov 序列，扩散模型在**潜在上下文马尔可夫决策过程**（latent contextual MDP）  
     $$\mathcal{M} = (\mathcal{S}, \mathcal{A}, \mathcal{C}, \mathcal{T}, \mathcal{R}, \gamma)$$  
     上进行条件生成，其中 $\mathcal{T}(\mathbf{s}_t \mid \mathbf{s}_{t-1}, \mathbf{a}_{t-1}, \mathbf{c}_t)$ 显式依赖潜在变量。  
   - **因果去噪调度**：不再同时去噪整条序列，而是按时间步自回归地逐块去噪，使去噪步骤与轨迹的因果结构对齐（Section 4.3）。  
   - **去噪‑精炼机制**：在去噪过程中交替使用先验潜在样本和经后验更新的潜在样本；具体而言，每完成一步去噪后，利用对比损失对潜在估计进行反向精炼，以减小后验不匹配（线性探针 MSE 从 0.28 降至 0.18，Table A16）。  

4. **之字形采样**  
   - 在推理阶段，采用 zig‑zag 采样方案交替执行两个操作：采样下一个状态‑动作对 $\mathbf{x}_{t+1} \sim p_\theta(\mathbf{x}_{t+1} \mid \mathbf{x}_t, \mathbf{c}_t)$，以及用新的观测更新潜在变量 $\mathbf{c}_{t+1}$。这种交织方式确保潜在变量始终反映最新的环境动态，避免规划后期因上下文陈旧而漂移。  

5. **动作恢复（仅状态规划时）**  
   - 若任务仅提供不含动作的状态演示（action‑free demonstrations），框架引入**逆动力学模型**（IDM），以 MLP 从状态 $\mathbf{s}_t$、$\mathbf{s}_{t+1}$ 和潜在变量 $\mathbf{c}_t$ 恢复动作 ${\mathbf{a}}_t$，使规划器在缺少动作标签时仍能生成可执行策略（Section 4.3, Appendix D.2）。  

**模块间关系与数据流摘要**  
- 第一阶段提取的潜在变量作为第二阶段扩散模型的条件输入，贯穿训练与推理全过程。  
- 扩散模型输出的去噪轨迹一方面用于规划或策略学习，另一方面反馈给潜在识别模块以更新后验——形成 "生成‑推断" 闭环。  
- 消融实验确认，移除潜在模块或精炼步骤均导致性能显著退化（如 Cheetah‑Wind‑S 规划器回报从 −73.5 降至 −103.5 或 −91.6；Table 2），表明各模块对自适应决策不可或缺。

> 注：本节描述的整体框架对应论文第 4 节；扩散基础（前向加噪 $q(\mathbf{x}^t \mid \mathbf{x}^{t-1}) = \mathcal{N}(\mathbf{x}^t; \sqrt{\alpha_t} \mathbf{x}^{t-1}, (1-\alpha_t) \mathbf{I})$）在 Background 部分已有铺垫，此处不再展开推导。



Ada-Diffuser 的核心由两条主线构成：**潜在因子识别模块**与**因果扩散生成模型**。前者利用最小充分观测块在线推断时变潜在变量；后者将该潜在变量一致地注入自回归去噪过程，通过之字形采样（zig-zag sampling）和"去噪-再精炼"机制实现潜在‑观测的联合对齐。以下围绕关键模块与对应公式展开。

### 潜在上下文 MDP 的形式化
为刻画环境中的时变潜在因素，Ada-Diffuser 引入上下文 MDP：

$$
\mathcal{M} = (\mathcal{S},\, \mathcal{A},\, \mathcal{C},\, \mathcal{T},\, \mathcal{R},\, \gamma)
$$

其中 $\mathcal{C}$ 为潜在上下文空间。时刻 $t$ 的状态转移和即时奖励同时受显式状态‑动作对与潜在变量 $\mathbf{c}_t$ 的影响：

$$
\mathcal{T}(\mathbf{s}_t \mid \mathbf{s}_{t-1}, \mathbf{a}_{t-1}, \mathbf{c}_t),\quad
\mathbf{c}_t = h(\mathbf{c}_{t-1}, \eta_t)
$$

$\eta_t$ 为独立噪声，$h$ 为潜在动态函数。这一形式化将环境变化（如风力、速度偏好）建模为可在线推理的隐变量。

### 潜在因子识别：最小充分块与可识别性
潜在识别模块基于 **Theorem 1** 构建：仅需连续 **4 个观测**即可在线识别 $\mathbf{c}_t$ 至可逆变换的精度：

$$
p(\mathbf{c}_t \mid \mathbf{x}_{t-2:t+1}) \;\; \text{identifiable up to invertible transformation}
$$

式中 $\mathbf{x}$ 表示可观测的状态‑动作（或仅状态）片段。实践中使用 6‑20 步的观测块替代理论上的 4 步，以稳定推断。该模块采用 **VAE 架构**，通过时域先验‑后验对齐和对比损失，将当前观测块映射为一组高斯参数，输出潜在后验样本。

### 扩散骨架与前向加噪
Ada-Diffuser 的生成侧基于扩散模型。对完整轨迹（或轨迹块）$\mathbf{x}^0$，前向加噪服从：

$$
q(\mathbf{x}^t \mid \mathbf{x}^{t-1}) = \mathcal{N}\bigl(\mathbf{x}^t; \sqrt{\alpha_t}\,\mathbf{x}^{t-1},\; (1-\alpha_t)\mathbf{I}\bigr)
$$

其中 $\alpha_t$ 按噪声调度递减。后续的所有去噪，均以此过程作为逆过程的定义基础。

### 因果自回归去噪与"去噪-再精炼"
与标准扩散模型中同时处理整个序列不同，Ada-Diffuser 采用**因果自回归去噪**：按时间步逐渐生成 $[\mathbf{x}_1, \mathbf{x}_2, \dots]$，每一步生成都以前一时间步的输出去噪结果和当前估计的 $\mathbf{c}_t$ 为条件。这一设计天然符合"轨迹 = 环境 + 潜在因果"这一生成结构。

为防止潜在后验与生成过程出现系统偏差，框架引入 **Denoise‑and‑Refine** 机制：在每一次去噪更新后，用同一去噪网络但分别输入**潜在先验**（来自前续时间步）与**潜在后验**（基于在线观测更新）进行两步精炼，并通过对比损失驱动对齐：

$$
\mathcal{L}_{\text{contrast}} = \max\!\left\{0,\; \mathcal{L}_{\text{prior}} - \mathcal{L}_{\text{post}}\right\}
$$

其中 $\mathcal{L}_{\text{prior}}, \mathcal{L}_{\text{post}}$ 分别对应使用先验样本与后验样本时的去噪误差。该损失迫使后验样本至少不差于先验样本，从而缩小后验不匹配。

### 之字形采样与逆动力学模型
推理时采用**zig‑zag 采样**：交替执行"采样状态‑动作对"与"基于新观测更新潜在变量"两个步骤，使得潜在估计随生成不断精化。这一采样策略与因果去噪和对比精炼配合，使得后验对齐在线且稳定。

当仅有状态观测而无动作标签时，Ada-Diffuser 可接入**逆动力学模型（IDM）**，其直接拟合 $p(\mathbf{a}_t \mid \mathbf{s}_t, \mathbf{s}_{t-1}, \mathbf{c}_t)$，用于从状态和潜在情境中恢复动作。该模块属于辅助模块，无额外公式，但其存在大幅扩展了方法的适用场景（例如利用机器人自由演示数据）。

通过上述模块级联，Ada-Diffuser 将潜在因子识别、因果生成、扩散对齐整合为单一的可训练框架，形成了理论保证与实践性能兼备的自适应决策模型。



## 实验与关键发现

### 主结果：显式潜在环境下的规划与策略提升

在精心构造的时变潜在因素环境（Cheetah‑Wind‑E/Vel‑E 等）中，**Ada‑Diffuser‑Planner 对伴随动力学和奖励变化的轨迹规划获得了显著增益**（Table 1/Table A4）。以 Cheetah‑Wind‑E 为例，该方法达到回报 −68.9±7.6，而最优对比方法 Diffuser 仅为 −120.4±12.7（提升约 50 分）；在 Cheetah‑Vel‑E 上回报也从 −102.4±18.2 提升至 −45.8±9.5。这一差距的**关键瓶颈**在于基线扩散模型忽略潜在时变因素，导致在部分可观察环境下生成行为与真实动力结构失配。Ada‑Diffuser 通过最小充分观测块（4 个时步）在线推断潜在变量，并以此条件化扩散生成过程，实现了对环境变化的自适应。

![[assets/figures/papers/iclr26_0006_PKifFVXtSR_Ada-Diffuser_Latent-Aware_Adaptive_Diffusion_for/figures/007_Table_1.jpg]]
*Table 1: Results (5 seeds) on Ada-Diffuser-Planner with latent factors that affects dynamics and rewards. $\mathbf { c } ^ { s }$ and $\mathbf { c } ^ { r }$ indicate the changes on dynamics and reward, E and S represent the episodic and time-step changes. All results are averaged over 5 random seeds

更一般的离线基准（Maze2D‑Large、Kitchen‑Partial 等）上，即使任务没有显式设计潜在因子，Ada‑Diffuser 仍优于 Diffuser 和 DF 等无条件/条件扩散方法（Figure 5, Table A6/A7）。例如，Maze2D‑Large 平均回报从 123.0（Diffuser）提升至 161.4（+38.4），Kitchen‑Partial 成功率从 55.8% 提高至 70.1%。这验证了框架能**从观测轨迹中自动捕获隐式潜在变化**，并用于改善规划。

Figure 4(a) 进一步揭示了**潜在识别质量与决策性能的正相关性**：在 Cheetah‑Wind 环境中，线性探针 R² 随块大小增加而上升，同时归一化奖励同步提升，印证了"准确识别潜在因子⇒更优规划"的因果逻辑。同时，动作免掉的规划结果（Figure 4(b), Table A3）表明，即使仅依赖状态观测，通过逆动力学模型（IDM）结合潜在推理仍可实现有效控制，且优于专门的动作免去方法 LDP。

![[assets/figures/papers/iclr26_0006_PKifFVXtSR_Ada-Diffuser_Latent-Aware_Adaptive_Diffusion_for/figures/005_Figure_4.jpg]]
*Figure 4: (a). Identification Results (i.e., Linear Probing MSE, R2) and normalized rewards on the Cheetah environment with time-varying wind as the latent factor, evaluated across different block sizes. (b). Results (i.e., average success rate) on planning with action-free demonstrations on Robomimic benchmark. "AF" denotes Action-free*

### 消融：组件解耦与瓶颈定位

Table 2 的消融实验明确了 **三个核心组件的贡献**（以 Cheetah‑Wind‑S 规划器为标准）：

![[assets/figures/papers/iclr26_0006_PKifFVXtSR_Ada-Diffuser_Latent-Aware_Adaptive_Diffusion_for/figures/008_Table_2.jpg]]
*Table 2: Ablations on Cheetah-Wind-S (planner) and LIBERO (DP-policy)*

1. **潜在因子识别模块移除（w/o latents）** 导致回报从 −73.5 骤降至 −103.5（降幅 ≈30），直接证实了局部观测情境下显式建模潜在变化是性能提升的主因。
2. **之字形采样移除（w/o zig‑zag）** 使回报降至 −91.6，说明仅用单向采样无法充分恢复潜在后验与状态‑动作的联合一致性。
3. **反向精炼步骤移除（w/o refine）** 回报降至 −82.0，揭示了在去噪过程中对齐先验与后验的重要性。

进一步的潜在识别精度直接证据来自 Table A16：完整模型线性探针 MSE 仅 0.18，而去除精炼和之字形采样分别涨至 0.28 和 0.23，证实**因果自回归去噪与交替精炼机制有效减轻了后验不匹配**，使推断出的潜在变量与真实风力变化更一致。

设计选择层面，潜在维度的缩放（0.5×–6×）对性能影响有限（Table 2 下半部分），表明识别模块在一定容量范围内鲁棒；不同噪声调度（线性/逻辑/Sigmoid）同样未导致显著差异（Table A15），表明方法对超参数不敏感。

### 关键图表证据强度与总结

- **Table 1 (及 Table A4)**：5 种子平均，各环境标准差较小，置信度 >0.95；同类对比均覆盖条件扩散（DD）、元学习（MetaDiffuser）以及潜在上下文方法（DynaMITE, LILAC），公平性得以保证。
- **Table 2**：消融在相同任务和种子下进行，改变单一组件即可观测回报断崖式下降，说明组件间强因果依赖。
- **Figure 4(a)**：识别质量‑奖励趋势在多个块大小上稳定，且与理论最小块大小（4 步）相容；块大小超过 15 左右后收益趋平，符合定理 1 中"充分"块的预期。
- **Figure 4(b)** 及 Table A3：动作免掉场景下相对 LDP 提升明显，说明潜在推断可部分补偿动作信息的缺失。

综合来看，Ada‑Diffuser 的性能提升可归结为**"最少观测块在线识别潜在因子→因果条件化扩散生成→反向精炼对齐后验"→自适应行为"的因果链**；每项组件的移除都会直接击中这一链条的薄弱点，消融证据强度高且一致。

（注：论文未报告明确失败模式或退化情景，若需讨论边缘情形，建议参照附录 A5 中的计算开销对比或 Picard 加速效果 Table A13，可手工核实推理效率与精度权衡。）

### 补充图表

![[assets/figures/papers/iclr26_0006_PKifFVXtSR_Ada-Diffuser_Latent-Aware_Adaptive_Diffusion_for/figures/031_Table_10.jpg]]
*Table 10: (MSE) of this probe for three variants: (i) the full model with backward refinement and zig–zag; (ii) without refinement; and (iii) without zig–zag. Table A16: Linear probing MSE for recovering the ground-truth wind latent on CHEETAH (changing wind). Lower is better*



## 定位与知识库关联

### 与基线方法的关系及定位

Ada‑Diffuser 的出发点是现有扩散决策模型（Diffuser、Decision Diffuser、Diffusion Policy 等）将轨迹生成视为独立同分布的去噪过程，未显式建模环境中时变的潜在因素（如动态变化、奖励变异），因此在部分可观察且存在潜在漂移的任务中规划或策略无法自适应。Ada‑Diffuser 与此类基线的关系可概括为：**保留了扩散生成框架的表达力，但通过融入潜在识别和因果结构，将模型从"无条件/条件轨迹生成器"变为"潜在感知的自适应生成器"**。具体差异体现在四个关键槽位（表见正文Table 1‑2 消融及方法对比）：

- **潜在因子建模**：Diffuser、Decision Diffuser 等没有显式的潜在变量；Ada‑Diffuser 引入基于块的最小充分观测的潜在识别模块（Section 4.2），将推断的潜在变量作为条件注入扩散生成过程。与同样使用潜在上下文的 DynaMITE 和 LILAC 相比，Ada‑Diffuser 的潜在模块直接内嵌于扩散去噪过程，利用因果依赖和对比精炼进行在线对齐，而非以插件方式为规划器提供额外的上下文表征。
- **去噪过程**：基线方法同时去噪整个序列，忽略时间因果。Ada‑Diffuser 采用**因果自回归去噪**（Section 4.3），即按时间步逐块执行去噪，并在每个块上反向精炼潜在估计，使训练信号与数据生成机制一致，降低了后验不匹配。
- **采样方案**：基线使用单一方向（前向或全序列）采样；Ada‑Diffuser 设计**之字形采样**（Section 4.3），交替采样状态‑动作对和更新潜在变量，使得潜在估计随采样迭代在线精化。
- **观测需求**：基线通常需要完整轨迹或大量多环境数据；Ada‑Diffuser 基于定理 1 证明只需 4 个连续观测即可在理论上识别潜在因子（实践中使用 6–20 步），具备在局部时间窗口上进行在线适应的能力。在这一约束下，模型对离线数据集的结构性需求下降，但对数据中的潜在变异覆盖率提出要求。

从方法谱系看，Ada‑Diffuser 结合了扩散生成模型、潜在变量模型和结构因果推理，可视为**扩散决策模型中因果潜变量增强的分支**。它与 MetaDiffuser 不同：后者依赖元学习适配新环境，需要在训练时看到多重环境；而 Ada‑Diffuser 基于单环境中的短暂观测块进行在线潜在识别，不要求预先区分不同环境标签。与基于扩散的 Q 学习方法（LDCQ、IDQL）相比，Ada‑Diffuser 更偏向以生成式规划/策略的方式统一处理状态‑动作序列，可能更容易扩展到免动作规划的设定。

### 适用边界与有效范围

Ada‑Diffuser 的有效性建立在以下前提上，也划定了其适用范围：

1. **存在可识别的时变潜在因子**。当潜在因子对动态或奖励的因果作用足够强且满足可分离性时，识别与条件化带来的提升显著（Cheetah‑Wind‑E 回报从 Diffuser 的 -120.4 提升至 -68.9，Table 1）。若潜在影响微弱（例如过渡可分离性很低），则潜在模块可能退化为冗余的开销（Figure A1 中弱上下文设置的回报降幅很小）。
2. **离线数据集覆盖潜在变异范围**。潜在识别需要从观测块中学习先验/后验分布，因此训练数据应包含足够的潜在变化样本；若数据集仅含单一潜在状态，则模块无法学到有意义的潜在表示。
3. **合适的块大小**。理论最小块为 4 步，实际块大小需大于等于潜在效应的滞后窗口，同时又不能过大以致超出模型容量。实验表明块大小为 10‑15 时识别 $R^2$ 和归一化回报同时达到峰值（Figure 4a）；在延迟或累积效应下更大的块（至 20）可改善识别但增加计算量（Table A2）。因此块大小选择应根据环境特性调节。
4. **任务类型与状态‑动作空间**。实验中主评估环境为 MuJoCo 连续控制（Cheetah）、迷宫导航（Maze2D）、机器人操作（Kitchen、Robomimic、LIBERO），表明方法适用于**低维状态‑动作连续/离散混合空间**。在高维图像输入任务上需要额外的编码器，其潜在识别的稳定性尚需验证。
5. **离线规划/策略学习模式**。当前框架基于固定离线数据集训练 VAE 和扩散模型，推理阶段使用之字形采样。尚未展示在线交互或持续学习场景下的表现。

### 已知局限与待验证假设

尽管实验证据有力，仍存在若干结构性局限或需要进一步验证的方面：

- **训练与推理开销**。潜在模块引入 VAE（GRU+MLP 编码器）、对比精炼损失以及自回归去噪与交替采样，训练和推理的消耗高于同规模的 Diffuser 约 1.5‑2 倍（论文未提供精确耗时对比）。在实时性要求高的部署场景中，推理延迟可能成为瓶颈。
- **逆动力学模型（IDM）对规划的依赖**。在状态‑免动作规划设定中需要额外学习 IDM 从状态和潜在变量恢复动作；若 IDM 精度不足，即使潜在识别准确也会导致动作偏差，这一点在 Kitchen‑Partial 的免动作规划结果中可以看到差异（Figure 4b，相关环境成功率下降）。
- **潜在维度和先验分布选择**。消融实验中潜在维度 0.5×–6× 变化对回报影响在 Cheetah‑Wind‑S 上达 ±15 左右（Table 2），说明性能对潜在空间容量敏感，目前缺乏自适应的维度选择机制。此外，潜在先验被假设为高斯分布，在具有多模态或离散潜在因子的环境中可能无法充分表征真实后验。
- **因果假设的鲁棒性**。定理 1 依赖于时变潜在因子通过 SCM 独立于历史噪声的条件可识别性假设；当实际环境中存在未观测的混淆因子或潜在因果图中包含反馈回路时，潜在识别可能失效。论文仅在模拟的 Cheetah 环境中验证了可分离性设定（Figure A1），其结论在更复杂的实际系统中的可迁移性有待检验。
- **未建模的安全和约束**。整个框架以最大化回报或任务成功率为目标，没有考虑约束违反或安全探索。在需要满足动态约束的环境（如自动驾驶、物理机器人）中应用前，需要增加约束模块。

### 开放问题与后续方向

结合 Appendix 中的讨论和当前方法边界，以下问题可构成后续研究的路径：

1. **真实世界与高维感知环境**。将 Ada‑Diffuser 部署到自动驾驶、无人机和物理机器人等真实系统是论文指出的未来方向（Appendix A.3）。这需要解决高维感知输入下的潜在识别稳定性，并保证在线适应对动力学漂移和传感器噪声的鲁棒性。
2. **延迟和累积潜在效应**。附录 Table A2 显示累积效应下的识别表现优于延迟效应，但两者仍逊于直接变化效应。如何设计潜在识别块以应对长程因果延迟或复合效应（例如多种潜在因素随时间叠加）仍是一个有待突破的问题。
3. **在线适应与持续学习**。当前框架是离线训练+在线潜在推理，但在线微调扩散模型或使潜在模块持续适应非平稳环境会带来灾难性遗忘和分布偏移的风险。开发能够安全在线更新模型的方法，是向终身学习式决策体迈进的关键。
4. **因果结构的发现与利用**。Ada‑Diffuser 假设潜在因子独立影响动态或奖励，但实践中可能存在多个潜在因子间的因果关系（如风→温度→摩擦力）。在推断潜在因子的同时识别因果图并据此设计更高效的干预式推理，可进一步拓宽方法的应用范围。
5. **跨任务泛化与操作对象变化**。在 Robomimic 和 LIBERO 实验中，潜在模块被用于操作任务内的上下文判断（如目标物体位置），但其在训练任务分布之外的新物体、新布局上的泛化能力仍不清晰。需要结合强泛化学习（如因果表示学习或元测试）来评估和提升。
6. **安全约束与风险感知**。引入潜在风险或不安全状态作为额外潜在因子，并在扩散生成中结合约束违反的预测，是实现安全强化学习决策的一条可行路径，但目前框架并未涉及。
7. **大规模模型与计算效率**。当前受限于 MLP/UNet/Transformer 下的小规模实验，扩展到高维轨迹和大批量数据时，因果去噪和之字形采样是否仍能维持增益，并能否与蒸馏技术结合以降低推理成本，是未来规模化的重要考量。



## 原文 PDF

PDF 文件：paperPDFs/ICLR_2026/Ada_Diffuser_Latent_Aware_Adaptive_Diffusion_for_Decision_Making.pdf

![[paperPDFs/ICLR_2026/Ada_Diffuser_Latent_Aware_Adaptive_Diffusion_for_Decision_Making.pdf]]
