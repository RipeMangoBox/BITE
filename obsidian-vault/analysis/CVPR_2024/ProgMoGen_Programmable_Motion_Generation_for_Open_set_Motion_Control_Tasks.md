---
title: ProgMoGen Programmable Motion Generation for Open set Motion Control Tasks
type: paper
paper_level: A
venue: CVPR
year: 2024
pdf_ref: paperPDFs/CVPR_2024/ProgMoGen_Programmable_Motion_Generation_for_Open_set_Motion_Control_Tasks.pdf
project_link: null
code_link: null
aliases:
- PMGP
- PPMGOSMCT
tags:
- CVPR_2024
- topic/vision_multimodal_applications
- topic/generative_models_diffusion
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: 将任务转化为原子约束的可微误差函数，并利用冻结的预训练运动生成模型，通过优化其潜在代码来最小化误差，从而在继承运动先验的同时满足任意组合的约束。
primary_logic: 复杂的开放集运动控制可以通过三个关键观察统一解决：(1) 任务可分解为原子约束的组合；(2) 几乎所有约束都能量化为可微误差；(3) 误差具有可加性。因此，只需编程一个误差函数，并以此引导预训练生成模型的潜在优化，就能在不重新训练的情况下生成满足定制约束的高质量运动。
claims:
- 在已知约束任务 (HSI-1) 上，我们的方法在 Foot Skate (0.075)、Max Acc. (0.094) 和 C.Err. (0.012) 之间取得最佳平衡，而所有基线在至少一个指标上失败。
- 对于多个未见过的任务 (HSI-2, HSI-3, GEO-1, HOI-1)，我们的方法实现了运动质量与约束误差的良好平衡，而修复类方法 (MDM Edit, PriorMDM) 无法原生处理这些任务。
- 在“在两墙之间行走”等全新约束下，我们的方法能生成合理的新行为（如收拢手臂和肩膀），展示了模型涌现新技能的能力。
- 我们的方法在维持低 Foot Skate 和 Max Acc 的同时，能有效保持骨骼长度，而基于修复的方法 (MDM Edit) 骨骼长度错误率高达 52.5%。
---

# ProgMoGen Programmable Motion Generation for Open set Motion Control Tasks

> [!tip] 核心洞察
> 复杂的开放集运动控制可以通过三个关键观察统一解决：(1) 任务可分解为原子约束的组合；(2) 几乎所有约束都能量化为可微误差；(3) 误差具有可加性。因此，只需编程一个误差函数，并以此引导预训练生成模型的潜在优化，就能在不重新训练的情况下生成满足定制约束的高质量运动。

| 字段 | 内容 |
|------|------|
| 中文题名 | 面向开放集运动控制任务的可编程运动生成 |
| 英文题名 | ProgMoGen Programmable Motion Generation for Open set Motion Control Tasks |
| 会议/期刊 | CVPR 2024 |
| Links |  |
| Topic | #topic/vision_multimodal_applications #topic/generative_models_diffusion #topic/vision_multimodal_applications/image_and_video_generation |
| Method | Programmable Motion Generation (ProgMoGen) |
| Dataset | Task HSI-1: 头部高度约束, Task HSI-2: 避开头顶障碍物, Task GEO-1: 手触墙壁 |

> [!tip] 效果简介
> - Task HSI-1: 头部高度约束 (已知约束) 上，Foot Skate ↓ 0.075 vs 0.093 (IK) (-0.018)。
> - Task HSI-1 上，Max Acc. ↓ 0.094 vs 0.414 (IK) (-0.320)；C.Err. ↓ 0.012 vs 0.012 (IK) (0.000)。
> - Task HSI-2: 避开头顶障碍物 (未见任务) 上，Foot Skate ↓ 0.189 vs 0.132 (IK) (+0.057)。

## 概要

现有运动控制方法将每个任务视为一个封闭集问题，需要为特定约束组合单独收集配对训练数据并设计专用网络，缺乏可组合性、可扩展性和可定制性。当面对开放世界中任意组合的约束时——例如“在两墙之间行走并保持头部高度”——这些方法无法原生处理。本文提出 **ProgMoGen**（Programmable Motion Generation），将开放集运动控制统一为一个可编程框架。其核心洞察在于：(1) 复杂任务可分解为若干原子约束的组合；(2) 几乎所有约束都能量化为可微误差；(3) 误差具有可加性。因此，只需将任务编程为一个误差函数，并以此引导冻结的预训练运动生成模型优化其潜在编码，即可在不重新训练的情况下生成既满足定制约束又继承运动先验的高质量运动。

在已知约束任务（HSI-1，头部高度约束）上，ProgMoGen 在足部滑动（0.075）、最大加速度（0.094）和约束误差（0.012）之间取得最佳平衡，而所有基线方法（IK、IK+Reg.、MDM Edit、PriorMDM）在至少一个指标上失败。在多个未见过的任务（HSI-2 避开头顶障碍物、HSI-3 方形区域内行走、GEO-1 手触墙壁、HOI-1 移动物体）上，该方法同样实现了运动质量与约束误差的良好平衡，而基于修复的方法（MDM Edit、PriorMDM）无法原生处理这些不等式或几何约束。此外，该方法在“在两墙之间行走”等全新约束下展示了涌现新技能的能力（如收拢手臂和肩膀），并在骨骼长度保持上显著优于修复类方法（骨骼长度错误率 5.1% vs 52.5%）。



