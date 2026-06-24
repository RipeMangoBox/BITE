---
title: Improving Motion in Image-to-Video Models via Adaptive Low-Pass Guidance
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/Improving_Motion_in_Image_to_Video_Models_via_Adaptive_Low_Pass_Guidance.pdf
project_link: https://choi403.github.io/ALG
aliases:
- ALPGA
- IMIVMALPG
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/image_and_video_generation
- topic/generative_models_diffusion/diffusion_image_video
- topic/generative_models_diffusion
core_operator: 输入参考图像的高频成分（精细纹理与细节）。
primary_logic: 在扩散采样的早期步骤中，通过自适应低通滤波去除输入图像的高频信息，可以避免生成过程陷入捷径，允许粗粒度运动结构形成；在后期步骤中恢复原始高频信息以重建精细细节，从而在不牺牲图像质量的情况下显著增强视频的运动动态性。
claims:
- I2V 模型相比 T2V 模型动态程度下降 18.6%，而其他质量指标相似。
- 对输入图像应用低通滤波可增加生成视频的动态程度，但会降低图像保真度。
- 可视化显示 I2V 生成过程存在捷径：特征图在第一步后即锁定于细节，而低通滤波可缓解此捷径。
- ALG 在保持视频质量的前提下，将多个模型的动态程度平均提升 33%。
---

# Improving Motion in Image-to-Video Models via Adaptive Low-Pass Guidance

> [!tip] 核心洞察
> 在扩散采样的早期步骤中，通过自适应低通滤波去除输入图像的高频信息，可以避免生成过程陷入捷径，允许粗粒度运动结构形成；在后期步骤中恢复原始高频信息以重建精细细节，从而在不牺牲图像质量的情况下显著增强视频的运动动态性。

| 字段 | 内容 |
|------|------|
| 中文题名 | 通过自适应低通引导改进图像到视频模型的运动 |
| 英文题名 | Improving Motion in Image-to-Video Models via Adaptive Low-Pass Guidance |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://openaccess.thecvf.com/content/CVPR2026/html/Choi_Improving_Motion_in_Image-to-Video_Models_via_Adaptive_Low-Pass_Guidance_CVPR_2026_paper.html) · [Project](https://choi403.github.io/ALG) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/image_and_video_generation #topic/generative_models_diffusion/diffusion_image_video #topic/generative_models_diffusion |
| Method | Adaptive Low-Pass Guidance (ALG) |
| Dataset | VBench I2V test suite, PVD, VidProM |

> [!tip] 效果简介
> - VBench I2V test suite 上，Dynamic Degree 39.0 vs 31.7 (+7.3 (+23%))；Dynamic Degree 39.4 vs 28.9 (+10.5 (+36%))；Dynamic Degree 21.5 vs 15.5 (+6.0 (+39%))。
> - PVD 上，Dynamic Degree 69.0 vs 65.0 (+4.0 (+6.2%))。
> - VidProM 上，Dynamic Degree 30.5 vs 27.3 (+3.2 (+11.7%))。

## 概述

图像到视频（I2V）生成模型在保持输入图像高保真度的同时，普遍存在**运动动态性被抑制**的问题：与文本到视频（T2V）模型相比，I2V 模型的动态程度（Dynamic Degree）平均下降 18.6%，而其他质量指标基本持平（Table 1）。这一瓶颈的根源在于，去噪过程的早期阶段，模型过度暴露于参考图像的高频细节（精细纹理与边缘），导致生成轨迹过早锁定到静态外观的“捷径”，从而抑制了大尺度运动结构的形成（Figure 2）。

针对上述问题，本文提出 **自适应低通引导（Adaptive Low-Pass Guidance, ALG）**，一种无需额外训练的推理时干预方法。其核心思想是：在扩散采样的早期步骤中，对条件图像施加低通滤波以去除高频成分，使模型先构建粗粒度运动结构；在后期步骤中恢复原始图像的高频信息，以重建精细细节。通过一个分段常数的滤波强度调度 $\kappa(t)$ 控制这一频率暴露策略，ALG 在保持视频质量的前提下，将多种 I2V 模型的动态程度平均提升 33%（VBench I2V 测试套件，Table 2），并在 PVD 和 VidProM 等多个基准上验证了泛化性（Table 3）。

在方法谱系上，ALG 属于**推理时条件调制**技术，与标准的分类器自由引导（CFG）相比，仅改变了条件图像在采样过程中的频率内容，不引入额外模型参数或训练开销。其设计区别于直接对输入图像进行全局低通滤波的朴素方案——后者虽能增强运动，但会显著牺牲逐帧图像保真度（Figure 3）。ALG 通过将滤波限定在早期步骤、并在无条件项中保留原始图像，实现了运动增强与画质保持之间的有效权衡。

## 背景与动机

### 图像到视频生成的“运动抑制”瓶颈

图像到视频（Image-to-Video, I2V）生成旨在从单张静态图像出发合成一段连贯的动态视频。近年来，基于流匹配（Flow Matching）和扩散模型的 I2V 方法在帧级图像质量上取得了显著进展，但在生成大尺度、富有表现力的运动方面仍存在明显不足。

