---
title: "MotionStream: Real-Time Video Generation with Interactive Motion Controls"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/MotionStream_Real_Time_Video_Generation_with_Interactive_Motion_Controls.pdf
openreview_forum_id: v1DKz5Vxr7
aliases:
- MotionStream
tags:
- ICLR_2026
- topic/generative_models_diffusion
- topic/generative_models_diffusion/generative_models_and_autoencoders
core_operator: "将双向教师模型蒸馏为因果自回归学生模型，结合滑动窗口因果注意力、注意力槽和KV缓存滚动，并融合联合文本-运动引导到蒸馏目标中。"
primary_logic: "通过分析注意力图发现初始帧标记在生成中持续被关注（类似注意力槽），因此引入注意力槽和滚动KV缓存，在训练中模拟外推分布，使得固定上下文窗口能够稳定生成任意长度视频，同时保持恒定速度和交互性。"
claims:
- "在DAVIS和Sora数据集上，MotionStream的因果蒸馏学生模型在480P分辨率下达到16.7 FPS，720P下10.4 FPS，而基线速度远低于1 FPS，且学生模型保持了较高的重建质量（PSNR 16.2, LPIPS 0.443等）。"
- "在新视角合成任务上，MotionStream的流程显著优于专门的3D方法（如SEVA、ViewCrafter），PSNR提升约2dB，且速度提升20倍以上。"
- "注意力槽消融显示，没有注意力槽时模型在长视频外推中发生漂移，LPIPS恶化（0.501 vs 0.464），EPE显著增加；且滑动窗口注意力导致延迟和吞吐量波动，而固定块大小（c3s1w1）保持稳定。"
- "联合文本-运动引导平衡了轨迹精度和视觉质量，纯运动引导导致僵硬运动，纯文本引导丧失轨迹忠实度，混合引导（w_t=3.0, w_m=1.5）达到最佳平衡。"
---

# MotionStream: Real-Time Video Generation with Interactive Motion Controls

