---
title: "Direct-a-Video: Customized Video Generation with User-Directed Camera Movement and Object Motion"
type: paper
paper_level: A
venue: SIGGRAPH
year: 2024
pdf_ref: paperPDFs/SIGGRAPH_2024/Direct_a_Video_Customized_Video_Generation_with_User_Directed_Camera_Movement_and_Object_Motion.pdf
aliases:
- DV
- Direct-a-Video
tags:
- SIGGRAPH_2024
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: "通过引入可训练的时序交叉注意力层（camera module）以自监督方式从相机增强数据中学习相机运动参数，同时利用无训练的空间交叉注意力调制（cross-attention modulation）在扩散模型中引导物体时空轨迹，实现了相机与物体运动的解耦控制。"
primary_logic: "相机运动可以通过对静态镜头视频进行简单的裁剪/缩放增强来模拟，并用专有的时序交叉注意力层进行参数化控制；物体运动则可以通过修改预训练T2V模型的空间交叉注意力图，以边界框引导的放大和抑制来精确控制物体的空间位置和运动，两者互补且无需昂贵的运动标注。"
claims:
- "物体运动通过利用模型内在先验的空间交叉注意力调制（spatial cross-attention modulation）来控制，无需额外优化。"
- "相机运动通过引入新的时序交叉注意力层（temporal cross-attention layers）来解释定量相机运动参数，并通过自监督的相机增强方式进行训练，无需运动标注。"
- "Direct-a-Video 在相机控制任务中取得最佳 FVD（888.91）、FID-vid（48.96）和最低 Flow error（0.46），显著优于 AnimateDiff 和 VideoComposer。"
- "消融实验表明，同时启用注意力放大和抑制能够显著提升物体-框对齐（mIoU 47.83%, AP50 31.33%），缺失任一项会导致性能大幅下降。"
---

# Direct-a-Video: Customized Video Generation with User-Directed Camera Movement and Object Motion

