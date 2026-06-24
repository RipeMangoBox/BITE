---
title: "DiffuView: Multi-View Diffusion Pretraining for 3D Aware Robotic Manipulation"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/DiffuView_Multi_View_Diffusion_Pretraining_for_3D_Aware_Robotic_Manipulation.pdf
project_link: null
code_link: null
aliases:
- DiffuView
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
- topic/generative_models_diffusion
core_operator: 通过多视角扩散预训练，模型在源观测和相机位姿条件下生成目标视图，隐式恢复场景几何并强制视图一致性，为下游策略提供3D感知的视觉特征。
primary_logic: 利用多视角扩散模型作为视觉预训练骨干，能够学习跨视角几何对应关系，并将该能力迁移到机器人模仿学习中，实现仅需单视角观测即可获得视角鲁棒的操作策略。
claims:
- DiffuView在Libero和MetaWorld基准上显著优于现有方法，视角偏移下成功率提升近20%。
- 在Mv-Bench视角泛化测试上，DiffuView平均成功率达到59.2，远超OpenVLA的39.3。
- 消融实验证明机器人数据预训练、Plücker光线嵌入和FiLM语言条件对性能至关重要。
- Libero 10 上 Success Rate (%) = 89.2
---

# DiffuView: Multi-View Diffusion Pretraining for 3D Aware Robotic Manipulation

> [!tip] 核心洞察
> 利用多视角扩散模型作为视觉预训练骨干，能够学习跨视角几何对应关系，并将该能力迁移到机器人模仿学习中，实现仅需单视角观测即可获得视角鲁棒的操作策略。

| 字段 | 内容 |
|------|------|
| 中文题名 | DiffuView：面向三维感知机器人操作的多视角扩散预训练 |
| 英文题名 | DiffuView: Multi-View Diffusion Pretraining for 3D Aware Robotic Manipulation |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://openaccess.thecvf.com/content/CVPR2026/html/Zhang_DiffuView_Multi-View_Diffusion_Pretraining_for_3D_Aware_Robotic_Manipulation_CVPR_2026_paper.html) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction #topic/generative_models_diffusion |
| Method | DiffuView |
| Dataset | Libero 10, Libero 90, Libero Average, MetaWorld Average |

> [!tip] 效果简介
> - Libero 10 上，Success Rate (%) 89.2 vs - (-)。
> - Libero 90 上，Success Rate (%) 92.5 vs - (-)。
> - Libero Average (100 tasks) 上，Success Rate (%) 92.2 vs - (-)。

## 概述

机器人操作策略的视觉表征学习长期面临一个核心瓶颈：现有方法（如掩码自编码器 MAE 或神经渲染）难以在多变视角和传感器配置下学习统一的 3D 一致性表示，导致视角偏移时鲁棒性显著下降。**DiffuView** 针对这一问题，提出以**多视角扩散模型**作为视觉预训练骨干，在源观测和相机位姿条件下生成目标视图，从而隐式恢复场景几何并强制视图一致性，为下游策略提供 3D 感知的视觉特征。

其核心洞察在于：利用多视角扩散模型学习跨视角几何对应关系，并将该能力迁移到机器人模仿学习中，使策略仅需单视角观测即可获得视角鲁棒的操作能力。方法上，DiffuView 将预训练的扩散 UNet 骨干重新用作 3D 感知的视觉编码器，仅执行单次前向传播提取多尺度特征，无需去噪迭代；策略端则采用 FiLM 条件的 Q-Former 与噪声条件 MoE 扩散 Transformer 相结合，实现语言指令调制的高效动作生成。

实验表明，DiffuView 在 Libero 和 MetaWorld 基准上显著优于现有方法：Libero 100 任务平均成功率达 92.2%，MetaWorld 50 任务平均成功率达 0.706。在专门设计的视角泛化测试 Mv-Bench 上，DiffuView 平均成功率达到 59.2%，远超 OpenVLA 的 39.3%，视角偏移下成功率提升近 20%。真实世界 4 项操作任务中，DiffuView 成功率为 0.65，优于 Diffusion Policy（0.51）和 OpenVLA（0.63）。消融实验进一步验证了机器人数据预训练、Plücker 光线嵌入和 FiLM 语言条件对性能的关键作用。

## 背景与动机

### 机器人操作中的视觉表征瓶颈

机器人操作策略的性能高度依赖视觉表征的质量。当前主流的视觉预训练范式主要分为两类，但它们在面对多变视角和传感器配置时均暴露出根本性缺陷。

**掩码自编码器（MAE）范式**通过重建被随机掩码的图像区域来学习视觉表征，其概率目标可形式化为：

$$p _ { \theta } ( \hat { O } _ { i } \mid O _ { i } [ m ] )$$

