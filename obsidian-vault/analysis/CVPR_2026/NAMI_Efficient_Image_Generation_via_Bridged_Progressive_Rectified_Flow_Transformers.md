---
title: "NAMI: Efficient Image Generation via Bridged Progressive Rectified Flow Transformers"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/NAMI_Efficient_Image_Generation_via_Bridged_Progressive_Rectified_Flow_Transformers.pdf
project_link: null
code_link: null
aliases:
- NBPRFT
- NAMI
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/generative_models_diffusion
- topic/benchmarks_datasets_evaluation
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: 通过分辨率区分整流流阶段，低分辨率阶段使用较少Transformer层生成布局和概念轮廓，高分辨率阶段逐步增加层数以细化细节。
primary_logic: 图像生成过程的早期主要进行粗略布局和概念构建，可在低分辨率下用较少参数高效完成；后期细节增强需要较高分辨率。通过分段流和模型空间分解，可以大幅降低推理时间而保持生成质量。
claims:
- NAMI-2B在1024×1024分辨率下相比同等规模的FLUX基线减少64%推理时间。
- NAMI-2B在GenEval和DPG-Benchmark上取得有竞争力或领先的结果，参数规模远小于FLUX-dev。
- 消融研究表明分段流和模型划分均有助于加速推理和提升收敛。
- BridgeFlow模块实现最佳速度-质量权衡，优于更复杂的跳跃点实现。
---

# NAMI: Efficient Image Generation via Bridged Progressive Rectified Flow Transformers

> [!tip] 核心洞察
> 图像生成过程的早期主要进行粗略布局和概念构建，可在低分辨率下用较少参数高效完成；后期细节增强需要较高分辨率。通过分段流和模型空间分解，可以大幅降低推理时间而保持生成质量。

| 字段 | 内容 |
|------|------|
| 中文题名 | NAMI：基于桥接渐进式整流流变换器的高效图像生成 |
| 英文题名 | NAMI: Efficient Image Generation via Bridged Progressive Rectified Flow Transformers |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2503.09242) |
| Topic | #topic/vision_multimodal_applications #topic/generative_models_diffusion #topic/benchmarks_datasets_evaluation #topic/vision_multimodal_applications/image_and_video_generation |
| Method | NAMI (Bridged Progressive Rectified Flow Transformers) |
| Dataset | Inference Time, GenEval, DPG-Benchmark, NAMI-1K Human Evaluation |

> [!tip] 效果简介
> - Inference Time (1024×1024) 上，Overall Latency (s) 2.98 vs 8.47 (-64.82%)。
> - GenEval 上，Overall Score 0.65 vs 0.55 (SDXL) / 0.62 (SD3-medium) / 0.66 (Sana) (与Sana接近，优于SD3-medium)。
> - DPG-Benchmark 上，Overall Score 84.8 vs 83.3 (SDXL) / 87.9 (SD3-medium) / 84.8 (Sana) (与Sana并列，略低于SD3-medium)。

## 概要

当前基于流匹配的 Transformer 图像生成模型（如 FLUX）在取得高质量生成结果的同时，面临着参数规模庞大导致的推理延迟高、计算成本昂贵等核心瓶颈。这一问题在高分辨率（如 1024×1024）场景下尤为突出，严重制约了模型的实用化部署。

NAMI（Bridged Progressive Rectified Flow Transformers）针对上述瓶颈提出了一种渐进式整流流架构。其核心洞察在于：图像生成过程的早期阶段主要进行粗略布局和概念轮廓的构建，可以在低分辨率下用较少参数高效完成；而后期细节增强阶段则需要更高分辨率。基于此，NAMI 将整流流按分辨率划分为多个阶段——低分辨率阶段使用较少的 Transformer 层生成图像布局和概念轮廓，随着分辨率提升逐步增加层数以细化细节；阶段之间通过可学习的 BridgeFlow 线性变换模块进行概率分布对齐，确保跨阶段的速度一致性。

在 2B 参数规模下，NAMI 在 1024×1024 分辨率上相比同等规模的 FLUX 基线减少了 64% 的推理时间（从 8.47 秒降至 2.98 秒），同时在 GenEval（0.65 vs. SD3-medium 的 0.62）和 DPG-Benchmark（84.8，与 Sana 持平）上取得了有竞争力甚至领先的生成质量。消融研究表明，分段流与模型划分分别贡献了约 53% 和 11% 的加速效果，且 BridgeFlow 模块在速度-质量权衡上优于更复杂的跳跃点实现方案。

