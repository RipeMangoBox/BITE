---
title: "MotionBooth: Motion-Aware Customized Text-to-Video Generation"
type: paper
paper_level: A
venue: NeurIPS
year: 2024
pdf_ref: paperPDFs/NEURIPS_2024/MotionBooth_Motion_Aware_Customized_Text_to_Video_Generation.pdf
project_link: https://jianzongwu.github.io/projects/motionbooth
code_link: null
aliases:
- MotionBooth
tags:
- NEURIPS_2024
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: "在主体学习阶段引入主体区域损失、视频保持损失和主体令牌交叉注意力损失（STCA），以及在推理阶段采用训练自由的交叉注意力映射操纵和潜空间偏移模块。"
primary_logic: "主体学习通过掩码化扩散损失和联合视频数据训练来保持预训练T2V模型的运动先验，然后利用交叉注意力绑定主体令牌与位置，并通过直接编辑交叉注意力图和偏移噪声潜变量实现免训练的主体和相机运动控制。"
claims:
- "主体微调破坏视频生成能力，导致背景过平滑。"
- "STCA损失有效链接主体令牌与位置映射。"
- "潜空间偏移模块以免训练方式实现精确相机控制，超越训练方法如CameraCtrl。"
- "MotionBooth在所有指标上优于现有定制视频生成基线。"
---

# MotionBooth: Motion-Aware Customized Text-to-Video Generation

