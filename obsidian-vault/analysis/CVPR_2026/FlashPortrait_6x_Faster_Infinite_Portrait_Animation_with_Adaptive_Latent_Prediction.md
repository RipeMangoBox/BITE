---
title: "FlashPortrait: 6x Faster Infinite Portrait Animation with Adaptive Latent Prediction"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/FlashPortrait_6x_Faster_Infinite_Portrait_Animation_with_Adaptive_Latent_Prediction.pdf
project_link: "https://francis-rings.github.io/FlashPortrait"
code_link: null
aliases:
- FlashPortrait
tags:
- CVPR_2026
- topic/vision_multimodal_applications/image_and_video_generation
- topic/generative_models_diffusion
- topic/benchmarks_datasets_evaluation
- topic/vision_multimodal_applications
core_operator: 通过自适应潜在预测机制实现训练无关的推理加速，利用历史潜变量高阶导数与动态调节函数跳过去噪步骤，同时采用归一化面部表达块对齐分布以稳定身份。
primary_logic: 利用泰勒级数展开和有限差分在DiT层上近似潜变量导数，并根据潜在变化率和层间衍生物大小比例自适应调整预测，从而在保持身份一致的前提下实现多步去噪跳过；此外通过对齐潜变量与面部特征的分布中心，增强跨帧身份稳定性。
claims:
- FlashPortrait 在 Hard100 数据集上相较 Wan-Animate 在 AED/APD/MAE 上分别提升 30.9%/30.4%/37.5%，同时推理速度快 3 倍。
- FlashPortrait 在消融研究中达到相对于基线 6 倍推理加速，且视觉质量未明显下降。
- 归一化面部表达块在消融中显著改善身份稳定性，AED 从 44.78 降至 29.68。
- 用户研究中，FlashPortrait 在长期身份保持、面部表情准确性等方面优于已有方法，偏好率达 92.8% 以上。
---

# FlashPortrait: 6x Faster Infinite Portrait Animation with Adaptive Latent Prediction

> [!tip] 核心洞察
> 利用泰勒级数展开和有限差分在DiT层上近似潜变量导数，并根据潜在变化率和层间衍生物大小比例自适应调整预测，从而在保持身份一致的前提下实现多步去噪跳过；此外通过对齐潜变量与面部特征的分布中心，增强跨帧身份稳定性。

