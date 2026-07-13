---
title: "Visual Planning: Let's Think Only with Images"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/Visual_Planning_Lets_Think_Only_with_Images.pdf
project_link: null
code_link: https://github.com/yix8/VisualPlanning
openreview_forum_id: wsnse46kRO
aliases:
- VPRLV
- VPLSTOI
tags:
- ICLR_2026
- topic/reinforcement_learning_planning_agents
- topic/reinforcement_learning_planning_agents/deep_rl
core_operator: "推理模态：从文本符号推理切换为纯视觉图像序列推理，消除语言中介环节。"
primary_logic: "在视觉-空间任务中，直接生成图像序列作为规划轨迹（视觉规划）比生成文本描述更能准确捕捉状态转移与空间关系；配合两阶段强化学习（随机轨迹初始化+GRPO进度奖励）可训练大视觉模型学会有效的视觉规划，从而绕过模态差距，显著提升准确性与分布外鲁棒性。"
claims:
- "视觉规划范式的平均Exact Match (EM) 比文本推理高出27个百分点（AVG EM 80.6% vs. 53.6%）。"
- "VPRL在FROZENLAKE上EM达91.6%，远超所有文本基线（最强文本Qwen SFT 68.6%，Gemini 2.5 Pro 72.0%）。"
- "文本规划系统有25.7%的坐标描述和22.3%的ASCII描述与真实布局不匹配，揭示了视觉-文本模态差距。"
- "VPRL将因无效动作导致的失败比例相比VPFT降低至少24%（VPFT 61-78%，VPRL 25-37%）。"
---

# Visual Planning: Let's Think Only with Images

