---
title: "ECHO: Ego-Centric modeling of Human-Object interactions"
type: paper
paper_level: A
venue: arXiv
year: 2025
pdf_ref: paperPDFs/arxiv_2025/ECHO_Ego_Centric_modeling_of_Human_Object_interactions.pdf
aliases:
- ECHO
tags:
- arxiv_2025
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: 引入独立噪声调度的三变量扩散过程，实现人体运动（H）、物体轨迹（O）和接触序列（I）的联合建模与灵活条件化，使模型能处理任意模态的组合与部分观测。
primary_logic: 通过为三个模态分配独立去噪进度，模型可被联合训练于大规模人体运动数据集（AMASS）与小型人-物交互数据集（BEHAVE, OMOMO），习得强人体运动先验的同时捕获交互细节；在推理时，利用平滑修补和自监督引导，能从稀疏、间歇性输入中实时生成长期物理一致的交互序列。
claims:
- 在BEHAVE和OMOMO数据集上，ECHO在人体和物体所有指标上均优于基线（例如OMOMO上人体MPJPE 6.0 vs EgoAllo+H+O的6.6，物体E_v2v 26.5 vs 30.8）。
- 在AMASS人体运动生成上，ECHO取得最低MPJPE（7.4）和MPJVE（8.6），显著超过NoAMASS变体（MPJPE 43.1），证明联合训练策略有效。
- 消融实验证实，移除接触模态（仅H,O）导致性能大幅下降（MPJPE从6.8升到8.1），表明接触在连接人体与物体模态中的关键作用。
- 即使在90%手腕追踪丢失的情况下，性能仅轻微退化（MPJPE 7.7 vs 6.0），表明模型对间歇性传感器噪声具有高鲁棒性。
---

# ECHO: Ego-Centric modeling of Human-Object interactions

> [!tip] 核心洞察
> 通过为三个模态分配独立去噪进度，模型可被联合训练于大规模人体运动数据集（AMASS）与小型人-物交互数据集（BEHAVE, OMOMO），习得强人体运动先验的同时捕获交互细节；在推理时，利用平滑修补和自监督引导，能从稀疏、间歇性输入中实时生成长期物理一致的交互序列。

