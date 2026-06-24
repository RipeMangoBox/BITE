---
title: "OVOD-Agent: A Markov-Bandit Framework for Proactive Visual Reasoning and Self-Evolving Detection"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/OVOD_Agent_A_Markov_Bandit_Framework_for_Proactive_Visual_Reasoning_and_Self_Evolving_Detection.pdf
project_link: null
code_link: null
aliases:
- OVOD-Agent
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: 引入弱马尔可夫决策过程（w-MDP）将检测过程建模为状态-动作统一体的序列决策，并通过基于UCB的赌博机（Bandit）探索不确定视觉区域，收集轨迹以训练弱监督奖励模型（RM），实现文本表示的迭代细化与检测策略的自适应调整。
primary_logic: 将OVOD重塑为主动视觉推理任务，利用八个离散视觉状态的弱马尔可夫过程与轻量级马尔可夫-赌博机联合强化学习，在完全摆脱大语言模型（LLM）依赖的前提下，以毫秒级延迟实现可解释的多步视觉思维链（Visual-CoT）与检测性能的显著提升。
claims:
- 在LVIS val上，OVOD-Agent使GroundingDINO的罕见类APr提升+2.7，YOLO-World提升+2.4，GroundingDINO 1.5提升+1.4，DINO-X Pro提升+1.2。
- UCB探索策略在Top-K@Stop和PWR指标上均显著优于其他探索策略（如表3），且完整Visual-CoT动作集使APr达到37.7（如表5）。
- 在LVIS minival上，OVOD-Agent + GroundingDINO的APr达到37.0，推理平均延迟仅55ms，远低于LLM依赖方法（如RALF 1.5s）。
- LVIS val 上 APr = OVOD-Agent + GroundingDINO
---

# OVOD-Agent: A Markov-Bandit Framework for Proactive Visual Reasoning and Self-Evolving Detection

> [!tip] 核心洞察
> 将OVOD重塑为主动视觉推理任务，利用八个离散视觉状态的弱马尔可夫过程与轻量级马尔可夫-赌博机联合强化学习，在完全摆脱大语言模型（LLM）依赖的前提下，以毫秒级延迟实现可解释的多步视觉思维链（Visual-CoT）与检测性能的显著提升。

| 字段 | 内容 |
|------|------|
| 中文题名 | OVOD-Agent：面向主动视觉推理与自演进检测的马尔可夫-赌博机框架 |
| 英文题名 | OVOD-Agent: A Markov-Bandit Framework for Proactive Visual Reasoning and Self-Evolving Detection |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2511.21064) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/image_and_video_generation |
| Method | OVOD-Agent |
| Dataset | LVIS val, LVIS minival, COCO2017 val, LVIS |

> [!tip] 效果简介
> - LVIS val 上，APr OVOD-Agent + GroundingDINO vs GroundingDINO (+2.7)；APr OVOD-Agent + YOLO-World vs YOLO-World (+2.4)；APr OVOD-Agent + GroundingDINO 1.5 vs GroundingDINO 1.5 (+1.4)。
> - LVIS minival 上，APr OVOD-Agent + GroundingDINO vs GroundingDINO (+1.6)。
> - COCO2017 val 上，mAP OVOD-Agent + GroundingDINO vs GroundingDINO (+0.6–1.3)。

## 概述

现有开放词汇目标检测（OVOD）方法在推理时普遍采用**单步静态匹配范式**：给定图像和固定类别名称，检测器直接输出区域提议与类别分数。这一范式难以应对视觉模糊性、上下文变化及稀有细粒度类别的识别挑战——文本表示空间未被充分利用，检测器缺乏对不确定区域的主动探索与多步推理能力。

**OVOD-Agent** 将 OVOD 重塑为**主动视觉推理任务**，核心思路是将检测过程建模为**弱马尔可夫决策过程（w-MDP）**，在八个离散视觉状态上执行可解释的视觉操作序列，形成**视觉思维链（Visual-CoT）**。方法包含三个关键机制：

1. **马尔可夫-赌博机联合框架**：通过基于 UCB 的上下文赌博机探索不确定视觉区域，收集推理轨迹，平衡探索与利用。
2. **弱监督奖励模型（RM）**：利用离线轨迹和图像特定的马尔可夫转移先验，训练轻量级双头 MLP，蒸馏策略并预测奖励。
3. **自演进推理**：部署时由 RM 直接指导状态转移，以毫秒级延迟完成多步视觉推理，**完全摆脱大语言模型（LLM）依赖**。

