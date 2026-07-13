---
title: "Counterfactual VLA: Self-Reflective Vision-Language-Action Model with Adaptive Reasoning"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/Counterfactual_VLA_Self_Reflective_Vision_Language_Action_Model_with_Adaptive_Reasoning.pdf
project_link: null
code_link: null
aliases:
- CVCV
- CVSRVLAMAR
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: 引入基于预测元动作的反事实自反射推理循环：模型首先预测时间分段元动作，然后进行反事实推理分析后果并修正元动作，最终生成轨迹。
primary_logic: 通过将时间分段元动作作为语言可解释的中间表征，并设计 rollout–filter–label 数据管线自动挖掘模型失败场景并生成反事实推理标签，可赋予 VLA 内生的自反射反事实推理能力，使其在困难场景中自适应地修正自身决策，而无需外部验证器。
claims:
- CF-VLA 将轨迹误差最多降低 17.6%（MinADE），安全指标提升 20.5%（碰撞率）
- 引入预填充真实元动作可使轨迹误差减半，表明元动作是主要瓶颈
- 自适应推理在困难场景中思考更频繁，且误差降低更显著
- 内部验证集 D_val（80,000小时驾驶数据） 上 MinADE (最小平均位移误差) = 0.7647 (CF-VLA w/o route, round2)
---

# Counterfactual VLA: Self-Reflective Vision-Language-Action Model with Adaptive Reasoning

> [!tip] 核心洞察
> 通过将时间分段元动作作为语言可解释的中间表征，并设计 rollout–filter–label 数据管线自动挖掘模型失败场景并生成反事实推理标签，可赋予 VLA 内生的自反射反事实推理能力，使其在困难场景中自适应地修正自身决策，而无需外部验证器。

| 字段 | 内容 |
|------|------|
| 中文题名 | 反事实VLA：具有自适应推理的自反射视觉-语言-动作模型 |
| 英文题名 | Counterfactual VLA: Self-Reflective Vision-Language-Action Model with Adaptive Reasoning |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2512.24426) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/image_and_video_generation |
| Method | CF-VLA (Counterfactual VLA) |
| Dataset | 内部验证集 D_val（80,000小时驾驶数据）, 内部验证集 D_val |

> [!tip] 效果简介
> - 内部验证集 D_val（80,000小时驾驶数据） 上，MinADE (最小平均位移误差) 0.7647 (CF-VLA w/o route, round2) vs 0.9283 (traj-only) (↓17.6%)。
> - 内部验证集 D_val 上，碰撞率 (Collision Rate) 0.0177 (CF-VLA w/ route, round1) vs 0.0244 (traj-only) (↓27.5%（相对）；或按论文声明降低20.5%)；MinADE (有路线信息) 0.6712 (CF-VLA w/ route, round1) vs 0.7263 (meta-act w/ route) (↓7.6%)；Meta-Action IOU (自我反思后) 0.9231 (CF-VLA w/ route, round1, edited) vs 0.9236 (meta-act w/ route, 无编辑) (基础持平，但通过编辑从0.9207提升至0.9231（↑0.0024）)。

## 概要

自动驾驶的视觉-语言-动作模型（VLA）通常将感知、推理与规划融为一体，但现有方法仅在生成最终动作前输出一次性的描述性推理，缺乏对自身计划进行质疑和修正的能力。当模型产生不安全的元动作（如不恰当的变道时机、激进的加速度）时，系统无法在执行前识别并纠正这些错误，构成了当前 VLA 的核心瓶颈。

本文提出 **CF-VLA（Counterfactual VLA）**，一种具有自适应反事实推理的自反射 VLA 模型。其核心思路是引入一个 **反事实自反射循环**：模型首先生成时间分段的语言可解释元动作（纵向、横向、车道意图），然后以这些元动作和视觉上下文为条件进行反事实推理——诊断初始计划中的潜在问题，并据此修正元动作，最终生成安全且精确的轨迹。这一循环赋予了 VLA 内生的“自我质疑与修正”能力，而无需依赖外部验证器。

为训练这一能力，论文设计了一套 **rollout–filter–label 数据管线**：让基础 VLA 在训练数据上自由滚动输出，自动筛选出元动作预测存在问题的场景，再由高容量教师模型为这些场景标注反事实推理链，形成自改进的训练循环。同时，CF-VLA 通过混合数据训练（包含有/无反事实推理的样本）隐式习得 **自适应推理** 策略——在简单场景中直接输出动作，在困难场景中自动触发更深度的自反射推理。

实验结果显示，CF-VLA 在内部大规模验证集上将轨迹误差（MinADE）最多降低 **17.6%**，安全指标（碰撞率）提升 **20.5%**。消融实验进一步揭示：元动作预测是性能的主要瓶颈（预填充真实元动作可使轨迹误差减半），而自适应推理在困难场景中思考更频繁且误差降低更显著，验证了方法的有效性。

### 端到端自动驾驶中的推理能力演进

