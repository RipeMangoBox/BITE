---
title: Towards Photorealistic and Efficient Bokeh Rendering via Diffusion Framework
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/Towards_Photorealistic_and_Efficient_Bokeh_Rendering_via_Diffusion_Framework.pdf
project_link: null
code_link: null
aliases:
- TPEBRDF
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
- topic/generative_models_diffusion
core_operator: 提出统一单步扩散框架，通过交替训练策略解耦超分与散景优化，辅以聚焦感知掩码注意力和退化感知深度估计，实现低质输入下的高质量散景渲染。
primary_logic: 预训练扩散模型内蕴散景先验；将Real-ISR与散景渲染交替优化并利用散焦图调制自注意力，可有效消除任务冲突，同时通过自特征蒸馏提升低质图像深度估计鲁棒性，实现高效、可控的真实感散景生成。
claims:
- MagicBokeh在合成退化数据集EBB400-LQ上取得最佳PSNR/SSIM/LPIPS及最快推理速度。
- 交替训练策略与聚焦感知掩码注意力联合提升散景质量（LPIPS、无参考指标等）。
- 真实世界高倍变焦移动摄影效果获用户偏好最优。
- EBB400-LQ 上 PSNR↑ / SSIM↑ / LPIPS↓ / DISTS↓ / Time(s)↓ = 24.23 / 0.7026 / 0.2786 / 0.1944 / 0.1062
---

# Towards Photorealistic and Efficient Bokeh Rendering via Diffusion Framework

> [!tip] 核心洞察
> 预训练扩散模型内蕴散景先验；将Real-ISR与散景渲染交替优化并利用散焦图调制自注意力，可有效消除任务冲突，同时通过自特征蒸馏提升低质图像深度估计鲁棒性，实现高效、可控的真实感散景生成。

| 字段 | 内容 |
|------|------|
| 中文题名 | 基于扩散框架的真实感高效散景渲染 |
| 英文题名 | Towards Photorealistic and Efficient Bokeh Rendering via Diffusion Framework |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2605.07429) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction #topic/generative_models_diffusion |
| Method | MagicBokeh |
| Dataset | EBB400-LQ |

> [!tip] 效果简介
> - EBB400-LQ 上，PSNR↑ / SSIM↑ / LPIPS↓ / DISTS↓ / Time(s)↓ 24.23 / 0.7026 / 0.2786 / 0.1944 / 0.1062 vs SOTA两阶段组合（如OSEDiff+BokehDiff等） (全面优于所有对比方法，推理速度最快)。

## 概述

高倍变焦摄影在移动设备上日益普及，但长焦镜头受限于物理孔径与传感器尺寸，常导致图像分辨率下降、噪声放大、边界模糊与纹理失真。现有散景渲染方法（如 **BokehMe**，Peng et al., CVPR 2022；**Dr.Bokeh**，Sheng et al., CVPR 2024；**BokehDiff**，Zhu et al., arXiv 2025）普遍依赖高质量输入，难以应对此类退化场景。常见的两阶段方案——先用真实世界超分（Real-ISR，如 **OSEDiff**，Wu et al., NeurIPS 2024；**S3Diff**，Zhang et al., arXiv 2024）恢复图像细节，再执行散景渲染——存在误差累积与计算效率低下双重瓶颈。

本文提出 **MagicBokeh**，首个面向高倍变焦散景渲染的统一单步扩散框架。核心思路是：预训练扩散模型内蕴散景先验，通过**交替训练策略**解耦超分与散景优化，辅以**聚焦感知掩码注意力**（Focus-aware Mask Attention）利用散焦图调制自注意力，消除任务冲突；同时引入**退化感知深度模块**，以自特征蒸馏提升低质图像深度估计的鲁棒性。该框架在合成退化基准 EBB400-LQ 上取得 PSNR 24.23 dB、SSIM 0.7026、LPIPS 0.2786 的最优结果，推理时间仅 0.1062 秒（512×512 输入，L40s GPU），全面优于两阶段 SOTA 组合（Table 1）。真实世界高倍变焦移动摄影的用户偏好实验进一步验证了其视觉质量优势（Figure 5）。

消融实验确认：移除聚焦感知掩码注意力导致无参考指标 MUSIQ 从 58.83 降至 57.41；去除交替训练策略使 LPIPS 从 0.2786 退化为 0.2798；退化感知深度模块的移除在所有指标上均造成性能损失（Table 2）。这些结果共同支撑了“解耦训练+注意力调制+鲁棒深度估计”三位一体设计的有效性。

