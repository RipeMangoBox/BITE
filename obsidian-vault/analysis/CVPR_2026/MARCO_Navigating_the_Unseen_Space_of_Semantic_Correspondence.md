---
title: "MARCO: Navigating the Unseen Space of Semantic Correspondence"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/MARCO_Navigating_the_Unseen_Space_of_Semantic_Correspondence.pdf
aliases:
- MARCO
tags:
- CVPR_2026
- topic/vision_multimodal_applications/segmentation
- topic/vision_multimodal_applications
core_operator: 1) 由粗到细的高斯RBF损失，通过余弦退火逐步缩小目标分布的带宽，引导模型从区域对齐过渡到亚像素级精确定位；2) 密集自蒸馏框架，利用DINOv2特征空间中可靠的互近邻匹配，经过Delaunay三角剖分、仿射致密化和流聚类，生成密集伪对应，并以GT关键点为锚点过滤错误匹配，从而将稀疏监督扩展为覆盖整个物体表面的平滑对应场。
primary_logic: DINOv2的预训练特征包含稀疏但语义一致的对应线索，可以通过互近邻挖掘和几何约束传播至整个物体区域，形成自我监督，使模型在学习过程中不仅保持原有的语义结构，而且获得细粒度的定位能力，从而在保持高效架构的同时实现强泛化。
claims:
- MARCO在标准基准SPair-71k的严格阈值PCK@0.01上较强基线Geo-SC提升+8.9个百分点，说明精细定位能力大幅增强。
- 移除密集自蒸馏损失后，在SPair-U未见关键点上PCK@0.10从67.5骤降至41.8（-25.7），证明自蒸馏对泛化至关重要。
- 仅添加由粗到细目标，就将SPair-71k的PCK@0.01从20.0提升至26.8，表明该策略显著提高细粒度对齐。
- 在MP-100未见类别上，MARCO平均PCK@0.10比先前最强方法高+4.5%，体现跨类别的鲁棒泛化。
---

# MARCO: Navigating the Unseen Space of Semantic Correspondence

> [!tip] 核心洞察
> DINOv2的预训练特征包含稀疏但语义一致的对应线索，可以通过互近邻挖掘和几何约束传播至整个物体区域，形成自我监督，使模型在学习过程中不仅保持原有的语义结构，而且获得细粒度的定位能力，从而在保持高效架构的同时实现强泛化。

