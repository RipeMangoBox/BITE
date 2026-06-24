---
title: "Mango-GS: Enhancing Spatio-Temporal Consistency in Dynamic Scenes Reconstruction using Multi-Frame Node-Guided 4D Gaussian Splatting"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/Mango_GS_Enhancing_Spatio_Temporal_Consistency_in_Dynamic_Scenes_Reconstruction_df1c4f8104b2.pdf
project_link: null
code_link: null
aliases:
- MG
- Mango-GS
tags:
- ICLR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
core_operator: 将稀疏控制节点解耦为规范位置与潜在特征代码，并在多帧时间窗口上施加时间注意力，使模型能够推断运动趋势，生成物理上连贯的节点轨迹，再通过语义感知的k-NN将运动传播至密集高斯云。
primary_logic: 通过解耦控制节点的空间位置与语义特征代码，建立基于学习的联合位置-特征空间邻域，从而在大幅度形变下依然保持稳定的运动传播对应关系，避免传统空间k-NN因大运动导致的邻域漂移。
claims:
- 提出解耦控制节点表示，将空间位置与潜在特征代码分离，以稳定运动传播并防止大运动下的对应漂移。
- 设计多帧时间注意力网络，学习控制节点在时间窗口内的运动动力学，取代逐帧变形。
- 节点影响力权重通过可学习MLP在联合位置-特征空间中计算，形成语义感知邻域。
- 时间输入掩码策略与运动感知损失共同训练，提升模型的时间鲁棒性。
---

# Mango-GS: Enhancing Spatio-Temporal Consistency in Dynamic Scenes Reconstruction using Multi-Frame Node-Guided 4D Gaussian Splatting

> [!tip] 核心洞察
> 通过解耦控制节点的空间位置与语义特征代码，建立基于学习的联合位置-特征空间邻域，从而在大幅度形变下依然保持稳定的运动传播对应关系，避免传统空间k-NN因大运动导致的邻域漂移。

| 字段 | 内容 |
|------|------|
| 中文题名 | Mango-GS：利用多帧节点引导4D高斯溅射增强动态场景重建的时空一致性 |
| 英文题名 | Mango-GS: Enhancing Spatio-Temporal Consistency in Dynamic Scenes Reconstruction using Multi-Frame Node-Guided 4D Gaussian Splatting |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=N4VKlSxCLc) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction |
| Method | Mango-GS |
| Dataset | Neural 3D Video, HyperNeRF-vrig |

> [!tip] 效果简介
> - Neural 3D Video 上，PSNR 31.89 vs 未提供具体对比值 (达到最高)。
> - HyperNeRF-vrig 上，PSNR / MS-SSIM / tLPIPS 26.2 / 0.78 / 0.0196 vs 未提供具体对比值 (三项指标均为最优)；FPS / Storage (MB) 149.5 / 60 vs 未提供具体对比值 (实时渲染，存储量较低)。
> - HyperNeRF-vrig (效率对比) 上，速度与tLPIPS/MS-SSIM 速度比MotionGS与TimeFormer快3倍以上，同时tLPIPS和MS-SSIM更优 vs MotionGS, TimeFormer (3× 加速 + 更好的时间一致性)。

## 概述

动态场景的神经渲染面临一个核心瓶颈：现有4D高斯溅射（4DGS）方法普遍采用**逐帧独立优化**策略，模型倾向于记忆每一帧的瞬时外观，而非学习底层的运动规律。这导致在快速或复杂运动场景下，渲染结果出现时间不一致、模糊和伪影，严重制约了动态重建的时空一致性。

**Mango-GS** 针对这一瓶颈，提出了一套以稀疏控制节点为中枢的多帧运动建模框架。其核心洞察在于：将控制节点解耦为**规范空间位置**与**可学习潜在特征代码**两个独立成分，从而在联合位置-特征空间中建立语义感知的邻域关系。这一设计使得在高斯点云与节点之间进行运动传播时，能够避免传统纯空间k-NN因大幅度形变而导致的邻域漂移问题（见图2）。在此基础上，Mango-GS引入**多帧时间注意力网络**，在固定时间窗口内对节点轨迹进行联合推理，使模型能够捕获运动趋势并生成物理上连贯的变形序列。

在方法谱系中，Mango-GS属于**节点引导的动态高斯溅射**范式，与SC-GS等采用稀疏控制节点驱动密集高斯的工作一脉相承，但通过解耦节点表示、学习型k-NN关联和多帧时间Transformer三项关键改进，显著提升了运动建模的鲁棒性。相比于**4D Gaussians**（Wu et al., CVPR 2024）的时空编码方案和**Deformable 3DGS**（Yang et al., CVPR 2024）的逐帧变形网络，Mango-GS将时间建模从像素/高斯级提升到节点级，兼顾了效率与时间一致性。

实验表明，Mango-GS在Neural 3D Video和HyperNeRF-vrig两个公开基准上均取得最优结果。在HyperNeRF-vrig数据集上，PSNR达26.2，MS-SSIM达0.78，tLPIPS低至0.0196，同时以149.5 FPS实现实时渲染，存储量仅60 MB。消融实验证实，解耦节点表示、时间注意力网络、top-k硬帧损失和运动感知损失的逐步引入持续提升各项指标，时间窗口T=6和邻居数K=3为最优配置。与MotionGS和TimeFormer相比，Mango-GS在速度上快3倍以上，同时保持更优的时间一致性。

