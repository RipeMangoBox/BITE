---
title: Bi-directional Autoregressive Diffusion for Large Complex Motion Interpolation
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/Bi_directional_Autoregressive_Diffusion_for_Large_Complex_Motion_Interpolation.pdf
project_link: null
code_link: null
aliases:
- BDADLCMI
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/generative_models_diffusion
- topic/benchmarks_datasets_evaluation
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: 双向自回归插帧策略（从输入帧向中间逐步生成）和 DINOv3 特征作为鲁棒运动表示。
primary_logic: 通过双向自回归扩散逐步预测中间帧，降低误差累积；利用 DINOv3 语义特征建模鲁棒运动，并在其引导下条件生成最终帧，从而在大复杂运动下实现一致且高质量的视频插帧。
claims:
- 双向自回归插帧相比全序列生成能显著降低远离输入帧的 FID 误差。
- DINOv3 特征在复杂运动下的匹配比光流和稀疏匹配更鲁棒。
- ARVFI 在所有数据集和指标上显著优于现有方法（LPIPS、FID、FVD）。
- 双向自回归插帧和 DINOv3 运动表示在消融实验中均带来持续提升。
---

# Bi-directional Autoregressive Diffusion for Large Complex Motion Interpolation

> [!tip] 核心洞察
> 通过双向自回归扩散逐步预测中间帧，降低误差累积；利用 DINOv3 语义特征建模鲁棒运动，并在其引导下条件生成最终帧，从而在大复杂运动下实现一致且高质量的视频插帧。

| 字段 | 内容 |
|------|------|
| 中文题名 | 面向大复杂运动的双向自回归扩散视频插帧 |
| 英文题名 | Bi-directional Autoregressive Diffusion for Large Complex Motion Interpolation |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://openaccess.thecvf.com/content/CVPR2026/html/Ma_Bi-directional_Autoregressive_Diffusion_for_Large_Complex_Motion_Interpolation_CVPR_2026_paper.html) |
| Topic | #topic/vision_multimodal_applications #topic/generative_models_diffusion #topic/benchmarks_datasets_evaluation #topic/vision_multimodal_applications/image_and_video_generation |
| Method | ARVFI |
| Dataset | DAVIS-7, Eval set, Pixels, Human Evaluation |

> [!tip] 效果简介
> - DAVIS-7 上，LPIPS 0.257；FID 21.65；FVD 188.77。
> - Eval set 上，LPIPS 0.206；FID 19.03；FVD 201.47。
> - Pixels 上，LPIPS 0.247。

## 概要

### 问题背景与核心瓶颈

视频插帧（VFI）旨在从两个输入帧之间生成连贯的中间帧序列。当场景包含大范围、复杂运动时，现有扩散插帧方法面临两个关键瓶颈：

1. **全序列生成导致误差累积**：当前主流方法（如 **Wan**，Wang et al., arXiv 2025）同时生成所有中间帧，缺乏时序因果约束，导致远离输入帧的中间帧累积误差显著增大（Figure 1）。
2. **像素级运动表示不可靠**：光流和稀疏匹配等传统运动表示在复杂运动下易出现颜色突变、流场不准确等问题，无法为生成过程提供鲁棒的运动引导（Figure 2）。

### 核心方法：ARVFI

ARVFI（Bi-directional Autoregressive Diffusion for VFI）提出了两个核心创新来解决上述瓶颈：

- **双向自回归插帧策略**：从两个输入帧向中间逐步生成，而非一次性生成所有中间帧。通过逐帧递增的噪声水平作为软掩膜，配合双向因果注意力掩膜防止跨方向噪声泄漏，实现“软”自回归生成，显著降低误差累积。
- **DINOv3 运动表示**：利用 DINOv3 特征作为鲁棒的运动表示，替代传统光流或稀疏匹配。DINOv3 特征在复杂运动下具有更强的语义匹配能力，并通过运动引导注意力机制注入帧生成过程。

ARVFI 采用两阶段架构：第一阶段自回归生成中间 DINOv3 运动特征，第二阶段在运动特征引导下自回归生成中间帧。

### 方法谱系与知识库定位

ARVFI 处于**扩散模型视频插帧**与**自回归生成**的交叉点。其方法定位如下：

| 维度 | 基线方法 | ARVFI 的差异化设计 |
|------|---------|-------------------|
| 插帧顺序 | 全序列同时生成（**LDMVFI**, Danier et al., AAAI 2024；**Wan**, Wang et al., arXiv 2025） | 双向自回归逐步生成 |
| 运动表示 | 光流（**FILM**, Reda et al., ECCV 2022）、稀疏匹配（**GI**, Wang et al., 2024） | DINOv3 语义特征 |
| 生成模块 | 统一模型同时生成运动与帧（**GIMM-VFI**, Guo et al., NeurIPS 2024） | 两个独立扩散 Transformer 分阶段生成 |
| 时间步调度 | 所有帧共享统一扩散时间步 | 逐帧递增噪声的软自回归调度 |
| 注意力机制 | 标准 DiT 注意力（仅帧特征） | 运动引导注意力（拼接 DINOv3 生成的 K、Q） |

