---
title: "Not All Labels Are Equal: Rationalizing The Labeling Costs for Training Object Detection"
type: paper
paper_level: A
venue: CVPR
year: 2022
pdf_ref: paperPDFs/CVPR_2022/Not_All_Labels_Are_Equal_Rationalizing_The_Labeling_Costs_for_Training_Object_Detection.pdf
project_link: https://github.com/NVlabs/AL-SSL
aliases:
- UALRPL
- NALAERLCTOD
tags:
- CVPR_2022
- topic/optimization_theory_probabilistic
- topic/optimization_theory_probabilistic/optimization_methods
core_operator: "将获取函数从纯不确定度（max entropy）修改为融合了不一致性（鲁棒性）与不确定度的乘积得分，使其对类别偏差具有鲁棒性；同时引入高置信度伪标签机制（τ=0.99）来抑制分布漂移，使数据集在标注和自动标注之间保持代表性。"
primary_logic: "网络对图像及其水平翻转增强的预测不一致性是一种类别无关、更可靠的标注价值信号，尤其在低表现类别中大幅超越熵；配合高阈值伪标签可以防止主动学习导致的数据集分布偏移，从而实现全类别性能的均衡提升。"
claims:
- "不一致性主动学习在VOC07+12的低表现类别（如Bottle）上相对熵方法提升高达24%。"
- "统一获取函数（H×I）加上伪标签后，在MS-COCO第1周期于76%的类别中超越了随机采样。"
- "在PASCAL VOC07+12的第5周期，本方法mAP达到75.60，远超随机基线（69.27）和最佳现有方法PM（74.29）。"
- "单独使用伪标签效果微弱，必须与统一获取函数配合才能发挥最大作用。"
---

# Not All Labels Are Equal: Rationalizing The Labeling Costs for Training Object Detection

