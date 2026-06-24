---
title: "EVLF: Early Vision-Language Fusion for Generative Dataset Distillation"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/EVLF_Early_Vision_Language_Fusion_for_Generative_Dataset_Distillation.pdf
project_link: null
code_link: "https://github.com/wenqi-cai297/earlyfusion-for-dd/"
aliases:
- EEVLF
- EVLF
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/generative_models_diffusion
- topic/benchmarks_datasets_evaluation
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: 语义信息注入的时机与位置：在扩散过程之前（早期融合）还是期间（晚期融合）。
primary_logic: 在扩散过程开始之前，将文本语义通过轻量级交叉注意力融入编码器输出的视觉潜在空间，使语义与视觉线索在后续去噪中共同演化，从而抑制文本主导效应，提升合成样本的语义准确性与视觉连贯性。
claims:
- EVLF 在 CIFAR-10 (IPC=10) 上较 D4M 准确率提升 8.1%，验证了早期融合有效缓解晚期融合的过度校正问题。
- t-SNE 可视化显示，EVLF 合成样本在真实数据流形上覆盖区域更广，证明其改善了合成数据的多样性和分布对齐。
- 消融实验表明，交叉注意力模块与去噪器微调的组合带来最高性能，且开启文本注入（λ₁>0）能显著提升准确率和样本覆盖率。
- ImageWoof (IPC=10, ResNetAP-10) 上 Accuracy (%) = 39.3
---

# EVLF: Early Vision-Language Fusion for Generative Dataset Distillation

> [!tip] 核心洞察
> 在扩散过程开始之前，将文本语义通过轻量级交叉注意力融入编码器输出的视觉潜在空间，使语义与视觉线索在后续去噪中共同演化，从而抑制文本主导效应，提升合成样本的语义准确性与视觉连贯性。