一个关键但未被充分诊断的现象是：**I2V 模型相比其对应的文本到视频（Text-to-Video, T2V）模型，动态程度出现系统性下降**。论文在 VBench 基准上的定量分析（Table 1）揭示了这一瓶颈——以 Wan 2.1 模型为例，使用相同提示词，T2V 模型生成的视频动态程度（Dynamic Degree）为 39.4，而将 T2V 生成的第一帧作为 I2V 输入后，动态程度降至 32.1，下降幅度达 18.6%。与此同时，其他质量相关指标（如美学质量、视频质量评分等）保持相似水平。这说明**运动抑制并非源于基础模型能力的整体退化，而是 I2V 条件化机制本身引入的特定偏差**。

### 高频捷径假说：细节过早锁定运动轨迹

论文通过可视化中间特征图（Figure 2）对这一现象进行了诊断。在标准 I2V 生成过程中，模型在去噪的极早期步骤（第一步之后）就将参考图像中的精细细节（如纹理、边缘）注入到特征表示中。这些高频信息迅速“锁定”了生成轨迹，使得粗粒度的运动结构（如物体位移、姿态变化）难以在后续步骤中形成，最终导致生成的视频趋于静态。

这一发现构成了论文的核心洞察：**输入参考图像的高频成分充当了“捷径”（shortcut），使生成过程过早收敛到静态外观，从而抑制了大尺度运动的涌现**。换言之，I2V 模型对参考图像高频细节的过度依赖，是以牺牲运动动态性为代价的。

### 低通滤波的潜力与代价

一个直观的解决方案是对输入图像进行低通滤波，去除高频细节后再送入 I2V 模型。论文在 Figure 3 中系统验证了这一思路：随着低通滤波强度（如下采样因子）的增加，生成视频的动态程度单调上升，但美学质量同步下降。视觉检查（Figure 3b）进一步表明，强滤波虽然使视频更加动态，却因模型接收到的输入图像变得模糊而导致帧级保真度受损。

这一实验揭示了运动动态性与图像保真度之间的根本性权衡：**低通滤波可以释放运动潜力，但以牺牲视觉质量为代价**。这一权衡构成了现有方法的缺口——无论是标准 I2V（运动不足）还是直接低通滤波（质量下降），都无法同时满足高质量和强动态性的需求。

### 本文动机：时间自适应的频率调控

上述分析指向一个核心问题：**能否仅在运动结构形成的关键阶段抑制高频信息，而在细节重建阶段恢复原始图像质量？** 论文的动机正是基于这一时间解耦的思想——在扩散采样的早期步骤中，通过低通滤波阻止模型陷入高频捷径，允许粗粒度运动结构充分形成；在后期步骤中，切换回原始参考图像以恢复精细细节。这种**自适应低通引导（Adaptive Low-Pass Guidance, ALG）**策略旨在在不牺牲图像质量的前提下，显著增强 I2V 模型的运动动态性。

## 核心创新

### 瓶颈发现：I2V 模型的“高频捷径”抑制运动

图像到视频（I2V）生成模型普遍面临一个隐蔽但关键的问题：**运动动态性被显著抑制**。定量诊断（Table 1）表明，同一架构从文本到视频（T2V）切换到 I2V 模式后，Dynamic Degree 下降 **18.6%**，而其他质量指标（如美学质量、时序一致性）几乎不变。这意味着问题并非模型能力不足，而是 I2V 条件机制本身引入了某种“锁定”效应。

通过可视化中间特征图（Figure 2），作者揭示了这一现象的因果机制：默认 I2V 生成在去噪的极早期步骤（甚至第一步后）就将特征图锁定在参考图像的**高频细节**（如纹理、边缘）上，形成一条“捷径”轨迹。该捷径使得粗粒度的运动结构（如物体位移、姿态变化）来不及形成，生成过程便被拖向静态外观的重建。这一发现将 I2V 运动退化的根源从模型架构或训练范式，**精确归因到条件信号的高频成分在采样早期的过度暴露**。

### 核心洞察：低频先行，高频后补

基于上述诊断，作者提出了一个简洁而深刻的假设：如果在扩散采样的早期阶段**去除输入图像的高频信息**，迫使模型先建立粗粒度的时空结构，然后在后期恢复高频细节，就能打破捷径，释放运动潜力。

验证实验（Figure 3）直接支持了这一假设：对输入图像施加低通滤波（如下采样-上采样）后，生成视频的 Dynamic Degree 随滤波强度单调递增，但同时美学质量下降——模型因接收到模糊的参考图像而牺牲了逐帧保真度。这揭示了一个**运动-保真度权衡**：全程低通滤波虽能提升运动，却无法维持画质。

### Changed Slot：条件图像频率成分的时间自适应调制

ALG 的核心创新在于将一个静态的条件输入（原始参考图像）替换为**时间自适应的频率调制信号**。具体而言，该方法在标准 CFG-I2V 采样框架中修改了条件图像的频率内容：

