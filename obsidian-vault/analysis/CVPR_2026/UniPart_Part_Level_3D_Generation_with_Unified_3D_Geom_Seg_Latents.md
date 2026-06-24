---
title: "UniPart: Part-Level 3D Generation with Unified 3D Geom-Seg Latents"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/UniPart_Part_Level_3D_Generation_with_Unified_3D_Geom_Seg_Latents.pdf
project_link: null
code_link: null
aliases:
- UniPart
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
- topic/generative_models_diffusion
core_operator: 从整体几何学习的自注意力中发现隐式部件感知，构建几何-分割联合隐空间（Geom-Seg VecSet），并设计两阶段扩散流水线（整体生成+部件精修）与双空间生成机制。
primary_logic: 在纯整体几何生成过程中，扩散Transformers的隐变量已自发形成与语义部件高度相关的聚类，因此可将部件分割信息融入统一的几何隐空间，实现端到端的可控部件级生成。
claims:
- Hunyuan3D-2.1 DiT自注意力图显示隐变量在相同语义部件内强相关，证明部件感知隐含存在。
- UniPart在定量比较中显著优于现有方法，CD降至0.72，F1@0.1达92.21。
- Part-level generation test set (curated from multiple sources) 上 Chamfer Distance (CD↓, ×10²) = 0.72
- Part-level generation test set 上 F1@0.1 (↑, ×10²) = 92.21
---

# UniPart: Part-Level 3D Generation with Unified 3D Geom-Seg Latents

> [!tip] 核心洞察
> 在纯整体几何生成过程中，扩散Transformers的隐变量已自发形成与语义部件高度相关的聚类，因此可将部件分割信息融入统一的几何隐空间，实现端到端的可控部件级生成。

| 字段 | 内容 |
|------|------|
| 中文题名 | UniPart：基于统一三维几何-分割隐变量的部件级三维生成 |
| 英文题名 | UniPart: Part-Level 3D Generation with Unified 3D Geom-Seg Latents |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2512.09435) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction #topic/generative_models_diffusion |
| Method | UniPart |
| Dataset | Part-level generation test set |

> [!tip] 效果简介
> - Part-level generation test set (curated from multiple sources) 上，Chamfer Distance (CD↓, ×10²) 0.72。
> - Part-level generation test set 上，F1@0.1 (↑, ×10²) 92.21。

## 概述

**问题瓶颈**：现有部件级三维生成方法面临一个根本性矛盾——依赖隐式分割的方法在粒度控制上能力有限，而依赖外部预训练分割器的方法则引入额外标注成本，且两类方法在部件几何质量上均存在退化风险。其深层瓶颈在于，缺乏一个能够同时表征整体几何与部件语义的统一隐空间，导致生成与分割两阶段割裂。

**核心发现**：UniPart 的出发点来自一项关键观察——在纯整体几何生成过程中，扩散 Transformer（DiT）的隐变量已自发形成与语义部件高度相关的聚类（见 Figure 1）。这意味着部件感知信息隐含地存在于整体几何隐空间中，无需外部监督即可被挖掘。

**方法定位**：基于上述发现，UniPart 构建了一个统一的**几何-分割联合隐空间（Geom-Seg VecSet）**，并设计了一套**两阶段扩散流水线**：整体级 DiT 首先生成全局几何与部件隐变量分割，部件级 DiT 随后在**双空间（全局坐标空间 + 归一化规范空间）**下精修每个部件的几何隐变量，最终通过共享几何解码器输出可组合的部件网格。该方法在方法谱系中区别于三类基线：**PartCrafter**（Lin et al., 2025）、**OmniPart**（Yang et al., 2025）、**X-Part**（Yan et al., 2025）和 **HoloPart**（Yang et al., 2025），它们或采用生成后分割的范式，或依赖外部分割先验，而 UniPart 首次实现了端到端的统一隐空间部件级生成。

**主要结果**：在部件级生成测试集上，UniPart 在几何质量指标上显著超越现有方法，Chamfer Distance（CD）降至 **0.72**（×10²），F1@0.1 达到 **92.21**（×10²）（Table 1）。消融实验进一步验证了归一化规范空间（NCS）、局部注意力机制与空间嵌入注入三个设计对部件几何连贯性和组合精度的关键作用（Figure 7）。

## 背景与动机

### 部件级三维生成的需求与挑战

