---
title: "One-Step Flow Q-Learning: Addressing the Diffusion Policy Bottleneck in Offline Reinforcement Learning"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/One_Step_Flow_Q_Learning_Addressing_the_Diffusion_Policy_Bottleneck_in_Offline_Reinforcement_Learning.pdf
project_link: null
code_link: null
openreview_forum_id: 60VgwdzxDM
aliases:
- OSFQLO
- OSFQLADPBORL
tags:
- ICLR_2026
- topic/reinforcement_learning_planning_agents
- topic/reinforcement_learning_planning_agents/deep_rl
core_operator: "将策略参数化从多步DDPM替换为学习平均速度场的单步流匹配模型(OFQL)，直接消除迭代去噪和BPTT，无需辅助模块或蒸馏。"
primary_logic: "通过流匹配框架学习平均速度场代替瞬时速度场，使得从噪声到动作的映射变为直线式单步生成，从而在保持多模态表达能力和行为正则化效果的同时，大幅提升训练和推理效率，并稳定Q值最大化过程。"
claims:
- "OFQL在流匹配范式下学习平均速度场，实现精确的单步动作生成，消除了多步去噪和BPTT。"
- "在D4RL基准上，OFQL在MuJoCo任务上的平均归一化得分从DQL的87.9显著提升至92.5，同时大幅降低训练和推理耗时。"
- "通过只训练单步策略，OFQL完全消除了对辅助模型和蒸馏的依赖，训练时间仅6.3小时，推理频率达846.5 Hz。"
- "平均速度匹配损失是行为分布与所学策略间2-Wasserstein距离的上界，保证行为正则化的同时不损失多模态建模能力。"
---

# One-Step Flow Q-Learning: Addressing the Diffusion Policy Bottleneck in Offline Reinforcement Learning

> [!tip] 核心洞察
> 通过流匹配框架学习平均速度场代替瞬时速度场，使得从噪声到动作的映射变为直线式单步生成，从而在保持多模态表达能力和行为正则化效果的同时，大幅提升训练和推理效率，并稳定Q值最大化过程。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 单步流Q学习：解决离线强化学习中扩散策略瓶颈问题 |
| 英文题名 | One-Step Flow Q-Learning: Addressing the Diffusion Policy Bottleneck in Offline Reinforcement Learning |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=60VgwdzxDM) |
| Topic | #topic/reinforcement_learning_planning_agents #topic/reinforcement_learning_planning_agents/deep_rl |
| Method | One-Step Flow Q-Learning (OFQL) |
| Dataset | D4RL MuJoCo (9 tasks), D4RL AntMaze (4 tasks), D4RL Kitchen (2 tasks), D4RL Adroit (pen-human, pen-cloned) |

> [!tip] 效果简介
> - D4RL MuJoCo (9 tasks) 上，Normalized Score (average) 为 92.5，对比 87.9 (DQL)，变化 +4.6。
> - D4RL AntMaze (4 tasks) 上，Normalized Score (average) 为 84.6，对比 64.6 (DQL)，变化 +20.0。
> - D4RL Kitchen (2 tasks) 上，Normalized Score (average) 为 67.0，对比 61.6 (DQL)，变化 +5.4。

## 概要

离线强化学习中，扩散策略（diffusion policy）通过多模态行为建模显著提升了策略表达能力，但其核心瓶颈在于**依赖多步去噪扩散模型（DDPM）生成动作**。这一设计导致两个连锁问题：推理时需迭代执行 $K$ 步反向链式采样（通常 $K=5\sim50$），决策频率受限；训练时需通过时间反向传播（BPTT）计算梯度，优化不稳定且收敛次优。

本文提出 **One-Step Flow Q-Learning（OFQL）**，将策略参数化从多步 DDPM 替换为**学习平均速度场的单步流匹配模型**。核心洞察在于：流匹配框架下，若直接学习瞬时速度场（marginal velocity），单步生成会产生严重的模式坍塌；而**学习平均速度场（average velocity field）**使得从噪声到动作的映射退化为直线式单步变换，在保持多模态表达能力和行为正则化效果的同时，彻底消除迭代去噪和 BPTT。

**核心结论：**
- 在 D4RL 基准上，OFQL 将 DQL 的 MuJoCo 平均归一化得分从 87.9 提升至 **92.5**（+4.6），AntMaze 从 64.6 提升至 **84.6**（+20.0），Kitchen 从 61.6 提升至 **67.0**（+5.4）。
- 训练耗时从 11.7 小时降至 **6.3 小时**，推理决策频率从 238.7 Hz 提升至 **846.5 Hz**，且无需任何辅助模型或蒸馏。
- 消融实验表明，单步 OFQL（92.6）超越 5 步 DQL（87.9），而其他单步策略（DQL+DDIM、FBRAC、FQL）均未能达到多步基线水平。

**方法定位：** OFQL 属于行为正则化 Actor-Critic 框架下的策略改进，以流匹配的平均速度参数化替代扩散模型的噪声预测参数化。与蒸馏方案（如 FQL）不同，OFQL 直接训练单步策略而非从多步教师蒸馏，避免了额外的训练开销和精度损失。



### 离线强化学习中的扩散策略范式