### 主要实验结果

在 DAVIS-7、FCVG 数据集及 Pixels 等评测基准上，ARVFI 在所有指标上一致优于现有方法：

- **DAVIS-7**：LPIPS 0.257，FID 21.65，FVD 188.77
- **FCVG 评测集**：LPIPS 0.206，FID 19.03，FVD 201.47
- **Pixels**：LPIPS 0.247，FID 17.60，FVD 101.71

消融实验（Table 2）证实，双向自回归插帧策略和 DINOv3 运动表示各自带来持续的性能提升。推理效率方面，ARVFI 在 576×1024 分辨率下 →25 插帧仅需每帧 0.78s，仅为骨干模型 Wan 的 30%（Table 3）。用户主观评测中，超过 85% 的观察者将 ARVFI 评为最佳方法。

### 局限性

ARVFI 无法正确处理具有物理场景交互的运动，例如球落地弹跳、周期性摆动的摆锤等，表明该方法缺乏对物理先验的建模能力。



视频插帧（Video Frame Interpolation, VFI）旨在从两帧或多帧输入中生成时间上连续的中间帧，是视频增强与生成领域的核心任务之一。近年来，扩散模型在图像和视频生成中展现出强大的能力，促使研究者将其引入视频插帧任务。然而，现有的扩散插帧方法在面临**大复杂运动**（如大幅度肢体动作、快速物体位移、遮挡与形变）时，仍存在根本性瓶颈。

### 现有方法的缺口

当前主流的扩散插帧方法（如 **LDMVFI** (Danier et al., AAAI 2024)、**Wan** (Wang et al., arXiv 2025)）采用**全序列同时生成**策略，即一次性对所有中间帧进行去噪生成。这一范式带来两个深层问题：

1. **累积误差放大**：由于所有中间帧同时生成，远离输入帧的帧缺乏足够的时序上下文约束，导致生成误差随距离增加而累积。如 **Figure 1** 左下角的 FID 误差曲线所示，全序列生成方法中，越靠近序列中心的帧，其 FID 误差越高，形成“中间塌陷”效应。

2. **运动表示脆弱**：现有方法普遍依赖像素级重建损失或光流作为运动监督信号。然而，在大复杂运动场景下，光流估计本身容易失效——如 **Figure 2** 所示，光流在背景区域出现不稳定颜色突变，对小运动（如手部）的表征能力有限；稀疏匹配结果则过于稀疏，无法提供稠密的运动引导。像素级损失仅关注逐像素对齐，缺乏对运动语义的理解，导致生成帧出现**时间不一致**和**结构破坏**（如物体断裂、肢体变形）。

这些缺口使得现有方法在处理真实世界中常见的大复杂运动视频时，难以同时保证插帧的**视觉质量**、**时序一致性**和**结构完整性**。

### 本文动机

针对上述瓶颈，本文提出 **ARVFI（Bi-directional Autoregressive Diffusion for Video Frame Interpolation）**，核心动机在于两个关键洞察：

- **双向自回归插帧**：与全序列同时生成不同，ARVFI 采用从输入帧向中间逐步生成的策略。通过双向自回归方式，先预测靠近输入帧的帧，再基于已预测帧逐步向中间推进。这一策略使每一帧的生成都能利用已完成的邻近帧作为可靠上下文，从而有效抑制误差累积。

- **鲁棒运动表示**：ARVFI 引入 **DINOv3 特征**作为运动表示。DINOv3 是自监督视觉 Transformer 提取的稠密语义特征，其在复杂运动下的跨帧匹配比光流和稀疏匹配更鲁棒（**Figure 2** 展示了 DINOv3 相似度在运动区域的高判别力）。通过将 DINOv3 特征作为运动先验，ARVFI 能够在语义层面理解运动模式，而非仅依赖像素级信号。

综上，ARVFI 通过“双向自回归扩散 + DINOv3 语义运动引导”的双重设计，旨在在大复杂运动场景下实现**一致、连贯且高质量**的视频插帧。



## 核心方法与创新机理

ARVFI 的核心创新可归结为两个相互协同的“因果旋钮”：**双向自回归插帧策略**与**基于 DINOv3 的鲁棒运动表示**。二者分别从生成顺序和运动建模两个维度，系统性地解决了现有扩散插帧方法在“大复杂运动”场景下的瓶颈。

### 1. 瓶颈溯源：全序列生成与像素级监督的失效

