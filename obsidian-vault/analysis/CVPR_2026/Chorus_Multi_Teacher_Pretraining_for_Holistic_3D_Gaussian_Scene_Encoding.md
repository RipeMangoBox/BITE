---
title: "Chorus: Multi-Teacher Pretraining for Holistic 3D Gaussian Scene Encoding"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/Chorus_Multi_Teacher_Pretraining_for_Holistic_3D_Gaussian_Scene_Encoding.pdf
project_link: null
code_link: null
huggingface_link: "https://huggingface.co/datasets/spatialverse/InteriorGS"
aliases:
- Chorus
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
core_operator: 利用多个互补的2D基础模型教师（语言对齐、通用视觉、物体感知）进行联合蒸馏，通过共享编码器加轻量投影头将多样化知识压缩到统一嵌入空间。
primary_logic: 互补的2D基础模型特征可以通过多教师蒸馏注入3DGS编码器，生成高度结构化且数据高效的场景表示，同表示既能处理3D高斯输入，也能迁移到点云任务。
claims:
- 在ScanNet200、Matterport3D等多个基准上，Chorus的零样本语义分割性能显著超越前代最佳方法SceneSplat（例如ScanNet200 f-mIoU +2.1%）。
- 仅使用点云变体（中心/颜色/法线），Chorus在语义分割线性探测中超越自监督基线Sonata（ScanNet200 36.0 vs. 28.8 mIoU），且所需预训练场景少约39.9倍。
- 教师消融实验证明，在语言教师基础上添加通用视觉（DINO）和物体感知（PE）教师，零样本语义分割指标持续提升（ScanNet++ v2 f-mIoU从27.1升至29.6）。
- 渲染式适配策略在InteriorGS数据集上仅用100个场景即可提升+2.7% mIoU（线性探测），且避免约1 TB的预计算存储开销。
---

# Chorus: Multi-Teacher Pretraining for Holistic 3D Gaussian Scene Encoding

> [!tip] 核心洞察
> 互补的2D基础模型特征可以通过多教师蒸馏注入3DGS编码器，生成高度结构化且数据高效的场景表示，同表示既能处理3D高斯输入，也能迁移到点云任务。

