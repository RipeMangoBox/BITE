---
title: "Towards Storytelling Animations: Joint Synthesis of Human and Camera Motions"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/Towards_Storytelling_Animations_Joint_Synthesis_of_Human_and_Camera_Motions.pdf
project_link: null
code_link: null
aliases:
- JCCMDM
- TSAJSHCM
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/image_and_video_generation
- topic/generative_models_diffusion
- topic/generative_models_diffusion/diffusion_image_video
core_operator: 将角色与相机视为独立实体，在扩散模型中显式建模它们之间的成对交互（角色-角色、角色-相机），从而联合生成协调的角色与相机运动。
primary_logic: 利用Toric空间表示相机运动，构建双向交互模块动态调整实体嵌入，捕捉角色与相机之间的空间与运动依赖关系，实现协同优化。
claims:
- 首次研究联合角色-相机运动生成，提出统一框架。
- 模型在角色运动FID指标上显著优于最强基线ComMDM（0.113 vs 0.156）。
- 模型在相机运动SeqFID指标上显著优于基线DC3D（0.256 vs 0.417）。
- 消融实验证实交互模块对角色和相机运动质量及角色-相机协调性至关重要。
---

# Towards Storytelling Animations: Joint Synthesis of Human and Camera Motions

> [!tip] 核心洞察
> 利用Toric空间表示相机运动，构建双向交互模块动态调整实体嵌入，捕捉角色与相机之间的空间与运动依赖关系，实现协同优化。

| 字段 | 内容 |
|------|------|
| 中文题名 | 走向叙事动画：人物与相机运动的联合合成 |
| 英文题名 | Towards Storytelling Animations: Joint Synthesis of Human and Camera Motions |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://openaccess.thecvf.com/content/CVPR2026/papers/Cheng_Towards_Storytelling_Animations_Joint_Synthesis_of_Human_and_Camera_Motions_CVPR_2026_paper.pdf) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/image_and_video_generation #topic/generative_models_diffusion #topic/generative_models_diffusion/diffusion_image_video |
| Method | Joint Character-Camera Motion Diffusion Model |
| Dataset | Our Dataset |

> [!tip] 效果简介
> - Our Dataset (Character Motion) 上，FID↓ 0.113 vs 0.156 (ComMDM) (-0.043)；Coverage↑ 0.264 vs 0.160 (ComMDM) (+0.104)。
> - Our Dataset (Camera Motion) 上，SeqFID↓ 0.256 vs 0.417 (DC3D) (-0.161)；Density↑ 1.937 vs 0.538 (CDM) (+1.399)。

## 概要

### 问题背景

叙事动画创作要求同时协调角色表演与相机运镜，以传达连贯的视觉故事。然而，现有方法将角色运动生成与相机运动生成视为两个独立任务分别处理——角色运动由**ComMDM**等扩散模型生成，相机运动由**DC3D**（Wang et al., CVPR 2024）或**CDM**（Jiang et al., CGF 2024）等方法单独规划。这种分离式流程导致生成的角色动作与相机视角之间缺乏内在协调，难以保证叙事连贯性与视觉一致性。

### 核心瓶颈

**现有方法无法在生成过程中显式建模角色与相机之间的空间与运动依赖关系**，导致动画缺乏电影级构图意识和流畅的视角调度。后处理式的约束匹配（如**M2C-T**、**AutoVisNarr**）仅能进行浅层对齐，无法从根本上解决协同生成问题。

### 核心方法

本文首次提出**联合角色-相机运动扩散模型**（Joint Character-Camera Motion Diffusion Model），将角色与相机视为独立实体，在统一的扩散框架中显式建模三实例（两角色+相机）之间的成对交互。核心设计包括：

- **Toric空间相机表示**：采用屏幕坐标与角度参数描述相机姿态，使相机特征与角色位置直接关联。
- **成对交互模块**：角色-角色、角色-相机之间的双向残差更新机制，动态调整实体嵌入以捕捉相互影响。
- **联合扩散解码**：在交互更新后的嵌入基础上预测去噪运动序列，实现协同优化。

### 关键结论

在本文构建的数据集上，所提方法在角色运动质量（FID 0.113 vs 最强基线ComMDM 0.156）和相机运动质量（SeqFID 0.256 vs DC3D 0.417）上均取得显著提升。消融实验证实，完整的成对交互模块对运动质量和角色-相机协调性至关重要——移除任一交互模块均导致性能显著下降。定性结果显示，本方法能够生成具有电影级构图意识和流畅视角调度的叙事动画。

