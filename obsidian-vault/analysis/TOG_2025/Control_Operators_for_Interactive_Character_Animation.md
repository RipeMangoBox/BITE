---
title: "Control Operators for Interactive Character Animation"
type: paper
paper_level: A
venue: TOG
year: 2025
pdf_ref: paperPDFs/TOG_2025/Control_Operators_for_Interactive_Character_Animation.pdf
project_link: null
code_link: null
aliases:
- COICA
tags:
- TOG_2025
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/robotics
core_operator: "将控制问题分解为有限的一组语义操作符（如Null, Bool, Encode, And, Or, Set, Array等），并为每种操作符自动生成对应的可训练神经网络模块，实现控制意图与网络结构的解耦，使非技术用户可通过蓝图脚本组合操作符定义控制模式。"
primary_logic: "通过让用户以类似逻辑和语义操作的方式组合控制操作符，并自动映射到背后的神经网络原语，可以在不要求用户具备机器学习知识的情况下，构建支持多技能、多控制模式的交互式角色控制器，同时保证控制器跨任务泛化和风格迁移。"
claims:
- "Control Operators 提供了一种非技术用户通过组合简单操作符来指定和设计交互式角色控制器的方法，而非整体构建网络。"
- "用户定义的输入控制结构被自动转化为网络架构，无需手动设计。"
- "框架与控制器无关，已成功应用于两种前沿控制器：基于片段的 Learned Motion Matching 变体和基于 Flow Matching 的自回归模型。"
- "控制编码器网络能够学习将语义相似的控制意图（如向左转的轨迹与置于左侧的目标）映射到相同的编码，实现跨任务风格泛化。"
---

# Control Operators for Interactive Character Animation

