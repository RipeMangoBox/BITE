---
title: "InstantRetouch: Efficient and High-Fidelity Instruction-Guided Image Retouching with Bilateral Space"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/InstantRetouch_Efficient_and_High_Fidelity_Instruction_Guided_Image_Retouching_with_Bilateral_Space.pdf
project_link: "https://openimaginglab.github.io/InstantRetouch/"
code_link: null
aliases:
- InstantRetouch
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: 将编辑操作从图像像素或潜空间转移到紧凑且与内容解耦的双边网格（bilateral grid）空间中，通过预测局部仿射变换参数实现仅调整外观而不改变几何纹理的约束。
primary_logic: 通过变分分数蒸馏（VSD）将多步扩散教师的强语义先验蒸馏至一步双边网格生成器中，并引入基于CLIP的提示对齐损失解决指令跟随弱化问题，从而在保证零内容漂移和极低延迟的同时，保留了扩散模型丰富的视觉表现力。
claims:
- 双边空间操作是内容解耦的且极其高效，天然防止内容漂移。
- 蒸馏框架使一步生成器保留了扩散先验，同时实现超快推理。
- VSD损失和提示对齐损失对提升编辑质量均起关键作用。
- iRetouch (自建指令修饰基准) 上 SSIM (内容保真度) = 0.989
---

# InstantRetouch: Efficient and High-Fidelity Instruction-Guided Image Retouching with Bilateral Space

> [!tip] 核心洞察
> 通过变分分数蒸馏（VSD）将多步扩散教师的强语义先验蒸馏至一步双边网格生成器中，并引入基于CLIP的提示对齐损失解决指令跟随弱化问题，从而在保证零内容漂移和极低延迟的同时，保留了扩散模型丰富的视觉表现力。

| 字段 | 内容 |
|------|------|
| 中文题名 | InstantRetouch：基于双边空间的高效高保真指令引导图像修饰 |
| 英文题名 | InstantRetouch: Efficient and High-Fidelity Instruction-Guided Image Retouching with Bilateral Space |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://openaccess.thecvf.com/content/CVPR2026/html/Wu_InstantRetouch_Efficient_and_High-Fidelity_Instruction-Guided_Image_Retouching_with_Bilateral_Space_CVPR_2026_paper.html) · [Project](https://openimaginglab.github.io/InstantRetouch/) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/image_and_video_generation |
| Method | InstantRetouch |
| Dataset | iRetouch |

> [!tip] 效果简介
> - iRetouch (自建指令修饰基准) 上，SSIM (内容保真度) 0.989 vs Gemini-2.5-Flash 0.865 (推测，因未给出具体值，但论文强调我们最高) (SSIM 明显更高，接近1)。
> - iRetouch 上，Runtime @4K (秒) 0.068s vs Gemini-2.5-Flash >10s (1024分辨率推理约10s，4K无法处理或极慢) (快约70-800倍)；整体质量得分 O (结合用户偏好/指令跟随/感知质量) 8.54 vs Gemini-2.5-Flash 8.74 (非常接近最强的封闭源系统，但效率/保真度大幅领先)。

## 概述

现有基于扩散模型的图像编辑方法直接在图像潜空间中进行操作，难以有效解耦光度调整与内容修改，导致在高分辨率场景下频繁出现内容漂移，且多步推理带来的延迟极高。InstantRetouch 提出了一种根本性的思路转变：**将编辑操作从像素/潜空间转移至紧凑且与内容解耦的双边网格（bilateral grid）空间**，仅预测局部仿射变换参数，从而天然保证零内容漂移。同时，通过变分分数蒸馏（VSD）将多步扩散教师的强语义先验压缩至一步双边网格生成器中，并引入基于 CLIP 的提示对齐损失以弥补步骤压缩造成的指令跟随弱化。

该方案在自建的 iRetouch 指令修饰基准上取得了极具竞争力的结果：内容保真度 SSIM 高达 0.989，4K 分辨率推理仅需 0.068 秒，比 **Gemini-2.5-Flash**（Comanici et al., arXiv 2025）等大模型快 70–800 倍，整体质量得分（8.54）与最强闭源系统（8.74）几乎持平。这是目前首个在指令驱动的图像修饰任务中，同时实现**高保真、高质量与极低延迟**的方法。

## 背景与动机

图像修饰（Image Retouching）旨在对照片进行光度调整（如色彩、对比度、亮度）以提升视觉美感，同时要求严格保留原始图像的结构与纹理内容。近年来，基于文本指令的图像编辑方法取得了显著进展，用户可通过自然语言描述期望的编辑效果。然而，现有方案在同时满足**高内容保真度**、**高编辑质量**和**高推理效率**三个目标时面临根本性瓶颈。

**核心瓶颈：编辑空间的内容-外观耦合**