端到端自动驾驶正经历从“感知-规划-控制”模块化架构向统一视觉-语言-动作（VLA）模型的范式迁移。VLA 模型将多模态感知、场景理解与运动规划集成于单一可训练框架中，其核心优势在于能够以自然语言形式输出驾驶推理，从而提升决策的可解释性与安全性。然而，现有 VLA 模型在推理机制上存在一个根本性瓶颈：**它们仅在生成最终动作之前输出一次性描述性推理**，用于解释“当前场景是什么”以及“我打算做什么”，却缺乏对自身计划进行质疑、验证和修正的能力。这种“描述但不自省”的模式意味着，一旦模型产生了不安全的初始动作意图，该意图将直接流入轨迹生成模块，没有任何内部机制能在执行前拦截或修正错误决策。

### 现有方法的缺口：缺乏自反射反事实推理

人类驾驶员的安全决策高度依赖一种**反事实自反射**能力——在执行动作前，我们会在心中预演可能的结果，设想“如果我这样做会发生什么”，并据此调整计划。例如，在观察到相邻车道车辆突然减速时，经验丰富的驾驶员会立即反思“我原本打算加速变道，但前车可能正在避让行人，我应该先减速观察”。这种基于预测动作的反事实推理是安全驾驶的关键认知机制，但在当前 VLA 模型中完全缺失。

具体而言，现有方法的缺口体现在三个层面：

1. **推理模式单一**：现有 VLA 采用前馈式描述推理，模型被告知“描述场景并给出动作”，而非“预测你的动作，然后反思它是否安全”。这使得模型无法捕捉自身计划中的潜在风险。
2. **动作表征不可解释**：主流 VLA 使用连续隐空间 token 或直接回归轨迹点作为动作输出。模型无法“谈论”自己的动作，更无法对其进行语义层面的诊断和修正。
3. **缺乏自我改进的数据机制**：标准的行为克隆训练仅从人类驾驶数据中学习，模型从未见过自身的失败案例，也没有机制从失败中学习反事实推理。

### 本文动机：赋予 VLA 内生的自反射反事实推理能力

针对上述缺口，本文提出 **CF-VLA（Counterfactual VLA，反事实 VLA）**，其核心动机是：**能否让 VLA 模型具备内生的自反射反事实推理能力，使其在生成最终轨迹之前，能够像人类驾驶员一样审视、质疑并修正自己的初始动作计划？**

实现这一目标需要解决三个关键挑战：（1）如何设计一种语言可解释的中间动作表征，使模型能够“谈论”自己的动作意图；（2）如何构建反事实推理的训练数据，使模型学会对自身计划进行诊断和修正；（3）如何让模型自适应地决定何时需要深度推理、何时可以直接响应，以平衡安全性与计算效率。

CF-VLA 通过三个核心设计应对这些挑战：引入**时间分段元动作**作为语言可解释的中间基元，设计 **rollout–filter–label 数据管线**自动挖掘模型失败场景并生成反事实推理标签，以及实现**自适应推理**机制使模型根据场景难度动态调整推理深度。这一框架首次将反事实自反射推理内化于 VLA 模型本身，无需依赖外部验证器或人工标注，为端到端自动驾驶的安全决策提供了新的范式。

## 核心方法与创新机理

CF-VLA 的核心创新不在于引入一个更强的轨迹预测骨干，而在于**赋予 VLA 模型内生的自反射反事实推理能力**，使其能够在执行动作前审视并修正自身计划。这一能力通过三个相互耦合的设计实现，分别对应推理模式、中间表征和训练数据构建三个维度的根本性改变。

### 从描述性推理到自反射反事实推理

现有 VLA 模型的推理模式通常是一次性的描述性推理——模型在生成动作之前输出一段对场景和意图的描述，但并不质疑或验证自身计划的合理性。CF-VLA 将这一模式替换为**基于预测元动作的反事实自反射循环**：

$$
\mathtt{meta\text{-}actions} \to \mathtt{CF\ reasoning} \to \mathsf{updated\ meta\text{-}actions} \to \mathsf{trajectory}
$$

具体而言，模型首先生成时间分段元动作序列作为初始计划，然后以视觉上下文和该初始计划为条件进行反事实推理——分析当前计划可能存在的问题（如“是否需要提前减速以避免碰撞”），并据此修正元动作，最终生成连续轨迹。这一循环使模型具备了“先计划、再反思、后执行”的能力，而无需依赖外部验证器或规则检查器。

### 时间分段元动作：语言可解释的中间动作表征

上述自反射循环得以成立的关键，是引入了一组**语言可解释的时间分段元动作**作为推理与低级动作之间的中间基元。这些元动作将 6.4 秒规划时域划分为三个维度：

- **纵向**：{加速, 减速, 保持速度, 等待, 倒车}
- **横向**：{直行, 左转, 右转}
- **车道**：{保持车道, 向左变道, 向右变道}