- **Baseline（标准 I2V-CFG）**：无条件项和文本条件项均使用原始未滤波图像 $\mathbf{x}_{\mathrm{init}}$。
- **ALG**：无条件项保留原始图像 $\mathbf{x}_{\mathrm{init}}$（维持基本视觉锚定），而文本条件项使用低通滤波后的图像 $\mathbf{x}_{\mathrm{init}}^{(t)} = \mathcal{F}_{\mathrm{LP}}(\mathbf{x}_{\mathrm{init}}, \kappa(t))$。

这一设计的精妙之处在于**非对称的频率暴露**：无条件项始终“看到”完整的高频信息，防止生成内容完全偏离参考图像；条件项在早期“看不到”高频细节，从而获得构建大尺度运动的灵活轨迹空间。速度场公式清晰体现了这一改动：

$$\mathbf{v}_{\mathrm{ALG}}(\mathbf{x}_t, t) = \mathbf{v}_{\theta}(\mathbf{x}_t, \mathbf{x}_{\mathrm{init}}, t, \mathcal{O}) + w \big( \mathbf{v}_{\theta}(\mathbf{x}_t, \mathbf{x}_{\mathrm{init}}^{(t)}, t, \mathbf{c}) - \mathbf{v}_{\theta}(\mathbf{x}_t, \mathbf{x}_{\mathrm{init}}^{(t)}, t, \mathcal{O}) \big)$$

### 滤波调度 $\kappa(t)$：简单阶跃函数的有效性

ALG 的第二个关键设计是低通滤波强度的**时间调度** $\kappa(t)$。作者采用最简单的阶跃函数：

$$\kappa(t) = \begin{cases} \kappa_* & \text{if } t < t_{\mathrm{trans}} \\ 0 & \text{if } t \geq t_{\mathrm{trans}} \end{cases}$$

在过渡时间 $t_{\mathrm{trans}}$ 之前，以恒定强度 $\kappa_*$ 进行低通滤波（默认使用双线性下采样因子 2.5）；之后完全关闭滤波，恢复原始高频信息以重建精细细节。消融实验（Figure 5）表明，这一极简调度已足够有效：增大 $t_{\mathrm{trans}}$ 可快速提升 Dynamic Degree，而质量指标保持稳定或仅略微下降；增大 $\kappa_*$ 同样增强动态性且不显著牺牲视频质量。作者指出，任何在早期施加更强滤波、后期减弱的 $\kappa(t)$ 均可适用，阶跃函数只是最简实现。

### 方法定位：无需训练的推理时修正

ALG 的方法学定位值得强调：它**不修改模型权重、不增加推理计算量、不改变训练流程**，仅在采样循环中对条件输入进行轻量级频率调制。这使得 ALG 可即插即用于任何已部署的 I2V 模型（论文验证了 Wan 2.1/2.2 和 LTX-Video 三个不同架构），避免了微调带来的分布偏移和公平性争议。从方法论谱系看，ALG 属于**推理时引导技术的扩展**——将 CFG 中固定条件拓展为时间自适应条件，开辟了通过控制条件信号频率来调控生成行为的新维度。

## 整体框架

**Adaptive Low-Pass Guidance (ALG)** 是一种无需训练、即插即用的推理时引导策略，旨在解决图像到视频（I2V）生成中运动动态性被抑制的问题。其核心思想源于一个关键诊断：I2V 模型在去噪早期阶段过度暴露于参考图像的高频细节（精细纹理与边缘），导致生成过程过早锁定到静态外观的“捷径”，从而抑制了大尺度运动结构的形成（Figure 2）。ALG 通过在采样过程中自适应地调制条件图像输入的频率成分，在早期步骤中抑制高频信息以促进粗粒度运动结构演化，在后期步骤中恢复原始高频信息以重建精细细节，从而在不牺牲每帧图像质量的前提下显著提升视频动态性。

### Pipeline 总览

ALG 的整体流程嵌入在标准的流匹配（Flow Matching）采样框架中，对基础 I2V 模型的架构不做任何修改。其输入输出流如下：

- **输入**：一张参考图像 $\mathbf{x}_{\text{init}}$（作为视频的第一帧）和一个文本提示 $\mathbf{c}$。
- **输出**：一段包含 $\mathbf{x}_{\text{init}}$ 作为首帧的视频序列。

在采样过程中，每个去噪时间步 $t$ 的速度预测由三个关键模块协同完成：

1. **低通滤波模块（Low-Pass Filter, $\mathcal{F}_{\text{LP}}$）**：在时间步 $t$，根据当前的滤波强度 $\kappa(t)$ 对参考图像潜在表示 $\mathbf{x}_{\text{init}}$ 进行低通滤波，生成滤波后的潜在表示 $\mathbf{x}_{\text{init}}^{(t)}$。默认实现采用双线性下采样后接双线性上采样，以简单有效地去除高频成分。

