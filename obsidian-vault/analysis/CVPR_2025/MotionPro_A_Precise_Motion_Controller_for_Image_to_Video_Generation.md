---
title: "MotionPro: A Precise Motion Controller for Image-to-Video Generation"
type: paper
paper_level: A
venue: CVPR
year: 2025
pdf_ref: paperPDFs/CVPR_2025/MotionPro_A_Precise_Motion_Controller_for_Image_to_Video_Generation.pdf
aliases:
- MotionPro
tags:
- CVPR_2025
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/robotics
core_operator: "区域级轨迹（region-wise trajectory）与运动掩码（motion mask）的联合利用，通过局部精确采样与全局运动区域标识实现互补控制。"
primary_logic: "在光流映射的局部区域内直接采样轨迹，避免高斯模糊，可保留精细运动细节；同时从光流推导运动掩码以显式指定运动类别（物体/相机），从而消除歧义并增强运动控制的精确性和自然度。"
claims:
- "MotionPro采用区域级轨迹和运动掩码作为互补控制信号，取代高斯滤波轨迹。"
- "区域级轨迹直接从光流图的多个局部区域采样，保留精确运动细节。"
- "运动掩码通过光流平均幅度的阈值化生成，用于强调整体运动区域并指定运动类别。"
- "自适应特征调制利用从轨迹和掩码预测的尺度与偏置参数，调制3D-UNet中的视频潜码特征。"
---

# MotionPro: A Precise Motion Controller for Image-to-Video Generation