与传统的隐式 latent token 或连续轨迹 token 不同，元动作是语言原生的离散符号，使得模型能够像谈论自然语言一样“谈论”自己的动作计划。这为反事实推理提供了可操作的语义锚点——模型可以诊断“当前计划在第三段加速过于激进”，并给出修正建议“应替换为减速等待”。消融实验证实，**元动作预测是整个流程的主要性能瓶颈**：当预填充真实元动作时，轨迹误差（MinADE）从 0.8411 锐减至 0.4831（Table 2），降幅接近一半，表明一旦元动作正确，下游轨迹生成的压力大幅降低。

### Rollout–Filter–Label：自改进的数据管线

CF-VLA 的第三个关键创新是**rollout–filter–label 数据管线**，它解决了反事实推理训练数据的获取难题。该管线的工作流程如下：

1. **Rollout**：使用基础 VLA 模型在训练数据上滚动输出，生成自由预测的元动作和轨迹。
2. **Filter**：通过比较自由生成轨迹与预填充真实元动作所诱导轨迹的误差，筛选出“高价值”场景。过滤条件为：

   $$
   \min \mathrm{ADE}(\mathbf{x}_{\mathrm{pf}}, x^\star) < \min \mathrm{ADE}(\mathbf{x}_{\mathrm{free}}, x^\star) \quad \text{and} \quad \min \mathrm{ADE}(\mathbf{x}_{\mathrm{free}}, x^\star) > \epsilon,\ \epsilon=0.5
   $$

   即仅保留那些预填充真实元动作能显著改善轨迹误差、且自由生成误差超过阈值的场景——这些正是模型自身元动作存在问题、反事实推理最可能产生价值的场景。
3. **Label**：使用高容量教师模型（Qwen2.5-VL-72B-Instruct）为筛选出的场景生成反事实推理标注。

这一管线的核心洞察在于：**并非所有场景都需要反事实推理，而应当聚焦于模型自身容易出错的困难场景**。消融实验证实了过滤的必要性：使用过滤后数据训练的 CF-VLA（filtered ds）相比使用全部样本训练的变体，不仅轨迹误差更低（MinADE 0.6712 vs 0.6811），思考率也大幅降低（0.219 vs 0.668），输出长度显著缩短（125.7 vs 191.1 tokens）。这表明过滤管线有效剔除了噪声样本，提取出更可靠的自反射信号。此外，将该管线应用于第一轮 CF-VLA 自身进行第二轮训练，可进一步压缩思考率和输出长度，同时降低轨迹误差和安全指标，形成了一个**自改进的正反馈循环**。

### 自适应推理：隐式学习何时反思

与上述设计相配合，CF-VLA 采用**自适应推理**策略：模型并非始终进行反事实推理，而是从统一指令格式的数据混合中隐式学习何时需要反思、何时可以直接输出。训练数据混合包含有反事实推理痕迹和无推理痕迹的样本，模型在推理时自主决定是否生成推理过程。实验表明，自适应推理变体（CF-VLA adaptive）在所有非预填充模型中取得了最低的 MinADE（0.7650），同时保持中等思考率（0.148），优于强制思考（思考率过高但误差未显著降低）和强制不思考（误差较高）的变体。Figure 1 进一步揭示，**模型在轨迹误差更高的困难场景中思考更频繁，且误差降低幅度更大**，验证了自适应推理的有效性。

综上，CF-VLA 通过“元动作中间表征 + 反事实自反射循环 + rollout–filter–label 自改进管线”三位一体的设计，将 VLA 从被动模仿提升为主动自省，在无需外部监督的条件下实现了可解释、可修正的动作规划。

CF-VLA 的核心是一个**自反射反事实推理循环**，其设计动机在于弥补现有 VLA 模型“描述性推理”的致命短板——模型在生成动作前会输出一段意图说明，但从不质疑自身计划的合理性，因而无法在执行前发现并修正不安全或不合适的决策。CF-VLA 通过引入**语言可解释的时间分段元动作**作为中间表征，并围绕它构建“预测→反思→修正→执行”的闭环，赋予模型内生的自我纠错能力，全程无需外部验证器介入。

### 推理循环：从元动作到轨迹的自反射闭环

CF-VLA 的推理过程遵循一个严格的因果链条：

$$
\mathtt{meta\text{-}actions} \;\to\; \mathtt{CF\;reasoning} \;\to\; \mathsf{updated\;meta\text{-}actions} \;\to\; \mathsf{trajectory}
$$

具体而言，给定视觉上下文（多视角图像与历史轨迹），模型首先预测一组**时间分段元动作**，用于概括未来 6.4 秒规划时域内的驾驶意图。元动作被设计为离散、语言可解释的基元，覆盖三个正交维度：

- **纵向**：加速、减速、保持速度、等待、倒车
- **横向**：直行、左转、右转
- **车道**：保持车道、向左变道、向右变道

这些基元按时间区间划分，形成一段结构化的“动作草稿”。随后，模型以该草稿和原始视觉上下文为条件，执行**反事实推理**——诊断初始元动作中可能存在的问题，并给出修正建议。修正后的元动作最终被送入轨迹解码器，生成连续的未来轨迹。

