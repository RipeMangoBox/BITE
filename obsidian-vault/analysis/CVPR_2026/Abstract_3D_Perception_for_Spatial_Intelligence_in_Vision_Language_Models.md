---
title: Abstract 3D Perception for Spatial Intelligence in Vision-Language Models
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/Abstract_3D_Perception_for_Spatial_Intelligence_in_Vision_Language_Models.pdf
project_link: null
code_link: null
aliases:
- A3PSIVLM
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
core_operator: SandboxVLM通过向VLM注入任务相关的抽象3D边界框表示，弥补了2D到3D的模态鸿沟。
primary_logic: 受人类抽象感知启发，仅使用粗粒度的符号化3D结构（而非精确几何重建）即可显著提升VLM的零样本空间推理能力，无需额外训练。
claims:
- SandboxVLM在SAT-Real基准上相比基线方法取得8.3%的性能提升。
- 在多个空间智能基准上，SandboxVLM平均准确率达81.4%，超越GPT-5-mini 2.9%。
- 消融研究表明，完整SandboxVLM在SAT-Real上达到84.1%准确率，相比原始VLM提升8.7%。
- SAT-Real 上 平均准确率 = 84.1
---

# Abstract 3D Perception for Spatial Intelligence in Vision-Language Models

> [!tip] 核心洞察
> 受人类抽象感知启发，仅使用粗粒度的符号化3D结构（而非精确几何重建）即可显著提升VLM的零样本空间推理能力，无需额外训练。

| 字段 | 内容 |
|------|------|
| 中文题名 | 面向视觉语言模型空间智能的抽象3D感知 |
| 英文题名 | Abstract 3D Perception for Spatial Intelligence in Vision-Language Models |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2511.10946) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction |
| Method | SandboxVLM |
| Dataset | SAT-Real, PhysBench, Spatial-Avg |

> [!tip] 效果简介
> - SAT-Real 上，平均准确率 84.1 vs 75.4 (+8.7%)；平均准确率 77.7 vs 60.3 (+17.4%)。
> - PhysBench 上，准确率 58.3 vs 54.9 (+3.4%)。
> - Spatial-Avg 上，平均准确率 81.4 vs 78.5 (+2.9%)。

## 概述

现有视觉语言模型（VLM）在训练过程中普遍缺乏3D感知能力，其2D训练范式与3D空间推理任务之间存在显著的模态鸿沟。直接通过监督微调注入3D知识面临3D数据匮乏和灾难性遗忘的双重困境。受人类通过粗粒度关系理解进行高效空间推理的启发，**SandboxVLM**提出了一种无需训练即可为VLM注入抽象3D结构的新范式。

**核心思想**：仅使用一组紧凑的抽象3D定向边界框（oriented bounding boxes）来表示场景的空间布局与物理动态，丢弃低层视觉细节，从而弥合2D到3D的模态鸿沟。这一设计使VLM能够在零样本条件下进行空间推理，无需任何额外训练。

**方法定位**：SandboxVLM是一个模块化的训练无关框架，包含四个阶段——基于抽象控制的多视图先验生成、代理提升（Proxy Elevation）、多视图投票与聚类（Multi-View Voting and Clustering）、以及3D感知推理。它通过轻量级的2D到3D代理反投影，将任务相关的符号化3D结构注入现有VLM，区别于需要密集3D监督或架构修改的现有方法。

**关键结果**：在SAT-Real基准上，SandboxVLM相比基线方法取得8.3%的性能提升，在多个空间智能基准上的平均准确率达到81.4%，超越GPT-5-mini 2.9%。消融实验证实，完整的3D Sandbox表示相比原始VLM在SAT-Real上提升8.7%（84.1% vs 75.4%），验证了抽象边界框作为空间推理上下文的有效性。

## 背景与动机

### 问题背景：VLM的2D训练范式与3D空间推理的鸿沟

视觉语言模型（VLM）在图像理解、视觉问答等任务上取得了显著进展，但其核心训练范式仍以2D为中心——模型从大规模图像-文本对中学习视觉与语言的关联，缺乏对三维空间结构的显式建模。这种2D训练模式与日益增长的3D空间推理需求之间存在根本性的模态鸿沟：当面对“从我的视角看，左边的物体比右边的更近吗？”这类需要空间感知的查询时，VLM必须从单张2D输入中隐式推断深度、遮挡和相对位置关系，而缺乏直接可用的3D信息。