现有扩散插帧方法（如 **Wan** (Wang et al., arXiv 2025)、**LDMVFI** (Danier et al., AAAI 2024)）采用**全序列生成**策略，即同时去噪所有中间帧（Figure 1 底部对比）。这一范式导致两个连锁问题：
- **误差累积**：远离输入帧的中间帧因缺乏逐步引导，FID 误差随距离单调递增（Figure 1 左下 FID error plot）。
- **运动坍塌**：像素级重建损失（如光流监督）在复杂运动下无法捕捉高层语义对应，导致时间不一致与结构破坏（Figure 2 中光流与稀疏匹配的失效案例）。

### 2. 关键创新一：双向自回归插帧（Bidirectional Autoregressive Interpolation）

ARVFI 将生成顺序从“全序列同步生成”改为**从输入帧向中间逐步生成**（changed slot: 插帧顺序）。具体而言：
- 前向自回归从第一帧向中间推进，反向自回归从最后一帧向中间推进，二者在时间中心汇合。
- 通过**逐帧递增的噪声水平**作为软掩膜（soft mask），实现“软自回归”生成——当前帧的噪声水平高于已生成的邻近帧，使模型在去噪时能同时关注已生成帧的干净信号与当前帧的噪声先验（Sec. 3.3, Algorithm 1）。
- 配合**双向因果注意力掩膜**，阻止前向与反向路径间的噪声泄漏，确保两条生成路径的独立性。

这一设计直接作用于误差累积瓶颈：消融实验（Table 2）表明，将“Frame Full-Seq”替换为“Frame Bi-AR”后，FVD 和 LPIPS 均获得显著改善。

### 3. 关键创新二：DINOv3 特征作为鲁棒运动表示

ARVFI 用 **DINOv3 语义特征**替代传统的光流或稀疏匹配作为运动表示（changed slot: 运动表示）。Figure 2 提供了决定性证据：在复杂运动（如鞋子快速移动、手部微小动作）下，光流出现颜色突变与匹配错误，而 DINOv3 特征在目标区域保持最高相似度。

这一表示被集成到两阶段生成流程中（Figure 3）：
- **第一阶段**：Intermediate Motion Estimator（$G_{\theta_d}$）自回归生成中间帧的 DINOv3 特征，训练时受相似度损失 $\mathcal{L}_{sim}$ 约束（Eq. 3），强制生成特征与输入帧特征的 patch 相似度对齐。
- **第二阶段**：Frame Generator（$G_{\theta_f}$）在运动引导下生成最终帧。引导机制通过**运动引导注意力**（Motion-Guided Attention，Figure 4）实现——将 DINOv3 特征经 MLP 生成的 Key $K_d$ 和 Query $Q_d$ 拼接到 DiT 注意力块的原始 $K_f$、$Q_f$ 中，使帧生成过程显式感知运动语义。

### 4. 两阶段分离设计的必要性

ARVFI 将运动估计与帧生成拆分为**两个独立的扩散 Transformer**（changed slot: 运动与帧生成模块关系），而非像统一模型那样同时输出光流可视化与帧。消融实验（Table 2, Figure 7）证实：分离设计（Ours）相比联合建模（Uni-DINOv3）能进一步提升插帧质量，因为两个子任务的目标函数与难度差异较大，分离训练避免了梯度冲突。

### 5. 创新协同效应

上述创新并非孤立生效。双向自回归策略降低了误差累积，使 DINOv3 运动特征在远离输入帧的位置仍能保持可靠引导；而鲁棒的运动表示又为自回归生成提供了高质量的条件信号。二者叠加使 ARVFI 在 DAVIS-7、FCVG eval set、Pixels 三个基准上全面超越 **FILM**、**GIMM-VFI**、**GI**、**FCVG** 和 **Wan** 等现有方法（Table 1），同时推理效率提升至 Wan 的 3 倍（Table 3，单帧 0.78s @ 1024×576 →25 插帧）。

### 6. 局限与待验证点

- **物理交互场景失效**：ARVFI 无法正确处理涉及物理场景交互的运动（如球落地弹跳、摆锤周期性摆动），这表明纯数据驱动的运动表示缺乏物理先验。
- **极端条件未验证**：实验聚焦于大复杂运动场景，在低纹理、极端光照等条件下的鲁棒性需手动验证。



ARVFI 将复杂运动下的视频插帧分解为两个阶段：**运动表示插值**与**条件帧生成**，两者均以**双向自回归**方式执行，从两帧输入逐步向时间中心生成。

### 核心洞察与设计动机

现有扩散插帧方法（如 **Wan**，Wang et al., arXiv 2025）同时生成所有中间帧，导致远离输入帧的位置累积误差持续增大（Figure 1 底部左侧 FID 误差曲线）。同时，像素级重建损失无法有效监督复杂运动，造成时间不一致与结构破坏。ARVFI 通过两条因果路径解决该瓶颈：

