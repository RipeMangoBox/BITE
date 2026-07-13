---
title: "Semantic Segmentation with Generative Models: Semi-Supervised Learning and Strong Out-of-Domain Generalization"
type: paper
paper_level: A
venue: CVPR
year: 2021
pdf_ref: paperPDFs/CVPR_2021/Semantic_Segmentation_with_Generative_Models_Semi_Supervised_Learning_and_Strong_Out_of_Domain_Generalization.pdf
code_link: null
project_link: https://research.nvidia.com/labs/toronto-ai/semanticGAN/
aliases:
- SP
- SSGMSSLSODG
tags:
- CVPR_2021
- topic/generative_models_diffusion
- topic/generative_models_diffusion/generative_models_and_autoencoders
core_operator: "利用生成对抗网络直接建模图像与标签的联合分布 p(x,y)，通过测试时潜在空间反演推断标签，将语义分割重构为生成式条件采样问题。"
primary_logic: "生成模型学习生成逼真图像时，其内部特征表示已编码语义信息；添加轻量标签分支即可实现半监督分割，且因生成器在连续潜在空间平滑训练，天然具备强域外泛化能力。"
claims:
- "在胸部X光域外数据集（NLM, NIH, SZ）上，仅用9个标注样本训练的模型大幅超越所有基线的域内性能，例如在NLM上达到0.9464 DICE，而U-Net仅为0.8605。"
- "在面部部件分割的域外评估（MetFaces）中，使用1.5k标签训练的模型（mIoU 0.6633）超越了使用全部28k标签训练的DeepLab（mIoU 0.6415）。"
- "对人脸模型，可对卡通、雕塑甚至动物面部等极端域外图像生成合理的分割掩码，表明生成式先验的强大泛化性。"
- "JSRT (Chest X-ray, in-domain) 上 DICE = 0.9591"
---

# Semantic Segmentation with Generative Models: Semi-Supervised Learning and Strong Out-of-Domain Generalization

