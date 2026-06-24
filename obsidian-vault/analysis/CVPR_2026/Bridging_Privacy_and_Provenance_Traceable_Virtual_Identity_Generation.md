---
title: "Bridging Privacy and Provenance: Traceable Virtual Identity Generation"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/Bridging_Privacy_and_Provenance_Traceable_Virtual_Identity_Generation.pdf
project_link: null
code_link: null
aliases:
- TVIG
- BPPTVIG
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
- topic/generative_models_diffusion
core_operator: 在扩散模型框架中引入虚拟身份采样器、3D几何与表情双分支条件以及隐式水印嵌入，实现身份解耦、属性保留和可验证溯源的一体化生成。
primary_logic: 通过将基于用户生物特征派生的轻量级数字水印嵌入到扩散解码过程中，可在不暴露真实面容的前提下为虚拟人脸绑定可验证的所有权签名，从而在保持身份一致性和匿名性的同时提供可追溯性。
claims:
- 在 CelebA-HQ 上，vMF 虚拟身份采样器实现 ArcFace EER 0.002，远低于最佳基线 RiDDLE 的 0.046，证明极高的虚拟身份一致性。
- 匿名性指标 IAR 达到 1.000，表明生成的虚拟身份与原始身份完全无法关联。
- 水印位准确率达到 0.998，且视觉质量几乎无损失（PSNR 39.74, SSIM 0.974），验证了轻量级身份绑定的可行性与保真度。
- CelebA-HQ 上 ArcFace EER↓ = 0.002 (Ours vMF & HS-AE)
---

# Bridging Privacy and Provenance: Traceable Virtual Identity Generation

> [!tip] 核心洞察
> 通过将基于用户生物特征派生的轻量级数字水印嵌入到扩散解码过程中，可在不暴露真实面容的前提下为虚拟人脸绑定可验证的所有权签名，从而在保持身份一致性和匿名性的同时提供可追溯性。

| 字段 | 内容 |
|------|------|
| 中文题名 | 桥接隐私与溯源：可追踪虚拟身份生成 |
| 英文题名 | Bridging Privacy and Provenance: Traceable Virtual Identity Generation |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://openaccess.thecvf.com/content/CVPR2026/html/Zeng_Bridging_Privacy_and_Provenance_Traceable_Virtual_Identity_Generation_CVPR_2026_paper.html) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction #topic/generative_models_diffusion |
| Method | Traceable Virtual Identity Generation |
| Dataset | CelebA-HQ, FFHQ |

> [!tip] 效果简介
> - CelebA-HQ 上，ArcFace EER↓ 0.002 (Ours vMF & HS-AE) vs 0.046 (RiDDLE) (-0.044)；ArcFace AUC↑ 1.000 (Ours vMF & HS-AE) vs 0.757 (RiDDLE) (+0.243)；Watermark Bit Accuracy↑ 0.998 vs N/A (自身嵌入与提取) (N/A)。
> - FFHQ 上，Pitch Error↓ / Roll Error↓ / Yaw Error↓ / Expression Similarity↑ 2.66 / 1.52 / 2.30 / 0.863 vs 所有对比方法中最低（具体数值见原文 Table 5） (N/A)。

## 概述

**问题瓶颈。** 现有虚拟身份生成方法面临一个根本性矛盾：若要保持跨实例的身份一致性，往往需要暴露足够多的身份信息，从而削弱匿名性；若追求强匿名性，又容易导致身份漂移或丧失可追溯性。诸如 **CIAGAN** (Maximov et al., CVPR 2020)、**FIT** (Gu et al., ECCV 2020)、**RiDDLE** (Li et al., CVPR 2023) 等工作分别从条件生成、可逆变换和多样化去身份化等角度切入，但均未内生地提供所有权验证机制，使得虚拟身份在应用中难以问责。

**核心思路。** 本文提出一种基于扩散模型的可追踪虚拟身份生成框架，核心创新在于将身份解耦、属性保留与溯源验证统一为单一流程。具体而言，该方法在扩散解码过程中嵌入由用户生物特征派生并加密的轻量级数字水印，在不暴露真实面容的前提下为虚拟人脸绑定可验证的所有权签名——这构成了连接隐私保护与溯源问责的关键因果机制。

**方法定位。** 该框架由三个协同模块构成：虚拟身份采样器在 ArcFace 嵌入空间中生成与原始身份角度远离但实例间一致的虚拟身份嵌入；双分支 3D 条件体系（EMOCA 提供全局几何与粗粒度表情约束，SMIRK 补充细粒度高频表情细节）确保姿态与表情的高保真保留；水印感知的 VAE 解码器在合成虚拟人脸的同时嵌入 128 位身份签名，支持后续无损提取与匹配验证。

