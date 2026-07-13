---
title: "4DP-QA: Scalable QA for 4D Perception in Vision Language Models"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/4DP_QA_Scalable_QA_for_4D_Perception_in_Vision_Language_Models.pdf
project_link: null
code_link: null
aliases:
- 4Q
- 4QSQ4PVLM
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: 构建一个可扩展的 QA 生成流水线，利用多源数据的精确几何信息（相机位姿、深度、6D 物体姿态）自动生成大规模 4D 推理 QA 对（4DP-QA），并引入“True-Motion Point Tracking”任务，使 VLM 从数据中学习解耦相机与物体运动的能力。
primary_logic: 通过精心设计的启发式规则，将连续几何测量转化为自然语言问答，特别是基于固定参考系的 true-motion 跟踪，为 VLM 提供直观的、图像对齐的运动表示。以这种数据驱动的方式，即使不修改 VLM 架构，也能让模型涌现出细粒度的 4D 理解能力。
claims:
- 在外部 4D 推理基准 VLM4D 上，使用 4DP-QA 训练后，NVILA-Lite-8B 的总体准确率从 42.8% 提升至 60.5%，Qwen2.5-VL-7B 从 52.3% 提升至 63.6%。
- 在 4DP-QA-Bench 上，多个开源 VLM 经过 4DP-QA 训练后性能大幅跃升，例如 NVILA-Lite-8B 从 42.3% 提升至 84.4%，且全部超越最强闭源基线 Gemini-2.5-Pro (66.8%)。
- 消融实验证实，加入 true-motion point tracking 任务对提升外部基准泛化能力最为关键，而集成几何编码器能进一步提升合成场景的准确率至 85.4%。
- 4DP-QA-Bench 上 Overall Accuracy = 84.4% (NVILA-Lite-8B+4DP-QA)
---

# 4DP-QA: Scalable QA for 4D Perception in Vision Language Models

> [!tip] 核心洞察
> 通过精心设计的启发式规则，将连续几何测量转化为自然语言问答，特别是基于固定参考系的 true-motion 跟踪，为 VLM 提供直观的、图像对齐的运动表示。以这种数据驱动的方式，即使不修改 VLM 架构，也能让模型涌现出细粒度的 4D 理解能力。

| 字段 | 内容 |
|------|------|
| 中文题名 | 4DP-QA：面向视觉语言模型的可扩展4D感知问答 |
| 英文题名 | 4DP-QA: Scalable QA for 4D Perception in Vision Language Models |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://openaccess.thecvf.com/content/CVPR2026/html/Cho_4DP-QA_Scalable_QA_for_4D_Perception_in_Vision_Language_Models_CVPR_2026_paper.html) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/image_and_video_generation |
| Method | 4DP-QA |
| Dataset | 4DP-QA-Bench, VLM4D |

> [!tip] 效果简介
> - 4DP-QA-Bench 上，Overall Accuracy 84.4% (NVILA-Lite-8B+4DP-QA) vs 42.3% (NVILA-Lite-8B) (+42.1%)；Overall Accuracy 84.3% (Qwen2.5-VL-7B+4DP-QA) vs 46.6% (Qwen2.5-VL-7B) (+37.7%)。
> - VLM4D 上，Overall Accuracy 60.5% (NVILA-Lite-8B+4DP-QA) vs 42.8% (NVILA-Lite-8B) (+17.7%)；Overall Accuracy 63.6% (Qwen2.5-VL-7B+4DP-QA) vs 52.3% (Qwen2.5-VL-7B) (+11.3%)。

## 概要

**问题背景与瓶颈** 当前视觉语言模型（VLM）在理解动态 4D 场景时存在根本性困难：运动信息通过投影到 2D 图像间接观测，深度信息丢失；同时，现有数据集未能解耦物体自身运动与相机运动，导致模型只能学习表观运动而无法理解真实 3D 运动。

**核心方法** 本文提出 **4DP-QA**，一个可扩展的时空问答生成流水线。该方法利用多源数据的精确几何信息（相机位姿、深度、6D 物体姿态），自动生成大规模 4D 推理问答对。其关键创新在于引入 **True-Motion Point Tracking** 任务——在固定参考系下表示物体的真实运动，从而为 VLM 提供一种直观的、图像对齐的运动表示，使模型能够从数据中学习解耦相机与物体运动的能力。

