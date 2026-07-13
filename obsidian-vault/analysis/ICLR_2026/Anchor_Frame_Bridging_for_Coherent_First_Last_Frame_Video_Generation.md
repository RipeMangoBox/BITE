---
title: "Anchor Frame Bridging for Coherent First-Last Frame Video Generation"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/Anchor_Frame_Bridging_for_Coherent_First_Last_Frame_Video_Generation.pdf
project_link: null
code_link: null
aliases:
- AFBA
- AFBCFLFVG
- "Anchor Frame Bridging (AFB)"
tags:
- ICLR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: "用反向生成候选中的镜像断裂位置选择锚帧来桥接首尾帧视频。"
primary_logic: "AFB先交换首尾帧做反向生成并定位连续性断裂，再把镜像锚帧作为额外条件引导前向生成。"
claims:
- "首尾帧条件在中间帧传播时会衰减，导致语义漂移和时间不一致。"
- "前向与反向生成的连续性断裂点近似对称，可用于自适应选择单个锚帧。"
- "在Wan2.1-I2V上加入AFB显著降低LPIPS和FVD并提高SSIM、PSNR。"
- "单个锚帧在默认设置下优于多个锚帧，过多锚帧会过度约束生成轨迹。"
---

# Anchor Frame Bridging for Coherent First-Last Frame Video Generation

> [!tip] 核心洞察
> 通过反转首尾帧顺序生成高质量候选帧，并利用前向与反向生成中连续性断裂点近似对称的特性，在镜像位置选取锚帧，以最小的额外计算代价（仅需一次反向生成和一次前向生成）显著提升中间帧的语义连贯性。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 锚帧桥接：实现首尾帧视频生成的连贯性 |
| 英文题名 | Anchor Frame Bridging for Coherent First-Last Frame Video Generation |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=isNjWnVsUR) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/image_and_video_generation |
| Method | Anchor Frame Bridging (AFB) |
| Dataset | 自定义数据集（436对首尾帧图像） |

> [!tip] 效果简介
> - 自定义数据集（436对首尾帧图像） 上，LPIPS↓ 为 0.16，对比 0.32 (Wan2.1-I2V)，变化 -0.16。
> - 自定义数据集（436对首尾帧图像） 上，FVD↓ 为 375.12，对比 449.68 (Wan2.1-I2V)，变化 -74.56 (16.58%)。
> - 自定义数据集（436对首尾帧图像） 上，SSIM↑ 为 0.97，对比 0.82 (Wan2.1-I2V)，变化 +0.15。

## 概要

本文提出 **Anchor Frame Bridging (AFB)**，一种即插即用的方法，用于解决首尾帧视频生成（First-Last Frame Video Generation）中中间帧语义信息衰减的问题。AFB 通过两个核心步骤运作：首先，自适应地从候选集中选取一个锚帧（anchor frame）；然后，利用该锚帧引导最终视频的生成。在 Wan2.1-I2V 模型上，AFB 实现了 FVD 16.58% 的提升和 PSNR 10.21% 的提升，并在所有评估指标上优于现有基线方法。



在首尾帧视频生成任务中，模型仅以第一帧和最后一帧作为条件，生成中间的连续帧序列。然而，现有方法面临一个核心瓶颈：**中间帧的语义信息衰减**。如 Figure 1(a) 所示，通过 DiT 自注意力机制的帧间注意力可视化分析发现，仅相邻帧之间具有显著的注意力值，而首帧和尾帧对中间帧的注意力值相对较低。这表明首尾帧的确定性语义在传播到中间帧时逐渐减弱，导致场景扭曲、主体变形以及时间一致性差。

Figure 1(b) 进一步展示了这一现象：在原始方法下，首帧与尾帧之间的 LPIPS 相似性在中间帧处出现突然下降，而 AFB 方法则保持了平滑的相似性变化。Figure 1(c) 和 (d) 的定性对比显示，原始方法生成的视频中间帧质量较差，而 AFB 方法平滑了中间帧并增强了视频的时间一致性。



## 核心方法与创新机理

AFB 的核心创新在于**在时间连续性断裂的关键位置自适应地插入锚帧**，通过显式桥接边界帧的语义到中间帧，从而缓解语义漂移。具体而言：

