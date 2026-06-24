---
title: "GA-VLN: Geometry-Aware BEV Representation for Efficient Vision-Language Navigation"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/GA_VLN_Geometry_Aware_BEV_Representation_for_Efficient_Vision_Language_Navigation.pdf
project_link: null
code_link: "https://github.com/jahhaoyang/GA-VLN"
aliases:
- GV
- GA-VLN
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
- topic/representation_self_supervised_transfer
core_operator: 将稠密RGB视频token替换为紧凑的几何感知BEV表示，该表示融合显式深度投影与隐式3D几何先验，从而大幅降低token数量并增强多视角空间推理。
primary_logic: 通过将RGB-D特征投影到以智能体为中心的BEV空间，并融入预训练3D基础模型的结构先验，形成紧凑且空间一致的表示，显著提升导航效率和性能，无需DAgger增强或多任务VQA数据。
claims:
- 在R2R-CE、RxR-CE、NavRAG-CE三个基准上，GA-VLN不使用DAgger增强或VQA混合训练即达到最优性能，超越所有对比方法。
- 消融实验表明，显式BEV投影与隐式3D几何先验互补：添加显式投影后SR从51.49%提升至59.21%，进一步加入3D先验后提升至60.96%（Table 2）。
- "GA-BEV表示将视觉token数从4003降至394（约一个数量级），同时显著改善成功率（Table 3，Row #1 vs #2）。"
- R2R-CE val unseen 上 NE↓/OSR↑/SR↑/SPL↑ = 4.80/67.6/61.0/55.2
---

# GA-VLN: Geometry-Aware BEV Representation for Efficient Vision-Language Navigation

> [!tip] 核心洞察
> 通过将RGB-D特征投影到以智能体为中心的BEV空间，并融入预训练3D基础模型的结构先验，形成紧凑且空间一致的表示，显著提升导航效率和性能，无需DAgger增强或多任务VQA数据。

