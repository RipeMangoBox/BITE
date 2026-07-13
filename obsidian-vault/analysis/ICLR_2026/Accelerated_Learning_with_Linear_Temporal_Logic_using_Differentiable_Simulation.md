---
title: "Accelerated Learning with Linear Temporal Logic using Differentiable Simulation"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/Accelerated_Learning_with_Linear_Temporal_Logic_using_Differentiable_Simulation.pdf
project_link: null
code_link: null
aliases:
- DRLLR
- ALLTLUDS
tags:
- ICLR_2026
- topic/reinforcement_learning_planning_agents
- topic/reinforcement_learning_planning_agents/planning_control
core_operator: "通过概率软标签（soft labeling）将离散自动机状态和奖励变为对动作可微，使得可以利用一阶梯度信号进行高效策略优化。"
primary_logic: "采用概率化软标签将LTL派生的自动机转换为可微的马尔可夫转换函数，从而让LTL奖励变得可微，在保持规范正确性的同时，利用梯度的低方差特性显著加速策略学习。"
claims:
- "通过软标签技术为连续环境生成概率性的ε-动作与自动机转移，保证了奖励和状态对动作的可微性，从而缓解了LTL固有的稀疏奖励问题。"
- "建立了连接自动机接受条件与可微框架的形式化保证，导出了离散与可微LTL回报之间差异的可调上界。"
- "在多个复杂、非线性、接触丰富的连续控制任务中，提出方法获得高达离散基线两倍的回报。"
- "Hopper 上 Probability of LTL satisfaction (Pr) = >0.8 (within 20M steps)"
---

# Accelerated Learning with Linear Temporal Logic using Differentiable Simulation

> [!tip] 核心洞察
> 采用概率化软标签将LTL派生的自动机转换为可微的马尔可夫转换函数，从而让LTL奖励变得可微，在保持规范正确性的同时，利用梯度的低方差特性显著加速策略学习。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 利用可微分仿真的线性时序逻辑加速学习 |
| 英文题名 | Accelerated Learning with Linear Temporal Logic using Differentiable Simulation |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=zbdhhlIy8o) |
| Topic | #topic/reinforcement_learning_planning_agents #topic/reinforcement_learning_planning_agents/planning_control |
| Method | Differentiable Reinforcement Learning with LTL (∂RLs) |
| Dataset | Hopper, Cheetah, Cheetah (reward machines) |

> [!tip] 效果简介
> - Hopper 上，Probability of LTL satisfaction (Pr) 为 >0.8 (within 20M steps)，对比 PPO needs 100M steps to reach similar level，变化 significantly faster convergence。
> - Cheetah 上，Probability of LTL satisfaction (Pr) 为 >0.9，对比 PPO gets suboptimal policy, SAC fails，变化 higher satisfaction probability。
> - Cheetah (reward machines) 上，Return 为 differentiable RM (SHAC, CRM) significantly outperforms all discrete RM baselines，对比 HRM+RS (discrete RM)，变化 superior returns。

## 概要

利用线性时序逻辑（LTL）描述复杂强化学习任务时，离散的自动机接受条件通常产生稀疏奖励信号，而人工设计的密集奖励容易破坏规范的正确性。本文引入一种端到端框架——可微分强化学习与线性时序逻辑（∂RLs），首次将LTL形式规范与可微分仿真器深度集成，通过概率软标签将离散自动机状态和奖励转化为对动作可微的形式，从而利用一阶梯度信息显著加速策略学习。

核心机制是将LTL公式转换为极限确定性Büchi自动机（LDBA），再与环境的马尔可夫决策过程（MDP）构造乘积MDP。在此基础上，用sigmoid激活函数为原子命题生成连续的软标签概率，使自动机状态转移和对应的奖励函数均对动作可微。理论与实验证据表明，该方法在维持规范正确性的同时大幅提升学习效率：在一维停车示例中可微LTL回报在满意度边界附近产生平滑过渡，梯度估计方差显著低于零阶方法；在Hopper、Cheetah等多类连续控制任务上，∂RLs收敛速度远超使用离散LTL奖励的PPO和SAC基线，达到最高约两倍的回报，且消融实验确认性能增益源于复杂规范下的可微性而非简单的任务结构。