离线强化学习（Offline RL）的核心挑战是从静态数据集中学习策略，而不与环境进行在线交互。近年来，扩散模型在该领域展现出显著优势，其核心思想是将策略参数化为条件去噪扩散概率模型（DDPM），通过多步迭代去噪从高斯噪声中生成动作。这种参数化方式天然具备多模态表达能力，能够有效捕捉行为数据中复杂的动作分布。

基于扩散模型的策略学习通常采用行为正则化的演员-评论家框架：演员（策略）通过行为克隆损失保持与数据分布的接近，同时最大化Q值以提升策略质量；评论家则通过标准的时序差分学习估计动作价值。代表性工作 **DQL**（Wang et al., 2022）将DDPM作为策略网络，在D4RL基准上取得了具有竞争力的结果。

### 扩散策略的计算瓶颈

尽管扩散策略在性能上表现突出，其计算效率存在根本性瓶颈。这一瓶颈源于两个紧密耦合的因素：

**多步迭代去噪。** DDPM的动作生成需要执行完整的K步反向扩散链（通常K=5~50），每一步都需要调用策略网络进行去噪预测。这不仅导致推理决策频率低下，还使得训练过程中的动作采样极为耗时——每次演员更新都需要展开完整的去噪链。

**时间反向传播（BPTT）。** 更为关键的是，由于动作生成涉及多个去噪步骤，Q值最大化项对策略参数的梯度必须通过整个去噪链反向传播。这种时间反向传播不仅计算开销巨大，还引入了优化不稳定性：梯度在长链中累积误差，容易导致次优收敛或训练崩溃。DQL通过重参数化技巧将行为克隆损失简化为噪声预测损失，但Q值最大化项仍无法避免BPTT。

### 流匹配范式的单步生成潜力

流匹配（Flow Matching, FM）为上述瓶颈提供了新的解决思路。与扩散模型通过随机微分方程逐步去噪不同，流匹配学习一个确定性速度场，通过常微分方程（ODE）将噪声分布连续变换为目标数据分布。理论上，流匹配框架支持通过ODE积分器以任意步数生成样本，但标准做法仍然需要多步积分才能保证生成质量。

关键洞察在于：常规流匹配学习的是**瞬时速度场**（marginal velocity field），它描述概率流路径上每一点的瞬时变化率。由于流路径本身是弯曲的（curved），用瞬时速度进行单步外推会产生显著的离散化误差，导致生成质量下降甚至模式坍塌。因此，直接将标准流匹配策略压缩为单步生成，并不能解决扩散策略的效率问题。

### 本文动机与核心思路

本文的核心动机是**在保持扩散策略多模态表达能力和行为正则化效果的前提下，从根本上消除多步去噪和BPTT带来的效率与稳定性瓶颈**。为此，OFQL提出学习**平均速度场**（average velocity field）而非瞬时速度场。

平均速度场描述的是从噪声到目标动作的直线式整体位移，而非路径上每一点的瞬时变化。通过直接预测这一整体位移，策略可以在单次前向传播中完成从噪声到动作的映射——无需ODE积分，无需迭代去噪，也无需时间反向传播。这一设计使得OFQL在训练和推理中均只需一步操作，同时保留了流匹配框架对复杂多模态分布的建模能力。

简言之，OFQL将扩散策略的“多步弯曲去噪”替换为“单步直线流映射”，实现了效率与性能的统一。



## 核心方法与创新机理

### 问题瓶颈：扩散策略的三重代价

离线强化学习中的扩散Q学习（DQL，Wang et al., 2022）将策略参数化为一个多步去噪扩散概率模型（DDPM），通过K步反向链（K=5~50）从噪声中逐步生成动作。这一设计引入了三重代价：

1. **推理缓慢**：每次动作采样需执行K次网络前向传播，推理决策频率仅约238.7 Hz（5步DQL），限制了实时部署。
2. **训练低效**：Actor更新需通过K步去噪链进行时间反向传播（BPTT），梯度需沿去噪链递归展开，导致训练耗时达11.7小时（100万步）。
3. **优化不稳定**：长程BPTT引入梯度消失/爆炸风险，使得Q值最大化的梯度信号在反向传播中衰减或畸变，导致次优收敛。

### 因果旋钮：从多步DDPM到单步平均速度场

OFQL的核心操作是将策略参数化从**多步DDPM**替换为**学习平均速度场的单步流匹配模型**。这一替换直接消除了迭代去噪和BPTT，无需辅助模块或蒸馏。

具体而言，OFQL在以下四个关键槽位上改变了DQL的设计：

| 设计槽位 | DQL（基线） | OFQL（本文） |
|---------|------------|------------|
| **策略参数化** | DDPM（多步去噪扩散） | 流匹配 + 平均速度场（单步生成） |
| **动作采样** | K步反向链：$a^{k-1} \sim p_\theta(a^{k-1} \mid a^k, s)$ | 单步端点映射：$a = \epsilon - u_\theta(\epsilon, r=0, t=1; s)$ |
| **行为正则化损失** | $\mathcal{L}_{\text{DBC}}$（得分匹配） | $\mathcal{L}_{\text{FBC}}$（平均速度匹配，Eq. 14） |
| **Actor更新** | K步去噪链的BPTT | 单步反向传播，无时间展开 |

