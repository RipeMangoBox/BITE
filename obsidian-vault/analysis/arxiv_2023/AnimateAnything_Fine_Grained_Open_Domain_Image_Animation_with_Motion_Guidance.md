---
title: "AnimateAnything: Fine-Grained Open Domain Image Animation with Motion Guidance"
type: paper
paper_level: A
venue: arXiv
year: 2023
pdf_ref: paperPDFs/arxiv_2023/AnimateAnything_Fine_Grained_Open_Domain_Image_Animation_with_Motion_Guidance.pdf
project_link: https://animationai.github.io/AnimateAnything
code_link: null
aliases:
- AnimateAnything
tags:
- arxiv_2023
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: 引入运动区域掩码引导和运动强度引导，通过合成训练数据和直接监督帧间差异，使视频扩散模型能够根据用户输入精确控制动画区域和速度。
primary_logic: 视频扩散模型具有强大的生成先验，但原始模型缺乏对局部运动和运动强度的显式控制。通过在潜空间拼接运动掩码并施加运动强度损失，能够在不破坏模型原有能力的情况下实现细粒度的交互式动画生成。
claims:
- 在MSR-VTT零样本测试上，AnimateAnything 的 FVD 达到 443，显著优于 VideoCrafter1 的 465。
- 运动区域引导消融实验表明，“掩码引导 + 冻结非移动区域”策略使运动掩码精确度达到 0.82。
- 运动强度引导消融表明，提出的运动强度损失使运动强度误差降至 2.36，优于仅使用 FPS 引导的方案。
- 定性结果展示了通过文本和运动掩码迭代地生成多个对象的复杂动画，验证了交互式生成能力。
---

# AnimateAnything: Fine-Grained Open Domain Image Animation with Motion Guidance

> [!tip] 核心洞察
> 视频扩散模型具有强大的生成先验，但原始模型缺乏对局部运动和运动强度的显式控制。通过在潜空间拼接运动掩码并施加运动强度损失，能够在不破坏模型原有能力的情况下实现细粒度的交互式动画生成。

