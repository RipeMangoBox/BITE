---
title: Masked-Diffusion Autoencoders for 3D Medical Vision Representation Learning
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/Masked_Diffusion_Autoencoders_for_3D_Medical_Vision_Representation_Learning.pdf
project_link: null
code_link: null
aliases:
- MDAM
- MDA3MVRL
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
- topic/generative_models_diffusion
- topic/representation_self_supervised_transfer
core_operator: 像素空间的双重损坏机制（空间掩码 + 扩散噪声）
primary_logic: 同时施加空间掩码与扩散噪声，迫使模型在执行掩码区域重建（学习全局结构）和可见区域去噪（学习纹理特征）这两个互补任务中，通过时间条件架构自适应调整重建策略，实现结构-纹理联合表征学习，突破传统方法在3D医学影像中的性能瓶颈。
claims:
- MDAE在16个临床基准上始终优于现有自监督基线，尤其在跨模态泛化任务上优势显著。
- 消融实验表明掩码与噪声具有协同效益，可变掩码策略优于固定掩码比例。
- In-distribution (3 tasks × 2 modalities) 上 平均AUROC = 73.6%
- Cross-modal generalization (6 OOD tasks) 上 平均AUROC = 78.6%
---

# Masked-Diffusion Autoencoders for 3D Medical Vision Representation Learning

> [!tip] 核心洞察
> 同时施加空间掩码与扩散噪声，迫使模型在执行掩码区域重建（学习全局结构）和可见区域去噪（学习纹理特征）这两个互补任务中，通过时间条件架构自适应调整重建策略，实现结构-纹理联合表征学习，突破传统方法在3D医学影像中的性能瓶颈。

| 字段 | 内容 |
|------|------|
| 中文题名 | 掩码扩散自编码器：面向3D医学视觉表征学习 |
| 英文题名 | Masked-Diffusion Autoencoders for 3D Medical Vision Representation Learning |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://openaccess.thecvf.com/content/CVPR2026/html/Tu_Masked-Diffusion_Autoencoders_for_3D_Medical_Vision_Representation_Learning_CVPR_2026_paper.html) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction #topic/generative_models_diffusion #topic/representation_self_supervised_transfer |
| Method | Masked-Diffusion Autoencoders (MDAE) |
| Dataset | In-distribution, Cross-modal generalization, BraTS18 tumor grading, UCSF-PDGM IDH classification |

> [!tip] 效果简介
> - In-distribution (3 tasks × 2 modalities) 上，平均AUROC 73.6% vs 最佳基线（详见Table 1） (全面超越基线)。
> - Cross-modal generalization (6 OOD tasks) 上，平均AUROC 78.6% vs 最佳基线（详见Table 2） (全面超越基线)。
> - BraTS18 tumor grading 上，AUROC 92.1% vs 最佳基线（详见Table 3） (最高)。

## 概要

### 问题背景

3D医学影像（如脑部MRI）的自监督表征学习面临一个核心瓶颈：现有方法难以同时捕捉全局解剖结构和细粒度组织纹理。**不变性对比学习**（如SimCLR、VoCo）依赖数据增强构建正负样本对，但医学影像中的关键诊断信息（如肿瘤边界、微小病灶）可能在增强过程中被破坏。**掩码图像建模**（如MAE）通过重建被遮挡区域学习结构表征，但通常需要高掩码比率（如75%）来制造足够困难的重建任务，这导致可见区域的纹理细节被牺牲。**扩散去噪方法**（如DSM）虽能学习纹理特征，但缺乏对全局结构的显式约束。三种范式各有所长却彼此割裂，无法形成统一的表征学习框架。

### 核心方法定位

**Masked-Diffusion Autoencoders (MDAE)** 提出了一种**像素空间双重损坏机制**来解决上述矛盾：对输入3D体积同时施加**空间掩码**（分块掩码可见区域）和**扩散噪声**（对全体素添加高斯噪声），迫使模型在一个统一框架内执行两个互补任务——

- **掩码区域重建**：从被噪声损坏的可见上下文推断被遮挡区域，迫使模型学习全局解剖结构和跨区域依赖关系；
- **可见区域去噪**：对被噪声污染的未掩码区域进行去噪，迫使模型学习细粒度组织纹理和局部特征。

这一设计的精妙之处在于：即使掩码比率较低（可见上下文较多），扩散噪声的存在仍使重建任务保持足够的挑战性，从而突破了传统MAE对高掩码比率的依赖。此外，MDAE通过**时间条件架构**（FiLM注入时间步嵌入）使网络感知噪声强度，自适应调整重建策略。从极限行为看，当噪声趋于零时MDAE退化为MAE，当掩码概率趋于零时退化为DSM，证明了框架的统一性。

### 主要结果

在**Open-Mind**数据集（114,570个3D脑部MRI体积，来自34,191名受试者）上预训练后，MDAE在16个临床基准上全面超越现有自监督基线：

