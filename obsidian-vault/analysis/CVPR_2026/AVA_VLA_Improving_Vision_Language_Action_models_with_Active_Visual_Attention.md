---
title: "AVA-VLA: Improving Vision-Language-Action models with Active Visual Attention"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/AVA_VLA_Improving_Vision_Language_Action_models_with_Active_Visual_Attention.pdf
project_link: "https://liauto-dsr.github.io/AVA-VLA-Page"
code_link: null
aliases:
- AV
- AVA-VLA
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: 将VLA策略学习重新表述为部分可观察马尔可夫决策过程（POMDP），引入循环状态作为历史信念的神经近似，并设计主动视觉注意力（AVA）模块，利用该状态动态调整视觉令牌的重要性，使模型能够根据历史上下文主动关注任务关键区域。
primary_logic: 通过POMDP视角构建循环状态并驱动主动视觉注意力，将历史信息压缩为可学习的潜在表示，从而将VLA转变为非马尔可夫策略，使得视觉处理不再是静态的，而是由历史信念动态指导，提升模型在顺序决策任务中的泛化和鲁棒性。
claims:
- AVA-VLA在LIBERO（多任务和单任务设置）和CALVIN ABC→D基准上均达到了最优性能，特别是在长序列任务上提升显著。
- 消融实验表明循环状态初始化和AVA模块相互补充，联合使用比单独使用任何一个模块都带来更大的性能增益，且在长视界任务中优势更明显。
- AVA模块赋予模型更强的抗视觉干扰能力（如光照、背景、物体布局变化），在LIBERO+基准上的综合表现最优。
- 在匹配训练设置下，AVA-VLA持续优于OpenVLA-OFT，且额外参数量少于总模型的1%，证明性能提升来自架构创新而非计算资源。
---

# AVA-VLA: Improving Vision-Language-Action models with Active Visual Attention

> [!tip] 核心洞察
> 通过POMDP视角构建循环状态并驱动主动视觉注意力，将历史信息压缩为可学习的潜在表示，从而将VLA转变为非马尔可夫策略，使得视觉处理不再是静态的，而是由历史信念动态指导，提升模型在顺序决策任务中的泛化和鲁棒性。

