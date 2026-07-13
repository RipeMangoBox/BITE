---
title: "MSCD-GS: Motion-Separated Cooperative Deblurring Dynamic Reconstruction via Gaussian Splatting"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/MSCD_GS_Motion_Separated_Cooperative_Deblurring_Dynamic_Reconstruction_via_Gaussian_Splatting.pdf
project_link: "https://liaoyongjian1.github.io/MSCD-GS/"
code_link: null
aliases:
- MG
- MSCD-GS
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
core_operator: 将场景的3D高斯原语显式分离为静态和动态部分，并分别为其设计运动模型（静态线性、动态Catmull-Rom非线性），模拟曝光时间内的模糊形成；同时引入预训练去模糊网络提供先验，与合成的虚拟模糊图像联合约束，平衡2D先验与3D物理一致性。
primary_logic: 通过运动分离建模和协作正则化，将去模糊网络的2D先验与3D运动建模有效结合，无需额外的深度、光流等先验数据，即可从运动模糊输入中实现高质量的动态4D重建。
claims:
- 在Stereo Blur数据集上，MSCD-GS的去模糊PSNR达到33.21，SSIM 0.957，LPIPS 0.043，显著优于SoM+NAFNet组合（PSNR 29.01）。
- 与最新的动态去模糊方法（Deblur4DGS, BARD-GS, DyBluRF等）相比，MSCD-GS在所有指标上均达到最优，同时渲染速度达121 FPS，训练时间仅0.72小时。
- 消融实验表明，去除去模糊网络（DN）后重建质量大幅下降（PSNR从31.72降至26.34），证明协作监督是关键。
- Stereo Blur 上 Deblurring PSNR↑ = 33.21
---

# MSCD-GS: Motion-Separated Cooperative Deblurring Dynamic Reconstruction via Gaussian Splatting

> [!tip] 核心洞察
> 通过运动分离建模和协作正则化，将去模糊网络的2D先验与3D运动建模有效结合，无需额外的深度、光流等先验数据，即可从运动模糊输入中实现高质量的动态4D重建。

| 字段 | 内容 |
|------|------|
| 中文题名 | MSCD-GS：基于高斯泼溅的运动分离协作去模糊动态重建 |
| 英文题名 | MSCD-GS: Motion-Separated Cooperative Deblurring Dynamic Reconstruction via Gaussian Splatting |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://openaccess.thecvf.com/content/CVPR2026/html/Liao_MSCD-GS_Motion-Separated_Cooperative_Deblurring_Dynamic_Reconstruction_via_Gaussian_Splatting_CVPR_2026_paper.html) · [Project](https://liaoyongjian1.github.io/MSCD-GS/) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction |
| Method | MSCD-GS |
| Dataset | Stereo Blur |

> [!tip] 效果简介
> - Stereo Blur 上，Deblurring PSNR↑ 33.21 vs 29.01 (SoM+NAFNet) (+4.20)；Deblurring SSIM↑ 0.957 vs 0.949 (SoM+NAFNet) (+0.008)；Deblurring LPIPS↓ 0.043 vs 0.101 (SoM+NAFNet) (-0.058)。

## 概要

在单目相机拍摄的动态场景中，相机与物体的同时运动会在曝光时间内产生复杂的混合运动模糊，这严重损害了基于高斯泼溅（3D/4D Gaussian Splatting）的动态重建与新视角合成质量。现有的去模糊方法或简单地将去模糊网络与4D重建管线串行集成（如 **SoM** + **NAFNet**），或仅对高斯进行统一的运动建模，无法有效解耦和处理相机与物体运动模糊的异构特性。

**MSCD-GS** 针对上述瓶颈提出了一个运动分离协作去模糊的动态重建框架。其核心思路是：将场景的3D高斯原语显式分离为**静态高斯**与**动态高斯**，并分别为其设计差异化的运动模型——静态高斯采用线性位移模型，动态高斯则利用 **Catmull-Rom** 样条插值位置与 **Slerp** 插值旋转来刻画非线性运动。在此基础上，方法引入预训练去模糊网络提供高质量的2D先验，将其与基于物理运动建模合成的虚拟模糊图像联合约束，通过加权协作损失平衡2D先验与3D物理一致性，从而无需额外的深度或光流先验数据即可实现高质量的去模糊4D重建。