**方法定位** 4DP-QA 属于数据驱动的方法谱系，通过精心设计的启发式规则将连续几何测量转化为自然语言问答，在不修改 VLM 架构的前提下，让模型涌现出细粒度的 4D 理解能力。其生成的数据集涵盖驾驶、室内、仿真等多种场景的 400K QA 对，覆盖相机运动、物体运动、3D 空间理解和点跟踪等 13 类时空推理任务。

**核心结论** 在自建基准 **4DP-QA-Bench** 上，NVILA-Lite-8B 经 4DP-QA 训练后准确率从 42.3% 跃升至 84.4%，Qwen2.5-VL-7B 从 46.6% 提升至 84.3%，全面超越最强闭源基线 Gemini-2.5-Pro（66.8%）。在外部基准 **VLM4D** 上，NVILA-Lite-8B 从 42.8% 提升至 60.5%，Qwen2.5-VL-7B 从 52.3% 提升至 63.6%。消融实验证实，True-Motion Point Tracking 任务对提升外部基准泛化能力最为关键。



视觉语言模型（VLM）在图像与视频理解任务上取得了显著进展，但当面对动态 4D 场景时，现有模型暴露出一个根本性瓶颈：**它们难以理解场景中真实的时空动态**。这一瓶颈的成因是双重的。

首先，运动信息在感知层面是间接获取的。三维世界中的物体运动通过相机投影到二维图像平面上，深度信息在此过程中丢失，模型只能观测到“表观运动”（apparent motion），而无法直接获取物体在三维空间中的真实位移。其次，现有用于训练 VLM 的视频数据集未能系统性地解耦**物体自身运动**与**相机运动**——当相机自身也在移动时，静止的背景物体会在画面中产生位移，而真实运动的物体可能表现出完全不同的图像轨迹。模型从这样的数据中学习，习得的只是像素层面的表观运动模式，而非对三维运动的真正理解。

这一缺口在现有基准中已有体现。例如，在外部 4D 推理基准 VLM4D 上，未经专门训练的 NVILA-Lite-8B 的总体准确率仅为 42.8%，Qwen2.5-VL-7B 为 52.3%，表明即使是当前最先进的开源 VLM，在面对需要解耦相机与物体运动的 4D 推理任务时，表现仍远未令人满意。

本文的核心动机正是填补这一缺口。作者提出，问题的关键不在于 VLM 的架构本身，而在于训练数据所承载的监督信号。如果能够大规模地生成包含精确几何真值的 4D 推理问答对，并将“真实运动”（true-motion）的概念显式地注入训练过程，VLM 就有可能在无需架构修改的前提下，涌现出细粒度的 4D 理解能力。这一思路驱动了整个 4DP-QA 框架的设计：利用多源数据中已有的相机位姿、深度图和 6D 物体姿态等几何信息，自动构建一个可扩展的时空推理 QA 生成流水线，并通过引入 **True-Motion Point Tracking** 这一新的感知任务，为模型提供直观的、图像对齐的运动表示（见 Figure 2），使其学会从表观运动中剥离相机效应，还原物体的真实运动轨迹。



## 核心方法与创新机理

4DP-QA 的核心创新在于**不修改 VLM 架构，而是通过几何驱动的数据生成流水线，系统性地赋予模型细粒度 4D 感知能力**。相对于现有 VLM 仅依赖表观运动进行问答，该方法在三个关键维度上实现了突破。

### 1. 从表观运动到真实运动：True-Motion Point Tracking

当前 VLM 理解动态场景的根本瓶颈在于：运动是通过变化相机投影到 2D 图像间接观测的，物体自身运动与相机运动被不可分地耦合在一起。模型只能学到表观运动（apparent motion），而无法理解真实的 3D 运动。

4DP-QA 引入了一项新的底层感知任务——**True-Motion Point Tracking**，通过固定参考系解耦相机与物体运动。具体而言：

- **视觉点跟踪**（Visual Point Tracking）由变化相机成像，轨迹耦合了物体运动和相机运动：
  $$P_{2D} = \{ \mathbf{p}[t] \}_{t \in [0, T)} = \{ \Pi( \mathbb{K}, \mathbb{T}[t], \mathbf{X}(t) ) \}_{t \in [0, T)}$$

