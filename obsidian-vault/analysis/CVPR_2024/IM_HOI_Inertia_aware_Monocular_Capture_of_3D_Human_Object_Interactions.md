---
title: "I’M HOI: Inertia-aware Monocular Capture of 3D Human-Object Interactions"
type: paper
paper_level: A
venue: CVPR
year: 2024
pdf_ref: paperPDFs/CVPR_2024/IM_HOI_Inertia_aware_Monocular_Capture_of_3D_Human_Object_Interactions.pdf
project_link: null
code_link: null
aliases:
- IMH
- IMHIAMC3HOI
tags:
- CVPR_2024
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
core_operator: 引入物体端的惯性测量单元（IMU）信号，为物体运动提供遮挡鲁棒的位姿先验，并与单目RGB视频进行多模态融合。
primary_logic: 将捕捉问题解耦为通用运动推断和类别特定运动细化两个阶段，利用物体IMU先验进行端到端跟踪，再通过扩散模型在学习的交互流形上对粗糙结果进行校正和补全，从而在最小化传感器配置下实现高精度、生动的交互运动捕捉。
claims:
- I'm-HOI在IMHD2快速交互子集上的物体跟踪精度（CD）比最优基线CHORE提升约9.9cm。
- 全流水线（包括反馈、优化、扩散滤波）比朴素实现性能提高4倍。
- 引入IMU模态后，基线方法的跟踪精度显著提升，而我们的方法进一步提升并达到最优。
- I'm-HOI每帧推理仅需约0.5秒，相较于VisTracker的20秒、CHORE的约1分钟、PHOSA的约2分钟，速度优势极大。
---

# I’M HOI: Inertia-aware Monocular Capture of 3D Human-Object Interactions

> [!tip] 核心洞察
> 将捕捉问题解耦为通用运动推断和类别特定运动细化两个阶段，利用物体IMU先验进行端到端跟踪，再通过扩散模型在学习的交互流形上对粗糙结果进行校正和补全，从而在最小化传感器配置下实现高精度、生动的交互运动捕捉。

| 字段 | 内容 |
|------|------|
| 中文题名 | I’M HOI：惯性感知的单目三维人物-物体交互捕捉 |
| 英文题名 | I’M HOI: Inertia-aware Monocular Capture of 3D Human-Object Interactions |
| 会议/期刊 | CVPR 2024 |
| Links |  |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction |
| Method | I’m-HOI |
| Dataset | IMHD2, Runtime |

> [!tip] 效果简介
> - IMHD2 (快速交互序列) 上，CD per-frame (人体/物体) [cm] 6.50 / 6.93 vs CHORE 14.20 / 16.81 (-7.70 / -9.88)。
> - Runtime (推理速度) 上，每帧推理时间 (s) ~0.5 vs VisTracker ~20 (快约40倍)。

## 概要

**核心问题**：现有单目人体-物体交互（HOI）捕捉方法在遮挡、深度模糊及快速运动条件下，对物体位姿的鲁棒估计能力严重不足，成为制约复杂交互场景整体捕捉精度的瓶颈。

**核心思路**：本文提出 **I’m-HOI**，一种惯性感知的单目三维人物-物体交互捕捉方法。其核心在于将捕捉问题解耦为两个阶段：**通用运动推断**与**类别特定运动细化**。第一阶段通过端到端的多模态融合，将物体视为人体额外关节，利用物体端惯性测量单元（IMU）信号为物体运动提供遮挡鲁棒的位姿先验，并与单目RGB视频进行整体跟踪；第二阶段则通过条件扩散模型，在学习的交互流形上对粗糙结果进行去噪校正与手部动作补全，从而在最小化传感器配置（单目RGB + 单IMU）下实现高精度、生动的交互运动捕捉。

**关键结论**：
- 在IMHD2数据集的快速交互子集上，I’m-HOI的物体跟踪精度（Chamfer Distance）比最优基线 **CHORE**（Xie et al., ECCV 2022）提升约9.9 cm（Table 1）。
- 全流水线（含网格对齐反馈、轻量优化及扩散滤波）相比朴素实现性能提升约4倍（Section 5.3）。
- 推理速度约0.5秒/帧，显著优于 **VisTracker**（Xie et al., CVPR 2023）的约20秒/帧及CHORE的约1分钟/帧（Runtime Cost 段落）。
- 输入模态消融实验表明，引入IMU信号后各基线方法跟踪精度均有提升，而本文的多模态深度融合方法在此基础上达到最优（Table 4）。