### 运动控制任务的封闭集困境

人类运动控制是计算机视觉与图形学中的核心问题，其目标是在给定约束条件下生成符合物理规律且语义合理的运动序列。然而，现有方法几乎无一例外地将运动控制视为一组**封闭集任务**：每个任务（如特定关节到达指定位置、避开障碍物、与物体交互等）需要单独收集配对的训练数据、设计专用网络架构并独立训练。这种范式存在三个根本性缺陷：

1. **可组合性缺失**：现实世界中的运动控制往往是多约束的组合（例如“边走路边举着球并避开头顶障碍物”），但封闭集方法无法将已学到的单一约束能力组合起来应对新场景。
2. **可扩展性受限**：每新增一种约束类型，就需要重新采集数据、设计网络、训练模型，成本随任务数量线性增长。
3. **可定制性不足**：用户无法按需定义全新约束（如“在两墙之间行走”），因为模型从未见过此类任务。

### 现有方法的尝试与局限

针对上述困境，学界提出了几类解决方案，但各有致命短板：

- **逆运动学（IK）** 直接优化关节点位置以满足约束，但由于缺乏运动先验，生成的运动往往抖动剧烈（Max Acc. 高达 0.414，见 Table 1），甚至产生解剖学上无效的姿态。
- **IK + 正则化（IK+Reg.）** 在 IK 基础上增加帧间一致性正则项 $L_{reg} = | x_{[i+1]} - x_{[i]} |$ 以缓解抖动，但会导致过度平滑和严重滑步（Foot Skate 恶化），丢失运动细节。
- **基于扩散模型的修复方法（MDM Edit）** 通过固定部分轨迹进行修补，仅支持精确轨迹控制，无法处理不等式约束（如“头部高度 < 0.8m”）和几何约束（如“手触碰墙壁”）。更严重的是，从局部关节位置恢复时，骨骼长度错误率高达 52.5%（Table 3），导致生成的运动物理上不成立。
- **PriorMDM** 在 MDM Edit 基础上微调模型参数以捕捉被控关节与其余身体的关系，但本质上仍受限于修复范式，无法原生处理未见约束类型。

### 核心洞察与动机

本文观察到，复杂的开放集运动控制任务可以统一解决的三个关键事实：

1. **任务可分解**：任意复杂的运动控制任务都可以分解为若干原子约束的组合。例如，“边走路边抱球”可分解为“双手接触球面”和“球体跟随身体移动”两个原子约束。
2. **约束可量化**：几乎所有约束都能通过可微误差函数来度量。例如，“双手接触”可用双手间距离作为误差，“避开障碍物”可用关节到障碍物的有符号距离来衡量。
3. **误差可加性**：不同约束的误差函数具有天然的可加性，使得组合约束的优化成为可能。

基于上述洞察，本文提出**可编程运动生成（ProgMoGen）**，将开放集运动控制转化为一个统一的优化问题：只需将任务编程为一个误差函数，然后通过优化冻结的预训练运动生成模型的潜在编码来最小化该误差，即可在不重新训练的情况下生成满足定制约束的高质量运动。这一范式从根本上摆脱了对任务专用数据和网络设计的依赖，实现了运动控制的开放集能力。



## 核心方法与创新机理

ProgMoGen 的核心创新在于将运动控制从**封闭集任务范式**转变为**开放集可编程范式**。现有方法（如 IK、MDM Edit、PriorMDM）将运动控制视为一组孤立的封闭集任务——每个任务需要专门的配对训练数据和网络设计，无法处理开放世界中任意组合的约束。ProgMoGen 则通过以下三个关键机制打破了这一限制：

### 1. 任务范式转变：从封闭集到开放集

传统方法为每种控制任务单独设计数据集和网络（如头部高度约束、手部轨迹修复等），缺乏可组合性和可扩展性。ProgMoGen 将任意复杂的运动控制任务统一视为**原子约束的组合**，只需编程一个误差函数即可求解，无需任务专用训练或数据（Figure 1, Section 1）。这一范式的核心洞察在于：

- 复杂任务可分解为原子约束的组合（如“持球行走”可分解为手部接触球和行走两个约束）；
- 几乎所有约束都可量化为可微误差（如用距离度量“双手接触”约束）；
- 误差具有可加性，因此任意组合的约束可统一为单个可微误差函数。

### 2. 约束实现与优化方式转变

**Baseline 的局限**：IK 直接优化关节位置，缺乏运动先验，产生不连贯或过度平滑的运动（Max Acc. 高达 0.414 vs ProgMoGen 的 0.094，Table 1）；MDM Edit 通过扩散修复强制轨迹，仅支持精确轨迹控制，且骨骼长度错误率高达 52.5%（Table 3）；PriorMDM 虽能捕捉被控关节与全身的关系，但同样无法原生处理不等式约束和几何约束。

**ProgMoGen 的方案**：使用**冻结的预训练运动扩散模型**（MDM），通过优化其潜在编码 $z$ 来最小化由原子约束构成的误差函数：
$$\min_{z} F(G_{\theta}(z, \mathcal{C}), p)$$
这使生成的运动既继承运动先验（保证连贯性和物理合理性），又能满足任意组合的约束。优化过程无需微调生成模型，完全通过潜在空间搜索实现约束满足。