这类方法（如 **MVP**，Xiao et al., arXiv 2022）虽然能够捕获局部纹理和语义信息，但本质上是2D驱动的——它们从未显式学习跨视角的几何对应关系。当相机位姿发生偏移时，编码器提取的特征会发生不可预测的畸变，导致下游策略对视角变化极度敏感。

**神经渲染范式**试图弥补这一缺陷，通过将2D观测提升至隐式3D潜空间并渲染新视图：

$$p _ { \theta } ( V \mid O _ { i } , P _ { i } ) , \quad \mathrm { w i t h } \quad { \hat { O } } = f _ { \phi } ( V , P )$$

代表性工作如 **GNFactor**（Ze et al., CoRL 2023）和 **PDFactor**（Tian et al., CVPR 2025）通过神经特征场或三平面表示来建模场景几何。然而，这类方法依赖精确的相机参数和密集的观测序列进行隐式重建，在稀疏视角或传感器配置变化时，潜空间的几何一致性难以保证。更关键的是，训练和测试阶段通常假设固定的相机配置，一旦部署环境中的视角与训练分布出现偏差，策略性能会急剧退化。

### 核心瓶颈：缺乏统一的3D一致性表示

上述方法的共同缺陷在于：**它们无法在多变视角和传感器配置下学习统一的3D一致性表示**。具体而言：

1. **MAE类方法**缺乏跨视图几何推理能力，视角偏移时特征空间缺乏不变性。
2. **神经渲染方法**虽然引入了3D归纳偏置，但其隐式潜空间对相机参数的依赖过强，泛化到新视角时需要昂贵的在线优化或重新渲染。
3. 现有视觉预训练基线（如 **3D-MVP**，Qian et al., CVPR 2025；**LIFT3D**，Jia et al., arXiv 2024；**SPA**，Zhu et al., ICLR 2025）虽然在特定基准上取得进展，但均未从根本上解决“单视角观测→跨视角鲁棒表征”这一核心挑战。

实验证据直接印证了这一瓶颈：在专门设计的视角泛化测试集 **Mv-Bench** 上，当前最强的视觉‑语言‑动作模型 **OpenVLA**（Kim et al., CoRL 2025）平均成功率仅为39.3%，而视角偏移下性能下降近20个百分点——这暴露了现有方法在视角鲁棒性上的系统性脆弱。

### 本文动机：从多视角生成中学习3D感知

本文的核心洞察在于：**如果模型能够在给定源观测和相机位姿的条件下生成逼真的目标视图，那么其内部必然已经隐式恢复了场景几何并建立了跨视图对应关系**。这种能力恰恰是视角鲁棒操作策略所需的基础。

基于此，DiffuView 提出将**多视角扩散模型**作为视觉预训练骨干，其生成目标形式化为：

$$p _ { \theta } ( \hat { O } _ { j } \mid O _ { i } , P _ { i } , P _ { j } )$$

与 MAE 的掩码重建和神经渲染的隐式3D提升不同，多视角扩散生成迫使网络在去噪过程中学习像素级的几何对应——因为只有正确推断源视图与目标视图之间的空间变换关系，才能生成几何一致的目标视图。一旦预训练完成，这个扩散UNet骨干便可作为3D感知的视觉编码器，仅需单次前向传播即可提取富含几何信息的特征，为下游扩散策略（如 **Diffusion Policy**，Reuss et al., RSS 2024）提供视角鲁棒的观测表征。

这一设计实现了关键突破：**部署时仅需单视角观测，即可通过预训练学到的几何先验实现跨视角泛化**，从根本上解决了传统方法对固定相机配置的依赖。

## 核心创新

DiffuView 的核心创新在于将**多视角扩散模型**引入机器人视觉表征预训练，从根本上改变了视觉特征与3D几何的交互方式。与现有范式相比，其关键改动可归结为以下四个维度。

### 1. 视觉预训练范式：从掩码重建到多视角扩散生成

现有机器人视觉预训练主要依赖两类范式：**掩码自编码器（MAE）** 通过重建被遮掩的图像区域学习2D统计特征（如 MVP，Xiao et al., arXiv 2022），以及**神经渲染方法**（如 GNFactor，Ze et al., CoRL 2023）将2D观测提升至隐式3D潜空间再渲染新视图。前者缺乏显式3D几何建模，后者则依赖隐式潜空间的质量且难以保证跨视角一致性。

DiffuView 将预训练目标重新定义为条件生成问题：

$$p _ { \theta } ( \hat { O } _ { j } \mid O _ { i } , P _ { i } , P _ { j } )$$

模型在源观测 $O_i$ 和相机位姿 $P_i, P_j$ 的条件下生成目标视图 $\hat{O}_j$。这一范式迫使网络隐式恢复场景几何并强制视图间一致性，从而学习到**3D感知的视觉表征**。相比于 MAE 的 $p _ { \theta } ( \hat { O } _ { i } \mid O _ { i } [ m ] )$ 或神经渲染的 $p _ { \theta } ( V \mid O _ { i } , P _ { i } )$，扩散生成直接建模跨视角的像素级对应关系，为下游策略提供了几何鲁棒的视觉基础。

