---
title: "DGGT: Feedforward 4D Reconstruction of Dynamic Driving Scenes using Unposed Images"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/DGGT_Feedforward_4D_Reconstruction_of_Dynamic_Driving_Scenes_using_Unposed_Images.pdf
project_link: null
code_link: "https://github.com/xiaomi-research/dggt"
aliases:
- DGGT
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
- topic/benchmarks_datasets_evaluation
core_operator: 将相机姿态从必需输入变为模型同步预测的输出，并一次性生成像素对齐的3D高斯图以及动态‐静态分解，使前馈重建能够摆脱对姿态校准和固定序列长度的限制。
primary_logic: 通过统一的前馈框架同时预测每帧3D高斯表示、生命期参数、动态掩膜和3D运动轨迹，可将动态场景建模为静态聚合与当前动态的组合，并利用扩散后处理消除插值伪影，实现从稀疏无姿态图像的高质量4D重建。
claims:
- 在Waymo数据集上达到27.41 PSNR、0.846 SSIM，推理时间0.39秒，超越优化和前馈基线。
- 仅Waymo训练即可在nuScenes上零样本获得25.31 PSNR，Argoverse2上26.34 PSNR。
- 移除生命期参数后PSNR从27.41降至24.21，扩散精细化也带来稳定增益。
- 3D运动估计达到0.183 m EPE3D，优于STORM。
---

# DGGT: Feedforward 4D Reconstruction of Dynamic Driving Scenes using Unposed Images

> [!tip] 核心洞察
> 通过统一的前馈框架同时预测每帧3D高斯表示、生命期参数、动态掩膜和3D运动轨迹，可将动态场景建模为静态聚合与当前动态的组合，并利用扩散后处理消除插值伪影，实现从稀疏无姿态图像的高质量4D重建。