现有尝试弥合这一鸿沟的方案主要分为两类。第一类是通过监督微调（SFT）向VLM注入3D知识，例如**VeBrain-8B**、**Magma-8B**、**Robix-32B-Base**等训练方法。然而，这类方法受限于3D标注数据的稀缺性，且微调过程可能导致灾难性遗忘，削弱模型原有的通用视觉理解能力。第二类是测试时缩放方法，如**MindJourney**，通过多步推理链增强空间推理，但本质上仍依赖VLM从2D输入中“猜测”3D结构，缺乏显式的空间表征。

### 核心洞察：人类抽象感知的启示

本文的动机源于对人类空间推理方式的观察。如图1所示，人类在理解三维场景时并不需要精确的度量重建——我们不会在脑海中构建每个物体的精确点云或网格模型。相反，人类依赖一种**粗粒度的、关系性的抽象感知**：我们大致知道物体的相对位置（“杯子在桌子上面，偏左”）、尺寸和朝向，并能据此进行高效的空间推理。

这一观察揭示了关键洞察：**仅使用粗粒度的符号化3D结构，而非精确的几何重建，即可显著提升VLM的零样本空间推理能力，且无需额外训练。** 具体而言，如果能为VLM提供任务相关的抽象3D边界框——即用简单的定向长方体表示场景中关键物体的空间占据和排列关系——就可能以最小的信息负载弥补2D到3D的模态鸿沟，同时避免低层视觉细节的干扰。

### 方法动机：SandboxVLM的设计哲学

基于上述洞察，SandboxVLM提出了一种**免训练框架**，通过向现有VLM注入符号化3D结构来实现零样本空间推理增强。其设计哲学包含三个关键原则：

1. **抽象而非精确**：仅构建粗粒度的3D边界框表示，而非密集的深度图、点云或网格。这种抽象表示既保留了空间推理所需的核心几何信息，又过滤了纹理、光照等无关细节，降低了VLM的认知负荷。

2. **任务相关性驱动**：3D重建并非无差别地进行，而是由VLM根据输入查询动态识别任务相关物体，仅对这些物体进行3D提升和建模。这种选择性机制避免了全场景重建的计算开销和噪声干扰。

3. **多视图先验增强**：单张图像提供的3D信息天然不足。SandboxVLM利用视频扩散模型生成多视图序列，通过跨视图一致性约束提升3D估计的可靠性，模拟了人类从多角度观察场景的认知过程。

这一设计使得SandboxVLM能够作为一个即插即用的3D感知模块，与GPT-4o、GPT-5-mini、Claude-Sonnet-4、Gemini-2.5-Pro等主流VLM无缝集成，在不修改模型参数的前提下显著提升其空间智能水平。

## 核心创新

SandboxVLM 的核心创新在于**不修改 VLM 参数、不引入稠密 3D 监督**的前提下，通过向现有 VLM 注入任务相关的**抽象 3D 边界框表示**，弥合了 2D 训练模式与 3D 空间推理之间的模态鸿沟。这一思路受人类抽象感知启发：人类在 3D 空间中有效推理，依赖的并非精确的度量几何，而是粗粒度的、关系性的空间理解（Figure 1）。SandboxVLM 将这一原则具象化为四个关键的 changed slots，每个 slot 都相对于基线方法引入了结构性改变。

### 从 2D 图像到抽象 3D 上下文表示

**核心改变**：基线 VLM 仅接收原始 2D 图像作为输入，缺乏任何显式的 3D 结构信息。SandboxVLM 则将场景表示为从多视图重建获得的**渲染抽象 3D 边界框**（Table 3），为 VLM 提供了可解释的空间布局线索，同时过滤掉与任务无关的低层视觉细节。

这一改变的因果效应在消融实验中得到了直接验证：完整 SandboxVLM 在 SAT-Real 上达到 84.1% 准确率，而移除 3D 抽象表示、仅使用多视图图像（设置 3）后性能下降至 78.7%（Table 3）。更关键的是，以文本形式提供 3D 坐标（设置 5）仅获得 80.8%，显著低于视觉 Sandbox 的 84.1%，表明**视觉模态的抽象 3D 表示**对空间推理具有不可替代的优势——VLM 更擅长从渲染的几何结构中“读取”空间关系，而非从数值坐标中推断。

### 多视图先验生成：从单帧到多视角序列

