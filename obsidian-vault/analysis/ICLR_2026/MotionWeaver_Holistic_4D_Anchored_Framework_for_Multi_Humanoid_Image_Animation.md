---
title: "MotionWeaver: Holistic 4D-Anchored Framework for Multi-Humanoid Image Animation"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/MotionWeaver_Holistic_4D_Anchored_Framework_for_Multi_Humanoid_Image_Animation.pdf
project_link: null
code_link: null
openreview_forum_id: KjlLwRsiUE
aliases:
- MotionWeaver
tags:
- ICLR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
core_operator: "论文提出的三个关键设计构成因果杠杆：(a) 统一编舞核心(UCC)提取身份无关的运动令牌并通过分组注意力绑定至角色，形成可泛化的统一运动表征；(b) 超场景集成器(HSI)在共享4D空间中通过深度感知注意力与动态C-RoPE融合运动表征与视频潜变量；(c) 分层4D监督(H4S)在高噪声步施加遮挡损失，在低噪声步施加运动级损失，将4D运动先验注入模型。"
primary_logic: "通过将运动与外观彻底解耦并嵌入共享4D时空坐标系，模型能够真正理解运动动态而非简单渲染控制信号，从而在多样类人形态和密集交互遮挡下实现稳健的动画生成。"
claims:
- "MotionWeaver在DualDynamics基准上所有指标均超越现有方法，FVD达到145.7（次优164.6）"
- "消融实验表明移除任一核心组件（MNP、GAM、DAA、DCR、H4S）均导致性能明显下降，其中DCR移除使FVD恶化至225.6"
- "定性结果展示MotionWeaver是唯一能正确处理密集角色间交互与遮挡的方法，身份保持和运动精度均显著优于基线"
- "用户研究显示MotionWeaver在视觉质量、运动对齐、交互连贯性、遮挡处理、角色保持五个维度均获得最高偏好票数，遮挡处理维度优势高达68%"
---

# MotionWeaver: Holistic 4D-Anchored Framework for Multi-Humanoid Image Animation

> [!tip] 核心洞察
> 通过将运动与外观彻底解耦并嵌入共享4D时空坐标系，模型能够真正理解运动动态而非简单渲染控制信号，从而在多样类人形态和密集交互遮挡下实现稳健的动画生成。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | MotionWeaver：面向多类人角色图像动画的整体4D锚定框架 |
| 英文题名 | MotionWeaver: Holistic 4D-Anchored Framework for Multi-Humanoid Image Animation |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=KjlLwRsiUE) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction |
| Method | MotionWeaver |
| Dataset | DualDynamics |

> [!tip] 效果简介
> - DualDynamics 上，FVD ↓ 为 145.7，对比 164.6 (RealisDance-DiT)，变化 -18.9。
> - DualDynamics 上，CLIP ↑ 为 0.9041，对比 0.8813 (RealisDance-DiT)，变化 +0.0228。

## 概要

### 问题瓶颈

现有角色图像动画方法在设计上普遍以**单人类角色**为中心，无法有效应对多类人角色（真人、机器人、拟人动物、游戏化身等）共存的复杂场景。其根本瓶颈体现在三个层面：

1. **运动表征与形态纠缠**：主流方法依赖骨架图或SMPL渲染图作为运动信号，这些表征天然携带身体比例、形状等身份信息。在多人物场景中，不同角色的运动信号相互混叠，模型难以将运动指令准确绑定到目标个体，导致身份漂移和运动错位。
2. **缺乏显式4D时空建模**：现有方法在融合运动信号与视频特征时多采用朴素的交叉注意力，未显式编码深度（z轴）和时间（t轴）信息。这使得模型无法有效解析角色间的遮挡关系和透视尺寸错觉，在密集交互场景下尤为脆弱。
3. **训练策略耦合运动与外观**：仅依赖2D像素级MSE损失进行监督，运动先验与外观生成相互耦合，模型倾向于过拟合人类外观模式，难以泛化到非人类形态。

### 核心方法定位

**MotionWeaver** 提出了一种**整体4D锚定框架**，通过三个关键设计构成因果杠杆，系统性地解耦运动与外观并嵌入共享时空坐标系：

| 模块 | 核心机制 | 解决的问题 |
|------|----------|------------|
| **统一编舞核心 (UCC)** | 将任意骨架映射至标准化骨架，提取身份无关的运动令牌，通过分组注意力绑定至各角色 | 运动-身份纠缠与多人信号混淆 |
| **超场景集成器 (HSI)** | 在共享4D空间中通过深度感知注意力和动态C-RoPE融合运动表征与视频潜变量 | 遮挡解析与时空定位缺失 |
| **分层4D监督 (H4S)** | 高噪声步施加遮挡损失，低噪声步施加运动级损失，自适应注入4D先验 | 运动-外观耦合与泛化不足 |

### 主要结果

在专门构造的 **DualDynamics** 基准（涵盖多样类人形态与复杂交互）上，MotionWeaver 在所有指标上均显著超越现有方法：