### 2. 视觉特征提取器：从2D编码器到预训练扩散UNet骨干

传统方法通常使用2D ViT/CNN 编码器或显式3D潜变量作为特征提取器。DiffuView 在预训练完成后，**将扩散UNet重定向为3D感知的视觉编码器**——仅执行单次扩散前向传播提取多尺度特征，不再进行迭代去噪。这一设计使得同一网络在预训练阶段学习几何对应，在策略学习阶段则作为高效的特征提取骨干，实现了预训练与下游任务的紧密耦合。

### 3. 策略网络结构：FiLM条件的Q-Former与噪声条件MoE扩散Transformer

在策略学习阶段，DiffuView 引入了三个关键组件：

- **FiLM条件的Q-Former**：通过CLIP文本嵌入的FiLM调节，将多尺度视觉特征压缩为紧凑的观测嵌入，使提取的特征受语言指令的语义意图调制，实现任务相关特征对齐。
- **噪声条件MoE扩散Transformer**：每个Transformer块内包含4个专家，通过噪声条件路由稀疏激活Top-2专家。消融实验表明，将激活专家数从Top-2降至Top-1会导致成功率从89.2降至87.7，验证了多专家稀疏激活对去噪质量的增益。
- **动作因果自注意力**：确保动作序列生成的时间一致性。

### 4. 视角泛化机制：从固定相机到单视角输入的视角自适应

现有方法通常假设训练和测试时的相机配置固定不变，视角偏移会导致策略性能急剧下降。DiffuView 的预训练模型在推理时充当**视角自适应模块**，能够将源视角观测隐式变换至目标视角，使策略仅需单视角输入即可适应部署时的视角变化。在 Mv-Bench 视角泛化测试上，DiffuView 平均成功率达到59.2，远超 OpenVLA 的39.3（+19.9个百分点），且在 −30° 至 60° 的视角变换范围内保持策略一致性。

### 创新总结

| 改动维度 | 基线方案 | DiffuView 方案 |
|---------|---------|---------------|
| 视觉预训练范式 | MAE 掩码重建 / 神经渲染 | 多视角扩散条件生成 |
| 视觉特征提取器 | 2D ViT/CNN 或显式3D潜变量 | 预训练扩散UNet单次前向传播 |
| 策略网络结构 | 标准扩散Transformer/MLP头 | FiLM Q-Former + 噪声条件MoE |
| 视角泛化机制 | 固定相机配置 | 视角自适应模块，单视角输入泛化 |

这些创新的协同效应在 Libero 100任务平均成功率92.2、MetaWorld 50任务平均成功率0.706 以及真实世界4任务平均成功率0.65 的结果中得到验证，其中机器人数据预训练、Plücker光线嵌入和FiLM语言条件被消融实验证明是性能的关键支柱。

## 整体框架

DiffuView 采用**两阶段训练范式**，将多视角扩散模型的几何推理能力迁移为机器人操作的视觉骨干。其核心设计思路是：先通过跨视角条件生成学习 3D 一致的视觉表示，再将预训练编码器嵌入扩散策略网络，实现视角鲁棒的动作预测。

### 阶段一：多视角扩散预训练

第一阶段的目标是让模型学会在给定源视角观测和相机位姿的条件下生成目标视角图像。该过程不依赖显式 3D 重建，而是通过扩散模型隐式恢复场景几何并强制跨视角一致性。如图 Figure 2（左）所示，预训练编码器接收以下输入：

![[assets/figures/papers/paper_list_l2187_https_openaccess_thecvf_com_content_CVPR2026_html_Zhang_DiffuView_Multi/figures/002_Figure_2.jpg]]
*Figure 2: (Left) Stage 1: Multi-view diffusion pretraining reconstructs target views from source observations using Plucker rays, depth, ¨ and warped RGB depth pairs to learn 3D consistent latent features. (Right) Stage 2: The pretrained backbone serves as a 3D aware encoder; a FiLM conditioned Query Transformer (Q-Former) with CLIP text guidance produces task aware tokens that condition a Mixture of Denoising Experts (MoDE) diffusion policy. A noise token η(σt) modulates attention and drives a noise conditioned router that sparsely activates experts, enabling faster inference while maintaining denoising performance*

- **源视角 RGB-D 图像** $I_i, D_i$，经 VAE 编码为潜变量 $z_{\text{source}}$；
- **目标相机位姿下的仿射视图** $(\tilde{I}_{i \to j}, \tilde{D}_{i \to j})$，由源 RGB-D 通过重投影函数 Warp 变换得到（Eq. 4）；
- **Plücker 光线嵌入** $\mathbf{E}_i, \mathbf{E}_j$，为每个像素编码完整的相机射线信息（方向向量 $\mathbf{d}$ 与矩量 $\mathbf{m}$，Eq. 5–6），注入像素级几何上下文。