- **真实运动点跟踪**（True-Motion Point Tracking）由固定时刻 $t_q$ 的参考相机成像，轨迹仅反映物体的真实运动：
  $$M_{2D} = \{ \mathbf{m}_{t_q}[t] \}_{t \in [0, T)} = \{ \Pi( \mathbb{K}, \mathbb{T}[t_q], \mathbf{X}(t) ) \}_{t \in [0, T)}$$

这一设计的因果机制在于：将连续的几何测量转化为图像对齐的运动表示，使 VLM 能够以直观的视觉形式感知物体在固定视角下的真实运动。如 Figure 2 所示，当相机向右运动时，视觉点跟踪显示猫向后移动，而真实运动点跟踪正确揭示猫在向前移动——背景点在视觉跟踪中移动，在真实运动跟踪中保持静止。

### 2. 从人工标注到几何驱动的可扩展 QA 生成

现有 VLM 训练数据依赖人工标注或通用图像/视频指令微调数据，难以大规模覆盖 4D 时空推理所需的精确几何信息。4DP-QA 构建了一套**自动几何驱动的 QA 生成流水线**，包含四个关键模块：

- **数据标准化**：将多源数据（驾驶、室内、仿真场景）统一为相同格式，包括坐标系、分辨率、帧率、相机参数、深度、分割、元数据和 6D 物体姿态。
- **资产采样**：根据启发式规则和数据集特定阈值筛选符合条件的视频片段和物体，并确定对象的引用方式（文本描述、坐标或视觉标注）。
- **离散标签生成**：将连续几何测量（如平移、旋转、距离）映射为人类可理解的分类标签（如 forward/backward、increasing/decreasing），确保标签准确且无歧义。
- **QA 生成器**：使用预定义模板和 LLM（Gemini-2.5-Pro）生成多样化的问答，涵盖 13 种问题类型，组织为四大类：相机运动、物体运动、3D 空间理解和点跟踪。

这一流水线的核心洞察在于：**利用数据源中已有的精确几何标注（相机位姿、深度、6D 物体姿态），通过精心设计的启发式规则，将连续几何测量转化为自然语言问答**。这使得无需人工标注即可生成大规模、高质量的 4D 推理训练数据。

### 3. 从稀疏覆盖到大规模多样化训练

现有 VLM 通常不包含或仅包含少量动态 4D 理解数据。4DP-QA 通过上述流水线，从多源数据中生成了**400K QA 对**（来自 3.3M 帧），跨越驾驶、室内、仿真等多种场景。训练数据规模的跃升（从几乎为零到 400K）是模型性能大幅提升的直接驱动力。

消融实验（Table 4）进一步揭示了创新组件的贡献：仅使用标准 4D QA（不含点跟踪）训练即可大幅提升 4DP-QA-Bench 性能，但加入 **True-Motion Point Tracking 任务是提升外部基准 VLM4D 泛化能力的最关键因素**。此外，集成预训练几何编码器 L4P 后，VLM4D 合成场景准确率进一步提升至 85.4%，验证了几何先验与数据驱动方法互补的有效性。



4DP-QA 框架采用**数据驱动**的策略，在不修改 VLM 架构的前提下，通过大规模几何驱动的时空推理问答对训练，赋予模型细粒度的 4D 感知能力。其核心思路是：利用多源数据中已有的精确几何信息，自动生成覆盖相机运动、物体运动、3D 空间理解与点跟踪四大类别的 QA 对，使 VLM 在训练中涌现出解耦相机与物体运动、理解真实 3D 动态的能力。

### 输入与输出

整个流水线的输入是来自**驾驶、室内、仿真**等多种场景的标准化 4D 数据（Table 1），输出为 13 类时空推理 QA 对。训练集 **4DP-QA** 包含约 400K QA 对（源自 3.3M 帧），评测集 **4DP-QA-Bench** 包含约 2.2K QA 对（源自 317K 保留测试帧），训练帧与测试帧来自不同片段，确保无数据泄漏。

### 流水线模块

如图 3 所示，生成流水线由四个核心模块串联构成：