**主要结果**：在 LVIS val 上，OVOD-Agent 使 GroundingDINO 的罕见类 APᵣ 提升 **+2.7**，YOLO-World 提升 **+2.4**，GroundingDINO 1.5 提升 **+1.4**，DINO-X Pro 提升 **+1.2**，推理平均延迟仅约 55 ms，远低于依赖 LLM 的方法（如 RALF 约 1.5 s）。消融实验验证了 UCB 探索策略、马尔可夫转移正则化及完整七动作 Visual-CoT 的有效性。

**方法定位**：OVOD-Agent 属于**无 LLM 的主动视觉推理范式**，区别于 RALF 等在线 LLM 引导方法和 CoT-PL 等视觉思维链方法，在保持低延迟部署优势的同时，实现了可解释的多步检测优化。

## 背景与动机

### 开放词汇目标检测的现状与瓶颈

开放词汇目标检测（Open-Vocabulary Object Detection, OVOD）旨在通过文本提示，识别训练中未见过的物体类别。现有主流方法，如 **GroundingDINO**、**YOLO-World** 等，通常遵循一种**单步静态匹配范式**：给定输入图像和固定类别名称，检测器直接输出区域提议与类别分数，推理过程在单次前馈中完成。

这种范式存在一个核心瓶颈：**文本表示空间未被充分利用**。当面对视觉模糊性（如“运动鞋”与“休闲鞋”的外观重叠）、上下文变化（同一物体在不同场景下的语义漂移）以及稀有细粒度类别（长尾分布中的罕见类）时，仅依赖初始类别名称的一次性匹配缺乏对视觉线索的多步推理能力。检测器无法根据图像的局部纹理、颜色、空间关系等属性动态调整其类别假设，导致对罕见类别的检测性能（APr）显著受限。

### LLM 辅助推理的代价与局限

为弥补上述推理缺口，近期工作尝试引入大语言模型（LLM）进行辅助推理。例如，**RALF** 利用在线 LLM 生成描述符以细化文本提示，**DVDet** 通过 VQA 方式获取细粒度描述，**LLMDet** 则在离线阶段使用 LLM 构建类别知识库。这些方法虽然在一定程度上提升了检测性能，但引入了严重的时间开销——RALF 的单次推理延迟可达 1.5 秒，与实时检测需求形成根本矛盾。此外，LLM 的依赖带来了高昂的计算成本与部署复杂度，使其难以在实际场景中大规模应用。

### 本文动机：重塑 OVOD 为主动视觉推理任务

本文的核心动机在于：**能否在完全摆脱 LLM 依赖的前提下，赋予检测器多步、可解释的视觉推理能力？**

为此，OVOD-Agent 将 OVOD 重塑为一个**主动视觉推理**任务。其关键思路是：将检测过程建模为一个序列决策问题，检测器不再是被动的单步匹配器，而是一个能够根据当前视觉状态主动选择“视觉动作”的智能体。通过执行一系列可解释的视觉操作（如分析颜色、纹理、空间关系），智能体逐步细化文本表示，最终收敛到更准确的类别假设。这一过程形成了一条**视觉思维链（Visual-CoT）**，既提升了检测精度，又保持了推理的可解释性。

更重要的是，OVOD-Agent 完全基于轻量级模块构建——核心的奖励-策略模型（RM）仅为一个 3 层 MLP，内存占用不到 20 MB——在实现与 LLM 方法竞争甚至更优性能的同时，将推理延迟控制在毫秒级别（平均 55 ms），从根本上解决了 LLM 依赖方法的效率瓶颈。

## 核心创新

OVOD-Agent 的核心创新在于将开放词汇目标检测（OVOD）从**单步静态类别名称匹配**重塑为**多步主动视觉推理（Visual-CoT）**。现有方法在推理时仅依赖固定的类别名称进行一次性的文本-视觉映射，完全忽略了视觉模糊性、上下文变化以及稀有细粒度类别所需的渐进式语义消歧。OVOD-Agent 通过三个紧密耦合的设计打破了这一范式。

