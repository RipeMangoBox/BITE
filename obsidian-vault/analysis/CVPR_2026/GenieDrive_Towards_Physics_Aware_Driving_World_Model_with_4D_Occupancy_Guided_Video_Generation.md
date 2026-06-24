---
title: "GenieDrive: Towards Physics-Aware Driving World Model with 4D Occupancy Guided Video Generation"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/GenieDrive_Towards_Physics_Aware_Driving_World_Model_with_4D_Occupancy_Guided_Video_Generation.pdf
project_link: null
code_link: null
aliases:
- GenieDrive
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/image_and_video_generation
- topic/vision_multimodal_applications/3d_rendering_reconstruction
- topic/generative_models_diffusion
core_operator: 引入4D占用作为中间物理表示，将任务分解为占用预测和视频生成两个阶段，在占用预测中显式建模控制对场景演化的影响，从而为视频生成提供物理先验。
primary_logic: 通过三平面VAE将高分辨率占用压缩为紧凑潜在表示，结合互控制注意力(MCA)和端到端训练实现高效准确的占用预测，再利用归一化多视角注意力(MVA)将预测占用转化为物理一致的多视角驾驶视频，从而克服黑盒模型的物理偏差。
claims:
- GenieDrive在占用预测任务上相较SOTA I2-World提升7.2% mIoU，仅用3.47M参数且推理速度达41 FPS。
- GenieDrive视频生成FVD相较UniScene降低20.7%，实现更长序列的多视角一致性生成。
- 在Trajectory-Controlled视频生成中，Vista和Epona无法正确响应左/右转指令，而GenieDrive可生成物理合理的转弯视频。
- 端到端训练将预测mIoU从39.79提升至42.59，而同类方法DOME和I2-World的端到端训练则导致性能崩溃或下降。
---

# GenieDrive: Towards Physics-Aware Driving World Model with 4D Occupancy Guided Video Generation

> [!tip] 核心洞察
> 通过三平面VAE将高分辨率占用压缩为紧凑潜在表示，结合互控制注意力(MCA)和端到端训练实现高效准确的占用预测，再利用归一化多视角注意力(MVA)将预测占用转化为物理一致的多视角驾驶视频，从而克服黑盒模型的物理偏差。

| 字段 | 内容 |
|------|------|
| 中文题名 | GenieDrive：基于4D占用引导视频生成的物理感知驾驶世界模型 |
| 英文题名 | GenieDrive: Towards Physics-Aware Driving World Model with 4D Occupancy Guided Video Generation |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2512.12751) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/image_and_video_generation #topic/vision_multimodal_applications/3d_rendering_reconstruction #topic/generative_models_diffusion |
| Method | GenieDrive |
| Dataset | NuScenes Occ3D, NuScenes Multi-view Video Generation |

> [!tip] 效果简介
> - NuScenes Occ3D 上，Forecasting mIoU (Avg. 1s-3s) 42.59% vs 39.73% (I2-World) (+7.20%)；Forecasting IoU (Avg. 1s-3s) 51.80% vs 49.80% (I2-World) (+4.00%)；Inference Speed (FPS) 41.38 FPS vs 37.04 FPS (I2-World) (faster)。
> - NuScenes Multi-view Video Generation (81 frames) 上，FVD (lower is better) 55.93 (GenieDrive-S) vs 70.52 (UniScene) (-20.7%)。

## 概述

现有视频驾驶世界模型普遍采用单阶段黑盒扩散范式，直接将驾驶控制信号映射为视频帧。这一范式缺乏显式的物理建模与约束，使得模型对训练数据中的分布偏差高度敏感——当控制指令偏离常见模式（如转弯）时，预测结果往往出现物理不一致的失真的问题。与此同时，4D占用（4D occupancy）作为一种显式的三维场景表示，天然携带几何与语义信息，但现有占用世界模型在预测精度、参数规模和推理速度之间难以取得平衡。

GenieDrive 提出了一种两阶段生成框架来解决上述瓶颈。其核心思路是将4D占用作为物理感知的中间表示，将任务分解为**占用预测**和**视频生成**两个阶段：第一阶段基于历史占用与控制信号自回归预测未来占用，第二阶段以预测占用为条件生成多视角驾驶视频。这一分解使得控制信号对场景演化的影响在占用空间中显式建模，从而为视频生成提供物理先验，克服黑盒模型的分布偏差。

在占用预测阶段，GenieDrive 引入三平面 VAE（tri-plane VAE）将高分辨率占用压缩为紧凑的潜在表示，仅使用先前方法58%的潜在空间大小；同时设计互控制注意力（Mutual Control Attention, MCA）实现占用特征与控制信号的交互注入，并通过端到端联合训练VAE和预测模块来对齐表示空间。在视频生成阶段，GenieDrive 通过占用投影（Occupancy Splatting）将预测的4D占用渲染为多视角语义图，并利用归一化多视角注意力（Normalized Multi-View Attention, MVA）将预训练视频扩散模型扩展为多视角一致生成器。