**主要结果。** 在 CelebA-HQ 上，vMF 虚拟身份采样器实现了 ArcFace EER 0.002，较最佳基线 RiDDLE 的 0.046 降低了 0.044（Table 1），表明极高的虚拟身份一致性。匿名性指标 IAR 达到 1.000（Table 2），证明生成的虚拟身份与原始身份完全无法关联。水印位准确率达到 0.998，且嵌入后图像的 PSNR 为 39.74、SSIM 为 0.974（Table 6），验证了轻量级身份绑定的可行性与视觉保真度。在 FFHQ 上，头部姿态误差（Pitch/Roll/Yaw）分别为 2.66/1.52/2.30，表情相似度达 0.863（Table 5），姿态与表情保留能力均优于对比方法。

## 背景与动机

人脸图像在身份认证、社交娱乐、虚拟交互等场景中被广泛采集与使用，但随之而来的隐私风险也日益突出——直接暴露真实面容可能导致身份盗用、未授权追踪或深度伪造攻击。为应对这一挑战，面部匿名化与虚拟身份生成技术应运而生，其目标是在剥离原始身份信息的同时，保留人脸图像中与身份无关的语义属性（如姿态、表情、光照），使生成结果仍可用于下游分析或交互任务。

然而，现有方法在三个关键维度上存在结构性缺口，难以同时满足实际部署的需求：

**身份一致性与匿名性的矛盾。** 早期基于生成对抗网络的方法如 **CIAGAN**（Maximov et al., CVPR 2020）和 **FALCO**（Barattin et al., CVPR 2023）通过条件生成或潜码优化实现属性保留的面部匿名化，但生成的虚拟身份在不同实例间缺乏稳定的对应关系——同一用户的多次匿名化结果可能被识别为不同身份，导致“身份漂移”。基于密码条件的可逆方法如 **FIT**（Gu et al., ECCV 2020）和 **RiDDLE**（Li et al., CVPR 2023）虽然支持可逆的身份变换，但其可逆性本身构成隐私泄漏的潜在通道。单射映射方法 **IVFG**（Yuan et al., ACM MM 2022）试图从真实身份生成固定的虚拟身份，但在匿名强度与身份一致性之间缺乏精细的调控手段。**G²Face**（Yang et al., TIFS 2024）引入几何先验以提升保真度，**FAS**（Kung et al., WACV 2025）追求简单高效，但它们均未在一致性与匿名性的联合优化上给出系统解。

**可追溯性的缺失。** 上述所有方法均未内建所有权验证机制。当虚拟人脸被用于恶意目的（如冒充他人、生成虚假内容）时，无法从生成结果中追溯其来源用户，导致问责链条断裂。这一缺陷使得虚拟身份技术在高合规性场景（如金融、政务）中难以落地。

**姿态与表情保留的粗粒度。** 现有方法多采用简单的属性编辑或无关属性保留策略，对头部姿态的全局几何变化和面部表情的细粒度高频细节缺乏分别建模，导致生成的虚拟人脸在姿态一致性或表情生动性上存在明显折损。

上述瓶颈的根源在于：虚拟身份生成需要在一个统一的框架中同时解决身份解耦、属性保留与可验证溯源三个子问题，而现有工作往往将三者割裂处理。本文的核心动机即在于弥合这一鸿沟——通过将基于扩散模型的生成能力、虚拟身份采样策略与隐式身份水印嵌入相结合，构建一个端到端的可追踪虚拟身份生成框架，在保持高身份一致性和强匿名性的同时，为每一张生成的虚拟人脸绑定可验证的所有权签名。

## 核心创新

本工作针对现有虚拟身份生成方法在**身份一致性、匿名性与可追溯性**三者无法兼得的瓶颈，提出了一套基于扩散模型的统一框架。其核心创新并非单一算法突破，而是通过三个**方法槽位（changed slots）** 的系统性重构，将身份解耦、属性保留与所有权验证首次集成到同一生成管线中。

### 从“身份映射”到“身份采样”：虚拟身份采样器

现有方法大多直接使用原始身份嵌入或通过可逆变换生成虚拟身份（如 **FIT** (Gu et al., ECCV 2020) 的密码条件变换、**IVFG** (Yuan et al., ACM MM 2022) 的单向映射），这种方式难以同时保证虚拟身份的实例间一致性与可控匿名性。本框架的核心机制转变在于引入**虚拟身份采样器（Virtual Identity Sampler）**，在预训练人脸识别器的超球面嵌入空间中，为每个真实身份分配一个在角度上远离原始嵌入、但在同一用户的不同图像间保持稳定的虚拟身份嵌入。