### 核心洞察：平均速度场实现直线式单步生成

流匹配（Flow Matching, FM）的标准范式学习的是**瞬时速度场** $v_\theta(a_t, t; s)$，它定义了概率流ODE中每个时刻的速度方向。然而，由于流路径本身是弯曲的（见图2c），从$t=0$到$t=1$的直接单步外推会产生显著误差，导致分布建模质量下降——这在玩具数据集实验中表现为瞬时速度参数化（v-param）在早期步数出现模式坍塌（Figure 4左）。

OFQL的关键洞察是：**学习平均速度场而非瞬时速度场**。平均速度定义为区间$[r, t]$上的总位移除以区间长度：

$$u(a_t, r, t; s) \triangleq \frac{1}{t - r} \int_{r}^{t} v(a_\tau, \tau; s) d\tau \quad \text{(Eq. 10)}$$

这一参数化的精妙之处在于，当$r=0, t=1$时，$u_\theta(\epsilon, 0, 1; s)$直接编码了从噪声$\epsilon$到目标动作的**直线位移向量**。因此，单步动作生成退化为简单的端点映射：

$$a = T_\theta(\epsilon, s) = \epsilon - u_\theta(\epsilon, r=0, t=1; s), \quad \epsilon \sim \mathcal{N}(0, I) \quad \text{(Eq. 12)}$$

这完全绕过了ODE积分，实现了从噪声到动作的直线式单步生成，同时保留了流匹配框架的多模态表达能力。玩具数据集实验证实，平均速度参数化（u-param）仅需单步生成即可达到DDPM 10步的采样质量（Figure 4右）。

### 训练效率的突破

平均速度匹配损失 $\mathcal{L}_{\text{FBC}}$（Eq. 14）通过MeanFlow恒等式（Eq. 13）避免了积分计算，将训练目标转化为可微分的回归问题。由于动作采样仅需单次前向传播，Actor更新中的Q值最大化梯度 $\nabla_\theta a$ 无需沿时间展开，直接通过单步反向传播计算。这带来了训练效率的质变：

- **训练耗时**：从DQL（5步）的11.7小时降至6.3小时（同一A100 GPU）
- **推理决策频率**：从238.7 Hz提升至846.5 Hz（约3.5倍加速）

### 行为正则化的理论保证

尽管动作生成被压缩为单步，OFQL的行为正则化并未退化。平均速度匹配损失被证明是行为分布与所学策略之间**2-Wasserstein距离的上界**，这意味着最小化 $\mathcal{L}_{\text{FBC}}$ 能够保证单步策略收敛至行为分布，同时通过非线性端点映射 $T_\theta$ 保留对复杂多模态动作分布的建模能力。在HalfCheetah任务上，OFQL的OOD-MSE低于DQL（Medium: 0.458 vs 0.462; Medium-Replay: 0.560 vs 0.582），验证了其更强的分布外泛化能力。

### 与其他单步策略的本质区别

Table 2的消融实验揭示了OFQL单步性能的关键来源。DQL+DDIM（1步）直接使用DDIM跳跃采样，得分从87.9骤降至11.6；FBRAC（1步）通过行为正则化约束单步策略，仅达67.1；FQL（1步）依赖多步流策略蒸馏，得分为79.2。这些方法均未触及核心矛盾——**单步外推在弯曲流/扩散路径上的固有误差**。OFQL通过平均速度参数化从根本上解决了这一问题，在单步条件下达到92.6（+4.7 over DQL），证明其性能增益并非来自辅助技巧，而是参数化范式的结构性优势。



![[assets/figures/papers/paper_list_l40_https_openreview_net_forum_id_60VgwdzxDM/figures/002_Figure_2.jpg]]
*Figure 2: Comparison between diffusion and flow matching. (a) Conditional flows arise from different (ϵ, x) pairs, resulting in varying conditional velocities. (b) Marginal velocity is obtained by averaging over these conditional velocities. (c) Flow paths are inherently curved, but average velocity fields enable direct one-step transport from noise to data. (d) Diffusion paths are also curved but noisy, making one-step denoising challenging. Note that all the velocities exhibit symmetry under time reversal. As the model is trained to parameterize the forward flow (from data to noise), inference inverts this direction to generate samples. Accordingly, for clarity, we plot the negative velocity vector...*

OFQL（One-Step Flow Q-Learning）的整体框架围绕一个核心设计展开：**将扩散策略从多步去噪范式替换为单步流匹配范式**，从而在保持行为正则化与多模态表达能力的同时，消除迭代采样和反向传播通过时间（BPTT）带来的效率瓶颈。

### 模块组成与数据流

整个pipeline由五个紧密耦合的模块构成，数据流遵循标准的actor-critic离线强化学习循环：

1. **策略网络（Policy Network $u_\theta$）**：接收状态 $s$、噪声样本 $\epsilon \sim \mathcal{N}(0, I)$ 以及时间参数 $r=0, t=1$，输出平均速度 $u_\theta(\epsilon, 0, 1; s)$。该网络是框架的核心创新——它学习的是**平均速度场**而非瞬时速度场，使得从噪声到动作的映射变为直线式单步生成。