![[assets/figures/papers/paper_list_l985_https_openaccess_thecvf_com_content_CVPR2026_html_Ma_Bi_directional_Auto/figures/001_Figure_1.jpg]]
*Figure 1: The proposed ARVFI interpolates a sequence frame (ω2) based on previous predictions (ω1, ω3), while the current full-sequence interpolation method, such as Wan [33], generates all intermediate frames simultaneously. This bidirectional autoregressive interpolation scheme mitigates increasing FID errors as frames move away from the input frames and generates more continuous and consistent results, as shown in the bottom left figure. Additionally, because a frame is predicted based on all previous interpolation results, the diffusion network can interpolate with fewer diffusion sampling steps and superior efficiency. Our ARVFI accelerates Wan [33] by 3→ with higher interpolation accuracy (FID...*

1. **双向自回归插帧策略**：从输入帧向中间逐步生成，利用已预测帧的信息降低后续帧的误差累积。
2. **DINOv3 语义运动表示**：替代光流或稀疏匹配，提供对复杂运动更鲁棒的稠密特征，并在其引导下条件生成最终帧。

### 两阶段 Pipeline

ARVFI 包含两个独立的扩散 Transformer，分阶段执行：

| 阶段 | 模块 | 功能 |
|------|------|------|
| 第一阶段 | **Intermediate Motion Estimator**（$G_{\theta_d}$） | 自回归生成中间帧的 DINOv3 运动特征 |
| 第二阶段 | **Frame Generator**（$G_{\theta_f}$） | 在运动特征引导下自回归生成中间帧 |

**输入**：两帧输入图像经 VAE 编码后的 latent 及其 DINOv3 特征。  
**输出**：$N-1$ 帧中间帧的 latent，经 VAE 解码得到最终视频帧。

### 双向自回归调度机制

ARVFI 采用“软”自回归生成方案（Algorithm 1），核心机制包括：

- **逐帧递增噪声作为软掩膜**：通过调度矩阵 $S \in \mathbb{R}^{K \times (N-1)}$（运动估计）和 $S' \in \mathbb{R}^{K' \times (N-1)}$（帧生成）控制每帧的噪声水平。靠近输入帧的中间帧噪声低（更清晰），远离输入帧的中间帧噪声高（更模糊），形成从输入到中心的渐进生成。
- **双向因果注意力掩膜**：防止来自相反方向（前向/后向）的噪声泄漏，确保两个方向的自回归过程相互独立且一致。
- **训练时随机采样时间步与间隔**：模拟推理时的自回归行为，使模型学会在不同噪声水平下利用已生成帧的信息。

### 运动引导注意力

第二阶段帧生成器通过 **Motion-Guided Attention** 将第一阶段估计的 DINOv3 特征注入 DiT 注意力块（Figure 4）：

- 从估计的 DINOv3 特征经 MLP 和归一化生成注意力键 $K_d$ 和查询 $Q_d$。
- 将 $K_d$、$Q_d$ 与原始帧特征的 $K_f$、$Q_f$ 沿序列维度拼接，使帧生成过程显式感知运动语义。
- DINOv3 特征在训练时以最小扩散时间步（无噪声）拼接至输入噪声，保持其语义完整性。

### 与基线方法的关键差异

| 设计维度 | 现有方法（如 Wan） | ARVFI |
|----------|-------------------|-------|
| 插帧顺序 | 同时生成所有中间帧 | 双向自回归逐步生成 |
| 运动表示 | 像素重建损失 / 光流 | DINOv3 语义特征 + 相似度损失 |
| 生成模块信息注入 | 标准 DiT 注意力（仅帧特征） | 运动引导注意力（拼接 DINOv3 的 K、Q） |
| 时间步调度 | 所有帧共享统一扩散时间步 | 逐帧递增噪声作为软掩膜 |
| 运动与帧生成关系 | 统一模型同时生成 | 两个独立扩散 Transformer 分阶段生成 |

该设计使 ARVFI 在推理时仅需 0.78 秒/帧（1024×576，→25 插帧），约为骨干模型 Wan 的 30%，同时在所有基准上取得更优的 LPIPS、FID 和 FVD 指标（Table 1）。

### 补充图表

![[assets/figures/papers/paper_list_l985_https_openaccess_thecvf_com_content_CVPR2026_html_Ma_Bi_directional_Auto/figures/003_Figure_3.jpg]]
*Figure 3: The proposed ARVFI consists of two main stages: motion representations interpolation and the conditional intermediate frame generation. ARVFI interpolates in a bi-directional autoregressive manner. To implement it, the ARVFI gradually denoises from input frames to the middle ones, coupling with a bi-directional causal attention mask to ensure each interpolation is only based on previous interpolation (see red arrows) rather than unprocessed noise. By this means, ARVFI interpolates the intermediate DINOv3 features as motion representations first, and then conditionally generates intermediate frames*



