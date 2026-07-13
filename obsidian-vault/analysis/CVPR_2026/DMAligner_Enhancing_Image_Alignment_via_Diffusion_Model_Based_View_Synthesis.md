---
title: "DMAligner: Enhancing Image Alignment via Diffusion Model Based View Synthesis"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/DMAligner_Enhancing_Image_Alignment_via_Diffusion_Model_Based_View_Synthesis.pdf
project_link: null
code_link: "https://github.com/boomluo02/DMAligner"
aliases:
- DMAligner
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/generative_models_diffusion
- topic/generative_models_diffusion/diffusion_image_video
- topic/representation_self_supervised_transfer
core_operator: 以扩散模型直接生成对齐视图（alignment-oriented view synthesis）替代显式光流估计与图像warping，并通过DMP模块在潜在空间中动态区分前景/背景，使扩散训练聚焦于动态区域。
primary_logic: 在潜在扩散模型训练过程中，利用动态感知掩码生成（DMP）模块捕获跨帧动态信息，从而在无深度、无相机参数、仅需两张RGB图像的条件下实现高质量对齐。
claims:
- DMAligner在DSIA数据集上取得平均PSNR/SSIM 26.67/0.81，全面超越所有对比方法（包括光流法和基于深度/扩散的基线）。
- DMP模块显著提升对齐性能，移除DMP后PSNR明显下降（消融实验中 (b) vs. (e) 对比）。
- 预测x0的去噪目标比预测噪声更适合图像对齐任务，在相同条件下PSNR更高。
- DMAligner生成的图像在视觉上最接近真值，且鬼影和背景失真显著减少（定性结果）。
---

# DMAligner: Enhancing Image Alignment via Diffusion Model Based View Synthesis

> [!tip] 核心洞察
> 在潜在扩散模型训练过程中，利用动态感知掩码生成（DMP）模块捕获跨帧动态信息，从而在无深度、无相机参数、仅需两张RGB图像的条件下实现高质量对齐。

