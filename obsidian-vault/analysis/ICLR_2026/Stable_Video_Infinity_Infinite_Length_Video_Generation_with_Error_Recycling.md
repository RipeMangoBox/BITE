---
title: "Stable Video Infinity: Infinite-Length Video Generation with Error Recycling"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/Stable_Video_Infinity_Infinite_Length_Video_Generation_with_Error_Recycling.pdf
project_link: https://stable-video-infinity.github.io/homepage/
code_link: null
openreview_forum_id: X96Ei9n34a
aliases:
- SVISERFT
- SVIILVGER
tags:
- ICLR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: "引入错误回收微调（ERFT），在训练过程中主动注入、计算、存储并重放模型自身产生的误差，打破无误差假设，迫使 DiT 学习识别并纠正自身错误。"
primary_logic: "将模型自生成的误差作为监督信号进行闭环回收，弥合训练与测试的假设差距，在不增加推理成本的前提下实现稳定、非循环的无限长度视频生成。"
claims:
- "SVI-Shot 在超长一致视频生成中主体一致性达到 97.50%，对比最强基线 FramePack（79.37%）提升 18.13 个百分点，差距巨大。"
- "移除参考图像误差 E_img 的消融实验导致所有指标大幅下降，证明交叉片段条件误差是长视频崩溃的主要驱动因素。"
- "随着错误回收强度（LoRA alpha）降低，一致性等指标持续单调下降，证实积极纠正自身错误对稳定长视频至关重要。"
- "天真的视频扩展（复制片段、乒乓回放）可以愚弄一致性指标，而 SVI 在全部指标间取得平衡，体现了真实的生成质量。"
---

# Stable Video Infinity: Infinite-Length Video Generation with Error Recycling