**核心改变**：基线方法仅使用单张输入图像进行推理。SandboxVLM 引入**视频扩散先验**（video diffusion prior），根据 VLM 生成的抽象相机运动控制（`left, fwd-left, fwd, fwd-right, right`），将输入图像扩展为短多视图序列（Sec 3.2）：

$$\{ X_v^{(m),t} \}_{t=0}^{T-1} = G_{\theta} \Big( I_v, \{ \hat{\mathbf{T}}_v^{(m),t} \}_{t=0}^{T-1} \Big)$$

这一改变的本质是为后续的 3D 重建提供**多视角信息源**。消融中，使用场景图文本提示（设置 2）仅获得 77.0%，远低于完整模型，说明仅靠关系图无法替代从多视图先验中提取的显式 3D 结构。

### 对象选取与 3D 提升：任务驱动的稀疏代理

**核心改变**：基线方法对场景中的所有信息一视同仁，不区分任务相关与无关对象。SandboxVLM 通过**代理提升模块**（Proxy Elevation）实现了任务驱动的稀疏化：VLM 首先识别查询相关的对象类别及其像素中心 $\hat{O}_{v,i} = ( \hat{o}_i, [x_i, y_i] )$，SAM 据此生成实例掩码，经腐蚀与最远点采样（FPS）后，选取 $N_{\mathrm{pts}}$ 个内部代理点，再通过深度估计提升到 3D 空间（Figure 3a）。

这一设计的精妙之处在于**稀疏性与任务相关性**：仅提升与查询相关的对象代理点，而非对整个场景进行稠密重建，既降低了计算开销，又避免了无关几何噪声对 VLM 推理的干扰。

### 多视图一致性融合：从噪声点到结构化边界框

**核心改变**：单视图提升的 3D 代理点天然带有噪声（深度估计误差、分割不精确等）。SandboxVLM 通过**多视图投票与聚类**（Multi-View Voting and Clustering, MVC）机制，将跨视图的代理点聚合为定向 3D 边界框（Figure 3b）。其核心是一致性函数：

$$\mathrm{Agree}(\mathbf{p}, X_v^{(m),t}) = \begin{cases} 1, & \text{if } \exists \mathbf{p}' \in S'^{(m),t} \text{ s.t. } \|\mathbf{p}' - \mathbf{p}\|_2 < \delta; \\ 0, & \text{otherwise} \end{cases}$$

仅当 3D 点在足够多的视图中获得一致性支持时，才被保留并参与 DBSCAN 聚类，最终拟合为定向边界框。消融实验证实了这一步的关键性：移除 MVC、直接使用渲染代理点（设置 6）导致性能骤降至 77.0%（Table 3），表明**结构化的 OBB 表示**远比稀疏点云更适合 VLM 的空间推理——边界框提供了清晰的体积与方位线索，而点云则缺乏这种可解释的结构。

### 创新本质：符号化 3D 结构的零样本注入

综合来看，SandboxVLM 的创新并非提出新的 VLM 架构或训练范式，而是在**推理时**构建了一个轻量级的 3D 沙盒层：通过视频扩散先验获取多视图信息，通过代理提升实现任务驱动的稀疏化，通过多视图投票与聚类生成结构化的抽象边界框，最终将这一符号化的 3D 表示注入 VLM 的推理上下文。整个过程无需任何训练或微调，所有模块均为现成模型的组合，使得该方法可以无缝适配不同的 VLM 骨干（GPT-4o、GPT-5-mini、GPT-5 等），在零样本设定下即取得一致的性能增益。

## 整体框架

SandboxVLM 是一个**免训练的零样本框架**，其核心思想是向现成的视觉语言模型（VLM）注入粗粒度的符号化 3D 结构信息，从而弥合 VLM 的 2D 训练模式与 3D 空间推理任务之间的模态鸿沟。该框架受人类抽象感知的启发——人类在 3D 推理时并不依赖精确的几何重建，而是通过粗粒度的关系性理解即可有效运作。SandboxVLM 遵循这一原则，为 VLM 提供紧凑且富含信息的抽象 3D 边界框上下文，同时丢弃低层视觉细节。

如图 2 所示，整个管道由**四个顺序模块**构成，形成一条从单张 2D 输入图像到 3D 感知推理输出的完整信息流：

1.  **视频扩散先验生成**：接收输入图像 $I_v$ 和文本查询 $q$，由 VLM 生成抽象相机运动控制信号，视频扩散模型 $G_{\theta}$ 据此将单张图像扩展为短多视图序列 $\{ X_v^{(m),t} \}_{t=0}^{T-1}$，为后续 3D 重建提供多视角先验。