## 背景与动机

### 高倍变焦摄影中的散景渲染困境

散景（bokeh）渲染旨在模拟浅景深下的背景虚化效果，是计算摄影中的核心任务之一。近年来，基于学习的方法（如 **BokehMe** (Peng et al., CVPR 2022)、**Dr.Bokeh** (Sheng et al., CVPR 2024)、**BokehDiff** (Zhu et al., arXiv 2025)）在合成高质量散景方面取得了显著进展。然而，这些方法普遍假设输入为高质量（HQ）图像，在真实高倍变焦摄影场景下面临严峻挑战。

高倍变焦摄影的瓶颈在于：物理变焦放大导致图像分辨率下降，同时引入多种退化——噪声被放大、主体边界模糊、纹理细节丢失。当此类低质（LQ）图像直接输入现有散景渲染模型时，退化会与散景合成过程相互干扰，导致散景边界不自然、主体区域伪影严重，整体真实感大幅下降。

### 两阶段方案的固有问题

为解决上述困境，现有工作通常采用**两阶段级联**策略：先使用真实世界图像超分（Real-ISR）模型（如 **OSEDiff** (Wu et al., NeurIPS 2024)、**S3Diff** (Zhang et al., arXiv 2024)）将 LQ 图像恢复为 HQ 图像，再输入散景渲染模型生成最终效果。这一方案存在两个根本性缺陷：

1. **误差累积**：超分阶段的恢复误差（如纹理失真、伪影）会被散景渲染阶段继承并放大，导致最终输出质量受限于上游瓶颈。
2. **计算冗余与效率低下**：两个独立模型串行运行，推理时间长，难以满足移动端实时处理需求。此外，两阶段方案需要为散景渲染阶段单独生成视差图（通常使用 **Depth Anything v2** (Yang et al., NeurIPS 2024) 从超分后的 HQ 图像中估计），进一步增加了计算开销。

### 核心动机：统一框架下的任务协同

本文的核心动机在于突破两阶段范式的局限，提出一个**统一的单步扩散框架 MagicBokeh**，将 Real-ISR 与散景渲染联合优化。其关键洞察是：预训练的扩散模型内蕴丰富的散景先验，若能有效复用该先验并解耦两个任务的优化目标，即可在单一模型中同时实现高质量超分与真实感散景生成，从而消除级联误差并大幅提升推理效率。如图 2 所示，MagicBokeh 将超分与散景渲染无缝集成，避免了低分辨率散景渲染（a）的质量损失和两阶段方案（b）的效率问题，实现了计算效率与真实感散景效果的统一。

## 核心创新

MagicBokeh的核心创新在于将真实感散景渲染重新定义为一个**统一单步扩散生成问题**，从根本上改变了现有两阶段级联范式。具体而言，其关键创新体现在以下四个相互耦合的维度：

### 1. 统一单步扩散架构：消除级联误差与效率瓶颈

现有方案（如 **BokehMe** (Peng et al., CVPR 2022)、**Dr.Bokeh** (Sheng et al., CVPR 2024)、**BokehDiff** (Zhu et al., arXiv 2025)）普遍采用“先超分后散景”的两阶段管线：首先使用Real-ISR模型（如 **OSEDiff** (Wu et al., NeurIPS 2024)、**S3Diff** (Zhang et al., arXiv 2024)）对低质输入进行超分辨率重建，再将重建结果送入散景渲染模块。这一范式存在两个结构性缺陷：（1）超分阶段的误差会直接传递并放大至散景渲染阶段，形成误差累积；（2）两个独立模型串行推理导致计算冗余与延迟叠加。

MagicBokeh通过**单步扩散模型联合执行Real-ISR与散景渲染**，从架构层面消除了级联误差。其核心设计是将LQ图像直接输入HQ特征提取模块（由VAE编码器、剪枝U-Net与LoRA微调层构成），无需引入噪声即可恢复高质量特征表示；同时以散焦图（defocus map）为条件，通过ControlNet控制散景渲染的强度与焦点区域。该设计使得超分重建与散景生成在统一的特征空间中协同优化，而非割裂的串行处理。

### 2. 交替训练策略：解耦任务冲突