- **分布内任务**（T1/T2模态，3项脑肿瘤分类）：平均AUROC达**73.6%**，全面超过SimCLR、VoCo、MAE、Models Genesis等基线；
- **跨模态泛化**（6项OOD任务，涵盖ASL、SWI、FLAIR、T1GD等模态）：平均AUROC达**78.6%**，优势尤为显著，证明双重损坏机制学习到的表征具有更强的模态不变性；
- **多模态脑肿瘤评测**：BraTS18肿瘤分级AUROC达**92.1%**，UCSF-PDGM IDH分类AUROC达**93.0%**，UCSF-PDGM分割Dice达**85.2%**，均取得最优。

消融实验揭示了几个关键发现：(1) 掩码与噪声具有**协同效益**，在75%掩码且噪声幅度σ_max=1.0时达到全局最优；(2) **可变掩码策略**（从均匀分布采样掩码比例）优于所有固定掩码比例变体；(3) 像素空间损坏显著优于嵌入空间损坏（AUROC提升4.2–10.2个百分点）；(4) ResNet编码器显著优于Vision Transformer（AUROC提升12.1–13.8个百分点），表明卷积归纳偏置在3D医学影像表征学习中仍具优势。

### 方法谱系与知识库定位

MDAE处于**掩码自编码器**与**扩散去噪**两大范式的交叉点，其方法谱系可追溯至：

| 范式 | 代表工作 | 与MDAE的关系 |
|------|----------|-------------|
| 掩码图像建模 | **MAE** (He et al., CVPR 2022) | MDAE在掩码重建目标上的直接前身，但MAE仅使用空间掩码且依赖高掩码比率 |
| 扩散去噪 | **DSM** (Score Matching系列) | MDAE的去噪目标源自DSM，但DSM缺乏结构推理的显式约束 |
| 对比学习 | **SimCLR** (Chen et al., ICML 2020)、**VoCo** (Wu et al., CVPR 2024) | 作为基线被MDAE全面超越，验证了双重损坏机制相比不变性学习的优势 |
| 多尺度恢复 | **Models Genesis** (Zhou et al., MICCAI 2019) | 同为生成式预训练，但MDAE通过扩散噪声引入连续损坏尺度，灵活性更强 |
| 多模态预训练 | **BrainMVP** (Rui et al., CVPR 2025) | 聚焦多模态融合，MDAE则通过单模态预训练实现跨模态泛化 |

MDAE的核心贡献在于**将两种损坏机制统一于像素空间**，通过时间条件架构实现自适应重建，为3D医学视觉表征学习提供了新的基准框架。其开源预训练模型可作为下游任务的通用编码器初始化。

### 3D医学影像自监督学习的现实需求

标注3D医学影像（如脑部MRI）需要放射科专家逐层勾画，成本极高。自监督表征学习（SSL）通过在海量无标注数据上预训练编码器，使下游任务仅需少量标注即可取得强泛化能力，已成为医学影像分析的核心范式。然而，3D医学影像具备两个并行的诊断信息维度——**全局解剖结构**（如肿瘤位置与占位效应）和**细粒度组织纹理**（如水肿边界、坏死核心的异质性），这对SSL方法的设计提出了双重挑战。

### 现有方法的结构性缺口

当前主流的SSL路线可归为两类，各自存在系统性局限：

**不变性对比学习**（如**SimCLR**，Chen et al., ICML 2020；**VoCo**，Wu et al., CVPR 2024）通过数据增强构造正样本对，迫使模型学习增强不变的表征。问题在于，医学影像中具有诊断意义的信号——如微小钙化、局部水肿纹理——极易被常用的颜色抖动、高斯模糊等增强破坏。增强越强，不变性越好，但诊断信息丢失的风险也越大。

**掩码图像建模**（如**MAE**，He et al., CVPR 2022）随机掩码大比例图像块，要求模型从可见上下文重建缺失区域。为迫使模型学习有意义的全局结构，通常需要极高的掩码比率（如75%–90%）。然而，这种策略将模型的注意力集中在被掩码区域，**可见区域的纹理细节未被显式监督**，导致编码器在需要精细纹理辨识的下游任务上表征能力不足。

简言之，对比学习牺牲纹理保真度换取不变性，掩码建模牺牲可见区域细节换取结构推理——二者在3D医学影像场景中形成了互补但尚未被弥合的能力缺口。

### 扩散去噪的启示与统一契机

扩散模型中的**去噪得分匹配（DSM）** 提供了另一条路径：对干净数据添加高斯噪声，训练网络从噪声观测中恢复原始信号。DSM天然适合学习细粒度纹理特征，因为去噪过程要求模型辨别不同噪声水平下的局部模式。然而，纯DSM缺乏对全局结构的显式约束——当整张体积都被噪声损坏时，模型可能仅依赖局部平滑先验即可完成去噪，而无需理解器官或病灶的空间布局。

这揭示了一个关键契机：**空间掩码与扩散噪声在像素空间并非互斥，而是可以同时施加，形成两个互补的学习目标**——掩码区域重建强制模型进行全局结构推理，可见区域去噪保留并强化纹理特征学习。更重要的是，噪声的引入使重建任务在低掩码比率下仍保持足够难度，从而突破传统MAE对高掩码比的依赖。