源潜变量与目标潜变量分别通过 CNN 残差路径融合几何信息（Eq. 7–8），随后送入多视角扩散 UNet。该 UNet 在单个视角内执行 2D 空间注意力以捕获局部依赖，同时跨所有视角执行 3D 全注意力以推理跨视角几何对应关系。训练时，源视角数量 $N$ 在 1 到 3 之间随机变化，总视图数固定为 $N+M=8$，迫使模型在不同观测条件下学习鲁棒的 3D 表示。

预训练完成后，扩散 UNet 被冻结并重新定位为**3D 感知的视觉特征提取器**：仅执行单次前向传播（不进行迭代去噪），从多尺度中间层提取特征图，供下游策略使用。

### 阶段二：扩散策略学习

第二阶段将预训练视觉骨干与扩散行为克隆策略耦合，构建端到端的动作预测管线（Figure 2 右）。该阶段包含三个关键模块：

1. **FiLM 条件的 Q-Former**：多尺度视觉特征通过可学习查询向量压缩为紧凑的观测嵌入 $\mathbf{z}_{\text{obs}}$。同时，CLIP 文本编码器提取语言指令嵌入，经 FiLM 层对 Q-Former 的中间特征进行逐通道仿射调制，确保视觉特征与任务语义意图对齐。

2. **噪声条件 MoE 扩散 Transformer**：策略网络采用 8 层 Transformer（潜维度 768），每个 Transformer 块内嵌混合专家（MoE）设计，共 4 个专家。噪声令牌 $\eta(\sigma_t)$ 调制注意力并驱动噪声条件路由器，稀疏激活 Top-2 专家，在保持去噪质量的同时加速推理。

3. **动作因果自注意力与去噪**：输入包含 2 帧单视角观测和语言嵌入，输出动作块长度为 10。训练时，干净动作 $\mathbf{a}_0$ 按累积噪声调度逐步添加高斯噪声（Eq. 9），策略网络学习预测添加的噪声 $\varepsilon$，损失函数为真实噪声与预测噪声的均方误差（Eq. 10）。推理时，从纯噪声出发迭代去噪，生成连续动作序列。

### 视角自适应推理机制

DiffuView 的关键创新在于预训练模型在推理阶段承担**双重角色**：训练时作为固定特征提取器，推理时作为**视角自适应模块**。当部署视角与训练视角不一致时，模型利用多视角扩散预训练中习得的几何对应关系，将源视角观测隐式变换至目标视角，使策略在仅需单视角输入的情况下仍能保持鲁棒性。Figure 4 的实验结果表明，该机制在 −30° 至 60° 的视角偏移范围内均能有效维持操作一致性。

### 补充图表

![[assets/figures/papers/paper_list_l2187_https_openaccess_thecvf_com_content_CVPR2026_html_Zhang_DiffuView_Multi/figures/001_Figure_1.jpg]]
*Figure 1: Comparison of visual representation learning paradigms for robotic manipulation. (a) MAE based methods learn visual representations by reconstructing masked regions from observations. (b) 3D reconstruction methods lift 2D observation features into implicit 3D latent spaces through neural rendering. (c) Our method leverages a multi view diffusion model that learns 3D consistent and geometry aware representations by generating novel target views conditioned on source observations and camera poses, enabling unified and view robust visual understanding for downstream manipulation tasks*

## 核心模块与公式推导

### 阶段一：多视角扩散预训练

DiffuView 的第一阶段旨在通过条件生成任务，迫使视觉编码器学习跨视角的 3D 一致表示。核心思想是：给定源视角观测 $O_i$ 及其相机位姿 $P_i$，以及目标相机位姿 $P_j$，模型学习生成目标视角的观测 $\hat{O}_j$。这一过程可形式化为条件概率分布：

$$p _ { \theta } ( \hat { O } _ { j } \mid O _ { i } , P _ { i } , P _ { j } )$$

该目标与传统的掩码自编码器（MAE）和神经渲染方法形成根本区别：MAE 仅重建被掩码的自身区域，其概率目标为 $p _ { \theta } ( \hat { O } _ { i } \mid O _ { i } [ m ] )$；神经渲染则将 2D 观测提升至隐式 3D 潜空间 $V$ 后再渲染新视图，即 $p _ { \theta } ( V \mid O _ { i } , P _ { i } )$ 且 $\hat { O } = f _ { \phi } ( V , P )$。DiffuView 直接在像素空间（潜空间）进行跨视角生成，隐式恢复场景几何，避免了显式 3D 重建的中间瓶颈。

#### 几何信息注入：仿射与 Plücker 光线

为提供精确的跨视角对应线索，DiffuView 注入两类几何先验：

**仿射 RGB-D 对**：利用已知的相机内参 $K_i, K_j$ 和深度 $D_i$，将源视角的 RGB-D 重投影至目标相机坐标系，生成对齐的仿射视图：