将超分与散景渲染纳入同一模型后，面临的核心挑战是两项任务的优化目标存在内在冲突：超分追求全图纹理细节的保真恢复，而散景渲染要求背景区域产生符合光学规律的模糊退化。直接端到端联合训练会导致梯度信号相互干扰，模型难以收敛至最优权衡点。

MagicBokeh提出**交替训练策略**来解耦这一冲突：训练过程在“Real-ISR阶段”与“散景渲染阶段”之间循环切换。在散景训练阶段，仅更新ControlNet与散景LoRA层，冻结超分相关参数；在Real-ISR训练阶段，仅更新超分LoRA层，冻结散景相关参数。消融实验（Table 2）证实，移除该策略后LPIPS从0.2786退化至0.2798，表明任务解耦训练有效缓解了优化冲突。

### 3. 聚焦感知掩码注意力：空间解耦的超分-散景协同

为进一步在特征层面实现主体超分与背景散景的解耦，MagicBokeh设计了**聚焦感知掩码注意力**（Focus-Aware Mask Attention, FAMA）。其核心机制是利用散焦图生成二进制掩码 $\mathbf{M}$，据此构造注意力调制矩阵 $\mathcal{M}$：

$$\mathcal { M } _ { ( x , y ) } = \begin{cases} 0 & \text{if } \mathbf{M}_{(x,y)}=1 \\ -\infty & \text{otherwise} \end{cases}$$

将该矩阵注入自注意力分数的计算过程：

$${\mathrm{Attention}} = {\mathrm{softmax}}\left( \frac { \mathbf{Q} \mathbf{K} ^ { \top } + {\mathcal{M}} } { \sqrt { d } } \right) \mathbf{V}$$

其效果是：聚焦区域（$\mathbf{M}_{(x,y)}=1$）内的token保持正常注意力交互，而跨区域（聚焦区与散焦区之间）的注意力权重被压制为0。这迫使模型在聚焦区域专注于超分重建的纹理细节恢复，在散焦区域专注于散景模糊的生成，避免两类操作在特征空间中相互污染。消融实验表明，移除FAMA导致无参考视觉质量指标MUSIQ从58.83显著下降至57.41，验证了其对视觉质量的关键作用。

### 4. 退化感知深度估计：低质输入的鲁棒视差获取

散景渲染的质量高度依赖准确的视差图（disparity map）来指导散焦模糊半径的计算。现有方案通常直接使用预训练深度模型（如 **Depth Anything v2** (Yang et al., NeurIPS 2024)）处理超分后的HQ图像，但这一做法在MagicBokeh的统一框架中不再适用——模型需直接从原始LQ输入估计视差图，而LQ图像中的噪声、模糊与压缩伪影会严重干扰深度估计精度。

MagicBokeh提出**退化感知深度模块**，采用**自特征蒸馏**框架来解决这一问题：以HQ图像经冻结的Depth Anything v2提取的特征作为教师信号，训练一个学生网络从对应的LQ图像中预测HQ-like特征，进而生成鲁棒的视差图。消融实验（Table 2）表明，移除该模块会在所有指标上造成性能退化，证实了鲁棒深度估计对统一框架的必要性。补充实验（Table s1）进一步显示，该模块在退化的NYUv2和KITTI基准上超越了原始Depth Anything v2。

## 整体框架

MagicBokeh 将真实图像超分辨率（Real‑ISR）与散景渲染统一到一个单步扩散框架中，避免了传统两阶段级联（先超分、后散景）带来的误差累积与冗余计算。其整体 pipeline 由四个核心模块串联构成：**高质量特征提取**、**退化感知深度估计**、**散焦图引导的可控散景渲染**，以及**聚焦感知掩码注意力**。输入为一张高倍变焦导致的低质（LQ）图像，输出为具有真实感散景效果的高分辨率图像。

### 信息流与模块关系

1. **HQ Feature Extraction（VAE + 剪枝 U‑Net + LoRA）**  
   将 LQ 图像直接送入预训练扩散模型的 VAE 编码器与剪枝后的 U‑Net，**不引入任何噪声**，通过 LoRA 微调恢复高质量特征表示。该模块为后续渲染提供具备丰富纹理与结构信息的 HQ 特征图。

2. **Degradation‑aware Depth Module**  
   从同一 LQ 输入估计视差图 $d$。该模块通过**自特征蒸馏**，以 HQ 图像深度特征为教师信号，提升低质图像深度估计的鲁棒性，为散焦图生成提供可靠的空间深度线索。