| 字段 | 内容 |
|------|------|
| 中文题名 | DGGT：从无姿态图像的前馈4D动态驾驶场景重建 |
| 英文题名 | DGGT: Feedforward 4D Reconstruction of Dynamic Driving Scenes using Unposed Images |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2512.03004) · [Code](https://github.com/xiaomi-research/dggt) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction #topic/benchmarks_datasets_evaluation |
| Method | DGGT |
| Dataset | Waymo Open Dataset, nuScenes, Argoverse2, Waymo Scene Flow |

> [!tip] 效果简介
> - Waymo Open Dataset (NVS) 上，PSNR / SSIM / D-RMSE 27.41 / 0.846 / 3.47 vs STORM: 26.05 / 0.819 / 5.91 (+1.36 / +0.027 / -2.44)；Inference time (s) 0.39 vs STORM: 0.50 (or 0.18 for light version) (comparable)。
> - nuScenes (zero-shot) 上，PSNR / SSIM / LPIPS 25.31 / 0.794 / 0.152 vs STORM: 17.77 / 0.669 / 0.394 (+7.54 / +0.125 / -0.242)。
> - Argoverse2 (zero-shot) 上，PSNR / SSIM / LPIPS 26.34 / 0.812 / 0.155 vs STORM: 20.83 / 0.542 / 0.326 (+5.51 / +0.270 / -0.171)。

## 概要

动态驾驶场景的4D重建是自动驾驶感知与仿真的核心任务，但现有方法面临根本性瓶颈：逐场景优化方案（如**EmerNeRF**，Yang et al., arXiv 2023）速度慢、难以规模化；前馈方法则普遍依赖已知相机姿态或固定短时间窗口，无法直接处理大规模驾驶日志中常见的无标定图像序列。**DGGT** 提出了一种统一的前馈框架，将相机姿态从必需输入转变为模型同步预测的输出，并一次性生成像素对齐的3D高斯图，配合动态-静态分解与3D运动轨迹插值，在0.39秒内从稀疏无姿态图像完成高质量4D重建。

其核心洞察在于：通过同时预测每帧的3D高斯表示、生命期参数、动态掩膜和3D位移向量，可将动态场景建模为“全时段静态高斯聚合 + 当前帧动态高斯”的组合，并利用单步扩散后处理消除插值产生的鬼影和去遮挡伪影。这一设计使模型摆脱了对姿态校准和固定序列长度的限制，在Waymo数据集上达到27.41 PSNR、0.846 SSIM，超越优化和前馈基线（如STORM的26.05 PSNR）；仅用Waymo训练即可在nuScenes上零样本获得25.31 PSNR，Argoverse2上26.34 PSNR，展现出强大的跨域泛化能力。3D运动估计也达到0.183 m EPE3D，优于STORM。

消融实验证实了各组件的关键作用：移除生命期参数后PSNR从27.41降至24.21，扩散精细化模块则稳定消除伪影、提升感知质量。该方法支持任意数量输入视图（4/8/16帧），性能稳健且略有提升，对稀疏输入具有低敏感性。此外，显式的动静分解和3D高斯表示天然支持场景编辑，如移除、移位或插入动态物体。

尽管如此，DGGT仍存在局限：当动态掩膜不准确或运动遮挡严重时，跟踪与重建会出现失败案例；扩散精细化模块增加了计算开销，尚未针对实时应用深度优化；模型主要在驾驶场景训练，在非结构化或极端动态环境中的泛化性有待验证。未来工作可探索自监督动态掩膜学习、更轻量的精细化模块，以及向更长时序序列的扩展。



自动驾驶系统依赖大规模时序传感器数据来感知、预测和规划。从这些数据中高效重建4D动态场景（3D空间+时间）是下游任务的基础能力，它需要同时恢复场景几何、外观、运动以及相机姿态。然而，现有方法在这一目标上存在根本性的效率与可扩展性瓶颈。

**逐场景优化的困境。** 以 **EmerNeRF** (Yang et al., arXiv 2023)、**PVG** (Chen et al., CVPR 2024) 和 **DeformableGS** (Yang et al., CVPR 2024) 为代表的动态场景重建方法，通常需要对每个场景进行独立的梯度下降优化，耗时数分钟到数小时。这种逐场景优化范式使其难以作为大规模驾驶日志的标准化预处理步骤，严重制约了数据管线的吞吐量。

**前馈方法的局限。** 为克服优化开销，一系列前馈重建方法被提出，如 **LGM** (Tang et al., ECCV 2024)、**GS-LRM** (Zhang et al., ECCV 2024)、**MVSplat** (Chen et al., 2025) 和 **DepthSplat** (Xu et al., CVPR 2025)。它们通过单次网络前向传播即可生成3D高斯表示，大幅提升了推理速度。但这些方法主要面向静态场景，无法建模驾驶场景中普遍存在的动态物体（车辆、行人等）。**STORM** (Yang et al., arXiv 2024) 率先将前馈重建扩展到动态场景，但其设计仍依赖两个关键前提：（1）相机姿态必须作为已知输入提供；（2）输入序列长度固定。在实际部署中，精确的相机标定并非总是可得，而固定窗口限制则削弱了对长时序数据的适应性。

**免姿态方法的缺口。** 最近，**NoPoSplat** (Ye et al., arXiv 2024) 和 **VGGT++** (Wang et al., CVPR 2025) 探索了无需已知姿态的前馈重建，但它们同样局限于静态场景，未触及动态建模这一核心挑战。

上述缺口共同指向一个核心瓶颈：**现有动态场景重建方法依赖逐场景优化、已知相机姿态或固定短窗口，导致速度慢、可扩展性差，难以作为大规模驾驶日志的预处理步骤。** 本文的动机正是打破这些依赖——将相机姿态从必需输入变为模型同步预测的输出，并一次性生成像素对齐的3D高斯图以及动态-静态分解，使前馈重建能够摆脱对姿态校准和固定序列长度的限制，从而在0.4秒内从无姿态图像完成高质量的4D动态场景重建。



## 核心方法与创新机理

DGGT的核心创新在于将动态场景重建从一个依赖逐场景优化与已知姿态的慢速流程，转变为一个**完全前馈、免姿态、可泛化的单次推理框架**。其关键设计围绕五个“changed slots”展开，每个都针对现有方法的根本瓶颈。

### 1. 姿态从先决条件变为同步输出

传统动态重建方法（如EmerNeRF、PVG、STORM）均将相机姿态作为已知输入或需逐场景标定的先决条件，这严重限制了其作为大规模驾驶日志预处理工具的实用性。DGGT通过**Camera Head**直接从多视图注意力特征中预测每帧的内参与外参（$\Pi^t = \mathcal{H}_{\text{cam}}(F_{\text{attn}})$），将姿态从“必需输入”降级为“模型输出”。这一改变使得系统可以直接处理未经校准的稀疏图像序列，消除了对离线SfM或SLAM的依赖，是实现真正前馈重建的基础。

### 2. 生命期参数：显式建模时间可见性

现有前馈方法（如LGM、MVSplat）对高斯的时序行为缺乏显式控制，导致静态区域在跨帧聚合时出现外观闪烁。DGGT引入**Lifespan Head**，为每个像素对齐的高斯预测生命期参数$\sigma$，通过高斯衰减函数调制其在不同时间戳的不透明度：

$$o^{t'} = o^{t} \cdot e^{-\frac{1}{2} \cdot \frac{(t'-t)^2}{\sigma^{t}}}$$

这一设计使得模型可以自动学习每个高斯的有效时间窗口——静态背景元素获得较大的$\sigma$以保持长期可见，而短暂出现的动态物体则获得较小的$\sigma$以自然消退。消融实验（Table 4）证实，移除生命期参数后PSNR从27.41骤降至24.21，验证了该机制对建模静态区域外观变化的核心作用。

### 3. 动静态分解：从统一表示到组件化建模

与STORM等仅预测速度矢量的方法不同，DGGT通过**Dynamic Head**预测像素级动态概率掩膜$M_d^t$，将每帧高斯图显式分解为静态与动态组件：

$$G_s^{t} = G^{t} \odot (1 - M_d^{t}), \quad G_d^{t} = G^{t} \odot M_d^{t}$$