2. **自适应调度模块（Adaptive Scheduling, $\kappa(t)$）**：控制滤波强度随时间步的变化。ALG 采用分段常数调度：在过渡时间 $t_{\text{trans}}$ 之前，滤波强度保持为常数 $\kappa_*$（默认下采样因子 2.5）；在 $t_{\text{trans}}$ 之后，滤波强度降为零，即恢复原始参考图像。这一设计确保早期步骤获得强低通滤波以促进运动，后期步骤使用原始图像以恢复细节。

3. **引导速度预测模块**：在每个时间步，ALG 的速度场由两项组成，如公式所示：

   $$\mathbf{v}_{\text{ALG}}(\mathbf{x}_t, t) = \mathbf{v}_{\theta}(\mathbf{x}_t, \mathbf{x}_{\text{init}}, t, \mathcal{O}) + w \big( \mathbf{v}_{\theta}(\mathbf{x}_t, \mathbf{x}_{\text{init}}^{(t)}, t, \mathbf{c}) - \mathbf{v}_{\theta}(\mathbf{x}_t, \mathbf{x}_{\text{init}}^{(t)}, t, \mathcal{O}) \big)$$

   其中无条件项 $\mathbf{v}_{\theta}(\mathbf{x}_t, \mathbf{x}_{\text{init}}, t, \mathcal{O})$ 始终使用**原始参考图像**，以保持与第一帧的结构一致性；条件项（文本条件与无条件）则使用**滤波后的参考图像** $\mathbf{x}_{\text{init}}^{(t)}$，使得引导方向偏向于促进动态运动的生成。这种非对称设计是 ALG 的关键：它避免了在全部三项中使用滤波图像时可能出现的采样不稳定问题，同时在早期步骤中有效抑制了高频细节对运动轨迹的锁定。

### 模块关系与数据流

各模块之间的数据依赖关系如下：自适应调度模块 $\kappa(t)$ 根据当前时间步 $t$ 输出滤波强度，低通滤波模块据此对参考图像进行处理，生成 $\mathbf{x}_{\text{init}}^{(t)}$；速度预测模块则分别以原始图像和滤波图像为条件，计算无条件速度和条件速度，最终合成 ALG 速度场驱动采样过程。在 $t \geq t_{\text{trans}}$ 时，$\kappa(t) = 0$，$\mathbf{x}_{\text{init}}^{(t)} = \mathbf{x}_{\text{init}}$，ALG 退化为标准 CFG-I2V，确保后期步骤的细节重建质量不受影响。

### 补充图表

![[assets/figures/papers/paper_list_l8_https_openaccess_thecvf_com_content_CVPR2026_html_Choi_Improving_Motion/figures/001_Figure_1.jpg]]
*Figure 1: Overcoming suppressed motion dynamics of I2V models with ALG. I2V models achieve high image fidelity to the conditioning image, but they often fail to generate dynamic videos (first row). We refer to this issue as suppressed motion dynamics, which is due to the high-frequency details present in the reference image. As a simple fix, applying low-pass filter to the input image improves the motion dynamics, yet degrades the per-frame image quality and fidelity (second row). Our method, ALG, applies low-pass filter to the conditioning image only at earlier steps, significantly enhancing the dynamic degree while preserving the image quality (third row)*

## 核心模块与公式推导

### 问题形式化与基线

图像到视频（I2V）生成基于条件流匹配（Conditional Flow Matching）框架。给定噪声样本 $\mathbf{x}_0 \sim \mathcal{N}(0, \mathbf{I})$ 和目标视频帧 $\mathbf{x}_1$，模型学习预测速度场 $\mathbf{v}_{\theta}$，损失函数为：

$$\mathcal{L}_{\mathrm{FM}}(\theta) = \mathbb{E}_{\mathbf{x}_t, \mathbf{c}} \big[ \| \mathbf{v}_{\theta}(\mathbf{x}_t, t, \mathbf{c}) - (\mathbf{x}_1 - \mathbf{x}_0) \|_2^2 \big]$$

其中 $\mathbf{c}$ 为条件信息（包括文本提示和参考图像 $\mathbf{x}_{\mathrm{init}}$），$t$ 为时间步。

推理时，标准 I2V 模型采用无分类器引导（CFG），其速度场定义为：

$$\mathbf{v}_{\mathrm{CFG-I2V}}(\mathbf{x}_t, t) = \mathbf{v}_{\theta}(\mathbf{x}_t, \mathbf{x}_{\mathrm{init}}, t, \mathcal{O}) + w \big( \mathbf{v}_{\theta}(\mathbf{x}_t, \mathbf{x}_{\mathrm{init}}, t, \mathbf{c}) - \mathbf{v}_{\theta}(\mathbf{x}_t, \mathbf{x}_{\mathrm{init}}, t, \mathcal{O}) \big)$$

其中 $w$ 为引导尺度，$\mathcal{O}$ 表示空文本条件。该公式中，无条件项与文本条件项均使用原始参考图像 $\mathbf{x}_{\mathrm{init}}$ 作为输入。

### 核心瓶颈：高频捷径锁定