框架实例化了三种采样策略，覆盖了从无训练到强条件生成的设计谱系：
- **vMF 采样**：基于 von Mises-Fisher 分布的直接采样，无需训练，通过控制浓度参数调节虚拟身份嵌入的集中程度。
- **HS-AE（超球面自编码器）**：在单位球面上训练编码器-解码器，将身份嵌入压缩为低维潜码 $\mathbf{z}$，解码器 $D_{\psi}$ 通过余弦相似度重建损失 $\mathcal{L} = 1 - \cos(\hat{\mathbf{e}}, \mathbf{e})$ 学习映射，并在推理时通过切线空间噪声注入 $\mathbf{z} = \mathrm{norm}((1 - \eta)\boldsymbol{\mu} + \eta \mathrm{norm}(\boldsymbol{\mu} + \sigma \boldsymbol{\xi}_{\perp}))$ 实现可控多样性。
- **ID-Mixer**：以原始身份嵌入 $\mathbf{e}_{ori}$ 和随机潜码 $\mathbf{z}$ 为条件，通过生成器 $G_{\phi}$ 直接合成虚拟身份嵌入 $\mathbf{e}_{vir} = G_{\phi}(\mathbf{e}_{ori}, \mathbf{z})$，其多任务损失 $\mathcal{L} = \lambda_{\mathrm{ano}} \mathcal{L}_{\mathrm{ano}} + \lambda_{\mathrm{div}} \mathcal{L}_{\mathrm{div}} + \lambda_{\mathrm{intra}} \mathcal{L}_{\mathrm{intra}} + \lambda_{\mathrm{inter}} \mathcal{L}_{\mathrm{inter}} + \lambda_{\mathrm{reg}} \mathcal{L}_{\mathrm{reg}}$ 显式平衡匿名性、多样性、类内一致性与类间分离。

这一设计的关键因果作用在于：将身份决策从扩散模型的条件注入阶段前移至独立的采样阶段，使扩散模型只需忠实地“描绘”给定的虚拟身份，而无需在生成过程中同时处理匿名化与一致性约束。实验证据表明，vMF 和 HS-AE 采样器在 CelebA-HQ 上实现了 ArcFace EER 0.002（Table 1），较最佳基线 **RiDDLE** (Li et al., CVPR 2023) 的 0.046 降低了一个数量级以上，验证了极高程度的虚拟身份一致性。

### 从“属性编辑”到“双分支条件注入”：几何与表情的解耦保留

现有方法对姿态和表情的保留多采用简单的属性编辑或无关属性保留策略（如 **FALCO** (Barattin et al., CVPR 2023) 的潜码优化、**G²Face** (Yang et al., TIFS 2024) 的几何先验），难以同时维持全局几何结构和高频表情细节。本框架提出**双分支条件体系**，将姿态与表情的保留分解为两个互补通路：

- **EMOCA 分支**：提取 3D 头部姿态参数与粗粒度表情，生成法线图（normal map）作为 **ControlNet** 的空间条件，提供全局几何约束与姿态锚定。
- **SMIRK 分支**：提取高维表情编码，通过 **IP-Adapter 风格**的交叉注意力机制注入扩散 UNet 的中间层，补充细粒度、高频的表情细节（如嘴角弧度、眼睑微动）。

双分支设计的因果机制在于：EMOCA 的法线图条件通过 ControlNet 的卷积通路影响生成图像的全局结构布局，而 SMIRK 的适配器通过注意力机制在语义层面调制局部纹理，二者在特征空间中形成“粗几何 + 细纹理”的分工，避免了单一条件通路下全局约束与局部细节的冲突。消融实验（Figure 5）证实，移除 EMOCA 会损害全局几何与表情保留，移除 SMIRK 则导致表情生动性下降。

### 从“仅匿名”到“匿名+溯源”：隐式身份水印嵌入

现有虚拟身份生成方法**无一具备内生的所有权验证机制**——一旦虚拟人脸被滥用，无法追溯到原始身份的授权记录。本框架在扩散模型的 VAE 解码阶段嵌入由用户生物特征派生并加密的 128 位身份签名，实现了**轻量级但高保真的可追溯性**。水印嵌入与提取共享解码器权重，在训练时联合优化重建质量与比特准确率，推理时无需额外网络。

该设计的核心洞察在于：水印嵌入发生在潜空间解码为像素空间的最后阶段，此时图像的高级语义（身份、姿态、表情）已由扩散过程确定，水印信号仅调制高频细节，因而几乎不影响视觉质量。实验证据（Table 6）表明，水印比特准确率达到 0.998，同时 PSNR 保持 39.74、SSIM 0.974，视觉质量损失可忽略不计。需要指出的是，该水印机制专为轻量级身份绑定设计，对强鲁棒性攻击（如对抗性扰动、高强度几何变换）的抵抗能力有限，不适用于高安全性取证场景。

## 整体框架