**弱马尔可夫决策过程（w-MDP）状态建模。** 传统 OVOD 方法将检测视为无状态的固定映射，而 OVOD-Agent 引入了八状态弱马尔可夫决策过程，将上下文与动作统一为弱马尔可夫单元 $z_t = g(c_t, a_t) \in \mathcal{Z}$（Eq. 4），并在短期记忆假设 $P(z_{t+1} \mid z_t, z_{t-1}, \dots) \approx P(z_{t+1} \mid z_t)$ 下建模状态转移（Eq. 5-6）。这一设计使得检测过程具备了可解释的序列决策结构，七个离散视觉动作（Table 1）构成了代理的推理语言，能够在颜色、纹理、空间等属性维度上逐步细化类别假设（Figure 1）。

**基于 UCB 的上下文赌博机探索。** 传统方法缺乏探索机制，无法主动识别不确定区域。OVOD-Agent 采用上置信界（UCB）策略 $Q_t(a) = \hat{\mu}_t(a \mid c_t) + \lambda \sqrt{\frac{\ln t}{1 + n_t(a \mid c_t)}}$（Eq. 9）进行动作选择，在探索与利用之间取得平衡。该策略在统一的停止协议下，Top-K@Stop 达到 $0.66 \pm 0.01$，PWR 达到 44.8%，显著优于随机和贪婪策略（Table 3）。收集的高质量轨迹为后续的奖励模型训练提供了关键数据。

**弱监督奖励模型与自演进闭环。** 传统方法仅依赖监督损失（分类/回归）作为优化信号。OVOD-Agent 构建了轻量级双头 MLP（仅 20MB），通过联合优化轨迹模仿、奖励预测和 KL-based 马尔可夫转移正则化三项损失 $\mathcal{L}_{\mathrm{RM}}$（Eq. 14）进行离线训练。这一设计使得代理在部署时完全摆脱对大语言模型（LLM）的依赖，以毫秒级延迟（平均 55ms）实现与 LLM 方法竞争的性能，同时保持自演进能力。

## 整体框架

OVOD-Agent 将开放词汇目标检测（OVOD）重塑为**主动视觉推理任务**，其核心流水线由四个协同模块构成：**环境状态更新**、**Bandit 探索**、**马尔可夫转移矩阵构建**与**奖励-策略模型（RM）训练**，最终在部署阶段由训练好的 RM 直接指导推理决策（Figure 2）。

![[assets/figures/papers/paper_list_l2198_https_arxiv_org_abs_2511_21064/figures/003_Figure_2.jpg]]
*Figure 2: OVOD-Agent operates through a self-evolving visual reasoning pipeline. (a) The environment updates the visual state by applying detector feedback and the current prompt-conditioned context. (b) A UCB-based Bandit module selects and executes visual actions, collecting rewards and empirical transitions from sampled trajectories. (c) The collected trajectories are joined into an imagespecific Markov transition matrix that models how weak Markov units evolve under different visual operations and serves as a structured prior for learning. (d) A lightweight Reward–Policy Model (RM) is trained on these trajectories and transition priors, distilling both transition behavior and weak reward signals....*

### 推理范式的根本转变

传统 OVOD 方法在推理时仅执行单步静态类别名称匹配：给定图像 $x$ 和文本提示 $T$，检测器 $D$ 一次性输出区域提议与类别分数 $p = D(x, T)$（Eq. 1）。这种“一次性”范式在面对视觉模糊性、上下文变化及稀有细粒度类别时，文本表示空间未被充分利用，检测性能受限。

OVOD-Agent 将这一过程重构为**多步序列决策**：从初始词典查找出发，智能体通过执行一系列可解释的视觉操作（共七种，Table 1），逐步更新上下文状态 $c_{t+1} = f(c_t, a_t)$（Eq. 2），形成一条**视觉思维链（Visual-CoT）**。每一步操作针对颜色、纹理、空间关系等属性进行调整，使类别假设逐步精细化，直至状态稳定或奖励收敛（Figure 1）。