### 方法定位

本方法属于**多实体运动联合生成**范式，在扩散模型框架下首次将角色运动生成与相机运动生成统一建模。相较于**InterGen**（Liang et al., IJCV 2024）等仅建模角色间交互的工作，本方法将交互建模扩展至角色-相机维度，填补了叙事动画生成中协同建模的空白。



### 叙事动画中的角色-相机协同困境

在电影、游戏和虚拟现实等叙事媒介中，富有表现力的动画不仅取决于角色运动的自然性，更依赖于相机运动与角色表演之间的精妙配合。导演通过推拉摇移、景别切换和构图变化来引导观众注意力，强化戏剧张力——这种角色与相机的协同叙事能力，是区分机械运动与生动叙事的关键所在。

然而，现有运动生成方法在这一核心需求上存在根本性断裂：**角色运动生成与相机运动生成被当作两个独立问题分别处理**。一方面，以 **ComMDM**、**InterGen** (Liang et al., IJCV 2024) 为代表的双角色交互生成方法专注于角色间的协调性，却完全忽略了相机视角的存在；另一方面，**CDM** (Jiang et al., CGF 2024)、**DC3D** (Wang et al., CVPR 2024) 等相机运动生成方法虽能产出平滑的镜头轨迹，但缺乏对角色空间位置和运动节奏的感知。这种分离式处理导致一个尴尬的后果：即使角色运动和相机运动各自质量很高，将它们拼合后却往往出现构图失衡、主体脱框或剪辑节奏错位等问题，动画整体缺乏叙事连贯性。

### 现有方法的三个结构性缺口

深入审视现有方法，可以识别出三个相互关联的结构性缺口：

**第一，生成空间的单实体范式。** 现有扩散模型或仅操作于角色运动空间，或仅操作于相机参数空间，从未将角色与相机纳入统一的生成框架。这意味着模型无法在采样过程中感知另一实体的存在，更谈不上协调优化。少数后处理方法（如 **M2C-T**、**AutoVisNarr**）试图在生成后施加约束规则来匹配角色与相机，但这种事后对齐的方式本质上是补救性的，无法从根本上解决联合分布建模的问题。

**第二，交互建模的缺失。** 角色之间的空间关系（如面对面、并排行走）直接影响最优相机位置的选择，而相机的运动方式（如跟拍、环绕）反过来又约束角色的走位和朝向。这种双向因果依赖在现有框架中被完全忽略——角色生成模型不知道相机在哪，相机生成模型也不知道角色在做什么。

**第三，相机表示的非结构化。** 传统方法通常使用全局三维坐标或原始欧拉角来表示相机运动，这些表示与屏幕构图之间缺乏直观的对应关系。导演关心的核心问题——角色在画面中的位置、头部在屏幕上的坐标——无法从这些表示中直接读取，使得模型难以学习到“将角色保持在画面合适位置”这样的基本构图规则。

### 本文动机与核心思路

针对上述困境，本文首次提出将角色运动与相机运动视为一个**联合生成问题**。核心动机在于：叙事动画的本质是角色与相机在时空上的协同编排，这要求在生成过程中显式建模两者之间的相互影响，而非事后拼接。

为此，本文引入三个关键设计来填补现有缺口：

- **三实例联合生成空间**：将扩散模型的生成空间扩展为同时包含两个交互角色和一个动态相机的统一空间，使三者能够在同一采样过程中相互感知。
- **成对交互模块**：显式建模角色-角色、角色-相机之间的双向影响，通过残差更新机制让每个实体的运动嵌入动态吸收来自其他实体的信息。
- **Toric空间相机表示**：采用基于屏幕坐标和角度的Toric空间参数化，使相机运动与画面构图直接关联，便于模型学习镜头语言的语义。

这一框架的最终目标是：从随机噪声出发，一次性采样出角色运动、角色间交互以及与之协调的相机运动，三者共同构成一段具有叙事感的动画序列。



## 核心方法与创新机理

本文的核心创新在于首次将角色运动生成与相机运动生成从两个独立问题统一为一个**联合生成问题**，并提出了一套与之匹配的架构设计。其创新点可归纳为三个关键的“changed slots”：生成空间的扩展、交互建模机制的引入，以及相机表示空间的重新设计。