> [!tip] 核心洞察
> 在视觉-空间任务中，直接生成图像序列作为规划轨迹（视觉规划）比生成文本描述更能准确捕捉状态转移与空间关系；配合两阶段强化学习（随机轨迹初始化+GRPO进度奖励）可训练大视觉模型学会有效的视觉规划，从而绕过模态差距，显著提升准确性与分布外鲁棒性。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 视觉规划：仅凭图像思考 |
| 英文题名 | Visual Planning: Let's Think Only with Images |
| 会议/期刊 | ICLR 2026 (Oral) |
| Links | [paper](https://openreview.net/forum?id=wsnse46kRO) · [GitHub](https://github.com/yix8/VisualPlanning) |
| Topic | #topic/reinforcement_learning_planning_agents #topic/reinforcement_learning_planning_agents/deep_rl |
| Method | Visual Planning via Reinforcement Learning (VPRL) |
| Dataset | FROZENLAKE, MAZE, MINIBEHAVIOR, Average across three tasks |

> [!tip] 效果简介
> - FROZENLAKE 上，EM (%) 为 91.6 (VPRL)，对比 68.6 (Qwen SFT)，变化 +23.0 pp。
> - MAZE 上，EM (%) 为 74.5 (VPRL)，对比 60.9 (Qwen SFT)，变化 +13.6 pp。
> - MINIBEHAVIOR 上，EM (%) 为 75.8 (VPRL)，对比 31.3 (Qwen SFT)，变化 +44.5 pp。

## 概要

当前多模态视觉-语言模型在执行空间规划任务时，普遍依赖将视觉场景转换为文本描述再进行推理的范式。这一模态转换过程引入显著信息损失：文本系统中有25.7%的坐标描述和22.3%的ASCII描述与真实布局不匹配，直接导致纯文本推理在视觉优先任务上的性能受限。

本文提出**视觉规划**范式，核心思想是将推理完全保留在视觉模态内——模型自回归生成图像序列作为规划轨迹，每一步即一个视觉状态，从根本上消除语言中介环节。配合**VPRL**两阶段强化学习框架（随机轨迹初始化 + GRPO进度奖励优化），该方法训练大视觉模型学会有效的视觉规划。

在FROZENLAKE、MAZE和MINIBEHAVIOR三个视觉导航与操作任务上，VPRL的平均Exact Match达80.6%，比最强文本基线高出27个百分点。其中FROZENLAKE上EM达91.6%，远超闭源模型Gemini 2.5 Pro的72.0%和开源文本SFT的68.6%。随网格复杂度增加，视觉规划的PR曲线保持平坦，而文本推理性能急剧下降，显示出更强的分布外鲁棒性。



### 视觉-空间规划中的模态瓶颈

当前多模态视觉-语言模型在空间规划任务中普遍遵循“视觉感知→文本描述→文本推理→动作输出”的流水线。这一范式隐含地将视觉场景转换为语言符号进行推理，再映射回空间动作。然而，该模态转换过程存在根本性信息损失：视觉场景的精确空间布局、物体间的拓扑关系以及动态状态转移往往难以用离散语言符号无损编码。

经验证据表明，文本规划系统在描述视觉布局时存在系统性偏差——**25.7%的坐标描述**和**22.3%的ASCII描述**与真实环境布局不匹配（Section 4）。这种“视觉-文本模态差距”直接导致语言中介环节成为空间推理的瓶颈：即使是最先进的文本推理模型，在网格导航等视觉优先任务上的精确匹配率（Exact Match, EM）也始终低于纯视觉规划范式（平均**53.6% vs. 80.6%**，Table 1）。

### 现有方法的局限

当前应对空间规划任务的方法可分为三类，各有结构性缺陷：

**文本推理方法**（如**Qwen 2.5-VL-Instruct-7B**的Direct、CoT、SFT变体）依赖模型将视觉输入转化为文本动作序列或带布局描述的动作序列。然而，文本强化学习变体（GRPO with progress reward）的性能均未超过文本监督微调基线（Table 2, Table 7），暗示文本模态本身存在难以逾越的性能天花板。

**闭源多模态推理模型**（如**Gemini 2.5 Pro**）虽在简单场景中表现优异，但随着网格复杂度增加，其EM从**98%骤降至38.8%**（Figure 5），暴露出对分布内模式的过拟合倾向，缺乏系统性的空间泛化能力。

**纯视觉监督规划方法**（**LVM-7B + VPFT**）虽直接在视觉模态中操作，但采用教师强制（teacher-forcing）训练范式，导致策略熵在训练中迅速下降至零、无效动作比例攀升至**61%-78%**（Figure 6, Table 6），丧失了强化学习所需的探索能力。

### 核心动机：绕过语言中介的视觉规划

本文的核心假设是：在视觉-空间优先的任务中，**直接生成图像序列作为规划轨迹**比生成文本描述更能准确捕捉状态转移与空间关系。这一假设基于以下因果逻辑：

1. **模态保真度**：图像保留完整的空间信息（物体位置、障碍物分布、目标方位），无需经过有损的语言编码-解码过程。
2. **状态转移的自然表示**：每一步规划输出即为下一视觉状态，形成“初始状态→中间状态₁→中间状态₂→……→目标状态”的纯图像轨迹，与环境的真实动力学直接对齐。
3. **绕过描述误差**：消除坐标/ASCII描述中23%-26%的布局不匹配错误源。

基于此，本文提出**视觉规划（Visual Planning）**范式，将推理定义为纯粹在视觉模态中自回归生成图像序列的过程，并配套设计**VPRL（Visual Planning via Reinforcement Learning）**两阶段强化学习框架，以解决纯视觉策略的探索与优化问题。



## 核心方法与创新机理

本文提出**视觉规划（Visual Planning）**范式，其核心创新在于将空间推理的模态从文本符号切换为纯视觉图像序列，从而消除语言中介环节带来的信息损失。传统多模态模型在空间规划任务中依赖将视觉场景转换为文本描述（如坐标列表或ASCII布局）后再进行推理，该模态转换引入了显著的信息损失——实验表明，文本规划系统有25.7%的坐标描述和22.3%的ASCII描述与真实布局不匹配。视觉规划范式则直接自回归生成图像序列作为规划轨迹，每一步输出即为下一视觉状态，从根本上绕过了这一瓶颈。

围绕该范式，本文提出了**VPRL（Visual Planning via Reinforcement Learning）**，一个两阶段强化学习框架，在以下三个关键维度上区别于已有方法：

### 推理模态：从文本到纯视觉

| 维度 | 文本推理基线 | VPRL 视觉规划 |
|------|-------------|--------------|
| 推理模态 | 输出动作文本序列或带布局描述的动作序列 | 自回归生成图像序列，每一步即视觉状态 |
| 状态表示 | 坐标/ASCII等符号描述 | 直接生成下一帧图像 |
| 模态差距 | 存在（坐标描述25.7%不匹配，ASCII描述22.3%不匹配） | 消除语言中介，无模态转换损失 |

视觉规划的形式化定义为：给定初始视觉状态 $v_0$，策略模型 $\pi_\theta$ 自回归生成中间视觉状态序列：

$$\hat{v}_{i} \sim \pi_{\theta}(v_{i} | v_{0}, \hat{v}_{1}, \dots, \hat{v}_{i-1})$$

该范式基于 **Large Vision Model (LVM)**（Bai et al., 2024）实现，该模型仅使用图像和视频帧训练，不含任何文本数据，确保了推理过程完全在视觉模态内进行。

### 训练策略：两阶段强化学习替代单一监督微调

视觉规划基线 **VPFT（Visual Planning Fine-Tuning）** 采用单一阶段监督微调，在最优轨迹上训练LVM生成图像序列。然而，VPFT存在两个关键缺陷：

1. **探索能力不足**：VPFT通过teacher-forcing训练，策略熵在训练中迅速下降至接近零，同时无效动作比例上升，导致模型难以在RL阶段进行有效探索。
2. **无效动作控制弱**：VPFT因无效动作导致的失败比例高达61%–78%。

VPRL通过两阶段设计解决上述问题：

- **Stage 1 — 随机轨迹初始化**：利用随机游走数据训练模型输出有效图像，损失函数为VPFT损失：

  $$\mathcal{L}_{\mathrm{VPFT}}(\theta) = -\mathbb{E}_{(v_{\leq i}, \tilde{v}_{i+1})} \Big[ \log \pi_{\theta} \big( \tilde{v}_{i+1} \mid v_{\leq i} \big) \Big]$$

  该阶段使策略保持高熵（接近均匀随机规划器）且低无效动作比率，为后续RL提供探索友好的初始化。消融实验证实，Stage 1仅提供探索友好的初始化，不直接贡献规划能力——从Stage 1随机轨迹初始化的VPFT*性能低于标准VPFT。

- **Stage 2 — GRPO优化**：采用无需价值函数的GRPO（Group Relative Policy Optimization）进行策略优化，通过组内相对优势更新策略：

  $$A^{(k)} = \frac{r^{(k)} - \operatorname{mean}\{r^{(1)}, r^{(2)}, \dots, r^{(G)}\}}{\operatorname{std}\{r^{(1)}, r^{(2)}, \dots, r^{(G)}\}}$$

  最终优化目标为：

  $$\mathcal{T}_{\mathrm{VPRL}}(\theta) = \mathbb{E} \left[ \frac{1}{G} \sum_{i=1}^{G} \min\left( \rho^{(k)} A^{(k)}, \mathrm{clip}(\rho^{(k)}, 1-\epsilon, 1+\epsilon) A^{(k)} \right) - \beta D_{\mathrm{KL}}(\pi_{\theta} || \pi_{\mathrm{ref}}) \right]$$

### 奖励设计：基于进度估计的复合奖励

文本RL基线仅使用基于文本结果的奖励，而VPRL设计了基于进度估计与状态转移合法性划分的复合奖励函数。该奖励函数依赖两个核心组件：

- **Dynamics Interpreter（动力学解释器）**：基于规则的视觉状态转移解释器，将生成的图像对解析为有效/无效动作。
- **Progress Estimator（进度估计器）**：基于广度优先搜索（BFS）的进度图，评估当前状态到目标的最小步数。

生成状态被划分为三类并赋予不同奖励：

$$r(v_{i}, \hat{v}_{i+1}^{(k)}) = \alpha_{\mathrm{opt}} \cdot \mathbb{I}[\mathcal{D}(v_{i}, \hat{v}_{i+1}^{(k)}) \in \mathcal{A}_{\mathrm{opt}}] + \alpha_{\mathrm{nopt}} \cdot \mathbb{I}[\mathcal{D}(v_{i}, \hat{v}_{i+1}^{(k)}) \in \mathcal{A}_{\mathrm{nopt}}] + \alpha_{\mathrm{inv}} \cdot \mathbb{I}[\mathcal{D}(v_{i}, \hat{v}_{i+1}^{(k)}) \in \mathcal{E}_{\mathrm{inv}}]$$

实验中设定 $\alpha_{\mathrm{opt}}=1$（最优动作正向奖励），$\alpha_{\mathrm{nopt}}=0$（非最优有效动作中性），$\alpha_{\mathrm{inv}}=-5$（无效动作重罚）。这一设计使VPRL将因无效动作导致的失败比例相比VPFT降低至少24个百分点（VPFT 61%–78%，VPRL 25%–37%）。

### 创新的效果验证

上述三个changed slots的协同作用带来了显著的性能提升：VPRL在三个任务上的平均Exact Match达80.6%，比最强文本基线Qwen SFT的53.6%高出27个百分点。更重要的是，视觉规划在分布外场景下展现出更强的鲁棒性——随网格复杂度增加，VPRL的性能曲线保持平坦，而Gemini 2.5 Pro的EM从98%骤降至38.8%。文本RL基线（GRPO with progress reward或PR metric）均未超过文本SFT，进一步验证了文本模态在视觉-空间任务中存在根本性瓶颈，而非训练策略问题。



![[assets/figures/papers/paper_list_l45_https_openreview_net_forum_id_wsnse46kRO/figures/002_Figure_2.jpg]]
*Figure 2: An overview of the proposed VPRL framework, illustrated with autoregressive large vision models for image generation in the context of a visual navigation task. We train the visual policy model with GRPO, using the progress reward that encourages progressing actions and penalizes invalid actions, yielding goal-aligned visual planning*

### 范式定位：从文本中介到纯视觉推理

传统多模态模型在空间规划任务中遵循“视觉→文本→动作”的推理链路：先将场景图像转换为文本描述（坐标、ASCII布局等），再在文本空间进行规划。该模态转换环节构成关键瓶颈——分析显示，文本规划系统中有**25.7%的坐标描述和22.3%的ASCII描述与真实布局不匹配**，直接导致推理准确性受损。

VPRL（Visual Planning via Reinforcement Learning）提出**视觉规划**范式，彻底消除语言中介：模型直接以图像序列形式生成规划轨迹，每一步输出即为下一帧视觉状态，形成“视觉→视觉”的闭环推理。这一范式切换使平均精确匹配率（Exact Match）相比最强文本基线提升**27个百分点**（80.6% vs. 53.6%）。

### 核心架构与模块关系

VPRL框架由以下核心模块构成，其整体流程如Figure 2所示：

**1. 大视觉模型（LVM）骨干网络**
使用Bai et al.（2024）提出的LVM-7B作为自回归图像生成器。在视觉规划任务中，模型接收初始状态图像 $v_0$ 及已生成的历史状态序列 $\hat{v}_1, \dots, \hat{v}_{i-1}$，自回归地预测下一帧视觉状态：
$$\hat{v}_{i} \sim \pi_{\theta}(v_{i} \mid v_{0}, \hat{v}_{1}, \dots, \hat{v}_{i-1})$$
该模型完全在图像和视频帧数据上训练，不包含任何文本数据，从架构层面保证了纯视觉推理的可行性。

**2. 动力学解释器（Dynamics Interpreter）**
基于规则的视觉状态转移解释器，负责将相邻两帧图像对解析为具体的动作类型。它判断生成的状态是否对应有效的环境转移，并将动作划分为三类：最优动作（向目标前进）、非最优有效动作（合法但未缩短距离）、无效动作（违反环境约束，如穿墙、越界）。该模块是奖励计算的前置条件，目前为手工设计规则。

**3. 进度估计器（Progress Estimator）**
基于广度优先搜索（BFS）的进度图，为每个网格状态计算到达目标的最短步数 $P(v)$。通过比较当前状态与生成状态的进度值，判断动作是否朝向目标推进。该模块与动力学解释器协同工作，为奖励函数提供分类依据。

**4. 复合奖励函数（Composite Reward Function）**
将生成状态划分到三类并赋予差异化奖励：
$$r(v_{i}, \hat{v}_{i+1}^{(k)}) = \alpha_{\mathrm{opt}} \cdot \mathbb{I}[\mathcal{D} \in \mathcal{A}_{\mathrm{opt}}] + \alpha_{\mathrm{nopt}} \cdot \mathbb{I}[\mathcal{D} \in \mathcal{A}_{\mathrm{nopt}}] + \alpha_{\mathrm{inv}} \cdot \mathbb{I}[\mathcal{D} \in \mathcal{E}_{\mathrm{inv}}]$$
实验系数设置为 $\alpha_{\mathrm{opt}}=1$（最优动作），$\alpha_{\mathrm{nopt}}=0$（非最优有效动作），$\alpha_{\mathrm{inv}}=-5$（无效动作）。该设计同时鼓励目标对齐和状态合法性。

### 两阶段训练流程

VPRL采用递进式训练策略，解决视觉规划中探索与优化的平衡问题：

**Stage 1：随机轨迹初始化**
使用随机游走数据对LVM进行监督微调（VPFT），损失函数为：
$$\mathcal{L}_{\mathrm{VPFT}}(\theta) = -\mathbb{E}_{(v_{\leq i}, \tilde{v}_{i+1})} \Big[ \log \pi_{\theta} \big( \tilde{v}_{i+1} \mid v_{\leq i} \big) \Big]$$
该阶段不追求最优规划，而是让模型学会生成符合环境约束的有效图像状态。关键作用在于**保留策略的高熵特性**：消融实验表明（Figure 6），VPFT直接训练会导致策略熵迅速降至零，而Stage 1的随机初始化使策略保持接近均匀随机规划器的熵水平，同时维持较低的无效动作比率，为后续强化学习提供充分的探索空间。

**Stage 2：GRPO策略优化**
在Stage 1基础上，使用GRPO（Group Relative Policy Optimization）进行强化学习训练。GRPO无需价值函数，通过组内相对优势计算更新策略：
$$A^{(k)} = \frac{r^{(k)} - \operatorname{mean}\{r^{(1)}, r^{(2)}, \dots, r^{(G)}\}}{\operatorname{std}\{r^{(1)}, r^{(2)}, \dots, r^{(G)}\}}$$
完整优化目标为：
$$\mathcal{T}_{\mathrm{VPRL}}(\theta) = \mathbb{E} \left[ \frac{1}{G} \sum_{i=1}^{G} \min\left( \rho^{(k)} A^{(k)}, \mathrm{clip}(\rho^{(k)}, 1-\epsilon, 1+\epsilon) A^{(k)} \right) - \beta D_{\mathrm{KL}}(\pi_{\theta} || \pi_{\mathrm{ref}}) \right]$$
其中 $\rho^{(k)}$ 为重要性采样比率，KL惩罚项约束策略不偏离参考模型过远。

### 两阶段协同机制

Stage 1与Stage 2的分工明确且互补：Stage 1仅提供探索友好的初始化，本身不直接贡献规划能力——实验表明，从Stage 1初始化的VPFT*性能甚至低于标准VPFT（Table 8），证实其角色是**为RL创造探索条件而非传授规划策略**。Stage 2则利用复合进度奖励，引导模型从“能生成有效状态”进化为“能生成最优轨迹”。这一协同使VPRL相比纯监督的VPFT，将因无效动作导致的失败比例降低至少24%（VPFT 61-78%，VPRL 25-37%，Table 6）。



### 视觉规划的自回归生成范式

VPRL 的核心推理模态是纯视觉序列生成。给定初始视觉状态 $v_0$，模型自回归地生成后续中间状态，每一步以前序所有生成状态为条件：

$$\hat{v}_{i} \sim \pi_{\theta}(v_{i} \mid v_{0}, \hat{v}_{1}, \dots, \hat{v}_{i-1})$$

该范式与文本推理的本质区别在于：模型输出的是下一帧图像而非文本动作描述，从而绕过“视觉→文本→动作”的模态转换瓶颈。实验证据表明，文本规划系统有 **25.7% 的坐标描述和 22.3% 的 ASCII 描述与真实布局不匹配**，正是这一瓶颈的直接体现。

### 两阶段训练框架

VPRL 的训练分为两个阶段，分别解决探索能力初始化和规划能力优化两个子问题。

**Stage 1：随机轨迹初始化（VPFT）**

第一阶段采用监督微调，目标不是学习最优规划，而是让模型获得生成有效视觉状态的基本能力。训练数据来自随机游走轨迹，损失函数为：

$$\mathcal{L}_{\mathrm{VPFT}}(\theta) = -\mathbb{E}_{(v_{\leq i}, \tilde{v}_{i+1})} \Big[ \log \pi_{\theta} \big( \tilde{v}_{i+1} \mid v_{\leq i} \big) \Big]$$

其中 $\tilde{v}_{i+1}$ 是从当前状态 $v_i$ 的所有有效下一状态中随机采样的候选。这一设计的因果机制在于：随机初始化使策略保持高熵且低无效动作比率，为 Stage 2 的 RL 探索提供基础。消融实验证实，从 Stage 1 随机轨迹初始化的 VPFT* 性能低于标准 VPFT，说明 Stage 1 只提供探索友好初始化，不直接贡献规划能力。

**Stage 2：GRPO 策略优化**

第二阶段采用 GRPO（Group Relative Policy Optimization）进行强化学习训练。GRPO 无需学习价值函数，而是通过组内相对优势计算训练信号。对于每个状态 $v_i$，旧策略 $\pi_{\theta_{\text{old}}}$ 采样 $G$ 个候选下一状态 $\{\hat{v}_{i+1}^{(k)}\}_{k=1}^{G}$，各候选的奖励经组内标准化后得到相对优势：

$$A^{(k)} = \frac{r^{(k)} - \operatorname{mean}\{r^{(1)}, r^{(2)}, \dots, r^{(G)}\}}{\operatorname{std}\{r^{(1)}, r^{(2)}, \dots, r^{(G)}\}}$$

最终策略优化目标为：

$$\mathcal{T}_{\mathrm{VPRL}}(\theta) = \mathbb{E} \left[ \frac{1}{G} \sum_{i=1}^{G} \min\left( \rho^{(k)} A^{(k)}, \mathrm{clip}(\rho^{(k)}, 1-\epsilon, 1+\epsilon) A^{(k)} \right) - \beta D_{\mathrm{KL}}(\pi_{\theta} \| \pi_{\mathrm{ref}}) \right]$$

其中 $\rho^{(k)}$ 为重要性采样比率，$\epsilon$ 控制裁剪范围，$\beta$ 调节 KL 惩罚强度以约束策略不偏离参考策略过远。

### 复合进度奖励函数

奖励设计是 VPRL 将视觉规划与 RL 训练耦合的关键模块。系统包含两个辅助组件：

- **动力学解释器（Dynamics Interpreter）**：基于规则的视觉状态转移解释器，将图像对 $(v_i, \hat{v}_{i+1}^{(k)})$ 解析为有效或无效动作。
- **进度估计器（Progress Estimator）**：基于广度优先搜索（BFS）构建进度图，评估当前状态到目标的最小步数 $P(\cdot)$。

根据进度估计结果，生成的候选状态被划分为三类：

- $\mathcal{A}_{\mathrm{opt}}$：最优动作集合，满足 $P(\hat{v}_{i+1}^{(k)}) < P(v_i)$，即向目标前进了一步。
- $\mathcal{A}_{\mathrm{nopt}}$：非最优有效动作集合，满足 $P(\hat{v}_{i+1}^{(k)}) \geq P(v_i)$，即未前进或后退。
- $\mathcal{E}_{\mathrm{inv}}$：无效动作集合，即生成的视觉状态违反环境约束。

复合奖励函数对三类动作赋予不同系数：

$$r(v_{i}, \hat{v}_{i+1}^{(k)}) = \alpha_{\mathrm{opt}} \cdot \mathbb{I}[\mathcal{D}(v_{i}, \hat{v}_{i+1}^{(k)}) \in \mathcal{A}_{\mathrm{opt}}] + \alpha_{\mathrm{nopt}} \cdot \mathbb{I}[\mathcal{D}(v_{i}, \hat{v}_{i+1}^{(k)}) \in \mathcal{A}_{\mathrm{nopt}}] + \alpha_{\mathrm{inv}} \cdot \mathbb{I}[\mathcal{D}(v_{i}, \hat{v}_{i+1}^{(k)}) \in \mathcal{E}_{\mathrm{inv}}]$$

实验中系数设定为 $\alpha_{\mathrm{opt}}=1$，$\alpha_{\mathrm{nopt}}=0$，$\alpha_{\mathrm{inv}}=-5$。这一设计同时鼓励向目标前进、容忍非最优探索、严厉惩罚无效动作，使 VPRL 相比 VPFT 将无效动作导致的失败比例降低至少 24 个百分点（VPFT 61%-78%，VPRL 25%-37%）。

### 评价指标

**Exact Match（EM）**：整个生成轨迹与任一最短最优轨迹完全匹配则记为 1，否则为 0。允许存在多条最优解：

$$\mathrm{EM} = \max_{m \in \{1,\dots,M\}} \prod_{j=1}^{n} \mathbb{I}(\hat{v}_{j} = v_{j}^{(m)})$$

**Progress Rate（PR）**：测量从起点连续正确前进的步数比例，提供比 EM 更软的评价信号：

$$\mathrm{PR} = \max_{m \in \{1,\dots,M\}} \frac{1}{n} \sum_{j=1}^{n} \left[ \prod_{k=1}^{j} \mathbb{I}(\hat{v}_{k} = v_{k}^{(m)}) \right]$$



## 实验与关键发现

### 核心发现：视觉规划范式全面超越文本推理

本工作在三个视觉-空间规划任务（FROZENLAKE、MAZE、MINIBEHAVIOR）上系统对比了视觉规划与文本推理的性能。**核心结论明确：纯视觉规划范式在准确性和鲁棒性上均显著优于所有文本推理基线。**

Table 1 汇总了主实验结果。VPRL 在三个任务上的平均 Exact Match (EM) 达到 **80.6%**，而最强文本基线 Qwen SFT 仅为 53.6%，**平均 EM 高出 27 个百分点**。在 Progress Rate (PR) 指标上，VPRL 同样以 84.9% 的平均 PR 领先。这一优势在三个任务上表现一致：

![[assets/figures/papers/paper_list_l45_https_openreview_net_forum_id_wsnse46kRO/figures/003_Table_1.jpg]]
*Table 1: Performance of the closed- and open-source models on FROZENLAKE, MAZE, and MINIBEHAVIOR. VPRL performs consistently the best (bold) across all tasks. † denotes the posttrained model. ~ represents texts and Õ represents images. The last column AVG. reports the average performance across three tasks*

- **FROZENLAKE**：VPRL 取得 **91.6% EM**，远超 Qwen SFT 的 68.6% 和 Gemini 2.5 Pro 的 72.0%（Table 1）。
- **MAZE**：VPRL 取得 **74.5% EM**，Qwen SFT 为 60.9%，领先 13.6 个百分点。
- **MINIBEHAVIOR**：VPRL 取得 **75.8% EM**，Qwen SFT 仅 31.3%，**领先幅度高达 44.5 个百分点**，表明视觉规划在物体操作类任务上的优势尤为突出。

值得注意的是，所有文本推理变体——无论是闭源的 Gemini 2.0 Flash (Direct/CoT)、Gemini 2.5 Pro，还是开源的 Qwen 2.5-VL-Instruct (Direct/CoT/SFT/RL)——平均 EM 均低于 50%。**文本 GRPO 基线（使用进度奖励或 PR 指标）甚至未能超越文本 SFT**（Table 2, Table 7），进一步印证了视觉-文本模态转换瓶颈的存在。

![[assets/figures/papers/paper_list_l45_https_openreview_net_forum_id_wsnse46kRO/figures/005_Table_2.jpg]]
*Table 2: Performance of text-based planning variants on FROZENLAKE. See Table 7 in Appendix F.2 for the full results*

![[assets/figures/papers/paper_list_l45_https_openreview_net_forum_id_wsnse46kRO/figures/014_Table_7.jpg]]
*Table 7: Performance of text-based variants of Qwen-2.5-VL-Instruct-3B and 7B on FROZENLAKE. We report Exact Match (EM) and Progress Rate (PR) across all difficulty levels (L3–L6) and their average*

### 模态差距的量化证据

文本推理在视觉-空间任务中的失效并非偶然。错误分析揭示了系统性的模态转换失真：**25.7% 的坐标描述和 22.3% 的 ASCII 描述与真实布局不匹配**（Section 4）。这意味着近四分之一的文本规划输出在“翻译”视觉场景时就已经出错，后续推理建立在错误的表征之上。

相比之下，视觉规划直接在图像空间中操作，无需将场景编码为语言符号，从根本上规避了这一信息损失。

### 两阶段训练的有效性

VPRL 的两阶段 RL 框架是其性能优势的关键。消融实验揭示了以下因果链条：

**Stage 1 的探索初始化作用**：直接使用 VPFT（监督微调）初始化的策略进行 GRPO 训练效果不佳。VPFT 在训练过程中策略熵迅速下降至接近零，同时无效动作比率攀升，导致 RL 阶段缺乏有效探索信号（Figure 6）。VPRL Stage 1 使用随机轨迹初始化，使策略保持接近均匀随机规划器的高熵，同时将无效动作比率控制在较低水平，为 Stage 2 的 GRPO 优化提供了良好的探索起点。

**Stage 1 本身不贡献规划能力**：从 Stage 1 随机轨迹初始化的 VPFT* 性能低于标准 VPFT（Table 8），证实 Stage 1 仅提供探索友好的初始化，而非直接的规划能力提升。

![[assets/figures/papers/paper_list_l45_https_openreview_net_forum_id_wsnse46kRO/figures/015_Table_8.jpg]]
*Table 8: Exact Match performance of VPFT and VPFT* across different grid sizes in FROZENLAKE*

**Stage 2 的 RL 优化效果**：VPRL Stage 2 相比 Stage 1 在所有三个任务上均有大幅提升（Table 10），验证了 GRPO 配合进度奖励的有效性。VPRL 将因无效动作导致的失败比例相比 VPFT **降低至少 24%**（VPFT 61%-78%，VPRL 25%-37%，Table 6），表明 RL 训练有效约束了动作合法性。

![[assets/figures/papers/paper_list_l45_https_openreview_net_forum_id_wsnse46kRO/figures/012_Table_6.jpg]]
*Table 6: We compute the percentage of failed trajectories that are caused by at least one invalid action, rather than a suboptimal but valid action. Lower values indicate better action validity control*

![[assets/figures/papers/paper_list_l45_https_openreview_net_forum_id_wsnse46kRO/figures/024_Table_10.jpg]]
*Table 10: Performance comparison of VPRL Stage 1 and Stage 2 across all three tasks*

### 分布外鲁棒性与复杂度扩展

视觉规划展现出显著优于文本推理的分布外鲁棒性。Figure 5 展示了 FROZENLAKE 上不同网格大小的性能变化曲线：随着网格从 3×3 增大到 6×6，**Gemini 2.5 Pro 的 EM 从 98% 骤降至 38.8%**，而 VPRL 的 EM 仅从 97.6% 降至 82.4%，性能曲线明显更平坦。MAZE 和 MINIBEHAVIOR 上呈现相同趋势（Figure 10）。

在分布外泛化实验中（Table 9），模型在小网格上训练、大网格上评估，视觉规划方法同样表现出更强的迁移能力。

![[assets/figures/papers/paper_list_l45_https_openreview_net_forum_id_wsnse46kRO/figures/016_Table_9.jpg]]
*Table 9: Out-of-distribution (OOD) performance on enlarged grids. Models are trained on smaller grids and evaluated on the sizes indicated in parentheses*

### 推理鲁棒性

VPRL 对生成图像的中间伪影具有鲁棒性。Table 11 显示，推理时使用环境真实图像替换自生成图像，性能几乎不变（平均 EM 91.6 vs 92.1），说明视觉规划不依赖像素级精确重建，而是捕捉了状态转移的语义本质。

![[assets/figures/papers/paper_list_l45_https_openreview_net_forum_id_wsnse46kRO/figures/031_Table_11.jpg]]
*Table 11: Exact Match (EM) and Progress Rate (PR) on FROZENLAKE under VPRL when using ground-truth images versus self-generated images as inputs during inference*

此外，在输入图像部分遮挡的扰动条件下，VPRL 仍能保持与可见结构一致的规划轨迹（Figure 12），进一步验证了其鲁棒性。

### 计算成本

视觉规划的推理 Token 成本约为同规模文本 CoT 的 3 倍（Table 12），但仍低于 Gemini 2.5 Pro 等高级推理模型。这一开销主要源于图像 Token 的高维度，但考虑到性能提升幅度，在计算上仍属可行。

### 失败模式分析

VPRL 的失败轨迹主要分为两类：**无效动作**（生成的状态不符合环境转移规则）和**非最优有效动作**（动作合法但未朝向目标推进）。Table 6 显示 VPRL 已将无效动作失败比例大幅压缩，但非最优路径仍是剩余错误的主要来源。这提示复合奖励函数中 $\alpha_{\text{nopt}} = 0$ 的设置可能过于保守，适度惩罚非最优动作或引入更细粒度的进度信号可能进一步提升性能。

### 补充图表

![[assets/figures/papers/paper_list_l45_https_openreview_net_forum_id_wsnse46kRO/figures/009_Table_3.jpg]]
*Table 3: Distribution of training dataset by grid sizes for each task. Value indicates the number of environments*

![[assets/figures/papers/paper_list_l45_https_openreview_net_forum_id_wsnse46kRO/figures/010_Table_4.jpg]]
*Table 4: Number of training and test samples for each task and method. For visual planning, the numbers here are represented in image pairs, which correspond to the same number of trajectories for SFT in Text*

![[assets/figures/papers/paper_list_l45_https_openreview_net_forum_id_wsnse46kRO/figures/011_Table_5.jpg]]
*Table 5: Hyper-parameters of training both textual and visual planners*



## 定位与知识库关联

### 1. 范式定位：从文本中介到纯视觉推理

当前多模态视觉-语言模型在执行空间规划任务时，普遍遵循“视觉→文本→推理→文本→动作”的流水线：模型首先将视觉场景转换为文本描述（如坐标列表或ASCII布局），再基于文本进行规划推理，最后输出文本动作序列。本文揭示，这一模态转换环节构成了核心瓶颈——分析显示，文本规划系统有25.7%的坐标描述和22.3%的ASCII描述与实际布局不匹配，直接导致信息损失与规划错误。因此，**VPRL** 的根本贡献不在于提出新的网络架构，而在于**切换了推理模态**：将规划过程完全保留在视觉空间内，自回归地生成图像序列作为规划轨迹，从而消除了语言中介带来的模态差距。

这一范式转换将VPRL置于一条区别于主流多模态推理的研究脉络中。传统方法可大致分为两类：

- **文本推理基线**：包括 **Qwen 2.5-VL-Instruct-7B** 的直接生成（Direct）、思维链（CoT）、监督微调（SFT）及GRPO强化学习变体，以及闭源模型 **Gemini 2.0 Flash** 和 **Gemini 2.5 Pro**。这些方法均在文本空间进行规划，性能受限于上述模态转换瓶颈——即使在最强的文本RL设置下，其性能也未超过文本SFT，进一步支持了文本模态在视觉-空间任务中存在固有瓶颈的判断。

- **纯视觉监督基线**：**VPFT**（Visual Planning Fine-Tuning）在 **LVM-7B**（Bai et al., 2024）上对最优轨迹进行监督微调，直接生成图像序列。VPFT证明了纯视觉规划的可行性，但其依赖教师强制训练，导致策略熵迅速下降至零且无效动作比例升高（61%-78%），缺乏探索能力。

VPRL通过两阶段强化学习框架（随机轨迹初始化 + GRPO进度奖励优化）解决了VPFT的探索不足问题，同时保持了纯视觉推理的优势。其因果机制清晰：Stage 1的随机策略初始化使策略保持高熵且低无效动作比率，为Stage 2的RL优化提供了有效的探索空间；Stage 2的复合奖励函数（最优动作+1，非最优有效动作0，无效动作-5）引导策略向目标对齐。

### 2. 适用边界与泛化能力

**任务域**：VPRL在三个视觉导航与操作任务上验证有效——FROZENLAKE（网格导航）、MAZE（迷宫求解）、MINIBEHAVIOR（物体操作）。这些任务的共同特征是状态转移完全可通过视觉观察，且环境动力学相对简单（离散网格、有限动作空间）。论文明确指出，该方法聚焦于“状态转移在视觉上可观测”的任务，区别于代码生成或传统视觉问答等以语言为中心的任务。

**分布外鲁棒性**：VPRL展现出显著的分布外泛化优势。随着FROZENLAKE网格尺寸从3×3增大到6×6，VPRL的EM从97.6%降至82.4%，而Gemini 2.5 Pro从98.0%骤降至38.8%（Figure 5）。在更大的未见过网格上，VPRL同样保持相对平坦的性能曲线。此外，推理时使用环境真实图像替换自生成图像几乎不影响性能（平均EM 91.6 vs 92.1），表明视觉规划对中间帧的图像伪影具有鲁棒性。

**计算成本**：视觉规划的推理Token成本约为同规模文本CoT的3倍，但低于Gemini 2.5 Pro等需要深度思考的模型。在计算上仍处于可行范围。

### 3. 关键局限与失效模式

**手工规则依赖**：当前VPRL框架的动力学解释器（Dynamics Interpreter）和进度估计器（Progress Estimator）均为手工设计的规则模块。动力学解释器通过比较生成图像与当前状态图像的差异来判定动作有效性，进度估计器基于广度优先搜索（BFS）构建进度图。这种设计便于分析和验证，但严重限制了向更复杂、更真实环境的扩展——当视觉状态连续或高维时，手工规则难以定义有效的状态比较和进度评估。

**状态空间扩展瓶颈**：Stage 1需要枚举所有可能的随机轨迹来初始化策略网络。当状态空间增大时（如连续控制或大规模环境），这一枚举的计算开销将不可接受。论文已明确承认这一限制。

**图像生成质量**：中间帧带有tokenizer引入的伪影。尽管实验表明这对当前任务的规划性能影响有限，但在需要高精度视觉判别的任务中（如精细操作、医学图像导航），伪影可能成为显著干扰源。

**任务范围受限**：仅在网格导航及简单物体操作任务上验证，在3D场景推理、物理动力学预测、需要丰富视觉理解的任务中的有效性完全未知。

### 4. 开放问题与未来方向

1. **跨模态规划扩展**：能否将纯视觉规划范式推广到更通用的跨模态生成模型，支持包含文本、图像甚至视频的混合规划序列？这需要模型同时理解多种模态的状态表示。

2. **可扩展的动力学解释器**：如何构建鲁棒且可扩展的视觉状态转移解释器？可能的方向包括基于模型的模块或可学习的状态比较函数，以替代当前的手工规则。

3. **端到端奖励信号**：是否可以用轨迹终端的成功信号直接作为奖励，替代需要显式状态对解析和进度估计的复合奖励设计？这将大幅简化训练流程并提升可扩展性。

4. **更紧凑的视觉表示**：能否设计更紧凑的图像标记化表示来降低推理成本？当前3倍的Token开销在资源受限场景中仍是实际障碍。

5. **更强生成模型的利用**：能否利用扩散模型等更强的图像生成骨干网络，进一步提升规划质量和视觉保真度？

6. **更广泛任务的验证**：该范式在3D空间推理、物理动力学预测、具身操作等更复杂的视觉-认知任务中是否依然有效？这需要构建相应的基准和环境。



## 原文 PDF

![[paperPDFs/ICLR_2026/Visual_Planning_Lets_Think_Only_with_Images.pdf]]