> [!tip] 核心洞察
> 相机运动可以通过对静态镜头视频进行简单的裁剪/缩放增强来模拟，并用专有的时序交叉注意力层进行参数化控制；物体运动则可以通过修改预训练T2V模型的空间交叉注意力图，以边界框引导的放大和抑制来精确控制物体的空间位置和运动，两者互补且无需昂贵的运动标注。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | Direct-a-Video：用户导向的相机运动与物体运动自定义视频生成 |
| 英文题名 | Direct-a-Video: Customized Video Generation with User-Directed Camera Movement and Object Motion |
| 会议/期刊 | SIGGRAPH 2024 |
| Links | [paper](https://arxiv.org/abs/2402.03162); [Project](https://direct-a-video.github.io/) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/image_and_video_generation |
| Method | Direct-a-Video |
| Dataset | Camera Control (200 scene prompts), Object Control (200 box-prompt pairs) |

> [!tip] 效果简介
> - Camera Control (200 scene prompts) 上，FVD 为 888.91，对比 1685.40 (AnimateDiff)，变化 -796.49。
> - Camera Control (200 scene prompts) 上，FID-vid 为 48.96，对比 82.57 (AnimateDiff)，变化 -33.61。
> - Camera Control (200 scene prompts) 上，Flow error 为 0.46，对比 0.74 (VideoComposer)，变化 -0.28。

## 概述

### 问题背景

文本到视频生成领域面临一个核心瓶颈：现有方法无法独立解耦控制相机运动（平移/缩放）与场景中物体的运动。用户若要生成“镜头左移的同时一只老虎向右行走”这样的视频，通常只能依赖模糊的文本描述或预定义的全局运动模式，缺乏对两类运动的精细、定量、独立控制能力。这一缺陷使得视频运动定义模糊，难以满足个性化创作需求。

### 核心方法

Direct-a-Video 提出了一套解耦控制框架，将相机运动与物体运动的控制拆分为两个互补的模块，分别作用于扩散模型的训练与推理阶段：

- **相机运动控制（训练阶段）**：引入可训练的**相机模块**（时序交叉注意力层），以自监督方式从相机增强数据中学习相机运动参数（水平平移 $c_x$、垂直平移 $c_y$、缩放 $c_z$）。通过在静态镜头视频上施加裁剪/缩放增强来模拟相机运动，无需昂贵的运动标注数据。

- **物体运动控制（推理阶段）**：采用**无训练的空间交叉注意力调制**，直接修改预训练 T2V 模型的空间交叉注意力图。用户通过指定物体在首尾帧的边界框及中间路径，系统以注意力放大（amplification）和抑制（suppression）机制引导物体的时空位置，充分利用模型内在先验，无需额外优化。

### 核心结论

1. **解耦控制有效**：Direct-a-Video 首次在 T2V 生成中实现了相机运动与物体运动的独立控制，用户可分别或联合指定两类运动，生成具有精确定义的整体视频运动。

2. **相机控制性能显著**：在 200 个场景提示的相机控制基准上，Direct-a-Video 取得最佳 FVD（888.91）、FID-vid（48.96）和最低光流误差（0.46），显著优于 AnimateDiff 和 VideoComposer（Wang et al., NeurIPS 2023）。

3. **物体控制精准**：在 200 个框-提示对的物体控制任务上，mIoU 达 47.83%，AP50 达 31.33%，远超 VideoComposer（mIoU 26.62%, AP50 4.55%）。消融实验证实，注意力放大与抑制的联合使用是物体-框对齐的关键。

4. **轻量高效**：相机模块仅需在小规模电影镜头数据集上训练，物体控制完全无训练，整体方案在增加动态内容的同时不会显著降低视频质量（FID-vid / FVD 变化微小）。

### 方法定位

Direct-a-Video 处于**可控视频生成**领域，与以下方法形成对比：

- **AnimateDiff**：仅提供预定义运动 LoRA，无法定量控制相机运动。
- **VideoComposer**（Wang et al., NeurIPS 2023）：需要像素级运动向量图作为条件，且相机与物体运动耦合。
- **Peekaboo**：仅支持单物体的注意力掩码控制。

Direct-a-Video 的核心差异在于：通过**时序交叉注意力注入定量相机参数**与**空间交叉注意力调制引导物体轨迹**的结合，首次实现了解耦的、用户导向的双控机制，且大幅降低了训练数据与标注需求。

## 背景与动机

文本到视频（T2V）生成近年来取得了显著进展，但现有方法在运动控制方面仍存在一个关键瓶颈：**相机运动与物体运动被耦合在一起，无法独立解耦控制**。用户要么只能接受模型隐式生成的模糊运动，要么通过粗糙的条件信号（如预定义的运动 LoRA 或像素级运动向量图）进行整体引导，难以精确指定“镜头如何移动”和“场景中的物体如何运动”这两个独立维度。

这一瓶颈的根源在于两个层面。在**相机运动**控制上，主流方法如 **AnimateDiff** 仅提供预定义的运动 LoRA 模块，无法接受用户定量的平移/缩放参数；**VideoComposer**（Wang et al., NeurIPS 2023）虽支持运动向量图条件，但需要大规模带有运动标注的数据集进行全监督训练，标注成本高昂。在**物体运动**控制上，VideoComposer 依赖像素级运动向量图，难以精确指定多物体的时空轨迹；**Peekaboo** 则通过注意力掩码控制物体，但仅支持单物体场景，且缺乏对物体间语义干扰的抑制机制。

上述方法的共同缺陷在于：它们将相机运动与物体运动视为一个整体运动信号，导致视频中“背景在动”和“前景在动”无法分离——用户无法在保持镜头静止的同时让物体自由移动，也无法在镜头平移时让特定物体保持相对静止。这种耦合限制了视频生成的灵活性和可控性。

**Direct-a-Video** 的核心动机正是打破这种耦合。其核心洞察在于：相机运动本质上是全局的、几何的变换，可以通过对静态镜头视频进行简单的裁剪/缩放增强来模拟，无需真实运动标注；而物体运动本质上是局部的、语义的定位问题，可以通过操纵预训练 T2V 模型内部的空间交叉注意力图来实现，无需额外训练。这两个机制天然互补，分别从全局几何和局部语义两个维度解耦运动控制，使得用户能够像导演一样独立指定镜头运动和演员走位。

## 核心创新

Direct-a-Video 的核心创新在于首次在文本到视频生成中实现了**相机运动与物体运动的解耦控制**，且通过非对称的设计哲学——相机运动需要轻量训练、物体运动完全无需训练——以极低的成本解决了此前方法中运动定义模糊、无法灵活定制的瓶颈。

### 关键改进点

**1. 相机运动控制：从无到有的定量参数化**

此前的方法如 **AnimateDiff** 仅能通过预定义的 LoRA 权重提供固定的运动风格，无法接受用户指定的连续相机参数。Direct-a-Video 引入了两个关键组件：
- **相机嵌入器（Camera Embedder）**：将用户输入的平移参数 $c_x$、$c_y$ 和缩放参数 $c_z$ 分别编码为嵌入向量，分离平移和缩放的语义空间。
- **相机模块（Camera Module）**：在预训练 U-Net 的时序自注意力层之后挂接新的时序交叉注意力层，以门控残差形式注入相机嵌入：

$$\mathbf{F} = \mathbf{F} + \tanh(\alpha) \cdot \mathrm{TempCrossAttn}(\mathbf{F}, \mathbf{e}_{\mathrm{cam}})$$

其中 $\mathrm{TempCrossAttn}$ 以视觉特征为查询，分别与平移和缩放嵌入的键/值计算注意力：

$$\mathrm{TempCrossAttn}(\mathbf{F}, \mathbf{e}_{\mathrm{cam}}) = \mathrm{Softmax}\left( \frac{\mathbf{Q} [\mathbf{K}_{xy}, \mathbf{K}_{z}]^T}{\sqrt{d}} \right) [\mathbf{V}_{xy}, \mathbf{V}_{z}]$$

这种设计使得模型能够精确解释连续的相机运动参数，而非仅仅模仿预定义的运动模式。

**2. 物体运动控制：从像素级条件到注意力调制**

**VideoComposer**（Wang et al., NeurIPS 2023）依赖像素级运动向量图作为条件输入，**Peekaboo** 则通过注意力掩码控制物体，但仅支持单物体场景。Direct-a-Video 提出**无训练的空间交叉注意力调制**，通过修改预训练 T2V 模型的空间交叉注意力图来引导物体的时空轨迹：

$$\mathrm{CrossAttnModulate}(\mathbf{Q}, \mathbf{K}, \mathbf{V}) = \mathrm{Softmax}\left( \frac{\mathbf{Q} \mathbf{K}^{\top} + \lambda \mathbf{S}}{\sqrt{d}} \right) \mathbf{V}$$

其中调制项 $\mathbf{S}$ 对物体词对应的注意力区域进行**放大（amplification）**和**抑制（suppression）**：在物体边界框内放大目标词的注意力权重，同时抑制其他物体词在该区域的注意力，防止语义混合。该方法天然支持多物体和任意边界框轨迹，且完全利用预训练模型的内部先验，无需任何额外优化。

**3. 训练策略：从大规模标注到自监督增强**

**VideoComposer** 和 **MotionCtrl** 等方法需要大规模带有运动标注的视频数据集进行全监督训练。Direct-a-Video 的相机运动训练采用自监督策略：在静态镜头视频上应用裁剪/缩放增强来模拟相机运动，增强参数直接作为训练标签，无需人工标注。物体运动控制则完全不参与训练，仅在推理时通过注意力调制实现。这种策略大幅降低了数据获取和训练成本。

## 整体框架

![[assets/figures/papers/paper_list_l13_Direct_a_Video_Customized_Video_Generation_with_User_Directed_Camera_Mov/figures/001_Figure_1.jpg]]
*Figure 1: Direct-a-Video is a text-to-video generation framework that allows users to individually or jointly control the camera movement and/or object motion*

![[assets/figures/papers/paper_list_l13_Direct_a_Video_Customized_Video_Generation_with_User_Directed_Camera_Mov/figures/010_Figure_7.jpg]]
*Figure 7: Limitations of our method. Top: con icting inputs can lead to unreal results - a moving house. Bottom: Overlapping boxes may lead to object interfere - tiger with a bear head*

Direct-a-Video 的整体流程分为两个解耦的阶段：**训练阶段学习相机运动控制**，**推理阶段实现物体运动控制**，两者在同一个预训练文本到视频（T2V）扩散模型中协同工作。

### 用户输入接口

用户通过三个并行的通道指定视频的运动行为：

- **文本提示**：描述场景内容，可选择性包含物体词 $O_1, O_2, \dots, O_N$。
- **相机运动参数**：三元组 $\mathbf{c}_{\text{cam}} = [c_x, c_y, c_z]$，分别表示水平平移比例、垂直平移比例和缩放比例。
- **物体边界框轨迹**：用户在第 1 帧和第 $L$ 帧绘制物体 $n$ 的起始框 $\mathbf{B}_n^1$ 和结束框 $\mathbf{B}_n^L$，中间路径由线性插值自动生成。

### 训练阶段：相机模块

相机运动控制通过引入**可训练的时序交叉注意力层**（camera module）来实现。这些新层被插入到 U-Net 原有的时序自注意力层之后，专门解释定量相机运动参数。

核心流程如下：
1. **数据增强**：从静态镜头视频数据集出发，根据采样的相机参数 $[c_x, c_y, c_z]$ 对视频帧进行裁剪和缩放，模拟相机平移和变焦效果，无需任何人工运动标注。
2. **相机嵌入**：相机参数通过 Camera Embedder 编码为嵌入向量 $\mathbf{e}_{\text{cam}}$，其中平移分量（$c_x, c_y$）和缩放分量（$c_z$）分别编码，以保留运动类型的独立性。
3. **特征注入**：相机嵌入通过时序交叉注意力注入视觉特征 $\mathbf{F}$，采用门控残差更新：
   $$\mathbf{F} = \mathbf{F} + \tanh(\alpha) \cdot \text{TempCrossAttn}(\mathbf{F}, \mathbf{e}_{\text{cam}})$$
   其中 $\alpha$ 为可学习的门控参数，控制相机条件的介入强度。
4. **注意力机制**：时序交叉注意力以视觉特征为查询 $\mathbf{Q}$，分别与平移嵌入的键值对 $[\mathbf{K}_{xy}, \mathbf{V}_{xy}]$ 和缩放嵌入的键值对 $[\mathbf{K}_z, \mathbf{V}_z]$ 计算注意力：
   $$\text{TempCrossAttn}(\mathbf{F}, \mathbf{e}_{\text{cam}}) = \text{Softmax}\left( \frac{\mathbf{Q} [\mathbf{K}_{xy}, \mathbf{K}_{z}]^\top}{\sqrt{d}} \right) [\mathbf{V}_{xy}, \mathbf{V}_{z}]$$
5. **训练目标**：以相机运动参数和文本为联合条件的标准扩散噪声预测损失：
   $$\mathcal{L} = \mathbb{E}_{\mathbf{x}_0, \mathbf{c}_{\text{cam}}, \mathbf{c}_{\text{txt}}, t, \epsilon \sim \mathcal{N}(0, I)} \left[ \lVert \epsilon - \epsilon_{\boldsymbol{\theta}} \left( \mathbf{x}_t, \mathbf{c}_{\text{cam}}, c_{\text{txt}}, t \right) \rVert_2^2 \right]$$

预训练 T2V 骨干网络（Zeroscope）的原始权重在训练过程中保持冻结，仅优化新添加的相机相关层。

### 推理阶段：物体运动控制

物体运动控制完全在推理时实现，**无需任何额外训练**。其核心是修改预训练模型的空间交叉注意力图：

1. **边界框到注意力调制**：对于每个物体 $n$ 在每一帧 $k$，根据其边界框 $\mathbf{B}_n^k$ 生成调制项 $\mathbf{S}_n^k$：
   $$\mathsf{S}_{n}^{k}[i, j] = \begin{cases} 
   1 - \frac{|\mathsf{B}_{n}^{k}|}{|\mathsf{QK}^{\top}|}, & \text{if } i \in \mathsf{B}_{n}^{k} \text{ and } j \in \mathsf{T}_{n} \text{ and } t \ge \tau \\
   0, & \text{if } i \in \mathsf{B}_{n}^{k} \text{ and } j \in \mathsf{T}_{n} \text{ and } t < \tau \\
   -\infty, & \text{otherwise}
   \end{cases}$$
   其中 $\mathsf{T}_n$ 为物体 $n$ 对应的文本 token，$\tau$ 为截止时间步。
2. **空间交叉注意力调制**：将调制项添加到原始注意力分数中：
   $$\text{CrossAttnModulate}(\mathbf{Q}, \mathbf{K}, \mathbf{V}) = \text{Softmax}\left( \frac{\mathbf{Q} \mathbf{K}^{\top} + \lambda \mathbf{S}}{\sqrt{d}} \right) \mathbf{V}$$
   其中 $\lambda$ 为放大强度超参数。
3. **双重机制**：调制项在边界框内对目标 token 的注意力进行**放大**（$t \ge \tau$ 时），同时对非目标 token 进行**抑制**（设为 $-\infty$），防止多物体场景中的语义混合。

### 解耦控制与联合生成

相机模块和物体运动调制分别作用于不同的交叉注意力层——前者在时序维度注入全局运动，后者在空间维度引导局部物体轨迹，两者互不干扰。推理时，用户可以独立指定相机参数和物体框序列，模型同时接受两个控制信号，生成相机运动和物体运动解耦的视频。

推理阶段还采用**分类器自由引导**（classifier-free guidance）策略，以无条件相机状态（静态镜头）作为负样本，增强相机控制的响应精度：
$$\hat{\epsilon}_{\theta}\left(\mathbf{z}_{t}, \mathbf{c}_{\text{cam}}, \mathbf{c}_{\text{txt}}, t\right) = \epsilon_{\theta}\left(\mathbf{z}_{t}, \boldsymbol{\mathbb{O}}_{\text{cam}}, \boldsymbol{\mathbb{O}}_{\text{txt}}, t\right) + s\left(\epsilon_{\theta}\left(\mathbf{z}_{t}, \mathbf{c}_{\text{cam}}, \mathbf{c}_{\text{txt}}, t\right) - \epsilon_{\theta}\left(\mathbf{z}_{t}, \boldsymbol{\mathbb{O}}_{\text{cam}}, \boldsymbol{\mathbb{O}}_{\text{txt}}, t\right)\right)$$

### 关键设计决策

| 模块 | 训练需求 | 控制信号 | 作用维度 |
|------|---------|---------|---------|
| Camera Module | 需要自监督训练 | 连续平移/缩放参数 | 时序交叉注意力 |
| Spatial Cross-Attn Modulation | 无需训练 | 边界框轨迹 | 空间交叉注意力 |

这种设计使得 Direct-a-Video 在**不依赖昂贵运动标注数据**的前提下，实现了相机运动和物体运动的独立解耦控制，同时支持单一控制和联合控制两种模式。

## 核心模块与公式推导

Direct-a-Video 的核心架构由两个解耦的控制分支构成：相机运动控制通过**可训练的时序交叉注意力模块**实现，物体运动控制则通过**无训练的空间交叉注意力调制**实现。两者共享一个冻结的预训练 T2V 骨干网络（Zeroscope），仅在推理时协同工作。

### 相机运动控制模块

相机运动被参数化为一个三元组 $\mathbf{c}_{\text{cam}} = [c_x, c_y, c_z]$，分别表示水平平移比率、垂直平移比率和缩放比率。训练时，通过对静态镜头视频施加裁剪/缩放增强来模拟相机运动，从而以自监督方式训练新增的相机模块，完全规避了对运动标注的依赖。

**Camera Embedder** 首先将相机参数编码为嵌入向量 $\mathbf{e}_{\text{cam}}$，并分离平移编码（对应 $c_x, c_y$）和缩放编码（对应 $c_z$），以支持后续的独立注意力计算。

**Camera Module** 是一组挂接到 U-Net 时序自注意力层之后的全新时序交叉注意力层。其核心运算为门控残差更新：

$$\mathbf{F} = \mathbf{F} + \tanh(\alpha) \cdot \mathrm{TempCrossAttn}(\mathbf{F}, \mathbf{e}_{\text{cam}})$$

其中 $\mathbf{F}$ 为视觉特征，$\alpha$ 为零初始化的可学习门控参数，确保训练初期相机模块不干扰原有特征。时序交叉注意力的具体计算为：

$$\mathrm{TempCrossAttn}(\mathbf{F}, \mathbf{e}_{\text{cam}}) = \mathrm{Softmax}\left( \frac{\mathbf{Q} [\mathbf{K}_{xy}, \mathbf{K}_{z}]^T}{\sqrt{d}} \right) [\mathbf{V}_{xy}, \mathbf{V}_{z}]$$

该公式的核心设计在于：以视觉特征为查询 $\mathbf{Q}$，分别与平移嵌入生成的键 $\mathbf{K}_{xy}$ 和缩放嵌入生成的键 $\mathbf{K}_{z}$ 进行拼接后计算注意力，对应的值 $\mathbf{V}_{xy}$ 和 $\mathbf{V}_{z}$ 同样拼接后加权聚合。消融实验证实，这种分离编码策略将光流误差从联合嵌入的 1.68 降至 0.46（Section 4.5），验证了平移和缩放运动需要独立建模的因果机制。

训练目标为标准扩散噪声预测损失：

$$\mathcal{L} = \mathbb{E}_{\mathbf{x}_0, \mathbf{c}_{\text{cam}}, \mathbf{c}_{\text{txt}}, t, \epsilon \sim \mathcal{N}(0, I)} \left[ \lVert \epsilon - \epsilon_{\boldsymbol{\theta}} \left( \mathbf{x}_t, \mathbf{c}_{\text{cam}}, \mathbf{c}_{\text{txt}}, t \right) \rVert_2^2 \right]$$

推理时采用分类器自由引导，以无条件相机状态（即静态镜头）作为负样本：

$$\hat{\epsilon}_{\theta}\left(\mathbf{z}_{t}, \mathbf{c}_{\text{cam}}, \mathbf{c}_{\text{txt}}, t\right) = \epsilon_{\theta}\left(\mathbf{z}_{t}, \boldsymbol{\mathbb{O}}_{\text{cam}}, \boldsymbol{\mathbb{O}}_{\text{txt}}, t\right) + s\left(\epsilon_{\theta}\left(\mathbf{z}_{t}, \mathbf{c}_{\text{cam}}, \mathbf{c}_{\text{txt}}, t\right) - \epsilon_{\theta}\left(\mathbf{z}_{t}, \boldsymbol{\mathbb{O}}_{\text{cam}}, \boldsymbol{\mathbb{O}}_{\text{txt}}, t\right)\right)$$

其中 $\boldsymbol{\mathbb{O}}_{\text{cam}}$ 表示空相机条件（附录 A.3, Eq. 6）。

### 物体运动控制模块

物体运动控制完全在推理阶段通过修改预训练模型的空间交叉注意力图实现，无需任何额外训练。其核心操作是**空间交叉注意力调制**：

$$\mathrm{CrossAttnModulate}(\mathbf{Q}, \mathbf{K}, \mathbf{V}) = \mathrm{Softmax}\left( \frac{\mathbf{Q} \mathbf{K}^{\top} + \lambda \mathbf{S}}{\sqrt{d}} \right) \mathbf{V}$$

其中 $\lambda$ 为调制强度超参数，$\mathbf{S}$ 为逐物体的调制项。对于第 $n$ 个物体在第 $k$ 帧的调制项定义为：

$$\mathsf{S}_{n}^{k}[i, j] = \left\{ \begin{array}{ll} {1 - \frac{|\mathsf{B}_{n}^{k}|}{|\mathsf{QK}^{\top}|}}, & {\mathrm{if~} i \in \mathsf{B}_{n}^{k} \mathrm{~and~} j \in \mathsf{T}_{n} \mathrm{~and~} t \ge \tau} \\ {0,} & {\mathrm{if~} i \in \mathsf{B}_{n}^{k} \mathrm{~and~} j \in \mathsf{T}_{n} \mathrm{~and~} t < \tau} \\ {-\infty,} & {\mathrm{otherwise}} \end{array} \right.$$

该公式的因果机制分三层：
- **注意力放大**（$t \ge \tau$）：在边界框 $\mathsf{B}_{n}^{k}$ 区域内，为对应文本标记 $\mathsf{T}_{n}$ 添加正调制项，增强物体与文本的注意力关联；
- **注意力减弱**（$t < \tau$）：在扩散早期（$\tau$ 通常设为 $0.9T$），对该区域施加零调制，避免过早固定物体位置导致语义质量下降；
- **注意力抑制**（otherwise）：对其他区域施加 $-\infty$，强制非目标区域无法关注该文本标记，防止多物体场景下的语义泄漏（如老虎纹理混入熊的身体）。

消融实验（Table 3）表明，同时启用注意力放大和抑制时 mIoU 达 47.83%、AP50 达 31.33%；仅保留抑制而关闭放大时，mIoU 骤降至 15.35%、AP50 降至 3.46%，验证了注意力放大对物体-框对齐的关键作用。此外，Table 4 显示将注意力放大同时应用于 U-Net 的编码器和解码器可获得最佳接地性能（mIoU 49.06%）。

## 实验与分析

Direct-a-Video 的实验设计围绕两个核心目标展开：验证相机运动与物体运动的解耦控制能力，以及评估该控制对视频生成质量的影响。实验基于预训练的 T2V 主干网络 Zeroscope，在 200 个场景提示词上评估相机控制，在 200 个框-提示词对上评估物体控制。

### 相机运动控制：定量与定性评估

**Table 1** 展示了相机运动控制的主结果。Direct-a-Video 在所有三个指标上均取得最优：FVD 为 888.91（AnimateDiff 为 1685.40，降幅约 47%），FID-vid 为 48.96（AnimateDiff 为 82.57），光流误差（Flow error）仅 0.46（VideoComposer 为 0.74）。这一结果表明，通过引入可训练的时序交叉注意力层（相机模块）并以自监督增强方式学习相机参数，模型能够精确地控制视频中的相机平移和缩放，同时保持生成质量。

![[assets/figures/papers/paper_list_l13_Direct_a_Video_Customized_Video_Generation_with_User_Directed_Camera_Mov/figures/003_Table_1.jpg]]
*Table 1: Quantitative comparison for camera movement control evaluation*

**Figure 3** 的定性对比进一步揭示了 Direct-a-Video 的关键优势：在 VideoComposer 的生成结果中，物体运动（黄色轨迹线）会随相机运动（青色轨迹线）发生非预期的位移，而 Direct-a-Video 成功实现了两者的解耦——物体运动独立于相机运动，用户可分别指定。

### 物体运动控制：接地精度与语义保持

**Table 2** 报告了物体运动控制的定量对比。Direct-a-Video 在接地指标上大幅领先：mIoU 达 47.83%（VideoComposer 仅 26.62%），AP50 达 31.33%（VideoComposer 仅 4.55%）。同时，CLIP-sim 为 27.63，略高于 VideoComposer 的 25.66，表明语义保真度未因强接地而受损。这一性能优势源于无训练的空间交叉注意力调制机制——它直接利用预训练模型的内部先验，通过边界框引导的注意力放大与抑制来精确控制物体的时空位置，无需额外的运动标注或模型微调。

![[assets/figures/papers/paper_list_l13_Direct_a_Video_Customized_Video_Generation_with_User_Directed_Camera_Mov/figures/006_Table_2.jpg]]
*Table 2: Quantitative comparison for object motion control evaluation*

**Figure 4** 的定性对比显示，Direct-a-Video 在处理多物体场景时尤为突出，而 Peekaboo 等方法仅支持单物体的注意力掩码控制。

### 消融实验：注意力放大与抑制的互补性

**Table 3** 揭示了注意力放大（amplification）与抑制（suppression）的互补作用。当仅启用抑制而不启用放大时，mIoU 骤降至 15.35%，AP50 降至 3.46%，CLIP-sim 降至 25.82，表明物体几乎无法与框对齐。当仅启用放大而不启用抑制时，mIoU 为 40.23%，AP50 为 22.92%，性能虽有回升但仍显著低于两者同时启用的结果（mIoU 47.83%，AP50 31.33%）。**Figure 6** 直观展示了这一现象：无放大时物体不跟随边界框移动；无抑制时会出现纹理泄漏（如老虎纹理混入熊的身体）；两者共同启用后问题得到解决。

![[assets/figures/papers/paper_list_l13_Direct_a_Video_Customized_Video_Generation_with_User_Directed_Camera_Mov/figures/007_Table_3.jpg]]
*Table 3: Quantitative evaluation of attention amplifcation and suppression*

**Table 4** 进一步分析了注意力放大在 U-Net 不同部分的作用。在编码器和解码器中同时应用放大可获得最佳接地性能（mIoU 49.06%，AP50 30.04%），仅在编码器中应用则分别降至 46.60% 和 28.20%。

![[assets/figures/papers/paper_list_l13_Direct_a_Video_Customized_Video_Generation_with_User_Directed_Camera_Mov/figures/011_Table_4.jpg]]
*Table 4: Assessment of attention amplifcation on di erent parts of UNet*

### 相机嵌入设计与超参数影响

相机嵌入的设计对控制精度有显著影响。消融实验表明，将平移参数（$c_x, c_y$）和缩放参数（$c_z$）分别编码（separate encoding）相比联合编码（joint encoding），光流误差从 1.68 降至 0.46，验证了分离编码对于精确解耦平移与缩放运动的必要性。

关于注意力放大的超参数，**Table 5** 显示截止时间步 $\tau > 0.9T$（即仅在扩散早期应用放大）可获得更好的语义质量，而放大强度 $\lambda$ 需在接地精度与图像质量之间权衡。

![[assets/figures/papers/paper_list_l13_Direct_a_Video_Customized_Video_Generation_with_User_Directed_Camera_Mov/figures/015_Table_5.jpg]]
*Table 5: CLIP-sim and mIOU metrics tested on di erent attention amplifcation hyper-parameters*

### 联合控制与视频质量影响

**Table 6** 评估了添加相机或物体控制对视频质量的影响。结果表明，无论是单独添加相机控制、物体控制，还是两者联合控制，FID-vid 和 FVD 的变化均不显著，说明 Direct-a-Video 在引入动态内容的同时不会造成明显的质量退化。**Figure 9** 的定性对比也印证了这一点：同一提示词在无控制、仅相机控制、仅物体控制、相机+物体控制四种模式下，生成质量保持稳定，而动态内容逐步丰富。

![[assets/figures/papers/paper_list_l13_Direct_a_Video_Customized_Video_Generation_with_User_Directed_Camera_Mov/figures/013_Table_6.jpg]]
*Table 6: Quantitative evaluation for camera/object control on video quality*

### 失败模式与局限性

**Figure 7** 展示了 Direct-a-Video 的两类典型失败模式。第一类为冲突输入导致的不真实结果：当用户指定相机向左平移而物体边界框保持静止时，模型可能生成一栋“移动的房屋”，这违背了物理常识。第二类为重叠边界框导致的物体特征干扰：当多个物体的边界框发生重叠时，可能会出现特征混合（如老虎长出熊头）。这些局限性表明，当前的解耦控制框架在处理物理一致性和多物体交互方面仍有提升空间，相关改进方向可作为后续工作的切入点。

### 补充图表

![[assets/figures/papers/paper_list_l13_Direct_a_Video_Customized_Video_Generation_with_User_Directed_Camera_Mov/figures/008_Figure.jpg]]
*Figure: “A zebra next to a river”（a) “A horse walking on grassland”（b) （c) “A tiger and a bear walking on grass“ （d) “A tiger and a bear walking on grass“*

