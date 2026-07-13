---
title: "MoVie: Broaden Your Views with Human Motion for Action Detection"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/MoVie_Broaden_Your_Views_with_Human_Motion_for_Action_Detection.pdf
project_link: null
code_link: null
aliases:
- MoVie
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
core_operator: 通过可学习运动字典将骨架运动分解为物理基元，并借助正交投影将基元信息作为正则化器注入视觉特征空间，是实现运动-视觉结构化融合并显著提升动作检测的关键。
primary_logic: 将骨架运动视作结构化的物理先验而非辅助模态，利用运动基元分解和正交变换桥接异构特征，使视觉表示在保持语义的同时获得几何与运动一致性，从而系统性增强动作理解。
claims:
- 在TSU-CS数据集上，MoVie以I3D特征超越先前最优视觉方法15.9% mAP，直接验证了引入结构化运动信号的决定性作用。
- 移除MGFR中的正交性约束导致TSU-CS性能下降2.8%，证明正交投影对齐是实现有效正则化的必要条件。
- 运动密集型活动（如起身+46.9%、搅拌+32.8%）获得巨大增益，而缺乏运动的动作提升微小，表明框架精准捕获了动作的运动本质。
- TSU-CS 上 frame-level mAP (%) = 50.1 (ViCLIP) / 49.6 (I3D)
---

# MoVie: Broaden Your Views with Human Motion for Action Detection

> [!tip] 核心洞察
> 将骨架运动视作结构化的物理先验而非辅助模态，利用运动基元分解和正交变换桥接异构特征，使视觉表示在保持语义的同时获得几何与运动一致性，从而系统性增强动作理解。

| 字段 | 内容 |
|------|------|
| 中文题名 | MoVie：以结构化人体运动拓宽视角的动作检测框架 |
| 英文题名 | MoVie: Broaden Your Views with Human Motion for Action Detection |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://openaccess.thecvf.com/content/CVPR2026/html/Yang_MoVie_Broaden_Your_Views_with_Human_Motion_for_Action_Detection_CVPR_2026_paper.html) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction |
| Method | MoVie |
| Dataset | TSU-CS, Multi-THUMOS, Charades |

> [!tip] 效果简介
> - TSU-CS 上，frame-level mAP (%) 50.1 (ViCLIP) / 49.6 (I3D) vs 先前最优视觉方法 (+15.9% (I3D over SoTA))。
> - Multi-THUMOS 上，frame-level mAP (%) 48.3 (ViCLIP) vs 先前最优视觉方法 (+3.7%)。
> - Charades 上，frame-level mAP (%) 33.5 (ViCLIP) vs 先前最优视觉方法 (N/A)。

## 概要

现有基于RGB的动作检测方法在处理复杂、组合性动作时面临根本瓶颈：视觉模型天然缺乏对物理运动动力学的理解，难以捕捉精细的时序动态。直接引入骨架模态的朴素方案——使用全局动作标签训练粗粒度特征（如AGCN）并与视觉特征简单拼接——不仅未能解决这一问题，反而因异构特征空间的相互干扰而引入噪声。MoVie的核心洞察在于：**骨架运动应被视为结构化的物理先验，而非简单的辅助模态**。通过将运动分解为可学习的物理基元，并以正交投影的方式将这些基元作为正则化器注入视觉特征空间，MoVie实现了运动与视觉的结构化融合，使视觉表示在保持语义丰富性的同时获得几何与运动一致性。

框架的关键创新体现在三个层面：（1）**结构化运动投影（SMP）** 将骨架特征投影到可学习运动字典上，将粗糙的标签驱动特征转化为细粒度的基元激活强度，从而显式建模运动的物理组成；（2）**运动引导特征正则化（MGFR）** 通过正交投影矩阵将运动基元方向映射到视觉通道，以正则化而非直接拼接的方式调制视觉特征，并辅以时序一致性损失对齐运动变化与视觉演化；（3）引入**历史记忆库**存储长期视觉上下文，与当前运动-视觉特征拼接后送入时序编码器，弥补了单帧正则化在长程时序建模上的不足。

