---
title: "Thinking in 360deg: Humanoid Visual Search in the Wild"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/Thinking_in_360deg_Humanoid_Visual_Search_in_the_Wild.pdf
project_link: "https://humanoid-vstar.github.io"
code_link: null
aliases:
- HVSH
- T3HVSW
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: 将MLLM的工具调用（head rotation）与物理动作耦合，形成主动头部旋转的闭环感知-行动范式，并通过多轮推理（SFT+RL）赋予模型探索和策略性决策的能力。
primary_logic: 利用360°全景图像作为轻量级模拟器，将视觉搜索建模为一系列透视视角下的头部旋转动作序列；通过两阶段后训练（多轮SFT注入行为先验，再通过GRPO强化学习优化长程探索策略），使模型在无硬件约束的条件下具备主动、可扩展的具身空间推理能力。
claims:
- 即使是最先进的专有模型在H*Bench上的成功率也仅约30%，表明现有MLLM缺乏具身视觉搜索能力。
- 后训练使3B模型的物体搜索成功率从14.83%提升至47.38%，路径搜索从6.44%提升至24.94%，验证了SFT+RL范式的有效性。
- 主动视觉搜索（透视视图旋转）显著优于被动的全景分析。
- 跨任务训练能够双向提升性能，表明物体搜索和路径搜索共享底层空间推理能力。
---

# Thinking in 360deg: Humanoid Visual Search in the Wild

> [!tip] 核心洞察
> 利用360°全景图像作为轻量级模拟器，将视觉搜索建模为一系列透视视角下的头部旋转动作序列；通过两阶段后训练（多轮SFT注入行为先验，再通过GRPO强化学习优化长程探索策略），使模型在无硬件约束的条件下具备主动、可扩展的具身空间推理能力。

| 字段 | 内容 |
|------|------|
| 中文题名 | 在360°中思考：人形机器人在野外的视觉搜索 |
| 英文题名 | Thinking in 360deg: Humanoid Visual Search in the Wild |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://openaccess.thecvf.com/content/CVPR2026/html/Yu_Thinking_in_360deg_Humanoid_Visual_Search_in_the_Wild_CVPR_2026_paper.html) · [Project](https://humanoid-vstar.github.io) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/image_and_video_generation |
| Method | Humanoid Visual Search (HVS) |
| Dataset | H*Bench HOS Overall, H*Bench HPS Overall |

> [!tip] 效果简介
> - H*Bench HOS Overall 上，Success Rate (%) 47.38 (HVS-3B) vs 14.83 (Qwen2.5-VL-3B-Instruct) (+32.55)；Success Rate (%) 40.83 (HVS-3B w/ SFT only) vs 14.83 (Qwen2.5-VL-3B-Instruct) (+26.00)；Success Rate (%) 47.38 (HVS-3B) vs 31.96 (Gemini2.5-Pro) (+15.42)。
> - H*Bench HPS Overall 上，Success Rate (%) 24.94 (HVS-3B) vs 6.44 (Qwen2.5-VL-3B-Instruct) (+18.50)。

## 概要

**核心问题：多模态大模型缺乏具身空间推理能力。** 当前最先进的多模态大模型（MLLM）在复杂真实环境中执行视觉搜索任务时表现乏力——即使是最强的专有模型，在 H*Bench 上的成功率也仅约 30%。其根本瓶颈在于：现有模型缺乏空间常识与主动 3D 规划能力，无法像人类一样通过主动调整视角来探索未知环境，尤其在需要精细空间推理和社会规范的路径搜索任务上短板尤为突出。

**核心思路：将 360° 全景作为轻量级模拟器，以主动头部旋转驱动闭环感知-行动循环。** 本文提出 **Humanoid Visual Search (HVS)** 范式，将视觉搜索建模为一系列透视视角下的头部旋转动作序列。具体而言，HVS 将 MLLM 的工具调用（头部旋转）与物理动作耦合——模型在每一步接收窄视场透视图像，输出旋转动作来改变观察方向，形成闭环的感知-行动周期。这一设计以单张 360° 全景图像作为环境模拟器，在无需硬件约束的条件下实现了可扩展的具身空间推理。

