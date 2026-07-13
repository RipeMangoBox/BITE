---
title: "VIRAL: Visual Sim-to-Real at Scale for Humanoid Loco-Manipulation"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/VIRAL_Visual_Sim_to_Real_at_Scale_for_Humanoid_Loco_Manipulation.pdf
project_link: "https://viral-humanoid.github.io"
code_link: null
aliases:
- VIRAL
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/representation_self_supervised_transfer
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: 通过大规模模拟训练，结合视觉域随机化、系统识别和特权教师-视觉学生蒸馏范式，VIRAL成功将仿真中学习的策略零样本迁移至真实人形机器人，解锁了持续移动操作的能力。关键要素包括：delta动作空间、参考状态初始化、DAgger-BC混合蒸馏以及大规模GPU并行训练。
primary_logic: 在仿真中训练一个具有完全状态信息的特权RL教师策略，然后通过大规模视觉随机化与分布式训练，将其蒸馏为一个仅依赖RGB和本体感觉的学生策略，可在无需任何真实世界微调的情况下，使人形机器人连续完成54个循环的移动操作任务，性能接近甚至超越人类专家遥操作。
claims:
- VIRAL在59次真实世界连续试验中成功54次（成功率91.5%），远超非专家遥操作（73%）
- 仅使用8-16个GPU训练教师策略，成功率可达90%以上，而1-2个GPU则无法达到高成功率
- 关闭所有视觉域随机化后，策略性能下降35.1%（标准化成功率降至0.649）
- 参考状态初始化对于教师策略至关重要：缺少该策略时成功率低于10%，加入后接近95%
---

# VIRAL: Visual Sim-to-Real at Scale for Humanoid Loco-Manipulation

> [!tip] 核心洞察
> 在仿真中训练一个具有完全状态信息的特权RL教师策略，然后通过大规模视觉随机化与分布式训练，将其蒸馏为一个仅依赖RGB和本体感觉的学生策略，可在无需任何真实世界微调的情况下，使人形机器人连续完成54个循环的移动操作任务，性能接近甚至超越人类专家遥操作。