- **FVD** 达到 145.7（次优 RealisDance-DiT 为 164.6），视频质量优势约 11.5%
- **CLIP** 达到 0.9041（次优为 0.8813），身份保持能力明显提升
- 定性结果（Figure 3）显示，MotionWeaver 是**唯一**能正确处理密集角色间交互与遮挡的方法
- 用户研究（Figure 13）中，在视觉质量、运动对齐、交互连贯性、遮挡处理、角色保持五个维度均获最高偏好票数，其中遮挡处理维度优势高达 **68%**

消融实验（Table 2）进一步验证了各组件的必要性：移除动态C-RoPE（DCR）使FVD从145.7急剧恶化至225.6，移除运动归一化管线（MNP）使CLIP从0.9041骤降至0.7801，证明显式时空编码和标准化运动表征是性能的核心支柱。

### 方法谱系与知识库定位

MotionWeaver 建立在预训练视频扩散模型 **Wan2.1-I2V-14B-480P** 之上，属于**基于扩散模型的图像动画**方法谱系。其与代表性基线的关系如下：

- 相对于 **MimicMotion**（Zhang et al., 2025）、**MusePose**（Tong et al., 2024）、**StableAnimator**（Tu et al., 2025a）、**Animate-X**（Tan et al., 2025）等单人/多人动画方法，MotionWeaver 的核心区分在于**身份无关的统一运动表征**和**显式4D时空建模**，使其首次具备跨类人形态泛化能力。
- 相对于 **UniAnimate-DiT**（Wang et al., 2025b）、**RealisDance-DiT**（Zhou et al., 2025）等基于DiT的统一动画框架，MotionWeaver 的**分层4D监督**策略提供了更精细的运动先验注入机制。
- 在知识库定位上，该方法开创性地将**4D空间锚定**引入多角色动画，为后续研究提供了运动-外观解耦和时空融合的新范式。

### 局限与开放问题

尽管性能显著领先，MotionWeaver 仍存在若干局限：在真实人类场景中手部生成模糊（因基础模型手部生成能力弱且有意避免以人为中心的偏见）；计算开销大，推理延迟较高；当前仅支持49帧固定长度输入。开放问题包括：如何在不牺牲泛化性的前提下增强手部细节？能否通过蒸馏实现实时推理？框架对三人及以上场景的鲁棒性如何？这些方向有待后续工作探索。



### 问题背景

图像动画任务旨在将参考图像中的角色按照目标运动序列驱动为连贯视频，在虚拟主播、游戏制作、影视特效等领域具有广泛应用。近年来，基于扩散模型的方法在这一任务上取得了显著进展，但其成功几乎完全局限于**单人场景**——即驱动单个真实人类角色执行简单动作。当场景扩展到多类人角色（如机器人、拟人动物、游戏化身、艺术风格角色）的密集交互与遮挡时，现有方法暴露出根本性缺陷。

这一局限性的根源可从三个层面理解：

**运动表征与形态纠缠。** 现有方法普遍采用骨架图或SMPL渲染图作为运动控制信号，这些表征天然携带身体比例、肢体长度等形态学信息，与角色外观深度耦合。当场景中存在多个形态各异的类人角色时，运动信号相互混叠，模型难以将正确的运动指令绑定到目标角色，导致身份漂移和运动错配。

**缺乏显式4D时空建模。** 多角色交互场景的核心挑战在于遮挡推理——当两个角色肢体交叉时，模型必须理解深度顺序才能正确渲染可见部分。现有方法的运动-视频融合仅依赖朴素的交叉注意力（cross-attention），缺乏对时间、空间和深度维度的显式位置编码，无法有效利用深度线索解析遮挡关系与尺寸错觉。

**训练策略的耦合缺陷。** 主流方法仅使用单一的2D像素MSE损失进行端到端训练，运动控制信号与外观重建目标完全耦合。这种训练范式使模型倾向于对人类外观过拟合，牺牲了对非标准类人形态的泛化能力。

### 现有方法缺口

为量化现有方法的局限性，论文在专门构造的**DualDynamics基准**上对7种代表性方法进行了系统评估。该基准包含多样的类人形态（真实人类、机器人、拟人动物、游戏角色）和丰富的交互场景（握手、拥抱、舞蹈、打斗）。

从定量结果（Table 1）来看，次优方法**RealisDance-DiT**（Zhou et al., 2025）的FVD为164.6，而本文方法达到145.7，差距显著。更关键的是定性表现（Figure 3）：**MimicMotion**（Zhang et al., 2025）、**MusePose**（Tong et al., 2024）、**StableAnimator**（Tu et al., 2025a）等方法在单人场景下表现尚可，但面对双角色遮挡交互时，普遍出现身份混淆（角色A的外观被错误赋予角色B的运动）、肢体融合（遮挡区域产生模糊伪影）和运动失真（目标姿势未正确执行）等问题。**Animate-X**（Tan et al., 2025）和**HumanVid**（Wang et al., 2024b）设计上仅支持单人，在多人场景下性能天然受限。**UniAnimate-DiT**（Wang et al., 2025b）虽为统一框架，但在多类人形态泛化方面同样表现不佳。