2.  **代理提升模块**：VLM 从各视图中识别任务相关对象及其近似中心位置 $\hat{O}_{v,i} = (\hat{o}_i, [x_i, y_i])$，SAM 分割模型生成实例掩码，经腐蚀和最远点采样（FPS）选取 2D 代理点 $\mathcal{S}_{v,i}$，再通过现成的深度估计器将其提升到 3D 空间，形成粗粒度的 3D 代理点云。

3.  **多视图投票与聚类**：聚合来自多个视图的 3D 代理点，通过跨视图一致性检查函数 $\mathrm{Agree}(\mathbf{p}, X_v^{(m),t})$ 过滤不可靠点——仅当某 3D 点在足够多的视图中存在距离小于阈值 $\delta$ 的对应点时，才被视为可靠点。随后对可靠点集进行 DBSCAN 聚类，拟合出面向任务的定向 3D 边界框，形成结构化的“3D 沙盒”表示。

4.  **3D 感知推理**：从后撤视角和俯视视角渲染抽象 3D 边界框，将渲染图像与原始查询组合后再次送入 VLM，VLM 在 `<thinking>` 标签内进行文本推理，最终在 `<answer>` 标签中输出空间推理答案。

**关键设计选择**：与直接使用多视图图像或稀疏点云不同，SandboxVLM 选择将 3D 信息压缩为**抽象定向边界框**。消融实验表明，这一选择在信息量和可解释性之间取得了有效平衡——完整模型在 SAT-Real 上达到 84.1% 准确率，而仅使用多视图图像（无 3D 抽象表示）的变体下降至 78.7%，使用渲染代理点的变体下降至 77.0%，验证了结构化边界框表示的核心价值。

### 补充图表

![[assets/figures/papers/paper_list_l2367_https_arxiv_org_abs_2511_10946/figures/002_Figure_2.jpg]]
*Figure 2: Overview of the SandboxVLM pipeline. Given an input image and a textual query, the system builds a compact, 3D-aware, query-conditioned context for a vision-language model (VLM). A video diffusion prior first expands the input into a short multi-view sequence along imagined trajectories guided by abstract control provided by the VLM. Inside the 3D Sandbox module, an off-the-shelf depth estimator predicts per-frame depth and camera parameters, while the VLM identifies task-relevant objects that guide a 2D segmenter to produce instance masks. The masked regions are lifted into coarse 3D proxies and merged across views through a Multi-View Voting and Clustering step to form abstract 3D boundin...*

![[assets/figures/papers/paper_list_l2367_https_arxiv_org_abs_2511_10946/figures/001_Figure_1.jpg]]
*Figure 1: Motivation of SandboxVLM. (a) Existing VLMs are trained without 3D awareness. Training or supervised fine-tuning (SFT) VLMs with 3D suffers from a lack of 3D data and forgetting. (b) Humans, however, reason effectively in 3D through coarse, relational understanding. (c) SandboxVLM follows this principle of abstract perception, providing a coarse but informative 3D context for zero-shot VLM reasoning*

## 核心模块与公式推导

SandboxVLM 的核心设计思想是向 VLM 注入任务相关的抽象 3D 结构，而非追求精确的几何重建。整个管道由四个关键模块级联构成，每个模块解决从 2D 输入到 3D 推理链条中的一个瓶颈。

### 3.1 场景定义

给定一个 3D 场景，其输入为多视图 RGB 图像集合：

$$\mathcal{T} = \{ I_v \}_{v=0}^{V-1}$$

其中每个 $I_v \in \mathbb{R}^{H \times W \times 3}$，$v$ 索引不同视图。系统的目标是根据文本查询 $q$，从该图像集合中构建紧凑的 3D 感知上下文，供 VLM 进行零样本空间推理。

### 3.2 视频扩散先验生成

该模块的核心作用是将单张输入图像扩展为多视图序列，为后续 3D 重建提供信息先验。其关键创新在于**抽象控制机制**：VLM 根据查询 $q$ 从预定义的抽象相机运动集合中选择合适的轨迹，而非依赖精确的相机参数。

抽象相机运动集合定义为：

$$\mathcal{T} = \{ \mathrm{left, fwd\text{-}left, fwd, fwd\text{-}right, right} \}$$