- **反转生成策略**：通过反转首尾帧顺序生成高质量候选帧，利用前向与反向生成中连续性断裂点近似对称的特性（Figure 14 显示前向生成中质量崩溃点出现在第 56 帧，反向生成中出现在第 55 帧，绝对位置偏差仅为 1 帧），在镜像位置选取锚帧。
- **最小额外计算代价**：仅需一次反向生成和一次前向生成，即可显著提升中间帧的语义连贯性。
- **即插即用**：无需额外模型训练，可直接应用于现有 I2V 模型。



![[assets/figures/papers/iclr26_vision_multimodal_applications__image_and_video_generation__b001_isNjWnVsUR_Anchor_Frame_/figures/001_Figure_1.jpg]]

AFB 的整体框架如 Figure 2 所示，包含两个核心模块：

**模块一：自适应锚帧选择（Adaptive Anchor Frame Selection）**（Figure 2(a)）
1. 交换首帧 \(I_0\) 和尾帧 \(I_{N-1}\) 的位置。
2. 使用 Qwen 模型根据交换后的首尾帧生成反向描述文本 \(P^{\mathrm{rev}}\)。
3. 将交换后的首尾帧通过 VAE 编码器编码为潜变量 \(z_c\)。
4. 在流匹配模型中进行反向去噪，生成候选帧集合。
5. 基于 LPIPS 质量评估函数检测连续性断裂点，通过镜像关系确定锚帧索引 \(n_a = (N-1)(1-\alpha)\)。

**模块二：锚帧引导生成（Anchor Frame Guided Generation）**（Figure 2(b)）
1. 将首帧、尾帧和锚帧与零填充帧沿时间轴拼接，形成引导帧 \(I_c\)。
2. 引入二进制掩码 \(M\) 指示哪些帧已存在（1 表示保留，0 表示生成）。
3. 使用 CLIP 图像编码器提取首尾帧的条件特征并拼接。
4. 利用 Qwen 生成前向文本提示 \(P^{\mathrm{fwd}}\)。
5. 在流匹配模型中进行最终的去噪生成，得到与首尾帧高度一致的视频。



### 5.1 扩散模型基础

前向马尔可夫过程将干净潜变量 \(z_0\) 逐步添加高斯噪声，经过 \(T\) 步变为纯噪声：

\[
q(z_{1:T} \mid z_0) = \prod_{t=1}^T q(z_t \mid z_{t-1}), \quad q(z_t \mid z_{t-1}) = \mathcal{N}\left(z_t; \sqrt{1-\beta_t} z_{t-1}, \beta_t \mathbf{I}\right)
\]

反向去噪过程从纯噪声 \(z_T\) 开始，通过去噪网络 \(f_\theta\) 和条件 \(c\) 迭代恢复干净潜变量：

\[
z_{t-1} = \mathrm{update}(z_t, f_\theta(z_t; t, c); t)
\]

### 5.2 自适应锚帧选择

**反向生成提示**：使用 Qwen 模型根据交换后的首尾帧生成反向描述文本：

\[
P^{\mathrm{rev}} = \mathrm{Qwen}(I_{N-1}, I_0)
\]

**条件输入编码**：将交换后的首尾帧通过 VAE 编码器 \(E\) 编码为潜变量：

\[
z_c = E(I_{N-1}, I_0)
\]

**反向去噪（速度场形式）**：在流匹配模型中，使用速度场 \(u_\theta\) 进行反向去噪：

\[
z_{t-1} = \mathrm{update}(z_t, u_\theta(z_t; t, z_c, c_{P^{\mathrm{rev}}}); t)
\]

**预测干净样本**：从当前噪声潜变量 \(z_t\) 和噪声预测网络 \(\epsilon_\theta\) 中估计干净潜变量：

\[
\hat{z}_0 = \frac{z_t - \sqrt{1-\bar{\alpha}_t} \epsilon_\theta(z_t, t)}{\sqrt{\bar{\alpha}_t}}
\]

**锚帧索引**：根据前向生成中连续性断裂点的归一化位置 \(\alpha\)，在反向生成候选集中通过镜像关系确定锚帧索引：

\[
n_a = (N-1)(1-\alpha)
\]

**帧质量评估函数**：通过计算帧 \(I_n\) 与其相邻帧的 LPIPS 的负局部平均值来评估帧质量：

\[
Q(I_n) = -\frac{1}{2}(\mathrm{LPIPS}(I_{n-1}, I_n) + \mathrm{LPIPS}(I_n, I_{n+1}))
\]

