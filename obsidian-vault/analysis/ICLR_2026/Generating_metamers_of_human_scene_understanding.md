---
title: "Generating metamers of human scene understanding"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/Generating_metamers_of_human_scene_understanding.pdf
project_link: https://rainarit.github.io/metamergen/
code_link: null
openreview_forum_id: cSDXx8V6K9
aliases:
- GMHSU
tags:
- ICLR_2026
- topic/representation_self_supervised_transfer
- topic/representation_self_supervised_transfer/transfer_multitask_and_meta_learning
core_operator: "双流DINOv2特征适配器（中央凹掩码token和周边全token）通过加法交叉注意力集成到Stable Diffusion，使模型能根据注视数量和位置调节生成图像的语义与细节，从而匹配人类内部场景表征。"
primary_logic: "场景同质异构体（metamer）的产生主要由高级语义特征相似性（DreamSim）决定，而非像素级相似性；基于观察者自身注视生成的图像比随机注视生成的在语义上更对齐，且中央凹与周边信息共同贡献。"
claims:
- "DreamSim距离是预测metamer判断最重要的因素（ΔR²=0.10），且像素级相似性（PSNR）无法预测。"
- "基于自身注视生成的场景，其高级语义特征相似性（DreamSim, CLIP）与metamer率正相关，而随机注视则不存在此关系。"
- "同时使用中央凹和周边信息生成的场景具有最高metamer率（54.5%），而仅中央凹信息的场景metamer率极低（8.4%），表明双流信息融合的必要性。"
- "在神经对齐特征分析中，各级特征相似性均与metamer判断正相关，表明metamer需要整个视觉层次的对齐。"
---

# Generating metamers of human scene understanding

