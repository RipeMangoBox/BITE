---
title: "When Lines Meet Textures: Spatial-Frequency Aligned Diffusion Features for Cross-Sparsity Correspondence"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/When_Lines_Meet_Textures_Spatial_Frequency_Aligned_Diffusion_Features_for_Cross_Sparsity_Correspondence.pdf
project_link: null
code_link: "https://github.com/Mofr77/SFA-DIFT"
aliases:
- SD
- WLMTSFADFCSC
tags:
- CVPR_2026
- topic/generative_models_diffusion
- topic/representation_self_supervised_transfer
- topic/generative_models_diffusion/diffusion_image_video
core_operator: 通过LoRA参数高效微调学习统一清洁扩散特征（空间对齐），并利用小波分解的低频特征聚合模块（频域对齐）来增强共享低频结构信息并抑制模态特异性高频噪声，实现空间-频率联合对齐。
primary_logic: 针对线条-纹理跨模态对应，关键在于同时进行空间域和频域的双重对齐：空间上通过LoRA微调将稀疏线条和丰富纹理映射到共享语义空间；频域上通过小波分解增强低频结构信息、抑制高频噪声，从而强调共有拓扑结构而非模态特有纹理。
claims:
- SFA-DIFT在PSC6K上PCK@1、5、10分别比次优方法提升0.87%、2.20%、0.95%，达到SOTA。
- SD特征在处理稀疏草图时出现“特征空洞”和噪声伪影，造成空间对应崩溃；SFA-DIFT显著改善了跨模态特征聚类（t-SNE按语义类聚而非模态类型）。
- 消融实验证实，LoFFA中AdaIN分布对齐、LoFE低频增强、显式小波变换及两级分解均为关键组件，移除任一项均导致性能下降。
- PSC6K 上 PCK@1 = 9.81
---

# When Lines Meet Textures: Spatial-Frequency Aligned Diffusion Features for Cross-Sparsity Correspondence

> [!tip] 核心洞察
> 针对线条-纹理跨模态对应，关键在于同时进行空间域和频域的双重对齐：空间上通过LoRA微调将稀疏线条和丰富纹理映射到共享语义空间；频域上通过小波分解增强低频结构信息、抑制高频噪声，从而强调共有拓扑结构而非模态特有纹理。

| 字段 | 内容 |
|------|------|
| 中文题名 | 当线条邂逅纹理：面向跨稀疏对应的空间-频率对齐扩散特征 |
| 英文题名 | When Lines Meet Textures: Spatial-Frequency Aligned Diffusion Features for Cross-Sparsity Correspondence |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://openaccess.thecvf.com/content/CVPR2026/html/Zhu_When_Lines_Meet_Textures_Spatial-Frequency_Aligned_Diffusion_Features_for_Cross-Sparsity_CVPR_2026_paper.html) · [Code](https://github.com/Mofr77/SFA-DIFT) |
| Topic | #topic/generative_models_diffusion #topic/representation_self_supervised_transfer #topic/generative_models_diffusion/diffusion_image_video |
| Method | SFA-DIFT |
| Dataset | PSC6K, MS-PSC6K |

> [!tip] 效果简介
> - PSC6K 上，PCK@1 9.81 vs 8.94 (previous best) (+0.87)；PCK@5 72.94 vs 70.74 (previous best) (+2.20)；PCK@10 92.70 vs 91.75 (previous best) (+0.95)。
> - MS-PSC6K (avg across 5 styles) 上，PCK@1 8.70 vs previous best (unspecified) (N/A)；PCK@5 69.21 vs previous best (unspecified) (N/A)；PCK@10 91.02 vs previous best (unspecified) (N/A)。

## 概要

**问题背景** 跨稀疏对应（cross-sparsity correspondence）旨在建立稀疏线条草图与丰富纹理图像之间的语义匹配，是图像编辑、三维重建等任务的基础。然而，扩散特征在这一跨模态场景中面临双重错位：空间域上，稀疏结构与密集纹理之间存在结构抽象差异；频域上，两种模态的纹理密度不一致导致特征频谱分布失配。现有方法仅关注空间对齐或语义级修补，未能有效弥合频域间隙，导致在草图上出现“特征空洞”和噪声伪影，跨模态特征按模态类型而非语义类别聚类（见 Figure 1）。

**核心方法** 本文提出 **SFA-DIFT**，一种学习空间-频率对齐扩散特征的方法。其关键创新在于双重域对齐：在空间域，通过 LoRA 参数高效微调将预训练的 **CleanDIFT**（Stracke et al., CVPR 2025）适配到草图数据，学习统一清洁扩散特征；在频域，设计低频特征聚合模块（LoFFA），利用两级离散小波变换增强共享低频结构信息，抑制模态特异的高频噪声，从而强调共有拓扑结构而非模态特有纹理。