本文提出一个面向**可追踪虚拟身份生成**的扩散框架，其设计目标是在不暴露用户真实面容的前提下，输出具有稳定虚拟身份、保留原始姿态与表情、且内嵌可验证身份签名的虚拟人脸。框架由三个核心模块串联构成：**虚拟身份采样器（Virtual Identity Sampler）**、**基于3DMM的姿态与表情保留模块**，以及**带隐式水印的扩散生成器**。整体流程如 Figure 2 所示：输入一张原始人脸图像，首先提取其 ArcFace 身份嵌入，经虚拟身份采样器映射为匿名化的虚拟身份嵌入；同时，通过 EMOCA 与 SMIRK 双分支提取头部姿态与面部表情参数，分别生成法线图和表情代码作为条件信号；最终，扩散模型以虚拟身份嵌入、法线图、表情代码为条件，合成保留姿态与表情的虚拟人脸，并在 VAE 解码阶段嵌入由用户生物特征派生的 128 位身份水印，实现可追溯的所有权绑定。

![[assets/figures/papers/paper_list_l842_https_openaccess_thecvf_com_content_CVPR2026_html_Zeng_Bridging_Privacy/figures/002_Figure_2.jpg]]
*Figure 2: Overview of our traceable virtual identity generation framework*

### 模块间的数据流与职责分工

**虚拟身份采样器**位于 pipeline 前端，负责将预训练人脸识别器 $E_{id}$ 提取的原始身份嵌入 $\mathbf{e}_{ori}$ 转换为虚拟身份嵌入 $\mathbf{e}_{vid}$。该模块需同时满足三个约束：① 虚拟身份与原始身份在嵌入空间中角度足够远离（匿名性）；② 同一用户的不同输入产生高度一致的虚拟身份嵌入（跨实例一致性）；③ 不同用户间的虚拟身份嵌入保持充分分离（可辨识性）。论文实例化了三种采样策略——基于 von Mises-Fisher 分布的随机采样（vMF）、基于超球面自编码器的生成式采样（HS-AE），以及以原始身份为条件的身份混合网络（ID-Mixer），三者均在 ArcFace 超球面嵌入空间上操作，确保生成的 $\mathbf{e}_{vid}$ 始终位于真实人脸流形附近。

**姿态与表情保留模块**采用 EMOCA 与 SMIRK 的双分支结构，分别负责全局几何约束与细粒度表情注入。EMOCA 从输入人脸重建 3DMM 参数，渲染为法线图后通过 ControlNet 注入扩散 UNet，提供头部姿态与粗粒度几何约束；SMIRK 则提取高维表情代码，经 IP-Adapter 风格的交叉注意力层映射到 UNet 的中间特征，补充高频、细微的表情细节。两分支互补：EMOCA 保证生成人脸的结构合理性，SMIRK 提升表情生动性。

**扩散生成器**以 Stable Diffusion 为骨干，接收三路条件信号——虚拟身份嵌入 $\mathbf{e}_{vid}$ 通过交叉注意力注入以控制“是谁”，法线图通过 ControlNet 注入以控制“什么姿态”，表情代码通过适配器注入以控制“什么表情”。去噪后的潜变量 $\hat{\mathbf{z}}_0$ 送入一个**含水印解码器**：该解码器在标准 VAE 解码器的基础上，额外接收一个 128 位身份签名，将其嵌入到解码过程中的特征图，使得生成的虚拟人脸在视觉上几乎无失真地携带可提取的水印信息。提取时，仅需将带水印图像通过对应的水印提取器即可恢复签名，与预存签名进行匹配即可完成所有权验证。

### 训练与推理的分离设计

三个核心模块的训练是解耦的：虚拟身份采样器（HS-AE 与 ID-Mixer）在 ArcFace 嵌入空间上独立预训练；姿态与表情提取器（EMOCA、SMIRK）使用现成预训练权重；扩散生成器与含水印解码器则联合微调。这种分离设计使得各模块可独立升级或替换，同时避免了端到端训练中身份、姿态、水印信号的相互干扰。推理时，用户仅需提供一张人脸图像，系统自动完成身份匿名化、属性保留与水印嵌入的全流程，输出可直接用于下游身份相关应用的虚拟人脸。

### 补充图表

![[assets/figures/papers/paper_list_l842_https_openaccess_thecvf_com_content_CVPR2026_html_Zeng_Bridging_Privacy/figures/001_Figure_1.jpg]]
*Figure 1: Overview of our traceable virtual identity generation framework. Original face images are converted into watermarked virtual faces for identity-related applications*

## 核心模块与公式推导

### 3.1 虚拟身份采样器