3. **Defocus Map 生成**  
   利用视差图 $d$ 与用户指定的焦点视差 $d_f$ 计算逐像素散景模糊半径：
   $$r = K \left| d - d _ { f } \right|$$
   其中 $K$ 控制全局模糊强度（模拟光圈大小）。由此得到的散焦图作为 ControlNet 的条件输入，决定每个像素的散景渲染强度。

4. **Controllable Bokeh Rendering（ControlNet + Bokeh LoRA）**  
   散焦图通过 ControlNet 注入扩散 U‑Net，与 HQ 特征共同驱动散景渲染。Bokeh LoRA 层在散景训练阶段学习可控的散景生成能力，实现焦点区域清晰、背景区域自然虚化的效果。

5. **Focus‑aware Mask Attention（FAMA）**  
   在自注意力层中，利用散焦图生成二进制聚焦掩码 $\mathbf{M}$，对注意力分数进行调制：
   $${\mathrm{Attention}} = {\mathrm{softmax}}\left( \frac { \mathbf{Q} \mathbf{K} ^ { \top } + {\mathcal{M}} } { \sqrt { d } } \right) \mathbf{V}$$
   其中掩码 $\mathcal{M}$ 定义为：
   $$\mathcal { M } _ { ( x , y ) } = \begin{cases} 0 & \text{if } \mathbf{M}_{(x,y)}=1 \\ -\infty & \text{otherwise} \end{cases}$$
   该机制强制前景（主体）与背景（散景区域）在注意力计算中相互隔离，解耦主体超分与背景虚化，有效消除任务冲突。

### 交替训练策略

上述模块并非端到端联合优化，而是采用**交替训练策略**解耦 Real‑ISR 与散景渲染两个子任务：
- **散景训练阶段**：冻结 SR LoRA，仅更新 ControlNet 与 Bokeh LoRA，学习可控散景渲染。
- **Real‑ISR 训练阶段**：冻结 Bokeh LoRA 与 ControlNet，仅更新 SR LoRA，学习低质图像超分。

这种循环交替的训练方式使模型在各自阶段专注单一目标，缓解了超分重建与散景生成之间的优化冲突，最终在推理时实现单步统一前向的高效、高质量散景渲染（Figure 3）。

![[assets/figures/papers/paper_list_l2055_https_arxiv_org_abs_2605_07429/figures/003_Figure_3.jpg]]
*Figure 3: The framework of MagicBokeh. We introduce an alternative training strategy to unified Real-ISR and bokeh rendering together. During the bokeh training, the Controlnet and bokeh LoRA layers are trainable to learn controllable bokeh rendering. During the Real-ISR training, only the SR LoRA is trainable to learn SR. During inference, given a high-zoom LQ photo, it can generate a disparity map through the degradation-aware depth model to guide bokeh rendering*

### 补充图表

![[assets/figures/papers/paper_list_l2055_https_arxiv_org_abs_2605_07429/figures/002_Figure_2.jpg]]
*Figure 2: Compared with low-resolution (LR) bokeh rendering (a) and two-stage super-resolution (SR) bokeh rendering (b), our proposed method (c) seamlessly integrates the SR with bokeh rendering within a unified framework, thereby achieving both computational efficiency and photorealistic bokeh effects*

![[assets/figures/papers/paper_list_l2055_https_arxiv_org_abs_2605_07429/figures/001_Figure_1.jpg]]
*Figure 1: MagicBokeh is the first unified method specifically designed for high-zoom bokeh rendering. (Zoom-in for best view)*

## 核心模块与公式推导

MagicBokeh 的整体架构由四个关键模块构成，围绕“预训练扩散模型内蕴散景先验”这一核心洞察，将真实世界图像超分辨率（Real-ISR）与散景渲染统一在单步扩散框架内。

### HQ 特征提取模块

该模块直接从低质量（LQ）输入图像提取高质量特征，**不引入任何噪声**。它以预训练 Stable Diffusion 的 VAE 编码器和 U-Net 为基础，但移除了所有交叉注意力层及中间模块（通过块剪枝实现），仅保留自注意力层与残差块。为恢复模型在 LQ 图像上的 HQ 特征提取能力，模块引入 LoRA 进行微调，使剪枝后 U-Net 能够输出可用于后续渲染的鲁棒特征表示。

### 可控散景渲染模块