最终的场景表示采用“全时段静态聚合 + 当前帧动态”的组合策略：

$$\hat{G}^{t} = \left( \bigcup_{t'=1}^{N} G_s^{t'} \right) \cup G_d^{t} \cup G_{\text{sky}}$$

这种分解使得静态背景可以从所有帧中积累信息，而动态物体仅从当前帧获取，从根本上解决了传统高斯表示中运动物体产生的“鬼影”问题。

### 4. 运动头：从速度预测到完整位移场

STORM等基线仅预测速度矢量，难以处理非线性运动轨迹。DGGT的**Motion Head**基于Transformer架构，显式预测任意像素对之间的完整3D位移向量$F(t_a, t_b)$，支持对动态高斯均值位置进行精确插值：

$$\mu_d^{t_i} = \mu_d^{t_a} + \omega^{t_i} \cdot F(t_a, t_b), \quad \omega^{t_i} = \frac{t_i - t_a}{t_b - t_a}$$

这一设计使DGGT在Waymo Scene Flow基准上达到0.183 m EPE3D，显著优于STORM的0.276 m（Table 5），Acc5从0.429提升至0.609。

### 5. 扩散后处理：消除插值伪影

前馈重建在插值渲染时不可避免地产生去遮挡伪影和细节丢失。DGGT引入**单步扩散精细化模块**，以随机参考图像为条件对渲染结果进行去噪：

$$\tilde{I}^{t_i} = f_{\text{diffusion}}( \hat{I}^{t_i}, I_{\text{ref}} )$$

该模块通过重建损失、感知损失和风格（Gram）损失的组合进行训练。消融实验（Table 4）表明，扩散精细化虽未大幅提升PSNR（27.41→27.32），但在视觉质量上显著减少了伪影，尤其在场景编辑中可修复空洞。



DGGT 提出了一种**免姿态的前馈式动态场景重建框架**，其核心设计理念是将相机姿态从必需的输入条件转变为模型同步预测的输出，从而摆脱对离线标定或固定序列长度的依赖。整个 pipeline 以多视图无姿态图像序列为输入，在单次前向传播中完成相机参数估计、像素对齐高斯图生成、动静态分解、3D 运动跟踪以及扩散精细化渲染，最终输出高质量的 4D 动态场景表示。

### 输入输出流

**输入**：给定一个动态场景的 $N$ 帧多视图图像序列 $\{I^1, I^2, \ldots, I^N\}$，每帧包含来自不同相机的多张图像。框架不要求任何预先标定的相机姿态，也不限制输入帧数——实验表明该方法对 4/8/16 视图均保持稳定性能（Table 3）。

**输出**：框架在约 0.39 秒内（Table 1）同步产出：
- 每帧的相机内外参数 $\Pi^t$
- 像素对齐的 3D 高斯图 $G^t$（包含位置、颜色、旋转、尺度、不透明度）
- 生命期参数 $\sigma^t$，控制高斯随时间的可见性衰减
- 动态掩膜 $M_d^t$，标识运动区域
- 3D 运动位移向量 $F(t_a, t_b)$，支持跨帧跟踪与插值
- 天空高斯 $G_{\text{sky}}$，模拟无限远背景
- 经扩散精细化后的渲染图像 $\tilde{I}^{t_i}$

### 模块拓扑与数据流动

框架由九个核心模块串联构成，数据流可概括为“编码→预测→分解→组合→渲染→精细化”六个阶段（Figure 2）：

![[assets/figures/papers/paper_list_l19_https_arxiv_org_abs_2512_03004/figures/002_Figure_2.jpg]]
*Figure 2: Overall Architecture. Given unposed images of dynamic scene, we estimate camera parameters, dynamic maps, and perpixel Gaussians in a single pass. Subsequently, a motion head is employed to track dynamic objects across time, and their trajectories are interpolated to construct temporally consistent Gaussian representations. Finally, a diffusion-based rendering module refines the resulting composition, producing high-fidelity renderings*

1. **ViT Backbone with DINO Encoder**：采用 DINO 预训练的 ViT 架构提取多视图图像特征，通过交替注意力机制融合语义信息与跨视图空间信息，生成融合特征 $F_{\text{attn}}$ 和 DINO 特征 $F_{\text{dino}}$。

2. **Camera Head**：从注意力特征 $F_{\text{attn}}$ 直接预测每帧的相机内参与外参 $\Pi^t = \mathcal{H}_{\text{cam}}(F_{\text{attn}})$，将姿态估计整合进统一的前馈流程。

3. **Gaussian Head**：结合 $F_{\text{dino}}$ 和 $F_{\text{attn}}$ 生成像素对齐的 3D 高斯图 $G^t \in \mathbb{R}^{H \times W \times 15}$，每个像素对应一个高斯基元。