虚拟身份采样是整个框架的入口模块，其核心目标是为每个真实用户分配一个**与原始身份在角度空间中远离、但跨实例保持高度一致**的虚拟身份嵌入。该模块接收预训练人脸识别器 $E_{id}$ 提取的真实身份嵌入作为输入，输出可直接注入扩散模型的条件向量 $\mathbf{e}_{vid}$。

论文实例化了三种不同机制的采样器：

- **vMF（von Mises-Fisher 分布采样）**：在超球面上以固定方向采样，无需训练，直接生成与原始身份无关的虚拟嵌入。其优势在于零训练成本，且生成的虚拟身份在实例间天然一致。
- **HS-AE（超球面自编码器）**：通过编解码结构学习身份嵌入的流形映射。解码过程为 $\mathbf{e}_{vir} = D_{\psi}(\mathbf{z})$，其中 $\mathbf{z}$ 为低维球面潜码，$D_{\psi}$ 为解码器。训练目标为余弦相似度重建损失 $\mathcal{L} = 1 - \cos(\hat{\mathbf{e}}, \mathbf{e})$，无需 KL 散度正则项。为增强多样性，在推理时通过切线空间噪声注入扰动潜码均值方向 $\boldsymbol{\mu}$：

$$\mathbf{z} = \mathrm{norm}((1 - \eta)\boldsymbol{\mu} + \eta \mathrm{norm}(\boldsymbol{\mu} + \sigma \boldsymbol{\xi}_{\perp}))$$

其中 $\boldsymbol{\xi}_{\perp}$ 为切线空间中的高斯噪声，$\eta$ 控制扰动强度，最终投影回单位球面。

- **ID-Mixer**：以原始身份嵌入与随机潜码 $\mathbf{z}$ 为条件，通过生成器 $G_{\phi}$ 映射得到虚拟身份嵌入 $\mathbf{e}_{vir} = G_{\phi}(\mathbf{e}_{ori}, \mathbf{z})$。其多任务训练损失为：

$$\mathcal{L} = \lambda_{\mathrm{ano}} \mathcal{L}_{\mathrm{ano}} + \lambda_{\mathrm{div}} \mathcal{L}_{\mathrm{div}} + \lambda_{\mathrm{intra}} \mathcal{L}_{\mathrm{intra}} + \lambda_{\mathrm{inter}} \mathcal{L}_{\mathrm{inter}} + \lambda_{\mathrm{reg}} \mathcal{L}_{\mathrm{reg}}$$

五项损失分别约束匿名性、多样性、类内一致性、类间分离和正则化，继承自 **IVFG**（Yuan et al., ACM MM 2022）的训练范式。

### 3.2 姿态与表情双分支条件注入

为保留原始人脸的姿态与表情信息，该方法构建了 EMOCA 与 SMIRK 协同的双分支条件体系，二者分工互补：

- **EMOCA 分支**：从输入人脸提取 3DMM 参数并渲染为法线图，通过 **ControlNet** 注入扩散 UNet，提供全局头部姿态与粗粒度几何约束。
- **SMIRK 分支**：提取高维表情编码，以 **IP-Adapter 风格**的方式映射为扩散 UNet 的交叉注意力条件，补充细粒度、高频的表情细节。

这种设计使 EMOCA 负责“骨架”级几何一致性，SMIRK 负责“肌肉”级表情生动性，二者联合覆盖从全局到局部的属性保留需求。

### 3.3 带水印的扩散生成

扩散生成模块以 Stable Diffusion 为骨干，接收三类条件：虚拟身份嵌入 $\mathbf{e}_{vid}$（身份控制）、法线图（姿态几何控制）、表情编码（表情细节控制）。去噪后的潜码 $\hat{\mathbf{z}}_0$ 进入 VAE 解码器时，额外嵌入一个 **128 位身份水印**。

水印由用户生物特征派生并经加密处理，在 VAE 解码阶段以隐式方式嵌入像素空间，后续可通过对称的解码器无损提取。该设计使水印与虚拟身份绑定，在不显著影响视觉质量的前提下实现可追溯的所有权验证。

## 实验与分析

### 实验设置总览

实验在 **CelebA-HQ** 与 **FFHQ** 两个数据集上进行评估，覆盖虚拟身份一致性、匿名性、多样性、面部实用性、姿态/表情保留以及水印真实性六个维度。所有身份相关指标均在三种不同的面部识别器（**ArcFace**、**FaceNet**、**AdaFace**）下独立评估，以避免单一识别器偏差。对比方法均遵循原始论文推荐设置或使用公开代码，确保公平比较。

### 虚拟身份一致性

虚拟身份一致性衡量同一用户的不同原始图像是否映射到稳定、可辨识的虚拟身份。核心指标为等错误率（EER↓）与曲线下面积（AUC↑），数值越低/越高表示虚拟身份越一致。

