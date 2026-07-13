---
title: "MacTok: Robust Continuous Tokenization for Image Generation"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/MacTok_Robust_Continuous_Tokenization_for_Image_Generation.pdf
project_link: null
code_link: null
aliases:
- MacTok
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
- topic/generative_models_diffusion
core_operator: 通过在输入图像上施加随机掩码和DINOv2引导的语义掩码，强迫模型从部分观测中重建完整图像；同时引入全局和局部表示对齐，使隐空间与预训练视觉特征保持一致。
primary_logic: 掩码重建创造了信息不对称：编码器只能看到部分图像，解码器却需重建全部内容，从而迫使隐变量编码足够的信息；语义掩码进一步将图像空间的语义先验迁移至隐空间；表示对齐则结构化隐空间，两者共同防止后验坍塌并提升压缩下的保真度。
claims:
- 仅图像 token 掩码（而非隐 token 掩码）能持久防止后验坍塌，并产生结构良好的隐空间。
- MacTok 在 ImageNet 256×256 上使用 128 tokens 实现 gFID 1.44（w/ CFG），在 512×512 上实现 gFID 1.52（w/ CFG），均达当时最优。
- DINO 语义掩码能在随机掩码基础之上进一步降低 gFID，且二者等概率混合效果最好。
- ImageNet 256×256 conditional generation 上 gFID (w/ CFG) = 1.44 (MacTok-128 + SiT-XL)
---

# MacTok: Robust Continuous Tokenization for Image Generation

> [!tip] 核心洞察
> 掩码重建创造了信息不对称：编码器只能看到部分图像，解码器却需重建全部内容，从而迫使隐变量编码足够的信息；语义掩码进一步将图像空间的语义先验迁移至隐空间；表示对齐则结构化隐空间，两者共同防止后验坍塌并提升压缩下的保真度。

| 字段 | 内容 |
|------|------|
| 中文题名 | MacTok：面向图像生成的鲁棒连续分词 |
| 英文题名 | MacTok: Robust Continuous Tokenization for Image Generation |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2603.29634) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction #topic/generative_models_diffusion |
| Method | MacTok |
| Dataset | ImageNet 256×256 conditional generation, ImageNet 512×512 conditional generation, ImageNet 256×256 reconstruction |

> [!tip] 效果简介
> - ImageNet 256×256 conditional generation 上，gFID (w/ CFG) 1.44 (MacTok-128 + SiT-XL) vs 2.06 (SiT-XL/2 with SD-VAE, 1024 tokens) (-0.62)。
> - ImageNet 512×512 conditional generation 上，gFID (w/ CFG) 1.52 (MacTok-128 + SiT-XL) vs 2.62 (SiT-XL/2 with SD-VAE, 4096 tokens) (-1.10)。
> - ImageNet 256×256 reconstruction 上，rFID 0.43 (MacTok-128) vs 0.62 (SiT-XL/2 tokenizer, 1024 tokens) (-0.19)。

## 概要

图像生成模型在追求极致压缩效率时面临一个根本性瓶颈：当连续分词器将图像压缩至极少量隐 token 时，KL-VAE 极易发生后验坍塌（posterior collapse）——编码器输出的隐变量退化为无信息的高斯先验，丧失对判别性特征的保留能力，导致重建和生成质量急剧下降。这一问题严重制约了高压缩比下生成模型的性能上限。

MacTok 针对上述瓶颈提出了一个简洁而有效的解决方案。其核心洞察在于：**在输入图像上施加掩码可以创造信息不对称**——编码器仅能观测部分图像，解码器却必须重建全部内容，从而迫使隐变量编码足够的信息以抵抗坍塌。基于此，MacTok 引入了两个关键机制：(1) **双重掩码策略**，以等概率混合随机掩码和 DINOv2 引导的语义掩码，前者提供正则化，后者将图像空间的语义先验迁移至隐空间；(2) **全局与局部表示对齐**，将隐 token 分别与 DINOv2 的 CLS token 和 patch token 进行余弦相似度对齐，结构化隐空间并进一步提升保真度。

实验结果表明，MacTok 在极端压缩条件下取得了显著突破。在 ImageNet 256×256 条件生成任务上，MacTok-128 配合 SiT-XL 仅需 128 个 token 即达到 gFID 1.44（w/ CFG），优于使用 1024 token 的 SD-VAE 基线（gFID 2.06）；在 512×512 分辨率上，MacTok-128 以 128 token 实现 gFID 1.52（w/ CFG），较 SD-VAE 的 4096 token 方案（gFID 2.62）提升 1.10，同时 token 用量减少最高达 64 倍。消融实验进一步证实，仅图像 token 掩码（而非隐 token 掩码）能持久防止后验坍塌，且随机掩码与语义掩码的等概率混合在所有配置中取得最优生成质量。