4. **Lifespan Head**：预测每像素的生命期参数 $\sigma^t$，用于调制高斯在不同时间戳的不透明度：$o^{t'} = o^t \cdot e^{-\frac{1}{2} \cdot \frac{(t'-t)^2}{\sigma^t}}$（Eq. 1）。该机制使静态区域的外观随时间变化（如光照、遮挡）得到显式建模。

5. **Dynamic Head**：从 $F_{\text{attn}}$ 预测动态区域概率掩膜 $M_d^t = \mathcal{H}_{\text{dy}}(F_{\text{attn}})$，将高斯图分解为静态组件 $G_s^t = G^t \odot (1 - M_d^t)$ 和动态组件 $G_d^t = G^t \odot M_d^t$（Eq. 2）。

6. **Motion Head**：基于 Transformer 架构，以两个时间戳的图像和高斯图为条件，预测任意查询像素集 $\mathcal{Q}$ 的 3D 位移：$F(t_a, t_b) = \mathcal{H}_{\text{motion}}(\mathcal{Q} \mid G^{t_a}, G^{t_b}, I^{t_a}, I^{t_b})$（Eq. 5）。支持非线性轨迹的线性插值：$\mu_d^{t_i} = \mu_d^{t_a} + \omega^{t_i} \cdot F(t_a, t_b)$（Eq. 6）。

7. **Sky Head**：生成半球天空高斯 $G_{\text{sky}}$，建模无限远背景区域。

8. **Differentiable Renderer**：将完整场景高斯 $\hat{G}^t = \left( \bigcup_{t'=1}^{N} G_s^{t'} \right) \cup G_d^t \cup G_{\text{sky}}$（Eq. 3）渲染为图像，提供训练监督信号。

9. **Diffusion Refinement Module**：以渲染图像 $\hat{I}^{t_i}$ 和随机参考图像 $I_{\text{ref}}$ 为条件，通过单步扩散去噪消除插值产生的鬼影和去遮挡伪影：$\tilde{I}^{t_i} = f_{\text{diffusion}}(\hat{I}^{t_i}, I_{\text{ref}})$（Eq. 11）。

### 关键设计决策与因果机制

框架的核心创新在于三个因果性设计：

- **姿态输出化**：将相机姿态从先决条件变为预测输出，使框架能够直接处理未标定的原始驾驶日志，大幅降低预处理成本。这是实现真正“前馈式”重建的关键。

- **生命期参数**：传统方法对静态区域的外观变化缺乏显式建模。DGGT 通过 $\sigma$ 参数控制高斯的时序可见性衰减，使静态高斯能够随时间自然消退或增强。消融实验表明，移除生命期参数后 PSNR 从 27.41 骤降至 24.21（Table 4），验证了其对建模静态区域外观变化的关键作用。

- **动静分解与运动插值**：通过动态掩膜将场景显式分解为静态聚合（全时段静态高斯并集）与当前动态的组合，避免了传统方法中动态物体导致的“鬼影”问题。Motion Head 预测的完整 3D 位移向量支持非线性轨迹插值，使框架能够处理任意帧间隔的运动重建。

扩散精细化模块作为后处理步骤，以单步去噪的方式消除插值渲染中的伪影并恢复细节，在 PSNR 上带来约 0.09 的增益，且在视觉上显著减少了鬼影和去遮挡区域的瑕疵（Figure 6）。

> **证据强度说明**：上述架构描述基于论文 Sec. 3.1–3.3 的完整方法阐述，所有模块的功能和连接关系均有明确的公式或文字锚点支撑（置信度 ≥ 0.95）。消融实验（Table 4, Figure 6）为各组件的有效性提供了因果验证。

### 补充图表

![[assets/figures/papers/paper_list_l19_https_arxiv_org_abs_2512_03004/figures/001_Figure_1.jpg]]
*Figure 1: Left: Our feedforward framework reconstructs dynamic driving scenes directly from unposed images within 0.4 seconds, producing outputs such as camera pose, 3D Gaussian tracking, depth, and dynamic maps, which further enable instance-level scene editing. Right: Quantitative comparison shows that our method achieves state-of-the-art reconstruction quality with competitive inference speed, outperforming prior feedforward approaches in both accuracy and efficiency.(using single-view input as an example)*



DGGT 的前馈流水线由八个核心模块串联构成，其设计逻辑是将动态场景重建分解为**姿态估计、逐帧高斯生成、动静分离、运动预测与插值、组合渲染、扩散后处理**六个可微阶段，从而将相机姿态从输入约束转变为模型输出。

### 3.1 姿态估计与逐帧高斯生成

**ViT 主干与 DINO 编码器**首先提取多视图图像特征。具体而言，DINO 预训练的 ViT 编码器为每张输入图像生成语义特征 $F_{\mathrm{dino}}$，随后通过交替注意力模块融合多视图间的空间与语义信息，输出注意力特征 $F_{\mathrm{attn}}$。

**相机头（Camera Head）** 直接由 $F_{\mathrm{attn}}$ 预测每帧的相机内参与外参：

$$\Pi^t = \mathcal{H}_{\mathrm{cam}}(F_{\mathrm{attn}})$$