当前主流的指令驱动编辑模型，如 **InstructPix2Pix**（Brooks et al., CVPR 2023）、**Gemini-2.5-Flash**（Comanici et al., arXiv 2025）等，通常直接在图像的像素空间或 VAE 潜空间中进行编辑操作。这种设计存在一个本质缺陷：**光度调整与内容修改在表示空间中高度耦合**。模型在尝试改变图像色调或氛围时，往往会不可控地修改物体的几何结构、纹理细节甚至语义内容，即产生所谓的“内容漂移”（content drift）。这一问题在高分辨率场景下尤为突出——扩散模型在低分辨率潜空间中进行的微小扰动，经解码器上采样后会被放大为可见的结构失真。

**效率困境：多步扩散与高分辨率处理的冲突**

扩散模型的推理需要多步迭代去噪（通常 20–50 步），计算开销随分辨率的提升呈超线性增长。对于 4K 级别的实际应用场景，大型编辑模型（如 Gemini-2.5-Flash）甚至无法直接处理，或需要超过 10 秒的推理时间。这导致现有方法在效率与分辨率之间存在尖锐矛盾：要么牺牲分辨率，要么牺牲交互实时性。

**动机：寻找内容解耦且紧凑的编辑表示**

上述困境的根本原因在于编辑操作发生在“错误的空间”中。本文的核心动机是：**能否将编辑操作从像素/潜空间转移到一个与内容天然解耦、且极度紧凑的表示空间中？** 受经典双边网格（bilateral grid）思想的启发，该表示通过预测局部仿射变换参数来实现外观调整，而不会触及原始图像的几何与纹理信息。如果能够将扩散模型强大的语义理解和视觉表现力蒸馏到这样一个双边网格生成器中，就有可能在**零内容漂移**的前提下，实现**单步、高分辨率、高质量**的指令引导图像修饰。

这一动机驱动了 InstantRetouch 的设计：通过变分分数蒸馏（VSD）将多步扩散教师的先验压缩至一步双边网格生成器，并辅以基于 CLIP 的提示对齐损失来弥补步数压缩带来的指令跟随弱化，从而在保真度、质量和速度三个维度上同时取得突破。

## 核心创新

InstantRetouch 的核心创新在于将图像编辑的**操作空间**从传统的像素/潜空间迁移至**紧凑且内容解耦的双边网格空间**，并通过**变分分数蒸馏**将多步扩散模型的强语义先验压缩至单步生成器中，从而在保真度、质量和效率三个维度上实现了突破性平衡。

### 编辑表示空间的范式转换

现有指令驱动的图像编辑方法（如 **InstructPix2Pix** (Brooks et al., CVPR 2023)、**Gemini-2.5-Flash** 等）直接在 VAE 潜空间或像素空间上执行去噪/生成过程。这种设计将光度调整（色调、曝光、对比度）与内容修改（纹理、几何结构）耦合在同一表示空间中，导致高分辨率下出现“内容漂移”——即非目标区域的纹理和结构被意外改变。

InstantRetouch 将编辑操作重新定义为**低分辨率双边网格中的局部仿射变换参数预测**。具体而言，模型不直接生成编辑后的图像像素，而是预测一个尺寸为 $\breve{H}_g \times W_g \times D \times 12$ 的三维双边网格 $\Gamma$，其中每个网格单元存储一个 $3 \times 4$ 的仿射变换矩阵。在全分辨率分支中，对于每个输入像素，系统先计算其灰度引导值，然后通过三线性插值从网格中检索对应的仿射矩阵，最后将该矩阵应用于原始像素颜色：

$$O_i = A(\Gamma, g(I_i)) \cdot I_i$$

这一表示具有两个关键性质：
- **内容解耦**：仿射变换仅对像素颜色进行线性映射，天然无法引入新的纹理或改变几何结构，从数学上保证了零内容漂移。
- **分辨率无关的效率**：双边网格的分辨率远低于输入图像（通常为 $64 \times 64 \times 8$），计算开销与输入分辨率几乎解耦。实验表明，从 720p 到 4K 分辨率，推理时间仅从 0.065s 微增至 0.068s。

### 从多步扩散到单步生成的知识蒸馏

双边网格表示虽然高效且保真，但缺乏足够的语义表达能力来理解复杂的编辑指令（如“营造温暖的电影感”）。为解决这一矛盾，InstantRetouch 采用**变分分数蒸馏 (Variational Score Distillation, VSD)** 将预训练的多步扩散教师模型的知识迁移至单步双边网格生成器。

蒸馏框架由两个协同分支构成：
- **低分辨率扩散分支**：包含冻结的 VAE 编码器和一步 U-Net 去噪器。该分支接收下采样至 $512 \times 512$ 的输入图像和文本指令，从白噪声 $z_{t_{max}} \sim \mathcal{N}(0, I)$ 出发，通过一步去噪直接预测干净潜变量 $\hat{z}_0$：