### 本文的核心动机

基于上述分析，本文提出**掩码扩散自编码器（Masked-Diffusion Autoencoders, MDAE）**，核心思想是：在像素空间对3D医学影像同时施加空间掩码与扩散噪声，通过时间条件架构将两个目标统一到一个框架中。MDAE旨在解决一个瓶颈问题——**如何在单一预训练过程中同时捕获全局解剖结构与细粒度组织纹理**，从而提升下游任务在分布内、跨模态及多模态场景下的泛化性能。

## 核心方法与创新机理

### 问题诊断：3D医学影像表征的双重困境

现有3D医学影像自监督学习方法面临一个根本性瓶颈：**全局解剖结构学习与细粒度组织纹理捕捉无法兼得**。具体而言，以**SimCLR**（Chen et al., ICML 2020）为代表的不变性对比学习方法依赖数据增强构建正样本对，但这些增强操作（如随机裁剪、颜色扰动）可能丢失对诊断至关重要的影像信息；而以**MAE**（He et al., CVPR 2022）为代表的掩码图像建模方法通过高掩码比（通常75%以上）迫使模型学习全局结构，却以牺牲可见区域的纹理细节为代价——模型仅需从少量可见patch推断缺失区域，对可见区域的细粒度特征缺乏显式监督。扩散去噪方法（DSM）虽能学习纹理特征，但缺乏对全局结构的约束。这一结构性矛盾在3D脑部MRI中尤为突出：肿瘤分类既需要理解肿瘤与正常组织的全局空间关系，又需要捕捉微小的组织纹理异常。

### 核心思想：双重损坏下的结构-纹理联合学习

MDAE的核心创新在于**将空间掩码与扩散噪声同时施加于像素空间**，构建两个互补的学习目标：

1. **掩码区域重建**（结构学习）：从被噪声污染的可见上下文推断掩码体素的原始值，迫使模型理解全局解剖结构；
2. **可见区域去噪**（纹理学习）：对未被掩码的区域进行去噪恢复，迫使模型捕捉细粒度组织纹理。

这一设计的精巧之处在于：**噪声的存在使掩码重建任务即使在低掩码比下仍保持足够的挑战性**——可见区域被噪声污染，模型不能简单地“复制”可见体素来完成重建，而必须从噪声上下文中推理缺失结构。这突破了传统MAE必须依赖高掩码比的限制，使得结构学习与纹理学习可以在同一框架内协同进行。

### 关键创新点（Changed Slots）

#### 1. 损坏机制：从单一损坏到双重损坏

| 维度 | 基线方法 | MDAE |
|------|---------|------|
| 损坏类型 | 仅空间掩码（MAE）或仅扩散噪声（DSM） | 空间掩码 + 扩散噪声同时施加 |
| 学习目标 | 单一重建或单一去噪 | 掩码区域重建 + 可见区域去噪联合优化 |

这一改变的因果机制在于：**两种损坏在像素空间产生正交的监督信号**。掩码迫使模型进行空间推理（“缺失了什么结构？”），噪声迫使模型进行纹理推理（“被污染的体素原始值是多少？”）。两者叠加时，模型必须同时回答两个问题，从而学习到既包含结构信息又包含纹理信息的统一表征。消融实验的AUROC景观图（Figure 3a）直接验证了这一协同效应：在75%掩码且σ_max=1.0时达到全局最优AUROC 0.658，而纯掩码（σ_max→0）或纯去噪（p_mask→0）的性能均显著低于该最优组合。

#### 2. 掩码策略：从固定比例到可变采样

传统MAE采用固定高掩码比（如75%），但MDAE从均匀分布U(p_min, p_max)中采样可变掩码比例。这一改变的动机在于：**不同的掩码比例迫使模型学习不同尺度的结构信息**——低掩码比时模型关注局部细节，高掩码比时模型关注全局结构。可变采样使模型在预训练过程中经历从局部到全局的全频谱结构推理，从而学习到更鲁棒的多尺度表征。消融实验（Table 4）证实可变掩码策略优于所有固定比例变体，取得最高平均AUROC 0.662。

#### 3. 架构时间感知：从静态网络到时间条件网络

标准MAE的编码器-解码器不感知损坏程度，而MDAE引入时间条件机制：将扩散时间步t通过正弦位置编码映射为256维嵌入，再通过**FiLM**（Feature-wise Linear Modulation）注入编码器-解码器的每一层：

$$h_{out} = h_{in} \odot (\gamma(t_{emb}) + 1) + \beta(t_{emb})$$

这一设计的深层逻辑在于：**不同噪声水平对应不同的去噪难度，模型需要自适应调整其重建策略**。当噪声较弱时，模型可以更多地依赖可见区域的直接信息；当噪声较强时，模型必须更多地依赖学到的先验知识。时间条件使单一网络能够灵活应对从“几乎无噪声”到“完全噪声”的全频谱损坏场景，实现了MAE和DSM的统一——如公式所示，当σ_max→0时MDAE退化为MAE，当p_mask→0时退化为DSM。