> [!tip] 核心洞察
> 网络对图像及其水平翻转增强的预测不一致性是一种类别无关、更可靠的标注价值信号，尤其在低表现类别中大幅超越熵；配合高阈值伪标签可以防止主动学习导致的数据集分布偏移，从而实现全类别性能的均衡提升。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 并非所有标签都平等：合理化目标检测的标注成本 |
| 英文题名 | Not All Labels Are Equal: Rationalizing The Labeling Costs for Training Object Detection |
| 会议/期刊 | CVPR 2022 |
| Links | [paper](https://arxiv.org/abs/2106.11921); [GitHub](https://github.com/NVlabs/AL-SSL) |
| Topic | #topic/optimization_theory_probabilistic #topic/optimization_theory_probabilistic/optimization_methods |
| Method | Unified Active Learning with Robustness and Pseudo-labeling |
| Dataset | PASCAL VOC07+12, MS-COCO |

> [!tip] 效果简介
> - PASCAL VOC07+12 上，mAP 为 75.60 ± 0.2，对比 Random Sampling 69.27 ± 0.2，变化 +6.33。
> - PASCAL VOC07+12 上，mAP 为 75.60 ± 0.2，对比 PM (Best AL) 74.29 ± 0.2，变化 +1.31。
> - MS-COCO 上，mAP 为 32.80 ± 0.0，对比 Random Sampling 31.47 ± 0.3，变化 +1.33。

## 概述

**问题与瓶颈**：目标检测的主动学习（Active Learning, AL）旨在以最小标注成本获得最大性能收益。然而，现有基于不确定度（如最大熵）的获取函数存在严重的类别偏差——它们倾向于选择网络已表现良好的高表现类别样本，而对真正需要标注的低表现类别（如PASCAL VOC中的Bottle、Pottedplant）反而失效，因为网络对这些类别的预测不可靠，熵值本身已失去指示意义。同时，单独选择困难样本会导致训练数据分布漂移。另一方面，半监督学习中的伪标签方法在最需要指导的低表现类别上反而可能生成高置信度的错误伪标签，进一步损害训练（Figure 1）。

**核心思路**：本文提出一种统一的主动学习框架，其核心洞察是：网络对原始图像及其水平翻转增强的预测不一致性，是一种类别无关、更可靠的标注价值信号。具体而言，方法将获取函数从纯不确定度（最大熵 $H(\Delta)$）修改为融合了不一致性与不确定度的乘积得分 $A(\Delta) = H(\Delta) \times I(\Delta)$，其中不一致性 $I(\Delta)$ 基于原始与增强预测之间的对称KL散度，使其对类别偏差具有鲁棒性。同时，引入极高阈值（$\tau = 0.99$）的类别无关伪标签机制，并修改MultiBox损失以避免对无标注区域的假阳性惩罚，从而抑制分布漂移，使数据集在人工标注与自动标注之间保持代表性。

**方法定位**：该方法处于主动学习与半监督学习的交叉点。与纯不确定度AL方法（Entropy、Core-Set、Ensemble、MC-dropout、PM等）相比，它引入了鲁棒性信号作为获取准则；与纯半监督方法（SSL-cons.、SSL-PL）相比，它将伪标签与主动选择有机结合，而非独立使用。整体训练采用一致性正则化（分类KL损失 + 定位L2损失）作用于全部未标注数据，配合标注损失和伪标签损失进行联合优化。

**主要结果**：在PASCAL VOC07+12上，本方法在第5周期达到75.60 mAP，远超随机采样基线（69.27）和最佳现有AL方法PM（74.29），相对提升最高达7.7%。在MS-COCO上，本方法达到32.80 mAP，优于随机采样（31.47）和PM（31.86），相对提升约7%。尤为关键的是，在VOC的低表现类别（如Bottle）上，不一致性驱动的主动学习相对熵方法提升高达24%（Figure 5），且在MS-COCO第1周期于76%的类别中超越了随机采样（Figure 10），验证了方法的类别均衡性。消融实验证实：伪标签单独使用效果微弱，必须与统一获取函数配合才能发挥最大作用；极高阈值 $\tau = 0.99$ 是伪标签质量的关键（错误率仅3.7%）；SSL训练是不一致性获取函数生效的必要条件。

## 背景与动机

目标检测的深度模型依赖大规模精确标注数据，但标注成本高昂。主动学习（Active Learning, AL）和半监督学习（Semi-Supervised Learning, SSL）是降低标注成本的两条主流路径，然而在目标检测场景中，现有方法存在一个被忽视的结构性缺陷：**类别偏差**。

### 现有方法的隐性假设与失效模式

基于不确定度的主动学习（如最大熵采样）隐含假设网络对“不确定”样本的判断是可靠的。但在目标检测中，网络对高表现类别（如“Car”、“Horse”）的预测通常校准良好，而对低表现类别（如“Bottle”、“Pottedplant”）的预测则不可靠——低表现类别的样本往往呈现低熵，使得不确定度方法系统性地忽略这些最需要指导的样本。如 **Figure 1(a)** 所示，一个来自低表现类别“Pottedplant”的样本因其低熵而不会被基于不确定度的AL方法选中标注。

同时，单独选择困难样本会导致训练数据分布漂移（distribution drift），使标注池逐渐偏离原始数据分布，损害模型的泛化能力。

伪标签半监督方法面临镜像问题：网络对高置信度但实际错误的预测（常见于低表现类别）会生成错误伪标签，反而污染训练信号（**Figure 1(b)**）。一致性半监督方法则因为网络在低表现类别上对增强变换的预测不一致，无法从中学习有效信息（**Figure 1(c)**）。

### 核心动机：打破类别偏差的闭环

上述三种方法的失效形成了一个闭环：不确定度AL忽略低表现类别 → 伪标签SSL在这些类别上产生错误监督 → 一致性SSL无法利用这些样本 → 低表现类别始终得不到改善。本文的核心动机是**同时打破这个闭环的两个关键节点**：

1. **设计类别无关的标注价值信号**：不再依赖网络预测的绝对不确定度，而是利用网络对图像增强变换（水平翻转）的预测不一致性作为获取函数，使低表现类别的有价值样本也能被有效识别。
2. **抑制主动学习引发的分布漂移**：通过高置信度伪标签机制（阈值 $\tau=0.99$）自动标注低信息量样本，使训练集在人工标注和自动标注之间保持代表性。

这一动机在 **Figure 1(d)** 中得到具象化：所提方法既能选中“Pottedplant”样本进行人工标注，又能防止其被错误伪标签，从而实现对全类别性能的均衡提升。

## 核心创新

本文的核心创新并非提出一种全新的主动学习范式，而是通过**重新设计获取函数**和**引入高置信度伪标签机制**，系统性地修复了现有基于不确定度的主动学习在目标检测中的两个结构性缺陷：类别偏差与分布漂移。这两个改动相互配合，构成了一个统一的主动学习框架。

### 改动槽位一：从纯不确定度到“不确定度 × 不一致性”的统一获取函数

**基线做法**：现有主动学习方法（如 Entropy-based AL、PM ）仅依赖网络预测的不确定度（如最大熵 $H(\Delta)$）来选择待标注样本。这种策略天然偏向高表现类别——网络对已学好的类别预测置信度高、熵值低，因此这些类别的困难样本不会被选中；而低表现类别的样本因网络预测不可靠，熵值反而可能较低，导致获取函数失效。

**提出方案**：将获取函数修改为最大熵与最大不一致性的乘积：

$$A(\Delta) = H(\Delta) \times I(\Delta)$$

其中 $I(\Delta)$ 基于图像与其水平翻转增强版本的预测之间的 KL 散度：

$$\mathcal{L}_{con_C}(c_i', \hat{c}_i) = \frac{1}{2}[KL(c_i', \hat{c}_i) + KL(\hat{c}_i, c_i')]$$

**核心洞察**：网络对图像及其增强的预测不一致性是一种**类别无关**的信号——它不依赖网络对某个类别的绝对置信度，而是反映网络对该样本的“鲁棒性”。在低表现类别（如 Bottle、Pottedplant）上，即使熵值不高，不一致性依然能有效暴露网络的知识盲区。Figure 5 的每类别分析显示，不一致性主动学习在 Bottle 类上相对熵方法提升高达 24%，在 Pottedplant 和 Chair 上分别提升 14% 和 18%。消融实验（Table 3b）进一步表明，统一得分（Combined）在第 5 周期比纯熵高 0.21 mAP，比纯不一致性高 0.08 mAP，验证了两者互补的有效性。

### 改动槽位二：类别无关的高置信度伪标签策略

**基线做法**：传统伪标签方法（如 SSL-PL ）通常按类别取 top-k% 最置信预测生成伪标签，或使用较低阈值。这导致两个问题：一是高表现类别产生大量伪标签而低表现类别几乎得不到伪标签，加剧类别不平衡；二是低阈值引入错误伪标签，损害训练。

**提出方案**：采用**类别无关的统一阈值** $\tau=0.99$ 生成伪标签：

$$\hat{y}_i^p = \begin{cases} 1, & \text{if } p = \arg\max(\boldsymbol{c}_i) \text{ and } \boldsymbol{c}_i^p \ge \tau \\ 0, & \text{otherwise.} \end{cases}$$

同时修改 MultiBox 损失，使未标注区域不产生假阳性惩罚，避免伪标签图像中未被伪标注的目标被错误地当作背景抑制。

**核心洞察**：极高阈值（$\tau=0.99$）将伪标签错误率降至仅 3.7%（Table 1b），远优于较低阈值。Figure 8 显示，伪标签增益在早期主动学习周期最大（达 3.7%），此时伪标签数量约占总标签一半时效果最佳。关键在于，伪标签并非单独使用——Figure 3b/4b 表明单独使用伪标签效果微弱，必须与统一获取函数配合才能发挥最大作用：获取函数负责挑选真正需要人工标注的困难样本，伪标签则自动标注高置信度的简单样本，两者共同抑制主动学习导致的数据分布漂移。

### 两个改动的协同机制

这两个改动槽位形成了“标注—自动标注”的分工闭环：统一获取函数 $H(\Delta) \times I(\Delta)$ 确保低表现类别的困难样本被优先送交人工标注（解决类别偏差），而高阈值伪标签自动吸收高置信度样本（抑制分布漂移）。一致性正则化训练（式 9-10）作为支撑条件，对全部未标注数据施加分类和定位一致性损失，使网络保持对增强变换的鲁棒性，从而让不一致性信号和伪标签质量随训练持续改善。消融实验（Table 1a）证实，SSL 训练是不一致性获取函数生效的必要条件——无 SSL 时不一致性 AL 表现不及随机采样。

## 整体框架

本文提出一个统一框架，将主动学习（Active Learning, AL）与半监督学习（Semi-Supervised Learning, SSL）协同整合，在目标检测的标注预算约束下实现全类别性能的均衡提升。框架的核心设计围绕一个关键观察展开：现有基于不确定度（如最大熵）的主动学习方法偏向高表现类别，对低表现类别因网络预测不可靠而失效；而单独使用伪标签或一致性正则化同样无法有效处理这些困难样本（参见 Figure 1 的动机示意）。

整个流程可分为三个串联的模块，如 Figure 2 所示：

**1. 半监督预训练阶段。** 在每个主动学习周期开始时，首先对当前已有的标注数据与未标注数据进行半监督训练。训练损失由三部分组成：改进的多盒分类损失（仅作用于标注和伪标注区域）、分类与定位一致性损失（作用于全部未标注数据），以及定位回归损失。一致性损失通过水平翻转增强构造原始图像与增强图像的预测对，分别计算对称KL散度（分类一致性）和L2偏移损失（定位一致性），引导网络对增强变换保持鲁棒预测。此阶段为后续的主动学习决策提供可靠的预测基础——消融实验表明，若无SSL训练，不一致性主动学习甚至不及随机采样（Table 1a）。

**2. 主动学习决策阶段。** 训练完成后，对每张未标注图像计算一个统一的获取分数 $A(\Delta) = H(\Delta) \times I(\Delta)$（Eq. 5）。其中 $H(\Delta)$ 为图像内所有检测框的最大预测熵，反映网络对该样本的不确定度；$I(\Delta)$ 为图像内所有检测框的最大不一致性，基于原始图像与水平翻转增强图像预测之间的对称KL散度 $\mathcal{L}_{con_C}(c_i', \hat{c}_i) = \frac{1}{2}[KL(c_i', \hat{c}_i) + KL(\hat{c}_i, c_i')]$（Eq. 2）计算。该乘积得分同时捕捉了“网络不知道什么”和“网络对变换不鲁棒什么”两个维度的标注价值，且不一致性信号天然具有类别无关特性，使其在低表现类别上大幅超越纯熵方法（Figure 5 显示在 Bottle 类上相对提升高达24%）。

根据获取分数，框架将未标注图像分为三条处理路径：
- **高分数样本**：提交人工标注，纳入下一周期的标注集。
- **中等分数样本**：若其预测置信度不低于极高阈值 $\tau = 0.99$，则自动生成伪标签（Eq. 6），以零成本扩充标注集。
- **低分数样本**：仅作为无标注数据参与一致性训练，不产生任何标签。

**3. 伪标签与损失修正。** 伪标签生成采用类别无关的统一阈值策略（$\tau = 0.99$），而非传统的按类别取top-k%。Table 1b 显示该阈值仅产生3.7%的错误伪标签，降低阈值会显著损害性能。关键的是，框架修改了标准多盒损失，使其仅对存在伪标签的区域计算分类损失，避免将未标注区域中的预测错误地惩罚为假阳性。伪标签增益在早期主动学习周期最大（约3.7%），当伪标签数量约占总标签一半时效果最佳（Figure 8b），且必须与统一获取函数配合才能发挥最大作用——单独使用伪标签仅带来微弱增益（Figure 3b/4b）。

**输入输出流总结**：每个周期以“部分标注图像 + 大量未标注图像”为输入，经半监督训练后输出网络预测，预测经统一获取函数评分后分流为人工标注、自动伪标注和纯无标注三类，三者共同构成下一周期的训练数据。该闭环机制使得数据集在人工标注和自动标注之间保持代表性，有效抑制了纯主动学习可能导致的数据分布漂移。

### 补充图表

![[assets/figures/papers/paper_list_l33_https_arxiv_org_abs_2106_11921/figures/006_Figure_5.jpg]]
*Figure 5: VOC07+12. In the bar plots we show the accuracy per class using random sampling in the zeroth and last cycle. We present the results of each AL method for the three best-performing (”Train”, ”Car”, and ”Horse”) and worst-performing (”Bottle”, ”Pottedplant”, and ”Chair”) classes*

![[assets/figures/papers/paper_list_l33_https_arxiv_org_abs_2106_11921/figures/014_Table_3.jpg]]
*Table 3: VOC07+12. a) Comparison to two semi-supervised learning methods. We initially use 2, 000 randomly sampled images and, in every other cycle, we label 1, 000 extra images. Our method outperforms both of them by a large margin. b) Ablation study on the effect of entropy, inconsistency, unified score, and our method in VOC07+12. We observe that doing active learning with either entropy or consistency outperforms the semi-supervised model, that the unified score performs better than either of the individual scores, and that our method reaches the best overall results. (1)*

## 核心模块与公式推导

本文方法由三个紧密协作的核心模块构成：**基于不一致性的获取分数计算**、**高置信度伪标签生成**，以及**一致性正则化训练**。三个模块围绕一个统一目标——在主动学习周期中既选出最有标注价值的样本，又充分利用剩余未标注数据防止分布漂移。

### 模块一：不一致性获取分数计算

传统基于熵的不确定度主动学习存在严重的类别偏差：网络对低表现类别（如 Bottle、Pottedplant）的预测置信度往往较低，但熵值却不高，导致这些真正需要标注的困难样本被忽略。本文的核心洞察是：**网络对同一图像在水平翻转增强前后的预测不一致性，是一种类别无关、更可靠的标注价值信号**。

具体计算流程如下：

1. **预测匹配**：对输入图像 $I$ 及其水平翻转版本 $I'$，分别通过网络获得预测框集合 $\{b\}$ 和 $\{\hat{b}\}$。通过最大化 IoU 建立匹配关系：

   $$\Delta_i' = \arg\max_{b_i \in \{b\}} \text{IoU}(b_i, \hat{b}_i)$$

   其中 $\Delta_i'$ 表示增强图像中第 $i$ 个预测框在原始图像中的最佳匹配框。

2. **类别不一致性**：对匹配后的预测对 $(c_i', \hat{c}_i)$，采用对称 KL 散度度量类别预测的不一致性：

   $$\mathcal{L}_{con_C}(c_i', \hat{c}_i) = \frac{1}{2}[KL(c_i', \hat{c}_i) + KL(\hat{c}_i, c_i')] \tag{Eq. 2}$$

   该对称形式确保度量与增强方向无关，且对低置信度预测的微小扰动敏感。

3. **图像级不一致性得分**：取图像内所有匹配对中不一致性的最大值，作为该图像的不一致性得分 $I(\Delta)$：

   $$I(\Delta) = \max_i \mathcal{L}_{con_C}(c_i', \hat{c}_i)$$

   采用最大值而非均值的原因是：即使图像中大部分区域预测一致，只要存在一个高度不一致的区域（通常是困难目标），该图像就值得标注。

4. **统一获取函数**：将最大熵 $H(\Delta)$ 与最大不一致性 $I(\Delta)$ 相乘，得到最终的图像级获取分数：

   $$A(\Delta) = H(\Delta) \times I(\Delta) \tag{Eq. 5}$$

   乘积形式确保只有同时具有高不确定度和高不一致性的样本才会被优先选中，从而兼顾信息量和鲁棒性两个维度。

### 模块二：高置信度伪标签生成

在每轮主动学习周期中，未被人工标注的图像并非完全无用。本文提出利用网络的高置信度预测自动生成伪标签，以扩充训练集并抑制分布漂移。

伪标签的生成条件极为严格，仅当预测置信度不低于阈值 $\tau$ 时才生成：

$$\hat{y}_i^p = \begin{cases} 1, & \text{if } p = \arg\max(\boldsymbol{c}_i) \text{ and } \boldsymbol{c}_i^p \ge \tau \\ 0, & \text{otherwise.} \end{cases} \tag{Eq. 6}$$

其中 $\boldsymbol{c}_i^p$ 表示第 $i$ 个预测框属于类别 $p$ 的置信度。本文采用 $\tau = 0.99$ 的极高阈值，实验表明该设置下伪标签错误率仅为 3.7%，而降低阈值会显著损害性能（见 Table 1b 和 Figure 8）。

关键设计在于**修改后的 MultiBox 损失**：标准 MultiBox 损失会将所有未匹配到真实标签的预测框视为负样本进行惩罚。但对于伪标签图像，仅部分区域有伪标签，其余区域并无标注。若沿用标准损失，无伪标签区域的预测将被错误地当作假阳性惩罚。修改后的损失仅对有伪标签的区域计算分类损失，其余区域忽略，从而避免假阳性惩罚。

### 模块三：一致性正则化训练

SSL（半监督学习）训练是使不一致性获取函数生效的**必要条件**。消融实验（Table 1a）表明，若无 SSL 训练，仅凭不一致性进行主动学习甚至不及随机采样。

本文的 SSL 训练对全部未标注数据施加两类一致性损失：

1. **分类一致性损失**：即前文定义的对称 KL 散度 $\mathcal{L}_{con_C}$，约束原始图像与增强图像的类别预测一致。

2. **定位一致性损失**：对匹配框的定位偏移施加 L2 损失。考虑到水平翻转后边界框坐标的几何对应关系（$\delta x$ 符号反转，$\delta y$ 不变），定位一致性损失定义为：

   $$\mathcal{L}_{con_L}(b_i', \hat{b}_i) = \frac{1}{4}\left(||\delta x_i' - (-\delta \hat{x}_i)||^2 + ||\delta y_i' - \delta \hat{y}_i||^2 + ||\delta w_i' - \delta \hat{w}_i||^2 + ||\delta h_i' - \delta \hat{h}_i||^2\right)$$

3. **总一致性损失**为分类与定位一致性损失的期望和：

   $$\mathcal{L}_{con} = \mathbb{E}[\mathcal{L}_{con_C}(\boldsymbol{c}', \hat{\boldsymbol{c}})] + \mathbb{E}[\mathcal{L}_{con_L}(\boldsymbol{b}', \hat{\boldsymbol{b}})] \tag{Eq. 9}$$

4. **整体训练损失**由三部分组成：

   $$\mathcal{L}_{total} = \mathcal{L}_{conf} + \mathcal{L}_{con} + \mathcal{L}_1 \tag{Eq. 10}$$

   其中 $\mathcal{L}_{conf}$ 为修改后的 MultiBox 损失（涵盖人工标注和伪标签），$\mathcal{L}_1$ 为定位回归损失。

### 模块协同机制

三个模块在主动学习周期中形成闭环：SSL 训练使网络对增强变换具有鲁棒性，从而让不一致性信号变得可靠；高不一致性样本被选中进行人工标注，而低不一致性但高置信度的样本则自动生成伪标签；伪标签与一致性损失共同作用，防止训练数据分布向困难样本漂移。Figure 2 展示了这一完整流程：每张未标注图像根据获取分数被分入三条路径——人工标注、伪标签标注、或仅作为未标注数据参与下一轮 SSL 训练。

## 实验与分析

### 核心发现：统一获取函数与伪标签的协同效应

本方法在两个主流基准上均取得了显著且一致的性能提升。在PASCAL VOC07+12上，第5主动学习周期时本方法mAP达到**75.60**，远超随机采样基线（69.27）和此前最佳主动学习方法**PM**（74.29），相对提升分别为**+6.33**和**+1.31** mAP（Table 2）。在更具挑战性的MS-COCO上，本方法同样以**32.80** mAP领先随机采样（31.47）和PM（31.86），分别提升**+1.33**和**+0.94** mAP（Table 4）。值得注意的是，这些增益是在仅标注少量额外样本的条件下实现的——VOC上从2,000张初始标注扩展至7,000张（其中5,000张主动选择），COCO上从5,000张扩展至10,000张。

消融研究揭示了三个关键组件的各自贡献与协同机制（Table 3b、Table 5b）。在VOC第5周期，单独使用熵获取函数相比随机采样有提升，但将获取函数替换为统一得分$H(\Delta) \times I(\Delta)$后（不含伪标签），mAP进一步提高0.21；在此基础上引入伪标签机制后，mAP再跃升0.62，最终达到75.60。这一递进关系在COCO上同样成立，证实了不一致性信号与高置信度伪标签之间存在正向互补：不一致性负责识别最值得人工标注的困难样本，而伪标签则利用网络对简单样本的确定性预测来扩充训练集、抑制分布漂移。

### 类别级分析：低表现类别的突破性提升

Figure 5的每类别详细对比揭示了本方法的核心优势所在。在VOC07+12的三个最差表现类别（Bottle、Pottedplant、Chair）上，基于不一致性的主动学习相对熵方法取得了显著提升：Bottle类相对增益高达**24%**，Pottedplant类**14%**，Chair类**18%**。这一结果直接验证了核心洞察——熵在低表现类别上因网络预测不可靠而失效，而不一致性作为类别无关的信号，能够有效识别这些类别的有价值样本。

![[assets/figures/papers/paper_list_l33_https_arxiv_org_abs_2106_11921/figures/003_Figure.jpg]]

在MS-COCO的80个类别上，统一获取函数在**60%**的类别中超越了单独的熵方法（Figure 6a）。更关键的是，当统一获取函数配合伪标签后，在第1周期于**76%**的类别中超越了随机采样（Figure 10），这一比例远超纯主动学习方法，表明伪标签机制有效缓解了主动学习可能导致的数据集分布偏移问题。

![[assets/figures/papers/paper_list_l33_https_arxiv_org_abs_2106_11921/figures/016_Figure_10.jpg]]
*Figure 10: MS-COCO. The percentage of classes where our unified acquisition function outperforms random with and without pseudolabels. Numbers 1-5 represent the active learning cycle. Example: taking the entry ”unified with PL” in the y-axis, and ”random” in the x-axis in (1), we get the value 0.76 which means that our method outperforms the random acquisition function in 76% of classes during the first active learning cycle*

### 伪标签机制的关键设计选择

伪标签阈值$\tau$的选择对性能有决定性影响。实验表明，极高阈值$\tau=0.99$产生最佳伪标签正确率——仅**3.7%**的错误率（Table 1b）。降低阈值会导致错误伪标签比例急剧上升，从而损害训练质量。Figure 8进一步显示，伪标签增益在早期主动学习周期最为显著（可达3.7%），此时伪标签数量约占总标签的一半时效果最佳；但随着周期推进，即使网络性能提升、伪标签数量增多，增益反而逐渐减弱——这是一个值得注意的开放问题。

在伪标签策略上，本方法采用的类别无关统一阈值策略优于传统的按类别top-k%策略（Table 6a）。按类别选取最高置信度伪标签的方法会加剧类别间的不平衡，而统一阈值$\tau=0.99$确保只有真正高置信度的预测被转为伪标签，避免了低表现类别被错误伪标签污染的风险。

### SSL训练的必要性与采样策略

一个关键的消融发现是：**SSL训练是不一致性获取函数生效的必要条件**（Table 1a）。当网络仅使用有监督损失训练时，基于不一致性的主动学习表现甚至不及随机采样。这是因为不一致性信号的有效性依赖于网络在半监督训练过程中学习到的对增强变换的鲁棒性——只有经过一致性正则化训练的网络，其预测不一致性才能真实反映样本的标注价值。

在标注与未标注数据的采样比例上，实验表明平衡策略（一半标注、一半未标注）在所有主动学习周期均优于全随机或四分之一标注策略（Table 6b）。这一发现为实际部署提供了明确的指导：主动学习不应完全替代随机采样，而应在保持数据集代表性的前提下进行有选择的标注。

### 实验设置的公平性保障

所有实验均使用相同的SSD300检测器和VGG骨干网络，训练超参数完全一致（120K迭代，初始学习率0.001，在80K和100K迭代时衰减，batch size 32，L2正则0.0005）。每个实验使用相同的初始随机种子划分，并训练三个独立网络取平均以消除随机性影响。对比的主动学习方法均采用与原文一致的公开实现，确保了比较的公平性。

### 补充图表

![[assets/figures/papers/paper_list_l33_https_arxiv_org_abs_2106_11921/figures/005_Figure_4.jpg]]
*Figure 4: MS-COCO. Left: Comparison to state-of-the-art active learning methods; Middle: Comparison to the two SSL methods used in this work when they do not use AL; Right: Ablation study on the effect of entropy, inconsistency, unified score without pseudo-labeling, and our method. † denotes ensemble method; ‡ denotes mixture of SSD*

![[assets/figures/papers/paper_list_l33_https_arxiv_org_abs_2106_11921/figures/008_Figure_6.jpg]]
*Figure 6: MS-COCO. a) The percentage of classes where one acquisition function outperforms another; b) The percentage of classes where our unified acquisition function outperforms random with and without pseudo-labels. Example: taking the entry ”unified” in the y-axis, and ”entropy” in the x-axis, we get the value 0.69 which means that ”unified” acquisition function outperforms the ”entropy” acquisition function in 69% of classes*

![[assets/figures/papers/paper_list_l33_https_arxiv_org_abs_2106_11921/figures/010_Figure_8.jpg]]
*Figure 8: VOC07+12. Left: Accuracy as a function of τ for selecting pseudo-labels. Right: Accuracy improvement with respect to the pseudo-labels ratio to the entire labels*

![[assets/figures/papers/paper_list_l33_https_arxiv_org_abs_2106_11921/figures/013_Table.jpg]]
*Table: (a) (b)*

![[assets/figures/papers/paper_list_l33_https_arxiv_org_abs_2106_11921/figures/015_Figure_9.jpg]]
*Figure 9: MS-COCO. The percentage of classes where one acquisition function outperforms another. Numbers 1-5 represent the active learning cycle. Example: taking the entry ”unified” in the y-axis, and ”entropy” in the x-axis in (1), we get the value 0.65 which means that ”unified” acquisition function outperforms the ”entropy” acquisition function in 65% of classes during the first active learning cycle*

![[assets/figures/papers/paper_list_l33_https_arxiv_org_abs_2106_11921/figures/018_Table_5.jpg]]
*Table 5: MS-COCO. a) Comparison to two semi-supervised learning methods. We initially use 5, 000 randomly sampled images and, in every other cycle, we label 1, 000 extra images. Our method outperforms both of them by a large margin. b) Ablation study on the effect of entropy, inconsistency, unified score, and our method in MS-COCO. We observe that doing active learning with either entropy or consistency outperforms the semi-supervised model, that the unified score performs better than either of the individual scores, and that our method reaches the best overall results*

![[assets/figures/papers/paper_list_l33_https_arxiv_org_abs_2106_11921/figures/019_Table_6.jpg]]
*Table 6: VOC07+12. a) The results of adding top k% most confident pseudo-labels for class, compared to the results of our method. Top 20%, Top 30%, Top 40% represent the methods where we choose to pseudo-label the most confident 20%, 30% and 40% pseudo-labels per class. Ours represent our method where we pseudo-label all the objects for which the network’s confidence is greater than 0.99. b) Accuracy as a function of label/unlabeled sampling strategy. Random refers to random sampling from the entire dataset, Balanced quarter refers to having a quarter of labeled samples; Unified refers to half of the samples being labeled. Our balanced strategy outperforms the other two strategies. Note that in orde...*