在 **Stereo Blur** 数据集上，MSCD-GS 的去模糊 PSNR 达到 **33.21**，SSIM **0.957**，LPIPS **0.043**，显著优于 SoM+NAFNet 组合（PSNR 29.01）及最新的动态去模糊方法（**Deblur4DGS**、**BARD-GS**、**DyBluRF** 等），同时渲染速度可达 **121 FPS**，训练时间仅 **0.72 小时**。消融实验进一步证实，去除去模糊网络先验会使 PSNR 从 31.72 骤降至 26.34，而移除静态或动态高斯的去模糊模块均会造成明显的性能损失，验证了运动分离建模与协作监督的核心作用。



### 动态场景重建中的运动模糊困境

从单目相机捕获的图像中重建动态4D场景（即随时间变化的三维表示）是计算机视觉与图形学中的核心挑战。近年来，以3D Gaussian Splatting（3DGS）为代表的显式表示方法在静态场景重建中取得了显著进展，并逐步被扩展至动态场景。然而，这些方法普遍假设输入图像是清晰的，忽略了真实拍摄中不可避免的运动模糊问题。

当相机与被拍摄物体在曝光时间内同时运动时，捕获的图像会产生复杂的混合运动模糊。这种模糊并非简单的均匀退化，而是在空间和时间维度上高度耦合的退化过程：相机的自运动导致全局背景模糊，而场景中动态物体的独立运动则叠加了局部、非均匀的运动轨迹。这种混合模糊严重破坏了4D重建的质量——无论是基于NeRF的隐式方法还是基于3DGS的显式方法，在模糊输入下都会产生细节丢失、几何失真和渲染伪影。

### 现有方法的缺口

面对运动模糊问题，一个直观的思路是“先去模糊，再重建”：即先使用预训练的去模糊网络（如**NAFNet**，Chen et al., ECCV 2022）对输入图像进行预处理，再将清晰化后的图像送入动态重建管线（如**SoM**，Wang et al., ICCV 2025）。然而，这一朴素集成策略存在根本性缺陷：

1. **2D先验与3D几何的割裂**：去模糊网络在2D图像层面操作，仅依赖单帧上下文恢复清晰度，缺乏对场景三维结构和运动连续性的理解。其输出去除了部分模糊，但可能引入不符合物理规律的纹理或边缘，导致重建结果仍然残留模糊（见Figure 1）。
2. **性能下界受制于去模糊模型**：实验表明（Table 1），SoM+NAFNet组合的去模糊PSNR仅为29.01，远低于MSCD-GS的33.21。这说明去模糊模型的能力直接决定了重建质量的上限，而2D去模糊本身在复杂运动场景中难以达到理想效果。

更近期的动态去模糊重建方法，如**Deblur4DGS**（Wu et al., arXiv 2024）、**BARD-GS**（Lu et al., CVPR 2025）和**DyBluRF**（Sun et al., CVPR 2024），尝试在重建过程中显式建模模糊形成过程。它们通常通过合成虚拟模糊图像与输入对齐来实现去模糊，但存在一个共同的盲点：**未对静态背景与动态前景的运动模式进行区分建模**。在真实场景中，背景的运动主要来源于相机的刚体变换（可近似为线性位移），而动态物体则遵循非线性、非刚体的运动轨迹。将两者混为一谈，用一个统一的变形场或运动模型去描述，必然导致模型容量不足或过拟合，难以同时恢复清晰的背景和锐利的动态对象。

### 核心动机

基于上述分析，本文的核心动机可归纳为：

- **运动分离的必要性**：静态高斯与动态高斯的运动特性本质上不同，必须分别设计运动模型，才能准确模拟曝光时间内的模糊形成过程。
- **2D先验与3D建模的协作**：去模糊网络提供的2D先验是有价值的，但不应作为唯一的监督信号。需要一种机制，将2D先验的“锐度引导”与3D运动建模的“物理一致性”有机结合，使两者相互约束、协同优化。
- **无需额外模态的轻量设计**：在保证重建质量的前提下，避免依赖深度、光流等额外先验数据，保持方法的实用性和泛化能力。

