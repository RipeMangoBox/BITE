---
title: Interactive Humanoid Online Full Body Motion Reaction Synthesis with Social Affordance Canonicalization and Forecasting
type: paper
paper_level: A
venue: 3DV
year: 2025
pdf_ref: paperPDFs/3DV_2025/Interactive_Humanoid_Online_Full_Body_Motion_Reaction_Synthesis_with_Social_Affordance_Canonicalization_and_Forecasting.pdf
aliases:
- SACF
- IHOFBMRSSACF
tags:
- 3DV_2025
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
core_operator: 通过等变局部框架对社会可供性进行规范化，简化动作分布；并利用社会可供性预测，使反应者基于想象的未来进行规划。
primary_logic: 将互动编码为以载体为中心的社会可供性表示，通过局部框架规范化来降低动作模式的复杂性，并通过预测未来动作来克服在线短视问题，是实现高质量反应合成的关键。
claims:
- 消融实验表明，移除规范化模块后FID从13.3升至34.5，验证了社会可供性规范化的核心作用。
- 在HHI、InterHuman、Chi3D三个数据集上，我们的方法在所有指标上均显著优于现有最佳基线方法。
- HHI 上 FID = 13.3
- InterHuman 上 FID = 14.7
---

# Interactive Humanoid Online Full Body Motion Reaction Synthesis with Social Affordance Canonicalization and Forecasting

> [!tip] 核心洞察
> 将互动编码为以载体为中心的社会可供性表示，通过局部框架规范化来降低动作模式的复杂性，并通过预测未来动作来克服在线短视问题，是实现高质量反应合成的关键。

