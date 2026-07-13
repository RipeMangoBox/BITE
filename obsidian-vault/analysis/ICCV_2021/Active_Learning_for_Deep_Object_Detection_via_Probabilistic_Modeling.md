---
title: "Active Learning for Deep Object Detection via Probabilistic Modeling"
type: paper
paper_level: A
venue: ICCV
year: 2021
pdf_ref: paperPDFs/ICCV_2021/Active_Learning_for_Deep_Object_Detection_via_Probabilistic_Modeling.pdf
project_link: null
code_link: https://github.com/NVlabs/AL-MDN
aliases:
- AMALMDN
- ALDODPM
tags:
- ICCV_2021
- topic/optimization_theory_probabilistic
- topic/optimization_theory_probabilistic/optimization_methods
core_operator: "采用混合密度网络（MDN）对目标检测器的定位和分类头部进行概率化改造，将确定性输出替换为多分量高斯混合模型（GMM）的估计，从而在单次前向传播中同时捕获每个预测的偶然不确定性和认知不确定性，并通过整合四种不确定性的评分函数指导样本选择。"
primary_logic: "将目标检测中来自定位和分类任务的偶然与认知不确定性进行显式建模并聚合，能提供互补的信息量度量（重叠率仅14%），使得单模型、单前向传递的主动学习在精度上超越单模型方法，并与多模型方法持平，同时大幅降低计算开销。"
claims:
- "在VOC07主动学习中，使用最大函数聚合四种不确定性在第3轮（4k图像）达到69.43 mAP，比随机采样高0.96，且优于所有单模型方法。"
- "定位与分类不确定性之间选择的图像重叠率仅为14%，证明两种不确定性提供多样化信息，对主动学习至关重要。"
- "在VOC07+12全量训练中，Ours_gmm达到75.98 mAP，超过LLAL（73.38）等单模型方法，与MC-dropout（75.67）和Ensemble（75.90）相当，但前向时间仅为MC-dropout的1/20。"
- "PASCAL VOC07 (active learning, 3rd cycle, 4k labeled) 上 mAP (IoU>0.5) % = 69.43±0.11 (Ours_gmm)"
---

# Active Learning for Deep Object Detection via Probabilistic Modeling