值得注意的是，即使将部分基线方法在专门的多人类数据集上进行微调，它们仍无法稳健处理多类人动画的核心挑战（Figure 6），这表明问题根源在于架构设计而非数据覆盖。

### 本文动机

上述分析揭示了一个深层瓶颈：现有方法将运动视为需要渲染到角色上的“控制信号”，而非需要理解的“动态过程”。当角色形态、交互模式和遮挡关系发生显著变化时，这种信号渲染范式必然失效。

本文的核心动机在于提出一种**运动-外观解耦**的范式转变：将运动表征从角色形态中彻底剥离，嵌入共享的4D时空坐标系，使模型能够真正理解运动动态而非简单渲染控制信号。具体而言，论文提出**MotionWeaver**框架，通过三个相互协同的设计实现这一目标：

- **统一编舞核心（Unified-Choreography Core, UCC）**：提取身份无关的运动令牌，通过分组注意力机制将运动信号绑定至对应角色，形成可泛化的统一运动表征。
- **超场景集成器（Hyper-Scene Integrator, HSI）**：在共享4D空间中通过深度感知注意力与动态C-RoPE融合运动表征与视频潜变量，显式建模遮挡关系。
- **分层4D监督（Hierarchical-4D Supervision, H4S）**：在高噪声扩散步施加遮挡损失，在低噪声步施加运动级损失，将4D运动先验注入训练过程。

这一设计使MotionWeaver成为首个能够在多样类人形态和密集交互遮挡下实现稳健动画生成的框架，其有效性通过定量指标、定性可视化和用户研究得到了系统验证。



## 核心方法与创新机理

MotionWeaver的核心创新在于构建了一个**整体4D锚定范式**，通过三个因果杠杆模块系统性地解决了多类人角色动画中长期存在的运动-外观耦合、多人信号混淆和遮挡处理难题。

### 1. 身份无关的统一运动表征（Unified-Choreography Core, UCC）

现有方法（如MimicMotion、MusePose等）直接使用骨架图或SMPL渲染图作为运动信号，这些表征天然携带身体比例、形状等身份信息。当场景中存在多个类人角色时，不同形态的运动信号在特征空间中相互混叠，导致模型难以区分“谁在执行哪个动作”。

UCC通过两步解耦实现身份无关的运动表征：

- **运动归一化管线（Motion Normalization Pipeline, MNP）**：将任意类人形态的关节坐标映射到标准化骨架ρ上，强制相邻关节间的欧氏距离固定，消除形态差异带来的信号偏差。
- **分组注意力绑定（Group Attention Module, GAM）**：以标准化后的运动令牌 $z_{mo}$ 为查询（Query），以角色身份令牌 $z_{id}$ 为键/值（Key/Value），通过分组注意力将运动信号绑定到对应角色，输出统一运动表征 $z_{uni}$。

这一设计的本质是将“谁在动”与“怎么动”在特征空间中显式分离，使运动表征成为可跨形态泛化的通用信号。消融实验表明，移除MNP导致CLIP从0.9041骤降至0.7801（Table 2），证明标准化骨架对泛化能力至关重要。

### 2. 共享4D空间中的深度融合（Hyper-Scene Integrator, HSI）

现有方法通常采用朴素的交叉注意力将运动信号注入视频生成过程，缺乏显式的时空位置建模和深度感知能力。这使得模型无法有效利用深度线索解析遮挡关系，也难以处理因距离产生的尺寸错觉。

HSI在共享4D空间（时间t + 空间x, y, z）中实现运动表征与视频潜变量的深度融合，包含两个关键设计：

- **深度感知注意力（Depth-Aware Attention, DAA）**：在生成注意力键（Key）时，将运动单元令牌与其深度令牌拼接后通过MLP处理，显式编码z轴信息。同时通过遮挡损失 $\mathcal{L}_{occ}$ 监督角色注意力图与真值遮挡掩码的对齐，强制模型学习正确的深度顺序。
- **动态C-RoPE（Dynamic C-RoPE）**：将传统RoPE扩展为分块对角旋转矩阵，分别对时间轴、水平轴、垂直轴进行独立的旋转位置编码。运动单元的旋转矩阵根据其全局位置动态选择，视频潜变量的旋转矩阵由其时空坐标决定。

这两个设计协同工作：DAA提供深度维度的语义感知，动态C-RoPE提供显式的时空坐标锚定。消融实验显示，移除DCR使FVD从145.7恶化至225.6（Table 2），是所有组件中对视频质量贡献最大的单一设计。

### 3. 分层4D监督策略（Hierarchical-4D Supervision, H4S）

现有方法普遍采用单一的2D像素MSE损失进行训练，运动信号仅作为条件输入而非显式监督目标，导致运动与外观在优化过程中耦合，模型倾向于过拟合人类外观而非真正理解运动动态。

H4S根据扩散时间步自适应地组合辅助损失：

$$
\mathcal{L}_{H4S} = \begin{cases} \mathcal{L}_{MSE} + \lambda_1 \mathcal{L}_{OCC}, & t \ge \alpha T \\ \mathcal{L}_{MSE} + \lambda_2 \mathcal{L}_{MO}, & t < \alpha T \end{cases}
$$