### 连续分词中的后验坍塌困境

现代图像生成模型广泛采用两阶段范式：先将图像压缩为低维隐表示（token），再在隐空间训练生成器。连续分词器（continuous tokenizer）——尤其是基于KL-VAE的框架——因其端到端可微、隐空间平滑等优势，成为潜在扩散模型和自回归生成模型的主流选择。然而，当追求极致压缩率（即使用极少的token数）时，这类模型面临一个根本性瓶颈：**后验坍塌（posterior collapse）**。

后验坍塌的典型表现是编码器输出的隐变量逐渐退化为无信息的高斯先验，丧失对输入图像判别性特征的编码能力。如Figure 1所示，plain KL-VAE的隐空间呈现严重坍塌，结构混乱且缺乏多样性；这直接导致重建保真度急剧下降，进而损害下游生成质量。这一困境使得现有连续分词器不得不在压缩率和重建质量之间做出妥协——**SD-VAE**使用1024个token才能在ImageNet 256×256上维持可接受的重建，而进一步减少token数则引发严重的质量退化。

### 现有方法的局限

针对后验坍塌问题，已有工作尝试了多种策略：在隐空间施加掩码（latent token masking）、引入向量量化（如**VA-VAE**、**SoftVQ-VAE**）、或采用更复杂的先验设计。但这些方法存在共同缺陷：

- **隐token掩码无法根本解决坍塌**：Figure 1的对比实验清晰表明，仅在隐空间丢弃token并不能阻止后验坍塌，因为编码器仍然可以从完整观测中“偷懒”，将信息压缩责任推卸给解码器。
- **量化方法引入额外复杂度**：向量量化虽然能约束隐空间，但面临码本坍塌、训练不稳定等问题，且离散表示天然牺牲了连续隐空间的灵活性。
- **缺乏对隐空间语义结构的主动塑造**：多数方法仅关注重建损失的优化，忽略了隐空间本身应具备的语义判别性和结构化特征。

### MacTok的核心动机

MacTok的提出源于一个关键洞察：**后验坍塌的本质是信息瓶颈设计不当——编码器可以轻易地将输入信息丢弃，而非被迫保留**。解决这一问题的因果杠杆在于创造**信息不对称**：让编码器只能访问部分图像信息，而解码器仍需重建完整图像，从而迫使隐变量承载足够的内容信息。

基于此，MacTok引入两个互补机制：

1. **图像级掩码（image token masking）**：直接在输入图像的patch层面施加掩码，而非在隐空间操作。Figure 1的对比实验提供了决定性证据——只有图像token掩码能持续稳定地防止后验坍塌，并产生结构良好的隐空间。这一发现构成了MacTok方法论的核心支柱。

2. **语义引导与表示对齐**：单纯的随机掩码虽然有效，但缺乏对“哪些信息更重要”的语义感知。MacTok进一步引入DINOv2引导的语义掩码，优先遮挡语义最相关的区域，将预训练视觉模型的语义先验迁移至隐空间；同时通过全局和局部表示对齐，主动将隐空间结构化，使隐token与DINOv2的特征空间保持一致。

这两个机制协同作用：掩码重建创造了信息保留的“刚需”，而语义掩码和表示对齐则确保保留的信息是语义有意义的。最终，MacTok在仅使用128个token（相比SD-VAE的1024个token减少8倍）的情况下，在ImageNet 256×256上实现gFID 1.44（w/ CFG），在512×512上实现gFID 1.52（w/ CFG），达到当时最优水平。

## 核心方法与创新机理

MacTok 的核心创新在于通过**信息不对称的掩码重建**与**结构化表示对齐**双机制，从根本上解决了连续分词器在强压缩下的后验坍塌（posterior collapse）问题。与简单增大模型或调整损失权重的传统思路不同，MacTok 将解决路径重新定位在编码器输入端的信息约束和隐空间的结构化上。

### 关键创新一：图像空间掩码而非隐空间掩码

此前掩码方法多作用于隐 token（如随机丢弃部分隐变量），但 MacTok 的消融实验表明，**仅图像 token 掩码能持久防止后验坍塌**，而隐 token 掩码与无掩码的 plain KL-VAE 同样会陷入坍塌（Figure 1）。其因果机制在于：当掩码施加于图像 patch 时，编码器只能观测到部分视觉信息，解码器却必须重建完整图像，这种信息不对称创造了强烈的信息编码压力，迫使隐变量保留足够的判别性特征，从而阻断后验分布退化为无信息高斯先验的路径。

### 关键创新二：DINOv2 引导的语义掩码

