---
title: PhysicsPingPong Strategy and Skill Learning for Physics based Table Tennis Animation
type: paper
paper_level: A
venue: SIGGRAPH
year: 2024
pdf_ref: paperPDFs/SIGGRAPH_2024/PhysicsPingPong_Strategy_and_Skill_Learning_for_Physics_based_Table_Tennis_Animation.pdf
project_link: "https://jiashunwang.github.io/PhysicsPingPong/"
code_link: null
aliases:
- PSSLPBTTA
tags:
- SIGGRAPH_2024
- topic/vision_multimodal_applications/image_and_video_generation
- topic/vision_multimodal_applications
core_operator: 通过引入混合专家（mixture-of-experts）式的分层技能控制器（含技能特定模仿策略、通用模仿策略和混合器策略）以及显式的策略级控制器（CVAE），使得智能体能够明确选择和切换技能，并学习动态决策策略。
primary_logic: 将技能学习分解为模仿、球控制、技能混合三个阶段逐步训练，形成一套可快速切换技能的分层控制器；在此基础上，利用基于条件变分自编码器的迭代行为克隆方法学习高级策略，实现技能多样性与战术决策的解耦控制。
claims:
- 提出的方法在判别器得分上比 ET 高 15.6%，技能准确率达 0.76，多样性得分分别比 ASE、CASE、ET 高 30.7%、32.3%、9.4%，显著缓解了模式坍塌。
- 在乒乓球对打任务中，本方法获得最高的平均击球次数 10.93（ET 为 6.28），且落点分布更接近人类。
- 策略学习框架在对抗场景中取得 68.7% 的胜率（随机对手），在协作场景中实现平均 18.2 回合的连续对打。
- 经过两次策略迭代优化后，智能体对抗胜率提升至 78%，表明策略学习有效。
---

# PhysicsPingPong Strategy and Skill Learning for Physics based Table Tennis Animation

> [!tip] 核心洞察
> 将技能学习分解为模仿、球控制、技能混合三个阶段逐步训练，形成一套可快速切换技能的分层控制器；在此基础上，利用基于条件变分自编码器的迭代行为克隆方法学习高级策略，实现技能多样性与战术决策的解耦控制。

