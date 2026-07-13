---
title: "UCMNet: Uncertainty-Aware Context Memory Network for Under-Display Camera Image Restoration"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/UCMNet_Uncertainty_Aware_Context_Memory_Network_for_Under_Display_Camera_Image_Restoration.pdf
project_link: "https://kdhrick2222.github.io/projects/UCMNet"
code_link: null
aliases:
- UUACMN
- UCMNet
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: 引入不确定性引导的自适应处理：通过估计像素级不确定性图并作为先验，驱动可学习的记忆库（Memory Bank）检索高频上下文特征（Context Bank），实现空间自适应的退化修复。
primary_logic: 将不确定性建模为可学习的先验，通过Memory-Context Bank机制将不确定性与高频补偿信息显式关联，使模型能够针对不同区域的衍射/散射退化模式自适应地注入先验知识。
claims:
- HF-UDL损失相较普通UDL在POLED上额外提升0.22 dB PSNR，且可视化显示更少伪影。
- UPT模块通过方向交叉注意力与记忆库检索显著提升PSNR/SSIM，移除不确定性引导导致PSNR下降0.18 dB。
- UCMNet在POLED-Test上以3.2 M参数达到33.81 dB PSNR，超越所有对比方法，且计算效率最优。
- POLED‑Test 上 PSNR↑ = 33.81
---

# UCMNet: Uncertainty-Aware Context Memory Network for Under-Display Camera Image Restoration

> [!tip] 核心洞察
> 将不确定性建模为可学习的先验，通过Memory-Context Bank机制将不确定性与高频补偿信息显式关联，使模型能够针对不同区域的衍射/散射退化模式自适应地注入先验知识。

