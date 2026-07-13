---
title: "EmerDiff: Emerging Pixel-level Semantic Knowledge in Diffusion Models"
type: paper
paper_level: A
venue: ICLR
year: 2024
pdf_ref: paperPDFs/ICLR_2024/EmerDiff_Emerging_Pixel_level_Semantic_Knowledge_in_Diffusion_Models.pdf
project_link: https://kmcode1.github.io/Projects/EmerDiff/
code_link: null
aliases:
- EmerDiff
tags:
- ICLR_2024
- topic/generative_models_diffusion
- topic/generative_models_diffusion/diffusion_image_video
core_operator: "通过对低维特征图的一个子区域施加扰动（在跨注意力层中添加偏移量cM），观察生成图像中哪些像素发生显著变化，从而揭示语义对应。"
primary_logic: "通过分析扩散模型从低分辨率特征图生成高分辨率图像的机制，发现扰动特征图的局部区域只会显著改变与之语义相关的图像像素，因此可以利用这种对应关系将低分辨率分割掩码上采样为像素级精细分割图。"
claims:
- "扰动低分辨率掩码区域后，只有语义相关的像素在差异图中响应明显。"
- "所提方法在多个数据集上显著优于朴素上采样基线（SD），验证了语义对应上采样的有效性。"
- "生成的精细分割图远比朴素上采样的低分辨率掩模清晰。"
- "ADE20K (AD150) 上 mIoU = 33.1"
---

# EmerDiff: Emerging Pixel-level Semantic Knowledge in Diffusion Models