仍需人工验证的方面包括部分可微混合系统（如物理仿真可微但控制模块离散）的扩展可行性，以及超参数β与信号函数设计的自动化方法。



将任务目标以线性时序逻辑（LTL）公式形式化，为强化学习（RL）提供了一种可解释且组合性强的规范方式，尤其适用于需要时序约束与长期安全性的连续控制问题。但在实际中，从LTL规范中导出训练信号通常面临**奖励稀疏性**这一瓶颈：传统做法基于离散的Büchi自动机接受条件产生二值奖励（如图1中间散点所示），不提供有效的梯度信息，导致无模型的PPO、SAC等算法在复杂非线性任务上收敛缓慢、方差高，甚至完全失败（如Cheetah环境中SAC无法学到有意义策略）。如果为缓解稀疏性而引入手工设计的密集奖励，则极易偏离原始LTL语义，破坏规范的正确性。

另一方面，以可微分仿真为代表的一阶信息获取手段正逐步成熟，理论上能够为RL提供低方差的梯度信号，从而极大地提升样本效率。然而，**将离散的LTL自动机转化为可微分形式，使奖励和自动机状态对连续动作可微，仍是一个开放难题**。已有的奖赏机（Reward Machine）方法将自动机配合离散奖励使用，但仅适用于协同安全LTL或有限域LTL（LTLf），无法直接扩展到完整的LTL无限域设定；且其离散奖励同样无法利用梯度信息。

针对上述缺口，本文的动机是：通过一种**概率化软标签机制**，将LTL导出的离散自动机转换为可微的马尔可夫转移函数，在保持规范语义正确性的前提下，构造出对策略参数可微的奖励与折扣信号。这使策略优化能够同时利用模型梯度（一阶信息）与自动机结构，从而突破稀疏奖励的瓶颈。正式的理论分析保证离散与可微LTL回报之间的差异存在一个**可调节的上界**（定理2），为可微近似的可靠性提供了定量依据。在Hopper、Cheetah、Ant等多个接触丰富的高维任务中，这一方法使策略满足LTL规范的概率（Pr）在2000万步内超过0.8–0.9，回报达到离散基线（PPO）的两倍左右，且不需要任何启发式奖励塑形。



## 核心方法与创新机理

基于线性时序逻辑（LTL）形式规范的强化学习面临一个根本矛盾：**LTL 派生的奖励信号通常高度稀疏**，而手工设计的密集奖励又极易破坏规范正确性。可微分仿真器能提供状态-动作梯度的精确信道，但直接将离散的自动机接受条件嵌入可微管线，会导致关键的梯度断裂。本文的核心创新正是在于 **将离散的 Büchi 自动机“软标签化”，使得 LTL 规范天然产生的奖励与自动机状态转移对连续动作可微**，从而将低方差的一阶梯度信号引入策略优化，在保持规范语义不变的前提下实现学习效率的质变。

具体而言，这一创新通过 **两个关键槽位（changed slots）** 的重构落到了方法层：  
1. **奖励函数**——从传统依据 Büchi 接受状态的硬性 `0/1` 奖励（公式 (2)）转变为基于概率软标签的连续可微奖励；  
2. **自动机状态转移**——从由离散原子命题标签确定的确定性跳转，转变为依赖 sigmoid 概率标签与 ε-动作的**概率转移**（公式 (4)–(6)）。  

其因果机制可概括为：对每个连续状态通过信号函数 $g(s)$ 计算 sigmoid 激活 $h(g(s))$，得到原子命题成立的软概率；这些概率一方面软化自动机状态分布，另一方面生成概率化的 ε-动作选择，使整个乘积 MDP 的转移函数与奖励在解析上对动作可微。该构造衍生出两点关键结果：  
- **低方差梯度**：与不可微的零阶估计相比，可微奖励的梯度在满足区边界之外也能提供平滑的学习方向，从而避免稀疏回报下的更新死区；  
- **形式化差异上界**：定理 2 给出了离散 LTL 回报与可微 LTL 回报之间可调节的上界 $|G^{disc.}(\sigma)-G^{diff.}(\sigma)|<\frac{1}{1+\frac{1-\beta}{(1-h(\varsigma))^{|\mathcal{A}|}}}$，证明了两者在误差可控的前提下同构，消除了“可微近似会破坏规范”的担忧。