实验结果表明，GenieDrive 在占用预测任务上相较 SOTA 方法 I2-World 提升 **7.2% mIoU**（42.59% vs. 39.73%），同时仅使用 **3.47M 参数**，推理速度达 **41 FPS**（Table 1）。在轨迹控制视频生成中，GenieDrive 能够正确响应左/右转指令，而 Vista 和 Epona 则无法生成物理合理的转弯视频（Figure 3）。视频生成质量方面，GenieDrive 相较 UniScene 降低 **20.7% FVD**（55.93 vs. 70.52），并支持长达 20 秒的多视角一致生成（Table 4, Figure 5a）。消融实验进一步验证了端到端训练、MCA 和归一化策略的关键作用——值得注意的是，同样的端到端训练施加于 DOME 和 I2-World 时，反而导致性能崩溃或下降（Table 3, Figure 10），表明 GenieDrive 的设计并非普适技巧的简单叠加，而是架构与训练策略的系统性协同。

## 背景与动机

驾驶世界模型旨在根据当前场景状态和驾驶控制信号，预测未来的驾驶场景演化。这类模型在自动驾驶的规划、仿真和数据生成中扮演着关键角色。近年来，视频生成模型的快速发展催生了一类**视频驾驶世界模型**——它们将驾驶控制信号直接映射为未来视频帧，试图以端到端的方式模拟驾驶场景的动态变化。

然而，这一直接映射范式存在根本性缺陷。现有方法将驾驶控制作为扩散模型的条件信号注入，缺乏对场景物理结构和运动规律显式建模。这种黑盒映射方式使得模型极易受到训练数据分布偏差的影响，导致对特定控制指令产生物理不一致的预测。如图3所示，**Vista**和**Epona**（Zhang et al., ICCV 2025）等代表性视频驾驶世界模型在直行场景下表现尚可，但面对左转和右转指令时无法生成物理合理的转弯视频——车辆姿态、场景几何与控制信号之间出现明显脱节。

这一瓶颈的根源在于：**视频像素空间中的生成缺乏对三维场景几何和物理约束的显式表征**。驾驶场景的本质是三维空间中的动态演化，而直接生成二维视频像素忽略了这一底层结构，使得模型难以学习控制信号与场景变化之间的因果关联。

与此同时，以**OccWorld**（Zheng et al., ECCV 2024）为代表的4D占用预测方法试图从三维占用的角度建模场景演化，为物理感知的场景预测提供了新思路。但这类方法通常采用分离训练策略——先训练VAE进行占用压缩，再独立训练预测模块——导致压缩表示与预测任务之间存在语义错位，限制了预测精度的进一步提升。此外，现有占用预测方法在长时序预测中性能退化严重，难以支撑实际驾驶场景中秒级以上的未来推演。

基于上述分析，本文的核心动机是：**能否将4D占用作为连接物理建模与视觉生成的桥梁，通过显式的中间物理表示克服黑盒视频生成的物理偏差？** 这一思路将驾驶世界建模分解为两个阶段——先预测物理一致的4D占用，再将其渲染为多视角视频——从而在占用预测阶段显式建模控制信号对场景演化的影响，为视频生成提供强物理先验。GenieDrive正是沿着这一方向，通过三平面VAE压缩、互控制注意力机制和端到端训练策略，构建了一个物理感知的驾驶世界模型。

## 核心创新

GenieDrive的核心创新在于将驾驶世界模型从“黑盒映射”重构为“物理中间表示引导的两阶段生成”，通过引入**4D占用（4D Occupancy）**作为显式物理先验，从根本上改变了控制信号到视频的生成路径。

### 从黑盒映射到物理引导的两阶段框架

现有视频驾驶世界模型（如**Vista**、**Epona** (Zhang et al., ICCV 2025)）采用单阶段扩散模型，直接将驾驶控制信号映射为视频帧。这种黑盒范式缺乏对场景物理结构的显式建模，导致模型高度依赖训练数据的分布偏差——当控制指令偏离训练分布（如转弯）时，生成的视频往往出现物理不一致（Figure 3证实Vista和Epona无法正确响应左/右转指令）。

GenieDrive的两阶段框架（Figure 2）将生成过程解耦为：
1. **占用预测阶段**：基于当前占用和控制信号，自回归预测未来4D占用；
2. **视频生成阶段**：将预测占用渲染为多视角语义图，作为条件引导视频扩散模型生成。

这一解耦的因果逻辑在于：**控制信号直接影响的是场景的物理布局演化（占用），而非像素级外观**。通过在占用空间中显式建模控制对场景演化的影响，GenieDrive为视频生成提供了物理约束，从而克服了黑盒模型的分布外泛化困境。

### 三平面VAE：紧凑连续表示的关键

