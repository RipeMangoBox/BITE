---
title: "Uni-Inter: Unifying 3D Human Motion Synthesis Across Diverse Interaction Contexts"
type: paper
paper_level: A
venue: arXiv
year: 2025
pdf_ref: paperPDFs/arxiv_2025/Uni_Inter_Unifying_3D_Human_Motion_Synthesis_Across_Diverse_Interaction_Contexts.pdf
project_link: null
code_link: null
aliases:
- UI
- Uni-Inter
tags:
- arxiv_2025
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
core_operator: 引入统一交互体积（UIV）将人、物体、场景编码为共享的体素语义占据场，并将运动生成转化为UIV上的关节级空间概率分布预测，从而以统一表示驱动任意交互组合的运动合成。
primary_logic: 通过体素化语义占据场统一异构交互实体，并以空间分布估计的形式在体积中推理运动，模型能够捕捉细粒度空间依赖，实现跨任务的泛化和上下文一致的运动生成。
claims:
- 移除UIV统一表示会一致降低所有交互任务的运动质量（HOI FID从0.51升至0.54，HSI FID从2.650升至3.517，HHI FID从2.216升至2.247）。
- "将空间概率分布输出替换为直接回归运动学参数会导致FID灾难性升高（HOI: 179.50, HSI: 66.003, HHI: 6170.243），验证了分布形式对空间推理的关键作用。"
- 在三个基准上Uni-Inter均优于领域特定SOTA（例如人-物交互FID 0.51 vs CHOIS 0.69，人-场景交互FID 2.650 vs Trumans 13.290），证明统一框架的有效性。
- FullBodyManipulation (Human-Object Interaction) 上 FID = 0.51
---

# Uni-Inter: Unifying 3D Human Motion Synthesis Across Diverse Interaction Contexts

> [!tip] 核心洞察
> 通过体素化语义占据场统一异构交互实体，并以空间分布估计的形式在体积中推理运动，模型能够捕捉细粒度空间依赖，实现跨任务的泛化和上下文一致的运动生成。