### 问题背景：单目三维人物-物体交互捕捉

从单目RGB视频中恢复三维人体与物体的交互运动，是计算机视觉与图形学领域的一项基础性挑战。该任务要求同时估计人体姿态、物体位姿以及两者之间的空间关系，在增强现实、机器人学习、运动分析等应用中具有广泛需求。然而，单目设置固有的深度歧义、自遮挡与交互遮挡，使得这一任务在复杂动态场景下尤为困难。

### 现有方法的瓶颈

早期方法如 **PHOSA**（Zhang et al., ECCV 2020）将人体与物体分开重建，再通过接触约束进行后优化，但该范式依赖单帧图像，缺乏时序一致性，且对遮挡极为敏感。**CHORE**（Xie et al., ECCV 2022）通过联合建模人体、物体与接触区域改善了单帧重建质量，但在视频场景中仍采用逐帧处理策略，未充分利用时序信息。**VisTracker**（Xie et al., CVPR 2023）将跟踪引入HOI捕捉，通过视频级优化提升了时序连贯性，然而其推理速度极慢（每帧约20秒），且纯视觉方案在快速运动或严重遮挡下仍会出现物体位姿漂移。

核心瓶颈可归纳为：**在遮挡、深度模糊及快速运动情形下，现有单目方法对物体位姿的鲁棒估计能力严重不足**。视觉信号在物体被人体大面积遮挡或纹理稀疏时近乎失效，而物体运动恰恰是决定交互质量的关键因素。

### 核心动机：以惯性信号弥补视觉脆弱性

本文的核心洞察在于引入一种廉价且遮挡鲁棒的传感模态——**物体端惯性测量单元（IMU）**。IMU直接测量物体的加速度与角速度，其信号不依赖于视线可见性，天然免疫于视觉遮挡。将单目RGB与物体端单IMU进行多模态融合，有望以极低的传感器成本（仅需在物体上贴附一个IMU）大幅提升复杂交互场景下的捕捉鲁棒性。

然而，IMU信号本身存在漂移、噪声大，且仅提供局部运动信息，无法独立求解全局位姿。因此，**如何有效地将IMU先验嵌入视觉跟踪流程，并处理两种模态在频率特性与误差模式上的差异**，构成了本文方法设计的核心驱动力。

### 方法概览：两阶段解耦范式

为解决上述挑战，本文提出**I’m-HOI**，采用一种两阶段解耦范式（见Figure 2）：

1. **通用交互运动推断（General Interaction Motion Inference）**：将物体视为人体的额外“肢体关节”，在端到端框架中联合估计人体-物体的空间布局。通过网格对齐反馈机制，将IMU信号与RGB特征逐步融合，获得遮挡鲁棒的粗糙跟踪结果。

2. **类别特定交互扩散滤波器（Category-specific Interaction Diffusion Filter）**：以粗糙跟踪结果和原始IMU信号为条件，利用条件扩散模型在学习的交互运动流形上进行去噪与手部动作补全，生成物理合理且视觉生动的精细交互运动。

该范式将“鲁棒跟踪”与“运动细化”解耦，使第一阶段专注于利用多模态信号实现遮挡鲁棒的位姿估计，第二阶段则利用数据驱动的交互先验校正残差并补全细节，从而在最小化传感器配置下实现高精度、高效率的交互运动捕捉。

## 核心方法与创新机理

I’m-HOI 的核心创新在于将单目三维人物-物体交互（HOI）捕捉问题重新定义为一个**惯性感知的多模态融合问题**，并通过“通用推断-类别细化”的两阶段范式加以解决。相较于现有纯视觉方法，该方法在三个关键维度上实现了根本性改变：传感器模态、人体-物体跟踪范式，以及运动细化策略。

### 1. 传感器模态：从纯视觉到视觉-惯性融合

现有单目HOI方法（如 **PHOSA** (Zhang et al., ECCV 2020)、**CHORE** (Xie et al., ECCV 2022)、**VisTracker** (Xie et al., CVPR 2023)）完全依赖RGB图像进行人体和物体的位姿估计。当面临快速运动、严重遮挡或深度模糊时，纯视觉信号所能提供的约束急剧减弱，导致物体跟踪精度大幅下降——这是当前方法的真实瓶颈。

