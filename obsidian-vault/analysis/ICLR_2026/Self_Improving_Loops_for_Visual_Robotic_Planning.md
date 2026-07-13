---
title: "Self-Improving Loops for Visual Robotic Planning"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/Self_Improving_Loops_for_Visual_Robotic_Planning.pdf
project_link: https://diffusion-supervision.github.io/silvr/
code_link: null
openreview_forum_id: SzUgx5r3wy
aliases:
- SILVRPS
- SILVRP
tags:
- ICLR_2026
- topic/reinforcement_learning_planning_agents
- topic/reinforcement_learning_planning_agents/deep_rl
core_operator: "通过迭代收集成功轨迹并微调域内视频生成模型，使视觉规划器逐步适应新任务。"
primary_logic: "视觉规划将环境动力学建模与动作预测解耦，动力学模型更易迁移；结合自适应的微调循环，实现了样本高效的自改进，且无需地面真值奖励函数即可工作。"
claims:
- "SILVR 在 MetaWorld 12 个未见任务上，迭代 4 平均成功率达 44.2%，远超 DSRL 的 7.7% 和 BCIL 的 23.2%。"
- "在连续 10 轮迭代中，SILVR 性能持续单调递增，但第 5 轮后增益递减，接近饱和。"
- "即使使用视觉语言模型（VLM）替代人工地面真值进行数据筛选，SILVR 仍能迭代改进，说明框架不依赖精确人工奖励信号。"
- "MetaWorld 12 unseen tasks 上 平均成功率 (%) (迭代 4) = 44.2"
---

# Self-Improving Loops for Visual Robotic Planning