4D占用（$200 \times 200 \times 16 \times 17$类）的高分辨率特性使其难以直接作为预测模块的输入。GenieDrive提出**三平面VAE**，将占用编码为三个正交平面（XY、YZ、XZ）的紧凑潜在表示，解码时通过Hadamard积与位置编码恢复占用：

$$\hat{O} = f_{\psi}(Z_{xy} \odot Z_{yz} \odot Z_{xz} + \mathrm{PE}(x,y,z))$$

训练目标（Eq. 3）结合交叉熵、Lovász-softmax和KL散度：

$$\mathcal{L}_{\mathrm{VAE}} = \mathcal{L}_{\mathrm{CE}}(O, \hat{O}) + \mathcal{L}_{\mathrm{Lov}}(O, \hat{O}) + \mathcal{L}_{\mathrm{KL}}(Z, \mathcal{N}(\mathbf{0}, \mathbf{I}))$$

该设计的核心优势在于：**潜在尺寸仅为先前方法的58%**，且采用连续表示（而非离散VQ），为后续端到端训练提供了可微分的表示空间。消融实验（Table 3）证实，使用离散表示（VQ）的变体在端到端训练后性能下降，表明连续表示对端到端训练的适配性至关重要。

### 互控制注意力（MCA）：控制与占用的显式交互

传统方法将控制信号作为扩散条件直接注入，缺乏对控制如何影响场景结构的显式建模。GenieDrive在占用预测模块中引入**互控制注意力（MCA）**，实现占用特征与控制特征的双向交互（Eqs. 5-7）：

$$Z^{l\prime} = Z^l + \mathrm{Attn}(Q_{Z^l}, K_{c^l}, V_{c^l})$$

$$Z^{l+1} = Z^{l\prime} + \mathrm{Attn}(Q_{Z^{l\prime}}, K_{Z^{l\prime}}, V_{Z^{l\prime}})$$

$$c^{l+1} = c^l + \mathrm{Attn}(Q_{c^l}, K_{Z^{l+1}}, V_{Z^{l+1}})$$

该机制并非简单的条件注入，而是让占用特征查询控制信息，同时控制特征也查询更新后的占用特征，形成**互信息最大化**的交互模式。消融实验（Table 3）表明，移除MCA导致3秒预测mIoU从35.83骤降至30.48，证实其对长时预测的关键作用。

### 端到端训练：表示对齐的非平凡性

GenieDrive提出将三平面VAE与占用预测模块**端到端联合训练**（Eq. 10），直接监督未来占用的重建：

$$\mathcal{L}_{E2E} = \sum_{t=0}^{N} \beta_t \| O_{t+1}, f_{\theta}( \mathcal{F}_{pred}( \mathcal{F}_{\{xy,yz,xz\}} \circ g_{\phi}(O_t), c) ) \|^2$$

端到端训练将预测mIoU从39.79提升至42.59（Table 3），但代价是重建mIoU从86.15下降至70.07（Table 6），表明VAE的表示从“最优重建”向“最优预测”发生了**表示对齐偏移**。

这一策略的**非平凡性**体现在：对**DOME**施加端到端训练导致预测完全崩溃（mIoU从27.10降至0.43），**I2-World**端到端训练也导致性能下降（Figure 10）。这说明端到端训练的有效性依赖于特定的架构设计——GenieDrive的连续三平面表示和MCA设计共同构成了端到端训练的可行基础。

### 归一化多视角注意力（MVA）：稳定多视角生成

将预训练视频扩散模型适配为多视角生成时，直接引入多视角注意力会导致预训练先验崩溃。GenieDrive提出**归一化多视角注意力（MVA）**（Eq. 15）：

$$Z^{\prime} = Z + \eta \left( \frac{M - \mu_M}{\sigma_M} \sigma_Z + \mu_Z \right)$$

该设计将多视角注意力输出$M$归一化后重新缩放到主干特征$Z$的分布，通过超参数$\eta$控制多视角信息的注入强度。消融实验（Table 5）表明，移除归一化导致FVD从98.06飙升至212.67，并出现网格伪影（Figure 5b）；移除MVA则导致多视角生成不一致。

## 整体框架

GenieDrive采用**两阶段生成流水线**，将驾驶世界建模分解为4D占用预测与多视角视频生成两个阶段，以显式物理中间表示克服现有黑盒扩散模型对控制指令的物理不一致响应。

### 流水线总览

如Figure 2所示，整个框架由两条串联通路构成：

1. **占用预测阶段**：以当前时刻的4D占用 $O_t$ 和驾驶控制信号 $c$ 为输入，自回归地预测未来占用序列 $\{O_{t+1}, \dots, O_{t+N}\}$。该阶段的核心瓶颈在于高分辨率占用的高效压缩与控制的精确注入。
2. **视频生成阶段**：将预测的未来占用通过**占用溅射（Occupancy Splatting）**渲染为多视角语义图 $\mathbf{M}$，作为条件注入预训练视频扩散Transformer（DiT），生成物理一致的多视角驾驶视频。

