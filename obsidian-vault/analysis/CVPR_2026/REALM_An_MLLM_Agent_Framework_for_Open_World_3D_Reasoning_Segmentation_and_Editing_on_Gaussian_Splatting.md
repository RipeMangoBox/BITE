---
title: "REALM: An MLLM-Agent Framework for Open World 3D Reasoning Segmentation and Editing on Gaussian Splatting"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/REALM_An_MLLM_Agent_Framework_for_Open_World_3D_Reasoning_Segmentation_and_Editing_on_Gaussian_Splatting.pdf
project_link: "https://ChangyueShi.github.io/REALM"
code_link: null
aliases:
- REALM
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
core_operator: 全局到局部的空间定位策略（GLSpaG），通过多视图全局推理投票实现粗定位，再结合目标为中心的局部视图细化，从根本上解决了单视角敏感性问题并提升了3D掩膜质量。
primary_logic: 以3D高斯溅射（3DGS）作为高保真场景代理，利用MLLM在2D图像上的推理能力和SAM的分割能力，通过分层多视图聚合（全局投票+局部优化）将2D推理稳健地提升到3D空间，无需针对3D进行大规模微调。
claims:
- 在LERF、3D-OVS和REALM3D三个隐式查询基准上，REALM的mIoU分别达到92.88%、93.68%和82.30%，远超最强基线GS-Group的42.43%、41.79%和65.55%，提升幅度超过50% (LERF/3D-OVS)。
- GLSpaG消融实验显示，从仅使用MLLM的~0.83，到加入全局接地提升至0.89，再经局部细化达到0.95 mIoU，证明组件增益显著。
- 全局相机采样策略中，K-means聚类与TopK-ID选择相比随机采样效果提升明显，是保证多视图推理质量的关键。
- 局部细化仅需50次迭代即可获得最佳性能，过度优化（1000步）会导致严重过拟合（mIoU从0.95降至0.74）。
---

# REALM: An MLLM-Agent Framework for Open World 3D Reasoning Segmentation and Editing on Gaussian Splatting

> [!tip] 核心洞察
> 以3D高斯溅射（3DGS）作为高保真场景代理，利用MLLM在2D图像上的推理能力和SAM的分割能力，通过分层多视图聚合（全局投票+局部优化）将2D推理稳健地提升到3D空间，无需针对3D进行大规模微调。