### 3. 约束类型支持的扩展

**Baseline 的局限**：IK 和 MDM Edit 仅支持有限类型的约束（精确轨迹或关键帧位置），难以处理不等式约束（如“头部高度低于 0.8m”）、几何约束（如“在两墙之间行走”）或物理约束（如质心平衡）。

**ProgMoGen 的方案**：提供**原子约束库**和**可编程逻辑框架**（Figure 3），涵盖六类原子约束：
- 绝对位置约束
- 高阶动态约束（速度、加速度）
- 几何约束（平面、球形区域等）
- 相对距离约束
- 方向约束
- 关键帧约束

配合重新设计的逻辑操作（`>`, `<`, `AND`, `OR`, `NOT`），用户或 LLM 可将任务描述组合成误差函数。例如，HSI-3 任务（在方形区域内行走）的约束误差可表示为：
$$\mathrm{Err}(\boldsymbol{x}) = \frac{1}{4 N N_j} \sum_{t=1}^{N} \sum_{j=1}^{N_j} \sum_{dim \in \{x,z\}} \max(-x_{j,t,dim}^{pos} - 1, 0) + \max(x_{j,t,dim}^{pos} - 1, 0)$$

这种可编程性使得 ProgMoGen 能处理全新约束组合。例如在“在两墙之间行走”任务中，模型涌现出收拢手臂和肩膀的新行为（Section 5.5），展示了预训练运动先验与约束优化结合后产生新技能的能力。



ProgMoGen 将开放集运动控制任务统一为一个**“编程—优化”**范式，其核心流程由三个关键模块串联而成：**原子约束库**、**运动编程框架**和**潜在噪声优化**。整体 pipeline 如 Figure 2 所示。

![[assets/figures/papers/paper_list_l1853_ProgMoGen_Programmable_Motion_Generation_for_Open_set_Motion_Control_Tas/figures/002_Figure_2.jpg]]
*Figure 2: Overview of Programmable Motion Generation. Given an arbitrary task, we formulate it as a combination of motion constraints. Under our programming framework, by combining modules from our atomic constraint library, it is easy to program the error function to solve complex tasks just like building blocks. The programming also supports to be performed automatically by LLMs via simply providing textual descriptions of the task. Finally, the latent code z of a pre-trained motion generation network is optimized to minimize the error function, thus producing motions in high quality as well as satisfying the constraints. The prompt is optional if we use text-to-motion network as the pre-trained ge...*

### 输入输出规范

系统的输入是一个运动控制任务的描述（可由用户直接提供，或通过 LLM 自动翻译为约束组合），输出是一段满足所有约束且保持高质量运动先验的人体运动序列。具体而言：

- **输入**：任务参数 $p$（如目标位置、障碍物几何体、接触条件等），以及可选的生成条件 $\mathcal{C}$（如文本描述）。
- **输出**：运动序列 $\boldsymbol{x} = G_\theta(z, \mathcal{C})$，其中 $G_\theta$ 是冻结的预训练运动生成模型，$z$ 是待优化的潜在编码。

### 模块关系与数据流

三个模块形成一条从“任务定义”到“运动生成”的完整链路：

1. **原子约束库 (Atomic Constraint Library)**  
   提供一组可微分的原子约束作为基础构建块，包括绝对位置约束、高阶动态约束（速度/加速度）、几何约束、相对距离约束、方向约束和关键帧约束等。每个原子约束将运动序列映射为一个标量误差，误差越小表示约束满足越好。

2. **运动编程框架 (Motion Programming Framework)**  
   定义了一套编程规则和重新设计的逻辑操作（`>`、`<`、`AND`、`OR`、`NOT`），允许用户或 LLM 将任意复杂的控制任务分解为原子约束的组合，并编程为一个统一的误差函数 $F$。例如，“手持一个直径为 0.4 米的球行走”这一任务被分解为双手接触球体的相对距离约束（Figure 3）。该框架使任务定义从“收集配对数据和设计专用网络”转变为“编写误差函数”，实现了可组合性和可定制性。

3. **潜在噪声优化 (Latent Noise Optimization)**  
   在冻结的预训练运动扩散模型（MDM）上，通过最小化编程的误差函数来优化潜在编码 $z$：
   $$\min_{z} F(G_{\theta}(z, \mathcal{C}), p)$$
   这一设计的关键在于：优化发生在生成模型的潜在空间而非运动参数空间，因此生成的运动天然继承预训练模型中的运动先验——表现为物理合理性、时序连贯性和骨骼长度保持——同时又能灵活满足任意组合的约束。

### 关键设计决策

- **冻结生成模型**：$G_\theta$ 在优化过程中保持冻结，确保运动先验不被破坏。这与基于修复的方法（如 MDM Edit）形成对比，后者在修补局部轨迹时可能破坏骨骼长度（骨骼长度错误率高达 52.5%，而 ProgMoGen 仅为 5.1%，Table 3）。
- **约束松弛策略**：对于水平位置相关的约束，引入约束松弛机制可显著降低约束误差（GEO-1 任务上从 0.118 降至 0.023，Table A1），以轻微的足部滑动增加换取更好的约束满足。
- **初始点搜索**：通过随机采样多个初始潜在编码并选择最优者，可进一步降低约束误差（HSI-1 任务上从 0.012 降至 0.002，Table A2），以轻微牺牲多样性为代价。