这种分解的核心因果机制在于：**控制信号对场景演化的影响在占用空间中显式建模**，而非以黑盒方式直接映射到像素空间，从而为视频生成提供强物理先验，缓解训练数据分布偏差导致的转弯等指令响应失败。

### 模块组成与数据流

四个关键模块按数据流依次连接：

| 模块 | 功能 | 输入 → 输出 |
|------|------|-------------|
| **Tri-plane VAE** | 将高分辨率4D占用压缩为紧凑的三平面潜在表示 $Z$，并支持解码重建 | $O_t \rightarrow Z_t$（编码）；$Z_t \rightarrow \hat{O}_t$（解码） |
| **Occupancy Prediction Module (with MCA)** | 基于历史潜在三平面和控制信号自回归预测未来潜在三平面 | $\{Z_t, c_t\} \rightarrow Z_{t+1}$ |
| **Occupancy Splatting** | 将4D占用投影到多摄像头视角，渲染为语义图作为视频生成条件 | $\{O_{t+1}, \dots, O_{t+N}\} \rightarrow \mathbf{M}$ |
| **Normalized Multi-View Attention (MVA)** | 扩展预训练视频DiT以建模多视角关系，并通过归一化稳定微调 | $\mathbf{M}, \boldsymbol{x}_t \rightarrow \boldsymbol{x}_{t-1}$（扩散去噪） |

### 关键设计决策

- **三平面表示的选择**：与离散表示（VQ）相比，连续三平面表示是端到端训练有效性的必要条件。消融实验（Table 3）表明，使用离散表示的变体在端到端训练后性能反而下降，而连续表示变体则显著受益。
- **端到端训练的独特性**：GenieDrive的端到端训练联合优化VAE和预测模块，使潜在表示向预测任务对齐。这一策略并非普适有效——对**DOME**和**I2-World**施加端到端训练分别导致预测完全崩溃（mIoU从27.10降至0.43）和性能下降（Figure 10），说明该训练策略的有效性依赖于特定的架构设计。
- **归一化多视角注意力的稳定性作用**：在预训练视频DiT中直接插入多视角注意力会破坏预训练先验，产生网格伪影。通过将多视角特征归一化后重缩放至目标分布，可在不破坏预训练权重的前提下实现多视角一致性建模。

### 输入输出规范

- **输入**：4帧历史占用（NuScenes Occ3D格式）及对应的驾驶控制信号（轨迹/速度）。
- **输出**：6帧未来占用预测（默认1s-3s），以及81帧多视角驾驶视频（约3秒，可扩展至20秒）。
- **推理效率**：占用预测阶段仅需3.47M参数，推理速度达41 FPS（Table 1），视频生成阶段在8张NVIDIA L40S GPU上完成微调。

### 补充图表

![[assets/figures/papers/paper_list_l2502_https_arxiv_org_abs_2512_12751/figures/001_Figure_1.jpg]]
*Figure 1: (a) Overview of our GenieDrive. It predicts physically accurate future occupancy given the initial state and driving controls, and renders the occupancy into a video, enabling physics-aware multi-view driving video generation. (b) and (c) Performance of 4D occupancy forecasting and video generation. GenieDrive achieves the highest occupancy forecasting accuracy using the fewest parameters (bubble size denotes model size) and facilitates 8× longer multi-view driving video generation with notably enhanced generation quality*

![[assets/figures/papers/paper_list_l2502_https_arxiv_org_abs_2512_12751/figures/002_Figure_2.jpg]]
*Figure 2: Overall framework of GenieDrive. Our GenieDrive adopts a two-stage generation pipeline that first predicts future occupancy and then generates multi-view driving videos. In the occupancy generation stage, the current occupancy is encoded using a tri-plane VAE and processed by our Mutual Control Attention (MCA). The predicted occupancy is rendered into multi-view semantic maps, which are then fed into the DiT blocks enhanced by our Normalized Multi-View Attention (MVA) module to produce the final driving videos*

## 核心模块与公式推导

GenieDrive 的两阶段框架由四个关键模块串联构成：三平面 VAE（Tri-plane VAE）、互控制注意力占用预测模块（Occupancy Prediction with MCA）、占用投影渲染（Occupancy Splatting）以及归一化多视角注意力视频生成模块（Normalized MVA）。以下逐一展开其设计与核心公式。

### 三平面 VAE：紧凑潜在表示

为将高分辨率 4D 占用压缩为紧凑潜在表示，GenieDrive 设计了基于三平面（tri-plane）的变分自编码器。编码器将占用体素 $S \in \mathbb{R}^{h \times w \times d \times C}$ 沿高度维度重排为 $S^{\prime} \in \mathbb{R}^{(hw) \times d \times C}$，再通过卷积投影为三个正交平面特征 $Z_{xy}$、$Z_{yz}$、$Z_{xz}$。解码时，对体素坐标 $(x, y, z)$ 在三个平面上采样并施加 Hadamard 积与位置编码：

