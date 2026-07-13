---
title: "Motion Prompting: Controlling Video Generation with Motion Trajectories"
type: paper
paper_level: A
venue: CVPR
year: 2025
pdf_ref: paperPDFs/CVPR_2025/Motion_Prompting_Controlling_Video_Generation_with_Motion_Trajectories.pdf
project_link: https://motion-prompting.github.io/
code_link: null
aliases:
- MPCVGMT
tags:
- CVPR_2025
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/robotics
core_operator: "运动轨迹（motion prompts）作为条件，通过改变轨迹（稀疏/密集、位置、可见性）直接控制生成视频的运动模式。"
primary_logic: "采用点轨迹作为统一的、灵活的运动表示，结合ControlNet适配器训练单阶段模型，能够有效编码任意数量和类型的运动；并通过运动提示扩展（motion prompt expansion）将用户高级意图自动转化为详细的运动轨迹，实现多种运动控制任务的统一框架。"
claims:
- "在DAVIS验证集上，本方法在PSNR、SSIM、LPIPS、FVD、EPE等指标上全面优于基线方法Image Conductor和DragAnything。"
- "人工研究显示，在运动坚持度、运动质量和视觉质量方面，本方法均被参与者显著偏好。"
- "本模型能够泛化到训练中未见过的稀疏轨迹、局部轨迹以及非首帧起始的轨迹。"
- "消融实验表明训练时使用密集轨迹优于使用稀疏轨迹，即使在测试时使用稀疏轨迹也不例外。"
---

# Motion Prompting: Controlling Video Generation with Motion Trajectories