这意味着相机姿态不再是已知输入或逐场景标定的结果，而是模型同步预测的输出——这是 DGGT 实现“免姿态”重建的关键因果旋钮。

**高斯头（Gaussian Head）** 以 $F_{\mathrm{dino}}$ 和 $F_{\mathrm{attn}}$ 为条件，为每帧生成像素对齐的 3D 高斯图 $G^t \in \mathbb{R}^{H \times W \times 15}$，其 15 个通道编码了每个高斯的 3D 位置、颜色、旋转四元数、尺度、不透明度等属性。

### 3.2 生命期参数与时间可见性

**生命期头（Lifespan Head）** 预测每个像素的生命期参数 $\sigma^t$，用于控制高斯在时间维度上的可见性衰减。给定基准时间 $t$ 的不透明度 $o^t$，在时间 $t'$ 的有效不透明度由高斯衰减函数调制：

$$o^{t'} = o^{t} \cdot e^{-\frac{1}{2} \cdot \frac{(t'-t)^2}{\sigma^{t}}} \tag{Eq. 1}$$

该机制解决了静态区域因光照变化、阴影移动等因素导致的外观变化问题：通过为每个高斯分配有限的生命期，模型可以在不同帧聚合不同生命期的高斯来表示同一静态区域在不同时刻的外观。消融实验（Table 4）证实，移除生命期参数后 PSNR 从 27.41 骤降至 24.21，表明该模块对建模静态区域外观变化至关重要。

### 3.3 动静分解与场景组合

**动态头（Dynamic Head）** 从 $F_{\mathrm{attn}}$ 预测动态区域概率掩膜 $M_d^t$，将高斯图分解为静态与动态两个组件：

$$G_s^{t} = G^{t} \odot (1 - M_d^{t}), \quad G_d^{t} = G^{t} \odot M_d^{t} \tag{Eq. 2}$$

**天空头（Sky Head）** 额外生成半球天空高斯 $G_{\mathrm{sky}}$，用于建模无限远背景。完整场景的组合方式为：聚合所有帧的静态高斯（利用生命期参数控制可见性），加上当前帧的动态高斯，再加上天空高斯：

$$\hat{G}^{t} = \left( \bigcup_{t'=1}^{N} G_s^{t'} \right) \cup G_d^{t} \cup G_{\mathrm{sky}} \tag{Eq. 3}$$

这一设计使得静态场景可以从多帧累积信息，而动态物体仅由当前帧表示，避免了运动物体的“鬼影”问题。

### 3.4 运动预测与轨迹插值

**运动头（Motion Head）** 基于 Transformer 架构，以两个时间戳的图像和高斯图作为条件，预测任意查询像素集 $\mathcal{Q}$ 的 3D 位移向量：

$$F(t_a, t_b) = \mathcal{H}_{\mathrm{motion}}( \mathcal{Q} \mid G^{t_a}, G^{t_b}, I^{t_a}, I^{t_b} ) \tag{Eq. 5}$$

与 STORM（Yang et al., arXiv 2024）仅预测速度矢量不同，DGGT 的运动头显式预测像素对之间的完整 3D 位移，支持非线性轨迹的线性插值。对于目标时间 $t_i$，动态高斯的均值位置通过插值得到：

$$\mu_d^{t_i} = \mu_d^{t_a} + \omega^{t_i} \cdot F(t_a, t_b), \quad \omega^{t_i} = \frac{t_i - t_a}{t_b - t_a} \tag{Eq. 6}$$

### 3.5 训练监督与前馈损失

**可微渲染器**将组合高斯 $\hat{G}^t$ 渲染为图像，提供训练监督信号。前馈模型的训练目标由四部分损失加权组合：

$$\mathcal{L}_{\mathrm{rgb}} = \mathcal{L}_{\ell_2} + \lambda_{\mathrm{LPIPS}} \mathcal{L}_{\mathrm{LPIPS}} \tag{Eq. 8}$$

$$\mathcal{L}_{\mathrm{opacity}} = \mathrm{BCE}(M_{\mathrm{sky}}, \hat{M}_{\mathrm{sky}}), \quad \mathcal{L}_{\mathrm{dynamic}} = \mathrm{BCE}(M_d, \hat{M}_{\mathrm{dynamic}}) \tag{Eq. 9}$$

$$\mathcal{L}_{\mathrm{feedforward}} = \mathcal{L}_{\mathrm{rgb}} + \lambda_{\mathrm{opacity}} \mathcal{L}_{\mathrm{opacity}} + \lambda_{\mathrm{dynamic}} \mathcal{L}_{\mathrm{dynamic}} + \lambda_{\mathrm{lifespan}} \mathcal{L}_{\mathrm{lifespan}} \tag{Eq. 10}$$

其中天空掩膜和动态掩膜的真值来自 Waymo LiDAR 标注和语义分割，为训练提供高置信度监督。

### 3.6 扩散精细化后处理