### 与传统方法的范式对比

| 维度 | 传统封闭集方法 | ProgMoGen |
|------|---------------|-----------|
| 任务定义 | 为每种控制任务单独设计数据集和网络 | 编程误差函数，无需任务专用训练 |
| 约束支持 | 有限类型（如精确轨迹） | 原子约束库 + 逻辑操作，支持任意组合 |
| 优化空间 | 运动参数空间 (IK) 或修复轨迹 (MDM Edit) | 冻结生成模型的潜在空间 |
| 运动先验 | 无 (IK) 或局部 (PriorMDM) | 全局运动先验，通过预训练模型继承 |

这种“编程—优化”范式使 ProgMoGen 能够在不重新训练的情况下，处理从已知约束（如头部高度控制）到全新约束（如“在两墙之间行走”需要收拢手臂和肩膀的涌现行为）的广泛任务。

### 补充图表

![[assets/figures/papers/paper_list_l1853_ProgMoGen_Programmable_Motion_Generation_for_Open_set_Motion_Control_Tas/figures/001_Figure_1.jpg]]
*Figure 1: We introduce Programmable Motion Generation as a solution for open-set human motion control. Unlike previous works that treat a finite set of motion constraints as individual tasks, we attempt to solve vast and novel tasks in a unified framework. Through Programmable Motion Generation, an arbitrary controlled motion generation task is effectively solved by simply programming an error function rather than collecting training data and designing networks. The programming is also able to be implemented automatically*



### 问题形式化：将运动控制转化为潜在优化

ProgMoGen 的核心思想是将任意运动控制任务统一建模为在冻结的预训练生成模型上的潜在代码优化问题。给定一个预训练的运动生成模型 $G_\theta$（如 MDM），其接受潜在噪声 $z$ 和可选条件 $\mathcal{C}$（如文本描述），生成运动序列 $\boldsymbol{x} = G_\theta(z, \mathcal{C})$。对于任意控制任务，用户只需定义一个误差函数 $F$，该函数量化生成运动 $\boldsymbol{x}$ 与任务参数 $p$ 所定义的约束之间的违反程度。运动控制问题即转化为：

$$\min_{z} F(G_{\theta}(z, \mathcal{C}), p)$$

其中 $F$ 由原子约束组合而成，$p$ 为任务参数（如目标位置、障碍物几何等）。通过优化潜在变量 $z$ 而非直接优化运动参数，该方法在满足约束的同时继承了预训练模型中的运动先验，从而生成自然、连贯的人体运动。

### 原子约束库：可微分约束的积木式组合

为解决开放集任务的多样性和可组合性，ProgMoGen 提供了一套原子约束库，将常见运动约束封装为可微分的误差函数模块。每个原子约束接受运动序列 $\boldsymbol{x}$ 和参数 $p$，输出标量误差。库中包含以下核心约束类型：

- **绝对位置约束**：约束特定关节在特定帧的 3D 位置，误差为预测位置与目标位置的 L2 距离。
- **高阶动态约束**：约束关节的速度或加速度，用于实现匀速运动、限制最大加速度等任务。
- **几何约束**：约束关节相对于几何体（如平面、球体、立方体）的空间关系，例如“手触碰墙壁”或“头部避开障碍物”。
- **相对距离约束**：约束两个关节之间的距离，如“双手接触”。
- **方向约束**：约束骨骼的方向向量，如“前臂保持水平”。
- **关键帧约束**：约束特定帧的完整姿态或部分关节位置。

这些原子约束构成了构建复杂任务的“积木块”。例如，“手持球行走”任务可分解为双手与球心的相对距离约束和球的位置约束的组合。

### 运动编程框架：误差函数的组合逻辑

为支持任意约束的逻辑组合，ProgMoGen 设计了运动编程框架，重新定义了适用于运动控制的逻辑操作：

- **大于 (>) 和小于 (<)**：通过 margin-based 实现，例如 $\text{Err} = \max(\text{margin} - E, 0)$ 实现“关节高度大于阈值”的约束，其中 $E$ 为原子约束误差。
- **逻辑与 (AND)**：通过误差求和实现，即 $F = \sum_i E_i$。
- **逻辑或 (OR)**：通过误差取最小值实现，即 $F = \min_i E_i$。
- **逻辑非 (NOT)**：通过误差取负实现。

该框架预定义了输入（运动序列 $\boldsymbol{x}$、任务参数 $p$）和输出（标量误差）的规范，用户或 LLM 可像编写程序一样将原子约束组合成误差函数。例如，HSI-3 任务“在方形区域内行走”的约束误差定义为：

$$\mathrm{Err}(\boldsymbol{x}) = \frac{1}{4 N N_j} \sum_{t=1}^{N} \sum_{j=1}^{N_j} \sum_{\text{dim} \in \{x,z\}} \max(-x_{j,t,\text{dim}}^{\text{pos}} - 1, 0) + \max(x_{j,t,\text{dim}}^{\text{pos}} - 1, 0)$$