这些动机直接催生了MSCD-GS的设计思路：通过高斯原语的显式动/静分离、差异化的运动建模（线性/非线性），以及协作去模糊损失函数，在无需外部先验的条件下实现高质量的动态4D去模糊重建。



## 核心方法与创新机理

MSCD-GS 的核心创新在于**运动分离建模 + 协作去模糊正则化**的双重设计，系统性地解决了动态场景中相机与物体混合运动模糊对 4D 高斯泼溅（4DGS）重建的破坏问题。

### 1. 高斯原语的运动分离

与现有 4DGS 方法将所有高斯统一处理不同，MSCD-GS 在优化过程中**显式地将 3D 高斯分离为静态高斯和动态高斯**。分离依据两个信号：高斯在相邻帧间的运动距离，以及来自预训练模型的 2D 动态掩膜。这一设计使得后续运动建模可以针对不同运动特性采用差异化策略。

### 2. 差异化的运动轨迹建模

分离后的两类高斯采用完全不同的运动模型：

- **静态高斯**：假设其在曝光时间内的运动近似为**线性位移**，通过起点位置和方向向量直接计算任意时刻的位置（Eq. 6）。
- **动态高斯**：采用**Catmull-Rom 样条**拟合非线性位置轨迹（Eq. 7），并使用**四元数球面线性插值（Slerp）** 建模旋转变化（Eq. 10），同时引入不透明度衰减因子模拟运动导致的透明度变化。

这种“静态线性 + 动态非线性”的建模策略，使框架能够精准捕捉曝光时间内相机自运动与物体独立运动的复杂耦合。

### 3. 运动感知的去模糊 MLP

为预测曝光时间内每帧虚拟清晰图像对应的高斯变化，MSCD-GS 设计了两个专用的 MLP：一个预测静态高斯逐帧的刚体旋转与平移（Eq. 14），另一个预测动态高斯每粒子的形变（Eq. 16）。这使得系统无需额外深度或光流先验，即可从模糊输入中推断曝光时间内的精细运动。

### 4. 协作去模糊损失

MSCD-GS 的监督信号由两部分加权组合（Eq. 18）：

- **去模糊先验损失**：将渲染的虚拟清晰图像与预训练去模糊网络（NAFNet）的输出对齐，提供高质量的 2D 先验。
- **物理合成模糊损失**：将虚拟清晰图像按曝光模型合成为虚拟模糊图像，与真实模糊输入对齐，保证 3D 物理一致性。

通过可调参数 λ 平衡两者，MSCD-GS 有效融合了 2D 先验的细节恢复能力与 3D 运动建模的几何约束，避免了单独依赖去模糊网络导致的细节失真，也克服了纯物理合成监督的收敛困难。消融实验证实，移除去模糊网络后去模糊 PSNR 从 31.72 骤降至 26.34，验证了协作监督的关键作用。

### 方法谱系与知识库定位

MSCD-GS 处于 **4D 高斯泼溅动态重建** 与 **运动模糊建模** 的交叉点。相较于以下代表性工作，其核心差异在于：

| 方法 | 运动分离 | 运动模型 | 去模糊策略 |
|------|----------|----------|------------|
| 4D Gaussian Splatting（基线） | 无 | 统一变形场 | 无模糊处理 |
| Deblur4DGS（Wu et al., arXiv 2024） | 无 | 统一 | 仅物理合成模糊监督 |
| BARD-GS（Lu et al., CVPR 2025） | 无 | 统一 | 物理合成模糊监督 |
| DyBluRF（Sun et al., CVPR 2024） | 基于 NeRF | 统一 | 物理合成模糊监督 |
| SoM + NAFNet（朴素集成） | 无 | 统一 | 直接以去模糊输出监督 |
| **MSCD-GS（本文）** | **显式分离** | **静态线性 + 动态非线性** | **去模糊先验 + 物理合成协作** |

MSCD-GS 首次在 4DGS 框架中引入运动分离建模，并通过协作损失将单图去模糊网络的 2D 先验与 3D 运动物理模型有机结合，无需额外模态数据，为动态场景去模糊重建提供了新的范式。