> [!tip] 核心洞察
> 将目标检测中来自定位和分类任务的偶然与认知不确定性进行显式建模并聚合，能提供互补的信息量度量（重叠率仅14%），使得单模型、单前向传递的主动学习在精度上超越单模型方法，并与多模型方法持平，同时大幅降低计算开销。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 基于概率建模的深度目标检测主动学习 |
| 英文题名 | Active Learning for Deep Object Detection via Probabilistic Modeling |
| 会议/期刊 | ICCV 2021 |
| Links | [paper](https://arxiv.org/abs/2103.16130) · [GitHub](https://github.com/NVlabs/AL-MDN) |
| Topic | #topic/optimization_theory_probabilistic #topic/optimization_theory_probabilistic/optimization_methods |
| Method | AL-MDN (Active Learning via Mixture Density Networks) |
| Dataset | PASCAL VOC07 (active learning, 3rd cycle, 4k labeled), PASCAL VOC07+12 (active learning, final 10k labeled), MS-COCO (active learning, 7k labeled) |

> [!tip] 效果简介
> - PASCAL VOC07 (active learning, 3rd cycle, 4k labeled) 上，mAP (IoU>0.5) % 为 69.43±0.11 (Ours_gmm)，对比 68.47±0.09 (Random)，变化 +0.96。
> - PASCAL VOC07+12 (active learning, final 10k labeled) 上，mAP (IoU>0.5) 为 0.7598±0.0021 (Ours_gmm)，对比 0.7117±0.0016 (Random)，变化 +0.0481。
> - MS-COCO (active learning, 3rd cycle, 7k labeled) 上，mAP (IoU>0.5:0.95) % 为 30.51±0.12 (Ours_gmm)，对比 28.69±0.11 (Random)，变化 +1.82。

## 概要

**问题瓶颈**：现有深度目标检测的主动学习方法普遍依赖多模型集成或多前向传递（如MC‑dropout）来估计不确定性，计算成本高昂；且大多数方法仅利用分类不确定性，忽略了定位不确定性，导致样本选择的信息量度量不够全面。

**核心方法**：本文提出基于混合密度网络（MDN）的主动学习框架AL‑MDN，对单阶段检测器的定位和分类头部进行概率化改造，将确定性输出替换为多分量高斯混合模型（GMM）的估计。在单次前向传播中，该方法可同时捕获每个预测的**偶然不确定性**（数据固有噪声）和**认知不确定性**（模型知识不足），并设计评分函数将定位与分类的四种不确定性聚合为每张图像的信息量得分。

**关键洞察**：定位与分类不确定性选择的图像重叠率仅为14%，证明两类不确定性提供高度互补的信息量信号——显式建模并聚合二者，是突破单模型主动学习精度瓶颈的关键。

**主要结果**：
- 在PASCAL VOC07主动学习中，第3轮（4000张标注图像）达到69.43 mAP，比随机采样高0.96个百分点，优于所有单模型方法（Table 4）。
- 在VOC07+12全量训练中达到75.98 mAP，与MC‑dropout（75.67）和Ensemble（75.90）持平，但前向时间仅为MC‑dropout的1/20（Figure 4, Figure 5）。
- 在MS‑COCO上第3轮（7000张标注图像）达到30.51 mAP，比随机采样高1.82个百分点（Table 5）。

**方法定位**：AL‑MDN属于单模型、单前向传递的主动学习范式，在精度上超越同类单模型方法，达到多模型方法的水平，同时大幅降低计算开销，为深度目标检测的主动学习提供了高效且全面的不确定性建模方案。

深度目标检测模型的性能高度依赖大规模标注数据，但边界框级标注成本高昂，这促使主动学习成为降低标注代价的关键范式。然而，现有主动学习方法在目标检测任务中面临两个核心瓶颈。

**计算效率瓶颈**。主流的不确定性估计方法依赖多模型或多前向传递。例如，**MC-dropout**（Feng et al., IV 2019）需要多次随机前向传播来近似后验分布，**Ensemble**（Haussmann et al., IV 2020）需训练并维护多个独立模型。如 Table 4 和 Figure 5 所示，MC-dropout 的单次前向时间达到 0.412 秒，是本文方法的 20 倍；Ensemble 的参数量高达 78.87M，计算开销显著。这些方法虽能提升主动学习精度，但高昂的计算成本限制了其在实际应用中的可扩展性。

**信息量度量不全面**。现有单模型方法——如基于分类熵的 **Entropy**（Roy et al., BMVC 2018）、基于特征空间覆盖的 **Core-set**（Sener & Savarese, ICLR 2018）和基于损失预测的 **LLAL**（Yoo & Kweon, CVPR 2019）——仅利用分类不确定性来选择样本，忽略了定位任务中的不确定性信息。目标检测包含分类和定位两个子任务，两者的不确定性具有互补性。如 Table 3 所示，基于定位不确定性与分类不确定性选择的图像重叠率仅为 **14%**，表明两类不确定性提供了高度多样化的信息量信号，单独使用任一种都会遗漏大量有价值的样本。

上述两个瓶颈的根源在于：确定性检测头无法在单次前向传播中同时捕获定位和分类任务的偶然不确定性（数据固有噪声）与认知不确定性（模型知识不足）。本文的核心动机正是通过概率建模改造检测头，在保持单模型、单前向传递效率的同时，显式估计并聚合四类不确定性，实现信息量更全面、计算成本更低的主动学习。

## 核心方法与创新机理

本工作的核心创新在于将目标检测主动学习中的**不确定性估计**从“多模型/多前向传递”范式迁移到“单模型/单前向传递”范式，并首次显式地同时建模**定位与分类**两个任务维度的**偶然与认知**两种不确定性。具体而言，该方法通过三个关键改造（changed slots）实现了这一突破。

### 1. 检测头的概率化改造：从确定性输出到混合密度网络

传统目标检测器的定位头和分类头均输出确定性值——边界框坐标回归值和类别得分。本方法将两个头部改造为**混合密度网络（MDN）**，使网络学习输出一个 $K$ 分量高斯混合模型（GMM）的参数（均值 $\mu^k$、方差 $\Sigma^k$、权重 $\pi^k$），而非单一确定值（Section 3.1, Eq. 2）。

这一改造在定位头上表现为：对于每个边界框的每个坐标，网络预测 $K$ 个高斯分量的参数，并通过 softmax 归一化权重、sigmoid 约束方差，形成合法的 GMM（Eq. 2）。在分类头上，网络同样为每个类别的 logit 预测 $K$ 分量 GMM 参数，并通过重参数化技巧（$\hat{c}_p^k = \mu_p^k + \sqrt{\Sigma_p^k} \gamma$，$\gamma \sim \mathcal{N}(0,1)$）引入随机性（Eq. 4）。

从 GMM 参数中，可自然地解耦出两种不确定性（Eq. 1）：
- **偶然不确定性**（aleatoric）：各分量方差的加权和 $u_{al} = \sum_{k=1}^K \pi^k \Sigma^k$，反映数据本身的噪声；
- **认知不确定性**（epistemic）：各分量均值相对于混合均值的加权方差 $u_{ep} = \sum_{k=1}^K \pi^k \| \mu^k - \sum_{i=1}^K \pi^i \mu^i \|^2$，反映模型对预测的不确信程度。

### 2. 损失函数的协同适配

为适配 GMM 输出，损失函数随之改变：

- **定位损失**：从 Smooth L1 loss 替换为基于 GMM 的负对数似然损失（Eq. 3），使模型在回归边界框偏移量时同时学习预测方差，方差正则化效应提供了天然的损失衰减（loss attenuation），对高噪声样本自动降低权重。
- **分类损失**：从标准交叉熵替换为加权混合交叉熵损失（Type-1, Eq. 5），对正样本和困难负样本分别计算各分量下的交叉熵并按权重 $\pi^k$ 加权求和，使模型能够在多个类别分布假设下评估预测质量。

### 3. 高效变体：以精度换效率的帕累托改进

全 GMM 分类头需要为每个类别预测方差参数，在类别数较多时（如 MS-COCO 的 80 类）参数量显著增加。为此，提出**高效变体**（Ours_eff, Section 3.2）：分类头不再显式预测方差，而是直接输出类别概率分布，并利用类别概率的方差公式 $u_{al} = \sum_{k=1}^K \pi^k (\text{diag}(\hat{c}_p^k) - (\hat{c}_p^k)^{\otimes 2})$ 计算偶然不确定性（Eq. 8）。该变体在 VOC07 上达到与全 GMM 相当的检测精度（Table 1），同时将参数量从 52.35M 降至 41.12M。

### 4. 四维不确定性聚合：互补信息的最大化利用

本方法的关键洞察在于：**定位不确定性**与**分类不确定性**所选择的图像重叠率仅为 14%（Table 3），证明两种任务的不确定性提供了高度互补的信息量信号。基于此，评分函数将定位-偶然、定位-认知、分类-偶然、分类-认知四种不确定性进行 z-score 归一化后取最大值，作为每张图像的信息量得分（Section 3.3, Table 2）。消融实验表明，该最大聚合策略比单独使用任何一种不确定性在 VOC07 上提升约 0.9 mAP，也优于求和聚合。

### 创新本质总结

本方法的本质创新在于：**通过输出层的概率化改造，将不确定性估计从“外部集成”内化为“单模型内部结构”，同时将不确定性空间从单一的分类维度拓展到定位与分类的联合维度，使单次前向传播即可捕获更全面的信息量信号**。这一定位使得方法在精度上超越所有单模型基线，与 MC-dropout、Ensemble 等多模型方法持平，而前向时间仅为 MC-dropout 的 1/20（Figure 5）。

![[assets/figures/papers/paper_list_l7_https_arxiv_org_abs_2103_16130/figures/002_Figure_2.jpg]]
*Figure 2: An overview of the proposed object detection network. The main difference with conventional object detectors [31, 32] is in the localization and classification heads (branches). a) Instead of having deterministic outputs, our approach learns the parameters of K-components GMM for each of the outputs: coordinates of the bounding box in the localization head and the class density distribution in the classification (confidence) head (see Section 3.1). b) A classification head that improves the efficiency by eliminating variance parameters from GMM’s classification head (see Section 3.2)*