三维内容生成在影视、游戏、工业设计等领域需求迫切，而**部件级三维生成**——即输出由独立语义部件组成的可分解三维模型——是实现可编辑、可交互三维资产的关键环节。与整体式生成不同，部件级生成要求模型同时输出高质量的几何形状和准确的语义分割，且部件之间需保持无缝组合，这对表征能力和生成控制提出了更高要求。

当前部件级三维生成面临一个根本性瓶颈：**缺乏能同时表征几何与部件语义的统一隐空间**。现有方法通常采用两种策略，但各有局限：

- **隐式分割策略**：在整体几何生成后，依赖隐空间中的聚类或后处理进行部件划分。这类方法的分割粒度受限于隐变量的表达能力，难以实现精细可控的部件分解。
- **外部分割器策略**：借助预训练的部件分割模型对生成结果进行标注，如 **PartCrafter**（Lin et al., 2025）、**OmniPart**（Yang et al., 2025）、**X-Part**（Yan et al., 2025）和 **HoloPart**（Yang et al., 2025）等。这类方法不仅引入额外的标注成本和模型依赖，且部件几何质量在分割后容易退化。

上述方法的共同症结在于：**几何生成与部件语义理解被解耦为两个独立过程**，导致信息损失和累积误差。

### 核心洞察：隐式部件感知的发现

UniPart 的动机源于一个关键观察：在纯整体几何生成过程中，扩散 Transformer（DiT）的隐变量已自发形成与语义部件高度相关的聚类。如 **Figure 1** 所示，Hunyuan3D-2.1 DiT 的自注意力图揭示，属于同一语义部件（如椅背、椅座、椅腿）的隐变量之间存在强相关性，而跨部件的相关性则显著较弱。这表明，**即使模型从未被显式训练进行部件感知，其隐空间已隐含编码了部件结构信息**。

这一发现构成了本文的核心洞察：**可将部件分割信息融入统一的几何隐空间，实现端到端的可控部件级生成**，从而消除几何与语义之间的表征鸿沟。

### 本文动机与思路

基于上述洞察，UniPart 提出了一条不同于现有方法的路径：

1. **构建几何-分割联合隐空间**：设计 Geom-Seg VecSet，使每个隐向量同时承载几何贡献和部件标签，从根本上统一几何与语义表征。
2. **两阶段扩散流水线**：先通过整体级 DiT 生成全局几何与部件隐变量分割，再通过部件级 DiT 在双空间（全局坐标+归一化规范空间）中精修每个部件的几何，实现高质量部件生成与无缝组合。
3. **端到端可控生成**：整个过程无需外部分割器，部件分割与几何生成共享同一隐空间，从机制上避免了信息解耦带来的质量退化。

这种设计将部件感知从“后处理”提升为“原生能力”，为部件级三维生成提供了新的范式。

## 核心创新

UniPart 的核心创新在于发现并利用了扩散 Transformer 隐空间中天然存在的部件感知能力，构建了一个**统一的几何-分割隐空间（Geom-Seg VecSet）**，并围绕它设计了端到端的两阶段部件级三维生成流水线。与现有方法相比，其关键创新体现在以下三个维度的 changed slots 上。

### 1. 隐空间表征：从纯几何到几何-分割联合

现有部件级生成方法要么依赖外部预训练分割器引入额外标注成本，要么采用隐式分割导致粒度控制有限。UniPart 的根本突破在于将部件分割信息直接融入几何隐空间。

**动机发现**：研究者在 Hunyuan3D-2.1 的 DiT 推理过程中观察到，自注意力图显示隐变量在相同语义部件内呈现强相关性（见 Figure 1），这证明即使在纯整体几何生成训练中，隐空间已自发形成与语义部件高度对应的聚类结构。

基于此发现，UniPart 将传统 VecSet VAE 的纯几何隐空间扩展为 **Geom-Seg VecSet**。在 VAE 训练阶段，每个隐向量不仅解码为几何贡献，还同时解码为部件标签，损失函数从原始的

$$\mathcal{L}_{\mathrm{vecset}} = \mathcal{L}_{\mathrm{recon}} + \lambda_{\mathrm{kl}} \cdot \mathcal{L}_{\mathrm{kl}}$$

扩展为联合优化形式：

$$\mathcal{L}_{\mathrm{vecset}} = \mathcal{L}_{\mathrm{recon}} + \mathcal{L}_{\mathrm{seg}} + \lambda_{\mathrm{kl}} \cdot \mathcal{L}_{\mathrm{kl}}$$

