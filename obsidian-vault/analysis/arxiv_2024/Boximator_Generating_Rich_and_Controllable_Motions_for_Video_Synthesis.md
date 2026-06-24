---
title: "Boximator: Generating Rich and Controllable Motions for Video Synthesis"
type: paper
paper_level: A
venue: arXiv
year: 2024
pdf_ref: paperPDFs/arxiv_2024/Boximator_Generating_Rich_and_Controllable_Motions_for_Video_Synthesis.pdf
aliases:
- Boximator
tags:
- arxiv_2024
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: 自跟踪（Self-Tracking）技术，通过强迫模型生成彩色跟踪框作为中间表示，将困难的控制对齐问题分解为生成正确颜色框和对齐约束两个简单子任务。
primary_logic: 多阶段训练策略（先硬盒+自跟踪，再引入软盒+自跟踪，最后移除可见框）使模型在可见框消失后仍保留隐式对齐能力，实现对复杂运动的精确约束。
claims:
- 去除自跟踪导致盒子对齐mAP从0.349骤降至0.118（MSR-VTT Box条件）。
- 仅使用标准损失训练110K步后，模型仍无法对齐大多数盒约束。
- 自跟踪训练时，模型能快速生成正确颜色的框并使其与约束对齐，去除可见框后隐式表示仍生效。
- MSR-VTT 上 FVD = 174 (PixelDance+Boximator with Box)
---

# Boximator: Generating Rich and Controllable Motions for Video Synthesis

> [!tip] 核心洞察
> 多阶段训练策略（先硬盒+自跟踪，再引入软盒+自跟踪，最后移除可见框）使模型在可见框消失后仍保留隐式对齐能力，实现对复杂运动的精确约束。