#### 4. 像素空间损坏 vs. 嵌入空间损坏

一个重要的架构选择是**在像素空间而非嵌入空间施加损坏**。消融实验（Figure 3b）显示，像素空间损坏（MDAE）相比嵌入空间损坏（EMDAE）带来4.2–10.2个百分点的AUROC提升。其因果解释在于：像素空间的损坏保留了体素间的空间连续性，使模型能够利用局部上下文进行推理；而嵌入空间的损坏破坏了这种空间结构，迫使模型依赖更抽象的语义信息，在3D医学影像中这种抽象信息尚不足以支撑精确的重建。

#### 5. 编码器架构选择：卷积优于Transformer

消融实验（Figure 3c）揭示了一个反直觉的发现：ResNet编码器显著优于Vision Transformer，AUROC提升12.1–13.8个百分点。这与自然图像领域的趋势相悖，但符合3D医学影像的特性：**医学影像中的诊断特征往往具有局部性和平移不变性**（如肿瘤纹理、组织边界），卷积的归纳偏置天然适合捕捉这些特征；而Transformer的全局自注意力在缺乏海量预训练数据时可能引入过多的无关上下文噪声。这一发现本身构成了对3D医学影像表征学习中架构选择的重要启示。

### 统一框架的理论意义

MDAE的极限行为揭示了其作为统一框架的理论价值：

$$\mathcal{L}_{\mathrm{MDAE}} \to \begin{cases} \mathcal{L}_{\mathrm{MAE}}, & \text{as } \sigma_{\max} \to 0 \\ \mathcal{L}_{\mathrm{DSM}}, & \text{as } p_{\mathrm{mask}} \to 0 \end{cases}$$

这意味着MDAE并非简单的技术叠加，而是将掩码自编码器和扩散去噪模型统一在一个连续的损坏参数空间内。这一统一性使得MDAE能够根据下游任务需求灵活调整损坏策略，同时也为理解不同自监督学习目标之间的关系提供了新的视角。

MDAE 的整体 pipeline 围绕一个核心设计展开：**在像素空间对 3D 医学影像同时施加两种互补的损坏——空间掩码与扩散噪声**，迫使模型在统一的时间条件架构下联合学习全局解剖结构与细粒度组织纹理。图 2 展示了完整的框架流程。

### 输入损坏阶段

给定一个清洁的 3D 体积 $X_0$，MDAE 按以下顺序施加双重损坏：

1. **扩散噪声损坏**：首先对全体积施加方差爆炸（Variance Exploding, VE）扩散噪声，生成噪声观测 $\tilde{X}_t = X_0 + \sigma_t Z$，其中 $Z \sim \mathcal{N}(0, I)$，$\sigma_t$ 为时间步 $t$ 对应的噪声级别。噪声级别从 $[\sigma_{\min}, \sigma_{\max}]$ 范围内采样，控制损坏强度。
2. **分块空间掩码**：将体积划分为不重叠的 $16^3$ 体素块，每个块以概率 $p_{\text{mask}}$ 被整体掩码（块内所有体素置为掩码 token），以概率 $1 - p_{\text{mask}}$ 保持可见。掩码比例 $p_{\text{mask}}$ 从均匀分布 $\mathcal{U}(p_{\min}, p_{\max})$ 中采样，形成**可变掩码策略**。

最终输入网络的损坏体积记为 $\tilde{X}_t^M$，其中掩码区域仅保留掩码 token，可见区域则同时携带扩散噪声。

### 时间条件编码器-解码器

MDAE 采用 **时间条件 ResNet U-Net** $g_\theta(\tilde{X}_t^M, t)$ 作为骨干网络。其关键设计在于：

- **时间嵌入**：时间步 $t$ 通过正弦位置编码映射为 256 维嵌入向量，再经 MLP 变换。
- **FiLM 条件调制**：该时间嵌入通过特征线性调制（Feature-wise Linear Modulation, FiLM）注入编码器和解码器的每一层：

  $$h_{\text{out}} = h_{\text{in}} \odot (\gamma(t_{\text{emb}}) + 1) + \beta(t_{\text{emb}})$$

  其中 $\gamma$ 和 $\beta$ 为可学习的缩放与偏移参数。这使得网络能够根据噪声级别自适应调整重建策略——低噪声时侧重结构重建，高噪声时侧重去噪。

- **跳跃连接**：U-Net 的跳跃连接将编码器特征直接传递到解码器对应层，保留空间细节信息。

### 双目标损失函数

MDAE 的训练目标由两个互补的损失项加权组合而成：

$$\mathcal{L}_{\mathrm{MDAE}}(\theta) = \lambda_{\mathrm{masked}} \cdot \mathcal{L}_{\mathrm{masked}}(\theta) + \lambda_{\mathrm{visible}} \cdot \mathcal{L}_{\mathrm{visible}}(\theta)$$