> [!tip] 核心洞察
> 采用点轨迹作为统一的、灵活的运动表示，结合ControlNet适配器训练单阶段模型，能够有效编码任意数量和类型的运动；并通过运动提示扩展（motion prompt expansion）将用户高级意图自动转化为详细的运动轨迹，实现多种运动控制任务的统一框架。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 运动提示：利用运动轨迹控制视频生成 |
| 英文题名 | Motion Prompting: Controlling Video Generation with Motion Trajectories |
| 会议/期刊 | CVPR 2025 |
| Links | [paper](https://arxiv.org/abs/2412.02700) · [Project](https://motion-prompting.github.io/) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/robotics |
| Method | Motion Prompting |
| Dataset | DAVIS Validation (N=2048), DAVIS Validation (N=512), Human Study (2AFC) |

> [!tip] 效果简介
> - DAVIS Validation (N=2048) 上，PSNR↑ 为 19.327，对比 11.609 (Image Conductor), 14.845 (DragAnything)，变化 +7.718 / +4.482。
> - DAVIS Validation (N=2048) 上，EPE↓ 为 3.887，对比 33.561 (Image Conductor), 12.485 (DragAnything)，变化 -29.674 / -8.598。
> - DAVIS Validation (N=512) 上，LPIPS↓ 为 0.229，对比 0.524 (Image Conductor), 0.381 (DragAnything)，变化 -0.295 / -0.152。

## 概要

### 问题瓶颈

现有视频生成模型在运动控制上高度依赖文本提示，但自然语言难以精确表达运动的细微动态、时序关系和空间细节——例如“加速靠近”、“缓慢旋转”或“先向右再向上”的复合动作。文本的模糊性导致生成结果在运动坚持度（motion adherence）和物理合理性上存在明显短板。

### 核心方案

**Motion Prompting** 提出以**点轨迹**作为统一的运动表示，将运动控制问题转化为“给定轨迹条件生成视频”的任务。其核心思路分为两步：

1. **训练阶段**：在预训练文本-视频扩散模型（Lumiere）之上，训练一个 ControlNet 适配器，接受任意稀疏或密集的点轨迹作为条件信号。每条轨迹包含 $N \times T$ 个二维坐标 $\mathbf{p} \in \mathbb{R}^{N \times T \times 2}$ 及对应的可见性标志 $\mathbf{v} \in \mathbb{R}^{N \times T}$，通过唯一的正弦位置编码嵌入到时空体积中（见 Figure 2）。训练采用单阶段、均匀采样密集轨迹的策略，无需特殊数据筛选或复杂工程。

2. **推理阶段**：通过**运动提示扩展**将用户的高级意图自动转化为详细的运动轨迹。用户可以通过鼠标拖拽、几何图元操作、深度估计等多种方式输入意图，系统将其转换为半密集的点轨迹，驱动视频生成。这一机制使得单一训练模型即可支持物体控制、相机控制、运动传递、拖拽编辑等多种应用（见 Figure 1）。

### 关键结论

- **定量优势**：在 DAVIS 验证集上，Motion Prompting 在 PSNR（19.327）、EPE（3.887）、LPIPS（0.229）等指标上全面优于基线方法 Image Conductor 和 DragAnything（Table 1）。
- **人类偏好**：2AFC 人类研究中，本方法在运动坚持度、运动质量和视觉质量三个维度上均获得超过 73% 的胜率（Table 2）。
- **泛化能力**：模型能够泛化到训练中未见过的稀疏轨迹、局部轨迹以及非首帧起始的轨迹（Figure 3, Figure 6）。
- **消融发现**：训练时使用密集轨迹（约 1000–2000 条）显著优于稀疏轨迹，即使在测试时仅使用稀疏轨迹也不例外（Table 3）。

### 方法谱系与知识库定位

Motion Prompting 属于**轨迹条件视频生成**这一新兴方向。与基于 AnimateDiff 微调的 **Image Conductor** 和基于 Stable Video Diffusion 的 **DragAnything** 相比，本方法的关键差异在于：

| 维度 | 基线方法 | Motion Prompting |
|------|---------|------------------|
| 运动条件 | 纯文本或简单稀疏轨迹 | 文本 + 任意稀疏/密集点轨迹（含可见性） |
| 训练策略 | 多阶段微调、特定损失、数据筛选 | 单阶段 ControlNet，均匀密集轨迹采样 |
| 用户交互 | 手动设计轨迹 | 运动提示扩展，自动将高级意图转为轨迹 |

该方法在知识库中的定位是：**以点轨迹为统一原语，桥接用户意图与视频扩散模型**，将多种运动控制任务纳入单一框架，避免了为不同任务设计独立模型的需求。

### 主要局限

- 运动条件可能错误地将物体部分与背景锁定，导致不自然拉伸。
- 底层视频模型可能违反物理约束，生成不合理物体（如棋子复制）。
- 生成速度慢（单视频约 12 分钟），不支持实时交互或因果生成。
- 极端相机运动下组合运动提示可能不准确。

视频生成模型近年来取得了显著进展，但精确的运动控制仍然是一个核心瓶颈。现有方法主要依赖文本提示（text prompts）来引导视频中的运动，然而自然语言在表达运动的细微动态、时序关系和空间细节方面存在固有局限。例如，文本难以精确描述“加速旋转”、“同步动作”或“部分遮挡下的运动轨迹”等复杂运动模式。这种文本与运动之间的语义鸿沟，使得用户无法对生成视频中的物体运动、相机运动及其组合进行细粒度的、可预期的控制。

为弥补这一缺口，一些工作开始探索超越纯文本的运动控制方式。例如，**Image Conductor** 基于 AnimateDiff 微调，尝试使用轨迹条件引导视频生成；**DragAnything** 则在 Stable Video Diffusion 基础上针对实体移动引入轨迹控制。然而，这些基线方法通常采用多阶段微调、特定损失函数或复杂的数据筛选等工程手段，且往往仅支持稀疏轨迹或特定类型的运动，缺乏统一的运动控制框架。

本文的核心动机在于：**是否存在一种统一的运动表示，既能灵活编码从稀疏到密集、从局部物体到全局场景的任意运动，又能通过简洁的训练策略和直观的用户交互实现多样化的运动控制任务？**

为此，本文提出 **Motion Prompting** 方法，其核心洞察是采用**点轨迹（point trajectories）**作为统一的运动表示。点轨迹天然具备以下优势：（1）可编码空间和时间上稀疏或密集的运动；（2）可描述单个物体或整个场景的运动；（3）通过可见性标志（visibility flag）可处理遮挡和出屏情况。基于这一表示，本文在预训练视频扩散模型 Lumiere 之上训练一个 ControlNet 适配器，以单阶段方式注入运动轨迹条件，无需复杂的工程技巧。在推理阶段，通过**运动提示扩展（motion prompt expansion）**机制，将用户的高级意图（如鼠标拖拽、几何图元操作、深度估计等）自动转化为详细的运动轨迹，从而在单一训练模型上实现物体控制、相机控制、运动传递、模型探测等多种能力。

## 核心方法与创新机理

本工作的核心创新在于提出**运动提示（Motion Prompting）**——一种以点轨迹为统一运动表示的视频生成控制范式。相较于现有方法，其关键改变体现在三个维度：

### 1. 运动条件信号：从文本到轨迹

现有视频生成模型（如 **Image Conductor**、**DragAnything**）主要依赖文本提示或简单的稀疏轨迹进行运动控制。文本难以精确表达运动的细微动态、时序关系和空间细节（如加速、同步动作等），而稀疏轨迹则缺乏对场景整体运动的约束能力。

本方法将运动条件信号统一为**任意稀疏或密集的点轨迹集合**，形式化定义为：

$$\mathbf{p} \in \mathbb{R}^{N \times T \times 2}$$

其中 $N$ 为轨迹数量，$T$ 为时间长度，每条轨迹在每个时间步包含二维坐标 $(x, y)$。同时引入可见性数组 $\mathbf{v} \in \mathbb{R}^{N \times T}$，标记轨迹在每一帧是否可见（1表示可见，0表示遮挡或出屏）。这一表示能够统一编码稀疏/密集运动、单物体/全场景运动，甚至通过可见性标志处理遮挡。

轨迹被编码为 $T \times H \times W \times C$ 维的时空条件体积（Figure 2），编码规则为：

$$\mathbf{c}[t, x_{t}^{n}, y_{t}^{n}] = \mathbf{v}[n, t] \phi_{n}$$

即每条轨迹被分配唯一的正弦位置编码嵌入 $\phi_n$，在轨迹经过且可见的时空位置写入该嵌入，其余位置置零。这一策略可以编码任意数量和配置的轨迹。

### 2. 训练策略：单阶段简化

许多现有工作采用多阶段微调、特定损失函数、数据筛选等复杂工程手段。本方法采用**单阶段训练**：在预训练文本-视频扩散模型 **Lumiere**（生成128×128、80帧、16fps视频，输入为文本和第一帧）之上，附加 **ControlNet 适配器**（复制 Lumiere 编码器并加入零卷积，首层替换为接受 $T \times H \times W \times C$ 条件信号的卷积层）。训练时均匀采样约1000-2000条密集轨迹，无需特殊数据筛选。

消融实验（Table 3）提供了关键证据：密集训练（Dense）在 N=2048 时 PSNR 达 19.197，远超稀疏训练（Sparse）的 15.697，表明训练时使用密集轨迹对遵循大量轨迹至关重要。训练过程中还观察到“突然收敛”现象（Figure A2）：在约20000步时模型突然学会遵循控制信号，且训练损失与模型性能不相关。

### 3. 运动提示扩展：从高级意图到详细轨迹

推理阶段，本方法通过**运动提示扩展（motion prompt expansion）**将用户的高级意图自动转化为详细的半密集轨迹，无需用户手动设计复杂的轨迹配置。具体扩展模式包括：

- **鼠标交互**（Figure 3）：将鼠标拖拽转化为以光标为中心的轨迹网格，支持“推拉”物体、拨动头发等交互。
- **几何图元控制**（Figure 6）：通过代理几何体（如球体）重新解释鼠标运动，实现对物体的精细控制（如旋转），这是单条轨迹无法表达的。
- **深度估计相机控制**（Figure 5）：利用单目深度估计器获取场景点云，根据相机轨迹重投影生成运动提示，实现相机运动控制——模型在训练中从未见过相机姿态，却能泛化出这一能力。
- **运动提示组合**（Figure 7）：将物体控制轨迹转换为位移量，叠加到相机控制轨迹上，实现物体与相机的同时控制。

这一设计使得单一训练模型能够支持物体控制、相机控制、运动传递、模型探测等多种应用，构成统一的运动控制框架。

Motion Prompting 的整体管线由两个阶段构成：**训练阶段**构建一个通用的轨迹条件视频生成模型；**推理阶段**则通过运动提示扩展（motion prompt expansion）将用户的高级意图转化为详细的运动轨迹，驱动该模型生成视频。

### 训练阶段：轨迹条件视频扩散模型

训练阶段的核心是在预训练视频扩散模型之上附加一个 ControlNet 适配器，使其能够接受点轨迹作为运动条件信号。整个训练流程如下：

1. **基础模型**：采用预训练的文本-视频扩散模型 **Lumiere** 作为骨干网络。该模型以文本提示和第一帧图像为输入，生成 128×128 分辨率、80 帧、16 fps 的视频。

2. **运动条件表示**：运动提示被定义为点轨迹集合 $\mathbf{p} \in \mathbb{R}^{N \times T \times 2}$，即 $N$ 条长度为 $T$ 的二维轨迹，每条轨迹在每个时间步包含一个 $(x, y)$ 坐标。同时，每条轨迹配有可见性数组 $\mathbf{v} \in \mathbb{R}^{N \times T}$，标记该点在每一帧是否可见（1 表示可见，0 表示遮挡或出屏）。

3. **轨迹编码器（Track Encoder）**：将点轨迹转换为时空条件体积。具体而言，为每条轨迹分配一个唯一的随机嵌入向量 $\phi_n \in \mathbb{R}^C$，然后在轨迹经过且可见的时空位置写入该嵌入：
   $$\mathbf{c}[t, x_t^n, y_t^n] = \mathbf{v}[n, t] \phi_n$$
   其余位置置零。这一设计使得条件体积能够编码任意数量和配置的轨迹，无论稀疏或密集。

4. **ControlNet 适配器**：复制 Lumiere 编码器的结构，并在其首层替换为接受 $T \times H \times W \times C$ 条件信号的卷积层，通过零卷积（zero convolution）将轨迹条件注入扩散模型的去噪过程。训练时仅优化适配器参数，冻结基础模型权重。

5. **训练策略**：单阶段训练，从视频数据中均匀采样约 1000–2000 条密集轨迹作为条件，无需特殊的数据筛选或复杂的多阶段微调工程。值得注意的是，训练过程中观察到“突然收敛”现象——在约 20000 步时模型突然学会遵循控制信号，而训练损失与测试指标之间并无相关性。

### 推理阶段：运动提示扩展

推理阶段的关键创新在于**运动提示扩展**（motion prompt expansion），即将用户的高级意图自动转化为详细的半密集轨迹，从而驱动训练好的模型生成视频。该过程支持多种应用模式：

- **鼠标交互**：将用户的鼠标拖动操作转化为以光标为中心的轨迹网格，实现对图像局部区域的“互动”（如移动物体、扰动头发或沙粒）。
- **几何图元控制**：通过代理几何体（如球体）重新解释鼠标运动，实现对物体的精细控制（如旋转），弥补单条轨迹无法表达的复杂运动。
- **相机控制**：利用单目深度估计器从输入帧获取场景点云，再根据指定的相机轨迹将点云重新投影，生成相机运动对应的轨迹。
- **运动组合**：将物体控制轨迹与相机控制轨迹相加（物体轨迹先转换为位移量），实现物体与相机的同步控制。
- **运动传递**：从源视频中提取运动轨迹，将其应用于目标图像，实现运动模式的迁移。

### 输入输出流

- **输入**：文本提示 + 第一帧图像 + 运动提示（任意稀疏或密集的点轨迹，含可见性信息）。
- **输出**：128×128 分辨率、80 帧、16 fps 的视频，其运动模式由输入轨迹控制。

该框架的统一性在于：单一训练模型无需针对不同控制任务进行微调，仅通过改变推理阶段的运动提示扩展方式，即可覆盖物体控制、相机控制、运动传递等多种应用场景。

### 运动提示：点轨迹与可见性

本方法的核心运动表示是点轨迹集合。给定一段时长为 $T$ 的视频，运动提示由 $N$ 条点轨迹及其可见性标志构成：

$$\mathbf{p} \in \mathbb{R}^{N \times T \times 2}$$

$$\mathbf{v} \in \mathbb{R}^{N \times T}$$

其中 $\mathbf{p}$ 的每个元素 $(x_t^n, y_t^n)$ 表示第 $n$ 条轨迹在时刻 $t$ 的二维空间坐标，$\mathbf{v}[n, t] \in \{0, 1\}$ 指示该时刻该轨迹是否可见（1 为可见，0 为遮挡或出屏）。这种统一表示能够灵活编码从稀疏到密集的任意数量和配置的运动，覆盖单物体、全场景乃至遮挡情形。

### 轨迹编码为时空条件体积

为将轨迹注入扩散模型，需要将上述集合编码为与视频潜空间兼容的时空条件体积。具体做法是：

1. 为每条轨迹 $n$ 分配一个唯一的随机正弦位置嵌入向量 $\phi_n \in \mathbb{R}^C$。
2. 构建一个 $T \times H \times W \times C$ 维的时空体积 $\mathbf{c}$，初始化为全零。
3. 对每条轨迹在每一时刻的可见位置进行赋值：

$$\mathbf{c}[t, x_t^n, y_t^n] = \mathbf{v}[n, t] \cdot \phi_n$$

即，在时空体积中，轨迹经过且可见的位置被写入该轨迹的唯一嵌入向量，其余位置保持为零。这一策略的关键优势在于：无论轨迹数量多少、空间分布如何，编码方式保持统一，且不同轨迹通过嵌入向量自然区分，无需显式分配轨迹 ID。

### ControlNet 适配器架构

模型构建于预训练的文本-视频扩散模型 **Lumiere** 之上，该基座模型以文本和第一帧为条件，生成 128×128 分辨率、80 帧、16 fps 的视频。运动条件的注入采用 ControlNet 范式：

- **可训练副本**：复制 Lumiere 编码器作为可训练分支，其余基座模型参数冻结。
- **零卷积层**：在可训练副本的每个编码器层后添加零初始化卷积，使训练初期条件信号不影响基座行为，保证训练稳定性。
- **首层替换**：将可训练副本的首层替换为可接受 $T \times H \times W \times C$ 条件信号的卷积层，用于接收上述时空条件体积。

训练时仅优化标准扩散损失，无需额外的专用损失函数或数据筛选策略。轨迹数据来自视频的密集光流估计，训练中均匀采样约 1000–2000 条密集轨迹。

### 运动提示扩展（推理阶段）

推理阶段的核心机制是**运动提示扩展**：将用户的高级意图自动转化为详细的半密集轨迹，再送入模型生成视频。这一过程不涉及模型参数的改变，而是通过计算机视觉信号在条件空间完成转换。主要扩展模式包括：

- **鼠标交互**：将鼠标拖拽轨迹扩展为以光标为中心的轨迹网格，同时可添加静态轨迹以固定背景。
- **几何图元控制**：将鼠标运动重新解释为对代理几何体（如球体）的操作，从而获得单条轨迹无法表达的精细控制（如旋转）。
- **深度相机控制**：通过单目深度估计器获取场景点云，再沿指定相机轨迹重投影，生成全场景的运动轨迹。
- **运动组合**：将物体控制轨迹转换为位移量，叠加到相机控制轨迹上，实现物体与相机的同步控制。

### 关键公式汇总

| 公式 | 含义 |
|------|------|
| $\mathbf{p} \in \mathbb{R}^{N \times T \times 2}$ | $N$ 条长度为 $T$ 的点轨迹集合 |
| $\mathbf{v} \in \mathbb{R}^{N \times T}$ | 轨迹可见性数组，$\{0,1\}$ 取值 |
| $\mathbf{c}[t, x_t^n, y_t^n] = \mathbf{v}[n, t] \phi_n$ | 时空条件体积赋值规则，可见位置写入轨迹嵌入，否则置零 |

## 实验与关键发现

### 定量评估

我们在DAVIS验证集上对Motion Prompting进行了系统的定量评估，并与两个轨迹条件视频生成基线方法——**Image Conductor**（基于AnimateDiff微调）和**DragAnything**（基于Stable Video Diffusion微调）——进行了对比。评估同时覆盖外观质量（PSNR、SSIM、LPIPS、FVD）和运动精度（EPE，端点误差），结果如Table 1所示。

![[assets/figures/papers/paper_list_l16_Motion_Prompting_Controlling_Video_Generation_with_Motion_Trajectories/figures/011_Table_1.jpg]]
*Table 1: Quantitative Evaluations. We evaluate the appearance (PSNR, SSIM, LPIPS, FVD) and motion (EPE) of generated videos on the validation set of the DAVIS dataset. Please note that each method is trained from a different base model*

在密集轨迹设置（N=2048）下，本方法在所有指标上均显著领先：PSNR达到19.327，相比Image Conductor的11.609提升+7.718，相比DragAnything的14.845提升+4.482；运动精度EPE仅为3.887，而Image Conductor为33.561（降低-29.674），DragAnything为12.485（降低-8.598）。在N=512设置下，LPIPS为0.229，远优于Image Conductor的0.524和DragAnything的0.381。

值得注意的是，DragAnything在极稀疏轨迹（N=1）下的EPE（9.135）优于本方法（14.619），但其外观指标全面落后。这一差异可能源于DragAnything在评估时额外使用了DAVIS数据集提供的真实分割掩码作为输入，而本方法无需此类辅助信息，因此该比较对本方法并不完全公平。此外，各方法基于不同的基础视频扩散模型（Lumiere vs AnimateDiff vs Stable Video Diffusion），这也会影响生成视频的视觉质量基准。

### 人类偏好研究

我们通过二选一强制选择（2AFC）人类研究进一步验证了方法的实际表现。参与者从运动坚持度（Motion Adherence）、运动质量（Motion Quality）和视觉质量（Visual Quality）三个维度对生成视频进行偏好判断。如Table 2所示，本方法在所有维度上均以显著优势胜出：相比Image Conductor，胜率分别为74.3%、80.5%和77.3%；相比DragAnything，胜率分别为74.5%、75.7%和73.7%。这表明运动轨迹条件不仅带来了精确的运动控制，也维持了良好的视觉质量。

![[assets/figures/papers/paper_list_l16_Motion_Prompting_Controlling_Video_Generation_with_Motion_Trajectories/figures/010_Table_2.jpg]]
*Table 2: Human Study. We present % win rates of our method against baselines in 2AFC human study results. Sample sizes are N = 1 0 3 . N = 1 0 3 , , and N = 1 1 5 for each column respectively*

### 消融实验

我们针对训练时的轨迹密度进行了关键消融（Table 3）。实验比较了三种训练策略：仅使用密集轨迹（Dense，约1000-2000条）、仅使用稀疏轨迹（Sparse，约100条）、以及密集与稀疏混合（Dense+Sparse）。结果表明，密集训练在N=2048测试设置下PSNR达19.197，远超稀疏训练的15.697和混合训练的15.294；在N=1设置下，密集训练的EPE为13.851，同样优于稀疏训练的23.727。这揭示了一个重要规律：即使在测试时仅使用稀疏轨迹，训练阶段使用密集轨迹也能显著提升模型对运动条件的遵循能力。密集轨迹提供了更丰富的运动监督信号，使模型学习到更鲁棒的运动表征。

![[assets/figures/papers/paper_list_l16_Motion_Prompting_Controlling_Video_Generation_with_Motion_Trajectories/figures/012_Table_3.jpg]]
*Table 3: Ablation. We ablate the density of tracks during training and find that training on dense tracks works best for our model*

### 泛化能力

模型展现出多方面的非平凡泛化能力，尽管训练时仅使用均匀采样的全帧密集轨迹。定性实验表明：

- **稀疏轨迹泛化**：模型能够遵循远少于训练时的轨迹数量（如单条拖拽轨迹），如Figure 3和Figure 4中的鼠标交互编辑场景。
- **空间局部化泛化**：训练轨迹均匀分布于整个画面，但模型能泛化到仅覆盖局部区域的轨迹条件，如物体控制中的几何图元操作（Figure 6）。
- **非首帧起始泛化**：尽管训练轨迹均从第一帧开始，模型仍能处理从中间帧起始的轨迹，如Figure 3b中的头发交互场景，这在训练中从未出现过。

![[assets/figures/papers/paper_list_l16_Motion_Prompting_Controlling_Video_Generation_with_Motion_Trajectories/figures/003_Figure_3.jpg]]
*Figure 3: “Interacting” with an Image. We translate a simple user input, mouse motions and drags, and expand it into a more complex motion prompt which helps to achieve the user’s intention. The mouse trajectories are visualized as a hand when dragging, and as a black cursor otherwise. A grid of tracks centered on the cursor are created when the mouse is dragged, as shown in the top row. Frames from the generated video are shown in the bottom row. Prompting our model in this way, we can (a) move the head of a parrot or (c) a cow (b) play with hair or (d) “interact” with an image of sand. We can also keep the background still by specifying static tracks, as in (b) or (d). Note these samples are not ge...*

### 训练动力学中的“突然收敛”

我们在训练过程中观察到一个值得关注的现象：模型在大约20000步时出现“突然收敛”（sudden convergence），测试指标（PSNR、SSIM、LPIPS、EPE）在此之前几乎无改善迹象，随后在极短步数内迅速提升至较高水平（Figure A2）。与此同时，训练损失曲线与测试指标之间不存在相关性——损失持续下降而测试指标长期停滞。这一现象的具体机制尚不明确，但提示了轨迹条件视频扩散模型训练中可能存在独特的相变行为，值得进一步研究。

### 失败模式与模型探测

通过运动提示，我们可以主动探测底层视频先验模型的局限性（Figure 9）。主要失败模式包括：

- **物理违背**：拖拽棋子时，模型可能生成一枚新棋子而非移动原有棋子，表明底层模型对物体恒存性和物理交互的理解不足。
- **不自然变形**：运动条件可能错误地将物体局部区域与背景锁定，导致不自然的拉伸效果（如牛角被拉长）。
- **组合运动误差**：在极端相机运动下，物体控制与相机控制的组合运动提示可能产生不准确的轨迹叠加效果。

这些失败模式本质上反映的是底层Lumiere模型的限制，而非运动提示框架本身的问题，但也指明了未来改进方向——增强视频先验模型对物理规律和物体恒存性的建模能力。

### 推理效率

当前模型的生成速度较慢，单个视频（128×128分辨率、80帧、16fps）约需12分钟，远未达到实时交互的要求。这是限制该方法走向实际交互式应用的主要工程瓶颈。

![[assets/figures/papers/paper_list_l16_Motion_Prompting_Controlling_Video_Generation_with_Motion_Trajectories/figures/014_Table.jpg]]
*Table: A1. Figure Details. We provide details about qualitative samples shown in our figures, including text prompts fed to the model and licensing information. In general, these are sorted by the order that they appear in the paper, moving from left to right, top to bottom*

![[assets/figures/papers/paper_list_l16_Motion_Prompting_Controlling_Video_Generation_with_Motion_Trajectories/figures/017_Table.jpg]]
*Table: A2. Quantitative Evaluations. We evaluate the appearance (PSNR, SSIM, LPIPS, FVD) and motion (EPE) of generated videos using the validation set of the DAVIS dataset. Please note that each method is trained from a different base model*

## 定位与知识库关联

### 1. 核心问题与现有方法瓶颈

现有视频生成模型主要依赖文本提示进行运动控制，但文本天然地难以精确表达运动的细微动态、时序和空间细节（如加速、同步动作等）。为了解决这一问题，此前的工作尝试引入多种条件信号，但各自存在局限：

- **轨迹条件方法**：**Image Conductor** 基于 AnimateDiff 微调，**DragAnything** 基于 Stable Video Diffusion 微调，两者均支持轨迹条件视频生成，但前者在运动精度（EPE）上表现较弱，后者则需要额外的分割掩码输入，且两者在视觉质量和运动坚持度上均不如本文方法（见 Table 1、Table 2）。
- **多阶段工程化方法**：许多现有工作依赖多阶段微调、特定损失函数设计、数据筛选等复杂工程手段来提升控制精度，增加了训练和部署的复杂度。

本文的核心洞察在于：**点轨迹是一种统一且灵活的运动表示**，能够编码任意数量和类型的运动（稀疏/密集、局部/全局、可见/遮挡），结合 ControlNet 适配器进行单阶段训练，即可有效注入运动控制信号，无需复杂的工程化设计。

### 2. 方法变革与创新点

本文提出的 **Motion Prompting** 方法在以下关键维度上实现了对基线的系统性改进：

| 变革维度 | 基线方法 | 本文方法 | 证据锚点 |
|---------|---------|---------|---------|
| **运动条件信号** | 纯文本提示或简单稀疏轨迹 | 文本提示 + 任意稀疏/密集点轨迹（含可见性信息） | Abstract, Section 3.1 |
| **训练策略** | 多阶段微调、特定损失、数据筛选 | 单阶段训练，均匀采样密集轨迹（约1000–2000条），ControlNet 附加零卷积 | Section 2, Section 3.4, Appendix A.1 |
| **运动提示生成** | 用户直接提供稀疏轨迹或手动设计 | 运动提示扩展（motion prompt expansion）：鼠标拖动、几何图元、深度估计等自动将高级意图转化为半密集轨迹 | Section 4, Section 4.1–4.5 |

**因果控制机制**：运动轨迹（motion prompts）作为条件信号，通过改变轨迹的稀疏/密集程度、空间位置和可见性，直接控制生成视频的运动模式。轨迹被编码为时空体积 $\mathbf{c} \in \mathbb{R}^{T \times H \times W \times C}$，每条轨迹分配唯一正弦位置编码 $\phi_n$，在轨迹经过且可见的时空位置写入嵌入，其余位置置零：

$$\mathbf{c}[t, x_t^n, y_t^n] = \mathbf{v}[n, t] \phi_n$$

这种编码方式支持任意数量和配置的轨迹，是模型泛化能力的关键基础。

### 3. 知识库定位与适用边界

**方法定位**：Motion Prompting 属于 **轨迹条件视频生成** 的范畴，其核心贡献在于：
1. 将点轨迹确立为统一的运动表示，统一了物体控制、相机控制、运动传递等多种任务；
2. 通过运动提示扩展，将用户高级意图自动转化为详细轨迹，降低了使用门槛；
3. 证明了单阶段 ControlNet 训练即可实现强大的轨迹条件遵循能力。

**适用边界**：
- **优势场景**：需要精确运动控制的视频生成任务，包括物体拖拽编辑、相机轨迹控制、物体与相机同时控制、运动传递、模型探测等。
- **已知局限**：
  - 运动条件可能错误地将物体部分与背景锁定，导致不自然拉伸（如牛角变形）。
  - 底层视频模型可能违反物理约束，生成不合理物体（如棋子复制）。
  - 生成速度慢，非实时（单个视频约需12分钟）。
  - 组合运动提示在极端相机运动下可能不准确。
  - 目前不支持因果生成，仅能生成固定长度视频。

### 4. 未解决问题与未来方向

本文揭示了若干有待深入探索的方向：

1. **物理规律遵循度**：如何进一步提升模型对物理规律的遵循度，避免生成违背常识的物体或运动？
2. **实时生成**：能否实现实时或接近实时的生成，以支持真正的交互式应用？
3. **点跟踪精度**：更精确的点跟踪算法是否可以消除运动放大中的平滑步骤，提升性能？
4. **训练稳定性**：训练中观察到的“突然收敛”现象（约20000步时模型突然学会遵循控制信号，且训练损失与模型性能不相关，见 Figure A2）的内在机制是什么？如何改进训练稳定性？
5. **长视频与多物体交互**：模型是否能够泛化到更长的视频生成或更复杂的多物体交互场景？

**注意**：本文与基线方法（Image Conductor、DragAnything）基于不同的基础模型（Lumiere vs AnimateDiff vs Stable Video Diffusion），这可能影响生成视频视觉质量的直接比较。此外，DAVIS 评估中 DragAnything 需要额外的分割掩码输入（本文方法不需要），但评估时使用了数据集提供的真实掩码，可能有利于 DragAnything——这些因素在解读定量结果时需加以考虑。

## 原文 PDF

![[paperPDFs/CVPR_2025/Motion_Prompting_Controlling_Video_Generation_with_Motion_Trajectories.pdf]]