## 方法谱系与知识库定位

### 与现有工作的关系

Direct-a-Video 的核心贡献在于首次在文本到视频（T2V）生成框架中实现了相机运动与物体运动的**解耦控制**，这一点使其在方法谱系中占据独特位置。现有工作通常将两者耦合处理或仅控制单一维度。

**相机运动控制方面**，Direct-a-Video 与以下基线形成对比：

- **AnimateDiff**：通过预定义的运动 LoRA 注入运动模式，但缺乏对相机平移、缩放的定量、连续控制能力。Direct-a-Video 以可训练的时序交叉注意力层（相机模块）替代了这种隐式控制，实现了参数化调节。
- **VideoComposer**（Wang et al., NeurIPS 2023）：使用像素级运动向量图作为条件，需要额外的运动提取模块和大规模运动标注数据。Direct-a-Video 的相机模块仅需对静态镜头视频进行裁剪/缩放增强即可自监督训练，完全消除了对运动标注的依赖，训练数据构建成本显著降低。

**物体运动控制方面**，Direct-a-Video 的定位更加鲜明：

- **VideoComposer**：同样依赖运动向量图，在处理多物体场景时，物体运动与相机运动难以解耦（见 Figure 3 定性对比：VideoComposer 中物体运动受相机运动干扰，而 Direct-a-Video 中两者独立）。
- **Peekaboo**：采用注意力掩码控制物体位置，但仅支持单物体场景。Direct-a-Video 通过无训练的**空间交叉注意力调制**（同时施加放大与抑制），天然支持多物体、多边界框轨迹的独立控制，且无需任何额外优化。