MacTok 在随机掩码基础上引入语义掩码，利用预训练 DINOv2 的 CLS token 与各 patch token 的余弦相似度 $s_i = \frac{\mathbf{c}^\top \mathbf{p}_i}{\|\mathbf{c}\| \|\mathbf{p}_i\|}$ 评估每个 patch 的语义重要性，并通过 Top-K 选择 $M_p = \mathrm{TopK}(\{s_i\}_{i=1}^N, \lfloor m \times N \rfloor)$ 优先掩码语义最相关的区域。这一设计将图像空间的语义先验迁移至隐空间，使模型被迫从非关键区域推断被掩码的语义内容，进一步强化隐变量的信息密度。消融实验证实，随机掩码与语义掩码以等概率混合（dino 50%）优于纯语义掩码（dino 100%）或纯随机掩码（Table 4），表明两种掩码策略具有互补性：随机掩码提供泛化的信息压缩压力，语义掩码注入结构化的语义先验。

### 关键创新三：全局-局部表示对齐

MacTok 引入双粒度表示对齐损失 $L_{\mathrm{RA}}$，将隐空间与 DINOv2 预训练特征空间对齐。局部对齐通过将 $L$ 个隐 token 扩展至 patch 粒度 $\tilde{\mathbf{z}}_{\mathrm{loc}} = \mathrm{Expand}(\hat{\mathbf{z}}, r)$ 后与 DINOv2 patch token 计算余弦相似度；全局对齐则将隐 token 平均池化 $\tilde{\mathbf{z}}_{\mathrm{glob}} = \frac{1}{L} \sum_{i=1}^L \hat{\mathbf{z}}_i$ 后与 DINOv2 CLS token 对齐。两者经轻量 MLP 投影后统一优化：

$$L_{\mathrm{RA}} = -\frac{1}{N+1} \left( \sum_{i=1}^N \mathrm{sim}(\mathbf{o}_{\mathrm{loc},i}, \mathbf{p}_i) + \mathrm{sim}(\mathbf{o}_{\mathrm{glob}}, \mathbf{c}) \right)$$

该对齐损失结构化隐空间，使相近语义的图像在隐空间中邻近分布。消融实验表明，同时包含随机掩码、语义掩码和表示对齐时，gFID 最低且重建质量最佳（Table 5）；移除表示对齐后，隐空间结构明显退化（Figure 5）。线性探测准确率随训练持续提升（Figure 6a），进一步验证了表示对齐对隐空间语义质量的持续改善。

### 方法谱系与知识库定位

MacTok 属于连续分词器（continuous tokenizer）家族，其基线包括 **KL-VAE**（plain）、**VA-VAE**、**MAETok**、**SoftVQ-VAE**、**SD-VAE**、**MAR-VAE** 和 **l-DeTok**（Table 3）。与这些方法相比，MacTok 的差异化在于：**将掩码从隐空间移至图像空间**（changed slot: masking_strategy），并**引入 DINOv2 引导的语义掩码与双粒度表示对齐**（changed slot: representation_alignment）。这两个 changed slots 协同作用，使 MacTok 在仅用 128 tokens 时即达到 rFID 0.43，并在 ImageNet 256×256 上以 SiT-XL 实现 gFID 1.44（w/ CFG），在 512×512 上实现 gFID 1.52（w/ CFG），均达到当时最优水平（Table 1, Table 2）。最大掩码比率 $M=0.7$ 时生成性能最佳，继续增大掩码率会轻微损害质量（Table 4），表明存在一个信息压缩与重建难度的最优平衡点。

**需要手动验证**：文中未提供 MacTok 在更大 token 数（如 256、512）下的性能表现，因此该方法在弱压缩场景下的优势尚不明确。此外，随机掩码与语义掩码的最优混合比例（50%）是否跨数据集泛化，仍需进一步实验确认。

MacTok 的整体框架围绕一个核心矛盾展开：**如何让一个强压缩的连续分词器在仅有极少量隐 token 的情况下，仍然保留足够的判别性信息，从而避免后验坍塌。** 其解决方案由三条相互协同的技术路径构成——输入端的图像掩码、隐空间端的表示对齐，以及输出端的辅助监督——共同形成一个从“信息不对称”到“语义结构化”的完整闭环。

### 框架总览

MacTok 采用标准的 ViT 编码器-解码器架构（Figure 4）。编码器接收图像 patch 和可学习的隐 token，输出后验分布参数 $(\mu, \sigma)$ 并采样隐向量 $\hat{\mathbf{z}}$；解码器则从该隐向量重建完整图像。框架的关键创新不在于编码器-解码器本身，而在于**输入端的信息扰动**和**隐空间的语义约束**。