| 字段 | 内容 |
|------|------|
| 中文题名 | AVA-VLA: 通过主动视觉注意力增强视觉-语言-动作模型 |
| 英文题名 | AVA-VLA: Improving Vision-Language-Action models with Active Visual Attention |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2511.18960) · [Project](https://liauto-dsr.github.io/AVA-VLA-Page) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/image_and_video_generation |
| Method | AVA-VLA |
| Dataset | LIBERO, CALVIN ABC→D |

> [!tip] 效果简介
> - LIBERO (one policy for all 4 suites) 上，平均成功率 (Average SR %) 98.0 vs 96.8 (OpenVLA-OFT) (+1.2)。
> - LIBERO (one policy per suite) 上，平均成功率 (Average SR %) 98.2 vs 97.1 (OpenVLA-OFT) (+1.1)。
> - CALVIN ABC→D (5 consecutive tasks) 上，成功率 (Task completed in a row, 5 tasks, %) 84.1 vs 72.9 (OpenVLA-OFT) (+11.2)。

## 概要

现有视觉-语言-动作（VLA）模型普遍将机器人操作建模为马尔可夫决策过程（MDP），逐帧独立处理视觉观测，忽略了执行历史中的上下文信息。这一设计导致模型在部分可观察环境中视觉注意力被动且缺乏时间一致性，难以有效利用过往信息来指导当前决策，在长视界任务中表现受限。

针对上述瓶颈，本文提出 **AVA-VLA** 框架，将VLA策略学习重新表述为部分可观察马尔可夫决策过程（POMDP）。核心思路是引入一个循环状态作为历史信念的神经近似，并基于该状态驱动主动视觉注意力（Active Visual Attention, AVA）模块，动态调整视觉令牌的重要性权重，使模型能够根据历史上下文主动聚焦于任务关键区域。这一设计将VLA从历史无关的马尔可夫策略转变为非马尔可夫策略，视觉处理不再是静态的，而是由历史信念动态指导。

实验表明，AVA-VLA在LIBERO（多任务和单任务设置）和CALVIN ABC→D基准上均达到最优性能，尤其在长序列任务上提升显著——CALVIN连续5任务成功率从72.9%提升至84.1%（+11.2个百分点）。消融实验证实循环状态初始化与AVA模块相互补充，联合使用带来的增益超过任一模块单独使用。AVA模块还赋予模型更强的抗视觉干扰能力（光照、背景、物体布局变化），在LIBERO+基准上综合表现最优。在匹配训练设置下，AVA-VLA持续优于OpenVLA-OFT，且新增参数量不足总模型的1%，表明性能提升源于架构创新而非计算资源增加。

在方法谱系上，AVA-VLA建立在OpenVLA-OFT的基础上，与UniVLA、FLOWER、RIPT-VLA、π0等同期工作形成对比。其独特贡献在于首次从POMDP视角显式建模VLA的历史上下文依赖，并通过轻量级的AVA模块实现历史条件化的视觉注意力调制，为VLA在顺序决策任务中的泛化和鲁棒性提供了新的技术路径。

### 机器人操作中的视觉-语言-动作模型

视觉-语言-动作（VLA）模型已成为机器人操作策略学习的主流范式。这类模型通常以预训练视觉-语言模型（VLM）为骨干，将视觉观测和语言指令作为输入，直接输出机器人动作序列。其标准前向传播可形式化为：

$$\mathcal{A}^t = \mathcal{Q}(\mathbf{h}^t) = \mathcal{Q}(\mathcal{M}(\mathbf{z}_I^t, \mathbf{z}_S^t))$$

其中 $\mathbf{z}_I^t$ 和 $\mathbf{z}_S^t$ 分别为当前时间步的视觉和语言令牌，$\mathcal{M}$ 为LLM骨干，$\mathcal{Q}$ 为动作头。为进一步提升效率，主流方法（如OpenVLA-OFT）引入了并行解码机制：

$$\mathcal{A}^t = \mathcal{Q}(\mathcal{M}_{\mathrm{parallel}}(\mathbf{z}_I^t, \mathbf{z}_S^t, \mathbf{p}^t))$$

其中 $\mathbf{p}^t$ 为动作占位符嵌入，使模型能够一次性预测整个动作块（action chunk）。

### 核心瓶颈：MDP假设下的历史上下文缺失

现有VLA模型在策略学习上普遍采用马尔可夫决策过程（MDP）假设，将机器人操作建模为：

$$\bar{\mathcal{A}}^t \sim \mathcal{P}_\theta(\mathcal{A}^t \mid \mathbf{x}^t)$$

即动作预测仅依赖当前观测 $\mathbf{x}^t$，逐帧独立处理视觉输入，完全忽略历史上下文。这一设计在部分可观察环境中暴露出根本性缺陷：当任务关键信息在当前帧中被遮挡、处于视野边缘或受光照变化影响时，模型缺乏从历史观测中提取补偿信息的能力。这导致两个直接后果：

1. **视觉注意力被动且缺乏时间一致性**：模型在每一帧上独立计算注意力，无法利用过往帧中已定位的任务关键区域来指导当前帧的视觉聚焦。如Figure 1(b)所示，在“打开炉灶并放上摩卡壶”任务中，基准模型OpenVLA-OFT未能定位关键的炉灶开关，而引入历史上下文后注意力则保持稳定聚焦。

2. **长视界任务性能显著下降**：随着任务序列增长，逐帧独立决策的累积误差加剧，模型在需要多步推理和持续状态追踪的场景中表现不佳。

### 从MDP到POMDP的视角转换

针对上述瓶颈，本文提出将VLA策略学习重新表述为部分可观察马尔可夫决策过程（POMDP）。在POMDP框架下，策略不仅依赖当前观测，还需维护一个信念状态 $b^{t-1}$ 来编码历史信息：

$$\bar{\mathcal{A}}^t \sim \mathcal{P}_\theta(\mathcal{A}^t \mid \mathbf{x}^t, b^{t-1})$$

这一视角转换带来了一个关键的因果调节变量：**循环状态（recurrent state）**。通过将历史上下文压缩为可学习的潜在表示，模型得以从非马尔可夫策略的角度进行决策，使视觉处理不再是静态的逐帧响应，而是由历史信念动态指导的主动过程。

### 本文动机与贡献定位

基于上述分析，本文的动机可归纳为三个递进层次：

- **填补历史上下文缺口**：现有VLA模型在架构层面缺乏有效利用历史信息的机制，循环状态提供了一条轻量而高效的补全路径。
- **实现主动视觉注意力**：仅有历史状态不足以让模型“知道该看哪里”，需要设计专门的注意力调制模块，使历史信念能够显式地影响视觉令牌的重要性分配。
- **保持计算效率**：新增模块应在不显著增加参数量的前提下带来可观的性能增益，确保方法的实用性和可部署性。

由此，本文提出AVA-VLA框架，核心包含两个互补组件：循环状态投影模块（将前一步LLM隐藏状态映射为信念状态的神经近似）和主动视觉注意力（AVA）模块（利用该状态动态计算软权重，调制LLM所有层的视觉注意力矩阵）。据论文声明，这是首个从POMDP视角显式解决VLA历史上下文缺失问题的工作。

## 核心方法与创新机理

### 从 MDP 到 POMDP：策略学习框架的根本转变

现有 VLA 模型（如 OpenVLA-OFT）将机器人操作建模为马尔可夫决策过程（MDP），逐帧独立处理视觉观测，策略仅依赖当前输入 $x^t$ 预测动作：

$$\bar{\mathcal{A}}^t \sim \mathcal{P}_\theta(\mathcal{A}^t \mid \mathbf{x}^t)$$

这一设计在部分可观察环境中存在根本性缺陷：模型无法捕获被遮挡的物体状态、不可直接观测的环境动态以及历史交互信息，导致视觉注意力被动且缺乏时间一致性。AVA-VLA 的核心创新在于将策略学习重新表述为**部分可观察马尔可夫决策过程（POMDP）**，使动作生成同时依赖于当前观测和历史信念状态：

$$\bar{\mathcal{A}}^t \sim \mathcal{P}_\theta(\mathcal{A}^t \mid \mathbf{x}^t, b^{t-1})$$

这一框架转变是后续所有技术创新的理论基础——它使模型从“只看当前”的静态策略转变为“记住过去”的非马尔可夫策略，为长视界任务中的鲁棒决策提供了可能。

### 循环状态：历史信念的神经近似

为在 VLA 架构中实现 POMDP 策略，AVA-VLA 引入了一个**循环状态** $r^{t-1}$ 作为历史信念的神经近似。该状态通过一个轻量级 MLP 投影模块 $\mathcal{B}$ 从前一时间步 LLM 最后解码器层的隐藏状态中提取：

$$\boldsymbol{r}^{t-1} = \boldsymbol{\mathcal{B}}(\boldsymbol{h}_{M}^{t-1}) \in \mathbb{R}^{\mathrm{L}_A \times d}$$

这一设计将完整的历史交互信息压缩为可学习的潜在表示，并在两个关键位置发挥作用：（1）作为当前时间步动作占位符的初始化嵌入，替代 OpenVLA-OFT 中使用的空嵌入（全零向量）；（2）作为 AVA 模块的核心输入，驱动主动视觉注意力。循环状态的存在使得模型在每一步决策时都能“回忆”之前的执行上下文，从而在部分可观察场景中保持决策连贯性。

### AVA 模块：历史驱动的主动视觉注意力

AVA 模块是 AVA-VLA 最具辨识度的技术创新，其设计理念是：**视觉处理不应是静态的，而应由历史信念动态指导**。该模块接收当前视觉观测和循环状态，计算软注意力权重 $\omega^t$，并通过修改 LLM 所有层的注意力矩阵来动态增强或抑制视觉令牌。具体而言，AVA 模块构造调制矩阵 $U^t$：

$$\mathbf{U}_{i,j}^t = \begin{cases} 1 & i=j \text{ or } j \notin \Lambda_I \\ \omega_j^t & i \neq j \text{ and } j \in \Lambda_I \end{cases}$$

其中 $\Lambda_I$ 为视觉令牌索引集。该矩阵被注入到 LLM 自注意力计算中，使得与任务相关的视觉区域获得更高的注意力权重，而无关背景被抑制。与标准自注意力机制的关键区别在于：权重 $\omega^t$ 由循环状态 $r^{t-1}$ 和当前视觉特征联合计算得出，因此注意力分配不仅取决于“当前看到了什么”，更取决于“之前经历了什么”。这一设计使模型能够根据任务进度动态切换关注区域，例如在“打开炉灶并放上摩卡壶”任务中，先聚焦炉灶开关，再关注壶的放置位置。

### 完整前向传播：三处关键变更的统一

将上述创新整合后，AVA-VLA 的完整前向传播过程为：

$$\mathcal{A}^t = \mathcal{Q}(\mathcal{M}_{\mathrm{parallel}}(z_I^t, \mathcal{V}(\boldsymbol{x}^t, \boldsymbol{r}^{t-1}), z_S^t, \boldsymbol{r}^{t-1}))$$

相比 OpenVLA-OFT 的基线设计，这一公式体现了三个核心变更槽位：

| 变更槽位 | 基线值 (OpenVLA-OFT) | 提出值 (AVA-VLA) | 功能角色 |
|---------|---------------------|-----------------|---------|
| 策略学习框架 | MDP，仅依赖 $x^t$ | POMDP，依赖 $x^t$ 和 $r^{t-1}$ | 引入历史上下文建模能力 |
| 动作占位符嵌入初始化 | 空嵌入（全零向量） | 循环状态 $r^{t-1}$ | 为动作预测提供历史先验 |
| 视觉注意力机制 | 标准自注意力，无历史调节 | AVA 模块通过 $r^{t-1}$ 计算软权重 $\omega^t$ 并调制 LLM 所有层的注意力矩阵 | 实现历史驱动的主动视觉聚焦 |

### 创新的互补性与参数效率

消融实验（Table 4, Table 9）揭示了循环状态初始化和 AVA 模块之间存在显著的**互补效应**：单独启用状态初始化（+init）或单独启用 AVA 模块（+ava）均能带来性能提升，但两者联合使用（完整 AVA-VLA）带来的增益远超各自贡献之和，且在长视界任务中这一协同效应更为突出。这表明循环状态不仅为动作预测提供了历史先验，更重要的是为 AVA 模块提供了有效的任务上下文，使其能够生成更有针对性的注意力权重。

值得注意的是，AVA 模块新增参数少于 50M，不足总模型参数的 1%，但在 LIBERO 和 CALVIN 基准上均带来了显著的性能提升。这一参数效率证明了性能增益源于 POMDP 框架和主动注意力机制的架构创新，而非简单的计算资源堆砌——在匹配训练设置（相同预训练起点、相同训练步数和批大小）下的公平对比实验（Table 7）进一步排除了额外计算量带来的混淆效应。

AVA‑VLA 的整体设计围绕一个核心目标展开：将视觉‑语言‑动作模型从被动的、逐帧独立的感知模式，转变为能够主动利用历史上下文进行决策的闭环系统。框架的输入流、模块关系与输出流如图 2 所示，其逻辑链条可概括为以下四个阶段。

**视觉与语言编码**  
在每一时间步 $t$，系统接收当前观测图像和自然语言指令。视觉编码器（由 DINOv2 和 SigLIP 组合而成）将图像编码为视觉令牌序列 $\mathbf{z}_I^t$；语言分词器将指令转换为语言令牌序列 $\mathbf{z}_S^t$。这一阶段与标准 VLA 模型一致，为后续的上下文感知处理提供原始感知表示。

**循环状态投影与动作占位符初始化**  
框架的关键创新在于引入了循环状态 $\boldsymbol{r}^{t-1}$，它由上一时间步 LLM 的隐藏状态 $\boldsymbol{h}_{M}^{t-1}$ 通过一个轻量级 MLP $\boldsymbol{\mathcal{B}}$ 投影得到（公式 5）。这一循环状态承担双重角色：其一，作为历史信念的神经近似，将策略学习从 MDP 范式重新表述为 POMDP 范式，使动作预测不仅依赖当前观测 $\mathbf{x}^t$，还依赖历史信念 $b^{t-1}$（公式 4）；其二，替代传统 VLA 中全零向量的动作占位符嵌入 $\mathbf{p}^t$，为并行解码提供富含时序上下文的初始状态。

**AVA 模块：历史驱动的主动视觉注意力**  
AVA 模块 $\mathcal{V}$ 是框架的第二个核心组件。它接收当前视觉观测和循环状态，通过模态特定的 MLP 编码视觉特征与指令特征，并利用循环状态作为“历史查询”来计算软注意力权重 $\boldsymbol{\omega}^t$。该权重向量随后被扩展为调制矩阵 $\mathbf{U}^t$（公式 12），逐层注入 LLM 所有层的自注意力计算中：对于视觉令牌索引集 $\Lambda_I$ 内的令牌，$\mathbf{U}^t$ 动态放大或抑制其注意力值，使模型能够根据历史上下文主动聚焦于任务关键区域，而非被动地处理所有视觉信息。

**动作解码与输出**  
经过 AVA 模块调制后的视觉令牌、语言令牌以及由循环状态初始化的动作占位符，共同输入 LLM 主干（LLaMA2‑7B）进行并行解码。LLM 输出的隐藏状态最终由动作头 $\mathcal{Q}$ 映射为机器人动作序列 $\mathcal{A}^t$，包含末端执行器的平移、旋转和夹爪状态。同时，当前步的隐藏状态会被保留，用于下一时间步的循环状态计算，形成闭环的时序信息流。

**训练机制**  
框架采用截断的沿时间反向传播策略进行端到端训练，时间窗口设为 $T=4$。除标准的动作预测损失外，还引入了注意力正则项 $\mathcal{L}_\omega$（公式 13），对软权重向量的均值施加 L2 惩罚，鼓励注意力聚焦于任务相关区域，抑制背景噪声的干扰。AVA 模块新增参数量不足总参数的 1%，但通过与循环状态初始化的协同作用，在长视界任务中带来了显著的性能增益。

![[assets/figures/papers/paper_list_l2372_https_arxiv_org_abs_2511_18960/figures/002_Figure.jpg]]
*Figure: xx x x x x x xFigure 2. Overview of the proposed AVA-VLA framework. At each timestep, the recurrent state is projected from the previous hidden state to preserve historical context and to initialize the current action tokens. Then the AVA module combines this recurrent state with textconditioned visual features from the current observation to generate soft importance scores, which modulate the visual attention matrices throughout the backbone LLM, enabling the model to focus on task-relevant regions based on both temporal context and current perception*

### 问题形式化：从 MDP 到 POMDP

标准 VLA 模型将机器人操作建模为马尔可夫决策过程（MDP），策略仅依赖当前观测 $\mathbf{x}^t$ 预测动作序列：

$$\bar{\mathcal{A}}^t \sim \mathcal{P}_\theta(\mathcal{A}^t \mid \mathbf{x}^t) \tag{3}$$

这种历史无关的设计在部分可观察环境中存在根本性缺陷：它无法捕捉被遮挡物体的状态、非可观测的环境动态等隐变量，导致视觉注意力被动且缺乏时间一致性。AVA-VLA 将策略学习重新表述为部分可观察马尔可夫决策过程（POMDP），策略同时依赖当前观测和信念状态 $b^{t-1}$：

$$\bar{\mathcal{A}}^t \sim \mathcal{P}_\theta(\mathcal{A}^t \mid \mathbf{x}^t, b^{t-1}) \tag{4}$$

其中信念状态 $b^{t-1}$ 编码了截至上一时间步的所有历史信息，使模型能够基于完整执行上下文进行决策。

### 循环状态投影模块

为在 VLA 架构中实现 POMDP 策略，AVA-VLA 引入循环状态 $\boldsymbol{r}^{t-1}$ 作为信念状态的神经近似。该状态由前一时间步 LLM 最后解码器层的隐藏状态 $\boldsymbol{h}_{M}^{t-1}$ 通过轻量 MLP $\boldsymbol{\mathcal{B}}$ 投影得到：

$$\boldsymbol{r}^{t-1} = \boldsymbol{\mathcal{B}}(\boldsymbol{h}_{M}^{t-1}) \in \mathbb{R}^{\mathrm{L}_A \times d} \tag{5}$$

其中 $\mathrm{L}_A$ 为动作序列长度，$d$ 为隐藏维度。循环状态承担双重角色：一方面作为动作占位符嵌入的初始化（替代基线中的全零向量），将历史上下文注入当前动作预测；另一方面作为 AVA 模块的核心输入，驱动主动视觉注意力。

### 主动视觉注意力（AVA）模块

AVA 模块是框架的核心创新，其功能是利用循环状态 $\boldsymbol{r}^{t-1}$ 和当前视觉观测 $\mathbf{x}^t$ 计算软注意力权重 $\omega^t$，并通过调制 LLM 所有层的注意力矩阵来动态增强或抑制视觉令牌。完整的前向传播为：

$$\mathcal{A}^t = \mathcal{Q}(\mathcal{M}_{\mathrm{parallel}}(z_I^t, \mathcal{V}(\boldsymbol{x}^t, \boldsymbol{r}^{t-1}), z_S^t, \boldsymbol{r}^{t-1})) \tag{6}$$

其中 $\mathcal{V}$ 代表 AVA 模块，其内部机制如下：

1. **多模态特征编码**：AVA 模块首先使用模态特定的 MLP 分别编码视觉特征 $z_I^t$ 和语言指令特征 $z_S^t$，再通过 FiLM 层将语言特征作为条件注入视觉特征，得到条件化视觉表示 $\hat{z}_I^t$。

2. **软权重计算**：以 $\hat{z}_I^t$ 作为 Query、循环状态 $\boldsymbol{r}^{t-1}$ 作为 Key 和 Value，通过交叉注意力机制计算每个视觉令牌的重要性得分，经 Sigmoid 激活后得到软权重向量 $\omega^t = [\omega_1^t, \omega_2^t, ..., \omega_{\mathrm{L}_I}^t]$，其中 $\mathrm{L}_I$ 为视觉令牌数量。

3. **注意力调制**：基于 $\omega^t$ 构造调制矩阵 $\mathbf{U}^t$，用于缩放 LLM 自注意力中的视觉令牌交互权重：

$$\mathbf{U}_{i,j}^t = \begin{cases} 1 & i=j \text{ or } j \notin \Lambda_I \\ \omega_j^t & i \neq j \text{ and } j \in \Lambda_I \end{cases} \tag{12}$$

其中 $\Lambda_I$ 为视觉令牌的索引集合。矩阵 $\mathbf{U}^t$ 被广播到 LLM 所有 Transformer 层的注意力矩阵上，通过逐元素乘法实现：当 $j$ 为视觉令牌且 $i \neq j$ 时，注意力权重被缩放为 $\omega_j^t$，从而根据历史上下文动态调节模型对每个视觉区域的关注程度。

### 注意力正则化

为防止软权重过度分散、确保模型聚焦于任务关键区域，训练时引入 L2 惩罚正则项：

$$\mathcal{L}_\omega^{t,n} = \| \mu(\omega^{t,n}) - c \| \tag{13}$$

其中 $\mu(\omega^{t,n})$ 为第 $n$ 层软权重向量的均值，$c$ 为目标均值常数。该正则项鼓励注意力集中在少数高相关性的视觉令牌上。消融实验（Table 8）表明，移除 $\mathcal{L}_\omega$ 导致平均成功率从 98.0% 降至 97.5%，且注意力图变得分散、背景噪声增加（Figure 12），验证了正则化对维持选择性注意力的关键作用。

![[assets/figures/papers/paper_list_l2372_https_arxiv_org_abs_2511_18960/figures/022_Figure_12.jpg]]
*Figure 12: Visualization of the soft weights without the regularizer*

### 训练策略

AVA-VLA 采用截断的时间反向传播（Truncated BPTT）进行训练，时间窗口 $T=4$，以平衡计算可行性与时序依赖学习的需求。循环状态 $\boldsymbol{r}^{t-1}$ 的梯度通过时间步反向传播，使模型学会将历史信息压缩为对当前决策有用的潜在表示。

![[assets/figures/papers/paper_list_l2372_https_arxiv_org_abs_2511_18960/figures/001_Figure_1.jpg]]
*Figure 1: (a) Visualized comparison of the proposed AVA-VLA framework and vanilla VLAs. (b) Qualitative comparison of visual focus from two viewpoints while executing the task “turn on the stove and put the moka pot on it.” The vanilla OpenVLA-OFT [20] baseline fails to locate the task-critical “stove” switch, whereas AVA-VLA exhibits more stable focus by leveraging historical context*

## 实验与关键发现

### 核心发现

AVA-VLA在模拟与真实世界基准上均取得了最优表现，且其增益在长序列任务和视觉扰动场景下尤为突出。核心机制——将VLA从MDP重新构建为POMDP，并利用循环状态驱动主动视觉注意力——使得模型能够依据历史上下文动态聚焦任务关键区域，而非被动地对每一帧独立响应。

**LIBERO基准。** 在LIBERO的两种评估协议下，AVA-VLA均超越了所有对比方法（Table 1）。在“one policy for all 4 suites”设置下，AVA-VLA的平均成功率达到98.0%，较OpenVLA-OFT的96.8%提升1.2个百分点；在“one policy per suite”设置下，平均成功率为98.2%，较OpenVLA-OFT的97.1%提升1.1个百分点。值得注意的是，在长视界任务套件LIBERO-Long上，AVA-VLA达到95.3%，比OpenVLA-OFT的92.7%高出2.6个百分点，初步验证了历史上下文建模对顺序决策任务的重要性。

**CALVIN ABC→D基准。** 在需要连续执行5个任务的CALVIN长序列基准上，AVA-VLA的优势更为显著（Table 2）。AVA-VLA的5任务连续成功率达到84.1%，相比OpenVLA-OFT的72.9%提升11.2个百分点；平均完成序列长度也从4.43提升至4.74。这一结果表明，POMDP框架下的循环状态在需要跨任务记忆和上下文推断的场景中发挥了关键作用。

### 消融研究

**核心组件消融。** 为验证循环状态初始化（+init）和AVA模块（+ava）的独立贡献与协同效应，论文在LIBERO（Table 4）和CALVIN（Table 9）上进行了组件消融。在LIBERO的“one policy for all 4 suites”设置下，单独启用状态初始化使平均成功率从96.8%提升至97.4%，单独启用AVA模块提升至97.5%，而两者联合使用（即完整AVA-VLA）达到98.0%。在CALVIN上，趋势一致：+init将5任务成功率从72.9%提升至78.6%，+ava提升至79.8%，完整AVA-VLA则达到84.1%。两个模块相互补充，且联合增益大于各自增益之和，表明历史状态初始化与动态注意力调制之间存在正向交互。

**模型主干泛化性。** 为排除增益来自特定LLM主干的可能，论文在LLaMA2-7B、LLaMA3-8B和Qwen2-7B三种主干上进行了对比（Table 3）。在LIBERO-Long任务套件上，AVA-VLA在三种主干下均稳定优于对应的OpenVLA-OFT基线，平均提升约1.7个百分点。这表明所提出的POMDP框架和AVA模块具有良好的架构无关性。

**视觉令牌修剪。** AVA模块输出的软权重$\omega^t$可直接用于视觉令牌重要性排序。论文据此进行了令牌修剪实验（Table 5）：在50%和70%的修剪率下，AVA-VLA的性能与未修剪时基本持平（97.8%和97.5% vs. 98.0%）；即使在90%的极端修剪率下，仍保持94.5%的平均成功率，优于多数未修剪的基线方法。这一发现揭示了AVA权重在视觉冗余压缩方面的潜力。

**注意力正则化。** 移除软权重的L2正则项$\mathcal{L}_\omega$后，平均成功率从98.0%下降至97.5%（Table 8）。定性可视化显示（Figure 12），缺乏正则化时注意力图变得分散，对背景区域的响应增加，表明该正则项有助于维持注意力掩码的选择性和结构稳定性。

### 鲁棒性分析

在LIBERO+扰动基准上（Table 6），AVA-VLA在7种扰动类型（包括光照变化、背景替换、物体纹理变化、布局扰动等）下的平均成功率均优于对比方法，综合平均成功率最高。这一结果说明，由历史上下文引导的主动注意力机制使模型对视觉分布偏移具有更强的抗干扰能力——模型能够根据任务语义而非表面视觉特征来定位关键区域。

![[assets/figures/papers/paper_list_l2372_https_arxiv_org_abs_2511_18960/figures/011_Table_6.jpg]]
*Table 6: Model performance under different perturbations in the LIBERO+ benchmark. For each column, the average task success rate (%) of four task suites (LIBERO-Spatial, LIBERO-Object, LIBERO-Goal, and LIBERO-Long) under the given perturbation type is reported. The last column reports the average task success rate over seven perturbation types. The best results in each column of each group are highlighted in bold*

### 公平性验证

为排除额外计算量带来的混淆，论文在匹配训练设置下进行了严格对比（Table 7）：双方均从相同的预训练OpenVLA检查点初始化，使用相同的100K训练步数和256的批大小。在此条件下，AVA-VLA在LIBERO四个任务套件上仍一致优于OpenVLA-OFT。此外，AVA模块新增参数量不足总参数的1%（少于50M），进一步确认性能增益源于架构创新而非计算资源增加。

![[assets/figures/papers/paper_list_l2372_https_arxiv_org_abs_2511_18960/figures/013_Table_7.jpg]]
*Table 7: Comparison under matched training settings. The results on the LIBERO benchmark in terms of success rates (%) under the “one policy for all 4 suites” setting are reported. Both OpenVLA-OFT and AVA-VLA are initialized from the same pretrained OpenVLA checkpoint and trained with 100K gradient steps in a batch size of 256. The best results in each column are highlighted in bold*

### 失败模式与局限

尽管AVA-VLA在整体上表现优异，论文指出了两个关键局限。第一，在长视界任务中，微小的感知或状态估计误差会随时间累积，导致**信念漂移**（belief drift），进而引发抓取、放置等精确操作失败。这一现象在LIBERO-Long任务及高视觉令牌修剪率下尤为明显。第二，训练中采用的截断BPTT策略（时间窗口T=4）可能不足以捕捉非常长期的依赖关系，限制了循环状态对远历史信息的建模能力。

![[assets/figures/papers/paper_list_l2372_https_arxiv_org_abs_2511_18960/figures/003_Table_1.jpg]]
*Table 1: Comparison on the LIBERO benchmark. The results are reported in two groups: one policy for all 4 suites, and one policy per suite. The best results in each column of each group are highlighted in bold*

## 定位与知识库关联

### 问题定位：从MDP到POMDP的VLA范式转换

当前主流的VLA模型——包括 **OpenVLA**、**OpenVLA-OFT**、**UniVLA**、**FLOWER**、**RIPT-VLA** 以及 **π0**——均将机器人操作建模为马尔可夫决策过程（MDP），其策略形式为 $\bar{\mathcal{A}}^t \sim \mathcal{P}_\theta(\mathcal{A}^t \mid \mathbf{x}^t)$，仅依赖当前观测 $\mathbf{x}^t$ 预测动作（Eq. 3）。这种历史无关的设计在部分可观察环境中存在根本性缺陷：模型无法利用过往信息推断被遮挡物体、非可观测动态或任务进度，导致视觉注意力被动且缺乏时间一致性。

AVA-VLA 的核心创新在于将策略学习重新表述为部分可观察马尔可夫决策过程（POMDP），策略形式变为 $\bar{\mathcal{A}}^t \sim \mathcal{P}_\theta(\mathcal{A}^t \mid \mathbf{x}^t, b^{t-1})$（Eq. 4），其中 $b^{t-1}$ 为历史信念状态的神经近似。据论文声明，这是首个从POMDP视角显式解决VLA历史上下文缺失问题的框架。

### 方法差异：三个关键槽位的变化

与基线方法 **OpenVLA-OFT** 相比，AVA-VLA 在三个关键设计槽位上进行了替换：

| 设计槽位 | 基线值（OpenVLA-OFT） | 提出值（AVA-VLA） |
|----------|----------------------|-------------------|
| 动作占位符嵌入初始化 | 空嵌入（全零向量） | 前一时间步的循环状态 $\boldsymbol{r}^{t-1}$ |
| 视觉注意力机制 | 基于当前视觉令牌和语言指令的标准自注意力，无历史调节 | AVA模块通过循环状态计算软权重 $\omega^t$，并调制LLM所有层的注意力矩阵 |
| 策略学习框架 | MDP假设，仅依赖当前观测 $\mathbf{x}^t$ | POMDP假设，基于 $\mathbf{x}^t$ 和 $\boldsymbol{r}^{t-1}$ 联合预测 |

其中，循环状态 $\boldsymbol{r}^{t-1}$ 由 MLP $\mathcal{B}$ 从前一步LLM的隐藏状态 $\boldsymbol{h}_{M}^{t-1}$ 映射得到（Eq. 5），作为历史信念的压缩表示。AVA模块 $\mathcal{V}$ 则接收当前视觉观测 $\boldsymbol{x}^t$ 和 $\boldsymbol{r}^{t-1}$，通过跨模态注意力计算软权重向量 $\omega^t$，进而构造调制矩阵 $\mathbf{U}^t$（Eq. 12），对LLM所有层的自注意力进行重新加权，使模型动态聚焦于任务关键区域。

### 与相关工作的关系

**循环状态机制。** 在VLA中引入循环状态以捕捉时序依赖，与一般序列建模中的RNN/Transformer思想相通，但AVA-VLA的独特之处在于将循环状态同时用于两个目的：(1) 初始化动作占位符嵌入，提供历史先验；(2) 驱动AVA模块的主动视觉注意力。消融实验（Table 4, Table 9）表明，状态初始化（+init）和AVA模块（+ava）相互补充，联合使用比单独使用任一模块带来更大增益，且在长视界任务中优势更显著。

**视觉注意力调制。** 与通用的交叉注意力或门控机制不同，AVA模块直接修改LLM内部的注意力矩阵，而非在输入端进行特征筛选。这种设计使历史信息能够渗透到LLM的每一层表示中，实现更深层的上下文调节。注意力正则项 $\mathcal{L}_\omega^{t,n} = \| \mu(\omega^{t,n}) - c \|$（Eq. 13）进一步约束软权重的集中度，防止注意力分散到无关背景区域（去除该正则项导致成功率从98.0%降至97.5%，Table 8）。

**视觉令牌压缩。** 利用AVA模块的软权重进行视觉令牌修剪，在50%–70%修剪率下性能与未修剪时相当，90%修剪时仍优于多数基线（Table 5），这表明AVA权重可作为高效的令牌重要性指标，为未来VLA的推理加速提供了可行路径。

### 适用边界与局限

**长视界信念漂移。** 在长序列任务中，微小的感知或状态估计误差会随时间累积，导致信念漂移（belief drift），进而引发抓取、放置等精确操作失败。这一现象在LIBERO-Long任务及视觉令牌大量修剪时尤为明显。论文采用的截断BPTT训练（$T=4$）可能不足以捕捉非常长期的依赖关系。

**训练与推理成本。** 虽然AVA模块新增参数少于50M（不足总参数的1%），且匹配训练设置下的公平对比（Table 7）排除了计算量带来的增益，但循环状态的序列依赖使得训练必须采用BPTT，增加了内存开销和训练复杂度。

**泛化边界。** 实验覆盖了LIBERO（模拟）、CALVIN（模拟）和Mobile ALOHA（真实世界双机械臂）三个平台，证明了方法在不同场景下的有效性。但所有任务均为桌面级操作，尚未验证在移动导航、人机交互等更广泛机器人任务上的适用性。

### 开放问题

1. **状态传播稳定性。** 如何提高循环状态传播的稳定性，以缓解长视界任务中的信念漂移？显式错误校正策略或更长视界的训练方案能否更好地将循环状态对齐到任务相关的环境动态？

2. **AVA模块的通用性。** AVA模块的软权重机制能否更广泛地用于其他VLA架构（如基于Diffusion Policy的模型），并实现更高效的视觉令牌压缩？当前方法依赖LLM内部的注意力调制，对于非Transformer架构的适配性尚不明确。

3. **训练效率优化。** 截断BPTT的序列长度 $T=4$ 是在计算可行性与时序学习之间的折中。是否存在更高效的训练策略（如稀疏注意力、状态缓存复用）可以在不显著增加开销的前提下扩展有效时间视野？

4. **多模态历史融合。** 当前循环状态仅编码视觉-语言联合信息，是否应当显式融合本体感觉（proprioception）或力觉信息，以构建更丰富的信念表示？

## 原文 PDF

![[paperPDFs/CVPR_2026/AVA_VLA_Improving_Vision_Language_Action_models_with_Active_Visual_Attention.pdf]]
