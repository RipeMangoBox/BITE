---
title: "Free-Form Motion Control: A Synthetic Video Generation Dataset with Controllable Camera and Object Motions"
type: paper
paper_level: A
venue: arXiv
year: 2025
pdf_ref: paperPDFs/arxiv_2025/Free_Form_Motion_Control_A_Synthetic_Video_Generation_Dataset_with_Controllable_Camera_and_Object_Motions.pdf
aliases:
- FFMCF
- FFMCSVGDCCOM
tags:
- arxiv_2025
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/image_and_video_generation
- topic/generative_models_diffusion
- topic/benchmarks_datasets_evaluation
core_operator: SynFMC合成数据集提供了精确的6D姿态标注及多样化的运动模式，结合FMC方法中的Camera Motion Controller和Object Motion Controller，以及针对性的损失函数L_cam和L_obj，实现了相机与物体运动的解耦控制。
primary_logic: 通过解耦训练（域适应、相机控制、物体控制三阶段）和专用区域损失，模型能够在合成数据上学习分离全局（相机）和局部（物体）运动，从而在推理时独立或同时控制二者的6D姿态，生成高保真视频。
claims:
- SynFMC是首个同时提供相机和物体6D姿态标注的数据集，且运动模式多样可控。
- FMC通过三阶段训练和背景/前景专用损失（L_cam, L_obj）实现相机与物体运动的解耦。
- FMC在物体运动控制上显著优于MotionCtrl，同时保持相机控制可比。
- 消融实验证明移除L_cam或L_obj会严重损害相应的控制精度（CamTransErr升至20.35，ObjTransErr升至46.62）。
---

# Free-Form Motion Control: A Synthetic Video Generation Dataset with Controllable Camera and Object Motions

> [!tip] 核心洞察
> 通过解耦训练（域适应、相机控制、物体控制三阶段）和专用区域损失，模型能够在合成数据上学习分离全局（相机）和局部（物体）运动，从而在推理时独立或同时控制二者的6D姿态，生成高保真视频。