$$\hat{O} = f_{\psi}(Z_{xy} \odot Z_{yz} \odot Z_{xz} + \mathrm{PE}(x,y,z))$$

VAE 的训练损失由交叉熵、Lovász-softmax 与 KL 散度三项构成：

$$\mathcal{L}_{\mathrm{VAE}} = \mathcal{L}_{\mathrm{CE}}(O, \hat{O}) + \mathcal{L}_{\mathrm{Lov}}(O, \hat{O}) + \mathcal{L}_{\mathrm{KL}}(Z, \mathcal{N}(\mathbf{0}, \mathbf{I}))$$

该设计使潜在表示尺寸仅为先前方法的 58%（Table 1），大幅降低冗余。

### 互控制注意力（MCA）：控制信号与占用特征交互

现有方法常将驾驶控制信号作为条件直接注入扩散模型，缺乏对控制如何影响场景演化的显式建模。GenieDrive 在占用预测模块中引入**互控制注意力（Mutual Control Attention, MCA）**，使占用特征与控制特征在 Transformer 层中双向交互。给定层 $l$ 的占用特征 $Z^l$ 与控制特征 $c^l$，MCA 执行三步注意力：

$$Z^{l\prime} = Z^l + \mathrm{Attn}(Q_{Z^l}, K_{c^l}, V_{c^l})$$

$$Z^{l+1} = Z^{l\prime} + \mathrm{Attn}(Q_{Z^{l\prime}}, K_{Z^{l\prime}}, V_{Z^{l\prime}})$$

$$c^{l+1} = c^l + \mathrm{Attn}(Q_{c^l}, K_{Z^{l+1}}, V_{Z^{l+1}})$$

第一步将控制信息注入占用特征，第二步执行占用自注意力，第三步将更新后的占用信息反馈至控制特征。这种双向交互使模型能准确建模控制指令（如转弯、直行）对未来场景几何的影响。消融实验表明，移除 MCA 导致 3 秒处预测 mIoU 从 35.83 骤降至 30.48（Table 3），证实其对长时预测的关键作用。

### 占用预测训练目标

占用预测模块以自回归方式工作：输入历史潜在三平面 $Z_t$ 与控制信号 $c_t$，预测下一时刻潜在三平面 $Z_{t+1}$。训练时对预测序列逐帧施加监督，并加入中间变换正则项：

$$\mathcal{L}_{pred} = \sum_{t=0}^{N} \beta_t \| Z_{t+1}, \mathrm{ST}(\mathrm{Attn}(Z_t^m, c_t^m, c_t^m)) \|^2 + \lambda \mathcal{L}_{reg}$$

其中 $\beta_t$ 为逐帧权重，$\mathrm{ST}$ 表示中间变换监督（Intermediate Supervision Token）。

### 端到端训练：表示对齐

传统方法分两阶段先训练 VAE 再训练预测模块，导致潜在表示与预测任务不对齐。GenieDrive 提出端到端联合训练，直接监督未来占用的重建质量：

$$\mathcal{L}_{E2E} = \sum_{t=0}^{N} \beta_t \| O_{t+1}, f_{\theta}( \mathcal{F}_{pred}( \mathcal{F}_{\{xy,yz,xz\}} \circ g_{\phi}(O_t), c) ) \|^2$$

其中 $g_{\phi}$ 为 VAE 编码器，$\mathcal{F}_{\{xy,yz,xz\}}$ 为三平面投影，$\mathcal{F}_{pred}$ 为预测模块，$f_{\theta}$ 为解码器。端到端训练使预测 mIoU 从 39.79 提升至 42.59（Table 3），但代价是重建 mIoU 从 86.15 下降至 70.07（Table 6），体现了表示对齐中预测与重建的权衡。值得注意的是，对 **DOME** 和 **I2-World** 施加相同端到端训练导致性能崩溃或下降（Table 3, Figure 10），说明该策略并非普适有效，其成功依赖于连续三平面表示与 MCA 设计的协同。

### 占用投影渲染（Occupancy Splatting）

预测得到的 4D 占用需转化为视频扩散模型可理解的条件信号。GenieDrive 采用体素渲染（splatting）将占用投影到多相机视角，生成语义图 $\mathbf{M}$：

$$\mathbf{M} = \mathrm{argmax}( \sum_{i \in N} s_i \alpha_i \prod_{j=1}^{i-1} (1-\alpha_j) )$$

其中 $s_i$ 为沿射线的占用语义分数，$\alpha_i$ 为累积透明度。该语义图作为物理先验输入后续视频生成模块。

### 归一化多视角注意力（MVA）：稳定多视角视频生成

