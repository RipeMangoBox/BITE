---
title: "Text-to-3D by Stitching a Multi-view Reconstruction Network to a Video Generator"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/Text_to_3D_by_Stitching_a_Multi_view_Reconstruction_Network_to_a_Video_Generator.pdf
project_link: https://gohyojun15.github.io/VIST3A/
code_link: null
openreview_forum_id: kI27Niy4xY
aliases:
- VVVS3A
- T3BSMVRNVG
tags:
- ICLR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
core_operator: "引入模型缝合技术，将预训练的三维重建网络的部分层作为解码器，与视频VAE编码器通过线性缝合层连接；并采用直接奖励微调，将生成模型的潜空间与缝合解码器对齐。"
primary_logic: "视频VAE编码器产生的潜向量与预训练三维模型早期层的激活之间存在线性可转移性，可通过最小二乘法找到最佳缝合层，从而复用强大的三维重建先验，无需大量三维训练数据。"
claims:
- "模型缝合可以有效地将预训练3D模型作为VAE解码器，并在新视图合成上优于原始3D模型。"
- "VIST3A框架在文本到3DGS生成任务上显著超越现有方法，在T3Bench、SceneBench和DPG-Bench上均取得最优性能。"
- "直接奖励微调（结合多视图质量、三维一致性和文本对齐）比仅使用多视图生成损失或仅部分奖励产生更高的生成质量和三维一致性。"
- "T3Bench 上 Imaging Quality = 58.83 (Wan+MVDUSt3R)"
---

# Text-to-3D by Stitching a Multi-view Reconstruction Network to a Video Generator