![[assets/figures/papers/paper_list_l33_https_arxiv_org_abs_2106_11921/figures/009_Table.jpg]]
*Table: (a)*

## 方法谱系与知识库定位

### 1. 在主动学习谱系中的位置

本工作处于**基于池的主动学习（Pool-based Active Learning）** 与**半监督学习（Semi-Supervised Learning）** 的交叉地带，核心创新在于将“鲁棒性”信号引入获取函数，并通过高置信度伪标签机制抑制主动学习固有的分布漂移问题。

#### 1.1 相对于不确定度方法的改进

传统不确定度主动学习方法——包括**Entropy-based AL**、**Ensemble** 、**MC-dropout** ——依赖网络对单个样本的预测熵或模型不确定性来评估标注价值。这类方法存在两个结构性缺陷：

- **类别偏差（Class Bias）**：高表现类别天然具有高熵，导致标注预算向这些类别集中，低表现类别（如PASCAL VOC中的Bottle、Pottedplant）因预测过于自信（低熵）而长期被忽略。如Figure 1a所示，低表现类别的目标反而被认为“确定性高”，从而被获取函数排除。
- **分布漂移（Distribution Drift）**：单独选择高不确定度样本会导致训练数据分布偏离原始数据分布，损害模型泛化能力。

本工作提出的**不一致性分数（Inconsistency Score）** $I(\Delta)$ 基于原始图像与水平翻转增强图像预测之间的对称KL散度（Eq. 2），是一种**类别无关（Class-agnostic）** 的标注价值信号。其核心洞察在于：网络对同一目标在不同视角下预测的不一致性，比预测熵本身更能反映该样本对当前模型的价值。实验证据表明，在VOC07+12的低表现类别上，不一致性AL相对熵方法可获得高达24%的相对提升（Figure 5, Bottle类）。