**方法定位** SFA-DIFT 属于“特征空间对齐 + 频域增强”范式，区别于纯空间匹配的零样本方法（如 **SketchFusion**, Koley et al., CVPR 2025）和仅使用监督对比损失的基线。其技术谱系上承扩散特征提取（**SD**, Rombach et al., CVPR 2022）与参数高效微调（LoRA），横向融合小波频域分析，形成空间-频率联合对齐的新路径。

**主要结果** 在 PSC6K 数据集上，SFA-DIFT 在 PCK@1、PCK@5、PCK@10 上分别达到 9.81%、72.94%、92.70%，较此前最优方法分别提升 0.87、2.20、0.95 个百分点，达到 SOTA。在多风格扩展数据集 MS-PSC6K 上，平均 PCK@1 为 8.70%，同样取得最优。消融实验证实，LoFFA 中的 AdaIN 分布对齐、LoFE 低频增强、显式小波变换及两级分解均为关键组件，移除任一项均导致性能下降。此外，SFA-DIFT 在纹理扰动下的鲁棒性比率（RR）显著优于对比方法，验证了频域对齐对纹理变化不敏感的优势。

**局限与展望** 当前方法的主要瓶颈在于推理效率：由于依赖扩散特征提取，每次对应估计平均耗时约 0.8 秒，难以满足实时应用需求。未来方向包括探索更高效的扩散特征表示或轻量化模型，以及在更多样化类别和大规模数据集上验证泛化能力。

### 跨稀疏对应的核心挑战

视觉对应（visual correspondence）是计算机视觉的基础任务，旨在建立不同图像间像素或关键点的语义匹配关系。传统方法主要关注同模态图像间的对应，如照片到照片或草图到草图的匹配。然而，现实应用中更常见的是**跨稀疏对应**（cross-sparsity correspondence）——在稀疏线条（如手绘草图、线稿）与丰富纹理（如自然照片、艺术渲染图）之间建立精确的语义对应。这一任务面临独特的双重困境：

**空间域的结构抽象差异。** 草图以稀疏的轮廓线条勾勒物体形状，而纹理图像则包含密集的颜色、光照和材质信息。这种模态间的信息密度不对称导致特征表示在空间域上出现系统性偏差。如Figure 2所示，**Stable Diffusion (SD)**（Rombach et al., CVPR 2022）在处理稀疏草图时会产生显著的“特征空洞”和噪声伪影，使得空间对应关系趋于崩溃。t-SNE可视化（Figure 1(b)）进一步揭示了这一偏差：SD的跨模态特征按模态类型而非语义类别聚类，表明其未能建立有效的跨模态语义桥梁。

**频域的纹理密度不一致。** 从频域视角分析，稀疏草图以低频轮廓信息为主导，而纹理图像则包含丰富的高频细节。现有方法（如**CleanDIFT**, Stracke et al., CVPR 2025；**SketchFusion**, Koley et al., CVPR 2025）虽在空间对齐或语义级修补上有所改进，但均未显式处理频域间隙。Figure 2的频谱分析显示，即使经过空间对齐的特征，其频域分布仍存在显著的模态特异性差异——草图的低频成分与纹理图像的高频噪声难以有效融合，导致跨模态匹配的鲁棒性不足。

### 现有方法的局限

当前跨模态对应方法可大致分为两类：

- **零样本方法**（如CleanDIFT、SketchFusion）利用预训练扩散模型或CLIP的特征空间进行匹配，无需专门训练。它们在一定程度上缓解了空间域偏差，但由于缺乏对草图稀疏特性的针对性适应，在稀疏区域的对应精度仍然有限。

- **有监督方法**通过标注数据进行端到端训练，虽然提升了精度，但通常仅关注空间域的特征对齐，忽略了频域中低频结构信息与高频模态噪声的本质差异。

### 本文动机：空间-频率双重对齐

上述分析表明，**扩散特征在稀疏线条与丰富纹理之间存在空间域结构抽象差异和频域纹理密度不一致的双重错位**，这是导致跨模态语义对应失败的根本瓶颈。仅进行空间对齐或语义级修补无法有效弥合频域间隙，因为即使空间上对齐的特征，其频域分布仍保留着模态特有的高频伪影，干扰匹配过程。

基于这一洞察，本文提出**SFA-DIFT**（Spatial-Frequency Aligned Diffusion Features），核心思路是进行**空间域与频域的联合对齐**：

