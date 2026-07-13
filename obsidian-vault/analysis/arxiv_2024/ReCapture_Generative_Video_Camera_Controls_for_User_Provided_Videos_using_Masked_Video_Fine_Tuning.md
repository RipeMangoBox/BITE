---
title: "ReCapture: Generative Video Camera Controls for User-Provided Videos using Masked Video Fine-Tuning"
type: paper
paper_level: A
venue: arXiv
year: 2024
pdf_ref: paperPDFs/arxiv_2024/ReCapture_Generative_Video_Camera_Controls_for_User_Provided_Videos_using_Masked_Video_Fine_Tuning.pdf
project_link: null
code_link: null
aliases:
- ReCapture
tags:
- arxiv_2024
- topic/vision_multimodal_applications
- topic/generative_models_diffusion
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: 掩码视频微调（masked video fine‑tuning）结合上下文感知空间 LoRA 和时间运动 LoRA，利用掩码扩散损失忽略锚点视频中的无效区域，使预训练视频扩散模型能够保留已知运动并自动补全缺失内容。
primary_logic: 将用户视频的相机重定位分解为两阶段：首先生成带有空洞和噪声的锚点视频，再利用视频扩散模型的强大先验通过掩码微调修复和补全，从而避免了对配对4D训练数据的依赖，并能合理想象未观测区域。
claims:
- 在 Kubric-4D 数据集上，ReCapture 的 PSNR 达到 20.92，显著优于 Generative Camera Dolly 和其他 4D 重建方法。
- 在 VBench 评估中，ReCapture 的主体一致性（Subject Consistency）达到 88.53%，比 Generative Camera Dolly 的 83.02% 提高 5.51 个百分点。
- 消融实验证实掩码视频微调、空间 LoRA 和 SDEdit 后处理各自均带来显著提升。
- VBench 上 Subject Consistency = 88.53%
---

# ReCapture: Generative Video Camera Controls for User-Provided Videos using Masked Video Fine-Tuning

> [!tip] 核心洞察
> 将用户视频的相机重定位分解为两阶段：首先生成带有空洞和噪声的锚点视频，再利用视频扩散模型的强大先验通过掩码微调修复和补全，从而避免了对配对4D训练数据的依赖，并能合理想象未观测区域。

