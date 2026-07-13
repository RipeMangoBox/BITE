---
title: Acting as Inverse Inverse Planning
type: paper
paper_level: A
venue: SIGGRAPH
year: 2023
pdf_ref: paperPDFs/SIGGRAPH_2023/Acting_as_Inverse_Inverse_Planning.pdf
project_link: "https://social-intelligencehuman-ai.github.io/docs/camready\\_12.pdf"
code_link: "https://people.csail.mit.edu/kach/a2i2p/"
aliases:
- IIP
- AAIIP
tags:
- SIGGRAPH_2023
- topic/other_unclear
core_operator: 引入基于观众反向规划（inverse planning）模型的逆逆向规划（inverse inverse planning）框架，通过优化器直接最大化观众对特定目标的后验信念。
primary_logic: 叙事表演可以建模为“逆逆向规划”：通过选择角色动作来操纵基于贝叶斯推断的观众心理模型，从而以模块化和高层的方式表达帮助、阻碍、剧情反转、讽刺、闪回等多种故事效果。
claims:
- 在帮助任务中，逆逆向规划生成的动画使73%的观众正确感知到帮助关系，而朴素规划基线仅为6%（p ≪ 0.01）。
- 在阻碍任务中，逆逆向规划达到62%准确率，朴素规划为29%（p ≪ 0.01）。
- 在物理世界“默剧”实验中，95.7%的观众认为默剧角色拉的盒子比轻盒重，68.6%认为甚至比实际重盒重。
- 图2定性展示逆逆向规划生成的帮助动画远比朴素规划有效，模型从初始就对帮助关系高度置信。
---

# Acting as Inverse Inverse Planning

> [!tip] 核心洞察
> 叙事表演可以建模为“逆逆向规划”：通过选择角色动作来操纵基于贝叶斯推断的观众心理模型，从而以模块化和高层的方式表达帮助、阻碍、剧情反转、讽刺、闪回等多种故事效果。