论文通过实验诊断发现（Table 1）：I2V 模型相比 T2V 模型动态程度下降 18.6%，但其他质量指标保持相近。进一步的特征图可视化（Figure 2）揭示，在去噪的第一步后，I2V 生成过程即锁定于参考图像的精细纹理细节（高频成分），形成“捷径”——生成轨迹过早收敛到静态外观，抑制了粗粒度运动结构的形成。

![[assets/figures/papers/paper_list_l8_https_openaccess_thecvf_com_content_CVPR2026_html_Choi_Improving_Motion/figures/002_Figure_2.jpg]]
*Figure 2: Visualization of shortcut effect in I2V generation. Intermediate feature map visualization from Wan 2.1 [55] reveal that default I2V generation (top) exhibits a “shortcut” completion where fine-grained details in the image appears quickly (yellow dashed box), which confines the trajectory and prevents coarse structure from forming, ending up with a static video. Applying a low-pass filter (bottom) suppresses this shortcut to allow details to emerge gradually, and such flexible trajectory helps generating dynamic motion*

这一现象的本质在于：参考图像的高频信息在早期去噪阶段过度暴露，破坏了扩散模型本应具备的从粗到细（coarse-to-fine）的生成特性。

### 诊断实验：低通滤波的权衡

对输入图像应用低通滤波（LPF）可缓解上述捷径效应。诊断实验（Figure 3）表明：随着低通滤波强度增加，生成视频的动态程度单调上升，但美学质量同步下降。这形成了一个运动-保真度权衡：去除高频信息释放了运动潜力，却牺牲了参考图像的细节还原能力。

![[assets/figures/papers/paper_list_l8_https_openaccess_thecvf_com_content_CVPR2026_html_Choi_Improving_Motion/figures/005_Figure_3.jpg]]
*Figure 3: Low-pass filtering improves motion dynamics. (a) We plot the dynamic degree of an I2V model (Wan 2.1 [55]) by applying low-pass filter (e.g., downsampling) to the input image. We observe that dynamic degree (VBench [24] metric which quantifies dynamicness) increases and aesthetic quality (VBench [24] metric which measures per-frame image quality) decreases as we use stronger low-pass filtering. (b) We visualize the frames when applying low-pass filtering to the input image. While the videos become more dynamic using stronger low-pass filters, it sacrifices video quality as the model receives a blurry image as input (highlighted in red)*

### ALG 核心模块

**模块一：低通滤波器 $\mathcal{F}_{\mathrm{LP}}$**

ALG 采用双线性下采样后接双线性上采样实现低通滤波。对于输入图像潜在表示 $\mathbf{x}_{\mathrm{init}}$，滤波操作定义为：

$$\mathbf{x}_{\mathrm{init}}^{(t)} = \mathcal{F}_{\mathrm{LP}}(\mathbf{x}_{\mathrm{init}}, \kappa(t))$$

其中 $\kappa(t)$ 为时变滤波强度，控制下采样因子。该操作有效去除高频分量，保留低频结构信息。

**模块二：自适应调度 $\kappa(t)$**

$\kappa(t)$ 控制低通滤波强度随去噪时间步的变化。核心设计原则是：早期步骤施加强滤波以抑制捷径，后期步骤恢复原始高频信息以重建细节。论文采用分段常数调度：

$$\kappa(t) = \begin{cases} \kappa_* & \text{if } t < t_{\mathrm{trans}} \\ 0 & \text{if } t \geq t_{\mathrm{trans}} \end{cases}$$

其中 $\kappa_*$ 为初始滤波强度（默认下采样因子 2.5），$t_{\mathrm{trans}}$ 为过渡时间步。在 $t_{\mathrm{trans}}$ 之前，模型使用低通滤波图像；之后切换回原始图像。论文指出，任何满足“早期强、后期弱”的 $\kappa(t)$ 调度均可工作，分段常数仅为最简实现。

### ALG 速度场公式

ALG 的核心创新在于将 CFG 中的条件项与无条件项解耦，仅对条件项施加低通滤波，而无条件项保持使用原始图像：

$$\mathbf{v}_{\mathrm{ALG}}(\mathbf{x}_t, t) = \mathbf{v}_{\theta}(\mathbf{x}_t, \mathbf{x}_{\mathrm{init}}, t, \mathcal{O}) + w \big( \mathbf{v}_{\theta}(\mathbf{x}_t, \mathbf{x}_{\mathrm{init}}^{(t)}, t, \mathbf{c}) - \mathbf{v}_{\theta}(\mathbf{x}_t, \mathbf{x}_{\mathrm{init}}^{(t)}, t, \mathcal{O}) \big)$$

**公式变量含义：**
- $\mathbf{v}_{\theta}(\mathbf{x}_t, \mathbf{x}_{\mathrm{init}}, t, \mathcal{O})$：无条件项，始终使用原始图像，为生成提供稳定的图像先验。
- $\mathbf{v}_{\theta}(\mathbf{x}_t, \mathbf{x}_{\mathrm{init}}^{(t)}, t, \mathbf{c})$：文本条件项，使用低通滤波图像，在早期步骤中避免高频捷径，促进运动结构形成。
- $\mathbf{v}_{\theta}(\mathbf{x}_t, \mathbf{x}_{\mathrm{init}}^{(t)}, t, \mathcal{O})$：空文本条件项，同样使用低通滤波图像，与条件项配对计算引导方向。