GenieDrive 将预训练视频 DiT（Diffusion Transformer）扩展为多视角生成器，在 DiT 块中插入**归一化多视角注意力（Normalized Multi-View Attention, MVA）**模块。核心挑战在于：直接注入多视角注意力会破坏预训练先验，导致训练不稳定。为此，MVA 对多视角注意力输出 $M$ 进行归一化，再重缩放至原始特征 $Z$ 的分布：

$$Z^{\prime} = Z + \eta \left( \frac{M - \mu_M}{\sigma_M} \sigma_Z + \mu_Z \right)$$

其中 $\eta$ 为控制多视角注意力强度的超参数。该归一化策略防止微调时预训练先验崩溃。视频生成微调采用速度预测损失（v-prediction）：

$$\mathcal{L}_{video} = \mathbb{E}_{\boldsymbol{x}_0, \boldsymbol{x}_1, \mathbf{M}, t} \| u(\boldsymbol{x}_t, \mathbf{M}, t; \theta) - \boldsymbol{v}_t \|^2$$

消融实验（Table 5, Figure 5b）表明：移除归一化导致 FVD 从 98.06 飙升至 212.67，并出现网格伪影；移除 MVA 则导致多视角生成不一致，同一车辆在不同视图下外观差异明显。

### 补充图表

![[assets/figures/papers/paper_list_l2502_https_arxiv_org_abs_2512_12751/figures/011_Figure_6.jpg]]
*Figure 6: Concatenated Tri-Plane Feature. To make tri-plane representation more suitable for the following processing, we concatenate three planes to get a unified feature representation*

![[assets/figures/papers/paper_list_l2502_https_arxiv_org_abs_2512_12751/figures/020_Figure_13.jpg]]
*Figure 13: Sim-to-Real Generation. The left side shows the BEV map of simulated driving scenes in the CARLA simulator. Our method possesses the ability to transform these simulated scenarios into realistic multi-view driving videos. The visualization results demonstrate that our method not only generates accurate ego-vehicle behaviors, such as left turns and overtaking, but also preserves important scene details, including surrounding vehicles highlighted with red boxes*

## 实验与分析

### 4D占用预测主结果

GenieDrive在NuScenes Occ3D基准上以极轻量的模型规模取得了最优的4D占用预测性能。如Table 1所示，在平均1s-3s的预测mIoU上，GenieDrive达到42.59%，相较此前SOTA方法**I2-World**的39.73%提升7.2%（相对提升）；预测IoU从49.80%提升至51.80%（+4.0%）。更关键的是，GenieDrive仅使用3.47M参数，不到I2-World（22.71M）的六分之一，同时推理速度达到41.38 FPS，实现了精度、效率与模型规模的全面领先。

这一优势在长时序预测中更加显著。如Table 2所示，在未经额外训练的情况下，GenieDrive在4s、5s、6s的预测mIoU分别维持在31.16%、27.17%和23.66%，而对比方法**OccWorld**（Zheng et al., ECCV 2024）和**I2-World**在超过3s后性能急剧退化。这表明三平面VAE的紧凑表示与互控制注意力（MCA）的建模能力在长时域上具有更强的稳定性。

### 轨迹控制视频生成定性对比

Figure 3展示了GenieDrive与**Vista**、**Epona**（Zhang et al., ICCV 2025）在轨迹控制视频生成上的定性对比。当给定左转（Turn Left）和右转（Turn Right）指令时，Vista和Epona无法正确响应转弯控制，生成的视频仍近似直行；而GenieDrive能够生成物理合理的转弯视频，车辆姿态与场景演化均与控制信号一致。这一差异直接验证了核心瓶颈论断：黑盒扩散模型缺乏物理建模，导致对分布外控制指令产生物理不一致的预测。

### 多视角视频生成量化对比

Table 4给出了多视角视频生成的量化对比。在81帧生成设定下，GenieDrive-S的FVD为55.93，相较**UniScene**的70.52降低20.7%，生成质量显著提升。在更长的生成长度上，GenieDrive同样保持优势，证明了占用引导的物理先验对长序列多视角一致性的关键作用。

### 消融实验：端到端训练与模型设计

**端到端训练的有效性与非普适性。** Table 3的消融实验揭示了端到端训练对GenieDrive的关键作用：移除端到端训练后，预测mIoU从42.59%降至39.79%。Table 6进一步展示了端到端训练过程中的动态权衡——随着训练epoch增加，预测性能逐步提升，而重建mIoU从86.15%下降至70.07%，表明VAE的潜在表示从“忠实重建”向“利于预测”对齐。

然而，端到端训练并非普适有效。对**DOME**施加端到端训练导致其预测完全崩溃（mIoU从27.10降至0.43），**I2-World**的端到端训练也导致性能下降和场景细节丢失（Figure 10）。这一对比表明，GenieDrive的三平面连续表示设计是端到端训练成功的前提条件——使用离散表示（VQ）的变体在端到端训练后性能同样下降（Table 3中w/o CR & E2E）。