- **空间域**：通过参数高效的LoRA微调，将稀疏线条和丰富纹理映射到统一的共享语义空间，消除模态间的结构抽象差异。
- **频域**：引入小波分解的低频特征聚合模块，增强共享的低频结构信息（如物体轮廓和拓扑关系），同时抑制模态特异性的高频噪声，从而强调共有拓扑结构而非模态特有纹理。

这种双重对齐策略从根本上解决了跨稀疏对应的核心矛盾——让线条与纹理在统一的特征空间中“相遇”，实现鲁棒且精确的语义匹配。

## 核心方法与创新机理

SFA-DIFT 的核心创新在于首次将**空间域**与**频域**的双重对齐引入跨稀疏对应任务，解决了扩散特征在处理稀疏线条与丰富纹理时出现的“特征空洞”和模态特异性噪声问题。与现有方法仅关注空间语义对齐或语义级修补不同，SFA-DIFT 通过两个关键模块实现空间-频率联合对齐：

**空间域对齐：统一清洁扩散特征学习。** 以 **CleanDIFT**（Stracke et al., CVPR 2025）为零样本基线，SFA-DIFT 采用参数高效的 **LoRA** 微调策略，在草图数据上进行无监督训练。LoRA 通过低秩矩阵 $A, B$ 和缩放因子 $\alpha$ 更新预训练权重 $W' = W + \alpha B A$，使模型在保持预训练知识的同时，将稀疏线条和丰富纹理映射到共享语义空间。训练采用教师-学生框架，以负余弦相似度损失对齐投影特征与目标特征，从而弥合空间域的结构抽象差异。

**频域对齐：低频特征聚合模块（LoFFA）。** 这是 SFA-DIFT 区别于所有 baseline 的关键 changed slot。LoFFA 对统一清洁扩散特征和 DINOv2 辅助特征进行两级离散小波变换（DWT），分解为低频子带 $F_{\mathrm{LL}}$ 和高频子带 $F_{\mathrm{H}}$。核心操作是通过 Sigmoid 门控调制 $\tilde{F}_{\mathrm{LL}}^{S,(2)} = F_{\mathrm{LL}}^{S,(2)} \odot (\mathbf{1} + \mathcal{M})$ 选择性增强共享低频结构信息，同时抑制模态特异性的高频纹理噪声。模块内还集成了 AdaIN 分布对齐和可学习标量 $\beta$ 控制的残差连接 $F_l^{S,\mathrm{out}} = F_l^{S,\mathrm{in}} + \beta(\mathcal{H}(F_l^{S,\mathrm{in}}) - F_l^{S,\mathrm{in}})$，确保训练稳定性。

**损失函数创新。** SFA-DIFT 联合 CLIP 风格的对称对比损失 $\mathcal{L}_{\mathrm{CL}}$ 与带有高斯噪声正则的密集匹配损失 $\mathcal{L}_{\mathrm{Dense}}$，总损失为 $\mathcal{L} = \mathcal{L}_{\mathrm{CL}} + \mathcal{L}_{\mathrm{Dense}}$，替代了传统的关键点对比损失或端点误差（EPE）。

**因果机制总结：** 空间 LoRA 微调解决“特征空洞”和模态聚类偏差，频域 LoFFA 解决频谱密度不一致——两者协同使特征按语义类而非模态类型聚类（t-SNE 可视化验证），从而在 PSC6K 上 PCK@1、5、10 分别达到 9.81%、72.94%、92.70%，较次优方法提升 0.87%、2.20%、0.95%。消融实验证实，移除 AdaIN、将 LoFE 替换为普通卷积、用卷积替代 DWT/IDWT、或使用单级 DWT 均导致性能下降，验证了分布对齐、低频增强、显式频率变换和深度频率分解均为必要组件。

SFA-DIFT 的整体流程围绕“空间-频率双重对齐”这一核心思想展开，旨在解决稀疏线条（sketch）与丰富纹理（textured image）之间的跨模态语义对应问题。该框架采用两阶段级联设计：第一阶段通过参数高效微调构建统一清洁扩散特征提取器，实现空间域对齐；第二阶段引入低频特征聚合模块，实现频域对齐。

### 两阶段流水线

**第一阶段：统一清洁扩散特征学习。** 以预训练的 **CleanDIFT**（Stracke et al., CVPR 2025）为骨干，通过 **LoRA**（Low-Rank Adaptation）对草图数据进行无监督微调。微调采用教师-学生框架：教师网络处理加噪的纹理图像，学生网络处理干净的草图，通过自适应对齐损失（负余弦相似度）拉近两者在多个特征层的投影特征。此阶段的目标是将稀疏线条和丰富纹理映射到共享的语义空间，弥合空间域的结构抽象差异。

