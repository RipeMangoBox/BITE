---
title: Closed-loop Control of Direct Ink Writing via Reinforcement Learning
type: paper
paper_level: A
venue: SIGGRAPH
year: 2022
pdf_ref: paperPDFs/SIGGRAPH_2022/Closed_loop_Control_of_Direct_Ink_Writing_via_Reinforcement_Learning.pdf
project_link: "https://misop.github.io/projects/DirectInkReinforcementLearning/index.html"
code_link: "https://github.com/misop/Closed-Loop-Controlof-Direct-Ink-Writing-via-Reinforcement-Learning"
aliases:
- RCLDC
- CLCDIWRL
tags:
- SIGGRAPH_2022
- topic/other_unclear
core_operator: 通过在高效近似模拟中引入数据驱动的噪声模型，并利用全局特权信息设计奖励函数，使得纯仿真训练的强化学习策略能够学习到可迁移至真机的行为模式，实现对打印头速度和路径偏移动态调整。
primary_logic: 对沉积过程进行定性而非精确的数值建模是可行的，关键在于使模拟与真实环境共享行为模式，从而让强化学习发现的策略具有极小的sim-to-real差距。
claims:
- 在仿真嘈杂沉积任务中，本文策略在所有形状上均优于基线，平均偏移改善显著。
- 物理硬件实验中，本文策略在所有场景下均相对基线取得改善，且无额外训练直接部署。
- 消融研究表明，控制策略的全部组件（观察空间、动作空间、噪声模型、特权奖励）均显著提升打印过程（p < 0.01）。
- Simulated printing tasks with constant deposition (2D slices from ABC dataset) 上 Relative improvement over baseline (average offset O) = positive improvement for all test shapes
---

# Closed-loop Control of Direct Ink Writing via Reinforcement Learning

> [!tip] 核心洞察
> 对沉积过程进行定性而非精确的数值建模是可行的，关键在于使模拟与真实环境共享行为模式，从而让强化学习发现的策略具有极小的sim-to-real差距。