### 3.1 扩散基础与训练目标

ARVFI 构建在视频扩散模型之上，采用 v-预测范式训练去噪网络。给定潜在变量 $z$ 和条件 $c$，训练损失为：

$$\mathcal{L}_{\theta} = \mathbb{E}_{t\sim U(1,T), \epsilon\sim\mathcal{N}(0,I)} \|G_{\theta}(z^t; t, c) - v^t\|$$

其中 $v^t$ 为速度预测目标，$G_{\theta}$ 为去噪网络。采样阶段通过迭代去噪逐步生成干净潜在变量：

$$z^{t-1} = \mathcal{B}ackward(z^t, G_{\theta}(z^t; t, c); t)$$

这一基础公式同时应用于运动估计和帧生成两个阶段。

### 3.2 两阶段分离架构

ARVFI 的核心架构由两个独立的扩散 Transformer 组成（Figure 3），将运动建模与帧生成解耦：

**第一阶段：中间运动估计器（$G_{\theta_d}$）**
负责自回归生成中间帧的 DINOv3 运动特征。选择 DINOv3 而非传统光流或稀疏匹配的核心原因在于：光流在复杂运动下存在颜色突变、对小运动表征能力不足等问题；稀疏匹配则受限于关键点覆盖密度。DINOv3 特征通过高层语义相似度提供鲁棒的运动对应关系（Figure 2），其相似度损失约束生成特征与输入帧特征的 patch 对齐：

![[assets/figures/papers/paper_list_l985_https_openaccess_thecvf_com_content_CVPR2026_html_Ma_Bi_directional_Auto/figures/002_Figure_2.jpg]]
*Figure 2: Current flow-based motion representations [3] suffer from unstable color mutations (background and the marked shoe), inaccurate flows, and limited representation ability for small motions (hands). As another popular choice [34], sparse matching results [24, 38] usually degrade to complex motions that contain occlusions and object deformation. In contrast, DINOv3 features [32] robustly yield the highest similarities to the highlighted shoe in the intermediate DINOv3 features, because these features contain both high-level semantics and low-level structures*

$$\mathcal{L}_{sim} = \|d_0\cdot d - d_0\cdot\hat{d}\|_2 + \|d_1\cdot d - d_1\cdot\hat{d}\|_2$$

其中 $d_0$、$d_1$ 为两个输入帧的 DINOv3 特征，$d$ 为真实中间特征，$\hat{d}$ 为生成特征。该损失确保生成的运动表示在语义层面与输入帧保持运动一致性。

**第二阶段：帧生成器（$G_{\theta_f}$）**
以第一阶段估计的运动特征为条件，自回归生成中间帧。两个阶段共享双向自回归调度策略，但使用独立的扩散 Transformer 和噪声调度矩阵。

### 3.3 双向自回归调度机制

区别于现有方法同时生成所有中间帧，ARVFI 采用从输入帧向中间逐步生成的策略。其关键创新在于“软自回归”实现：通过为不同时间位置的帧分配递增的扩散噪声水平，形成软掩膜效果。

运动估计阶段的调度矩阵 $S\in\mathbb{R}^{K\times(N-1)}$ 控制 $K$ 步自回归过程中 $N-1$ 个中间帧的噪声水平；帧生成阶段使用独立的调度矩阵 $S'\in\mathbb{R}^{K'\times(N-1)}$。越靠近输入帧的位置噪声越低（更接近干净潜在变量），越远离输入帧的位置噪声越高（更接近纯噪声），从而自然地实现了从已知到未知的渐进生成顺序。

同时，双向因果注意力掩膜防止来自相反方向的噪声泄漏，确保两个方向的自回归过程独立且一致地向中间汇聚。

### 3.4 运动引导注意力

帧生成器并非简单地将 DINOv3 特征作为条件拼接，而是通过运动引导注意力机制将其深度注入 DiT 的注意力计算中（Figure 4）。

![[assets/figures/papers/paper_list_l985_https_openaccess_thecvf_com_content_CVPR2026_html_Ma_Bi_directional_Auto/figures/004_Figure_4.jpg]]
*Figure 4: We generate attention keys*

具体而言，从估计的 DINOv3 特征通过 MLP 层和归一化生成额外的注意力键 $K_d$ 和查询 $Q_d$，将其与原始帧特征的键 $K_f$ 和查询 $Q_f$ 沿序列维度拼接：

- 键拼接：$K = [K_f; K_d]$
- 查询拼接：$Q = [Q_f; Q_d]$
- 值保持原始帧特征：$V = V_f$