2. **动作采样器（Action Sampler）**：执行单步前向传播，通过端点映射 $a = \epsilon - u_\theta(\epsilon, 0, 1; s)$ 直接生成动作。这一操作完全可微，无需ODE积分或多步链式展开，是训练和推理加速的根本原因。

3. **Q网络（Q-Networks $\phi_1, \phi_2$）**：采用双Q学习架构，每个Q网络为3层MLP（Mish激活函数）。Critic损失为标准Clipped Double Q-learning：
   $$\mathcal{L}(\phi) = \mathbb{E}_{(s,a,r,s') \sim \mathcal{D}, a' \sim \pi_{\theta'}} \big[ ( r + \gamma \min_{i \in \{1,2\}} Q_{\phi_i'}(s', a') - Q_{\phi_i}(s, a) )^2 \big]$$
   其中目标网络参数 $\phi', \theta'$ 通过指数移动平均（EMA）更新。

4. **Actor损失（Actor Loss）**：联合行为正则化与Q值最大化：
   $$\mathcal{L}(\theta) = \mathcal{L}_{\mathrm{FBC}}(\theta) - \alpha \mathbb{E}_{s \sim \mathcal{D}, a \sim \pi_\theta} \big[ Q_\phi(s, a) \big]$$
   其中 $\mathcal{L}_{\mathrm{FBC}}$ 为平均速度匹配损失（Flow Behavior Cloning），训练 $u_\theta$ 拟合真实平均速度。第二项通过Q梯度引导策略向高价值区域优化，$\alpha$ 为平衡系数。

5. **Critic损失（Critic Loss）**：与DQL一致，但目标动作 $a'$ 通过目标策略 $\pi_{\theta'}$ 的**单步采样**获得，无需多步去噪。

### 关键设计决策

**为什么是平均速度场？** 在标准流匹配中，瞬时速度场 $v_\theta$ 定义的流线本质上是弯曲的，单步沿切线方向外推会导致显著的离散化误差（在玩具实验中表现为模式坍塌，见Figure 4左侧）。OFQL转而学习区间 $[r, t]$ 上的平均速度：
$$u(a_t, r, t; s) \triangleq \frac{1}{t - r} \int_{r}^{t} v(a_\tau, \tau; s) d\tau$$
该平均速度直接连接任意两个时间步，使得 $r=0$ 到 $t=1$ 的单步映射在理论上等价于完整ODE积分（Figure 2(c)）。训练时通过MeanFlow恒等式避免显式积分：
$$u(a_t, r, t; s) = v(a_t, t; s) - (t - r) \frac{d}{dt} u(a_t, r, t; s)$$
实用损失中采用停止梯度（$\mathrm{sg}$）稳定训练：
$$\mathcal{L}_{\mathrm{FBC}}(\theta) = \mathbb{E}_{t, r, r \leq t, (a, s) \sim \mathcal{D}, \epsilon} \big\| u_\theta(a_t, r, t; s) - \mathrm{sg}(u_{\mathrm{tgt}}) \big\|_2^2$$

**与DQL的模块级差异**：OFQL继承了DQL的Q网络架构和行为正则化actor-critic框架，但在三个关键槽位上进行了替换（Table 2消融证实这些替换的累积收益）：

| 模块槽位 | DQL | OFQL |
|---------|-----|------|
| 策略参数化 | DDPM（多步去噪扩散） | 流匹配 + 平均速度场（单步生成） |
| 动作采样 | K步反向链（$K=5\sim50$） | 单步端点映射 $a = \epsilon - u_\theta(\epsilon,0,1;s)$ |
| 行为正则化损失 | $\mathcal{L}_{\mathrm{DBC}}$（得分匹配） | $\mathcal{L}_{\mathrm{FBC}}$（平均速度匹配） |
| Actor更新 | K步BPTT | 单步反向传播 |

### 效率-性能权衡

框架设计消除了DQL的两大瓶颈：**训练时BPTT的优化不稳定性**和**推理时多步去噪的延迟**。在D4RL MuJoCo基准上，OFQL训练耗时仅6.3小时（DQL 5步需11.7小时），推理决策频率达846.5 Hz（DQL 5步为238.7 Hz），同时平均归一化得分从87.9提升至92.5（Figure 1, Figure 3）。这表明**单步流匹配策略并非以牺牲性能为代价换取效率，而是通过更稳定的优化和精确的单步生成实现了效率与性能的双赢**。

### 当前局限

框架目前仅在D4RL离线基准的状态输入任务上验证，扩展到视觉观察任务需要更强的编码器设计。平均速度场的精确学习依赖MeanFlow恒等式中的瞬时速度估计，可能引入近似误差。此外，超参数（流比率 $\lambda$、平衡系数 $\eta$）仍需网格搜索。



### 问题瓶颈与设计动机

DQL的核心瓶颈在于其策略参数化方式：它依赖DDPM的多步去噪过程生成动作，每一步都需要通过噪声预测网络进行反向传播，形成**通过时间的反向传播（BPTT）**。这导致两个致命问题：一是训练和推理速度缓慢；二是长链梯度传播引发优化不稳定和次优收敛。