I’m-HOI 在单目RGB基础上引入**物体端单个惯性测量单元（IMU）**，构成“单目RGB + 单IMU”的最小传感器配置。IMU直接提供物体在三维空间中的加速度和角速度读数，这些信号**不受视觉遮挡影响**，能够在视觉线索失效时为物体运动提供持续、鲁棒的位姿先验。实验证据表明，仅将IMU作为额外约束项（Eq.4）加入纯视觉基线方法即可带来显著的跟踪精度提升，而I’m-HOI通过深度多模态融合进一步将性能推向最优（Table 4）。

### 2. 人体-物体跟踪范式：从分离式处理到端到端整体联合跟踪

传统方法通常将人体与物体视为独立实体分别估计，再通过后处理步骤协调二者的空间关系（如CHORE的“拟合-学习-优化”流程）。这种分离式范式割裂了交互过程中人体与物体之间的物理耦合，难以捕捉“人带动物体”或“物体影响人体”的协同运动模式。

I’m-HOI 提出**将物体视为人体的一个额外肢体关节**，在统一的端到端框架中整体估计人体-物体的空间布局。具体而言，通用交互运动推断模块首先通过多尺度CNN估计人体3D关键点，再经由逆运动学（IK）优化层回归姿态与体型参数；物体的初始位姿则由IMU积分提供，并通过**网格对齐反馈循环**（mesh-aligned feedback）与RGB图像特征进行迭代融合校正——渲染物体网格剪影与真实掩码的面积差异（Eq.1）被用作反馈信号，逐步将物体位姿拉向视觉一致的最优解。这一设计使得人体与物体的运动推断在特征层面相互耦合，而非事后拼接。

### 3. 运动细化：从无后处理到条件扩散驱动的交互流形校正

现有方法在获得初步跟踪结果后，通常仅依赖简单的时序平滑或不再进行后处理。然而，粗糙的跟踪结果往往偏离真实的物理交互模式——例如手部可能穿透物体、接触关系不自然等。

I’m-HOI 引入**类别特定的交互扩散滤波器**，将运动细化建模为一个条件生成问题。该模块以第一阶段输出的粗糙跟踪结果和原始IMU信号为条件，在过参数化的交互表示空间（包含身体-手部关节位置、旋转及物体位姿，共486维）中学习特定交互类别的运动流形。通过扩散模型的逐步去噪过程，粗糙结果被“投影”到学习到的交互流形上，同时补全因遮挡而缺失的手部动作（Eq.6, Eq.9, Eq.13）。这一设计的关键洞察在于：**IMU提供了物体运动的物理锚点，而扩散模型则提供了人体-物体交互的统计先验**，二者互补，使得最终输出既满足物理约束，又符合特定交互类别的自然运动模式。

### 创新点的协同效应

上述三个创新点并非孤立存在，而是形成了一条完整的因果链路：IMU模态的引入解决了遮挡下的鲁棒性问题（传感器层），整体联合跟踪实现了人体与物体运动的协同推断（范式层），扩散滤波器则利用学习到的交互先验对结果进行精细化校正（后处理层）。消融实验证实，完整的I’m-HOI流水线（包含网格对齐反馈、优化模块和扩散滤波）相比朴素的直接回归实现，性能提升约4倍（Section 5.3）。

I’m-HOI 采用 **两阶段解耦范式**，将单目 RGB 视频与物体端单 IMU 信号的多模态融合问题，分解为通用交互运动推断与类别特定运动细化两个串行阶段。该设计的核心动机在于：IMU 为物体运动提供遮挡鲁棒的位姿先验，而 RGB 流则承载丰富的视觉上下文；两阶段分工使得第一阶段专注于从原始传感器数据中端到端地恢复粗糙但全局一致的人-物运动，第二阶段则利用学习到的交互流形对粗糙结果进行去噪、校正与手部补全，从而在最小化传感器配置下实现高精度、生动的交互运动捕捉。

**输入与预处理**：系统输入为一段单目 RGB 视频 $I_{1:T}$ 及同步的物体端 IMU 信号（加速度与角速度）。预处理阶段利用 SAM 生成人体与物体掩码，并通过预训练 ResNet-34 提取图像特征，为后续模块提供结构化的视觉先验。

