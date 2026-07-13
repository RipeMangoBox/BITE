---
title: "DeepPhase: periodic autoencoders for learning motion phase manifolds"
type: paper
paper_level: A
venue: TOG
year: 2022
pdf_ref: paperPDFs/TOG_2022/DeepPhase_periodic_autoencoders_for_learning_motion_phase_manifolds.pdf
code_link: https://github.com/sebastianstarke/AI4Animation/tree/master/AI4Animation/SIGGRAPH_2022
project_link: https://github.com/sebastianstarke/AI4Animation/tree/master/AI4Animation/SIGGRAPH_2022
aliases:
- PA
- DeepPhase
tags:
- TOG_2022
- topic/representation_self_supervised_transfer
- topic/representation_self_supervised_transfer/representation_learning
core_operator: "通过学习多个局部周期性成分（相位、幅度、频率等）来分解运动，构建一个能够自然对齐时间与空间的相位流形。"
primary_logic: "即使是复杂或非周期性运动，也可视为多个局部周期性运动的组合；将运动编码为多通道的正弦信号，并由自编码器从数据中无监督地学习这些信号的参数，可以产生一个在特征距离上更具区分性的流形，从而改善运动对齐和合成质量。"
claims:
- "所提方法提取的多维相位空间能够有效聚类动画，并在特征距离上提供比原始运动空间更好的相似性度量。"
- "在运动匹配任务中，使用学习的相位特征，其对齐误差（0.034）远低于基于接触的相位（0.146）和启发式主成分分析（0.074）。"
- "使用相位特征的神经运动控制器在多项任务（包括双足/四足运动、风格化运动、舞蹈、足球运球）中产生了更生动的运动（更高的平均关节旋转速度）并减少了脚部滑动。"
- "相位流形的2D PCA投影呈现出与极坐标类似的一致结构，其中角度表示时序，幅度表示运动速度，而传统的速度/全连接嵌入则呈现混乱分布。"
---

# DeepPhase: periodic autoencoders for learning motion phase manifolds