| 字段 | 内容 |
|------|------|
| 中文题名 | 作为逆逆向规划 |
| 英文题名 | Acting as Inverse Inverse Planning |
| 会议/期刊 | SIGGRAPH 2023 |
| Links | [paper](https://arxiv.org/abs/2305.16913) · [Code](https://people.csail.mit.edu/kach/a2i2p/) · [paper](https://arxiv.org/pdf/1903.06445.pdf) · [Project](https://social-intelligencehuman-ai.github.io/docs/camready\_12.pdf) |
| Topic | #topic/other_unclear |
| Method | Inverse Inverse Planning |
| Dataset | Grid-world depiction task: Helping, Grid-world depiction task: Hindering, Grid-world depiction task: Indifference, Physics-world box weight perception: Mime vs. Light box |

> [!tip] 效果简介
> - Grid-world depiction task: Helping 上，参与者选择“帮助”的比例 73% vs 6% (+67%)。
> - Grid-world depiction task: Hindering 上，参与者选择“阻碍”的比例 62% vs 29% (+33%)。
> - Grid-world depiction task: Indifference 上，参与者选择“漠不关心”的比例 N/A（与基线效果相当） vs N/A (≈0%)。

## 概要

传统叙事动画生成依赖智能体的最优规划，忽视观众如何推断角色意图，导致动画无法有效传达帮助、阻碍等高层叙事关系。本文提出 **逆逆向规划（Inverse Inverse Planning）** 框架：将叙事表演建模为对观众认知模型的优化——通过选择角色动作序列，最大化模拟观众反向规划模型对特定目标（如“机器人在帮助奶酪”）的后验信念。在网格世界实验中，该方法生成的帮助动画使 73% 的观众正确感知到帮助关系，而朴素规划基线仅为 6%（p ≪ 0.01）；阻碍任务中达到 62% vs. 29%。该方法还支持情节转折、戏剧性讽刺、闪回等多种故事元素，并在物理模拟“默剧”实验中成功操纵观众对物体重量的感知。逆逆向规划为计算机图形学中的叙事动画提供了一种基于认知科学原理的模块化、高层创作范式。

## 核心方法与创新机理

### 问题瓶颈：叙事动画为何难以传达高层意图？

传统叙事动画生成依赖**智能体规划**（agent planning）：给定角色的隐藏目标（如“机器人想帮助奶酪到达粉色目标”），通过求解最优策略生成动作序列，再渲染为动画。这一范式存在根本性缺陷——它只考虑**角色如何最优地达成目标**，却完全忽略了**观众如何从观察到的行为中推断角色意图**。如图 1 所示，当机器人和奶酪都执行各自的最优策略时，观众看到的只是两个角色在网格中各自移动，难以察觉机器人“帮助”奶酪的意图。朴素规划（naïve planning）产生的动画在传达帮助关系上极其失败：后续人类实验证实，仅 6% 的观众正确感知到帮助关系。

这一瓶颈的本质在于：**叙事表演的核心不是“角色做什么”，而是“观众从角色的行为中推断出什么”**。动画生成逻辑需要从“执行最优策略”转变为“操纵观众的认知推断过程”。

### 核心洞察：叙事即逆逆向规划

本文的核心创新是将叙事动画生成建模为**逆逆向规划**（Inverse Inverse Planning, A2I2P）。这一命名的逻辑链条如下：

1. **正向规划**（Planning）：给定目标，计算最优动作序列。
2. **反向规划**（Inverse Planning）：给定观察到的动作序列，反向推断隐藏目标——这是认知科学中理解智能体行为的标准计算模型（Baker et al. 将“动作理解”建模为反向规划）。
3. **逆逆向规划**（Inverse Inverse Planning）：给定“希望观众推断出的目标”，反向优化动作序列，使得观众（模拟为反向规划模型）的后验信念最大化。

类比于图形学中的“逆逆向渲染”（inverse inverse rendering）——先逆向渲染从图像推断场景参数，再逆逆向渲染优化场景参数使渲染结果匹配目标图像——本文的框架将叙事创作定义为：**通过优化角色动作来操纵基于贝叶斯推断的观众心理模型，从而以模块化、可组合的方式表达帮助、阻碍、剧情反转、戏剧讽刺、闪回等多种故事效果**。

### 核心机制：优化观众信念而非角色行为

框架的**唯一因果旋钮**（causal knob）是：将动画生成逻辑从“执行针对固定目标的最优策略”改为“通过搜索/优化动作序列，最大化观众反向规划模型对特定目标的后验信念”。这一 changed slot 使得系统从**行为驱动**转变为**认知驱动**。

具体而言，给定一个叙事目标（如“让观众相信机器人在帮助奶酪”），系统定义一个**目标函数** $f(\sigma)$，该函数对脚本 $\sigma$（即初始状态和动作序列）进行评分，评分依据是模拟观众——一个运行贝叶斯反向规划的认知模型——在观察脚本每一步后的信念状态。优化器（beam search 或梯度下降）搜索使 $f(\sigma)$ 最大化的脚本，渲染为最终动画。

### 模块架构与推理路径

系统由五个模块串联构成，形成完整的**认知优化管线**：

#### 1. 世界模型（World Model）
定义动画发生的状态空间、动作空间、转移函数与奖励函数。网格世界版本基于 Ullman et al. 的设定：两个角色在带墙壁的网格中移动，奶酪有粉色/绿色两个可能目标，机器人有社会倾向参数 $\rho_{\text{robot}}$（正值表示帮助奶酪，负值表示阻碍）。物理世界版本使用可微物理仿真器，包含跳跃机器人（hopper）拉动箱子的场景。世界模型为后续所有模块提供共享的语义基础。

#### 2. 规划模块（Planning Module）
为每个可能的角色目标假设 $H$ 预计算近似最优策略和价值函数。网格世界中使用**价值迭代**（value iteration），物理世界中使用 **Short-Horizon Actor-Critic** 算法（Xu et al. 2022）。规划模块的输出是 $\boldsymbol{Q}_c^H(s, a)$——在假设 $H$ 下角色 $c$ 在状态 $s$ 选择动作 $a$ 的 Q 值。这一模块是**离线预计算**的，为后续的观众推断和脚本优化提供动作似然基础。

#### 3. 观众反向规划（Audience Inverse Planner）
这是系统的**认知核心**，模拟观众如何从观察到的动作序列推断角色的隐藏目标。给定假设空间 $\mathcal{H}$（包含奶酪目标 $G_{\text{cheese}}$、机器人目标 $G_{\text{robot}}$、机器人社会倾向 $\rho_{\text{robot}}$ 的组合），反向规划器执行贝叶斯推断：

**动作似然**（软极大策略）：
$$\mathsf P ( s \to a \mid H ) \propto \exp \left( \boldsymbol \beta \cdot \boldsymbol Q _ { c } ^ { H } ( s , a ) \right)$$

其中 $\beta$ 为逆温度参数，控制角色行为的理性程度。

**目标后验**（贝叶斯规则）：
$$\mathsf P ( H \mid s \to a ) \propto \mathsf P ( s \to a \mid H ) \mathsf P ( H )$$

反向规划器在每一步观察新动作后更新所有假设的后验分布，形成观众对角色关系的动态信念轨迹。这一模块是**可微的**（在物理世界版本中），使得梯度优化成为可能。

#### 4. 逆逆向规划优化器（Inverse Inverse Planning Optimizer）
这是系统的**决策核心**，负责搜索最大化目标函数的脚本。根据场景复杂度，使用两种优化策略：

- **离散搜索**（网格世界）：使用 **beam search**，beam width 通常为 100。优化器在每一步展开多个候选动作组合，用反向规划器评估每个候选脚本前缀的信念状态，保留得分最高的 beam。
- **梯度优化**（物理世界）：使用梯度下降直接优化连续轨迹参数，因为物理仿真器和反向规划器均可微。

优化器与反向规划器之间存在**紧密的反馈循环**：优化器每尝试一个候选动作序列，反向规划器就模拟观众对该序列的推断结果，优化器根据推断结果调整搜索方向。这种“生成-推断-评估”的闭环是框架能够有效操纵观众认知的关键。

#### 5. 动画渲染（Rendering）
将优化后的动作序列渲染为视频。在 44 核服务器上，整个优化+渲染流程可在两分钟内完成。

### 关键目标函数：叙事效果的模块化编码

框架的核心优势在于**叙事效果的模块化表达**：不同的故事元素通过组合不同的目标函数项来实现，无需修改底层认知模型。以下是几个关键目标函数及其因果机制：

**帮助（Helping）**：
$$f _ { \mathrm { h e l p } } ( \sigma ) = \sum _ { 1 \le t \le T } \mathsf { P } ( \rho _ { \mathrm { r o b o t } } > 0 \mid \sigma _ { 1 : t } )$$
最大化每一步观众认为机器人社会倾向为正的后验概率。优化器会搜索那些让机器人的行为“看起来像在帮助”的动作序列——例如机器人主动推动奶酪向其目标移动。

**剧情反转（Plot Twist）**：
$$f _ { \mathrm { t w i s t } } ( \sigma ) = \sum _ { t } \left\{ \begin{array} { l l } { \mathrm { P } ( \rho _ { \mathrm { r o b o t } } > 0 \mid \sigma _ { 1 : t } ) } & { t \leq T / 2 } \\ { \mathrm { P } ( \rho _ { \mathrm { r o b o t } } < 0 \mid \sigma _ { 1 : t } ) } & { t > T / 2 } \end{array} \right.$$
前半段最大化“帮助”信念，后半段切换为最大化“阻碍”信念。因果机制：优化器必须在前半段积累足够的帮助证据，同时在后半段引入反转行为，使得观众经历信念的剧烈转变。

**戏剧讽刺（Dramatic Irony）**：
$$\begin{array} { l } { { f _ { \mathrm { i r o n y } } ( \sigma ) = \displaystyle \sum _ { t } + \mathsf { P } ( G _ { \mathrm { c h e e s e } } = \mathrm { g r e e n } \mid \sigma _ { 1 : t } ) \qquad } } \\ { { \qquad + \mathsf { P } ( \rho _ { \mathrm { r o b o t } } < 0 \mid \sigma _ { 1 : t } , G _ { \mathrm { c h e e s e } } = \mathrm { g r e e n } ) } } \\ { { \qquad + \mathsf { P } ( \rho _ { \mathrm { r o b o t } } > 0 \mid \sigma _ { 1 : t } , G _ { \mathrm { c h e e s e } } = \mathrm { p i n k } ) \qquad } } \end{array}$$
机器人基于错误信念行动：当奶酪实际目标为绿色时，机器人误以为目标是粉色并“帮助”奶酪走向粉色，实则阻碍了奶酪。目标函数同时最大化“观众知道奶酪目标是绿色”的信念和“在绿色目标条件下机器人是阻碍”的信念。因果机制：观众拥有机器人不具备的信息，产生讽刺感。

**叙事弧（Narrative Arc）**：
$$f _ { \mathrm { a r c } } ( \sigma ) = \displaystyle \sum _ { t } + \sin ( t / T \cdot 3 \pi ) \cdot \mathbf { E } \left[ V _ { \mathrm { r o b o t } } ^ { H } ( s _ { t } ) \mid \sigma _ { 1 : t } \right] - 0 . 1 \cdot D _ { \mathrm { K L } } ( H _ { 1 : t - 1 } \parallel H _ { 1 : t } )$$
让机器人的期望价值函数沿 1.5 个正弦周期波动（升-降-升），同时用 KL 散度惩罚目标信念的突变以保持角色一致性。因果机制：优化器搜索使机器人“处境”先改善、后恶化、再改善的动作序列，创造出经典的叙事张力曲线。

### 训练与推理路径

系统**不需要训练**（在机器学习意义上），而是依赖**预计算+在线优化**：

1. **离线阶段**：对世界模型中所有可能的角色目标假设，使用价值迭代或 Actor-Critic 预计算最优 Q 函数。这一计算复杂度随状态空间和假设空间增长，是系统的主要扩展瓶颈。
2. **在线阶段**：给定叙事目标（目标函数），优化器通过 beam search 或梯度下降搜索最优脚本。每一步候选评估都需要运行完整的贝叶斯反向规划（枚举所有假设的后验更新），计算成本随序列长度 $T$ 和假设空间大小 $|\mathcal{H}|$ 线性增长。
3. **渲染阶段**：将最优脚本渲染为视频。

推理路径的关键因果链为：**叙事目标 → 目标函数 → 优化器搜索 → 候选脚本 → 反向规划器评估 → 信念状态 → 目标函数评分 → 选择最优脚本 → 渲染动画**。这一链条中，反向规划器是观众认知的代理模型，优化器是叙事者的决策代理，两者通过目标函数形成闭环。

## 实验与关键发现

### 网格世界叙事传达实验

作者在网格世界环境中设计了帮助、阻碍、漠不关心三种叙事传达任务，系统比较了**逆逆向规划（Inverse Inverse Planning）**与**朴素规划（Naïve Planning）**的观众感知效果。每段动画时长约 15 步，观众观看后需回答机器人对奶酪的态度（帮助、阻碍或漠不关心）。

**核心结果（Figure 5）**：

| 任务 | 逆逆向规划 | 朴素规划 | 提升幅度 | 显著性 |
|------|-----------|---------|---------|--------|
| 帮助（Helping） | **73%** | 6% | +67% | p ≪ 0.01 |
| 阻碍（Hindering） | **62%** | 29% | +33% | p ≪ 0.01 |
| 漠不关心（Indifference） | 与基线相当 | 相当 | ≈0% | 无显著差异 |

在帮助任务上，逆逆向规划使观众正确感知帮助关系的比例达到 73%，而朴素规划仅有 6%——前者是后者的 **12 倍**。这一巨大差异的因果机制在于：朴素规划中角色各自执行最优策略，机器人的“帮助”行为与奶酪自身向目标移动的行为在视觉上难以区分（Figure 1）；逆逆向规划则通过 beam search 优化动作序列，直接最大化观众反向规划模型对“机器人有帮助”的后验信念 $f_{\mathrm{help}}(\sigma) = \sum_{t} \mathsf{P}(\rho_{\mathrm{robot}} > 0 \mid \sigma_{1:t})$，从而生成机器人主动推挤奶酪、为其开路等明确传达帮助意图的动作（Figure 2）。

![[assets/figures/papers/paper_list_l51_https_arxiv_org_abs_2305_16913/figures/003_Figure_1.jpg]]
*Figure 1: (top) Suppose we animate a robot that is helping the cheese reach its goal, by having both characters follow their optimal policies (“naïve planning,” Section 2). This produces a poor depiction: it is not clear that the robot wants to help the cheese, only that it wants to go to green. (bottom) The inverse planner agrees. It infers that the cheese wants pink (first plot), and that the robot wants green (second plot; notice bump at ?? = 10 when the robot reaches green and stays). But it remains uncertain about the robot’s alignment (third plot), because the robot’s behavior is consistent with both ambivalence to the cheese and wanting to help the cheese (but doing nothing because the cheese...*

![[assets/figures/papers/paper_list_l51_https_arxiv_org_abs_2305_16913/figures/004_Figure_2.jpg]]
*Figure 2: (top) Using inverse inverse planning, we optimize animations that maximize the inverse planner’s belief that the robot is helpful (Section 3). This finds a much more effective depiction. (bottom) Now, it is clear that the robot is helping, and indeed the model is confident of that from the beginning (third plot)*

在阻碍任务上，逆逆向规划同样显著优于基线（62% vs 29%），但绝对准确率低于帮助任务。这提示“阻碍”叙事的传达难度更高——观众需要从动作中同时推断机器人的目标与奶酪目标的冲突，认知负荷更大。漠不关心任务上两者效果相当，说明当叙事目标本身缺乏强烈信号时，优化空间有限。

### 物理世界“默剧”实验

为验证框架在连续物理环境中的适用性，作者构建了一个可微物理仿真器：一个单足跳跃机器人（hopper）通过弹簧连接一个盒子，位于斜坡上（Figure 6a）。实验目标是让机器人通过“表演”（miming）来传达盒子的重量感知——实际拉的是轻盒（质量为 1），但希望观众认为它很重。

**观众感知结果**：
- **95.7%** 的观众认为默剧机器人拉的盒子比轻盒更重（ground truth：97% 选择实际重盒）
- **68.6%** 的观众认为默剧盒子甚至比实际重盒更重——尽管默剧盒子的质量仅为重盒的 1/5

该实验的优化目标是通过梯度下降调整机器人的关节力矩轨迹，最大化观众逆规划模型对“盒子很重”的信念。生成的动画中，机器人表现出夸张的倾斜身体、缓慢拖拽等特征，成功“欺骗”了绝大多数观众。这一结果证明逆逆向规划框架可以扩展到连续动作空间，且能处理“传达虚假物理属性”这类更微妙的叙事意图。

### 定性叙事效果验证

除定量实验外，作者展示了多种故事元素的生成动画（Figure 3、Figure 4），定性验证了框架的表达能力：

![[assets/figures/papers/paper_list_l51_https_arxiv_org_abs_2305_16913/figures/007_Figure_4.jpg]]
*Figure 4: Example animations generated in Section 3 (continued from above)*

- **情节转折（Plot Twist）**：前半段机器人帮助奶酪向粉色目标移动，后半段突然将奶酪推离目标并阻挡其去路。目标函数 $f_{\mathrm{twist}}$ 在 $t \leq T/2$ 时最大化 $\mathsf{P}(\rho_{\mathrm{robot}} > 0)$，在 $t > T/2$ 时最大化 $\mathsf{P}(\rho_{\mathrm{robot}} < 0)$，实现了观众信念的戏剧性翻转。
- **戏剧性讽刺（Dramatic Irony）**：机器人基于错误信念（以为奶酪目标是绿色）行动，看似帮助实则阻碍。目标函数 $f_{\mathrm{irony}}$ 同时最大化观众对奶酪真实目标的信念和条件于该目标下机器人行为的反向推断。
- **闪回（Flashback）**：在动画末尾插入一段“过去”的推动动作，强化帮助叙事。
- **故事弧（Narrative Arc）**：通过 $f_{\mathrm{arc}}$ 使机器人的价值函数沿正弦曲线波动，同时用 KL 散度惩罚目标信念的突变，生成具有“起-落-起”节奏的叙事。

所有优化在配备 44 个 CPU 的服务器上均可在 **2 分钟内**完成渲染，证明方法在计算上是可行的。

### 方法适用边界与失败模式

**适用边界**：
1. **状态空间规模受限**：网格世界实验仅涉及 $5 \times 5$ 网格和两个简单角色；物理实验为低自由度单足机器人。价值迭代和枚举式贝叶斯推理的时间复杂度随状态空间指数增长，难以直接扩展到高维环境。
2. **观众模型假设过强**：整个优化过程假设观众严格遵循论文中的反向规划模型进行推断。实际人类观众存在认知偏差、注意力波动和个体差异，当真实观众与模型偏差较大时，优化效果可能下降。
3. **离线策略依赖**：最优策略和价值函数需预先离线计算，动画生成时角色行为被锁定在预计算策略中，无法适应动态变化的交互环境。

**已知失败模式**：
- 漠不关心任务的优化结果与朴素规划无显著差异，说明当叙事目标本身缺乏强信号时，逆逆向规划无法“无中生有”地创造观众感知。
- 阻碍任务的绝对准确率（62%）远低于帮助任务（73%），表明某些叙事类型的传达本质上更困难，优化器可能受限于世界模型提供的动作表达能力。
- 物理默剧实验中，仍有 31.4% 的观众未被“欺骗”（认为默剧盒子不比实际重盒更重），说明优化器找到的轨迹并非对所有观众都有效。

**需人工验证的边界**：论文未提供消融实验（如去掉目标函数中特定项的影响、不同 beam search 宽度对结果的影响），也未系统测试观众模型参数（如理性系数 $\beta$）的敏感性。这些缺失使得方法对模型超参数的鲁棒性难以评估。

![[assets/figures/papers/paper_list_l51_https_arxiv_org_abs_2305_16913/figures/009_Figure_5.jpg]]
*Figure 5: In Section 3.4.1 we empirically compare inverse inverse planning and naïve planning on three depiction tasks: showing the robot to be helping, hindering, or indifferent. Participants viewed the resulting animations and reported their impression of the robot (help / hinder / indifferent / unclear). Each bar represents a separate animation (from a different random seed), showing the proportion of participants who reported the desired response for that animation. Horizontal dashed lines are averages across animations for each condition (higher is better) and shaded areas span 95% confidence intervals for each condition. Our animations are significantly more effective than the naïve planning ba...*

![[assets/figures/papers/paper_list_l51_https_arxiv_org_abs_2305_16913/figures/002_Table_1.jpg]]
*Table 1: “Inverse inverse planning” is analogous to past graphics work on “inverse inverse rendering.”*

## 定位与知识库关联

本文的核心贡献在于将叙事动画生成问题从“为角色规划动作”转变为“为观众规划信念”，即改变了一个关键槽位：**动画生成逻辑**。传统方法（本文称为朴素规划，Naïve planning）直接执行角色针对固定目标的最优策略来生成动作序列，不考虑观众如何从这些动作中推断角色的隐藏意图。本文提出的**逆逆向规划**（Inverse Inverse Planning）则通过优化器（beam search 或梯度下降）直接最大化模拟观众反向规划模型对特定目标的后验信念，从而生成能有效传达高层叙事意图（帮助、阻碍、剧情反转、讽刺等）的动作序列。

### 与已有工作的本质差异

**逆逆向渲染**（Inverse Inverse Rendering）是计算机图形学中一类成熟的方法论：给定期望的图像，反向推断场景参数，再正向渲染生成最终图像。本文在 Table 1 中明确将逆逆向规划定位为这一传统的延续，只是将优化目标从“像素值”替换为“观众心理状态”。这一类比揭示了方法论的深层一致性，但逆逆向规划面对的是完全不同的技术挑战：观众模型是概率推理系统而非物理光学模型，优化空间是离散的动作序列而非连续的材质与光照参数。

与 **Baker 等人提出的“将动作理解视为逆向规划”**（action understanding as inverse planning）相比，本文实现了对称的翻转：Baker 等人用逆向规划来解释观察到的行为，而本文用“逆逆向规划”来生成能够被逆向规划者正确解读的行为。这一翻转使得原本用于认知建模的贝叶斯推断框架，直接成为动画创作的可微优化目标。

与基于强化学习的角色动画方法相比，本文不追求角色行为的物理真实性或任务效率，而是追求观众对角色关系的正确感知。朴素规划基线在帮助任务中仅让 6% 的观众感知到帮助关系，而逆逆向规划达到 73%（p ≪ 0.01），这一 67% 的差距直接证明了“为观众规划”与“为角色规划”之间的本质鸿沟。

### 知识库挂载点

本工作可挂载到以下知识节点：

1. **计算叙事学**（Computational Narratology）：首次将认知科学中的逆向规划模型作为可微优化目标引入叙事生成，为叙事自动化提供了可形式化、可验证的“观众体验”目标函数。此前该领域多依赖符号规则或模板，缺乏对观众推理过程的显式建模。

2. **认知科学驱动的图形学**（Cognition-inspired Graphics）：延续了将人类感知/认知模型嵌入图形学管线的传统，但将应用从视觉感知（如视觉注意力模型用于渲染优化）拓展到社会认知（推断他人意图与关系）。观众反向规划模型基于 **Ullman 等人**的工作，该模型本身已在人类行为实验中得到验证。

3. **人机交互与可解释 AI**：逆逆向规划生成的动画天然具有“可解释性”，因为优化目标直接对应观众应形成的信念。这一特性可连接到可解释强化学习、机器人动作生成等领域，其中智能体需要让人类观察者理解其意图。

### 适用边界

- **状态空间规模限制**：当前实现依赖精确的价值迭代和枚举式贝叶斯推理，仅适用于网格世界（约 400 个状态）和低自由度物理系统。扩展到高维连续状态空间需要引入近似推理（如神经网络观众模型）或基于采样的优化方法。
- **观众模型假设**：框架的有效性高度依赖观众反向规划模型的准确性。若真实人类观众的推理方式与模型存在系统性偏差（如认知偏差、文化差异），优化结果可能失效。本文未对人类观众的个体差异进行建模。
- **叙事模态局限**：当前仅处理角色的空间动作序列，未涉及对话、音乐、镜头语言等其他叙事模态。逆逆向规划框架在概念上可扩展到这些模态，但需要构建对应的多模态观众模型。
- **实时性不足**：优化过程需要数分钟（在 44 CPU 服务器上），无法用于实时交互式创作。对于离线动画制作，这一延迟可接受，但限制了在游戏等动态场景中的应用。

### 后续研究启发

1. **可微观众模型的构建**：用神经网络近似观众反向规划过程，可大幅提升优化效率，同时可能学习到更接近真实人类的推理模式。这需要收集人类在观看动画时的实时信念标注数据。

2. **艺术家交互界面**：如何让创作者直观地指定“希望观众感受到帮助”这样的高层目标？自然语言界面（如“让机器人看起来在帮助奶酪”）结合大型语言模型，可能成为连接创作者意图与形式化目标函数的桥梁。

3. **多智能体社会场景**：扩展到三个或更多角色的场景，涉及联盟、欺骗、竞争等复杂社会关系，需要定义更丰富的假设空间和目标函数族。

4. **与其他生成技术的融合**：逆逆向规划优化的动作序列可作为扩散模型或大型行为模型的微调信号，将“观众意识”注入更强大的生成系统中。

## 原文 PDF

![[paperPDFs/SIGGRAPH_2023/Acting_as_Inverse_Inverse_Planning.pdf]]