- **高噪声步（$t \ge \alpha T$）**：此时模型主要构建全局布局，施加遮挡损失 $\mathcal{L}_{OCC}$ 引导正确的深度排序和角色可见性。
- **低噪声步（$t < \alpha T$）**：此时模型细化细节，施加运动级损失 $\mathcal{L}_{MO}$ 注入4D运动先验，确保生成结果与目标运动精确对齐。

这一策略的巧妙之处在于利用了扩散模型不同去噪阶段的功能分工：早期关注全局结构（遮挡关系是结构性问题），后期关注局部精度（运动对齐是细节性问题）。移除H4S后FID从19.41升至21.46、CLIP从0.9041降至0.8714（Table 2），验证了分层监督的有效性。

### 创新总结

三个模块构成因果闭环：UCC提供可泛化的运动表征，HSI在4D空间中实现表征与视觉生成的精确对齐，H4S通过分阶段监督将4D运动先验注入模型训练。这一组合使MotionWeaver成为首个在多样类人形态和密集交互遮挡下实现稳健动画生成的框架——定性结果（Figure 3）显示其为唯一能正确处理角色间密集交互与遮挡的方法，用户研究中遮挡处理维度优势高达68%（Figure 13）。



![[assets/figures/papers/paper_list_l31_https_openreview_net_forum_id_KjlLwRsiUE/figures/002_Figure_2.jpg]]
*Figure 2: The overview of our MotionWeaver. (a) Unified-Choreography Core extracts unified motion representations $\left( z _ { u n i } \right$) . (b) Hyper-Scene Integrator integrates the motion representations with video latents within a shared 4D space. (c) Hierarchical-4D Supervision utilizes timestep-specific 4D supervision to help the model effectively learn motion representations

MotionWeaver 提出了一个面向多类人角色图像动画的整体4D锚定框架，其核心设计目标是在不依赖角色特定外观先验的前提下，实现多样类人形态（人类、机器人、拟人动物、游戏化身等）在多角色密集交互与遮挡场景下的稳健动画生成。框架由三个关键模块构成：**统一编舞核心 (Unified-Choreography Core, UCC)**、**超场景集成器 (Hyper-Scene Integrator, HSI)** 和**分层4D监督 (Hierarchical-4D Supervision, H4S)**，三者协同工作于一个预训练视频扩散模型主干之上（Wan2.1-I2V-14B-480P）。

### 输入与输出流

框架的输入包括：(1) 一张包含多个类人角色的参考图像；(2) 各角色的目标运动序列，以3D关节坐标 $\chi$ 的形式给出。输出为一段保持参考图像中角色身份和外观、同时精确执行目标运动的连续视频。

### 模块关系与数据流

**UCC → 统一运动表征提取。** 输入的运动序列首先进入 UCC，其核心操作分为两步：运动归一化管线 (Motion Normalization Pipeline, MNP) 将任意骨架的关节坐标映射到标准化骨架 $\rho$ 上，消除身体比例与形态差异；随后通过任务专用分词器 $\Phi_{tok}$ 沿时间轴下采样，生成身份无关的运动令牌 $z_{mo} \in \mathbb{R}^{P \times (T \times J) \times D}$（$P$ 为角色数，$T$ 为时间帧数，$J$ 为关节数，$D$ 为特征维度）。接着，分组注意力模块 (Group Attention Module, GAM) 以运动令牌为查询、对应角色的身份令牌 $z_{id}$ 为键/值进行交叉注意力，将运动信号绑定到具体角色，输出统一运动表征 $z_{uni}$。这一设计使运动表征与角色形态彻底解耦，从根本上解决了多人物信号混淆问题。

**HSI → 共享4D空间融合。** $z_{uni}$ 随后进入 HSI，与视频扩散模型中的视频潜变量 $z_v$ 在共享4D时空坐标系中深度融合。HSI 包含两个互补机制：(1) **深度感知注意力 (Depth-Aware Attention, DAA)**：通过将运动单元令牌与深度令牌拼接后经 MLP 生成 z 轴感知的键 $\bar{k}$，同时将视频潜变量经 MLP 生成 z 轴感知的查询 $\bar{q}$，使注意力计算隐式编码深度顺序；(2) **动态 C-RoPE (Dynamic C-RoPE, DCR)**：为键和查询分别施加分块对角旋转矩阵，显式编码时间轴 ($t$)、水平轴 ($x$) 和垂直轴 ($y$) 的位置信息，旋转矩阵根据运动单元的全局时空位置动态选取。HSI 模块以每四个基础模型块的固定间隔插入 Wan2.1 主干中，实现运动信号对生成过程的逐步引导。

