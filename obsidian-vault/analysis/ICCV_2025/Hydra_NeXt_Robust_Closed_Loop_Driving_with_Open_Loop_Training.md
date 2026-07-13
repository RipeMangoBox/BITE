---
title: "Hydra-NeXt: Robust Closed-Loop Driving with Open-Loop Training"
type: paper
paper_level: A
venue: ICCV
year: 2025
pdf_ref: paperPDFs/ICCV_2025/Hydra_NeXt_Robust_Closed_Loop_Driving_with_Open_Loop_Training.pdf
project_link: null
code_link: https://github.com/woxihuanjiangguo/Hydra-NeXt
aliases:
- HN
- Hydra-NeXt
tags:
- ICCV_2025
- topic/reinforcement_learning_planning_agents
- topic/reinforcement_learning_planning_agents/deep_rl
core_operator: "引入直接控制解码器进行高频响应，并利用运动学自行车模型和扩散策略细化轨迹以符合闭环约束。"
primary_logic: "通过在开环训练中联合优化轨迹、控制和运动学可行的轨迹细化，可显著提升闭环驾驶性能而不依赖强化学习专家。"
claims:
- "在CARLA v2协议下，Hydra-NeXt较DriveAdapter提升22.98 DS和17.49 SR，证实多分支规划与轨迹细化的有效性。"
- "消融实验显示，移除控制解码器或扩散策略会导致DS下降超过5点，且最近邻匹配对最终性能至关重要。"
- "扩散策略生成的控制提案结合运动学模型可显著改善平滑度和碰撞避免，单独轨迹解码器在交互场景中表现不足。"
- "Hydra-NeXt在NAVSIM上达到88.6 PDMS，超越前SOTA DiffusionDrive，表明其泛化至真实世界开环规划。"
---

# Hydra-NeXt: Robust Closed-Loop Driving with Open-Loop Training