在方法谱系上，NAMI 属于整流流生成模型的效率优化分支，与 FLUX-dev/schnell（12B）、SD3-medium（2B）、Sana（1.6B）等模型形成直接对比。其独特之处在于将分辨率分层与模型容量分配联合设计，而非简单的模型压缩或蒸馏策略。



### 问题背景：流匹配生成模型的推理效率瓶颈

近年来，基于流匹配（Flow Matching）的视觉生成模型在文本到图像合成任务上取得了显著进展。这类模型通过定义从噪声分布到数据分布的速度场 $v_\theta(x_t, t)$，并求解常微分方程

$$\frac{d x_t}{d t} = v_\theta(x_t, t), \quad x_0 \sim \mathcal{N}(0, I)$$

来生成高保真图像。以 FLUX 系列为代表的大规模流匹配 Transformer 模型（如 FLUX-dev，12B 参数）在生成质量上达到了新的高度，但这一进步伴随着严重的推理效率问题：**高参数规模导致单张图像生成延迟极高，计算成本巨大**，严重制约了实际部署。

### 现有方法的缺口：统一架构中的参数冗余

当前主流的流匹配 Transformer 模型（如 FLUX）采用**统一架构**设计：在整个生成过程中，所有去噪步骤使用相同规模的 DiT（Diffusion Transformer）模块处理相同分辨率的特征图。这种设计存在明显的**参数冗余**——图像生成的早期阶段主要进行粗略布局和概念轮廓的构建，此时高分辨率特征图和大量 Transformer 层的计算能力并未被充分利用。直观上，生成过程的不同阶段对模型容量的需求是不均匀的：早期阶段需要的是全局结构和语义布局的快速建立，而细节增强则集中在后期高分辨率阶段。

尽管已有工作（如 Pyramid Flow）尝试通过多分辨率策略优化生成效率，但它们通常依赖于固定分辨率训练或顺序微调，未能从根本上解决**模型空间与生成阶段需求之间的结构性错配**问题。

### 本文动机：分阶段多分辨率整流流

本文的核心洞察是：**图像生成过程可沿时间轴和分辨率轴进行双重分解**。具体而言：

- **时间维度**：整流流（Rectified Flow）的生成轨迹可以被划分为多个连续的时间窗口，每个窗口对应不同的生成子任务。
- **空间维度**：低分辨率阶段仅需较少的 Transformer 层即可高效生成图像布局和概念轮廓，高分辨率阶段则需要逐步增加层数以细化纹理和细节。

基于这一洞察，本文提出 **NAMI（Bridged Progressive Rectified Flow Transformers）**，通过**分辨率区分的渐进式整流流**架构，在保持生成质量的前提下大幅降低推理延迟。其核心设计包括：(1) 将整流流按分辨率划分为多个阶段，各阶段使用不同规模的子模型；(2) 通过可学习的 **BridgeFlow 模块**连接相邻阶段，对齐不同分辨率下的概率分布。实验表明，NAMI-2B 在 1024×1024 分辨率下相比同等规模的 FLUX 基线**减少 64% 推理时间**（Table 2），同时在 GenEval 和 DPG-Benchmark 上取得有竞争力甚至领先的生成质量（Table 3, Table 4）。



## 核心方法与创新机理

NAMI 的核心创新在于将整流流（Rectified Flow）的生成过程沿两个正交维度进行分解——**分辨率**与**模型容量**——从而在保持生成质量的前提下大幅降低推理成本。与 FLUX 等统一使用相同规模 DiT 处理所有去噪步骤的基线相比，NAMI 引入了两个关键的结构性改动（changed slots）。

### 1. 分段多分辨率整流流

传统整流流模型在整个时间轴上使用固定分辨率和固定深度的 Transformer 处理所有噪声水平。NAMI 的做法是将完整的生成过程划分为 $K$ 个分辨率阶段，每个阶段对应一个时间窗口 $[t_{k-1}, t_k]$。低分辨率阶段（如 256×256）负责生成图像的全局布局和概念轮廓，高分辨率阶段（如 512×512、1024×1024）逐步补充纹理和细节。这种设计源于一个核心洞察：**图像生成的早期步骤主要进行粗粒度的结构和语义构建，完全可以在低分辨率下高效完成，无需消耗高分辨率计算**。