> [!tip] 核心洞察
> 通过让用户以类似逻辑和语义操作的方式组合控制操作符，并自动映射到背后的神经网络原语，可以在不要求用户具备机器学习知识的情况下，构建支持多技能、多控制模式的交互式角色控制器，同时保证控制器跨任务泛化和风格迁移。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 交互式角色动画的控制操作符 |
| 英文题名 | Control Operators for Interactive Character Animation |
| 会议/期刊 | TOG 2025 |
| Links | [paper](https://doi.org/10.1145/3763319) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/robotics |
| Method | Control Operators |
| Dataset | Internal Dataset, 100STYLE Dataset |

> [!tip] 效果简介
> - Internal Dataset 上，Foot Sliding (cm)↓ 为 0.249 ± 0.071 (LAFM)，对比 0.532 ± 0.195 (LAFM w/o skip connections)，变化 -0.283。
> - Internal Dataset 上，Toe Penetration Freq %↓ 为 0.862 ± 1.033 (LAFM)，对比 24.471 ± 21.590 (LAFM w/o latent space)，变化 -23.609。
> - 100STYLE Dataset 上，Foot Sliding (cm)↓ 为 0.251 ± 0.070 (LAFM)，对比 0.385 ± 0.183 (LAFM w/o skip connections)，变化 -0.134。

## 概要

交互式角色动画控制器的设计长期面临一个核心瓶颈：控制输入的设计高度依赖定制化的特征工程与专用网络架构，导致控制逻辑与神经网络深度耦合。每当设计师希望扩展新的行为、组合多种控制模式或调整控制逻辑时，都必须重新设计网络结构并重新训练，这对非技术用户构成了极高的门槛。

本文提出 **Control Operators**，将控制问题分解为一组有限的语义操作符（如 Null、Bool、Encode、And、Or、Set、Array 等），每种操作符自动映射为对应的可训练神经网络模块。用户通过蓝图脚本以类似逻辑运算的方式组合这些操作符来定义控制模式，网络架构随之自动生成，无需手动设计。这一设计实现了控制意图与网络结构的解耦，使不具备机器学习知识的设计师也能构建支持多技能、多控制模式的交互式角色控制器。

核心结论包括：

- **控制与架构解耦**：用户通过组合语义操作符描述控制模式后，网络结构自动生成，无需手动设计输入层或特征编码流程。
- **控制器无关性**：框架已成功应用于两种前沿控制器——基于片段的 Learned Motion Matching 变体与基于 Flow Matching 的自回归模型——验证了其通用性。
- **语义泛化**：控制编码器网络能够学习将语义相似的控制意图（如“向左转的轨迹”与“置于左侧的目标”）映射到相近的编码空间，从而实现跨任务风格迁移。
- **用户研究验证**：在可扩展性上显著优于 Motion Matching 和 Animation Blueprints，运动真实感与 Motion Matching 相当。

主要实验结果（Internal Dataset，LAFM 模型）表明：足部滑动从 0.532 cm 降至 0.249 cm，脚趾穿透频率从 24.47% 降至 0.86%；经蒸馏的单步推理将每帧运行时间从 2.890 ms 压缩至 0.784 ms，而控制编码器网络的内存开销小于 0.63 MB，CPU 时间小于 0.025 ms，相对主网络可忽略。

方法定位上，Control Operators 属于**控制编码自动化框架**，区别于手工特征工程的整体式控制器设计，也不同于强化学习中的策略网络条件化方案。它通过有监督学习将多任务控制变量整合进单一网络，在方法谱系中填补了“非技术用户可组合、可复用的控制编码原语”这一空白。

交互式角色动画是游戏与虚拟现实领域的核心技术，其目标是根据用户实时输入生成自然、响应迅速的角色运动。近年来，基于神经网络的控制器在运动质量与多样性上取得了显著进展，但在实际生产落地中面临一个根本性瓶颈：**控制输入的设计高度依赖定制化的特征工程与专用网络架构**。每当设计师希望添加新的控制模式（如从轨迹跟随切换到移动到目标，或引入风格化运动），通常需要重新设计输入特征、调整网络结构并重新训练整个模型。这种控制设计与神经网络的深度耦合，使得非技术用户（如动画师、游戏设计师）难以独立扩展和组合多种行为，迭代成本极高。

现有工业界的主流方案各有局限。**Motion Matching**（Büttner and Clavet 2015; Clavet 2016）通过最近邻搜索从动画数据库中选取片段，运动真实感强，但控制逻辑与数据检索紧密绑定，扩展新行为需要大量手工标注与规则调整。**Animation Blueprints**（Unreal 2022a）提供了可视化的动画逻辑编排能力，但本质上仍是状态机或流程图的变体，面对复杂、连续的多行为融合时，状态爆炸和过渡设计成为瓶颈。学术界基于学习的控制器虽然能生成高质量运动，但其控制接口往往是整体设计的——一个网络对应一组固定的控制信号，缺乏模块化和可复用性。

本文的核心洞察在于：**将控制问题分解为一组有限的语义操作符，并自动生成对应的可训练神经网络模块**，可以实现控制意图与网络结构的解耦。具体而言，Control Operators 框架允许用户以类似逻辑和语义操作的方式组合控制操作符（如 Null, Bool, Encode, And, Or, Set, Array 等），系统自动将这些操作符映射为背后的神经网络原语（线性层、注意力机制、拼接等），从而在不要求用户具备机器学习知识的前提下，构建支持多技能、多控制模式的交互式角色控制器。用户只需通过蓝图脚本定义控制模式，网络架构便随之自动生成，无需手动设计输入层或特征编码流程。

该框架与具体控制器架构无关，论文已成功将其应用于两种前沿方案：基于片段的 Learned Motion Matching 变体，以及基于 Flow Matching 的自回归模型。实验表明，Control Operators 不仅能够学习将语义相似的控制意图（如向左转的轨迹与置于左侧的目标）映射到相同的控制编码空间，还展现出跨任务风格泛化能力——仅在轨迹跟随任务上训练的特定风格，可自动泛化到移动到目标任务中。用户研究进一步证实，本文系统在可扩展性上显著优于 Motion Matching 和 Animation Blueprints，运动真实感与 Motion Matching 相当，为非技术用户的交互式角色动画设计提供了一条可行的解耦路径。

## 核心方法与创新机理

本文的核心创新在于提出 **Control Operators**——一组语义化的控制操作符，将交互式角色动画的控制输入设计从“手工特征工程+专用网络架构”的深度耦合模式中解耦出来，使非技术用户能够通过类似蓝图脚本的组合方式定义多行为、多控制模式的控制器，并自动生成对应的可训练神经网络模块。

### 从手工特征工程到语义操作符自动组合

传统基于神经网络的交互式角色控制器（如 Learned Motion Matching、Flow-Matching 控制器）面临一个关键瓶颈：**控制输入的设计高度依赖定制化的特征工程**。开发者需要针对每种控制类型（轨迹跟随、移动到目标、风格选择等）手动设计控制特征向量、处理缺失值、截断变长输入，并据此调整网络输入层的结构。每次新增或修改一种控制行为，都意味着重新设计特征编码流程和网络架构，这对非技术用户构成了极高的使用门槛。

Control Operators 的核心因果机制在于：**将控制问题分解为有限的一组语义操作符，并为每种操作符自动映射到对应的神经网络原语**。具体而言，本文定义了以下关键操作符及其网络映射：

- **Null / Bool / Encode**：基础操作符，分别产生空向量、布尔编码和全连接层编码，构成控制编码的原子单元。
- **And**：将多个控制向量拼接，对应网络中的拼接操作。
- **Or**：根据索引从预定义的控制集合中选择并变换，引入独热编码的条件选择机制。
- **Set**：使用多头自注意力对变长同类型控制向量集合进行编码，并拼接计数编码，天然处理可变数量输入。
- **Array / Dictionary**：通过索引-元素拼接或键值对拼接后送入 Set，实现有序数组和字典的编码。

这些操作符的自动网络映射机制（详见原文 Section 3.2–3.3）使得**用户定义的输入控制结构被自动转化为网络架构，无需手动设计**。用户只需在蓝图界面中描述控制模式（Control Schema），系统即可生成对应的 Control Encoder Network，将语义控制变量编码为固定维度的控制向量，馈入下游的运动生成网络。

### 控制器无关的框架设计

Control Operators 的另一个关键创新在于其**控制器无关性（controller-agnostic）**。该框架不绑定特定的运动生成模型，而是作为一个通用的控制编码前端。本文验证了其在两种前沿控制器上的有效性：

- **基于片段的 Learned Motion Matching 变体**：Control Encoder Network 输出控制编码，Projector Network 据此预测下一段动画的潜在姿态序列。
- **基于 Flow Matching 的自回归模型**：Flow Network 在自动编码器的潜在空间中以控制编码和前一姿态为条件，从噪声生成当前姿态。

这种解耦设计意味着，当用户需要调整控制逻辑时，只需修改 Control Schema 并重训练轻量的 Control Encoder Network，而无需改动下游的运动生成网络——这直接回应了“每次更改都需调整网络结构和训练流程”的核心痛点。

### 控制编码的语义泛化能力

Control Operators 的自动编码网络展现出超出显式设计的泛化特性。实验表明，**语义相似的控制意图（如向左转的轨迹与置于左侧的目标）会被映射到相近的控制编码空间**（Fig. 12），这使得模型能够在不同控制模式之间共享运动知识。更进一步，**仅在轨迹跟随任务上训练的特定风格（如 Mummy 风格）可以泛化到移动到目标任务**（Fig. 13），实现了跨任务的风格迁移。这种泛化能力并非来自手工设计的特征共享，而是 Control Encoder Network 在训练中自发学习到的控制语义结构。

### 与现有方法的本质差异

相较于工业界主流的 **Motion Matching**（Büttner and Clavet 2015; Clavet 2016）和 **Animation Blueprints**（Unreal 2022a），Control Operators 在以下维度实现了根本性改变：

| 维度 | Motion Matching / Animation Blueprints | Control Operators |
|------|----------------------------------------|-------------------|
| 控制设计方式 | 手工设计特征或状态机逻辑 | 组合语义操作符，自动生成网络 |
| 多行为扩展 | 需增加状态或修改搜索特征 | 通过 Or/Either 等操作符在单一网络中组合 |
| 变长输入处理 | 需特殊填充或截断 | Set/Array 操作符原生支持 |
| 网络架构 | 固定或手动调整 | 随控制模式自动生成 |

用户研究（Fig. 11）进一步证实，本文系统在可扩展性上显著优于 Motion Matching 和 Animation Blueprints，同时运动真实感与 Motion Matching 相当。

### 局限与开放问题

尽管 Control Operators 大幅降低了控制设计的门槛，其当前形式仍存在若干局限：训练时间较长（最复杂控制器约 20 小时），缺乏对运动加速度、响应时间等动力学特性的直接精确控制，且用户仍需理解基本的操作符语义。如何进一步缩短训练迭代周期、开发更精细的模型调节机制，以及将操作符扩展至空间信息（如高度图的卷积操作符），是值得探索的开放方向。

![[assets/figures/papers/paper_list_l22_https_doi_org_10_1145_3763319/figures/002_Figure_2.jpg]]
*Figure 2: Visual Overview of Control Operators. Here we show visual illustrations of our Basic Operators and examples of Control Operators defined in terms of other Control Operators*

Control Operators 框架将交互式角色动画控制器的设计问题，从“为每个控制任务手工定制神经网络”转变为“通过组合语义操作符声明控制意图，并自动生成对应的网络结构”。该框架由三个核心模块串联构成：**控制编码器网络 (Control Encoder Network)**、**自动编码器 (Auto-Encoder)** 和**姿态生成网络（Flow Network 或 Projector Network）**，其运行时数据流如 Fig. 5 所示。

### 1. 控制编码器网络：从蓝图到编码向量

控制编码器网络 $C$ 是框架的入口，也是核心创新所在。用户通过 Unreal Engine 的蓝图脚本定义**控制模式 (Control Schema)**，声明角色接受哪些控制变量（如目标位置、轨迹点序列、风格标签、布尔触发条件等）以及它们之间的逻辑关系。控制模式随后被自动编译为一组可训练的神经网络原语——即控制操作符的组合图。在运行时，蓝图将游戏输入映射为具体的控制变量值，送入 $C$ 网络，输出一个固定维度的**控制编码向量**，作为下游姿态生成网络的条件信号。

这一设计的关键因果机制是**解耦**：用户只需用类似游戏逻辑的语义操作符（如 `And`、`Or`、`Optional`、`Set`、`Array` 等）描述“我想控制什么”，而无需关心底层网络如何编码这些信号。网络结构——包括线性层、多头自注意力、拼接操作、独热编码等——由操作符图自动生成，控制意图与网络架构同步定义，从根本上消除了手工特征工程和网络架构反复调整的瓶颈。

### 2. 自动编码器：姿态的紧凑潜在空间

姿态生成网络不直接在高维姿态向量上操作，而是通过一个预训练的自动编码器 $(\mathcal{E}, \mathcal{D})$ 将姿态映射到 $d_z = 128$ 维的潜在空间。姿态向量 $\mathbf{p}$ 包含根关节的线速度和角速度、骨盆平移及其速度、各关节旋转及其角速度等变量，经归一化和关节链长度加权后，由编码器 $\mathcal{E}$ 压缩为潜在编码 $\mathbf{z}$，解码器 $\mathcal{D}$ 则从 $\mathbf{z}$ 重建完整姿态。该自动编码器重建精度极高，即使在关节链末端，位置误差也通常低于 $1\text{cm}$（Fig. 6）。潜在空间的引入有两个关键作用：其一，降低姿态歧义，提升生成稳定性；其二，为流匹配模型提供结构良好的概率流形。

### 3. 姿态生成网络：控制器无关的条件生成

框架支持两种前沿的姿态生成范式，体现其**控制器无关 (controller-agnostic)** 的特性：

- **Latent Auto-Regressive Flow-Matching (LAFM)**：在自动编码器的潜在空间中执行条件流匹配。推理时，从标准高斯分布 $\mathcal{N}(\mathbf{0}, \mathbf{I})$ 采样噪声 $\tilde{\mathbf{z}}$，以控制编码 $C(\mathbf{v}_f)$ 和前一帧的潜在姿态 $\hat{\mathbf{z}}_{f-1}$ 为条件，通过多步集成（$S=4$ 步即可饱和）将噪声逐步输运至目标条件分布，生成当前帧的潜在姿态 $\mathbf{z}_f$，再经解码器恢复为姿态向量。训练目标是最小化流网络 $\mathcal{V}$ 预测的瞬时速度与目标速度之间的均方误差：
  $$\mathcal{L}_{\theta_{\mathcal{V}}, \theta_C} = \mathbb{E}_{f,t,\tilde{\mathbf{z}}} \left\| \mathcal{V}(\bar{\mathbf{z}}, \hat{\mathbf{z}}_{f-1}, C(\mathbf{v}_f), t) - (\mathbf{z}_f - \tilde{\mathbf{z}}) \right\|_2^2$$

- **Learned Motion Matching (LMM)**：在基于片段的变体中，控制编码器网络输出的编码向量被送入 Projector 网络 $P$，直接预测下一段动画的潜在姿态序列，替代传统 Motion Matching 中的最近邻搜索。

### 4. 端到端工作流

完整的用户工作流（Fig. 3）包含三个阶段：
1. **定义控制模式**：用户以蓝图组合控制操作符，声明角色的控制接口。
2. **关联训练控制**：为训练数据的每一帧生成对应的控制变量值，使网络学习控制信号与运动之间的映射。
3. **映射运行时控制**：将游戏输入（如摇杆、目标点、风格选择）映射为控制变量，驱动实时动画生成。

这一流程将控制设计的复杂性封装在操作符的组合逻辑中，而网络训练和推理的细节对用户完全透明。控制编码器网络的内存和计算开销极小（$<0.63\text{ MB}$，$<0.025\text{ ms}$），相对于主生成网络可忽略不计（Table 3），确保了运行时的实时性。

### 控制操作符体系

Control Operators 的核心思想是将交互式角色动画的控制输入设计问题分解为一组有限的、可组合的语义操作符。每个操作符本质上是一个带有可训练参数的函数，接收一个或多个控制变量作为输入，输出一个固定维度的控制向量。这种设计将用户面向蓝图脚本的语义描述自动映射到神经网络原语上，实现了控制意图与网络结构的解耦。

#### 基础操作符

**Null 操作符**生成空输出向量，用于无控制生成或作为其他操作符的占位组件：

$$\mathrm{Null}() = []$$

**Bool 操作符**将布尔变量编码为一维控制向量：

$$\mathrm{Bool}(x \in \mathbb{B}) = [x]$$

**Encode 操作符**通过带激活函数的全连接层对输入控制向量进行进一步编码，是可训练非线性变换的基本单元：

$$\mathrm{Encode}(\mathbf{x}) = \sigma(\mathbf{W}\mathbf{x} + \mathbf{b})$$

**And 操作符**将多个控制向量沿特征维度拼接，是组合多个控制信号的基础机制：

$$\mathrm{And}(\mathbf{x}_0, \mathbf{x}_1, \ldots, \mathbf{x}_{N-1}) = \mathbf{x}_0 \parallel \mathbf{x}_1 \parallel \dots \parallel \mathbf{x}_{N-1}$$

**Or 操作符**根据索引 $i$ 从预定义的控制集合中选择对应向量，经线性变换后与选择索引的独热编码拼接。这一机制使得网络能够根据条件激活不同的控制通路：

$$\mathrm{Or}(\mathbf{x}, i) = \mathbf{W}_i \mathbf{x} + \mathbf{b}_i \parallel \mathrm{OneHot}(i, N)$$

**Set 操作符**处理变长集合类型的控制输入，使用多头自注意力机制对一组同类型控制向量进行编码，并拼接输入数量的计数编码 $\mathrm{C}$。这是框架处理可变数量控制信号（如多个路径点、多个目标）的关键机制：

$$\mathrm{Set}(\mathbf{x}_0, \mathbf{x}_1, \ldots, \mathbf{x}_{M-1}) = \mathbf{h}_0 \parallel \mathbf{h}_1 \parallel \ldots \parallel \mathbf{h}_{H-1} \parallel \mathrm{C}$$

其中每个注意力头 $\mathbf{h}_j$ 的计算为：

$$\mathbf{h}_j = \mathrm{softmax}\left(\frac{\mathbf{Q}\Lambda\mathbf{K}^T}{\sqrt{d_k}}\right) \mathbf{V}$$

$$\mathbf{q}_i = \mathbf{W}_{Q_j}\Lambda\mathbf{x}_i + \mathbf{b}_{Q_j}, \quad \mathbf{k}_i = \mathbf{W}_{K_j}\Lambda\mathbf{x}_i + \mathbf{b}_{K_j}, \quad \mathbf{v}_i = \mathbf{W}_{V_j}\Lambda\mathbf{x}_i + \mathbf{b}_{V_j}$$

其中 $\Lambda$ 为可训练的逐元素缩放参数。

#### 复合操作符

基础操作符可通过组合派生出处理复杂控制类型的复合操作符。

**Transform 操作符**将 4×4 变换矩阵分解为位置、旋转、缩放三个类型操作符，通过 And 组合编码：

$$\mathrm{Transform}(\mathbf{x} \in \mathbb{R}^{4\times 4}) = \mathrm{And}(\mathrm{Location}(\mathbf{x}^{pos}), \mathrm{Rotation}(\mathbf{x}^{rot}), \mathrm{Scale}(\mathbf{x}^{scl}))$$

**FixedArray 操作符**通过多次应用 And 编码固定长度的控制数组：

$$\mathrm{FixedArray}(\mathbf{x}) = \mathrm{And}(\mathbf{x}_{[0]}, \mathbf{x}_{[1]}, \ldots, \mathbf{x}_{[N-1]})$$

**Optional 操作符**编码可选控制信号，当条件 $c$ 为假时使用空向量，否则使用给定控制，通过 Or 操作符实现条件分支：

$$\mathrm{Optional}(\mathbf{x}, c) = \begin{cases} \mathrm{Or}([], 0), & \text{if } \neg c \\ \mathrm{Or}(\mathbf{x}, 1), & \text{if } c \end{cases}$$

**Either 操作符**实现二选一控制，根据布尔条件选择两种控制之一：

$$\mathrm{Either}(\mathbf{a}, \mathbf{b}, c) = \begin{cases} \mathrm{Or}(\mathbf{a}, 0), & \text{if } \neg c \\ \mathrm{Or}(\mathbf{b}, 1), & \text{if } c \end{cases}$$

**Array 操作符**通过将索引与元素拼接后送入 Set 操作符来编码有序数组：

$$\mathrm{Array}(\mathbf{x}) = \mathrm{Set}(\mathrm{I}(0) \parallel \mathbf{x}_{[0]}, \mathrm{I}(1) \parallel \mathbf{x}_{[1]}, \ldots, \mathrm{I}(M-1) \parallel \mathbf{x}_{[M-1]})$$

**Dictionary 操作符**将键值对拼接后输入 Set 操作符编码字典：

$$\mathrm{Dictionary}({\mathbf{k}}, {\mathbf{v}}) = \mathrm{Set}(\mathbf{k}_{[0]} \parallel \mathbf{v}_{[0]}, \mathbf{k}_{[1]} \parallel \mathbf{v}_{[1]}, \ldots, \mathbf{k}_{[M-1]} \parallel \mathbf{v}_{[M-1]})$$

#### 典型控制编码器

基于上述操作符体系，用户可通过蓝图脚本定义具体的控制编码器网络。例如，**MoveToTarget 控制编码器**将目标位置与可选的目标朝向组合，用于“移动到目标”行为：

$$\mathrm{MoveToTarget}(\mathbf{x}^{pos}, \mathbf{x}^{dir}, c) = \mathrm{And}(\mathbf{x}^{pos}, \mathrm{Optional}(\mathbf{x}^{dir}, c))$$

**TrajectoryFollow 控制编码器**将一系列未来轨迹点（位置+方向）编码为固定长度数组，用于轨迹跟随行为：

$$\mathrm{TrajectoryFollow}(\mathbf{t}^{pos}, \mathbf{t}^{dir}) = \mathrm{FixedArray}\left([\mathrm{And}(\mathrm{Location}(\mathbf{t}_{[i]}^{pos}), \mathrm{Direction}(\mathbf{t}_{[i]}^{dir})) \mid 0 \leq i < N]\right)$$

### 姿态表示与自动编码器

角色姿态由高维向量 $\mathbf{p}$ 表示，包含根关节的线速度 $\dot{\mathbf{r}}^t$ 和角速度 $\dot{\mathbf{r}}^q$、骨盆平移 $\mathbf{t}$ 及其速度 $\dot{\mathbf{t}}$、所有关节的旋转 $\mathbf{q}$ 及其角速度 $\dot{\mathbf{q}}$，以及其他附加变量 $\mathbf{o}$：

$$\mathbf{p} = \begin{bmatrix} \dot{\mathbf{r}}^t & \dot{\mathbf{r}}^q & \mathbf{t} & \dot{\mathbf{t}} & \mathbf{q} & \dot{\mathbf{q}} & \mathbf{o} \end{bmatrix}$$

为降低歧义并提升生成稳定性，框架使用自动编码器将高维姿态向量压缩到 $d_z = 128$ 维的潜在空间：

$$\mathbf{z} = \mathcal{E}(\mathbf{p}), \quad \mathbf{p} = \mathcal{D}(\mathbf{z}), \quad \mathbf{z} \in \mathbb{R}^{d_z}$$

该自动编码器经过精细的归一化处理：姿态向量的各分量先减去均值，再按变量类型分别除以平均标准差；关节旋转和角速度额外按其所有后代关节链的总长度进行缩放，以补偿误差沿关节链的累积效应。训练后的自动编码器高度精确，即使在关节链末端，重建误差通常小于 1 cm。

### 潜在流匹配生成模型

在自动编码器的潜在空间中，Flow Network $\mathcal{V}$ 以控制编码和前一帧姿态为条件，通过流匹配从噪声生成当前姿态。给定前一帧的潜在编码 $\hat{\mathbf{z}}_{f-1}$、当前帧的控制变量 $\mathbf{v}_f$ 经控制编码器网络 $C$ 编码后的向量、以及从单位高斯分布 $\mathcal{N}(\mathbf{0}, \mathbf{I})$ 采样的噪声 $\tilde{\mathbf{z}}$，定义线性插值路径：

$$\bar{\mathbf{z}} = (1 - t) \tilde{\mathbf{z}} + t \mathbf{z}_f, \quad t \in [0, 1]$$

流匹配的训练损失最小化网络预测的瞬时速度与目标速度之间的均方误差：

$$\mathcal{L}_{\theta_{\mathcal{V}}, \theta_C} = \mathbb{E}_{f, t, \tilde{\mathbf{z}}} \left\| \mathcal{V}(\bar{\mathbf{z}}, \hat{\mathbf{z}}_{f-1}, C(\mathbf{v}_f), t) - (\mathbf{z}_f - \tilde{\mathbf{z}}) \right\|_2^2$$

推理时，从 $\tilde{\mathbf{z}} \sim \mathcal{N}(\mathbf{0}, \mathbf{I})$ 出发，通过 $S$ 步数值积分逐步逼近目标姿态。为加速推理，框架支持将多步流匹配蒸馏为单步推理。蒸馏损失使单步推理的预测速度匹配 $S$ 步集成速度的平均值：

$$\mathcal{L}_{\theta_{\mathcal{V}'}} = \mathbb{E}_{f, \tilde{\mathbf{z}}} \left\| \frac{1}{S} \sum_{s=0}^{S-1} \mathcal{V}\left(\bar{\mathbf{z}}, \hat{\mathbf{z}}_{f-1}, C(\mathbf{v}_f), \frac{s}{S}\right) - \mathcal{V}'\left(\bar{\mathbf{z}}, \hat{\mathbf{z}}_{f-1}, C(\mathbf{v}_f), 0\right) \right\|_2^2$$

消融实验表明，蒸馏为单步后几乎不影响运动质量，同时推理时间从 2.890 ms 降至 0.784 ms。控制编码器网络的内存占用（<0.63 MB）和计算开销（<0.025 ms）相对主网络可忽略不计。

## 实验与关键发现

### 核心实验设置

本文在内部数据集和 100STYLE 公开数据集上评估了所提出的 Latent Auto-Regressive Flow-Matching (LAFM) 控制器。所有性能测量均在配备 NVIDIA GeForce RTX 3080 的同一台机器上进行，确保公平可比。用户研究邀请了具有不同机器学习背景的行业从业者，以排除先验知识偏差。

### 主实验结果

**运动质量与稳定性**。Table 1 报告了 LAFM 在内部数据集和 100STYLE 数据集上的运动伪影指标。在内部数据集上，LAFM 的脚滑动（Foot Sliding）仅为 0.249±0.071 cm，相比移除跳跃连接的变体（0.532±0.195 cm）降低了约 47%。脚趾穿透频率（Toe Penetration Freq）方面，LAFM 为 0.862±1.033%，而移除潜在空间的变体高达 24.471±21.590%，表明潜在空间对防止自回归生成崩溃至关重要。在 100STYLE 数据集上，LAFM 同样表现出色，脚滑动为 0.251±0.070 cm。

![[assets/figures/papers/paper_list_l22_https_doi_org_10_1145_3763319/figures/014_Table_1.jpg]]
*Table 1: Evaluations of common motion artifacts. We compare the performance of our method, Latent Auto-Regressive Flow-Matching (LAFM), to versions with the following components removed: Layer Normalization (LayerNorm), the Auto-Encoder Latent space (Latent), and Skip-Connections (Skip). This comparison is performed on our Internal Dataset, and the 100STYLE dataset. Statistics were computed from 100 randomly selected frames, each used to generate 20 auto-regressive rollouts lasting 20 seconds, starting from that initial frame. Measurements are taken without procedural adjustments applied*

**推理效率**。Table 3 展示了各网络模块的内存占用和运行时间。蒸馏后的单步 Flow-Matching 模型的每帧推理时间仅为 0.784 ms，相比 4 步集成推理的 2.890 ms 减少了约 73%，且几乎不影响运动质量。控制编码器网络 C 的内存开销极小（<0.63 MB），CPU 评估时间 <0.025 ms，相对主网络可忽略不计。

**用户研究**。Fig. 11 展示了本系统与 Motion Matching 和 Animation Blueprints 在五项指标上的 Likert 5 点量表评分分布。用户对本系统在可扩展性（scalability）上的评分显著优于两个基线，运动真实感（motion realism）与 Motion Matching 相当，验证了控制操作符在降低设计门槛的同时保持了高质量运动生成能力。

### 消融实验

**潜在空间的作用**。移除自动编码器的潜在空间（即直接在原始姿态空间进行流匹配）导致自回归生成极易崩溃。如 Fig. 14a 所示，大部分样本快速停驻于站姿，脚趾穿透频率从 0.862% 急剧升高至 24.471%（Table 1），证实潜在空间对稳定长序列生成不可或缺。

![[assets/figures/papers/paper_list_l22_https_doi_org_10_1145_3763319/figures/016_Figure_14.jpg]]
*Figure 14: (b) Without skip connections Fig. 14. Comparison of root trajectories generated from ablation experiments. (a) without using the auto-encoder’s latent space. The left plot starts with a pose in the middle of a walking motion, while the right plot starts with an idle pose. (b) without skip connections. The left plot shows a circling skating motion, while the right plot illustrates gliding with a static pose*

**跳跃连接的作用**。移除跳跃连接（skip connections）使生成结果更加嘈杂和不稳定，易发生漂移或数值爆炸（Fig. 14b）。脚滑动从 0.249 cm 升至 0.532 cm，表明跳跃连接在保持运动平滑性和稳定性方面起关键作用。

**层归一化的作用**。移除 Layer Normalization 仅轻微降低运动质量和稳定性，并非模型运行的必要组件，说明该架构对此正则化手段的依赖度较低。

**流匹配集成步数**。Table 2 展示了不同集成步数 S 对运动质量的影响。运动质量在 S=4 到 S=8 时趋于饱和，4 步即可接近最优，因此 4 步集成在质量与效率间取得良好平衡。

![[assets/figures/papers/paper_list_l22_https_doi_org_10_1145_3763319/figures/015_Table_2.jpg]]
*Table 2: Motion quality of the Latent Auto-Regressive Flow-Matching model saturates at 4 to 8 integration steps (??)*

**蒸馏加速**。将 4 步 Flow Network 蒸馏为单步版本后，每帧推理时间从 2.890 ms 降至 0.784 ms（Table 3），同时运动质量几乎无损，为实时应用提供了高效推理方案。

### 定性分析

**控制编码空间的语义结构化**。Fig. 12 的可视化实验表明，控制编码器网络能够学习将语义相似的控制意图映射到相近的编码。例如，向左转的轨迹跟随与置于左侧的移动到目标，在 8 维控制编码空间中呈现出高度相似的表示，验证了操作符组合自动产生的编码具有语义一致性。

![[assets/figures/papers/paper_list_l22_https_doi_org_10_1145_3763319/figures/012_Figure_12.jpg]]
*Figure 12: Experiment showing that Control Operators can learn to map similar controls to the same encoding. Here, the 8-dimensional control encoding is visualized using the vertical positions of the white balls. Left: Move To Target. Right: Trajectory Following. From top to bottom: Turning Right, Turning Left, and Walking Forward*

**跨任务风格泛化**。Fig. 13 展示了跨任务泛化能力。模型仅在轨迹跟随任务上训练了 Mummy 风格的运动，却能自动将该风格泛化到移动到目标任务中。这得益于控制编码器将不同控制模式映射到共享的语义空间，使下游生成网络能够复用已学习的风格表征。

![[assets/figures/papers/paper_list_l22_https_doi_org_10_1145_3763319/figures/013_Figure_13.jpg]]
*Figure 13: Experiment showing cross-task generalization. Even though the model was only trained on the Mummy style of locomotion for the Trajectory Following task (Right), it is able to generalize and apply this style to the Move To Target task (Left)*

**多行为控制**。Fig. 9 和 Fig. 10 分别展示了运动任务和交互任务的生成结果，包括轨迹跟随、路径跟随、风格化移动、坐下、站起、跳跃至目标、拾取物体等。这些行为均通过组合有限的操作符实现，无需为每种行为设计专用网络架构。

### 失败模式与局限性

**训练时间瓶颈**。最复杂的控制器需约 20 小时训练，成为快速设计迭代的主要瓶颈。

**静止状态残留噪声**。流匹配模型在角色静止时可能产生微小的残留抖动，影响静止姿态的视觉稳定性。

**分布外输入的脆弱性**。当运行时控制输入超出训练分布时，模型可能产生不稳定运动或卡住，缺乏对异常情况的鲁棒回退机制。

**动力学特性的间接控制**。系统缺乏对运动加速度、响应时间等动力学特性的直接精确控制，设计师仍需依赖经验调整控制参数。

**操作符学习成本**。尽管框架大幅降低了控制设计门槛，用户仍需理解基本的操作符语义（如 And, Or, Optional 等），存在一定的学习曲线。

## 定位与知识库关联

### 1. 问题定位与核心瓶颈

在交互式角色动画领域，传统控制方法通常要求开发者针对每一种控制模式（如轨迹跟随、目标移动、风格切换）手动设计特征工程和专用网络架构。这种“控制-网络”深度耦合的范式导致三个核心瓶颈：其一，控制逻辑的修改必然触发网络结构的调整和重新训练，迭代成本极高；其二，非技术用户（如游戏设计师）难以理解底层网络机制，无法自主扩展或组合多种行为；其三，不同控制模式之间缺乏统一的编码框架，跨任务泛化能力薄弱。

Control Operators 的核心洞察在于：将控制问题分解为一组语义明确、可组合的操作符原语（如 Null、Bool、Encode、And、Or、Set、Array 等），并自动将这些操作符映射到对应的可训练神经网络模块。这一设计实现了控制意图与网络架构的解耦——用户通过蓝图脚本组合操作符定义控制模式，网络结构随之自动生成，无需手动介入。

### 2. 与基线方法的关系

#### 2.1 Motion Matching（Büttner & Clavet 2015; Clavet 2016）

Motion Matching 是当前游戏工业中广泛采用的动画控制系统，其核心是通过最近邻搜索在动画数据库中匹配当前姿态与控制信号。该方法在运动真实感上表现优异，但存在两个结构性局限：一是搜索质量和数据库规模高度依赖于特征工程的手工设计；二是系统不具备生成能力，无法产生训练数据中未出现的运动模式。

Control Operators 在控制编码层面继承了 Motion Matching 的“控制信号驱动动画选择”的思想，但将其从离散搜索范式迁移至连续生成范式。在用户研究中（Fig. 11），本文系统在运动真实感指标上与 Motion Matching 评分相当，而在可扩展性上显著优于后者——这是因为 Control Operators 通过流匹配生成模型可以产生数据库之外的运动变化，且控制模式的增删无需重新设计特征工程。

#### 2.2 Animation Blueprints（Unreal 2022a）

Animation Blueprints 是 Unreal Engine 中的可视化动画逻辑系统，通过状态机或流程图控制动画的混合与切换。其优势在于设计师熟悉的图形化工作流，但本质上仍是对预定义动画片段的调度，缺乏对运动本身的生成能力。当行为复杂度上升时，状态机规模迅速膨胀，维护和扩展成本急剧增加。

Control Operators 在用户交互层面借鉴了蓝图式组合的设计哲学——用户同样通过可视化节点图描述控制逻辑——但将底层执行机制从动画片段调度替换为神经网络生成。这使得系统能够处理连续控制空间中的平滑过渡和风格泛化，而无需预先枚举所有可能的状态转换。

#### 2.3 Hand-crafted Control Vector

在多数基于学习的角色控制器中，控制信号以手工设计的特征向量形式输入网络。例如，轨迹跟随任务通常需要计算未来若干时间步的位置和方向，拼接为固定长度的向量；不同控制类型（如目标位置 vs. 轨迹点）需要设计不同的编码方案，缺失值需要特殊填充或截断。

Control Operators 通过 Optional、Either、Set、Array 等操作符统一处理了这些编码模式。以变长路径点为例，传统方法需要截断或填充至固定长度，而 Array 操作符通过多头自注意力机制自然处理变长输入，同时保留元素间的顺序关系。消融实验（Table 1）表明，这种自动编码方案在脚部滑动、脚趾穿透等运动伪影指标上显著优于手工设计的替代方案。

### 3. 方法适用边界

**适合的场景：**
- 需要支持多种控制模式（轨迹跟随、目标移动、风格选择、交互动作）且控制模式可能频繁增删的项目；
- 非技术用户（游戏设计师、动画师）需要直接参与控制逻辑设计的工作流；
- 对运动多样性有较高要求，希望生成训练数据中未出现的运动变化。

**不适合的场景：**
- 对训练时间敏感、需要快速迭代的项目——最复杂的控制器训练约需 20 小时；
- 对运动加速度、响应时间等动力学特性有精确物理约束的场景——当前系统缺乏对这些参数的直接控制；
- 控制输入可能大幅超出训练分布的场景——模型可能产生不稳定运动或卡住。

### 4. 已知局限

1. **训练时间瓶颈**：最复杂的控制器（多行为、多风格）训练约需 20 小时，成为设计迭代的主要障碍。这一局限源于流匹配模型的自回归训练和潜在空间自动编码器的联合优化。

2. **静止状态残留噪声**：流匹配模型在角色长时间静止时可能产生微小的残余运动噪声，影响动画的静止稳定性。

3. **分布外脆性**：当运行时控制输入显著偏离训练数据分布时，模型可能生成不稳定运动或陷入退行性姿态（如停驻于站姿）。这一现象在消融实验中移除潜在空间时尤为明显（Fig. 14a），但完整模型仍存在一定风险。

4. **动力学间接控制**：系统缺乏对运动加速度、响应速度、步态频率等动力学特性的直接调节接口。设计师无法直观地指定“角色应更快响应转向指令”或“步态应更沉重”，仍需依赖训练数据的隐式覆盖。

5. **操作符学习成本**：尽管框架大幅降低了控制设计的门槛，用户仍需理解基本操作符的语义（如 And 拼接 vs. Set 注意力编码的区别），具有一定的学习曲线。

### 5. 开放问题与后续方向

1. **加速训练与迭代**：能否通过控制编码器网络的轻量化重训练（复用冻结的流网络）来支持控制模式的快速增删，从而将迭代时间从小时级降至分钟级？

2. **精细化运动调节**：如何引入可解释的参数化机制，使设计师能够直观地调整运动加速度、响应速度和步态风格，而无需修改训练数据？

3. **空间感知扩展**：当前操作符主要处理时间序列和离散控制信号。能否引入卷积操作符处理高度图等空间信息，以支持地形自适应运动和更丰富的环境交互？

4. **运行时安全介入**：在已部署的控制器中，是否能在异常情况下（如检测到不稳定运动）动态回退到安全策略，而无需重新训练整个网络？

5. **跨任务风格泛化的边界**：实验表明，仅在轨迹跟随任务上训练的 Mummy 风格可泛化到移动到目标任务（Fig. 13），但这种泛化的边界条件尚不明确——当任务差异增大（如从移动任务泛化到坐下交互）时，风格迁移是否仍然有效？

## 原文 PDF

![[paperPDFs/TOG_2025/Control_Operators_for_Interactive_Character_Animation.pdf]]