该公式对所有帧、所有关节在 $x$ 轴和 $z$ 轴上超出区间 $[-1, 1]$ 的部分做平均，得到步行区域约束的平均违反量。

### 潜在噪声优化：继承运动先验的约束满足

优化过程的核心是冻结预训练运动扩散模型（MDM），仅优化其输入的潜在噪声 $z$。具体而言，使用 DDIM 采样器以 100 步去噪生成运动序列，通过反向传播将误差函数 $F$ 的梯度传递至 $z$，使用梯度下降迭代更新 $z$。这一设计的关键优势在于：

1. **运动先验继承**：冻结的生成模型保证了生成运动始终位于自然人体运动的流形上，避免了直接优化关节位置导致的无效姿态和帧间不连贯。
2. **骨骼长度保持**：由于生成模型输出的运动本身满足人体骨骼约束，优化过程不会破坏骨骼长度。实验表明，ProgMoGen 的骨骼长度错误率仅为 0.051，而基于修复的 MDM Edit 高达 0.525。
3. **约束松弛策略**：对于水平位置等难以精确满足的约束，引入约束松弛机制——在优化初期放宽约束边界，随后逐步收紧，有效降低了约束误差（在 GEO-1 任务上从 0.118 降至 0.023）。
4. **初始点搜索**：随机采样多个初始 $z$ 并选择误差最小者进行优化，可在牺牲少量多样性的情况下显著提升约束满足精度（HSI-1 约束误差从 0.012 降至 0.002）。

### 方法谱系与知识库定位

ProgMoGen 的方法论定位可通过与现有范式的对比清晰呈现：

| 方法维度 | 传统封闭集方法 | ProgMoGen (本文) |
|---------|---------------|-----------------|
| **任务范式** | 为每种控制任务单独设计数据集和网络 | 将任务分解为原子约束并编程为误差函数，统一解决任意任务 |
| **约束实现** | 直接优化运动参数 (IK) 或通过修复强制轨迹 (MDM Edit) | 优化冻结生成模型的潜在编码，继承运动先验 |
| **约束类型** | 仅支持有限类型（如精确轨迹），难以处理不等式和几何约束 | 提供原子约束库和逻辑操作，可编程处理广泛约束组合 |

**IK 方法**直接优化关节点位置以满足约束，但缺乏运动先验，导致帧间不连贯和无效姿态。**IK+Reg.** 通过添加帧间一致性正则化 $L_{reg} = | x_{[i+1]} - x_{[i]} |$ 缓解抖动，但会引入过度平滑和大量脚步滑动。**MDM Edit** 基于扩散模型的轨迹修复方法，仅支持精确轨迹控制，且修复过程会破坏骨骼长度。**PriorMDM** 在 MDM Edit 基础上微调模型参数，但本质上仍受限于修复范式，无法原生处理不等式约束和几何约束。

ProgMoGen 通过“编程误差函数 + 潜在优化”的范式，从根本上突破了封闭集限制，实现了对开放世界中任意组合约束的统一处理。

### 补充图表

![[assets/figures/papers/paper_list_l1853_ProgMoGen_Programmable_Motion_Generation_for_Open_set_Motion_Control_Tas/figures/003_Figure_3.jpg]]
*Figure 3: The programming framework that pre-defines the input, output, atomic constraints and the redesigned logical operations as building blocks for motion programming. The example code corresponds to the task of “holding a ball”*



## 实验与关键发现

### 核心实验设计

实验围绕一个核心主张展开：**ProgMoGen 能在不针对任务重新训练的前提下，在运动质量与约束满足之间取得平衡，而所有基线方法总会在至少一个关键指标上失败。** 为验证这一点，作者设计了两种互补的评估场景：

1.  **已知约束任务 (HSI-1)**：从 HumanML3D 测试集中采样头部高度约束（施加于首、中、末三帧），此时约束来自模型见过的分布，可同时评估运动语义保持（FID、Diversity、R-precision）与物理质量。
2.  **未见约束任务 (HSI-2, HSI-3, GEO-1, HOI-1)**：构造训练中未出现的开放集约束（如避开头顶障碍物、在方形区域内行走、手触墙壁、持球），仅评估物理质量与约束误差，因为语义指标在分布外无参考意义。

基线方法包括：**IK**（直接优化关节位置）、**IK+Reg.**（增加帧间平滑正则项 $| x_{[i+1]} - x_{[i]} |$）、**MDM Edit**（基于扩散修复）和 **PriorMDM**（MDM Edit 的微调版本）。对于无法原生处理不等式/几何约束的修复类方法，作者采用特设技巧（如将约束投影为手部轨迹）使其适配，并保证所有方法在相同 DDIM 预训练模型（100 步）及优化策略（约束松弛、初始点搜索）下公平比较。

### 已知约束任务：运动质量与物理合理性的唯一胜出者

在 HSI-1 任务上（Table 1），所有基线方法均因某个指标失败而整体不可用：
- **IK** 的最大加速度高达 0.414，表明帧间严重不连贯，且脚滑动（Foot Skate）为 0.093；
- **IK+Reg.** 通过平滑正则将加速度降至可接受水平，但脚滑动飙升至 0.281，且约束误差（C.Err.）从 0.012 升至 0.029——平滑与约束满足出现冲突；
- **MDM Edit** 和 **PriorMDM** 在约束误差上尚可（0.017/0.016），但成功率（Unsucc. Rate）分别为 0.202 和 0.179，意味着大量生成未能满足约束。