这种设计使得帧生成过程中的每个 token 能够同时关注帧内信息和运动对应信息，从而在保持视觉质量的同时确保运动一致性。该模块是连接两个阶段的关键桥梁，将第一阶段估计的抽象运动表示转化为对像素生成的直接约束。



## 实验与关键发现

### 核心性能对比

ARVFI 在三个涵盖大复杂运动的基准数据集上全面超越现有方法。Table 1 汇总了在 DAVIS-7、FCVG 评估集 和 Pixels 三个数据集上的 LPIPS、FID、FVD 指标对比结果。ARVFI 在所有三个数据集的所有指标上均取得最佳成绩。具体而言：

![[assets/figures/papers/paper_list_l985_https_openaccess_thecvf_com_content_CVPR2026_html_Ma_Bi_directional_Auto/figures/007_Table_1.jpg]]
*Table 1: Numeric comparison results. The best and the second-best results are highlighted by bold and underline. The proposed ARVFI consistently outperforms existing methods across all metrics*

- **DAVIS-7**：LPIPS 0.257，FID 21.65，FVD 188.77；
- **FCVG 评估集 **：LPIPS 0.206，FID 19.03，FVD 201.47；
- **Pixels**：LPIPS 0.247，FID 17.60，FVD 101.71。

值得注意的是，论文仅展示了 ARVFI 的完整数值，基线方法的具体数值未在 Table 1 中给出，仅标注了最佳和次佳结果的格式高亮。因此，各基线的精确数值需要读者自行查阅原文或联系作者获取。

定性对比（Figure 5）进一步揭示了 ARVFI 的优势来源。与 **FILM**（Reda et al., ECCV 2022）、**GIMM-VFI**（Guo et al., NeurIPS 2024）、**GI**（Wang et al., 2024）、**FCVG**（Zhu et al., arXiv 2024）和 **Wan**（Wang et al., arXiv 2025）相比，ARVFI 生成的运动更加连续且一致，而非逐像素的近似重建。在自行车场景中，ARVFI 减少了物体断裂现象；在人物腿部运动场景中，ARVFI 避免了物体形变。这些改进直接归因于双向自回归插帧策略和 DINOv3 运动表示。

![[assets/figures/papers/paper_list_l985_https_openaccess_thecvf_com_content_CVPR2026_html_Ma_Bi_directional_Auto/figures/006_Figure_5.jpg]]
*Figure 5: Visual comparisons with state-of-the-art methods: FILM [27], GIMM-VFI [9], GI [34], FCVG [42], and Wan [33]. The results clearly show the effectiveness of the proposed bidirectional autoregressive interpolation scheme and DINOv3 motion representations. Our ARVFI can generate continuous and consistent motions rather than pixel-wise approximation (see red boxes). Thus, ARVFI interpolates with fewer object fractions (see bike) and object deformations (leg in the bottom row)*

### 人类偏好评估

在用户研究中，超过 85% 的观察者将 ARVFI 评选为最佳运动质量的视频插帧方法，其余所有方法合计仅获得约 15% 的偏好率。这一结果与定量指标高度一致，表明 ARVFI 在感知运动质量上具有压倒性优势。

### 消融实验：双向自回归与运动表示

Table 2 在 FCVG 数据集 上系统消融了 ARVFI 的两个核心设计选择：插帧策略和运动表示。消融设置包括：

![[assets/figures/papers/paper_list_l985_https_openaccess_thecvf_com_content_CVPR2026_html_Ma_Bi_directional_Auto/figures/009_Table_2.jpg]]
*Table 2: Ablation study on FCVG dataset [42]. The proposed bidirectional autoregressive interpolation strategy and DINOv3 motion representations effectively advance interpolation quality for large, complex motions*

1. **Frame Full-Seq**：全序列同时生成所有中间帧，而非双向自回归；
2. **Frame Bi-AR**：仅启用双向自回归插帧，但仍使用统一的光流可视化作为运动表示；
3. **Uni-Flow Vis**：使用统一的扩散模型同时生成光流可视化和中间帧；
4. **Uni-DINOv3**：将光流可视化替换为 DINOv3 特征，但仍使用统一模型。

从 Frame Full-Seq 切换到 Frame Bi-AR，FVD 和 LPIPS 均显著下降，验证了双向自回归策略在降低远离输入帧的累积误差方面的关键作用。从 Uni-Flow Vis 到 Uni-DINOv3，插帧质量进一步提升，证实 DINOv3 特征作为运动表示优于传统光流可视化。

最终，ARVFI（分离的运动估计器 $G_{\theta_d}$ 和帧生成器 $G_{\theta_f}$）在所有消融变体中取得最佳结果。Figure 7 的定性对比显示，统一模型（Uni-DINOv3）在处理手部和腿部等细节区域时仍存在不一致性，而 ARVFI 的两阶段分离设计能够生成更高质量的视觉效果。

