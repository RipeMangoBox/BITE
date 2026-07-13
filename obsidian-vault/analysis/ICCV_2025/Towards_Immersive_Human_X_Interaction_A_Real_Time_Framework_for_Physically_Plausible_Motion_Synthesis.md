---
title: Towards Immersive Human X Interaction A Real Time Framework for Physically Plausible Motion Synthesis
type: paper
paper_level: A
venue: ICCV
year: 2025
pdf_ref: paperPDFs/ICCV_2025/Towards_Immersive_Human_X_Interaction_A_Real_Time_Framework_for_Physically_Plausible_Motion_Synthesis.pdf
project_link: https://humanx-interaction.github
code_link: null
aliases:
- HX
- TIHXIRTFPPMS
tags:
- ICCV_2025
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: 联合自回归动作-反应扩散规划器 + 演员感知物理跟踪策略 + 多重接触感知损失。
primary_logic: 通过反应者中心表示和联合扩散模型同时预测双方运动，合成反应；再引入强化学习训练的物理策略实时跟踪生成运动，既能保证交互质量，又可确保物理可行性，从而支持低延迟、安全的沉浸式交互。
claims:
- Human-X在Inter-X数据集上显著优于所有基线方法，FID达到0.975，同时物理指标（滑步0.092、穿透体积0.076）大幅改善。
- 消融实验表明，移除交互损失L_inter导致FID从0.975恶化至1.457，交互质量指标严重退化，证明其关键作用。
- Inter-X 上 FID↓ = 0.975
- Inter-X 上 Skating↓ = 0.092
---

# Towards Immersive Human X Interaction A Real Time Framework for Physically Plausible Motion Synthesis

> [!tip] 核心洞察
> 通过反应者中心表示和联合扩散模型同时预测双方运动，合成反应；再引入强化学习训练的物理策略实时跟踪生成运动，既能保证交互质量，又可确保物理可行性，从而支持低延迟、安全的沉浸式交互。