| 字段 | 内容 |
|------|------|
| 中文题名 | 交互式人形机器人：基于社会可供性规范化和预测的在线全身动作反应合成 |
| 英文题名 | Interactive Humanoid Online Full Body Motion Reaction Synthesis with Social Affordance Canonicalization and Forecasting |
| 会议/期刊 | 3DV 2025 |
| Links | [Project](https://yunzeliu.github.io/iHuman/) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction |
| Method | Social Affordance Canonicalization and Forecasting |
| Dataset | HHI, InterHuman, Chi3D, CoChair |

> [!tip] 效果简介
> - HHI 上，FID 13.3。
> - InterHuman 上，FID 14.7。
> - Chi3D 上，FID 12.8。

## 概述

本文提出了一项新任务——**在线全身动作反应合成**（Online Full-Body Motion Reaction Synthesis），目标是在仅能访问人类表演者历史动作的在线设定下，由人形机器人实时生成自然、及时且符合社会规范的全身反应动作。该任务面临两个核心瓶颈：其一，反应者只能基于过去观察进行决策，信息短视导致难以做出及时反应；其二，人类表演者的动作模式高度多样，直接学习从观察到反应的映射极为困难。

针对上述问题，本文提出了**社会可供性规范化与预测**（Social Affordance Canonicalization and Forecasting）技术。其核心洞察是：将互动过程编码为以“载体”为中心的社会可供性表示，通过等变局部框架对该表示进行规范化以降低动作分布的复杂性，并借助社会可供性预测使反应者能够基于想象的未来进行规划，从而克服在线短视问题。该方法统一处理有人-物交互与纯人-人交互场景，通过载体选择、载体中心表示、等变规范化、动作预测和4D Transformer自编码器五个模块协同完成反应生成。

实验表明，该方法在自建的HHI（人-人交互）和CoChair（人-物-人交互）数据集以及公开的InterHuman、Chi3D数据集上，所有评估指标均显著优于现有基线方法。消融实验进一步验证了社会可供性规范化的关键作用——移除该模块后，FID指标从13.3急剧上升至34.5。此外，该方法参数量小，可实现约25 FPS的实时推理。

## 背景与动机

### 问题背景：在线全身动作反应合成

在人机交互场景中，人形机器人（humanoid）需要根据人类表演者（actor）的动作实时生成自然、协调的全身反应动作。这一任务被称为**在线全身动作反应合成**（online full-body motion reaction synthesis），其核心挑战在于：反应者（reactor）在每一时刻只能观察到表演者过去的动作序列，却需要立即输出当前帧的合理反应。与离线设定不同，在线设定下的反应者无法访问未来信息，这构成了根本性的信息短视困境。

该任务的可选扩展场景是**人-物体-人形机器人交互**（human-object-humanoid interaction），例如协作搬运椅子。此时，物体本身承载了重要的社会可供性（social affordance）信息——它暗示着双方可能的接触区域和交互意图。

### 现有方法的缺口

现有的人体运动预测与反应生成方法存在三个层面的不足：

**第一，坐标框架的选择。** 主流基线方法（如 **Progressively Generating Better Initial Guesses**（Ma et al., CVPR 2022）、**Spatio-temporal Transformer**、**HumanMAC**（Chen et al., arXiv 2023））均在全局坐标系下编码关节位置与速度。这种表示将同一交互动作在不同空间位置下的实例视为截然不同的样本，导致动作分布高度多模态，学习难度显著增大。

**第二，时间信息范围的局限。** 现有在线方法仅基于历史观测序列进行推理，缺乏对未来的预判能力。当表演者动作发生快速变化时，反应者容易产生延迟或不协调的反应。

**第三，交互表示的统一性缺失。** 有物体交互与无物体交互（纯人-人形机器人交互）通常被当作两个独立问题处理，缺乏统一的表示框架。现有交互生成方法（如 **InterFormer**（Chopin et al., TMM 2023）、**InterGen-revised**（Liang et al., arXiv 2023））主要关注多人体运动生成，未系统建模以物体或反应者自身为载体的社会可供性结构。

### 本文动机与核心思路

本文的核心洞察是：**将交互编码为以载体为中心的社会可供性表示，通过局部框架规范化来降低动作模式的复杂性，并通过预测未来动作来克服在线短视问题，是实现高质量反应合成的关键。**

具体而言，本文提出两大技术手段：

- **社会可供性规范化（Social Affordance Canonicalization）**：引入“可供性载体”（affordance carrier）概念——在有物体场景中选择物体，在无物体场景中选择人形机器人的休息姿态作为载体。以载体为参考系构建等变局部框架，将表演者运动投影到该框架下，从而消除全局坐标系带来的分布复杂性。消融实验表明，移除规范化模块后FID从13.3升至34.5，验证了这一策略的核心作用（Table 4）。

- **社会可供性预测（Social Affordance Forecasting）**：在训练阶段，反应者可访问表演者的完整动作序列；在在线预测阶段，通过预测模块基于历史序列推断表演者未来的动作趋势，使反应者能够基于“想象的未来”进行规划，从而生成更及时、更协调的反应。

该方法统一处理有/无物体的交互场景，并在HHI、InterHuman、Chi3D三个数据集上一致优于现有最佳基线（Table 2）。

## 核心创新

本工作提出了一项新的任务——**在线全身动作反应合成**，并针对该任务中两个根本瓶颈设计了系统性的解决方案。核心瓶颈在于：**（1）在线设定下反应者仅能访问过去观测，信息短视导致难以做出及时反应；（2）人类表演者的动作模式高度多样，直接学习从表演者到反应者的映射极其困难。** 为此，方法引入了两个相互协同的关键创新。

### 创新一：社会可供性规范化

传统方法直接在全局坐标系下编码表演者的关节位置与速度，导致动作分布高度复杂且对空间变换敏感。本工作提出**社会可供性规范化**策略，通过三个步骤从根本上简化了学习目标：

1. **载体选择与以载体为中心的表示**：引入“可供性载体”概念，在有物体交互场景中选择物体，在纯人-人交互场景中选择反应者的休息姿态作为载体。以载体上的点/关节为参考系，通过图神经网络将表演者运动编码为局部表示 $R^{i}(h^{i}, c^{i}) = \{ (x_{j}^{i}, \epsilon_{\theta}(h^{i})) \}_{j=1}^{N}$，形成社会可供性 $A^{i} = \{R^{t}\}_{t=1}^{i}$。

2. **等变局部框架学习**：通过 Equiv-FrameNet 从载体几何中学习旋转等变的局部框架 $\mathbf{F}_{l}$，将表演者运动投影到该框架下进行规范化。这一操作使得不同空间姿态下的相同交互模式被映射到相近的规范表示，显著降低了动作分布的复杂度。

3. **统一处理有/无物体场景**：无论载体是物体还是人形机器人，规范化后的社会可供性表示具有统一的形式，使得同一框架可以无缝处理两类场景。

**证据强度**：消融实验（Table 4）显示，移除规范化模块后，FID 从 13.3 急剧上升至 34.5，验证了该策略对简化动作分布的核心作用（置信度 0.95）。

### 创新二：社会可供性预测

在线设定下，反应者仅能观测到表演者的历史动作，缺乏对未来意图的信息。本工作提出**社会可供性预测**模块，在训练阶段学习从历史序列预测未来的社会可供性表示，在推理阶段使反应者能够基于“想象的未来”进行规划，从而克服信息短视问题。该模块直接预测规范化后的可供性表示，而非原始运动，进一步利用了规范化带来的分布简化优势。

**与基线的关键差异**：基线方法（如 **InterFormer** (Chopin et al., TMM 2023)、**InterGen-revised** (Liang et al., arXiv 2023)）仅使用历史观测到的动作序列作为输入，而本方法将时间信息范围扩展为“历史观测 + 预测的未来动作序列”，使反应者具备前瞻性规划能力。

### 方法谱系与知识库定位

本工作在运动生成与交互建模的交叉点上做出了以下贡献：

- **相对于人体运动预测方法**：**Progressively Generating Better Initial Guesses** (Ma et al., CVPR 2022) 和 **HumanMAC** (Chen et al., arXiv 2023) 等方法专注于单人或多人运动预测，但未涉及反应生成任务，且缺乏对社会可供性的显式建模。本工作首次将可供性概念引入反应合成，并通过规范化与预测实现了从“预测”到“反应”的跨越。

- **相对于交互生成方法**：**InterFormer** 和 **InterGen-revised** 采用时空注意力或扩散模型生成交互动作，但在线设定下性能受限。本工作通过等变局部框架规范化（而非全局坐标）和社会可供性预测（而非仅历史信息），在三个数据集上全面超越这些基线（Table 2）。

- **核心改变槽位总结**：

| 改变槽位 | 基线值 | 本方法值 |
|---------|--------|---------|
| 坐标框架 | 全局坐标系下的关节位置与速度 | 载体局部等变规范化框架 |
| 时间信息范围 | 仅历史观测到的动作序列 | 历史观测 + 预测的未来动作序列 |
| 交互表示方式 | 独立的关节运动表示，忽略载体角色 | 以载体为中心的社会可供性表示，统一处理有/无物体场景 |

### 技术管线的协同机制

上述两个创新并非孤立运作，而是形成协同效应：规范化简化了动作分布，使得预测模块更容易学习未来可供性的演化规律；预测模块提供的未来信息，又使规范化后的表示能够支撑更及时、更合理的反应生成。最终，规范化的完整社会可供性 $A_{cf}$ 通过 4D Transformer 自编码器直接解码为反应者动作 $\hat{s_r} = 4DNet(A_{cf})$，训练采用关节位置和速度的联合 MSE 损失。

## 整体框架

本文提出了一套面向在线全身动作反应合成的完整框架，其核心设计围绕“社会可供性”（Social Affordance）的表示、规范化与预测展开。整体流水线由五个关键模块串联构成，形成从原始表演者运动到反应者动作的端到端生成路径。

**输入与任务设定。** 系统在在线设定下运行：反应者（人形机器人）在每个时间步仅能观测到人类表演者过去时刻的动作序列，无法访问未来信息。输入包含表演者的全身关节位置与速度，以及场景中可能存在的交互物体或反应者自身的静止姿态。

**流水线模块。**
1. **社会可供性载体选择（Social Affordance Carrier Selection）。** 首先从场景中确定“可供性载体”——在人物-物体-人形机器人交互场景中，载体为真实的物体；在纯人物-人形机器人交互场景中，载体为反应者自身的静止姿态。载体的选择依据是表演者与之存在潜在接触的对象。
2. **以载体为中心的表演者表示（Carrier-centric Actor Representation）。** 以载体的点（物体）或关节（人形机器人）为参考基准，通过图神经网络（GNN）将表演者的运动编码为逐点的载体-表演者表示 $\pmb{R}^i$，如公式 $R^{i}(h^{i}, c^{i}) = \{ (x_{j}^{i}, \epsilon_{\theta}(h^{i})) \}_{j=1}^{N}$ 所示。这一表示将表演者的运动与载体的动态几何绑定，形成局部化的交互描述。
3. **社会可供性规范化（Social Affordance Canonicalization）。** 该模块是整个框架的核心创新之一。通过等变局部框架学习网络 Equiv-FrameNet，从载体几何中提取旋转等变的局部坐标系 $\mathbf{F}_l$，并将以载体为中心的表演者表示投影到该局部框架中，得到规范化后的社会可供性表示 $\pmb{A}_c^i$。规范化的目的是消除全局坐标变化带来的动作分布复杂性，使后续学习任务显著简化。
4. **社会可供性预测（Social Affordance Forecasting）。** 为克服在线设定中反应者仅能观测历史信息的短视问题，该模块基于已观测的历史序列预测未来表演者的动作，使反应者能够基于“想象的未来”进行规划。训练阶段反应者可访问表演者的完整动作序列，而在实际预测阶段仅依赖过去观测。
5. **4D Transformer 自编码器（4D Transformer Autoencoder）。** 将规范化后的完整社会可供性编码 $\pmb{A}_{cf}$ 输入 4D Transformer 网络，直接解码生成反应者的全身动作序列 $\hat{s}_r = \text{4DNet}(A_{cf})$。训练损失为关节位置与关节速度的均方误差之和：$\text{Loss} = \text{MSE}(s_r - \hat{s}_r) + \text{MSE}(ds_r - \hat{ds}_r)$。

**信息流与因果机制。** 整个框架的信息流遵循“载体选择 → 局部表示构建 → 等变规范化 → 未来预测 → 时空解码”的因果链条。其中，等变规范化通过降低动作模式的分布复杂度，是提升生成质量的关键因果旋钮——消融实验表明，移除该模块后 FID 从 13.3 骤升至 34.5（Table 4）。社会可供性预测则通过扩展有效时间视野，弥补了在线观测的信息短视瓶颈。两者协同作用，使得反应者能够在简化后的动作空间中基于更完整的时序信息进行规划，从而实现高质量、及时的反应生成。

### 补充图表

![[assets/figures/papers/paper_list_l1660_Interactive_Humanoid_Online_Full_Body_Motion_Reaction_Synthesis_with_Soc/figures/004_Figure_3.jpg]]
*Figure 3: Social Affordance Canonicalization. Given a sequence, we first select a social affordance carrier and build the carrier-centric representation. Then we can compute the social affordance representation. We propose to learn the local frame for carrier and canonicalize social affordance to simplify the distribution. Then a motion encoder and decoder are used to generate reactions*

## 核心模块与公式推导

### 模块总览

本方法由五个核心模块构成，围绕“社会可供性”（Social Affordance）的规范化与预测展开：

1. **Social Affordance Carrier Selection**：根据场景选择可供性载体——在人与物体交互场景中，载体为真实物体；在纯人人交互场景中，载体为人形机器人自身的静止姿态。
2. **Carrier-centric Actor Representation**：以载体点/关节为参考基准，通过图神经网络（GNN）编码表演者运动，形成逐点的载体-表演者局部表示。
3. **Social Affordance Canonicalization**：通过等变局部框架学习网络（Equiv-FrameNet），从载体几何中提取旋转等变的局部坐标系，将表演者运动投影至该框架以简化动作分布。
4. **Social Affordance Forecasting**：基于历史序列预测未来表演者动作，使反应者能基于“想象的未来”进行规划，克服在线设定下的信息短视问题。
5. **4D Transformer Autoencoder**：对规范化后的完整社会可供性进行编码，并通过解码器直接生成反应者全身动作序列。

---

### 载体选择与演员表示

**载体选择**（Sec 4.1）：社会可供性载体指承载交互信息的物体或人形机器人。当场景中存在物体时，选择该物体作为载体；在纯人人交互中，选择人形机器人的静止姿态关节作为载体。人形机器人反应者 $r^i$ 与表演者 $h^i$ 共享相同的骨架结构（$J$ 个关节，每个关节 $D_h$ 维表示，包含关节位置与速度）。

**以载体为中心的演员表示**（Sec 4.2, Eq (1)）：对于第 $i$ 帧，将表演者运动编码到载体的 $N$ 个点/关节上：

$$R^{i}(h^{i}, c^{i}) = \{ (x_{j}^{i}, \epsilon_{\theta}(h^{i})) \}_{j=1}^{N}$$

其中：
- $x_{j}^{i}$ 为载体上第 $j$ 个点的空间位置；
- $\epsilon_{\theta}(h^{i})$ 为通过 GNN 编码的表演者运动特征，该特征以载体点 $j$ 为中心聚合邻域信息；
- 最终形成 $N$ 组（载体点位置，表演者编码）对，构成该帧的载体-表演者表示。

---

### 社会可供性表示与规范化

**社会可供性表示**（Sec 4.2, Eq (2)）：将截至时间步 $i$ 的所有载体-表演者表示聚合，形成社会可供性：

$$\pmb{A}^{i} = \{ \pmb{R}^{t} \}_{t=1}^{i} = \{ \{ (\pmb{x}_{j}^{t}, \pmb{\epsilon}_{\theta}(h_{j}^{t})) \}_{j=1}^{N} \}_{t=1}^{i}$$

这一表示同时编码了表演者的运动历史、载体的动态几何，以及二者的空间关系。

**等变局部框架学习**（Sec 4.3, Eq (5)）：为降低表演者动作模式在全局坐标系下的高度多样性，引入 Equiv-FrameNet 从载体几何中学习旋转等变的局部框架：

$$\mathbf{F}_{l} \gets \mathrm{Equiv\text{-}FrameNet}(c, H_{in}, \mathbf{V}_{in})$$

其中 $c$ 为载体几何，$H_{in}$ 和 $\mathbf{V}_{in}$ 分别为输入特征与方向向量。该网络输出一组局部正交框架 $\mathbf{F}_{l}$，满足对载体旋转的等变性——当载体旋转时，框架同步旋转，从而保证投影后的表示具有旋转不变性。

**规范化表示**（Sec 4.3）：将表演者运动投影到学习到的局部框架后，得到规范化的载体-演员表示和社会可供性表示 $A_{c}^{i}$。这一规范化策略的核心作用在消融实验中得到了充分验证：移除规范化模块后，HHI 数据集上的 FID 从 13.3 急剧上升至 34.5（Table 4），表明动作分布简化对生成质量至关重要。

---

### 社会可供性预测

在线反应合成的核心瓶颈在于：预测阶段反应者仅能观测表演者的过去动作（Figure 4 右），而训练阶段可访问完整序列（Figure 4 左）。为解决这一信息不对称，引入社会可供性预测模块（Sec 4.4）：

![[assets/figures/papers/paper_list_l1660_Interactive_Humanoid_Online_Full_Body_Motion_Reaction_Synthesis_with_Soc/figures/005_Figure_4.jpg]]
*Figure 4: Social Affordance Forecasting. At the training stage, the humanoid reactor can access all motions of the actor. At the prediction stage in the real world, the humanoid reactor can only observe the past motions of the human actor. The forecasting module can anticipate the motions that the human will take*

- 训练时，基于前 $i$ 帧历史预测未来 $K$ 帧的表演者动作，并与真实未来动作计算监督损失；
- 推理时，将预测的未来动作与历史观测拼接，构建“完整”的社会可供性 $A_{cf}$，使反应者能基于想象的未来进行规划。

---

### 反应生成与训练损失

**4D Transformer 生成**（Sec 4.5, Eq (9)）：将规范化并预测补全的社会可供性 $A_{cf}$ 输入 4D Transformer 网络，直接输出反应者的动作序列：

$$\hat{s_r} = 4DNet(A_{cf})$$

该网络同时处理空间（关节间关系）和时间（帧间依赖）两个维度的信息。

**训练损失**（Eq (10)）：采用关节位置与关节速度的联合均方误差损失：

$$Loss = MSE(s_r - \hat{s_r}) + MSE(ds_r - \hat{ds_r})$$

其中 $s_r$ 为真实反应动作，$ds_r$ 为真实关节速度，$\hat{s_r}$ 和 $\hat{ds_r}$ 为对应的预测值。同时约束位置和速度有助于生成更平滑、物理上更合理的动作序列。

### 补充图表

![[assets/figures/papers/paper_list_l1660_Interactive_Humanoid_Online_Full_Body_Motion_Reaction_Synthesis_with_Soc/figures/012_Figure_8.jpg]]
*Figure 8: Visualization results of learned local frame. The local frames are roughly consistent across different chairs*

## 实验与分析

### 实验设置

为验证所提方法的有效性，作者在**四个数据集**上进行了全面评估，包括自建的 **HHI** 和 **CoChair** 数据集，以及公开的 **InterHuman** 和 **Chi3D** 数据集。HHI 是首个大规模全身动作反应数据集，具备明确的动作反馈；CoChair 则是首个大规模多人-物体交互数据集（见 Table 1 对比）。所有实验均在**在线设定**下进行，即反应者只能访问表演者的历史动作信息，确保了比较的公平性。

![[assets/figures/papers/paper_list_l1660_Interactive_Humanoid_Online_Full_Body_Motion_Reaction_Synthesis_with_Soc/figures/003_Table_1.jpg]]
*Table 1: Dataset comparisons. We compare our iHuman dataset with existing multi-human interaction datasets. Object refers to human-object-human interaction. Whole-body refers to wholebody motion capture. Actor&Reactor refers to whether there is an obvious initiator of the action. Motions is the total number of motion clips. Verbs is the number of interaction categories. Duration refers to the total time of each dataset*

评估指标涵盖生成质量与物理合理性：采用 **FID（Fréchet Inception Distance）** 衡量生成动作分布与真实分布的差异，同时引入**穿透深度（Penetration depth）** 评估 CoChair 场景中人-物交互的物理合理性，并通过用户偏好研究（User Preference）进行主观评价。

对比基线包括：
- **Progressively Generating Better Initial Guesses**（Ma et al., CVPR 2022）：基于时空密集图卷积的运动预测方法；
- **InterFormer**（Chopin et al., TMM 2023）：基于时空注意力的交互 Transformer；
- **InterGen-revised**（Liang et al., arXiv 2023）：基于扩散模型的多人交互生成方法，将原 CLIP 分支替换为时空 Transformer 以编码表演者动作；
- **Spatio-temporal Transformer**：基于 Transformer 的时空运动预测基线；
- **HumanMAC**（Chen et al., arXiv 2023）：基于掩码运动补全的运动预测方法。

### 主实验结果

#### 人-人交互场景

Table 2 展示了在 HHI、InterHuman 和 Chi3D 三个数据集上的定量结果。**本方法在所有指标上均一致优于现有最佳基线**：

![[assets/figures/papers/paper_list_l1660_Interactive_Humanoid_Online_Full_Body_Motion_Reaction_Synthesis_with_Soc/figures/006_Table_2.jpg]]
*Table 2: Quantitative results on HHI, InterHuman, and Chi3D. Our method consistently outperforms the previous method in all metrics*

- 在 HHI 上，FID 达到 **13.3**，用户偏好率 **67.2%**；
- 在 InterHuman 上，FID 达到 **14.7**，用户偏好率 **50.6%**；
- 在 Chi3D 上，FID 达到 **12.8**，用户偏好率 **44.2%**。

定性可视化（Figure 6、Figure 7）进一步表明，本方法能生成**更及时的反应动作**，并更好地捕捉手部运动细节。

![[assets/figures/papers/paper_list_l1660_Interactive_Humanoid_Online_Full_Body_Motion_Reaction_Synthesis_with_Soc/figures/009_Figure_6.jpg]]
*Figure 6: Visualization results on HHI. Our method can generate more prompt reactions and can better capture hand motion*

![[assets/figures/papers/paper_list_l1660_Interactive_Humanoid_Online_Full_Body_Motion_Reaction_Synthesis_with_Soc/figures/010_Figure_7.jpg]]
*Figure 7: Visualization gallery of our method on InterHuman (left) and Chi3D(right). The deep black one is generated by our method*

#### 人-物-人交互场景

Table 3 报告了 CoChair 数据集上的定量结果。本方法在 FID 和穿透深度两个指标上均取得最优：
- FID 为 **7.8**；
- 穿透深度仅为 **0.9**。

![[assets/figures/papers/paper_list_l1660_Interactive_Humanoid_Online_Full_Body_Motion_Reaction_Synthesis_with_Soc/figures/008_Table_3.jpg]]
*Table 3: Quantitative results on CoChair dataset*

Figure 5 的定性结果显示，本方法能够生成**更合理的抓握动作**，并与人类表演者实现更好的协作。

![[assets/figures/papers/paper_list_l1660_Interactive_Humanoid_Online_Full_Body_Motion_Reaction_Synthesis_with_Soc/figures/007_Figure_5.jpg]]
*Figure 5: Visualization results on CoChair. Our method can provide a more reasonable grasp and better collaboration with the human actor*

### 消融实验

Table 4 的消融研究验证了各设计组件的必要性。其中**最关键的发现**是：

- **移除社会可供性规范化模块**后，FID 从 13.3 急剧上升至 **34.5**，充分验证了通过等变局部框架对社会可供性进行规范化以简化动作分布的核心作用；
- 移除社会可供性预测模块同样导致性能显著下降，证实了基于想象未来进行规划对克服在线短视问题的必要性。

### 计算效率

Table 5 显示，本方法的参数量显著低于对比基线，且能够实现约 **25 FPS** 的实时推理，满足人形机器人在线交互的实时性需求。

![[assets/figures/papers/paper_list_l1660_Interactive_Humanoid_Online_Full_Body_Motion_Reaction_Synthesis_with_Soc/figures/015_Table_5.jpg]]
*Table 5: Our method is significantly more lightweight and can achieve real-time inference at approximately 25 FPS*

### 关键图表结论

- **Table 2/Table 3**：本方法在全部四个数据集、所有评估指标上一致超越现有方法，建立了新的基准；
- **Table 4**：规范化模块是性能的核心支柱，移除后 FID 恶化超 2.5 倍；
- **Figure 8**：学习到的局部框架在不同椅子之间大致保持一致，验证了等变框架学习的泛化能力；
- **Figure 5/Figure 6**：定性结果直观展示了本方法在反应及时性、手部动作捕捉和物体抓握合理性方面的优势。

### 补充图表

![[assets/figures/papers/paper_list_l1660_Interactive_Humanoid_Online_Full_Body_Motion_Reaction_Synthesis_with_Soc/figures/011_Table.jpg]]

![[assets/figures/papers/paper_list_l1660_Interactive_Humanoid_Online_Full_Body_Motion_Reaction_Synthesis_with_Soc/figures/013_Figure_9.jpg]]
*Figure 9: Visualization results of Motion Forecasting with object(left) and without object(right)*

## 方法谱系与知识库定位

### 与现有基线的结构性差异

本工作（Social Affordance Canonicalization and Forecasting）与现有方法的本质差异体现在三个关键设计槽位上，这些差异直接回应了在线反应合成任务中的核心瓶颈。

**坐标框架的选择。** 传统方法——包括基于时空密集图卷积的运动预测方法 **Progressively Generating Better Initial Guesses**（Ma et al., CVPR 2022）、基于时空注意力的交互Transformer **InterFormer**（Chopin et al., TMM 2023）、以及基于扩散模型的多人交互生成方法 **InterGen-revised**（Liang et al., arXiv 2023）——均在全局坐标系下编码关节位置与速度。这种全局表示导致同一交互动作在不同空间位置和朝向下呈现截然不同的特征分布，显著增加了学习难度。本方法通过等变局部框架学习（Equiv-FrameNet，见 Eq (5)），将表演者运动投影到以载体为中心的局部规范化框架中，从根本上简化了动作分布。消融实验提供了决定性证据：移除规范化模块后，FID 从 13.3 急剧上升至 34.5（Table 4），证实该设计是方法性能的关键支柱。

**时间信息范围。** 现有基线在在线设定下仅能利用历史观测到的动作序列进行反应生成，这种信息短视（myopia）导致反应者无法预判表演者的未来意图，尤其在高动态交互场景中容易产生延迟或不协调的反应。本方法引入社会可供性预测模块（Social Affordance Forecasting，见 Sec 4.4, Fig 4），在训练阶段学习从历史序列预测未来表演者动作，使反应者能够基于"想象的未来"进行规划。这一设计将反应生成从纯粹的被动响应提升为具备前摄性的交互规划。

**交互表示方式。** 现有方法通常将表演者与反应者的运动视为独立的关节序列，忽略了交互中载体（物体或人形机器人）的结构性角色。本方法提出以载体为中心的社会可供性表示（见 Sec 4.2, Eq (1)(2)），通过图神经网络将表演者运动编码为相对于载体点/关节的逐点表示，统一处理有物体和无物体的交互场景。这种表示不仅捕捉了表演者-载体之间的空间关系，还为后续的规范化和预测提供了结构化基础。

### 方法适用边界与局限

本方法在以下条件下展现出显著优势：(1) 交互场景中存在明确的"可供性载体"——无论是实物物体（如 CoChair 数据集中的椅子）还是处于静止姿态的反应者自身（如 HHI 数据集）；(2) 表演者的动作具有可预测的时间结构，使得社会可供性预测模块能够有效发挥作用。

然而，当前验证分析中未提供明确的方法局限性说明，以下边界判断需结合方法论逻辑进行审慎推断。首先，载体选择的鲁棒性是一个潜在薄弱点：当交互中不存在明显的物理载体，或表演者与多个物体同时交互时，单一载体选择策略可能不足以充分表征社会可供性。其次，等变局部框架的学习依赖于载体几何的稳定性；若载体自身发生剧烈形变或快速运动，框架的等变性可能受到挑战。此外，社会可供性预测模块在长时域预测中可能累积误差，其预测精度对反应质量的影响程度尚未在消融实验中单独量化。这些边界条件需要进一步的实验验证。

### 在知识库中的定位

从方法谱系来看，本工作处于**交互运动生成**与**可供性感知的具身智能**的交叉地带。与纯运动预测方法（如 **Spatio-temporal Transformer**、**HumanMAC**（Chen et al., arXiv 2023））相比，本工作不仅预测运动，还建模了交互中的社会可供性结构。与基于扩散模型的交互生成方法（如 InterGen-revised）相比，本工作通过规范化和预测机制，在在线设定下实现了更高效的推理——Table 5 显示方法参数量显著更小，可达到约 25 FPS 的实时推理。

### 开放问题

当前验证分析中未提取到明确的开放问题。基于方法设计逻辑，以下问题值得关注：(1) 社会可供性规范化框架能否推广到更多样化的载体类型（如可变形物体、移动平台）？(2) 预测模块的误差传播对反应质量的影响是否需要显式的不确定性建模？(3) 该方法在真实人形机器人平台上的部署效果如何，仿真到现实的迁移差距有多大？这些问题需要在后续研究中加以探索。

## 原文 PDF

![[paperPDFs/3DV_2025/Interactive_Humanoid_Online_Full_Body_Motion_Reaction_Synthesis_with_Social_Affordance_Canonicalization_and_Forecasting.pdf]]