![[assets/figures/papers/paper_list_l985_https_openaccess_thecvf_com_content_CVPR2026_html_Ma_Bi_directional_Auto/figures/011_Figure_7.jpg]]
*Figure 7: Visual comparisons for ablation studies. Settings #1 to #4 are for “Frame Full-Seq”, “Frame Bi-AR”, “Uni-Flow Vis”, and “Uni-DINOv3”, respectively. Results show that the autoregressive interpolation method improves interpolation consistency (see hands and the head in #1 and #2). The joint motion representations and frame generation biases the diffusion model to predict data across multiple distributions, degrading the generated frames. In contrast, our ARVFI estimates the motions and frames with separate diffusion transformers and leads to superior visual quality (see hands and the foot in #3, #4, and ours)*

### 推理效率

Table 3 展示了在 1024×576 分辨率下进行 ×25 插帧的推理耗时对比。ARVFI 的单帧推理时间仅为 0.78 秒，是骨干模型 Wan 的约 30%，相比第二快的 Wan 节省了约 70% 的时间。这一效率优势源于双向自回归策略允许使用更少的扩散采样步数即可生成高质量中间帧。

### 失败模式与局限性

ARVFI 并非在所有场景下都表现完美。论文明确指出，该方法无法正确处理涉及物理场景交互的物体运动，典型失败案例包括球落地后的弹跳运动、周期性摆动的摆锤等。这些场景中，物体的运动受物理定律支配，而 ARVFI 的 DINOv3 运动表示和自回归生成策略缺乏对物理先验的显式建模能力，导致插帧结果违反物理规律。

### 补充图表

![[assets/figures/papers/paper_list_l985_https_openaccess_thecvf_com_content_CVPR2026_html_Ma_Bi_directional_Auto/figures/008_Figure_6.jpg]]
*Figure 6: Interpolated sequence in [42] dataset. FCVG [42] interpolates based on linearly interpolated matching results across input frames; Wan [33] utilizes a more advanced backbone, the diffusion transformer, to interpolate intermediate frames directly. These methods cannot solve large complex motions, producing unnatural motions and object deformations (see red boxes). In contrast, our ARVFI can effectively and consistently deal with large complex motions, producing interpolation results with superior accuracy and visual quality*



## 定位与知识库关联

### 1. 方法谱系：从光流插帧到双向自回归扩散插帧

ARVFI 的提出建立在视频插帧（VFI）领域两条主线的交汇点上：**基于光流的插帧方法**与**基于扩散模型的生成式插帧方法**。

**光流派基线。** 以 **FILM**（Reda et al., ECCV 2022）为代表的传统方法依赖显式的光流估计与 warping 操作，在中等运动幅度下表现稳定，但面对大复杂运动时，光流估计本身变得不可靠——颜色突变、遮挡区域的错误匹配、微小运动的分辨能力不足（参见 Figure 2）。**GIMM-VFI**（Guo et al., NeurIPS 2024）尝试在光流框架内引入更强的运动建模，但仍受限于光流表示的表达能力上限。

**扩散模型派基线。** **LDMVFI**（Danier et al., AAAI 2024）率先将潜在扩散模型引入 VFI，但其核心策略是同时生成所有中间帧。**Wan**（Wang et al., arXiv 2025）作为 ARVFI 的骨干模型，采用了更先进的 Diffusion Transformer（DiT）架构，但同样沿用了“全序列同时生成”范式。**FCVG**（Zhu et al., arXiv 2024）和 **GI**（Wang et al., 2024）则分别尝试在扩散框架中引入匹配结果线性插值或稀疏匹配，试图弥补全序列生成带来的时序不一致问题。

**ARVFI 的关键突破在于识别并切断了上述两条线的共同瓶颈：生成顺序与运动表示。** 全序列同时生成导致远离输入帧的中间帧累积误差急剧增大（Figure 1 左下角 FID error plot 直接量化了这一效应），而像素级重建损失或光流无法为复杂运动提供鲁棒的监督信号。ARVFI 通过两个相互耦合的“槽位替换”从根本上改变了这一局面：

| 槽位 | 基线值（代表性方法） | ARVFI 方案 | 证据锚点 |
|------|---------------------|-----------|---------|
| 插帧顺序 | 同时生成所有中间帧（Wan, LDMVFI） | 双向自回归逐步生成（从输入帧向中间） | Sec. 3.3, Algorithm 1 |
| 运动表示 | 像素重建损失 / 光流（FILM, GIMM-VFI） | DINOv3 语义特征及其相似度损失 | Sec. 3.2, Eq. (3) |
| 生成模块的信息注入 | 标准 DiT 注意力（仅帧特征） | 运动引导注意力（拼接来自 DINOv3 的 K, Q） | Sec. 3.4, Figure 4 |
| 时间步调度 | 所有帧共享统一扩散时间步 | 逐帧递增噪声作为软掩膜，实现软自回归生成 | Sec. 3.3, Algorithm 1 |
| 运动与帧生成关系 | 统一模型同时生成光流/运动可视化与帧 | 两个独立的扩散 Transformer 分阶段生成运动特征和帧 | Sec. 3.2, Figure 3 |

