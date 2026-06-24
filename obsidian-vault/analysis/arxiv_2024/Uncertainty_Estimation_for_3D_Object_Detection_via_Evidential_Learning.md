---
title: Uncertainty Estimation for 3D Object Detection via Evidential Learning
type: paper
paper_level: A
venue: arXiv
year: 2024
pdf_ref: paperPDFs/arxiv_2024/Uncertainty_Estimation_for_3D_Object_Detection_via_Evidential_Learning.pdf
aliases:
- EDL3ODU
- UE3ODEL
tags:
- arxiv_2024
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
core_operator: 将检测器BEV热图头替换为证据深度学习（EDL）头，同时输出类别存在概率和不确定性参数（α, β），并设计结合高斯焦点损失加权的EDL损失函数及KL正则化，使模型在单次前向传播中同时获得类别、定位及场景级不确定性。
primary_logic: EDL在BEV热图上建模二阶分布，通过联合预测对象存在概率和不确定性，可以在低计算开销下检测分布外场景、评估定位质量并发现漏检目标；配合正则化防止过自信，有效提升自动标注管线的检测指标。
claims:
- 在nuScenes vs Waymo场景分布外检测中，本方法平均ROC-AUC达0.6594，比次优方法提升0.09；PR-AUC达0.6696，提升0.16。
- 在检测错误定位框的任务中，本方法平均ROC-AUC达0.6235，比次优方法提升0.06；PR-AUC达0.3634，提升0.02。
- 在漏检目标检测中，本方法在2m距离F1-score达0.0989，显著优于其他不确定性基线。
- 基于不确定性验证的自动标注管线使下游检测器mAP提升约1%，NDS提升1-2%。
---

# Uncertainty Estimation for 3D Object Detection via Evidential Learning

> [!tip] 核心洞察
> EDL在BEV热图上建模二阶分布，通过联合预测对象存在概率和不确定性，可以在低计算开销下检测分布外场景、评估定位质量并发现漏检目标；配合正则化防止过自信，有效提升自动标注管线的检测指标。