这一设计的核心洞察在于：元动作作为语言本原的中间抽象层，既足够粗粒度以承载高层驾驶语义（便于语言模型进行推理和编辑），又足够细粒度以有效约束底层轨迹生成。消融实验为这一论断提供了强有力证据：当用真实元动作替换模型预测的元动作时，轨迹误差（MinADE）从 0.8411 骤降至 0.4831，几乎减半，表明**元动作预测是限制整体性能的主要瓶颈**，也解释了为何围绕元动作进行反事实修正能够带来显著的端到端增益。

### 自适应推理：按需思考的隐式决策机制

与始终输出推理或仅在任务边界切换推理的传统方案不同，CF-VLA 采用**自适应推理**策略：模型在统一的指令提示下，从包含反事实推理和不包含推理的混合数据中隐式学习何时需要反思。在推理阶段，模型自主决定是否生成反事实推理——对于简单场景直接输出元动作和轨迹，对于困难场景则触发自反射循环。

实验验证了这一机制的有效性：在困难场景中，模型的思考频率显著更高，且轨迹误差的降低幅度更大。在无路线信息的消融实验中，自适应推理变体以 0.7650 的 MinADE 取得最优性能，同时保持中等思考率（0.148），优于强制不思考（误差更高）和强制始终思考（计算开销更大）的变体。

### 数据管线：Rollout–Filter–Label 自改进循环

CF-VLA 的训练依赖一套专门设计的 **rollout–filter–label 数据管线**，用于从模型自身的行为中挖掘高价值场景并自动生成反事实推理标注。管线分为三个阶段：

1. **Rollout**：使用基础 VLA 模型在训练数据上执行推理，记录其自由生成的元动作和轨迹。
2. **Filter**：根据轨迹误差筛选高价值场景。筛选条件为：预填充真实元动作能显著改善轨迹误差，且自由生成轨迹的误差超过阈值 $\epsilon = 0.5$。这一条件确保仅保留“模型元动作预测有缺陷且修正后能带来实质改善”的场景，避免在模型已经表现良好的样本上浪费反事实推理。
3. **Label**：对筛选出的场景，使用高容量教师模型（Qwen2.5-VL-72B-Instruct）生成简洁的反事实推理文本，形成反事实推理数据集 $\mathcal{D}_{\mathrm{CF}}$。

该管线的关键价值在于其**自改进特性**：第一轮训练得到的 CF-VLA 可作为新的基础模型，再次运行管线生成更高质量的反事实样本，驱动第二轮训练。实验表明，第二轮训练不仅进一步降低了轨迹误差和安全指标，还压缩了思考率和输出长度，使推理更加高效。

数据过滤的有效性在消融实验中得到了明确证实：使用经过滤的反事实样本训练的模型，相比使用全量样本训练的模型，在轨迹误差更低（MinADE 0.6712 vs 0.6811）的同时，思考率大幅降低（0.219 vs 0.668），输出长度也更短（125.7 vs 191.1 tokens）。这验证了**过滤管线对于提取可靠自反射信号至关重要**——未经过滤的全量标注包含大量噪声推理，反而拖累模型性能。

### 训练策略与损失设计

CF-VLA 的训练采用分阶段策略：基础 VLM 首先在轨迹数据集 $\mathcal{D}_{\mathrm{traj}}$ 上训练得到 traj-only 模型，随后在元动作数据集 $\mathcal{D}_{\mathrm{meta}}$ 上微调得到 meta-act 模型，最终在混合数据集 $\mathcal{D}_{\mathrm{traj}} \cup \mathcal{D}_{\mathrm{meta}} \cup \mathcal{D}_{\mathrm{CF}}$ 上微调得到完整的 CF-VLA。训练损失中，轨迹、元动作和反事实推理 token 的权重比例为：

$$
w_{\mathrm{act}} : w_{\mathrm{meta}} : w_{\mathrm{CF}} = 1 : 10 : 10
$$

较高的元动作和反事实推理权重反映了这些信号对最终性能的决定性影响。此外，训练时对首个元动作块进行损失掩码，以避免模型在推理初期受到不合理的监督信号干扰。

![[assets/figures/papers/paper_list_l2381_https_arxiv_org_abs_2512_24426/figures/002_Figure_2.jpg]]
*Figure 2: The framework of CF-VLA. A base VLA is finetuned on a counterfactual reasoning dataset generated by a rollout–filter–label pipeline. The resulting CF-VLA supports both direct inference and self-reflective inference, in which counterfactual reasoning edits meta-actions before trajectory generation*

### 自反射反事实推理循环

CF-VLA 的核心在于将传统 VLA 的单次描述性推理升级为**自反射反事实推理循环**。模型首先预测时间分段元动作，然后基于视觉上下文和初始元动作进行反事实推理，诊断潜在问题并修正元动作，最后生成连续轨迹。整个闭环可形式化为：

$$
\mathtt{meta\text{-}actions} \to \mathtt{CF\ reasoning} \to \mathsf{updated\ meta\text{-}actions} \to \mathsf{trajectory}
$$