- **掩码区域重建损失** $\mathcal{L}_{\mathrm{masked}}$：仅对掩码体素计算 MSE，迫使模型从损坏的可见上下文推断缺失区域的全局结构：

  $$\mathcal{L}_{\mathrm{masked}}(\theta) = \mathbb{E}\left[ \frac{1}{|\Omega_M|} \cdot \| M \odot (g_\theta(\tilde{X}_t^M, t) - X_0) \|_2^2 \right]$$

- **可见区域去噪损失** $\mathcal{L}_{\mathrm{visible}}$：对未掩码区域施加去噪监督，使用噪声级别加权 $w(\sigma_t)$ 平衡不同噪声水平的贡献，迫使模型学习细粒度纹理特征：

  $$\mathcal{L}_{\mathrm{visible}}(\theta) = \mathbb{E}\left[ \frac{w(\sigma_t)}{|\Omega_V|} \cdot \| M_v \odot (g_\theta(\tilde{X}_t^M, t) - X_0) \|_2^2 \right]$$

### 框架的统一性

MDAE 具有优雅的极限行为，将 MAE 和 DSM 统一为特例：

$$\mathcal{L}_{\mathrm{MDAE}} \to \begin{cases} \mathcal{L}_{\mathrm{MAE}}, & \text{当 } \sigma_{\max} \to 0 \\ \mathcal{L}_{\mathrm{DSM}}, & \text{当 } p_{\mathrm{mask}} \to 0 \end{cases}$$

当噪声趋于零时，框架退化为标准 MAE；当掩码概率趋于零时，退化为去噪得分匹配（DSM）。这种统一性使得 MDAE 能够在两个极端之间平滑插值，通过双重损坏的协同作用，在较低掩码比率下即可实现有效的表征学习——去噪目标的存在确保了即使更多上下文可见时，重建任务仍具挑战性。

### 补充图表