| 字段 | 内容 |
|------|------|
| 中文题名 | DMAligner：基于扩散模型视图合成的图像对齐增强 |
| 英文题名 | DMAligner: Enhancing Image Alignment via Diffusion Model Based View Synthesis |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2602.23022) · [Code](https://github.com/boomluo02/DMAligner) |
| Topic | #topic/vision_multimodal_applications #topic/generative_models_diffusion #topic/generative_models_diffusion/diffusion_image_video #topic/representation_self_supervised_transfer |
| Method | DMAligner |
| Dataset | DSIA, Sintel, DAVIS, HDR imaging |

> [!tip] 效果简介
> - DSIA 上，Average PSNR / SSIM 26.67 / 0.81 vs best competitor < 26.67 / 0.81 (N/A)。
> - Sintel 上，Average LPIPS / DreamSim 0.211 / 0.108 (lower is better) vs DPFlow (0.xxx / 0.xxx) (N/A)。
> - DAVIS 上，Average LPIPS / DreamSim 0.211 / 0.108 (lower is better) vs GenWarp (0.xxx / 0.xxx) (N/A)。

## 概要

**问题瓶颈**：传统图像对齐方法依赖“光流估计 + 图像warping”的判别式范式。这一范式在遮挡、光照变化和复杂运动场景下存在根本性局限——显式warping无法处理多对一映射所导致的不可见区域，容易产生鬼影与背景失真（Fig. 1）。此外，部分基于深度或3D表示的方法（如COGS、AccidentalGS）需要额外的深度图、运动掩码或相机参数作为输入，限制了其在通用场景下的适用性。

**核心思路**：DMAligner 放弃显式光流估计，转而采用**扩散模型端到端生成对齐视图**的生成式范式。其关键洞察在于：在潜在扩散模型（LDM）训练过程中，通过**动态感知掩码生成（DMP）模块**捕获跨帧动态信息，区分前景运动区域与静态背景，使扩散训练能够聚焦于动态区域的条件生成。整个框架仅需两张连续RGB图像作为输入，无需深度、相机参数等额外几何信息。

**方法定位**：DMAligner 将图像对齐重新定义为“对齐导向的视图合成”（alignment-oriented view synthesis），在潜在空间中执行条件去噪以直接生成对齐后的图像。与基于光流的判别式方法（PWCNet、RAFT、FlowFormer++、DPFlow）以及基于扩散的warping方法（GenWarp）相比，DMAligner 的核心差异在于：用生成式潜在空间合成替代了显式的像素级warping操作，并通过DMP模块为扩散模型提供动态先验。

**主要结果**：在自建的DSIA数据集上，DMAligner 取得平均PSNR 26.67 / SSIM 0.81，全面超越所有对比方法（Table 2）。在Sintel和真实场景DAVIS数据集上，DMAligner 在LPIPS和DreamSim指标上也表现出色（Table 3）。定性结果显示，DMAligner 生成的图像在视觉上最接近真值，鬼影和背景失真显著减少（Fig. 4-7）。消融实验证实，DMP模块和预测x₀（而非噪声）的去噪目标对性能有决定性贡献（Table 4）。压力测试表明，DMAligner 在运动幅度增大时的性能退化速度明显慢于DPFlow和GenWarp（Fig. 8）。在下游HDR成像任务中，替换对齐模块为DMAligner后，鬼影和背景失真同样得到显著抑制（Fig. 7）。



图像对齐是计算机视觉中的一项基础任务，其目标是将不同时间或视角下捕获的同一场景图像在几何和语义上对齐，广泛应用于视频稳定、HDR重建、图像拼接等下游任务。传统对齐范式遵循“光流估计 + 图像warping”的两阶段流程：首先通过光流网络预测两帧之间的密集运动场，然后基于该运动场对源图像进行空间变换，使其与参考图像对齐。然而，这一范式存在根本性的瓶颈。

**现有范式的失效模式。** 当场景中存在显著遮挡、复杂运动或剧烈光照变化时，光流估计本身就会产生较大误差。更为关键的是，即使光流预测完全准确，基于warping的图像变换也无法处理“多对一”映射所导致的不可见区域——即源图像中被遮挡或移出视野的部分，在参考图像中找不到对应像素。这直接导致对齐结果中出现鬼影、撕裂和背景失真等伪影（见Figure 1(a)）。近年来，尽管光流方法在精度上持续提升——从经典的**PWCNet**（Sun et al., ICCV 2018）到基于循环全对场变换的**RAFT**（Teed and Deng, ECCV 2020），再到引入掩码自编码预训练的**FlowFormer++**（Shi et al., CVPR 2023）——但这些方法本质上仍受限于warping机制的固有缺陷，无法从根本上解决遮挡区域的生成问题。

**替代方案的局限。** 部分工作尝试绕过纯光流范式，引入额外的几何先验。例如，**COGS**（Jiang et al., ACM SIGGRAPH 2024）需要深度图和运动掩码作为输入进行稀疏视图合成；**AccidentalGS**（Mao et al., ICCV 2025）利用3D高斯喷洒处理意外相机运动，但依赖相机内参和外参；**GenWarp**（Seo et al., NeurIPS 2024）基于扩散模型实现单图新视图合成，但仍需要额外的语义或几何引导。这些方法虽然在特定场景下有效，但额外的输入需求严重限制了其实用性和泛化能力。

**核心动机。** 本文的核心洞察在于：图像对齐的本质并非精确估计运动场，而是生成一张在参考视角下、目标时刻的完整场景图像。换言之，对齐任务可以被重新定义为一种**对齐导向的视图合成（alignment-oriented view synthesis）**问题。这一视角转换将任务从判别式的“估计-变换”范式转向生成式的“条件生成”范式，使得模型能够直接合成对齐后的完整图像，包括传统warping无法处理的遮挡和不可见区域。扩散模型在图像生成领域展现出的强大先验建模能力，为这一范式转换提供了技术基础。本文提出的**DMAligner**正是基于这一动机，旨在仅需两张连续RGB图像的前提下，利用扩散模型的生成能力实现高质量、无鬼影的图像对齐。



## 核心方法与创新机理

DMAligner 的核心创新在于**将对齐任务从“显式估计光流→图像warping”的判别式范式，重新定义为“以对齐为目标的扩散视图生成”的生成式范式**。这一转变直接回应了传统对齐范式的根本瓶颈：光流估计在遮挡、光照变化和复杂运动下不可靠，而 warp 操作无法处理多对一映射导致的不可见区域，最终产生鬼影与背景失真（Figure 1）。

围绕这一范式转变，DMAligner 在三个关键维度上实现了 **changed slots**：

### 1. 对齐核心机制：从光流+warping到扩散端到端生成

传统方法（如 PWCNet、RAFT、FlowFormer++、DPFlow）依赖光流场将源图像像素“搬运”到目标视角，其性能上限受限于光流精度和 warp 的可逆性。DMAligner 完全摒弃了这一显式几何映射，转而利用**潜在扩散模型（LDM）**在潜在空间中直接生成对齐后的视图。扩散模型以噪声潜在 $x_t$、条件 $x_{cond}$ 和时间步 $t$ 为输入，预测干净潜在 $\tilde{x}_0$（Eq. 8），再经解码器 $\mathcal{D}$ 还原为 RGB 图像。这种生成式路径天然具备处理遮挡区域内容补全的能力，无需依赖不可靠的光流插值。

### 2. 动态信息利用方式：DMP模块驱动的潜在空间动态感知

传统光流方法通过前后一致性检查等后处理手段间接识别动态区域，但无法在训练过程中主动引导模型关注前景运动。DMAligner 的核心洞察是：**在扩散模型训练过程中，让网络具备捕获跨帧动态信息的能力**。这一能力由 **Dynamics-aware Mask Producing (DMP) 模块**实现。

DMP 模块的工作流程如下：
- 计算两个输入帧的潜在表示 $V_1$ 和 $V_2$ 之间的相关体积 $\mathcal{C}$（Eq. 6），捕获跨帧运动信息；
- 基于相关体积预测运动掩码 $\tilde{M}_{pred}$；
- 利用膨胀后的掩码 $d_r(\tilde{M}_{pred})$ 融合 $V_1$ 的背景区域和 $V_2$ 的前景区域，生成混合潜在表示 $\mathcal{V}_M$（Eq. 7）；
- 将 $V_1$、$V_2$ 和 $\mathcal{V}_M$ 沿通道维度拼接作为扩散模型的条件输入 $x_{cond}$。

这一设计使扩散模型能够**感知前景与背景的区分**，在去噪过程中对动态区域施加更强的生成约束。消融实验（Table 4）证实，移除 DMP 模块后 PSNR 显著下降，验证了动态感知机制对对齐性能的关键作用。

### 3. 输入数据需求：极简的两帧RGB输入

如表 Table 1 所示，DMAligner 仅需两张连续的 RGB 图像 $(I_1, I_2)$ 作为输入，而无需任何额外几何信息。相比之下：
- **COGS** 需要深度图和掩码输入；
- **AccidentalGS** 依赖相机内参和外参进行 3D 高斯喷洒；
- **GenWarp** 虽基于扩散模型，但面向单图新视图合成，需要显式的相机位姿变换。

DMAligner 的极简输入要求使其在真实场景中具有更强的适用性，避免了深度估计或相机标定引入的误差累积。

### 4. 辅助创新：预测 $x_0$ 的去噪目标

扩散模型通常预测添加的噪声 $\epsilon$，但 DMAligner 选择直接预测干净潜在 $\tilde{x}_0$。消融实验（Table 4）表明，在相同条件下，预测 $x_0$ 比预测噪声的 PSNR 更高。这一选择的直觉在于：图像对齐任务本质上是生成一个与真值像素级对齐的目标图像，直接回归干净信号比间接去除噪声更契合任务目标。

### 5. 加权去噪损失与掩码联合优化

DMAligner 的训练目标由两部分组成（Eq. 12）：
$$L_{\mathrm{Total}} = \lambda_1 L_{\mathrm{Denoising}} + \lambda_2 L_{\mathrm{Mask}}$$

其中 $L_{\mathrm{Denoising}}$ 利用 DMP 预测的掩码对前景和背景区域施加差异化权重（Eq. 10），引导模型聚焦于动态区域的对齐质量；$L_{\mathrm{Mask}}$ 为掩码预测的交叉熵损失。这种联合优化策略将动态感知与生成质量统一在一个端到端框架内。



DMAligner 将图像对齐从一个“显式光流估计 + 图像 warping”的判别式任务，重构为一个以对齐为目标的扩散视图生成任务。其核心流水线由三个关键阶段串联而成：**潜在空间编码与条件构建**、**动态感知扩散训练**，以及**动态感知去噪推理**。

### 输入与输出定义

框架的输入仅为两张连续的 RGB 图像 $(I_1, I_2)$，无需深度图、运动掩码、相机内参或外参（Table 1）。输出是一张对齐后的图像 $I_{\text{pred}}$，其背景与 $I_1$ 保持静态一致，而前景动态内容则与 $I_2$ 同步——这正是 Figure 2 所定义的“对齐导向视图合成”的真值含义。

![[assets/figures/papers/paper_list_l2466_https_arxiv_org_abs_2602_23022/figures/002_Figure_2.jpg]]
*Figure 2: Overview of DSIA dataset generation. The ground truth image is rendered by setting the time to*

### 潜在空间编码

首先，预训练的 VAE 编码器 $\mathcal{E}$ 将输入图像压缩到低维潜在空间：
$$V_1 = \mathcal{E}(I_1),\quad V_2 = \mathcal{E}(I_2)$$
这一压缩步骤在保持关键结构信息的同时，大幅降低了扩散模型的计算负担。训练时，真值图像 $I_{gt}$ 同样被编码为 $V_{gt}$，解码器 $\mathcal{D}$ 则负责将去噪后的潜在表示重建回 RGB 空间：
$$\tilde{I}_{gt} = \mathcal{D}(V_{gt}) = \mathcal{D}(\mathcal{E}(I_{gt}))$$

### 动态感知掩码生成模块

这是整个框架的**核心因果调节旋钮**。DMP 模块在潜在空间中捕获跨帧动态信息，其工作流程为：

1. **相关体构建**：计算 $V_1$ 与 $V_2$ 之间的归一化点积相关体积，捕获像素级运动线索：
   $$\mathcal{C}\{\mathbf{u}, \mathbf{d}\} = \frac{1}{N} \sum_{k=1}^{N} V_1^{(k)}(\mathbf{u}) \cdot V_2^{(k)}(\mathbf{u} + \mathbf{d})$$
2. **运动掩码预测**：基于相关体预测一个粗糙的运动掩码 $\tilde{M}_{\text{pred}}$，用于区分前景动态区域与背景静态区域。
3. **混合潜在融合**：利用膨胀后的掩码 $d_r(\tilde{M}_{\text{pred}})$ 将 $V_1$ 的背景区域与 $V_2$ 的前景区域进行融合，形成条件信号 $\mathcal{V}_M$：
   $$\mathcal{V}_M = V_2 \odot d_r(\tilde{M}_{\text{pred}}) + V_1 \odot \{1 - d_r(\tilde{M}_{\text{pred}})\}$$
4. **条件拼接**：将 $V_1$、$V_2$ 和 $\mathcal{V}_M$ 沿通道维度拼接，构成扩散模型的条件输入 $x_{\text{cond}}$。

### 扩散训练与推理

在训练阶段，对 $V_{gt}$ 施加前向扩散噪声：
$$q(x_t \mid x_0) = \mathcal{N}(x_t \mid \sqrt{\bar{\alpha}_t} x_0, (1-\bar{\alpha}_t) I)$$
条件 U-Net $\theta$ 以噪声潜在 $x_t$、条件 $x_{\text{cond}}$ 和时间嵌入 $\mathrm{PE}(t)$ 为输入，直接预测干净潜在 $\tilde{x}_0$：
$$\tilde{x}_0 = \theta([x_t, x_{\text{cond}}, \mathrm{PE}(t)])$$
训练总损失由加权去噪损失与掩码交叉熵损失联合组成：
$$L_{\text{Total}} = \lambda_1 L_{\text{Denoising}} + \lambda_2 L_{\text{Mask}}$$
其中 $\lambda_1=2$、$\lambda_2=0.1$，加权去噪损失利用预测掩码对前景和背景区域施加差异化权重，引导模型聚焦于动态区域。

在推理阶段，采用迭代更新策略从纯噪声逐步去噪，步长 $\Delta=20$，总步数 $T=1000$，通过循环更新过程实现加速推理与增量细化：
$$\{x_T \to \hat{x}_0^{(T)}\} \to \{x_{T-\Delta} \to \hat{x}_0^{(T-\Delta)}\} \to \cdots \to \{x_1 \to \hat{x}_0^{(1)}\}$$

### 与传统范式的本质差异

Figure 3 直观展示了这一范式转换：传统方法依赖光流网络显式估计运动场，再通过 warping 操作将 $I_2$ 变换到 $I_1$ 视角，这不可避免地会在遮挡区域产生鬼影和空洞。DMAligner 则完全绕开了显式 warping，让扩散模型在 DMP 提供的动态感知条件下，直接从噪声中生成对齐视图——这是一个从“变换已有像素”到“合成目标视图”的根本性转变。

![[assets/figures/papers/paper_list_l2466_https_arxiv_org_abs_2602_23022/figures/003_Figure_3.jpg]]
*Figure 3: Overview of our DMAligner. Instead of using the discriminative learning paradigm for optical flow estimation and image warping, our framework employs a generative approach to achieve image alignment with a diffusion model. Dynamics-aware Mask Producing (DMP) module is crucial for providing dynamic information, essential for performing the Dynamics-aware Diffusion Training process in this task*

### 补充图表

![[assets/figures/papers/paper_list_l2466_https_arxiv_org_abs_2602_23022/figures/001_Figure_1.jpg]]
*Figure 1: (a) Conventional image alignment based on optical flow and image warping, resulting in ghosting artifacts and occlusion. (b) Our DMAligner directly generates the complete alignment image via diffusion-based view synthesis*



### 问题建模与对齐目标

给定两张连续帧 $I_1$ 和 $I_2$，图像对齐的目标是生成一幅从 $I_1$ 视角观察、但内容反映 $I_2$ 时刻场景的对齐图像 $I_{gt}$。两帧之间的变换可分解为全局相机运动 $\mathcal{H}$、局部前景运动 $\mathcal{F}$ 和纹理变化 $\mathcal{T}$：

$$I_1 = \mathcal{W}(I_2) + \mathcal{T} = \mathcal{H}(\mathcal{F}(I_2)) + \mathcal{T}$$

由此，对齐真值定义为：

$$I_{gt} = \mathcal{H}(I_2) = \mathcal{F}(I_1) + \mathcal{T}$$

传统光流+warping范式在遮挡、光照变化和复杂运动下会产生鬼影与失真，且显式warping无法处理多对一映射导致的不可见区域。DMAligner以扩散模型直接生成对齐视图（alignment-oriented view synthesis）替代显式光流估计与图像warping，从根本上规避了上述瓶颈。

### 潜在扩散模型（LDM）基础

DMAligner在潜在空间而非像素空间执行扩散过程。编码器 $\mathcal{E}$ 将真值图像 $I_{gt}$ 压缩为潜在表示 $V_{gt}$，解码器 $\mathcal{D}$ 将其重建回RGB图像：

$$\tilde{I}_{gt} = \mathcal{D}(V_{gt}) = \mathcal{D}(\mathcal{E}(I_{gt}))$$

前向扩散过程从初始状态 $x_0$ 逐步加噪到任意时间步 $x_t$，单步扩散公式为：

$$q(x_t \mid x_0) = \mathcal{N}(x_t \mid \sqrt{\bar{\alpha}_t} x_0, (1-\bar{\alpha}_t) I)$$

其中 $\bar{\alpha}_t$ 为累积噪声调度参数。

### Dynamics-aware Mask Producing（DMP）模块

DMP模块是DMAligner的核心创新，其关键洞察在于：**在扩散模型训练过程中，利用跨帧潜在特征的相关性捕获动态信息，从而在无深度、无相机参数、仅需两张RGB图像的条件下实现高质量对齐。**

DMP模块的工作流程如下：

**Step 1: 相关体构建。** 将 $I_1$ 和 $I_2$ 分别编码为潜在表示 $V_1$ 和 $V_2$，计算两者之间的归一化点积相关体积，以捕获跨帧运动信息：

$$\mathcal{C}\{\mathbf{u}, \mathbf{d}\} = \frac{1}{N} \sum_{k=1}^{N} V_1^{(k)}(\mathbf{u}) \cdot V_2^{(k)}(\mathbf{u} + \mathbf{d})$$

其中 $\mathbf{u}$ 为像素位置，$\mathbf{d}$ 为位移向量，$N$ 为通道数。

**Step 2: 运动掩码预测。** 基于相关体 $\mathcal{C}$，通过轻量网络预测运动掩码 $\tilde{M}_{pred}$，用于区分动态前景区域与静态背景区域。

**Step 3: 混合潜在融合。** 利用膨胀后的预测掩码 $d_r(\tilde{M}_{pred})$ 融合 $V_1$ 的背景区域和 $V_2$ 的前景区域，生成条件信号 $\mathcal{V}_M$：

$$\mathcal{V}_M = V_2 \odot d_r(\tilde{M}_{pred}) + V_1 \odot \{1 - d_r(\tilde{M}_{pred})\}$$

其中 $d_r(\cdot)$ 为膨胀操作（膨胀半径 $r=2$），$\odot$ 表示逐元素乘法。这一融合策略使扩散模型能感知动态区域的位置，从而在去噪过程中有针对性地合成前景与背景。

### 条件去噪与训练目标

**条件构建。** 将 $V_1$、$V_2$ 和 $\mathcal{V}_M$ 沿通道维度拼接，形成条件输入 $x_{cond}$，为去噪U-Net提供完整的跨帧上下文。

**去噪预测头。** 扩散模型 $\theta$ 以噪声潜在 $x_t$、条件 $x_{cond}$ 和时间嵌入 $\mathrm{PE}(t)$ 为输入，直接预测干净潜在 $\tilde{x}_0$（而非预测噪声）：

$$\tilde{x}_0 = \theta([x_t, x_{cond}, \mathrm{PE}(t)])$$

消融实验证实，预测 $x_0$ 的去噪目标比预测噪声更适合图像对齐任务，在相同条件下PSNR更高。

**加权去噪损失。** 利用预测掩码 $\hat{M}_{pred}$ 对前景和背景区域施加不同权重的L2损失，引导模型聚焦于动态区域：

$$L_{\mathrm{Denoising}} = (1-\gamma)(1-\hat{M}_{pred})(I_{gt}-I_{pred})_2 + \gamma(\hat{M}_{pred})(I_{gt}-I_{pred})_2$$

其中 $\gamma$ 为前景权重系数。

**总体训练目标。** 联合优化加权去噪损失和掩码交叉熵损失：

$$L_{\mathrm{Total}} = \lambda_1 L_{\mathrm{Denoising}} + \lambda_2 L_{\mathrm{Mask}}$$

超参数设置为 $\lambda_1=2$，$\lambda_2=0.1$，下采样因子 $s=4$。

### 动态感知去噪推理

推理阶段从纯噪声 $x_T$ 开始，采用迭代更新策略逐步去噪（$T=1000$，步长 $\Delta=20$）：

$$\{x_T \to \hat{x}_0^{(T)}\} \to \{x_{T-\Delta} \to \hat{x}_0^{(T-\Delta)}\} \to \cdots \to \{x_1 \to \hat{x}_0^{(1)}\}$$

每一步利用上一步的预测结果作为下一轮的条件输入，实现增量式细化。最终 $\hat{x}_0^{(1)}$ 经解码器 $\mathcal{D}$ 还原为对齐后的RGB图像。



## 实验与关键发现

### 主实验结果

DMAligner 在自建 DSIA 数据集以及合成/真实世界基准上均取得了最优或极具竞争力的对齐质量，验证了“扩散模型直接生成对齐视图”这一范式的有效性。

**DSIA 数据集定量评估（Table 2）。** 在 DSIA 的四个子集（LcLf、LcSf、ScLf、ScSf）上，DMAligner 的平均 PSNR/SSIM 达到 **26.67 / 0.81**，全面超越所有对比方法，包括基于光流的 PWCNet（Sun et al., ICCV 2018）、RAFT（Teed and Deng, ECCV 2020）、FlowFormer++（Shi et al., CVPR 2023）、FlowDiffuser（Luo et al., CVPR 2024）、DPFlow（Morimitsu et al., CVPR 2025），以及基于深度/扩散的 COGS（Jiang et al., ACM SIGGRAPH 2024）和 GenWarp（Seo et al., NeurIPS 2024）。需要指出的是，Table 2 中标 † 的方法在计算 PSNR/SSIM 时排除了遮挡和鬼影区域（基于前后一致性检查），这使流式方法在指标上可能更具优势；但 DMAligner 在全图（未排除区域）结果上同样保持领先。

**DSIA 定性结果（Figure 4）。** 在视觉对比中，DMAligner 生成的对齐图像最接近真值，尤其在遮挡边界和动态前景区域，鬼影和背景失真显著少于 DPFlow、COGS 和 GenWarp。这直接印证了扩散模型在“多对一映射导致不可见区域”这一瓶颈上的生成优势。

**Sintel 与 DAVIS 数据集泛化评估（Table 3）。** 由于真实场景缺乏像素级对齐真值，采用 LPIPS 和 DreamSim 度量预测图 $I_{pred}$ 与参考帧 $I_1$ 的感知相似度。DMAligner 在两个数据集上均取得最低的平均 LPIPS / DreamSim（**0.211 / 0.108**），优于 DPFlow 和 GenWarp。定性结果（Figure 5、Figure 6）进一步表明，DMAligner 在合成场景（Sintel）和真实场景（DAVIS）中均能稳定保持背景结构，避免流式方法常见的边缘撕裂和前景模糊。

**下游 HDR 任务验证（Figure 7）。** 将 HDRFlow（Xu et al., CVPR 2024）中的光流对齐模块替换为 DMAligner 后，HDR 融合结果中的鬼影和背景畸变显著减少，尤其在遮挡区域和运动物体周围。这表明 DMAligner 的对齐质量可直接转化为下游任务的增益，而非仅在像素指标上占优。

### 消融实验

Table 4 系统消融了预测目标和 DMP 模块的作用。

![[assets/figures/papers/paper_list_l2466_https_arxiv_org_abs_2602_23022/figures/012_Table_4.jpg]]
*Table 4: Ablation studies of predict targets and our DMP*

- **预测目标选择。** 在相同条件下，预测干净潜在 $\tilde{x}_0$ 的去噪目标比预测噪声 $\epsilon$ 获得更高的 PSNR/SSIM（完整模型 26.67/0.81 vs. 对应噪声预测变体更低值）。这表明图像对齐任务中直接回归图像信号比回归噪声更有利于保留高频细节和结构一致性。
- **DMP 模块贡献。** 移除 DMP 后（即仅用 $V_1$、$V_2$ 作为条件，无动态掩码融合），性能出现明显下降（Table 4 中 (b) vs. (e) 对比）。这证明 DMP 通过潜在空间中的前景/背景差异化融合，使扩散训练聚焦于动态区域，是框架的核心使能组件。

### 压力测试

Figure 8 展示了性能随运动幅度的变化曲线。随着帧间运动幅度增大，DPFlow 和 GenWarp 的性能退化速度明显快于 DMAligner。DMAligner 在大运动场景下仍能保持相对稳定的对齐质量，这归因于其生成式范式不依赖显式光流场的稠密匹配，避免了大幅运动下光流估计失败导致的灾难性失真。

![[assets/figures/papers/paper_list_l2466_https_arxiv_org_abs_2602_23022/figures/011_Figure_8.jpg]]
*Figure 8: Stress test: performance vs. motion magnitude*

### 输入信息公平性说明

Table 1 对比了各方法的输入需求。DMAligner 仅需两张连续 RGB 图像（$I_1$, $I_2$），而 COGS 需要深度图和掩码，AccidentalGS（Mao et al., ICCV 2025）依赖相机参数，GenWarp 需要单图及语义条件。输入信息的不对等可能影响比较的绝对公平性，但 DMAligner 在信息更受限的条件下仍取得最优结果，反而强化了其方法优势的证据强度。

![[assets/figures/papers/paper_list_l2466_https_arxiv_org_abs_2602_23022/figures/004_Table_1.jpg]]
*Table 1: Comparison of network inputs among DPFlow [34], COGS [14], AccidentalGS [33], GenWarp [41] and our DMAligner. Other optical flow networks (PWCNet [44], RAFT [45], FlowFormer++ [42], FlowDiffuser [28]) have the same input structure as DPFlow*

### 补充图表

![[assets/figures/papers/paper_list_l2466_https_arxiv_org_abs_2602_23022/figures/006_Table_2.jpg]]
*Table 2: Quantitative comparison on our DSIA dataset across four subsets (LcLf, LcSf, ScLf, and ScSf) using PSNR and SSIM metrics, higher scores indicate better performance. The average (“Avg”) across all subsets summarizes overall results. † indicates that occlusion and ghost regions are excluded during metric computation, as determined by forward-backward consistency check [50]*

![[assets/figures/papers/paper_list_l2466_https_arxiv_org_abs_2602_23022/figures/010_Table_3.jpg]]
*Table 3: Quantitative comparison on Sintel and DAVIS dataset. Due to the lack of ground truth for precise evaluation, we compute LPIPS and DreamSim [9] between*

![[assets/figures/papers/paper_list_l2466_https_arxiv_org_abs_2602_23022/figures/009_Figure_7.jpg]]
*Figure 7: Comparison of HDR results using flow-based method HDRFlow [49], DPFlow [34] and our DMAligner. Our DMAligner significantly reduces ghosting and background distortions, especially around occluded regions and moving objects*

![[assets/figures/papers/paper_list_l2466_https_arxiv_org_abs_2602_23022/figures/005_Figure_4.jpg]]
*Figure 4: Qualitative comparisons between DPFlow [34], COGS [14], GenWarp [41] and our DMAligner on our DSIA dataset*

![[assets/figures/papers/paper_list_l2466_https_arxiv_org_abs_2602_23022/figures/007_Figure_5.jpg]]
*Figure 5: Qualitative comparisons between DPFlow [34], GenWarp [41] and our DMAligner on Sintel dataset*

![[assets/figures/papers/paper_list_l2466_https_arxiv_org_abs_2602_23022/figures/008_Figure_6.jpg]]
*Figure 6: Qualitative comparisons between DPFlow [34], GenWarp [41] and our DMAligner on the real-world DAVIS dataset*



## 定位与知识库关联

### 1. 与光流对齐范式的边界

DMAligner 的核心突破在于**将对齐问题从“显式几何估计+像素搬运”重构为“条件扩散生成”**，从而绕开了传统光流对齐范式的结构性瓶颈。

传统光流对齐遵循两条主线：
- **金字塔warping + cost volume**：以 **PWCNet** (Sun et al., ICCV 2018) 为代表，通过多尺度特征金字塔和局部代价体进行光流估计，再以图像warping完成对齐。这类方法在遮挡边界和大幅度运动下会因warping无法处理“多对一映射”而产生鬼影与空洞。
- **循环全对场变换**：以 **RAFT** (Teed and Deng, ECCV 2020) 为代表，通过迭代更新光流场提升精度，但其本质仍依赖显式warping，无法生成遮挡区域的有效像素。后续的 **FlowFormer++** (Shi et al., CVPR 2023) 引入掩码cost volume自编码预训练，**DPFlow** (Morimitsu et al., CVPR 2025) 提出自适应双金字塔结构，均是在光流估计精度上精进，而未改变“估计→warping”的基本范式。

DMAligner 与上述方法的**适用边界**在于：
- **输入需求**：DMAligner 仅需两张连续RGB图像（I₁, I₂），无需深度图、运动掩码或相机内参/外参；而光流方法虽然输入同样简洁，但其输出是光流场而非对齐图像，对齐图像需额外warping步骤。
- **遮挡处理**：光流方法在遮挡区域无法生成有效像素（warping的固有缺陷）；DMAligner 通过扩散模型的生成能力直接合成完整对齐视图，从机制上避免了鬼影问题。
- **动态信息利用**：光流方法依赖光流场处理动态区域，但光流本身是“运动矢量”而非“语义理解”；DMAligner 的 DMP 模块在潜在空间通过相关体计算和掩码融合，使模型能区分前景动态与背景静态，从而在训练中聚焦动态区域。

### 2. 与扩散/生成式对齐方法的差异

近年来，扩散模型也被引入图像对齐相关任务，但 DMAligner 在**任务定义、条件机制和训练策略**上均有本质区别。

- **FlowDiffuser** (Luo et al., CVPR 2024)：将扩散模型用于**光流估计**而非直接生成对齐图像。其输出仍是光流场，后续仍需warping步骤，因此无法解决遮挡区域的生成问题。DMAligner 则直接生成对齐视图，跳过了warping环节。
- **GenWarp** (Seo et al., NeurIPS 2024)：基于扩散模型进行单图新视图合成，具备语义保持的生成warping能力。但其任务本质是“新视图合成”，需要相机位姿变换作为条件，且输入为单张图像；DMAligner 的任务是“跨帧对齐”，以两张连续帧为输入，无需相机参数，且通过 DMP 模块显式利用跨帧动态信息。
- **COGS** (Jiang et al., ACM SIGGRAPH 2024) 和 **AccidentalGS** (Mao et al., ICCV 2025)：前者需要深度和掩码输入的稀疏视图合成，后者利用3D高斯喷洒处理意外相机运动对齐。两者均依赖额外的几何先验（深度、相机参数或3D表示），而 DMAligner 在仅有两张RGB输入的条件下即可完成对齐，适用场景更广。

### 3. 知识库定位：生成式对齐的新范式

DMAligner 在知识库中的定位可归纳为以下三个维度：

**范式层面**：将图像对齐从“判别式光流估计”推进到“生成式视图合成”。这一转变的核心因果机制在于：对齐任务本质上要求模型理解场景的三维结构和动态变化，而扩散模型的生成能力天然适合处理遮挡、光照变化和复杂运动等光流方法难以建模的情况。

**机制层面**：提出“动态感知扩散训练”（Dynamics-aware Diffusion Training），通过 DMP 模块在潜在空间捕获跨帧动态信息，并以预测掩码引导扩散模型聚焦动态区域。这一设计使扩散模型在训练过程中即获得区分前景/背景的能力，而非在推理时依赖外部运动估计。

**证据强度**：
- 定量证据：DSIA 数据集上平均 PSNR 26.67 / SSIM 0.81，全面超越所有对比方法（Table 2）；Sintel 和 DAVIS 上平均 LPIPS 0.211 / DreamSim 0.108，同样最优（Table 3）。
- 消融证据：移除 DMP 模块后 PSNR 明显下降（Table 4），验证了动态感知机制的关键作用；预测 x₀ 的去噪目标优于预测噪声，表明“直接预测干净潜在”更适合对齐任务。
- 压力测试：在运动幅度增大的条件下，DMAligner 的性能退化速度明显慢于 DPFlow 和 GenWarp（Figure 8），表明其对复杂运动的鲁棒性。

### 4. 局限与开放问题

**当前局限**：
- 扩散模型的迭代去噪推理导致推理速度慢于前馈光流方法，限制了实时应用场景。
- 训练依赖合成数据集（DSIA），在真实场景极端光照或非刚性形变下的泛化边界尚未充分验证。
- DMP 模块的掩码预测精度直接影响对齐质量，在运动模糊严重或低纹理区域可能存在退化风险（需人工验证具体退化模式）。

**开放问题**：
- 能否将 DMP 的动态感知机制泛化到视频帧插值、视频稳定等多帧对齐任务？
- 扩散模型的对齐生成与光流估计是否存在互补关系——例如以光流初始化扩散过程的噪声起点以加速推理？
- 在无真值对齐图像的真实场景中，如何设计自监督训练策略以扩展 DMAligner 的适用范围？

### 5. 方法输入需求对比

| 方法 | 输入需求 | 核心机制 | 出处 |
|------|---------|---------|------|
| PWCNet / RAFT / FlowFormer++ / FlowDiffuser / DPFlow | 两张RGB图像 | 光流估计 + warping | ICCV 2018 / ECCV 2020 / CVPR 2023 / CVPR 2024 / CVPR 2025 |
| COGS | RGB + 深度 + 掩码 | 稀疏视图合成 | Jiang et al., SIGGRAPH 2024 |
| AccidentalGS | RGB + 相机参数 | 3D高斯喷洒对齐 | Mao et al., ICCV 2025 |
| GenWarp | 单张RGB + 相机位姿 | 扩散新视图合成 | Seo et al., NeurIPS 2024 |
| **DMAligner** | **两张RGB图像** | **扩散对齐视图合成 + DMP** | 本文 |



## 原文 PDF

![[paperPDFs/CVPR_2026/DMAligner_Enhancing_Image_Alignment_via_Diffusion_Model_Based_View_Synthesis.pdf]]