1. **数据标准化**  
   将不同来源的数据统一为相同格式，包括坐标系、图像分辨率、帧率、相机参数、深度、分割、元数据和 6D 物体姿态。3D 点轨迹从深度图、相机位姿和 6D 物体姿态中提取，为后续 QA 生成提供精确几何基础。

2. **资产采样**  
   根据启发式规则和数据集特定阈值，筛选符合条件的视频片段和物体，并确定对象的引用方式（文本描述、坐标或视觉标注），为 QA 模板提供具体“素材”。

3. **离散标签生成**  
   将连续的几何测量（如平移量、旋转量、距离）映射为人类可理解的分类标签（如 forward/backward、increasing/decreasing），确保标签准确且无歧义。

4. **QA 生成器**  
   使用预定义模板与 LLM（Gemini-2.5-Pro）生成多样化的问答。对于描述性问题，模板填入离散标签；对于视觉点跟踪和 true-motion 点跟踪问题，模板填入连续测量值作为答案。

### 关键创新：True-Motion Point Tracking

传统视觉点跟踪（Visual Point Tracking）捕捉的是耦合了相机运动与物体运动的**表观运动**：
$$P_{2D} = \{ \mathbf{p}[t] \}_{t \in [0, T)} = \{ \Pi( \mathbb{K}, \mathbb{T}[t], \mathbf{X}(t) ) \}_{t \in [0, T)}$$

而 True-Motion Point Tracking 通过固定参考相机（时刻 $t_q$ 的相机位姿）重新投影物体 3D 轨迹，得到解耦后的**真实运动**：
$$M_{2D} = \{ \mathbf{m}_{t_q}[t] \}_{t \in [0, T)} = \{ \Pi( \mathbb{K}, \mathbb{T}[t_q], \mathbf{X}(t) ) \}_{t \in [0, T)}$$

这一任务为 VLM 提供了直观的、图像对齐的运动表示，是框架提升 4D 理解能力的关键组件。消融实验证实，加入 true-motion point tracking 任务对提升外部基准泛化能力最为关键（Table 4）。

### 训练设置

所有标准 VLM 基线使用统一训练配置：batch size 128，1 epoch（约 3.1K 次迭代），冻结视觉编码器，AdamW 优化器配合余弦学习率衰减。NVILA-Lite-8B 学习率为 $2 \times 10^{-5}$，Qwen2.5-VL-7B 学习率为 $1 \times 10^{-5}$。评测采用精确字符串匹配的准确率指标，问题格式为多项选择或二选一（Y/N），随机基线为 40.8%。

### 补充图表

![[assets/figures/papers/paper_list_l2230_https_openaccess_thecvf_com_content_CVPR2026_html_Cho_4DP_QA_Scalable_QA/figures/002_Figure_1.jpg]]
*Figure 1: Our framework equips VLMs with better 4D understanding for in-the-wild videos. Training a state-of-the-art VLM (NVILA [42]) on our dataset yields performance gains (NVILA vs. Ours). We also introduce true-motion point tracking, a new capability that enables the VLM to isolate true object motion from camera movement, leading to better 4D understanding*

![[assets/figures/papers/paper_list_l2230_https_openaccess_thecvf_com_content_CVPR2026_html_Cho_4DP_QA_Scalable_QA/figures/005_Figure_3.jpg]]
*Figure 3: Dataset Generation Pipeline (Section 3.2). The pipeline takes as input standardized 4D input data, and produces QA pairs for 13 question types. Each QA pair is generated by instantiating a pre-defined template with the sampled assets and either their discrete labels (for descriptive questions) or continuous measurements (for visual and true-motion point tracking)*



### 真实运动点跟踪 (True-Motion Point Tracking)

4D 场景理解的核心挑战在于，视觉语言模型 (VLM) 通过 2D 图像间接观测 3D 运动，导致物体自身运动与相机运动相互耦合。为此，4DP-QA 首先定义了一个新的感知任务——真实运动点跟踪，作为后续 QA 对生成的关键组件。

**视觉点跟踪 (Visual Point Track)** 描述了 3D 点 $\mathbf{X}(t)$ 经由随时间变化的相机投影到 2D 图像平面的轨迹：

$$P_{2D} = \{ \mathbf{p}[t] \}_{t \in [0, T)} = \{ \Pi( \mathbb{K}, \mathbb{T}[t], \mathbf{X}(t) ) \}_{t \in [0, T)}$$