$$( \tilde { I } _ { i \to j } , \tilde { D } _ { i \to j } ) = \mathrm { W a r p } ( I _ { i } , D _ { i } , P _ { i } , P _ { j } , K _ { i } , K _ { j } )$$

该仿射对为目标视图生成提供了强几何先验，尤其在视差较大时，能显著降低扩散模型的生成难度。

**Plücker 光线嵌入**：为每个像素编码完整的相机射线信息。对于像素 $(x,y)$，其观测方向向量 $\mathbf{d}_{i,xy}$ 与相机光心 $\mathbf{o}_i$ 构成 Plücker 坐标：

$$\mathbf { r } _ { i , x y } = \langle \mathbf { d } _ { i , x y } , \ \mathbf { m } _ { i , x y } \rangle , \qquad \mathbf { m } _ { i , x y } = \mathbf { o } _ { i } \times \mathbf { d } _ { i , x y }$$

其中 $\mathbf{m}_{i,xy}$ 为矩量（moment），编码射线相对于原点的空间位置。将方向与矩量拼接，得到逐像素的 6 维密集嵌入：

$$\mathbf { e } _ { i , x y } = \left[ \mathbf { d } _ { i , x y } \ ; \ \mathbf { m } _ { i , x y } \right] \in \mathbb { R } ^ { 6 }$$

所有像素的嵌入构成几何上下文张量 $\mathbf{E}_i$，与 RGB 和深度一同输入条件编码器。

#### 潜变量条件注入

扩散过程在 VAE 潜空间中进行。源视角和目标视角的潜变量分别注入几何残差：

源潜变量结合原始 RGB、深度和相机嵌入：
$$z _ { \mathrm { s o u r c e } } = \mathcal { E } ( I _ { i } ) + \mathrm { C N N } ( I _ { i } , D _ { i } , \mathbf { E } _ { i } )$$

目标潜变量结合仿射 RGB-D 和目标相机嵌入：
$$z _ { \mathrm { t a r g e t } } = \mathcal { E } ( I _ { j } ) + \mathrm { C N N } ( \tilde { I } _ { i  j } , \tilde { D } _ { i  j } , \mathbf { E } _ { j } )$$

其中 $\mathcal{E}$ 为冻结的 VAE 编码器，CNN 学习几何残差。这种设计使扩散 UNet 在去噪时能同时感知源视角的几何上下文和目标视角的仿射先验，有效引导跨视角生成。

### 阶段二：扩散策略学习

预训练完成后，扩散 UNet 被重新用作 3D 感知的视觉编码器，仅执行单次前向传播（不进行去噪），提取多尺度特征。这些特征经 FiLM 条件的 Q-Former 压缩为紧凑的观测嵌入 $\mathbf{z}_{\mathrm{obs}}$，再送入 MoDE 扩散策略网络生成动作序列。

#### 动作扩散过程

策略网络采用扩散行为克隆范式。给定干净动作序列 $\mathbf{a}_0$，按累积噪声调度逐步添加高斯噪声：

$$\mathbf { a } ^ { ( t ) } = \sqrt { \bar { \alpha } _ { t } } \mathbf { a } _ { 0 } + \sqrt { 1 - \bar { \alpha } _ { t } } \varepsilon , \quad \varepsilon \sim \mathcal { N } ( \mathbf { 0 } , \mathbf { I } ) , \quad t \in \{ 1 , ... , T \}$$

其中 $\bar{\alpha}_t$ 为累积噪声系数，$T$ 为总去噪步数。策略网络 $\varepsilon_\psi$ 以噪声动作 $\mathbf{a}^{(t)}$、去噪步 $t$、观测嵌入 $\mathbf{z}_{\mathrm{obs}}$ 和语言嵌入 $l_{emb}$ 为条件，预测所添加的噪声 $\varepsilon$。

#### 策略损失函数

训练目标为最小化真实噪声与预测噪声的均方误差：

$$\mathcal { L } _ { \mathrm { p o l i c y } } = \mathbb { E } _ { ( \mathbf { a } _ { 0 } , \mathbf { z } _ { \mathrm { o b s } } , \mathbf { l } ) , t , \varepsilon } \left[ \left| \left| \varepsilon - \varepsilon _ { \psi } \left( \mathbf { a } ^ { ( t ) } , t , \mathbf { z } _ { \mathrm { o b s } } , l _ { e m b } \right) \right| \right| ^ { 2 } \right]$$

该损失约束策略网络在给定观测和语言指令的条件下，精确恢复去噪方向，从而在推理时通过迭代去噪生成连续动作序列。

### 关键模块协同机制