OFQL的解决思路极为直接——将策略参数化从多步DDPM替换为**学习平均速度场的单步流匹配模型**，从根源上消除迭代去噪和BPTT，无需任何辅助模块或知识蒸馏。

### 核心模块

OFQL的整体架构沿袭DQL的行为正则化Actor-Critic框架，但策略模块发生了根本性重构：

- **策略网络 $u_\theta$**：不再预测DDPM中的噪声 $\epsilon_\theta$，而是输出**平均速度场**。网络输入为噪声动作 $a_t$、起始时间 $r$、目标时间 $t$ 和状态 $s$，输出区间 $[r,t]$ 上的平均位移方向。该网络继承DQL的MLP架构，仅额外增加目标时间步嵌入 $r$。
- **Q网络 $\phi_1, \phi_2$**：双Q学习批评家，采用3层MLP加Mish激活函数，与DQL完全一致，确保比较公平。
- **动作采样器**：单步前向传播即可完成：$a = \epsilon - u_\theta(\epsilon, r=0, t=1; s)$，其中 $\epsilon \sim \mathcal{N}(0, I)$。这是一个可微分的单步操作，梯度无需跨越多个时间步。
- **Actor损失**：联合行为正则化 $\mathcal{L}_{\text{FBC}}$ 与Q值最大化 $-\alpha \mathbb{E}[Q_\phi(s,a)]$。
- **Critic损失**：标准Clipped Double Q-learning，使用目标策略单步采样下一动作。

### 关键公式推导

#### 从瞬时速度到平均速度

流匹配框架中，条件速度场定义为线性路径的导数：

$$a_t = (1-t)a + t\epsilon, \quad v_t = \frac{da_t}{dt} = \epsilon - a$$

其中 $a$ 是数据动作，$\epsilon$ 是噪声，$t \in [0,1]$。传统方法训练网络 $v_\theta$ 拟合**瞬时速度**，但单步外推时误差累积严重。

OFQL的核心洞察是：与其学习瞬时速度，不如直接学习**平均速度**，它直接连接任意两个时间步：

$$u(a_t, r, t; s) \triangleq \frac{1}{t - r} \int_{r}^{t} v(a_\tau, \tau; s) d\tau$$

意义：区间 $[r,t]$ 上的总位移除以区间长度。当 $r=0, t=1$ 时，$u(\epsilon, 0, 1; s) = \epsilon - a$，即从噪声到动作的直线位移。

#### 理想平均速度匹配损失

$$\mathcal{L}_{\mathrm{FBC}^\star}(\theta) = \mathbb{E}_{0 \leq r \leq t \leq 1; s, \epsilon} \big[ \| u_\theta(a_t, r, t; s) - u(a_t, r, t; s) \|^2 \big]$$

直接计算上式需要积分瞬时速度，计算代价高昂。

#### MeanFlow恒等式与实用损失

为解决积分问题，引入MeanFlow恒等式将平均速度与瞬时速度关联：

$$u(a_t, r, t; s) = v(a_t, t; s) - (t - r) \frac{d}{dt} u(a_t, r, t; s)$$

利用条件速度 $v_t = \epsilon - a$ 的解析形式，可推导出无需积分的训练目标。实用FBC损失为：

$$\mathcal{L}_{\mathrm{FBC}}(\theta) = \mathbb{E}_{t, r, r \leq t, (a, s) \sim \mathcal{D}, \epsilon} \big\| u_\theta(a_t, r, t; s) - \mathrm{sg}(u_{\mathrm{tgt}}) \big\|_2^2$$

其中 $\mathrm{sg}(\cdot)$ 为停止梯度算子，$u_{\mathrm{tgt}}$ 由MeanFlow恒等式计算的目标值。

#### 单步动作生成

训练完成后，动作生成仅需一步：

$$a = T_\theta(\epsilon, s) = \epsilon - u_\theta(\epsilon, r=0, t=1; s), \quad \epsilon \sim \mathcal{N}(0, I)$$

无需ODE积分，无需多步去噪。梯度 $\nabla_\theta a$ 在单步内完成，彻底消除BPTT。

#### 完整Actor-Critic损失

Critic损失为标准双Q学习：

$$\mathcal{L}(\phi) = \mathbb{E}_{(s,a,r,s') \sim \mathcal{D}, a' \sim \pi_{\theta'}} \big[ ( r + \gamma \min_{i \in \{1,2\}} Q_{\phi_i'}(s', a') - Q_{\phi_i}(s, a) )^2 \big]$$

Actor损失联合行为正则化与Q值最大化：

$$\mathcal{L}(\theta) = \mathcal{L}_{\mathrm{FBC}}(\theta) - \alpha \mathbb{E}_{s \sim \mathcal{D}, a \sim \pi_\theta} \big[ Q_\phi(s, a) \big]$$

### 理论保证

最小化平均速度匹配损失等价于最小化学得策略与行为分布之间的2-Wasserstein距离上界。这意味着OFQL在保持行为正则化效果的同时，通过非线性端点映射 $T_\theta$ 仍能建模复杂的多模态动作分布——单步生成不牺牲表达能力。



## 实验与关键发现

### 主结果：D4RL基准全面验证