| 字段 | 内容 |
|------|------|
| 中文题名 | FlashPortrait：基于自适应潜在预测的6倍速无限人像动画 |
| 英文题名 | FlashPortrait: 6x Faster Infinite Portrait Animation with Adaptive Latent Prediction |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2512.16900) · [Project](https://francis-rings.github.io/FlashPortrait) |
| Topic | #topic/vision_multimodal_applications/image_and_video_generation #topic/generative_models_diffusion #topic/benchmarks_datasets_evaluation #topic/vision_multimodal_applications |
| Method | FlashPortrait |
| Dataset | Hard100, Voxceleb2 & Vfhq, Ablation, User Study |

> [!tip] 效果简介
> - Hard100 上，AED↓ 29.68 vs 42.98 (Wan-Animate) (-30.9%)；MAE↓ 12.54 vs 20.08 (Wan-Animate) (-37.5%)。
> - Voxceleb2 & Vfhq 上，Inference Speed (20s video) 720s vs 2298s (Wan-Animate) (3.2× faster)。
> - Ablation (Acceleration) 上，Inference Speedup 6× vs 1× (无加速基线) (+5×)。

## 概要

人像动画旨在根据驱动视频的面部表情和头部姿态，合成一段身份一致的目标人物视频。尽管基于扩散模型的方法（如 **Wan-Animate**、**HunyuanPortrait**）在生成质量上取得了显著进展，但其在长时域动画中面临三个核心瓶颈：**身份一致性退化**（长时间合成后出现面部扭曲与颜色漂移）、**推理速度缓慢**（完整多步去噪耗时过长），以及**片段间过渡不平滑**（传统滑动窗口策略导致闪烁）。这些瓶颈严重制约了人像动画在实时交互与长视频生成场景中的实际部署。

**FlashPortrait** 针对上述问题提出了一套训练无关的推理加速框架，核心贡献包括：

1. **归一化面部表达块 (Normalized Facial Expression Block)**：通过将 DiT 中的人像交叉注意力输出对齐到图像特征的分布中心，增强跨帧身份稳定性。
2. **加权滑动窗口融合策略**：在长视频推理时对相邻窗口的重叠区域进行帧索引感知的加权融合，消除片段间过渡伪影。
3. **自适应潜在预测加速机制**：利用历史潜变量的高阶有限差分与动态调节函数，在 DiT 各层预测未来时间步的潜变量，从而跳过多步去噪，实现训练无关的 6 倍推理加速。

在 **Hard100** 长视频基准上，FlashPortrait 相较 Wan-Animate 在身份一致性指标 AED 上降低 30.9%（29.68 vs. 42.98），表情准确性指标 MAE 降低 37.5%（12.54 vs. 20.08），同时推理速度快 3 倍以上。用户研究中，FlashPortrait 在长期身份保持维度以 92.8% 的偏好率显著优于竞争对手。消融实验进一步验证了归一化面部块、加权滑动窗口与动态预测函数各自的关键作用。

方法上，FlashPortrait 属于**基于 DiT 的扩散人像动画加速范式**，与 TeaCache、FoCa 等缓存加速方法及 Self-Forcing 等蒸馏方法形成对比——前者加速有限，后者虽加速高但引入身份不一致和伪影，而 FlashPortrait 在 6 倍加速下仍保持视觉质量无明显下降。

### 问题背景

人像动画（Portrait Animation）旨在根据一段驱动视频的运动信号，驱动一张静态参考图像生成同步的面部表情和头部姿态变化，同时严格保持参考图像中的身份特征。这项技术在虚拟主播、数字人交互、影视制作等领域具有广泛的应用前景。近年来，基于扩散模型（Diffusion Models）的方法，尤其是基于 DiT（Diffusion Transformer）架构的模型，如 **Wan-Animate**、**HunyuanPortrait** 和 **FantasyPortrait**，在人像动画的视觉质量和表情精度上取得了显著进展。与此同时，基于 GAN 的方法（如 **LivePortrait**）和基于 3D Morphable Model 的方法（如 **Skyreels-A1**）也在该领域占据一席之地。

### 现有方法的瓶颈

尽管现有方法在短时域人像动画上表现良好，但在实际应用中仍面临两个核心瓶颈：

**1. 长时域生成中的身份漂移与视觉退化。**
当生成超过数百帧的长序列动画时，扩散模型容易出现身份一致性逐渐丧失的问题，表现为面部扭曲、颜色漂移和伪影累积。尤其是当驱动视频中面部运动幅度大且复杂时，模型难以在长时间跨度内稳定维持参考图像的身份特征。部分方法采用滑动窗口策略将长视频切分为短片段分别生成，但简单拼接或传统滑动窗口融合会导致片段间的运动不连贯和表情跳变。

**2. 推理速度慢，难以满足实时交互需求。**
扩散模型的多步迭代去噪过程计算开销极大。以最新的开源人像动画模型 Wan-Animate 为例，生成一段 20 秒的 480×832 视频需要约 2298 秒（超过 38 分钟），远无法满足实时或准实时的应用需求。现有的扩散模型加速方法——包括缓存方法（如 **TeaCache**、**FoCa**）和蒸馏方法（如 **Self-Forcing**）——在应用于长时域人像动画时存在明显局限：缓存方法加速幅度有限，蒸馏方法虽然速度提升显著，但往往引入严重的伪影和身份不一致问题。

### 本文动机

针对上述瓶颈，本文提出 **FlashPortrait**，核心动机在于：
- **维持长时域身份一致性**：需要一种机制，在扩散去噪过程中系统性地对齐潜变量与面部特征的分布，从根本上增强跨帧身份稳定性，而非仅在生成后进行后处理。
- **实现训练无关的显著加速**：需要一种推理阶段的加速机制，能够在不重新训练模型的前提下，利用去噪过程中潜变量的时序冗余性，大幅跳过去噪步骤，同时不牺牲视觉质量和身份保持。
- **统一身份保持与加速**：将身份稳定机制与推理加速机制有机整合到同一 DiT 框架中，使二者协同工作，而非相互独立或彼此冲突。

FlashPortrait 的设计正是围绕上述动机展开：通过**归一化面部表达块（Normalized Facial Expression Block）**对齐潜变量与面部特征的分布中心以稳定身份，通过**自适应潜在预测加速（Adaptive Latent Prediction Acceleration）**利用泰勒级数展开和动态调节函数跳过去噪步骤以实现 6 倍推理加速，并通过**加权滑动窗口融合策略**确保长动画片段间的平滑过渡。

## 核心方法与创新机理

FlashPortrait 的核心创新并非提出全新的生成范式，而是针对当前基于 DiT 的人像动画模型（如 **Wan-Animate**）在长时域推理中面临的**身份一致性退化**与**推理速度瓶颈**，构建了一套训练无关（training-free）的推理加速框架。该方法通过三个相互协同的“changed slots”实现突破：归一化面部表达块（Normalized Facial Expression Block）锚定身份分布，加权滑动窗口策略（Weighted Sliding-Window Strategy）保障长时域平滑过渡，以及自适应潜在预测加速机制（Adaptive Latent Prediction Acceleration）实现多步去噪跳跃。

### 归一化面部表达块：身份分布的显式对齐

传统 DiT 人像动画模型通过图像交叉注意力（Image Cross-Attention）将参考图像特征注入潜变量，但面部表情特征与图像特征在分布中心和尺度上的差异会导致去噪过程中身份信息逐渐漂移。FlashPortrait 用归一化面部表达块替换标准图像交叉注意力块，其关键操作是**分布中心的显式对齐**：

$$
\bar{z}_i^{p} = \frac{z_i^{p} - \mu_p}{\sigma_p} \times \sigma_{img} + \mu_{img},\quad \bar{z}_i = \bar{z}_i^{p} + z_i^{img}
$$

其中 $z_i^{p}$ 是潜变量与面部表情嵌入的交叉注意力输出，$z_i^{img}$ 是潜变量与图像嵌入的交叉注意力输出。该操作将面部特征的均值 $\mu_p$ 和标准差 $\sigma_p$ 对齐到图像特征的统计量 $\mu_{img}$、$\sigma_{img}$，再通过逐元素相加融合两者。消融实验（Table 2）证实，这一设计是身份稳定性的决定性因素：移除归一化对齐（仅使用纯标准化或中心化）会导致 AED 指标显著恶化，而完整方案将 AED 从基线的 44.78 降至 29.68。

### 加权滑动窗口策略：长时域推理的平滑过渡

无限长人像动画需要将视频分割为片段（clip）逐段生成，但片段间的硬切换会引入视觉跳变。FlashPortrait 提出加权滑动窗口融合策略，对相邻窗口的重叠区域按帧索引感知的权重进行融合：

$$
z_i^{overlap} = W \cdot C_i + (1 - W) \cdot C_{i-1}
$$

其中 $W$ 随帧索引线性变化，确保当前窗口 $C_i$ 的贡献在重叠区逐渐过渡到前一窗口 $C_{i-1}$。消融实验（Table 3）表明，该策略相比运动帧（Motion Frame）和传统滑动窗口方法，在长动画中显著提升表情准确性，是实现“无限时长”生成的关键工程创新。

### 自适应潜在预测加速：训练无关的多步跳跃

这是 FlashPortrait 实现 6 倍加速的核心机制。其洞察在于：DiT 去噪过程中相邻时间步的潜变量具有高度可预测性，无需完整执行每一步去噪。方法利用泰勒级数展开，将未来时间步 $t$ 的潜变量 $f(t)$ 表示为当前步 $t+k$ 的潜变量及其高阶导数的函数：

$$
f(t) = \sum_{i=0}^{n} \frac{f^{(i)}(t+k)}{i!}(-k)^i + R_{n+1}
$$

为避免显式求导，使用有限差分 $\triangle^i f(t+k)$ 近似导数。在此基础上，引入两个动态调节函数以自适应控制预测精度：

- **时间步缩放因子** $s(t) = (\frac{\sigma(t)}{\sigma_{avg}(t)})^{\alpha}$（$\alpha=1.5$）：根据潜变量变化率动态调整跳跃步长 $K$。当潜变量变化剧烈时（$\sigma(t)$ 大），缩小步长以保证精度；变化平缓时，增大步长以加速。
- **层间缩放因子** $w(t,l,i) = \frac{1}{\sqrt{r(t,l,i)}}$，其中 $r(t,l,i) = \frac{\mathrm{E}[||f^{(i)}(t,l)||]}{\mathrm{E}[||f^{(i)}(t,avg)||]}$：根据 DiT 各层导数的相对幅度调整有限差分到导数的映射权重，层间导数幅度差异大时自动补偿。

最终预测公式为：

$$
f(t,l) = f(t+k,l) + \sum_{i=1}^{n} \frac{\triangle^i f(t+k,l) \cdot (-k)^i}{i! \cdot K^i \cdot w(t+k,l,i) \cdot s(t+k)}
$$

消融实验（Table 7）证实，移除动态函数 $s(t)$ 和 $w(t,l,i)$ 会导致性能显著下降，验证了自适应调节的必要性。参数消融（Table 5）表明 $K=5$ 和 $n=3$ 在质量与速度间取得最佳平衡。与缓存方法（**TeaCache**）和蒸馏方法（**Self-Forcing**）的对比（Table 4, Fig. 8）进一步显示：缓存方法加速有限，蒸馏方法虽加速高但引入伪影和身份不一致，而 FlashPortrait 的预测机制在 6 倍加速下仍保持视觉质量。

### 训练损失的小幅改进

作为辅助创新，FlashPortrait 在训练阶段使用面部和唇部掩码加权的 MSE 损失：

$$
\mathcal{L} = \mathbb{E}_{\theta} \left( \| (z_{gt} - z_{\varepsilon}) \odot (1 + M_{face} + M_{lip}) \|^2 \right)
$$

其中 $M_{face}$ 和 $M_{lip}$ 通过 MediaPipe 从视频帧中提取。该设计增强了对关键面部组件的学习，但消融证据的置信度相对较低（0.85），需手动验证其独立贡献。

**创新总结**：FlashPortrait 的三大 changed slots 形成因果链条——归一化面部表达块从结构层面锚定身份分布，加权滑动窗口从时序层面保障长程一致性，自适应潜在预测从计算层面实现训练无关加速。三者协同使得模型在 Hard100 长时域基准上相较 Wan-Animate 在 AED/APD/MAE 上分别提升 30.9%/30.4%/37.5%，同时推理速度提升 3 倍（Table 1），加速消融中达到 6 倍加速（Table 4）。

FlashPortrait 以 Wan2.1 视频扩散 Transformer 为骨干网络，构建了一个面向无限时长、身份保持的人像动画合成框架。其核心设计围绕三个层次展开：**身份稳定性增强**、**长时域平滑过渡**、以及**训练无关的推理加速**。整体架构如 Figure 2 所示，输入为一张参考图像和一段驱动视频，输出为与驱动视频表情同步且保持参考身份的长动画。

![[assets/figures/papers/paper_list_l988_https_arxiv_org_abs_2512_16900/figures/002_Figure_2.jpg]]
*Figure 2: Architecture of FlashPortrait. (a) and (b) refer to the structure of the Facial Expression Block and long-length video generation pipeline. Embeddings from the Image Encoder and Face Encoder are injected to each block of DiT. To speed up sliding window computation, each window predicts future latents from cached historical states, rather than invoking DiT for denoising*

### 模块构成与数据流

系统由六个关键模块串联而成：

1. **Face Encoder (PD-FGC)**：从驱动视频的每一帧中提取身份无关的面部表情特征，涵盖嘴部运动、头部位姿、眼部状态和情感表达。这些特征经 MLP 融合后生成人像嵌入 $emb_p$（Eq. 1）。

2. **Image Encoder (CLIP)**：从参考图像中提取身份相关的图像嵌入 $emb_{img}$，作为身份锚点贯穿整个生成过程。

3. **Normalized Facial Expression Block**：这是对 DiT 标准交叉注意力块的改造。在每一层 DiT 中，噪声潜变量 $z_i$ 分别与图像嵌入 $emb_{img}$ 和人像嵌入 $emb_p$ 进行交叉注意力计算，得到 $z_i^{img}$ 和 $z_i^{p}$。关键创新在于：将 $z_i^{p}$ 的分布中心对齐到 $z_i^{img}$ 的统计量上，再通过逐元素相加融合（Eq. 3）。这一归一化操作缩小了扩散潜变量与面部特征分布中心之间的距离，从而在去噪过程中稳定身份表征。

4. **Weighted Sliding-Window Strategy**：为突破单次推理的帧数限制，推理时采用滑动窗口机制将长视频切分为重叠的子片段分别去噪。相邻窗口的重叠区域通过帧索引感知的权重 $W$ 进行加权融合（Eq. 4），$W$ 随帧位置线性变化，确保片段间平滑过渡。重叠长度 $v$ 设为 5 帧（Algorithm 1）。

5. **Adaptive Latent Prediction Acceleration**：在滑动窗口推理过程中，利用已缓存的历史潜变量高阶导数，通过泰勒展开和有限差分近似预测未来时间步的潜变量，从而跳过大量 DiT 去噪步骤。预测公式中引入了两个动态调节函数——基于潜变量变化率的 $s(t)$（Eq. 12）和基于层间导数幅度比的 $w(t,l,i)$（Eq. 13）——以自适应控制预测精度。该机制仅在推理时激活，无需额外训练。

6. **Video Diffusion Transformer (Wan2.1 backbone)**：作为去噪骨干网络，接收上述条件嵌入和预测潜变量，迭代生成最终视频帧。训练时仅更新 DiT 的注意力模块参数，损失函数采用面部和唇部掩码加权的 MSE 重建损失（Eq. 16），掩码由 MediaPipe 从输入视频帧中提取。

### 推理流程

给定参考图像和驱动视频后，系统按以下步骤运行：
- Image Encoder 和 Face Encoder 分别提取身份嵌入和逐帧表情嵌入；
- 将长视频划分为固定长度的窗口，每个窗口内调用 DiT 进行去噪生成；
- 对每个窗口，自适应潜在预测机制利用历史潜变量预测部分时间步的潜变量，仅对剩余关键步执行完整去噪；
- 相邻窗口重叠区域通过加权融合实现无缝拼接；
- 最终输出与驱动视频等长的身份保持动画序列。

该框架的核心优势在于：归一化面部表达块从结构层面增强了身份稳定性，加权滑动窗口从时序层面保证了长动画的连贯性，自适应潜在预测从计算层面实现了 6 倍推理加速。三者协同工作，使得 FlashPortrait 在保持身份一致性的前提下，能够合成超过 1800 帧的无限时长动画。

FlashPortrait 的核心架构由四个关键模块构成：归一化面部表达块、加权滑动窗口策略、自适应潜在预测加速机制，以及面部掩码加权的训练损失。这些模块协同工作，在保持身份一致性的前提下实现 6 倍推理加速。

### 归一化面部表达块

该模块替换了标准 DiT 中的图像交叉注意力块，旨在对齐扩散潜变量与面部特征的分布中心，从而增强去噪过程中的身份稳定性。其处理流程如下：

首先，从驱动视频中提取身份无关的面部特征。嘴部嵌入 $emb_m$ 与头姿/眼睛/情感嵌入 $emb_{e*}$ 经拼接和 MLP 处理后得到人像嵌入：

$$emb_{m.e} = MLP(Concat(emb_m, emb_{e*})), \quad emb_p = Concat(FFN(SA(emb_m)), FFN(SA(emb_{e*})), emb_{m.e})$$

随后，扩散潜变量 $z_i$ 分别与图像嵌入 $emb_{img}$ 和人像嵌入 $emb_p$ 进行交叉注意力计算：

$$z_i^{img} = CA(z_i, emb_{img}), \quad z_i^{p} = CA(z_i, emb_p)$$

关键创新在于对 $z_i^{p}$ 进行归一化处理，使其统计特性与 $z_i^{img}$ 对齐，再逐元素相加：

$$\bar{z}_i^{p} = \frac{z_i^{p} - \mu_p}{\sigma_p} \times \sigma_{img} + \mu_{img}, \quad \bar{z}_i = \bar{z}_i^{p} + z_i^{img}$$

这一操作将人像特征的均值和标准差迁移至图像特征的分布空间，有效缩小了潜变量与原始面部嵌入分布中心之间的距离。消融实验证实，移除该归一化（使用纯标准化或中心化替代）会导致 AED 从 29.68 恶化至 44.78，身份和运动精度显著下降（Table 2）。

### 加权滑动窗口策略

为生成无限长人像动画，FlashPortrait 采用滑动窗口方式进行分片段推理。传统滑动窗口在片段交接处易产生不自然过渡，为此提出加权融合策略。

设相邻窗口的重叠区域长度为 $v$（实验中设为 5 帧），对重叠部分的潜变量按帧索引感知权重进行融合：

$$z_i^{overlapp} = W * C_i + (1 - W) * C_{i-1}$$

其中 $W$ 为随帧位置变化的权重向量，$C_i$ 和 $C_{i-1}$ 分别为当前窗口和前序窗口在重叠区域的潜变量。该策略动态融合相邻窗口，确保长动画片段间的平滑过渡。消融表明，加权滑动窗口在长动画中优于运动帧策略和传统滑动窗口，尤其在表情准确性上提升明显（Table 3）。

### 自适应潜在预测加速机制

这是 FlashPortrait 实现 6 倍推理加速的核心。其基本思想是利用历史去噪步骤的潜变量信息，预测未来时间步的潜变量，从而跳过大量 DiT 前向计算。

**泰勒展开与有限差分近似**：将潜变量随时间步的变化视为函数 $f(t)$，在 $a = t + k$ 处进行 $n$ 阶泰勒展开：

$$f(t) = \sum_{i=0}^{n} \frac{f^{(i)}(a)}{i!}(t-a)^i + R_{n+1}$$

由于扩散模型在离散时间步上运行，无法直接计算导数 $f^{(i)}(a)$。FlashPortrait 利用有限差分进行近似，将上式转化为：

$$f(t) = \sum_{i=0}^{n} \frac{\triangle^i f(t+k)}{i! K^i}(-k)^i + R_{n+1}$$

其中 $\triangle^i f(t+k)$ 为在 $t+k$ 处的 $i$ 阶有限差分，$K$ 为基础跳步间隔。该公式使得模型仅需缓存历史潜变量即可预测未来值，无需调用 DiT 进行完整去噪。

**动态时间步缩放函数 $s(t)$**：潜变量的变化速率在去噪过程中并非恒定。为自适应调整跳步幅度，引入基于潜变量变化率的动态缩放因子：

$$s(t) = \left(\frac{\sigma(t)}{\sigma_{avg}(t)}\right)^{\alpha}$$

其中 $\sigma(t)$ 为当前时间步的潜变量标准差，$\sigma_{avg}(t)$ 为滑动窗口内的平均标准差，$\alpha = 1.5$。当潜变量变化剧烈时，$s(t)$ 增大，减小有效跳步间隔，保证预测精度；变化平缓时则增大跳步幅度。

**动态层间缩放函数 $w(t,l,i)$**：DiT 不同层对潜变量的贡献幅度差异显著。为在各层间合理分配预测权重，定义层间缩放因子：

$$w(t,l,i) = \frac{1}{\sqrt{r(t,l,i)}}, \quad r(t,l,i) = \frac{\mathrm{E}[||f^{(i)}(t,l)||]}{\mathrm{E}[||f^{(i)}(t,avg)||]}$$

$r(t,l,i)$ 为第 $l$ 层第 $i$ 阶导数幅度与所有层平均幅度的比值。导数幅度较大的层获得较小的 $w$，从而在预测中权重更高。

**最终预测公式**：综合上述动态函数，得到最终的潜变量预测公式：

$$f(t,l) = f(t+k,l) + \sum_{i=1}^{n} \frac{\triangle^i f(t+k,l) \cdot (-k)^i}{i! \cdot K^i \cdot w(t+k,l,i) \cdot s(t+k)}$$

该公式完全训练无关，仅在推理时激活。消融实验表明，移除动态函数 $s(t)$ 和 $w(t,l,i)$ 会导致性能显著下降（Table 7）；参数 $K=5$、$n=3$ 在质量和速度之间取得最佳平衡（Table 5）。

### 面部掩码加权训练损失

为提升面部关键区域的重建质量，FlashPortrait 在训练时引入面部和唇部掩码加权的 MSE 损失：

$$\mathcal{L} = \mathbb{E}_{\theta} \left( \| (z_{gt} - z_{\varepsilon}) \odot (1 + M_{face} + M_{lip}) \|^2 \right)$$

其中 $M_{face}$ 和 $M_{lip}$ 通过 MediaPipe 从输入视频帧中提取，$z_{gt}$ 为真实潜变量，$z_{\varepsilon}$ 为噪声潜变量。该损失使模型更关注面部和唇部区域的像素重建，进一步提升身份保持和表情准确性。训练时仅更新 DiT 的注意力模块参数。

## 实验与关键发现

### 核心定量结果

FlashPortrait 在两个互补的测试基准上与现有方法进行了全面对比：Voxceleb2&Vfhq（平均时长10秒，评估短时动画质量）和 Hard100（平均时长1分钟，评估长时身份保持能力）。Hard100 数据集包含100个具有大幅度头部运动、复杂表情和遮挡的驱动视频，专门用于考验模型在极端条件下的身份保持性能（示例见 Figure 7）。

![[assets/figures/papers/paper_list_l988_https_arxiv_org_abs_2512_16900/figures/011_Figure_7.jpg]]
*Figure 7: Examples from Hard100*

**Table 1** 报告了主要定量结果。在 Hard100 基准上，FlashPortrait 相比最新的 DiT 基人像动画模型 **Wan-Animate**，在三个核心指标上取得了显著提升：AED 降低 30.9%（29.68 vs 42.98），APD 降低 30.4%，MAE 降低 37.5%（12.54 vs 20.08）。在 Voxceleb2&Vfhq 上同样保持优势。值得注意的是，FlashPortrait 在所有 DiT 基方法中实现了最快的推理速度——生成一段20秒的480×832视频仅需720秒，而 Wan-Animate 需要2298秒（约3.2倍加速）。基于 GAN 的 **LivePortrait** 虽然速度极快（约1秒），但其身份保持和运动精度指标显著劣于 FlashPortrait。基于 UNet 的扩散方法（**X-Portrait**、**FollowYE**）和基于 3D Morphable Model 的 **Skyreels-A1** 同样在各项指标上被 FlashPortrait 超越。

用户偏好研究（**Table 6**）进一步验证了定量结果：在长期身份保持（L-A）维度上，用户对 FlashPortrait 的偏好率达到 92.8%（vs Wan-Animate 7.2%）；在面部表情准确性、唇同步和运动平滑度上，偏好率均超过 90%。

![[assets/figures/papers/paper_list_l988_https_arxiv_org_abs_2512_16900/figures/010_Table_6.jpg]]
*Table 6: User preference of FlashPortrait compared with other competitors. Higher indicates users prefer more to our model*

### 消融实验

#### 归一化面部表达块

**Table 2** 消融了归一化面部表达块的设计选择。基线方法（直接相加 $z_i^p + z_i^{img}$）在 Hard100 上的 AED 为 44.78。仅使用纯标准化（Pure Norm）或中心化（Centralization）均无法有效对齐潜变量与面部特征的分布中心，性能改善有限。本文提出的完整归一化方案——将人像交叉注意力输出归一化到图像特征的均值和标准差后再相加（Eq. 3）——将 AED 降至 29.68，验证了分布中心对齐对身份稳定性的关键作用。

#### 长视频片段过渡策略

**Table 3** 比较了三种长视频生成策略。运动帧策略（Motion Frame）使用前一窗口的最后一帧作为新窗口的起始帧，缺乏平滑过渡机制；传统滑动窗口策略（Sliding Window）直接拼接相邻窗口，在重叠区域产生不连续。本文提出的加权滑动窗口融合策略（Eq. 4, Algorithm 1）通过帧索引感知的权重 $W$ 对相邻窗口的重叠区域进行加权融合，在 APD 和 MAE 上均取得最优结果，尤其显著提升了长动画中的表情准确性。

#### 自适应潜在预测加速

加速方法的消融实验（**Figure 5 / Table 4**）对比了多种加速策略。缓存方法 **TeaCache** 加速幅度有限，**FoCa** 虽加速更多但导致身份不一致。蒸馏方法 **Self-Forcing** 可实现高倍加速，但引入明显伪影和身份漂移（见 Figure 8）。FlashPortrait 的自适应潜在预测加速在达到6倍推理加速的同时，视觉质量未出现明显下降，在加速比与质量保持之间取得了最佳平衡。

![[assets/figures/papers/paper_list_l988_https_arxiv_org_abs_2512_16900/figures/007_Figure_5.jpg]]
*Figure 5: Ablation study on acceleration*

![[assets/figures/papers/paper_list_l988_https_arxiv_org_abs_2512_16900/figures/013_Figure_8.jpg]]
*Figure 8: Ablation study on different acceleration methods. w/o DF refers to w/o Dynamic Functions*

动态函数的必要性在 **Table 7** 中得到验证。移除时间步动态缩放函数 $s(t)$（Eq. 12）或层间动态缩放函数 $w(t,l,i)$（Eq. 13）均导致性能显著下降，表明根据潜变量变化率和各层导数幅度自适应调整预测对维持生成质量至关重要。

![[assets/figures/papers/paper_list_l988_https_arxiv_org_abs_2512_16900/figures/012_Table_7.jpg]]
*Table 7: Ablation study on different weight assignment*

**Table 5** 探索了关键超参数 $K$（预测跳步数）和 $n$（泰勒展开阶数）的影响。实验表明 $K=5$ 和 $n=3$ 在推理速度与生成质量之间达到最佳平衡。过大的 $K$ 值虽进一步加速，但预测误差累积导致面部扭曲；过高的 $n$ 阶数增加计算开销而边际收益递减。

#### 训练损失

使用面部和唇部掩码加权的重建损失（Eq. 16）进一步提升了面部区域的保真度（Sec. 3.4），该结论来自消融实验，但具体数值需查阅原文确认。

### 失败模式

FlashPortrait 在非真实人形角色（如游戏化身、神话人物）的身份保持上存在困难。如 **Figure 16** 所示，当参考图像为风格化或非写实人脸时，模型倾向于将其合成为更真实的人脸外观，导致身份特征丢失。作者指出这可能需要引入额外的参考网络来专门处理非真实人形角色的身份保持。此外，模型训练需要大量计算资源（200 H100 GPU），限制了社区复现和进一步探索的可行性。

## 定位与知识库关联

### 问题域与基线关系

FlashPortrait 解决的是**长时域、身份保持的无限人像动画生成**问题，核心瓶颈在于：现有扩散模型（尤其是基于 DiT 的模型）在长序列生成中面临身份漂移、颜色偏移和面部扭曲，同时推理速度慢，难以满足实时应用需求。

在方法谱系上，FlashPortrait 直接对标以下基线：

- **Wan-Animate**：基于 DiT 的最新开源人像动画模型，是 FlashPortrait 的直接骨干和主要对比对象。FlashPortrait 在其基础上引入三个关键改造：归一化面部表达块、加权滑动窗口融合、自适应潜在预测加速。在 Hard100 数据集上，FlashPortrait 相较 Wan-Animate 在 AED/APD/MAE 上分别提升 30.9%/30.4%/37.5%，同时推理速度快 3 倍（Table 1）。
- **HunyuanPortrait** 与 **FantasyPortrait**：同为 DiT 系人像动画模型，FlashPortrait 在定量指标和推理速度上均显著优于它们。
- **LivePortrait**：基于 GAN 的方法，推理速度快但身份保持和表情准确性弱于 FlashPortrait。
- **Skyreels-A1**：基于 3D Morphable Model 的扩散方法，在长期身份保持上表现较差。
- **X-Portrait** 与 **FollowYE**：基于 UNet 的扩散方法，属于较早的技术路线，在生成质量和速度上均不占优。

### 加速方法谱系中的定位

FlashPortrait 的加速机制属于**训练无关的推理时加速**，与以下方法形成对比：

- **TeaCache** 和 **FoCa**：基于缓存的方法。消融实验（Table 4）表明，缓存方法加速有限，而 FlashPortrait 的自适应潜在预测可达到 6 倍加速，且视觉质量损失最小。
- **Self-Forcing**：基于蒸馏的加速方法。虽然加速比高，但消融显示其会导致伪影和身份不一致（Figure 8），而 FlashPortrait 在加速与质量之间取得了更好的平衡。

FlashPortrait 的核心洞察在于：利用泰勒级数展开和有限差分在 DiT 层上近似潜变量导数，并根据潜在变化率和层间衍生物大小比例自适应调整预测，从而安全地跳过多步去噪。这种思路与简单的缓存或蒸馏有本质区别——它不是复用历史结果，而是**预测未来潜变量**，并通过动态函数 $s(t)$ 和 $w(t,l,i)$ 控制预测风险。

### 适用边界

1. **真实人像场景表现最佳**：FlashPortrait 在真实人脸动画上展现了强大的身份保持能力，用户研究中长期身份保持的偏好率达 92.8%（Table 6）。
2. **非真实人形角色存在困难**：论文明确指出的失败案例（Figure 16）表明，对于游戏化身、神话人物等非真实人形角色，模型倾向于合成更真实的人脸，身份保持能力下降。作者提出引入额外参考网络作为潜在解决方案，但尚未实现。
3. **计算资源需求高**：训练需要 200 块 H100 GPU，对资源受限的研究团队不友好。

### 局限与开放问题

1. **非真实人形角色的身份保持**：这是论文明确承认的局限。如何在不牺牲真实人像性能的前提下，扩展模型对非真实角色的泛化能力，是一个开放问题。
2. **自适应潜在预测的泛化性**：该方法在 DiT 骨干上验证有效，但其在更广泛视频生成任务（如通用视频生成、多主体场景）中的适用性尚未探索。
3. **加速上限与质量边界**：消融实验表明 $K=5, n=3$ 是最佳平衡点（Table 5），但更激进的加速设置下性能退化规律尚未系统研究。
4. **训练损失中面部掩码的贡献**：论文提到使用加权面部和唇部掩码的 MSE 损失（Eq. 16）可提升面部区域保真度，但该消融的置信度标注为 0.85，需手动验证其独立贡献是否被充分量化。

### 知识库定位

FlashPortrait 在人像动画领域贡献了两个可迁移的技术模块：

1. **归一化面部表达块**：通过对齐潜变量与面部特征的分布中心（Eq. 3），增强跨帧身份稳定性。消融实验（Table 2）证实，移除该模块会使 AED 从 29.68 恶化至 44.78。这一思路可推广到其他需要身份保持的生成任务。
2. **自适应潜在预测加速**：训练无关、即插即用的推理加速机制，为扩散模型的推理效率优化提供了不同于缓存和蒸馏的新范式。其动态函数设计（Eq. 12-13）体现了对去噪过程中时间步和层间差异的精细建模。

## 原文 PDF

![[paperPDFs/CVPR_2026/FlashPortrait_6x_Faster_Infinite_Portrait_Animation_with_Adaptive_Latent_Prediction.pdf]]
