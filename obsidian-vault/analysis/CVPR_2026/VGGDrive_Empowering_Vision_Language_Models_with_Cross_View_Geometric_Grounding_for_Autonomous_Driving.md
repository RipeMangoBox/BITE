---
title: "VGGDrive: Empowering Vision-Language Models with Cross-View Geometric Grounding for Autonomous Driving"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/VGGDrive_Empowering_Vision_Language_Models_with_Cross_View_Geometric_Grounding_for_Autonomous_Driving.pdf
project_link: null
code_link: "https://github.com/WJ-CV/VGGDrive"
aliases:
- VGGDrive
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
- topic/benchmarks_datasets_evaluation
core_operator: 将成熟三维基础模型(VGGT)的跨视角几何特征通过即插即用的层次化自适应注入机制(CVGE)注入到VLM的视觉表示中，使模型获得几何定位能力。
primary_logic: 通过解耦基础LLM的层级结构，在每一解码层利用多头交叉注意力融合2D视觉查询与3D几何键值，并显式编码相机内外参进行几何对齐，实现从“被动接收”到“主动挖掘”的跨模态深度融合，从而在保持VLM语言能力的同时大幅提升多任务驾驶性能。
claims:
- VG-GDrive在NAVSIM闭环规划中PDMS达到88.76，比基础VLM(86.04)提升2.72，比VGGT-Dist(86.68)和VGGT-Add(86.10)明显更优。
- 在NuInstruct的跨视角风险物体感知(MAP)任务上，VG-GDrive达到37.49，较基础VLM(6.15)提升31.34点，远超其他集成方案。
- 单层注入3D特征即可将PDMS提升至约88，全层自适应注入进一步达到最优，证明层次化注入的有效性。
- 在DriveLM的精确匹配(Match)指标上，VG-GDrive较baseline提升15.23，达到49.77。
---

# VGGDrive: Empowering Vision-Language Models with Cross-View Geometric Grounding for Autonomous Driving

> [!tip] 核心洞察
> 通过解耦基础LLM的层级结构，在每一解码层利用多头交叉注意力融合2D视觉查询与3D几何键值，并显式编码相机内外参进行几何对齐，实现从“被动接收”到“主动挖掘”的跨模态深度融合，从而在保持VLM语言能力的同时大幅提升多任务驾驶性能。