实验证据有力支撑了这一创新：  
- 在 Hopper 上，∂RLs 在 **20M 步内** 即达到 LTL 满足概率 >0.8，而 PPO 需 100M 步；  
- 在 Cheetah 上，∂RLs 达到满足概率 >0.9，基线 PPO 仅获次优策略，SAC 完全失败；  
- 消融实验表明，**一旦将可微奖励替换回离散版本**，可微 RL 算法（SHAC/AHAC）立即退化为无效策略（图 7），而当简化规范使奖励本身不再稀疏时，所有方法均能成功（图 8），证实性能优势的确源于复杂规范下的可微性，而非其他混杂因素。

该创新的**核心效力源于处理“稀疏规范—连续控制”的结构性鸿沟**，其薄弱点亦很明确：依赖完全可微的环境（含状态标签函数），无法直接处理离散状态 MDP 或含有不可微模块的混合系统；同时超参数 β 的选择在理论正确性与收敛稳定性之间缺乏自动化方案，大型自动机带来的转换矩阵显存占用也构成扩展瓶颈。这些限制恰好为后续研究划定了靶点。



![[assets/figures/papers/iclr26_0005_zbdhhlIy8o_Accelerated_Learning_with_Linear_Temporal_Logic/figures/003_Figure_1.jpg]]
*Figure 1: LTL Returns and Derivatives. Left: The parking scenario where the car must brake to stop in the parking area without entering the grass field ($\varphi_$p$). Middle: LTL satisfaction probability and return estimates from discrete and differentiable LTL formulations as functions of deceleration. Right: LTL return gradients with respect to deceleration and their standard deviation. The key challenge in learning from LTL arises from slightly-sloped regions and sharp changes in the returns produced by discrete LTL rewards. Our differentiable LTL approach not only smooths these abrupt changes but also enables the use of low-variance first-order gradient estimates essential for efficient learning.*

∂RLs（Differentiable Reinforcement Learning with LTL）的整体流程围绕一个核心思路展开：将线性时序逻辑（LTL）导出的离散自动机转换为可微的概率化转移结构，从而把稀疏且不连续的 LTL 奖励变成对动作可微的连续信号，使基于梯度的可微强化学习能够高效优化策略。

**输入**→**LDBA 构建**→**乘积 MDP 装配**→**软标签与可微奖励生成**→**可微 RL 策略优化**，五个模块串联，形成一个端到端的学习管线。

1. **从 LTL 到 LDBA**  
   给定任务规范（一个 LTL 公式），首先将其翻译为极限确定 Büchi 自动机（LDBA）。LDBA 利用 Büchi 接受条件取代一般 Rabin 条件，使奖励设计更简洁，同时保证了有限状态记忆的表达力。

2. **乘积 MDP 构建**  
   将原始连续控制 MDP 的状态和动作用 LDBA 的指示向量进行增广，得到乘积 MDP。乘积状态编码了系统的物理状态和当前自动机状态，乘积动作则附加了由自动机决定的 ε‑动作。这一步把需要有限记忆的 LTL 满足问题转化为标准 MDP 上的无记忆策略学习问题（Proposition 1）。

3. **软标签与可微自动机转换**  
   在连续状态空间中，原子命题的满足不再是硬性的真/假，而通过信号函数 $g(s)$ 和 sigmoid 激活 $h(g(s)) = 1/(1+\exp(-g(s)))$ 计算“软标签”概率。由此，原本确定的自动机状态转移变为概率化的软转移（式 4‑6），并进一步导出状态依赖的可微奖励 $R(\mathbf{s})$ 和可微折扣因子 $\Gamma(\mathbf{s})$（式 2、5‑6、8）。奖励函数以 Büchi 接受状态为基础，折扣机制实现了对无穷轨迹的有限折扣回报（Theorem 1）。