这一循环的关键创新在于：**元动作作为语言可解释的中间表征**，使模型能够“谈论”自身的动作计划，从而在生成最终轨迹之前进行自我验证和修正，而无需依赖外部验证器。

### 时间分段元动作定义

元动作将 6.4 秒的规划时域划分为多个时间区间，在每个区间内定义三个维度的离散动作：

- **纵向动作**（Longitudinal）：$\{ \text{Accelerate, Decelerate, Keep Speed, Wait, Reverse} \}$
- **横向动作**（Lateral）：$\{ \text{Straight, Left Turn, Right Turn} \}$
- **车道动作**（Lane）：$\{ \text{Keep Lane, Left Lane Change, Right Lane Change} \}$

这一离散化设计使得模型能够以自然语言形式表达驾驶意图，为后续的反事实推理提供了可操作的语义基元。

### 自适应推理机制

CF-VLA 支持**自适应推理**：模型并非在每一帧都执行反事实推理，而是通过统一指令提示，从包含有/无反事实推理样本的混合数据中隐式学习何时需要启动自反射过程。训练时，模型同时接触直接推理样本和自反射推理样本，使其在推理时能够动态决定是否生成反事实推理链。实验表明，模型在困难场景中思考更频繁，且误差降低更显著。

### 数据过滤条件

rollout–filter–label 管线中的过滤阶段使用以下条件筛选高价值场景：

$$
\min \mathrm{ADE}(\mathbf{x}_{\mathrm{pf}}, x^\star) < \min \mathrm{ADE}(\mathbf{x}_{\mathrm{free}}, x^\star) \quad \text{and} \quad \min \mathrm{ADE}(\mathbf{x}_{\mathrm{free}}, x^\star) > \epsilon, \ \epsilon=0.5
$$

其中 $\mathbf{x}_{\mathrm{pf}}$ 表示预填充真实元动作后生成的轨迹，$\mathbf{x}_{\mathrm{free}}$ 表示自由生成的轨迹，$x^\star$ 为真实轨迹。该条件筛选出两类场景：**（1）** 提供真实元动作能显著改善轨迹误差（说明元动作预测存在问题）；**（2）** 自由生成轨迹的误差超过阈值 0.5（说明场景本身具有挑战性）。只有同时满足这两个条件的场景才会进入反事实标注阶段，从而避免在简单或无关场景上浪费推理资源。

### 训练损失权重

CF-VLA 在混合数据上进行多任务训练，损失函数对轨迹、元动作和反事实推理三类 token 采用加权策略：

$$
w_{\mathrm{act}} : w_{\mathrm{meta}} : w_{\mathrm{CF}} = 1 : 10 : 10
$$

元动作和反事实推理 token 的权重是轨迹 token 的 10 倍，这反映了模型对推理质量和元动作精度的侧重。此外，训练时对首个元动作块进行损失掩码，以减少初始预测噪声对后续推理的干扰。

### 训练阶段递进

训练采用分阶段策略：首先在纯轨迹数据 $\mathcal{D}_{\mathrm{traj}}$ 上训练基础 VLA，然后在元动作标注数据 $\mathcal{D}_{\mathrm{meta}}$ 上微调得到 meta-act 基线，最后在混合数据 $\mathcal{D}_{\mathrm{traj}} \cup \mathcal{D}_{\mathrm{meta}} \cup \mathcal{D}_{\mathrm{CF}}$ 上微调得到完整的 CF-VLA。第二轮训练则使用第一轮 CF-VLA 自身 rollout 产生的数据，通过数据管线挖掘新的高价值场景，形成自改进循环。

![[assets/figures/papers/paper_list_l2381_https_arxiv_org_abs_2512_24426/figures/003_Figure_3.jpg]]
*Figure 3: (A) Adaptive Reasoning can be achieved by training models on a mixture of data with the unified instruction prompt. (B) Data generation process. We build a rollout–filter–label pipeline that runs the VLA, detects samples where its meta-actions are problematic, and labels counterfactual (CF) reasoning traces, forming a CF reasoning dataset. (C) Data filtering process. We use trajectory disagreement between trajectories that are free-generated and those induced by the ground-truth meta-actions to filter data. Each data point is colored by the meta-actions IOU in free generation*

## 实验与关键发现

### 核心实验结果

CF-VLA 在内部验证集 D_val（基于 80,000 小时驾驶数据构建）上，从轨迹精度、行为安全性和推理质量三个维度全面评估。表 1 汇总了主要结果。

**轨迹精度。** 在无路线信息的设置下，CF-VLA（round2）将 MinADE 从 traj-only 基线的 0.9283 降至 0.7647，相对降低 17.6%；MinFDE 从 2.3978 降至 2.0094。有路线信息时，CF-VLA（w/ route, round1）的 MinADE 为 0.6712，相比 meta-act（w/ route）的 0.7263 降低 7.6%。这表明反事实自反射推理在两种设置下均带来一致的轨迹质量提升。