> [!tip] 核心洞察
> 在光流映射的局部区域内直接采样轨迹，避免高斯模糊，可保留精细运动细节；同时从光流推导运动掩码以显式指定运动类别（物体/相机），从而消除歧义并增强运动控制的精确性和自然度。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | MotionPro: 一种用于图像到视频生成的精确运动控制器 |
| 英文题名 | MotionPro: A Precise Motion Controller for Image-to-Video Generation |
| 会议/期刊 | CVPR 2025 |
| Links | [paper](https://arxiv.org/abs/2505.20287); [Project](https://zhw-zhang.github.io/MotionPro-page/) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/robotics |
| Method | MotionPro |
| Dataset | WebVid-10M, MC-Bench (object-level) |

> [!tip] 效果简介
> - WebVid-10M 上，FVD (↓) 为 59.88，对比 87.70 (MOFA-Video) / 96.65 (DragNUWA)，变化 -27.82 / -36.77。
> - WebVid-10M 上，FID (↓) 为 10.40，对比 12.18 (MOFA-Video) / 13.19 (DragNUWA)，变化 -1.78 / -2.79。
> - WebVid-10M 上，Frame Consistency (↑) 为 0.9895，对比 0.9894 (MOFA-Video) / 0.9888 (DragNUWA)，变化 +0.0001 / +0.0007。

## 概述

### 问题瓶颈

图像到视频（I2V）生成的可控运动合成面临一个核心瓶颈：现有方法（如 **DragNUWA**，Yin et al., arXiv 2023；**MOFA-Video**）普遍依赖大高斯核对稀疏点轨迹进行扩展，以生成密集运动场。这一操作虽然简单，却不可避免地模糊了运动细节，导致精细粒度控制能力不足。更关键的是，仅凭轨迹本身无法区分物体运动与相机运动——当用户拖拽背景区域时，模型容易误解为物体移动，从而产生不符合物理直觉的视频。

### 核心思路

MotionPro 通过引入一对互补的控制信号来解决上述问题：

- **区域级轨迹（region-wise trajectory）**：不再对全图光流做高斯平滑，而是在光流图的多个局部区域内直接采样轨迹。这保留了原始运动的精细细节，避免了模糊。
- **运动掩码（motion mask）**：从光流平均幅度的阈值化结果中推导出二值掩码，显式标识运动区域，从而明确运动类别（物体运动 vs. 相机运动）。

两者的联合利用形成了一个“因果旋钮”：局部精确采样保证运动细节，全局掩码消除运动歧义。此外，MotionPro 采用自适应特征调制（而非简单的通道拼接或求和）将多尺度运动特征注入预训练视频扩散模型的 3D-UNet，并通过 LoRA 低秩适配器微调所有注意力模块，在保护预训练运动先验的同时提升轨迹对齐能力。

### 方法定位

MotionPro 属于 I2V 可控生成的**运动条件注入**范式，其方法谱系可归纳如下：

| 维度 | 基线方法 | MotionPro 改进 |
|------|----------|----------------|
| 运动条件表示 | 高斯滤波点迹（DragNUWA）或稀疏到密集轨迹网络（MOFA-Video） | 区域级轨迹 + 运动掩码 |
| 运动区域指定 | 无显式机制 | 光流阈值化运动掩码 |
| 控制信号注入 | 通道拼接或特征求和 | 自适应特征调制（SPADE-like） |
| 微调策略 | 全参数微调或未明确 | LoRA 低秩适配（仅注意力模块） |

在知识库定位上，MotionPro 与 **DragAnything**（Wu et al., ECCV 2024）等基于实体表示的目标级控制方法形成互补——前者擅长细粒度运动，后者侧重目标级实体跟踪。

### 主要结果

MotionPro 在细粒度和目标级运动控制两个维度上均取得显著提升：

- **WebVid-10M 基准**：FVD 降至 59.88（相比 MOFA-Video 的 87.70 降低 27.82，相比 DragNUWA 的 96.65 降低 36.77）；FID 降至 10.40；帧一致性达到 0.9895。
- **MC-Bench 目标级控制**：MD-Img 为 10.48（DragAnything 为 12.30），MD-Vid 为 8.59（DragAnything 为 11.37）。
- **人类评估**：细粒度运动质量偏好率达 75.00%（MOFA-Video 仅 21.88%），目标级运动质量偏好率达 68.75%（DragAnything 仅 18.75%）。

消融实验进一步验证了设计的必要性：移除区域级轨迹使 FVD 升至 73.7，移除运动掩码使 FVD 升至 66.2，证明两个信号缺一不可。局部区域大小 $k=8$ 和最小掩码比例 $r_{min}=0.95$ 被确认为最优配置。

### 局限与待验证点

- 运动条件质量受限于外部光流追踪模型 DOT 在复杂场景下的精度。
- 运动掩码基于光流幅度阈值化生成，可能遗漏平滑或微小运动区域。
- 未对比更近期的视频扩散模型（如 CogVideoX），在更强基线上的提升有待验证。
- 多独立运动物体场景下的信号分工机制尚未深入探索。

## 背景与动机

图像到视频（I2V）生成旨在从单张静态参考图像出发，合成一段具有自然动态的视频。随着扩散模型在视频生成领域的快速发展，I2V的视觉质量已取得显著提升，但**精确的运动控制**仍然是一个核心瓶颈——用户不仅希望视频“动起来”，更希望视频中的运动与指定的轨迹精确对齐，同时能够区分运动的主体类别（物体运动 vs. 相机运动）。

### 现有方法的缺口：高斯滤波轨迹的模糊性

当前主流的可控I2V方法，如 **DragNUWA**（Yin et al., arXiv 2023）和 **MOFA-Video**，通常采用以下流程来实现运动控制：首先从训练视频的光流图中随机采样稀疏点轨迹，然后应用**大核高斯滤波**将这些稀疏轨迹扩展为密集控制信号。这一范式存在两个根本性缺陷：

1. **运动细节模糊**：大核高斯滤波会平滑掉轨迹中的精细运动信息，导致生成的视频在局部运动细节上与用户意图产生偏差。对于需要精确控制（如物体沿复杂曲线运动、局部形变等）的场景，这种模糊性尤为致命。

2. **运动类别歧义**：仅凭轨迹本身无法区分物体运动与相机运动。例如，一条从左到右的轨迹，可能意味着物体向右移动，也可能意味着相机向左平移。现有方法缺乏显式机制来消除这种歧义，导致生成结果中运动语义的误解。

### 本文动机：从模糊控制到精确互补控制

针对上述缺口，**MotionPro** 提出了一个核心洞察：**在光流映射的局部区域内直接采样轨迹，避免高斯模糊，可保留精细运动细节；同时从光流推导运动掩码以显式指定运动类别，从而消除歧义**。

具体而言，MotionPro 引入了两个互补的控制信号：

- **区域级轨迹（Region-wise Trajectory）**：不再对全图光流进行随机采样和高斯滤波，而是在光流图的多个局部区域内直接采样稀疏轨迹。这种“局部精确采样”策略保留了原始光流中的精细运动信息，避免了高斯核带来的模糊效应。

- **运动掩码（Motion Mask）**：基于光流幅度的时序平均值进行阈值化，生成二进制掩码，显式标识视频中发生运动的区域。该掩码从全局视角强调运动区域，帮助模型区分物体运动与相机运动——例如，当整个画面都在运动时，掩码覆盖全图，暗示相机运动；当仅局部区域有运动时，掩码仅覆盖该区域，暗示物体运动。

通过将区域级轨迹（提供局部精确的运动细节）与运动掩码（提供全局的运动区域标识）联合作为控制条件，MotionPro 实现了从“模糊控制”到“精确互补控制”的范式转变，为细粒度和目标级运动控制提供了统一的解决方案。

## 核心创新

MotionPro 的核心创新在于**以区域级轨迹（region-wise trajectory）与运动掩码（motion mask）的联合控制，替代了现有方法中依赖大高斯核扩展稀疏轨迹的范式**，从而解决了运动细节模糊和运动类别歧义两大瓶颈。这一变革体现在四个关键组件的协同设计上。

### 1. 从高斯滤波轨迹到区域级轨迹

现有可控 I2V 方法（如 **DragNUWA**，Yin et al., arXiv 2023）通常从全图光流中随机采样稀疏点迹，再通过大核高斯滤波将其扩展为稠密条件。这一策略不可避免地平滑了局部运动细节，导致精细运动（如物体微小的形变或旋转）难以被精确控制。

MotionPro 的解法是**在光流图的局部区域内直接采样轨迹，完全摒弃高斯滤波**。具体而言，方法将全局可见性掩码 $M_g$ 与各帧光流 $f^i$ 相乘得到掩码光流图 $\mathbf{\mathcal{f}}_m$，随后将其空间划分为 $k \times k$ 个局部区域，并均匀采样子集作为区域级轨迹 $\mathbf{T}_s$。由于轨迹直接取自光流映射的原始值，精细运动信息得以完整保留。消融实验（Figure 6(a)）表明，局部区域大小 $k=8$ 时 MD-Vid 和帧一致性达到最优，验证了小区域采样对运动精度的关键作用。

### 2. 从隐式运动区域到显式运动掩码

仅凭轨迹条件无法区分物体运动与相机运动——当轨迹指示画面中某区域发生位移时，模型难以判断这是物体自身移动还是相机视角变化所致。现有方法对此缺乏显式建模。

MotionPro 引入**运动掩码**作为第二路控制信号，通过光流幅度的时序平均值 $f_{avg} = \frac{1}{L} \sum_{i=1}^{L} \parallel f^i \parallel_2$ 进行阈值化（阈值为 1），生成二值掩码 $M_{mot}$，显式标识运动区域。这一掩码向模型传递了“哪些区域正在运动”的全局信息，从而消除运动类别歧义。在目标级运动控制中，运动掩码使 MotionPro 能够处理复杂轨迹（如太阳的往返运动）和反直觉轨迹（如火车倒退），而 **DragAnything**（Wu et al., ECCV 2024）等基线则需额外添加静态点来辅助区分物体与相机运动。

### 3. 从通道拼接/求和的刚性注入到自适应特征调制

**DragNUWA** 等基线将轨迹条件直接与视频潜码进行通道拼接，这要求控制信号与生成特征在空间-时间维度上严格对齐，限制了信息交换的灵活性。

MotionPro 采用**自适应特征调制（Adaptive Feature Modulation）**，通过轻量运动编码器从轨迹与掩码的拼接中学习多尺度特征，并在 3D-UNet 的各个层级预测缩放参数 $\gamma_s$ 和偏置参数 $\beta_s$，对组归一化后的视频潜码特征 $h_s$ 进行仿射变换：

$$h_s' = \text{GN}(h_s) \cdot \gamma_s + \beta_s + h_s$$

这种 SPADE-like 的调制方式无需空间-时间严格对齐，且通过快捷连接保留了原始特征信息。消融实验（Figure 8）显示，自适应特征调制在 MD-Vid 指标上显著优于特征拼接（MotionPro$^\text{C}$）和特征求和（MotionPro$^+$）。

### 4. LoRA 低秩微调保护运动先验

为在注入新控制能力的同时保护预训练视频扩散模型（SVD）已学到的丰富运动先验，MotionPro **仅在所有时空 Transformer 的注意力模块中集成 LoRA 低秩适配器**，将低秩分解矩阵 $AB^T$ 作为残差叠加到原始注意力权重上：

$$\mathcal{W}' = \mathcal{W} + \Delta\mathcal{W} = \mathcal{W} + AB^T$$

这一策略使可训练参数量远小于全参数微调，同时保证了运动-轨迹对齐的优化效率。

### 创新点的证据强度

消融实验（Section 6.4）直接验证了核心创新的因果作用：移除区域级轨迹（MotionPro$^{-traj}$）使 FVD 从 59.88 升至 73.7；移除运动掩码（MotionPro$^{-mask}$）使 FVD 升至 66.2，证明两个信号缺一不可。在 MC-Bench 上，MotionPro 的 MD-Img 和 MD-Vid 分别领先 **DragAnything** 1.82 和 2.78，人类评估中运动质量偏好率高达 75%（细粒度）和 68.75%（目标级），远超基线方法。

## 整体框架

![[assets/figures/papers/paper_list_l35_MotionPro_A_Precise_Motion_Controller_for_Image_to_Video_Generation/figures/002_Figure_2.jpg]]
*Figure 2: An overview of (a) our MotionPro for controllable I2V generation and (b) pipeline of motion condition generation. During training, MotionPro first extracts the proposed region-wise trajectory and motion mask on the input video as the control signals. The multiscale features are then learnt on these signals by a motion encoder, and further injected into the 3D-UNet of SVD in a feature modulation manner. Meanwhile, LoRA layers are integrated into all attention modules in the transformer blocks to improve the optimization of motiontrajectory alignment. In the inference stage, the region-wise trajectory and motion mask are first derived from the user provided trajectory and brushed region, and...*

MotionPro 的整体 pipeline 围绕**区域级轨迹（region-wise trajectory）** 与**运动掩码（motion mask）** 两个互补控制信号的生成与注入展开，在预训练视频扩散模型 SVD 的基础上实现精确可控的图像到视频（I2V）生成。其架构与工作流如 Figure 2 所示，分为训练和推理两个阶段。

**训练阶段**的输入是原始视频片段及其首帧参考图像。首先，利用外部光流追踪模型 DOT 估计视频各帧相对于首帧的光流映射 $f^i$ 及帧间可见性掩码 $M^i$：
$$f^i, M^i = \mathrm{DOT}(\mathbf{x}_0^1, \mathbf{x}_0^i), \quad i = 1, 2, ..., L$$
在此基础上，区域级轨迹生成器从光流图的多个局部区域直接采样轨迹点，**不使用大核高斯滤波**，从而保留精细运动细节；运动掩码生成器则通过对时序平均光流幅度 $f_{avg}$ 进行阈值化，输出二值掩码 $M_{mot}$，显式标识整体运动区域。这两个信号经通道拼接后，送入一个轻量级**运动编码器（Motion Encoder）**，编码为多尺度特征图。

这些多尺度运动特征随后被注入 SVD 的 3D-UNet 中，通过**自适应特征调制（adaptive feature modulation）** 对视频潜码特征进行调节：
$$h_s' = GN(h_s) \cdot \gamma_s + \beta_s + h_s$$
其中 $\gamma_s$ 和 $\beta_s$ 由运动编码器预测，$GN$ 为组归一化，快捷连接保证了原始信息的保留。同时，在时空 Transformer 的所有注意力模块中集成 **LoRA 低秩适配器**，以低分解形式 $\mathcal{W}' = \mathcal{W} + A B^T$ 微调权重，在保护预训练运动先验的前提下提升运动-轨迹对齐能力。

**推理阶段**，区域级轨迹和运动掩码由用户提供的轨迹线与涂抹区域推导而来，经相同的运动编码器与特征调制通路注入 3D-UNet，校准视频去噪过程，最终生成与输入控制信号精确对齐的视频。

整个 pipeline 的核心设计逻辑在于：区域级轨迹负责局部精确采样，运动掩码负责全局运动类别标识，二者通过自适应特征调制实现松耦合但互补的控制，避免了传统高斯滤波轨迹带来的细节模糊与运动歧义问题。

## 核心模块与公式推导

MotionPro 的核心设计围绕三个关键模块展开：运动条件生成、自适应特征调制与高效微调策略。以下逐一剖析其技术细节与公式含义。

### 运动条件生成：区域级轨迹与运动掩码

传统方法（如 DragNUWA）从全图光流随机采样点迹后施加高斯滤波，导致运动细节模糊。MotionPro 的改进在于**直接在光流局部区域内采样轨迹**，避免高斯平滑带来的信息损失。

**光流与可见性估计**。给定训练视频帧序列 $\{\mathbf{x}_0^i\}_{i=1}^{L}$，首先利用 DOT 追踪模型估计第 1 帧与第 $i$ 帧之间的光流 $f^i$ 与可见性掩码 $M^i$：

$$f^i, M^i = \mathrm{DOT}(\mathbf{x}_0^1, \mathbf{x}_0^i), \quad i = 1, 2, ..., L$$

对所有帧的可见性掩码取交集，得到全局可见性掩码 $M_g$：

$$M_g = \prod_{i=1}^{L} M^i$$

将 $M_g$ 与各帧光流逐元素相乘，过滤不可见区域：

$$\mathbf{\mathcal{f}}_m = \{ f^i \cdot M_g \}_{i=1}^{L}$$

**区域级轨迹采样**。将掩码后的光流图划分为 $k \times k$ 个局部区域，均匀采样子集作为区域级轨迹 $\mathbf{T}_s$：

$$\mathbf{T}_s = \{ f_m^i \cdot Pad(M_{sel}) \}_{i=1}^{L}$$

其中 $M_{sel}$ 为所选区域的二值掩码。这种局部直接采样策略保留了区域内的精确运动细节，是 MotionPro 实现细粒度控制的关键。

**运动掩码生成**。为显式标识运动类别（物体运动 vs. 相机运动），MotionPro 从光流幅度推导运动掩码。首先计算所有帧光流幅度的时序平均值：

$$f_{avg} = \frac{1}{L} \sum_{i=1}^{L} \parallel f^i \parallel_2$$

然后通过阈值化生成二值运动掩码 $M_{mot} \in \{0,1\}^{H \times W}$：将 $f_{avg} > 1$ 的位置设为 True，其余为 False。该掩码全局强调运动区域，与区域级轨迹形成互补——轨迹提供局部精确控制，掩码指定整体运动范围与类别。

### 扩散模型基础

MotionPro 基于 Stable Video Diffusion (SVD) 的 EDM 训练框架。前向扩散过程将高斯噪声 $\mathbf{n}$ 添加到干净视频潜码 $\mathbf{z}_0$：

$$\mathbf{z} = \mathbf{z}_0 + \mathbf{n}, \quad (\sigma, \mathbf{n}) \sim p(\sigma, \mathbf{n})$$

3D-UNet $F_{\pmb{\theta}}$ 基于噪声水平 $\sigma$ 和参考图像条件 $\mathbf{c}_I$ 预测干净潜码：

$$\hat{\mathbf{z}}_0 = c_{\mathrm{skip}}(\sigma) \mathbf{z} + c_{\mathrm{out}}(\sigma) F_{\pmb{\theta}}(c_{\mathrm{in}}(\sigma) \mathbf{z}, \, \mathbf{c}_I; \, c_{\mathrm{noise}}(\sigma))$$

训练损失采用去噪得分匹配：

$$\mathcal{L} = \mathbb{E}_{\mathbf{z}_0, \mathbf{c}_I, (\boldsymbol{\sigma}, \mathbf{n}) \sim p(\boldsymbol{\sigma}, \mathbf{n})} \left[ \lambda_{\sigma} \lVert \hat{\mathbf{z}}_0 - \mathbf{z}_0 \rVert_2^2 \right]$$

### 自适应特征调制

MotionPro 通过轻量运动编码器将拼接后的轨迹与掩码编码为多尺度特征，再注入 3D-UNet。注入方式采用**自适应特征调制**，而非传统的通道拼接或特征求和。

具体而言，运动编码器对每个尺度 $s$ 输出特征 $l_s$，通过时空卷积层预测缩放参数 $\gamma_s$ 和偏置参数 $\beta_s$。对视频潜码特征 $h_s$ 先进行组归一化，再施加仿射变换，并添加快捷连接：

$$h_s' = GN(h_s) \cdot \gamma_s + \beta_s + h_s$$

这种调制方式的优势在于：拼接或求和需要控制信号与视频特征在时空维度上严格对齐，而调制通过预测参数间接影响特征分布，无需显式对齐，从而更灵活地融合运动条件。

### LoRA 微调策略

为保护预训练模型的运动先验，MotionPro 仅在所有时空 Transformer 的注意力模块中集成 LoRA 低秩适配器进行微调。原始注意力权重 $\mathcal{W}$ 与低秩分解矩阵的融合方式为：

$$\mathcal{W}' = \mathcal{W} + \Delta \mathcal{W} = \mathcal{W} + A B^T$$

其中 $A$ 和 $B$ 为低秩矩阵。这种策略在保持基座模型泛化能力的同时，显著提升了运动-轨迹对齐精度，且仅引入极少可训练参数。

## 实验与分析

### 主实验结果

MotionPro 在细粒度运动控制和目标级运动控制两个设定下均展现出显著优势。在 WebVid-10M 基准上，MotionPro 取得 FVD 59.88，相比 MOFA-Video（87.70）和 DragNUWA（96.65）分别降低 27.82 和 36.77；FID 降至 10.40，帧一致性达到 0.9895（Table 1）。FVD 的大幅下降表明生成视频的运动质量与真实视频分布更为接近，而帧一致性的微弱优势说明基线方法在时序连贯性上已具备较强能力，该指标并非区分性瓶颈。

![[assets/figures/papers/paper_list_l35_MotionPro_A_Precise_Motion_Controller_for_Image_to_Video_Generation/figures/004_Table_1.jpg]]
*Table 1: Fine-grained motion control results on WebVid-10M*

在 MC-Bench 细粒度控制评估中，MotionPro 的 MD-Img 和 MD-Vid 分别为 10.56 和 9.23，均优于 MOFA-Video 和 DragNUWA（Table 2）。更关键的是，MotionPro 生成视频的平均光流幅度达 8.95，约为 MOFA-Video（4.95）的 1.8 倍，直接量化了其生成运动幅度更接近真实运动轨迹的能力。

![[assets/figures/papers/paper_list_l35_MotionPro_A_Precise_Motion_Controller_for_Image_to_Video_Generation/figures/005_Table_2.jpg]]
*Table 2: Fine-grained motion control results on MC-Bench*

目标级控制设定下，MotionPro 在 MC-Bench 上取得 MD-Img 10.48、MD-Vid 8.59，相较 DragAnything 分别降低 1.82 和 2.78（Table 3）。值得注意的是，DragAnything 在此设定中已添加静态点以辅助区分物体与相机运动，MotionPro 仍能显著超越，表明运动掩码的显式运动类别指定机制在目标级控制中发挥了关键作用。

![[assets/figures/papers/paper_list_l35_MotionPro_A_Precise_Motion_Controller_for_Image_to_Video_Generation/figures/007_Table_3.jpg]]
*Table 3: Object-level motion control results on MC-Bench*

人体评估进一步验证了上述结论：在细粒度控制中，75.00% 的评估者偏好 MotionPro 的运动质量，远超 MOFA-Video（21.88%）和 DragDiffusion（3.12%）；在目标级控制中，68.75% 偏好 MotionPro，而 MOFA-Video 和 DragAnything 分别仅为 12.50% 和 18.75%（Table 4）。DragDiffusion 在细粒度控制中仅获 3.12% 偏好，暴露了逐帧图像编辑策略在视频运动连贯性上的根本缺陷。

![[assets/figures/papers/paper_list_l35_MotionPro_A_Precise_Motion_Controller_for_Image_to_Video_Generation/figures/013_Table_4.jpg]]
*Table 4: Human evaluation of user preference ratios (%) over both fine-grained and object-level motion control on MC-Bench*

### 消融实验

**区域级轨迹与运动掩码的必要性。** 移除区域级轨迹（MotionPro−traj，替换为随机轨迹）使 FVD 升至 73.7，移除运动掩码（MotionPro−mask，替换为全一掩码）使 FVD 升至 66.2，均显著劣于完整 MotionPro 的 59.88。两个信号缺一不可，且区域级轨迹的贡献更大——FVD 恶化幅度（+13.82）高于移除运动掩码（+6.32），表明精确轨迹是运动控制的首要条件，而运动掩码提供全局运动区域标识以消除歧义。

**局部区域大小 k 的影响。** 在 MC-Bench 上，k=8 时 MD-Vid 和帧一致性均达到最优（Figure 6a）。k 过小（如 k=4）导致每个区域包含的轨迹信息过于稀疏，运动细节不足；k 过大（如 k=16）则退化为近似全局采样的高斯滤波效应，丧失区域级轨迹的精细控制优势。可视化对比（Figure 7）印证了这一趋势：k=4 时运动幅度偏弱，k=16 时出现运动模糊和轨迹偏离。

![[assets/figures/papers/paper_list_l35_MotionPro_A_Precise_Motion_Controller_for_Image_to_Video_Generation/figures/009_Figure_6.jpg]]
*Figure 6: Performance comparisons of MD-Vid and Frame Consistency on MC-Bench under the settings of both fine-grained and objectlevel motion control by using different (a) local region size k and (b) minimal mask ratio r _ { m i n } in MotionPro*

**最小掩码比例 r_min 的影响。** 训练时随机丢弃部分轨迹区域以增强鲁棒性，r_min=0.95（即保留 95% 的轨迹区域）在 MD-Vid 和帧一致性上取得最佳平衡（Figure 6b）。过低的 r_min 导致训练信号过于稀疏，运动-轨迹对齐能力下降；r_min=1.0（无丢弃）则降低了对推理时不精确掩码的鲁棒性。

**特征注入方式的对比。** 自适应特征调制在 MD-Vid 指标上显著优于特征拼接（MotionProC）和特征求和（MotionPro⁺）（Figure 8）。特征拼接和求和要求控制信号与视频潜码在空间-时序维度上严格对齐，而光流轨迹的稀疏性与视频特征的密集性之间存在天然的结构错位；特征调制通过学习缩放 γ_s 和偏置 β_s 进行仿射变换，绕过了这一对齐约束，同时保留快捷连接以维持预训练特征的信息通路。

### 鲁棒性与局限性

MotionPro 对运动掩码的形状变化具有较强的鲁棒性：训练时掩码由 DOT 光流阈值化生成（并非精确标注），推理时即使使用不同形状的掩码区域，生成质量仍保持稳定（Figure 10）。这一特性源于训练阶段引入的掩码随机丢弃机制，使模型学会从非精确掩码中提取运动区域信息。

然而，该方法的运动条件质量受限于外部光流追踪模型 DOT 的精度。在包含遮挡、快速运动或纹理稀疏的复杂场景中，DOT 估计的光流可能存在误差，进而影响区域级轨迹和运动掩码的准确性。此外，运动掩码基于光流幅度阈值化（阈值为 1）生成，可能遗漏平滑或微小的运动区域，且边界精度有限。论文未在更强基线（如 CogVideoX）上进行对比验证，其在更近期视频扩散模型上的增益幅度仍有待确认。

### 补充图表

![[assets/figures/papers/paper_list_l35_MotionPro_A_Precise_Motion_Controller_for_Image_to_Video_Generation/figures/008_Figure.jpg]]
*Figure: Input Control MOFA-Video DragAnything MotionPro*

## 方法谱系与知识库定位

### 核心瓶颈与设计动机

现有可控图像到视频生成（I2V）方法在细粒度运动控制上面临一个共同瓶颈：依赖大高斯核将稀疏点迹扩展为稠密运动场。这一操作虽然能覆盖更大空间范围，却不可避免地模糊了运动细节，导致生成的视频难以精确复现用户指定的轨迹。更关键的是，仅凭轨迹信号无法区分物体运动与相机运动——例如，背景整体平移既可解释为相机摇镜，也可解释为物体平移，这种歧义在复杂场景中尤为突出。

MotionPro 的因果调节旋钮在于**区域级轨迹（region-wise trajectory）与运动掩码（motion mask）的联合利用**：前者在光流图的局部区域内直接采样，避免高斯平滑以保留精细运动细节；后者从光流幅度推导出二进制掩码，显式标识运动区域并指定运动类别，从而消除物体/相机运动的歧义。

### 与现有方法的关键差异

MotionPro 相对于代表性基线方法做出了四个关键槽位改变：

**1. 运动条件轨迹表示**

- **基线做法**：DragNUWA（Yin et al., arXiv 2023）等从全图光流随机采样点迹后，应用大核高斯滤波生成稠密轨迹条件。MOFA-Video 采用稀疏到密集轨迹网络，但同样依赖全局光流信息。
- **MotionPro 改变**：在光流图的多个 $k \times k$ 局部区域内直接采样轨迹，不使用高斯滤波，保持原始运动细节。消融实验显示，当 $k=8$ 时 MD-Vid 和帧一致性达到最优（Figure 6a），验证了小区域轨迹对精确运动信息的保留能力。

**2. 运动区域指定**

- **基线做法**：DragNUWA、DragAnything（Wu et al., ECCV 2024）等方法仅凭轨迹隐含运动区域，缺乏显式的运动类别标识。
- **MotionPro 改变**：引入运动掩码 $M_{mot} \in \{0,1\}^{H \times W}$，通过光流平均幅度阈值化生成（$f_{avg} > 1$ 的位置设为 True），显式标识运动区域。消融实验表明，移除运动掩码（MotionPro⁻ᵐᵃˢᵏ）使 FVD 从 59.88 升至 66.2（Section 6.4），证明该信号对整体运动建模不可或缺。

**3. 控制信号注入方式**

- **基线做法**：DragNUWA 将轨迹条件与视频潜码通道拼接；其他方法多采用特征求和。
- **MotionPro 改变**：采用自适应特征调制（adaptive feature modulation），利用轻量运动编码器预测缩放 $\gamma_s$ 和偏置 $\beta_s$，通过 SPADE-like 变换 $h_s' = GN(h_s) \cdot \gamma_s + \beta_s + h_s$ 注入 3D-UNet。Figure 8 的消融显示，该方式在 MD-Vid 指标上显著优于特征拼接（MotionProᶜ）和特征求和（MotionPro⁺），且不要求控制信号与视频潜码之间严格的空间-时间对齐。

**4. 可训练参数量与微调策略**

- **基线做法**：多数方法采用全参数微调或未明确说明微调范围。
- **MotionPro 改变**：仅在所有时空 Transformer 的注意力模块中集成 LoRA 低秩适配器（$W' = W + AB^T$），在保护预训练运动先验的同时提升运动-轨迹对齐能力。

### 方法适用边界与局限

**1. 对外部光流模型的依赖**

MotionPro 的训练条件（区域级轨迹和运动掩码）完全依赖 DOT 光学追踪模型从训练视频中估计的光流和可见性掩码。在遮挡严重、纹理稀疏或快速运动的场景下，DOT 的估计精度下降会直接传导至控制信号质量，进而影响生成效果。这一依赖关系构成了方法的系统性上限。

**2. 运动掩码的粒度限制**

运动掩码基于光流幅度阈值化（$f_{avg} > 1$）生成，本质上是硬阈值二值化。对于平滑缓慢的运动（如云层漂移）或微小运动区域，该阈值可能无法有效捕捉；同时掩码边界精度受限于光流估计的分辨率，可能不够精确。

**3. 基座模型的时效性**

论文实验基于 SVD（Stable Video Diffusion）构建，未对比更近期的视频扩散模型（如 CogVideoX）。在更强基座模型上的性能提升幅度仍有待验证。

**4. 多物体独立运动的信号冲突**

当前设计中，运动掩码是一个全局二值图，区域级轨迹在多个局部区域采样。当场景包含多个独立运动物体（如一人向左走、一车向右开）时，掩码无法区分不同物体的运动类别，区域级轨迹的采样策略也可能导致信号冲突。论文未对此场景进行专门消融。

### 开放问题

1. **多物体场景的分工机制**：在多个独立运动物体共存的场景中，区域级轨迹和运动掩码如何有效分工以避免信号冲突？是否需要对掩码进行实例级扩展？

2. **长视频与高分辨率扩展**：当前方法在 16 帧、WebVid-10M 分辨率上验证。扩展到更长时序（如 64 帧以上）和更高分辨率时，区域级轨迹的采样策略和自适应特征调制的计算开销是否仍可行？

3. **与文本提示的语义融合**：能否将区域级轨迹控制与文本提示进一步结合，实现更语义化的运动生成（如“让这只鸟沿弧形轨迹飞翔，同时翅膀扇动”）？这需要在运动编码器中引入跨模态对齐机制。

4. **实时交互式控制**：当前推理流程需要用户提供轨迹和掩码，能否实现画笔式实时交互，让用户在生成过程中动态调整运动条件？这对运动编码器的推理效率提出更高要求。

## 原文 PDF

![[paperPDFs/CVPR_2025/MotionPro_A_Precise_Motion_Controller_for_Image_to_Video_Generation.pdf]]