4. **可微 RL 优化**  
   获得可微 LTL 回报后，可以直接嵌入任何需要梯度信号的可微 RL 算法（如 SHAC、AHAC）。梯度的传播路径为：策略输出动作 → 可微仿真器产生下一状态 → 软标签更新自动机状态 → 自动机状态给出奖励与折扣 → 通过反向传播将梯度沿轨迹传递至策略参数。该过程利用了可微奖励的低梯度方差特性（相比于 REINFORCE 之类的零阶估计），大幅加速了复杂规范下的策略收敛（Figure 3 的对比实验）。

整个框架的**关键因果机制**是软标签技术将离散自动机上的硬判定松弛为动作可微的概率分布，同时保留规范的正确性——在离散与可微回报之间提供了可调的差异上界（Theorem 2），从而在保持 LTL 语义的前提下，允许使用高效的一阶梯度更新。实验表明，∂RLs 在不改变 LTL 规范的情况下，使 Hopper 任务在 20M 步内达到满足概率 >0.8（PPO 需要 100M 步），Cheetah 上满足概率 >0.9（PPO 仅能得到次优策略，SAC 失败），并在奖励机扩展实验中显著超越所有离散基线（Table 1）。

**输入输出流**可概括为：  
- 输入：LTL 公式 $\varphi$，仿真环境动力学（包括可微的状态转移函数和信号函数）。  
- 输出：一个在乘积 MDP 上训练出的策略，该策略直接优化可微 LTL 回报，从而实现对原 LTL 规范的高概率满足。

这一管线对“完全可微”假设的依赖也构成了其主要限制：当仿真或自动机中存在不可微模块时，难以直接适用；当 LDBA 状态空间过大时，转换矩阵可能超出 GPU 显存。这些边界需要在工程实现中给予注意。



可微LTL强化学习（∂RLs）的整体流水线包括：将LTL公式编译为限确定Büchi自动机（LDBA）；构造产品MDP以将自动机离散状态嵌入连续控制问题的状态‑动作空间；通过软标签技术赋予自动机状态转移以概率可微性；基于软自动机状态计算可微奖励与折扣因子；最后在可微仿真器上通过反向传播或一阶梯度算法进行策略优化。整个链条的关键在于**将离散的自动机接受条件转变为对动作连续可微的奖励信号**，从而利用低方差的梯度信息加速学习。

### 软标签与可微自动机转移

真实状态$s$是否满足某个原子命题$AP$，通常由一条信号函数$g(s)$的非线性输出决定。为保留可微性，文章使用 **sigmoid 激活** 对信号函数进行“软”化，得到原子命题为真的概率（Equation 3）：