**关键技术路径：两阶段后训练赋予模型探索与策略决策能力。** HVS 采用“监督微调（SFT）+ 强化学习（RL）”的两阶段后训练范式：第一阶段通过多轮 SFT 注入行为先验，使模型建立从透视图像到合理动作的基础映射；第二阶段采用 GRPO 强化学习优化长程探索策略，培养模型在不确定环境中进行策略性决策的能力。

**主要结果：后训练带来三倍以上性能提升，但路径搜索仍具挑战。** 在最小的 3B 模型上，HVS 将物体搜索成功率从 14.83% 提升至 47.38%（+32.55 个百分点），路径搜索从 6.44% 提升至 24.94%（+18.50 个百分点），验证了 SFT+RL 范式的有效性。消融实验进一步揭示：主动视觉搜索显著优于被动的全景分析，且物体搜索与路径搜索之间存在可迁移的空间推理能力。然而，路径搜索在中高难度级别上的提升有限，RL 训练甚至可能导致性能退化，表明当前方法在注入物理、空间和社会常识方面仍存在明显不足。

### 从被动描述到主动搜索的范式缺口

当前多模态大语言模型（MLLM）在视觉理解任务上取得了显著进展，但其能力边界仍停留在“描述所见”的被动模式——给定一张静态图像，模型输出一段文字描述或回答相关问题。然而，真实世界中的具身智能体面临的挑战远不止于此：一个类人机器人需要在复杂的三维环境中**主动转动头部**，通过多视角观察来搜索目标物体或规划行进路径。这种“在 360° 中思考”的能力，要求模型具备空间常识、主动规划与闭环感知-行动循环，而现有 MLLM 在这些维度上表现出明显的推理短板。

论文将这一任务形式化为 **人形视觉搜索（Humanoid Visual Search, HVS）**：智能体从一个窄视场（narrow FOV）的透视视角出发，在由单张 360° 全景图像表示的沉浸式环境中，通过主动旋转头部来搜索目标物体或路径。与传统的 2D 视觉问答不同，HVS 是**交互式**的——每个头部旋转动作都会改变智能体的视觉输入，形成闭环的感知-行动循环。

### 现有方法的根本局限

现有视觉搜索方法存在两个核心瓶颈：

**（1）缺乏空间常识与主动 3D 规划能力。** 当前最先进的专有模型在 H*Bench 基准上的成功率仅约 30%（Gemini2.5-Pro 在物体搜索上为 31.96%，路径搜索为 33.00%；GPT-4o 仅约 20%），这表明即使是最强大的 MLLM，在需要精细空间推理和社会规范理解的任务上也力不从心。模型无法有效判断“向哪个方向看”以及“何时停止搜索并提交答案”。

**（2）被动分析范式与具身搜索的本质不匹配。** 现有方法要么在静态 2D 图像内进行裁剪/缩放操作，要么直接分析完整的全景图。前者将视觉搜索退化为 2D 画布上的计算操作，缺乏物理交互；后者虽能“一览无余”，但全景图的畸变与 MLLM 训练时使用的透视图像分布存在冲突，导致模型难以有效利用全景信息。消融实验证实，主动视觉搜索（透视视图旋转）显著优于被动的全景分析，原因有二：主动范式更接近人类的高效搜索策略，且避免了全景畸变对模型先验的干扰。

### 本文动机与核心思路

上述缺口催生了本文的核心动机：**能否让 AI 智能体像人类一样，在 3D 世界中主动搜索，而非仅仅被动描述？**

为实现这一目标，论文提出了一套可扩展的范式，其核心洞察在于：**利用 360° 全景图像作为轻量级模拟器，将视觉搜索建模为一系列透视视角下的头部旋转动作序列**。具体而言，该方法将 MLLM 的工具调用（head rotation）与物理动作耦合，形成主动头部旋转的闭环感知-行动范式，并通过两阶段后训练赋予模型探索和策略性决策的能力：

- **阶段一（SFT）**：使用带有人工修正思维链（CoT）的多轮轨迹进行监督微调，注入基本的行为先验（如“看到墙壁时应该转身”）。
- **阶段二（RL）**：采用 GRPO（Group Relative Policy Optimization）对 SFT 策略进行强化学习微调，培养长程探索与策略性决策能力（如“持续探索直到获得足够证据再提交”）。