这些语义化的运动方向（左、前左、前、前右、右）作为高层控制信号，引导视频扩散模型 $G_\theta$ 生成多视图序列：

$$\{ X_v^{(m),t} \}_{t=0}^{T-1} = G_{\theta} \Big( I_v, \{ \hat{\mathbf{T}}_v^{(m),t} \}_{t=0}^{T-1} \Big)$$

其中 $\hat{\mathbf{T}}_v^{(m),t}$ 为候选相机轨迹，$X_v^{(m),t}$ 为生成的 $T$ 帧多视图序列。这种抽象控制避免了精确相机标定的需求，同时保留了足够的 3D 几何线索。

### 3.3 代理提升模块

代理提升模块的任务是从 2D 图像中识别与查询相关的对象，并将其提升到 3D 空间。该过程分三步完成：

**步骤一：对象识别。** VLM $M_\psi$ 从输入图像 $I_v$ 和查询 $q$ 中识别任务相关对象：

$$\{ \hat{O}_{v,i} \} = M_{\psi} ( I_v, q )$$

每个识别结果为一个元组：

$$\hat{O}_{v,i} = ( \hat{o}_i, [x_i, y_i] )$$

其中 $\hat{o}_i$ 为对象类别名称，$[x_i, y_i]$ 为对象中心的像素坐标。这一步利用了 VLM 的语义理解能力来聚焦任务相关区域。

**步骤二：掩码生成与代理点采样。** 使用 SAM 等分割模型根据中心点提示生成对象实例掩码，然后对掩码进行腐蚀操作以消除边界噪声，最后在最远点采样策略下选取 $N_{\mathrm{pts}}$ 个内部代理点：

$$\mathcal{S}_{v,i} = \mathrm{FPS}( \mathbf{M}_{v,i}^{\mathrm{erode}}, N_{\mathrm{pts}} )$$

**步骤三：3D 提升。** 利用现成的深度估计器获取逐像素深度，结合相机参数将 2D 代理点反投影到 3D 空间，形成稀疏的 3D 代理点云。

### 3.4 多视图投票与聚类

由于单视图深度估计存在噪声，且不同视图间可能存在不一致，该模块通过跨视图一致性检查和聚类来构建可靠的 3D 表示。

**一致性函数**定义为：若 3D 点 $\mathbf{p}$ 在视图 $X_v^{(m),t}$ 中存在距离小于阈值 $\delta$ 的对应点 $\mathbf{p}'$，则认为该点与该视图一致：

$$\mathrm{Agree}(\mathbf{p}, X_v^{(m),t}) = \begin{cases} 1, & \text{if } \exists \mathbf{p}' \in S'^{(m),t} \text{ s.t. } \|\mathbf{p}' - \mathbf{p}\|_2 < \delta; \\ 0, & \text{otherwise} \end{cases}$$

一个 3D 点被视为可靠，当且仅当它与至少 $N$ 个视图达成一致。通过此投票机制，噪声点被有效滤除。随后对保留的可靠代理点应用 DBSCAN 聚类，并为每个聚类拟合定向 3D 边界框，形成结构化的抽象场景表示。

### 3.5 3D 感知推理

最终的推理阶段将抽象 3D 边界框从后撤视角和俯视视角进行渲染，生成清晰的空间布局图像。这些渲染图与原始查询组合后送入 VLM，VLM 按照以下模板进行文本推理后给出答案：

$$\begin{array} { l } { { < \mathrm { t h i n k i n g > ~ T h e ~ reasoning. ~ < / t h i n k i n g > ~ } } } \\ { { < \mathrm { a n s w e r > ~ T h e ~ final ~ answer. ~ < / a n s w e r > ~ } } } \end{array}$$

这种设计使 VLM 能够基于符号化的 3D 结构进行显式空间推理，同时避免了低层视觉细节的干扰。

### 补充图表

![[assets/figures/papers/paper_list_l2367_https_arxiv_org_abs_2511_10946/figures/003_Figure_3.jpg]]
*Figure 3: Core modules of 3D Sandbox. (a) Proxy Elevation: The VLM identifies task-relevant objects and their approximate locations. A segmentation model produces object masks, followed by mask erosion and farthest point sampling to select interior proxy pixels. (b) Multi-View Voting: The proxies are unprojected into 3D space and aggregated across views through a cross-view consistency check (“Agree to”) to filter unreliable points. The remaining proxies will be clustered into boxes*

