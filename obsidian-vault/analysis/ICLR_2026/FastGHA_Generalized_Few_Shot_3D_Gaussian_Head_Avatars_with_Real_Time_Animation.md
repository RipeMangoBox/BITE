---
title: "FastGHA: Generalized Few-Shot 3D Gaussian Head Avatars with Real-Time Animation"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/FastGHA_Generalized_Few_Shot_3D_Gaussian_Head_Avatars_with_Real_Time_Animation_b897e4f1e33f.pdf
project_link: null
code_link: null
aliases:
- FastGHA
tags:
- ICLR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/image_and_video_generation
- topic/vision_multimodal_applications/3d_rendering_reconstruction
core_operator: 将表情驱动从交叉注意力替换为轻量级逐点MLP变形网络，并将VGGT几何先验从输入特征变为正则化损失，从而解耦表情建模与几何监督。
primary_logic: 前馈重建一个不含表情的“规范”高斯表示，再通过一个独立作用于每个高斯点的轻量MLP，根据FLAME表情码预测属性偏移，可在获得高保真重建的同时实现实时动画。
claims:
- FastGHA在所有指标上均优于基线方法，且动画速度高达62FPS（4视图输入），而Avat3r仅8FPS。
- 消融实验证明移除VAE预训练权重、几何损失L_geo、每高斯特征或替换DINOv3均导致质量显著下降。
- Ava-256 上 PSNR↑ = 22.5 (Ours both)
- Ava-256 上 SSIM↑ = 0.77 (Ours both)
---

# FastGHA: Generalized Few-Shot 3D Gaussian Head Avatars with Real-Time Animation

> [!tip] 核心洞察
> 前馈重建一个不含表情的“规范”高斯表示，再通过一个独立作用于每个高斯点的轻量MLP，根据FLAME表情码预测属性偏移，可在获得高保真重建的同时实现实时动画。