**局限性**方面，当前固定时间窗口难以捕获超过T=6帧的长程运动依赖；在极端非刚性形变下，节点-高斯的语义邻域仍可能出现传播误差；尚未验证在在线流式长视频场景下的适应性。这些方向为后续工作留下了明确的改进空间。

## 背景与动机

### 动态场景重建的核心矛盾

动态场景重建的目标是从多视角视频中同时恢复场景几何、外观和运动信息。近年来，3D高斯溅射（3DGS）凭借其显式表示和实时渲染能力，已成为静态场景重建的事实标准。然而，将其扩展至动态场景时，一个根本性瓶颈逐渐暴露：**现有方法普遍采用逐帧优化策略，模型倾向于记忆每一帧的瞬时外观，而非学习底层的运动规律**。

具体而言，以 **Deformable 3DGS**（Yang et al., CVPR 2024）和 **D-3DGS**（Luiten et al., 3DV 2024）为代表的可变形高斯方法，通过逐帧MLP预测每个高斯的平移、旋转和缩放。这种设计虽然灵活，但缺乏对帧间运动连续性的显式约束，导致在快速或复杂运动下出现**时间不一致、运动模糊和闪烁伪影**。类似地，**4D Gaussians**（Wu et al., CVPR 2024）虽引入4D时空编码，但其变形预测仍以单帧为粒度，未能充分建模跨帧运动依赖。

### 现有运动建模范式的局限性

为缓解上述问题，研究者提出了两类改进思路：

1. **节点引导范式**：**SC-GS**等方法引入稀疏控制节点，通过空间k近邻（k-NN）将节点运动传播至密集高斯云。这种设计将运动建模从“逐高斯”降维至“逐节点”，显著提升了效率。但其关键缺陷在于：**节点-高斯关联仅依赖纯空间欧氏距离**。在大幅度形变下，高斯可能漂移至空间邻近但语义无关的节点邻域，导致运动传播的对应关系断裂（参见Figure 2）。

2. **显式时间建模范式**：**TimeFormer**将跨时间Transformer应用于可变形高斯，显式建模帧间关系；**MotionGS**（Zhu et al., NeurIPS 2024）引入显式运动引导。这些方法虽提升了时间一致性，但时间建模直接作用于密集高斯或全局特征，计算开销较高，且未与节点引导的高效传播机制结合。

### 本文动机与核心思路

上述分析揭示了一个关键洞察：**动态场景重建的核心挑战不在于“能否变形”，而在于“如何在大运动下维持稳定的运动传播对应关系”**。

Mango-GS的动机由此展开——通过三个层面的设计突破现有瓶颈：

- **解耦控制节点表示**：将控制节点从单一的3D位置解耦为“规范位置 + 可学习特征代码”，建立基于学习的联合位置-特征空间邻域。这使得节点-高斯关联不仅考虑空间邻近性，更捕捉语义一致性，从而在大幅度形变下保持稳定的对应关系。

- **多帧时间注意力建模**：将运动建模从逐帧独立预测提升为窗口级联合推理。通过在节点级时间窗口上施加自注意力，使模型能够捕获运动趋势和长程依赖，生成物理上连贯的节点轨迹。

- **运动感知训练策略**：通过时间输入掩码策略和组合损失函数（硬帧光度损失 + 运动感知损失），强制模型学习时序鲁棒的运动表示，而非过拟合于特定帧的外观。

这一设计将时间建模的计算负载限制在稀疏节点集上（默认2048个初始节点），同时通过语义感知的k-NN将运动高效传播至密集高斯云，在保持实时渲染能力的前提下，显著提升了动态场景的时空一致性。

## 核心创新

Mango‑GS 的核心创新在于**将动态场景的运动建模从“逐帧记忆”转向“节点级时序推理”**。现有 4D 高斯溅射方法（如 **4D Gaussians**（Wu et al., CVPR 2024）、**Deformable 3DGS**（Yang et al., CVPR 2024））普遍采用逐帧 MLP 预测每个高斯的变形，模型倾向于记忆每一帧的瞬时外观，而非学习底层的运动规律。这导致在快速或复杂运动下出现时间不一致、模糊和伪影。Mango‑GS 通过三个相互耦合的机制设计，系统性地改变了这一范式。

### 1. 解耦控制节点表示：从空间锚点到语义锚点

传统节点引导方法（如 **SC‑GS**）仅使用控制节点的 3D 空间位置来建立与高斯的关联。在大幅度形变下，这种纯空间 k‑NN 关联会发生“邻域漂移”——高斯在变形后可能被关联到语义上不相关的节点，导致运动传播错误。

Mango‑GS 将每个控制节点解耦为 **规范位置 $p_i$ 与可学习特征代码 $f_i$** 两部分：

> “Each control node $n_i = (p_i, f_i)$ is a decoupled entity composed of a canonical position $p_i$ and a learnable feature code $f_i$.”

