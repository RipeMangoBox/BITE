---
title: "ReSplat: Degradation-agnostic Feed-forward Gaussian Splatting via Self-guided Residual Diffusion"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/ReSplat_Degradation_agnostic_Feed_forward_Gaussian_Splatting_via_Self_guided_Residual_Diffusion.pdf
openreview_forum_id: 461VpgnLsi
aliases:
- ReSplat
tags:
- ICLR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
core_operator: "将通用图像恢复扩散模型（DiffUIR）与前馈式高斯泼溅深度耦合，使扩散采样过程中提取的3D几何（高斯中心）能够反向引导多视图一致的恢复，同时恢复后的清晰图像又提升高斯原语的预测质量，形成双向增强。核心控制点包括：GS引导的多视图对齐模块（3D交叉注意力）和退化感知的预过滤权重。"
primary_logic: "通过在残差扩散模型内部嵌入前馈高斯泼溅，让2D图像恢复和3D场景重建互为“自引导”信号：高斯中心提供多视图对应的几何锚点以约束恢复一致性，而逐步净化的图像则去除高斯泼溅中的退化伪影，从而实现无需退化类型先验的鲁棒NVS。"
claims:
- "利用扩散采样过程中生成的3D高斯作为自引导，实现多视图一致的通用图像恢复。"
- "ReSplat在LLFF退化数据集的五种退化（模糊、雪、雾、低光、雨）上均显著优于对比方法，在NVS和IR指标上取得最佳或次优。"
- "在混合退化（雨+模糊、雪+模糊、雾+雪）下，ReSplat的NVS PSNR比DiffUIR最高提升4.79 dB。"
- "消融实验证明对齐模块和预过滤模块均独立且联合提升NVS质量，结合后PSNR达到22.69。"
---

# ReSplat: Degradation-agnostic Feed-forward Gaussian Splatting via Self-guided Residual Diffusion