#### 1.2 相对于多样性与混合方法的定位

- **Core-Set** 通过几何多样性选择代表性样本，但忽略了样本的标注难度，可能选择大量简单样本浪费标注预算。
- **PM** 结合偶然不确定度（Aleatoric）与认知不确定度（Epistemic），是当前最先进的主动学习方法之一。本工作在VOC07+12第5周期以75.60 mAP超越PM的74.29 mAP（Table 2），在MS-COCO上以32.80 mAP超越PM的31.86 mAP（Table 4），表明“鲁棒性”信号比更精细的不确定度分解更具实用价值。

本方法的统一获取函数 $A(\Delta) = H(\Delta) \times I(\Delta)$（Eq. 5）本质上是一种**乘积融合策略**：熵捕捉预测不确定性，不一致性捕捉模型鲁棒性，两者互补而非替代。消融实验（Table 3b）证实，单独使用不一致性得分在第5周期仅略优于熵（+0.08 mAP），而乘积融合后再配合伪标签可获得额外+0.62 mAP的提升。

### 2. 在半监督学习谱系中的位置

#### 2.1 相对于一致性正则化方法

**SSL-cons.** 通过对未标注数据施加分类一致性损失来利用无标签数据。本工作扩展了这一范式：不仅施加分类一致性损失 $\mathcal{L}_{con_C}$，还引入了**定位一致性损失** $\mathcal{L}_{con_L}$（Eq. 9），对边界框偏移施加L2约束。这一双重一致性设计使得网络在增强变换下同时保持分类和定位的鲁棒性。