在每个时间窗口内，起始点 $\hat{x}_{s_k}$ 和终点 $\hat{x}_{e_k}$ 之间的线性插值定义为：

$$\hat{x}_t = t' \hat{x}_{e_k} + (1 - t') \hat{x}_{s_k}, \quad t' = (t - t_{k-1}) / (t_k - t_{k-1})$$

阶段间的连接通过上采样和 BridgeFlow 模块实现：上一阶段终点 $\hat{x}_{e_{k-1}}$ 经上采样后，由 BridgeFlow 映射为当前阶段的起始分布 $\hat{x}_{s_k}$。推理时从最低分辨率开始，逐阶段推进至目标分辨率，各阶段使用 Flow-Euler 离散采样器求解 ODE。

### 2. 模型容量的渐进式分配

与分辨率分段相配合，NAMI 在不同阶段分配不同数量的 Transformer 层：低分辨率阶段使用较少层数，高分辨率阶段逐步增加。这一设计打破了“所有去噪步骤使用相同模型”的惯例，实现了模型空间的分解。消融实验（Figure 7）表明，低分辨率阶段层数过少会导致性能下降，层数过多则产生冗余——均匀分配附近性能趋于饱和，验证了“早期生成任务更简单、可用更少参数完成”的假设。

推理时间的分解分析（Figure 9）量化了两个改动的贡献：仅按分辨率分段流即可减少 53% 的计算时间，模型划分在此基础上进一步降低 11%，合计使 1024×1024 分辨率下的推理延迟从 FLUX-2B 基线的 8.47 秒降至 2.98 秒（**-64.82%**，Table 2）。

### 3. BridgeFlow：阶段间分布对齐

阶段间的跳跃点需要将上一阶段的输出分布映射到下一阶段的输入分布。NAMI 采用可学习的线性变换 BridgeFlow：

$$\hat{x}_{s_k} = W \cdot \mathrm{Up}(\hat{x}_{e_{k-1}}) + B$$

相比 Pyramid Flow 的 renoising 方法以及 MLP、CNN 等更复杂的实现，BridgeFlow 在推理时间、FID 和 CLIP score 之间取得了最佳平衡（Table 7）。这表明阶段间的分布偏移相对简单，线性变换已足够捕捉，更复杂的模块反而可能引入不必要的计算开销。

### 4. 多分辨率联合训练

与顺序微调不同，NAMI 采用多分辨率联合训练策略：同时使用不同分辨率的数据，动态调整各阶段权重，所有时间窗口的联合优化目标为：

$$\min_{\theta_k} \sum_{k=1}^{K} \mathbb{E}_{(k, t, (\hat{x}_{s_k}, \hat{x}_{e_k}))} \left[ \int_{t_{k-1}}^{t_k} \left\| (\hat{x}_{s_k} - \hat{x}_{e_k}) - v_{\theta_k}(\hat{x}_t, t) \right\|^2 dt \right]$$

这种联合训练使得各阶段子模型能够协同优化，避免了分阶段独立训练可能引入的误差累积。训练效率对比（Table 6）显示，NAMI 在 256 分辨率下的吞吐量（274 img/s）高于 FLUX 基线（241 img/s），FID 也显著更优（8.93 vs 9.76），同时显存占用更低。

**需要手动验证的点**：论文仅在文本到图像生成任务上验证了 NAMI 的有效性，对图像编辑等任务仅做了初步探索（附录 D 示例）。BridgeFlow 的线性假设在更大规模模型（如 12B+）或更复杂的分布偏移场景下是否仍然充分，尚待进一步验证。



NAMI 的整体 pipeline 围绕“分辨率分阶段整流流 + 模型空间分解”这一核心思路构建，将图像生成过程划分为多个分辨率递增的阶段，并在阶段间引入可学习的桥接模块以对齐概率分布。

**输入与输出流**：推理时，首先在最低分辨率（如 256×256）下采样一个高斯噪声 $x_0 \sim \mathcal{N}(0, I)$ 作为起始点。生成过程按阶段 $k=1$ 到 $k=K$ 顺序推进，每个阶段在其对应的时间窗口 $[t_{k-1}, t_k]$ 内使用 Flow-Euler 采样器求解 ODE。阶段间通过上采样和 BridgeFlow 模块进行变换，将上一阶段的输出映射为下一阶段的起始分布。最终阶段输出目标分辨率（如 1024×1024）下的生成图像。