OFQL在D4RL基准的三个核心领域——MuJoCo运动控制、AntMaze导航和Kitchen机械臂操作——上进行了系统评估。如Table 1所示，OFQL在所有领域均一致超越其核心基线DQL（Wang et al., 2022）。

![[assets/figures/papers/paper_list_l40_https_openreview_net_forum_id_60VgwdzxDM/figures/003_Table_1.jpg]]
*Table 1: Comparison of normalized scores on D4RL benchmark across MuJoCo, Kitchen, and AntMaze domains. Bold values indicate the best performance per row*

**MuJoCo运动控制（9个任务）**：OFQL将DQL的平均归一化得分从87.9显著提升至92.5（+4.6），尤其在medium和medium-replay类任务上增益明显。这一结果验证了单步流策略在短期决策任务中的有效性。与扩散规划器（Diffuser、DD）和其他多步扩散策略（IDQL、EDP）相比，OFQL同样保持领先。

**AntMaze导航（4个任务）**：在需要长期策略推理的导航场景中，OFQL的优势更为突出，将DQL的64.6大幅提升至84.6（+20.0）。这表明平均速度参数化在稀疏奖励、长时序依赖任务中具有更强的行为正则化与Q值最大化平衡能力。

**Kitchen机械臂操作（2个任务）**：OFQL从61.6提升至67.0（+5.4），进一步验证了方法在复杂操作任务上的泛化性。

**Adroit灵巧手操作**：在pen-human和pen-cloned两个高维操作任务上，OFQL分别达到79.5±9.5和62.3±10.3，均优于BC和DQL，证明了单步流策略在高维动作空间中的多模态建模能力。

Figure 1的散点图直观展示了OFQL的核心优势：在MuJoCo任务上以约846.5 Hz的决策频率达到92.5的平均归一化得分，而DQL仅以约238.7 Hz达到87.9。OFQL是唯一同时实现高推理速度与强性能的方法。

![[assets/figures/papers/paper_list_l40_https_openreview_net_forum_id_60VgwdzxDM/figures/001_Figure_1.jpg]]
*Figure 1: Performance and decision frequency. Performance (i.e., normalized score) and decision frequency are measured on an A100 GPU and averaged across MuJoCo tasks from D4RL. OFQL achieves both high inference speed and strong performance, clearly outperforming prior baselines*

### 消融实验：单步策略的关键设计验证

**单步生成策略对比（Table 2）**：为验证OFQL单步策略的独特优势，实验对比了四种单步化路径：
- **DQL+DDIM (1步)**：直接使用DDIM一步采样，得分骤降至11.6（-76.3），表明扩散模型的迭代去噪对采样质量至关重要，简单减少步数不可行。
- **FBRAC (1步)**：基于行为正则化Actor-Critic的单步策略，得分67.1，远低于多步基线。
- **FQL (1步)**：使用蒸馏的一步流策略，得分79.2，虽优于前两者但仍不及多步DQL（87.9），说明蒸馏过程存在信息损失。
- **OFQL (1步)**：得分92.6（+4.7），是唯一超越多步基线的单步方法，证明平均速度参数化无需蒸馏即可实现高质量单步生成。

![[assets/figures/papers/paper_list_l40_https_openreview_net_forum_id_60VgwdzxDM/figures/004_Table_2.jpg]]
*Table 2: Comparison of methods (steps) using different improvement strategies toward one-step action generation across 9 MuJoCo tasks. The average normalized score is reported*

**流比率λ的影响（Table 3）**：流比率控制着行为正则化损失中平均速度匹配的区间长度。在HalfCheetah三个数据集上，λ=0.5始终最优（Medium-Expert 95.2, Medium 63.8, Medium-Replay 51.2）。λ过小（0.25）或过大（1）均导致性能下降，尤其在Medium-Replay任务上λ=0时严重退化。这表明适度的流比率是平衡行为约束与策略改进的关键正则化器。

![[assets/figures/papers/paper_list_l40_https_openreview_net_forum_id_60VgwdzxDM/figures/012_Table_3.jpg]]
*Table 3: D4RL scores across HalfCheetah datasets under varying flow ratios*

**时间采样策略（Table 7）**：对数正态采样（logit-normal）相比均匀采样在Medium-Expert（95.2 vs 94.5）和Medium（63.8 vs 61.1）上略有提升，但OFQL对时间采样策略整体不敏感，方法具有较好的鲁棒性。

![[assets/figures/papers/paper_list_l40_https_openreview_net_forum_id_60VgwdzxDM/figures/030_Table_7.jpg]]

**OOD泛化能力（Table 6）**：OFQL在HalfCheetah上的OOD-MSE持续低于DQL（Medium: 0.458 vs 0.462; Medium-Replay: 0.560 vs 0.582），说明平均速度场学习的行为正则化在分布外状态上具有更强的泛化能力，不易产生过估计。

![[assets/figures/papers/paper_list_l40_https_openreview_net_forum_id_60VgwdzxDM/figures/029_Table_6.jpg]]

### 效率分析：训练与推理的双重加速

Figure 3对比了各方法的训练耗时与推理决策频率（均在A100 GPU、PyTorch框架下测量）：