以 ControlNet 为核心，该模块接收散焦图（defocus map）作为条件信号，控制散景渲染的强度与焦点区域。散焦图的计算公式为：

$$r = K \left| d - d_{f} \right|$$

其中 $r$ 表示像素级模糊半径，$d$ 为像素视差，$d_f$ 为焦点平面视差，$K$ 为控制模糊强度的缩放因子。通过调节 $d_f$，用户可以灵活指定焦点位置，实现重对焦等应用。

### 聚焦感知掩码注意力（FAMA）

为解耦前景主体的超分重建与背景区域的散景渲染，FAMA 利用散焦图生成二进制掩码 $\mathbf{M}$，调制 U-Net 自注意力层的注意力分数。调制后的注意力计算为：

$${\mathrm{Attention}} = {\mathrm{softmax}}\left( \frac { \mathbf{Q} \mathbf{K} ^ { \top } + {\mathcal{M}} } { \sqrt { d } } \right) \mathbf{V}$$

其中 $\mathcal{M}$ 为聚焦注意力掩码，其元素定义为：

$$\mathcal { M } _ { ( x , y ) } = \begin{cases} 0 & \text{if } \mathbf{M}_{(x,y)}=1 \\ -\infty & \text{otherwise} \end{cases}$$

该机制使前景像素（$\mathbf{M}_{(x,y)}=1$）仅关注前景区域，而背景像素仅关注背景区域，有效屏蔽了跨区域注意力，避免超分与散景任务间的特征干扰。

### 退化感知深度模块

针对 LQ 图像深度估计精度下降的问题，该模块采用**自特征蒸馏**框架：以 Depth Anything v2 作为教师模型，在高质量图像上提取深度特征；学生模型则从 LQ 图像中学习预测与教师特征对齐的 HQ 级深度表示。这一设计使深度估计对真实高倍变焦引入的噪声、模糊等退化具有鲁棒性，为散焦图生成提供可靠基础。

### 交替训练策略

上述模块通过**交替训练策略**协同优化：在散景训练阶段，ControlNet 与散景 LoRA 层可训练，学习可控散景渲染；在 Real-ISR 训练阶段，仅 SR LoRA 可训练，学习超分重建。这种解耦训练方式有效缓解了两任务联合优化时的目标冲突，使模型能够复用扩散先验同时保持各任务的独立性能。

### 补充图表

![[assets/figures/papers/paper_list_l2055_https_arxiv_org_abs_2605_07429/figures/011_Figure_S.1.jpg]]
*Figure S.1: The training pipeline of the DA depth module*

## 实验与分析

### 核心瓶颈与实验动机

现有散景渲染方法依赖高质量输入，当面对高倍变焦导致的低质图像时，噪声放大、边界模糊与纹理失真使得两阶段级联方案（先超分后散景）产生显著的误差累积，且推理效率低下。MagicBokeh 通过统一单步扩散框架，将 Real-ISR 与散景渲染联合优化，旨在从根本上消除任务冲突与级联误差。实验围绕三个核心问题展开：统一框架能否在合成退化场景下超越两阶段 SOTA 组合？各设计模块（交替训练、聚焦感知掩码注意力、退化感知深度估计）的独立贡献如何？真实世界高倍变焦移动摄影中的用户偏好是否支持方法的实用性？

### 主实验结果

#### 合成退化基准 EBB400-LQ

Table 1 给出了在 EBB400-LQ 数据集上的定量对比。MagicBokeh 在所有参考指标上均取得最优：PSNR 24.23 dB，SSIM 0.7026，LPIPS 0.2786，DISTS 0.1944，且推理时间仅 0.1062 秒（512×512 输入，L40s GPU），为所有对比方法中最快。对比的两阶段 SOTA 组合包括 OSEDiff（Wu et al., NeurIPS 2024）和 S3Diff（Zhang et al., arXiv 2024）作为 Real-ISR 前端，分别搭配 BokehMe（Peng et al., CVPR 2022）、Dr.Bokeh（Sheng et al., CVPR 2024）或 BokehDiff（Zhu et al., arXiv 2025）作为散景渲染后端。这些两阶段流水线在超分阶段引入的纹理失真与伪影会被后续散景模块进一步放大，而 MagicBokeh 的统一架构从机制上避免了这一误差累积路径。