**Table 1** 展示了 CelebA-HQ 上的全面对比。本文提出的 **vMF** 与 **HS-AE** 采样器在 ArcFace 下达到 EER 0.002、AUC 1.000，远优于最佳基线 **RiDDLE**（Li et al., CVPR 2023）的 EER 0.046、AUC 0.757，差距分别为 −0.044 与 +0.243。**ID-Mixer** 采样器的 ArcFace EER 为 0.021，仍显著优于所有对比方法。在 AdaFace 下，HS-AE 的 EER 低至 0.001，进一步验证了跨识别器的鲁棒性。

这一压倒性优势的因果瓶颈在于：现有方法（如 **FALCO**、Barattin et al., CVPR 2023；**G²Face**、Yang et al., TIFS 2024）或依赖潜码优化，或依赖可逆变换，缺乏对虚拟身份嵌入空间的显式建模，导致跨实例身份漂移。本文的虚拟身份采样器直接在 ArcFace 超球面嵌入空间中对每个用户分配一个固定的虚拟身份方向，从根本上消除了漂移问题。

### 匿名性

匿名性衡量虚拟身份与原始身份的可关联程度。本文采用余弦相似度（CSim↓）与身份匿名化率（IAR↑）作为指标。

**Table 2** 显示，本文方法在 ArcFace 下的 IAR 达到 **1.000**，CSim 低至 0.034（ID-Mixer），表明生成的虚拟身份与原始身份完全无法关联。相比之下，**CIAGAN**（Maximov et al., CVPR 2020）和 **FIT**（Gu et al., ECCV 2020）等方法由于采用条件生成或可逆变换，其虚拟身份与原始身份间仍存在可检测的统计关联，IAR 明显低于本文。

### 多样性与实用性

**Table 3** 的多样性对比表明，本文方法在生成虚拟身份的类间多样性（Div）与整体多样性（ODV）上均具有竞争力。**Table 4** 的面部实用性评估涵盖 FID、FDR 等指标，本文方法在 FFHQ 与 CelebA-HQ 上均保持较低的 FID，证明生成人脸仍位于真实人脸流形内，未因匿名化而损失自然度。

### 姿态与表情保留

**Table 5** 展示了头部姿态误差（Pitch/Roll/Yaw Error↓）与表情相似度（Expression Similarity↑）的定量对比。本文方法在 FFHQ 上取得 Pitch Error 2.66、Roll Error 1.52、Yaw Error 2.30、表情相似度 0.863，在所有对比方法中全面领先。这一优势源于 **EMOCA + SMIRK** 双分支条件体系：EMOCA 通过法线图注入 ControlNet 提供全局几何与粗粒度表情约束，SMIRK 通过 IP-Adapter 风格注入补充细粒度、高频表情细节，两者互补实现了高保真属性保留。

### 水印嵌入与视觉质量

**Table 6** 展示了水印位准确率与嵌入后图像的视觉质量。水印位准确率达到 **0.998**，且嵌入水印后的图像 PSNR 为 39.74、SSIM 为 0.974，与无水印版本相比几乎无损。这一结果验证了轻量级身份绑定水印的可行性：在 VAE 解码阶段嵌入 128 位由生物特征衍生并加密的身份签名，既不影响视觉质量，又为每张虚拟人脸绑定了可验证的所有权签名。

### 消融实验

**Figure 5** 与 Sec. 4.6 的消融分析揭示了各组件的因果贡献：

- **移除虚拟身份采样器（w/o VID sampler）**：生成人脸偏离真实人脸流形，FID 显著恶化，身份一致性崩溃。这证明在嵌入空间中进行显式身份分配是维持虚拟身份稳定性的必要条件。
- **移除 EMOCA（w/o EMOCA）**：全局几何约束丢失，头部姿态保留能力下降，人脸出现不自然的朝向偏差。
- **移除 SMIRK（w/o SMIRK）**：虽然粗粒度表情仍由 EMOCA 部分保留，但细粒度表情（如嘴角弧度、眼睑细节）的生动性明显减弱，表情相似度下降。
- **水印模块对比（w/o watermarking vs. with watermarking）**：PSNR、SSIM 和 LPIPS 均无显著变化，证实水印嵌入对视觉质量的影响可忽略不计。

### 失败模式与局限性

尽管整体性能优异，方法仍存在以下已知局限：

1. **水印鲁棒性有限**：当前水印机制专为轻量级身份绑定设计，对强鲁棒性攻击（如对抗性扰动、高强度几何变换、重度压缩）的抵抗能力不足，不适用于高安全性取证场景。
2. **识别器依赖性**：HS-AE 与 ID-Mixer 的训练依赖于预训练人脸识别器的嵌入分布，可能继承原始识别器的偏差，在跨种族或非标准人脸数据上的泛化性需进一步验证。
3. **静态图像限制**：目前仅在静态人脸图像上验证，未涉及视频序列或动态表情变化，复杂姿态与大角度遮挡下可能产生伪影。
4. **扩散模型先验约束**：虚拟身份生成质量仍受限于底层 Stable Diffusion 的先验，极端条件下可能无法完全维持自然度。