**安全性。** 碰撞率从 traj-only 的 0.0244 降至 CF-VLA（w/ route, round1）的 0.0177，相对降幅达 27.5%（论文结论中保守表述为 20.5%）。离路率（Off-road）和角点距离（Corner Distance）也同步改善。多轮训练（round2）进一步压缩了安全指标，证明 rollout–filter–label 管线的自改进循环有效。

**推理质量。** 以元动作 IOU 衡量，CF-VLA 在编辑后的 IOU 达到 0.9231（w/ route, round1），与无推理的 meta-act 基线的 0.9236 基本持平，但通过反事实编辑从初始的 0.9207 提升至 0.9231（Δ = 0.0024）。这说明反事实推理能够在保持元动作整体质量的前提下，对关键帧进行有意义的修正。

### 消融分析

#### 元动作预测是主要瓶颈

表 2 的消融实验揭示了元动作预测对整体性能的决定性影响。当向 meta-act 基线预填充真实元动作（pre-filled）时，MinADE 从 0.8411 骤降至 0.4831，降幅达 42.6%。这一结果直接证实：**元动作预测是当前 VLA 系统的主要性能瓶颈**，而非下游的轨迹解码。因此，CF-VLA 将自反思聚焦于元动作层面，具有明确的因果合理性。

#### 自适应推理优于强制策略

表 2 对比了三种推理模式：强制不思考（force no think）、强制思考（force think）和自适应推理（adaptive）。CF-VLA adaptive 在所有非预填充模型中取得最低 MinADE（0.7650），同时保持中等思考率（0.148）。强制思考变体虽然思考率高达 0.998，但 MinADE 反而升至 0.7829；强制不思考变体则因完全放弃推理而性能最差。这一结果验证了自适应推理的核心假设：**并非所有场景都需要反事实推理，模型应学会在困难场景中动态激活自反思能力**。图 1（上）进一步可视化该趋势——在轨迹误差更大的复杂场景中，思考率显著升高，且误差降幅更大。

#### 数据过滤管线是关键组件

表 3 和表 4 对比了在全量数据集与经 rollout–filter–label 管线筛选的高价值子集上训练反事实推理的效果。使用过滤数据的 CF-VLA（filtered ds）在 MinADE 更低（0.6712 vs 0.6811）的同时，思考率大幅降低（0.219 vs 0.668），输出 token 长度也更短（125.7 vs 191.1）。这表明：**全量数据中包含大量低质量或冗余的反事实标签，会诱导模型过度思考并损害效率；过滤管线通过仅保留“预填充真实元动作能显著改善轨迹”的场景，提取了更可靠的自反射信号**。图 6 的验证曲线进一步显示，过滤数据训练的模型在 D_val 上收敛更稳定，验证 MinADE 持续优于全量数据训练。

#### 多轮反事实训练的自改进效应

表 1 中 round2 相比 round1 的结果表明，将第一轮 CF-VLA 的输出重新送入 rollout–filter–label 管线，生成第二轮反事实数据并继续训练，可进一步降低轨迹误差和安全指标，同时压缩思考率和输出长度。这证明了管线具有**自改进能力**：随着基础模型能力增强，其失败模式向更难、更细微的场景集中，后续轮次的过滤管线能够针对这些场景生成更精准的反事实标签，形成正向循环。

### 失败模式分析

论文提供了两类定性失败案例，揭示了 CF-VLA 的局限性。

**过度校正。** 图 15 展示了一个典型失败：在直道行驶的安全场景中，CF-VLA 错误地建议执行不必要的左变道。反事实推理误读了视觉线索（可能将相邻车道车辆的正常行驶解读为需要避让），导致原本正确的计划被“修正”为错误计划。这表明反事实推理在缺乏明确危险信号时，可能产生**虚幻的意图改变**。

**过度保守。** 图 16 展示了另一个失败模式：CF-VLA 的推理否决了一个合理的“等待-加速”计划，将其替换为纯等待策略。模型错误地判断了红灯与自车的位置关系，导致不必要的保守行为。图 12 也呈现类似趋势——模型在切入场景中纠正了过长的减速，但选择了保守的保持车道策略，而非人类驾驶员可能采取的超越行为。

这些失败模式指向一个核心问题：**反事实推理由教师模型（Qwen2.5-VL-72B-Instruct）生成，可能继承其偏见和幻觉倾向**。教师模型在生成推理时使用硬性约束（如“仅输出一个最关键问题”），可能丢失部分必要信息；同时，教师模型自身的视觉理解偏差会直接传导至学生模型的自反思行为。

### 关键图表结论

- **表 1**：CF-VLA 在轨迹精度（MinADE ↓17.6%）、安全性（碰撞率 ↓20.5%）和推理质量（IOU 持平且编辑后提升）三个维度全面超越基线，多轮训练进一步增效。
- **表 2**：预填充真实元动作使误差减半，证实元动作是核心瓶颈；自适应推理在性能和效率间取得最优平衡。
- **表 3/表 4**：数据过滤管线是提取可靠自反射信号的关键，过滤后模型性能更优、思考更高效。
- **图 6**：过滤数据训练的验证曲线更稳定且误差更低，验证了管线对数据质量的控制作用。
- **图 15/图 16**：失败案例揭示了过度校正和过度保守两种典型失败模式，根因在于教师模型的偏见传导和视觉理解偏差。