> [!tip] 核心洞察
> 场景同质异构体（metamer）的产生主要由高级语义特征相似性（DreamSim）决定，而非像素级相似性；基于观察者自身注视生成的图像比随机注视生成的在语义上更对齐，且中央凹与周边信息共同贡献。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 生成人类场景理解的同质异构体 |
| 英文题名 | Generating metamers of human scene understanding |
| 会议/期刊 | ICLR 2026 (Oral) |
| Links | [paper](https://openreview.net/forum?id=cSDXx8V6K9) · [Project](https://rainarit.github.io/metamergen/) |
| Topic | #topic/representation_self_supervised_transfer #topic/representation_self_supervised_transfer/transfer_multitask_and_meta_learning |
| Method | MetamerGen |
| Dataset | COCO-10k-test, Visual Genome Same-Different Task (300 images, 45 participants) |

> [!tip] 效果简介
> - COCO-10k-test 上，FID 为 MetamerGen (0.25× blur, 1 fixation)，对比 Stable Diffusion 1.5 text-to-image，变化 lower (better)。
> - Visual Genome Same-Different Task (300 images, 45 participants) 上，Metamer Rate (proportion 'same') 为 29.4% (own fixations)，对比 27.7% (random fixations)，变化 +1.7% (p=0.24, not significant)。

## 概要

人类在观看自然场景时，通过一系列注视点（fixations）逐步构建对场景的内部表征——中央凹区域捕获高分辨率细节，而周边视觉则提供低分辨率的场景gist信息。然而，现有场景理解模型无法同时结合这两种信息流，生成与人类动态注视行为对齐的复杂场景假设，更缺乏行为范式来验证这些生成场景的知觉等价性。

本文提出 **MetamerGen**，一个基于潜在扩散模型的场景同质异构体（metamer）生成框架。其核心操作变量是**双流DINOv2特征适配器**：从原始图像提取的patch token经注视掩码保留中央凹信息，从降采样模糊图像提取的全体token编码周边信息，二者分别通过Perceiver重采样器压缩后，以加法交叉注意力机制集成到冻结的Stable Diffusion 1.5（Rombach et al., CVPR 2022）UNet中。这一设计使模型能够根据注视数量和位置，调节生成图像的语义与细节，从而逼近人类内部场景表征。

核心发现可概括为三条因果链：

1. **语义相似性驱动metamer判断**：DreamSim距离是预测metamer判断的最重要因素（ΔR²=0.10），而像素级相似性（PSNR）无法区分“相同”与“不同”判断（Figure 12）。这表明场景同质异构体的产生主要由高级语义特征相似性决定，而非像素级重建精度。

2. **自身注视的语义对齐优势**：基于观察者自身注视生成的场景，其高级语义特征相似性（DreamSim, CLIP）与metamer率正相关；而基于随机注视生成的场景则不存在此关系（Figure 5）。这证明注视位置携带了与个体内部表征绑定的语义信息。

3. **双流信息融合的必要性**：同时使用中央凹和周边信息的完整模型达到54.5%的metamer率，仅周边信息为45.8%，仅中央凹信息则骤降至8.4%（Figure 13）。这表明周边gist提供场景骨架，中央凹细节在此基础上增强知觉可信度，二者缺一不可。

在方法定位上，MetamerGen属于**条件扩散模型的适配器扩展**，其关键改动在于将单文本条件替换为文本（冻结为空字符串）、中央凹、周边三种条件的加法组合，并通过随机注视掩码和条件丢弃策略进行训练。与直接使用文本到图像生成相比，MetamerGen在仅使用单次中央注视和0.25×模糊的条件下，FID指标即优于基线。

行为实验采用实时同异判断范式：被试自由观看场景至预定注视次数后，模型在5秒内基于注视坐标实时生成图像，随后以200ms短暂呈现，被试判断生成图像与原始图像是否“相同”。总体metamer率约为29%（自身注视）vs 27.7%（随机注视），差异未达统计显著（p=0.24），但多层次特征分析一致表明，自身注视条件下生成图像的特征相似性与metamer判断的相关性更强、更可解释。

**证据强度评估**：双流消融实验和行为-特征关联分析均具有高置信度（≥0.9），但总体metamer率较低（约29%）表明模型对复杂场景内部表征的重建仍不充分；行为实验排除了含人类、文本、时钟等元素的图像，且200ms的短暂呈现可能低估精细细节辨别能力，这些限制了结论的泛化性。

人类视觉系统在浏览复杂自然场景时，并非均匀地处理所有视觉信息。中央凹（fovea）仅覆盖约2°视角，提供高分辨率的细节感知；而周边视野虽然分辨率急剧下降，却持续传递着场景的全局结构和语义gist。这种**中央凹-周边信息的分工与融合**，使得人类能够在有限的注视次数下快速建立对场景的连贯理解——我们感知到的并非像素级的精确副本，而是一种在语义和结构上等价的内部表征。

**核心瓶颈：生成与人类内部表征知觉等价的场景**

现有场景理解模型面临一个根本性缺口：它们无法模拟人类通过动态注视行为构建的内部场景表征。具体而言，这一瓶颈体现在三个层面：

1. **信息融合的缺失**：当前模型要么处理均匀分辨率的完整图像，要么仅关注局部显著区域，缺乏将注视点的高分辨率细节与周边低分辨率gist信息进行动态整合的机制。
2. **生成能力的局限**：即便能够提取注视相关特征，现有方法也无法基于这些不完整的、注视依赖的表征生成新的场景图像——即产生所谓的“同质异构体”（metamer）——这些图像在物理上不同于原始场景，但在人类知觉层面却无法区分。
3. **验证范式的空白**：缺乏严格的行为实验范式来量化评估生成场景是否真正达到了与人类内部表征的知觉等价性。传统的图像质量指标（如PSNR、FID）无法捕捉这种高层次的对齐关系。

**同质异构体的概念渊源**

“同质异构体”概念源于视觉神经科学。在早期视觉研究中，具有相同低层统计特性（如纹理的傅里叶谱）但在像素上完全不同的图像，可以引发无法区分的神经响应。将这一概念提升到复杂自然场景层面，意味着需要寻找那些在**整个视觉层次**（从纹理到语义）上都与原始场景对齐的生成图像——这正是本工作的核心挑战。

**现有方法的缺口**

主流的文本到图像扩散模型（如**Stable Diffusion**，Rombach et al., CVPR 2022）虽然能够生成高质量的自然场景，但其条件信号仅限于文本嵌入，无法接收来自人类注视行为的空间化视觉特征。另一方面，视觉编码器如DINOv2虽然能够提取富含语义和上下文信息的patch token，但如何将这些特征有效地注入生成过程，并模拟中央凹-周边的信息不对称性，仍是一个未解决的问题。CLIP等对比学习编码器虽然擅长全局语义，但其patch token对空间细节和模糊退化的编码能力不足（见Appendix A.10），难以胜任周边信息的精确表征。

**本文动机**

基于上述缺口，本文提出**MetamerGen**——一个双流条件扩散模型，旨在回答一个核心问题：**能否仅凭人类在自由观看场景时产生的注视行为，重建出与观察者内部场景表征知觉等价的图像？** 这一问题的解答不仅关乎对人类视觉理解的逆向工程，也为评估和解释视觉表征模型提供了新的行为学工具。

## 核心方法与创新机理

MetamerGen的核心创新在于将人类动态注视行为中的双流信息——中央凹的高分辨率细节与周边的低分辨率场景gist——首次统一到一个可控的扩散生成框架中，从而生成与人类内部场景表征知觉等价的同质异构体（metamer）。这一设计直接回应了现有模型的关键瓶颈：**无法结合注视与周边信息生成与人类动态注视对齐的复杂场景假设**，并缺乏行为范式来验证生成场景的知觉等价性。

### 双流DINOv2特征适配器：从“文本条件”到“注视条件”的范式转换

相对于仅使用文本嵌入作为条件的**Stable Diffusion 1.5**（Rombach et al., CVPR 2022），MetamerGen在条件模态和集成方式上做出了根本性改变：

- **条件模态替换**：将文本嵌入替换为DINOv2 patch embeddings，并进一步解耦为两个独立的信息流——中央凹掩码token（仅保留注视区域）和周边全体token（来自降采样模糊图像）。这种双流设计模拟了人类视觉系统中中央凹高分辨率和周边低分辨率gist的并行处理机制。

- **加法交叉注意力集成**：在UNet的交叉注意力层中，将文本（冻结为空字符串）、中央凹、周边三种条件通过**加法组合**（而非串联或替换）注入去噪过程，公式为：

$$ \mathrm{Attention}(Q,K,V) = \mathrm{softmax}\left(\frac{Q K_{\mathrm{text}}^T}{\sqrt{d_k}}\right) V_{\mathrm{text}} + \lambda_{\mathrm{foveal}} \mathrm{softmax}\left(\frac{Q K_{\mathrm{foveal}}^T}{\sqrt{d_k}}\right) V_{\mathrm{foveal}} + \lambda_{\mathrm{peripheral}} \mathrm{softmax}\left(\frac{Q K_{\mathrm{peripheral}}^T}{\sqrt{d_k}}\right) V_{\mathrm{peripheral}} $$

其中 $\lambda_{\mathrm{foveal}}=1.2$、$\lambda_{\mathrm{peripheral}}=0.7$ 为推理时的缩放因子，用于调节两种视觉信息流的相对贡献。这种设计使得模型能够根据注视数量和位置灵活调节生成图像的语义与细节。

### 注视感知的训练与推理策略

为支持可变注视数量的条件输入，MetamerGen引入了两项关键训练策略：

- **随机注视掩码采样**：训练时随机采样1-10个注视token，使模型学会从稀疏到密集的不同注视模式下重建场景。
- **条件丢弃正则化**：以 $p_{\mathrm{foveal}}=0.05$、$p_{\mathrm{peripheral}}=0.10$ 的概率随机丢弃中央凹或周边条件，增强模型对单一信息流的鲁棒性，同时防止过拟合到特定条件组合。

推理阶段采用CFG++采样器，并通过调节 $\lambda$ 因子控制双流信息的融合强度，使生成过程与人类注视行为实时对齐。

### 核心洞察：语义相似性驱动metamer判断

MetamerGen的设计背后有一个关键的因果发现：**场景同质异构体的产生主要由高级语义特征相似性（DreamSim）决定，而非像素级相似性**。消融实验表明，DreamSim距离是预测metamer判断最重要的因素（$\Delta R^2=0.10$），而PSNR无法区分“相同”与“不同”判断（Figure 12）。这一洞察直接指导了DINOv2编码器的选择——相比CLIP，DINOv2在周边信息编码上显著降低了FID，并在低token数下提升了语义相似性（Figure 15, Figure 16），证明其对视觉层次结构的表征更接近人类知觉。

### 双流融合的必要性：来自行为实验的决定性证据

行为消融实验（Section 5.3, Figure 13）为双流设计的必要性提供了最强证据：同时使用中央凹和周边信息的完整模型metamer率达到**54.5%**，仅周边信息为**45.8%**，而仅中央凹信息仅为**8.4%**。这一巨大差距表明，周边gist提供了场景理解的骨架，而中央凹细节则在此基础上进行精细化对齐，两者缺一不可。更重要的是，基于观察者自身注视生成的图像比随机注视生成的在语义上更对齐（Figure 5），说明注视位置携带了观察者特定的内部表征信息，MetamerGen成功捕获了这一动态过程。

![[assets/figures/papers/paper_list_l15_https_openreview_net_forum_id_cSDXx8V6K9/figures/004_Figure_4.jpg]]
*Figure 4: Multi-level feature analysis pipeline using neurally-grounded model: (Top) Early, mid, and late network layers serve as proxies for different stages of processing across the hierarchy of visual brain areas. (Bottom) Results show that as feature similarity increased at these different processing levels, the proportion of participants judging generated images as metameric also increased. These effects were clearer when metamers were generated based on a viewer’s own fixated locations (salmon) than on randomly-sampled locations (turquoise)*

![[assets/figures/papers/paper_list_l15_https_openreview_net_forum_id_cSDXx8V6K9/figures/001_Figure_1.jpg]]
*Figure 1: MetamerGen model architecture. High-resolution and blurred, low-resolution images are processed through DINOv2-Base to extract patch tokens. Foveal features are obtained by applying binary masks to high-resolution patch tokens, retaining only fixated regions. Both foveal and peripheral patch tokens are processed through separate Perceiver-based query networks that compress features into conditioning tokens compatible with Stable Diffusion’s cross-attention mechanism. The resulting dual conditioning streams are integrated into the pretrained UNet*

MetamerGen 的整体流水线围绕一个核心目标构建：**将人类动态注视过程中的双流视觉信息（中央凹高分辨率细节 + 周边低分辨率 gist）转化为与人类内部场景表征知觉等价的生成图像**。该框架以预训练的 Stable Diffusion 1.5（Rombach et al., CVPR 2022）为生成基座，通过适配器架构将注视引导的 DINOv2 特征注入扩散去噪过程。

### 输入流与特征提取

流水线接收两类输入：原始高分辨率场景图像 $I_{\text{original}}$ 和经过降采样-升采样处理的模糊图像 $I_{\text{peripheral}}$（模拟周边视觉的低分辨率特性）。两者分别送入冻结的 **DINOv2-Base 特征提取器**，获得 patch token 序列。

- **中央凹流**：对 $I_{\text{original}}$ 的 patch token 施加二值注视掩码 $M_{\text{fixation}}$，仅保留注视坐标对应的 token，其余位置归零。这模拟了人类仅在高分辨率中央凹区域获取精细信息的特点。
- **周边流**：对 $I_{\text{peripheral}}$ 的全体 patch token 不做掩码，完整保留场景的全局 gist 信息。

### 条件嵌入压缩

两路 token 序列分别通过独立的 **Perceiver Resampler** $R_{\text{foveal}}$ 和 $R_{\text{peripheral}}$，将 1024 个 DINOv2 patch token 压缩为各 32 个条件 token：

$$e_{\text{foveal}} = R_{\text{foveal}}(\text{DINOv2}(I_{\text{original}}) \odot M_{\text{fixation}}), \quad e_{\text{peripheral}} = R_{\text{peripheral}}(\text{DINOv2}(I_{\text{downsample}}))$$

### 多条件交叉注意力集成

压缩后的条件嵌入与冻结的文本条件（设为空字符串以消除文本引导）通过**加法组合**集成到 Stable Diffusion UNet 的交叉注意力层中。每种条件独立投影为键 $K_c$ 和值 $V_c$，最终注意力输出为三项之和：

$$\text{Attention}(Q,K,V) = \text{softmax}\left(\frac{Q K_{\text{text}}^T}{\sqrt{d_k}}\right) V_{\text{text}} + \lambda_{\text{foveal}} \cdot \text{softmax}\left(\frac{Q K_{\text{foveal}}^T}{\sqrt{d_k}}\right) V_{\text{foveal}} + \lambda_{\text{peripheral}} \cdot \text{softmax}\left(\frac{Q K_{\text{peripheral}}^T}{\sqrt{d_k}}\right) V_{\text{peripheral}}$$

其中 $\lambda_{\text{foveal}}=1.2$、$\lambda_{\text{peripheral}}=0.7$ 为推理时的缩放因子，用于调节各信息流的贡献强度。

### 训练与推理策略

- **训练时**：随机采样注视数量（1-10 个 token）和周边模糊级别，并采用条件丢弃策略（$p_{\text{foveal}}=0.05$, $p_{\text{peripheral}}=0.10$）增强鲁棒性。
- **推理时**：使用 CFG++ 采样器，50 步 DDIM 去噪以满足实时生成需求（行为实验中需在 5 秒内完成生成）。

### 模块关系与数据流

整体数据流可概括为：**原始图像 + 模糊图像 → DINOv2 双流特征提取 → 注视掩码/全保留 → Perceiver 压缩 → 加法交叉注意力注入 UNet → 扩散去噪生成**。Figure 1 展示了这一架构的全貌，其中双流信息的融合是产生场景同质异构体的关键——消融实验表明，仅中央凹信息的 metamer 率仅 8.4%，仅周边信息为 45.8%，而完整双流模型达到 54.5%（Section 5.3, Figure 13），证实了中央凹精细细节与周边场景 gist 协同作用的必要性。

### 双流DINOv2特征编码

MetamerGen 的核心设计在于将人类注视行为解耦为两条互补的信息流：**中央凹（foveal）** 通道捕获注视点处的高分辨率细节，**周边（peripheral）** 通道编码全局场景的低分辨率gist信息。两条通道共享一个冻结的 DINOv2-Base（with registers）作为视觉编码器，但输入和掩码策略不同。

**中央凹特征提取**：对原始高分辨率图像 $I_{\mathrm{original}}$ 经 DINOv2 提取的 patch tokens，施加二值注视掩码 $M_{\mathrm{fixation}}$，仅保留注视点所在区域的 token，其余位置置零。这一操作模拟了人类视网膜中央凹的高锐度采样。

**周边特征提取**：将原始图像先降采样再升采样至原分辨率，得到模糊图像 $I_{\mathrm{downsample}}$，经 DINOv2 提取全部 patch tokens 而不做掩码。该设计模拟了周边视野的低通滤波特性，迫使模型从全局布局和粗粒度语义中重建场景。

### 条件嵌入压缩与投影

两条通道各自产生 1024 个 DINOv2 patch embeddings，需压缩为扩散模型可消费的固定长度条件 token。MetamerGen 采用两个独立的 **Perceiver Resampler** 网络 $R_{\mathrm{foveal}}(\cdot)$ 和 $R_{\mathrm{peripheral}}(\cdot)$，将高维特征压缩为 32 个条件 token：

$$
e_{\mathrm{foveal}} = R_{\mathrm{foveal}}(\mathrm{DINOv2}(I_{\mathrm{original}}) \odot M_{\mathrm{fixation}}), \quad
e_{\mathrm{peripheral}} = R_{\mathrm{peripheral}}(\mathrm{DINOv2}(I_{\mathrm{downsample}}))
$$

其中 $\odot$ 表示逐元素乘法。文本条件 $e_{\mathrm{text}}$ 被冻结为空字符串的嵌入，以消除语义先验的干扰，确保生成仅由视觉注视信号驱动。

### 加法多条件交叉注意力

MetamerGen 将文本、中央凹、周边三种条件以**加法形式**集成到 Stable Diffusion UNet 的交叉注意力层中。每种条件独立投影为键 $K_c$ 和值 $V_c$：

$$
K_c = e_c W_K^c, \quad V_c = e_c W_V^c, \quad c \in \{\mathrm{text}, \mathrm{foveal}, \mathrm{peripheral}\}
$$

UNet 中间特征 $F$ 投影为查询 $Q = F W_Q$。最终的交叉注意力输出为三个独立注意力头的加权和：

$$
\mathrm{Attention}(Q,K,V) = \mathrm{softmax}\!\left(\frac{Q K_{\mathrm{text}}^T}{\sqrt{d_k}}\right) V_{\mathrm{text}}
+ \lambda_{\mathrm{foveal}} \cdot \mathrm{softmax}\!\left(\frac{Q K_{\mathrm{foveal}}^T}{\sqrt{d_k}}\right) V_{\mathrm{foveal}}
+ \lambda_{\mathrm{peripheral}} \cdot \mathrm{softmax}\!\left(\frac{Q K_{\mathrm{peripheral}}^T}{\sqrt{d_k}}\right) V_{\mathrm{peripheral}}
$$

其中 $\lambda_{\mathrm{foveal}} = 1.2$、$\lambda_{\mathrm{peripheral}} = 0.7$ 为推理时的缩放因子，用于调节两条视觉通道的相对贡献。这种加法设计（而非拼接或门控）使得各条件流保持独立可解释性，同时允许 UNet 在去噪过程中灵活组合全局布局与局部细节。

### 训练与推理策略

训练阶段采用随机注视掩码（1–10 个 token）和周边模糊级别采样，并施加条件丢弃（$p_{\mathrm{foveal}} = 0.05$，$p_{\mathrm{peripheral}} = 0.10$）以增强鲁棒性。推理阶段使用 CFG++ 采样器，扩散步数固定为 50 步以平衡实时生成需求与图像质量。

## 实验与关键发现

### 核心行为范式与总体结果

为评估MetamerGen是否生成感知上令人信服的场景同质异构体（metamer），作者设计了一个实时同异判断行为范式（Figure 6）。45名被试自由观看原始场景图像，达到预设注视次数（1、2、3、5或10次）后，图像消失；注视坐标通过API实时传输至MetamerGen，在5秒内生成新图像。随后，生成图像（或原始图像，作为对照条件）以200ms短暂呈现，被试需在10秒内通过游戏手柄判断“相同”或“不同”。实验排除了含人类、文本、时钟等复杂元素的图像。

在自身注视条件下，MetamerGen的总体metamer率（被试判断为“相同”的比例）为29.4%，而随机注视条件下为27.7%，差异不显著（p=0.24）。这表明仅凭注视位置的整体统计差异不足以驱动metamer感知的显著变化，需要更细粒度的特征分析来解释判断机制。

### 多层级特征对齐驱动Metamer判断

为揭示哪些视觉特征驱动metamer感知，作者采用了一个经模糊训练的AlexNet（Jang & Tong, 2024），其内部表征与从V1到IT的视觉脑区神经响应对齐。从早期、中期和晚期层提取特征图，计算原始图像与生成图像间的余弦相似度（Figure 4）。

**关键发现：** 在自身注视条件下，所有层级的特征相似度均与metamer判断正相关——相似度越高，“相同”判断比例越大。这一关系在视觉层级的各阶段一致成立，表明metamer需要整个视觉层次的对齐，而非仅高层语义。与之形成鲜明对比的是，随机注视条件下，当特征相似度较高时，metamer率反而下降。这一反向关系暗示：随机注视生成的图像可能在局部纹理上匹配，但缺乏与人类注视驱动的全局场景理解一致的语义结构，导致被试更容易察觉差异。

### 中高层视觉特征的预测力分解

通过前向逐步回归量化各可解释视觉特征对metamer判断的贡献（Section A.4, Figure 12），**DreamSim距离是预测metamer判断的最重要因素（ΔR²=0.10）**，远超其他特征。具体而言：

- **高层语义特征（Figure 5 Right）：** DreamSim距离越小，“相同”判断比例越高，且这一关系仅在自身注视条件下成立。CLIP余弦相似度在自身注视条件下也呈现正相关趋势，但在随机注视条件下完全不具预测性——这是理解模型行为的关键差异点。
- **中层特征（Figure 5 Left）：** 单目深度估计的变化（SiLog误差）和原型物体分割的对齐程度（mIoU）均与metamer率正相关，但预测力弱于高层语义特征。
- **低层纹理特征（Figure 7）：** Gabor滤波器响应的增强（相较于原始图像）与更高的metamer判断比例相关，表明增强的纹理定义有助于提升生成场景的感知真实感。
- **像素级相似度（PSNR）无法预测metamer判断（Figure 12）：** “相同”与“不同”判断的PSNR分布几乎完全重叠，而DreamSim距离可清晰分离两类判断。这构成核心证据：场景同质异构体的产生由高级语义特征相似性决定，而非像素级保真度。

![[assets/figures/papers/paper_list_l15_https_openreview_net_forum_id_cSDXx8V6K9/figures/005_Figure_5.jpg]]
*Figure 5: (Left) Mid-level visual features driving metamer judgments: For metamers generated from the viewer’s own fixation locations (salmon), changes in monocular depth estimates of scene structure strongly predicted “same” judgments to generations. The alignment in protoobject segmentation between original and generated scenes, quantified by mIoU, similarly predicted metamerism rate (higher mIoU scores correlating with higher proportions of “same” judgments), although here the relationship was less pronounced. (Right) High-level visual features driving metamer judgments: Semantic similarity strongly predicts metameric scene understanding, with larger DreamSim distances corresponding to reduced per...*

![[assets/figures/papers/paper_list_l15_https_openreview_net_forum_id_cSDXx8V6K9/figures/007_Figure_7.jpg]]
*Figure 7: Stronger Gabor texture responses than originals coincided with greater proportions of metameric judgments. This suggests that enhanced texture definition, like enhanced edge information, contributes to the perceived realism of generated metamers across multiple spatial frequencies and orientations*

### 物体检测精度与Metamer感知的关联

使用预训练物体检测器评估生成图像中的物体保留程度（Figure 8）。在自身注视条件下，物体检测精度（mAP）的提升与metamer率呈正相关，尤其在严格定位阈值（mAP 60%至80%）下更为明显。精确率、召回率和F1分数的改善均与“相同”判断比例增加相关。这表明生成图像中物体的正确保留和定位是metamer感知的重要底层支撑。

![[assets/figures/papers/paper_list_l15_https_openreview_net_forum_id_cSDXx8V6K9/figures/008_Figure_8.jpg]]
*Figure 8: Object detection errors predict metameric perception: (Top) mAP scores demonstrate that higher precision accuracies (from mAP 60% to mAP 80%) with better alignment at strict localization boundaries correlate with increased “same” metameric judgments. (Bottom) Object detection metrics show a positive relationship where improvements in model precision, recall, and F1 scores correspond to increased “same” metameric judgments*

### 消融实验：中央凹与周边信息的双重必要性

通过系统消融条件流评估中央凹和周边信息各自的贡献（Section 5.3, Figure 13）：

| 条件 | Metamer率 |
|------|-----------|
| 完整模型（中央凹+周边） | **54.5%** |
| 仅周边信息 | 45.8% |
| 仅中央凹信息 | 8.4% |

仅中央凹信息的metamer率极低（8.4%），证明注视区域的局部高分辨率细节远不足以重建人类场景理解。周边信息贡献了大部分metamer感知（45.8%），而中央凹信息的加入进一步提升了8.7个百分点，表明注视带来的高分辨率细节在周边gist基础上提供了有意义的增量。Figure 14进一步展示了三种条件下多层级特征对metamer判断的可解释性差异，完整模型在各层级均保持最强的预测关系。

![[assets/figures/papers/paper_list_l15_https_openreview_net_forum_id_cSDXx8V6K9/figures/014_Figure_14.jpg]]
*Figure 14: Impact of input visual streams on hierarchical feature analyses. (Top Row) Multilevel feature analysis using neurally-grounded model (Jang & Tong, 2024) on driving metameric judgments. (Middle Row) Mid-level visual features driving metameric judgments (mid-level segemention mIoU and SiLog depth estimation). (Bottom Row) High-level visual features driving metameric judgments (CLIP cosine similarity and DreamSim distance)*

### 编码器选择与生成质量

DINOv2与CLIP作为视觉编码器的对比消融（Figure 15, Figure 16）揭示了关键差异：

![[assets/figures/papers/paper_list_l15_https_openreview_net_forum_id_cSDXx8V6K9/figures/015_Figure_15.jpg]]
*Figure 15: FID and DreamSim evaluations based on DINOv2 and CLIP as vision encoders for foveal and peripheral feature extraction. (Left) The image generation quality (FID) for DINOv2- based peripheral generations is consistently better than CLIP patch embeddings. For DINOv2, we observe a sharp drop when decreasing the blur level, showing how decreasing blur results in the model encoding different, more accurate image features. This is not true for CLIP patch tokens, which seem to encode the same limited information across all blur levels. (Right) With increasing numbers of foveal token inputs, the DreamSim distance for both DINOv2 and CLIP-based embeddings decreases. However, DINOv2-based generations...*

- **周边信息编码：** DINOv2在周边条件下FID显著优于CLIP，且随模糊程度降低（下采样率从28×28升至448×448），DINOv2的生成质量持续改善，而CLIP几乎无变化。这表明CLIP的patch token在不同模糊级别下编码的信息量有限且相似。
- **中央凹信息编码：** 随中央凹token数量增加，两种编码器的DreamSim距离均下降，但DINOv2在低token数下语义相似性优势更明显。
- **定性对比（Figure 16）：** DINOv2生成的图像在物体大小和空间位置上更好地保留了原始图像的结构，而CLIP生成在低模糊度下改善甚微。

增加中央凹token数量可改善生成质量（FID和DreamSim），但仅凭中央凹token远不及周边信息（Figure 11 Bottom），再次验证了双流信息融合的必要性。

![[assets/figures/papers/paper_list_l15_https_openreview_net_forum_id_cSDXx8V6K9/figures/011_Figure_11.jpg]]
*Figure 11: Influence of blur-level and foveal token count on image generation quality. (Top Row) Image generation quality decreases as greater blur degrades the base image. (Bottom Row) Image generation quality increases as a function of increasing foveal tokens*

### 局限性与失败模式

1. **总体metamer率仍较低（约29%）：** 即使完整模型在消融中达到54.5%，实际行为实验中仅约29%，表明对复杂场景内部表征的重建仍不充分。
2. **200ms短暂呈现可能低估辨别能力：** 快速呈现限制了被试对精细细节的加工，实际感知等价性阈值可能更低。
3. **图像内容限制：** 排除含人类、文本、时钟等图像，限制了结论的泛化性。
4. **实时生成约束：** 50步DDIM采样限制了图像质量，更多步数可能提升metamer率。
5. **未探索任务驱动注视和动态场景：** 当前仅使用自由观看注视，不同任务目标下的注视策略可能产生不同的metamer特征。

## 定位与知识库关联

### 方法定位与基线关系

MetamerGen 的核心技术路线属于**基于扩散模型的图像条件生成**，但其条件信号从传统的文本嵌入转向了**双流注视驱动的视觉特征**。该方法直接建立在 **Stable Diffusion 1.5**（Rombach et al., CVPR 2022）的潜在扩散框架之上，但通过适配器架构（adapter-based framework）将条件注入方式进行了根本性改造。

与标准文本到图像生成相比，MetamerGen 的关键差异体现在四个维度：

1. **条件模态替换**：将文本嵌入替换为 DINOv2 patch embeddings，其中中央凹 token 通过注视掩码筛选，周边 token 来自降采样模糊图像的全量 patch（Section 3.1）。
2. **多条件加法集成**：文本、中央凹、周边三种条件通过独立的 Perceiver 重采样器压缩为 32 个条件 token 后，以加法形式组合到 UNet 的交叉注意力中（Eq. 5），而非单一条件注入。
3. **注视感知训练策略**：训练时随机采样注视数量（1-10 个 token）和周边模糊级别，并引入条件丢弃机制（p_foveal=0.05, p_peripheral=0.10），使模型对不同注视配置具有鲁棒性（Section 3.3）。
4. **推理缩放因子**：采用 CFG++ 采样，并设置 λ_foveal=1.2, λ_peripheral=0.7，以平衡中央凹细节与周边上下文在生成中的贡献（Section 3.3）。

在生成质量基准上，MetamerGen 在 COCO-10k-test 上的 FID 指标优于纯文本条件的 Stable Diffusion 1.5 基线（Figure 2），验证了注视驱动条件相较于文本描述在场景重建保真度上的优势。

### 核心瓶颈与因果机制

该工作解决的真实瓶颈是：**现有场景理解模型无法模拟人类动态注视行为中中央凹高分辨率信息与周边低分辨率 gist 信息的融合过程**，且缺乏行为范式来验证生成场景的知觉等价性。

因果操纵的核心在于双流 DINOv2 特征适配器：中央凹掩码 token 提供注视区域的精细语义，周边全量 token 提供场景上下文，两者通过加法交叉注意力集成到冻结的 Stable Diffusion UNet 中。这一设计使模型能够根据注视数量和位置精确调节生成图像的语义与细节。

决定性证据表明，该机制的有效性依赖于高级语义特征的对齐：DreamSim 距离是预测 metamer 判断最重要的因素（ΔR²=0.10），而像素级相似度（PSNR）无法区分“same”与“different”判断（Figure 12）。同时，基于观察者自身注视生成的场景中，DreamSim 和 CLIP 相似度与 metamer 率正相关，而随机注视则不存在此关系（Figure 5 Right），说明注视信息的个性化编码是产生知觉等价的关键。

### 消融实验揭示的适用边界

消融实验为 MetamerGen 的适用边界提供了清晰证据：

- **双流信息的必要性**：完整模型（中央凹+周边）的 metamer 率达 54.5%，仅周边条件为 45.8%，仅中央凹条件骤降至 8.4%（Section 5.3, Figure 13）。这表明周边 gist 信息是场景理解的基础，中央凹细节起增强作用但无法独立支撑场景重建。
- **编码器选择的影响**：DINOv2 作为视觉编码器在周边信息编码上显著优于 CLIP，FID 更低且在低 token 数下 DreamSim 相似度更高（Figure 15）。CLIP 在不同模糊级别下编码的信息量几乎不变，而 DINOv2 能随模糊降低持续提取更准确的特征（Figure 16），这限制了 CLIP 在该任务中的适用性。
- **注视数量与质量的权衡**：增加中央凹 token 数量可改善生成质量（FID, DreamSim），但即便大量中央凹 token 也远不及周边信息的贡献（Figure 11 Bottom），说明场景 gist 的编码效率远高于逐点注视累积。
- **特征层级贡献差异**：高级语义特征（DreamSim）对 metamer 判断的贡献最大（ΔR²=0.10），其次为 Gabor 纹理、深度估计、中层 CNN 特征等（Section A.4），表明 metamer 需要整个视觉层次的对齐，但高层语义是主导因素。

### 局限与开放问题

**已明确的局限：**

1. **整体 metamer 率偏低**：即使在最优条件下，metamer 率仅约 54.5%，在自然观看条件下（自身注视）仅约 29%，表明对复杂场景内部表征的重建仍存在显著不足。
2. **行为范式限制**：仅采用 200ms 的短暂呈现，可能低估了精细细节的辨别能力；实验排除了含人类、文本、时钟等复杂元素的图像，限制了结论的泛化性。
3. **基座模型依赖**：依赖 DINOv2 编码器的特性，可能对某些视觉特征不敏感；使用 Stable Diffusion 1.5 作为基座，其生成能力直接影响最终质量上限。
4. **实时生成约束**：实时生成需求限制了扩散步数（50 步），可能影响图像质量。
5. **注视策略单一**：仅探索了自由观看注视，未涉及任务驱动注视或动态场景。

**待解决的开放问题：**

- 哪些具体的高层语义特征（如物体类别、空间关系、场景布局）最能预测 metamerism？
- 注视次数如何定量影响 metamer 生成质量和 metamer 率？是否存在饱和点？
- 为什么 CLIP 相似度能预测自身注视生成的 metamer 判断，却无法预测随机注视生成的判断？这是否反映了两种注视条件下场景表征的本质差异？
- MetamerGen 框架能否扩展到动态场景或视频的知觉理解？
- 个体差异（如视觉能力、注意力策略）如何调节 metamer 生成的效果？

## 原文 PDF

![[paperPDFs/ICLR_2026/Generating_metamers_of_human_scene_understanding.pdf]]