### 1. 从单实体生成到三实例联合空间

现有工作将角色运动（如 **ComMDM**、**InterGen** (Liang et al., IJCV 2024)）与相机运动（如 **CDM** (Jiang et al., CGF 2024)、**DC3D** (Wang et al., CVPR 2024)）视为独立任务处理。即使是后处理方法（如 **M2C-T**、**AutoVisNarr**），也仅在生成后施加约束，无法在生成过程中实现两者的协同优化。其根本瓶颈在于：角色与相机在叙事动画中是因果耦合的——角色的位置与动作决定了最佳的拍摄角度，而相机的运动轨迹又反过来定义了观众所见的叙事空间。分离建模必然导致视觉一致性与叙事连贯性的缺失。

本文的方法将扩散模型的生成空间从单一实体直接扩展为**三实例联合运动空间**（两个交互角色 + 一个动态相机）。如原文所述：“we extend the diffusion model to operate in a three-instance motion space, consisting of two interacting characters and a dynamic camera”。这一设计使得模型能够从联合分布 $p(\text{角色A}, \text{角色B}, \text{相机})$ 中直接采样，从根源上保证了生成结果的内在协调性，而非事后修补。

### 2. 双向成对交互模块：显式建模实体间的因果影响

仅将三个实体的运动向量拼接后送入扩散模型并不足以捕捉它们之间复杂的依赖关系。本文的核心机制创新在于引入了**三种成对交互模块**，对实体间的影响进行显式建模：

- **角色-角色交互模块**：建模角色A与B之间的双向影响，预测残差 $\Delta h_t^{B \to A}$ 和 $\Delta h_t^{A \to B}$。
- **相机-角色交互模块**（两组）：分别建模相机与角色A、相机与角色B之间的双向影响，产生从角色到相机（$\Delta h_t^{A \to c}$）和从相机到角色（$\Delta h_t^{c \to A}$）的残差。

这些模块的工作方式是**双向残差更新**：每个实体的Transformer编码特征 $h_t$ 会加上来自其他实体的交互残差，得到精炼后的隐藏状态。例如，角色A的更新公式为：

$$\hat{h}_t^A = h_t^A + \Delta h_t^{B \to A} + \Delta h_t^{c \to A}$$

这种设计的关键在于，它使得每个实体的特征不仅包含自身的运动信息，还融合了其他实体对它的“因果影响”。相机模块会“知道”角色当前的运动状态，从而调整自身轨迹以保持最佳构图；角色模块也会“感知”相机的视角变化，从而调整表演的空间位置。消融实验有力地证实了这一设计的必要性：移除任一交互模块（角色-角色或相机-角色）都会导致角色运动FID、相机运动SeqFID以及角色-相机对齐损失（Character-Camera Alignment loss）的显著恶化（Table 4, 5, 6）。

### 3. Toric空间相机表示：从物理参数到叙事构图

传统相机运动生成方法通常直接使用相机的全局3D坐标或原始姿态参数，这种表示与屏幕上的叙事构图（如角色在画面中的位置、景别大小）之间缺乏直观联系，不利于模型学习角色与相机之间的空间耦合关系。

本文改用**Toric空间坐标系统**来表示相机运动。如公式(1)所示，相机特征序列由四个参数定义：

$$x_c^{1:N} = \{ p_A^i, p_B^i, \theta^i, \phi^i \}_{i=1}^N \in \mathbb{R}^{6N}$$

其中，$(p_A, p_B)$ 是两个角色头部在屏幕上的归一化二维坐标，直接定义了画面的构图；$(\theta, \phi)$ 是相机在Toric空间中的方位角和俯仰角，描述了相机围绕角色连线的旋转姿态。这一表示将相机的物理运动与**叙事意图**（即“画面中的人物如何被观看”）直接对齐，使得模型能够更容易地学习到“当角色A靠近角色B时，相机应推近以捕捉特写”这类高层语义规律，是实现角色-相机协同生成的重要使能技术。

综上，本文的创新并非单一的技术点，而是一套环环相扣的系统性设计：**Toric空间**提供了叙事感知的表示基础，**三实例联合空间**确立了协同生成的框架，而**双向成对交互模块**则是实现该框架内实体间因果建模的核心机制。三者共同构成了首个能够端到端联合生成叙事动画中角色与相机运动的统一框架。