AL-MDN 的整体流程围绕“单模型、单前向传播同时估计定位与分类的偶然和认知不确定性”这一核心机制展开。与依赖多模型集成（Ensemble）或多前向 MC-Dropout 的传统方法不同，该方法仅需一次前向即可获得每张图像的信息量评分，从而在保持与多模型方法相当精度的同时，将前向时间降低至 MC-Dropout 的约 1/20（Figure 5）。

### 模块构成与数据流

整个框架由三个关键模块串联构成：

1. **GMM-based Localization Head**
   将标准检测器的确定性边界框回归头替换为混合密度网络（MDN）。对于每个预测框的每个坐标，网络输出一个 $K$ 分量高斯混合模型（GMM）的参数：均值 $\mu^k$、方差 $\Sigma^k$ 和混合权重 $\pi^k$（经 softmax 归一化）。这些参数通过负对数似然损失（Eq. 3）进行训练，损失函数内置了对方差的正则化效应。前向传播后，从 GMM 参数中按 Eq. 1 分别计算定位的偶然不确定性（分量方差的加权和）与认知不确定性（分量均值的加权方差）。

2. **GMM-based Classification Head**
   分类头同样被概率化改造。完整版本（Ours_gmm）为每个类别的 logit 预测 GMM 参数，并通过重参数化技巧（Eq. 4）采样得到类别分布；高效变体（Ours_eff）则省去方差预测，直接利用类别概率的方差计算偶然不确定性（Eq. 8），在保持精度的同时减少参数量（Table 1）。分类损失采用加权混合交叉熵（Eq. 5），并包含困难负样本挖掘（比例 $M=3$）。