![[assets/figures/papers/paper_list_l16_https_arxiv_org_abs_2603_29634/figures/004_Figure_4.jpg]]
*Figure 4: Overview of the MacTok framework. Top: Transformer-based encoder and decoder operating on image, latent, and mask tokens. Bottom left: DINO-guided image masking introduces semantic priors. Bottom center: Global and local representation alignment between latent and pretrained visual representations. Bottom right: Discriminator and perceptual networks provide auxiliary supervision*

### 核心模块与数据流

**1. 输入掩码模块（信息不对称的创造者）**

图像在进入编码器之前，首先经过掩码处理。MacTok 设计了两种互补的掩码策略，以**等概率**随机选择其一执行：

- **随机掩码（Random Masking）**：随机替换一定比例的图像 patch 为可学习的 mask token，最大掩码比率 $M = 0.7$，实际掩码比率在 $[0, M]$ 范围内动态采样。这使得编码器只能看到部分图像内容，但解码器仍需重建完整图像，从而**强迫隐变量编码足够的信息**以弥补缺失。
- **DINO 语义掩码（DINO Semantic Masking）**：利用冻结的 DINOv2 模型提取图像的 patch token $\mathbf{p}_i$ 和 CLS token $\mathbf{c}$，计算余弦相似度作为每个 patch 的语义重要性评分：
  $$s_i = \frac{\mathbf{c}^\top \mathbf{p}_i}{\|\mathbf{c}\| \|\mathbf{p}_i\|}$$
  然后通过 Top-K 选择语义最相关的 patch 进行掩码：
  $$M_p = \mathrm{TopK}(\{s_i\}_{i=1}^N, \lfloor m \times N \rfloor)$$
  这一策略将图像空间的**语义先验迁移至隐空间**，迫使模型关注并编码最具判别性的视觉信息。

**2. 表示对齐模块（隐空间的结构化约束）**

编码器输出的隐向量 $\hat{\mathbf{z}} \in \mathbb{R}^{L \times d}$ 通过两个并行的对齐路径与 DINOv2 的预训练特征空间建立联系：

- **局部表示对齐**：将 $L$ 个隐 token 每个重复 $r = N/L$ 次，扩展至与 DINOv2 patch token 相同的粒度：$\tilde{\mathbf{z}}_{\mathrm{loc}} = \mathrm{Expand}(\hat{\mathbf{z}}, r)$。随后通过轻量 MLP 投影到 DINOv2 特征空间，与对应的 patch token 计算余弦相似度损失。
- **全局表示对齐**：对 $L$ 个隐 token 取平均得到全局表示：$\tilde{\mathbf{z}}_{\mathrm{glob}} = \frac{1}{L} \sum_{i=1}^L \hat{\mathbf{z}}_i$，同样经 MLP 投影后与 DINOv2 的 CLS token 对齐。

表示对齐损失为局部与全局余弦相似度的负均值：
$$L_{\mathrm{RA}} = -\frac{1}{N+1} \left( \sum_{i=1}^N \mathrm{sim}(\mathbf{o}_{\mathrm{loc},i}, \mathbf{p}_i) + \mathrm{sim}(\mathbf{o}_{\mathrm{glob}}, \mathbf{c}) \right)$$

该模块的核心作用是**将隐空间结构化**，使其与预训练视觉特征的语义结构保持一致，从而在强压缩下仍能保留类别判别性信息。

**3. 辅助监督模块（生成质量的保障）**

解码器输出端引入两个辅助网络：

- **判别器（Discriminator）**：提供对抗损失 $L_{\mathrm{adv}}$，提升重建图像的逼真度。
- **感知损失（Perceptual Loss）**：在预训练特征空间中度量重建图像与原始图像的感知差异 $L_{\mathrm{percep}}$。

### 训练目标

总损失函数为各模块损失的加权和：
$$L = L_{\mathrm{recon}} + \lambda_{1} L_{\mathrm{percep}} + \lambda_{2} L_{\mathrm{adv}} + \lambda_{3} L_{\mathrm{KL}} + \lambda_{4} L_{\mathrm{RA}}$$
其中 $\lambda_{1}=1.0$，$\lambda_{2}=0.2$，$\lambda_{3}=10^{-6}$，$\lambda_{4}=0.1$。极小的 KL 权重（$10^{-6}$）是防止后验坍塌的关键设计选择，它允许隐变量偏离先验以保留信息，而掩码和表示对齐则确保这种偏离是有结构的而非随机的。

### 关键因果机制

框架的有效性建立在两条因果链上：

1. **掩码 → 信息不对称 → 隐变量信息量提升**：编码器只能看到部分图像，解码器却需重建全部内容，这种信息缺口迫使隐变量编码尽可能多的判别性特征。消融实验（Table 5）表明，仅图像 token 掩码（而非隐 token 掩码）能持久防止后验坍塌，并产生结构良好的隐空间（Figure 1）。