![[assets/figures/papers/paper_list_l2541_https_openaccess_thecvf_com_content_CVPR2026_html_Tu_Masked_Diffusion_Au/figures/002_Figure_2.jpg]]
*Figure 2: MDAE Framework. A 3D volume is jointly corrupted by patch-based masking (blocky*

### 4.1 双重损坏机制

MDAE的核心创新在于像素空间同时施加**空间掩码**与**扩散噪声**两种损坏，形成互补的学习目标。与MAE仅掩码或DSM仅加噪不同，双重损坏迫使模型在掩码区域重建（学习全局解剖结构）和可见区域去噪（学习细粒度组织纹理）之间建立联合表征。

**分块空间掩码**：将3D体积划分为不重叠的 $16^3$ 体素块，每个块以概率 $p_{\text{mask}}$ 独立决定是否被掩码。掩码比例从均匀分布 $\mathcal{U}(p_{\min}, p_{\max})$ 中采样，而非采用固定比例，使模型适应不同难度的重建任务。

**扩散噪声损坏**：采用方差爆炸（Variance Exploding, VE）噪声调度，对清洁体积 $X_0$ 添加高斯噪声：

$$\tilde{X}_t = X_0 + \sigma_t Z, \quad Z \sim \mathcal{N}(0, I)$$

其中 $\sigma_t$ 为噪声级别，控制损坏强度。噪声先于掩码施加于全局体积，确保可见区域也包含噪声信息。

### 4.2 时间条件架构

MDAE采用**时间条件U-Net**作为骨干网络 $g_\theta(\tilde{X}_t^M, t)$。时间步 $t$ 通过正弦位置编码映射为256维嵌入，经MLP后通过**特征线性调制（FiLM）**注入编码器和解码器的每一层：

$$h_{\text{out}} = h_{\text{in}} \odot (\gamma(t_{\text{emb}}) + 1) + \beta(t_{\text{emb}})$$

其中 $\gamma$ 和 $\beta$ 为从时间嵌入学习的缩放与偏置参数。时间条件使网络能根据噪声级别自适应调整重建策略：低噪声时侧重结构重建，高噪声时侧重纹理去噪。

### 4.3 双目标损失函数

MDAE的总损失为掩码区域重建损失与可见区域去噪损失的加权组合：

$$\mathcal{L}_{\text{MDAE}}(\theta) = \lambda_{\text{masked}} \cdot \mathcal{L}_{\text{masked}}(\theta) + \lambda_{\text{visible}} \cdot \mathcal{L}_{\text{visible}}(\theta)$$

**掩码区域损失** $\mathcal{L}_{\text{masked}}$：仅对掩码体素计算MSE，迫使模型从损坏的可见上下文推断缺失的解剖结构：

$$\mathcal{L}_{\text{masked}}(\theta) = \mathbb{E}\left[ \frac{1}{|\Omega_M|} \cdot \| M \odot (g_\theta(\tilde{X}_t^M, t) - X_0) \|_2^2 \right]$$

**可见区域损失** $\mathcal{L}_{\text{visible}}$：对未掩码区域去噪，使用噪声级别加权 $w(\sigma_t)$ 平衡各噪声水平的贡献：

$$\mathcal{L}_{\text{visible}}(\theta) = \mathbb{E}\left[ \frac{w(\sigma_t)}{|\Omega_V|} \cdot \| M_v \odot (g_\theta(\tilde{X}_t^M, t) - X_0) \|_2^2 \right]$$

### 4.4 框架统一性

MDAE的两个极限行为揭示了其作为统一框架的本质：

$$\mathcal{L}_{\text{MDAE}} \to \begin{cases} \mathcal{L}_{\text{MAE}}, & \text{as } \sigma_{\max} \to 0 \\ \mathcal{L}_{\text{DSM}}, & \text{as } p_{\text{mask}} \to 0 \end{cases}$$

当噪声趋于零时退化为标准MAE，当掩码概率趋于零时退化为DSM。这种统一性使得MDAE能够同时继承掩码建模的结构学习能力与扩散模型的纹理表征能力，突破传统方法在3D医学影像中结构-纹理难以兼顾的瓶颈。

### 补充图表

![[assets/figures/papers/paper_list_l2541_https_openaccess_thecvf_com_content_CVPR2026_html_Tu_Masked_Diffusion_Au/figures/001_Figure_1.jpg]]
*Figure 1: Comparison of corruption schemes. Left: MAE applies fixed masking corruption. Middle: DSM applies diffusion noise. Right: MDAE combines spatial masking with diffusion noising, creating dual objectives for holistic reconstruction and fine-grained denoising*

## 实验与关键发现

### 主结果：分布内与跨模态泛化性能

MDAE在三个评测场景中均取得最优性能，验证了双重损坏机制在3D医学影像表征学习中的有效性。

**分布内评测（Table 1）**：在T1和T2模态的三个脑肿瘤分类任务（BraTS23胶质瘤vs转移瘤分型、RSNA-MICCAI MGMT甲基化状态、UPenn-GBM IDH1突变检测）上，MDAE取得73.6%的平均AUROC和71.6%的平均AP，全面超越SimCLR、VoCo、MAE、Models Genesis等基线方法。该结果证明，同时施加空间掩码与扩散噪声的双重损坏策略，相比纯掩码建模或纯对比学习，能更有效地捕获诊断相关的3D特征。

**跨模态泛化评测（Table 2）**：在6个分布外（OOD）任务上——包括UCSF-PDGM的ASL/SWI模态IDH分类、UPenn-GBM的FLAIR模态年龄分组、T1GD模态肿瘤全切除状态预测，以及TCGA-GBM的混合序列一年生存与无进展间期预测——MDAE取得78.6%的平均AUROC和75.4%的平均AP，优势尤为显著。这表明双重损坏迫使模型学习模态不变的结构-纹理联合表征，而非依赖特定序列的浅层统计特征。部分基础模型（BrainIAC、MRI-Core）未对TCGA任务提供预测，MDAE在此类缺失模态场景下仍保持领先。

**多模态脑肿瘤评测（Table 3）**：在BraTS18（4模态）和UCSF-PDGM（6模态）数据集上，MDAE在分类和分割任务中均取得最高指标——BraTS18肿瘤分级AUROC达92.1%，UCSF-PDGM IDH分类AUROC达93.0%，UCSF-PDGM分割Dice达85.2%。这进一步验证了MDAE表征在多模态融合场景下的鲁棒性。

### 消融实验：损坏机制与架构设计的协同效应

消融实验系统性地揭示了MDAE各组件的贡献及其交互机制。

**掩码与噪声的协同效益（Figure 3a）**：通过扫描掩码比例（25%/50%/75%/90%）与噪声水平（σ_max=0/0.5/1.0/1.5）的参数空间，发现两者存在显著的非线性交互。全局最优AUROC 0.658出现在75%掩码且σ_max=1.0的配置，验证了两者结合优于单独使用任一种损坏。当σ_max→0时，MDAE退化为纯MAE；当掩码比例→0时，退化为纯DSM——这两种退化情形的性能均低于联合配置。

**像素空间vs嵌入空间损坏（Figure 3b）**：在嵌入空间施加损坏（EMDAE）导致AUROC下降4.2–10.2个百分点。这表明在像素空间直接操作对于迫使模型学习可迁移表征至关重要，嵌入空间的损坏可能破坏了潜在空间的语义结构。

**掩码策略消融（Table 4）**：块状掩码（16³体素块）显著优于随机体素掩码（AUROC 0.623 vs 0.600），原因是块状掩码保留了医学影像的解剖结构完整性。可变掩码策略（从均匀分布U(p_min, p_max)采样）进一步优于所有固定比例变体，取得最高平均AUROC 0.662，表明动态调整掩码难度有助于模型学习更鲁棒的表征。

**噪声调度对比**：VE、VP与Flow Matching三种噪声调度表现几乎一致（AUROC分别为0.615、0.613、0.614），说明MDAE框架对噪声调度选择不敏感，核心收益来自双重损坏机制本身而非特定噪声设计。

**编码器架构选择（Figure 3c）**：ResNet编码器显著优于Vision Transformer（AUROC提升12.1–13.8个百分点），且时间条件调制（FiLM）的引入进一步提升了ResNet的性能。这一发现与自然图像领域的结论相反，提示3D医学影像的局部纹理特征对卷积归纳偏置有更强的依赖。

**损失权重消融（Table 5）**：在UCSF-PDGM上对λ_masked和λ_visible进行网格搜索，结果表明两者权重在合理范围内（如1:1至1:2）对性能影响有限，MDAE对损失权重不敏感，具有较好的训练稳定性。

### 公平性与局限性

实验采用Open-Mind公开数据集（114,570个3D脑部MRI体积，来自34,191名受试者），使用分层划分（stratified splits）确保评测可复现。然而，论文未进行人口学属性（年龄、性别、种族）或设备厂商相关的公平性分析，MDAE在不同人群亚组上的性能偏差需进一步验证。此外，当前评测仅覆盖脑部MRI，方法在胸部CT、腹部MRI等其他器官/模态上的泛化性尚未探索。

### 补充图表

![[assets/figures/papers/paper_list_l2541_https_openaccess_thecvf_com_content_CVPR2026_html_Tu_Masked_Diffusion_Au/figures/003_Table_1.jpg]]
*Table 1: Performance comparison on T1 and T2 modalities. All methods are evaluated on three brain tumor classification tasks: BraTS23 glioma vs metastasis (Tumor Type), RSNA-MICCAI MGMT methylation status (MGMT Methylation), and UPenn-GBM IDH1 mutation detection (IDH1 Status). Values represent AUROC and average precision (AP) in %. Best results per row in bold, second-best underlined*

![[assets/figures/papers/paper_list_l2541_https_openaccess_thecvf_com_content_CVPR2026_html_Tu_Masked_Diffusion_Au/figures/005_Figure_3.jpg]]
*Figure 3: Ablation study overview. (a) AUROC landscape over masking ratio and noise level, showing synergistic interaction between masking and noise (see §5.2 for analysis). (b) Pixel-space vs. embedding-space (EMDAE) corruption across encoder depths. (c) Convolutional (ResNet), ResNet with time conditioning, and transformer (EVA) encoder architectures*

![[assets/figures/papers/paper_list_l2541_https_openaccess_thecvf_com_content_CVPR2026_html_Tu_Masked_Diffusion_Au/figures/008_Table_4.jpg]]
*Table 4: Masking ratio ablation with*

![[assets/figures/papers/paper_list_l2541_https_openaccess_thecvf_com_content_CVPR2026_html_Tu_Masked_Diffusion_Au/figures/006_Table_5.jpg]]
*Table 5: Loss weight ablation on UCSF-PDGM. Validation performance for segmentation (Dice %) and classification (AU-ROC/AP %) with varying loss weights*

## 定位与知识库关联

### 1. 方法定位：双重损坏机制的统一框架

MDAE的核心创新在于将**空间掩码**与**扩散噪声**在像素空间同时施加，从而统一了掩码自编码器（MAE）与去噪得分匹配（DSM）两类自监督学习范式。这一设计的理论依据体现在其极限行为中：当噪声强度 $\sigma_{\max} \to 0$ 时，MDAE退化为标准MAE；当掩码概率 $p_{\mathrm{mask}} \to 0$ 时，MDAE退化为DSM。因此，MDAE并非简单的技术叠加，而是构建了一个连续的损坏-重建谱系，使模型能够在结构推理与纹理保留之间自适应权衡。

与现有方法的关键差异体现在三个维度：

| 方法维度 | 现有范式 | MDAE |
|---------|---------|------|
| **损坏机制** | 仅空间掩码（**MAE**, He et al., CVPR 2022）或仅扩散噪声（DSM） | 像素空间同时施加空间掩码与扩散噪声 |
| **掩码策略** | 固定高掩码比（如75%） | 从均匀分布 $\mathcal{U}(p_{\min}, p_{\max})$ 采样可变掩码比例 |
| **时间感知** | 标准MAE无时间条件输入 | 时间条件编码器-解码器，通过FiLM注入时间嵌入 |

双重损坏的关键优势在于**降低了对高掩码比的依赖**：传统MAE需要75%以上的掩码率才能迫使模型学习有意义的表征，而MDAE中可见区域的去噪目标本身就提供了足够的监督信号，使模型在较低掩码比下仍能获得有效的学习压力。

### 2. 与基线方法的关系

#### 2.1 相对于对比学习方法的优势

对比学习基线（**SimCLR**, Chen et al., ICML 2020; **VoCo**, Wu et al., CVPR 2024）依赖数据增强构建正负样本对，但在3D医学影像中，不恰当的增强可能破坏诊断相关的细微结构（如肿瘤边界、水肿区域）。MDAE完全避免了数据增强的敏感性，通过重建和去噪两个原生任务学习表征，在16个临床基准上始终优于对比学习方法，尤其在跨模态泛化任务上优势显著（平均AUROC 78.6%）。

#### 2.2 相对于掩码自编码器的改进

**MAE**（He et al., CVPR 2022）仅关注掩码区域的重建，可见区域的信息未被充分利用。MDAE通过引入扩散噪声，使可见区域也参与去噪学习，从而同时捕获全局解剖结构（掩码重建）和细粒度组织纹理（可见去噪）。消融实验证实，在75%掩码且 $\sigma_{\max}=1.0$ 时达到全局最优AUROC 0.658，验证了两种损坏的协同效益。

#### 2.3 相对于生成式预训练方法的定位

**Models Genesis**（Zhou et al., MICCAI 2019）通过多尺度图像恢复进行自监督学习，但其恢复任务缺乏明确的结构-纹理解耦。MDAE的双目标设计提供了更清晰的归纳偏置：掩码区域损失 $\mathcal{L}_{\mathrm{masked}}$ 强制全局推理，可见区域损失 $\mathcal{L}_{\mathrm{visible}}$ 保留局部细节。

#### 2.4 相对于多模态/基础模型的比较

在跨模态泛化场景中，MDAE与**BrainMVP**（Rui et al., CVPR 2025）、**BrainIAC**、**MRI-Core**等基础模型进行了直接对比。MDAE在无需多模态预训练数据的情况下，取得了具有竞争力的性能，表明其表征具有天然的模态不变性。

### 3. 关键设计选择的消融证据

#### 3.1 像素空间 vs. 嵌入空间损坏

像素空间损坏（MDAE）显著优于嵌入空间损坏（EMDAE），AUROC提升4.2–10.2个百分点（Figure 3b）。这表明在3D医学影像中，直接在原始信号空间施加损坏能保留更丰富的物理信息，嵌入空间的抽象反而损失了对下游任务关键的细节。

#### 3.2 块状掩码 vs. 随机体素掩码

块状掩码（$16^3$ 体素块）优于随机体素掩码（AUROC 0.623 vs. 0.600），说明结构化的空间损坏比随机丢弃更能迫使模型学习全局上下文推理。

#### 3.3 可变掩码 vs. 固定掩码

可变掩码策略（从均匀分布采样）优于所有固定掩码比例变体，取得最高平均AUROC 0.662（Table 4）。这一发现具有实用价值：模型在预训练过程中接触不同难度的损坏模式，增强了表征的鲁棒性。

#### 3.4 编码器架构选择

ResNet编码器显著优于Vision Transformer，AUROC提升12.1–13.8个百分点（Figure 3c）。这一结果与自然图像领域的趋势相反，提示3D医学影像的局部纹理特征可能更适合卷积归纳偏置，Transformer的全局自注意力在小规模医学数据集上可能引入过拟合风险。

#### 3.5 噪声调度选择

VE、VP与Flow Matching噪声调度表现几乎一致（VE: 0.615, Flow Matching: 0.614, VP: 0.613 AUROC），表明MDAE框架对噪声调度类型不敏感，具有良好的鲁棒性。

### 4. 适用边界与局限

#### 4.1 已验证的适用场景

- **模态**：脑部MRI（T1、T2、FLAIR、T1GD、ASL、SWI等多序列）
- **任务类型**：肿瘤分类（胶质瘤分级、IDH突变、MGMT甲基化）、分割、生存预测
- **数据规模**：基于Open-Mind数据集（114,570个3D脑MRI体积，来自34,191名受试者）预训练

#### 4.2 已知局限

**本文仅聚焦于脑部MRI，在不同器官（如肺、肝脏、前列腺）和不同模态（如CT、超声）上的泛化性尚未验证。** 3D医学影像的解剖结构和成像物理特性在不同部位差异显著，MDAE的双重损坏策略是否能直接迁移至其他解剖区域，需要进一步实验验证。

#### 4.3 公平性考量

实验使用公开数据集Open-Mind，采用分层划分（stratified splits）确保可复现评测，但**未进行人口学（种族、性别、年龄）或设备（不同MRI扫描仪、场强）相关的公平性分析**。在临床部署前，需要评估模型在不同亚群上的性能差异。

### 5. 开放问题

#### 5.1 生成式预训练目标的融合

如何将生成式预训练目标有效融入3D医学视觉自监督学习仍是一个有待探索的问题。MDAE目前采用判别式重建目标（MSE损失），未来可探索将扩散模型本身的生成能力（如条件采样、图像修复）整合到表征学习框架中，实现“表征-生成”一体化。

#### 5.2 跨器官/跨模态迁移

MDAE在脑部MRI上的成功是否可复制到其他解剖部位（腹部、胸部）和成像模态（CT、PET），需要系统性的迁移学习研究。不同模态的噪声特性和解剖结构差异可能要求调整损坏策略的超参数。

#### 5.3 掩码策略的自适应优化

当前可变掩码策略采用固定的均匀分布，未来可探索基于图像内容的自适应掩码策略——例如，对解剖结构复杂区域施加更高掩码比，对均匀组织区域降低掩码比——以进一步提升表征质量。

#### 5.4 与视觉-语言模型的对齐

随着医学视觉-语言模型的发展，MDAE学到的结构-纹理解耦表征是否能与放射学报告等文本信息自然对齐，为多模态医学AI提供更丰富的表征基础，是一个值得探索的方向。

## 原文 PDF

![[paperPDFs/CVPR_2026/Masked_Diffusion_Autoencoders_for_3D_Medical_Vision_Representation_Learning.pdf]]