关键发现：SSL训练是使不一致性获取函数生效的**必要条件**。Table 1a显示，无SSL训练时，不一致性AL的表现甚至不及随机采样。这是因为未经过一致性训练的网络，其预测不一致性更多来自随机噪声而非真正的模型不确定区域，无法提供有效的标注价值信号。

#### 2.2 相对于伪标签方法

**SSL-PL** 通过高置信度预测生成伪标签扩展训练集。但如Figure 1b所示，伪标签方法在低表现类别上可能生成**高置信度的错误伪标签**，反而损害训练。

本工作的伪标签策略有三个关键设计差异：

1. **极高阈值** $\tau = 0.99$：Table 1b显示，该阈值下伪标签错误率仅3.7%，降低阈值会显著增加错误伪标签比例。
2. **类别无关选择**：不使用按类top-k%策略（Table 6a显示该方法效果不佳），而是对所有类别统一应用阈值。
3. **修改的MultiBox损失**：标准MultiBox损失会将无伪标签区域的预测视为假阳性进行惩罚。本工作修改损失函数，使其仅在存在伪标签的区域计算监督信号，避免对未标注目标的不当惩罚。

伪标签与主动学习的协同效应是方法成功的关键：Figure 3b/4b显示单独使用伪标签效果微弱，但与统一获取函数配合后效果显著。消融实验（Table 3b）证实，伪标签在统一得分基础上额外贡献+0.62 mAP，且增益在早期主动学习周期最大（Figure 8b），当伪标签数量约占总标签一半时效果最佳。