MSCD-GS 的整体流程以运动分离与协作去模糊为核心，将单目相机捕获的运动模糊图像作为输入，输出高质量的去模糊动态场景重建与新视角合成结果。其 pipeline 由三个关键阶段构成：**高斯分离（Section A）**、**运动建模与虚拟图像合成（Section B）** 以及**协作去模糊监督（Section C）**，如图 Figure 2 所示。

![[assets/figures/papers/paper_list_l35_https_openaccess_thecvf_com_content_CVPR2026_html_Liao_MSCD_GS_Motion_Se/figures/003_Figure_2.jpg]]
*Figure 2: The pipeline of our MSCD-GS. We construct an initial Gaussian model using blurred images as input. Section A: During optimization, static and dynamic Gaussians are separated using Gaussian motion distance and dynamic masks. Section B: We model static and dynamic Gaussian motion separately and design two motion-aware MLPs to predict their changes over exposure time, thereby generating multiple virtual sharp images. Section C: We also utilize the results from the deblurring network to constrain these virtual images, and these virtual sharp images are synthesized into a virtual blurred image to align with the input real image*

### 输入与初始化

系统以运动模糊图像序列为输入，首先构建初始的 3D 高斯模型。该初始化阶段不依赖额外的清晰图像或深度、光流等先验数据，完全基于模糊输入完成高斯原语的初始分布估计。

### 阶段 A：静态与动态高斯分离

在优化过程中，MSCD-GS 将场景的 3D 高斯原语显式分离为**静态高斯** $G_S$ 和**动态高斯** $G_D$ 两类。分离依据两个信号：一是高斯在相邻帧间的运动距离，二是从 2D 图像中提取的动态掩膜。运动距离较大且位于动态掩膜区域的高斯被归类为动态高斯，其余归为静态高斯。这一分离是后续差异化运动建模的基础。

### 阶段 B：差异化运动建模与虚拟清晰图像合成

针对静态和动态高斯截然不同的运动特性，MSCD-GS 设计了两套独立的运动模型：

- **静态高斯运动模型**：假设背景区域的运动在短时间窗口内近似线性，采用线性位移模型描述静态高斯在曝光时间内的轨迹。
- **动态高斯运动模型**：对前景运动对象采用非线性建模，使用 Catmull-Rom 样条插值预测位置变化，并用四元数球面线性插值（Slerp）建模旋转变化，同时引入不透明度衰减机制。

在此基础上，系统设计了两组**运动感知 MLP**，分别预测曝光时间内静态高斯和动态高斯在多个采样时刻的位置、旋转等属性变化。在每个采样时刻 $t^i$，合并静态与动态高斯，渲染生成一组**虚拟清晰图像** $I(t^i)$。随后，将同一曝光时间窗口内的虚拟清晰图像按运动模糊成像模型（Eq. 1）取平均，合成**虚拟模糊图像** $\hat{B}(t)$。

### 阶段 C：协作去模糊损失

MSCD-GS 的关键创新在于**协作去模糊损失**的设计。该损失由两项加权组合而成：

1. **去模糊先验损失**：利用预训练去模糊网络（NAFNet）对输入模糊图像进行处理，将其输出作为高质量先验，约束虚拟清晰图像的生成。
2. **物理合成模糊损失**：将合成的虚拟模糊图像与真实输入模糊图像对齐，保证 3D 运动建模的物理一致性。

两项损失通过平衡参数 $\lambda$ 加权协作，公式为：

$$\mathcal{L}_{render}(t) = \lambda \sum_{i \in N} \| \mathbf{B}_d(t^i) - \mathbf{I}(t^i) \|_1 + (1-\lambda) \sum \| \mathbf{B}(t) - \hat{\mathbf{B}}(t) \|_1$$

其中 $\mathbf{B}_d(t^i)$ 为去模糊网络的输出，$\mathbf{I}(t^i)$ 为虚拟清晰图像，$\mathbf{B}(t)$ 为真实模糊图像，$\hat{\mathbf{B}}(t)$ 为合成虚拟模糊图像。实验设置中 $N=3$、$\lambda=0.4$。

### 模块间的因果联动