| 字段 | 内容 |
|------|------|
| 中文题名 | MARCO：探索语义对应未至空间 |
| 英文题名 | MARCO: Navigating the Unseen Space of Semantic Correspondence |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2604.18267) · [Project](https://visinf.github.io/MARCO) |
| Topic | #topic/vision_multimodal_applications/segmentation #topic/vision_multimodal_applications |
| Method | MARCO |
| Dataset | SPair-71k, SPair-U, MP-100 Apparel items, MP-100 Animal body |

> [!tip] 效果简介
> - SPair-71k 上，PCK@0.10 87.2 vs 83.2 (Geo-SC) (+4.0)；PCK@0.01 27.0 vs 21.7 (Geo-SC) (+5.3)。
> - SPair-U (unseen keypoints) 上，PCK@0.10 67.5 vs 62.4 (Jamais Vu) (+5.1)。
> - MP-100 Apparel items (unseen keypoints) 上，PCK@0.10 55.9 vs 45.7 (Jamais Vu) (+10.2)。

## 概述

语义对应（semantic correspondence）旨在建立不同图像中同一语义部位之间的像素级映射，是视觉理解的核心子问题。近年来，基于稀疏关键点监督的方法在标准基准上取得了显著进展，但一个关键瓶颈始终存在：**模型过度拟合有限的标注位置，导致在未见关键点和新类别上的泛化能力急剧下降**。其深层原因在于，稀疏监督使模型仅在标注点附近优化特征表示，而非标注区域的特征发生“坍塌”，破坏了物体表面的几何一致性（见Figure 2）。

针对这一问题，**MARCO** 提出了一种基于密集自蒸馏的语义对应学习框架。其核心洞察在于：DINOv2 的预训练特征空间本身就蕴含稀疏但语义一致的对应线索——这些线索可以通过互近邻匹配挖掘，并借助几何约束传播至整个物体表面，从而将有限的稀疏标注扩展为覆盖全局的密集训练信号。这一思路使得模型在保持轻量架构的同时，获得了显著的泛化能力。

具体而言，MARCO 从两个维度驱动模型突破稀疏监督的局限：

1. **由粗到细的高斯 RBF 损失**：通过余弦退火逐步缩小目标分布的带宽（σ 从 3 降至 1），引导模型从区域级粗对齐平滑过渡到亚像素级精确定位，在细粒度阈值下大幅提升匹配精度。

2. **密集自蒸馏框架**：利用教师模型（EMA 更新）在 DINOv2 特征空间中挖掘互近邻匹配，经过 Delaunay 三角剖分、仿射致密化和流聚类，生成覆盖物体表面的密集伪对应；再以 GT 关键点为锚点过滤错误匹配，最终通过自蒸馏损失将稀疏监督扩展为平滑的对应场。

在标准基准 **SPair-71k** 上，MARCO 在严格阈值 PCK@0.01 上达到 27.0%，较先前最强方法 **Geo-SC**（21.7%）提升 **+5.3 个百分点**；在宽松阈值 PCK@0.10 上达到 87.2%（+4.0）。在泛化测试中，MARCO 在 **SPair-U**（未见关键点）上达到 67.5%，较同期工作 **Jamais Vu**（62.4%）提升 +5.1；在 **MP-100** 未见类别上平均 PCK@0.10 领先 4.5 个百分点。同时，MARCO 的推理速度（8.30 FPS）是 Geo-SC 的约 10 倍，模型参数仅为其 1/3。

消融实验进一步验证了两个核心设计的决定性作用：移除密集自蒸馏损失后，SPair-U PCK@0.10 从 67.5 骤降至 41.8（**-25.7**），表明自蒸馏是泛化的关键驱动力；仅添加由粗到细目标，就将 SPair-71k PCK@0.01 从 20.0 提升至 26.8。

**方法定位**：MARCO 属于基于预训练视觉基础模型（DINOv2）的语义对应方法，与 Geo-SC（DINOv2 + 扩散模型）、Jamais Vu（3D 模板增强）等同期工作相比，其独特之处在于**完全依赖稀疏关键点监督，不引入深度图、3D 模板或推理时掩码**，通过自蒸馏机制从特征空间内部挖掘监督信号，在效率与泛化之间取得了显著优势。

## 背景与动机

### 语义对应的核心挑战

语义对应（semantic correspondence）旨在建立不同图像中同一语义部位之间的像素级映射，是视觉理解、三维重建和物体姿态估计等任务的基础。与几何匹配不同，语义对应需要跨越实例、姿态甚至类别的外观差异，在物体表面建立一致的对应关系。近年来，基于DINOv2等大规模自监督预训练特征的方法取得了显著进展，这些特征天然携带丰富的语义信息，使得零样本匹配成为可能。

然而，现有方法面临一个根本性的瓶颈：**稀疏关键点监督下的表征坍塌**。当模型在有限标注的关键点上进行微调时，虽然训练标注位置的精度得到提升，但在未标注区域的特征表示会退化，导致几何一致性被破坏。如Figure 2所示，直接在稀疏关键点上微调DINOv2会降低物体表面的流动一致性——模型学会了“记住”标注位置，却丧失了DINOv2预训练特征原有的平滑语义结构。这一现象的本质是：稀疏监督信号不足以约束整个物体表面的特征空间，模型在非标注区域缺乏引导，特征表示趋于坍塌。

### 现有方法的缺口

当前语义对应方法可大致分为两类路径：

**零样本匹配方法**（如**DINOv2+NN**）直接使用冻结的预训练特征进行最近邻匹配，无需任何标注，但精度有限，尤其在需要细粒度定位时表现不佳。这类方法完全依赖预训练特征的质量，无法针对特定任务进行适配。

**监督微调方法**则在标注数据上训练专门的对应模型。其中，对偶编码器架构（如**SD+DINOv2**和**Geo-SC**）联合DINOv2与扩散模型特征，在标准基准上取得了领先精度。然而，这些方法存在三个显著缺口：

1. **泛化能力不足**：在训练时见过的关键点类别上表现良好，但面对未见关键点或全新物体类别时精度急剧下降。例如，Geo-SC在SPair-71k标准基准上达到83.2 PCK@0.10，但在SPair-U未见关键点上的表现大幅落后于MARCO（Table 3）。
2. **计算开销巨大**：对偶编码器方法通常需要同时运行DINOv2和扩散模型两个大型骨干网络，推理速度慢（如Geo-SC仅0.85 FPS），模型体积大，限制了实际部署。
3. **监督信号稀疏**：仅依赖稀疏关键点标注进行训练，无法充分利用DINOv2特征空间中已有的丰富语义结构。同期工作**Jamais Vu**尝试通过3D模板和深度监督来缓解这一问题，但引入了额外的监督需求。

### MARCO的核心动机

MARCO的核心洞察在于：**DINOv2的预训练特征本身包含稀疏但语义一致的对应线索，这些线索可以通过互近邻挖掘和几何约束传播至整个物体表面，形成自我监督信号**。基于这一洞察，MARCO提出了一种全新的训练范式：

- **从稀疏到密集的监督扩展**：不满足于仅在标注关键点上优化，而是利用DINOv2特征空间中自然涌现的可靠匹配，通过Delaunay三角剖分、仿射致密化和流聚类，将稀疏关键点监督扩展为覆盖整个物体表面的密集对应场。
- **保持语义结构的微调**：通过由粗到细的高斯RBF损失和密集自蒸馏框架，引导模型在适配下游任务的同时，保持甚至增强预训练特征原有的几何一致性，从而在未见关键点和新类别上获得强泛化能力。
- **高效架构设计**：仅需在冻结的DINOv2骨干上添加轻量级AdaptFormer适配器和紧凑上采样头，避免了扩散模型等重计算组件，使模型体积仅为对偶编码器方法的1/3，推理速度快10倍（Figure 1d, Table 12）。

简言之，MARCO的目标是**在保持高效架构的前提下，探索稀疏标注之外的语义对应未至空间**——即那些训练时未见过的关键点位置和物体类别，通过自蒸馏机制将DINOv2的预训练语义结构转化为可泛化的精细定位能力。

## 核心创新

MARCO 的核心创新在于将语义对应的学习从“稀疏关键点回归”重新定义为“以稀疏锚点引导的密集表面流场重建”，从而系统性地解决了现有方法在未见关键点和新类别上泛化崩塌的问题。

### 1. 由粗到细的高斯 RBF 损失：从区域对齐到亚像素定位

传统方法（如 Geo-SC、GECO）使用 L2 回归或 soft-argmax + L2 直接预测关键点坐标，这迫使模型在训练初期就追求精确的像素级定位，容易陷入局部最优。MARCO 将监督信号改造为**以真值关键点为中心的高斯 RBF 交叉熵损失**：

$$\mathcal{L}_{\mathrm{sup}} = -\frac{1}{K}\sum_{i=1}^K \sum_{\mathbf{u}\in\hat{\Lambda}} G_\sigma(\mathbf{u}; \mathbf{p}_i^t) \log \operatorname{softmax} S(\mathbf{p}_i^s, \mathbf{u})$$

其中 $G_\sigma(\mathbf{u}; \mathbf{p}_i^t) \propto \exp\left(-\frac{\|\mathbf{u} - \mathbf{p}_i^t\|_2^2}{2\sigma^2}\right)$ 是带宽为 $\sigma$ 的高斯目标分布。关键创新在于**带宽 $\sigma$ 的余弦退火调度**：

$$\sigma(t) = \sigma_{\min} + \frac{1}{2}\left(\sigma_{\max} - \sigma_{\min}\right)\left(1 + \cos\left(\pi \frac{t}{T}\right)\right)$$

训练初期 $\sigma=3$，高斯核覆盖较大邻域，引导模型学习**粗粒度的区域级对齐**；随着训练推进，$\sigma$ 余弦退火至 1，目标分布逐渐锐化为尖峰，迫使模型过渡到**亚像素级精确定位**。这一机制显式解耦了“找到大致位置”与“精确定位”两个学习阶段，避免了固定带宽策略在细粒度阈值下的性能瓶颈。消融实验证实，仅添加由粗到细目标就将 SPair-71k 的 PCK@0.01 从 20.0 提升至 26.8（Table 8）。

### 2. 密集自蒸馏框架：将稀疏监督扩展为覆盖全表面的对应场

这是 MARCO 最核心的创新——**利用 DINOv2 预训练特征中固有的语义对应线索，通过几何传播与聚类锚定，自动生成密集伪对应，形成自我监督**。该框架包含四个关键步骤：

**互近邻匹配（MNN）** 在 EMA 教师网络的特征空间中，为源图像的每个块寻找目标最近邻，仅保留双向互为最近邻的可靠匹配对：

$$\mathcal{P}_{\mathrm{MNN}} = \{ (\mathbf{u}, \mathbf{v}) \mid \operatorname{NN}_{st}(\mathbf{u}) = \mathbf{v} \wedge \operatorname{NN}_{ts}(\mathbf{v}) = \mathbf{u} \}$$

这些 MNN 匹配与 GT 关键点共同构成种子对应集。

**Delaunay 致密化** 对种子对应进行 Delaunay 三角剖分，在每个三角形内通过仿射映射将离散匹配传播至所有像素，获得覆盖整个物体表面的密集流场 $\mathbf{D}(\mathbf{u})$。这一步将稀疏的“点对应”扩展为连续的“流场”，是伪标签能够覆盖非标注区域的关键。

**流聚类与 GT 锚定** 对位移向量进行 k-means 聚类，按 BIC 准则自动合并簇，识别出具有一致运动的区域。然后利用 GT 关键点作为“锚点”——仅保留那些同时包含源端和目标端 GT 关键点的流簇，从而过滤掉因对称性、遮挡或匹配错误产生的不一致流动区域：

$$\mathcal{P}_{\mathrm{self}} = \{ (\mathbf{u}, \mathbf{u} + \mathbf{D}(\mathbf{u})) \mid \exists n, (\mathbf{p}_i^s,\mathbf{p}_i^t)\in\mathcal{E}: \mathbf{u}\in C_n^s \wedge \mathbf{p}_i^s\in C_n^s \wedge \mathbf{p}_i^t\in C_n^t \}$$

**自蒸馏 L2 损失** 学生模型通过 soft-argmax 回归到这些伪标签坐标：

$$\mathcal{L}_{\mathrm{self}} = \frac{1}{|\mathcal{P}_{\mathrm{self}}|} \sum_{(\hat{\mathbf{u}}, \hat{\mathbf{v}}) \in \mathcal{P}_{\mathrm{self}}} \left\| \mathrm{soft-argmax}\big(S(\hat{\mathbf{u}}, \mathbf{u})\big) - \hat{\mathbf{v}} \right\|_2^2$$

教师参数通过 EMA 更新 $\theta_{\mathrm{T}} \leftarrow \beta \theta_{\mathrm{T}} + (1 - \beta) \theta_{\mathrm{S}}$，提供稳定的伪标签，避免训练震荡。

### 3. 轻量化架构适配：冻结骨干 + 瓶颈适配器 + 紧凑上采样头

与 Geo-SC 等对偶编码器方法（同时使用 DINOv2 和 Stable Diffusion，模型庞大且推理缓慢）不同，MARCO 坚持**极简架构**：

- **冻结 DINOv2 ViT-L/14 骨干**，保留预训练语义结构；
- 在高层 Transformer 层插入 **AdaptFormer 瓶颈适配器**：$\mathcal{A}(\mathbf{x}) = \mathrm{GELU}(\mathbf{x} \mathbf{W}_{\mathrm{down}}) \mathbf{W}_{\mathrm{up}}$，以残差形式注入可学习的任务适配能力，参数量极小；
- 添加由转置卷积和深度可分离卷积组成的**4 倍上采样头**，恢复亚块级空间细节。

这一设计使 MARCO 在保持 3 倍更小模型体积的同时，推理速度达到 8.30 FPS，是 Geo-SC（0.85 FPS）的 **9.8 倍**（Table 12）。

### 创新间的因果耦合

三个创新并非孤立叠加，而是形成因果闭环：**由粗到细损失**确保模型在稀疏标注上获得细粒度定位能力；**密集自蒸馏**利用 DINOv2 的预训练语义结构，将这种能力从标注点传播至整个物体表面，防止非标注区域的特征坍塌（Figure 2 定性展示了这一效果）；**轻量架构**则保证整个流程高效可部署。消融实验显示，移除密集自蒸馏后，SPair-U 上 PCK@0.10 从 67.5 骤降至 41.8（-25.7），而仅用 MNN 匹配不加 Delaunay 致密化时仅为 52.5（Table 4），证明几何传播与自蒸馏共同构成了泛化能力的核心驱动力。

## 整体框架

MARCO 的整体 pipeline 以冻结的 DINOv2 ViT-L/14 为特征提取骨干，在其上插入轻量可学习的适配器模块与紧凑的上采样头，构成学生网络；同时维护一个通过指数移动平均（EMA）更新的教师网络，用于生成稳定的密集伪标签。训练过程由两条互补的监督支路驱动：**（1）由粗到细的高斯 RBF 交叉熵损失**，以余弦退火策略逐步缩小目标分布的带宽，引导学生从区域级对齐过渡到亚像素级精确定位；**（2）密集自蒸馏损失**，利用教师特征空间中的互近邻匹配挖掘可靠对应种子，经 Delaunay 三角剖分致密化、流聚类与 GT 关键点锚定，生成覆盖整个物体表面的密集伪对应，学生通过 soft-argmax 回归到这些伪标签，从而将稀疏关键点监督扩展为平滑的对应场。

### 特征提取与增强

给定源图像 $\mathbf{I}^s$ 和目标图像 $\mathbf{I}^t$，首先通过冻结的 DINOv2 骨干提取多尺度 token 特征。在高层 Transformer 层中插入 AdaptFormer 瓶颈适配器，对每个 token 执行可学习的降维-激活-升维变换：

$$\mathcal{A}(\mathbf{x}) = \mathrm{GELU}(\mathbf{x} \mathbf{W}_{\mathrm{down}}) \mathbf{W}_{\mathrm{up}}$$

适配器以残差形式集成到注意力与 MLP 之后：

$$\mathbf{x}_{\mathrm{self}} = \mathrm{Attention}(\mathbf{x}), \quad \mathbf{x}' = \mathrm{MLP}(\mathbf{x}_{\mathrm{self}}) + \mathbf{x}_{\mathrm{self}} + \mathcal{A}(\mathbf{x}_{\mathrm{self}})$$

随后，一个由 $2\times2$ 转置卷积与 $3\times3$ 深度可分离卷积组成的上采样头将特征分辨率提升 4 倍，恢复亚块级空间细节：

$$\mathbf{F}_1 = \mathrm{ConvTranspose}_{2\times2}(\mathbf{F}), \quad \hat{\mathbf{F}} = \mathrm{DepthwiseConv}_{3\times3}(\mathrm{GELU}(\mathbf{F}_1))$$

最终得到增强后的源特征图 $\hat{\mathbf{F}}^s$ 与目标特征图 $\hat{\mathbf{F}}^t$，用于后续的对应匹配。

### 由粗到细的监督损失

对于每个标注关键点，以真值坐标 $\mathbf{p}_i^t$ 为中心构建高斯 RBF 目标分布：

$$G_\sigma(\mathbf{u}; \mathbf{p}_i^t) \propto \exp\left(-\frac{\|\mathbf{u} - \mathbf{p}_i^t\|_2^2}{2\sigma^2}\right)$$

源描述子 $\hat{\mathbf{F}}^s[\mathbf{p}_i^s]$ 在目标特征网格上的余弦相似度经 softmax 归一化后，通过交叉熵损失与高斯目标对齐：

$$\mathcal{L}_{\mathrm{sup}} = -\frac{1}{K}\sum_{i=1}^K \sum_{\mathbf{u}\in\hat{\Lambda}} G_\sigma(\mathbf{u}; \mathbf{p}_i^t) \log \operatorname{softmax} S(\mathbf{p}_i^s, \mathbf{u})$$

关键创新在于带宽 $\sigma$ 的调度策略——采用余弦退火从 $\sigma_{\max}=3$ 逐步降至 $\sigma_{\min}=1$：

$$\sigma(t) = \sigma_{\min} + \frac{1}{2}\left(\sigma_{\max} - \sigma_{\min}\right)\left(1 + \cos\left(\pi \frac{t}{T}\right)\right)$$

早期大带宽迫使模型学习区域级语义对齐，后期窄带宽驱动亚像素级精确定位，有效平衡了收敛稳定性与细粒度精度。

### 密集自蒸馏支路

为克服稀疏监督导致的非标注区域特征坍塌，MARCO 引入一条无需额外人工标注的自蒸馏支路。教师网络的参数通过学生参数的 EMA 更新：

$$\theta_{\mathrm{T}} \leftarrow \beta \theta_{\mathrm{T}} + (1 - \beta) \theta_{\mathrm{S}}$$

在教师特征空间中，首先通过互近邻（MNN）匹配挖掘可靠的对应种子：

$$\mathcal{P}_{\mathrm{MNN}} = \{ (\mathbf{u}, \mathbf{v}) \mid \operatorname{NN}_{st}(\mathbf{u}) = \mathbf{v} \wedge \operatorname{NN}_{ts}(\mathbf{v}) = \mathbf{u} \}$$

将 MNN 种子与 GT 关键点合并为种子集 $\mathcal{P}_{\mathrm{seed}}$，并限制在 SAM 物体掩码内。随后对种子点进行 Delaunay 三角剖分，在每个三角形内通过仿射映射将离散匹配传播为覆盖整个物体表面的密集流场 $\mathbf{D}(\mathbf{u})$。对流向量进行 k-means 聚类，按 BIC 准则自动合并簇，并利用 GT 关键点作为锚点筛选出几何一致的流簇——仅保留同时包含源端和目标端 GT 关键点的对应区域：

$$\mathcal{P}_{\mathrm{self}} = \{ (\mathbf{u}, \mathbf{u} + \mathbf{D}(\mathbf{u})) \mid \exists n, (\mathbf{p}_i^s,\mathbf{p}_i^t)\in\mathcal{E}: \mathbf{u}\in C_n^s \wedge \mathbf{p}_i^s\in C_n^s \wedge \mathbf{p}_i^t\in C_n^t \}$$

学生模型通过 soft-argmax 预测坐标，并与伪标签之间计算 L2 回归损失：

$$\mathcal{L}_{\mathrm{self}} = \frac{1}{|\mathcal{P}_{\mathrm{self}}|} \sum_{(\hat{\mathbf{u}}, \hat{\mathbf{v}}) \in \mathcal{P}_{\mathrm{self}}} \left\| \mathrm{soft-argmax}\big(S(\hat{\mathbf{u}}, \mathbf{u})\big) - \hat{\mathbf{v}} \right\|_2^2$$

最终训练目标为 $\mathcal{L} = \mathcal{L}_{\mathrm{sup}} + \lambda \mathcal{L}_{\mathrm{self}}$，两条支路协同作用：监督损失提供精确的关键点定位信号，自蒸馏损失将稀疏监督扩展为覆盖整个物体表面的几何一致对应场，从而在保持高效架构的同时实现强泛化。

### 补充图表

![[assets/figures/papers/paper_list_l30_https_arxiv_org_abs_2604_18267/figures/003_Figure_3.jpg]]
*Figure 3: Overview of MARCO. We insert lightweight adapters into DINOv2 and add a compact upsampling layer (red). At training time, we propose a coarse-to-fine Gaussian RBF loss that progressively sharpens peaks on annotated keypoints and a self-distillation objective that exploits the pre-existing structure of DINOv2 features. Given source and target images, we extract features from an EMA teacher and identify reliable mutual nearest-neighbor matches (a). These sparse correspondences are densified via piecewise-affine interpolation over a Delaunay triangulation, producing an initial flow field (b). Coherent motion regions are then obtained by clustering in the displacement space and anchored to spar...*

## 核心模块与公式推导

### 架构设计：冻结骨干 + 轻量适配

MARCO 的架构建立在冻结的 DINOv2 ViT-L/14 预训练骨干之上，仅引入两类可学习模块（Fig. 3），参数开销极小。

**AdaptFormer 适配器** 插入到高层 Transformer 层中，以残差形式增强特征表示。每个适配器对 token 独立操作，由可学习的降维投影 $\mathbf{W}_{\mathrm{down}} \in \mathbb{R}^{D \times d}$ 和升维投影 $\mathbf{W}_{\mathrm{up}} \in \mathbb{R}^{d \times D}$ 构成瓶颈结构：

$$
\mathcal{A}(\mathbf{x}) = \mathrm{GELU}(\mathbf{x} \mathbf{W}_{\mathrm{down}}) \mathbf{W}_{\mathrm{up}}
$$

适配器以残差方式集成到注意力与 MLP 之后：

$$
\mathbf{x}_{\mathrm{self}} = \mathrm{Attention}(\mathbf{x}), \quad \mathbf{x}' = \mathrm{MLP}(\mathbf{x}_{\mathrm{self}}) + \mathbf{x}_{\mathrm{self}} + \mathcal{A}(\mathbf{x}_{\mathrm{self}})
$$

**上采样头** 将特征分辨率提升 4 倍，恢复亚块级空间细节。先通过 $2 \times 2$ 转置卷积进行 2 倍上采样，再经 GELU 激活和 $3 \times 3$ 深度可分离卷积精细增强：

$$
\mathbf{F}_1 = \mathrm{ConvTranspose}_{2\times2}(\mathbf{F}), \quad \hat{\mathbf{F}} = \mathrm{DepthwiseConv}_{3\times3}(\mathrm{GELU}(\mathbf{F}_1))
$$

### 相似度计算与坐标预测

给定源图像块 $\mathbf{p}_i^s$ 和目标特征网格上的位置 $\mathbf{u}$，相似度图通过余弦相似度计算：

$$
S(\mathbf{p}_i^s, \mathbf{u}) = \langle \hat{\mathbf{F}}^s[\mathbf{p}_i^s], \hat{\mathbf{F}}^t[\mathbf{u}] \rangle
$$

最终关键点坐标由 soft-argmax 从相似度图中回归得到（原文 Eq. 6 附近描述，具体 soft-argmax 公式见推理部分）。

### 由粗到细的高斯 RBF 监督损失

传统 L2 回归直接优化坐标，对细粒度定位不敏感。MARCO 将监督信号建模为以真值关键点 $\mathbf{p}_i^t$ 为中心、带宽 $\sigma$ 的高斯目标分布：

$$
G_\sigma(\mathbf{u}; \mathbf{p}_i^t) \propto \exp\left(-\frac{\|\mathbf{u} - \mathbf{p}_i^t\|_2^2}{2\sigma^2}\right)
$$

监督损失为 softmax 相似度图与高斯目标之间的交叉熵，优化分布匹配而非点回归：

$$
\mathcal{L}_{\mathrm{sup}} = -\frac{1}{K}\sum_{i=1}^K \sum_{\mathbf{u}\in\hat{\Lambda}} G_\sigma(\mathbf{u}; \mathbf{p}_i^t) \log \operatorname{softmax} S(\mathbf{p}_i^s, \mathbf{u})
$$

**由粗到细调度** 是该方法的核心机制。带宽 $\sigma$ 按余弦退火从 $\sigma_{\max}=3$ 逐步降至 $\sigma_{\min}=1$，引导模型从粗粒度区域对齐过渡到亚像素级精确定位：

$$
\sigma(t) = \sigma_{\min} + \frac{1}{2}\left(\sigma_{\max} - \sigma_{\min}\right)\left(1 + \cos\left(\pi \frac{t}{T}\right)\right)
$$

### 密集自蒸馏框架

自蒸馏的核心思路是利用 DINOv2 特征空间中已有的语义结构，从稀疏标注扩展出密集伪对应。

**互近邻匹配** 在教师特征空间中寻找可靠对应种子。给定源块 $\mathbf{u}$，其目标最近邻为：

$$
\operatorname*{NN}_{st}(\mathbf{u}) = \arg\max_{\mathbf{v}\in\hat{\Lambda}} \langle \mathbf{F}_T^s[\mathbf{u}], \mathbf{F}_T^t[\mathbf{v}] \rangle
$$

互近邻集合 $\mathcal{P}_{\mathrm{MNN}}$ 要求源和目标互为最近邻，过滤单向匹配的噪声：

$$
\mathcal{P}_{\mathrm{MNN}} = \{ (\mathbf{u}, \mathbf{v}) \mid \operatorname{NN}_{st}(\mathbf{u}) = \mathbf{v} \wedge \operatorname{NN}_{ts}(\mathbf{v}) = \mathbf{u} \}
$$

**Delaunay 致密化** 将离散种子扩展为连续流场。对种子对应进行 Delaunay 三角剖分，在每个三角形内通过仿射映射插值，得到密集位移图：

$$
\mathbf{u} \mapsto \mathbf{D}(\mathbf{u}) = \hat{\mathcal{W}}(\mathbf{u}) - \mathbf{u}
$$

**流聚类与 GT 锚定** 消除致密化引入的错误匹配。对位移向量 $\mathbf{D}(\mathbf{u})$ 进行 k-means 聚类，按 BIC 准则自动合并簇。每个簇定义源区域 $C_n^s$ 和目标区域 $C_n^t$：

$$
C_n^s = \{ \mathbf{u} \mid \mathbf{D}(\mathbf{u}) \in \Omega_n \}, \quad C_n^t = \{ \mathbf{u} + \mathbf{D}(\mathbf{u}) \mid \mathbf{u} \in C_n^s \}
$$

仅保留同时包含 GT 关键点对的流簇中的伪对应，作为最终自蒸馏伪标签 $\mathcal{P}_{\mathrm{self}}$：

$$
\mathcal{P}_{\mathrm{self}} = \{ (\mathbf{u}, \mathbf{u} + \mathbf{D}(\mathbf{u})) \mid \exists n, (\mathbf{p}_i^s,\mathbf{p}_i^t)\in\mathcal{E}: \mathbf{u}\in C_n^s \wedge \mathbf{p}_i^s\in C_n^s \wedge \mathbf{p}_i^t\in C_n^t \}
$$

**教师网络** 由学生参数的指数移动平均更新，提供稳定的伪标签：

$$
\theta_{\mathrm{T}} \leftarrow \beta \theta_{\mathrm{T}} + (1 - \beta) \theta_{\mathrm{S}}
$$

**自蒸馏损失** 为学生预测坐标与伪标签之间的 L2 回归：

$$
\mathcal{L}_{\mathrm{self}} = \frac{1}{|\mathcal{P}_{\mathrm{self}}|} \sum_{(\hat{\mathbf{u}}, \hat{\mathbf{v}}) \in \mathcal{P}_{\mathrm{self}}} \left\| \mathrm{soft\text{-}argmax}\big(S(\hat{\mathbf{u}}, \mathbf{u})\big) - \hat{\mathbf{v}} \right\|_2^2
$$

总训练损失为 $\mathcal{L} = \mathcal{L}_{\mathrm{sup}} + \lambda \mathcal{L}_{\mathrm{self}}$，其中 $\lambda$ 平衡稀疏监督与密集自蒸馏。

### 补充图表

![[assets/figures/papers/paper_list_l30_https_arxiv_org_abs_2604_18267/figures/002_Figure_2.jpg]]
*Figure 2: Flow consistency in DINOv2. Semantic flow (in HSV space) from raw feature matches between two objects. Fine-tuning on sparse keypoints improves only the landmarks’ representation, reducing geometric coherence (b). Our self-supervised objective produces smooth, object-consistent flow across the surface (c)*

## 实验与分析

### 核心瓶颈与方法对应

语义对应任务的核心瓶颈在于：基于稀疏关键点监督的模型虽然在训练标注上表现良好，但一旦遇到**未见关键点**或**新类别**，精度便急剧下降。其根源在于模型过度拟合有限的标注位置，导致非标注区域的特征表示坍塌，破坏了物体表面的几何一致性（Figure 2b）。MARCO 通过两个核心机制应对这一瓶颈：

1. **由粗到细的高斯RBF损失**：以余弦退火逐步缩小目标分布带宽 $\sigma$，引导模型从区域对齐过渡到亚像素级精确定位。
2. **密集自蒸馏框架**：利用 DINOv2 特征空间中互近邻匹配的语义一致性，经过 Delaunay 三角剖分、仿射致密化和流聚类，生成覆盖物体表面的密集伪对应，并以 GT 关键点为锚点过滤错误匹配，将稀疏监督扩展为平滑的对应场。

### 标准基准结果

Table 1 展示了 MARCO 在 SPair-71k、AP-10K 和 PF-PASCAL 三个标准基准上的性能。MARCO 在所有阈值下均达到最优，尤其在严格阈值上优势显著：

![[assets/figures/papers/paper_list_l30_https_arxiv_org_abs_2604_18267/figures/006_Table_1.jpg]]
*Table 1: Evaluation on standard benchmarks. Per-image PCK (%, ↑) at multiple thresholds on SPair-71k, AP-10K (intra-, cross-species, and cross-family), and PF-PASCAL. Best results bold, 2nd best underlined. § uses depth maps at training; † uses object masks at training; ‡ uses object masks at inference. For MARCO, we report two variants, with and without restricting pixels to object masks during training. MARCO, built solely on DINOv2, sets a new state of the art, with strong gains at challenging fine-grained thresholds (PCK@0.01)*

- **SPair-71k**：PCK@0.10 达到 87.2%，较此前最强的 **Geo-SC**（83.2%）提升 +4.0 个百分点；在更严苛的 PCK@0.01 阈值上，MARCO 达到 27.0%，较 Geo-SC（21.7%）提升 +5.3 个百分点。若在训练时使用 SAM 物体掩码，PCK@0.01 进一步提升至 27.0%（Table 1）。
- **AP-10K**：在跨物种（cross-species）和跨科（cross-family）设定下，MARCO 的 PCK@0.01 分别达到 32.2% 和 28.5%，较 Geo-SC 提升 +3.0 和 +2.2 个百分点。
- **PF-PASCAL**：PCK@0.05 达到 91.1%，同样位居榜首。

这些结果表明，MARCO 的由粗到细监督和特征上采样设计显著增强了细粒度定位能力，而不仅仅是在宽松阈值下取得表面提升。

### 泛化能力：未见关键点与未见类别

语义对应方法的真正考验在于对训练分布外样本的泛化。Table 3 和 Table 2 分别报告了在 SPair-U（未见关键点）和 MP-100（未见关键点与未见类别）上的结果。

![[assets/figures/papers/paper_list_l30_https_arxiv_org_abs_2604_18267/figures/007_Table_2.jpg]]
*Table 2: Generalization on MP-100 [48]. Per-image PCK@0.10 (%, ↑) across unseen keypoints and semantic unseen categories. ∗ unsupervised methods. Best results bold, 2nd best underlined*

![[assets/figures/papers/paper_list_l30_https_arxiv_org_abs_2604_18267/figures/008_Table_3.jpg]]
*Table 3: Generalization on SPair-U (Unseen keypoints) in terms of per-image PCK@0.10 (in %, ↑). Methods marked with ∗ are unsupervised. All methods are trained on SPair-71k. Best results are shown in bold; 2nd best are underlined*

- **SPair-U**：MARCO 的 PCK@0.10 达到 67.5%，较同期工作 **Jamais Vu**（62.4%）提升 +5.1 个百分点，较 Geo-SC（53.4%）提升 +14.1 个百分点。值得注意的是，Jamais Vu 依赖额外的单目深度监督和 3D 模板，而 MARCO 仅使用稀疏关键点监督即实现了更强的泛化。
- **MP-100 未见关键点**：在服装（Apparel）类别上，MARCO 的 PCK@0.10 达到 55.9%，较 Jamais Vu（45.7%）提升 +10.2 个百分点；在动物身体（Animal body）类别上达到 42.3%，较 Jamais Vu（39.3%）提升 +3.0 个百分点。
- **MP-100 未见类别**：MARCO 的平均 PCK@0.10 比先前最强方法高出 +4.5%（Table 14），体现出跨类别、跨域的鲁棒泛化能力。

这些提升的核心驱动力来自密集自蒸馏——它迫使模型学习覆盖整个物体表面的平滑对应场，而非仅记忆稀疏关键点位置。

### 消融实验：各组件的因果贡献

Table 4 和 Table 8 通过系统消融揭示了各组件的独立贡献。

![[assets/figures/papers/paper_list_l30_https_arxiv_org_abs_2604_18267/figures/009_Table_4.jpg]]
*Table 4: Ablation studies. Per-image PCK (%, ↑) on SPair-71k and SPair-U. SPair-71k evaluates the effect of architecture and sparse supervision, whereas SPair-U (unseen keypoints) analyzes the generalization effect of our dense self-supervision. Each component group is assessed independently, keeping the others fixed*

![[assets/figures/papers/paper_list_l30_https_arxiv_org_abs_2604_18267/figures/013_Table_8.jpg]]
*Table 8: Ablation of architectural and training components. Per-image PCK (in %, ↑) on SPair-71k (seen keypoints) and SPair-U (unseen keypoints). Adapters and feature upsampling are added to a frozen DINOv2 backbone, while training objectives progressively include standard supervision*

**密集自蒸馏**是最关键的泛化驱动力。移除该损失后，SPair-U 的 PCK@0.10 从 67.5% 骤降至 41.8%（-25.7），几乎回退到仅用稀疏监督的水平。这直接证明了自蒸馏生成的密集伪标签对未见关键点泛化的决定性作用。

**Delaunay 致密化**是伪标签质量的关键。若仅使用互近邻（MNN）匹配而不进行 Delaunay 三角剖分和仿射致密化，SPair-U 的 PCK@0.10 从 64.7% 降至 52.5%（-12.2）。这说明 MNN 匹配虽然可靠，但过于稀疏，必须通过几何传播才能覆盖整个物体表面。

**紧凑上采样头**对细粒度定位至关重要。添加 4 倍特征上采样头后，SPair-71k 的 PCK@0.01 和 PCK@0.10 分别提升 +12.6 和 +10.3 个百分点（Table 4）。这表明恢复亚块级空间细节是亚像素精度匹配的必要条件。

**AdaptFormer 适配器**在域内精度和泛化之间取得了最佳平衡。Table 7 显示，采用 AdaptFormer 适配器（SPair-U PCK@0.10 = 67.5%）显著优于全微调（43.9%）和冻结骨干（较低基线），同时保持了域内性能。适配器插入高层 Transformer 层、瓶颈维度选择中等大小时效果最优。

**由粗到细的余弦退火**策略在细粒度阈值下明显优于固定带宽策略，同时保持了较粗阈值的竞争力（Section 4.3, Table 1）。仅添加该目标就将 SPair-71k 的 PCK@0.01 从 20.0% 提升至 26.8%（Table 8），验证了从区域对齐逐步过渡到精确定位的必要性。

### 自蒸馏框架的通用性与鲁棒性

Table 5 验证了密集自蒸馏损失的通用性：将 MARCO 的自蒸馏目标应用于 **Geo-SC** 模型后，其在 SPair-U 上的 PCK@0.10 从 53.4% 提升至 60.1%（+6.7），证明该策略不依赖于特定架构，可作为即插即用的泛化增强模块。

![[assets/figures/papers/paper_list_l30_https_arxiv_org_abs_2604_18267/figures/010_Table_5.jpg]]
*Table 5: General applicability of our self-distillation loss. By training the state-of-the-art Geo-SC model with our dense selfdistillation objective, we markedly improve its generalization to unseen keypoints on SPair-U. In MARCO, we integrate this objective with a coarse-to-fine supervised loss, reaching state-of-the-art results while being smaller and faster. Per-image PCK (in %, ↑) on SPair-71k, and SPair-U (unseen keypoints); models trained on SPair-71k. Best results bold, 2nd best underlined*

Table 9 评估了伪标签噪声的容忍度：向伪标签坐标添加标准差 $\sigma$ 的高斯噪声后，SPair-U 性能在 $\sigma \approx 10$ 像素处开始显著退化，表明 MARCO 对适度噪声具有鲁棒性，但伪标签的精确度仍是性能保障。

![[assets/figures/papers/paper_list_l30_https_arxiv_org_abs_2604_18267/figures/014_Table_9.jpg]]
*Table 9: Pseudo-label noise estimation. SPair-U PCK@0.10 (%, ↑) when Gaussian noise with standard deviation σ (px) is added to pseudo-label coordinates. Performance degrades near σ=10*

Table 10 分析了流聚类对初始簇数 $k$ 的敏感性：初始化为较大的 $k$ 并使用 BIC 准则自动合并，可获得最佳结果，避免了手动调参的需求。

![[assets/figures/papers/paper_list_l30_https_arxiv_org_abs_2604_18267/figures/015_Table_10.jpg]]
*Table 10: Clustering sensitivity. Performance on SPair-U (PCK@0.10, in %, ↑) for different initial numbers of clusters k. Initializing with a larger k and merging clusters using BIC yields the best result, avoiding the need to tune k*

### 效率对比

Table 12 报告了模型规模和推理速度。MARCO 在 RTX 4090 GPU 上达到 8.30 FPS，而 **Geo-SC** 和 **Jamais Vu** 仅为 0.85 FPS，加速约 9.8 倍。同时，MARCO 的参数量约为对偶编码器方法的三分之一。这一效率优势源于其极简架构设计：仅依赖单个 DINOv2 骨干加轻量适配器，无需扩散模型或多模态编码器。

![[assets/figures/papers/paper_list_l30_https_arxiv_org_abs_2604_18267/figures/017_Table_12.jpg]]
*Table 12: Compute comparison. Model size and inference speed measured on an RTX4090 GPU. All methods use the same evaluation protocol: feature extraction at 840p, batched reference–target pairs, and the same soft-argmax keypoint prediction*

### 失败模式与局限性

尽管 MARCO 在多数场景下表现优异，仍存在以下已知局限：

1. **严重遮挡与对称物体**：伪标签质量依赖于互近邻匹配的准确性。在严重遮挡或高度对称的物体上，即使使用 GT 锚定，流聚类仍可能保留错误流动区域，导致自蒸馏信号含噪。
2. **无掩码设定下的背景噪声**：训练流程默认使用 SAM 物体掩码过滤背景。Table 11 显示，完全不使用掩码时性能仍具竞争力，但伪标签可能引入更多背景噪声，在复杂背景场景下精度有所下降。
3. **基础模型依赖性**：当前方法基于 DINOv2 ViT-L 架构验证，尚未在其他基础模型（如 MAE、DINOv1）或更轻量骨干上测试迁移效果。由粗到细退火策略是否对更小模型同样最优，需进一步评估。

### 开放问题

- Delaunay 三角剖分在严重遮挡下的失效模式如何定量影响最终对应质量？是否存在更鲁棒的插值策略（如基于图神经网络的传播）？
- 自蒸馏伪标签在物体边界和低纹理区域的覆盖率和噪声分布特性如何？能否进一步减少对 GT 锚定的依赖，甚至实现完全无监督的密集对应学习？
- 适配器放置位置和瓶颈维度的最优选择是否对不同视觉基础模型具有普适性？

### 补充图表

![[assets/figures/papers/paper_list_l30_https_arxiv_org_abs_2604_18267/figures/011_Table_7.jpg]]
*Table 7: Additional ablations comparing fine-tuning vs. adaptation strategies, adapter placement, and bottleneck dimension. All results reported as PCK@0.10 (in %, ↑)*

## 方法谱系与知识库定位

### 1. 在语义对应研究中的位置

MARCO处于**稀疏监督语义对应**（sparse supervised semantic correspondence）这一研究脉络中。该领域的核心瓶颈长期存在：基于稀疏关键点标注训练的方法在训练分布内表现良好，但泛化到未见关键点和新类别时精度急剧下降。MARCO直面这一挑战，通过密集自蒸馏将稀疏监督扩展为覆盖整个物体表面的平滑对应场，从而在保持高效架构的同时实现强泛化。

从方法演进角度看，MARCO可被视为**从“对偶编码器+扩散模型”范式向“单编码器+自蒸馏”范式**的转向节点：

- **前序对偶编码器方法**：**Geo-SC**（当前领先的DINOv2+扩散对偶编码器方法）通过联合DINOv2和Stable Diffusion特征获得强表示，但推理需依赖物体掩码且计算开销大（0.85 FPS）。**SD+DINOv2**同样采用对偶编码器设计。MARCO证明，仅凭单个DINOv2编码器配合适配器微调和密集自蒸馏，即可在精度上超越这些对偶方法（SPair-71k PCK@0.01: +5.3 vs Geo-SC），同时模型缩小3倍、推理加速10倍（8.30 FPS）。

- **同期泛化工作**：**Jamais Vu**通过引入单目深度监督和3D模板来提升未见关键点泛化，在SPair-U上达到62.4 PCK@0.10。MARCO不使用任何深度或3D信息，仅凭2D自蒸馏即达到67.5（+5.1），表明**几何约束可从预训练特征空间中自挖掘**，无需外部3D先验。

- **基于最优传输的方法**：**GECO**采用类别感知关键点和最优传输进行监督。MARCO的密集自蒸馏在思路上与最优传输有相通之处（均追求全局一致的对应分配），但实现路径不同：MARCO通过互近邻匹配→Delaunay致密化→流聚类→GT锚定的管道生成伪标签，避免了显式求解传输问题的高计算成本。

- **零样本基线**：**DINOv2+NN**（冻结DINOv2特征+最近邻匹配）作为零样本基线，揭示了预训练特征本身已蕴含稀疏但语义一致的对应线索。MARCO的核心洞察正是将这些线索通过几何约束传播至整个物体区域，形成自我监督。

### 2. 技术贡献的边界与适用条件

MARCO的技术贡献可分解为三个独立可复用的模块，各有其适用边界：

**（1）由粗到细的高斯RBF损失**
- **机制**：通过余弦退火将高斯目标分布的带宽σ从3逐步降至1，引导模型从区域对齐过渡到亚像素级精确定位。
- **适用边界**：该策略在SPair-71k的严格阈值PCK@0.01上带来+6.8的显著提升（Table 8），但在高度可变形物体（如服装类别）上的最优退火调度尚未充分验证。当物体形变超出训练分布时，固定带宽策略可能在某些阈值下更稳健。

**（2）密集自蒸馏框架**
- **机制**：利用教师EMA网络在DINOv2特征空间中挖掘互近邻匹配，经Delaunay三角剖分和仿射致密化生成密集流场，再通过k-means聚类和GT关键点锚定过滤错误匹配。
- **适用条件**：
  - 伪标签质量依赖初始互近邻匹配的准确性——在严重遮挡或高度对称物体上，即使使用GT锚定仍可能出现错误对应。
  - 训练流程需要目标掩码（或边界框）来限制种子对应区域；完全无掩码设定下伪标签可能引入更多背景噪声。
  - 框架尚未验证在DINOv2之外的基础模型（如DINOv1、MAE）上的迁移效果。

**（3）轻量适配器架构**
- **机制**：在冻结DINOv2高层Transformer层中插入AdaptFormer瓶颈适配器，配合转置卷积+深度可分离卷积的4倍上采样头。
- **适用边界**：适配器放置位置和瓶颈维度选择针对ViT-L/14优化；对于更小模型或不同架构的ViT，最优配置需重新验证。

### 3. 局限性与已知失效模式

**（1）几何插值的脆弱性**
Delaunay三角剖分在严重遮挡情况下可能产生退化三角形，导致仿射映射在遮挡边界处产生不连续的流场。Figure 4的流聚类锚定机制可部分缓解此问题，但当遮挡区域同时缺少GT关键点时，该区域的自蒸馏信号将完全失效。

**（2）对称性混淆**
对于高度对称的物体（如正面人脸、对称图案的服装），互近邻匹配可能将源点错误匹配到对称位置。GT锚定通过要求流簇同时包含正确的GT关键点对来过滤此类错误，但若对称区域的GT关键点恰好也满足约束，错误对应仍会保留。

**（3）低纹理区域的覆盖不足**
DINOv2特征在低纹理或重复纹理区域的判别力下降，导致互近邻匹配稀疏甚至缺失。这些区域的伪标签覆盖率较低，模型可能在这些位置保持接近冻结特征的状态，精细定位能力受限。

**（4）对SAM掩码的软依赖**
训练中使用SAM掩码过滤背景种子点，尽管Table 11显示不使用掩码时精度仍具竞争力，但完全无掩码设定下背景噪声可能降低伪标签质量，尤其是在源图像和目标图像的背景纹理相似时。

### 4. 开放问题

1. **跨基础模型的通用性**：密集自蒸馏框架能否在DINOv1、MAE、或未来更大规模的视觉基础模型上复现类似的泛化增益？适配器的最优插入位置和瓶颈维度是否具有跨架构的普适性？

2. **完全无监督的语义对应**：当前方法仍需稀疏关键点作为锚点和监督信号。能否将密集自蒸馏推广到完全无监督设定，仅凭预训练特征中的互近邻结构实现语义对应？这需要解决无GT锚定条件下的错误匹配过滤问题。

3. **高可变形物体的退火策略**：由粗到细的余弦退火在刚性或半刚性物体上效果显著，但在服装等高度可变形类别上的收敛行为尚未充分研究。是否需要类别自适应的退火调度？

4. **Delaunay插值的替代方案**：在严重遮挡或极端视角变化下，Delaunay三角剖分的退化模式如何定量影响最终对应质量？是否存在更鲁棒的插值策略（如基于学习的致密化模块）？

5. **伪标签噪声的精细刻画**：Table 9通过添加高斯噪声模拟伪标签误差，但真实伪标签噪声在物体边界和低纹理区域的空间分布可能高度非均匀。更精细的噪声建模可能指导自适应损失加权策略。

6. **与3D先验的潜在协同**：MARCO证明2D自蒸馏即可超越使用3D模板的Jamais Vu，但2D自蒸馏与3D先验是否互补？两者结合能否在极端视角变化下进一步提升鲁棒性？

## 原文 PDF

![[paperPDFs/CVPR_2026/MARCO_Navigating_the_Unseen_Space_of_Semantic_Correspondence.pdf]]