尽管上述流程已能生成合理的新视角图像，但运动插值不可避免地会产生去遮挡伪影和“鬼影”。**扩散精细化模块**以渲染图像 $\hat{I}^{t_i}$ 和随机选取的参考图像 $I_{\mathrm{ref}}$ 为条件，执行单步扩散去噪：

$$\tilde{I}^{t_i} = f_{\mathrm{diffusion}}( \hat{I}^{t_i}, I_{\mathrm{ref}} ) \tag{Eq. 11}$$

扩散模块的训练损失包含重建损失、感知损失和风格（Gram）损失：

$$\mathcal{L}_{\mathrm{diffusion}} = \mathcal{L}_{\mathrm{Recon}} + \mathcal{L}_{\mathrm{LPIPS}} + \lambda_{\mathrm{Gram}} \mathcal{L}_{\mathrm{Gram}} \tag{Eq. 12}$$

消融实验（Table 4）表明，移除扩散精细化后 PSNR 从 27.41 降至 27.32，SSIM 和 LPIPS 也有下降，尤其在减少伪影方面效果显著。



## 实验与关键发现

### 主实验：Waymo 数据集新视角合成

DGGT 在 Waymo Open Dataset 上以 3 个输入视角、插值相邻帧中间视角的设定进行评测，与逐场景优化方法和前馈方法全面对比。**Table 1** 汇总了各方法的渲染质量、推理时间及功能支持情况。

![[assets/figures/papers/paper_list_l19_https_arxiv_org_abs_2512_03004/figures/003_Table_1.jpg]]
*Table 1: Quantitative comparison on the Waymo dataset. Higher PSNR and SSIM, and lower D-RMSE indicate better performance. All methods were evaluated using three input views, where the task is to interpolate the intermediate frame between adjacent views. (* denotes results from our replication). Detailed experimental settings are provided in Appendix*

DGGT 取得了 **27.41 PSNR**、**0.846 SSIM** 和 **3.47 D-RMSE**，在所有指标上均显著优于前馈基线。相比最强的免姿态前馈方法 **NoPoSplat**（Ye et al., arXiv 2024），PSNR 提升 4.01 dB；相比需姿态输入的前馈动态重建方法 **STORM**（Yang et al., arXiv 2024），PSNR 提升 1.36 dB，D-RMSE 降低 2.44。与逐场景优化的 **EmerNeRF**（Yang et al., arXiv 2023）相比，DGGT 在 PSNR 上高出 1.92 dB，同时推理时间仅需 **0.39 秒**，而 EmerNeRF 等优化方法需数分钟至数小时。

**Figure 3** 的定性对比显示，DGGT 在动态物体（如行驶车辆）和静态背景上均生成更清晰的渲染结果，而 STORM 在动态区域存在模糊和重影，NoPoSplat 则因缺乏显式动态建模在移动物体上产生明显伪影。

### 零样本跨域泛化

为验证方法的泛化能力，将在 Waymo 上训练的 DGGT 模型直接应用于 nuScenes 和 Argoverse2 数据集，结果见 **Table 2**。

在零样本设定下，DGGT 在 nuScenes 上取得 **25.31 PSNR / 0.794 SSIM / 0.152 LPIPS**，在 Argoverse2 上取得 **26.34 PSNR / 0.812 SSIM / 0.155 LPIPS**，分别超出 STORM 7.54 dB 和 5.51 dB。这一巨大差距源于 STORM 依赖已知相机姿态，而跨域姿态分布差异导致其性能崩溃。DGGT 将姿态作为输出同步预测，从根本上规避了该问题。在目标数据集上微调后，DGGT 的性能进一步提升至 nuScenes 27.09 PSNR、Argoverse2 28.21 PSNR。**Figure 7** 展示了零样本推理的定性示例，渲染结果保持了良好的结构与细节。

![[assets/figures/papers/paper_list_l19_https_arxiv_org_abs_2512_03004/figures/011_Figure_7.jpg]]
*Figure 7: Zero-shot experiment on nuScenes and Argoverse2 datasets*

### 3D 运动估计精度

**Table 5** 报告了 Waymo Scene Flow 基准上的 3D 运动估计结果。DGGT 达到 **0.183 m EPE3D**，较 STORM 的 0.276 m 降低 33.7%；Acc5 和 Acc10 分别提升 18.0 和 14.2 个百分点，角度误差降低 4.8°。**Figure 4** 的可视化展示了跨帧一致的点对应关系，验证了运动头对动态物体轨迹的精确捕捉能力。

### 消融实验

**Table 4** 和 **Figure 6** 系统评估了各组件的贡献。

**生命期参数**是建模静态区域外观变化的关键。移除生命期参数后，PSNR 从 27.41 骤降至 **24.21**（−3.20 dB），SSIM 从 0.846 降至 0.796。Figure 6 显示，缺少生命期调制时，静态区域（如路面、建筑物）在不同时间戳的外观出现明显闪烁和不一致，因为模型无法区分“该高斯在当前时刻是否可见”。

