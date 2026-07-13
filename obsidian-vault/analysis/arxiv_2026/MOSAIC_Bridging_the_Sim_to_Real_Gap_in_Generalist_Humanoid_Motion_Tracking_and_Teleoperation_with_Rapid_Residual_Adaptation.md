---
title: "MOSAIC: Bridging the Sim-to-Real Gap in Generalist Humanoid Motion Tracking and Teleoperation with Rapid Residual Adaptation"
type: paper
paper_level: A
venue: arXiv
year: 2026
pdf_ref: paperPDFs/arxiv_2026/MOSAIC_Bridging_the_Sim_to_Real_Gap_in_Generalist_Humanoid_Motion_Tracking_and_Teleoperation_with_Rapid_Residual_Adaptation.pdf
project_link: null
code_link: https://github.com/lcm-proj/lcm
aliases:
- MOSAIC
tags:
- arxiv_2026
- topic/vision_multimodal_applications
- topic/benchmarks_datasets_evaluation
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: 残余适配器：通过在冻结的通用跟踪器上添加可训练的残余模块，实现小样本接口特定的快速适应，在保持通用性的同时有效补偿接口偏移。
primary_logic: 针对遥操作的实际需求，单一通用运动跟踪器不足以应对接口特定误差；引入以世界坐标系运动一致性为重点的奖励设计，并通过残余蒸馏将接口适应能力与广泛运动知识解耦，可在不牺牲通用性的前提下显著提升实际部署的鲁棒性和长期稳定性。
claims:
- 遥操作VR数据集上，Adapter (W) 在全局锚点位置误差 E_AP 上从基础模型的 2.9352 m 降至 1.1940 m，大幅提升跟踪精度。
- 多源数据（5-Sources）相比单源数据在OOD测试集上一致提升跟踪保真度和鲁棒性。
- 加入世界坐标系追踪奖励显著降低长期漂移，提升成功率和平均步数。
- 残差适配器在保持通用运动跟踪能力的同时，优于微调和连续学习。
---

# MOSAIC: Bridging the Sim-to-Real Gap in Generalist Humanoid Motion Tracking and Teleoperation with Rapid Residual Adaptation

> [!tip] 核心洞察
> 针对遥操作的实际需求，单一通用运动跟踪器不足以应对接口特定误差；引入以世界坐标系运动一致性为重点的奖励设计，并通过残余蒸馏将接口适应能力与广泛运动知识解耦，可在不牺牲通用性的前提下显著提升实际部署的鲁棒性和长期稳定性。