### 2. 知识库定位：扩散模型、自回归生成与视觉特征的交汇

ARVFI 处于三个研究方向的交叉地带，其贡献可分别定位：

**（1）扩散模型中的自回归生成。** 将自回归范式引入扩散模型并非 ARVFI 首创（文中引用“soft autoregressive generation scheme using sequence noise as masks similar to ”），但 ARVFI 的关键创新在于**双向因果注意力掩膜**与**逐帧递增噪声调度矩阵**（$S \in \mathbb{R}^{K \times (N-1)}$ 和 $S' \in \mathbb{R}^{K' \times (N-1)}$）的组合设计。这确保了从两个输入帧向中间逐步生成时，两个方向的信息不会通过噪声通道相互泄漏，同时保持了生成的连贯性。

**（2）自监督视觉特征作为运动表示。** 使用 DINOv3 特征（ViT-S，将 16×16 patch 嵌入为 384 维向量）替代光流作为运动表示，是 ARVFI 在 VFI 领域的原创性贡献。DINOv3 的高层语义特征在复杂运动下展现出比光流和稀疏匹配更强的鲁棒性（Figure 2 的相似度对比提供了直接证据），其 patch 级相似度损失 $\mathcal{L}_{sim} = \|d_0 \cdot d - d_0 \cdot \hat{d}\|_2 + \|d_1 \cdot d - d_1 \cdot \hat{d}\|_2$ 约束了生成特征与输入特征的语义对齐。

**（3）两阶段生成架构。** ARVFI 将运动估计与帧生成解耦为两个独立的扩散 Transformer（Intermediate Motion Estimator $G_{\theta_d}$ 和 Frame Generator $G_{\theta_f}$），并通过运动引导注意力（将 DINOv3 特征经 MLP 生成的 $K_d$、$Q_d$ 与原始帧特征的 $K_f$、$Q_f$ 拼接）实现信息注入。消融实验（Table 2, Figure 7）表明，这种分离设计优于联合建模（Uni-DINOv3），验证了“先估计鲁棒运动，再条件生成帧”的两阶段策略的有效性。

### 3. 适用边界与局限

**适用场景。** ARVFI 的设计目标明确针对**大复杂运动**场景下的视频插帧，在 DAVIS-7、Pixels 以及 FCVG 评估集上均取得了显著优于现有方法的 LPIPS、FID、FVD 指标（Table 1）。其推理效率也构成实用优势：在 1024×576 分辨率下进行 ×25 插帧时，每帧仅需约 0.78 秒，是骨干模型 Wan 的 30%（Table 3）。

**已知局限。** 论文明确指出了一个重要失效模式：**ARVFI 无法正确处理具有物理场景交互的物体**，例如球落地后弹跳、周期性摆动的摆锤等。这类场景涉及动力学约束，而 ARVFI 的运动表示（DINOv3 语义特征）和生成策略（纯数据驱动的自回归扩散）缺乏对物理规律的显式建模。

**未验证边界。** 以下场景需要谨慎对待，文中未提供独立验证：
- 低纹理或极端光照条件下的运动估计鲁棒性（DINOv3 特征在这些条件下的表现未经测试）；
- 极长序列插帧（如 ×100 以上）时自回归误差累积的上限；
- 对训练分布外运动类型（如高速旋转、剧烈形变）的泛化能力。

### 4. 开放问题

论文提出的核心开放问题是：**如何结合物理先验（如动力学模型）或高层语义提示（如文本描述）来处理涉及物理交互场景的视频插帧？** 这一问题指向了 ARVFI 的根本局限——纯视觉运动表示无法捕捉物理约束。可能的延伸方向包括：

- 将物理模拟器或神经物理模型作为额外的条件信号注入运动估计阶段；
- 利用文本-视频对齐模型（如 Video-LMM）提供高层运动语义提示，辅助 DINOv3 特征在物理交互场景下的运动推理；
- 探索将 DINOv3 运动表示与显式几何约束（如深度、法线）融合，以增强对三维运动和遮挡的建模能力。

此外，ARVFI 的双向自回归策略为更广泛的视频生成任务提供了可迁移的范式——任何需要从两端向中间逐步生成时序内容的任务（如视频补全、视角插值）都可能受益于这一调度策略和软掩膜机制。



## 原文 PDF

![[paperPDFs/CVPR_2026/Bi_directional_Autoregressive_Diffusion_for_Large_Complex_Motion_Interpolation.pdf]]