| 字段 | 内容 |
|------|------|
| 中文题名 | VGGDrive：赋能视觉语言模型以跨视角几何定位用于自动驾驶 |
| 英文题名 | VGGDrive: Empowering Vision-Language Models with Cross-View Geometric Grounding for Autonomous Driving |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2602.20794) · [Code](https://github.com/WJ-CV/VGGDrive) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction #topic/benchmarks_datasets_evaluation |
| Method | VGGDrive |
| Dataset | NAVSIM navtest, NuInstruct, DriveLM, OmniDrive |

> [!tip] 效果简介
> - NAVSIM navtest 上，PDMS 88.76 vs 86.04 (Qwen2.5-VL-7B) (+2.72)。
> - NuInstruct 上，MAP 37.49 vs 6.15 (Qwen2.5-VL-7B) (+31.34)。
> - DriveLM 上，Match 49.77 vs 34.54 (Qwen2.5-VL-7B) (+15.23)。

## 概述

视觉语言模型(VLM)凭借强大的常识推理与指令遵循能力，正被逐步引入自动驾驶领域。然而，VLM本质上缺乏跨视角的3D几何建模能力，难以在复杂驾驶场景中进行精确的空间感知与安全导航，导致其在风险目标感知、运动预测和轨迹规划等关键任务上表现平庸。

**核心瓶颈**：VLM仅依赖2D视觉编码器输出的二维语义特征，无法显式利用多视角图像之间的几何约束，造成空间定位缺失。

**方法定位**：VGGDrive提出一种即插即用的跨视角几何定位框架，将冻结的三维基础模型VGGT提取的几何一致3D特征，通过**跨视角3D几何使能器(CVGE)**注入到基础VLM的解码层中。CVGE解耦LLM的层级结构，在每一解码层利用多头交叉注意力融合2D视觉查询与3D几何键值，并显式编码相机内外参进行几何对齐，实现从“被动接收”到“主动挖掘”的跨模态深度融合。

**主要结果**：在五个自动驾驶基准上，VGGDrive一致且显著地提升了基础VLM的性能：
- **NAVSIM闭环规划**：PDMS达到88.76，较基础VLM(86.04)提升2.72；
- **NuInstruct跨视角风险感知**：MAP达到37.49，较基础VLM(6.15)提升31.34；
- **DriveLM空间推理**：Match指标达到49.77，提升15.23；
- **nuScenes开环规划**：碰撞率降至0.22%，较基线降低近一半。

该框架在保持VLM语言能力的同时，大幅增强了自动驾驶所需的空间感知与规划能力，为VLM在具身智能场景中的应用提供了新的范式。

## 背景与动机

### 自动驾驶中的视觉语言模型困境

视觉语言模型（VLM）凭借其强大的常识推理与泛化能力，正被越来越多地引入自动驾驶领域，用于处理风险目标感知、运动预测、轨迹规划等多类任务。然而，一个根本性瓶颈始终存在：**VLM 本身缺乏跨视角的 3D 几何建模能力**。在自动驾驶场景中，车辆通常搭载多视角相机，场景理解高度依赖精确的空间感知——目标的相对位置、运动方向、距离与碰撞风险等，而这些恰是 VLM 所不擅长的。

这一瓶颈导致基础 VLM 在多项关键驾驶任务上表现平庸。以 **Qwen2.5-VL-7B**（Bai et al., arXiv 2025）为例：在 NAVSIM 闭环规划的 PDMS 指标上仅取得 86.04，在 NuInstruct 的跨视角风险物体感知（MAP）任务上更是低至 6.15。这些数字表明，仅靠语言模型的语义推理，无法弥补几何感知的结构性缺失。

### 现有集成方案的局限

为了赋予 VLM 以 3D 感知能力，研究者尝试将成熟的视觉 3D 基础模型（如 VGGT）与 VLM 结合，但现有方案存在明显不足（Figure 1）：

- **VGGT-Dist**：通过知识蒸馏将 3D 特征隐式迁移到 VLM，但蒸馏过程信息损失严重，VLM 难以真正“理解”几何结构。
- **VGGT-Add**：直接将 3D 特征与 2D 视觉特征相加融合，但简单的线性组合无法建立跨模态的动态交互，3D 信息往往被稀释或忽略。

这两种方案本质上都是“被动接收”——VLM 被强制接收 3D 信号，却缺乏主动挖掘几何信息的能力。实验表明，VGGT-Dist 和 VGGT-Add 在 NAVSIM 上分别仅达到 86.68 和 86.10 的 PDMS，相比基础 VLM 提升极为有限。

### 核心动机

上述分析揭示了一个清晰的因果机制：**VLM 的几何盲区源于其解码器层级结构中缺乏对 3D 空间的显式建模，而简单的特征注入无法弥补这一结构性缺陷**。本文的核心动机由此展开：

1. **解耦 LLM 层级结构**：不再将 VLM 视为黑箱，而是拆解其解码层，在每一层中提取 2D 视觉表示，为几何信息的深度注入提供入口。
2. **建立跨模态主动融合**：设计一种可学习的交叉注意力机制，使 2D 视觉查询能够“主动挖掘”3D 几何键值中的关键信息，而非被动接收。
3. **显式编码相机参数**：将相机内外参显式嵌入融合过程，实现 2D 像素与 3D 空间的几何对齐，确保注入的几何特征具有空间一致性。

这一思路最终凝结为 **VGGDrive** 框架——通过即插即用的 **跨视角 3D 几何使能器（CVGE）** 和层次化自适应注入机制，将冻结的 VGGT 模型生成的跨视角几何特征深度注入 VLM，在保持语言能力的同时，大幅提升多任务驾驶性能。

## 核心创新

### 创新动机：VLM在自动驾驶中的几何盲区

视觉语言模型（VLMs）在通用场景理解与语言推理上展现出强大能力，但在自动驾驶任务中面临一个根本性瓶颈：**缺乏跨视角的3D几何建模能力**。基础VLM仅处理2D图像特征，无法显式理解多相机之间的空间对应关系与场景深度结构，导致其在风险目标感知、运动预测和闭环轨迹规划等任务上表现平庸。以Qwen2.5-VL-7B为基线，其在NuInstruct跨视角风险物体感知（MAP）任务上仅得6.15分（Table 2），在NAVSIM闭环规划中PDMS为86.04（Table 1），均显著低于具备几何感知能力的方法。

### 核心洞察：从“被动接收”到“主动挖掘”的跨模态深度融合

VGGDrive的核心洞察在于**解耦基础LLM的层级结构，将成熟的3D基础模型（VGGT）的跨视角几何特征通过层次化自适应注入机制融入VLM的视觉表示中**，使模型获得几何定位能力。与现有集成方案的本质区别在于：

- **VGGT-Dist**：通过蒸馏将3D知识间接传递至VLM，信息损失严重，融合深度不足。
- **VGGT-Add**：将3D特征与2D特征简单相加，缺乏跨模态动态交互，无法自主筛选关键几何信息。
- **VGGDrive**：在LLM的**每一解码层**利用**多头交叉注意力**，以2D视觉特征为查询（Q）、3D几何特征为键（K）和值（V），并**显式编码相机内外参**进行几何对齐，实现2D查询主动从3D特征中挖掘关键信息。

这种“主动挖掘”机制使得模型能够根据当前解码层的语义需求，动态选择最相关的几何线索，而非被动接收固定融合后的特征。

### 关键创新点（Changed Slots）

以下三个维度的创新构成了VGGDrive相对于基线VLM的核心改进：

#### 1. 视觉特征注入方式：从纯2D到层次化3D几何增强

| 维度 | 基线（Qwen2.5-VL-7B） | VGGDrive |
|------|----------------------|----------|
| 输入特征 | 仅VLM视觉编码器输出的2D视觉嵌入 | 冻结VGGT提取的跨视角3D几何特征，通过CVGE在LLM每一解码层进行层次化自适应注入 |
| 证据 | — | Section 3.2, Eq. 4 |

**关键机制**：VGGT利用多视角图像生成几何一致的3D特征 $V^{3d}$，该特征在所有解码层间共享。CVGE在每一层 $i$ 将该共享3D特征与当前层的2D视觉表示 $V_i^{2d}$ 融合，输出几何增强的嵌入 $V_i^{3d}$。消融实验证实，**单层注入即可将PDMS提升至约88，全层自适应注入达到最优88.76**（Figure S1, Section B），验证了层次化注入的必要性。

#### 2. 跨模态融合机制：从无融合到多头交叉注意力几何对齐

| 维度 | 基线（Qwen2.5-VL-7B） | VGGDrive |
|------|----------------------|----------|
| 融合方式 | 无跨模态融合；VLM仅处理2D特征 | 利用多头交叉注意力（MHCA），以2D特征为Q、3D特征为K/V，并融入相机内外参编码 |
| 证据 | — | Section 3.3, Eq. 7-10 |

**关键机制**：CVGE首先通过MLP将2D和3D特征投影至低维空间（Eq. 7-8），然后利用显式编码的相机内外参（Eq. 9）对K/V进行几何位置增强，最后通过多头交叉注意力实现动态信息融合（Eq. 10）。消融实验（Table 6）表明，采用CVGE的层次化注入（OURS）在NAVSIM上PDMS达88.76，显著优于特征相加（VGGT-Add, 86.10）、蒸馏（VGGT-Dist, 86.68）以及LLM前融合（ID-5, 86.80），证明跨模态交叉注意力机制是实现深度几何定位的核心。

#### 3. 层级结构利用：从整体前向到解耦逐层注入

| 维度 | 基线（Qwen2.5-VL-7B） | VGGDrive |
|------|----------------------|----------|
| 层级利用 | LLM作为整体前向；各层隐藏状态无额外干预 | 解耦LLM，提取每层2D视觉表示，注入CVGE输出的3D增强表示后通过残差连接传递 |
| 证据 | — | Section 3.2, Eq. 2-6 |

**关键机制**：将LLM解耦为 $n$ 个解码层，每层隐藏状态 $X_i$ 中的视觉token通过图像位置掩码提取为 $V_i^{2d}$（Eq. 3），经CVGE增强后通过残差连接 $x_i = X_i + X_i'$（Eq. 6）更新隐藏状态。消融实验（Table 7）显示，**移除残差连接（ID-4）导致性能下降**，证明在LLM内部注入时保持原始隐藏状态的残差至关重要。

### 创新效果：跨任务几何定位能力的质变

上述创新带来的性能提升具有明显的**任务特异性**——几何密集型任务提升巨大，语义描述任务基本持平：

- **跨视角风险感知（NuInstruct MAP）**：37.49 vs. 6.15（+31.34），提升509%（Table 2）
- **闭环轨迹规划（NAVSIM PDMS）**：88.76 vs. 86.04（+2.72）（Table 1）
- **精确匹配（DriveLM Match）**：49.77 vs. 34.54（+15.23）（Table 3）
- **描述任务（OmniDrive Average）**：52.85 vs. 52.64（+0.21），几乎无变化（Table 4）

这种差异化提升模式直接验证了核心主张：VGGDrive赋予VLM的是**几何定位能力**，而非通用语言能力的提升。在需要精确空间感知的任务上，性能飞跃；在依赖语义理解的描述任务上，VLM原有能力得以完整保留。

## 整体框架

VGGDrive的整体架构围绕一个核心设计原则展开：**将冻结的视觉三维基础模型的跨视角几何建模能力，以即插即用的方式深度注入到基础视觉语言模型（VLM）的解码过程中**，从而赋予VLM原本不具备的空间感知与几何定位能力。

### 架构总览

如图3所示，VGGDrive由三个核心组件构成：

1. **基础VLM（Base VLM）**：采用**Qwen2.5-VL-7B**（Bai et al., arXiv 2025）作为骨干，负责处理多视角图像输入与语言指令，自回归生成推理和动作token。其视觉编码器从多视角图像中提取初始2D视觉嵌入，而LLM解码器则被解耦为多个独立的解码层，以便在每一层进行几何特征的层次化注入。

2. **层次化自适应注入机制（Hierarchical Adaptive Injection Mechanism）**：这是VGGDrive区别于现有VLM与3D模型集成方案的关键创新。传统方案（如VGGT-Dist的蒸馏对齐、VGGT-Add的特征相加）仅在LLM外部或单一位置进行特征融合，而VGGDrive将LLM解码器解耦为n层，在每一层提取2D视觉表示$V_i^{2d}$，通过CVGE注入几何信息后，将增强后的3D视觉嵌入$V_i^{3d}$以残差连接的方式更新隐藏状态$x_i = X_i + X_i'$，形成下一层的输入。这种逐层递进的注入策略使模型能够从浅层到深层持续挖掘和利用几何信息。

3. **跨视角3D几何使能器（Cross-view 3D Geometric Enabler, CVGE）**：作为2D视觉特征与3D几何特征之间的桥梁，CVGE通过MLP降维、相机内外参显式编码、多头交叉注意力融合三个子步骤，实现跨模态的深度交互。具体而言，2D视觉特征被投影为查询$Q$，3D几何特征被投影为键$K$和值$V$，通过多头交叉注意力机制让2D查询主动从3D键值中挖掘关键几何信息，最后经MLP升维恢复到原始维度。

### 数据流与模块关系

整个pipeline的数据流如下：

1. **多视角图像输入**：$C$个相机视角的图像$\{I_c\}_{c=1}^{C}$同时输入两个并行的处理分支——基础VLM的视觉编码器和冻结的**VGGT**模型（用于提取几何一致的跨视角3D特征$V^{3d}$）。

2. **2D视觉嵌入提取**：VLM视觉编码器将图像转换为视觉token，与语言指令$L$拼接后送入LLM解码器。解码器逐层前向，第$i$层的隐藏状态$X_i = DL_i(x_{i-1})$通过固定的图像位置掩码$M_{id}^{img}$提取出该层的2D视觉表示$V_i^{2d}$。

3. **几何特征注入**：每一层提取的$V_i^{2d}$与共享的3D特征$V^{3d}$一同输入CVGE模块。CVGE首先通过MLP将两者降维到统一空间，随后将相机内外参编码融入$K$和$V$向量中，利用多头交叉注意力实现2D查询对3D几何信息的自适应挖掘，输出几何增强的视觉嵌入$V_i^{3d}$。

4. **残差更新与逐层传递**：增强后的视觉嵌入通过残差连接与原始隐藏状态相加，更新后的隐藏状态继续传入下一解码层。这一设计确保了原始语言建模能力不被破坏，同时逐层累积几何信息。

5. **自回归生成**：经过所有解码层处理后，LLM基于注入几何信息的多模态序列自回归生成最终的推理和动作token。整个模型通过标准交叉熵损失进行优化：

$$L_{CE} = - \sum_{t=1}^{T} \log p_{\theta}(y_t | y_{<t}, \{I_c\}_{c=1}^{C}, L)$$

### 关键设计决策

- **冻结VGGT**：3D基础模型在训练过程中保持冻结，仅作为几何特征的静态提供者，避免了大规模3D模型训练的计算开销，同时保留了其预训练的跨视角几何一致性。
- **共享3D特征**：同一个$V^{3d}$被所有解码层共享，每层通过独立的CVGE模块（参数不共享）进行差异化融合，在效率与表达能力之间取得平衡。
- **相机参数显式编码**：将相机内外参通过齐次变换矩阵$T_i^{img2lidar}$显式编码到$K$和$V$中，使几何融合过程具备空间感知能力，是实现跨视角几何定位的关键。
- **残差连接的必要性**：消融实验（Table 7, ID-4）表明，移除残差连接会导致性能显著下降，证明在LLM内部注入时必须保留原始隐藏状态的通路，以维护语言模型的稳定性。

### 补充图表

![[assets/figures/papers/paper_list_l2428_https_arxiv_org_abs_2602_20794/figures/003_Figure_3.jpg]]
*Figure 3: Overview of VGGDrive. Specifically, the frozen visual 3D foundation model (VGGT [39]) extracts geometrically consistent 3D features V 3d through cross-view analysis, while the base VLM is decomposed into multiple decoder layers. The proposed CVGE sequentially integrates the shared 3D features V 3d with the 2D visual representations V 2di , injecting them V 3di through a hierarchical adaptive mechanism, thereby establishing geometric grounding and enabling deep enhancement of the VLM architecture*

![[assets/figures/papers/paper_list_l2428_https_arxiv_org_abs_2602_20794/figures/001_Figure_1.jpg]]
*Figure 1: Existing relevant paradigms vs. our VGGDrive. (a) The VLA paradigm for trajectory planning. (b) Two existing paradigms for integrating 3D foundation models (VGGT [39]) with VLMs: VGGT-Dist [11] and VGGT-Add [48]. (c) Our VG-GDrive, which leverages the VGGT model to profoundly empower the basic VLM with cross-view geometric grounding capabilities, thereby handling diverse autonomous driving tasks*

## 核心模块与公式推导

VGGDrive 的核心架构由三个模块构成：基础视觉语言模型（Base VLM）、层次化自适应注入机制（Hierarchical Adaptive Injection Mechanism）和跨视角三维几何使能器（CVGE）。其设计目标是将冻结的 VGGT 三维基础模型提取的跨视角几何一致性特征，通过即插即用的方式深度注入 VLM 的解码过程，赋予模型几何定位能力。

### 基础 VLM 与优化目标

基础 VLM 采用 **Qwen2.5-VL-7B**（Bai et al., arXiv 2025），输入为多视角图像序列 $\{I_c\}_{c=1}^{C}$ 和自然语言指令 $L$，自回归生成目标 token 序列 $y = (y_1, ..., y_T)$。模型通过标准交叉熵损失进行优化：

$$L_{CE} = - \sum_{t=1}^{T} \log p_{\theta}(y_t | y_{<t}, \{I_c\}_{c=1}^{C}, L)$$

该损失函数驱动 VLM 学习从多模态输入到驾驶决策 token 的映射。然而，基础 VLM 仅依赖视觉编码器输出的二维特征，缺乏对三维空间结构和跨视角几何关系的显式建模能力，这构成了性能瓶颈。

### 层次化自适应注入机制

VGGDrive 的核心创新在于解耦 LLM 的解码器层级结构，在每一层注入几何增强的视觉表示。设解码器共 $n$ 层，第 $i$ 层的隐藏状态为：

$$X_i = DL_i(x_{i-1}), \quad i = 1, ..., n$$

其中 $DL_i$ 为第 $i$ 层解码器，$x_{i-1}$ 为上一层输出。通过固定的图像位置掩码 $M_{id}^{img}$，从隐藏状态中提取二维视觉表示：

$$V_i^{2d} = X_i, \text{ if } M_{id}^{img} = 1$$

随后，CVGE 在第 $i$ 层将共享的三维几何特征 $V^{3d}$ 与当前层的二维视觉特征 $V_i^{2d}$ 融合，生成几何增强的三维视觉嵌入：

$$V_i^{3d} = CVGE_i(V^{3d}, V_i^{2d}), \quad i = 1, ..., n$$

更新后的视觉嵌入通过残差连接注入隐藏状态，形成下一层的输入：

$$x_i = X_i + X_i', \quad i = 1, ..., n$$

消融实验证实，移除残差连接（ID-4）会导致性能显著下降，证明在 LLM 内部注入时保持原始隐藏状态的残差路径至关重要（Table 7）。此外，单层注入三维特征即可将 PDMS 提升至约 88，全层自适应注入达到最优 88.76，验证了层次化机制的有效性（Figure S1）。

### 跨视角三维几何使能器（CVGE）

CVGE 是实现跨模态深度融合的关键模块。其核心操作流程如下：

**维度投影**：首先通过降维 MLP 将二维视觉特征和三维几何特征投影到低维空间：

$$Q = MLP_i^{down}(V_i^{2d}), \quad K, V = MLP_i^{down}(\text{Re}(V^{3d}))$$

其中 $Q$ 作为查询向量，$K$ 和 $V$ 作为键值对，$\text{Re}(\cdot)$ 表示对三维特征的重塑操作，使其与二维特征在空间维度上对齐。

**相机参数编码**：为建立二维像素与三维空间的几何对应关系，CVGE 显式编码相机内外参。图像到 LiDAR 坐标系的齐次变换矩阵为：

$$T_i^{img2lidar} = \left( K_i \cdot \begin{bmatrix} R_i^T & -R_i^T t_i \\ 0 & 1 \end{bmatrix} \right)^{-1}$$

其中 $K_i$ 为相机内参矩阵，$R_i$ 和 $t_i$ 分别为旋转矩阵和平移向量。该变换矩阵被编码并融入生成的 $K$ 和 $V$ 向量中，为交叉注意力提供显式的几何对齐信号。

**多头交叉注意力融合**：利用多头交叉注意力机制，使二维视觉查询能够自主挖掘三维几何键值中的关键信息：

$$V_i^{3d} = MLP_i^{up}(MHCA_i^h(Q, K, V))$$

其中 $MHCA_i^h$ 表示具有 $h$ 个注意力头的多头交叉注意力，$MLP_i^{up}$ 将融合后的特征升维回原始维度。消融实验表明，采用 CVGE 的层次化注入（OURS）在 NAVSIM 上 PDMS 达到 88.76，显著优于简单的特征相加（VGGT-Add, 86.10）、蒸馏（VGGT-Dist, 86.68）以及直接在 LLM 前融合（ID-5, 86.80），证实了跨模态交叉注意力机制的必要性（Table 6）。进一步消融显示，降维 MLP 的缩放因子 $s=4$ 在效率与性能间取得良好平衡，增加注意力头数 $h=8$ 可进一步略微提升性能（Table 9）。

### 闭环评估指标

在 NAVSIM 闭环规划评估中，采用预测驾驶员模型得分（PDMS）作为综合指标，其定义为：

$$PDMS = NC \times DAC \times \left( \frac { 5 \times EP + 5 \times TTC + 2 \times C } { 12 } \right)$$

该指标集成了五个子维度：无过失碰撞（NC）、可行驶区域遵循（DAC）、碰撞时间（TTC）、舒适度（C）和自我进展（EP），通过加权平均综合评估轨迹规划的质量与安全性。

## 实验与分析

### 核心发现

VGGDrive 在五个自动驾驶基准上一致且显著地提升了基础 VLM 的性能，验证了跨视角几何定位注入的有效性。最突出的增益出现在对空间感知要求极高的任务上：在 NuInstruct 的跨视角风险物体感知（MAP）任务中，VGGDrive 达到 **37.49**，较基础 VLM（Qwen2.5-VL-7B）的 6.15 提升 **31.34 点**（Table 2）；在 NAVSIM 闭环规划中，PDMS 达到 **88.76**，较基础 VLM 的 86.04 提升 2.72（Table 1）。在 DriveLM 的精确匹配（Match）指标上，VGGDrive 达到 49.77，较 baseline 提升 15.23（Table 3）。这些结果表明，几何定位能力的注入使 VLM 从“被动接收”2D 特征转变为“主动挖掘”3D 空间信息，从而在需要精确空间推理的任务上获得质的飞跃。

![[assets/figures/papers/paper_list_l2428_https_arxiv_org_abs_2602_20794/figures/004_Table_1.jpg]]
*Table 1: The performance comparison on the NAVSIM navtest [5] benchmark, evaluated using closed-loop metrics, involves both SOTA E2E approaches and existing VLA models under supervised fine-tuning. This evaluation aims to reflect the performance gains achieved by VGGDrive in enhancing the closed-loop trajectory planning capability of the base VLM*

![[assets/figures/papers/paper_list_l2428_https_arxiv_org_abs_2602_20794/figures/005_Table_2.jpg]]
*Table 2: The performance comparison on the NuInstruct dataset [6] is conducted against existing SOTA methods. This experiment is forecasting within autonomous driving scenarios. The symbol * indicates max crucial for evaluating the performance gains of VGGDrive in cross-view risk object perception (MAP), state prediction, and ego-motion   Accuracy+MAP+BLEU−MAE , 0 . 4*

![[assets/figures/papers/paper_list_l2428_https_arxiv_org_abs_2602_20794/figures/006_Table_3.jpg]]
*Table 3: The performance comparison on the DriveLM dataset [38] is conducted against existing SOTA methods. This experiment is crucial for evaluating the performance gains of VGGDrive in cross-view risk object perception (Match), action prediction and planning*

在描述类任务（OmniDrive）上，VGGDrive 仅带来 0.21 的微弱提升（52.85 vs 52.64，Table 4），这与预期一致——描述任务主要依赖语义理解，而非几何精度。在 nuScenes 开环规划中，VGGDrive 将碰撞率从 0.41% 降至 **0.22%**，L2 位移降至 0.31m（Table 5），进一步佐证了几何增强对安全关键指标的改善。

![[assets/figures/papers/paper_list_l2428_https_arxiv_org_abs_2602_20794/figures/007_Table_4.jpg]]
*Table 4: The performance comparison on the OmniDrive dataset [42] focuses on caption-related tasks in which base VLMs excel*

![[assets/figures/papers/paper_list_l2428_https_arxiv_org_abs_2602_20794/figures/008_Table_5.jpg]]
*Table 5: Performance comparison on nuScenes open-loop planning, with metrics from BEV-Planner’s reproduced results [30]*

### 集成方案对比：CVGE 的不可替代性

Table 6 的消融实验对比了 VGGT 与 VLM 的四种集成方式，直接验证了 CVGE 层次化交叉注意力机制的必要性：

![[assets/figures/papers/paper_list_l2428_https_arxiv_org_abs_2602_20794/figures/011_Table_6.jpg]]
*Table 6: Ablation study of various integration schemes between VGGT and VLM on the NAVSIM [5] and NuInstruct Datasets [6]. Inference speed is evaluated on the NuInstruct MAP task*

| 方案 | 机制 | NAVSIM PDMS | NuInstruct MAP |
|------|------|-------------|----------------|
| Baseline (Qwen2.5-VL-7B) | 无 3D 特征 | 86.04 | 6.15 |
| VGGT-Dist | 蒸馏对齐 | 86.68 | 24.39 |
| VGGT-Add | 特征相加 | 86.10 | 26.13 |
| ID-5（LLM 前融合） | 前置拼接 | 86.80 | 22.45 |
| **OURS (CVGE)** | 层次化交叉注意力 | **88.76** | **37.49** |

简单的特征相加（VGGT-Add）和蒸馏（VGGT-Dist）虽能带来一定增益，但在 MAP 任务上分别仅达到 26.13 和 24.39，远低于 CVGE 的 37.49。这表明，**跨模态交叉注意力机制是实现深度几何-语义融合的关键**——它允许 2D 视觉查询主动从 3D 几何键值中检索相关空间信息，而非被动接收固定映射。前置拼接方案（ID-5）在 MAP 上仅达 22.45，进一步说明在 LLM 内部逐层注入比简单的前端融合更有效。

### 关键组件消融

Table 7 对 VGGDrive 的核心组件进行了消融。移除残差连接（ID-4）导致性能显著下降，证明在 LLM 内部注入时保持原始隐藏状态的残差路径至关重要——它防止了几何特征的注入破坏原有的语义流。单层注入实验（Figure S1 及 Section B）显示，仅在某一解码层注入 3D 特征即可将 PDMS 提升至约 88，而全层自适应注入进一步达到最优 88.76，验证了层次化注入机制的累积增益。

![[assets/figures/papers/paper_list_l2428_https_arxiv_org_abs_2602_20794/figures/010_Table_7.jpg]]
*Table 7: Ablation Study of the Main Components of VGGDrive*

![[assets/figures/papers/paper_list_l2428_https_arxiv_org_abs_2602_20794/figures/015_Figure_S.1.jpg]]
*Figure S.1: Ablation analysis of closed-loop trajectory planning performance on the NAVSIM dataset when cross-view 3D geometric empowerment and adaptive injection are applied to individual decoding layers of the LLM*

### 3D 专家模型选择

Table 8 对比了不同 3D 基础模型作为几何特征提取器的效果。VGGT 在所有指标上均优于 DUSt3R 等替代方案，验证了 VGGT 跨视角几何特征的质量优势。这一选择是 VGGDrive 性能的底层保障——劣质的几何特征即使经过精心设计的融合机制，也无法带来实质性的空间感知提升。

![[assets/figures/papers/paper_list_l2428_https_arxiv_org_abs_2602_20794/figures/012_Table_8.jpg]]
*Table 8: Ablation Study of the 3D Expert Model*

### 效率与性能权衡

Table 9 对 CVGE 的超参数进行了灵敏度分析。缩放因子 $s=4$ 在效率与性能间取得良好平衡；将注意力头数增至 $h=8$ 可进一步略微提升性能，但计算开销相应增加。这为实际部署中的精度-延迟权衡提供了参考依据。

![[assets/figures/papers/paper_list_l2428_https_arxiv_org_abs_2602_20794/figures/013_Table_9.jpg]]
*Table 9: Further Ablation Analysis on the Navsim Benchmark*

### 失败模式与局限

尽管 VGGDrive 在多数任务上表现优异，仍需注意以下边界情况：
- **描述类任务增益微弱**：OmniDrive 上仅 0.21 的提升表明，几何定位注入对纯语义任务几乎无贡献，但也不会造成性能退化。
- **极端场景的可靠性未验证**：论文未提供在极端天气、照明条件或域外场景下的评估，VGGT 的几何特征质量在这些条件下是否依然可靠需要进一步验证。
- **计算开销**：CVGE 的层次化交叉注意力机制引入了额外计算成本，Table 6 中的推理速度数据（需查阅原文具体数值）表明其相比简单融合方案存在一定延迟增加。

## 方法谱系与知识库定位

### 1. 与现有范式的关系

VGGDrive 的核心贡献在于为视觉语言模型（VLM）引入跨视角几何定位能力，其定位需要从三个维度审视：VLA 范式、VLM 与 3D 基础模型集成范式、以及 VLM 自身的演进。

**相对于 VLA 范式**：现有的视觉-语言-动作（VLA）模型（Figure 1a）直接以多视角图像和语言指令为输入，通过 VLM 的通用推理能力输出轨迹规划。然而，这类方法受限于 VLM 本身缺乏显式的 3D 空间建模能力，导致在需要精确几何感知的任务（如风险目标定位、运动预测）上表现平庸。VGGDrive 并未抛弃 VLA 框架，而是通过冻结的 3D 基础模型作为“几何专家”，为 VLM 注入空间感知能力，从而在保持语言推理优势的同时大幅提升驾驶性能。

**相对于 3D-VLM 集成范式**：论文明确对比了两类现有集成方案（Figure 1b）：
- **VGGT-Dist**：通过知识蒸馏将 3D 特征对齐到 VLM 的表示空间。该方案仅进行浅层对齐，VLM 被动接收蒸馏信号，缺乏动态的跨模态交互。
- **VGGT-Add**：将 3D 特征与 2D 视觉特征简单相加后送入 LLM。该方案忽略了模态间的语义鸿沟，且未利用 LLM 的层级结构。

VGGDrive 的关键突破在于提出 **CVGE（Cross-view 3D Geometric Enabler）**，通过多头交叉注意力实现从“被动接收”到“主动挖掘”的跨模态深度融合，并利用层次化自适应注入机制解耦 LLM 的每一解码层，使几何信息在多个抽象层级发挥作用。消融实验（Table 6）强有力地证明了这一设计优势：CVGE 层次化注入（OURS）在 NAVSIM 上达到 PDMS 88.76，显著优于 VGGT-Add（86.10）、VGGT-Dist（86.68）以及 LLM 前直接融合方案 ID-5（86.80）。

**相对于基础 VLM**：VGGDrive 以 **Qwen2.5-VL-7B**（Bai et al., arXiv 2025）作为基础模型，但方法本身是模型无关的即插即用框架。其层级解耦设计可泛化至任何具有多层解码器结构的 VLM。实验表明，VGGDrive 在五个自动驾驶基准上一致提升基础 VLM 性能，尤其在需要几何感知的任务上提升幅度最大（如 NuInstruct MAP 从 6.15 提升至 37.49，+31.34 点）。

### 2. 方法谱系中的关键设计选择

VGGDrive 的三个核心组件各自代表了特定的设计谱系位置：

**3D 专家模型选择**：论文选择 **VGGT**（冻结）作为几何特征提取器，而非其他 3D 基础模型（如 DUSt3R）。消融实验（Table 8）证实 VGGT 的跨视角几何特征质量优于替代方案，这是性能提升的基础。VGGT 能够从多视角图像中生成几何一致的 3D 特征，恰好弥补 VLM 缺乏显式 3D 建模的短板。

**跨模态融合机制**：CVGE 采用多头交叉注意力（MHCA），以 2D 视觉特征为查询（Q）、3D 几何特征为键（K）和值（V），并显式编码相机内外参进行几何对齐。这与简单的特征拼接或相加形成鲜明对比——后者无法建模模态间的长程依赖关系。公式上体现为：

$$Q = MLP_i^{down}(V_i^{2d}), \quad K, V = MLP_i^{down}(\text{Re}(V^{3d}))$$

$$V_i^{3d} = MLP_i^{up}(MHCA_i^h(Q, K, V))$$

其中相机变换矩阵 $T_i^{img2lidar}$ 被编码到 K 和 V 中，确保几何对齐。

**层次化注入策略**：VGGDrive 解耦 LLM 的 n 层解码器，在每一层提取 2D 视觉表示 $V_i^{2d}$，通过 CVGE 得到几何增强的 $V_i^{3d}$，再通过残差连接更新隐藏状态：

$$x_i = X_i + X_i', \quad i = 1, ..., n$$

消融实验（Table 7）证明残差连接至关重要（移除导致性能下降），且单层注入即可大幅提升性能（PDMS 约 88），全层自适应注入达到最优。这表明几何信息在 LLM 的不同抽象层级均有价值，且残差连接保证了原始 VLM 的语言能力不被破坏。

### 3. 适用边界与局限

**任务适用性**：VGGDrive 在需要几何感知的任务上提升显著（跨视角风险感知 MAP +31.34、闭环规划 PDMS +2.72），但在纯语义描述任务上提升有限（OmniDrive 仅 +0.21）。这表明 3D 几何注入主要增强空间推理能力，对 VLM 原有的语言能力既无损害也无显著增益。在需要常识推理的复杂交互场景中，几何注入是否会干扰语义先验仍需进一步验证。

**计算开销**：CVGE 的层次化注入引入额外计算。Table 6 显示推理速度有所下降（具体数值需查看原文），这是精度提升的代价。论文通过设置 MLP 缩放因子 s=4 和注意力头数 h=8 在效率与性能间取得平衡（Table 9），但面向车载端侧部署的低延迟需求，仍需进一步优化。

**3D 专家的鲁棒性**：VGGT 作为冻结模型，其几何特征质量直接影响 VGGDrive 性能。在极端天气、照明条件或域外场景下，VGGT 的特征可靠性尚未经过验证，这构成了方法在开放环境中的潜在风险。

**训练数据依赖**：所有实验在相同训练数据和微调策略下进行，方法的跨数据集泛化能力（如从 nuScenes 到 Waymo）尚未被充分探索。

### 4. 开放问题

1. **效率优化**：如何进一步减少 CVGE 的计算开销，使其适用于低延迟的车载端侧部署？是否可以通过层选择策略（仅注入关键层）实现性能与效率的最佳平衡？

2. **鲁棒性边界**：在极端天气、照明条件或域外场景下，VGGT 的几何特征质量是否依然可靠？是否需要引入不确定性建模或自适应融合权重？

3. **通用性验证**：该框架能否作为通用插件与更多类型的 3D 基础模型（如 MASt3R、SpatialLM）或 VLM（如 LLaVA、InternVL）组合？能否扩展至机器人等具身智能任务？

4. **能力干扰**：跨视角几何定位的注入是否会削弱 VLM 的原有常识推理能力，尤其在需要语义先验的复杂交互场景中？如何量化并缓解这种潜在的能力干扰？

5. **端到端训练**：当前 VGGT 保持冻结，若将其部分解冻进行端到端微调，是否能进一步提升几何特征与 VLM 的适配度，同时避免灾难性遗忘？

## 原文 PDF

![[paperPDFs/CVPR_2026/VGGDrive_Empowering_Vision_Language_Models_with_Cross_View_Geometric_Grounding_for_Autonomous_Driving.pdf]]