> [!tip] 核心洞察
> 将模型自生成的误差作为监督信号进行闭环回收，弥合训练与测试的假设差距，在不增加推理成本的前提下实现稳定、非循环的无限长度视频生成。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 稳定视频无限：通过错误回收实现无限长度视频生成 |
| 英文题名 | Stable Video Infinity: Infinite-Length Video Generation with Error Recycling |
| 会议/期刊 | ICLR 2026 (Oral) |
| Links | [paper](https://openreview.net/forum?id=X96Ei9n34a) · [Project](https://stable-video-infinity.github.io/homepage/) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/image_and_video_generation |
| Method | Stable Video Infinity (SVI) with Error-Recycling Fine-Tuning |
| Dataset | 自建超长一致视频生成基准 (50-clip), VBench 长视频生成 (50-clip), 音频驱动长对话, 骨骼驱动长舞蹈 |

> [!tip] 效果简介
> - 自建超长一致视频生成基准 (50-clip) 上，Subject Consistency 为 97.50% (SVI-Shot)，对比 80.00% (Wan 2.1)，变化 +17.50%。
> - VBench 长视频生成 (50-clip) 上，Subject Consistency 为 96.24% (SVI)，对比 76.11% (Wan 2.1)，变化 +20.13%。
> - 音频驱动长对话 上，Sync-C 为 6.12 (SVI-Talk)，对比 0.21 (Wan 2.1)，变化 +5.91。

## 概要

**问题瓶颈**：当前基于扩散变换器（DiT）的视频生成模型在训练时依赖无误差的干净潜在变量，而测试时自回归生成不可避免地引入预测误差与条件误差，二者相互增强并迅速累积，导致长视频在主体一致性、美学质量与成像质量上严重退化。这一训练-测试假设差距是制约无限长度视频生成的根本障碍。

**核心方法**：Stable Video Infinity（SVI）提出**错误回收微调**（Error-Recycling Fine-Tuning, ERFT），将 DiT 自身产生的误差作为监督信号进行闭环回收。具体而言，SVI 在训练中主动注入、计算并存储模型自生成的误差，迫使 DiT 学习识别并纠正自身错误，从而弥合训练与测试的假设差距，在不增加推理成本的前提下实现稳定、非循环的无限长度视频生成。

**方法定位**：SVI 属于参数高效微调范式，在冻住的 DiT 基础上通过 LoRA 适配器进行错误回收训练。其技术路线区别于基于噪声重调度的 **StreamingT2V**、基于历史指导的 **HistoryGuidance** 以及帧打包方法 **FramePack** 等现有长视频扩展方案，开辟了以“自生成误差作为闭环监督信号”的新视角。

**主要结果**：
- 在自建超长一致视频生成基准（50 片段）上，SVI-Shot 的主体一致性达到 **97.50%**，对比最强基线 FramePack（79.37%）提升 **18.13 个百分点**；对比通用强基线 Wan 2.1（80.00%）提升 **17.50 个百分点**。
- 在 VBench 长视频生成基准（50 片段）上，SVI 的主体一致性为 **96.24%**，较 Wan 2.1（76.11%）提升 **20.13 个百分点**。
- 在音频驱动长对话任务上，SVI-Talk 的 Sync-C 指标达到 **6.12**，远超 Wan 2.1 的 0.21。
- 在骨骼驱动长舞蹈任务上，SVI-Dance 的 PSNR 达到 **20.01**，优于专用方法 UniAnimate-DiT 的 18.97。

**决定性证据**：消融实验表明，移除参考图像误差 $E_{\mathrm{img}}$ 会导致所有指标大幅下降，证实交叉片段条件误差是长视频崩溃的主要驱动因素；随着错误回收强度（LoRA α）降低，一致性等指标持续单调下降，证实主动纠正自身错误对稳定长视频至关重要。天真的视频扩展（复制片段、乒乓回放）虽然可以愚弄一致性指标，但动态性降为零，而 SVI 在所有指标间取得了真实平衡。

### 视频生成范式的演进与瓶颈

扩散变换器（Diffusion Transformer, DiT）的规模化扩展推动了视频生成领域的快速发展。当前主流的视频生成范式可归纳为两类：**视频生成 DiT** 与**视频恢复 DiT**。

- **视频生成 DiT** 采用流匹配（Flow Matching）框架，在训练时假设历史轨迹与中间状态完全无误差，直接从噪声和干净图像条件中预测速度场。其训练目标为最小化预测速度与真实速度之间的均方误差（见 Eq. 1）。然而，在测试阶段的自回归生成过程中，前序片段产生的预测误差会作为条件输入传递给后续片段，导致**预测误差**与**条件误差**相互增强并迅速累积——这正是 Figure 1 与 Figure 2 所揭示的训练-测试假设差距。

- **视频恢复 DiT** 虽然显式考虑了误差输入，但其训练目标是将退化的潜在变量恢复为干净版本，本质上执行的是“修复”而非“生成”。这种方法在长视频扩展中容易丧失动态多样性和美学质量，且无法从根本上解决误差累积问题。

### 核心瓶颈：训练-测试假设差距

现有方法面临的根本瓶颈在于：**训练时的无误差假设与测试时自回归使用误差污染输入之间存在根本性假设差距**。具体而言（Figure 2）：

1. **预测误差**：由自回归生成的回归特性引起，影响轨迹终点 $X_{\mathrm{vid}}$，使生成视频的末端帧偏离干净分布。
2. **条件误差**：由包含误差的图像条件 $\tilde{X}_{\mathrm{noi}}^{\mathrm{img}}$ 引起，影响轨迹起点，使后续片段的起始状态已经包含偏差。

这两种误差在自回归循环中相互增强，导致视频一致性、美学质量和成像质量随视频长度增加而严重退化。现有的长视频生成方法（如 **StreamingT2V**、**HistoryGuidance**、**FramePack** 等）虽然通过噪声重调度、历史指导或帧打包等策略试图缓解这一问题，但均未从根本上打破训练与测试之间的假设差距。

### 本文动机

本文从一个新的视角出发：**将 DiT 自身产生的误差作为监督信号进行闭环回收**，迫使模型在训练过程中主动学习识别并纠正自身错误。这一思路的核心洞察在于：与其被动地容忍误差累积，不如在训练阶段就模拟测试时的误差污染环境，让模型学会在误差存在的条件下仍然指向干净的生成目标。通过这种“错误回收”（Error Recycling）机制，可以在不增加推理成本的前提下，弥合训练与测试的假设差距，实现稳定、非循环的无限长度视频生成。

## 核心方法与创新机理

### 问题本质：训练-测试假设差距

长视频生成的根本瓶颈并非模型容量或计算资源不足，而在于一个结构性的**训练-测试假设差距**。如图 2 所示，现有基于 DiT 的流匹配视频生成模型在训练时假设历史轨迹和中间状态完全无误差，以干净潜在变量 $X_{\mathrm{vid}}$ 为目标进行速度预测。然而在测试时，自回归生成过程中每一步的预测误差会通过两个渠道向后续步骤传播：(1) **预测误差**——回归性质导致轨迹终点 $X_{\mathrm{vid}}$ 偏离真实值；(2) **条件误差**——包含误差的图像条件 $\tilde{X}_{\mathrm{noi}}^{\mathrm{img}}$ 进一步污染输入的起点。这两种误差相互增强，迅速累积，导致视频一致性、美学质量和成像质量严重退化。

SVI 的核心洞察是：**将模型自生成的误差作为监督信号进行闭环回收，弥合训练与测试的假设差距，在不增加推理成本的前提下实现稳定、非循环的无限长度视频生成。**

### 关键机制：错误回收微调 (ERFT)

SVI 通过错误回收微调 (Error-Recycling Fine-Tuning, ERFT) 引入了三个相互关联的 changed slots，从根本上打破了传统训练中的无误差假设：

**1. 训练数据假设：从无误差到误差注入**

传统流匹配训练使用完全干净的潜在变量（$X_{\mathrm{vid}}$、$X_{\mathrm{noi}}$、$X_{\mathrm{img}}$），而 SVI 以概率 $p$ 向这些干净输入注入历史或自生成的误差 $E_{\mathrm{vid}}$、$E_{\mathrm{noi}}$、$E_{\mathrm{img}}$，模拟测试时误差累积的退化输入：

$$\tilde{X}_{\mathrm{vid}} = X_{\mathrm{vid}} + \mathbb{I}_{\mathrm{vid}} \cdot E_{\mathrm{vid}}, \quad \tilde{X}_{\mathrm{noi}} = X_{\mathrm{noi}} + \mathbb{I}_{\mathrm{noi}} \cdot E_{\mathrm{noi}}, \quad \tilde{X}_{\mathrm{img}} = X_{\mathrm{img}} + \mathbb{I}_{\mathrm{img}} \cdot E_{\mathrm{img}}$$

同时保留 50% 概率使用无误差输入，以维持基础生成能力。

**2. 训练监督目标：从预测原始速度到预测错误回收速度**

传统目标是最小化预测速度与真实速度 $V_t = X_{\mathrm{vid}} - X_{\mathrm{noi}}$ 之间的差距。SVI 转而预测**错误回收速度** $V_t^{\mathrm{rcy}}$，该速度始终指向干净潜在变量 $X_{\mathrm{vid}}$，独立于当前状态 $\tilde{X}_t$ 和历史轨迹的正确性。这使得模型学会从任意误差状态出发，主动纠正轨迹回到正确路径。

$$\mathcal{L}_{\mathrm{SVI}} = \mathbb{E}_{\tilde{X}_{\mathrm{vid}}, \tilde{X}_{\mathrm{noi}}, \tilde{X}_{\mathrm{img}}, C, t} \big| u(\tilde{X}_t, \tilde{X}_{\mathrm{img}}, C, t; \theta) - V_t^{\mathrm{rcy}} \big|^2$$

**3. 误差处理与纠正：从无显式机制到闭环回放记忆**

SVI 构建了一套完整的误差闭环系统：
- **双向误差计算**：通过单步前向-后向积分近似预测，计算视频潜在误差 $E_{\mathrm{vid}}$、噪声误差 $E_{\mathrm{noi}}$ 和图像误差 $E_{\mathrm{img}}$；
- **误差回放记忆**：按测试时间步（$N_{\mathrm{test}}=50$）离散化存储误差，每时间步维护上限 $Z=500$ 的误差池，满时替换最相似的误差以保持多样性；
- **选择性重采样**：从记忆库中按策略采样误差注入新一轮训练输入，形成闭环循环。

### 与传统方法的本质区别

SVI 与现有长视频生成方法存在根本性差异。**StreamingT2V** 和 **HistoryGuidance** 等方法试图在推理时通过噪声重调度或历史指导来缓解误差，但并未触及训练时的假设差距。**FramePack** 等帧打包方法通过改变输入结构来扩展长度，但同样受限于误差累积。SVI 首次将 DiT 的自生成误差转化为训练监督信号，使模型在训练阶段就学会识别和纠正自身错误，从而在推理时无需额外计算开销即可实现稳定生成。这一范式转变使得 SVI 在超长一致视频生成中将主体一致性从最强基线 FramePack 的 79.37% 提升至 97.50%，提升幅度达 18.13 个百分点（Table 1）。

### 消融实验的关键证据

消融实验进一步验证了各 changed slots 的必要性。移除参考图像误差 $E_{\mathrm{img}}$ 导致所有指标大幅下降（Table 4），证实交叉片段条件误差是长视频崩溃的主要驱动因素。降低 LoRA 的 $\alpha$ 值（减弱错误回收强度）导致指标单调下降（Table 7），证明性能提升源于主动纠正自身错误而非其他因素。自生成误差优于人工图像增强（颜色偏移、模糊、锐化），结合两者反而引起冲突（Table 6），表明模型自身误差具有独特分布，无法用简单数据增强替代。

![[assets/figures/papers/paper_list_l12_https_openreview_net_forum_id_X96Ei9n34a/figures/024_Figure_10.jpg]]
*Figure 10: Overview of the proposed end-to-end automatic pipeline, which is able to generate infinite short films from user-given keywords. This engine is used to generate the prompt streams according to a specific storyline for our creative video generation benchmarks*

Stable Video Infinity (SVI) 的核心目标是以非循环、自回归的方式生成无限长度的视频，同时保持主体一致性、成像质量和动态自然度。其整体框架围绕一个闭环的错误回收微调（Error-Recycling Fine-Tuning, ERFT）机制构建，该机制将扩散变换器（DiT）在生成过程中自产生的误差作为监督信号重新注入训练，从而弥合训练时的无误差假设与测试时误差累积的现实之间的根本性差距。

### 框架概览

SVI 的 pipeline 由四个核心模块串联成一个闭环循环，如图 3 所示：

1.  **错误注入 (Error Injection)**：从错误回放记忆中采样历史误差，以概率 $p$ 注入到干净的视频潜在变量 $X_{\mathrm{vid}}$、噪声 $X_{\mathrm{noi}}$ 和参考图像潜在变量 $X_{\mathrm{img}}$ 中，人为构造退化输入 $\tilde{X}$，打破训练中的无误差假设。
2.  **双向误差计算 (Bidirectional Error Curation)**：利用单步前向和后向积分近似预测，高效地计算出三种关键的误差项——视频潜在误差 $E_{\mathrm{vid}}$、噪声误差 $E_{\mathrm{noi}}$ 和参考图像误差 $E_{\mathrm{img}}$。
3.  **错误回放记忆 (Error Replay Memory)**：将计算出的误差按测试时间步离散化分桶存储，动态维护一个误差池。当存储达到上限时，替换最相似的旧误差以保持多样性。
4.  **LoRA 速度预测 (Velocity Prediction with LoRA)**：在冻结的 DiT 主干网络上通过 LoRA 进行微调，接收注入误差后的输入，预测一个始终指向干净潜在变量的“误差回收速度” $V_t^{\mathrm{rcy}}$。

### 模块交互与数据流

整个流程构成了一个自监督的闭环系统：

- **训练阶段**：首先，从**错误回放记忆**中采样一组误差，送入**错误注入**模块，将干净数据污染。然后，被污染的输入进入 DiT 进行前向传播。与此同时，**双向误差计算**模块利用 DiT 对干净数据和污染数据分别进行单步预测，计算出新的误差。这些新误差被存入**错误回放记忆**，用于未来的训练迭代。模型的优化目标是让**LoRA 速度预测**模块输出的速度尽可能接近预先计算好的误差回收速度 $V_t^{\mathrm{rcy}}$，损失函数为：

    $$ \mathcal{L}_{\mathrm{SVI}} = \mathbb{E}_{\tilde{X}_{\mathrm{vid}}, \tilde{X}_{\mathrm{noi}}, \tilde{X}_{\mathrm{img}}, C, t} \big| u(\tilde{X}_t, \tilde{X}_{\mathrm{img}}, C, t; \theta) - V_t^{\mathrm{rcy}} \big|^2 $$

- **推理阶段**：框架退化为标准的自回归生成流程，不引入额外计算开销。DiT 以常规方式逐片段生成视频，但由于在训练时已学会识别和纠正自身错误，其生成过程的误差累积被显著抑制。

### 错误类型与角色

框架明确定义并处理了三类在自回归生成中累积的错误，消融实验（Table 4）证实它们对长视频稳定性至关重要：

- **视频潜在误差 $E_{\mathrm{vid}}$**：模型预测的视频潜在变量与干净目标之间的差距，反映了轨迹末端的预测误差。
- **噪声误差 $E_{\mathrm{noi}}$**：在给定含误差参考图像的条件下，模型预测的初始噪声与理想噪声之间的差距，反映了条件误差对轨迹起点的污染。
- **参考图像误差 $E_{\mathrm{img}}$**：通过对 $E_{\mathrm{vid}}$ 跨时间步均匀采样得到，用于模拟跨片段条件信号（即上一片段的最后一帧）的退化。消融实验表明，移除该项会导致所有指标大幅下降，是驱动长视频崩溃的决定性因素。

通过上述闭环设计，SVI 在不改变推理架构、不增加推理成本的前提下，赋予了 DiT 主动纠错和稳定自回归生成的能力。

### 问题形式化：训练-测试假设差距

SVI 的核心洞察在于揭示并弥合视频生成 DiT 在训练与测试之间的根本性假设差距。在标准流匹配训练中（Eq. 1），模型假设历史轨迹和中间状态均无误差：

$$
\mathcal{L} = \mathbb{E}_{X_{\mathrm{noi}}, X_{\mathrm{vid}}, X_{\mathrm{img}}, C, t} {\lvert u(X_t, X_{\mathrm{img}}, C, t; \theta) - V_t \rvert}^2
$$

其中 $X_t$ 由无误差的干净潜在变量线性插值得到，$V_t = X_{\mathrm{vid}} - X_{\mathrm{noi}}$ 为指向干净视频的真实速度。然而在测试时，自回归生成通过 ODE 逐步积分实现（Eq. 2）：

$$
X_{t_{k+1}} = X_{t_k} + (t_{k+1} - t_k) \cdot u(X_{t_k}, X_{\mathrm{img}}, t_k; \theta)
$$

每一步的预测误差会累积到下一片段的条件输入中，导致**预测误差**（模型回归性质导致的轨迹末端偏差）与**条件误差**（误差污染的参考图像输入）相互增强，迅速使生成崩溃。这一假设差距构成了长视频生成的核心瓶颈。

### 错误回收微调（ERFT）总体框架

为打破上述假设差距，SVI 提出错误回收微调（Error-Recycling Fine-Tuning, ERFT），构建了一个闭环的错误注入、计算、存储与重放机制（Figure 3）。其核心思想是将 DiT 自生成的误差作为监督信号进行回收，迫使模型学习识别并主动纠正自身错误，预测始终指向干净潜在变量的**错误回收速度** $V_t^{\mathrm{rcy}}$。

ERFT 包含四个关键模块：

1. **错误注入（Error Injection）**：将回放记忆中的历史误差按概率注入干净输入，模拟测试时的误差累积退化。
2. **双向误差计算（Bidirectional Error Curation）**：通过单步前向-后向积分近似预测，高效计算三类误差项。
3. **错误回放记忆（Error Replay Memory）**：按时间步分桶存储误差，动态维护误差池并选择性采样。
4. **LoRA 速度预测（Velocity Prediction with LoRA）**：在冻住的 DiT 上通过 LoRA 微调，接收误差注入输入，预测错误回收速度。

### 错误注入

训练时，SVI 以概率 $p$ 向干净的视频潜在变量 $X_{\mathrm{vid}}$、噪声 $X_{\mathrm{noi}}$ 和参考图像潜在变量 $X_{\mathrm{img}}$ 注入从回放记忆中采样的误差（Eq. 3）：

$$
\tilde{X}_{\mathrm{vid}} = X_{\mathrm{vid}} + \mathbb{I}_{\mathrm{vid}} \cdot E_{\mathrm{vid}}, \quad \tilde{X}_{\mathrm{noi}} = X_{\mathrm{noi}} + \mathbb{I}_{\mathrm{noi}} \cdot E_{\mathrm{noi}}, \quad \tilde{X}_{\mathrm{img}} = X_{\mathrm{img}} + \mathbb{I}_{\mathrm{img}} \cdot E_{\mathrm{img}}
$$

其中 $\mathbb{I}_{*} \in \{0, 1\}$ 为指示变量，控制各误差项的注入概率。同时，以概率 $p = 0.5$ 保留无误差输入，以维持模型的基础生成能力。这一设计直接打破了训练中的无误差假设，使模型暴露于与测试一致的退化输入分布。

### 双向误差计算

为高效获取训练所需的误差监督信号，SVI 采用单步前向和后向积分来近似误差嵌入的预测（Figure 4）：

- **前向方向**：从误差注入的噪声 $\tilde{X}_{\mathrm{noi}}$ 出发，单步积分得到视频潜在预测 $\hat{X}_{\mathrm{vid}}$。
- **后向方向**：从误差注入的视频 $\tilde{X}_{\mathrm{vid}}$ 出发，反向单步积分得到噪声预测 $\hat{X}_{\mathrm{noi}}^{\mathrm{img}}$。

基于这些近似预测，统一计算三类误差（Eq. 4）：

$$
E_{\mathrm{vid}} = \hat{X}_{\mathrm{vid}} - X_{\mathrm{vid}}^{\mathrm{rcy}}, \quad E_{\mathrm{noi}} = \hat{X}_{\mathrm{noi}}^{\mathrm{img}} - X_{\mathrm{noi}}^{\mathrm{rcy}}, \quad E_{\mathrm{img}} = \mathrm{Unif}_T(E_{\mathrm{vid}})
$$

其中 $X_{\mathrm{vid}}^{\mathrm{rcy}}$ 和 $X_{\mathrm{noi}}^{\mathrm{rcy}}$ 为指向干净潜在变量的回收目标。$E_{\mathrm{img}}$ 通过对视频误差在时间维度均匀采样得到，用于模拟跨片段的条件误差。

### 错误回放记忆

计算得到的误差被动态存入按测试时间步离散化的回放记忆库 $B_{\mathrm{vid}, n}$ 和 $B_{\mathrm{noi}, n}$。训练时间步 $T_{\mathrm{tra}}$（通常 1000 步）被对齐到测试时间步 $T_{\mathrm{test}}$（通常 50 步）。每个时间步桶的误差数量上限为 $Z = 500$，当桶满时替换最相似的误差以维持多样性。

训练时，从记忆库中按选择性策略采样误差（Eq. 5）：

$$
E_{\mathrm{vid}} = \mathrm{Unif}(B_{\mathrm{vid},n}), \quad E_{\mathrm{noi}} = \mathrm{Unif}(B_{\mathrm{noi},n}), \quad E_{\mathrm{img}} = \mathrm{Unif}_T(B_{\mathrm{vid}})
$$

视频误差和噪声误差从对应时间步桶中均匀采样，图像误差则从视频误差池中跨时间步均匀采样，以覆盖不同的条件误差模式。

### 优化目标

SVI 的训练目标是最小化预测速度与错误回收速度之间的均方误差：

$$
\mathcal{L}_{\mathrm{SVI}} = \mathbb{E}_{\tilde{X}_{\mathrm{vid}}, \tilde{X}_{\mathrm{noi}}, \tilde{X}_{\mathrm{img}}, C, t} \big| u(\tilde{X}_t, \tilde{X}_{\mathrm{img}}, C, t; \theta) - V_t^{\mathrm{rcy}} \big|^2
$$

其中 $V_t^{\mathrm{rcy}} = X_{\mathrm{vid}}^{\mathrm{rcy}} - X_{\mathrm{noi}}^{\mathrm{rcy}}$ 始终指向干净潜在变量，与当前状态和历史轨迹的正确性无关。这一设计使 DiT 在自回归生成中能够主动纠正误差，而非被动适应退化输入。为保持用户灵活性，仅训练 LoRA 参数，冻住基础 DiT 权重。

## 实验与关键发现

### 主实验结果

SVI 在通用视频生成、音频驱动说话脸和骨骼驱动舞蹈三个主要场景上进行了系统评估，所有对比均基于自建的超长视频生成基准（50 个片段串联）和标准 VBench 基准。

**通用视频生成。** 表 1 报告了一致场景、创意场景和超长一致场景下的定量结果。在一致视频生成中，SVI-Shot 取得 **93.52% 的主体一致性**和 **95.33% 的背景一致性**，分别超出最强基线 FramePack 5.05 和 3.37 个百分点；在成像质量上领先 5.16 个百分点。当场景扩展至超长一致生成（50 片段），Wan 2.1 和 FramePack 的主体一致性分别下降 7.03 和 13.71 个百分点，而 SVI-Shot 仅下降 **0.63 个百分点**，达到 **97.50%**，同时保持了令人满意的动态程度。在创意视频生成中，SVI-Shot 在一致性、美学质量和动态性三个维度取得了最佳平衡，没有出现其他方法为追求一致性而牺牲动态性的情况。

**音频驱动长对话。** 表 2 显示，SVI-Talk 在唇音同步指标 Sync-C 上达到 **6.12**，远超 Wan 2.1 的 0.21 和 MultiTalk 的 3.35，提升幅度达 5.91。这表明错误回收微调有效抑制了长对话中条件误差的累积，保持了跨片段的唇形一致性。

**骨骼驱动长舞蹈。** 表 3 显示，SVI-Dance 在 PSNR 上达到 **20.01**，比专用方法 UniAnimate-DiT 的 18.97 提升 1.04；在 SSIM 和 LPIPS 上也取得最优或次优结果。这验证了 SVI 框架对结构化控制信号的兼容性。

**VBench 标准基准。** 在 VBench 长视频生成（50 片段）上（表 11），SVI 的主体一致性达到 **96.24%**，比 Wan 2.1 的 76.11% 提升 20.13 个百分点，背景一致性和运动平滑度也全面领先，证明了方法在标准评测体系下的有效性。

### 消融实验

**误差项的消融。** 表 4 系统移除了三类误差注入。移除参考图像误差 $E_{\text{img}}$ 导致所有指标大幅下降，主体一致性从 97.50% 骤降至 86.12%，成像质量从 65.25% 降至 58.37%。这揭示了一个关键因果机制：交叉片段的条件误差是长视频崩溃的**决定性驱动因素**——当参考图像被误差污染后，每个新片段的条件输入都携带偏差，导致误差在片段间持续放大。移除视频潜在误差 $E_{\text{vid}}$ 和噪声误差 $E_{\text{noi}}$ 也造成明显退化，但幅度较小，说明三者协同作用。

![[assets/figures/papers/paper_list_l12_https_openreview_net_forum_id_X96Ei9n34a/figures/008_Table_4.jpg]]

![[assets/figures/papers/paper_list_l12_https_openreview_net_forum_id_X96Ei9n34a/figures/016_Table_4.jpg]]
*Table 4: Ablation study on each error term*

**天真扩展方法的对比。** 表 5 探索了简单的视频扩展策略（复制片段、乒乓回放）。这些方法可以**愚弄一致性指标**——乒乓回放甚至取得了异常高的一致性分数——但动态性降低为 0%，完全丧失了视频的时序变化。SVI 在一致性、质量和动态性之间取得了真实平衡，没有通过牺牲运动来换取表面的一致。

![[assets/figures/papers/paper_list_l12_https_openreview_net_forum_id_X96Ei9n34a/figures/025_Table_5.jpg]]
*Table 5: Exploring naive video extension methods. The best is highlighted in red (abnormally large)*

**自生成误差 vs. 人工增强误差。** 表 6 对比了使用模型自生成误差与人工图像增强（颜色偏移、模糊、锐化）构造误差的效果。自生成误差在所有指标上显著优于人工增强；将两者结合反而引起冲突，导致性能下降。这证明模型自身的误差具有**独特的分布特性**，人工设计的扰动无法有效模拟。

![[assets/figures/papers/paper_list_l12_https_openreview_net_forum_id_X96Ei9n34a/figures/026_Table_6.jpg]]
*Table 6: Comparison between self-generated errors and handcraft errors with image augmentation*

**错误回收强度。** 表 7 通过调整 LoRA 的 $\alpha$ 参数控制错误回收强度。随着 $\alpha$ 从 16 降至 1，主体一致性从 97.50% 单调下降至 93.21%，成像质量从 65.25% 降至 60.12%。这种**单调趋势**直接证实 SVI 的性能源于主动纠正自身错误，而非 LoRA 微调的附带效应。

![[assets/figures/papers/paper_list_l12_https_openreview_net_forum_id_X96Ei9n34a/figures/027_Table_7.jpg]]
*Table 7: Analysis on error-recycling intensity by modifying LoRA alpha*

**误差缓存池大小。** 表 8 显示，缓存池大小 $Z=500$ 时性能达到饱和，继续增大至 1000 并无显著提升。这表明 500 个样本已能充分覆盖误差多样性，在计算开销与性能之间取得了最优平衡。

**LoRA 秩。** 表 9 探索了不同 LoRA 秩的影响。秩从 16 提升至 64 带来明显增益，继续增至 128 提升边际递减。这证明参数高效的微调策略（秩 64 以上）即可提供足够的纠错能力。

**在线误差注入变体。** 表 10 对比了不同的在线误差注入策略，确认了论文提出的概率注入方案（$p=0.5$ 使用无误差输入）在保持生成能力与学习纠错之间取得了最佳平衡。

### 稳定性与长度扩展

图 5 展示了视频长度增长时的稳定性对比。Wan 2.1 和 FramePack 随着片段数增加，一致性和质量持续下降；SVI 则保持平稳，没有出现明显的退化趋势。图 6 提供了错误纠正效果的直接可视化对比，SVI 生成的片段在主体外观保持上显著优于基线。

### 超长生成与定性分析

图 8 展示了 10 分钟以上的超长生成结果，包括长提示流驱动和不同音频片段驱动的场景，视频展现出非循环、多样化的特性。图 9 可视化了一个关键能力：当人物脱出当前场景后重新进入下一片段时，发型、衣着等个人信息保持高度相似，体现了长距离身份一致性。

### 失败模式与局限性

尽管 SVI 在多数场景下表现优异，仍存在以下局限：

1. **色彩偏移**：当测试图像的风格与训练数据分布差异较大时，SVI 可能出现色彩偏移现象，这源于错误回收微调的数据依赖。
2. **复杂场景转换**：跨镜头的主体一致性在剧烈场景变化中仍有提升空间，特别是当主体经历大幅度姿态变化或遮挡时。
3. **域外泛化**：模型对于极端风格或训练分布外内容的泛化能力有限，需要扩大训练数据规模和多样性来改善。

## 定位与知识库关联

### 问题根源：训练-测试假设差距

Stable Video Infinity (SVI) 的核心贡献在于识别并弥合了一个被先前工作系统性忽视的根本瓶颈：**训练时的无误差假设与测试时自回归使用误差污染输入之间的假设差距**。现有视频生成 DiT 在流匹配训练中假设历史轨迹和中间状态完全无误差（见 Eq. 1），然而在长视频自回归生成中，前一片段的预测误差会通过 ODE 积分步骤（Eq. 2）累积并污染后续片段的输入。这种累积产生两类相互增强的误差：**预测误差**（模型回归性质导致轨迹终点偏离）和**条件误差**（误差污染图像作为条件输入导致轨迹起点偏移），二者形成恶性循环，使视频一致性、美学质量和成像质量迅速退化（Figure 2）。

### 方法定位：错误回收微调的闭环范式

SVI 提出的 **Error-Recycling Fine-Tuning (ERFT)** 在方法谱系中占据独特位置。与现有长视频生成方法相比：

- **StreamingT2V** 和 **HistoryGuidance** 等方法试图在推理时通过噪声重调度或历史指导来缓解误差累积，但未触及训练阶段的无误差假设，属于“推理端修补”范式。
- **FramePack** 等帧打包方法通过改变输入结构来延长视频，但同样未解决模型对误差输入的脆弱性。
- **Wan 2.1** 等通用图像到视频 DiT 模型是强基线，但在长视频场景中直接自回归使用时，一致性随长度急剧下降（Table 1 中超长一致视频生成中主体一致性从 80.00% 降至约 73%）。

SVI 的 ERFT 开创了**“训练端闭环回收”范式**：在训练过程中主动注入模型自生成的误差，计算误差信号，存储于回放记忆，再选择性注入到干净输入中，迫使 DiT 学习识别并纠正自身错误。该范式的核心洞察是：**将模型自生成的误差作为监督信号进行闭环回收**，在不增加推理成本的前提下实现稳定、非循环的无限长度视频生成。

### 与图像恢复 DiT 的本质区别

SVI 与图像恢复 DiT 存在根本性差异（Figure 1）：恢复 DiT 假设输入始终包含误差并学习去除噪声，而视频生成 DiT 在训练中假设输入无误差，仅在测试时遭遇误差污染。SVI 通过 ERFT 打破了这一假设，使生成 DiT 在保持生成能力的同时获得误差纠正能力，弥合了生成与恢复之间的鸿沟。

### 适用边界与领域泛化

SVI 的适用边界已通过多领域验证得到初步界定：

1. **通用视频生成**：在一致视频、创意视频和超长一致视频三种设置下，SVI-Shot 在主体一致性、背景一致性、美学质量和成像质量等核心指标上全面超越基线（Table 1）。特别是在超长一致视频生成中，主体一致性达到 97.50%，对比最强基线 FramePack（79.37%）提升 18.13 个百分点。

2. **音频驱动长对话**：SVI-Talk 通过引入音频控制信号（$C_{\text{vis}}$ 和 $C_{\text{emb}}$），在 Sync-C 指标上达到 6.12，远超 Wan 2.1 的 0.21（Table 2），证明 ERFT 可有效泛化至多模态条件生成。

3. **骨骼驱动长舞蹈**：SVI-Dance 在 PSNR 指标上达到 20.01，超越专用方法 UniAnimate-DiT 的 18.97（Table 3），表明 ERFT 可适配结构化控制信号。

4. **超长生成（10+ 分钟）**：SVI 展示了非循环、多样化的超长视频生成能力（Figure 8），支持长文本流和不同音频片段的连续驱动。

### 局限性与开放问题

**已确认的局限性：**

1. **色彩偏移**：当测试图像的风格与训练数据分布差异较大时，SVI 可能出现色彩偏移现象。这源于 ERFT 训练数据的分布覆盖范围有限，模型对域外风格的误差纠正能力不足。

2. **跨镜头一致性**：在复杂场景转换中，跨镜头的主体一致性仍有提升空间。尽管 SVI 在长距离身份保持上展示了令人瞩目的能力（Figure 9，人物脱出场景后重新进入仍保持相似外貌），但在极端场景变化下的一致性尚未完全解决。

3. **域外泛化**：模型仍依赖于特定训练数据规模，对于极端风格或域外内容泛化有限。消融实验（Table 6）表明，人工图像增强（颜色偏移、模糊、锐化）无法替代模型自生成误差，甚至与自生成误差结合时引起冲突，这暗示模型误差具有独特的分布特征，也限制了通过简单数据增强扩展泛化能力的路径。

**待解决的开放问题：**

1. **端到端拍摄流水线**：如何构建集成持久身份嵌入、跨镜头特征缓存和场景感知锚点的端到端系统，以进一步强化超长视频中的身份一致性？当前 SVI 主要依赖参考图像误差（$E_{\text{img}}$）进行跨片段条件纠正（Table 4 消融实验证明该误差项是决定性的驱动因素），但更结构化的身份保持机制仍有探索空间。

2. **训练数据规模与多样性**：如何扩大训练数据规模和多样性，以纠正色彩偏移并提升域外泛化能力？当前 SVI 采用 LoRA 微调（秩 64 以上即可提供足够纠错能力，Table 9），参数高效的特性为大规模数据训练提供了可行性，但数据策展策略仍需进一步研究。

3. **评价指标的可靠性**：天真的视频扩展方法（复制片段、乒乓回放）可以愚弄一致性指标（Table 5，一致性高但动态性降为 0%），这提示当前评价体系存在盲区。SVI 在一致性、质量、动态性等多个维度取得了平衡，但更鲁棒的评估方法仍是领域共同面临的挑战。

## 原文 PDF

![[paperPDFs/ICLR_2026/Stable_Video_Infinity_Infinite_Length_Video_Generation_with_Error_Recycling.pdf]]