**第一阶段：通用交互运动推断**。该模块以端到端方式联合恢复人体与物体的空间配置。其核心创新在于将物体视为人体的一个“额外肢体关节”，通过多尺度 CNN 估计 3D 人体关键点，再经 IK 优化层回归姿态与体型参数。物体位姿的估计则引入 **网格对齐反馈循环**：以当前物体位姿渲染剪影，与真实掩码的面积差异作为反馈信号，逐步校正物体位姿；同时，IMU 信号通过加速一致性约束与旋转正则化项直接融入优化过程，形成视觉-惯性紧耦合的跟踪框架。训练损失由 3D 关键点损失 $\mathcal{L}_{\mathrm{kp3d}}$、2D 重投影损失 $\mathcal{L}_{\mathrm{j2d}}$、逆运动学扭曲损失 $\mathcal{L}_{\mathrm{twist}}$ 及网格对齐反馈损失 $\mathcal{L}_{\mathrm{maf}}$ 联合构成（Eq. 2）。在此基础上，可选的轻量鲁棒优化模块进一步结合物体剪影与 IMU 约束，对物体位姿进行小范围后优化，提升时序一致性。

**第二阶段：类别特定交互扩散滤波器**。第一阶段输出的粗糙运动序列 $x_{1:T}$ 与原始 IMU 信号共同作为条件，输入一个类别特定的条件扩散模型。该模型在过参数化的交互表示空间中学习人体-物体交互的运动流形，通过前向加噪与反向去噪过程，将粗糙结果投影到流形上，同时补全手部动作。扩散模型的训练采用简单 L1 损失 $\mathcal{L}_{\mathrm{simple}}$（Eq. 6），并辅以运动一致性正则化 $\mathcal{L}_{\mathrm{consist}}$（Eq. 9）与加速度约束损失 $\mathcal{L}_{\mathrm{acc}}$（Eq. 13），确保去噪后的运动在人体关节一致性、物体轨迹物理合理性等方面均满足交互先验。

**输出**：最终输出为时序连续的人体 SMPL 参数序列与物体 6-DoF 位姿序列，可直接驱动三维角色与物体模型，生成生动的交互动画。整个流水线每帧推理仅需约 0.5 秒，相比 VisTracker（约 20 秒/帧）和 CHORE（约 1 分钟/帧）具有显著的速度优势。

### 补充图表

![[assets/figures/papers/paper_list_l1721_I_M_HOI_Inertia_aware_Monocular_Capture_of_3D_Human_Object_Interactions/figures/002_Figure_2.jpg]]
*Figure 2: The pipeline of I’m-HOI. Assuming video and inertial measurements input, our approach consists of a general interaction motion inference module (Sec. 3.1) and a category-specific interaction diffusion filter (Sec. 3.2) to capture challenging interaction motions*

I’m-HOI 将单目三维人物-物体交互捕捉解耦为两个核心阶段：**通用交互运动推断**（General Interaction Motion Inference）与**类别特定交互扩散滤波**（Category-specific Interaction Diffusion Filter）。前者以端到端方式联合恢复人体-物体的空间排布，后者在学习的交互流形上对粗糙结果进行去噪与手部动作补全。

### 通用交互运动推断模块

该模块的核心设计在于将物体视为人体的一个额外肢体关节，从而实现人体-物体空间排布的整体估计。输入为单目RGB视频帧与物体端IMU信号（加速度 $A_t$ 与朝向四元数 $Q_t$），经SAM分割与预训练ResNet-34提取图像特征后，通过多尺度CNN估计3D人体关键点，再由逆运动学优化层回归人体姿态 $\theta_{h,t}$ 与体型 $\beta$。

物体位姿的估计采用**网格对齐反馈循环**（Mesh-Aligned Feedback loop）：在 $N_F$ 次迭代中，当前估计的物体旋转 $\hat{\mathbf{R}}_{o,t}^{(i)}$ 与平移 $\hat{\mathbf{T}}_{o,t}^{(i)}$ 被用于渲染物体剪影，并与真实掩码 $\mathbf{S}_{o,t}$ 比对，通过增强剪影面积损失进行监督：

$$
\mathcal{L}_{\mathrm{area}} = \frac{1}{T} \sum_{t=0}^{T-1} \sum_{i=0}^{N_F-1} \left\| \sum \mathcal{D}(\hat{\mathbf{R}}_{o,t}^{(i)} \mathcal{O} + \hat{\mathbf{T}}_{o,t}^{(i)}) - \sum \mathbf{S}_{o,t} \right\|_2^2 \tag{1}
$$

其中 $\mathcal{D}$ 为可微渲染器，$\mathcal{O}$ 为预先扫描的物体模板。该损失仅约束剪影面积而非像素级对齐，在保证梯度有效性的同时降低了计算开销。