3. **Uncertainty Aggregation & Scoring**
   对每张图像的每个检测目标，分别计算四类不确定性：定位偶然、定位认知、分类偶然、分类认知。随后，对每个目标的不确定性进行 z-score 归一化，再取所有目标、所有不确定性类型中的最大值作为该图像的信息量得分。消融实验（Table 2）证实，这种“最大值聚合”策略优于单独使用任一类不确定性（提升约 0.9 mAP），也优于求和聚合。其有效性源于定位与分类不确定性间极低的选择重叠率——仅 14%（Table 3），表明两者提供了高度互补的信息量度量。

### 输入输出规范

- **输入**：未标注图像池中的单张图像，经标准预处理后送入单阶段检测器（默认 SSD300）的骨干网络。
- **中间表示**：骨干网络提取特征图后，分别进入定位头和分类头的 GMM 分支。两个分支均输出 $K$ 分量 GMM 的参数集合。
- **输出**：每张图像获得一个标量信息量得分。主动学习循环中，选择得分最高的 top-$B$ 张图像送人工标注，加入训练集后重新训练模型，进入下一轮迭代。

Figure 2 直观展示了标准检测头与 GMM 检测头的结构差异：确定性输出被替换为对每个输出量学习 $K$ 分量 GMM 参数，这是实现单次前向不确定性估计的架构基础。

### 3.1 混合密度网络（MDN）驱动的概率化目标检测

方法的核心创新在于将标准目标检测器的确定性输出层替换为混合密度网络（MDN），使其预测每个输出的概率分布——即K分量高斯混合模型（GMM）的参数，而非单一标量值。该改造同时作用于定位头和分类头，从而在单次前向传播中显式捕获偶然不确定性（数据固有噪声）和认知不确定性（模型知识不足）。

**GMM参数归一化**：网络原始输出 $\hat{\pi}_b^k$、$\hat{\mu}_b^k$、$\hat{\Sigma}_b^k$ 需经归一化以构成合法GMM：

$$\pi_b^k = \frac{e^{\hat{\pi}_b^k}}{\sum_{j=1}^K e^{\hat{\pi}_b^j}}, \quad \mu_b^k = \hat{\mu}_b^k, \quad \Sigma_b^k = \sigma(\hat{\Sigma}_b^k)$$

其中 $\pi_b^k$ 为第 $k$ 个分量的混合权重（经softmax），$\mu_b^k$ 为均值（恒等映射），$\Sigma_b^k$ 为方差（经sigmoid确保正值），$b$ 表示边界框坐标维度。

**不确定性估计**：从GMM参数直接计算两类不确定性（Choi et al., 2019）：

$$u_{al} = \sum_{k=1}^K \pi^k \Sigma^k, \quad u_{ep} = \sum_{k=1}^K \pi^k \| \mu^k - \sum_{i=1}^K \pi^i \mu^i \|^2$$

偶然不确定性 $u_{al}$ 为分量方差的加权和，反映数据本身的不确定性；认知不确定性 $u_{ep}$ 为分量均值相对于混合均值的加权方差，反映模型对预测的分散程度——当不同分量给出分歧较大的预测时，认知不确定性升高。

### 3.2 定位头：GMM驱动的边界框回归

定位头为每个边界框坐标预测K分量GMM。对于第 $i$ 个正样本锚框与第 $j$ 个真实框的匹配，网络输出坐标偏移量的混合分布。定位损失采用GMM负对数似然：

$$\mathcal{L}_{loc} = -\sum_{i\in Pos}^N \sum_b \lambda_G^{ij} \log\bigl(\sum_{k=1}^K \pi_b^{ik} \mathcal{N}(\hat{g}_b^j | \mu_b^{ik}, \Sigma_b^{ik}) + \varepsilon\bigr)$$

其中 $\lambda_G^{ij}$ 为锚框-真实框匹配指示，$\hat{g}_b^j$ 为真实框坐标偏移，$\mathcal{N}(\cdot|\mu,\Sigma)$ 为高斯密度，$\varepsilon$ 防止数值下溢。该损失具有**损失衰减**效应——当预测方差较大（偶然不确定性高）时，损失自动降低，起到自适应正则化作用。

推理时，边界框坐标由各分量均值加权求和得到：$R_b = \sum_{k=1}^K \pi_b^k \mu_b^k$。

### 3.3 分类头：GMM驱动的类别分布建模

分类头为每个类别预测K分量GMM。通过重参数化技巧从分布中采样类别logits：