> [!tip] 核心洞察
> 视频VAE编码器产生的潜向量与预训练三维模型早期层的激活之间存在线性可转移性，可通过最小二乘法找到最佳缝合层，从而复用强大的三维重建先验，无需大量三维训练数据。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 通过缝合多视图重建网络与视频生成器实现文本到三维生成 |
| 英文题名 | Text-to-3D by Stitching a Multi-view Reconstruction Network to a Video Generator |
| 会议/期刊 | ICLR 2026 (Oral) |
| Links | [paper](https://openreview.net/forum?id=kI27Niy4xY) · [Project](https://gohyojun15.github.io/VIST3A/) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction |
| Method | VIST3A (VIdeo VAE STitching and 3D Alignment) |
| Dataset | T3Bench, SceneBench, DPG-Bench, User Study (Text Alignment) |

> [!tip] 效果简介
> - T3Bench 上，Imaging Quality 为 58.83 (Wan+MVDUSt3R)，对比 54.32 (Director3D)，变化 +4.51。
> - SceneBench 上，Imaging Quality 为 64.87 (Wan+AnySplat)，对比 58.19 (VideoRFSplat)，变化 +6.68。
> - DPG-Bench 上，Global score 为 81.82 (Wan+MVDUSt3R)，对比 69.70 (SplatFlow)，变化 +12.12。

## 概要

### 问题背景

文本到三维（Text-to-3D）生成旨在从自然语言描述直接合成三维场景表示。近年来，基于潜扩散模型（LDM）的视频生成器在视觉内容生成上取得了显著进展，但将其用于三维生成时面临一个核心瓶颈：现有方法通常需要从零开始训练一个三维VAE解码器，将视频潜向量映射为三维表示（如高斯泼溅或点云）。这类解码器缺乏预训练的三维重建先验，导致生成质量低、三维一致性差；同时，生成模型的潜空间与解码器之间缺乏有效对齐，进一步限制了端到端性能。

### 核心方法

本文提出 **VIST3A**（VIdeo VAE STitching and 3D Alignment），一个通用框架，通过两个互补组件解决上述问题：

1. **模型缝合（Model Stitching）**：将预训练的前馈式三维重建网络（如MVDUSt3R、AnySplat、VGGT）的部分层作为解码器，缝合到视频VAE编码器之后。具体而言，通过最小二乘法找到一个线性缝合层，将编码器潜向量映射到三维模型中间层的激活空间，从而复用强大的三维重建先验，无需大量三维训练数据。该方法在闭式解下即可使VAE潜空间与三维解码器良好匹配。

2. **直接奖励微调（Direct Reward Finetuning）**：在缝合完成后，采用直接奖励微调将视频生成模型的潜空间与缝合解码器对齐。奖励函数由多视图图像质量、三维表示质量和三维一致性三部分构成，通过最大化奖励来引导生成模型产生可解码、三维一致的潜向量，同时保留原有的生成损失。

### 主要结果

VIST3A在多个文本到三维生成基准上取得最优性能：

- **T3Bench**：VIST3A（Wan+MVDUSt3R）的Imaging Quality达到58.83，相比最优基线Director3D的54.32提升**+4.51**。
- **SceneBench**：VIST3A（Wan+AnySplat）的Imaging Quality达到64.87，相比VideoRFSplat的58.19提升**+6.68**。
- **DPG-Bench**：VIST3A（Wan+MVDUSt3R）的Global score达到81.82，相比SplatFlow的69.70提升**+12.12**。
- **用户研究**：在文本对齐和视觉质量的平均排名上，VIST3A均显著优于对比方法（平均排名1.54 vs. 2.74–3.03）。

消融实验证实，缝合能有效增强新视图合成能力（缝合AnySplat到任意视频模型后均优于单独使用AnySplat），而完整奖励微调（多视图质量+三维一致性+文本对齐）相比仅用多视图生成损失或部分奖励，在场景级指标上取得最佳表现。

### 方法定位

VIST3A属于**基于视频扩散模型的三维生成方法**，其关键创新在于通过模型缝合技术将视频生成与三维重建解耦并重新组合，避免了从零训练三维解码器的需求。与Matrix3D-omni、Director3D、Prometheus3D、SplatFlow、VideoRFSplat等现有方法相比，VIST3A不依赖定制化的三维VAE训练，而是直接复用预训练三维基础模型的解码能力，在生成质量和三维一致性上实现了显著提升。



文本到三维生成旨在从自然语言描述中直接合成三维内容，其核心挑战在于同时满足视觉质量、三维几何一致性与文本语义对齐。近年来，基于潜扩散模型（Latent Diffusion Models, LDMs）的生成框架在二维图像和视频生成领域取得了显著进展，推动了研究者将其扩展至三维生成任务。这类方法通常遵循一个两阶段范式：首先训练一个三维变分自编码器（3D VAE），将三维表示压缩至潜空间；随后在该潜空间上训练扩散模型以实现从文本到三维潜向量的生成。

然而，这一范式存在一个关键的瓶颈：**现有方法中的三维解码器需要从零开始学习三维重建能力，而这一能力本身极为复杂且数据需求巨大**。具体而言，当前的三维 VAE 解码器通常是在二维 VAE 的基础上从头训练或微调而来，其三维重建的先验知识远不如专门为三维视觉任务设计的预训练模型丰富。与此同时，生成模型（如视频扩散模型）的潜空间与这些能力不足的解码器之间缺乏有效的对齐机制，导致生成的潜向量在解码时产生三维不一致的几何结构、模糊的纹理或语义退化。

图 2 清晰地对比了 VIST3A 与现有 LDM-based 三维生成器在架构设计上的根本差异：传统方法（图 2 上半部分）依赖于一个从多视图二维潜向量到三维输出的定制解码器，该解码器需要独立学习三维重建的全部知识；而 VIST3A（图 2 下半部分）另辟蹊径，通过模型缝合技术直接复用预训练三维重建网络的强大先验，仅需学习一个轻量的线性缝合层即可桥接两个异构模型。

这一瓶颈在文本到三维高斯泼溅（3D Gaussian Splatting, 3DGS）生成任务中尤为突出。现有方法如 **Matrix3D-omni**、**Director3D**、**Prometheus3D**、**SplatFlow** 和 **VideoRFSplat** 虽然在特定场景下取得了进展，但在生成质量、三维一致性和文本对齐方面仍存在明显不足。例如，在 T3Bench 基准上，表现最好的 Director3D 的成像质量（Imaging Quality）仅为 54.32；在 SceneBench 上，VideoRFSplat 的成像质量为 58.19；在 DPG-Bench 上，SplatFlow 的全局分数为 69.70。这些结果反映了现有方法在处理复杂场景、精细几何和长文本描述时的能力上限。

本文的动机正是源于上述观察：**视频生成模型擅长从文本生成丰富的视觉内容潜向量，而三维基础模型擅长将潜表示解码为一致的三维几何——两者的能力天然互补，但缺乏有效的连接机制**。VIST3A 的核心洞察在于，视频 VAE 编码器产生的潜向量与预训练三维模型早期层的激活之间存在线性可转移性，这为模型缝合提供了理论基础。通过最小二乘法找到最佳缝合层，可以将三维重建网络的部分层复用为解码器，从而在不依赖大量三维训练数据的情况下，赋予生成模型强大的三维重建先验。进一步地，采用直接奖励微调将生成模型的潜空间与缝合解码器对齐，确保生成的潜向量能够被准确、一致地解码为高质量的三维表示。



## 核心方法与创新机理

VIST3A 的核心创新在于用**模型缝合（Model Stitching）**替代了传统潜扩散模型（LDM）文本到三维管线中“从零训练三维解码器”的范式，并通过**直接奖励微调（Direct Reward Finetuning）**实现生成模型与缝合解码器的潜空间对齐。这两个组件共同构成了一个可泛化的框架，其设计直击现有方法的两个瓶颈：解码器三维重建能力不足，以及生成模型与解码器之间缺乏有效对齐。

### 创新点一：模型缝合——复用预训练三维重建先验

**基线做法**：现有基于 LDM 的文本到三维方法（如 Matrix3D-omni、Director3D、Prometheus3D、SplatFlow、VideoRFSplat 等）通常采用“视频 VAE 编码器 + 从头训练或微调的三维 VAE 解码器”架构。解码器需要从多视图二维潜变量中学习重建三维表示，这一过程对三维训练数据的规模和质量高度敏感，且解码器本身缺乏预训练三维先验的加持。

**VIST3A 的改变**：VIST3A 不再训练自定义三维解码器，而是将预训练的**前馈式三维重建网络**（如 VGGT、AnySplat、MVDUSt3R）的尾段直接缝合到视频 VAE 编码器之后，作为三维解码器使用。具体而言，给定视频 VAE 编码器 $\mathcal{E}$ 和三维重建模型 $F_{1:l}$，缝合后的三维 VAE 定义为：

$$\mathcal{M}_{\mathrm{stitched}} = F_{k^{\star}+1:l} \circ \mathbf{S} \circ \mathcal{E}(\pmb{x}) = \hat{\pmb{y}},\quad \mathcal{D}_{\mathrm{stitched}} = F_{k^{\star}+1:l} \circ \mathbf{S}$$

其中 $\mathbf{S}$ 是**唯一需要训练的线性缝合层**，$k^{\star}$ 是最佳缝合层索引。这一设计的核心洞察在于：视频 VAE 编码器产生的潜向量与预训练三维模型早期层的激活之间存在**线性可转移性**——通过求解最小二乘问题即可找到最优线性映射：

$$\mathbf{S}^{\ast}_{k} = \arg \min_{\mathbf{S}_{k}} \| \mathbf{B} \mathbf{S}_{k} - \mathbf{A}_{k} \|_{F}^{2} = \left( \mathbf{B}^{\top} \mathbf{B} \right)^{-1} \mathbf{B}^{\top} \mathbf{A}_{k}$$

其中 $\mathbf{B}$ 为编码器潜向量矩阵，$\mathbf{A}_k$ 为三维模型第 $k$ 层激活矩阵。缝合层选择以最小均方误差（MSE）为准则：$k^{\star} = \arg\min_k \|\mathbf{B} \mathbf{S}_k^{\ast} - \mathbf{A}_k\|_F^2$。缝合后仅需对线性层 $\mathbf{S}$ 和三维模型尾段 $F_{k^{\star}+1:l}$ 进行轻量微调（使用 LoRA），以自监督方式（无需三维标注）逼近原始三维模型的预测输出。

**关键证据**：Table 3 表明，将 AnySplat 缝合到任意视频模型上，其新视图合成性能始终优于单独使用 AnySplat，验证了缝合策略的有效性。Table 5 进一步显示，缝合模型在点云重建和相机姿态估计上几乎完整保留了原始三维基础模型的能力。

### 创新点二：直接奖励微调——对齐生成模型与缝合解码器

**基线做法**：现有方法通常仅使用多视图生成损失（如流匹配损失）对生成模型进行微调，以适配其自定义解码器。这种纯生成损失的微调方式缺乏对三维一致性和解码质量的显式约束，容易导致语义退化、模糊以及动态视频带来的鬼影问题。

**VIST3A 的改变**：VIST3A 采用**直接奖励微调**，将生成模型的潜空间与缝合三维解码器对齐。总损失函数定义为：

$$L_{\mathrm{total}} = L_{\mathrm{gen}} - r(z_0(\theta, c, z_T), c)$$

其中 $L_{\mathrm{gen}}$ 为原始生成损失（如流匹配损失），$r(\cdot)$ 为奖励函数，依赖于最终潜变量 $z_0$ 和文本提示 $c$。奖励函数由三个互补的奖励项组成：

- **多视图图像质量奖励**：$R_{\text{quality}}(I, c) = s_{\text{clip}}(I, c) + s_{\text{hps}}(I, c) - 2$，结合 CLIP 和 HPSv2.1 分数评估生成视图的视觉质量与文本对齐度。
- **三维一致性奖励**：$R_{\text{consistency}}(I_{\text{decode}}, I_{\text{rendered}}(\hat{\pi})) = -|I_{\text{decode}} - I_{\text{rendered}}(\hat{\pi})|_1 - 0.25 \times \text{LPIPS}(I_{\text{decode}}, I_{\text{rendered}}(\hat{\pi}))$，惩罚解码视图与由三维表示渲染视图之间的像素级距离和感知差异。
- **三维表示质量奖励**：对生成的三维高斯泼溅或点云本身的质量进行评估。

**关键证据**：Table 6 的消融实验表明，使用完整奖励（多视图质量 + 三维一致性 + 三维表示质量）在 SceneBench 上取得最佳 Imaging Aesthetic（64.87）和 Unified Reward 分数，显著优于仅使用多视图生成损失或仅使用部分奖励的配置。Figure 7 的定性对比进一步显示，直接奖励微调消除了多视图微调中出现的语义退化和模糊，同时有效抑制了动态视频导致的鬼影问题。

### 创新点三：缝合范式的鲁棒性优势

VIST3A 的缝合范式还带来了一个额外优势：相比“先 VAE 解码再送入三维模型”的顺序式流程，缝合后的 VGGT 解码器对 VAE 潜空间的扰动具有更强的鲁棒性。Figure 8 在 ETH3D 数据集上的实验表明，在潜空间中注入不同强度的噪声时，缝合模型始终优于顺序式流程，说明缝合层起到了隐式的正则化和适配作用，使三维解码器能够容忍生成模型潜空间中的不完美。

### 方法谱系与知识库定位

VIST3A 位于**文本到三维生成**与**模型重用**的交叉点。与依赖 Score Distillation Sampling（SDS）的优化式方法不同，VIST3A 属于**前馈式生成**范式，一次前向传播即可从文本生成三维表示。与现有 LDM-based 三维生成器（如 Director3D、SplatFlow 等）相比，VIST3A 的独特贡献在于**将模型缝合技术引入三维生成领域**，证明了视频生成模型与三维重建模型之间可以通过简单的线性层实现有效连接，从而绕过了训练专用三维解码器所需的大量三维数据和计算资源。这一思路与自然语言处理领域的“模型缝合”研究一脉相承，但在三维视觉生成场景中首次得到了系统验证。



![[assets/figures/papers/paper_list_l22_https_openreview_net_forum_id_kI27Niy4xY/figures/036_Figure_10.jpg]]
*Figure 10: Log-MSE values in Eq. 2 across various video VAEs. Early layers of feedforward models show lower MSE values within each VAE architecture. While lower MSE correlates with better stitching performance within the same VAE (e.g., layer 2 outperforms layer 16 for Wan in Fig 5), absolute MSE values cannot predict performance across different VAE architectures. For instance, despite CogVideoX and Hunyuan + AnySplat having the lowest absolute MSE (0.008), SVD + AnySplat achieves the best performance (21.48 PSNR) in Table 3*

VIST3A 的整体流程由两个互补的核心组件构成：**模型缝合（Model Stitching）** 与 **直接奖励微调（Direct Reward Finetuning）**，二者协同将视频生成模型与三维重建网络整合为端到端的文本到三维生成系统（图 3）。

### 模块组成与数据流

系统包含四个关键模块，按推理时的数据流向依次为：

1. **视频扩散生成模型（Video LDM）**：以文本提示 $c$ 为条件，从初始噪声 $z_T$ 出发，通过去噪过程生成连续的潜向量序列 $z_0$。主干模型采用 Wan 2.1 T2V large，在实验中亦兼容 CogVideoX、SVD、HunyuanVideo 等架构。
2. **视频 VAE 编码器 $\mathcal{E}$**：接收视频 LDM 输出的潜向量，将其解码为多视图图像序列 $\pmb{x}$。该编码器继承自预训练视频生成模型的 VAE 组件，无需额外训练。
3. **线性缝合层 $\mathbf{S}$**：一个可训练的线性映射（在实现中限制为 3D 卷积），将编码器输出的图像潜空间激活 $\mathbf{B}$ 映射到目标三维模型第 $k^\star$ 层的激活空间 $\mathbf{A}_{k^\star}$。缝合层的最优权重通过最小二乘问题以闭合形式求解：
   $$\mathbf{S}^{*}_{k} = \arg \min_{\mathbf{S}_{k}} \| \mathbf{B} \mathbf{S}_{k} - \mathbf{A}_{k} \|_{F}^{2} = \left( \mathbf{B}^{\top} \mathbf{B} \right)^{-1} \mathbf{B}^{\top} \mathbf{A}_{k}$$
   最佳缝合层 $k^\star$ 选取使该均方误差（MSE）最小的层。
4. **缝合的三维解码器 $F_{k^\star+1:l}$**：预训练前馈式三维重建模型（如 MVDUSt3R、AnySplat、VGGT）的后半段，接收缝合层输出的激活，直接重建出三维表示 $\hat{\pmb{y}}$（高斯泼溅或点云）。

整个缝合后的三维 VAE 可形式化表示为：
$$\mathcal{M}_{\mathrm{stitched}} = F_{k^{\star}+1:l} \circ \mathbf{S} \circ \mathcal{E}(\pmb{x}) = \hat{\pmb{y}}, \quad \mathcal{D}_{\mathrm{stitched}} = F_{k^{\star}+1:l} \circ \mathbf{S}$$

### 训练流程

VIST3A 的训练分为两个阶段，均不依赖三维标注数据：

**阶段一：缝合解码器微调（自监督）**。在确定最佳缝合层 $k^\star$ 后，以原始三维模型在真实多视图数据上的预测作为伪目标，对缝合层 $\mathbf{S}$ 和三维解码器 $F_{k^\star+1:l}$ 进行微调。微调采用 LoRA 更新解码器参数，损失函数为各输出头的加权 $\ell_1$ 损失之和。训练数据来自 DL3DV-10K 和 ScanNet。

**阶段二：直接奖励微调（对齐训练）**。冻结缝合后的 VAE 解码器，仅微调视频 LDM 的生成参数 $\theta$。训练目标为最小化总损失：
$$L_{\mathrm{total}} = L_{\mathrm{gen}} - r(z_0(\theta, c, z_T), c)$$
其中 $L_{\mathrm{gen}}$ 为原有的生成损失（如流匹配损失），$r(\cdot)$ 为奖励函数。奖励函数综合了三个维度：多视图图像质量（CLIP + HPSv2.1 分数）、三维表示质量、以及三维一致性（解码视图与渲染视图间的 $\ell_1$ 距离和 LPIPS 感知差异）。训练模拟完整去噪轨迹，迫使生成模型输出可被缝合解码器正确解码、且具有三维一致性的潜向量。训练数据使用 DL3DV-10K 并辅以 HPSv2 训练集的文本提示。

### 与现有范式的本质区别

现有基于潜扩散模型（LDM）的三维生成方法通常需从零训练或微调一个定制的三维 VAE 解码器，将二维潜空间映射到三维输出。这要求解码器同时学习三维重建能力，且生成模型与解码器之间缺乏有效对齐。

VIST3A 的核心创新在于**绕过从零学习三维重建的瓶颈**：通过模型缝合技术，直接复用预训练三维基础模型的强大重建先验，仅需训练一个轻量的线性缝合层和少量 LoRA 参数。随后的直接奖励微调则系统性地解决了生成模型潜空间与缝合解码器之间的错配问题，将多视图质量、三维一致性和文本对齐统一纳入优化目标。



VIST3A 框架由两个互补组件构成：**模型缝合**（Model Stitching）与**直接奖励微调**（Direct Reward Finetuning）。前者构建一个可解码三维表示的 VAE 解码器，后者将视频生成模型的潜空间与该解码器对齐。

### 模型缝合：构建三维 VAE

现有基于潜扩散模型（LDM）的三维生成方法通常需要从零训练一个三维 VAE 解码器，解码能力受限于三维训练数据的规模与多样性。VIST3A 的核心洞察是：视频 VAE 编码器产生的潜向量与预训练三维重建模型早期层的激活之间存在**线性可转移性**，因而可以通过一个轻量的线性缝合层将二者桥接，直接复用预训练三维模型的强大重建先验。

设视频 VAE 编码器为 $\mathcal{E}$，其将输入的多视图图像 $\pmb{x}$ 编码为潜向量。设前馈式三维重建模型为 $F_{1:l}$，其由 $l$ 层组成。在某个中间层 $k$ 处将模型切分为 $F_{1:k}$ 和 $F_{k+1:l}$ 两部分。缝合后的三维 VAE 定义为：

$$\mathcal{M}_{\mathrm{stitched}} = F_{k^{\star}+1:l} \circ \mathbf{S} \circ \mathcal{E}(\pmb{x}) = \hat{\pmb{y}},\ \mathcal{D}_{\mathrm{stitched}} = F_{k^{\star}+1:l} \circ \mathbf{S}$$

其中 $\mathbf{S}$ 为线性缝合层，$\hat{\pmb{y}}$ 为缝合模型输出的三维表示（如高斯泼溅或点云），$\mathcal{D}_{\mathrm{stitched}}$ 即为缝合得到的三维解码器。

**缝合层选择** 通过最小二乘问题求解。对于每个候选层 $k$，收集一批训练样本，将编码器输出记为矩阵 $\mathbf{B}$，三维模型第 $k$ 层的激活记为 $\mathbf{A}_k$，则最优线性映射为：

$$\mathbf{S}^{\ast}_{k} = \arg \min_{\mathbf{S}_{k}} \| \mathbf{B} \mathbf{S}_{k} - \mathbf{A}_{k} \|_{F}^{2} = \left( \mathbf{B}^{\top} \mathbf{B} \right)^{-1} \mathbf{B}^{\top} \mathbf{A}_{k}$$

选择使均方误差（MSE）最小的层作为最佳缝合层 $k^{\star}$。实验证明，缝合层 MSE 越低，下游点云重建质量越高（Figure 5），且该 MSE 上界约束了缝合后的理论风险（Insulla et al., 2025）。

缝合后的解码器还需经过**自监督微调**：以原始三维模型的输出作为伪目标，对 $\mathbf{S}$ 和 $F_{k^{\star}+1:l}$ 进行微调，损失为各输出项 $\ell_1$ 损失的加权和。缝合层被约束为三维卷积，解码器尾部采用 LoRA 进行参数高效更新。

### 直接奖励微调：对齐生成模型与缝合解码器

缝合 VAE 仅保证编码-解码通路有效，但生成模型（如 Wan 2.1 LDM）的潜空间未必能产生适合该解码器的潜向量。直接奖励微调通过模拟完整去噪轨迹并最大化奖励信号来解决这一对齐问题。

总损失函数为生成损失与奖励函数的组合：

$$L_{\mathrm{total}} = L_{\mathrm{gen}} - r(z_0(\theta, c, z_T), c)$$

其中 $L_{\mathrm{gen}}$ 为流匹配损失，$z_0(\theta, c, z_T)$ 为从纯噪声 $z_T$ 经生成模型 $\theta$ 去噪得到的最终潜变量，$c$ 为文本提示，$r(\cdot)$ 为奖励函数。

奖励函数由三个维度加权构成（详见附录 B.2）：

- **多视图图像质量奖励**：结合 CLIP 分数与 HPSv2.1 分数，衡量生成视图与文本 $c$ 的视觉一致性和美学质量：
  $$R_{\text{quality}}(I, c) = s_{\text{clip}}(I, c) + s_{\text{hps}}(I, c) - 2$$

- **三维一致性奖励**：惩罚解码视图 $I_{\text{decode}}$ 与从三维表示渲染的视图 $I_{\text{rendered}}(\hat{\pi})$ 之间的像素级差异和感知差异：
  $$R_{\text{consistency}}(I_{\text{decode}}, I_{\text{rendered}}(\hat{\pi})) = -|I_{\text{decode}} - I_{\text{rendered}}(\hat{\pi})|_1 - 0.25 \times \text{LPIPS}(I_{\text{decode}}, I_{\text{rendered}}(\hat{\pi}))$$

- **三维表示质量奖励**：对重建的三维表示本身进行评估（如点云完整度、高斯泼溅的几何合理性）。

消融实验（Table 6）表明，仅使用多视图生成损失会导致语义退化和模糊，仅使用部分奖励无法充分约束三维一致性；完整奖励组合（多视图质量 + 三维一致性 + 表示质量）在 SceneBench 上取得了最优的 Imaging Aesthetic（64.87）和 Unified Reward 分数，同时有效抑制了动态视频带来的鬼影问题（Figure 7）。



## 实验与关键发现

### 核心定量结果

VIST3A 在三个主流的文本到三维高斯泼溅（3DGS）生成基准上均取得了最优性能，显著超越现有方法。

**T3Bench 与 SceneBench（Table 1）**。在 T3Bench 上，VIST3A: Wan+MVDUSt3R 的 Imaging Quality 达到 58.83，比最强基线 Director3D（54.32）提升 +4.51。在 SceneBench 上，VIST3A: Wan+AnySplat 以 64.87 的 Imaging Quality 领先 VideoRFSplat（58.19）达 +6.68。该基准同时报告了 VBench 定义的图像质量、美学质量、CLIP 分数及 UnifiedReward 等多维度指标，避免了无参考指标（如 NIQE、BRISQUE）可能产生的虚假高分问题。

![[assets/figures/papers/paper_list_l22_https_openreview_net_forum_id_kI27Niy4xY/figures/010_Table_1.jpg]]
*Table 1: Quantitative results on T3Bench and SceneBench. Table 3: Stitching enhances NVS*

**DPG-Bench（Table 2）**。在 DPG-Bench 的 Global 综合评分上，VIST3A: Wan+MVDUSt3R 取得 81.82，较 SplatFlow（69.70）提升 +12.12，表明该方法在多样化提示下的整体生成质量具有显著优势。

![[assets/figures/papers/paper_list_l22_https_openreview_net_forum_id_kI27Niy4xY/figures/011_Table_2.jpg]]
*Table 2: Quantitative results on DPG-Bench*

**用户研究（Table 4）**。28 位参与者对随机样本进行排序的结果显示，VIST3A 在文本对齐（平均排名 1.54）和视觉质量（平均排名 1.45）两个维度均获最低平均排名（越低越好）。超过 68% 的案例中 VIST3A 在文本对齐上被排为第一，超过 87% 的案例在视觉质量上被排为第一，远优于 VideoRFSplat（文本对齐 2.74）和 Director3D（文本对齐 3.03）。

![[assets/figures/papers/paper_list_l22_https_openreview_net_forum_id_kI27Niy4xY/figures/013_Table_4.jpg]]
*Table 4: User study results. Participants rank five methods in terms of text alignment and visual quality of rendered videos from generated 3DGS (lower average rank is better)*

### 缝合增强新视图合成

Table 3 系统验证了模型缝合对新视图合成（NVS）的增益：将 AnySplat 缝合到任意视频模型上，其 NVS 性能始终优于单独使用 AnySplat。这表明缝合后的解码器不仅保留了原三维模型的重建能力，还借助视频 VAE 编码器的表征获得了额外提升。

![[assets/figures/papers/paper_list_l22_https_openreview_net_forum_id_kI27Niy4xY/figures/012_Table_3.jpg]]

在点云重建任务上（Table 5），缝合模型在点云质量和相机姿态估计精度上与原三维基础模型相比几乎没有损失，证明缝合过程有效保留了预训练三维模型的几何重建精度。

![[assets/figures/papers/paper_list_l22_https_openreview_net_forum_id_kI27Niy4xY/figures/017_Table_5.jpg]]
*Table 5: Results of point map reconstruction with stitched models*

### 直接奖励微调消融

Table 6 在 SceneBench 上对直接奖励微调进行了组件消融，比较了五种配置：（1）无微调；（2）仅多视图生成损失微调；（3）仅三维一致性奖励微调；（4）仅质量奖励微调；（5）完整奖励微调（质量 + 一致性）。结果表明，完整奖励微调在 Imaging Aesthetic（64.87）和 Unified Reward 上均取得最优，验证了多视图图像质量奖励与三维一致性奖励的互补性。

![[assets/figures/papers/paper_list_l22_https_openreview_net_forum_id_kI27Niy4xY/figures/023_Table_6.jpg]]
*Table 6: Ablation study on direct reward finetuning on SceneBench. We compare (1) no finetuning; (2) multi-view-only finetuning (generative loss only); (3) reward tuning with 3D-consistency reward only; (4) reward tuning with quality reward only; and (5) reward tuning with both rewards (full)*

定性对比（Figure 7）进一步揭示了不同微调策略的行为差异：预训练视频模型（无微调）产生动态视频，导致重建的三维场景出现严重鬼影；仅使用多视图生成损失微调可减少运动并提升三维一致性，但引入了语义退化和模糊；而直接奖励微调则产生更锐利的渲染结果，且更好地对齐输入文本提示。

### 缝合层选择准则

Figure 5 展示了缝合层 MSE 与点云质量的关系：在 7-Scenes 数据集上，缝合层 MSE 较低的层确实产生更好的点云重建质量，支持以线性最小二乘拟合的 MSE 作为层选择准则。这一观察与 Insulla et al.（2025）的理论一致——缝合风险被缝合层处的 MSE 上界所约束。

Figure 6 的 CKA 可视化显示，CKA 指标虽能反映整体表征退化程度，但在层选择精度上不如 MSE。

**跨架构的局限性**。Figure 10 展示了不同视频 VAE 架构的缝合层 log-MSE 值。尽管在同一 VAE 内部，较低 MSE 与更好的缝合性能相关（如 Wan 的第 2 层优于第 16 层），但绝对 MSE 值无法跨架构预测性能。例如，CogVideoX 和 Hunyuan+AnySplat 具有最低的绝对 MSE（0.008），但 SVD+AnySplat 在 Table 3 中取得了最佳 PSNR（21.48）。这意味着缝合层选择必须针对每个 VAE-三维模型对单独搜索，MSE 的跨架构可迁移性有限。

### 鲁棒性分析

Figure 8 比较了缝合 VGGT 与顺序式流程（先 VAE 解码再 VGGT 重建）在 ETH3D 数据集上对潜空间噪声注入的鲁棒性。结果表明，缝合模型对 VAE 潜空间的扰动具有更强的容忍度。这一特性对生成式场景至关重要——视频扩散模型产生的潜向量天然存在一定偏差，缝合解码器的鲁棒性确保了三维输出的稳定性。

![[assets/figures/papers/paper_list_l22_https_openreview_net_forum_id_kI27Niy4xY/figures/029_Figure_8.jpg]]
*Figure 8: Pointmap estimation performance comparison on ETH3D dataset between the stitched VGGT and the sequential approach (VAE followed by VGGT) under varying noise scales injected into the latent space. The stitched model demonstrates greater robustness to noise injection in the VAE*

### 生成质量与扩展能力

定性结果（Figure 4、Figure 11、Figure 12）展示了 VIST3A 在 T3Bench、SceneBench 和 DPG-Bench 上的生成样例。VIST3A 生成的三维场景具有逼真的细节、准确的几何结构和外观，且忠实反映输入提示的细粒度语义。

Figure 13 和 Figure 16 展示了在交互式查看器中直接观察的 3DGS 结果。VIST3A 在明显改变的相机轨迹下仍保持高视觉质量，证明了其在新视角下的鲁棒性和稳定性。通过扩展视频生成模型的帧数，VIST3A 能够生成连贯的大规模场景。

Figure 9 展示了基于提示的相机视角控制能力：包含“Aerial drone shot”的提示产生高角度俯视视角，而“Camera pans left to right”则生成从左到右扫视场景的轨迹，表明视频生成模型固有的相机运动先验被有效传递到三维生成流程中。

![[assets/figures/papers/paper_list_l22_https_openreview_net_forum_id_kI27Niy4xY/figures/032_Figure_9.jpg]]
*Figure 9: Viewpoint control in 3DGS generation with prompts. (Top) The prompt containing “Aerial dronshot” results in a high-angle downward perspective. (Bottom) The prompt containing “Camera pans left to right” generates a trajectory where the viewpoint sweeps across the scene from left to right. Table 7: Video generation performance comparison between the original video generator and VIST3A on VBench*

### 失败模式与局限

1. **时序依赖假设**。缝合模型的编码器继承自视频生成模型，要求输入图像排列为连续、时序连贯的视频序列。对无序多视图图像的支持未经验证，在此类数据上可能出现性能下降。

2. **缝合层搜索的跨架构不可迁移性**。如 Figure 10 所示，绝对 MSE 无法跨 VAE 架构预测缝合性能，每个 VAE-三维模型对需要独立的层搜索过程，增加了实际部署的工程成本。

3. **长序列生成的极限未探明**。尽管扩展帧数可生成大规模场景，但随着帧数进一步增加，生成质量和一致性是否保持稳定仍是开放问题。



## 定位与知识库关联

### 1. 方法谱系与基线关系

VIST3A 的核心定位是：**将文本到三维生成问题重新表述为“视频生成器 + 三维解码器”的缝合与对齐问题**，从而绕开现有潜扩散模型（LDM）方法中三维解码器能力不足的根本瓶颈。

**与 LDM-based 三维生成方法的对比。** 现有基于 LDM 的文本到三维生成方法（如 **Matrix3D-omni**、**Director3D**、**Prometheus3D**、**SplatFlow**、**VideoRFSplat**）通常采用“视频VAE编码器 + 从头训练或微调的三维解码器”范式。这些方法面临两个关键问题：其一，解码器需从零开始学习三维重建，在数据有限的情况下难以匹敌专用三维基础模型的能力；其二，生成模型与VAE解码器之间缺乏有效对齐，导致生成质量低、三维一致性差。VIST3A 通过**模型缝合**直接将预训练三维重建网络的部分层作为解码器复用，仅训练一个线性缝合层和少量LoRA参数，从根本上回避了“从头学习三维重建”的困难。在 T3Bench 上，VIST3A: Wan+MVDUSt3R 的 Imaging Quality 达 58.83，显著优于 Director3D 的 54.32（+4.51）；在 SceneBench 上，VIST3A: Wan+AnySplat 以 64.87 超过 VideoRFSplat 的 58.19（+6.68）；在 DPG-Bench 上，Global 分数 81.82 对比 SplatFlow 的 69.70（+12.12）。这些结果一致表明，缝合策略在多个基准上实现了对现有方法的系统性超越。

**与视频生成模型的继承关系。** VIST3A 的主干生成器采用 **Wan 2.1 T2V large**（Wan et al., 2025），其视频VAE编码器产生的潜向量是缝合的输入源。框架同时验证了与其他视频模型（CogVideoX、SVD、HunyuanVideo）的兼容性——Table 3 显示，将 AnySplat 缝合到任意视频模型上，其新视图合成性能始终优于单独使用 AnySplat，说明缝合策略具有跨架构的泛化性。

**与三维重建基础模型的继承关系。** 缝合的目标三维模型包括 **MVDUSt3R**、**VGGT** 和 **AnySplat** 等前馈式三维重建网络。VIST3A 并非替代这些模型，而是将其尾段作为解码器嵌入生成管线。Table 5 表明，缝合后的点云重建质量和相机姿态精度与原始三维模型几乎持平，说明缝合过程保留了三维基础模型的核心能力。

### 2. 适用边界

**输入格式约束。** 缝合模型的编码器继承自视频生成模型，要求输入图像排列为连续、时序连贯的视频序列。框架目前仅验证了视频格式的多视图输入，对无序多视图图像或三维扫描数据的支持未经验证，在这些场景下性能可能出现下降。

**缝合层选择的跨架构局限。** 缝合层的选择依赖于线性最小二乘拟合（Eq. 2），MSE 较低的层通常对应更好的三维重建质量（Figure 5），但绝对 MSE 值不能跨VAE架构预测性能。Figure 10 显示，尽管 CogVideoX 和 Hunyuan + AnySplat 的绝对 MSE 最低（0.008），SVD + AnySplat 却取得了最佳 PSNR（21.48）。这意味着每个 VAE-三维模型对需要独立进行缝合层搜索，无法通过统一的 MSE 阈值进行跨架构选择。

**长序列生成的稳定性。** Figure 16 展示了通过扩展生成帧数来构建大规模场景的能力，但框架在极限帧数下的生成质量和一致性是否持续保持稳定，仍缺乏系统性验证。

### 3. 局限与开放问题

**已验证的局限。**

1. **无序多视图支持缺失**：当前缝合流程假设输入为时序视频序列，对无序多视图图像或三维扫描数据的直接适配能力未经检验。
2. **缝合层选择标准的单一性**：仅依赖线性最小二乘 MSE 作为层选择标准，虽在单一 VAE-三维模型对内有效，但无法跨架构预测性能，需要逐对搜索。
3. **生成模型能力的继承限制**：VIST3A 的生成质量上限受限于所使用的视频生成模型。Table 7 显示微调后的生成模型在 VBench 上的视频生成性能与原始模型相比有所变化，表明对齐过程可能影响生成模型的通用视频生成能力。

**开放问题。**

1. **缝合层选择标准的改进空间**：是否应超越 MSE，引入考虑下游任务表现或非线性对应关系的选择标准？CKA 可视化（Figure 6）虽能反映整体退化程度，但不如 MSE 精确，是否存在更优的组合指标？
2. **无序数据扩展**：框架能否通过修改编码器或引入重排序机制，扩展到无序多视图数据集或三维扫描数据？这是走向通用三维生成的重要一步。
3. **长序列场景的极限**：随着帧数增加，生成质量和三维一致性是否保持稳定？当前仅在有限帧数下验证了场景扩展能力（Figure 16），极限边界尚不明确。
4. **缝合策略的理论完备性**：虽然 Insulla et al. (2025) 的定理表明缝合风险由缝合层 MSE 上界约束，但该理论假设的 Lipschitz 条件在深层三维模型中是否始终成立，仍需进一步验证。



## 原文 PDF

![[paperPDFs/ICLR_2026/Text_to_3D_by_Stitching_a_Multi_view_Reconstruction_Network_to_a_Video_Generator.pdf]]