第一阶段整体训练目标为：

$$
\mathcal{L} = \mathcal{L}_{\mathrm{kp3d}} + \lambda_{\mathrm{j2d}} \mathcal{L}_{\mathrm{j2d}} + \mathcal{L}_{\mathrm{twist}} + \mathcal{L}_{\mathrm{maf}} \tag{2}
$$

其中 $\mathcal{L}_{\mathrm{kp3d}}$ 为3D关键点损失，$\mathcal{L}_{\mathrm{j2d}}$ 为2D重投影损失，$\mathcal{L}_{\mathrm{twist}}$ 为逆运动学扭转正则化，$\mathcal{L}_{\mathrm{maf}}$ 为网格对齐反馈损失。

**轻量鲁棒优化**（可选后处理）进一步融合物体剪影与IMU约束，对物体位姿进行小范围修正。其IMU正则化能量定义为：

$$
\mathcal{E}_{\mathrm{imu}} = \frac{1}{T-1} \sum_{t=1}^{T-1} \left\| (\hat{T}_{o,t-1} + \hat{T}_{o,t+1} - 2\hat{T}_{o,t}) - 0.5 A_t^2 \right\|_2^2 + \frac{1}{T} \sum_{t=0}^{T-1} \left\| \hat{R}_{o,t} - Q_t \right\|_2^2 \tag{4}
$$

第一项利用加速度一致性约束物体平移轨迹，第二项直接以原始IMU四元数约束物体朝向。

### 类别特定交互扩散滤波器

第二阶段以第一阶段输出的粗糙跟踪结果与原始IMU信号为条件，通过条件扩散模型在过参数化的交互表示空间中进行运动细化。交互表示 $\mathbf{x}_t^n \in \mathbb{R}^{486}$ 包含：人体-手部关节位置 $\mathbf{j}_{h,t}$ 与旋转 $\theta_{h,t}$、物体位姿 $\mathbf{j}_{o,t}$ 与 $\theta_{o,t}$、以及原始IMU加速度 $\mathbf{a}_t$ 与朝向 $\mathbf{q}_t$。

前向扩散过程定义为：

$$
q(\mathbf{x}_{1:T}^n | \mathbf{x}_{1:T}^{n-1}) = \mathcal{N}(\sqrt{\alpha_n} \mathbf{x}_{1:T}^{n-1}, (1-\alpha_n) \mathbb{Z}) \tag{5}
$$

扩散模型训练采用预测 $\mathbf{x}_0$ 的简单损失：

$$
\mathcal{L}_{\mathrm{simple}} = \mathbb{E}_{\mathbf{x}_0, n} \left\| \hat{\mathbf{x}}_\phi(\mathbf{x}_n, n, \mathbf{x}) - \mathbf{x}_0 \right\|_1 \tag{6}
$$

在推理阶段，模型以粗糙交互运动 $\tilde{\mathbf{x}}_{1:T}$ 为条件，从随机噪声逐步去噪生成细化后的运动序列。

为确保生成运动在物理与结构上的一致性，扩散阶段引入两项关键约束。**运动一致性正则化**确保预测的人体关节与从姿态参数蒙皮得到的关节一致：

$$
\mathcal{L}_{\mathrm{consist}} = \frac{1}{T} \sum_{t=0}^{T-1} \left\| \hat{\mathbf{j}}_{h,t} - \mathcal{I}(\mathcal{M}(\hat{\beta}, \hat{\theta}_{h,t})) \right\|_1 \tag{9}
$$

其中 $\mathcal{M}$ 为SMPL蒙皮函数，$\mathcal{I}$ 为关节回归器。

**加速度约束损失**直接利用IMU加速度信号约束物体轨迹的一致性：

$$
\mathcal{L}_{\mathrm{acc}, t} = \left\| \left(\hat{\mathbf{j}}_{o,t} - \hat{\mathbf{j}}_{o,t-1} + \frac{\mathbf{a}_t \tau^2}{2}\right) - (\mathbf{j}_{o,t+1} - \mathbf{j}_{o,t}) \right\|_1 \tag{13}
$$

物体旋转则通过旋转正则化损失直接监督：

$$
\mathcal{L}_{\mathrm{rot}} = \frac{1}{T} \sum_{t=0}^{T-1} \left\| \hat{\theta}_{o,t} - \mathbf{q}_t \right\|_1 \tag{12}
$$