LPIPS 值越大，\(Q\) 值越小，表示帧质量越低。

### 5.3 锚帧引导生成

**条件特征拼接**：将首帧和尾帧的 CLIP 图像特征 \(c_0\) 和 \(c_{N-1}\) 拼接成条件向量：

\[
\boldsymbol{c}_i = [\boldsymbol{c}_0, \boldsymbol{c}_{N-1}]
\]

**最终迭代去噪**：锚帧引导生成中的最终去噪过程，条件包括重排后的掩码 \(m\)、图像条件 \(c_i\)、文本条件 \(c_{P^{\mathrm{fwd}}}\) 和潜变量条件 \(z_c\)：

\[
z_{t-1} = \mathrm{update}(z_t, u_\theta(z_t; t, m, c_i, c_{P^{\mathrm{fwd}}}, z_c); t)
\]



## 实验与关键发现

### 6.1 数据集与设置

作者构建了一个包含 436 对首尾帧图像的数据集（Figure 3），覆盖多种场景和运动类型。所有实验均在 NVIDIA A100 GPU 上进行，基线方法使用其官方实现和默认超参数。

### 6.2 主要结果

Table 1 展示了与基线模型的定量比较。Wan2.1 + AFB 在所有指标上均优于所有基线模型：


![[assets/figures/papers/iclr26_vision_multimodal_applications__image_and_video_generation__b001_isNjWnVsUR_Anchor_Frame_/figures/009_Table_1.jpg]]
*Table 1: Comparison with baseline models.*

| 方法 | LPIPS↓ | FVD↓ | SSIM↑ | PSNR↑ | GPT-4o评分↑ | Gemini 2.0 Flash评分↑ |
|------|--------|------|-------|-------|-------------|----------------------|
| Wan2.1-I2V | 0.32 | 449.68 | 0.82 | 32.13 | 79.55 | 80.12 |
| HunyuanVideo-I2V | 0.35 | 468.23 | 0.79 | 31.45 | 77.23 | 78.45 |
| Wan2.1-FLF2V | 0.28 | 413.68 | 0.88 | 33.67 | 83.12 | 84.23 |
| ViBiDSampler | 0.31 | 435.56 | 0.84 | 32.89 | 81.34 | 82.56 |
| Generative Inbetweening | 0.26 | 405.34 | 0.90 | 34.12 | 85.67 | 86.12 |
| **Wan2.1 + AFB** | **0.16** | **375.12** | **0.97** | **35.41** | **88.64** | **89.35** |

Figure 4 的定性比较显示，Wan2.1 + AFB 在不同场景下均能生成更连贯、更清晰的中间帧。

### 6.3 消融研究

**锚帧数量消融**（Table 2）：在默认 5 秒视频设置下，使用单个锚帧（\(N_a=1\)）达到最优性能。增加锚帧数量会导致性能下降，归因于过度约束生成轨迹。


![[assets/figures/papers/iclr26_vision_multimodal_applications__image_and_video_generation__b001_isNjWnVsUR_Anchor_Frame_/figures/013_Table_2.jpg]]
*Table 2: Ablation study on multiple anchor frames.*

| \(N_a\) | LPIPS↓ | FVD↓ | SSIM↑ | PSNR↑ |
|---------|--------|------|-------|-------|
| 1 | **0.16** | **375.12** | **0.97** | **35.41** |
| 2 | 0.18 | 386.94 | 0.93 | 34.27 |
| 3 | 0.21 | 397.50 | 0.82 | 30.49 |

**停止步长消融**（Table 3）：停止步长 \(K=15\) 时，FVD 为 388.45，接近全通 AFB（375.12），推理时间仅增加 35%（27 分钟 vs 20 分钟），实现了性能与成本的最佳平衡。


![[assets/figures/papers/iclr26_vision_multimodal_applications__image_and_video_generation__b001_isNjWnVsUR_Anchor_Frame_/figures/011_Table_3.jpg]]
*Table 3: Ablation study on stop step K.*

| \(K\) | 时间开销 | FVD↓ | LPIPS↓ | SSIM↑ | PSNR↑ |
|------|---------|------|--------|-------|-------|
| 5 | +15% | 412.73 | 0.19 | 0.90 | 32.74 |
| 15 | +35% | 388.45 | 0.18 | 0.93 | 33.68 |
| 40 | +85% | 379.35 | 0.16 | 0.96 | 34.81 |
| 50 | +105% | 375.12 | 0.16 | 0.97 | 35.41 |

