---
title: "CT-1: Camera Trajectory Generation for Camera-Controlled Video Generation"
type: paper
paper_level: A
venue: arXiv
year: 2026
pdf_ref: paperPDFs/arxiv_2026/CT_1_Camera_Trajectory_Generation_for_Camera_Controlled_Video_Generation.pdf
project_link: https://gulucaptain.github.io/Camera-Transformer-1/
code_link: https://github.com/gulucaptain/Camera-Transformer-1
aliases:
- C1CT1
- CT-1
tags:
- arxiv_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/image_and_video_generation
- topic/generative_models_diffusion
core_operator: 引入视觉-语言-相机（VLC）模型，结合双分支视觉编码器、LLaMA-2语言模型和带小波正则化损失的扩散Transformer，从图像和文本联合推理出相机轨迹分布。
primary_logic: 通过将视觉语义理解与扩散建模相结合，并利用小波变换将轨迹分解为低频全局运动和高频细节进行正则化，CT-1学会了从稀疏的视觉和文本线索中生成平滑、场景感知且语义对齐的相机轨迹，从而将空间推理知识迁移到视频生成中。
claims:
- CT-1在CameraBench100上的平均成功率达81.6%，相对最佳基线Wan2.2提升25.7%
- 小波分析表明低频成分主导相机运动能量，且低频重构误差极小
- WavReg损失相比速度/加速度/抖动正则化等策略在所有指标上均表现最优
- <CAM> token融合视觉和语言信息显著优于仅文本或仅视觉条件
---

# CT-1: Camera Trajectory Generation for Camera-Controlled Video Generation

> [!tip] 核心洞察
> 通过将视觉语义理解与扩散建模相结合，并利用小波变换将轨迹分解为低频全局运动和高频细节进行正则化，CT-1学会了从稀疏的视觉和文本线索中生成平滑、场景感知且语义对齐的相机轨迹，从而将空间推理知识迁移到视频生成中。