$$\hat{c}_p^k = \mu_p^k + \sqrt{\Sigma_p^k} \cdot \gamma, \quad \gamma \sim \mathcal{N}(0,1)$$

其中 $\mu_p^k$ 和 $\Sigma_p^k$ 分别为第 $p$ 类第 $k$ 分量的均值和方差。采样后的logits经softmax得到类别概率，再代入加权混合交叉熵损失（Type‑1）：

$$\mathcal{L}_{cl}^{Pos} = -\sum_{i\in Pos}^N \lambda_G^{ij} \sum_{k=1}^K \pi^{ik} (\hat{c}_G^j - \log\sum_{p=0}^C e^{\hat{c}_p^{ik}})$$

$$\mathcal{L}_{cl}^{Neg} = -\sum_{i\in Neg}^{M\times N} \sum_{k=1}^K \pi^{ik} (\hat{c}_0^i - \log\sum_{p=0}^C e^{\hat{c}_p^{ik}})$$

正样本损失对匹配的真实类别 $\hat{c}_G^j$ 计算，负样本损失对背景类计算，$M=3$ 为困难负样本挖掘比率。

### 3.4 高效分类头变体

为降低参数量，高效变体（Ours_eff）移除分类头的方差预测，直接利用类别概率的方差计算偶然不确定性：

$$u_{al} = \sum_{k=1}^K \pi^k (\text{diag}(\hat{c}_p^k) - (\hat{c}_p^k)^{\otimes 2})$$

其中 $\hat{c}_p^k$ 为第 $k$ 分量的类别概率向量，$\text{diag}(\cdot)$ 提取对角线元素，$(\cdot)^{\otimes 2}$ 表示外积。该变体在VOC07上精度与完整GMM相当（Table 1），但参数从52.35M降至41.12M。

### 3.5 总体训练目标

完整训练损失结合定位与分类损失：

$$L = \begin{cases} \frac{1}{N} (\mathcal{L}_{loc}/\eta + \mathcal{L}_{cl}^{Pos} + \mathcal{L}_{cl}^{Neg}), & \text{if } N > 0 \\ 0, & \text{otherwise} \end{cases}$$

其中 $N$ 为正样本数量，$\eta=1$ 为定位损失权重。

### 3.6 不确定性聚合评分函数

对于每张图像，首先对每个检测目标的四种不确定性（定位偶然/认知、分类偶然/认知）进行z-score归一化，使不同尺度的不确定性可比。随后取所有目标所有不确定性中的**最大值**作为该图像的信息量得分。消融实验（Table 2）表明，最大聚合显著优于单独使用任一类不确定性（提升约0.9 mAP），也优于求和聚合。其有效性根源在于定位与分类不确定性选择的图像重叠率仅为14%（Table 3），证明两者提供高度互补的信息。

## 实验与关键发现

### 概率建模对检测精度的基准影响

在引入主动学习之前，作者首先验证了混合密度网络（MDN）改造对检测器本身精度的影响。**Table 1** 报告了在PASCAL VOC07和MS-COCO上，不同概率建模实例与原始SSD的mAP对比。核心发现如下：

![[assets/figures/papers/paper_list_l7_https_arxiv_org_abs_2103_16130/figures/003_Table_1.jpg]]
*Table 1: mAP (in %) of different instances of our approach compared to the original SSD network. SGM and MDN refer to single and multiple Gaussian models, and we apply those to localization (Loc), classification (Cl), and their combination (Loc+Cl)*

- **单高斯（SGM）与多高斯（MDN）的差异**：在定位头上使用MDN（K个分量的GMM）相比SGM（单高斯），在VOC07的IoU>0.75指标上获得显著提升（46.01 vs 43.36），表明多模态分布能更好地捕获边界框回归中的复杂不确定性。在分类头上，MDN同样优于SGM。
- **定位+分类联合建模**：将定位和分类头同时替换为MDN（Ours_gmm Loc+Cl）在VOC07 IoU>0.75上达到46.11，在MS-COCO上达到19.62，均优于单独改造任一头部的配置。这证明**定位与分类的不确定性建模具有互补性**。
- **高效变体（Ours_eff）**：移除分类头方差参数的高效变体在VOC07上达到46.18（IoU>0.75），与完整GMM持平，同时参数量更少（41.12M vs 52.35M），验证了**式8**中用类别概率方差替代GMM方差计算偶然不确定性的有效性。
- **正则化效应**：所有概率模型在标准IoU>0.5指标上也一致超越SSD基线（VOC07上Ours_eff 70.45 vs SSD 69.83），归因于偶然不确定性带来的损失衰减正则化。

### 不确定性聚合策略的消融实验

主动学习的核心在于如何将多种不确定性聚合为每张图像的信息量得分。**Table 2** 在VOC07上系统比较了不同聚合函数的主动学习效果（第3轮，4k标注图像）：