实验证据直接验证了方法的核心主张。在TSU-CS数据集上，MoVie以I3D视觉特征超越先前最优纯视觉方法**+15.9% mAP**，这一决定性提升表明结构化运动信号的引入是性能飞跃的根本原因。消融实验中，移除MGFR的正交性约束导致性能下降**2.8%**，证明正交投影对齐是实现有效正则化的必要条件。逐类分析进一步揭示，运动密集型活动（如起身+46.9%、搅拌+32.8%）获得巨大增益，而缺乏显著运动的动作提升微小，表明框架精准捕获了动作的运动本质。然而，框架对细粒度手物交互（如从瓶子喝水-4.1%）仍存在性能下降，揭示了当前方法在手部和物体显式建模方面的局限性。



### 动作检测的核心瓶颈：视觉模型缺乏物理运动理解

时序动作检测（Temporal Action Detection）旨在从视频中定位并识别多类动作的起止时间，是视频理解的核心任务之一。现有方法主要依赖纯视觉模态（RGB或光流），通过强大的视觉编码器（如I3D、ViCLIP）提取外观特征，再送入时序建模网络（如**MS-TCT**（Dai et al., CVPR 2022）、**PDAN**（Dai et al., WACV 2021）、**MLAD**（Tirupattur et al., CVPR 2021）等）进行帧级多标签分类。然而，这类纯视觉范式存在一个根本性缺陷：**视觉特征擅长捕捉场景和物体外观，却难以刻画动作背后的物理运动动力学**。

Figure 1(a) 直观地揭示了这一问题：当面对“起身”（get up）这类由躯干弯曲和腿部伸展构成的组合性动作时，纯RGB方法往往无法区分其精细的运动模式，容易与外观相似但运动本质不同的动作混淆。这种局限在复杂场景——如光照变化剧烈、背景杂乱或多人交互——下尤为突出，因为视觉特征容易受到外观噪声的干扰，而动作的本质恰恰在于“如何运动”而非“看起来像什么”。

### 现有跨模态方法的不足：粗糙融合与异构空间冲突

骨架（skeleton）模态天然地编码了人体关节的时空轨迹，是描述运动动力学的理想信号。因此，一个直观的思路是将骨架特征作为辅助模态引入动作检测框架。然而，现有跨模态方法面临两个关键挑战：

1. **标签驱动的骨架特征过于粗糙**：传统方法（如AGCN）使用全局动作类别标签训练骨架编码器，提取的特征是对整个动作的粗粒度概括，无法捕捉构成复杂动作的细粒度运动基元（如“起身”中的躯干弯曲与腿部伸展）。这种粗糙的运动表示在注入视觉模型时，难以提供有效的物理先验。

2. **异构空间直接融合导致信息干扰**：视觉特征和骨架特征源自完全不同的语义空间——前者编码外观和语义，后者编码几何和运动。直接拼接或晚期融合（late fusion）将两者强行混合，不仅无法实现互补，反而引入跨模态噪声，导致性能提升有限甚至下降。

### MoVie的核心动机：将运动作为结构化物理先验

MoVie的核心洞察在于：**骨架运动不应被视为辅助模态，而应被建模为结构化的物理先验，用于正则化和增强视觉表示**。这一视角转变带来了两个关键设计理念：

- **运动基元分解**：通过可学习的运动字典，将骨架运动分解为可解释的物理基元（如躯干弯曲、手臂旋转、腿部伸展），从而获得细粒度的、结构化的运动描述。这使模型能够精确地“理解”动作由哪些基本运动成分构成。

- **正交投影桥接异构空间**：不直接融合运动与视觉特征，而是将运动基元作为正则化器，通过正交投影注入视觉特征空间。正交性约束确保了每个运动基元方向在视觉通道中独立解耦，使视觉特征在保持语义的同时获得几何与运动一致性，从而系统性增强动作理解能力。

Figure 1(b)-(d) 展示了这一框架的整体逻辑：从骨架序列中学习结构化运动基元，通过运动引导特征正则化（MGFR）将其对齐并注入视觉空间，最终送入历史感知的跨模态时序编码器进行精确的动作检测。这一设计从根本上解决了“视觉模型忽视物理运动”的瓶颈，为动作检测提供了新的范式。



## 核心方法与创新机理