![[assets/figures/papers/paper_list_l2198_https_arxiv_org_abs_2511_21064/figures/001_Figure_1.jpg]]
*Figure 1: We illustrate the state-transition behavior of OVOD-Agent as it iteratively updates its category hypothesis. Starting from an initial dictionary lookup, the agent applies attribute-aware actions that adjust color, texture, and spatial cues to produce a more accurate and grounded state description. The number of required actions varies across images, from single-step updates to multi-step reasoning*

### 弱马尔可夫决策过程（w-MDP）

为建模这一序列演化过程，OVOD-Agent 引入**弱马尔可夫决策过程（w-MDP）**，将上下文与动作统一为**弱马尔可夫单元** $z_t = g(c_t, a_t) \in \mathcal{Z}$（Eq. 4），形成状态-动作一体化表示。在短期记忆假设下，转移概率简化为 $P(z_{t+1} \mid z_t)$（Eq. 5-6），使整个推理过程可在八个离散视觉状态构成的紧凑空间内进行。

### Bandit 探索与轨迹收集

在训练阶段，**基于 UCB 的上下文赌博机（Bandit）模块**负责探索不确定或语义模糊的视觉区域。UCB 动作选择公式为：

$$Q_t(a) = \hat{\mu}_t(a \mid c_t) + \lambda \sqrt{\frac{\ln t}{1 + n_t(a \mid c_t)}}$$

该公式通过平衡历史平均奖励与探索力度（Eq. 9），生成高质量推理轨迹。每条轨迹在满足状态稳定、奖励收敛或步数限制等停止条件时终止，图像级采样则基于平均奖励增量与转移矩阵收敛性进行控制。

### 奖励-策略模型训练与部署

收集到的轨迹被整合为图像特定的**马尔可夫转移矩阵**，作为结构化先验。随后，一个紧凑的**双头 MLP（约 20MB）**作为 RM，在离线轨迹和狄利克雷转移先验的指导下进行联合训练，训练目标包含轨迹模仿、奖励预测与 KL 正则化三项损失（Eq. 14）。部署时，RM 直接替换 Bandit 探索，以策略驱动、奖励驱动或混合模式（由 $\alpha \in [0,1]$ 控制）指导状态转移，实现毫秒级推理延迟（平均 55ms），完全摆脱对大语言模型（LLM）的依赖。

## 核心模块与公式推导

OVOD-Agent 将开放词汇目标检测重塑为主动视觉推理任务，其核心由四个紧密耦合的模块构成：环境状态更新、Bandit 探索、马尔可夫转移矩阵构建、以及奖励-策略模型（RM）训练与推理。

### 环境状态更新模块

给定输入图像 $x$ 和初始文本提示 $T$（通常为类别名称的字典查询），检测器 $D$ 输出区域提议与类别分数：

$$p = D(x, T)$$

检测器反馈与当前提示条件共同构成上下文状态 $c_t$。在每一步 $t$，代理从七个可解释的视觉操作（Table 1）中选择动作 $a_t$，通过函数 $f$ 更新上下文：

$$c_{t+1} = f(c_t, a_t)$$

这七个动作包括颜色调整、纹理描述、空间关系查询等属性感知操作，构成了代理的视觉思维链（Visual-CoT）语言。

### 弱马尔可夫决策过程（w-MDP）

为建模上下文演化的结构化依赖，OVOD-Agent 将状态与动作统一为**弱马尔可夫单元**（weak Markov unit）：

$$z_t = g(c_t, a_t) \in \mathcal{Z}$$

其中 $\mathcal{Z}$ 为八个离散视觉状态构成的有限空间。转移概率满足短期记忆假设：

$$P(z_{t+1} \mid z_t, z_{t-1}, \ldots) \approx P(z_{t+1} \mid z_t)$$

这一设计将检测过程形式化为弱马尔可夫决策过程，既保留了序列决策的结构化先验，又避免了完整 MDP 的状态空间爆炸。

### Bandit 探索与轨迹收集

在训练阶段，代理采用基于上置信界（UCB）的上下文赌博机策略选择动作，以平衡探索与利用：

$$Q_t(a) = \hat{\mu}_t(a \mid c_t) + \lambda \sqrt{\frac{\ln t}{1 + n_t(a \mid c_t)}}$$

其中 $\hat{\mu}_t(a \mid c_t)$ 为动作 $a$ 在上下文 $c_t$ 下的历史平均奖励，第二项为探索奖励（随选择次数 $n_t$ 增加而衰减），$\lambda$ 控制探索强度。