本文提出**Joint Character-Camera Motion Diffusion Model**，首次将双角色运动与动态相机运动纳入统一的扩散生成框架。核心思路是将两个角色与相机视为三个独立但相互影响的实体，在扩散模型内部显式建模它们之间的成对交互，从而实现协调的联合运动生成。

### 输入表示

框架接受三个实体的运动序列作为联合生成目标。对于两个角色，每个角色的运动被表示为一个包含6D旋转表示与根节点位移的位姿序列，并附加一个9维偏移向量以确定角色在全局场景中的相对位置，最终每帧展平为150维向量。对于相机，采用**Toric空间**参数化（见Figure 2），使用屏幕上两个角色头部的位置坐标 $(p_{Ax}, p_{Ay})$ 和 $(p_{Bx}, p_{By})$，以及相机的偏航角 $\theta$ 和俯仰角 $\phi$，共6维参数描述每帧的相机姿态：

$$x_c^{1:N} = \{ p_A^i, p_B^i, \theta^i, \phi^i \}_{i=1}^N \in \mathbb{R}^{6N}$$

### 扩散流程

模型以MDM架构为基础，将扩散过程扩展至三实例运动空间。前向过程逐步向原始运动序列注入高斯噪声：

$$q(x_{1:T}^{1:N} | x_0^{1:N}) = \prod_{t=1}^T q(x_t^{1:N} | x_{t-1}^{1:N})$$

$$q(x_t^{1:N} | x_{t-1}^{1:N}) = \mathcal{N}(x_t^{1:N}; \sqrt{1-\beta_t} x_{t-1}^{1:N}, \beta_t \mathbf{I})$$

逆向过程学习从纯噪声中逐步去噪恢复运动序列，训练时采用直接预测干净运动的简化损失：

$$\mathcal{L}_{simple} = \mathbb{E}_{x_0^{1:N} \sim q(x_0^{1:N}), t \sim [1,T]} [\| x_0^{1:N} - f_\theta(x_t^{1:N}, t) \|_2^2]$$

### 核心架构：三实例编码与成对交互

如Figure 3所示，去噪网络由三个并行的**Transformer Encoder**分支构成，分别处理角色A、角色B和相机的噪声运动序列输入，提取高维运动嵌入 $h_t^A$、$h_t^B$、$h_t^c$。

框架的关键创新在于三个**成对交互模块**，它们在不同实体之间建模双向影响：

- **角色-角色交互模块**：建模角色A与B之间的相互影响，预测两个方向的残差修正 $\Delta h_t^{B \to A}$ 和 $\Delta h_t^{A \to B}$。
- **相机-角色交互模块（×2）**：分别建模相机与角色A、相机与角色B之间的双向影响，每个模块生成两个方向残差（角色→相机、相机→角色）。

每个实体的隐藏状态通过累加来自其他实体的交互残差进行更新：

$$\hat{h}_t^A = h_t^A + \Delta h_t^{B \to A} + \Delta h_t^{c \to A}$$

$$\hat{h}_t^B = h_t^B + \Delta h_t^{A \to B} + \Delta h_t^{c \to B}$$

$$\hat{h}_t^c = h_t^c + \Delta h_t^{A \to c} + \Delta h_t^{B \to c}$$

更新后的嵌入 $(\hat{h}_t^A, \hat{h}_t^B, \hat{h}_t^c)$ 被送入**Diffusion Decoder**，预测去噪后的运动序列 $(\hat{x}_0^{A,1:N}, \hat{x}_0^{B,1:N}, \hat{x}_0^{c,1:N})$。

### 设计逻辑

该架构的因果机制在于：通过将角色与相机视为独立实体并显式建模它们之间的成对交互，模型能够同时捕捉角色间的空间协调关系（如打斗、拥抱）以及相机对角色构图的动态响应（如跟拍、推拉）。消融实验（Table 4-6）证实，移除任一交互模块均会导致角色运动质量、相机运动质量以及角色-相机对齐度显著下降，验证了双向交互建模对叙事动画协同生成的关键作用。

### 补充图表

![[assets/figures/papers/paper_list_l3_https_openaccess_thecvf_com_content_CVPR2026_papers_Cheng_Towards_Storyt/figures/003_Figure_3.jpg]]
*Figure 3: Overview of our joint character-camera motion generation framework. The model takes Gaussian noise as input and jointly generates motion sequences for two interacting characters and a dynamic camera. Each instance is processed through a Transformer encoder to extract high-level motion embeddings. Three pairwise interaction modules model the relationships between each pair of instances: A↔ B, A↔ Camera, and B↔ Camera. These modules produce residuals that are added to the original embeddings to enable mutual influence among all agents*