| 字段 | 内容 |
|------|------|
| 中文题名 | CT-1：面向相机可控视频生成的相机轨迹生成 |
| 英文题名 | CT-1: Camera Trajectory Generation for Camera-Controlled Video Generation |
| 会议/期刊 | arXiv 2026 |
| Links | [paper](https://arxiv.org/abs/2604.09201) · [Code](https://github.com/gulucaptain/Camera-Transformer-1) · [Project](https://gulucaptain.github.io/Camera-Transformer-1/) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/image_and_video_generation #topic/generative_models_diffusion |
| Method | CT-1 (Camera Transformer 1) |
| Dataset | CameraBench100, VBench |

> [!tip] 效果简介
> - CameraBench100 上，Success Rate (Average) 81.6 vs 64.9 (Wan2.2 w/ PE) (+16.7 (相对提升25.7%))。
> - VBench 上，Aesthetic Quality 0.585 vs 0.571 (Wan2.1 w/o PE) (+0.014)。

## 概要

现有相机可控视频生成方法面临一个核心瓶颈：**缺乏自动生成与用户意图和场景上下文一致的相机轨迹的能力**。手动指定相机参数（如平移向量、旋转矩阵）不仅耗时费力，而且要求用户具备专业知识；基于文本提示的隐式控制方式则精度不足，难以将特定的相机运动意图推广到多样化的视觉场景中。

针对这一问题，本文提出 **CT-1（Camera Transformer 1）**，一种视觉-语言-相机（Vision-Language-Camera, VLC）模型。其核心思路是：从单张参考图像和一段描述用户意图的文本出发，**联合推理出语义对齐的相机轨迹分布**，并将该轨迹作为显式控制信号输入下游视频生成模型，从而实现端到端的相机可控视频生成。CT-1 的关键设计包括：（1）双分支视觉编码器与 LLaMA-2 语言模型构成的视觉-语言模块，输出融合了场景语义与相机意图的 `<CAM>` token；（2）基于扩散 Transformer（DiT）的轨迹建模模块，以 `<CAM>` token 为条件学习 SE(3) 相机轨迹的概率分布；（3）**小波正则化损失（WavReg）**，利用 Haar 小波变换将轨迹分解为低频全局运动和高频细节，在频域施加多尺度监督，从而引导模型生成平滑、稳定的相机运动。

在实验验证方面，CT-1 在 **CameraBench100** 基准上取得了 **81.6% 的平均成功率**，相对最佳基线方法 Wan2.2 提升 **25.7%**（Table 1）。小波分析表明，相机运动的能量高度集中于低频分量，且低频重构误差极小，这为 WavReg 损失的设计提供了经验依据（Figure 3）。消融实验进一步证实，WavReg 损失在所有评估指标上均优于速度正则化、加速度正则化、抖动正则化等替代策略（Table 10），而 `<CAM>` token 的多模态融合方式也显著优于仅文本或仅视觉的条件策略（Table 11）。在视频生成质量方面，CT-1 驱动的视频在 VBench 美学质量指标上同样展现出优势（Table 2）。

在方法谱系上，CT-1 区别于 **MotionCtrl** 和 **CameraCtrl** 等依赖外部指定轨迹的相机可控视频生成模型，也不同于 **CogVideoX**、**LTX-Video**、**Wan2.1/Wan2.2** 等仅从文本隐式推断相机运动的图像到视频生成模型。CT-1 的核心贡献在于**将轨迹生成建模为一个独立的、可迁移的视觉推理任务**，使得空间推理知识可以从 VLC 模型迁移到任意下游视频生成主干中。



### 相机可控视频生成的现状与瓶颈

相机运动是视频叙事中的核心表达手段——推拉摇移、跟拍环绕等运镜方式直接决定了观众的视觉体验和叙事节奏。近年来，扩散模型在视频生成领域取得了显著进展，催生了一系列相机可控视频生成方法，如**MotionCtrl**、**CameraCtrl**等，它们允许用户通过显式指定相机参数（如平移向量、旋转矩阵）来操控生成视频的视角运动。然而，这些方法面临一个根本性瓶颈：**相机轨迹的获取本身就是一个未解决的难题**。

现有的相机轨迹指定方式主要分为两类：

1. **手动参数指定**：用户直接输入SE(3)空间中的相机位姿序列，这要求用户具备专业的3D视觉知识，且对复杂场景的轨迹设计极为耗时费力。
2. **文本提示隐式控制**：通过自然语言描述运镜意图（如“镜头向右平移”），让视频生成模型自行推断相机运动。这种方式虽然降低了使用门槛，但控制精度严重不足——文本对空间运动的表达能力有限，难以精确指定运动幅度、速度和轨迹形状，且在不同场景间的泛化性差。

这两种方式的共同缺陷在于：**缺乏一个能够自动将用户意图和场景上下文转化为精确相机轨迹的中间模块**。用户要么在专业性和效率之间做取舍，要么在易用性和精度之间妥协。

### 核心科学问题

上述困境指向一个关键的科学问题：**如何从稀疏的视觉和语言线索中，自动推理出与场景语义一致、运动平滑且符合用户意图的相机轨迹分布？**

这个问题的挑战性体现在三个层面：

- **非唯一性**：同一段文字描述（如“镜头缓缓推近主体”）在同一张图像上可以对应多种合理的相机轨迹，模型需要学习一个分布而非单点映射。
- **场景感知**：相机运动必须与图像内容深度耦合——例如，“跟随汽车”的轨迹在高速公路和越野山路场景下应有本质不同。
- **时序平滑性**：生成的轨迹需要在时间维度上保持物理合理性，避免抖动和突变，同时保留必要的细节运动。

### 本文动机与核心思路

针对上述瓶颈，本文提出**CT-1（Camera Transformer 1）**，一个视觉-语言-相机（Vision-Language-Camera, VLC）模型。其核心动机是：**将相机轨迹生成建模为一个条件分布学习问题**，利用视觉-语言模型的空间语义理解能力，结合扩散模型的分布建模优势，从单张参考图像和文本运镜描述中自动生成平滑、场景感知的相机轨迹。

CT-1的设计围绕三个关键洞察展开：

1. **语义-空间桥接**：通过双分支视觉编码器和LLaMA-2语言模型，将图像的空间布局信息与文本的运镜意图融合为统一的相机上下文表征（`<CAM>` token），为扩散模型提供丰富的条件信号。
2. **扩散分布建模**：采用扩散Transformer（DiT）对轨迹的SE(3)分布进行建模，天然适配轨迹的非唯一性，避免了确定性回归的模态坍塌问题。
3. **频域正则化**：引入基于小波变换的正则化损失（WavReg），将轨迹分解为低频全局运动和高频细节，通过加权监督强调低频成分的主导地位，从而在保持轨迹平滑性的同时不丢失必要的细节变化。

通过这一设计，CT-1将空间推理知识迁移到视频生成流程中，使得下游的相机可控视频生成模型（如CameraCtrl、MotionCtrl）能够获得高质量、场景感知的相机轨迹，最终实现从“图像+文本”到“可控视频”的端到端生成。



## 核心方法与创新机理

CT-1的核心创新在于将相机轨迹生成从“手动指定参数”或“隐式依赖文本提示”的范式，转变为**从图像-文本对自动推理SE(3)轨迹分布**的生成式建模问题。具体而言，CT-1在以下三个关键维度上实现了突破：

### 1. 相机控制信号来源的范式转变

现有相机可控视频生成方法（如MotionCtrl、CameraCtrl）通常要求用户手动指定相机参数（如平移向量、旋转角度），或通过文本提示间接控制视频扩散模型（如Wan2.2、CogVideoX）。前者费时费力且不直观，后者控制精度不足，难以推广到多样化场景。

CT-1引入**视觉-语言-相机（VLC）模型**，直接从参考图像和描述用户意图的文本指令中自动生成相机轨迹作为控制信号。这一转变使得用户可以用自然语言表达拍摄意图（如“向左平移以展示整个房间”），模型则负责将语义理解转化为精确的SE(3)轨迹，从而打通了从语义到空间控制的自动化通道（见Figure 2(a)(b), Section 3.1）。

### 2. 轨迹建模方式的升级：扩散Transformer + 小波正则化

基线方法缺乏显式的轨迹分布模型——文本提示方法隐式依赖语言模型的先验，而轨迹输入方法通常采用简单的确定性回归。CT-1则采用**扩散Transformer（DiT）**来显式建模相机轨迹的条件分布 $p_{\theta}(K_{1:T} \mid v, \ell)$，使得模型能够生成多样但合理的轨迹样本。

更进一步，CT-1提出了**小波正则化损失（WavReg）**，将预测轨迹与真实轨迹在多级小波域进行加权L1监督：

$$\mathcal{L}_{\mathrm{wav}} = \lambda_a \| a_L(\hat{\mathbf{K}}) - a_L(\mathbf{K}) \|_1 + \sum_{l=1}^{L} \lambda_{d_l} \| d_l(\hat{\mathbf{K}}) - d_l(\mathbf{K}) \|_1$$

其中权重满足 $\lambda_a > \lambda_{d_L} > \dots > \lambda_{d_1}$，即对低频全局运动施加更强的监督约束。这一设计的动机源于小波分析揭示的关键发现：**相机轨迹的能量主要集中在低频分量**（Figure 3），低频成分主导了整体运动趋势，而高频细节则对应抖动等不稳定因素。WavReg通过在频域解耦全局运动与局部抖动，使模型学会生成平滑且场景感知的轨迹。消融实验（Table 10）证实，WavReg在所有指标上均优于速度正则化、加速度正则化、抖动正则化及低通滤波等替代策略。

### 3. 空间推理机制：<CAM> token的信息融合

基线方法通常将视觉特征和文本特征简单拼接或池化后送入生成模型，缺乏专用的相机上下文表示。CT-1设计了专用的 **<CAM> token**，在视觉语言模块中融合双分支视觉编码器提取的场景感知特征与LLaMA-2语言模型编码的用户意图，形成富含空间推理信息的相机上下文表征，再作为条件注入扩散Transformer。消融实验（Table 11）表明，<CAM> token的融合策略显著优于仅文本条件、仅视觉条件以及池化条件，验证了联合视觉-语言空间推理对于轨迹生成的关键作用。



CT-1 的整体 pipeline 围绕“视觉-语言-相机（VLC）”这一核心范式构建，目标是从单张参考图像和一段描述用户意图的文本指令出发，自动生成与场景语义对齐的 SE(3) 相机轨迹，并将该轨迹作为控制信号馈入下游相机可控视频生成模型，实现端到端的图像-文本到视频生成。整个框架由三个关键模块串联构成，如图 Figure 2 所示。

![[assets/figures/papers/paper_list_l15_https_arxiv_org_abs_2604_09201/figures/003_Figure_2.jpg]]
*Figure 2: Overview of the proposed camera-controllable video generation framework based on the CT-1 model, which includes (a) a vision–language module for semantic embedding, (b) a Diffusion Transformer module for modeling camera trajectory distributions, and (c) controllable generation models that synthesize videos conditioned on the trajectories*

### 输入与输出流

系统的输入是一对 $(v, \ell)$，其中 $v$ 为初始视觉观测（单张参考图像），$\ell$ 为描述期望相机运动的文本指令。输出为一条时长为 $T$ 的相机轨迹 $\mathrm{K}_{1:T} = \{\mathrm{K}_t\}_{t=1}^T$，每个 $\mathrm{K}_t \in SE(3)$ 由旋转矩阵和平移向量参数化。该轨迹随后被注入下游视频扩散模型，生成相机运动可控的视频序列。

### 模块关系与数据流

**模块一：Vision-Language Module（视觉-语言模块）。** 该模块采用双分支视觉编码器提取图像的多尺度视觉特征，并与 LLaMA-2 语言模型处理后的文本指令进行融合，输出一个紧凑的 camera-context token `<CAM>`。此 token 编码了场景语义、空间布局和用户意图之间的联合信息，是连接视觉理解与轨迹生成的信息瓶颈。

**模块二：Camera Transformer（扩散 Transformer）。** `<CAM>` token 作为条件信号注入基于 Diffusion Transformer（DiT）的扩散模型。该模型在轨迹空间上执行去噪扩散过程：前向过程逐步向真实轨迹添加高斯噪声，反向过程则从噪声中恢复出符合条件分布的轨迹。去噪网络以 `<CAM>` token 和扩散时间步为条件，预测出干净的轨迹 $\hat{\mathrm{K}}_{1:T}$。

**模块三：Wavelet-based Regularization Loss（小波正则化损失，WavReg）。** 在训练阶段，预测轨迹 $\hat{\mathrm{K}}$ 与真实轨迹 $\mathrm{K}$ 分别经过多级 Haar 离散小波变换，分解为低频近似系数 $a_L$ 和高频细节系数 $d_l$。WavReg 损失对这些小波系数施加加权 L1 监督，权重遵循 $\lambda_a > \lambda_{d_L} > \dots > \lambda_{d_1}$ 的递减次序，强制模型优先学习占主导能量的低频全局运动，同时抑制高频抖动。最终训练目标为扩散损失与 WavReg 损失的加权组合：$\mathcal{L} = \mathcal{L}_{\mathrm{diff}} + \beta \mathcal{L}_{\mathrm{wav}}$。

**下游集成。** 推理时，CT-1 预测的轨迹直接作为即插即用的控制信号，驱动 CameraCtrl、MotionCtrl 等相机可控视频生成模型，无需对下游模型进行任何微调。整个推理过程中，CT-1 的轨迹估计阶段仅占总时间开销的约 5.3%，保持了高效的端到端生成效率。

### 补充图表

![[assets/figures/papers/paper_list_l15_https_arxiv_org_abs_2604_09201/figures/002_Figure_1.jpg]]
*Figure 1: A high-level overview of CT-1’s architecture, its integration with the video generation model, and comparisons*

![[assets/figures/papers/paper_list_l15_https_arxiv_org_abs_2604_09201/figures/014_Figure_6.jpg]]
*Figure 6: Visualization of camera trajectories estimated by CT-1. The red (X), green (Y), and blue (Z) axes indicate the camera’s local coordinate system [25]: the red axis denotes the right–left direction, the green axis represents the vertical direction (down or up), and the blue axis corresponds to the viewing direction (forward or backward, i.e., zoom-in or zoom-out)*



CT-1 的核心架构由三个紧密协作的模块构成：**视觉-语言模块（Vision-Language Module）**、**相机Transformer（Camera Transformer / DiT）** 和**小波正则化损失（WavReg）**。以下逐一展开其设计逻辑与关键公式。

### 视觉-语言模块：<CAM> token 的生成

该模块负责从场景图像和用户文本指令中提取相机感知的语义信息。其输入为一帧参考图像 $v$ 和一段描述相机运动意图的文本 $\ell$，输出为一个紧凑的相机上下文 token `<CAM>`。具体而言，模块采用双分支视觉编码器（分别捕获全局场景布局和局部细节）与 LLaMA-2 语言模型进行跨模态融合，最终将视觉和语言信息压缩到 `<CAM>` token 中。该 token 随后作为条件信号注入下游的扩散Transformer。

**关键公式：** 问题形式化为学习轨迹的条件分布

$$p_{\theta}(K_{1:T} \mid v, \ell)$$

其中 $K_{1:T} = \{K_t\}_{t=1}^T$ 表示长度为 $T$ 的相机轨迹序列，每个 $K_t \in SE(3)$ 由旋转矩阵 $R_t \in SO(3)$ 和平移向量 $\mathbf{p}_t \in \mathbb{R}^3$ 参数化。

**设计依据：** `<CAM>` token 融合策略的消融实验（Table 11）表明，同时融合视觉和语言信息显著优于仅使用文本条件、仅使用视觉条件或池化条件，验证了跨模态融合对相机轨迹推理的必要性。

### 相机Transformer：扩散建模轨迹分布

轨迹生成采用基于扩散Transformer（DiT）的扩散模型，以 `<CAM>` token 为条件，从随机噪声逐步去噪生成 SE(3) 轨迹。前向扩散过程向真实轨迹 $\mathrm{K}$ 逐步注入高斯噪声：

$$\mathrm{K}^{(s)} = \sqrt{\bar{\alpha}_s} \mathrm{K} + \sqrt{1 - \bar{\alpha}_s} \epsilon, \quad \epsilon \sim \mathcal{N}(0,I)$$

其中 $s$ 为扩散步数，$\bar{\alpha}_s$ 为累积噪声调度参数。反向去噪过程由 DiT 网络 $\epsilon_\theta$ 预测添加的噪声，通过标准扩散损失 $\mathcal{L}_{\mathrm{diff}}$ 进行监督。

### 小波正则化损失：频域多尺度约束

CT-1 的关键创新在于引入**小波正则化损失（WavReg）**，在频域对预测轨迹进行多尺度监督。其动机来自对相机轨迹的小波分析（Figure 3）：低频成分主导运动能量，且低频重构即可保留大部分几何信息，而高频成分主要贡献抖动。因此，WavReg 对低频近似系数施加更大权重，引导模型优先学习平滑的全局运动。

对预测轨迹 $\hat{\mathbf{K}}$ 进行 Haar 离散小波变换（DWT），一级分解为：

$$a_l^{(1)} = \frac{\hat{\mathbf{K}}[2l-1,:] + \hat{\mathbf{K}}[2l,:]}{\sqrt{2}}, \quad d_l^{(1)} = \frac{\hat{\mathbf{K}}[2l-1,:] - \hat{\mathbf{K}}[2l,:]}{\sqrt{2}}$$

其中 $a_l^{(1)}$ 为低频近似系数，$d_l^{(1)}$ 为高频细节系数。多级分解后，WavReg 损失定义为预测轨迹与真实轨迹在小波域各尺度的加权 L1 距离：

$$\mathcal{L}_{\mathrm{wav}} = \lambda_a \| a_L(\hat{\mathbf{K}}) - a_L(\mathbf{K}) \|_1 + \sum_{l=1}^{L} \lambda_{d_l} \| d_l(\hat{\mathbf{K}}) - d_l(\mathbf{K}) \|_1$$

权重满足 $\lambda_a > \lambda_{d_L} > \dots > \lambda_{d_1}$，即低频分量获得更大的监督权重。完整训练目标为扩散损失与小波正则化损失的加权组合：

$$\mathcal{L} = \mathcal{L}_{\mathrm{diff}} + \beta \mathcal{L}_{\mathrm{wav}}$$

其中 $\beta$ 控制正则化强度，实验表明 $\beta=0.1$ 达到最优效果（Table 4）。

**消融验证：** Table 10 系统比较了 WavReg 与速度正则化、加速度正则化、抖动正则化、低通滤波等替代策略，WavReg 在所有指标上均表现最优，证实了频域多尺度约束对轨迹平滑性和准确性的关键作用。

### 下游集成：相机可控视频生成

CT-1 预测的 SE(3) 轨迹可直接驱动现有的相机可控视频生成模型（如 CameraCtrl、MotionCtrl），替换其原本需要手动指定的相机参数。推理时，CT-1 从图像-文本对自动生成轨迹，下游视频扩散模型据此合成符合用户意图的相机运动视频，形成端到端的图像-文本-视频生成管线。

### 补充图表

![[assets/figures/papers/paper_list_l15_https_arxiv_org_abs_2604_09201/figures/019_Figure_11.jpg]]
*Figure 11: Qualitative results of applying the trajectories results of the CT-1 on CameraCtrl [9] model, which is a camera-controllable video generation model. The tested scenes are from the RealEstate10K dataset [44]*

![[assets/figures/papers/paper_list_l15_https_arxiv_org_abs_2604_09201/figures/020_Figure_12.jpg]]
*Figure 12: Qualitative results of applying the trajectories results of the CT-1 on MotionCtrl [32] model, which is a camera-controllable video generation model. The tested scenes are from the MultiCamVideo dataset [1]*



## 实验与关键发现

### 核心实验设置

为全面评估CT-1的性能，作者构建了**CameraBench100**基准，涵盖六类典型相机运动任务（如平移、缩放、旋转等），并以**Success Rate**作为主要评价指标。Success Rate由两位专家独立评判，确保一致性。对于基于文本提示的基线方法，引入**Prompt Extension (PE)**策略进行公平比较：将相机运动描述显式附加到生成提示中。CT-1属于无PE的提示输入设置，直接从图像-文本对生成视频。轨迹输入基线则使用外部轨迹估计器，并非完全端到端的图像-文本-视频生成。

### 主实验结果

**相机控制精度。** 在CameraBench100上，CT-1取得了**81.6%的平均Success Rate**，显著优于所有基线方法（Table 1）。具体而言，相比最强的提示输入基线Wan2.2（w/ PE）的64.9%，CT-1绝对提升**16.7个百分点**，相对提升**25.7%**。与基于轨迹输入的VLM方法相比，CT-1的平均成功率相对提升达**171.1%**，表明从稀疏图像-文本对中学习轨迹分布的策略远优于直接回归或文本隐式控制。

**视频生成质量。** 在VBench基准上，CT-1驱动的视频在**Aesthetic Quality**指标上达到0.585，优于Wan2.1（w/o PE）的0.571（Table 2）。这验证了CT-1生成的轨迹不仅控制精确，同时保持了视频的视觉美学质量。

### 消融实验

**模型规模扩展。** Table 3显示，CT-1从Base→Large→Huge规模持续提升相机控制成功率和视频生成质量，表明模型容量是性能的关键驱动因素，且未观察到饱和迹象。

**WavReg损失的有效性。** Table 10对比了多种轨迹正则化策略：速度正则化、加速度正则化、抖动正则化及低通滤波。**WavReg在所有指标上均表现最优**，验证了小波域多尺度监督的独特优势。Table 4进一步表明，当权重系数β=0.1时WavReg达到最佳效果，过大的β（如1.0）反而损害性能，说明需要适度平衡扩散损失与频域正则化。

**<CAM> token融合机制。** Table 11消融了相机上下文token的设计：仅文本条件、仅视觉条件、池化融合与<CAM> token融合。**<CAM> token融合视觉和语言信息显著优于所有替代方案**，证明专用token能更有效地编码相机感知语义，为扩散模型提供高质量条件信号。

**数据组成的影响。** Table 6显示，加入推理场景数据（CT-200K中的RS子集）显著提升了复杂运动建模能力，特别是在需要空间推理的任务上。这验证了CT-200K数据管道的价值。

**泛化稳定性。** Table 5表明，无论是固定图像切换提示（Image → Prompts）还是固定提示切换图像（Prompt → Images），CT-1均能保持稳定的轨迹生成性能，证明模型学习到了解耦的场景理解和运动推理能力。

**推理效率。** Table 7显示，CT-1的轨迹推理阶段仅占总时间的约**5.3%**，额外开销极小，适合作为即插即用的前端模块。

### 小波分析支撑

Figure 3对1000条轨迹的小波分析揭示了**低频成分主导相机运动能量**，且仅用低频重构即可保留轨迹的几何结构，而高频成分主要对应抖动噪声。这一发现为WavReg的设计提供了坚实的频域依据：通过加权L1损失强调低频保真度、适度抑制高频抖动，实现了平滑性与轨迹偏差之间的最优权衡（Figure 16进一步在单场景内展示了角速度、线速度、加速度能量与高频D1能量的分布）。

### 失败模式与局限性

1. **时间分辨率受限。** 由于下游视频扩散模型采用固定的4×时间压缩，CT-1只能为49帧视频预测13步轨迹，限制了轨迹的时间分辨率，可能不适用于需要高帧率相机控制的场景（如快速摇镜或剧烈运动）。
2. **评估主观性。** Success Rate依赖人工专家主观判断，在大规模基准上的可重复性和扩展性受限。Table 9的统计稳定性分析表明跨测试集的性能波动较小，但自动化指标的缺失仍是瓶颈。
3. **单帧输入的局限。** CT-1主要从单张参考图像生成轨迹，未显式利用多帧历史信息或深度先验。在高度动态、遮挡严重或需要长程时序建模的场景中，轨迹预测的鲁棒性可能下降。
4. **模型集成依赖。** CT-1的性能部分受限于下游视频生成模型（如CameraCtrl、MotionCtrl）的能力边界。Figure 11和Figure 12展示了CT-1与不同下游模型的集成效果，但跨模型的泛化性仍需进一步验证。

### 重要图表结论速览

- **Table 1:** CT-1在CameraBench100上平均Success Rate 81.6%，相对Wan2.2提升25.7%。
- **Table 10:** WavReg损失在所有正则化策略中表现最优，验证了小波域监督的核心作用。
- **Table 11:** <CAM> token融合视觉-语言信息是性能的关键，显著优于仅文本或仅视觉条件。
- **Table 3:** 模型规模扩展持续提升性能，未饱和。
- **Table 7:** CT-1推理开销仅占总时间的5.3%，高效实用。
- **Figure 3:** 低频成分主导相机运动能量，为WavReg设计提供频域依据。

![[assets/figures/papers/paper_list_l15_https_arxiv_org_abs_2604_09201/figures/006_Table_1.jpg]]
*Table 1: Zero-shot quantitative results on CameraBench100 for camera trajectory estimation across six typical tasks using the Success Rate metric. PE denotes Prompt Extension for fair comparison, and AR denotes autoregressive trajectory generation*

![[assets/figures/papers/paper_list_l15_https_arxiv_org_abs_2604_09201/figures/009_Table_3.jpg]]
*Table 3: Ablation of camera control and video generation performance across different CT-1 scales*

![[assets/figures/papers/paper_list_l15_https_arxiv_org_abs_2604_09201/figures/026_Table_10.jpg]]
*Table 10: Comparison of different trajectory regularization strategies. The second-best results are underlined*

![[assets/figures/papers/paper_list_l15_https_arxiv_org_abs_2604_09201/figures/027_Table_11.jpg]]
*Table 11: Comparison of different camera-context token strategies. The second-best results are underlined*

![[assets/figures/papers/paper_list_l15_https_arxiv_org_abs_2604_09201/figures/013_Table_7.jpg]]
*Table 7: Comparison of the time and memory costs of the CT-1 estimation stage and the video generation stage*

### 补充图表

![[assets/figures/papers/paper_list_l15_https_arxiv_org_abs_2604_09201/figures/007_Table_2.jpg]]
*Table 2: Comparison of generated video quality with baseline methods using VBench. Results w/o PE are in gray*

![[assets/figures/papers/paper_list_l15_https_arxiv_org_abs_2604_09201/figures/010_Table_4.jpg]]
*Table 4: Impact of the WavReg loss and the parameter*



## 定位与知识库关联

### 1. 问题定位与核心瓶颈

在相机可控视频生成领域，现有方法面临一个根本性瓶颈：**缺乏自动生成与用户意图和场景上下文一致的相机轨迹的能力**。当前主流方案分为两类——手动指定相机参数（如旋转矩阵和位移向量）费时费力且需要专业知识，而基于文本提示直接驱动视频生成模型的方法（如**MotionCtrl**、**CameraCtrl**）虽然降低了使用门槛，却存在控制不精确、难以推广到多样化场景的问题。这些方法本质上将相机控制的推理责任转嫁给了视频生成模型或用户，而非在生成前显式建模轨迹分布。

CT-1的核心洞察在于：**将视觉语义理解与扩散建模相结合，并利用小波变换将轨迹分解为低频全局运动和高频细节进行正则化**，使模型学会从稀疏的视觉和文本线索中生成平滑、场景感知且语义对齐的相机轨迹，从而将空间推理知识迁移到视频生成中。

### 2. 方法谱系中的定位

#### 2.1 与现有相机可控视频生成方法的关系

CT-1在方法谱系中占据了一个独特的位置——它不是一个视频生成模型，而是一个**相机轨迹生成器**，可灵活集成到下游任意相机可控视频生成模型中。这一设计使其与现有方法形成互补而非替代关系：

- **MotionCtrl** 和 **CameraCtrl**：这两类方法直接接收相机参数作为控制信号生成视频，但相机参数需要外部提供。CT-1恰好填补了这一空缺——为它们自动生成场景感知的轨迹。论文实验证实，CT-1预测的轨迹可直接驱动CameraCtrl（Figure 11）和MotionCtrl（Figure 12），在RealEstate10K和MultiCamVideo数据集上均产生合理结果。
- **Wan2.1、Wan2.2、CogVideoX、LTX-Video**：这些图像到视频生成模型主要依赖文本提示隐式控制相机运动。在CameraBench100上，即使采用Prompt Extension（PE）公平比较，最佳基线Wan2.2的平均成功率也仅为64.9%，而CT-1达到81.6%，相对提升25.7%（Table 1）。这揭示了纯文本控制的根本局限——语言描述难以精确约束SE(3)空间中的连续轨迹。

#### 2.2 技术路线的创新维度

CT-1在三个关键维度上区别于现有工作：

| 维度 | 基线方法 | CT-1 |
|------|----------|------|
| **相机控制信号来源** | 文本提示直接控制视频生成模型，或手动指定相机参数 | 从图像-文本对自动生成SE(3)相机轨迹作为控制信号 |
| **轨迹建模方式** | 无显式轨迹模型（隐式依赖文本），或简单的确定性回归 | 扩散Transformer结合小波正则化损失学习轨迹分布 |
| **空间推理机制** | 无专用相机上下文token | `<CAM>` token在视觉语言模块中融合信息，作为扩散条件 |

其中，**小波正则化损失（WavReg）** 的设计源于对相机轨迹频域特性的深入分析：Figure 3显示低频成分主导相机运动能量，且仅用低频重构即可保留大部分几何信息。基于此，WavReg对低频近似系数和高频细节系数施加加权L1监督（Eq. 6），权重满足 $\lambda_a > \lambda_{d_L} > \dots > \lambda_{d_1}$，优先保证全局运动的准确性。消融实验（Table 10）证实，WavReg相比速度正则化、加速度正则化、抖动正则化及低通滤波等策略在所有指标上均表现最优。

### 3. 适用边界与局限

#### 3.1 时间分辨率约束

CT-1的一个结构性局限源于下游视频扩散模型的架构限制。由于主流视频生成模型（如文中使用的CameraNoise）采用固定的 $4\times$ 时间压缩，CT-1只能为49帧视频预测13步轨迹。这意味着**轨迹的时间分辨率受限于视频生成主干的压缩比**，可能不适用于需要高帧率精细相机控制的场景（如快速摇镜或震动效果）。

#### 3.2 评估体系的可扩展性

当前主要评估指标Success Rate依赖人工专家主观判断，由两位专家独立评判以确保一致性。虽然这保证了评估质量，但在大规模基准上的可重复性和扩展性受限。论文也承认这一点，并在Table 9中进行了统计稳定性分析，比较了CT-1和Wan2.2在不同测试集上的表现，但客观自动化指标的缺失仍是该领域面临的共同挑战。

#### 3.3 输入模态的固有限制

CT-1主要从**单张参考图像**生成轨迹，未显式利用多帧历史信息或深度先验。这一设计简化了模型架构和训练流程，但在复杂动态场景中可能影响鲁棒性——例如，当单张图像无法充分暗示场景的三维结构时，模型需要依赖从训练数据中学到的先验进行推断，而非基于显式的几何推理。

### 4. 开放问题

1. **长序列与多镜头扩展**：CT-1能否扩展到处理极长轨迹或多镜头序列？当前的自回归轨迹生成（AR）模式已在Table 1中进行了初步探索，但其在更长时序上的误差累积效应尚不明确。

2. **频域正则化的替代方案**：WavReg损失是否可与其他频率域方法（如傅里叶正则化）结合或替代？小波变换的优势在于多尺度分解，但傅里叶方法在全局频谱建模上可能具有互补优势。

3. **模型规模扩展的边际收益**：Table 3显示CT-1从Base到Large再到Huge持续提升性能，但模型在更大规模（>458M参数）下是否继续提升并保持高效推理（当前推理开销仅占总时间的约5.3%，Table 7）仍是一个开放问题。

4. **高度动态场景的泛化**：在更真实、高度动态的驾驶场景中（如DrivingDoJo数据集，Figure 14），CT-1的性能上限和失败模式需要更系统的研究。

5. **与不同视频生成主干的集成灵活性**：当前实验主要验证了与CameraNoise、CameraCtrl和MotionCtrl的集成，是否可以将CT-1与基于U-Net架构的视频生成模型或其他扩散主干灵活集成，仍有待探索。



## 原文 PDF

![[paperPDFs/arxiv_2026/CT_1_Camera_Trajectory_Generation_for_Camera_Controlled_Video_Generation.pdf]]
