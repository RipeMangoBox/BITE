---
title: "Vision-Zero: Scalable VLM Self-Evolution via Multi-Agent Self-Play"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/Vision_Zero_Scalable_VLM_Self_Evolution_via_Multi_Agent_Self_Play.pdf
project_link: null
code_link: https://github.com/wangqinsi1/Vision-Zero
openreview_forum_id: s00SNXREV6
aliases:
- VZISPPOIS
- Vision-Zero
tags:
- ICLR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/vision_models_multimodal
core_operator: "通过设计一种基于“谁是间谍”规则的多智能体自我博弈视觉游戏，使VLM在无需任何人工标注的情况下通过竞争互动自主生成训练数据，并利用交替优化（Iterative-SPO）持续提升视觉理解与推理能力。"
primary_logic: "将社交推理游戏的机制映射到VLM训练中，利用不对称视觉输入（平民观察真实图像，间谍接收空白图像）创造了一个零和博弈环境，迫使模型在提供线索与识别间谍的过程中主动发展细粒度视觉比较、逻辑推理和策略性沟通能力。"
claims:
- "Vision-Zero在完全不使用人工标注的情况下，在推理、图表问答和视觉中心任务上超越了多个依赖昂贵人工标注的SOTA方法。"
- "所提出的Iterative-SPO交替训练算法能够避免纯自我博弈的局部均衡，并在训练效率上较纯GRPO提升3.3x至6.4x。"
- "角色优势估计（RAE）模块对于消除角色信息不对称至关重要，移除后模型性能反而低于原始基座模型。"
- "MathVista 上 Accuracy = 72.2 (VisionZero-Qwen-7B CLEVR)"
---

# Vision-Zero: Scalable VLM Self-Evolution via Multi-Agent Self-Play