> [!tip] 核心洞察
> 主体学习通过掩码化扩散损失和联合视频数据训练来保持预训练T2V模型的运动先验，然后利用交叉注意力绑定主体令牌与位置，并通过直接编辑交叉注意力图和偏移噪声潜变量实现免训练的主体和相机运动控制。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | MotionBooth：运动感知的定制文本到视频生成 |
| 英文题名 | MotionBooth: Motion-Aware Customized Text-to-Video Generation |
| 会议/期刊 | NeurIPS 2024 |
| Links | [paper](https://arxiv.org/abs/2406.17758) · [Project](https://jianzongwu.github.io/projects/motionbooth) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/image_and_video_generation |
| Method | MotionBooth |
| Dataset | Custom subject-motion eval (26 subjects, 40 text-motion pairs), Camera motion control eval (MSRVTT subset) |

> [!tip] 效果简介
> - Custom subject-motion eval (26 subjects, 40 text-motion pairs) 上，R-CLIP 为 0.667，对比 0.608 (DreamBooth)，变化 +0.059。
> - Custom subject-motion eval (26 subjects, 40 text-motion pairs) 上，R-DINO 为 0.306，对比 0.279 (DreamBooth)，变化 +0.027。
> - Custom subject-motion eval (26 subjects, 40 text-motion pairs) 上，Flow error 为 0.252，对比 0.690 (DreamBooth)，变化 -0.438。

## 概要

**核心问题**：预训练文本到视频（T2V）扩散模型在针对特定主体进行微调时，存在一个关键瓶颈——模型容易过拟合背景细节，同时丧失原有的视频生成能力，导致生成的视频要么背景退化、要么运动匮乏。现有的定制化视频生成方法（如 **DreamBooth** (Ruiz et al., CVPR 2023)、**CustomVideo** 等）主要关注主体外观保真度，却忽视了运动层面的可控性。

**MotionBooth** 提出了一套统一的框架，在保持主体外观保真度的同时，实现对主体运动和相机运动的精确控制。其核心思路分为两个阶段：

1. **主体学习阶段**：通过三项损失函数增强微调过程——
   - **主体区域损失**（Subject Region Loss）：将扩散重建损失限制在主体掩码区域内，防止背景过拟合；
   - **视频保持损失**（Video Preservation Loss）：在通用视频数据上联合训练，维持预训练模型的视频生成先验；
   - **主体令牌交叉注意力损失**（STCA Loss）：以二元交叉熵强制主体令牌的交叉注意力图与主体空间位置对齐，建立运动控制的“因果旋钮”。

2. **推理阶段**：采用免训练的操控技术——
   - **交叉注意力编辑**：通过向注意力分数添加编辑矩阵，直接控制主体在画面中的位置；
   - **潜空间偏移**：对去噪过程中的噪声潜变量进行轴向采样、偏移和填充，模拟相机平移运动。

**主要实验结论**：MotionBooth 在定制主体-运动生成任务上全面超越现有基线——在 Zeroscope 上，主体保真度指标 R-CLIP 从 0.608 提升至 0.667，R-DINO 从 0.279 提升至 0.306；运动质量指标 Flow error 从 0.690 降至 0.252。在相机运动控制方面，Flow error 从 **CameraCtrl** 的 1.683 降至 0.190，FVD 从 1468.53 降至 905.40，且无需额外训练。消融实验证实，三项损失各自独立贡献于主体保真度、视频质量和运动可控性，而潜空间偏移中提出的轴向对齐采样填充方法在视觉质量和运动灵活性上均优于随机填充、循环填充等替代方案。

**局限与展望**：该方法在处理非动物物体上的动物运动时可能出现严重变形，无法处理多主体复杂交互，极端相机运动速度下存在平铺效应。未来方向包括扩展到多主体场景、利用更丰富的运动控制信号（如光流、骨架）、以及减少对精确主体掩码的依赖。



### 问题背景：定制化视频生成的兴起

随着扩散模型在图像生成领域的巨大成功，文本到视频（Text-to-Video, T2V）生成近年来取得了长足进步。大型预训练T2V模型能够根据文本描述生成逼真的视频内容。然而，用户往往不仅希望生成通用场景，还希望将特定的个性化主体（如自己的宠物、特定玩具等）植入生成的视频中，并让其按照指定的方式运动。这一需求催生了**定制化视频生成**（customized video generation）这一研究方向。

定制化视频生成面临的核心挑战在于：如何在保持预训练模型视频生成能力的同时，将新的主体概念注入模型，并实现对主体运动和相机运动的精确控制。

### 现有方法的缺口

当前解决定制化视频生成的方法主要存在以下瓶颈：

**1. 主体微调破坏视频生成能力**

现有的主体定制方法（如 **DreamBooth**，Ruiz et al., CVPR 2023）主要通过微调将主体绑定到特殊令牌上。然而，当直接将此类方法应用于T2V模型时，会出现严重的副作用：模型容易**过拟合训练图像的背景**，并丧失原有的视频生成知识。其结果是生成的视频中背景趋于过平滑、缺乏多样性，视频质量显著退化（见 Figure 3）。这一现象的根本原因在于，标准扩散损失对整帧图像施加等权重的重建约束，导致模型将背景静态信息也一并编码进主体令牌中。

**2. 运动控制依赖额外训练**

在运动控制方面，现有方法通常需要训练额外的模块或学习特定的运动模式。例如，**AnimateDiff** 和 **CameraCtrl** 等相机运动控制方法需要在大规模视频数据集上进行训练，才能实现对相机轨迹的控制。对于主体运动控制，类似 **GLIGEN** 的方法需要训练专用的空间条件注入模块。这些基于训练的方法不仅增加了计算开销，还限制了方法的灵活性和泛化能力——每当面临新的运动模式或相机轨迹时，往往需要重新训练或微调。

**3. 主体令牌与空间位置缺乏显式绑定**

在标准的微调流程中，主体令牌与空间位置的关联是通过隐式学习建立的，缺乏显式的监督信号。这导致在推理阶段进行运动控制时，模型无法准确地将主体令牌的交叉注意力图与目标位置对齐，从而难以实现精确的主体运动控制。如 Figure 4 所示，未经显式绑定的模型，其交叉注意力图无法与主体掩码有效重合。

### 本文动机

针对上述问题，MotionBooth 的动机可以归纳为三个层面：

- **训练层面**：设计一种损失增强的训练架构，在主体学习阶段同时解决背景过拟合和视频能力退化的问题，并建立主体令牌与空间位置的显式关联。
- **推理层面**：开发免训练的运动控制技术，避免对额外模块或大规模数据集的依赖，实现灵活且高效的主体运动和相机运动控制。
- **系统层面**：将上述训练和推理技术统一为一个端到端框架，使得用户仅需提供少量主体图像和简单的运动指令（边界框序列和相机偏移量），即可生成运动感知的定制化视频。

简而言之，MotionBooth 旨在回答一个核心问题：**如何在不破坏预训练T2V模型视频生成先验的前提下，实现精确且免训练的主体和相机运动控制？**



## 核心方法与创新机理

MotionBooth 的核心创新在于**将主体定制化视频生成中的三大瓶颈——背景过拟合、运动控制缺失、相机运动僵化——转化为三个可解耦的“改变槽位”（changed slots）**，并通过训练期损失重构与推理期免训练操控的组合策略逐一突破。

### 改变槽位一：训练损失的重新设计（从标准重建损失到三合一损失）

预训练 T2V 模型在主体微调时，标准扩散重建损失（Eq. 1）会同时对前景主体和背景施加约束，导致模型**过拟合背景并丧失视频生成能力**（Figure 3）。MotionBooth 将这一槽位从单一的 `L_recon` 替换为三项损失的加权组合（Eq. 5）：

1. **主体区域损失** `L_sub`（Eq. 2）：仅在主体掩码 **M** 内计算重建损失，使模型专注于学习主体外观，同时允许背景自由变化，从根本上阻断背景过拟合路径。
2. **视频保持损失** `L_vid`（Eq. 3）：在通用视频数据上联合训练，以标准重建损失维持预训练模型内化的运动先验和时序一致性。消融实验表明，移除该损失会导致视觉质量显著退化（Table 3）。
3. **主体令牌交叉注意力损失（STCA）** `L_stca`（Eq. 4）：通过二元交叉熵强制主体令牌 `[V]` 的交叉注意力图 **A** 与主体掩码 **M** 对齐，将主体令牌与空间位置显式绑定。这是后续免训练运动控制的**关键因果杠杆**——无 STCA 时，交叉注意力图无法与主体位置对齐（Figure 4），运动控制失去作用锚点。

### 改变槽位二：主体运动控制（从训练依赖到免训练交叉注意力编辑）

现有方法（如 GLIGEN）需要训练额外模块来实现主体位置控制，而 MotionBooth 利用 STCA 已建立的令牌-位置绑定关系，在推理时**直接编辑交叉注意力图**，实现免训练的主体运动控制。具体而言，通过在 Softmax 前的注意力分数上添加编辑矩阵 **S**（Eq. 6-7），在用户指定的边界框 **B_k** 内放大主体令牌的注意力权重，同时抑制其他区域。编辑强度由超参数 α 和时间窗口 τ 控制：α 过大会产生不自然的方形外观，τ 需在主体布局确定后、视频细节完成前施加（Figure 13a）。

### 改变槽位三：相机运动控制（从训练依赖到免训练潜空间偏移）

现有方法（如 **AnimateDiff**、**CameraCtrl**）需要大规模视频数据集训练专门的相机控制模块。MotionBooth 提出**潜空间偏移模块**（Eq. 8），在去噪过程的中间时间步对噪声潜变量 **z_t** 进行轴向采样、偏移、裁剪和填充，模拟相机平移运动。该方法的有效性建立在两个关键设计上：

- **轴对齐采样填充**：从原始潜变量的水平和垂直方向采样令牌来填充偏移后的空缺区域，相比随机填充、循环填充和反射填充，能提供更好的初始化质量和更平滑的视频过渡（Table 6c）。
- **主体令牌过滤**：采样时滤除主体相关令牌，因为主体不太可能出现在新场景区域，避免伪影。

该免训练方法在相机运动控制上**超越训练依赖的 CameraCtrl**，Flow error 从 1.683 降至 0.190，FVD 从 1468.53 降至 905.40（Table 2, Zeroscope）。

### 创新之间的因果耦合关系

上述三个改变槽位并非独立运作，而是形成**因果链条**：STCA 损失建立了主体令牌与空间位置的绑定（训练期），这使免训练的交叉注意力编辑能够精确控制主体运动（推理期）；同时，视频保持损失保护了预训练模型的运动先验，使潜空间偏移模块能够利用该先验生成连贯的相机运动。若移除任一环节，整个系统的控制精度和生成质量都会显著下降（Table 3 消融实验）。



![[assets/figures/papers/paper_list_l11_MotionBooth_Motion_Aware_Customized_Text_to_Video_Generation/figures/001_Figure_1.jpg]]
*Figure 1: Motion-aware customized video generation results of MotionBooth. Our method animates a customized object with controllable subject and camera motions*

MotionBooth 提出了一套统一的运动感知定制视频生成框架，其核心设计围绕一个关键瓶颈展开：**预训练 T2V 模型在主体微调过程中极易过拟合背景并丧失视频生成能力**，导致生成结果中运动匮乏或背景严重退化。为解决这一问题，MotionBooth 将整个流程划分为两个阶段——**主体学习阶段**和**免训练推理控制阶段**——分别通过损失增强训练和潜空间/注意力操纵来实现主体保真度、视频质量与运动可控性的三重平衡。

### 流程总览

如图 2 所示，MotionBooth 的整体管线包含以下关键模块及其数据流：

1. **主体学习阶段（训练时）**：输入为包含目标主体的少量图像及其掩码，以及一批通用视频数据。T2V 模型在三个互补损失的联合约束下进行微调：
   - **主体区域损失**（Subject Region Loss）：仅在主体掩码区域内计算扩散重建损失，抑制背景过拟合。
   - **视频保持损失**（Video Preservation Loss）：在通用视频数据上执行标准扩散重建，维持模型的视频生成先验。
   - **主体令牌交叉注意力损失**（STCA Loss）：强制主体令牌 `[V]` 的交叉注意力图与主体掩码对齐，建立令牌与空间位置之间的显式绑定。

2. **免训练推理控制阶段（推理时）**：接收用户指定的文本提示、主体运动边界框序列和相机运动信号 $c_{cam} = [c_x, c_y]$，在不引入额外训练的前提下实现双重运动控制：
   - **交叉注意力编辑模块**：通过向注意力分数矩阵添加编辑矩阵 $\mathbf{S}$，将主体令牌的注意力引导至目标边界框区域，实现主体运动控制。
   - **潜空间偏移模块**：对去噪过程中的噪声潜变量进行轴向采样、偏移、裁剪和填充，模拟相机平移运动。

### 模块间因果机制

框架设计的因果逻辑链可归纳为：

> **主体区域损失 + 视频保持损失** → 保持预训练运动先验，避免背景退化  
> **STCA 损失** → 将主体令牌与空间位置绑定，打通运动控制信号通道  
> **交叉注意力编辑** → 利用已绑定的令牌-位置映射，通过编辑注意力图实现免训练主体运动控制  
> **潜空间偏移** → 利用潜在空间的语义连续性假设，通过直接偏移噪声潜变量实现免训练相机运动控制

三个训练损失的协同作用至关重要：若仅使用主体区域损失，模型虽能保留主体外观，但背景仍趋于过平滑（Figure 3）；若移除视频保持损失，模型则完全丧失视频生成能力；若缺少 STCA 损失，主体令牌的交叉注意力图无法与主体位置对齐（Figure 4），后续的注意力编辑控制将失去基础。

### 输入输出规范

- **训练输入**：3–5 张主体图像 + 对应主体掩码 + 通用视频片段及文本描述
- **推理输入**：文本提示 + 主体运动边界框序列 + 相机运动比率 $c_x, c_y$
- **输出**：包含定制主体且主体运动和相机运动均可控的视频

### 与基线方法的关键差异

相比于 **DreamBooth**（Ruiz et al., CVPR 2023）等仅关注主体外观保持的定制方法，MotionBooth 的核心区别在于：

| 维度 | DreamBooth 类方法 | MotionBooth |
|------|-------------------|-------------|
| 背景处理 | 无显式约束，易过拟合 | 主体区域损失掩码化背景梯度 |
| 视频能力保持 | 无视频数据参与训练 | 视频保持损失联合训练 |
| 主体-位置绑定 | 隐式通过微调实现 | STCA 损失显式对齐注意力图与掩码 |
| 主体运动控制 | 需额外训练模块（如 GLIGEN） | 免训练交叉注意力编辑 |
| 相机运动控制 | 需训练专用模块（如 CameraCtrl） | 免训练潜空间偏移 |

这种设计使得 MotionBooth 在保持主体外观保真度的同时，无需任何额外训练即可灵活控制主体和相机运动，且实验表明其相机控制精度甚至超越了需要大规模数据训练的 **CameraCtrl**（Table 2）。



### 3.1 问题形式化与框架概览

MotionBooth 的目标是在给定一个主体（3~5 张图像）的条件下，生成该主体在指定主体运动和相机运动下的视频。框架分为两个阶段：**主体学习阶段**（训练时）和**运动控制阶段**（推理时）。整体流程如 Figure 2 所示。

输入包括：主体图像集、对应的主体掩码 $\mathbf{M}$、主体类别令牌、主体运动信号（边界框序列 $\mathbf{B}$）和相机运动信号 $\mathbf{c}_{cam} = [c_x, c_y]$（水平与垂直移动比例）。

### 3.2 主体学习阶段：三项损失函数

主体学习阶段的核心瓶颈在于：直接对预训练 T2V 模型进行主体微调会导致**背景过拟合**和**视频生成能力退化**。MotionBooth 通过三项损失函数协同解决这一问题。

#### 标准扩散重建损失

基础 T2V 模型在图像数据上微调时，通常采用标准扩散重建损失：

$$\mathcal{L} = \mathbb{E}_{\mathbf{z}, \epsilon \sim \mathcal{N}(\mathbf{0}, \mathbf{I}), t, \mathbf{c}} \left[ || \epsilon - \epsilon_{\theta}(\mathbf{z}_t, \mathbf{c}, t) ||_2^2 \right] \quad \text{(Eq. 1)}$$

其中 $\mathbf{z}_t$ 为时间步 $t$ 的噪声潜变量，$\epsilon$ 为真实噪声，$\epsilon_{\theta}$ 为模型预测噪声，$\mathbf{c}$ 为文本条件。该损失在整帧上均匀计算，是背景过拟合的直接原因。

#### 主体区域损失（Subject Region Loss）

为阻止模型学习背景信息，MotionBooth 将重建损失限制在主体掩码区域内：

$$\mathcal{L}_{sub} = \mathbb{E}_{\mathbf{z}, \epsilon \sim \mathcal{N}(\mathbf{0}, \mathbf{I}), t, \mathbf{c}} \left[ || (\epsilon - \epsilon_{\theta}(\mathbf{z}_t, \mathbf{c}_i, t)) \cdot \mathbf{M} ||_2^2 \right] \quad \text{(Eq. 2)}$$

其中 $\mathbf{M}$ 为主体二值掩码（1 表示主体区域，0 表示背景），$\mathbf{c}_i$ 为主体图像对应的文本条件。该损失仅在主体区域内施加监督信号，从根本上切断了背景过拟合的梯度通路。消融实验（Table 3）表明，移除该损失（w/o mask）导致主体保真度 R-DINO 下降约 0.256。

#### 视频保持损失（Video Preservation Loss）

仅使用主体区域损失虽能保护背景，但模型仍会因缺乏视频数据而丧失视频生成能力。MotionBooth 引入视频保持损失，在通用视频数据上进行联合训练：

$$\mathcal{L}_{vid} = \mathbb{E}_{\mathbf{z}, \epsilon \sim \mathcal{N}(\mathbf{0}, \mathbf{I}), t, \mathbf{c}} \left[ || \epsilon - \epsilon_{\theta}(\mathbf{z}_t, \mathbf{c}_v, t) ||_2^2 \right] \quad \text{(Eq. 3)}$$

其中 $\mathbf{c}_v$ 为通用视频的文本描述。该损失在标准视频数据上计算完整帧的重建损失，维持预训练 T2V 模型中蕴含的运动先验和时序一致性知识。Figure 3 的定性消融显示，无视频保持损失时生成的视频背景过平滑且运动匮乏；加入后背景恢复多样性和自然动态。Table 3 的定量消融进一步证实，移除该损失导致视频质量指标（CLIP-T、T-Cons.）显著恶化。

#### 主体令牌交叉注意力损失（STCA Loss）

上述两项损失解决了背景和视频质量问题，但并未建立主体令牌与空间位置之间的显式关联，导致后续运动控制缺乏可操作的“手柄”。MotionBooth 提出 STCA 损失，强制主体令牌 $[\mathrm{V}]$ 的交叉注意力图 $\mathbf{A}$ 与主体掩码 $\mathbf{M}$ 对齐：

$$\mathcal{L}_{stca} = -\left[ \mathbf{M} \log(\mathbf{A}) + (1 - \mathbf{M}) \log(1 - \mathbf{A}) \right] \quad \text{(Eq. 4)}$$

这是一个标准的二元交叉熵损失。其因果机制在于：通过梯度反传，模型学习将 $[\mathrm{V}]$ 令牌的注意力权重集中在主体掩码对应的空间位置，而类别令牌（如“dog”）的注意力则被推离该区域。Figure 4 的可视化对比清晰地展示了这一效果——无 STCA 损失时，$[\mathrm{V}]$ 和“dog”的注意力图均呈散乱分布；加入 STCA 后，$[\mathrm{V}]$ 的注意力精确聚焦于主体区域，为后续推理时的交叉注意力编辑提供了精确的空间绑定基础。

#### 总体训练损失

三项损失的加权组合构成训练总目标：

$$\mathcal{L} = \mathcal{L}_{sub} + \lambda_{1} \mathcal{L}_{vid} + \lambda_{2} \mathcal{L}_{stca} \quad \text{(Eq. 5)}$$

其中 $\lambda_1 = 1.0$，$\lambda_2 = 0.01$。训练使用 AdamW 优化器（学习率 $5 \times 10^{-2}$，权重衰减 $1 \times 10^{-2}$），共 300 步。

### 3.3 推理时主体运动控制：交叉注意力编辑

主体学习阶段建立的令牌-空间绑定，使得推理时可通过直接编辑交叉注意力图来实现免训练的主体运动控制。

核心操作为在标准交叉注意力的 Softmax 输入中添加编辑矩阵 $\mathbf{S}$：

$$\mathrm{EditedCrossAttn}(\mathbf{Q}, \mathbf{K}, \mathbf{V}) = \mathrm{Softmax}\left( \frac{\mathbf{Q} \mathbf{K}^{\top}}{\sqrt{d}} + \alpha \mathbf{S} \right) \mathbf{V} \quad \text{(Eq. 6)}$$

其中 $\mathbf{Q}$、$\mathbf{K}$、$\mathbf{V}$ 分别为查询、键、值矩阵，$d$ 为特征维度，$\alpha$ 为编辑强度超参数。

编辑矩阵 $\mathbf{S}$ 的定义为：

$$S_{k}[i,j] = \begin{cases} 1 - \frac{|\mathbf{B}_{k}|}{|\mathbf{Q}|}, & \text{if } i \in \mathbf{B}_{k} \text{ and } j \in \mathbf{P} \text{ and } t \geq \tau \\ 0, & \text{if } i \in \mathbf{B}_{k} \text{ and } j \in \mathbf{P} \text{ and } t < \tau \\ -\infty, & \text{otherwise} \end{cases} \quad \text{(Eq. 7)}$$

该矩阵的因果逻辑如下：
- **空间维度**：在边界框 $\mathbf{B}_k$ 区域内，对主体令牌集合 $\mathbf{P}$（包含 $[\mathrm{V}]$ 和类别令牌）的注意力分数施加正向偏置；区域外设为 $-\infty$（Softmax 后趋近于 0）。
- **幅度自适应**：偏置值 $1 - \frac{|\mathbf{B}_k|}{|\mathbf{Q}|}$ 根据边界框相对面积动态调整——框越小，偏置越大，确保小目标也能获得足够的注意力强度。
- **时间步门控**：仅在去噪时间步 $t \geq \tau$ 时施加编辑。早期去噪步（$t < \tau$）不干预，让模型自由确定整体布局；后期去噪步施加控制，精确定位主体。

消融实验（Figure 13a）表明：增大 $\alpha$ 和延长编辑时间窗口 $\tau$ 可增强控制强度，但过强会导致主体外观出现不自然的方形伪影。

### 3.4 推理时相机运动控制：潜空间偏移

MotionBooth 提出一种免训练的潜空间偏移方法来实现相机运动控制，其核心思想是：在去噪过程的特定时间窗口内，根据相机运动信号 $\mathbf{c}_{cam} = [c_x, c_y]$ 直接偏移噪声潜变量 $\mathbf{z}_t$。

操作流程如下（Eq. 8）：

$$\begin{array} { r l } & { { \mathbf{h} } _ { x } = { \mathrm { SampleHorizontal } } ( { \mathbf{z} } _ { t } , { \mathbf{B} } , c _ { x } ) , } \\ & { { \mathbf{h} } _ { y } = { \mathrm { SampleVertical } } ( { \mathbf{z} } _ { t } , { \mathbf{B} } , c _ { y } ) , } \\ & { { \mathbf{z} } _ { \mathrm { shift } } = { \mathrm { Crop } } ( { \mathrm { Shift } } ( { \mathbf{z} } _ { t } , c _ { x } , c _ { y } ) ) , } \\ & { { \mathbf{z} } _ { t } = { \mathrm { Fill } } ( { \mathbf{z} } _ { \mathrm { shift } } , { \mathbf{h} } _ { x } , { \mathbf{h} } _ { y } , c _ { x } , c _ { y } ) , } \end{array}$$

具体步骤为：
1. **轴向采样**：从原始潜变量 $\mathbf{z}_t$ 中沿水平方向采样 $\mathbf{h}_x$（用于填充垂直偏移产生的空缺）和沿垂直方向采样 $\mathbf{h}_y$（用于填充水平偏移产生的空缺）。采样时过滤掉主体令牌对应的区域 $\mathbf{B}$，因为主体不太可能出现在新暴露的场景区域。
2. **偏移与裁剪**：将 $\mathbf{z}_t$ 按 $c_x$、$c_y$ 偏移后裁剪出有效区域，得到 $\mathbf{z}_{\mathrm{shift}}$。
3. **填充**：用采样得到的 $\mathbf{h}_x$ 和 $\mathbf{h}_y$ 填充 $\mathbf{z}_{\mathrm{shift}}$ 中的空缺区域。

该方法的关键设计在于**轴对齐采样填充**。消融实验（Table 6c）对比了随机填充、循环填充和反射填充，轴对齐采样在保持视觉质量和相机运动灵活性方面均显著优于其他方案。其因果机制在于：自然视频中，水平移动暴露的新内容与原始帧的水平邻域具有语义连续性，垂直移动亦然；轴向采样利用了潜空间中的这一语义连续性假设，为去噪过程提供了更合理的初始化。

时间窗口方面，潜空间偏移仅在去噪步 $[\sigma_1, \sigma_2]$ 内执行——需在主体布局大致确定之后、视频细节完成之前施加。消融（Figure 13b）表明，过早偏移会破坏布局，过晚则无法产生有效的相机运动效果。

Table 2 的定量结果表明，该免训练方法在 Flow error 和 FVD 上均显著优于需要大规模训练的 **CameraCtrl**（Flow error：0.190 vs 1.683；FVD：905.40 vs 1468.53，基于 Zeroscope），验证了潜空间偏移作为相机控制机制的有效性。



## 实验与关键发现

### 实验设置

MotionBooth 基于两个公开的预训练文本到视频（T2V）扩散模型进行评估：**Zeroscope** 和 **LaVie**。训练使用 AdamW 优化器，学习率设为 $5 \times 10^{-2}$，权重衰减 $1 \times 10^{-2}$，共训练 300 步。损失权重超参数 $\lambda_1$ 和 $\lambda_2$ 分别设为 1.0 和 0.01。主体运动控制中，交叉注意力编辑的强度 $\alpha$ 和时间阈值 $\tau$ 需在推理时设定；相机运动控制中，潜空间偏移仅作用于去噪时间步区间 $[\sigma_1, \sigma_2]$——即主体布局已大致确定但视频细节尚未完成的时间窗口。

评估数据集包含 26 个主体和 40 个文本-运动对，用于运动感知定制视频生成评测；相机运动控制评测则在 MSRVTT 子集上进行。指标方面，采用 **R-CLIP** 和 **R-DINO** 衡量主体保真度与文本对齐，**CLIP-T** 评估文本-视频语义一致性，**T-Cons.** 衡量时序一致性，**Flow error** 评估运动控制精度（光流误差），**FVD** 评估视频整体质量。

### 主实验结果

#### 运动感知定制视频生成

Table 1 展示了在 Zeroscope 和 LaVie 两个骨干模型上的定量对比。MotionBooth 在所有指标上均优于现有基线方法。


![[assets/figures/papers/paper_list_l11_MotionBooth_Motion_Aware_Customized_Text_to_Video_Generation/figures/006_Table_1.jpg]]
*Table 1: Quantitative comparison for motion-aware customized video generation*

在 Zeroscope 骨干上，MotionBooth 的 R-CLIP 达到 **0.667**，相比 DreamBooth（Ruiz et al., CVPR 2023）的 0.608 提升了 +0.059；R-DINO 达到 **0.306**，相比 DreamBooth 的 0.279 提升了 +0.027。更为显著的是 Flow error：MotionBooth 仅 **0.252**，而 DreamBooth 高达 0.690，降低了 0.438——这表明 DreamBooth 在主体微调后几乎丧失了运动生成能力，生成的视频近乎静态。CustomVideo 和 DreamVideo 等参数高效或运动学习基线同样表现不佳，Flow error 分别为 0.432 和 0.604。

在 LaVie 骨干上，趋势一致。MotionBooth 的 R-CLIP 为 0.739，R-DINO 为 0.504，Flow error 仅 0.259，全面领先。值得注意的是，LaVie 本身的视频生成质量（FVD）优于 Zeroscope，MotionBooth 在其基础上进一步降低了 FVD。

**公平性说明**：对于不支持内在运动控制的基线方法（DreamBooth、CustomVideo、DreamVideo），实验统一应用了 MotionBooth 提出的相机和主体运动控制技术，确保对比聚焦于主体学习质量本身。

#### 相机运动控制

Table 2 展示了相机运动控制的定量对比。MotionBooth 的免训练潜空间偏移方法显著优于需要大规模数据训练的 CameraCtrl 和 AnimateDiff。


![[assets/figures/papers/paper_list_l11_MotionBooth_Motion_Aware_Customized_Text_to_Video_Generation/figures/007_Table_2.jpg]]
*Table 2: Quantitative comparison for camera movement control*

在 Zeroscope 骨干上，MotionBooth 的 Flow error 仅 **0.190**，而 CameraCtrl 高达 1.683，降低了 **1.493**；FVD 为 **905.40**，CameraCtrl 为 1468.53，降低了 563.13。在 LaVie 骨干上，MotionBooth 的 Flow error 为 0.296，FVD 为 **723.26**，同样大幅领先。这些结果表明，训练自由的潜空间偏移不仅能精确控制相机运动，还能保持更高的视频质量，而训练方法（如 CameraCtrl）可能因引入额外模块而损害生成质量。

定性结果（Figure 6、Figure 7）进一步印证：MotionBooth 生成的主体外观保持度高，主体运动与文本描述一致，相机运动平滑自然；而基线方法常出现主体变形、运动匮乏或背景退化等问题。


![[assets/figures/papers/paper_list_l11_MotionBooth_Motion_Aware_Customized_Text_to_Video_Generation/figures/008_Figure_6.jpg]]
*Figure 6: Qualitative comparison of customizing objects and controlling their motions. Figure 7: Qualitative comparison of camera motion control. Lines and points are used to help the readers track the camera movement more easily*

### 消融实验

#### 训练损失项的消融（Table 3）

Table 3 系统消融了三个核心训练损失项在 LaVie 上的贡献：


![[assets/figures/papers/paper_list_l11_MotionBooth_Motion_Aware_Customized_Text_to_Video_Generation/figures/009_Table_3.jpg]]
*Table 3: Ablation study for training technologies. “mask” means subject region loss. “STCA” means subject token cross-attention loss. “video” means video preservation loss. “w/ class video” means utilizing class-specific videos in video preservation loss. The results are evaluated on LaVie*

- **移除主体区域损失（w/o mask）**：R-DINO 从完整模型的 0.472 骤降至约 0.216（降低约 0.256），表明不对背景进行掩码会导致模型过拟合背景，严重损害主体保真度。
- **移除 STCA 损失（w/o STCA）**：Flow error 显著上升，主体运动控制能力下降。Figure 4 的可视化显示，无 STCA 时交叉注意力图分散，无法聚焦于主体位置；加入 STCA 后注意力图与主体掩码精确对齐。
- **移除视频保持损失（w/o video）**：视觉质量严重退化。Figure 3 的定性案例表明，仅使用主体区域损失会导致背景过平滑且缺乏多样性；加入视频保持损失后，模型恢复了生成丰富动态背景的能力。
- **使用类别特定视频（w/ class video）**：相比使用通用视频数据，性能略有下降，说明通用视频的多样性对保持视频生成先验更为有效。


![[assets/figures/papers/paper_list_l11_MotionBooth_Motion_Aware_Customized_Text_to_Video_Generation/figures/003_Figure_3.jpg]]
*Figure 3: Case study on subject learning. “Region” indicates subject region loss. “Video” indicates video preservation loss. The images are extracted from generated videos*

![[assets/figures/papers/paper_list_l11_MotionBooth_Motion_Aware_Customized_Text_to_Video_Generation/figures/004_Figure_4.jpg]]
*Figure 4: Case study on subject token cross-attention maps. (b) and (c) are visualization of cross-attention maps on token$s ^ { 6 6 } [ \mathrm { V } ] ^ { , , }$ and “dog”*

#### 视频保持数据数量（Table 5）

保持视频的数量在 100 到 900 之间变化时，各指标波动不大。这表明关键因素是**引入视频数据本身**来激活预训练模型的视频生成能力，而非视频数量的多少。

#### 训练图像掩码方式（Table 6b）

若直接对训练图像进行掩码（即将主体区域外的像素置零输入模型），而非仅对损失函数进行掩码，R-DINO 从 0.472 暴跌至 **0.060**。这是因为输入掩码破坏了图像的全局上下文，使模型无法学习到合理的主体-背景关系，严重损害主体学习。

#### 潜空间填充方法（Table 6c）

消融了四种填充策略：随机填充、循环填充、反射填充和所提出的轴对齐采样填充。轴对齐采样填充在保持视觉质量和相机运动灵活性方面均优于其他方法。随机填充会引入不自然的纹理断裂，循环和反射填充则可能在边界处产生明显的重复伪影。

#### 运动控制超参数（Figure 13）

- **交叉注意力编辑强度 $\alpha$** 和 **编辑时间步阈值 $\tau$**：增大 $\alpha$ 和延长 $\tau$ 会增强主体运动控制强度，但过强（$\alpha$ 过大）会导致主体出现不自然的方形外观。需要在控制精度和视觉自然度之间权衡。
- **潜空间偏移时间窗口 $[\sigma_1, \sigma_2]$**：最佳窗口为中间去噪步。过早偏移（主体布局未定）会导致运动与内容不协调，过晚偏移（细节已固化）则无法有效改变相机视角。

### 人类偏好研究

Figure 8 展示了人类偏好研究结果。评估维度包括主体外观对齐、运动控制精度和整体视频质量。MotionBooth 在所有维度和所有对比模型中获得最高偏好分数，尤其在主体外观对齐方面优势显著——这直接受益于主体区域损失和 STCA 损失对主体学习的增强。

### 失败模式与局限性

Figure 9 展示了 MotionBooth 的典型失败案例，结合分析可知主要局限包括：

1. **非常规主体-运动组合**：在非动物物体上施加动物运动（如让花瓶奔跑）时，主体可能发生严重变形。模型缺乏对物理合理性的理解。
2. **多主体交互与遮挡**：无法有效处理多个主体之间的复杂空间关系和遮挡场景，主体令牌的交叉注意力绑定在多主体情况下会产生冲突。
3. **极端相机运动**：当相机运动速度极高（偏移量超过画面宽度）时，潜空间偏移可能产生平铺效应，新填充区域与原有内容不连贯。
4. **过度运动控制**：交叉注意力编辑强度过大时，主体边缘出现不自然的方形轮廓，破坏视觉质量。
5. **主体掩码依赖**：训练需要精确的主体掩码（手动或自动获取），增加了实际应用的成本和复杂度。
6. **潜空间语义连续性假设**：相机控制依赖于潜在空间在空间维度上的语义连续性，在某些场景（如复杂纹理或非均匀背景）下该假设可能不成立，导致填充区域不协调。

### 补充图表

![[assets/figures/papers/paper_list_l11_MotionBooth_Motion_Aware_Customized_Text_to_Video_Generation/figures/014_Figure_12.jpg]]
*Figure 12: Up Right A playful puppy frolicking in flowers (g) Examples of controlling both subject and camera (h) Comparison of latent shift and text guidance to motion. control camera motion. Figure 12: More qualitative results*

![[assets/figures/papers/paper_list_l11_MotionBooth_Motion_Aware_Customized_Text_to_Video_Generation/figures/019_Table_6.jpg]]
*Table 6: More ablation studies. (a) Ablation of controlling single (b) Ablation of masking the training (c) Ablation of the latent filling motion type. images. method in latent shift*

![[assets/figures/papers/paper_list_l11_MotionBooth_Motion_Aware_Customized_Text_to_Video_Generation/figures/021_Figure_15.jpg]]
*Figure 15: More qualitative results of our MotionBooth*

![[assets/figures/papers/paper_list_l11_MotionBooth_Motion_Aware_Customized_Text_to_Video_Generation/figures/015_Table_4.jpg]]
*Table 4: Comparison with More Baselines. (a) Comparison of the latent shift method and text (b) Comparison of subject motion control with more guidance for camera motion control. baselines*

![[assets/figures/papers/paper_list_l11_MotionBooth_Motion_Aware_Customized_Text_to_Video_Generation/figures/016_Table.jpg]]




## 定位与知识库关联

MotionBooth 的核心技术路径是在预训练文本到视频（T2V）扩散模型之上，通过**损失增强的主体微调**与**免训练的推理时操控**两个阶段，实现主体外观、主体运动与相机运动的联合可控生成。其方法定位可从三个维度进行谱系梳理：主体定制、运动控制、以及相机运动生成。

### 主体定制方法的继承与改进

MotionBooth 直接继承了 **DreamBooth**（Ruiz et al., CVPR 2023）的主体定制范式——使用稀有令牌（`[V]`）绑定特定主体，并通过微调将主体外观注入预训练模型。然而，DreamBooth 面向图像生成，直接迁移到视频模型时暴露出两个关键瓶颈：**背景过拟合**与**视频生成能力退化**（见 Figure 3）。MotionBooth 的解决方案是引入两项针对性损失：

- **主体区域损失**（Subject Region Loss）：将扩散重建损失的计算范围限制在主体掩码 $\mathbf{M}$ 内，从因果机制上阻断背景像素对梯度更新的贡献，从而防止模型将背景“记住”为主体的一部分。
- **视频保持损失**（Video Preservation Loss）：在主体微调的同时，联合训练通用视频数据，迫使模型维持对时序动态的建模能力。这一设计的关键洞察是：微调不应只“教”模型认识新主体，还应持续“提醒”它如何生成视频。

与之相比，**CustomVideo** 和 **DreamVideo** 等参数高效的视频定制方法（具体出处未在分析中提供，需手动核实）虽然也关注主体学习效率，但未显式处理背景过拟合与视频先验保持问题。消融实验表明，移除视频保持损失会导致视觉质量显著退化，而仅使用类别特定视频（而非通用视频）作为保持数据效果更差（Table 3），说明通用视频数据的多样性对维持视频生成泛化能力至关重要。

### 运动控制方法的谱系定位

在主体运动控制方面，现有方法通常需要训练额外模块（如 GLIGEN 的 grounded generation 范式）或从视频中学习特定运动模式。MotionBooth 选择了一条**免训练**路径，其关键使能技术是**主体令牌交叉注意力损失**（STCA Loss）：

$$\mathcal{L}_{stca} = -\left[ \mathbf{M} \log(\mathbf{A}) + (1 - \mathbf{M}) \log(1 - \mathbf{A}) \right]$$

STCA 通过二元交叉熵将主体令牌 `[V]` 和类别令牌的交叉注意力图 $\mathbf{A}$ 与主体掩码 $\mathbf{M}$ 对齐。这一设计的因果逻辑是：如果微调阶段已经将令牌与空间位置绑定，那么推理时只需编辑交叉注意力分数即可控制主体位置，无需额外训练。推理时的编辑通过向注意力分数添加编辑矩阵 $\mathbf{S}$ 实现：

$$\mathrm{EditedCrossAttn}(\mathbf{Q}, \mathbf{K}, \mathbf{V}) = \mathrm{Softmax}\left( \frac{\mathbf{Q} \mathbf{K}^{\top}}{\sqrt{d}} + \alpha \mathbf{S} \right) \mathbf{V}$$

编辑矩阵 $\mathbf{S}$ 在边界框 $\mathbf{B}_k$ 内放大主体令牌的注意力权重，强度由超参数 $\alpha$ 和时间步阈值 $\tau$ 控制。消融实验（Figure 13a）表明，增大 $\alpha$ 或延长 $\tau$ 会增强控制强度，但过强时会产生不自然的方形外观，揭示了注意力编辑方法在控制精度与视觉自然度之间的固有权衡。

### 相机运动控制的创新定位

相机运动控制是 MotionBooth 方法谱系中最具差异化的贡献。现有方法如 **AnimateDiff** 和 **CameraCtrl** 依赖大规模视频数据集训练专门的相机运动模块，不仅计算成本高，且与特定基础模型耦合紧密。MotionBooth 提出的**潜空间偏移**（Latent Shift）方法则完全免训练，其核心假设是：扩散模型去噪过程中的噪声潜变量在空间上具有语义连续性，因此可以通过轴向平移潜变量来模拟相机运动。

具体操作（Eq. 8）包括四个步骤：从原始潜变量 $\mathbf{z}_t$ 中沿水平和垂直方向采样填充令牌 $\mathbf{h}_x, \mathbf{h}_y$；按相机运动参数 $c_x, c_y$ 偏移潜变量；裁剪超出边界的部分；用采样令牌填充空白区域。消融实验（Table 6c）证实，轴对齐采样填充方法在视觉质量和运动灵活性上优于随机填充、循环填充和反射填充。

定量比较（Table 2）显示，MotionBooth 的潜空间偏移在 Flow error 上大幅超越 CameraCtrl（Zeroscope 上 0.190 vs 1.683），FVD 也显著更低（905.40 vs 1468.53）。这一结果值得注意的公平性考量是：论文为不支持内在运动控制的基线方法（DreamBooth、CustomVideo、DreamVideo）同样应用了 MotionBooth 的相机和主体运动控制技术（见 fairness_notes），因此 Table 1 中的比较实际上是在控制运动控制能力的前提下评估主体定制质量。

### 适用边界与局限

MotionBooth 的能力边界受限于以下约束：

1. **主体-运动语义匹配**：当对非动物物体应用动物运动（如让花瓶“跳跃”）时，模型会产生严重变形（Figure 9），说明交叉注意力编辑无法弥补高层语义理解的缺失。
2. **多主体交互**：方法无法处理多个主体之间的复杂交互和遮挡，因为 STCA 损失和注意力编辑均基于单一主体掩码设计。
3. **极端相机运动**：在相机运动速度超过画面宽度时，潜空间偏移会出现平铺效应，性能下降。这源于填充机制无法生成真正的新内容，而只是复制已有潜变量。
4. **训练数据依赖**：需要手动或自动获取精确的主体掩码用于训练，增加了实际应用成本。
5. **潜空间连续性假设**：相机控制依赖的潜空间语义连续性假设在某些场景可能不成立，例如涉及大幅度视点变化时。

### 开放问题

从方法谱系演进的角度，以下问题值得后续工作关注：

- 如何将运动控制信号从边界框扩展为更丰富的表示（光流、关键点、骨架），以支持更精细的主体运动描述？
- 潜空间偏移能否从平移运动扩展到旋转、缩放等非平移相机轨迹？这可能需要与 3D 感知或单视角重建技术结合。
- 如何减少对精确主体掩码的依赖，实现完全自动化的训练流程？
- 是否可能通过在线学习或测试时自适应来增强模型在极端运动条件下的鲁棒性？
- 如何降低同时启用主体和相机控制时的推理延迟，使方法更适用于实时应用场景？



## 原文 PDF

![[paperPDFs/NEURIPS_2024/MotionBooth_Motion_Aware_Customized_Text_to_Video_Generation.pdf]]