**模块关系与阶段划分**：整个 pipeline 包含 $K$ 个分辨率阶段，各阶段使用不同规模的 MM-DiT Transformer 块。低分辨率阶段（如 256×256）仅分配少量 Transformer 层，负责生成图像的粗略布局和概念轮廓；随着分辨率提升（如 512×512、1024×1024），Transformer 层数逐步增加，以细化纹理和细节。各阶段的模型参数独立，形成“渐进式”模型空间分解。

**BridgeFlow 桥接机制**：相邻阶段之间通过 BridgeFlow 模块连接。具体而言，第 $k-1$ 阶段的输出 $\hat{x}_{e_{k-1}}$ 经上采样后，通过可学习的线性变换 $W \cdot \mathrm{Up}(\hat{x}_{e_{k-1}}) + B$ 映射到第 $k$ 阶段的起始点 $\hat{x}_{s_k}$。该模块以 MSE 损失预训练，用于对齐不同分辨率阶段间的概率分布偏移，是实现分段流连续生成的关键纽带。

**训练策略**：采用多分辨率联合训练，同时使用不同分辨率的数据，动态调整各阶段权重。训练目标为所有时间窗口内速度场与直线路径间 L2 距离的期望最小化：

$$\min_{\theta_k} \sum_{k=1}^{K} \mathbb{E}_{(k, t, (\hat{x}_{s_k}, \hat{x}_{e_k}))} \left[ \int_{t_{k-1}}^{t_k} \left\| (\hat{x}_{s_k} - \hat{x}_{e_k}) - v_{\theta_k}(\hat{x}_t, t) \right\|^2 dt \right]$$

其中时间窗口内的插值遵循 $\hat{x}_t = t' \hat{x}_{e_k} + (1-t') \hat{x}_{s_k}$，$t' = (t - t_{k-1}) / (t_k - t_{k-1})$。

这一框架的核心优势在于：早期低分辨率阶段的轻量化设计大幅降低了计算量，而后期高分辨率阶段的深层模型保证了细节生成能力。消融实验（Figure 9）表明，按分辨率划分流本身可减少 53% 的计算时间，模型空间分解进一步贡献 11% 的加速，两者叠加使 NAMI-2B 在 1024×1024 分辨率下相比同等规模的 FLUX 基线减少 64% 的推理时间（Table 2）。

### 补充图表

![[assets/figures/papers/paper_list_l902_https_arxiv_org_abs_2503_09242/figures/004_Figure_4.jpg]]
*Figure 4: Overview of NAMI: The left figure shows the progressive flow transformers of NAMI, where the same color represents the same module. The right figure depicts the integration of the BridgeFlow module, which establishes connections across adjacent time windows. Specifically, we divide the image generation process into K resolution stages and the entire flow is divided into K time windows, where adjacent stages are connected through upsampling and the BridgeFlow module. We use fewer transformer layers at the low-resolution stages to generate image layouts and concept contours, progressively adding more layers as the resolution increases*



### 3.1 整流流基础

NAMI 建立在整流流（Rectified Flow）框架之上。生成过程由常微分方程（ODE）描述，定义从噪声到数据的速度场：

$$\frac { d x _ { t } } { d t } = v _ { \theta } ( x _ { t } , t ) , \quad x _ { 0 } \sim \mathcal { N } ( 0 , I )$$

其中 $x_0$ 从标准高斯分布采样，$v_\theta$ 为可学习的速度预测网络。训练目标是最小化速度场与直线路径之间的 $L_2$ 距离：

$$\operatorname* { m i n } _ { \theta } \mathbb { E } _ { x _ { 0 } \sim \mathcal { N } ( 0 , I ) , x _ { 1 } \sim D } \left[ \int _ { 0 } ^ { 1 } \| ( x _ { 0 } - x _ { 1 } ) - v _ { \theta } ( x _ { t } , t ) \| ^ { 2 } d t \right]$$

该目标鼓励速度场学习从噪声 $x_0$ 到数据 $x_1$ 的直线传输路径，从而减少采样所需的 ODE 求解步数。

### 3.2 渐进式分段流与模型空间分解

NAMI 的核心创新在于将统一的整流流过程按分辨率拆分为 $K$ 个阶段，对应 $K$ 个时间窗口。在每个时间窗口 $[t_{k-1}, t_k]$ 内，流轨迹通过线性插值定义：