### 补充图表

![[assets/figures/papers/paper_list_l842_https_openaccess_thecvf_com_content_CVPR2026_html_Zeng_Bridging_Privacy/figures/003_Table_1.jpg]]
*Table 1: Virtual identity consistency comparison on the CelebA-HQ test set across all baseline methods and our method*

![[assets/figures/papers/paper_list_l842_https_openaccess_thecvf_com_content_CVPR2026_html_Zeng_Bridging_Privacy/figures/005_Table_2.jpg]]
*Table 2: Anonymity comparison on the CelebA-HQ test set*

![[assets/figures/papers/paper_list_l842_https_openaccess_thecvf_com_content_CVPR2026_html_Zeng_Bridging_Privacy/figures/011_Table_6.jpg]]
*Table 6: Bit Accuracy and visual quality of our watermarked virtual faces on CelebA-HQ and FFHQ*

![[assets/figures/papers/paper_list_l842_https_openaccess_thecvf_com_content_CVPR2026_html_Zeng_Bridging_Privacy/figures/010_Table_5.jpg]]
*Table 5: Head pose and facial expression comparison of virtual faces generated by different methods on FFHQ and CelebA-HQ*

![[assets/figures/papers/paper_list_l842_https_openaccess_thecvf_com_content_CVPR2026_html_Zeng_Bridging_Privacy/figures/008_Figure_5.jpg]]
*Figure 5: Ablation study on our proposed framework*

![[assets/figures/papers/paper_list_l842_https_openaccess_thecvf_com_content_CVPR2026_html_Zeng_Bridging_Privacy/figures/009_Table_4.jpg]]
*Table 4: Face utility comparison of virtual faces generated by different methods on FFHQ and CelebA-HQ*

![[assets/figures/papers/paper_list_l842_https_openaccess_thecvf_com_content_CVPR2026_html_Zeng_Bridging_Privacy/figures/006_Table_3.jpg]]
*Table 3: Diversity comparison on the CelebA-HQ test set*

![[assets/figures/papers/paper_list_l842_https_openaccess_thecvf_com_content_CVPR2026_html_Zeng_Bridging_Privacy/figures/004_Figure_3.jpg]]
*Figure 3: Visual comparison of virtual faces generated by different methods including ours (rightmost) and original faces (leftmost)*

![[assets/figures/papers/paper_list_l842_https_openaccess_thecvf_com_content_CVPR2026_html_Zeng_Bridging_Privacy/figures/007_Figure_4.jpg]]
*Figure 4: Examples of virtual faces generated by our method. Each row shows three original faces of the same user (left) and their corresponding virtual faces (right)*

## 方法谱系与知识库定位

### 1. 问题定位：从匿名化到可追溯虚拟身份

本文解决的核心瓶颈在于：现有面部身份保护方法在**虚拟身份一致性**、**可控匿名性**与**可追溯的所有权验证**三个维度上无法兼得，导致虚拟身份在实际应用中要么出现身份漂移（同一用户的多次生成结果不一致），要么完全丧失问责能力。

现有方法可大致归为三类，各自存在结构性缺陷：

- **基于条件生成对抗网络的匿名化方法**，如 **CIAGAN**（Maximov et al., CVPR 2020），通过条件GAN修改面部属性以隐藏身份，但缺乏内生的虚拟身份一致性约束，同一用户多次生成的虚拟面容可能指向不同身份。
- **基于可逆变换的身份保护方法**，如 **FIT**（Gu et al., ECCV 2020）和 **RiDDLE**（Li et al., CVPR 2023），通过密码条件或可逆映射实现身份隐藏与恢复，但可逆性本身隐含了原始身份的可恢复风险，且未提供面向第三方的所有权验证机制。
- **基于生成先验的虚拟身份方法**，如 **IVFG**（Yuan et al., ACM MM 2022）、**FALCO**（Barattin et al., CVPR 2023）和 **G²Face**（Yang et al., TIFS 2024），利用GAN潜码优化或扩散先验生成虚拟面容，在身份一致性和视觉质量上有所提升，但均未内建可追溯的溯源机制，生成的虚拟身份一旦脱离系统便无法验证其归属。

本文的差异化贡献在于：**首次将轻量级身份绑定水印嵌入到扩散解码过程中**，在保持虚拟身份一致性和匿名性的同时，赋予每张生成的虚拟人脸可验证的所有权签名，从而将“隐私保护”与“可问责性”统一在同一框架内。