整个框架的核心模块形成清晰的因果链条：**Plücker 光线嵌入**提供像素级相机几何，使扩散 UNet 在预训练阶段学习精确的跨视角对应；**仿射 RGB-D 对**降低大视差下的生成难度，加速收敛；**Q-Former with FiLM** 将视觉特征与 CLIP 语言嵌入对齐，使下游策略能感知任务语义；**MoDE 扩散策略**通过噪声条件路由稀疏激活专家，在保持去噪质量的同时提升推理效率。消融实验（Table 5）定量验证了各模块的贡献：移除 Plücker 嵌入使成功率从 89.2 降至 76.2，移除 FiLM 条件降至 73.3，将 MoE 专家激活数从 Top-2 减为 Top-1 降至 87.7。

## 实验与分析

### 实验设置

DiffuView采用两阶段训练范式。预训练阶段，模型在约100个来自RH20T的真实机器人任务多视角序列上进行微调，同时辅以仿真环境中随机采样的超过5,000个相机视角的渲染数据，以增强视角多样性。微调使用8块NVIDIA A100 GPU，耗时约2天。策略学习阶段，多任务动作学习框架采用8层Transformer块，隐变量维度为768，输入为单一视角的2帧观测图像及CLIP语言嵌入，输出动作块大小为10。噪声条件模块采用MoE设计，每个Transformer块包含4个专家，推理时激活Top-2专家。所有仿真评估均使用标准成功率指标，每个任务多次试验取平均以保证统计稳定性。

### 仿真基准实验结果

**Libero Benchmark**：如表1所示，DiffuView在Libero 10上达到89.2的成功率，在Libero 90上达到92.5，在包含100个任务的Libero平均成功率上达到92.2，全面超越所有视觉预训练基线（MVP、3D-MVP、LIFT3D、GNFactor、SPA、PDFactor）和策略基线（DP、OpenVLA）。

**MetaWorld Benchmark**：如表2所示，DiffuView在50个任务的MetaWorld基准上取得0.706的平均成功率，显著优于对比方法。该结果验证了多视角扩散预训练在不同操作场景下的泛化能力。

### 视角泛化实验

**Mv-Bench测试**：为专门评估视角自适应能力，作者构建了Mv-Bench基准，在不同视角角度下测试策略鲁棒性。如表3所示，DiffuView在Mv-Bench上平均成功率达到59.2，远超OpenVLA的39.3，提升近20个百分点。图4进一步展示了视角自适应模块的效果，模型在−30°至60°的视角变换范围内均能保持策略一致性，验证了多视角扩散预训练赋予的跨视角几何对应能力。

### 真实世界实验

在包含4个操作任务的真实世界评估中（表4），DiffuView取得0.65的平均成功率，优于DP（0.51）和OpenVLA（0.63）。图5展示了DiffuView在真实场景中的成功执行案例及实验设置。图6和图7分别展示了腕部相机视角生成与跨视角泛化定性结果，以及真实世界多视角扩散生成质量，进一步验证了模型在真实传感器条件下的几何感知与视角鲁棒性。

### 消融实验

表5的系统消融揭示了各组件的关键贡献：

- **移除机器人数据预训练**（仅依赖通用多视角数据）：成功率从89.2骤降至63.3，表明在机器人操作数据上的跨域微调对适应下游任务至关重要。
- **移除Plücker光线嵌入**：成功率降至76.2，说明显式的像素级相机几何信息（方向向量与矩量）对空间理解和跨视角对应具有显著增益。
- **移除Q-Former中的FiLM语言条件**：成功率降至73.3，验证了通过CLIP文本嵌入调制视觉特征、实现任务语义对齐的有效性。
- **将MoE激活专家数从Top-2减为Top-1**：成功率下降至87.7，表明多专家稀疏激活有助于提升去噪质量和策略精度。

### 失败模式与局限性

尽管DiffuView在视角鲁棒性上表现突出，其当前设计仍存在以下局限：

1. **缺乏时间动态建模**：多视角扩散预训练仅针对空间视角变化，未显式建模时间维度上的运动连续性与时序依赖，限制了在高度动态或快速变化环境中的推理能力。
2. **对几何先验的依赖**：框架依赖精确的相机位姿和深度估计。若位姿噪声较大或深度不可靠，仿射视图质量下降，可能影响生成效果与策略性能，但具体衰减程度尚需进一步量化验证。
3. **单源视图的信息瓶颈**：在极端视角偏移或严重遮挡场景下，单张源视图可能不足以提供充分的几何线索，导致目标视图生成质量下降。

### 开放问题

- 如何将时间序列建模（如视频扩散）与多视角空间预训练统一，实现时空一致的3D感知？
- DiffuView能否在更复杂的长期操作任务、多机器人协作或人机交互场景中保持视角鲁棒性？
- 在不显著增加推理延迟的前提下，如何通过更轻量的注意力机制进一步提升视角自适应模块的效率？

### 补充图表

![[assets/figures/papers/paper_list_l2187_https_openaccess_thecvf_com_content_CVPR2026_html_Zhang_DiffuView_Multi/figures/004_Table_1.jpg]]
*Table 1: Quantitative results on Libero Benchmark*