这一范式使模型在无硬件约束的条件下具备主动、可扩展的具身空间推理能力，为从“被动描述者”到“主动搜索者”的转变提供了可行路径。

## 核心方法与创新机理

本工作针对当前多模态大模型（MLLM）在具身视觉搜索中暴露出的空间常识与主动3D规划短板，提出了**Humanoid Visual Search（HVS）**范式，其核心创新可归纳为以下三个维度的“changed slots”。

### 1. 视觉搜索范式：从被动描述到主动闭环感知

现有MLLM的视觉搜索停留在对静态2D图像进行裁剪、缩放等画布操作，缺乏与物理世界的交互（baseline_value）。HVS将其重构为**在360°全景环境中的主动头部旋转闭环**：智能体以窄视场（narrow FOV）透视图像为输入，每次头部旋转动作改变其视觉观测，形成“感知—推理—行动—再感知”的完整闭环（proposed_value）。这一范式的关键洞察在于，**360°全景图像充当了轻量级环境模拟器**，使模型无需依赖3D仿真或真实硬件即可获得主动探索的经验——每个旋转动作直接对应全景球面上的方位角与俯仰角变化，从而将具身空间推理从硬件约束中解放出来。

### 2. 行动空间：从2D画布操作到物理耦合的旋转动作

传统方法在2D画布上执行区域选择或缩放操作（baseline_value），而HVS定义了与物理世界耦合的**离散动作原语**（proposed_value）：
- **Rotate**：以相对偏航角 $\Delta\phi$ 和俯仰角 $\Delta\gamma$ 旋转头部，改变观测视角；
- **Submit**：当智能体确信已定位目标方向时，提交最终估计并终止搜索。

这一设计将MLLM的工具调用能力与物理动作耦合，使模型在推理过程中显式地控制“看哪里”，而非被动接受全图信息。实验证明，这种主动范式显著优于被动的全景图分析——后者因全景畸变与MLLM训练先验冲突而表现不佳，而主动搜索更贴近人类的高效搜索策略。

### 3. 训练目标：从单轮监督到多轮SFT+RL的策略优化

现有方法通常依赖单轮监督微调或零样本推理（baseline_value），难以培养长程探索与策略性决策能力。HVS引入**两阶段后训练管线**（proposed_value）：
- **Stage 1 多轮SFT**：利用GPT-4o生成并经人工修正的思维链（CoT）轨迹进行监督学习，注入基础行为先验（如“看到墙壁时应转身探索”）；
- **Stage 2 多轮强化学习（RL）**：采用**GRPO（Group Relative Policy Optimization）**对SFT策略进行微调，通过组内相对奖励优化探索策略，使模型学会在获取充分证据后才提交最终估计。

消融实验表明，SFT使3B模型的物体搜索成功率从14.83%跃升至40.83%，路径搜索从6.44%提升至23.00%；RL在此基础上进一步将物体搜索推至47.38%（+6.55个百分点），验证了“行为先验注入+策略探索优化”两阶段范式的有效性。值得注意的是，RL在路径搜索上的增益有限（仅+1.94个百分点），且在中高难度级别出现性能退化，这揭示了当前奖励设计与真实任务目标之间的偏差——这也是后续研究需要突破的关键瓶颈。

Humanoid Visual Search (HVS) 将具身视觉搜索建模为一个**闭环感知-行动周期**：智能体在由单张360°全景图像表示的沉浸式环境中，通过主动旋转头部来获取窄视场（FOV）透视图像，并基于多轮多模态推理逐步定位目标物体或路径。整个框架的核心思想是将多模态大模型（MLLM）的工具调用能力与物理世界的头部旋转动作耦合，从而在无需真实机器人硬件的条件下实现可扩展的具身空间推理。

### 管道模块与数据流

HVS 的完整管道由四个关键模块串联组成，形成从环境模拟到策略优化的端到端流程：