### 2. 方法谱系中的技术创新点

本文在扩散模型框架下引入了三个关键的技术改造，形成与现有工作的结构性差异：

**（1）虚拟身份采样器替代直接身份注入**

现有方法通常直接使用原始身份嵌入或其变换结果作为生成条件（如 IVFG 的映射网络），这导致虚拟身份与原始身份之间存在可学习的关联。本文提出三种虚拟身份采样策略——基于 von Mises-Fisher 分布的随机采样（vMF）、基于超球面自编码器的生成式采样（HS-AE）和基于条件身份混合的采样（ID-Mixer）——在预训练人脸识别器的超球面嵌入空间中生成与原始身份角度远离且实例间一致的虚拟身份嵌入。这一设计从源头上切断了原始身份与虚拟身份之间的可逆关联，是匿名性指标 IAR 达到 1.000 的结构性原因。

**（2）3D几何与表情的双分支条件体系**

不同于 **FALCO** 等方法的简单属性保留，本文联合 **EMOCA**（全局几何与粗粒度表情，通过 ControlNet 注入法线图）和 **SMIRK**（细粒度、高频表情，通过 IP-Adapter 风格注入）构建双分支条件。这一设计的因果逻辑在于：EMOCA 提供姿态和几何的结构性约束，确保生成的虚拟人脸在三维空间上与原始人脸对齐；SMIRK 补充高频表情细节，避免表情僵硬。消融实验证实，移除任一支路分别损害全局几何保留和表情生动性（Figure 5）。

**（3）VAE解码器内嵌身份水印**

这是本文区别于所有基线方法的根本性创新。在 Stable Diffusion 的 VAE 解码器阶段嵌入 128 位由用户生物特征派生并经加密的身份签名，后续可通过无损提取进行匹配验证。该设计的关键优势在于：水印嵌入与图像生成共享解码过程，不引入额外的后处理步骤，且对视觉质量几乎无影响（PSNR 39.74, SSIM 0.974，Table 6）。相比之下，**FAS**（Kung et al., WACV 2025）和 **DP2**（Hukkelås et al., WACV 2023）等方法仅关注匿名化本身，完全未涉及溯源机制。

### 3. 适用边界与局限

本文方法存在以下明确的适用边界，需在实际部署中审慎评估：

- **水印鲁棒性有限**：当前水印机制专为轻量级身份绑定设计，位准确率达 0.998 的测试条件为无损传输场景。对于对抗性扰动、高强度几何变换（如大角度旋转、透视变形）、图像压缩或二次编辑等攻击，水印的可提取性未经验证，不适用于高安全性取证场景。
- **依赖预训练识别器的嵌入分布**：HS-AE 与 ID-Mixer 的训练均以预训练人脸识别器（如 ArcFace）的超球面嵌入空间为基础，虚拟身份的质量和分布特性受原始识别器偏差的影响。若底层识别器对特定人群存在性能偏差，该偏差可能传导至虚拟身份采样。
- **静态图像验证为主**：当前实验仅在 CelebA-HQ 和 FFHQ 等静态图像数据集上进行，未涉及视频序列或动态表情变化。复杂姿态与大角度遮挡下可能产生伪影，跨帧身份一致性也未经验证。
- **扩散先验的固有限制**：虚拟身份生成质量受限于底层 Stable Diffusion 模型的先验分布，极端条件下（如罕见姿态、非自然光照）可能无法完全维持自然度。

### 4. 开放问题

以下问题指向该方向的潜在延伸空间：

1. **鲁棒水印机制**：如何提升嵌入水印的抗干扰能力，使其在 JPEG 压缩、裁剪、缩放、二次生成等常见变换后仍能可靠提取？可能的路径包括引入对抗训练或频域嵌入策略。
2. **视频扩展**：能否将本框架扩展至视频人脸生成，保持跨帧的虚拟身份一致性与水印可验证性？这需要解决时序一致性建模和高效水印嵌入/提取的联合优化问题。
3. **多模态泛化**：除人脸外，该框架的身份采样-水印嵌入范式是否可泛化至其他生物特征模态（如声纹、步态），实现多模态虚拟身份的统一溯源？
4. **自适应匿名强度**：虚拟身份采样策略如何根据应用场景自适应地平衡匿名强度、一致性与多样性？例如，在低风险社交场景与高风险金融场景下可能需要不同的匿名化配置。
5. **与差分隐私的形式化关联**：当前方法的匿名性通过经验指标（IAR、CSim）衡量，缺乏与差分隐私等形式化隐私框架的理论关联，这限制了其在合规要求严格场景下的可解释性。

## 原文 PDF

![[paperPDFs/CVPR_2026/Bridging_Privacy_and_Provenance_Traceable_Virtual_Identity_Generation.pdf]]