$$\hat { x } _ { t } = t ^ { \prime } \hat { x } _ { e _ { k } } + ( 1 - t ^ { \prime } ) \hat { x } _ { s _ { k } } , \quad t ^ { \prime } = ( t - t _ { k - 1 } ) / ( t _ { k } - t _ { k - 1 } )$$

其中 $\hat{x}_{s_k}$ 为当前窗口起始点，$\hat{x}_{e_k}$ 为终点。相邻阶段之间，上一阶段的终点 $\hat{x}_{e_{k-1}}$ 经上采样后，通过 BridgeFlow 模块映射为下一阶段的起始点 $\hat{x}_{s_k}$。整个系统的联合优化目标为：

$$\operatorname* { m i n } _ { \theta _ { k } } \sum _ { k = 1 } ^ { K } E _ { ( k , t , ( \hat { x } _ { s _ { k } } , \hat { x } _ { e _ { k } } ) ) } \left[ \int _ { t _ { k - 1 } } ^ { t _ { k } } \left\| \left( \hat { x } _ { s _ { k } } - \hat { x } _ { e _ { k } } \right) - v _ { \theta _ { k } } ( \hat { x } _ { t } , t ) \right\| ^ { 2 } d t \right]$$

**关键设计**：低分辨率阶段（如 $256 \times 256$）仅分配较少 Transformer 层用于生成布局和概念轮廓；随着分辨率提升（如 $512 \times 512$、$1024 \times 1024$），逐步增加层数以细化细节。这种模型空间分解直接降低了高分辨率阶段的浮点运算量，是实现 64% 推理加速的核心机制。

### 3.3 BridgeFlow 模块

阶段间的概率分布对齐由 BridgeFlow 模块完成，其形式为可学习的线性变换：

$$\hat { x } _ { s _ { k } } = W \cdot \mathrm { U p } ( \hat { x } _ { e _ { k - 1 } } ) + B$$

其中 $\mathrm{Up}(\cdot)$ 为上采样操作，$W$ 和 $B$ 为可学习参数。该模块通过 MSE 损失预训练，用于将上一阶段的上采样输出映射到当前阶段速度预测网络期望的起始分布。消融实验（Table 7）表明，线性 BridgeFlow 在推理时间、FID 和 CLIP score 之间取得了最佳平衡，优于 Pyramid Flow 的 renoising 方法以及更复杂的 MLP/CNN 替代方案。

![[assets/figures/papers/paper_list_l902_https_arxiv_org_abs_2503_09242/figures/014_Table_7.jpg]]
*Table 7: Comparison of different implementations at jump point for 256 resolution. Our proposed BridgeFlow module achieves the best overall performance, while more complex modules do not lead to further improvements*

### 3.4 训练与推理

训练阶段，各时间窗口内的速度预测网络使用 MSE 损失进行优化：

$$\mathrm { l o s s } = \Vert ( \hat { x } _ { s _ { k } } - \hat { x } _ { e _ { k } } ) - v _ { \theta _ { k } } ( \hat { x } _ { t } , t ) \Vert ^ { 2 }$$

采用多分辨率联合训练策略，同时使用不同分辨率数据，动态调整各阶段权重（Algorithm 1）。

推理阶段，从最低分辨率采样初始噪声，依次经过 $K$ 个阶段，每个阶段内使用 Flow-Euler 离散化采样器求解 ODE，阶段间通过上采样和 BridgeFlow 完成跳转。

### 补充图表

![[assets/figures/papers/paper_list_l902_https_arxiv_org_abs_2503_09242/figures/002_Figure_3.jpg]]
*Figure 3: Overview of the image generation process for FLUXdev [20] and our NAMI-2B, with upscaling alignment applied during the low-resolution stages of NAMI-2B*



## 实验与关键发现

### 核心推理效率验证

NAMI的核心设计目标是在保持生成质量的前提下大幅降低推理延迟。Table 2（推理时间详情）和Figure 2（推理延迟对比）共同支撑了这一核心结论：在1024×1024分辨率下，NAMI-2B的总推理时间为2.98秒，相比同等规模的FLUX-2B基线模型（8.47秒）减少了**64.82%**。且该加速效果随分辨率提升而更加显著——在256分辨率下加速约30%，在512分辨率下加速约50%，在1024分辨率下达到64%的峰值加速。这一趋势验证了“低分辨率阶段用少量参数处理布局和概念轮廓、高分辨率阶段逐步增加层数”的策略在计算量分配上的有效性：分辨率越高，NAMI节省的冗余计算越多。