**扩散精细化模块**提供了稳定但相对温和的增益。移除该模块后，PSNR 降至 27.32（−0.09 dB），SSIM 降至 0.841，LPIPS 从 0.119 升至 0.127。Figure 6 的定性对比表明，扩散精细化主要消除了运动插值产生的鬼影和去遮挡伪影，尤其在动态物体边缘区域效果显著。

**Table 3** 展示了输入视图数量的消融。DGGT 在 4/8/16 个输入视图下性能稳定，PSNR 分别为 27.41/27.60/27.72，表明方法对稀疏输入具有鲁棒性。相比之下，STORM 随视图数量增加性能反而恶化（16 视图时降至 25.11 PSNR），这与其对固定窗口长度的依赖有关。

### 失败模式与局限性

尽管 DGGT 在整体指标上表现优异，分析揭示了以下失败模式：

1. **动态掩膜不准确**：当物体交互复杂或运动模糊严重时，动态头预测的掩膜可能遗漏部分动态区域，导致静态聚合中混入移动物体的残影，产生“鬼影高斯”。
2. **严重遮挡下的跟踪失败**：在密集交通流或大范围遮挡场景中，运动头的跨帧对应关系可能断裂，导致插值位置偏移，表现为动态物体的错位或形变。
3. **扩散精细化的计算开销**：扩散模块虽提升质量，但增加了额外推理时间，目前未针对实时应用深度优化。
4. **域外泛化受限**：模型主要基于结构化驾驶场景训练，在非结构化环境或极端动态场景中的表现有待验证。

### 补充图表

![[assets/figures/papers/paper_list_l19_https_arxiv_org_abs_2512_03004/figures/004_Figure_3.jpg]]
*Figure 3: Qualitative comparison of different methods on Waymo dataset. (results shown are for the forward-facing camera)*

![[assets/figures/papers/paper_list_l19_https_arxiv_org_abs_2512_03004/figures/006_Figure_4.jpg]]
*Figure 4: 3D Tracking Visualization. Points with the same color correspond across frames*

![[assets/figures/papers/paper_list_l19_https_arxiv_org_abs_2512_03004/figures/007_Table_3.jpg]]
*Table 3: Ablation study on the number of input views. Reconstruction performance shows low sensitivity to the number of input frames, demonstrating robustness with sparse inputs*

![[assets/figures/papers/paper_list_l19_https_arxiv_org_abs_2512_03004/figures/008_Table_4.jpg]]
*Table 4: Ablation study. Removing lifespan parameters or the diffusion refinement model decreases performance*

![[assets/figures/papers/paper_list_l19_https_arxiv_org_abs_2512_03004/figures/010_Figure_6.jpg]]
*Figure 6: Ablation study. Removing the lifespan parameter hinders the capture of changing appearance of static scene, while the diffusion refinement reduces artifacts and improves rendering*

![[assets/figures/papers/paper_list_l19_https_arxiv_org_abs_2512_03004/figures/009_Figure_5.jpg]]
*Figure 5: Scene editing results. Cars can be removed or shifted (row 1), and novel vehicles/cyclists inserted from other scenes (row 2). Diffusion refinement fixes artifacts such as holes (red box)*

![[assets/figures/papers/paper_list_l19_https_arxiv_org_abs_2512_03004/figures/012_Figure_8.jpg]]
*Figure 8: More Qualitative Results*



## 定位与知识库关联

### 1. 与基线方法的关系

DGGT 处于**前馈动态场景重建**这一新兴技术路线上，其核心突破在于将相机姿态从“必需输入”转变为“同步预测输出”，从而摆脱了对离线标定或已知姿态的依赖。这一设计使其在方法谱系中占据了独特位置。

**（1）相对于逐场景优化方法**

传统动态场景重建依赖逐场景优化（per-scene optimization），代表性工作包括 **EmerNeRF**（Yang et al., arXiv 2023）、**PVG**（Chen et al., CVPR 2024）和 **DeformableGS**（Yang et al., CVPR 2024）。这些方法虽然能获得高质量重建，但存在根本性瓶颈：每个新场景需要数分钟至数小时的梯度下降，且通常需要已知相机姿态。DGGT 以单次前馈推理（0.39秒/场景）替代了迭代优化，同时将姿态预测内化于模型之中，使其可作为大规模驾驶日志的预处理步骤——这是优化方法无法实现的可扩展性优势。

**（2）相对于前馈静态重建方法**

前馈3D重建领域已有 **LGM**（Tang et al., ECCV 2024）、**GS-LRM**（Zhang et al., ECCV 2024）、**MVSplat**（Chen et al., 2025）等工作，但这些方法仅处理静态场景。DGGT 通过引入**生命期参数**（lifespan parameter σ）和**动静分解机制**，将前馈重建从静态域扩展到动态域。生命期参数控制每个高斯随时间的可见性衰减（Eq. 1），使静态区域的外观变化（如光照、透视变化）得以建模；动态掩膜则将高斯图分解为静态与动态组件，分别采用不同的时序聚合策略（Eq. 2, Eq. 3）。

**（3）相对于免姿态前馈方法**