**1. 360° 全景模拟器（360° Panorama Simulator）**
该模块是环境的轻量级替代品。给定一张野外采集的360°全景图像，模拟器根据当前的头部偏航角 $\phi$ 和俯仰角 $\gamma$，从中渲染出对应的窄FOV透视视图 $o_{\phi,\gamma}$。这使得智能体每次执行“旋转”动作时，都能获得一个与其注视方向一致的新视觉输入，从而闭合感知-行动循环。这一设计的核心优势在于**绕过了对3D仿真或物理硬件的依赖**，使得大规模训练和评估成为可能。

**2. 工具增强的 MLLM 策略（Tool-Augmented MLLM Policy）**
这是框架的推理核心。给定语言指令 $x$、当前透视观察 $o_t$ 和历史动作序列 $H_t$，MLLM 策略 $\pi_\theta(y_t, a_t \mid o_t, x, H_t)$ 同时生成思维链推理文本 $y_t$ 和一个动作 $a_t$。动作空间包含两种基元：
- **旋转（Rotate）**：输出相对方位角变化 $\Delta\phi$ 和俯仰角变化 $\Delta\gamma$，驱动模拟器更新视角。
- **提交（Submit）**：输出最终估计的绝对目标方向 $(\phi, \gamma)$，表示智能体认为目标所在的最佳注视方向。

这种设计将视觉搜索转化为一个**多模态推理任务**：模型需要像人类一样，在看到不充分的证据时选择探索（旋转），在积累足够信息后自信地提交最终判断。

**3. 监督微调（Supervised Fine-Tuning, SFT）**
SFT 阶段的目标是注入基本的任务导向行为先验。训练数据由 GPT-4o 生成的思维链推理轨迹经人工修正后构建，包含多轮交互中的合理动作序列（例如，看到空白墙壁时选择转身探索）。这一阶段赋予模型将透视图像映射到合理动作的基础能力，为后续的强化学习优化奠定冷启动基础。

**4. 多轮强化学习（Multi-Turn RL with GRPO）**
RL 阶段采用组相对策略优化（Group Relative Policy Optimization, GRPO）对 SFT 策略进行进一步微调。与 SFT 的模仿学习不同，RL 通过奖励信号鼓励模型发展出**战略性探索能力**：智能体学会在信息不足时持续旋转以收集证据，仅在获得足够置信度时才执行提交动作。这一阶段的关键在于培养长程推理和策略性决策能力，而非简单的单步反应。

### 两阶段后训练的逻辑

图2清晰地展示了 SFT 和 RL 两个阶段的递进关系：
- **SFT** 提供“看到什么就做什么”的基础反应模式（如看到死胡同时转身）；
- **RL** 将这种反应细化为“为了最大化任务成功概率，我应该如何序列化地探索”的战略性策略。

这种分阶段设计使得模型能够先掌握基本的行为语法，再在此基础上发展出面向任务目标的优化策略，从而在 H*Bench 的物体搜索和路径搜索任务上均取得显著提升。

### 补充图表