| 字段 | 内容 |
|------|------|
| 中文题名 | AnimateAnything：基于运动引导的细粒度开放域图像动画 |
| 英文题名 | AnimateAnything: Fine-Grained Open Domain Image Animation with Motion Guidance |
| 会议/期刊 | arXiv 2023 |
| Links | [paper](https://arxiv.org/abs/2311.12886) · [Project](https://animationai.github.io/AnimateAnything) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/image_and_video_generation |
| Method | AnimateAnything |
| Dataset | MSR-VTT |

> [!tip] 效果简介
> - MSR-VTT (zero-shot) 上，FVD 443 vs 465 (VideoCrafter1) (-22)。

## 概要

**问题瓶颈**：现有图像动画方法大多局限于特定对象类别（如流体、人体部位或场景），难以泛化至任意开放域图像。更关键的是，这些方法普遍缺乏对**运动区域**（哪些部分动）和**运动强度**（动得多快）的细粒度控制，用户无法精确指定动画行为。

**核心思想**：AnimateAnything 利用视频扩散模型强大的生成先验，通过两个因果调节变量实现精细控制——**运动区域掩码**（在潜空间通道维度拼接，指定可动区域）和**运动强度引导**（通过直接监督帧间差异的损失函数，精确控制运动速度）。这一设计在不破坏模型原有生成能力的前提下，将图像动画从“整体猜测”转变为“局部可控”。

**方法定位**：该方法属于基于扩散模型的图像到视频生成范式，以 3D U-Net 为骨干，仅微调时间层。与 **VideoComposer**（Wang et al., arXiv 2023）的运动轨迹控制不同，AnimateAnything 引入运动掩码的条件化机制和运动强度损失，实现了更直接、更稳定的局部运动控制。

**主要结果**：
- 在 MSR-VTT 零样本测试上，FVD 达到 **443**，优于 VideoCrafter1 的 465（Table 1）。
- 运动区域消融实验表明，“掩码引导 + 冻结非移动区域”策略使运动掩码精确度达到 **0.82**（Table 3）。
- 运动强度消融表明，提出的运动强度损失使运动强度误差降至 **2.36**，优于仅依赖 FPS 引导的方案（Table 4）。
- 定性结果验证了通过文本和运动掩码迭代生成多对象复杂动画的交互能力（Figure 1）。

**局限与开放问题**：模型因训练资源限制未在高分辨率视频上训练，限制了高分辨率应用；运动阈值 $T_m$ 与不同视频内容类型的交互机制、损失权重 $\lambda$ 的定量影响，以及如何高效扩展至高分辨率生成，仍需进一步探索。



图像动画旨在为静态图像注入可控的运动，使其生成连贯的视频片段。这一任务在内容创作、视觉特效和交互式媒体中具有广泛的应用前景。然而，现有方法普遍面临两个核心瓶颈：**对象类别的封闭性**和**运动控制的粗糙性**。

一方面，主流的图像动画方法通常针对特定对象类别进行设计，例如流体模拟、场景动画或人体部位驱动，难以泛化至任意开放域图像。另一方面，即使部分基于视频扩散模型的方法（如 **VideoComposer** (Wang et al., arXiv 2023) 和 **VideoCrafter1**）展现出更强的生成能力，它们仍然缺乏对运动区域和运动速度的精细控制——用户无法精确指定“图像的哪个部分应该运动”以及“运动的速度有多快”。VideoComposer 虽然引入了运动轨迹控制，但其控制粒度仍无法满足细粒度交互式动画的需求；而 VideoCrafter1 等通用图像到视频模型则倾向于让整个图像产生整体运动，难以实现局部动画。

从生成范式来看，视频扩散模型为图像动画提供了强大的生成先验，但其原始设计并未显式建模局部运动区域和运动强度。这构成了一个关键的因果缺口：**模型具备生成能力，但缺乏可控性**。如果能够在潜空间中引入运动掩码条件化，并直接监督帧间差异，就有可能在保持模型原有生成质量的前提下，实现细粒度的交互式动画生成。

本文提出的 **AnimateAnything** 正是针对上述缺口，通过运动区域掩码引导和运动强度引导两项核心机制，首次在视频扩散框架中实现了对动画区域和速度的精确控制，从而将图像动画任务从封闭域推向开放域。



## 核心方法与创新机理

AnimateAnything 的核心创新在于为视频扩散模型引入了两种互补的细粒度运动控制机制，使其能够对任意开放域图像进行可控动画生成，而无需局限于特定对象类别。

### 创新一：运动区域掩码引导

现有图像动画方法通常缺乏对局部运动区域的显式控制，导致整个画面产生非预期的全局运动（例如，背景本应静止却发生漂移）。AnimateAnything 提出将运动区域掩码沿通道维度与视频潜变量拼接，并采用零初始化卷积权重，灵感来源于 ControlNet。具体而言，给定形状为 `(frames, height, width, channel)` 的带噪视频潜变量，模型将运动掩码在通道维度拼接，形成 `(frames, height, width, channel+1)` 的输入。

为进一步强化运动区域约束，模型在推理时采用**“掩码引导 + 冻结非移动区域”**策略：对于非运动区域，将其潜变量重置为参考图像首帧的对应值（见公式 $z_0' = (1 - m) \cdot z_0^0 + m \cdot z_0$），从而确保静止区域与参考图像严格一致。消融实验（Table 3）表明，该策略使运动掩码精确度达到 **0.82**，显著优于未使用冻结机制的方案。

为获取训练所需的运动掩码，论文提出了一种无监督的合成数据生成方法：从真实视频中基于帧间灰度差自动提取运动差异掩码（见公式 $d = \bigcup_{i=1}^{N-1} (|x_{gray}^i - x_{gray}^{i-1}| > T_m)$），阈值 $T_m$ 设为 5。

### 创新二：运动强度引导

传统方法仅通过帧率（FPS）隐式控制运动速度，这是一种全局调整，缺乏对运动幅度的直接约束。AnimateAnything 引入**运动强度**这一显式可控变量，定义为潜空间中帧间差异的平均值：

$$s(z) = \frac{1}{N-1} \sum_{i=1}^{N} |z^i - z^{i-1}|$$

在此基础上，论文设计了**运动强度损失**，直接监督生成视频的帧间差异：

$$l_s = || s(z_0) - s(\hat{z}_0) ||_2^2$$

其中 $\hat{z}_0$ 是从噪声预测中恢复的估计干净潜变量。该损失与标准扩散噪声预测损失联合优化，总损失为 $l = l_\epsilon + \lambda \cdot l_s$，$\lambda$ 设为 0.001。运动强度值被投影为位置嵌入，注入到 3D U-Net 的每个残差块中，使模型能够感知并遵循用户指定的运动速度。

消融实验（Table 4）验证了该设计的有效性：运动强度损失使运动强度误差降至 **2.36**，而仅使用 FPS 引导的方案在稳定性和准确性上均不及此方法。定性结果（Figure 4）进一步展示了运动强度对动画速度的精细调控能力——适度增强运动强度可加速蒙娜丽莎表情变化，但过度增强会导致面部细节丢失。

### 与 Baseline 的核心差异

| 控制维度 | Baseline 方案 | AnimateAnything 方案 |
|---------|-------------|-------------------|
| 运动区域 | 无掩码引导，整体可能产生非预期运动 | 通道维度拼接运动掩码 + 冻结非移动区域潜变量 |
| 运动速度 | 通过 FPS 隐式全局调整 | 引入运动强度度量 + 直接监督帧间差异的损失函数 |

这两种控制机制相互独立且可组合使用：用户可以同时指定“哪些区域运动”和“运动多快”，实现细粒度的交互式动画生成（如 Figure 1 后三行所示的迭代式多对象动画）。



AnimateAnything 的整体 pipeline 围绕一个预训练的 **3D U-Net 视频扩散骨干** 构建，目标是将单张参考图像转化为可控的动画视频。其核心设计思想是在不破坏扩散模型原有生成能力的前提下，通过潜空间拼接与嵌入注入的方式引入显式的运动控制信号，实现细粒度的开放域图像动画。

### 输入输出流与模块关系

整个流程的输入由三部分组成：一张参考图像、一段描述运动的文本提示，以及用户可选的运动区域掩码与运动强度值。输出为一段包含 N 帧的动画视频。

如图 Figure 2 所示，pipeline 包含以下关键模块及其信息流：

![[assets/figures/papers/paper_list_l1038_https_arxiv_org_abs_2311_12886/figures/002_Figure_2.jpg]]
*Figure 2: Overview of our pipeline. We adopt the widely used 3D U-Net based video diffusion model [11, 52] for image animation. Given a noisy video latent with shape (frames, height, width, channel), we concatenate the clean latent of the reference image and the noisy frames in the temporal dimension. Additionally, we concatenate the motion area mask with the video latent in the channel dimension. This results in the input latent with shape (frames+1, height, width, channel+1) for the 3D U-Net. To control the motion strength of the generated video, we project the motion strength as positional embedding and concatenate it with the time step embedding*

1. **VAE 编码参考图像**：参考图像首先经由预训练的 VAE 编码器映射至潜空间，得到干净潜变量 $z_{\text{ref}}$。该潜变量将作为生成视频的首帧内容锚点。

2. **运动区域掩码条件化**：运动区域掩码 $m$ 在通道维度上与视频潜变量进行拼接。具体而言，输入 3D U-Net 的潜变量形状由原始的 `(frames, H, W, C)` 扩展为 `(frames+1, H, W, C+1)`——其中 `+1` 在时间维度上对应拼接的参考图像潜变量，`+1` 在通道维度上对应拼接的运动掩码。这一设计受 ControlNet 启发，新增加的卷积权重以零初始化，确保训练初期不会干扰预训练模型的先验。

3. **3D U-Net 视频扩散骨干**：该骨干包含时空注意力机制，负责从带噪潜变量中预测噪声。为降低训练成本，模型仅微调时间层参数，空间层权重保持冻结。

4. **运动强度条件化**：运动强度值被投影为位置嵌入，并与时间步嵌入进行拼接后注入到 3D U-Net 的每个残差块中，从而实现对运动速度的全局调控。

5. **共享噪声推理**（测试时）：在推理阶段，模型采用共享噪声策略——将参考图像潜变量按扩散调度添加噪声后作为初始噪声，在不同帧之间引入可控的多样性，同时维持与参考图像的内容一致性。

### 训练数据构造的关键设计

为实现运动区域和运动强度的有效监督，AnimateAnything 引入了两种训练数据构造机制：

- **合成运动掩码生成**：从真实视频中自动提取运动区域掩码。具体而言，通过计算帧间灰度差并设定阈值 $T_m$ 来生成运动差异掩码 $d$（见公式 (4)）。在训练过程中，模型将掩码与视频潜变量拼接，并在去噪后通过后处理操作将非运动区域的潜变量重置为第一帧的值（见公式 (5)），从而强化模型对运动区域的遵循能力。

- **运动强度损失**：定义潜空间中的运动强度度量 $s(z)$ 为帧间差异的平均值（见公式 (6)），并引入直接监督帧间差异的损失函数 $l_s$（见公式 (7)）。该损失与标准的噪声预测损失 $l_\epsilon$ 联合优化（见公式 (9)），使模型能够精确控制生成视频的运动幅度。

### 从瓶颈到设计的因果链路

现有图像动画方法面临的核心瓶颈在于：**缺乏对运动区域和运动速度的精细控制**，导致难以应用于包含多对象的开放域图像。AnimateAnything 的 pipeline 设计直接针对这一瓶颈：

- **运动区域控制**通过通道维度的掩码拼接与潜空间后处理实现，使模型能够精确限定动画发生的空间范围，避免非目标区域的意外运动。
- **运动强度控制**通过损失函数直接监督帧间差异，替代了传统方法中依赖 FPS 的隐式全局调控，提供了更稳定且可量化的运动速度控制手段。

这种“条件拼接 + 损失监督”的双重机制，使得视频扩散模型的强大生成先验得以被精准引导，同时保持了模型对任意开放域图像的泛化能力。



AnimateAnything 围绕视频扩散模型构建，通过两个核心控制模块——**运动区域掩码引导**和**运动强度引导**——实现对开放域图像动画的细粒度控制。整体流程如 Figure 2 所示。

### 3D U-Net 视频扩散骨干

方法采用基于 3D U-Net 的视频扩散模型作为生成骨干。前向扩散过程逐步向视频潜变量 $z_0$ 添加高斯噪声，单步加噪可表示为：

$$z_t = \sqrt{\bar{\alpha}_t} z_0 + \sqrt{1-\bar{\alpha}_t} \epsilon, \quad \epsilon \sim \mathcal{N}(0, I)$$

扩散模型通过预测噪声进行训练，基础损失函数为：

$$l_\epsilon = ||\epsilon - \epsilon_\theta(z_t, t, c)||_2^2$$

其中 $\epsilon_\theta$ 为噪声预测网络，$c$ 为条件信息。训练时仅微调时间层参数，以保留预训练模型的生成先验。

### 运动区域掩码条件化

为实现对局部运动区域的精确控制，模型在潜空间中将运动掩码 $m$ 沿通道维度与视频潜变量拼接，形成形状为 $(frames+1, H, W, channel+1)$ 的输入。运动掩码的卷积权重初始化为零，以在微调初期保持模型原有行为。

训练数据的运动掩码通过无监督方式从真实视频自动生成。给定视频帧序列，首先计算相邻帧灰度图的绝对差，然后通过阈值 $T_m$ 二值化得到运动差异掩码：

$$d = \bigcup_{i=1}^{N-1} (|x_{gray}^i - x_{gray}^{i-1}| > T_m)$$

为进一步强化运动区域引导，在推理时对预测的干净潜变量 $\hat{z}_0$ 进行后处理，将非运动区域潜变量重置为参考图像第一帧的对应值：

$$z_0' = (1 - m) \cdot z_0^0 + m \cdot z_0$$

这一“掩码引导 + 冻结非移动区域”策略是运动区域控制精度的关键，消融实验表明其运动掩码精确度达到 0.82（Table 3）。

### 运动强度条件化与运动强度损失

运动强度 $s(z)$ 用于量化潜空间中帧间运动的幅度：

$$s(z) = \frac{1}{N-1} \sum_{i=1}^{N} |z^i - z^{i-1}|$$

运动强度值被投影为位置嵌入，与时间步嵌入拼接后注入到 3D U-Net 的每个残差块中，使模型能够感知并响应目标运动速度。

为直接监督运动强度，方法引入运动强度损失。首先从噪声预测中恢复估计的干净潜变量：

$$\hat{z}_0 = \frac{z_0 - \sqrt{1 - \bar{\alpha}_t} \epsilon_\theta(z_t, t, c)}{\sqrt{\bar{\alpha}_t}}$$

然后计算估计潜变量与真实潜变量之间运动强度的均方误差：

$$l_s = || s(z_0) - s(\hat{z}_0) ||_2^2$$

最终训练损失为噪声预测损失与运动强度损失的加权联合：

$$l = l_\epsilon + \lambda \cdot l_s$$

其中 $\lambda$ 为运动强度损失的缩放因子，在实现中设为 0.001。消融实验（Table 4）表明，该方案的运动强度误差降至 2.36，相比仅使用 FPS 隐式引导的方案更稳定且准确。

### 共享噪声推理

测试时，为在保持参考图像保真度的同时引入帧间多样性，采用共享噪声初始化策略。对每一帧的噪声潜变量，以参考图像潜变量 $z_{ref}$ 为基础添加共享噪声：

$$z_T^i = \sqrt{\bar{\alpha}_T} z_{ref} + \sqrt{1 - \bar{\alpha}_T} \epsilon^i$$

该设计使所有帧共享参考图像的内容结构，同时通过不同的噪声分量 $\epsilon^i$ 产生帧间变化，有效平衡了图像保真度与运动多样性。

### 补充图表


![[assets/figures/papers/paper_list_l1038_https_arxiv_org_abs_2311_12886/figures/003_Figure_3.jpg]]
*Figure 3: Motion mask guidance examples. The first column and second column are the input mask and motion mask respectively. The user can specify one or multiple movable areas in the motion mask to fine grained control the video generation*

![[assets/figures/papers/paper_list_l1038_https_arxiv_org_abs_2311_12886/figures/004_Figure_4.jpg]]
*Figure 4: Motion strength guidance examples. Augmenting the motion strength accelerates the alteration of Mona Lisa’s expression, but excessive motion strength may lead to the loss of finegrained facial details*



## 实验与关键发现

### 主实验结果

在 MSR-VTT 零样本测试集上，AnimateAnything 在文本+图像条件下取得了 **FVD 443** 的指标，显著优于开源基线 **VideoCrafter1** 的 FVD 465（Table 1）。该结果验证了所提出的运动区域掩码引导与运动强度引导对视频生成质量的有效提升。需要指出的是，该评估仅覆盖 256×256 分辨率，且与商业产品 **Gen-2** 的比较仅停留在定性层面（Figure 5），因此跨分辨率和跨产品的定量结论尚需进一步验证。

![[assets/figures/papers/paper_list_l1038_https_arxiv_org_abs_2311_12886/figures/006_Table_1.jpg]]
*Table 1: Video generation performance on the test set of MSR-VTT. “Conditions” denotes the type of condition for generation*

![[assets/figures/papers/paper_list_l1038_https_arxiv_org_abs_2311_12886/figures/005_Figure_5.jpg]]
*Figure 5: Qualitative Results. Comparing to open sourced methods Video Composer and VideoCrafter1, our method achieves higher image fidelity. Comparing to the commercial product Gen-2, our method achieves higher frame consistency*

### 消融实验

#### 图像条件设计消融

Table 2 比较了三种图像条件注入策略：CLIP 图像嵌入、潜变量通道拼接（Concat Latent Channel）和潜变量时间维度拼接（Concat Latent Temporal）。其中，**时间维度拼接**方案在 FVD（443）和帧一致性（0.916）上均优于其他方案，同时仅占用 5.9 GB 显存。这表明将参考图像潜变量作为视频首帧在时间轴上拼接，能够更高效地利用视频扩散模型的时空注意力机制，维持图像保真度的同时不引入额外的计算开销。

![[assets/figures/papers/paper_list_l1038_https_arxiv_org_abs_2311_12886/figures/007_Table_2.jpg]]
*Table 2: The performance comparison of image condition designs*

#### 运动区域掩码引导消融

Table 3 系统消融了运动掩码引导的三种策略：（1）无掩码引导，（2）掩码引导但不冻结非移动区域，（3）掩码引导 + 冻结非移动区域（即 Eq. 5 中的 $z_0' = (1 - m) \cdot z_0^0 + m \cdot z_0$）。结果显示，**掩码引导 + 冻结策略**使运动掩码精确度达到 0.82，显著优于仅使用掩码引导的方案。其因果机制在于：冻结非移动区域潜变量至第一帧，强制模型仅在掩码指定区域内生成运动变化，从而避免了扩散去噪过程中非目标区域的意外漂移。

![[assets/figures/papers/paper_list_l1038_https_arxiv_org_abs_2311_12886/figures/008_Table_3.jpg]]
*Table 3: Ablation study of the motion mask guidance. Our proposed strategy demonstrates effective capability in following designated motion areas to generate corresponding animation videos*

#### 运动强度引导消融

Table 4 对比了两种运动速度控制方式：传统的 FPS 隐式引导与本文提出的运动强度损失直接监督。运动强度损失（Eq. 7：$l_s = || s(z_0) - s(\hat{z}_0) ||_2^2$）使运动强度误差降至 **2.36**，而 FPS 引导方案误差更高且稳定性较差。这一差异的根源在于 FPS 仅全局调整帧采样率，无法精确控制局部运动幅度；而运动强度损失直接监督潜空间帧间差异 $s(z) = \frac{1}{N-1} \sum_{i=1}^{N} |z^i - z^{i-1}|$，实现了对运动速度的像素级约束。

![[assets/figures/papers/paper_list_l1038_https_arxiv_org_abs_2311_12886/figures/009_Table_4.jpg]]
*Table 4: Ablate the design of the motion strength guidance. Comparing to FPS guidance, our method offers greater flexibility in incorporating motion into animation videos*

### 定性分析与失败模式

Figure 3 展示了运动掩码引导的定性效果：用户可通过指定单个或多个可移动区域实现细粒度动画控制。Figure 4 揭示了运动强度引导的边界效应——适度增加运动强度可加速蒙娜丽莎表情变化，但**过高的运动强度会导致面部细节丢失**，表明该方法在极端参数下存在保真度与运动幅度之间的权衡。

Figure 5 的定性对比显示，相较于 **VideoComposer**（Wang et al., arXiv 2023）和 VideoCrafter1，AnimateAnything 在图像保真度上表现更优；相较于 Gen-2，其帧间一致性更高。然而，由于 Gen-2 为闭源商业产品且仅进行定性比较，该结论的普适性需要更多定量基准测试支撑。

Figure 1 的后三行进一步验证了方法的交互式生成能力：通过文本提示和运动掩码的迭代组合，可依次生成多个对象的复杂动画，表明该框架支持累积式创作流程。

### 局限性与待验证问题

论文明确指出的核心局限是**模型未在高分辨率视频上训练**，限制了高分辨率动画应用场景。此外，以下问题需要进一步实验验证：

- 运动掩码阈值 $T_m$ 在不同视频内容类型（如快速运动 vs. 缓慢运动场景）下的鲁棒性表现。
- 运动强度损失权重 $\lambda$ 对收敛速度和最终运动强度准确性的定量影响曲线。
- 在有限训练资源约束下，如何通过渐进式训练或超分辨率级联策略扩展至高分辨率生成。



## 定位与知识库关联

### 任务定位与核心差异

AnimateAnything 聚焦于**开放域图像动画**任务：给定一张任意内容的参考图像，生成一段包含合理运动的短视频。该任务介于图像到视频生成（image-to-video generation）与可控视频生成（controllable video generation）之间，核心挑战在于：如何在保持参考图像高保真度的同时，实现对运动区域和运动强度的细粒度控制。

与现有工作相比，AnimateAnything 的核心差异体现在两个控制维度上：

**运动区域控制**：现有图像动画方法大多局限于特定对象类别，如人体姿态迁移、流体模拟或场景漫游，缺乏对任意开放域图像中局部运动区域的精确指定能力。VideoComposer（Wang et al., arXiv 2023）引入了运动轨迹控制，但其控制粒度是全局或半全局的，难以处理“仅让画面中某一物体运动而其余部分保持静止”的需求。AnimateAnything 通过将运动区域掩码沿通道维度拼接到视频潜变量中，并冻结非移动区域的潜变量至第一帧值，实现了对任意形状、任意数量运动区域的精确控制。

**运动强度控制**：此前的视频生成方法通常通过调整帧率（FPS）隐式地影响运动速度，这是一种全局且间接的控制手段。AnimateAnything 引入了一个显式的运动强度度量 $s(z) = \frac{1}{N-1} \sum_{i=1}^{N} |z^i - z^{i-1}|$，并通过运动强度损失 $l_s = || s(z_0) - s(\hat{z}_0) ||_2^2$ 直接监督帧间差异，从而实现了对运动速度的连续、精确控制。

### 技术谱系与继承关系

AnimateAnything 建立在视频扩散模型的成熟技术栈之上，其技术继承关系可追溯至以下几个关键节点：

1. **视频扩散骨干**：采用基于 3D U-Net 的视频扩散模型架构，该架构由 Video Diffusion Models 等先驱工作确立，并在后续的视频生成方法中得到广泛采用。AnimateAnything 采用微调策略，仅训练时间层参数，冻结空间层，以保留预训练模型的图像生成先验。

2. **图像条件注入**：在如何将参考图像作为条件引入扩散模型这一设计上，AnimateAnything 比较了两种方案——CLIP 图像嵌入注入与潜变量时间维度拼接。消融实验（Table 2）表明，**Concat Latent Temporal** 方案（将参考图像潜变量与噪声帧在时间维度拼接）在 FVD（443 vs. 更高值）和内存占用（5.9 GB）上均优于 CLIP 嵌入方案。这一发现为后续图像到视频生成工作的条件设计提供了参考。

3. **零初始化卷积**：运动掩码的通道维度拼接采用了受 ControlNet 启发的零初始化卷积权重策略，确保在训练初期不破坏预训练模型的生成能力，逐步学习运动区域的控制信号。

4. **合成训练数据生成**：为克服真实视频中运动区域掩码标注的缺失，AnimateAnything 提出了一种无监督的合成掩码生成方法：基于帧间灰度差阈值 $T_m$ 自动提取运动差异掩码 $d = \bigcup_{i=1}^{N-1} (|x_{gray}^i - x_{gray}^{i-1}| > T_m)$，从而从真实视频中自动构造带运动掩码的训练数据。这种“从真实视频中自监督提取控制信号”的思路，为缺乏标注数据的可控生成任务提供了可复用的范式。

### 方法适用边界

根据论文中的实验设置和局限性声明，AnimateAnything 的适用边界可归纳如下：

- **分辨率限制**：模型因训练资源限制未在高分辨率视频上训练，所有定量指标反映的是 256×256 分辨率下的性能。对于高分辨率动画应用，当前版本存在明显不足。
- **运动强度上限**：定性结果（Figure 4）显示，过高的运动强度会导致细粒度细节丢失（如蒙娜丽莎面部细节的退化），表明运动强度控制存在一个保真度-运动幅度的权衡区间。
- **评估范围**：零样本评估仅在 MSR-VTT 数据集上进行（2,990 个视频片段），与 Gen-2 等商业产品的比较仅为定性。对更广泛领域（如高动态场景、细粒度人体动作）的泛化性尚未得到充分验证。
- **训练数据依赖**：模型在 HD-VILA-100M 的 20K 子集上进行微调以去除水印，其性能可能受限于该数据集的分布特征。

### 局限与开放问题

论文明确指出的局限以及分析中浮现的开放问题包括：

**已声明局限**：
- 高分辨率训练的缺失直接限制了模型在实际高画质动画场景中的应用。

**开放问题**：

1. **运动阈值 $T_m$ 的鲁棒性**：合成掩码生成依赖帧间灰度差阈值 $T_m$（论文中设为 5），但该阈值如何与不同视频内容类型（如低对比度场景、缓慢运动、相机运动）交互，以保持自动掩码生成的稳健性，论文未给出系统分析。

2. **损失权重 $\lambda$ 的定量影响**：总损失 $l = l_\epsilon + \lambda \cdot l_s$ 中 $\lambda$ 设为 0.001，但该超参数对噪声预测损失与运动强度损失之间的平衡、收敛行为以及最终运动强度准确性的定量影响，缺乏参数敏感性分析。

3. **高分辨率扩展路径**：在有限训练资源约束下，如何将模型扩展到高分辨率视频生成？可能的路径包括级联生成、空间超分模块的独立训练、或利用更高效的注意力机制降低计算开销，但这些方向尚未在论文中探讨。

4. **多对象交互运动的语义一致性**：Figure 1 展示了通过迭代文本和掩码生成多个对象动画的能力，但多对象之间的运动语义一致性（如两个物体的运动是否物理上协调）缺乏定量评估指标和系统分析。

5. **与商业系统的差距量化**：与 Gen-2 的比较仅为定性，缺乏在统一基准上的定量对比，使得 AnimateAnything 与最前沿商业系统之间的真实差距难以精确评估。



## 原文 PDF

![[paperPDFs/arxiv_2023/AnimateAnything_Fine_Grained_Open_Domain_Image_Animation_with_Motion_Guidance.pdf]]