![[assets/figures/papers/paper_list_l1853_ProgMoGen_Programmable_Motion_Generation_for_Open_set_Motion_Control_Tas/figures/005_Table_1.jpg]]
*Table 1: Comparison with other methods with constraints sampled from groundtruth HumanML3D test set. The constraints are imposed on the first, central and last frames. MDM (Unconstrained) serves as a numerical reference. The failure of any single indicator (marked in red) means the failure of the entire task. Baseline methods always fail in certain metrics while ours performs generally well on all metrics*

**ProgMoGen 是唯一在所有指标上同时达标的方法**：Foot Skate 0.075、Max Acc. 0.094、C.Err. 0.012，成功率 0.088。这得益于冻结的预训练生成模型提供的运动先验——它天然保证帧间连贯性和骨骼长度一致性，而优化过程仅需在潜在空间中搜索满足约束的解，不会破坏底层运动流形。

### 未见约束任务：泛化到开放世界的平衡能力

在四个未见任务上（Table 2），ProgMoGen 展示了更强的泛化鲁棒性：
- **HSI-2（避开头顶障碍物）**：IK 的最大加速度飙至 1.919，运动严重抖动；ProgMoGen 将 Max Acc. 控制在 0.150，但约束误差（0.022）略高于 IK（0.016），Foot Skate（0.189）也逊于 IK（0.132）。这是一个典型的**质量-约束权衡**案例：IK 可以精确满足约束但产生不连贯运动，ProgMoGen 以轻微牺牲约束精度换取大幅提升的物理合理性。
- **GEO-1（手触墙壁）**：ProgMoGen 在 Foot Skate（0.110 vs 0.147）和 Max Acc.（0.104 vs 0.187）上均优于 IK，约束误差（0.023）虽高于 IK（0.010），但仍在可接受范围。这验证了运动先验在几何约束任务中的价值——IK 为满足手部位置可能产生不合理的全身姿态，而生成模型能协调全身运动。
- **HSI-3（方形区域内行走）** 和 **HOI-1（持球）**：修复类方法（MDM Edit、PriorMDM）无法原生处理这些任务，即使使用特设技巧适配，仍因无法保持骨骼长度（详见下文）或约束满足失败而整体不可用。

### 骨骼长度保持：修复方法的根本缺陷

Table 3 揭示了基于修复的方法在结构保持上的致命弱点。在头部高度约束任务中，MDM Edit 的骨骼长度错误率高达 **52.5%**，这意味着超过一半的生成帧中骨骼发生非物理形变。其根本原因在于：修复方法仅替换被控关节的局部轨迹，而扩散模型的去噪过程无法从局部位置恢复全局一致的骨骼结构。相比之下，ProgMoGen 通过优化全局潜在编码生成完整运动，骨骼长度错误率仅为 **0.051**——运动先验在生成过程中隐式保证了人体结构的物理一致性。

### 消融实验：约束松弛与初始点搜索

两项消融揭示了优化策略的关键作用：

**约束松弛（Constraint Relaxation）** 是解决水平位置约束满足不足的核心手段。在 GEO-1 任务上（Table A1），无松弛时约束误差高达 0.118，启用后降至 0.023；HOI-1 任务上从 0.069 降至 0.028。松弛策略允许约束在一定容差内被满足，避免了优化陷入局部极小——代价是 Foot Skate 略有上升（GEO-1: 0.110→0.125），但整体质量-约束平衡显著改善。

**初始点搜索（Initial Point Search）** 通过在 5 个随机初始点中择优，将 HSI-1 的约束误差从 0.012 进一步降至 0.002（Table A2）。这证实了优化景观的非凸性：不同初始点可能收敛到不同局部极小。代价是多样性从 9.611 降至 9.422，FID 略有上升——搜索策略倾向于选择更容易满足约束的解，可能轻微偏离原始分布。

### 定性分析：运动先验的直观效果

Figure 5 提供了运动先验作用的最直观证据。在“方形区域内行走”任务中：
- **IK** 生成无效姿态（关节扭曲、身体穿透），因为仅优化关节位置缺乏对人体姿态流形的感知；
- **IK+Reg.** 产生过度平滑的运动，伴随大量脚滑动——正则化强制相邻帧相似，但牺牲了运动动态性；
- **ProgMoGen** 生成连贯、物理合理的行走运动，同时遵守区域约束。

![[assets/figures/papers/paper_list_l1853_ProgMoGen_Programmable_Motion_Generation_for_Open_set_Motion_Control_Tas/figures/008_Figure_5.jpg]]
*Figure 5: Effect of our motion prior. Top row: Ours generates valid poses while IK and IK+Reg produce invalid ones. Bottom row: IK generates incoherent motion and IK+Reg generates oversmooth motion with massive foot skating. Our method generates coherent motion while adhering to the given constraint*