![[assets/figures/papers/paper_list_l2187_https_openaccess_thecvf_com_content_CVPR2026_html_Zhang_DiffuView_Multi/figures/005_Table_2.jpg]]
*Table 2: Quantitative results on MetaWorld Benchmark*

![[assets/figures/papers/paper_list_l2187_https_openaccess_thecvf_com_content_CVPR2026_html_Zhang_DiffuView_Multi/figures/006_Table_3.jpg]]
*Table 3: Mv-bench results*

![[assets/figures/papers/paper_list_l2187_https_openaccess_thecvf_com_content_CVPR2026_html_Zhang_DiffuView_Multi/figures/007_Figure_4.jpg]]
*Figure 4: This figure illustrates the effect of our pretrained model serving as a view-adaptive module. The results herein demonstrate that our approach competently handles view transformation within −30◦ ∼ 60◦*

![[assets/figures/papers/paper_list_l2187_https_openaccess_thecvf_com_content_CVPR2026_html_Zhang_DiffuView_Multi/figures/008_Table_4.jpg]]
*Table 4: Real world experiment results on success rate*

![[assets/figures/papers/paper_list_l2187_https_openaccess_thecvf_com_content_CVPR2026_html_Zhang_DiffuView_Multi/figures/009_Table_5.jpg]]
*Table 5: Ablation Results*

![[assets/figures/papers/paper_list_l2187_https_openaccess_thecvf_com_content_CVPR2026_html_Zhang_DiffuView_Multi/figures/003_Figure_3.jpg]]
*Figure 3: Simulation benchmarks. We conducted our experiments on two established benchmarks, LIBERO and MetaWorld, as shown in (a) and (b), respectively. These benchmarks collectively encompass a diverse array of manipulation tasks with varying levels of difficulty and complexity. Furthermore, we also conducted experiments on our self-formulated benchmark, Mv-Bench, which is specifically designed to evaluate the view adaptive capability of our method, as illustrated in (c)*

![[assets/figures/papers/paper_list_l2187_https_openaccess_thecvf_com_content_CVPR2026_html_Zhang_DiffuView_Multi/figures/010_Figure_5.jpg]]
*Figure 5: Successful rollouts of DiffuView (left) and real world set-up (right). The image illustrates the robotic arm performing various manipulation tasks, showcasing the real-time execution of the DiffuView model*

![[assets/figures/papers/paper_list_l2187_https_openaccess_thecvf_com_content_CVPR2026_html_Zhang_DiffuView_Multi/figures/012_Figure_7.jpg]]
*Figure 7: Qualitative Results of Real-World Multi-View Diffusion*

## 方法谱系与知识库定位

### 1. 视觉表征范式演进：从掩码重建到多视角扩散

机器人操作中的视觉表征学习长期围绕一个核心瓶颈展开：**如何在多变视角和传感器配置下学习统一的3D一致性表示**。现有方法大致沿两条技术路线演进：

**掩码自编码器路线** 以 **MVP**（Xiao et al., arXiv 2022）为代表，通过重建被掩码的图像区域来学习视觉特征。其概率目标为 $p _ { \theta } ( \hat { O } _ { i } \mid O _ { i } [ m ] )$，即从部分观测中恢复完整视图。该范式在固定相机配置下表现良好，但学习到的表征本质上仍是2D统计规律，缺乏显式的跨视角几何约束。当测试视角与训练视角发生偏移时，模型无法推理场景的三维结构，导致策略性能急剧退化。

**神经渲染路线** 尝试弥补这一缺陷。**GNFactor**（Ze et al., CoRL 2023）将2D观测提升至隐式3D神经特征场，通过体渲染生成新视图，其概率映射为 $p _ { \theta } ( V \mid O _ { i } , P _ { i } )$，其中 $\hat{O} = f _ { \phi } ( V , P )$。**SPA**（Zhu et al., ICLR 2025）则通过3D空间感知ViT编码器显式建模空间关系。**3D-MVP**（Qian et al., CVPR 2025）将MAE扩展至多视角设置，在3D空间中执行掩码重建。然而，这些方法要么依赖昂贵的逐场景优化，要么在视角泛化时仍受限于训练视角的覆盖范围。

**DiffuView的方法论跃迁** 在于将视觉预训练从“重建”范式切换为“条件生成”范式。其核心概率模型为 $p _ { \theta } ( \hat { O } _ { j } \mid O _ { i } , P _ { i } , P _ { j } )$，即在源观测和相机位姿条件下生成目标视图。这一设计的关键洞察是：**多视角扩散模型在生成过程中必须隐式恢复场景几何并强制视图一致性，从而自然习得跨视角的几何对应关系**。与MAE的局部重建和神经渲染的显式3D建模不同，扩散生成提供了一个更灵活的表征学习信号——模型无需显式定义3D表示，而是通过去噪过程学习一个蕴含几何信息的隐空间。