![[assets/figures/papers/paper_list_l2502_https_arxiv_org_abs_2512_12751/figures/017_Figure_10.jpg]]
*Figure 10: Effect of End-to-End Training on the Comparison Methods. We visualize the impact of end-to-end (E2E) training on the comparison methods DOME [17] and I2-World [32] by presenting the ground truth along with their predictions before and after E2E training. For DOME, the forecasting capability completely breaks down after E2E training. For I2-World, E2E training fails to produce more accurate forecasts and further leads to noticeable loss of scene details*

**互控制注意力（MCA）的长时预测贡献。** 移除MCA后，3s处的预测mIoU从35.83降至30.48，降幅显著大于短时域，证明MCA对长时域控制-场景交互建模的关键作用。

### 消融实验：视频生成模块

Table 5和Figure 5(b)展示了视频生成模块的消融结果。移除归一化策略后，FVD从98.06急剧升至212.67，并出现明显的网格伪影（grid artifacts）和模糊输出，表明归一化对稳定微调预训练视频扩散模型至关重要。移除多视角注意力（MVA）则导致多视角生成不一致——同一车辆在不同视角下外观差异明显，验证了MVA对跨视角关系建模的必要性。

### 失败模式与局限性

GenieDrive的主要失败模式源于端到端训练带来的重建质量下降（Table 6）。当VAE的重建能力过度牺牲时，占用预测的物理精度可能受到潜在表示信息瓶颈的限制。此外，MVA模块中的超参数$\eta$控制多视角注意力的强度，其最优值可能依赖于具体场景和视角配置，需要针对不同部署条件进行调参。当前实验均在NuScenes数据集上进行，对极端天气、复杂路口等长尾场景的泛化能力尚需进一步验证。

![[assets/figures/papers/paper_list_l2502_https_arxiv_org_abs_2512_12751/figures/013_Table_6.jpg]]
*Table 6: Reconstruction and Forecasting Performance Change in End-to-End Training. ‘R’ denotes reconstruction and ‘F’ denotes forecasting. As the number of training epochs increases, forecasting performance gradually improves, whereas reconstruction performance decreases*

### 补充图表

![[assets/figures/papers/paper_list_l2502_https_arxiv_org_abs_2512_12751/figures/003_Figure_3.jpg]]
*Figure 3: Comparison of Trajectory-Controlled Driving Video Generation. Our method can generate physics-aware future frames for the trajectories Turn Left, Go Straight, and Turn Right. In contrast, Vista [16] and Epona [67] struggle with Turn Left and Turn Right*

![[assets/figures/papers/paper_list_l2502_https_arxiv_org_abs_2512_12751/figures/005_Table_1.jpg]]
*Table 1: Performance of 4D Occupancy forecasting. We compare our method with the most competitive methods on reconstruction, forecasting accuracy, inference speed and parameter count respectively. Our method achieves superior performance across all metrics*

![[assets/figures/papers/paper_list_l2502_https_arxiv_org_abs_2512_12751/figures/007_Table_3.jpg]]
*Table 3: Ablation on end-to-end training, model design and representation. We also apply E2E training on other comparative methods to demonstrate not all methods benefit from E2E. ‘CR’ represents continuous representation*

![[assets/figures/papers/paper_list_l2502_https_arxiv_org_abs_2512_12751/figures/008_Figure_5.jpg]]
*Figure 5: (a) Comparison with UniScene [30]. Our method generates longer driving videos while maintaining high quality. (b) Ablation Study. Removing normalization during fine-tuning results in noticeable grid artifacts and blurry outputs, while removing the MVA leads to multi-view inconsistent generation. (c) Driving Scenario Editing. With our two-stage generation method, edits such as removal or insertion can be easily applied to the occupancy, allowing for the generation of edited driving videos*

![[assets/figures/papers/paper_list_l2502_https_arxiv_org_abs_2512_12751/figures/009_Table_4.jpg]]
*Table 4: Quantitative Comparison of Multi-view Driving Video Generation. Our GenieDrive achieves outstanding performance across various generation lengths and metrics. Vista∗ is a multiview invariant proposed in [30]*

![[assets/figures/papers/paper_list_l2502_https_arxiv_org_abs_2512_12751/figures/010_Table_5.jpg]]
*Table 5: Ablation Study on Video Generation. We removed the Multi-View Attention and normalization modules separately and re-ran the fine-tuning. Omitting these modules degraded video generation quality, especially without the normalization module*

## 方法谱系与知识库定位

### 1. 核心瓶颈与突破路径