这一设计的因果机制是：特征代码通过端到端训练，编码了节点所在区域的语义与运动属性。在联合位置‑特征空间中计算高斯与节点的距离，使得关联权重不仅依赖空间邻近性，更依赖运动语义的一致性。**Figure 2** 的可视化直接验证了这一点——在高运动区域，解耦节点能保持语义一致的邻域，而纯空间节点则因大运动而漂移到不相关区域。

### 2. 多帧时间注意力网络：从逐帧预测到窗口级运动推理

现有方法的变形预测是逐帧独立的，每帧的变形仅由当前时间戳驱动，缺乏对运动趋势的显式建模。Mango‑GS 提出**在控制节点层面对整个时间窗口进行联合推理**：

> “We apply a multi‑frame temporal Transformer to model the dynamics of control nodes for Gaussian Splatting.”

时间注意力网络 $\Phi$ 接收所有节点的规范位置和 $T$ 个连续时间戳，通过 MLP 骨架与时间自注意力块（**Figure 3**）一次性输出窗口内所有帧的节点位移、旋转和缩放：

$$\{\Delta p_i(t), \Delta q_i(t), \Delta s_i(t)\}_{t=0}^{T-1} = \Phi(\{p_i\}_{i=1}^{M}, \{t\}_{t=0}^{T-1}; \Theta)$$

时间自注意力沿时间轴对每个节点独立执行多头注意力，捕获长程时间依赖：

$$H_{\mathrm{attn}} = \mathrm{MHA}(H_{\mathrm{in}}^{(l)}, H_{\mathrm{in}}^{(l)}, H_{\mathrm{in}}^{(l)})$$

并通过可学习的门控机制自适应融合时序信息：

$$H^{(l+1)} = H^{(l)} \otimes (\sigma(w_{\mathrm{gate}})) + w_{\mathrm{bias}}$$

这一设计的核心优势在于：**模型能够观察到相邻帧之间的运动趋势**，从而生成物理上连贯的节点轨迹，而非孤立地拟合每一帧。

### 3. 学习型 k‑NN 关联与运动传播

节点到高斯的关联权重在联合位置‑特征空间中通过可学习 MLP 计算，并经 softmax 归一化：

$$w_{ij} = \frac{\exp(-\mathcal{D}(g_j, n_i))}{\sum_{i' \in \mathcal{K}(j)} \exp(-\mathcal{D}(g_j, n_{i'}))}, \quad \forall i \in \mathcal{K}(j)$$

其中 $\mathcal{D}$ 是联合空间中的距离度量。每个高斯的变形由其 $k$ 个最相关节点的变形加权混合得到：

$$\{\Delta(x_j)(t)\}_{t=0}^{T-1} = \sum_{i \in \mathcal{K}(j)} w_{ij} \Delta p_i \in \{\Delta p_i(t)\}_{t=0}^{T-1}$$

这种语义感知的 k‑NN 机制，使得即使在大幅度非刚性形变下，运动传播的对应关系依然稳定——这是纯空间 k‑NN 无法保证的。

### 4. 训练策略增强：时间掩码与运动感知损失

为进一步提升模型的时间鲁棒性，Mango‑GS 引入了两个辅助机制：

- **时间输入掩码**：训练时随机掩码部分输入时间嵌入，迫使网络从可见帧推断缺失帧的运动，降低对特定时间戳的过拟合。
- **运动感知损失**：在传统光度损失之外，引入时序差分损失 $\mathcal{L}_{\mathrm{diff}}$、运动幅度损失 $\mathcal{L}_{\mathrm{amp}}$ 和运动方向损失 $\mathcal{L}_{\mathrm{dir}}$，强制模型生成时间连贯且物理合理的运动：

$$\mathcal{L}_{\mathrm{motion}} = \lambda_{\mathrm{diff}} \mathcal{L}_{\mathrm{diff}} + \lambda_{\mathrm{amp}} \mathcal{L}_{\mathrm{amp}} + \lambda_{\mathrm{dir}} \mathcal{L}_{\mathrm{dir}}$$

整体损失为组合形式：

$$\mathcal{L} = 0.8 \times \mathcal{L}_{\mathrm{frame}} + 0.2 \times \mathcal{L}_{\mathrm{motion}}$$

### 创新总结

| 设计维度 | 基线方法 | Mango‑GS 创新 |
|---------|---------|-------------|
| 控制节点表示 | 纯空间 3D 位置 | 解耦为位置 + 可学习特征代码 |
| 运动建模粒度 | 逐帧独立预测 | 多帧窗口联合推理（时间注意力） |
| 节点‑高斯关联 | 空间欧氏距离 k‑NN | 联合位置‑特征空间学习型 k‑NN |
| 时间增强 | 无 | 随机时间掩码 |
| 损失函数 | 逐帧光度损失 | 组合损失（硬帧光度 + 运动感知） |

**组件消融实验（Table 3）** 直接验证了上述创新的累积效果：逐步加入解耦节点表示、时间注意力网络、硬帧损失和运动损失，PSNR、SSIM、LPIPS 和 tLPIPS 均持续提升。

## 整体框架