![[assets/figures/papers/paper_list_l7_https_arxiv_org_abs_2103_16130/figures/005_Table_2.jpg]]
*Table 2: VOC07: Comparison of scoring aggregation functions for active learning based on the aleatoric uncertainty, epistemic uncertainty, and their combination of each task*

- **单一不确定性**：单独使用定位偶然不确定性（Loc Aleatoric）或分类认知不确定性（Cl Epistemic）均不如组合方案，mAP差距约0.5-0.9。
- **最大聚合 vs 求和聚合**：对四种不确定性（定位偶然/认知 + 分类偶然/认知）取最大值（Max All），在第3轮达到**69.43 mAP**，比求和聚合（Sum All）高约0.3，且比随机采样高0.96。最大值聚合的优势在于**避免某类不确定性主导得分**，确保每张图像由最显著的不确定性维度驱动选择。
- **互补性证据**：**Table 3** 进一步揭示了定位与分类不确定性选择图像的重叠率仅为**14%**，而同一任务内偶然与认知不确定性的重叠率分别为48%（定位）和33%（分类）。这直接解释了为何聚合四种不确定性优于单一类型——定位和分类不确定性指向几乎不重叠的困难样本集合，联合使用能覆盖更多样化的信息量维度。

![[assets/figures/papers/paper_list_l7_https_arxiv_org_abs_2103_16130/figures/007_Table_3.jpg]]
*Table 3: Overlapping ratio (in %) of selected images as a function of the type of uncertainty used. Table 4: VOC07: Comparison of mAP and computing cost of active learning with most relevant approaches. Para. and sec refer to parameters and seconds, respectively*

### 与现有主动学习方法的全面对比

#### PASCAL VOC07 主结果

**Table 4** 展示了VOC07主动学习第3轮（4k标注图像）的精度与计算成本对比：

| 方法 | mAP (%) | 参数量 (M) | 前向时间 (s) |
|------|---------|-----------|-------------|
| Random | 68.47±0.09 | 26.29 | 0.016 |
| Entropy [33] | 68.39±0.12 | 26.29 | 0.016 |
| Core-set [34] | 68.50±0.07 | 26.29 | 0.016 |
| LLAL [40] | 68.60±0.12 | 26.29 | 0.016 |
| MC-dropout [11] | 69.52±0.17 | 26.29 | **0.412** |
| Ensemble [16] | 69.49±0.10 | 78.87 | 0.069 |
| **Ours_gmm** | **69.43±0.11** | 52.35 | 0.031 |
| **Ours_eff** | 69.11±0.12 | 41.12 | 0.029 |

**关键结论**：
- Ours_gmm以**69.43 mAP**显著超越所有单模型方法（LLAL 68.60、Core-set 68.50等），验证了显式建模定位+分类不确定性的优势。
- 与多模型方法MC-dropout（69.52）和Ensemble（69.49）精度持平，但**前向时间仅为MC-dropout的1/13**（0.031s vs 0.412s），参数效率也远优于Ensemble（52.35M vs 78.87M）。
- Ours_eff在略降0.32 mAP的代价下，参数量减少21%，前向时间缩短6%，在资源受限场景下是更优选择。

#### PASCAL VOC07+12 全量训练

**Figure 4** 展示了VOC07+12上从2k到10k标注图像的主动学习曲线：
- **Figure 4a**：与单模型方法对比，Ours_gmm在所有标注量下均保持领先，最终10k时达到**75.98 mAP**，比LLAL（73.38）高2.6，比Entropy（71.17）高4.81。
- **Figure 4b**：与多模型方法对比，Ours_gmm的曲线与MC-dropout（75.67）和Ensemble（75.90）几乎重合，但**Figure 5**显示其计算成本仅为MC-dropout的1/20（前向时间0.031s vs 0.618s@50次前向），参数量也远低于Ensemble。

#### MS-COCO 大规模验证

**Table 5** 在MS-COCO上第3轮（7k标注图像）的结果进一步验证了方法的可扩展性：

![[assets/figures/papers/paper_list_l7_https_arxiv_org_abs_2103_16130/figures/010_Table_5.jpg]]
*Table 5: MS-COCO: Comparison of mAP and computing cost of active learning with most relevant methods. Para. and sec refer to parameters and seconds, respectively*

| 方法 | mAP (%) | 参数量 (M) | 前向时间 (s) |
|------|---------|-----------|-------------|
| Random | 28.69±0.11 | 26.29 | 0.016 |
| MC-dropout | 30.49±0.13 | 26.29 | 0.412 |
| Ensemble | 30.52±0.09 | 78.87 | 0.069 |
| **Ours_gmm** | **30.51±0.12** | 52.35 | 0.031 |