**H4S → 分层训练监督。** 训练阶段，H4S 根据扩散时间步自适应组合损失函数：在高噪声步 ($t \ge \alpha T$)，损失为 $\mathcal{L}_{MSE} + \lambda_1 \mathcal{L}_{OCC}$，其中 $\mathcal{L}_{OCC}$ 最小化角色注意力图与真值遮挡掩码间的 MSE，强制模型学习正确的深度排序；在低噪声步 ($t < \alpha T$)，损失切换为 $\mathcal{L}_{MSE} + \lambda_2 \mathcal{L}_{MO}$，其中 $\mathcal{L}_{MO}$ 注入运动级先验。这种分层策略将4D运动理解注入生成过程，而非简单地将运动作为外观渲染的附加条件。

### 设计动机与因果逻辑

现有方法（如 **MimicMotion** (Zhang et al., 2025)、**UniAnimate-DiT** (Wang et al., 2025b) 等）的根本瓶颈在于运动表征与角色形态纠缠，且缺乏显式4D时空建模能力，导致多角色场景下信号混叠、遮挡处理失败。MotionWeaver 通过三个因果杠杆破解这一困境：UCC 实现运动-身份解耦，HSI 提供深度感知的时空融合，H4S 将4D运动先验注入生成过程。消融实验 (Table 2) 证实，移除任一组件均导致性能显著下降——移除 DCR 使 FVD 从 145.7 恶化至 225.6，移除 MNP 使 CLIP 从 0.9041 骤降至 0.7801，验证了各模块的因果贡献。



### 3.1 统一编舞核心 (Unified-Choreography Core, UCC)

UCC 旨在从任意类人形态的骨架序列中提取**身份无关**的运动表征，并将其与对应角色绑定，形成可泛化的统一运动信号。该模块包含两个关键子步骤。

**运动归一化管线 (Motion Normalization Pipeline, MNP)。** 给定第 $p$ 个角色的原始关节坐标序列 $\chi$，首先将其映射到预定义的标准化骨架 $\rho$ 上——该骨架强制相邻关节间保持固定的欧氏距离，从而消除不同角色间肢体比例和形状的差异，得到标准化表征 $\bar{\chi}$。随后，一个任务特定的运动令牌化器 $\Phi_{tok}$ 沿时间轴对 $\bar{\chi}$ 进行下采样，生成身份无关的运动令牌：

$$z_{mo} = \Phi_{tok}(\mathrm{Map}(\chi, \rho)) \in \mathbb{R}^{P \times (T \times J) \times D} \quad \text{(Eq. 2)}$$

其中 $P$ 为角色数，$T$ 为下采样后的时间长度，$J$ 为标准化骨架的关节数，$D$ 为特征维度。

**分组注意力模块 (Group Attention Module, GAM)。** 为将运动令牌与特定角色身份关联，GAM 以运动令牌 $z_{mo[p]}$ 作为查询（Query），以对应角色的身份令牌 $z_{id[p]}$ 作为键（Key）和值（Value），通过分组交叉注意力产生第 $p$ 个角色的统一运动表征：

$$z_{uni[p]} = \mathrm{GroupAttn}(\mathrm{Q}(z_{mo[p]}), \mathrm{K}(z_{id[p]}), \mathrm{V}(z_{id[p]})) \in \mathbb{R}^{(T \times J) \times D} \quad \text{(Eq. 3)}$$

该操作确保每个角色的运动表征仅与其自身的身份信息绑定，避免多角色场景下的信号混淆。

### 3.2 超场景集成器 (Hyper-Scene Integrator, HSI)

HSI 在共享 4D 时空坐标系中深度融合统一运动表征 $z_{uni}$ 与视频潜变量 $z_v$，使扩散模型能够感知深度顺序与时空位置，从而有效解析遮挡和密集交互。HSI 包含两个核心机制。

**深度感知注意力 (Depth-Aware Attention, DAA)。** DAA 显式建模 z 轴（深度轴），使模型学习正确的深度排序。对于运动单元的键，将其与对应时间步的深度令牌 $z_{depth[p,t]}$ 拼接后经 MLP 投影，生成深度感知键：

$$\bar{\boldsymbol{k}}_{p,t,j} = \mathrm{MLP}_{\mathrm{K}}([\boldsymbol{z}_{uni[p,t,j]} \parallel \boldsymbol{z}_{depth[p,t]}]) \in \mathbb{R}^{D} \quad \text{(Eq. 4)}$$

对于视频潜变量的查询，同样经 MLP 投影生成深度感知查询：

$$\bar{\boldsymbol{q}}_{t,x,y} = \mathrm{MLP}_{\mathbf{Q}}(z_{v[t,x,y]}) \in \mathbb{R}^{D} \quad \text{(Eq. 5)}$$

为强制深度感知注意力的学习，引入遮挡损失 $\mathcal{L}_{occ}$，最小化各角色注意力图 $\mathbf{h}_i$ 与真值遮挡掩码 $\mathbf{m}_i$ 间的 MSE：

$$\mathcal{L}_{\mathrm{occ}} = \frac{1}{TP} \sum_{i=1}^{P} \mathrm{MSE}(\mathbf{h}_i, \mathbf{m}_i) \quad \text{(Eq. 6)}$$