![[assets/figures/papers/paper_list_l3_https_openaccess_thecvf_com_content_CVPR2026_papers_Cheng_Towards_Storyt/figures/001_Figure_1.jpg]]
*Figure 1: Our framework jointly generates the motion of two interacting characters and the motion of a camera to visually tell a story. The central panel shows two instances of generated character-camera motions. For each pair of character and camera motions, we display rendered viewpoints at four sampled moments along each camera motion trajectory*



### 运动表示

**角色运动表示**。每个角色的运动序列由 $N$ 帧姿态构成，采用连续 6D 旋转表示与根节点平移。对于双角色场景，为每个角色计算一个 9 维偏移向量 $D \in \mathbb{R}^9$，将其附加到每一帧的姿态向量中，使得每帧表示为 $25 \times 6$ 矩阵，展平后得到 150 维向量。这一设计确保了双角色在世界空间中的全局位置关系被显式编码。

**相机运动表示**。相机运动采用 Toric 空间坐标系描述，该表示直接捕捉镜头构图的核心要素：两个主要角色头部在屏幕上的归一化坐标以及相机的朝向角。具体而言，相机在 $N$ 帧上的运动序列表示为：

$$x_c^{1:N} = \{ p_A^i, p_B^i, \theta^i, \phi^i \}_{i=1}^N \in \mathbb{R}^{6N}$$

其中 $p_A^i = (p_{Ax}^i, p_{Ay}^i)$ 和 $p_B^i = (p_{Bx}^i, p_{By}^i)$ 分别为第 $i$ 帧角色 A 与角色 B 头部在屏幕上的二维位置，$\theta^i$ 和 $\phi^i$ 为相机的偏航角和俯仰角。这一 6N 维表示将相机运动与角色屏幕位置直接关联，为后续的交互建模提供了自然的耦合接口。

### 扩散模型框架

本文以 MDM（Motion Diffusion Model）架构为基础，将扩散模型扩展至三实例联合运动空间——两个交互角色与一个动态相机。扩散过程包含前向加噪与逆向去噪两个阶段。

**前向扩散过程**。给定干净运动序列 $x_0^{1:N}$，前向过程通过 $T$ 步逐步注入高斯噪声：

$$q(x_{1:T}^{1:N} | x_0^{1:N}) = \prod_{t=1}^T q(x_t^{1:N} | x_{t-1}^{1:N})$$

单步前向扩散定义为：

$$q(x_t^{1:N} | x_{t-1}^{1:N}) = \mathcal{N}(x_t^{1:N}; \sqrt{1-\beta_t} x_{t-1}^{1:N}, \beta_t \mathbf{I})$$

其中 $\beta_t$ 为噪声调度参数。

**逆向去噪过程**。逆向过程学习从纯噪声 $x_T^{1:N}$ 逐步恢复干净运动：

$$p(x_{0:T}^{1:N}) = p(x_T^{1:N}) \prod_{t=1}^T p_\theta(x_{t-1}^{1:N} | x_t^{1:N})$$

训练时采用简化的预测损失，直接预测干净运动 $x_0^{1:N}$：

$$\mathcal{L}_{simple} = \mathbb{E}_{x_0^{1:N} \sim q(x_0^{1:N}), t \sim [1,T]} [|| x_0^{1:N} - f_\theta(x_t^{1:N}, t) ||_2^2]$$

### 三实例交互架构

去噪网络的核心设计在于将角色与相机视为独立但相互作用的实体，通过三个并行的 Transformer 编码器分别提取角色 A、角色 B 和相机的高维运动嵌入 $h_t^A$、$h_t^B$、$h_t^c$。在此基础上，三组建模成对交互的模块被引入，以捕捉实体间的双向影响。

**角色-角色交互模块**。该模块建模角色 A 与 B 之间的双向影响，预测两个方向的残差修正量 $\Delta h_t^{B \to A}$ 和 $\Delta h_t^{A \to B}$，分别表示角色 B 对角色 A 的影响以及角色 A 对角色 B 的影响。