**文本提示消融**（Table 4）：使用 Qwen 生成的文本提示显著优于通用文本提示。


![[assets/figures/papers/iclr26_vision_multimodal_applications__image_and_video_generation__b001_isNjWnVsUR_Anchor_Frame_/figures/012_Table_4.jpg]]
*Table 4: Ablation study on text prompts.*

| 方法 | 文本类型 | LPIPS↓ | FVD↓ | SSIM↑ | PSNR↑ |
|------|---------|--------|------|-------|-------|
| Wan2.1 | 通用文本 | 0.32 | 486.23 | 0.76 | 29.15 |
| Wan2.1+AFB | 通用文本 | 0.28 | 475.33 | 0.81 | 30.54 |
| Wan2.1 | Qwen文本 | 0.32 | 449.68 | 0.82 | 32.13 |
| Wan2.1+AFB | Qwen文本 | **0.16** | **375.12** | **0.97** | **35.41** |

### 6.4 额外分析与用户研究

**帧间相似性分析**（Figure 5）：对于 DAVIS-25 train-69，初始帧几乎没有变化，但从第 40 帧开始出现突然的场景切换（摩托车运动），表明中间帧的连续性差。对于 RealEs-25 95，场景在第 40 到 70 帧之间突然切换，证明中间帧的生成不受首尾帧控制。

**注意力可视化**（Figure 6）：应用 AFB 后，中间帧的注意力图稀疏性显著降低，表明首尾帧的语义成功桥接到中间帧。

**用户研究**（Figure 17）：收集了 52 份有效回复，涵盖视频一致性、文本对齐和视觉质量三个维度。结果显示，Wan2.1 + AFB 比单独使用 Wan2.1 更受用户青睐。在锚帧数量方面，用户明显偏好单个锚帧（\(K=1\)）的配置。

### 6.5 与额外基线的比较

Table 5 和 Figure 15 展示了与 FCVG 和 MoG 的定量和定性比较。AFB 在所有指标上均优于这两种方法，且 FCVG 和 MoG 在静态物体上表现出明显的重影伪影（如橱柜把手）。


![[assets/figures/papers/iclr26_vision_multimodal_applications__image_and_video_generation__b001_isNjWnVsUR_Anchor_Frame_/figures/037_Table_5.jpg]]
*Table 5: Quantitative evaluation. The best results are bolded.*

### 6.6 长视频分析

对于长视频生成（10 秒），Figure 16 和附录 G 的分析表明，多锚帧策略（插入 2 或 3 帧）优于单锚帧方法。随着锚帧数量的增加，中间帧的时间连贯性也得到改善。



## 定位与知识库关联

AFB 属于**首尾帧视频生成**（First-Last Frame Video Generation）领域，该领域最早由 Zeng et al. (2024) 的 Make Pixels Dance 提出。现有方法可分为三类：

1. **基于额外模型训练的方法**：如 Generative Inbetweening (Wang et al., 2025b)，需要训练专门的插值模型。
2. **基于时间反转策略的方法**：如 ViBiDSampler (Yang et al., 2025a)，通过多次噪声注入实现时间反转。
3. **基于帧级约束的方法**：如 FCVG (Zhu et al., 2025) 和 MoG (Zhang et al., 2025)，通过光流或帧级约束引导生成。

AFB 的创新在于**无需额外训练**，通过**反转生成 + 自适应锚帧选择**的即插即用策略，以最小的计算代价显著提升中间帧的语义连贯性。该方法可广泛应用于现有 I2V 模型（如 Wan2.1 和 HunyuanVideo），为视频生成的时间一致性提供了一种高效、通用的解决方案。

**局限性**：
- 在复杂场景（非刚性运动、极端视角变化、严重遮挡）中，AFB 虽有所改善，但无法完全解决关节扭曲和运动模糊等固有问题。
- 默认 5 秒视频使用单个锚帧效果最佳，增加锚帧数量会因过度约束生成轨迹而导致性能下降。
- 全通 AFB 增加 105% 的推理开销，但可通过提前终止（\(K=15\)）将开销降至 35%。
- 数据集规模有限（436 对图像），可能无法完全代表真实世界的多样性。



## 原文 PDF

![[paperPDFs/ICLR_2026/Anchor_Frame_Bridging_for_Coherent_First_Last_Frame_Video_Generation.pdf]]