**动态 C-RoPE (Dynamic C-RoPE)。** 在 DAA 基础上，动态 C-RoPE 对时间轴 $t$、水平轴 $x$、垂直轴 $y$ 分别施加旋转位置编码，使模型显式感知运动单元在 4D 空间中的全局位置。其分块对角旋转矩阵为：

$$\tilde{R}_{\Theta, t, x, y}^d = \begin{pmatrix} R_{\Theta, t}^{d/3} & \mathbf{0} & \mathbf{0} \\ \mathbf{0} & R_{\Theta, x}^{d/3} & \mathbf{0} \\ \mathbf{0} & \mathbf{0} & R_{\Theta, y}^{d/3} \end{pmatrix} \quad \text{(Eq. 7)}$$

该旋转矩阵分别作用于深度感知键 $\bar{\boldsymbol{k}}$ 和深度感知查询 $\bar{\boldsymbol{q}}$，得到旋转后的键 $\tilde{\boldsymbol{k}}$ 和查询 $\tilde{\boldsymbol{q}}$，随后在共享 4D 空间中执行交叉注意力，完成运动表征与视频潜变量的融合。

### 3.3 分层 4D 监督 (Hierarchical-4D Supervision, H4S)

H4S 根据扩散时间步 $t$ 自适应地组合不同的辅助损失，将 4D 运动先验分阶段注入模型。其核心思想是：在高噪声步（$t \ge \alpha T$），模型主要构建全局布局和深度顺序，此时施加遮挡损失 $\mathcal{L}_{OCC}$；在低噪声步（$t < \alpha T$），模型细化运动细节，此时施加运动级损失 $\mathcal{L}_{MO}$（由光流等运动先验导出）。H4S 的总体损失函数为：

$$\mathcal{L}_{H4S} = \begin{cases} \mathcal{L}_{MSE} + \lambda_1 \mathcal{L}_{OCC}, & t \ge \alpha T \\ \mathcal{L}_{MSE} + \lambda_2 \mathcal{L}_{MO}, & t < \alpha T \end{cases} \quad \text{(Eq. 10)}$$

其中 $\alpha$ 为时间步阈值，$\lambda_1$、$\lambda_2$ 为各辅助损失的权重系数。$\mathcal{L}_{MSE}$ 为标准的像素级重建损失。这种分层设计使得运动与外观的学习解耦：高噪声步专注于空间结构和遮挡关系，低噪声步专注于运动精度，从而避免单一 2D MSE 损失导致的运动-外观耦合问题。

### 3.4 模块间因果链路

上述三个模块形成清晰的因果链条：**UCC** 将形态各异的类人骨架统一为身份无关的运动令牌，解决了运动表征与形态纠缠的瓶颈；**HSI** 在共享 4D 空间中通过深度感知注意力和动态 C-RoPE 融合运动与视频信号，赋予模型理解深度顺序和时空位置的能力；**H4S** 通过分阶段监督将 4D 运动先验注入扩散过程，使运动学习与外观生成解耦。消融实验（Table 2）证实了这一因果链路：移除 MNP 导致泛化能力骤降（CLIP 从 0.9041 降至 0.7801），移除 DCR 使视频质量严重恶化（FVD 从 145.7 升至 225.6），移除 H4S 则同时损害图像质量和运动对齐（FID 从 19.41 升至 21.46，CLIP 降至 0.8714）。



## 实验与关键发现

### 主实验结果

MotionWeaver在专门构造的**DualDynamics基准**上与7个现有方法进行了全面对比。该基准包含多样化的类人形态（真实人类、机器人、拟人动物、游戏化身）和密集交互场景，旨在评估模型在分布外形态和复杂遮挡下的泛化能力。所有对比方法均使用公开可用的官方实现或模型权重，未在MultiHuman46上进行额外微调，以保证公平性。

**Table 1**总结了量化对比结果。MotionWeaver在所有8项指标上均取得最优：

![[assets/figures/papers/paper_list_l31_https_openreview_net_forum_id_KjlLwRsiUE/figures/004_Table_1.jpg]]
*Table 1: Quantitative results on the DualDynamics benchmark. Our method consistently outperforms all baselines across all metrics, demonstrating significant advantages in multi-humanoid scenarios involving diverse humanoid forms and rich interactions*

- **视频质量**：FVD达到**145.7**，相比次优方法RealisDance-DiT（164.6）降低18.9，降幅达11.5%；FID-VID为20.34，显著优于其他方法。
- **图像质量**：FID为19.41，CLIP分数达**0.9041**（次优0.8813），表明生成结果与参考图像的身份一致性最高。
- **运动精度**：L1、PSNR、SSIM等像素级指标同样领先，说明运动对齐更为精准。

值得注意的是，部分对比方法（如Animate-X、MusePose）设计上仅支持单人场景，在多人场景下性能天然受限。而MotionWeaver是唯一在密集角色间交互与遮挡场景下保持稳定输出的方法——**Figure 3**的定性对比清晰展示了这一点：当两个角色发生肢体交叉或前后遮挡时，基线方法普遍出现身份混淆、肢体错位或遮挡穿透，而MotionWeaver能正确解析深度顺序并保持各自身份完整。