![[assets/figures/papers/paper_list_l902_https_arxiv_org_abs_2503_09242/figures/006_Table_2.jpg]]
*Table 2: The inference time details of the NAMI architecture (measured in seconds)*

Figure 9进一步分解了加速来源：按分辨率分段流（flow piece）贡献了约53%的计算时间缩减，而模型划分（model partition）额外贡献了约11%的缩减。两者叠加产生了64%的总加速。

### 生成质量基准对比

**GenEval基准**（Table 3）：NAMI-2B以0.65的Overall Score与Sana（1.6B）的0.66接近，显著优于SDXL（2.6B，0.55）和SD3-medium（2B，0.62）。在子维度上，NAMI在Counting（0.51 vs SD3-medium的0.43）和Position（0.38 vs SD3-medium的0.28）上表现突出，但在Colors（0.78 vs SD3-medium的0.84）上略逊。与12B参数的FLUX-dev（0.66）相比，NAMI-2B以仅1/6的参数量取得了极具竞争力的结果。

**DPG-Benchmark**（Table 4）：NAMI-2B Overall Score为84.8，与Sana（84.8）并列，略低于SD3-medium（87.9）。在Global（88.2 vs SD3-medium的85.7）和Entity（89.4 vs SD3-medium的89.1）子维度上表现强劲，但在Attribute（87.1 vs SD3-medium的91.6）上存在差距。

**NAMI-1K人类评估**（Table 5）：NAMI-2B以70.69的Overall Score领先于SD3-medium（69.97）和Sana（67.80）。在Relevance（87.57 vs SD3-medium的86.83）和Coherence（86.67 vs SD3-medium的85.58）上优势明显，Aesthetic（63.46）与SD3-medium（63.64）持平，Realism（45.07）略低于SD3-medium（45.82）。该基准的文本长度分布（Figure 5）和主题类型分布（Figure 11）显示其覆盖了比GenEval和DPG-Benchmark更长的提示和更多样的主题类型（Figure 10），增强了评估的生态效度。

### 消融研究

**组件有效性**（Figure 6）：在256和512分辨率下，完整的NAMI结构（分段流+模型划分）相比纯FLUX基线收敛更快，FID和CLIP score均更优。单独使用分段流或模型划分均能带来正向收益，但两者结合效果最佳。在512分辨率下，NAMI的FID优势比256分辨率下更显著，印证了高分辨率阶段冗余计算更多、NAMI的收益更大的规律。

**层分配比例**（Figure 7）：低分辨率阶段层数过少会导致性能明显下降（FID上升），层数过多则产生冗余（性能饱和甚至微降）。均匀分配附近性能达到饱和，表明各阶段的计算需求大致均衡，无需极端倾斜的层数分配。

**时间窗口划分**（Figure 8）：1:1:1的均匀划分已取得良好效果。过度偏重某一阶段（如将更多时间分配给高分辨率阶段）可能降低精度，说明各阶段的流积分时间需要合理平衡。

**BridgeFlow模块设计**（Table 7）：在256分辨率下对比了多种跳跃点实现方案。BridgeFlow（可学习线性变换）在推理时间、FID和CLIP score三者之间取得了最佳平衡。更复杂的方案（MLP、CNN、Pyramid Flow的renoising方法）并未带来进一步改善，反而可能增加计算开销或降低质量。这表明阶段间的分布偏移相对简单，线性变换已足以有效对齐。

**训练效率**（Table 6）：NAMI在256分辨率下的训练吞吐量（274 img/s）高于FLUX基线（241 img/s），显存占用更低（22.0 GB vs 28.4 GB），且FID更优（8.93 vs 9.76）。这说明NAMI不仅在推理端高效，在训练端同样具备效率优势。

### 架构细节

Table 1给出了NAMI各变体的架构详情。NAMI采用多阶段MM-DiT Blocks，低分辨率阶段使用较少Transformer层，高分辨率阶段逐步增加层数。阶段间通过Upsampling/Downsampling进行分辨率调整，并由BridgeFlow模块进行分布对齐。推理时采用Flow-Euler采样器求解ODE。