**弱监督奖励信号**来自检测器预测框与真实框的 IoU：

$$r_t^{GT} = 1 - \mathrm{IoU}(b_t^{pred}, b_t^{GT})$$

该奖励值越大，表示当前状态越不确定，需要进一步推理。轨迹停止条件包括状态稳定（$\lVert c_{t+1} - c_t \rVert < \delta_s$）、奖励收敛（$|r_{t+1} - r_t| < \delta_r$）或达到最大步数。图像级采样则在平均奖励增量、转移矩阵收敛或最大 episode 数满足时终止。

收集的轨迹形成图像特定的数据集：

$$\mathcal{T}_i = \{(z_t^{(m)}, z_{t+1}^{(m)}, r_t^{(m)})\}_{t,m}$$

### 马尔可夫转移矩阵构建

对每张图像 $x_i$，将多条轨迹的弱马尔可夫单元转移统计整合为经验转移矩阵 $\hat{P}(a' \mid a, x)$。为每个单元 $z_t$ 分配狄利克雷先验以正则化转移概率：

$$\hat{P}(\cdot \mid z_t) \gets \mathrm{Dirichlet}(\mathbf{n}_{z_t})$$

该矩阵作为结构化先验，在 RM 训练中约束策略学习，保持推理轨迹的马尔可夫一致性。

### 奖励-策略模型（RM）训练

RM 是一个紧凑的三层 MLP（约 20MB），包含策略头 $\pi_\theta$ 和奖励头 $\hat{r}_\theta$。离线训练目标联合优化三项损失：

$$\mathcal{L}_{\mathrm{RM}} = \mathbb{E}_{(z_t, z_{t+1})} [-w_t \log \pi_\theta(z_{t+1}|z_t)] + \beta \mathbb{E}_{(z_t, r_t)} [(\hat{r}_\theta(z_t) - r_t)^2] + \gamma \mathbb{E}_{z_t} [D_{\mathrm{KL}}(\pi_\theta(\cdot|z_t) \| \hat{P}_i(\cdot|z_t))]$$

- **第一项**：加权轨迹蒸馏损失，$w_t$ 为重要性权重，使策略头模仿高质量轨迹的转移行为。
- **第二项**：奖励预测的均方误差，训练奖励头逼近弱监督信号。
- **第三项**：KL 散度正则化，约束策略头输出与图像特定的马尔可夫转移先验保持一致，$\gamma$ 控制正则化强度。

### 推理部署

部署时，Bandit 探索模块被移除，RM 直接指导状态转移。代理支持三种推理模式：**策略驱动**（纯 $\pi_\theta$ 输出）、**奖励驱动**（纯 $\hat{r}_\theta$ 贪婪选择）、以及**混合模式**，通过参数 $\alpha \in [0,1]$ 平衡两者：

$$a_t = \arg\max_a [\alpha \cdot \pi_\theta(a \mid z_t) + (1-\alpha) \cdot \hat{r}_\theta(z_t)]$$

整个过程无需大语言模型参与，推理延迟保持在毫秒级（平均 55ms），内存开销仅约 20MB。

### 补充图表

![[assets/figures/papers/paper_list_l2198_https_arxiv_org_abs_2511_21064/figures/002_Table.jpg]]

![[assets/figures/papers/paper_list_l2198_https_arxiv_org_abs_2511_21064/figures/010_Figure_4.jpg]]
*Figure 4: Step-by-step Case Study of OVOD-Agent, showing how visual actions (color, texture, container, background, spatial cues) progressively refine the caption and stabilize detector grounding*

## 实验与分析

### 主实验结果

OVOD-Agent 在 LVIS 和 COCO 两大基准上对四款主流开放词汇检测器（GroundingDINO、YOLO-World、GroundingDINO 1.5、DINO-X Pro）进行了即插即用式增强。核心结论是：**Agent 对稀有类别（rare categories）的检测提升显著，同时整体 AP 保持稳定，推理延迟仅增加约 55 ms**（Table 2）。

![[assets/figures/papers/paper_list_l2198_https_arxiv_org_abs_2511_21064/figures/004_Table_2.jpg]]
*Table 2: Main results on LVIS and COCO benchmarks. OVOD-Agent improves rare-category detection (APr) while maintaining stable overall accuracy (AP), with only a small increase in inference latency*

具体而言，在 LVIS val 上，OVOD-Agent 使 GroundingDINO 的 APr 提升 **+2.7**，YOLO-World 提升 **+2.4**，GroundingDINO 1.5 提升 **+1.4**，DINO-X Pro 提升 **+1.2**。LVIS minival 上趋势一致，APr 分别提升 +1.6、+1.8、+1.3、+1.1。COCO2017 val 上，OVOD-Agent + GroundingDINO 的 mAP 提升 +0.6–1.3，且 AP50^N 增益尤为突出（+2.6，见 Table 6）。这些结果表明，**Agent 的主动推理机制对长尾、细粒度类别特别有效，而对常见类别的性能几乎无损**。

![[assets/figures/papers/paper_list_l2198_https_arxiv_org_abs_2511_21064/figures/009_Table_6.jpg]]
*Table 6: Comparison with LLM-guided reasoning modules. OVOD-Agent achieves competitive rare-category improvements while keeping inference in the millisecond regime, whereas LLM-based online reasoning methods (e.g., RALF) require second-level latency*

与 LLM 引导的推理方法相比，OVOD-Agent 在保持毫秒级延迟（平均 55 ms）的同时，实现了与 RALF（1.5 s）等在线 LLM 方法竞争甚至更优的稀有类检测性能（Table 6）。这验证了 **弱马尔可夫决策过程与轻量级 RM 的组合，可以在完全摆脱大语言模型依赖的前提下，实现高效的多步视觉推理**。

### 探索策略消融

Table 3 在统一停止协议下对比了三种探索策略：随机（Random）、贪婪（Greedy）和 UCB（本文方案）。评估指标包括 Top‑K@Stop（轨迹质量）、PWR（成对胜率）以及盲评 GPT‑5 评分。

![[assets/figures/papers/paper_list_l2198_https_arxiv_org_abs_2511_21064/figures/005_Table_3.jpg]]
*Table 3: Comparison of exploration strategies under the unified stopping protocol. Higher is better for all metrics. AI scores are based on a blind GPT-5 evaluation (strategy names anonymized) to ensure fairness and prevent prior knowledge bias*

UCB 策略在所有指标上均显著领先：Top‑K@Stop 达到 **0.66±0.01**，PWR 为 **44.8%**，盲评 AI 得分亦最高。这组数据揭示了两个关键机制：

1. **不确定性驱动的探索**：UCB 的上置信界公式（Eq. 9）在历史平均奖励与探索力度之间取得平衡，使 Agent 能够系统性地访问那些视觉模糊或语义歧义的状态，而非过早收敛到局部最优动作。
2. **轨迹质量与检测性能的正相关**：高质量的推理轨迹直接转化为更高的 APr，说明 Bandit 探索阶段收集的经验是后续 RM 训练的有效监督信号。

### 马尔可夫状态建模消融

Table 4 检验了在奖励优化中显式引入马尔可夫转移先验的效果。完整马尔可夫‑Bandit 变体（含经验转移矩阵 $\hat{P}(a'|a, x)$ 与 KL 正则化）相比无转移先验的基线：

![[assets/figures/papers/paper_list_l2198_https_arxiv_org_abs_2511_21064/figures/006_Table_4.jpg]]
*Table 4: Ablation on explicit Markov-state modeling in reward optimization. Metrics include RM loss stability, action entropy, and detection performance (AP and APr) measured on the LVISminival benchmark*

- **RM 损失标准差降至 0.028**，表明训练稳定性大幅提升；
- **动作熵增加**，意味着策略保持了更好的探索多样性；
- **AP 和 APr 均有提升**，证明结构化的弱马尔可夫先验不仅稳定了训练，还直接贡献于检测性能。

这一结果支持了论文的核心设计选择：**将视觉推理过程建模为弱马尔可夫链，并通过狄利克雷先验（Eq. 8）和 KL 正则化将转移结构注入 RM，是实现自演进检测的关键**。

### Visual‑CoT 动作空间消融

Table 5 对七种可解释视觉操作（a1–a7，定义于 Table 1）进行了消融。完整 Visual‑CoT 动作集在 LVIS minival 上取得 **37.7 APr**，优于任何部分动作组合。逐步移除单个动作的实验表明：

![[assets/figures/papers/paper_list_l2198_https_arxiv_org_abs_2511_21064/figures/008_Table_5.jpg]]
*Table 5: Ablation on Visual-CoT actions and visual priors. Metrics are evaluated on the LVIS minival dataset*

- **颜色（color）和纹理（texture）动作**对性能影响最大，移除后 APr 下降明显；
- **空间线索（spatial cues）和背景（background）动作**在复杂场景中尤为重要，有助于消除上下文歧义；
- 动作之间存在互补性——单一动作无法覆盖所有视觉模糊类型，完整的七动作集才能形成鲁棒的推理闭环。

### 失败模式分析

尽管 OVOD-Agent 在多数场景下表现鲁棒，Figure 3 揭示了若干系统性失败模式：

![[assets/figures/papers/paper_list_l2198_https_arxiv_org_abs_2511_21064/figures/007_Figure_3.jpg]]
*Figure 3: Failure cases of OVOD-Agent. Representative examples where the agent fails to correctly identify rare or occluded objects*

1. **非典型外观**：当目标呈现严重变形、罕见配色或非规范形态时，视觉动作提取的颜色/纹理线索可能与语义空间不匹配，导致推理链偏离正确类别假设。
2. **微小与遮挡目标**：在杂乱背景下，被严重遮挡或尺寸极小的稀有物体难以被低级视觉特征（纹理、几何）有效区分，Agent 的逐步细化过程可能无法收敛到正确状态。
3. **GT 种子奖励依赖**：推理轨迹的质量和 RM 训练依赖于基于 GT 框的弱监督奖励（Eq. 7）。在极弱标注或无 GT 的全无监督场景下，奖励信号的可靠性下降，可能影响自演进效果。

这些失败模式指向了当前框架的边界：**当低级视觉先验与高级语义空间之间存在不可约的鸿沟时，纯视觉推理链的效力会衰减**。可能的改进方向包括引入更强的视觉先验、自适应 OOD 推理机制，或利用 3D/时序信息增强对遮挡和微小目标的定位能力。

### 补充图表

![[assets/figures/papers/paper_list_l2198_https_arxiv_org_abs_2511_21064/figures/011_Figure_5.jpg]]
*Figure 5: Evaluation protocol for blind GPT-5 trajectory scoring, including the instruction prompt defining the evaluator’s role and the anonymized input prompt to ensure unbiased assessment*

## 方法谱系与知识库定位

### 1. 与现有基线的结构性差异

OVOD-Agent 的核心贡献并非设计新的检测架构，而是**重塑了开放词汇目标检测（OVOD）的推理范式**。现有 OVOD 方法（包括 **GroundingDINO**、**YOLO-World**、**GroundingDINO 1.5**、**DINO-X Pro** 等）在推理阶段均采用单步静态匹配：给定图像 $x$ 和固定类别名称文本 $T$，检测器 $D$ 输出 $p = D(x, T)$ 后即完成推理。这一范式存在两个结构性瓶颈：

1. **文本表示空间未被充分利用**：类别名称仅作为一次性查询，缺乏对视觉模糊性、上下文变化及稀有细粒度类别的多步推理能力。
2. **无探索机制**：检测器无法主动识别不确定区域并调整语义假设，导致对罕见类别的召回率受限。

OVOD-Agent 将上述静态匹配重塑为**主动视觉推理**：通过弱马尔可夫决策过程（w-MDP）将检测过程建模为八状态序列决策，并引入基于 UCB 的赌博机（Bandit）探索策略，在不确定视觉区域收集轨迹以训练弱监督奖励模型（RM），实现文本表示的迭代细化与检测策略的自适应调整。这一范式转换的关键在于**完全摆脱大语言模型（LLM）依赖**，以毫秒级延迟实现可解释的多步视觉思维链（Visual-CoT）。

### 2. 与 LLM 引导推理方法的定位对比

当前利用 LLM 增强 OVOD 的方法可归为两类：

- **在线 LLM 推理**：如 **RALF**在推理时实时调用 LLM 进行语义细化，但引入秒级延迟（约 1.5s），难以部署于实时场景。
- **离线 LLM 辅助**：如 **LLMDet**利用 LLM 预生成类别描述符，但推理时仍为单步匹配，缺乏动态推理能力。

OVOD-Agent 在方法论上明确区别于上述路线：其 RM 为紧凑的三层 MLP 双头网络（约 20MB），推理时无需任何 LLM 调用。在 LVIS minival 上，OVOD-Agent + GroundingDINO 的 APr 达到 37.0，推理平均延迟仅 55ms，远低于 RALF 的秒级延迟（Table 6）。在 COCO 的 AP50^N 指标上，OVOD-Agent 提升 +2.6（33.4 vs. 30.8），进一步验证了无 LLM 路线的竞争力。

与 **CoT-PL**等视觉思维链方法相比，OVOD-Agent 的核心差异在于其思维链由**七个可解释的视觉操作**（颜色、纹理、容器、背景、空间线索等，见 Table 1）显式定义，而非依赖隐式提示工程。与 **DVDet**等 VQA 细化描述符方法相比，OVOD-Agent 的推理过程是**序列决策驱动**的，而非一次性描述符生成。

### 3. 适用边界与局限性

基于论文提供的实验证据与失败案例分析，OVOD-Agent 的适用边界可归纳如下：

**有效场景**：
- 稀有类别检测（LVIS APr 提升 +1.2 至 +2.7，跨四个检测器骨干）
- 需要多步视觉推理的模糊场景（如颜色、纹理线索互补）
- 对推理延迟敏感的应用（平均 55ms，远低于 LLM 方法）

**已知局限**（Figure 3 失败案例及论文讨论）：

1. **非典型外观失效**：当目标外观为非典型形态（如严重变形、罕见配色）时，视觉动作提取的线索可能与语义空间不匹配，导致推理链断裂。例如 Figure 3 中展示的稀有或遮挡物体识别失败案例。
2. **微小/遮挡目标定位困难**：复杂背景中微小或被严重遮挡的稀有物体，其低级视觉特征（纹理、几何）判别力不足，Bandit 探索难以有效聚焦。
3. **弱监督依赖**：推理轨迹质量和 RM 训练仍依赖 GT 种子奖励 $r_t^{GT} = 1 - \mathrm{IoU}(b_t^{pred}, b_t^{GT})$，在极弱或无 GT 的全无监督场景下性能可能下降。论文未提供无 GT 场景的实验验证，此点需进一步确认。
4. **采样成本线性增长**：Bandit 探索的采样成本随轨迹长度和动作空间大小线性增长（Sec. 3.3），在大规模动作空间或长推理链场景下可能成为瓶颈。

### 4. 开放问题

基于当前方法的局限性和论文的未覆盖领域，以下开放问题值得关注：

1. **语义-视觉不匹配的鲁棒性**：如何有效处理非典型对象状态？是否需要更强的视觉先验（如 3D 几何线索）或自适应 OOD 推理机制来扩展 w-MDP 的状态覆盖范围？
2. **微小/遮挡目标的定位增强**：能否引入跨帧时序信息或多尺度特征聚合来提升对部分不可见目标的推理能力？当前单帧二维视觉动作在此场景下存在固有局限。
3. **跨任务泛化**：OVOD-Agent 的主动推理框架能否推广到其他开放词汇视觉任务（如 open-vocabulary segmentation、open-vocabulary tracking）并保持无 LLM 的低延迟特性？这需要重新定义视觉动作空间和状态表示。
4. **弱监督极限下的鲁棒性**：在训练数据极度稀缺的条件下，狄利克雷先验 $\hat{P}(\cdot \mid z_t) \gets \mathrm{Dirichlet}(\mathbf{n}_{z_t})$ 和弱奖励机制是否足够鲁棒？是否需要元学习或其他形式的结构先验来补偿 GT 信号的稀疏性？
5. **动作空间的可扩展性**：当前七个视觉操作（a1–a7）针对通用目标检测设计。对于特定领域（如医学影像、遥感），如何系统性地扩展动作空间并保持 w-MDP 的紧凑性是一个工程与理论并存的挑战。

## 原文 PDF

![[paperPDFs/CVPR_2026/OVOD_Agent_A_Markov_Bandit_Framework_for_Proactive_Visual_Reasoning_and_Self_Evolving_Detection.pdf]]