2. **表示对齐 → 隐空间结构化 → 压缩下的语义保真**：通过将隐空间与 DINOv2 的语义空间对齐，即使 token 数极少（如 64 或 128），隐变量仍能保留类别级别的判别性信息，这一点由线性探测准确率随训练持续提升所验证（Figure 6）。

MacTok 的核心架构由 **ViT 编码器-解码器**、**双重掩码策略**、**表示对齐模块**和**辅助监督**四大组件构成（Figure 4），其设计目标是在极低 token 数（64/128）下防止后验坍塌，同时保持隐空间的语义结构。

### 3.1 ViT 编码器-解码器

MacTok 采用 Vision Transformer（ViT）作为编码器 $E$ 和解码器 $D$ 的骨干网络。编码器接收图像 patch 和一组可学习的隐 token，输出后验分布参数 $(\mu, \sigma)$，并通过重参数化技巧采样隐向量 $\hat{\mathbf{z}}$；解码器则从该隐向量重建完整图像。与标准 KL-VAE 的关键区别在于，编码器并非始终看到完整图像——输入在进入编码器前会经过掩码处理。

### 3.2 双重掩码策略

掩码是 MacTok 防止后验坍塌的核心机制。与直接在隐空间丢弃 token 不同，MacTok 在**图像空间**施加掩码，迫使编码器从部分观测中推断完整表示，从而创造信息不对称：编码器只能看到部分图像，解码器却需重建全部内容。

#### 3.2.1 随机掩码

随机掩码以一定比例将输入图像 patch 替换为可学习的 mask token。掩码比率 $m$ 在训练时从 $[0, M]$ 区间动态采样，其中 $M$ 为最大掩码比率。消融实验表明 $M=0.7$ 时生成性能最优（Table 4）。

#### 3.2.2 DINO 语义掩码

语义掩码利用预训练 DINOv2 模型将图像空间的语义先验迁移至隐空间。具体而言，对于输入图像，DINOv2 提取分类 token $\mathbf{c}$ 和 patch token $\{\mathbf{p}_i\}_{i=1}^N$，每个 patch 的语义重要性通过余弦相似度计算：

$$s_i = \frac{\mathbf{c}^\top \mathbf{p}_i}{\|\mathbf{c}\| \|\mathbf{p}_i\|}$$

其中 $s_i$ 表示 patch $i$ 与全局语义的相关性得分。随后选择得分最高的 $\lfloor m \times N \rfloor$ 个 patch 进行掩码：

$$M_p = \mathrm{TopK}(\{s_i\}_{i=1}^N, \lfloor m \times N \rfloor)$$

训练时，随机掩码与语义掩码以**等概率**（各 50%）随机选用。消融实验证实，这种混合策略（dino 50%）比纯语义掩码（dino 100%）或纯随机掩码获得更低的 gFID（Table 4）。

### 3.3 表示对齐

表示对齐模块将隐空间与 DINOv2 的预训练视觉特征对齐，进一步结构化隐空间。

**局部对齐**：首先将 $L$ 个隐 token $\hat{\mathbf{z}}$ 扩展至 patch 粒度，每个隐 token 重复 $r = N/L$ 次：

$$\tilde{\mathbf{z}}_{\mathrm{loc}} = \mathrm{Expand}(\hat{\mathbf{z}}, r)$$

**全局对齐**：对 $L$ 个隐 token 取平均，得到全局图像表示：

$$\tilde{\mathbf{z}}_{\mathrm{glob}} = \frac{1}{L} \sum_{i=1}^L \hat{\mathbf{z}}_i$$

随后通过两个轻量 MLP 将局部和全局特征投影到 DINOv2 的特征空间：

$$\mathbf{o}_{\mathrm{loc}} = \mathrm{MLP}_1(\tilde{\mathbf{z}}_{\mathrm{loc}}), \quad \mathbf{o}_{\mathrm{glob}} = \mathrm{MLP}_2(\tilde{\mathbf{z}}_{\mathrm{glob}})$$

表示对齐损失鼓励投影特征与 DINOv2 参考特征余弦相似：

$$L_{\mathrm{RA}} = -\frac{1}{N+1} \left( \sum_{i=1}^N \mathrm{sim}(\mathbf{o}_{\mathrm{loc},i}, \mathbf{p}_i) + \mathrm{sim}(\mathbf{o}_{\mathrm{glob}}, \mathbf{c}) \right)$$

该损失同时约束 patch 级局部语义和图像级全局语义的一致性。

### 3.4 辅助监督与总损失

除上述模块外，MacTok 还引入判别器提供对抗损失 $L_{\mathrm{adv}}$，以及感知损失 $L_{\mathrm{percep}}$ 在预训练特征空间中度量重建差异。总损失函数为各项加权和：