**第二阶段：低频特征聚合。** 冻结第一阶段得到的统一 CleanDIFT 提取器，将其多尺度特征与 **DINOv2**（Oquab et al., arXiv 2023）的辅助特征一同送入 **LoFFA**（Low-Frequency Feature Aggregation）模块。LoFFA 对每个尺度的特征执行两级离散小波变换（DWT），分离出低频子带（LL）和高频子带，通过 sigmoid 门控调制选择性增强低频结构信息，同时抑制模态特异性的高频噪声。增强后的特征经逆小波变换（IDWT）重建，并通过可学习标量加权的残差连接与原始特征融合，保证训练稳定性。

### 模块关系与数据流

整个框架的输入是一对草图-纹理图像，输出是密集的跨模态语义对应。

1. **统一 CleanDIFT 提取器**：接收草图和纹理图像，输出多尺度扩散特征 $\boldsymbol{F}^S$ 和 $\boldsymbol{F}^T$。该提取器内部的 UNet 注意力层注入了 LoRA 低秩矩阵，仅需训练极少参数即可适应草图模态。
2. **DINOv2 辅助分支**：并行提取纹理图像的多尺度视觉特征，为 LoFFA 提供互补的结构先验。
3. **LoFFA 模块**：对每个尺度的草图特征和纹理特征分别执行两级 DWT 分解 → 低频增强（LoFE 子模块） → IDWT 重建 → 残差融合。模块内还包含 AdaIN 分布对齐，用于归一化跨模态特征的统计分布差异。
4. **投影头**：时间步条件化的逐点投影层，将学生网络特征投影到与教师网络时变特征对齐的空间，服务于第一阶段的对比学习。
5. **损失函数**：第一阶段使用自适应对齐损失 $\mathcal{L}_{\mathrm{ada}}$；第二阶段联合 CLIP 风格的对称对比损失 $\mathcal{L}_{\mathrm{CL}}$ 与带有高斯噪声正则的密集匹配损失 $\mathcal{L}_{\mathrm{Dense}}$，总损失为 $\mathcal{L} = \mathcal{L}_{\mathrm{CL}} + \mathcal{L}_{\mathrm{Dense}}$。

### 设计逻辑

该两阶段设计的因果逻辑在于：空间域对齐（LoRA 微调）解决的是“特征空洞”和模态特异性聚类问题——预训练 SD 特征在处理稀疏草图时会产生噪声伪影，导致 t-SNE 可视化中按模态分簇而非按语义分簇（见 Figure 1b 左侧）。频域对齐（LoFFA）则进一步解决纹理密度不一致导致的频域间隙——草图的频谱能量集中于低频，而纹理图像的高频分量丰富，直接匹配会产生错位。通过两级小波分解增强共享的低频结构信息，SFA-DIFT 使得跨模态特征在频域也趋于一致（见 Figure 4 的频谱对比），从而实现鲁棒的跨稀疏对应。

> **注意**：关于 LoFFA 内部 AdaIN 的具体插入位置、DINOv2 特征的融合方式、以及投影头的详细架构，建议结合原文 Section 3 及 Figure 3 进行确认。

![[assets/figures/papers/paper_list_l2629_https_openaccess_thecvf_com_content_CVPR2026_html_Zhu_When_Lines_Meet_Te/figures/003_Figure_3.jpg]]
*Figure 3: Our SFA-DIFT framework first creates a Unified CleanDIFT extractor via LoRA fine-tuning, and then uses its frozen features to train a Low-Frequency Feature Aggregation (LoFFA) module that amplifies low-frequency components for robust correspondence*

### 3.1 统一清洁扩散特征学习（空间域对齐）

SFA-DIFT的空间域对齐建立在**CleanDIFT**（Stracke et al., CVPR 2025）预训练特征提取器之上，通过参数高效微调策略弥合稀疏线条与丰富纹理之间的语义鸿沟。核心机制如下：

**LoRA参数高效微调**。给定预训练权重矩阵 $W \in \mathbb{R}^{d \times d}$，引入低秩分解：

$$W' = W + \alpha B A \tag{1}$$

其中 $B \in \mathbb{R}^{d \times r}$、$A \in \mathbb{R}^{r \times d}$ 为可训练低秩矩阵（秩 $r \ll d$），$\alpha$ 为缩放因子。该设计仅需更新极少量参数即可使扩散特征提取器适应草图模态，无需大规模有监督标注。