| 字段 | 内容 |
|------|------|
| 中文题名 | REALM：面向开放世界基于推理的3D分割与编辑的MLLM-Agent框架 |
| 英文题名 | REALM: An MLLM-Agent Framework for Open World 3D Reasoning Segmentation and Editing on Gaussian Splatting |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2510.16410) · [Project](https://ChangyueShi.github.io/REALM) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction |
| Method | REALM |
| Dataset | LERF, 3D-OVS, REALM3D |

> [!tip] 效果简介
> - LERF 上，mIoU 92.88 vs 42.43 (GS-Group) (+50.45)。
> - 3D-OVS 上，mIoU 93.68 vs 41.79 (GS-Group) (+51.89)。
> - REALM3D 上，mIoU 82.30 vs 65.55 (GS-Group) (+16.75)。

## 概要

开放世界中的3D场景理解正从显式类别识别走向隐式、依赖常识推理的指令理解。现有3D开放词汇分割方法多基于CLIP等视觉-语言模型，仅能响应直接描述性查询，缺乏对“泰迪熊手里拿的饮料是什么？”这类需要空间推理与常识判断的隐式指令的理解能力。另一方面，多模态大语言模型（MLLM）虽在2D图像推理上表现出色，但将其直接应用于3D场景时面临根本性瓶颈：仅输入单张或少量随机渲染视图，分割结果对视角选择高度敏感，缺乏鲁棒的3D空间理解与精确定位能力（见Figure 2）。

**REALM**针对上述瓶颈提出了一个MLLM-Agent框架，其核心洞察是：以**3D高斯溅射（3DGS）**作为高保真场景代理，利用MLLM在2D图像上的推理能力与SAM的分割能力，通过分层多视图聚合策略将2D推理稳健地提升到3D空间，全程无需对MLLM进行3D微调。方法的关键调控旋钮是**全局到局部的空间定位策略（GLSpaG）**——先通过多视图全局推理投票实现粗粒度目标定位，再以目标为中心的局部视图进行掩膜细化，从根本上解决了单视角敏感性问题。

在三个隐式查询基准上的实验结果验证了该设计的有效性：REALM在LERF上达到92.88% mIoU，在3D-OVS上达到93.68% mIoU，在自建REALM3D基准上达到82.30% mIoU，相较最强基线GS-Group分别提升50.45、51.89和16.75个百分点（Table 1）。消融实验进一步表明，GLSpaG各阶段贡献显著——从仅使用MLLM的约0.83 mIoU，到加入全局接地提升至0.89，再经局部细化达到0.95（Table 3a）。此外，REALM还支持基于语言指令的多样化3D编辑任务，包括物体移除、替换与风格迁移（Figure 7）。

### 开放世界3D场景理解的新需求

随着3D视觉与图形技术的快速发展，对三维场景进行语义理解与交互式编辑的需求日益增长。传统的3D分割方法主要依赖预定义的类别标签，难以应对开放世界中灵活多变的语言指令。近年来，以CLIP为代表的视觉-语言模型被引入3D场景理解任务，催生了一系列开放词汇3D分割方法，如**Gaga**（Lyu et al., arXiv 2024）、**GAGS**（Peng et al., arXiv 2024）和**GS-Group**（Ye et al., ECCV 2024）等。这些方法虽然能够处理部分直接描述的查询，但在面对需要常识推理的隐式指令时暴露出根本性缺陷。

### 核心瓶颈：从“看见”到“理解”的鸿沟

现有方法的瓶颈在于，它们依赖CLIP等模型进行语义匹配，而CLIP本质上是基于图像-文本对齐的检索模型，缺乏对复杂语义关系的推理能力。例如，当用户提出“泰迪熊手里拿着的饮料是哪一个？”这类需要空间关系理解与常识推断的隐式查询时，CLIP只能进行简单的特征相似度匹配，无法拆解指令中的逻辑链条。这使得现有方法在隐式查询场景下的分割精度极低——在LERF和3D-OVS基准上，最强基线GS-Group的mIoU分别仅为42.43%和41.79%（Table 1）。

多模态大语言模型（MLLM）在2D图像推理上展现出卓越能力，能够理解复杂的自然语言指令并进行视觉推理。一个直观的思路是将MLLM直接应用于3D场景的渲染视图。然而，这一方案面临一个关键障碍：**单视图敏感性问题**。如Figure 2所示，仅向MLLM输入一张或少数几张随机渲染视图时，分割结果对视角选择高度敏感——某些视角下目标被遮挡、处于图像边缘或与背景混淆时，MLLM无法准确识别，导致3D分割失败。这暴露了2D推理直接迁移到3D空间时的根本矛盾：MLLM擅长单张图像的深度理解，却缺乏对3D场景的空间一致性感知。

### 本文动机：将2D推理稳健地提升到3D

REALM的提出正是为了解决上述双重挑战：**如何在保留MLLM强大推理能力的同时，克服单视图敏感性，实现稳健的3D推理分割？** 核心思路是采用3D高斯溅射（3DGS）作为高保真场景代理，利用其逼真的新视角渲染能力为MLLM提供多视角输入，并通过分层多视图聚合策略将2D推理结果提升为3D空间中的一致分割。

具体而言，REALM的设计围绕三个关键动机展开：

1. **以3DGS为桥梁**：3DGS能够渲染照片级真实感的新视角，这些视图天然适配MLLM的视觉理解能力，为2D推理向3D迁移提供了高质量的信息载体。

2. **从全局到局部的空间定位**：单视角的脆弱性源于信息不完整，而多视角冗余可以弥补这一缺陷。通过在多视角间进行投票聚合，可以从统计上消除单视角误判，实现鲁棒的3D目标定位。

3. **无需3D微调**：REALM不要求对MLLM进行任何3D数据的微调，完全利用预训练模型的2D推理能力，通过精心设计的空间聚合策略将其泛化到3D领域，保持了方法的通用性和可扩展性。

## 核心方法与创新机理

REALM的核心创新在于将多模态大语言模型（MLLM）的2D推理能力稳健地提升到3D空间，解决了现有方法在隐式、常识性查询下的根本性缺陷。其创新路径可归纳为三个关键的“changed slots”：

### 1. 从CLIP直接查询到MLLM推理分割

现有3D开放词汇分割方法（如**Gaga** (Lyu et al., arXiv 2024)、**GAGS** (Peng et al., arXiv 2024)、**GS-Group** (Ye et al., ECCV 2024)）依赖CLIP等视觉-语言模型提取特征，本质上是基于相似度匹配的直接查询。这类方法缺乏对隐式指令（如“泰迪熊手里拿着的饮料是什么？”）的理解能力——它们无法建立“持有”这一空间关系与目标物体之间的因果联系。

REALM用**MLLM（Qwen2.5-VL）+ SAM**的组合替代了CLIP作为2D语义理解源。其核心模块**LMSeg**（MLLM-based Visual Segmenter）通过提示工程技术，让MLLM对单张渲染视图执行图像级推理，返回目标的边界框、类别和解释：

$$(\boldsymbol{B}, \boldsymbol{\mathcal{C}}, \boldsymbol{\mathcal{E}}) = \mathbf{MLLM}(\boldsymbol{\mathcal{T}}, q)$$

这一替换从根本上赋予了系统常识推理能力，使其能够处理需要空间关系理解、属性判断和逻辑推断的复杂查询。

### 2. 从单视图敏感到全局-局部空间定位（GLSpaG）

然而，直接将MLLM应用于3D场景存在一个关键瓶颈：**单视图敏感性**。如Figure 2所示，仅向MLLM输入一张或少量随机渲染视图时，分割结果高度依赖视角选择——某些视角下目标可能被遮挡、位于边缘，或与其他物体混淆，导致MLLM推理失败。

现有方法多采用单视图或简单求和的多视图聚合策略，缺乏对3D空间结构的显式建模。REALM提出的**Global-to-Local Spatial Grounding（GLSpaG）**通过分层多视图聚合从根本上解决了这一问题：

- **全局粗定位**：首先对训练相机位姿进行K-means聚类，确保视角多样性；然后通过TopK-ID策略选择包含最多不同实例ID的前$N^{\mathrm{global}}$个视图作为全局视图。MLLM在这些全局视图上并行推理，通过投票机制聚合各视图的实例ID预测，得到粗粒度的目标身份：

  $$\{\phi_i^{\mathrm{global}}\}_{i=1}^{N^{\mathrm{global}}} = \mathrm{TopK-ID}(\{\phi_i^{\mathrm{cluster}}, \mathrm{i}\hat{\mathrm{d}}_i\}_{i=1}^{N^{\mathrm{cluster}}}, N^{\mathrm{global}})$$

- **局部细化**：选取目标所在区域的局部特写视图，利用LMSeg生成的2D掩膜与渲染的3D掩膜之间的L1损失进行精细化优化：

  $$\mathcal{L}_{\mathrm{local}} = || \hat{M}_i - M_i^{2D-\mathrm{Local}} ||_1$$

这一分层策略的因果逻辑清晰：全局投票解决了“哪个物体”的问题（粗定位），局部优化解决了“边界在哪”的问题（精细化），二者互补，使得2D推理结果能够稳健地映射到3D空间。

### 3. 从无优化到基于局部视图的3D掩膜细化

基线方法通常直接使用多视图聚合结果作为最终3D掩膜，不做进一步优化。REALM引入了一个轻量级的局部细化步骤：以LMSeg在局部视图上生成的2D掩膜为监督信号，对3D高斯原语的掩膜进行迭代优化。消融实验（Table 3(a)）显示，这一步骤将mIoU从仅使用全局接地的0.89提升至0.95，贡献显著。

值得注意的是，局部细化仅需**50次迭代**即可达到最佳性能；过度优化（1000步）会导致严重过拟合，mIoU从0.95骤降至0.74（Table 3(f)）。这表明该模块的设计恰到好处——在提供足够细化能力的同时，避免了过度依赖单一2D视图导致的3D一致性退化。

### 创新本质：以3DGS为代理的2D-to-3D推理提升

上述三个changed slots共同构成了REALM的核心技术路径：**以3D高斯溅射（3DGS）为高保真场景代理**，利用其逼真的新视角渲染能力作为MLLM的“眼睛”，通过分层多视图聚合策略将MLLM在2D图像上的推理能力稳健地提升到3D空间。这一路径无需对MLLM进行3D特定的大规模微调，保持了框架的灵活性和可扩展性。

REALM 的整体架构围绕一个核心洞察展开：**以 3D 高斯溅射（3DGS）作为高保真场景代理，将 MLLM 在 2D 图像上的推理能力稳健地提升到 3D 空间**。框架的输入是已重建为 3DGS 的场景以及用户的自然语言隐式查询，输出是精确的 3D 目标掩膜，并可进一步支持移除、替换、风格迁移等 3D 编辑操作。

### Pipeline 总览

REALM 由四个主要模块串联构成，形成一条从 2D 实例特征提取到 3D 掩膜细化的完整链路：

1. **3D 特征场构建（3D Feature Field）**：首先利用 SAM 在多视图训练图像上提取实例掩膜，通过时序传播模型关联跨视图实例，为每个 3D 高斯原语分配一致的实例特征，并训练一个分类器 CLS 用于后续的实例识别。通过 alpha 混合可将这些特征渲染到任意视点的 2D 特征图：

   $$F = \sum_{i=1}^{n} f_i \alpha_i \prod_{j=1}^{i-1} (1 - \alpha_j)$$

   进而逐像素预测实例 ID：

   $$\hat{id}(u,v) = \arg\max_k (CLS(F)_{u,v,k})$$

2. **MLLM-based Visual Segmenter（LMSeg）**：对单张渲染视图执行图像级推理分割。通过提示工程技术将用户查询 $q$ 和渲染图像输入 MLLM（Qwen2.5-VL），MLLM 返回目标边界框 $B$、类别 $C$ 和解释 $E$：

   $$(B, C, E) = \mathbf{MLLM}(T, q)$$

   随后借助 SAM 和已构建的特征场，将 2D 边界框映射为场景中的具体实例 ID。

3. **Global Spatial Grounding（全局空间接地）**：这是解决单视角敏感性的关键设计。首先对训练相机位姿进行 K-means 聚类，从每簇中选取一个代表相机：

   $$\{ \phi_i^{\mathrm{cluster}} \}_{i=1}^{N^{\mathrm{cluster}}} = \mathbf{KMeans}(\{ \phi_j^{\mathrm{train}} \}_{j=1}^{N^{\mathrm{train}}}, N^{\mathrm{cluster}})$$

   再从中选择包含最多不同实例 ID 的前 $N^{\mathrm{global}}$ 个视图作为全局视图：

   $$\{ \phi_i^{\mathrm{global}} \}_{i=1}^{N^{\mathrm{global}}} = \mathrm{TopK-ID}(\{ \phi_i^{\mathrm{cluster}}, \mathrm{i}\hat{\mathrm{d}}_i \}_{i=1}^{N^{\mathrm{cluster}}}, N^{\mathrm{global}})$$

   每个全局视图独立运行 LMSeg，各视图的实例 ID 预测通过投票机制聚合，确定最终目标实例身份 $ID^y$。根据该身份，为每个高斯原语生成初始 3D 掩膜：

   $$M_i^{3D} = \begin{cases} 1, & \arg\max_k (CLS(f_i)) = ID^y \\ 0, & \arg\max_k (CLS(f_i)) \neq ID^y \end{cases}$$

4. **Local Spatial Grounding（局部空间接地）**：从聚类相机中筛选出预测实例图中包含目标 ID 的视图作为局部特写视图：

   $$\{ \phi_i^{\mathrm{local}} \}_{i=1}^{N^{\mathrm{local}}} = \{ \phi_j^{\mathrm{cluster}} \mid ID^y \in \mathrm{i}\hat{\mathrm{d}}_j, j=1,\dots,N^{\mathrm{cluster}} \}$$

   在这些局部视图上，利用 LMSeg 生成的 2D 掩膜与渲染的 3D 掩膜之间的 L1 损失对 3D 掩膜进行精细化优化：

   $$\mathcal{L}_{\mathrm{local}} = || \hat{M}_i - M_i^{2D-\mathrm{Local}} ||_1$$

### 模块间关系与数据流

上述四个模块形成 **“全局到局部”的层次化聚合策略（GLSpaG）**：3D 特征场提供底层的实例识别能力；LMSeg 在 2D 层面完成推理与初步分割；全局接地通过多视图投票将单视角的不确定性转化为稳健的粗粒度 3D 定位；局部接地则利用目标特写视图进行细粒度掩膜优化。这种设计从根本上规避了直接向 MLLM 输入单张或少量渲染视图时对视角选择高度敏感的问题（如 Figure 2 所示）。

### 关键设计选择

- **3DGS 作为场景代理**：利用其高保真新视图渲染能力，为 MLLM 提供适合理解的真实感图像，无需在 3D 层面进行大规模微调。
- **MLLM 替代 CLIP**：将 2D 语义理解源从仅支持直接查询的 CLIP/Grounded-SAM 升级为具备常识推理能力的 MLLM，使框架能够处理“帮我找到那个看起来孤独的玩具”等隐式查询。
- **分层多视图聚合**：相比基线方法的单视图或简单求和，K-means 聚类加 TopK-ID 投票的全局粗定位与局部 L1 细化的组合，是性能提升的核心因果机制。消融实验证实，仅使用 MLLM 时 mIoU 约 0.83，加入全局接地提升至 0.89，再经局部细化达到 0.95（Table 3a）。

> **注意**：框架的推理总耗时约 8.68 秒/查询，其中局部细化仅需 50 次迭代（3.67 秒），过度优化（1000 步）会导致严重过拟合，mIoU 从 0.95 降至 0.74（Table 3f）。

![[assets/figures/papers/paper_list_l2183_https_arxiv_org_abs_2510_16410/figures/003_Figure_3.jpg]]
*Figure 3: Overview of REALM. Top: Global-to-Local Spatial Grounding (GLSpaG) pipline hierarchically aggregates the outputs of LMSeg agents from global context to local refinement. Bottom left: We optimize a 3D feature field from 2D SAM masks for 3D consistent identification. Bottom right: MLLM-based Visual Segmenter (LMSeg) performs image-level reasoning on one viewpoint and integrates identity information from the optimized feature field to determine the selected instance ID*

![[assets/figures/papers/paper_list_l2183_https_arxiv_org_abs_2510_16410/figures/001_Figure_1.jpg]]
*Figure 1: We propose REALM, an MLLM-agent framework designed for open-world 3D reasoning segmentation and editing within 3D Gaussian Splatting (3DGS). REALM can perform reasoning over implicit instructions and accurately segment the target object. REALM also supports various 3D editing instructions, including object removal, replacement, and style transfer*

REALM 的核心架构围绕一个关键洞察展开：将 2D MLLM 的推理能力稳健地提升到 3D 空间，需要一个分层式的多视图聚合机制。本节解析构成该框架的四个核心模块及其关键公式。

### 3D 特征场构建

REALM 首先为 3DGS 场景中的每个高斯原语分配一致的实例特征，构建可渲染的 3D 特征场。具体而言，利用 SAM 从训练视图中提取 2D 实例掩膜，再通过时序传播模型跨视图关联实例，最终为每个高斯原语优化得到一个实例特征向量 $f_i$。

渲染时，采用与 3DGS 颜色渲染相同的 alpha 混合机制，将 3D 特征投影到 2D 图像平面：

$$F = \sum_{i=1}^{n} f_i \alpha_i \prod_{j=1}^{i-1} (1 - \alpha_j) \quad \text{(Eq. 1)}$$

其中 $f_i$ 为第 $i$ 个高斯原语的特征，$\alpha_i$ 为其不透明度。得到渲染特征图 $F$ 后，通过预训练的分类器 CLS 逐像素预测实例 ID：

$$\hat{id}(u,v) = \arg\max_k (CLS(F)_{u,v,k}) \quad \text{(Eq. 2)}$$

这一特征场是整个框架的 3D 身份识别基础，使后续的 MLLM 推理结果能够与 3D 高斯原语建立对应关系。

### MLLM 驱动的视觉分割器（LMSeg）

LMSeg 是 REALM 的 2D 推理核心。对于给定的渲染视图和自然语言查询 $q$，LMSeg 通过提示工程引导 MLLM（Qwen2.5-VL）进行图像级推理，输出结构化的三元组：

$$(\boldsymbol{B}, \boldsymbol{\mathcal{C}}, \boldsymbol{\mathcal{E}}) = \mathbf{MLLM}(\boldsymbol{\mathcal{T}}, q) \quad \text{(Eq. 3)}$$

其中 $\boldsymbol{\mathcal{T}}$ 为提示模板，$\boldsymbol{B}$ 为目标边界框，$\boldsymbol{\mathcal{C}}$ 为预测类别，$\boldsymbol{\mathcal{E}}$ 为推理过程的自然语言解释。随后，将边界框 $\boldsymbol{B}$ 作为 SAM 的提示，生成精细的 2D 分割掩膜，并结合 Eq. 2 的实例 ID 预测图，确定该视图中目标对应的实例 ID。

与依赖 CLIP 等固定编码器的基线方法（如 **GS-Group** (Ye et al., ECCV 2024)、**Gaga** (Lyu et al., arXiv 2024)）不同，LMSeg 能够理解隐式、需要常识推理的指令（如“泰迪熊拿着的饮料”），这是 REALM 在复杂查询上取得显著优势的根本原因。

### 全局空间接地（Global Spatial Grounding）

单视图推理对视角选择高度敏感，这是直接使用 MLLM 进行 3D 分割的核心瓶颈。全局空间接地通过多视图投票机制解决此问题。

首先，对训练相机位姿进行 K-means 聚类，获得 $N^{\text{cluster}}$ 个代表性视角：

$$\{ \phi_i^{\mathrm{cluster}} \}_{i=1}^{N^{\mathrm{cluster}}} = \mathbf{KMeans}(\{ \phi_j^{\mathrm{train}} \}_{j=1}^{N^{\mathrm{train}}}, N^{\mathrm{cluster}}) \quad \text{(Eq. 4)}$$

随后，从聚类代表中选取包含最多不同实例 ID 的前 $N^{\text{global}}$ 个视图作为全局视角：

$$\{ \phi_i^{\mathrm{global}} \}_{i=1}^{N^{\mathrm{global}}} = \mathrm{TopK-ID}(\{ \phi_i^{\mathrm{cluster}}, \mathrm{i}\hat{\mathrm{d}}_i \}_{i=1}^{N^{\mathrm{cluster}}}, N^{\mathrm{global}}) \quad \text{(Eq. 5)}$$

对每个全局视图独立运行 LMSeg，获得各自的候选实例 ID。通过投票机制聚合这些预测，确定最终的目标实例 ID $ID^y$。基于此，生成初始的 3D 掩膜：

$$M_i^{3D} = \begin{cases} 1, & \arg\max_k (CLS(f_i)) = ID^y \\ 0, & \arg\max_k (CLS(f_i)) \neq ID^y \end{cases} \quad \text{(Eq. 6)}$$

消融实验证实，K-means 聚类与 TopK-ID 选择策略是保证多视图推理质量的关键——相比随机采样，该策略在 Figurines 场景上将 mIoU 从约 0.83 提升至 0.89（Table 3a, 3b）。

### 局部空间接地与掩膜细化（Local Spatial Grounding）

全局阶段产生的 3D 掩膜较为粗糙，局部空间接地通过目标特写视图进行精细化调整。首先筛选出预测实例图中包含目标 ID 的聚类相机作为局部视图：

$$\{ \phi_i^{\mathrm{local}} \}_{i=1}^{N^{\mathrm{local}}} = \{ \phi_j^{\mathrm{cluster}} \mid ID^y \in \mathrm{i}\hat{\mathrm{d}}_j, j=1,\dots,N^{\mathrm{cluster}} \} \quad \text{(Eq. 7)}$$

在这些局部视图上运行 LMSeg 获得精确的 2D 掩膜 $M_i^{2D-\mathrm{Local}}$，将其作为监督信号，通过最小化 L1 损失优化 3D 掩膜：

$$\mathcal{L}_{\mathrm{local}} = || \hat{M}_i - M_i^{2D-\mathrm{Local}} ||_1 \quad \text{(Eq. 8)}$$

其中 $\hat{M}_i$ 为渲染的 3D 掩膜在当前局部视图上的投影。实验表明，仅需 50 次迭代即可将 mIoU 从 0.89 提升至 0.95；但过度优化（1000 步）会导致严重过拟合，mIoU 降至 0.74（Table 3f），揭示了该模块“适度优化”的重要性。

### 模块协同的因果机制

GLSpaG 的分层设计体现了从粗到精的空间推理逻辑：全局阶段通过多视角投票消除了单视图的歧义性，解决了“视角敏感性”瓶颈；局部阶段利用特写视图的高分辨率信息，弥补了全局视图在目标边界处的精度不足。这一“先定位、后细化”的策略是 REALM 在 LERF 和 3D-OVS 基准上 mIoU 超过 92% 的核心因果机制。

## 实验与关键发现

### 主实验结果：隐式查询下的3D推理分割

REALM在三个隐式查询基准上展现了决定性的性能优势。如表1所示，在LERF数据集上，REALM的mIoU达到**92.88%**，而最强基线GS-Group仅为42.43%，提升幅度超过50个百分点；在3D-OVS数据集上，REALM取得**93.68%** mIoU，对比GS-Group的41.79%同样实现了51.89个百分点的巨大领先。在论文新提出的REALM3D基准上，REALM以**82.30%** mIoU显著优于GS-Group的65.55%，领先16.75个百分点。

这一压倒性优势揭示了现有方法的根本瓶颈：**Gaga**（Lyu et al., arXiv 2024）、**GAGS**（Peng et al., arXiv 2024）和**GS-Group**（Ye et al., ECCV 2024）等开放词汇3D分割方法依赖CLIP或Grounded-SAM，仅能处理直接查询，缺乏对隐式、需要常识推理指令的理解能力。当查询涉及“可以盛放液体的容器”或“用来书写的工具”这类需要语义推理的表述时，CLIP的文本-图像匹配机制无法建立正确的对应关系，导致分割完全失败。REALM通过引入MLLM（Qwen2.5-VL）作为推理引擎，从根本上弥补了这一能力缺口。

### 消融实验：GLSpaG各组件的因果贡献

在LERF数据集的Figurines场景上进行的消融实验（Table 3）系统性地拆解了GLSpaG各阶段的增益。

![[assets/figures/papers/paper_list_l2183_https_arxiv_org_abs_2510_16410/figures/017_Table_3.jpg]]
*Table 3: Ablation Study. We conduct a detailed ablation study on “Figurines” of the LERF dataset to evaluate the contribution of each component in our method. Cells highlighted in bold indicate the best performance*

**组件增益的因果链**（Table 3a）：仅使用Qwen2.5-VL进行单视图推理时，mIoU约为**0.83**。这一基线已经优于所有对比方法，证明了MLLM推理能力的价值，但单视图对视角选择的敏感性限制了其上限。加入全局空间接地（Global Spatial Grounding）后，mIoU提升至**0.89**，验证了多视图投票聚合能够有效消除单视角歧义。进一步引入局部空间接地（Local Spatial Grounding）进行50步迭代优化后，mIoU达到**0.95**，mBIoU达到0.94。这一从0.83→0.89→0.95的递进式提升清晰表明：全局投票解决“是什么”的粗定位问题，局部细化解决“在哪里”的精确边界问题，两者形成互补。

**全局相机采样的关键性**（Table 3b, 3d）：K-means聚类与TopK-ID选择策略的组合取得了最优性能（mIoU 0.95）。消融显示，若将K-means替换为随机采样，性能显著下降；若聚类数量设置不当（过少导致视角多样性不足，过多引入噪声视角），多视图推理质量均会受到损害（Table 3d）。这证实了全局接地阶段的核心在于选取**信息量大且视角互补**的视图子集，而非简单增加视图数量。Table 3e进一步表明，REALM对全局视图数量$N^{global}$不敏感，在较大范围内保持鲁棒。

**局部细化的适度原则**（Table 3f）：局部细化仅需**50次迭代**即可达到最佳mIoU 0.95，耗时3.67秒。当迭代步数增加到100步时性能基本持平，但增加到1000步后mIoU急剧下降至**0.74**，出现严重的过拟合。这一现象的原因在于：局部细化使用的2D掩膜$M_i^{2D-Local}$来自LMSeg的单视图推理，其本身存在边界不确定性。过度优化会使3D掩膜过拟合到该特定视图的2D噪声，丧失多视图一致性带来的鲁棒性。50步迭代在拟合精度与泛化性之间取得了最优平衡。

### 渲染效率与推理开销

Table 3c显示，REALM的3DGS渲染速度高达**354.72 FPS**，LMSeg推理、GLSpaG聚合和局部优化等额外模块未对渲染管线造成可感知的影响。整体推理时间为**8.68秒/查询**，其中主要开销来自MLLM的多视图调用和局部迭代优化。这一速度虽未达到实时交互要求，但已具备实用价值，且MLLM推理速度的持续提升将直接惠及REALM。

### REALM3D基准的贡献

论文构建的REALM3D基准（Table 2, Figure 6）包含**100+场景**和**1444对提示-掩膜标注**，每个掩膜均配有隐式查询提示。与LERF和3D-OVS相比，REALM3D在场景数量和提示多样性上均有显著扩展。值得注意的是，该基准使用Qwen2.5-VL进行半自动标注，这虽大幅降低了人工成本，但也引入了对该特定MLLM的潜在偏好——REALM在该基准上的优势可能部分源于标注模型与推理模型的一致性，这一公平性限制需要在解读结果时予以考虑。

![[assets/figures/papers/paper_list_l2183_https_arxiv_org_abs_2510_16410/figures/009_Figure_6.jpg]]
*Figure 6: Examples in REALM3D benchmark. We use MLLM [3] and SAM [21] to annotate over 1K prompt–mask pairs, enabling quantitative evaluation on implicit queries*

### 失败模式与局限性

尽管REALM在主实验中表现优异，实验分析揭示了以下边界条件：

1. **过拟合敏感性**：局部细化在1000步迭代后性能崩溃（0.95→0.74），表明当前仅依赖单一2D掩膜进行3D优化的策略缺乏正则化机制，在极端优化条件下缺乏鲁棒性。
2. **场景覆盖局限**：实验集中在室内物体级场景，缺乏室外大规模环境或动态场景的验证。REALM3D基准本身也以室内场景为主。
3. **MLLM依赖性**：REALM的性能与所选MLLM的能力强绑定。若MLLM对某类查询的推理失败，GLSpaG的多视图投票机制仅能缓解视角歧义，无法纠正语义层面的错误推理。

![[assets/figures/papers/paper_list_l2183_https_arxiv_org_abs_2510_16410/figures/007_Table_1.jpg]]
*Table 1: Quantitative results on LERF [18], 3D-OVS [25] and our proposed REALM3D benchmarks. We compare REALM with other models on implicit queries. The best results are marked in bold*

![[assets/figures/papers/paper_list_l2183_https_arxiv_org_abs_2510_16410/figures/018_Figure_8.jpg]]
*Figure 8: Ablation study on GLSpaG. The local grounding stage refines the 3D segmentation results*

## 定位与知识库关联

### 1. 方法继承与关键突破

REALM 的核心技术路线是将 **2D 视觉推理能力稳健地提升到 3D 空间**，其方法谱系可从以下三个维度追溯：

**3D 开放词汇分割**：现有方法如 **Gaga** (Lyu et al., arXiv 2024)、**GAGS** (Peng et al., arXiv 2024) 和 **GS-Group** (Ye et al., ECCV 2024) 均依赖 CLIP 等视觉-语言模型进行语义对齐，但这类模型仅能处理直接查询，缺乏对隐式指令的常识推理能力。REALM 在 Table 1 中的结果直接揭示了这一瓶颈：在 LERF 和 3D-OVS 的隐式查询上，GS-Group 的 mIoU 仅为 42.43% 和 41.79%，而 REALM 达到 92.88% 和 93.68%，提升幅度超过 50 个百分点。这一巨大差距的根本原因在于，CLIP 类模型无法理解诸如“泰迪熊正在喝的饮料”这类需要空间关系推理的查询。

**2D 推理分割**：REALM 的 LMSeg 模块借鉴了 MLLM + SAM 的图像级推理分割范式，但将其从 2D 领域引入 3D 场景。与传统 2D 推理分割不同，REALM 面临的核心挑战是**单视角敏感性**（Figure 2 所示）：直接向 MLLM 输入单个或少量随机渲染视图时，分割结果高度依赖视角选择，缺乏鲁棒性。

**3D 场景表示**：REALM 选择 3D Gaussian Splatting (3DGS) 作为场景代理，利用其高保真渲染能力（354.72 FPS，Table 3(c)）为 MLLM 提供逼真的 2D 视图。这一选择使 REALM 无需针对 3D 数据进行大规模微调，仅需训练一个轻量级的 3D 特征场用于跨视角实例关联。

### 2. 核心创新：GLSpaG 的分层聚合机制

REALM 的核心创新在于 **Global-to-Local Spatial Grounding (GLSpaG)** 策略，它通过分层多视图聚合从根本上解决了单视角敏感性问题：

- **全局粗定位**：对训练相机位姿进行 K-means 聚类（$N^{\text{cluster}}=24$），再通过 TopK-ID 选择包含最多不同实例 ID 的 $N^{\text{global}}=8$ 个视图，在这些视图上并行运行 LMSeg 进行推理，最后通过投票机制确定目标实例 ID。消融实验（Table 3(b)）证实，K-means + TopK-ID 的组合相比随机采样等策略显著提升了性能。

- **局部精细化**：选取目标实例所在的局部特写视图，利用 LMSeg 生成的 2D 掩膜与渲染的 3D 掩膜之间的 L1 损失 $\mathcal{L}_{\text{local}} = || \hat{M}_i - M_i^{2D-\text{Local}} ||_1$ 进行优化。消融实验（Table 3(a)）显示，从仅使用 MLLM 的 mIoU ~0.83，到加入全局接地提升至 0.89，再经局部细化达到 0.95，证明了各阶段的独立贡献。

值得注意的是，局部细化的迭代次数存在最优值：50 步迭代达到最佳 mIoU 0.95，但过度优化至 1000 步时性能急剧下降至 0.74（Table 3(f)），表明该方法对过拟合高度敏感。

### 3. 适用边界与局限

**适用场景**：
- 室内静态场景的物体级推理分割与编辑
- 需要常识推理的隐式语言查询（空间关系、功能属性等）
- 基于 3DGS 重建的高保真场景

**已知局限**（需在后续研究中验证）：

1. **基准偏差风险**：REALM3D 数据集使用 Qwen2.5-VL 进行半自动标注，可能对该特定 MLLM 产生性能评估偏差。这一标注策略的公平性需要在更多 MLLM 上进行交叉验证。

2. **场景多样性不足**：当前实验集中在室内物体级分割（LERF、3D-OVS、REALM3D），缺乏室外大规模场景或动态场景的验证。能否将 REALM 推广至完全开放域的大规模户外环境并保持推理鲁棒性，仍是一个开放问题。

3. **实时性限制**：整体推理时间为 8.68 秒/查询，虽已优化但仍未达到实时交互要求。此外，局部细化对迭代次数高度敏感，过度优化会导致严重过拟合。

4. **静态场景假设**：REALM 假设场景已重建为 3DGS，对于动态物体或大幅视角变化的鲁棒性尚未验证。能否与 SLAM 或在线建图系统结合，实现面向机器人的即时推理交互，是重要的后续方向。

### 4. 开放问题与后续方向

1. **多模态 3D 掩膜优化**：当前的局部细化仅依赖单一 2D 掩膜（L1 损失），能否结合深度、法向等多模态信息进行更精细的 3D 分割，是提升掩膜质量的可能路径。

2. **时序推理与多步交互**：REALM 目前处理的是单步隐式查询，未涉及时序推理或需要多步交互的复杂指令（如“先找到沙发，再找到沙发上的遥控器”），这限制了其在具身智能等场景中的应用。

3. **MLLM 无关性验证**：由于 REALM3D 标注和主实验均使用 Qwen2.5-VL，该方法对 MLLM 选择的鲁棒性需要在更多模型（如 GPT-4V、Gemini）上进行验证，以排除对特定 MLLM 的过拟合。

## 原文 PDF

![[paperPDFs/CVPR_2026/REALM_An_MLLM_Agent_Framework_for_Open_World_3D_Reasoning_Segmentation_and_Editing_on_Gaussian_Splatting.pdf]]