| 字段 | 内容 |
|------|------|
| 中文题名 | 基于强化学习的直接墨水书写闭环控制 |
| 英文题名 | Closed-loop Control of Direct Ink Writing via Reinforcement Learning |
| 会议/期刊 | SIGGRAPH 2022 |
| Links | [paper](https://misop.github.io/projects/DirectInkReinforcementLearning/index.html) · [Code](https://github.com/misop/Closed-Loop-Controlof-Direct-Ink-Writing-via-Reinforcement-Learning) · [Project](https://misop.github.io/projects/DirectInkReinforcementLearning/index.html") |
| Topic | #topic/other_unclear |
| Method | 基于强化学习的直接墨水书写闭环控制器 (RL-Closed-Loop DIW Controller) |
| Dataset | Simulated printing tasks with constant deposition, Simulated printing tasks with dynamic/noisy deposition, Simulated infill printing under noise, Physical printing tasks |

> [!tip] 效果简介
> - Simulated printing tasks with constant deposition (2D slices from ABC dataset) 上，Relative improvement over baseline (average offset O) positive improvement for all test shapes vs baseline path planning (all positive (see Fig. 6))。
> - Simulated printing tasks with dynamic/noisy deposition 上，Relative improvement over baseline (average offset O) outperformed baseline in every slice vs baseline path planning (all positive (see Fig. 7))。
> - Simulated infill printing under noise 上，Standard deviation of deposited heightfield 114 microns vs 163 microns (49 microns improvement)。

## 概要

增材制造中的直接墨水书写（DIW）面临材料特性与过程参数的随机波动，传统开环路径规划难以保证几何精度与一致性。本文提出一种基于强化学习的闭环控制框架，通过在仿真中训练策略并将其直接部署到真实硬件，实现对打印过程的动态调控。核心思路是构建一个定性的数值沉积模拟器，结合从硬件校准数据中学习的数据驱动噪声模型，使仿真环境与真实系统的行为模式对齐，从而弥合sim-to-real差距。策略网络以原位高度图、目标切片和基线路径组成的三通道局部图像为输入，输出打印头速度与路径偏移的连续控制量，并利用仿真中可用的全局信息设计特权奖励函数引导学习。实验表明，该方法在仿真噪声沉积任务中全面优于固定基线，物理打印实验在所有测试场景下均取得一致性改善，消融研究证实了速度控制、噪声模型、特权奖励等各组件的关键贡献。该方法定位为一种面向单层DIW的视觉闭环学习控制方案，为增材制造中数据驱动的过程控制提供了新范式。

## 核心方法与创新机理

### 问题瓶颈与核心思路

直接墨水书写（Direct Ink Writing, DIW）增材制造面临一个根本性瓶颈：材料特性（如粘度、颗粒分布）和过程参数（如气压、温度）的随机波动，使得传统开环路径规划无法保证一致的几何精度。物理沉积过程涉及复杂的流固耦合与长时序效应，高保真数值模拟成本过高，而直接在硬件上通过试错学习需要数以万计的打印样本，在实践中不可行。

本文的核心洞察在于：**对沉积过程进行定性而非精确的数值建模是可行的**——只要模拟环境能够与真实硬件共享行为模式，强化学习发现的策略就能以极小的sim-to-real差距迁移至真机。基于这一思想，作者构建了一个高效的近似模拟器，在其中注入从硬件校准数据中学习到的噪声模型，并利用仿真环境独有的全局信息设计奖励函数，使纯仿真训练的策略能够学习到可迁移的闭环控制行为。

### 系统框架与模块顺序

整个方法包含七个核心模块，按训练与部署流程组织如下：

1. **原位高度图获取**：通过背光光学系统将打印床的强度图像转换为局部材料高度场。
2. **观察预处理**：裁剪并对齐局部视图，生成三通道输入图像。
3. **PBD粒子沉积模拟器**：基于位置的动力学（Position-Based Dynamics）近似流体材料行为。
4. **LPC噪声生成器**：根据硬件校准数据生成流量噪声，注入模拟环境。
5. **特权奖励计算**：利用仿真中的全局沉积状态评估打印质量。
6. **PPO策略训练**：使用CNN策略网络和近端策略优化算法搜索最优控制策略。
7. **实机部署**：将训练好的策略直接应用于真实DIW打印机，无需再训练。

### 关键Changed Slots与创新机理

相较于固定路径规划的基线方法，本文在三个关键维度上进行了根本性改造：

#### Slot 1：观察空间——从全局状态到工程化的局部视图

基线方法假设已知完整的全局状态，而真实硬件只能获取局部传感器信息。本文的观察空间被设计为一个以打印喷嘴为中心的 $3.5 \times 3.5$ mm局部视窗，并堆叠为三通道图像（图3）：
- **通道1**：原位高度图，反映当前已沉积材料的空间分布；
- **通道2**：目标切片，指示期望的打印轮廓；
- **通道3**：基线路径，提供开环规划的参考轨迹。

所有通道均对齐至当前打印方向，且喷嘴正下方的遮挡区域被掩码处理。这一设计的关键在于：它迫使策略从局部观察中推断全局沉积状态，从而学习到鲁棒的闭环调整行为，而非简单记忆全局路径。推理时，该视觉策略可在4毫秒内完成评估，满足实时控制需求。

#### Slot 2：动作空间——从固定路径到速度与偏移的联合连续控制

基线方法以恒定速度沿预设路径运动，无法应对材料流量的动态变化。本文的动作空间包含两个连续控制维度：
- **打印头速度**：范围 $[0.2, 2]$ mm/s，通过调节速度控制单位路径上的材料沉积量；
- **路径偏置**：相对基线路径的横向偏移 $\pm 0.315$ mm，允许策略在材料过量时向外偏移以避免过沉积，或在材料不足时向内偏移以填补间隙。

这两个维度的联合控制构成了因果闭环：当原位观察检测到局部过沉积时，策略可同时增加速度（减少停留时间）并向外偏移（将多余材料引导至目标区域外）；反之则减速并向内偏移。消融实验证实，移除速度控制仅保留路径偏移会显著降低性能（Table 1），验证了联合控制空间的必要性。

#### Slot 3：沉积模拟——从理想恒定沉积到数据驱动的噪声注入

这是实现sim-to-real迁移的核心创新。基线方法假设恒定的材料流量和理想的沉积行为，而本文构建了一个两层模拟架构：

**底层：PBD粒子模拟器**。材料被离散为粒子，通过两个约束条件近似流体行为：
- 喷嘴碰撞约束：$C_i(\mathbf{p_i}) := (\mathbf{p_i} - \mathbf{q}_c) \cdot \mathbf{n}_c \geq 0$，确保粒子不穿透喷嘴几何；
- 密度约束（不可压缩性）：$C_i(\mathbf{p}_1, ..., \mathbf{p}_n) := \frac{\rho_i}{\rho_0} - 1 = 0$，基于SPH密度估计维持材料体积守恒。

**上层：LPC噪声生成器**。从九次硬件校准打印中测量指定位置的宽度变化（图4），使用线性预测编码（Linear Predictive Coding）拟合流量波动的时间序列模型：

$$Q_N = -\sum_{m=1}^M a_{M,m} Q_{N-m} + \epsilon_n$$

其中 $Q_N$ 为当前时刻的预测流量，$a_{M,m}$ 为LPC系数，$\epsilon_n$ 为随机噪声项。该生成模型直接驱动模拟器中喷嘴的压力参数，使仿真环境产生与真实硬件统计特性一致的流量波动。消融实验表明，移除LPC噪声模型导致策略无法适应真实硬件噪声，性能显著下降（Table 1），证实了数据驱动噪声注入是实现零样本sim-to-real迁移的关键。

### 策略学习：特权奖励与PPO训练

强化学习的奖励设计面临一个根本矛盾：真实硬件上只能获得局部观察，无法计算全局打印质量；但训练阶段需要全局信号来引导策略学习长期优化行为。本文的解决方案是**利用仿真环境独有的特权信息（privileged information）**设计奖励函数。

对于轮廓打印，奖励函数为：

$$\mathcal{R}^t = \sum_{i,j} C_{ij} \mathcal{T}_{ij} - \sum_{i,j} C_{ij} (1 - \mathcal{T})_{ij}$$

其中 $C$ 为当前沉积画布，$\mathcal{T}$ 为目标切片。第一项奖励目标区域内的沉积量，第二项惩罚目标区域外的过沉积。对于填充打印，额外增加高度标准差惩罚项：

$$\mathcal{R}^t = \sum_{i,j} C_{ij} \mathcal{T}_{ij} - \sum_{i,j} C_{ij} (1 - \mathcal{T})_{ij} - \text{std}(C_{ij} \mathcal{T}_{ij})$$

以促进均匀沉积。消融研究显示，使用局部奖励（而非全局特权奖励）训练的策略在尖锐拐角等挑战性区域性能较差（Fig. 11, Table 1），因为局部奖励无法区分“暂时偏离但最终有益”的探索行为与真正的错误。

策略网络采用CNN架构，以三通道观察图像为输入，输出速度与偏移的连续动作。训练使用近端策略优化（PPO）算法，在模拟环境中搜索最优控制策略。训练曲线（Fig. 5）显示，随着材料粘度增加，策略需要更多训练步数才能收敛，但最终均能达到稳定性能。

### 推理与部署路径

训练完成后，策略网络被直接部署到真实DIW打印机。推理时：
1. 原位视觉系统捕获当前打印床的局部高度图；
2. 观察预处理模块将其与目标切片、基线路径对齐并堆叠为三通道图像；
3. CNN策略网络前向传播（<4 ms），输出速度与偏移指令；
4. 运动控制器执行指令，调整打印头运动。

整个过程无需在线学习或参数调整，实现了从仿真到真机的零样本迁移。

![[assets/figures/papers/paper_list_l17_https_misop_github_io_projects_DirectInkReinforcementLearning_index_html_repair/figures/006_Figure_4.jpg]]
*Figure 4: We performed nine printouts and measured the width variation at specified locations. We fit the measured data with an LPC model. Please note that since our model is generative, we do not exactly match the data. Any observed resemblance is a testament to the quality of our predictor*

## 实验与关键发现

### 仿真环境下的主实验结果

本文在两类仿真场景下系统评估了所提出的闭环控制策略：恒定沉积（理想条件）和含噪沉积（模拟真实硬件波动）。评估指标为平均偏移量 $O$（式12），该指标综合了欠沉积与过沉积面积，并除以目标轮廓长度进行归一化，其值越小表示打印质量越高。所有测试形状均来自 ABC 数据集，并与训练集保持划分独立。

在恒定沉积任务中，本文策略在所有测试形状上均取得了相对于基线路径规划的正向改进（Fig. 6）。基线方法假设材料宽度恒定，采用 Clipper 库进行轮廓偏移和 Zig-Zag 填充路径生成（Johnson 2015），不具备在线调整能力。本文策略通过动态调节打印头速度和路径偏移，即使在理想条件下也能进一步减少沉积偏差。

![[assets/figures/papers/paper_list_l17_https_misop_github_io_projects_DirectInkReinforcementLearning_index_html_repair/figures/010_Figure_6.jpg]]
*Figure 6: The relative improvement of our policy over baseline in printing task with constant deposition*

在更具挑战性的含噪沉积任务中，仿真环境注入了由 LPC 模型驱动的流量噪声（Fig. 4），模拟硬件上观察到的材料宽度波动（标准差约 175 μm）。在此条件下，本文策略在每个测试切片上均优于基线（Fig. 7），且沉积直方图显示策略实现了更紧致的沉积分布控制（Fig. 8）。具体而言，在填充打印场景下，本文策略将沉积高度场的标准差从基线的 163 μm 降至 114 μm，改善了 49 μm（Fig. 9），表明策略能够有效抑制噪声环境下的过沉积和表面不平整。

![[assets/figures/papers/paper_list_l17_https_misop_github_io_projects_DirectInkReinforcementLearning_index_html_repair/figures/008_Figure_7.jpg]]
*Figure 7: The relative improvement of our policy over baseline in printing task with noisy deposition*

![[assets/figures/papers/paper_list_l17_https_misop_github_io_projects_DirectInkReinforcementLearning_index_html_repair/figures/009_Figure_8.jpg]]
*Figure 8: Deposition histograms for two exemplar slices from our dataset. Even in challenging, noisy environments, our control policy achieves tighter control over the deposition process*

![[assets/figures/papers/paper_list_l17_https_misop_github_io_projects_DirectInkReinforcementLearning_index_html_repair/figures/011_Figure_9.jpg]]
*Figure 9: In a noisy environment, the baseline printing policy (left) significantly over-deposits and produces a bulging surface. In contrast, our policy (right) has almost no over-deposition and creates a uniform surface*

### 物理硬件实验验证

物理实验在定制 DIW 平台上进行，使用低粘度和高粘度两种材料，策略完全在仿真中训练后直接部署至真机，未进行任何在线微调。在所有测试场景下，本文策略均相对于基线取得了一致的改进（Fig. 13）。沉积质量估计结果进一步表明，学习到的策略在真实硬件上能够复现仿真中观察到的行为模式（Fig. 14），验证了所提 sim-to-real 迁移策略的有效性。

值得注意的是，策略推理时间小于 4 毫秒，满足实时闭环控制的需求，不会成为打印过程的瓶颈。

### 消融研究

为量化各组件对系统性能的贡献，本文进行了系统的消融实验（Table 1），所有对比均在含噪仿真环境下进行，统计显著性水平为 p < 0.01。

![[assets/figures/papers/paper_list_l17_https_misop_github_io_projects_DirectInkReinforcementLearning_index_html_repair/figures/014_Table_1.jpg]]
*Table 1: Average improvements of controllers from our ablation studies*

**动作空间的必要性。** 移除速度控制、仅保留路径偏移的策略在性能上显著下降。全动作空间（速度 [0.2, 2] mm/s + 偏移 ±0.315 mm）使策略能够同时应对快速和大幅度的材料偏差：速度调节应对瞬时流量波动，路径偏移补偿持续性的沉积偏差（Fig. 10）。两者协同作用对于在尖锐拐角和高曲率区域保持精确沉积至关重要。

**LPC 噪声模型的关键作用。** 移除 LPC 噪声生成器后，策略在纯确定性仿真中训练，虽能在仿真中取得良好表现，但部署到含噪环境（或真实硬件）时性能严重退化。LPC 模型通过拟合硬件校准数据（9 次打印样件的宽度测量，Fig. 4）捕获了真实材料流动的时序相关性，使仿真与真实环境共享行为模式，这是实现有效 sim-to-real 迁移的核心机制。

**特权奖励函数的贡献。** 将全局特权奖励替换为局部基于视窗的奖励后，训练出的策略在挑战性区域（如尖锐拐角、窄通道）表现明显较差（Fig. 11）。全局奖励（式10-11）利用仿真中专有的完整沉积状态信息，为策略提供了关于长期沉积质量的密集反馈信号，有助于策略学习到具有前瞻性的控制行为——例如在接近拐角时提前减速以避免过沉积。局部奖励因缺乏全局上下文，难以引导策略形成此类行为。

### 泛化性与边界条件

本文进一步评估了策略对材料粘度变化的鲁棒性（Fig. 12）。结果表明，针对特定粘度训练的控制器在粘度偏离训练条件时性能逐渐下降，揭示了当前方法的第一个关键边界：策略不具备对材料特性的在线辨识与自适应能力。在实际应用中，若材料批次间存在显著差异，可能需要重新校准 LPC 模型并重新训练策略。

第二个重要边界是当前框架仅针对单层打印进行设计与验证。多层三维打印涉及层间堆积、已沉积层的变形以及误差的跨层传播，这些效应在当前仿真模型和奖励设计中均未被考虑。因此，将方法直接扩展到多层场景需要重新设计状态表示、过渡模型和奖励函数。

第三个适用边界在于硬件依赖性。原位高度图获取依赖背光光学系统，LPC 噪声模型需要针对特定硬件平台和材料进行预校准打印。迁移到不同类型的 DIW 打印机或更换材料时，需重新执行校准流程，目前尚无法实现即插即用。

### 失败模式分析

在物理实验中观察到的残余误差主要来源于两方面。其一，LPC 模型虽能捕获材料波动的主要统计特征，但作为线性预测模型，无法完全复现真实材料的非线性行为（如剪切变稀效应导致的瞬时流量突变）。其二，中心遮挡区域的存在使策略无法直接观测喷嘴正下方的沉积状态，在极端情况下（如材料突然断流或过量挤出）可能导致响应延迟。这些失败模式表明，当前方法在材料行为高度非线性或需要亚毫米级精度的应用中仍有改进空间。

## 定位与知识库关联

本文的核心贡献在于改变了增材制造控制管线中的一个关键槽位：**从开环的固定路径规划转向基于视觉的闭环强化学习控制**。基线方法（Clipper 路径偏移与 Zig-Zag 填充，Johnson 2015）假设材料沉积宽度恒定，完全依赖离线规划的固定路径和速度，缺乏对材料特性波动和过程噪声的在线响应能力。本文在该槽位中嵌入了一个 CNN 策略网络，使用 PPO 在定制仿真环境中训练，直接输出打印头速度和路径偏移的连续控制信号，从而实现了对沉积过程的实时动态调节。

**相对已有方法的本质差异体现在三个层面：**

1. **控制范式转换**：传统 DIW 控制依赖精确的物理建模或离线路径规划，而本文证明，通过在仿真中引入数据驱动的噪声模型（LPC 拟合硬件流量波动）并利用仿真专属的全局特权信息设计奖励函数，可以在纯仿真环境中学习到可迁移至真机的控制策略。这种“定性仿真 + sim-to-real 迁移”的范式，与需要高保真物理模拟或大量真机交互样本的现有方法形成根本区别。

2. **观察空间设计**：不同于使用完整状态观测或原始相机图像的方法，本文设计了工程化的三通道局部视图（原位高度图、目标切片、基线路径），对齐至打印方向并遮挡中心区域。这种紧凑的局部表示使策略能够在 4 毫秒内完成推理，满足实时控制需求，同时降低了状态空间的维度。

3. **噪声建模与奖励设计**：LPC 噪声模型将硬件校准数据转化为可注入仿真的生成式压力波动，弥合了 sim-to-real 差距；特权奖励函数利用仿真中可访问的全局沉积状态计算轮廓精度和填充均匀性，引导策略学习到长时域有效的控制行为。这两项设计共同构成了方法可行性的关键支撑。

**知识库挂载点：**

- **物理仿真与强化学习**：本文可挂载至“基于学习的制造控制”节点，与利用深度强化学习进行机器人操作（如 dexterous manipulation）的工作形成交叉。其核心启示在于：对于物理过程复杂、高保真模拟昂贵的系统，定性建模 + 噪声注入 + 特权信息奖励的组合可以有效降低 sim-to-real 迁移难度。
- **增材制造过程控制**：与熔融沉积成型（FDM）中的实时监控与参数调整方法（如基于视觉的缺陷检测与反馈）形成互补。本文的方法论可推广至其他需要动态调节工艺参数的增材制造场景，但需针对具体工艺重新设计观察空间和噪声模型。
- **sim-to-real 迁移**：本文的迁移策略属于“域随机化”的一种变体——通过在仿真中注入从硬件数据拟合的噪声分布，使策略对真实噪声具有鲁棒性。这与基于系统辨识的域适应方法（如学习逆向动力学模型）形成对比，可挂载至 sim-to-real 迁移方法的分类体系中。

**适用边界与限制：**

1. **仅验证单层打印**：当前方法针对二维切片进行训练和评估，未涉及多层堆积、层间粘附、误差累积等三维打印特有挑战。扩展到多层场景需要重新设计状态表示和奖励函数，以考虑层间一致性。

2. **硬件与材料依赖性**：观察系统依赖背光光学高度估计，LPC 噪声模型需针对特定硬件和材料组合进行预校准。更换打印机、喷嘴或材料时需重新采集校准数据并拟合噪声模型，流程尚未自动化。

3. **无在线自适应能力**：策略在训练时针对固定材料特性（如粘度）进行优化，缺乏对材料批次间波动或打印过程中特性变化的在线识别与策略切换机制。这限制了其在材料特性时变场景下的鲁棒性。

4. **奖励函数不可直接部署**：特权奖励依赖仿真中的全局沉积信息，在真实硬件上无法直接计算相同奖励，因此无法在部署后继续在线优化策略。

**后续工作启发：**

- **多层扩展**：将当前框架推广至三维零件打印，需解决层间状态传递、误差补偿和支撑结构打印等新问题。可考虑引入三维卷积或图神经网络处理多层高度场。
- **材料特性在线辨识**：开发从原位视图中自动估计材料粘度或流动特性的模块，实现策略的动态切换或连续参数化控制，提升对材料波动的适应能力。
- **无校准部署**：探索通过元学习或在线域适应减少对预校准的依赖，使策略能在少量试打印后快速适应新硬件或新材料。
- **跨工艺迁移**：验证该方法在 FDM、激光粉末床熔融等其他增材制造工艺中的适用性，需针对各工艺的物理特性重新设计仿真器和观察空间。

## 原文 PDF

![[paperPDFs/SIGGRAPH_2022/Closed_loop_Control_of_Direct_Ink_Writing_via_Reinforcement_Learning.pdf]]