| 字段 | 内容 |
|------|------|
| 中文题名 | VIRAL：大规模视觉Sim-to-Real人形机器人移动操作 |
| 英文题名 | VIRAL: Visual Sim-to-Real at Scale for Humanoid Loco-Manipulation |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2511.15200) · [Project](https://viral-humanoid.github.io) |
| Topic | #topic/vision_multimodal_applications #topic/representation_self_supervised_transfer #topic/vision_multimodal_applications/image_and_video_generation |
| Method | VIRAL |
| Dataset | Real-world loco-manipulation, Simulation teacher training, Sim-to-real transfer with domain randomization, Teacher training at scale |

> [!tip] 效果简介
> - Real-world loco-manipulation (walking, placing, grasping, turning) 上，Success rate 91.5% (54/59 trials) vs 73% (non-expert teleoperator) (+18.5%)。
> - Real-world loco-manipulation 上，Cycle time 20.2 s vs 21.4 s (expert teleoperator) (-1.2 s (faster))。
> - Simulation teacher training 上，Success rate ~95% (VIRAL with RSI + delta action) vs <10% (no reference state initialization) (>85%)。

## 概要

人形机器人要在真实世界中实现完全自主的移动操作，必须解决一个根本性瓶颈：如何从机载RGB视觉出发，可靠地完成“边行走边操作”的长时程任务。现有系统要么依赖盲态运动、静态桌面操作，要么需要人类遥操作，始终无法跨越视觉sim-to-real的迁移鸿沟。**VIRAL**（Visual Sim-to-Real at Scale for Humanoid Loco-Manipulation）正是针对这一瓶颈提出的大规模视觉sim-to-real框架。

VIRAL的核心洞察是：在仿真中先训练一个拥有完全状态信息的特权强化学习教师策略，再通过大规模视觉域随机化与分布式训练，将其蒸馏为一个仅依赖RGB和本体感觉的学生策略。这一“特权教师-视觉学生”蒸馏范式，使人形机器人在**无需任何真实世界微调**的条件下，连续完成54个循环的移动操作任务，成功率高达**91.5%**，不仅远超非专家遥操作（73%），甚至比专家遥操作更快（20.2 s vs 21.4 s）。

该方法的关键设计要素包括：
- **Delta动作空间**：教师策略输出相对于底层WBC控制器（HOMIE）的增量指令，而非绝对关节目标，这是任务成功的必要条件。
- **参考状态初始化**：从200条遥操作演示中构建状态缓冲区，使RL训练从有意义的初始状态开始，将成功率从不足10%提升至约95%。
- **DAgger-BC混合蒸馏**：以α=0.5的比例混合在线DAgger与行为克隆，显著优于纯BC蒸馏。
- **大规模视觉域随机化**：覆盖光照、材质、相机外参、图像质量与传感器延迟，关闭全部随机化后标准化成功率下降35.1%。
- **计算规模扩展**：教师训练需8-16个GPU才能达到>90%的成功率，学生训练扩展至64个GPU可加速收敛并提升最终性能。

在方法谱系上，VIRAL位于**视觉sim-to-real强化学习**与**人形全身控制**的交汇点。其底层依赖**HOMIE**作为预训练的全身控制策略，上层则通过分布式仿真系统（基于TRL与Accelerate）实现大规模并行训练。与纯盲态运动或静态操作方案不同，VIRAL首次在单一RGB策略中统一了行走、抓取、放置与转向等子任务，并展现出对托盘位置、物体类别、桌面高度、光照条件等变量的强泛化能力。

尽管成果显著，VIRAL仍面临若干限制：模拟器难以精确建模流体、可变形体等复杂物理交互；训练任务依赖人工设计，缺乏自动生成多样化场景的能力；手工奖励函数存在被策略利用的风险；数十个GPU的计算需求也限制了中小型实验室的复现可能。这些限制同时也指明了未来的研究方向——如何降低物理建模成本、自动化任务生成、设计更鲁棒的奖励函数，以及探索算力效率的甜蜜点。

人形机器人因其类人形态，具备在人类环境中执行复杂移动操作任务的潜力。然而，让一个全尺寸人形机器人在真实世界中仅凭机载RGB视觉自主完成长时程的移动操作——例如在桌子之间行走、抓取物体、转身放置——至今仍是一个未解决的系统性挑战。

现有方法的缺口集中在三个层面。**第一，视觉sim-to-real迁移差距巨大。** 仿真中训练的策略在面向真实世界的视觉感知、光照变化、相机噪声和物理接触时，往往出现灾难性退化。多数成功的人形机器人系统要么回避视觉输入，依赖盲态运动规划；要么将操作限定在静态桌面上，回避移动与操作的耦合。**第二，长时程任务中的误差累积难以控制。** 移动操作涉及行走、抓取、放置、转身等多个子任务的顺序衔接，任何环节的微小偏差都会在数十个循环中放大，导致任务链断裂。**第三，训练计算规模不足。** 视觉策略的泛化能力高度依赖于训练时的视觉多样性，而大规模并行仿真渲染对计算资源的要求远超单GPU所能提供的上限，这限制了中小型实验室对视觉sim-to-real范式的探索。

VIRAL正是在这一背景下提出的。其核心动机是验证一个假设：**通过在仿真中大规模扩展视觉域随机化、系统识别对齐和分布式训练，可以训练出一个仅依赖RGB和本体感觉的视觉策略，使其零样本迁移至真实人形机器人，并可靠地执行数十个循环的连续移动操作。** 这一假设的成立与否，直接关系到人形机器人能否从实验室演示走向实际部署。

## 核心方法与创新机理

VIRAL 的核心创新在于构建了一套从仿真中训练、零样本迁移至真实人形机器人的视觉移动操作框架。其关键突破并非单一技术点，而是通过多个 **changed slots** 的系统性组合，解决了视觉 sim-to-real 迁移中的误差累积与训练规模瓶颈。以下聚焦相对 baseline 的关键创新要素。

### 1. 特权教师-视觉学生蒸馏范式

VIRAL 采用教师-学生框架（Figure 2），将仿真中可获取的完全状态信息与真实世界中仅有的 RGB 视觉和本体感觉解耦：

- **Phase 1**：在仿真中训练一个特权 RL 教师策略，该策略接收完全的本体感知与外感知信息（包括物体精确位姿、机器人全状态等），输出 WBC 命令。教师策略使用 PPO 训练，并采用 **delta 动作空间** 和 **参考状态初始化** 两个关键设计。
- **Phase 2**：通过 DAgger 与行为克隆的混合蒸馏（α=0.5），将教师策略的知识迁移到仅依赖 108×192 RGB 图像和 sim-to-real 本体感觉的学生策略。蒸馏损失为教师与学生动作之间的 MSE：

$$
\mathscr{L}_{\mathrm{distill}} = \mathbb{E}_{o_t \sim \rho^{o}} \left[ \left\| \pi_{\mathrm{teacher}}(o_t^{\mathrm{teacher}}) - \pi_{\mathrm{student}}(o_t^{\mathrm{student}}) \right\|_2^2 \right]
$$

其中观测分布为教师与学生分布的混合：$\rho^{o} \triangleq \alpha \rho_{\pi_{\mathrm{teacher}}}^{o} + (1 - \alpha) \rho_{\pi_{\mathrm{student}}}^{o}$。

**证据强度**：消融实验（Figure 11）表明，纯 BC 蒸馏在真实世界部署成功率上明显低于 DAgger-BC 混合（α=0.5），后者是 VIRAL 的默认选择。

### 2. Delta 动作空间：人形移动操作的关键表征

传统方法通常使用绝对关节目标作为动作空间，但 VIRAL 发现这对人形移动操作无效。VIRAL 改用 **delta 动作空间**，即输出 WBC 命令的增量：

$$
a_t = (\Delta \mathbf{v}_t, \Delta \omega_t^{\mathrm{yaw}}, \Delta \mathbf{q}_t^{\mathrm{arm}}, \Delta \mathbf{q}_t^{\mathrm{finger}})
$$

这一设计使得策略只需学习相对调整量，而非绝对目标值，显著降低了学习难度。

**证据强度**：Figure 9 的消融实验显示，使用绝对动作空间的教师策略无法达到高成功率，而 delta 动作空间的教师策略成功率接近 95%。这是 VIRAL 成功的关键 changed slot 之一。

### 3. 参考状态初始化：破解长时程 RL 探索难题

长时程移动操作任务的 RL 训练面临严重的探索挑战——随机初始化的机器人几乎不可能偶然完成任务。VIRAL 通过收集 200 条遥操作仿真演示（Figure 4），构建参考状态初始化缓冲区，在训练中从这些有意义的状态开始 episode，而非从零开始。

**证据强度**：Figure 9 显示，取消参考状态初始化后，教师策略成功率从约 95% 骤降至 10% 以下，证明该设计对 RL 训练至关重要。

### 4. 大规模视觉域随机化与系统识别

VIRAL 的 sim-to-real 迁移依赖两个互补机制：

- **视觉域随机化**（Figure 3）：在训练中随机化光照、材质、相机外参、图像质量、传感器延迟等，使视觉学生策略学会对视觉变化保持鲁棒。
- **系统识别**：对灵巧手进行 SysID（Figure 5），校准手指执行器参数以对齐仿真与真实的关节轨迹；对相机外参进行 real-to-sim 对齐（Figure 6），使仿真视角匹配真实机器人相机。

**证据强度**：Figure 13 显示，关闭所有视觉域随机化后，标准化成功率下降 35.1%（降至 0.649），单独关闭任何一项（材质、光照、相机外参）均导致性能下降。

### 5. 计算规模：解锁高性能的隐藏要素

VIRAL 揭示了一个常被忽视的维度——**训练计算规模**对视觉 sim-to-real 的决定性影响：

- **教师训练**（Figure 14）：1-2 个 GPU 无法达到高成功率，8-16 个 GPU 的分布式并行环境训练才能获得 >90% 的成功率。
- **学生训练**（Figure 15）：将学生蒸馏扩展到 64 个 GPU 可显著加快收敛速度、提高训练稳定性并最终提升性能。

**证据强度**：Figure 14 和 Figure 15 分别展示了教师和学生训练的计算扩展曲线，提供了清晰的 scaling 证据。

### 创新总结

VIRAL 的创新本质上是 **delta 动作空间 + 参考状态初始化 + DAgger-BC 混合蒸馏 + 大规模视觉域随机化 + 系统识别 + 大规模并行训练** 的系统性组合。单独看每个组件可能并非全新，但它们在人形移动操作场景下的集成与规模化应用，使得零样本 sim-to-real 的连续 54 循环移动操作成为可能——这一结果在现有 baseline 中未见报道。

VIRAL 采用**特权教师-视觉学生**两阶段蒸馏范式，将仿真中训练的全状态策略零样本迁移至真实人形机器人，实现基于机载 RGB 视觉的连续移动操作。

### 两阶段流水线

**第一阶段：特权 RL 教师训练。** 在仿真中，教师策略接收完整的特权观测——包括精确的机器人本体感觉（所有关节位置、速度、基座线速度/角速度等，见 Table 1）和任务外部状态（物体位姿、目标位置等）。教师策略输出 **delta 动作空间**的 WBC 命令 $a_t = (\Delta \mathbf{v}_t, \Delta \omega_t^{\mathrm{yaw}}, \Delta \mathbf{q}_t^{\mathrm{arm}}, \Delta \mathbf{q}_t^{\mathrm{finger}})$，由底层 **HOMIE** 全身控制器转换为关节力矩。教师通过 PPO 强化学习训练，其奖励函数按任务阶段（行走、抓取、放置、转向等）加权组合，如行走奖励 $r_{\mathrm{walk}} = \exp(-4(\|p_{\mathrm{robot}} - p_{\mathrm{GraspObj}}\| - 0.45)^2)$ 和放置奖励 $r_{\mathrm{place}} = -\|\mathbf{f}_{\mathrm{PlaceObj}}\| * (\|p_{\mathrm{PlaceObj}} - p_{\mathrm{tray}}\| < 0.3)$（完整公式见 Table 3）。训练采用 **参考状态初始化**（从 200 条遥操作演示中采样初始状态，Figure 4），使教师策略能够从任务中途的多样状态开始探索，避免从零开始探索的困难（消融显示缺少此策略时成功率从约 95% 骤降至 10% 以下，Figure 9）。

**第二阶段：视觉学生蒸馏。** 学生策略仅接收 **108×192 RGB 图像**和 sim-to-real 本体感觉（Table 2），通过模仿教师策略学习移动操作。蒸馏采用 **DAgger-BC 混合策略**：以比例 $\alpha = 0.5$ 混合教师观测分布和学生自滚动观测分布 $\rho^{o} \triangleq \alpha \rho_{\pi_{\mathrm{teacher}}}^{o} + (1 - \alpha) \rho_{\pi_{\mathrm{student}}}^{o}$，最小化教师-学生动作间的 MSE 损失 $\mathscr{L}_{\mathrm{distill}} = \mathbb{E}_{o_t \sim \rho^{o}} [ \| \pi_{\mathrm{teacher}}(o_t^{\mathrm{teacher}}) - \pi_{\mathrm{student}}(o_t^{\mathrm{student}}) \|_2^2 ]$。纯 BC 蒸馏在真实世界部署时性能显著劣于 DAgger-BC 混合（Figure 11），表明在线纠错对缩小分布偏移至关重要。

### Sim-to-Real 迁移关键模块

VIRAL 通过三个核心模块弥合仿真到现实的鸿沟：

1. **大规模视觉域随机化**（Figure 3, Table 7）：在训练中随机化光照强度/色温/方向、物体材质纹理、相机内外参、图像质量（模糊/噪声/对比度）以及传感器延迟。消融实验表明，关闭所有视觉随机化后标准化成功率下降 35.1%（Figure 13），单独关闭任何一项均导致性能退化。

2. **灵巧手系统辨识**（Figure 5）：通过执行真实世界的抓取-释放原语并在仿真中重放相同动作序列，优化手指关节的 armature、刚度和阻尼参数，使仿真关节轨迹与真实测量高度对齐。

3. **相机外参标定**（Figure 6）：将真实机器人头部相机视角与仿真相机对齐，确保学生策略在真实环境中看到的视觉输入与训练分布一致。

### 分布式训练系统

教师训练使用 8-16 个 GPU 的并行仿真环境，实验表明 1-2 个 GPU 无法使策略达到高成功率，而 8-16 个 GPU 可实现 90% 以上的渐近成功率（Figure 14）。学生蒸馏进一步扩展到 64 个 GPU，基于定制版 TRL 和 HuggingFace Accelerate 实现多节点并行渲染，大幅加快收敛速度并提升训练稳定性（Figure 15）。

![[assets/figures/papers/paper_list_l1040_https_arxiv_org_abs_2511_15200/figures/002_Figure_2.jpg]]
*Figure 2: VIRAL teacher-student pipeline. Phase 1: In simulation, a privileged RL teacher policy*

VIRAL 采用“特权教师–视觉学生”两阶段蒸馏框架，其核心模块与公式设计围绕长时程移动操作的奖励塑形、动作空间表示以及教师到学生的分布匹配展开。

### 特权教师策略的训练要素

教师策略在仿真中接收完整状态信息，输出增量式 WBC 指令。其关键设计包括：

- **Delta 动作空间**：教师策略输出增量命令 $a_t = (\Delta \mathbf{v}_t, \Delta \omega_t^{\mathrm{yaw}}, \Delta \mathbf{q}_t^{\mathrm{arm}}, \Delta \mathbf{q}_t^{\mathrm{finger}})$，作为底层 WBC 控制器 **HOMIE** 的输入。消融实验表明，delta 动作空间是人形移动操作成功的关键，绝对动作空间变体无法达到高成功率（Figure 9）。
- **参考状态初始化（RSI）**：从 200 条遥操作仿真演示中构建状态初始化缓冲区，用于 RL 训练中的 episode 重置。缺少 RSI 时教师成功率低于 10%，加入后接近 95%（Figure 9）。

![[assets/figures/papers/paper_list_l1040_https_arxiv_org_abs_2511_15200/figures/009_Figure_9.jpg]]
*Figure 9: Ablations of teacher policy training. Training rewards (left) and success rates (right) for the full method (RSI + delta action), without demonstration resets, and without delta action space, showing that both components are critical for final success*

### 分阶段奖励函数

任务被分解为五个阶段（行走、抓取、提升、放置、转向），每个阶段有独立的奖励组件。总奖励为各阶段奖励的加权和：

$$r_t = \sum_{i=0}^{4} w_i \mathbb{1}[s_t = i] r_t^{(i)}, \qquad w_i > 0$$

其中 $s_t$ 为当前阶段指示器，$\mathbb{1}[\cdot]$ 为示性函数。

各阶段核心奖励公式如下：

- **行走奖励**：鼓励机器人向抓取目标物体靠近。

$$r_{\mathrm{walk}} = \exp(-4(\|p_{\mathrm{robot}} - p_{\mathrm{GraspObj}}\| - 0.45)^2)$$

- **抓取高度奖励**：鼓励将物体提升到桌面以上。

$$r_{\mathrm{grasp-z}} = \min(h_{\mathrm{GraspObj}} - h_{\mathrm{table}}, 0.15)$$

- **抓取目标奖励**：鼓励将物体移动到目标位置。

$$r_{\mathrm{grasp-goal}} = \exp(-10\|p_{\mathrm{GraspObj}} - p_{\mathrm{goal}}\|^2)$$

- **放置奖励**：当物体靠近托盘时鼓励放置。

$$r_{\mathrm{place}} = -\|\mathbf{f}_{\mathrm{PlaceObj}}\| \cdot (\|p_{\mathrm{PlaceObj}} - p_{\mathrm{tray}}\| < 0.3)$$

- **转向奖励**：鼓励机器人朝向目标偏航角。

$$r_{\mathrm{turn}} = -|\mathbf{y}_{\mathrm{robot}} - \mathbf{y}_{\mathrm{desired}}|$$

### 视觉学生策略的蒸馏损失

学生策略仅依赖 RGB 图像和本体感觉，通过 DAgger 与行为克隆（BC）的混合方式进行蒸馏。核心机制为观测分布混合：

$$\rho^{o} \triangleq \alpha \rho_{\pi_{\mathrm{teacher}}}^{o} + (1 - \alpha) \rho_{\pi_{\mathrm{student}}}^{o}$$

其中 $\alpha$ 为教师观测分布的比例。蒸馏损失采用教师与学生动作之间的 MSE：

$$\mathscr{L}_{\mathrm{distill}} = \mathbb{E}_{o_t \sim \rho^{o}} \left[ \left\| \pi_{\mathrm{teacher}}(o_t^{\mathrm{teacher}}) - \pi_{\mathrm{student}}(o_t^{\mathrm{student}}) \right\|_2^2 \right]$$

消融实验表明，采用 $\alpha = 0.5$ 的 DAgger-BC 混合蒸馏比纯 BC 获得明显更高的真实世界部署成功率（Figure 11）。

![[assets/figures/papers/paper_list_l1040_https_arxiv_org_abs_2511_15200/figures/012_Figure_11.jpg]]
*Figure 11: Ablation of ratio of DAgger/BC of student policy*

### Sim-to-Real 迁移的支撑模块

除策略训练外，VIRAL 依赖两个关键的 sim-to-real 对齐模块：

- **灵巧手系统辨识**：通过回放真实世界的抓取–释放基元动作序列，在仿真中优化手指骨架、刚度和阻尼参数，使仿真关节轨迹与真实测量高度对齐（Figure 5）。
- **相机外参标定**：将真实机器人相机视角与仿真相机对齐，缩小视觉观测的域差距（Figure 6）。
- **视觉域随机化**：在训练中对光照、材质、相机外参、图像质量和传感器延迟进行大规模随机化。关闭所有随机化后策略性能下降 35.1%（标准化成功率降至 0.649），证明其对于 sim-to-real 迁移至关重要（Figure 13）。

### 分布式训练系统

学生策略的视觉训练通过定制版 TRL 结合 HuggingFace Accelerate 实现多 GPU 扩展。将学生训练从 1 个 GPU 扩展到 64 个 GPU 可显著加快收敛速度、提高训练稳定性并最终提升性能（Figure 15）。教师策略从 1-2 个 GPU 扩展到 8-16 个 GPU 同样是达到 90% 以上成功率的必要条件（Figure 14）。

## 实验与关键发现

### 真实世界部署：连续移动操作的可靠性边界

VIRAL 在真实世界中的核心验证是在 Unitree G1 人形机器人上进行的连续移动操作循环测试。每个循环包含“行走至抓取桌→抓取物体→行走至放置桌→放置物体→转身回到起始位置”五个阶段。在 59 次连续试验中，VIRAL 基于 RGB 的策略成功完成 54 次，成功率 **91.5%**，平均循环时间 **20.2 秒**。作为对照，人类专家遥操作（使用相同的底层 HOMIE WBC 策略）成功率为 100%，但平均循环时间更慢（21.4 秒）；非专家遥操作成功率仅为 73%，且执行速度更慢（Figure 7）。

![[assets/figures/papers/paper_list_l1040_https_arxiv_org_abs_2511_15200/figures/005_Figure_7.jpg]]
*Figure 7: Real-world performance comparison: VIRAL matches expert-level reliability, outperforms non-experts, and operates faster than the expert teleoperator*

这一结果揭示了两个关键信号：其一，VIRAL 的策略可靠性已逼近专家水平，远超非专家遥操作；其二，策略执行速度甚至快于人类专家，表明其动作决策具有高度的时间效率。所有试验均未进行任何真实世界微调，策略完全在仿真中训练后零样本部署。

### 泛化能力：空间、外观与物体的鲁棒性

VIRAL 在多种真实世界扰动下展现出鲁棒的泛化能力（Figure 8）。具体包括：
- **空间扰动**：托盘和物体的位置变化、机器人起始位姿变化、桌面高度和类型变化；
- **外观扰动**：桌布颜色变化、光照条件变化；
- **物体泛化**：在不同于训练物体的类别上进行抓取。

这些泛化能力来源于大规模视觉域随机化训练（Figure 3, Table 7），涵盖图像质量、光照、材质、相机外参和传感器延迟等维度。值得注意的是，多物体训练在 10 种不同物体上的归一化成功率全面优于仅用圆柱体训练的单物体策略（Figure 16），表明物体多样性对泛化能力至关重要。

![[assets/figures/papers/paper_list_l1040_https_arxiv_org_abs_2511_15200/figures/016_Figure_16.jpg]]
*Figure 16: Ablation of object generalization of teacher policy*

### 核心消融：方法组件的因果贡献

#### 教师策略的关键设计

**参考状态初始化（RSI）** 是教师策略成功的必要条件。消融实验（Figure 9）表明，取消基于 200 条遥操作演示的状态重置后，教师策略成功率从约 95% 骤降至 10% 以下。RSI 解决了长时程 RL 训练中的探索困难问题——通过将 episode 重置到有意义的中间状态，策略无需从零开始探索整个任务空间。

**Delta 动作空间** 同样不可或缺。绝对动作空间（直接输出关节目标位置）的教师策略无法达到高成功率（Figure 9）。Delta 动作空间输出 WBC 命令的增量（$\Delta \mathbf{v}_t, \Delta \omega_t^{\mathrm{yaw}}, \Delta \mathbf{q}_t^{\mathrm{arm}}, \Delta \mathbf{q}_t^{\mathrm{finger}}$），为策略提供了更稳定的控制接口，避免了绝对位置输出在长时程任务中的累积误差。

#### 学生蒸馏策略的选择

DAgger-BC 混合比例对真实世界部署性能有显著影响（Figure 11）。纯行为克隆（BC, $\alpha=0$）虽然优化收敛更快，但部署成功率较低；引入学生在线 rollout（$\alpha=0.5$）略微减慢优化速度，但显著提升了部署成功率。这一现象符合 DAgger 的经典理论——在线交互使策略接触到自身诱导的分布偏移，从而提高了闭环鲁棒性。

#### 视觉域随机化的不可替代性

视觉域随机化的消融（Figure 13）揭示了每个组件的独立贡献：
- 单独关闭材质随机化、光照随机化或相机外参随机化均导致性能下降；
- 关闭所有视觉随机化后，归一化成功率降至 0.649，性能下降 **35.1%**。

![[assets/figures/papers/paper_list_l1040_https_arxiv_org_abs_2511_15200/figures/011_Figure_13.jpg]]
*Figure 13: Ablation of visual randomization*

这一结果证实了大规模视觉域随机化对于弥合 sim-to-real 视觉差距的核心作用。值得注意的是，VIRAL 的域随机化并非简单的颜色抖动，而是涵盖图像质量退化、材质属性变化、相机内外参扰动和传感器延迟等多个物理层面（Table 7）。

#### 历史架构与视觉骨干

学生策略的历史架构消融（Figure 12）和视觉骨干消融（Figure 10）进一步优化了策略设计。具体结论需参照原文图表确认，但验证分析表明这些架构选择对最终性能有可测量的影响。

### 计算规模：从“可行”到“可靠”的相变

VIRAL 的规模分析揭示了计算量对性能的非线性影响，这是该工作最具启示性的发现之一。

**教师训练**（Figure 14）：使用 1-2 个 GPU 训练时，教师策略的性能处于低水平平台期，无法可靠解决任务。将 GPU 数量扩展到 8-16 个后，策略不仅收敛更快，且渐近成功率跃升至 90% 以上。这一“相变”现象表明，人形移动操作任务存在一个计算阈值，低于该阈值时 RL 探索无法有效覆盖任务空间。

**学生训练**（Figure 15）：将视觉学生策略的训练从 1 个 GPU 扩展到 64 个 GPU，蒸馏损失收敛速度显著加快，优化动力学更加平滑，最终性能更高。这凸显了大规模并行仿真对于视觉策略学习的必要性——每个 GPU 渲染不同的视觉随机化场景，使策略暴露于更丰富的视觉分布中。

### 系统识别与标定：缩小物理差距

VIRAL 的 sim-to-real 迁移不仅依赖视觉随机化，还包括两项关键的物理对齐（Section 2.3）：

**灵巧手系统辨识**（Figure 5）：通过在真实世界执行“抓取-释放”原语并在仿真中回放相同动作序列，对灵巧手的手指骨架、刚度和阻尼参数进行系统辨识。辨识后，仿真与真实的关节轨迹高度对齐，为精确抓取提供了物理基础。

**相机外参标定**（Figure 6）：将真实机器人相机的视角与仿真相机对齐，使策略在仿真中观察到的视觉几何与真实世界一致。这一步骤降低了视觉策略对相机位姿偏差的敏感性。

### 失败模式分析

尽管 VIRAL 取得了 91.5% 的成功率，5 次失败案例揭示了当前方法的边界：
- 抓取失败是主要的失败模式，通常源于物体位姿的微小偏差导致手指与物体的接触不充分；
- 在极少数情况下，放置阶段的定位误差导致物体未能准确放入托盘。

这些失败模式指向了系统辨识和视觉随机化仍无法完全覆盖的物理差距——特别是接触动力学的精细建模。模拟器对摩擦、接触柔顺性和物体微动等物理现象的近似，在抓取这种对接触精度要求极高的任务中尤为明显。

### 关键图表汇总

| 图表 | 核心结论 |
|------|----------|
| Figure 7 | 真实世界 91.5% 成功率，速度超越人类专家 |
| Figure 8 | 在空间、外观、物体类别上的泛化能力 |
| Figure 9 | RSI 和 Delta 动作空间是教师策略成功的必要条件 |
| Figure 11 | DAgger-BC 混合（α=0.5）显著优于纯 BC |
| Figure 13 | 关闭视觉域随机化导致性能下降 35.1% |
| Figure 14 | 教师训练需要 8-16 GPU 才能达到高成功率 |
| Figure 15 | 学生训练扩展到 64 GPU 带来显著的收敛和性能提升 |
| Figure 16 | 多物体训练在所有类别上优于单物体训练 |

### 计算成本与可复现性

VIRAL 的计算需求值得关注：教师训练需 8-16 GPU，学生训练需 64 GPU 的大规模并行仿真。这一计算门槛虽然带来了突破性的 sim-to-real 迁移能力，但也限制了中小型实验室的直接复现。论文使用了基于 Genesis 物理引擎的定制仿真环境，并通过 TRL 和 HuggingFace Accelerate 实现分布式训练。

## 定位与知识库关联

### 1. 方法谱系：从盲态运动到底层WBC的继承与突破

VIRAL并非孤立的工作，它深植于两条日益交汇的研究主线：**人形机器人的全身控制（WBC）** 与 **视觉Sim-to-Real迁移**。理解VIRAL的创新，需要先厘清它在这些谱系中的继承与断裂点。

**底层控制器继承：HOMIE WBC**
VIRAL的高层策略并不直接输出关节扭矩，而是输出delta指令给一个预训练的全身控制器（WBC）——**HOMIE**。HOMIE充当了“运动API”的角色，将高层语义指令（如“向目标移动基座速度增量$\Delta \mathbf{v}_t$”、“调整手臂关节增量$\Delta \mathbf{q}_t^{\mathrm{arm}}$”）转化为关节空间的扭矩。这一分层设计使得VIRAL的策略网络可以专注于任务级决策，而将底层稳定控制交给成熟的WBC。所有消融实验和人类遥操作对比均在同一HOMIE WBC上运行，确保了比较的公平性。

**核心突破：将Sim-to-Real蒸馏范式拓展至人形移动操作**
在VIRAL之前，Sim-to-Real的成功案例主要集中在四足盲态运动或固定基座的桌面操作。将这一范式迁移到**人形移动操作**面临三重断裂：
1. **动作空间耦合**：行走、转向、抓取、放置的动作高度耦合，单一动作空间的偏差会通过全身动力学级联放大。
2. **视觉依赖**：移动操作天然依赖机载RGB视觉来定位物体和目标，而视觉的Sim-to-Real gap远大于本体感觉。
3. **长时程误差累积**：连续54个循环的移动操作意味着任何微小偏差都会在数分钟内累积至任务失败。

VIRAL通过**特权教师-视觉学生蒸馏**框架跨越了这些断裂。教师策略在仿真中享有完全状态信息（物体精确位姿、全局坐标等），通过PPO强化学习掌握任务；学生策略仅依赖108×192的RGB图像和本体感觉，通过DAgger与行为克隆的混合蒸馏（$\alpha=0.5$）继承教师的能力。这一框架继承了“特权学习”的思想，但将其首次成功应用于**视觉驱动的人形移动操作**这一高维、长时程领域。

### 2. 关键设计选择的因果机制

VIRAL的成功并非偶然，而是由几个相互依赖的设计选择共同支撑。消融实验揭示了这些选择的因果强度：

| 设计选择 | 因果强度 | 机制 | 证据锚点 |
|---------|---------|------|---------|
| **Delta动作空间** | 决定性 | 绝对关节目标会因累积误差导致策略崩溃；delta指令使WBC在局部线性化空间内工作，大幅降低探索难度 | Figure 9：绝对动作空间变体无法达到高成功率 |
| **参考状态初始化（RSI）** | 决定性 | 从200条遥操作演示中采样初始状态，将RL探索约束在有意义的区域，避免从零开始的稀疏奖励困境 | Figure 9：无RSI时成功率<10%，加入后~95% |
| **视觉域随机化** | 强因果（-35.1%） | 光照、材质、相机外参、图像质量、传感器延迟的全域随机化，迫使学生策略学习视觉不变性 | Figure 13：关闭所有随机化后标准化成功率降至0.649 |
| **DAgger-BC混合蒸馏** | 中等因果 | 纯BC因分布偏移导致级联失败；引入学生在线rollout（DAgger）使训练分布更接近部署分布 | Figure 11：α=0.5的混合策略显著优于纯BC |
| **系统识别（SysID）** | 必要但非充分 | 校准手指执行器的armature、刚度和阻尼参数，使仿真关节轨迹与真实测量对齐 | Figure 5：SysID前后关节轨迹对齐度显著改善 |

**Delta动作空间与RSI的协同效应**尤为关键。单独使用RSI而无delta动作空间，策略仍会因绝对目标的累积误差而失败；单独使用delta动作空间而无RSI，RL在稀疏奖励下无法有效探索。两者共同作用，将成功率从<10%推升至~95%（Figure 9），形成了VIRAL教师策略的“最小可行组合”。

### 3. 计算规模的门槛效应

VIRAL揭示了一个重要的**规模门槛**：视觉Sim-to-Real迁移的成功不仅依赖于算法设计，还依赖于足够的并行计算规模。

- **教师训练**：1-2个GPU无法使策略收敛到高成功率；扩展到8-16个GPU后，异步PPO的并行环境数量足以覆盖多样化的初始状态和随机化条件，成功率跃升至90%以上（Figure 14）。
- **学生蒸馏**：视觉域随机化使观测空间高度复杂，1个GPU的训练缓慢且不稳定；扩展到64个GPU后，分布式渲染大幅提升了视觉多样性的吞吐量，收敛速度、优化平滑度和最终性能均显著提升（Figure 15）。

这一发现意味着VIRAL的复现门槛较高，中小型实验室可能因GPU资源不足而无法直接迭代。这也引出了开放问题：**是否存在算力效率的“甜蜜点”**，在保证迁移能力的同时降低计算需求？

### 4. 适用边界与已知局限

VIRAL的能力边界由其训练范式的固有局限所定义：

**物理覆盖差距**
模拟器（Genesis）难以精确建模流体-结构交互、可变形物体、复杂摩擦/碰撞等动力学。当前任务（刚性桌面物体抓取-放置）避开了这些挑战，但在涉及布料折叠、液体搬运、柔性工具使用等任务时，SysID和域随机化可能不足以弥合Sim-to-Real gap。这是一个需要手动验证的潜在失效模式。

**任务多样性受限**
当前训练任务由研究人员手动设计（固定的“走向桌子→抓取→走向托盘→放置→转向”循环），缺乏像大语言模型那样自动生成大规模多样化任务的能力。多物体训练（Figure 16）已展示出初步的泛化能力，但任务结构的多样性（如开门、上下楼梯、动态避障）仍未覆盖。

**奖励设计的可扩展性瓶颈**
VIRAL使用手工设计的五阶段加权奖励函数（$r_t = \sum_{i=0}^{4} w_i \mathbb{1}[s_t = i] r_t^{(i)}$），每个阶段有独立的奖励项（行走奖励$r_{\mathrm{walk}}$、放置奖励$r_{\mathrm{place}}$、抓取高度奖励$r_{\mathrm{grasp-z}}$等）。这种设计在复杂任务中极易被策略“偷懒”或“奖励黑客”利用，且随着任务增长，工程成本呈非线性增长。

**计算成本**
视觉Sim-to-Real训练需要数十个GPU的大规模并行渲染，这限制了该方法的普适性和快速迭代能力。

### 5. 开放问题与未来方向

基于上述局限，VIRAL指向以下开放问题：

1. **物理覆盖的工程降本**：如何以较低的工程成本为模拟器注入多样化物理现象（可变形体、流体、颗粒介质），缩小物理覆盖差距？自动化SysID流水线或基于真实数据的物理参数学习可能是方向。

2. **任务生成的规模化**：能否借鉴大语言模型的数据生成范式，自动生成海量、多样化的功能性移动操作任务？这需要将自然语言任务描述转化为可执行的奖励函数和场景配置。

3. **可扩展奖励设计**：如何设计不易被策略利用且可自动扩展的奖励函数？基于视觉-语言模型的自动奖励生成、或基于演示的逆强化学习可能是候选路径。

4. **Sim-to-Real的闭环整合**：当前VIRAL是纯仿真训练+零样本部署。如何将真实世界的模仿学习、基础模型与仿真训练有机整合，形成“仿真预训练→真实微调→仿真增强”的闭环框架，是提升鲁棒性和泛化能力的关键方向。

5. **算力效率的优化**：在Sim-to-Real训练中，是否存在更高效的视觉随机化策略或蒸馏方法，在降低GPU需求的同时保持迁移能力？这直接关系到该范式的民主化。

## 原文 PDF

![[paperPDFs/CVPR_2026/VIRAL_Visual_Sim_to_Real_at_Scale_for_Humanoid_Loco_Manipulation.pdf]]