![[assets/figures/papers/paper_list_l1082_https_openaccess_thecvf_com_content_CVPR2026_html_Yu_Thinking_in_360deg/figures/002_Figure_2.jpg]]
*Figure 2: Pipeline Illustration. Stage 1 (SFT) provides the foundational ability to map perspective images to plausible actions (e.g., turning around upon seeing nothing). Stage 2 (RL) refines this into a strategic policy: the model learns to explore (outputting*

### 3.1 问题形式化：最优视角方向

HVS将人形视觉搜索建模为在360°全景空间中寻找最优头部朝向的决策问题。给定语言指令 $x$ 和当前窄视角观察 $o_{\phi,\gamma}$，模型需要输出使任务成功概率最大化的方位角 $\phi$ 与俯仰角 $\gamma$：

$$(\phi^*, \gamma^*) = \arg \max_{\phi, \gamma} P(r_s \mid o_{\phi, \gamma}, x)$$

其中 $r_s$ 表示任务成功状态，$o_{\phi,\gamma}$ 是从全景图中以 $(\phi,\gamma)$ 为中心渲染的窄视场透视图像。该目标将视觉搜索转化为一个主动感知问题：模型必须通过一系列旋转动作逐步逼近最优方向，而非一次性分析完整全景图。

### 3.2 工具增强的MLLM策略

方法的核心是将MLLM的工具调用能力与物理头部旋转动作耦合，构建闭环感知-行动周期。策略 $\pi_\theta$ 在每个时间步 $t$ 接收当前透视观察 $o_t$、语言指令 $x$ 和历史上下文 $H_t$，输出思维链 $y_t$ 和动作 $a_t$：

$$\pi_\theta(y_t, a_t \mid o_t, x, H_t)$$

**动作空间**由两个原语组成：
- **旋转动作** $a_t^{rot} = (\Delta\phi, \Delta\gamma)$：调整头部偏航角和俯仰角，改变下一时刻的视觉输入
- **提交动作** $a_t^{sub}$：当模型积累足够证据后，提交最终的目标方向估计

这一设计使视觉搜索从静态2D图像分析转变为交互式具身推理任务——每次旋转都改变感知输入，形成渐进式信息收集过程。

### 3.3 两阶段后训练管线

**阶段一：多轮监督微调（SFT）**。使用GPT-4o生成初始思维链，经人工修正后构建多轮交互轨迹数据。SFT的目标是注入基本行为先验：将透视图像映射到合理动作（如看到空白墙壁时选择转身探索）。训练环境基于LLaMA-Factory实现。

**阶段二：多轮强化学习（RL）**。在SFT策略基础上，采用Group Relative Policy Optimization（GRPO）进行强化学习微调。RL阶段的奖励函数基于任务成功与否设计，目标是培养长程探索与策略性决策能力——模型学会在探索（持续输出 $a_t^{rot}$）与利用（在获得充分证据后输出 $a_t^{sub}$）之间做出权衡。RL训练基于VAGEN框架实现。

### 3.4 评价容差区域

为评估搜索是否成功，论文定义了以标注最优方向为中心的容差窗口：

$$[\phi^* - \tau_{\phi}, \phi^* + \tau_{\phi}] \times [\gamma^* - \tau_{\gamma}, \gamma^* + \tau_{\gamma}]$$

其中容差参数 $\tau_{\phi}$ 由物体边界框宽度与预设基础容差共同决定：

$$\tau_{\phi} = \max\left(\frac{w_{\phi}}{2}, \tau_{\phi}^{base}\right)$$

$w_{\phi}$ 为物体在方位角方向的边界框宽度，$\tau_{\phi}^{base}$ 为基础容差。当模型提交的方向落在此区域内时，判定搜索成功。这一设计既考虑了物体本身的空间范围，也保留了合理的判断弹性。

## 实验与关键发现

### 实验设置与评估协议

实验围绕提出的 **H\*Bench** 基准展开，该基准包含物体搜索（HOS）和路径搜索（HPS）两个任务族，并按难度划分为 Easy、Medium、Extreme 三个级别。评估指标为成功率（Success Rate），其判定标准为：模型提交的最终方向 $(\phi, \gamma)$ 是否落在以标注最优方向 $(\phi^*, \gamma^*)$ 为中心的容差区域内：

$$[\phi^* - \tau_\phi, \phi^* + \tau_\phi] \times [\gamma^* - \tau_\gamma, \gamma^* + \tau_\gamma]$$

其中 $\tau_\phi = \max(\frac{w_\phi}{2}, \tau_\phi^{\text{base}})$，容差基于物体边界框在360°全景上的反投影宽度与预设基础容差共同确定。

后训练基线统一采用混合数据集（物体搜索+路径搜索）进行微调。SFT阶段基于LLaMA-Factory框架实现，RL阶段使用VAGEN框架进行多轮GRPO训练。零样本基线覆盖开源模型 **InternVL3.5-4B/8B**、**Qwen2.5-VL-3B/7B-Instruct**，以及闭源模型 **Gemini2.5-Pro**、**GPT-4o**。

### 主结果：后训练带来的性能跃升

Table 1 汇总了各模型在 H\*Bench 上的完整结果。核心发现如下：

![[assets/figures/papers/paper_list_l1082_https_openaccess_thecvf_com_content_CVPR2026_html_Yu_Thinking_in_360deg/figures/005_Table_1.jpg]]
*Table 1: Left: Quantitative results of open-source, proprietary, and fine-tuned models on H∗Bench. Top-three performances are highlighted with red , green and blue . Right: Performance comparison of the best-in-class open-source, proprietary, and fine-tuned models*

**零样本基线的困境。** 即使是最强的闭源模型 Gemini2.5-Pro，在 HOS 整体成功率也仅为 31.96%，在 HPS 上为 33.00%。开源模型中，Qwen2.5-VL-3B-Instruct 的 HOS 成功率仅 14.83%，HPS 仅 6.44%。这验证了核心瓶颈：当前多模态大模型缺乏具身视觉搜索所需的空间常识与主动规划能力。

**SFT 注入行为先验。** 经过多轮 SFT，Qwen2.5-VL-3B 的 HOS 成功率从 14.83% 跃升至 40.83%（+26.00 pp），HPS 从 6.44% 提升至 23.00%（+16.56 pp）。这表明通过人工修正的 CoT 轨迹进行行为克隆，能有效建立基本的探索-提交动作映射。

**RL 进一步优化策略。** 在 SFT 基础上叠加 GRPO 强化学习后，HVS-3B 的 HOS 成功率进一步提升至 47.38%（+6.55 pp），HPS 提升至 24.94%（+1.94 pp）。最终，HVS-3B 相比零样本基线实现了超过三倍的提升，并显著超越 Gemini2.5-Pro（HOS: 47.38 vs 31.96）。

**模型规模的边际收益。** 采用更大基座模型（Qwen3-VL-8B）进行 SFT 后，HVS-8B 在 HOS 上达到 60.29% 的整体成功率，表明更强的视觉-语言基础能力有助于空间推理。

### 消融实验：各组件贡献的精细解耦

**SFT 与 RL 的分阶段贡献。** Table 1 的对比清晰展示了两个阶段的独立增益。在物体搜索上，RL 在 SFT 基础上额外贡献了 6.55 个百分点，且 Figure 6（左）显示 RL 后的累积成功率随探索步数增长更快，验证了 RL 培养了更高效的长程探索策略。然而，在路径搜索中，RL 的提升幅度有限（+1.94 pp），且存在关键退化现象：HPS Medium 难度从 SFT 的 23.03% 降至 RL 后的 20.18%，Extreme 难度从 14.81% 降至 12.04%。这说明当前 GRPO 的奖励设计在复杂空间推理任务上存在偏差，模型可能在优化奖励信号时牺牲了泛化能力。

**交叉任务训练揭示可迁移的空间推理能力。** Figure 4 展示了任务族间训练的交叉效应。仅用物体搜索数据训练的模型，在 HPS 上的成功率从零样本的 6.4% 提升至 20.7%；反之，仅用路径搜索数据训练的模型，在 HOS 上的成功率从 14.8% 提升至 29.5%。这种双向提升表明，物体搜索和路径搜索共享底层的空间推理能力（如视角规划、环境探索策略），后训练可以部分迁移这些能力。值得注意的是，在 HPS Easy 难度上，物体搜索模型甚至超越了专用的 HPS 模型（37.8% vs 33.8%），暗示物体搜索训练可能培养了更灵活的探索行为。

**主动搜索 vs 被动全景分析。** Figure 7（左）的对比实验直接验证了核心设计选择：主动视觉搜索（透视视角下的渐进式旋转探索）显著优于被动分析完整全景图。论文指出两个关键原因：(1) 主动范式模仿了人类高效的目标搜索策略；(2) 全景图存在畸变，与 MLLM 训练时接触的透视图像分布不一致，导致直接全景分析性能下降。

**奖励塑形的局限性。** Table 2 系统探索了 GRPO 在 HPS 上的多种奖励塑形策略，包括形状奖励（form）、校正奖励（corr）、距离奖励（dist）的组合。结果显示，所有变体仅在 Easy 难度上有效，在 Medium 和 Extreme 难度上普遍出现性能退化。这表明当前奖励函数难以捕捉路径搜索所需的物理常识（如可通行性判断）、空间常识（如楼梯与平面的功能区分）和社会规范（如机场入口提示），这些知识隐含、情境化且程序性，难以通过简单的奖励信号注入。

### 失败模式分析

Figure 5（左）展示了 HPS 任务中的三类典型失败案例：

![[assets/figures/papers/paper_list_l1082_https_openaccess_thecvf_com_content_CVPR2026_html_Yu_Thinking_in_360deg/figures/006_Figure_5.jpg]]
*Figure 5: Left: Failure cases in HPS. (a) Vision-action mismatch. (b) Attempting to traverse an impassable surface instead of using the staircase. (c) Missing socio-spatial conventions (e.g., airport entrance cues). Right: H∗Bench results breakdown of Gemma3-4B-it*

1. **视觉-动作不匹配（Vision-action mismatch）：** 模型正确识别了目标方向，但输出的旋转动作与视觉推理不一致，导致探索方向错误。
2. **物理常识缺失：** 模型试图穿越不可通行的表面（如直接穿过栏杆），而非使用旁边的楼梯，表明缺乏对3D空间可通行性的基本理解。
3. **社会-空间规范缺失：** 模型忽略了场景中的社会空间线索（如机场入口标识），选择了不符合人类行为规范的路径。

这些失败模式与消融实验中 HPS 中高难度级别的性能退化高度一致，共同指向当前后训练范式的根本局限：SFT+RL 可以有效提升视觉定位和探索策略，但难以注入物理、空间和社会常识。

### 上下文长度的影响

Figure 6（右）展示了测试时上下文长度对成功率的影响。随着允许的最大交互轮数增加，成功率整体呈上升趋势，但存在边际递减效应。这表明更长的探索预算确实有助于信息收集，但模型的策略效率仍有提升空间。

![[assets/figures/papers/paper_list_l1082_https_openaccess_thecvf_com_content_CVPR2026_html_Yu_Thinking_in_360deg/figures/008_Figure_6.jpg]]
*Figure 6: Left: Cumulative success rate by step before and after RL (t indicates maximum turn limit in RL training). Right: Impact of test-time context length on success rate*

### 补充图表

![[assets/figures/papers/paper_list_l1082_https_openaccess_thecvf_com_content_CVPR2026_html_Yu_Thinking_in_360deg/figures/004_Figure_4.jpg]]
*Figure 4: Comparison of In-task (train and test on the same task family) and Cross-task (train on one task family and test on the other)*

![[assets/figures/papers/paper_list_l1082_https_openaccess_thecvf_com_content_CVPR2026_html_Yu_Thinking_in_360deg/figures/007_Figure_7.jpg]]
*Figure 7: Left: Comparison of active and passive visual search. Right: Comparison of different visual search paradigms*

## 定位与知识库关联

### 1. 问题定位：MLLM的空间推理瓶颈

当前多模态大模型（MLLM）在具身视觉搜索任务上表现出明显的推理短板。H*Bench的零样本评测显示，即使是最先进的专有模型，在物体搜索（HOS）和路径搜索（HPS）上的成功率也仅约30%（Gemini2.5-Pro：HOS 31.96%，HPS 33.00%），而GPT-4o仅约20%。这表明现有MLLM缺乏在复杂3D环境中进行主动、多步空间推理的能力——它们擅长被动描述所见内容，却无法像人类一样通过主动调整视角来搜索目标。

核心瓶颈在于两个层面：
- **感知层面**：模型习惯处理静态2D图像，缺乏对3D空间关系和视角变化的建模能力。
- **决策层面**：路径搜索需要精细的空间推理和社会规范理解（如机场入口标识、楼梯与坡道的可通行性判断），这些常识在现有模型的训练分布中严重不足。

### 2. 方法谱系：视觉搜索范式的演进

本文提出的Humanoid Visual Search（HVS）处于视觉搜索与具身导航的交叉地带，其方法定位可从以下维度理解：

#### 2.1 从被动分析到主动搜索

传统MLLM的视觉搜索范式是在静态2D图像内进行裁剪、缩放或区域选择操作，无物理交互含义。HVS的关键突破在于将MLLM的工具调用（head rotation）与物理动作耦合，形成**闭环感知-行动周期**：每个头部旋转动作（Δϕ, Δγ）都会改变视觉输入，模型需根据新观测逐步推理并决策下一步动作。这一范式转变使模型从“被动描述者”升级为“主动搜索者”。

消融实验（Figure 7）直接验证了主动范式的优势：主动视觉搜索（透视视图逐步旋转探索）显著优于被动的全景图一次性分析。原因有二：（1）主动搜索模仿了人类高效的信息收集策略；（2）全景图存在畸变，与MLLM训练时的透视图像分布不一致，导致被动分析性能下降。

#### 2.2 与视觉导航方法的关系

HVS与经典视觉导航（Visual Navigation）的区别在于抽象层次。视觉导航通常需要完整的3D仿真环境或真实硬件，关注连续动作空间中的避障和路径规划。HVS则聚焦于**关键决策点**——即“朝哪个方向看”和“何时提交答案”——从而绕过了对3D仿真或物理硬件的依赖，直接用360°全景图像作为轻量级模拟器。这一设计使得大规模、低成本的数据采集和训练成为可能。

#### 2.3 训练范式的创新

基线方法多采用单轮监督微调（SFT）或零样本推理。HVS采用**两阶段后训练**：
- **Stage 1（多轮SFT）**：使用GPT-4o生成CoT推理链，经人工修正后注入行为先验，使模型建立“看到什么→转向哪里”的基础映射。
- **Stage 2（多轮GRPO强化学习）**：在SFT基础上用Group Relative Policy Optimization（GRPO）优化长程探索策略，培养模型在信息不完整时持续探索、在证据充分时果断提交的策略性决策能力。

实验表明，SFT带来显著增益（HOS：14.83%→40.83%；HPS：6.44%→23.00%），RL在物体搜索上进一步提升了6.55个百分点。但在路径搜索中，RL仅在简单样本上有效，中等和极端难度甚至出现性能退化（HPS medium：23.03%→20.18%；extreme：14.81%→12.04%），说明现有奖励设计与真实任务目标存在偏差。

### 3. 知识库定位：贡献与适用边界

#### 3.1 核心贡献

1. **任务定义与基准**：首次将人形视觉搜索形式化为360°全景中的主动头部旋转任务，并构建了H*Bench（涵盖物体搜索HOS和路径搜索HPS两个子任务，含难度分级）。
2. **可扩展的训练范式**：证明了“多轮SFT + GRPO强化学习”的后训练管线能显著提升小模型（3B）的空间推理能力，无需依赖昂贵硬件。
3. **跨任务可迁移性证据**：物体搜索训练可将路径搜索从6.4%提升至20.7%，路径搜索训练可将物体搜索从14.8%提升至29.5%，表明两类任务共享底层空间推理能力。

#### 3.2 适用边界与局限

1. **路径搜索的性能天花板**：HPS的性能提升远低于HOS（3B模型仅24.94%），尤其在需要物理常识（如判断表面可通行性）和社会空间规范（如识别机场入口）的场景中，后训练难以注入这些隐式、情境化的知识。
2. **奖励设计的困境**：在HPS的GRPO中尝试了多种奖励塑形策略（形状、校正、距离的组合），均只在简单难度上有效，难以全面提升（Table 2）。这暴露了当前RL奖励函数在复杂空间推理任务中的根本局限。
3. **数据标注成本**：SFT数据依赖GPT-4o生成CoT和人工修正，成本高且难以大规模扩展，限制了模型的进一步scaling。
4. **评估的局限性**：实验仅在H*Bench上进行，未在实际机器人或更复杂的动态环境中验证泛化性。与基线的比较也主要覆盖开源7B/8B模型和少数闭源模型，未全面涵盖现有2D视觉搜索方法的适配版本。
5. **计算效率未讨论**：未涉及模型在不同计算条件下的推理延迟，而这对于实时人形机器人应用至关重要。

### 4. 开放问题

1. **鲁棒奖励函数设计**：如何为路径搜索设计能同时提升简单和困难样本、且不易被gaming的奖励函数？
2. **空间世界知识的预训练注入**：能否通过预训练直接注入面向行动的空间世界常识，从而减少对精心标注SFT数据的依赖？
3. **混合任务训练的难度平衡**：如何平衡HOS与HPS混合训练中的难度分布，避免RL阶段出现负迁移？
4. **范式扩展**：将HVS扩展到多模态交织推理（如与操纵、导航协同）会遇到哪些新挑战？360°全景模拟器的抽象层次是否足以支撑更复杂的交互？

## 原文 PDF

![[paperPDFs/CVPR_2026/Thinking_in_360deg_Humanoid_Visual_Search_in_the_Wild.pdf]]