| 字段 | 内容 |
|------|------|
| 中文题名 | ReCapture：基于掩码视频微调的用户视频生成式相机控制 |
| 英文题名 | ReCapture: Generative Video Camera Controls for User-Provided Videos using Masked Video Fine-Tuning |
| 会议/期刊 | arXiv 2024 |
| Links | [paper](https://arxiv.org/abs/2411.05003) |
| Topic | #topic/vision_multimodal_applications #topic/generative_models_diffusion #topic/vision_multimodal_applications/image_and_video_generation |
| Method | ReCapture |
| Dataset | VBench, Kubric-4D |

> [!tip] 效果简介
> - VBench 上，Subject Consistency 88.53% vs 83.02% (Generative Camera Dolly) (+5.51%)。
> - Kubric-4D 上，PSNR (All) 20.92 vs 未提供具体基线值，文中声称优于 4D Gaussian Splatting 等方法 (N/A)。

## 概要

### 问题与瓶颈

用户拍摄的视频受限于原始相机的固定轨迹，无法事后调整视角来重新观察场景。现有视频扩散模型的可控相机技术（如 **Generative Camera Dolly**，Van Hoorick et al., arXiv 2024）虽然能生成新视角，但它们仅适用于模型自身生成的视频，无法处理用户提供的真实单目视频。核心瓶颈在于：从单目视频重建新视角时，既要保持场景中已有的动态运动，又必须合理填补因视角变化而暴露出的未观测区域——而现有方法缺乏在不依赖配对4D训练数据的前提下同时解决这两个问题的有效手段。

### 核心方法

ReCapture 将用户视频的相机重定位任务分解为两个阶段，其核心洞察是：**先利用图像级视图合成生成一个带有空洞和噪声的“锚点视频”，再借助预训练视频扩散模型的强大生成先验，通过掩码微调（masked fine-tuning）修复伪影并补全缺失内容**。这一设计避免了对配对4D训练数据的依赖，并能够合理“想象”未观测区域。

具体而言，第一阶段通过两种互补策略生成锚点视频：**深度点云渲染**（将每帧提升为3D点云后投影到新相机姿态）和**多视图图像扩散**（逐帧生成新视图）。第二阶段则采用**掩码视频微调**，在锚点视频上同时训练时间 LoRA 和上下文感知的空间 LoRA——时间 LoRA 使用掩码扩散损失忽略无效区域以保留已知运动，空间 LoRA 在源帧上学习场景外观先验——最终通过 SDEdit 后处理消除残余模糊，输出干净且时空一致的视频。

### 方法定位

在方法谱系中，ReCapture 位于**生成式动态新视角合成**与**视频扩散模型微调**的交叉点。与依赖4D仿真配对数据的 Generative Camera Dolly 不同，ReCapture 仅需用户提供的单目视频即可工作；与基于显式4D表示的重建方法（如 **DynIBaR**、**4D Gaussian Splatting**，Wu et al., CVPR 2024）相比，ReCapture 无需多视图同步视频，而是利用视频扩散模型隐式编码的运动和外观先验来补全缺失信息。其关键创新——掩码扩散损失结合双路 LoRA 微调——为将大规模预训练视频模型适配到用户视频级别的相机控制任务提供了新的技术范式。

### 主要结果

在 Kubric-4D 数据集上，ReCapture 的 PSNR 达到 20.92，显著优于 Generative Camera Dolly 及其他4D重建方法（Table 2）。在 VBench 基准上，ReCapture 的主体一致性（Subject Consistency）达到 88.53%，比 Generative Camera Dolly 的 83.02% 高出 5.51 个百分点（Table 1）。消融实验进一步证实，掩码视频微调、空间 LoRA 和 SDEdit 后处理三个组件各自均带来显著性能提升（Table 3），验证了方法设计的有效性。

### 问题背景

用户拍摄的视频受限于录制时的相机轨迹，观众只能从固定的视角观察场景。若能对任意用户视频施加任意的相机控制——例如环绕拍摄、推拉镜头或平移视角——将极大拓展视频创作的自由度。然而，从单目视频生成新视角视频面临双重挑战：一方面需要保持原始场景的动态内容（人物动作、物体运动），另一方面必须合理想象并填补因视角变化而暴露出的未观测区域。

### 现有方法的局限

传统的新视角合成方法主要依赖显式的4D场景重建。例如，**DynIBaR** 等基于体素图像渲染的方法需要多视图同步视频作为输入，通过重建动态神经辐射场来渲染新视角。**4D Gaussian Splatting**（Wu et al., CVPR 2024）则采用动态高斯泼溅表示，同样依赖多视图数据。这些重建类方法对输入条件要求苛刻，难以处理用户随手拍摄的单目视频。

近年来，视频扩散模型展现出强大的生成先验，催生了生成式相机控制方法。**Generative Camera Dolly**（Van Hoorick et al., arXiv 2024）首次尝试利用视频扩散模型实现动态场景的新视角合成，但其训练依赖4D仿真环境中的配对视频数据，无法泛化到真实用户视频。此外，该方法采用端到端的视频到视频翻译范式，缺乏对未观测区域的结构化处理机制。

**核心瓶颈**在于：现有可控相机技术要么依赖多视图同步采集（重建类方法），要么需要4D配对训练数据（生成类方法），均无法直接处理用户提供的任意单目视频，且缺乏从单目视频重建新视角并同时保持场景动态和填补未观测区域的有效方法。

### 本文动机

本文提出 **ReCapture**，旨在突破上述限制，实现对用户视频的生成式相机控制。核心思路是将任务分解为两个阶段：

1. **锚点视频生成**：利用单目深度估计将源视频帧提升为3D点云，再投影到目标相机姿态，或使用多视图扩散模型逐帧生成新视图，得到带有空洞和噪声的“锚点视频”。
2. **掩码视频微调**：利用预训练视频扩散模型的强大运动先验，通过掩码扩散损失和低秩适应（LoRA）对锚点视频进行修复和补全，生成时空一致的干净视频。

这一设计使得 ReCapture **无需任何配对训练数据**，仅依赖用户提供的单目视频和目标相机轨迹，即可保留原始场景运动并合理想象未观测区域。该方法将问题重新定义为视频到视频的再生翻译任务，充分释放了视频扩散模型的内在先验能力。

## 核心方法与创新机理

ReCapture 的核心创新在于**将用户视频的相机重定位重构为一种无需配对训练数据的视频到视频翻译任务**，并通过**掩码视频微调（masked video fine‑tuning）**机制，使预训练视频扩散模型能够在保留原始场景运动的同时，合理填补新视角下未观测的区域。这一设计直接回应了现有方法的根本瓶颈：**生成式相机控制技术（如 Generative Camera Dolly）依赖4D仿真配对数据**，无法泛化到用户提供的真实单目视频；而传统4D重建方法（如 DynIBaR、4D Gaussian Splatting）则难以处理动态场景中的大面积遮挡和未观测内容。

### 关键 changed slots 分析

与基线方法相比，ReCapture 在三个关键维度上实现了结构性突破：

**1. 训练数据需求：从“配对依赖”到“单目自洽”**

Generative Camera Dolly（Van Hoorick et al., arXiv 2024）需要成对的4D视频数据——即同一动态场景在多个相机轨迹下的同步录制——来训练端到端的视频到视频模型。这种数据在实际场景中极难获取。ReCapture 完全消除了这一依赖：它仅需用户提供的一段单目视频和目标相机轨迹，通过两阶段流程（锚点视频生成 + 掩码视频微调）完成任务。第一阶段利用单目深度估计或多视图扩散模型生成带有空洞和噪声的锚点视频（anchor video），第二阶段则借助视频扩散模型的强大先验进行修复和补全。这种设计使得方法可以处理任意用户视频，无需任何形式的配对训练数据。

**2. 视频生成流程：从“端到端黑箱”到“两阶段可控修复”**

Generative Camera Dolly 采用端到端的生成范式，直接从源视频和目标相机参数映射到输出视频，其内部表示和失败模式难以诊断。ReCapture 将流程显式分解为两个可解释的阶段（见 Figure 2）：

- **锚点视频生成**：通过深度点云渲染（将每帧提升为3D点云后重新投影，见公式 $\mathcal{P}_i = \phi([\mathbf{I}_i, \mathbf{D}_i], \mathbf{K})$ 和 $\mathbf{V}^{a} = \{\psi(\mathcal{P}_i, \mathbf{K}, \mathbf{P}_i)\}$）或多视图图像扩散（逐帧生成新视角，见公式 $p(\mathbf{I}_{i}^{a} \mid \mathbf{I}_{i}, \mathbf{P}_{cond}, \mathbf{P}_{i})$），产生一个包含空洞、噪声和伪影的粗糙锚点视频。这一阶段明确暴露了哪些区域因视角变化而缺失（如 Figure 4 所示的有效像素掩码），为后续修复提供了精确的指导信号。
- **掩码视频微调**：在锚点视频上对预训练视频扩散模型进行微调，利用掩码扩散损失（masked diffusion loss）仅对有效像素区域计算损失，使模型专注于修复缺失内容而非重建已知区域。

这种分解不仅提升了方法的可解释性，还使得每个阶段的失败模式可以被独立诊断和改进。

**3. 微调策略：从“全参数微调”到“掩码损失 + 双 LoRA 架构”**

这是 ReCapture 最具技术深度的创新。标准的视频扩散模型微调通常使用全参数更新或单一损失函数，但直接应用于锚点视频会因大量无效像素而引入噪声梯度。ReCapture 引入了三个协同设计的组件：

- **掩码扩散损失**：在时间维度上，仅对锚点视频中有效像素（即掩码 $\mathbf{M}^{a}$ 标记的区域）计算扩散损失 $\mathcal{L}_{temp} = \mathbb{E}_{\epsilon, t} [\mathbf{M}^{a} \cdot |\epsilon - \epsilon_{\theta}(\mathbf{V}_{t}^{a}, t, y)|]$，确保模型不会试图“重建”空洞区域，而是利用扩散先验进行合理想象。
- **时间 LoRA**：通过低秩适应（LoRA，权重更新公式 $W = W_{0} + BA$）在时间层注入运动信息，使模型学习从锚点视频的噪声帧序列中恢复连贯的运动模式。消融实验（Table 3）证实，仅使用时间 LoRA 与掩码损失即可显著提升时间一致性。
- **上下文感知空间 LoRA**：在源视频帧上计算标准扩散损失 $\mathcal{L}_{spatial} = \mathbb{E}_{\epsilon, t, i \sim \mathcal{U}\{0, \dots N-1\}} [\| \epsilon - \epsilon_{\theta}((\mathbf{I}_{i, t}), t, y) \|]$，使模型保留原始场景的外观和细节特征。这一设计确保修复后的视频在视觉上与源视频保持一致，而非生成风格漂移的内容。

此外，SDEdit 后处理（在空间 LoRA 基础上省略时间 LoRA 进行去模糊）进一步消除了残余模糊，将整体质量推向最优（Table 3 中 “+++ SD-Edit” 达到最佳指标）。

### 创新性的因果机制

这些 changed slots 并非孤立改进，而是形成了一个**因果闭环**：单目数据可用性（slot 1）使得两阶段流程成为可能（slot 2），而两阶段流程中锚点视频的“不完整性”又催生了对掩码微调策略的需求（slot 3）。掩码损失确保模型不被无效像素误导，双 LoRA 架构则分别处理运动连贯性和外观保真度这两个相互制约的目标。最终，这一设计使得 ReCapture 在 VBench 的主体一致性（Subject Consistency）上达到 88.53%，比需要配对数据的 Generative Camera Dolly（83.02%）高出 5.51 个百分点（Table 1），同时在 Kubric-4D 数据集上取得了 20.92 的 PSNR（Table 2），验证了“无配对数据”范式不仅可行，而且在关键指标上超越了依赖配对数据的方法。

ReCapture 提出了一种**两阶段视频到视频翻译**范式，将用户提供的单目视频与任意目标相机轨迹作为输入，输出一段在新视角下保持场景动态一致的重渲染视频。其核心设计哲学是：**不依赖成对的4D训练数据，而是借助预训练视频扩散模型的强大生成先验，通过“生成—修复”的闭环完成相机重定位**。

### 两阶段流水线

整个框架由两个串行阶段构成，如图2所示：

**阶段一：锚点视频生成（Anchor Video Generation）**  
给定源视频帧 $\{\mathbf{I}_i\}_{i=0}^{N-1}$ 和目标相机姿态序列 $\{\mathbf{P}_i\}_{i=0}^{N-1}$，该阶段独立地将每一帧变换到新视角，生成一个**带有空洞、噪声和伪影的粗糙锚点视频** $\mathbf{V}^a$，同时输出对应的**有效性掩码** $\mathbf{M}^a$，标记哪些像素是有效投影区域。锚点视频的质量不需要很高——它仅作为第二阶段修复的初始化起点。具体实现提供两种互补方案：
- **深度点云渲染**：通过单目深度估计将每帧提升为3D点云 $\mathcal{P}_i = \phi([\mathbf{I}_i, \mathbf{D}_i], \mathbf{K})$，再投影到新相机姿态生成新视图。该方法在小幅度相机运动下效率高，但会在遮挡边界和未观测区域产生空洞。
- **多视图图像扩散**：对于大角度旋转，逐帧调用多视图扩散模型，以源帧和相对相机参数为条件生成新视图。该方法能合理想象未观测区域，但逐帧独立处理可能引入时间闪烁。

**阶段二：掩码视频微调（Masked Video Fine-Tuning）**  
这是ReCapture的核心创新。在锚点视频 $\mathbf{V}^a$ 上，对预训练视频扩散模型（Stable Video Diffusion）进行轻量级微调，目标是**修复伪影、补全缺失区域，同时保留源视频中的场景运动**。微调采用两种互补的低秩适应（LoRA）模块：

1. **时间LoRA + 掩码扩散损失**：仅对掩码 $\mathbf{M}^a$ 标记的有效区域计算扩散损失 $\mathcal{L}_{temp}$，迫使模型在保留已知运动的前提下，自动补全被遮挡或未观测的内容。时间LoRA捕获帧间运动一致性。
2. **空间LoRA + 标准扩散损失**：在源视频帧上随机采样并计算标准扩散损失 $\mathcal{L}_{spatial}$，使模型学习源视频的视觉外观和上下文信息，防止生成内容偏离原始场景。

两种LoRA在微调时联合优化，训练完成后，仅需对锚点视频执行标准推理即可获得干净的重渲染视频。

**后处理：SDEdit去模糊**  
微调后的视频可能存在残余模糊，框架在推理阶段追加一步SDEdit后处理：使用仅加载空间LoRA的视频扩散模型对输出视频进行轻度加噪再去噪，在保持结构的同时消除模糊，进一步提升视觉质量。

### 模块关系与数据流

```
源视频帧 → [深度估计/多视图扩散] → 锚点视频 + 掩码
                                            ↓
                              掩码视频微调（时间LoRA + 空间LoRA）
                                            ↓
                                    干净重渲染视频
                                            ↓
                                   SDEdit后处理 → 最终输出
```

整个流程的关键瓶颈在于**阶段二**：掩码微调是连接“粗糙锚点”与“高质量输出”的桥梁，它利用视频扩散模型的运动先验来修复阶段一无法处理的空洞和噪声，同时避免了对配对4D数据的依赖。消融实验（Table 3, Figure 8）证实，时间LoRA、空间LoRA和SDEdit三者各自均带来显著增益，移除任一组件都会导致时间一致性下降或视觉质量劣化。

ReCapture 将用户视频的相机重定位任务分解为两个核心阶段：**锚点视频生成**与**掩码视频微调**。其关键在于，第一阶段生成带有空洞和噪声的锚点视频，第二阶段利用预训练视频扩散模型的强大先验进行修复和补全，从而避免了对配对 4D 训练数据的依赖。

### 阶段一：锚点视频生成

该阶段的目标是，给定源视频帧 $\mathbf{I}_i$ 和目标相机轨迹，生成一个包含新视角但存在空洞和伪影的锚点视频 $\mathbf{V}^a$。ReCapture 提供了两种互补的生成路径：

**1. 深度点云渲染（Depth-based Point Cloud Rendering）**

首先，通过单目深度估计将每帧提升为 3D 点云：

$$
\mathcal{P}_{i} = \phi([\mathbf{I}_{i}, \mathbf{D}_{i}], \mathbf{K})
$$

其中 $\mathbf{D}_i$ 为估计的深度图，$\mathbf{K}$ 为相机内参，$\phi$ 表示将 RGBD 数据映射到相机坐标系下的 3D 点云。

随后，将点云投影到目标相机姿态 $\mathbf{P}_i$ 下，生成锚点视频帧序列：

$$
\mathbf{V}^{a} = \{\mathbf{I}_{0}^{a}, \ldots, \mathbf{I}_{N-1}^{a}\} = \{\psi(\mathcal{P}_{i}, \mathbf{K}, \mathbf{P}_{i}) \mid i \in \{0, \ldots, N-1\}\}
$$

$\psi$ 为投影函数。由于单目深度估计的噪声和相机移动带来的遮挡，生成的锚点帧会存在空洞和无效区域，这些区域在后续阶段由掩码机制排除。

**2. 多视图图像扩散（Multiview Image Diffusion）**

对于大角度旋转场景，深度点云渲染的缺失区域过大，ReCapture 引入多视图扩散模型逐帧生成新视图。该过程建模为条件分布：

$$
p(\mathbf{I}_{i}^{a} \mid \mathbf{I}_{i}, \mathbf{P}_{cond}, \mathbf{P}_{i})
$$

其中 $\mathbf{P}_{cond}$ 为条件相机姿态。为保持姿态表示对刚体变换的不变性，ReCapture 采用与 CAT3D 类似的 raymap 表示——计算相对于首帧相机姿态的 raymap，并将其通道级联到条件图像上。

> **瓶颈分析**：多视图扩散逐帧独立生成，天然缺乏时间一致性。这一缺陷正是第二阶段掩码视频微调需要解决的核心问题。

### 阶段二：掩码视频微调

该阶段是 ReCapture 的**因果调节变量**，通过两类低秩适应（LoRA）和掩码扩散损失，使预训练视频扩散模型在保留已知运动的同时自动补全缺失内容。

**LoRA 权重更新**遵循标准形式：

$$
W = W_{0} + \Delta W = W_{0} + B A
$$

其中 $W_0$ 为冻结的原始权重，$B$ 和 $A$ 为低秩因子。

**时间 LoRA 与掩码扩散损失**

时间 LoRA 作用于视频扩散模型的时间层，以锚点视频 $\mathbf{V}^a$ 为目标进行微调。其核心是掩码扩散损失，仅对有效像素计算损失：

$$
\mathcal{L}_{temp} = \mathbb{E}_{\epsilon, t} \left[ \mathbf{M}^{a} \cdot \left| \epsilon - \epsilon_{\theta} ( \mathbf{V}_{t}^{a} , t , y ) \right| \right]
$$

其中 $\mathbf{M}^a$ 为锚点视频的有效性掩码（1 表示有效像素，0 表示空洞/无效区域），$\epsilon_{\theta}$ 为扩散模型的噪声预测网络，$y$ 为条件信号。掩码机制确保模型仅从有意义的像素学习，而忽略第一阶段产生的空洞区域。

**空间 LoRA 与上下文感知损失**

为防止模型在修复空洞时遗忘源视频的视觉细节，ReCapture 额外引入上下文感知的空间 LoRA，在源视频帧上计算标准扩散损失：

$$
\mathcal{L}_{spatial} = \mathbb{E}_{\epsilon, t, i \sim \mathcal{U}\{0, \dots N-1\}} \left[ \| \epsilon - \epsilon_{\theta} ( (\mathbf{I}_{i, t}) , t , y ) \| \right]
$$

其中 $i$ 从源视频帧中均匀采样。空间 LoRA 使模型保留对原始场景内容的感知能力，与时间 LoRA 协同工作，在补全缺失区域的同时维持主体一致性。

**SDEdit 后处理**

微调完成后，ReCapture 使用空间 LoRA（省略时间 LoRA）对输出视频执行 SDEdit 去噪步骤，以消除残余模糊并增强帧间一致性。消融实验证实，这一后处理步骤对最终视觉质量有显著贡献。

## 实验与关键发现

### 主实验结果

ReCapture 在两个核心基准上展现出相对于现有方法的显著优势：生成式基线 **Generative Camera Dolly** (Van Hoorick et al., arXiv 2024) 和基于显式 4D 表示的重建方法（如 **4D Gaussian Splatting**, Wu et al., CVPR 2024）。

在 VBench 评估中，ReCapture 的主体一致性（Subject Consistency）达到 **88.53%**，相较 Generative Camera Dolly 的 83.02% 提升了 **5.51 个百分点**（Table 1）。这一指标的提升直接反映了方法在保持场景主体外观一致性方面的优势——即使在新视角下，生成视频中的人物和物体仍能与源视频保持高度一致的外观。

![[assets/figures/papers/paper_list_l6_https_arxiv_org_abs_2411_05003/figures/007_Table_1.jpg]]
*Table 1: Quantitative comparisons with Generative Camera Dolly on VBench*

在 Kubric-4D 数据集上，ReCapture 取得了 **20.92 的 PSNR**（Table 2），优于包括 4D Gaussian Splatting 在内的重建方法和生成式方法。这一结果验证了掩码视频微调策略的有效性：通过利用视频扩散模型的强大先验，方法能够在无需配对 4D 训练数据的情况下，合理补全因视角变化而暴露的未观测区域，同时保持场景的动态运动。

![[assets/figures/papers/paper_list_l6_https_arxiv_org_abs_2411_05003/figures/009_Table_2.jpg]]
*Table 2: Comparison results on Kubric-4D. We evaluate gradual dynamic view synthesis models following [82] to use video with resolution 384 × 256. Our method achieves superior performance compared to other reconstruction and generative methods*

### 消融研究

消融实验系统性地验证了 ReCapture 各组件对最终性能的贡献（Table 3, Figure 8）：

![[assets/figures/papers/paper_list_l6_https_arxiv_org_abs_2411_05003/figures/010_Table_3.jpg]]
*Table 3: Ablation studies for each component of mask video diffusion finetuning: ’+ Temporal LoRAs’ applies temporal LoRAs solely for masked video finetuning. ’++ Spatial LoRAs’ introduces additional context-aware LoRAs, using both spatial and temporal LoRAs for finetuning. ’+++ SD-Edit’ involves applying SD-editing after completing training with both LoRAs for eliminating blurriness*

![[assets/figures/papers/paper_list_l6_https_arxiv_org_abs_2411_05003/figures/011_Figure_8.jpg]]
*Figure 8: Detailed ablation of all components of our method*

**+ Temporal LoRAs（仅时间 LoRA + 掩码损失）**：仅应用时间 LoRA 进行掩码视频微调，即可从充满空洞和噪声的锚点视频中生成具有连贯运动的时间一致输出。掩码扩散损失在此阶段起到关键作用——它确保模型仅从有效像素区域学习，避免了无效区域对运动先验的污染。

**++ Spatial LoRAs（加入空间 LoRA）**：在时间 LoRA 基础上引入上下文感知的空间 LoRA，通过均匀采样源视频帧计算标准扩散损失，使模型能够保留源视频中的场景上下文和外观细节。这一组件进一步提升了视觉质量和主体一致性。

**+++ SD-Edit（加入 SDEdit 后处理）**：在完成双 LoRA 训练后，对输出视频应用 SDEdit 后处理。该步骤使用空间 LoRA（省略时间 LoRA）对生成视频进行去模糊和一致性增强，消除了残余的模糊伪影，使整体质量达到最佳水平。值得注意的是，SDEdit 在此并非独立的重建步骤，而是对已有时空一致输出的精细化后处理。

### 实验公平性说明

所有比较实验均在相同输出分辨率（384×256）下进行，且均以 Stable Video Diffusion 作为骨干网络，确保了比较的公平性。需要特别指出的是，Generative Camera Dolly 需要基于 4D 仿真环境的配对训练数据，而 ReCapture 仅需目标视频本身，无需任何配对数据，因此其泛化能力本质上更强——这一优势在真实用户视频上的表现尤为突出。

### 定性分析

Figure 5 展示了 ReCapture 与 Generative Camera Dolly 在轨道相机轨迹下的定性比较。Figure 6 提供了更广泛的生成视频画廊，展示了多种用户自定义相机轨迹（包括平移、旋转、推拉等）下的效果。Figure 7 直观展示了掩码视频微调阶段的效果：从充满空洞的锚点视频出发，经过第二阶段处理后，模型能够自动补全缺失区域并消除噪声，同时保持场景的动态运动。

![[assets/figures/papers/paper_list_l6_https_arxiv_org_abs_2411_05003/figures/005_Figure_5.jpg]]
*Figure 5: Comparisons with generative camera dolly [82] using an orbit camera trajectory*

![[assets/figures/papers/paper_list_l6_https_arxiv_org_abs_2411_05003/figures/006_Figure_6.jpg]]
*Figure 6: Gallery of generated videos with novel and unseen user-provided camera trajectories using ReCapture*

## 定位与知识库关联

### 任务定位与核心瓶颈

ReCapture 解决的是**用户提供单目视频的生成式相机重控制**问题：给定一段任意来源的视频，用户可自由指定新的相机轨迹，生成视角变化但场景动态保持一致的新视频。这一任务位于动态新视角合成（Dynamic Novel View Synthesis）与视频生成（Video Generation）的交汇处。

现有工作在此任务上存在根本性瓶颈：**视频扩散模型的可控相机技术（如 Generative Camera Dolly）仅适用于模型自身生成的视频，无法处理用户提供的真实视频**。同时，传统4D重建方法（如 DynIBaR、4D Gaussian Splatting）虽能从多视图或单目视频重建场景，但依赖显式几何表示，难以合理填补大面积未观测区域并保持动态场景的视觉一致性。ReCapture 的核心突破在于**将问题重新表述为视频到视频的翻译任务**，利用预训练视频扩散模型的强大运动先验，通过掩码微调策略避免了配对4D训练数据的依赖。

### 与基线方法的对比分析

#### 生成式动态新视角合成基线

**Generative Camera Dolly**（Van Hoorick et al., arXiv 2024）是唯一直接可比的开创性生成式基线。该方法训练端到端视频到视频模型，需要基于4D仿真环境的配对视频数据（源相机轨迹与目标相机轨迹的成对视频）。其关键局限在于：
- **数据依赖性**：需大量4D配对数据训练，泛化到任意用户视频的能力受限
- **训练范式**：全参数微调，计算开销大
- **视角范围**：在训练数据覆盖的相机运动范围内有效，对极端视角变化效果下降

ReCapture 在三个维度上实现了范式转变：

| 维度 | Generative Camera Dolly | ReCapture |
|------|------------------------|-----------|
| 训练数据需求 | 需成对4D视频数据 | 仅需用户提供的单目视频，无需任何配对数据 |
| 视频生成流程 | 端到端视频到视频模型 | 两阶段：锚点视频生成 + 掩码视频微调 |
| 微调策略 | 全参数微调或标准扩散损失 | 掩码扩散损失 + 低秩适应（时间LoRA + 空间LoRA） |

定量对比（Table 1，VBench评估）显示，ReCapture 在主体一致性上达到 **88.53%**，比 Generative Camera Dolly 的 83.02% 提高 **5.51个百分点**。在 Kubric-4D 数据集上（Table 2），ReCapture 的 PSNR 达到 **20.92**，显著优于包括 4D Gaussian Splatting 在内的重建方法。需注意，所有比较均在相同输出分辨率（384×256）下进行，且均使用 Stable Video Diffusion 作为骨干网络，保证了公平性。

#### 传统4D重建基线

- **DynIBaR**（基于体素图像渲染的4D重建）：利用时空点云和神经渲染从多视图视频重建动态场景，但需要同步多视图输入，无法从单目视频工作，且对新视角的补全能力受限于显式几何表示。
- **4D Gaussian Splatting**（Wu et al., CVPR 2024）：将3D高斯泼溅扩展到时间维度，可从单目视频重建动态场景。但其显式点云表示在遮挡区域和大角度旋转时会产生明显空洞和伪影，缺乏对未观测区域的合理想象能力。

ReCapture 通过引入视频扩散模型的生成先验，在第二阶段掩码微调中自动补全缺失内容，从根本上规避了显式几何方法的局限。

### 方法谱系中的知识继承与创新

ReCapture 的技术方案可视为多条研究脉络的交叉融合：

**1. 视频扩散模型与低秩适应（LoRA）**
继承自 Stable Video Diffusion 的预训练运动先验，通过 LoRA（$W = W_0 + \Delta W = W_0 + BA$）实现参数高效微调。创新点在于**分离设计时间LoRA和空间LoRA**：时间LoRA专注于学习目标相机轨迹下的时序运动模式，空间LoRA则保持源视频的上下文外观信息。

**2. 掩码扩散损失**
借鉴掩码自编码器（MAE）的思想，但将其引入扩散模型训练。通过掩码 $M^a$ 排除锚点视频中的无效像素，使模型仅从有效区域学习：
$$\mathcal{L}_{temp} = \mathbb{E}_{\epsilon, t} \left[ \mathbf{M}^a \cdot \left| \epsilon - \epsilon_\theta ( \mathbf{V}_t^a , t , y ) \right| \right]$$
这一设计使模型在修复空洞的同时保持已知区域的运动一致性，是方法有效性的关键。

**3. 锚点视频生成的两条路径**
- **深度点云渲染**：将单帧RGBD提升为3D点云（$\mathcal{P}_i = \phi([\mathbf{I}_i, \mathbf{D}_i], \mathbf{K})$），再投影到新相机姿态。适合小到中等相机运动，但深度估计误差和大面积遮挡会导致空洞。
- **多视图图像扩散**：逐帧使用多视图扩散模型（如CAT3D）生成新视角，适合大角度旋转。但逐帧独立生成会引入时间不一致性。

这两条路径的互补性使方法能适应不同幅度的相机运动，但论文未明确给出选择策略的自动化标准。

### 适用边界与开放问题

**已知适用场景：**
- 单目视频输入，无需多视图或深度传感器
- 支持多种相机轨迹（平移、环绕、自定义路径）
- 动态场景中保持主体运动一致性

**已知局限与待验证问题：**

1. **大面积遮挡区域的生成质量**：当相机运动揭示源视频中完全未观测的区域时，模型需依赖生成先验“想象”内容。论文未提供极端遮挡场景（如物体背面）的定量评估，此能力边界需进一步验证。

2. **深度估计器的依赖**：点云渲染路径依赖单目深度估计，论文未明确所使用的具体深度模型。深度估计的精度和泛化性直接影响锚点视频质量，进而影响最终结果。在复杂几何或透明/反射表面场景中，此依赖可能成为瓶颈。

3. **多视图扩散的时间一致性**：逐帧多视图生成缺乏时序约束，虽在第二阶段通过时间LoRA修复，但严重的时间不一致性（如剧烈光照变化）可能超出修复能力。论文未讨论是否在第一阶段有预处理措施。

4. **计算开销**：两阶段流程（锚点生成 + 掩码微调）比端到端方法增加了推理时间。论文未提供与基线的推理效率对比。

5. **相机轨迹的物理合理性**：方法假设用户提供的目标相机轨迹是平滑且物理可行的。对于不连续或违背场景几何的轨迹，锚点视频生成可能失败，论文未讨论此情况。

6. **动态物体的几何一致性**：对于快速运动或非刚性变形的物体，点云提升和投影可能产生严重伪影。方法依赖视频扩散模型的运动先验来修复，但在极端情况下可能产生不合理的运动。

### 在知识库中的定位

ReCapture 代表了**从显式4D重建到隐式生成式新视角合成**的范式转变。其核心贡献不在于提出全新的网络架构，而在于**将视频扩散模型的强大先验通过掩码微调策略适配到任意视频的相机重控制任务**。这一思路可推广到其他需要“保留已知、补全未知”的视频编辑任务，如视频修复、视角插值等。

后续工作可能沿以下方向展开：引入更强的深度估计或几何约束以改善锚点视频质量；设计端到端的单阶段方法以减少计算开销；扩展到手动物体运动与相机运动的联合控制；以及在更大规模的真实世界视频上验证泛化能力。

## 原文 PDF

![[paperPDFs/arxiv_2024/ReCapture_Generative_Video_Camera_Controls_for_User_Provided_Videos_using_Masked_Video_Fine_Tuning.pdf]]