其中 $\mathcal{L}_{\mathrm{seg}}$ 为新增的分割损失项。这一设计使得统一的隐空间能够同时表征整体几何与部件语义，为后续可控部件级生成奠定了基础。

### 2. 生成流水线：从单阶段到两阶段级联

与 **PartCrafter**（Lin et al., 2025）、**OmniPart**（Yang et al., 2025）等方法的单阶段生成或先生成再分割范式不同，UniPart 采用**两阶段潜变量扩散流水线**：

- **第一阶段（整体级 DiT）**：以输入图像为条件，通过整流流扩散（Rectified Flow）生成全局的 Geom-Seg VecSet 隐变量 $\hat{Z}_0$，训练目标为条件流匹配损失：

  $$\mathcal{L}_{\mathrm{cfm}}(\theta) = \mathbb{E}_{t, Z_0, \epsilon} \| v_{\theta}(Z_t, t | I) - (\epsilon - Z_0) \|_2^2$$

  随后，冻结的分割解码器 $D_{\mathrm{seg}}$ 对该全局隐变量进行潜空间分割，产生每个部件的隐变量掩码；同时，一个轻量位置解码器 $D_{\mathrm{pos}}$ 恢复每个隐向量的锚点三维坐标，辅助分割后处理。

- **第二阶段（部件级 DiT）**：以输入图像和第一阶段生成的全局隐变量为条件，对每个部件独立进行潜变量扩散生成。这一级联设计使得部件生成能够利用全局上下文信息，同时保持部件级的精细控制。

### 3. 部件生成空间：从全局坐标到双空间协同

传统方法直接在全局坐标空间中生成部件网格，容易导致部件几何扭曲和组合错位。UniPart 提出**双空间生成机制**，将每个部件的隐变量同时表示在全局坐标空间（Global Coordinate Space, GCS）和归一化规范空间（Normalized Canonical Space, NCS）中。

在部件级 DiT 中，双空间注意力机制由两部分组成：

- **局部注意力**（单空间内）：对每个空间内的隐向量独立建模部件内部结构

  $$\mathrm{Attn}_{\mathrm{local}} = \mathrm{Softmax}\left(\frac{\sigma_q(X_i^s)^\top \sigma_k(X_i^s)}{\sqrt{h}}\right) \sigma_v(X_i^s)$$

- **全局注意力**（跨空间）：融合两个空间的表征，确保部件在全局场景中的位置一致性和形状规范性

  $$\mathrm{Attn}_{\mathrm{global}} = \mathrm{Softmax}\left(\frac{\sigma_q(X_i^*)^\top \sigma_k(X_i^*)}{\sqrt{h}}\right) \sigma_v(X_i^*)$$

消融实验（Figure 7）验证了该设计的必要性：去除 NCS 生成后部件几何扭曲且组合错位；去除局部注意力后部件内部结构不连贯；去除空间嵌入注入后双空间无法有效区分，导致位置和形状失真。最终，两个空间的潜变量通过共享的预训练几何解码器分别解码为网格 $\bar{\mathcal{M}}_i^{\mathrm{gcs}}$ 和 $\mathcal{M}_i^{\mathrm{ncs}}$，组合得到完整的部件级三维模型 $\mathcal{O} = \{\mathcal{M}_i\}_{i=1}^N$。

## 整体框架

UniPart 的整体流水线围绕一个核心设计展开：**将部件分割语义与三维几何编码进统一的隐空间**，并以此为基础构建两阶段级联扩散模型，实现从单张图像到可分解部件网格的端到端生成。流水线由三大模块串联构成（见图 2）。

### 1. Geom-Seg VAE：几何-分割联合隐空间

流水线的基石是一个几何-分割联合变分自编码器（Geom-Seg VAE）。其输入为完整物体的三维形状及其部件分割标注，输出为 **Geom-Seg VecSet**——一组隐向量集合，其中每个隐向量同时承载局部几何贡献与部件语义标签。训练损失在标准 VecSet VAE 的重建项与 KL 正则项基础上，显式加入分割损失 $\mathcal{L}_{\mathrm{seg}}$：

$$
\mathcal{L}_{\mathrm{vecset}} = \mathcal{L}_{\mathrm{recon}} + \mathcal{L}_{\mathrm{seg}} + \lambda_{\mathrm{kl}} \cdot \mathcal{L}_{\mathrm{kl}}
$$

