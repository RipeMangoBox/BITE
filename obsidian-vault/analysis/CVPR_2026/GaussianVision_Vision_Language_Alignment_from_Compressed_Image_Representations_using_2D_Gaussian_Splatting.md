---
title: "GaussianVision: Vision-Language Alignment from Compressed Image Representations using 2D Gaussian Splatting"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/GaussianVision_Vision_Language_Alignment_from_Compressed_Image_Representations_using_2D_Gaussian_Splatting.pdf
project_link: null
code_link: "https://github.com/LAION-AI/CLIP_benchmark"
aliases:
- G2AC
- GaussianVision
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/representation_self_supervised_transfer
- topic/benchmarks_datasets_evaluation
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: 将图像表示为紧凑的、自适应空间分布的二维高斯泼溅参数，替代原始RGB像素作为视觉编码器的输入。
primary_logic: 通过结构化初始化、亮度感知剪枝和批量CUDA核加速的2DGS拟合，可利用少量可训练的GS stem将压缩的高斯表示映射到与预训练RGB ViT兼容的嵌入空间，实现高效视觉-语言对齐。
claims:
- 3136点GS模型在压缩3倍的情况下达到RGB基线96-98%的相对零样本准确率。
- 对GS-1600进行RGB渲染再训练的ViT准确率下降程度与直接使用GS表示训练CLIP的下降程度几乎一致，表明当前GS编码器的性能上限受到压缩RGB重建质量的制约。
- CLIP Benchmark (38 datasets) 上 Relative Accuracy vs RGB Baseline = GS 3136 (196 tokens)
- CLIP Benchmark (38 datasets) 上 Compression Ratio = 3× (3136 GS)
---

# GaussianVision: Vision-Language Alignment from Compressed Image Representations using 2D Gaussian Splatting

> [!tip] 核心洞察
> 通过结构化初始化、亮度感知剪枝和批量CUDA核加速的2DGS拟合，可利用少量可训练的GS stem将压缩的高斯表示映射到与预训练RGB ViT兼容的嵌入空间，实现高效视觉-语言对齐。