![[assets/figures/papers/paper_list_l2055_https_arxiv_org_abs_2605_07429/figures/005_Table_1.jpg]]
*Table 1: Quantitative comparison of performance with two-stage SOTA models on EBB400-LQ benchmark. ISR methods use OSEDiff (*) and S3Diff(+). The inference times are tested with an input image of size 512 × 512, and the inference time is measured on an L40s GPU. Bold and underline denote the best and the second best result*

定性结果（Figure 4）进一步印证了数值优势：MagicBokeh 在焦点区域保持了更清晰的纹理细节，散景区域的光斑过渡更自然，而两阶段方法常出现焦点边界处的伪影或散景区域的块状模糊。

![[assets/figures/papers/paper_list_l2055_https_arxiv_org_abs_2605_07429/figures/004_Figure_4.jpg]]
*Figure 4: Qualitative comparison on EBB400-LQ. More results can be seen in the supplementary material*

#### 真实世界用户偏好

Figure 5 展示了真实高倍变焦移动摄影结果上的用户偏好实验。MagicBokeh 在所有对比方法中获得最优偏好，验证了统一框架在未知真实退化分布下的泛化能力。需要注意的是，真实场景的退化类型多样，合成训练管线能否完全覆盖未知分布仍是一个开放问题，但当前用户研究提供了正向实践证据。

![[assets/figures/papers/paper_list_l2055_https_arxiv_org_abs_2605_07429/figures/006_Figure_5.jpg]]
*Figure 5: The human preference on the real-world results*

### 消融实验

Table 2 系统拆解了三个关键设计的贡献，所有消融均在 EBB400-LQ 上进行。

![[assets/figures/papers/paper_list_l2055_https_arxiv_org_abs_2605_07429/figures/007_Table_2.jpg]]
*Table 2: Ablation study on the EBB400-LQ dataset. The setting of “FAMA”, “Strategy”, and “DA depth” are short for the focus-aware mask attention, alternate training strategy, and degradation-aware depth module respectively. Bold and underline denote the best and the second best result*

**聚焦感知掩码注意力（FAMA）**：移除 FAMA 后，无参考指标 MUSIQ 从 58.83 降至 57.41，MANIQA 和 CLIPIQA 也同步下降。这表明利用散焦图调制自注意力，强制前景超分与背景散景在特征层面解耦，对视觉质量有实质性提升。参考指标（PSNR/SSIM/LPIPS）变化相对温和，因为 FAMA 主要影响感知质量而非像素级保真度。

**交替训练策略（Strategy）**：去除交替训练、改用标准端到端联合优化后，LPIPS 从 0.2786 退化至 0.2798，其他参考指标也有轻微下降。该结果验证了 Real-ISR 与散景渲染存在目标冲突——前者追求高频细节恢复，后者需要在背景区域引入可控模糊——交替优化通过周期性切换任务焦点，有效缓解了这一冲突。不过，LPIPS 的退化幅度较小，提示冲突的严重程度可能受限于具体数据分布，交替频率的优化仍有探索空间。

**退化感知深度模块（DA depth）**：移除该模块、直接使用标准 Depth Anything v2（Yang et al., NeurIPS 2024）从 LQ 输入估计视差图，导致所有指标全面退化。这是三个消融中影响最显著的一项，证明在低质图像上鲁棒的深度估计是高质量散景渲染的前提条件。补充实验（Table S.1）在 NYUv2 和 KITTI 的合成退化版本上独立评估深度估计精度，DA depth 在 Degrade 场景下显著优于 Depth Anything v2，进一步支撑了这一结论。

Figure 6 提供了消融的可视化对比，直观展示了各模块对散景自然度和焦点区域清晰度的影响。

![[assets/figures/papers/paper_list_l2055_https_arxiv_org_abs_2605_07429/figures/008_Figure_6.jpg]]
*Figure 6: Visual comparison of the ablation study*

### 公平性说明

两阶段对比方法均先使用各自的 Real-ISR 模型进行超分，再使用 Depth Anything v2 从超分结果生成视差图；MagicBokeh 则直接从原始 LQ 输入通过退化感知深度模块估计视差图。输入条件不完全一致，但消融实验已单独量化了深度模块的贡献，且 Table S.1 的独立深度估计基准为公平比较提供了补充证据。此外，Table S.2 在 RealSR 和 DrealSR 真实世界超分基准上，通过输入全零散焦图生成全焦图像进行定量对比，MagicBokeh 仍取得有竞争力的结果，验证了其 Real-ISR 子任务的有效性。