**教师-学生自适应对齐**。训练采用双路前向传播框架：教师网络以带噪纹理图像 $x_t$ 为输入提取时变扩散特征 $F_{\text{target}}^{(k)}(x_t, t)$；学生网络以清洁草图 $x_0$ 为输入，经可训练投影头映射至与教师特征对齐的空间 $F_{\text{proj}}^{(k)}(x_0, t')$。自适应对齐损失为负余弦相似度：

$$\mathcal{L}_{\mathrm{ada}} = \mathbb{E}_{x_0,\epsilon,t}\left[-\sum_{k=1}^{K}\frac{F_{\mathrm{proj}}^{(k)}(x_0,t')\cdot F_{\mathrm{target}}^{(k)}(x_t,t)}{\|F_{\mathrm{proj}}^{(k)}(x_0,t')\|\|F_{\mathrm{target}}^{(k)}(x_t,t)\|}\right] \tag{2}$$

其中 $K$ 为对齐的特征层数，$t$ 为扩散时间步，$t'$ 为投影头条件时间步。该损失强制学生网络在无监督条件下学习将稀疏草图映射至与纹理图像共享的语义空间，从而消除“特征空洞”和模态特异性聚类（参见 Figure 1(b) 的 t-SNE 对比）。

![[assets/figures/papers/paper_list_l2629_https_openaccess_thecvf_com_content_CVPR2026_html_Zhu_When_Lines_Meet_Te/figures/001_Figure_1.jpg]]
*Figure 1: Cross-sparsity correspondence examples and feature visualization. (a) Representative cross-sparsity correspondence examples from extended MS-PSC6K. (b) t-SNE [20] visualization comparing cross-modal features from Stable Diffusion (SD) and our SFA-DIFT method. Best viewed when zoomed in*

### 3.2 低频特征聚合模块（频域对齐）

空间对齐后的特征仍存在频域错位——草图特征缺乏纹理图像的高频细节而富含结构化低频信息。LoFFA模块通过两级离散小波变换（DWT）选择性增强共享低频结构，抑制模态特异性高频噪声。

**多尺度特征输入**。模块接收来自统一CleanDIFT提取器和DINOv2（Oquab et al., arXiv 2023）的 $L$ 层多尺度特征 $\boldsymbol{F}^{S} = \{F_l^{S}\}_{l=1}^{L}$（草图）和 $\boldsymbol{F}^{T} = \{F_l^{T}\}_{l=1}^{L}$（纹理）。

**一级小波分解**。对每层特征 $F_l^{S,\mathrm{in}}$ 进行DWT：

$$F_{\mathrm{LL},l}^{S,(1)}, F_{\mathrm{H},l}^{S,(1)} = \mathrm{DWT}(F_l^{S,\mathrm{in}}) \tag{3}$$

得到低频子带 $F_{\mathrm{LL},l}^{S,(1)}$ 和高频子带 $F_{\mathrm{H},l}^{S,(1)}$。低频子带保留全局拓扑结构，高频子带编码纹理细节。

**二级分解与门控增强**。对一级低频子带再次进行DWT，获得更深层低频分量 $F_{\mathrm{LL},l}^{S,(2)}$。引入可学习注意力掩码 $\mathcal{M}$ 进行 sigmoid 门控调制：

$$\tilde{F}_{\mathrm{LL},l}^{S,(2)} = F_{\mathrm{LL},l}^{S,(2)} \odot (\mathbf{1} + \mathcal{M}) \tag{5}$$

其中 $\odot$ 表示逐元素乘法。该机制自适应增强对跨模态对应关键的低频结构信息。

**分布对齐与残差连接**。在LoFFA内部，通过AdaIN（自适应实例归一化）将草图特征的统计分布对齐至纹理特征，消除模态间分布偏移。最终输出经可学习标量 $\beta$ 缩放的残差连接：

$$F_l^{S,\mathrm{out}} = F_l^{S,\mathrm{in}} + \beta(\mathcal{H}(F_l^{S,\mathrm{in}}) - F_l^{S,\mathrm{in}}) \tag{6}$$

其中 $\mathcal{H}(\cdot)$ 表示完整的LoFE（低频增强）子模块处理。残差结构确保训练稳定性，$\beta$ 初始化为零使模块逐步学习频域增强。

### 3.3 训练目标

SFA-DIFT的最终训练损失联合对比损失与密集匹配损失：

$$\mathcal{L} = \mathcal{L}_{\mathrm{CL}} + \mathcal{L}_{\mathrm{Dense}} \tag{10}$$

**对比损失** $\mathcal{L}_{\mathrm{CL}}$ 采用对称CLIP风格损失，在特征空间拉近匹配的草图-纹理对、推远非匹配对，强化跨模态语义一致性。

**密集匹配损失** $\mathcal{L}_{\mathrm{Dense}}$ 在像素级关键点坐标上施加高斯噪声正则化：

$$\mathcal{L}_{\mathrm{Dense}} = \sum_{i} \left\| \hat{k}_i^{\mathrm{T}} - (k_i^{\mathrm{T}} + \epsilon) \right\|_2 \tag{9}$$

其中 $\hat{k}_i^{\mathrm{T}}$ 为预测纹理关键点，$k_i^{\mathrm{T}}$ 为真值，$\epsilon \sim \mathcal{N}(0, \sigma^2)$ 为小方差高斯噪声。噪声正则化的作用在于防止模型过拟合到精确坐标，提升对纹理变化的鲁棒性（参见 Table 3 的鲁棒性比率评估）。

### 3.4 关键设计决策与消融验证

消融实验（Table 4）揭示了各组件的因果贡献：

- **移除AdaIN分布对齐**：性能显著下降，验证了跨模态特征分布对齐的必要性。
- **LoFE替换为普通卷积**：低频增强能力丧失，证明小波分解的选择性频率处理不可替代。
- **DWT/IDWT替换为卷积**：显式频率变换的缺失导致频域对齐失败，说明隐式学习无法有效分离高低频分量。
- **单级DWT替代两级分解**：深层频率分解对提取共享低频结构至关重要，浅层分解不足以抑制高频噪声。

这些消融结果共同证实了SFA-DIFT的核心洞察：**空间-频率联合对齐是实现鲁棒跨稀疏对应的必要条件**，任一维度的缺失都将导致性能退化。

## 实验与关键发现

### 核心问题与评估基准

本方法聚焦于**跨稀疏对应（Cross-Sparsity Correspondence）**任务——在稀疏线条（草图）与丰富纹理（自然/艺术图像）之间建立精确的语义对应。评估在两个基准上进行：

- **PSC6K**：标准的照片-草图对应数据集，包含6,000对图像。
- **MS-PSC6K**：本文扩展的多风格数据集，覆盖Abstract、Baroque、Realism、Post-Imp、Neo-Imp五种艺术风格，用于评估跨纹理变化的泛化能力。

评估指标采用**PCK@α**（Percentage of Correct Keypoints），即预测关键点落在真实位置α倍边界框尺寸范围内的百分比，α取1、5、10。

### 主实验结果

#### PSC6K数据集

Table 1展示了SFA-DIFT与现有方法的定量对比。SFA-DIFT在所有指标上均达到SOTA：

- **PCK@1**：9.81%，较次优方法（8.94%）提升0.87个百分点。
- **PCK@5**：72.94%，较次优方法（70.74%）提升2.20个百分点。
- **PCK@10**：92.70%，较次优方法（91.75%）提升0.95个百分点。

值得注意的是，零样本方法（如**CleanDIFT**（Stracke et al., CVPR 2025）和**SketchFusion**（Koley et al., CVPR 2025））在PCK@1上普遍低于5%，而有监督方法可达到8%以上。SFA-DIFT作为有监督方法，进一步将这一指标推近10%，表明空间-频率联合对齐策略有效弥合了草图的稀疏性与照片的丰富纹理之间的语义鸿沟。

#### MS-PSC6K数据集

Table 2展示了跨五种艺术风格的性能。SFA-DIFT在五种风格上的平均结果为：

- **PCK@1**：8.70%
- **PCK@5**：69.21%
- **PCK@10**：91.02%

三项指标均刷新SOTA。相比PSC6K，MS-PSC6K上的PCK@1下降约1.11个百分点，这反映了艺术风格化纹理引入的额外域差异。但PCK@10仍维持在91%以上，说明SFA-DIFT在宽松阈值下保持了强鲁棒性。该结果验证了频域低频增强模块（LoFFA）在抑制风格特异性高频噪声、保留共享拓扑结构方面的有效性。

### 鲁棒性分析

Table 3报告了**鲁棒性比率（Robustness Ratio, RR）**，定义为纹理扰动后PCK与原始PCK的比值：

$$\mathrm{RR} := \frac{\frac{1}{N}\sum_{i=1}^{N}\mathrm{PCK}(x_i^s,\hat{x}_i^{t,\mathrm{pert}})}{\frac{1}{N}\sum_{i=1}^{N}\mathrm{PCK}(x_i^s,\hat{x}_i^{t,\mathrm{orig}})}$$

RR越接近1.0，表明方法对纹理变化越不敏感。SFA-DIFT在所有方法中取得了最高的RR值，证实了频域对齐策略有效抑制了纹理扰动引入的高频噪声，使对应估计更依赖于稳定的低频结构信息而非易变的表面纹理。

### 消融实验

Table 4通过组件消融验证了各模块的贡献。关键发现如下：

1. **基线方法（UCD+Conv）**：仅使用统一清洁扩散特征（Unified CleanDIFT）加普通卷积，无频域模块。性能显著低于完整SFA-DIFT，验证了频域处理的必要性。
2. **移除AdaIN（LoFFA w/o AdaIN）**：去除分布对齐子模块后性能下降，证实了跨模态特征分布对齐的重要性。
3. **LoFE替换为普通卷积（LoFE→Conv）**：将低频增强子模块替换为标准卷积，性能明显降低，说明显式的低频增强策略不可替代。
4. **DWT/IDWT替换为卷积（DWT/IDWT→Conv）**：用卷积替代离散小波变换及其逆变换，性能下降，验证了显式频域分解的价值。
5. **单级DWT（Single DWT/IDWT）**：仅使用一级小波分解而非两级，性能低于完整模型，表明深层频率分解对充分分离低频结构信息与高频噪声至关重要。

上述消融一致表明：**分布对齐（AdaIN）、低频增强（LoFE）、显式频率变换（DWT/IDWT）和深度频率分解（两级DWT）** 均为关键设计，移除任一项均导致性能损失。

### 定性分析

**Figure 5**展示了跨稀疏对应的定性结果。SFA-DIFT在草图到纹理和纹理到草图的双向匹配中均表现出色，能够在纹理剧烈变化的情况下准确定位对应点。相比之下，基线方法在纹理复杂区域常出现错误匹配或定位漂移，尤其在纹理边缘和重复图案区域失效明显。

**Figure 4**的渐进式特征优化分析进一步揭示了LoFFA的作用机制：PCA可视化显示，加入LoFFA后，草图和纹理图像的特征在空间域上呈现更一致的语义布局；频谱分析则表明，LoFFA有效增强了低频分量并抑制了高频噪声，使跨模态特征的频域分布趋于一致。

### 失败模式与局限性

尽管SFA-DIFT在精度和鲁棒性上表现优异，但存在以下局限：

- **推理延迟**：扩散特征提取导致每次对应估计平均耗时约0.8秒，限制了实时或大规模应用场景。该瓶颈源于扩散模型的多步去噪过程，而非LoFFA模块本身。
- **极端纹理退化**：当纹理图像遭受严重模糊或大尺度遮挡时，低频结构信息本身受损，LoFFA的增强效果有限，对应精度下降明显。此场景下需结合更强的空间先验或外部知识。
- **跨类别泛化**：当前评估集中在PSC6K的有限类别上，该方法在更多样化类别和更大规模数据集上的泛化能力尚未充分验证，需进一步实验确认。

### 补充图表

![[assets/figures/papers/paper_list_l2629_https_openaccess_thecvf_com_content_CVPR2026_html_Zhu_When_Lines_Meet_Te/figures/005_Table_1.jpg]]
*Table 1: Quantitative comparison with state-of-the-art methods on PSC6K datasets. ∗ indicates zero-shot methods. ‡ indicates supervised methods*

![[assets/figures/papers/paper_list_l2629_https_openaccess_thecvf_com_content_CVPR2026_html_Zhu_When_Lines_Meet_Te/figures/006_Table_2.jpg]]
*Table 2: Quantitative comparison with state-of-the-art methods on MS-PSC6K datasets. Performance is evaluated across five artistic styles (Abstract, Baroque, Realism, Post-Imp, Neo-Imp). ∗ indicates zero-shot methods. ‡ indicates supervised methods*

![[assets/figures/papers/paper_list_l2629_https_openaccess_thecvf_com_content_CVPR2026_html_Zhu_When_Lines_Meet_Te/figures/007_Figure_5.jpg]]
*Figure 5: Qualitative cross-sparsity correspondence comparison. Each row demonstrates cross-sparsity correspondence results between sketches and various textured images. Methods (a), (b), and (c) represent different approaches. For each method, we present correspondence results using both sketch-to-texture and texture-to-sketch configurations to evaluate bidirectional correspondence performance. SFA-DIFT achieves superior accuracy and robustness*

![[assets/figures/papers/paper_list_l2629_https_openaccess_thecvf_com_content_CVPR2026_html_Zhu_When_Lines_Meet_Te/figures/009_Table_4.jpg]]
*Table 4: Ablation study. Quantitative analysis of method variants. ∗ indicates zero-shot methods. ‡ indicates supervised methods*

## 定位与知识库关联

### 任务定位与核心瓶颈

SFA-DIFT 聚焦于**跨稀疏对应**任务——在稀疏线条草图与丰富纹理图像之间建立语义关键点对应。该任务的核心瓶颈在于双重错位：空间域上，稀疏线条的结构抽象与纹理图像的密集细节存在特征分布差异；频域上，纹理模态特有的高频信息与草图模态的低频结构之间存在不一致。现有方法或仅关注空间对齐，或仅进行语义级修补，未能有效弥合频域间隙，导致跨模态对应失败。

### 方法谱系与基线关系

#### 扩散特征提取基线

SFA-DIFT 建立在扩散特征提取方法的基础之上。**Stable Diffusion (SD)**（Rombach et al., CVPR 2022）作为基础扩散特征提取器，在处理稀疏草图时会产生“特征空洞”和噪声伪影，导致空间对应崩溃。**CleanDIFT**（Stracke et al., CVPR 2025）通过去除扩散特征中的噪声成分，改善了特征质量，但未针对草图模态进行适应，仍存在模态偏差。SFA-DIFT 以 CleanDIFT 为骨干，通过 LoRA 无监督微调学习统一清洁扩散特征，弥补了草图理解的不足。

#### 跨模态对齐基线

**SketchFusion**（Koley et al., CVPR 2025）利用 CLIP 对齐草图和照片特征，属于零样本方法，但在频域上仍存在纹理密度不一致的问题。SFA-DIFT 与之不同，不仅进行空间域对齐，还引入显式频域对齐机制。此外，SFA-DIFT 借助 **DINOv2**（Oquab et al., arXiv 2023）作为辅助视觉特征提取器，为 LoFFA 模块提供多尺度特征。

#### 消融基线

UCD+Conv 作为监督训练基线，仅使用统一清洁扩散特征加普通卷积，无频域模块。消融实验表明，该基线性能显著低于完整 SFA-DIFT，验证了频域对齐的必要性。

### 核心因果机制

SFA-DIFT 的因果调控旋钮在于**空间-频率联合对齐**：

1. **空间域对齐**：通过 LoRA 参数高效微调，将稀疏线条和丰富纹理映射到共享语义空间。训练采用教师-学生框架，学生网络以无噪声图像为输入预测教师网络在加噪条件下的时变特征，通过负余弦相似度损失实现自适应对齐。

2. **频域对齐**：LoFFA 模块利用两级离散小波变换（DWT）分解多尺度特征，选择性增强低频子带（LL 分量）并抑制高频噪声。核心机制包括：AdaIN 分布对齐消除模态间统计差异；LoFE 子模块通过 sigmoid 门控调制增强最低频子带；可学习标量残差连接保证训练稳定。

3. **联合优化**：训练损失联合 CLIP 风格对称对比损失与带有高斯噪声正则的密集匹配损失，同时优化特征表示和对应精度。

### 适用边界

- **输入模态**：适用于稀疏线条草图与纹理图像之间的对应，对草图抽象程度和纹理风格变化具有一定鲁棒性（MS-PSC6K 涵盖五种艺术风格）。
- **任务范围**：当前聚焦于语义关键点对应，未涉及密集像素级匹配或全景分割等任务。
- **计算约束**：扩散特征提取导致推理耗时较长（平均每次约 0.8 秒），限制了实时或大规模应用场景。

### 局限与开放问题

#### 已知局限

1. **推理效率**：扩散特征提取的多步前向传播导致推理延迟较高，不适用于实时应用。未来可探索更高效的扩散特征表示或轻量化模型。
2. **泛化边界**：当前实验仅在 PSC6K 和 MS-PSC6K 上进行，对更多样化类别和更大规模数据集的泛化能力尚待验证。

#### 开放问题

1. **效率-精度权衡**：如何在保持空间-频率对齐效果的同时显著降低推理延迟？知识蒸馏或特征缓存策略是否可行？
2. **跨域泛化**：该方法对草图-照片跨模态对应任务在更多样化的类别（如细粒度物种、人造物体）上的泛化能力如何？是否需要域适应或增量学习？
3. **频域机制的可解释性**：小波分解的层级选择与任务性能之间存在何种定量关系？不同层级的小波子带对语义对应和纹理抑制的贡献是否有明确的功能分工？

## 原文 PDF

![[paperPDFs/CVPR_2026/When_Lines_Meet_Textures_Spatial_Frequency_Aligned_Diffusion_Features_for_Cross_Sparsity_Correspondence.pdf]]