一个特别值得注意的发现是**涌现行为**：在“两墙之间行走”等全新约束下，ProgMoGen 自动产生了收拢手臂和肩膀的行为，以适应狭窄空间。这并非显式编程的结果，而是预训练运动先验在约束引导下自然涌现的新技能——模型从训练数据中习得的“人如何移动”的知识，使其能在新约束下合成合理的全身协调运动。

### 失败模式与局限性

尽管整体表现优越，ProgMoGen 存在以下可识别的失败模式：

1.  **约束精度与运动质量的固有张力**：在 HSI-2 等任务中，约束误差仍高于纯 IK 方法。当约束与运动先验强烈冲突时（如要求头部保持极低高度同时自然行走），优化可能陷入先验与约束的折衷区，无法精确满足约束。
2.  **不自然姿态与运动伪影**：在某些复杂约束组合下，生成结果可能出现局部不自然的关节角度或过渡伪影。这源于预训练模型容量和数据覆盖的限制——当约束将潜在代码推向分布边缘时，生成质量下降。
3.  **动作语义偏移**：优化过程中，文本条件指定的动作语义可能轻微漂移。例如，“行走”可能在满足头部高度约束时退化为“蹲伏行走”，虽然物理合理但语义不完全匹配。
4.  **优化效率**：每次任务优化需数分钟，不适合实时交互场景，仅适用于离线内容创作管线。

### 关键图表索引

- **Table 1**：已知约束 HSI-1 的全面对比，ProgMoGen 是唯一全指标达标方法
- **Table 2**：四个未见任务的对比，展示泛化能力与质量-约束权衡
- **Table 3**：骨骼长度保持对比，揭示修复方法的根本缺陷（52.5% vs 5.1%）
- **Figure 5**：运动先验效果的定性对比，IK 产生无效姿态，ProgMoGen 保持连贯性
- **Table A1**：约束松弛消融，GEO-1 误差从 0.118 降至 0.023
- **Table A2**：初始点搜索消融，HSI-1 误差从 0.012 降至 0.002

![[assets/figures/papers/paper_list_l1853_ProgMoGen_Programmable_Motion_Generation_for_Open_set_Motion_Control_Tas/figures/010_Table.jpg]]
*Table: A1. Effect of constraint relaxation. Constraint relaxation helps better reach constraints related to horizontal positions for optimization-based methods. Table A2. Effect of initial point search. $N _ { S }$ denotes the number of searches. Using a random initial point search leads to significantly smaller constraint error. It provides a solution for generating motions that better adhere to the given constraint*

### 补充图表

![[assets/figures/papers/paper_list_l1853_ProgMoGen_Programmable_Motion_Generation_for_Open_set_Motion_Control_Tas/figures/009_Table.jpg]]

![[assets/figures/papers/paper_list_l1853_ProgMoGen_Programmable_Motion_Generation_for_Open_set_Motion_Control_Tas/figures/004_Table.jpg]]
*Table: Task HSI-1: head height constraint*

![[assets/figures/papers/paper_list_l1853_ProgMoGen_Programmable_Motion_Generation_for_Open_set_Motion_Control_Tas/figures/006_Figure_4.jpg]]
*Figure 4: Qualitative examples of our method for diverse open-set motion control tasks. The task, error function code and generated motion are demonstrated for each example. The code labeled with GPT marker is generated by GPT given the task description in text*

![[assets/figures/papers/paper_list_l1853_ProgMoGen_Programmable_Motion_Generation_for_Open_set_Motion_Control_Tas/figures/007_Figure.jpg]]
*Figure: Task: “walking” + head height for the keyframe = 0.8 m*

![[assets/figures/papers/paper_list_l1853_ProgMoGen_Programmable_Motion_Generation_for_Open_set_Motion_Control_Tas/figures/011_Table.jpg]]
*Table: A3. Evaluation on motion programming by LLM. Tasks that are successfully handled by LLM are labeled with ✓*



## 定位与知识库关联

### 1. 核心瓶颈：从封闭集任务到开放集约束的范式断裂

现有运动控制方法存在一个根本性瓶颈：**将不同的运动控制需求视为相互独立的封闭集任务**。无论是基于逆运动学（Inverse Kinematics, IK）的优化方法，还是基于扩散模型的轨迹修复方法（如 MDM Edit、PriorMDM），均需为每种任务单独设计数据集和网络结构。这种范式导致三个层面的断裂：

1. **可组合性缺失**：无法将“保持头部高度”与“双手接触”等约束自由组合，因为每个任务被建模为独立的映射关系。
2. **可扩展性受限**：每新增一种约束类型，就需要重新收集配对训练数据并调整网络架构。
3. **可定制性不足**：用户无法像编程一样灵活定义“在两墙之间行走”或“手持球体”等定制化需求。

ProgMoGen 的核心洞察在于：**复杂的运动控制任务可分解为原子约束的组合，几乎所有约束都可量化为可微误差，且误差具有可加性**。这一认识将运动控制从“任务驱动”的封闭范式，转向了“约束驱动”的开放范式。

### 2. 与基线方法的本质差异

#### 2.1 与 IK 类方法的对比

**Inverse Kinematics (IK)** 直接优化关节点位置以满足约束，但完全缺乏运动先验，导致生成的运动在帧间不连贯（Max Acc. 可达 0.414，而 ProgMoGen 仅 0.094）。**IK+Reg.** 通过添加帧间 L2 正则化 $L_{reg} = | x_{[i+1]} - x_{[i]} |$ 缓解抖动，但正则化强度难以调节：过弱则运动不连贯，过强则导致过度平滑和严重滑步（Foot Skate 指标恶化）。