**设计原理：** 在早期步骤（$t < t_{\mathrm{trans}}$），条件项和空文本条件项均接收低通滤波图像，引导方向（条件项减去空文本项）促进动态运动生成；无条件项保持原始图像，防止生成完全偏离参考帧。在后期步骤（$t \geq t_{\mathrm{trans}}$），$\kappa(t) = 0$，所有三项恢复为原始图像，ALG 退化为标准 CFG，完成精细细节重建。

这种非对称设计避免了论文在消融中发现的问题：若对三项均使用低通滤波图像，会导致生成不稳定；若仅对无条件项保留原始图像，则可在运动增强与保真度之间取得最佳平衡。

## 实验与分析

### 核心发现：I2V 模型的运动抑制现象

实验首先验证了图像到视频（I2V）模型相较于文本到视频（T2V）模型存在显著的“运动抑制”问题。在 VBench 基准测试中，使用相同的提示词，先生成 T2V 视频，再将其第一帧作为 I2V 模型的输入生成视频。结果显示，I2V 模型的平均动态程度（Dynamic Degree）较 T2V 模型下降了 18.6%，而在其他质量相关指标（如美学质量、帧间一致性等）上两者表现相近（Table 1）。这一现象构成了本文方法的核心动机：I2V 模型在保持高保真度的同时，牺牲了生成视频的运动动态性。

### 诊断实验：低通滤波的权衡效应

为探究运动抑制的成因，作者对输入图像施加了不同强度的低通滤波（通过下采样-上采样实现），并观察其对生成视频的影响。结果揭示了一个清晰的权衡关系：随着低通滤波强度的增加，生成视频的动态程度单调上升，但每帧图像的美学质量（Aesthetic Quality）同步下降（Figure 3a）。可视化结果表明，更强的低通滤波确实使视频更加动态，但代价是模型接收到的是模糊的输入图像，导致生成帧的细节丢失（Figure 3b）。这一诊断实验直接支撑了核心假设：高频细节是导致运动抑制的关键因素，但简单去除高频信息会损害图像保真度。

### 主要结果：ALG 在多个模型与基准上的表现

ALG 的核心优势在于打破了上述权衡——在显著提升动态程度的同时，保持视频质量指标几乎不变。在 VBench I2V 测试套件上，ALG 在三个不同规模的 I2V 模型上均取得了显著的动态程度提升：

- **Wan 2.2**：Dynamic Degree 从 31.7 提升至 39.0（+23%），VBench 平均分从 79.6 升至 80.5。
- **Wan 2.1**：Dynamic Degree 从 28.9 提升至 39.4（+36%），VBench 平均分从 79.1 升至 80.0。
- **LTX-Video**：Dynamic Degree 从 15.5 提升至 21.5（+39%），VBench 平均分从 77.8 升至 78.2。

在所有模型中，ALG 的质量指标（VBench-QS、I2V Subject Consistency、DOVER、VisionReward）与 CFG 基线基本持平，表明 ALG 并未引入额外的质量损失（Table 2）。

![[assets/figures/papers/paper_list_l8_https_openaccess_thecvf_com_content_CVPR2026_html_Choi_Improving_Motion/figures/007_Table_2.jpg]]
*Table 2: Comparison across various I2V models. Using Wan 2.1/2.2 [55], and LTX-Video on VBench [24], videos from ALG show higher dynamicness (blue) compared to baseline (CFG), while quality metrics (all except Dynamic Degree) remain similar*

跨基准泛化实验进一步验证了 ALG 的鲁棒性。在 PVD（PE Video Dataset）和 VidProM 数据集上，使用 Wan 2.2 模型，ALG 分别将 Dynamic Degree 从 65.0 提升至 69.0（+6.2%）和从 27.3 提升至 30.5（+11.7%），同时质量指标保持稳定（Table 3）。这表明 ALG 的效果不依赖于特定数据分布。

![[assets/figures/papers/paper_list_l8_https_openaccess_thecvf_com_content_CVPR2026_html_Choi_Improving_Motion/figures/008_Table_3.jpg]]
*Table 3: Comparison across various benchmarks. Across three datasets (VBench [24], PE Video Dataset (PVD) [4], and Vid-ProM [57]), and using Wan 2.2 [55], ALG improves motion dynamics (blue) over the baseline (CFG) while maintaining quality*

### 消融分析：超参数与设计选择的影响

ALG 仅有两个关键超参数：过渡时间 $t_{\mathrm{trans}}$ 和初始滤波强度 $\kappa_*$。消融实验系统考察了它们对动态程度和质量指标的影响：