### 失败模式与局限

论文未单独报告失败案例。从方法机制推断，潜在风险包括：退化感知深度模块在极端退化（如严重运动模糊、极低光照）下的估计误差可能传导至散景渲染，导致焦点区域误判；交替训练策略的收敛稳定性在更大规模数据或更长训练周期下未经充分验证。真实高倍变焦照片的退化类型远超合成管线覆盖范围，模型在未知退化上的鲁棒性仍需谨慎评估。

### 开放问题

1. 真实高倍变焦照片的退化分布未知，合成退化管线能否充分覆盖？当前用户偏好实验虽为正向，但样本量和场景多样性有限。
2. 模型在视频散景渲染上的时空一致性与推理效率如何？单帧 0.106 秒的推理速度对实时视频应用仍有差距。
3. 交替训练策略的最优交替频率与收敛稳定性是否存在理论指导？当前设计依赖经验设定。
4. 退化感知深度模块的自特征蒸馏范式在其他下游任务（如去模糊、超分）中的迁移效果如何？这关系到方法的通用性。

### 补充图表

![[assets/figures/papers/paper_list_l2055_https_arxiv_org_abs_2605_07429/figures/009_Figure_7.jpg]]
*Figure 7: Further application in refocusing*

![[assets/figures/papers/paper_list_l2055_https_arxiv_org_abs_2605_07429/figures/012_Table_S.1.jpg]]
*Table S.1: Quantitative comparison on the NYUv2 and KITTI datasets (seen datasets with synthetic degradations) for “Degrade”, “Clear”, and “Average” scenarios*

![[assets/figures/papers/paper_list_l2055_https_arxiv_org_abs_2605_07429/figures/013_Table_S.2.jpg]]
*Table S.2: Quantitative comparison with state-of-the-art methods on real-world benchmarks (RealSR and DrealSR ). By providing a defocus map with all-zero input, our method can generate a high-quality all-in-focus image for quantitative comparison. The best and second-best results are highlighted in bold and underline*

## 方法谱系与知识库定位

### 1. 方法沿革与基线对比

MagicBokeh 的核心定位是**面向高倍变焦摄影的统一单步散景渲染框架**。其直接对标的方法谱系可分为两类：两阶段级联方案与单阶段散景渲染方案。

**两阶段级联方案**是当前的主流范式，其基本流程为：先通过真实世界图像超分（Real-ISR）模型将低质（LQ）输入恢复为高质（HQ）图像，再通过散景渲染模型在 HQ 图像上合成散景效果。代表性组合包括 **OSEDiff**（Wu et al., NeurIPS 2024）或 **S3Diff**（Zhang et al., arXiv 2024）作为 ISR 前端，搭配 **BokehMe**（Peng et al., CVPR 2022）、**Dr.Bokeh**（Sheng et al., CVPR 2024）或 **BokehDiff**（Zhu et al., arXiv 2025）作为散景渲染后端。这类方案存在两个结构性瓶颈：① 两阶段独立优化导致误差累积，ISR 阶段引入的伪影或纹理失真会直接污染后续散景渲染；② 推理效率受限于串行流水线，难以满足移动端实时需求。

**单阶段散景渲染方案**（如直接对 LQ 图像施加散景模糊）虽然避免了级联误差，但受限于 LQ 输入本身的信息量，无法生成高质量的散景纹理与清晰的主体细节。MagicBokeh 的突破在于**将 Real-ISR 与散景渲染统一在单个扩散框架内，通过单步推理同时完成超分与散景生成**，从根本上消除了级联误差与效率瓶颈。

### 2. 关键差异机制

MagicBokeh 与两阶段基线的方法论差异体现在四个关键维度：

| 维度 | 两阶段基线 | MagicBokeh |
|------|-----------|------------|
| **流水线架构** | 串行级联（ISR → 散景渲染） | 统一单步扩散模型联合执行 |
| **训练策略** | 各阶段独立端到端优化 | 交替训练解耦 Real-ISR 与散景渲染 |
| **注意力机制** | 标准自注意力 | 聚焦感知掩码注意力（散焦图引导） |
| **深度估计** | Depth Anything v2（Yang et al., NeurIPS 2024）作用于 HQ 图像 | 退化感知深度模块，直接从 LQ 输入估计视差图 |