**NoPoSplat**（Ye et al., arXiv 2024）和 **VGGT++**（Wang et al., CVPR 2025）同样探索了免姿态前馈重建，但它们聚焦于静态场景。DGGT 将免姿态能力与动态建模结合，是首个在免姿态设定下实现动态场景前馈重建的工作。在 Waymo 数据集上，DGGT 达到 27.41 PSNR，而 NoPoSplat 和 VGGT++ 由于缺乏动态建模，在动态区域出现严重伪影。

**（4）相对于前馈动态方法 STORM**

**STORM**（Yang et al., arXiv 2024）是最直接的前馈动态重建基线，但仍需已知相机姿态作为输入。DGGT 在三个关键维度上超越了 STORM：

- **姿态依赖**：STORM 需要外部提供相机参数，DGGT 则通过 Camera Head 同步预测内参与外参；
- **运动建模**：STORM 仅预测速度矢量，DGGT 的 Motion Head 显式预测任意像素对之间的完整 3D 位移向量 $F(t_a, t_b)$（Eq. 5），支持非线性轨迹插值，在 Waymo Scene Flow 基准上达到 0.183 m EPE3D，显著优于 STORM 的 0.276 m；
- **跨域泛化**：STORM 在 nuScenes 零样本测试中仅获 17.77 PSNR，而 DGGT 达到 25.31 PSNR（+7.54 dB），表明其姿态预测和动态建模具有更强的泛化能力。

### 2. 适用边界与能力定位

**（1）输入灵活性**

DGGT 对输入视图数量具有低敏感性：消融实验（Table 3）表明，使用 4、8 或 16 个输入视图时，性能保持稳定甚至略有提升，而 STORM 随视图增加性能恶化。这得益于其静态高斯跨帧聚合机制——更多视图为静态区域提供更丰富的观测，而动态组件仅依赖当前帧，避免了时序混淆。

**（2）场景适用范围**

当前模型主要基于驾驶场景训练（Waymo Open Dataset），在 nuScenes 和 Argoverse2 上的零样本结果（Table 2）证明了跨数据集泛化能力，但存在明确边界：

- **结构化动态**：模型擅长处理车辆、骑行者的刚性运动，但在高度非结构化或极端动态环境（如人群密集场景）中的表现未经验证；
- **严重遮挡**：当动态掩膜不准确或物体间遮挡复杂时，跟踪和重建会出现失败案例——这是论文明确承认的局限；
- **长时序序列**：当前设计基于固定窗口（20帧），扩展到数分钟日志的能力仍是开放问题。

**（3）计算效率定位**

DGGT 在 NVIDIA A100 上的推理时间为 0.39 秒，与 STORM（0.50秒）可比，但显著快于逐场景优化方法（数分钟至小时级）。然而，扩散精细化模块虽然提升了渲染质量（PSNR 从 27.32 提升至 27.41），也增加了计算开销。当前版本未针对实时应用进行深度优化，在边缘设备上的部署可行性有待验证。

### 3. 局限与失败模式

**（1）动态掩膜依赖**

动态分解依赖于 LiDAR 标注训练的动态掩膜监督（$\mathcal{L}_{\mathrm{dynamic}}$，Eq. 9）。当掩膜预测不准确时——例如运动物体边界模糊或新出现物体——动静分解会产生错误，导致动态高斯被错误地聚合到静态组件中，产生“鬼影”伪影。Figure 6 的消融可视化间接揭示了这一问题：移除生命期参数后，静态区域的外观闪烁表明模型对掩膜质量高度敏感。

**（2）运动跟踪失效**

Motion Head 基于 Transformer 预测像素对之间的 3D 位移，但当物体间存在严重交互遮挡或运动高度非线性时，跟踪精度下降。论文明确指出这一局限，但未提供定量分析。

**（3）扩散精细化的代价**

扩散模块以单步去噪方式消除插值伪影（Eq. 11），但增加了推理延迟和模型复杂度。消融实验（Table 4）显示其增益有限（PSNR +0.09），在资源受限场景下可能成为负担。

### 4. 开放问题

1. **自监督动态分解**：当前依赖 LiDAR 标注训练动态掩膜，能否通过运动一致性、光度误差等自监督信号完全摆脱对标注的依赖？
2. **长时序扩展**：固定窗口设计限制了时间上下文，如何扩展到数分钟甚至更长的驾驶日志而不降低质量？
3. **遮挡鲁棒性**：在高度遮挡和非线性动态下，运动跟踪的鲁棒性如何进一步提升？多假设跟踪或概率建模是否是可行方向？
4. **轻量级精细化**：扩散模块能否被轻量级模型（如轻量 U-Net 或对抗训练）替代，以降低延迟？
5. **非驾驶场景泛化**：模型在室内动态场景、运动捕捉等非结构化环境中的表现如何？需要什么样的适配策略？



## 原文 PDF

![[paperPDFs/CVPR_2026/DGGT_Feedforward_4D_Reconstruction_of_Dynamic_Driving_Scenes_using_Unposed_Images.pdf]]