$$
h(g(s)) = \frac{1}{1+\exp(-g(s))
$$

其中$h(g(s))\in(0,1)$。该概率值取代原来的二值真值标签，被用于计算自动机中各边的转移权重。对于LDBA中的每一条边，其转移概率由源状态、目标状态及所有相关原子命题的软标签概率联合确定（Equations 4‑6）。这使得自动机状态的更新函数变为**对状态‑动作对可微的概率转移算子**$T^{\text{diff}}$，从而打通从原始动作到自动机状态再到最终回报的梯度链路。

### 可微奖励与折扣函数

产品MDP的状态$\mathbf{s}$融合了原始MDP状态和LDBA的独热指示向量。文章基于Büchi接受条件定义了 **可微的、逐状态‑动作的奖励$R^{\text{diff}}$和折扣因子$\Gamma^{\text{diff}}$**，其数值由当前自动机状态的软标签分布决定（参考Equations 2, 5‑6, 8）。这些函数对动作连续可微，因此其一阶梯度可以通过可微仿真器和LDBA转移矩阵直接反向传播。

与离散版本相比，可微LTL奖励在满足区域边界附近产生平滑过渡而非尖锐跳变（见Figure 1），从而缓解了LTL规范天然存在的稀疏奖励问题，同时保持了由Büchi条件保证的规范正确性（Theorem 1）。

### 理论保证：离散与可微回报的差异上界

为了定量刻画软标签引入的偏差，文章证明了 **离散LTL回报$G^{\text{disc}}$与可微LTL回报$G^{\text{diff}}$之间的最大差异可由一个可调参数$\beta$和原子命题的容限$\varsigma$联合控制**（Theorem 2）：

$$
|G^{\text{disc}}(\sigma) - G^{\text{diff}}(\sigma)| < \frac{1}{1 + \frac{1-\beta}{(1-h(\varsigma))^{|\mathcal{A}|}}}
$$

其中$\beta$是折扣因子中的接受状态折扣参数，$\varsigma$由信号函数的容差决定，$|\mathcal{A}|$为LDBA的转移字母表大小。该上界表明：通过增大信号函数的“锐度”（使$h(\varsigma)$趋近1）并适当调节$\beta$，可以随意缩小可微近似带来的回报偏差，从而在 **保持近似正确性的同时获取低方差的梯度**。

### 关键模块总结

- **LDBA构造**：将LTL公式转化为带接受条件的有限状态自动机，为奖励定义提供严格基础。
- **产品MDP**：将自动机状态作为额外记忆并入系统状态，使最优策略的搜索降维到无记忆策略空间。
- **软标签（Soft labeling）**：用sigmoid概率替代二值原子命题，实现可微的自动机转移。
- **可微奖励与折扣**：从软自动机状态导出对动作可微的$R^{\text{diff}}$和$\Gamma^{\text{diff}}$。
- **梯度优化**：利用可微仿真器进行BPTT或梯度上升，大幅加速规范满足策略的学习（在hopper任务中逼近$Pr>0.8$所需步数仅为PPO的1/5）。



## 实验与关键发现

**实验设置与公平性**。所有比较均在相同的连续控制环境和LTL规范下进行，各算法超参数均单独调优以确保公平。可微RL基线（SHAC、AHAC）使用本文提出的可微LTL奖励，模型无关基线（PPO、SAC）使用原始的离散LTL奖励。评估的核心指标为 **LTL满足概率（Pr）**，其取值范围在0到1之间，等价于期望折扣回报。

### 主结果：可微LTL奖励显著加速策略收敛

**Figure 2** 汇总了不同环境中各算法的学习曲线与最终回报分布。关键发现如下：

![[assets/figures/papers/iclr26_0005_zbdhhlIy8o_Accelerated_Learning_with_Linear_Temporal_Logic/figures/004_Figure_2.jpg]]
*Figure 2: Comparison Across Environments: Differentiable vs. Discrete LTL Rewards. The wider plots show the learning curves of all baseline algorithms, while the narrower plots on the right display the maximum returns achieved after 100 M steps. All results are averaged over 5 random seeds, and the curves are smoothed using max and uniform filters for visual clarity. The reported returns, bounded between 0 and 1, serve as proxies for the probability of satisfying the LTL specifications. In all the environments, algorithms utilizing differentiable LTL rewards (SHAC, AHAC) rapidly learn near-optimal policies, whereas those relying on discrete LTL rewards (PPO, SAC), display high variance, converge slowly, or fail entirely.*

- **跳跃机器人（Hopper）**：PPO 需要超过 1 亿步才能达到的满足概率，∂RLs（SHAC/AHAC）在 **2000 万步以内** 即可收敛至 Pr > 0.8（锚点 Figure 2，置信度 1.0）。SAC 在该任务上几乎无法取得进展。
- **猎豹机器人（Cheetah）**：∂RLs 最终稳定在 **Pr > 0.9** 的高满足水平，而 PPO 学到的是次优策略，SAC 完全失败（置信度 1.0）。
- **奖励机器场景（Cheetah, Table 1）**：采用可微 RM 的 SHAC 与 CRM 在所有训练步长（500K–3000K）上，均显著优于使用离散 RM 的 HRM+RS 等基线，验证了可微化方法对 **奖励机器（RM）** 的自然泛化能力（置信度 0.9）。

![[assets/figures/papers/iclr26_0005_zbdhhlIy8o_Accelerated_Learning_with_Linear_Temporal_Logic/figures/010_Table_1.jpg]]
*Table 1: Comparison between differentiable RMs and discrete RMs for Cheetah*

上述结果的内在机制是：基于软标签的概率化自动机转换产生了对动作可微的奖励信号，使得一阶梯度能够提供低方差、密集的方向性信息，从而引导策略快速进入高回报区域（锚点 part_005 method_evidence）。相比之下，离散奖励仅在 Büchi 接受状态处产生稀疏信号，模型无关梯度估计方差高且缺乏方向引导性。

### 消融实验：可微性是关键瓶颈

两组消融实验直接验证了“可微性”在复杂规范下的决定性作用：

1. **替换为离散 LTL 奖励（Figure 7）**：将 SHAC 和 AHAC 原本使用的可微奖励替换为与其结构相同的离散版本后，两者在 Cheetah 和 Ant 任务上完全无法学到合理策略，最终回报接近零（置信度 1.0）。这说明仅依靠可微模拟器而缺少可微奖励无法解决稀疏规范奖励问题，**可微性必须贯穿奖励链**。
2. **简化LTL公式（Figure 8，公式(21)）**：当原始复杂规范被简化为易满足的形式后，所有算法（包括 PPO 和 SAC）均可学习到接近最优的策略（Pr > 0.9）。结合第一组消融，可确认本文方法的性能优势**并非来自模拟器或算法本身，而在于处理复杂规范时可微奖励提供的有效梯度信号**（置信度 1.0）。

![[assets/figures/papers/iclr26_0005_zbdhhlIy8o_Accelerated_Learning_with_Linear_Temporal_Logic/figures/014_Figure_7.jpg]]
*Figure 7: Ablation study for differentiability of LTL rewards. The maximum returns obtained after 100 M steps for SHAC and AHAC (∂RLs) with discrete LTL rewards. Returns (0 to 1) indicate LTL satisfaction probabilities. With discrete LTL rewards, ∂RLs fail to learn near-optimal policies. However, as shown in Fig. 2, with our differentiable LTL rewards, they can successfully learn near-optimal policies.*

![[assets/figures/papers/iclr26_0005_zbdhhlIy8o_Accelerated_Learning_with_Linear_Temporal_Logic/figures/015_Figure_8.jpg]]
*Figure 8: Ablation study for complexity of LTL formulas. The maximum returns obtained after 100 M steps for simplified LTL formulas (21). Returns (0 to 1) indicate LTL satisfaction probabilities. Under these simpler specifications, both ¬∂RLs and ∂RLs successfully learn near-optimal policies. However, as shown in Fig. 2, the performance of discrete ¬∂RLs degrades dramatically with increasing LTL complexity–unlike differentiable ∂RLs, which maintain reasonable performance by leveraging the LTL rewards differentiability.*

### 梯度信号分析

停车示例（Figure 1）直观地展示了可微LTL奖励与离散奖励的差异：离散奖励在满足边界处产生陡峭跳变，而可微版本在边界附近平滑过渡，同时其梯度具有较低方差，这使得一阶随机梯度下降能够比零阶方法更快收敛（Figure 3）。理论层面，**定理2** 给出了离散与可微 LTL 回报之间差异的可调上界，确保了规范正确性在可微化过程中不会被破坏。

![[assets/figures/papers/iclr26_0005_zbdhhlIy8o_Accelerated_Learning_with_Linear_Temporal_Logic/figures/006_Figure_3.jpg]]
*Figure 3: Convergence speed comparison of stochastic gradient descent algorithms using $\bar{\nabla}_{\theta}^{[0]}$ and $\bar{\nabla}_{\theta}^{[1]}$ for the parking example ($N=10$).

### 失败模式与已知局限

尽管效果显著，本文方法存在若干需要关注的失效风险：

- **无法处理固有离散状态的任务**：方法依赖连续状态空间的可微性，纯离散 MDP 或状态空间存在硬性离散的模块无法直接应用。
- **依赖全可微模拟器**：要求环境动态、状态标签（信号函数）和自动机转移全部可微，若实际系统含有不可微的物理引擎或逻辑模块则难以迁移。
- **超参数 β 的敏感性**：定理 2 揭示 β 是平衡理论正确性与训练稳定性的关键，批量实验中 β 需手动从小到大调节，缺乏自动调优机制。
- **大型自动机的内存瓶颈**：当 LTL 导出的 LDBA 状态数过大时，转换矩阵可能超出 GPU 显存，导致训练不可行。目前未提供稀疏化或因子化方案。
- **尖锐信号函数的梯度爆炸**：若原子命题的信号函数存在陡峭区域（如严格判决的阶跃），会产生极大梯度，损害学习稳定性，需要精心设计平滑的信号函数。
- **部分可微混合系统的缺失**：对物理仿真可微但控制逻辑离散等混合场景尚无解决方案（需手动验证该限制的彻底性）。

### 重要图表结论汇总

- **Figure 2**：∂RLs 在所有任务上相较离散归一化算法（PPO/SAC）收敛速度与最终满足概率均有数量级提升，验证了可微 LTL 奖励对长时序规范任务的核心价值。
- **Figure 3**：一阶梯度收敛速度远优于零阶梯度，从优化角度支撑了可微架构的加速效应。
- **Figure 7**：直接移除可微性后梯度失效，策略无法学习。
- **Figure 8**：简化规范后性能差距消失，反向证明复杂规范下可微性是性能瓶颈。
- **Table 1**：可微化方法可无缝扩展至奖励机器，并保持优势，表明框架的模块化特性。

**综上所述**，实验充分证明通过软标签将 LTL 自动机可微化，可以解决复杂接触丰富连续控制任务中的稀疏规范奖励瓶颈，主要性能提升来自梯度低方差与密集的方向引导；系统的脆弱性则集中在可微性假设和自动机规模上。



## 定位与知识库关联

本工作提出的 **∂RLs（Differentiable Reinforcement Learning with LTL）** 属于将形式化时序逻辑规范融入强化学习的谱系，处于 **从离散奖励到可微奖励的关键转折点**。此前利用线性时序逻辑（LTL）的 RL 方法（例如 PPO、SAC 与奖励机 RM 的结合）普遍采用基于 Büchi‐接受条件的离散、状态依赖的奖励函数（式 (2)）。这种离散奖励虽能精确刻画规范满足性，却造成了 **极度稀疏的奖励信号**：接受状态与非接受状态之间缺乏平滑的中间梯层，导致模型无关的 RL 算法收敛极慢或陷入次优，Hopper 环境中 PPO 需 1 亿步才能逼近 ∂RLs 在 2000 万步达到的满足概率（Pr > 0.8），Cheetah 等复杂规范下 SAC 甚至完全失败。

∂RLs 的核心突破在于通过 **概率化软标签（soft labeling）** 将 LDBA 的离散自动机状态和转移映射为动作上的可微函数（式 (3)–(6)），从而使 LTL 奖励也能够进行端到端的一阶梯度优化。该设计不仅保留了规范的正确性——理论给出了离散回报与可微回报之间的可调上界（Theorem 2）——而且大幅降低了梯度方差，使 SHAC、AHAC 等可微 RL 算法能够快速发现高回报区域。因此 ∂RLs 与已有的基于离散自动机的模型无关 RL 基线（PPO、SAC）构成 **直接替换关系**：奖励生成模块由二元跳变函数变为 Sigmoid 型平滑函数，其余策略优化部分无需修改，但学习效率与终端性能显著提升。

与 **信号时序逻辑（STL）** 和 **时态逻辑 TLTL** 等谱系相比，∂RLs 并未采用基于鲁棒性分数的稠密奖励设计，而是坚持离散时间语义和 LDBA 的紧凑自动机构造。STL 的鲁棒性分数容易破坏马尔可夫性，难以直接用于长序列、随机环境下的值函数方法；TLTL 虽然语法与本文所定义的可微 LTL 一致，但其语义直接使用状态轨迹而不构建自动机，缺少有限记忆机制。∂RLs 则在保留离散语义的前提下引入软标签，兼顾了正确性与可微性，因此既不属于“稠密奖励着色”路线，也不是纯离散状态机路线，而是在两者之间建立了 **可调谱系**（通过超参数 β 控制接近离散程度）。

该方法可以直接泛化至 **奖励机（RM）框架**：只要 RM 是由 co‑safe LTL 或 LTLf 导出的自动机，无需任何修改便可使用本文的可微奖励生成。实验显示，在 Cheetah 的两个任务上，可微 RM（SHAC、CRM）在 300 万步内的回报全面超越离散 RM 基线（HRM+RS），证明可微自动机奖励在更一般的结构中也具有优势。

**适用边界**十分清晰：∂RLs **仅适用于系统动态与信号函数都可微的连续状态‑动作环境**。它必须依赖可微仿真器（如计算图形式的物理引擎）和支持反向传播的信号函数；对于存在不可微模块的混合系统，以及完全离散的 MDP，目前无法直接应用。另外，自动机状态的维数决定了计算图上的转换矩阵大小，当 LTL 公式产生的自动机状态数过大时，**GPU 显存可能不足以承载完整的批处理转换**，导致实际计算不可行。信号函数若出现尖锐决策边界（例如在满足与不满足区域之间快速切换），会产生 **高幅梯度**，不利于学习稳定性，因而需要精心设计平滑信号。

**局限性总结**如下（均需结合具体环境配置进行人工评估）：

- **纯离散或不可微系统无法处理**：当前方案假定世界模型完全可微，未给出部分可微情形的解决框架。
- **超参数 β 缺乏自动调节机制**：β 同时控制回报的理论界和训练稳定性，论文给出的经验方案是“从小值开始逐步增加”，并非数据驱动或自动化的。
- **大型自动机的扩展性风险**：对 LDBAs 状态空间爆炸没有提供因子化或稀疏化策略，仅依赖 GPU 显存硬限制。
- **信号函数的设计依赖领域知识**：必须人工选择激活函数（如式 (3) 的 Sigmoid）并调整信号界限，否则容易出现梯度平坦或突变。
- **仅在有限任务上验证**：实验覆盖 Hopper、Cheetah、Ant、CartPole 等接触丰富的连续控制任务，对更广泛机器人学或高阶规划任务的泛化性尚未充分检验。

**开放问题**包括：

1. **混合可微系统扩展**：如何使 ∂RLs 在物理模拟可微但部分控制模块（如离散控制器）不可微的系统中工作？
2. **大规模自动机处理**：是否可以采用稀疏转移矩阵或因子化自动机表示，打破 GPU 显存对 LTL 复杂度的限制？
3. **LTL‑特定的可微 RL 算法**：能否利用自动机的合成结构（如顺序任务组成）设计特殊的探索和迁移机制，超越通用可微 RL 算法（SHAC/AHAC）的性能？
4. **经验回放与奖励塑形**：反事实经验回放或状态势函数能否与可微 LTL 奖励结合，同时不削弱规范的正确性保证？
5. **信号函数自动设计**：如何自动选择或学习激活函数（如裁剪 ReLU）来替代手工 Sigmoid，降低超参数调优难度？
6. **规范编写门槛**：如何让非逻辑专业用户安全地指定 LTL 公式，减少形式化规范设计的认知负担？
7. **与 STL/稠密奖励的联合**：是否能够吸收 STL 鲁棒性分数的稠密引导优势，同时通过自动机保持马尔可夫性和长程正确性？

总体而言，∂RLs 在“可微奖励代替离散奖励”这一瓶颈上提供了具备理论界和显著经验增益的方案，且与奖励机自然兼容，但向更一般系统、更大规模和更低使用门槛的拓展仍面临实质挑战。后续工作应着重于部分可微桥接、自动机规模控制和信号自学习，才能将这一谱系推向实际部署。



## 原文 PDF

PDF 文件：paperPDFs/ICLR_2026/Accelerated_Learning_with_Linear_Temporal_Logic_using_Differentiable_Simulation.pdf

![[paperPDFs/ICLR_2026/Accelerated_Learning_with_Linear_Temporal_Logic_using_Differentiable_Simulation.pdf]]