| 字段 | 内容 |
|------|------|
| 中文题名 | Uni-Inter：统一多样化交互上下文下的三维人体运动合成 |
| 英文题名 | Uni-Inter: Unifying 3D Human Motion Synthesis Across Diverse Interaction Contexts |
| 会议/期刊 | arXiv 2025 |
| Links |  [paper](https://doi.org/10.1145/3757377.3763954)|
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction |
| Method | Uni-Inter |
| Dataset | FullBodyManipulation, TRUMANS, NTU120-AS |

> [!tip] 效果简介
> - FullBodyManipulation (Human-Object Interaction) 上，FID 0.51 vs 0.69 (CHOIS) (-0.18 (26% reduction))；MPJPE (cm) 12.15 vs 15.30 (CHOIS) (-3.15 (20.6% reduction))。
> - TRUMANS (Human-Scene Interaction) 上，FID 2.650 vs 13.290 (Trumans) (-10.640 (80.0% reduction))；Goal Dist. (cm) 20.136 vs 25.434 (Trumans) (-5.298 (20.8% improvement))。
> - NTU120-AS (Human-Human Interaction) 上，FID 2.216 vs 3.045 (ReGenNet) (-0.829 (27.2% reduction))。

## 概要

三维人体运动合成在数字人、具身智能和混合现实中具有核心地位，但现有方法普遍采用**任务特定架构与异构表示**——人体用骨架、物体用点云、场景用占据网格——导致模型无法统一处理人-人、人-物、人-场景乃至复合交互。随着交互场景日趋复杂，这种“一个任务一个模型”的范式暴露出跨任务泛化能力弱的根本瓶颈。

针对上述问题，本文提出 **Uni-Inter**，一个面向复合交互运动生成的统一多任务框架，发表于 SIGGRAPH Asia 2025。其核心思路是引入**统一交互体积（Unified Interactive Volume, UIV）**，将人、物体、场景三类异构实体编码为共享的体素语义占据场，并将运动生成转化为 UIV 上的关节级空间概率分布预测。这一设计使得模型能够以单一表示驱动任意交互组合的运动合成，从根本上打破了任务特定架构的限制。

实验在三个代表性基准上验证了方法的有效性。在人-物交互任务（FullBodyManipulation）上，Uni-Inter 的 FID 达到 0.51，较 **CHOIS**（Li et al., ECCV 2024）的 0.69 降低 26%；在人-场景交互任务（TRUMANS）上，FID 为 2.650，远优于 **Trumans**（Jiang et al., CVPR 2024）的 13.290；在人-人交互任务（NTU120-AS）上，FID 为 2.216，相比 **ReGenNet**（Xu et al., CVPR 2024）降低 27.2%。消融实验进一步揭示了两个关键因果机制：移除 UIV 统一表示会一致地恶化所有任务的运动质量，而将空间概率分布替换为直接回归运动学参数则导致 FID 灾难性升高（HOI: 179.50, HSI: 66.003, HHI: 6170.243），表明分布形式的输出对于学习细粒度空间依赖是不可替代的。

**方法定位**：Uni-Inter 属于扩散模型驱动的运动生成方法，其独特之处在于以体素化语义占据场统一异构交互实体，并通过空间分布估计在体积中推理运动，实现了从任务特定建模到统一交互建模的范式转变。



三维人体运动合成是计算机图形学与视觉领域的核心问题，其目标是根据给定的控制信号生成自然、逼真的人体动作序列。随着数字人、虚拟现实和具身智能的发展，交互场景下的运动生成——即人体需要与物体、场景或其他人进行物理协作——成为关键挑战。然而，现实世界中的交互往往是复合的：一个人可能同时手持物体、行走于室内场景并与他人互动。这种复合交互要求模型能够同时理解人、物体、场景三类异构实体的空间关系与语义约束。

现有方法在这一问题上存在根本性架构瓶颈。如 **Figure 2** 所示，当前主流方案采用**任务特定架构**，针对人-物交互（HOI）、人-场景交互（HSI）、人-人交互（HHI）分别设计独立的模型与表示：人体通常用骨架关节表示，物体用点云编码，场景则依赖占据网格。这种异构表示体系导致三个直接后果：

1. **表示不可融合**：不同任务的实体编码无法在同一空间中统一处理，模型无法在复合交互场景下建立跨实体类型的空间关联。
2. **泛化能力弱**：任务特定模型只能处理训练时见过的交互组合，面对“人+物+场景”等复合输入时缺乏零样本泛化能力。
3. **空间推理粗糙**：直接回归关节坐标或运动学参数的方式难以捕捉精细的空间依赖关系，尤其在需要精确接触（如手部抓取物体、脚部接触地面）的场景中表现不佳。

从因果机制角度看，核心瓶颈在于：**现有方法缺乏一个统一的交互空间表示，使得异构实体能够在同一坐标系下被编码，并且运动生成过程能够在该空间中显式地进行空间分布推理**。这构成了本文的核心动机——能否设计一种统一的表示与生成范式，使得单一模型能够处理人、物体、场景的任意组合交互，并在所有任务上保持或超越领域特定SOTA的性能？



## 核心方法与创新机理

Uni-Inter的核心创新在于通过**统一交互体积（Unified Interactive Volume, UIV）**将异构的交互实体（人体、物体、场景）编码为共享的体素语义占据场，并将运动生成转化为该体积上的**关节级空间概率分布预测**，从而以单一模型统一处理人-人、人-物、人-场景及任意复合交互任务。这一设计从根本上改变了现有方法的两个关键环节：

### 从任务特定表示到统一交互体积

现有方法为不同交互类型维护独立的表示形式——人体使用骨架关节、物体使用点云、场景使用占据网格——导致无法在统一框架内建模复合交互（Figure 2）。Uni-Inter提出的UIV将所有交互实体映射到一个共享的三维语义占据场中，通过one-hot通道标记实体类型（人体 $c_h=[1,0,0]$，物体 $c_o=[0,1,0]$，场景 $c_s=[0,0,1]$），使得任意组合的人、物、场景能够被统一编码为条件输入（Section 4.1）。

这一表示层面的统一是跨任务泛化的基础。消融实验表明，移除UIV统一表示会导致所有交互任务的运动质量一致下降：人-物交互FID从0.51升至0.54，人-场景交互FID从2.650升至3.517，人-人交互FID从2.216升至2.247（Table 4-6），验证了共享体积表示对跨任务泛化的关键贡献。

### 从直接回归运动学到空间概率分布推理

传统方法直接回归关节旋转角或坐标等运动学参数，这种方式在复杂交互场景中难以捕捉细粒度的空间依赖关系。Uni-Inter将运动生成重新表述为：在UIV上为每个关节预测体素级的空间概率分布，并通过计算分布的一阶矩（期望）获得连续关节位置：

$$\hat{j}_t^k = \mathbb{E}_{\hat{\mathcal{P}}_t^k}[u] = \int_{u \in S} \hat{\mathcal{P}}_t^k(u) \cdot u \, du$$

这种概率化输出形式使模型能够在体积空间中显式推理关节位置的不确定性和空间关系，实现亚体素精度的定位（Section 4.2, Eq. 6-7）。消融实验提供了决定性证据：将空间概率分布替换为直接回归运动学参数（w/o space dist.）会导致FID灾难性升高——人-物交互升至179.50，人-场景交互升至66.003，人-人交互升至6170.243（Table 4-6），证明空间分布形式对于学习交互结构是不可替代的。

### 配套的UIV对齐正则化

为充分发挥UIV表示和空间分布输出的协同作用，Uni-Inter设计了多损失项联合监督框架，包括位置损失 $\mathcal{L}_{pos}$、速度损失 $\mathcal{L}_{vel}$、骨架一致性损失 $\mathcal{L}_{sk}$ 和方向损失 $\mathcal{L}_{ori}$，总目标为：

$$\mathcal{L} = \mathcal{L}_{rec} + \lambda_1 \cdot \mathcal{L}_{pos} + \lambda_2 \cdot \mathcal{L}_{vel} + \lambda_3 \cdot \mathcal{L}_{sk} + \lambda_4 \cdot \mathcal{L}_{ori}$$

其中 $\lambda_1=\lambda_2=\lambda_3=0.1$, $\lambda_4=1$（Section 4.2, Eq. 13）。各损失项具有互补作用：去除骨架一致性损失使人-物交互C-F1从0.86显著降至0.68，去除速度损失使C-F1降至0.67，去除方向损失使HOI FID升至0.67（Table 7-9）。

### 统一框架的跨任务优势

基于上述创新，Uni-Inter在三个基准上均超越了领域特定SOTA方法（Table 1-3）：
- **人-物交互**（FullBodyManipulation）：FID 0.51 vs CHOIS 0.69，MPJPE降低20.6%
- **人-场景交互**（TRUMANS）：FID 2.650 vs Trumans 13.290，目标距离改善20.8%
- **人-人交互**（NTU120-AS）：FID 2.216 vs ReGenNet 3.045，Diversity 22.169 vs 21.925

该结果表明，通过统一表示和空间概率推理这两个核心changed slots，Uni-Inter不仅消除了任务特定架构的冗余，还实现了跨任务的一致性能提升。



Uni-Inter 的整体设计围绕一个核心洞察展开：**通过体素化语义占据场统一异构交互实体，并以空间分布估计的形式在体积中推理运动**，从而以单一模型支撑人-人、人-物、人-场景及其任意复合交互的运动生成。

### 输入输出流

框架接收三类异构输入：
1. **交互实体**：人体骨架、物体点云、场景占据网格，以任意组合形式提供。
2. **条件信号**：文本描述（经 CLIP 编码）作为语义条件。
3. **目标输出**：生成的人体运动序列，以关节级空间概率分布的形式在统一交互体积（UIV）上逐帧预测。

### 核心模块与数据流

整个 pipeline 由五个关键模块串联构成，数据流如下：

**① 统一交互体积（UIV）编码器**
首先将所有人、物体、场景实体分别转化为语义占据体素，每个体素携带 one-hot 实体类型通道（人体 $c_h=[1,0,0]$，物体 $c_o=[0,1,0]$，场景 $c_s=[0,0,1]$），然后聚合为共享的 UIV 体积 $\Omega = \{\mathcal{V}_t\}_{t=1}^{T}$。这一步将任务特定的异构表示统一为单一空间场，是整个框架的表示瓶颈。

**② 金字塔特征提取器（FPN）**
在 UIV 上构建多尺度特征金字塔，提取不同粒度的空间-语义特征，用于后续层次化特征注入。

**③ 扩散去噪网络**
以文本嵌入和 UIV 多尺度特征作为条件，从高斯噪声出发，通过迭代去噪逐步生成输出分布张量 $P = \{\mathcal{P}_t^k\}_{k,t} \in \mathbb{R}^{T \times H \times W \times D \times K}$。扩散过程采用直接回归清晰运动 $x_0$ 的参数化策略，反向步骤为：

$$P_{\theta}(x_{i-1}|x_i) = \mathcal{N}(\mu_i(\theta), \sigma_i^2 I)$$

**④ 关节级空间分布头**
将去噪网络的输出建模为每个关节 $k$ 在每帧 $t$ 占据 UIV 体素 $u$ 的概率分布。训练时以真实关节位置为中心的各向同性高斯分布作为目标：

$$\mathcal{P}_t^k(u) = \frac{1}{(2\pi\sigma^2)^{3/2}} \exp\left(-\frac{\|u - j_t^k\|_2^2}{2\sigma^2}\right)$$

推理时通过计算预测分布的一阶矩获得连续关节位置，实现亚体素精度定位：

$$\hat{j}_t^k = \mathbb{E}_{\hat{\mathcal{P}}_t^k}[u] = \int_{u \in S} \hat{\mathcal{P}}_t^k(u) \cdot u \, du$$

**⑤ 多损失端到端训练**
总损失函数组合了重建损失、位置损失、速度损失、骨架一致性损失和朝向损失：

$$\mathcal{L} = \mathcal{L}_{rec} + \lambda_1 \cdot \mathcal{L}_{pos} + \lambda_2 \cdot \mathcal{L}_{vel} + \lambda_3 \cdot \mathcal{L}_{sk} + \lambda_4 \cdot \mathcal{L}_{ori}$$

其中 $\lambda_1=\lambda_2=\lambda_3=0.1$，$\lambda_4=1$。各损失项互补：骨架一致性损失 $\mathcal{L}_{sk}$ 确保生成运动符合人体骨骼刚性约束，速度损失 $\mathcal{L}_{vel}$ 保证时序平滑性，朝向损失 $\mathcal{L}_{ori}$ 约束初始身体朝向。

### 关键设计选择

框架的两个关键设计选择在消融实验中得到严格验证：

- **UIV 统一表示**：移除 UIV 统一表示（即回退到任务特定编码）在所有交互任务上一致导致 FID 恶化（HOI: 0.51→0.54；HSI: 2.650→3.517；HHI: 2.216→2.247），验证了共享体积表示对跨任务泛化的贡献。
- **空间概率分布输出**：将空间分布头替换为直接回归运动学参数会造成灾难性 FID 上升（HOI: 179.50；HSI: 66.003；HHI: 6170.243），证明分布形式对于学习细粒度空间交互结构是不可替代的。

### 训练策略

训练采用三个交互数据集（FullBodyManipulation、TRUMANS、NTU120-AS）以 1:1:1 等量混合的策略，确保各任务公平参与训练，避免任务偏斜。

### 补充图表

![[assets/figures/papers/paper_list_l1698_Uni_Inter_Unifying_3D_Human_Motion_Synthesis_Across_Diverse_Interaction/figures/002_Figure_2.jpg]]
*Figure 2: Different paradigms for compound interaction motion generation. (a) Existing methods rely on task-specific architectures, resulting in separately modeling when handling compound interactions involving multiple entity types. (b) In contrast, Uni-Inter provides a unified motion generation framework that seamlessly supports arbitrary combinations of interactive entities—including humans, objects, and scenes—within a single model*

![[assets/figures/papers/paper_list_l1698_Uni_Inter_Unifying_3D_Human_Motion_Synthesis_Across_Diverse_Interaction/figures/003_Figure_3.jpg]]
*Figure 3: (a) Uni-Inter supports arbitrary combinations of interactive entities as input and generates corresponding interaction motions. This is enabled by the Unified Interactive Volume (UIV) representation and UIV-aligned regularization. Each interaction entity—whether human, object, or scene—is first encoded as a semantic occupancy grid in the interaction space and then merged into the*



Uni-Inter 的核心架构围绕两个关键设计展开：**统一交互体积（UIV）** 将异构交互实体编码为共享空间场，以及**关节级空间概率分布**在该体积上推理运动。以下按模块逐一拆解。

### 统一交互体积（UIV）编码器

UIV 的核心思想是将人体、物体、场景三类异构实体统一映射到一个共享的三维语义占据场中。对于每个时间步 $t$，体素 $u$ 的语义占据映射定义为：

$$\phi_t(u) = \sum_{c \in C} \mathcal{I}_c(u, t) \cdot c$$

其中 $c$ 为实体类型的 one-hot 通道标识：人体 $c_h = [1,0,0]$，物体 $c_o = [0,1,0]$，场景 $c_s = [0,0,1]$。$\mathcal{I}_c(u,t)$ 为指示函数，当体素 $u$ 在时间 $t$ 被类型 $c$ 的实体占据时取 1，否则为 0。所有时间步的占据体素集合聚合为统一交互体积：

$$\Omega = \{\mathcal{V}_t\}_{t=1}^{T}$$

这一设计使得不同交互任务（人-物、人-场景、人-人）共享同一表示空间，消除了任务特定架构对异构表示（骨架、点云、占据网格）的依赖。消融实验表明，移除 UIV 统一表示后，三个任务的 FID 均一致恶化（HOI: 0.51→0.54; HSI: 2.650→3.517; HHI: 2.216→2.247），验证了共享体积表示对跨任务泛化的关键作用。

### 金字塔特征提取器（FPN）

在 UIV 之上，模型采用金字塔结构特征提取器（FPN, Lin et al. 2017）提取多尺度空间特征。该模块将不同分辨率下的 UIV 特征注入扩散去噪网络，实现层次化特征融合，使模型能够同时捕获粗粒度的全局交互布局和细粒度的局部接触关系。

### 扩散去噪网络

运动生成采用扩散架构，以文本嵌入（CLIP）和 UIV 多尺度特征作为条件输入。扩散过程的反向去噪步骤参数化为：

$$P_{\theta}(x_{i-1}|x_i) = \mathcal{N}(\mu_i(\theta), \sigma_i^2 I)$$

模型直接预测清晰运动 $x_0$，并使用重建损失进行监督：

$$\mathcal{L}_{rec}(x_0, x_0^*) = \|x_0 - x_0^*\|_2^2$$

其中 $x_0^*$ 为真实运动。最终输出为关节级空间分布张量 $P = \{\mathcal{P}_t^k\}_{k,t} \in \mathbb{R}^{T \times H \times W \times D \times K}$，覆盖 $T$ 帧、空间网格 $H \times W \times D$ 和 $K$ 个关节分量。

### 关节级空间分布头

与直接回归运动学参数的传统方法不同，Uni-Inter 将运动表示为 UIV 上的体素级关节概率分布。对于关节 $k$ 在时间 $t$，真实分布建模为以真实关节位置 $j_t^k$ 为中心的归一化各向同性高斯：

$$\mathcal{P}_t^k(u) = \frac{1}{(2\pi\sigma^2)^{3/2}} \exp(-\frac{\|u - j_t^k\|_2^2}{2\sigma^2})$$

预测的关节位置通过计算预测分布的一阶矩（期望）获得，实现亚体素精度的连续定位：

$$\hat{j}_t^k = \mathbb{E}_{\hat{\mathcal{P}}_t^k}[u] = \int_{u \in S} \hat{\mathcal{P}}_t^k(u) \cdot u \, du$$

这一空间分布形式对模型学习交互结构至关重要。消融实验显示，将其替换为直接回归运动学参数（w/o space dist.）会导致 FID 灾难性升高（HOI: 179.50; HSI: 66.003; HHI: 6170.243），证明分布形式对于空间推理具有不可替代的作用。

### 多损失项联合训练

总训练目标由五个损失项加权组合：

$$\mathcal{L} = \mathcal{L}_{rec} + \lambda_1 \cdot \mathcal{L}_{pos} + \lambda_2 \cdot \mathcal{L}_{vel} + \lambda_3 \cdot \mathcal{L}_{sk} + \lambda_4 \cdot \mathcal{L}_{ori}$$

其中 $\lambda_1 = \lambda_2 = \lambda_3 = 0.1$，$\lambda_4 = 1$。各损失项功能如下：

- **位置损失** $\mathcal{L}_{pos}(\hat{j}_t^k, j_t^k) = \|\hat{j}_t^k - j_t^k\|_2^2$：对预测关节位置的 L2 监督。
- **速度损失** $\mathcal{L}_{vel}$：约束帧间关节运动速度的连续性。
- **骨架一致性损失** $\mathcal{L}_{sk}$：保持人体骨骼长度在不同帧间的一致性。消融实验表明，去除 $\mathcal{L}_{sk}$ 使人-物交互 C-F1 从 0.86 骤降至 0.68，并在人-人和人-场景任务上造成 FID 剧烈升高，是该损失中对生成质量贡献最大的项。
- **方向损失** $\mathcal{L}_{ori}$：约束人体朝向与交互上下文的语义对齐，去除后 HOI FID 升至 0.67。

各损失项互补作用显著：去除速度损失 $\mathcal{L}_{vel}$ 使人-物交互 C-F1 降至 0.67，验证了运动时序平滑性对交互质量的影响。



## 实验与关键发现

### 主实验结果

Uni-Inter在三个不同的交互基准上均一致优于领域特定的SOTA方法，验证了统一框架的有效性。

**人-物交互（FullBodyManipulation）**。如Table 1所示，Uni-Inter在FID指标上达到0.51，相比CHOIS（Li et al., ECCV 2024）的0.69降低了26%；MPJPE从15.30 cm降至12.15 cm，相对改善20.6%。接触精度方面，C-F1达到0.86，表明模型在手部-物体接触的空间定位上具有显著优势。定性对比（Figure 4）进一步显示，Uni-Inter在手部动作的精细控制上明显优于CHOIS，生成的抓取和操作动作更加自然。

**人-场景交互（TRUMANS）**。如Table 2所示，Uni-Inter的FID为2.650，相比Trumans（Jiang et al., CVPR 2024）的13.290降低了80.0%，这是一个数量级的提升。目标距离（Goal Dist.）从25.434 cm降至20.136 cm，改善20.8%，表明模型能更准确地执行高层语义指令。Figure 6的定性案例揭示了关键差异：当指令为“左手”时，Trumans错误地使用右手；当关键动词为“躺下”时，Trumans完全未能执行该动作，而Uni-Inter在语义理解上展现出明显优势。

**人-人交互（NTU120-AS）**。如Table 3所示，Uni-Inter的FID为2.216，相比ReGenNet（Xu et al., CVPR 2024）的3.045降低了27.2%；Diversity达到22.169，略高于ReGenNet的21.925，表明统一建模并未牺牲生成多样性。Figure 5的定性结果展示了Uni-Inter在交互事件的空间对齐上更优，生成的互动动作更符合上下文一致性。

**复合交互生成**。得益于UIV对人、物、场景的统一建模，Uni-Inter能够在任意实体组合下生成高质量运动（Figure 7），这是任务特定方法无法直接支持的场景。

### 消融实验

消融实验从两个核心设计维度展开：统一交互体积（UIV）的必要性，以及空间概率分布输出的不可替代性。

**UIV统一表示的作用**。在三个任务上分别移除UIV统一表示（w/o unified），均导致性能一致退化：HOI FID从0.51升至0.54（Table 4），HSI FID从2.650升至3.517（Table 5），HHI FID从2.216升至2.247（Table 6）。这一致性退化验证了共享体积表示对跨任务泛化的关键贡献——UIV使模型能够在统一的特征空间中学习异构实体间的空间依赖。

**空间概率分布的核心地位**。将空间概率分布输出替换为直接回归运动学参数（w/o space dist.）造成了灾难性的性能崩塌：HOI FID飙升至179.50（Table 4），HSI FID升至66.003（Table 5），HHI FID升至6170.243（Table 6）。这一结果有力地证明了，空间分布形式对于学习细粒度交互结构是不可替代的——直接的参数回归无法捕捉体素级别的空间关系。

**损失函数的互补作用**。损失项消融（Table 7-9）揭示了各损失项的互补贡献：
- 去除骨架一致性损失（$L_{sk}$）对人-物交互的接触精度影响最大，C-F1从0.86骤降至0.68（Table 7），同时在HSI和HHI任务上也造成FID显著升高（Table 8-9），表明骨骼结构约束对生成物理合理运动至关重要。
- 去除速度损失（$L_{vel}$）使HOI的C-F1降至0.67（Table 7），验证了时序平滑性对接触建模的辅助作用。
- 去除方向损失（$L_{ori}$）使HOI的FID升至0.67（Table 7），表明全局朝向监督有助于空间一致性。

![[assets/figures/papers/paper_list_l1698_Uni_Inter_Unifying_3D_Human_Motion_Synthesis_Across_Diverse_Interaction/figures/014_Table_7.jpg]]
*Table 7: Ablation study on loss terms for human-object interaction on the FullBodyManipulation dataset*

![[assets/figures/papers/paper_list_l1698_Uni_Inter_Unifying_3D_Human_Motion_Synthesis_Across_Diverse_Interaction/figures/016_Table_8.jpg]]
*Table 8: Ablation study on loss terms for human-scene interaction on the TRUMANS dataset*

### 公平性说明

实验结果在严格公平的条件下获得：所有基线均采用官方实现或提供的预训练模型，在相同数据划分上进行评估。训练采用三个数据集1:1:1等量混合策略，确保各任务公平参与训练。对于人-人交互任务采用跨被试评估协议，人-场景交互任务采用与基线相同的7:2:1数据划分。Uni-Inter以物体姿态作为条件，不显式生成物体运动序列，评估聚焦于人体运动质量，与基线在相同任务设定下进行比较。

### 失败模式与局限性

尽管Uni-Inter在各项基准上取得了显著提升，仍存在以下局限：

1. **完整观测假设**：当前模型假设所有交互实体完全可观测，不支持因果实时部分观测下的运动规划，无法直接应用于动态环境中的在线推理。
2. **物体运动生成缺失**：模型对物体运动没有生成能力，仅限于给定物体轨迹条件下生成人体运动，不能端到端地同时推理物体与人体的联合交互。
3. **静态体积空间**：UIV空间是预定义静态的，处理大规模、无界环境下的运动生成仍是一个开放问题。

### 补充图表

![[assets/figures/papers/paper_list_l1698_Uni_Inter_Unifying_3D_Human_Motion_Synthesis_Across_Diverse_Interaction/figures/004_Table_1.jpg]]
*Table 1: Quantitative comparison on the FullBodyManipulation dataset for the human-object interaction task*

![[assets/figures/papers/paper_list_l1698_Uni_Inter_Unifying_3D_Human_Motion_Synthesis_Across_Diverse_Interaction/figures/005_Table_2.jpg]]
*Table 2: Quantitative comparison on the TRUMANS dataset for the human-scene interaction task*

![[assets/figures/papers/paper_list_l1698_Uni_Inter_Unifying_3D_Human_Motion_Synthesis_Across_Diverse_Interaction/figures/006_Table_3.jpg]]
*Table 3: Quantitative comparison on the NTU120-AS dataset for the human-human interaction task*

![[assets/figures/papers/paper_list_l1698_Uni_Inter_Unifying_3D_Human_Motion_Synthesis_Across_Diverse_Interaction/figures/008_Table_4.jpg]]
*Table 4: Ablation results for human-object interaction tasks on the FullBodyManipulation dataset. ‘w/o space dist’ means directly regressing the kinematic parameters of motion*

![[assets/figures/papers/paper_list_l1698_Uni_Inter_Unifying_3D_Human_Motion_Synthesis_Across_Diverse_Interaction/figures/007_Table_5.jpg]]
*Table 5: Ablation results for human-scene interaction tasks on the TRUMANS dataset. ‘w/o space dist’ means directly regressing the kinematic parameters of motion*

![[assets/figures/papers/paper_list_l1698_Uni_Inter_Unifying_3D_Human_Motion_Synthesis_Across_Diverse_Interaction/figures/009_Table_6.jpg]]
*Table 6: Ablation results for human-human interaction tasks on the NTU120-AS dataset. ‘w/o space dist’ means directly regressing the kinematic parameters of motion*

![[assets/figures/papers/paper_list_l1698_Uni_Inter_Unifying_3D_Human_Motion_Synthesis_Across_Diverse_Interaction/figures/013_Figure_7.jpg]]
*Figure 7: Qualitative results of compound interaction generation by Uni-Inter. Thanks to the unified modeling of humans, objects, and scenes via UIV, Uni-Inter supports high-quality compound motion generation across arbitrary combinations of interactive entities. Blue person and object indicate the input conditions, while yellow-green motions represent the generated results*

![[assets/figures/papers/paper_list_l1698_Uni_Inter_Unifying_3D_Human_Motion_Synthesis_Across_Diverse_Interaction/figures/010_Figure_4.jpg]]
*Figure 4: Qualitative comparison on the Human-Object Interaction dataset. Compared to state-of-the-art method CHOIS [Li et al. 2024], Uni-Inter achieves more precise control and interaction, particularly in hand movements. The blue object represents the conditional input, while the yellow-green person shows the generated motion*



## 定位与知识库关联

### 任务建模范式的统一化演进

三维人体运动合成在交互建模方向上经历了从任务特定架构到统一表示范式的转变。现有方法通常为每种交互类型设计独立的编码策略和生成架构：**CHOIS**（Li et al., ECCV 2024）以人体骨架与物体点云分别编码来处理人-物交互，**ReGenNet**（Xu et al., CVPR 2024）通过双人骨架建模人-人交互，**Trumans**（Jiang et al., CVPR 2024）则依赖场景占据网格实现人-场景交互。这些异构表示的根本瓶颈在于无法在单一框架内处理复合交互——当场景中同时存在人、物、场景元素时，任务特定架构只能分别建模，缺乏跨实体类型的空间依赖推理能力。

Uni-Inter的核心推进在于引入**统一交互体积（UIV）**，将人、物体、场景三类实体编码为共享的三维语义占据场。这一设计使模型不再需要为不同交互类型维护独立的编码器和特征空间，而是将运动生成转化为在统一体积上的关节级空间概率分布预测。从方法谱系角度看，Uni-Inter可视为将**MDM**（Tevet et al., arXiv 2022）等通用扩散运动生成框架与**Interdiff**（Xu et al., ICCV 2023）等交互感知方法融合的尝试，但关键区别在于：Uni-Inter不是简单地将交互信息作为条件注入扩散过程，而是通过UIV将交互空间结构直接嵌入生成目标的表示空间，使空间推理成为生成过程的内在组成部分。

### 空间分布输出形式的关键地位

Uni-Inter的方法贡献中，最值得关注的是将运动输出形式从直接回归运动学参数改为预测体素级空间概率分布。消融实验提供了强证据：将空间概率分布替换为直接回归关节坐标或旋转参数后，三个任务上的FID均出现灾难性上升——人-物交互从0.51升至179.50，人-场景交互从2.650升至66.003，人-人交互从2.216升至6170.243（Table 4-6, "w/o space dist."行）。这一结果揭示了空间分布形式对于学习交互结构的不可替代性：分布估计通过期望操作（soft-argmax）获得亚体素精度的连续关节位置，同时保留了空间不确定性信息，使模型能够在体积空间中隐式推理接触约束和空间关系。

这一设计与传统运动生成方法形成鲜明对比。直接回归方法（如MDM对关节坐标的预测）在单人体运动生成中有效，但在交互场景下，关节位置与交互实体表面之间的距离关系是决定交互质量的核心因素。空间分布形式使损失函数能够直接在体积空间中施加几何约束，而无需通过前向运动学链间接传播梯度。

### 损失函数设计的互补性

Uni-Inter的训练目标由五个损失项加权组合构成：重建损失 $\mathcal{L}_{rec}$、位置损失 $\mathcal{L}_{pos}$、速度损失 $\mathcal{L}_{vel}$、骨架一致性损失 $\mathcal{L}_{sk}$ 和方向损失 $\mathcal{L}_{ori}$，权重分别为 $\lambda_1=\lambda_2=\lambda_3=0.1$，$\lambda_4=1$（Equation 13）。消融实验表明各损失项之间存在明确的互补关系：

- 移除骨架一致性损失 $\mathcal{L}_{sk}$ 后，人-物交互的接触F1（C-F1）从0.86显著降至0.68（Table 7），表明该损失对维持生成人体与交互实体之间的合理空间关系至关重要；
- 移除速度损失 $\mathcal{L}_{vel}$ 使C-F1降至0.67（Table 7），说明时序平滑性直接影响接触质量；
- 移除方向损失 $\mathcal{L}_{ori}$ 使人-物交互FID升至0.67（Table 7），验证了方向监督对运动自然度的贡献。

这种多损失协同设计反映了交互运动生成的内在复杂性：单一的重建目标无法同时保证空间精度、时序一致性和语义合理性。

### 适用边界与局限性

Uni-Inter的适用边界受以下因素约束：

**完整观测假设**：模型假设所有交互实体在生成前已完全观测，不支持因果实时部分观测下的运动规划。这意味着Uni-Inter无法直接应用于动态环境中的在线推理场景，如机器人实时避障或人机协作中的增量式运动预测。

**物体运动生成缺失**：Uni-Inter以物体姿态作为条件输入，仅生成人体运动序列，不显式生成物体运动。这一设计简化了问题空间，但也限制了模型在需要端到端联合推理物体与人体交互的场景中的应用——例如，预测人推物体时物体的位移轨迹。

**静态体积空间**：UIV的体素网格是预定义的空间范围，这限制了模型处理大规模、无界环境的能力。在开放世界场景中，交互空间的动态扩展需要更灵活的体积表示策略。

### 开放问题与后续方向

从Uni-Inter的局限性出发，若干开放问题值得关注：

1. **复合交互的泛化边界**：当前验证限于三类交互的成对组合，当交互实体数量增加（如多人+多物+动态场景）时，UIV的体素分辨率与计算开销之间的权衡将变得更加突出。统一建模方法在此类场景下的泛化边界尚未被系统探索。

2. **物理约束的整合**：UIV目前仅编码语义占据信息，不包含力、接触摩擦力等物理属性。将物理约束引入空间分布预测过程，可能进一步提升生成运动的物理合理性，但如何在扩散框架中有效整合显式物理约束仍是一个开放挑战。

3. **因果实时扩展**：将当前离线生成范式扩展至因果实时设置，需要解决部分观测下的UIV构建和增量式运动预测问题，这涉及表示学习与时序建模的深层耦合。

4. **与大规模运动基座模型的融合**：Uni-Inter的统一体积表示能否作为通用交互接口，与现有的大规模运动生成基座模型结合，实现更广泛的跨任务泛化，是一个值得探索的方向。



## 原文 PDF

![[paperPDFs/arxiv_2025/Uni_Inter_Unifying_3D_Human_Motion_Synthesis_Across_Diverse_Interaction_Contexts.pdf]]