其中 $\mathbb{K}$ 为相机内参矩阵，$\mathbb{T}[t]$ 为时刻 $t$ 的相机外参（位姿），$\Pi$ 表示透视投影。该轨迹同时包含物体运动和相机运动的信息，模型仅能感知到“表观运动”（apparent motion）——例如，当相机向右平移时，静止的猫在图像中会向左移动，视觉点跟踪无法区分这一表象。

**真实运动点跟踪 (True-Motion Point Track)** 通过将参考相机固定在某一查询时刻 $t_q$，解耦相机运动与物体运动：

$$M_{2D} = \{ \mathbf{m}_{t_q}[t] \}_{t \in [0, T)} = \{ \Pi( \mathbb{K}, \mathbb{T}[t_q], \mathbf{X}(t) ) \}_{t \in [0, T)}$$

在此公式中，所有时刻的 3D 点 $\mathbf{X}(t)$ 均通过固定时刻 $t_q$ 的相机位姿 $\mathbb{T}[t_q]$ 进行投影。这意味着轨迹反映的是物体在固定参考系下的真实 3D 运动，而非受相机运动污染的表观运动。如 Figure 2 所示，真实运动点跟踪下，背景点保持静止（灰色轨迹），而物体轨迹准确反映其自身的运动方向。

![[assets/figures/papers/paper_list_l2230_https_openaccess_thecvf_com_content_CVPR2026_html_Cho_4DP_QA_Scalable_QA/figures/003_Figure_2.jpg]]
*Figure 2: True-motion Point Tracking. Visual point tracking (a) only captures the apparent motion of the object, here making the cat appear to move backward due to the rightward camera motion. True-motion point tracking (b) disentangles camera and object motion, showing the cat moving forward. Background tracks (gray points) show movement in (a) but remain stationary in (b), highlighting that true-motion tracks reflect actual object motion as seen from a fixed viewpoint*

### QA 生成流水线的关键模块

4DP-QA 的 QA 生成流水线包含四个核心模块，将精确的几何测量转化为自然语言问答对：

1. **数据标准化 (Data Standardization)**：将来自驾驶、室内、仿真等多种场景的原始数据统一为相同格式，包括坐标系对齐、图像分辨率、帧率、相机参数（内参 $\mathbb{K}$ 和外参 $\mathbb{T}$）、深度图、分割掩码、元数据以及 6D 物体姿态。3D 点轨迹由深度图、相机位姿和物体姿态联合提取，为后续 QA 对提供几何基础。

2. **资产采样 (Asset Sampling)**：根据启发式规则和数据集特定阈值，筛选符合条件的视频片段和动态物体。同时确定对象的引用方式——可以是文本描述、像素坐标，或视觉标注（如边界框），以适应不同问题类型的需求。

3. **离散标签生成 (Discrete Label Generation)**：将连续的几何测量映射为人类可理解的分类标签。例如，将物体的平移向量方向离散化为 `forward`、`backward`、`left`、`right` 等空间关系词；将距离变化映射为 `increasing`、`decreasing` 或 `unchanged`。这一映射确保标签准确且无歧义，是生成高质量 QA 对的关键步骤。

4. **QA 生成器 (QA Generator)**：使用预定义模板和 LLM（Gemini-2.5-Pro）实例化多样化的问答对。对于描述性问题，填入采样资产的离散标签；对于点跟踪任务，则直接输出连续的归一化坐标序列作为答案。最终生成覆盖 4 大类 13 种问题类型的 400K QA 对。

### 问题类型组织

13 种问题类型按 4 个类别组织：

- **相机运动 (Camera Motion)**：判断相机自身的平移/旋转方向及其变化。
- **物体运动 (Object Motion)**：判断特定物体的运动方向、速度变化，以及物体间相对运动关系。
- **3D 空间理解 (3D Spatial Understanding)**：涉及物体间的 3D 距离、深度排序和空间关系推理。
- **点跟踪 (Point Tracking)**：包含视觉点跟踪 ($P_{2D}$) 和真实运动点跟踪 ($M_{2D}$) 两类任务，要求模型输出点的 2D 轨迹坐标序列。

消融实验（Table 4）证实，真实运动点跟踪任务的加入是提升模型在外部基准 VLM4D 上泛化能力的最关键因素，同时不影响标准 4D QA 任务的性能。