Mango-GS 将动态场景建模为**规范空间 3D 高斯点云的可变形表示**。其核心管线由五个模块串联构成：解耦控制节点初始化、学习型 k-NN 关联、时间注意力网络、高斯变形传播以及可微分渲染。整个模型以端到端方式优化，训练时引入时间输入掩码策略与组合损失函数。

### 管线总览

**Figure 1** 展示了 Mango-GS 的完整框架。管线从一组稀疏的**解耦控制节点**（decoupled control nodes）出发，每个节点同时携带规范位置与可学习的潜在特征代码。密集的 3D 高斯云通过基于联合位置-特征空间的**学习型 k-NN 机制**与这些节点建立关联，形成语义感知邻域。随后，**时间注意力网络**接收所有节点的规范位置和一个时间窗口 $[0, T]$ 作为输入，经 MLP 层与时间自注意力块处理后，一次性预测整个窗口内所有节点的位移、旋转与缩放。学习到的节点运动通过预计算的 k-NN 权重**传播回高斯云**，生成每一帧的动态场景表示。最终经可微分高斯溅射渲染与真值比较，驱动端到端优化。

### 模块关系与数据流

1. **解耦控制节点初始化**：在规范空间中初始化 $M$ 个控制节点 $n_i = (p_i, f_i)$，其中 $p_i \in \mathbb{R}^3$ 为规范位置，$f_i \in \mathbb{R}^d$ 为可学习特征代码。节点数默认 $M = 2048$，训练中会通过剪枝进一步精简至约 1420 个有效节点。

2. **学习型 k-NN 关联**：对每个高斯 $g_j$，在联合位置-特征空间中计算其与所有节点的距离，选取 $K$ 个最相关节点构成邻域 $\mathcal{K}(j)$，并通过可学习 MLP 与 softmax 计算归一化影响力权重 $w_{ij}$（公式 3）。这一设计使高斯能够稳定地依附于语义一致的节点，避免纯空间 k-NN 在大运动下因邻域漂移导致的对应失效（**Figure 2**）。

3. **时间注意力网络**：网络 $\Phi$ 以所有节点的规范位置 $\{p_i\}_{i=1}^M$ 和 $T$ 个时间戳 $\{t\}_{t=0}^{T-1}$ 为输入，经 MLP 骨架与时间自注意力块交替处理后，一次性输出每个节点在窗口内的位移、旋转和缩放序列（公式 4）。**Figure 3** 展示了该网络的内部架构：沿时间轴执行多头自注意力捕获长程依赖，并通过轻量门控机制自适应融合时序信息（公式 6-7）。

4. **高斯变形传播**：每个高斯 $g_j$ 在时刻 $t$ 的变形由其 $K$ 个语义邻域节点的变形加权混合得到（公式 5）。旋转与缩放变换同理传播，最终生成逐帧动态高斯云。

5. **可微分渲染**：变形后的高斯云经 alpha 合成渲染（公式 2），与真值图像计算组合损失 $\mathcal{L} = 0.8 \times \mathcal{L}_{\text{frame}} + 0.2 \times \mathcal{L}_{\text{motion}}$（公式 8-9），驱动反向传播优化全部可学习参数。

### 输入输出规范

- **输入**：多视角视频序列的标定图像与对应时间戳。
- **输出**：任意时刻、任意视角的渲染图像，以及底层动态高斯云表示。
- **训练窗口**：默认 $T = 6$ 帧，采用稀疏步进采样器与插值采样器交替的多帧组采样策略（**Figure 6**），比例 $0.7:0.3$ 时取得最佳时间一致性。
- **时间增强**：训练时随机掩码部分输入时间嵌入，作为正则化手段抑制时序过拟合。
- **硬件与效率**：单块 NVIDIA RTX 3090 上完成两阶段训练（5000 + 35000 次迭代），推断速度达 149.5 FPS，存储量仅 60 MB。

> **注意**：上述管线描述中的公式编号、图表引用均来自原文。若需查看具体公式形式，请参见“公式体系”章节；定性渲染对比见 **Figure 4**（Neural 3D Video）与 **Figure 5**（HyperNeRF）。

![[assets/figures/papers/paper_list_l3_https_openreview_net_forum_id_N4VKlSxCLc/figures/004_Figure_4.jpg]]
*Figure 4: Visualization comparison between baselines and our methods from the Neural 3D Video dataset. The main differences are highlighted and zoomed in with boxes*

### 补充图表

![[assets/figures/papers/paper_list_l3_https_openreview_net_forum_id_N4VKlSxCLc/figures/001_Figure_1.jpg]]
*Figure 1: An overview of the Mango-GS framework. Our method is driven by a set of decoupled control nodes, each comprising a canonical position and a feature code. A dense 3D Gaussian cloud is associated with these nodes via a learned k-NN relationship based on both position and features. A temporal attention network takes the canonical node positions and a time window [0, T ] as input, processing them through MLP layers and temporal attention blocks to predict the nodes’ deformations over the entire time window. This learned motion is then propagated back to the Gaussian cloud to produce the final dynamic scene representation for each frame. The entire model is optimized end-to-end with a temporal i...*

## 核心模块与公式推导