| 字段 | 内容 |
|------|------|
| 中文题名 | Boximator：生成丰富且可控运动的视频合成 |
| 英文题名 | Boximator: Generating Rich and Controllable Motions for Video Synthesis |
| 会议/期刊 | arXiv 2024 |
| Links | [paper](https://arxiv.org/abs/2402.01566) · [Project](https://boximator.github.io) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/image_and_video_generation |
| Method | Boximator |
| Dataset | MSR-VTT, ActivityNet, UCF-101 |

> [!tip] 效果简介
> - MSR-VTT 上，FVD 174 (PixelDance+Boximator with Box) vs 237 (PixelDance, no box) (-63)；mAP (Box alignment) 0.349 (PixelDance+Boximator, Box condition) vs 0.059 (PixelDance+Boximator, no box) (+0.290)。
> - ActivityNet 上，mAP (Box alignment) 4.4-8.9倍增长相比无盒条件 vs without box (4.4-8.9x)。
> - UCF-101 上，mAP 0.284 (PixelDance+Boximator FO+Box) vs 0.060 (PixelDance+Boximator no box) (+0.224)。

## 概述

**Boximator** 是一项面向视频扩散模型的运动控制插件，旨在解决当前文本到视频生成中“对象运动不可控”这一瓶颈。现有模型难以将用户指定的离散盒子坐标、对象 ID 等控制信号与视觉元素准确关联，并在多帧间维持时间一致性，尤其当多个物体发生重叠时，标准训练策略无法有效习得这种关联。

Boximator 的核心洞察在于引入**自跟踪（Self-Tracking）** 技术：训练阶段强制模型在生成视频帧的同时，为每个受约束对象生成对应颜色的跟踪框。这一设计将困难的控制对齐问题分解为“生成正确颜色框”和“对齐约束”两个简单子任务，使视频扩散模型能快速掌握盒子与物体的关联。配合**多阶段训练策略**——先以硬盒结合自跟踪建立基础对齐，再引入软盒增强时序平滑，最后移除可见框——模型在可见框消失后仍保留隐式对齐能力，实现对复杂运动的精确约束。

该方法作为即插即用模块，冻结基础视频扩散模型（如 **PixelDance** (Zeng et al., arXiv 2023) 和 **ModelScope** (Wang et al., arXiv 2023)）的全部权重，仅训练新增的控制模块，从而保留基模型的生成质量。在 MSR-VTT 零样本测试中，Boximator 在维持甚至提升视频质量（FVD 从 237 降至 174）的同时，将盒子对齐 mAP 从 0.059 提升至 0.349；在 ActivityNet 上对齐精度提升 4.4–8.9 倍。消融实验进一步证实，移除自跟踪会导致 mAP 骤降至 0.118，验证了该技术的关键作用。

## 背景与动机

### 视频扩散模型的快速演进与可控性缺口

近年来，文本到视频（T2V）扩散模型在生成质量上取得了显著突破。以 **Make-A-Video**（Singer et al., arXiv 2022）为代表的工作率先将扩散模型从图像域拓展到视频域，随后 **ModelScope**（Wang et al., arXiv 2023）和 **PixelDance**（Zeng et al., arXiv 2023）等模型进一步提升了视频的视觉质量和时序一致性。然而，这些模型主要依赖文本描述作为唯一的控制信号，用户无法精确指定视频中特定对象的空间位置和运动轨迹——当文本描述“一只猫跳起来”时，模型生成的跳跃高度、落点位置和运动幅度完全由采样随机性和文本语义决定，缺乏细粒度的空间可控性。

### 现有控制方法的局限

为弥补文本控制的不足，研究者提出了多种条件注入方案。**VideoComposer**（Wang et al., arXiv 2023）支持将深度图、草图、运动向量等多种模态作为额外条件输入，但其控制形式要么过于稠密（如逐帧深度图），要么难以直观指定单个对象的运动轨迹。更关键的是，当用户希望用离散的盒子坐标和对象ID来约束视频中多个物体的运动时，视频扩散模型面临一个核心困难：**如何将抽象的坐标数字与视觉像素中的具体对象建立关联，并在多帧之间保持这种关联的时间一致性**。当多个物体发生重叠或遮挡时，这一对齐问题变得更加严峻。

### 标准训练为何失败

视频扩散模型的标准训练范式是最小化噪声预测损失：

$$
\mathcal{L}_{\theta} = \mathbb{E}_{z_0, c, \epsilon, t} \left[||\epsilon - \epsilon_{\theta}(z_t, t, c)||_2^2\right]
$$

其中 $z_t = \sqrt{\bar{\alpha}_t} z_0 + \sqrt{1 - \bar{\alpha}_t} \epsilon$ 是前向扩散后的噪声隐变量。当条件 $c$ 仅包含文本时，模型通过交叉注意力自然地学习文本-视觉对齐；但当 $c$ 中混入盒子坐标这类结构化控制信号时，模型需要同时完成“理解坐标含义”“识别对应对象”“跨帧跟踪同一对象”三个子任务。实验表明，**仅使用标准损失训练110K步后，模型仍无法对齐大多数盒约束**（Section 5.4），这揭示了标准训练范式在复杂空间控制任务上的根本性不足。

### Boximator 的动机与核心思路

Boximator 的提出正是为了解决上述瓶颈。其核心动机是：**将困难的“坐标-对象-时序”联合对齐问题，分解为模型更容易学习的子任务**。具体而言，Boximator 引入了两种直观的约束形式——**硬盒**（hard box）精确指定目标帧上对象的位置和形状，**软盒**（soft box）允许在中间帧存在一定自由度——使用户无需额外文本即可定义任意对象的运动。更重要的是，Boximator 作为一个即插即用的控制模块，冻结基础视频扩散模型的全部权重，仅训练新增的控制层，从而在保留基模型生成能力的同时赋予其精确的运动控制能力。

## 核心创新

Boximator的核心创新在于通过**自跟踪（Self-Tracking）**机制，将视频扩散模型中困难的控制信号-视觉元素对齐问题分解为两个简单的子任务，并以**多阶段训练策略**使模型在可见辅助信号消失后仍保留隐式对齐能力。

### 瓶颈与因果机制

视频扩散模型难以将离散的盒子坐标、对象ID等控制信号与视觉元素直接关联，并在多帧间维持时间一致性——尤其在多物体重叠场景下。标准训练损失（$\mathcal{L}_{\theta} = \mathbb{E}_{z_0, c, \epsilon, t} [||\epsilon - \epsilon_{\theta}(z_t, t, c)||_2^2]$）在110K步后仍无法使模型对齐大多数盒约束（Section 5.4），表明该映射关系过于复杂，模型无法自发习得。

Boximator的**因果旋钮**是自跟踪：强制模型在训练阶段同时生成视频帧和彩色跟踪框作为中间表示（Figure 4）。这一设计将“对齐盒子与物体”的单一困难任务拆分为：（1）生成正确颜色的边界框；（2）使该框与约束坐标对齐。视频扩散模型能快速掌握这两项任务，且当训练后期移除可见框后，模型已内化的隐式表示仍能维持盒子对齐能力。

### 关键结构变更（Changed Slots）

Boximator作为即插即用的控制模块，在基础视频扩散模型（如**PixelDance**（Zeng et al., arXiv 2023）、**ModelScope**（Wang et al., arXiv 2023））上引入了以下关键变更：

**1. 空间注意力构成重组**

基线模型的注意力顺序为 SelfAttn → CrossAttn。Boximator在两者之间插入一个**Box-Aware Self-Attention层**（Figure 2），以视觉令牌和盒控制令牌为联合输入：

$$
\begin{aligned}
\boldsymbol{v} &= \boldsymbol{v} + \mathrm{SelfAttn}(\boldsymbol{v}) \\
\boldsymbol{v} &= \boldsymbol{v} + \mathrm{TS}(\mathrm{SelfAttn}([\boldsymbol{v}, \boldsymbol{h}_{\mathrm{box}}])) \\
\boldsymbol{v} &= \boldsymbol{v} + \mathrm{CrossAttn}(\boldsymbol{v}, \boldsymbol{h}_{\mathrm{text}})
\end{aligned}
$$

其中盒控制令牌 $\boldsymbol{t}_b = \mathrm{MLP}(\mathrm{Fourier}([b_{\mathrm{loc}}, b_{\mathrm{id}}, b_{\mathrm{flag}}]))$ 将盒子坐标、对象ID和硬/软标志经Fourier嵌入与MLP编码为统一表示。

**2. 盒子-物体关联学习方式**

基线方法试图让模型直接从离散坐标和ID学习视觉关联，效果极差。Boximator通过自跟踪阶段强制生成彩色边界框，将抽象的坐标约束转化为模型擅长的视觉生成任务，大幅降低关联学习难度。

**3. 多阶段训练策略**

基线采用单阶段标准噪声预测损失。Boximator采用三阶段训练：
- **S1**：全硬盒 + 自跟踪，建立盒子-物体基础关联；
- **S2**：引入80%软盒 + 自跟踪，训练模型适应宽松约束；
- **S3**：移除自跟踪，使模型在无可见辅助信号下保留隐式对齐能力。

消融实验表明，仅S1即可达到0.294的mAP，而完整三阶段训练将mAP提升至0.349（Table 4）。

**4. 基础模型权重处理**

与通常微调全部参数不同，Boximator冻结原模型全部权重，仅训练控制模块。消融显示训练全部U-Net参数并不会改善运动控制（ActivityNet FO+Box下mAP为0.331，低于冻结方式的0.394），验证了该设计的有效性。

### 决定性证据强度

自跟踪是Boximator最关键的创新组件：移除自跟踪导致MSR-VTT Box条件下的mAP从0.349骤降至0.118（Table 4），降幅达66%，确证了该机制对学习盒子-物体关联的不可替代性。推理时取消软盒约束同样使mAP降至0.235，表明软盒在维持时间一致性运动控制中发挥重要作用。

## 整体框架

Boximator 的整体设计遵循“冻结基础模型 + 插入控制模块”的即插即用范式，其目标是在不损害原视频扩散模型生成质量的前提下，赋予模型对任意对象运动轨迹的精确控制能力。图 2 给出了控制模块的架构概览。

**输入层：盒子约束的编码。** 用户通过两种约束形式定义运动意图——硬盒（hard box）精确指定对象在首帧和末帧的目标位置与形状，软盒（soft box）则作为中间帧的宽松运动引导。每个盒子被编码为一个控制令牌 $\boldsymbol{t}_b$，其编码过程为：
$$\boldsymbol{t}_b = \mathrm{MLP}(\mathrm{Fourier}([b_{\mathrm{loc}}, b_{\mathrm{id}}, b_{\mathrm{flag}}]))$$
其中 $b_{\mathrm{loc}}$ 为归一化的盒子坐标，$b_{\mathrm{id}}$ 为对象标识符，$b_{\mathrm{flag}}$ 区分硬盒与软盒。三者拼接后经 Fourier 特征嵌入和 MLP 映射为固定维度的控制令牌。当实际盒子数少于预设上限时，剩余槽位用可学习的空令牌填充。

**核心控制模块：Box-Aware Self-Attention。** 控制模块被插入到原视频扩散模型每一个空间注意力块的固定位置。原始的空间注意力栈顺序为 SelfAttn → CrossAttn，Boximator 将其扩展为：
$$\begin{aligned} \boldsymbol{v} &= \boldsymbol{v} + \mathrm{SelfAttn}(\boldsymbol{v}) \\ \boldsymbol{v} &= \boldsymbol{v} + \mathrm{TS}(\mathrm{SelfAttn}([\boldsymbol{v}, \boldsymbol{h}_{\mathrm{box}}])) \\ \boldsymbol{v} &= \boldsymbol{v} + \mathrm{CrossAttn}(\boldsymbol{v}, \boldsymbol{h}_{\mathrm{text}}) \end{aligned}$$
新增的自注意力层以视觉令牌 $\boldsymbol{v}$ 与全部盒子控制令牌 $\boldsymbol{h}_{\mathrm{box}}$ 的拼接作为输入，使视觉特征在空间自注意力之后、文本交叉注意力之前与盒子约束进行交互。这一插入位置的选择使得盒子控制信号既能利用已聚合的空间上下文，又能在文本语义注入前施加运动引导。整个训练过程中，原模型的所有权重保持冻结，仅训练这一新增控制模块，从而保留基础模型的生成知识。

**训练管线：三阶段渐进式学习。** 这是 Boximator 实现从显式约束到隐式对齐的关键设计。第一阶段（S1）采用全硬盒约束并引入自跟踪（Self-Tracking）机制：模型被训练为在每个视频帧中同时生成场景内容和包围每个受控对象的彩色边界框，框的颜色由对象 ID 决定。这迫使模型学会将离散的盒子坐标与视觉元素建立关联。第二阶段（S2）引入软盒约束：在 80% 的训练样本中，中间帧的硬盒被替换为通过插值和松弛生成的软盒，使模型适应推理时用户仅指定少量关键帧的场景。第三阶段（S3）移除自跟踪目标，模型停止生成可见的彩色框，但盒子对齐能力得以保留——此时模型已将控制信号内化为隐式表示。

**推理管线：从稀疏约束到密集引导。** 推理时，用户只需在少数关键帧（通常为首帧和末帧）指定硬盒，或额外定义运动路径。系统自动完成两个步骤：首先，根据用户指定的硬盒或运动路径，通过线性插值生成中间帧的盒子位置；然后，对插值盒子施加边界松弛，将其转化为软盒约束。这些软盒作为密集的运动引导信号注入所有帧，与用户指定的硬盒共同构成完整的盒子约束序列，驱动模型生成符合运动意图的视频。

### 补充图表

![[assets/figures/papers/paper_list_l2_https_arxiv_org_abs_2402_01566/figures/002_Figure_2.jpg]]
*Figure 2: Overview of the control module: adding a new selfattention layer to every spatial attention block, between the spatial self-attention and the spatial cross attention. During training, all the original model parameters are frozen*

![[assets/figures/papers/paper_list_l2_https_arxiv_org_abs_2402_01566/figures/001_Figure.jpg]]

## 核心模块与公式推导

Boximator 的核心设计围绕一个轻量级控制模块展开，该模块以插件形式嵌入预训练视频扩散模型，冻结原模型全部权重，仅训练新增参数。其关键模块与公式如下。

### 盒子控制令牌编码

每个用户定义的约束盒子被编码为一个控制令牌 $\boldsymbol{t}_b$，输入包含三个分量：归一化坐标 $b_{\mathrm{loc}}$（边界框中心坐标与宽高）、对象标识 $b_{\mathrm{id}}$ 以及硬盒/软盒标志 $b_{\mathrm{flag}}$。三者拼接后经 Fourier 特征嵌入与 MLP 映射为连续表示：

$$
\boldsymbol{t}_b = \mathrm{MLP}(\mathrm{Fourier}([b_{\mathrm{loc}}, b_{\mathrm{id}}, b_{\mathrm{flag}}]))
$$

其中 Fourier 编码对归一化至 $[0,1]$ 的输入 $x$ 按如下方式计算：

$$
\mathrm{Fourier}(x) = [\cos(x \cdot 100^{0/8}), \dots, \cos(x \cdot 100^{7/8}), \sin(x \cdot 100^{0/8}), \dots, \sin(x \cdot 100^{7/8})]
$$

所有盒子的控制令牌组成固定长度的 $\boldsymbol{h}_{\mathrm{box}}$，当实际盒子数不足时以可学习的空令牌填充。

### 空间注意力改造

控制模块的核心改动发生在视频扩散模型的空间注意力块中。原始空间注意力块的标准顺序为空间自注意力（SelfAttn）后接空间交叉注意力（CrossAttn）。Boximator 在两者之间插入一个新增的自注意力层，其输入为视觉令牌 $\boldsymbol{v}$ 与盒子控制令牌 $\boldsymbol{h}_{\mathrm{box}}$ 的拼接，形式化为：

$$
\begin{aligned}
\boldsymbol{v} &= \boldsymbol{v} + \mathrm{SelfAttn}(\boldsymbol{v}) \\
\boldsymbol{v} &= \boldsymbol{v} + \mathrm{TS}(\mathrm{SelfAttn}([\boldsymbol{v}, \boldsymbol{h}_{\mathrm{box}}])) \\
\boldsymbol{v} &= \boldsymbol{v} + \mathrm{CrossAttn}(\boldsymbol{v}, \boldsymbol{h}_{\mathrm{text}})
\end{aligned}
$$

其中 $\mathrm{TS}$ 表示仅取视觉令牌对应输出的时间步切片操作。该层使视觉特征能够显式地与盒子约束交互，为后续的运动控制对齐提供结构基础。

### 自跟踪训练机制

自跟踪（Self-Tracking）是 Boximator 实现盒子-物体关联的关键训练策略。其核心思想是：在第一阶段训练中，强迫模型在生成视频帧的同时，为每个受约束对象生成对应颜色的可见边界框（颜色由该对象的控制令牌指定）。这相当于将困难的控制信号到视觉元素的直接映射，分解为“生成正确颜色框”和“将框与约束对齐”两个更简单的子任务。

训练损失沿用视频扩散模型的标准噪声预测损失：

$$
\mathcal{L}_{\theta} = \mathbb{E}_{z_0, c, \epsilon, t} \left[||\epsilon - \epsilon_{\theta}(z_t, t, c)||_2^2\right]
$$

其中 $z_t = \sqrt{\bar{\alpha}_t} z_0 + \sqrt{1 - \bar{\alpha}_t} \epsilon$ 为前向扩散过程的加噪潜变量，条件 $c$ 包含文本嵌入与盒子控制令牌。自跟踪阶段不修改损失函数形式，而是通过训练数据中叠加的彩色跟踪框作为目标信号，引导模型建立盒子与物体区域的对应关系。

### 软盒推理模块

推理时，用户通常仅在首尾帧指定硬盒约束。为向中间帧提供运动引导，Boximator 构建软盒（Soft Box）约束：对用户指定的硬盒对进行线性插值，或让盒子沿用户定义的运动路径滑动，并在每帧对插值结果施加松弛操作（扩大边界框范围），形成宽松的空间约束。这些软盒在推理时作为额外的控制令牌注入模型，无需用户逐帧标注。

### 补充图表

![[assets/figures/papers/paper_list_l2_https_arxiv_org_abs_2402_01566/figures/004_Figure_4.jpg]]
*Figure 4: Self-tracking: train the model to track every constrained object. This figure shows 3 frames where the black horse and the yellow box surrounding it are generated together*

![[assets/figures/papers/paper_list_l2_https_arxiv_org_abs_2402_01566/figures/005_Figure_5.jpg]]
*Figure 5: Soft boxes in inference. We interpolate soft boxes and relax them based on a pair of user-specified boxes (upper row), or a user-specified box combined with a motion path (lower row)*

![[assets/figures/papers/paper_list_l2_https_arxiv_org_abs_2402_01566/figures/003_Figure_3.jpg]]
*Figure 3: Training data: all bounding boxes are projected to the cropped region (white dashed box)*

## 实验与分析

### 主实验结果

Boximator 在两个基础视频扩散模型（**PixelDance** (Zeng et al., arXiv 2023) 和 **ModelScope** (Wang et al., arXiv 2023)）上均验证了其运动控制能力与视频质量的保持。

**MSR-VTT 零样本评估。** 如表 1 所示，Boximator 不仅保留了基础模型的视频质量，甚至有所提升。以 PixelDance 为基座时，不提供首帧条件下，FVD 从 237 降至 174（降低 63 点）；以 ModelScope 为基座时，FVD 从 239 降至 216。盒子对齐指标 mAP 的提升更为显著：PixelDance+Boximator 在加入盒约束后，mAP 从无盒条件的 0.059 跃升至 0.349（提升 0.290），验证了硬/软盒约束对运动控制的直接有效性。

**ActivityNet 盒子对齐。** 在 ActivityNet 数据集上，加入盒约束使 mAP 达到无盒条件的 4.4–8.9 倍（见表 2）。该数据集采用人工扩展标注，可信度高于自动标注的 MSR-VTT 和 UCF-101，进一步巩固了 Boximator 的运动控制能力。

**UCF-101 零样本评估。** 在 UCF-101 上，PixelDance+Boximator FO+Box 的 mAP 达到 0.284，而无盒条件仅为 0.060（提升 0.224，见表 5）。需注意 UCF-101 因长文本描述导致自动标注的噪声盒子增多，绝对 AP 值偏低，但相对提升趋势与 MSR-VTT 一致。

**人类评估。** 100 个样本的盲比结果显示，Boximator 在运动控制维度以 76.0% 的偏好率显著优于基础模型（见表 3）。评估者不知晓模型来源，随机顺序呈现，确保了评估的公平性。

### 消融研究

表 4 的消融实验揭示了 Boximator 各设计组件的因果贡献：

1. **自跟踪（Self-Tracking）是关键使能技术。** 移除自跟踪后，MSR-VTT Box 条件下的 mAP 从 0.349 骤降至 0.118。仅使用标准噪声预测损失训练 110K 步后，模型仍无法对齐大多数盒约束，这直接证明了自跟踪将困难的控制对齐问题分解为“生成正确颜色框”和“对齐约束”两个可学习子任务的有效性。

2. **软盒（Soft Box）约束不可或缺。** 推理时取消软盒约束、仅保留用户定义的硬盒，导致 mAP 从 0.349 降至 0.235。软盒在用户未指定盒子的帧上提供插值后的宽松运动引导，对维持时间一致性至关重要。

3. **冻结基础模型权重优于全参数训练。** 训练全部 U-Net 参数（不解冻基础模型）并未带来额外收益——ActivityNet FO+Box 下 mAP 仅为 0.331，低于冻结方式的 0.394。这表明 Boximator 的控制模块设计已足够有效，冻结权重还有效保留了基础模型的先验知识。

4. **三阶段训练策略的渐进收益。** 仅第一阶段（硬盒+自跟踪）即可达到 0.294 的 mAP，加入软盒和后续阶段后进一步提升至 0.349，验证了“先学会精确跟踪，再学会隐式对齐”的课程学习策略的必要性。

### 失败模式与局限性

Boximator 在以下场景表现出局限性：

- **自动标注噪声。** UCF-101 上因长文本导致 Grounding DINO + DEVA 自动标注的盒子质量下降，绝对 mAP 偏低。评估指标受标注质量影响，需结合人类评估来全面判断运动控制质量。
- **域外泛化。** 训练数据源自 WebVid-10M 的高动态子集（1.1M 视频），模型在域外场景的泛化能力尚未充分验证。
- **架构覆盖有限。** 当前仅在 PixelDance 和 ModelScope 两种基于 U-Net 的视频扩散模型上验证，未在 Transformer-based 架构上测试。
- **控制形式受限。** 盒子控制限于矩形框，无法直接处理形变、遮挡等更复杂的运动细节。

### 图表核心结论

- **图 6(b)**：盒约束引导模型生成“婴儿横跨整个画面”的大幅运动，而无盒约束时该运动难以生成，体现了 Boximator 对影响画面大部分区域的运动的控制能力。
- **图 6(c)**：盒约束可泛化至复合对象（如“a man on a horse”），模型正确地将“人+马”作为整体向左边缘移动，展示了盒子视觉接地的组合泛化能力。

### 补充图表

![[assets/figures/papers/paper_list_l2_https_arxiv_org_abs_2402_01566/figures/006_Table_1.jpg]]
*Table 1: Zero-shot results on MSR-VTT. F0 means given the first frame as condition. Box means box constraints. The results show that Boximator retains or improves the video quality (FVD) of the base models. In all cases, adding box constraints (Box) significantly improves the average precision (AP) score of bounding box alignment*

![[assets/figures/papers/paper_list_l2_https_arxiv_org_abs_2402_01566/figures/007_Table_4.jpg]]
*Table 4: Ablation study: removing self-tracking and soft boxes both result in significant drop in the box alignment metric. Training all model weights doesn’t give extra benefits*

![[assets/figures/papers/paper_list_l2_https_arxiv_org_abs_2402_01566/figures/008_Table_2.jpg]]
*Table 2: Box alignment results on ActivityNet. In all cases, adding box constraints significantly improves the AP score*

![[assets/figures/papers/paper_list_l2_https_arxiv_org_abs_2402_01566/figures/009_Table_3.jpg]]
*Table 3: Human side-by-side blind comparison on 100 samples*

![[assets/figures/papers/paper_list_l2_https_arxiv_org_abs_2402_01566/figures/011_Table_5.jpg]]
*Table 5: Zero-shot results on UCF-101*

![[assets/figures/papers/paper_list_l2_https_arxiv_org_abs_2402_01566/figures/010_Figure_6.jpg]]
*Figure 6: Case study: (a) Generation and motion control based on four boxes; (b) A motion that affects significant portion of the frame; (c) Box defined on a combination of objects (e.g., “a man on a horse”); (d) Adding new objects to the scene*

![[assets/figures/papers/paper_list_l2_https_arxiv_org_abs_2402_01566/figures/012_Figure_7.jpg]]
*Figure 7: Sample videos from human evaluation (Part 1). Each group displays two rows: the first generated by the Boximator model and the second by the base model. Vote results are denoted as X/Y/Z, indicating raters’ preferences: X for Boximator model, Y for no preference, and Z for base model*

## 方法谱系与知识库定位

Boximator 作为视频扩散模型的即插即用运动控制模块，其设计思路与现有可控视频生成方法形成了清晰的对比与互补关系。

### 与基线方法的关系

Boximator 构建于两类基础视频扩散模型之上：**PixelDance** (Zeng et al., arXiv 2023) 和 **ModelScope** (Wang et al., arXiv 2023)。其核心设计原则是冻结基础模型的全部权重，仅训练新增的控制模块，从而完整保留基模型原有的视频生成知识。这种冻结策略与许多需要对基模型进行全参数微调的控制方法形成对比——消融实验表明，训练全部U-Net参数反而不会带来运动控制的额外收益（ActivityNet FO+Box 下 mAP 仅 0.331，低于冻结方式的 0.394）。

在可控视频生成的谱系中，Boximator 与以下工作构成参照系：
- **Make-A-Video** (Singer et al., arXiv 2022)：纯文本驱动的视频生成模型，缺乏显式的空间运动约束能力。
- **VideoComposer** (Wang et al., arXiv 2023)：支持多条件（如深度图、草图）控制的视频合成模型，但未专门针对离散盒子坐标与对象ID的时空对齐问题设计学习机制。

Boximator 的关键区别在于引入了**自跟踪（Self-Tracking）**范式：通过强制模型生成彩色跟踪框作为中间表示，将困难的控制-视觉关联问题分解为“生成正确颜色框”和“对齐约束”两个子任务。这一设计使得模型在可见框消失后仍能保留隐式对齐能力，而标准训练即使经过 110K 步优化也无法有效学习盒子与物体的关联。

### 适用边界

Boximator 的适用边界受以下因素制约：

1. **基模型架构依赖**：当前仅验证了 PixelDance 和 ModelScope 两种基于 U-Net 的视频扩散模型，尚未在 Transformer-based 架构上测试其即插即用能力。
2. **控制形式限制**：盒子约束限于矩形边界框，无法直接处理物体形变、遮挡、旋转等更精细的运动细节。
3. **训练数据分布**：训练数据源自 WebVid-10M 中筛选的 1.1M 高动态片段，域外场景（如医学影像、极端光照）的泛化能力未经验证。
4. **视频长度限制**：当前实验均在 16 帧视频上进行，更长视频上的盒子跟踪稳定性是开放问题。
5. **自动标注噪声**：MSR-VTT 和 UCF-101 使用 Grounding DINO + DEVA 自动标注盒子，标注噪声会影响绝对 AP 值的可解释性——尤其在 UCF-101 上因长文本导致噪声盒子增多，指标偏低。

### 局限与开放问题

**已知局限**：
- 自跟踪阶段依赖模型生成可见的彩色框，这在某些视觉场景（如暗色背景上的深色物体）中可能引入生成伪影。
- 软盒的插值与松弛参数目前采用固定策略，缺乏自适应调整机制。
- 多物体重叠场景下的盒子-物体关联仍存在挑战，尤其在物体外观相似时。

**开放问题**：
- 自跟踪范式能否推广到其他控制信号（如关键点、骨架、深度图），以简化扩散模型对多样化条件的对齐学习？
- 软盒的生成策略是否存在基于运动预测或内容感知的更优自动化方式？
- 如何将 Boximator 扩展到更长视频（>16 帧）并保持稳定的跨帧盒子跟踪？
- 能否在无需额外训练的零样本自适应框架中实现盒子控制，使方法更具即插即用性？
- 将盒子约束与文本描述、图像条件进行深度融合，是否可进一步提升控制粒度和视频质量？

## 原文 PDF

![[paperPDFs/arxiv_2024/Boximator_Generating_Rich_and_Controllable_Motions_for_Video_Synthesis.pdf]]