## 实验与关键发现

### 主实验结果

为验证 4DP-QA 数据集的有效性，作者在内部基准 4DP-QA-Bench 和外部基准 VLM4D 上进行了系统评测。训练设置上，所有标准 VLM 基线采用统一配置：batch size 128，训练 1 epoch（约 3.1K 迭代），冻结视觉编码器，AdamW 优化器配合余弦学习率衰减。NVILA-Lite-8B 的学习率设为 $2 \times 10^{-5}$，Qwen2.5-VL-7B 的学习率设为 $1 \times 10^{-5}$。4DP-QA-Bench 包含 2.2K QA 对，来自 317K 保留测试帧，评测采用精确字符串匹配的准确率指标（随机基线为 40.8%）。

**内部基准 4DP-QA-Bench 结果**（Table 2）显示，经 4DP-QA 训练后，所有开源 VLM 均取得大幅跃升：

- NVILA-Lite-8B 从 42.3% 提升至 **84.4%**（+42.1%）
- Qwen2.5-VL-7B 从 46.6% 提升至 **84.3%**（+37.7%）

值得注意的是，训练后的模型全部超越最强闭源基线 Gemini-2.5-Pro（66.8%），表明 4DP-QA 的数据驱动策略能有效弥补开源 VLM 在 4D 感知上的短板。

**外部基准 VLM4D 泛化结果**（Table 3）进一步证实了方法的迁移能力：

- NVILA-Lite-8B + 4DP-QA 达到 60.5%，相比未训练的 42.8% 提升 17.7%
- Qwen2.5-VL-7B + 4DP-QA 达到 63.6%，相比未训练的 52.3% 提升 11.3%

VLM4D 的数据分布与训练集不同，上述增益表明模型确实学到了可迁移的 4D 推理能力，而非简单记忆训练模板。

### 消融实验

消融实验（Table 4）围绕数据集组成展开，核心结论如下：

![[assets/figures/papers/paper_list_l2230_https_openaccess_thecvf_com_content_CVPR2026_html_Cho_4DP_QA_Scalable_QA/figures/008_Table_4.jpg]]
*Table 4: Ablation study on dataset composition. We ablate the effect of adding tracking tasks to Std-4DP-QA by evaluating the resulting models on both our 4DP-QA-Bench and the external VLM4D dataset [71]. See Section 3.3 for description of each question type*

1. **标准 4D QA 的独立贡献**：仅使用标准 4D QA（不含点跟踪任务）训练，即可在 4DP-QA-Bench 上取得显著性能提升，说明覆盖相机运动、物体运动和 3D 空间理解的 13 类问答已具备较强的教学信号。

2. **True-Motion Point Tracking 的关键作用**：在标准 4D QA 基础上加入点跟踪任务（特别是 True-Motion Tracking），能在保持标准 QA 性能的同时，**显著提升 VLM4D 外部基准的泛化能力**。这验证了核心假设：解耦相机与物体运动的 true-motion 表示，是 VLM 实现鲁棒 4D 理解的关键因果杠杆。

3. **几何编码器的加成效应**：在 VLM 中集成预训练几何编码器 L4P 后，模型在 4DP-QA-Bench 和 VLM4D 合成子集上均获得进一步提升，VLM4D 合成场景准确率达到 **85.4%**。这表明显式的几何先验可以与数据驱动的 4D QA 形成互补。

### 失败模式与局限性

尽管整体性能大幅提升，分析揭示了若干值得关注的局限：

- **几何标注依赖性**：QA 生成流水线依赖精确的相机位姿、深度和 6D 物体姿态。对于缺乏此类标注的真实视频，需借助现成的 4D 重建方法，可能引入级联误差。这一瓶颈限制了方法向完全开放域视频的直接推广。
- **模型规模覆盖有限**：训练和评测集中在 3B–8B 规模的 VLM 上，更大规模模型（如 70B+）上的效果仍有待验证。目前无法判断性能增益是否随模型规模持续扩大。
- **场景多样性不足**：数据集虽覆盖驾驶、室内和仿真场景，但种类仍有限。合成场景与真实场景之间的分布差异对泛化的影响尚未深入分析——VLM4D 合成子集 85.4% 的准确率与整体 60.5–63.6% 之间的差距，暗示域差异可能是当前泛化瓶颈之一。
- **点跟踪评估粒度**：点跟踪任务采用归一化坐标匹配作为评估指标，与某些下游应用对绝对像素精度的要求可能存在差距，实际部署时需额外校准。