Mango-GS将动态场景建模为规范3D高斯点云的变形，其核心设计围绕三个关键模块展开：解耦控制节点表示、学习型k-NN关联机制，以及多帧时间注意力网络。以下逐一剖析各模块的数学表述与设计动机。

### 3D高斯溅射基础

场景由一组3D高斯表示，每个高斯的空间分布由均值 $\mu$ 和协方差矩阵 $\Sigma$ 参数化：

$$G(x) = \exp\bigl(-\frac{1}{2}(x-\mu)^{\top}\Sigma^{-1}(x-\mu)\bigr)$$

渲染时，将 $N$ 个高斯按从前到后的顺序进行alpha合成，得到像素颜色 $C$：

$$C = \sum_{i=1}^{N} c_i \alpha_i' \prod_{j=1}^{i-1} (1 - \alpha_j')$$

其中 $c_i$ 为第 $i$ 个高斯的颜色，$\alpha_i'$ 为经协方差投影后的有效不透明度。这一可微分渲染管线构成所有后续变形建模的末端。

### 解耦控制节点表示

传统节点引导方法（如SC-GS）仅使用控制节点的3D空间位置来建立与高斯的关联，在剧烈运动下容易发生邻域漂移——即高斯在变形后可能被错误地关联到空间邻近但语义无关的节点上。Mango-GS的解决方案是将每个控制节点 $n_i$ 解耦为两个独立成分：

$$n_i = (p_i, f_i)$$

其中 $p_i \in \mathbb{R}^3$ 为规范空间位置，$f_i \in \mathbb{R}^d$ 为可学习的潜在特征代码。这一解耦使得节点同时具备空间锚定能力和语义表征能力，为后续在联合空间中建立稳定的运动传播对应关系奠定了基础。

### 学习型k-NN关联机制

每个高斯 $g_j$ 需要与 $k$ 个最相关的控制节点建立关联。Mango-GS在联合位置-特征空间中计算高斯与节点之间的距离 $\mathcal{D}(g_j, n_i)$，并通过可学习MLP对该距离进行自适应映射。对于高斯 $g_j$ 的 $k$ 个最近邻节点集合 $\mathcal{K}(j)$，影响力权重通过softmax归一化得到：

$$w_{ij} = \frac{\exp(-\mathcal{D}(g_j, n_i))}{\sum_{i' \in \mathcal{K}(j)} \exp(-\mathcal{D}(g_j, n_{i'}))}, \quad \forall i \in \mathcal{K}(j)$$

这一权重 $w_{ij}$ 度量了节点 $n_i$ 对高斯 $g_j$ 变形的贡献比例。与纯空间k-NN相比，联合空间中的邻域选择对大幅度形变具有更强的鲁棒性，因为即使空间位置发生显著变化，语义特征的一致性仍能维持正确的节点-高斯对应关系。

### 多帧时间注意力网络

Mango-GS的运动建模核心是一个时间注意力网络 $\Phi$，它以所有 $M$ 个控制节点的规范位置 $\{p_i\}_{i=1}^{M}$ 和 $T$ 个时间戳 $\{t\}_{t=0}^{T-1}$ 作为输入，一次性预测整个时间窗口内每个节点的位移 $\Delta p_i$、旋转 $\Delta q_i$ 和缩放 $\Delta s_i$：

$$\{\Delta p_i(t), \Delta q_i(t), \Delta s_i(t)\}_{t=0}^{T-1} = \Phi(\{p_i\}_{i=1}^{M}, \{t\}_{t=0}^{T-1}; \Theta)$$

网络内部结构由MLP骨架与时间自注意力块交错堆叠而成。对于第 $l$ 层的输入特征 $H_{\text{in}}^{(l)}$，沿时间轴执行多头自注意力：

$$H_{\text{attn}} = \text{MHA}(H_{\text{in}}^{(l)}, H_{\text{in}}^{(l)}, H_{\text{in}}^{(l)})$$

注意力输出通过轻量级门控机制自适应地融入主流特征：

$$H^{(l+1)} = H^{(l)} \otimes (\sigma(w_{\text{gate}})) + w_{\text{bias}}$$

其中 $\sigma$ 为sigmoid激活函数，$w_{\text{gate}}$ 和 $w_{\text{bias}}$ 为可学习参数。门控设计使网络能够选择性保留或更新各时间步的特征，避免注意力引入的噪声破坏原有表示。最终解码层将处理后的特征映射为各节点在所有 $T$ 帧上的变形参数。

### 变形传播与渲染

获得节点变形后，每个高斯 $g_j$ 的变形通过其 $k$ 个关联节点的位移加权求和得到：

$$\{\Delta(x_j)(t)\}_{t=0}^{T-1} = \sum_{i \in \mathcal{K}(j)} w_{ij} \Delta p_i \in \{\Delta p_i(t)\}_{t=0}^{T-1}$$

旋转和缩放的传播采用类似的对数映射加权混合策略。变形后的高斯云可直接通过前述可微分渲染管线生成任意视角的图像。

### 训练损失函数

Mango-GS采用组合损失函数进行端到端优化：

$$\mathcal{L} = 0.8 \times \mathcal{L}_{\text{frame}} + 0.2 \times \mathcal{L}_{\text{motion}}$$