$$L = L_{\mathrm{recon}} + \lambda_{1} L_{\mathrm{percep}} + \lambda_{2} L_{\mathrm{adv}} + \lambda_{3} L_{\mathrm{KL}} + \lambda_{4} L_{\mathrm{RA}}$$

其中权重设置为 $\lambda_1=1.0$，$\lambda_2=0.2$，$\lambda_3=10^{-6}$，$\lambda_4=0.1$。极小的 KL 权重（$10^{-6}$）是防止后验坍塌的关键——过强的 KL 正则化会迫使隐分布趋近无信息先验，而掩码重建与表示对齐提供的结构化信号使得模型即使在弱 KL 约束下也能学到有意义的隐表示。

![[assets/figures/papers/paper_list_l16_https_arxiv_org_abs_2603_29634/figures/010_Figure_5.jpg]]
*Figure 5: Visualization of latent space from (a) Collapsed; (b) MacTok-128 trained without representation alignment; (c) MacTok-128*

## 实验与关键发现

### 核心瓶颈：后验坍塌与压缩困境

KL-VAE 在追求高压缩率（即极少的隐 token 数）时面临一个根本性困境：后验坍塌（posterior collapse）。此时编码器输出的隐变量分布趋近于无信息的高斯先验，丧失了保留判别性图像特征的能力，导致重建保真度和下游生成质量急剧下降。这一现象在 MacTok 中被明确验证：普通 KL-VAE 在强压缩设置下，其 KL 损失迅速衰减至零，隐空间结构崩塌（Figure 1 右半部分），重建结果严重模糊（Figure 11）。

### 因果机制：掩码创造信息不对称

MacTok 的核心设计在于通过图像空间的掩码重建，强制编码器从部分观测中推断完整图像，从而打破后验坍塌的恶性循环。这一机制的关键因果链条如下：

1. **信息不对称**：编码器只能看到被随机掩码或语义掩码破坏的部分图像 patch，但解码器仍需重建完整图像。这种输入与输出之间的信息差，迫使隐变量必须编码足够丰富的图像信息，而非退化为先验噪声。
2. **图像 token 掩码 vs 隐 token 掩码**：Figure 1 左侧对比了三种策略——普通 KL-VAE（无掩码）、隐 token 掩码（在隐空间丢弃 token）和图像 token 掩码。**仅图像 token 掩码能持续防止后验坍塌**，而隐 token 掩码与无掩码方案均迅速坍塌。这表明掩码必须作用于编码器输入端的信息瓶颈，而非隐空间本身。
3. **语义掩码的补充作用**：DINOv2 引导的语义掩码（Sec 3.2）根据 patch 与 CLS token 的余弦相似度 $s_i = \frac{\mathbf{c}^\top \mathbf{p}_i}{\|\mathbf{c}\| \|\mathbf{p}_i\|}$ 选择语义最相关的 patch 进行掩码，将图像空间的语义先验迁移至隐空间。Figure 3 显示，语义掩码能在随机掩码基础上进一步降低 gFID。

### 表示对齐的结构化作用

掩码策略解决了“信息编码”问题，但隐空间的结构化程度同样关键。MacTok 引入全局和局部表示对齐（Sec 3.3），将隐 token 映射到 DINOv2 预训练特征空间：

- **局部对齐**：将 $L$ 个隐 token 扩展至 patch 粒度，与 DINOv2 patch token 计算余弦相似度损失。
- **全局对齐**：隐 token 平均池化后与 DINOv2 CLS token 对齐。

Figure 5 的可视化表明，无表示对齐的 MacTok 隐空间结构较差，而完整 MacTok 的隐空间呈现出清晰的类别结构与良好的多样性。Figure 8 进一步在 64 tokens 设置下验证了这一结论。线性探测实验（Figure 6a）显示，MacTok 的隐空间判别能力随训练步数持续提升，与生成性能（Figure 6b）呈正相关。

![[assets/figures/papers/paper_list_l16_https_arxiv_org_abs_2603_29634/figures/014_Figure_8.jpg]]
*Figure 8: Visualization of laten space from (a) MacTok-64 trained without Representation alignment; (b) MacTok-64*

### 主实验结果

**ImageNet 256×256 条件生成**（Table 1）：MacTok-128 配合 SiT-XL 生成器在 CFG 设置下达到 gFID 1.44，显著优于 SD-VAE（1024 tokens, gFID 2.06），同时 token 数减少 8 倍。MacTok-128 配合 LightningDiT-XL 亦达到 gFID 1.50。在重建质量上，MacTok-128 的 rFID 为 0.43，优于 SD-VAE 的 0.62。