| 字段 | 内容 |
|------|------|
| 中文题名 | EVLF：面向生成式数据集蒸馏的早期视觉-语言融合方法 |
| 英文题名 | EVLF: Early Vision-Language Fusion for Generative Dataset Distillation |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2603.07476) · [Code](https://github.com/wenqi-cai297/earlyfusion-for-dd/) |
| Topic | #topic/vision_multimodal_applications #topic/generative_models_diffusion #topic/benchmarks_datasets_evaluation #topic/vision_multimodal_applications/image_and_video_generation |
| Method | EVLF (Early Vision-Language Fusion) |
| Dataset | ImageWoof, ImageNette, ImageIDC, CIFAR-10 |

> [!tip] 效果简介
> - ImageWoof (IPC=10, ResNetAP-10) 上，Accuracy (%) 39.3 vs 36.6 (D4M) (+2.7%)。
> - ImageNette (平均) 上，Accuracy (%) N/A vs D4M (+4.9% 平均提升)。
> - ImageIDC (IPC=10) 上，Accuracy (%) N/A vs D4M (+9.6%)。

## 概述

生成式数据集蒸馏旨在将大规模真实数据集压缩为极少量的合成样本，使下游模型在这些合成样本上训练后仍能保持竞争力。扩散模型因其强大的生成能力，近年来成为该领域的主流骨干。然而，现有扩散式蒸馏方法普遍采用**晚期融合（late fusion）**策略，即在去噪过程中通过去噪器内部的交叉注意力层注入文本语义。这种做法导致文本提示主导生成过程，削弱了编码器视觉潜在特征的作用，引发**过度校正（over-correction）**：合成样本过度拟合标签语义，却丢失了类内结构细节与视觉多样性。

本文提出 **EVLF（Early Vision-Language Fusion）**，一种面向生成式数据集蒸馏的早期视觉-语言融合方法。其核心思想是**将语义信息注入的时机从去噪阶段前移至编码器与扩散骨干之间的接口**：在扩散过程开始之前，通过一个轻量级交叉注意力模块，将文本语义融入视觉潜在空间，使语义线索与视觉特征在后续去噪中共同演化。这一设计有效抑制了文本主导效应，在保持类别语义准确性的同时，显著提升了合成样本的视觉保真度与分布多样性。

EVLF 具有即插即用的特性，不修改训练调度、损失函数或去噪器架构，可无缝集成到任何基于编码器-扩散骨干的蒸馏流程中。在 CIFAR-10/100、ImageNet-1K 及其多个子集上的实验表明，EVLF 在多种 IPC 设置和测试架构下均取得一致且显著的性能提升：在 CIFAR-10（IPC=10）上较 **D4M**（Su et al., CVPR 2024）准确率提升 **8.1%**，在 ImageWoof 上提升 **2.7%**，在 ImageIDC 上提升 **9.6%**，在 ImageNet-1K（IPC=50, ResNet-18）上达到 **61.9%**。t-SNE 可视化进一步证实，EVLF 合成样本在真实数据流形上覆盖区域更广，改善了合成数据的多样性与分布对齐。

## 背景与动机

### 数据集蒸馏的核心挑战

数据集蒸馏（Dataset Distillation, DD）旨在将大规模真实数据集压缩为极少量合成样本，同时保持下游模型训练效果。其核心目标可形式化为：

$$
\min_{S} \mathbb{E}_{(x,y)\sim T}[\ell(x,y;\theta_S^*)] \quad \text{where } \theta_S^* = \operatorname{Alg}(S,\theta_0)
$$

其中合成数据集 $S$ 训练出的模型参数 $\theta_S^*$ 需在真实数据集 $T$ 上达到低损失。这一目标的实现面临双重约束：合成样本既要保留类别判别语义，又要维持足够的视觉保真度与结构细节。

### 扩散式数据集蒸馏的瓶颈：晚期融合与语义过度校正

近年来，基于扩散模型的数据集蒸馏方法（如 **D4M**（Su et al., CVPR 2024）、**MGD³**（Chan-Santiago et al., arXiv 2025）、**MinimaxDiffusion**（Gu et al., CVPR 2024））展现出强大的生成能力。然而，这些方法普遍采用**晚期融合**策略：文本语义（通常来自 CLIP 等文本编码器）在扩散去噪过程中才被注入，通过去噪器内部的交叉注意力层与视觉潜在表示交互（见 Figure 1(a)）。

晚期融合带来一个关键瓶颈——**语义过度校正**。由于文本提示在去噪阶段直接引导生成过程，语义信号容易主导视觉潜在表示，削弱编码器提取的原始视觉特征的作用。其后果是：合成样本过度拟合标签语义，丧失结构细节和纹理丰富性，导致视觉保真度下降。如 Figure 1(c)(d) 所示，晚期融合生成的样本虽语义正确，但结构模糊、纹理贫乏，与真实数据分布存在明显偏差。

### 本文动机：从晚期融合到早期融合

针对上述瓶颈，本文提出一个根本性的调控变量：**语义信息注入的时机与位置**。核心洞察在于：若将文本语义在扩散过程开始之前融入视觉潜在空间，使语义线索与视觉特征在后续去噪中**共同演化**，则可抑制文本主导效应，同时提升合成样本的语义准确性与视觉连贯性。

基于此洞察，本文提出 **EVLF（Early Vision-Language Fusion）**——一种即插即用的早期视觉-语言融合方法。EVLF 在 VAE 编码器与扩散去噪骨干网络之间的接口处引入轻量级交叉注意力模块，在扩散过程之前完成语义对齐（见 Figure 1(b) 和 Figure 2）。该方法无需修改训练调度、损失函数或去噪器架构，可无缝集成至任何基于扩散的 DD 流程中。

## 核心创新

### 瓶颈发现：晚期融合中的文本主导与过度校正

现有扩散式数据集蒸馏方法（如 **D4M** (Su et al., CVPR 2024)、**MGD³** (Chan-Santiago et al., arXiv 2025)）普遍采用**晚期融合**策略，即在去噪过程中通过去噪器内部的交叉注意力层注入文本语义。这一设计导致文本提示在生成过程中占据主导地位，削弱了编码器提取的视觉潜在特征的作用，引发**过度校正**问题——合成样本过度拟合标签语义，丧失结构细节和视觉保真度（Figure 1a）。

### 因果调控变量：语义注入的时机与位置

EVLF 的核心创新在于将语义信息注入的时机从“扩散过程期间”前移至“扩散过程之前”，即在编码器与生成骨干网络之间完成视觉-语言融合。这一**早期融合**策略使语义线索与视觉特征在后续去噪过程中共同演化，从根本上抑制了文本主导效应（Figure 1b）。

### 关键改进槽位（Changed Slots）

| 改进槽位 | 基线方案（晚期融合） | EVLF 方案（早期融合） |
|----------|---------------------|----------------------|
| **语义注入点** | 去噪过程中，通过去噪器内部交叉注意力注入 | 编码器与扩散骨干之间，扩散过程开始前注入 |
| **融合模块** | 无额外模块，依赖去噪器自带交叉注意力层 | 轻量级交叉注意力模块（图像 token 为查询、文本 token 为键值，含残差连接与层归一化） |
| **融合训练目标** | 隐式/无专门训练，仅依赖去噪器的生成目标 | 双损失训练：MSE（视觉保真度）+ InfoNCE（类别语义对齐） |

### 融合机制设计

EVLF 在 VAE 编码器输出的视觉潜在表示 $z_{\mathrm{img}}$ 与文本编码器（如 CLIP）生成的文本嵌入 $e_{\mathrm{text}}$ 之间引入一个轻量级交叉注意力模块：

1. **投影对齐**：将视觉潜在和文本嵌入分别投影到共享特征维度 $d$：
   $$\tilde{z} = \phi_{\mathrm{img}}(z_{\mathrm{img}})\in\mathbb{R}^{N\times d}, \quad \tilde{e} = \phi_{\mathrm{text}}(e_{\mathrm{text}})\in\mathbb{R}^{L\times d}$$

2. **交叉注意力融合**：以图像 token 为查询、文本 token 为键值进行缩放点积注意力：
   $$\mathrm{Attn}(\tilde{z},\tilde{e}) = \mathrm{softmax}\left(\frac{QK^{\top}}{\sqrt{d}}\right)V, \quad Q=\tilde{z}W_Q, K=\tilde{e}W_K, V=\tilde{e}W_V$$

3. **残差路径与恢复**：通过残差连接和层归一化保留原始视觉信息，再恢复空间维度：
   $$u = \mathbf{LN}(\tilde{z} + \mathrm{Attn}(\tilde{z},\tilde{e})), \quad z_{\mathrm{fused}} = \psi(u) \in \mathbb{R}^{H\times W\times C}$$

### 双损失训练策略

交叉注意力模块通过两项损失联合优化：

- **$\mathcal{L}_{\mathrm{MSE}} = \|z_{\mathrm{fused}} - z_{\mathrm{img}}\|_2^2$**：约束融合后潜在表示尽可能接近原始图像潜在表示，保持视觉保真度。
- **$\mathcal{L}_{\mathrm{InfoNCE}}$**：基于类别标签的对比损失，使融合潜在与同类文本嵌入对齐，强化语义一致性。

总损失为 $\mathcal{L}_{\mathrm{CA}} = \lambda_1 \mathcal{L}_{\mathrm{InfoNCE}} + \lambda_2 \mathcal{L}_{\mathrm{MSE}}$，其中 $\lambda_1=0.1$ 固定，$\lambda_2$ 在前 2 个训练 epoch 从 0.05 线性增至 1.0。

### 即插即用特性

EVLF 作为一个模块化组件，无需修改现有扩散式蒸馏管线的训练调度、损失函数或去噪器架构，可直接嵌入任何含编码器的扩散式数据集蒸馏框架（如 D4M、MGD³）。消融实验（Table 7）证实，交叉注意力模块与去噪器微调的组合带来最高性能增益，单独使用任一组件均不及组合效果。

## 整体框架

EVLF 的 pipeline 遵循“编码—融合—生成”三阶段范式，其核心设计在于将语义注入点从去噪过程内部前移至编码器与生成骨干网络之间的接口处。

**输入流与编码阶段。** 给定一批真实图像及其类别标签，系统首先通过两个独立的编码器提取异构表示：
- **视觉编码器**（预训练 VAE 编码器）将图像压缩到潜在空间，输出视觉潜在特征 $z_{\mathrm{img}}$；
- **文本编码器**（如 CLIP 文本塔）根据类别标签生成文本嵌入 $e_{\mathrm{text}}$。

**早期融合阶段。** 在扩散过程启动之前，一个轻量级交叉注意力模块 $\mathbf{CA}$ 以 $z_{\mathrm{img}}$ 为查询、$e_{\mathrm{text}}$ 为键值执行融合，输出语义增强的潜在表示 $z_{\mathrm{fused}} = \mathbf{CA}(z_{\mathrm{img}}, e_{\mathrm{text}})$。该模块通过残差连接和层归一化保持视觉结构的稳定性，并采用双损失训练：
- $\mathcal{L}_{\mathrm{MSE}} = \|z_{\mathrm{fused}} - z_{\mathrm{img}}\|_2^2$ 约束融合潜在不偏离原始视觉特征；
- $\mathcal{L}_{\mathrm{InfoNCE}}$ 基于类别标签的对比损失对齐融合潜在与同类文本嵌入。

总损失为 $\mathcal{L}_{\mathrm{CA}} = \lambda_1 \mathcal{L}_{\mathrm{InfoNCE}} + \lambda_2 \mathcal{L}_{\mathrm{MSE}}$，其中 $\lambda_1$ 控制语义注入强度，$\lambda_2$ 控制视觉保真度。

**生成与蒸馏阶段。** 融合后的 $z_{\mathrm{fused}}$ 作为条件输入扩散去噪器（UNet 或 DiT）。去噪器可选择性在 $z_{\mathrm{fused}}$ 上以标准扩散目标微调，以适配目标数据分布。随后，对融合嵌入进行聚类，并通过 VAE 解码器生成最终合成图像，构成蒸馏数据集。

**关键设计特性。** 与晚期融合方法（如 **D4M**，Su et al., CVPR 2024）在去噪过程中通过去噪器内部交叉注意力注入文本语义不同，EVLF 的早期融合使语义线索与视觉特征在后续去噪过程中共同演化，从机制上抑制了文本信号对视觉潜在表示的主导效应。该方法即插即用，无需修改训练调度、损失函数或去噪器架构，可集成至任何具备编码器的扩散式数据集蒸馏管线。

> **需要人工核实：** 文中未提供交叉注意力模块的具体参数规模与计算开销对比数据，若需评估实际部署成本，建议查阅源代码或联系作者获取详细配置。

### 补充图表

![[assets/figures/papers/paper_list_l2190_https_arxiv_org_abs_2603_07476/figures/002_Figure_2.jpg]]
*Figure 2: Overview of EVLF. Visual latents from a VAE and text embeddings from a text encoder are fused via cross-attention at the encoder-backbone interface. The fused embeddings are trained with*

## 核心模块与公式推导

### 瓶颈定位：语义注入的时机决定视觉-语义平衡

扩散式数据集蒸馏方法（如 **D4M** (Su et al., CVPR 2024)、**MGD³** (Chan-Santiago et al., arXiv 2025)）通常采用**晚期融合**策略：在去噪过程中通过去噪器内部的交叉注意力层注入文本语义。这种设计导致文本提示主导生成过程，削弱编码器输出的视觉潜在特征的作用，引发**过度校正**——合成样本过度拟合标签语义而丢失结构细节与纹理多样性（见 Figure 1）。

![[assets/figures/papers/paper_list_l2190_https_arxiv_org_abs_2603_07476/figures/001_Figure_1.jpg]]
*Figure 1: Comparison between traditional late-fusion approaches and the proposed EVLF. (a) Late-fusion methods inject textual prompts during the denoising process, causing semantic signals to dominate visual latent representations. (b) EVLF introduces vision-language alignment before diffusion, allowing semantic cues and visual features to co-evolve throughout generation. (c) Synthetic samples on ImageNette (256 × 256). (d) Synthetic samples on CIFAR-10 (32 × 32). Rows display real images, latefusion results, and EVLF results. EVLF produces samples with stronger label fidelity and more coherent visual details*

EVLF 的核心洞察是：**语义信息注入的时机与位置**是调节视觉-语义平衡的关键因果旋钮。将文本语义从“去噪期间”移至“去噪之前”，使语义与视觉线索在扩散过程的每一步中**共同演化**，而非让语义单向压制视觉。

### 模块架构：编码器-骨干接口的早期融合

EVLF 在 VAE 编码器与扩散去噪器（UNet/DiT）之间插入一个**轻量级交叉注意力模块（CA）**，构成“编码器→CA→去噪器”的串行管线（Figure 2）。各模块职责如下：

| 模块 | 功能 | 证据锚点 |
|------|------|----------|
| **VAE 编码器** | 将输入图像压缩到潜在空间，生成视觉潜在特征 $z_{\mathrm{img}} \in \mathbb{R}^{H \times W \times C}$ | Section 4, Figure 2 |
| **文本编码器**（如 CLIP） | 根据类别标签生成文本嵌入 $e_{\mathrm{text}}$ | Section 4, Figure 2 |
| **早期融合交叉注意力模块（CA）** | 以图像 token 为查询、文本 token 为键值，输出语义增强的融合潜在 $z_{\mathrm{fused}}$ | Section 4.1 |
| **扩散去噪器** | 以 $z_{\mathrm{fused}}$ 和 $e_{\mathrm{text}}$ 为条件，通过迭代去噪生成最终潜在表示；可选择性微调 | Section 4.3 |
| **聚类与解码** | 对融合嵌入聚类，VAE 解码器生成最终合成图像 | Figure 2 caption |

### 交叉注意力融合的数学推导

**步骤一：特征投影。** 将视觉潜在和文本嵌入投影到共享维度 $d$：

$$\tilde{z} = \phi_{\mathrm{img}}(z_{\mathrm{img}}) \in \mathbb{R}^{N \times d}, \quad \tilde{e} = \phi_{\mathrm{text}}(e_{\mathrm{text}}) \in \mathbb{R}^{L \times d} \tag{5-6}$$

其中 $N=H \times W$ 为图像 token 数，$L$ 为文本 token 数。

**步骤二：缩放点积注意力。** 以图像 token 为查询（Q），文本 token 为键（K）和值（V）：

$$\mathrm{Attn}(\tilde{z}, \tilde{e}) = \mathrm{softmax}\left(\frac{QK^{\top}}{\sqrt{d}}\right)V, \quad Q=\tilde{z}W_Q,\; K=\tilde{e}W_K,\; V=\tilde{e}W_V \tag{7}$$

**步骤三：残差连接与层归一化。** 保留原始视觉信息，避免语义完全覆盖视觉特征：

$$u = \mathbf{LN}(\tilde{z} + \mathrm{Attn}(\tilde{z}, \tilde{e})) \tag{8}$$

**步骤四：空间恢复。** 将融合后的 token 序列恢复为空间特征图：

$$z_{\mathrm{fused}} = \psi(u) \in \mathbb{R}^{H \times W \times C}$$

### 双损失训练目标

交叉注意力模块通过两个互补的损失函数联合训练，平衡**视觉保真度**与**语义对齐**：

**MSE 损失（视觉保真度）：** 约束融合潜在尽可能接近原始图像潜在，防止语义注入破坏视觉结构。

$$\mathcal{L}_{\mathrm{MSE}} = \|z_{\mathrm{fused}} - z_{\mathrm{img}}\|_2^2 \tag{9}$$

**InfoNCE 损失（语义对齐）：** 基于类别标签的对比损失，使融合潜在与同类文本嵌入对齐，与异类文本嵌入分离。其中 $s^{ij}$ 为融合潜在与文本嵌入的余弦相似度，$M^{ij}$ 为同类掩码（同类为 1，异类为 0）。

$$\mathcal{L}_{\mathrm{InfoNCE}} = \frac{1}{B}\sum_{i=1}^{B}\left(-\log\frac{\sum_j M^{ij}\exp(s^{ij})}{\sum_j \exp(s^{ij})}\right) \tag{11}$$

**总损失：** 加权组合，$\lambda_1$ 控制语义对齐强度，$\lambda_2$ 控制视觉保真度。实验中固定 $\lambda_1=0.1$，$\lambda_2$ 在前 2 个 epoch 从 0.05 线性增至 1.0。

$$\mathcal{L}_{\mathrm{CA}} = \lambda_1 \mathcal{L}_{\mathrm{InfoNCE}} + \lambda_2 \mathcal{L}_{\mathrm{MSE}} \tag{12}$$

### 去噪器微调

交叉注意力模块训练完成后，可选择性对去噪器进行微调，使用标准扩散去噪目标，但以融合潜在 $z_{\mathrm{fused}}$ 替代原始潜在：

$$\mathcal{L}_{\mathrm{DM}} = \mathbb{E}_{z_{\mathrm{fused}},\epsilon,t}\left[\|\epsilon_{\theta}(z_t, t, e_{\mathrm{text}}) - \epsilon\|_2^2\right] \tag{13}$$

消融实验（Table 7）证实：**交叉注意力模块与去噪器微调的组合**带来最高性能，二者单独使用均不及组合。这验证了 EVLF 的早期融合需要与生成骨干协同适配才能充分释放其潜力。

![[assets/figures/papers/paper_list_l2190_https_arxiv_org_abs_2603_07476/figures/008_Table_7.jpg]]
*Table 7: Ablation on the contributions of denoiser fine-tuning (FT.) and the CrossAttention module (CA.) within the*

### 设计优势总结

EVLF 的模块化设计具备**即插即用**特性：无需修改去噪器架构、训练调度或损失函数，可直接接入任何带有编码器的扩散式数据集蒸馏管线。其核心机制——在扩散过程之前完成视觉-语义对齐——从根本上改变了语义信号与视觉特征的作用关系，使二者从“对抗”转为“协同”，从而缓解晚期融合的过度校正瓶颈。

## 实验与分析

### 核心瓶颈与因果机制

扩散式数据集蒸馏方法普遍在去噪阶段（晚期融合）通过去噪器内部的交叉注意力层注入文本语义。这一设计导致文本提示主导生成过程，削弱编码器视觉潜在特征的作用，引发**过度校正**——合成样本过度拟合标签语义而丢失结构细节与类内多样性。EVLF 将语义注入点前移至编码器与扩散骨干之间（早期融合），使语义与视觉线索在后续去噪中共同演化，从而抑制文本主导效应。

### 主实验结果

#### ImageWoof 基准（Table 1）

![[assets/figures/papers/paper_list_l2190_https_arxiv_org_abs_2603_07476/figures/003_Table_1.jpg]]
*Table 1: Dataset distillation results on ImageWoof across different IPC settings and test models. The best results in each row are in bold, and the second-best are underlined*

在 ImageWoof 上，EVLF 以即插即用方式集成到 D4M 和 MGD³ 两种扩散式基线中，在所有 IPC 设置和测试架构下均取得一致提升。以 IPC=10、ResNetAP-10 为例，EVLF 达到 39.3%，较 D4M 基线（36.6%）提升 2.7 个百分点。MGD³+EVLF 组合在多数设置下取得最优结果，例如 IPC=20、ResNetAP-10 达到 45.1±0.9%，IPC=100、ResNetAP-10 达到 68.1±0.9%。

#### ImageNette 与 ImageIDC 基准（Table 2）

![[assets/figures/papers/paper_list_l2190_https_arxiv_org_abs_2603_07476/figures/004_Table_2.jpg]]
*Table 2: Comparison of SOTA methods under various IPC settings on ImageNette and ImageIDC. All results are on ResNetAP-10. Best in bold, second best underlined*

在 ImageNette 上，EVLF 较 D4M 平均提升 4.9%；在 ImageIDC 上提升更为显著，IPC=10 时准确率提升达 9.6%。这些一致增益证实早期融合有效缓解了晚期融合的过度校正问题，生成的合成数据在语义忠实度和结构连贯性上均优于基线。

#### CIFAR-10/100 与 Tiny-ImageNet（Table 3、Table 4）

![[assets/figures/papers/paper_list_l2190_https_arxiv_org_abs_2603_07476/figures/005_Table_4.jpg]]
*Table 4: Performance comparison on Tiny-ImageNet*

在 CIFAR-10（IPC=10）上，EVLF 较 D4M 准确率提升 8.1%。在 Tiny-ImageNet 上，EVLF 同样展现出持续的性能优势，验证了方法在不同数据规模和分辨率下的鲁棒性。

#### ImageNet-1K 全量基准（Table 5）

![[assets/figures/papers/paper_list_l2190_https_arxiv_org_abs_2603_07476/figures/006_Table_5.jpg]]
*Table 5: Performance comparison on ImageNet-1K*

在 ImageNet-1K（IPC=50，ResNet-18）上，EVLF 达到 61.9±0.1%，较 MGD³ 等基线持续提升。这证明早期融合策略可扩展至大规模、高分辨率场景。

#### 迁移学习性能（Table 6）

![[assets/figures/papers/paper_list_l2190_https_arxiv_org_abs_2603_07476/figures/007_Table_6.jpg]]
*Table 6: Transfer learning results on target datasets using models pretrained on the distilled ImageNet-1K dataset*

使用 EVLF 蒸馏的 ImageNet-1K 合成数据集预训练模型，在下游目标数据集上的迁移学习性能同样优于基线蒸馏方法，表明合成数据保留了可迁移的判别特征。

### 消融实验

#### 去噪器微调与交叉注意力模块的贡献（Table 7）

消融实验在 D4M 流水线上分别评估去噪器微调（FT.）和交叉注意力模块（CA.）的独立与组合效果。结果表明，**FT.+CA. 组合**取得最佳准确率（IPC=10 达 57.3%），二者单独使用均不及组合。这证实语义注入模块与去噪器对目标分布的适配之间存在协同效应。

#### 语义对齐损失权重 λ₁ 的影响（Figure 4）

![[assets/figures/papers/paper_list_l2190_https_arxiv_org_abs_2603_07476/figures/011_Figure_4.jpg]]
*Figure 4: Parameter Analysis of λ1 on ImageIDC*

调节 λ₁（InfoNCE 权重）的实验显示：λ₁ > 0 时准确率与样本覆盖率均显著提升；λ₁ = 0（关闭文本注入）时，生成结果出现过度校正，多样性降低。这直接验证了语义对齐训练对抑制文本主导效应的必要性。

#### 早期融合与晚期融合的视觉质量对比（Figure 5）

![[assets/figures/papers/paper_list_l2190_https_arxiv_org_abs_2603_07476/figures/010_Figure_5.jpg]]
*Figure 5: Visualization of synthesized images generated by*

在 CIFAR-10 和 ImageNet-1K 上的生成样本可视化表明，EVLF 相比 D4M 产生更清晰的结构、更丰富的纹理和更大的类内差异，且在不同分辨率（32×32 与 256×256）下均保持一致的视觉质量优势。

### 多样性与分布对齐分析（Figure 3）

![[assets/figures/papers/paper_list_l2190_https_arxiv_org_abs_2603_07476/figures/009_Figure_3.jpg]]
*Figure 3: t-SNE visualization of synthetic and real samples on four ImageNet-1K classes. D4M [32] and MGD3 [5] produce synthetic samples that occupy limited regions of the real-data manifold. With EVLF, the synthesized samples cover a broader and more varied region, indicating improved diversity and distributional alignment*

t-SNE 可视化显示，D4M 和 MGD³ 的合成样本在真实数据流形上仅占据有限区域，而 EVLF 合成样本覆盖更广、更多样的区域，证明早期融合改善了合成数据的多样性和分布对齐。

### 失败模式与局限性

当前 EVLF 仅支持类别级别的条件，无法处理实例级或多标签场景。在需要细粒度实例区分或组合式提示的任务中，早期融合模块的语义注入粒度不足，可能限制合成样本的多样性和可控性。此外，所有实验均在单张 NVIDIA A5000 GPU 上完成，大规模分布式训练场景下的可扩展性尚待验证。

### 公平性说明

所有实验使用统一评估协议，报告多次运行的均值和标准差。比较涵盖多种数据集（CIFAR-10/100、ImageNet-1K 及其子集、Tiny-ImageNet）、不同 IPC 设置（1–100）和不同测试架构（ConvNet-6、ResNetAP-10、ResNet-18），以验证方法的广泛适用性。

## 方法谱系与知识库定位

### 扩散式数据集蒸馏中的语义注入范式

数据集蒸馏（Dataset Distillation）的核心目标是合成一个极小规模的代理数据集 $S$，使得在其上训练的模型能够逼近在完整真实数据集 $T$ 上的性能。其数学形式为：

$$
\min_{S} \mathbb{E}_{(x,y)\sim T}[\ell(x,y;\theta_S^*)] \quad \text{where } \theta_S^* = \operatorname{Alg}(S,\theta_0)
$$

近年来，扩散模型因其强大的生成先验被引入数据集蒸馏，形成了扩散式 DD（Diffusion-based DD）这一新兴范式。在该范式中，语义信息（通常为类别标签的文本嵌入）的注入时机成为影响合成质量的关键瓶颈。现有方法普遍采用**晚期融合（Late Fusion）**策略：文本语义在去噪过程中通过去噪器内部的交叉注意力层注入，如 **D4M**（Su et al., CVPR 2024）和 **MGD³**（Chan-Santiago et al., arXiv 2025）。这一设计导致文本提示主导生成过程，削弱编码器视觉潜在特征的作用，引发**过度校正（Overcorrection）**——合成样本过度拟合标签语义而丢失结构细节与类内多样性。

EVLF 通过将语义注入点从“去噪过程中”前移至“编码器与扩散骨干之间”，实现了**早期视觉-语言融合（Early Vision-Language Fusion）**。这一范式转换使语义线索与视觉特征在后续去噪中共同演化，而非让语义单方面支配生成。从知识库定位来看，EVLF 并非重新设计扩散骨干或蒸馏优化目标，而是在编码器-骨干接口处插入一个可插拔的融合模块，属于**架构层面的语义注入策略改进**。

### 与基线方法的关系

**D4M**（Su et al., CVPR 2024）是扩散式 DD 的代表性基线，基于解耦扩散模型，在去噪阶段通过标准交叉注意力注入文本条件。EVLF 直接在其 pipeline 上验证了早期融合的有效性：在 CIFAR-10（IPC=10）上提升 8.1%，在 ImageNette 上平均提升 4.9%，在 ImageIDC 上提升 9.6%（Table 2, Table 3）。这些增益直接归因于语义注入时机的改变，而非更强的生成模型或更复杂的优化策略。

**MGD³**（Chan-Santiago et al., arXiv 2025）在扩散式 DD 中引入多模态引导，但仍采用晚期融合范式。EVLF 在其上的集成同样带来持续提升（Table 1, Table 5），表明早期融合对不同扩散骨干（UNet 或 DiT）具有通用性。

**MinimaxDiffusion**（Gu et al., CVPR 2024）通过最小最大优化改进扩散式 DD 的训练目标。EVLF 的贡献与其正交：前者优化“如何训练”，后者优化“在何处注入语义”。两者可在同一 pipeline 中组合，但论文未提供直接组合实验，需手动验证。

在非扩散 DD 方法中，**SRe2L**（Yin et al., NeurIPS 2023）基于特征压缩与恢复，**DM**（Zhao and Bilen, WACV 2023）基于分布匹配。这些方法不依赖扩散先验，因此 EVLF 的早期融合策略不直接适用。但 EVLF 揭示的“语义注入时机影响生成多样性”这一洞察，可能启发非扩散方法重新审视其语义对齐机制。

### 适用边界与局限

EVLF 的适用边界由以下三个维度界定：

1. **生成范式**：仅适用于基于扩散模型的数据集蒸馏 pipeline，且要求 pipeline 具备显式的编码器-骨干接口（如 VAE 编码器 + UNet/DiT 去噪器）。对于非扩散方法（如 SRe2L、DM）或端到端生成方法，早期融合模块无法直接插入。

2. **条件粒度**：当前方法仅支持**类别级别的条件**（class-level conditioning），即文本嵌入由类别标签通过 CLIP 等文本编码器生成。无法处理实例级条件（如特定实例的图像描述）或多标签场景。论文明确将此列为局限。

3. **计算开销**：交叉注意力模块的训练引入双损失优化（MSE + InfoNCE），且可选去噪器微调增加了训练成本。所有实验在单张 NVIDIA A5000 GPU 上完成，但论文未报告与基线的训练时间对比，实际部署效率需手动验证。

### 开放问题

论文提出的开放问题直接指向当前局限的突破方向：**如何将 EVLF 扩展到实例感知和组合式提示**，以实现更细粒度的控制和更高的样本多样性。从知识库视角看，这一问题连接了三个活跃研究方向：

- **实例级数据集蒸馏**：现有方法（包括 EVLF）在每类合成固定数量样本时，难以保证样本覆盖类内不同模式。引入实例级文本描述可能使合成样本更精准地锚定真实分布的子区域。
- **组合式生成**：将类别标签分解为属性组合（如“棕色狗” vs. “白色狗”），通过组合式提示控制合成样本的属性分布，有望在不增加 IPC 的前提下提升数据多样性。
- **多模态对齐的理论理解**：EVLF 的 InfoNCE 损失在融合潜在空间中强制视觉-文本对齐，但该对齐的泛化边界及其与下游分类性能的因果关系尚未被形式化分析。这一理论缺口是数据集蒸馏领域的共性挑战。

## 原文 PDF

![[paperPDFs/CVPR_2026/EVLF_Early_Vision_Language_Fusion_for_Generative_Dataset_Distillation.pdf]]