其中 $\mathcal{L}_{\text{frame}}$ 为top-k硬帧光度损失，在每轮迭代中选取损失最大的若干帧进行重点优化，迫使模型关注难以重建的时间片段。运动感知损失 $\mathcal{L}_{\text{motion}}$ 由三项子损失加权构成：

$$\mathcal{L}_{\text{motion}} = \lambda_{\text{diff}} \mathcal{L}_{\text{diff}} + \lambda_{\text{amp}} \mathcal{L}_{\text{amp}} + \lambda_{\text{dir}} \mathcal{L}_{\text{dir}}$$

- $\mathcal{L}_{\text{diff}}$：时序差分损失，约束相邻帧间节点运动的平滑性；
- $\mathcal{L}_{\text{amp}}$：运动幅度损失，防止节点产生不合理的剧烈位移；
- $\mathcal{L}_{\text{dir}}$：运动方向损失，确保节点运动方向的时序一致性。

此外，训练过程中随机掩码部分输入时间嵌入，作为一种时序正则化手段，降低模型对特定时间戳的过拟合，提升时间泛化能力。

### 补充图表

![[assets/figures/papers/paper_list_l3_https_openreview_net_forum_id_N4VKlSxCLc/figures/002_Figure_2.jpg]]
*Figure 2: Position-only nodes versus decoupled nodes with position and code. We visualize 24 Gaussians (red) in high motion region and its three corresponding nodes (white). With the decoupled design, Gaussians attach to semantically consistent nodes rather than merely following spatial neighbors, which struggle under large motion*

![[assets/figures/papers/paper_list_l3_https_openreview_net_forum_id_N4VKlSxCLc/figures/003_Figure_3.jpg]]
*Figure 3: The Architecture of the Temporal Deformation Network. For each of the N control nodes, features over a window of T frames are processed by an MLP backbone interleaved with temporal self-attention blocks. Attention operates along the time axis and is fused by a lightweight gate, then decoded to per-node translation, rotation, and scale for all T frames*

![[assets/figures/papers/paper_list_l3_https_openreview_net_forum_id_N4VKlSxCLc/figures/009_Figure_6.jpg]]
*Figure 6: Overview of multi-frame group sampling strategies. Colored blocks with number denote real frames, and gray blocks with F indicate placeholder timestamps. A row of blocks represents the T -frame training window*

## 实验与分析

### 主实验结果

Mango-GS在两个公开动态场景数据集上与多个代表性基线进行了定量对比，覆盖渲染质量、时间一致性与效率三个维度。Table 1汇总了Neural 3D Video和HyperNeRF-vrig上的完整结果。

在Neural 3D Video数据集上，Mango-GS以PSNR 31.89达到最高，显著超越包括**4D Gaussians**（Wu et al., CVPR 2024）、**Deformable 3DGS**（Yang et al., CVPR 2024）和**D-3DGS**（Luiten et al., 3DV 2024）在内的强基线。这一优势源于多帧时间注意力网络对运动动力学的显式建模：与逐帧独立预测变形的基线不同，Mango-GS在T=6的时间窗口内联合推断节点轨迹，有效抑制了快速运动下的帧间闪烁。

在HyperNeRF-vrig数据集上，Mango-GS在PSNR（26.2）、MS-SSIM（0.78）和tLPIPS（0.0196）三项指标上均取得最优。tLPIPS作为衡量时间一致性的专用指标，其最低值直接验证了方法在抑制时序伪影方面的核心能力。值得关注的是，**TimeFormer**（同样应用跨时间Transformer到可变形高斯）和**MotionGS**（Zhu et al., NeurIPS 2024，引入显式运动引导）在tLPIPS上均弱于Mango-GS，说明将时间建模约束在稀疏控制节点层面——而非密集高斯层面——是一种更有效的运动先验注入方式。

效率方面，Mango-GS以149.5 FPS实现实时渲染，存储量仅60 MB。与**MotionGS**和**TimeFormer**相比，Mango-GS速度提升超过3倍，同时tLPIPS和MS-SSIM更优。这种效率-质量的双重优势归因于：时间注意力仅在稀疏控制节点（初始2048个，最终约1420个）上操作，密集高斯的变形通过预计算的k-NN权重进行轻量级插值传播。

### 消融实验

#### 核心组件消融

Table 3通过逐步添加各组件，验证了Mango-GS每个设计选择的有效性。基线模型采用纯空间k-NN关联和逐帧MLP变形预测。

首先，引入**解耦控制节点表示**（将规范位置与可学习特征代码分离）后，PSNR和SSIM出现首次跃升。这证实了Figure 2所揭示的机制：在联合位置-特征空间中建立的k-NN邻域，能够在大幅度运动下维持语义一致的节点-高斯对应关系，避免纯空间k-NN因邻域漂移导致的变形传播错误。

其次，加入**时间注意力网络**后，tLPIPS显著下降，表明多帧联合建模直接转化为时间一致性的提升。时间自注意力沿T帧的时间轴操作，使每个节点能够聚合窗口内的运动上下文，而非孤立地预测单帧变形。