三个阶段的因果链条清晰：**高斯分离**为差异化运动建模提供了场景结构先验；**运动建模**将曝光时间内的物理模糊过程显式参数化，使虚拟模糊图像能够与真实输入对齐；**协作损失**则通过 2D 去模糊先验与 3D 物理约束的互补，解决了单一监督信号不足的问题。消融实验（Table 4）表明，移除任一模块（去模糊网络 DN、静态高斯去模糊 SGD、动态高斯去模糊 DGD）均会导致重建质量大幅下降，其中去除 DN 使去模糊 PSNR 从 31.72 骤降至 26.34，验证了协作机制的核心作用。



MSCD-GS 的核心在于将场景的 3D 高斯原语显式分离为静态与动态两部分，并分别设计运动模型来模拟曝光时间内的模糊形成过程。整体流程如 Figure 2 所示，包含三个关键模块：高斯分离、运动建模与去模糊、以及协作去模糊监督。

### 3.1 运动模糊物理建模

运动模糊图像被建模为曝光时间 $[\tau_s, \tau_e]$ 内 $N$ 个虚拟清晰图像的平均：

$$ \mathbf{B} = \int_{\tau_s}^{\tau_e} \mathbf{I}(\mathbf{P}_\tau) d\tau \approx \frac{1}{N} \sum_{i=1}^{N} \mathbf{I}(\mathbf{P}_{\tau_i}) \tag{1} $$

其中 $\mathbf{P}_\tau$ 表示时刻 $\tau$ 的相机位姿。这一离散化近似是整个去模糊重建框架的物理基础。

### 3.2 高斯分离策略

MSCD-GS 利用两个信号将高斯原语分类为静态高斯 $\mathcal{G}_S$ 和动态高斯 $\mathcal{G}_D$：**高斯运动距离**和 **2D 动态掩膜**。运动距离衡量每个高斯在相邻帧间的位移幅度，结合预训练分割模型提供的动态掩膜，可以有效区分背景与运动物体。这一显式分离是后续差异化运动建模的前提。

### 3.3 静态高斯运动模型

对于静态高斯（通常对应背景），其运动主要由相机运动引起。在单个图像子集的时间窗口 $\tau_d$ 内，其运动轨迹被建模为线性位移：

$$ \mu_S(t_i) = \mu_S(t^s) + \frac{t_i}{\tau_d} \mathbf{d} \tag{6} $$

其中 $t_i$ 为子集内的采样时刻，$t^s$ 为子集起始时刻，$\mathbf{d}$ 为位移向量。这一线性假设在相机运动相对平滑时是合理的近似。

### 3.4 动态高斯运动模型

动态高斯对应场景中的运动物体，其轨迹更为复杂。MSCD-GS 采用 **Catmull-Rom 样条** 进行位置插值：

$$ \mu_D(t_i) = \mathbf{T}(t_i) \cdot \mathbf{M}_\mu \cdot \mu \tag{7} $$

其中 $\mathbf{T}(t_i)$ 为样条基函数矩阵，$\mathbf{M}_\mu$ 为控制点矩阵。对于旋转，则使用四元数球面线性插值（Slerp）以保证旋转的平滑性：

$$ \mathbf{q}_D(t_i) = \frac{\sin((1 - t_i)\theta) \mathbf{q}^{-1} + \sin(t_i \theta) \mathbf{q}^{+1}}{\sin\theta} \tag{10} $$

此外，动态高斯的不透明度也随时间衰减，以模拟运动导致的模糊效应。

### 3.5 运动感知去模糊 MLP

为预测曝光时间内每帧高斯的具体变化，MSCD-GS 设计了两个运动感知 MLP。静态高斯 MLP 预测每帧的刚体变换：

$$ \{\Delta R^i, \Delta T^i \mid i \in N\} = F_S(\mu_S(t), i) \tag{14} $$

动态高斯 MLP 则预测每个粒子的形变参数。这些 MLP 使框架能够灵活捕捉曝光时间内的微小运动。

### 3.6 协作去模糊损失

核心创新在于将去模糊网络的 2D 先验与 3D 物理建模相结合。协作渲染损失定义为：

$$ \mathcal{L}_{render}(t) = \lambda \sum_{i \in N} \|\mathbf{B}_d(t^i) - \mathbf{I}(t^i)\|_1 + (1-\lambda) \sum \|\mathbf{B}(t) - \hat{\mathbf{B}}(t)\|_1 \tag{18} $$