| 字段 | 内容 |
|------|------|
| 中文题名 | 基于证据学习的3D目标检测不确定性估计 |
| 英文题名 | Uncertainty Estimation for 3D Object Detection via Evidential Learning |
| 会议/期刊 | arXiv 2024 |
| Links | [paper](https://arxiv.org/abs/2410.23910) · [Code](https://github.com/open-mmlab/mmdetection3d) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction |
| Method | Evidential Deep Learning for 3D Object Detection Uncertainty |
| Dataset | nuScenes vs Waymo OOD detection, nuScenes erroneous box detection (IoU<0.3) — FF(L) model, nuScenes missed object detection (2m, FF(L)), nuScenes auto-labeling 10k budget (FF(L)) |

> [!tip] 效果简介
> - nuScenes vs Waymo OOD detection 上，ROC-AUC (average across models) 0.6594 vs 0.5685 (Deep Ensembles) (+0.0909)。
> - nuScenes erroneous box detection (IoU<0.3) — FF(L) model 上，ROC-AUC 0.6329 vs 0.5923 (Deep Ensembles) (+0.0406)。
> - nuScenes missed object detection (2m, FF(L)) 上，F1-score 0.0989 vs highest among competitors (see Tab. 3) (~0.03 improvement)。

## 概述

**问题瓶颈**：现有3D目标检测器缺乏高效可靠的不确定性估计机制，难以量化分布外场景、定位误差和漏检的置信度。传统采样式不确定性方法（如MC-Dropout、Deep Ensembles）计算开销大，不适用于实时自动驾驶系统。

**核心方法**：本文提出将检测器的BEV热图头替换为证据深度学习（EDL）头，同时输出类别存在概率和不确定性参数（α, β），并设计结合高斯焦点损失加权的EDL损失函数及KL正则化，使模型在单次前向传播中同时获得类别、定位及场景级不确定性。

**关键洞察**：EDL在BEV热图上建模二阶分布，通过联合预测对象存在概率和不确定性，可以在低计算开销下检测分布外场景、评估定位质量并发现漏检目标；配合正则化防止过自信，有效提升自动标注管线的检测指标。

**主要结果**：
- 在nuScenes vs Waymo场景分布外检测中，本方法平均ROC-AUC达0.6594，比次优方法提升0.09；PR-AUC达0.6696，提升0.16（Table 1）。
- 在检测错误定位框的任务中，本方法平均ROC-AUC达0.6235，比次优方法提升0.06；PR-AUC达0.3634，提升0.02（Table 2）。
- 在漏检目标检测中，本方法在2m距离F1-score达0.0989，显著优于其他不确定性基线（Table 3）。
- 基于不确定性验证的自动标注管线使下游检测器mAP提升约1%，NDS提升1–2%（Table 4）。

**方法定位**：本方法属于不确定性估计与3D目标检测的交叉领域，通过轻量级EDL头替代传统热图头，在不增加推理开销的前提下实现多层级不确定性量化，并与**FocalFormer3D**（Chen et al., ICCV 2023）和**DeformFormer3D**（Zhu et al., ICLR 2021）等主流检测器架构兼容。相较于**MC-Dropout**（Gal & Ghahramani, ICML 2016）、**Deep Ensembles**（Lakshminarayanan et al., NeurIPS 2017）、**BatchEnsemble**（Wen et al., ICLR 2020）、**Masksembles**（Durasov et al., CVPR 2021）和**Packed-Ensembles**（Laurent et al., ICLR 2023）等采样式或集成式不确定性基线，本方法在OOD检测、错误框识别和漏检发现三项任务上均取得显著提升，且计算效率更高。

## 背景与动机

### 3D目标检测的不确定性困境

现代自动驾驶系统依赖3D目标检测器感知周围环境，然而现有检测器普遍缺乏高效可靠的不确定性估计机制。这一缺口在三个关键场景中尤为突出：

**分布外（OOD）场景检测**：当模型遭遇训练分布之外的场景（如恶劣天气、异常光照），检测器的预测置信度往往不可靠，但系统缺乏量化手段来识别这些高风险场景并触发安全降级或人工接管。

**定位误差识别**：检测器输出的边界框可能存在严重的定位偏差（如IoU < 0.3），但传统检测头仅输出类别概率，无法区分“定位准确的高置信度预测”与“定位错误的高置信度预测”。

**漏检目标发现**：某些目标完全未被检测器捕获（如被遮挡的车辆），现有方法无法提供关于“某区域可能遗漏了目标”的信号。

这三个问题的共同根源在于：**检测器的热图头（heatmap head）仅建模一阶概率分布，缺乏对预测本身不确定性的二阶建模能力**。

### 现有不确定性方法的局限

学术界已提出多种不确定性估计方法，但在实时自动驾驶场景中均存在严重瓶颈：

- **MC-Dropout**（Gal & Ghahramani, ICML 2016）：需要多次前向传播采样，计算开销随采样次数线性增长。
- **Deep Ensembles**（Lakshminarayanan et al., NeurIPS 2017）：需训练并维护多个独立模型，内存和推理成本成倍增加。
- **BatchEnsemble**（Wen et al., ICLR 2020）与**Masksembles**（Durasov et al., CVPR 2021）：虽降低了集成成本，但仍需多次前向传播。
- **Packed-Ensembles**（Laurent et al., ICLR 2023）：通过张量打包减少开销，但依然无法实现真正的单次推理不确定性估计。

这些采样或集成方法的共同缺陷是**计算开销与实时性需求之间的矛盾**——自动驾驶系统要求毫秒级推理延迟，而多次前向传播在算力受限的车载平台上难以部署。

### 证据深度学习的机遇

证据深度学习（Evidential Deep Learning, EDL）提供了一条不同的路径：通过在预测头之上建模**二阶概率分布**（如Beta分布），使模型在单次前向传播中同时输出预测值和对该预测的不确定性。EDL的核心思想是将分类问题转化为证据收集过程——模型输出的是支持各类别的“证据量”，证据越充分，预测越确定；证据匮乏则意味着高不确定性。

然而，EDL此前主要应用于简单分类任务，尚未被系统性地适配到3D目标检测的复杂场景中。3D检测面临独特的挑战：类别严重不平衡（BEV网格中绝大多数位置为背景）、多标签预测特性（一个网格可能同时属于多个类别）、以及不确定性需要在场景级、框级、网格级等多个粒度上聚合。

### 本文动机

针对上述缺口，本文提出将EDL引入3D目标检测的热图头，通过以下关键设计实现高效的不确定性估计：

1. **架构最小侵入**：仅替换检测器的热图头为EDL头（输出$\alpha$和$\beta$参数），保留骨干网络和BEV编码器不变，确保与现有检测架构（如**FocalFormer3D** Chen et al., ICCV 2023；**DeformFormer3D** Zhu et al., ICLR 2021）的兼容性。
2. **损失函数适配**：设计结合高斯焦点损失（GFL）权重的EDL损失，应对BEV热图的极端类别不平衡，并通过KL正则化惩罚错误预测时的过度自信。
3. **多层级不确定性聚合**：从BEV网格级不确定性出发，聚合得到场景级不确定性（用于OOD检测）和框级不确定性（用于定位质量评估），并额外设计漏检目标头以发现被遗漏的目标。

该方法的核心优势在于**单次前向传播即可获得类别概率、定位信息及不确定性**，计算开销几乎等同于标准检测器，使其具备在实时自动驾驶系统中部署的可行性。

## 核心创新

本工作的核心创新在于将**证据深度学习（Evidential Deep Learning, EDL）**引入3D目标检测的不确定性估计，以极低的计算开销实现单次前向传播中的多层次不确定性量化。与传统采样式方法（MC-Dropout、Deep Ensembles等）需要多次推理不同，本方法仅需**修改检测器的热图头（heatmap head）**即可同时输出目标存在概率与不确定性。

### 关键结构变更：EDL热图头

方法的核心改造点在于将标准BEV热图头替换为EDL热图头（Fig. 2）。标准热图头输出 $C$ 维类别概率，而EDL头输出两组 $C$ 维参数——**正证据参数 $\alpha_i$ 和负证据参数 $\beta_i$**，对应每个BEV网格 $i$ 的每个类别 $j$。这两组参数共同参数化一个Beta分布 $\text{Beta}(\alpha_{ij}, \beta_{ij})$，作为类别存在概率 $p_{ij}$ 的二阶先验。由此，模型不仅给出预测概率 $\hat{p}_{ij} = \alpha_{ij}/(\alpha_{ij}+\beta_{ij})$，还天然附带**证据不确定性** $u_{ij} = 2/(\alpha_{ij}+\beta_{ij})$——证据总量越低，不确定性越高。这一设计使得不确定性估计与目标检测共享同一个前向传播过程，无需额外的采样或集成推理。

### 损失函数设计：GFL加权EDL损失 + KL正则化

直接将标准EDL损失应用于3D检测面临严重的类别不平衡问题。本方法提出**组合损失函数** $\mathcal{L} = \sum_i (\mathcal{L}_i^{\text{EDL}} + \lambda \mathcal{L}_i^{\text{Reg}})$，包含两个关键创新：

1. **GFL加权EDL损失**（Eq. 3）：在EDL的贝叶斯风险损失中引入高斯焦点损失（Gaussian Focal Loss）的加权机制。对于正样本项，乘以 $(1 - \hat{p}_{ij})^{\gamma}$ 降低易分样本权重；对于负样本项，乘以 $(\hat{p}_{ij})^{\gamma} \cdot (1 - \hat{y}_{ij})^{\eta}$，其中 $\hat{y}_{ij}$ 为基于BEV网格与目标中心距离的高斯衰减因子，使远离目标中心的负样本获得更低的惩罚权重。这一设计有效缓解了BEV热图中正负样本极度不均衡的问题。

2. **KL正则化惩罚误导性证据**（Eq. 5）：当模型预测错误时，原始的 $\alpha$ 和 $\beta$ 可能给出误导性的高置信度。本方法对证据进行修正——若真实标签为正（$y_{ij}=1$），则 $\tilde{\alpha}_{ij}=1, \tilde{\beta}_{ij}=\beta_{ij}$；若真实标签为负，则 $\tilde{\alpha}_{ij}=\alpha_{ij}, \tilde{\beta}_{ij}=1$——然后最小化修正后Beta分布与无信息先验 $\text{Beta}(1,1)$ 之间的KL散度。这迫使模型在犯错时降低证据总量、增加不确定性，防止过自信。

### 多层次不确定性聚合

EDL热图头输出的逐网格逐类不确定性通过**层级聚合**服务于不同任务（Fig. 3）：
- **场景级不确定性**：对全场景所有BEV网格的不确定性取平均，用于分布外（OOD）场景检测；
- **框级不确定性**：对预测边界框内的各网格各类别不确定性取最小值聚合（$u_b = \min_i \hat{u}_b^i$），用于定位质量评估；
- **漏检目标检测**：设计独立的漏检头 $\mathcal{M}^{\text{miss}}$，以BEV嵌入、热图概率和EDL不确定性为输入，预测每个网格存在漏检目标的置信度（$\mathbf{p}_i^{\text{miss}} = \mathcal{M}^{\text{miss}}([\mathbf{e}_i, \mathbf{p}_i, \mathbf{u}_i])$）。

### 计算效率优势

相较于需要 $N$ 次前向传播的Deep Ensembles或MC-Dropout，本方法仅需**单次前向传播**，额外计算开销仅来自热图头输出维度的翻倍（$2C$ 替代 $C$）和轻量级漏检头。这一特性使其天然适用于实时自动驾驶系统，同时在下游自动标注管线中（Tab. 4），基于不确定性筛选伪标签可使下游检测器mAP提升约1%、NDS提升1-2%。

**需要人工验证的点**：漏检头 $\mathcal{M}^{\text{miss}}$ 的具体架构细节（层数、通道数等）在原文中未明确给出，仅描述了其输入为拼接向量 $[\mathbf{e}_i, \mathbf{p}_i, \mathbf{u}_i]$，需查阅代码仓库确认。

## 整体框架

本文提出一种基于证据深度学习（Evidential Deep Learning, EDL）的3D目标检测不确定性估计框架，其核心设计理念是：**在保持单次前向传播的低计算开销前提下，使检测器同时输出目标存在概率及其对应的不确定性**。该框架由以下关键模块构成：

### 输入与骨干网络

系统以LiDAR点云作为输入，采用**CenterPoint-Voxel**作为点云骨干网络进行体素化特征提取。提取后的特征经BEV特征编码器处理，生成多阶段BEV嵌入表示。本文在两个代表性的3D检测器架构上验证方法：**FocalFormer3D**（Chen et al., ICCV 2023）和**DeformFormer3D**（Zhu et al., ICLR 2021），前者采用多阶段特征细化策略，后者基于可变形注意力机制。

### EDL热图头：核心替换模块

框架的关键改造在于将检测器原有的标准热图头替换为**EDL热图头**（Figure 2）。标准热图头通常输出一个$C$维向量，表示$C$个类别的目标存在概率；EDL热图头则将输出维度翻倍，前$C$维作为正向证据参数$\alpha_i$，后$C$维作为负向证据参数$\beta_i$。对于BEV网格中的每个单元格$i$和每个类别$j$，模型通过Beta分布$\text{Beta}(\alpha_{ij}, \beta_{ij})$对类别概率进行二阶建模，从而同时获得：

- **目标存在概率**：$\hat{p}_{ij} = \alpha_{ij} / (\alpha_{ij} + \beta_{ij})$
- **不确定性估计**：$u_{ij} = 2 / (\alpha_{ij} + \beta_{ij})$

这种设计使得不确定性估计内嵌于检测器的前向传播过程中，无需多次采样或集成推理，从根本上规避了MC-Dropout、Deep Ensembles等方法的高计算开销问题。

### 训练损失与正则化

为适配3D目标检测中的类别不平衡和稀疏标注特性，本文设计了组合损失函数：

$$
\mathcal{L} = \sum_{i=1}^{S} \left( \mathcal{L}_i^{\mathrm{EDL}} + \lambda \mathcal{L}_i^{\mathrm{Reg}} \right)
$$

其中$\mathcal{L}_i^{\mathrm{EDL}}$在标准EDL损失的基础上引入了**高斯焦点损失（GFL）权重**和邻近中心折扣项，以缓解正负样本严重不均衡的问题；$\mathcal{L}_i^{\mathrm{Reg}}$通过KL散度惩罚错误预测时的误导性证据，将调整后的证据分布拉向无信息先验$\text{Beta}(1,1)$，从而防止模型在错误预测时仍保持过低的置信度。

### 多层级不确定性聚合

框架支持三个粒度的不确定性应用（Figure 3）：

1. **场景级不确定性**：对全场景所有BEV网格的不确定性值取平均，用于分布外（OOD）场景检测，如识别恶劣天气或未见环境。
2. **框级不确定性**：对每个预测边界框内的网格，按类别取最小值聚合为单一框不确定性$u_b = \min_i \hat{u}_b^i$，用于评估定位质量、检测错误预测框。
3. **漏检目标检测**：引入独立的漏检目标头$\mathcal{M}^{\mathrm{miss}}$，其输入为BEV嵌入$\mathbf{e}_i$、热图概率$\mathbf{p}_i$和EDL不确定性$\mathbf{u}_i$的拼接，输出每个网格的漏检置信度$\mathbf{p}_i^{\mathrm{miss}}$。

### 下游应用闭环

不确定性估计的最终目标是支撑自动标注管线中的选择性人工验证：高不确定性场景或预测框被筛选出来进行人工复核，低不确定性结果直接作为伪标签使用。实验表明，这种基于不确定性引导的验证策略使下游检测器的mAP提升约1%，NDS提升1-2%（Table 4），证明了框架在实际自动驾驶数据闭环中的有效性。

> **局限性提示**：当前框架仅更新检测器的热图头部分，骨干网络和BEV编码器未参与端到端的不确定性学习；场景级和框级不确定性聚合依赖手动设计的平均/最小值操作，可能并非最优策略。

### 补充图表

![[assets/figures/papers/paper_list_l81_https_arxiv_org_abs_2410_23910/figures/001_Figure_1.jpg]]
*Figure 1: 3D Object Detection Uncertainty Estimation Framework. Our Evidential Deep Learning approach jointly generates heatmap probabilities for objects within Bird’s Eye View and their corresponding uncertainty values, which allows us to detect several critical problems within autonomous driving, namely (left) identifying out-of-distribution scenes (e.g., with bad weather conditions), (middle) erroneous predicted boxes, and (right) missed objects (e.g., missed grey and white cars in the image). The uncertainty estimates guide selective human verification, leading to improvements in detection metrics (e.g., mean Average Precision (mAP) and nuScenes Detection Score (NDS))*

## 核心模块与公式推导

### 方法总览

本方法的核心思路是将现代3D检测器中的BEV热图头替换为证据深度学习（EDL）头，使模型在单次前向传播中同时输出目标存在概率和不确定性。如图Figure 2所示，EDL头为每个BEV网格的每个类别预测两个参数 $\alpha_i$ 和 $\beta_i$，分别对应正证据和负证据。通过聚合这些BEV层级的不确定性估计，可以同时获得场景级和框级的不确定性。

### EDL热图头

标准热图头输出 $C$ 维类别概率，EDL头则输出 $2C$ 维参数——前 $C$ 维为 $\alpha_i$，后 $C$ 维为 $\beta_i$。第 $i$ 个BEV网格的预测概率和不确定性由Beta分布的参数导出：

$$p_{ij} = \frac{\alpha_{ij}}{\alpha_{ij} + \beta_{ij}}, \quad u_{ij} = \frac{1}{\alpha_{ij} + \beta_{ij}}$$

其中 $p_{ij}$ 为类别 $j$ 的存在概率，$u_{ij}$ 为对应的不确定性（证据总量越小，不确定性越高）。

### EDL损失函数

EDL的核心是将多标签分类建模为Beta分布上的贝叶斯风险最小化问题。对于第 $i$ 个BEV网格，基础EDL损失的闭式解为：

$$\mathcal{L}_i(\Theta) = \sum_{j=1}^{C} \left[ y_{ij} \left( \psi(\alpha_{ij}+\beta_{ij}) - \psi(\alpha_{ij}) \right) + (1-y_{ij}) \left( \psi(\alpha_{ij}+\beta_{ij}) - \psi(\beta_{ij}) \right) \right]$$

其中 $\psi(\cdot)$ 为digamma函数，$y_{ij}$ 为真实标签。

针对3D检测中的类别不平衡问题，作者将高斯焦点损失（GFL）权重引入EDL框架，得到定制化损失：

$$\mathcal{L}_i^{\mathrm{EDL}} = \sum_{j=1}^{C} \left[ y_{ij} \left( \psi(\alpha_{ij}+\beta_{ij}) - \psi(\alpha_{ij}) \right) \cdot (1 - \frac{\alpha_{ij}}{\alpha_{ij}+\beta_{ij}})^{\gamma} + (1-y_{ij}) \left( \psi(\alpha_{ij}+\beta_{ij}) - \psi(\beta_{ij}) \right) \cdot (\frac{\alpha_{ij}}{\alpha_{ij}+\beta_{ij}})^{\gamma} \cdot (1 - \hat{y}_{ij})^{\eta} \right]$$

其中 $\gamma$ 为焦点参数，$\hat{y}_{ij}$ 为邻近中心折扣项，$(1-\hat{y}_{ij})^{\eta}$ 用于抑制远离目标中心的负样本权重。

### KL正则化

为防止模型对错误预测产生过自信，作者设计了证据调整策略。当预测错误时，将误导性证据重定向：

$$\tilde{\alpha}_i = \mathbf{y}_i + (1 - \mathbf{y}_i) \odot \alpha_i, \quad \tilde{\beta}_i = (1 - \mathbf{y}_i) + \mathbf{y}_i \odot \beta_i$$

其中 $\odot$ 表示逐元素乘法。调整后的证据使错误预测的Beta分布被推向无信息先验 $\mathrm{Beta}(1,1)$。正则化损失为KL散度：

$$\mathcal{L}_i^{\mathrm{Reg}} = \sum_{j=1}^{C} \mathrm{KL} \left( \mathrm{Beta}(\tilde{\alpha}_j, \tilde{\beta}_j) \| \mathrm{Beta}(\mathbf{1}, \mathbf{1}) \right)$$

总损失函数为两者加权组合：

$$\mathcal{L} = \sum_{i=1}^{S} \left( \mathcal{L}_i^{\mathrm{EDL}} + \lambda \mathcal{L}_i^{\mathrm{Reg}} \right)$$

### 不确定性聚合模块

**场景级不确定性**：对全场景所有BEV网格的不确定性取平均，用于分布外（OOD）场景检测（见Figure 3(a)）。

**框级不确定性**：对预测框内的各网格各类别不确定性取最小值聚合：

$$u_b = \min_i \hat{u}_b^i$$

该聚合方式使框内任一网格存在高置信度时即可降低整体不确定性，用于检测定位质量差的预测框（见Figure 3(b)）。

**漏检目标头 $M^{\mathrm{miss}}$**：一个独立的轻量头，输入BEV嵌入 $\mathbf{e}_i$、热图概率 $\mathbf{p}_i$ 和EDL不确定性 $\mathbf{u}_i$ 的拼接，输出漏检置信度：

$$\mathbf{p}_i^{\mathrm{miss}} = \mathcal{M}^{\mathrm{miss}}([\mathbf{e}_i, \mathbf{p}_i, \mathbf{u}_i])$$

该模块专门用于发现检测器遗漏的目标。其具体架构细节在原文中未完整披露，需要手动验证。

### 补充图表

![[assets/figures/papers/paper_list_l81_https_arxiv_org_abs_2410_23910/figures/002_Figure_2.jpg]]
*Figure 2: Model architecture with EDL Heatmap Head. We replace the standard heatmap head with an Evidential Deep Learning (EDL) head, which predicts both object presence probabilities and uncertainty by outputting*

![[assets/figures/papers/paper_list_l81_https_arxiv_org_abs_2410_23910/figures/003_Figure_3.jpg]]
*Figure 3: Uncertainty at different levels. (a) Scene-level uncertainty aggregates uncertainty values across all BEV cells in a scene to produce an overall uncertainty score, which help detect OOD scenes. (b) Box-level uncertainty focuses on each predicted bounding box’s uncertainty using ROI pooling, allowing for the identification of poorly localized bounding boxes*

## 实验与分析

### 核心实验设计

本文围绕三个关键安全场景评估不确定性估计质量：**分布外（OOD）场景检测**、**错误定位框检测**和**漏检目标发现**，并进一步验证不确定性在自动标注管线中的下游价值。实验基座为**FocalFormer3D**（Chen et al., ICCV 2023）和**DeformFormer3D**（Zhu et al., ICLR 2021）两种代表性3D检测器，均替换其BEV热图头为EDL头。对比的不确定性基线包括**Entropy**（Malinin & Gales, NeurIPS 2018）、**MC-Dropout**（Gal & Ghahramani, ICML 2016）、**Deep Ensembles**（Lakshminarayanan et al., NeurIPS 2017）、**BatchEnsemble**（Wen et al., ICLR 2020）、**Masksembles**（Durasov et al., CVPR 2021）和**Packed-Ensembles**（Laurent et al., ICLR 2023）。

### 分布外场景检测

OOD检测实验以nuScenes（分布内）与Waymo（分布外）构成跨数据集评估。场景级不确定性通过对全场景所有BEV网格的不确定性值取平均得到（Fig. 3a）。**Tab. 1**汇总了各方法在不同检测器配置下的ROC-AUC和PR-AUC。

本方法在平均ROC-AUC上达到**0.6594**，比次优方法Deep Ensembles（0.5685）提升**0.09**；平均PR-AUC达到**0.6696**，比次优方法Masksembles（0.5164）提升**0.16**。从**Fig. 4**的ROC/PR曲线可见，本方法的曲线在所有配置下均显著高于其他基线，尤其在高召回区间优势更为明显，表明EDL不确定性对OOD场景具有更强的判别力。

![[assets/figures/papers/paper_list_l81_https_arxiv_org_abs_2410_23910/figures/005_Figure_4.jpg]]
*Figure 4: Scene out-of-distribution detection ROC and PR curves evaluation. ROC and PR curves for the OOD detection task using the uncertainty measure described in Section 4.2. A higher position of the curve indicates a better ability of the uncertainty measure to detect OOD scenes. Our uncertainty measure outperforms other methods by a significant margin across various setups*

值得注意的是，DeformFormer在OOD检测上表现普遍弱于FocalFormer，一个可能的原因是FocalFormer的多阶段特征细化机制为不确定性估计提供了更丰富的BEV表示——这一点在原文中未作消融验证，需读者自行判断。

### 错误定位框检测

错误框检测任务将预测框按与真值的IoU分为正确框（IoU≥0.3）和错误框（IoU<0.3），评估不确定性对错误框的识别能力。框级不确定性通过框内各网格各类别不确定性的最小值聚合得到（$u_b = \min_i \hat{u}_b^i$）。

**Tab. 2**显示，本方法在平均ROC-AUC上达到**0.6235**，比次优方法Deep Ensembles（0.5923，FF(L)配置）提升约**0.06**；平均PR-AUC为**0.3634**，提升约**0.02**。**Fig. 5**的ROC/PR曲线进一步确认本方法在所有检测器配置下均优于基线。然而，PR-AUC的绝对数值普遍偏低（最高仅0.3646），说明错误框检测任务本身存在严重的类别不平衡——错误框占比远小于正确框，导致精确率受限。这是任务固有特性，而非方法缺陷。

### 漏检目标发现

漏检目标检测评估不确定性是否能指示模型“遗漏了什么”。实验在BEV网格上定义漏检目标为未被任何预测框覆盖的真值目标，使用专门的漏检头$\mathcal{M}^{\text{miss}}$（输入BEV嵌入、热图概率和EDL不确定性）预测漏检置信度。

**Tab. 3**报告了2m和4m距离阈值下的精确率、召回率和F1-score。在2m距离下，本方法F1-score达到**0.0989**，显著优于其他不确定性基线。虽然绝对数值较低，但考虑到漏检目标在BEV网格中极为稀疏，这一结果已体现出EDL不确定性的独特价值——传统采样方法（MC-Dropout、Ensembles）对此任务几乎无能为力。

### 自动标注管线验证

将不确定性用于自动标注验证是本方法的直接应用场景：对无标签数据，使用教师模型生成伪标签，仅保留不确定性低于阈值的预测框用于训练下游检测器。**Tab. 4**报告了nuScenes上不同标注预算（5k/10k/20k帧）下的mAP和NDS。

在10k预算下，基于不确定性验证的自动标注使下游检测器mAP相比无验证基线提升约**0.785%**，NDS提升1-2%。整体而言，不确定性验证管线在各预算下均一致优于标准伪标签基线，mAP绝对增益约**1%**。这验证了EDL不确定性在筛选高质量伪标签方面的实用价值。

### 方法局限与失效模式

1. **局部更新而非端到端**：当前方法仅替换检测器的热图头，骨干网络和BEV编码器未参与不确定性学习。这意味着不确定性质量受限于固定特征表示，无法通过端到端优化进一步提升。
2. **手工聚合策略**：场景级不确定性使用简单平均，框级不确定性使用最小值操作。这些手工设计的聚合方式可能并非最优，尤其在多目标密集场景下，最小值聚合可能过度受单点噪声影响。
3. **漏检头架构未充分披露**：$\mathcal{M}^{\text{miss}}$的具体网络结构、超参数选择及训练细节未在原文中详细说明，复现该模块需要额外工程探索。
4. **PR-AUC偏低**：错误框检测和漏检目标检测的PR-AUC绝对数值较低，反映任务固有的极端类别不平衡。实际部署时需结合具体业务阈值进行校准。

### 补充图表

![[assets/figures/papers/paper_list_l81_https_arxiv_org_abs_2410_23910/figures/004_Table_1.jpg]]
*Table 1: Scene OOD detection ROC- and PR-AUCs evaluation. The best result in each category is in bold and the second best is in bold. Ours outperforms the second-best on average by 0.09 ROC-AUC & 0.16 PR-AUC, respectively*

![[assets/figures/papers/paper_list_l81_https_arxiv_org_abs_2410_23910/figures/006_Table_2.jpg]]
*Table 2: Detection of erroneous boxes ROC- and PR-AUCs evaluation. The best result in each category is in bold and the second best is in bold. Ours outperforms the second-best on average by 0.06 ROC-AUC & 0.02 PR-AUC, respectively*

![[assets/figures/papers/paper_list_l81_https_arxiv_org_abs_2410_23910/figures/007_Figure_5.jpg]]
*Figure 5: ROC and PR curve evaluation for the detection of erroneous boxes. ROC and PR curves for the erroneous box detection task using the uncertainty measure in Section 4.3. A higher position of the curve indicates a better ability of the uncertainty measure to detect erroneous boxes predicted by the model. Our uncertainty measure outperforms baselines across various setups*

![[assets/figures/papers/paper_list_l81_https_arxiv_org_abs_2410_23910/figures/008_Table_3.jpg]]
*Table 3: Missed object detection evaluation. The best result in each category is in bold and the second best is in bold. Ours outperforms others by a significant margin*

![[assets/figures/papers/paper_list_l81_https_arxiv_org_abs_2410_23910/figures/009_Table_4.jpg]]
*Table 4: NuScenes auto-labeling results. We compare our uncertainty-based verification method against two baselines: standard training on the smaller training set and auto-labeling without uncertainty-based verification. FT represents training on the entire dataset, which we consider as an upper bound for quality. The results show that our approach consistently outperforms both baselines, achieving higher mAP and NDS scores across all configurations, with significant relative improvements over the auto-labeling without uncertainty baseline, as shown in the “Imp, %” column*

## 方法谱系与知识库定位

### 方法沿革与基线定位

本工作处于**3D目标检测不确定性估计**与**证据深度学习**的交叉点，其直接技术脉络可追溯至两条主线：

1. **不确定性估计基线**：传统上，基于采样的方法主导了深度学习不确定性估计，包括 **MC-Dropout**（Gal & Ghahramani, ICML 2016）、**Deep Ensembles**（Lakshminarayanan et al., NeurIPS 2017）以及后续的效率优化变体 **BatchEnsemble**（Wen et al., ICLR 2020）、**Masksembles**（Durasov et al., CVPR 2021）和 **Packed-Ensembles**（Laurent et al., ICLR 2023）。这些方法的核心瓶颈在于多次前向传播带来的计算开销，使其难以部署于实时自动驾驶系统。此外，基于最大概率熵的 **Entropy** 基线（Malinin & Gales, NeurIPS 2018）虽计算轻量，但缺乏对分布外场景的结构化建模能力。

2. **3D检测器架构**：本方法以 **FocalFormer3D**（Chen et al., ICCV 2023）和 **DeformFormer3D**（Zhu et al., ICLR 2021）作为宿主检测器，二者均采用BEV热图头进行目标存在性预测。本工作的关键改造在于将标准热图头替换为EDL头，输出每类每网格的 $\alpha$ 和 $\beta$ 参数，而非单一的类别概率向量。

### 关键改造槽位

本方法对检测器流水线的改动高度集中，仅触及三个槽位：

| 槽位 | 基线值 | 本方法 | 证据锚点 |
|------|--------|--------|----------|
| 热图头 | 标准C维类别概率输出 | EDL头，输出 $\alpha_i, \beta_i$（双倍维度） | Sec. 3.2, Fig. 2 |
| 损失函数 | 高斯焦点损失（GFL） | 组合EDL损失 $L_i^{\text{EDL}}$ + $\lambda L_i^{\text{Reg}}$ | Sec. 3.2 Eq. 3, Eq. 5 |
| 正则化 | 无或L2正则 | 证据调整 + KL散度正则化至Beta(1,1)先验 | Sec. 3.2 |

这种**仅更新头部**的策略使其可即插即用地接入现有BEV检测器流水线，骨干网络（CenterPoint-Voxel）和BEV特征编码器保持不变。这一设计既是优势（低侵入性、易部署），也构成当前方法的核心局限——骨干网络未参与不确定性学习，可能限制了不确定性质量的上限。

### 适用边界与局限

1. **头部局限**：当前方法仅改造热图头，未对LiDAR骨干或BEV编码器进行端到端不确定性学习。这意味着不确定性信号仅来自BEV热图层的二阶分布建模，而底层特征提取中的不确定性未被显式捕获。

2. **聚合策略的手工设计**：场景级不确定性（全场景平均池化）和框级不确定性（框内min pooling）均依赖手工设计的聚合操作，缺乏可学习参数。这种设计在实验中被证明有效，但在理论上可能并非最优——例如，不同类别的不确定性可能具有不同的空间分布特性，统一平均可能掩盖细粒度信号。

3. **漏检头架构未充分披露**：漏检目标头 $\mathcal{M}^{\text{miss}}$ 的具体架构和超参数选择在论文中未详细说明（仅给出公式 $\mathbf{p}_i^{\text{miss}} = \mathcal{M}^{\text{miss}}([\mathbf{e}_i, \mathbf{p}_i, \mathbf{u}_i])$），其可复现性需要手动验证。

4. **跨检测器泛化性**：实验仅在FocalFormer3D和DeformFormer3D两个检测器上进行验证，且DeformFormer在场景OOD检测中表现显著弱于FocalFormer（见Tab. 1）。这一差异暗示EDL头的有效性可能与BEV编码器的多阶段特征细化能力相关，在更简单的BEV架构上可能无法获得同等增益。

### 开放问题

1. **端到端不确定性学习**：若将EDL范式扩展至骨干网络和BEV编码器，使不确定性信号从底层特征开始传播，能否进一步提升OOD检测和定位质量评估的性能？

2. **聚合策略的可学习化**：用注意力机制或轻量网络替代手工平均/min pooling，是否能在保持推理效率的同时提升不确定性质量？

3. **DeformFormer表现差异的根因**：为何DeformFormer在场景OOD检测中显著弱于FocalFormer？是否因为FocalFormer的多阶段热图细化过程天然适合EDL的二阶分布建模？这一问题对方法的通用性至关重要。

4. **漏检头的最优设计**：$\mathcal{M}^{\text{miss}}$ 的架构空间（层数、输入特征组合、与主检测头的参数共享策略）尚未被系统探索，其最优配置可能因检测器架构和数据集而异。

## 原文 PDF

![[paperPDFs/arxiv_2024/Uncertainty_Estimation_for_3D_Object_Detection_via_Evidential_Learning.pdf]]