> [!tip] 核心洞察
> 生成模型学习生成逼真图像时，其内部特征表示已编码语义信息；添加轻量标签分支即可实现半监督分割，且因生成器在连续潜在空间平滑训练，天然具备强域外泛化能力。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 使用生成模型进行语义分割：半监督学习与强域外泛化 |
| 英文题名 | Semantic Segmentation with Generative Models: Semi-Supervised Learning and Strong Out-of-Domain Generalization |
| 会议/期刊 | CVPR 2021 |
| Links | [paper](https://arxiv.org/abs/2104.05833) · [Project](https://nv-tlabs.github.io/semanticGAN/) · [Project](https://research.nvidia.com/labs/toronto-ai/semanticGAN/) |
| Topic | #topic/generative_models_diffusion #topic/generative_models_diffusion/generative_models_and_autoencoders |
| Method | SemanticGAN (proposed) |
| Dataset | JSRT (Chest X-ray, in-domain), NLM (Chest X-ray, out-of-domain), MetFaces (Face Part Segmentation, ISIC (Skin Lesion |

> [!tip] 效果简介
> - JSRT (Chest X-ray, in-domain) 上，DICE 为 0.9591，对比 0.9318 (U-Net)，变化 +0.0273。
> - NLM (Chest X-ray, out-of-domain) 上，DICE 为 0.9464，对比 0.8605 (U-Net)，变化 +0.0859。
> - MetFaces (Face Part Segmentation, out-of-domain) 上，mIoU 为 0.6633 (1500 labels)，对比 0.6415 (DeepLab with 28k labels)，变化 +0.0218。

## 概要

语义分割是计算机视觉的核心任务，但主流判别式模型（如 **U-Net** (Ronneberger et al., MICCAI 2015)、**DeepLabV2** (Chen et al., CVPR 2016)）依赖大量逐像素标注数据，标注成本高昂，且在域外数据上泛化能力显著下降——这一瓶颈在医学影像等专业领域尤为突出。

本文提出 **SemanticGAN**，将语义分割重构为生成式条件采样问题。其核心思路是：利用生成对抗网络直接建模图像与标签的联合分布 $p(x, y)$，而非传统的条件分布 $p(y|x)$。生成器在学习生成逼真图像的过程中，其内部特征表示已天然编码语义信息；只需添加轻量标签分支，即可实现半监督分割。由于生成器在连续潜在空间中平滑训练，模型展现出**强域外泛化**能力——即使面对与训练数据视觉差异极大的图像（如从真实人脸泛化到卡通、雕塑甚至动物面部），仍能输出合理的分割掩码。

**关键实证发现：**
- 在胸部X光肺部分割中，仅使用**9个标注样本**训练的 SemanticGAN，在域外数据集 NLM 上达到 0.9464 DICE，大幅超越全监督 U-Net 的 0.8605（Table 1）。
- 在人脸部件分割中，使用**1.5k标注样本**的 SemanticGAN 在域外 MetFaces 数据集上 mIoU 达 0.6633，优于使用全部 28k 标注训练的 DeepLab（mIoU 0.6415）（Table 4）。
- 消融实验表明，增加无标注数据比增加标注数据更有效：30 标注 + 28k 未标注 ≈ 150 标注 + 3k 未标注（Table 5）。

**方法定位：** SemanticGAN 属于生成式分割范式，基于 StyleGAN2 架构，训练过程完全依赖对抗损失（双判别器 $D_r$ 保证图像真实性，$D_m$ 强制图文对齐），无需逐像素交叉熵损失。推理时通过测试时潜在空间反演推断标签，而非单步前向传播。该方法当前适用于人脸、医学影像等单模态数据，尚未扩展到复杂街景等场景，且测试时优化导致推理速度较慢。

语义分割是计算机视觉的核心任务，旨在为图像中的每个像素赋予类别标签。传统方法依赖判别式模型直接学习从图像到标签的映射 $p(y|x)$，这需要大量逐像素标注的数据。然而，获取高质量像素级标注极其昂贵，尤其在医学影像等专业领域，标注成本更为高昂。这一瓶颈严重制约了语义分割技术在标注稀缺场景下的应用。

现有半监督学习方法试图通过利用大量无标注数据来缓解标注压力，但其核心范式仍然是判别式的。典型方法如 **Mean Teacher**（Tarvainen & Valpola, NeurIPS 2017）通过一致性正则化约束模型对扰动输入输出一致预测，**AdvSSL**（Hung et al., 2018）引入对抗训练以利用无标注数据，**Guided Collaborative Training (GCT)**（Ke et al., 2020）则通过协同训练策略提升半监督性能。这些方法虽然在域内数据上取得了一定进展，但在域外数据上的泛化能力仍然有限——当测试数据分布与训练数据分布存在差异时，判别式模型的性能往往急剧下降。

另一个关键挑战是强域外泛化。在真实场景中，部署环境与训练环境可能截然不同：例如，在某个医院训练的X光分割模型需要泛化到其他医院的设备，或在真实人脸数据上训练的模型需要处理卡通、雕塑甚至动物面部图像。判别式模型由于仅学习条件分布 $p(y|x)$，缺乏对数据生成过程的完整建模，在面对分布偏移时容易过拟合到训练域的表观特征，导致泛化失败。

本文的核心动机在于：**将语义分割从判别式范式重构为生成式范式**。作者提出，通过生成对抗网络直接建模图像与标签的联合分布 $p(x,y)$，可以同时解决标注稀缺和域外泛化两大难题。其关键洞察是：当生成模型学会生成逼真图像时，其内部特征表示已经自然地编码了丰富的语义信息；只需在生成器中添加轻量级的标签输出分支，即可实现半监督语义分割。更重要的是，由于生成器在连续潜在空间中平滑训练，模型天然具备对未见域数据的强泛化能力——即使面对与训练数据视觉差异极大的输入，生成式先验仍能引导模型输出合理的分割结果。

这种范式转换带来了根本性的方法差异：训练时不再依赖逐像素标注损失，而是通过对抗训练迫使生成器同时生成逼真图像和准确标签；推理时也不采用单步前向传播，而是通过测试时潜在空间反演，将输入图像投影到生成器的潜在流形上，再从中解码出对应的分割掩码。这一设计使得模型能够以极少量标注样本（如仅9个胸部X光标注）实现超越全监督基线的性能，并在极端域外数据上展现出令人瞩目的泛化能力。

## 核心方法与创新机理

### 1. 范式转换：从判别式到生成式联合建模

传统语义分割方法（如 **U-Net** (Ronneberger et al., MICCAI 2015)、**DeepLabV2** (Chen et al., CVPR 2016)）采用判别式范式，直接建模条件分布 $p(y|x)$，输入图像后单步前向传播输出分割掩码。该范式的瓶颈在于：需要大量逐像素标注数据来学习从图像到标签的映射，且学到的决策边界在域外数据上泛化能力差——模型只见过训练分布中的图像-标签对应关系，缺乏对“什么是合理图像”这一更本质先验的建模。

本文的核心创新在于**将语义分割重构为生成式条件采样问题**：直接建模图像与标签的联合分布 $p(x,y)$，而非条件分布 $p(y|x)$。具体而言，生成器 $G(z): \mathcal{Z} \to (\mathcal{X}, \mathcal{Y})$ 将潜在向量 $z$ 同时映射为图像 $x$ 和语义标签 $y$，在给定 $z$ 的条件下，图像与标签条件独立。这一设计使得生成器在学习生成逼真图像的过程中，其内部特征表示已自然编码了语义结构信息——无需显式的逐像素标注损失即可实现分割。

**范式转换的关键影响**：
- 测试时通过潜在空间反演推断标签，而非直接前向传播，使模型天然具备域外泛化能力
- 生成器在连续潜在空间中的平滑训练，为分割提供了强大的生成式先验

### 2. 训练机制创新：纯对抗损失替代逐像素标注损失

传统监督分割方法依赖交叉熵或 Dice 损失，半监督方法（如 **Mean Teacher** (Tarvainen & Valpola, NeurIPS 2017)、**AdvSSL** (Hung et al., 2018)、**GCT** (Ke et al., 2020)）则引入一致性正则化或对抗损失作为辅助。本文的方法在训练损失函数上做出了根本性改变：**完全采用对抗损失，不使用任何逐像素标注损失**。

系统采用双判别器架构：
- **图像判别器 $D_r$**：判别生成图像与真实图像的真实性，损失函数为：
  $$\mathcal{L}_{D_r} = \mathbb{E}_{x_r \sim D_u}[\log D_r(x_r)] + \mathbb{E}_{(x_f,\cdot)=G(z), z \sim p(z)}[\log(1 - D_r(x_f))]$$
  
- **图像-标签对判别器 $D_m$**：判别生成图像-标签对与真实标注对的一致性，损失函数为：
  $$\mathcal{L}_{D_m} = \mathbb{E}_{(x_r,y_r) \sim D_l}[\log D_m(x_r, y_r)] + \mathbb{E}_{(x_f,y_f)=G(z), z \sim p(z)}[\log(1 - D_m(x_f, y_f))]$$

生成器损失联合优化图像真实性和图文对齐：
$$\mathcal{L}_G = \mathbb{E}_{(x_f,\cdot)=G(z)}[\log(1 - D_r(x_f))] + \mathbb{E}_{(x_f,y_f)=G(z)}[\log(1 - D_m(x_f, y_f))]$$

**关键设计**：梯度从 $D_m$ 不回传到生成器的图像合成分支，仅通过标签分支传递，确保图像生成质量不受标签判别器干扰。

### 3. 推理流程创新：测试时反演替代单步前向传播

传统分割方法的推理是单步前向传播，速度极快但不具备对域外数据的适应能力。本文的推理流程分为两阶段：

**阶段一：编码器初始化**。训练一个编码器 $E: \mathcal{X} \to \mathcal{W}^+$，将输入图像映射到 StyleGAN2 的 $\mathcal{W}^+$ 潜在空间。编码器训练结合监督损失（交叉熵 + Dice）和无监督图像重建损失（LPIPS + L2）：
$$\min_E [\mathcal{L}_{\text{LPIPS}}(x, G_x(E(x))) + \lambda_1 \|x - G_x(E(x))\|_2^2]$$

**阶段二：测试时迭代反演**。对测试图像 $x^*$，以编码器输出为初始点，优化潜在向量以最小化重建误差：
$$w^{+*} = \arg\min_{w^+ \in \mathcal{W}^+} [\mathcal{L}_{\text{reconst}}(x^*, G_x(w^+)) + \lambda_2 \|w^+ - E(G(w^+))\|_2^2]$$

其中重建损失结合感知损失和 L2 损失：
$$\mathcal{L}_{\text{reconst}}(x, x^*) = \mathcal{L}_{\text{LPIPS}}(x, x^*) + \lambda_3 \|x - x^*\|_2^2$$

正则化项 $\lambda_2 \|w^+ - E(G(w^+))\|_2^2$ 约束优化后的潜在向量不偏离编码器学到的流形，防止反演到不合理区域。

**推理机制的核心优势**：测试时优化使模型能主动“寻找”最能解释测试图像的潜在表示，而非被动接受训练时学到的固定映射。这解释了为何模型在极端域外数据（如卡通、动物面部）上仍能生成合理分割——生成器在训练时学到的平滑潜在空间，使得即使测试图像远离训练分布，反演过程仍能找到语义上合理的近似表示。

### 4. 架构创新：基于 StyleGAN2 的双输出生成器

生成器架构基于 StyleGAN2 修改，核心改动是在每个风格层添加标签输出分支（Figure 3）。tImage 和 tSeg 模块分别在不同分辨率输出中间图像和分割掩码，两者共享相同的风格层。这种设计确保了图像与标签在多层次上的语义一致性——从粗糙结构到精细细节，标签与图像始终由相同的潜在编码控制。

### 创新总结

| 维度 | 传统方法 | 本文方法 (SemanticGAN) |
|------|---------|----------------------|
| **模型范式** | 判别式 $p(y\|x)$ | 生成式 $p(x,y)$ |
| **训练损失** | 交叉熵/Dice + 一致性/对抗辅助 | 纯对抗损失（双判别器） |
| **推理流程** | 单步前向传播 | 编码器初始化 + 迭代反演优化 |
| **标注需求** | 大量标注数据 | 少量标注 + 大量无标注数据 |
| **域外泛化** | 依赖数据增强，效果有限 | 生成式先验天然支持强域外泛化 |

SemanticGAN 将语义分割重构为**生成式条件采样问题**，核心思想是直接建模图像与标签的联合分布 $p(x,y)$，而非传统判别式模型所学习的条件分布 $p(y|x)$。其整体 pipeline 由四个核心模块构成，形成训练与推理两条协同的数据流。

### 训练流程

训练阶段涉及三个模块的联合优化：生成器 $G$、图像判别器 $D_r$ 和图像-标签对判别器 $D_m$，以及一个辅助编码器 $E$（见 Figure 2）。

![[assets/figures/papers/paper_list_l32_https_arxiv_org_abs_2104_05833/figures/003_Figure_2.jpg]]
*Figure 2: Model Overview. Generator G and discriminators $D _ { m }$ and $D _ { r }$ are trained with adversarial objectives $\mathcal { L } _ { G }$ (not indicated here), $\mathcal { L } _ { D _ { m } }$ and $\mathcal { L } _ { D _ { r } }$ . We do not backpropagate gradients from $D _ { m }$ into the generator’s image synthesis branch. We train an additional encoder E in a supervised fashion using image and mask reconstruction losses $\mathcal { L } _ { u }$ and $\mathcal { L } _ { s }$ Figure 3: Generator Architecture. We modify StyleGAN2’s image synthesis network to also output masks. The tImage and tSeg blocks output intermediate images and segmentation masks at different resolutions, respectively. Both share t...

**生成器 $G$** 基于 StyleGAN2 架构修改而来，将噪声向量 $z \sim p(z)$ 映射到中间潜在空间 $\mathcal{W}$，再同时输出图像 $x_f$ 和逐像素语义分割掩码 $y_f$（见 Figure 3）。具体而言，在 StyleGAN2 的每个风格层上添加一个额外的分割分支（tSeg 块），与图像合成分支（tImage 块）共享相同的风格调制参数，从而保证图像与标签在潜在空间中的条件独立性——给定 $z$，$x$ 与 $y$ 条件独立。

**双判别器设计** 是该框架的关键创新。$D_r$ 为标准图像判别器，仅判别生成图像 $x_f$ 与真实无标注图像 $x_r \sim D_u$ 的真实性，其损失函数为：

$$\mathcal{L}_{D_r} = \mathbb{E}_{x_r \sim D_u}[\log D_r(x_r)] + \mathbb{E}_{(x_f,\cdot)=G(z), z \sim p(z)}[\log(1 - D_r(x_f))]$$

$D_m$ 则判别**图像-标签对**的一致性，输入为真实标注对 $(x_r, y_r) \sim D_l$ 或生成对 $(x_f, y_f)$，强制生成器输出语义正确的分割掩码：

$$\mathcal{L}_{D_m} = \mathbb{E}_{(x_r, y_r) \sim D_l}[\log D_m(x_r, y_r)] + \mathbb{E}_{(x_f, y_f)=G(z), z \sim p(z)}[\log(1 - D_m(x_f, y_f))]$$

生成器的对抗损失为两者之和：

$$\mathcal{L}_G = \mathbb{E}_{(x_f,\cdot)=G(z)}[\log(1 - D_r(x_f))] + \mathbb{E}_{(x_f, y_f)=G(z)}[\log(1 - D_m(x_f, y_f))]$$

值得注意的是，$D_m$ 的梯度**不会回传**到生成器的图像合成分支，仅用于监督标签分支，从而避免干扰图像生成质量。整个训练过程**不使用任何逐像素标注损失**（如交叉熵或 Dice 损失），完全依赖对抗训练，这使得模型能够从大量无标注数据中学习图像的流形结构，仅需少量标注样本即可引导标签语义的对齐。

**编码器 $E$** 用于学习从图像到 $\mathcal{W}^+$ 空间的映射，为后续推理提供良好的初始化点。其训练包含两个目标：对标注数据的监督损失 $\mathcal{L}_s$（交叉熵 + Dice），以及对所有数据（标注与无标注）的无监督重建损失 $\mathcal{L}_u$（LPIPS 感知损失 + L2 像素损失）：

$$\mathcal{L}_u = \mathbb{E}_{x \sim D_l \cup D_u}[\mathcal{L}_{\mathrm{LPIPS}}(x, G_x(E(x))) + \lambda_1 ||x - G_x(E(x))||_2^2]$$

### 推理流程

推理阶段不依赖编码器的直接前向传播，而是采用**测试时潜在空间反演**策略。给定目标图像 $x^*$，首先通过编码器 $E$ 获得初始潜在向量 $w^+_{\text{init}} = E(x^*)$，然后在 $\mathcal{W}^+$ 空间中迭代优化以下目标：

$$w^{+*} = \underset{w^+ \in \mathcal{W}^+}{\arg\min} \; [\mathcal{L}_{\mathrm{reconst}}(x^*, G_x(w^+)) + \lambda_2 ||w^+ - E(G(w^+))||_2^2]$$

其中重建损失 $\mathcal{L}_{\mathrm{reconst}}$ 同样由 LPIPS 和 L2 组成：

$$\mathcal{L}_{\mathrm{reconst}}(x, x^*) = \mathcal{L}_{\mathrm{LPIPS}}(x, x^*) + \lambda_3 ||x - x^*||_2^2$$

优化目标的第一项确保生成图像 $G_x(w^+)$ 与目标图像 $x^*$ 在感知和像素层面一致；第二项作为正则化，约束优化后的 $w^+$ 不远离编码器的映射域，防止反演落入生成器未充分训练的区域。一旦找到最优 $w^{+*}$，对应的分割掩码 $y^* = G_y(w^{+*})$ 即为最终预测结果。

### 模块间关系与数据流

整体 pipeline 的输入输出流可概括为：
- **训练时**：无标注图像 $D_u$ 驱动 $D_r$ 和生成器的图像真实性学习；少量标注对 $D_l$ 驱动 $D_m$ 和生成器的图文对齐学习；编码器 $E$ 从两者中学习图像到潜在空间的映射。
- **推理时**：输入单张图像 $x^*$ → 编码器初始化 $w^+_{\text{init}}$ → 迭代优化重建目标 → 生成器输出对应分割掩码。

这种设计将生成模型的平滑潜在空间先验引入分割任务——生成器在连续 $\mathcal{W}^+$ 空间中被训练以生成逼真图像，其内部特征表示已编码丰富的语义信息，因此即使面对域外图像，只要能在潜在空间中找到合理的重建点，就能推断出语义一致的分割结果。

### 3.1 生成器架构 (Generator G)

生成器基于 **StyleGAN2** 构建，核心修改是在每个风格层添加一个额外的分割分支，使其能够同时输出图像 $x$ 和逐像素语义标签 $y$。如 Figure 3 所示，生成器将噪声向量 $z$ 映射到中间潜在空间 $\mathcal{W}$，再映射到输出空间：

$$G : \mathcal{Z} \to \mathcal{W} \to (\mathcal{X}, \mathcal{Y})$$

其中 tImage 和 tSeg 模块分别在不同分辨率下输出中间图像和分割掩码，两者共享相同的风格层。这种设计使得潜在向量 $z$ 同时解释图像和标签，给定 $z$ 时图像与标签条件独立。

### 3.2 双判别器设计

模型采用两个判别器，均使用对抗训练，不使用任何逐像素标注损失（如交叉熵）：

- **图像判别器 $D_r$**：判别生成图像与真实图像的真实性，输入为无标注图像集 $D_u$。
- **图文对齐判别器 $D_m$**：判别生成与真实的图像-标签对的一致性，输入为有标注图像集 $D_l$。

关键设计选择：$D_m$ 的梯度不会反向传播到生成器的图像合成分支，仅影响标签分支，确保图像生成质量不受标签判别器的干扰（见 Figure 2）。

### 3.3 核心损失函数

**图像判别器损失 $D_r$**（标准 GAN 判别器损失）：

$$\mathcal { L } _ { D _ { r } } = \underset { x _ { r } \sim D _ { u } } { \mathbb { E } } \left[ \log D _ { r } ( x _ { r } ) \right] + \underset { ( x _ { f } , \cdot ) = G ( z ) , z \sim p ( z ) } { \mathbb { E } } \left[ \log ( 1 - D _ { r } ( x _ { f } ) ) \right]$$

其中 $x_r$ 为真实图像，$x_f$ 为生成图像，$p(z)$ 为标准正态先验。

**图文对齐判别器损失 $D_m$**：

$$\mathcal { L } _ { D _ { m } } = \underset { ( x _ { r } , y _ { r } ) \sim D _ { l } } { \mathbb { E } } [ \log D _ { m } ( x _ { r } , y _ { r } ) ] + \underset { ( x _ { f } , y _ { f } ) = G ( z ) , z \sim p ( z ) } { \mathbb { E } } [ \log ( 1 - D _ { m } ( x _ { f } , y _ { f } ) ) ]$$

其中 $(x_r, y_r)$ 为真实图像-标签对，$(x_f, y_f)$ 为生成对。该损失强制生成器产生语义一致的图文对。

**生成器对抗损失 $G$**（联合优化图像与标签）：

$$\mathcal { L } _ { G } = \underset { ( x _ { f } , \cdot ) = G ( z ) , z \sim p ( z ) } { \mathbb { E } } [ \log ( 1 - D _ { r } ( x _ { f } ) ) ] + \underset { ( x _ { f } , y _ { f } ) = G ( z ) , z \sim p ( z ) } { \mathbb { E } } [ \log ( 1 - D _ { m } ( x _ { f } , y _ { f } ) ) ]$$

### 3.4 编码器 E 与潜在空间反演

为实现测试时分割，模型引入编码器 $E : \mathcal{X} \to \mathcal{W}^+$，将输入图像直接映射到 $\mathcal{W}^+$ 空间作为反演初始点。编码器采用特征金字塔网络（FPN）作为骨干提取多层级特征，再通过小型全卷积网络映射到 $\mathcal{W}^+$ 空间。

**编码器监督损失**（利用有标注数据）：

$$\mathcal { L } _ { s } = \underset { ( x , y ) \sim D _ { l } } { \mathbb { E } } \mathbf { H } ( y , G _ { y } ( E ( x ) ) ) + \mathbf { D C } ( y , G _ { y } ( E ( x ) ) )$$

其中 $\mathbf{H}$ 为交叉熵，$\mathbf{DC}$ 为 Dice 损失，$G_y$ 表示生成器的标签输出分支。

**编码器无监督重建损失**（利用所有数据）：

$$\mathcal { L } _ { u } = \underset { x \sim D _ { l } \cup D _ { u } } { \mathbb { E } } \mathcal { L } _ { \mathrm { L P I P S } } ( x , G _ { x } ( E ( x ) ) ) + \lambda _ { 1 } | | x - G _ { x } ( E ( x ) ) | | _ { 2 } ^ { 2 }$$

该损失结合感知损失（LPIPS）和像素级 L2 损失，使编码器学习将图像映射到能够重建原图的潜在向量，$G_x$ 表示生成器的图像输出分支。

### 3.5 测试时反演推理

给定测试图像 $x^*$，分割通过优化以下目标获得最优潜在向量 $w^{+*}$：

$$w ^ { + * } = \underset { w ^ { + } \in \mathcal { W } ^ { + } } { \arg \operatorname* { m i n } } [ \mathcal { L } _ { \mathrm { r e c o n s t } } ( x ^ { * } , G _ { x } ( w ^ { + } ) ) + \lambda _ { 2 } | | w ^ { + } - E ( G ( w ^ { + } ) ) | | _ { 2 } ^ { 2 } ]$$

其中重建损失定义为：

$$\mathcal { L } _ { \mathrm { r e c o n s t } } ( x , x ^ { * } ) = \mathcal { L } _ { \mathrm { L P I P S } } ( x , x ^ { * } ) + \lambda _ { 3 } | | x - x ^ { * } | | _ { 2 } ^ { 2 }$$

优化目标包含两项：第一项确保生成图像 $G_x(w^+)$ 与测试图像 $x^*$ 在感知和像素层面一致；第二项正则化项约束 $w^+$ 保持在编码器域内（即 $w^+$ 应接近 $E(G(w^+))$），防止反演到生成器未充分训练的区域。获得 $w^{+*}$ 后，分割结果由 $G_y(w^{+*})$ 直接给出。

**关键机制**：整个推理过程无需前向传播的判别模型，而是通过生成模型的潜在空间反演，利用生成器学习到的联合分布 $p(x,y)$ 推断标签。这一设计使得模型在域外数据上表现出强泛化能力，因为生成器在连续潜在空间中的平滑训练天然提供了正则化先验。

## 实验与关键发现

### 核心实验结果

SemanticGAN 在多个医学影像与人脸分割基准上，以极少标注样本实现了对全监督基线的超越，并在域外泛化任务上展现出显著优势。

**胸部X光肺部分割。** 在域内数据集 JSRT 上，本方法以 9 个标注样本搭配 108k 无标注数据，取得 **0.9591 DICE**，超越全监督 U-Net（**0.9318**，Ronneberger et al., MICCAI 2015）约 2.7 个百分点（Table 1）。域外泛化优势更为突出：在 NLM 数据集上，本方法 DICE 达 **0.9464**，而 U-Net 仅 **0.8605**，相对提升约 8.6 个百分点；在 NIH 和 SZ 数据集上同样大幅领先所有半监督基线（Mean Teacher、AdvSSL、GCT）。这表明生成式先验对跨医院、跨设备的胸部X光影像具有强鲁棒性。

**皮肤病灶分割。** 在 ISIC 数据集上，仅使用 40 个标注样本，本方法取得 **0.7144 JC index**，显著优于最佳半监督基线（约 0.6410），相对提升超过 7 个百分点（Table 2）。生成模型在医学影像小样本场景下的分割质量优势得到跨任务验证。

**人脸部件分割与极端域外泛化。** 在 CelebA 域内测试中，使用 1.5k 标注样本的 SemanticGAN 取得 **0.7780 mIoU**，接近全监督 DeepLabV2（Chen et al., CVPR 2016）使用 28k 标注的性能（0.7885）。关键突破在域外评估：在 MetFaces 数据集上，本方法以 1.5k 标注样本取得 **0.6633 mIoU**，**超越使用全部 28k 标注训练的 DeepLab（0.6415 mIoU）**（Table 4）。Figure 8 进一步展示，模型对卡通、雕塑甚至动物面部等与训练分布存在极大视觉差异的图像，仍能生成合理的语义分割掩码，验证了生成式先验在连续潜在空间中平滑训练所带来的强泛化能力。

**跨模态医学影像分割。** 在 CT 到 MRI 的肝脏分割迁移任务中，本方法同样展现出域外泛化优势，体现了生成模型对医学影像模态差异的适应性（Figure 1 定性展示）。

### 消融实验

**标注样本 vs. 无标注样本的效率。** Table 5 揭示了关键效率瓶颈：**增加无标注数据比增加标注数据更有效**。具体而言，30 个标注样本搭配 28k 无标注数据所达到的性能，与 150 个标注样本搭配 3k 无标注数据的性能大致相当。这表明生成模型能够从大量无标注图像中提取有效的语义先验，从而大幅降低对逐像素标注的依赖。

**生成式分割 vs. 合成数据训练独立模型。** Table 6 对比了三种策略：（1）直接用生成器进行分割（本方法）；（2）用生成器合成 20k 标注图像训练 DeepLab（Ours-sim）；（3）合成数据与 150 真实标注混合训练 DeepLab（Ours-mix）。结果显示，**直接使用生成器进行分割始终优于用合成数据训练独立分割模型**。此外，采用截断技巧（truncation trick, ψ=0.7）生成的合成数据视觉质量更高但多样性降低，对下游分割模型的训练效果反而不如不截断的多样化合成数据（div vs. tru），说明在分割任务中**合成数据的多样性比视觉保真度更为关键**。

### 关键图表结论

- **Figure 1**：定性展示跨域泛化能力——从真实人脸到油画、雕塑、动物面部，从胸部X光到穿衣人体，从CT到MRI，模型均能输出合理分割结果。
- **Figure 4**：生成器在各数据集上合成的图像-标签对样本，展示联合分布建模的质量。
- **Figure 5**：胸部X光分割的域内与域外定性对比，本方法在域外数据上的分割边界更接近真实标注。
- **Table 1 & Table 4**：定量证实生成式分割在**域外泛化上的系统性优势**，这是判别式方法难以通过增加标注数据弥补的。

![[assets/figures/papers/paper_list_l32_https_arxiv_org_abs_2104_05833/figures/007_Figure_5.jpg]]
*Figure 5: Chest X-ray Segmentation. Qualitative examples for both in-domain and out-of-domain datasets. Table 4: Face Part Segmentation. Numbers are mIoU. We train on CelebA and evaluate on CelebA as well as the MetFaces dataset. “# Train labels” denotes the number of annotated examples used during training. Our model as well as the semi-supervised baselines additionally use 28k unlabeled CelebA data samples*

### 失败模式与局限

尽管域外泛化能力突出，本方法存在以下局限：

1. **推理效率低。** 测试时需通过迭代优化（Eq. 7）反演潜在向量，每张图像需数百次前向传播，远慢于单步前向的判别式模型，不适用于实时场景。
2. **复杂场景建模能力受限。** 当前 StyleGAN2 生成器难以处理户外街景等高度复杂、多类别、大尺度变化的场景，方法适用范围局限于人脸、医学影像等相对结构化的单模态数据。
3. **精细结构分割精度不足。** 生成模型的平滑先验可能导致小目标或边界细节的分割精度下降，这在医学影像中可能影响临床可用性。
4. **无标注数据需求仍高。** 虽然大幅降低标注需求，但训练生成器仍需大量无标注数据（如胸部X光实验使用 108k 无标注图像），在数据稀缺领域可能受限。

### 开放问题

- 能否将本框架扩展到复杂场景（如自动驾驶街景）的语义分割？
- 如何通过蒸馏或一次性编码器加速测试时反演，实现实时分割？
- 生成式平滑先验对精细结构分割精度的影响如何量化与缓解？
- 最优标注/未标注数据比例的理论或经验规律是什么？

![[assets/figures/papers/paper_list_l32_https_arxiv_org_abs_2104_05833/figures/005_Table.jpg]]

![[assets/figures/papers/paper_list_l32_https_arxiv_org_abs_2104_05833/figures/010_Table_5.jpg]]
*Table 5: Ablation Study on Number of Labeled vs Unlabeled Examples. Numbers are mIoU. Entries marked with red or blue color roughly correspond to each other, i.e. 30 labeled and 28k unlabeled results in similar performance as 150 labeled and 3k unlabeled examples*

![[assets/figures/papers/paper_list_l32_https_arxiv_org_abs_2104_05833/figures/006_Figure_6.jpg]]
*Figure 6: Face Parts Segmentation. Qualitative examples for both indomain and out-of-domain datasets*

![[assets/figures/papers/paper_list_l32_https_arxiv_org_abs_2104_05833/figures/011_Table_6.jpg]]
*Table 6: Synthesize Annotated Images to Train a Task Model vs Our Method. Numbers are mIoU. DeepLab-real denotes supervised training of a DeepLab model using 150 labeled real examples. Ours-sim denotes training DeepLab using only the 20k synthetic dataset. Ours-mix means training DeepLab using both the synthetic and 150 labeled real examples. div denotes sampling without applying the truncation trick [44], which results in more diverse but less visually appealing images; tru means applying the truncation trick with factor of 0.7. Ours denotes performing segmentation directly with our generative segmentation method*

## 定位与知识库关联

### 判别式分割 → 生成式分割的范式转换

传统语义分割方法（如 **U-Net** (Ronneberger et al., MICCAI 2015)、**DeepLabV2** (Chen et al., CVPR 2016)）均采用判别式范式，直接建模条件分布 $p(y|x)$，通过单步前向传播输出分割掩码。半监督方法如 **Mean Teacher** (Tarvainen & Valpola, NeurIPS 2017)、**AdvSSL** (Hung et al., 2018) 和 **Guided Collaborative Training (GCT)** (Ke et al., 2020) 在此基础上引入一致性正则化或对抗训练，但始终未脱离判别式框架。这些方法的共同瓶颈在于：判别边界由标注样本划定，当测试数据分布偏移时，缺乏对图像本身结构的先验理解，泛化能力严重受限。

本文提出的 **SemanticGAN** 实现了根本性的范式转换：将语义分割重构为生成式条件采样问题，直接建模图像与标签的联合分布 $p(x,y)$。核心因果机制在于：生成器在连续潜在空间中以对抗方式学习生成逼真图像时，其内部表示已自然编码了语义结构的平滑先验——这使得仅需少量标注样本即可通过轻量标签分支实现半监督分割，且天然具备强域外泛化能力。

### 关键模块差异对比

| 维度 | 判别式基线 | SemanticGAN |
|------|-----------|-------------|
| **模型范式** | 判别式 $p(y|x)$，输入图像直接输出掩码 | 生成式 $p(x,y)$，基于 StyleGAN2 联合生成图像与标签，测试时通过反演推断标签 |
| **训练损失** | 交叉熵/Dice 损失（监督），或一致性/对抗损失（半监督） | 完全对抗损失，无逐像素标注损失；双判别器 $D_r$（图像真实性）和 $D_m$（图文对齐）联合训练 |
| **推理流程** | 单步前向传播 | 编码器 $E$ 初始化潜在向量 + 迭代优化 Eq. (7) 进行重建反演 |
| **数据需求** | 依赖大量标注数据 | 仅需少量标注 + 大量无标注数据训练生成器 |

### 在生成模型谱系中的定位

该方法建立在 **StyleGAN2** 的架构基础上，但进行了关键修改：在每个风格层添加分割掩码输出分支（tSeg 块），使生成器同时输出图像和逐像素标签。与现有生成式分割方法的本质区别在于：**SemanticGAN 是首个完全使用对抗目标（无交叉熵项）的生成式分割方法**，且生成器直接建模联合分布 $p(x,y)$ 而非仅生成图像用于数据增强。

测试时推理采用潜在空间反演策略：编码器 $E$ 将输入图像映射到 $\mathcal{W}^+$ 空间作为初始化，随后通过优化重建目标 Eq. (7) 迭代求解最优潜在向量 $w^{+*}$，再通过生成器的标签分支 $G_y(w^{+*})$ 获得分割结果。这一流程与 GAN Inversion 领域的工作一脉相承，但首次将其系统性地应用于语义分割任务。

### 适用边界与局限

**适用场景**：
- 单模态数据的分割任务，且测试数据分布与生成器训练分布足够接近（如人脸部件分割、胸部X光肺部分割、皮肤病变分割）
- 标注极度稀缺但无标注数据充足的场景（如医学影像领域）
- 对域外泛化有强需求的场景

**核心局限**：
1. **生成模型表达能力瓶颈**：当前框架不能处理高度复杂数据（如户外街景），受限于 GAN 对复杂场景的生成能力
2. **推理速度慢**：测试时优化（Eq. 7 的迭代求解）导致推理耗时，不适合实时应用
3. **无标注数据需求仍高**：虽然大幅减少标注需求，但训练生成器仍需大量无标注数据
4. **精细结构分割精度**：生成器的平滑先验可能导致对精细边界的刻画不足（文中未量化分析，需人工验证）

### 开放问题

1. **框架扩展性**：能否将生成式分割框架扩展到复杂场景（如自动驾驶街景）？这依赖于 GAN 生成能力的进一步提升或替代生成模型的引入
2. **推理加速**：如何通过知识蒸馏或一次性编码器直接预测标签，避免测试时迭代优化，实现实时分割？
3. **精细度权衡**：生成式先验的平滑性与精细结构分割精度之间的定量关系尚待研究
4. **最优数据配比**：标注/未标注数据的最优比例如何确定，以在标注成本与性能之间取得平衡？消融实验（Table 5）已初步表明增加无标注数据比增加标注数据更有效，但系统性的理论指导仍缺失

## 原文 PDF

![[paperPDFs/CVPR_2021/Semantic_Segmentation_with_Generative_Models_Semi_Supervised_Learning_and_Strong_Out_of_Domain_Generalization.pdf]]