第一项为**去模糊先验监督**：要求渲染的虚拟清晰图像 $\mathbf{I}(t^i)$ 接近去模糊网络输出 $\mathbf{B}_d(t^i)$；第二项为**物理合成模糊监督**：要求虚拟清晰图像平均合成的模糊图像 $\hat{\mathbf{B}}(t)$ 与真实输入模糊图像 $\mathbf{B}(t)$ 对齐。超参数 $\lambda$ 平衡两者权重（实验设为 0.4），消融实验（Table 4）表明去除去模糊网络监督后 PSNR 从 31.72 骤降至 26.34，验证了协作策略的关键作用。



## 实验与关键发现

### 核心定量结果

MSCD-GS在Stereo Blur数据集上的去模糊4D重建任务中全面超越现有方法。**Table 1**展示了与朴素集成基线SoM+NAFNet的对比：MSCD-GS的去模糊PSNR达到**33.21**（+4.20），SSIM达到**0.957**（+0.008），LPIPS降至**0.043**（-0.058），说明仅靠去模糊网络输出的2D监督无法充分驱动4DGS的3D运动建模，而协作去模糊损失有效弥合了这一差距。在新视角合成任务上，MSCD-GS同样取得**29.49** PSNR和**0.941** SSIM，较基线分别提升1.73和0.031，证明运动分离建模不仅改善了去模糊质量，也提升了场景几何的时空一致性。

![[assets/figures/papers/paper_list_l35_https_openaccess_thecvf_com_content_CVPR2026_html_Liao_MSCD_GS_Motion_Se/figures/002_Table_1.jpg]]
*Table 1: Quantitative comparison on the Stereo Blur dataset. * indicates that sharp images are used as input, while all others use motion-blurred images*

与专用动态去模糊重建方法的全面对比见**Table 2**。在去模糊指标上，MSCD-GS在所有三个指标（PSNR/SSIM/LPIPS）上均排名第一，优于Deblur4DGS、BARD-GS和DyBluRF。在新视角合成上同样取得最优。值得注意的是，MSCD-GS的渲染速度达到**121 FPS**，训练时间仅**0.72小时**，在效率维度显著优于基于NeRF的DyBluRF，也优于同类4DGS方法。在真实世界模糊数据集上（**Table 3**），MSCD-GS在新视角合成任务中以28.13 PSNR保持SOTA，验证了方法对真实模糊的泛化能力。

![[assets/figures/papers/paper_list_l35_https_openaccess_thecvf_com_content_CVPR2026_html_Liao_MSCD_GS_Motion_Se/figures/004_Table_2.jpg]]
*Table 2: Quantitative comparison of Deblurring 4D Reconstruction and Novel View Synthesis on the Stereo Blur dataset. Colors indicate the best , second best , and third best results respectively. Per-scene results are provided in the supplementary material. Our method can reconstruct high-quality 4D scenes while being more efficient and achieving a higher rendering frame rate compared to similar methods*

定性结果（**Figure 3**, **Figure 4**）进一步印证了定量结论：无论背景区域还是动态对象，MSCD-GS均能恢复出最清晰的纹理细节，而对比方法在快速运动区域仍残留明显模糊或伪影。

![[assets/figures/papers/paper_list_l35_https_openaccess_thecvf_com_content_CVPR2026_html_Liao_MSCD_GS_Motion_Se/figures/005_Figure_3.jpg]]
*Figure 3: Qualitative comparison of Deblurring 4D Reconstruction. The challenging regions have been highlighted with bounding boxes. Whether the background or dynamic objects, our method provides the best deblurring 4D reconstruction results*

![[assets/figures/papers/paper_list_l35_https_openaccess_thecvf_com_content_CVPR2026_html_Liao_MSCD_GS_Motion_Se/figures/007_Figure_4.jpg]]
*Figure 4: Qualitative comparison of Novel View Synthesis. The challenging regions have been highlighted with bounding boxes. Whether the background or dynamic objects, our method provides the best Novel View Synthesis results*

### 消融实验：各模块的必要性

**Table 4**的系统消融揭示了三个关键设计的作用：