最后，**top-k硬帧光度损失**和**运动感知损失**的引入进一步提升了所有指标。硬帧损失通过聚焦每个训练批次中光度误差最大的k帧，迫使模型关注困难时间点；运动感知损失由时序差分损失、运动幅度损失和运动方向损失三项组成（公式(9)），为节点轨迹施加物理合理性约束。

#### 时间窗口大小与邻居数量

Table 2展示了时间窗口T和k-NN邻居数K的消融结果。T=6在所有指标上取得最佳平衡：较小的T（如3）无法充分捕获运动依赖，导致tLPIPS升高；较大的T（如9）虽未显著损害质量，但增加了计算开销且边际收益递减。K=3获得最高的PSNR和SSIM：过小的K（如1）使变形传播过于刚性，过大的K（如5）则引入无关节点的噪声。

#### 训练策略与控制节点数

Table 4的采样器比例消融表明，稀疏步进采样器与插值采样器以0.7:0.3的比例混合时达到最佳tLPIPS。稀疏步进采样器提供大跨度的帧组，有助于学习长程运动动态；插值采样器提供密集的局部帧组，保障时间平滑性。该比例实现了两者的有效平衡。

Table 5的控制节点数消融显示，初始2048个节点（最终约1420个）取得最高PSNR和SSIM。节点数过少（如512）时，稀疏锚点不足以覆盖复杂运动区域；节点数过多（如4096）则可能导致过拟合，表现为训练集指标虚高但测试集泛化下降。

### 定性分析

Figure 4和Figure 5分别展示了Neural 3D Video和HyperNeRF-vrig数据集上的可视化对比。在快速运动区域（如人体手臂挥动、面部表情剧烈变化），基线方法普遍出现模糊、拖影或几何断裂，而Mango-GS保持了清晰的边界和稳定的纹理。Figure 7的连续12帧推断序列进一步验证了时间一致性：在包含大位移的片段中，Mango-GS的输出无闪烁、无跳变，高斯云在连续帧间平滑迁移。

### 失败模式与局限

尽管整体性能优异，Mango-GS仍存在以下边界情况：

1. **超窗口运动**：时间窗口固定为T=6，对于运动周期超过该窗口的缓慢长程变化（如持续数十帧的渐变光照），模型可能退化为类逐帧预测，时间注意力收益减弱。
2. **极端非刚性形变**：虽然解耦节点在联合空间中提升了邻域稳定性，但在拓扑结构剧烈改变的场景（如衣物大幅褶皱、流体飞溅）下，规范空间的k-NN关联仍可能出现传播误差，导致局部区域的高斯跟随错误节点运动。
3. **遮挡与去遮挡**：方法未集成显式的几何或光流先验，在严重遮挡区域，控制节点的运动推断缺乏足够的观测约束，可能产生不合理轨迹。

### 补充图表

![[assets/figures/papers/paper_list_l3_https_openreview_net_forum_id_N4VKlSxCLc/figures/005_Table_1.jpg]]
*Table 1: Quantitative comparison on two datasets. Best is bold and second-best is underlined*

![[assets/figures/papers/paper_list_l3_https_openreview_net_forum_id_N4VKlSxCLc/figures/006_Figure_5.jpg]]
*Figure 5: Qualitative comparison on HyperNeRf. Our method offers sharp results. Differences are highlighted with boxes*

![[assets/figures/papers/paper_list_l3_https_openreview_net_forum_id_N4VKlSxCLc/figures/007_Table_2.jpg]]
*Table 2: Ablation on time window size T and number of neighbors K*

![[assets/figures/papers/paper_list_l3_https_openreview_net_forum_id_N4VKlSxCLc/figures/008_Table_3.jpg]]
*Table 3: Ablation on the core components of Mango-GS. We report results from progressively adding each component to a baseline*

![[assets/figures/papers/paper_list_l3_https_openreview_net_forum_id_N4VKlSxCLc/figures/010_Table_4.jpg]]
*Table 4: Ablation on the ratio between sparse stride and interpolation samplers*

![[assets/figures/papers/paper_list_l3_https_openreview_net_forum_id_N4VKlSxCLc/figures/011_Table_5.jpg]]
*Table 5: Ablation on the number of control nodes N. We report initial and final node counts, along with reconstruction quality metrics*

![[assets/figures/papers/paper_list_l3_https_openreview_net_forum_id_N4VKlSxCLc/figures/012_Table_6.jpg]]
*Table 6: Per-scene reconstruction quality of Mango-GS on the HyperNeRF-vrig dataset*

## 方法谱系与知识库定位

### 与基线方法的关系

Mango-GS 立足于动态高斯溅射（4DGS）的两条技术路线交汇点：**节点引导的变形传播**与**基于 Transformer 的时间建模**。

在节点引导范式上，**SC-GS** 率先提出用稀疏控制节点驱动密集高斯云的运动，但其节点仅依赖空间 3D 位置，通过纯欧氏距离的 k-NN 建立节点-高斯关联。Mango-GS 继承了这一“稀疏控制-密集传播”的宏观架构，但将控制节点解耦为规范位置与可学习特征代码，将关联机制从纯空间 k-NN 升级为联合位置-特征空间中的学习型 k-NN。这一改动直接回应了 SC-GS 在大幅度运动下的核心弱点：空间邻域随形变漂移，导致节点-高斯对应关系失效（Figure 2 提供了直观对比证据）。

