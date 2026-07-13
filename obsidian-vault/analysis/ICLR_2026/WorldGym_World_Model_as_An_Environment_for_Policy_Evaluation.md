---
title: "WorldGym: World Model as An Environment for Policy Evaluation"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/WorldGym_World_Model_as_An_Environment_for_Policy_Evaluation.pdf
project_link: https://world-model-eval.github.io
code_link: null
openreview_forum_id: hidBHy1CAw
aliases:
- WorldGym
tags:
- ICLR_2026
- topic/reinforcement_learning_planning_agents
- topic/reinforcement_learning_planning_agents/deep_rl
core_operator: "利用大规模离线视频数据训练单个动作条件世界模型，通过Monte Carlo rollout模拟执行并配合VLM自动评估成功，从而以极低成本获得与真实世界高度相关的策略性能估计；同时灵活对齐扩散生成时域与策略动作块大小，实现高效并行评估。"
primary_logic: "尽管任务和策略层出不穷，物理世界遵循统一的物理规律。因此，用一个在多样化数据上训练的世界模型即可泛化地评估任意策略在任意任务上的表现，避免了为每个策略单独建模动力学的困难。"
claims:
- "世界模型评估的策略成功率与真实世界成功率之间的皮尔逊相关系数达到0.78，显示出强相关性。"
- "三个VLA策略（RT-1-X, Octo, OpenVLA）在世界模型中的平均成功率仅与真实世界相差3.3%，且相对排名完全保持。"
- "世界模型能够正确反映不同模型版本、尺寸和训练步数之间的性能排序（更大/更新的模型得到更高成功率）。"
- "通过编辑初始图像或修改语言指令，世界模型可便捷地测试策略在OOD任务和环境上的表现，并揭示出策略对物体形状、2D/3D混淆等弱点。"
---

# WorldGym: World Model as An Environment for Policy Evaluation