| 字段 | 内容 |
|------|------|
| 中文题名 | 自由形式运动控制：一个具有可控相机与目标运动的合成视频生成数据集 |
| 英文题名 | Free-Form Motion Control: A Synthetic Video Generation Dataset with Controllable Camera and Object Motions |
| 会议/期刊 | arXiv 2025 |
| Links | [paper](https://arxiv.org/abs/2501.01425) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/image_and_video_generation #topic/generative_models_diffusion #topic/benchmarks_datasets_evaluation |
| Method | Free-Form Motion Control (FMC) |
| Dataset | SynFMC test set, User study |

> [!tip] 效果简介
> - SynFMC test set 上，CamTransErr 18.12 vs CameraCtrl / MotionCtrl (comparable) (comparable)；CamRotErr 1.03 vs CameraCtrl / MotionCtrl (comparable) (comparable)；ObjTransErr 42.25 vs MotionCtrl (significantly higher) (significantly lower)。
> - User study 上，Quality Score 0.91 vs CameraCtrl / MotionCtrl (higher)；Camera Motion Score 0.95 vs CameraCtrl / MotionCtrl (higher)；Object Motion Score 0.98 vs CameraCtrl / MotionCtrl (much higher)。

## 概述

可控视频生成的核心瓶颈在于：现有方法缺乏同时提供相机与物体完整6D姿态标注的数据集，导致无法在三维空间中独立或联合控制相机与物体运动。本文提出**Free-Form Motion Control (FMC)**，通过构建合成数据集**SynFMC**并设计解耦训练策略，首次实现了相机与物体6D姿态的自由形式控制。

**核心结论**：FMC通过三阶段训练（域适应、相机控制、物体控制）和专用的背景/前景区域损失函数（$L_{cam}$、$L_{obj}$），在合成数据上学习分离全局（相机）与局部（物体）运动，从而在推理时独立或同时控制二者的6D姿态，生成高保真视频。在SynFMC测试集上，FMC在物体运动控制上显著优于**MotionCtrl**（Wang et al., SIGGRAPH 2024），同时保持相机控制精度可比；用户研究中，物体运动评分达到0.98，远超对比方法。

**方法定位**：FMC属于基于预训练文本到视频扩散模型（如**AnimateDiff**, Guo et al., ICLR 2024）的运动注入式控制方法，通过Camera Motion Controller (CMC)和Object Motion Controller (OMC)两个轻量级模块实现解耦控制。与仅支持2D相机姿态的**CameraCtrl**（He et al., arXiv 2024）和存在运动纠缠问题的**MotionCtrl**不同，FMC首次提供了完整的6D物体姿态控制能力。

## 背景与动机

可控视频生成旨在让用户精确操纵视频中的运动元素，包括相机运动和物体运动。然而，现有方法在这一目标上存在根本性瓶颈：**缺乏同时包含相机和物体完整6D姿态标注的数据集**，导致模型无法在三维空间中独立或联合控制相机和物体运动。

具体而言，当前的视频生成可控性方案大致可分为以下几类，但各有局限：

- **无运动控制的文本到视频基线**（如 **AnimateDiff**，Guo et al., ICLR 2024）仅依赖文本提示，无法对运动进行显式操控。
- **仅相机运动控制方法**（如 **CameraCtrl**，He et al., arXiv 2024）能操控相机轨迹，但无法控制场景中物体的独立运动。
- **尝试同时控制物体和相机的方法**（如 **MotionCtrl**，Wang et al., SIGGRAPH 2024）虽然引入了物体运动控制模块，但由于训练数据仅提供从真实视频提取的2D轨迹或相机姿态（如RealEstate10K、WebVid），缺乏物体的6D姿态真值，导致相机与物体运动之间存在严重的**运动纠缠**问题——模型难以区分全局运动（相机）和局部运动（物体），在独立控制某一运动时，另一运动会发生不期望的漂移。

这一瓶颈的根源在于数据层面：现有数据集要么只标注相机姿态，要么只提供2D物体轨迹，没有一个数据集能同时提供相机和物体的完整6D姿态标注以及多样化的运动模式。合成数据虽可提供精确标注，但如何弥合合成渲染风格与真实视觉风格之间的域差距，是将其用于视频生成模型训练的另一个挑战。

针对上述问题，本文的动机明确：**构建首个同时提供相机和物体6D姿态标注的合成数据集，并设计相应的解耦训练策略，实现相机与物体运动的独立或联合控制**。为此，本文提出SynFMC合成数据集和Free-Form Motion Control (FMC)方法，通过三阶段解耦训练和专用的区域损失函数，在合成数据上学习分离全局与局部运动，从而在推理时生成高保真且运动可控的视频。

## 核心创新

本节聚焦 FMC 相对于现有运动控制方法的三个关键创新维度：训练数据、运动控制模块设计和损失函数策略。这些创新共同解决了当前视频生成中相机与物体运动无法解耦控制的核心瓶颈。

### 1. 训练数据：从 2D 轨迹到完整 6D 姿态标注

现有运动控制方法依赖真实视频提取的 2D 轨迹或相机姿态（如 RealEstate10K、WebVid），缺乏物体在三维空间中的完整运动信息。FMC 的核心突破在于构建了 **SynFMC 合成数据集**，首次同时提供相机和物体的完整 6D 姿态真值标注（Table 1）。

SynFMC 基于 Unreal Engine 的规则化生成流水线构建（Figure 1），其关键设计包括：

- **物体运动**：基于 Bézier 曲线设计轨迹，旋转信息由曲线切向量和法向量推导，覆盖水平直线/曲线、非水平直线/曲线及静止五种类型（Figure 3）。
- **相机运动**：分解为视角（前/后/左/右/顶）、距离和高度三个独立维度（Figure 4），支持动态组合生成复杂运镜轨迹（Figure 5）。

这种设计使模型能够学习物体在三维空间中的方位和距离变化，而非仅依赖图像空间的 2D 位移信号，为后续的 6D 姿态控制提供了数据基础。

### 2. 运动控制模块：解耦的相机与物体控制器

FMC 设计了两个独立的控制模块，分别处理全局相机运动和局部物体运动（Figure 7）：

- **Camera Motion Controller (CMC)**：由 Camera Encoder 和 Camera Adapter 组成。Camera Encoder 将相机姿态编码为 **Plücker 嵌入**（一种对相机射线几何的紧凑表示），Camera Adapter 将其注入预训练 T2V 模型的时间块中。CMC 仅负责学习背景区域的运动模式。

- **Object Motion Controller (OMC)**：接收物体的 **6D 姿态**（3D 平移 + 3D 旋转）和粗略掩码作为输入。与需要精确分割掩码的方法不同，OMC 采用**高斯模糊处理掩码**，避免模型过拟合到精确边界，同时保留足够的空间引导信息。OMC 仅学习前景物体的运动。

这种模块化设计的关键优势在于：相机和物体的运动信号分别注入模型的不同控制通路，从架构层面实现了二者的解耦，避免了 MotionCtrl 等方法中常见的运动纠缠问题。

### 3. 损失函数：区域感知的运动解耦训练

仅靠架构解耦不足以完全分离相机与物体运动，FMC 进一步引入了两个**区域感知的扩散损失函数**，强制模型在特定空间区域学习对应的运动模式：

**相机损失** $L_{cam}$ 使用背景掩码 $\mathcal{M}_{bg}$ 加权：

$$
L_{cam} = \mathbb{E}_{z_0^{1:N}, t, \epsilon, C_p, \mathcal{C}_{RT}} \left[ \mathcal{M}_{bg} \| \varepsilon_{\theta,\theta_c}(z_t^{1:N}, t, C_p, \mathcal{C}_{RT}) - \epsilon \|^2 + \lambda_c \| \varepsilon_{\theta,\theta_c}(z_t^{1:N}, t, C_p, \mathcal{C}_{RT}) - \epsilon \|^2 \right]
$$

该损失强制背景区域的去噪过程严格跟随相机轨迹，$\lambda_c$ 控制整体运动一致性。

**物体损失** $L_{obj}$ 使用前景掩码 $\mathcal{M}_{fg}$ 加权：

$$
L_{obj} = \mathbb{E}_{z_0^{1:N}, t, \epsilon, C_p, \mathcal{C}_{RT}, \mathcal{O}_{RT}} \left[ \mathcal{M}_{fg} \| \varepsilon_{\theta,\theta_c,\theta_o}(z_t^{1:N}, t, C_p, \mathcal{C}_{RT}, \mathcal{O}_{RT}) - \epsilon \|^2 + \lambda_o \| \varepsilon_{\theta,\theta_c,\theta_o}(z_t^{1:N}, t, C_p, \mathcal{C}_{RT}, \mathcal{O}_{RT}) - \epsilon \|^2 \right]
$$

该损失在保持物体运动准确性的同时，**抑制前景区域中的相机运动效应**，防止物体因相机运动而产生漂移。

消融实验（Table 5）验证了这一设计的决定性作用：移除 $L_{cam}$ 后，相机平移误差从 18.12 升至 20.35；移除 $L_{obj}$ 后，物体平移误差从 42.25 升至 46.62。定性结果（Figure 12）进一步表明，仅使用标准扩散损失训练 CMC 会导致前景物体随相机运动漂移，而非实现准确的相机控制。

### 4. 训练策略：三阶段渐进解耦

FMC 采用三阶段训练策略实现域适应与运动解耦的渐进学习（Figure 7）：

1. **Domain LoRA 阶段**：仅在空间块中注入 LoRA 参数，使用合成数据的随机帧进行训练，弥合渲染风格与真实图像之间的域差距（Figure 6）。该 LoRA 在推理时丢弃。
2. **CMC 训练阶段**：冻结 Domain LoRA 和基础模型，仅训练 Camera Encoder 和 Camera Adapter，使用 $L_{cam}$ 学习背景运动。
3. **OMC 训练阶段**：冻结前两阶段的所有参数，仅训练 Object Encoder，使用 $L_{obj}$ 学习前景运动。

这种渐进式训练确保了各模块专注于各自的子任务，避免了联合训练中可能出现的梯度冲突。

### 关键创新总结

| 创新维度 | 基线方法 | FMC 方法 | 核心优势 |
|---------|---------|---------|---------|
| 训练数据 | 真实视频的 2D 轨迹/相机姿态 | SynFMC 合成数据集的完整 6D 姿态 | 提供物体三维运动真值 |
| 相机控制 | 基于 2D 姿态的单一模块 | CMC + Plücker 嵌入 | 更精确的 3D 相机轨迹建模 |
| 物体控制 | 无 6D 姿态或运动纠缠 | OMC + 6D 姿态 + 粗略掩码 | 独立控制物体方位和距离 |
| 损失函数 | 标准扩散 MSE 损失 | $L_{cam}$ + $L_{obj}$ 区域加权 | 前景/背景运动解耦 |
| 训练策略 | 端到端联合训练 | 三阶段渐进解耦 | 避免模块间梯度冲突 |

## 整体框架

FMC 的整体训练与推理架构围绕**解耦相机运动与物体运动**这一核心目标设计，采用三阶段渐进训练策略，在预训练文本到视频（T2V）扩散模型的基础上逐步注入运动控制能力。

### 三阶段训练流水线

**第一阶段：域适应（Domain LoRA）**

合成数据集 SynFMC 的渲染风格与真实视频存在域差距。为避免模型过拟合到合成纹理，FMC 首先在 T2V 模型的空间块中注入 **Domain LoRA** 模块，仅使用 SynFMC 视频中随机采样的单帧图像进行训练。该 LoRA 在推理时被丢弃，仅起到弥合域差距的桥梁作用（Figure 6 展示了有无 Domain LoRA 的首帧质量对比）。

**第二阶段：相机运动控制器（CMC）**

CMC 由 **Camera Encoder** 和 **Camera Adapter** 两部分组成。Camera Encoder 接收相机 6D 姿态的 **Plücker 嵌入**，将其编码后通过 Camera Adapter 注入到扩散模型的时间块中。此阶段仅训练 CMC 参数，并引入**背景加权损失函数** $L_{cam}$：

$$L_{cam} = E_{z_0^{1:N}, t, \epsilon, C_p, \mathcal{C}_{RT}} [ \mathcal{M}_{bg} \| \varepsilon_{\theta,\theta_c}(z_t^{1:N}, t, C_p, \mathcal{C}_{RT}) - \epsilon \|^2 + \lambda_c \| \varepsilon_{\theta,\theta_c}(z_t^{1:N}, t, C_p, \mathcal{C}_{RT}) - \epsilon \|^2 ]$$

其中 $\mathcal{M}_{bg}$ 为背景掩码，强制背景区域的运动严格匹配相机轨迹；$\lambda_c$ 控制整体运动一致性。该设计确保 CMC 仅学习全局相机运动，而不干扰前景物体。

**第三阶段：物体运动控制器（OMC）**

OMC 的 **Object Encoder** 接收物体 6D 姿态 $\mathcal{O}_{RT}$ 和粗略掩码（经高斯模糊处理以避免精确掩码依赖），将其注入已冻结的 CMC 和基础模型。此阶段使用**前景加权损失函数** $L_{obj}$：

$$L_{obj} = E_{z_0^{1:N}, t, \epsilon, C_p, \mathcal{C}_{RT}, \mathcal{O}_{RT}} [ \mathcal{M}_{fg} \| \varepsilon_{\theta,\theta_c,\theta_o}(z_t^{1:N}, t, C_p, \mathcal{C}_{RT}, \mathcal{O}_{RT}) - \epsilon \|^2 + \lambda_o \| \varepsilon_{\theta,\theta_c,\theta_o}(z_t^{1:N}, t, C_p, \mathcal{C}_{RT}, \mathcal{O}_{RT}) - \epsilon \|^2 ]$$

$\mathcal{M}_{fg}$ 为前景掩码，使 OMC 专注于学习物体运动，同时抑制前景区域中相机运动的影响；$\lambda_o$ 负责整体一致性约束。

### 推理时的解耦控制

经过三阶段训练后，FMC 在推理时支持三种控制模式：
- **仅相机控制**：CMC 激活，OMC 关闭
- **仅物体控制**：OMC 激活，CMC 接收静态相机姿态
- **同时控制**：CMC 与 OMC 同时激活，实现相机与物体的独立或联合 6D 姿态控制

### 关键设计决策

消融实验（Table 5）证实了各模块的必要性：移除 $L_{cam}$ 导致相机平移误差从 18.12 升至 20.35，旋转误差从 1.03 升至 1.19；移除 $L_{obj}$ 使物体平移误差从 42.25 升至 46.62，旋转误差从 0.96 升至 1.15。仅使用标准扩散损失训练 CMC 会导致前景漂移而非准确的相机运动（Figure 12）。

### 补充图表

![[assets/figures/papers/paper_list_l26_https_arxiv_org_abs_2501_01425/figures/009_Figure_7.jpg]]
*Figure 7: The architecture of FMC. In the first stage, we randomly sample the images from synthetic videos and update the parameters from injected Domain LoRA. Next, the modules from CMC are learned. It consists of two parts: Camera Encoder and Camera Adapter, where the Camera Adapter is introduced into the temporal modules. Finally, we train the Object Encoder from OMC. It receives the 6D object pose features, which are repeated in the corresponding object region. We use Gaussian blur kernel centered at the centroid to prevent the need of precise masks. Then, the output is multiplied by the coarse masks to modulate the features in the main branch*

## 核心模块与公式推导

FMC 方法的核心由三个关键模块构成，并通过两个专用损失函数实现相机与物体运动的解耦控制。

### 1. Domain LoRA：弥合合成-真实域差距

由于 SynFMC 数据集由虚幻引擎渲染生成，其视觉风格与真实视频存在显著差异。为避免模型过拟合到渲染风格，FMC 在第一阶段向预训练 T2V 扩散模型的空间块（spatial blocks）中注入 **Domain LoRA** 模块，仅使用合成视频的单帧图像进行训练。该模块在推理时被丢弃，不参与视频生成过程，从而在保持真实感生成能力的同时，使后续运动控制模块能够在合成数据上有效学习。

### 2. Camera Motion Controller (CMC)：全局相机运动控制

CMC 由 **Camera Encoder** 和 **Camera Adapter** 两部分组成，负责接收相机姿态条件并控制全局场景运动。

- **Camera Encoder**：将相机外参转换为 Plücker 嵌入（Plücker embeddings），为扩散模型提供逐像素的几何先验。
- **Camera Adapter**：将编码后的相机特征注入到扩散模型的时间块（temporal blocks）中，实现对视频帧间全局运动的一致性调控。

CMC 的训练由 **相机损失 $L_{cam}$** 驱动：

$$
L_{cam} = \mathbb{E}_{z_0^{1:N}, t, \epsilon, C_p, \mathcal{C}_{RT}} \left[ \mathcal{M}_{bg} \| \varepsilon_{\theta,\theta_c}(z_t^{1:N}, t, C_p, \mathcal{C}_{RT}) - \epsilon \|^2 + \lambda_c \| \varepsilon_{\theta,\theta_c}(z_t^{1:N}, t, C_p, \mathcal{C}_{RT}) - \epsilon \|^2 \right]
$$

**变量含义**：
- $z_t^{1:N}$：扩散时间步 $t$ 的 $N$ 帧噪声潜在表示
- $\epsilon$：目标噪声
- $C_p$：文本提示条件
- $\mathcal{C}_{RT}$：相机旋转和平移参数
- $\mathcal{M}_{bg}$：背景掩码（background mask）
- $\varepsilon_{\theta,\theta_c}$：含 CMC 参数 $\theta_c$ 的噪声预测网络
- $\lambda_c$：整体运动一致性权重

**核心机制**：第一项通过 $\mathcal{M}_{bg}$ 对背景区域加权，强制背景像素的运动严格跟随相机轨迹；第二项以权重 $\lambda_c$ 保证整体帧间运动的一致性。这种设计使得 CMC 仅学习背景的全局运动，而不干扰前景物体的独立运动。

### 3. Object Motion Controller (OMC)：局部物体运动控制

OMC 由 **Object Encoder** 组成，接收两个关键输入：

- **物体 6D 姿态 $\mathcal{O}_{RT}$**：包含物体的三维旋转和平移参数，使模型能够根据物体朝向和距离生成更真实的外观变化。
- **粗略掩码（coarse mask）**：经高斯模糊处理的前景区域指示，避免使用精确掩码带来的过拟合问题，同时提供物体的大致空间位置。

OMC 的训练由 **物体损失 $L_{obj}$** 驱动：

$$
L_{obj} = \mathbb{E}_{z_0^{1:N}, t, \epsilon, C_p, \mathcal{C}_{RT}, \mathcal{O}_{RT}} \left[ \mathcal{M}_{fg} \| \varepsilon_{\theta,\theta_c,\theta_o}(z_t^{1:N}, t, C_p, \mathcal{C}_{RT}, \mathcal{O}_{RT}) - \epsilon \|^2 + \lambda_o \| \varepsilon_{\theta,\theta_c,\theta_o}(z_t^{1:N}, t, C_p, \mathcal{C}_{RT}, \mathcal{O}_{RT}) - \epsilon \|^2 \right]
$$

**变量含义**：
- $\mathcal{O}_{RT}$：物体 6D 姿态参数（旋转 + 平移）
- $\mathcal{M}_{fg}$：前景掩码（foreground mask）
- $\varepsilon_{\theta,\theta_c,\theta_o}$：含 CMC 参数 $\theta_c$ 和 OMC 参数 $\theta_o$ 的完整噪声预测网络
- $\lambda_o$：整体一致性权重

**核心机制**：第一项通过 $\mathcal{M}_{fg}$ 对前景区域加权，确保物体运动与给定的 6D 姿态一致；第二项以权重 $\lambda_o$ 维持整体一致性。关键在于，该损失在前景区域**抑制相机运动的影响**，使 OMC 学习到的物体运动与 CMC 控制的相机运动相互解耦。

### 4. 三阶段解耦训练策略

FMC 的分阶段训练是实现运动解耦的关键设计：

1. **阶段一（域适应）**：仅训练 Domain LoRA，弥合合成数据与真实风格的域差距。
2. **阶段二（相机控制）**：冻结 Domain LoRA，训练 CMC，使用 $L_{cam}$ 仅学习背景的全局相机运动。
3. **阶段三（物体控制）**：冻结 CMC，训练 OMC，使用 $L_{obj}$ 在前景区域学习物体运动，同时抑制相机运动对前景的干扰。

这种顺序训练策略确保了相机和物体运动的独立可控性，使得推理时用户可以自由组合或独立控制二者的 6D 姿态。消融实验证实，移除 $L_{cam}$ 会导致相机平移误差从 18.12 升至 20.35，移除 $L_{obj}$ 则使物体平移误差从 42.25 升至 46.62，验证了两个专用损失函数的关键作用。

### 补充图表

![[assets/figures/papers/paper_list_l26_https_arxiv_org_abs_2501_01425/figures/003_Table_1.jpg]]
*Table 1: Comparison of the proposed SynFMC with existing datasets. The object/camera motion pattern columns apply only to synthetic datasets. In addition to offering a rich variety of object categories, SynFMC outperforms in motion pattern variety and controllability with comprehensive pose annotations of camera and objects. In our implementation, we only use 26K subset as training data*

![[assets/figures/papers/paper_list_l26_https_arxiv_org_abs_2501_01425/figures/007_Table_2.jpg]]
*Table 2: Comparison of FMC with other methods. FMC excels in controlling 6D poses of objects and camera with diverse motion patterns*

![[assets/figures/papers/paper_list_l26_https_arxiv_org_abs_2501_01425/figures/005_Figure_3.jpg]]
*Figure 3: Object motion types. The trajectory of stationary point is not presented in the figure, which is a fixed point in the space*

![[assets/figures/papers/paper_list_l26_https_arxiv_org_abs_2501_01425/figures/006_Figure_4.jpg]]
*Figure 4: Camera motion types. We decompose camera motion into 3 aspects. (a) Viewpoint controls camera orientation when capturing object. 1 - 5 present front/back, left/right and top perspectives. (b) Distance and (c) Height determine horizontal and vertical distance between camera and object, respectively. 6 - 9 are zoom in/out and up/down, respectively. The “static” types are omitted in (b) and (c), which stand for fixed distances*

## 实验与分析

### 核心瓶颈与实验动机

现有视频生成方法在运动可控性上的根本瓶颈在于：缺乏同时标注相机与物体完整6D姿态的数据集，导致模型无法在三维空间中解耦全局（相机）与局部（物体）运动。因此，实验设计的核心验证链条围绕三个层次展开：（1）SynFMC数据集是否提供了足够的运动多样性与标注精度；（2）FMC方法能否通过三阶段训练和专用损失函数实现相机-物体运动的解耦控制；（3）解耦控制是否在定量指标、用户主观评估和消融实验中一致成立。

### 主实验结果

#### 定量对比

Table 3报告了FMC与**AnimateDiff**（Guo et al., ICLR 2024）、**CameraCtrl**（He et al., arXiv 2024）和**MotionCtrl**（Wang et al., SIGGRAPH 2024）在SynFMC测试集上的定量对比。在相机运动控制指标上，FMC与CameraCtrl、MotionCtrl表现可比：相机平移误差（CamTransErr）为18.12，旋转误差（CamRotErr）为1.03。这表明FMC的Camera Motion Controller（CMC）在相机运动控制精度上达到了现有最佳水平。

物体运动控制是FMC的核心优势所在。与MotionCtrl相比，FMC在物体平移误差（ObjTransErr）和旋转误差（ObjRotErr）上均显著更低（ObjTransErr: 42.25，ObjRotErr: 0.96），说明Object Motion Controller（OMC）有效解决了MotionCtrl存在的运动纠缠问题——即物体运动控制会干扰相机运动的独立性。

#### 用户研究

Table 4的用户研究进一步验证了上述结论。FMC在视频质量评分（0.91）、文本相似度（0.95）、相机运动保真度（0.95）和物体运动保真度（0.98）上均优于CameraCtrl和MotionCtrl。其中物体运动保真度得分0.98的领先幅度最大，与定量指标中ObjRotErr的显著优势相互印证。

#### 定性分析

Figure 8展示了独立控制相机与物体运动的定性结果。在相机运动控制（Figure 8a）中，所有方法均能有效反映相机条件；但在物体运动控制（Figure 8b）中，对比方法无法保持相机静止，且物体朝向的保真度较低。Figure 9展示了同时控制相机与物体运动的结果：MotionCtrl难以生成逼真的物体动态，导致物体从画面中消失，而FMC实现了高质量的同时控制。

### 消融实验

Table 5和Figure 12报告了消融实验的定量与定性结果，验证了损失函数设计的必要性。

**L_cam移除的影响**：移除相机运动损失L_cam后，相机平移误差从18.12升至20.35，旋转误差从1.03升至1.19。Figure 12的定性结果显示，仅使用标准扩散损失训练CMC会导致前景漂移，而非准确的相机运动——这证实了背景加权损失对于强制背景区域跟随相机轨迹的关键作用。

**L_obj移除的影响**：移除物体运动损失L_obj后，物体平移误差从42.25升至46.62，旋转误差从0.96升至1.15。这表明前景加权损失在保持物体运动准确性的同时，有效抑制了前景中相机运动的干扰效应。

**OMC的6D姿态处理**：消融分析还表明，OMC处理6D姿态（而非仅2D轨迹）能够基于物体方位和与相机的距离生成更真实的外观——这一效果通过粗略掩码的尺寸变化隐式反映物体距离信息。

### 失败模式与局限

尽管FMC在解耦控制上取得了显著进展，实验分析揭示了以下局限：

1. **多对象复杂运动**：当前版本在控制多个对象的复杂交互运动上能力有限，可能导致生成视频不够自然。这是未来需要重点突破的方向。

2. **评估指标的局限性**：现有的CamTransErr、ObjTransErr等指标可能无法完全代表视频质量。物体运动评估尤其需要更准确的客观指标来衡量运动真实性与一致性。

3. **真实场景泛化**：该方法完全基于合成数据训练和评估。虽然Domain LoRA在一定程度上缓解了合成-真实的域差距，但在真实世界场景下的泛化能力仍需要进一步验证。

4. **运动控制与视频质量的权衡**：在追求精确运动控制的同时，如何保持生成视频的自然度和视觉质量，仍是一个开放问题。

### 方法谱系与知识库定位

FMC在视频运动控制方法谱系中的定位可通过Table 2和实验对比清晰呈现：

- **无运动控制基线**：**AnimateDiff**（Guo et al., ICLR 2024）仅提供文本到视频生成，无运动控制能力，在物体运动指标上表现最差。
- **仅相机控制**：**CameraCtrl**（He et al., arXiv 2024）实现了相机运动控制，但不支持物体运动，无法进行联合控制。
- **相机+物体控制（存在纠缠）**：**MotionCtrl**（Wang et al., SIGGRAPH 2024）同时支持相机和物体控制，但由于缺乏6D姿态标注和专用损失函数，存在运动纠缠问题——物体运动控制会破坏相机运动的独立性。
- **FMC（解耦控制）**：通过SynFMC数据集的6D姿态真值、三阶段解耦训练（域适应→相机控制→物体控制）以及背景/前景专用损失函数（L_cam/L_obj），FMC首次实现了相机与物体运动的独立或联合控制，在物体运动保真度上显著超越MotionCtrl，同时保持相机控制精度可比。

这一方法谱系表明，FMC的核心贡献不在于提出全新的网络架构，而在于通过数据集-训练策略-损失函数的协同设计，解决了运动可控视频生成中的解耦控制瓶颈。

### 补充图表

![[assets/figures/papers/paper_list_l26_https_arxiv_org_abs_2501_01425/figures/010_Table_3.jpg]]
*Table 3: Quantitative comparison of our proposed method FMC with AnimateDiff [11], CameraCtrl [12], and MotionCtrl [47]*

![[assets/figures/papers/paper_list_l26_https_arxiv_org_abs_2501_01425/figures/013_Table_5.jpg]]
*Table 5: Quantitative results in ablation study*

![[assets/figures/papers/paper_list_l26_https_arxiv_org_abs_2501_01425/figures/014_Figure_12.jpg]]
*Figure 12: Results of different settings in the ablation study. The first row is MotionCtrl [47] trained on SynFMC*

![[assets/figures/papers/paper_list_l26_https_arxiv_org_abs_2501_01425/figures/011_Figure_8.jpg]]
*Figure 8: Independent controls over camera and object motions. Results in (a) reveal that all methods [12, 47] effectively reflect the camera conditions. For object motion, the compared methods [47, 51] fail to maintain a stationary camera as shown in green boxes from (b) (e.g., movement of flower in row 5). Furthermore, they also present low fidelity of object orientation (3D axes in conditions)*

![[assets/figures/papers/paper_list_l26_https_arxiv_org_abs_2501_01425/figures/012_Table_4.jpg]]
*Table 4: User study in quality, text similarity, and motion fidelity*

![[assets/figures/papers/paper_list_l26_https_arxiv_org_abs_2501_01425/figures/015_Figure_11.jpg]]
*Figure 11: Simultaneous control results of MotionCtrl [47] trained on SynFMC without and with camera pose during training*

![[assets/figures/papers/paper_list_l26_https_arxiv_org_abs_2501_01425/figures/008_Figure_6.jpg]]
*Figure 6: Domain LoRA. We sample the first frame of generated videos under without and with Domain LoRA settings*

## 方法谱系与知识库定位

### 1. 与现有运动控制方法的谱系关系

FMC 处于“视频生成中的可控运动”这一研究脉络中，其核心贡献在于首次实现了相机与物体 6D 姿态的解耦控制。为理解这一定位，需先梳理该脉络中的关键节点。

**无运动控制的文本到视频基线。** **AnimateDiff** (Guo et al., ICLR 2024) 通过在预训练 T2I 模型中插入时间注意力层实现了文本到视频生成，但缺乏任何运动控制能力，生成的运动完全由文本提示隐式驱动，无法指定相机或物体的具体轨迹。

**仅相机运动控制。** **CameraCtrl** (He et al., arXiv 2024) 引入了相机姿态条件，使模型能够根据输入的相机轨迹生成视频。然而，该方法仅控制全局相机运动，不提供对场景中物体运动的任何控制手段。

**相机与物体运动联合控制的尝试。** **MotionCtrl** (Wang et al., SIGGRAPH 2024) 是首个尝试同时控制相机和物体运动的方法，但其存在根本性缺陷：由于训练数据中缺乏物体 6D 姿态真值，且未在损失函数层面区分运动来源，导致相机与物体运动高度纠缠——当用户尝试独立控制某一方时，另一方会产生不可预期的漂移。**Direct-a-Video** (Yang et al., SIGGRAPH 2024) 也提供了有限的相机和物体运动控制，但同样受限于数据标注的缺失。

**基于 2D 轨迹的控制范式。** **DragNUWA** (Yin et al., arXiv 2023) 和 **VideoComposer** (Wang et al., NeurIPS 2023) 等方法通过在图像空间绘制轨迹来控制运动，这种 2D 范式无法表达深度信息，因而无法实现真正的 3D 感知控制。

FMC 在这一谱系中的突破在于：通过 SynFMC 合成数据集提供了完整的 6D 姿态真值，并设计了专门的损失函数（L_cam 和 L_obj）在训练时显式解耦相机与物体运动。这使得 FMC 在保持相机控制能力与 CameraCtrl 可比的同时，在物体运动控制上显著超越 MotionCtrl（ObjTransErr 和 ObjRotErr 均大幅降低，见 Table 3）。

### 2. 关键设计差异：从数据到损失函数的系统性改进

FMC 与最相关基线 MotionCtrl 的核心差异体现在三个层面，这三个层面构成了一个完整的因果链条：

| 差异维度 | MotionCtrl | FMC |
|---------|-----------|-----|
| 训练数据 | 真实视频（WebVid 等），仅有 2D 轨迹或部分相机姿态 | SynFMC 合成数据集，提供相机和物体的完整 6D 姿态真值 |
| 物体运动表示 | 基于 2D 轨迹，缺乏深度和方位信息 | 6D 姿态（3D 平移 + 3D 旋转），使模型感知物体的空间方位和距离 |
| 损失函数 | 标准扩散 MSE 损失，不区分运动来源 | L_cam 使用背景掩码强制背景跟随相机；L_obj 使用前景掩码在保留物体姿态的同时抑制前景中的相机运动效应 |

这一设计链条的因果逻辑是：**完整的 6D 标注数据是解耦训练的前提，而专用区域损失是将数据中的分离信号转化为模型解耦能力的关键机制。** 消融实验（Table 5）提供了强因果证据：移除 L_cam 后，相机平移误差从 18.12 升至 20.35，旋转误差从 1.03 升至 1.19；移除 L_obj 后，物体平移误差从 42.25 升至 46.62，旋转误差从 0.96 升至 1.15。仅使用标准扩散损失训练 CMC 会导致前景漂移而非准确的相机运动（Figure 12）。

### 3. 适用边界与已知局限

尽管 FMC 在解耦控制上取得了突破，其适用边界受以下因素制约：

- **多对象复杂交互。** 当前版本在控制多个对象的复杂运动时能力有限，可能导致生成视频不够自然。这一问题源于 SynFMC 数据集中多对象交互场景的覆盖不足，以及 OMC 模块在设计上主要针对单对象场景。
- **合成数据到真实场景的泛化。** FMC 的训练和评估均基于合成数据。虽然 Domain LoRA 在一定程度上弥合了渲染风格与真实风格的域差距，但模型在真实世界场景下的泛化能力——特别是面对复杂光照、遮挡和多样化的物体外观时的鲁棒性——仍缺乏系统验证。
- **运动评估指标的不足。** 现有的定量指标（如 CamTransErr、ObjTransErr）可能无法完全代表视频质量，特别是物体运动的自然度和与场景上下文的协调性。用户研究（Table 4）虽然提供了补充，但主观评估的可复现性和规模有限。

### 4. 开放问题与未来方向

基于上述局限，该方向存在以下开放问题：

1. **更准确的物体运动评估指标。** 如何设计客观指标来衡量物体运动的真实性、与物理规律的符合度以及与场景上下文的一致性？现有指标主要关注姿态误差，但忽略了运动轨迹的自然性和时序连贯性。

2. **多对象复杂交互运动的控制。** 如何扩展 FMC 框架以支持多个对象之间的协调运动控制？这需要在数据集层面增加多对象交互场景，并在模型层面设计对象间的运动协调机制。

3. **跨域泛化能力验证。** 合成数据训练的模型在真实世界场景下的泛化能力需要系统性的基准测试和评估协议，这是将该方法推向实际应用的关键一步。

4. **额外输入模态的融合。** 论文指出未来需要额外输入模态（如图像）来定制参考主体的运动视频，这暗示了将 FMC 与个性化生成、视频编辑等任务结合的可能性。

## 原文 PDF

![[paperPDFs/arxiv_2025/Free_Form_Motion_Control_A_Synthetic_Video_Generation_Dataset_with_Controllable_Camera_and_Object_Motions.pdf]]