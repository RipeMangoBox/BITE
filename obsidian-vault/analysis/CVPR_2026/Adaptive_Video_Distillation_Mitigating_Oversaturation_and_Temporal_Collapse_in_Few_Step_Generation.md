---
title: "Adaptive Video Distillation: Mitigating Oversaturation and Temporal Collapse in Few-Step Generation"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/Adaptive_Video_Distillation_Mitigating_Oversaturation_and_Temporal_Collapse_in_Few_Step_Generation.pdf
project_link: null
code_link: "https://github.com/yuyangyou/Adaptive-Video-Distillation"
aliases:
- AVD
- AVDMOTCFSG
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/generative_models_diffusion
- topic/benchmarks_datasets_evaluation
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: 在蒸馏过程中引入自适应回归损失，利用真实视频数据动态修正教师模型造成的分布偏向，同时用时序方差正则化强制保持帧间运动幅度，以对抗过饱和和运动减少。
primary_logic: 通过指数移动平均缓存记录各去噪步的历史回归损失，并用Sigmoid函数生成自适应权重来调节回归损失的贡献，从而在稳定对齐真实分布的同时抑制偏差过大的样本；时序正则化损失以负对数方差的形式惩罚静态输出，促进运动多样性，并通过截断机制防止过度放大帧间变化。
claims:
- DMD蒸馏生成的视频出现严重的颜色过饱和和运动减少（见图1）。
- 引入自适应回归损失可以解决简单回归损失造成的物体融合伪影（图4）。
- 添加时序正则化后，运动动态得分从72.22提升至100.00（表2），完全恢复运动多样性。
- 用户研究显示，蒸馏后的学生模型在视觉质量和语义对齐上甚至优于教师模型（图7）。
---

# Adaptive Video Distillation: Mitigating Oversaturation and Temporal Collapse in Few-Step Generation

> [!tip] 核心洞察
> 通过指数移动平均缓存记录各去噪步的历史回归损失，并用Sigmoid函数生成自适应权重来调节回归损失的贡献，从而在稳定对齐真实分布的同时抑制偏差过大的样本；时序正则化损失以负对数方差的形式惩罚静态输出，促进运动多样性，并通过截断机制防止过度放大帧间变化。