Ours_gmm以30.51 mAP与MC-dropout（30.49）和Ensemble（30.52）持平，比随机采样高**1.82 mAP**，且计算成本优势在COCO的80类别、大规模场景下更为突出。

### 方法迁移性与鲁棒性

#### 跨架构迁移

**Table 6** 展示了将MDN改造应用于两阶段检测器Faster R-CNN（FPN）的结果：
- Ours_gmm在VOC07上达到78.55 mAP，比Faster R-CNN基线（77.42）提升**1.13 mAP**。
- **Table 7** 进一步验证了数据集的可迁移性：使用Ours_gmm在SSD上选择的标注数据，迁移到Faster R-CNN、不同骨干网络（VGG→ResNet）训练时，仍比随机采样选择的等量数据提升最高**2.52 mAP**。这表明不确定性评分捕获的是**任务固有的困难样本特征**，而非特定模型架构的偏差。

#### 超参数敏感性

- **混合分量数K**（Table 8）：K=4在精度与计算成本间取得最佳平衡。K=2时mAP下降约0.3，K=8时精度不再提升但参数量和前向时间显著增加。
- **输入分辨率**（Table 9）：Ours_gmm在300×300和512×512分辨率下均一致优于SSD基线，证明概率建模的增益不依赖于特定输入尺度。
- **分类损失类型**（Table 14, Table 15）：Type-1损失（式5/9，加权混合交叉熵）在MS-COCO上明显优于Type-2损失（式10，直接交叉熵），但在VOC07上差异不大。这与COCO类别数多（80类）、类别分布更复杂有关——Type-1的混合权重机制能更好地处理类别不平衡，但仍存在权重集中于单一分量的趋势，是论文指出的**已知局限**。

### 定性分析与失败模式

**Figure 3** 提供了模型错误检测时四种不确定性的可视化示例：
- **假阳性**（Person误检）：分类偶然不确定性极高，定位不确定性较低，表明模型对“该区域是否为行人”的类别判断高度不确定。
- **定位偏差**（Person框不准）：定位认知不确定性显著升高，分类不确定性正常，反映模型对边界框位置的预测存在模型层面的不确定。
- **类别混淆**（Sheep→Bird / Sheep→Cow）：分类认知不确定性激增，定位不确定性保持低位，说明模型对细粒度类别区分缺乏知识。

![[assets/figures/papers/paper_list_l7_https_arxiv_org_abs_2103_16130/figures/004_Figure_3.jpg]]
*Figure 3: Examples of aleatoric and epistemic uncertainties for inaccurate detections, see more examples in the supplementary material. Starting from top-left image and going in clockwise direction: Person is a false positive; Person bounding box is not correct; A sheep is misclassified as a bird; A sheep is misclassified as a cow*

这些定性模式与**Table 3**的定量重叠率分析一致：定位和分类不确定性在不同失败模式下各自扮演主导角色，**最大聚合策略正是为了在任何一种不确定性信号强烈时都能触发样本选择**。

### 计算成本公平性说明

所有实验均使用相同训练超参数（batch size=32, lr=0.001, 120k iterations），进行三次独立试验并报告均值±标准差。计算成本测量基于单张300×300图像的推理时间，在相同硬件环境下完成。Ours_gmm的额外参数集中在检测头的最后一层（GMM参数预测），不改变骨干网络结构，因此前向时间的增加（0.016s→0.031s）远小于MC-dropout的多前向累积（0.412s@25次）。

## 定位与知识库关联

### 1. 方法在主动学习谱系中的位置

目标检测领域的主动学习方法大致可分为三类：基于单模型不确定性、基于多模型不确定性和基于特征多样性的方法。本文提出的AL-MDN属于第一类，但其核心创新在于通过概率建模将单模型的信息量度量能力提升至与多模型方法相当的水平。

**单模型基线**方面，AL-MDN直接对比了三种代表性工作：基于分类熵的**Entropy**方法（Roy et al., BMVC 2018）、基于特征空间覆盖的**Core-set**方法（Sener & Savarese, ICLR 2018）和通过学习预测任务损失来选择样本的**LLAL**方法（Yoo & Kweon, CVPR 2019）。这些方法的共同瓶颈在于：要么仅利用分类不确定性而忽略定位不确定性，要么需要额外的损失预测模块。AL-MDN通过混合密度网络在单次前向传播中同时捕获定位与分类的偶然不确定性和认知不确定性，在VOC07+12全量训练中达到75.98 mAP，显著超过LLAL的73.38（Figure 4, Table 12），证明了显式概率建模相对于隐式损失预测的优势。