- **移除去模糊网络（w/o DN）**：去模糊PSNR从31.72骤降至26.34，降幅达5.38 dB。这证实了去模糊网络提供的2D先验是协作监督的核心驱动力——仅靠物理合成模糊对齐（即传统Deblur-GS范式）无法有效约束运动建模。
- **移除静态高斯去模糊（w/o SGD）**：性能明显下降，说明背景区域的运动模糊同样不可忽视。静态高斯的线性运动建模与专用MLP对曝光时间内刚体变换的预测是必要的。
- **移除动态高斯去模糊（w/o DGD）**：性能同样受损，验证了动态对象的非线性运动建模（Catmull-Rom位置插值+Slerp旋转插值）和对应MLP的不可替代性。

定性消融结果（**Figure 5**）直观展示了各模块缺失时的退化模式：w/o DN导致整体模糊残留，w/o SGD使背景纹理受损，w/o DGD则使动态对象边缘出现拖影。

![[assets/figures/papers/paper_list_l35_https_openaccess_thecvf_com_content_CVPR2026_html_Liao_MSCD_GS_Motion_Se/figures/009_Figure_5.jpg]]
*Figure 5: Qualitative results of ablation experiments on each module of MSCD-GS. The experimental results demonstrate that each module proposed in our method is indispensable for deblurring 4D reconstruction*

### 虚拟视图数量的影响

**Table 5**考察了曝光时间内采样虚拟视图数N的敏感性。当N从2增至3时，性能提升；但继续增至5或7时，指标反而逐渐下降。论文将N=3设为默认值。这一现象的可能解释是：过多的虚拟视图引入了冗余的自由度，使运动MLP的优化难度增加；而过少的视图则不足以充分模拟曝光时间内的连续运动轨迹。

### 失败模式与局限性

尽管MSCD-GS在去模糊重建上表现优异，**Figure 6**揭示了其根本性局限：当运动模糊导致图像中物体部分内容彻底缺失（如快速运动的腿部在模糊帧中完全不可见），方法无法凭空恢复这些区域，只能渲染出背景。这是物理成像模型的内在限制——模糊是信息的丢失，而非仅是信息的混合。论文指出未来可结合扩散模型等生成式先验，为缺失区域提供合理的监督信号，但这需要解决时空一致性的挑战。

![[assets/figures/papers/paper_list_l35_https_openaccess_thecvf_com_content_CVPR2026_html_Liao_MSCD_GS_Motion_Se/figures/010_Figure_6.jpg]]
*Figure 6: Although deblurring 4D reconstruction methods (Deblur4DGS) can render sharp images, they still fail to recover the missing parts in the image. The challenging regions have been highlighted with bounding boxes*

### 补充图表

![[assets/figures/papers/paper_list_l35_https_openaccess_thecvf_com_content_CVPR2026_html_Liao_MSCD_GS_Motion_Se/figures/011_Table_5.jpg]]
*Table 5: Quantitative results of ablation experiments on the number of virtual views. The results indicate that a relatively small number of virtual views can achieve high-quality reconstruction*

![[assets/figures/papers/paper_list_l35_https_openaccess_thecvf_com_content_CVPR2026_html_Liao_MSCD_GS_Motion_Se/figures/001_Figure_1.jpg]]
*Figure 1: Motion blur is inevitably present in images captured by a monocular camera, which significantly degrades the quality of 4D reconstruction. Although the addition of the deblurring model NAFNet [2] improves image sharpness, the reconstruction results of SoM [34] still suffer from blur. Therefore, we propose a novel deblurring 4D Gaussian method MSCD-GS, which can render sharper images*



## 定位与知识库关联

### 方法沿革与基线关系

MSCD-GS 处于动态场景去模糊重建的交叉地带，其方法谱系可沿两条主线追溯：**动态高斯泼溅（4DGS）** 与 **运动模糊建模**。

在动态重建侧，4D Gaussian Splatting 基线将所有高斯统一处理，不包含运动模糊建模。MSCD-GS 的核心改造在于引入**高斯分类机制**——利用运动距离与 2D 动态掩膜将场景原语显式分离为静态高斯与动态高斯，这一设计直接回应了单目动态场景中“背景与前景运动特性迥异”的物理事实。