| 字段 | 内容 |
|------|------|
| 中文题名 | MOSAIC：通过快速残差适应弥合通用人形运动跟踪与遥操作的仿真到现实差距 |
| 英文题名 | MOSAIC: Bridging the Sim-to-Real Gap in Generalist Humanoid Motion Tracking and Teleoperation with Rapid Residual Adaptation |
| 会议/期刊 | arXiv 2026 |
| Links | [paper](https://arxiv.org/abs/2602.08594v2) · [Code](https://github.com/lcm-proj/lcm) · [paper](https://arxiv.org/abs/2511.04831) |
| Topic | #topic/vision_multimodal_applications #topic/benchmarks_datasets_evaluation #topic/vision_multimodal_applications/image_and_video_generation |
| Method | MOSAIC |
| Dataset | VR teleoperation dataset, Motion-X-Sub |

> [!tip] 效果简介
> - VR teleoperation dataset 上，E_AP (m) ↓ 1.1940 vs 2.9352 (-1.7412)。
> - Motion-X-Sub (OOD general motions) 上，Success Rate ↑ 77.25% vs 77.88% (-0.63%)。

## 概要

**问题**：通用人形运动跟踪策略在仿真环境中表现优异，但部署到真实遥操作场景时，接口相关的延迟（VR约0.4 s，惯性动捕约0.2 s）、噪声和抖动导致显著的仿真到现实（Sim-to-Real）域差距。这使通用跟踪器出现漂移、接触中断和长期不稳定，而非运动多样性不足。

**核心洞察**：单一通用运动跟踪器不足以应对接口特定误差。MOSAIC通过冻结通用跟踪器主干、添加可训练的残差模块，实现小样本接口特定的快速适应，在保持通用性的同时有效补偿接口偏移。其关键设计在于以世界坐标系运动一致性为重点的奖励设计，以及通过残差蒸馏将接口适应能力与广泛运动知识解耦。

**方法定位**：MOSAIC是一个统一的训练-部署流水线，包含多源数据加载与预处理、两级自适应重采样、通用运动跟踪策略训练（π_GMT）、接口特定适应策略训练（π_ADAPT）、运动条件残差适配器蒸馏（π_RES），以及RobotBridge模块化部署框架。残差适配器采用近零权重初始化，通过双教师蒸馏损失（加权MSE）同时学习适应域和通用域的知识。

**主要结果**：在VR遥操作数据集上，Adapter (W) 将全局锚点位置误差 E_AP 从基础模型的2.9352 m降至1.1940 m（Table V）。在OOD通用运动测试集Motion-X-Sub上，残差适配器保持77.25%成功率，仅比通用跟踪器下降0.63个百分点，而微调（Fine-tuning）和连续学习（Continual Learning）分别降至40.60%和显著退化（Table IV）。多源数据（5-Sources）一致优于单源数据，世界坐标系奖励显著降低长期漂移。30分钟遥操作数据即可达到有效适配，3分钟不足，FLD数据增强效果有限（Table VI）。

**局限与展望**：MOSAIC仍依赖可靠的低延迟感知和状态估计，残差适应主要针对接口偏移而非所有仿真到现实不匹配（如动力学建模误差）。当前适配器为单一接口训练，多接口间的迁移能力未充分验证，长时遥操作（>10分钟）的稳定性极限仍需进一步研究。

### 人形机器人运动跟踪与遥操作的双重挑战

人形机器人运动跟踪旨在驱动真实机器人复现给定的参考运动序列，是实现通用运动技能复用的核心技术路径。近年来，基于强化学习（RL）的通用运动跟踪器（General Motion Trackers）在仿真环境中取得了显著进展，能够跟踪涵盖行走、奔跑、跳跃、踢腿等多样化动作的大规模运动数据集。然而，当这些跟踪器被部署到真实遥操作场景时，一个关键瓶颈浮现：**仿真到现实（Sim-to-Real）的域差距并非主要源于运动多样性不足，而是由遥操作接口引入的延迟、噪声和抖动所导致**。具体而言，VR遥操作系统的端到端延迟约0.4秒，惯性动作捕捉系统约0.2秒，这种接口特异性误差会使通用跟踪器在真实部署中发生漂移、接触中断和长期不稳定。

现有方法存在明显的结构性缺口。一方面，通用运动跟踪器（如**GMT**和**TWIST**）在仿真指标上表现饱和，但缺乏对遥操作接口特性的建模，直接部署时性能急剧退化。另一方面，简单的微调（Fine-tuning）策略虽然能在适配数据上获得局部改善，却会导致对通用运动能力的灾难性遗忘——在Motion-X-Sub通用测试集上，微调方法的成功率从77.88%骤降至40.60%，暴露出过拟合小样本遥操作数据的根本缺陷。连续学习（Continual Learning）试图在保留原有语料的同时混合遥操作数据继续训练，但同样无法在通用性与接口特异性之间取得平衡。

### 核心洞察：接口适应与通用能力的解耦

MOSAIC的核心洞察在于认识到：**遥操作部署中的性能退化本质上是接口特定的偏移问题，而非通用运动跟踪能力的缺失**。因此，理想的解决方案应当在不牺牲广泛运动知识的前提下，以最小的数据和计算代价实现针对特定接口的快速适应。这一洞察直接催生了MOSAIC的残差适配范式——将通用运动跟踪能力冻结在基础策略中，通过可训练的轻量残差模块专门补偿接口偏移，从而实现通用性与适应性的解耦。

### 本文动机与目标

针对上述挑战，MOSAIC提出了一套完整的训练-适应-部署流水线，旨在回答三个关键问题：

1. **如何训练一个面向遥操作的通用运动跟踪器？** 通过引入世界坐标系运动一致性奖励和两级自适应重采样策略，使基础跟踪器具备更强的全局稳定性，为后续适应奠定坚实基础。

2. **如何以最小的数据和计算代价实现接口特定适应？** 通过残差适配器蒸馏框架，仅需约30分钟的遥操作数据即可完成接口适应，同时保持通用运动跟踪能力几乎无损（成功率仅下降0.63个百分点）。

3. **如何在真实机器人上实现鲁棒且可移植的部署？** 通过RobotBridge标准化部署框架，统一策略推理、仿真/机器人后端和底层控制器的接口，支持离线运动回放和在线遥操作的无缝切换。

## 核心方法与创新机理

MOSAIC 的核心创新在于提出了一套**残差适应框架**，将通用运动跟踪能力与遥操作接口特异性需求解耦，从而在保持广泛运动泛化能力的同时，实现针对特定遥操作接口的快速、小样本适应。这一框架围绕四个关键设计展开，形成从数据到策略再到部署的完整创新链条。

### 1. 适应策略：冻结主干 + 残差蒸馏

传统的微调（Fine-tuning）或连续学习（Continual Learning）方法在适应遥操作数据时，会不可避免地覆盖通用运动跟踪策略中已学到的广泛运动知识，导致灾难性遗忘。MOSAIC 的核心策略创新在于**冻结通用运动跟踪器（π_GMT）的主干网络**，仅在其上添加一个可训练的轻量残差模块（π_RES），构成学生策略：

$$\pi_{S}(\mathbf{o}_{t}) = \pi_{GMT}(\mathbf{o}_{t}) + \pi_{RES}(\mathbf{o}_{t})$$

这一设计的深层逻辑是：遥操作接口引入的误差（延迟、噪声、抖动）表现为对通用策略输出的**系统性偏移**，而非对运动语义的根本性改变。残差模块只需学习这一偏移量，即可在保持通用性的前提下补偿接口特异性误差。蒸馏过程采用**双教师（π_ADAPT 和 π_GMT）加权均方误差损失**：

$$\mathcal{L}_{\mathrm{distill}} = \sum_{k\in\{\mathrm{ADAPT, GMT}\}} w_{k} \mathbb{E}\left[\left\| \pi_{S}(\mathbf{o}_{t}) - \pi_{(k)}(\mathbf{o}_{t}) \right\|_{2}^{2}\right]$$

其中 π_ADAPT 是在少量遥操作数据上专门训练的接口特定策略，π_GMT 是通用跟踪策略。通过调节权重 w_k，可在接口适应与通用能力保持之间取得平衡。为确保残差模块初始时不影响通用策略的行为，其最后一层采用**近零权重增益和零偏置初始化**，使初始输出接近零向量。

**决定性证据**：在 VR 遥操作数据集上，Adapter (W) 将全局锚点位置误差 E_AP 从基础模型的 2.9352 m 降至 1.1940 m（Table V），降幅达 59.3%。同时，在 OOD 通用运动测试集 Motion-X-Sub 上，Adapter (W) 的成功率仅从 77.88% 微降至 77.25%（Table IV），降幅仅 0.63%，远优于微调（40.60%）和连续学习（表中对应行），证明残差适应在提升遥操作性能的同时有效避免了灾难性遗忘。

### 2. 奖励设计：世界坐标系运动一致性

通用运动跟踪器通常仅在机器人本体坐标系下定义追踪奖励，这在仿真中足以获得高指标，但在真实遥操作中会导致**长期漂移**——机器人逐渐偏离世界坐标系下的绝对位置，最终失去平衡或脱离接触。MOSAIC 在奖励设计中**引入世界坐标系追踪项**（包括全局锚点位置、全局速度等），直接约束机器人在世界系下的运动一致性。

这一设计的因果机制在于：本体坐标系奖励只能保证局部姿态匹配，无法感知全局累积误差；世界坐标系奖励为策略提供了绝对空间参考，迫使策略主动纠正漂移趋势。此外，奖励设计还融合了遥操作专属项（如接触稳定性、步态自然度），形成对遥操作场景的针对性优化。

**决定性证据**：消融实验（Fig. 3b）表明，加入世界坐标系追踪奖励后，全局追踪误差显著降低，成功率与平均步数均提升。这一结果与 Table V 中 Adapter (W) 相对基础模型的巨大提升相互印证——世界坐标系奖励是通用跟踪器本身鲁棒性的基础，残差适配器则在此基础上进一步补偿接口特异性偏移。

### 3. 数据采样：两级自适应重采样

多源运动数据的规模和质量直接影响通用跟踪器的泛化能力。MOSAIC 提出了**两级自适应重采样策略**，在运动级和帧内两个粒度上优化数据利用效率：

- **运动级**：基于混合分布分配采样权重，综合考虑运动的失败率（优先采样困难运动）、新颖性（鼓励多样性探索）和均匀性（防止过拟合），使训练聚焦于策略的薄弱环节。
- **帧内**：采用失败感知的指数移动平均（EMA）平滑采样，在运动片段内部优先采样失败帧附近的区域，同时通过平滑避免采样过于集中。

这一设计与残差适应框架形成互补：多源数据 + 自适应采样赋予通用跟踪器广泛的运动知识，残差模块则在此坚实基础上进行轻量适配。

**决定性证据**：Fig. 3a 显示，5-Sources 多源数据相比单源数据在 OOD 测试集上一致提升了跟踪保真度和鲁棒性，验证了数据多样性的关键作用。

### 4. 接口特异性处理：即插即用的接口适应

MOSAIC 的残差适配器实现了**接口特异性处理与通用运动知识的彻底解耦**。训练流程分为两阶段：

1. **通用阶段**：在大规模多源数据上训练 π_GMT，不涉及任何遥操作接口。
2. **适应阶段**：在少量（约 30 分钟）遥操作数据上训练接口特定的 π_ADAPT，再通过蒸馏将其知识压缩到残差模块 π_RES 中。

这种设计使残差模块成为**即插即用的接口适配器**：更换遥操作设备时，只需用新接口的数据重新训练残差模块，无需触碰通用跟踪器主干。Table VI 的数据扩展分析表明，30 分钟遥操作数据即可达到最佳适配效果（3 分钟不足），而 FLD 数据增强的收益有限，说明残差模块主要学习的是接口的**系统性误差模式**（如延迟、噪声分布），而非运动多样性。

**决定性证据**：Table V 中 Adapter (W) 相对 Fine-tuning 的巨大优势（E_AP 1.1940 vs 微调对应值）直接证明了残差解耦策略的有效性。Fig. S5 进一步揭示，VR 遥操作的端到端延迟约 0.4 s，惯性动捕约 0.2 s，接口延迟是影响稳定性的主要因素——这正是残差模块需要补偿的核心域差距。

### 创新点总结

| 创新维度 | 基线做法 | MOSAIC 方案 | 核心收益 |
|---------|---------|------------|---------|
| 适应策略 | 微调或连续学习，覆盖通用知识 | 冻结主干 + 残差蒸馏，双教师约束 | 遥操作性能提升 59%，通用能力保持 99%+ |
| 奖励设计 | 仅机器人坐标系追踪 | 加入世界坐标系追踪 + 遥操作专属项 | 显著降低长期漂移，提升稳定性 |
| 数据采样 | 均匀采样或简单失败重采样 | 两级自适应：运动级混合分布 + 帧内失败感知平滑 | 多源数据 OOD 泛化一致提升 |
| 接口处理 | 无特殊化，通用策略直接部署 | 接口特定策略蒸馏到残差模块，即插即用 | 30 分钟数据完成适配，更换接口无需重训主干 |

**需注意的局限**：残差适应主要针对接口偏移（延迟、噪声、抖动），不能解决所有仿真到现实的差距（如动力学建模误差）。当前系统在单一接口上训练适配器，不同接口间的迁移能力未充分验证。在长时遥操作（>10 分钟）中，积累的微小残差误差仍可能导致缓慢漂移，需要进一步研究。

MOSAIC 构建了一条统一的训练–部署流水线，使单一人形机器人策略能够同时支持离线运动回放和在线全身遥操作两种模式。如图 2 所示，系统在逻辑上分为训练/仿真侧和部署/真实机器人侧，两端通过 RobotBridge 框架桥接，实现一致的策略推理与跨平台移植。

**训练侧**的入口是多源运动数据的聚合与预处理。系统从光学动捕、惯性动捕、公开数据集及生成数据中收集异构运动序列，统一重定向至目标机器人的关节空间（Sec. IV-A, Table I）。随后，两级自适应重采样模块（Sec. IV-B）在运动级别按失败率、新颖性和均匀分布的混合策略分配采样权重，在帧级别采用失败感知的指数滑动平均平滑采样，从而在充分利用数据的同时聚焦困难运动段。

重采样后的数据驱动两个策略的训练。首先是通用运动跟踪策略 **π_GMT**（Sec. V-A a），采用不对称 PPO 在大规模多源数据上训练，其奖励设计在传统机器人坐标系跟踪项之外，显式加入世界坐标系跟踪项（如全局锚点位置、速度等），以抑制长期漂移（Table III, Fig. 3b）。其次是适应运动跟踪策略 **π_ADAPT**（Sec. V-A b），仅在少量遥操作数据（约 30 分钟）上训练，专门捕捉特定接口的噪声、延迟和步态特征。

两个教师策略训练完成后，进入运动条件残差适配器蒸馏阶段（Sec. V-B）。学生策略定义为冻结的通用跟踪器与可训练残差模块的加和：

$$\pi_{S}(\mathbf{o}_{t}) = \pi_{\mathrm{GMT}}(\mathbf{o}_{t}) + \pi_{\mathrm{RES}}(\mathbf{o}_{t})$$

蒸馏损失为双教师加权均方误差：

$$\mathcal{L}_{\mathrm{distill}} = \sum_{k\in\{\mathrm{ADAPT, GMT}\}} w_{k} \mathbb{E}\left[\left\| \pi_{S}(\mathbf{o}_{t}) - \pi_{(k)}(\mathbf{o}_{t}) \right\|_{2}^{2}\right]$$

残差模块采用近零权重增益和零偏置初始化，确保初始输出接近零，蒸馏初期行为与通用跟踪器一致。这一设计将接口适应能力与广泛运动知识解耦——通用主干保持冻结以保留运动多样性，残差模块仅学习接口特定的偏移补偿。

**部署侧**，最终策略以 50 Hz 输出关节目标位置，由底层 PD 控制器执行：

$$\tau_{t} = K_{p}(q_{t}^{des} - q_{t}) + K_{d}(\dot{q}_{t}^{des} - \dot{q}_{t})$$

策略仅消费下一帧参考运动（单步前瞻），不依赖多步未来窗口，满足在线遥操作的实时性要求。RobotBridge 框架标准化了策略推理、仿真/机器人后端与底层控制器之间的接口，支持离线回放与在线遥操作的无缝切换，以及跨仿真器（Isaac Lab、MuJoCo）和真实机器人平台的移植（Sec. K, L, M）。

**关键因果机制**：通用跟踪器在大规模多源数据上获得了丰富的运动先验，但在真实遥操作中因接口延迟（VR 端到端约 0.4 s，惯性动捕约 0.2 s，Fig. S5）、噪声和抖动而产生域偏移；残差适配器通过冻结主干、仅蒸馏接口特定的修正量，在保持通用性的前提下快速补偿这些偏移。决定性证据来自 Table V：Adapter (W) 在 VR 遥操作数据集上将全局锚点位置误差 $E_{AP}$ 从基础模型的 2.9352 m 降至 1.1940 m，同时 Table IV 显示其在 OOD 通用运动集上的成功率（77.25%）与基础模型（77.88%）几乎持平，验证了“适应不牺牲通用性”的核心设计目标。

### 补充图表

![[assets/figures/papers/paper_list_l53_https_arxiv_org_abs_2602_08594v2/figures/003_Figure_2.jpg]]
*Figure 2: MOSAIC System Overview. MOSAIC consists of a unified training–deployment pipeline for humanoid motion tracking and teleoperation. Training/Simulation aggregates heterogeneous multi-source motions, two-level adaptive resampling, policy training process, yielding a deployable policy that preserves generality while improving real-robot robustness. Deployment/Real Robot supports both offline motion replay and online teleoperation. Finally, RobotBridge provides a modular interface that enables consistent evaluation and portable deployment across platforms*

![[assets/figures/papers/paper_list_l53_https_arxiv_org_abs_2602_08594v2/figures/001_Figure_1.jpg]]
*Figure 1: MOSAIC in Action. MOSAIC enables a single humanoid policy to operate in two modes: offline motion replay (top) and online whole-body teleoperation from multiple wearable interfaces (bottom). In offline replay, the robot robustly tracks diverse and highly dynamic reference motions—walking, running, kicking, kungfu-style strikes, jumping, and squatting. In online teleoperation, MOSAIC faithfully mirrors real-time human motion streams and supports challenging contact-rich and high-agility behaviors, including mid-air jump turns, single-leg support, and jump-shot–style movements*

### 3.1 控制基础：关节空间PD控制

MOSAIC的策略输出目标关节位置 $q_t^{des} \in \mathbb{R}^{29}$，由底层PD控制器转换为关节力矩命令：

$$
\tau_{t} = K_{p}(q_{t}^{des} - q_{t}) + K_{d}(\dot{q}_{t}^{des} - \dot{q}_{t})
$$

其中 $\tau_t$ 为关节力矩，$q_t$ 和 $\dot{q}_t$ 分别为当前关节位置与速度，$K_p$ 和 $K_d$ 为比例和微分增益。该控制器以50 Hz频率执行，策略仅消耗下一帧参考姿态（单步前瞻），而非多步未来窗口。

### 3.2 策略参数化与观测空间

策略网络采用MLP架构，隐藏层维度为 $[1024, 1024, 512, 256]$，激活函数为ELU。采用非对称Actor-Critic结构：Actor使用Prop观测栈（含5步历史），Critic额外访问特权状态信息（Priv项）。具体观测项与噪声配置见Table II，奖励项与权重见Table III。

### 3.3 通用运动跟踪策略训练：$\pi_{\text{GMT}}$

第一阶段训练通用运动跟踪策略 $\pi_{\text{GMT}}$，核心设计要点：

- **多源数据聚合**：融合光学动捕、惯性动捕、公开数据集及生成数据，统一重定向至机器人运动空间（Table I）。
- **两级自适应重采样**：运动级分配基于失败率、新颖性及均匀分布的混合分布；帧内采用失败感知的EMA平滑采样，在平衡数据利用的同时聚焦困难片段。
- **世界坐标系追踪奖励**：在传统机器人坐标系追踪奖励基础上，加入全局位置、速度等遥操作导向项，显著降低长期漂移（Fig. 3b）。

训练采用非对称PPO，在Isaac Lab框架下使用8块NVIDIA A100 GPU并行训练约48小时，每GPU实例化30,000个环境。

### 3.4 接口特定适应策略训练：$\pi_{\text{ADAPT}}$

第二阶段在少量遥操作数据上训练接口特定策略 $\pi_{\text{ADAPT}}$，捕捉设备噪声、延迟特征及步态偏移。该策略与 $\pi_{\text{GMT}}$ 共享网络架构但独立训练，作为后续蒸馏的领域教师。

### 3.5 运动条件残差适配器蒸馏：$\pi_{\text{RES}}$

核心创新在于通过残差蒸馏实现即插即用的接口适应，同时保持通用运动跟踪能力。

**学生策略合成**：学生策略 $\pi_S$ 定义为冻结的通用跟踪策略与残差适配器输出的加和：

$$
\pi_{S}(\mathbf{o}_{t}) = \pi_{\text{GMT}}(\mathbf{o}_{t}) + \pi_{\text{RES}}(\mathbf{o}_{t})
$$

其中 $\pi_{\text{GMT}}$ 权重完全冻结，仅训练轻量残差模块 $\pi_{\text{RES}}$。

**双教师蒸馏损失**：最小化学生策略与两个领域教师策略（通用领域 $\pi_{\text{GMT}}$ 和适配领域 $\pi_{\text{ADAPT}}$）的加权均方误差：

$$
\mathcal{L}_{\mathrm{distill}} = \sum_{k\in\{\mathrm{ADAPT, GMT}\}} w_{k} \mathbb{E}\left[\left\| \pi_{S}(\mathbf{o}_{t}) - \pi_{(k)}(\mathbf{o}_{t}) \right\|_{2}^{2}\right]
$$

其中 $w_{\text{ADAPT}}$ 和 $w_{\text{GMT}}$ 为领域权重，平衡接口适应与通用性保持。

**零偏置残差初始化**：$\pi_{\text{RES}}$ 的末层权重以接近零的增益初始化，偏置置零，确保初始输出接近零向量，使学生策略在训练初期近似等价于 $\pi_{\text{GMT}}$，避免灾难性遗忘。

### 3.6 部署框架：RobotBridge

RobotBridge提供标准化的策略推理、仿真/机器人后端及底层控制器之间的接口抽象，支持离线运动回放与在线遥操作的无缝切换，并实现跨平台可移植部署（Fig. 2）。

### 补充图表

![[assets/figures/papers/paper_list_l53_https_arxiv_org_abs_2602_08594v2/figures/005_Figure.jpg]]
*Figure: (a) Quantitative Comparison of Data Source. (b) Quantitative Ablation of Reward Design and Training Paradigms Alongside Benchmarking with Prior Work*

## 实验与关键发现

### 实验设置

所有策略均基于 **Isaac Lab** 框架训练，使用 8 块 NVIDIA A100 GPU，每块 GPU 并行运行 30,000 个环境，总训练时间约 48 小时。策略网络采用 MLP 架构，隐藏层结构为 [1024, 1024, 512, 256]，激活函数为 ELU。底层控制通过关节空间 PD 控制器实现，策略以 50 Hz 频率输出关节目标位置：

$$\tau_{t} = K_{p}(q_{t}^{des} - q_{t}) + K_{d}(\dot{q}_{t}^{des} - \dot{q}_{t})$$

评估指标涵盖跟踪保真度与鲁棒性两个维度。保真度指标包括全局锚点位置误差 $E_{AP}$、锚点线速度误差 $E_{AV}$、身体位置误差 $E_{BP}$、身体线速度误差 $E_{BV}$ 和末端执行器位置误差 $E_{EP}$，均在世界坐标系下计算。鲁棒性指标包括成功率（Success Rate）和平均 episode 步数（Average Steps per Episode）。通用运动跟踪能力的基准测试采用 **Motion-X-Sub**，这是从 Motion-X 数据集中筛选出的 OOD 子集，包含 633 个序列，平均时长 19.04 秒，总计约 3.35 小时，经过物理合理性筛选。遥操作适配能力在 VR 遥操作数据集上评估，该数据集与训练所用接口错配，以测试适应能力。

对比基线包括通用运动跟踪器 **GMT**、遥操作系统 **TWIST**，以及直接微调（Fine-tuning）和连续学习（Continual Learning）两种消融基线。所有策略使用相同的 PPO 超参数、网络架构和训练环境以保证公平性。

### 通用运动跟踪能力保持

Table IV 展示了各方法在 Motion-X-Sub 上的通用运动跟踪能力。MOSAIC 的 Adapter (W) 变体成功率为 77.25%，与基础通用跟踪器（Base Model）的 77.88% 几乎持平（仅下降 0.63%），表明残差适配器在引入接口特定适应后**几乎不损害通用运动跟踪能力**。相比之下，直接微调（Fine-tune）成功率骤降至 40.60%，连续学习（Continual Learning）为 55.75%，说明直接修改通用策略主干会导致灾难性遗忘，而冻结主干仅训练残差模块的设计有效解耦了通用知识与接口适应。

在跟踪保真度方面，Adapter (W) 的 $E_{AP}$ 为 0.3128 m，$E_{BP}$ 为 0.0804 m，$E_{EP}$ 为 0.1832 m，与 Base Model 的各项指标（0.3145 m, 0.0806 m, 0.1836 m）几乎一致。这进一步证实残差蒸馏策略在保持通用运动跟踪精度上的有效性。

### 遥操作适配效果

Table V 展示了 VR 遥操作数据集上的核心结果。Base Model 在该接口错配的遥操作任务上表现不佳，$E_{AP}$ 高达 2.9352 m，成功率仅 60.40%。Adapter (W) 将 $E_{AP}$ 降至 1.1940 m（**下降 1.7412 m，降幅 59.3%**），成功率提升至 82.20%，平均 episode 步数从 439.83 步提升至 483.33 步。这一结果表明，残差适配器有效补偿了接口特定的延迟、噪声和抖动带来的域偏移，显著提升遥操作部署的跟踪精度和稳定性。

对比消融方法，Fine-tune 的成功率仅 65.80%，$E_{AP}$ 为 1.7563 m；Continual Learning 成功率为 72.20%，$E_{AP}$ 为 1.6146 m。Adapter (W) 在遥操作精度和成功率上均显著优于两者，验证了**冻结主干 + 残差蒸馏**策略相比直接微调或混合训练的优越性。值得注意的是，Fine-tune 虽然遥操作精度有所提升，但在通用运动跟踪上严重退化（成功率仅 40.60%），而 Adapter (W) 实现了两者的兼顾。

### 消融实验

#### 多源数据的作用

Fig. 3a 对比了多源数据（5-Sources）与单源数据训练的通用跟踪器在 OOD 测试集上的表现。雷达图显示，多源数据在五项跟踪保真度指标上均优于单源数据，柱状图表明成功率和平均 episode 步数也一致提升。这验证了**运动多样性的增加是提升通用跟踪器泛化能力的关键因素**，异构数据源的组合有效覆盖了更广泛的运动分布。

#### 世界坐标系奖励设计

Fig. 3b 的消融实验对比了三种奖励配置：纯 RL + 世界坐标系奖励（Pure RL + world frame reward）、纯 RL + 机器人坐标系奖励（Pure RL + robot frame reward）、以及 DAgger 风格蒸馏 + 世界坐标系奖励（DAgger + world frame reward）。结果表明，加入世界坐标系追踪奖励后，全局跟踪误差显著降低，成功率和平均 episode 步数均得到提升。这证实了**世界坐标系下的运动一致性奖励是抑制长期漂移、提升稳定性的关键设计**。此外，纯 RL 训练在跟踪保真度和鲁棒性上均优于 DAgger 风格蒸馏，说明端到端 RL 训练比行为克隆蒸馏更适合该任务。

#### 适配数据量与数据增强

Table VI 的数据规模分析表明，使用 30 分钟遥操作数据进行适配效果最佳。当数据量降至 3 分钟时，适配效果明显不足。此外，使用 FLD（Future Lookahead Distillation）进行数据增强的效果有限，未能显著提升适配性能。这表明**残差适配器在少量但充分的真实遥操作数据下即可有效学习接口特征**，但数据量过少时信息不足。

#### 网络架构选择

Fig. S7 的网络架构消融显示，MLP 融合架构在训练成本和性能之间取得了最佳平衡，优于基于编码器和注意力机制的融合方案。

![[assets/figures/papers/paper_list_l53_https_arxiv_org_abs_2602_08594v2/figures/021_Figure_S.7.jpg]]
*Figure S.7: Network-architecture ablation. Training curves comparing the MLP actor (ours) against encoder-based actors (VQ, FSQ) and an attention-based actor, under identical PPO settings with the same critic. The MLP achieves higher reward and longer episode length, while more complex actors do not yield gains despite increased training cost*

### 接口延迟分析

Fig. S5 的端到端延迟分析揭示了接口延迟是影响遥操作稳定性的主要因素。VR 遥操作的端到端延迟约 0.4 秒，惯性动捕约 0.2 秒。这种显著的延迟差异是导致通用跟踪器在 VR 遥操作中发生漂移和接触中断的核心原因之一，也解释了为何接口特定的残差适配能带来大幅性能提升。

![[assets/figures/papers/paper_list_l53_https_arxiv_org_abs_2602_08594v2/figures/017_Figure_S.5.jpg]]
*Figure S.5: Delay Analysis. The teleoperation delay, as measured via video analysis, is approximately 0.4 s for the VR system and 0.2 s for the inertial motion capture system*

### 定性对比

Fig. 4 展示了高动态运动的定性对比。从左至右依次为 MOSAIC、TWIST 和 GMT。在参考动作的跳跃顶点，MOSAIC 实现了显著的地面间隙，而 TWIST 和 GMT 难以捕捉高加速度的爆发性运动。这表明 MOSAIC 的通用运动跟踪器在多源数据和世界坐标系奖励的共同作用下，对高动态运动具有更强的跟踪能力。

![[assets/figures/papers/paper_list_l53_https_arxiv_org_abs_2602_08594v2/figures/006_Figure_4.jpg]]
*Figure 4: Qualitative Comparison on High Dynamic Motion. From left to right are our model, TWIST, and GMT. Our model achieves substantial ground clearance at the reference apex, whereas baselines (i.e., TWIST and GMT) struggle to capture high-acceleration explosive movements*

### 失败模式与局限性

尽管 MOSAIC 在遥操作适配和通用性保持上表现优异，仍存在以下局限：

1. **传感器依赖**：系统仍依赖可靠的低延迟感知和状态估计，尚未完全消除对传感器和通信链路的依赖。
2. **动力学建模误差**：残差适应主要针对接口偏移，不能解决所有仿真到现实的不匹配，如接触动力学建模误差。
3. **接口间迁移**：当前系统在单一接口上训练适配器，不同接口间的迁移能力未充分验证。
4. **长时漂移**：在长时遥操作中，积累的微小误差仍可能导致缓慢漂移，需要进一步研究。
5. **训练成本**：训练耗时约 48 小时（8 块 A100 GPU），对更多机器人平台的泛化需要额外适配成本。

> **注意**：关于系统在超过 10 分钟连续遥操作中的稳定性极限，以及多接口统一适配器的可行性，原文未提供充分实验证据，这些开放问题需要进一步验证。

### 补充图表

![[assets/figures/papers/paper_list_l53_https_arxiv_org_abs_2602_08594v2/figures/007_Table.jpg]]
*Table: IV. Evaluation results on Motion-X-Sub. ↓ denotes lower is better, ↑ denotes higher is better. TABLE V. Evaluation results on VR dataset*

![[assets/figures/papers/paper_list_l53_https_arxiv_org_abs_2602_08594v2/figures/008_Table.jpg]]
*Table: VI. Data scaling analysis on VR dataset*

![[assets/figures/papers/paper_list_l53_https_arxiv_org_abs_2602_08594v2/figures/002_Table.jpg]]
*Table: I. Dataset summary. We will open-source all highquality multi-source motion data collected in-house*

## 定位与知识库关联

### 与基线方法的关系

**MOSAIC** 的核心定位是在通用人形运动跟踪与遥操作部署之间建立一个“即插即用”的适应层，其方法设计直接回应了现有基线的结构性不足。

**通用运动跟踪基线：GMT 与 TWIST。** 论文将 **GMT**（通用运动跟踪器）和 **TWIST**（遥操作基线）作为主要对比对象。这两个基线代表了当前领域的两类典型方案：GMT 追求大规模运动数据的广泛覆盖，但在真实遥操作接口下因域差距（接口延迟约 0.4 s、噪声和抖动）出现严重漂移和接触中断；TWIST 则面向遥操作设计，但缺乏对多样化运动的泛化能力。MOSAIC 的实验表明，在 Motion-X-Sub OOD 测试集上，其通用跟踪成功率（77.25%）与 GMT（77.88%）几乎持平，仅下降 0.63 个百分点（Table IV），证明残差适应并未牺牲通用性。在高动态运动（如跳跃）的定性对比中（Fig. 4），MOSAIC 能够达到参考动作的离地高度，而 GMT 和 TWIST 均无法捕捉高加速度爆发性运动。

**微调与连续学习的消融对比。** 论文将 **Fine-tuning**（仅用遥操作数据微调通用跟踪器）和 **Continual Learning**（混合遥操作数据与原始语料继续训练）作为适应策略的消融基线。在 VR 遥操作数据集上，残差适配器（Adapter W）的全局锚点位置误差 $E_{AP}$ 降至 1.1940 m，而微调仅为 2.9352 m（Table V）；成功率方面，Adapter (W) 达到 77.25%，微调仅 40.60%（Table IV）。这一巨大差距揭示了关键洞察：直接微调会导致灾难性遗忘，通用运动跟踪能力急剧退化；而连续学习虽能部分保留通用性，但无法有效补偿接口特定的偏移。MOSAIC 通过冻结通用策略主干、仅训练轻量残差模块的方案，在保持通用性的同时实现了接口适应的解耦。

**与 BeyondMimic 等运动模仿系统的奖励设计继承关系。** MOSAIC 的奖励设计明确继承了 **BeyondMimic** 的跟踪目标体系，同时融合了来自 **ASAP** 和 **KungfuBot** 等系统的全局遥操作导向奖励项（Table III）。其核心创新在于引入世界坐标系追踪奖励：消融实验（Fig. 3b）显示，加入世界坐标系奖励后，全局跟踪误差显著降低，成功率和平均步数均得到提升，有效抑制了长期漂移——这正是遥操作场景下最致命的失效模式。

### 适用边界

MOSAIC 在以下条件下展现出显著优势：

1. **接口特异性偏移补偿**：当遥操作接口存在可辨识的系统性误差（如 VR 设备的端到端延迟约 0.4 s、惯性动捕约 0.2 s，见 Fig. S5）时，残差适配器可在 30 分钟量级的小样本数据上实现有效适应（Table VI）。
2. **通用性与专用性的解耦需求**：适用于需要在保持广泛运动跟踪能力的同时，针对特定部署条件进行快速定制的场景。
3. **离线回放与在线遥操作双模式**：单一策略可无缝切换于离线运动复现和实时遥操作之间（Fig. 1）。

然而，MOSAIC 的适用边界同样明确：

1. **依赖可靠感知与状态估计**：系统尚未完全消除对低延迟传感器和通信链路的依赖，在极端通信退化场景下可能失效。
2. **接口适应而非动力学校准**：残差适应主要针对接口层面的输入偏移，不能解决仿真与现实之间的动力学建模误差（如接触力学、执行器饱和等）。
3. **单接口适配器限制**：当前系统为每个接口独立训练适配器，不同接口间的迁移能力未经验证，跨接口泛化需要额外研究。
4. **计算资源需求**：训练耗时约 48 小时（8 块 A100 GPU），对资源受限的机器人平台，部署和再训练成本较高。

### 局限与开放问题

**已知局限：**

- **长时稳定性边界未探明**：在长时遥操作（>10 分钟）中，积累的微小残差误差仍可能导致缓慢漂移，系统的稳定性极限尚未被系统性地刻画。
- **多接口统一适配缺失**：当前方案要求为每种遥操作设备单独训练适配器，缺乏统一的多接口适配器，限制了大规模部署的灵活性。
- **动力学域差距未覆盖**：残差适应仅作用于策略输出层，无法补偿底层动力学参数（如质量、摩擦、关节阻尼）的仿真与现实不匹配。

**开放问题：**

1. 能否将接口级残差适应与动力学校准或域随机化方法（如系统辨识、贝叶斯优化）相结合，从输入和动力学两个层面联合缩小仿真与现实差距？
2. 是否可能开发统一的多接口适配器，使单个策略无需再训练即可适应多种遥操作设备（如 VR 头显、惯性动捕、外骨骼）？这可能需要引入接口编码器或元学习框架。
3. 在资源受限的机器人上，如何通过模型压缩（如知识蒸馏、量化、剪枝）降低残差模块的计算开销，同时保持适应效果？
4. 残差适配器在更复杂、多模态任务（如人机协作、动态环境交互）中的有效性如何？当前的验证主要集中在运动跟踪和遥操作任务上。
5. 系统在更长时遥操作中的稳定性极限是多少？是否存在理论上的误差累积上界，以及如何通过在线校准或闭环修正机制来突破这一极限？

### 知识库定位

MOSAIC 在人形机器人运动控制的知识谱系中占据以下位置：

- **上游继承**：运动模仿（BeyondMimic）、仿真到现实迁移（域随机化、教师-学生蒸馏）、强化学习运动控制（不对称 PPO）的融合。
- **核心贡献**：提出“冻结通用策略 + 残差蒸馏”的适应范式，将接口适应与运动知识解耦，实现了小样本、低破坏性的部署适应。
- **下游启示**：为通用机器人策略的“基础模型 + 轻量适配器”架构提供了实证支撑，与基础模型时代的 LoRA 等参数高效微调方法形成呼应，但面向的是物理仿真到真实部署的域差距问题。

## 原文 PDF

![[paperPDFs/arxiv_2026/MOSAIC_Bridging_the_Sim_to_Real_Gap_in_Generalist_Humanoid_Motion_Tracking_and_Teleoperation_with_Rapid_Residual_Adaptation.pdf]]