> [!tip] 核心洞察
> 通过在开环训练中联合优化轨迹、控制和运动学可行的轨迹细化，可显著提升闭环驾驶性能而不依赖强化学习专家。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | Hydra-NeXt: 利用开环训练实现鲁棒闭环驾驶 |
| 英文题名 | Hydra-NeXt: Robust Closed-Loop Driving with Open-Loop Training |
| 会议/期刊 | ICCV 2025 |
| Links | [paper](https://arxiv.org/abs/2503.12030) · [GitHub](https://github.com/woxihuanjiangguo/Hydra-NeXt) |
| Topic | #topic/reinforcement_learning_planning_agents #topic/reinforcement_learning_planning_agents/deep_rl |
| Method | Hydra-NeXt |
| Dataset | Bench2Drive (CARLA v2), Bench2Drive (Bench2Drive protocol) |

> [!tip] 效果简介
> - Bench2Drive (CARLA v2) 上，Driving Score (DS) 为 65.89，对比 42.91，变化 +22.98。
> - Bench2Drive (CARLA v2) 上，Success Rate (SR) 为 48.20%，对比 30.71%，变化 +17.49%。
> - Bench2Drive (Bench2Drive protocol) 上，Driving Score 为 73.86，对比 64.22，变化 +9.64。

## 概要

### 1. 问题瓶颈

端到端自动驾驶模型普遍采用开环轨迹预测范式进行训练。此类方法仅学习模仿专家路径的路点坐标，却忽略了两个闭环部署中的关键约束：**动态交互响应**与**运动学可行性**。开环训练下的模型对反应式智能体（如突然切入的车辆）响应迟缓，且其输出的轨迹在考虑车辆转向角、轴距等物理限制时往往不可执行。这导致模型在开环评测中表现尚可，但一旦部署到闭环仿真环境，驾驶得分（Driving Score, DS）和成功率（Success Rate, SR）便大幅下降。强化学习专家虽能通过环境交互习得响应能力与运动学约束，但其训练成本高昂且难以泛化。

### 2. 核心方法

Hydra-NeXt 提出了一种**多分支规划框架**，在开环训练范式内联合优化三个互补的策略模块，以弥合开环训练与闭环部署之间的鸿沟：

- **轨迹解码器（π_traj）**：继承自 Hydra-MDP，基于离散轨迹词汇表生成 3 秒全局路由轨迹，并蒸馏碰撞、软车道保持、自我进度等规则指标，提供高层规划意图。
- **控制解码器（π_ctrl）**：新增的分类式解码器，直接输出离散的油门、转向、制动信号，专注于短时域动作以实现对动态场景的快速响应。
- **轨迹细化网络（π_dp）**：引入扩散策略（Diffusion Policy）生成平滑的控制提案序列，通过运动学自行车模型将其转换为物理可行的轨迹，再经最近邻匹配与轨迹解码器输出对齐，最终集成出满足运动学约束的控制信号。

三个模块共享同一感知骨干提取的环境 token，端到端联合训练，总损失为轨迹模仿与蒸馏损失、控制分类损失及扩散去噪损失的加权和。

### 3. 核心结论

- 在 **Bench2Drive** 闭环基准（CARLA v2 协议）上，Hydra-NeXt 取得 **65.89 DS** 和 **48.20% SR**，较前 SOTA 方法 DriveAdapter 分别提升 **+22.98 DS** 和 **+17.49 SR**（Table 1）。在 Bench2Drive 自有协议下，DS 与 SR 亦分别达到 73.86 和 50.00%（Table 2）。
- 消融实验证实，**控制解码器与扩散策略缺一不可**：仅使用轨迹解码器的基线 Hydra-MDP 上，增加二者并通过最近邻匹配融合后，DS 提升 13.09，SR 提升 17.47（Table 10）；移除扩散策略导致 DS 下降 5.78（Table 5）。
- 在真实世界开环规划基准 **NAVSIM** 上，Hydra-NeXt 以 **88.6 PDMS** 超越前 SOTA DiffusionDrive（88.1 PDMS），验证了其泛化能力（Table 4 / Table 9）。
- 扩散策略的推理延迟可通过替换 DDPM 为 DDIM 调度器并引入 Flash-attention 降低约 53%，在几乎不损失性能的情况下将延迟从 528 ms 压缩至 243 ms（Table 11）。

### 4. 方法定位

Hydra-NeXt 属于**端到端开环训练、闭环部署**范式，其核心创新在于将控制预测与运动学可行的轨迹细化显式纳入开环训练框架，从而在不依赖强化学习专家或特权信息的前提下，显著提升闭环驾驶的鲁棒性。相较于依赖专家特征蒸馏的 DriveAdapter 和纯轨迹预测的 VAD、UniAD 等基线，Hydra-NeXt 通过多分支联合优化实现了对动态交互和物理约束的显式建模，同时保持了开环训练的数据效率优势。



### 端到端自动驾驶的闭环困境

端到端（End-to-End, E2E）自动驾驶方法近年来取得了显著进展，但其训练范式与部署环境之间存在根本性鸿沟。当前主流方法采用**开环训练**策略：模型从离线驾驶数据中学习预测轨迹路点，随后通过PID控制器将其转换为车辆控制信号。这种范式虽然在感知-规划一体化建模上展现出优势，却忽视了闭环驾驶中两个关键因素——**动态交互**与**运动学约束**。

具体而言，开环训练的轨迹预测器在面对反应式智能体（reactive agents）时响应迟缓。由于训练数据中的自车行为是固定的，模型从未学习到自身决策如何影响其他交通参与者的未来状态。当部署到闭环仿真器时，这种“自车-环境交互”的缺失导致规划路径在动态场景中频繁失效。与此同时，由轨迹路点经PID控制器间接生成的控制信号往往违反车辆的运动学极限，产生不可行的转向角度或加速度指令，进一步加剧了碰撞和偏离路线的风险。

Figure 1 清晰地刻画了三种自动驾驶范式的差异：基于强化学习（RL）的闭环专家通过与环境的持续交互学习控制信号，天然具备对智能体的响应能力和运动学可行性；而端到端方法依赖开环轨迹预测，忽略了自车-智能体交互与运动学约束。本文所提出的方法正是要填补这一缺口。

### 现有方法的局限

以 **Hydra-MDP** 为代表的开环轨迹规划基线通过蒸馏碰撞、车道保持等规则指标提升了开环性能，但其闭环表现仍然受限。**DriveAdapter** 作为此前 Bench2Drive 基准上的闭环 SOTA，依赖专家特征蒸馏来弥补开环训练的不足，然而这种外部知识的引入增加了框架的复杂性和对特定专家的耦合度。**VAD**、**UniAD** 等 E2E 规划基线同样受困于轨迹-控制转换链中的信息损失和运动学不可行问题。

Figure 2 展示了从 Hydra-MDP 到 Hydra-NeXt 的演进路线：Hydra-MDP 通过模仿学习达到 49.0 DS，已超越 DriveAdapter 的 42.9 DS，但距离真正的闭环可靠性仍有巨大空间。这一差距的根源在于：**单一的轨迹预测输出无法同时满足高频响应、交互感知和运动学可行性这三个闭环驾驶的核心需求**。

### 核心动机与研究问题

上述分析揭示了一个关键瓶颈：**开环训练忽略动态交互与运动学约束，导致闭环部署时对反应式智能体响应慢、路径不可行**。本文的核心动机在于探索一个根本性问题——能否在不依赖 RL 专家在线交互的前提下，通过在开环训练中引入适当的归纳偏置，使模型学会闭环驾驶所需的行为模式？

这一问题的回答需要解决三个相互关联的子问题：
1. 如何让模型具备对动态场景的快速响应能力？
2. 如何确保规划输出符合车辆的运动学约束？
3. 如何将轨迹层面的全局规划与控制层面的局部响应有效融合？

Hydra-NeXt 的设计正是围绕这些问题展开，其核心洞察是：**通过在开环训练中联合优化轨迹、控制和运动学可行的轨迹细化，可显著提升闭环驾驶性能而不依赖强化学习专家**。



## 核心方法与创新机理

Hydra-NeXt 的核心创新在于通过**多分支规划架构**与**运动学约束下的轨迹细化**，弥合开环训练与闭环部署之间的鸿沟。其关键设计围绕三个 changed slots 展开：

### 1. 双头运动解码器：轨迹预测 + 控制预测

传统开环方法（如 Hydra-MDP）仅预测轨迹路点，依赖下游 PID 控制器生成控制信号，对动态交互场景响应迟缓。Hydra-NeXt 在轨迹解码器 $\pi_{traj}$ 基础上，新增一个基于分类的**控制解码器** $\pi_{ctrl}$，直接输出离散控制信号 $(brake, throttle, steer)$。

- **因果机制**：控制解码器采用离散化策略处理不确定性（借鉴 RL 专家 Think2Drive 的做法），以更高频率（默认 2Hz）聚焦短期动作，实现对反应式智能体的快速响应。
- **证据强度**：消融实验（Table 10）表明，在 Hydra-MDP 基线上增加控制解码器并通过最近邻匹配集成，使 Driving Score 提升 13.09，Success Rate 提升 17.47。

### 2. 运动学自行车模型 + 扩散策略的轨迹细化

仅靠轨迹与控制解码器仍不足以保证闭环可行性——轨迹可能违反运动学约束，控制信号可能不够平滑。Hydra-NeXt 引入 **Trajectory Refinement 模块** $\pi_{dp}$，核心包含：

- **扩散策略（Diffusion Policy）**：作为控制提案生成器，从噪声中迭代去噪生成平滑、多样化的控制序列。实验证实其优于离散控制解码器的直接输出——移除扩散策略导致 DS 下降 5.78（Table 5）。
- **运动学自行车模型**：将高频控制提案（默认 10Hz）转换为运动学可行的轨迹，确保路径可被车辆执行。
- **最近邻匹配（Algorithm 1）**：计算扩散生成轨迹与轨迹解码器预测轨迹的 $L_2$ 距离，选择最近的两个控制提案进行集成。消融实验（Table 5）表明，仅做简单平均集成仅提升约 3 DS，而加入最近邻匹配以遵循运动学约束后，最终性能跃升至 65.89 DS。

### 3. 基于最近邻匹配的决策融合

最终控制信号 $C^*$ 的生成采用分层融合策略：

- **油门与转向**：对选中的两个候选控制提案取加权平均。
- **制动**：若候选制动值之和超过阈值 $\tau$（设为候选集大小的一半），则制动设为 1，否则为 0。

这种融合机制将轨迹解码器的全局路由能力与控制解码器及扩散策略的局部响应能力有机结合，使 Hydra-NeXt 在 CARLA v2 协议下达到 65.89 DS 和 48.20% SR，较前 SOTA DriveAdapter 分别提升 22.98 和 17.49（Table 1）。

**需注意的局限**：扩散策略的迭代去噪带来推理延迟（DDPM 下 528ms），虽然通过 DDIM + Flash-attention 优化可降至 243ms（Table 11），但仍可能影响实时闭环运行。此外，该方法对交通标志响应等细粒度规则遵守表现不理想，存在过拟合开环数据分布的风险。



![[assets/figures/papers/paper_list_l12_https_arxiv_org_abs_2503_12030/figures/002_Figure_2.jpg]]
*Figure 2: Roadmap from Hydra-MDP to Hydra-NeXt . DriveAdapter [26] was the previous state-of-the-art method on the Bench2Drive benchmark*

Hydra-NeXt 的整体架构围绕“开环训练 + 闭环部署”的核心矛盾设计，由三个功能互补的模块构成：**感知网络**、**多头运动解码器**（轨迹解码器与控制解码器）以及**轨迹细化模块**。其设计逻辑是：在开环阶段联合优化轨迹预测、控制预测与运动学可行的轨迹细化，从而在闭环测试中无需依赖强化学习专家即可获得强鲁棒性。

### 感知网络

感知网络负责将原始传感器观测转化为统一的环境表征。具体而言，系统接收前视与后视多视图图像，通过图像骨干网络提取多视图特征，随后将其展平为一串环境 token 序列 $F_{env}$。该序列作为下游所有解码器的共享输入，承载了场景的语义与几何信息。在 NAVSIM 等开环基准评估中，Hydra-NeXt 统一采用 **Transfuser**（ResNet34 骨干）作为感知网络，以确保与 Hydra-MDP、DiffusionDrive 等基线的公平对比。

### 多头运动解码器

多头运动解码器包含两个并行的预测头，分别从环境 token 中解码出不同时间尺度与表示形式的运动意图：

- **轨迹解码器 $\pi_{traj}$**：延续 Hydra-MDP 的设计，基于一个包含 4096 条候选轨迹的离散词汇表 $V$，生成一条 3 秒、频率为 2 Hz 的轨迹 $T$。该解码器通过模仿损失（以高斯核计算轨迹锚与专家轨迹的相似度作为软标签）和知识蒸馏损失（使轨迹锚的碰撞、软车道保持、自我进程等指标分数逼近特权信息真值）进行监督，总损失为 $\mathcal{L}_{traj} = \mathcal{L}_{im} + \mathcal{L}_{kd}$。轨迹解码器提供全局路由与长时运动规划能力。

- **控制解码器 $\pi_{ctrl}$**：新增的离散控制预测头，直接输出离散化的制动、油门、转向信号 $(C^1, ..., C^{t_{ctrl}})$，默认频率为 2 Hz。该设计借鉴了 RL 驾驶策略 **Think2Drive** 的离散化思路，以显式处理控制不确定性，并使模型能够对反应式智能体做出快速响应。控制解码器的训练损失由三部分组成：制动使用 Focal Loss，油门和转向使用交叉熵，跨多个控制时间步求和，即 $\mathcal{L}_{ctrl} = \mathcal{L}_{brake} + \mathcal{L}_{throttle} + \mathcal{L}_{steer}$。

轨迹解码器与控制解码器的输出在表示形式和时间尺度上互补：前者提供空间上的全局路径，后者提供时间上的高频响应能力。

### 轨迹细化模块

轨迹细化模块 $\pi_{dp}$ 是连接开环训练与闭环部署的关键桥梁，其核心任务是生成运动学可行的控制序列，并与上游解码器输出进行决策融合。该模块的工作流程如下：

1. **扩散策略生成控制提案**：采用扩散策略（Diffusion Policy）从噪声中迭代去噪，生成 $N$ 条平滑、多样化的控制序列（默认频率 10 Hz，$N=5$）。扩散策略的损失函数为均方误差 $\mathcal{L}_{dp} = \text{MSE}(\varepsilon^j, \pi_{dp}((\hat{C}^1, ..., \hat{C}^{\hat{t}_{dp}}) + \varepsilon^j, j))$，使其学习从加噪专家控制序列中预测噪声。

2. **运动学自行车模型展开轨迹**：将扩散策略生成的每条控制提案通过运动学自行车模型展开为细粒度轨迹 $T_{dp}^i$，从而显式施加运动学约束，确保轨迹的物理可行性。

3. **最近邻匹配与集成**：利用最近邻匹配算法（Algorithm 1），分别从控制提案展开轨迹集合中选出与轨迹解码器输出 $T$ 和控制解码器输出轨迹 $T_{ctrl}$ 最接近的两条提案（基于 $\mathbb{L}_2$ 距离）。随后，对入选提案的油门和转向值取加权平均得到最终控制信号；制动信号则采用阈值融合策略：若入选提案的制动值之和超过阈值 $\tau$（设为候选集大小的一半），则最终制动为 1，否则为 0。

### 端到端训练

整个 Hydra-NeXt 框架以端到端方式联合优化，总损失为三个模块损失之和：

$$\mathcal{L} = \mathcal{L}_{traj} + \mathcal{L}_{ctrl} + \mathcal{L}_{dp}$$

这种联合优化使得轨迹、控制与运动学细化三个分支在训练中相互协同，而非独立工作。消融实验证实，仅使用轨迹解码器的 Hydra-MDP 基线上，增加控制解码器和扩散策略并通过最近邻匹配集成后，Driving Score 提升 13.09，Success Rate 提升 17.47；若移除扩散策略而仅保留离散控制解码器，DS 下降 5.78，验证了各模块的互补性。

### 架构全景

Figure 3 展示了 Hydra-NeXt 的完整数据流：感知网络 → 多头运动解码器（轨迹解码器 + 控制解码器）→ 轨迹细化模块（扩散策略 + 运动学模型 + 最近邻匹配）→ 最终控制信号 $C^*$。Figure 2 则从 Hydra-MDP 出发，逐步叠加控制解码器和轨迹细化模块，展示了各组件带来的累积性能增益，最终超越前闭环 SOTA **DriveAdapter**。



Hydra-NeXt 的核心由三个可端到端联合优化的模块构成：**轨迹解码器（Trajectory Decoder）**、**控制解码器（Control Decoder）** 与**轨迹细化网络（Trajectory Refinement Network）**。三者共享同一感知网络提取的环境 token 序列 $F_{env}$，但分别解决规划中的不同瓶颈——路由规划、高频响应与运动学可行性。

### 轨迹解码器：Hydra-MDP 的继承

轨迹解码器 $\pi_{traj}$ 延续了 Hydra-MDP 的设计：基于离散轨迹词汇表 $V$（含 4096 条候选轨迹），以 2Hz 频率预测一条 3 秒的轨迹 $T$。其训练目标由两部分组成。

**模仿损失 $\mathcal{L}_{im}$** 以高斯核计算轨迹锚点与专家轨迹的相似度作为软标签，监督轨迹锚的模仿分数：

$$y_i = \frac{e^{-(\hat{T} - T_i)^2}}{\sum_{j=1}^k e^{-(\hat{T} - T_j)^2}}, \quad \mathcal{L}_{im} = -\sum_{i=1}^k y_i \log(S_i^{im})$$

其中 $\hat{T}$ 为专家轨迹，$T_i$ 为词汇表中第 $i$ 条轨迹锚点，$S_i^{im}$ 为模型预测的模仿分数。

**知识蒸馏损失 $\mathcal{L}_{kd}$** 使轨迹锚的预测指标分数逼近由特权信息计算的真值 $\hat{S}_i^m$：

$$\mathcal{L}_{kd} = -\sum_{m,i} \hat{S}_i^m \log S_i^m + (1 - \hat{S}_i^m) \log(1 - S_i^m), \quad m \in \{COL, SLK, EP\}$$

其中 $m$ 分别对应碰撞（COL）、软车道保持（SLK）与自我进程（EP）三类规则指标。

轨迹解码器总损失为二者之和：

$$\mathcal{L}_{traj} = \mathcal{L}_{im} + \mathcal{L}_{kd}$$

### 控制解码器：高频响应与离散化

控制解码器 $\pi_{ctrl}$ 是 Hydra-NeXt 对 Hydra-MDP 的关键扩展。它采用分类头直接预测离散控制信号 $(brake, throttle, steer)$，跨 $t_{ctrl}$ 个时间步输出。离散化设计借鉴了 RL 专家 Think2Drive 的实践，以处理控制空间的不确定性。其损失函数按控制维度分别设计：

$$\mathcal{L}_{brake} = \sum_{t=1}^{t_{ctrl}} Focal(b^t, \hat{b}^t), \quad \mathcal{L}_{throttle} = \sum_{t=1}^{t_{ctrl}} CE(th^t, \hat{th}^t), \quad \mathcal{L}_{steer} = \sum_{t=1}^{t_{ctrl}} CE(s^t, \hat{s}^t)$$

$$\mathcal{L}_{ctrl} = \mathcal{L}_{brake} + \mathcal{L}_{throttle} + \mathcal{L}_{steer}$$

其中制动使用 Focal Loss 以缓解类别不平衡，油门和转向使用标准交叉熵。控制解码器的存在使得模型能对反应式智能体做出更快响应，弥补纯轨迹规划在动态交互场景中的不足。

### 轨迹细化网络：扩散策略与运动学约束

轨迹细化网络 $\pi_{dp}$ 是解决开环训练与闭环部署之间运动学可行性鸿沟的核心模块。其工作机制分为三步：

1. **扩散生成**：以扩散模型从随机噪声中迭代去噪，生成平滑的控制序列提案。扩散策略损失为均方误差，使模型从加噪专家控制序列中预测噪声：

$$\mathcal{L}_{dp} = MSE(\varepsilon^j, \pi_{dp}((\hat{C}^1, ..., \hat{C}^{\hat{t}_{dp}}) + \varepsilon^j, j))$$

其中 $\hat{C}$ 为专家控制序列，$\varepsilon^j$ 为第 $j$ 步注入的噪声。

2. **运动学展开**：将扩散生成的控制提案通过运动学自行车模型展开为细粒度轨迹 $T_{dp}$，确保路径物理可行。

3. **最近邻匹配与融合**：以 L2 距离分别从扩散提案和轨迹解码器输出中选出与预测轨迹 $T$ 最近的两个控制候选，通过加权平均油门与转向、基于阈值 $\tau$ 融合制动（$\tau$ 默认设为候选集大小的一半，即 1），得到最终控制信号 $C^*$。

### 端到端联合优化

三个模块在开环数据上端到端联合训练，总损失为：

$$\mathcal{L} = \mathcal{L}_{traj} + \mathcal{L}_{ctrl} + \mathcal{L}_{dp}$$

这一联合优化使得轨迹规划、高频控制响应与运动学可行细化三者协同进化，无需依赖强化学习专家的在线交互即可显著提升闭环驾驶性能。



## 实验与关键发现

### 核心定量结果

Hydra-NeXt在CARLA v2闭环协议下取得**65.89 Driving Score（DS）**与**48.20% Success Rate（SR）**，相较此前闭环SOTA方法**DriveAdapter**分别提升+22.98 DS和+17.49 SR（Table 1）。在Bench2Drive自有协议下，Hydra-NeXt达到73.86 DS和50.00% SR，领先DriveAdapter +9.64 DS和+16.92 SR（Table 2）。值得注意的是，Hydra-NeXt的开环L2误差仅为0.92米，表明其轨迹预测精度本身具有竞争力，但闭环性能的大幅跃升主要源于控制解码器与轨迹细化模块的引入。

![[assets/figures/papers/paper_list_l12_https_arxiv_org_abs_2503_12030/figures/005_Table_1.jpg]]
*Table 1: Open-loop and Closed-loop Performance of E2E-AD Methods on the Bench2Drive Benchmark with the CARLA v2 Evaluation Protocol. The CARLA v2 protocol calculates the Driving Score (DS) by aggregating all infractions multiplicatively, including minimum speed infractions. * The model benefits from expert feature distillation. Table 2. Closed-loop Performance of E2E-AD Methods on the Bench2Drive Benchmark with the Bench2Drive Evaluation Protocol. * The model benefits from expert feature distillation*

在真实世界开环基准NAVSIM上，Hydra-NeXt以**88.6 PDMS**超越前SOTA **DiffusionDrive**（88.1 PDMS），验证了该方法在非仿真场景下的泛化能力（Table 4 / Table 9）。所有NAVSIM评估均统一采用**Transfuser**（ResNet34）作为感知骨干，确保与Hydra-MDP、DiffusionDrive等基线的公平比较。

![[assets/figures/papers/paper_list_l12_https_arxiv_org_abs_2503_12030/figures/006_Table_3.jpg]]
*Table 3: Multi-Ability Results of E2E-AD Methods on the Bench2Drive Benchmark. * denotes expert feature distillation. Table 4. Performance of E2E-AD Methods on NAVSIM*

![[assets/figures/papers/paper_list_l12_https_arxiv_org_abs_2503_12030/figures/012_Table_9.jpg]]
*Table 9: Performance of E2E-AD Methods on NAVSIM. All methods above use Transfuser [9] with ResNet34 [18] as the perception backbone. *DRAMA [54] uses Mamba [10] for multi-modal interaction. Hydra-MDP [33] uses grid search to obtain the optimal hyperparameters for weighting different predicted metric scores*

### 多能力细分分析

Table 3展示了各方法在Bench2Drive子场景上的广义性能。Hydra-NeXt在多数能力维度上优于DriveAdapter，平均能力提升11.14%。然而，在**交通标志遵守**和**特勤车辆避让**两项上，Hydra-NeXt表现不理想，甚至落后于部分基线。这提示当前框架对细粒度交通规则的建模仍存在短板，可能源于开环训练数据中此类场景的分布不足或规则指标蒸馏的不充分。

### 消融实验：各模块贡献

Table 10揭示了从Hydra-MDP基线到完整Hydra-NeXt的增量收益。仅使用轨迹解码器（π_traj）的Hydra-MDP基线上，增加控制解码器（π_ctrl）和扩散策略（π_dp）并通过最近邻匹配集成，使DS提升13.09，SR提升17.47。这证实了多分支规划与轨迹细化的联合有效性。

![[assets/figures/papers/paper_list_l12_https_arxiv_org_abs_2503_12030/figures/011_Table_10.jpg]]
*Table 10: Performance of Individual Policies on Bench2Drive*

Table 5进一步拆解轨迹细化中的策略选择。移除扩散策略而仅依赖离散控制解码器，导致DS从65.89降至60.15（下降5.78），说明扩散策略生成的平滑控制序列对碰撞避免和路径可行性至关重要。单独使用轨迹解码器在复杂交互场景中表现不足，这促使了控制解码器的引入——后者专门针对反应式智能体提供高频响应。

![[assets/figures/papers/paper_list_l12_https_arxiv_org_abs_2503_12030/figures/007_Table_5.jpg]]
*Table 5: Ablation of the Policy in Trajectory Refinement. Table 6. Ablation of the Prediction Frequency of the Control Decoder and the Diffusion Policy*

### 频率与提案数量消融

Table 6显示，将扩散策略频率从2Hz提升至10Hz带来DS约+3.94和SR约+9.15的显著增益，验证了高频控制在闭环环境中的必要性。Table 7表明，增加扩散提案数量N（5→20）对DS提升有限（约0.5），SR甚至略有波动下降，说明最近邻匹配机制在少量提案下已能有效选择高质量候选。

![[assets/figures/papers/paper_list_l12_https_arxiv_org_abs_2503_12030/figures/008_Table_7.jpg]]
*Table 7: Ablation of the Proposal Number N in Trajectory Refinement*

### 推理效率与加速策略

Table 8对比了各方法的推理延迟。Hydra-NeXt在RTX 3090上的延迟为528ms（DDPM），高于VAD但低于UniAD和DriveAdapter（后两者在A100/A6000上测试，需注意硬件差异）。Table 11显示，将DDPM替换为DDIM并配合Flash-attention，延迟可降低53%至243ms，且性能几乎无损。这为实时部署提供了可行路径，但243ms的延迟在高速场景下仍可能构成瓶颈。

![[assets/figures/papers/paper_list_l12_https_arxiv_org_abs_2503_12030/figures/010_Table_8.jpg]]
*Table 8: Analysis of Runtime Efficiency. The latency of Hydra-NeXt and VAD are benchmarked on an NVIDIA RTX 3090, while UniAD and DriveAdapter are on NVIDIA Tesla A100 and A6000, respectively. F refers to Flash-attention [11] for acceleration*

![[assets/figures/papers/paper_list_l12_https_arxiv_org_abs_2503_12030/figures/013_Table_11.jpg]]
*Table 11: Efficiency of Different Diffusion Schedulers. * denotes Flash-attention [11]*

### 失败模式与局限性

1. **交互响应滞后**：尽管控制解码器提升了反应速度，但与使用特权输入的RL专家（如Think2Drive）相比，Hydra-NeXt在密集交互场景中仍有明显差距。扩散策略的迭代去噪过程（即使优化后243ms）可能加剧这一问题。
2. **规则遵守不足**：交通标志响应和特勤车辆避让表现不佳，暗示开环训练的规则指标蒸馏可能过拟合训练分布，缺乏对罕见但关键场景的泛化。
3. **专家数据依赖**：Table 12显示，使用不同专家数据（Think2Drive vs PDM-Lite）训练的模型性能存在差异，表明框架对专家数据分布敏感，更换数据源需重新调整组件。

![[assets/figures/papers/paper_list_l12_https_arxiv_org_abs_2503_12030/figures/014_Table_12.jpg]]
*Table 12: Performance of Models Trained with Different Experts. †Ensemble of three models trained with different seeds*

### 补充图表

![[assets/figures/papers/paper_list_l12_https_arxiv_org_abs_2503_12030/figures/004_Table.jpg]]



## 定位与知识库关联

### 1. 方法继承与突破

Hydra-NeXt 构建在 Hydra-MDP 的开环轨迹规划框架之上，后者通过离散轨迹词汇表与规则指标蒸馏实现了高效的开环模仿学习。然而，Hydra-MDP 仅预测轨迹路点，在闭环部署中面临双重瓶颈：其一，轨迹解码器对反应式智能体的响应速度不足；其二，生成的轨迹缺乏运动学可行性约束，导致路径不可执行。Hydra-NeXt 的核心突破在于将开环训练范式扩展为多分支规划架构，在不依赖强化学习专家在线交互的前提下，系统性地弥合了开环训练与闭环部署之间的鸿沟。

具体而言，该方法保留了 Hydra-MDP 的感知网络与轨迹解码器（$\pi_{traj}$）作为路由规划分支，同时引入两个关键组件：（1）**控制解码器**（$\pi_{ctrl}$），直接预测离散控制信号（制动、油门、转向），实现对动态场景的高频响应；（2）**轨迹细化网络**（$\pi_{dp}$），利用扩散策略生成平滑控制序列，经运动学自行车模型转换为运动学可行的轨迹提案，并通过最近邻匹配与轨迹分支集成。这种“轨迹规划 + 控制响应 + 运动学细化”的三支路架构，使得开环训练的模型首次在闭环基准上大幅超越依赖专家特征蒸馏的前 SOTA 方法。

### 2. 与基线方法的关系定位

**DriveAdapter** 是 Hydra-NeXt 最直接的对比基线，也是此前 Bench2Drive 闭环基准的 SOTA。DriveAdapter 通过特征蒸馏从特权专家中迁移驾驶知识，其性能高度依赖专家特征的质量与泛化性。Hydra-NeXt 在完全不使用专家特征蒸馏的前提下，在 CARLA v2 协议下以 65.89 DS 超越 DriveAdapter 的 42.91 DS（+22.98），在 Bench2Drive 协议下以 73.86 DS 超越其 64.22 DS（+9.64）。这一结果表明，多分支规划与运动学约束的显式建模比单纯的特征蒸馏更有效地解决了闭环驾驶的因果瓶颈。

**VAD** 与 **UniAD** 作为端到端规划的代表性基线，在闭环测试中表现显著弱于 Hydra-NeXt（VAD 的 DS 仅为 3.82，UniAD 为 19.82，见表 1）。这进一步验证了 Hydra-NeXt 的设计理念：开环轨迹预测若不辅以控制响应与运动学细化，在闭环交互场景中将严重失效。

**Transfuser** 在 NAVSIM 评估中作为统一的感知骨干，确保了 Hydra-NeXt 与 Hydra-MDP、DiffusionDrive 等方法的公平比较。Hydra-NeXt 在 NAVSIM 上达到 88.6 PDMS，超越前 SOTA DiffusionDrive 的 88.1，表明其多分支架构同样适用于真实世界的开环规划任务。

### 3. 适用边界与约束条件

Hydra-NeXt 的有效性建立在一系列前提假设之上：

- **专家数据依赖性**：轨迹解码器的模仿学习与控制解码器的监督训练均依赖固定的专家数据分布（默认使用 Think2Drive 作为专家）。当更换专家数据源（如 PDM-Lite）时，框架组件需要重新调整，且性能可能波动（见表 12）。这意味着该方法尚未实现对专家分布的无偏泛化。

- **仿真环境的运动学一致性**：轨迹细化模块依赖运动学自行车模型的精确参数化。在 CARLA 仿真中，车辆动力学模型是已知且确定的；若迁移至真实车辆或不同仿真器（如 CARLA 3.0），运动学参数的失配可能导致轨迹提案的可行性下降。

- **感知骨干的可替换性**：Hydra-NeXt 的感知网络设计为模块化，在 NAVSIM 上可替换为 Transfuser（ResNet34）。但在闭环测试中，感知误差对规划分支的级联影响尚未被系统消融，这构成了部署鲁棒性的潜在风险。

### 4. 已知局限与失效模式

尽管 Hydra-NeXt 在整体指标上表现卓越，但细粒度分析揭示了若干失效模式：

- **交通规则遵守不足**：在多能力评估（表 3）中，Hydra-NeXt 在交通标志响应（Traffic Sign）子项上落后于 DriveAdapter，表明开环训练的数据分布可能未充分覆盖标志识别与响应的长尾场景。类似地，所有方法在特勤车辆避让（Specialized Vehicles）子项上均表现不佳，这暗示当前开环数据与评估协议对该场景的建模存在系统性缺陷。

- **扩散策略的推理延迟**：DDPM 调度器下扩散策略的迭代去噪耗时 528ms，虽通过 DDIM + Flash-attention 优化至 243ms（表 11），仍可能影响高速动态场景的实时响应。这一延迟瓶颈源于扩散模型的生成机制，而非工程实现问题。

- **提案数量的边际收益递减**：消融实验（表 7）显示，将扩散提案数量从 5 增至 20 对 DS 的提升仅约 0.5，SR 甚至略有下降。这表明最近邻匹配策略在候选集增大时可能引入冗余或冲突提案，融合机制仍有优化空间。

- **与特权专家的性能差距**：即便在最优配置下，Hydra-NeXt 的闭环性能仍显著落后于使用特权输入的 RL 专家 Think2Drive（DS 约 82），在复杂多智能体交互场景中差距尤为明显。这提示开环模仿学习在探索能力与交互建模上存在根本性上限。

### 5. 开放问题与未来方向

Hydra-NeXt 的开环训练范式为闭环驾驶提供了新的基准，但也引出了若干待解问题：

1. **性能上限的突破**：如何进一步缩小与 RL 特权专家的差距？可能的路径包括引入对抗性数据增强、模型集成（表 12 中三模型集成可带来约 2 DS 提升）、或探索离线 RL 与模仿学习的混合训练策略。

2. **扩散策略的替代方案**：能否通过模型蒸馏、一致性模型或流匹配等更高效的生成范式替代 Diffusion Policy，在保持运动学平滑性的同时大幅降低推理延迟？

3. **域迁移鲁棒性**：开环训练的泛化策略在真实传感器噪声、天气变化与未知场景下的鲁棒性尚未被验证。NAVSIM 的开环评估虽提供了初步证据，但闭环真实世界测试仍是关键缺口。

4. **分支间信息交互**：当前控制解码器与轨迹解码器独立预测，仅在最终阶段通过最近邻匹配融合。是否存在更优的中间层特征共享或交叉注意力机制，使两分支协同更紧密？

5. **跨仿真器可迁移性**：该方法能否无缝迁移至 CARLA 3.0 或其他高保真仿真环境？运动学模型参数的自适应标定与感知网络的域适应是潜在的技术挑战。



## 原文 PDF

![[paperPDFs/ICCV_2025/Hydra_NeXt_Robust_Closed_Loop_Driving_with_Open_Loop_Training.pdf]]