这一设计使得隐空间自发形成与语义部件对齐的聚类结构——论文通过 Hunyuan3D-2.1 DiT 的自注意力图验证了该现象（Figure 1）：同一语义部件内的隐向量呈现强相关，表明部件感知在纯几何生成过程中已隐含存在。Geom-Seg VAE 将这种隐含感知显式化，为下游扩散模型提供了统一的几何-语义操作空间。

### 2. 整体级 DiT：全局生成与隐式分割

在第一阶段，一个整体级整流流扩散 Transformer（Whole-level DiT）以输入图像为条件，直接生成全局 Geom-Seg VecSet $\hat{Z}_0$。训练目标采用条件流匹配（Conditional Flow Matching）：

$$
\mathcal{L}_{\mathrm{cfm}}(\theta) = \mathbb{E}_{t, Z_0, \epsilon} \| v_{\theta}(Z_t, t | I) - (\epsilon - Z_0) \|_2^2
$$

得到全局隐变量后，利用 Geom-Seg VAE 中**冻结的分割解码器 $D_{\text{seg}}$** 对每个隐向量预测部件标签，完成隐式部件分割。同时，一个轻量位置解码器 $D_{\text{pos}}$ 恢复每个隐向量的锚点三维坐标，辅助后续分割后处理。至此，整体级 DiT 输出两样东西：全局几何隐变量，以及按部件划分的隐变量掩码。

### 3. 部件级 DiT：双空间精修与组合

第二阶段，部件级扩散 Transformer（Part-level DiT）以输入图像和整体级输出的部件隐变量为联合条件，对各部件隐变量进行精修生成。关键创新在于**双空间生成机制**：每个部件同时在全局坐标空间（GCS）和归一化规范空间（NCS）中建模，通过局部-全局交替注意力实现空间内一致性与跨空间对齐：

- **局部注意力**在单一空间内捕捉部件内部结构：
  $$\mathrm{Attn}_{\mathrm{local}} = \mathrm{Softmax}\left(\frac{\sigma_q(X_i^s)^\top \sigma_k(X_i^s)}{\sqrt{h}}\right) \sigma_v(X_i^s)$$

- **全局注意力**跨两个空间协调部件位姿与形状：
  $$\mathrm{Attn}_{\mathrm{global}} = \mathrm{Softmax}\left(\frac{\sigma_q(X_i^*)^\top \sigma_k(X_i^*)}{\sqrt{h}}\right) \sigma_v(X_i^*)$$

精修后的部件隐变量经共享几何解码器分别解码为 GCS 网格与 NCS 网格，最终组合为完整的可分解物体网格 $\mathcal{O} = \{ \mathcal{M}_i \}_{i=1}^N$。

### 输入输出流总结

| 阶段 | 输入 | 输出 |
|------|------|------|
| Geom-Seg VAE（训练） | 完整网格 + 部件分割标注 | Geom-Seg VecSet |
| 整体级 DiT（推理） | 单张 RGB 图像 | 全局几何隐变量 + 部件隐变量掩码 |
| 部件级 DiT（推理） | 图像 + 部件隐变量条件 | 各部件精修隐变量（双空间） |
| 共享几何解码器 | 部件隐变量 | 可分解部件网格 |

整个流水线的核心优势在于：部件分割并非后处理步骤，而是从隐空间构建之初就内嵌于表示之中，使得整体生成与部件精修共享同一语义空间，避免了传统“先生成再分割”范式中的几何-语义错位问题。

### 补充图表

![[assets/figures/papers/paper_list_l2616_https_arxiv_org_abs_2512_09435/figures/003_Figure_2.jpg]]
*Figure 2: The pipeline of UniPart. It includes a Geom-Seg VAE that encodes both whole geometry and part segmentation information into a unified representation, Geom-Seg VecSet. The image-guided part-level generation adopts a two-level pipeline, where a whole-level DiT first generates the whole geometry and segmented part latent, and a part-level DiT then accepts the input image and the whole-part latent as conditions for dual-space part latent generation. The final object mesh is composed of each full-resolution part mesh*

## 核心模块与公式推导

UniPart 的核心架构由三个关键模块构成：**Geom-Seg VAE**（统一几何-分割变分自编码器）、**Whole-level DiT**（整体级扩散Transformer）和**Part-level DiT**（部件级扩散Transformer），三者协同完成从单张图像到可分解部件网格的端到端生成。