### 公平性说明

所有基线模型均从同一 traj-only 检查点初始化，训练数据、评估协议和硬件环境保持一致。评估在专有数据集上进行，未在公开基准（如 nuScenes、Waymo Open Dataset）上测试，可能限制与外部工作的直接比较。读者在引用性能数字时需注意此上下文差异。

![[assets/figures/papers/paper_list_l2381_https_arxiv_org_abs_2512_24426/figures/006_Table_2.jpg]]
*Table 2: Ablations on meta–trajectory alignment and adaptive counterfactual reasoning. We train models without route information*

![[assets/figures/papers/paper_list_l2381_https_arxiv_org_abs_2512_24426/figures/007_Table_3.jpg]]
*Table 3: Effect of our proposed data filtering pipeline. Models are fine-tuned with route information from meta-act (w/ route)*

![[assets/figures/papers/paper_list_l2381_https_arxiv_org_abs_2512_24426/figures/008_Figure_5.jpg]]
*Figure 5: Qualitative results of CF-VLA. For three representative and safety-critical scenarios, each row shows the model’s initial metaactions (left), the reasoning trace (middle), and the updated meta-actions (right) together with the resulting trajectory. The counterfactual reasoning step identifies issues (missing lane changes, late turns, and failure to slow for pedestrians) and edits the meta-actions accordingly*

![[assets/figures/papers/paper_list_l2381_https_arxiv_org_abs_2512_24426/figures/010_Table_4.jpg]]
*Table 4: Effect of our proposed data filtering pipeline. We use models with route information and train them with the counterfactualD→1traj → D→10meta → D→10CFD→1traj → D→2meta → D→10CF reasoning traces on the filtered or the whole training dataset*

## 定位与知识库关联

### 问题定位：从描述性推理到自反射反事实推理

当前视觉-语言-动作（VLA）模型在自动驾驶中已展现出将视觉感知、语言推理与动作规划统一建模的潜力。然而，现有方法的核心瓶颈在于：模型仅在生成动作之前输出**一次性描述性推理**（one-shot descriptive reasoning），即描述当前场景和驾驶意图，却缺乏对自身计划的**反事实自反思**能力——它无法在执行前追问“如果我这样做了，会发生什么？”，更无法据此修正不安全的决策。

CF-VLA 的因果调节变量是引入一个基于**预测元动作的反事实自反射推理循环**：模型首先生成时间分段元动作（time-segmented meta-actions）作为语言可解释的中间表征，然后对这些元动作进行反事实推理，分析潜在后果并修正元动作，最终生成轨迹。这一设计的核心洞察在于：将元动作作为语言原生的中间抽象层，使模型能够“谈论”并“反思”自己的动作计划，从而赋予 VLA 内生的自反射反事实推理能力，无需依赖外部验证器或规则检查器。

### 与基线方法的差异分析

论文通过三个递进的基线模型清晰刻画了 CF-VLA 的增量贡献：

- **traj-only**：纯轨迹预测基线，直接从传感器数据映射到未来轨迹，无元动作或推理模块。这是最基础的行为克隆范式，完全不具备可解释性和自反思能力。
- **meta-act**：在 traj-only 基础上引入元动作序列作为中间基元，将规划分解为纵向（加速/减速/保持/等待/倒车）、横向（直行/左转/右转）和车道（保持/左变道/右变道）三个维度的时间分段动作。该基线使模型输出更结构化，但仍无推理能力。
- **lang-meta-act**：同时预测语言推理、元动作和轨迹，但其推理是**描述性**的（描述场景和意图），而非反事实的。它不质疑自身计划，也不进行修正。

CF-VLA 在上述基线上实现了五个关键槽位的变更：

| 变更槽位 | 基线值 | CF-VLA 值 |
|---------|--------|-----------|
| 推理模式 | 一次性描述性推理 | 基于预测元动作的自反射反事实推理 |
| 中间动作表征 | 隐空间 token 或连续轨迹 token | 语言可解释的时间分段元动作 |
| 训练数据构建 | 从驾驶数据直接行为克隆 | rollout–filter–label 自改进管线 |
| 训练策略 | 标准微调，样本等同对待 | 混合数据训练 + 损失加权（1:10:10）+ 首元动作块掩码 |
| 推理触发 | 始终推理或任务边界切换 | 自适应推理：模型从数据混合中隐式学习何时推理 |