**ImageNet 512×512 条件生成**（Table 2）：MacTok-128 配合 SiT-XL 达到 gFID 1.52（CFG），较 SD-VAE（4096 tokens, gFID 2.62）提升 1.10，token 数减少 32 倍。MacTok-64 同样取得 gFID 1.87 的强结果。

**连续分词器对比**（Table 3）：在与 VA-VAE、MAETok、SoftVQ-VAE、SD-VAE、MAR-VAE、l-DeTok 等连续分词器的系统对比中，MacTok 在压缩率与重建质量的平衡上表现最优，且下游生成性能全面领先。

### 消融实验

**掩码比率与语义掩码比例**（Table 4, Figure 3）：最大掩码比率 $M=0.7$ 时生成性能最佳；继续增大至 $M=0.8$ 会轻微损害质量。在语义掩码比例上，随机掩码与语义掩码等概率混合（dino 50%）优于纯语义掩码（dino 100%）或纯随机掩码，表明两种掩码策略具有互补性。

**模块消融**（Table 5）：同时包含随机掩码、语义掩码和表示对齐时，gFID 最低（3.15，无 CFG），重建质量最佳（rFID 0.47）。移除任一模块均导致性能退化，验证了各模块的必要性。

**解码器微调与模型规模**（Table 6）：解码器微调可进一步提升重建和生成质量；增大 MacTok 模型规模（从 ViT-Base 到 ViT-Large）亦带来一致的性能增益。

### 关键图表结论

- **Figure 1**：图像 token 掩码是防止后验坍塌的必要条件，隐 token 掩码无效。
- **Figure 3**：掩码比率和语义掩码比例存在最优配置，等概率混合效果最好。
- **Figure 5/8**：表示对齐显著改善隐空间结构，使其呈现清晰的语义聚类。
- **Figure 6**：隐空间判别能力与生成性能随训练同步提升，表明两者存在内在关联。
- **Table 1/2**：MacTok 在 256×256 和 512×512 分辨率上均以极少 token 数取得当时最优生成质量。

![[assets/figures/papers/paper_list_l16_https_arxiv_org_abs_2603_29634/figures/005_Table_1.jpg]]
*Table 1: System-level comparison on ImageNet 256×256 conditional generation. “# Params (G)” denotes generator parameters; “Tok. Model” refers to the tokenizer model type; “Token Type” indicates 1D or 2D tokenization; “# Params (T)” denotes tokenizer parameters; and “# Tokens” represents the number of latent tokens. ‡ denotes methods that rely on pretrained vision models*

### 失败模式与局限

论文未明确报告失败案例或负面结果。从方法机理推断，MacTok 的性能依赖于 DINOv2 预训练特征的质量，在 DINOv2 表征能力较弱的数据域（如医学影像、遥感图像等与 ImageNet 分布差异较大的场景）上，语义掩码和表示对齐的有效性可能下降。此外，掩码比率和语义掩码比例的最优配置可能随数据集和 token 数变化，需额外调参。这些问题在论文中作为开放问题提出，但未进行实验验证，需在实际应用中手动确认。

![[assets/figures/papers/paper_list_l16_https_arxiv_org_abs_2603_29634/figures/006_Table_2.jpg]]
*Table 2: System-level comparison on ImageNet 512×512 conditional generation. SiT-XL trained with MacTok achieves state-of-the-art generation performance using only 64 and 128 tokens (†: Large decoder for fair comparison; ‡: relies on pretrained vision models)*

![[assets/figures/papers/paper_list_l16_https_arxiv_org_abs_2603_29634/figures/009_Table_4.jpg]]
*Table 4: Ablation on maximum mask ratio M (w/o Decoder Finetuning). MacTok is evaluated over mask ratios from 0.4 to 0.8 and different DINO-guided semantic masking settings: “dino 100%” denotes full use of DINO-guided semantic masking, while “dino 50%” applies random and semantic masking with equal probability. Generation performance is reported without CFG*

## 定位与知识库关联

### 与基线方法的关系

MacTok 的核心贡献在于解决连续分词器（continuous tokenizer）在强压缩条件下的**后验坍塌（posterior collapse）**问题。传统的 KL-VAE 在将图像压缩至极少量 token（如 64 或 128 个）时，编码器输出的隐变量会退化为无信息的高斯先验，导致重建和生成质量急剧下降。MacTok 通过两个关键机制突破这一瓶颈：**图像空间的掩码重建**和**基于预训练视觉特征的表示对齐**。