| 字段 | 内容 |
|------|------|
| 中文题名 | 自适应视频蒸馏：缓解少步生成中的过饱和与时序坍塌 |
| 英文题名 | Adaptive Video Distillation: Mitigating Oversaturation and Temporal Collapse in Few-Step Generation |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2603.21864) · [Code](https://github.com/yuyangyou/Adaptive-Video-Distillation) |
| Topic | #topic/vision_multimodal_applications #topic/generative_models_diffusion #topic/benchmarks_datasets_evaluation #topic/vision_multimodal_applications/image_and_video_generation |
| Method | Adaptive Video Distillation |
| Dataset | VBench2, VBench1, User Study |

> [!tip] 效果简介
> - VBench2 上，Total Score 55.08 (1.3B) / 59.06 (14B) vs DMD* 53.63 (1.3B) / 56.87 (14B) (+1.45 (1.3B) / +2.19 (14B))。
> - VBench1 上，Total Score 81.35 (1.3B) / 82.57 (14B) vs DMD* 80.66 (1.3B) / 79.63 (14B) (+0.69 (1.3B) / +2.94 (14B))。
> - User Study 上，Human Preference Ours preferred over Teacher and all baselines vs Teacher Wan2.1 (N/A)。

## 概要

**核心问题**：视频扩散模型的分布匹配蒸馏（DMD）在迁移至视频生成时，会出现严重的颜色过饱和与运动模式坍塌（时序模式崩溃）。在自回归生成中，过饱和现象会逐帧累积，进一步恶化视频质量（见图1）。

**关键洞察**：过饱和的根源在于教师模型在去噪过程中过度强调细粒度细节，将学生生成器推向一个偏差较大、过饱和的次优分布（见图3）。同时，蒸馏过程缺乏对时序动态的显式约束，导致生成视频的运动幅度显著减少。

**方法定位**：本文提出**自适应视频蒸馏（Adaptive Video Distillation）**，在DMD框架基础上引入两个核心组件：
- **自适应回归损失**：利用真实视频数据提供直接监督，通过指数移动平均（EMA）缓存记录各去噪步的历史损失，并用Sigmoid函数生成自适应权重，动态调节回归损失的贡献——当当前样本偏差过大时自动降低其权重，从而在稳定对齐真实分布的同时抑制伪影（如物体融合，见图4）。
- **时序正则化损失**：以负对数方差的形式惩罚静态输出，强制保持帧间运动幅度，促进运动多样性，并通过截断机制防止过度放大帧间变化导致的内容幻像。

**主要结果**：
- 在VBench2和VBench1基准上，本方法在1.3B和14B参数规模下均超越DMD基线（VBench2 Total Score: 55.08 vs 53.63 @1.3B; 59.06 vs 56.87 @14B）。
- 消融实验证实：加入时序正则化后，运动动态得分从72.22恢复至100.00；加入自适应回归损失后，实例保存得分从88.88提升至92.39，接近教师模型水平（见表2）。
- 用户研究表明，蒸馏后的学生模型在视觉质量和语义对齐上甚至优于教师模型（见图7）。



视频扩散模型近年来在生成质量上取得了显著进展，但其推理过程通常需要数十甚至上百个去噪步骤，导致极高的计算开销和生成延迟。分布匹配蒸馏（Distribution Matching Distillation, **DMD**）作为一种高效的少步蒸馏范式，通过最小化学生生成分布与教师模型分布之间的KL散度，成功将图像扩散模型的推理步数压缩至4步以内。然而，当DMD被直接迁移到视频生成任务时，出现了两个严重且相互关联的退化现象。

**过饱和与分布偏向。** DMD蒸馏的视频呈现出明显的颜色过饱和（color oversaturation），表现为色彩过度鲜艳、偏离真实视觉分布。其根本原因在于：在给定去噪时间步，教师模型$s_{real}$对细粒度细节的过度强调会通过分布匹配梯度（Eq. 4）传递给学生模型，使其偏向一个过饱和的次优分布（见图3）。这一偏差在自回归生成中逐帧累积，严重降低视频的感知质量。

**时序模式坍塌。** 除空间域的色彩异常外，DMD蒸馏还导致运动模式的严重退化——生成视频中的运动幅度显著减小，甚至趋于静态。这种时序坍塌（temporal collapse）表现为帧间变化不足，丧失了教师模型原有的运动多样性和场景动态感。图1的定性对比清晰地展示了DMD和rCM等基线方法在色彩过饱和（左）和运动减少（右）两方面的退化。

**简单回归损失的副作用。** 一个直观的修复思路是引入真实视频数据的回归损失来纠正分布偏向。然而，朴素的回归监督会引入新的伪影：当教师分布与真实数据分布存在显著偏差时，固定的回归损失权重会迫使生成器产生物体融合（object fusion）等空间伪影（见图4第3行，t=2.5s处），这揭示了静态回归策略在处理分布偏移时的根本脆弱性。

**核心动机。** 上述分析表明，视频扩散蒸馏面临一个关键瓶颈：如何在纠正分布偏向的同时，避免因过度回归导致的伪影，并有效保持时序运动动态？现有蒸馏方法（DMD、LCM、PCM、DCM、rCM）均未同时解决过饱和与时序坍塌问题。本文的核心动机在于设计一种**自适应机制**——在训练过程中动态感知分布偏移程度并据此调节监督强度，同时引入显式的时序约束来对抗运动模式崩溃，从而实现稳定、高质量的少步视频生成。



## 核心方法与创新机理

本文提出的**自适应视频蒸馏（Adaptive Video Distillation）**方法，针对分布匹配蒸馏（DMD）在视频生成中暴露的**颜色过饱和**与**时序模式坍塌**两大瓶颈，引入了三个关键改进槽位（changed slots），构成一个协同的蒸馏训练框架。

### 1. 自适应回归损失：动态抑制分布偏差

DMD 仅依赖分布匹配损失 $\mathcal{L}_{\mathrm{KL}}$，缺乏对真实数据分布的直接监督。当教师模型对细粒度细节的过度强调（见图 3）将学生模型引向过饱和的次优分布时，简单的回归损失虽能提供真实数据锚定，却会引入物体融合伪影（见图 4，t=2.5s 处）。

本方法的核心创新在于**自适应权重机制**，使回归损失的贡献随样本偏差动态调节：

1. **EMA 损失缓存**：为每个去噪步 $t$ 维护一个指数移动平均缓存，记录历史回归损失值：
   $$\bar{\mathcal{L}}_{t,s} = \alpha \mathcal{L}_{t,s-1} + (1-\alpha) \mathcal{L}_s \quad \text{(Eq. 6)}$$

2. **Sigmoid 自适应权重**：根据当前损失 $\mathcal{L}_s$ 与历史均值 $\bar{\mathcal{L}}_{t,s-1}$ 的偏差，通过 Sigmoid 函数生成权重：
   $$\omega_{t,s} = 1 - \sigma(k \cdot (\mathcal{L}_s - \bar{\mathcal{L}}_{t,s-1})), \quad \sigma(x) = \frac{1}{1+e^{-x}} \quad \text{(Eq. 7)}$$

   当偏差过大时，$\omega_{t,s}$ 趋近于 0，抑制不可靠样本的梯度贡献；偏差较小时，$\omega_{t,s}$ 趋近于 1，允许回归损失有效对齐真实分布。

3. **因果机制**：该设计在稳定对齐真实分布的同时，自动过滤教师模型造成的极端分布偏移样本，从根源上缓解过饱和。

消融实验证实，加入自适应回归损失（AdaLoss）后，**Instance Preservation 得分从 88.88 大幅提升至 92.39**（Table 2），接近教师模型水平，同时消除了简单回归损失造成的物体融合伪影。

### 2. 时序正则化损失：强制保持运动多样性

DMD 蒸馏后的视频出现严重的运动减少，即**时序模式坍塌**——生成视频趋于静态，帧间变化微弱。本方法引入时序正则化损失，直接惩罚低时序方差的输出：
$$\mathcal{L}_{\mathrm{temp}} = -\log(\mathbb{E}_{x\sim p_\theta}[\mathrm{Var}(x)] + \epsilon) \quad \text{(Eq. 8)}$$

该损失以负对数方差的形式，强制学生模型在生成过程中保持足够的帧间变化幅度，从而促进运动多样性。关键设计细节包括：

- **截断机制**：未截断的时序损失会导致严重的帧跳跃和内容幻像伪影（见图 14）。通过设置截断阈值（如 0.6），在运动分数和实例保存之间取得最佳平衡（见图 12）。
- **因果机制**：该损失直接作用于学生模型从纯噪声生成的视频，不依赖真实视频的运动标签，通过梯度反向传播鼓励模型探索更大的帧间变化空间。

消融实验表明，加入时序正则化（TR）后，**Dynamic Degree 从 72.22 跃升至 100.00**（Table 2），完全恢复了运动多样性，甚至超越了教师模型的运动动态。

### 3. 推理帧率策略：高噪声步半帧率推理

在推理阶段，本方法观察到高噪声去噪步（前 2 步）中相邻帧的余弦相似度显著更高（见图 15），表明此时帧间信息冗余较大。基于此洞察，提出**高噪声步半帧率推理**策略：

- 高噪声步仅对一半帧进行去噪，降低计算开销；
- 低噪声步前通过 U-Net 插值模块恢复全帧率，保证最终输出的时序平滑性。

该策略在不牺牲生成质量的前提下，有效减少了推理计算量，属于蒸馏框架下的推理效率优化。

### 4. 最终训练损失

上述组件与 DMD 的分布匹配损失 $\mathcal{L}_{\mathrm{KL}}$ 组合为最终生成器损失：
$$\mathcal{L}_{G} = \mathcal{L}_{\mathrm{KL}} + \omega_{\mathrm{reg}} \omega_{t,s} \mathcal{L}_{\mathrm{reg}} + \omega_{\mathrm{temp}} \mathcal{L}_{\mathrm{temp}} \quad \text{(Eq. 9)}$$

其中 $\omega_{\mathrm{reg}}$ 和 $\omega_{\mathrm{temp}}$ 为固定超参数，$\omega_{t,s}$ 为自适应权重。三者协同作用：$\mathcal{L}_{\mathrm{KL}}$ 提供分布匹配基础，$\mathcal{L}_{\mathrm{reg}}$ 通过自适应权重缓解过饱和，$\mathcal{L}_{\mathrm{temp}}$ 强制保持运动多样性。

### 创新总结

| 改进槽位 | 基线（DMD） | 本方法 | 核心作用 |
|---------|-----------|--------|---------|
| 蒸馏损失函数 | 仅 $\mathcal{L}_{\mathrm{KL}}$ | 加入自适应回归损失 $\mathcal{L}_{\mathrm{reg}}$ 和时序正则化 $\mathcal{L}_{\mathrm{temp}}$ | 缓解过饱和 + 恢复运动 |
| 回归损失权重 | 固定权重或无 | EMA 缓存 + Sigmoid 自适应权重 $\omega_{t,s}$ | 动态抑制偏差样本 |
| 推理帧策略 | 全帧率推理 | 高噪声步半帧率 + U-Net 插值恢复 | 降低推理开销 |



Adaptive Video Distillation 的目标是将预训练的视频扩散教师模型压缩为少步学生生成器，同时解决蒸馏过程中出现的**颜色过饱和**与**时序模式坍塌**两大瓶颈。整体框架围绕一个核心洞察构建：教师模型的分布偏向会通过分布匹配蒸馏（DMD）传递给学生，导致生成视频的颜色偏差与运动衰减；通过引入真实视频数据的自适应监督和时序方差约束，可以有效纠正这一偏差。

### 训练流程

整体训练流程如图 2 所示，包含三条并行的数据流：

1. **真实视频回归支路**：从数据集中采样真实视频-文本对，对视频施加噪声扰动后由学生模型进行去噪重建，计算重建视频与真实视频之间的回归损失。该损失经**Loss Mean Cache**（EMA 缓存）自适应加权后，形成最终的自适应回归损失 $ \omega_{t,s} \mathcal{L}_{\mathrm{reg}} $。
2. **文本条件生成支路**：从数据集中采样文本条件，指导学生模型从纯噪声生成视频。去噪输出用于计算**时序正则化损失** $ \mathcal{L}_{\mathrm{temp}} $（Eq. 8）和**分布匹配损失** $ \mathcal{L}_{\mathrm{KL}} $（Eq. 4）。
3. **生成器更新**：学生生成器 $ G_{\phi} $ 通过组合损失 $ \mathcal{L}_{G} = \mathcal{L}_{\mathrm{KL}} + \omega_{\mathrm{reg}} \omega_{t,s} \mathcal{L}_{\mathrm{reg}} + \omega_{\mathrm{temp}} \mathcal{L}_{\mathrm{temp}} $ 进行梯度下降更新。DMD 中的伪造得分网络 $ s_{\mathrm{gen},\xi} $ 按 DMD2 的方式独立更新。

### 核心模块与因果机制

框架包含四个关键模块，分别针对过饱和与运动坍塌的因果链路：

| 模块 | 因果作用 | 关键机制 |
|------|----------|----------|
| **Adaptive Regression Loss** | 纠正教师分布偏向导致的过饱和 | 利用真实视频监督，通过 EMA 缓存记录各去噪步的历史损失均值，以 Sigmoid 函数生成自适应权重 $ \omega_{t,s} = 1 - \sigma(k \cdot (\mathcal{L}_s - \bar{\mathcal{L}}_{t,s-1})) $，对偏差过大的样本降低回归贡献 |
| **Temporal Regularization Loss** | 对抗运动模式坍塌 | 以负对数方差 $ \mathcal{L}_{\mathrm{temp}} = -\log(\mathbb{E}_{x\sim p_\theta}[\mathrm{Var}(x)] + \epsilon) $ 惩罚静态输出，促进帧间运动多样性，并通过截断机制防止过度放大帧间变化 |
| **Loss Mean Cache (EMA)** | 提供自适应权重的历史基准 | 指数移动平均 $ \bar{\mathcal{L}}_{t,s} = \alpha \mathcal{L}_{t,s-1} + (1-\alpha) \mathcal{L}_s $ 维护各去噪步的损失期望，使权重能感知当前样本相对于历史分布的偏差程度 |
| **Frame Interpolation Module** | 降低推理计算开销 | 在高噪声去噪步（前 2 步）采用半帧率推理，低噪声步前通过 U-Net 插值恢复全帧率，利用高噪声阶段帧间相似度较高的特性（见图 15）节省计算 |

### 过饱和的成因与自适应回归损失的应对

图 3 揭示了过饱和的因果机制：在给定去噪步，教师模型 $ s_{\mathrm{real}} $ 对细粒度细节的过度强调会偏向学生模型 $ s_{\mathrm{fake}} $ 的分布估计，使其收敛到过饱和的次优分布。简单的回归损失虽然能提供真实数据监督，但会引入物体融合伪影（图 4 Row 3），因为不加区分地强制对齐会放大教师-学生分布差异较大的样本的负面影响。

自适应回归损失通过 EMA 缓存感知每个去噪步的“正常”损失水平：当某样本的损失显著高于历史均值时，Sigmoid 权重函数自动降低其贡献，抑制偏差过大的数据点；当损失在正常范围内时，权重接近 1，保持有效的真实分布对齐。消融实验证实，加入 AdaLoss 后，Instance Preservation 从 DMD 基线的 88.88 提升至 92.39（表 2），接近教师模型水平。

### 时序坍塌的应对与时序正则化

DMD 蒸馏后的视频出现运动显著减少（图 1 右），Dynamic Degree 仅 72.22。时序正则化损失以负对数方差的形式直接惩罚帧间变化过小的生成结果，强制学生模型保持运动多样性。加入 TR 后，Dynamic Degree 从 72.22 跃升至 100.00（表 2），完全恢复运动动态。

然而，未截断的时序损失会导致严重的帧跳跃和内容幻像伪影（图 14）：训练后期，生成器过度放大帧间方差，造成建筑物扭曲、场景内容突变为不相关内容等幻觉现象。截断阈值设为 0.6 时，运动分数和实例保存达到最佳平衡（图 12）。

### 推理优化

推理阶段采用帧插值策略：高噪声去噪步（前 2 步）将帧率减半以降低计算量，低噪声步前通过 U-Net 插值恢复原始帧率。这一设计的依据是图 15 的统计分析——高噪声阶段相邻帧的余弦相似度显著更高，半帧率推理不会损失关键的运动信息。该模块与自适应回归损失、时序正则化结合后（Full+VIF），在 VBench2 上取得 55.08（1.3B）和 59.06（14B）的 Total Score，分别比 DMD 基线提升 +1.45 和 +2.19（表 1）。

### 输入输出规范

- **训练输入**：真实视频-文本对（回归支路，使用 15 万高质量视频子集）+ 文本条件（生成支路）
- **推理输入**：高斯噪声 + 文本条件
- **输出**：少步去噪生成的视频序列（4 步推理）
- **教师模型**：Wan2.1 预训练权重，所有蒸馏方法共享同一教师以保证公平比较

### 补充图表

![[assets/figures/papers/paper_list_l835_https_arxiv_org_abs_2603_21864/figures/002_Figure_2.jpg]]
*Figure 2: Our method distills a pre-trained teacher model, denoted as*



### 3.1 问题分析：DMD蒸馏中的过饱和与运动坍塌

分布匹配蒸馏（DMD）在迁移至视频生成时暴露出两个核心缺陷：**颜色过饱和**与**时序模式坍塌**（运动幅度显著降低）。如图1所示，DMD和rCM等基线方法生成的视频出现严重的色彩过饱和，同时运动动态明显减弱。

过饱和的根源在于DMD的分布匹配机制。如Figure 3所示，在给定去噪时间步 $t$，教师模型 $s_{\text{real}}$ 对细粒度细节的过度强调会偏置学生模型 $s_{\text{fake}}$ 的分布估计，使其收敛至过饱和的次优分布。由于自回归生成中误差逐帧累积，这种色彩偏差会随时间步加剧，严重降低视频感知质量。

运动坍塌则源于蒸馏过程缺乏对时序变化的显式约束。DMD仅通过KL散度匹配教师与学生的边缘分布，未对帧间运动幅度施加任何正则化，导致学生模型倾向于生成静态或低运动幅度的输出。

### 3.2 自适应回归损失（Adaptive Regression Loss）

为解决过饱和问题，本文引入直接监督机制——自适应回归损失。核心思想是：利用真实视频数据对学生的去噪重建进行监督，并通过**自适应权重**动态调节监督强度，抑制偏差过大的样本对分布的扰动。

**基础回归损失**定义如下：

$$\mathcal{L}_{\text{reg}} = w_{t,s} \| \epsilon_{\theta}(x_t, t) - \epsilon \|_2^2$$

其中 $x_t = \alpha_t x_0 + \sigma_t \epsilon$ 为加噪后的真实视频帧，$\epsilon_{\theta}(x_t, t)$ 为学生模型的噪声预测，$w_{t,s}$ 为去噪步 $t$ 和训练步 $s$ 依赖的自适应权重。

**自适应权重的计算**依赖于一个指数移动平均（EMA）缓存，用于记录各去噪步的历史回归损失均值：

$$\bar{\mathcal{L}}_{t,s} = \alpha \mathcal{L}_{t,s-1} + (1-\alpha) \mathcal{L}_s$$

其中 $\mathcal{L}_s$ 为当前训练步的回归损失值，$\alpha$ 为EMA衰减系数。基于该缓存，自适应权重通过Sigmoid函数生成：

$$\omega_{t,s} = 1 - \sigma(k \cdot (\mathcal{L}_s - \bar{\mathcal{L}}_{t,s-1})), \quad \sigma(x) = \frac{1}{1+e^{-x}}$$

**权重机制解析**：当当前损失 $\mathcal{L}_s$ 显著高于历史均值 $\bar{\mathcal{L}}_{t,s-1}$ 时，偏差 $\mathcal{L}_s - \bar{\mathcal{L}}_{t,s-1}$ 为正且较大，$\sigma(\cdot)$ 趋近于1，$\omega_{t,s}$ 趋近于0，从而抑制异常样本的梯度贡献。反之，当损失低于历史均值时，权重趋近于1，允许有效样本充分参与训练。超参数 $k$ 控制Sigmoid函数的陡峭程度，实验表明 $k=3.0$ 能在早期大偏差抑制与后期精细区分之间取得最佳平衡（见图13）。

**消融验证**：如Figure 4所示，简单回归损失（Row 3）会导致物体融合伪影（$t=2.5\text{s}$ 处），而自适应回归损失（Row 4）成功消除了该伪影。定量消融（Table 2）进一步表明，在DMD基础上加入自适应回归损失（AdaLoss）后，实例保存得分（Instance Preservation）从88.88大幅提升至92.39，接近教师模型水平。

### 3.3 时序正则化损失（Temporal Regularization Loss）

为对抗运动坍塌，本文提出时序正则化损失，以负对数方差的形式惩罚低时序方差的生成输出：

$$\mathcal{L}_{\text{temp}} = -\log(\mathbb{E}_{x \sim p_{\theta}}[\text{Var}(x)] + \epsilon)$$

其中 $\text{Var}(x)$ 为生成视频帧序列的像素级方差，$\epsilon$ 为数值稳定项。该损失强制学生模型保持足够的帧间变化幅度，从而促进运动多样性。

**截断机制**：未截断的时序损失会导致严重的帧跳跃和内容幻像伪影（见图14）。因此，实际训练中对 $\mathcal{L}_{\text{temp}}$ 施加截断阈值，防止其过度放大帧间变化。消融实验（Figure 12）表明，截断阈值设为0.6时，运动分数和实例保存达到最佳平衡。

**消融验证**：Table 2显示，在DMD基础上单独加入时序正则化（TR）后，运动动态得分（Dynamic Degree）从72.22跃升至100.00，完全恢复了运动多样性。

### 3.4 帧插值推理模块

为降低推理计算开销，本文提出**半帧率推理策略**：在高噪声去噪阶段（前2步）将帧率减半，低噪声阶段前通过U-Net插值模块恢复原始帧率。该设计的动机来自统计分析（Figure 15）：高噪声阶段相邻帧的余弦相似度显著更高，表明此时帧间冗余较大，降低帧率不会严重损失信息。

![[assets/figures/papers/paper_list_l835_https_arxiv_org_abs_2603_21864/figures/017_Figure_15.jpg]]
*Figure 15: Violin plot showing the distribution of adjacent-frame cosine similarity across different denoising stages. The overall similarity is notably higher during the high-noise stage, which motivates our approach of halving the inference frame rate in this phase to reduce computational cost*

### 3.5 最终生成器损失

组合分布匹配、自适应回归和时序正则化，最终生成器 $G_{\phi}$ 的训练损失为：

$$\mathcal{L}_{G} = \mathcal{L}_{\text{KL}} + \omega_{\text{reg}} \omega_{t,s} \mathcal{L}_{\text{reg}} + \omega_{\text{temp}} \mathcal{L}_{\text{temp}}$$

其中 $\mathcal{L}_{\text{KL}}$ 为DMD的分布匹配损失（Eq. 4），$\omega_{\text{reg}}$ 和 $\omega_{\text{temp}}$ 分别为回归损失和时序损失的全局平衡超参数。训练流程如Figure 2所示：真实视频-文本对用于计算自适应回归损失，纯噪声生成用于计算时序正则化损失和分布匹配损失，三者联合更新学生生成器。

### 补充图表

![[assets/figures/papers/paper_list_l835_https_arxiv_org_abs_2603_21864/figures/004_Figure_3.jpg]]
*Figure 3: This figure explains the origin of oversaturation in distribution-matching distillation. At a given denoising timestep*

![[assets/figures/papers/paper_list_l835_https_arxiv_org_abs_2603_21864/figures/003_Figure_4.jpg]]
*Figure 4: A naive regression loss (Row 3) causes object fusion artifacts (t=2.5s) absent in the teacher (Row 1) and baseline (Row 2). Our adaptive loss (Row 4) resolves this artifact, improving generation quality*

![[assets/figures/papers/paper_list_l835_https_arxiv_org_abs_2603_21864/figures/015_Figure_13.jpg]]
*Figure 13: Visualization of the adaptive weight function in Eq. (7) for different values of k. The x-axis represents the deviation*



## 实验与关键发现

### 核心瓶颈验证：过饱和与时序坍塌的量化表现

分布匹配蒸馏（DMD）在迁移至视频生成时，产生两个相互关联的退化现象：**颜色过饱和**与**时序模式坍塌**。图1的定性对比清晰展示了这一瓶颈——DMD和rCM生成的视频在左侧案例中出现严重的颜色过饱和，右侧案例则表现为运动幅度显著减少，即“时序坍塌”。在自回归生成中，过饱和现象会逐帧累积，进一步降低长视频质量。

从量化角度看，表2的消融实验提供了直接证据：DMD基线的Dynamic Degree（运动动态得分）仅为**72.22**，实例保存得分（Instance Preservation）为**88.88**，两者均显著低于教师模型水平。这验证了分析中的核心判断——蒸馏过程中的分布偏差同时损害了视觉保真度和时序一致性。

### 主实验结果

表1报告了在VBench2和VBench1两个基准上的全面对比。我们的方法在两个模型规模下均取得最优总分：

- **VBench2**：1.3B模型总分**55.08**（DMD*基线53.63，提升+1.45），14B模型总分**59.06**（DMD*基线56.87，提升+2.19）
- **VBench1**：1.3B模型总分**81.35**（DMD*基线80.66，提升+0.69），14B模型总分**82.57**（DMD*基线79.63，提升+2.94）

值得注意的是，14B模型在VBench1上的提升幅度（+2.94）远大于1.3B模型（+0.69），表明自适应蒸馏方法对更大规模模型的分布偏差修正更为有效。

图5的定性对比进一步验证：基线方法在左侧案例中产生过饱和颜色，右侧案例中呈现僵硬或静态的运动模式，而我们的方法生成更自然的色调、更流畅的时序动态，且场景切换与提示词更一致。

### 用户研究

图7报告了用户偏好研究结果。我们的蒸馏学生模型不仅一致优于所有基线方法，甚至**比其教师模型Wan2.1更受用户偏好**，同时推理成本显著降低。这一反直觉的结果表明，自适应回归损失和时序正则化的联合作用不仅修复了蒸馏带来的退化，还引入了教师模型可能缺乏的运动增强效果。研究招募了12名独立标注者，每个视频对至少经3人评判，采用多数投票决定偏好，确保了统计可靠性。

### 消融实验：组件贡献的因果分析

表2的消融实验逐层揭示了各组件的因果贡献：

| 配置 | Dynamic Degree | Instance Preservation |
|------|---------------|----------------------|
| DMD（基线） | 72.22 | 88.88 |
| DMD + TR（时序正则化） | **100.00** | 87.94 |
| DMD + AdaLoss（自适应回归损失） | 84.41 | **92.39** |
| Full + VIF（完整模型） | 100.00 | 91.49 |

**时序正则化（TR）的因果效应**：单独添加TR将Dynamic Degree从72.22提升至100.00（+27.78），完全消除了运动坍塌。这表明运动减少的根本原因是蒸馏过程中缺乏对时序方差的约束，而负对数方差损失$\mathcal{L}_{\mathrm{temp}} = -\log(\mathbb{E}_{x\sim p_\theta}[\mathrm{Var}(x)] + \epsilon)$直接惩罚静态输出，强制恢复了运动多样性。然而，TR对实例保存得分有轻微负面影响（88.88→87.94），揭示了运动增强与内容保持之间的内在张力。

**自适应回归损失（AdaLoss）的因果效应**：单独添加AdaLoss将Instance Preservation从88.88提升至92.39（+3.51），接近教师模型水平。这验证了分析中的核心机制——通过EMA缓存记录各去噪步的历史回归损失，并用Sigmoid函数$\omega_{t,s} = 1 - \sigma(k \cdot (\mathcal{L}_s - \bar{\mathcal{L}}_{t,s-1}))$生成自适应权重，有效抑制了偏差过大的样本对分布的扭曲，同时保持了对真实数据分布的对齐。AdaLoss对运动得分也有正向贡献（72.22→84.41），说明过饱和的缓解间接有利于运动模式的保持。

**完整模型的协同效应**：Full+VIF配置同时达到Dynamic Degree 100.00和Instance Preservation 91.49，证明了两个组件在联合作用时互补而非冲突——TR恢复运动多样性，AdaLoss修正分布偏差，帧插值模块（VIF）在高噪声步（前2步）采用半帧率推理降低计算开销，同时通过U-Net插值恢复全帧率，保持了生成质量。

### 自适应权重的行为分析

图13可视化了自适应权重函数在不同斜率$k$下的曲线。当$k=3.0$时（论文采用的设置），权重函数能够在早期大偏差时有效抑制（$\omega \to 0$），而在后期精细区分阶段保持足够的敏感度。消融分析证实$k=3.0$能有效兼顾早期大偏差抑制与后期精细区分。

图4的定性消融提供了自适应权重的直观证据：简单回归损失（Row 3）在$t=2.5s$时产生物体融合伪影，而教师模型（Row 1）和DMD基线（Row 2）均无此问题。自适应损失（Row 4）成功消除了该伪影。这表明固定权重的回归损失会在某些样本上引入过强的分布偏移，而自适应机制通过动态调节权重避免了这一问题。

### 时序正则化的截断机制与失败模式

图12展示了时序正则化损失截断阈值对模型性能的影响。阈值设为**0.6**时，运动分数和实例保存达到最佳平衡——过低阈值无法充分激发运动，过高阈值则导致内容保持下降。

图14揭示了不截断时序损失的严重后果：训练后期学生生成器产生严重伪影。上图案例中，第一秒后出现剧烈的内容偏移，建筑物明显扭曲；下图案例中，场景内容在两秒处突然消失，三秒处再次发生重大内容偏移。这些现象与合理的相机运动不一致，是典型的“幻觉”表现。这揭示了时序方差正则化的本质风险——负对数形式缺乏自然收敛上界，若不加以截断，会过度放大帧间变化，导致内容幻像和帧跳跃。截断机制通过限制$\mathcal{L}_{\mathrm{temp}}$的最大贡献，在运动增强与内容稳定之间建立了必要的人工约束。

### 风格迁移的下游适应性

图6展示了自适应回归损失在下游动画风格迁移中的适应性。教师模型和DMD基线均无法生成与目标域一致的特定动漫风格视频，而自适应回归损失使蒸馏过程能够有效地将真实数据分布（GT）迁移到学生模型。这表明自适应回归损失不仅是一种质量修复机制，还赋予了蒸馏框架对数据域偏移的适应能力。

### 方法的可扩展性与局限性

实验在两个模型规模（1.3B和14B）上均验证了方法的有效性，且14B模型获益更大，表明方法具有良好的可扩展性。帧插值模块（图15的统计分析显示高噪声阶段相邻帧余弦相似度显著更高，为半帧率推理提供了依据）有效降低了推理计算开销。

然而，以下局限性需要关注：时序正则化损失缺乏自然收敛机制，必须人工设置截断阈值（0.6），否则会导致运动伪影和内容幻像（图14）；自适应回归损失依赖于历史损失缓存，EMA系数$\alpha$可能影响对新数据分布的适应速度；方法仅在Wan2.1模型上验证，迁移到其他视频扩散主干网络（如DiT、UNet3D）的有效性尚待检验。

### 补充图表

![[assets/figures/papers/paper_list_l835_https_arxiv_org_abs_2603_21864/figures/001_Figure_1.jpg]]
*Figure 1: Baselines like DMD and rCM show severe color oversaturation (left) and reduced motion indicative of temporal collapse (right). Our method achieves appropriate saturation and enhances motion dynamics beyond the teacher model*

![[assets/figures/papers/paper_list_l835_https_arxiv_org_abs_2603_21864/figures/005_Table_1.jpg]]
*Table 1: Quantitative comparison on two benchmarks (VBench2 and VBench1). Our method achieves the best overall score across all metrics and datasets. DMD∗ is denoted as our baseline method. In all result tables, bold text indicates the optimal result, while underlined text represents the suboptimal result*

![[assets/figures/papers/paper_list_l835_https_arxiv_org_abs_2603_21864/figures/009_Table_2.jpg]]
*Table 2: Ablation study on the effectiveness of the proposed Adaptive Regression Loss and Temporal Regularization. DMD serves as the baseline method, while TR and AdaLoss denote models equipped with the Temporal Regularization and Adaptive Regression Loss, respectively. Full+VIF refers to the model incorporating both components and frame-interpolation*

![[assets/figures/papers/paper_list_l835_https_arxiv_org_abs_2603_21864/figures/006_Figure_5.jpg]]
*Figure 5: Qualitative comparison. Baseline methods tend to produce oversaturated colors (left case) and exhibit stiff or static motion (right case), while our method generates videos with more natural color tones, smoother temporal dynamics, and scene transitions that better align with the prompt. The highlighted text in the prompt indicates key visual changes described in the scene. Zoom in for better visualization*

![[assets/figures/papers/paper_list_l835_https_arxiv_org_abs_2603_21864/figures/014_Figure_12.jpg]]
*Figure 12: This figure illustrates the impact of the truncation threshold of the temporal regularization loss on model performance. The horizontal axis represents the truncation threshold of the regularization loss, while the vertical axis shows the motion score and the instance preservation score of the videos generated by the student model, respectively*

![[assets/figures/papers/paper_list_l835_https_arxiv_org_abs_2603_21864/figures/012_Figure_10.jpg]]
*Figure 10: Comparison with baselines on MovieGen prompts. While DMD and rCM (a strong performer from Sec. 4) produce videos with low motion dynamics and oversaturated colors, our method resolves both issues. It achieves superior motion, well-calibrated colors, and excellent detail and stability.More video examples are included in the supplementary zip file. (Note: We have confirmed that any visual artifacts in some videos are not code-level issues.)*

![[assets/figures/papers/paper_list_l835_https_arxiv_org_abs_2603_21864/figures/016_Figure_14.jpg]]
*Figure 14: Failure cases resulting from unclipped temporal regularization. Without clipping, the student generator produces severe artifacts late in training. (Top) After the first second, a drastic content shift occurs, accompanied by a noticeable distortion of the building (highlighted by the red box). (Bottom) The scene content abruptly vanishes at the two-second mark and is replaced by another major content shift at the three-second mark (highlighted by the red box). These phenomena, inconsistent with plausible camera motion, are clear manifestations of hallucinations. This highlights the necessity of clipping the temporal loss to prevent it from excessively amplifying inter-frame variance*



## 定位与知识库关联

### 1. 方法继承与基线关系

本工作直接建立在**分布匹配蒸馏（Distribution Matching Distillation, DMD）**框架之上。DMD通过最小化学生生成分布与教师分布之间的KL散度，将多步扩散模型压缩为少步生成器，其核心梯度为：

$$\nabla_{\phi} \mathcal{L}_{\mathrm{DMD}} \triangleq \mathbb{E}_{t} [ \nabla_{\phi} \mathrm{KL} ( p_{\mathrm{gen}, t} \| p_{\mathrm{data}, t} ) ]$$

然而，论文通过分析指出（Figure 3），DMD在迁移至视频生成时存在根本性缺陷：教师模型在去噪过程中对细粒度细节的过度强调会偏置学生模型朝向过饱和、次优的分布，导致颜色失真和运动模式坍塌。这一发现构成了本工作的核心动机——DMD的分布匹配机制本身缺乏对真实数据分布的显式锚定，而本方法通过引入自适应回归损失在蒸馏过程中直接注入真实视频监督，填补了这一空白。

与现有蒸馏路线的对比：

- **DMD/DMD2**：本方法的生成器训练流程继承自DMD2，包括伪造得分模型 $s_{\mathrm{fake}}$ 的在线更新策略。但DMD系列仅依赖分布匹配损失 $\mathcal{L}_{\mathrm{KL}}$，缺乏对过饱和和时序坍塌的针对性处理。
- **LCM（潜在一致性模型）**：一致性蒸馏路线，通过强制相邻时间步输出一致性实现少步生成。论文将LCM列为对比基线，但一致性约束本身不直接解决视频特有的时序动态退化问题。
- **rCM（得分正则化连续时间一致性模型）**：在一致性蒸馏中引入得分正则化，是基线中表现较强的对比方法（Figure 10），但仍出现严重的过饱和和低运动动态。
- **PCM / DCM**：同样被列为对比蒸馏方法，论文未详细讨论其机制差异，仅作为性能参照。

本方法的核心创新在于**两个独立于DMD框架的可插拔组件**：自适应回归损失（Sec. 3.2）和时序正则化损失（Sec. 3.3）。消融实验（Table 2）清晰验证了二者的独立贡献——在DMD基线（Dynamic Degree 72.22, Instance Preservation 88.88）上单独添加时序正则化将运动分数提升至100.00，单独添加自适应回归损失将实例保存分数提升至92.39，完整模型（Full+VIF）达到两者兼优。

### 2. 适用边界与迁移性

**已验证的适用范围：**

- **主干网络**：仅在Wan2.1视频扩散模型上完成验证，包括1.3B和14B两个参数规模。
- **推理步数**：4步推理配置（前2步高噪声阶段采用半帧率推理）。
- **视频长度与分辨率**：论文未明确报告极限长度和分辨率，但从实验设置推断主要为短视频生成（秒级）。
- **数据域**：回归损失使用15万高质量视频样本训练，在通用视频生成和动画风格迁移（Figure 6）场景均验证有效。

**未验证的边界（需手动确认）：**

- 方法迁移到其他视频扩散主干（如DiT架构、3D-UNet）的有效性尚未检验，论文将其列为开放问题。
- 在更长视频（>30秒）或更高分辨率（1080p以上）下的可扩展性缺乏实验支撑。
- 自适应损失缓存的EMA系数 $\alpha$ 对新数据分布的适应速度可能影响在线学习场景的表现，论文未给出该参数的消融分析。

**已知的失效模式：**

- 时序正则化损失 $\mathcal{L}_{\mathrm{temp}} = -\log(\mathbb{E}_{x\sim p_\theta}[\mathrm{Var}(x)] + \epsilon)$ 缺乏自然收敛机制，未截断时会导致严重的帧跳跃和内容幻像（Figure 14），必须人工设置截断阈值（消融确定最优值为0.6，Figure 12）。
- 帧插值模块在极低帧率或剧烈运动场景下可能引入轻微插值伪影，论文承认此为局限性之一。

### 3. 局限性与开放问题

**结构性局限：**

1. **时序正则化的截断依赖**：$\mathcal{L}_{\mathrm{temp}}$ 以负对数方差形式无上界地鼓励帧间变化，若不截断会过度放大帧间差异，导致内容偏移和建筑扭曲等幻像（Figure 14）。截断阈值0.6是通过网格搜索获得的经验最优值（Figure 12），缺乏自适应调节机制。

2. **缓存依赖与分布漂移**：自适应权重 $\omega_{t,s} = 1 - \sigma(k \cdot (\mathcal{L}_s - \bar{\mathcal{L}}_{t,s-1}))$ 依赖EMA缓存 $\bar{\mathcal{L}}_{t,s}$ 记录历史损失均值。当训练数据域发生显著变化时，历史缓存可能滞后于当前分布，斜率参数 $k=3.0$（Figure 13）是否需要动态调整尚不明确。

3. **单教师验证**：方法仅在Wan2.1教师模型上验证，过饱和成因分析（Figure 3）是否普适于其他教师模型（如Sora类架构、CogVideoX等）有待检验。

**论文明确提出的开放问题：**

- 自适应损失缓存的设计能否推广到非DMD的蒸馏框架（如一致性蒸馏、对抗蒸馏）？
- 时序正则化能否采用更精确的运动度量（如光流幅度）代替简单的像素方差，以进一步提升运动质量？
- 帧插值模块是否可融入训练过程，实现端到端的极低帧率训练与推理？
- 当训练数据域发生显著变化时，自适应权重的斜率 $k$ 是否需要动态调整？
- 该方法在更长视频（>30秒）或更高分辨率（1080p）下的可扩展性如何？

**知识库定位总结：** Adaptive Video Distillation 处于视频扩散模型蒸馏与分布匹配方法的交叉点，其核心贡献在于揭示了DMD在视频域的两个系统性失效模式（过饱和、时序坍塌），并提出了两个低耦合、高收益的解决方案。该方法在Wan2.1上验证有效，但其泛化性和极限场景鲁棒性仍需跨架构、跨尺度的进一步检验。



## 原文 PDF

![[paperPDFs/CVPR_2026/Adaptive_Video_Distillation_Mitigating_Oversaturation_and_Temporal_Collapse_in_Few_Step_Generation.pdf]]