### 3. 适用边界与局限

#### 3.1 已验证的适用条件

- **检测架构**：仅验证于SSD300 + VGG骨干，未在Faster R-CNN、YOLO等架构上测试。
- **数据增强**：不一致性计算仅基于水平翻转，未探索色彩抖动、随机裁剪等其他增强策略。
- **数据集规模**：在PASCAL VOC（~16K图像）和MS-COCO（~83K图像）上验证，未测试更大规模数据集。
- **标注预算策略**：平衡策略（一半标注、一半未标注）在Table 6b中被验证为最优，但该比例的最优性可能依赖于具体数据集和任务。

#### 3.2 已知局限与开放问题

1. **伪标签增益的衰减**：Figure 8b显示，伪标签增益在后期主动学习周期逐渐减弱，即使网络变得更好、伪标签数量更多。这一现象的原因尚不明确，可能与后期标注集已足够丰富、伪标签带来的边际信息增益递减有关。

2. **架构泛化性**：方法是否适用于两阶段检测器（如Faster R-CNN）或anchor-free检测器（如YOLO、FCOS）需要进一步验证。不同架构的预测不确定性特性可能影响不一致性信号的质量。

3. **多任务与开放世界场景**：该框架是否可扩展到多任务网络（如同时进行检测和分割）或开放世界目标检测（需要发现未知类别）仍是开放问题。

4. **增强策略的丰富性**：水平翻转是相对弱的增强，引入更强的增强（如色彩抖动、随机裁剪、CutMix）可能进一步提升不一致性信号对标注价值的判别能力，但也可能引入过多噪声。

5. **计算开销**：方法需要在前向传播中同时处理原始图像和增强图像，并计算KL散度矩阵，在超大规模数据集上的计算效率需要评估。

### 4. 知识库定位总结

本工作在目标检测的标注效率优化领域占据以下定位：

- **上游继承**：继承不确定度主动学习（Entropy、PM）的池式选择框架，继承半监督学习（SSL-cons.、SSL-PL）的一致性训练与伪标签机制。
- **核心贡献**：提出“鲁棒性即标注价值”的新视角，将预测不一致性作为类别无关的获取信号，并通过乘积融合与高阈值伪标签实现主动学习与半监督学习的有效协同。
- **下游影响**：为类别不平衡场景下的主动学习提供了新范式，其“不一致性+伪标签”的组合策略可被后续工作在不同任务和架构上复用。

## 原文 PDF

![[paperPDFs/CVPR_2022/Not_All_Labels_Are_Equal_Rationalizing_The_Labeling_Costs_for_Training_Object_Detection.pdf]]