> [!tip] 核心洞察
> 通过分析扩散模型从低分辨率特征图生成高分辨率图像的机制，发现扰动特征图的局部区域只会显著改变与之语义相关的图像像素，因此可以利用这种对应关系将低分辨率分割掩码上采样为像素级精细分割图。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | EmerDiff：扩散模型中涌现的像素级语义知识 |
| 英文题名 | EmerDiff: Emerging Pixel-level Semantic Knowledge in Diffusion Models |
| 会议/期刊 | ICLR 2024 |
| Links | [paper](https://arxiv.org/abs/2401.11739) · [Project](https://kmcode1.github.io/Projects/EmerDiff/) |
| Topic | #topic/generative_models_diffusion #topic/generative_models_diffusion/diffusion_image_video |
| Method | EmerDiff |
| Dataset | ADE20K (AD150), COCO-Stuff (CS171), COCO-Stuff-27 |

> [!tip] 效果简介
> - ADE20K (AD150) 上，mIoU 为 33.1，对比 29.1 (SD)，变化 +4.0。
> - COCO-Stuff (CS171) 上，mIoU 为 30.5，对比 27.6 (SD)，变化 +2.9。
> - COCO-Stuff-27 上，mIoU (传统评估) 为 26.6，对比 26.8 (STEGO)，变化 -0.2。

## 概要

### 问题瓶颈

预训练扩散模型（如 Stable Diffusion）已被证明其内部特征图包含丰富的语义信息，可用于语义分割等下游任务。然而，这些有意义的语义特征图通常存在于空间分辨率较低的层（如 16×16），直接将其上采样到原图分辨率会丢失大量空间细节，难以提取像素级的精细语义关系。核心瓶颈在于：**如何从低维特征图中恢复出高分辨率的像素级语义对应，从而构建精细的分割掩码**。

### 核心发现

EmerDiff 揭示了一个关键现象：**当对低分辨率特征图的某个子区域施加扰动时，生成图像中只有与该子区域语义相关的像素会发生显著变化，其余像素几乎保持不变**。这一“涌现”的语义对应关系表明，扩散模型在从低分辨率特征图生成高分辨率图像的过程中，隐式地编码了像素与低维空间位置之间的语义映射。基于此，EmerDiff 通过“调制去噪”过程来显式地揭示这种对应，并将低分辨率分割掩码上采样为像素级的精细分割图。

### 方法定位

EmerDiff 是一种**完全无监督的图像分割框架**，仅依赖预训练扩散模型中已蕴含的语义知识，无需任何额外训练或人工标注。其方法谱系与知识库定位如下：

| 方法 | 核心思路 | 与 EmerDiff 的关系 |
|------|----------|-------------------|
| **SD (朴素上采样)** | 直接从 SD 特征图通过双线性插值获得分割掩码 | 基线：使用相同的 SD 特征图，但缺乏语义对应上采样机制 |
| **STEGO** (Hamilton et al., ICLR 2022) | 通过对比学习对齐特征与语义 | 无监督分割基线，EmerDiff 在传统评估协议下与之可比 |
| **DINOSAUR** (Seitzer et al., 2022) | 基于 DINO 特征的无监督分割 | 无监督分割基线 |
| **MaskCLIP** (Zhou et al., ECCV 2022) | 利用 CLIP 进行开放词汇分割 | 无标注开放词汇分割基线，EmerDiff 可与其结合提升细粒度 |
| **TCL** (Cha et al., 2023) | 文本条件对齐的开放词汇分割 | 同上，EmerDiff 作为掩码细化模块叠加 |
| **CLIPpy** (Ranasinghe et al., 2023) | 基于 CLIP 的开放词汇分割 | 同上 |

EmerDiff 的核心创新在于将**低分辨率到高分辨率的映射策略**从朴素的双线性插值替换为**通过调制去噪寻找语义对应并分配像素**。这一策略变化使得分割掩码从粗糙的块状上采样结果转变为清晰保留物体边界的精细分割图。

### 主要结果

- **无监督语义分割**：在修改后的评估协议下，EmerDiff 在 ADE20K (AD150) 上达到 33.1 mIoU，相比 SD 朴素上采样基线（29.1）提升 +4.0；在 COCO-Stuff (CS171) 上达到 30.5 mIoU，提升 +2.9（Table 2）。
- **传统评估协议**：在 COCO-Stuff-27 上达到 26.6 mIoU，与 STEGO（26.8）可比（Table 1），但传统协议因类别定义粗粒度而低估了 EmerDiff 的细粒度分割能力。
- **开放词汇分割**：将 EmerDiff 的细粒度掩码与 MaskCLIP、TCL、CLIPpy 等基线的文本对齐嵌入结合后，各基线性能均获得一致提升（Table 3）。
- **定性结果**：生成的精细分割图远比朴素上采样的低分辨率掩模清晰，能够准确勾勒物体边界（Figure 4）。

### 局限与展望

EmerDiff 存在以下局限：难以区分极小对象（如动物腿部、人脸细节），因为细节信息在低维层中被压缩；特征表示中可能混杂空间位置和颜色属性，导致天空、地面等同质区域被过度分割。未来方向包括将调制语义特征的思路推广至其他生成模型（如 GAN），以及利用生成的掩码作为伪标签进行弱监督语义分割以减少标注需求。



图像语义分割旨在为图像中的每一个像素分配一个语义类别标签，是计算机视觉领域的一项基础任务。传统的分割方法依赖大量像素级人工标注进行监督训练，成本高昂且难以扩展。近年来，自监督和无监督分割方法试图摆脱对密集标注的依赖，但它们通常需要在大规模无标注数据上进行额外的训练，或者依赖于专门设计的自监督代理任务。

与此同时，以 Stable Diffusion 为代表的文本到图像扩散模型展现出惊人的生成能力。这些模型在数十亿图文对上预训练后，不仅能够合成高质量图像，其内部表征也被发现蕴含丰富的语义信息。然而，一个关键瓶颈在于：扩散模型中有意义的语义特征图通常存在于空间分辨率较低的中间层（如 16×16 的特征图），这些低维表征虽然能捕捉图像的全局语义结构，却难以直接提取像素级的精细语义关系，导致无法直接用于高分辨率的分割任务。

现有利用扩散模型进行语义分割的尝试，大多采用朴素的双线性插值将低分辨率特征图上采样到原图尺寸，得到的掩码边界粗糙、细节模糊，难以刻画物体的精确轮廓。这一现象引出一个核心问题：**预训练的扩散模型是否本身就具备像素级的语义理解能力？如果具备，又该如何将其提取出来？**

本文正是从这一问题出发，探索扩散模型从低分辨率特征图生成高分辨率图像的内在机制。作者发现，当对低维特征图的一个子区域施加扰动时，生成图像中只有与该子区域语义相关的像素会发生显著变化，而其他像素几乎保持不变。这一观察揭示了扩散模型内部存在一种隐式的“语义对应”关系——低分辨率特征图上的每一个空间位置，都与高分辨率图像中一组语义相关的像素紧密关联。基于这一核心洞察，EmerDiff 提出了一种无需任何额外训练或标注的框架，利用这种语义对应关系将低分辨率分割掩码“上采样”为像素级的精细分割图，从而首次从预训练扩散模型中提取出高精度的像素级语义知识。



## 核心方法与创新机理

EmerDiff 的核心创新在于**将扩散模型从低分辨率特征图生成高分辨率图像的机制，转化为一种天然的语义对应上采样器**，从而绕过了传统无监督分割中“低维语义特征图与高维像素空间难以对齐”的根本瓶颈。

### 关键机制：从“调制去噪”到“语义对应”

预训练的 Stable Diffusion 模型在空间低维层（如 16×16）中蕴含丰富的语义特征，但这些特征图的分辨率远低于目标图像，直接通过双线性插值上采样得到的掩码粗糙且难以解释（Figure 4）。EmerDiff 的关键洞察是：**当对低维特征图的某个子区域施加扰动时，生成图像中只有与该区域语义相关的像素会发生显著变化**（confidence 0.95）。这一因果特性使得“语义对应”可以被显式测量。

具体而言，EmerDiff 在跨注意力层引入一个可调的偏移量 $cM$，其中 $M$ 为低分辨率二进制掩码：

$$f\left(\sigma\left(\frac{QK^T}{\sqrt{d}}\right) \cdot V\right) + cM \in \mathbb{R}^{hw \times d}$$

通过分别施加正负偏移（$c = -\lambda, +\lambda$）并执行两次调制去噪，得到两幅修改后的图像 $I^-$ 和 $I^+$。二者的欧氏距离差异图 $d = ||I^- - I^+||_2 \in \mathbb{R}^{H \times W}$ 直接量化了每个像素与扰动区域之间的语义对应强度。像素标签分配遵循 $k = \mathrm{argmax}_i d_{x,y}^i$，即将每个像素分配给语义对应最强的低分辨率掩码。

### Changed Slot：映射策略的根本性重构

| 维度 | 基线方法（SD naive upsampling） | EmerDiff（本文） |
|------|-------------------------------|------------------|
| 低分辨率 → 高分辨率映射 | 双线性插值 | 通过调制去噪寻找语义对应并分配像素 |
| 证据强度 | — | confidence 0.95 |

这一 changed slot 的本质区别在于：**基线方法假设空间邻近性等于语义邻近性，而 EmerDiff 利用扩散模型自身的生成机制来显式揭示语义对应关系**。实验表明，这一策略在多个数据集上带来了一致且显著的提升：在 ADE20K (AD150) 上 mIoU 从 29.1 提升至 33.1（+4.0），在 COCO-Stuff (CS171) 上从 27.6 提升至 30.5（+2.9）（Table 2，confidence 0.98）。

### 辅助创新：注意力注入与高斯滤波

为保证调制去噪过程中图像结构不被破坏，EmerDiff 注入原始注意力图（固定 $QK^T$）以保持空间布局的稳定性。此外，对差异图施加高斯滤波以抑制像素化伪影。消融实验证实，注意力注入能有效保留更精细的物体结构，对分割性能有正向贡献（Table 9，confidence 0.98）。

### 与现有方法谱系的定位

EmerDiff 在无监督语义分割领域占据了一个独特位置：它**既不依赖自监督预训练的视觉编码器（如 DINO），也不依赖语言模型的文本监督（如 CLIP）**，而是纯粹从预训练扩散模型的生成机制中提取像素级语义知识。这使得它可以作为一种“即插即用”的细粒度分割前端，与现有的无标注开放词汇分割方法（如 **MaskCLIP** (Zhou et al., ECCV 2022)、**TCL** (Cha et al., 2023)、**CLIPpy** (Ranasinghe et al., 2023)）组合使用，为其粗糙的文本对齐像素嵌入提供精细的类别无关掩码（Table 3），从而产生文本对齐的细粒度分割结果。



![[assets/figures/papers/paper_list_l23_https_arxiv_org_abs_2401_11739/figures/002_Figure_2.jpg]]
*Figure 2: Overview of our framework. green: we first construct low-resolution segmentation maps by applying k-means on semantically meaningful low-dimensional feature maps. orange: Next, we generate image-resolution segmentation maps by mapping each pixel to the most semantically corresponding low-resolution mask, where semantic correspondences are identified by the modulated denoising process*

EmerDiff 的整体 pipeline 围绕一个核心洞察展开：**预训练扩散模型从低分辨率特征图生成高分辨率图像的过程中，隐式编码了像素级的语义对应关系**。通过“调制去噪”揭示这种对应，即可将粗糙的低分辨率分割掩码上采样为精细的图像分辨率分割图。

整个框架分为两个阶段（图 2）：

### 阶段一：低分辨率分割图构建（绿色分支）

1. **特征提取**：从 Stable Diffusion 的向上 16×16 模块块的第一层跨注意力层中提取查询向量，时间步设为 $t_f=1$（最小噪声），以获得语义最丰富的低维特征图。
2. **聚类生成掩码**：对提取的特征图应用 k-means 聚类，得到 $K$ 个聚类，作为低分辨率分割掩码（如 16×16）。每个掩码对应一个语义区域。

### 阶段二：图像分辨率分割图生成（橙色分支）

这是框架的核心创新，通过调制去噪过程将低分辨率掩码映射到高分辨率像素空间：

1. **调制去噪**：在时间步 $t_m=281$ 的特定跨注意力层，对低分辨率掩码 $M^i$ 施加偏移量 $cM$（$c = \pm\lambda$，$\lambda=10$），分别生成两张修改后的图像 $I^-$ 和 $I^+$。同时注入原始注意力图以保持图像结构。
2. **差异图计算**：计算两张图像在 RGB 维度上的欧氏距离，得到差异图 $d^i = \|I^- - I^+\|_2 \in \mathbb{R}^{H \times W}$，表示每个像素与掩码 $i$ 的语义对应强度。
3. **像素标签分配**：对每个像素 $(x,y)$，将其分配给对应强度最大的掩码：$k = \operatorname{argmax}_i d_{x,y}^i$。
4. **后处理**：对差异图应用高斯滤波以抑制像素化伪影。

### 关键机制：语义对应涌现

框架之所以有效，是因为一个经验发现：**扰动低分辨率特征图的某个子区域时，只有与该子区域语义相关的像素在生成图像中发生显著变化**，其余像素基本保持不变（图 3）。这一“因果杠杆”使得差异图天然成为语义对应强度的可靠度量，从而无需任何额外训练即可实现从低分辨率到高分辨率的语义上采样。

### 输入输出流

- **输入**：单张 RGB 图像
- **中间产物**：16×16 的低分辨率分割掩码（k-means 聚类结果）
- **输出**：与输入图像分辨率相同的精细分割图，每个像素被分配到一个语义掩码标签
- **可选扩展**：通过计算掩码嵌入（在掩码区域内平均 SD 特征图），可为每个掩码生成特征向量，用于后续的开放词汇分类或聚类评估



EmerDiff 的核心管线由两个阶段构成：**低分辨率语义掩码构建**与**像素级语义对应上采样**。第一阶段从扩散模型的低维特征图中提取语义分组；第二阶段通过调制去噪过程揭示低分辨率掩码与高分辨率像素之间的语义对应关系，从而将粗糙掩码上采样为精细分割图。

### 低分辨率语义掩码构建

该模块从预训练 Stable Diffusion 的跨注意力层中提取语义特征。具体而言，在时间步 $t_f = 1$（噪声最小），从向上采样的 16×16 模块块的第一层跨注意力层中提取查询向量（query vectors）。这些查询向量构成空间尺寸为 $h \times w$（如 16×16）的低维特征图，随后对其应用 k-means 聚类，得到 $K$ 个聚类，作为低分辨率语义掩码 $M^i \in \{0,1\}^{hw \times 1}$。

### 调制去噪与语义对应发现

这是方法的核心创新。给定一个低分辨率掩码 $M^i$，在特定时间步 $t_m$ 和特定跨注意力层中引入偏移量 $cM$，调制后的跨注意力输出为：

$$f\left(\sigma\left(\frac{QK^T}{\sqrt{d}}\right) \cdot V\right) + cM \in \mathbb{R}^{hw \times d}$$

其中 $Q$、$K$、$V$ 分别为查询、键、值矩阵，$d$ 为缩放因子，$\sigma$ 为 softmax 函数，$f$ 为输出投影，$c$ 为调制强度（取 $\pm\lambda$）。分别以 $c = -\lambda$ 和 $c = +\lambda$ 运行调制去噪过程，得到两张修改后的图像 $I^-$ 和 $I^+$。随后计算差异图：

$$d^i = \|I^- - I^+\|_2 \in \mathbb{R}^{H \times W}$$

差异图 $d^i$ 的每个空间位置 $(x,y)$ 的值表示该像素与低分辨率掩码 $i$ 之间的语义对应强度——受扰动影响的像素在差异图中响应显著，而语义无关的像素基本保持不变。这构成了从低维特征到高分辨率像素的语义映射桥梁。

### 像素标签分配

对每个低分辨率掩码 $i$ 重复上述过程得到差异图 $d^i$ 后，将每个像素 $(x,y)$ 分配给语义对应最强的掩码：

$$k = \mathrm{argmax}_i \, d_{x,y}^i$$

为保证生成图像的结构一致性，在调制去噪过程中注入原始注意力图（固定所有自注意力和跨注意力层的 $QK^T$），并对差异图应用高斯滤波以抑制像素化伪影。

### 掩码嵌入生成

在开放词汇分割场景中，需要为每个掩码生成语义嵌入。具体做法是：在掩码区域内对 Stable Diffusion 的低维特征图取平均，得到掩码嵌入 $e \in \mathbb{R}^c$，每个像素继承其所属掩码的嵌入向量。



## 实验与关键发现

### 主实验结果

EmerDiff 在无监督语义分割任务上展现出显著优势，尤其是在作者提出的**修改评估协议**下，该方法一致优于所有基线。该评估协议的核心改变在于：不再依赖匈牙利匹配，而是将属于同一真实类别的像素嵌入取平均作为概念嵌入，从而更精确地衡量分割的细粒度质量。

如表 2 所示，在 ADE20K (AD150) 上，EmerDiff 达到 33.1 mIoU，相比使用相同 Stable Diffusion 特征图但通过双线性插值朴素上采样的 SD 基线（29.1 mIoU）提升了 **+4.0 mIoU**。在 COCO-Stuff (CS171) 上，EmerDiff 达到 30.5 mIoU，相比 SD 基线（27.6 mIoU）提升 **+2.9 mIoU**。这一性能差距验证了语义对应上采样策略的有效性——通过调制去噪过程发现的像素到低分辨率掩码的对应关系，远比单纯的插值更精确。

![[assets/figures/papers/paper_list_l23_https_arxiv_org_abs_2401_11739/figures/008_Table_2.jpg]]
*Table 2: Results of unsupervised semantic segmentation under our modified evaluation strategy. Evaluated on ADE20K (AD150) (Zhou et al., 2019), PASCAL-Context (PC59, PC459) (Mottaghi et al., 2014), COCO-Stuff (CS171, CS27) (Caesar et al., 2018), and Cityscapes (City19) (Cordts et al., 2016). MDC (Cho et al., 2021), PiCIE (Cho et al., 2021), DINO, and STEGO are trained solely on images, while CLIP (Radford et al., 2021), TCL (Cha et al., 2023), and CLIPpy (Ranasinghe et al., 2023) are trained on text-image pairs. For CLIP, we follow Zhou et al. (2022) to modify the image encoder to output pixel-wise embeddings. For SD, we naively up-sample low-resolution segmentation maps (via bilinear interpolation,...*

在传统的匈牙利匹配评估协议下，EmerDiff 在 COCO-Stuff-27 上达到 26.6 mIoU，与 **STEGO**（Hamilton et al., ICLR 2022）的 26.8 mIoU 基本持平（-0.2 mIoU）。这一结果表明，即使在不依赖任何标注或额外训练的情况下，仅从预训练扩散模型中提取的语义知识也能达到与专用无监督分割方法相当的性能。

定性对比（Figure 4）进一步揭示了差异的本质：朴素上采样的分割图“粗糙且难以解释”，而 EmerDiff 生成的分割图“清晰得多”，能够精确勾勒物体边界。

### 无标注开放词汇分割

EmerDiff 生成的类无关精细掩码可以与现有无标注开放词汇分割模型的文本对齐像素嵌入相结合，产生类感知的精细分割图。如表 3 所示：

![[assets/figures/papers/paper_list_l23_https_arxiv_org_abs_2401_11739/figures/010_Table_3.jpg]]
*Table 3: Comparison between baselines and baselines + ours in annotation-free open vocabulary semantic segmentation. Evaluated on ADE20K(AD150) (Zhou et al., 2019), PASCAL-Context(PC59, PC459) (Mottaghi et al., 2014), COCO-Stuff(CS171) (Caesar et al., 2018), and Cityscapes(City19) (Cordts et al., 2016). For a fair comparison, we re-evaluate TCL, MaskCLIP, and CLIPpy with the same prompt engineering. The results of other works are also put for reference, where OVSegmentor is taken from the original paper, and GroupViT from Cha et al. (2023)*

- **MaskCLIP**（Zhou et al., ECCV 2022）结合 EmerDiff 后，在 ADE20K 上从 9.8 mIoU 提升至 15.9 mIoU，增益显著。
- **TCL**（Cha et al., 2023）结合 EmerDiff 后，在 ADE20K 上从 12.1 mIoU 提升至 17.4 mIoU，在 PASCAL-Context (PC59) 上从 28.9 mIoU 提升至 35.4 mIoU。
- **CLIPpy**（Ranasinghe et al., 2023）的增益较小（ADE20K 上从 12.0 升至 12.9），作者将其归因于 CLIPpy 像素嵌入的过度平滑特性，导致掩码嵌入的判别力不足。

这种互补性源于一个关键洞察：现有基线产生“文本对齐但粗糙”的像素嵌入，而 EmerDiff 产生“边界清晰但类无关”的掩码——二者的结合恰好弥补了各自的短板。

### 消融实验

**掩码数量 K 的影响**（Table 4）：当每个图像的聚类数量在 10–40 之间变化时，mIoU 仅出现微小波动，表明方法对掩码数量的选择不敏感，具有良好的鲁棒性。

![[assets/figures/papers/paper_list_l23_https_arxiv_org_abs_2401_11739/figures/015_Table_4.jpg]]
*Table 4: Effects of varying the number of masks on open-vocabulary segmentation and unsupervised semantic segmentation tasks*

**特征提取时间步**（Table 6）：随着提取特征图的时间步 $t_f$ 增大（即噪声增加），分割性能显著下降。这验证了低噪声条件下的特征图包含更丰富的语义信息，因此作者选择 $t_f=1$（最小噪声）。

![[assets/figures/papers/paper_list_l23_https_arxiv_org_abs_2401_11739/figures/018_Table_6.jpg]]
*Table 6: Varying the timestep of extracting feature maps. Evaluated on unsupervised semantic segmentation and open-vocabulary semantic segmentation (MaskCLIP + Ours) w/ ADE20K*

**调制时间步**（Table 7）：调制去噪过程在中间时间步（281–481）表现最佳。过早或过晚施加调制都会降低语义对应的质量，因为早期噪声过大而后期图像结构已基本定型。

![[assets/figures/papers/paper_list_l23_https_arxiv_org_abs_2401_11739/figures/020_Table_7.jpg]]
*Table 7: Varying the modulation timestep t _ { m } . . Evaluated on unsupervised semantic segmentation w/ ADE20K*

**调制强度 λ**（Table 8）：λ=10 时达到最高 mIoU，λ 继续增大性能略有下降，表明适度的扰动足以揭示语义对应，过强的调制可能引入伪影。

![[assets/figures/papers/paper_list_l23_https_arxiv_org_abs_2401_11739/figures/021_Table_8.jpg]]
*Table 8: Varying the modulation strength λ. Evaluated on unsupervised semantic segmentation w/ ADE20K*

**注意力注入**（Table 9）：在调制去噪过程中注入原始注意力图（即固定 $QK^T$）可提升分割性能，尤其能保留更精细的物体结构。移除注意力注入会导致性能下降，因为调制过程可能破坏生成图像的整体结构一致性。

![[assets/figures/papers/paper_list_l23_https_arxiv_org_abs_2401_11739/figures/023_Table_9.jpg]]
*Table 9: Ablating attention injection. Evaluated on unsupervised semantic segmentation and openvocabulary semantic segmentation (MaskCLIP + Ours) w/ ADE20K*

**跨注意力层选择**（Table 5）：从 16×16 向上模块的不同跨注意力层提取特征图，性能无显著差异，表明语义知识在该尺度的多个层中均有分布。

![[assets/figures/papers/paper_list_l23_https_arxiv_org_abs_2401_11739/figures/016_Table_5.jpg]]
*Table 5: Effects of extracting feature maps from each cross-attention layer in 16 × 16 upward block. Evaluated on ADE150K. No significant differences in performance*

### 失败模式与局限性

Figure 8 展示了典型失败案例：EmerDiff 偶尔无法区分**极小的对象**，如小桌子、动物腿、人脸局部细节。这是因为这些细节在 16×16 的低维特征层中已被高度压缩，难以保留足够的判别信息。

此外，由于 Stable Diffusion 的特征表示可能编码了空间位置和颜色属性，导致天空、地面等大面积均匀区域被过度分割。生成的掩码仍可能包含噪声，若用于弱监督下游任务（如语义分割的训练伪标签），需要进一步的后处理。

### 补充图表

![[assets/figures/papers/paper_list_l23_https_arxiv_org_abs_2401_11739/figures/006_Table_1.jpg]]
*Table 1: Results of unsupervised semantic segmentation under traditional evaluation strategy. Evaluated on full COCO-Stuff-27 (Caesar et al., 2018). ACSeg is taken from the original paper. IIC, PiCIE, and TransFGU from Yin et al. (2022). DINO from Koenig et al. (2023). Other results from Seitzer et al. (2022). Some works are evaluated on curated datasets (Ji et al., 2019), which generally gives higher mIoU than being evaluated on the full datasets (Yin et al., 2022)*

![[assets/figures/papers/paper_list_l23_https_arxiv_org_abs_2401_11739/figures/022_Figure_14.jpg]]
*Figure 14: Effects of modulating different cross-attention layers vs different computation $\left$( f $\left( \sigma \cdot$ V $\right$) + c M , f $\left( \sigma \cdot$ V + c M $\right) \right$) vs different λ. For cross-attention layers, we experiment with the three different layers in 16 × 16 upward modular blocks. Note that we abbreviate $\sigma \left( { \textstyle { \frac { Q K ^ { T } } { \sqrt { d } } } } \right$) to σ for convenience



## 定位与知识库关联

### 问题定位与核心瓶颈

无监督语义分割长期以来面临一个根本性矛盾：**语义理解发生在低分辨率特征空间，但分割输出需要像素级精度**。传统方法通常依赖双线性插值将低分辨率特征图上采样到原图尺寸，导致分割边界模糊、细节丢失。EmerDiff 重新审视了这一瓶颈，指出预训练扩散模型中有意义的语义特征图天然存在于空间低维层（如 16×16 的跨注意力层），直接上采样无法恢复丢失的像素级语义对应关系。

这一洞察将问题从“如何学习更好的特征表示”转变为“如何从低维特征中还原高分辨率语义结构”——这正是 EmerDiff 与现有无监督分割方法的分水岭。

### 方法谱系中的位置

EmerDiff 处于**无监督语义分割**与**扩散模型表征利用**两条研究线的交汇点。其对比基线可大致分为三类：

**1. 传统无监督语义分割方法**
- **STEGO**（Hamilton et al., ICLR 2022）：通过对比学习蒸馏 DINO 特征，在 COCO-Stuff-27 上达到 26.8 mIoU，是传统评估协议下的强基线。
- **DINOSAUR**（Seitzer et al., 2022）：基于 DINO 特征的 object-centric 分割方法。
- **ACSeg**、**IIC**、**PiCIE**、**TransFGU** 等早期工作：依赖自监督或聚类策略，性能普遍低于 20 mIoU。

EmerDiff 在传统评估协议下与 STEGO 持平（26.6 vs. 26.8 mIoU），但其优势在修改后的评估协议中才真正显现——传统匈牙利匹配会惩罚细粒度分割（例如将人体的头、臂、躯干分开标注会被视为错误），从而系统性低估 EmerDiff 的细粒度能力。

**2. 无标注开放词汇分割方法**
- **MaskCLIP**（Zhou et al., ECCV 2022）：利用 CLIP 的图像级对齐产生粗粒度像素嵌入。
- **TCL**（Cha et al., 2023）：通过文本-图像对齐实现开放词汇分割。
- **CLIPpy**（Ranasinghe et al., 2023）：基于 CLIP 的像素级嵌入方法。

这些方法的特点是**文本对齐但空间粗糙**——像素嵌入携带语义类别信息，但缺乏清晰的物体边界。EmerDiff 恰好提供了互补能力：**空间精细但类别无关**的分割掩码。将两者结合后，MaskCLIP 在 ADE20K 上从 10.3 提升至 15.9 mIoU，TCL 从 13.8 提升至 17.4 mIoU，验证了这种互补性。

**3. 朴素上采样基线（SD）**
使用与 EmerDiff 相同的 SD 特征图，但通过双线性插值上采样低分辨率掩码。在 ADE20K 上仅 29.1 mIoU，EmerDiff 以 33.1 mIoU 领先 4.0 个点，直接证明了语义对应上采样策略的有效性。

### 核心机制差异：从“插值”到“语义对应发现”

EmerDiff 的方法论创新在于**改变了低分辨率到高分辨率的映射策略**（changed_slots 中的唯一关键变更）：

| 维度 | 朴素上采样（SD 基线） | EmerDiff |
|------|----------------------|----------|
| 映射机制 | 双线性插值（几何平滑） | 调制去噪发现语义对应 |
| 信息源 | 仅低分辨率掩码的空间位置 | 扩散模型的生成机制（跨注意力层扰动） |
| 输出特性 | 边界模糊、细节丢失 | 边界清晰、保留物体结构 |

这一变更的因果机制是：在跨注意力层中对低维特征图的子区域施加偏移量 $cM$，观察生成图像中哪些像素发生显著变化。论文的核心发现是“扰动低分辨率掩码区域后，只有语义相关的像素在差异图中响应明显”（置信度 0.95），从而建立了**低分辨率掩码区域与高分辨率图像像素之间的语义对应关系**。差异图 $d = ||I^- - I^+||_2$ 本质上是一张“语义归属热力图”，每个像素被分配给对应强度最大的低分辨率掩码。

### 适用边界与局限

**已验证的有效范围：**
- 基于 Stable Diffusion 的预训练扩散模型（底层思想可能适用于其他生成模型，但未经验证）
- 特征图提取时间步 $t_f=1$（最小噪声），噪声增大会导致分割性能显著下降（Table 6）
- 调制时间步在 281–481 的中段表现最佳（Table 7）
- 调制强度 $\lambda=10$ 达到峰值，过大反而略有下降（Table 8）
- 掩码数量在 10–40 之间表现稳定（Table 4）

**已知失败模式（Figure 8）：**
1. **极小物体识别困难**：动物腿、人脸部件等细节在低维层中被压缩，难以建立可靠的语义对应。
2. **过分割倾向**：特征表示中包含空间位置和颜色属性，导致天空、地面等连续区域被过度分割。
3. **噪声残留**：生成的掩码可能仍含噪声，用于弱监督下游任务时需要进一步处理。

### 开放问题与后续方向

1. **跨模型泛化**：调制语义特征图的核心思想能否迁移到 GAN、自回归模型等其他生成范式？当前仅验证了 Stable Diffusion 这一条路径。

2. **过分割缓解**：如何解耦特征表示中的语义信息与空间/颜色等低级属性？这是提升分割语义一致性的关键。

3. **弱监督下游应用**：生成的掩码能否直接作为伪掩码用于弱监督语义分割，从而减少人工标注需求？论文在结论中将其列为未来方向，但尚未提供实验验证。

4. **小物体分割增强**：在高分辨率特征图稀缺的约束下，是否可以通过多尺度调制或分层对应发现策略提升对小物体的分割能力？



## 原文 PDF

![[paperPDFs/ICLR_2024/EmerDiff_Emerging_Pixel_level_Semantic_Knowledge_in_Diffusion_Models.pdf]]