通过上述两阶段设计，I’m-HOI 在遮挡与快速运动场景下实现了鲁棒的人体-物体联合跟踪，并通过扩散模型在交互流形上补全了手部细节动作。消融实验表明，完整的流水线（网格对齐反馈 + 优化 + 扩散滤波）相比朴素实现性能提升约4倍（Section 5.3）。

### 补充图表

![[assets/figures/papers/paper_list_l1721_I_M_HOI_Inertia_aware_Monocular_Capture_of_3D_Human_Object_Interactions/figures/009_Table_3.jpg]]
*Table 3: Quantitative evaluation of network architecture design*

![[assets/figures/papers/paper_list_l1721_I_M_HOI_Inertia_aware_Monocular_Capture_of_3D_Human_Object_Interactions/figures/008_Table_4.jpg]]
*Table 4: Quantitative evaluations on input modality configurations*

## 实验与关键发现

### 主实验结果

I’m-HOI 在自建数据集 IMHD2 上与多个代表性基线方法进行了定量比较。IMHD2 包含快速交互序列（如滑板、篮球等），是评估动态场景下跟踪鲁棒性的核心基准。评估指标采用倒角距离（CD，单位 cm），分别报告人体（SMPL）与物体的逐帧误差。

在快速交互子集上，I’m-HOI 取得了 **6.50 / 6.93**（人体/物体）的 CD 值，相比此前最优基线 CHORE（Xie et al., ECCV 2022）的 14.20 / 16.81，物体跟踪精度提升约 **9.9 cm**（Table 1）。这一显著差距源于物体端 IMU 提供了遮挡鲁棒的位姿先验，而纯视觉方法在快速旋转、运动模糊或局部遮挡下几乎无法可靠估计物体 6-DoF 姿态。

在推理速度方面，I’m-HOI 每帧仅需约 **0.5 秒**，而 VisTracker（Xie et al., CVPR 2023）约需 20 秒，CHORE 约需 1 分钟，PHOSA（Zhang et al., ECCV 2020）约需 2 分钟。速度优势主要来自端到端联合跟踪范式——将物体视为额外肢体关节进行整体推断，避免了传统分离式“拟合-学习-优化”流水线中的冗余计算。

在泛化能力评估中（Table 2），I’m-HOI 在 HODome 和 CHAIRS 两个外部数据集上同样显著优于基线方法。HODome 上人体/物体逐帧 CD 为 8.19 / 9.05，CHAIRS 上为 9.55 / 9.91，验证了多模态融合策略对域差异的鲁棒性。定性对比（Figure 5）进一步显示，基线方法在遮挡或快速运动时会出现人体-物体空间关系错乱或穿透，而 I’m-HOI 保持了物理合理的交互布局。

![[assets/figures/papers/paper_list_l1721_I_M_HOI_Inertia_aware_Monocular_Capture_of_3D_Human_Object_Interactions/figures/006_Figure_5.jpg]]
*Figure 5: Qualitative comparison results. I’m-HOI outperforms the baselines and generalizes well to new datasets*

![[assets/figures/papers/paper_list_l1721_I_M_HOI_Inertia_aware_Monocular_Capture_of_3D_Human_Object_Interactions/figures/007_Table_2.jpg]]
*Table 2: Quantitative evaluations of generalization ability*

### 消融实验

为量化各模块的独立贡献，作者在 IMHD2 上进行了架构消融（Table 3）。以朴素直接回归为起点，逐步加入关键设计：

- **网格对齐反馈**（maf.）在每帧物体跟踪中带来明显改进，因为它利用渲染轮廓面积损失（Eq. 1）将物体位姿逐步校正到与视觉证据一致的状态。
- **轻量鲁棒优化**（optim.）提升了运动的时序一致性，其通过 IMU 正则化能量（Eq. 4）约束物体平移的加速度一致性和旋转的朝向一致性。
- **类别特定扩散滤波器**（filter.）将人体-物体空间布局修正到学习的交互流形上，同时补全手部动作。该模块以粗糙跟踪结果和原始 IMU 为条件，在过参数化表示中进行去噪。

完整流水线（maf. + optim. + filter.）的逐帧 CD 为 6.50 / 6.93，10 秒窗口 CD 为 5.36 / 8.53，相比朴素实现性能提升约 **4 倍**。定性消融示例（Figure 6）直观展示了各模块对运动平滑性和交互合理性的递进改善。