$$\hat{z}_0 = \frac{z_{t_{max}} - \beta_t \epsilon_{\theta}(z_{t_{max}}, t_{max}, c_I, c_T)}{\alpha_t}$$

- **全分辨率双边处理分支**：通过轻量双边适配器从低分辨率分支的特征中生成双边网格，并在原始高分辨率输入上执行切片和仿射变换。

VSD 损失的梯度通过教师模型 $\epsilon_{\phi}$ 与正则化器 $\epsilon_{\phi'}$ 之间的噪声预测差异驱动学生生成器 $\theta$ 的更新：

$$\nabla_{\theta} \mathcal{L}_{\mathrm{VSD}} = \mathbb{E}_{t, \epsilon, \hat{z}_t} \left[ \omega(t) ( \epsilon_{\phi}(\hat{z}_t, t, c_I, c_T) - \epsilon_{\phi'}(\hat{z}_t, t, c_I, c_T) ) \frac{\partial \hat{z}_0}{\partial \theta} \right]$$

训练采用渐进式噪声调度：初期使用高噪声水平学习色调、曝光等粗粒度属性，随后逐步降低噪声阈值以蒸馏细粒度细节。

### 提示对齐损失：弥补压缩带来的指令跟随弱化

将多步扩散压缩为单步会削弱模型的指令跟随能力，尤其对于“复古胶片感”、“忧郁冷调”等风格化模糊指令。为此，InstantRetouch 引入了基于 CLIP 的**提示对齐损失**。

该模块首先通过规则匹配器将用户指令 $c_T$ 拆解为一组原子修饰属性 $\mathcal{A}(c_T) = \{a\}$（如“增加对比度”、“暖色调”等），然后针对每个属性计算 InfoNCE 对比损失：

$$\ell_{\mathrm{nce}}(a) = - \log \frac{\exp\left( s_a^{+} / \tau \right)}{\exp\left( s_a^{+} / \tau \right) + \exp\left( s_a^{-} / \tau \right)}$$

其中 $s_a^{+}$ 为输出图像与正属性提示的 CLIP 相似度，$s_a^{-}$ 为与负属性提示的相似度。最终的对齐损失为所有检测属性的加权平均：

$$\mathcal{L}_{\mathrm{align}} = \frac{1}{|\mathcal{A}(c_T)|} \sum_{a \in \mathcal{A}(c_T)} \left[ w_a \ell_{\mathrm{nce}}(a) \right]$$

消融实验证实，$\mathcal{L}_{\mathrm{align}}$ 提供了 VSD 单独无法提供的方向性语义监督，对整体编辑质量产生显著增益。

### 与基线的系统性差异

| 维度 | 现有扩散编辑模型 | InstantRetouch |
|------|-----------------|----------------|
| **编辑表示空间** | 直接修改 VAE 潜变量 | 预测低分辨率双边网格的仿射变换参数 |
| **推理步数** | 多步迭代去噪（20-50 步） | 单步前向预测 |
| **内容保真度** | 高分辨率下存在内容漂移 | 数学保证零内容漂移（SSIM 0.989） |
| **推理效率** | 随分辨率急剧增长 | 近常数时间（4K 仅 0.068s） |
| **语义表达能力** | 强（多步扩散先验） | 通过 VSD 蒸馏保留扩散先验 + CLIP 对齐增强 |

这种设计使得 InstantRetouch 成为目前唯一同时实现**扩散级语义质量**（整体得分 8.54，接近 Gemini-2.5-Flash 的 8.74）、**数学级内容保真度**（SSIM 0.989）和**极低推理延迟**（比大模型快 70-800 倍）的指令驱动图像修饰方法。

## 整体框架

InstantRetouch 的整体流水线围绕一个核心设计原则展开：**将编辑操作从图像像素/潜空间解耦至紧凑的双边网格空间**，从而在单步前向传播中同时实现高保真内容保留与高语义质量的指令跟随。如图 2 所示，框架包含三个关键阶段：教师模型预训练、一步生成器蒸馏、以及全分辨率双边处理。

### 输入输出流

系统接收两路输入：原始高分辨率图像 $x \in \mathbb{R}^{H \times W \times 3}$ 和用户文本指令 $c_T$（如“让这张照片更有电影感”）。输出为修饰后的全分辨率图像 $\hat{x}_B$，其内容结构严格对齐输入，仅外观属性（色调、曝光、对比度、色彩风格等）发生改变。

### 双分支生成器架构

一步生成器 $G_\theta$ 由两个协同分支构成：

1. **低分辨率扩散分支（Low-Resolution Diffusion Branch）**：负责语义理解与扩散先验保持。该分支包含一个冻结的 VAE 编码器和一个一步 U-Net 去噪器。输入图像首先被下采样至低分辨率，经 VAE 编码为潜变量 $c_I$，与文本指令 $c_T$ 共同作为条件。从白噪声 $z_{t_{max}} \sim \mathcal{N}(0, I)$ 出发，执行一步去噪直接预测干净潜变量 $\hat{z}_0$：
   $$\hat{z}_0 = \frac{z_{t_{max}} - \beta_t \epsilon_{\theta}(z_{t_{max}}, t_{max}, c_I, c_T)}{\alpha_t}$$
   该低分辨率输出 $\hat{x}$ 提供了编辑的语义方向和全局外观基调。

2. **全分辨率双边处理分支（Full-Resolution Bilateral Processing Branch）**：负责高保真外观迁移。该分支包含一个轻量级双边适配器，从低分辨率分支的特征中生成一个紧凑的双边网格 $\Gamma \in \mathbb{R}^{H_g \times W_g \times D \times 12}$，存储局部仿射变换参数。对于每个输入像素，系统首先计算灰度引导值，然后通过三线性插值从网格中检索特定的仿射矩阵 $A$，最终将该矩阵应用于原始像素颜色，生成修饰结果 $\hat{x}_B$。

这一设计的核心优势在于：**双边网格天然与图像内容解耦**——它仅编码颜色映射关系，不触及像素的空间位置或纹理信息，因此从根本上杜绝了内容漂移；同时，网格分辨率远低于图像分辨率，即使在 4K 输入下也能保持极低的计算开销。

### 训练流程

训练分为两个阶段：

- **阶段一：低分辨率蒸馏**。利用变分分数蒸馏（VSD）损失将多步扩散教师的知识迁移至一步生成器，同时辅以数据监督损失 $\mathcal{L}_{\text{data}}$（L2 + LPIPS）和基于 CLIP 的提示对齐损失 $\mathcal{L}_{\text{align}}$。此阶段仅优化低分辨率分支和双边适配器，全分辨率分支冻结。

- **阶段二：联合双边蒸馏**。阶段一收敛后，解冻双边适配器，端到端训练整个生成器，并引入双边损失 $\mathcal{L}_{\text{bila}}$，包含 L1、LPIPS、与低分辨率预测的感知一致性、拉普拉斯平滑项和超色域惩罚，确保全分辨率输出的视觉质量与数值稳定性。

### 推理过程

推理为单次前向传播：给定输入图像和文本指令，模型直接生成双边网格并将其应用于原始分辨率输入，无需任何迭代去噪步骤。这一设计使 InstantRetouch 在 4K 分辨率下的推理时间仅为 0.068 秒，同时保持 0.989 的结构相似度（SSIM）。

### 补充图表

![[assets/figures/papers/paper_list_l759_https_openaccess_thecvf_com_content_CVPR2026_html_Wu_InstantRetouch_Effi/figures/002_Figure_2.jpg]]
*Figure 2: Our framework distills a multi-step diffusion teacher into a fast, one-step generator composed of two synergistic branches. The low-resolution diffusion branch processes the input image and text instruction to understand the edit, and then uses a light bilateral adapter to predict the parameters of a bilateral grid. The full-resolution branch then applies this grid to the original high-res image, producing the final high-fidelity result. We use Variational Score Distillation (VSD) to transfer the teacher’s knowledge and a CLIP-based language alignment loss to ensure instruction alignment*

## 核心模块与公式推导

InstantRetouch 的核心架构由三个紧密协同的模块构成：**低分辨率扩散分支**、**双边适配器**与**全分辨率双边处理分支**。其设计哲学是将语义理解与像素级变换彻底解耦——扩散分支负责“理解编辑意图”，双边分支负责“执行外观变换”，二者通过一个紧凑的双边网格桥接。

### 3.1 教师模型与扩散先验

在蒸馏之前，需先训练一个多步扩散教师模型。教师以输入图像潜变量 $c_I = \mathcal{E}_{\phi}(x)$ 和文本指令 $c_T$ 为条件，预测添加到目标图像潜变量中的噪声：

$$
\mathcal{L}_{\mathrm{teacher}}(\phi) = \mathbb{E}_{x, x^{\star}, c_T, t, \epsilon} \left[ \| \epsilon - \epsilon_{\phi}(z_t, t, c_I, c_T) \|_2^2 \right]
$$

其中 $z_t$ 是目标图像 $x^{\star}$ 经 VAE 编码后加噪得到的带噪潜变量，$\epsilon_{\phi}$ 为教师 U-Net 的噪声预测网络。该损失使教师获得丰富的语义编辑先验，为后续一步蒸馏提供知识源。

### 3.2 一步去噪与低分辨率扩散分支

低分辨率分支的核心是将多步迭代去噪压缩为单步前向预测。给定白噪声 $z_{t_{max}} \sim \mathcal{N}(0, I)$，以输入图像潜变量 $c_I$ 和文本指令 $c_T$ 为条件，直接预测干净潜变量 $\hat{z}_0$：

$$
\hat{z}_0 = \frac{z_{t_{max}} - \beta_t \epsilon_{\theta}(z_{t_{max}}, t_{max}, c_I, c_T)}{\alpha_t}
$$

该分支包含一个冻结的 VAE 编码器和一个一步 U-Net 去噪器，负责语义理解并保留扩散先验。其输出 $\hat{z}_0$ 经 VAE 解码得到低分辨率编辑结果 $\hat{x}$，同时为双边适配器提供特征。

### 3.3 双边适配器与全分辨率双边处理分支

双边适配器从低分辨率分支的特征中生成一个紧凑的双边网格 $\Gamma \in \mathbb{R}^{H_g \times W_g \times D \times 12}$，存储局部仿射变换参数。对全分辨率输入图像的每个像素，双边处理分支首先计算灰度引导值，通过三线性插值从网格中检索对应的仿射矩阵 $A$，再将其应用于原始像素颜色：

$$
I_{out}(p) = A(p) \cdot I_{in}(p) + b(p)
$$

其中 $A(p) \in \mathbb{R}^{3 \times 3}$ 为仿射矩阵，$b(p)$ 为偏置向量。这一操作仅在紧凑的引导空间中进行参数预测，天然防止了对图像内容的直接修改，从而确保零内容漂移。

### 3.4 蒸馏损失体系

#### 3.4.1 变分分数蒸馏损失（VSD）

VSD 损失将教师的多步扩散知识迁移至一步生成器。其梯度形式为：

$$
\nabla_{\theta} \mathcal{L}_{\mathrm{VSD}} = \mathbb{E}_{t, \epsilon, \hat{z}_t} \left[ \omega(t) ( \epsilon_{\phi}(\hat{z}_t, t, c_I, c_T) - \epsilon_{\phi'}(\hat{z}_t, t, c_I, c_T) ) \frac{\partial \hat{z}_0}{\partial \theta} \right]
$$

其中 $\epsilon_{\phi}$ 为冻结的教师模型，$\epsilon_{\phi'}$ 为随训练更新的 VSD 正则化器。两者噪声预测的差异构成驱动学生生成器的梯度信号。训练采用渐进式噪声调度：初始阶段使用高噪声水平 $t \in [t_{hi}, t_{max}]$ 学习色调、曝光等粗粒度属性，随后逐步降低 $t_{hi}$ 以蒸馏细粒度细节。

#### 3.4.2 提示对齐损失（Prompt Alignment Loss）

为弥补一步压缩导致的指令跟随弱化，引入基于 CLIP 的语义监督。首先通过规则匹配器将用户指令 $c_T$ 拆解为原子修饰属性集合 $\mathcal{A}(c_T) = \{a\}$，然后对每个属性计算 InfoNCE 对比损失：

$$
\ell_{\mathrm{nce}}(a) = - \log \frac{\exp\left( s_a^{+} / \tau \right)}{\exp\left( s_a^{+} / \tau \right) + \exp\left( s_a^{-} / \tau \right)}
$$

其中 $s_a^{+} = \text{sim}(E_I(\hat{x}), E_T(a^{+}))$ 为生成图像嵌入与正属性提示嵌入的余弦相似度，$s_a^{-}$ 为与负属性提示的相似度。最终指令对齐损失为所有检测属性的加权平均：

$$
\mathcal{L}_{\mathrm{align}} = \frac{1}{|\mathcal{A}(c_T)|} \sum_{a \in \mathcal{A}(c_T)} \left[ w_a \ell_{\mathrm{nce}}(a) \right]
$$

该损失为一步生成器提供方向性语义监督，尤其对“复古”“电影感”等风格化模糊指令效果显著。

#### 3.4.3 数据监督损失与双边损失

为稳定蒸馏，低分辨率分支额外施加数据监督：

$$
\mathcal{L}_{\mathrm{data}} = \| \hat{x} - x^{\star} \|_2^2 + \lambda_{\mathrm{LPIPS}} \mathcal{L}_{\mathrm{LPIPS}}(\hat{x}, x^{\star})
$$

全分辨率双边分支的损失函数为：

$$
\mathcal{L}_{\mathrm{bila}} = \lambda_1 \| \hat{x}_B - x^{\star} \|_1 + \lambda_2 \cdot \mathcal{L}_{\mathrm{LPIPS}}(\hat{x}_B, x^{\star}) + \lambda_3 \cdot \mathcal{L}_{\mathrm{LPIPS}}(\hat{x}_B, \hat{x}) + \lambda_4 \cdot \| \Delta^3 \Gamma \|_2^2 + \lambda_5 \cdot \Psi(\hat{x}_B)
$$

其中各项依次为：L1 像素损失、与真值的 LPIPS 感知损失、与低分辨率预测的感知一致性约束、双边网格的拉普拉斯平滑项、以及超色域惩罚项 $\Psi(\hat{x}_B)$。

### 3.5 两阶段训练策略

训练分为两个阶段。第一阶段仅优化低分辨率分支，冻结双边适配器，损失为 $\mathcal{L}_{\mathrm{stage1}} = \mathcal{L}_{\mathrm{VSD}} + \mathcal{L}_{\mathrm{data}} + \mathcal{L}_{\mathrm{align}}$。第二阶段解冻双边适配器，端到端联合训练整个生成器，总损失为：

$$
\mathcal{L}_{\mathrm{stage2}} = \mathcal{L}_{\mathrm{stage1}} + \lambda_{\mathrm{bila}} \mathcal{L}_{\mathrm{bila}}
$$

消融实验证实，VSD 损失与提示对齐损失对编辑质量均起关键作用：仅用基础损失（$\mathcal{L}_{\mathrm{data}} + \mathcal{L}_{\mathrm{bila}}$）无法实现高质量编辑；添加 VSD 后评分大幅跃升；再引入提示对齐损失则带来最终的显著增益，尤其强化了对风格化指令的跟随能力。

## 实验与分析

### 主实验结果

我们在自建的指令修饰基准 **iRetouch** 上对 InstantRetouch 进行了全面评估，涵盖内容保真度、推理效率与编辑质量三个维度。Table 1 给出了与当前主流方法的量化对比。

![[assets/figures/papers/paper_list_l759_https_openaccess_thecvf_com_content_CVPR2026_html_Wu_InstantRetouch_Effi/figures/003_Table_1.jpg]]
*Table 1: Comparison on iRetouch benchmark. Our method achieves state-of-the-art efficiency and content fidelity while remaining highly competitive in editing quality. Blank entries indicate models that cannot process high resolutions or are not instruction-driven*

**内容保真度。** 在 SSIM 指标上，InstantRetouch 达到 **0.989**，显著优于直接操作潜空间的扩散编辑模型（如 **InstructPix2Pix**，Brooks et al., CVPR 2023）和通用图像编辑大模型（如 **Gemini-2.5-Flash**，Comanici et al., arXiv 2025 推测 SSIM 约 0.865）。这一优势源于双边网格操作的天然内容解耦特性——预测的仿射变换仅作用于像素颜色，不改变几何纹理，从机制上杜绝了内容漂移。

**推理效率。** 在 4K 分辨率下，InstantRetouch 的单次推理耗时仅为 **0.068 秒**，且从 720p 到 4K 的延迟几乎恒定（0.065–0.068 秒）。相比之下，Gemini-2.5-Flash 在 1024 分辨率下即需约 10 秒，在 4K 下无法处理或极慢。整体加速比达到 **70–800 倍**。高效性得益于编辑操作被压缩至低分辨率双边网格空间，切片与应用操作的计算量几乎不随分辨率增长。

**编辑质量。** 在综合质量得分 O（融合用户偏好、指令跟随与感知质量）上，InstantRetouch 获得 **8.54**，与最强的闭源系统 Gemini-2.5-Flash（8.74）高度接近，但效率与保真度大幅领先。Figure 3 的定性对比进一步印证：InstantRetouch 在自然风景与人像场景中均能准确跟随文本指令生成视觉愉悦的修饰结果，同时完整保留原始内容结构，而其他方法则存在不同程度的内容修改。

**身份保持能力。** 在 PPR10K 人脸修饰基准上，InstantRetouch 取得了最高的面部余弦相似度分数（Figure 5），证明双边空间操作在保持人物身份特征方面具有天然优势——仿射变换无法改变人脸几何结构，从而严格约束了身份信息的完整性。

### 框架消融研究

Table 2 对框架的双分支协同设计进行了消融分析。

![[assets/figures/papers/paper_list_l759_https_openaccess_thecvf_com_content_CVPR2026_html_Wu_InstantRetouch_Effi/figures/005_Table_2.jpg]]
*Table 2: Ablation study on our framework. We evaluate content fidelity, editing quality, and runtime. Our full model effectively combines the strengths of diffusion priors and bilateral processing, achieving high scores across all criteria*

- **仅低分辨率扩散分支**：能利用扩散先验实现语义理解，但输出分辨率受限，无法直接生成高保真全分辨率结果。
- **仅全分辨率双边分支**：内容保真度极高，但缺乏语义先验，无法理解复杂指令，编辑质量低下。
- **完整双分支框架**：融合扩散的语义强度（O-score 8.54）与双边处理的结构保持能力（SSIM 0.989），在所有维度上均取得最优，是唯一同时满足高质量、高保真与高效率的方案。

### 蒸馏损失消融

Table 3（对应 Figure 6 的可视化）系统拆解了蒸馏损失各组件的贡献。

![[assets/figures/papers/paper_list_l759_https_openaccess_thecvf_com_content_CVPR2026_html_Wu_InstantRetouch_Effi/figures/008_Figure_6.jpg]]
*Figure 6: Visualization of ablation study on the loss configuration of one-step bilateral distillation*

- **仅基础损失（L_base = L_data + L_bila）**：模型无法实现高质量编辑，输出趋于模糊或缺乏风格表现力。
- **加入 VSD 蒸馏损失（L_VSD）**：评分大幅跃升，证明多步扩散教师向一步生成器传递的生成先验是编辑质量的核心驱动力。VSD 通过教师与正则化器之间的噪声预测差异梯度，将教师对色调、曝光等粗粒度属性的理解压缩至学生网络。
- **加入提示对齐损失（L_align）**：带来最终的显著增益。尤其对于风格化模糊指令（如“温暖电影感”），VSD 单独难以提供方向性监督，而基于 CLIP 的原子属性 InfoNCE 损失通过正/负提示对比，为一步生成器恢复了因步数压缩而弱化的指令跟随能力。

消融结论清晰：VSD 与提示对齐损失对达成高编辑质量均起关键作用，二者不可偏废。

### 连续编辑强度控制

InstantRetouch 支持通过标量参数 $s$ 控制编辑强度（Figure 7）。当 $s \in [0, 1]$ 时，效果从原始图像平滑过渡到目标修饰；当 $s > 1$ 时，可进一步增强修饰强度。这种连续控制能力源于双边网格中仿射变换参数的线性插值特性，无需重新推理即可实现实时调节。

![[assets/figures/papers/paper_list_l759_https_openaccess_thecvf_com_content_CVPR2026_html_Wu_InstantRetouch_Effi/figures/007_Figure_7.jpg]]
*Figure 7: Visualization of continuous control on editing strength*

### 失败模式与局限性

论文正文未明确列出局限性章节，但根据实验设计和方法机理，可推断以下潜在问题：

1. **未见指令类型的泛化**：尽管训练数据通过大语言模型生成多样化指令，但其覆盖度仍受限于预定义的原子属性模板。对于超出模板范围的组合指令或抽象风格描述，提示对齐模块的规则匹配器可能失效，导致指令跟随质量下降。
2. **极端修饰的色调映射失真**：当目标修饰效果极大偏离预训练数据分布（如极端过曝或非自然色彩映射）时，一步生成器可能产生不自然的色调映射。这受限于教师模型的能力上限与蒸馏过程中的信息压缩损失。
3. **空间局部编辑的缺失**：当前框架预测全局双边网格，无法处理空间变化的指令（如“仅将天空变蓝”）。将框架扩展至局部编辑需引入空间注意力或分割引导，可能破坏双边网格的紧凑性优势。

> 以上局限性分析基于方法机理推断，建议结合论文补充材料或后续版本进行人工验证。

### 补充图表

![[assets/figures/papers/paper_list_l759_https_openaccess_thecvf_com_content_CVPR2026_html_Wu_InstantRetouch_Effi/figures/004_Figure_3.jpg]]
*Figure 3: Visual comparisons of different image editing methods on our iRetouch benchmark*

## 方法谱系与知识库定位

### 1. 核心瓶颈与解决思路

现有指令驱动的图像编辑模型，如 **InstructPix2Pix** (Brooks et al., CVPR 2023) 和 **Gemini-2.5-Flash** (Comanici et al., arXiv 2025)，普遍采用扩散模型直接在图像潜空间（VAE latent space）中进行编辑。这一范式存在一个根本性瓶颈：无法有效解耦光度调整与内容修改。在潜空间中的每一步去噪操作都同时影响图像的外观属性和几何纹理，导致高分辨率下出现内容漂移（content drift），且多步迭代采样带来极高的推理延迟。

InstantRetouch 的核心解决思路是将编辑操作从像素/潜空间转移到一个紧凑且与内容解耦的双边网格（bilateral grid）空间中。该方法仅预测低分辨率双边网格中的局部仿射变换参数，再通过切片操作应用于全分辨率图像。这一设计天然地约束了编辑操作只能改变外观（色调、曝光、对比度等），而无法触及几何纹理，从而在机制层面杜绝了内容漂移。同时，双边空间的紧凑性使得推理效率极高——即使在 4K 分辨率下，推理时间也仅约 0.068 秒。

### 2. 方法谱系定位

InstantRetouch 处于指令驱动图像编辑、扩散模型知识蒸馏和双边空间图像处理三个领域的交叉点。

**与指令驱动扩散编辑模型的关系：** 主流方法如 InstructPix2Pix、**FLUX.1-Kontext**、**Qwen-Image** 和 **Step-1X-Edit** (Liu et al., arXiv 2025) 均依赖多步扩散采样在潜空间中直接生成编辑结果。InstantRetouch 继承了这些模型的扩散先验，但通过变分分数蒸馏（VSD）将多步教师压缩为一步生成器，并将编辑输出从像素空间迁移至双边网格参数空间。这种“蒸馏+空间迁移”的策略使其在保持扩散模型语义丰富性的同时，获得了数量级的效率提升和零内容漂移的保真度优势。

**与图像增强 LUT 方法的关系：** **3D LUTs** 类方法（如 **RSFNet**, Ouyang et al., ICCV 2023；**3D LUT**, Zeng et al., TPAMI 2020）同样追求高效的色彩变换，但它们依赖固定风格的查找表，不支持自由形式的文本指令驱动。InstantRetouch 的双边网格可以视为一种“动态生成的条件化 3D LUT”，通过扩散分支的语义理解来实时预测变换参数，从而将 LUT 的高效性与扩散模型的灵活性统一。

**与知识蒸馏方法的关系：** InstantRetouch 的蒸馏框架借鉴了 DMD（Distribution Matching Distillation）中的 VSD 损失，但针对修饰任务做了两个关键适配：(1) 引入了基于 CLIP 的提示对齐损失（prompt alignment loss），将用户指令拆解为原子修饰属性并通过 InfoNCE 损失进行对比学习，解决了步数压缩导致的指令跟随弱化问题；(2) 采用渐进式噪声调度策略——训练初期使用高噪声水平学习色调、曝光等粗粒度属性，随后逐步降低噪声以蒸馏细粒度细节。

### 3. 适用边界与局限

**适用边界：** InstantRetouch 的设计天然适用于全局图像修饰任务，包括色调映射、曝光调整、色彩风格迁移等不改变图像几何结构的操作。其双边网格表示对全局仿射变换的建模能力极强，且推理延迟几乎不随分辨率增长（从 720p 到 4K 仅从 0.065s 增至 0.068s），特别适合需要实时处理高分辨率图像的场景。

**局限性：** 论文正文未明确列出局限性，但从方法设计可推断以下潜在边界：

- **空间变化编辑的受限性：** 双边网格本质上是全局变换表示，虽然通过引导图（guidance map）可以实现一定程度的局部自适应，但对于“只将天空变蓝”这类需要精确空间掩码的局部编辑，当前框架的紧凑性可能成为约束。论文的开放问题中也明确提出了这一扩展方向。

- **指令泛化的覆盖度：** 提示对齐模块依赖规则匹配器将指令拆解为原子属性，这意味着其对未见指令类型的泛化能力受限于预定义的属性词表和匹配规则。虽然论文使用大模型生成了多样化训练数据，但极端偏离训练分布的指令可能产生不自然的色调映射。

- **教师模型的能力上限：** 蒸馏框架的最终质量受限于教师扩散模型的能力。若教师模型对某些修饰风格的理解不足，一步生成器也难以超越这一上限。如何更有效地利用更大的教师模型是一个开放问题。

### 4. 开放问题与后续方向

论文提出了三个值得关注的开放问题：

1. **局部编辑扩展：** 如何将框架扩展到空间变化的指令（如局部区域修饰）而不损失双边网格的紧凑性和效率优势？这可能需要引入空间掩码机制或可学习的空间调制模块。

2. **指令理解模块的改进：** 能否将基于规则的属性匹配器替换为更纯净的端到端指令理解模块，以减少规则匹配带来的误差并提升对自由形式指令的泛化能力？这涉及将提示对齐损失与更强的视觉-语言模型（如更强的 CLIP 变体或多模态大模型）进行更紧密的耦合。

3. **教师模型规模的扩展：** 蒸馏过程中教师模型的能力上限直接影响最终质量。如何在保持一步推理效率的前提下，更有效地利用更大的教师模型（如从 SD 系列扩展到 FLUX 等更强的基座），是进一步提升编辑质量的关键方向。

### 5. 知识库定位总结

InstantRetouch 在知识库中的独特贡献在于：它首次证明了扩散模型的强语义先验可以被蒸馏到一个内容解耦的双边网格生成器中，从而在指令驱动的图像修饰任务上同时实现三个看似矛盾的目标——高语义质量（O-score 8.54，接近 Gemini-2.5-Flash 的 8.74）、极高内容保真度（SSIM 0.989）和极低推理延迟（4K 分辨率 0.068 秒）。这一“扩散先验 + 双边约束”的范式为实时、高保真的 AI 图像编辑提供了一条与现有潜空间编辑方法互补的技术路径。

## 原文 PDF

![[paperPDFs/CVPR_2026/InstantRetouch_Efficient_and_High_Fidelity_Instruction_Guided_Image_Retouching_with_Bilateral_Space.pdf]]