**相机-角色交互模块**。两组相机-角色交互模块分别处理相机与角色 A、相机与角色 B 之间的双向关系。每组模块产生两个方向残差：角色到相机的影响以及相机到角色的影响，例如 $\Delta h_t^{A \to c}$ 和 $\Delta h_t^{c \to A}$。

**残差融合**。所有交互残差计算完成后，每个实体的隐藏状态通过累加对应残差项进行更新：

$$\hat{h}_t^A = h_t^A + \Delta h_t^{B \to A} + \Delta h_t^{c \to A}$$

$$\hat{h}_t^B = h_t^B + \Delta h_t^{A \to B} + \Delta h_t^{c \to B}$$

$$\hat{h}_t^c = h_t^c + \Delta h_t^{A \to c} + \Delta h_t^{B \to c}$$

更新后的隐藏状态 $(\hat{h}_t^A, \hat{h}_t^B, \hat{h}_t^c)$ 随后被送入扩散解码器，预测去噪后的运动序列 $(\hat{x}_0^{A,1:N}, \hat{x}_0^{B,1:N}, \hat{x}_0^{c,1:N})$。

这一残差更新机制的本质在于：每个实体的运动生成不仅依赖自身的运动先验，还动态地受到其他实体当前运动状态的调节，从而实现了角色与相机在扩散去噪全过程中的协同优化。消融实验证实，移除任一交互模块均会导致角色运动 FID 升高、相机运动 SeqFID 恶化，以及角色-相机对齐损失显著增加，验证了双向交互建模对协调性至关重要。

### 补充图表

![[assets/figures/papers/paper_list_l3_https_openaccess_thecvf_com_content_CVPR2026_papers_Cheng_Towards_Storyt/figures/002_Figure_2.jpg]]
*Figure 2: We represent shot composition using the on-screen coordinates of the two principal characters’ heads, denoted as*



## 实验与关键发现

### 主实验结果

为验证联合角色-相机运动生成框架的有效性，作者在自建数据集上进行了多维度定量对比，所有方法均在相同的85%/15%训练-测试划分下重新训练与评估，确保公平性。

**角色运动生成质量。** 如表1所示，本文方法在角色运动生成上全面超越现有基线。在核心保真度指标FID上，本文方法达到**0.113**，显著优于最强基线ComMDM的0.156（Δ=-0.043）。在衡量双角色交互质量的InterFID指标上，本文方法同样取得最优结果（0.651）。此外，Coverage指标从ComMDM的0.160提升至**0.264**（Δ=+0.104），表明生成的角色运动在分布覆盖度上有实质性改善。这些结果表明，联合建模相机运动不仅没有损害角色运动质量，反而通过交互模块的协同优化提升了角色运动的真实性与多样性。

**相机运动生成质量。** 表2展示了相机运动生成的结果对比。本文方法在序列级保真度SeqFID上达到**0.256**，相比专门设计用于相机运动生成的DC3D（0.417）大幅降低0.161。在帧级保真度FrameFID上同样取得最优（0.268）。值得注意的是，Density指标从CDM的0.538跃升至**1.937**（Δ=+1.399），说明联合生成框架能够产生更丰富多样的相机运动模式，而非简单的静态或重复轨迹。

**角色-相机运动协调性。** 表3专门评估了生成结果中角色与相机之间的协调程度。本文方法在所有协调性指标上均取得最优，证实了显式建模角色-相机交互对于实现叙事级视觉一致性的关键作用。

### 消融实验

为深入理解各交互模块的贡献，作者进行了系统的消融研究，逐步移除角色-角色交互模块（C-C）和角色-相机交互模块（C-Cam）。

**对角色运动的影响。** 表4显示，完整模型在角色运动的FID、InterFID和Coverage上均取得最优。移除任一交互模块均导致性能下降，其中同时移除两类交互（即无交互的独立生成）性能退化最为严重，证实了成对交互建模对于角色运动质量的重要性。

**对相机运动的影响。** 表5展示了相机运动生成的消融结果。完整模型在SeqFID、FrameFID、Diversity、Coverage和Density五项指标上全面领先。值得注意的是，仅保留角色-角色交互而移除角色-相机交互时，相机运动质量显著下降，表明相机运动的生成高度依赖来自角色运动的信息传递。

**对角色-相机协调性的影响。** 表6直接量化了交互模块对协调性的贡献。完整模型取得最低的角色-相机对齐损失（**2.284**），移除角色-角色交互或角色-相机交互均导致对齐损失显著升高。这一结果有力证明了双向交互机制——既让角色行为影响相机取景，也让相机视角约束角色呈现——是实现叙事级动画协同的关键设计。