与现有连续分词器的对比中，MacTok 显示出显著优势。**SD-VAE**（Stable Diffusion 使用的分词器）通常需要 1024 个 token 来表示 256×256 图像，而 MacTok 仅用 128 个 token 即可实现更优的重建质量（rFID 0.43 vs 0.62）和生成性能（gFID 1.44 vs 2.06，均使用 SiT-XL 生成器，Table 1）。**VA-VAE**、**MAETok**、**SoftVQ-VAE**、**MAR-VAE** 和 **l-DeTok** 等连续分词器在相同 ViT-Base 骨架和 SiT-B 生成器的公平比较下，MacTok 在重建-压缩权衡和生成质量上均达到最优（Table 3）。特别值得注意的是，MacTok 在仅使用 64 个 token 时，其无 CFG 的 gFID 比 SoftVQ-VAE 低 2.21（Table 2 相关文本）。

MacTok 与**掩码自编码器（MAE）**系列工作的关系值得深入辨析。MAE 通过随机掩码图像 patch 进行自监督预训练，证明了从部分观测中重建完整图像可以学习到鲁棒的视觉表示。MacTok 将这一思想迁移到分词器训练中，但目标不同：MAE 追求的是下游任务的迁移能力，而 MacTok 追求的是隐空间的信息密度和结构质量。关键区别在于，MacTok 的掩码发生在**编码器输入端**（图像 token 掩码），而非隐空间（latent token 掩码）。论文通过 Figure 1 和 Figure 7 的 KL 损失曲线明确证明：仅图像 token 掩码能持久防止后验坍塌，而隐 token 掩码则无法阻止 KL 损失快速下降至零——这是后验坍塌的明确信号。

在表示对齐方面，MacTok 借鉴了知识蒸馏的思想，但与典型的知识蒸馏（如 CLIP 或 DINO 蒸馏到生成模型）不同，MacTok 的对齐发生在**分词器的隐空间**而非生成器。通过将隐 token 扩展至 patch 粒度并与 DINOv2 的 patch token 进行局部对齐，同时将隐 token 平均池化后与 DINOv2 的 CLS token 进行全局对齐，MacTok 将预训练视觉模型的语义先验结构化地注入隐空间。Figure 5 和 Figure 8 的 t-SNE 可视化清晰展示了这一效果：无表示对齐的 MacTok 隐空间结构模糊，而完整 MacTok 的隐空间呈现出清晰的类别聚类。

### 适用边界与局限

MacTok 的设计和验证主要集中在以下条件下：

1. **压缩率**：论文验证了 64 和 128 个 token 的设置（对应 256×256 分辨率下 16× 和 32× 压缩），在更高 token 数（如 256 或 512）下，后验坍塌问题本身可能不那么严重，MacTok 的增益幅度需要进一步验证。论文未报告更高 token 数的实验。

2. **数据模态**：所有实验均在 ImageNet 自然图像上进行。掩码策略和 DINOv2 语义先验在医学影像、遥感图像、工业检测等领域的有效性尚未验证。DINOv2 的特征空间在这些域上的语义质量可能下降，从而影响语义掩码和表示对齐的效果。

3. **生成器依赖**：MacTok 本身是分词器，其生成性能通过 SiT-XL、LightningDiT-XL 等扩散/流匹配生成器评估。不同生成器架构对 MacTok 隐空间的利用效率可能存在差异，论文未对此进行系统消融。

4. **最优掩码比例**：Table 4 显示最大掩码比率 M=0.7 时性能最佳，且随机掩码与语义掩码以等概率混合（dino 50%）优于纯语义掩码（dino 100%）。但这一最优比例可能依赖于数据集和分辨率，论文未在不同数据集上验证其泛化性。

5. **计算开销**：MacTok 需要额外的 DINOv2 前向传播来计算语义掩码和表示对齐损失，这增加了训练成本。论文未详细报告训练时间或计算资源消耗的对比数据。

### 开放问题

1. **跨模态泛化**：MacTok 的掩码策略和表示对齐机制能否推广到视频、3D 点云或多模态数据？不同模态的语义先验来源（如视频的时序一致性、点云的几何结构）如何设计？

2. **最优掩码策略的自适应**：随机掩码与语义掩码的最优比例是否可以通过学习得到，而非固定的 50%？不同训练阶段是否需要不同的掩码策略？

3. **与离散分词器的桥接**：MacTok 是连续分词器，其掩码策略能否迁移到 VQ-VAE 等离散分词器中？离散隐空间的码本坍塌问题与连续空间的后验坍塌是否有共同的解决路径？

4. **更大规模验证**：在更高分辨率（如 1024×1024）和更大规模数据集（如 LAION-5B）上，MacTok 的掩码策略是否仍然有效？压缩率与语义保真度的权衡曲线如何变化？

5. **表示对齐的替代方案**：除 DINOv2 外，CLIP、SigLIP 等多模态模型的特征空间是否更适合作为对齐目标？多模态对齐能否进一步提升生成多样性？

## 原文 PDF

![[paperPDFs/CVPR_2026/MacTok_Robust_Continuous_Tokenization_for_Image_Generation.pdf]]