在去模糊侧，早期朴素集成方案 **SoM + NAFNet**（SoM: Wang et al., ICCV 2025; NAFNet: Chen et al., ECCV 2022）直接以去模糊模型的输出监督 4DGS，但该方法存在根本性缺陷：去模糊网络的 2D 先验与 3D 重建之间存在不可调和的域间隙，去模糊能力直接决定了重建质量的下限（Table 1 中该组合 PSNR 仅为 29.01，而 MSCD-GS 达 33.21）。MSCD-GS 的关键突破在于将去模糊网络从“监督者”降级为“先验提供者”，通过协作损失函数（Eq. 18）的 λ 加权机制，平衡 2D 先验与 3D 物理合成模糊的一致性约束。

与同期工作的差异化对比如下：

| 方法 | 核心机制 | 与 MSCD-GS 的关键差异 |
|------|----------|----------------------|
| **Deblur4DGS** (Wu et al., arXiv 2024) | 4DGS + 运动模糊建模 | 未进行静态/动态高斯分离，运动模型统一处理 |
| **BARD-GS** (Lu et al., CVPR 2025) | 动态场景运动模糊重建 | 同样缺乏运动分离机制 |
| **DyBluRF** (Sun et al., CVPR 2024) | 基于 NeRF 的运动模糊动态重建 | 采用 NeRF 而非 3DGS 作为场景表示，渲染效率受限 |

MSCD-GS 在 Stereo Blur 数据集上的全面优势（Table 2：去模糊 PSNR 33.21，新视角合成 PSNR 29.49，渲染速度 121 FPS，训练时间仅 0.72 小时）表明，**运动分离建模 + 协作去模糊监督**的组合策略在精度与效率两个维度上同时超越了上述方法。

### 适用边界与关键前提

MSCD-GS 的有效性依赖于以下前提条件，这些条件界定了其适用边界：

1. **运动模糊可建模性**：方法假设曝光时间内的运动可通过线性（静态高斯）或 Catmull-Rom 样条（动态高斯）插值近似。对于极端非线性运动（如高频振动、碰撞反弹），当前运动模型的表达能力可能不足。

2. **场景可分离性**：高斯分类依赖于运动距离阈值与 2D 动态掩膜。当动态对象与静态背景的运动差异不显著（如缓慢移动的物体），或动态掩膜质量较低时，分离精度会下降。

3. **去模糊先验质量**：消融实验（Table 4）表明，移除去模糊网络后 PSNR 从 31.72 骤降至 26.34，证明协作监督对去模糊网络先验存在强依赖。若输入模糊程度超出预训练去模糊网络的处理能力，重建质量将受到显著影响。

4. **内容完整性假设**：方法无法恢复因运动模糊而彻底丢失的图像内容。Figure 6 展示了典型失败案例——快速运动导致的腿部区域缺失，方法只能渲染出背景，无法补全动态对象。

### 局限与开放问题

**已确认的局限**：
- 对于小而快速移动的物体，若其在捕获图像中因模糊而完全缺失（如快速运动的肢体），MSCD-GS 无法恢复该部分内容，仅能渲染背景区域。这是物理成像过程的硬性约束，而非算法设计缺陷。

**开放问题**：
1. **缺失内容生成**：能否在框架中集成可控的生成模型（如扩散模型），以自动补全因运动模糊彻底丢失的动态细节？这需要解决生成内容与 3D 场景表示的时空一致性问题。

2. **运动模型泛化**：当前线性/样条运动模型对极端非刚性形变（如布料飘动、流体）的适用性有待验证。是否需要引入更灵活的运动基元（如神经形变场）来扩展适用边界？

3. **去模糊先验的自适应选择**：λ 参数（论文设为 0.4）在不同场景、不同模糊程度下的最优取值是否具有普适性？能否设计自适应加权机制，根据局部模糊程度动态调整协作监督的强度？

4. **多传感器扩展**：当前框架针对单目相机设计，能否扩展至多视角或事件相机输入，利用多源信息互补解决单目运动模糊的不适定性？



## 原文 PDF

![[paperPDFs/CVPR_2026/MSCD_GS_Motion_Separated_Cooperative_Deblurring_Dynamic_Reconstruction_via_Gaussian_Splatting.pdf]]