在输入模态消融中（Table 4），作者向纯视觉基线方法加入了基于 IMU 的惯性优化项（Eq. 4），以部分补偿模态缺失。结果显示，引入 IMU 后各基线方法的跟踪精度均有提升，但 I’m-HOI 仍然显著领先——因为其将 IMU 深度融合进端到端跟踪流程，而非仅作为后处理正则项。Figure 7 的定性示例表明，纯视觉方法在物体快速旋转时完全丢失朝向信息，而 IMU 的介入使跟踪恢复稳定。

### 失败模式与局限性

尽管 I’m-HOI 在多数场景下表现优异，仍存在以下局限：

1. **物体模板依赖**：方法假设物体具有预先扫描的 3D 模板，且传感器与模板坐标系的手动对齐已完成。在无模板或对齐不精确的场景下，轮廓面积损失和 IMU 正则化均会失效。
2. **刚性假设**：当前仅支持刚性物体，无法处理铰接物体（如剪刀、笔记本电脑）或可变形物体（如背包、衣物）的交互。
3. **类别泛化有限**：数据集仅涵盖 10 类扫描物体，扩散滤波器学习的交互流形可能对未见物体类别的运动模式覆盖不足。

### 图表核心结论

- **Figure 4 / Table 1**：I’m-HOI 在 IMHD2 快速交互序列上以大幅优势超越所有基线，验证了 IMU 先验在动态遮挡场景中的决定性作用。
- **Table 2**：跨数据集泛化能力优异，表明多模态融合策略未过拟合特定场景分布。
- **Table 3 / Figure 6**：消融实验证实了反馈、优化、扩散滤波三个模块的递进增益，全流水线性能是朴素实现的 4 倍。
- **Table 4 / Figure 7**：IMU 模态的引入对纯视觉基线有普遍提升，但深度多模态融合（I’m-HOI）才能充分释放其潜力。

![[assets/figures/papers/paper_list_l1721_I_M_HOI_Inertia_aware_Monocular_Capture_of_3D_Human_Object_Interactions/figures/005_Figure_4.jpg]]
*Figure 4: Qualitative 3D capturing results of I’m-HOI on IMHD2 dataset. Each sample includes an RGB image input, captured motion from camera view, and side-view visualization*

## 定位与知识库关联

### 传感器融合范式的演进定位

I’m-HOI 处于单目视觉感知与惯性传感融合的交叉点上。传统单目人物-物体交互（HOI）捕捉方法——如基于单一RGB图像的优化式方法 **PHOSA**（Zhang et al., ECCV 2020）、单图人体-物体-接触重建方法 **CHORE**（Xie et al., ECCV 2022），以及视频式交互跟踪方法 **VisTracker**（Xie et al., CVPR 2023）——完全依赖视觉信号进行位姿估计。这类方法在遮挡、深度模糊及快速运动情形下，物体位姿的鲁棒估计能力严重不足，成为制约整体捕捉精度的核心瓶颈。

I’m-HOI 的关键范式跃迁在于**将物体端单IMU信号引入HOI捕捉管线**，以最小传感器增量（单目RGB + 一个物体端IMU）换取遮挡鲁棒的物体运动先验。与多模态融合领域中常见的“后融合”策略不同，I’m-HOI 将IMU信号深度嵌入跟踪流程：在通用运动推断阶段，通过网格对齐反馈循环（mesh-aligned feedback）逐步融合IMU约束；在运动细化阶段，以原始IMU信号作为扩散模型的条件输入。这种设计使IMU从辅助正则项升格为运动推断的核心驱动因素之一。

### 跟踪范式的结构化创新

在人体-物体跟踪范式的谱系中，I’m-HOI 提出了一项值得关注的架构决策：**将物体视为人体的额外肢体关节，进行端到端的整体空间布局推断**。这一设计区别于传统方法中“先人体后物体”的分离式拟合-学习-优化管线，其优势在于：

- 人体运动推断网络可以隐式学习人体-物体之间的运动耦合模式，而非将物体位姿作为独立的后处理步骤；
- 网格对齐反馈机制在每次迭代中同时优化人体和物体的空间关系，形成闭环校正；
- 训练目标（Eq.2）将3D关键点损失、2D重投影损失、逆运动学扭曲损失与网格对齐反馈损失统一在一个端到端框架内：

$$\mathcal{L} = \mathcal{L}_{\mathrm{kp3d}} + \lambda_{\mathrm{j2d}} \mathcal{L}_{\mathrm{j2d}} + \mathcal{L}_{\mathrm{twist}} + \mathcal{L}_{\mathrm{maf}}$$

