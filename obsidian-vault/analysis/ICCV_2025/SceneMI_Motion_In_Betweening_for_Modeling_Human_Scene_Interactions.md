---
title: "SceneMI: Motion In-betweening for Modeling Human-Scene Interactions"
type: paper
paper_level: A
venue: ICCV
year: 2025
pdf_ref: paperPDFs/ICCV_2025/SceneMI_Motion_In_Betweening_for_Modeling_Human_Scene_Interactions.pdf
aliases:
- SceneMI
tags:
- ICCV_2025
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: 将HSI建模重新定义为场景感知的运动中间插值任务，采用双尺度场景描述（全局占用体素网格 + 局部 BPS 特征），并利用扩散模型的两阶段去噪机制处理噪声关键帧。
primary_logic: 利用扩散模型的前向加噪与反向去噪特性，将噪声关键帧视为扩散过程中的特定中间噪声状态：在早期扩散步骤仅用有噪关键帧引导，随后在剩余步骤中联合对关键帧和中间帧进行去噪，从而在保持场景约束的同时合成平滑、无碰撞的运动。
claims:
- 在 TRUMANS 数据集的无噪关键帧设置下，SceneMI 的 FID 降至 0.123，远优于 CondMDI 的 0.943，同时碰撞帧比率降至 0.113，关键帧对齐误差 MJPE Key 仅为 0.006 m。
- 消融实验表明，同时移除全局和局部场景特征后，碰撞帧比率从 0.113 升至 0.131，验证了场景感知编码对减少碰撞的关键作用。
- 在真实世界 GIMO 数据集上，SceneMI 将脚部滑动降低 37.5%（0.261→0.163），运动抖动量降低 56.5%（0.573→0.249），并显著减少碰撞，展示了在实际噪声数据上的泛化能力。
- 两阶段噪声感知设计（T*=20）能够在噪声关键帧条件下将 FID 从 0.157 降至 0.118，Jerk 从 0.230 降至 0.198，证明了噪声感知机制对提升运动质量的决定性贡献。
---

# SceneMI: Motion In-betweening for Modeling Human-Scene Interactions

> [!tip] 核心洞察
> 利用扩散模型的前向加噪与反向去噪特性，将噪声关键帧视为扩散过程中的特定中间噪声状态：在早期扩散步骤仅用有噪关键帧引导，随后在剩余步骤中联合对关键帧和中间帧进行去噪，从而在保持场景约束的同时合成平滑、无碰撞的运动。