![[assets/figures/papers/paper_list_l40_https_openreview_net_forum_id_60VgwdzxDM/figures/006_Figure_3.jpg]]
*Figure 3: Training Time (↓) and Decision Frequency (↑) over one million steps, averaged on MuJoCo tasks. NFE (Number of Function Evaluations) denotes the denoising steps required by a flow/diffusion model to generate one action from pure noise. During training and inference, OFQL uses only one NFE, while DQL requires multiple ones. It is worth noting that for inference, FQL runs with a one-step policy, but training still relies on a multi-step flow policy to construct distillation targets*

![[assets/figures/papers/paper_list_l40_https_openreview_net_forum_id_60VgwdzxDM/figures/011_Figure_4.jpg]]
*Figure 4: Comparison of distribution modeling capabilities between FM with marginal velocity parameterization (left; evaluated at 1,2,5,10 steps generation) and average velocity parameterization (right; evaluated with one-step generation) on a toy dataset with complex multi-modal structure. Training and Inference Efficiency Comparison. Figure 3 reports the wall-clock training time (1M steps) and decision frequency (Lu et al., 2025b) on an A100 GPU (see Appendix D for experimental protocol). DQL’s training time scales nearly linearly with the number of denoising steps—from 11.7 hours at 5 steps to 49.5 hours at 50 steps—while OFQL completes training in only 6.3 hours. At inference, OFQL reaches 846.5...*

- **训练效率**：OFQL在100万步训练中仅需6.3小时，而5步DQL需11.7小时，FQL需12.1小时。单步反向传播消除了BPTT的计算开销，是加速的核心原因。
- **推理效率**：OFQL决策频率达846.5 Hz，是5步DQL（238.7 Hz）的3.5倍以上。单次前向传播即可生成动作，无需迭代去噪。

值得注意的是，FQL虽然推理时使用一步策略，但其训练依赖多步流策略构建蒸馏目标（NFE=5），因此训练耗时反而最高。

### 分布建模能力的根源分析

Figure 4和Figure 6在玩具多模态数据集上的对比揭示了平均速度参数化（u-param）与瞬时速度参数化（v-param）的本质差异：

- **v-param（瞬时速度）**：在1步生成时出现严重模式坍塌，仅覆盖部分模态；随着步数增加（2→5→10步），采样质量逐步改善但始终需要多步ODE积分。
- **u-param（平均速度）**：仅需单步生成即可达到DDPM 10步的采样质量，实现对复杂多模态分布的精确覆盖。

Figure 7进一步验证：DDPM在1步去噪时完全失效，而u-param的单步生成质量与DDPM 10步相当。这一结果从分布建模层面解释了OFQL在离线RL中成功的原因——平均速度场学习的行为正则化损失是行为分布与所学策略间2-Wasserstein距离的上界，在保持多模态表达能力的同时实现了精确的单步生成。

### 失败模式与局限性

**视觉观察任务（Table 5）**：在基于像素输入的视觉操作任务上，OFQL（54.0±9.0, 8.0±3.0）显著落后于FQL（98.0±3.0, 21.0±11.0）。这表明当前的MLP策略网络和简单状态条件注入方式不足以处理高维视觉输入，需要更强的编码器和条件注入策略。

![[assets/figures/papers/paper_list_l40_https_openreview_net_forum_id_60VgwdzxDM/figures/028_Table_5.jpg]]

**流比率的任务敏感性**：Table 3显示，Medium-Replay任务在λ=0时性能严重退化，且最优λ=0.5可能不适用于所有任务类型，超参数仍需网格搜索。

**方法验证范围**：当前验证仅限于D4RL离线基准，对其他离线RL数据集和在线RL场景的泛化性尚未评估。平均速度场的精确学习依赖MeanFlow恒等式中的瞬时速度估计，该估计可能引入近似误差。

### 补充图表

![[assets/figures/papers/paper_list_l40_https_openreview_net_forum_id_60VgwdzxDM/figures/027_Table_4.jpg]]



## 定位与知识库关联

### 核心瓶颈与因果机制

离线强化学习中，扩散Q学习（Diffusion Q-Learning, DQL）类方法的核心瓶颈在于其策略参数化依赖多步去噪扩散概率模型（DDPM）。具体而言，DQL通过K步反向高斯链（通常K=5~50）生成动作，导致两个连锁问题：**推理延迟**——每次动作采样需执行K次网络前向传播；**训练不稳定**——策略梯度需通过K步去噪过程进行反向传播（BPTT），梯度路径长且易受噪声干扰，导致优化困难与次优收敛。

OFQL的因果旋钮定位明确：**将策略参数化从多步DDPM替换为学习平均速度场的单步流匹配模型**。这一替换直接消除了迭代去噪和BPTT，无需蒸馏或辅助模块。核心洞察在于：流匹配框架中，学习**平均速度场**（而非瞬时速度场）使得从噪声到动作的映射退化为直线式单步生成——动作通过端点映射 $a = \epsilon - u_\theta(\epsilon, r=0, t=1; s)$ 直接获得，既保留了多模态表达能力，又稳定了Q值最大化过程。

### 方法谱系中的定位

OFQL处于**行为正则化Actor-Critic离线RL**与**生成式策略**的交叉节点，其方法谱系可沿两条轴线梳理：