> [!tip] 核心洞察
> 视觉规划将环境动力学建模与动作预测解耦，动力学模型更易迁移；结合自适应的微调循环，实现了样本高效的自改进，且无需地面真值奖励函数即可工作。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 视觉机器人规划的自改进循环 |
| 英文题名 | Self-Improving Loops for Visual Robotic Planning |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=SzUgx5r3wy) · [Project](https://diffusion-supervision.github.io/silvr/) |
| Topic | #topic/reinforcement_learning_planning_agents #topic/reinforcement_learning_planning_agents/deep_rl |
| Method | Self-Improving Loops for Visual Robotic Planning (SILVR) |
| Dataset | MetaWorld 12 unseen tasks, Real-World Panda Arm Cup Push (2 unseen colors), Real-World Panda Arm Drawer Open (1 unseen color), MetaWorld 12 tasks (suboptimal init) |

> [!tip] 效果简介
> - MetaWorld 12 unseen tasks 上，平均成功率 (%) (迭代 4) 为 44.2，对比 DSRL: 7.7, BCIL: 23.2，变化 +36.5 / +21.0。
> - Real-World Panda Arm Cup Push (2 unseen colors) 上，平均成功率 (趋势) 为 持续提升至约 40-50%（基于图中的估值），对比 BCIL 提升缓慢，DSRL 未测试，变化 显著优于 BCIL。
> - Real-World Panda Arm Drawer Open (1 unseen color) 上，平均成功率 (趋势) 为 从低成功启动，多轮后提升，对比 BCIL 提升缓慢，变化 显著优于 BCIL。

## 概要

离线训练的视觉规划模型面临泛化瓶颈：在训练分布之外的新任务上表现脆弱，而基于行为克隆的在线强化微调方法（如 BCIL）样本效率低、提升幅度有限。根本原因在于，视觉规划将环境动力学建模与动作预测解耦——动力学模型本身具有更强的迁移性，但现有方法未能有效利用这一特性进行在线自适应。

SILVR（Self-Improving Loops for Visual Robotic Planning）的核心思路是：通过迭代收集成功轨迹并微调域内视频生成模型，使视觉规划器逐步适应新任务，无需地面真值奖励函数即可工作。具体而言，SILVR 每轮自采集轨迹，经稀疏奖励信号过滤后，同时微调域内文本到视频生成模型和逆动力学模型，形成闭环自改进。可选地，通过逆概率自适应（IPA）将互联网预训练视频模型（如 AnimateDiff）与域内模型组合，增强真实世界的泛化能力。

在 MetaWorld 仿真环境的 12 个未见任务上，SILVR 迭代 4 轮后平均成功率达 **44.2%**，远超 DSRL 的 7.7% 和 BCIL 的 23.2%。连续 10 轮迭代中性能单调递增，但第 5 轮后增益递减并趋于饱和。在真实世界 Panda 机械臂的推杯和开抽屉任务中，SILVR 同样展现出持续改进能力，尤其在启用互联网视频先验时效果显著。即使使用视觉语言模型替代人工地面真值进行数据筛选，SILVR 仍能迭代改进，表明框架不依赖精确人工奖励信号。

**方法定位**：SILVR 属于视觉规划与自改进学习的交叉，通过解耦环境动力学与动作预测、结合自适应微调循环，实现了样本高效的自改进。与 DSRL（基于扩散策略的强化学习微调）和 BCIL（基于行为克隆的自改进）相比，SILVR 在样本效率和最终性能上均具显著优势。

机器人学习系统长期面临一个核心瓶颈：**离线训练的视觉规划模型泛化能力有限，而基于行为克隆的在线强化微调方法样本效率低、提升幅度小**。具体而言，依赖静态数据集训练的策略在面对训练分布之外的新任务时性能急剧下降，而将强化学习直接应用于高维视觉观测空间的微调方法（如 DSRL，Wagenmaker et al., 2025）虽然在理论上可行，但在实践中每轮迭代仅能获得微弱的性能增益，难以有效利用在线交互数据。

这一瓶颈的因果根源在于**视觉规划将环境动力学建模与动作预测解耦**。动力学模型描述的是“世界如何变化”，其底层规律在不同任务间具有更强的可迁移性；而动作预测则高度依赖具体任务和机器人本体。现有方法未能充分利用这一结构特性：纯离线方法将两者绑定训练，限制了动力学模型的泛化潜力；在线微调方法则试图直接优化端到端策略，忽略了动力学模型可以作为更高效的迁移媒介。

SILVR（Self-Improving Loops for Visual Robotic Planning）的核心洞察正是基于上述解耦思想：**通过迭代收集成功轨迹并微调域内视频生成模型，使视觉规划器能够逐步适应新任务，而无需地面真值奖励函数即可工作**。该方法将视频生成模型作为可迁移的动力学先验，在每次与环境交互后，利用稀疏的成功信号筛选高质量经验，并将其反馈至模型微调过程中，形成一个闭环的自改进机制。这一设计使得模型能够在少量在线交互中持续提升性能，显著优于传统的行为克隆改进循环（BCIL）和基于扩散策略的强化学习微调方法（DSRL）。

此外，SILVR 还通过逆概率自适应（IPA）机制，可选地将互联网预训练的大规模视频模型（如 AnimateDiff）与域内模型组合。这一设计在真实世界机器人任务中尤为关键——互联网视频先验提供了丰富的视觉常识和物理直觉，弥补了域内数据在多样性和覆盖度上的不足，使视觉规划器在真实环境的复杂视觉条件下仍能有效运作。

从更宏观的视角看，SILVR 提出了一种**数据驱动、模型自适应的机器人学习新范式**：系统不再依赖人工设计的奖励函数或海量离线数据，而是通过与环境的闭环交互，自主筛选有益经验并持续改进自身。这一范式为视觉机器人规划在开放环境中的部署提供了可行的技术路径。

## 核心方法与创新机理

SILVR 的核心创新在于将视觉规划从“一次性离线训练”转变为“闭环在线自改进”，通过三个关键的 **changed slots** 实现了样本高效且无需精确奖励函数的自我提升。

### 1. 训练范式：从离线静态到在线迭代自改进

传统视觉规划方法（如扩散策略 **Diffusion Policy**，Chi et al., 2023）依赖纯离线训练，模型部署后性能固定，无法适应新任务。基于行为克隆的自改进循环 **BCIL** 试图通过在线收集数据微调策略，但提升缓慢；而基于强化学习的 **DSRL**（Wagenmaker et al., 2025）则因样本效率极低，在相同交互预算下几乎无法改进（Table 1 中 DSRL 迭代 4 仅达 7.7%）。

SILVR 将在线自改进构建为**迭代闭环**：每轮自主采集轨迹，经稀疏奖励过滤后，同时微调域内视频模型与逆动力学模型（IDM）。这一设计的关键因果机制在于：视觉规划将环境动力学建模与动作预测**解耦**——视频模型学习“场景如何变化”，IDM 学习“如何产生动作”。动力学模型因捕捉视觉-物理规律而更易跨任务迁移，使得少量成功轨迹即可驱动有效微调。实验表明，SILVR 在 MetaWorld 12 个未见任务上迭代 4 平均成功率已达 44.2%，远超 BCIL 的 23.2% 和 DSRL 的 7.7%（Table 1）；且性能在连续 10 轮迭代中**单调递增**，尽管第 5 轮后增益递减并趋于饱和（Figure 4 左图）。

### 2. 先验利用：从单域模型到互联网先验组合

基线方法仅使用域内视频模型，在真实世界场景中泛化能力有限。SILVR 通过**逆概率自适应**（Inverse Probabilistic Adaptation, IPA）将互联网预训练的大规模文本到视频模型（**AnimateDiff**，~2B 参数，预训练于 WebVid-10M）与域内模型组合。IPA 是一种免训练的采样时组合方法，其核心公式为：

$$\tilde{\epsilon}_{\mathrm{inv}} = \epsilon_{\mathrm{general}}(\tau_t, t) + \alpha \Bigl( \epsilon_{\mathrm{general}}(\tau_t, t \mid \mathrm{text}) + \gamma \epsilon_{\theta}(\tau_t, t \mid \mathrm{text}) - \epsilon_{\mathrm{general}}(\tau_t, t) \Bigr)$$

其中 $\epsilon_{\mathrm{general}}$ 为通用预训练模型，$\epsilon_{\theta}$ 为域内模型，$\gamma$ 控制先验强度，$\alpha$ 为文本引导尺度。这一组合使域内模型在保持特定环境动力学的同时，获得了互联网先验中的丰富视觉知识和文本条件泛化能力。

该创新的决定性证据来自真实世界实验：在 Panda 机械臂的推杯子和开抽屉任务中，若禁用互联网视频先验，SILVR 不仅难以改进，甚至出现性能退化；而启用 AnimateDiff 先验后，SILVR 持续提升并显著优于 BCIL（Figure 3 中右图）。值得注意的是，在仿真环境 MetaWorld 中这一差距不明显，说明互联网先验对弥合仿真-真实差距具有关键作用。

### 3. 数据过滤信号：从精确奖励到稀疏成功信号

传统强化学习微调依赖精心设计的密集奖励函数，而 BCIL 则无过滤机制，易受低质量数据污染。SILVR 仅需**稀疏成功信号**即可运作：每轮收集的轨迹经成功/失败二值判定过滤，仅保留成功轨迹用于微调。

这一设计的突破性在于：成功信号甚至可由**视觉语言模型（VLM）替代人工标注**。实验表明，使用 VLM（如 GPT-5、Gemini）进行数据筛选时，SILVR 仍能持续迭代改进，MetaWorld 上迭代 4 达 38.4%，虽略低于使用地面真值过滤的 44.2%，但已证明框架不依赖精确人工奖励函数（Table 1, Figure 5a）。这为 SILVR 在无奖励函数的开放环境中部署提供了可行路径。

### 创新协同效应

上述三个 changed slots 并非孤立生效，而是通过**解耦-组合-筛选**的协同机制产生放大效应：解耦的动力学模型降低了微调难度，互联网先验提供了泛化基础，稀疏筛选确保了数据质量。消融实验（Table A11）证实，仅微调 IDM 或仅微调视频模型均导致性能快速饱和，同时更新两者对处理对象和运动高度新颖的任务至关重要——这验证了视觉规划解耦设计的核心价值。

![[assets/figures/papers/paper_list_l18_https_openreview_net_forum_id_SzUgx5r3wy/figures/001_Figure_1.jpg]]
*Figure 1: SILVR Framework. SILVR has access to two pretrained video generative models (left): one pretrained generally on internet-scale data and another pretrained on a general set of in-domain demonstrations. By default, SILVR uses the in-domain video model as a visual planner, which when utilized to interact with the environment, is able to achieve successful trajectories even for initially unseen tasks. These trajectories are then iteratively fed back to finetune the in-domain model (right), thus improving the overall quality of future visual planning as a whole through self-collected online experience. SILVR can optionally incorporate internet-scale pretrained video models as prior, which partic...*

SILVR（Self-Improving Loops for Visual Robotic Planning）构建了一套解耦视觉规划与动作执行的闭环自改进系统。其核心思路源于一个因果洞察：**视觉规划将环境动力学建模与动作预测解耦后，动力学模型本身更易迁移**。基于此，SILVR 将离线预训练的视频生成模型作为视觉规划器，通过在线交互中自采集成功轨迹并迭代微调，逐步适应未见任务，而无需地面真值奖励函数即可工作。

### 框架总览

SILVR 框架由四个核心模块串联构成一条闭环自改进流水线（Figure 1）：

1. **域内文本到视频生成模型（In-domain Text-to-Video Model）**：基于 AVDC（Ko et al., 2024）构建，在去噪 U-Net 的每一层添加交叉注意力层以增强文本条件能力。该模型接收任务文本提示和当前观测图像，生成未来 8 帧的视觉规划。其参数规模约 13 亿（U-Net 为主），是框架的默认视觉规划器。

2. **逆概率自适应模块（IPA Adaptation）**：在采样时组合互联网预训练视频模型（AnimateDiff，约 20 亿参数，预训练于 WebVid-10M）与域内模型的分数预测，实现无需训练的域适配。采样公式为：

   $$\tilde{\epsilon}_{\mathrm{inv}} = \epsilon_{\mathrm{general}}(\tau_t, t) + \alpha \Bigl( \epsilon_{\mathrm{general}}(\tau_t, t \mid \mathrm{text}) + \gamma \epsilon_{\theta}(\tau_t, t \mid \mathrm{text}) - \epsilon_{\mathrm{general}}(\tau_t, t) \Bigr)$$

   其中 $\gamma$ 为先验强度，$\alpha$ 为文本引导尺度。该模块在真实世界实验中尤为关键——**若禁用互联网视频先验，SILVR 难以改进甚至退化**（Figure 3）。

3. **逆动力学模型（Inverse Dynamics Model, IDM）**：将视觉规划中连续两帧的嵌入映射为可执行的机器人动作。存在两种实现：MLP-IDM（轻量，直接预测动作）和 Diffusion-IDM（基于扩散策略 **Diffusion Policy**，Chi et al., 2023，建模能力更强）。

4. **自改进循环（Self-Improving Loop）**：每轮迭代执行三步操作——① 域内视频模型（可选结合 IPA）在环境中采集 30 条轨迹；② 利用稀疏奖励信号（地面真值或 VLM 如 GPT-5、Gemini）筛选成功轨迹；③ 用筛选后的数据微调域内视频模型（MetaWorld 上 10,000 步，学习率 1e-6）和逆动力学模型。该循环可迭代多轮，使模型逐步适应特定任务。

### 输入输出流

- **输入**：任务文本提示（如 "push the cup to the right"）、当前 RGB 观测图像、可选的互联网视频先验。
- **中间产物**：未来 8 帧的视觉规划视频片段。
- **输出**：通过 IDM 解码的机器人动作序列，或蒸馏后的轻量扩散策略（SILVR-Distilled DP）直接输出动作。

### 关键设计决策

- **解耦设计**：将“环境会如何变化”（视频生成）与“该如何动作”（IDM）分离，使动力学建模更易跨任务迁移，这是 SILVR 样本效率远超 DSRL（Wagenmaker et al., 2025）的根本原因——DSRL 的性能瓶颈不在于梯度更新步数，而在于经验收集（Table A7）。
- **自适应微调**：同时微调视频模型和 IDM 对处理对象与运动高度新颖的任务至关重要。仅微调其中之一会导致性能快速饱和（Table A11：仅微调 IDM 在迭代 4 仅达 29.8%，同时微调达 44.2%）。
- **稀疏奖励驱动**：框架不依赖密集奖励函数，仅需二值稀疏信号判断轨迹是否成功。即使使用 VLM 替代地面真值进行筛选，SILVR 仍能迭代改进（Figure 5：VLM 筛选下迭代 4 达 38.4%，虽略低于地面真值的 44.2%），证明框架对奖励信号的鲁棒性。
- **蒸馏部署**：视觉规划在推理时因视频生成计算开销较大，SILVR 支持将最终迭代的视觉规划器蒸馏为轻量扩散策略，在保持性能的同时实现反应式推理（Table 1：蒸馏后从 44.2% 提升至 49.2%）。

### 局限性

自改进循环约在 5 轮后趋于饱和，缺乏显式探索机制使模型可能陷入局部策略最小点。当前框架依赖手工子任务分解处理长时序任务，尚未实现端到端自改进。

SILVR 框架由四个核心模块构成，其设计根植于一个关键洞察：**视觉规划将环境动力学建模与动作预测解耦**，而单独学习的环境视觉动力学比直接映射观测到动作的端到端策略更易迁移。这一解耦使得域内视频模型成为自改进循环中的主要优化对象，逆动力学模型则承担将视觉预测转换为可执行动作的桥梁角色。

### 域内文本到视频生成模型

该模块是 SILVR 的视觉规划核心，基于 **AVDC**（Ko et al., 2024）实现，并在去噪 U-Net 的每一层额外添加了交叉注意力层以增强文本条件化能力。给定当前观测和任务文本提示，模型预测未来 8 帧的视觉规划。这一设计将“规划”转化为视频生成问题：模型需要想象完成任务所需的未来视觉状态序列，而非直接输出动作序列。在自改进循环中，该模型是微调的主要对象——每轮迭代在筛选后的成功轨迹上微调 10,000 步（MetaWorld 学习率 1e-6，Panda Arm 抽屉任务 1e-5，推动任务 8,000 步/学习率 2e-5）。

### 逆动力学模型

逆动力学模型（Inverse Dynamics Model, IDM）负责将连续两帧视觉预测转换为可执行的机器人动作。SILVR 提供了两种实现：**MLP-IDM** 取两帧视频的嵌入并直接输出动作预测；**Diffusion-IDM**（DIDM）则基于 **Diffusion Policy**（Chi et al., 2023）构建，以扩散过程建模动作分布。消融实验（Table A11）揭示了关键因果机制：仅微调 IDM 或仅微调视频模型均导致性能快速饱和，同时更新两者对于处理对象和运动高度新颖的任务至关重要——迭代 4 时，全更新（SILVR）达 44.2%，仅更新 IDM 降至 29.8%，不更新 IDM 则仅为 26.8%。

### 逆概率自适应模块

该模块以训练无关的方式，在采样时将通用预训练视频模型与域内模型的分数预测进行组合，增强文本条件泛化能力。其核心公式为：

$$\tilde{\epsilon}_{\mathrm{inv}} = \epsilon_{\mathrm{general}}(\tau_t, t) + \alpha \Bigl( \epsilon_{\mathrm{general}}(\tau_t, t \mid \mathrm{text}) + \gamma \epsilon_{\theta}(\tau_t, t \mid \mathrm{text}) - \epsilon_{\mathrm{general}}(\tau_t, t) \Bigr)$$

其中 $\epsilon_{\mathrm{general}}$ 为大规模预训练模型（SILVR 使用 **AnimateDiff**，约 2B 参数，在 WebVid-10M 上预训练），$\epsilon_{\theta}$ 为域内视频模型，$\gamma$ 控制先验强度，$\alpha$ 为文本引导尺度。该公式的本质是在通用模型的去噪方向上叠加一个“域内修正项”——当 $\gamma > 0$ 时，域内模型的文本条件预测被注入采样过程。真实世界实验中，禁用此先验导致视觉规划器难以改进甚至退化，说明互联网视频先验对于弥合仿真到真实的分布偏移具有决定性作用。

### 自改进循环

自改进循环（Algorithm 1）将上述模块串联为迭代优化流程：每轮迭代采集 30 条轨迹，经稀疏奖励信号（地面真值或 VLM）筛选成功样本，随后同时微调域内视频模型和逆动力学模型。该循环的样本效率优势源于其与 DSRL 的根本差异——DSRL 的性能瓶颈不在于梯度更新步数（Table A7 显示 150 步与 60,000 步更新效果相近），而在于经验收集本身的质量。SILVR 通过视觉规划的动力学解耦，使有限的经验能更有效地转化为模型改进。

## 实验与关键发现

### 核心瓶颈与因果机制

离线训练的视觉规划模型面临两个结构性困难：其一，域内视频模型在未见任务上的泛化能力有限，视觉规划质量随任务分布偏移而急剧下降；其二，基于行为克隆（BC）的在线微调方法（如 BCIL）样本效率低下，而基于扩散策略的强化学习微调方法（DSRL）提升幅度微小。**SILVR 的核心因果杠杆在于将环境动力学建模与动作预测解耦**——视觉规划器仅需学习“环境如何变化”，而非直接映射观测到动作。动力学模型比端到端策略更易迁移，因为它捕捉的是任务无关的物理交互规律。在此基础上，SILVR 通过迭代收集成功轨迹并微调域内视频生成模型，使视觉规划器逐步适应新任务，且整个过程仅需稀疏奖励信号（甚至可由 VLM 提供），无需地面真值奖励函数。

### 主实验结果

#### MetaWorld 仿真基准

**Table 1** 报告了 SILVR 在 12 个未见 MetaWorld 任务上的平均成功率。SILVR（使用地面真值过滤）在第 4 轮迭代时达到 **44.2%（±4.5）**，远超 DSRL 的 **7.7%（±3.4）** 和 BCIL 的 **23.2%（±0.9）**，相对提升分别为 +36.5 和 +21.0 个百分点。SILVR 从第 1 轮起即显著优于所有基线，且性能随迭代单调递增。进一步将最终轮视觉规划器蒸馏为轻量扩散策略（SILVR-Distilled DP）后，平均成功率进一步提升至 **49.2%（±3.4）**，部分任务在蒸馏后反而表现更好。

![[assets/figures/papers/paper_list_l18_https_openreview_net_forum_id_SzUgx5r3wy/figures/002_Table_1.jpg]]
*Table 1: SILVR Results on MetaWorld. We report the average performance over 12 unseen Meta-World tasks for SILVR and all baseline methods, each aggregated over three seeds. We also provide the performance of diffusion policy distilled from the video model from the last SILVR iteration, denoted as “SILVR-Distilled DP”. SILVR outperforms all baselines by a large margin since Iteration 1. Furthermore, SILVR-Distilled DP achieves the best overall performance*

**Figure 4** 展示了 SILVR 在 10 轮迭代中的性能趋势：成功率持续单调递增，但第 5 轮后增益递减并趋于饱和，最终轮（第 9 轮）达到 53.1%。这表明自改进循环的边际收益在约 5 轮后显著收窄，模型可能陷入局部策略最小点。

![[assets/figures/papers/paper_list_l18_https_openreview_net_forum_id_SzUgx5r3wy/figures/011_Figure_4.jpg]]
*Figure 4: SILVR results on MetaWorld for 10 iterations. We report effects of training SILVR on an extended amount of iterations. On the left plot, we show that performance continues to monotonically increase, but with diminishing improvements and effective saturation past iteration 5. On the middle and right plots we visualize a comparison between the final iteration visual planner against its distilled student BC policy from the visual planner across 6 tasks, where we observe that certain tasks actually improve after distillation*

#### 真实世界机器人实验

在 Franka Emika Panda 机械臂的两个真实操作任务上（**Figure 3**），SILVR 结合 AnimateDiff 互联网视频先验后展现出持续的迭代改进趋势：

![[assets/figures/papers/paper_list_l18_https_openreview_net_forum_id_SzUgx5r3wy/figures/009_Figure_3.jpg]]
*Figure 3: SILVR Results in comparison to Behavior Cloning Improvement Loop (BCIL). We report the average performance over 12 unseen MetaWorld tasks, as well as novel pushing and drawer opening tasks for Panda arm experiments across several iterations of self-improvement (x-axis). Numbers in the graph correspond to success rate achieved (y-axis)*

- **推杯子任务**（两种未见颜色）：SILVR 成功率从低起点持续提升至约 40-50%（图中估值），而 BCIL 提升缓慢。
- **开抽屉任务**（一种未见颜色）：SILVR 借助互联网视频先验成功启动初始视觉规划性能，多轮后持续提升，显著优于 BCIL。

关键发现：若禁用互联网视频先验，SILVR 在真实世界任务中难以改进甚至退化；但在 MetaWorld 仿真中，有无先验的差距不明显。这说明**互联网预训练视频模型提供的视觉先验对于弥合仿真到真实世界的分布偏移至关重要**。

### 消融实验

#### 数据过滤信号

**Figure 5** 和 **Table 1** 表明，将数据过滤信号从地面真值替换为视觉语言模型（VLM，如 GPT-5、Gemini）后，SILVR 仍能迭代改进，但最终性能略低（VLM 过滤：38.4% vs GT 过滤：44.2%）。这验证了框架不依赖精确人工奖励信号——VLM 提供的稀疏、带噪反馈足以驱动自改进。

![[assets/figures/papers/paper_list_l18_https_openreview_net_forum_id_SzUgx5r3wy/figures/013_Figure_5.jpg]]
*Figure 5: Ablations on data filtering. We compare the effect filtering has on success rate (yaxis) across iterations of finetuning (x-axis), on both MetaWorld (5a) and Panda arm (5b) setups. On MetaWorld (left plot), we further report accuracy when filtering is performed by a VLM. We observe SILVR consistently improves task even without access to ground-truth filtering signals*

#### 组件更新策略

**Table A11** 的消融揭示了各组件对自改进的贡献：
- 同时微调视频模型和逆动力学模型（IDM）：**44.2%**
- 仅微调 IDM：**29.8%**
- 不微调 IDM（仅微调视频模型）：**26.8%**

仅更新单一组件会导致性能快速饱和；对于对象和运动模式高度新颖的任务，**同时更新视频模型和 IDM 是必要的**。

#### 域内数据质量

**Figure 6** 和 **Table A9** 展示了 SILVR 对初始数据质量的鲁棒性。当初始域内数据仅含 30% 专家动作（70% 随机动作）时，SILVR 仍能成功自改进，平均成功率从 **9.5% 提升至 41.0%**。论文将此归因于分数组合机制——次优演示仍能传递有用的视觉信息、有效运动模式和交互动力学。值得注意的是，部分任务（如 Faucet Close、Plate Slide）在次优初始化下几乎无法改进，说明某些任务对初始数据质量更为敏感。

#### 样本效率对比

**Table A7** 表明 DSRL 的性能瓶颈不在于梯度更新步数——将每轮更新步数从 150 增至 60000，DSRL 的成功率仍维持在 7-10% 的低位且无明显提升趋势。这反衬出 SILVR 的样本效率优势：通过视觉规划解耦动力学学习，SILVR 能更有效地利用有限的自采集经验。

### 失败模式与局限性

1. **真实世界无先验退化**：在真实机器人任务中，若无互联网视频先验（AnimateDiff），自改进效果大幅下降甚至退化。这表明域内视频模型本身在真实世界视觉多样性面前的泛化能力不足。
2. **迭代饱和**：自改进循环约在 5 轮后饱和，缺乏主动探索机制使模型可能陷入局部策略最小点，无法发现更优的行为模式。
3. **长时序任务依赖手工分解**：当前长时序任务（如按顺序推杯子，**Figure A16/A17**）依赖手工子任务分解，未实现端到端自改进。
4. **推理计算开销**：视觉规划在推理时因视频生成计算开销较大，虽可通过蒸馏为轻量策略弥补，但蒸馏后的性能提升有限且增加了工程复杂度。
5. **环境多样性有限**：当前实验主要基于 MetaWorld 仿真和两个简单真实操作任务，泛化到更复杂、多样化的环境仍需验证。

### 开放问题

- 如何将可控探索引入视觉规划框架，以克服迭代饱和并发现更优策略？
- 能否利用视频生成模型的随机性，在微调过程中生成更多样化的规划以提升自改进鲁棒性？
- SILVR 框架能否与高效的子任务分割机制无缝结合，从而处理任意复杂的长时序任务？
- 在使用 VLM 作为奖励信号时，如何量化和减少其固有偏差及噪声对自改进的影响？

![[assets/figures/papers/paper_list_l18_https_openreview_net_forum_id_SzUgx5r3wy/figures/029_Table_11.jpg]]
*Table 11: Table A11: Component Update Ablations. We report the mean success rate and standard deviation across 12 unseen tasks, aggregated over 3 seeds each*

## 定位与知识库关联

### 核心瓶颈与因果机制

离线训练的视觉规划模型面临一个根本性瓶颈：在未见任务上泛化能力有限，而直接对策略进行在线强化微调（如 **DSRL**，Wagenmaker et al., 2025）的样本效率极低，提升幅度微小。SILVR 通过一个关键的因果调节变量——迭代收集成功轨迹并微调域内视频生成模型——使视觉规划器逐步适应新任务，从而绕开这一瓶颈。

其核心洞察在于：视觉规划将环境动力学建模与动作预测解耦。动力学模型（视频生成）描述“世界如何变化”，这一知识在不同任务间更具迁移性；而动作预测（逆动力学模型）则是任务特定的。结合自适应的微调循环，SILVR 实现了样本高效的自改进，且无需地面真值奖励函数即可工作。

### 训练范式的根本转变

传统视觉规划方法（如 **AVDC**，Ko et al., 2024）采用纯离线训练范式，模型部署后不再更新。SILVR 将范式转变为在线迭代微调：每轮自采集 30 条轨迹，经稀疏奖励过滤后，同时微调域内视频模型与逆动力学模型（Algorithm 1）。这一转变使得模型能够从自身经验中持续学习，而非仅仅依赖固定的离线数据集。

与基于行为克隆的自改进基线 **BCIL**（使用 **Diffusion Policy**，Chi et al., 2023 作为底层策略）相比，SILVR 的样本效率优势显著。在 MetaWorld 12 个未见任务上，迭代 4 后 SILVR 平均成功率达 44.2%，远超 BCIL 的 23.2%（Table 1）。BCIL 直接克隆成功轨迹中的动作，而 SILVR 通过视频生成模型学习环境动力学，能够更充分地利用有限的经验数据。

与基于扩散策略的强化学习微调方法 **DSRL** 相比，差距更为悬殊——DSRL 在相同条件下仅达 7.7%。消融实验揭示，DSRL 的性能瓶颈不在于梯度更新步数（将更新步数从 150 增至 60,000 步，性能几乎无变化，Table A7），而在于经验收集的效率。这进一步验证了视觉规划解耦策略在样本效率上的结构性优势。

### 大规模先验的利用策略

SILVR 的一个关键创新在于可选地引入互联网预训练视频模型作为先验。通过逆概率自适应（IPA），将通用预训练模型 **AnimateDiff**（Guo et al., 2023，约 2B 参数，预训练于 WebVid-10M）与域内模型的分数预测进行组合采样：

$$
\tilde{\epsilon}_{\mathrm{inv}} = \epsilon_{\mathrm{general}}(\tau_t, t) + \alpha \Bigl( \epsilon_{\mathrm{general}}(\tau_t, t \mid \mathrm{text}) + \gamma \epsilon_{\theta}(\tau_t, t \mid \mathrm{text}) - \epsilon_{\mathrm{general}}(\tau_t, t) \Bigr)
$$

其中 $\gamma$ 为先验强度，$\alpha$ 为文本引导尺度。这一训练无关的组合机制使得域内模型能够借助互联网规模数据中习得的视觉先验，显著提升在真实世界场景中的泛化能力。

真实世界实验验证了这一设计的必要性：在 Panda 机械臂的推杯子和开抽屉任务中，若禁用互联网视频先验，SILVR 难以改进甚至性能退化；而在仿真环境（MetaWorld）中，这一差距不明显（Figure 3）。这表明，当域内数据有限且视觉复杂度较高时，大规模先验对于自改进循环的成功启动至关重要。

### 数据过滤信号的灵活性

SILVR 不依赖精确的人工定义奖励函数。框架利用稀疏奖励信号筛选成功轨迹，且这一信号可以来自地面真值或视觉语言模型（如 GPT-5、Gemini 等）。实验表明，将过滤信号从地面真值换为 VLM 后，SILVR 仍能迭代改进，尽管最终性能略低于使用地面真值（Table 1：VLM Filter 38.4 vs GT 44.2；Figure 5a）。这一特性使得 SILVR 在缺乏精确奖励工程的实际场景中具有更广泛的适用性。

### 组件协同更新的必要性

SILVR 的自改进依赖于域内视频模型与逆动力学模型（IDM）的协同微调。消融实验（Table A11）表明：仅微调 IDM 或仅微调视频模型均导致性能很快饱和；同时更新两者对于处理对象和运动高度新颖的任务至关重要（同时微调 44.2 > 仅微调 IDM 29.8 > 不微调 IDM 26.8）。这验证了视觉规划解耦设计的另一层优势：动力学建模与动作预测虽可分离训练，但在自改进过程中需要协同进化。

### 适用边界与局限性

1. **真实世界先验依赖**：在真实机器人任务中，若无互联网视频先验，自改进效果大幅下降。这意味着 SILVR 在视觉分布与互联网数据差距极大的特殊环境中可能难以启动。

2. **迭代饱和**：自改进循环约在 5 轮后饱和，性能增益递减（Figure 4 左图）。缺乏探索机制使得模型可能陷入局部策略最小点，无法发现更优的行为模式。这是当前框架的结构性局限。

3. **推理效率与蒸馏权衡**：视觉规划在推理时因视频生成计算开销较大。虽可蒸馏为轻量扩散策略（SILVR-Distilled DP）以提升推理效率，且蒸馏后部分任务性能甚至有所提升（Figure 4 中、右图），但这一增益并非普遍保证。

4. **环境泛化待验证**：当前实验主要基于 MetaWorld 仿真和两个简单真实操作任务（推杯子、开抽屉），在更复杂、多样化的真实环境中是否仍能有效自改进，仍需进一步验证。

5. **长时序任务依赖手工分解**：对于长时序任务（如按顺序推多个杯子），SILVR 目前依赖手工子任务分解，未实现端到端自改进。

### 开放问题

- 如何将可控制的探索引入视觉规划框架，以克服迭代饱和并发现更优策略？当前框架缺乏内在的探索机制，模型倾向于重复已有行为模式。

- 能否利用视频生成模型固有的随机性，在微调过程中生成更多样化的视觉规划，从而提升自改进的鲁棒性和上限？

- SILVR 框架能否与高效的子任务分割机制无缝结合，从而处理任意复杂的长时序任务？这需要将自改进循环从单任务扩展到任务层次结构。

- 在使用 VLM 作为奖励信号时，如何量化和减少其固有的偏差及噪声对自改进的影响？VLM 过滤引入了新的不确定性来源，其长期效应尚不明确。

## 原文 PDF

![[paperPDFs/ICLR_2026/Self_Improving_Loops_for_Visual_Robotic_Planning.pdf]]