| 字段 | 内容 |
|------|------|
| 中文题名 | PhysicsPingPong：基于物理的乒乓球动画的策略与技能学习 |
| 英文题名 | PhysicsPingPong Strategy and Skill Learning for Physics based Table Tennis Animation |
| 会议/期刊 | SIGGRAPH 2024 |
| Links | [paper](https://arxiv.org/abs/2407.16210) · [Project](https://jiashunwang.github.io/PhysicsPingPong/) · [arXiv](http://arxiv.org/abs/1712.00004) |
| Topic | #topic/vision_multimodal_applications/image_and_video_generation #topic/vision_multimodal_applications |
| Method | PhysicsPingPong |
| Dataset | Table Tennis Skill Evaluation, Ball Control Task, Agent-Agent Competition, Agent-Agent Cooperation |

> [!tip] 效果简介
> - Table Tennis Skill Evaluation 上，Discriminator Score Ours vs ET (15.6% higher)；Skill Accuracy 0.76 vs ET/ASE/CASE (lower) (highest)；Diversity Score Ours vs ASE / CASE / ET (30.7% / 32.3% / 9.4% higher)。
> - Ball Control Task 上，Avg Hits 10.93 vs ET 6.28 (+4.65 (74% increase))。
> - Agent-Agent Competition (vs Random opponent) 上，Winning rate 0.687 vs RL ~0.5 (+0.187)。

## 概述

**PhysicsPingPong** (SIGGRAPH 2024) 提出一种面向物理仿真乒乓球动画的分层控制方法，同时解决**多样化技能学习**与**战术决策**两大难题。其核心动机在于：现有基于可重用技能嵌入的方法在技能差异细微时，容易在任务训练阶段出现**模式坍塌**——智能体仅在少数技能上探索，无法充分利用已学习的技能多样性，从而限制了强化学习的探索效率。

该方法的关键思路是将控制分解为**技能级控制器**与**策略级控制器**两个层次。技能级控制器采用混合专家设计，通过模仿策略、球控制策略和混合器策略三阶段训练，实现五种乒乓球技能（正手攻球、正手推挡、正手扣杀、反手攻球、反手推挡）的稳定执行与平滑切换。策略级控制器则基于条件变分自编码器，根据对手状态和球状态输出技能指令与目标落点，并通过迭代行为克隆持续优化决策。

实验表明，该方法在技能多样性得分上分别超出 **ASE** (Peng et al., SIGGRAPH 2022)、**CASE** (Dou et al., SIGGRAPH Asia 2023) 和 **ET** (Won et al., SIGGRAPH 2021) 30.7%、32.3% 和 9.4%，显著缓解了模式坍塌；在乒乓球对打任务中平均击球次数达 10.93 次（ET 为 6.28 次），落点分布更接近人类；策略控制器在对抗场景中取得 68.7% 胜率，经两次迭代优化后提升至 78%。

## 背景与动机

基于物理的角色动画旨在生成逼真且可控的运动，在游戏、影视和虚拟现实等领域具有重要应用。乒乓球作为一项高速、高技巧性的对抗运动，对动画系统提出了极高的要求：智能体不仅需要掌握多种击球技能（如正手攻球、反手推挡、正手扣杀等），还必须具备根据对手状态和来球轨迹进行实时战术决策的能力。构建一个既能执行多样化技能又能进行策略博弈的乒乓球动画系统，是该领域长期以来的核心挑战。

近年来，基于可重用技能嵌入（reusable skill embedding）的方法在运动生成中展现出潜力，其核心思路是学习一个连续隐空间，使智能体能够通过采样不同隐变量来调用不同技能。然而，当技能之间的运动差异较为细微时（例如正手 drive 与 push），现有方法普遍面临**模式坍塌（mode collapse）**的严重问题。具体而言，在任务训练阶段，智能体倾向于仅探索少数几个隐变量对应的技能，导致已学习的多样技能无法被充分利用。例如，**ASE**（Peng et al., SIGGRAPH 2022）和 **CASE**（Dou et al., SIGGRAPH Asia 2023）在接收到特定技能指令时，仍可能错误地执行其他技能；而 **ET**（Won et al., SIGGRAPH 2021）通过离散技能切换虽能缓解该问题，但在技能过渡时往往需要提前终止当前动作以返回准备姿态，造成运动不连贯。这些局限性使得现有方法难以在复杂对抗场景中同时保证技能的准确执行与平滑过渡。

上述瓶颈的根源在于：单一通用策略无法显式区分不同技能的运动特征，而技能切换机制又缺乏对过渡过程的精细控制。因此，本文的核心动机是设计一种新的分层控制架构，将技能执行的多样性与技能切换的平滑性进行解耦，从而从根本上缓解模式坍塌。在此基础上，进一步引入策略级控制器，使智能体能够根据实时博弈状态自主选择技能和目标落点，最终实现从底层运动生成到高层战术决策的完整闭环。

## 核心创新

PhysicsPingPong 的核心创新在于构建了一套**分层解耦的控制架构**，将技能执行与战术决策彻底分离，从而同时解决了技能多样性保持和复杂决策学习两大难题。其关键创新点体现在以下三个“changed slots”上：

### 1. 技能表示：从单一通用策略到混合专家系统

现有方法（如 **ASE** (Peng et al., SIGGRAPH 2022) 和 **CASE** (Dou et al., SIGGRAPH Asia 2023)）通常采用单一通用模仿策略来覆盖所有技能。当不同技能之间的运动差异非常细微时（例如乒乓球的正手攻球与推挡），这种设计极易导致**模式坍塌**——智能体倾向于仅探索少数几个技能，丧失了技能的多样性。

PhysicsPingPong 将此“槽位”重构为**混合专家式设计**：
- **五个技能特定模仿策略**：每个策略 $\pi^i(a^i|s, z^i)$ 专注于一种特定技能（正手攻球、正手推挡、正手扣杀、反手攻球、反手推挡），通过各自的运动判别器和隐变量编码器进行独立训练。
- **一个通用模仿策略**：捕捉所有技能共享的基础运动模式。
- **混合器策略**：在推理时动态融合通用策略与选定技能策略的输出。

这一设计的关键因果机制在于：**技能特定策略提供了明确的、可区分的动作原型，强制智能体在探索时保持技能间的差异**。实验证据表明，该设计使多样性得分相比 ASE、CASE 和 **ET** (Won et al., SIGGRAPH 2021) 分别提升了 30.7%、32.3% 和 9.4%，技能准确率达到 0.76，显著缓解了模式坍塌。

### 2. 技能切换：从离散跳变到连续时间步的关节级混合

**ET** 等方法通过直接切换控制器来实现技能转换，这往往导致切换瞬间的姿态失配和运动不连贯。PhysicsPingPong 的**混合器策略**从根本上改变了技能过渡的机制。

混合器策略 $\omega^m(z^m|s, b, \delta, y)$ 在**每一个时间步**都输出关节级的混合权重 $\varphi$，并通过加权和将通用策略与选定技能策略的动作融合为最终的 PD 目标关节角度：

$$a = \varphi \odot \pi^u(\cdot | s, z^u) + (1 - \varphi) \odot \sum_{i=1}^{5} \delta_i \pi^i(\cdot | s, z^i)$$

这一公式是本工作的核心操作原语。其效果是：技能之间的过渡不再是瞬间的“硬切换”，而是通过混合权重 $\varphi$ 的连续变化实现的**平滑姿态演化**。可视化证据（Figure 8）显示，混合权重在击球瞬间最低（技能特定策略主导），而在技能过渡期间升高（通用策略介入），验证了混合器在协调技能切换中的关键作用。消融实验也证实，与直接切换单技能控制器相比，混合器策略显著减少了过渡阶段的失败。

### 3. 决策策略：从手动指定到基于 CVAE 的迭代行为克隆

在技能层之上，PhysicsPingPong 引入了一个**策略级控制器**，改变了技能和目标选择的方式。基线方法中，技能指令和击球目标通常由人类手动指定或随机生成；本工作则采用**条件变分自编码器**，根据对手状态、球状态和自身状态，同时输出技能指令和目标落点。

该控制器的训练采用**迭代行为克隆**：先用初始数据训练 CVAE，然后让智能体自我对打生成新数据，再用新数据精炼策略。这形成了一个“决策-执行-反馈-优化”的闭环。实验表明，经过两次迭代细化后，人机对抗胜率从 55% 提升至 78%（Table 5），验证了这一策略学习框架的有效性。

### 创新总结

PhysicsPingPong 的创新本质上是**将技能多样性和战术决策这两个耦合难题进行了架构层面的解耦**：技能层通过混合专家和平滑混合机制保证了运动的多样性与连贯性；策略层通过 CVAE 和迭代学习实现了对复杂博弈场景的适应性决策。这种“下层稳定执行，上层灵活决策”的分层设计，为物理仿真角色动画中的技能学习与策略规划提供了一套完整的解决方案。

## 整体框架

PhysicsPingPong 采用“策略-技能”双层分层控制架构，将乒乓球对打任务分解为高层决策与底层运动执行两个解耦的子问题。该设计直接回应了核心瓶颈：现有基于可重用技能嵌入的方法在技能差异细微时，容易在任务训练阶段出现模式坍塌，导致智能体仅在少数技能上进行探索。通过显式分离“何时使用何种技能”与“如何执行技能”，本方法实现了技能多样性与战术决策的独立优化。

### 系统架构与数据流

整个系统的输入输出流如 Figure 2 和 Figure 3 所示，自上而下分为两个层级的控制器：

![[assets/figures/papers/paper_list_l2_https_arxiv_org_abs_2407_16210/figures/003_Figure_3.jpg]]
*Figure 3: The architecture of our method. We train the skill-level controller through the stages of imitation policies, ball control policies, and finally, the mixer policy. We train the strategy-level controller after the skill-level controller is ready and its weight is frozen. ⊗⊕ stands for the weighted sum in Equation 8*

![[assets/figures/papers/paper_list_l2_https_arxiv_org_abs_2407_16210/figures/002_Figure_2.jpg]]
*Figure 2: An overview of our method. Strategy action includes the skill command and ball’s target landing location. Skill action includes the target joint angles for PD controllers, blended from the outputs of imitation policies*

**策略级控制器** 接收智能体状态、对手状态和球的运动状态作为输入，输出策略动作。策略动作由两部分组成：技能指令和球的目标落点位置。技能指令决定底层应激活哪一项击球技能，目标落点则定义了球的期望飞行终点。该控制器采用条件变分自编码器实现，以建模竞技体育中固有的随机性决策。

**技能级控制器** 接收智能体状态、球状态以及来自策略级控制器的策略动作，输出技能动作。技能动作的具体形式是 PD 控制器的目标关节角度，由模仿策略的输出经关节级混合权重融合得到。最终，PD 控制器将目标关节角度转换为关节力矩，驱动物理仿真中的智能体角色执行动作。

### 技能级控制器的三阶段训练

技能级控制器的训练遵循“模仿→球控制→混合”的递进式流程，如 Figure 3 所示：

1. **模仿策略阶段**：从动作捕捉数据中学习五种技能特定的模仿策略和一个通用模仿策略。每个技能特定策略对应一种击球技能，通用策略则捕获跨技能共享的运动模式。这一混合专家设计是缓解模式坍塌的关键——通过为每种技能维护独立的策略网络，避免了单一通用策略在技能差异细微时的表示混淆。

2. **球控制策略阶段**：在模仿策略的基础上，训练智能体在技能执行过程中命中来球并控制球的落点。该阶段使用组合奖励函数，包含球拍接近奖励、球落点奖励和风格奖励三项，引导智能体在保持运动风格的同时完成击球任务。

3. **混合器策略阶段**：学习一个混合器策略，在连续时间步上输出关节级混合权重，将通用策略和当前选定技能策略的动作进行融合。这一机制实现了技能间的平滑过渡——击球瞬间混合权重最低以保证技能执行的纯粹性，技能过渡期间权重升高以利用通用策略的稳定性。

### 策略级控制器的迭代学习

技能级控制器训练完成并冻结权重后，开始训练策略级控制器。该控制器采用迭代行为克隆方法：首先收集专家数据训练初始策略，随后让策略与环境交互生成新数据，再通过行为克隆进行策略细化。这一迭代过程使策略能够在对抗和协作场景中持续优化决策质量。

## 核心模块与公式推导

### 技能级控制器：三层递进训练

技能级控制器的训练分为三个阶段，逐步构建可平滑切换的多样技能表示。

**模仿策略** 从动捕数据学习各技能的运动风格。针对五种技能分别训练技能特定模仿策略 $\pi^{i}(a^{i}|s, z^{i})$，同时训练一个通用模仿策略 $\pi^{u}$。训练采用对抗性技能嵌入框架，其判别器损失为：

$$\min_{D^{i}} -\mathbb{E}_{d_{M^{i}}(s,s')}\log(D^{i}(s,s')) - \mathbb{E}_{d_{\pi^{i}}(s,s')}\log(1-D^{i}(s,s')) + \lambda_{gp}\mathbb{E}_{d_{M^{i}}(s,s')}\|\nabla_{\phi}D^{i}(\phi)\|_{\phi=(s,s')}\|^{2}$$

其中 $d_{M^{i}}$ 为第 $i$ 个技能的参考运动分布，$d_{\pi^{i}}$ 为策略生成的状态转移分布，梯度惩罚项保证训练稳定性。同时训练编码器最大化隐变量与状态转移的互信息：

$$\max_{q^{i}} \mathbb{E}_{p(z^{i})}\mathbb{E}_{d^{\pi^{i}}(s,s'|z^{i})}[\log q^{i}(z^{i}|s,s')]$$

模仿阶段的奖励函数结合判别器分数与隐变量一致性：

$$r_{t} = -\log(1 - D^{i}(s_{t}, s_{t+1})) + \beta\log q^{i}(z_{t}^{i}|s_{t}, s_{t+1})$$

**球控制策略** 在各技能模仿策略基础上训练智能体实际击球并控制落点。组合奖励函数为：

$$\boldsymbol{r}(t) = \boldsymbol{w_{p}}\boldsymbol{r_{p}}(t) + \boldsymbol{w_{b}}\boldsymbol{r_{b}}(t) + \boldsymbol{w_{s}}\boldsymbol{r_{s}}(t)$$

其中球拍接近奖励在接触前生效：

$$r_{p}(t) = \begin{cases} \exp(-4||x_{p}(t)-x_{b}(t)||^{2}), & \text{if } C_{bp}(t)=0, \\ 0, & \text{otherwise.} \end{cases}$$

球落点奖励在击球后且球未触台前生效：

$$r_{b}(t) = \begin{cases} 1 + \exp(-4||x_{c}(t)-x_{t}(t)||^{2}), & \text{if } C_{bp}(t)=1 \text{ and } C_{bt}(t)=0, \\ 0, & \text{otherwise.} \end{cases}$$

风格奖励 $r_{s}$ 沿用模仿阶段的判别器与编码器奖励，防止球控制训练破坏运动风格。

**混合器策略** 是解决技能切换时模式坍塌的关键模块。混合器策略 $\omega^{m}(z^{m}|s, b, \delta, y)$ 以智能体状态 $s$、球状态 $b$、技能指令 $\delta$ 和目标落点 $y$ 为输入，输出通用模仿策略的隐变量 $z^{m}$ 以及关节级混合权重 $\varphi$。最终输出到 PD 控制器的目标关节角度为：

$$a = \varphi \odot \pi^{u}(\cdot|s, z^{u}) + (1 - \varphi) \odot \sum_{i=1}^{5} \delta_{i}\pi^{i}(\cdot|s, z^{i})$$

其中 $\odot$ 表示逐元素乘法，$\delta_{i}$ 为技能选择指示器。混合器在连续时间步上输出时变权重，击球瞬间混合权重最低（技能特定策略主导），技能过渡期间权重升高（通用策略辅助平滑过渡），验证见 Figure 8。

![[assets/figures/papers/paper_list_l2_https_arxiv_org_abs_2407_16210/figures/013_Figure_8.jpg]]
*Figure 8: Visualization of the average blending weights ?? of the shoulder, elbow, and wrist joints. The weights of the mixer policy are usually lowest when the paddle contacts the ball, and higher before and after transitions between different skills*

### 策略级控制器：迭代行为克隆

策略级控制器采用条件变分自编码器建模乒乓球对打中的随机决策。其训练损失为：

$$\sum_{k=1}^{K} ||c_{k}^{\mathrm{expert}} - c_{k}'|| + \beta_{KL} D_{KL}(Q(u|\mu_{k}, \sigma_{k}^{2}) || N(0, I))$$

第一项为技能指令与目标落点的重构误差，第二项为隐变量后验分布与标准正态先验的 KL 散度。训练采用迭代行为克隆：初始用人类对打数据训练 CVAE，随后让智能体与自身对打收集新数据，将胜者的决策作为专家轨迹进行下一轮克隆，逐步优化策略。

## 实验与分析

### 技能学习评估

我们首先评估技能级控制器在区分和生成多样化乒乓球技能方面的能力。评估围绕三个核心指标展开：判别器得分（Discriminator Score）、技能准确率（Skill Accuracy）和多样性得分（Diversity Score）。判别器得分衡量智能体执行的动作与目标技能参考运动的相似度，技能准确率反映技能指令与实际执行技能的一致性，多样性得分则专门评估模型对视觉相似技能（如正手 drive 与 push）的区分能力。

**表 1** 给出了与 **ASE**（Peng et al., SIGGRAPH 2022）、**CASE**（Dou et al., SIGGRAPH Asia 2023）和 **ET**（Won et al., SIGGRAPH 2021）的定量对比。本方法在判别器得分上比 ET 高出 15.6%，技能准确率达到 0.76，均为所有方法中最优。在多样性得分上，本方法分别比 ASE、CASE、ET 高出 30.7%、32.3% 和 9.4%。这一显著提升的核心原因在于混合专家式的模仿策略设计：五个技能特定策略各自专注单一技能的运动分布，通用策略提供跨技能的平滑过渡能力，混合器策略在连续时间步上输出关节级融合权重，从而有效缓解了单一通用策略在技能差异细微时出现的模式坍塌问题。

**Figure 4** 的定性对比进一步印证了这一结论。当给定四种不同的技能指令时，ASE 和 CASE 偶尔会错误地使用其他技能（红色框标注），而 ET 为了回到准备姿态可能提前终止击球动作（黄色框标注）。相比之下，本方法能够准确执行指定的技能，并在技能切换过程中保持动作的连贯性。

### 任务性能评估

在球控制任务中，我们衡量智能体在连续对打中维持回合的能力，核心指标为平均击球次数（Avg Hits）和落点精度（Accuracy）。**表 2** 显示，本方法取得了最高的平均击球次数 10.93，相比 ET 的 6.28 提升了约 74%。这一优势源于混合器策略在技能过渡期间提供的连续动作融合：如 **Figure 8** 所示，混合器在肩、肘、腕关节的混合权重在击球瞬间通常最低（此时技能特定策略主导），而在技能过渡期间升高（通用策略介入），从而实现了无缝的技能切换，避免了 ET 因直接切换控制器导致的姿态失配和回合中断。

值得注意的是，本方法的落点精度为第二优。分析认为，精度略低于最优方法的原因可能是混合器在过渡期间引入的微小动作扰动，但这一代价换来了显著更长的对打回合，整体上更符合乒乓球动画对连贯性和观赏性的需求。

### 策略学习评估

策略级控制器的评估在两种场景下进行：竞争场景（agent-agent competition）和协作场景（agent-agent cooperation）。**表 3** 显示，在竞争场景中，本方法对随机策略对手取得 68.7% 的胜率，而纯强化学习基线（RL）仅约 50%。在协作场景中，本方法实现平均 18.2 回合的连续对打，显著优于 RL 基线。**Table 4** 进一步表明，当策略控制器使用不同类型的对手（随机策略 vs. 基于视频的对手）进行训练后，其对抗 RL 的胜率均保持在 65% 以上，验证了策略学习框架的泛化能力。

![[assets/figures/papers/paper_list_l2_https_arxiv_org_abs_2407_16210/figures/011_Table_4.jpg]]
*Table 4: Winning rates between our method and RL. The opponent in parentheses is the opponent during training of the strategy policy*

策略控制器的有效性还体现在技能指令分布和落点分布上。**Figure 6** 显示，本方法的技能指令分布覆盖了全部五种技能，而 RL 基线倾向于仅使用少数技能，再次印证了模式坍塌的缓解。**Figure 7** 的落点分布对比表明，本方法生成的落点分布更接近人类选手的模式，具有更好的空间多样性和战术合理性。

![[assets/figures/papers/paper_list_l2_https_arxiv_org_abs_2407_16210/figures/008_Figure_6.jpg]]
*Figure 6: Skill command distribution of our method and RL*

![[assets/figures/papers/paper_list_l2_https_arxiv_org_abs_2407_16210/figures/009_Figure_7.jpg]]
*Figure 7: Target landing locations of our method, RL and Human*

### 迭代行为克隆与消融分析

策略控制器的核心学习机制是迭代行为克隆。**Table 5** 的人机交互评估提供了关键的消融证据：策略控制器在初始训练后对人机对打的胜率为 55%，经过第一次迭代细化后提升至 64%，第二次迭代后进一步提升至 78%。每次迭代中，CVAE 使用上一轮策略生成的专家数据进行行为克隆，逐步将策略分布向更优的决策区域收缩。这一结果表明，迭代行为克隆能够有效利用自博弈产生的数据进行策略自改进，而无需额外的强化学习奖励设计。

![[assets/figures/papers/paper_list_l2_https_arxiv_org_abs_2407_16210/figures/012_Table_5.jpg]]
*Table 5: Evaluation of human-agent interaction*

技能过渡的消融分析（**Figure 5**）表明，若仅使用正手和反手 drive 控制器进行直接切换（无混合器），智能体在技能切换时频繁失败，表现为试图在击球前切换技能但动作不连贯。混合器策略通过关节级连续融合，使技能切换发生在击球前的准备阶段，显著降低了过渡失败率。

### 失败模式与局限性

尽管本方法在技能多样性和策略决策上取得了显著进展，仍存在以下局限。首先，当前框架针对五种乒乓球技能设计，技能特定策略的数量与技能种类线性相关；扩展到数百种技能时，混合专家架构的计算开销和训练复杂度将显著增加。其次，物理仿真中未考虑马格努斯效应（Magnus effect），球的旋转轨迹不够真实，可能影响策略控制器对落点选择的决策质量。在实验中，我们观察到当对手发出高而慢的球时，正手扣杀（forehand smash）的执行不够明显（如 **Figure 9** 所述），部分原因在于球轨迹的物理简化限制了扣杀时机的自然出现。

![[assets/figures/papers/paper_list_l2_https_arxiv_org_abs_2407_16210/figures/014_Figure_9.jpg]]
*Figure 9: Agent-agent gameplay. Blue agent is applying our strategy-level controller. The red dot is the target. We demonstrate four skills; the forehand smash is less obvious because the opponent does not deliver high and slow shots*

### 补充图表

![[assets/figures/papers/paper_list_l2_https_arxiv_org_abs_2407_16210/figures/006_Table_1.jpg]]
*Table 1: Comparisons on Discriminator Score, Skill Accuracy, and Diversity Score*

![[assets/figures/papers/paper_list_l2_https_arxiv_org_abs_2407_16210/figures/007_Table_2.jpg]]
*Table 2: Task performance evaluation. Our method can achieve the longest average hits and the second best accuracy*

![[assets/figures/papers/paper_list_l2_https_arxiv_org_abs_2407_16210/figures/005_Figure_4.jpg]]
*Figure 4: Comparison with other methods with four skill commands. ASE and CASE may use wrong skills as shown in the red box. ET may terminate earlier to return to a preparation pose, as shown in the yellow boxes*

![[assets/figures/papers/paper_list_l2_https_arxiv_org_abs_2407_16210/figures/010_Table_3.jpg]]
*Table 3: Strategy evaluation. We report the winning rates for the competition setting and average rounds for the cooperation setting*

## 方法谱系与知识库定位

### 核心瓶颈与设计动机

现有基于可重用技能嵌入的物理角色动画方法面临一个关键瓶颈：当技能之间的运动差异较为细微时，在任务训练阶段极易出现**模式坍塌（mode collapse）**。具体而言，智能体倾向于仅探索少数几个技能，无法充分利用已学习的多样技能库，这直接限制了强化学习在复杂任务中的探索效率与最终表现。PhysicsPingPong 的核心设计动机正是通过显式的技能选择与平滑切换机制，从根本上缓解这一问题。

### 方法谱系：与基线工作的关系

PhysicsPingPong 的方法设计直接回应了三条主要基线的局限性：

- **ASE**（Peng et al., SIGGRAPH 2022）：采用对抗性技能嵌入，但依赖单一通用模仿策略，无法显式区分不同技能。当技能间视觉差异较小时，策略容易混淆技能指令，导致模式坍塌。
- **CASE**（Dou et al., SIGGRAPH Asia 2023）：在 ASE 基础上引入条件对抗性技能嵌入，但仍未解决技能切换时的姿态失配问题。
- **ET**（Won et al., SIGGRAPH 2021）：通过离散技能切换实现专家迁移，但直接切换控制器的方式导致技能过渡不平滑，智能体往往需要提前终止当前动作以返回准备姿态，损失了运动连续性。

PhysicsPingPong 针对上述基线的三个关键设计槽位进行了系统性改进：

| 设计槽位 | 基线做法 | PhysicsPingPong 改进 | 核心机制 |
|---------|---------|---------------------|---------|
| **技能表示** | 单一通用模仿策略 | 混合专家（MoE）设计：5 个技能特定策略 + 1 个通用策略 + 混合器策略 | 显式区分技能，通过关节级融合权重实现动作组合 |
| **技能切换** | 直接切换或终端状态正则化 | 连续时间步上的混合器策略输出关节级混合权重 | 击球瞬间混合权重最低，过渡期间权重升高，实现平滑切换 |
| **决策策略** | 人工指定或随机生成 | 条件变分自编码器（CVAE）+ 迭代行为克隆 | 根据对手与球状态输出技能指令与目标落点，支持策略迭代优化 |

### 三阶段递进训练范式

PhysicsPingPong 的技能级控制器采用**三阶段递进训练**，形成因果链条：

1. **模仿策略阶段**：从动捕数据学习各技能的运动风格，采用对抗性判别器（含梯度惩罚）与隐变量编码器联合训练，确保技能嵌入的可区分性。
2. **球控制策略阶段**：在模仿策略基础上训练智能体命中来球并控制落点，组合奖励由球拍接近奖励、球落点奖励和风格奖励构成。
3. **混合器策略阶段**：训练混合器策略融合通用策略与选定技能策略的输出，实现技能间的平滑过渡。

这种分阶段训练范式将技能多样性学习与战术决策解耦，使得技能级控制器在冻结后可直接被策略级控制器调用。

### 策略级控制器的知识定位

策略级控制器采用 **CVAE + 迭代行为克隆** 的框架，其知识定位具有以下特点：

- **随机性建模**：CVAE 的隐变量捕捉体育对抗中的固有随机性，使得策略输出具有多样性。
- **迭代优化能力**：通过行为克隆学习专家数据后，可在实际对抗中收集新数据并迭代细化策略。实验表明，经过两次迭代细化后，人机对抗胜率从 55% 提升至 78%。
- **解耦设计**：策略控制器仅输出高层指令（技能类型 + 目标落点），底层运动执行完全由技能控制器负责，实现了战术决策与运动控制的清晰分离。

### 适用边界与局限

PhysicsPingPong 的设计存在明确的适用边界：

1. **技能规模限制**：当前方法仅针对乒乓球五个技能（正手攻球、推挡、扣杀、反手攻球、反手推挡）设计。扩展到包含数百种技能的数据集时，混合专家架构的计算开销和技能表示的区分度可能面临挑战。
2. **物理仿真简化**：物理仿真中未考虑马格努斯效应（Magnus effect），球的旋转轨迹和相应的策略可能不够真实。这在专业级乒乓球模拟中是一个显著局限。
3. **策略泛化性**：策略级控制器通过迭代行为克隆学习，其泛化能力依赖于训练对手的多样性。当面对全新风格的对手时，策略可能需要额外的微调。

### 开放问题

1. **大规模技能扩展**：如何将混合专家架构扩展到包含数百种不同技能的数据集，同时保持技能间可区分性和计算效率？
2. **物理真实性增强**：如何引入马格努斯效应等高级物理现象，以获得更真实的球轨迹和相应的战术策略？
3. **策略泛化**：如何在无需大量额外训练的前提下，使策略控制器泛化到未见过的对手风格和比赛场景？

## 原文 PDF

![[paperPDFs/SIGGRAPH_2024/PhysicsPingPong_Strategy_and_Skill_Learning_for_Physics_based_Table_Tennis_Animation.pdf]]