## 实验与分析

### 主实验结果

SandboxVLM在四个空间推理基准上与三类基线方法进行了定量对比（Table 1）。整体上，SandboxVLM在空间基准上平均准确率达81.4%，超越GPT-5-mini 2.9个百分点，在PhysBench物理推理基准上超越测试时缩放方法MindJourney 3.4个百分点。这一结果的核心驱动力来自SAT-Real基准：以GPT-5-mini为骨干时，SandboxVLM达到84.1%，较基线（75.4%）提升8.7个百分点；以GPT-4o为骨干时提升幅度更大，从60.3%跃升至77.7%（+17.4个百分点），表明抽象3D表示对较弱VLM骨干的增益更为显著。

![[assets/figures/papers/paper_list_l2367_https_arxiv_org_abs_2511_10946/figures/004_Table_1.jpg]]
*Table 1: Quantitative comparison with three categories of baselines across four benchmarks evaluating spatial reasoning. Our SandboxVLM achieves the highest overall performance, particularly on SAT-Real and PhysBench, demonstrating strong generalization in real-world spatial and physical tasks*

Table 2进一步按空间推理维度拆分了SAT-Real和SAT-Synth上的表现。在SAT-Real的五个子维度（自我运动、物体运动、目标瞄准、动作后果、视角采择）上，SandboxVLM在GPT-5骨干下达到84.3%平均准确率，在GPT-5-mini下为84.1%，均取得最佳或次优结果。值得注意的是，在物体运动子任务上SandboxVLM相对较弱，这与方法本身的静态重建设计一致——当前管道无法建模动态场景中的物体位移。

### 消融实验

Table 3和Table 5报告了八种模型变体在SAT-Real上的消融结果，系统拆解了每个设计选择的作用。完整SandboxVLM（设置8）以84.1%准确率位居榜首。

**3D抽象表示的有效性。** 去除3D抽象边界框、仅使用多视图图像作为上下文（设置3）导致性能从84.1%下降至78.7%，降幅达5.4个百分点。这验证了核心洞察：粗粒度的符号化3D结构（定向边界框）比原始多视图像素信息更适合VLM的空间推理。Figure 4的可视化对比进一步支持这一结论——3D Sandbox在信息量和可解释性之间取得了平衡，既提供生动的空间线索，又过滤了无关细节。

**结构化OBB优于稀疏点云。** 移除多视图投票与聚类，改用渲染的代理点（设置6）后，性能降至77.0%（-7.1个百分点）。这表明经过一致性过滤和DBSCAN聚类后拟合的定向边界框，比稀疏的3D点云更具信息密度和结构清晰度，VLM从中提取空间关系更为高效。

**视觉模态优于文本模态。** 以文本形式提供3D坐标（设置5）准确率为80.8%，低于视觉Sandbox的84.1%（-3.3个百分点）。这说明对于空间推理任务，视觉模态的3D渲染比文本坐标描述更有效，VLM在视觉空间中处理空间关系的效率高于语言描述。

**显式3D结构优于关系图。** 使用场景图文本提示（设置2）性能仅为77.0%（-7.1个百分点），证明简单的对象关系图无法替代显式的3D空间结构。场景图虽然编码了语义关系，但丢失了精确的空间配置信息，这对VLM的空间推理至关重要。

**其他消融发现。** 仅使用VLM进行对象过滤而不构建3D表示（设置1）性能为75.9%，验证了3D提升的必要性。使用2D边界框而非3D Sandbox（设置7）达到81.3%，表明2D框已提供部分空间信息，但缺少深度和三维布局限制了其效果。使用原始点云渲染（设置4）为79.2%，说明未经一致性过滤的噪声点云反而干扰VLM推理。

### 失败模式分析

Figure 5统计了SAT-Real上的错误分布，揭示了五类典型失败模式：

1. **物体运动推理错误。** 由于3D重建模块为静态设计，SandboxVLM无法建模物体在时间维度上的位移，导致在Object Movement子任务上表现相对较弱。这是当前架构的根本性限制。

2. **外观依赖查询失败。** 抽象边界框丢弃了物体外观细节（如人物朝向、物体纹理），当查询需要依赖这些外观信息时（例如“面向左的人”），模型无法给出正确答案。

3. **VLM指向不准确。** 代理提升模块依赖VLM识别任务相关对象及其中心像素坐标。当VLM指向错误或遗漏关键对象时，误差会向下游传播，导致重建的3D盒子不完整或错误。

