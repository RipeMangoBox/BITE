---
title: Learning Human Motion with Temporally Conditional Mamba
type: paper
paper_level: A
venue: SIGGRAPH ASIA
year: 2025
pdf_ref: paperPDFs/SIGGRAPH_ASIA_2025/TCM_Learning_Human_Motion_with_Temporally_Conditional_Mamba.pdf
project_link: https://zquang2202.github.io/TCM
code_link: null
aliases:
- TCMT
- LHMTCM
tags:
- SIGGRAPH_ASIA_2025
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
core_operator: 将时间条件信号直接注入Mamba块的选择矩阵 B 和 C 的仿射调制中，使状态空间的演化过程在每个时间步都依赖于外部条件，实现自回归的时序对齐。
primary_logic: 利用线性参数变化状态空间模型的思想，对Mamba的输入/输出矩阵进行逐时间步的条件调制（缩放与偏移），让循环动态可以灵活适应不同的外部条件，从而在保持长序列建模能力的同时显著提升时间一致性和条件一致性。
claims:
- 在AIST++音乐到舞蹈任务上，TCM的节拍对齐分数（BAS）达到0.2761，远超交叉注意力的0.2411和Vanilla Mamba的0.2434，表明更强的时序对齐能力。
- 消融实验显示，移除TCM块会导致BAS从0.2761降至0.2434，其他质量指标也明显下降，证明TCM是时序对齐的关键组件。
- 生成运动的关节平均速度曲线显示，TCM产生的运动节拍（局部极小值）与音乐节拍高度吻合，而交叉注意力和Vanilla Mamba的节拍对齐较差。
- 在自我中心视频到运动任务中，TCM生成的头部轨迹比交叉注意力和Vanilla Mamba更接近真实值。
---

# Learning Human Motion with Temporally Conditional Mamba

> [!tip] 核心洞察
> 利用线性参数变化状态空间模型的思想，对Mamba的输入/输出矩阵进行逐时间步的条件调制（缩放与偏移），让循环动态可以灵活适应不同的外部条件，从而在保持长序列建模能力的同时显著提升时间一致性和条件一致性。