| 字段 | 内容 |
|------|------|
| 中文题名 | FastGHA: 泛化少样本3D高斯头像与实时动画 |
| 英文题名 | FastGHA: Generalized Few-Shot 3D Gaussian Head Avatars with Real-Time Animation |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=E7VL9Zl1Nc) · [paper](https://arxiv.org/abs/2505.00615) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/image_and_video_generation #topic/vision_multimodal_applications/3d_rendering_reconstruction |
| Method | FastGHA |
| Dataset | Ava-256, Nersemble |

> [!tip] 效果简介
> - Ava-256 上，PSNR↑ 22.5 (Ours both) vs 20.7 (Avat3r) (+1.8)；SSIM↑ 0.77 (Ours both) vs 0.71 (Avat3r) (+0.06)；LPIPS↓ 0.23 (Ours both) vs 0.33 (Avat3r) (-0.10)。
> - Nersemble 上，PSNR↑ 24.0 (Ours both) vs 20.8 (GPAvatar) (+3.2)；SSIM↑ 0.81 (Ours both) vs 0.76 (GPAvatar) (+0.05)；LPIPS↓ 0.24 (Ours both) vs 0.30 (GPAvatar) (-0.06)。

## 概要

**问题瓶颈**：现有前馈式3D高斯头像方法（如Avat3r）将表情参数直接注入交叉注意力模块，导致动画推理速度慢（仅8 FPS）；同时VGGT几何先验以跳跃连接形式直接作为网络输入，引入不准确的几何信息，限制了重建保真度。

**核心思路**：FastGHA提出“先重建规范头像，再轻量变形”的两阶段范式——从前馈重建一个不含表情的“规范”高斯表示，再通过一个独立作用于每个高斯点的轻量MLP，根据FLAME表情码预测属性偏移。这一设计将表情驱动从交叉注意力替换为逐点MLP变形网络，并将VGGT几何先验从输入特征变为正则化损失，从而解耦表情建模与几何监督。

**方法定位**：FastGHA属于泛化少样本3D高斯头像重建与实时动画框架。其技术路线与Avat3r（Kirschstein et al., CVPR 2025）同属像素级高斯回归范式，但在动画架构和几何先验使用方式上做出关键改变；同时区别于GPAvatar（Chu et al., 2024）的三平面表示与FLAME点云先验路线，以及GAGAvatar（Chu & Harada, 2024）、LAM（He et al., 2025）等单样本3D感知重建方法。

**主要结果**：FastGHA在所有指标上均优于基线方法——在Ava-256数据集上PSNR达22.5（Avat3r为20.7），LPIPS降至0.23（Avat3r为0.33）；在Nersemble数据集上PSNR达24.0（GPAvatar为20.8）。动画速度达62 FPS（4视图输入），较Avat3r的8 FPS提升近8倍。消融实验证实，预训练VAE权重、几何损失、每高斯特征和DINOv3语义编码器均为关键设计要素，移除任一项均导致质量显著下降。



### 问题背景：从少样本图像重建可动画的3D头像

高质量、可实时驱动的3D头像重建是计算机视觉与图形学中的核心问题，在虚拟现实、远程通信和数字人等领域有广泛应用。传统方法通常依赖多视图立体匹配或昂贵的光场采集设备，难以在消费级场景中推广。近年来，3D高斯泼溅（3D Gaussian Splatting, 3DGS）的兴起为高效、高保真的场景重建提供了新的技术路线，而前馈式（feed-forward）方法则试图通过神经网络直接从少量输入图像中推理3D表示，避免逐实例优化，从而在泛化性和推理速度上取得突破。

在头像重建领域，现有前馈式方法（如**Avat3r**，Kirschstein et al., CVPR 2025）已开始采用像素级高斯回归策略，从多视图输入直接预测3D高斯属性。然而，这类方法面临两个核心瓶颈：**动画推理效率低**和**几何先验使用不当**，限制了其在实际应用中的部署。

### 现有方法的瓶颈：动画速度与几何先验的矛盾

**动画机制的效率瓶颈。** Avat3r将表情参数直接注入交叉注意力（cross-attention）模块，使其与多视图特征进行融合。这种设计虽然理论上能够建模表情与外观的复杂交互，但交叉注意力的计算开销极大，导致动画推理速度仅为8 FPS，远未达到实时交互的要求（通常需≥30 FPS）。对于需要流畅动画的应用场景（如实时对话头像），这一速度是不可接受的。

**几何先验的使用方式存在缺陷。** VGGT等预训练几何模型能够从图像中预测点云或深度图，为3D重建提供有价值的几何先验。然而，Avat3r将VGGT预测的点图通过跳跃连接（skip connection）直接作为网络输入特征。这种方式存在两个问题：其一，VGGT的预测本身存在误差，将其直接注入网络会将不准确的几何信息传播至整个重建管线；其二，在推理阶段，VGGT的几何预测误差无法被纠正，导致重建保真度受限。

### 本文动机：解耦规范重建与表情驱动

针对上述瓶颈，本文提出**FastGHA**，核心动机在于将“规范头像重建”与“表情驱动动画”解耦为两个独立阶段：

1. **规范重建阶段**：从多视图输入中重建一个不含表情的“规范”（canonical）3D高斯头像。该阶段专注于几何与外观的准确恢复，不受表情参数的干扰。
2. **表情驱动阶段**：通过一个轻量级、独立作用于每个高斯点的MLP变形网络，根据FLAME表情码预测位置与颜色的逐点偏移，实现动画。

这一解耦设计的优势在于：动画网络无需处理复杂的多视图特征融合，仅需学习表情到形变的映射，从而大幅降低计算量；同时，规范重建可以专注于从多视图中提取准确的3D信息，不受表情变化的影响。

此外，FastGHA改变了几何先验的使用方式：VGGT点图不再作为网络输入，而是转化为训练时的正则化损失（$L_{geo}$），监督渲染深度与VGGT预测深度的一致性。这避免了推理阶段的误差传播，同时保留了几何先验对训练过程的约束作用。

综上，FastGHA的设计动机可以概括为：通过架构解耦和先验重构，在保持高保真重建的同时实现实时动画，解决现有前馈式3D高斯头像方法在效率与精度之间的权衡困境。



## 核心方法与创新机理

FastGHA 的核心创新在于对前馈式 3D 高斯头像重建与动画管线的两个关键环节进行了根本性重构，将此前相互耦合的“表情驱动”与“几何先验利用”解耦为独立、高效的模块。

### 1. 从交叉注意力到逐点 MLP 的表情驱动范式转变

现有前馈式方法（如 **Avat3r** (Kirschstein et al., CVPR 2025)）将 FLAME 表情参数直接注入交叉注意力模块，使其参与多视图特征融合过程。这种设计导致动画推理时需重复运行注意力计算，速度仅为 8 FPS，严重制约实时应用。

FastGHA 提出了一种**两阶段解耦策略**：
1. **规范重建阶段**：前馈网络仅从输入图像重建一个不含表情的“规范” 3D 高斯头像 $\mathcal{G}_f^c$，其中每个高斯点携带一个额外的逐点特征 $\mathbf{f} \in \mathbb{R}^{32}$（Equation 2）。
2. **动画变形阶段**：引入一个轻量级 MLP 变形网络 $\mathcal{D}$，独立作用于每个高斯点，根据 FLAME 表情码 $\mathbf{z}_{exp}$ 预测位置和颜色的偏移量：

$$\delta_{\mathbf{z}} = \mathcal{D}(\mathcal{G}_f^c, \mathbf{z}_{exp})$$

该 MLP 的输入包括规范高斯的位置编码、颜色、逐点特征以及表情码，输出为位置偏移 $\delta_{\mathbf{X}}$ 和颜色偏移 $\delta_{\mathbf{C}}$。由于 $\mathcal{D}$ 对每个高斯点独立操作，无需跨点注意力计算，动画速度从 Avat3r 的 **8 FPS 跃升至 62 FPS**（4 视图输入，Table 2），实现真正意义上的实时动画。

这一范式转变的核心洞察在于：**表情变形本质上是一个逐点的局部属性调整问题，而非需要全局上下文融合的感知任务**。轻量 MLP 配合逐点高斯特征 $\mathbf{f}$ 足以编码表情驱动的细粒度形变，无需昂贵的注意力机制。

### 2. 几何先验从“输入信号”到“正则化损失”的角色转换

Avat3r 将 VGGT 预测的点图通过跳跃连接直接作为网络输入，这种设计存在两个根本性问题：
- VGGT 的几何估计本身存在误差，作为输入会传播不准确信息，限制重建保真度。
- 推理时仍需运行 VGGT，增加计算开销。

FastGHA 将 VGGT 几何先验的**使用方式从“输入特征”转变为“训练损失”**，引入几何正则化项：

$$\mathcal{L}_{geo} = ||D_{out} - D_{gt}||_1$$

其中 $D_{gt}$ 是将 VGGT 对齐点云重投影得到的深度图，$D_{out}$ 为渲染深度图。该损失仅在训练时约束 3D 几何一致性，推理阶段完全不依赖 VGGT，从而：
- **阻断误差传播**：不准确的几何估计不会进入网络前向通路。
- **提升重建质量**：消融实验证实，移除 $\mathcal{L}_{geo}$ 导致 PSNR 下降 0.14 dB，并出现 3D 不一致和伪影（Table 3: w/o L_geo PSNR 21.132 vs Ours 21.274）。

### 3. 预训练视觉先验的冻结编码策略

不同于 Avat3r 等从零训练编码器/解码器，FastGHA 采用**冻结预训练模型作为特征提取骨干**：
- **SD-Turbo VAE**（Sauer et al., 2024）：冻结编码器提取颜色特征，仅微调解码器用于高斯图回归。
- **DINOv3**（Simeoni et al., 2025）：冻结语义编码器，提供视角不变的身份和结构特征。

消融实验表明，移除 VAE 预训练权重（从头训练）导致 PSNR 下降约 0.5 dB（Table 3: w/o VAE weights PSNR 20.789 vs Ours 21.274），而替换 DINOv3 为 Sapiens 特征同样造成质量损失（PSNR 21.081），验证了预训练视觉先验对少样本泛化重建的关键作用。

### 创新点总结

| 设计维度 | 基线方法 (Avat3r) | FastGHA 创新 | 效果 |
|---------|-----------------|-------------|------|
| 表情驱动机制 | 交叉注意力融合 | 逐点 MLP 变形 | 动画速度 8→62 FPS |
| 几何先验使用 | 跳跃连接输入 | 训练正则化损失 | 阻断误差传播，PSNR +0.14 dB |
| 视觉编码器 | 从零训练 | 冻结预训练 VAE + DINOv3 | PSNR +0.5 dB |

这三项创新共同构成了 FastGHA 的技术护城河：解耦的表情变形实现实时动画，正则化的几何监督保证重建精度，冻结的预训练特征提供强泛化能力。三者协同使得 FastGHA 在 Ava-256 和 Nersemble 数据集上全面超越 Avat3r 和 GPAvatar 等基线方法（Table 1: PSNR 分别领先 +1.8 dB 和 +3.2 dB）。



FastGHA 采用两阶段流水线：首先从少样本输入图像重建一个不含表情的**规范高斯头像**，随后通过一个轻量级**变形网络**根据表情码驱动动画。其核心设计在于将表情建模与几何监督解耦——表情驱动不再嵌入交叉注意力模块，而是交由一个独立作用于每个高斯点的逐点 MLP；几何先验也不再作为网络输入，而是转化为训练时的正则化损失。

### 输入与多视图特征提取

给定 $V$ 幅任意视角、任意表情的输入图像 $\{I_i\}_{i=1}^{V}$，以及对应的相机参数和 FLAME 表情码，系统首先使用两个冻结的预训练模型提取多视图特征（Figure 2 左侧）：

![[assets/figures/papers/paper_list_l80_https_openreview_net_forum_id_E7VL9Zl1Nc/figures/002_Figure_2.jpg]]
*Figure 2: Overview of our method. Given a few input images with arbitrary views and expressions, we first extract multi-view features with pre-trained models and then train a multi-view transformer network that projects these features into 3D to reconstruct a canonical Gaussian head avatar. To enable real-time animation, we introduce a lightweight MLP that deforms the Gaussians according to the expression code*

- **语义特征**：由冻结的 DINOv3 提取，提供视角不变的语义信息。
- **颜色特征**：由冻结的 SD-Turbo VAE 编码器提取，保留细粒度纹理。
- **几何线索**：将相机参数编码为 Plücker 射线坐标 $P_{cam}$，为后续多视图融合提供显式的几何对应关系。

三者在通道维度级联，形成多视图特征体 $\mathcal{V}$：

$$\mathcal{V} = [F_{dino}; F_{enc}; P_{cam}] \in \mathbb{R}^{V \times (C_d + C_e + 6) \times H_f \times W_f}$$

### 多视图变换器与高斯图解码

级联特征 $\mathcal{V}$ 送入一个基于 Vision Transformer 的**多视图变换器**（Figure 2 中部），通过自注意力层融合多视图信息，隐式建模视图间的几何对应关系。变换器输出的特征随后被送入**高斯图解码器**——一个扩展的 SD-Turbo VAE 解码器（微调训练），为每个像素回归一组 3D 高斯属性：

$$\mathcal{G}_f = \{\mathbf{X}, \mathbf{C}, \mathbf{Q}, \mathbf{S}, \alpha\} \cup \{\mathbf{f}\}$$

其中 $\mathbf{X}$ 为位置，$\mathbf{C}$ 为颜色，$\mathbf{Q}$ 为旋转四元数，$\mathbf{S}$ 为尺度，$\alpha$ 为不透明度，$\mathbf{f} \in \mathbb{R}^{32}$ 为新增的**每高斯特征**。该特征向量是后续动画变形的关键条件信号，使变形网络能够学习每个高斯点对表情变化的响应模式。

此时重建的高斯头像处于**规范空间**（canonical space），即不含任何表情偏移的基准表示。整个过程是前馈式的，无需对规范高斯进行显式监督，网络通过端到端的渲染损失自动学习将多视图信息投影为一致的 3D 表示。

### 轻量级变形网络与实时动画

动画阶段，一个轻量级 MLP $\mathcal{D}$ 独立作用于每个高斯点，根据 FLAME 表情码 $\mathbf{z}_{exp}$ 预测属性偏移（Figure 2 右侧）：

$$\delta_{\mathbf{z}} = \mathcal{D}(\mathcal{G}_f^c, \mathbf{z}_{exp})$$

具体而言，$\mathcal{D}$ 接收规范高斯的位置编码、每高斯特征 $\mathbf{f}$ 以及表情码，输出对位置 $\mathbf{X}$ 和颜色 $\mathbf{C}$ 的逐点偏移。由于该 MLP 对每个高斯点独立运算，无需跨点注意力或特征聚合，因此具有极高的并行度。变形后的高斯集合通过 3DGS 可微光栅化器 $\mathcal{R}$ 渲染为图像：

$$I = \mathcal{R}(\mathcal{G}_f^c + \delta_{\mathbf{z}}, \mu)$$

### 几何先验的正则化角色

与 Avat3r 将 VGGT 预测的点图通过跳跃连接直接注入网络不同，FastGHA 将 VGGT 几何先验**仅作为训练时的正则化损失** $\mathcal{L}_{geo}$：将对齐的点云重投影为深度图，与渲染深度图计算 L1 损失。这一设计避免了推理时因几何先验不准确而引入的误差传播，同时保留了其对 3D 一致性的约束作用。消融实验证实，移除 $\mathcal{L}_{geo}$ 会导致 PSNR 下降约 0.14 dB，并出现 3D 不一致和伪影（Table 3）。

### 训练与推理效率

整个流水线端到端训练，总损失为 RGB L1、SSIM、VGG 感知损失、轮廓损失和几何损失的加权和。训练在 4 块 H800 GPU 上约需 4 天（400k 步）。推理时，重建阶段耗时不到 1 秒；动画阶段，变形 MLP 的轻量设计使得 4 视图输入下可达 **62 FPS**，而 Avat3r 仅 8 FPS（Table 2），实现了真正的实时动画。



FastGHA 的整体流程可分解为四个关键模块：多视图特征提取、规范高斯重建、轻量级变形MLP与可微渲染。以下逐一阐述其设计逻辑与核心公式。

### 3D高斯表示与增强

基础3D高斯集合 $\mathcal{G}$ 包含位置 $\mathbf{X}$、颜色 $\mathbf{C}$、旋转四元数 $\mathbf{Q}$、尺度 $\mathbf{S}$ 和不透明度 $\alpha$，通过可微光栅化器 $\mathcal{R}$ 在给定相机参数 $\mu$ 下渲染为图像 $I$：

$$\mathcal{G} = \{\mathbf{X}, \mathbf{C}, \mathbf{Q}, \mathbf{S}, \alpha\}, \qquad I = \mathcal{R}(\mathcal{G}, \mu). \tag{1}$$

为支持后续的逐点动画变形，FastGHA 为每个高斯点附加一个可学习的特征向量 $\mathbf{f} \in \mathbb{R}^{N \times 32}$，形成增强高斯集合：

$$\mathcal{G}_f = \{\mathbf{X}, \mathbf{C}, \mathbf{Q}, \mathbf{S}, \alpha\} \cup \{\mathbf{f}\}. \tag{2}$$

该每高斯特征 $\mathbf{f}$ 是变形网络的关键输入条件，消融实验表明移除它将严重损害动画精度（PSNR从21.274降至21.053，见Table 3）。

### 多视图特征提取

给定 $V$ 幅任意视角与表情的输入图像，FastGHA 采用两个冻结的预训练模型并行提取特征：
- **SD-Turbo VAE** 编码器提取颜色特征 $F_{enc}$，保留细粒度纹理信息；
- **DINOv3** 提取语义特征 $F_{dino}$，提供稳健的形状与身份先验。

两路特征与 Plücker 射线坐标 $P_{cam}$（编码每个像素的相机射线方向）在通道维度级联，形成多视图变换器的输入潜变量：

$$\mathcal{V} = [F_{dino}; F_{enc}; P_{cam}] \in \mathbb{R}^{V \times (C_d + C_e + 6) \times H_f \times W_f}. \tag{3}$$

冻结编码器的设计避免了从零训练的不稳定性，消融实验证实：移除预训练 VAE 权重（从头训练编解码器）导致 PSNR 下降约 0.5 dB（Table 3: 20.789 vs 21.274）；替换 DINOv3 为 Sapiens 特征同样造成质量下降（21.081 vs 21.274）。

### 多视图变换器与高斯图解码器

潜变量 $\mathcal{V}$ 送入基于 Vision Transformer 的多视图自注意力网络，通过跨视图信息交互建模几何对应关系，将 2D 特征提升至 3D 空间。随后，扩展的 SD-Turbo VAE 解码器（微调）对每个输入像素回归一组高斯属性，生成规范高斯头像 $\mathcal{G}_f^c$。该规范头像不含表情，作为动画的基准状态。

### 变形MLP：表情驱动的实时动画

这是 FastGHA 实现实时动画的核心模块。给定 FLAME 表情码 $\mathbf{z}_{exp}$，一个轻量级 MLP 网络 $\mathcal{D}$ 独立作用于每个高斯点，预测其位置与颜色的偏移量：

$$\delta_{\mathbf{z}} = \mathcal{D}(\mathcal{G}_f^c, \mathbf{z}_{exp}). \tag{4}$$

$\mathcal{D}$ 的输入包含规范高斯的每高斯特征 $\mathbf{f}$、位置编码以及表情码，输出为位置偏移 $\Delta\mathbf{X}$ 和颜色偏移 $\Delta\mathbf{C}$。由于 $\mathcal{D}$ 逐点独立运算，天然支持高效并行，使得动画速度可达 62 FPS（4视图输入），远超 Avat3r 的交叉注意力动画方案（仅 8 FPS）。

### 损失函数设计

训练采用端到端方式，无需对规范高斯施加显式监督。总损失由五项加权组成：

$$\mathcal{L} = \mathcal{L}_{RGB} + \lambda_{SSIM}\mathcal{L}_{SSIM} + \lambda_{perc}\mathcal{L}_{perc} + \lambda_{sil}\mathcal{L}_{sil} + \lambda_{geo}\mathcal{L}_{geo}, \tag{8}$$

其中各项定义如下：

- **RGB重建损失**：L1 损失约束渲染图像与真值的一致性：
  $$\mathcal{L}_{RGB} = ||I_{out} - I_{gt}||_1. \tag{5}$$

- **结构相似性损失**：SSIM 损失增强局部结构保真度：
  $$\mathcal{L}_{SSIM} = SSIM(I_{out}, I_{gt}). \tag{5}$$

- **感知损失**：VGG 网络提取的多层特征差异：
  $$\mathcal{L}_{perc} = VGG(I_{out}, I_{gt}). \tag{6}$$

- **轮廓损失**：L1 损失约束渲染 Alpha 掩膜与真值掩膜：
  $$\mathcal{L}_{sil} = ||M_{out} - M_{gt}||_1. \tag{6}$$

- **几何正则化损失**：这是 FastGHA 区别于 Avat3r 的关键设计——VGGT 几何先验不再作为网络输入，而是转化为训练时的深度监督信号。将对齐的点云重投影为深度图后，施加 L1 损失：
  $$\mathcal{L}_{geo} = ||D_{out} - D_{gt}||_1. \tag{7}$$

权重配置为 $\lambda_{SSIM}=1$，$\lambda_{sil}=1$，$\lambda_{perc}=0.5$，$\lambda_{geo}=0.5$。移除 $\mathcal{L}_{geo}$ 将导致 PSNR 下降约 0.14 dB 并出现 3D 不一致伪影（Table 3: 21.132 vs 21.274），验证了该正则化对几何一致性的贡献。

### 补充图表

![[assets/figures/papers/paper_list_l80_https_openreview_net_forum_id_E7VL9Zl1Nc/figures/009_Figure.jpg]]



## 实验与关键发现

### 核心定量结果

FastGHA在两个主流头像重建基准上均取得了最优性能，且推理速度达到实时水平。在Ava-256数据集上，FastGHA（混合训练版本）的PSNR达到22.5 dB，相比前馈式3D高斯头像方法**Avat3r**（Kirschstein et al., CVPR 2025）的20.7 dB提升了1.8 dB；在感知质量指标LPIPS上，FastGHA从0.33降至0.23，身份保持指标CSIM从0.59提升至0.73（Table 1）。在Nersemble数据集上，FastGHA的PSNR达到24.0 dB，较**GPAvatar**（Chu et al., 2024）的20.8 dB提升了3.2 dB，SSIM从0.76提升至0.81。

![[assets/figures/papers/paper_list_l80_https_openreview_net_forum_id_E7VL9Zl1Nc/figures/003_Table_1.jpg]]
*Table 1: Quantitative comparison with state-of-the-art methods on Ava-256 and Nersemble datasets*

速度方面，FastGHA在4视图输入下重建时间小于1秒，动画帧率达到62 FPS（Table 2），而Avat3r仅能达到8 FPS。这一数量级的加速源于将表情驱动从交叉注意力模块替换为独立作用于每个高斯点的轻量MLP变形网络，使得变形计算可以完全并行化。

![[assets/figures/papers/paper_list_l80_https_openreview_net_forum_id_E7VL9Zl1Nc/figures/008_Table_2.jpg]]
*Table 2: Running time with different number of input images of our method. All results exclude the time for obtaining camera and expression parameters that can be calculated in advance*

### 消融研究

消融实验在Ava-256数据集上系统验证了各设计决策的贡献（Table 3, Table 5）：

![[assets/figures/papers/paper_list_l80_https_openreview_net_forum_id_E7VL9Zl1Nc/figures/011_Table_3.jpg]]
*Table 3: Ablation results on the Ava-256 dataset*

![[assets/figures/papers/paper_list_l80_https_openreview_net_forum_id_E7VL9Zl1Nc/figures/014_Table_5.jpg]]
*Table 5: More ablation results on the Ava-256 dataset*

**预训练VAE权重**：移除SD-Turbo VAE的预训练权重、从头训练编码器和解码器，PSNR从21.274降至20.789（-0.48 dB）。这表明预训练的颜色先验对高质量纹理重建至关重要。

**几何正则化损失 $\\mathcal{L}_{geo}$**：移除基于VGGT的几何损失后，PSNR降至21.132（-0.14 dB），且出现3D不一致和伪影。这验证了将几何先验作为损失而非输入特征的设计合理性——既保留了几何监督的有效性，又避免了推理阶段的不准确几何信息传播。

**每高斯特征**：移除每高斯特征 $\\mathbf{f}$ 后PSNR降至21.053，动画精度严重受损。特征维度从32降至16时PSNR为21.220（边际下降），但进一步降低维度会明显损害动画质量；增至64维仅带来微弱提升（PSNR 21.420）。这表明32维特征在表达能力与效率间取得了良好平衡。

**语义编码器选择**：用Sapiens特征替代DINOv3后PSNR降至21.081，完全移除DINOv3特征图则降至21.068，同时形状一致性下降（Figure 9）。DINOv3的语义特征对多视图几何对应建模具有不可替代的作用。

### 输入视图数量分析

Figure 5和Table 2揭示了输入视图数量对性能的影响规律。由于FastGHA采用逐像素高斯回归，高斯点数量和重建时间随视图数近似线性增长。1视图下重建仅需0.05秒，4视图下约0.8秒。重建质量随视图数增加而提升，但边际收益递减——4视图已能获得较高质量，更多视图主要用于覆盖更大视角范围。

### 失败模式与局限性

尽管FastGHA在定量和定性上均表现出色，仍存在以下局限：

1. **相机参数敏感性**：模型对相机参数扰动较为敏感，不准确的相机输入会降低多视图一致性。当前训练依赖实验室校准的多视图数据集，在无相机内参的真实场景中需要额外的相机估计步骤。
2. **极端姿态与表情**：Figure 8展示了大姿态和大表情下的动画效果，但在完全侧面或大仰角等极端视角下，动画质量仍有提升空间。
3. **区域限制**：当前方法仅支持头部区域重建与动画，未扩展至完整上半身或手部等复杂动态区域。

### 补充图表

![[assets/figures/papers/paper_list_l80_https_openreview_net_forum_id_E7VL9Zl1Nc/figures/010_Figure_7.jpg]]
*Figure 7: Ablation study showing the importance of each of our design decisions*

![[assets/figures/papers/paper_list_l80_https_openreview_net_forum_id_E7VL9Zl1Nc/figures/016_Figure_9.jpg]]
*Figure 9: More qualitative ablation of our design choices*

![[assets/figures/papers/paper_list_l80_https_openreview_net_forum_id_E7VL9Zl1Nc/figures/006_Figure_4.jpg]]
*Figure 4: Qualitative reconstruction comparison on Nersemble held-out subjects*

![[assets/figures/papers/paper_list_l80_https_openreview_net_forum_id_E7VL9Zl1Nc/figures/007_Figure_5.jpg]]
*Figure 5: Analysis on the different number of input views. Two inputs means the first two in the top row, three inputs means the first three, four inputs adds the first image in the bottom row, and so on*

![[assets/figures/papers/paper_list_l80_https_openreview_net_forum_id_E7VL9Zl1Nc/figures/012_Figure.jpg]]

![[assets/figures/papers/paper_list_l80_https_openreview_net_forum_id_E7VL9Zl1Nc/figures/017_Figure_10.jpg]]
*Figure 10: Qualitative comparison with one-shot methods*



## 定位与知识库关联

### 与前馈式3D高斯头像重建的谱系关系

FastGHA 在方法谱系上直接继承自像素级高斯回归的前馈式重建范式，其最直接的对比对象是 **Avat3r** (Kirschstein et al., CVPR 2025)。两者共享的核心设计包括：从多视图输入直接预测每个像素对应的3D高斯原语，以及利用Vision Transformer进行多视图特征融合。然而，FastGHA 在两个关键维度上对 Avat3r 进行了结构性改造，形成了明确的方法论分叉：

1. **动画机制的范式转换**：Avat3r 将表情参数注入交叉注意力模块，使表情驱动与多视图特征融合深度耦合。这种设计虽然理论上能够学习复杂的表情-几何交互，但导致动画推理时每次表情变化都需要重新执行完整的注意力计算，速度仅为 8 FPS。FastGHA 将这一耦合拆解为“规范重建 + 逐点变形”的两阶段架构——先重建一个不含表情的规范高斯头像，再通过一个独立作用于每个高斯点的轻量级 MLP 根据 FLAME 表情码预测属性偏移。这一改造将动画速度提升至 62 FPS（4视图输入），实现了实时动画的质变。

2. **几何先验的使用方式**：Avat3r 将 VGGT 预测的点图通过跳跃连接直接作为网络输入，使得不准确的几何估计会直接污染重建过程。FastGHA 则将 VGGT 点图从输入特征降级为训练时的正则化损失 $\mathcal{L}_{geo}$，仅在训练阶段提供几何监督信号，推理时完全不再依赖 VGGT。这一设计既保留了几何先验对3D一致性的约束作用（消融实验证明移除 $\mathcal{L}_{geo}$ 会导致 PSNR 下降约 0.14 dB 并出现 3D 不一致伪影），又避免了推理时的误差传播。

### 与其他动画头像方法的对比定位

在更广泛的动画头像重建领域，FastGHA 与以下方法形成差异化定位：

- **GPAvatar** (Chu et al., 2024) 使用三平面表示和 FLAME 点云先验，属于基于隐式神经表示的方法。在 Nersemble 数据集上，FastGHA 的 PSNR 达到 24.0，显著优于 GPAvatar 的 20.8，表明显式高斯表示在细节保留上具有优势。

- **InvertAvatar** (Zhao et al., SIGGRAPH 2024) 基于 3D GAN 反演，需要针对每个身份进行优化，而 FastGHA 是前馈式方法，推理时无需任何优化步骤。

- **GAGAvatar** (Chu & Harada, 2024) 和 **LAM** (He et al., 2025) 是单样本 3D 感知头像重建方法。FastGHA 在 one-shot 设定下经过额外微调后也展现出竞争力（见 Table 6），但其核心优势在于少样本（2-4视图）设定下的高保真重建。

### 核心设计决策的有效性边界

消融实验揭示了 FastGHA 各设计决策的贡献强度和作用边界：

- **预训练 VAE 权重**（SD-Turbo VAE）：移除预训练权重（从头训练编码器/解码器）导致 PSNR 从 21.274 降至 20.789，下降约 0.5 dB，是单一消融中影响最大的因素。这表明预训练的颜色先验对高质量纹理重建至关重要。

- **每高斯特征**：移除每高斯特征 $\mathbf{f}$ 后 PSNR 降至 21.053，且动画精度严重受损。该特征是连接规范重建与动画变形的关键信息桥梁——变形 MLP 需要这些特征来理解每个高斯点的语义身份（如属于嘴唇还是脸颊），从而预测合理的表情偏移。

- **DINOv3 语义特征**：替换为 Sapiens 特征导致 PSNR 降至 21.081，完全移除 DINOv3 降至 21.068。DINOv3 提供的语义信息对形状一致性有显著贡献（见 Figure 9）。

- **每高斯特征维度**：从 32 降至 16 会明显损害动画精度，但从 32 提升至 64 仅带来边际改善（PSNR 21.420 vs 21.274），说明 32 维已达到信息瓶颈的饱和点。

### 适用边界与限制

FastGHA 的适用边界由以下因素界定：

1. **相机参数依赖**：模型对相机参数扰动较为敏感，不准确的相机输入会降低多视图一致性。当前训练依赖实验室校准的多视图数据集，在无相机内参的真实场景应用中需要额外的相机估计步骤。这是一个结构性的限制——方法本身没有设计对相机误差的鲁棒机制。

2. **区域范围**：目前仅支持头部区域，未扩展至完整上半身或全身。这一限制与训练数据（Ava-256、Nersemble 均为头部数据集）和 FLAME 模型的表示能力有关。

3. **极端姿态和表情**：虽然方法在常规表情范围内表现良好（见 Figure 8 的大姿态和大表情结果），但在极端视角（完全侧面、大仰角）和极端表情下的动画质量提升空间仍有待探索。

4. **训练成本**：训练需要约 4 天（400k 步，4 块 H800 GPU），虽然推理极快，但训练成本对于资源有限的场景仍是一道门槛。

### 开放问题与后续方向

从方法设计和实验分析中，可以识别出以下值得探索的方向：

- **相机鲁棒性**：能否通过在训练中加入相机噪声增强，或设计不显式依赖相机参数的网络结构，提高对相机误差的鲁棒性？这是将方法推向真实场景应用的关键一步。

- **区域扩展**：如何将像素级高斯回归和逐点变形 MLP 的架构扩展至全身或手部等复杂动态区域？这需要解决更大空间范围下的多视图一致性和变形建模问题。

- **极端条件下的泛化**：在极端视角和极端表情下的动画质量提升，可能需要更丰富的训练数据增强策略或更具表达能力的变形网络设计。

- **与优化式方法的融合**：当前方法完全依赖前馈推理，若能结合轻量级的测试时优化（如在推理时对几何损失进行少量迭代），可能进一步提升重建精度而不显著牺牲速度。



## 原文 PDF

![[paperPDFs/ICLR_2026/FastGHA_Generalized_Few_Shot_3D_Gaussian_Head_Avatars_with_Real_Time_Animation_b897e4f1e33f.pdf]]