### 补充图表

![[assets/figures/papers/paper_list_l2230_https_openaccess_thecvf_com_content_CVPR2026_html_Cho_4DP_QA_Scalable_QA/figures/006_Table_2.jpg]]
*Table 2: Quantitative comparison of VLMs on our 4DP-QA-Bench. We report the accuracy (%) for each task. Alongside comparisons with off-the-shelf VLMs, we also present the performance improvements obtained by training the baseline models on 4DP-QA. Please refer to Section 3.3 for detailed descriptions of each column*

![[assets/figures/papers/paper_list_l2230_https_openaccess_thecvf_com_content_CVPR2026_html_Cho_4DP_QA_Scalable_QA/figures/007_Table_3.jpg]]
*Table 3: Evaluation on VLM4D [71] Benchmark. We evaluate how training on our 4DP-QA dataset improves generalization to the VLM4D benchmark*

![[assets/figures/papers/paper_list_l2230_https_openaccess_thecvf_com_content_CVPR2026_html_Cho_4DP_QA_Scalable_QA/figures/004_Table_1.jpg]]
*Table 1: Data sources for the dataset generation pipeline. We collect data from a variety of sources, including driving, indoor, and simulation datasets, spanning synthetic and real-world scenes. Once preprocessed, they are standardized to a common format that our generation pipeline (Section 3.2) can use to produce QA pairs*

![[assets/figures/papers/paper_list_l2230_https_openaccess_thecvf_com_content_CVPR2026_html_Cho_4DP_QA_Scalable_QA/figures/009_Figure_4.jpg]]
*Figure 4: Visualization of true motion track prediction. Truemotion tracking for dynamic scenes with camera motion (all but bottom right). Estimated tracks disentangle camera motion and summarize object motion as seen in the first frame*



## 定位与知识库关联

### 1. 与现有 VLM 基线的谱系关系

4DP-QA 并非提出新的模型架构，而是构建一套**数据驱动的 4D 感知能力注入框架**，作用于现有开源 VLM 之上。论文选用的基线模型包括：

- **NVILA-Lite-8B**（Liu et al., CVPR 2025）：高效视觉语言模型，作为主要实验载体。
- **Qwen2.5-VL-7B**（Bai et al., ArXiv 2025）：通义千问视觉语言模型，用于验证方法的跨架构泛化性。
- **GPT-4o** 与 **Gemini-2.5-Pro**（Comanici et al., ArXiv 2025）：作为闭源商业模型的对比参照系。

这些基线模型在原生状态下均缺乏专门的 4D 时空推理能力——它们仅通过通用图像/视频指令微调数据训练，对动态场景的理解停留在表观运动层面，无法解耦相机运动与物体自身运动。4DP-QA 的核心贡献在于证明：**即使不修改 VLM 架构，仅通过精心设计的几何驱动 QA 数据进行监督微调，也能使模型涌现出细粒度的 4D 理解能力**。

### 2. 关键设计差异：从表观运动到真实运动

方法谱系上的根本差异体现在两个维度：

**（1）训练数据生成方式**

| 维度 | 基线 VLM 训练数据 | 4DP-QA 训练数据 |
|------|------------------|----------------|
| 标注方式 | 人工标注或通用图像/视频指令微调 | 自动几何驱动 QA 生成流水线 |
| 几何信息利用 | 无 | 利用相机位姿、深度、6D 物体姿态等精确信息 |
| 问题类型覆盖 | 通用视觉问答 | 13 类时空推理 QA 对，覆盖相机运动、物体运动、3D 空间理解和点跟踪 |
| 数据规模 | 不包含或仅少量动态 4D 数据 | 跨越驾驶、室内、仿真等多场景的 400K QA 对 |

**（2）运动表示与任务**

这是方法层面最本质的创新。传统 VLM 仅能感知**视觉点跟踪（Visual Point Tracking）**——由变化相机成像的 2D 轨迹，其数学形式为：