| 字段 | 内容 |
|------|------|
| 中文题名 | Chorus：面向全息3D高斯场景编码的多教师预训练框架 |
| 英文题名 | Chorus: Multi-Teacher Pretraining for Holistic 3D Gaussian Scene Encoding |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2512.17817) · [HuggingFace](https://huggingface.co/datasets/spatialverse/InteriorGS) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction |
| Method | Chorus |
| Dataset | ScanNet200, Matterport3D, ScanNet, InteriorGS |

> [!tip] 效果简介
> - ScanNet200 (零样本语义分割) 上，f-mIoU 24.6 vs 22.5 (SceneSplat) (+2.1)。
> - Matterport3D (零样本语义分割) 上，f-mIoU 18.7 vs 14.0 (SceneSplat) (+4.7)。
> - ScanNet200 (零样本实例分割) 上，mAP 19.6 vs 17.8 (Mosaic3D) (+1.8 (+7.6尾类))。

## 概述

3D高斯泼溅（3DGS）已成为高质量场景重建的核心表示，然而现有3DGS场景编码器仅依赖单一教师信号（如语义对齐），无法获取实例分组和精细空间结构信息，导致特征表示不够全面，跨任务迁移能力弱。**Chorus** 提出了一种多教师预训练框架，利用互补的2D基础模型教师——语言对齐（SigLIP2）、通用视觉（DINOv3）与物体感知（PE-Spatial）——进行联合蒸馏，通过共享编码器加轻量投影头将多样化知识压缩到统一嵌入空间。

核心洞察在于：互补的2D基础模型特征可以通过多教师蒸馏注入3DGS编码器，生成高度结构化且数据高效的场景表示，同一表示既能处理3D高斯输入，也能迁移到点云任务。

**主要结果**：

- **零样本语义分割**：在ScanNet200上f-mIoU达24.6（SceneSplat为22.5，+2.1%），Matterport3D上达18.7（+4.7%）。
- **开放词汇实例分割**：仅用3D输入即取得最高mAP 19.6，尾类mAP达13.0（此前最佳仅5.4，+7.6）。
- **点云变体线性探测**：ScanNet200 mIoU 36.0，超越自监督基线Sonata（28.8），且所需预训练场景减少约39.9倍。
- **数据效率**：在ScanNet数据效率基准上，使用1%训练场景时mIoU达42.0，20%时反超Sonata（71.3 vs. 69.8）。
- **域外适配**：渲染式适配策略在InteriorGS数据集上仅用100个场景即提升+2.7% mIoU，且避免约1 TB的预计算存储开销。

**方法定位**：Chorus继承并扩展了SceneSplat的“上提-对齐”范式，将单一语言教师扩展为多教师蒸馏体系，同时引入3DGS感知的数据增强和在线渲染-蒸馏适配策略，在3DGS场景编码与点云预训练之间架起桥梁。

## 背景与动机

### 3D场景表示从点云到3D高斯的演进

三维场景理解长期依赖点云作为主要表示形式。点云方法通过自监督预训练或2D视觉-语言模型蒸馏来获取逐点特征，代表性工作包括**OpenScene**（Peng et al., CVPR 2023）、**RegionPLC**（Yang et al., ECCV 2024）和**Sonata**（Zuo et al., CVPR 2025）。然而，点云本身受限于稀疏性和缺乏显式几何结构，难以捕捉精细的表面细节和语义边界。

3D高斯泼溅（3D Gaussian Splatting, 3DGS）作为一种新兴场景表示，以显式高斯原语集 $\mathcal{G} = \{ ( \mathbf{x}_i, \mathbf{s}_i, \mathbf{q}_i, \alpha_i, \mathbf{c}_i ) \}_{i=1}^N$ 描述场景，每个高斯携带中心位置、尺度、旋转四元数、不透明度和颜色参数。通过alpha合成渲染方程，3DGS能以高保真度从任意视点渲染图像，同时其原生参数集蕴含丰富的几何与外观先验。这为构建场景编码器提供了更丰富的信息源，但也带来了新的挑战：如何有效利用这些结构化参数进行语义级场景理解。

### 现有3DGS编码器的单一教师瓶颈

当前最先进的3DGS场景编码器**SceneSplat**（Peng et al., arXiv 2024）采用“上提-对齐”（lift-then-align）范式：先将2D教师特征通过渲染权重上提到3D高斯，再训练编码器对齐这些伪标签。这一范式验证了3DGS编码器的可行性，但存在根本性局限——**仅依赖单一语言对齐教师**（如SigLIP）。

单一教师信号的缺陷体现在三个层面：

1. **语义粒度受限**：语言对齐特征擅长粗粒度语义（区分“椅子”与“桌子”），但难以捕捉精细的视觉结构（椅腿、扶手等部件）和实例级区分（同一类别的不同实例）。
2. **物体感知缺失**：语言教师缺乏显式的物体边界和分组信息，导致编码特征在物体边界处模糊，不利于下游的实例分割和物体级推理。
3. **跨任务迁移能力弱**：仅从语言信号蒸馏的特征表示，在需要细粒度几何理解的任务（如开放词汇实例分割的尾类识别）上表现不足。

### 互补2D基础模型提供未被利用的知识源

近年来，2D基础模型在多个维度上取得了突破性进展，形成了互补的知识体系：

- **通用视觉模型**（如DINOv3）：通过自监督训练学习到强健的视觉结构表示，其注意力图自然涌现出物体边界和部件分割能力，无需任何标注即可捕捉精细空间结构。
- **物体感知模型**（如PE-Spatial）：专门针对实例级和物体级理解设计，输出与物体身份和分组相关的特征，补充语言模型缺失的实例区分能力。

这些模型各自编码了场景理解的不同侧面，但它们的知识此前未被系统性地注入3DGS编码器。核心洞察在于：**这些互补的2D基础模型特征可以通过多教师蒸馏，注入统一的3DGS编码器，生成高度结构化且数据高效的场景表示**。

### 预计算瓶颈与域外适应困境

现有蒸馏方法（包括SceneSplat）面临严重的实用瓶颈：需要在训练前离线预计算所有场景的2D教师伪标签，并存储为3D特征文件。对于大规模场景集合，这一过程产生约**1 TB的存储开销**，且在新场景上部署时需重复整个预计算流程，极大限制了方法的可扩展性和实际部署效率。

### Chorus的核心动机

针对上述缺口，Chorus提出三个核心设计目标：

1. **多教师联合蒸馏**：利用语言对齐（SigLIP2）、通用视觉（DINOv3）和物体感知（PE-Spatial）三个互补教师，通过共享编码器加轻量投影头将多样化知识压缩到统一嵌入空间。
2. **全息场景表示**：生成的嵌入同时编码语义、几何和实例信息，使得同一表示既能处理3D高斯输入，也能迁移到点云任务，实现跨模态泛化。
3. **轻量化域外适应**：通过在线渲染-蒸馏（render-and-distill）策略，利用3DGS固有的渲染能力，在适配阶段完全避免离线预计算，将存储需求从TB级降至GB级，同时保持竞争力。

这些设计使Chorus在显著更少的预训练场景下（相较Sonata减少约39.9倍），仍能在零样本语义分割、开放词汇实例分割和场景问答等多个任务上取得领先性能。

## 核心创新

Chorus 的核心创新在于将 3DGS 场景编码从**单一教师蒸馏**范式升级为**多教师联合蒸馏**范式，并通过一系列配套设计实现了更全面、更高效、更可迁移的场景表示。

### 1. 从单一教师到多教师互补蒸馏

前代方法 **SceneSplat** 仅蒸馏语言对齐信号（如 SigLIP），导致编码器学到的特征缺乏实例分辨能力和精细空间结构信息。Chorus 将教师信号源从单一语言教师扩展为三类互补的 2D 基础模型教师：

| 教师信号 | 基础模型 | 提供的知识维度 |
|----------|----------|----------------|
| 语言对齐语义 | SigLIP2 | 开放词汇语义对齐 |
| 通用视觉特征 | DINOv3 | 通用视觉模式与结构感知 |
| 物体感知线索 | PE-Spatial | 实例/物体级别的分组与边界感知 |

**因果机制**：三类教师提供互补的监督信号——语言教师赋予特征语义可解释性，通用视觉教师注入稠密的视觉结构信息，物体感知教师提供实例级别的分组先验。通过共享 3DGS 编码器 $g_{\theta}$ 加轻量级每教师投影头 $h_t$ 的架构，这些异构知识被压缩到统一的潜在嵌入空间 $Z = g_{\theta}(\mathcal{G}) \in \mathbb{R}^{N \times d_z}$ 中，避免了多分支独立训练可能带来的特征割裂。

**证据强度**：教师消融实验（Table 9）在 ScanNet++ v2 上验证了这一设计的有效性——在语言教师基础上逐步添加 DINO 和 PE-Spatial 教师，零样本语义分割 f-mIoU 从 27.1 单调提升至 29.4 再到 29.6，证明多教师信号确实产生了互补增益而非相互干扰。

### 2. 渲染式域外适配：从离线预计算到在线蒸馏

传统 3DGS 编码器在适配新场景时，需要**离线预计算 3D 伪标签**——将 2D 教师特征通过渲染权重上提到 3D 高斯，并存储为磁盘文件。对于 800 个训练场景，这一过程产生约 **1 TB 的存储开销**（Table 7）。

Chorus 提出 **render-and-distill** 适配策略，核心思路是：

1. **在线渲染**：利用 3DGS 原生的可微分渲染能力，在训练时实时渲染多视角 2D 特征图 $\hat{F}_{p,\mathbf{u}}^{(t)}$。
2. **图像级监督**：直接在 2D 域计算渲染特征图与教师特征图之间的匹配损失 $\mathcal{L}_{\mathrm{img}}^{(t)}$，无需中间 3D 伪标签存储。
3. **轻量实现**：每视图仅增加约 0.1 秒的特征光栅化开销。

这一设计将适配存储需求从 **1080 GB 降至 8 GB**（Table 7），同时仅用 100 个 InteriorGS 场景即可在线性探测下带来 **+2.7% mIoU** 的提升（Figure 6）。

### 3. 3DGS 感知的数据增强

Chorus 提出了两种专为 3DGS 表示设计的数据增强策略，区别于通用点云增强（如 dropout、弹性形变）：

- **渲染等效扰动（Rendering-Equivalent Perturbation）**：在高斯中心添加协方差感知的位置噪声，使得扰动后的高斯参数渲染出近似相同的图像，迫使编码器学习对渲染外观不敏感的结构特征。
- **不成熟流形扰动（Immature-Manifold Perturbation）**：膨胀高斯的尺度参数，模拟 3DGS 优化早期阶段的不成熟几何状态，提升编码器对欠优化场景的鲁棒性。

**因果机制**：3DGS 参数空间存在大量“渲染等效”的自由度——不同参数组合可以渲染出几乎相同的图像。通用点云增强无法利用这一结构特性，而 Chorus 的增强策略直接在参数空间施加物理上有意义的扰动，使编码器学会区分“影响渲染”与“不影响渲染”的参数变化，从而提取更本质的场景结构。

**证据强度**：设计选择消融（Figure 8）显示，3DGS 感知增强带来了可测量的性能增益；Table 10 进一步验证了 Chorus 对 3DGS 优化程度和密度变化的鲁棒性显著优于基线。

### 4. 点云兼容性与数据效率

Chorus 的另一个关键创新是其**点云变体**：仅使用高斯中心、颜色和估计法线作为输入，舍弃尺度、旋转和不透明度等 3DGS 特有参数。这使得同一个预训练框架产出的表示既能处理 3DGS 输入，也能直接应用于点云任务。

这一设计的意义在于：
- **公平对比**：点云变体与自监督点云基线 **Sonata** 使用完全相同的输入模态，但 Chorus 在 ScanNet200 语义分割线性探测中达到 **36.0 mIoU**，显著超越 Sonata 的 28.8 mIoU（Table 4）。
- **极高数据效率**：Chorus 仅使用约 **39.9 倍更少**的预训练场景就取得了更优性能，证明多教师蒸馏学到的表示具有极强的泛化能力，不依赖海量预训练数据。

---

**总结**：Chorus 的核心创新可归纳为三个 changed slots——（1）教师信号从单一语言对齐扩展为语言+通用视觉+物体感知的多教师互补蒸馏；（2）域外适应从离线预计算伪标签转变为在线渲染蒸馏；（3）数据增强从通用点云扰动升级为 3DGS 参数空间感知的扰动。这三项创新共同实现了更结构化、更数据高效、跨模态可迁移的 3D 场景表示。

## 整体框架

Chorus 构建了一个“上提-对齐”（lift-then-align）的多教师预训练框架，其核心目标是将互补的 2D 基础模型知识蒸馏到统一的 3D 高斯场景编码器中。整个 pipeline 由三个关键阶段串联而成：**多教师预训练**、**渲染式适配**与**任务特定迁移**（Figure 2）。

![[assets/figures/papers/paper_list_l2077_https_arxiv_org_abs_2512_17817/figures/002_Figure_2.jpg]]
*Figure 2: Chorus Overview. (a) Multi-Teacher Pretraining. We train a feed-forward 3DGS scene encoder to distill complementary signals–language-aligned (SigLIP), generalist (DINO), and object-aware (PE)–from 2D teachers. This knowledge is transferred into a shared embedding space via lightweight per-teacher projectors and losses. To accelerate out-of-domain adaptation, we support finetuning the encoder with online rendering-based supervision. (b) Task-Specific Transfer. A pretrained Chorus encoder enables diverse downstream tasks, including semantic and instance segmentation, open-vocabulary query, and 3D visual question answering (VQA)*

### 输入：3DGS 场景参数集

框架的输入是一个优化后的 3DGS 场景，由 $N$ 个高斯原语组成：
$$\mathcal{G} = \{ ( \mathbf{x}_i, \mathbf{s}_i, \mathbf{q}_i, \alpha_i, \mathbf{c}_i ) \}_{i=1}^N$$
其中 $\mathbf{x}_i$ 为中心位置，$\mathbf{s}_i$ 为尺度，$\mathbf{q}_i$ 为旋转四元数，$\alpha_i$ 为不透明度，$\mathbf{c}_i$ 为颜色（Eq. 1）。3DGS 的渲染方程（Eq. 2）通过深度排序的 alpha 合成，为任意视点 $p$ 和像素 $\mathbf{u}$ 生成颜色 $\mathbf{C}(\mathbf{u}|p)$，并产生每个高斯的渲染权重 $w_i(p,\mathbf{u})$。

### 阶段一：多教师预训练

**教师信号提取与标准化。** 对每个训练场景，首先通过视图采样与配对策略（Figure 3）选择空间覆盖广、重叠高的视点对。对每个选定视点，利用三个互补的 2D 基础模型教师提取特征图：
- **SigLIP2**：提供语言对齐的语义特征；
- **DINOv3**：提供通用视觉特征；
- **PE-Spatial**：提供物体感知（object-aware）特征。

随后，利用归一化的渲染权重 $\bar{w}_i(p,\mathbf{u})$ 将 2D 教师特征“上提”到每个 3D 高斯上（Eq. 3），形成逐高斯的教师目标特征 $\widetilde{f}_i^{(t)}$。为平衡不同教师特征的方差差异，所有教师特征在进入蒸馏前均经过 **PHI-S 标准化**——先进行 PCA 旋转，再进行各向同性的 Hadamard 缩放，使每个通道达到单位平均方差。

**共享编码器与投影头。** 框架的核心是一个共享的 3DGS 编码器 $g_{\theta}$，它将高斯参数映射为逐高斯的潜在特征：
$$Z = g_{\theta}(\mathcal{G}) \in \mathbb{R}^{N \times d_z}$$
每个教师 $t \in \mathcal{T}$ 配备一个轻量的投影头 $h_t$（2 层 MLP + LayerNorm + GELU），将共享潜在特征投影到对应教师的特征空间，得到预测特征 $\hat{f}_i^{(t)}$。

**蒸馏损失。** 预训练损失由两部分组成：
- **匹配损失** $\mathcal{L}_{\mathrm{match}}^{(t)}$（Eq. 5）：结合余弦相似度损失和平滑 L1 损失，同时对特征方向和幅度进行监督；
- **教师特定对比损失** $\mathcal{L}_{\mathrm{con}}^{(t)}$：对语义/实例组使用 InfoNCE 对比正则，增强类内紧凑性和类间可分性。

总预训练目标（Eq. 6）对当前激活的教师集合 $\mathcal{A}(e)$ 加权求和，支持分阶段引入教师（如先训练语言教师，再逐步加入 DINO 和 PE-Spatial），避免教师间干扰。

**3DGS 感知数据增强。** 预训练中引入两种专为 3DGS 设计的数据增强：
- **渲染等效扰动**：对高斯参数施加协方差感知的位置噪声，使得增强后的参数仍能渲染出近似相同的图像；
- **不成熟流形扰动**：膨胀高斯的尺度，模拟优化早期的不成熟几何。

### 阶段二：渲染式适配

为将预训练模型快速迁移到新场景域（如 InteriorGS），Chorus 提出 **render-and-distill** 策略，完全避免离线预计算 3D 伪标签所需的约 1 TB 存储开销。适配过程利用 3DGS 的原生渲染能力，在线渲染视点并将编码器预测的逐高斯特征通过渲染权重投影回 2D 特征图（Eq. 7），在有效像素上与教师 2D 特征图计算图像级匹配损失（Eq. 8）。该过程仅需 100 个适配场景即可带来 +2.7% mIoU 的线性探测增益，且每次渲染仅增加约 0.1 秒的延迟。

### 阶段三：任务特定迁移

预训练完成后，共享编码器的输出 $Z$ 可直接作为下游任务的场景表示。对于语义/实例分割，可在冻结特征上训练线性分类器（线性探测）或进行全微调；对于 3D 视觉问答，仅将编码器最后一阶段的特征馈入视觉语言模型，替代多层级特征。框架同时提供标准 3DGS 变体（使用全部高斯参数）和点云兼容变体（仅使用中心、颜色和估计法线），后者可直接处理点云输入，实现跨表示迁移。

### 模块关系总结

整个框架的数据流为：**3DGS 场景 → 共享编码器 → 潜在特征 → 投影头 → 教师匹配**。多教师信号通过共享主干进行知识融合，PHI-S 标准化和分阶段训练策略抑制教师间干扰，渲染式适配实现轻量化域外扩展，最终生成高度结构化且数据高效的全息场景表示。

### 补充图表

![[assets/figures/papers/paper_list_l2077_https_arxiv_org_abs_2512_17817/figures/001_Figure_1.jpg]]
*Figure 1: Chorus Framework. (a) Multi-Teacher Pretraining. A feed-forward 3DGS scene encoder with per-teacher projectors distills complementary signals—language-aligned, generalist, and object-aware—into a shared embedding. (b) Example Feature PCA (results on novel scenes). At inference we input the full 3DGS scene; PCA on encoder features presents clear semantic awareness despite domain shift. (c) Evaluation & Data Efficiency. Chorus attains strong results across scene understanding tasks while using noticeably fewer training scenes—8.32× and 39.9× less than the SoTA point-cloud pretraining baselines—highlighting the efficiency of our pretraining*

![[assets/figures/papers/paper_list_l2077_https_arxiv_org_abs_2512_17817/figures/003_Figure_3.jpg]]
*Figure 3: Rendering-Based View Sampling and Pairing: (a) Camera Location Sampling: We use Furthest Point Sampling to select camera positions that achieve broad spatial coverage across the entire navigable scene space. (b) Visibility Culling: For each location, we sample view angles and track the visibility of the 3D Gaussians across frames. (c) View Pairing and Selection: We obtain a minimum 2D bounding box covering all visible Gaussians for a given view. Candidate pairs of poses are then calculated and sorted based on the overlap score. (d,e,f) Rendered images corresponding to the colored camera viewpoints*

## 核心模块与公式推导

### 3DGS场景参数化与渲染

Chorus的输入是一个经过优化的3D高斯泼溅场景，由 $N$ 个高斯原语组成。每个高斯 $i$ 的参数集定义为：

$$\mathcal{G} = \{ ( \mathbf{x}_i, \mathbf{s}_i, \mathbf{q}_i, \alpha_i, \mathbf{c}_i ) \}_{i=1}^N$$

其中 $\mathbf{x}_i \in \mathbb{R}^3$ 为高斯中心位置，$\mathbf{s}_i \in \mathbb{R}^3$ 为各向异性尺度，$\mathbf{q}_i \in \mathbb{R}^4$ 为旋转四元数，$\alpha_i \in \mathbb{R}$ 为不透明度，$\mathbf{c}_i \in \mathbb{R}^3$ 为颜色（由球谐系数编码）。这些参数构成了编码器的完整输入。

3DGS的渲染过程通过深度排序的alpha合成实现。对于给定视点 $p$ 和像素坐标 $\mathbf{u}$，渲染颜色由下式给出：

$$\mathbf{C}(\mathbf{u}|p) = \sum_{i \in \mathcal{S}_{d,\mathbf{u}}} w_i(p,\mathbf{u}) \mathbf{c}_i, \quad w_i(p,\mathbf{u}) = T_i \alpha_i(\mathbf{u}|p), \quad T_i = \prod_{j<i}(1-\alpha_j(\mathbf{u}|p))$$

其中 $w_i(p,\mathbf{u})$ 为渲染权重，$T_i$ 为累积透射率。这一渲染机制在Chorus中被双重利用：预训练阶段用于将2D教师特征上提到3D高斯，适配阶段则通过在线渲染投影回2D进行监督。

### 教师特征上提

为了获得每个高斯的监督信号，Chorus采用归一化特征上提策略。给定一个视点-像素对 $(p,\mathbf{u})$ 和对应的高斯集合 $S_i$，2D教师特征 $F_{p,\mathbf{u}}$ 通过归一化渲染权重分配到3D高斯：

$$f_i = \sum_{(p,\mathbf{u})\in S_i} \bar{w}_i(p,\mathbf{u}) F_{p,\mathbf{u}}, \quad \bar{w}_i(p,\mathbf{u}) = \frac{w_i(p,\mathbf{u})}{\sum_{(p',\mathbf{u}')\in S_i} w_i(p',\mathbf{u}')}$$

这种归一化保证了每个高斯获得的多视图特征贡献是加权平均，避免了因不同视角下可见性差异导致的特征尺度不一致。

### 共享编码器与投影头

Chorus的核心设计是一个共享的3DGS编码器 $g_{\theta}$，它将高斯参数集直接映射为逐高斯的潜在特征：

$$Z = g_{\theta}(\mathcal{G}) \in \mathbb{R}^{N \times d_z}$$

其中 $d_z$ 为潜在特征维度。该编码器采用前馈架构，一次前向传播即可为场景中所有高斯生成嵌入。这种设计的关键优势在于：所有教师信号通过同一个主干网络进行压缩，避免了独立分支间的特征干扰（消融实验证实单主干+投影头优于独立分支设计）。

对于每个教师 $t \in \mathcal{T}$（包括SigLIP2语言对齐教师、DINOv3通用视觉教师、PE-Spatial物体感知教师），Chorus配备一个轻量级投影头 $h_t$——由2层MLP加LayerNorm和GELU激活组成——将共享潜在特征投影到对应教师的特征空间。在投影之前，教师特征经过PHI-S标准化处理：先进行PCA旋转，再施加各向同性Hadamard缩放，使得每个通道具有单位平均方差，同时保留通道间关系。

### 匹配损失与对比正则

每个教师的逐高斯匹配损失结合了余弦相似度损失和平滑L1损失：

$$\mathcal{L}_{\mathrm{match}}^{(t)} = \frac{1}{|\mathcal{M}^{(t)}|} \sum_{i\in\mathcal{M}^{(t)}} \lambda_1(1-\cos(\hat{f}_i^{(t)},\widetilde{f}_i^{(t)})) + \lambda_2 \mathrm{SmoothL1}(\hat{f}_i^{(t)},\widetilde{f}_i^{(t)})$$

其中 $\hat{f}_i^{(t)} = h_t(z_i)$ 为编码器预测特征，$\widetilde{f}_i^{(t)}$ 为上提的教师伪标签特征，$\mathcal{M}^{(t)}$ 为有效匹配的高斯集合。余弦项保持方向一致性，SmoothL1项约束幅度匹配——消融实验表明两者结合优于单独使用任一项。

对于语义教师和物体感知教师，Chorus额外引入教师特定的对比损失 $\mathcal{L}_{\mathrm{con}}^{(t)}$，基于语义类别或实例分组构建InfoNCE形式的对比正则，增强嵌入空间的判别性。

### 总预训练目标与分阶段训练

总预训练损失对当前激活的教师进行加权求和：

$$\mathcal{L}_{\mathrm{total}}(e) = \sum_{t \in \mathcal{A}(e)} \lambda_t \big( \mathcal{L}_{\mathrm{match}}^{(t)} + \eta_t \mathcal{L}_{\mathrm{con}}^{(t)} \big)$$

其中 $\mathcal{A}(e)$ 为训练阶段 $e$ 激活的教师集合。Chorus采用分阶段训练策略：先以语言教师为主进行基础对齐，随后逐步引入通用视觉教师和物体感知教师。教师消融实验（Table 9）证实，在语言教师基础上逐步添加DINO和PE-Spatial教师，零样本语义分割指标单调提升（ScanNet++ v2 f-mIoU从27.1升至29.4再升至29.6），验证了多教师互补蒸馏的有效性。

### 渲染式适配损失

对于域外场景的轻量化适配，Chorus将编码器预测的逐高斯特征通过渲染权重投影回2D特征图：

$$\hat{F}_{p,\mathbf{u}}^{(t)} = \sum_{i \in S_{p,\mathbf{u}}} w_i(p,\mathbf{u}) \hat{f}_i^{(t)}$$

然后在有效像素区域 $\Omega$ 上计算图像级匹配损失：

$$\mathcal{L}_{\mathrm{img}}^{(t)} = \frac{1}{|\Omega|} \sum_{(p,\mathbf{u})\in\Omega} \ell_{\mathrm{match}}( \hat{F}_{p,\mathbf{u}}^{(t)}, \widetilde{F}_{p,\mathbf{u}}^{(t)} )$$

这一设计的关键价值在于：避免了传统方法中约1 TB的3D伪标签预计算存储开销（Table 7显示存储从1080 GB降至8 GB），同时将适配延迟控制在每视图0.1秒以内。消融实验（Figure 5）表明，即使使用30×40的低分辨率DINOv3特征，也能产生明显的性能改善。

## 实验与分析

### 核心瓶颈与实验设计逻辑

现有3DGS场景编码器仅依赖单一教师信号（如语义对齐），无法获取实例分组和精细空间结构信息，导致特征表示不够全面，跨任务迁移能力弱。Chorus通过利用多个互补的2D基础模型教师（语言对齐、通用视觉、物体感知）进行联合蒸馏，将多样化知识压缩到统一嵌入空间，从而生成高度结构化且数据高效的场景表示。实验设计围绕三个核心问题展开：（1）多教师蒸馏是否带来一致的性能增益？（2）生成的表示是否具备跨任务、跨模态、跨数据域的泛化能力？（3）各设计组件的贡献如何？

### 零样本语义分割：主结果

Table 1展示了Chorus在四个基准上的零样本3D语义分割性能。在细粒度ScanNet200（200类）上，Chorus联合训练后达到**24.6 f-mIoU**，较前代最佳3DGS编码器SceneSplat（22.5）提升**+2.1%**，f-mAcc提升**+6.0%**。在Matterport3D（160类）上，优势更为显著：Chorus取得**18.7 f-mIoU**，超出SceneSplat（14.0）**+4.7%**。在ScanNet++ v2（100类）和InteriorGS（72类）上，Chorus同样保持领先。值得注意的是，Chorus和SceneSplat均以3DGS为输入，而其他方法依赖点云或多视图图像，Chorus在仅使用前馈3D编码的情况下即取得最优，验证了多教师蒸馏的有效性。

### 开放词汇实例分割

Table 2报告了ScanNet200上的开放词汇3D实例分割结果。Chorus（仅3D输入）取得**19.6 mAP**，超越此前最佳的Mosaic3D（17.8）。关键突破在于尾类（tail classes，共66类）性能：Chorus尾类mAP达**13.0**，而此前最佳方法仅5.4，提升**+7.6 mAP**。这表明物体感知教师（PE-Spatial）注入的实例级知识显著增强了对罕见类别的识别能力。需要指出的是，实例分割评估使用Mask3D作为区域建议网络，Chorus仅提供逐点特征，与使用多视图2D特征的方法相比，Chorus以更低成本实现了更强的尾类泛化。

### 线性探测与微调：表示质量验证

Table 4展示了语义分割的线性探测和微调实验，这是评估预训练表示质量的标准范式。Chorus点云变体（仅使用中心/颜色/法线）在ScanNet200上线性探测达到**36.0 mIoU**，大幅超越自监督基线Sonata（28.8），提升**+7.2%**。更关键的是，Chorus所需预训练场景数量仅为Sonata的约**1/39.9**（约1000 vs 约39900），展示了极强的数据效率。在ScanNet和Matterport3D上，Chorus点云变体同样在更少预训练数据下取得有竞争力的性能。

Table 5的ScanNet数据效率基准进一步验证了这一优势。在1%训练场景下，Chorus线性探测mIoU为42.0，略低于Sonata的45.3（-3.3）；但当数据量增至20%时，Chorus反超至**71.3 vs 69.8**，表明多教师特征在小样本下已包含丰富语义，随微调数据增加可充分释放潜力。

### 渲染式适配：轻量化域外迁移

Chorus提出的渲染-蒸馏（render-and-distill）适配策略解决了域外场景的预计算存储瓶颈。Table 7对比了传统上提（uplifting）与渲染式适配的资源开销：上提方法需约**1080 GB**存储预计算特征，而渲染式适配仅需**8 GB**，且训练时每视图仅增加0.1秒的特征光栅化开销。Figure 6显示，在InteriorGS上仅用100个适配场景即可带来**+2.7% mIoU**的线性探测增益。Figure 5的消融表明，即使使用30×40的低分辨率DINOv3特征也能产生明显改善，提升教师特征分辨率和增加适配场景数量可进一步提高性能。

### 教师消融：多教师互补性验证

Table 9的教师消融实验在ScanNet++ v2上系统验证了多教师设计的必要性。基线仅使用语言教师（SigLIP2）时f-mIoU为27.1；加入通用视觉教师（DINOv3）后升至**29.4**（+2.3）；进一步加入物体感知教师（PE-Spatial）达到**29.6**（+0.2）。单调递增的趋势证明三类教师信号互补：语言教师提供语义锚定，通用视觉教师增强细粒度结构，物体感知教师注入实例边界意识。

### 设计选择消融

Figure 8展示了关键设计组件的消融结果。SmoothL1损失（补充余弦损失的幅度信息）、3DGS感知增强（渲染等效扰动与不成熟流形扰动）、阶段性引入PE-Spatial教师、以及实例级对比损失各自带来增量收益。PHI-S教师标准化和多教师共享主干的设计避免了教师间干扰——实验表明单主干+投影头的效果优于独立分支，验证了共享表示空间的有效性。

### 3D场景问答

Table 3展示了Chorus特征在3D场景问答任务上的迁移能力。在ScanQA和Nr3D两个基准上，仅使用Chorus编码器的最终阶段特征（替换多层级特征）即可取得有竞争力的表现，表明多教师蒸馏产生的特征已包含高层语义信息，可直接服务于视觉语言模型。

### 鲁棒性分析

Table 8的实例检索实验评估了特征对点云扰动的鲁棒性。在ScanNet++验证集的684个实例上，Chorus在多种扰动（高斯噪声、下采样、旋转）下均保持最高的检索精度，验证了3DGS感知增强策略的有效性。Table 10和Table 11分别展示了Chorus对3DGS优化程度和iPhone RGB-D采集质量的鲁棒性，进一步证明其在实际部署场景中的稳定性。

### 失败模式与局限

尽管Chorus在多数任务上表现优异，仍存在以下局限：（1）预训练阶段仍需离线预计算教师伪标签，虽适配阶段通过在线渲染大幅降低了存储，但预计算的离线和存储资源需求仍不可忽视；（2）3DGS编码器的泛化能力依赖训练场景多样性，点云变体虽有效但仍需3DGS作为预训练载体；（3）当前未探索更轻量的教师模型或更高效的特征上采样策略来进一步降低适配延迟。这些方向值得后续工作深入探索。

### 补充图表

![[assets/figures/papers/paper_list_l2077_https_arxiv_org_abs_2512_17817/figures/005_Table_1.jpg]]
*Table 1: Zero-Shot 3D Semantic Segmentation on the Fine-Grained ScanNet++ (100 classes) [69], Matterport3D (160 classes) [9], ScanNet200 (200 classes) [12], and InteriorGS (72 classes) [56] Benchmarks. ✾ denotes 3DGS modality input. Chorus and SceneSplat [32] are the only methods that target 3DGS modality pretraining. We report the foreground mean IoU (f-mIoU) and foreground mean accuracy (f-mAcc) excluding the wall, floor, and ceiling classes, following [42, 68]. † denotes the official checkpoint and the baseline results are partly taken from [31]. Dataset abbreviations SN, SN++, ARKitS, MP3D, and S3D are short for ScanNet [12], ScanNet++ [69], ARKitScenes [5], Matterport3D [9], and Structured3D [7...*

![[assets/figures/papers/paper_list_l2077_https_arxiv_org_abs_2512_17817/figures/006_Table_2.jpg]]
*Table 2: Open-Vocabulary 3D Instance Segmentation on Scan-Net200. Methods are grouped by input type. Methods using both 3D+2D inputs require expensive multi-view image processing, whereas Chorus is feed-forward and shows strong performance, especially on the 66 tail classes*

![[assets/figures/papers/paper_list_l2077_https_arxiv_org_abs_2512_17817/figures/010_Table_4.jpg]]
*Table 4: Semantic Segmentation Probing & Finetuning Experiments. Chorus point-cloud variant • is used for ScanNet, ScanNet++, and Matterport3D, whereas the 3DGS-input model ✾ is used for InteriorGS, whose source data are of 3DGS*

![[assets/figures/papers/paper_list_l2077_https_arxiv_org_abs_2512_17817/figures/016_Table_9.jpg]]
*Table 9: Teacher Ablation with Zero-Shot Semantic Segmentation. The “Teachers” columns mark included components (✓/–). We report foreground metrics for all settings*

![[assets/figures/papers/paper_list_l2077_https_arxiv_org_abs_2512_17817/figures/013_Table_7.jpg]]
*Table 7: Resource and Time Comparison of Uplifting and Rendering-Based Adaptation. Trade-off on InteriorGS (800 scenes): preprocessing-heavy uplifting versus online-heavy rendering adaptation*

![[assets/figures/papers/paper_list_l2077_https_arxiv_org_abs_2512_17817/figures/014_Figure_6.jpg]]
*Figure 6: Scaling Trend Together With Rendering-Based Adaptation. Linear probing performance on InteriorGS vs. number of pretraining scenes. We compare our multi-teacher pretraining with the self-supervised pretraining [63] on 3DGS; Chorus scales faster and to higher accuracy. Our adaptation recipe yields a +2.7% mIoU gain on this new dataset using only 100 scenes*

![[assets/figures/papers/paper_list_l2077_https_arxiv_org_abs_2512_17817/figures/018_Figure_8.jpg]]
*Figure 8: Design Choice Ablation. We validate the choices by evaluating zero-shot segmentation on ScanNet++ Val using a subset of training scenes. SmoothL1 loss, 3DGS-aware augmentations, introducing PE-Spatial in a separate stage, and an instancelevel contrastive term each provide incremental gains*

![[assets/figures/papers/paper_list_l2077_https_arxiv_org_abs_2512_17817/figures/008_Figure_5.jpg]]
*Figure 5: 2D Adaptation Ablation. Performance improves with higher teacher render resolution (left) and more adaptation scenes (right). The left x-axis denotes the 2D teacher’s feature resolution, formatted as (feature size) × bilinear upsample factor*

![[assets/figures/papers/paper_list_l2077_https_arxiv_org_abs_2512_17817/figures/019_Table_10.jpg]]
*Table 10: Robustness to 3DGS Optimization and Density*

## 方法谱系与知识库定位

### 1. 技术谱系与继承关系

Chorus 直接构建在 **SceneSplat** 提出的“上提-对齐”（lift-then-align）范式之上：先利用 3DGS 渲染权重将 2D 教师特征上提到 3D 高斯中心，再训练编码器对齐这些伪标签。SceneSplat 仅蒸馏单一语言对齐教师（SigLIP），而 Chorus 将这一范式扩展为**多教师联合蒸馏**——在共享 3DGS 编码器上同时对齐语言对齐（SigLIP2）、通用视觉（DINOv3）和物体感知（PE-Spatial）三类互补信号。这一扩展并非简单的教师堆叠：Chorus 通过 PHI-S 标准化消除教师特征间的方差差异，并利用分阶段激活策略（先语言教师，再逐步引入通用视觉和物体感知教师）避免教师间干扰，使单共享主干+投影头的设计优于独立分支方案。

在 3D 点云预训练谱系中，Chorus 的点云变体与自监督基线 **Sonata** 形成直接对比，但走的是完全不同的技术路线：Sonata 依赖大规模点云自监督学习，而 Chorus 通过 3DGS 载体获得 2D 基础模型的监督信号，实现了数据效率的跃升（所需预训练场景减少约 39.9 倍）。在语义蒸馏方向上，Chorus 可追溯至 **OpenScene**（早期点云-图像特征蒸馏）和 **RegionPLC**（区域感知点云语言对比），但区别于这些方法依赖点云输入和离线预计算 3D 伪标签，Chorus 利用 3DGS 的原生渲染能力实现了轻量化在线适配。

### 2. 与相关工作的关键区分

**vs. 3DGS 场景编码器（SceneSplat）**：SceneSplat 是唯一直接可比的 3DGS 场景编码基线。Chorus 在三个维度上超越：① 教师信号从单一语言对齐扩展到三类互补知识；② 引入渲染式适配策略，将域外迁移的存储开销从约 1 TB 降至 8 GB；③ 提出 3DGS 感知的数据增强（渲染等效扰动与不成熟流形扰动），替代通用点云增强。

**vs. 点云预训练方法（Sonata 等）**：Chorus 点云变体仅使用中心/颜色/估计法线作为输入，在语义分割线性探测中以 36.0 mIoU 超越 Sonata 的 28.8 mIoU（ScanNet200），且预训练场景数减少约 39.9 倍。这一优势源于 2D 基础模型教师提供的强语义先验，而非点云自监督学习的弱信号。

**vs. 开放词汇分割方法（Mosaic3D 等）**：Mosaic3D 等 3D+2D 方法需要昂贵的多视图图像处理，而 Chorus 是纯前馈的 3D 输入方法。在开放词汇实例分割中，Chorus 不仅以 19.6 mAP 超越 Mosaic3D 的 17.8 mAP，更在 66 个尾类上取得 13.0 mAP（对比前最佳 5.4 mAP），表明多教师蒸馏有效缓解了罕见类别的识别困难。

**vs. 3D 视觉问答方法**：Chorus 仅使用最终编码器阶段的特征（而非多级特征）馈入 VLM，即在 ScanQA 和 Nr3D 上取得有竞争力的结果，证明其嵌入已高度结构化，无需多层特征融合即可支撑语言推理任务。

### 3. 适用边界与限制

**预计算依赖**：尽管渲染式适配消除了域外迁移时的存储瓶颈，但预训练阶段仍需离线提取 2D 教师特征并上提到 3D 高斯中心，这一过程消耗大量离线和存储资源（约 1 TB）。当前未探索在线蒸馏替代预计算的可能性。

**3DGS 载体依赖**：点云变体虽有效，但无法完全独立于 3DGS——预训练仍需 3DGS 场景作为载体来获取 2D 教师监督。对于仅有原始点云的场景，需先优化 3DGS 表示，增加了预处理步骤。

**场景多样性约束**：编码器泛化能力依赖于预训练场景的多样性。在 InteriorGS 数据集上，直接零样本迁移的性能弱于域内适配后，表明模型对训练分布外场景仍存在性能衰减。

**未探索的轻量化空间**：当前教师模型（SigLIP2、DINOv3、PE-Spatial）均为重量级 2D 基础模型，适配阶段每视图需约 0.1 s 的特征光栅化开销。更轻量的教师或更高效的特征上采样策略尚未探索。

### 4. 开放问题与未来方向

1. **在线蒸馏替代预计算**：能否在预训练阶段即采用渲染-蒸馏循环，完全消除离线伪标签的存储和计算开销？这需要解决在线渲染的吞吐量瓶颈和教师模型推理的延迟问题。

2. **统一编码器架构**：当前 3DGS 变体和点云变体共享编码器结构但输入不同。能否构建一个真正统一的编码器，直接接受高斯参数或点云坐标作为输入，而无需变体模型？这涉及对缺失属性（如点云无尺度/不透明度）的鲁棒处理。

3. **大规模户外与动态场景**：现有评估集中在室内场景（ScanNet、Matterport3D、InteriorGS）。在大规模户外环境（如城市街道）或动态场景中，Chorus 的语义一致性、视图配对策略和增强方法是否依然有效，尚待验证。

4. **教师组合的完备性**：当前三类教师（语言对齐、通用视觉、物体感知）是否覆盖了场景理解的必要维度？是否存在其他互补信号（如几何结构、时序一致性）可进一步丰富表示空间？

5. **自监督信号的融合**：Chorus 完全依赖 2D 教师监督，未利用 3DGS 渲染的自监督信号（如新视角合成一致性）。将自监督目标与多教师蒸馏结合，可能进一步提升数据效率和表示质量。

## 原文 PDF

![[paperPDFs/CVPR_2026/Chorus_Multi_Teacher_Pretraining_for_Holistic_3D_Gaussian_Scene_Encoding.pdf]]