### 失败模式与局限

尽管NAMI在多数基准上表现优异，但在以下方面存在局限：
- **Colors和Attribute子维度**：在GenEval的Colors（0.78）和DPG-Benchmark的Attribute（87.1）上，NAMI与SD3-medium存在差距。这可能与低分辨率阶段对细粒度颜色和属性信息的编码能力有限有关，需要进一步验证。
- **Realism评分**：NAMI-1K人类评估中，NAMI的Realism（45.07）略低于SD3-medium（45.82），表明在真实感方面仍有提升空间。
- **任务泛化**：当前验证仅限于文本到图像生成任务，图像编辑仅做了初步探索（Figure 27示例），尚未系统评估。
- **超大规模扩展**：2B参数规模下的线性加速是否能在12B+模型上保持，尚待验证。

### 补充图表

![[assets/figures/papers/paper_list_l902_https_arxiv_org_abs_2503_09242/figures/003_Figure_2.jpg]]
*Figure 2: An overview of inference latency between the proposed NAMI-2B and the corresponding FLUX-2B base model of the same size without NAMI. With NAMI, inference performance improvement becomes more significant as image resolution increases. The measurements are conducted with a batch size of 1 on an A100 GPU*

![[assets/figures/papers/paper_list_l902_https_arxiv_org_abs_2503_09242/figures/008_Table_3.jpg]]
*Table 3: Comparison of different methods on GenEval. With highlight the best, second best entries. Ovr & Sgl & Two & Cnt & Col & Pos & CA mean: Overall & Single & Two & Counting & Colors & Position & Color Attribution*

![[assets/figures/papers/paper_list_l902_https_arxiv_org_abs_2503_09242/figures/009_Table_4.jpg]]
*Table 4: Comparison of different methods on DPG-Benchmark. With highlight the best, second best entries. Ovr & Gbl & Ent & Attr & Rel & Oth mean: Overall & Global & Entity & Attribute & Relation & Other*

![[assets/figures/papers/paper_list_l902_https_arxiv_org_abs_2503_09242/figures/007_Table_5.jpg]]
*Table 5: Human evaluation results on NAMI-1K dataset. Rele & Cohe & Aes & Real mean: Relevance & Coherence & Aesthetic & Realism. With highlight the best, second best entries*

![[assets/figures/papers/paper_list_l902_https_arxiv_org_abs_2503_09242/figures/010_Figure_6.jpg]]
*Figure 6: The effectiveness of the NAMI components at resolutions of 256 and 512*

![[assets/figures/papers/paper_list_l902_https_arxiv_org_abs_2503_09242/figures/015_Figure_9.jpg]]
*Figure 9: The inference time of NAMI Components*

![[assets/figures/papers/paper_list_l902_https_arxiv_org_abs_2503_09242/figures/013_Table_6.jpg]]
*Table 6: Comparison of Training Efficiency between NAMI and FLUX-based Architectures*

![[assets/figures/papers/paper_list_l902_https_arxiv_org_abs_2503_09242/figures/011_Figure_5.jpg]]
*Figure 5: The distribution of text lengths across GenEval, DPG-Benchmark and NAMI-1K*



## 定位与知识库关联

### 1. 与基线方法的差异定位

NAMI 的核心贡献在于对基于流（Flow-based）的 Transformer 图像生成模型进行**分辨率感知的时空分解**，这与现有方法在两个维度上形成差异化：

**模型架构层面**：传统整流流（Rectified Flow）模型（如 **FLUX** (Black Forest Labs, 2024) 系列）在所有去噪步骤中采用统一分辨率和相同深度的 DiT（Diffusion Transformer）架构。NAMI 则通过**分段渐进式整流流（Bridged Progressive Rectified Flow）**将生成过程按分辨率划分为 K 个阶段：低分辨率阶段（如 256×256）使用较少 Transformer 层生成布局和概念轮廓，高分辨率阶段（如 512×512、1024×1024）逐步增加层数以细化细节。这种“模型空间分解”直接回应了 Flow-based Transformer 参数规模大导致高推理延迟的核心瓶颈。

**阶段连接机制**：在阶段间的“跳跃点”（Jump Point），NAMI 引入可学习的 **BridgeFlow 模块**——一个线性变换 $W \cdot \mathrm{Up}(\hat{x}_{e_{k-1}}) + B$，将上一阶段的上采样输出映射到当前阶段的起始分布。消融实验（Table 7）表明，该模块在推理时间、FID 和 CLIP score 之间取得最佳平衡，优于 **Pyramid Flow** 的 renoising 方法以及 MLP/CNN 等更复杂的实现方案。