### 2. 策略学习范式的对比定位

在策略学习层面，DiffuView与两类基线形成对比：

**端到端视觉‑语言‑动作模型** 以 **OpenVLA**（Kim et al., CoRL 2025）为代表，将视觉编码、语言理解和动作生成统一为单一模型。然而，这类模型通常在大规模互联网数据上预训练，缺乏机器人操作特有的3D几何先验，导致视角偏移时性能显著下降（Mv-Bench平均成功率仅39.3，DiffuView为59.2）。

**扩散行为克隆方法** 以 **Diffusion Policy**（Reuss et al., RSS 2024）为典型，将动作生成建模为条件去噪过程。DiffuView继承了这一框架，但引入了三个关键改进：(1) 以预训练的多视角扩散UNet替代标准2D编码器作为视觉骨干；(2) 通过FiLM条件的Q-Former将CLIP语言嵌入注入视觉特征，实现任务相关调制；(3) 采用噪声条件MoE扩散Transformer，以Top-2稀疏专家激活替代全连接去噪，在保持去噪质量的同时降低推理延迟。消融实验表明，移除FiLM条件使成功率从89.2降至73.3，验证了语言调制对策略学习的有效性。

**3D感知策略方法** 如 **LIFT3D**（Jia et al., arXiv 2024）和 **PDFactor**（Tian et al., CVPR 2025），分别通过2D基础模型提升至3D和基于三平面的扩散策略来增强空间感知。DiffuView的差异化优势在于：预训练阶段的多视角扩散学习使得视觉编码器本身即具备3D感知能力，策略网络无需额外设计3D推理模块，从而保持了架构的简洁性和迁移效率。

### 3. 技术组件的增量贡献

消融实验（Table 5）揭示了DiffuView各组件的因果贡献：

- **机器人数据预训练**（成功率从63.3提升至89.2）：仅使用通用多视角数据预训练而跳过机器人领域微调，模型无法适应操作任务的特定视觉分布，表明跨域微调对弥合通用3D感知与任务相关特征之间的鸿沟至关重要。
- **Plücker光线嵌入**（成功率从76.2提升至89.2）：该组件为每个像素注入完整的相机射线信息（方向向量 $\mathbf{d}_{i,xy}$ 与矩量 $\mathbf{m}_{i,xy} = \mathbf{o}_i \times \mathbf{d}_{i,xy}$），形成6D几何上下文张量 $\mathbf{e}_{i,xy} = [\mathbf{d}_{i,xy}; \mathbf{m}_{i,xy}] \in \mathbb{R}^6$。移除该嵌入后模型缺少显式相机几何信息，跨视角对应能力显著退化。
- **噪声条件MoE**（Top-2 vs Top-1专家激活，成功率从87.7提升至89.2）：多专家稀疏激活机制使去噪网络能够根据噪声水平动态选择专家组合，相比单专家模式提供了更精细的去噪能力。

### 4. 适用边界与局限

DiffuView的适用边界由以下约束定义：

1. **静态场景假设**：多视角扩散预训练仅针对空间视角变化建模，缺乏对动态时间信息的显式处理。在高度动态或快速变化的环境中，单张源视图可能不足以提供充分的几何线索，导致目标视图生成质量下降。
2. **位姿与深度依赖**：框架依赖精确的相机位姿 $P_i, P_j$ 和深度图 $D_i$ 进行仿射变换（Warp函数，Eq. 4）和Plücker嵌入计算。若位姿噪声较大或深度估计不可靠，几何条件注入的准确性将受损，性能衰减程度尚待系统评估。
3. **计算资源需求**：预训练数据集包含约100个RH20T真实机器人任务及仿真渲染的5,000+随机视角，微调阶段需8块NVIDIA A100 GPU耗时约2天。虽然与SPA、GNFactor等基线相当，但在资源受限场景下的部署可行性需进一步验证。

### 5. 开放问题与未来方向

1. **时空统一建模**：如何将时间序列建模（如视频扩散模型）与多视角空间预训练统一，实现时空一致的3D感知，从而提升对运动连续性和时序依赖的推理能力？
2. **复杂场景泛化**：DiffuView能否在长期操作任务、多机器人协作或人机交互场景中保持视角鲁棒性？当前评估局限于单臂操作，扩展到更复杂的交互场景需要验证。
3. **推理效率优化**：在不显著增加推理延迟的前提下，能否通过更轻量的注意力机制或知识蒸馏进一步提升视角自适应模块的效率？
4. **位姿鲁棒性**：当前框架假设精确的相机位姿；在位姿噪声较大或深度不可靠的条件下，性能衰减的定量特征和容错边界需要系统研究。

## 原文 PDF

![[paperPDFs/CVPR_2026/DiffuView_Multi_View_Diffusion_Pretraining_for_3D_Aware_Robotic_Manipulation.pdf]]