**训练范式对比**：Direct-a-Video 采用“部分训练 + 无训练推理”的混合策略——相机模块在小规模数据集上轻量训练（仅新增的交叉注意力层，冻结 T2V 骨干网络），物体运动控制完全在推理时通过调制预训练模型的内在先验实现。这与 VideoComposer 等需要全监督训练的方法形成根本性差异。

### 适用边界与条件

Direct-a-Video 的有效性依赖于以下前提和边界：

1. **相机运动类型受限**：当前仅支持平移（pan）和缩放（zoom）两种相机运动，参数化为 $[c_x, c_y, c_z]$。不支持旋转（roll/pitch/yaw）等更复杂的相机运动，这受限于训练增强策略的设计——增强仅模拟了裁剪和平移，无法合成旋转视角下的新内容。
2. **基础模型先验依赖**：物体运动控制完全依赖预训练 T2V 模型（Zeroscope）的空间交叉注意力先验。若基础模型对特定物体或场景的理解不足，注意力调制可能无法正确引导物体位置。该方法本质上是在“引导”而非“注入”知识。
3. **多物体交互场景的脆弱性**：当多个物体的边界框发生重叠时，注意力抑制机制可能失效，导致物体特征相互干扰（如老虎的纹理泄漏到熊的身体上，见 Figure 7 底部）。这表明空间交叉注意力调制的分辨率受限于潜在空间的空间维度，无法精细处理遮挡关系。
4. **冲突输入的物理不一致**：当用户指定的物体运动与相机运动在物理上矛盾时（如相机左移但物体边界框保持静止），模型可能生成不真实的结果（如移动的房屋，见 Figure 7 顶部）。系统缺乏对运动一致性的显式约束或检测机制。