MoVie的核心突破在于**将骨架运动重新定义为结构化的物理先验，而非单纯的辅助模态**，并通过两个关键机制实现运动与视觉特征的深度融合：**结构化运动投影（SMP）** 和 **运动引导特征正则化（MGFR）**。这一设计从根本上改变了运动信号与视觉表征的交互方式，使模型能够捕捉复杂、组合性动作的精细动态。

### 从粗糙标签驱动到结构化运动基元

现有方法通常基于全局动作标签训练骨架特征提取器（如AGCN），得到的运动表征粗糙且与RGB特征空间异构，直接拼接或晚期融合容易引入干扰。MoVie通过**SMP模块**实现了运动表示的质变：

- **运动字典分解**：将骨架运动特征投影到可学习的运动字典 $\mathbf{D_m}$ 上，获得基元激活强度 $\pmb{\alpha} = \| \mathbf{D_m} \mathbf{F} \|_2$（Eq. 3），将连续动作分解为有限个物理基元的组合。
- **多人运动聚合**：通过MLP投影 $\sigma(\cdot)$ 稳定噪声后，使用交互池化算子 $\mathcal{G}_p$ 将多人基元融合为统一描述子 $\hat{\pmb{\alpha}} \in \mathbb{R}^{K \times T}$（Eq. 5），解决了多目标场景下的运动信息整合问题。

这一设计使得运动信号从“动作类别标签驱动的粗粒度特征”转变为“物理基元级别的细粒度结构化表示”，为后续的跨模态融合提供了可解释的运动语义基础。

### 正交投影驱动的结构化融合

传统方法将运动与视觉特征直接拼接，忽略了两个模态在特征空间中的异构性。MoVie的**MGFR模块**通过正交投影实现了运动对视觉特征的“正则化注入”：

$$\mathbf{F_{mv}} = \epsilon(\mathbf{F_v}) + \lambda (\mathbf{Q}^{\top} \hat{\alpha})$$

其中投影矩阵 $\mathbf{Q}$ 的列向量满足正交性约束 $\langle \mathbf{q}_i, \mathbf{q}_j \rangle = 0\ (i \neq j)$（Eq. 7）。这一约束确保每个运动基元方向独立地调制视觉通道，避免信号混叠。消融实验证实，移除正交性约束导致TSU-CS性能下降2.8%（Table 2），直接验证了正交对齐是实现有效正则化的必要条件。

此外，MGFR还引入时序一致性损失 $\mathcal{L}_{align}$（Eq. 8），强制运动基元的时间演化与视觉特征的变化对齐，使视觉表征在保持语义丰富性的同时获得几何与运动一致性。

### 历史感知的时序建模

MoVie在时序编码器输入中引入了**固定记忆库的历史视觉特征** $\mathbf{F_h}$，与当前运动-视觉特征拼接后送入交替Transformer-TCN的时序编码器TM：