### 定性分析

图5展示了不同方法的定性对比。M2C-T和AutoVisNarr等方法在生成结果中出现构图碎片化或机位静态僵化的问题，而本文方法能够保持富有表现力的取景和流畅的电影感运动，角色与相机之间呈现出协调一致的叙事节奏。

### 失败模式与局限性

尽管本文方法在定量和定性评估中均表现优异，但仍存在以下局限：

1. **固定角色数量假设。** 当前框架仅支持两角色交互场景，无法直接扩展至多角色动态，限制了在群戏或复杂场景中的应用。
2. **数据分布覆盖不足。** 数据集主要来源于电影片段和虚拟引擎合成数据，可能未充分覆盖现实世界中多样化的交互类型和相机运动风格。
3. **无条件生成范式。** 当前模型为无条件采样，缺乏对文本叙事、剧本指令或高层语义条件的控制能力，难以直接应用于需要精确叙事驱动的动画创作场景。

这些局限性也指向了未来的研究方向：扩展至多角色动态场景、引入文本叙事条件实现可控生成，以及构建更丰富多样的训练数据以提升模型泛化能力。

### 补充图表

![[assets/figures/papers/paper_list_l3_https_openaccess_thecvf_com_content_CVPR2026_papers_Cheng_Towards_Storyt/figures/005_Table_1.jpg]]
*Table 1: Comparison with baselines on character motion*

![[assets/figures/papers/paper_list_l3_https_openaccess_thecvf_com_content_CVPR2026_papers_Cheng_Towards_Storyt/figures/006_Table_2.jpg]]
*Table 2: Comparison with baselines on camera motion*

![[assets/figures/papers/paper_list_l3_https_openaccess_thecvf_com_content_CVPR2026_papers_Cheng_Towards_Storyt/figures/007_Table_3.jpg]]
*Table 3: Comparison with baselines on character-camera motion coordination*

![[assets/figures/papers/paper_list_l3_https_openaccess_thecvf_com_content_CVPR2026_papers_Cheng_Towards_Storyt/figures/008_Table_4.jpg]]
*Table 4: Ablation on interaction modeling for character motion*

![[assets/figures/papers/paper_list_l3_https_openaccess_thecvf_com_content_CVPR2026_papers_Cheng_Towards_Storyt/figures/009_Table_5.jpg]]
*Table 5: Ablation on interaction modeling for camera motion*

![[assets/figures/papers/paper_list_l3_https_openaccess_thecvf_com_content_CVPR2026_papers_Cheng_Towards_Storyt/figures/010_Table_6.jpg]]
*Table 6: Ablation on interaction modeling for character-camera motion coordination*

![[assets/figures/papers/paper_list_l3_https_openaccess_thecvf_com_content_CVPR2026_papers_Cheng_Towards_Storyt/figures/011_Figure_5.jpg]]
*Figure 5: Qualitative comparison. While M2C-T and AutoVisNarr yield fragmented or static compositions, our method maintains expressive framing and cinematic flow, resulting in superior coordination between characters and camera motion*



## 定位与知识库关联

### 1. 问题定位与核心瓶颈

叙事动画生成要求同时协调角色运动与相机运动，以构建连贯的视觉叙事。现有工作将这两个子任务割裂处理：角色运动生成方法（如 **ComMDM**、**InterGen** (Liang et al., IJCV 2024)、**RIG**）仅关注单角色或双角色交互，完全忽略相机视角；相机运动生成方法（如 **CDM** (Jiang et al., CGF 2024)、**DC3D** (Wang et al., CVPR 2024)）则将角色运动视为固定输入，无法反向影响角色行为。这种分离范式导致生成结果缺乏叙事连贯性——角色动作与镜头语言各自为政，无法形成电影级的协同表达。

本文的核心突破在于**首次将角色运动与相机运动纳入统一生成框架**，在扩散模型中显式建模三实体（两角色+相机）之间的成对交互关系。这一设计将问题从“两个独立生成任务的拼接”提升为“一个联合分布的学习问题”，直接回应了叙事动画中角色-相机协调性的根本需求。

### 2. 技术谱系与继承关系

本方法建立在两条技术路线的交叉点上：