### 3.1 Geom-Seg VAE：统一的几何-分割隐空间

该模块的根本创新在于将部件分割信息显式融入几何隐变量，构建 **Geom-Seg VecSet** 表示。传统 VecSet VAE 仅编码几何信息，其训练目标为：

$$\mathcal{L}_{\mathrm{vecset}} = \mathcal{L}_{\mathrm{recon}} + \lambda_{\mathrm{kl}} \cdot \mathcal{L}_{\mathrm{kl}}$$

UniPart 在此基础上引入分割损失，使每个隐向量同时承载其几何贡献与部件标签信息，扩展后的联合训练目标为：

$$\mathcal{L}_{\mathrm{vecset}} = \mathcal{L}_{\mathrm{recon}} + \mathcal{L}_{\mathrm{seg}} + \lambda_{\mathrm{kl}} \cdot \mathcal{L}_{\mathrm{kl}}$$

其中 $\mathcal{L}_{\mathrm{recon}}$ 为几何重建损失，$\mathcal{L}_{\mathrm{seg}}$ 为部件分割交叉熵损失，$\mathcal{L}_{\mathrm{kl}}$ 为隐空间正则化项，$\lambda_{\mathrm{kl}}$ 控制正则化强度。这一设计的因果机制在于：通过在压缩阶段强制隐空间同时保留几何与语义信息，解码器可从同一隐变量中恢复完整形状并输出每个隐向量的部件标签，从而避免额外依赖外部预训练分割器。

### 3.2 Whole-level DiT：整体生成与隐式分割

整体级扩散模型采用整流流（Rectified Flow）框架，在 Geom-Seg VAE 的隐空间上进行条件生成。给定输入图像 $I$，模型学习从噪声 $\epsilon$ 到干净隐变量 $Z_0$ 的速度场 $v_\theta$，训练目标为条件流匹配损失：

$$\mathcal{L}_{\mathrm{cfm}}(\theta) = \mathbb{E}_{t, Z_0, \epsilon} \| v_{\theta}(Z_t, t | I) - (\epsilon - Z_0) \|_2^2$$

其中 $Z_t = t Z_0 + (1-t) \epsilon$ 为扩散时间步 $t$ 处的隐变量。该模块的核心洞察在于：**纯整体几何生成过程中，扩散Transformer的自注意力已自发形成与语义部件高度相关的聚类**（如 Figure 1 所示，相同语义部件内的隐变量呈现强相关性）。基于此，UniPart 在整体生成后冻结分割解码器 $D_{\mathrm{seg}}$，对去噪后的全局隐变量 $\hat{Z}_0$ 进行部件标签预测，实现无需额外标注的隐式部件分割。同时，一个轻量位置解码器 $D_{\mathrm{pos}}$ 恢复每个隐向量的锚点三维坐标 $p_i^{\mathrm{latent}} = D_{\mathrm{pos}}(\hat{z}_i)$，辅助后续部件隐变量的空间定位。

![[assets/figures/papers/paper_list_l2616_https_arxiv_org_abs_2512_09435/figures/002_Figure_1.jpg]]
*Figure 1: Latent correlation maps from Hunyuan3D-2.1 DiT attention at inference. Latents (points) correlate strongly within the same semantic part, suggesting implicit part awareness*

### 3.3 Part-level DiT：双空间部件精修

部件级扩散模型接收整体隐变量 $\hat{Z}_0$ 和分割掩码作为条件，对每个部件独立生成高质量几何。其关键设计是**双空间生成机制**：每个部件同时在全局坐标空间（GCS）和归一化规范空间（NCS）中表示，前者保持部件间的空间关系，后者消除全局位姿干扰以专注局部几何细节。

双空间扩散的注意力机制分为两个层次。**局部注意力**在单一空间内捕捉部件内部结构：

$$\mathrm{Attn}_{\mathrm{local}} = \mathrm{Softmax}\left(\frac{\sigma_q(X_i^s)^\top \sigma_k(X_i^s)}{\sqrt{h}}\right) \sigma_v(X_i^s)$$

其中 $X_i^s$ 表示第 $i$ 个部件在空间 $s \in \{\mathrm{gcs}, \mathrm{ncs}\}$ 中的隐变量，$\sigma_q, \sigma_k, \sigma_v$ 分别为查询、键、值的线性投影，$h$ 为注意力头维度。**全局注意力**则跨两个空间进行信息融合，确保双空间表示的一致性：