- **过渡时间 $t_{\mathrm{trans}}$**：当 $t_{\mathrm{trans}}$ 从 0 开始增加时，动态程度迅速上升，而质量指标保持稳定或仅略微下降。这表明即使在较短的早期阶段施加低通滤波，也能有效打破捷径效应（Figure 5a）。
- **初始滤波强度 $\kappa_*$**：增加 $\kappa_*$（即更强的低通滤波）可以进一步增强动态程度，且不会显著牺牲视频质量。这验证了 ALG 的设计——仅在条件项中施加滤波、在无条件项中保留原始图像——能够有效解耦运动增强与质量保持（Figure 5b）。
- **滤波器类型**：比较双线性下采样与高斯模糊两种低通滤波实现，两者均能提升动态程度，表明 ALG 的核心机制对具体滤波实现不敏感（Figure 5c）。

### 提示词增强实验

为探究 ALG 与运动增强提示词的交互效果，实验使用 Gemini 2.5 对原始提示词进行运动增强改写。结果显示，增强提示词对 CFG 和 ALG 均有帮助，但值得注意的是，ALG 即使不使用增强提示词，其动态程度也已超过 CFG 基线（Table 4）。这表明 ALG 的运动增强效果独立于提示工程，直接作用于生成过程的底层机制。

### 失败模式与局限性

尽管 ALG 在多数场景下表现优异，但仍存在以下局限性：

1. **超参数敏感性**：$t_{\mathrm{trans}}$ 和 $\kappa_*$ 的最优值因模型而异，需要手动调整。极端滤波强度或过长的过渡时间可能导致第一帧保真度轻微下降。
2. **根本建模能力的限制**：ALG 仅在推理时修正频率暴露，无法从根本上改变基础模型对运动模式的建模能力。对于基础模型本身运动生成能力极弱的情况，ALG 的提升幅度有限。
3. **与其他技术的组合**：ALG 是否能与其他运动增强技术（如运动 LoRA、运动先验注入）协同工作而不重新引入保真度损失，仍是一个开放问题。

### 补充图表

![[assets/figures/papers/paper_list_l8_https_openaccess_thecvf_com_content_CVPR2026_html_Choi_Improving_Motion/figures/006_Figure_4.jpg]]
*Figure 4: Qualitative comparison between ALG and CFG. We provide visual comparison between the videos generated by using default image-to-video generation method (CFG) and our method (ALG). The input conditioning frames are denoted with red outline. We observe that the videos using ALG show more dynamic motion (e.g., larger object movement, animal movement, or human action, and more complex background movements). The list of prompts and models used for each video is included in the supplementary material*

![[assets/figures/papers/paper_list_l8_https_openaccess_thecvf_com_content_CVPR2026_html_Choi_Improving_Motion/figures/012_Figure_5.jpg]]
*Figure 5: Component analysis with VBench-I2V. (a) As*

## 方法谱系与知识库定位

### 问题定位：I2V 模型的“运动抑制”瓶颈

图像到视频（I2V）生成模型面临一个关键瓶颈：尽管能保持输入参考图像的高保真度，但生成的视频往往缺乏足够的大尺度运动动态性。本文通过定量实验证实了这一现象——在 VBench 基准上，I2V 模型（Wan 2.1）相比其对应的 T2V 模型，Dynamic Degree 下降了 **18.6%**（39.4 → 32.1），而其他质量指标（Aesthetic Quality、Imaging Quality 等）保持相近水平（Table 1）。这表明运动抑制并非模型整体生成能力的退化，而是 I2V 条件机制引入的特定问题。

进一步的诊断可视化（Figure 2）揭示了该问题的因果机制：在默认 I2V 生成中，中间特征图在第一个去噪步骤后即迅速锁定于参考图像的精细纹理细节，形成一种“捷径”完成路径。这种过早的高频细节锁定限制了粗粒度运动结构的形成空间，导致生成轨迹被约束在静态外观附近。该发现将 I2V 运动抑制问题从经验观察提升到了生成动力学层面的因果解释。

### 核心洞察：频率暴露的时序控制

本文的核心洞察在于识别出可操作的因果调控旋钮——**输入参考图像的高频成分**。实验表明，对输入图像应用低通滤波可单调提升生成视频的动态程度，但同时会牺牲逐帧图像质量（Figure 3）。这一权衡关系暗示：高频信息在生成过程中的作用具有时序依赖性——早期阶段需要抑制高频以避免捷径，后期阶段则需要恢复高频以重建细节。

基于此洞察，ALG 将问题转化为一个**频率暴露的时序调度问题**，而非简单的滤波强度选择问题。这种视角转换使方法从“全局滤波”的保真度-运动权衡中跳脱出来，进入“分阶段频率控制”的新设计空间。

### 方法谱系：CFG 框架下的条件频率调制

从方法谱系来看，ALG 继承并扩展了分类器自由引导（Classifier-Free Guidance, CFG）框架。标准 I2V 的 CFG 速度场定义为：

$$\mathbf{v}_{\mathrm{CFG-I2V}}(\mathbf{x}_t, t) = \mathbf{v}_{\theta}(\mathbf{x}_t, \mathbf{x}_{\mathrm{init}}, t, \mathcal{O}) + w \big( \mathbf{v}_{\theta}(\mathbf{x}_t, \mathbf{x}_{\mathrm{init}}, t, \mathbf{c}) - \mathbf{v}_{\theta}(\mathbf{x}_t, \mathbf{x}_{\mathrm{init}}, t, \mathcal{O}) \big)$$