ProgMoGen 的解决思路是**将运动先验内嵌于冻结的预训练生成模型，而非依赖手工设计的正则项**。通过优化隐变量 $z$ 而非直接优化运动参数，生成的运动天然继承预训练模型学习到的运动流形，从而在约束满足与运动质量之间取得平衡。

#### 2.2 与修复类方法的对比

**MDM Edit** 基于扩散模型的轨迹修复机制，通过固定部分关节轨迹进行修补。该方法存在两个根本局限：
- **约束类型受限**：仅支持精确轨迹控制，无法处理不等式约束（如“头部高度 > 0.8m”）、几何约束（如“手触墙壁平面”）或相对距离约束（如“双手间距 < 0.5m”）。
- **骨骼长度破坏**：从局部关节位置恢复时，修复过程会破坏骨骼长度约束，导致骨骼长度错误率高达 52.5%，而 ProgMoGen 仅为 5.1%（Table 3）。

**PriorMDM** 在 MDM Edit 基础上微调模型参数以捕捉被控关节与其余身体的关系，但仍未突破精确轨迹的限制，无法原生处理不等式和几何约束。

ProgMoGen 通过**原子约束库**和**可微误差函数**绕过了这些限制：任何约束只要能量化为可微误差，即可通过优化隐变量来满足，无需修改模型参数或依赖特定训练数据。

#### 2.3 方法谱系定位

从方法论角度看，ProgMoGen 处于**生成模型引导的约束优化**这一交叉地带：

| 维度 | 纯优化方法 (IK) | 修复方法 (MDM Edit) | ProgMoGen |
|------|-----------------|---------------------|-----------|
| 运动先验来源 | 手工正则项 | 扩散模型去噪过程 | 冻结的预训练生成模型 |
| 约束类型支持 | 精确位置约束 | 精确轨迹约束 | 任意可微约束的组合 |
| 任务适应性 | 单一任务 | 单一任务 | 开放集任务 |
| 是否需要训练 | 无需训练 | 无需训练（但需ad-hoc适配） | 无需训练 |

ProgMoGen 的独特贡献在于：**将“任务”的概念从网络设计层面提升到编程抽象层面**，使得运动控制问题转化为误差函数的设计问题，而非模型架构或训练数据的问题。

### 3. 适用边界与局限

#### 3.1 已知适用边界

1. **约束类型边界**：当前原子约束库覆盖了绝对位置、高阶动态（速度/加速度）、几何（平面/体积）、相对距离、方向和关键帧等约束。但对于周期性运动（如“交替摆臂”）、旋转对称约束和频域约束，库的覆盖不足——论文指出约 16% 的 BABEL-120 动作无法直接支持。
2. **优化效率边界**：每次任务优化需数分钟，不适合实时交互场景，但适用于离线内容创作和动画预生成。
3. **语义保持边界**：优化过程中动作语义可能轻微偏移，需要更忠实于文本条件的生成模型和优化方法。

#### 3.2 已知失败模式

1. **复杂约束下的约束误差**：在 HSI-2（避开头顶障碍物）任务中，ProgMoGen 的约束误差（C.Err.）仍高于纯 IK 方法，表明当约束涉及多个关节的复杂空间关系时，单纯依赖隐变量优化可能无法达到 IK 的精确度。
2. **不自然姿态**：在某些任务中会产生运动伪影和不自然姿态，论文认为可通过更大的预训练模型和更多数据改善。
3. **初始点敏感性**：消融实验（Table A2）表明，随机采样 5 次初始点可将约束误差从 0.012 降至 0.002，但以牺牲多样性为代价（Diversity 从 9.611 降至 9.422），说明优化结果对初始隐变量敏感。

### 4. 开放问题与未来方向

1. **约束库的完备性扩展**：如何系统性地扩展原子约束库以覆盖频域约束、旋转对称约束和外部力约束（如拉力、离心力），使框架能够处理更广泛的物理交互场景？

2. **优化策略的混合设计**：能否将 IK 的精确性融入去噪过程，或在优化中部分放松生成模型参数，以在复杂任务中同时实现低约束误差和高运动质量？

3. **语义保真度增强**：如何在优化过程中更好地保留文本指定的动作语义？当前方法在约束满足与语义保持之间存在权衡，需要设计语义感知的优化正则项或约束松弛策略。

4. **自动约束生成与组合**：LLM 自动编程已展示初步可行性（Table A3），但如何在大规模、丰富语义场景中自动识别、生成和组合约束，仍需探索。

5. **实时性能优化**：当前数分钟的优化时间限制了交互式应用，需要研究更高效的优化器设计、隐变量初始化策略或模型蒸馏方案。

6. **全身生成扩展**：如何将框架从身体运动扩展到包含手指、表情等细节的全身生成，需要在约束库和生成模型两个层面进行扩展。



## 原文 PDF

![[paperPDFs/CVPR_2024/ProgMoGen_Programmable_Motion_Generation_for_Open_set_Motion_Control_Tasks.pdf]]