![[assets/figures/papers/paper_list_l31_https_openreview_net_forum_id_KjlLwRsiUE/figures/003_Figure_3.jpg]]
*Figure 3: Qualitative Comparison with Existing Methods. The yellow and red meshes indicate the target motions of the l e f t and right characters from the reference image, respectively. Our MotionWeaver method achieves superior identity preservation and motion accuracy for multiple humanoid characters. Notably, it is the only approach that correctly handles dense inter-character interactions and occlusions*

用户偏好调查（**Figure 13**）进一步验证了上述结论：在视觉质量、运动对齐、交互连贯性、遮挡处理、角色保持五个维度，MotionWeaver均获得最高偏好票数，其中遮挡处理维度的优势高达**68%**。

### 消融实验

为验证各核心组件的贡献，论文对**统一编舞核心（UCC）**、**超场景集成器（HSI）**和**分层4D监督（H4S）**进行了系统消融，结果见**Table 2**。

![[assets/figures/papers/paper_list_l31_https_openreview_net_forum_id_KjlLwRsiUE/figures/005_Table_2.jpg]]
*Table 2: Ablation study of the core components on the DualDynamics benchmark. The complete design achieves the best overall performance*

**UCC消融**包含两个子组件：
- **移除运动归一化管线（MNP）**：直接用原始骨架坐标替代标准化骨架映射。CLIP从0.9041骤降至**0.7801**，表明身份无关的标准化骨架对跨形态泛化至关重要——模型在缺乏归一化时会过拟合到训练中的人类身体比例。
- **移除分组注意力模块（GAM）**：将分组注意力替换为朴素的拼接融合。FVD从145.7升至**197.2**，说明分组注意力有效避免了多人物运动信号的混淆。

**HSI消融**包含两个子组件：
- **移除深度感知注意力（DAA）**：去掉z轴编码和遮挡损失监督，仅保留4D RoPE。FVD升至**189.4**，CLIP降至0.8786。这表明深度线索对于解析遮挡关系不可或缺。
- **移除动态C-RoPE（DCR）**：移除显式的时空位置编码。这是**性能恶化最严重的消融**——FVD从145.7飙升至**225.6**，FID从19.41升至26.52。这说明显式4D位置编码是模型理解运动时空动态的核心机制，其缺失会导致严重的时空错位。

**H4S消融**：将分层监督替换为固定的MSE+遮挡损失组合。FID从19.41升至**21.46**，CLIP从0.9041降至**0.8714**。分层策略的关键在于：高噪声步的遮挡监督帮助模型建立正确的深度顺序，低噪声步的运动级监督则将4D运动先验注入生成过程——两者在不同扩散阶段发挥互补作用。

**Figure 4**提供了消融的可视化对比及注意力图。完整模型的注意力图显示，视频潜变量能准确聚焦到对应角色的运动表征区域；而移除DCR后，注意力分布明显发散，无法形成有效的时空对应。

![[assets/figures/papers/paper_list_l31_https_openreview_net_forum_id_KjlLwRsiUE/figures/007_Figure_4.jpg]]
*Figure 4: Visual Comparison of Ablation Results. (a) The yellow and red meshes represent the target motions of the red and blue characters, respectively. The original design achieves the best visual performance among all variants. (b) Visualization of attention maps between frame latents and per-character unified motion representations*

### 泛化性与扩展性

**Figure 5**展示了MotionWeaver在三人及以上场景的生成结果，证明框架的编舞核心和4D注意力机制可以自然扩展到更多角色，无需架构修改。但论文未提供三人以上场景的系统量化评估，该方向的鲁棒性仍需进一步验证。

### 失败模式与局限

论文坦诚分析了以下局限：

1. **真实人类手部模糊**（**Figure 12**）：在真实人类场景中，生成的手部区域常出现模糊或形变。根本原因在于：基础模型Wan2.1-I2V-14B-480P本身的手部生成能力较弱，且论文有意避免引入显式手部控制信号，以防止对人类外观的过拟合、保持跨类人形态的泛化性。这是一个刻意的设计取舍，而非简单的模型缺陷。

2. **计算开销**：基于14B参数的视频扩散主干，加上多角色4D注意力计算，推理延迟较高，难以用于实时或交互式应用。

3. **序列长度限制**：当前仅支持49帧连续视频输入（固定潜在时间长度），扩展到更长序列需要额外的时序建模设计。

4. **上游依赖**：训练依赖于专业多人姿势检测器CoMotion提取运动序列，其检测精度直接影响上层动画质量。

### 补充图表

![[assets/figures/papers/paper_list_l31_https_openreview_net_forum_id_KjlLwRsiUE/figures/001_Figure_1.jpg]]
*Figure 1: We propose MotionWeaver, a novel framework for multi-humanoid image animation, which effectively handles occlusions and complex interactions in multi-character scenarios, while showing strong generalization across diverse humanoid characters and artistic styles*



## 定位与知识库关联

### 1. 与现有工作的关系

MotionWeaver处于基于扩散模型的角色动画与视频生成两条技术路线的交汇点。现有方法可以按两个维度进行定位：**驱动信号类型**和**场景复杂度**。