### 局限与开放问题

**已知局限**（论文明确讨论）：

- 冲突输入导致非物理结果（如上述移动房屋）。
- 重叠边界框引发物体特征干扰。
- 相机模块仅在小规模电影镜头数据集上训练，对极端或高速相机运动的泛化能力可能有限。

**开放问题**（基于方法本质的延伸）：

1. **相机运动维度的扩展**：能否将增强策略从 2D 裁剪/缩放扩展到模拟 3D 旋转（roll/pitch/yaw）？这可能需要引入单目深度估计或 3D 先验来合成旋转视角下的合理内容，而非简单的图像变换。
2. **遮挡与外观一致性**：在多物体重叠或相互遮挡时，如何保持各物体的外观一致性？当前的空间交叉注意力调制是逐帧独立的，缺乏对物体外观的显式跟踪或记忆机制。结合实例级的外观嵌入可能是一个方向。
3. **与 3D 表示的融合**：该解耦控制框架能否与基于 3D 表示（如 NeRF、3D Gaussian Splatting）的视频生成方法结合？3D 表示天然支持相机运动的精确控制，而 Direct-a-Video 的注意力调制可处理物体运动，两者互补。
4. **增强随机性与运动精度的对齐**：训练时相机参数 $c_x, c_y, c_z$ 是从均匀分布中随机采样的（见附录 A.2），增强后的视频可能无法保证运动参数与视觉内容精确对齐（如缩放中心偏差）。这种“弱监督”信号是否会限制相机控制的精度上限，值得进一步验证。
5. **物体运动的时序平滑性**：当前方法逐帧独立计算注意力调制项 $S_n^k$，物体轨迹的平滑性完全依赖边界框插值。在快速运动或非均匀运动场景下，是否会出现物体抖动或瞬移，论文未给出定量评估。