| 字段 | 内容 |
|------|------|
| 中文题名 | 面向沉浸式人机交互的物理合理运动实时合成框架 |
| 英文题名 | Towards Immersive Human X Interaction A Real Time Framework for Physically Plausible Motion Synthesis |
| 会议/期刊 | ICCV 2025 |
| Links | [Project](https://humanx-interaction.github) · [paper](https://arxiv.org/abs/2508.02106) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/image_and_video_generation |
| Method | Human-X |
| Dataset | Inter-X, InterHuman |

> [!tip] 效果简介
> - Inter-X 上，FID↓ 0.975 vs 1.359 (CAMDM) (-0.384)；Skating↓ 0.092 vs 0.143 (InterGen) (-0.051)；IV↓ 0.076 vs 0.138 (CAMDM) (-0.062)。
> - InterHuman 上，FID↓ 1.995 vs 2.166 (CAMDM) (-0.171)。

## 概要

沉浸式人机交互要求系统在动态交互中同时满足实时响应、物理合理性与安全性。现有方法面临两难：运动学生成模型缺乏物理约束，易产生滑步、穿透等伪影；而基于物理的方法则难以有效捕捉复杂的交互动态。**Human-X** 针对这一瓶颈，提出联合自回归动作-反应扩散规划器与演员感知物理跟踪策略，首次实现面向人-虚拟人、人-人形机器人及人-机器人交互的低延迟、物理合理运动合成。

核心思路是：通过反应者中心表示将双方运动统一到同一坐标系，利用自回归扩散模型基于历史交互上下文联合预测动作与反应；再引入强化学习训练的物理策略实时跟踪生成运动，确保交互质量的同时保障物理可行性。训练中引入脚部接触损失、交互损失和前缀连续性损失，强化模型对接触细节和时序一致性的感知。

在 Inter-X 和 InterHuman 数据集上的实验表明，Human-X 在运动质量（FID 0.975）、物理指标（滑步 0.092、穿透体积 0.076）上均显著优于 **InterFormer**、**InterGen**、**ReGenNet**、**CAMDM** 等基线方法。消融实验证实交互损失是关键组件——移除后 FID 从 0.975 恶化至 1.457。用户研究进一步验证了所生成交互在多样性、一致性与真实性上的优势。

### 问题背景

沉浸式人机交互（Human‑X Interaction）要求虚拟角色或机器人在真实世界中与人类进行实时、自然且安全的互动。这类场景涵盖人‑虚拟人交互、人‑人形机器人交互以及人‑机器人交互（**Figure 1**），其核心挑战在于：反应者必须在极低延迟下生成与演员动作协调、物理合理且无安全隐患的运动。

### 现有方法缺口

当前人类反应合成方法大致分为两类，但均无法同时满足实时性、物理合理性与交互质量的要求。

- **运动学方法**：基于运动学生成的模型（如 InterFormer、InterGen、ReGenNet、CAMDM）虽然能够产生多样化的反应运动，但普遍缺乏物理约束，导致脚部滑步、身体穿透等伪影，难以直接部署到真实机器人或安全关键场景。
- **基于物理的方法**：通过强化学习或轨迹优化引入物理仿真，能够保证运动可行性，但现有工作在动态人机交互中难以有效捕捉交互动态，反应往往生硬且缺乏上下文适应性。

**Table 1** 的系统对比进一步揭示：已有方案在实时在线推理、物理跟踪策略、文本引导生成以及沉浸式 VR 接口等方面存在明显缺失，无法构成完整的沉浸式交互闭环。

### 本文动机

针对上述瓶颈，本文提出 **Human‑X**——首个面向沉浸式人机交互的实时物理合理运动合成框架。其核心动机在于：

1. **联合预测动作与反应**：通过自回归扩散规划器同时建模双方运动历史，避免独立预测导致的交互不协调。
2. **物理可行性保障**：引入基于强化学习的演员感知运动跟踪策略，在跟踪生成运动的同时消除滑步、穿透等物理伪影，确保接触安全。
3. **低延迟沉浸体验**：整合实时动作捕捉、扩散生成与 VR 渲染，实现端到端低延迟交互，使反应者能够即时响应演员动作。

简言之，Human‑X 旨在弥合运动学生成与物理仿真之间的鸿沟，为真实世界人机交互提供一种兼具交互质量与物理安全性的实时解决方案。

## 核心方法与创新机理

Human‑X 的核心创新在于将**联合自回归扩散规划**与**演员感知物理跟踪**首次整合为一个实时交互框架，解决了动态人机交互中运动质量、物理合理性与低延迟难以兼得的瓶颈。其关键设计围绕三个 changed slots 展开。

### 1. 联合自回归动作‑反应扩散规划器

现有反应生成模型（如 InterFormer、InterGen、ReGenNet、CAMDM）通常采用独立或非自回归策略，无法充分建模交互双方的运动耦合与长时序依赖。Human‑X 提出**反应者中心交互表示** $z^{n} = (x^{n}, y^{n}, \mathcal{T}^{n})$，将反应者运动、相对演员运动及关节接触特征统一编码（Sec. 3.3.1）。在此基础上，扩散规划器以自回归方式联合利用双方运动历史 $\{ \mathbf{x}^{i-1}, \mathbf{y}^{i-1} \}$ 预测未来 $k$ 帧的反应运动 $\mathbf{x}^i$（Sec. 3.3），从而在时序连贯性和交互一致性上获得显著增益。消融实验证实，移除交互损失 $\mathcal{L}_{inter}$ 后 FID 从 0.975 恶化至 1.457（Table 3），验证了联合建模对交互质量的关键作用。

### 2. 多重接触感知训练目标

与基线方法仅使用简单重建损失不同，Human‑X 在训练目标中显式引入了三类辅助损失（Eq. 7）：
- **脚部接触损失 $\mathcal{L}_{foot}$**：抑制滑步与浮空伪影，提升物理可信度；
- **交互损失 $\mathcal{L}_{inter}$**：利用二值身体交互场 $\bar{\mathcal{T}}^{x,y}$ 加权接触关节位置差异，强制生成高保真接触（Eq. 6）；
- **前缀连续性损失 $\mathcal{L}_{prefix}$**：保证自回归窗口中相邻片段的光滑过渡。

消融实验表明，移除 $\mathcal{L}_{foot}$ 会显著增加滑步和浮空指标（Table 3），而 $\mathcal{L}_{inter}$ 的缺失直接导致交互质量指标严重退化，证明这些损失是运动质量与物理合理性提升的核心驱动力。

### 3. 演员感知物理跟踪策略

传统方法缺乏物理约束或仅采用简单碰撞避免，难以保证安全交互。Human‑X 引入基于强化学习的**演员感知运动跟踪策略（PHC‑based）**，在跟踪扩散生成运动的同时，动态适应交互伙伴的动作，从根本上消除脚部滑步、身体穿透等伪影（Sec. 3.4）。Table 2 显示，Human‑X*（带物理跟踪器）在滑步（0.092）和穿透体积（0.076）上均大幅优于纯运动学基线，且演员感知策略相比普通 PHC 进一步降低了干涉体积并提高成功率（Table 8），验证了物理跟踪在安全实时交互中的必要性。

### 4. 系统级创新：从合成到部署的闭环

上述三个 changed slots 并非孤立改进，而是通过**实时动作捕捉（RGB‑D + HybrIK）→ 自回归扩散规划 → 物理跟踪 → VR 渲染**的流水线（Figure 2）形成闭环。这使得 Human‑X 成为首个在统一框架内同时实现实时响应、物理合理性和交互多样性的系统，可直接部署于人‑虚拟人、人‑人形机器人、人‑机器人等多种沉浸式交互场景（Figure 1）。

Human‑X 提出了一种面向沉浸式人机交互的实时运动合成框架，其核心目标是同时满足动态交互中的三项关键需求：**实时响应**、**物理合理性**与**接触安全**。现有方法通常在这三者之间存在取舍——纯运动学生成模型缺乏物理约束，容易产生滑步、穿透等伪影；而基于物理的方法则难以有效捕捉复杂的交互动态。Human‑X 通过将**自回归动作‑反应扩散规划器**与**基于强化学习的演员感知物理跟踪策略**解耦，形成“先规划、后跟踪”的两阶段流水线，从而在保证交互质量的同时，确保生成的运动在物理仿真中可行。

### 系统流水线

整个框架由四个核心模块串联而成，形成从演员动作捕获到沉浸式渲染的闭环（见图 2）：

1.  **演员运动捕获**：通过 RGB‑D 相机以 30 fps 实时采集演员图像，并利用 HybrIK 进行无延迟的人体姿态重建。重建后的 SMPL 姿态被重定向到仿人角色，作为后续模块的在线动作输入。
2.  **自回归交互扩散规划器**：该模块是框架的生成核心。它接收双方的历史交互上下文（过去 20 帧的动作与反应），并可选择性地接受文本提示（如“跳舞”），通过联合扩散模型自回归地预测未来 40 帧的反应者运动。其关键在于引入了**反应者中心交互表示**和**多重接触感知损失**，使模型能同时关注自身运动质量与双方的空间协调关系。
3.  **演员感知反应运动跟踪器**：基于物理角色控制器构建，使用强化学习训练的策略来跟踪扩散规划器生成的反应运动。该策略不仅接收本体感知信号，还显式感知演员的运动状态，从而动态调整反应，避免脚部滑动、身体穿透等物理伪影，确保交互安全。
4.  **实时 VR 接口**：基于 Unity 构建，将跟踪后的运动实时渲染至 VR 头显，同时提供第三人称视角和双目立体视角，支持人‑虚拟人、人‑人形机器人等多种交互场景的沉浸式体验。

### 模块间的输入输出流

流水线的数据流是单向且低延迟的：演员运动捕获模块输出实时 SMPL 姿态序列；扩散规划器以滑动窗口方式消费这些姿态，输出未来反应运动序列；物理跟踪器将规划器的输出作为跟踪目标，在物理仿真器中执行，并将最终的运动状态传递给 VR 渲染模块。规划器与跟踪器的解耦设计使得生成质量与物理可行性可以独立优化，同时跟踪器能补偿规划器可能产生的物理不可行运动。

### 关键设计决策

-   **反应者中心表示**：所有交互信息均以反应者为参考系进行规范化（canonicalization），将反应者置于原点并统一朝向，演员的运动也经过相同变换。这一设计消除了全局坐标的干扰，使模型更容易学习相对运动模式。
-   **联合扩散规划**：与独立预测反应者运动的基线方法不同，Human‑X 的扩散模型同时预测动作和反应双方的未来运动，从机制上保证了交互的协调性。消融实验证实，移除交互损失 $L_{inter}$ 会导致 FID 从 0.975 恶化至 1.457，交互质量指标严重退化（Table 3）。
-   **物理跟踪策略的演员感知**：传统物理跟踪器仅依赖本体感知，无法预判交互方的动作。Human‑X 的策略显式编码演员运动信息，在测试中将干涉体积从 PHC 的 0.138 降至 0.076，同时提高了交互成功率（Table 8）。

### 方法谱系与知识库定位

Human‑X 位于**物理合理的人‑人/人‑机交互运动合成**这一交叉领域。在反应生成侧，它与 **InterFormer**、**InterGen**、**ReGenNet**、**CAMDM** 等方法同属基于学习的反应生成模型，但通过自回归扩散架构和联合预测机制，在交互质量和运动多样性上实现了显著提升。在物理仿真侧，它继承并扩展了基于物理的角色控制方法，将传统的单人运动跟踪策略升级为演员感知的交互跟踪策略。这种“生成模型 + 物理策略”的组合范式，为实时、安全、高质量的沉浸式交互提供了新的技术路线。

> **注意**：当前分析中，InterFormer、InterGen、ReGenNet、CAMDM 的具体作者/年份/会议信息未在提供的上下文中给出，建议手动补充引用元数据。

### 反应者中心交互表示

Human‑X 的核心设计之一是**反应者中心交互表示**（reactor‑centric interaction representation）。该表示以反应者（虚拟人/机器人）为参照系，将双方运动统一到同一坐标系下，避免全局朝向和根位移带来的歧义。具体地，先将反应者的根关节平移到原点并旋转至正前方，再对演员施加相同的刚体变换，从而保留相对空间关系。第 $n$ 帧的交互原语定义为：

$$z^{n} = (x^{n}, y^{n}, \mathcal{T}^{n})$$

其中：
- $x^{n}$：反应者自身运动（局部姿态、根位移、关节旋转等）；
- $y^{n}$：经过相同变换后的演员相对运动；
- $\mathcal{T}^{n}$：二值化身体交互场（binary body interaction field），编码双方各关节是否处于接触状态（维度 $6 \times 6$，对应双方各 6 个身体区域）。

这一表示将“交互”从“两个独立运动序列”提升为“一个联合交互原语”，为后续扩散模型的同时预测提供了紧凑的输入/输出空间（见 Eq. 1 及 3.3.1 节）。

### 自回归扩散规划器

Human‑X 的反应生成由**自回归扩散规划器**完成，其任务是根据历史交互上下文预测未来反应运动。在第 $i$ 个滑动窗口，模型以过去 $h$ 帧的交互原语 $\mathbf{z}^{i-1}$ 为条件，预测未来 $k$ 帧的交互原语 $\mathbf{z}^{i}$。

**前向扩散过程**采用标准 DDPM 公式，向真实交互原语 $\mathbf{z}_{0}^{i}$ 逐步注入高斯噪声：

$$q(\mathbf{z}_{t} \vert \mathbf{z}_{t-1}) = \mathcal{N}(\sqrt{\alpha_{t}} \mathbf{z}_{t-1}, (1 - \alpha_{t}) \mathbf{I})$$

**去噪网络** $\mathcal{G}$ 基于 Transformer 架构，其输入包括当前噪声样本 $\mathbf{z}_{t}^{i}$、历史上下文 $\mathbf{z}^{i-1}$、扩散时间步 $t$ 以及可选文本条件 $c$。与常规 DDPM 预测噪声不同，该网络直接预测干净的交互原语 $\hat{\mathbf{z}}_{0}^{i}$：

$$\hat{\mathbf{z}}_{0}^{i} = \mathcal{G}(\mathbf{z}_{t}^{i}, \mathbf{z}^{i-1}, t, c)$$

这一“预测原语而非噪声”的设计在运动生成中已被证明更稳定（Eq. 3，3.3.2 节）。

**简单扩散损失**为预测原语与真实原语之间的均方误差：

$$\mathcal{L}_{simple} = \mathbb{E}_{\mathbf{z}_{0}^{i} \sim q(\mathbf{z}_{0}^{i}), t \sim [1,T]} [\| \mathbf{z}_{0}^{i} - \hat{\mathbf{z}}_{0}^{i} \|_{2}^{2}]$$

### 多重接触感知损失

仅靠 $\mathcal{L}_{simple}$ 无法保证交互的物理合理性和接触真实性。Human‑X 引入了三项辅助损失，共同构成完整训练目标：

$$\mathcal{L} = \mathcal{L}_{simple} + \lambda_{foot} \mathcal{L}_{foot} + \lambda_{inter} \mathcal{L}_{inter} + \lambda_{prefix} \mathcal{L}_{prefix}$$

各损失的作用如下（Eq. 7，3.3.2 节）：

1. **脚部接触损失 $\mathcal{L}_{foot}$**：惩罚脚部与地面的相对滑动和浮空，通过检测脚部速度与地面接触状态的不一致性来约束，直接降低滑步（Skating）指标。
2. **交互损失 $\mathcal{L}_{inter}$**：利用二值身体交互场 $\bar{\mathcal{T}}^{x,y}$ 作为掩码，计算双方接触关节位置之间的 L2 距离：

   $$\mathcal{L}_{inter} = \Vert (p^{x}(\hat{\mathbf{z}}_{0}^{i}) - p^{y}(\hat{\mathbf{z}}_{0}^{i})) \odot \bar{\mathcal{T}}^{x,y}(\hat{\mathbf{z}}_{0}^{i}) \Vert_{2}^{2}$$

   该损失仅在预测的接触关节上施加约束，迫使双方在交互时刻保持合理的空间对齐（如握手时手掌贴合）。消融实验证实，移除 $\mathcal{L}_{inter}$ 会使 FID 从 0.975 恶化至 1.457，交互质量指标严重退化（Table 3）。

3. **前缀连续性损失 $\mathcal{L}_{prefix}$**：约束当前窗口前若干帧的预测与上一窗口的生成结果保持一致，缓解自回归过程中的时序断裂和漂移。

### 文本引导采样

为支持文本指定的交互风格（如“跳舞”“击掌”），Human‑X 在推理时采用**无分类器引导**（classifier‑free guidance）。采样时，去噪网络同时接收条件文本 $c$ 和空文本 $\phi$，通过加权外推增强文本控制力：

$$\mathcal{G}_{w}(\mathbf{z}_{t}^{i}, \mathbf{z}^{i-1}, t, c) = \mathcal{G}(\mathbf{z}_{t}^{i}, \mathbf{z}^{i-1}, t, \phi) + w \cdot (\mathcal{G}(\mathbf{z}_{t}^{i}, \mathbf{z}^{i-1}, t, c) - \mathcal{G}(\mathbf{z}_{t}^{i}, \mathbf{z}^{i-1}, t, \phi))$$

其中 $w$ 为引导强度（Eq. 8）。这一机制使同一演员动作可根据不同文本提示生成不同风格的反应，在 Inter‑X 和 InterHuman 的文本引导实验中均取得最优（Table 5、Table 6）。

### 演员感知物理跟踪策略

扩散规划器输出的运动虽在运动学层面合理，但直接驱动虚拟角色仍会产生滑步、穿透等物理伪影。Human‑X 引入基于强化学习的**演员感知运动跟踪策略**（actor‑aware motion tracking policy），将生成的反应运动作为模仿目标，同时感知演员的实时运动状态，在物理仿真器中执行跟踪。

该策略的关键在于**安全感知**：其奖励函数不仅包含对目标姿态的跟踪精度，还显式惩罚与演员身体的穿透体积（interpenetration volume）。相比仅使用标准 PHC（Perpetual Humanoid Control）策略，演员感知版本将干涉体积从 0.138 降至 0.076，同时将交互成功率提升约 12%（Table 8，3.4 节）。

### 系统流水线模块

上述方法模块被整合为四个流水线组件（Figure 2）：

1. **演员动作捕捉**：RGB‑D 相机以 30 fps 采集图像，HybrIK 实时重建 SMPL 姿态，并重定向到类人角色（3.2 节）。
2. **自回归交互扩散规划器**：以历史交互原语和可选文本为输入，生成未来反应运动（3.3 节）。
3. **反应运动跟踪器**：基于 PHC 的强化学习策略，在物理引擎中跟踪生成运动，保证物理可行性和接触安全（3.4 节）。
4. **VR 接口**：基于 Unity 的实时渲染管线，将交互场景输出至 VR 头显，支持第三人称和双目立体视图（4.1 节）。

## 实验与关键发现

### 主实验结果

Human-X 在两个主流交互数据集 **Inter-X** 和 **InterHuman** 上均展现出对现有方法的显著优势。在 Inter-X 数据集的在线无约束反应设置下（Table 2），Human-X 的 FID 达到 **0.975**，相比最强运动学基线 CAMDM（1.359）降低了 0.384，同时物理合理性指标大幅改善：滑步（Skating）仅 **0.092**（InterGen 为 0.143），穿透体积（IV）仅 **0.076**（CAMDM 为 0.138）。引入物理跟踪策略的 Human-X* 版本进一步将滑步降至 0.081、穿透体积降至 0.066，但 FID 略有上升（1.011），体现了物理约束与运动多样性之间的权衡。

![[assets/figures/papers/paper_list_l1777_Towards_Immersive_Human_X_Interaction_A_Real_Time_Framework_for_Physical/figures/006_Table_2.jpg]]
*Table 2: Action-to-Reaction with online unconstrained reaction setting on Inter-X [65] dataset. A higher or lower value is better for ↑ or ↓, and → means the value closer to ground truth is better. * denotes the method with reaction policy designed for humanoid reaction*

在 InterHuman 数据集上（Table 4），Human-X 同样保持领先：FID 为 **1.995**，优于 CAMDM 的 2.166。物理跟踪版本 Human-X* 的滑步指标从纯运动学版本的 0.098 进一步压缩至 0.082，验证了物理策略的跨数据集泛化能力。

![[assets/figures/papers/paper_list_l1777_Towards_Immersive_Human_X_Interaction_A_Real_Time_Framework_for_Physical/figures/008_Table_4.jpg]]
*Table 4: Action-to-Reaction with online unconstrained reaction setting on InterHuman[32] dataset. A higher or lower value is better for*

文本引导反应设置下（Table 5、Table 6），Human-X 在 FID、R-Precision 等指标上依然保持最优或次优，证明其文本条件控制机制与运动生成质量可以协同工作。

![[assets/figures/papers/paper_list_l1777_Towards_Immersive_Human_X_Interaction_A_Real_Time_Framework_for_Physical/figures/009_Table_5.jpg]]
*Table 5: Action-to-Reaction with online text-guided reaction setting on Inter-X [65] dataset, where a higher or lower value is better for ↑ or ↓, and → means the value closer to ground truth is better*

### 消融实验分析

消融实验（Table 3）揭示了各损失组件的因果贡献：

![[assets/figures/papers/paper_list_l1777_Towards_Immersive_Human_X_Interaction_A_Real_Time_Framework_for_Physical/figures/007_Table_3.jpg]]
*Table 3: Ablation studies of online reaction setting on the Inter-X [65] dataset*

- **移除交互损失 $\mathcal{L}_{inter}$**：FID 从 0.975 恶化至 **1.457**，交互质量指标（FID_cd、接触精度）严重退化。这直接验证了 $\mathcal{L}_{inter}$ 是保障强交互场景（如击打面部、握手）下肢体接触准确性的关键因素。
- **移除脚部接触损失 $\mathcal{L}_{foot}$**：滑步和浮空指标明显上升，物理伪影增加，说明该损失对地面接触约束和运动自然性有实质贡献。
- **时间步数消融**：扩散步数 $T$ 从 8 增至 16 时性能饱和，$T=8$ 即可在效率与质量间取得最优平衡（Table 7）。

额外消融（Table 7）表明：反应者中心表示优于世界坐标系表示；交互场维度 $6 \times 6$ 是合理选择；Transformer 解码器层数以 8 层为最优配置。

### 物理策略对比

Table 8 对比了标准 PHC 策略与本文提出的演员感知策略（actor-aware policy）在物理跟踪任务上的表现。演员感知策略在干涉体积（IV）和任务成功率上均优于 PHC，证明显式建模交互伙伴运动对安全物理交互至关重要。

![[assets/figures/papers/paper_list_l1777_Towards_Immersive_Human_X_Interaction_A_Real_Time_Framework_for_Physical/figures/012_Table_8.jpg]]
*Table 8: Test performance of reaction policy on Inter-X dataset. (Ours-safety indicates actor-aware policy)*

### 定性分析与用户研究

Figure 3 的定性对比显示，CAMDM 在手部接触任务中存在接触不完整、脚部运动不自然等问题，而 Human-X 实现了更完整的手部接触和更自然的足部运动。Figure 4 展示了人机握手交互的完整过程，从手臂伸展、手掌接触到握手完成，体现了空间协调性和运动连贯性。

![[assets/figures/papers/paper_list_l1777_Towards_Immersive_Human_X_Interaction_A_Real_Time_Framework_for_Physical/figures/005_Figure_4.jpg]]
*Figure 4: Visualization results on Human-Robot Interaction. The robot (black skeleton) and human (orange mesh) perform a handshake on a flat plane, from arm extension and palm contact through to shake completion, illustrating our method’s spatial coordination and motion coherence*

用户研究（Figure 5，Table 9）邀请参与者从多样性、一致性和真实性三个维度评价生成结果，Human-X 在所有指标上均获得最高偏好，进一步佐证了定量指标的优势具有感知层面的实际意义。

### 失败模式与局限性

尽管 Human-X 在主要指标上表现优异，仍存在以下限制：

1. **短时序窗口**：模型仅使用过去 20 帧预测未来 40 帧，可能导致长程交互上下文的丢失，在需要记忆早期动作线索的场景中产生不协调反应。
2. **模态单一**：当前仅支持动作和文本输入，未集成音频、视觉等多模态信号，限制了更丰富交互场景的表达能力。
3. **表示局限**：反应者表示限于 SMPL 骨架，未扩展到 SMPL-X 或机器人关节，无法精细控制面部表情、手部姿态和体型。
4. **人数限制**：仅支持两人交互，多人协同场景尚未实现。
5. **个性缺失**：反应生成缺乏个性定制，无法模拟不同性格特征的差异化回应。

这些局限性在 Table 2 中也有间接体现：Human-X 的多样性指标（Diversity）在部分设置下略低于某些基线，可能与物理约束和短时序窗口对运动空间的压缩有关，需在后续工作中进一步平衡。

## 定位与知识库关联

### 1. 核心问题与因果瓶颈

沉浸式人机交互（Human‑X Interaction）要求系统在动态、非结构化场景中同时满足三个强约束：**实时响应**（低延迟）、**物理合理性**（无滑步、无穿透）和**交互安全性**（接触真实、避免碰撞）。现有方法普遍在两个维度上存在瓶颈：

- **运动学生成方法**（如 InterFormer、InterGen、ReGenNet、CAMDM）虽然能产生多样化的反应动作，但缺乏物理约束，导致脚部滑步、身体穿透等伪影，难以直接部署到真实机器人或物理仿真环境中。
- **基于物理的方法**（如 PHC 等通用运动跟踪策略）虽然能保证物理可行性，但无法有效捕捉双人交互的动态语义和接触意图，生成的反应动作在交互质量（如握手完整性、击掌对齐度）上明显不足。

**Human‑X 的因果调节变量**在于：通过**反应者中心表示**将双人运动统一到一个相对坐标系下，再利用**自回归扩散规划器**联合预测双方未来运动，从而在生成阶段就内嵌交互语义；同时引入**演员感知的物理跟踪策略**（基于强化学习），将运动学输出转化为物理仿真中的安全动作，最终在实时闭环中实现“生成‑跟踪”协同优化。

### 2. 方法继承与突破

Human‑X 的方法架构可视为三条技术路线的交叉融合：

| 技术路线 | 代表工作/组件 | Human‑X 的继承 | Human‑X 的突破 |
|---------|-------------|---------------|---------------|
| **运动扩散模型** | MDM (Tevet et al., ICLR 2023)、MotionDiffuse (Zhang et al., 2023) | 采用 DDPM 框架进行运动生成，使用 Transformer 去噪器预测干净运动原语而非噪声 | 首次将扩散模型应用于**在线自回归交互反应生成**，并引入无分类器引导实现文本可控 |
| **交互运动合成** | InterFormer (Chopin et al., 2023)、InterGen (Liang et al., ECCV 2024)、CAMDM | 继承双人运动联合建模的思路和 Inter‑X/InterHuman 数据集 | 提出反应者中心表示和联合扩散规划器，将交互建模从离线生成推向**实时在线**场景 |
| **物理角色控制** | PHC (Luo et al., SIGGRAPH 2023)、AMP (Peng et al., 2021) | 使用 PHC 作为基础运动跟踪策略，利用强化学习训练 | 设计**演员感知的跟踪策略**，将演员运动作为策略输入的一部分，使反应者能动态适应交互伙伴的动作 |

**关键改变槽位**（Table 1 对照）：

1. **反应生成模型**：从独立或非自回归模型（如固定窗口扩散、单人类模型迁移）升级为**自回归扩散规划器**，基于双方运动历史联合预测动作与反应（Sec. 3.3）。
2. **物理约束**：从无约束或简单碰撞避免升级为**基于强化学习的演员感知运动跟踪策略（PHC）**，确保物理合理性和接触安全（Sec. 3.4）。
3. **训练目标**：从简单重建损失升级为**多重接触感知损失**，包括脚部接触损失 $\mathcal{L}_{foot}$、交互损失 $\mathcal{L}_{inter}$ 和前缀连续性损失 $\mathcal{L}_{prefix}$（Eq. 7）。

### 3. 方法适用边界与局限

Human‑X 在设计上存在明确的适用边界，这些边界既是当前方法的能力上限，也指明了后续改进方向：

- **时序窗口限制**：模型仅使用过去 20 帧（约 0.67 秒）预测未来 40 帧（约 1.33 秒），短时序窗口在长时间交互中可能丢失关键历史信息，导致反应动作与早期交互上下文脱节。
- **模态输入单一**：当前仅支持基于动作和文本输入的反应生成，尚未集成音频、视觉等多模态信号，限制了在语音对话、视觉场景理解等复杂交互场景中的应用。
- **角色表示受限**：反应者表示限于 SMPL 骨架，未扩展到 SMPL‑X（含面部、手部细节）或机器人关节，难以支持精细的手部交互（如弹钢琴）或异构机器人交互。
- **交互规模固定**：仅支持两人交互，多人协同场景（如三人舞蹈、团队运动）尚未实现，反应生成无法考虑多方动态。
- **个性缺失**：反应生成缺乏个性定制，无法模拟不同性格（如外向/内向、主动/被动）的差异回应，限制了在虚拟人、游戏 NPC 等需要角色一致性的场景中的应用。

### 4. 开放问题与未来方向

基于上述局限，Human‑X 框架指出了若干开放问题：

- **长时序上下文整合**：如何利用大型语言模型（LLM）或长程记忆机制整合更长时序的交互历史，提升运动规划与决策的全局一致性？
- **多模态融合**：如何将音频（语音、环境声）、视觉（场景语义、物体位置）等多模态信号融入反应生成，实现更丰富的交互合成（如“听到指令后握手”）？
- **精细角色表示**：如何将反应者表示扩展到 SMPL‑X/SMPL+H，支持面部表情、手部姿态和体型的精细控制，以适应高保真虚拟人应用？
- **多人交互扩展**：如何从双人交互扩展到三人或更多参与者的实时交互，处理更复杂的空间关系和社交动态？
- **个性化反应**：如何赋予反应者稳定的个性特征，生成与角色设定一致的个性化响应，同时保持交互的自然性和多样性？

### 5. 知识库定位

Human‑X 在现有知识库中的定位可概括为：

- **任务层面**：属于**在线动作到反应合成**（Online Action‑to‑Reaction Synthesis），区别于离线批量生成（如 InterGen）和单人类运动生成（如 MDM）。
- **方法层面**：是**扩散模型 + 强化学习**在交互运动合成中的首次端到端整合，将运动学规划与物理执行解耦但协同优化。
- **应用层面**：覆盖**人‑虚拟人、人‑人形机器人、人‑机器人**三类交互场景，是首个面向实时沉浸式交互的统一框架。

与已有工作的关系：Human‑X 在运动质量（FID 0.975 vs. CAMDM 1.359，Table 2）和物理指标（滑步 0.092、穿透体积 0.076）上显著超越现有基线，但运动多样性（Diversity 指标）在引入物理跟踪器后有所下降（Human‑X* 版本），体现了物理约束与运动多样性之间的固有权衡。

## 原文 PDF

![[paperPDFs/ICCV_2025/Towards_Immersive_Human_X_Interaction_A_Real_Time_Framework_for_Physically_Plausible_Motion_Synthesis.pdf]]