4. **多视图生成噪声。** 视频扩散先验生成的多视图序列可能包含几何不一致或伪影，这些噪声通过代理提升和投票聚类进入最终的3D表示。

5. **深度估计误差。** 现成深度估计器的误差直接导致3D代理点位置偏差，尤其在遮挡边界和细薄结构处更为明显。

Figure 6展示了不同输入类型下的具体失败案例：渲染点云输入容易因点稀疏性导致VLM误判空间关系；文本坐标提示则因缺乏视觉直观性使VLM难以准确推理相对位置。

### 公平性说明

所有评估均在零样本设置下进行，未在任何目标基准上进行微调，确保了与基线的公平比较。针对SAT-Synth基准，为控制API成本进行了子采样，子采样策略在补充材料中公开（见Listing 2）。

### 补充图表

![[assets/figures/papers/paper_list_l2367_https_arxiv_org_abs_2511_10946/figures/005_Table_2.jpg]]
*Table 2: Quantitative results on the SAT-Real and SAT-Synth benchmarks. Each block compares baseline, MindJourney, and our SandboxVLM under the same backbone (GPT-4o, GPT-5-mini, or GPT-5). Metrics are reported across five spatial reasoning dimensions: EgoMovement (EgoM), ObjectMovement (ObjectM), GoalAiming (GoalAim), ActionConsequence (ActCons), and PerspectiveTaking (Perspect). SandboxVLM consistently achieves the best or second-best results*

![[assets/figures/papers/paper_list_l2367_https_arxiv_org_abs_2511_10946/figures/006_Table_3.jpg]]
*Table 3: Ablation study across multiple spatial reasoning benchmarks. We evaluate eight model variants described in Sec. 4.3, each isolating a key design choice. The full model achieves the highest overall accuracy, demonstrating that 3D Sandbox is one effective way of modeling spatial structure for VLMs*

![[assets/figures/papers/paper_list_l2367_https_arxiv_org_abs_2511_10946/figures/007_Figure_4.jpg]]
*Figure 4: Visualization of representations in ablation study. (a) Input image to the system; (b) Scene graph generated by expert model; (c) Reconstructed point cloud rendering. (d) Text description of 3D bounding boxes; (e) Rendered proxy points; (f) 3D Sandbox. 3D Sandbox strikes a balance between informativeness and interpretability, providing vivid spatial cues while filtering out irrelevant details*

![[assets/figures/papers/paper_list_l2367_https_arxiv_org_abs_2511_10946/figures/010_Table_5.jpg]]
*Table 5: Composition of each ablation method. We list: Average: the average performance on SAT-Real [25]; Modality: in which modality is the context information provided to VLM; Priors: whether a world model is used as a 3D-aware prior in generating the context; 3D: whether the context is lifted into the 3D space; Filtered: before constructing the context, whether a VLM is used to collect information relevant with the task; Using Boxes: whether we finally construct the 3D Sandbox as the context*

![[assets/figures/papers/paper_list_l2367_https_arxiv_org_abs_2511_10946/figures/009_Table_4.jpg]]
*Table 4: Question types and examples from each benchmark. The four types of benchmarks we evaluated on contain various tasks from metric questions like relative depths to comprehensive ones like physical scene understanding. For more details, please refer to the corresponding paper*

## 方法谱系与知识库定位

### 问题定位：从2D训练到3D推理的模态鸿沟

当前主流视觉语言模型（VLM）在训练阶段几乎完全依赖2D图像-文本对，缺乏对三维空间结构的显式建模。这导致了一个核心瓶颈：**VLM的2D训练模式与3D空间推理任务之间存在模态鸿沟**，使得模型难以从单张2D输入中高效检索和理解三维空间关系。现有应对此问题的方案大致分为三类：

- **通用VLM零样本推理**：如 **GPT-4o**、**GPT-5-mini**、**Claude-Sonnet-4**、**Gemini-2.5-Pro** 以及 **Qwen2.5-VL** 系列，直接使用2D图像进行空间问答，但缺乏3D先验，在需要精确空间理解的场景中表现受限。
- **训练/微调方法**：如 **VeBrain-8B**、**Magma-8B**、**Robix-32B-Base**、**RoboBrain2.0-32B**和 **Cosmos-Reason1**，通过对VLM进行3D任务监督微调来注入空间知识。然而，这类方法面临3D训练数据稀缺和灾难性遗忘的风险。
- **测试时缩放方法**：如 **MindJourney**，在推理阶段引入额外的计算或搜索策略，但未从根本上改变VLM对3D信息的表征方式。