### 知识库定位

Direct-a-Video 在“可控视频生成”领域的知识库中定位为**解耦式、轻量级运动控制框架**。其核心知识贡献包括：

- **概念层**：首次明确将相机运动与物体运动作为两个可独立控制的轴，并证明在扩散模型框架下可通过不同机制（时序交叉注意力 vs. 空间交叉注意力调制）实现解耦。
- **方法层**：提供了一套低成本的训练/推理方案——自监督相机增强 + 无训练注意力调制，为后续工作提供了“无需昂贵运动标注”的可行范式。
- **实证层**：通过系统的消融实验，揭示了注意力放大与抑制的互补关系（单独使用任一项性能大幅下降）、放大在 U-Net 编解码器上的最佳配置、以及分离相机嵌入（平移/缩放分别编码）对控制精度的关键作用。这些发现为后续的注意力调制方法提供了实用指导。

在更广泛的 T2V 可控生成谱系中，Direct-a-Video 填补了“用户导向的、解耦的运动控制”这一空白，与基于条件注入（如 ControlNet 类方法）、基于运动向量（如 VideoComposer）、基于预定义模式（如 AnimateDiff）的方法形成互补。其局限性（旋转缺失、遮挡处理）也指明了该子方向的下一步研究重点。

## 原文 PDF

![[paperPDFs/SIGGRAPH_2024/Direct_a_Video_Customized_Video_Generation_with_User_Directed_Camera_Movement_and_Object_Motion.pdf]]