$$\mathbf{F_{mv}'} = \mathrm{TM}(\mathrm{concat}[\mathbf{F_{mv}}, \mathbf{F_h}])$$

这一设计与运动正则化形成互补：运动基元提供短时动态约束，历史特征则捕获长期时序依赖。消融实验表明，引入历史特征带来额外性能提升，证明两种时序信息源具有协同效应（Table 3）。

### 创新点的决定性实验证据

运动密集型活动的巨大增益直接验证了框架的核心价值。在TSU-CS数据集上，“起身”动作提升+46.9%，“搅拌”提升+32.8%，而缺乏全身运动的动作（如“从瓶子喝水”-4.1%）提升微小甚至下降（Table 4）。这表明MoVie精准捕获了动作的运动本质，而非简单地从多模态数据中获益。整体上，MoVie以I3D特征在TSU-CS上超越先前最优视觉方法**+15.9% mAP**（Table 1），在Multi-THUMOS上提升**+3.7% mAP**，为运动-视觉结构化融合的有效性提供了强有力的实证支撑。



MoVie 将人体运动视为结构化的物理先验，而非简单的辅助模态。其核心流程由两条并行的编码通路与一个跨模态正则化模块构成，最终通过时序编码器输出帧级多标签动作预测。

**视觉通路**：输入视频片段 $\mathbf{v}$ 经过冻结的预训练视觉编码器 $\operatorname{Ev}$（如 I3D 或 ViCLIP）提取每帧视觉特征 $\mathbf{F}_{\mathbf{v}}$，保留丰富的语义与外观信息。

**运动通路**：骨架序列经由堆叠的时空层（空间多头注意力 + 时间卷积网络）编码为每帧、每人的运动嵌入 $\mathbf{F}$。随后，**结构化运动投影模块（SMP）** 将运动特征投影到可学习的运动字典 $\mathbf{D}_{\mathbf{m}}$ 上，获得 $K$ 个物理基元的激活强度 $\pmb{\alpha}$。这些基元经 MLP 精炼 $\tilde{\pmb{\alpha}} = \sigma(\pmb{\alpha})$ 后，通过交互池化算子 $\mathcal{G}_p$ 聚合多人的运动描述，得到统一的帧级运动基元表示 $\hat{\pmb{\alpha}} \in \mathbb{R}^{K \times T}$。

**跨模态融合**：**运动引导特征正则化模块（MGFR）** 是连接两条通路的关键。它不采用直接拼接或晚期融合，而是通过正交投影矩阵 $\mathbf{Q}$ 将运动基元信号注入视觉特征空间：

$$\mathbf{F}_{\mathbf{mv}} = \epsilon(\mathbf{F}_{\mathbf{v}}) + \lambda (\mathbf{Q}^{\top} \hat{\alpha})$$

其中 $\mathbf{Q}$ 的列向量满足正交约束 $\langle \mathbf{q}_i, \mathbf{q}_j \rangle = 0\ (i \neq j)$，确保不同运动方向在视觉通道中解耦，作为结构化的正则化器调制视觉表示。同时，时序一致性损失 $\mathcal{L}_{align}$ 约束运动基元变化与视觉特征的时间演化对齐。

**时序建模与预测**：运动正则化后的特征 $\mathbf{F}_{\mathbf{mv}}$ 与来自固定记忆库的历史视觉特征 $\mathbf{F}_{\mathbf{h}}$ 拼接后，送入时序编码器 TM（交替 Transformer 与 TCN 层，沿用 MS-TCT 架构），捕获全局与局部时序依赖。最终，逐帧分类器以二分类交叉熵损失 $\mathcal{L}_{det}$ 输出多标签动作概率。

整个框架的模块关系与信息流可参见 Figure 1（框架总览）和 Figure 2（规则化运动-视觉特征学习流程）。

![[assets/figures/papers/paper_list_l1072_https_openaccess_thecvf_com_content_CVPR2026_html_Yang_MoVie_Broaden_You/figures/001_Figure_1.jpg]]
*Figure 1: Overview of the MoVie framework. (a) Conventional RGB-based methods struggle to capture complex and compositional motions. (b) MoVie introduces motion as a structured physical prior to complement visual representation. (c) Structured motion primitives are learned from skeleton sequences through a motion decomposition model. (d) The Motion-guided Feature Regularization (MGFR) aligns these primitives to inject geometric and physical cues into the visual space, and the learned features are sent to a history-aware Multi-modal Temporal Processing for more accurate action detection*



MoVie 的核心设计逻辑是将骨架运动视为结构化的物理先验，通过“分解-对齐-注入”三阶段将其有机地融入视觉特征空间，而非简单地拼接或晚期融合。以下按模块阐述其关键机制与公式。

### 3.1 视觉编码器

视觉编码器 $E_v$ 采用冻结的预训练模型（如 I3D 或 ViCLIP），从输入视频片段 $\mathbf{v}$ 中提取逐帧视觉特征：

$$\mathbf{F}_{\mathbf{v}} = E_v(\mathbf{v})$$

$\mathbf{F}_{\mathbf{v}}$ 作为后续运动正则化的基础视觉表示，在整个训练过程中保持冻结，确保视觉特征提取与基线方法一致。

### 3.2 结构化运动投影（SMP）

SMP 模块的核心功能是将粗糙的标签驱动骨架特征分解为细粒度的运动基元激活，从而捕捉动作的物理动力学本质。

**运动特征提取。** 给定骨架序列，首先通过堆叠的时空层（多头注意力空间层 + TCN 时序层）提取每帧、每人的运动嵌入：

$$\mathbf{F} = [\mathbf{f}_1, \ldots, \mathbf{f}_T], \quad \mathbf{f}_t = \{\mathbf{f}_t^{(1)}, \ldots, \mathbf{f}_t^{(M)}\}$$

其中 $T$ 为帧数，$M$ 为检测到的人数。

**运动基元激活。** 将运动特征投影到可学习的运动字典 $\mathbf{D}_{\mathbf{m}} \in \mathbb{R}^{K \times d}$ 上，计算每个基元的激活强度：

$$\pmb{\alpha} = \| \mathbf{D}_{\mathbf{m}} \mathbf{F} \|_2, \quad \pmb{\alpha} \in \mathbb{R}^{K \times T \times M}$$

其中 $K$ 为基元数量。这一投影将连续的运动轨迹量化为 $K$ 个物理基元的组合激活模式。

**激活精炼与多人池化。** 通过 MLP 投影 $\sigma(\cdot)$ 稳定噪声，再利用交互池化算子 $\mathcal{G}_p$ 聚合多人基元为统一的逐帧运动描述子：

$$\hat{\pmb{\alpha}} = \mathcal{G}_p(\sigma(\pmb{\alpha})) \in \mathbb{R}^{K \times T}$$

消融实验表明，MLP 交互池化优于简单的 max/mean 池化，验证了多人运动加权融合的有效性。

### 3.3 运动引导特征正则化（MGFR）

MGFR 是 MoVie 实现运动-视觉结构化融合的关键模块。其核心思想是通过正交投影将运动基元作为正则化器注入视觉特征空间，而非直接拼接。

**正交投影注入。** 引入可学习的投影矩阵 $\mathbf{Q} \in \mathbb{R}^{d_v \times K}$，将运动基元激活 $\hat{\pmb{\alpha}}$ 映射到视觉通道空间，与视觉特征相加：

$$\mathbf{F}_{\mathbf{mv}} = \epsilon(\mathbf{F}_{\mathbf{v}}) + \lambda (\mathbf{Q}^{\top} \hat{\alpha})$$

其中 $\epsilon(\cdot)$ 为视觉特征的线性投影，$\lambda$ 控制运动信号的注入强度。

**正交性约束。** 为确保不同运动基元在注入时相互解耦、避免信息冗余，对投影矩阵 $\mathbf{Q}$ 的列向量施加正交性约束：

$$\langle \mathbf{q}_i, \mathbf{q}_j \rangle = \begin{cases} 0, & i \neq j \\ 1, & i = j \end{cases}$$

消融实验直接验证了这一约束的必要性：移除正交性约束导致 TSU-CS 上 mAP 下降 2.8%，证明正交投影对齐是实现有效正则化的必要条件。

**时序一致性损失。** 为使运动注入与视觉特征的时序演化保持一致，引入对齐损失：

$$\mathcal{L}_{align} = \frac{1}{T}\sum_{t=1}^{T}\left\| \mathbf{Q}^{\top}\hat{\pmb{\alpha}}_t - \left(\epsilon(\mathbf{F}_{\mathbf{v},t}) - \mathbf{F}_{\mathbf{mv}}^{mean}\right) \right\|_2^2$$

该损失强制运动基元激活的时序变化与视觉特征偏离均值的模式对齐，从而增强运动-视觉的时序一致性。

### 3.4 跨模态时序编码与检测

运动正则化后的特征 $\mathbf{F}_{\mathbf{mv}}$ 与历史视觉特征 $\mathbf{F}_{\mathbf{h}}$（来自固定记忆库）拼接后送入时序编码器 TM：

$$\mathbf{F}_{\mathbf{mv}}^{\prime} = \mathrm{TM}(\mathrm{concat}[\mathbf{F}_{\mathbf{mv}}, \mathbf{F}_{\mathbf{h}}])$$

TM 沿用 MS-TCT 的设计，交替使用 Transformer 和 TCN 层捕获全局与局部时序依赖。最终通过多标签分类器输出逐帧动作概率，训练采用二分类交叉熵损失：

$$\mathcal{L}_{det} = -\frac{1}{T}\sum_{t,c} [ y_{t,c}\log P_{t,c} + (1-y_{t,c})\log(1-P_{t,c}) ]$$

整体训练目标为 $\mathcal{L} = \mathcal{L}_{det} + \mathcal{L}_{align}$。消融实验证实，引入历史特征可进一步提升性能，表明运动正则化与长期时序上下文是互补的。

### 补充图表

![[assets/figures/papers/paper_list_l1072_https_openaccess_thecvf_com_content_CVPR2026_html_Yang_MoVie_Broaden_You/figures/002_Figure_2.jpg]]
*Figure 2: Overview of the Regularized Motion-Video Feature Learning. Given an input skeleton sequence, we obtain the features*

![[assets/figures/papers/paper_list_l1072_https_openaccess_thecvf_com_content_CVPR2026_html_Yang_MoVie_Broaden_You/figures/009_Figure_4.jpg]]
*Figure 4: Example of the SMP (“Get up”). Primitives in (a) that correspond to torso bending and leg extension are strongly activated. Primitives in (b) with almost no activation change mostly correspond to arm rotation or minor upper-body motion*



## 实验与关键发现

### 主要结果：结构化运动先验的决定性作用

MoVie 在三个主流时序动作检测数据集上进行了系统验证，核心结论高度一致：**将骨架运动视为结构化物理先验而非简单辅助模态，能够为视觉特征注入几何与运动一致性，从而系统性提升动作理解能力**。在 TSU-CS 数据集上，MoVie 以冻结的 I3D 视觉特征取得 49.6% 的帧级 mAP，**超越先前最优纯视觉方法 15.9 个百分点**；采用更强 ViCLIP 视觉编码器时进一步提升至 50.1%（Table 1）。在 Multi-THUMOS 上，MoVie（ViCLIP）以 48.3% mAP **超越先前最优方法 3.7 个百分点**。在 Charades 上取得 33.5% mAP，同样展现了稳定的增益。这一结果直接验证了核心洞察：粗糙的标签驱动骨架特征与 RGB 异构空间相互干扰，而 MoVie 通过运动基元分解与正交投影对齐，实现了有效的结构化融合。

![[assets/figures/papers/paper_list_l1072_https_openaccess_thecvf_com_content_CVPR2026_html_Yang_MoVie_Broaden_You/figures/003_Table_1.jpg]]
*Table 1: Frame-level mAP on TSU, Charades and Multi-THUMOS for comparison with SoTA action detection methods. Modalities used by the approaches are shown for reference*

事件级检测指标进一步佐证了这一结论。在 TSU-CS 和 PKU-MMD 事件级评测中，MoVie 一致提升了多模态基线的检测精度（Table 5），表明运动正则化带来的时序一致性不仅改善帧级判别，也增强了事件边界的定位能力。

![[assets/figures/papers/paper_list_l1072_https_openaccess_thecvf_com_content_CVPR2026_html_Yang_MoVie_Broaden_You/figures/007_Table_5.jpg]]
*Table 5: Event-level detection performance on TSU-CS and PKU-MMD (PKU)-CS. MoVie improves multi-modal baselines*

### 消融实验：运动分解与正交正则化的必要性

为厘清各模块的因果贡献，论文设计了系统的消融实验（Table 2）。在 TSU-CS 数据集上：

![[assets/figures/papers/paper_list_l1072_https_openaccess_thecvf_com_content_CVPR2026_html_Yang_MoVie_Broaden_You/figures/004_Table_2.jpg]]
*Table 2: Ablation study on MGFR, SMP, and orthogonality on TSU and Charades datasets*

- **完整 MoVie（SMP + MGFR，字典 K=128）** 取得 50.1% mAP（ViCLIP）和 33.5%（Charades），为所有配置中最高。
- **移除 MGFR 中的正交性约束** 导致 TSU-CS 性能下降 2.8 个百分点，直接证明正交投影对齐是实现有效正则化的必要条件——若投影矩阵列向量不正交，运动方向信号会相互耦合，无法为视觉通道提供解耦的几何约束。
- **去除运动分解（SMP）而直接使用原始骨架特征** 同样导致性能显著下降，表明将运动特征投影到可学习字典、分解为物理基元，是桥接异构特征空间的关键步骤。
- **仅使用视觉特征或仅使用运动特征** 的基线性能均远低于融合方案，验证了两模态互补的必要性。

进一步消融（Table 3）揭示了两个重要设计选择：

![[assets/figures/papers/paper_list_l1072_https_openaccess_thecvf_com_content_CVPR2026_html_Yang_MoVie_Broaden_You/figures/005_Table_3.jpg]]
*Table 3: Ablation on interaction pooling and history features on TSU and Charades datasets*

1. **多人交互池化**：采用 MLP 驱动的交互池化（Interaction Pooling）聚合多人运动基元，优于简单的 max/mean 池化，证明对不同人体实例的运动信号进行加权融合能够更好地捕捉多人协作或交互场景。
2. **历史记忆库**：引入固定记忆库存储历史视觉特征，与当前运动-视觉特征拼接后送入时序编码器，进一步提升性能。这表明运动正则化与长期时序上下文是互补的——运动基元提供物理一致性约束，历史特征提供长程语义依赖。

### 逐类增益分析：运动密集型活动大幅受益

Table 4 的逐类分析揭示了 MoVie 增益的分布规律，这一规律直接呼应了框架的设计动机——**精准捕获动作的运动本质**：

![[assets/figures/papers/paper_list_l1072_https_openaccess_thecvf_com_content_CVPR2026_html_Yang_MoVie_Broaden_You/figures/008_Table_4.jpg]]
*Table 4: Activities that benefit on frame-level mAP (%) from MoVie on TSU-CS, compared with Visual-only model [12]*

- **运动密集型活动获得巨大增益**：“起身”（Get up）提升 46.9%，“搅拌”（Stir）提升 32.8%，“倒液体”（Pour liquid）提升 23.4%。这些动作涉及显著的全身运动或大范围肢体位移，视觉模型容易因外观变化、遮挡或背景干扰而失效，而运动基元提供的物理动力学信号恰好弥补了这一缺陷。
- **缺乏明显运动的动作提升微小**：“站立”（Stand）、“坐”（Sit）等静态或微动动作的增益有限，因为视觉特征本身已能较好捕捉其语义，运动正则化的边际贡献自然较小。

### 失败模式与定性分析

尽管整体提升显著，逐类分析同时暴露了框架的边界：

- **细粒度手物交互动作出现性能下降**：“从瓶子喝水”（Drink from a bottle）下降 4.1%，“搅拌咖啡”（Stir coffee）等涉及精细手部操作的动作增益有限或为负。这是因为 MoVie 的运动字典专注于全身动力学，**缺乏对手部关键点和物体交互的显式建模**，导致手部微小但关键的运动模式无法被有效分解和注入。
- **严重遮挡下的骨架质量退化**：Figure 3 的定性示例显示，在大面积遮挡导致骨架估计不可靠时，运动基元的质量会下降，从而削弱正则化效果。不过即使在光照恶劣或背景混乱的场景中，只要骨架估计基本可靠，MoVie 仍能提供一致的性能提升，展现了运动先验对视觉噪声的鲁棒性。

![[assets/figures/papers/paper_list_l1072_https_openaccess_thecvf_com_content_CVPR2026_html_Yang_MoVie_Broaden_You/figures/006_Figure_3.jpg]]
*Figure 3: Examples of video with challenging light conditions (top right) and confused background (bottom right), video without accurate skeleton data in large occlusions (top left), video with the simple scenario (bottom left). MoVie can improve the performance compared to single-modal approaches in all these cases*

### 关键图表结论速览

- **Table 1**：MoVie 在 TSU-CS 上以 I3D 特征超越先前最优视觉方法 15.9% mAP，Multi-THUMOS 上超越 3.7%，Charades 上取得 33.5%，验证结构化运动融合的决定性作用。
- **Table 2**：移除正交性约束导致 TSU-CS 性能下降 2.8%，去除 SMP 同样显著下降，证明运动基元分解与正交投影对齐是框架有效性的两个必要条件。
- **Table 3**：MLP 交互池化优于简单池化，历史记忆库与运动正则化互补，共同提升时序建模能力。
- **Table 4**：运动密集型活动（起身 +46.9%、搅拌 +32.8%）大幅受益，手物交互动作（从瓶子喝水 -4.1%）下降，暴露手部建模缺失的局限。
- **Figure 3**：定性示例展示 MoVie 在光照恶劣、背景混乱场景下的鲁棒性，以及骨架质量退化时的性能边界。



## 定位与知识库关联

### 1. 与现有方法的谱系关系

MoVie 的核心贡献在于将人体骨架运动重新定位为**结构化的物理先验**，而非单纯的辅助模态。这一视角使其在方法谱系中处于视觉动作检测与多模态融合的交叉地带，但与现有工作存在本质差异。

**与视觉动作检测方法的对比。** 现有视觉方法（如 **MS-TCT** (Dai et al., CVPR 2022)、**PDAN** (Dai et al., WACV 2021)、**MLAD** (Tirupattur et al., CVPR 2021)、**DualDETR** (Zhu et al., CVPR 2024)、**AAN** (Dai et al., BMVC 2023)）主要依赖 RGB 外观特征，通过改进时序建模或注意力机制来捕捉动作。然而，这些方法缺乏对物理运动动力学的显式建模，在复杂、组合性动作（如“起身”“搅拌”）上表现受限。MoVie 通过引入结构化运动基元，从根本上弥补了这一缺陷——在 TSU-CS 数据集上以 I3D 特征超越先前最优视觉方法 **+15.9% mAP**（Table 1），直接验证了运动先验的决定性作用。

**与直接引入骨架模态的方法对比。** 现有工作通常将骨架特征（如 AGCN 提取的标签驱动特征）通过直接拼接或晚期融合与视觉特征结合。这种粗糙的融合方式存在两个关键问题：(1) 骨架特征由全局动作标签训练，无法捕捉细粒度运动动态；(2) 骨架与 RGB 特征处于异构空间，直接拼接会导致相互干扰。MoVie 通过两个核心模块解决了这些问题：**Structural Motion Projection (SMP)** 将运动分解为可学习的物理基元，产生细粒度的基元激活强度；**Motion-guided Feature Regularization (MGFR)** 则通过正交投影将运动基元作为正则化器注入视觉通道空间，而非简单拼接。消融实验表明，移除正交性约束导致 TSU-CS 性能下降 **-2.8%**（Table 2），证明正交投影对齐是实现有效异构融合的必要条件。

**与多模态时序检测方法的对比。** 在时序建模层面，MoVie 继承了 **MS-TCT** (Dai et al., CVPR 2022) 的 Transformer-TCN 交替架构，但在此基础上引入固定记忆库（memory bank）缓存历史视觉特征，与当前运动-视觉特征拼接后送入时序编码器。这一设计使运动正则化与长期时序上下文形成互补，进一步提升了检测精度（Table 3）。

### 2. 适用边界与局限性

尽管 MoVie 在多个基准上取得显著提升，其设计存在明确的适用边界：

**严重遮挡导致骨架估计不可靠时性能受限。** 框架依赖骨架序列提取运动基元，当遮挡严重导致骨架估计质量下降时，运动基元的可靠性随之降低，进而影响 MGFR 的正则化效果。Figure 3 的定性示例（top left）展示了这一场景，虽然 MoVie 仍优于纯视觉方法，但提升幅度有限。

**细粒度手物交互动作存在性能下降。** MoVie 专注于全身运动动力学，对涉及手部精细操作的动作（如“从瓶子喝水” -4.1%）仍存在性能下降（Table 4）。这表明框架缺乏对手部关键点和物体交互的显式建模能力。

**运动字典的泛化边界。** 运动字典基于预训练数据学习，对训练集中未见过的新运动模式泛化能力有限。字典规模 K 的选择目前依赖经验调参，缺乏任务驱动的自适应机制。

### 3. 开放问题

基于上述局限，以下方向值得进一步探索：

1. **手物交互的基元扩展。** 如何将手部关键点和物体交互信息集成到运动基元框架中，以改进细粒度动作检测？这可能需要构建包含手物关系的扩展运动字典。

2. **运动不确定性建模。** 在遮挡或低质量骨架条件下，能否显式建模运动基元激活的不确定性，从而提升框架的鲁棒性？例如，通过概率化运动投影或自适应调整正则化强度。

3. **运动字典的自适应优化。** 运动字典的规模 K 与基元的物理可解释性是否可以进一步自动化或由下游任务驱动优化？当前的固定字典设计限制了模型对未知运动模式的适应能力。

4. **跨域泛化能力。** MoVie 在三个数据集上展示了有效性，但其运动字典和正则化策略在更广泛的域偏移（如不同相机视角、不同运动风格）下的泛化能力尚未得到系统验证。



## 原文 PDF

![[paperPDFs/CVPR_2026/MoVie_Broaden_Your_Views_with_Human_Motion_for_Action_Detection.pdf]]