现有视频驾驶世界模型（如 **Vista**、**Epona** (Zhang et al., ICCV 2025)）普遍采用单阶段黑盒扩散模型，将驾驶控制信号直接映射为视频帧。这种端到端生成范式缺乏显式的物理建模与约束，导致两个关键缺陷：
- **物理不一致性**：模型对转弯等控制指令产生违背物理规律的预测，**Vista** 和 **Epona** 在左/右转轨迹下无法正确响应（Figure 3）。
- **分布偏差敏感**：生成结果高度依赖训练数据分布，难以泛化到训练分布之外的控制序列。

GenieDrive 的核心突破在于**引入4D占用作为中间物理表示**，将任务分解为“占用预测→视频渲染”两阶段框架。这一设计将控制对场景演化的影响显式建模在占用空间中，为视频生成提供物理先验，从根本上克服黑盒模型的物理偏差。

### 2. 方法谱系定位

#### 2.1 与4D占用预测方法的对比

| 维度 | **OccWorld** (Zheng et al., ECCV 2024) | **I2-World** | **GenieDrive（本方法）** |
|------|------|------|------|
| 表示压缩 | 离散表示（VQ） | 未明确 | 连续三平面VAE，潜在尺寸仅为前人的58% |
| 控制建模 | 基础条件注入 | 基础条件注入 | 互控制注意力（MCA） + 中间变换监督 |
| 训练策略 | 两阶段分离训练 | 两阶段分离训练 | 端到端联合训练VAE与预测模块 |
| 参数量 | — | 22.71M | **3.47M** |
| 推理速度 | — | 37.04 FPS | **41.38 FPS** |
| 预测mIoU | — | 39.73% | **42.59%**（+7.2%） |

**关键差异**：GenieDrive 的端到端训练策略使其在参数大幅减少的同时实现性能反超。消融实验（Table 3）揭示了一个重要发现：**端到端训练并非普适有效**——对 **DOME** 施加端到端训练导致预测完全崩溃（mIoU 从27.10降至0.43），**I2-World** 端到端训练后性能同样下降（Figure 10）。GenieDrive 的连续三平面表示是端到端训练成功的关键前提，使用离散表示（VQ）的变体在端到端训练后性能反而下降。

#### 2.2 与视频驾驶世界模型的对比

| 维度 | **Vista** / **Epona** | **UniScene** | **MagicDrive-V2** | **GenieDrive（本方法）** |
|------|------|------|------|------|
| 生成范式 | 单阶段黑盒扩散 | 占用引导 | 多视角生成 | 两阶段物理感知生成 |
| 物理建模 | 无 | 部分 | 无 | 4D占用中间表示 + 占用投射 |
| 多视角一致性 | 单视角 | 多视角 | 多视角 | 归一化多视角注意力（MVA） |
| 控制响应 | 转弯指令失效 | — | — | 物理合理的转弯生成 |
| FVD（81帧） | — | 70.52 | — | **55.93**（降低20.7%） |
| 生成长度 | 短序列 | 短序列 | — | **8倍更长序列** |

**关键差异**：GenieDrive 的归一化多视角注意力（MVA）模块通过分布对齐策略（Eq. 15）将多视角关系建模集成到预训练视频DiT中，避免直接微调导致的预训练先验崩溃。消融实验（Table 5）表明，移除归一化策略导致FVD从98.06飙升至212.67，并出现网格伪影（Figure 5b）；移除MVA则导致多视角生成不一致。

### 3. 适用边界与局限

**适用边界**：
- 依赖NuScenes Occ3D标注数据进行占用预测训练，当前验证集中在城市驾驶场景。
- 占用投射（Occupancy Splatting）生成的语义图作为视频条件，语义类别受限于占用标签的语义定义。
- 视频生成阶段基于预训练视频扩散模型微调，生成质量受基模型能力约束。

**已知局限**（需人工验证）：
- 论文未明确讨论极端天气、复杂光照条件下的占用预测鲁棒性。
- 端到端训练导致重建mIoU从86.15下降至70.07（Table 6），表明VAE的表示能力与预测任务对齐存在trade-off。
- Sim-to-Real生成（Figure 13）仅在CARLA仿真场景展示，真实场景下的域迁移能力缺乏量化评估。

### 4. 开放问题

1. **端到端训练的泛化条件**：为何连续表示使端到端训练有效而离散表示导致失败？这一现象的深层机制尚待理论解释。
2. **占用-视频解耦的极限**：当前两阶段框架中，占用预测误差会传播到视频生成阶段。是否存在更紧耦合的方式（如可微渲染）来缓解误差累积？
3. **物理约束的形式化**：当前“物理感知”通过占用中间表示隐式实现，是否可引入显式物理约束（如动力学方程）进一步提升长时预测的物理一致性？
4. **跨数据集泛化**：GenieDrive 在NuScenes上的优异表现能否迁移到Waymo、KITTI等其他自动驾驶数据集，尚待验证。

## 原文 PDF

![[paperPDFs/CVPR_2026/GenieDrive_Towards_Physics_Aware_Driving_World_Model_with_4D_Occupancy_Guided_Video_Generation.pdf]]