$$P_{2D} = \{ \mathbf{p}[t] \}_{t \in [0, T)} = \{ \Pi( \mathbb{K}, \mathbb{T}[t], \mathbf{X}(t) ) \}_{t \in [0, T)}$$

该轨迹将物体运动与相机运动纠缠在一起，导致模型学到的是表观运动而非真实 3D 运动。

4DP-QA 引入**真实运动点跟踪（True-Motion Point Tracking）**任务，其数学形式为：

$$M_{2D} = \{ \mathbf{m}_{t_q}[t] \}_{t \in [0, T)} = \{ \Pi( \mathbb{K}, \mathbb{T}[t_q], \mathbf{X}(t) ) \}_{t \in [0, T)}$$

核心差异在于：使用**固定时刻 $t_q$ 的参考相机**对所有帧进行成像，从而解耦相机运动与物体运动。如 Figure 2 所示，当相机向右移动时，视觉点跟踪会错误地显示猫向后移动，而真实运动点跟踪则正确反映猫向前移动，背景轨迹保持静止。

### 3. 适用边界与能力范围

4DP-QA 的能力边界由以下因素界定：

**（1）数据依赖边界**

QA 生成流水线**强依赖数据源提供的精确几何标注**（相机位姿、深度图、6D 物体姿态）。对于无此类标注的真实开放域视频，论文明确指出需借助现成的 4D 重建方法，而这可能引入误差。当前数据来源覆盖驾驶场景、室内场景和合成场景（Table 1），但场景种类仍有限。

**（2）模型规模边界**

训练和评测主要集中在 **3B–8B 参数规模**的 VLM 上。更大规模模型（如数十亿参数级别的 VLM）上的效果仍有待验证——这是方法可扩展性的一个未闭合环节。

**（3）任务覆盖边界**

所设计的 13 种问题类型分为四大类：相机运动、物体运动、3D 空间理解、点跟踪。消融实验（Table 4）表明：
- 仅使用标准 4D QA（不含点跟踪）训练即可大幅提升 4DP-QA-Bench 性能；
- 加入点跟踪任务（特别是 True-Motion Tracking）能在保持标准 QA 性能的同时，显著提高 VLM4D 外部基准的泛化能力；
- 集成预训练几何编码器 L4P 后，VLM4D 合成子集准确率进一步提升至 85.4%。

这暗示点跟踪任务对泛化能力至关重要，但当前任务集是否覆盖所有真实世界的 4D 时空推理需求仍是一个开放问题。

### 4. 局限性与开放问题

**已确认的局限：**

1. **几何标注依赖**：流水线依赖精确几何标注，对无标注真实视频需借助 4D 重建方法，可能引入级联误差。
2. **场景多样性有限**：合成场景与真实场景之间的分布差异对泛化的影响尚未深入分析。
3. **评估粒度**：点跟踪任务采用归一化坐标匹配评估，可能与下游应用对绝对精度的要求存在差距。

**待探索的开放问题：**

1. **无监督/弱监督扩展**：如何将 True-Motion Point Tracking 推广到完全无几何标注的开放域视频中？
2. **任务完备性**：13 种问题类型是否足够覆盖真实世界中所有的 4D 时空推理需求？是否存在未被捕捉的重要动态属性（如非刚性形变、流体运动）？
3. **域差异量化与弥合**：合成数据与真实数据之间的域差异在多大程度上影响模型泛化？如何通过域适应或数据增强进一步缩小这一差异？
4. **复杂场景拓展**：True-Motion 思想是否可拓展到多相机系统或非刚性物体运动场景？

### 5. 知识库定位总结

4DP-QA 在知识谱系中的定位可概括为：**一种几何驱动的数据增强与任务设计方法**，架起了精确 3D/4D 几何信息与 VLM 自然语言理解能力之间的桥梁。其核心洞察在于：通过精心设计的启发式规则将连续几何测量转化为自然语言问答，以数据驱动的方式让 VLM 涌现 4D 理解能力，而非依赖架构修改。该方法属于“数据为中心”的 VLM 能力扩展范式，与“模型为中心”的架构创新路线形成互补。



## 原文 PDF

![[paperPDFs/CVPR_2026/4DP_QA_Scalable_QA_for_4D_Perception_in_Vision_Language_Models.pdf]]