> [!tip] 核心洞察
> 通过在残差扩散模型内部嵌入前馈高斯泼溅，让2D图像恢复和3D场景重建互为“自引导”信号：高斯中心提供多视图对应的几何锚点以约束恢复一致性，而逐步净化的图像则去除高斯泼溅中的退化伪影，从而实现无需退化类型先验的鲁棒NVS。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | ReSplat：基于自引导残差扩散的退化无关前馈式高斯泼溅 |
| 英文题名 | ReSplat: Degradation-agnostic Feed-forward Gaussian Splatting via Self-guided Residual Diffusion |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=461VpgnLsi); [GitHub](https://github.com/yh-yoon/ReSplat) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction |
| Method | ReSplat |
| Dataset | LLFF degradation (Motion Blur), LLFF degradation (Snow), LLFF degradation (Haze), LLFF degradation (Low-light) |

> [!tip] 效果简介
> - LLFF degradation (Motion Blur) 上，PSNR (NV) 为 23.15，对比 22.75 (DiffUIR)，变化 +0.40。
> - LLFF degradation (Snow) 上，PSNR (NV) 为 24.46，对比 24.24 (DiffUIR)，变化 +0.22。
> - LLFF degradation (Haze) 上，PSNR (NV) 为 21.99，对比 21.56 (DiffUIR)，变化 +0.43。

## 概述

### 问题瓶颈

现有可泛化新颖视角合成（NVS）方法主要面向理想清晰输入，无法统一处理真实世界中常见的模糊、低光、雾、雨、雪等多样退化。即使存在针对特定退化的NVS方法，也缺乏通用性，且未充分利用2D图像恢复领域积累的预训练先验。当输入图像同时包含多种退化时，这一问题更为严重。

### 核心方案

ReSplat 提出了一种退化无关的前馈式高斯泼溅框架，核心思路是将通用图像恢复扩散模型（DiffUIR）与前馈高斯泼溅深度耦合，使两者互为“自引导”信号。具体而言，扩散采样过程中提取的3D高斯中心作为几何锚点，通过**GS引导的多视图对齐模块**约束多视图恢复的一致性；而逐步净化的清晰图像则去除高斯泼溅中的退化伪影，提升高斯原语预测质量。此外，**退化感知预过滤模块**通过预测可靠性图软性抑制伪影区域的聚合权重，进一步净化场景表示。整个框架支持单次前馈即可输出NVS结果，无需退化类型先验。

### 方法定位

- **IR→NV 串行范式**：如 **AiRnet**（Li et al., CVPR 2022）、**PromptIR**（Potlapalli et al., NeurIPS 2023）、**DiffUIR**（Zheng et al., CVPR 2024）等方法先进行图像恢复再进行NVS，但恢复与重建过程解耦，缺乏几何信息对恢复的反馈。
- **仅NVS范式**：如 **GAURA** 直接从退化多视图泛化NeRF，未利用图像恢复先验。
- **ReSplat**：将恢复扩散模型与前馈GS联合训练，在扩散采样循环中交互迭代——GS为恢复提供几何引导，恢复为GS提供净化图像，形成双向增强。

### 主要结果

在LLFF退化数据集上，ReSplat在五种单一退化（模糊、雪、雾、低光、雨）的NVS和IR指标上均显著优于对比方法，相比DiffUIR的NVS PSNR提升0.22–0.89 dB。在混合退化场景下优势更为突出，雾+雪组合的NVS PSNR比DiffUIR提升**4.79 dB**。在DeblurNeRF、REVIDE、LLNeRF三个真实世界退化数据集上，ReSplat同样取得最优NVS结果。消融实验证实对齐模块和预过滤模块各自独立提升质量，联合使用达到最佳性能（PSNR 22.69），验证了两者的互补性。

## 背景与动机

新颖视角合成（Novel View Synthesis, NVS）旨在从稀疏的多视图图像中重建场景并渲染任意新视角，是计算机视觉与图形学中的核心任务。近年来，以3D高斯泼溅（3D Gaussian Splatting, 3DGS）为代表的可泛化前馈方法取得了显著进展，能够从多视图输入中一次性预测场景的显式3D高斯原语，实现高效、高质量的新视角渲染。然而，现有可泛化NVS方法普遍建立在一个隐含假设之上：输入的多视图图像是理想清晰的。这一假设在真实世界的应用中往往难以成立——图像采集过程不可避免地会遭受模糊、低光、雾、雨、雪等多种退化因素的影响。

面对退化的输入，一个直观的解决方案是“先恢复，后合成”（IR→NV），即先利用图像恢复模型对每一帧进行独立去退化，再将恢复后的清晰图像送入NVS管线。这一范式虽然利用了2D图像恢复领域积累的丰富预训练先验，但存在一个根本性的缺陷：单帧独立恢复缺乏跨视图的几何一致性约束，导致不同视角的恢复结果在纹理、光照和边缘上不一致。这种不一致性在后续的3D重建和新视角渲染中会被放大，产生闪烁、伪影和几何错位等严重问题。另一方面，部分工作尝试从退化多视图中直接泛化神经辐射场（NeRF），如**GAURA**，但由于缺乏对退化过程的显式建模，其恢复能力有限，难以应对多样化的退化类型。

更关键的是，真实世界中的退化往往是未知且混合的——例如雨夜场景可能同时包含雨纹、低光照和运动模糊。现有方法要么针对特定退化类型设计（如去模糊NVS、去雨NVS），缺乏通用性；要么在混合退化下性能急剧退化，无法满足实际应用的需求。这一瓶颈的根源在于：2D恢复模型缺少3D几何信息的引导，而3D重建模型又缺少对退化过程的鲁棒建模能力，两者之间缺乏有效的双向信息交换机制。

针对上述问题，本文提出**ReSplat**（Restoration-based feed-forward Gaussian Splatting），一个退化无关的统一框架。其核心动机在于：将通用图像恢复扩散模型与前馈式高斯泼溅深度耦合，使得2D图像恢复和3D场景重建能够互为“自引导”信号——扩散采样过程中生成的3D高斯中心为多视图恢复提供几何锚点以约束一致性，而逐步净化的图像则去除高斯泼溅中的退化伪影，从而在无需退化类型先验的条件下实现鲁棒的NVS。

## 核心创新

### 问题瓶颈：从“特定退化”到“退化无关”的跨越

现有可泛化新颖视角合成（NVS）方法——无论是先恢复后NVS的串行方案（如**AiRnet** Li et al., CVPR 2022；**PromptIR** Potlapalli et al., NeurIPS 2023；**DiffUIR** Zheng et al., CVPR 2024），还是直接从退化多视图泛化NeRF的**GAURA**——均面向理想清晰输入或仅针对单一退化类型设计。真实场景中模糊、低光、雾、雨、雪等退化往往混合出现，这些方法缺乏统一的处理能力，且未能充分利用2D图像恢复领域积累的预训练扩散先验。

ReSplat的核心突破在于：**将通用图像恢复扩散模型（DiffUIR）与前馈式高斯泼溅进行深度耦合，使2D恢复与3D重建互为“自引导”信号**，从而在无需退化类型先验的条件下，实现退化无关的鲁棒NVS。

### 关键机制：双向自引导的残差扩散框架

ReSplat的创新并非简单的模块拼接，而是在扩散采样循环内部建立了三个相互增强的控制点：

**1. 扩散采样中的几何自引导（GS引导的多视图对齐）**

传统DiffUIR仅利用单帧信息进行独立恢复，缺乏跨视图一致性约束。ReSplat在扩散模型的每一步中，利用前馈GS预测的高斯中心 $P_0^\phi$ 作为伪几何锚点，将多视图特征投影到3D空间后执行自注意力，再重投影回各视图。这一“3D交叉注意力”机制使得恢复过程能够感知场景几何结构，从而约束多视图恢复结果在3D空间中的一致性（Figure 3）。消融实验（Table 4）表明，仅添加该对齐模块即可显著提升NVS的PSNR。

**2. 退化感知的软性伪影抑制（预过滤模块）**

前馈GS在聚合多视图特征时，原有的聚合权重 $W^i$（如基于可见性/特征的权重）无法区分退化伪影与真实纹理。ReSplat引入退化感知预过滤模块：将扭曲后的恢复图像与退化图像进行自注意力，预测每视图的可靠性图 $W_{\text{pre}}^i$，最终聚合权重变为 $W_{\text{final}}^i = W_{\text{pre}}^i \cdot W^i$（Figure 4）。该模块以软性门控方式抑制残余伪影区域，同时保留有效细节。消融实验证实，预过滤模块独立提升NVS质量，且与对齐模块联合后达到最佳PSNR 22.69（Table 4）。

**3. 联合训练与迭代交互范式**

不同于“先恢复后NVS”的分步推断，ReSplat将恢复模型与GS模型联合训练，在扩散采样循环中交互迭代：GS从当前估计的清晰图像预测高斯原语，为下一扩散步提供几何引导；逐步净化的图像则去除GS预测中的退化伪影。训练时联合优化残差L1损失和新视角L1损失（Algorithm 1），推理时单次前馈即可输出NVS结果（Algorithm 2）。

### 创新效果验证

上述三个changed slots的协同作用在实验中得到了充分验证：

- **合成退化数据集（LLFF）**：在模糊、雪、雾、低光、雨五种退化上，ReSplat的NVS PSNR均优于最强基线DiffUIR（Table 1），其中低光场景提升最大（+0.89 dB）。
- **混合退化**：在雨+模糊、雪+模糊、雾+雪三种混合退化下，ReSplat的NVS PSNR比DiffUIR最高提升4.79 dB（Table 2），证明双向引导在复杂退化下的鲁棒性远超串行方案。
- **真实世界数据集**：在DeblurNeRF（运动模糊）、REVIDE（雾）、LLNeRF（低光）三个真实退化数据集上，ReSplat均取得最佳PSNR（Table 3），其中低光场景提升达0.92 dB。

### 局限性说明

需要指出的是，扩散细化和迭代交互增加了计算与内存开销，推理速度可能不及纯前馈方案。此外，框架继承了3D高斯泼溅在镜面反射和透明度处理上的固有偏差，且性能依赖于预训练的通用恢复先验——尽管模块化设计允许未来替换更先进的恢复模型。

## 整体框架

![[assets/figures/papers/paper_list_l3_https_openreview_net_forum_id_461VpgnLsi/figures/002_Figure_2.jpg]]
*Figure 2: The overall framework for degaradation-agnostic feed-forward gaussian splatting (GS). A diffusion-based image restoration model restores the original image by iteratively estimating the residual image. During this process, feed-forward GS is performed using the original image generated in the intermediate stages of diffusion sampling. By utilizing the Gaussian points information obtained in this process, the diffusion model receives multi-view information in the next diffusion step, enabling more accurate image restoration*

![[assets/figures/papers/paper_list_l3_https_openreview_net_forum_id_461VpgnLsi/figures/001_Figure_1.jpg]]
*Figure 1: Proposed degradation-agnostic feed-forward Gaussian Splatting (GS) framework. Our framework achieves high-performance universal image restoration and novel view synthesis results through mutual information exchange between the universal image restoration model and the generalizable GS model*

ReSplat 的核心设计是将一个**通用图像恢复扩散模型**与一个**前馈式 3D 高斯泼溅模型**深度耦合，使二者在扩散采样的迭代过程中互为“自引导”信号，从而实现对多种退化类型无差别鲁棒的新颖视角合成（NVS）。

### 总体数据流

框架接收一组带有未知退化的多视图图像 $\{I_{\mathrm{in}}^i\}$ 及其相机位姿 $\{\Pi^i\}$ 作为输入。数据流沿两条主线展开：

1. **恢复-重建循环**：扩散模型以退化图像 $I_{\mathrm{in}}$ 和当前时间步的噪声图 $I_t$ 为输入，逐步预测残差图像 $I_{\mathrm{res}}^\theta$，从而得到伪干净图像 $I_0^\theta = I_{\mathrm{in}} - I_{\mathrm{res}}^\theta$。该伪干净图像被送入前馈 GS 模型，预测 3D 高斯原语参数并渲染目标新视角。
2. **几何反哺**：前馈 GS 模型在预测过程中产生的**高斯中心点云 $P_0^\phi$** 被回传给扩散模型，作为跨视图特征对齐的几何锚点，引导下一扩散步产生多视图一致的恢复结果。

这一双向信息交换使得图像恢复质量与 3D 重建精度在采样过程中协同提升：逐步净化的图像去除了高斯泼溅中的退化伪影，而多视图一致的几何约束又反过来抑制了单帧恢复中的不一致性。

### 核心模块构成

ReSplat 的 pipeline 由四个功能模块有机组成：

| 模块 | 角色 |
|---|---|
| **残差扩散恢复模型**（基于 DiffUIR + 3D 对齐） | 接收退化图像与噪声图，通过迭代预测残差来复原清晰图像；扩散 U-Net 的编码器中嵌入 GS 引导的多视图交叉注意力，确保恢复结果跨视图一致 |
| **前馈高斯泼溅模型** | 从当前估计的清晰多视图图像一次性预测像素级高斯原语（均值 $\mu$、协方差 $\Sigma$、不透明度 $\alpha$、颜色 $c$），并渲染新视角 |
| **GS 引导的多视图对齐模块** | 利用高斯中心 $P_0^\phi$ 作为 3D 查询点，将各视图特征投影到同一 3D 位置执行自注意力，再将增强特征重投影回各视图 |
| **退化感知预过滤模块** | 对扭曲对齐后的恢复图像与原始退化图像进行自注意力，预测每视图的可靠性图 $W_{\mathrm{pre}}^i$，软性调制 GS 聚合权重以抑制残余伪影 |

### 训练与推理范式

与“先恢复后 NVS”的串行方案（如 **DiffUIR**（Zheng et al., CVPR 2024）恢复后接前馈 GS）不同，ReSplat 采用**联合训练、交互式推理**的范式：

- **训练**（Algorithm 1）：同时优化恢复模型 $\theta$ 和 GS 模型 $\phi$，损失函数为残差图的 L1 损失与新颖视角渲染的 L1 损失之和：
  $$\nabla_\theta \|I_{\mathrm{res}} - I_{\mathrm{res}}^\theta(P_0^\phi, I_t, I_{\mathrm{in}}, t)\|_1 + \nabla_\phi \|I_{\mathrm{nv}} - I_{\mathrm{nv}}^\phi(I_{\mathrm{in}} - I_{\mathrm{res}}^\theta, I_{\mathrm{in}})\|_1$$
- **推理**（Algorithm 2）：在扩散采样的每一步，先用当前预测残差更新伪干净图像，再由 GS 模型提取几何信息 $P_0^\phi$ 反馈给下一扩散步，单次前馈即可输出 NVS 结果。

### 关键控制点

框架中两个关键控制点实现了退化无关的鲁棒性：

1. **GS 引导的多视图对齐**：将单帧扩散恢复从“独立逐帧”提升为“几何一致的多视图联合恢复”。高斯中心提供了显式的 3D 对应关系，使跨视图自注意力能够在正确的空间位置交换信息，这是 ReSplat 在混合退化场景下显著优于 DiffUIR（PSNR 最高提升 4.79 dB）的核心原因。
2. **退化感知预过滤权重**：在标准 GS 聚合权重 $W^i$ 之上叠加预测的可靠性图，形成最终权重 $W_{\mathrm{final}}^i(x) = W_{\mathrm{pre}}^i(x) \cdot W^i(x)$。该机制以软性门控方式抑制退化残留区域对高斯原语预测的污染，消融实验证实其独立提升 NVS 质量（Table 4）。

> **注意**：扩散采样循环带来了额外的计算与内存开销，推理速度方面相对于纯前馈方案存在劣势，这是该框架在实际部署中需要权衡的因素。

## 核心模块与公式推导

ReSplat 的核心在于将残差扩散恢复模型与前馈高斯泼溅深度耦合，形成双向增强的推理循环。整体框架包含四个关键模块，其协同方式如下。

### 3D 高斯泼溅前馈映射

前馈 GS 模型从多视图图像中一次性预测像素级高斯原语参数，映射函数为：

$$\phi : \{ (I_{\mathrm{in}}^i, \Pi^i) \}_{i=1}^N \longmapsto \{ (\mu_j, \Sigma_j, \alpha_j, c_j) \}_{j=1}^{H \times W \times N}$$

其中 $I_{\mathrm{in}}^i$ 为第 $i$ 个视角的输入图像，$\Pi^i$ 为对应的相机投影矩阵，输出为每个像素对应的高斯椭球参数：中心位置 $\mu$、协方差矩阵 $\Sigma$、不透明度 $\alpha$ 和颜色 $c$。3D 高斯函数定义为：

$$G(x) = e^{-\frac{1}{2}(x-\mu)^T \Sigma^{-1} (x-\mu)}$$

渲染时，将 3D 高斯投影到 2D 图像平面，通过 α 复合合成像素颜色：

$$C(x') = \sum_{i \in N} c_i \sigma_i \prod_{j=1}^{i-1} (1-\sigma_j), \quad \sigma_i = \alpha_i G_i'(x')$$

### 残差扩散恢复模型

恢复模型采用 DiffUIR（Zheng et al., CVPR 2024）的残差扩散范式。其前向过程在标准加噪基础上引入共享分布项以适配通用图像恢复：

$$I_t = I_{t-1} + \alpha_t I_{res} + \beta_t \epsilon_{t-1} - \delta_t I_{in}$$

其中 $I_{res} = I_{in} - I_0$ 为退化图像与干净图像的残差，$\alpha_t$、$\beta_t$、$\delta_t$ 为时间步相关的系数。反向过程从噪声图逐步减去预测残差和噪声：

$$I_{t-1} = I_t - \alpha_t I_{res}^\theta + \delta_t I_{in} - (\beta_t^2 / \bar{\beta}_t) \epsilon^\theta$$

在确定性隐式采样（DDIM）下，可由预测残差直接复原伪干净图像：

$$I_{t-1} = I_0^\theta + \bar{\alpha}_{t-1} I_{res}^\theta - \bar{\delta}_{t-1} I_{in} \quad \text{s.t.} \quad I_0^\theta = I_{in} - I_{res}^\theta$$

这一公式是双向耦合的关键：扩散采样过程中每一步产生的伪干净图像 $I_0^\theta$ 被送入前馈 GS 模型，而 GS 模型输出的高斯中心又反向引导下一扩散步的多视图对齐。

### GS 引导的多视图对齐模块

该模块嵌入残差扩散模型的编码器中，利用扩散中间步生成的高斯中心 $P_0^\phi$ 作为几何锚点。对于每个高斯中心，将多视图特征投影到该 3D 点，执行自注意力以增强跨视图一致性，再将增强后的特征重投影回各视图。对于离散查询点 $q$，其特征由周围重投影特征通过面积加权插值获得：

$$F_q = \sum_i w_i f_{i,rep}^j \quad \text{where } i \in Q$$

其中 $Q$ 为包含查询点的最小矩形区域内的重投影点集合，$w_i$ 为 2D 插值权重。这一机制使得扩散模型在恢复每个视图时能够感知其他视图的对应几何信息，从而约束多视图恢复的一致性。

### 退化感知预过滤模块

前馈 GS 模型在聚合多视图特征时，原有的聚合权重 $W^i$ 基于可见性和特征相似度，无法区分退化伪影区域。预过滤模块以扭曲后的恢复图像和退化图像为输入，通过自注意力预测每视图的可靠性图 $W_{pre}^i$，最终聚合权重为两者的逐像素乘积：

$$W_{\mathrm{final}}^i(x) = W_{\mathrm{pre}}^i(x) \cdot W^i(x)$$

该模块实质上是一个软性的退化感知门控：残差伪影强烈或跨视图不一致的区域获得较低的 $W_{pre}^i$，从而在特征聚合时被抑制，避免伪影传播到高斯原语预测中。

### 训练与推理范式

训练时（Algorithm 1），联合优化恢复模型 $\theta$ 和前馈 GS 模型 $\phi$，损失函数为残差图的 L1 损失与新视角渲染的 L1 损失之和。推理时（Algorithm 2），在扩散采样的每一步中：先用当前预测残差复原伪干净图像 $I_0^\theta = I_{in} - I_{res}^\theta$，将其送入 GS 模型预测高斯原语 $P_0^\phi$；高斯中心信息反馈给恢复模型用于下一步的多视图对齐。整个过程单次前馈即可输出 NVS 结果，无需退化类型先验。

## 实验与分析

### 核心定量结果：合成退化场景

ReSplat在LLFF退化数据集上，针对五种单一退化类型（运动模糊、雪、雾、低光、雨）进行了系统评估，输入均为三视图。Table 1汇总了新颖视角合成（NV）与多视图图像恢复（IR）的双维度指标。在NV任务上，ReSplat在所有退化类型上均取得最优或次优PSNR，相较最强基线**DiffUIR**（Zheng et al., CVPR 2024）的增益幅度为+0.22 dB（雪）至+0.89 dB（低光）。值得注意的是，低光场景的PSNR提升最为显著（19.76 vs. 18.87），表明多视图几何引导对极端光照退化下的场景重建具有关键作用。在IR任务上，ReSplat同样保持优势，例如雪的IR PSNR达到32.07，比DiffUIR高出0.87 dB，证明双向增强机制不仅惠及NVS，也实质性提升了恢复质量。

![[assets/figures/papers/paper_list_l3_https_openreview_net_forum_id_461VpgnLsi/figures/004_Table_1.jpg]]
*Table 1: Novel View Synthesis (NV) and Image Restoration (IR) results of five corruption types on LLFF degradation dataset with three multi-view inputs. The best scores and second best scores are highlighted with their respective colors. gion, ensuring that features closer to the query point have a higher influence. Therefore, when there is a discrete point q , the multi-view feature F _ { q } that q obtains is as follows*

与**AiRnet**（Li et al., CVPR 2022）和**PromptIR**（Potlapalli et al., NeurIPS 2023）这类“先恢复后NVS”的串行方案相比，ReSplat的优势更为明显。以低光场景为例，AiRnet的NV PSNR仅为17.43，PromptIR为17.83，而ReSplat达到19.76，差距超过1.9 dB。这验证了核心洞察：将恢复与几何估计耦合为交互迭代过程，比独立执行两个任务更能保留场景结构。**GAURA**（仅NVS方案）在多数退化下表现最弱，说明完全忽略图像恢复而直接从退化视图泛化NeRF，难以应对严重退化。

### 混合退化与真实世界场景的鲁棒性

Table 2揭示了ReSplat在混合退化下的压倒性优势。在“雾+雪”组合下，ReSplat的NV PSNR达到20.17，而DiffUIR仅为15.38，差距高达+4.79 dB；在“雨+运动模糊”和“雪+运动模糊”组合下，增益分别为+1.41 dB和+1.02 dB。这种大幅领先说明：当多种退化叠加时，单视图恢复模型（即使如DiffUIR般强大）缺乏跨视图一致性约束，容易在不同视图间产生不一致的恢复伪影，进而严重破坏后续高斯泼溅的几何预测；而ReSplat的GS引导多视图对齐模块（3.3节）恰好弥补了这一缺陷——高斯中心提供的3D锚点强制扩散采样过程维持几何一致性。

![[assets/figures/papers/paper_list_l3_https_openreview_net_forum_id_461VpgnLsi/figures/005_Table_2.jpg]]
*Table 2: Novel View Synthesis results and multi-view image restoration results of three types (rain+motion blur, snow+motion blur, and haze+snow) on LLFF mixed degradation dataset with three multi-view inputs. The best scores are highlighted*

在真实世界数据集上（Table 3），ReSplat同样保持领先。在DeblurNeRF（运动模糊）上PSNR为22.91（vs. DiffUIR 22.68），在REVIDE（雾）上为17.75（vs. 17.26），在LLNeRF（低光）上为22.92（vs. 22.00）。真实世界退化的分布偏移未显著削弱ReSplat的优势，佐证了退化感知预过滤模块（3.4节）的泛化能力——该模块通过自注意力机制学习到的可靠性图并非过拟合于特定合成退化模式。

![[assets/figures/papers/paper_list_l3_https_openreview_net_forum_id_461VpgnLsi/figures/007_Table_3.jpg]]
*Table 3: Novel view synthesis results of three types (motion blur, haze, low-light) on real-world degradation datasets*

### 消融实验：对齐模块与预过滤模块的因果贡献

Table 4通过四个模型变体解耦了两个核心模块的独立与联合效应。基线Model 1（无对齐、无预过滤）的NV PSNR为22.39。仅添加预过滤模块（Model 2）提升至22.57（+0.18 dB），同时LPIPS从0.1979降至0.1913，证明退化感知权重能有效抑制伪影区域对高斯聚合的污染。仅添加对齐模块（Model 3）提升至22.62（+0.23 dB），且SSIM从0.8590升至0.8622，说明多视图对齐主要改善了几何结构的一致性。同时启用两者（Model 4）达到22.69（+0.30 dB），在所有指标上均为最优，验证了两模块的互补性：对齐模块确保多视图恢复的几何一致性，预过滤模块则在几何对齐的基础上进一步净化残余伪影，二者协同而非冗余。

![[assets/figures/papers/paper_list_l3_https_openreview_net_forum_id_461VpgnLsi/figures/008_Table_4.jpg]]

定性消融（Figure 7、Figure 8）进一步佐证了这一结论。Figure 7显示，启用对齐模块后，恢复图像的RGB误差图在高频区域（如物体边缘）显著减弱，说明跨视图自注意力有效消除了视图间的几何错位。Figure 8则展示预过滤模块在保持细节纹理的前提下，选择性抑制了残余退化斑块——这与该模块的“软门控”设计（$W_{\mathrm{final}}^i(x) = W_{\mathrm{pre}}^i(x) \cdot W^i(x)$）一致：它并非硬性剔除像素，而是通过逐像素乘积调制聚合权重，从而在伪影抑制与细节保留之间取得平衡。

### 失败模式与局限性分析

尽管ReSplat在多数场景下表现优异，但以下局限性需关注：

1. **推理效率瓶颈**：扩散采样循环中每步均需执行前馈GS预测与多视图对齐，导致推理延迟显著高于纯前馈方法（如MVSplat）。Table 1中ReSplat与DiffUIR的差距在部分退化上较小（如雪仅+0.22 dB），若应用场景对延迟敏感，需权衡精度增益与计算成本。

2. **极端退化的几何估计失效**：低光场景下ReSplat虽相对提升最大，但绝对PSNR（19.76）仍显著低于其他退化类型（如雪24.46）。这表明在极端低光条件下，前馈GS从近乎全黑的退化图像中预测的高斯中心$P_0^\phi$本身不可靠，导致“自引导”信号质量下降，形成误差传播。该问题根源在于3DGS的显式点表示对输入图像质量高度敏感。

3. **镜面反射与透明表面的固有偏差**：ReSplat继承了3D高斯泼溅在处理镜面反射和透明度时的已知缺陷，这在真实世界数据集（如REVIDE雾场景中的玻璃反射）中可能被放大。

4. **分布外退化的泛化未知**：预过滤模块的训练数据覆盖了五种单一退化及三种混合退化，但Table 5和Table 6显示，在真实世界去雨和去雪数据集上，ReSplat并未在所有指标上取得绝对最优（D-Splat/3DGSplat在某些指标上更优），说明针对特定退化的专用方法在分布内仍可能占优。对于训练中未见过的退化组合，预过滤模块的可靠性图预测能力尚需进一步验证。

### 关键图表结论速览

- **Table 1**：ReSplat在五种合成退化上全面优于DiffUIR，低光场景增益最大（+0.89 dB PSNR），IR指标同步提升。
- **Table 2**：混合退化下优势急剧扩大，“雾+雪”场景领先DiffUIR达4.79 dB，证明多视图对齐在复杂退化下的关键作用。
- **Table 3**：真实世界数据集上保持领先，验证了方法的实用鲁棒性。
- **Table 4**：对齐模块与预过滤模块独立有效且互补，联合启用达到最优PSNR 22.69。
- **Figure 7/8**：对齐模块消除几何不一致，预过滤模块软性抑制伪影而不损细节。

### 补充图表

![[assets/figures/papers/paper_list_l3_https_openreview_net_forum_id_461VpgnLsi/figures/003_Figure_3.jpg]]
*Figure 3: GS-guided multi-view alignment. Module embedded in the residual diffusion model that shares info between adjacent views using Gaussian centers. Figure 4: Pre-filtering with warped features. Warped inputs are self-attended to form prefiltering weights for feature aggregation*

![[assets/figures/papers/paper_list_l3_https_openreview_net_forum_id_461VpgnLsi/figures/010_Table_5.jpg]]
*Table 5: Novel View Synthesis (NV) results of Rain corruption on the real-world deraining dataset with three multi-view inputs. The best scores and second best scores are highlighted*

![[assets/figures/papers/paper_list_l3_https_openreview_net_forum_id_461VpgnLsi/figures/011_Table_6.jpg]]
*Table 6: Novel View Synthesis (NV) results of Snow corruption on the real-world desnowing dataset with three multi-view inputs. The best scores and second best scores are highlighted*

## 方法谱系与知识库定位

### 1. 与现有工作的关系

ReSplat 的核心贡献在于将**通用图像恢复（UIR）扩散模型**与**前馈式3D高斯泼溅（3DGS）**深度耦合，形成双向增强的“自引导”机制。其方法定位可从以下两条技术路线的交叉点来理解。

#### 1.1 相对于“先恢复后NVS”串行范式

现有工作普遍采用分步策略：先用图像恢复模型处理退化输入，再将恢复后的清晰图像送入新颖视角合成（NVS）模型。典型代表包括：

- **AiRnet**（Li et al., CVPR 2022）与 **PromptIR**（Potlapalli et al., NeurIPS 2023）：两者均先对退化多视图图像进行统一恢复，再执行NVS。该范式将恢复与合成解耦，恢复模型无法感知下游3D任务对多视图一致性的需求。
- **DiffUIR**（Zheng et al., CVPR 2024）：作为当前最强的通用图像恢复扩散模型之一，DiffUIR 在单图像恢复上表现优异。将其输出直接送入前馈GS模型（即 DiffUIR→NVS 串行基线）构成了 ReSplat 最直接的对比基线。

ReSplat 对这一范式的改造体现在两个关键“插槽”上：

| 插槽 | 串行基线值 | ReSplat 改造 |
|------|-----------|-------------|
| 图像恢复模型 | 独立单图像 DiffUIR，仅利用当前帧信息 | 嵌入 **GS引导的多视图对齐模块**（3D交叉注意力），在扩散每一步利用伪几何 $P_0^\phi$（高斯中心）进行跨视图特征自注意力，实现多视图一致恢复 |
| 高斯聚合权重 | MVSplat 等前馈GS中基于可见性/特征的逐视图标准聚合权重 $W^i$ | 引入**退化感知预过滤模块**，预测可靠图 $W_{pre}^i$，最终权重 $W_{final}^i = W_{pre}^i \cdot W^i$，软性抑制伪影区域 |

这一改造使得恢复模型与GS模型不再是串行的上下游关系，而是**扩散采样循环中的交互迭代**：GS为恢复提供几何引导，恢复为GS提供净化图像。

#### 1.2 相对于“仅NVS”的直接泛化范式

另一类方法尝试从退化多视图直接泛化NVS，不经过显式的图像恢复阶段：

- **GAURA**：从退化多视图直接泛化NeRF，但缺乏通用性，通常针对特定退化类型设计。
- **D-Splat / 3DGSplat**：针对特定真实世界数据集的GS变体，在各自目标退化上表现良好（如 D-Splat 在真实去雨数据集上取得最优PSNR 24.35），但同样不具备退化无关的通用性。

ReSplat 不同于此类方法的关键在于：它**显式地利用了2D图像恢复领域预训练的通用先验**（DiffUIR），而非从零开始学习退化到3D的映射。这使得它能够统一处理模糊、低光、雾、雨、雪等五种退化，并在混合退化场景下展现出显著优势（Haze+Snow 场景下 NVS PSNR 比 DiffUIR 串行基线提升 4.79 dB）。

#### 1.3 知识库定位

从更宏观的视角看，ReSplat 处于以下三个研究方向的交汇点：

1. **可泛化新颖视角合成**（如 pixelNeRF、MVSplat 等前馈范式）：ReSplat 继承了前馈GS的快速推理能力，单次前馈即可输出NVS结果。
2. **通用图像恢复扩散模型**（如 DiffUIR）：ReSplat 将扩散模型的迭代细化能力引入3D场景重建，并赋予其多视图几何感知。
3. **3D引导的图像恢复**：ReSplat 的核心洞察——“用3D几何引导多视图恢复一致性”——为图像恢复领域提供了新的思路，即利用显式3D表示（高斯椭球）作为跨视图信息融合的锚点。

### 2. 适用边界与局限

尽管 ReSplat 在退化无关的NVS任务上表现出色，其适用边界和局限同样需要明确：

1. **计算与内存开销**：扩散细化和迭代交互显著增加了推理成本。与纯前馈GS方法相比，扩散采样步骤带来了额外的计算延迟，限制了其在高分辨率场景或实时应用中的部署。这是该方法当前最突出的工程瓶颈。

2. **3DGS表示的固有偏差**：ReSplat 继承了3D高斯泼溅在镜面反射和透明度处理上的不足。当场景中存在大量反射表面或半透明物体时，高斯椭球的显式表示可能无法准确建模光线传输。

3. **对预训练先验的依赖**：方法的性能建立在 DiffUIR 的通用恢复能力之上。虽然模块化设计允许替换更先进的恢复模型，但在预训练先验覆盖不足的退化类型（如极端噪声、严重压缩伪影）上，性能可能下降。

4. **极端退化下的几何估计可靠性**：在雾、低光等视觉信息严重缺失的条件下，前馈GS预测的高斯中心 $P_0^\phi$ 可能包含显著的几何误差。由于该伪几何直接用于引导多视图对齐，几何估计的偏差会传播到恢复过程，形成误差累积。这一问题在真实世界低光数据集 LLNeRF 上已有体现——尽管 ReSplat 仍优于 DiffUIR（PSNR 22.92 vs. 22.00），但绝对性能仍远低于清晰输入场景。

### 3. 开放问题

1. **推理效率优化**：如何在不损害恢复质量的前提下降低扩散采样步骤的推理延迟？可能的路径包括：减少扩散步数、采用蒸馏策略、或设计更轻量的对齐模块。这一问题的解决将直接影响该方法走向实际应用的可能性。

2. **动态场景与严重遮挡**：当前框架假设多视图输入来自静态场景。能否将自引导机制扩展到动态场景（如包含运动物体的退化视频）或存在严重遮挡的退化输入？这需要解决伪几何在动态/遮挡区域的有效性问题。

3. **3D表示的替代方案**：3DGS的显式点表示在极端退化下的几何估计是否可靠？能否通过其他3D表示（如NeRF的隐式场、或混合表示）增强几何引导的鲁棒性？这涉及到“引导信号”本身的质量保证问题。

4. **分布外退化的泛化**：预过滤模块通过自注意力学习退化感知的可靠性图，但其训练数据覆盖的退化类型有限。在遇到未见过的退化组合（如雨+低光、雾+模糊等训练中未出现的混合退化）时，该模块能否保持鲁棒性？初步实验（Table 2 的混合退化结果）提供了积极信号，但更系统的分布外评估仍有待开展。

5. **单视图退化场景的拓展**：当前方法依赖多视图输入来构建几何引导。在仅有一张退化图像的单视图场景下，自引导机制将失效。如何将框架适配到单视图退化NVS是一个值得探索的方向。

## 原文 PDF

![[paperPDFs/ICLR_2026/ReSplat_Degradation_agnostic_Feed_forward_Gaussian_Splatting_via_Self_guided_Residual_Diffusion.pdf]]