| 字段 | 内容 |
|------|------|
| 中文题名 | ECHO：以自我为中心的人与物体交互建模 |
| 英文题名 | ECHO: Ego-Centric modeling of Human-Object interactions |
| 会议/期刊 | arXiv 2025 |
| Links | [Project](https://www.projectaria.com/glasses/) · [paper](https://arxiv.org/abs/2508.21556) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/image_and_video_generation |
| Method | ECHO |
| Dataset | BEHAVE, OMOMO, AMASS |

> [!tip] 效果简介
> - BEHAVE 上，MPJPE (cm) 6.8±0.1 vs 7.6±0.1 (EgoAllo+H+O) (-0.8)；E_v2v (cm) 33.5±0.5 vs 39.1±1.1 (EgoAllo+H+O) (-5.6)。
> - OMOMO 上，MPJPE (cm) 6.0±0.1 vs 6.6±0.1 (EgoAllo+H+O) (-0.6)；E_v2v (cm) 26.5±1.1 vs 30.8±0.9 (EgoAllo+H+O) (-4.3)。
> - AMASS (human motion only) 上，MPJPE (cm) 7.4±0.1 vs 8.9±0.1 (EgoAllo+H+O) (-1.5)。

## 概述

从稀疏可穿戴传感器（头部与手腕追踪）中联合重建全身姿态、物体运动及接触动态，是一个高度欠约束的问题。现有方法缺乏统一的框架来建模人体、物体与接触这三种模态之间的相互依赖关系，导致交互重建中出现物体穿透、漂浮等物理不一致现象。

**ECHO** 是首个仅依赖头部与手腕三点追踪信号，即可联合恢复全身人-物交互（HOI）序列的统一框架。其核心方法是一种**三变量扩散过程**，为人体运动（$\mathcal{H}$）、物体轨迹（$\mathcal{O}$）和接触序列（$\mathcal{I}$）分配独立的噪声调度，从而实现对任意模态组合与部分观测的灵活条件化。这一设计使模型能够联合训练于大规模人体运动数据集（AMASS）与小型人-物交互数据集（BEHAVE、OMOMO），在习得强人体运动先验的同时捕获精细的交互细节。

在推理阶段，ECHO 结合**平滑修补**与**自监督引导**，从稀疏、间歇性的输入中实时生成长期物理一致的交互序列。实验表明，ECHO 在 BEHAVE 和 OMOMO 数据集上的人体与物体重建指标均优于基线方法（例如 OMOMO 上人体 MPJPE 降至 6.0 cm，物体顶点误差 $E_{v2v}$ 降至 26.5 cm），且在 90% 手腕追踪丢失的情况下性能仅轻微退化，展现出对传感器噪声的高鲁棒性。

## 背景与动机

### 问题背景：从稀疏可穿戴信号重建人-物交互

理解人类如何与周围物体交互是计算机视觉与具身智能的核心问题。近年来，以自我为中心（egocentric）的感知设备（如智能眼镜、头戴显示器）日益普及，它们能够持续捕获穿戴者的头部和手部运动轨迹。然而，从这些稀疏的三点追踪信号（头部 + 双手腕）中完整恢复全身姿态、物体运动以及人与物体的接触动态，仍然是一个极具挑战性的问题。

这一问题的难度源于其本质上的**高度欠约束性**：仅凭头部和手腕的空间位置信息，系统需要同时推断出全身22个关节的旋转、物体的6自由度刚体运动，以及人体表面与物体之间的精细接触关系。当手部追踪因遮挡或传感器噪声而间歇性丢失时，问题的欠约束程度进一步加剧。

### 现有方法的缺口

当前从自我中心信号重建人-物交互（HOI）的方法存在三个核心局限：

**第一，模态建模的割裂。** 现有工作通常将人体运动预测与物体运动预测视为两个独立或松耦合的任务。例如，**BoDiffusion+O** 将人体运动扩散模型扩展以同时预测物体姿态，但使用单一联合噪声调度，无法灵活处理不同模态之间的依赖关系；**EgoAllo+H+O** 则在逐帧规范化的框架下增加手部条件与物体预测，但缺乏对接触动态的显式建模。这些方法未能将人体、物体和接触三者作为一个相互依赖的整体进行统一建模。

**第二，接触信息的缺失。** 人与物体的接触是连接人体模态与物体模态的关键桥梁——正是接触约束决定了手部姿态如何影响物体运动，以及物体运动如何反过来约束人体姿态。然而，现有基线方法均未显式建模接触模态（如 Table 5 消融实验所示，移除接触模态后 MPJPE 从 6.8 升至 8.1），导致预测结果常出现物体穿透或漂浮等物理不一致现象。

**第三，数据利用的低效。** 大规模人体运动捕捉数据集（如 AMASS）包含丰富的人体运动先验，但缺乏物体交互标注；而专门的 HOI 数据集（如 BEHAVE、OMOMO）虽然包含交互标注，但规模有限且物体种类受限。现有方法通常仅在 HOI 数据集上训练，未能有效利用大规模人体运动数据来学习强先验。如 Table 2 所示，不使用 AMASS 训练的变体（NoAMASS）在人体运动生成上的 MPJPE 从 7.4 急剧恶化至 43.1，充分说明了这一缺口的严重性。

### 本文动机与核心思路

针对上述缺口，本文提出 **ECHO（Ego-Centric modeling of Human-Object interactions）**，这是首个从稀疏可穿戴传感器信号中**联合**重建全身人-物交互序列的统一框架。ECHO 的核心设计围绕三个关键洞察展开：

1. **三变量扩散与独立噪声调度**：通过为人体运动（$\mathcal{H}$）、物体轨迹（$\mathcal{O}$）和接触序列（$\mathcal{I}$）分配独立的去噪进度，模型可以在一个统一的扩散过程中灵活处理任意模态的组合与部分观测，真正实现三者的联合建模。

2. **接触作为桥梁模态**：引入基于 SMPL-X 表面点与物体距离的连续接触表示，使接触成为连接人体与物体的显式信息通道，显著提升交互重建的物理一致性。

3. **联合训练策略**：通过可学习的 token 标志无物体场景，ECHO 能够在大规模人体运动数据集（AMASS）与小型 HOI 数据集（BEHAVE、OMOMO）上联合训练，在习得强人体运动先验的同时捕获精细的交互细节。

在推理阶段，ECHO 通过**平滑修补**（smooth inpainting）和**自监督引导**（reconstruction guidance）技术，能够从稀疏、间歇性的传感器输入中实时生成长期物理一致的交互序列。实验表明，即使在 90% 手腕追踪丢失的极端情况下，ECHO 的性能仅轻微退化（MPJPE 7.7 vs 6.0），展现出对传感器噪声的高度鲁棒性。

## 核心创新

ECHO 的核心创新在于将人-物交互（HOI）重建从一个多阶段、脆弱的过程重构为一个**统一的三变量扩散生成问题**。针对从稀疏可穿戴传感器（仅头部与手腕追踪）信号中联合恢复全身姿态、物体运动及接触这一高度欠约束的瓶颈，ECHO 通过以下关键设计实现了突破。

### 1. 三变量扩散与独立噪声调度

传统方法（如 **BoDiffusion+O**）采用单一或串联的扩散过程，所有模态共享同一噪声调度，无法灵活处理部分观测与模态缺失。ECHO 引入了**三变量扩散过程**，为人体运动 $\mathcal{H}$、物体轨迹 $\mathcal{O}$ 和接触序列 $\mathcal{I}$ 分别分配独立的去噪时间步 $(\tau_{\mathcal{H}}, \tau_{\mathcal{O}}, \tau_{\mathcal{I}})$（Fig. 3, Eq. 9）。这一设计使模型能够：

- 在训练时，从任意噪声水平的模态组合中学习恢复干净序列，天然支持**灵活条件化**——推理时可将任意已知模态（或部分观测）作为条件，对其余模态进行修补生成（Table 4）。
- 在联合训练于大规模人体运动数据（AMASS）与小规模 HOI 数据（BEHAVE, OMOMO）时，通过可学习 token 标志无物体场景，使人体运动先验与交互细节的学习互不干扰。

### 2. 接触模态作为显式桥梁

此前方法（如 **EgoAllo+H+O**）仅预测人体与物体姿态，缺乏对接触动态的显式建模。ECHO 将**接触提升为独立连续模态**：基于 SMPL-X 表面采样点 $P_c$ 与物体网格 $V_{\mathcal{O}}$ 的最短距离，经 sigmoid 映射生成 $[0,1]$ 内的接触值（Eq. 3）：

$$c_{\mathcal{T}}^{\mathrm{HOI}} = \{ \sigma\left(\alpha\cdot\left(\tau_c - d(p, V_{\mathcal{O}})\right)\right) \mid p \in P_c \subset V_{\mathcal{H}} \}$$

这一设计使接触成为连接人体与物体模态的**因果桥梁**。消融实验证实，移除接触模态（仅保留 $\mathcal{H}, \mathcal{O}$）导致人体 MPJPE 从 6.8 升至 8.1，物体预测亦显著恶化（Table 5），表明接触信息对于协调两种模态的生成至关重要。

### 3. 推理时的平滑修补与自监督引导

长序列推理中，标准滑动窗口忽略历史上下文，简单修补则直接丢弃重叠区域的新预测。ECHO 提出**平滑修补（smooth inpainting）**策略：在每个扩散步，将当前窗口预测与上一窗口结果按权重 $\alpha=0.4$ 混合（Eq. 21, Fig. 4）：

$$\hat{\mathcal{H}}_{\mathcal{W}}^{\tau_{\mathcal{H}}} := \alpha\hat{\mathcal{H}}_{\mathcal{W}}^{\tau_{\mathcal{H}}} + (1-\alpha)\hat{\mathcal{H}}_{\mathcal{W}-1}$$

同时，**重构引导（reconstruction guidance）**在反向扩散过程中依据接触一致性损失梯度修正预测（Eq. 20），强制生成的人-物网格与预测接触向量对齐，并惩罚脚部滑动。消融表明，取消引导主要损害物体预测质量，移除平滑修补则破坏时间一致性（Table 5）。

### 4. 联合训练策略

ECHO 将 AMASS（纯人体运动）与 BEHAVE、OMOMO（人-物交互）联合训练，通过可学习 token 区分有无物体的场景。这一策略使模型从大规模运动数据中习得强人体运动先验——在 AMASS 人体运动生成上，ECHO 取得 MPJPE 7.4，显著优于不使用 AMASS 的变体（NoAMASS MPJPE 43.1, Table 2），证明联合训练是解决 HOI 数据稀缺问题的有效路径。

**创新总结**：ECHO 通过独立噪声调度的三变量扩散、接触模态的显式桥梁作用、平滑修补与引导推理，以及联合训练策略，将稀疏可穿戴信号下的 HOI 重建统一为灵活、鲁棒的生成框架，在 BEHAVE 和 OMOMO 上全面超越基线（Table 1），并在 90% 手腕追踪丢失时仍保持稳定性能（Table 3）。

## 整体框架

ECHO 是一个以自我为中心的人-物交互（HOI）重建框架，其核心目标是仅从头戴式设备与腕部追踪器提供的稀疏 3 点信号（头部、左手腕、右手腕）中，联合恢复全身人体运动、物体运动以及接触动态。该框架围绕一个统一的 Transformer 扩散模型构建，将人体运动 $\mathcal{H}$、物体运动 $\mathcal{O}$ 和接触序列 $\mathcal{I}$ 作为三个独立模态进行联合建模。

### 输入与条件提取

框架的输入由两部分组成：自我中心条件与物体先验信息。

**自我中心条件提取器**从每帧的头部和腕部追踪数据中提取头部相对变换、正则化后的头部朝向以及头部到地面的距离，构成逐帧的自我中心条件序列 $\mathcal{E}$。这一步骤将所有空间信息统一到以头部为中心的正则坐标系下，消除了全局坐标漂移对模型学习的干扰（Fig. 2）。

**物体特征提取器**则利用 PointNext 网络从物体的正则网格中提取几何特征，并与物体的类别独热编码拼接，形成全局物体条件 $\mathcal{C}_{\mathcal{O}}$。值得注意的是，物体类别是框架所需的唯一高层语义输入，无需预先知道物体的具体 6D 姿态。

### 核心推理引擎：三变量扩散 Transformer

框架的核心是一个基于 Diffusion Transformer（DiT）架构的去噪网络，即三变量 DiT 去噪器。该网络接收三类输入 token：

1. **带噪模态 token**：人体运动 $\mathcal{H}^{T_{\mathcal{H}}}$、物体运动 $\mathcal{O}^{T_{\mathcal{O}}}$ 和接触序列 $\mathcal{I}^{T_{\mathcal{I}}}$，各自处于不同的扩散时间步 $T_{\mathcal{H}}, T_{\mathcal{O}}, T_{\mathcal{I}}$。
2. **去噪步编码**：三个模态各自的时间步嵌入，告知网络每个模态当前的噪声水平。
3. **条件 token**：自我中心条件 $\mathcal{E}$ 与物体条件 $\mathcal{C}_{\mathcal{O}}$。

网络通过最小化预测的干净序列与真实干净序列之间的 L2 误差进行训练，其训练目标为：

$$\mathbb{E}_{p}\mathbb{E}_{\mathcal{T}}\mathbb{E}_{q}\|\mathrm{ECHO}_{\psi}(\mathcal{H}^{T_{\#}},\mathcal{O}^{T_{\mathcal{O}}},\mathcal{T}^{T_{\mathcal{I}}}; \mathcal{T}_{\mathcal{H}},\mathcal{T}_{\mathcal{O}},\mathcal{T}_{\mathbb{Z}}; \mathcal{C}_{\mathcal{O}},\mathcal{E})-(\mathcal{H}^{0},\mathcal{O}^{0},\mathcal{T}^{0})\|_{2}$$

这一设计的核心因果机制在于**独立噪声调度**：三个模态可以在训练中被随机赋予完全不同的去噪进度。这使得模型能够灵活处理任意模态的组合——例如，在部分观测场景下，已知模态可以保持干净（$T=0$），而未知模态从纯噪声开始去噪。同时，该设计允许在 AMASS 等大规模纯人体运动数据上进行联合训练（此时物体与接触模态被置为纯噪声并配合可学习的“无物体”标志 token），从而让模型习得强健的人体运动先验，再在小型 HOI 数据集上精调交互细节。

### 接触模态的构建

接触模态 $\mathcal{I}$ 是 ECHO 连接人体与物体的关键桥梁。对于每帧，框架从 SMPL-X 人体网格表面采样一组点 $P_c$，计算每个采样点到物体网格 $V_{\mathcal{O}}$ 的最近距离，并通过带参数的 sigmoid 函数映射为 $[0,1]$ 范围内的连续接触值：

$$c_{\mathcal{T}}^{\mathrm{HOI}} = \{ \sigma\left(\alpha\cdot\left(\tau_c - d(p, V_{\mathcal{O}})\right)\right) \mid p \in P_c \subset V_{\mathcal{H}} \}$$

这一连续表示避免了硬性二值接触带来的梯度不稳定问题，使得接触信息可以作为可微分的模态融入扩散过程。

### 推理阶段的时序缝合与引导

在长序列推理时，框架以滑动窗口方式运行，并通过两个关键模块保证输出质量：

**平滑修补模块**在每个扩散步中，将当前窗口与上一窗口的重叠区域进行加权混合（权重 $\alpha=0.4$），确保相邻窗口之间无缝过渡：

$$\hat{\mathcal{H}}_{\mathcal{W}}^{\mathcal{T}_{\mathcal{H}}} := \alpha\hat{\mathcal{H}}_{\mathcal{W}}^{\mathcal{T}_{\mathcal{H}}} + (1-\alpha)\hat{\mathcal{H}}_{\mathcal{W}-1}$$

**引导模块**在反向扩散过程中，利用分类器引导策略，对当前预测施加接触一致性约束——要求预测的人体-物体网格间距离与预测的接触向量一致，同时惩罚脚部滑动。梯度修正的更新形式为：

$$(\hat{\mathcal{H}},\hat{\mathcal{O}},\hat{\mathcal{I}}) := (\hat{\mathcal{H}},\hat{\mathcal{O}},\hat{\mathcal{I}}) - \lambda \nabla_{\mathcal{H}\mathcal{O}\mathcal{I}} \tau(\mathcal{F})$$

### 输出

框架最终输出完整的全身人体运动序列（以 SMPL-X 姿态参数表示）、物体在头部中心坐标系下的 SE(3) 轨迹，以及逐帧的接触序列。这三者共同构成物理一致的长期人-物交互重建结果。

### 补充图表

![[assets/figures/papers/paper_list_l1678_ECHO_Ego_Centric_modeling_of_Human_Object_interactions/figures/003_Figure_3.jpg]]
*Figure 3: ECHO overview. ECHO requires just head and hand tracking and and object class, to predict Human, Object, and Interaction. The input tokens are composed of condition, and of either observed modality, or noise for*

![[assets/figures/papers/paper_list_l1678_ECHO_Ego_Centric_modeling_of_Human_Object_interactions/figures/002_Figure_2.jpg]]
*Figure 2: Representation. ECHO operates in a perframe head-centric coordinate system*

![[assets/figures/papers/paper_list_l1678_ECHO_Ego_Centric_modeling_of_Human_Object_interactions/figures/001_Figure_1.jpg]]
*Figure 1: ECHO. Inferring complex interactions from sparse wearable signals is challenging. ECHO is the first method to jointly recover full-body Human-Object Interaction sequences (top) solely from sparse 3-point tracking. Our flexible framework supports various inference modes (bottom), leveraging partial or intermittent observations (shown in red) of human pose, object trajectory, or contact dynamics*

## 核心模块与公式推导

ECHO 的核心是一个基于 Diffusion Transformer (DiT) 的三变量扩散模型，其设计围绕一个中心洞察：人体运动（H）、物体轨迹（O）和接触序列（I）三者之间存在强相互依赖，但各自的不确定性结构和观测条件不同。为此，模型为三个模态分配独立的噪声调度，使它们可以在同一框架内被联合去噪，同时允许任意模态的组合条件化与部分观测。

### 表示空间定义

所有模态均在以头部为中心的逐帧坐标系中表示（Fig. 2），以消除全局运动歧义。对于长度为 N 的序列：

- **人体运动序列**：$\mathcal{H} = \{ \pmb{\theta}_{\mathcal{H}}^{1..N} \}$，为 SMPL-X 身体姿态参数序列。
- **物体轨迹序列**：$\mathcal{O} = \{ T_{\mathcal{O}}^{1..N} \}$，为物体在头部中心坐标系下的 SE(3) 位姿序列。
- **接触序列**：$\mathcal{I} = \{ c_{\mathcal{T}}^{1\dots N} \}$，为每帧的连续接触向量。

### 接触模态建模（关键创新）

接触是连接人体与物体模态的核心桥梁。ECHO 将接触建模为连续模态，包含人-物接触和人-地接触两部分。对于人-物接触，首先从 SMPL-X 人体网格表面采样点集 $P_c \subset V_{\mathcal{H}}$，计算每点到物体网格 $V_{\mathcal{O}}$ 的最近距离 $d(p, V_{\mathcal{O}})$，然后通过带温度参数 $\alpha$ 和阈值 $\tau_c$ 的 sigmoid 函数映射为 [0,1] 内的连续接触值：

$$c_{\mathcal{T}}^{\mathrm{HOI}} = \{ \sigma\left(\alpha\cdot\left(\tau_c - d(p, V_{\mathcal{O}})\right)\right) \mid p \in P_c \subset V_{\mathcal{H}} \}$$

这一连续化处理使接触信息适配扩散框架，避免了二值接触带来的梯度不稳定性。

### 三变量扩散与独立噪声调度

ECHO 的核心机制是对三个模态分别施加独立的前向扩散过程。设 $\mathcal{T}_{\mathcal{H}}, \mathcal{T}_{\mathcal{O}}, \mathcal{T}_{\mathbb{Z}}$ 分别为人体、物体和接触模态的扩散时间步，每个时间步从均匀分布 $\mathcal{U}\{0,\ldots,T\}$ 中独立采样。这种设计允许模型在训练时看到任意模态组合处于不同噪声水平的状态，从而学会从部分观测中推断完整交互。

去噪网络 $\mathrm{ECHO}_{\psi}$ 接收带噪模态序列、各自的时间步以及条件信息（自我中心条件 $\mathcal{E}$、物体类别条件 $\mathcal{C}_{\mathcal{O}}$），预测原始干净序列。训练目标为最小化期望 L2 误差：

$$\mathbb{E}_{p}\mathbb{E}_{\mathcal{T}}\mathbb{E}_{q}\|\mathrm{ECHO}_{\psi}(\mathcal{H}^{T_{\#}},\mathcal{O}^{T_{\mathcal{O}}},\mathcal{T}^{T_{\mathcal{I}}}; \mathcal{T}_{\mathcal{H}},\mathcal{T}_{\mathcal{O}},\mathcal{T}_{\mathbb{Z}}; \mathcal{C}_{\mathcal{O}},\mathcal{E}) - (\mathcal{H}^{0},\mathcal{O}^{0},\mathcal{T}^{0})\|_{2}$$

其中 $\mathbb{E}_{\mathcal{T}} \equiv \mathbb{E}_{(\mathcal{T}_{\mathcal{H}}, \mathcal{T}_{\mathcal{O}}, \mathcal{T}_{\mathbb{Z}}) \sim \mathcal{U}\{0,\ldots,T\}^{N\times 3}}$ 表示对三个模态时间步的联合期望。

### 联合训练策略

为习得强人体运动先验，ECHO 在 AMASS（大规模人体运动数据集）与 BEHAVE、OMOMO（小规模人-物交互数据集）上联合训练。对于无物体的 AMASS 序列，模型通过可学习的 token 标志无物体场景，使去噪网络能够在纯人体运动与交互场景之间平滑切换。这一策略是 ECHO 在人体运动生成指标上显著超越未使用 AMASS 变体的关键原因（AMASS 上 MPJPE 7.4 vs NoAMASS 43.1，Table 2）。

### 推理引导模块

在推理阶段，ECHO 采用分类器引导确保预测结果的物理一致性。引导损失 $\mathcal{F}$ 强制预测的人体-物体网格与预测的接触向量对齐，同时惩罚脚部滑动。在每个反向扩散步骤中，使用梯度修正当前预测：

$$(\hat{\mathcal{H}},\hat{\mathcal{O}},\hat{\mathcal{I}}) := (\hat{\mathcal{H}},\hat{\mathcal{O}},\hat{\mathcal{I}}) - \lambda \nabla_{\mathcal{H}\mathcal{O}\mathcal{I}} \tau(\mathcal{F})$$

其中 $\lambda$ 为引导强度，$\tau(\mathcal{F})$ 为基于接触一致性和脚部接触的损失函数。

### 平滑修补模块

长序列推理时，ECHO 采用平滑修补策略保证窗口间的时间连续性。对于相邻窗口的重叠区域，在每一步扩散过程中将当前窗口预测与上一窗口预测进行加权混合：

$$\hat{\mathcal{H}}_{\mathcal{W}}^{\mathcal{T}_{\mathcal{H}}} := \alpha\hat{\mathcal{H}}_{\mathcal{W}}^{\mathcal{T}_{\mathcal{H}}} + (1-\alpha)\hat{\mathcal{H}}_{\mathcal{W}-1}$$

其中 $\alpha=0.4$ 为混合权重。相比标准逐窗口推理（忽略历史上下文）和简单修补（丢弃新预测的重叠部分），平滑修补在每一扩散步都进行混合，确保无缝过渡（Fig. 4）。

![[assets/figures/papers/paper_list_l1678_ECHO_Ego_Centric_modeling_of_Human_Object_interactions/figures/004_Figure_4.jpg]]
*Figure 4: Comparison of inference strategies. Standard per-window inference (left) ignores the context of the past predictions. Inpainting (middle) uses past prediction as condition but drops new predictions for the overlapping region. Our smooth inpainting (right) blends past and current predictions in the overlapping region on every diffusion step, ensuring seamless transitions*

### 条件提取模块

ECHO 的条件输入由两部分组成：
- **自我中心条件提取器**：从头部和手腕追踪数据提取每帧的头部相对变换、正则化朝向和头-地距离，构成条件序列 $\mathcal{E}$。
- **物体特征提取器**：使用 PointNext 从物体正则网格提取几何特征，与类别独热编码拼接为全局物体条件 $\mathcal{C}_{\mathcal{O}}$。

这些条件与带噪模态序列一同送入 DiT 骨干网络，网络使用旋转位置嵌入捕获时序依赖。

## 实验与分析

### 主实验结果

ECHO在BEHAVE和OMOMO两个标准人-物交互基准上，对人体和物体的联合重建质量均优于现有基线。Table 1报告了核心指标对比：

- **人体重建**：在BEHAVE上，ECHO取得MPJPE 6.8 cm，优于**EgoAllo+H+O**的7.6 cm（相对提升约10.5%）；在OMOMO上，MPJPE为6.0 cm，同样优于EgoAllo+H+O的6.6 cm。这表明三变量扩散与接触模态的引入有效提升了从稀疏自我中心信号中恢复全身姿态的精度。
- **物体重建**：ECHO在物体顶点误差（$E_{v2v}$）上优势更为显著——BEHAVE上33.5 cm vs 39.1 cm（降低5.6 cm），OMOMO上26.5 cm vs 30.8 cm（降低4.3 cm）。物体姿态预测的改善直接受益于接触模态在人体与物体之间建立的显式几何关联。
- **人体运动生成质量**：在AMASS纯人体运动数据集上（Table 2），ECHO取得MPJPE 7.4 cm、MPJVE 8.6 cm，均优于EgoAllo+H+O（8.9 cm / 10.1 cm）和**BoDiffusion+O**。这证明联合训练策略使模型从大规模运动数据中习得了强人体运动先验，同时未损害交互场景下的性能。

![[assets/figures/papers/paper_list_l1678_ECHO_Ego_Centric_modeling_of_Human_Object_interactions/figures/008_Table_2.jpg]]
*Table 2: Quality of motion generation. ECHO outperforms the baselines on the AMASS dataset, demonstrating that our joint HOI formulation effectively learns a strong human motion prior. The significant drop in performance for NoAMASS confirms the importance of training on large-scale motion data*

所有方法均使用相同的联合数据集（AMASS + BEHAVE + OMOMO）训练，且采用一致的头部中心化坐标系和网络架构扩展，对比具有公平性。实验结果报告了多轮平均与方差。

### 消融实验

Table 5在BEHAVE数据集上系统评估了ECHO各组件的贡献：

- **接触模态的关键作用**：移除接触模态（仅保留H和O）导致人体MPJPE从6.8 cm升至8.1 cm，物体$E_{v2v}$也明显恶化。接触向量作为人体与物体之间的几何桥梁，为扩散模型提供了不可或缺的互依赖约束。
- **AMASS联合训练**：NoAMASS变体（仅用BEHAVE和OMOMO训练）使人体运动质量大幅下降——AMASS上MPJPE从7.4 cm飙升至43.1 cm，证实大规模运动数据对于学习人体运动先验至关重要。
- **推理引导**：取消重构引导（NoGuide）主要损害BEHAVE上的物体预测质量，表明基于接触一致性的梯度修正在保障物理合理性方面发挥实质作用。
- **平滑修补**：移除平滑混合（Inpaint w/o smooth）损害了长序列的时间一致性，验证了在相邻窗口重叠区域进行加权融合的必要性。

补充实验（Table S2）进一步揭示，将接触信息作为额外条件输入时，性能提升最为显著，确认接触在人-物交互建模中扮演核心角色。

![[assets/figures/papers/paper_list_l1678_ECHO_Ego_Centric_modeling_of_Human_Object_interactions/figures/013_Table.jpg]]
*Table: S2: Evaluation of ECHO with additional input modalities. We observe that providing ECHO with contact information provides the biggest quality improvement among all three modalities*

### 鲁棒性与稀疏输入

ECHO对传感器噪声和间歇性丢失表现出高鲁棒性。Table 3显示，即使随机丢弃90%的手腕追踪数据，人体MPJPE仅从6.0 cm轻微退化至7.7 cm，物体$E_{v2v}$从26.5 cm升至28.9 cm。这一特性源于三变量扩散的灵活条件化能力——当某一模态的部分观测缺失时，模型可借助其他模态的上下文进行合理推断。

Table 4展示了ECHO利用稀疏追踪信息的灵活性：提供额外的部分人体关节轨迹或物体轨迹作为条件，可进一步改善对应模态的预测精度。这验证了框架对任意模态组合与部分观测的适应能力。

### 定性分析

Fig. 5展示了ECHO与基线方法在多样化交互场景下的定性对比。ECHO能准确重建人体与物体的接触动态，而竞争方法常出现物体穿透或漂浮等伪影。Fig. 6展示了模型在Aria Digital Twin数据集上的泛化能力，表明ECHO可适应训练集之外的物体类别和运动模式。

### 失败模式与局限

尽管整体性能优越，ECHO仍存在以下局限：

1. **物体先验依赖**：模型需要已知物体的正则网格和类别标签作为输入，在物体未知或网格不可获取的场景中不可用。
2. **单物体假设**：当前设计针对单物体交互，无法直接处理多物体同时交互的场景。
3. **交互多样性受限**：训练数据（BEHAVE、OMOMO）的物体种类和交互类型有限，对极端或新型交互的泛化可能受限。
4. **手部细节不足**：模型未显式建模手-物细节接触，精细手部姿态可能不够准确——这从Table 1中手部相关指标的改善幅度相对较小可间接印证。

需要手动验证的是：论文中未提供在完全未知物体类别上的零样本泛化实验，上述第1点局限的严重程度需结合实际部署场景评估。

### 补充图表

![[assets/figures/papers/paper_list_l1678_ECHO_Ego_Centric_modeling_of_Human_Object_interactions/figures/007_Table_1.jpg]]
*Table 1: Comparison with baselines on BEHAVE and OMOMO. ECHO demonstrates better performance for human-object interaction modeling and competitive motion modeling quality*

![[assets/figures/papers/paper_list_l1678_ECHO_Ego_Centric_modeling_of_Human_Object_interactions/figures/011_Table_5.jpg]]
*Table 5: Ablation study on BEHAVE. Evaluating the impact of ECHO components proves the usefulness of guidance, smooth inpainting, usage of three modalities, and training with AMASS data*

![[assets/figures/papers/paper_list_l1678_ECHO_Ego_Centric_modeling_of_Human_Object_interactions/figures/009_Table_3.jpg]]
*Table 3: Evaluation of ECHO with noise simulation. We demonstrate the robustness of ECHO to intermittent hand tracking by randomly dropping a percentage of the input. The model maintains stable performance even with significant missing hand tracking data, confirming its resilience to sensor noise*

![[assets/figures/papers/paper_list_l1678_ECHO_Ego_Centric_modeling_of_Human_Object_interactions/figures/010_Table_4.jpg]]
*Table 4: Evaluation of ECHO with sparse tracking. We demonstrate the versatility of ECHO by providing additional sparse tracking information alongside egocentric conditioning. Providing partial information for one modality (Human or Object) significantly improves its reconstruction quality and helps regularize the other*

![[assets/figures/papers/paper_list_l1678_ECHO_Ego_Centric_modeling_of_Human_Object_interactions/figures/005_Figure_5.jpg]]
*Figure 5: Qualitative results of ECHO. Our method accurately reconstructs humanobject interactions across diverse scenarios. In contrast, competing methods often fail to capture correct contact dynamics, leading to artifacts such as object penetration or floating. For dynamic visualizations, please refer to the supplementary video*

![[assets/figures/papers/paper_list_l1678_ECHO_Ego_Centric_modeling_of_Human_Object_interactions/figures/006_Figure_6.jpg]]
*Figure 6: \ Fig. 6: Qualitative results of ECHO. We demonstrate generalization to novel motion and objects from the Aria Digital Twin [65]; RGB is included for reference*

## 方法谱系与知识库定位

### 1. 核心问题定位：从稀疏穿戴信号重建全身人-物交互

ECHO 针对的是从极度稀疏的自我中心传感器信号（仅头部与手腕的 3D 追踪）中联合重建全身人体姿态、物体运动以及接触动态这一高度欠约束问题。现有方法面临两个关键瓶颈：第一，缺乏统一的框架来建模人体、物体和接触三种模态之间的相互依赖关系；第二，人-物交互（HOI）数据集的规模远小于纯人体运动数据集，导致模型难以习得强健的人体运动先验。ECHO 通过引入**三变量扩散过程**与**独立噪声调度**，将三种模态纳入统一的生成式框架，同时利用大规模人体运动数据（AMASS）进行联合训练，从根本上解决了上述瓶颈。

### 2. 与基线方法的关系与改进

ECHO 在实验部分与两个直接基线进行了系统对比，这些基线代表了从现有方法向人-物交互联合建模扩展的不同路径。

**BoDiffusion+O** 是将人体运动扩散模型 BoDiffusion 扩展为同时预测物体姿态的基线，采用单一联合噪声调度对所有模态施加相同的噪声水平。这种设计隐含假设人体与物体的运动复杂度相当，忽略了两种模态在数据分布和可预测性上的本质差异。ECHO 的独立调度策略直接克服了这一局限，允许模型根据各模态的观测完整度灵活调整去噪进度。

**EgoAllo+H+O** 是在自我中心姿态估计方法 EgoAllo 的基础上增加手部条件与物体预测分支的基线，使用逐帧规范化处理。该基线的核心局限在于缺乏显式的接触建模——它仅预测人体与物体的独立姿态，而未引入两者之间的物理交互约束。ECHO 通过引入连续接触模态（基于 SMPL-X 表面采样点与物体最近距离的 sigmoid 映射），将接触作为连接人体与物体的“桥梁”，从而在物理一致性上获得显著提升。

在定量对比中，ECHO 在所有人体和物体指标上均优于上述基线。以 OMOMO 数据集为例，ECHO 的人体 MPJPE 为 6.0 cm（EgoAllo+H+O 为 6.6 cm），物体顶点误差 E_v2v 为 26.5 cm（EgoAllo+H+O 为 30.8 cm），验证了接触模态和三变量扩散设计的有效性（Table 1）。定性结果进一步显示，基线方法常出现物体穿透或漂浮等接触失败案例，而 ECHO 能准确重建交互动态（Fig. 5）。

### 3. 方法谱系中的位置：扩散生成与多模态条件化

ECHO 在方法谱系中处于**多模态扩散生成模型**与**自我中心感知**的交叉地带。其技术架构以 Diffusion Transformer（DiT）为骨干网络，结合旋转位置嵌入，属于基于 Transformer 的扩散生成范式。与标准扩散模型的关键区别在于三变量独立调度机制——这是对经典 DDPM 框架在条件化灵活性维度的重要扩展。

在训练策略上，ECHO 采用了**大规模无交互数据与小型交互数据联合训练**的方案。具体而言，模型在 AMASS（纯人体运动）与 BEHAVE、OMOMO（人-物交互）上联合训练，通过可学习的 token 标志区分无物体场景。这一策略使模型能从 AMASS 中习得强健的人体运动先验，同时从 HOI 数据集中捕获精细的交互模式。消融实验证实，移除 AMASS 训练（NoAMASS 变体）导致人体 MPJPE 从 7.4 cm 急剧上升至 43.1 cm（Table 2），充分验证了联合训练策略的关键作用。

在推理阶段，ECHO 引入了两项重要创新：**平滑修补**与**重构引导**。平滑修补通过在相邻窗口重叠区域进行加权混合（权重 α=0.4），解决了标准滑动窗口推理中的时间不连续问题（Fig. 4）。重构引导则利用接触一致性损失（人-物接触与脚-地接触）的梯度修正预测结果，强制物理合理性。消融实验表明，移除引导主要损害物体预测质量，而移除平滑修补则影响时间一致性（Table 5）。

### 4. 适用边界与局限

ECHO 的设计存在以下明确边界：

- **物体先验依赖**：模型要求已知物体的正则网格和类别标签作为输入。在物体未知或网格不可获取的场景中，ECHO 无法直接应用。这限制了其在开放世界环境中的泛化能力。
- **单物体交互限制**：当前框架针对单个物体交互设计，无法直接处理多物体同时交互的场景（如双手分别操作不同物体）。
- **训练数据覆盖有限**：BEHAVE 和 OMOMO 数据集的物体种类和交互类型有限，模型对极端或新型交互（如非刚性物体、复杂工具使用）的泛化可能受限。
- **手部细节不足**：模型未显式建模手-物细节接触，精细手部姿态（如手指的精确抓取配置）可能不够准确。这源于输入仅为手腕追踪，缺乏手指级别的观测信号。

### 5. 开放问题与未来方向

ECHO 的工作为以下开放问题奠定了基础：

- **动态环境约束融合**：如何将来自动态环境的物理约束（如场景几何、障碍物）纳入生成过程，以实现长期一致的运动生成？当前模型仅依赖接触一致性引导，未来可探索与场景重建方法的深度耦合。
- **细粒度手指交互**：如何引入细粒度手指追踪以支持灵巧的小物体交互？这需要解决手指运动的高维性与稀疏观测之间的矛盾，可能需要在接触模态中增加手部接触的专门表示。
- **视觉条件化扩展**：如何将框架扩展至基于 RGB 的自我中心 HOI 数据集，实现视觉条件化的交互重建？这涉及将图像特征作为额外条件注入扩散过程，同时处理视觉观测中的遮挡与模糊问题。
- **多物体与多智能体交互**：将三变量框架扩展至更多模态（多物体、多人交互）是自然的延伸方向，但独立调度策略的复杂度将随模态数量线性增长，需要更高效的调度机制。

### 6. 知识库定位总结

ECHO 在知识库中的定位可概括为：**首个统一建模人体-物体-接触三模态的自我中心人-物交互重建框架**。其核心贡献在于三变量扩散的独立调度机制，使得模型能灵活处理任意模态的组合与部分观测，同时通过联合训练策略弥合大规模运动数据与小型交互数据之间的鸿沟。该方法在稀疏、间歇性传感器输入下展现出高鲁棒性（即使在 90% 手腕追踪丢失的情况下，MPJPE 仅从 6.0 cm 退化至 7.7 cm，Table 3），为可穿戴设备上的实时交互理解提供了可行的技术路径。

## 原文 PDF

![[paperPDFs/arxiv_2025/ECHO_Ego_Centric_modeling_of_Human_Object_interactions.pdf]]