| 字段 | 内容 |
|------|------|
| 中文题名 | 用时间条件Mamba学习人体运动 |
| 英文题名 | Learning Human Motion with Temporally Conditional Mamba |
| 会议/期刊 | SIGGRAPH ASIA 2025 |
| Links | [Project](https://zquang2202.github.io/TCM) · [paper](https://dl.acm.org/doi/10.1145/3746027.3755855) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction |
| Method | Temporally Conditional Mamba (TCM) |
| Dataset | AIST++ |

> [!tip] 效果简介
> - AIST++ (music-to-dance) 上，FID_k (↓) 20.66 vs 23.43 (Cross-Attention) (-2.77)；FID_g (↓) 9.75 vs 12.86 (Cross-Attention) (-3.11)；Div_k (↑) 8.98 vs 7.87 (Cross-Attention) (+1.11)。
> - AIST++ (25s length) 上，FID_k (↓) 23.82 vs 31.36 (Cross-Attention) (-7.54)。

## 概要

**问题瓶颈**：现有基于扩散模型的人体运动生成方法（如 **EDGE** (Tseng et al., CVPR 2023)、**Bailando** (Siyao et al., CVPR 2022)）普遍采用交叉注意力（Cross-Attention）将音乐、视频等时间条件信号注入Transformer或Mamba主干网络。这种全局交互方式缺乏逐步的时间对齐能力，导致生成的运动与条件信号之间存在明显的时序偏差——具体表现为舞蹈动作的节拍与音乐节拍错位、自我中心视频估计的头部轨迹偏离真实值等。

**核心方法**：本文提出**时间条件Mamba（Temporally Conditional Mamba, TCM）**，将时间条件信号直接注入Mamba块的状态空间演化过程。具体而言，TCM对Mamba的选择矩阵 $\widetilde{\mathbf{B}}_l$ 和 $\widetilde{\mathbf{C}}_l$ 进行逐时间步的仿射调制（缩放与偏移），使循环动态在每个时间步都依赖于外部条件，实现自回归的时序对齐。这一设计源于线性参数变化状态空间模型的思想，在保持长序列建模能力的同时显著提升时间一致性。

**方法定位**：TCM作为即插即用的Mamba变体，可嵌入扩散模型的去噪骨干网络。与交叉注意力在层间进行条件融合不同，TCM在Mamba块内部完成条件感知的状态更新。该架构还整合了**自适应层归一化（AdaLN）**和**空间Mamba（Spatial Mamba）**模块，分别负责全局条件调制和关节间空间依赖建模。

**主要结果**：
- 在**AIST++音乐到舞蹈**任务上，TCM的节拍对齐分数（BAS）达到0.2761，显著优于交叉注意力（0.2411）和Vanilla Mamba（0.2434）；运动质量指标FID_k降至20.66（交叉注意力为23.43）。
- 在**长序列生成**（25秒）场景下，TCM的FID_k仅从20.66增至23.82，而交叉注意力则从25.61急剧恶化至31.36，展现更强的长程稳定性。
- 在**自我中心视频到运动**任务上，TCM生成的头部轨迹比交叉注意力和Vanilla Mamba更贴近真实值。
- 消融实验证实，移除TCM块会导致BAS从0.2761降至0.2434，证明其是时序对齐的关键组件；缩放调制（$\gamma$）比偏移调制（$\beta$）对性能贡献更大。

**局限与开放问题**：当前TCM要求条件序列与运动序列具有相同的时间长度，难以直接处理文本等静态条件；极端头部运动下的鲁棒性、足部滑动伪影的消除、超长序列（数分钟）的稳定性等问题尚待进一步探索。



### 问题背景

人体运动生成是计算机视觉与图形学中的核心问题，其目标是根据给定的外部条件（如音乐、视频、物体轨迹等）合成自然、逼真的人体动作序列。该技术在虚拟人动画、游戏角色控制、AR/VR交互等领域具有广泛的应用前景。近年来，扩散模型（Diffusion Models）已成为人体运动生成的主流范式，通过逐步去噪的方式从随机噪声中恢复出高质量的运动序列。

### 现有方法的瓶颈

当前基于扩散模型的人体运动生成方法，在融合时间条件信号（如音乐节拍、头部运动轨迹）时，普遍采用**交叉注意力（Cross-Attention）**机制。具体而言，这些方法将条件嵌入作为额外的键值对（Key-Value）注入到Transformer或Mamba主干网络中，通过全局交互的方式实现条件与运动特征的融合。

然而，这种全局融合策略存在一个根本性的缺陷：**缺乏逐步的时间对齐能力**。交叉注意力在每一层对所有时间步的条件和运动特征进行一次性全局交互，并未显式建模条件信号与运动序列在逐时间步上的对应关系。这导致生成的运动与条件信号之间出现明显的**时序偏差（temporal misalignment）**，表现为：

- 在音乐到舞蹈生成中，舞蹈动作的节拍与音乐节拍错位（参见 **Fig. 3**）；
- 在自我中心视频到运动估计中，生成的头部轨迹逐渐偏离真实轨迹（参见 **Fig. 1c**）。

此外，当运动序列长度增加时（如从5秒扩展到25秒），交叉注意力方法的生成质量急剧下降，FID_k从25.61飙升至31.36（参见 **Table 3**），暴露出其在长程时间建模上的不足。

### 核心动机

上述瓶颈的根源在于：**条件融合机制与序列生成过程的时间结构不匹配**。人体运动天然具有自回归的时间依赖特性——当前时刻的动作不仅取决于当前的条件信号，还依赖于过去的状态演化。因此，理想的条件注入方式应当允许外部条件在每一个时间步直接参与状态空间的递推更新，而非仅在全局层面进行特征混合。

受状态空间模型（State Space Models, SSM）中参数化动态系统的启发，本文提出一个关键洞察：**将时间条件信号直接注入到Mamba块的选择矩阵 $\mathbf{B}$ 和 $\mathbf{C}$ 的仿射调制中**，使状态空间的演化过程在每个时间步都依赖于外部条件，从而实现自回归的时序对齐。这一设计利用了线性参数变化（Linear Parameter-Varying, LPV）状态空间模型的思想——通过对输入/输出矩阵进行逐时间步的条件调制（缩放与偏移），让循环动态可以灵活适应不同的外部条件，在保持长序列建模能力的同时显著提升时间一致性。

基于此动机，本文提出了**时间条件Mamba（Temporally Conditional Mamba, TCM）**，一种新型的Mamba变体，将条件感知机制嵌入到Mamba块的内部递归动态中，从根本上解决现有方法中条件融合与时间演化相分离的问题。



## 核心方法与创新机理

Temporally Conditional Mamba (TCM) 的核心创新在于**将时间条件信号直接注入状态空间模型（SSM）的循环动态中**，而非像现有方法那样通过外部交叉注意力（Cross-Attention）进行全局条件融合。这一设计解决了当前人体运动生成领域的一个关键瓶颈：基于交叉注意力的扩散模型（如 **EDGE**，Tseng et al., CVPR 2023）缺乏逐步的时间对齐能力，导致生成的运动与条件信号（如音乐节拍、头部轨迹）之间存在明显的时序偏差。

### 创新点一：条件感知的选择矩阵调制

TCM 最关键的 changed slot 是对 Mamba 块中输入/输出选择矩阵 $\mathbf{B}$ 和 $\mathbf{C}$ 的逐时间步仿射调制。标准 Mamba（Vanilla Mamba）的隐藏状态更新遵循：

$$h_{dl} = \overline{\mathbf{A}}_{dl} \cdot h_{d,l-1} + \overline{\mathbf{B}}_{dl} \cdot x_{dl}, \quad y_{dl} = \mathbf{C}_l \cdot h_{dl}$$

其中 $\mathbf{B}$ 和 $\mathbf{C}$ 仅依赖于当前输入 $x_l$，与外部条件无关。TCM 将条件嵌入 $m_l$ 引入这一过程，通过缩放参数 $\gamma$ 和偏移参数 $\beta$ 对矩阵进行调制：

$$\widetilde{\mathbf{B}}_l = \gamma_{\mathbf{B}}(m_l) \odot \mathbf{B}_l + \beta_{\mathbf{B}}(m_l), \quad \widetilde{\mathbf{C}}_l = \gamma_{\mathbf{C}}(m_l) \odot \mathbf{C}_l + \beta_{\mathbf{C}}(m_l)$$

这使得状态空间的演化过程在每个时间步都直接受外部条件控制，实现了**自回归的时序对齐**。消融实验（Table 2）证实了这一设计的决定性作用：移除 TCM 块（即回退到 Vanilla Mamba 仅通过 AdaLN 融合全局条件）导致节拍对齐分数 BAS 从 0.2761 降至 0.2434，FID_k 从 20.66 升至 25.61。进一步分析表明，缩放调制 $\gamma$ 比偏移调制 $\beta$ 更为关键——移除 $\gamma$ 造成的性能下降显著大于移除 $\beta$。

### 创新点二：自适应层归一化（AdaLN）

作为辅助机制，TCM 将标准 LayerNorm 替换为自适应层归一化（AdaLN）。其缩放参数 $\lambda_i$ 和偏移参数 $\rho_i$ 由时间步嵌入 $\mathbf{t}$ 和条件嵌入 $\mathbf{m}$ 的求和通过 MLP 联合生成：

$$\lambda_i, \rho_i = \mathrm{MLP}(\mathrm{Sum}(\mathbf{t}, \mathbf{m}))$$

调制后的特征为 $\mathbf{x}' = \lambda_i \odot \mathbf{Norm}(\mathbf{x}) + \rho_i$。AdaLN 为 TCM 和 Spatial Mamba 模块提供全局的条件感知特征调制，与 TCM 的逐帧调制形成互补。消融实验（Table 2）显示，移除 AdaLN 使 FID_k 升至 21.89，BAS 降至 0.2615，表明其对性能有正向贡献但非核心。

### 创新点三：时空解耦的 Mamba 架构

TCM 与 Spatial Mamba 协同工作，形成时空解耦的建模方案：TCM 沿时间维度建模条件驱动的运动动态，Spatial Mamba 将运动表示从时间域重排至空间域（关节维度），用标准 Mamba 建模关节间的空间依赖。这一设计使得模型能够分别专注于时序对齐和空间合理性，在多个任务（音乐到舞蹈、自我中心视频到运动、物体轨迹到人体运动）上均展现出优于交叉注意力方案的一致性能提升。



TCM 构建在扩散模型的骨干框架之上，整体 pipeline 遵循“噪声运动 → 去噪网络 → 预测干净运动”的标准扩散范式。给定一段噪声化的运动序列 **x**、时间条件嵌入 **m** 以及扩散时间步嵌入 **t**，模型的目标是预测对应的干净运动  **x̂**。

架构的核心由两类 Mamba 块交替堆叠而成：**Temporally Conditional Mamba (TCM)** 和 **Spatial Mamba**，两者之前均设有自适应层归一化（AdaLN）模块。

1. **输入嵌入与条件准备**  
   运动序列首先通过线性投影映射到隐空间。同时，外部条件信号（如音乐特征、视觉特征）经由预训练的特征提取器（如 Jukebox、ResNet-50）编码为帧级条件嵌入 **m**，扩散时间步 **t** 也通过正弦位置编码生成时间步嵌入。两者在送入 AdaLN 时被求和融合，用于生成逐通道的缩放/偏移参数。

2. **Temporally Conditional Mamba（时间条件 Mamba）**  
   这是 TCM 框架的核心创新模块。运动嵌入与条件嵌入共同输入 TCM，TCM 内部对标准 Mamba 的选择矩阵 **B** 和输出矩阵 **C** 进行逐时间步的仿射调制（缩放 γ 与偏移 β），使得状态空间的循环演化过程直接受条件信号驱动。这一设计将时间条件自回归地注入到每个时间步的隐状态更新中，实现了运动与条件信号的逐步时序对齐。图 2b 展示了 TCM 的详细结构，算法 1 给出了其前向传播的伪代码。

3. **Spatial Mamba（空间 Mamba）**  
   在时间建模之后，运动表示被从时间域重排至空间域（关节维度），送入标准 Mamba 块以捕获人体关节之间的空间依赖关系。该模块不涉及条件注入，专注于学习合理的身体姿态与关节协调。图 2c 展示了其结构。

4. **自适应层归一化（AdaLN）**  
   在每个 TCM 和 Spatial Mamba 之前，AdaLN 利用时间步嵌入与条件嵌入的联合 MLP 生成维度级的缩放参数 λ 和偏移参数 ρ，对归一化后的运动嵌入进行全局调制。这一机制在扩散过程中动态调整特征的分布，为后续的 Mamba 块提供全局上下文。

5. **输出与训练目标**  
   经多组 TCM + Spatial Mamba 块交替处理后，最终通过线性投影输出预测的干净运动。训练目标为最小化预测运动与真实运动之间的期望 L1 距离。

整个 pipeline 的输入输出流可概括为：**噪声运动 + 条件嵌入 + 时间步嵌入 → AdaLN 调制 → TCM（时间条件对齐）→ AdaLN 调制 → Spatial Mamba（空间依赖建模）→ 多层堆叠 → 预测干净运动**。图 2a 给出了这一架构的整体概览。

### 补充图表

![[assets/figures/papers/paper_list_l1928_TCM_Learning_Human_Motion_with_Temporally_Conditional_Mamba/figures/002_Figure_2.jpg]]
*Figure 2: Architecture overview of the proposed approach. (a) We show the overview of the diffusion human motion framework with Mamba blocks. (b) Our key contribution is the Temporally Conditional Mamba, which incorporates temporal conditions into the internal dynamics of the Mamba block. (c) The Spatial Mamba block is used to learn human spatial features*



### 问题定义与扩散框架

TCM 以扩散模型为骨干框架，输入带噪运动序列 $\mathbf{X}_t$、条件嵌入 $\mathbf{m}$ 与时间步嵌入 $\mathbf{t}$，预测去噪后的运动 $\hat{\mathbf{X}}_0$。训练目标为最小化预测与真实运动之间的期望 L1 距离：

$$
\boldsymbol{\hat{\theta}} = \arg\min_{\boldsymbol{\theta}} \mathbb{E}_{t, \mathbf{X}_t} \left[ \| \mathbf{X}_0 - f_{\boldsymbol{\theta}}(\mathbf{X}_t, \mathbf{m}, \mathbf{t}) \|_1 \right]
$$

### Mamba S6 基础状态空间模型

TCM 建立在 Mamba 的 S6 选择性状态空间模型之上。对于第 $d$ 个通道在时间步 $l$ 的隐藏状态更新与输出，其离散化后的递推形式为：

$$
h_{dl} = \overline{\mathbf{A}}_{dl} \cdot h_{d,l-1} + \overline{\mathbf{B}}_{dl} \cdot x_{dl}, \quad y_{dl} = \mathbf{C}_l \cdot h_{dl}
$$

其中系统矩阵通过零阶保持器离散化得到：

$$
\overline{\mathbf{A}}_{dl} = e^{\Delta_{dl} \cdot \mathbf{A}_d}, \quad \overline{\mathbf{B}}_{dl} = \Delta_{dl} \cdot \mathbf{B}_l
$$

### Temporally Conditional Mamba：条件感知的状态空间演化

TCM 的核心创新在于将时间条件信号直接注入 Mamba 的选择矩阵 $\mathbf{B}$ 和 $\mathbf{C}$，使状态空间的演化过程在每个时间步都依赖于外部条件。具体而言，TCM 将标准 Mamba 的状态更新方程重新定义为：

$$
h_{dl} = \bar{\mathbf{A}}_{dl} \cdot h_{d,l-1} + (\Delta_{dl} \cdot \widetilde{\mathbf{B}}_l(x_l, m_l)) \cdot x_{dl}, \quad y_{dl} = \widetilde{\mathbf{C}}_l(x_l, m_l) \cdot h_{dl}
$$

其中 $\widetilde{\mathbf{B}}_l$ 和 $\widetilde{\mathbf{C}}_l$ 是经条件嵌入 $m_l$ 调制后的选择矩阵。调制方式为逐元素的仿射变换：

$$
\widetilde{\mathbf{B}}_l = \gamma_{\mathbf{B}}(m_l) \odot \mathbf{B}_l + \beta_{\mathbf{B}}(m_l), \quad \widetilde{\mathbf{C}}_l = \gamma_{\mathbf{C}}(m_l) \odot \mathbf{C}_l + \beta_{\mathbf{C}}(m_l)
$$

**变量含义**：
- $h_{dl}$：第 $d$ 个通道在时间步 $l$ 的隐藏状态
- $\bar{\mathbf{A}}_{dl}$：离散化后的状态转移矩阵
- $\Delta_{dl}$：时间步长参数
- $\mathbf{B}_l, \mathbf{C}_l$：原始 Mamba 的输入/输出投影矩阵
- $\gamma_{\mathbf{B}}, \beta_{\mathbf{B}}, \gamma_{\mathbf{C}}, \beta_{\mathbf{C}}$：由条件嵌入 $m_l$ 生成的可学习缩放与偏移参数
- $m_l$：时间步 $l$ 的条件嵌入（如音乐节拍特征、头部轨迹编码）
- $x_{dl}, y_{dl}$：输入与输出特征

这种设计的因果机制在于：条件信号通过 $\gamma$ 和 $\beta$ 对每一帧的输入/输出投影进行缩放与偏移，使 Mamba 的循环动态可以灵活适应不同外部条件，实现自回归的时序对齐，而非仅在全局层面融合条件信息。

### Spatial Mamba：空间依赖建模

为建模人体关节间的空间依赖，TCM 在 Temporal Mamba 之后引入 Spatial Mamba 模块。该模块将运动表示从时间域重排至空间域（关节维度），利用标准 Mamba 块学习关节间的结构化关系（Fig. 2c）。

### 自适应层归一化（AdaLN）

在 TCM 和 Spatial Mamba 之前，均采用自适应层归一化对特征进行全局调制。其缩放参数 $\lambda_i$ 和偏移参数 $\rho_i$ 由时间步嵌入与条件嵌入求和后通过 MLP 生成：

$$
\lambda_i, \rho_i = \mathrm{MLP}(\mathrm{Sum}(\mathbf{t}, \mathbf{m}))
$$

调制后的特征为：

$$
\mathbf{x}' = \lambda_i \odot \mathbf{Norm}(\mathbf{x}) + \rho_i
$$

AdaLN 使模型能够根据扩散时间步和全局条件自适应调整特征分布，为后续 TCM 的逐帧条件调制提供更稳定的特征基底。消融实验表明，移除 AdaLN 会导致 FID_k 升至 21.89、BAS 降至 0.2615（Table 2），证明其对性能有正向贡献，但影响程度低于 TCM 模块本身。

### 关键消融发现

在调制参数层面，移除缩放参数 $\gamma_{B,C}$ 比移除偏移参数 $\beta_{B,C}$ 造成更大的性能下降（Table 2），表明缩放调制在条件感知的状态空间演化中扮演更关键的角色。这一发现从侧面印证了 TCM 的核心机理：通过缩放调整输入/输出投影的强度，使模型能够根据条件信号的强弱动态调控状态更新的幅度。

### 补充图表

![[assets/figures/papers/paper_list_l1928_TCM_Learning_Human_Motion_with_Temporally_Conditional_Mamba/figures/001_Figure_1.jpg]]
*Figure 1: High-level comparison between our approach and previous methods. (a) Previous works usually use Cross-Attention to integrate input condition into Mamba/Transformer backbone. (b) Our approach embeds the condition directly within the Mamba block; (c) We show the head trajectory over time in an ego-to-motion task. Compared to Cross-Attention and Vanilla Mamba, which generate motions that deviate noticeably from the ground truth, our method produces a trajectory that closely follows the actual motion pattern*



## 实验与关键发现

### 核心实验设计

TCM的实验验证围绕**时序对齐能力**这一核心瓶颈展开。作者构建了三个内部基线进行公平对比：**Vanilla Mamba**（仅通过AdaLN融合全局条件，无逐帧调制）、**Cross-Attention**（在Mamba/Transformer层中插入交叉注意力模块注入时间条件），以及完整的**TCM**。所有方法共享相同的预训练特征提取器（音乐用Jukebox，视觉用ResNet-50）、扩散框架和数据划分，推理效率评测统一使用DDIM采样器（50步）。

### 音乐到舞蹈合成：时序对齐的定量验证

在AIST++数据集上，TCM在所有运动质量与节拍对齐指标上均显著优于两个内部基线（Table 1）：

![[assets/figures/papers/paper_list_l1928_TCM_Learning_Human_Motion_with_Temporally_Conditional_Mamba/figures/003_Table_1.jpg]]
*Table 1: Comparative results of dance synthesis from music task. We compare our proposed TCM with Cross-Attention and Vanilla Mamba. Bold indicates best, and underline indicates second best*

- **运动质量**：TCM的FID_k降至20.66，相比Cross-Attention（23.43）和Vanilla Mamba（25.61）分别降低2.77和4.95；FID_g降至9.75，相比Cross-Attention（12.86）降低3.11。
- **运动多样性**：TCM的Div_k达到8.98，Div_g达到7.24，均高于Cross-Attention（7.87 / 6.48）和Vanilla Mamba（7.56 / 6.12），表明条件调制并未牺牲生成多样性。
- **节拍对齐**：TCM的BAS达到0.2761，远超Cross-Attention的0.2411和Vanilla Mamba的0.2434。这是TCM机制优势的直接证据——将条件注入状态空间的选择矩阵B和C，使每一步的隐藏状态演化都受音乐节拍信号驱动，实现了自回归的时序对齐。

关节平均速度曲线的可视化（Fig. 3）进一步从运动学层面印证了上述结论：TCM生成的运动节拍（速度曲线局部极小值）与音乐节拍高度吻合，而Cross-Attention和Vanilla Mamba的节拍对齐存在明显偏差。这表明交叉注意力的全局交互机制缺乏逐步的时间对齐能力，无法精确匹配细粒度的时序条件。

![[assets/figures/papers/paper_list_l1928_TCM_Learning_Human_Motion_with_Temporally_Conditional_Mamba/figures/005_Figure_3.jpg]]
*Figure 3: Motion and music beat alignment. We plot the mean joint velocity over time for different methods. Kinematic beats are identified as local minima in the velocity curves. Our method produces motion with kinematic beats that align more closely with the music beats*

### 消融实验：TCM是时序对齐的关键组件

消融实验（Table 2）系统拆解了TCM各组件的作用：

![[assets/figures/papers/paper_list_l1928_TCM_Learning_Human_Motion_with_Temporally_Conditional_Mamba/figures/004_Table_2.jpg]]
*Table 2: Ablation experiment on network components. We assess the performance of the proposed method under different settings*

- **移除TCM块**（w.o. TCM block）：BAS从0.2761骤降至0.2434，FID_k从20.66升至25.61，退化至Vanilla Mamba水平。这直接证实TCM的逐帧调制机制是时序对齐的核心来源。
- **移除自适应层归一化**（w.o. AdaLN block）：FID_k升至21.89，BAS降至0.2615。AdaLN对性能有正向贡献，但其影响幅度远小于TCM块本身，表明AdaLN起辅助调制作用而非核心驱动。
- **缩放参数γ vs 偏移参数β**：移除γ_B,C（w.o. γ_B,C）造成的性能下降显著大于移除β_B,C（w.o. β_B,C），说明缩放调制比偏移调制在条件适应中扮演更关键的角色。这一发现揭示了仿射调制中两个参数的非对称重要性。

### 长程生成能力

随着序列长度从5s增至25s（Table 3），TCM的FID_k仅从20.66升至23.82（增幅3.16），而Cross-Attention从25.61猛增至31.36（增幅5.75）。TCM在长序列上的性能衰减显著更慢，这归因于Mamba的状态空间模型本身具备线性复杂度的长程建模能力，而TCM的条件调制机制在长序列上仍能维持有效的时序对齐，不会像交叉注意力那样因全局交互的注意力分散而累积误差。

![[assets/figures/papers/paper_list_l1928_TCM_Learning_Human_Motion_with_Temporally_Conditional_Mamba/figures/006_Table_3.jpg]]
*Table 3: Ablation experiments on sequence length of motion. Length analysis. We evaluate the FID score of our TCM and Cross-Attention at different sequence lengths*

### 跨任务泛化

在自我中心视频到运动任务中，TCM生成的头部轨迹比Cross-Attention和Vanilla Mamba更接近真实值（Fig. 1c），定量指标O_head（0.15）、T_head（112.6）、MPJPE（116.3）均优于基线（Table 5）。在物体轨迹驱动的人体运动生成任务中，TCM同样取得最优结果（Table 7）。这表明TCM的条件注入机制对不同类型的时间条件（音乐特征、视觉特征、物体轨迹）具有通用性。

![[assets/figures/papers/paper_list_l1928_TCM_Learning_Human_Motion_with_Temporally_Conditional_Mamba/figures/010_Table_5.jpg]]
*Table 5: Comparison with State-of-the-art methods on ego-to-motion task. Bold indicates the best, and underline indicates the second-best results*

![[assets/figures/papers/paper_list_l1928_TCM_Learning_Human_Motion_with_Temporally_Conditional_Mamba/figures/008_Table_7.jpg]]
*Table 7: Comparative results on human motion generation from object movement task. Bold indicates best and underline indicates second best*

### 可解释性分析

对TCM块学习到的γ_B,C和β_B,C参数进行t-SNE可视化（Fig. 4），发现不同音乐流派的条件调制参数呈现明显的聚类结构。这说明TCM的条件仿射调制不仅仅是数值上的性能提升手段，其学习到的缩放/偏移参数确实编码了与音乐风格相关的判别性信息，为模型的可解释性提供了证据。

![[assets/figures/papers/paper_list_l1928_TCM_Learning_Human_Motion_with_Temporally_Conditional_Mamba/figures/007_Figure_4.jpg]]
*Figure 4: t-SNE visualization of ??B,C and*

### 失败模式与局限性

尽管TCM在时序对齐上表现优异，仍存在以下不足：

1. **极端头部运动的鲁棒性不足**：在自我中心视频任务中，突然的、剧烈的头部运动仍会导致生成动作的准确度下降，说明条件调制机制对输入信号的突变缺乏足够的缓冲能力。
2. **足部滑动与抖动伪影**：生成的运动可能包含物理上不合理的足部滑动和抖动，这是因为当前损失函数未引入运动学约束（如速度/加速度损失）或显式足部接触建模。
3. **条件长度耦合限制**：TCM设计要求运动序列与条件嵌入具有相同的时间长度，难以直接处理文本、场景描述等静态条件或时间分辨率不一致的多模态输入。

### 与SOTA的全面比较

在音乐到舞蹈任务上，TCM与**EDGE**（Tseng et al., CVPR 2023）、**Bailando**（Siyao et al., CVPR 2022）等代表性方法进行了全面对比（Table 4），在FID_k（20.66）、BAS（0.2761）等核心指标上取得最优或次优结果。在自我中心视频到运动任务上，TCM相比**EgoEgo**（Li et al., CVPR 2023）在MPJPE（116.3 vs 120.5）和加速度误差（6.2 vs 7.8）上均有提升（Table 5），定性可视化（Fig. 5）显示TCM生成的动作更加连贯且与自我中心视角的线索更一致。

![[assets/figures/papers/paper_list_l1928_TCM_Learning_Human_Motion_with_Temporally_Conditional_Mamba/figures/009_Table_4.jpg]]
*Table 4: Comparison with State-of-the-art methods on music-to-dance task. Bold indicates the best results, and underlined indicates the second-best results*

![[assets/figures/papers/paper_list_l1928_TCM_Learning_Human_Motion_with_Temporally_Conditional_Mamba/figures/013_Figure_5.jpg]]
*Figure 5: Qualitative comparison of human motion estimation from the egocentric task. Our method produces more coherent and accurate motion compared to EgoEgo. For additional visualizations, please refer to our demo video*

### 补充图表

![[assets/figures/papers/paper_list_l1928_TCM_Learning_Human_Motion_with_Temporally_Conditional_Mamba/figures/011_Table_6.jpg]]
*Table 6: Performance comparison between proposed and other methods on human dance estimation from egocentric and music. Bold indicates the best results, and underline indicates the second-best results*



## 定位与知识库关联

### 1. 核心贡献与问题定位

**瓶颈诊断**：现有基于扩散模型的人体运动生成方法（如**EDGE**（Tseng et al., CVPR 2023）、**Bailando**（Siyao et al., CVPR 2022））主要通过交叉注意力（Cross-Attention）在Transformer或Mamba层之间全局融合时间条件信号（如音乐节拍、头部轨迹）。这种设计缺乏逐步的时间对齐能力，导致生成的运动与条件信号之间存在明显的时序偏差——运动节拍滞后或超前于音乐节拍，头部轨迹偏离真实路径。

**调控旋钮**：本文提出**时间条件Mamba（Temporally Conditional Mamba, TCM）**，将时间条件信号直接注入Mamba块的选择矩阵 $\widetilde{\mathbf{B}}$ 和 $\widetilde{\mathbf{C}}$ 的仿射调制中（Eq. 6-7），使状态空间的演化过程在每个时间步都依赖于外部条件，实现自回归的时序对齐。

**核心洞察**：利用线性参数变化状态空间模型的思想，对Mamba的输入/输出矩阵进行逐时间步的条件调制（缩放与偏移），让循环动态可以灵活适应不同的外部条件，从而在保持长序列建模能力的同时显著提升时间一致性和条件一致性。

### 2. 与现有工作的关系图谱

#### 2.1 与Mamba系列的关系

- **Vanilla Mamba**（内部基线）：标准Mamba块仅通过自适应层归一化（AdaLN）融合全局条件，其选择矩阵 $\mathbf{B}$ 和 $\mathbf{C}$ 仅依赖于输入 $\mathbf{x}$ 本身，不直接感知外部条件信号。TCM在此基础上将条件嵌入 $\mathbf{m}_l$ 引入 $\widetilde{\mathbf{B}}$ 和 $\widetilde{\mathbf{C}}$ 的生成过程，实现了从“输入感知”到“条件感知”的跃升。消融实验（Table 2）显示，移除TCM块导致节拍对齐分数（BAS）从0.2761降至0.2434，FID_k从20.66升至25.61，证实TCM是时序对齐的关键组件。

- **Spatial Mamba**：TCM专注于时间维度的条件融合，而Spatial Mamba将运动表示从时间域重排至空间域（关节维度），用标准Mamba建模关节间的空间依赖。两者互补，共同构成完整的时空建模框架。

#### 2.2 与交叉注意力机制的关系

- **Cross-Attention基线**（内部基线）：在Mamba/Transformer层中插入交叉注意力模块来注入时间条件，是**EDGE**等方法的典型设计。TCM与之的核心区别在于条件注入的位置和方式：
  - 交叉注意力在层间进行全局条件融合，缺乏逐帧对齐能力；
  - TCM在Mamba的循环动态内部进行逐时间步的条件调制，使条件信号直接参与状态演化。

  定量对比（Table 1）显示，TCM在AIST++音乐到舞蹈任务上的BAS达到0.2761，远超交叉注意力的0.2411；在长序列（25s）场景下，TCM的FID_k仅从20.66增至23.82，而交叉注意力从25.61猛增至31.36（Table 3），展现出显著更优的长程生成能力。

#### 2.3 与扩散模型基线的关系

- **EDGE**（Tseng et al., CVPR 2023）：音乐到舞蹈生成的代表性扩散模型，采用交叉注意力融合音乐条件。TCM在相同扩散框架下替换条件融合机制，在FID_k（20.66 vs. 23.43）和BAS（0.2761 vs. 0.2411）上均实现显著提升（Table 1）。

- **Bailando**（Siyao et al., CVPR 2022）：结合演员-评论家GPT的音乐驱动舞蹈生成模型。TCM在AIST++上全面超越Bailando（Table 4），在运动质量（FID_k）、多样性（Div_k）和节拍对齐（BAS）三个维度均取得更优结果。

- **EgoEgo**（Li et al., CVPR 2023）：基于Transformer解码器的自我中心视频到人体运动估计模型。TCM在头部方向误差（O_head: 0.15 vs. 0.24）、头部平移误差（T_head: 112.6 vs. 140.3）和MPJPE（116.3 vs. 139.4）上均显著优于EgoEgo（Table 5）。

### 3. 适用边界与能力范围

**已验证的任务域**：
- 音乐到舞蹈生成（AIST++数据集）
- 自我中心视频到人体运动估计
- 自我中心视频+音乐联合条件的人体运动估计
- 物体轨迹驱动的人体运动生成

**方法的核心假设**：
1. 运动序列与条件嵌入具有相同的时间长度——TCM的逐帧调制要求条件信号在时间维度上与运动序列对齐。
2. 条件信号具有时序结构——TCM的设计天然适合音乐节拍、头部轨迹、物体轨迹等时序条件，对静态条件（如文本描述、场景标签）的适配性未经验证。

### 4. 局限性与开放问题

#### 4.1 已知局限

1. **条件类型受限**：当前TCM设计要求运动序列与条件嵌入具有相同的时间长度，难以直接处理文本、场景描述等静态或时变分辨率不一致的条件输入。这是方法的核心架构约束。

2. **极端运动的鲁棒性不足**：在自我中心视频到运动任务中，极端的、突然的头部运动仍会导致生成动作的准确度下降。这暗示TCM的条件调制机制在应对快速变化的条件信号时可能存在响应延迟或过平滑问题。

3. **物理合理性缺陷**：生成的运动可能包含足部滑动和抖动伪影。这是扩散模型生成人体运动的共性问题，TCM并未引入额外的运动学约束（如速度/加速度损失、显式足部接触建模）来解决。

4. **超长序列未探索**：虽然TCM在25s序列上表现优于交叉注意力，但尚未验证在数分钟级超长序列下的稳定性与计算效率。Mamba的线性复杂度理论上支持长序列，但条件调制的累积效应可能导致漂移。

#### 4.2 开放问题

1. **多模态条件融合**：如何扩展TCM以适配静态条件或时间分辨率不一致的多模态输入（如文本+音乐）？可能的路径包括将静态条件映射为时间不变的条件嵌入，或设计条件投影层统一不同时间分辨率的输入。

2. **物理约束集成**：能否通过引入运动学约束（如足部接触标签、物理仿真）进一步消除足部滑动和抖动？这需要在扩散采样过程中或后处理阶段加入约束项，可能与TCM的条件调制机制产生交互。

3. **跨领域泛化**：TCM的条件感知调制机制是否可以推广到其他时间序列生成任务（如语音合成、生理信号建模、金融时序预测）？这需要验证仿射调制在不同模态条件信号下的有效性。

4. **推理效率优化**：在实时/低延迟应用场景中，TCM的推理效率能否通过模型蒸馏、量化或专用硬件部署进一步优化？当前Table 1报告的推理时间基于DDIM 50步采样，仍有压缩空间。

5. **鲁棒性增强**：如何处理自我中心视频中极端的头部运动或遮挡情况？可能需要引入不确定性建模或自适应条件权重机制，在条件信号不可靠时降低其影响。

### 5. 方法定位总结

TCM在人体运动生成领域的方法谱系中处于**条件融合机制创新**的位置：它不改变扩散框架或Mamba的宏观架构，而是重新设计了条件信号进入状态空间模型的方式。与交叉注意力的“层间全局融合”相比，TCM的“循环内逐帧调制”实现了更精细的时序对齐，这一设计思想可追溯到线性参数变化系统（LPV）的控制理论传统，但在深度生成模型中尚属首次系统性地应用于人体运动生成。该方法在时序条件驱动的运动生成任务上建立了新的性能标杆，但其对静态条件的适配性和物理合理性增强仍是后续工作的重要方向。



## 原文 PDF

![[paperPDFs/SIGGRAPH_ASIA_2025/TCM_Learning_Human_Motion_with_Temporally_Conditional_Mamba.pdf]]