在时间建模路线上，**TimeFormer** 将跨时间 Transformer 应用于可变形高斯，显式建模帧间时间关系；**MotionGS**（Zhu et al., NeurIPS 2024）则引入显式运动引导。Mango-GS 与这两者的关键差异在于**时间建模的粒度与载体**：TimeFormer 和 MotionGS 在密集高斯或全局层面建模时间依赖，而 Mango-GS 将时间注意力网络限定在稀疏控制节点上——仅对约 2048 个节点（训练后约 1420 个）沿时间轴执行多头自注意力，再将学习到的运动通过预计算权重传播至密集高斯云。这种“稀疏时间建模 + 密集传播”的设计在效率上形成显著优势：Table 1 显示 Mango-GS 在 HyperNeRF-vrig 上达到 149.5 FPS，比 MotionGS 和 TimeFormer 快 3 倍以上，同时 tLPIPS 和 MS-SSIM 更优。

与更早的逐帧变形方法相比，**Deformable 3DGS**（Yang et al., CVPR 2024）和 **D-3DGS**（Luiten et al., 3DV 2024）均采用 MLP 对规范高斯进行逐帧独立预测，缺乏跨帧时间约束。**4D Gaussians**（Wu et al., CVPR 2024）虽引入 4D 时空编码，但本质上仍是逐帧优化。Mango-GS 的多帧时间窗口（T=6）和运动感知损失（时序差分损失 + 运动幅度损失 + 运动方向损失）从架构和训练信号两个层面强制模型学习帧间运动动力学，而非记忆单帧外观。

### 适用边界与局限

**适用场景**：Mango-GS 面向预设长度的动态场景离线重建，在 Neural 3D Video 和 HyperNeRF-vrig 两个公开基准上验证了有效性。其核心设计——解耦节点表示与多帧时间注意力——特别适用于包含快速运动、非刚性形变的场景，这类场景正是纯空间 k-NN 和逐帧变形方法容易产生伪影的难点。

**已知局限**：

1. **固定时间窗口**：当前方法的时间窗口固定为 T=6（Table 2 消融证实 T=6 在 PSNR、SSIM 和 tLPIPS 上均为最优），这意味着模型的时间感受野受限于 6 帧。对于超过此窗口的长程运动依赖（如周期性动作的完整周期），模型无法显式捕获。Table 2 中 T=8 时性能反降，暗示简单扩大窗口可能引入噪声，需要更精巧的长程建模机制。

2. **规范空间关联的极限**：虽然解耦节点在联合位置-特征空间中建立语义感知邻域，大幅提升了大幅度形变下的鲁棒性（Figure 2），但节点-高斯关联仍基于规范空间计算。在极端非刚性拓扑变化（如物体撕裂、融合）下，规范空间的 k-NN 对应关系可能仍不够稳定，传播误差难以完全避免。

3. **离线序列假设**：训练和推断均面向完整预设序列，未验证在在线流式场景或极长视频下的适应能力。时间注意力网络需要完整的 T 帧窗口作为输入，无法直接处理逐帧到达的流式数据。

4. **缺乏显式几何先验**：Mango-GS 未集成光流、深度或场景流等显式几何监督信号，运动学习完全依赖光度损失和运动感知损失。在剧烈运动、严重遮挡或纹理稀疏区域，纯光度信号的引导可能不足。

### 开放问题与后续方向

从当前设计的约束出发，可识别以下开放问题：

1. **长程时间建模**：如何通过轻量级记忆机制（如可学习的时间记忆 token 或滑动窗口状态传递）扩展时间视野，使模型能处理更长视频序列而不显著增加计算开销？Table 2 中 T>6 的性能下降提示，直接扩大窗口并非有效方案，需要结构化的长程依赖建模。

2. **流式与在线适应**：如何使 Mango-GS 适应在线或流式长视频场景？可能的思路包括将固定窗口改为滑动窗口，并设计窗口间的状态传递机制，实现动态重建的持续学习。

3. **几何先验集成**：能否将光流或单目深度估计作为辅助监督信号，融入运动感知损失或节点变形预测中？这有望提升极端运动和复杂拓扑变化下的重建精度，特别是在遮挡边界和纹理稀疏区域。

4. **跨表示推广**：节点引导的多帧建模思想是否可推广到其他显式场景表示（如 3D 高斯点云的其他变体、基于 mesh 的表示）或大规模动态场景（如自动驾驶场景的动态重建）？这需要验证控制节点机制在不同表示密度和运动复杂度下的可迁移性。

5. **节点数量的自适应**：Table 5 显示控制节点数从 2048 增加到 4096 时性能下降（可能因过拟合），当前采用固定初始数量。能否设计自适应节点剪枝或增长策略，根据场景运动复杂度动态调整节点密度？

## 原文 PDF

![[paperPDFs/ICLR_2026/Mango_GS_Enhancing_Spatio_Temporal_Consistency_in_Dynamic_Scenes_Reconstruction_df1c4f8104b2.pdf]]