> [!tip] 核心洞察
> 即使是复杂或非周期性运动，也可视为多个局部周期性运动的组合；将运动编码为多通道的正弦信号，并由自编码器从数据中无监督地学习这些信号的参数，可以产生一个在特征距离上更具区分性的流形，从而改善运动对齐和合成质量。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | DeepPhase：用于学习运动相位流形的周期性自编码器 |
| 英文题名 | DeepPhase: periodic autoencoders for learning motion phase manifolds |
| 会议/期刊 | TOG 2022 |
| Links | [paper](https://doi.org/10.1145/3528223.3530178) · [GitHub](https://github.com/sebastianstarke/AI4Animation/tree/master/AI4Animation/SIGGRAPH_2022) |
| Topic | #topic/representation_self_supervised_transfer #topic/representation_self_supervised_transfer/representation_learning |
| Method | Periodic Autoencoder |
| Dataset | Style and Dance Dataset |

> [!tip] 效果简介
> - Style and Dance Dataset 上，Alignment Error (average distance between joint pairs of 10 matched poses over 10000 queries) 为 0.034，对比 0.146 (Contact-based), 0.074 (PCA Heuristic)，变化 -76.7% vs Contact-based, -54.1% vs PCA Heuristic。

## 概要

### 问题背景

在角色动画合成中，运动数据具有稀疏且高度非线性的特点。现有方法在时间和空间上对齐运动时面临根本性困难——合成结果往往出现平滑化、僵硬或失真等问题。其瓶颈在于：缺乏一种能够自然捕捉运动内在周期结构、并在时间和空间维度上同时提供有效对齐的特征表示。

### 核心思想

本文的核心洞察是：即使是复杂或非周期性运动，也可以视为多个局部周期性运动的组合。基于此，DeepPhase 提出了一种**周期性自编码器（Periodic Autoencoder）**，将角色运动无监督地分解为多个潜在通道，每个通道捕获不同身体部位的非线性周期性（相位、幅度、频率、偏移等参数）。这些通道共同构成一个**相位流形（phase manifold）**，其上的特征距离能够提供比原始运动空间更具区分性的相似性度量，从而自然地实现时间与空间的对齐。

### 方法定位

与现有工作的关键区别在于相位的提取方式：

- **传统方法**：依赖手工定义的相位变量，如基于足部接触的启发式规则（**Contact-based phase**, Starke et al., TOG 2020）或 PCA 启发式方法（**PCA heuristic phase**, Mason et al., arXiv 2022），以及全局相位方法 **PFNN**（Holden et al., TOG 2017）和局部相位方法 **LMP**（Starke et al., TOG 2020）。
- **本文方法**：通过周期性自编码器从大规模非结构化运动数据中**无监督地学习**多维相位变量。编码器将运动映射为潜在嵌入，可微 FFT 层从中推导幅度、频率和偏移，全连接层预测相位偏移，最终以参数化正弦函数重建潜在空间，再由解码器恢复运动。这一设计使相位流形天然具备有序的循环结构。

### 主要结果

**运动对齐**：在风格与舞蹈数据集上，本文学习的相位特征的对齐误差为 **0.034**，相比基于接触的相位（0.146）降低 **76.7%**，相比 PCA 启发式方法（0.074）降低 **54.1%**（Table 4）。

**运动合成质量**：将相位流形特征作为神经运动控制器（MoE 门控网络）的输入，在双足/四足运动、风格化运动、舞蹈及足球运球等多项任务中，合成的运动表现出更高的平均关节旋转速度（运动更生动），并显著减少了脚部滑动（Table 2, Table 3）。

**流形结构**：相位流形的 2D PCA 投影呈现出与极坐标类似的、按时间和幅度有序排列的循环结构；相比之下，传统速度空间和全连接潜在空间的投影则呈现混乱分布（Fig. 6, Fig. 7），验证了周期性约束对流形结构的根本性改善。

### 局限与开放问题

- 舞蹈动作合成无法泛化到任意音乐，需结合能学习音乐上下文与动作映射的模型。
- 相位流形能有效聚类动作，但不能解决运动技能选择问题，仍需用户控制或概率采样。
- 相位通道数是一个关键超参数，其最优值依赖于数据量和运动类型，通道过少可能导致错误对齐，过多则可能导致门控网络过分割。
- 开放问题：周期性自编码器能否在大规模异构数据集上预训练，作为通用模型为未见过的角色运动计算对齐？该框架能否应用于视频、声音或语音等其他模态数据？



### 运动合成中的核心瓶颈

角色动画合成是计算机图形学中的长期挑战，其核心难点在于如何生成自然、生动且时序连贯的运动序列。现有数据驱动方法面临一个根本性瓶颈：**运动数据稀疏且高度非线性**，不同运动片段在时间和空间维度上难以有效对齐。这一瓶颈直接导致合成运动出现平滑化、僵硬或失真等典型伪影——模型为规避不连续过渡，倾向于输出“平均化”的姿态，牺牲了运动的锐利度和表现力。

### 现有相位方法的局限

为缓解上述问题，研究者引入了相位（phase）概念来表征运动的周期性时序。早期工作如 **PFNN**（Holden et al., TOG 2017）采用全局相位变量，将完整步态周期映射为单一的 $[0, 1)$ 标量。这种方式虽能处理简单的双足行走，但无法捕捉身体不同部位的非线性周期行为——例如，挥手动作中手臂的频率远高于腿部步频，全局相位无法同时编码这两种节律。

随后，**局部相位方法**（如 **LMP**，Starke et al., TOG 2020）通过基于足部接触或启发式规则的手动定义，为各关节分配独立相位，部分缓解了多节律问题。然而，这类方法存在根本性缺陷：

- **依赖手工规则**：接触式相位需要精确的足部接地检测，对舞蹈、足球运球等足部接触不明确的运动类型泛化能力差；
- **启发式局限**：基于主成分分析（PCA）的启发式相位（Mason et al., arXiv 2022）虽能自动提取，但提取的特征缺乏明确的周期性结构，难以在特征空间中形成有意义的流形。

### 核心洞察与本文动机

本文的出发点源于一个关键观察：**即使是复杂或非周期性运动，也可视为多个局部周期性运动的组合**。人体运动本质上由不同频率、不同幅度的节律性成分叠加而成——腿部以低频驱动步态循环，手臂可能以高频执行风格化摆动，躯干则维持相对稳定的偏移。如果能够从数据中自动解耦这些多通道的周期性成分，就能构建一个自然对齐时间与空间的相位流形，从根本上改善运动合成质量。

基于此洞察，本文提出 **Periodic Autoencoder**（周期性自编码器），一种无需任何相位标签、完全从非结构化运动数据中无监督学习多维相位变量的神经网络架构。该方法将运动分解为多个潜在通道，每个通道捕获特定身体部位的非线性周期性，并在特征空间中形成一个在距离度量上更具区分性的相位流形，为下游的运动生成与匹配任务提供结构化的时序表征。



## 核心方法与创新机理

### 从手动定义到无监督学习的相位提取

运动合成领域长期依赖手动定义的相位变量来对齐时间与空间维度上的运动帧。早期工作如 **PFNN**（Holden et al., ACM TOG 2017）使用全局标量相位，**LMP**（Starke et al., ACM TOG 2020）则通过脚部接触事件定义局部相位。这类启发式规则存在两个根本性缺陷：其一，接触检测对噪声敏感且依赖阈值调参；其二，单变量相位无法捕捉身体不同部位的非线性周期特性——例如舞蹈中手臂与腿部的运动频率可能截然不同。

DeepPhase 的核心创新在于将相位提取从**规则驱动**转变为**数据驱动**。所提出的 **Periodic Autoencoder** 能够在无监督条件下，从大规模非结构化运动捕捉数据中自动学习多维相位变量。其关键设计体现在以下三个 changed slots：

**1. 相位提取方式：从接触/启发式规则到无监督学习**

传统方法（如 Contact-based phase）通过检测脚部与地面的接触事件来定义局部相位，或使用 PCA 启发式方法（Mason et al., arXiv 2022）从运动数据中提取主成分作为相位。这些方法本质上是人工设计的特征工程，难以泛化到缺少明确接触事件的动作类型（如游泳、挥手）。

Periodic Autoencoder 则通过重构目标端到端地学习相位：编码器将输入运动映射为低维潜在嵌入，解码器从参数化的潜在空间重建原始运动。网络在最小化重构误差的过程中，自然习得了能够有效表征运动时序结构的相位变量。定量实验表明，在风格与舞蹈数据集的对齐任务中，学习到的相位特征的对齐误差仅为 **0.034**，相比基于接触的相位（0.146）降低 **76.7%**，相比 PCA 启发式方法（0.074）降低 **54.1%**（Table 4）。

**2. 潜在空间约束：从无约束嵌入到正弦函数参数化**

标准卷积自编码器（Holden et al., SIGGRAPH Asia 2015）的潜在空间没有结构性约束，导致学习到的嵌入在 PCA 投影下呈现杂乱无章的分布（Fig. 6 中行），无法为运动对齐提供有意义的距离度量。

DeepPhase 强制每个潜在通道服从正弦函数形式：

$$\hat{\mathbf{L}} = \mathbf{A} \cdot \sin(2\pi \cdot (\mathbf{F} \cdot \mathcal{T} - \mathbf{S})) + \mathbf{B}$$

其中幅度 $\mathbf{A}$、频率 $\mathbf{F}$、偏移 $\mathbf{B}$ 通过可微 FFT 层从潜在嵌入的功率谱中推导，相位偏移 $\mathbf{S}$ 则由全连接层预测的 2D 向量经 atan2 计算得到。这一参数化设计将潜在空间显式约束为多个正弦波的叠加，使每个通道天然具备周期性，从而构建出结构化的相位流形。

消融实验证实了可微 FFT 层的必要性：若直接由网络学习幅度和频率参数，不仅相位会振荡，幅度和频率也会随时间剧烈波动，导致相位流形充满噪声。FFT 层通过频域变换提供了稳定的参数估计，显著稳定了训练过程。

**3. 运动对齐特征：从原始姿态/速度到低维相位流形坐标**

传统运动合成方法直接使用关节位置或速度作为对齐特征进行最近邻搜索，或作为神经网络控制器的输入。这类特征维度高且缺乏时序结构，容易在运动匹配中产生时间上的错位。

DeepPhase 从相位流形中提取低维特征作为对齐表示。每个相位通道生成一对 2D 坐标：

$$\mathcal{P}_{2i-1}^{(t)} = \mathbf{A}_i^{(t)} \cdot \sin(2\pi \cdot \mathbf{S}_i^{(t)}), \quad \mathcal{P}_{2i}^{(t)} = \mathbf{A}_i^{(t)} \cdot \cos(2\pi \cdot \mathbf{S}_i^{(t)})$$

该设计将幅度与相位偏移统一编码为流形上的点，使得特征距离在空间和时间上同时具有判别力。2D PCA 投影显示，相位流形呈现出与极坐标一致的有序循环结构，其中角度表示时序，幅度表示运动速度（Fig. 6 下行）；而速度空间和全连接潜在空间的投影则分别呈现随机分布和较少结构化的模式（Fig. 6 上、中行）。在运动匹配任务中，相位特征能够将搜索索引聚焦在当前帧附近，而姿态/速度特征则无法保证这一性质（Fig. 15）。

### 创新点的协同效应

上述三个 changed slots 并非孤立改进，而是形成了一条因果链：**正弦参数化约束**赋予了潜在空间周期性结构，使得**无监督学习**能够自动发现运动中的多维周期成分，进而产出的**低维相位流形坐标**在特征距离上比原始运动空间更具判别力。这一协同效应解释了为何 DeepPhase 在多项下游任务中一致优于基于规则的传统方法——从双足/四足运动的生动度提升（Table 2），到脚部滑动的减少（Table 3），再到多相位舞蹈动作的对齐精度跃升（Table 4）。



![[assets/figures/papers/paper_list_l25_https_doi_org_10_1145_3528223_3530178/figures/002_Figure_2.jpg]]
*Figure 2: Network architecture of the Periodic Autoencoder for extracting multi-dimensional phase manifolds from unstructured motion data*

DeepPhase 的核心是一个名为 **Periodic Autoencoder** 的无监督学习框架，其设计目标是：给定任意非结构化的运动捕捉数据，自动学习一个多维的**周期性潜在空间**（即相位流形），使得运动的时序与空间结构在该流形上自然对齐。整个 pipeline 由以下模块串联构成，形成“编码 → 周期性参数化 → 解码”的闭环：

1. **时序卷积编码器 (Temporal Convolutional Encoder)**  
   输入为经过根节点对齐和窗口均值中心化处理的 3D 关节速度轨迹 $\mathbf{X}$。编码器 $g(\cdot)$ 采用两层时序卷积（每层后接批归一化与 tanh 激活），将运动曲线压缩为低维潜在嵌入 $\mathbf{L} = g(\mathbf{X})$。这一嵌入尚未具备周期性约束。

2. **可微 FFT 层与幅度/频率/偏移推导**  
   对 $\mathbf{L}$ 的每个通道执行可微实数快速傅里叶变换，得到傅里叶系数 $\mathbf{c} = FFT(\mathbf{L})$ 及功率谱 $\mathbf{p}_{i,j} = \frac{2}{N} |\mathbf{c}_{i,j}|^2$。随后从功率谱中解析出每个通道的全局形状参数：
   - 幅度 $\mathbf{A}_i = \sqrt{\frac{2}{N} \sum_{j=1}^{K} \mathbf{p}_{i,j}}$
   - 频率 $\mathbf{F}_i = \frac{\sum_{j=1}^{K} (\mathbf{f}_j \cdot \mathbf{p}_{i,j})}{\sum_{j=1}^{K} \mathbf{p}_{i,j}}$
   - 偏移 $\mathbf{B}_i = \frac{\mathbf{c}_{i,0}}{N}$  
   这一设计替代了直接由网络学习这些参数，显著稳定了训练过程，避免了参数在时间轴上的剧烈振荡。

3. **相位偏移预测**  
   编码器输出的 $\mathbf{L}_i$ 同时送入一个全连接层，预测 2D 向量 $(s_x, s_y)$，并通过 $\mathbf{S}_i = \mathrm{atan2}(s_y, s_x)$ 得到每个通道的相位偏移 $\mathbf{S}$。至此，每个潜在通道的周期性函数参数 $(A, F, B, S)$ 全部确定。

4. **参数化潜在空间重建**  
   利用上述参数，在时间窗口 $\mathcal{T}$ 上重建参数化潜在曲线：
   $$\hat{\mathbf{L}} = f(\mathcal{T}; \mathbf{A}, \mathbf{F}, \mathbf{B}, \mathbf{S}) = \mathbf{A} \cdot \sin(2\pi \cdot (\mathbf{F} \cdot \mathcal{T} - \mathbf{S})) + \mathbf{B}$$
   这一强制正弦约束使得潜在空间天然具备周期性结构。

5. **卷积解码器 (Convolutional Decoder)**  
   解码器 $h(\cdot)$ 将 $\hat{\mathbf{L}}$ 映射回运动曲线 $\mathbf{Y} = h(\hat{\mathbf{L}})$。整个网络以最小化重建损失 $\mathcal{L} = MSE(\mathbf{X}, \mathbf{Y})$ 进行端到端训练，无需任何相位标签。

6. **相位流形特征提取**  
   训练完成后，从每个通道提取 2D 相位流形坐标：
   $$\mathcal{P}_{2i-1}^{(t)} = \mathbf{A}_i^{(t)} \cdot \sin(2\pi \cdot \mathbf{S}_i^{(t)}), \quad \mathcal{P}_{2i}^{(t)} = \mathbf{A}_i^{(t)} \cdot \cos(2\pi \cdot \mathbf{S}_i^{(t)})$$
   这样得到的低维相位特征（维度为 $2M$，$M$ 为相位通道数）同时编码了运动的时序相位和运动幅度，可作为下游任务的输入。

**下游应用接口**  
- **神经运动控制器 (MoE)**：将相位流形特征作为门控网络的输入，自回归地预测下一帧姿态。  
- **运动匹配 (Motion Matching)**：用相位特征替代传统的姿态/速度特征进行最近邻搜索，实现时序对齐的帧检索。

**关键设计选择**  
- 相位通道数 $M$ 是任务相关的超参数：双足/四足运动取 5，风格化运动取 10，舞蹈取 8，足球运球取 6。通道数过少会导致错误对齐，过多则可能使门控网络过分割。  
- 输入采用窗口均值中心化的速度轨迹而非绝对位置，使网络聚焦于运动动态而非全局姿态。  
- 可微 FFT 层的引入是训练稳定性的关键：消融实验表明，若直接由网络学习幅度和频率，参数会在时间轴上剧烈振荡，导致相位流形充满噪声。



### 整体架构

Periodic Autoencoder 的核心是一个时序卷积自编码器，其架构沿用了 **Holden et al., SIGGRAPH Asia 2015** 的卷积自编码器结构。输入为角色根空间下的3D关节速度轨迹，经过窗口均值中心化后送入编码器。编码器由两层卷积层组成，每层后接批归一化和 tanh 激活函数，将运动序列 $\mathbf{X}$ 映射为低维潜在嵌入 $\mathbf{L}$：

$$\mathbf{L} = g(\mathbf{X})$$

解码器 $h$ 则将参数化后的潜在空间 $\hat{\mathbf{L}}$ 重构回运动曲线 $\mathbf{Y}$：

$$\mathbf{Y} = h(\hat{\mathbf{L}})$$

整个网络以均方误差作为重建损失进行端到端训练：

$$\mathcal{L} = MSE(\mathbf{X}, \mathbf{Y})$$

### 周期性潜在空间参数化

这是方法的核心创新点。传统自编码器的潜在空间没有结构性约束，而 Periodic Autoencoder 强制每个潜在通道服从正弦函数形式。参数化过程分为两步：

**第一步：通过可微 FFT 层推导幅度、频率和偏移。** 对潜在嵌入 $\mathbf{L}$ 的每个通道执行实数快速傅里叶变换，得到傅里叶系数 $\mathbf{c}$ 和功率谱 $\mathbf{p}$：

$$\mathbf{c} = FFT(\mathbf{L}), \quad \mathbf{p}_{i,j} = \frac{2}{N} |\mathbf{c}_{i,j}|^2$$

其中 $N$ 为时间窗口长度，$K$ 为使用的频率分量数（取前 $K$ 个非直流分量）。从功率谱中推导各通道的幅度 $\mathbf{A}_i$、频率 $\mathbf{F}_i$ 和偏移 $\mathbf{B}_i$：

$$\mathbf{A}_i = \sqrt{\frac{2}{N} \sum_{j=1}^{K} \mathbf{p}_{i,j}}, \quad \mathbf{F}_i = \frac{\sum_{j=1}^{K} (\mathbf{f}_j \cdot \mathbf{p}_{i,j})}{\sum_{j=1}^{K} \mathbf{p}_{i,j}}, \quad \mathbf{B}_i = \frac{\mathbf{c}_{i,0}}{N}$$

其中 $\mathbf{f}_j$ 为第 $j$ 个频率分量对应的频率值。消融实验表明，使用可微 FFT 层来推导这些参数（而非让网络直接学习）显著稳定了训练过程，避免了幅度和频率沿时间的大幅振荡。

**第二步：通过全连接层预测相位偏移。** 对每个潜在通道 $\mathbf{L}_i$，使用全连接层预测一个2D向量，再通过 atan2 函数计算相位偏移 $\mathbf{S}_i$：

$$(s_x, s_y) = FC(\mathbf{L}_i), \quad \mathbf{S}_i = \mathrm{atan2}(s_y, s_x)$$

最终，参数化潜在空间 $\hat{\mathbf{L}}$ 由学习到的幅度、频率、偏移和相位偏移共同定义，在时间窗口 $\mathcal{T}$ 上重建为正弦曲线：

$$\hat{\mathbf{L}} = f(\mathcal{T}; \mathbf{A}, \mathbf{F}, \mathbf{B}, \mathbf{S}) = \mathbf{A} \cdot \sin(2\pi \cdot (\mathbf{F} \cdot \mathcal{T} - \mathbf{S})) + \mathbf{B}$$

这一设计的因果机制在于：FFT 层从全局时间窗口提取了信号的频域结构（幅度、频率、偏移），保证了参数的稳定性；而相位偏移则由编码器根据局部运动上下文灵活预测，使模型能够捕捉运动相位的瞬时变化。

### 相位流形构建

训练完成后，每个时间步 $t$ 的相位流形特征 $\mathcal{P}$ 由各通道的幅度和相位偏移组合而成，每个通道贡献两个维度：

$$\mathcal{P}_{2i-1}^{(t)} = \mathbf{A}_i^{(t)} \cdot \sin(2\pi \cdot \mathbf{S}_i^{(t)}), \quad \mathcal{P}_{2i}^{(t)} = \mathbf{A}_i^{(t)} \cdot \cos(2\pi \cdot \mathbf{S}_i^{(t)})$$

这样设计的目的是让相位特征同时在空间和时间上聚类动画：幅度编码运动速度，相位偏移编码时序位置。相位通道数 $M$ 是一个关键超参数——双足/四足运动设为5，风格化运动设为10，舞蹈设为8，足球运球设为6。通道数过少可能导致错误对齐，过多则可能导致下游门控网络的过分割。

### 相位更新机制

在运动合成阶段，未来时刻 $t+\Delta t$ 的相位状态通过当前相位向量与预测的频率进行外推，使用球面线性插值来保持相位流形上的平滑过渡：

$$\mathcal{P}_{t + \Delta t}^{\prime} = A_{t + \Delta t} \cdot I(R(\theta) \cdot \mathcal{P}_t, \mathcal{P}_{t + \Delta t}), \qquad \theta = \Delta t \cdot 2\pi \cdot F_{t + \Delta t}$$

其中 $I$ 为球面线性插值函数，$R(\theta)$ 为旋转矩阵。这一机制使得相位特征在运动匹配任务中能够自回归地索引下一帧姿态，且索引结果紧邻当前帧（见 Fig. 15 的定量验证）。



## 实验与关键发现

### 数据集与实验设置

本文在五类运动数据集上分别训练独立的周期性自编码器和运动生成器，数据集之间无重复（Table 1）。输入为根空间下的3D关节速度轨迹，经窗口均值中心化后送入编码器。编码器由两层时间卷积、批归一化和tanh激活组成。相位通道数根据运动类型设置为：双足/四足运动5通道，风格化运动10通道，舞蹈8通道，足球6通道。训练在NVIDIA RTX 3080上完成，较小数据集耗时不足一小时。

![[assets/figures/papers/paper_list_l25_https_doi_org_10_1145_3528223_3530178/figures/008_Table_1.jpg]]
*Table 1: The motion capture dataset used to train our model. Each dataset is used to train different Periodic Autoencoders and motion generators*

### 相位流形的结构验证

相位流形在多个维度上展现出显著优于传统特征空间的结构化特性。将不同运动类型的特征分布通过2D PCA投影可视化（Fig. 6），相位空间呈现与极坐标一致的有序结构——角度编码时间进程，幅度编码运动速度。相比之下，全连接潜在空间仅形成较少结构化的团簇，而速度空间则呈现近乎随机的散点分布。在单段运动的时间序列嵌入中（Fig. 7），相位流形的轨迹沿清晰的循环路径行进，相邻帧在流形上保持邻近；全连接嵌入的循环结构明显弱化，速度嵌入则完全丧失时序连续性。对于包含多周期成分的复杂运动（Fig. 8），如手臂摆动频率高于步态的风格化行走，以及多肢体异步运动的舞蹈编排，3D PCA投影清晰揭示了多个嵌套或重叠的子循环，表明各相位通道成功解耦了不同身体部位的独立周期性。

### 运动合成质量评估

以学习到的相位特征作为门控网络输入的神经运动控制器，在多项任务中一致优于基线方法。Table 2以平均关节旋转速度衡量运动生动度：在双足运动（51.2 vs. PFNN的41.3）、双足急转弯（143.5 vs. LMP的113.2）、四足运动（195.7 vs. MANN的184.2）等类别上，本文方法均产生更大幅度的运动。Table 3以着地期间足部速度与最大足速之比衡量足部滑动：双足运动（0.476）、风格化运动（0.279）和舞蹈（0.443）的滑动量均低于对比方法。定性观察进一步印证：急转弯和敏捷动作的边缘更锐利（Fig. 9），四足尾巴摆动更活跃——至少一个相位通道自主学会了以不同于身体其他部位的周期来驱动尾部运动（Fig. 10）。在风格化运动合成中，手臂动作显著更清晰，身体惯性保持更好（Fig. 12），原因在于相位特征同时对齐了上下半身的运动信息。

![[assets/figures/papers/paper_list_l25_https_doi_org_10_1145_3528223_3530178/figures/017_Table_2.jpg]]
*Table 2: The average joint rotations per second for different classes of motions. The proposed method produces more movements in all classes of motions*

![[assets/figures/papers/paper_list_l25_https_doi_org_10_1145_3528223_3530178/figures/018_Table_3.jpg]]
*Table 3: The average amount of foot skating during ground contacts, calculated as the average ratio of the foot speed with respect to the maximum foot speed during contacts in the motion dataset*

### 运动匹配与对齐精度

将相位特征直接用于运动匹配任务，进一步验证了其作为相似性度量的有效性。在自回归搜索中，相位特征索引到的下一帧紧邻当前帧（Fig. 15左），而完整姿态或降维姿态特征则无法保证这一邻近性。扩展到未来多帧的匹配中（Fig. 15右），相位特征始终维持较低的索引偏移。L2距离相似度图（Fig. 18）显示，相位流形在双足冲刺、四足小跑/慢跑和迪斯科舞蹈上的帧间相似度矩阵均呈现出清晰的块对角结构，而姿态/速度特征的相似度矩阵则噪声显著。

![[assets/figures/papers/paper_list_l25_https_doi_org_10_1145_3528223_3530178/figures/016_Figure_15.jpg]]
*Figure 15: The average index of the following frame in the motion capture data when matched with features of the phase manifold, reduced pose and full pose (left) and the average indices of the future frames in the motion capture data when matched with the three feature setups (right)*

在风格与舞蹈数据集上的定量对齐实验中（Table 4），以10000次查询中10对匹配姿态的平均关节对距离作为对齐误差，本文学习的相位特征达到0.034，相比基于接触的相位（0.146）降低76.7%，相比PCA启发式相位（0.074）降低54.1%。定性对比（Fig. 16）显示，在多相位舞蹈动作的对齐中，基于接触的方法因仅依赖脚部接触事件而无法捕捉上肢的独立周期，PCA启发式方法则对噪声敏感，而本文方法实现了上下肢的同步对齐。

![[assets/figures/papers/paper_list_l25_https_doi_org_10_1145_3528223_3530178/figures/019_Table_4.jpg]]
*Table 4: The alignment error for different phase extraction methods. The error is calculated as the average distance between joints pairs of 10 matched poses over 10000 search queries over the style and dance dataset*

### 消融实验

**周期性约束的必要性**：移除潜在空间的正弦参数化约束，即使用标准卷积自编码器，其潜在空间的PCA投影失去极坐标式的有序结构，仅形成无明确时序含义的团簇（Fig. 6中 vs. Fig. 7下）。

**可微FFT层的稳定性**：尝试由网络直接学习幅度、频率和偏移参数，而非通过FFT层推导，导致这些参数沿时间剧烈振荡，相位流形充满噪声。引入可微FFT层显著稳定了训练过程，使各通道收敛为特定幅度和频率范围的带通滤波器（Fig. 4）。

![[assets/figures/papers/paper_list_l25_https_doi_org_10_1145_3528223_3530178/figures/005_Figure_4.jpg]]
*Figure 4: Distribution of amplitudes and frequencies of learned phase channels. Each channel becomes tuned for a specific range of amplitudes and frequencies to decompose the motion, roughly acting like a set of learned band-pass filters. Note that there were no parameter ranges predefined for each phase channel, but they are extracted as needed by the model*

**相位特征作为网络输入**：在运动控制器中移除相位特征输入后，合成运动的手臂动作模糊化，身体惯性丢失（Fig. 12），验证了相位流形特征对运动生成质量的因果贡献。

### 局限与失败模式

相位通道数作为关键超参数，其最优值依赖于数据量和运动复杂度。通道数过少会导致不同周期的运动片段在流形上错误重叠，引起对齐失败；过多则可能使门控网络过分割，损害运动合成的连贯性。舞蹈动作合成无法泛化到任意音乐输入，需要额外模型学习音乐上下文到动作的映射。相位流形虽能有效聚类运动并约束相邻帧的可行过渡，但本身不解决高层运动技能选择问题，仍需用户控制信号或概率采样策略。



## 定位与知识库关联

### 问题定位：从全局相位到局部相位再到学习型相位

在角色动画的运动合成中，如何提取有效的时序相位信息一直是核心瓶颈。早期方法依赖**全局相位变量**，如 **PFNN** (Holden et al., ACM TOG 2017) 使用单一标量相位来编码步态周期，这在处理周期性双足行走时表现良好，但无法应对包含多个独立周期成分的复杂运动（如舞蹈中手臂与腿部的异步运动）。后续工作转向**局部相位**，如 **LMP** (Starke et al., ACM TOG 2020) 和 **MANN** (Zhang et al., ACM TOG 2018) 分别针对双足和四足运动提出了基于接触状态的相位定义，但这些方法的相位提取依赖于手工设计的启发式规则（如脚部接触检测的阈值），难以泛化到非周期性运动或非接触驱动的动作（如尾巴摆动、风格化手臂运动）。

本文的 **Periodic Autoencoder** 直接回应了这一瓶颈：它将相位提取从手工定义转向**无监督学习**，通过强制潜在空间的正弦参数化，使网络从数据中自动发现运动中的多通道周期性结构。这一设计使得方法能够同时处理周期性运动（行走、奔跑）和非周期性运动（舞蹈、足球运球），而无需针对每种运动类型重新设计相位规则。

### 核心差异：潜在空间约束的本质转变

与标准自编码器（如 **Convolutional Autoencoder**，Holden et al., SIGGRAPH Asia 2015）相比，Periodic Autoencoder 的关键改变在于**潜在空间的参数化约束**。标准自编码器的潜在空间是自由学习的，其 PCA 投影呈现杂乱无章的分布（Fig. 6 中间行），无法提供有意义的时序对齐信号。Periodic Autoencoder 则通过三个关键模块实现了结构化约束：

1. **可微 FFT 层**：对每个潜在通道执行快速傅里叶变换，从功率谱中推导幅度 $A$、频率 $F$ 和偏移 $B$，而非让网络直接学习这些参数。消融实验表明，直接学习会导致参数剧烈振荡，而 FFT 层显著稳定了训练过程。
2. **相位偏移预测**：通过全连接层预测 2D 向量，使用 $\mathrm{atan2}$ 计算相位偏移 $S$，避免了角度表示的周期性歧义。
3. **正弦参数化重建**：将潜在空间显式建模为 $\hat{\mathbf{L}} = A \cdot \sin(2\pi \cdot (F \cdot \mathcal{T} - S)) + B$，使潜在通道天然具备周期性。

这一约束的因果效应是：学习到的相位流形在 2D PCA 投影中呈现出与极坐标类似的有序循环结构（Fig. 6 底行），其中角度表示时序、幅度表示运动速度。相比之下，基于接触的相位（Contact-based, Starke et al., 2020）和 PCA 启发式相位（PCA heuristic, Mason et al., arXiv 2022）都无法产生这种结构化流形，导致对齐误差显著偏高（Table 4：Learned 0.034 vs Contact-based 0.146 vs PCA Heuristic 0.074）。

### 相位流形的下游应用与适用边界

Periodic Autoencoder 提取的相位流形并非直接替代运动生成器，而是作为**特征提取前端**嵌入到现有运动合成管线中。论文验证了两种下游应用模式：

- **神经运动控制器**：将相位流形特征作为 MoE（Mixture of Experts）门控网络的输入，自回归地预测下一帧姿态。这一模式在双足/四足运动、风格化运动、舞蹈和足球运球等任务上均产生了更生动的运动（Table 2：更高的平均关节旋转速度）和更少的脚部滑动（Table 3）。
- **运动匹配（Motion Matching）**：使用低维相位向量代替姿态/速度特征进行最近邻搜索。相位特征能够更准确地索引到下一帧的邻近姿态（Fig. 15），且相似度图（Fig. 18）显示出更清晰的周期性结构。

然而，方法的适用边界同样明确：

1. **相位通道数是关键超参数**：通道数需要根据运动类型调整（双足/四足运动 5 通道，风格化运动 10 通道，舞蹈 8 通道，足球 6 通道）。通道数过少可能导致错误对齐，过多则可能导致门控网络过分割。这一权衡意味着方法尚未实现完全自动的超参数选择。
2. **不解决运动技能选择问题**：相位流形能有效聚类动画并缩小相邻帧的过渡空间，但“选择何种运动技能”仍需用户控制或概率采样。
3. **舞蹈合成不能泛化到任意音乐**：需要结合能学习音乐上下文及其与动作映射的模型。

### 局限与开放问题

论文明确指出的局限包括上述超参数敏感性和技能选择问题。此外，在四足运动的尾巴摆动场景中，至少有一个相位通道学习到了与身体其他部分不同周期的尾巴运动（Fig. 10 左），这表明方法能够自动解耦多肢体周期，但解耦的粒度取决于通道数的设置。

开放问题指向两个方向：

1. **跨模态泛化**：Periodic Autoencoder 的正弦参数化框架是否可应用于视频、声音或语音等非运动数据？其核心思想——从非结构化数据中无监督地学习局部周期性成分——在理论上具有跨模态潜力，但需要验证。
2. **大规模预训练**：Periodic Autoencoder 是否可以在大规模异构运动数据集上预训练，作为通用模型为未见过的角色运动计算运动对齐？这类似于 NLP 中的预训练-微调范式，但运动数据的异构性（不同骨骼拓扑、不同运动风格）可能构成挑战。

### 在知识库中的定位

Periodic Autoencoder 处于**学习型运动相位提取**这一细分方向的开端。它继承了自编码器运动压缩的传统（Holden et al., 2015），但通过引入显式的周期性归纳偏置，将潜在空间从“压缩表示”升级为“可解释的相位流形”。与同期或后续工作中基于接触/启发式的相位方法相比，其核心优势在于**无监督性和运动类型无关性**；其核心劣势在于**通道数超参数敏感性和对下游任务的部分依赖**。在方法谱系中，它桥接了手工相位定义与完全端到端运动生成之间的空白，为后续工作（如结合音乐条件的舞蹈生成、跨骨骼运动重定向）提供了可复用的相位特征提取模块。



## 原文 PDF

![[paperPDFs/TOG_2022/DeepPhase_periodic_autoencoders_for_learning_motion_phase_manifolds.pdf]]