**多模型基线**方面，AL-MDN与**MC-dropout**（Feng et al., IV 2019）和**Ensemble**（Haussmann et al., IV 2020）进行了系统对比。MC-dropout需要多次随机前向传播（通常10-20次）来估计不确定性，Ensemble需要训练和推理多个独立模型。AL-MDN在精度上与两者持平（75.98 vs. MC-dropout 75.67 vs. Ensemble 75.90），但前向时间仅为MC-dropout的1/20（0.031s vs. 0.412s），参数量也远低于Ensemble（52.35M vs. 78.87M）（Figure 5, Table 12）。这一结果表明，精心设计的单模型概率化输出可以替代笨重的多模型不确定性估计。

### 2. 概率目标检测的知识库定位

AL-MDN的技术根基是将混合密度网络（Mixture Density Networks, MDN）引入目标检测的输出层。这一设计与以下工作形成知识谱系：

- **单高斯模型（SGM）**：仅预测单个高斯分布的均值和方差，是MDN的特例（K=1）。Table 1显示，SGM在VOC07上的mAP（IoU>0.75）为44.37%，低于MDN的46.11%，说明多模态分布在捕获复杂不确定性方面具有本质优势。
- **标准SSD**：确定性输出，mAP（IoU>0.75）为43.36%，是AL-MDN的改造起点。AL-MDN将定位头的确定性回归替换为K分量GMM的均值、方差和权重预测（Eq. 2），将分类头的确定性softmax替换为基于GMM的类别分布建模（Eq. 4），并通过重参数化技巧实现端到端训练。
- **高效变体（Ours_eff）**：为进一步降低参数开销，分类头移除了方差估计，改为直接从类别概率计算偶然不确定性（Eq. 8）。该变体在VOC07上达到46.18% mAP（IoU>0.75），与完整GMM版本（46.11%）相当，但参数量从52.35M降至41.12M（Table 1, Table 4）。

### 3. 适用边界与局限性

**已验证的适用范围**：
- 数据集：PASCAL VOC07、VOC07+12和MS-COCO，覆盖中小规模和大规模目标检测场景。
- 检测架构：单阶段检测器SSD（主要实验）和两阶段检测器Faster R-CNN with FPN（迁移验证，Table 6显示最高1.13 mAP提升）。
- 骨干网络：VGG16和ResNet系列，Table 7显示数据集获取策略可迁移至不同骨干网络，相对随机采样最高提升2.52 mAP。
- 主动学习设置：逐轮递增标注预算的池式主动学习，每轮选择固定数量的未标注图像。

**已知局限**：
1. **混合分量数K是固定超参数**：实验表明K=4在精度与计算成本间取得最佳平衡（Table 8），但该值可能需要根据数据集规模、类别数和标注预算手动调整，缺乏自适应机制。
2. **分类损失存在权重集中偏差**：Type-1分类损失（Eq. 5/9）在训练过程中倾向于将混合权重集中于单一分量，削弱了GMM的多模态表达能力。高效变体（Ours_eff）通过移除方差参数部分缓解了这一问题，但在MS-COCO等大规模数据集上，Type-1损失仍显不足（Table 14, Table 15），需要设计更优的分类损失函数。
3. **检测框架覆盖有限**：主要实验基于SSD，虽然在Faster R-CNN上展示了迁移性，但未在Anchor-free检测器（如CenterNet、FCOS）或Transformer-based检测器（如DETR）上进行验证。

### 4. 开放问题

1. **分类损失设计**：如何设计既能减轻混合权重集中偏差、又能在极大类别数（如MS-COCO的80类）下保持甚至提升主动学习性能的分类损失函数？Type-1损失在VOC07（20类）上表现良好，但在MS-COCO上的退化表明类别数量是关键变量。
2. **极端场景适应性**：该方法在类别分布极度不平衡（如长尾分布）、域偏移（如从自然图像到医学图像）或开放词汇检测等复杂场景下的不确定性估计质量如何？GMM的先验假设（高斯分布）在这些场景下可能不再成立。
3. **与特征多样性策略的结合**：当前方法仅依赖不确定性进行样本选择。能否将显式不确定性估计与基于特征空间覆盖（如Core-set）或多样性采样的策略结合，在信息量和代表性之间取得更好的平衡？
4. **计算效率的进一步优化**：虽然AL-MDN的单次前向传播已远快于MC-dropout和Ensemble，但GMM头仍引入了额外参数（约11M）。能否通过知识蒸馏或参数共享进一步压缩模型，使其更适合边缘设备上的主动学习部署？

## 原文 PDF

![[paperPDFs/ICCV_2021/Active_Learning_for_Deep_Object_Detection_via_Probabilistic_Modeling.pdf]]