$$\mathrm{Attn}_{\mathrm{global}} = \mathrm{Softmax}\left(\frac{\sigma_q(X_i^*)^\top \sigma_k(X_i^*)}{\sqrt{h}}\right) \sigma_v(X_i^*)$$

此处 $X_i^*$ 为拼接了双空间隐变量的联合表示。消融实验（Figure 7）证实：去除 NCS 生成直接使用全局坐标会导致部件几何扭曲和组合错位；去除局部注意力使部件内部结构不连贯；去除空间嵌入注入则导致双空间无法有效区分，部件位置和形状均出现失真。最终，共享的预训练几何解码器将双空间部件隐变量解码为网格，通过坐标变换组合成完整的可分解三维物体 $\mathcal{O} = \{ \mathcal{M}_i \}_{i=1}^N$。

### 补充图表

![[assets/figures/papers/paper_list_l2616_https_arxiv_org_abs_2512_09435/figures/006_Figure_4.jpg]]
*Figure 4: Generated results of our whole-level DiT. (a) Input image; (b) Generated whole-object geometry; (c) Generated part latent segmentation. Please zoom in for details*

## 实验与分析

### 主实验设置与评估指标

UniPart 在从多个来源整理而成的部件级生成测试集上进行了系统评估。评估采用两个核心几何质量指标：**Chamfer Distance (CD)**（越低越好，×10²）衡量生成网格与真值之间的平均最近点距离，以及 **F1@0.1**（越高越好，×10²）衡量在一定阈值下的召回率与精确率平衡。对比的基线方法包括近期代表性工作：**PartCrafter** (Lin et al., 2025)、**OmniPart** (Yang et al., 2025)、**X-Part** (Yan et al., 2025) 和 **HoloPart** (Yang et al., 2025)，这些方法代表了当前部件级生成的不同技术路线。

### 主要定量结果

如 Table 1 所示，UniPart 在所有评估指标上均显著优于现有方法。具体而言，UniPart 将 CD 降至 **0.72**，F1@0.1 提升至 **92.21**，表明所生成的部件网格不仅整体形状更准确，而且细节保持更好。这一优势源于 Geom-Seg VecSet 统一隐空间对几何与分割信息的联合建模，以及两阶段扩散流水线中部件级精修对局部几何的有效增强。

![[assets/figures/papers/paper_list_l2616_https_arxiv_org_abs_2512_09435/figures/012_Table_1.jpg]]
*Table 1: Quantitative comparison on the geometry quality of partlevel generation results. Best results are marked in bold font. Our UniPart significantly outperforms other methods on both CD and F-score metrics*

Table 2 报告了 VAE 重建质量的定量比较，UniPart 的 Geom-Seg VAE 在保持高保真几何重建的同时，实现了准确的隐式部件分割，验证了联合训练策略的有效性。Table S1 进一步从分割角度以 mIoU 指标评估，确认了隐式分割解码器 D_seg 在部件标签预测上的准确性。

![[assets/figures/papers/paper_list_l2616_https_arxiv_org_abs_2512_09435/figures/011_Table_2.jpg]]
*Table 2: Quantitative comparison on the geometry quality of partlevel generation results. Best results are marked in bold font*

![[assets/figures/papers/paper_list_l2616_https_arxiv_org_abs_2512_09435/figures/015_Table_S.1.jpg]]
*Table S.1: Quantitative comparison on the geometry quality of part-level generation results. Best results are marked in bold font*

### 定性可视化分析

Figure 3 展示了 Geom-Seg VAE 的重建效果：输入网格的部件分割掩码（a）与重建几何（b）及重建的部件隐变量分割可视化（c）高度一致，验证了统一隐空间对几何与语义信息的有效编码能力。与 Hunyuan3D-2.1 的纯几何重建（d）相比，Geom-Seg VAE 在保持几何质量的同时额外提供了部件级语义。

Figure 4 展示了整体级 DiT 的生成效果：给定输入图像（a），模型生成的全局物体几何（b）与部件隐变量分割（c）在语义上合理对应，证明从整体生成中即可获得初步的部件感知。

Figure 5 提供了更多部件级生成结果，展示了从输入图像到全局几何、再到分解的部件网格的完整流程，部件组合自然且边界清晰。