| 字段 | 内容 |
|------|------|
| 中文题名 | UCMNet：面向屏下摄像头图像复原的不确定性感知上下文记忆网络 |
| 英文题名 | UCMNet: Uncertainty-Aware Context Memory Network for Under-Display Camera Image Restoration |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2604.00381) · [Project](https://kdhrick2222.github.io/projects/UCMNet) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/image_and_video_generation |
| Method | UCMNet (Uncertainty-aware Context-Memory Network) |
| Dataset | POLED‑Test, TOLED‑Test, SYNTH |

> [!tip] 效果简介
> - POLED‑Test 上，PSNR↑ 33.81 vs 33.39 (BNUDC) (+0.42)。
> - TOLED‑Test 上，PSNR↑ 38.37 vs 38.22 (BNUDC) (+0.15)。
> - SYNTH 上，PSNR↑ 46.71 vs not specified (N/A)。

## 概要

屏下摄像头（UDC）技术为智能手机实现真全面屏提供了关键路径，但显示屏的衍射、散射和透光率衰减会引入空间变化的复杂退化——高频细节丢失、网格伪影与局部模糊。现有方法在应对这类局部自适应的精细复原上能力有限。本文提出 **UCMNet**（Uncertainty-aware Context-Memory Network），一个轻量化的不确定性感知上下文记忆网络，核心思路是将不确定性建模为可学习的先验：通过估计像素级不确定性图，驱动可学习的 Memory Bank 与 Context Bank 检索高频补偿特征，实现空间自适应的退化修复。

在方法设计上，UCMNet 构建了 U 型编码器-解码器架构，编码/解码块中引入 **Frequency Convolution Module（FCM）** 显式利用傅里叶域信息增强高频表示；解码块进一步嵌入 **Uncertainty-Prior Transformer（UPT）**，通过垂直-水平交叉注意力与记忆库检索实现不确定性引导的特征提炼。损失函数方面，提出 **High-Frequency Uncertainty-Driven Loss（HF-UDL）**，在拉普拉斯域施加不确定性加权 L1 损失，针对性增强高频细节。

实验结果表明，UCMNet 在 POLED、TOLED 和 SYNTH 三个基准上均取得领先性能：POLED-Test 上以仅 3.2 M 参数达到 **33.81 dB PSNR**，超越 BNUDC（33.39 dB）等现有最优方法，且在 PSNR/SSIM 散点图中处于右上最优区域（**Figure 1**）。消融实验确认，HF-UDL 相较普通 UDL 额外提升 0.22 dB，UPT 中的不确定性引导与记忆库检索机制对性能贡献显著。在严重衍射导致信息丢失的 SYNTH 场景下，UCMNet 仍存在高频细节恢复不足的局限，这指向了引入更强模型先验的未来方向。



屏下摄像头（Under-Display Camera, UDC）技术通过将前置摄像头置于显示屏下方，实现了真正的全面屏体验。然而，光线在穿过显示面板时会发生衍射、散射和衰减，导致捕获的图像出现严重的空间变化退化——主要表现为高频细节丢失、对比度下降以及由像素结构引起的网格状伪影。这种退化模式在空间上高度不均匀：屏幕中心区域与边缘区域的透光率、衍射强度差异显著，使得单一全局滤波器难以有效复原。

现有UDC图像复原方法大致分为两类：一是基于物理建模的预处理管线，通过估计点扩散函数（PSF）进行反卷积，但这类方法对屏幕制造公差和成像条件变化敏感，泛化能力有限；二是基于深度学习的端到端复原网络，如频率分离方法**BNUDC**和频率-空间交互方法**FSI**，它们在特定数据集上取得了进展，但在应对空间变化的复杂退化时仍显不足——尤其是对高频纹理的恢复往往过于平滑，且难以自适应地处理不同区域的差异化退化程度。

更关键的是，现有方法普遍缺乏对“不确定性”的显式建模。在UDC成像中，不同像素位置的信息丢失程度差异巨大：严重衍射区域的信号几乎被噪声淹没，恢复难度远高于轻度退化区域。若模型对所有位置施加同等强度的复原约束，要么在困难区域产生伪影，要么在简单区域过度平滑。因此，**核心瓶颈**在于如何让模型感知并自适应地响应这种空间变化的复原难度。

本文的**核心动机**正是将不确定性从“被动观测”转变为“主动先验”：通过估计像素级的不确定性图，显式地告诉模型“哪里更难复原、哪里需要更多高频补偿”，从而驱动一个可学习的记忆检索机制，为不同退化模式匹配差异化的先验知识。基于这一思想，我们提出了**UCMNet（Uncertainty-aware Context-Memory Network）**，一个轻量化的不确定性感知上下文记忆网络，旨在以更少的参数量实现空间自适应的精细复原，在多个UDC基准上达到最优性能。



## 核心方法与创新机理

UCMNet 的核心创新在于将**不确定性建模从损失函数层面提升为可学习的结构先验**，通过三个紧密耦合的 changed slots 实现了对屏下摄像头（UDC）空间变化退化的自适应复原。

### 创新一：不确定性先验的机制化——Uncertainty-Prior Transformer（UPT）

现有 UDC 方法普遍缺乏对空间变化退化的显式建模能力，仅依赖卷积或通用注意力机制进行均匀处理。UCMNet 的关键突破是通过 **UPT 模块**将像素级不确定性估计转化为驱动自适应特征检索的先验信号（Figure 4）。

具体而言，UPT 在每个解码块中通过方差估计器生成不确定性图，并将其作为查询向量，从可学习的 **Memory Bank（M）**与 **Context Bank（C）**中检索对应的高频补偿特征。这一设计的因果机制在于：Memory Bank 存储了典型的不确定性退化模式，Context Bank 存储了对应的高频补偿信息，两者通过余弦相似度进行匹配检索：

$$s_{ij} = \frac{m_i f_j^{u^\top}}{\|m_i\| \cdot \|f_j^u\|}$$

这种显式的“不确定性-补偿”关联使得模型能够针对不同区域的衍射/散射退化程度，自适应地注入差异化的先验知识。消融实验（Table 5）证实，移除不确定性引导后 PSNR 下降 0.18 dB，验证了该机制的有效性。可学习令牌对的数量 N=256 时达到最佳性能（33.78 dB PSNR），兼顾了效率与表征能力。

### 创新二：频率域特征增强——Frequency Convolution Module（FCM）

UDC 退化的本质特征之一是高频细节的严重丢失与网格伪影的引入。UCMNet 在编码器-解码器的每个块中嵌入 **FCM 模块**（Figure 3b），显式利用傅里叶域信息进行特征增强。该模块对特征进行傅里叶变换后调整振幅分量，再结合空间注意力机制，使得网络能够主动捕捉并补偿因屏下成像导致的高频信息损失。与传统卷积或普通注意力相比，FCM 为后续的 UPT 模块提供了更丰富的频率域表示基础。

### 创新三：高频不确定性驱动损失（HF-UDL）

传统不确定性驱动损失（UDL）在像素空间施加加权 L1 损失，但对高频细节的约束不足。UCMNet 将其扩展为**高频不确定性驱动损失（HF-UDL）**，在拉普拉斯域施加不确定性加权：

$$\mathcal{L}_{\mathrm{HF-UDL}} = \exp(-s) \left\| \Delta(\hat{I}) - \Delta(I_{gt}) \right\|_1 + 2s$$

其中 $\Delta$ 为拉普拉斯算子，$s$ 为不确定性估计。这一设计的因果逻辑在于：拉普拉斯算子天然放大了高频区域的误差信号，与不确定性加权结合后，迫使网络在不确定性高的区域（通常是高频细节丢失严重的位置）投入更多学习容量。消融实验（Table 4）表明，引入 UDL 相较纯 PSNR 损失提升 0.21 dB，替换为 HF-UDL 后再提升 0.22 dB，且可视化结果（Figure 9）显示高频伪影显著减少。

最终，三个 changed slots 形成协同效应：HF-UDL 提供不确定性学习信号，UPT 将该信号转化为结构化的上下文检索先验，FCM 则保证编码器提供充分的频率域表示。这一组合使 UCMNet 在仅 3.2 M 参数下于 POLED-Test 达到 33.81 dB PSNR，超越所有对比方法。



UCMNet 采用 U 型编码器‑解码器架构，以端到端方式直接处理屏下摄像头（UDC）退化图像，无需手工设计的预处理步骤。整体 pipeline 由四个核心模块级联构成：**Frequency Convolution Module（FCM）**、**Uncertainty‑Prior Transformer（UPT）**、**Memory Bank / Context Bank** 和 **Vanilla Transformer**，通过编码器逐级压缩特征、解码器逐级恢复分辨率，并在解码阶段引入不确定性引导的自适应特征精炼。

### 编码器：频率感知特征提取

编码器由多个编码块（encoding block）堆叠而成（Figure 3c）。每个编码块首先通过步长为 2 的 2×2 卷积将空间分辨率减半、感受野加倍，随后由 FCM 对下采样后的特征进行频率域增强。FCM（Figure 3b）显式利用傅里叶域信息：对输入特征执行快速傅里叶变换（FFT），在频域调整振幅分量以强化高频响应，再通过逆变换回到空间域并与空间注意力机制融合。这种设计使编码器在逐级压缩过程中能够主动捕获并补偿由屏下衍射/散射引起的高频细节丢失。

### 解码器：不确定性引导的自适应重建

解码器由多个解码块（decoding block）堆叠而成（Figure 3d）。每个解码块依次包含三个组件：**FCM**、**UPT** 和**转置卷积上采样**。FCM 首先对解码器当前层特征进行频率增强；随后 UPT 作为核心自适应模块，利用估计的像素级不确定性图从 Memory Bank 和 Context Bank 中检索高频补偿上下文，实现空间变化的退化修复；最后通过转置卷积将特征图上采样至更高分辨率。解码器最终输出复原图像，同时每个解码块中的并行方差估计器（variance estimator）产生对应尺度的不确定性图，用于驱动 UPT 的记忆检索和损失函数计算（Figure 5）。

### UPT：不确定性先验驱动的记忆检索与交叉注意力

UPT（Figure 4）是连接不确定性建模与高频补偿的关键桥梁。其内部流程为：

1. **不确定性图生成**：解码块中的方差估计器从输入特征 $F_{in}$ 预测像素级不确定性图，该图编码了每个空间位置受 UDC 退化影响的置信度。
2. **记忆库检索**：将不确定性特征 $F_U$ 作为查询，通过余弦相似度（$s_{ij} = \frac{m_i f_j^{u^\top}}{\|m_i\| \cdot \|f_j^u\|}$）在可学习的 Memory Bank $\mathbf{M} = [m_1, m_2, \ldots, m_N]$ 中检索最匹配的不确定性模式，并从对应的 Context Bank $\mathbf{C} = [c_1, c_2, \ldots, c_N]$ 中提取高频补偿令牌。Memory Bank 与 Context Bank 以令牌对 $(\mathbf{M}, \mathbf{C})$ 的形式联合学习，$N=256$ 时达到最佳效率‑性能平衡。
3. **方向交叉注意力**：检索到的上下文特征与原始特征 $F_{in}$ 通过并行的垂直注意力和水平注意力进行融合，使用可学习的缩放因子 $\alpha$ 控制注意力分布：
   $$F_v = \mathrm{softmax}\left(\frac{\mathbf{Q}_v \mathbf{K}_v^\top}{\sqrt{\alpha}}\right) \mathbf{V}_v, \quad F_h = \mathrm{softmax}\left(\frac{\mathbf{Q}_h \mathbf{K}_h^\top}{\sqrt{\alpha}}\right) \mathbf{V}_h$$
   最终输出 $\hat{F} = 0.5 \times (F_v + F_h) + F_{in}$，其中残差连接保留了原始特征信息。
4. **Vanilla Transformer 全局精炼**：$\hat{F}$ 经过通道自注意力（channel self‑attention）进一步强化全局一致性，产生最终解码块输出 $F_{out}$。

### 训练目标：高频不确定性驱动损失

UCMNet 采用复合损失函数进行端到端训练：
$$\mathcal{L}_{\mathrm{total}} = \lambda_1 \mathcal{L}_{\mathrm{HF-UDL}} + \lambda_2 \mathcal{L}_{\mathrm{PSNR}}$$
其中 $\lambda_1=100$、$\lambda_2=0.5$。核心创新在于 **HF‑UDL（High‑Frequency Uncertainty‑Driven Loss）**，它在拉普拉斯域施加不确定性加权的 L1 损失：
$$\mathcal{L}_{\mathrm{HF-UDL}} = \exp(-s) \left\| \Delta(\hat{I}) - \Delta(I_{gt}) \right\|_1 + 2s$$
其中 $s$ 为不确定性估计，$\Delta$ 为拉普拉斯算子。该损失显式引导模型关注高频区域的重建质量，同时通过不确定性项自适应调节不同区域的损失权重——高不确定性区域（如严重衍射区）获得较低的损失惩罚，避免模型对不可恢复信息过拟合；低不确定性区域则施加更强的重建约束。

### 输入输出流总结

给定 UDC 退化图像 $I_{in}$，pipeline 的完整数据流为：
1. 编码器逐级下采样并通过 FCM 增强频率特征；
2. 瓶颈层特征进入解码器，每个解码块依次执行 FCM → UPT（含不确定性估计、记忆库检索、方向交叉注意力、Vanilla Transformer）→ 上采样；
3. 最终解码块输出复原图像 $\hat{I}$ 及多尺度不确定性图；
4. 使用 HF‑UDL 与 PSNR 损失的加权组合进行监督。

消融实验表明，移除不确定性引导（即用 $F_{in}$ 替代 $F_U$ 作为记忆检索先验）导致 PSNR 下降 0.18 dB（Table 6），验证了不确定性先验对空间自适应修复的关键作用。

### 补充图表

![[assets/figures/papers/paper_list_l2271_https_arxiv_org_abs_2604_00381/figures/003_Figure_3.jpg]]
*Figure 3: Architecture of the proposed method for UDC image restoration. Our model follows a U-shaped encoder–decoder architecture. The core module of the encoding block is the Frequency Convolution Module (FCM), while the decoding block additionally incorporates the Uncertainty Prior Transformer (UPT) block for uncertainty-guided feature refinement*



### 整体架构

UCMNet采用U型编码器-解码器架构（Figure 3），其核心设计围绕两个关键模块展开：**频率卷积模块（FCM）** 和 **不确定性先验Transformer（UPT）**。编码器通过FCM增强频域表示并逐步下采样，解码器则在FCM基础上引入UPT进行不确定性引导的特征精炼，最终通过转置卷积恢复分辨率。

### 频率卷积模块（FCM）

FCM的设计动机在于显式利用傅里叶域信息来捕获和应对屏下成像条件导致的退化（Figure 3b）。该模块通过傅里叶变换将特征映射到频域，对振幅分量进行调整以增强高频表示，再结合空间注意力机制，将增强后的频域特征与原始特征融合。FCM被嵌入到所有编码块和解码块中，为后续的不确定性建模提供更丰富的频率先验。

### 不确定性先验Transformer（UPT）

UPT是UCMNet实现空间自适应复原的核心模块（Figure 4），其关键创新在于将不确定性建模为可学习的先验，并通过记忆库检索机制将不确定性与高频补偿信息显式关联。UPT的处理流程包含三个紧密耦合的子阶段：

![[assets/figures/papers/paper_list_l2271_https_arxiv_org_abs_2604_00381/figures/004_Figure_4.jpg]]
*Figure 4: Architecture of the Uncertainty-Prior Transformer (UPT) block. The uncertainty transformer refines the input feature*

**（1）不确定性引导的上下文生成（Memory-Context Bank检索）**

UPT首先通过方差估计器从输入特征 $F_{in}$ 中预测像素级不确定性图，该不确定性图反映了各空间位置因屏下衍射/散射导致的退化程度。基于此不确定性特征 $F_U$，UPT从一个可学习的**记忆库（Memory Bank）** $\mathbf{M}$ 和**上下文库（Context Bank）** $\mathbf{C}$ 中检索对应的补偿信息：

$$\mathbf{M} = [m_1, m_2, \ldots, m_N], \quad \mathbf{C} = [c_1, c_2, \ldots, c_N]$$

其中 $\mathbf{M}$ 和 $\mathbf{C}$ 为可学习的令牌对，$m_i$ 存储不确定性模式，$c_i$ 存储对应的高频补偿信息，$N$ 为库大小（实验确定最优值为 $N=256$）。检索通过余弦相似度进行：

$$s_{ij} = \frac{m_i f_j^{u^\top}}{\|m_i\| \cdot \|f_j^u\|}$$

检索到的上下文特征为后续的交叉注意力提供了空间自适应的先验知识。

**（2）方向交叉注意力（Vertical-Horizontal Cross-Attention）**

UPT采用并行的垂直方向和水平方向交叉注意力，以高效捕获空间变化的退化模式。具体而言，对垂直和水平方向分别计算Query、Key、Value，并通过带可学习缩放因子 $\alpha$ 的缩放点积注意力进行特征聚合：

$$F_v = \mathrm{softmax}\left(\frac{\mathbf{Q}_v \mathbf{K}_v^\top}{\sqrt{\alpha}}\right) \mathbf{V}_v, \quad F_h = \mathrm{softmax}\left(\frac{\mathbf{Q}_h \mathbf{K}_h^\top}{\sqrt{\alpha}}\right) \mathbf{V}_h$$

两个方向的注意力输出取平均并与输入残差连接，得到不确定性增强的表示：

$$\hat{F} = 0.5 \times (F_v + F_h) + F_{in}$$

消融实验（Table 5）表明，方向交叉注意力与Context Bank的组合（case d）使PSNR达到33.81 dB，显著优于仅使用vanilla transformer的配置（case a），且移除不确定性引导导致PSNR下降0.18 dB（Table 6）。

**（3）Vanilla Transformer全局精炼**

UPT最后通过一个通道自注意力Transformer对 $\hat{F}$ 进行全局一致性增强，输出最终特征 $F_{out}$。

### 损失函数：高频不确定性驱动损失（HF-UDL）

UCMNet在标准不确定性驱动损失（UDL）的基础上，提出了专门针对高频细节增强的**高频不确定性驱动损失（HF-UDL）**：

$$\mathcal{L}_{\mathrm{HF-UDL}} = \exp(-s) \left\| \Delta(\hat{I}) - \Delta(I_{gt}) \right\|_1 + 2s$$

其中 $s$ 为不确定性估计，$\Delta$ 为拉普拉斯算子，$\hat{I}$ 和 $I_{gt}$ 分别为复原图像和真值图像。该损失的核心思想是：在拉普拉斯域（高频域）施加不确定性加权的L1损失，使模型在不确定性高的区域（即退化严重的区域）更关注高频细节的恢复。消融实验（Table 4）验证了HF-UDL的有效性：引入标准UDL相较纯PSNR损失提升0.21 dB PSNR，而替换为HF-UDL再额外提升0.22 dB。

最终训练损失为HF-UDL与PSNR损失的加权组合：

$$\mathcal{L}_{\mathrm{total}} = \lambda_1 \mathcal{L}_{\mathrm{HF-UDL}} + \lambda_2 \mathcal{L}_{\mathrm{PSNR}}$$

其中权重经验性地设为 $\lambda_1 = 100$，$\lambda_2 = 0.5$。

### 方法局限

在SYNTH数据集上，对于衍射导致严重信息丢失的区域，UCMNet仍难以恢复精细细节。论文指出未来计划通过引入更强的模型先验来改善这一问题，但未给出具体方案。

### 补充图表

![[assets/figures/papers/paper_list_l2271_https_arxiv_org_abs_2604_00381/figures/005_Figure_5.jpg]]
*Figure 5: Uncertainty maps are derived from the uncertaintydriven loss, where each decoding block includes parallel mean and variance estimators that jointly predict the restored image and its corresponding uncertainty map*



## 实验与关键发现

### 1. 主实验结果

UCMNet 在 POLED 和 TOLED 两个真实屏下摄像头测试集上均取得了最优定量结果，同时保持极低的参数量（3.2 M），在 PSNR/SSIM 散点图中位于右上角区域，表明性能与效率的综合领先（Figure 1）。

![[assets/figures/papers/paper_list_l2271_https_arxiv_org_abs_2604_00381/figures/001_Figure_1.jpg]]
*Figure 1: PSNR/SSIM comparisons on the POLED and TOLED datasets. Each marker denotes a restoration model positioned by its PSNR (x-axis) and SSIM (y-axis). UCMNet lies in the upperright region, delivering the best performance and computational efficiency among all competing methods*

**Table 1** 汇总了各方法在 POLED-Test 和 TOLED-Test 上的 PSNR、SSIM、LPIPS、DISTS 四项指标。在 POLED-Test 上，UCMNet 的 PSNR 达到 33.81 dB，超出此前最优方法 **BNUDC**（33.39 dB）0.42 dB，较 **FSI**（33.14 dB）提升 0.67 dB。在 TOLED-Test 上，UCMNet 以 38.37 dB 的 PSNR 同样位列第一，领先 BNUDC（38.22 dB）0.15 dB。SSIM、LPIPS 和 DISTS 指标也一致反映 UCMNet 的整体优势。值得注意的是，UCMNet 在无需手工预处理的情况下直接处理 POLED 和 TOLED 输入，展现出较强的鲁棒性和通用性。

在 SYNTH 合成数据集上，UCMNet 的 PSNR 达到 46.71 dB（Table 3），在所有对比方法中表现最佳。视觉对比（Figure 2）进一步显示，UCMNet 在纹理重建和伪影抑制方面明显优于现有方法，误差图中蓝色区域（小误差）更广，黄色区域（大误差）更少。

![[assets/figures/papers/paper_list_l2271_https_arxiv_org_abs_2604_00381/figures/002_Figure_2.jpg]]
*Figure 2: Visual comparison of restored results (top row) and error maps (bottom row) among existing UDC restoration models and the proposed UCMNet. UCMNet shows fewer artifacts and more accurate texture reconstruction (blue: small errors, yellow: large errors)*

验证集结果（Table 2）与测试集一致：UCMNet 在 POLED-Validation 上取得 34.74 dB PSNR，在 TOLED-Validation 上取得 39.17 dB PSNR，均领先于其他方法。

在真实 UDC 数据集（来自 Align-Former）上的补充实验（Table S.2）进一步验证了 UCMNet 的泛化能力，PSNR 和 SSIM 均优于对比方法。

### 2. 消融实验

#### 2.1 损失函数消融

Table 4 在 POLED 数据集上系统地消融了损失函数的设计。以仅使用 PSNR 损失为基线，引入标准不确定性驱动损失（$ \mathcal{L}_{\mathrm{UDL}} $）使 PSNR 提升 0.21 dB；进一步替换为高频不确定性驱动损失（$ \mathcal{L}_{\mathrm{HF-UDL}} $）再额外提升 0.22 dB。Figure 9 的可视化对比表明，$ \mathcal{L}_{\mathrm{HF-UDL}} $ 能更有效地恢复高频细节，减少伪影。最终总损失函数为：

![[assets/figures/papers/paper_list_l2271_https_arxiv_org_abs_2604_00381/figures/010_Table_4.jpg]]
*Table 4: Ablation study of loss functions on POLED [49] dataset*

![[assets/figures/papers/paper_list_l2271_https_arxiv_org_abs_2604_00381/figures/014_Figure_9.jpg]]
*Figure 9: The visualization of the loss function ablation study, where (a), (b), and (c) correspond to the cases in Table 4*

$$
\mathcal{L}_{\mathrm{total}} = \lambda_1 \mathcal{L}_{\mathrm{HF-UDL}} + \lambda_2 \mathcal{L}_{\mathrm{PSNR}}
$$

其中权重 $ \lambda_1 = 100 $、$ \lambda_2 = 0.5 $ 由经验确定。

#### 2.2 UPT 模块消融

Table 5 对不确定性先验 Transformer（UPT）的核心组件进行了消融。以仅使用两个 Vanilla Transformer 模块（无方向交叉注意力）为基准（case a），逐步添加垂直-水平交叉注意力（hv-attention）和 Context Bank 检索机制。最终配置（case d，包含 hv-attention、cross-attention 与 Context Bank）使 PSNR 达到 33.81 dB，显著优于基准配置。Figure 10 的视觉对比也证实了 UPT 各组件对纹理恢复的贡献。

![[assets/figures/papers/paper_list_l2271_https_arxiv_org_abs_2604_00381/figures/012_Table_5.jpg]]
*Table 5: Ablations of UPT on POLED dataset. The case without hv-attention uses two vanilla transformer modules in the UPT*

![[assets/figures/papers/paper_list_l2271_https_arxiv_org_abs_2604_00381/figures/015_Figure_10.jpg]]
*Figure 10: The visualization of the UPT ablation study, where (a), (b), (c), and (d) correspond to the cases in Table 5*

#### 2.3 不确定性引导上下文生成消融

Table 6 对比了使用不同特征作为上下文检索先验的效果。以不确定性特征 $ F_U $（由方差估计器生成的不确定性图）作为先验，比直接使用输入特征 $ F_{in} $ 提高 PSNR 0.18 dB，SSIM 也同步提升。这表明不确定性图能够有效引导 Memory Bank 检索与局部退化模式匹配的高频补偿信息，实现空间自适应修复。

![[assets/figures/papers/paper_list_l2271_https_arxiv_org_abs_2604_00381/figures/013_Table_6.jpg]]
*Table 6: Ablation on the use of Uncertainty-Guided Context Generation. Incorporating uncertainty as guidance for Context generation improves both PSNR and SSIM, demonstrating effective spatial adaptation to locally varying degradations*

#### 2.4 Context-Memory Bank 规模消融

Table S.1 探索了可学习令牌对 $ (\mathbf{M}, \mathbf{C}) $ 的数量 $ N $ 对性能的影响。当 $ N = 256 $ 时，PSNR 达到 33.78 dB、SSIM 达到 0.9626，在精度与效率之间取得最佳平衡。

### 3. 不确定性图可视化与分析

Figure 8 可视化解码器各阶段的不确定性图。不确定性图由每个解码块中并行的均值估计器和方差估计器联合预测（Figure 5）。随着解码器层级逐步恢复分辨率，不确定性图从模糊的全局分布逐渐细化为局部精确的退化指示，高不确定性区域恰好对应衍射/散射导致的严重细节丢失区域。这验证了不确定性先验能够有效定位空间变化的退化，并驱动 UPT 进行针对性的上下文检索。

![[assets/figures/papers/paper_list_l2271_https_arxiv_org_abs_2604_00381/figures/011_Figure_8.jpg]]
*Figure 8: Visualization of uncertainty maps across decoder stages*

### 4. 局限性

在 SYNTH 数据集上，对于衍射导致严重信息丢失的区域，UCMNet 仍难以恢复精细细节。论文指出，未来计划通过引入更强的模型先验来改善这一不足。此外，UCMNet 在低光照增强任务上的初步实验（Table S.3）显示了一定的泛化潜力，但性能提升幅度有限，表明面向其他空间变化退化任务的迁移仍需任务特定的微调策略。

### 5. 关键图表结论汇总

| 图表 | 核心结论 |
|------|----------|
| Figure 1 | UCMNet 在 PSNR/SSIM 散点图中位于右上角，以 3.2 M 参数实现最优性能与效率平衡 |
| Figure 2 | 误差图显示 UCMNet 纹理重建更准确，伪影更少 |
| Table 1 | POLED-Test 33.81 dB，TOLED-Test 38.37 dB，均列第一 |
| Table 4 | $ \mathcal{L}_{\mathrm{UDL}} $ 提升 0.21 dB，$ \mathcal{L}_{\mathrm{HF-UDL}} $ 再提升 0.22 dB |
| Table 5 | UPT 完整配置（hv-attention + Context Bank）显著优于 Vanilla Transformer 基准 |
| Table 6 | 不确定性特征 $ F_U $ 作为先验比 $ F_{in} $ 提高 0.18 dB |
| Table S.1 | Context-Memory Bank 规模 $ N=256 $ 时达到最佳精度-效率平衡 |

![[assets/figures/papers/paper_list_l2271_https_arxiv_org_abs_2604_00381/figures/006_Table_1.jpg]]
*Table 1: Quantitative results on the POLED and TOLED test datasets. Average PSNR, SSIM, LPIPS, and DISTS are reported, with the best and second-best scores colored (↑ higher is better; ↓ lower is better)*



## 定位与知识库关联

### 1. 基线方法与技术谱系

UCMNet 所面对的 UDC 图像复原问题，现有方法可大致归入两条技术路线：**频率域分离**与**通用图像复原架构迁移**。论文中明确对比的基线包括：

- **BNUDC**：频率分离路线的代表，将图像分解为不同频段分别处理，在 POLED 和 TOLED 上长期占据 SOTA 位置（POLED-Test PSNR 33.39 dB，TOLED-Test 38.22 dB）。
- **FSI**：频率-空间交互方法，同样属于针对 UDC 设计的专用架构。
- **Restormer**：基于 Transformer 的通用图像复原架构，代表了将标准复原模型直接迁移到 UDC 场景的尝试。
- **GSAD**：注意力机制驱动的复原基线。
- **Retinexformer** 与 **DarkIR**：低光照增强领域的代表性方法，被引入作为跨任务对比。

从技术谱系上看，UCMNet 的创新并非凭空出现，而是在两个关键维度上对现有路线进行了系统性升级：

| 技术维度 | 现有路线 | UCMNet 的改进 |
|---------|---------|-------------|
| 频率域处理 | BNUDC 的频率分离 | FCM 模块在傅里叶域显式增强振幅分量，结合空间注意力实现更精细的频率域特征利用 |
| 不确定性建模 | 无显式建模，或仅使用标准 UDL 损失 | UPT 模块将不确定性图作为可学习先验，驱动 Memory-Context Bank 检索高频补偿特征 |
| 损失函数 | PSNR loss 或标准 UDL | HF-UDL 损失在拉普拉斯域施加不确定性加权 L1 损失，针对性增强高频细节 |

### 2. 因果机制与性能瓶颈突破

UCMNet 的核心因果机制可以概括为“**不确定性估计 → 记忆库检索 → 自适应补偿**”的闭环：

1. **不确定性图估计**：每个解码块通过并行的均值/方差估计器，联合预测复原图像及其像素级不确定性图（见 Figure 5）。该不确定性图捕捉了由显示屏衍射/散射引起的空间变化退化程度。
2. **Memory-Context Bank 检索**：不确定性特征 $F_U$ 作为查询，通过余弦相似度从可学习的 Memory Bank $\mathbf{M}$ 中检索匹配的不确定性模式，进而从配对的 Context Bank $\mathbf{C}$ 中提取对应的高频补偿信息（见 Eq. (2) 及 Figure 4）。
3. **方向交叉注意力融合**：检索到的上下文特征通过垂直-水平并行的交叉注意力（Eq. (5)）与输入特征融合，实现空间自适应的退化修复。

消融实验（Table 5 和 Table 6）直接验证了这一因果链的有效性：
- 移除不确定性引导，改用输入特征 $F_{in}$ 直接检索，PSNR 下降 **0.18 dB**（Table 6）。
- 移除方向交叉注意力及 Context Bank，PSNR 显著低于完整 UPT 配置（Table 5 case a vs. case d）。
- 引入 HF-UDL 损失相较普通 UDL 额外提升 **0.22 dB** PSNR，且可视化显示更少伪影（Table 4 与 Figure 9）。

### 3. 适用边界与局限

尽管 UCMNet 在 POLED 和 TOLED 上取得了全面领先，其适用边界仍存在明确限制：

- **严重信息丢失场景的复原能力不足**：在 SYNTH 数据集上，对于衍射导致严重信息丢失的区域，UCMNet 仍难以恢复精细细节。论文明确将此列为局限性，并指出未来计划通过引入更强的模型先验来改善。
- **对不确定性估计质量的依赖**：整个 UPT 模块的性能建立在不确定性图准确反映退化程度的前提上。若不确定性估计失准，Memory-Context Bank 的检索机制可能引入不匹配的补偿信息，反而损害复原质量。当前论文未系统分析不确定性估计失败的模式。
- **跨任务泛化未经验证**：UCMNet 的设计（特别是 FCM 和 UPT）紧密耦合于 UDC 的物理退化特性（衍射、散射、网格伪影）。其在其他空间变化退化任务（如低光照增强、去雾）上的泛化能力尚待验证。

### 4. 开放问题

从论文的讨论和局限性声明中，可以提炼出以下待解决的开放问题：

1. **强先验的引入方式**：如何在严重衍射丢失信息时，通过更强的模型先验（如预训练扩散先验、物理退化模型）恢复 SYNTH 数据集上的高频细节？这是论文明确指出的未来方向。
2. **不确定性估计的可靠性**：当前的不确定性图由网络端到端学习，缺乏对估计质量的显式监督或校准机制。能否引入贝叶斯推断或集成方法提高不确定性估计的鲁棒性？
3. **Memory Bank 的可解释性**：可学习的 Memory-Context Bank 令牌对是否确实学到了与物理退化模式对应的可解释表示？论文未对检索到的上下文特征进行可视化或语义分析。
4. **跨任务微调策略**：UCMNet 在其他空间变化退化任务上的泛化能力是否可以通过任务特定微调（如 adapter 或 prompt tuning）进一步提高？这关系到该方法能否从 UDC 专用方案升级为更通用的空间自适应复原框架。



## 原文 PDF

![[paperPDFs/CVPR_2026/UCMNet_Uncertainty_Aware_Context_Memory_Network_for_Under_Display_Camera_Image_Restoration.pdf]]