| 字段 | 内容 |
|------|------|
| 中文题名 | GaussianVision：利用二维高斯泼溅从压缩图像表示进行视觉-语言对齐 |
| 英文题名 | GaussianVision: Vision-Language Alignment from Compressed Image Representations using 2D Gaussian Splatting |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2509.22615) · [Code](https://github.com/LAION-AI/CLIP_benchmark) |
| Topic | #topic/vision_multimodal_applications #topic/representation_self_supervised_transfer #topic/benchmarks_datasets_evaluation #topic/vision_multimodal_applications/image_and_video_generation |
| Method | GaussianVision (2DGS-adapted CLIP) |
| Dataset | CLIP Benchmark |

> [!tip] 效果简介
> - CLIP Benchmark (38 datasets) 上，Relative Accuracy vs RGB Baseline GS 3136 (196 tokens) vs RGB ViT-B/16 (Small) (0.98 (98% of baseline))；Compression Ratio 3× (3136 GS) vs 1× (RGB) (3× reduction)；Relative Accuracy GS 400 (196 tokens) vs RGB ViT-B/16 (Small) (0.91 (91% at 23.5× compression))。

## 概要

当前多模态视觉-语言模型通常以密集的RGB像素图像作为输入，通过分块（patch）得到大量视觉token，再与文本嵌入对齐。这种流程在边缘-云协同场景下面临两个核心瓶颈：**密集RGB图像的传输能耗高**，以及**基于patch的tokenization产生大量冗余token，制约模型的可扩展性与效率**。

**GaussianVision** 针对上述瓶颈提出一个关键的因果调节变量：**将图像表示为紧凑的、自适应空间分布的二维高斯泼溅（2D Gaussian Splatting, 2DGS）参数，替代原始RGB像素作为视觉编码器的输入**。其核心洞察在于：通过结构化初始化、亮度感知剪枝和批量CUDA核加速的2DGS拟合，可利用少量可训练的GS stem将压缩的高斯表示映射到与预训练RGB ViT兼容的嵌入空间，从而实现高效的视觉-语言对齐。

该方法在方法谱系中处于**视觉表示压缩与对比语言-图像预训练（CLIP）的交叉点**，与标准的CLIP ViT-B/16（Radford et al., 2021）基线形成直接对比。关键设计变更包括：

| 设计维度 | 基线（RGB CLIP） | GaussianVision |
|----------|------------------|----------------|
| 视觉输入表示 | RGB像素分块为patches | 2DGS参数（8维：位置、协方差、颜色） |
| 输入处理模块 | 线性投影 + patch embedding | GS stem（对数变换、傅里叶特征、归一化、线性投影、Perceiver交叉注意力重采样器） |
| 训练方式 | 直接端到端对比学习 | 两阶段：先蒸馏RGB嵌入，再参数高效CLIP适应 |

主要实验结果验证了该方案的有效性：在DataComp-12.8M数据集上训练，并在CLIP Benchmark的38个数据集上评估，**3136个高斯点的GS模型在实现3倍压缩的同时，达到RGB基线98%的相对零样本准确率**；即使压缩至400个高斯点（23.5倍压缩），仍保持91%的相对准确率。一项决定性证据表明，对GS-1600进行RGB渲染后再训练ViT，其准确率下降程度与直接使用GS表示训练CLIP几乎一致，说明当前GS编码器的性能上限主要受限于压缩RGB重建质量，而非对齐机制本身。

然而，该方法存在若干已知局限：2DGS拟合仍需大量GPU预处理时间；从头训练GS编码器收敛极差，必须依赖RGB教师模型；在医学图像等细粒度任务上性能显著下降。这些局限也指向了开放问题：**能否设计具有原生归纳偏置的GS-native Transformer架构以摆脱对RGB教师的依赖？如何利用2DGS的可变密度特性实现自适应token分配？**



### 大规模视觉-语言模型的数据传输瓶颈

视觉-语言模型（VLMs）和对比语言-图像预训练模型（如CLIP）已成为多模态理解的核心范式，但其训练和推理依赖于海量高分辨率RGB图像。在边缘-云协同场景中，密集RGB图像的传输构成了显著能效瓶颈：以224×224×3的原始像素表示为例，单张图像即需约150KB的未压缩数据量，大规模预训练数据集（如DataComp-12.8M）的传输与加载成本极高。据Scope3方法论估算，数字内容传输的碳排放强度已达每GB约0.06 kWh，而当前多模态模型的数据吞吐量仍在持续增长。

### Patch-based Tokenization的冗余困境

现有视觉编码器（如ViT）普遍采用patch-based tokenization策略，将图像均匀划分为固定大小的patches后线性投影为token序列。这一范式存在结构性冗余：图像中的平滑背景区域与纹理丰富的语义区域被分配等量的token预算，导致大量token承载低信息密度的视觉信号。以ViT-B/16为例，每张224×224图像产生196个视觉token，其中相当比例用于编码对语义理解贡献甚微的背景或重复纹理。这种冗余直接推高了Transformer的自注意力计算复杂度（$O(n^2)$），制约了模型的可扩展性。

### 现有压缩方法的局限

针对上述问题，现有工作主要沿两条路径探索：一是图像压缩编码（如JPEG、WebP），但此类方法针对人类视觉感知优化，未考虑下游视觉-语言对齐任务的语义保真度需求；二是token压缩（如token merging、pruning），但这些方法在ViT内部操作，无法减少前端数据传输量。**GViT**等工作初步探索了将2D高斯泼溅（2DGS）用于监督图像分类，证明了压缩表示可达到与RGB ViT相当的ImageNet-1K top-1准确率（76.9%），但尚未涉足更具挑战性的视觉-语言对齐任务。

### 核心研究问题

本文的核心动机在于回答一个关键问题：**能否用紧凑的、自适应空间分布的2D高斯泼溅参数替代原始RGB像素，作为视觉-语言对比学习的输入表示？** 这一问题的解决需要同时克服三重挑战：

1. **拟合效率**：对百万级图像数据集进行逐张2DGS优化在计算上不可行，需设计可批量执行的加速拟合方案；
2. **表示迁移**：2DGS的8维参数空间（位置、协方差、颜色）与预训练ViT期望的RGB patch嵌入存在本质差异，需构建有效的模态桥接机制；
3. **语义保真度**：压缩表示必须在极高压缩比（3×–23.5×）下保留足够的语义信息，以支撑38个多样化数据集的零样本分类。

### 本文的切入路径

GaussianVision的核心洞察在于：2DGS的稀疏各向异性高斯分布天然适配图像的语义结构——高斯点密度隐含编码了区域重要性，其位置与协方差参数携带空间布局信息，而颜色参数保留了外观线索。通过设计专用的GS stem（含对数变换、傅里叶特征、归一化及Perceiver交叉注意力重采样器）和两阶段蒸馏-适应训练策略，可将这些压缩参数映射到与冻结RGB ViT兼容的嵌入空间，从而在不重新训练视觉编码器骨干的前提下实现高效视觉-语言对齐。



## 核心方法与创新机理

GaussianVision 的核心创新在于**将视觉-语言对齐的输入基底从密集 RGB 像素替换为紧凑的二维高斯泼溅（2DGS）参数表示**，并通过一系列配套设计使压缩后的表示能够有效驱动冻结的预训练 ViT，从而在显著降低数据传输和存储开销的同时保持有竞争力的零样本性能。这一创新体现在三个关键维度的系统性改变上。

### 1. 视觉输入表示的范式转换：从像素到高斯参数

传统 CLIP 训练以 RGB 像素分块（patches）作为视觉编码器的输入，每个 224×224 图像产生 196 个 patch token。GaussianVision 将这一输入基底替换为**一组自适应空间分布的二维各向异性高斯参数**，每个高斯由 8 个参数描述（2D 位置 $\pmb{\mu}_i$、协方差 $\pmb{\Sigma}_i$ 和颜色 $\mathbf{c}_i$），图像通过所有高斯的加权求和重建：

$$\hat{I}(x,y) = \sum_{i=1}^n \mathbf{c}_i \exp\left\{ -\frac{1}{2} \left( \begin{bmatrix} x \\ y \end{bmatrix} - \pmb{\mu}_i \right)^\top \Sigma_i^{-1} \left( \begin{bmatrix} x \\ y \end{bmatrix} - \pmb{\mu}_i \right) \right\}$$

这一表示的核心优势在于**空间自适应性**：高斯点天然倾向于在纹理丰富、信息密集的区域聚集，而在平坦区域保持稀疏，从而以少量参数捕获图像的结构化信息。在 3136 个高斯点的配置下，压缩比达到 3×；在 400 点的极限配置下，压缩比可达 23.5×。压缩比的计算公式为：

$$\mathrm{Compression} = \frac{224 \times 224 \times 3 \times 18}{N_{\mathrm{GS}} \times 8 \times 28}$$

其中分子对应未压缩 RGB 输入的字节量（含 18 倍 JPEG 压缩因子），分母对应 $N_{\mathrm{GS}}$ 个高斯点以 FP16 存储 8 个参数的开销。

### 2. 输入处理模块的重构：GS Stem 替代线性投影

RGB 基线仅需简单的线性投影将 patch 映射为 token embedding。GaussianVision 设计了一个**溅射感知的 GS stem** 来处理非结构化的高斯参数集，这是弥合高斯表示与预训练 ViT 之间语义鸿沟的关键桥梁。GS stem 由以下组件构成：

- **对数变换与傅里叶特征编码**：对高斯参数进行预处理，增强模型对空间位置和尺度变化的感知能力。
- **归一化与线性投影**：将每个高斯点的 8 维参数映射到与 ViT 隐藏维度对齐的高维空间。
- **Perceiver 交叉注意力重采样器**：将可变数量的高斯点嵌入聚合为固定数量的视觉 token（196 或 98 个），使输出与冻结 ViT 的输入接口完全兼容。

消融实验表明，Perceiver 交叉注意力方案在训练稳定性和零样本准确率上均优于网格池化和 Hilbert 分块等替代方案。

### 3. 训练策略的两阶段重构：从端到端到蒸馏+适应

RGB 基线采用端到端的对比学习直接优化全部参数。GaussianVision 改用**两阶段参数高效训练**，以解决从头训练 GS 编码器收敛极差的问题：

- **阶段一：RGB→GS 蒸馏**。以预训练 RGB ViT 为教师模型，仅训练 GS stem，使用 CLS embedding 之间的 MSE 损失将 GS 表示对齐到 RGB 嵌入空间。此阶段仅需 2 个 epoch。
- **阶段二：参数高效 CLIP 适应**。解冻仅约 9.7% 的 CLIP 参数（GS stem、前两个 Transformer block、最终归一化和投影层），其余 ViT 层和文本编码器保持冻结，使用标准 CLIP 对比损失进行微调。

这种设计使 GaussianVision 能够**继承预训练 RGB ViT 的视觉语义能力**，同时大幅降低训练开销。但这也构成了一个根本性限制：GS 模型的性能上限受制于 RGB 教师模型的质量，且无法完全摆脱对像素预训练模型的依赖。附录中的关键证据（Figure 14）表明，对 GS-1600 进行 RGB 渲染后再训练 ViT 所导致的准确率下降幅度，与直接使用 GS 表示训练 CLIP 的下降幅度几乎一致，说明当前 GS 编码器的性能瓶颈主要源于压缩 RGB 重建质量的损失，而非 GS stem 本身的设计缺陷。

### 4. 使能技术：高效可扩展的 2DGS 拟合

上述创新的落地依赖于对 2DGS 拟合过程的大幅加速，否则在千万级图像数据集上进行预处理将不可行。GaussianVision 提出了三项优化：

- **批量 CUDA 核**：通过批量感知的内存布局、同步线程和共享内存优化，在 batch size 4096、400 高斯点的配置下实现 **90.3× 加速**，GPU 利用率达 97%。
- **结构化初始化**：以均匀网格初始化高斯中心、各向同性协方差和单元平均颜色，替代随机初始化。在 4900 高斯点、3000 迭代下，PSNR 从 28.24 提升至 **35.25（+6.01 dB）**，且在低高斯预算下优势更为显著。
- **亮度感知剪枝**：结合 L1 颜色正则化和基于亮度分数的自适应剪枝，从较大高斯预算（1600–3136 点）出发逐步稀疏化，比直接使用小预算获得更高的最终重建质量。

拟合损失函数整合了像素级 L2 重建误差和颜色通道的 L1 稀疏正则化：

$$\mathcal{L}_{\mathrm{GS}} = \frac{1}{B} \sum_{b=1}^{B} \left[ \frac{1}{HW} \| \hat{\mathbf{I}}^{(b)} - \mathbf{I}^{(b)} \|_2^2 + \lambda_{\mathrm{reg}} \| \mathbf{C}^{(b)} \|_1 \right]$$

### 创新边界与待验证假设

GaussianVision 的贡献在于**首次系统性地验证了压缩高斯表示可作为视觉-语言对齐的有效基底**，而非提出全新的模型架构。其核心假设——2DGS 的空间自适应性能够保留足够的语义信息以支撑对比学习——在 38 个 CLIP Benchmark 数据集上得到了初步验证，但以下边界仍需注意：

- **细粒度任务退化**：在 diabetic_retinopathy 等医学图像任务上性能显著下降，表明 GS 表示可能丢失了对某些专业领域至关重要的纹理细节。
- **对 RGB 教师的依赖**：两阶段训练策略意味着该方法本质上是 RGB 预训练模型的一种压缩适应方案，而非独立的表示学习范式。
- **预处理成本**：即使经过 CUDA 加速，400 点配置处理 12.8M 图像仍需约 25.6 GPU 小时，对于更大规模数据集的可扩展性有待验证。



GaussianVision 的核心思路是用紧凑的二维高斯泼溅（2DGS）参数替代原始 RGB 像素作为视觉编码器的输入，从而在保持视觉-语言对齐能力的同时大幅压缩图像表示。整个 pipeline 由三个逻辑阶段串联而成：**2DGS 拟合与压缩**、**GS Stem 嵌入映射**、以及**两阶段 CLIP 适应训练**，如图 1 所示。

**阶段一：图像到高斯表示的压缩。** 给定一张输入图像，首先通过 2DGS 拟合模块将其表示为一组稀疏的二维各向异性高斯。每个高斯由 8 个参数描述：二维位置 $\pmb{\mu}_i$、协方差矩阵 $\pmb{\Sigma}_i$ 和颜色 $\mathbf{c}_i$。图像重建遵循标准的二维高斯泼溅公式：

$$\hat{I}(x,y;\{\pmb{\mu}_i,\pmb{\Sigma}_i,\mathbf{c}_i\}_{i=1}^n) = \sum_{i=1}^n \mathbf{c}_i \exp\Bigg\{ -\frac{1}{2} \left( \left[ \begin{array}{c} x \\ y \end{array} \right] - \pmb{\mu}_i \right)^\top \Sigma_i^{-1} \left( \left[ \begin{array}{c} x \\ y \end{array} \right] - \pmb{\mu}_i \right) \Bigg\}$$

拟合过程通过最小化像素级 L2 重建误差与颜色通道 L1 正则化的联合损失来优化高斯参数：

$$\mathcal{L}_{\mathrm{GS}} = \frac{1}{B} \sum_{b=1}^{B} \bigg[ \underbrace{ \frac{1}{HW} || \hat{\mathbf{I}}^{(b)} - \mathbf{I}^{(b)} ||_2^2 }_{ \mathrm{L2\ reconstruction} } + \lambda_{\mathrm{reg}} \underbrace{ \big\| \mathbf{C}^{(b)} \big\|_1 }_{ \mathrm{L1\ color\ reg} } \bigg]$$

为在 12.8M 规模的数据集上高效运行，作者引入了三项关键优化：**结构化初始化**（以均匀网格分布初始化高斯中心、各向同性协方差和平均单元格颜色，在 4900 点下 PSNR 提升 6.01 dB）、**亮度感知剪枝**（结合 L1 正则化与亮度阈值剔除贡献微小的高斯，从较大高斯预算开始剪枝比直接使用小预算获得更高最终 PSNR），以及**批量 CUDA 核加速**（针对大批量输入重新设计内存布局与同步机制，在 batch size 4096 和 400 高斯点配置下实现 90.3 倍加速，GPU 利用率达 97%）。压缩比定义为：

$$\mathrm{Compression} = \frac{224 \times 224 \times 3 \times 18}{N_{\mathrm{GS}} \times 8 \times 28}$$

其中 $N_{\mathrm{GS}}$ 为高斯点数量，每个 splat 以 FP16 存储 8 个参数。实验覆盖 400 至 3136 点的高斯预算，对应约 23.5 倍到 3 倍的压缩比。

**阶段二：GS Stem 嵌入映射。** 压缩后的高斯参数无法直接送入为标准 RGB patch 设计的 ViT。GS Stem 模块充当“翻译层”，将可变数量的高斯点映射为固定数量的视觉 token。其处理流程包括：对位置和协方差参数进行对数变换与傅里叶特征编码、归一化、线性投影，最后通过 **Perceiver 交叉注意力重采样器**将任意数量的高斯嵌入汇聚为固定长度（196 或 98 个 token）的序列。消融实验表明，Perceiver 方案在训练稳定性和零样本准确率上均优于网格池化和 Hilbert 分块等替代方案。

**阶段三：两阶段 CLIP 适应训练。** 直接从头训练 GS 编码器收敛极差，因此采用从预训练 RGB ViT 迁移知识的策略。第一阶段为 **RGB→GS 蒸馏**：冻结 RGB 教师 ViT，仅训练 GS Stem，以 MSE 损失对齐 GS 学生与 RGB 教师的 L2 归一化 CLS 嵌入，训练 2 个 epoch。第二阶段为 **参数高效 CLIP 适应**：解冻约 9.7% 的 CLIP 参数（GS Stem、前两个 Transformer block、最终归一化与投影层），使用标准 CLIP 对比损失在 DataComp-12.8M 数据集上进行训练。文本编码器保持冻结。

整个框架的输入是经过 2DGS 拟合的高斯参数，输出是可与文本嵌入进行对比对齐的视觉特征。值得注意的是，该 pipeline 并非端到端可微：2DGS 拟合作为预处理步骤独立完成，拟合后的高斯参数被保存并作为后续训练阶段的固定输入——这一设计使得大规模预处理的计算开销（例如 400 点配置需约 25.6 GPU 小时处理 12.8M 图像）与 CLIP 训练解耦。

### 补充图表

![[assets/figures/papers/paper_list_l2391_https_arxiv_org_abs_2509_22615/figures/001_Figure_1.jpg]]
*Figure 1: (a) Illustration of 2D Gaussian Splatting (2DGS) for image fitting. Each image is represented as a sparse mixture of anisotropic Gaussians parameterized by position, covariance, and color. Summing contributions from all splats reconstructs the original image (with a minor and configurable degradation loss), enabling compact, spatially adaptive representations. (b) 2DGS adaptation of contrastive language-image pre-training (CLIP). (c) Architecture of an autoregressive visual language model (VLM). (d) Architecture of our 2DGSadapted CLIP pipeline: a splat-aware stem embeds a configurable number of Gaussian points using Fourier features, log scaling, normalization layers, and projections. Thes...*



### 2D高斯泼溅图像重建公式

GaussianVision的核心表示层基于**2D Gaussian Splatting (2DGS)**，将每幅图像建模为一组稀疏的各向异性二维高斯函数的叠加。每个高斯由8个参数描述：二维位置 $\pmb{\mu}_i$、各向异性协方差 $\pmb{\Sigma}_i$ 和颜色 $\mathbf{c}_i$。给定 $n$ 个高斯点，图像在像素坐标 $(x,y)$ 处的重建强度为：

$$\hat{I}(x,y;\{\pmb{\mu}_i,\pmb{\Sigma}_i,\mathbf{c}_i\}_{i=1}^n) = \sum_{i=1}^n \mathbf{c}_i \exp\Bigg\{ -\frac{1}{2} \left( \left[ \begin{array}{c} x \\ y \end{array} \right] - \pmb{\mu}_i \right)^\top \Sigma_i^{-1} \left( \left[ \begin{array}{c} x \\ y \end{array} \right] - \pmb{\mu}_i \right) \Bigg\}$$

**变量含义：**
- $\pmb{\mu}_i \in \mathbb{R}^2$：第 $i$ 个高斯的中心位置
- $\pmb{\Sigma}_i \in \mathbb{R}^{2\times 2}$：各向异性协方差矩阵，控制高斯的形状和方向
- $\mathbf{c}_i \in \mathbb{R}^3$：RGB颜色向量
- $n$：高斯点总数（可配置为400、900、1600、3136等）

该公式的物理意义是：每个像素位置的颜色由所有高斯在该位置的贡献加权求和得到，权重由高斯核的指数衰减决定。这种表示天然具有空间自适应性——高纹理区域可分配更多高斯点，平坦区域仅需少量高斯。

---

### 2DGS拟合优化损失函数

为将原始RGB图像转换为2DGS参数，需要求解一个拟合优化问题。损失函数由像素级L2重建误差和颜色通道的L1正则化组成：

$$\mathcal{L}_{\mathrm{GS}} = \frac{1}{B} \sum_{b=1}^{B} \bigg[ \underbrace{ \frac{1}{HW} || \hat{\mathbf{I}}^{(b)} - \mathbf{I}^{(b)} ||_2^2 }_{ \mathrm{L2\ reconstruction} } + \lambda_{\mathrm{reg}} \underbrace{ \big\| \mathbf{C}^{(b)} \big\|_1 }_{ \mathrm{L1\ color\ reg} } \bigg]$$

**变量含义：**
- $B$：批次大小
- $H, W$：图像高度和宽度（均为224）
- $\hat{\mathbf{I}}^{(b)}$：重建图像
- $\mathbf{I}^{(b)}$：原始RGB图像
- $\mathbf{C}^{(b)}$：所有高斯点的颜色参数矩阵
- $\lambda_{\mathrm{reg}}$：正则化权重（典型值 $10^{-6}$）

L1颜色正则化的作用是通过惩罚颜色参数的绝对值来鼓励稀疏性，使不重要区域的高斯点颜色趋向于零，为后续的亮度感知剪枝提供依据。

---

### 亮度感知剪枝分数

在拟合完成后，GaussianVision通过**亮度感知剪枝**进一步压缩高斯点数量。每个高斯点的剪枝分数定义为其颜色通道的亮度加权和：

$$s_{b,n} = \underbrace{ 0.2126 |R_{b,n}| + 0.7152 |G_{b,n}| + 0.0722 |B_{b,n}| }_{ \mathrm{luminance\ score\ } \ell(\mathbf{c}_{b,n}) }$$

**变量含义：**
- $R_{b,n}, G_{b,n}, B_{b,n}$：批次中第 $b$ 张图像的第 $n$ 个高斯点的RGB颜色值
- 权重系数（0.2126, 0.7152, 0.0722）遵循ITU-R BT.709亮度转换标准

当某个高斯的亮度分数 $s_{b,n}$ 低于预设阈值 $\tau_{\mathrm{th}}$ 时，该高斯被剪枝移除。实验表明（Figure 4），从较大的高斯预算（1600-3136点）开始拟合再剪枝，比直接使用小预算获得更高的最终PSNR——大预算模型可支持更高的剪枝率而重建质量损失极小。

![[assets/figures/papers/paper_list_l2391_https_arxiv_org_abs_2509_22615/figures/004_Figure_4.jpg]]
*Figure 4: Trade-off between pruning ratio and reconstruction degradation for different Gaussian budgets (400–3136 points), evaluated over 100 Mini-ImageNet samples per configuration. Each marker represents a single hyperparameter setting, while the surrounding shaded KDE envelopes summarize the empirical distribution of ∆PSNR for each model size: models with larger initial Gaussian budgets (1600–3136) consistently support higher pruning ratios with minimal loss, while smaller models are more sensitive to sparsification*

---

### 压缩比计算公式

相对于未压缩的RGB像素输入，2DGS表示的压缩比定义为：

$$\mathrm{Compression} = \frac{224 \times 224 \times 3 \times 18}{N_{\mathrm{GS}} \times 8 \times 28}$$

**变量含义：**
- $224 \times 224 \times 3$：RGB图像的原始像素字节数
- $18$：RGB像素的比特深度因子（相对于FP16的折算）
- $N_{\mathrm{GS}}$：高斯点数量
- $8$：每个高斯点的参数维度（位置2 + 协方差3 + 颜色3）
- $28$：FP16存储的比特宽度因子

当 $N_{\mathrm{GS}}=3136$ 时，压缩比约为3×；当 $N_{\mathrm{GS}}=400$ 时，压缩比可达23.5×。

---

### GS Stem：泼溅感知嵌入模块

GaussianVision的**GS Stem**是将2DGS参数映射到视觉token空间的关键桥梁。其处理流程为：

1. **对数变换**：对协方差参数应用对数映射，稳定数值范围
2. **傅里叶特征编码**：将位置和协方差参数映射到高频特征空间，增强对空间细节的建模能力
3. **归一化层**：对各参数通道进行标准化
4. **线性投影**：将8维GS参数投影到与ViT兼容的嵌入维度
5. **Perceiver交叉注意力重采样器**：将可变数量的高斯点嵌入聚合为固定数量的视觉token（196或98个）

消融实验（Figure 18）证实，Perceiver交叉注意力方案在训练稳定性和零样本准确率上均优于网格池化和Hilbert分块等替代方案。

![[assets/figures/papers/paper_list_l2391_https_arxiv_org_abs_2509_22615/figures/031_Figure_18.jpg]]
*Figure 18: GS-Stem architecture study: different approaches to going from N points to smaller M latents*

---

### 两阶段训练框架

GaussianVision采用**两阶段训练**以高效迁移RGB预训练知识：

- **Stage 1 — RGB→GS蒸馏**：使用MSE损失对齐GS stem输出的CLS嵌入与RGB教师模型的CLS嵌入，仅训练GS stem参数
- **Stage 2 — 参数高效CLIP适应**：解冻约9.7%的CLIP参数（GS stem、前两个Transformer块、最终归一化和投影层），使用标准CLIP对比损失进行端到端对齐

这种设计使GS编码器能够继承RGB ViT的语义理解能力，同时仅需微调少量参数即可适应压缩表示的特性。

### 补充图表

![[assets/figures/papers/paper_list_l2391_https_arxiv_org_abs_2509_22615/figures/002_Figure_2.jpg]]
*Figure 2: Speedup results achieved by our CUDA kernels compared to the [41] baseline, following our batch-aware implementation. Speedups are presented for various batch sizes and Gaussian counts for image resolutions of 224x224. For a batch size of 4096 and 400 Gaussian points per image, we observe a 90.3X speedup compared to the baseline*

![[assets/figures/papers/paper_list_l2391_https_arxiv_org_abs_2509_22615/figures/003_Figure_3.jpg]]
*Figure 3: Visualization of reconstruction results for random vs. structured initialization (Ours) for 2DGS fitting for a fixed number of iterations (3000): structured initialization accelerates convergence and achieves higher perceptual quality than random initialization. This is consistent across various compression ratios (ie, numbers of Gaussian points per image) especially for more aggressive compression ratios*

![[assets/figures/papers/paper_list_l2391_https_arxiv_org_abs_2509_22615/figures/005_Figure_5.jpg]]
*Figure 5: Visualization of Gaussian splats and reconstructed images for a 3136-point GS fit (2000 iterations). Left*



## 实验与关键发现

### 主结果：压缩-精度权衡

GaussianVision在CLIP Benchmark的38个数据集上系统评估了不同高斯点预算下的零样本分类性能。核心发现是：**2DGS表示能够以显著的压缩比换取可接受的精度损失**。

**3136点配置**（196个视觉token）实现了RGB基线96–98%的相对零样本准确率，同时将输入数据量压缩**3倍**。该配置下的绝对平均准确率与在相同DataComp-12.8M数据集上训练的CLIP ViT-B/16 (Small)基线高度接近，验证了GS表示在保持语义对齐能力方面的有效性。

当高斯点数量进一步减少时，压缩比急剧上升，精度呈可控下降：
- **1600点**：约6×压缩，相对精度保持在95%左右
- **900点**：约10×压缩，相对精度约92%
- **400点**：约**23.5×压缩**，相对精度约91%

上述结果表明，2DGS表示存在一个“效率甜区”——即使在高压缩率下，GS编码器仍能保留大部分视觉语义信息。Table 1汇总了各配置的压缩比、数据加载速度与准确率对比。

**Figure 6**展示了各模型变体在196 token和98 token两种设置下跨38个数据集的零样本准确率分布。GS-3136在多数数据集上紧贴RGB基线，而GS-400在部分细粒度任务上出现明显下降。完整的逐数据集准确率见**Table 5**，相对准确率排名见**Table 6**。

### 2DGS拟合优化的消融实验

#### 结构化初始化的作用

随机初始化高斯参数会导致收敛缓慢且重建质量差。实验表明，**结构化初始化在4900高斯点、3000次迭代下将PSNR从28.24 dB提升至35.25 dB（+6.01 dB）**。即使在400点的极端压缩下，结构化初始化仍保持22.04 dB vs. 17.77 dB的显著优势（**Figure 3**）。

结构化初始化的三个关键设计：
1. **位置初始化**：均匀网格分布，使高斯中心覆盖整个图像空间
2. **协方差初始化**：各向同性设置，基于网格间距
3. **颜色初始化**：取对应网格单元的平均RGB值

这种像素先验大幅降低了早期优化阶段的探索成本，使优化器能更快收敛到高质量解。

#### 亮度感知剪枝的有效性

**Figure 4**揭示了高斯预算与剪枝鲁棒性之间的关键关系：从较大初始预算（1600–3136点）开始训练后剪枝，比直接使用小预算训练获得更高的最终PSNR。具体而言，1600–3136点模型可承受更高剪枝比例而重建质量损失极小，而400点模型对稀疏化高度敏感。

剪枝策略结合了L1颜色正则化和亮度评分：
$$s_{b,n} = 0.2126|R_{b,n}| + 0.7152|G_{b,n}| + 0.0722|B_{b,n}|$$
低亮度的高斯点被认为对重建贡献小，优先被移除。**Figure 5**展示了3136点模型剪枝前后的可视化对比：23.72%剪枝率下PSNR从37.43降至31.1，但视觉质量仍可接受。

#### CUDA核加速

批量并行CUDA核对2DGS拟合的可扩展性至关重要。**Figure 2**显示，在批大小4096、每图400高斯点的配置下，相比基线实现**90.3×加速**。**Table 3**的Nsight Systems分析表明，内核利用率和内存带宽利用率均达到高水平。**Table 4**列出了各配置的批大小选择和12.8M图像数据集的预估GPU总耗时——400点配置约需25.6 GPU小时。

![[assets/figures/papers/paper_list_l2391_https_arxiv_org_abs_2509_22615/figures/014_Table_3.jpg]]
*Table 3: Nsight Systems profiling of our batch-parallel 2DGS CUDA kernels. Reported numbers correspond to 4000 points and 2000 iterations per image. Kernel/Memory percentages reflect the fraction of active GPU time*

![[assets/figures/papers/paper_list_l2391_https_arxiv_org_abs_2509_22615/figures/015_Table_4.jpg]]
*Table 4: Gaussian Splat fitting configurations. Each configuration specifies the number of Gaussian points per image. Batch sizes were selected using CUDA profiling for maximal throughput. Total GPU hours are estimated by dividing the 12.8M-image dataset size by the measured time per batch. We report dataset-level statistics (mean and std) for covariance components*

### 视觉Token数量消融

将视觉token从196减至98时，所有模型变体的性能均出现下降（**Figure 6**）。但GS模型的相对下降幅度与RGB基线可比，表明GS表示并未引入额外的token效率损失。附录中的**Figure 13**和**Table 7**进一步显示，对RGB ViT进行1–5 epoch的token减少微调可部分恢复性能，这为GS模型的token效率优化提供了参考上限。

![[assets/figures/papers/paper_list_l2391_https_arxiv_org_abs_2509_22615/figures/007_Figure_6.jpg]]
*Figure 6: Zero-shot classification accuracy on 38 datasets from the CLIP Benchmark for ViT-B-16 (Small) and multiple variants of GS vision encoders (number of gaussian points/img: 3136, 1600, 900, 400). Results are presented for 196 tokens (baseline) and 98 tokens*

### 训练策略消融：两阶段范式的必要性

GS编码器的训练采用两阶段策略：**Stage 1蒸馏**将GS stem对齐到RGB教师的CLS嵌入空间（MSE损失），**Stage 2 CLIP适应**解冻约9.7%的参数进行对比学习。消融实验表明，跳过Stage 1直接进行对比训练会导致严重的不稳定和收敛失败，验证了RGB教师引导对于GS表示语义对齐的必要性。

### 失败模式与性能瓶颈

尽管整体表现优异，GS模型在特定场景下暴露了明显局限：

1. **细粒度医学图像**：在diabetic_retinopathy数据集上，所有GS变体的性能均显著低于RGB基线，表明GS表示在捕捉精细纹理和局部病变特征方面存在不足。

2. **压缩重建瓶颈**：**Figure 14**的对照实验揭示了当前GS编码器的性能上限——对GS-1600进行RGB渲染后再训练ViT，其准确率下降程度与直接使用GS表示训练CLIP几乎一致。这表明**GS编码器的性能主要受限于压缩RGB重建的质量，而非GS stem的映射能力**。

![[assets/figures/papers/paper_list_l2391_https_arxiv_org_abs_2509_22615/figures/024_Figure_14.jpg]]
*Figure 14: Comparison of distillation strategies and their effect on CLIP alignment and optimization dynamics*

3. **小预算模型的脆弱性**：400点配置在多个数据集上出现大幅波动，说明极端压缩下GS表示丢失了关键的判别性信息。

### 公平性说明

需注意以下实验设计的不对称性：
- GS模型经过两阶段训练（蒸馏+CLIP适应），而RGB基线直接端到端训练
- 附录中提供了RGB 98 token微调结果作为更公平的token效率基线
- 所有模型使用相同的DataComp-12.8M数据集和Open CLIP标准超参数，ViT-B/16采用宽度512的Small变体以控制计算成本

### 补充图表

![[assets/figures/papers/paper_list_l2391_https_arxiv_org_abs_2509_22615/figures/020_Table_5.jpg]]
*Table 5: Zero-shot classification accuracy across datasets. For each dataset, the best score (across all models and token counts) is shown in bold, and the second-best is underlined*

![[assets/figures/papers/paper_list_l2391_https_arxiv_org_abs_2509_22615/figures/021_Table_6.jpg]]
*Table 6: Relative accuracy table with bold marking the best per row and underline marking the second-best per row*



## 定位与知识库关联

### 1. 方法谱系：从像素到高斯参数的视觉表示迁移

GaussianVision 的核心技术路线是将视觉-语言对齐的输入底物从**密集RGB像素**替换为**压缩的二维高斯泼溅（2DGS）参数**。这一思路处于两条研究脉络的交汇点：

**脉络一：神经图像压缩与隐式表示。** 传统图像压缩（JPEG、WebP）以像素域变换为基础，而2DGS属于**显式结构化表示**——每张图像被建模为一组稀疏的、各向异性的二维高斯核，每个高斯仅需8个参数（2D位置 $\pmb{\mu}_i$、协方差 $\pmb{\Sigma}_i$、颜色 $\mathbf{c}_i$），通过叠加所有高斯的贡献重建图像：

$$\hat{I}(x,y) = \sum_{i=1}^n \mathbf{c}_i \exp\left\{ -\frac{1}{2} \left( \begin{bmatrix} x \\ y \end{bmatrix} - \pmb{\mu}_i \right)^\top \Sigma_i^{-1} \left( \begin{bmatrix} x \\ y \end{bmatrix} - \pmb{\mu}_i \right) \right\}$$

与基于patch的tokenization（如ViT将图像均匀切分为196个patch）相比，2DGS的**自适应空间分布**特性使其能用更少的基元覆盖图像的关键结构区域。论文通过**结构化初始化**（均匀网格位置 + 各向同性协方差 + 平均颜色）和**亮度感知L1剪枝**，在保持重建质量的同时实现3×–23.5×的输入压缩。

**脉络二：视觉-语言模型的输入效率优化。** CLIP（Radford et al., 2021）及其变体将图像线性投影为固定数量的patch token，但密集RGB输入在边缘-云传输场景下带宽消耗大，且patch token数量恒定，无法根据图像内容自适应调整。GaussianVision 通过引入**GS stem**（对数变换 + 傅里叶特征 + 归一化 + 线性投影 + Perceiver交叉注意力重采样器），将可变数量的高斯参数映射为固定数量的视觉token，送入冻结的预训练RGB ViT骨干网络。

### 2. 与基线方法的核心差异

| 维度 | RGB CLIP ViT-B/16（基线） | GaussianVision |
|------|--------------------------|----------------|
| **视觉输入表示** | RGB像素分块为patches | 2DGS参数（8维：位置、协方差、颜色） |
| **输入处理模块** | 简单线性投影 + patch embedding | GS stem（对数变换、傅里叶特征、归一化、线性投影、Perceiver交叉注意力重采样器） |
| **训练方式** | 直接端到端对比学习 | 两阶段：先蒸馏RGB嵌入（MSE损失），再参数高效CLIP适应（仅解冻约9.7%参数） |
| **压缩比** | 1× | 3×–23.5× |
| **相对零样本准确率** | 100%（基准） | 91%–98%（随压缩比变化） |

**关键设计选择：两阶段训练的必要性。** 论文明确指出，**从头训练GS编码器收敛极差**，必须依赖RGB预训练教师模型进行蒸馏（Stage 1），再通过参数高效微调（Stage 2）恢复对比学习性能。这一约束意味着GaussianVision目前**无法完全去像素化**，其性能上限受限于RGB教师模型的质量——附录实验（Figure 14）表明，对GS-1600进行RGB渲染再训练的ViT准确率下降程度与直接使用GS表示训练CLIP的下降程度几乎一致，证实了当前GS编码器的瓶颈在于**压缩RGB重建质量**，而非GS stem本身的设计缺陷。

### 3. 适用边界与局限

**已验证的适用场景：**
- **自然图像零样本分类**：在CLIP Benchmark的38个数据集上，3136点GS模型（3×压缩）达到RGB基线96%–98%的相对准确率；400点模型（23.5×压缩）仍保持91%相对准确率。
- **带宽受限的边缘-云传输**：GS表示在数据加载和解码速度上具有优势（Table 1），配合批量CUDA核加速（batch size 4096 + 400高斯点实现90.3×加速，GPU利用率97%），适合大规模预处理流水线。

**明确的失效模式与局限：**

1. **细粒度/域外任务性能下降**：在医学图像数据集（diabetic_retinopathy）等与自然图像分布差异较大的任务上，GS模型性能显著下降，表明2DGS的压缩表示可能丢失了对细粒度判别至关重要的纹理细节。

2. **预处理计算开销**：尽管CUDA核大幅加速了拟合过程，但大规模预处理仍需显著GPU时间——400点配置处理12.8M图像约需25.6 GPU小时。这限制了GS表示在实时或资源受限场景下的直接部署。

3. **对RGB教师模型的强依赖**：两阶段训练框架无法摆脱预训练RGB ViT，意味着GS编码器继承而非超越了像素域模型的归纳偏置。论文将此列为开放问题：**能否设计具有原生GS归纳偏置的Transformer架构？**

4. **固定token数量的限制**：当前GS stem通过Perceiver重采样器将任意数量的高斯点映射为固定数量的视觉token（196或98），**未充分利用2DGS的自适应密度特性**——理论上，简单图像可以用更少的高斯点和更少的token表示，但现有架构不支持这种动态分配。

### 4. 开放问题与未来方向

论文明确提出了四个开放问题，这些问题定义了该方向的后续研究空间：

1. **GS-native架构设计**：能否构建不依赖RGB教师模型、直接从2DGS参数中学习视觉表征的Transformer？这需要解决GS参数空间（位置、协方差、颜色）与自注意力机制的归纳偏置对齐问题。

2. **自适应token分配**：如何利用2DGS的可变密度特性，根据图像内容动态决定高斯点数量和输出token数量？这将使压缩比从“全局固定”升级为“内容自适应”，进一步提升效率。

3. **域外泛化性改善**：GS表示在医学图像等分布外任务上的性能下降需要针对性解决，可能的路径包括：域特定的GS拟合策略、多尺度高斯表示、或与原始RGB信号的混合输入。

4. **端到端边缘-云优化**：当前2DGS拟合和CLIP训练是解耦的，能否通过更先进的量化或熵编码方案进一步减小传输带宽，实现从边缘设备到云端的高效联合学习？

**需要人工验证的方面：** 论文未提供GS表示在**视频数据**或**多帧时序输入**上的适用性分析，也未讨论2DGS拟合过程对图像分辨率变化的敏感性（所有实验基于224×224分辨率）。这些边界条件需要后续工作验证。



## 原文 PDF

![[paperPDFs/CVPR_2026/GaussianVision_Vision_Language_Alignment_from_Compressed_Image_Representations_using_2D_Gaussian_Splatting.pdf]]