Figure 6 的定性比较直观展示了 UniPart 相对于基线方法的优势：PartCrafter 等方法的部件分割往往不够合理或几何质量退化，而 UniPart 生成的部件在语义合理性和几何精细度上均明显更优。

### 消融实验

Figure 7 通过可视化消融实验验证了三个关键设计选择：

![[assets/figures/papers/paper_list_l2616_https_arxiv_org_abs_2512_09435/figures/014_Figure_7.jpg]]
*Figure 7: Visual results of ablation studies for the design of Uni-Part, i.e., without using normalized canonical space (NCS) generation, local attention, and space embedding injection*

1. **去除归一化规范空间（NCS）生成**：直接使用全局坐标生成部件网格，导致部件几何扭曲和组合错位，说明 NCS 为每个部件提供的归一化局部坐标空间对于保持部件形状一致性至关重要。
2. **去除局部注意力机制**：部件内部结构变得不连贯，细节丢失严重，验证了局部注意力在捕捉部件内细粒度几何依赖关系中的核心作用。
3. **去除空间嵌入注入**：双空间生成无法有效区分全局坐标空间与规范空间，导致部件位置和形状同时失真，说明空间嵌入是双空间注意力机制正确运作的必要条件。

### 失败模式分析

Figure 8 系统展示了 UniPart 的典型失败案例，主要可归纳为以下模式：

![[assets/figures/papers/paper_list_l2616_https_arxiv_org_abs_2512_09435/figures/013_Figure_8.jpg]]
*Figure 8: Failure cases of our proposed UniPart. (a) Input images; (b) The whole object geometry output by our whole-level DiT; (c) The composed part meshes output by our part-level DiT; (d) The part latent segmentation visualization produced by our whole-level DiT*

- **非标准拓扑失效**：对于具有非标准拓扑结构或极端姿态的物体，整体级 DiT 的隐式分割可能产生不合理的部件分解，例如将语义上应属于同一部件的区域错误分割。
- **罕见类别泛化不足**：方法依赖高质量的部件标注数据进行训练，对于训练分布外的未见类别，分割质量和几何生成精度均出现退化。
- **细微结构退化**：薄壁结构或复杂拓扑连接处的几何重建仍存在退化现象，表现为网格不完整或表面噪声增加。

这些失败模式揭示了当前方法的核心局限：统一的几何-分割隐空间虽能有效捕捉常见物体的部件结构，但对拓扑变异和极端几何的鲁棒性仍需提升，且对标注数据的依赖限制了其在新类别上的泛化能力。

## 方法谱系与知识库定位

### 1. 在部件级三维生成中的位置

部件级三维生成（part-level 3D generation）是三维生成领域的前沿方向，其目标是从图像、文本等输入直接生成具有语义可分解性的三维物体，即输出由多个独立部件网格组成的完整物体 $\mathcal{O} = \{ \mathcal{M}_i \}_{i=1}^N$。该任务的核心挑战在于同时保证**部件分割的语义合理性**与**部件几何的高保真度**。

现有方法大致分为两条技术路线：

- **生成后分割（generate-then-segment）**：先利用整体生成模型（如 **Hunyuan3D-2.1**）生成完整网格，再借助外部预训练分割器进行后处理分解。代表工作包括 **PartCrafter**（Lin et al., 2025）和 **OmniPart**（Yang et al., 2025）。此类方法对分割器精度高度依赖，且分割与生成过程解耦，难以端到端优化部件几何质量。

- **隐式部件感知生成**：在生成过程中隐式建模部件结构，如 **X-Part**（Yan et al., 2025）和 **HoloPart**（Yang et al., 2025）。这些方法试图在生成过程中融入部件信息，但由于缺乏统一的几何-分割隐空间，部件语义的粒度控制和几何一致性仍受限制。

UniPart 在方法谱系中的定位是**端到端联合几何-分割隐空间的部件级生成**，其核心创新在于将部件分割信息直接融入几何隐变量，形成统一的 Geom-Seg VecSet 表示，从而避免了对外部分割器的依赖，并在统一的扩散框架内实现从整体到部件的两阶段生成。

### 2. 关键设计选择与替代方案的权衡

#### 2.1 统一隐空间 vs. 解耦表示