> [!tip] 核心洞察
> 通过分析注意力图发现初始帧标记在生成中持续被关注（类似注意力槽），因此引入注意力槽和滚动KV缓存，在训练中模拟外推分布，使得固定上下文窗口能够稳定生成任意长度视频，同时保持恒定速度和交互性。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | MotionStream：具有交互式运动控制的实时视频生成 |
| 英文题名 | MotionStream: Real-Time Video Generation with Interactive Motion Controls |
| 会议/期刊 | ICLR 2026 (Oral) |
| Links | [paper](https://openreview.net/forum?id=v1DKz5Vxr7) |
| Topic | #topic/generative_models_diffusion #topic/generative_models_diffusion/generative_models_and_autoencoders |
| Method | MotionStream |
| Dataset | DAVIS (运动转移), Sora Demo Subset (运动转移), LLFF (新视角合成) |

> [!tip] 效果简介
> - DAVIS (运动转移) 上，PSNR / SSIM / LPIPS / EPE 为 Ours Causal (480P): 16.20 / 0.447 / 0.443 / 7.80，对比 ATI (480P): 15.33 / 0.374 / 0.473 / 17.41，变化 PSNR +0.87, EPE -9.61。
> - Sora Demo Subset (运动转移) 上，PSNR / SSIM / LPIPS / EPE 为 Ours Causal (480P): 16.67 / 0.531 / 0.360 / 4.21，对比 ATI (480P): 16.04 / 0.502 / 0.366 / 6.12，变化 PSNR +0.63, EPE -1.91。
> - LLFF (新视角合成) 上，PSNR / SSIM / LPIPS 为 Ours Teacher (480P): 16.0 / 0.42 / 0.21，对比 SEVA: 14.1 / 0.30 / 0.29，变化 PSNR +1.9, LPIPS -0.08。

## 概述

### 问题瓶颈

现有运动条件视频生成方法存在两个根本性瓶颈：**不可接受的高延迟**（数分钟级）和**双向非因果处理**。这些方法基于扩散模型，需要并行生成完整视频序列，无法实现实时交互，且只能生成有限长度的视频。例如，基于Wan 2.1-14B的**ATI**（Wang et al., 2025a）等方法虽然能产生视觉质量较好的结果，但其离线生成范式从根本上限制了交互式应用的可能性。

### 核心方法

MotionStream通过一条**因果蒸馏流水线**将双向教师模型转化为因果自回归学生模型，实现流式视频生成。其核心机制包括三个层次：

1. **轨迹表示**：使用正弦位置编码配合可学习轨迹头，替代传统的RGB着色轨迹加VAE编码方案，编码速度提升约40倍（24.8 ms vs 1053 ms），同时质量更优（Table 3）。
2. **因果适应与蒸馏**：通过分布匹配蒸馏（DMD）将教师模型的知识迁移到学生模型，并引入**注意力槽**（attention sink）和**滑动窗口因果注意力**。关键洞察来自对注意力图的分析——初始帧标记在生成过程中持续被关注，因此将其作为持久化的锚点（注意力槽），配合滚动KV缓存，使固定上下文窗口能够稳定生成任意长度视频。
3. **联合文本-运动引导**：将昂贵的多步引导（$w_t=3.0, w_m=1.5$）蒸馏到学生模型中，平衡轨迹精度和视觉质量，消除推理时的引导开销。

### 核心结论

MotionStream在单张H100 GPU上实现了**实时交互速度**：480P分辨率下16.7 FPS，720P下10.4 FPS，使用Tiny VAE解码器后可进一步提升至29.5 FPS和23.9 FPS。在运动转移任务上，因果学生模型在DAVIS和Sora子集上重建质量（PSNR 16.2, LPIPS 0.443）与教师模型相当，同时速度远超所有基线（基线均低于1 FPS）。在新视角合成任务上，MotionStream流程显著优于专门的3D方法（如**SEVA**、**ViewCrafter**），PSNR提升约2dB，速度提升20倍以上。

### 方法定位

MotionStream属于**流式自回归视频生成**范式，区别于传统的离线扩散模型。其技术路线融合了运动控制视频生成、因果注意力机制和分布匹配蒸馏三个方向，在实时交互性和生成质量之间建立了新的权衡边界。该方法不依赖特定骨干网络规模，在Wan 2.1和Wan 2.2上均验证了有效性，且运动条件的引入未显著降低基础模型的生成能力（Table A4）。

## 背景与动机

### 运动条件视频生成：离线范式与实时交互的鸿沟

运动条件视频生成（motion-conditioned video generation）旨在根据用户提供的运动轨迹（如点轨迹或光流）控制视频中对象的运动。这一能力在运动转移、拖拽式编辑、3D 相机控制等交互式应用中具有核心价值。然而，现有方法几乎全部采用**离线扩散范式**：它们以双向注意力机制并行处理完整视频序列，生成固定长度的视频。这种设计带来了两个根本性限制：

1. **不可接受的高延迟**：现有方法（如基于AnimateDiff的**Image Conductor**（Li et al., 2025e）、基于CogVideoX-5B的**Go-With-The-Flow**（Burgert et al., 2025）和**Diffusion-As-Shader**（Gu et al., 2025b）、基于Wan 2.1-14B的**ATI**（Wang et al., 2025a））的生成时间以分钟计，远无法满足实时交互需求。
2. **固定长度输出**：双向处理意味着模型只能生成预设长度的序列，无法支持流式、任意长度的视频生成。

这一鸿沟的**核心瓶颈**在于：离线扩散模型的双向非因果处理与实时流式生成所需的因果自回归范式之间存在结构性的不兼容。将现有模型直接转换为自回归模式面临两大挑战——如何在外推生成中保持稳定质量，以及如何将昂贵的多步扩散过程压缩为高效的少步推理。

### 注意力槽现象：从观察到机制

MotionStream的作者通过分析双向教师模型的自注意力图（Figure 3）发现了一个关键现象：在去噪生成过程中，多个注意力头持续关注**初始帧对应的标记**，即便在生成后期帧时也是如此。这一“注意力槽”（attention sink）现象——类似于大语言模型中的初始标记保持机制——暗示了在流式生成中保留初始帧信息对于维持时间一致性至关重要。

### 本文动机

基于上述观察，MotionStream提出了一条从离线教师到因果学生的蒸馏路径，核心动机在于：

- **将双向知识迁移到因果框架**：通过分布匹配蒸馏，将教师模型的双向生成能力压缩为因果自回归学生模型，同时引入注意力槽机制和滑动窗口因果注意力，使得固定上下文窗口能够稳定外推任意长度视频。
- **消除推理时的引导开销**：将昂贵的联合文本-运动引导蒸馏到学生模型中，使推理时无需额外的前向传播即可同时保持轨迹忠实度和视觉自然性。
- **实现恒定速度的流式生成**：通过滚动KV缓存和固定块大小设计，使延迟和吞吐量在任意长度生成中保持恒定，从而真正支持实时交互。

这一技术路线使得MotionStream在单张H100 GPU上达到480P分辨率下16.7 FPS、720P下10.4 FPS的生成速度（Table 1），而基线方法的速度远低于1 FPS，同时在运动转移和新视角合成任务上保持甚至超越了离线方法的生成质量。

## 核心创新

MotionStream 的核心创新在于将离线、双向的运动条件视频扩散模型转化为一个因果自回归的流式生成系统，从而在保持运动控制精度的同时实现实时交互。这一转化围绕四个关键的技术槽位展开。

**1. 轨迹表示：从 RGB-VAE 到正弦位置编码**

传统方法（如 **Image Conductor**、**Go-With-The-Flow**）通常将 2D 轨迹渲染为 RGB 着色图，再通过 VAE 编码器嵌入到潜在空间。MotionStream 发现这种方案存在两个瓶颈：VAE 编码引入的压缩损失会降低轨迹精度，且编码延迟高（约 1053 ms），无法满足实时流式需求。

该方法提出使用正弦位置编码配合一个轻量级可学习的轨迹头（Track Head）。具体而言，对于每个可见轨迹点，其嵌入被直接放置到空间下采样后的对应位置，构建轨迹条件信号：

$$c_{m}[t, \lfloor \frac{y_{t}^{n}}{s} \rfloor, \lfloor \frac{x_{t}^{n}}{s} \rfloor] = v[t, n] \cdot \phi_{n}$$

处理后的轨迹嵌入直接与视频潜在变量在通道维度拼接，仅需微调 DiT 的 patchify 层，无需引入 ControlNet 式的额外分支。这一设计使得轨迹编码速度提升约 40 倍（24.8 ms vs 1053 ms），同时在 DAVIS 和 Sora 子集上的 PSNR 和 EPE 指标均优于 RGB-VAE 方案（Table 3）。

**2. 注意力模式：注意力槽与滑动窗口因果注意力**

标准的因果自回归模型使用全历史注意力，导致推理延迟随序列长度线性增长。而直接采用滑动窗口因果注意力虽然降低了计算量，但在长视频外推中会发生严重漂移。

MotionStream 的关键洞察来自对教师模型注意力图的可视化分析（Figure 3）：在双向注意力的去噪过程中，多个注意力头持续聚焦于初始帧对应的标记。这一现象类似于大语言模型中的“注意力槽”（attention sink）——初始帧标记充当了稳定的锚点。

基于此，该方法设计了“注意力槽 + 滑动窗口”的混合注意力模式。对于第 $i$ 个生成块，其注意力上下文定义为：

$$\mathcal{C}_i = \{z_t^i\} \cup \{z_0^j\}_{j \leq S} \cup \{z_0^j\}_{\max(1, i-W) \leq j < i}$$

其中 $S$ 为注意力槽大小（保留前 $S$ 个块的干净潜在变量），$W$ 为局部窗口大小。消融实验（Table 4, Figure 6）表明，至少保留 1 个注意力槽块（c3s1w1）是防止外推漂移的必要条件——无注意力槽时 LPIPS 从 0.464 恶化至 0.501，EPE 显著增加。同时，固定块大小（chunk-3）避免了直接滑动窗口（c3s0w6）导致的延迟和吞吐量大幅波动，维持了流式系统的稳定性。

**3. 生成框架：分布匹配蒸馏与自回归滚动**

教师模型基于 Wan I2V 骨干，使用双向注意力和流匹配损失进行全序列并行生成，推理延迟高达数分钟。MotionStream 通过 Self Forcing 风格的分布匹配蒸馏（DMD）将教师压缩为少步因果学生模型。

蒸馏的核心梯度由真实得分与虚假得分的差异驱动：

$$\nabla_{\theta} \mathcal{L}_{\mathrm{DMD}} \approx - \mathbb{E}_{t, \hat{z}_0} \left[ \left( s_{\mathrm{real}}(\Psi(\hat{z}_0, t), t) - s_{\mathrm{fake}}(\Psi(\hat{z}_0, t), t) \right) \cdot \frac{\partial \hat{z}_0}{\partial \theta} \right]$$

其中真实得分 $s_{\mathrm{real}}$ 使用冻结的教师模型融合联合文本-运动引导计算，虚假得分 $s_{\mathrm{fake}}$ 由可训练的判别器提供。训练过程中采用自回归滚动（autoregressive rollout）和滚动 KV 缓存，模拟推理时的外推分布，使得学生模型仅需 3 步采样即可生成高质量视频块。

**4. 引导方式：联合文本-运动引导蒸馏**

传统运动条件生成通常依赖单独的运动引导或无分类器引导（CFG），但联合文本和运动引导需要在推理时多次评估教师模型，计算开销巨大。MotionStream 将联合引导直接融入蒸馏目标：

$$s_{\mathrm{real}} = s_{\mathrm{base}} + w_t \cdot (f_{\phi}(c_t, c_m) - f_{\phi}(\emptyset, c_m)) + w_m \cdot (f_{\phi}(c_t, c_m) - f_{\phi}(c_t, \emptyset))$$

通过将引导权重（$w_t=3.0, w_m=1.5$）蒸馏到学生模型中，推理时无需额外的前向传播即可同时获得文本语义对齐和轨迹精度控制。消融实验（Figure 4, Figure 5）显示，纯运动引导导致运动僵硬，纯文本引导丧失轨迹忠实度，混合引导在两者间取得最佳平衡。

**5. 解码效率：Tiny VAE 解码器**

标准的 Wan VAE 解码器成为流式系统的吞吐量瓶颈。MotionStream 设计了一个紧凑的 Tiny VAE 解码器，在几乎不损失重建质量的前提下，将 Wan 2.1 的吞吐量从 16.7 FPS 提升至 29.5 FPS，Wan 2.2 从 10.4 FPS 提升至 23.9 FPS（Table A2），解码延迟降低超过 10 倍。

**创新总结**

上述技术槽位的协同作用使得 MotionStream 在 480P 分辨率下达到 16.7 FPS（Wan 2.1-1.3B）和 720P 下 10.4 FPS（Wan 2.2-5B）的实时生成速度，同时在运动转移重建任务上保持与离线教师模型可比的质量（DAVIS PSNR 16.20, LPIPS 0.443），并在新视角合成任务上以 20 倍以上的速度优势超越专门的 3D 方法（如 **SEVA**、**ViewCrafter**）。

## 整体框架

![[assets/figures/papers/paper_list_l8_https_openreview_net_forum_id_v1DKz5Vxr7/figures/002_Figure_2.jpg]]
*Figure 2: Model architecture and training pipeline. To build a teacher motion-controlled video model, we extract and randomly sample 2D tracks from the input video and encode them using a lightweight track head. The resulting track embeddings are combined with the input image, noisy video latents, and text embeddings as input to the diffusion transformer with bidirectional attention, which is then trained with a flow matching loss (top). We then distill a few-step causal diffusion model from the teacher through Self Forcing-style DMD distillation, integrating joint text-motion guidance into the objective, where autoregressive rollout with rolling KV cache and attention sink is applied during both tra...*

MotionStream 的整体流水线围绕一个核心矛盾展开：**离线双向扩散模型**能够高质量地生成受运动轨迹控制的视频，但其非因果处理范式导致不可接受的高延迟（数分钟），无法支持实时交互式生成。为此，MotionStream 设计了一个三阶段的“教师-蒸馏-流式推理”框架，将离线模型的能力迁移到因果自回归学生模型中，并在推理时维持恒定的吞吐量和亚秒级延迟。

### 流水线总览

整个系统由五个核心模块串联构成，形成从轨迹输入到流式视频输出的端到端管线：

1.  **轨迹提取与编码（Track Head）**：从输入视频或用户交互中提取 2D 轨迹，通过正弦位置编码和轻量卷积网络生成轨迹嵌入。这一设计替代了传统的 RGB-VAE 轨迹编码，编码速度提升约 40 倍（24.8 ms vs 1053 ms），是实时流式的关键前提（Table 3）。
2.  **运动控制教师模型（Teacher DiT）**：基于 Wan I2V 骨干，接收轨迹嵌入、图像潜在表示和文本嵌入，使用**双向注意力**和流匹配损失进行训练。教师模型负责学习高质量的运动条件生成能力，并通过**联合文本-运动引导**（$w_t=3.0, w_m=1.5$）平衡轨迹忠实度与视觉自然性。
3.  **因果适应与蒸馏（Causal Distillation）**：这是框架的核心转换环节。通过分布匹配蒸馏（DMD）将双向教师模型的知识迁移到因果学生模型中。蒸馏过程引入三个关键机制：
    -   **滑动窗口因果注意力**：将双向注意力替换为仅允许历史帧可见的因果注意力，并限制注意力窗口大小。
    -   **注意力槽（Attention Sink）**：保留初始帧的 KV 缓存作为持久化锚点，防止长视频外推中的模型漂移。
    -   **联合引导蒸馏**：将教师模型推理时昂贵的联合文本-运动引导直接融入蒸馏目标，使学生模型无需额外 CFG 步骤即可继承引导效果。
4.  **Tiny VAE 解码器**：一个紧凑的视频解码器，将潜在空间表示高效解码为像素级视频帧。相比原始 VAE，解码吞吐量提升 1.75–2.3 倍，将 Wan 2.1 模型的端到端帧率从 16.7 FPS 推至 29.5 FPS。
5.  **流式推理引擎**：在推理时，学生模型以**固定块大小**（chunk-3）逐块生成视频帧，利用**滚动 KV 缓存**和注意力槽维持恒定内存与计算开销，实现稳定的实时交互式生成。

### 输入输出流

系统的输入输出流清晰定义了从控制信号到视频帧的转换路径：

-   **输入**：
    -   **初始图像** $I_0$：作为视频生成的起始帧。
    -   **文本提示** $c_t$：描述期望的视频内容和运动语义。
    -   **2D 轨迹**：一组随时间变化的稀疏轨迹点，由用户交互或视频跟踪算法（如 CoTracker3）提供。轨迹通过正弦位置编码转换为空间-时间嵌入 $c_m$。
-   **内部表示**：
    -   轨迹嵌入与噪声视频潜在表示在通道维度拼接后送入 DiT 骨干。
    -   教师模型使用双向注意力处理完整序列；学生模型使用因果滑动窗口注意力，仅关注当前块、注意力槽块和局部历史块。
-   **输出**：
    -   **流式视频帧**：学生模型以恒定速度逐块生成视频帧，经 Tiny VAE 解码后输出。在 480P 分辨率下达到 16.7 FPS（Wan 2.1-1.3B），720P 下达到 10.4 FPS（Wan 2.2-5B），优化 Tiny VAE 后分别提升至 29.5 FPS 和 23.9 FPS。

### 关键设计决策的因果链

框架中每个设计选择都直接回应了实时交互式生成的具体瓶颈：

-   **瓶颈：双向处理导致高延迟** → **方案：因果蒸馏**，将双向教师模型压缩为因果学生模型，消除对未来的依赖。
-   **瓶颈：自回归生成中的长视频漂移** → **方案：注意力槽 + 滚动 KV 缓存**，通过分析注意力图发现初始帧标记在生成中持续被关注，因此显式保留初始帧作为锚点，并在训练中模拟外推分布。
-   **瓶颈：联合引导增加推理开销** → **方案：引导蒸馏**，将 $w_t=3.0, w_m=1.5$ 的联合引导效果直接融入 DMD 目标，避免推理时多次模型前向。
-   **瓶颈：VAE 解码成为吞吐量瓶颈** → **方案：Tiny VAE**，通过紧凑解码器设计将解码时间压缩至原来的十分之一以下。

这一框架使得 MotionStream 能够从单张图像出发，在用户实时绘制的运动轨迹控制下，以交互式速度流式生成任意长度的视频，并支持运动转移、拖拽控制和 3D 相机控制等多种下游应用。

## 核心模块与公式推导

### 轨迹提取与编码（Track Head）

MotionStream 从输入视频中提取稀疏 2D 轨迹作为运动控制信号。轨迹由 CoTracker3 在 50×50 均匀网格上追踪得到，每条轨迹包含时间步 $t$ 上的空间坐标 $(x_t^n, y_t^n)$ 和可见性标记 $v[t,n]$。与将轨迹渲染为 RGB 视频再通过 VAE 编码的常规方案不同，MotionStream 采用**正弦位置编码 + 可学习的轻量轨迹头**：

- 每条轨迹被分配一个可学习的身份嵌入 $\phi_n$，通过正弦位置编码注入空间坐标信息。
- 轨迹信号按以下方式构造（Sec. 3.1）：

$$c_{m}[t, \lfloor \frac{y_{t}^{n}}{s} \rfloor, \lfloor \frac{x_{t}^{n}}{s} \rfloor] = v[t, n] \cdot \phi_{n}$$

其中 $s$ 为空间下采样因子，可见轨迹的嵌入被放置到对应的下采样空间位置，不可见轨迹位置填充零。该轨迹嵌入通过轻量卷积网络处理后，直接与视频潜在表示在通道维度拼接，仅需微调 patchify 层的通道适配，核心 DiT 架构保持不变。

**关键优势**：PE-Head 编码仅需 24.8 ms，而 RGB-VAE 方案需要 1053 ms（Table 3），提速约 40 倍，且轨迹忠实度（EPE）和重建质量（PSNR）均更优。

### 运动控制教师模型（Teacher DiT）

教师模型基于 Wan I2V 骨干，接收四类输入：噪声视频潜在表示、轨迹嵌入、条件图像、文本嵌入。教师模型使用**双向注意力**机制，对所有帧进行全互注意，并通过流匹配损失训练。为处理遮挡与未指定轨迹的歧义，引入**随机中间帧掩码**策略（$p_{\text{mask}}=0.2$）：先无掩码训练，再用掩码微调，使模型学会在轨迹缺失时依赖文本和图像先验进行合理补全。

推理时采用**联合文本-运动无分类器引导**（Sec. 3.1）：

$$\hat{v} = v_{\mathrm{base}} + w_t \cdot (v(c_t, c_m) - v(\emptyset, c_m)) + w_m \cdot (v(c_t, c_m) - v(c_t, \emptyset))$$

其中 $v_{\mathrm{base}}$ 为基础速度预测，$w_t$ 为文本引导权重，$w_m$ 为运动引导权重。消融实验确定最优平衡点 $w_t=3.0, w_m=1.5$：纯运动引导导致僵硬运动，纯文本引导丧失轨迹忠实度，混合引导在轨迹精度与视觉自然性之间取得最佳折衷（Figure 4, Figure 5）。

### 因果蒸馏与自回归滚动

核心瓶颈在于：双向教师模型需要完整序列才能推理，无法流式生成。MotionStream 通过**分布匹配蒸馏**将双向教师压缩为因果自回归学生模型。

**注意力槽与滑动窗口**：分析教师模型的自注意力图发现，多个注意力头在去噪全过程中持续关注初始帧标记（Figure 3），形成天然的“注意力槽”。基于此发现，学生模型采用滑动窗口因果注意力，第 $i$ 个 chunk 的注意力上下文为：

$$\mathcal{C}_i = \{z_t^i\} \cup \{z_0^j\}_{j \leq S} \cup \{z_0^j\}_{\max(1, i-W) \leq j < i}$$

其中 $z_t^i$ 为当前 chunk 的噪声标记，$S$ 为注意力槽 chunk 数（初始帧），$W$ 为局部窗口大小。最优配置为 c3s1w1（chunk 大小 3，sink 大小 1，窗口大小 1），在视觉质量、延迟稳定性和吞吐量之间取得最佳平衡（Table 4）。

**DMD 蒸馏梯度**（Sec. 3.2）：

$$\nabla_{\theta} \mathcal{L}_{\mathrm{DMD}} \approx - \mathbb{E}_{t, \hat{z}_0} \left[ \left( s_{\mathrm{real}}(\Psi(\hat{z}_0, t), t) - s_{\mathrm{fake}}(\Psi(\hat{z}_0, t), t) \right) \cdot \frac{\partial \hat{z}_0}{\partial \theta} \right]$$

其中 $\Psi$ 为前向扩散过程，$\hat{z}_0$ 为学生生成器输出。驱动梯度来自真实得分与虚假得分之差。

**真实得分**使用冻结教师模型融合联合引导，将多步 CFG 开销蒸馏到学生中：

$$s_{\mathrm{real}} = s_{\mathrm{base}} + w_t \cdot (f_{\phi}(c_t, c_m) - f_{\phi}(\emptyset, c_m)) + w_m \cdot (f_{\phi}(c_t, c_m) - f_{\phi}(c_t, \emptyset))$$

虚假得分由可训练判别器 $f_{\psi}$ 参数化，不使用 CFG。

**自回归滚动训练**：训练时模拟推理外推分布，使用滚动 KV 缓存保留注意力槽和局部窗口的历史干净潜在表示，每个新 chunk 生成后更新缓存。这使固定上下文窗口能够稳定生成任意长度视频，同时维持恒定速度和交互性。

### Tiny VAE 解码器

为消除 VAE 解码瓶颈，MotionStream 采用紧凑的 Tiny VAE 解码器，在训练时增加数据量和针对性损失设计。Tiny VAE 将 Wan 2.1 吞吐量从 16.7 FPS 提升至 29.5 FPS，Wan 2.2 从 10.4 FPS 提升至 23.9 FPS，质量损失可忽略（Sec. 4.4, Table A2）。

### 流式推理引擎

推理时，学生模型以固定块大小（c3s1w1）逐块生成，利用滚动 KV 缓存和注意力槽维持恒定吞吐量，避免直接滑动窗口（c3s0w6）导致的延迟和吞吐量大幅波动（Figure 6）。学生模型使用 3 步生成最优，增加步数收益递减，减少至 2 步质量明显下降（Appendix C, Figure A2）。

## 实验与分析

### 核心实验设置

MotionStream 的实验围绕两个骨干网络展开：基于 Wan 2.1 的 1.3B 模型（480P 分辨率）和基于 Wan 2.2 的 5B 模型（720P 分辨率）。教师模型在 OpenVid-1M 和 Wan T2V 生成的合成数据上训练（480P 约 70K 样本，720P 约 30K 样本），轨迹由 CoTracker3 在 50×50 均匀网格上提取。因果蒸馏阶段使用相同的合成数据集，采样输入图像、文本提示和 2D 轨迹进行自回归滚动训练。所有延迟和吞吐量测量均在单张 H100 GPU 上使用 bfloat16 精度和 Flash Attention 3 完成，评估时统一将视频分辨率调整为 832×480 以消除尺度对 EPE 等指标的影响。

### 运动转移重建基准

Table 1 报告了在 DAVIS 验证集和 Sora Demo 子集上的运动转移重建结果。MotionStream 的因果蒸馏学生模型在 480P 下以 16.7 FPS 生成，720P 下达到 10.4 FPS，而所有基线方法速度均远低于 1 FPS。在质量指标上，学生模型保持了较强的重建能力：DAVIS 上 PSNR 16.20、LPIPS 0.443、EPE 7.80，Sora 子集上 PSNR 16.67、LPIPS 0.360、EPE 4.21。相比最强的运动转移基线 ATI（Wang et al., 2025a，基于 Wan 2.1-14B），MotionStream 在 DAVIS 上 PSNR 提升 0.87、EPE 降低 9.61，在 Sora 子集上 PSNR 提升 0.63、EPE 降低 1.91，且 ATI 的模型规模是 MotionStream 的 10 倍以上。


![[assets/figures/papers/paper_list_l8_https_openreview_net_forum_id_v1DKz5Vxr7/figures/004_Table_1.jpg]]
*Table 1: Benchmark on Motion Transfer (Reconstruction)*

教师模型在使用联合文本-运动引导（w_t=3.0, w_m=1.5）时取得最佳重建质量，DAVIS 上 EPE 降至 5.35。值得注意的是，从教师到学生的蒸馏过程仅带来有限的质量损失（DAVIS PSNR 从 16.61 降至 16.20），却换来了两个数量级的速度提升。

### 新视角合成任务

Table 2 展示了 MotionStream 在 LLFF 数据集上的新视角合成能力，这是一个模型未专门训练的任务，仅通过相机轨迹作为运动条件驱动。MotionStream 教师模型（1.3B）取得 PSNR 16.0、SSIM 0.42、LPIPS 0.21，显著优于专门的 3D 方法：相比 SEVA（Zhou et al., 2025b）PSNR 提升约 1.9，LPIPS 降低 0.08；相比 ViewCrafter（Yu et al., 2024）和 DepthSplat（Xu et al., 2025）也有明显优势。在速度方面，MotionStream 因果模型以 16.7 FPS 运行，而 DepthSplat 仅 1.40 FPS，速度提升超过 20 倍。这验证了运动条件框架的泛化能力：模型无需针对 3D 任务重新训练，仅通过改变输入轨迹即可实现相机控制。


![[assets/figures/papers/paper_list_l8_https_openreview_net_forum_id_v1DKz5Vxr7/figures/006_Table_2.jpg]]
*Table 2: Evaluation on Novel View Synthesis*

### 轨迹表示消融

Table 3 对比了两种轨迹编码方式。正弦位置编码加可学习轨迹头（PE-Head）在 DAVIS 上取得 PSNR 16.29、EPE 7.09，Sora 上 PSNR 17.15、EPE 4.14，均优于基于 RGB-VAE 的编码方式（DAVIS PSNR 16.03、EPE 7.83）。更关键的是效率差异：PE-Head 编码耗时仅 24.8 ms，而 RGB-VAE 需要 1053 ms，加速约 40 倍。这一效率优势对实时流式生成至关重要——RGB-VAE 的编码开销本身就会使系统无法达到交互帧率。


![[assets/figures/papers/paper_list_l8_https_openreview_net_forum_id_v1DKz5Vxr7/figures/007_Table_3.jpg]]
*Table 3: Comparing track representation methods. Our sinusoidal PE with learnable track head outperforms RGB-VAE in both quality and efficiency, achieving 40× faster encoding critical for real-time streaming*

### 注意力机制消融

Figure 6 和 Table 4 系统消融了稀疏注意力模式对长视频外推的影响。使用 Sora 子集中最长 241 帧的视频测试，核心发现如下：


![[assets/figures/papers/paper_list_l8_https_openreview_net_forum_id_v1DKz5Vxr7/figures/008_Figure_6.jpg]]
*Figure 6: Impact of Sparse Attention Patterns. Using longer clips (up to 241 frames) from the Sora subset, we ablate attention sink size and local window size in extrapolation scenarios. Having at least a single sink chunk is crucial, but more provides marginal benefit, while larger window sizes degrade performance as attending to long-past history allows errors to accumulate in context tokens*

**注意力槽的必要性**：配置 c3s1w1（chunk=3, sink=1, window=1）在 Sora Extended 上取得 LPIPS 0.464、EPE 25.34。移除注意力槽后（c3s0w1），LPIPS 恶化至 0.501，EPE 增至 33.62，表明模型在长视频生成中发生明显漂移。注意力槽通过持久化初始帧标记，为模型提供了稳定的空间锚点，防止误差累积导致的内容偏移。

**固定块大小 vs 滑动窗口**：直接使用滑动窗口注意力（c3s0w6，每个 chunk 关注前 6 个 chunk 而无 sink token）虽然 LPIPS 为 0.474，但其延迟和吞吐量出现大幅波动——这是流式应用无法接受的。固定块大小配置 c3s1w1 保持了稳定的延迟和吞吐量，因为 KV 缓存大小恒定，每次推理的计算量可预测。

**注意力槽数量**：增加注意力槽至更多块（如 c3s2w1）收益边际递减，LPIPS 仅从 0.464 微降至 0.461，但增加了 KV 缓存开销。单个注意力槽块已足以提供有效的空间锚定。

**局部窗口大小**：增大局部窗口（如 c3s1w3）反而导致性能下降（LPIPS 0.472），因为更大的历史窗口会引入更多早期累积的误差，干扰当前块的生成。

### 引导策略消融

Figure 4 和 Figure 5 分别从定量和定性角度消融了联合文本-运动引导。定量结果显示：纯文本引导（w_t=3.0, w_m=0）虽然视觉质量较好，但轨迹忠实度不足；纯运动引导（w_t=0, w_m=1.5）能精确跟随轨迹，但导致运动僵硬、缺乏自然动态。混合引导 w_t=3.0, w_m=1.5 在 PSNR、LPIPS 和 EPE 之间取得最佳平衡。定性对比（Figure 5）进一步揭示：纯运动引导下对象运动机械刻板，而文本引导即使面对不完美的轨迹也能保持自然运动和形状保持。混合引导结合了两者优势，既能忠实于用户指定的轨迹，又能维持自然的外观动态。


![[assets/figures/papers/paper_list_l8_https_openreview_net_forum_id_v1DKz5Vxr7/figures/005_Figure_4.jpg]]
*Figure 4: Quantitative ablation on guidance. We use Sora subset to ablate guidance strategies. Higher text guidance reduces overall metrics while motion guidance improves trajectory accuracy at the cost of visual quality (LPIPS). Figure 5: Qualitative ablation on guidance. Pure motion guidance produces rigid movements while text guidance enables natural motion and shape preservation even with imperfect tracks. Our Hybrid joint guidance balances these two*

### Tiny VAE 效率优化

Table A1 和 Table A2 报告了 Tiny VAE 解码器的效果。在 Sora 子集的 VAE 重建评估中，Tiny VAE 在保持可接受重建质量的前提下，将解码时间降低一个数量级以上。在流式生成场景中，替换为 Tiny VAE 后，Wan 2.1 骨干的吞吐量从 16.7 FPS 提升至 29.5 FPS（延迟从 0.69s 降至 0.39s），Wan 2.2 骨干从 10.4 FPS 提升至 23.9 FPS。Tiny VAE 几乎不损失生成质量，因为蒸馏学生模型本身已适应了 Tiny VAE 的潜在空间分布。

### 运动条件对生成能力的影响

Table A4 检验了注入运动控制是否损害预训练模型的生成能力。结果显示，添加运动条件并未显著降低基础模型的 I2V 生成质量，在某些情况下甚至通过显式运动约束改善了 FVD 分数。与更大规模的专用 I2V 基线（Wan 2.1 14B I2V）对比，MotionStream 的 1.3B 模型在 VBench-I2V 各维度上保持了竞争力（Table A3），表明轻量级运动控制模块的引入是低侵入性的。

### 学生模型推理步数

Appendix C 的 Figure A2 显示，学生模型使用 3 步生成达到最佳质量-效率平衡。增加步数至 4 步或更多收益递减，减少至 2 步则质量明显下降。3 步配置是蒸馏过程中的最优选择，与 DMD 框架的理论预期一致。

### 失败模式与局限性

尽管 MotionStream 在速度和可控性上取得了显著突破，但存在以下已知失败模式：

1. **场景变化适应不足**：固定注意力槽机制使模型倾向于保留初始帧的场景特征，当需要完全场景转换（如从室内走到室外）时，生成内容可能出现不一致或无法自然过渡到新环境。

2. **快速/不合理轨迹的伪影**：当用户提供的运动轨迹过快或物理上不合理时，模型可能产生时间不一致的运动或对象外观扭曲，尤其在复杂纹理区域。

3. **源细节保留困难**：在复杂场景、文本或运动意图下，小容量骨干网络（1.3B）难以完整保留源图像细节，部分细节在长序列生成中逐渐丢失。

4. **2D 轨迹的表达局限**：2D 轨迹表示难以编码完整的场景转换信息（如遮挡关系、深度变化），且注意力槽优先保持源特征，对新物体出现或持续场景变化的处理能力不足。

这些局限性指向了未来的改进方向：动态注意力槽策略以自适应刷新锚帧、训练中的轨迹增强以模拟不完美用户输入、以及更大规模骨干网络以提升细节保留能力。

### 补充图表

![[assets/figures/papers/paper_list_l8_https_openreview_net_forum_id_v1DKz5Vxr7/figures/016_Figure.jpg]]
*Figure: (a) Impact of Chunk Size and Sampling Steps in Throughput and Latency (b) LPIPS Over Varying Sampling Steps*

![[assets/figures/papers/paper_list_l8_https_openreview_net_forum_id_v1DKz5Vxr7/figures/009_Table.jpg]]

![[assets/figures/papers/paper_list_l8_https_openreview_net_forum_id_v1DKz5Vxr7/figures/012_Table.jpg]]
*Table: A1: Comparison of Causal VAE Models. We evaluate reconstruction quality on the Sora demo samples (resized to 81f×832×480) by encoding videos with the Full VAE encoder and decoding with different VAE variants. Our Tiny VAE achieves an order-of-magnitude faster decoding than Full VAEs while outperforming existing community implementations in reconstruction quality*

![[assets/figures/papers/paper_list_l8_https_openreview_net_forum_id_v1DKz5Vxr7/figures/013_Table.jpg]]
*Table: A2: Evaluating Tiny VAE in Streaming Generation Setup. Using the same distilled student model, we ablate the impact of switching VAE from original Full VAE to Tiny VAE in Sora demo subset. It’s important to note that even after changing to Tiny VAE, our distilled models still outperform all other baselines and quality differences compared to Full VAEs are marginal while achieving 1.75× and 2.3× higher throughput*

![[assets/figures/papers/paper_list_l8_https_openreview_net_forum_id_v1DKz5Vxr7/figures/014_Table.jpg]]
*Table: A3: VBench-I2V Results. We evaluate other baselines using VBench-I2V on Sora subset. While the results primarily depend on the choice of backbone, our models generally achieve high performance across all dimensions*

![[assets/figures/papers/paper_list_l8_https_openreview_net_forum_id_v1DKz5Vxr7/figures/018_Table.jpg]]
*Table: A4: Impact of Motion Control on Generative Quality. We evaluate whether injecting motion control degrades the pretrained model’s capability by comparing against a larger, dedicated I2V baseline (Wan 2.1 14B I2V). We also report performance when motion conditions are dropped. Results indicate that adding motion conditioning does not significantly degrade the base model’s generative quality. While removing motion conditions introduces a slight quality drop as our models were not optimized for this setting, the output still adheres to the given text and image inputs*


## 方法谱系与知识库定位

### 在运动条件视频生成中的定位

MotionStream 处于**运动条件视频生成**与**实时交互式生成**的交叉点。传统运动转移方法（如 **Image Conductor** (Li et al., 2025e) 基于 AnimateDiff、**Go-With-The-Flow** (Burgert et al., 2025) 和 **Diffusion-As-Shader** (Gu et al., 2025b) 基于 CogVideoX-5B、**ATI** (Wang et al., 2025a) 基于 Wan 2.1-14B）均采用离线扩散范式，在整个视频序列上进行双向注意力处理，导致不可接受的高延迟（数分钟级别）且只能生成固定长度序列。MotionStream 的核心突破在于将这一范式从**双向非因果处理**转变为**因果自回归流式生成**，通过分布匹配蒸馏（DMD）将教师模型的知识压缩到学生模型中，同时引入注意力槽和滚动 KV 缓存机制，使得固定上下文窗口能够稳定外推到任意长度视频。

### 关键设计选择的谱系分析

**轨迹表示方式的演进。** 现有方法普遍将轨迹渲染为 RGB 着色图并通过 VAE 编码（如 Image Conductor、ATI），这带来了两个瓶颈：编码延迟高达秒级，且 RGB-VAE 压缩损失会模糊精确的轨迹位置。MotionStream 改用正弦位置编码加可学习轨迹头的方案（Table 3），将编码时间从 1053 ms 降至 24.8 ms（约 40 倍加速），同时在 DAVIS 和 Sora 子集上 PSNR 分别提升 0.26 dB 和 0.16 dB。这一设计选择本质上是将轨迹信号从“像素级渲染-压缩”通路迁移到“坐标级编码-拼接”通路，消除了 VAE 瓶颈对实时性的制约。

**注意力模式的根本性重构。** 双向注意力（教师模型）提供了最强的条件建模能力，但无法用于流式生成；全因果注意力（标准自回归）虽然支持流式，但在长视频外推中会出现严重的分布漂移。MotionStream 通过可视化分析（Figure 3）发现初始帧标记在去噪生成过程中持续被多个注意力头关注——这一“注意力槽”现象与 LLM 中观察到的初始 token 注意力集中现象类似。基于此洞察，MotionStream 设计了滑动窗口因果注意力 + 注意力槽的混合模式：初始帧标记作为持久化的“锚”保留在 KV 缓存中，当前块仅关注最近的局部窗口和注意力槽块。消融实验（Table 4, Figure 6）表明，至少 1 个注意力槽块（c3s1w1）对于防止外推漂移是必需的（无注意力槽时 LPIPS 从 0.464 恶化至 0.501，EPE 显著增加），而更大的局部窗口反而因历史错误累积降低性能。

**流式推理的系统性优化。** 除了注意力机制的改造，MotionStream 在推理栈的多个层面进行了协同优化：Tiny VAE 解码器将解码吞吐量提升 1.75-2.3 倍（Wan 2.1 从 16.7 FPS 升至 29.5 FPS，Wan 2.2 从 10.4 FPS 升至 23.9 FPS）；固定块大小（chunk-3）避免了滑动窗口（c3s0w6）导致的延迟和吞吐量大幅波动（Table 4）；KV 缓存滚动机制使得每步计算复杂度保持恒定，而非随视频长度线性增长。

### 引导策略的权衡机制

MotionStream 采用联合文本-运动引导（$w_t=3.0, w_m=1.5$），这一设计源于对纯运动引导和纯文本引导各自失败模式的系统分析（Figure 4, Figure 5）。纯运动引导（$w_t=0$）虽然轨迹精度最高，但导致运动僵硬、缺乏自然动态，因为模型失去了文本条件提供的语义先验和形状保持能力。纯文本引导（$w_m=0$）则丧失轨迹忠实度，生成的运动与用户指定的轨迹偏离。混合引导在两者之间取得平衡，且通过将引导蒸馏到学生模型中（公式 $s_{\mathrm{real}}$），消除了推理时的多步 CFG 评估开销，使得实时交互成为可能。

### 跨任务泛化能力

MotionStream 的流程在新视角合成任务上展现出意外的强泛化能力。在 LLFF 基准上（Table 2），MotionStream Teacher（1.3B）以 PSNR 16.0、SSIM 0.42、LPIPS 0.21 显著优于专门的 3D 方法（如 **SEVA** (Zhou et al., 2025b) 的 14.1/0.30/0.29、**ViewCrafter** (Yu et al., 2024) 的 14.3/0.31/0.27），且因果蒸馏版本以 16.7 FPS 的速度比 **DepthSplat** (Xu et al., 2025) 的 1.40 FPS 快 20 倍以上。这表明 2D 轨迹条件结合强大的视频先验可以隐式编码 3D 几何约束，而无需显式的深度或相机参数建模。

### 适用边界与局限性

尽管 MotionStream 在实时性和重建质量上取得了显著进展，其设计存在几个根本性限制：

1. **固定注意力槽的场景锁定效应。** 注意力槽机制强制模型持续关注初始帧标记，这在保持时间一致性方面是关键优势，但也导致模型倾向于保留初始场景的外观和布局，难以适应需要完全场景转换的应用（如长距离漫游、场景切换）。这是注意力槽机制固有的“锚定-漂移”权衡：锚越强，外推越稳定，但场景变化的灵活性越低。

2. **2D 轨迹表示的表达力上限。** 2D 轨迹本质上是稀疏的屏幕空间约束，无法编码完整的 3D 场景变换（如遮挡关系变化、深度排序、物体进出视野）。当轨迹运动过快或物理上不合理时，模型会产生时间不一致或外观扭曲的伪影。这一问题在复杂场景下尤为突出，且小容量骨干网络（1.3B）比大容量网络（5B）更容易出现源细节丢失。

3. **运动条件与文本条件的潜在冲突。** 联合引导虽然通过权重调谐实现了平衡，但本质上是一个多目标优化问题的近似解。当文本描述的运动模式与轨迹指定的运动模式冲突时，模型需要在语义忠实度和轨迹精确度之间做出取舍，这可能导致生成结果在两种条件之间“折中”而非精确满足任一条件。

### 开放问题与后续方向

1. **动态注意力槽策略。** 当前固定初始帧作为注意力槽的设计限制了场景演化能力。一个自然的发展方向是设计动态注意力槽刷新机制——当场景变化累积到一定程度时，自动更新锚帧以支持“世界模型”式的持续探索，同时保持时间一致性。这需要解决何时刷新、如何平滑过渡、以及新旧锚帧之间的信息继承等问题。

2. **轨迹增强与鲁棒性训练。** 当前模型在训练时使用 CoTracker3 提取的精确轨迹，但实际交互场景中用户输入的轨迹往往是粗糙、不完整甚至物理上不合理的。如何在训练中融入有效的轨迹增强策略（如加噪、中断、抖动、延迟），使模型学会从“不完美信号”中推断合理运动，是提升交互体验的关键。

3. **源细节保持能力的扩展。** 在复杂场景、长文本提示或极端运动条件下，模型（尤其小容量骨干）难以保持源图像的精细细节。这一问题可能需要更大规模骨干网络（如 14B 级别）的验证，以及专门设计的细节保持损失或注意力约束。

4. **3D 感知轨迹表示。** 2D 轨迹的表达力上限限制了场景变换的复杂度。将轨迹表示扩展到 3D（如结合深度估计的 2.5D 轨迹或稀疏 3D 点云轨迹）可能显著提升模型处理遮挡、视角变化和场景转换的能力，但也会引入额外的计算开销和标注需求。

## 原文 PDF

![[paperPDFs/ICLR_2026/MotionStream_Real_Time_Video_Generation_with_Interactive_Motion_Controls.pdf]]