**轴线一：离线RL策略参数化演进**

| 方法 | 策略形式 | 关键特征 |
|------|---------|---------|
| **BC** | 确定性/高斯策略 | 纯行为克隆，无Q值引导 |
| **TD3-BC** (Fujimoto & Gu, 2021) | 确定性策略+行为克隆正则 | 简单正则化，单模态 |
| **IQL** (Kostrikov et al., 2021) | 隐式Q学习+优势加权回归 | 免去分布外动作评估 |
| **DQL** (Wang et al., 2022) | DDPM多步扩散策略 | 多模态行为建模+BPTT |
| **IDQL** (Hansen-Estruch et al., 2023) | 扩散策略+隐式Q学习 | 解耦策略评估与改进 |
| **EDP** (Kang et al., 2023) | 扩散策略+高效采样 | 减少去噪步数 |
| **FQL** (Park et al., 2025) | 流匹配策略+蒸馏 | 训练多步、推理单步 |
| **OFQL** (本文) | 流匹配+平均速度场 | 训练与推理均单步 |

OFQL对DQL的改进是**结构性替换**而非增量修补：四个关键槽位全部改变（策略参数化、动作采样、行为正则化损失、Actor更新方式），但继承了DQL的Q网络架构（3层MLP+Mish激活）和行为正则化Actor-Critic框架，保证了比较的公平性。

**轴线二：生成模型范式转换**

扩散模型（DDPM）与流匹配（Flow Matching）的根本差异在于路径几何：
- **DDPM**：前向加噪与反向去噪均为弯曲随机路径，单步去噪质量差，需多步迭代（Figure 2d）。
- **流匹配（瞬时速度v-param）**：确定性ODE路径，但边际速度场在早期步数存在模式坍塌（Figure 4左），需多步积分。
- **流匹配（平均速度u-param）**：学习区间平均速度，路径退化为直线，单步生成即可达到DDPM 10步的采样质量（Figure 4右）。

OFQL的贡献在于将**MeanFlow建模**（Geng et al., 2025）首次引入离线RL的策略学习，并通过Q梯度引导平均速度学习，而非纯监督学习。平均速度匹配损失 $\mathcal{L}_{\mathrm{FBC}}$ 是行为分布与所学策略间2-Wasserstein距离的上界，保证了行为正则化的理论正当性。

### 适用边界与局限

**已验证的有效域：**
- **D4RL基准**：MuJoCo运动控制（9任务，平均归一化得分92.5）、AntMaze导航（4任务，84.6）、Kitchen操作（2任务，67.0）、Adroit灵巧手（2任务，79.5/62.3），全面超越DQL。
- **数据质量谱**：在中等（Medium）、中等回放（Medium-Replay）、中等专家（Medium-Expert）等不同质量数据上均表现稳健。
- **效率维度**：训练耗时6.3小时（vs DQL 5步的11.7小时），推理频率846.5 Hz（vs DQL的238.7 Hz），在A100 GPU上测量。

**已知局限与待验证边界：**

1. **视觉输入扩展困难**：OFQL在视觉观察任务上的性能仍落后于专门的视觉基线（如FQL）。将流匹配策略扩展到高维像素输入需要更强的编码器和条件注入策略，当前MLP架构难以直接适配。

2. **在线RL泛化未验证**：方法仅在D4RL离线基准上测试，对在线交互场景的泛化性（如探索-利用平衡、非平稳数据分布）尚未评估。

3. **超参数敏感性**：流比率λ在0.5附近表现最优（HalfCheetah Medium-Expert 95.2），过小（0.25）或过大（1）会导致性能下降，尤其在Medium-Replay任务上λ=0时严重退化。这意味着λ需要针对任务进行网格搜索。

4. **平均速度估计的近似误差**：实用FBC损失依赖MeanFlow恒等式 $u(a_t, r, t; s) = v(a_t, t; s) - (t-r)\frac{d}{dt}u(a_t, r, t; s)$ 中的瞬时速度估计，该估计可能引入近似误差，在复杂分布边缘处影响建模精度。

5. **随机环境鲁棒性边界不明**：单步生成策略在高度随机或部分可观测环境中的鲁棒性尚未系统研究。

### 开放问题

1. **如何将OFQL高效扩展到基于视觉或点云的连续控制任务？** 这需要设计适配高维输入的编码器架构和条件注入机制，同时保持单步生成的计算优势。

2. **OFQL能否通过在线微调进一步提升样本效率与策略质量？** 单步策略的在线探索行为与多步扩散策略可能存在差异，需要研究在线交互下的稳定性与改进潜力。

3. **平均速度参数化是否可以推广到目标条件或多任务强化学习？** 将条件信息融入平均速度场可能实现零样本泛化，但需验证条件注入对单步生成质量的影响。

4. **在更复杂的随机环境中，单步生成策略的鲁棒性边界是什么？** 单步确定性映射可能在高熵场景下丢失必要的随机性，需要研究是否可通过噪声注入或混合策略弥补。



## 原文 PDF

![[paperPDFs/ICLR_2026/One_Step_Flow_Q_Learning_Addressing_the_Diffusion_Policy_Bottleneck_in_Offline_Reinforcement_Learning.pdf]]