**交替训练策略**是解耦任务冲突的核心设计。Real-ISR 追求纹理锐化与细节恢复，而散景渲染需要在背景区域引入平滑模糊，两者优化方向存在内在矛盾。MagicBokeh 通过在 Real-ISR 阶段仅训练 SR LoRA 层、在散景渲染阶段仅训练 ControlNet 与 Bokeh LoRA 层，实现了任务间的显式解耦。消融实验（Table 2）表明，移除该策略会导致 LPIPS 从 0.2786 退化至 0.2798，验证了任务冲突缓解的有效性。

**聚焦感知掩码注意力**（Focus-Aware Mask Attention, FAMA）进一步强化了任务解耦。其核心机制为：利用散焦图生成二进制掩码 $\mathbf{M}$，在自注意力分数中加入调制项 $\mathcal{M}$：

$${\mathrm{Attention}} = {\mathrm{softmax}}\left( \frac { \mathbf{Q} \mathbf{K} ^ { \top } + {\mathcal{M}} } { \sqrt { d } } \right) \mathbf{V}$$

其中 $\mathcal{M}_{(x,y)} = 0$ 当 $\mathbf{M}_{(x,y)}=1$（前景区域），否则为 $-\infty$。这一设计强制前景区域的自注意力仅聚焦于前景 token，背景区域仅聚焦于背景 token，从而在特征层面实现主体超分与背景散景的彻底分离。消融实验显示，移除 FAMA 导致无参考指标 MUSIQ 从 58.83 降至 57.41，证明其对视觉质量有显著贡献。

**退化感知深度模块**解决了一个被两阶段方案忽视的关键问题：LQ 图像（尤其是高倍变焦导致的噪声放大、边界模糊）会严重破坏深度估计精度。两阶段方案将深度估计置于 ISR 之后，依赖 HQ 图像生成视差图，但这一设计在 MagicBokeh 的统一框架中不可行——模型需要直接从 LQ 输入获取散焦图以控制渲染。MagicBokeh 通过自特征蒸馏（self-feature distillation）框架，以 HQ 图像的特征为教师信号训练 LQ 深度估计器，显著提升了退化场景下的鲁棒性。消融实验（Table 2）证实，移除该模块会在所有指标上造成性能退化。

### 3. 适用边界与局限

根据论文提供的证据，MagicBokeh 的适用边界可归纳如下：

**已验证的有效场景**：
- 高倍变焦移动摄影的散景渲染（Figure 5 用户偏好最优）
- 合成退化数据集 EBB400-LQ（Table 1 全面 SOTA）
- 重对焦应用（Figure 7 展示）

**需手动验证的潜在局限**（论文未提供明确实验证据）：
- **视频散景渲染的时空一致性**：当前设计为单帧推理，未讨论时序约束或帧间一致性机制，视频场景下的 flickering 问题需要手动验证。
- **极端退化类型的覆盖**：EBB400-LQ 的合成退化管线能否覆盖真实世界中多样化的高倍变焦退化分布（如运动模糊、压缩伪影、传感器噪声的复杂耦合），论文未提供分布外泛化实验。
- **交替训练的收敛特性**：交替频率、任务配比等超参数对收敛稳定性的影响未做敏感性分析，最优训练策略是否具有普适性仍需验证。

### 4. 开放问题

1. **退化泛化边界**：合成退化管线（Figure S.2）与真实高倍变焦退化分布之间的 gap 有多大？在极端低光、强噪声场景下，退化感知深度模块的鲁棒性是否依然成立？

2. **时空扩展性**：MagicBokeh 的单步推理效率（512×512 输入仅需 0.1062s，L40s GPU）为视频处理提供了可能性，但自注意力机制的帧间扩展方案（如时序注意力）尚未探索。

3. **退化感知深度的迁移价值**：自特征蒸馏框架本质上是退化鲁棒的特征学习策略，其在其他退化敏感的下游任务（如去模糊、去噪、低光增强）中的迁移效果值得进一步研究。

4. **可控性的粒度**：当前散景控制依赖散焦图（模糊半径 $r = K |d - d_f|$）与焦点视差 $d_f$，但散景形状、口径蚀、二线性等更精细的光学特性控制尚未纳入框架。

## 原文 PDF

![[paperPDFs/CVPR_2026/Towards_Photorealistic_and_Efficient_Bokeh_Rendering_via_Diffusion_Framework.pdf]]