**训练策略对比**：与通常采用固定分辨率训练或顺序微调的方法不同，NAMI 采用**多分辨率联合训练**，同时使用不同分辨率数据并动态调整各阶段权重（Algorithm 1），使得各阶段子模型能够协同优化。

### 2. 方法谱系中的位置

NAMI 处于 **高效文生图（Efficient Text-to-Image Generation）** 的研究脉络中，其技术路线可追溯至以下关键节点：

- **整流流/流匹配（Rectified Flow / Flow Matching）**：继承自 Flow Matching 和 Rectified Flow 的理论框架，直接学习从噪声到数据的直线速度场 $v_\theta(x_t, t)$，通过最小化 $\|(x_0 - x_1) - v_\theta(x_t, t)\|^2$ 训练模型。NAMI 的创新在于将该框架**分段化**，在每个时间窗口 $[t_{k-1}, t_k]$ 内独立建模。

- **多分辨率生成**：与 **SANA**（1.6B 参数，采用高压缩 AE）和 **LUMINA-Next**（2B 参数）等高效生成模型相比，NAMI 的独特之处在于将分辨率变化与模型深度变化**显式耦合**，而非仅依赖 VAE 压缩或统一架构。

- **级联/渐进式生成**：区别于传统的级联扩散模型（如 DALL·E 2 的超分辨率级联），NAMI 的渐进式设计内嵌于统一的整流流框架中，各阶段共享相同的训练目标，通过 BridgeFlow 实现端到端优化。

### 3. 适用边界与局限性

基于论文提供的证据，NAMI 的适用边界和局限可归纳如下：

**已验证的适用范围**：
- **文生图任务**：在 GenEval（Overall 0.65）、DPG-Benchmark（Overall 84.8）和自建 NAMI-1K 基准（人类评估 Overall 70.69）上取得有竞争力或领先的结果。
- **模型规模**：主要在 2B 参数级别验证，与同规模的 SD3-medium、Sana 等对比具有优势。
- **分辨率范围**：256×256 至 1024×1024，推理加速随分辨率提升而更加显著（1024×1024 下减少 64% 推理时间）。

**已知局限**：
1. **任务泛化未充分验证**：仅在文生图任务上进行了系统评估，图像编辑等任务仅做了初步探索（附录 D 示例），在其他生成任务（如视频生成、3D 生成）上的有效性尚不明确。
2. **基准覆盖有限**：NAMI-1K 虽然比现有基准更全面，但仍只有 1000 个提示，可能不足以完全反映现实场景的多样性。
3. **阶段间对齐能力上限**：BridgeFlow 为线性变换，尽管实验表明其优于更复杂的方案，但在处理复杂分布偏移时可能存在表达能力的理论上限。
4. **超大规模模型的加速比例未知**：当前验证集中于 2B 级别，在 12B+ 的超大规模模型上是否仍能保持线性加速尚需验证。

### 4. 开放问题

1. **自适应阶段配置**：当前各阶段的层数分配和时间窗口划分依赖人工设定（消融实验显示均匀分配附近性能饱和），如何根据输入提示的复杂度自适应确定最优配置是一个开放方向。

2. **BridgeFlow 的非线性扩展**：线性变换虽已取得最佳权衡，但是否存在更优的非线性变换（如小型注意力模块或条件归一化流）以进一步改善阶段间对齐，值得探索。

3. **与高压缩 VAE 的协同**：SANA 等模型通过高压缩 AE 大幅降低计算量，NAMI 的分段流策略与高压缩 VAE 结合是否能产生叠加加速效果，目前尚无实验证据。

4. **跨模态和跨任务迁移**：该方法在视频生成、3D 生成等需要更高计算量的任务中是否同样有效，是重要的后续研究方向。

5. **更大规模的验证**：在 12B+ 参数规模下，分段流和模型划分的加速比例是否会因通信开销或阶段间瓶颈而衰减，需要进一步实验验证。



## 原文 PDF

![[paperPDFs/CVPR_2026/NAMI_Efficient_Image_Generation_via_Bridged_Progressive_Rectified_Flow_Transformers.pdf]]