> [!tip] 核心洞察
> 将社交推理游戏的机制映射到VLM训练中，利用不对称视觉输入（平民观察真实图像，间谍接收空白图像）创造了一个零和博弈环境，迫使模型在提供线索与识别间谍的过程中主动发展细粒度视觉比较、逻辑推理和策略性沟通能力。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | Vision-Zero：通过多智能体自我博弈实现可扩展视觉语言模型自进化 |
| 英文题名 | Vision-Zero: Scalable VLM Self-Evolution via Multi-Agent Self-Play |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=s00SNXREV6) · [GitHub](https://github.com/wangqinsi1/Vision-Zero) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/vision_models_multimodal |
| Method | Vision-Zero with Iterative Self-Play Policy Optimization (Iterative-SPO) |
| Dataset | MathVista, BLINK, ChartXiv_RQ |

> [!tip] 效果简介
> - MathVista 上，Accuracy 为 72.2 (VisionZero-Qwen-7B CLEVR)，对比 68.2 (Qwen2.5-VL-7B)，变化 +4.0。
> - BLINK 上，Accuracy 为 57.2 (VisionZero-Qwen-7B Real-World)，对比 55.2 (Qwen2.5-VL-7B)，变化 +2.0。
> - ChartXiv_RQ 上，Accuracy 为 45.8 (VisionZero-Qwen-7B Chart)，对比 42.5 (Qwen2.5-VL-7B)，变化 +3.3。

## 概要

当前视觉语言模型（VLM）的后训练范式高度依赖人工标注或专家整理的高质量问答对。无论是监督微调（SFT）还是基于可验证奖励的强化学习（RLVR），其性能上限都被固化为人类提供的监督信号水平，模型无法自主发现超越人类经验的推理策略。此外，昂贵的数据构建成本严重制约了训练数据的规模与多样性。

Vision-Zero 提出了一条根本不同的路径：**将 VLM 训练重构为一个标签无关、领域无关的多智能体自我博弈游戏**。其核心思想源于社交推理游戏“谁是间谍”——平民观察真实图像，间谍仅接收空白图像，双方通过多轮自然语言线索进行策略性对抗。这种不对称视觉输入天然构造了一个零和博弈环境，迫使模型在提供线索与识别间谍的过程中主动发展细粒度视觉比较、逻辑推理和策略性沟通能力，而整个过程**完全不依赖任何人工标注**。

在训练算法层面，Vision-Zero 提出了 **Iterative Self-Play Policy Optimization（Iterative-SPO）**，在自我博弈（Self-Play）与 RLVR 之间交替优化。其中，**角色优势估计（RAE）** 模块通过指数移动平均消除不同角色固有的胜率不对称性，是稳定训练的关键——消融实验表明，移除 RAE 后模型性能反而低于原始基座模型（Table 13）。

在推理、图表问答和视觉中心理解等多项基准上，Vision-Zero 在完全不使用人工标注的条件下，超越了多个依赖昂贵标注数据的 SOTA 方法（Figure 2; Table 1; Table 2）。消融实验进一步揭示：增加平民玩家数量（2→4人）和多轮线索交互（1→3轮）均能显著提升推理能力，验证了更复杂的社交博弈环境对模型能力增长的驱动作用。



视觉语言模型（VLM）近年来在推理、图表理解和视觉中心任务上取得了显著进展，但其能力提升仍高度依赖人类专家标注的高质量训练数据。当前主流范式——无论是监督微调（SFT）结合人类反馈强化学习（RLHF），还是基于可验证奖励的强化学习（RLVR）——都面临一个根本性瓶颈：**模型的推理能力被固化在人类提供的监督信号水平上，无法自主发现超越人类经验的策略**。同时，大规模人工标注的成本高昂，严重制约了训练数据的规模与多样性。

图 Figure 1 清晰地展示了这一困境：监督学习完全依赖人工策划的推理轨迹；而强化学习虽然允许模型通过验证奖励自主探索推理过程，其训练数据仍然依赖专家设计的问答对。这意味着，模型的上限被人为标注的质量和覆盖范围所限定，难以实现真正的自主进化。

针对这一缺口，本文提出 **Vision-Zero**，一个完全无需人工标注的多智能体自我博弈框架。其核心动机在于：**将社交推理游戏的机制映射到 VLM 训练中，利用不对称视觉输入创造零和博弈环境，迫使模型在竞争互动中主动发展细粒度视觉比较、逻辑推理和策略性沟通能力**。具体而言，Vision-Zero 设计了一种基于“谁是间谍”规则的视觉游戏——平民观察真实图像，间谍接收空白图像——使模型在提供线索与识别间谍的过程中自主生成训练数据，并通过交替优化算法持续提升推理能力。这一范式转变使得 VLM 的训练首次完全摆脱了对人类经验的依赖，为可扩展的自进化视觉智能开辟了新路径。



## 核心方法与创新机理

Vision‑Zero 的核心创新在于**将 VLM 的训练从“依赖人类标注的静态监督”彻底转变为“多智能体自我博弈驱动的动态自进化”**，在三个相互耦合的维度上实现了系统性突破。

### 1. 标签无关的自我博弈数据生成

传统 VLM 后训练（SFT、RLHF、RLVR）的根基是人工标注或专家整理的 QA 对（如 **R1‑OneVision‑7B**、**MM‑Eureka‑Qwen‑7B** 等基线均依赖此类数据）。这一依赖造成了双重瓶颈：数据规模与多样性受限于标注成本，且模型的推理能力被锁定在人类提供的监督信号水平上，无法自主发现超越人类经验的策略。

Vision‑Zero 通过引入**“谁是间谍”风格的多智能体视觉游戏**，彻底切断了这一依赖。游戏规则创造了天然的信息不对称——平民观察真实图像，间谍接收空白图像——迫使模型在提供线索与识别间谍的竞争互动中，自主生成海量训练数据。这一过程**无需任何人工标注**，且图像输入可以是合成场景（CLEVR）、图表或真实自然图像，实现了领域无关的数据生成。从 changed‑slot 视角看，**训练数据来源从“人类标注的 QA 对”变为“自我博弈游戏自主生成的标签无关数据”**，这是整个范式转换的基石。

### 2. 零和博弈驱动的奖励设计

传统 RLVR 的奖励函数依赖人工设计或验证，难以捕捉视觉推理中微妙而丰富的策略性行为。Vision‑Zero 利用游戏本身的零和结构，设计了**无需外部监督的内生奖励机制**：

- **线索阶段**采用零和博弈奖励（Eq. 1）：间谍的奖励与得票偏差异号，平民的奖励包含全局任务奖励和个体一致性惩罚，自然驱动模型发展出既具信息量又避免暴露身份的线索策略。
- **决策阶段**采用离散稀疏奖励（Eq. 4）：投票正确得 +1，弃权得 –0.5，错误得 –1，鼓励模型在不确定时承认不确定性，而非盲目猜测。
- **角色优势估计（RAE）**（Eq. 2）通过指数移动平均消除间谍与平民因信息不对称带来的固有胜率差异，是稳定自我博弈训练的关键模块——消融实验（Table 13）证实，移除 RAE 后模型平均准确率降至 37.4，远低于基线的 41.1。

这一奖励设计使得**训练范式从“依赖人工设计奖励的 RLVR”变为“以零和博弈内生奖励驱动的自我博弈”**。

### 3. 交替优化防止局部均衡

纯自我博弈训练容易陷入局部均衡：当间谍的线索策略过于隐晦时，平民无法有效识别间谍，训练信号消失；反之，当平民过于强大时，间谍无法学习。Vision‑Zero 提出的 **Iterative Self‑Play Policy Optimization（Iterative‑SPO）** 通过**在自我博弈与 RLVR 之间交替优化**来解决这一问题。

交替由滞后阈值控制器（Eq. 9‑10）自动触发：当决策阶段准确率上升且弃权率下降时，表明线索阶段策略趋于饱和，训练自动切换至线索阶段优化；当间谍难以被识别时，则切回决策阶段。这一机制在训练效率上较纯 GRPO 提升 **3.3× 至 6.4×**（Figure 7），并在 LogicVista 上显著优于纯自我博弈和纯 RLVR（Figure 8）。

### 创新点之间的因果链条

三个创新并非孤立存在，而是形成了一条因果闭环：**自我博弈游戏**创造了无需标注的数据生成环境与零和博弈结构 → **零和奖励与 RAE** 将博弈结果转化为有效的训练信号 → **Iterative‑SPO 交替优化**防止博弈陷入局部均衡，持续推动能力提升。这一闭环使得 VLM 能够在完全脱离人类经验的情况下，自主发展出细粒度视觉比较、逻辑推理和策略性沟通能力，最终在推理、图表问答和视觉中心任务上超越依赖昂贵人工标注的 SOTA 方法（Figure 2, Table 1‑2）。



![[assets/figures/papers/paper_list_l41_https_openreview_net_forum_id_s00SNXREV6/figures/005_Figure_3.jpg]]
*Figure 3: Overall Framework of Vision-Zero. Vision-Zero comprises three core components. Strategic Game Environment: Each role is required to exhibit strategic behavior tailored to diverse scenarios, thereby simultaneously necessitating multiple capabilities. Label-free and Domainagnostic Data Input: Vision-Zero accepts arbitrary inputs to promote diversity and generalization. To verify this, we train Qwen2.5-VL-7B for 100 iterations on Gobang and our environment and evaluate on MathVision; results show that Vision-Zero effective generalization. Iterative-SPO: We introduce a novel two-stage training algorithm. In the clue stage, models are trained via Self-Play using a zero-sum reward inversely propo...*

![[assets/figures/papers/paper_list_l41_https_openreview_net_forum_id_s00SNXREV6/figures/003_Figure_1.jpg]]
*Figure 1: Vision-Zero Paradigm. (a) Supervised learning depends on human-curated reasoning trajectories; (b) Reinforcement Learning, although enabling models to autonomously learn reasoning processes via validated rewards, still relies heavily on expert-designed question-answer pairs. (c) In contrast, Vision-Zero is a novel self-improvement paradigm entirely independent of human experience. It constructs self-play games by leveraging image pairs that exhibit visual differences. Through the interactive and strategic game, Vision-Zero continuously generates training data for VLMs, enabling the model to achieve scalable self-improvement*

Vision-Zero 的整体框架由三个核心组件构成：**战略性游戏环境**、**标签无关且领域无关的数据输入**，以及 **迭代式自我博弈策略优化（Iterative-SPO）**。框架的核心设计理念是将社交推理游戏“谁是间谍”映射到视觉语言模型的训练中，通过多智能体竞争互动自主生成训练信号，彻底摆脱对人类标注数据的依赖。

### 2.1 战略性游戏环境

游戏环境模拟一个零和博弈场景：每局游戏包含 $n_c$ 名平民（civilians）和一名间谍（spy）。平民观察到同一张真实图像 $I_c$，而间谍接收空白视觉输入 $I_s$。游戏分为两个阶段：

- **线索阶段（Clue Stage）**：所有玩家依次发表自然语言线索。平民需提供足够具体以证明自己“看到了图像”、但又不至于直接暴露图像内容的描述；间谍则需根据已发表的线索进行推理，编造与图像主题一致但模糊的线索以避免暴露。
- **决策阶段（Decision Stage）**：所有玩家基于全部历史线索进行推理，投票指认谁是间谍。

这种不对称视觉输入的设计创造了一个天然的竞争环境：平民必须发展细粒度视觉比较和策略性沟通能力，间谍必须发展逻辑推理和上下文整合能力。

### 2.2 标签无关的领域无关数据输入

Vision-Zero 的数据生成不依赖任何人工标注或专家整理的问答对。其核心机制是利用**图像编辑器**对任意输入图像生成差异化图像对。具体而言：

- 给定一张任意领域的图像 $I$，通过编辑操作（如属性修改、物体增删、颜色变换等）生成变体图像 $I'$。
- 平民观察原始图像 $I$，间谍观察空白图像，但间谍需要猜测图像内容并模仿平民的发言风格。

论文在实验中使用了三类代表性数据：CLEVR 合成场景、图表数据（Chart-based）和真实自然图像（Real-world），验证了框架的领域无关性。由于整个过程仅需未标注的原始图像，数据构建成本为零。

### 2.3 迭代式自我博弈策略优化（Iterative-SPO）

Iterative-SPO 是框架的训练核心，它在自我博弈（Self-Play）和可验证奖励强化学习（RLVR）之间交替进行，以解决纯自我博弈容易陷入局部均衡或发散的问题。

#### 线索阶段训练

线索阶段采用**零和奖励**设计。对于间谍 $s$ 和平民 $c_j$，奖励函数为：

$$r_{s}^{clue} = -\beta (v_{s} - \bar{v}_{c}), \quad r_{c_j}^{clue} = \frac{\beta}{n_{c}} (v_{s} - \bar{v}_{c}) - \lambda (v_{c_j} - \bar{v}_{c})$$

其中 $v_s$ 是间谍在决策阶段获得的票数，$\bar{v}_c$ 是平民的平均得票数。这一设计的直觉是：间谍被正确指认（高票）时受到惩罚，平民被误投时受到惩罚；同时引入个体一致性惩罚项 $\lambda(v_{c_j} - \bar{v}_c)$，防止平民生成过于突兀的线索。

为消除角色固有的不对称优势，框架引入了**角色优势估计（Role-Advantage Estimation, RAE）**模块：

$$b_s = \alpha b_s + (1-\alpha) r_s^{clue}, \quad b_c = \alpha b_c + (1-\alpha) \frac{1}{n_c} \sum_j r_{c_j}^{clue}$$

$$A_k^{clue} = r_k^{clue} - b_k$$

通过指数移动平均分别估计间谍和平民角色的基线奖励，从原始奖励中减去角色基线得到标准化的优势估计 $A_k^{clue}$。消融实验表明，移除 RAE 后模型平均准确率降至 37.4，甚至低于基座模型的 41.1，证实该模块是平衡角色不对称性的关键。

#### 决策阶段训练

决策阶段采用**离散稀疏奖励**。每个平民 $c_i$ 的投票结果 $\hat{s}_{c_i}$ 与真实间谍身份 $s^\star$ 比较：

$$r_{c_i}^{dec} = +1 \text{ if } \hat{s}_{c_i} = s^\star, \quad -0.5 \text{ elif } \hat{s}_{c_i} = \varnothing, \quad -1 \text{ else}$$

其中 $\varnothing$ 表示“无法确定”（弃权）。这一设计鼓励模型在不确定时承认不确定性，而非盲目猜测。

#### 迭代阶段切换

为防止训练停滞，框架根据决策阶段的准确率和弃权率动态切换训练阶段：

$$m_{t+1} = 1 \text{ if } m_t=0, \overline{\text{acc}}_t \geq \tau_{\text{acc}}^{\uparrow}, \overline{\text{na}}_t \leq \tau_{\text{na}}^{\downarrow}$$

$$m_{t+1} = 0 \text{ if } m_t=1, (1-\overline{\text{acc}}_t \geq \tau_{\text{err}}^{\uparrow} \text{ or } \overline{\text{na}}_t \geq \tau_{\text{na}}^{\uparrow})$$

其中 $\overline{\text{acc}}_t$ 和 $\overline{\text{na}}_t$ 分别为准确率和弃权率的指数移动平均，$\tau$ 为滞后阈值。当决策阶段表现饱和（准确率高、弃权率低）时，切换至线索阶段训练；当间谍识别变得困难时，切换回决策阶段。同时引入最小驻留时间 $K_{\text{min}}$ 防止阶段震荡。

### 2.4 框架整体流程

Figure 3 展示了 Vision-Zero 的完整 pipeline：

1. **数据输入**：任意图像通过编辑器生成差异化图像对，构建游戏场景。
2. **角色分配**：随机分配 $n_c$ 名平民和 1 名间谍，平民观察真实图像，间谍接收空白输入。
3. **线索阶段**：所有玩家依次生成自然语言线索，收集完整对话历史 $H$。
4. **决策阶段**：平民基于历史 $H$ 推理并投票指认间谍。
5. **奖励计算**：根据投票结果计算线索阶段零和奖励和决策阶段离散奖励，通过 RAE 消除角色偏差。
6. **策略更新**：使用 GRPO 算法更新模型参数，交替优化线索策略和决策策略。
7. **阶段切换**：根据性能指标自动切换训练阶段，防止局部均衡。

这种设计使得模型在无需任何人工标注的情况下，通过竞争互动自主发展出细粒度视觉理解、逻辑推理和策略性沟通能力。



Vision-Zero 的训练框架围绕一个非对称视觉博弈环境构建，其核心由**线索阶段**与**决策阶段**两个策略模块、**角色优势估计（RAE）** 以及**迭代阶段控制器**组成。以下逐一解析各模块的机制与关键公式。

### 2.1 线索阶段：零和博弈奖励

在每一轮游戏的线索阶段，间谍观察到空白图像 $I_s$，而 $n_c$ 名平民观察到真实图像 $I_c$。所有玩家依次发表自然语言线索，随后进行一轮匿名投票，每名玩家投票选出自己认为是间谍的人。记间谍得票数为 $v_s$，平民 $j$ 得票数为 $v_{c_j}$，平均平民得票 $\bar{v}_c = \frac{1}{n_c} \sum_j v_{c_j}$。

线索阶段的奖励设计遵循严格的零和原则，迫使间谍与平民之间形成策略性对抗：

$$r_{s}^{\text{clue}} = -\beta (v_{s} - \bar{v}_{c})$$

$$r_{c_j}^{\text{clue}} = \frac{\beta}{n_{c}} (v_{s} - \bar{v}_{c}) - \lambda (v_{c_j} - \bar{v}_{c})$$

其中 $\beta, \lambda$ 为超参数（实验中均设为 $0.\bar{1}$）。间谍的奖励与自身得票偏离平均平民得票的程度呈负相关——得票越多，惩罚越重，从而迫使间谍生成与平民高度相似的线索以隐藏身份。平民的奖励由两部分构成：全局任务项 $\frac{\beta}{n_c}(v_s - \bar{v}_c)$ 鼓励平民群体将票投给间谍，个体一致性惩罚项 $-\lambda(v_{c_j} - \bar{v}_c)$ 则抑制个别平民发表过于突兀的线索而被误认为间谍。这种设计使奖励总和恒为零，构建了一个寻求均衡的动态系统。

### 2.2 角色优势估计（RAE）

由于间谍与平民之间存在固有的信息不对称（间谍仅看到空白图像），不同角色的胜率天然存在差异。若直接使用原始奖励进行策略优化，模型可能学到利用角色先验而非发展真正的推理能力。RAE 模块通过指数移动平均（EMA）估计各角色的基线奖励，从而消除这一系统性偏差：

$$b_{s} = \alpha b_{s} + (1-\alpha) r_{s}^{\text{clue}}, \quad b_{c} = \alpha b_{c} + (1-\alpha) \frac{1}{n_{c}} \sum_{j} r_{c_j}^{\text{clue}}$$

$$A_{k}^{\text{clue}} = r_{k}^{\text{clue}} - b_{k}$$

其中 $\alpha$ 为衰减因子，$b_s$ 和 $b_c$ 分别为间谍与平民角色的 EMA 基线奖励。最终的优势估计 $A_k^{\text{clue}}$ 将原始奖励减去对应角色的基线，使不同角色的优势值具有可比性。消融实验（Table 13）表明，移除 RAE 后模型平均准确率降至 37.4，远低于基线的 41.1，证实该模块是平衡角色不对称性的关键组件。

基于 RAE 得到的优势估计，线索阶段的策略优化目标为：

$$\mathcal{L}^{\text{clue}}(\theta) = -\mathbb{E}\left[\frac{1}{n}\sum_{k\in\mathcal{K}} A_{k}^{\text{clue}} \log \pi_{\theta}^{k}(u_{k} \mid I_{k}, h)\right] + \tau_{\text{clue}} \mathbb{E}\left[\frac{1}{n}\sum_{k\in\mathcal{K}} D_{\mathrm{KL}}(\pi_{\theta}^{k} \parallel \pi_{\text{ref}}^{k})\right]$$

其中 $\mathcal{K}$ 为所有玩家集合，$u_k$ 为玩家 $k$ 生成的线索 token 序列，$h$ 为历史线索上下文，$\tau_{\text{clue}}$ 控制 KL 散度正则化强度，防止策略偏离参考模型过远。

### 2.3 决策阶段：离散稀疏奖励

在决策阶段，每位平民基于所有历史线索 $H$ 独立推理并投票指认间谍 $\hat{s}_{c_i}$。该阶段的奖励设计为离散稀疏形式，鼓励模型在不确定时承认不确定性：

$$r_{c_i}^{\text{dec}} = \begin{cases} +1, & \text{if } \hat{s}_{c_i} = s^{\star} \\ -0.5, & \text{if } \hat{s}_{c_i} = \varnothing \\ -1, & \text{otherwise} \end{cases}$$

其中 $s^{\star}$ 为真实间谍标签，$\varnothing$ 表示弃权（输出“not a spy”）。正确指认同伴得 +1，弃权得 -0.5，错误指认得 -1。这一设计使盲目猜测的期望收益为负，有效抑制了模型的投机行为。

决策阶段的优化目标为：

$$\mathcal{L}^{\text{dec}}(\theta) = -\mathbb{E}\left[\frac{1}{n_c}\sum_{i=1}^{n_c} A_{c_i}^{\text{dec}} \log q_{\theta}(\hat{s}_{c_i} \mid H)\right] + \tau_{\text{dec}} \mathbb{E}\left[\frac{1}{n_c}\sum_{i=1}^{n_c} D_{\mathrm{KL}}(q_{\theta} \parallel q_{\text{ref}})\right]$$

其中 $q_{\theta}$ 为决策策略，$A_{c_i}^{\text{dec}} = r_{c_i}^{\text{dec}} - \bar{r}^{\text{dec}}$ 为批内归一化后的优势估计。

### 2.4 迭代阶段控制器

纯自我博弈容易陷入局部均衡——当间谍或平民某一方找到简单策略后，对手无法产生有效的对抗压力，导致训练停滞。Iterative-SPO 通过一个滞后阈值控制器在**线索阶段**（$m_t=0$）与**决策阶段**（$m_t=1$）之间自动切换，打破性能平台。

控制器基于两个指标的指数移动平均进行决策：

$$\overline{\text{acc}}_t = \rho \overline{\text{acc}}_{t-1} + (1-\rho) \text{acc}_t, \quad \overline{\text{na}}_t = \rho \overline{\text{na}}_{t-1} + (1-\rho) \text{na}_t$$

其中 $\text{acc}_t$ 为当前批次决策准确率，$\text{na}_t$ 为弃权率。阶段切换条件为：

$$m_{t+1} = 1 \quad \text{if } m_t=0,\ \overline{\text{acc}}_t \geq \tau_{\text{acc}}^{\uparrow},\ \overline{\text{na}}_t \leq \tau_{\text{na}}^{\downarrow}$$

$$m_{t+1} = 0 \quad \text{if } m_t=1,\ (1-\overline{\text{acc}}_t \geq \tau_{\text{err}}^{\uparrow} \text{ or } \overline{\text{na}}_t \geq \tau_{\text{na}}^{\uparrow})$$

当处于线索阶段且决策准确率足够高、弃权率足够低时，说明当前线索质量已饱和，切换至决策阶段训练以提升推理能力；当处于决策阶段且错误率或弃权率过高时，说明间谍线索已难以识别，切换回线索阶段以增强线索生成能力。此外，每个阶段设有最小驻留步数 $K_{\text{min}}$，避免频繁抖动。消融实验（Figure 8）显示，Iterative-SPO 在 LogicVista 上的性能显著优于纯自我博弈和纯 RLVR 训练。

### 2.5 训练效率

与原始 GRPO 相比，Iterative-SPO 的交替训练策略大幅提升了数据效率。在相同硬件条件下，Vision-Zero 的训练效率较纯 GRPO 提升 **3.3× 至 6.4×**（Figure 7），且仅需 127 A100 小时即可完成训练（Table 3），远低于依赖人工标注数据的同类方法。



## 实验与关键发现

### 核心实验设置

所有实验均基于 **Qwen2.5-VL-7B** 基座模型进行后训练，在统一的开源评测平台 **VLMEvalKit** 上完成评估（Table 1, Table 2）。训练采用 Iterative-SPO 算法，每轮游戏配置 **4 名平民** 和 **2 轮线索发言**，线索阶段超参数设为 $\beta = \lambda = 0.\bar{1}$。训练数据涵盖三类领域无关输入：CLEVR 合成场景、图表数据和真实自然图像（Figure 4）。

![[assets/figures/papers/paper_list_l41_https_openreview_net_forum_id_s00SNXREV6/figures/008_Table_1.jpg]]
*Table 1: Performance Comparison of Vision-Zero and SOTA models on Reasoning and Math, evaluated on VLMEvalKit. All results are obtained under same settings, except ViGaL-Snake and ViGaL-Rotation, whose results are obtained from the original paper due to unavailable models. Vision-Zero outperforms baselines trained on extensive manually annotated datasets in related tasks*

![[assets/figures/papers/paper_list_l41_https_openreview_net_forum_id_s00SNXREV6/figures/012_Table_2.jpg]]
*Table 2: Performance comparison between Vision-Zero and other state-of-the-art models on Chart Understanding and Vision-Centric benchmarks. All models are evaluated using the opensource platform VLMEvalKit. Additional results on related datasets are provided in the Appendix A.4*

### 主结果：推理、图表与视觉中心任务

**推理与数学基准（Table 1）**。Vision-Zero 在完全不依赖人工标注的条件下，在六个推理和数学基准上取得显著提升。以 VisionZero-Qwen-7B (CLEVR) 为例，MathVista 准确率达 **72.2**，较基座模型 Qwen2.5-VL-7B（68.2）提升 **+4.0** 个百分点；在 LogicVista 上达 **43.3**（+3.8），DynaMath 上达 **46.1**（+4.1）。值得注意的是，该模型在 MathVista 和 LogicVista 上均超越了依赖人工标注数据训练的 **R1-OneVision-7B**（Yang et al., 2025b）和 **MM-Eureka-Qwen-7B**（Meng et al., 2025）等 RLVR 基线。

**图表理解与视觉中心基准（Table 2）**。在图表理解任务上，VisionZero-Qwen-7B (Chart) 在 ChartXiv_RQ 上取得 **45.8**（+3.3），FunctionQA 上取得 **52.0**（+6.2），均显著超越基座模型。在视觉中心任务上，VisionZero-Qwen-7B (CLEVR) 在 MMVP 上达 **79.5**（+2.7），BLINK 上达 **57.2**（Real-World 变体，+2.0），展现出对细粒度视觉差异的捕捉能力。

Figure 2 以准确率变化量（$\Delta$ Accuracy）直观展示了这一优势：Vision-Zero 在全部任务上的准确率变化均为正值，且整体幅度超越多个依赖昂贵标注数据的 SOTA 后训练方法。

![[assets/figures/papers/paper_list_l41_https_openreview_net_forum_id_s00SNXREV6/figures/004_Figure_2.jpg]]
*Figure 2: Performance Comparison of Vision-Zero with SOTA post-training methods. All models were post-trained on Qwen2.5-VL-7B. The numbers on the horizontal axis represent the accuracy of Qwen2.5-VL-7B on different tasks, while the vertical axis represents the change in accuracy of the trained model. Vision-Zero outperforms baselines trained on expensive human-labeled datasets*

### 训练效率与成本分析

**训练效率（Figure 7）**。Iterative-SPO 在相同硬件设置下，训练效率较纯 GRPO 提升 **3.3x 至 6.4x**。具体而言，在 Qwen2.5-VL-7B 上，Vision-Zero 仅需纯 GRPO 约 1/3 的训练步数即可达到同等或更优的胜率；在 InternVL3-8B 上，效率优势更为显著。

![[assets/figures/papers/paper_list_l41_https_openreview_net_forum_id_s00SNXREV6/figures/015_Figure_7.jpg]]
*Figure 7: Taining effectiveness comparison between Vision-Zero and the original GRPO. We compare Vision-Zero and GRPO under identical hardware settings to evaluate training cost and efficiency. Specifically, for the original GRPO, we trained on the MM-Eureka dataset using 8×NVIDIA A100 (80GB) GPUs with a batch size of 128 for 100 iterations on both Qwen2.5-VL-7B and InternVL3-8B. Vision-Zero is trained for the same setting on the Clever dataset using the same hardware. We evaluate the performance of checkpoints from different iterations on MathVista*

**综合成本（Table 3）**。Vision-Zero 的标注成本为 **零**——无需任何教师模型或评判 LLM 生成标注 token。相比之下，R1-OneVision-7B 需 15.4M 标注 token，MM-Eureka-Qwen-7B 需 5.8M。训练时间方面，Vision-Zero 仅需 **127 A100-小时**，远低于 R1-OneVision-7B 的 480 小时和 OpenVLThinker-7B 的 384 小时。在 MMMu 基准上，VisionZero-Qwen-7B (CLEVR) 以 58.8 的得分超越所有对比方法，实现了“零标注成本、最低训练时间、最高性能”的三重优势。

![[assets/figures/papers/paper_list_l41_https_openreview_net_forum_id_s00SNXREV6/figures/013_Table_3.jpg]]
*Table 3: Comparison of dataset construction costs, training costs and model performance across methods. Label Cost refers to the number of tokens generated by teacher or judging LLMs during data curation; for consistency, all token counts are recalculated using the Qwen2.5 tokenizer. Since VIGAL and Vision-Zero are trained on unlabeled data, they incur no labeling cost. To estimate training time cost, we refer to each baseline’s original paper to obtain the number of samples used during RL training, and multiply this by a standard GRPO cost per sample to simulate the expected time consumption under a fully fair setting. For some methods, the value is shown as ≥ because we only account for RL cost, e...*

### 消融实验：关键设计验证

**玩家数量与线索轮次（Table 11, Table 12）**。将平民玩家数从 2 人增至 4 人，六个基准的平均准确率从 42.4 提升至 **44.9**，表明更复杂的多智能体交互迫使模型发展更强的推理能力。线索轮次从 1 轮增至 3 轮，平均准确率从 41.3 提升至 **45.2**，验证了多轮线索整合对深度推理的必要性。

**角色优势估计（RAE）（Table 13）**。移除 RAE 模块后，平均准确率骤降至 **37.4**，不仅远低于完整模型的 44.1，甚至低于基座模型的 41.1。这一显著退化证实了 RAE 是平衡间谍与平民之间信息不对称的核心机制——若不消除角色固有优势，自我博弈训练将崩溃。

**训练范式对比（Figure 8）**。Iterative-SPO 在胜率和 LogicVista 性能上均优于纯自我博弈和纯 RLVR。纯自我博弈训练因缺乏外部监督信号，模型性能在早期即陷入平台期；纯 RLVR 则无法充分利用博弈互动的探索性优势。Iterative-SPO 通过交替优化，既保留了自我博弈的探索能力，又借助 RLVR 的验证奖励稳定了训练方向。

### 训练动态与定性分析

**训练动态（Figure 6）**。胜率随训练迭代持续上升，表明模型在博弈中逐步习得有效的策略。同时，线索阶段的 token 长度呈现先增后稳的趋势，说明模型在训练初期学会了生成更详细的信息性线索，随后趋于高效表达。

**推理能力可视化（Figure 5）**。对比训练前后间谍的推理过程，GPT 评分显示模型在规划、信息检索、分解、策略制定和逻辑推理五个维度均有显著提升。训练后的模型能够系统性地分析历史线索、推断图像内容并制定误导策略，而非简单猜测。

### 失败模式与局限性

1. **图像编辑依赖**：当前框架依赖图像编辑器生成差异化图像对（如 CLEVR 的物体属性修改、真实图像的局部编辑）。在医学影像、遥感、科学图表等专业领域，缺乏合适的编辑工具将限制框架的适用性。
2. **模态扩展困难**：游戏规则针对单图像观察和成对编辑设计。要扩展到视频流、多图像上下文或交互式 3D 环境，需要对游戏机制和训练算法进行重大改动。
3. **模式坍缩风险**：随着博弈轮次增加，模型生成的线索可能存在模式坍缩（如固定套路），需要进一步研究多样性保证机制。

### 补充图表

![[assets/figures/papers/paper_list_l41_https_openreview_net_forum_id_s00SNXREV6/figures/016_Table_4.jpg]]
*Table 4: Model generalizability of Vision-Zero. We train InternVL3-8B and InternVL3-14B within the Vision-Zero using the CLEVR-based dataset. As a baseline, we train InternVL3-8B and InternVL3-14B with vanilla GRPO on the MM-Eureka training set under the same setting as Vision-Zero, and evaluate all models on six reasoning benchmarks*

![[assets/figures/papers/paper_list_l41_https_openreview_net_forum_id_s00SNXREV6/figures/019_Table_5.jpg]]

![[assets/figures/papers/paper_list_l41_https_openreview_net_forum_id_s00SNXREV6/figures/020_Table_5.jpg]]
*Table 5: Vision-Zero training hyperparameters*

![[assets/figures/papers/paper_list_l41_https_openreview_net_forum_id_s00SNXREV6/figures/021_Table_6.jpg]]
*Table 6: Performance comparison between Vision-Zero and other models on OCR, Chart, and Document Understanding. All models are evaluated using the open-source platform VLMEvalKit*

![[assets/figures/papers/paper_list_l41_https_openreview_net_forum_id_s00SNXREV6/figures/022_Table_7.jpg]]
*Table 7: Performance comparison between Vision-Zero and other state-of-the-art models on Vision-Centric benchmarks. All models are evaluated using the open-source platform VLMEvalKit*



## 定位与知识库关联

### 1. 与现有VLM后训练范式的谱系关系

**Vision-Zero** 的提出根植于当前视觉语言模型（VLM）后训练的两条主线：基于人类标注数据的监督微调与强化学习，以及基于可验证奖励的强化学习（RLVR）。其核心突破在于彻底切断了方法对“人类经验”的依赖，构建了一个完全自洽的数据生成与能力进化闭环。

*   **相对于监督微调（SFT）与RLHF/RLVR基线**：现有SOTA方法，如 **R1-OneVision-7B** (Yang et al., 2025b)、**MM-Eureka-Qwen-7B** (Meng et al., 2025)、**VLAA-Thinker-7B** (Zhou et al., 2025) 和 **OpenVLThinker-7B** (Deng et al., 2025)，虽然在RLVR阶段允许模型自主探索推理过程，但其训练数据（QA对）的源头仍严重依赖于专家设计或人工标注。Vision-Zero则通过“谁是间谍”式的多智能体自我博弈游戏，将任意无标签图像直接转化为训练信号，实现了从“人类策划数据”到“环境生成数据”的范式跃迁（见 **Figure 1**）。这一转变的因果效应是：模型的推理能力上限不再受限于人类标注者的水平，而是由博弈环境的复杂度和模型自身的对抗性探索共同决定。

*   **相对于基于游戏的数据收集方法**：**ViGaL** (Xie et al., 2025) 等工作也利用游戏收集数据进行后训练，但其流程是“玩游戏→收集数据→训练”，游戏与训练是解耦的。Vision-Zero的不同之处在于，它实现了 **在博弈中训练（Learning-in-the-Game）**：自我博弈既是数据生成器，也是策略优化器。通过提出的 **Iterative-SPO** 算法，模型的策略更新会立即改变博弈对手的行为，形成持续的共同进化，这是产生超越人类经验策略的关键机制。

*   **相对于纯自我博弈与纯RLVR**：纯自我博弈（如原始的GRPO直接应用于博弈）容易陷入局部均衡（如角色坍缩或策略发散），而纯RLVR则无法获得博弈互动带来的策略多样性。Vision-Zero的 **Iterative-SPO** 通过交替执行“线索阶段自我博弈”与“决策阶段RLVR”，在探索与稳定之间找到了平衡。消融实验（**Figure 8**）证实，这种交替训练在LogicVista上的性能显著优于纯自我博弈和纯RLVR，训练效率较纯GRPO提升3.3x至6.4x（**Figure 7**）。

### 2. 方法的核心适用边界与前提

Vision-Zero的有效性建立在以下关键前提之上，这些前提同时也界定了其当前最适用的场景：

1.  **可编辑的视觉输入**：框架的核心机制依赖于生成“平民图像”与“间谍图像（空白）”的差异化输入。当前实现使用图像编辑器来生成这些图像对。因此，该方法在**自然图像、图表、合成场景**等易于编辑的领域表现优异（**Figure 4**），但在**医疗影像、遥感图像、科学图表**等专业领域，因缺乏合适的编辑工具或编辑可能破坏语义保真度而受限。这是论文明确指出的一个局限性。

2.  **单图像观察与成对编辑**：游戏规则专为单张图像的观察和成对差异化设计。要将其扩展到**视频流理解、多图像上下文推理或交互式3D环境**，需要对游戏规则、输入处理管线以及训练算法进行重大改动。这是方法当前的一个硬性边界。

3.  **角色不对称性的有效平衡**：游戏中“平民”与“间谍”存在固有的信息不对称，这会导致胜率偏差。**角色优势估计（RAE）模块**是纠正这一偏差的“因果旋钮”。消融实验（**Table 13**）提供了决定性证据：移除RAE后，模型平均准确率降至37.4，甚至低于原始基座模型（41.1），证实了RAE是维持训练稳定性的必要条件。

### 3. 局限性与开放问题

*   **模式坍缩的潜在风险**：尽管Iterative-SPO通过交替训练和滞后阈值机制防止了训练停滞，但随着博弈轮次的增加，模型生成的线索仍可能陷入固定套路（模式坍缩）。如何进一步保证策略多样性，是一个待解的开放问题。论文目前通过监控胜率和token长度（**Figure 6**）来观察训练动态，但未提出主动的多样性激励措施。

*   **向标签稀缺领域的迁移**：如局限性所述，如何将Vision-Zero的自博弈环境适配到**遥感、医学影像**等标签稀缺且难以编辑的特殊领域，是一个重要的开放问题。可能的路径包括：设计无需图像编辑的新博弈规则，或利用生成模型创造语义等价的差异化输入。

*   **向更丰富模态的扩展**：当前框架针对静态图像设计。如何重新设计游戏机制以支持**视频流、多图像上下文或三维场景**，是方法未来发展的关键方向。这需要定义新的观察空间、行动空间和奖励结构。

*   **与对比式RLVR的关系**：**MiCo-7B** (Chen et al., 2025b) 等对比式RLVR方法通过对比学习增强视觉表示。Vision-Zero的博弈过程天然包含了细粒度的视觉比较，未来工作可探索将博弈中产生的对比信号显式化，以进一步提升视觉中心任务上的性能。



## 原文 PDF

![[paperPDFs/ICLR_2026/Vision_Zero_Scalable_VLM_Self_Evolution_via_Multi_Agent_Self_Play.pdf]]