**角色运动生成线**：继承自 **MDM**（Motion Diffusion Model）的扩散架构，将运动序列视为去噪目标。与 **ComMDM** 的双角色独立编码不同，本文引入了显式的角色-角色交互模块，通过双向残差更新捕捉角色间的空间与运动依赖。这一设计借鉴了 **InterGen** 的交互建模思想，但将其从纯角色域扩展至角色-相机跨域交互。

**相机运动生成线**：相机表示采用 **Toric 空间**参数化——将相机姿态编码为两个角色头部在屏幕上的归一化坐标 $(p_A, p_B)$ 以及相机的偏航角 $\theta$ 和俯仰角 $\phi$。这一表示源自影视摄影的 Toric 坐标系理论，**DC3D** 曾将其引入舞蹈场景的相机运动生成。本文的关键改进在于将 Toric 参数从“给定角色位置后的后处理计算”变为“扩散模型联合优化的内生变量”，使相机运动与角色运动在生成过程中相互塑造。

**协调方法线**：**M2C-T** 和 **AutoVisNarr** 曾尝试协调角色与相机，但均采用后处理约束或规则式映射，无法在生成阶段实现深度耦合。本文的交互模块设计从根本上解决了这一问题——角色-相机交互模块在扩散去噪的每一步都动态调整两者的隐藏状态，使协调性成为生成过程的内在属性。

### 3. 方法边界与适用条件

**适用场景**：
- 双角色交互场景（对话、打斗、舞蹈等），角色数量固定为 2。
- 需要电影级镜头构图的叙事动画生成。
- 无条件生成或基于运动先验的采样。

**不适用或需谨慎使用的场景**：
- **多角色动态场景**（>2 角色）：当前架构的三实例设计无法直接扩展，交互模块数量将随角色数呈二次增长。
- **强文本条件控制**：模型为无条件生成，缺乏对文本叙事或剧本语义的显式建模，无法根据“紧张的对峙”或“欢快的舞蹈”等高层描述控制生成。
- **极端交互类型**：数据集主要来源于电影片段和 Cine Tracer 虚拟引擎合成数据，可能未充分覆盖体育竞技、人群疏散等特殊交互模式。

### 4. 关键设计决策的消融证据

交互模块的消融实验（Table 4-6）为架构设计提供了强因果证据：

- **角色-角色交互模块**：移除后，角色运动 FID 从 0.143 升至 0.192（Table 4），表明角色间双向建模对运动质量至关重要。
- **角色-相机交互模块**：移除后，相机运动 SeqFID 从 0.077 升至 0.119（Table 5），角色-相机对齐损失从 2.284 升至 3.102（Table 6），证实跨域交互是协调性的核心来源。
- **完整三模块配置**在所有指标上取得最优，证明“分离建模+成对交互”的架构假设成立。

### 5. 局限与开放问题

**已知局限**（论文明确指出的边界）：
1. **固定双角色限制**：模型无法直接处理单角色或多于两角色的场景，架构缺乏实例数量的灵活性。
2. **数据覆盖偏差**：数据集依赖电影片段和虚拟引擎，现实场景中的交互多样性和相机运动风格可能未被充分代表。
3. **无条件生成**：缺乏对文本、音频或剧本等高层语义条件的控制，限制了在完整叙事管线中的应用。

**开放研究问题**：
- **如何扩展至多角色动态场景？** 可能的路径包括引入图神经网络建模可变数量的角色交互，或采用注意力机制动态分配交互权重。
- **如何实现文本叙事条件控制？** 需要将语言语义与角色-相机联合运动空间对齐，可能借助 CLIP 等多模态嵌入或基于大语言模型的运动规划。
- **如何评估叙事连贯性？** 当前指标（FID、Coverage 等）侧重运动质量和多样性，缺乏对“叙事逻辑”的直接度量，需要设计新的评估范式。

### 6. 知识库定位

本文在叙事动画生成领域填补了“联合角色-相机运动生成”的空白。相较于分离式方法（ComMDM + DC3D 的简单拼接），本文首次证明了在扩散模型内部进行跨实体交互建模的可行性与优越性。其 Toric 空间表示与成对交互模块的设计为后续工作提供了可复用的技术组件，同时也暴露了多角色扩展和语义条件控制两个明确的研究缺口，为社区指明了后续攻关方向。



## 原文 PDF

![[paperPDFs/CVPR_2026/Towards_Storytelling_Animations_Joint_Synthesis_of_Human_and_Camera_Motions.pdf]]