SandboxVLM 采取了一条不同于上述所有方案的路径：**训练无关的符号化3D结构注入**。其核心洞察源自人类抽象感知——人类无需精确的度量重建即可进行高效的空间推理，仅依赖粗粒度的关系性理解。SandboxVLM 将这一原则具象化为“3D沙盒”表示：一组紧凑的抽象3D定向边界框，编码空间布局与物理动态，同时丢弃低层视觉细节。

### 方法谱系中的位置

从技术路线看，SandboxVLM 处于**零样本VLM推理**与**3D场景理解**的交叉地带，但其设计哲学与两类工作均有本质区别：

1. **相对于零样本VLM基线**：SandboxVLM 不改变VLM本身，而是在输入端注入任务相关的3D上下文。这种“外挂式”架构使其可适配任意VLM骨干（实验中覆盖了GPT-4o、GPT-5-mini和GPT-5），保持了零样本特性，同时弥补了VLM原生3D感知能力的不足。

2. **相对于训练方法**：SandboxVLM 无需任何微调，避免了3D数据稀缺和遗忘问题。在BLINK和EmbSpatial-Bench上，SandboxVLM 相比训练方法仍有差距——这可能是由于这些基准的简单问答风格和任务特定训练带来的领域适配优势。这揭示了当前方法的适用边界：**在高度特化的具身任务上，训练方法仍具竞争力**。

3. **相对于测试时缩放方法（MindJourney）**：SandboxVLM 在SAT-Real上相比MindJourney取得8.3%的提升，在PhysBench上提升3.4%。关键差异在于，MindJourney 在推理时进行搜索/规划，而SandboxVLM 在推理前构建显式的3D世界状态表示——这是一种“先理解，再推理”的范式。

4. **相对于3D重建+推理管线**：SandboxVLM 刻意避免精确的度量重建（如稠密点云或网格），而是通过代理提升（Proxy Elevation）和多视图投票聚类（MVC）生成符号化的定向边界框。消融实验（Table 3）直接验证了这一设计：使用渲染的代理点云（设置6）性能降至77.0%，而完整的3D沙盒表示达到84.1%，表明**结构化OBB比稀疏点云对VLM更友好**。

### 适用边界与局限

SandboxVLM 的设计取舍带来了明确的适用边界：

- **静态场景假设**：当前3D重建模块为静态设计，无法直接建模动态场景中的物体运动。这导致在SAT-Real的Object-Movement子任务上表现相对较弱——系统无法捕捉物体的时序位移。
- **外观信息丢失**：抽象边界框刻意忽略物体外观细节（如人物朝向、纹理），当查询依赖此类信息时，系统可能无法正确回答。论文在失败案例分析中明确指出了这一模式。
- **误差传播风险**：模块化管道依赖多个现成模型——视频扩散模型（多视图生成）、深度估计器、SAM分割器和VLM对象指向。任何模块的误差都可能级联放大，尤其在VLM指向不准确时，后续的分割和3D提升都会偏离目标对象。
- **基准覆盖的局限**：在BLINK和EmbSpatial-Bench上，SandboxVLM相比训练方法仍有差距，说明当前方案在处理具身空间交互任务时并非最优选择。

### 开放问题

论文提出的开放问题直接指向上述局限的解决路径：

1. **动态场景扩展**：如何将SandboxVLM扩展到动态3D场景重建，以捕捉物体移动和时间变化？这可能需要引入时序建模或4D重建组件。

2. **外观建模集成**：如何在抽象3D表示中整合物体外观信息（如集成Sam-3D-Objects），以支持面向朝向等外观相关查询？这需要在“抽象”与“保真”之间找到新的平衡点。

3. **物理属性编码**：如何将质量、摩擦力等物理属性集成到沙盒表示中，以进一步提升物理推理性能？这涉及从视觉信号到物理参数的映射问题。

4. **噪声鲁棒性**：如何缓解多视图生成和VLM对象指向中的噪声，降低误差传播？可能的方案包括引入不确定性估计或端到端的可微分优化。

## 原文 PDF

![[paperPDFs/CVPR_2026/Abstract_3D_Perception_for_Spatial_Intelligence_in_Vision_Language_Models.pdf]]