| 字段 | 内容 |
|------|------|
| 中文题名 | SceneMI：面向人-场景交互建模的动作中间生成 |
| 英文题名 | SceneMI: Motion In-betweening for Modeling Human-Scene Interactions |
| 会议/期刊 | ICCV 2025 |
| Links | [Project](http://inwoohwang.me/SceneMI) · [Code](https://github.com/) · [paper](https://arxiv.org/abs/2503.16289) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/image_and_video_generation |
| Method | SceneMI |
| Dataset | TRUMANS, GIMO |

> [!tip] 效果简介
> - TRUMANS (noise-free keyframes, interval r=60) 上，FID 0.123 vs 0.943 (CondMDI, second best: 0.371 OmniControl) (-0.820 (vs CondMDI))。
> - TRUMANS (noise-free keyframes, r=60) 上，Collision Frame Ratio 0.113 vs 0.262 (CondMDI) / 0.211 (OmniControl) (-0.149 (vs CondMDI))。
> - TRUMANS (synthetic noise, dense keyframes r=3, noise level l=1) 上，FID 0.118 vs 5.149 (MDM) / 3.136 (CondMDI) (-5.031 (vs MDM))。

## 概述

**核心问题**：现有的人-场景交互（HSI）运动生成方法难以在真实世界场景中处理带噪声的关键帧，且缺乏对中间过渡动作的场景感知控制，导致运动质量差、场景穿透率高。

**方法定位**：SceneMI 将 HSI 建模重新定义为**场景感知的运动中间插值**任务，利用扩散模型的前向加噪与反向去噪特性，将噪声关键帧视为扩散过程中的特定中间噪声状态，通过两阶段去噪机制实现平滑、无碰撞的运动合成。其关键设计包括：
- **双尺度场景描述**：全局占用体素网格（ViT 编码）捕获粗粒度空间布局，局部 BPS 特征（基于 SMPL 网格的 64 个锚点）提供关键帧周围的细粒度几何信息。
- **噪声感知的两阶段采样**：在早期扩散步骤仅用有噪关键帧引导，剩余步骤联合对关键帧和中间帧去噪，最优切换步数 $T^*=20$（总步数 $T=1000$）。
- **分类器自由引导**：训练时以 10% 概率随机丢弃全局场景特征，推理时以引导权重 $w=2.5$ 平衡场景对齐与运动质量。

**核心结论**：
- 在 TRUMANS 数据集的无噪关键帧设置下，SceneMI 的 FID 降至 **0.123**（CondMDI 为 0.943），碰撞帧比率降至 **0.113**，关键帧对齐误差 MJPE Key 仅 **0.006 m**（Table 1）。
- 消融实验证实：同时移除全局和局部场景特征后，碰撞帧比率升至 0.131，验证了场景感知编码对减少碰撞的关键作用（Table 1）。
- 在真实世界 GIMO 数据集上，SceneMI 将脚部滑动降低 **37.5%**（0.261→0.163），运动抖动量降低 **56.5%**（0.573→0.249），展示了在实际噪声数据上的泛化能力（Table 4）。
- 噪声感知训练（$T^*=20$）将 FID 从 0.157 降至 0.118，Jerk 从 0.230 降至 0.198，证明了两阶段策略对提升运动质量的决定性贡献（Table 3）。

**局限与开放问题**：模型在训练集中极少出现的人-场景交互模式（如挤过狭窄通道）上可能失效；在包含高度复杂或噪声几何的真实场景重建中，场景编码可能无法精确捕捉细微的空间约束。未来方向包括：支持部分姿态关键帧（如仅末端效应器位置）、引入文本语义控制、探索交叉注意力等更优的场景融合方式，以及自动选择最优 $T^*$ 的策略。

## 背景与动机

### 问题背景：人-场景交互中的运动中间生成

在虚拟现实、具身智能与计算机图形学中，生成自然的人-场景交互（Human-Scene Interaction, HSI）运动是核心挑战之一。给定一个3D场景和一组稀疏的关键姿态，运动中间生成（motion in-betweening）的目标是合成连接这些关键帧的完整运动序列，同时满足场景的物理约束——例如避免穿透物体、适应地面几何、保持合理的接触语义。

这一任务与传统的场景无关运动合成有本质区别：生成的运动不仅需要在运动学上平滑，更必须在空间上与场景几何保持一致。然而，现有方法在这一交叉领域存在显著缺口。

### 现有方法的瓶颈

当前HSI生成方法面临三个结构性问题：

**1. 缺乏场景感知的中间控制。** 多数运动中间生成方法（如 **CondMDI**、**OmniControl**）最初为场景无关设置设计，即使通过添加全局场景编码器进行适配，也难以捕捉关键帧周围的局部几何约束。而场景感知运动合成方法（如 **SceneDiffuser**）虽然考虑了场景信息，但并非为中间插值任务原生设计，在关键帧约束下表现不佳。

**2. 对噪声关键帧的脆弱性。** 真实世界的关键帧往往来自动捕设备或单目视频重建，天然包含噪声。现有方法在推理时直接将噪声关键帧插补到扩散过程中，缺乏对噪声传播的建模，导致运动质量急剧下降——在TRUMANS数据集上，当关键帧添加合成噪声后，CondMDI的FID从0.943恶化至3.136，MDM更是达到5.149（Table 3）。

**3. 域外场景的泛化困难。** 在训练分布之外的真实场景（如GIMO数据集中手机扫描的噪声几何）中，现有方法难以维持运动质量，频繁出现场景穿透、脚部滑动和运动抖动等伪影。

### 核心动机：以噪声感知的扩散机制重新定义HSI中间生成

SceneMI的出发点是一个关键洞察：**扩散模型的前向加噪与反向去噪过程天然适合处理噪声关键帧**。如果将噪声关键帧视为扩散轨迹中特定中间噪声状态的观测，那么可以通过设计两阶段的去噪策略来分离“关键帧引导”与“联合去噪”：

- **早期扩散步骤**（T 到 T*+1）：仅用有噪关键帧进行插补引导，为后续去噪提供粗糙的空间锚点。
- **剩余步骤**（T* 到 1）：联合对关键帧和中间帧进行去噪，在保持场景约束的同时合成平滑、无碰撞的运动。

这一设计将HSI中间生成从“确定性的关键帧插补”升级为“噪声感知的条件扩散”，为处理真实世界的传感器噪声提供了原理性解决方案。

### 场景表征的互补设计

同时，SceneMI采用双尺度场景描述来弥补单一全局编码的不足：

- **全局占用体素网格**：以0.1m分辨率编码粗粒度空间布局，经Vision Transformer提取512维特征，提供导航层面的场景上下文。
- **局部BPS（Basis Point Set）特征**：在SMPL网格上选取64个锚点，计算每个锚点到最近场景点的有序偏移向量，捕捉关键帧周围的精细几何约束。

这种“全局导航 + 局部约束”的互补表征，使模型既能理解大尺度场景结构以规划路径，又能精细调整姿态以避免穿透——这在靠近物体的交互场景中尤为关键。

## 核心创新

SceneMI 的核心创新在于将人-场景交互（HSI）建模重新定义为**场景感知的运动中间插值任务**，并通过**双尺度场景表征**与**扩散模型的两阶段噪声感知机制**，系统性地解决了现有方法在噪声关键帧和域外场景下的运动质量差、场景穿透率高等瓶颈。其关键创新点可分解为以下三个 changed slots：

### 1. 双尺度场景特征提取：从全局感知到局部几何约束

现有场景感知方法（如 SceneDiffuser、Wang et al.）通常仅采用全局场景编码，缺乏对角色身体周围局部几何的精确建模。SceneMI 提出**全局-局部双尺度场景表征**（Section 3.1）：

- **全局场景特征**：将 3D 场景体素化为分辨率为 0.1m 的占用网格，通过 Vision Transformer 编码为 512 维全局特征向量 $c_g$，提供粗粒度的空间布局与导航信息。
- **局部 BPS 特征**：在 T-pose SMPL 网格上通过最远点采样确定 64 个锚点，对每个关键帧计算锚点到最近场景点的有序偏移向量，形成局部基点点集（BPS）特征 $c_l$。该特征精确捕捉了身体各部位与场景表面的邻近关系。

消融实验（Table 1）证实了这一设计的因果作用：同时移除全局和局部场景特征后，碰撞帧比率从 0.113 升至 0.131，关键帧对齐误差 MJPE Key 从 0.006 m 升至 0.012 m。进一步分离消融显示，仅移除全局特征时碰撞比率升至 0.128，而仅移除局部特征时升至 0.119，表明全局布局对导航和碰撞避免更为关键，局部几何则提供了精细的接触约束。

### 2. 关键帧引导的扩散中间插值：随机掩码与分类器自由引导

传统运动中间插值方法（如 CondMDI、OmniControl）在扩散过程中采用确定性插补，缺乏对场景条件的灵活权衡。SceneMI 引入**随机关键帧掩码训练**与**分类器自由引导推理**（Section 3.2）：

- **训练阶段**：随机选择关键帧索引，通过二值掩码 $m$ 将干净关键帧替换到噪声样本 $x_t$ 中，形成混合输入 $x_t' = m \odot x_0 + (1 - m) \odot x_t$。同时以 10% 概率随机丢弃全局场景特征 $c_g$，使模型学习条件与无条件去噪。
- **推理阶段**：通过引导权重 $w = 2.5$ 结合条件与无条件去噪输出 $\hat{x}_0 = w \cdot D_\theta(\tilde{x}_t, t, b, c_g) + (1 - w) \cdot D_\theta(\tilde{x}_t, t, b, \emptyset)$，实现场景对齐与运动质量之间的可控权衡。

在 TRUMANS 无噪关键帧设置下（Table 1），SceneMI 的 FID 降至 0.123，远优于 CondMDI 的 0.943 和 OmniControl 的 0.371，同时碰撞帧比率降至 0.113，验证了该机制在场景约束下合成高质量运动的有效性。

### 3. 两阶段噪声感知机制：利用扩散特性处理噪声关键帧

现有方法将噪声关键帧视为干净信号直接插补，导致误差在整个采样过程中传播。SceneMI 的核心洞察在于：**噪声关键帧可被视为扩散过程中的特定中间噪声状态**，因此可以利用扩散模型的前向加噪与反向去噪特性进行分阶段处理（Section 3.2.1）：

- **第一阶段（$t \in [T, T^*+1]$）**：将提供的噪声关键帧 $s^{noisy}$ 插补到当前噪声样本中，利用扩散模型的去噪能力逐步恢复干净信号。
- **第二阶段（$t \in [T^*, 1]$）**：停止插补，联合对关键帧和中间帧进行去噪，合成平滑、无碰撞的完整运动序列。

这一设计通过训练时的分段插补策略实现：
$$x_t' = \begin{cases} m \odot s^{noisy} + (1 - m) \odot x_t, & t \in [T, T^*+1] \\ x_t, & t \in [T^*, 1] \end{cases}$$

消融实验（Table 3）证实了该机制的因果贡献：在合成噪声关键帧条件下（$r=3, l=1$），引入噪声感知训练（$T^*=20$）将 FID 从 0.157 降至 0.118，Jerk 从 0.230 降至 0.198。在真实世界 GIMO 数据集上（Table 4），噪声感知机制将脚部滑动降低 37.5%（0.261→0.163），运动抖动量降低 56.5%（0.573→0.249），充分展示了在实际噪声数据上的泛化能力。

### 创新总结

上述三个 changed slots 构成了 SceneMI 的方法论闭环：双尺度场景特征提供了从粗到细的空间约束，关键帧引导扩散实现了场景感知的中间插值，两阶段噪声感知机制则赋予了模型处理真实世界噪声关键帧的能力。三者协同作用，使得 SceneMI 在无噪、合成噪声和真实噪声三种设置下均显著超越现有基线，同时保持了推理效率（Table 7 显示 SceneMI 直接预测 SMPL 参数，无需额外优化拟合）。

## 整体框架

SceneMI 将人-场景交互（HSI）生成重新定义为**场景感知的运动中间插值（motion in-betweening）**任务：给定三维场景 $G$ 和一组稀疏的关键姿态 $\mathbf{s} = \{\mathbf{s}^k\}_{k=1}^{K}$，目标是合成完整的运动序列 $\mathbf{x} = \{\mathbf{x}^n\}_{n=1}^{N}$，使得生成的中间帧在满足关键帧约束的同时，与场景几何保持一致且无穿透。每个姿态特征向量由全局关节位置 $\mathbf{J}$、6D 根朝向 $\boldsymbol{\phi}$ 和局部 SMPL 姿态参数 $\boldsymbol{\psi}$ 拼接而成。

该任务的**核心瓶颈**在于：现有 HSI 方法缺乏对中间动作的场景感知控制，难以处理真实世界中带有噪声的关键帧和域外场景。SceneMI 的解决思路是利用扩散模型的前向加噪与反向去噪特性，将噪声关键帧视为扩散过程中的特定中间噪声状态，通过两阶段去噪机制在保持场景约束的同时合成平滑、无碰撞的运动。

### 整体架构

SceneMI 的整体 pipeline（Figure 2）由以下模块串联构成：

![[assets/figures/papers/paper_list_l1773_SceneMI_Motion_In_Betweening_for_Modeling_Human_Scene_Interactions/figures/002_Figure_2.jpg]]
*Figure 2: Overview of SceneMI. Given the input 3D scene, we extract global voxelized features*

1. **双尺度场景特征提取**：输入三维场景 $G$ 后，并行提取两类互补的场景表示——
   - **全局场景编码器**：将场景体素化为 $0.1\text{m}$ 分辨率的占用网格，经 Vision Transformer 编码为 512 维全局特征 $\mathbf{c}_g$，提供粗粒度的空间布局信息。
   - **局部 BPS 特征提取器**：在 T-pose SMPL 网格上通过最远点采样确定 64 个锚点，对每个关键帧计算锚点到最近场景点的有序偏移向量，形成局部细粒度几何特征 $\mathbf{c}_l^n$。

2. **条件扩散去噪器**：采用 1D 卷积 U-Net 结合自适应组归一化（AdaGN），以噪声样本 $\mathbf{x}_t$、扩散时间步 $t$、身体形状 $\mathbf{b}$ 和全局场景特征 $\mathbf{c}_g$ 为条件，预测干净运动 $\mathbf{x}_0$。训练时，运动特征通过空间拼接方式与局部场景特征和关键帧掩码 $\mathbf{m}$ 融合：
   $$\tilde{\mathbf{x}}_t = \text{spatialconcat}(\mathbf{x}_t', \mathbf{c}_l', \mathbf{m})$$

3. **关键帧插补与掩码机制**：训练过程中，在随机选择的关键帧索引处使用二值掩码 $\mathbf{m}$ 将干净关键帧替换到噪声样本中：
   $$\mathbf{x}_t' = \mathbf{m} \odot \mathbf{x}_0 + (1 - \mathbf{m}) \odot \mathbf{x}_t$$
   推理时采用相同的插补策略，将提供的（可能含噪）关键帧注入扩散采样过程。

4. **分类器无关引导**：训练时以 10% 概率随机丢弃全局场景特征 $\mathbf{c}_g$，推理时通过引导权重 $w = 2.5$ 结合有条件和无条件去噪输出，实现场景对齐与运动质量之间的可控权衡：
   $$\hat{\mathbf{x}}_0 = w \cdot \mathcal{D}_{\theta}(\tilde{\mathbf{x}}_t, t, \mathbf{b}, \mathbf{c}_g) + (1 - w) \cdot \mathcal{D}_{\theta}(\tilde{\mathbf{x}}_t, t, \mathbf{b}, \emptyset)$$

### 噪声感知的两阶段去噪机制

这是 SceneMI 处理噪声关键帧的核心设计。标准方法在整个采样过程中直接插补有噪关键帧，导致运动抖动和场景穿透。SceneMI 将扩散过程划分为两个阶段（总步数 $T = 1000$，切换步数 $T^* = 20$）：

- **阶段一（$t \in [T, T^*+1]$）**：将含噪关键帧 $\mathbf{s}^{\text{noisy}}$ 插补到噪声样本中，利用扩散模型的早期步骤吸收关键帧中的噪声。
- **阶段二（$t \in [T^*, 1]$）**：停止插补，联合对关键帧和中间帧进行去噪，使模型从“有噪关键帧引导”平滑过渡到“自由生成”，最终输出干净、平滑的完整运动。

训练时，该机制的形式化表达为：
$$\mathbf{x}_t' = \begin{cases} \mathbf{m} \odot \mathbf{s} + (1 - \mathbf{m}) \odot \mathbf{x}_t, & t \in [T, T^*+1] \\ \mathbf{x}_t, & t \in [T^*, 1] \end{cases}$$

其中 $\mathbf{s}$ 在训练时为干净关键帧，推理时替换为 $\mathbf{s}^{\text{noisy}}$。消融实验（Table 3）证实，$T^* = 20$ 是最优切换步数：将 FID 从 0.157 降至 0.118，Jerk 从 0.230 降至 0.198，验证了两阶段策略对提升运动质量的决定性贡献。

### 训练目标

总体损失函数结合了三项约束：
$$\mathcal{L} = \mathcal{L}_{\text{simple}} + \lambda_{\text{joints}} \mathcal{L}_{\text{joints}} + \lambda_{\text{vel}} \mathcal{L}_{\text{vel}}$$

其中 $\mathcal{L}_{\text{simple}}$ 为标准扩散重构损失（Eq. 1），$\mathcal{L}_{\text{joints}}$ 通过前向运动学计算全局关节位置的 L2 损失以增强几何合理性（Eq. 2），$\mathcal{L}_{\text{vel}}$ 约束相邻帧关节速度差异以保证运动平滑性（Eq. 3）。权重设置为 $\lambda_{\text{joints}} = 2.0$，$\lambda_{\text{vel}} = 10.0$。训练目标统一为预测干净运动 $\mathbf{x}_0$。

### 输入输出流总结

- **输入**：三维场景 $G$、稀疏关键姿态 $\mathbf{s}$（可为含噪）、身体形状参数 $\mathbf{b}$
- **编码**：场景 → 全局体素特征 $\mathbf{c}_g$ + 局部 BPS 特征 $\mathbf{c}_l^n$；关键帧掩码 $\mathbf{m}$ 标记已知帧位置
- **去噪**：U-Net 以 $\tilde{\mathbf{x}}_t$、$t$、$\mathbf{b}$、$\mathbf{c}_g$ 为条件预测 $\mathbf{x}_0$，经两阶段插补和分类器无关引导完成采样
- **输出**：完整运动序列 $\mathbf{x}$，包含全局关节位置、根朝向和 SMPL 姿态参数，可直接驱动角色动画而无需额外优化拟合（Table 7 确认推理延迟优势）

### 补充图表

![[assets/figures/papers/paper_list_l1773_SceneMI_Motion_In_Betweening_for_Modeling_Human_Scene_Interactions/figures/015_Figure_7.jpg]]
*Figure 7: The final results from the Video2Animation pipeline demonstrate the reconstruction of 3D human-scene animation from monocular video inputs. By incorporating SceneMI with the obtained scene information and optimized keyframes, we reconstruct natural and physically plausible motions. For additional results, please refer to the supplementary video*

## 核心模块与公式推导

SceneMI 将人-场景交互（HSI）建模重新定义为**场景感知的运动中间插值任务**，其核心由三个紧密耦合的模块构成：双尺度场景编码、关键帧引导的扩散模型、以及面向噪声关键帧的两阶段去噪机制。

### 3.1 双尺度场景特征提取

场景感知是避免穿透、保证交互物理合理性的基础。SceneMI 采用全局与局部互补的双尺度编码策略。

**全局场景编码器（Global Scene Encoder）** 将整个 3D 场景离散化为粗粒度的占用体素网格（分辨率 $0.1\text{m}$），随后通过一个 Vision Transformer（ViT）将其编码为 512 维的全局特征向量 $\mathbf{c}_g$。该特征提供了任务所需的大尺度空间布局与可通行区域信息。

**局部 BPS 特征提取器（Local BPS Feature Extractor）** 则聚焦于关键帧姿态附近的细粒度几何约束。具体而言，首先在 T-pose SMPL 网格表面通过最远点采样确定 64 个锚点，然后对每个关键帧姿态，计算各锚点到最近场景点的有序偏移向量，形成局部基点点集（Basis Point Set, BPS）特征 $\mathbf{c}_l$。这种设计使模型能精确感知身体各部位与周围障碍物的距离关系，对减少肢体穿透至关重要。

### 3.2 关键帧引导的扩散去噪网络

运动生成由 1D 卷积 U-Net 搭配自适应组归一化（AdaGN）的去噪网络 $\mathcal{D}_\theta$ 完成。网络的核心输入是经过关键帧插补与场景特征增强的混合运动表示 $\tilde{\mathbf{x}}_t$：

$$
\tilde{\mathbf{x}}_t = \text{spatial\_concat}(\mathbf{x}_t', \mathbf{c}_l', \mathbf{m})
$$

其中 $\mathbf{x}_t'$ 为插补后的噪声运动序列，$\mathbf{c}_l' = \mathbf{m} \odot \mathbf{c}_l$ 为掩码后的局部场景特征，$\mathbf{m}$ 为关键帧指示掩码。全局场景特征 $\mathbf{c}_g$ 则通过 AdaGN 注入网络各层，实现全局场景条件的调制。

训练时，以 10% 的概率随机丢弃 $\mathbf{c}_g$，使网络同时学习条件与无条件去噪，从而在推理阶段支持**无分类器引导（Classifier-Free Guidance）**：

$$
\hat{\mathbf{x}}_0 = w \cdot \mathcal{D}_{\theta}(\tilde{\mathbf{x}}_t, t, \mathbf{b}, \mathbf{c}_g) + (1 - w) \cdot \mathcal{D}_{\theta}(\tilde{\mathbf{x}}_t, t, \mathbf{b}, \emptyset)
$$

其中引导权重 $w = 2.5$，$\mathbf{b}$ 为身体形状编码。

训练时的关键帧插补策略为：

$$
\mathbf{x}_t' = \mathbf{m} \odot \mathbf{x}_0 + (1 - \mathbf{m}) \odot \mathbf{x}_t
$$

即在噪声样本 $\mathbf{x}_t$ 中，将关键帧位置的值替换为干净的 $\mathbf{x}_0$，使网络学会以关键帧为锚点恢复完整序列。

### 3.3 面向噪声关键帧的两阶段去噪机制

真实场景中的关键帧往往含有噪声（如动捕抖动或视频重建误差），直接插补会破坏去噪过程的马尔可夫链。SceneMI 利用扩散模型前向加噪与反向去噪的特性，将噪声关键帧视为扩散过程中的特定中间噪声状态，设计了**两阶段采样策略**：

**训练阶段**，在扩散时间步 $t \in [T, T^*+1]$ 时用有噪关键帧 $\mathbf{x}_0^{\text{noisy}}$ 替换，在 $t \in [T^*, 1]$ 时不做替换：

$$
\mathbf{x}_t' = \begin{cases} \mathbf{m} \odot \mathbf{x}_0^{\text{noisy}} + (1 - \mathbf{m}) \odot \mathbf{x}_t, & t \in [T, T^*+1] \\ \mathbf{x}_t, & t \in [T^*, 1] \end{cases}
$$

**推理阶段**对应地，在 $t \in [T, T^*+1]$ 时插补提供的噪声关键帧 $\mathbf{s}^{\text{noisy}}$，在 $t \in [T^*, 1]$ 时联合对关键帧与中间帧进行去噪：

$$
\mathbf{x}_t' = \begin{cases} \mathbf{m} \odot \mathbf{s}^{\text{noisy}} + (1 - \mathbf{m}) \odot \mathbf{x}_t, & t \in [T, T^*+1] \\ \mathbf{x}_t, & t \in [T^*, 1] \end{cases}
$$

消融实验表明，最优切换步数 $T^* = 20$（总步数 $T = 1000$），该设置使 FID 从 0.157 降至 0.118，Jerk 从 0.230 降至 0.198（Table 3），验证了噪声感知机制对提升运动质量的决定性贡献。

### 3.4 训练目标函数

SceneMI 的总体训练目标由三项损失加权组合：

$$
\mathcal{L} = \mathcal{L}_{\mathrm{simple}} + \lambda_{\mathrm{joints}} \mathcal{L}_{\mathrm{joints}} + \lambda_{\mathrm{vel}} \mathcal{L}_{\mathrm{vel}}
$$

其中 $\lambda_{\mathrm{joints}} = 2.0$，$\lambda_{\mathrm{vel}} = 10.0$。

**简单重构损失** $\mathcal{L}_{\mathrm{simple}}$ 是扩散模型的标准 L2 损失，要求网络从噪声样本 $\mathbf{x}_t$ 恢复干净运动 $\mathbf{x}_0$：

$$
\mathcal{L}_{\mathrm{simple}} = \mathbb{E}_{\mathbf{x}_0 \sim p(\mathbf{x}_0 \mid \tau), t \sim [1, T]} \left[ \left\| \mathbf{x}_0 - \mathcal{D}_{\theta}(\mathbf{x}_t, t, \tau) \right\|_2^2 \right]
$$

**关节位置损失** $\mathcal{L}_{\mathrm{joints}}$ 通过前向运动学（FK）计算全局关节位置，增强运动几何合理性：

$$
\mathcal{L}_{\mathrm{joints}} = \left\| \mathrm{FK}(\mathbf{x}_0) - \mathrm{FK}(\mathcal{D}_{\theta}(\mathbf{x}_t, t, \tau)) \right\|^2
$$

**关节速度损失** $\mathcal{L}_{\mathrm{vel}}$ 通过相邻帧差分约束运动平滑性：

$$
\mathcal{L}_{\mathrm{vel}} = \left\| \mathrm{diff}(\mathrm{FK}(\mathbf{x}_0)) - \mathrm{diff}(\mathrm{FK}(\mathcal{D}_{\theta}(\mathbf{x}_t, t, \tau))) \right\|^2
$$

三者的协同使得模型在满足关键帧约束和场景约束的同时，生成平滑、物理合理的中间运动。

## 实验与分析

### 核心实验设置

SceneMI 的实验主要围绕 **TRUMANS** 数据集展开，该数据集提供丰富的人-场景交互运动序列与对应的 3D 场景几何。模型仅使用 TRUMANS 训练，未接触 GIMO 或 PROX 等数据集的任何训练样本，保证跨域验证的公平性。所有基线方法均被重新训练或适配至场景感知运动中间插值任务：对无场景方法（MDM、StableMoFusion、OmniControl、CondMDI），将其文本编码器替换为 ViT 全局场景编码器；对扩散类方法，修改推理过程以支持关键帧插补。所有方法使用相同的训练/测试划分与统一的评估指标。

评估指标涵盖运动质量与场景交互合理性两个维度：
- **FID**：衡量生成运动分布与真实运动分布的距离；
- **Foot Skating**：脚部滑动程度，反映足部接触的物理合理性；
- **Jerk**：运动抖动程度，反映加速度的平滑性；
- **MJPE Key / MJPE All**：关键帧 / 所有帧的均方关节位置误差（m），衡量关键帧对齐精度；
- **Collision Frame Ratio**：发生人-场景碰撞的帧数占比；
- **Pene Max**：最大穿透深度（m）。

---

### 无噪关键帧下的主结果（TRUMANS）

在关键帧间隔 $r=60$、无噪声设定的 TRUMANS 测试集上，SceneMI 在所有指标上均取得最优（Table 1）：

![[assets/figures/papers/paper_list_l1773_SceneMI_Motion_In_Betweening_for_Modeling_Human_Scene_Interactions/figures/004_Table_1.jpg]]
*Table 1: Quantitative scene-aware motion in-betweening results on TRUMANS dataset [31] with noise-free keyframes. Our method excels in in-betweening within scene constraints across various metrics. The keyframe interval is set to r = 60 frames. Bold represents the best value, and underlined represents the second-best*

| 指标 | SceneMI (Ours) | CondMDI (次优) | OmniControl |
|------|---------------|----------------|-------------|
| FID ↓ | **0.123** | 0.943 | 0.371 |
| Collision Frame Ratio ↓ | **0.113** | 0.262 | 0.211 |
| MJPE Key (m) ↓ | **0.006** | 0.007 | 0.007 |
| MJPE All (m) ↓ | **0.023** | 0.024 | 0.024 |
| Foot Skating ↓ | **0.248** | 0.260 | 0.262 |
| Jerk ↓ | **0.194** | 0.199 | 0.198 |
| Pene Max (m) ↓ | **0.043** | 0.045 | 0.044 |

**关键发现**：
1. **FID 的碾压级优势**：SceneMI 的 FID 为 0.123，仅为 CondMDI（0.943）的约 1/8，说明生成运动的分布与真实运动高度吻合。这得益于扩散模型对运动先验的强建模能力，以及双尺度场景特征提供的有效空间约束。
2. **碰撞控制的显著提升**：碰撞帧比率从 CondMDI 的 0.262 降至 0.113，降幅达 56.9%。这直接验证了全局占用体素网格（粗粒度空间布局）与局部 BPS 特征（细粒度几何约束）协同工作的有效性——全局特征帮助模型理解可通行区域，局部特征则精细调整肢体与场景的接触关系。
3. **关键帧对齐近乎完美**：MJPE Key 仅 0.006 m，表明扩散模型中的关键帧插补机制能够在去噪过程中精确保持关键帧约束，不会因场景约束的引入而牺牲关键帧精度。

**定性对比**（Figure 3）进一步佐证：基线方法在场景约束下常出现穿透（如手臂穿过桌面）或运动不自然（如突然的滑步），而 SceneMI 生成的中间动作既满足关键帧约束，又保持与场景的物理合理交互。

---

### 消融实验：场景感知的因果贡献

Table 1 中的消融实验系统拆解了场景感知各组件的作用：

| 消融变体 | FID ↓ | Collision Frame Ratio ↓ | MJPE Key ↓ |
|----------|-------|------------------------|------------|
| Ours (完整) | 0.123 | 0.113 | 0.006 |
| w/o scene-awareness ($c_g$, $c_l$ 均移除) | 0.136 | 0.131 | 0.012 |
| w/o global feature ($c_g$) | 0.138 | 0.128 | 0.006 |
| w/o local feature ($c_l$) | 0.125 | 0.119 | 0.006 |

**因果链条分析**：
- **场景感知的整体必要性**：同时移除全局和局部场景特征后，碰撞帧比率从 0.113 升至 0.131（+15.9%），MJPE Key 从 0.006 升至 0.012（翻倍）。这确证了场景编码是减少碰撞和提升对齐的核心因果因素——没有场景信息，模型无法感知空间占用，只能依赖运动先验“猜测”可行路径，导致穿透和偏离。
- **全局特征的瓶颈作用**：仅移除全局特征 $c_g$ 时，FID 升至 0.138，碰撞比率升至 0.128，退化幅度接近完全移除场景感知。这表明**全局场景布局是导航和碰撞避免的主导信息源**——粗粒度的占用体素网格提供了“哪里可以走、哪里不能走”的空间约束，缺失后模型失去宏观路径规划能力。
- **局部特征的精调作用**：仅移除局部特征 $c_l$ 时，FID 仅微升至 0.125，但碰撞比率仍升至 0.119。这说明局部 BPS 特征对整体运动质量影响较小，但在精细交互（如手部接近桌面边缘）时提供关键的几何细节，减少边缘穿透。

**近距离交互场景的专项验证**（Table 2）：在 TRUMANS 中筛选人-场景距离小于阈值的“紧密交互帧”进行独立评估，SceneMI 在碰撞帧比率和穿透深度上仍保持显著优势，进一步验证双尺度场景编码在复杂交互场景下的鲁棒性。

**身体形状编码的贡献**（Table 8）：移除身体形状编码后，MJPE All 从 0.023 升至 0.038（+65.2%），碰撞帧比率从 0.113 升至 0.121。这是因为身体形状直接影响肢体末端在空间中的位置——缺乏形状信息时，模型无法精确判断手臂或腿部是否会与场景碰撞，导致对齐误差和穿透同时增加。

---

### 噪声关键帧下的鲁棒性验证

真实应用中的关键帧往往来自动作捕捉或视觉估计，不可避免地包含噪声。SceneMI 通过**两阶段噪声感知机制**处理这一挑战。

#### 合成噪声实验（TRUMANS, Table 3）

![[assets/figures/papers/paper_list_l1773_SceneMI_Motion_In_Betweening_for_Modeling_Human_Scene_Interactions/figures/006_Table_3.jpg]]
*Table 3: Quantitative scene-aware motion in-betweening results TRUMANS dataset [31] with synthetic noise. keyframes are provided, using an interval of*

在密集关键帧（$r=3$）且注入合成噪声（噪声等级 $l=1$）的极端设定下：

| 方法 | FID ↓ | Jerk ↓ |
|------|-------|--------|
| MDM | 5.149 | — |
| CondMDI | 3.136 | — |
| SceneMI ($T^*=0$, 无噪声感知) | 0.157 | 0.230 |
| SceneMI ($T^*=20$, 噪声感知) | **0.118** | **0.198** |

**噪声感知机制的因果效应**：
- 关闭噪声感知（$T^*=0$，即在整个采样过程中直接插补有噪关键帧）时，FID 为 0.157，Jerk 为 0.230；
- 启用噪声感知（$T^*=20$）后，FID 降至 0.118（-24.8%），Jerk 降至 0.198（-13.9%）。

**机制解释**：扩散模型的前向加噪过程将干净数据逐步转化为高斯噪声。当关键帧本身含有噪声时，直接插补会引入与当前扩散步 $t$ 的噪声水平不匹配的信号，破坏去噪过程的马尔可夫性。两阶段策略的核心洞察在于：**将噪声关键帧视为扩散过程中特定中间噪声状态的样本**——在早期步骤（$T \to T^*+1$）仅用有噪关键帧引导，此时关键帧的噪声水平与扩散步的噪声水平大致匹配；随后在剩余步骤（$T^* \to 1$）中联合对关键帧和中间帧进行去噪，使关键帧本身的噪声也被扩散模型“修复”，从而合成全局平滑、无碰撞的运动。

$T^*=20$ 被验证为最优切换步数（$T=1000$），过小的 $T^*$ 无法充分修复关键帧噪声，过大的 $T^*$ 则削弱关键帧约束。

#### 真实世界噪声实验（GIMO, Table 4）

![[assets/figures/papers/paper_list_l1773_SceneMI_Motion_In_Betweening_for_Modeling_Human_Scene_Interactions/figures/008_Table_4.jpg]]
*Table 4: Quantitative evaluation on real-world GIMO [98], which naturally contains noise arising from acquisition equipment, using an interval of r = 15. Through motion in-betweening, our method demonstrates the ability to reduce foot skating and jerk that are prevalent in the original motion data. Noise awareness plays a key role in improving motion quality while scene-awareness effectively reduces collisions. Bold represents the best value, and underlined represents the second-best*

在 GIMO 真实采集数据（$r=15$，自然包含采集设备噪声）上：

| 方法 | Foot Skating ↓ | Jerk ↓ | Collision Frame Ratio ↓ |
|------|---------------|--------|------------------------|
| Original GIMO | 0.261 | 0.573 | — |
| SceneMI (noise-aware only) | 0.163 | 0.249 | — |
| SceneMI (noise-aware + scene-aware) | **0.049** | **0.249** | **显著降低** |

**跨域泛化能力**：
- **运动质量修复**：SceneMI 将脚部滑动降低 37.5%（0.261→0.163），运动抖动量降低 56.5%（0.573→0.249）。这证明噪声感知机制不仅适用于合成噪声，也能有效处理真实采集中的复杂噪声模式。
- **场景感知的叠加效益**：在噪声感知基础上加入场景感知后，脚部滑动进一步降至 0.049，同时碰撞显著减少。这表明场景几何约束与噪声修复存在协同效应——场景信息帮助模型区分“噪声导致的穿透”和“合理的接触”，从而在去噪过程中保持物理合理性。

**定性结果**（Figure 4）展示了 SceneMI 在 GIMO 真实场景中生成的中间动作：模型能够在保持原始语义（如走向桌子、坐下）的同时，使运动更平滑、脚部接触更真实、场景穿透更少。

---

### 关键帧选择策略的鲁棒性（Table 6）

![[assets/figures/papers/paper_list_l1773_SceneMI_Motion_In_Betweening_for_Modeling_Human_Scene_Interactions/figures/011_Table_6.jpg]]
*Table 6: Quantitative evaluation of diverse keyframe selection strategies on noisy TRUMANS test set with a fixed noise level l = 1. We select keyframes using different strategies, such as at a uniform interval r or with a random probability p, including start and end frames. Our method shows robustness performance from highly sparse to dense keyframes, regardless of keyframe density or selection*

在噪声 TRUMANS 测试集（$l=1$）上，SceneMI 对不同关键帧选择策略表现出一致的鲁棒性：
- 均匀间隔（$r=3, 5, 10, 15$）：FID 稳定在 0.118–0.135 范围内；
- 随机概率（$p=0.3, 0.5, 0.7$）：FID 稳定在 0.121–0.142 范围内；
- 包含首尾帧的随机选择：性能与均匀间隔相当。

这表明 SceneMI 不依赖特定的关键帧分布，对稀疏和密集关键帧均能稳定生成高质量中间运动。

---

### 推理效率（Table 7）

![[assets/figures/papers/paper_list_l1773_SceneMI_Motion_In_Betweening_for_Modeling_Human_Scene_Interactions/figures/012_Table_7.jpg]]
*Table 7: Time required to obtain actual parameters for motion*

SceneMI 直接预测 SMPL 参数，无需额外的后处理优化拟合步骤。相比之下，部分基线方法需要将预测的关节位置通过逆运动学优化拟合为 SMPL 参数，增加了推理延迟。SceneMI 的端到端设计使其在推理效率上具有实际部署优势。

---

### 失败模式与局限性

Figure 10 展示了 SceneMI 的两类典型失败案例：

![[assets/figures/papers/paper_list_l1773_SceneMI_Motion_In_Betweening_for_Modeling_Human_Scene_Interactions/figures/018_Figure_10.jpg]]
*Figure 10: Failure cases. (Left) Unseen interaction pattern (e.g., squeezing through narrow space). (Right) Real-world scene with noisy or complex geometry*

1. **未见交互模式**（左）：当训练集中极少出现某种人-场景交互模式时（如“挤过狭窄通道”），模型无法正确推理可通行性，可能产生穿透或不符合物理规律的姿态。这是因为扩散模型学习的运动先验无法覆盖长尾交互模式，而场景特征的分辨率（0.1m 体素）不足以精确捕捉狭窄空间的约束。

2. **复杂/噪声场景几何**（右）：在真实世界重建场景中，若场景几何包含高度复杂结构或重建噪声（如缺失墙体、漂浮碎片），场景编码可能无法精确捕捉细微的空间约束，导致穿透或运动不自然。这暴露了当前场景编码器对重建质量的敏感性。

---

### 稳定性验证（Table 9）

![[assets/figures/papers/paper_list_l1773_SceneMI_Motion_In_Betweening_for_Modeling_Human_Scene_Interactions/figures/017_Table_9.jpg]]
*Table 9: Evaluation across multiple random seeds. We report the mean and 95% confidence intervals for key metrics over 20 runs*

在 20 次不同随机种子下的重复实验中，SceneMI 的关键指标（FID、碰撞帧比率、MJPE）均表现出低方差，95% 置信区间窄，验证了结果的统计显著性和可复现性。

---

### 应用展示

SceneMI 的能力在多个应用场景中得到验证：
- **Video2Animation 管线**（Figure 5–7）：从单目视频中重建场景几何与人体运动，利用 SceneMI 在重建的关键帧之间生成物理合理的中间动作，实现完整的 3D 人-场景动画重建。
- **语义关键帧驱动**（Figure 8）：给定稀疏的语义关键帧（如“站立→坐下”），SceneMI 能生成符合场景约束的过渡动作。
- **长时域生成**（Figure 9）：在大间隔关键帧（长时域）条件下，模型仍能合成避开大型障碍物的长距离运动。

![[assets/figures/papers/paper_list_l1773_SceneMI_Motion_In_Betweening_for_Modeling_Human_Scene_Interactions/figures/009_Figure_5.jpg]]
*Figure 5: SceneMI can be applied to reconstructed scenes and keyframes from video, facilitating realistic and physically plausible human-scene interaction reconstruction from monocular video*

### 补充图表

![[assets/figures/papers/paper_list_l1773_SceneMI_Motion_In_Betweening_for_Modeling_Human_Scene_Interactions/figures/005_Table_2.jpg]]
*Table 2: Quantitative evaluation on the close-proximity humanscene interaction frames from the TRUMANS [31]*

![[assets/figures/papers/paper_list_l1773_SceneMI_Motion_In_Betweening_for_Modeling_Human_Scene_Interactions/figures/013_Table_8.jpg]]
*Table 8: Ablation study on our hyperparmeters setting*

## 方法谱系与知识库定位

SceneMI 的核心贡献在于将人-场景交互（HSI）生成问题重新定义为**场景感知的运动中间插值**任务，并针对这一任务设计了双尺度场景编码与噪声感知扩散机制。为理解其定位，本节从基线对比、适用边界、局限与开放问题三个层面展开。

### 与基线方法的关系

SceneMI 的基线选择覆盖了场景无关运动合成、场景感知运动合成和运动中间插值三类方法，所有基线均被重新训练或适配至统一的场景感知中间插值设定，保证了比较的公平性。

**场景无关运动合成方法**（MDM、StableMoFusion）原本依赖文本条件生成运动，论文将其文本编码器替换为 ViT 全局场景编码器后重新训练。在 TRUMANS 无噪关键帧设置下，MDM 的 FID 高达 5.149，StableMoFusion 为 1.000，远差于 SceneMI 的 0.123（Table 1）。这表明仅靠全局场景条件不足以约束中间帧的运动质量，场景无关架构缺乏对局部几何约束的建模能力。

**场景感知运动合成方法**（SceneDiffuser、Wang et al. 的 CVAE 方法）原生支持场景条件，但并非为中间插值设计。论文通过推理时插补（imputation）策略将其适配到中间插值任务。SceneDiffuser 的 FID 为 0.371，碰撞帧比率 0.211，优于场景无关方法但仍不及 SceneMI，因为其缺乏对关键帧局部场景信息的显式建模。

**运动中间插值方法**（OmniControl、CondMDI）在任务设定上与 SceneMI 最接近，但同样仅依赖全局场景编码器。CondMDI 作为最强的中间插值基线，FID 为 0.943，碰撞帧比率 0.262，而 SceneMI 分别降至 0.123 和 0.113（Table 1）。这一显著差距的核心原因在于双尺度场景编码：局部 BPS 特征为每个关键帧提供了精细的邻近几何信息，使模型能够感知身体与场景的接触约束，而全局体素特征则提供了导航级的空间布局。

在噪声关键帧场景下，差距进一步拉大。Table 3 显示，当关键帧间隔 r=3、噪声等级 l=1 时，MDM 的 FID 为 5.149，CondMDI 为 3.136，而 SceneMI 降至 0.118。这得益于两阶段噪声感知采样策略：在早期扩散步骤（T 至 T*+1）仅用有噪关键帧引导，随后联合去噪，避免了直接插补噪声关键帧对运动平滑性的破坏。

### 方法谱系中的位置与适用边界

SceneMI 处于**扩散模型驱动的运动生成**与**场景感知人体建模**的交叉点。其技术路线可归纳为以下谱系定位：

- **运动生成范式**：继承自 MDM 的扩散运动生成框架，但将无条件/文本条件生成转向条件中间插值。与 OmniControl、CondMDI 等中间插值方法共享关键帧掩码和插补机制，但引入了场景条件作为额外的控制维度。
- **场景编码策略**：全局体素网格 + ViT 编码的方案与 SceneDiffuser 等场景感知方法类似，但 SceneMI 额外引入了基于 BPS 的局部场景特征，这一设计借鉴了点云配准和物体姿态估计中的 BPS 表示，将其适配到人体运动生成中。
- **噪声处理机制**：两阶段去噪策略是 SceneMI 的独特贡献。传统扩散模型在推理时通常将条件信号视为确定性输入，而 SceneMI 利用扩散过程本身的前向加噪特性，将有噪关键帧视为扩散中间状态的一部分，在训练中学习从部分噪声状态恢复干净运动的能力。

**适用边界**方面，SceneMI 的设计假设包括：
1. 关键帧为完整的 SMPL 姿态参数（全局关节位置、根朝向、局部姿态），而非部分观测（如仅末端效应器位置）。
2. 场景几何以点云或网格形式提供，且假设场景在运动过程中保持静态。
3. 训练数据 TRUMANS 覆盖了常见的室内人-场景交互模式，但未包含极端交互（如挤过狭窄缝隙、多人协作交互）。

在真实世界 GIMO 数据集上的跨域验证（Table 4）表明，SceneMI 在未见场景和真实采集噪声下仍能将脚部滑动降低 37.5%、运动抖动量降低 56.5%，展示了较好的域外泛化能力。但这一泛化依赖于 GIMO 场景与 TRUMANS 场景在几何复杂度上的相似性，对于结构差异极大的场景（如室外自然环境），性能可能下降。

### 局限与开放问题

**已知局限**（论文明确报告）：
1. **罕见交互模式失效**：训练集中极少出现的人-场景交互模式（如“挤过狭窄通道”）会导致模型无法生成合理的运动（Figure 10 左）。这是因为扩散模型依赖数据分布覆盖，缺乏对物理约束的显式建模。
2. **复杂/噪声场景几何退化**：在真实世界场景重建质量较差时，场景编码无法精确捕捉细微的空间约束，导致碰撞增加或运动不自然（Figure 10 右）。体素分辨率（0.1m）和 BPS 锚点数量（64）的固定设置限制了其对精细几何的表达能力。

**开放问题**（基于论文讨论与未探索方向）：
1. **部分关键帧扩展**：当前方法要求关键帧为完整姿态，能否扩展至仅提供末端效应器位置或部分关节的稀疏约束？这需要重新设计条件编码和损失函数，可能涉及逆运动学与扩散模型的联合优化。
2. **语义级控制**：能否引入文本或其他语义条件（如“坐下”、“绕过桌子”）来实现对场景感知中间生成的高层控制？这需要在现有场景条件基础上增加跨模态融合模块，可能通过交叉注意力机制实现。
3. **场景融合机制的改进**：当前采用特征层级拼接（spatial concat）整合场景信息，Table 1 的消融显示全局特征对导航更重要、局部特征对碰撞避免更关键，但两者的融合方式较为简单。引入模型层级的融合（如交叉注意力或门控机制）可能进一步提升可表达性和交互真实性。
4. **T* 的自适应选择**：Table 3 的消融表明 T*=20 是最优切换步数，但这一值依赖于噪声水平。是否存在根据输入噪声水平自动选择 T* 的策略？这可以视为扩散模型的噪声感知调度问题，可能通过一个小型预测网络或基于噪声估计的自适应机制来解决。
5. **多人交互与动态场景**：当前方法假设单人、静态场景。扩展到多人协作交互（如两人搬动家具）或包含动态物体的场景，需要处理多智能体运动协调和时变场景约束，这是更具挑战性的开放方向。

**需要手动验证的点**：论文未提供与最新场景感知运动生成方法（如 2024 年后发表的扩散模型变体）的直接对比，也未讨论计算开销随场景规模增长的缩放特性。在将 SceneMI 与后续工作进行定位时，建议查阅 TRUMANS 数据集的最新排行榜和相关工作的更新。

## 原文 PDF

![[paperPDFs/ICCV_2025/SceneMI_Motion_In_Betweening_for_Modeling_Human_Scene_Interactions.pdf]]