> [!tip] 核心洞察
> 尽管任务和策略层出不穷，物理世界遵循统一的物理规律。因此，用一个在多样化数据上训练的世界模型即可泛化地评估任意策略在任意任务上的表现，避免了为每个策略单独建模动力学的困难。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | WorldGym：以世界模型作为策略评估环境 |
| 英文题名 | WorldGym: World Model as An Environment for Policy Evaluation |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=hidBHy1CAw) · [Project](https://world-model-eval.github.io) |
| Topic | #topic/reinforcement_learning_planning_agents #topic/reinforcement_learning_planning_agents/deep_rl |
| Method | WorldGym |
| Dataset | OpenVLA Bridge evaluation 17项任务, Bridge OOD Language Tasks (4项), Bridge OOD Image Distractors (17项) |

> [!tip] 效果简介
> - OpenVLA Bridge evaluation 17项任务 上，皮尔逊相关系数（每任务成功率在WorldGym与真实世界之间） 为 0.78，对比 1.0（理想），变化 -0.22。
> - OpenVLA Bridge evaluation 17项任务 上，平均成功率差异（WorldGym vs 真实世界） 为 3.3%，对比 0%（完美），变化 3.3%。
> - Bridge OOD Language Tasks (4项) 上，成功率（计数） 为 OpenVLA: 7,1,8,3，对比 RT-1-X: 3,0,4,1; Octo: 0,0,2,2，变化 OpenVLA显著优于其他。

## 概要

### 问题瓶颈

机器人策略评估长期受困于一个核心矛盾：真实世界测试成本高昂、难以复现且无法规模化，而传统手工仿真器（如PyBullet、MuJoCo）又难以捕捉复杂物理交互，导致显著的sim-to-real差距，使评估结果无法可靠地反映策略在真实场景中的表现。这一瓶颈严重制约了机器人学习——特别是视觉语言动作（VLA）策略——的快速迭代与公平比较。

### 核心洞察

WorldGym的出发点是一个简单但有力的观察：尽管任务和策略层出不穷，物理世界始终遵循统一的物理规律。因此，**用一个在多样化数据上训练的动作条件世界模型，即可泛化地评估任意策略在任意任务上的表现**，无需为每个策略单独建模动力学。这一洞察将评估问题从“为每个策略构建仿真器”降维为“学习一个通用的物理世界代理”。

### 方法定位

WorldGym是一个**基于世界模型的策略评估环境**。其核心组件包括：一个在潜在空间运行的扩散Transformer世界模型，以动作序列为条件生成未来视频帧；一个策略rollout循环，将策略推理与世界模型前传交替执行，实现长序列仿真；以及一个视觉语言模型（VLM）奖励模块，自动判断任务完成度。该方法在方法谱系中填补了“可扩展、高保真且低成本的策略评估”这一空白——它既避免了真实机器人实验的高昂开销，又克服了手工仿真器的物理建模局限。

### 核心结果

WorldGym在多项关键指标上验证了其作为评估环境的有效性：

- **与真实世界高度相关**：在OpenVLA Bridge评估套件的17项任务上，WorldGym评估的策略成功率与真实世界成功率之间的皮尔逊相关系数达到 **r = 0.78**，显示出强相关性（Figure 4a）。
- **绝对误差小**：三个VLA策略（RT-1-X、Octo、OpenVLA）在世界模型中的平均成功率与真实世界仅相差 **3.3%**，且相对排名完全保持（Figure 4b）。
- **版本敏感性**：WorldGym能够正确反映不同模型版本、尺寸和训练步数之间的性能排序——更大、更新的模型获得更高成功率（Figure 6, Figure 7）。
- **OOD泛化测试**：通过编辑初始图像或修改语言指令，WorldGym可便捷地测试策略在分布外任务和环境上的表现，并成功揭示了策略对物体形状依赖、2D/3D混淆等弱点（Figure 8-13）。
- **长期稳定性**：在40步rollout中，生成视频的平均LPIPS始终低于0.2，表明视觉误差不会爆炸式累积（Figure 17）。



### 机器人策略评估的现实困境

机器人学习面临一个核心瓶颈：**如何高效、可靠地评估策略性能**。真实世界的物理实验是最直接的评价方式，但其成本高昂、难以复现，且无法规模化——每一次策略迭代都需要重新部署机器人、重置环境、执行数百次试验，严重制约了机器人学习的发展速度。

传统方法试图通过**手工仿真器**（如PyBullet、MuJoCo）来缓解这一问题。然而，手工建模的仿真器存在两个根本性缺陷：其一，构建高保真仿真环境需要大量人工建模工作，难以覆盖真实世界的多样场景；其二，物理引擎与真实物理交互之间存在难以弥合的**sim-to-real差距**，导致仿真中的策略排名往往无法准确反映真实世界的表现。

### 从“为每个策略建模”到“为物理世界建模”

面对上述困境，一个关键洞察浮现：**尽管任务和策略层出不穷，物理世界遵循统一的物理规律**。这意味着，与其为每个新策略单独构建动力学模型，不如训练一个通用的世界模型，使其能够泛化地模拟任意策略在任意任务上的行为轨迹。

这一思路将问题从“策略特定的动力学建模”转化为“数据驱动的物理世界建模”。近年来，大规模离线机器人视频数据的积累——涵盖多种机器人形态、操作场景和任务类型——为训练此类世界模型提供了前所未有的数据基础。

### WorldGym的核心动机

基于上述洞察，WorldGym提出了一种全新的策略评估范式：**以动作条件视频世界模型作为生成式评估环境**。具体而言：

- **替代真实环境**：利用大规模离线视频数据训练单个动作条件世界模型，使其能够从初始观测帧和动作序列出发，预测未来的视觉观测序列。策略在该世界模型中进行Monte Carlo rollout，模拟执行过程。

- **自动化评估**：将生成的rollout视频输入视觉语言模型（VLM），由VLM根据任务语言指令自动判断成功与否，替代人工观察或手工启发式规则。

- **高效并行**：通过将扩散生成时域与策略的动作块大小对齐，实现可变长度的并行帧生成，显著提升长序列rollout的推理效率。

这一框架旨在以极低成本获得与真实世界高度相关的策略性能估计，同时保持策略之间的相对排名，使研究者能够在无需物理机器人的情况下，快速迭代和比较不同策略。



## 核心方法与创新机理

WorldGym 的核心创新在于将策略评估从物理世界迁移至**生成式视频世界模型**，从而以极低成本获得与真实世界高度相关的策略性能估计。其关键设计围绕三个 changed slots 展开。

### 1. 评估环境：从物理交互到生成式视频仿真

传统策略评估依赖真实机器人实验或手工物理仿真器（如PyBullet、MuJoCo）。前者成本高昂且难以复现，后者需手工建模场景与物理参数，存在显著的sim-to-real差距。WorldGym 用一个**动作条件视频生成模型**替代物理环境：给定初始观测帧 $o_0$ 和策略输出的动作序列，世界模型 $\hat{T}$ 自回归地预测未来观测帧，形成闭环的生成式仿真器（Figure 1）。该世界模型在 Bridge V2、RT-1、VIOLA、Berkeley UR5 等多形态机器人数据上联合训练，能够复现不同形态机器人的动作效果（Figure 2），并在端到端控制扫描中精确跟随单一动作维度（如上下、左右、开合）的变化（Figure 3）。

这一设计的核心洞察在于：**尽管任务和策略层出不穷，物理世界遵循统一的物理规律**。因此，一个在多样化数据上训练的世界模型即可泛化地支持任意策略在任意任务上的评估，避免了为每个策略单独建模动力学的困难。

### 2. 动作遵循机制：AdaLN-Zero 调制与无分类器引导

为提升世界模型对动作输入的遵循度，WorldGym 设计了专门的动作条件化机制。每帧的机器人动作向量经线性投影后，与扩散时间步嵌入**逐元素相加**，其结果通过 **AdaLN-Zero 调制**注入潜在扩散Transformer的每一层（Section 3.1.1）。相较于标准交叉注意力，这种逐元素相加与自适应层归一化的组合提供了更强的动作可控性。

此外，训练时对动作进行**随机丢弃**（random action dropout），推理时采用**无分类器引导**（classifier-free guidance），进一步强化了模型对动作信号的依赖，避免模型忽略动作输入而仅依赖视觉上下文外推。这一设计是 WorldGym 在长序列 rollout 中保持动作一致性的关键。

### 3. 可变扩散时域：对齐策略动作块大小以提升效率

现有视频扩散模型（如 Cosmos）通常固定生成帧数（如16帧），而机器人策略常以不同长度的**动作块**（action chunk）输出。WorldGym 提出将扩散去噪时域与策略的动作块大小**动态对齐**：若策略一次输出 $k$ 步动作，世界模型则一次生成 $k$ 帧未来观测。这使得世界模型可以并行预测整个动作块对应的视频片段，而非逐帧串行生成。

实验表明，将扩散时域从1帧增加到4帧，生成40帧 rollout 的推理时间从 93s 缩短至 33s，**加速2.8倍**（Table 9）。该设计使 WorldGym 能在单张 GPU 上一小时内完成数百步交互的完整评估，兼具高吞吐与灵活性。

### 4. VLM 自动奖励：替代人工成功判定

传统评估依赖人工观察或手工启发式规则判定任务成功。WorldGym 将世界模型生成的 rollout 视频输入视觉语言模型（GPT-4o），由 VLM 根据语言指令自动判断成功/失败，并支持部分积分（partial credit）。在 RT-1 真实视频上的验证显示，该奖励模型达到**高真阳率（0.81）和极低假阳率（0.03）**（Table 3），保障了评估的可靠性。所有策略使用相同的 VLM 提示和奖励机制，避免了因评估标准差异造成的不公。



![[assets/figures/papers/paper_list_l42_https_openreview_net_forum_id_hidBHy1CAw/figures/001_Figure_1.jpg]]

WorldGym 将机器人策略评估重新表述为一个**基于生成式世界模型的闭环仿真问题**。其核心 pipeline 由三个相互耦合的模块构成：世界模型（World Model）、策略 Rollout 循环与 VLM 奖励评估，三者协同工作，仅需一张初始观测图像和一条语言指令即可完成对任意策略的性能估计。

### 输入输出流

系统接受两类输入：(1) 来自真实场景的初始帧 $o_0$（RGB 图像）；(2) 描述任务目标的语言指令 $g$。输出为策略 $\pi$ 在任务上的期望成功率估计 $\hat{\rho}(\pi)$，定义为：

$$\hat{\rho}(\pi) = \mathbb{E}\left[\hat{R}([o_0, \ldots, o_H], g) \mid s_0, g \sim G, \mathbf{a} \sim \pi(\mathbf{o}, g), \mathbf{o}' \sim \hat{T}(\mathbf{o}, \mathbf{a}), \mathbf{o} = \mathbf{o}'\right]$$

其中 $\hat{T}$ 为学习到的动作条件世界模型，$\hat{R}$ 为 VLM 奖励函数，$H$ 为任务执行时域。

### 模块关系与数据流

**世界模型**是整个系统的动力学核心，基于潜在扩散 Transformer 和 Diffusion Forcing 构建（见 Section 3.1.1）。它接收当前观测帧和策略输出的动作块，生成未来帧序列。动作通过 AdaLN-Zero 调制机制注入：动作向量与扩散时间步嵌入逐元素相加后，经 AdaLN-Zero 调节模型各层的归一化参数，同时配合随机动作丢弃与无分类器引导增强动作可控性。因果时间注意力确保自回归生成时仅依赖历史帧。

**策略 Rollout 循环**实现长序列仿真（见 Section 3.1.2）。流程为：世界模型以 $o_0$ 初始化 → 策略 $\pi$ 接收当前观测并输出动作块 $\mathbf{a}_{\text{pred}}$ → 世界模型根据 $\mathbf{a}_{\text{pred}}$ 预测新帧 → 最新帧反馈给策略 → 迭代至时域 $H$。关键创新在于**扩散时域与策略动作块大小的灵活对齐**：世界模型可根据不同策略的 chunk size 动态调整每次生成的帧数，实现可变长度并行生成，显著提升推理效率。

**VLM 奖励评估**接收完整的 rollout 视频序列和语言指令，由 GPT-4o 判断任务完成度（见 Section 3.1.3）。奖励机制支持稀疏成功判定与部分积分，输出用于计算策略的 Monte Carlo 期望成功率。

### 设计逻辑

该框架的根本假设是：尽管任务和策略层出不穷，物理世界遵循统一的物理规律。因此，一个在多样化数据上训练的世界模型即可泛化地评估任意策略在任意任务上的表现，避免了为每个策略单独建模动力学的困难。整个评估流程可在单 GPU 上一小时内完成，仅需每项任务的初始图像，无需真实机器人硬件。



### 问题形式化

WorldGym 将策略评估形式化为在真实环境动力学 $T$ 下的期望累积奖励估计问题。给定初始状态 $s_0$、目标 $g$ 和策略 $\pi$，策略的真实价值定义为：

$$\rho ( \pi ) = \mathbb { E } [ R ( s _ { H } , g ) | s _ { 0 } , g \sim G , a _ { t } \sim \pi ( s _ { t } , g ) , s _ { t + 1 } \sim T ( s _ { t } , a _ { t } ) , \forall t \in [ 0 , H ] ]$$

其中 $R(s_H, g)$ 为稀疏奖励函数，仅在最终状态判定任务成功与否；$H$ 为任务时域。由于真实动力学 $T$ 不可直接获取，WorldGym 用学习到的世界模型 $\hat{T}$ 和 VLM 奖励函数 $\hat{R}$ 进行 Monte Carlo 近似：

$$\hat { \rho } ( \pi ) = \mathbb { E } [ \hat { R } ( [ o _ { 0 } , \ldots , o _ { H } ] , g ) | s _ { 0 } , g \sim G , \mathbf { a } \sim \pi ( \mathbf { o } , g ) , \mathbf { o } ^ { \prime } \sim \hat { T } ( \mathbf { o } , \mathbf { a } ) , \mathbf { o } = \mathbf { o } ^ { \prime } ]$$

此处 $\mathbf{o}$ 为观测帧序列，$\hat{T}$ 以动作序列 $\mathbf{a}$ 为条件生成未来帧，$\hat{R}$ 基于完整 rollout 视频判定任务完成度。

### 世界模型架构

世界模型基于潜在扩散 Transformer 和 Diffusion Forcing 构建，核心设计包括三个关键机制：

**动作条件注入。** 每帧机器人动作向量经线性投影后与扩散时间步嵌入逐元素相加，结果通过 AdaLN-Zero 调制注入模型各层。训练时以概率 $p$ 随机丢弃动作向量（替换为零向量），推理时结合无分类器引导增强动作可控性。

**因果时序注意力。** 在空间注意力块之间交错插入因果时序注意力块，使模型在生成当前帧时仅能访问历史帧的潜在表示，实现自回归式帧生成。

**可变扩散时域。** 推理时，扩散时域长度 $K$ 与策略的动作块大小对齐——策略一次输出 $K$ 步动作，世界模型同步生成 $K$ 帧未来观测，再将最新帧反馈给策略进行下一轮推理。这一设计使 40 帧 rollout 的推理时间从固定单帧生成的 93 秒缩短至 33 秒（$K=4$ 时，2.8 倍加速）。

### 策略 Rollout 循环

评估流程为闭环迭代：世界模型以真实初始帧 $o_0$ 初始化，策略 $\pi$ 根据当前观测生成动作块 $\mathbf{a}_{\text{pred}}$，世界模型以 $\mathbf{a}_{\text{pred}}$ 为条件预测新帧序列，取最新帧作为下一轮策略输入，循环直至达到时域 $H$。所有策略使用相同的真实世界初始帧，每任务进行 10 次随机初始物体位置的独立试验。

### VLM 奖励评估

生成的 rollout 视频送入视觉语言模型（GPT-4o），由 VLM 根据语言指令 $g$ 判断任务是否成功，输出成功/失败标签及部分积分。在 RT-1 真实视频上的验证显示，该奖励模型达到 0.81 的真阳率和 0.03 的极低假阳率，保障了评估可靠性。所有策略使用相同的 VLM 提示和奖励机制，避免因评估差异造成不公。

### 视觉保真度保障

长期 rollout 的视觉误差不会爆炸：在 40 步生成中，平均 LPIPS 始终低于 0.2（Figure 17），确保生成视频在整个仿真过程中保持视觉合理性。这一特性得益于 Diffusion Forcing 的序列建模能力和大规模多样化训练数据——使用 Bridge V2（相比 V1）训练的世界模型在所有像素级指标（MSE、LPIPS、SSIM）上均有显著提升。



## 实验与关键发现

### 核心评估指标与策略排名保真度

WorldGym作为策略评估环境的根本有效性，取决于其能否复现真实世界中的策略性能排序。实验在OpenVLA Bridge评估套件（17项任务）上展开，每项任务执行10次真实世界试验，并使用相同的初始帧在世界模型中进行10次rollout仿真。

**成功率相关性。** 将各任务上三种VLA策略（RT-1-X、Octo、OpenVLA）在WorldGym中的成功率与真实世界成功率绘制散点图，得到皮尔逊相关系数 **r = 0.78**（Figure 4a）。这一强相关性表明，世界模型能够捕捉任务难度和策略能力的相对差异，而非仅输出随机或均匀的成功率。

**平均成功率偏差。** 三种策略在WorldGym中的平均成功率与真实世界仅相差 **3.3%**（Figure 4b）。具体而言，OpenVLA在真实世界成功率为70.6%，世界模型中为67.4%；Octo分别为20.0%和23.8%；RT-1-X分别为14.1%和13.5%。更重要的是，三种策略的相对排名在世界模型中完全保持：OpenVLA > Octo > RT-1-X。这一排名的稳定性是WorldGym作为评估工具的核心价值——即使绝对数值存在小幅偏差，只要排序可靠，就能支持模型选择和迭代决策。

**版本与训练动态的敏感性。** WorldGym能够区分同一策略系列中不同版本和尺寸的模型。Figure 6显示，更大/更新的Octo和OpenVLA版本在世界模型中获得更高的成功率。Figure 7进一步验证了训练过程中的评估一致性：从头训练基于视频的策略和扩散策略时，WorldGym评估的成功率随训练步数增加而单调上升。这意味着WorldGym不仅适用于最终模型的横向对比，也可用于训练过程中的检查点选择。


![[assets/figures/papers/paper_list_l42_https_openreview_net_forum_id_hidBHy1CAw/figures/006_Figure_6.jpg]]
*Figure 6: Per-Task Success Rates: Real World vs World Model*

**计算效率。** 所有WorldGym rollout可在单GPU上于一小时内完成，仅需每项试验的初始图像。相比之下，真实世界评估需要物理机器人、人工监督和大量时间成本，且难以保证试验条件的一致性。

### 消融实验：世界模型质量与推理效率

**训练数据规模的影响。** 世界模型的视觉保真度直接影响策略评估的可靠性。Table 8显示，使用更大的Bridge V2数据集（相比V1）训练世界模型，在所有像素级指标上均取得显著提升：MSE降低、LPIPS降低、SSIM提高。这表明世界模型的生成质量受益于更多样化的训练数据，与“物理规律统一性”的核心洞察一致——更多数据帮助模型学习更通用的物理交互模式。

**扩散时域与推理速度。** WorldGym的关键设计之一是灵活对齐扩散生成时域与策略的动作块大小。Table 9的消融表明，将扩散时域从1帧增加到4帧，可将生成40帧rollout的推理时间从93秒缩短至33秒，加速 **2.8倍**。这一设计使得WorldGym能够高效评估使用不同动作块大小的策略（如RT-1-X的固定块 vs OpenVLA的可变块），避免了为每种策略重新训练世界模型的需要。

**动作遵循机制。** 世界模型对动作输入的忠实遵循是评估有效性的前提。Section 3.1.1报告，对动作向量进行随机丢弃（random action dropout）并结合无分类器引导（classifier-free guidance），有效提升了生成视频对指定动作的遵循度。Figure 3的端到端控制扫描实验定性地验证了这一点：对单一动作维度（上下、左右、开合）进行扫描时，生成视频紧密跟随预期的末端执行器运动，即使这些动作模式在训练数据中未以纯扫描形式出现。

**VLM奖励模型的可靠性。** 评估流程的最后一环是GPT-4o作为奖励模型判断任务成功与否。Table 3的混淆矩阵显示，在RT-1真实视频上，GPT-4o的真阳率（True Positive Rate）为 **0.81**，假阳率（False Positive Rate）仅为 **0.03**。极低的假阳率意味着VLM很少将失败误判为成功，这对于策略评估的保守性至关重要——避免高估策略能力。相对较高的假阴率（0.19）虽然可能导致低估部分策略，但不会破坏策略间的相对排名。

**长期rollout的视觉稳定性。** 一个潜在担忧是生成误差在长序列rollout中累积爆炸。Figure 17显示，在40步rollout中，平均LPIPS始终低于0.2，表明视觉误差保持有界，生成帧在视觉上始终保持合理。这一特性是WorldGym能够支持长时域任务评估的基础。

### OOD泛化评估：揭示策略的隐藏弱点

WorldGym的独特价值在于，它能够以极低成本测试策略在分布外（OOD）任务和环境上的表现——这在真实世界中往往需要重新搭建场景、购置物体，成本高昂。

**OOD语言指令。** Table 1展示了四项修改语言指令后的Bridge任务结果。OpenVLA在所有任务上均优于RT-1-X和Octo，尤其在“将锅移到台面上”这一最具挑战性的任务上（Bridge数据集中不存在将物体移出水槽的轨迹），OpenVLA成功8次，而Octo仅2次。这一优势归因于OpenVLA更强的语言模型骨干。


![[assets/figures/papers/paper_list_l42_https_openreview_net_forum_id_hidBHy1CAw/figures/018_Table_1.jpg]]

**OOD视觉场景。** 通过图像编辑模型（Nano Banana）在初始帧中添加未见物体，可测试策略的视觉泛化能力。Figure 8的颜色分类实验显示，OpenVLA完美辨别红/蓝纸片（成功率100%），而其他策略接近随机水平（约50%）。Figure 9进一步揭示，OpenVLA对物体的选择主要依赖形状而非颜色：当胡萝卜和橙子同时出现时，策略抓取距离更近的物体；但将胡萝卜颜色编辑为红色后，策略正确选择了橙子。

**失败模式诊断。** Figure 10展示了WorldGym揭示的两类典型失败模式：
- **2D/3D混淆**：在场景中添加显示胡萝卜图像的笔记本电脑后，OpenVLA在15%的试验中抓取了屏幕而非真实胡萝卜。这表明策略尚未完全理解屏幕图像的二维性质。
- **细粒度形状分类失败**：在区分方形/圆形、名人面孔、猫/狗的任务上，所有策略均接近随机水平，暴露了VLA在精细视觉理解上的普遍短板。

**分心物鲁棒性。** Figure 13和Table 7报告了在Bridge评估套件的每张初始图像中添加分心物后的策略性能下降：RT-1-X下降 **51%**，Octo下降 **83%**，OpenVLA下降 **41.5%**。OpenVLA展现出最强的鲁棒性，但所有策略均遭受显著性能损失，说明对视觉干扰的鲁棒性仍是VLA的共性弱点。

**跨环境泛化。** Table 4展示了在Google Robot任务（RT-1子集）上的评估结果。OpenVLA整体表现仍优于RT-1-X和Octo，但优势较Bridge环境缩小。这表明WorldGym能够反映策略在不同机器人形态和环境下的差异化表现，而非输出单一维度的排名。

### 实验公平性保障

所有策略评估遵循严格的公平性协议：使用相同的真实世界初始帧，每任务随机初始物体位置，试验次数一致（10次）；OOD测试中初始图像通过同一编辑模型生成，确保编辑一致性；所有策略使用相同的VLM提示和奖励机制。这些措施排除了因评估条件差异导致的不公平比较。

### 补充图表

![[assets/figures/papers/paper_list_l42_https_openreview_net_forum_id_hidBHy1CAw/figures/004_Figure_4.jpg]]

![[assets/figures/papers/paper_list_l42_https_openreview_net_forum_id_hidBHy1CAw/figures/007_Table_5.jpg]]
*Table 5: (a) Per-Task Task Success Rates. Each point represents a task from Table 5, with different policies being represented by different shaped markers. There is a strong correlation (r = 0.78) between policy performance in our world model (y-axis) and within the real world (x-axis). (b) Mean Success Rates. Robot policies’ mean success rates in the world model differ by an average of only 3.3% between from the real world, near the standard error range for each policy. Relative performance rankings between RT-1-X, Octo, and OpenVLA are also preserved. Figure 4: Success rates of modern VLAs, as evaluated within WorldGym and the real world*

![[assets/figures/papers/paper_list_l42_https_openreview_net_forum_id_hidBHy1CAw/figures/020_Figure_12.jpg]]
*Figure 12: OOD Distraction Examples. We use Nano Banana (Google, 2025) to add distractions to every image of the OpenVLA Bridge task suite. The resulting change in mean success rates can be seen in Figure 13. Figure 13: Effect of OOD Distractors. We use an image editing model to add distractor objects to the Bridge evaluation suite, finding that RT-1- X drops in performance by 51%, Octo by 83%, and OpenVLA by 41.5%, making OpenVLA the most robust to distractors. See Table 7 for details*




## 定位与知识库关联

### 核心设计逻辑

WorldGym的出发点源于一个根本瓶颈：真实机器人策略评估缺乏可扩展、高保真且多样化的测试环境。传统手工仿真器（如PyBullet、MuJoCo）需手工建模，难以捕捉复杂物理交互，导致sim-to-real差距；而真实世界测试成本高昂、难以复现，制约了机器人学习的迭代速度。

该工作的核心洞察在于物理规律统一性假设——尽管任务和策略层出不穷，物理世界遵循统一的物理规律。因此，用一个在多样化数据上训练的世界模型即可泛化地评估任意策略在任意任务上的表现，避免了为每个策略单独建模动力学的困难。这一假设将问题从“为每个策略建模”降维为“为物理世界建模”，显著降低了系统复杂度。

基于此，WorldGym构建了三个关键模块形成闭环评估流程：

**世界模型**：基于潜在扩散Transformer和Diffusion Forcing的动作条件视频生成模型。动作向量与扩散时间步嵌入逐元素相加后经AdaLN-Zero调制，同时采用随机动作丢弃与无分类器引导增强动作可控性。因果时间注意力机制使模型能以前帧为条件自回归生成未来帧。

**策略Rollout循环**：迭代运行策略推理与世界模型前传。关键创新在于根据策略的动作块大小动态调整扩散时域，实现可变并行生成——将扩散时域从1帧增加到4帧可将生成40帧rollout的推理时间缩短2.8倍（93s→33s），显著提升评估效率。

**VLM奖励评估**：使用GPT-4o接收生成视频，根据语言指令自动判断任务完成度。该奖励模型在RT-1真实视频上达到高真阳率（0.81）和极低假阳率（0.03），保障了评估的可靠性。

### 与现有方法的关系

WorldGym在评估环境类型上实现了根本性转变。传统方法依赖真实机器人实验（作为真值基准）或手工仿真器，而WorldGym构建了完全以图像观测驱动的生成式评估环境。这一转变使得评估从物理空间迁移到像素空间，成本从硬件依赖降低到单GPU小时级。

在视频生成的前向预测时域上，传统扩散模型（如Cosmos）固定生成帧数（通常16帧），而WorldGym根据策略的动作块大小动态调整，实现了策略无关的高效并行评估。在任务成功判定方式上，从人工观察或手工启发式规则转向VLM自动判断，支持部分积分，提升了评估的一致性和粒度。

值得注意的是，WorldGym并不试图替代真实世界评估，而是作为其高效代理。实验表明，世界模型评估的策略成功率与真实世界成功率之间的皮尔逊相关系数达到0.78，三个VLA策略（RT-1-X、Octo、OpenVLA）在世界模型中的平均成功率仅与真实世界相差3.3%，且相对排名完全保持。这一相关性水平足以支持策略筛选、版本对比和训练监控等实际应用场景。

### 适用边界与局限

**物理交互保真度**：世界模型完全基于视觉观测驱动，缺乏对力反馈、接触动力学等物理量的显式建模。长期rollout中视觉误差会累积，但实验显示在40步rollout中平均LPIPS始终低于0.2，保持视觉合理性，未出现误差爆炸。

**策略泛化评估的可靠性**：WorldGym能正确反映不同模型版本、尺寸和训练步数之间的性能排序（更大/更新的模型得到更高成功率），且可便捷地测试策略在OOD任务和环境上的表现。然而，OOD测试揭示了策略的特定弱点——如OpenVLA在15%的试验中混淆屏幕图像与真实物体（2D/3D混淆），所有策略在形状分类任务上接近随机水平。这些发现表明世界模型能够暴露策略缺陷，但其本身是否引入了额外的分布偏移需要进一步验证。

**数据依赖性**：世界模型的生成质量高度依赖训练数据规模。使用更大训练数据集（Bridge V2 vs V1）使生成视频在所有像素级指标（MSE、LPIPS、SSIM）上均显著提升。这意味着在数据稀缺的机器人形态或任务上，模型性能可能受限。

### 开放问题

WorldGym目前聚焦于桌面级操作任务和固定相机视角场景。其是否能泛化到更复杂的操作任务（如灵巧操作、长序列任务）和移动操作场景，仍需验证。此外，世界模型作为生成式环境，其自身的评估偏差如何随任务难度、策略分布偏移等因素变化，尚未有系统性分析。

一个更具野心的方向是将WorldGym从评估工具升级为训练环境。初步实验表明，在RL微调过程中WorldGym评估的成功率随训练步数增加而提升，暗示其可能作为策略优化的奖励信号源。但生成环境中的策略优化是否会导致对抗性利用世界模型的视觉缺陷，是一个需要警惕的风险。



## 原文 PDF

![[paperPDFs/ICLR_2026/WorldGym_World_Model_as_An_Environment_for_Policy_Evaluation.pdf]]