UniPart 选择将几何与分割信息编码至同一 VecSet 隐空间，而非分别维护独立的几何隐变量和分割隐变量。这一设计的因果逻辑源于 Figure 1 的发现：在 **Hunyuan3D-2.1** 的 DiT 自注意力图中，隐变量在相同语义部件内部呈现强相关性，表明纯整体几何生成过程中已自发形成隐式部件感知。基于此，将分割信息显式注入同一隐空间是自然的归纳偏置——它使模型无需学习从几何到分割的跨模态映射，而是直接利用已有的隐式结构。

替代方案（如解耦的几何编码器+分割编码器）将引入额外的跨模态对齐损失和训练复杂度，且可能破坏几何隐变量中已存在的部件聚类结构。

#### 2.2 两阶段扩散 vs. 单阶段生成

UniPart 采用“整体级 DiT → 部件级 DiT”的两阶段流水线，而非直接生成部件隐变量。这一选择的核心因果机制在于：整体级扩散为部件级扩散提供了全局上下文条件（$Z_0$），使部件生成过程能够感知整体形状约束，避免部件间的穿透和错位。若采用单阶段直接生成各部件隐变量，则缺乏全局协调机制，部件组合的几何一致性将难以保证。

#### 2.3 双空间生成 vs. 单一全局坐标空间

部件级 DiT 在全局坐标空间（GCS）和归一化规范空间（NCS）两个空间中同时生成部件隐变量，并通过局部-全局注意力机制进行跨空间信息交换。消融实验（Figure 7）表明：
- **去除 NCS 生成**：直接使用全局坐标生成部件网格，导致部件几何扭曲和组合错位；
- **去除局部注意力**：部件内部结构不连贯，细节丢失；
- **去除空间嵌入注入**：双空间生成无法有效区分，部件位置和形状失真。

NCS 的引入为每个部件提供了归一化的局部坐标系，使部件几何学习不受其在全局空间中位姿的影响，本质上是一种**几何解耦策略**——将“部件形状”与“部件位姿”的学习分离，降低了扩散模型的优化难度。

### 3. 方法适用边界与局限

尽管 UniPart 在定量指标上显著优于现有方法（Table 1：CD 降至 0.72，F1@0.1 达 92.21），其方法仍存在明确的适用边界：

- **拓扑泛化受限**：对于非标准拓扑或极端姿态下的物体，部件分割可能失败或产生不合理分解（Figure 8）。这表明 Geom-Seg VAE 学到的部件语义与训练数据中的常见拓扑结构高度相关，对分布外拓扑的泛化能力有限。

- **标注数据依赖**：Geom-Seg VecSet 的训练需要高质量的部件标注数据，这限制了方法向新未见类别的直接迁移。当前方法未验证在零样本或少样本部件分割场景下的性能。

- **细粒度几何退化**：细微部件或薄壁结构的几何重建仍存在退化，尤其在复杂拓扑连接处。这可能是 VecSet 表示本身的分辨率瓶颈所致——有限数量的隐向量难以精确编码极端细粒度的几何细节。

- **推理效率**：两阶段扩散模型（整体级 + 部件级）的联合推理时间较长，难以满足实时交互式应用需求。这是级联扩散模型的固有代价。

### 4. 开放问题与未来方向

基于上述局限，以下开放问题值得进一步探索：

1. **弱监督与零样本扩展**：如何减少对手工部件标注的依赖？可能的路径包括利用大规模三维数据中的自监督信号（如运动结构、对称性）学习部件语义，或借助视觉-语言模型的知识蒸馏实现开放词汇的部件分割。

2. **多层级部件结构**：当前方法仅支持单层部件分解。双空间生成策略是否适用于更复杂的多层级部件树（如组件包含子部件）？这需要扩展隐空间表示以编码层级化的部件关系。

3. **闭环纠错机制**：能否引入物理约束或几何一致性检查作为闭环反馈，以纠正部件间的穿透或错位？例如，在推理阶段加入碰撞检测引导的拒绝采样或梯度引导。

4. **跨模态扩展**：统一的几何-分割隐空间如何扩展到文本或草图驱动的生成任务？这需要在条件注入机制上进行适配，使分割语义能够响应非图像模态的条件信号。

5. **推理加速**：如何通过蒸馏、一致性模型或级联去噪调度策略降低两阶段扩散的联合推理成本，是走向实际应用的关键工程问题。

## 原文 PDF

![[paperPDFs/CVPR_2026/UniPart_Part_Level_3D_Generation_with_Unified_3D_Geom_Seg_Latents.pdf]]