| 字段 | 内容 |
|------|------|
| 中文题名 | GA-VLN：面向高效视觉语言导航的几何感知BEV表示 |
| 英文题名 | GA-VLN: Geometry-Aware BEV Representation for Efficient Vision-Language Navigation |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2605.22036) · [Code](https://github.com/jahhaoyang/GA-VLN) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction #topic/representation_self_supervised_transfer |
| Method | GA-VLN |
| Dataset | R2R-CE val unseen, RxR-CE val unseen, NavRAG-CE val unseen |

> [!tip] 效果简介
> - R2R-CE val unseen 上，NE↓/OSR↑/SR↑/SPL↑ 4.80/67.6/61.0/55.2 vs 4.83/63.3/58.2/54.0 (InternVLA-N1) (-0.03/+4.3/+2.8/+1.2)。
> - RxR-CE val unseen 上，NE↓/OSR↑/SR↑/SPL↑ 5.88/67.0/55.4/45.2 vs 5.91/53.5/46.1 (InternVLA-N1, OSR未报告) (-0.03/+1.9/-0.9)。
> - NavRAG-CE val unseen 上，NE↓/OSR↑/SR↑/SPL↑ 7.88/46.4/22.2/18.2 vs 8.12/38.4/24.7/18.8 (MapNav) (-0.24/-2.5/-0.6)。

## 概述

### 问题与瓶颈

视觉语言导航（VLN）要求智能体根据自然语言指令在连续环境中移动并抵达目标位置。近年来，基于多模态大语言模型（MLLM）的方法展现出强大的指令理解和推理能力，但其核心瓶颈在于：**现有方法依赖稠密的RGB视频帧作为视觉输入，产生大量冗余视觉token且缺乏显式三维空间结构，导致高计算开销和有限的空间推理能力**。例如，典型的图像基线方法在单步推理中需处理超过4000个视觉token，且token数量随导航步数线性增长，严重制约了实时部署效率。

### 核心思路与方法定位

GA-VLN提出**几何感知的鸟瞰图表示（Geometry-Aware BEV, GA-BEV）**，从根本上改变了VLN中的视觉表征范式。其核心洞察是：将稠密RGB视频token替换为紧凑且空间一致的BEV表示，该表示融合了**显式深度引导的3D投影特征**与**隐式3D基础模型的结构先验**，从而大幅降低token数量（约一个数量级）并增强多视角空间推理能力。

具体而言，GA-BEV通过以下机制实现效率与精度的双重提升：
- **显式深度投影**：利用RGB-D观测和相机参数，将2D图像patch中心反投影到以智能体为中心的3D世界坐标，再聚合到BEV网格平面。
- **隐式几何先验**：引入冻结的预训练3D基础模型VGGT-1B，从历史图像序列中提取多视图几何特征，为BEV表示注入结构连续性和形状先验。
- **紧凑表征**：仅保留非空BEV网格单元，token数从约4000降至约400，且token数不随导航步数线性增长。

在方法谱系上，GA-VLN属于**基于MLLM的端到端VLN方法**，但与同类工作形成鲜明对比：**NaVid**（Zhang et al., arXiv 2024）和**Uni-NaVid**（Zhang et al., arXiv 2024b）使用视频VLM处理稠密帧序列；**StreamVLN**（Wei et al., arXiv 2025）采用慢-快上下文建模但仍依赖图像token；**InternVLA-N1**（InternNav Contributors, 2025）和**NaVILA**（Cheng et al., arXiv 2024）同样基于图像MLLM，未引入显式3D空间结构。GA-VLN的关键区分点在于：**用几何感知的BEV表示替代稠密图像token，将空间推理从隐式学习转向显式几何编码**。

### 主要结果

在R2R-CE、RxR-CE和NavRAG-CE三个标准基准的val unseen划分上，GA-VLN**不使用DAgger增强或混合VQA训练**即达到最优性能（Table 1）：
- **R2R-CE**：SR 61.0%，SPL 55.2%，超越InternVLA-N1（SR 58.2%）等所有对比方法。
- **RxR-CE**：SR 55.4%，SPL 45.2%，在成功率上显著领先。
- **NavRAG-CE**：SR 22.2%，在检索增强导航场景中展现竞争力。

消融实验（Table 2）揭示了各模块的因果贡献：纯图像基线SR仅51.49%；添加显式BEV投影后提升至59.21%，同时推理计算量从32.19 TFLOPs降至5.15 TFLOPs，延迟从342.9ms降至212.9ms；进一步融入隐式3D几何先验后SR达到60.96%，验证了两类几何信息的互补性。Token效率分析（Table 3）表明，GA-BEV将视觉token从4003压缩至394，且性能大幅优于简单深度拼接方案（RGB-Depth拼接致token翻倍至8006，SR反而降至38.61%）。

### 局限与开放问题

GA-VLN在零样本实机部署时暴露出路径安全性不足的问题（因缺少避障模块，智能体偶尔贴近墙壁行走），离散动作粒度也导致停止位置不够精确。训练数据方面，引入NavRAG-CE会损害R2R-CE和RxR-CE的泛化性能，存在数据集分布偏移。开放问题包括：两轮对话格式对推理延迟的实际影响、调整为更细粒度旋转步角后的定量效果、BEV表示在深度噪声较大时的退化程度，以及3D基础模型预训练数据分布对室内导航场景的适配性。

## 背景与动机

视觉语言导航（VLN）要求智能体在连续三维环境中根据自然语言指令自主移动。近年来，多模态大语言模型（MLLM）的兴起为VLN带来了端到端的推理与决策能力，但现有基于MLLM的导航方法普遍依赖**稠密RGB视频帧**作为视觉输入。这一设计存在两个根本性缺陷：

1. **严重的token冗余**：每帧图像经视觉编码器（如SigLIP）提取的patch token数量通常在数百至数千量级，历史帧累积后视觉token总数急剧膨胀。例如，基准图像MLLM方法在一次推理中需处理4003个视觉token（Table 3, Row #1），导致MLLM推理的计算开销和延迟居高不下。

2. **缺乏显式三维空间结构**：稠密RGB patch token本质上是二维图像特征的扁平序列，未编码深度信息或三维几何关系。MLLM被迫从这些扁平token中隐式推断空间布局，空间推理能力受限，尤其在需要多视角一致性理解的长程导航任务中表现不足。

现有工作尝试通过慢-快上下文建模（**StreamVLN**，Wei et al., arXiv 2025）、统一多任务训练（**Uni-NaVid**，Zhang et al., arXiv 2024b）或DAgger增强等策略缓解上述问题，但这些方法仍是**在图像token空间内操作**，未从根本上改变视觉表示的形态。深度信息若被简单拼接到RGB通道，反而使token数量翻倍（如RGB-Depth拼接导致8006个token，Table 8），进一步加剧计算负担。

本文的核心动机在于：**是否能用一种紧凑且空间一致的表示替代稠密图像token，从根本上降低MLLM的视觉token负载，同时注入显式的三维几何结构？** 受自动驾驶领域BEV（Bird's-Eye View）表示启发，作者提出将历史RGB-D观测投影到以智能体为中心的鸟瞰平面，形成**几何感知BEV（Geometry-Aware BEV, GA-BEV）表示**。该表示通过以下两个机制实现紧凑性与空间表达力的统一（Figure 1）：

- **显式深度投影**：利用深度图与相机内外参将每个图像patch的中心点反投影到三维世界坐标，再投影到BEV网格平面进行聚合，使视觉特征天然携带空间位置信息。
- **隐式3D几何先验**：引入冻结的预训练3D基础模型（VGGT-1B），从历史图像序列中提取多视图几何特征，经MLP对齐后与BEV特征融合，注入结构连续性和形状先验。

GA-BEV表示仅保留非空网格单元，token数量从数千降至数百（如394个token，Table 3），同时显著提升导航成功率。该方法仅使用高质量导航数据训练，无需DAgger增强或混合VQA数据，在R2R-CE、RxR-CE和NavRAG-CE三个基准上达到最优性能（Table 1），验证了**以几何感知的紧凑表示替代稠密图像token**这一技术路线的有效性。

## 核心创新

GA-VLN的核心创新在于用一个**紧凑的几何感知BEV表示（GA-BEV）**替代传统MLLM导航方法中的稠密RGB视频token，从根本上解决视觉token冗余与三维空间结构缺失两大瓶颈。这一表示通过两个互补机制构建：**显式深度引导的空间投影**与**隐式3D几何先验注入**。

### 从稠密图像到几何感知BEV的表示跃迁

现有基于MLLM的VLN方法（如**NaVid**、**Uni-NaVid**、**NaVILA**、**StreamVLN**等）将每帧RGB图像编码为 $H_p \times W_p$ 个patch token，并累积多帧历史，导致视觉token数量随导航步数线性增长，产生大量冗余信息。更关键的是，这种纯图像表示缺乏显式的三维空间结构，MLLM必须从扁平的token序列中隐式推断空间关系，限制了空间推理的精度与效率。

GA-VLN的解决方案是将视觉表示从“像素空间”迁移到“以智能体为中心的BEV空间”。具体而言，系统利用RGB-D观测和相机内外参，将每一帧的patch中心点反投影到三维世界坐标：

$$\hat{\mathbf{p}}_t(u,v) = \left[ R_t \quad \mathbf{p}_t \right] K^{-1} \left[ \begin{array}{l} u \\ v \\ 1 \end{array} \right] D_t(u,v)$$

随后，这些三维特征点根据其 $(x,z)$ 坐标被分配到地面平面的BEV网格中。每个网格单元内的特征经均值池化并加上正弦位置编码，形成GA-BEV表示。由于仅保留非空网格单元，最终token数从稠密图像的约4000个骤降至约400个（约一个数量级），同时保留了显式的空间结构——每个token天然对应一个物理位置区域。

### 显式投影与隐式先验的互补设计

GA-BEV的核心洞察在于：**显式深度投影**提供了几何定位的“骨架”，而**隐式3D几何先验**则补充了结构连续性和形状理解。两者并非替代关系，而是高度互补。

**显式深度引导投影**将2D视觉特征与3D空间坐标显式绑定，使MLLM能够直接感知物体和结构在空间中的分布。消融实验（Table 2）表明，在纯图像基线（SR 51.49%）上仅添加显式BEV投影，成功率即跃升至59.21%，同时推理计算量从32.19 TFLOPs降至5.15 TFLOPs，延迟从342.9ms降至212.9ms。这验证了空间结构化表示本身即可大幅提升效率与精度。

**隐式3D几何先验**来自冻结的预训练3D基础模型VGGT-1B。该模型从历史图像序列 $\{I_1, \dots, I_t\}$ 中提取多视图几何特征，经两层MLP（Linear–GeLU–Linear，隐藏层维度4096）投影对齐后，与视觉特征在BEV网格内融合。VGGT-1B的大规模3D预训练赋予了系统强大的形状先验和结构连续性感知能力，能够补全因遮挡或视角有限而缺失的几何信息。在显式投影基础上加入3D几何先验后，成功率进一步提升至60.96%，同时仅引入可接受的计算开销（延迟258.7ms）。

### 与基准方法的关键差异

| 设计维度 | 基准方法 | GA-VLN |
|---------|---------|--------|
| **视觉输入表示** | 稠密RGB patch token（每帧 $H_p \times W_p$ 个），累积历史帧 | 紧凑BEV表示，仅保留非空网格单元，token数减少约10倍 |
| **深度信息处理** | 不使用深度或简单将深度图与RGB通道拼接（token加倍） | 深度引导的3D空间投影，将patch中心映射到世界坐标后聚合到BEV平面 |
| **3D几何先验** | 无 | 冻结的VGGT-1B提取多视图几何特征，经MLP投影后与视觉特征融合 |
| **动作预测策略** | 通常每次预测一个动作，使用整个历史帧 | 两轮对话生成，每轮预测四个离散动作，BEV每8步更新一次 |

值得注意的是，GA-VLN在训练中**未使用DAgger增强数据或通用VQA混合训练**，仅依赖高质量导航数据集（R2R-CE、RxR-CE、EnvDrop、ScaleVLN、SRDF）即达到最优性能。这进一步验证了架构创新本身的有效性——紧凑的空间表示降低了对大规模增强数据的依赖，使MLLM能够更高效地学习导航策略。

## 整体框架

GA-VLN 的整体设计围绕一个核心洞察展开：**将稠密 RGB 视频 token 替换为紧凑的几何感知 BEV 表示**，从而在保留三维空间结构的同时大幅降低视觉 token 数量。整个框架由三个关键阶段构成——视觉编码与深度投影、隐式几何先验注入、BEV 聚合与 MLLM 决策。

### 输入与视觉编码

系统在每个导航步接收 **RGB-D 前视图**（60° 视场角）以及历史帧序列。RGB 图像通过冻结的视觉编码器 **SigLIP** 提取 patch 级特征，深度图则被重采样到与 patch 网格对齐的分辨率，用于后续的 3D 空间投影（Section 3.2）。

### GA-BEV 表示的构建

GA-BEV 的构建是框架的核心创新，由两条互补路径组成（Figure 2）：

![[assets/figures/papers/paper_list_l2157_https_arxiv_org_abs_2605_22036/figures/002_Figure_2.jpg]]
*Figure 2: Overview of the proposed Geometry-Aware Vision-Language Navigation (GA-VLN) framework. Given RGB-D current and historical front views, our method constructs a Geometry-Aware BEV (GA-BEV) representation by combining explicit depth-guided projections with implicit geometry priors from a pretrained 3D foundation model. The projected features are aggregated into BEV grid cells to form compact and spatially expressive tokens. These BEV tokens, together with current-view features and instruction embeddings, are fed into the multimodal large language model (MLLM) to predict navigation actions*

**显式深度引导投影**：利用深度图和相机内外参，将每个 2D patch 中心点反投影到以智能体为中心的世界坐标系：

$$\hat{\mathbf{p}}_t(u,v) = \left[ R_t \quad \mathbf{p}_t \right] K^{-1} \left[ \begin{array}{l} u \\ v \\ 1 \end{array} \right] D_t(u,v)$$

其中 $R_t$、$\mathbf{p}_t$ 为相机旋转与位置，$K$ 为内参矩阵，$D_t(u,v)$ 为对应深度值。投影后的 3D 点携带其对应的视觉特征，按 $(x,z)$ 坐标落入预定义的 BEV 网格（网格尺寸 0.25 米，范围 $[-10\text{m}, 10\text{m}]$）。

**隐式 3D 几何先验**：历史图像序列 $\{I_1, \dots, I_t\}$ 通过冻结的预训练 3D 基础模型 **VGGT-1B** 编码，提取其倒数第二层特征：

$$V^g = f_{\mathrm{3DFM}}(\{I_1, \dots, I_t\}) \in \mathbb{R}^{t \times H_g \times W_g \times d_g}$$

随后通过一个 **2 层 MLP**（Linear–GeLU–Linear，隐藏层维度 4096）将特征维度对齐到视觉编码器输出维度：

$$\tilde{V^g} = f_{\mathrm{project}}(V^g) \in \mathbb{R}^{t \times H_g \times W_g \times d_p}$$

VGGT-1B 的大规模 3D 预训练提供了强大的形状先验和结构连续性，弥补了单视角深度投影在遮挡区域的信息缺失。

### BEV 聚合与 token 压缩

将显式投影特征与隐式几何特征在 3D 空间中对齐后，按 BEV 网格单元进行聚合。对落入网格 $(i,j)$ 的特征点集合 $\mathcal{S}_{i,j}$ 执行**均值池化**，并加上正弦位置编码：

$$B = \{ \frac{1}{|\mathcal{S}_{i,j}|} \sum_{v \in \mathcal{S}_{i,j}} v + e_{i,j} \mid |\mathcal{S}_{i,j}| \in [1,N] \}$$

**仅保留非空网格单元**，使得最终 BEV token 数量远小于 $N \times N$ 全网格尺寸，也远小于原始视觉 patch 集合 $t \times H_p \times W_p$。典型配置下，token 数从 4003 降至 394（约一个数量级），这是推理加速的根本原因（Table 3）。

### MLLM 集成与动作预测

GA-BEV 表示与当前视图特征、语言指令嵌入一同输入多模态大语言模型 **LLaVA-Video-7B**。采用**两轮对话生成**策略（Section 3.3）：
- **第一轮**：根据语言指令 $L$、BEV 特征 $B$ 和当前视图 $V_t$ 预测 4 个离散动作 $A_t$；
- **第二轮**：复用 $B$，仅更新当前视图 $V_{t+1}$，结合第一轮输出 $A_t$ 继续预测下 4 个动作 $A_{t+1}$。

BEV 表示每 **8 个动作**更新一次，在效率与精度之间取得最优平衡（Table 7）。离散动作空间包括前进 0.25m、左转/右转 15°、停止等，两轮对话共输出 8 步动作。

### 关键设计选择

| 模块 | 选择 | 原因 |
|------|------|------|
| 视觉编码器 | SigLIP（冻结） | 提供高质量的 patch 特征，无需微调 |
| 深度投影 | 显式反投影到世界坐标 | 建立 2D 特征与 3D 空间的确定性映射 |
| 3D 基础模型 | VGGT-1B（冻结） | 大规模 3D 预训练提供强几何先验 |
| 特征融合 | 全局均值池化 | 优于分层池化（SR 53.56 vs 50.57，Table 6） |
| BEV 更新间隔 | 每 8 步 | 效率-精度 Pareto 最优（Table 7） |
| 训练数据 | 仅高质量导航数据 | 无需 DAgger 增强或 VQA 混合训练 |

### 数据流总结

```
RGB-D 帧序列 → SigLIP 编码 → patch 特征
                              ↓
深度图 + 相机参数 → 3D 反投影 → BEV 网格聚合 ─┐
                                              ├→ GA-BEV tokens → MLLM → 动作序列
历史帧序列 → VGGT-1B → MLP 投影 → 几何先验 ─┘
```

这一设计使得 GA-VLN 在保持紧凑 token 预算的同时，具备显式的空间推理能力，为后续在三个 VLN-CE 基准上取得最优性能奠定了基础。

## 核心模块与公式推导

GA-VLN 的核心架构围绕一个关键设计展开：将传统 MLLM 导航中稠密的 RGB 视频 token 替换为紧凑的**几何感知 BEV（GA-BEV）表示**。该表示由三个紧密耦合的模块构建，最终通过两轮对话机制驱动动作预测。

### 3.1 显式深度引导的空间投影

给定当前时刻 $t$ 的 RGB 图像 $I_t$ 和深度图 $D_t$，视觉编码器（SigLIP）首先提取 patch 级特征。对于每个 patch 中心像素 $(u, v)$，利用深度值和相机参数将其反投影到 3D 世界坐标系：

$$\hat{\mathbf{p}}_t(u,v) = \left[ R_t \quad \mathbf{p}_t \right] K^{-1} \left[ \begin{array}{l} u \\ v \\ 1 \end{array} \right] D_t(u,v)$$

其中 $K$ 为相机内参矩阵，$R_t$ 和 $\mathbf{p}_t$ 分别为智能体在时刻 $t$ 的旋转矩阵和世界坐标位置。该公式将 2D 视觉特征显式地“提升”到 3D 空间，赋予每个 patch 特征明确的空间位置，这是构建 BEV 表示的基础。

### 3.2 隐式 3D 几何先验注入

为弥补单帧深度投影在遮挡区域和结构连续性上的不足，GA-VLN 引入一个冻结的预训练 3D 基础模型 VGGT-1B 来提取多视图几何特征。给定历史图像序列 $\{I_1, \dots, I_t\}$，该模型输出隐式编码了 3D 结构先验的特征：

$$V^g = f_{\mathrm{3DFM}}(\{I_1, \dots, I_t\}) \in \mathbb{R}^{t \times H_g \times W_g \times d_g}$$

随后通过一个两层 MLP（Linear–GeLU–Linear，隐藏层维度 4096）将特征维度对齐到视觉编码器的输出维度 $d_p$：

$$\tilde{V}^g = f_{\mathrm{project}}(V^g) \in \mathbb{R}^{t \times H_g \times W_g \times d_p}$$

VGGT-1B 的大规模 3D 预训练提供了强大的形状先验和结构连续性信息，与显式深度投影形成互补：前者提供精确的局部 3D 定位，后者补充全局几何上下文。

### 3.3 BEV 聚合与 GA-BEV 表示

将显式投影特征与隐式几何特征在 3D 空间中合并后，GA-VLN 以智能体为中心构建 BEV 网格。网格覆盖范围为 $[-10\text{m}, 10\text{m}]$，单元格大小 $\Delta = 0.25\text{m}$。对于 BEV 网格单元 $(i, j)$，定义落入其中的特征点集合：

$$\mathcal{S}_{i,j} = \big\lbrace v_k \in \mathcal{V} \mid \hat{\mathbf{p}}_k^x \in [-R + i\Delta, -R + (i+1)\Delta), \hat{\mathbf{p}}_k^z \in [-R + j\Delta, -R + (j+1)\Delta) \big\rbrace$$

对每个非空网格单元进行均值池化，并加上正弦位置编码 $e_{i,j}$，形成最终的 GA-BEV 表示：

$$B = \left\{ \frac{1}{|\mathcal{S}_{i,j}|} \sum_{v \in \mathcal{S}_{i,j}} v + e_{i,j} \mid |\mathcal{S}_{i,j}| \in [1,N] \right\}$$

关键设计在于**仅保留非空网格单元**，这使得 GA-BEV 的 token 数量远小于 $N \times N$ 的理论上限，甚至少于原始视觉 patch 总数。实验表明，GA-BEV 将视觉 token 数从 4003 降至 394（约一个数量级），同时显著提升导航性能（Table 3）。

### 3.4 两轮对话动作预测

GA-BEV 表示构建完成后，与语言指令嵌入 $L$ 和当前视角特征 $V_t$ 一同送入 MLLM（LLaVA-Video-7B）。动作预测采用两轮对话格式，每轮预测 4 个离散动作：

**第一轮：**
$$A_t = f_{\mathrm{MLLM}}(L, B, V_t)$$

**第二轮：**
$$A_{t+1} = f_{\mathrm{MLLM}}(L, B, V_t, A_t, V_{t+1})$$

第二轮复用相同的 BEV 表示 $B$，仅更新当前视角特征 $V_{t+1}$，从而在保持空间记忆的同时降低推理开销。BEV 表示每执行 8 个动作后更新一次，在效率与精度之间取得最佳平衡（Table 7）。消融实验证实，该两轮机制相比逐帧预测大幅减少了 MLLM 调用次数，是推理延迟从 342.9ms 降至 258.7ms 的关键因素之一（Table 2）。

### 补充图表

![[assets/figures/papers/paper_list_l2157_https_arxiv_org_abs_2605_22036/figures/001_Figure_1.jpg]]
*Figure 1: Illustration of different representations for VLN. (A) Dense image-based representations contain heavy token redundancy and lack explicit spatial structure. (B) Our Geometry-Aware BEV (GA-BEV) representation combines explicit depth-projected features with implicit geometry priors from 3D foundation models, producing a highly compact yet spatially expressive representation tailored for VLN*

## 实验与分析

### 核心实验设置

GA-VLN在三个标准视觉语言导航基准上进行评估：**R2R-CE**、**RxR-CE**和**NavRAG-CE**的val unseen划分。所有实验采用单目前视RGB-D观测（60°视野），不使用全景图或额外传感器。训练数据仅包含高质量导航数据集——R2R-CE（10,819条）、RxR-CE（19,990条）、EnvDrop（146,304条）、ScaleVLN（155,098条）和SRDF（319,022条），**未使用DAgger增强数据或通用VQA混合训练**，确保与基线方法的对比公平性。视觉编码器采用SigLIP，3D基础模型使用冻结的**VGGT-1B**，提取其倒数第二层特征后经2层MLP（Linear–GeLU–Linear，隐藏层维度4096）投影对齐。BEV网格单元尺寸为0.25米，范围[-10m, 10m]。

### 主要结果

Table 1展示了GA-VLN与现有方法在三个基准上的全面对比。在**R2R-CE val unseen**上，GA-VLN取得NE 4.80、OSR 67.6、SR 61.0、SPL 55.2，在所有指标上超越对比方法。相比最强的图像基MLLM方法**InternVLA-N1**（SR 58.2, SPL 54.0），SR提升2.8个百分点，SPL提升1.2个百分点；相比使用DAgger增强的**NaVILA**（SR 55.8, SPL 53.0），优势更为显著。在**RxR-CE val unseen**上，GA-VLN以SR 55.4、SPL 45.2取得领先，OSR达到67.0，超越InternVLA-N1（SR 46.1）达9.3个百分点。在更具挑战性的**NavRAG-CE**基准上，GA-VLN的SR为22.2，与**MapNav**（SR 24.7）接近，但NE从8.12降至7.88，路径效率更优。值得注意的是，GA-VLN是Table 1中唯一不使用DAgger增强即达到该性能水平的方法，其数据效率显著优于依赖额外行为克隆数据的方案。

### 消融实验：GA-BEV表示的有效性

Table 2的消融实验系统验证了GA-BEV两大核心组件的贡献。以纯图像MLLM基线（#1）为起点，其使用稠密RGB patch tokens，SR仅51.49，推理延迟342.9ms，单步计算量32.19 TFLOPs。引入**显式深度引导BEV投影**（#2, BEV Rep.）后，SR跃升至59.21（+7.72），同时推理延迟降至212.9ms（-38%），计算量降至5.15 TFLOPs（-84%），验证了BEV表示在压缩冗余token和注入空间结构方面的双重收益。进一步融入**隐式3D几何先验**（#3, 3D-Geo.）后，SR达到60.96，SPL提升至55.19，延迟仅小幅增加至258.7ms。这表明显式投影与隐式先验**高度互补**：前者提供精确的深度引导空间定位，后者从大规模3D预训练中带来场景结构连续性和形状先验。

### Token效率与空间分辨率权衡

Table 3深入分析了GA-BEV的token压缩机制。在无SRDF数据训练的受控条件下，纯RGB表示（#1）需4003个视觉token，SR为46.49；切换为GA-BEV后（#2），token数骤降至394（约一个数量级），SR提升至51.50（+5.01）。这一结果直接证实了核心机制：**通过将稠密2D patch token替换为仅保留非空网格单元的BEV表示，在大幅降低MLLM推理负担的同时改善了空间推理质量**。简单将深度图与RGB通道拼接（RGB-Depth, Table 8）反而导致token翻倍至8006且SR降至38.61，凸显了GA-BEV投影策略的不可替代性。

![[assets/figures/papers/paper_list_l2157_https_arxiv_org_abs_2605_22036/figures/013_Table_8.jpg]]
*Table 8: Ablation on different depth processing strategies*

BEV网格粒度方面（Table 3 #4-#5），更细的0.125m网格（token数增至516）相比0.25m网格（394 tokens）SR仅从51.50变为51.49，收益饱和，表明0.25m在精度与效率间取得良好平衡。BEV步长范围消融（#6-#8）显示8步更新一次为最优（SR 51.50），更频繁的更新（4步）增加计算开销但无性能增益。Figure 6进一步展示了不同配置下token数随导航步数的增长曲线，GA-BEV配置的token增长远缓于纯图像基线，验证了其在长距离导航中的可扩展性。

![[assets/figures/papers/paper_list_l2157_https_arxiv_org_abs_2605_22036/figures/005_Table_3.jpg]]
*Table 3: Analysis of token efficiency and spatial resolution trade-offs of GA-BEV. The experiments compare different visual representations (rows 1–3), BEV grid size (rows 4–5), and BEV step range (rows 6–8). “Token Num” denotes the total visual tokens fed into the fMLLM. Unlike Table 2, all models in this table are trained without incorporating the SRDF dataset to reduce computational overhead*

![[assets/figures/papers/paper_list_l2157_https_arxiv_org_abs_2605_22036/figures/015_Figure_6.jpg]]
*Figure 6: Comparison of token usage across navigation steps for different configurations. The number shows in each legend corresponds to the configuration of the respective row in Table 3. The shaded area in the figure indicates the variance range of the sample data*

### 训练数据与辅助任务分析

Table 5的数据组成消融揭示了一个重要的分布偏移问题：在R2R-CE和RxR-CE上，加入NavRAG-CE训练数据反而损害性能（R2R-CE SR从60.96降至58.92，RxR-CE SR从55.4降至52.8），仅在NavRAG-CE自身任务上带来收益（SR从17.0升至22.2）。这表明不同VLN数据集之间存在场景分布和指令风格的差异，混合训练需谨慎权衡。

Table 9考察了引入导航VQA辅助任务的影响：添加Nav-VQA后SR从60.96微降至59.92，说明**导航数据本身已提供足够的多模态对齐信号**，额外VQA任务并非必需。这一发现与GA-VLN不使用通用VQA数据即可达到SOTA的结果一致。

### 推理效率与鲁棒性

Table 4评估了传感器噪声鲁棒性：在深度噪声标准差为0.1m时，SR从60.96仅降至59.83；噪声增至0.2m时SR为58.55，退化幅度有限，表明GA-BEV中的均值池化聚合和3D几何先验提供了天然的噪声平滑能力。

Table 6对比了BEV特征融合策略：全局均值池化（SR 53.56）优于分层均值池化（SR 50.57），说明在BEV网格内直接聚合所有投影特征比先按帧聚合再跨帧融合保留了更丰富的空间信息。

### 失败模式与局限

尽管GA-VLN在基准测试中表现优异，论文报告了以下关键局限：

1. **避障能力缺失**：零样本实机部署时，由于框架未集成显式避障模块，智能体偶尔贴近墙壁行走，路径安全性不足。这在Figure 3的真实世界示例中有所体现。
2. **离散动作粒度**：当前动作空间为离散的4动作预测（前进、左转、右转、停止），导致停止位置不够精确，在需要精细操控的场景中表现受限。
3. **数据集分布偏移**：如前所述，NavRAG-CE的引入损害了R2R-CE和RxR-CE的泛化性能，说明训练数据的选择对模型行为有显著影响。
4. **未使用DAgger增强**：虽体现了高数据效率，但在某些困难场景（如长指令、复杂拓扑）中，缺乏在线纠正数据可能导致导航鲁棒性有限。

### 补充图表

![[assets/figures/papers/paper_list_l2157_https_arxiv_org_abs_2605_22036/figures/003_Table_1.jpg]]
*Table 1: Comparison with state-of-the-art VLN methods on R2R-CE, RxR-CE, and NavRAG-CE val unseen benchmarks. “System” groups methods into modular planners, 3D end-to-end agents, and Image-based MLLM agents, while “DAgger” indicates the use of DAgger augmentation data*

![[assets/figures/papers/paper_list_l2157_https_arxiv_org_abs_2605_22036/figures/004_Table_2.jpg]]
*Table 2: Ablation study of Geometry-Aware BEV representation and efficiency comparison per inference step*

![[assets/figures/papers/paper_list_l2157_https_arxiv_org_abs_2605_22036/figures/007_Table_4.jpg]]
*Table 4: Robustness to Sensor Noise on R2R-CE val unseen*

![[assets/figures/papers/paper_list_l2157_https_arxiv_org_abs_2605_22036/figures/010_Table_5.jpg]]
*Table 5: Ablation on training data composition across R2R-CE, RxR-CE, and NavRAG-CE benchmarks*

![[assets/figures/papers/paper_list_l2157_https_arxiv_org_abs_2605_22036/figures/011_Table_6.jpg]]
*Table 6: Comparison of BEV feature fusion strategies*

![[assets/figures/papers/paper_list_l2157_https_arxiv_org_abs_2605_22036/figures/012_Table_7.jpg]]
*Table 7: Ablation on BEV update interval w/o 3D geometry priors*

![[assets/figures/papers/paper_list_l2157_https_arxiv_org_abs_2605_22036/figures/006_Figure_3.jpg]]
*Figure 3: An example of the GA-VLN real-world result*

## 方法谱系与知识库定位

### 1. 方法谱系：从稠密图像MLLM到几何感知BEV

GA-VLN的核心定位是**基于MLLM的VLN方法中视觉表示范式的转换**，其方法谱系可从三个维度理解。

**与基于图像的MLLM导航方法的关系。** 现有主流方法将VLN建模为MLLM的多模态序列预测任务，直接输入稠密RGB视频帧的patch token序列。**NaVid**（Zhang et al., arXiv 2024）和**Uni-NaVid**（Zhang et al., arXiv 2024b）使用视频VLM进行导航，**NaVILA**（Cheng et al., arXiv 2024）将其扩展到连续环境，**StreamVLN**（Wei et al., arXiv 2025）引入慢-快上下文建模以处理历史帧，**InternVLA-N1**（InternNav Contributors, 2025）则基于InternNav平台构建。这些方法的共同瓶颈在于：每帧产生 $H_p \times W_p$ 个视觉token，多帧累积后token数线性增长，且缺乏显式三维空间结构。GA-VLN的突破在于**将“稠密RGB patch token序列”替换为“紧凑的BEV空间token集合”**，从根本上改变了MLLM的视觉输入接口——从无结构的像素网格变为有结构的空间网格，同时将token数量降低约一个数量级（从4003降至394，Table 3）。

**与3D端到端智能体的关系。** Table 1的“System”分组将方法分为模块化规划器、3D端到端智能体和基于图像的MLLM智能体三类。GA-VLN虽然属于MLLM智能体范畴，但其BEV表示引入了3D端到端方法的空间推理能力——通过深度引导的显式投影和3D基础模型的隐式先验，在MLLM内部构建了以智能体为中心的空间表征，弥合了两类方法之间的鸿沟。

**与BEV表示在自动驾驶中的关系。** BEV表示在自动驾驶领域已被广泛验证，但将其引入VLN面临独特挑战：VLN是单目前视、离散动作、室内环境的设置，观测范围有限且需要语言-空间联合推理。GA-VLN的贡献在于**将BEV表示适配到MLLM的token化接口**——通过均值池化聚合和非空网格筛选，使BEV token可以直接作为MLLM的输入，无需额外的跨模态对齐模块。

### 2. 关键技术决策的谱系定位

**深度信息处理策略的演进。** Table 8揭示了深度处理策略的性能差异：简单将深度图与RGB通道拼接（RGB-Depth）导致token加倍（8006个）且性能下降（SR 38.61 vs RGB-Only的46.49），说明**深度信息的价值不在于增加数据量，而在于提供空间结构**。GA-VLN的深度引导投影（Eq. 1）将深度从“额外的像素通道”转化为“空间坐标变换的媒介”，这一设计决策是BEV表示能够压缩token而不损失空间信息的关键。

**3D基础模型先验的引入。** GA-VLN使用冻结的VGGT-1B（3D foundation model）提取多视图几何特征，通过MLP投影后与视觉特征在BEV网格内融合。这一设计与端到端训练3D特征提取器的方法不同：冻结的大规模预训练模型提供了**数据高效的结构先验**，使得在有限导航数据下（Table 3，无SRDF时SR从46.49→51.50→53.56）仍能稳定提升。这一定位与“基础模型+任务适配”的范式一致。

**两轮对话决策机制。** 传统MLLM导航每次预测一个动作，GA-VLN采用两轮对话每轮预测4个动作、每8步更新BEV的设计（Table 7验证了8步更新的最优平衡）。这一设计在**推理效率与空间信息新鲜度之间取得折中**：BEV复用降低了MLLM调用频率，而定期更新保证了空间表征的时效性。

### 3. 适用边界与局限

**传感器配置边界。** GA-VLN依赖单目前视RGB-D输入（60°视场角），不依赖全景相机或额外传感器。这一设置与标准VLN-CE基准一致，但在需要全向感知的场景（如窄道后退、侧向避障）中存在感知盲区。Table 4的传感器噪声鲁棒性实验表明方法对深度噪声有一定容忍度，但极端噪声下的表征退化程度尚需进一步验证。

**动作空间粒度限制。** 离散动作空间（前进、左转、右转、停止等）的粗粒度导致停止位置不够精确，这是VLN-CE基准的固有局限。论文未探索连续动作空间下的扩展。

**训练数据分布偏移。** Table 5显示，引入NavRAG-CE训练数据会损害R2R-CE和RxR-CE的泛化性能，表明不同VLN基准之间存在**数据集分布偏移**，GA-VLN的BEV表示未能完全消除这种跨数据集的负迁移。

**零样本部署的安全性。** 实机部署时因缺少避障模块，智能体偶尔贴近墙壁行走，路径安全性不足。这说明GA-BEV表示虽然提供了空间结构，但**未显式编码可通行区域或障碍物信息**，需要额外的安全层。

**DAgger增强的缺失。** GA-VLN未使用DAgger增强，虽然数据效率高，但在某些困难场景（如长距离导航、复杂指令）可能导航鲁棒性有限。这一定位使其更接近“数据高效”方法而非“最大鲁棒性”方法。

### 4. 开放问题

1. **两轮对话格式的推理延迟优化。** 两轮对话机制在实际部署中对端到端推理延迟的影响如何？是否可以通过KV缓存复用或异步BEV更新进一步优化？

2. **旋转步角的定量影响。** 论文提到实机部署时调整为15°旋转步角，但未报告该调整对定量成功率的影响。更细粒度的旋转动作是否能在BEV表示下带来显著收益？

3. **连续动作空间与动态障碍的泛化。** GA-VLN能否泛化到连续动作空间（如速度控制、曲线路径）或包含动态障碍的环境？BEV表示对动态物体的建模能力是开放的。

4. **3D基础模型预训练数据分布的适配性。** VGGT-1B的大规模预训练数据分布（可能以室外/通用场景为主）对室内导航特定场景（如狭窄走廊、家具遮挡）的适配性如何？是否需要领域内微调？

5. **BEV表示的遮挡补全能力。** 当深度噪声较大或存在严重遮挡时，BEV表示的空间结构退化程度如何？是否可以通过多帧融合或不确定性建模来增强鲁棒性？

6. **与模块化规划方法的融合潜力。** GA-BEV表示作为紧凑的空间token，是否可以与显式地图构建、路径规划等模块化方法融合，形成端到端与模块化的混合架构？

## 原文 PDF

![[paperPDFs/CVPR_2026/GA_VLN_Geometry_Aware_BEV_Representation_for_Efficient_Vision_Language_Navigation.pdf]]