**姿势驱动动画方法**构成了最直接的基线类别。**MimicMotion**（Zhang et al., 2025）和**MusePose**（Tong et al., 2024）均采用扩散架构，但前者依赖骨架图、后者依赖SMPL渲染图作为运动表征。这些表征天然耦合了角色的身体比例与形状信息，在多人物场景中信号混叠严重，导致身份漂移和运动错位。**StableAnimator**（Tu et al., 2025a）和**Animate-X**（Tan et al., 2025）在设计上仅面向单人场景，缺乏多角色解耦机制。**UniAnimate-DiT**（Wang et al., 2025b）和**RealisDance-DiT**（Zhou et al., 2025）虽然采用了更现代的DiT骨干，但其运动-视频融合仍依赖朴素的交叉注意力，没有显式的位置编码或深度建模。

MotionWeaver相对于上述方法的根本差异在于**运动表征的去身份化**和**融合机制的4D时空化**。统一编舞核心（UCC）通过标准化骨架映射和运动令牌化，将任意类人形态的关节坐标投影到统一的运动空间，再通过分组注意力与角色身份令牌绑定，实现了运动与外观的彻底解耦。超场景集成器（HSI）则引入了两个关键机制：深度感知注意力在z轴上建模遮挡关系，动态C-RoPE在t/x/y轴上提供显式的位置编码。这与基线方法中"将运动信号简单注入扩散模型"的做法有本质区别。

**人类视频生成方法**如**HumanVid**（Wang et al., 2024b）虽然也处理多人物场景，但其目标是生成而非动画，缺乏对驱动信号的精确控制。

### 2. 适用边界

MotionWeaver的核心假设和适用边界可从数据、形态、计算三个维度界定：

**数据依赖**。框架的训练和推理依赖专业的多人姿势检测器（CoMotion），其精度直接影响上层运动表征的质量。在姿势检测失败的极端遮挡或罕见姿态下，整个管线可能退化。此外，训练仅使用人类视频数据，其对非人类形态（机器人、拟人动物）的泛化依赖于标准化骨架映射的抽象能力，而非显式的域适应。

**形态覆盖**。标准化骨架ρ的设计隐含了对类人形态的拓扑假设——即存在可映射到固定关节集合的肢体结构。对于高度非人形的角色（如蛇形、多足生物），该映射可能不成立或信息损失严重。论文在Figure 1中展示了机器人、游戏化身、拟人动物等多种形态，但未系统评估形态多样性的上限。

**场景复杂度**。当前设计支持固定49帧的视频长度（Wan2.1-I2V-14B-480P的潜在时间维度），扩展到更长序列需要额外的时间维度设计。Figure 5展示了三人场景的初步结果，但注意力分布随角色数增加的稀释效应尚未量化分析。

**计算开销**。基于14B参数的Wan2.1主干网络，在8张H100 GPU上训练，推理延迟较高，不适合实时或交互式应用场景。

### 3. 局限与开放问题

论文明确承认的局限包括：

- **手部生成模糊**（Figure 12）：在真实人类场景中，基础模型Wan2.1-I2V-14B-480P的手部生成能力较弱，且MotionWeaver有意避免引入显式手部控制信号，以保持对多样类人形态的泛化性。这是一个有意的设计权衡，而非技术缺陷。
- **固定帧长**：当前仅支持49帧连续视频输入，超长序列需要额外的时序扩展策略。
- **姿势检测器依赖**：CoMotion的精度瓶颈会向上传播。

从方法谱系的角度，以下几个开放问题值得关注：

1. **手部细节与泛化性的平衡**：能否引入手部级运动令牌，在不耦合身份信息的前提下增强手部生成？这需要在标准化骨架中增加手部关节密度，同时保持与身份令牌的解耦绑定。

2. **实时推理路径**：14B基座模型的推理成本限制了实际部署。可能的路径包括蒸馏到更小的DiT骨干、设计高效的稀疏注意力机制（利用C-RoPE的显式位置信息进行选择性注意力），或采用一致性模型缩短采样步数。

3. **多人扩展的鲁棒性**：分组注意力机制在P>3时是否会因注意力分布稀释而退化？是否需要引入层次化的角色分组策略或稀疏注意力掩码？

4. **4D建模的深化**：当前4D空间建模聚焦于z轴遮挡和t/x/y轴位置编码。能否进一步联合估计光流和深度图，以支持更自由的相机运动（如视角旋转、缩放）？

5. **域适应策略**：仅使用人类视频训练却能泛化到非人类形态的原理，本质上是标准化骨架映射的抽象能力。但该泛化的上限在哪里？是否需要合成数据（如Blender渲染的机器人/动物动画）进行显式的域适应？消融实验（Table 2）中移除MNP导致CLIP从0.9041骤降至0.7801，表明标准化骨架对泛化至关重要，但其对极端非人形形态的鲁棒性仍需系统评估。



## 原文 PDF

![[paperPDFs/ICLR_2026/MotionWeaver_Holistic_4D_Anchored_Framework_for_Multi_Humanoid_Image_Animation.pdf]]