其中无条件项和文本条件项均使用原始参考图像 $\mathbf{x}_{\mathrm{init}}$。ALG 的关键修改在于**仅对 CFG 中的条件项施加时变低通滤波**，形成非对称的频率暴露：

$$\mathbf{v}_{\mathrm{ALG}}(\mathbf{x}_t, t) = \mathbf{v}_{\theta}(\mathbf{x}_t, \mathbf{x}_{\mathrm{init}}, t, \mathcal{O}) + w \big( \mathbf{v}_{\theta}(\mathbf{x}_t, \mathbf{x}_{\mathrm{init}}^{(t)}, t, \mathbf{c}) - \mathbf{v}_{\theta}(\mathbf{x}_t, \mathbf{x}_{\mathrm{init}}^{(t)}, t, \mathcal{O}) \big)$$

其中 $\mathbf{x}_{\mathrm{init}}^{(t)} = \mathcal{F}_{\mathrm{LP}}(\mathbf{x}_{\mathrm{init}}, \kappa(t))$ 为经时变强度 $\kappa(t)$ 低通滤波后的参考图像。滤波强度采用分段常数调度：

$$\kappa(t) = \begin{cases} \kappa_* & \text{if } t < t_{\mathrm{trans}} \\ 0 & \text{if } t \geq t_{\mathrm{trans}} \end{cases}$$

这种设计的精妙之处在于：无条件项始终接收完整高频信息，为后期细节重建保留了“锚点”；而条件项在早期（$t < t_{\mathrm{trans}}$）使用低通滤波图像以促进运动结构形成，在后期（$t \geq t_{\mathrm{trans}}$）恢复原始图像以重建精细细节。

### 与相关技术路线的关系

ALG 在方法谱系中占据了一个独特位置——**无需训练的推理时频率调控方法**。这使其区别于以下几条技术路线：

- **训练时运动增强**：如通过运动特定损失函数或运动先验注入来微调基础模型。这类方法需要额外训练成本，且可能改变模型的通用生成能力。ALG 作为推理时方法，可直接应用于任意已训练的 I2V 模型，避免了微调引入的不确定性。
- **提示工程**：通过运动增强提示（如添加“动态的”“快速移动”等描述）来引导模型生成更多运动。Table 4 显示，ALG 即使不使用运动增强提示，其 Dynamic Degree 也超过使用增强提示的 CFG 基线，表明频率控制比语义引导在运动增强上更为根本。
- **全局低通滤波**：直接对输入图像进行低通滤波虽能提升运动，但以牺牲保真度为代价（Figure 3）。ALG 通过时序调度解耦了这一权衡。

### 适用边界与局限

1. **超参数依赖性**：ALG 的性能依赖于两个超参数（$t_{\mathrm{trans}}$ 和 $\kappa_*$）的合理选择。消融实验（Figure 5）表明，增加 $t_{\mathrm{trans}}$ 可快速提升动态程度，增加 $\kappa_*$ 也能增强运动性，但极端取值可能导致第一帧保真度轻微下降。不同 I2V 模型（Wan 2.1、Wan 2.2、LTX-Video）可能需要不同的最优设置，目前依赖手动调整。

2. **模型能力的上限约束**：ALG 仅在推理时修正频率暴露模式，不能从根本上改变基础模型对运动模式的建模能力。若基础模型的运动生成能力本身较弱（如 LTX-Video 的 Dynamic Degree 仅从 15.5 提升至 21.5），ALG 的提升幅度受限于模型自身的生成潜力。

3. **滤波器选择的鲁棒性**：消融实验显示，双线性下采样和高斯模糊两种低通滤波实现均能提升动态程度（Figure 5c），表明方法对具体滤波器选择具有一定鲁棒性。但不同滤波器类型对质量指标的细微影响仍需进一步研究。

### 开放问题

1. **自动调度优化**：如何针对不同 I2V 模型自动选择最优的 $\kappa(t)$ 调度？是否可能通过学习或启发式方法从模型特征中推断最佳过渡时间？

2. **多技术协同**：ALG 能否与运动增强提示、运动先验注入等其他技术结合而不重新引入保真度损失？Table 4 初步表明 ALG 与增强提示可协同工作，但更广泛的兼容性研究仍有待开展。

3. **捷径形成的精确机制**：高频信号在早期扩散步骤中锁定生成轨迹的精确动力学机制是什么？这一理解可能催生更精细的频率调控策略。

4. **训练阶段的频率控制**：是否可以在训练阶段就融入自适应频率控制，使模型从根本上学习更鲁棒的粗到细生成过程，从而避免推理时的权衡？这可能是下一代 I2V 模型训练范式的重要方向。

## 原文 PDF

![[paperPDFs/CVPR_2026/Improving_Motion_in_Image_to_Video_Models_via_Adaptive_Low_Pass_Guidance.pdf]]