### 运动细化：从时序平滑到交互流形投影

在运动后处理层面，I’m-HOI 的类别特定交互扩散滤波器代表了一次显著的范式升级。此前方法（如VisTracker）主要依赖时序平滑或简单的物理约束进行后处理，而I’m-HOI 将问题重新定义为**在学习的交互流形上的条件生成**：

1. **过参数化表示**：扩散模型的操作空间包含身体-手部关节位置与旋转、物体位姿，以及原始IMU信号（加速度与朝向），构成486维的特征向量；
2. **条件去噪**：以粗糙跟踪结果和原始IMU为条件，通过扩散过程将运动投影到类别特定的交互流形上；
3. **手部补全**：在物体交互上下文中，对因遮挡而缺失的手部动作进行条件生成式补全。

训练采用简化的L1去噪损失：

$$\mathcal{L}_{\mathrm{simple}} = \mathbb{E}_{\mathbf{x}_0, n} \| \hat{\mathbf{x}}_\phi(\mathbf{x}_n, n, \mathbf{x}) - \mathbf{x}_0 \|_1$$

同时辅以运动一致性正则化确保预测关节与蒙皮关节一致：

$$\mathcal{L}_{\mathrm{consist}} = \frac{1}{T} \sum_{t=0}^{T-1} \| \hat{\mathbf{j}}_{h,t} - \mathcal{I}(\mathcal{M}(\hat{\beta}, \hat{\mathbf{\theta}}_{h,t})) \|_1$$

### 推理效率的阶跃式提升

从系统实现角度看，I’m-HOI 在推理速度上实现了数量级的跃升：每帧约0.5秒，相较于VisTracker的约20秒、CHORE的约1分钟、PHOSA的约2分钟，分别快约40倍、120倍和240倍。这一效率优势源于端到端联合推断架构避免了迭代优化带来的计算开销，同时扩散滤波器以并行去噪方式替代了传统的逐帧优化。

### 适用边界与局限

I’m-HOI 的适用性受以下边界条件的约束：

1. **模板依赖**：方法要求预先扫描的物体模板，并需手动完成IMU传感器坐标系与模板坐标系的对齐。这限制了其在无模板场景（如未知物体的即时交互捕捉）中的应用；
2. **刚性物体限定**：当前框架仅支持刚性物体的位姿跟踪，尚未扩展至铰接物体（如剪刀、门）或可变形物体（如衣物、背包）的交互；
3. **物体类别泛化**：数据集INHD²涵盖10类扫描物体，类别覆盖有限，可能影响跨类别的泛化能力——尽管Table 2的跨数据集实验（HODome、CHAIRS）显示了初步的泛化潜力；
4. **单物体假设**：当前设计假定场景中仅存在一个交互物体，多物体交互场景（如同时使用工具与容器）尚未被建模。

### 开放问题与后续方向

从知识库定位的角度，I’m-HOI 打开了以下研究路径：

- **无模板联合重建**：能否在无预先扫描模板的条件下，端到端地同时推断物体几何与运动？这需要将神经隐式表面重建与惯性-视觉融合跟踪统一在一个框架内；
- **可变形与铰接物体扩展**：将方法从刚性6-DoF位姿估计扩展到铰接物体的关节状态推断或可变形物体的稠密变形场估计，需要重新设计物体表示与IMU约束形式；
- **多模态异步融合的自适应机制**：IMU与视觉模态存在固有的采样率差异与噪声特性差异，如何自适应地处理模态间的时序对齐与置信度加权，是提升系统鲁棒性的关键问题；
- **多传感器扩展**：在物体端IMU之外，是否可引入人体端IMU或其他稀疏传感器，以在极端遮挡下进一步提升捕捉精度，值得探索。

### 证据强度说明

本文的核心实验主张——I’m-HOI在IMHD²快速交互子集上的物体跟踪精度（CD）比最优基线CHORE提升约9.9cm（6.93 vs 16.81 cm），全流水线相比朴素实现性能提升约4倍——均有Table 1和Table 3的定量消融数据支撑，证据置信度较高。跨数据集泛化实验（Table 2）提供了初步的泛化性证据，但受限于测试数据集的规模与多样性，该结论需要更多独立验证。

## 原文 PDF

![[paperPDFs/CVPR_2024/IM_HOI_Inertia_aware_Monocular_Capture_of_3D_Human_Object_Interactions.pdf]]