其中，**rollout–filter–label 数据管线**是 CF-VLA 方法论的独特贡献。该管线首先让基础 VLA 在训练数据上滚动输出（rollout），然后通过比较自由生成轨迹与预填充真实元动作诱导轨迹的误差，自动筛选出元动作存在问题的高价值场景（过滤条件：$\min \mathrm{ADE}(\mathbf{x}_{\mathrm{pf}}, x^\star) < \min \mathrm{ADE}(\mathbf{x}_{\mathrm{free}}, x^\star)$ 且 $\min \mathrm{ADE}(\mathbf{x}_{\mathrm{free}}, x^\star) > \epsilon, \epsilon=0.5$），最后使用高容量教师模型（Qwen2.5-VL-72B-Instruct）为这些场景标注反事实推理痕迹。这一管线形成了自改进循环：第二轮 CF-VLA 训练使用第一轮 CF-VLA 的滚动输出数据，进一步压缩推理开销并提升性能。

### 知识库定位：在 VLA 与自动驾驶推理研究中的坐标

CF-VLA 处于以下几条研究脉络的交汇点：

1. **VLA 模型谱系**：继承自将视觉-语言模型（VLM）应用于机器人/自动驾驶动作生成的范式。与直接预测连续轨迹的端到端方法不同，CF-VLA 通过元动作这一离散化中间层将规划问题部分转化为语言建模问题，使模型能够利用 VLM 的语言推理能力。

2. **推理增强规划**：区别于在推理阶段依赖外部验证器或规划器的方法，CF-VLA 将反事实推理**内化**到模型自身的生成过程中。这种内生的自反思机制与 chain-of-thought 推理有相似之处，但关键区别在于其推理对象是模型自身生成的元动作计划，而非仅对输入场景的描述。

3. **数据驱动自改进**：rollout–filter–label 管线与强化学习中的 self-play 和数据增强中的难例挖掘有概念上的亲缘性，但将其应用于 VLA 的反事实推理标注是新的实践。该管线不依赖人工标注，也不需要环境交互反馈，仅通过模型自身的轨迹分歧信号驱动数据筛选。

4. **自适应计算**：CF-VLA 的自适应推理机制使模型在简单场景下直接输出动作，仅在困难场景下触发反事实推理循环。这与 conditional computation 和 early-exit 等自适应推理范式相呼应，但实现方式是通过数据混合让模型隐式学习推理触发条件，而非显式的门控网络。

### 适用边界与局限

尽管 CF-VLA 在内部验证集上展现出显著的性能提升，其适用边界和局限值得审慎评估：

**数据依赖性**：所有实验均在专有大规模数据集（约 1160 万段 20 秒视频片段，43.3 万段元动作标注片段）上进行，未在公开基准（如 nuScenes、Waymo Open Dataset）上验证。模型对传感器配置、地理环境和驾驶文化的泛化能力尚不明确，需要独立验证。

**教师模型偏差**：反事实推理标签由 Qwen2.5-VL-72B-Instruct 教师模型生成，CF-VLA 可能继承该模型的推理偏差、幻觉倾向或保守偏好。论文中展示的失败案例（Figure 15: 错误建议变道；Figure 16: 过度保守地否定加速并误判交通灯）提示了这一风险。

**自适应推理的隐式性**：推理触发完全从数据混合中隐式习得，缺乏显式的不确定性校准机制。在分布外场景下，模型可能错误地跳过必要推理或进行不必要的推理。Figure 8 显示解码温度与思考率存在强负相关，表明推理触发对采样策略敏感。

**过度校正风险**：反事实推理可能引入新的安全问题——将原本安全的计划修正为不安全计划（如不必要的变道），或将合理的动态决策修正为过度保守的行为（如不必要的长时间等待）。

**计算开销**：虽然自适应推理降低了平均推理成本，但在需要反事实推理时仍引入额外的自回归生成开销。论文未提供推理延迟的定量数据，对于极端实时性要求的部署场景，这一开销需要进一步评估。

### 开放问题

1. **跨领域泛化**：rollout–filter–label 管线能否扩展到不同驾驶环境（如不同国家、不同交通规则）或更广泛的机器人操作领域？元动作的定义是否需要领域特定的重新设计？

2. **推理质量提升**：如何减少反事实推理中的幻觉和过度校正？是否可以通过引入反事实推理的真值标注（如人类驾驶员的反事实思考）或偏好优化来提升推理准确性？

3. **多维过滤信号**：当前数据过滤仅依赖轨迹误差（ADE），是否可以融合安全性（碰撞率）、舒适度（加加速度）、交通规则合规性等多维指标来筛选更高价值的反事实样本？

4. **显式不确定性集成**：自适应推理能否与显式的不确定性估计（如预测分布的熵、置信度校准）结合，提供更可靠的推理触发决策？是否可以通过人类反馈的偏好优化来对齐推理触发策略？

5. **安全边界保障**：在极端 corner case 下，CF-VLA 的内生自反思是否足够稳健，还是需要与基于规则的安全层（如责任敏感安全模型 RSS）集成作为最后防线？

## 原文 PDF

![[paperPDFs/CVPR_2026/Counterfactual_VLA_Self_Reflective_Vision_Language_Action_Model_with_Adaptive_Reasoning.pdf]]
