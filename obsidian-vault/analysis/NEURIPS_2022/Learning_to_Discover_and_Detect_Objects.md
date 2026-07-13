---
title: "Learning to Discover and Detect Objects"
type: paper
paper_level: A
venue: NeurIPS
year: 2022
pdf_ref: paperPDFs/NEURIPS_2022/Learning_to_Discover_and_Detect_Objects.pdf
project_link: null
code_link: https://github.com/vlfom/RNCDL
aliases:
- RBNR
- LDDO
tags:
- NEURIPS_2022
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/vision_models_multimodal
core_operator: "通过引入基于长尾分布先验的在线约束聚类（Sinkhorn-Knopp）生成伪标签，并在检测器中添加辅助分类头，配合记忆模块和多视图交换训练，迫使网络学习区分各种未知类别，同时保持已知类别分类能力。"
primary_logic: "在自然场景中，将类不可知的检测器与长尾分布约束的自监督聚类相结合，可在不增加额外标注的情况下，端到端地发现和定位新物体类别，显著减轻离线聚类方法的偏差。"
claims:
- "RNCDL在COCO_half+LVIS上达到6.92 mAP_all，超过最强基线UNO达4.74 mAP。"
- "移除记忆模块导致mAP下降4.09，表明其对自监督伪标签生成至关重要。"
- "使用对数正态长尾先验代替均匀先验显著提升了新类别的发现性能。"
- "端到端训练比基于离线的k-means聚类方案在新类别mAP上提升4.86。"
---

# Learning to Discover and Detect Objects

> [!tip] 核心洞察
> 在自然场景中，将类不可知的检测器与长尾分布约束的自监督聚类相结合，可在不增加额外标注的情况下，端到端地发现和定位新物体类别，显著减轻离线聚类方法的偏差。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 学习发现与检测物体 |
| 英文题名 | Learning to Discover and Detect Objects |
| 会议/期刊 | NeurIPS 2022 |
| Links | [paper](https://arxiv.org/abs/2210.10774) · [GitHub](https://github.com/vlfom/RNCDL) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/vision_models_multimodal |
| Method | Region-based NCDL (RNCDL) |
| Dataset | COCO_half + LVIS, LVIS → VisualGenome |

> [!tip] 效果简介
> - COCO_half + LVIS 上，mAP (all) 为 6.92，对比 2.18 (UNO)，变化 +4.74。
> - COCO_half + LVIS 上，mAP (known) 为 25.00，对比 0.93 (k-means)*，变化 +24.07。
> - COCO_half + LVIS 上，mAP (novel) 为 5.42，对比 1.36 (UNO)，变化 +4.06。

## 概要

**核心问题**：在真实场景中，目标检测器依赖大规模有标注数据，但标注成本限制了可识别类别的数量。当面对未标注的新颖物体类别时，现有检测器通常将对应区域的特征压缩为“背景”类，缺乏对新类别的判别表示，且模型严重偏向已知类，导致传统离线聚类方法难以有效发现新类别。

**方法定位**：本文提出**基于区域的端到端新类别发现与检测框架 RNCDL**（Region-based Novel Class Discovery and Localization），将类不可知的两阶段检测器与长尾分布约束的在线自监督聚类相结合。其核心思路是：在已有标注的已知类数据上训练检测器，冻结骨干网络和区域提议网络后，附加一个新颖类分类头，通过 Sinkhorn-Knopp 在线约束聚类生成伪标签，配合记忆模块和多视图交换训练，迫使网络学习区分各种未知类别，同时保持对已知类的分类能力。

**方法谱系与知识库定位**：该方法继承了两阶段检测器（Faster/Mask R-CNN）的架构范式，在自监督学习层面与基于对比学习的聚类方法（如 Weng et al. 的长尾分割方法、**SwAV** 的等分约束聚类）以及新类别发现分类方法（如 **ORCA**、**UNO**）共享部分思想。区别于上述工作，RNCDL 首次将在线约束聚类引入目标检测的新类别发现任务，用长尾对数正态先验替代均匀先验以建模真实类别分布，并通过双头分类器与记忆模块实现端到端的联合训练，避免了离线 k-means 等方法的偏差。

**主要结果**：在 COCO_half + LVIS 设定下，RNCDL 达到 **6.92 mAP_all**，比最强基线 UNO（2.18 mAP）提升 **4.74 mAP**；在新颖类别上达到 5.42 mAP，比 UNO 提升 4.06 mAP；在已知类别上达到 25.00 mAP。消融实验表明，移除记忆模块导致 mAP 下降 4.09，使用对数正态长尾先验显著优于均匀先验，端到端在线聚类比离线 k-means 方案在新类别 mAP 上提升 4.86。在 LVIS → VisualGenome 跨数据集泛化实验中，RNCDL 成功发现了 2.56 mAP 的新颖类别，验证了方法的通用性。



### 任务定义：新类别发现与定位

传统的物体检测器依赖大规模人工标注，能够识别的类别受限于训练集中出现的语义概念。然而，现实世界中存在大量未被标注的物体类别，模型需要具备在无监督条件下发现并定位这些新颖类别的能力。该任务被定义为**新类别发现与定位**（Novel Class Discovery and Localization, NCDL）：给定一组包含已知类别标注的图像，以及另一组可能包含新颖类别实例但无任何标注的图像，要求模型同时完成对已知类别的识别与定位，以及对新颖类别的聚类式发现与定位（Figure 1）。

### 核心瓶颈：背景压缩与已知类偏向

现有方法面临一个根本性瓶颈：在无标注的真实图像中，检测器倾向于将未知物体区域的特征压缩为单一的“背景”类表示。这种压缩导致模型缺乏对新类别的判别性特征，无法有效区分不同的新颖语义概念。更严重的是，模型在训练过程中严重偏向已知类别——任何无法匹配已知类的区域都被迫归入背景，使得后续聚类算法（如离线k-means）难以从这些退化的特征中恢复出有意义的新类别簇。这一“背景黑洞”效应构成了NCDL任务的核心挑战。

### 现有方法缺口：离线聚类与端到端学习的割裂

针对上述挑战，已有工作主要沿两条路径展开：

- **基于对比学习与离线聚类的方法**：如Weng et al. 在长尾分割任务中采用对比学习结合k-means的策略，但离线聚类与特征学习相互割裂，聚类结果无法反向优化特征表示，导致伪标签质量受限于初始特征的质量。
- **基于等分约束的在线聚类方法**：如UNO 引入SwAV风格的等分约束进行在线伪标签生成，但其假设类别服从均匀分布，与真实场景中长尾分布的实际情况严重不符，限制了新颖类别的发现能力。
- **扩展至检测任务的方法**：如ORCA 将新类别发现从分类任务扩展至同时包含已知和未知类别的设定，但本质上仍依赖离线聚类流程。

这些方法的共同缺陷在于：**离线聚类产生的伪标签与检测器的特征学习之间缺乏端到端的协同优化**，且普遍忽略真实世界中类别分布的长尾特性。实验证据表明，基于离线k-means聚类的方案在新类别mAP上相比端到端方法下降4.86（Section 4.2），充分暴露了这一割裂带来的性能损失。

### 本文动机：端到端联合发现与检测

针对上述缺口，本文提出**基于区域的NCDL框架（Region-based NCDL, RNCDL）**，核心动机在于：

1. **消除特征学习与聚类的割裂**：通过在线约束聚类（Sinkhorn-Knopp算法）直接在检测流程中生成伪标签，使特征表示与聚类目标在统一的端到端框架下协同优化。
2. **引入真实分布先验**：采用对数正态长尾先验替代均匀先验，更准确地建模自然场景中的类别分布，显著提升新颖类别的发现性能。
3. **保持已知类别能力**：在发现新颖类别的过程中，通过双头分类架构（已知类分类头与新颖类分类头）和缩小的有监督损失，避免灾难性遗忘，维持对已知类别的识别能力。
4. **提升伪标签质量**：引入记忆模块存储历史批次的RoI特征，结合多视图交换训练策略，增强自监督信号的一致性与稳定性。



## 核心方法与创新机理

RNCDL的核心创新在于将**类不可知的区域检测**与**长尾分布约束的在线聚类**深度融合，构建了一个端到端的新类别发现与定位框架。相对于传统多阶段管线（如自监督特征提取 + 离线k-means聚类）以及已有的NCD分类方法（ORCA、UNO），RNCDL在四个关键维度上进行了系统性改造：

### 1. 双头分类架构：解耦已知与未知

传统检测器仅使用单一分类头，将未知物体区域的特征压缩为“背景”类，导致网络严重偏向已知类别，无法为新颖类别学习判别性表示。RNCDL引入**双头分类器**：

- **已知类分类头** $h^k$：输出 $K$ 类logits（无背景类），在发现阶段持续接收有监督损失以保持已知类分类能力。
- **新颖类分类头** $h^n$：由MLP投影层和**余弦分类器**组成，在冻结的框特征上训练，专门学习新颖类别的判别表示。

这一设计的关键在于：新颖头使用余弦相似度（$\mathbf{l}^n = \frac{\mathbf{W}^n}{||\mathbf{W}^n||} \cdot \frac{\hat{\mathbf{f}}^n}{||\hat{\mathbf{f}}^n||}$）而非全连接层——实验表明，替换为全连接层会导致训练发散（Section E），说明归一化空间对无监督聚类至关重要。

### 2. 在线约束聚类：替代离线k-means

传统方法（如**k-means** ）在离线阶段对冻结特征进行聚类，无法与检测网络协同优化，且聚类偏差会直接固化。RNCDL采用**Sinkhorn-Knopp在线约束聚类**，在每批次训练中动态生成伪标签：

- 使用**对数正态长尾先验**代替均匀先验，更符合真实场景中类别分布的长尾特性。消融实验证实，这一先验显著提升了新颖类别的发现性能（Section 4.2）。
- 聚类能量函数 $E(\hat{\mathbf{p}}, \mathbf{q}) = \frac{1}{B} \sum_{i=1}^{B} \sum_{y}^{N+K} q(y|I_i) \log \hat{p}(y|I_i)$ 同时优化网络权重和伪标签分配，形成端到端闭环。

直接与离线k-means对比：用k-means替代在线聚类后，新颖类mAP下降4.86（Section 4.2），证明了在线协同优化的决定性作用。

### 3. 记忆模块：提升伪标签质量

在线聚类受限于批次大小，伪标签噪声较大。RNCDL引入**记忆模块**：存储最近批次的RoI特征，将当前批次特征与记忆特征拼接后输入Sinkhorn聚类（$\hat{\mathbf{l}} = [h^k([\hat{\mathbf{f}}, \mathbf{M}]), h^n([\hat{\mathbf{f}}, \mathbf{M}])]$），从而扩大聚类上下文。

移除记忆模块导致mAP下降4.09（Table 3），这是所有消融组件中影响最大的单一模块，表明记忆增强对伪标签质量的关键作用。

### 4. 多视图交换训练：强化特征一致性

RNCDL对每张图像生成两个增强视图，计算各自的伪标签后**交换使用**：用视图1的伪标签监督视图2的预测，反之亦然。交换损失 $\hat{L}_{ss} = (E(\hat{\mathbf{p}}_1, \mathbf{q}_2) + E(\hat{\mathbf{p}}_2, \mathbf{q}_1)) / 2$ 迫使网络学习视图不变的特征表示。

去除多视图交换后性能显著降低（Table 3），验证了该自监督信号对特征学习的贡献。

### 创新协同效应

上述四个模块并非孤立改进，而是形成正向协同：记忆模块提供更稳定的聚类上下文，在线Sinkhorn生成更准确的伪标签，多视图交换增强特征鲁棒性，双头架构确保已知类能力不退化。在COCO_half+LVIS基准上，RNCDL达到6.92 mAP_all，超过最强基线**UNO**（Fini et al.）达4.74 mAP（Table 4），其中新颖类mAP从1.36提升至5.42。



RNCDL 采用两阶段训练范式，将新类别发现与定位统一在一个端到端的检测框架内。其核心思路是：先在带标注的已知类数据上训练一个标准的双阶段检测器，获得类不可知的区域提议能力和可迁移的视觉特征；随后冻结大部分网络参数，仅通过在线约束聚类与辅助分类头，在无标注图像中同时保持已知类识别能力并发现新类别。

**第一阶段：有监督引导**。网络以 Faster/Mask R-CNN 为基础，使用标准 R-CNN 损失 $L_{sup} = L_{RPN} + L_{box} + L_{cls}$ 在已标注的已知类数据上训练。此阶段产出三个关键组件：一个经过预训练的主干网络（ResNet50-FPN，采用 MoCo 自监督初始化）、一个类不可知的区域提议网络（RPN），以及一个包含背景类的 $K+1$ 路分类头。该阶段的目标并非直接发现新类，而是为后续的发现阶段提供高质量的候选框和具备判别力的冻结特征。

**第二阶段：联合发现**。在此阶段，网络的所有卷积层与框回归头均被冻结，仅训练两个分类头：原有的已知类分类头 $h^k$（此时移除背景类，仅保留 $K$ 个已知类别）和新引入的新颖类分类头 $h^n$。$h^n$ 由一个 MLP 投影层与一个余弦分类器组成，其 logits 计算为 $\mathbf{l}^n = \frac{\mathbf{W}^n}{||\mathbf{W}^n||} \cdot \frac{\hat{\mathbf{f}}^n}{||\hat{\mathbf{f}}^n||}$，以避免全连接层在自监督聚类下发散。两个头共享冻结的 RoI 特征，通过联合损失 $L_{disc} = L_{ss} + \alpha \cdot L_{cls}$ 进行优化——其中 $L_{ss}$ 为在线聚类产生的伪标签交叉熵，$L_{cls}$ 为缩小的有监督分类损失（系数 $\alpha=0.5$ 时达到最佳平衡，Table 1）。

**在线聚类与伪标签生成回路**。发现阶段的核心是一个基于 Sinkhorn-Knopp 算法的在线约束聚类模块。每个批次中，RPN 为每张无标注图像生成固定数量（如 50 个，无 NMS）的类不可知提议，RoIAlign 提取其特征后，与一个记忆模块中存储的历史特征拼接，计算双头 logits $\hat{\mathbf{l}} = [h^k([\hat{\mathbf{f}}, \mathbf{M}]), h^n([\hat{\mathbf{f}}, \mathbf{M}])]$。Sinkhorn 算法在长尾对数正态先验的约束下求解最优传输问题，为每个提议分配软伪标签 $\mathbf{q}$，并最小化交叉熵 $E(\hat{\mathbf{p}}, \mathbf{q})$。记忆模块通过队列更新，为聚类提供更稳定的全局统计量——移除该模块会导致 mAP 骤降 4.09（Table 3）。

**多视图交换与一致性训练**。为进一步提升特征不变性，网络对同一图像施加两组随机增强（SimCLR 风格），得到两个视图的预测 $\hat{\mathbf{p}}_1$、$\hat{\mathbf{p}}_2$ 和伪标签 $\mathbf{q}_1$、$\mathbf{q}_2$。自监督损失被替换为交换视图后的平均交叉熵 $\hat{L}_{ss} = (E(\hat{\mathbf{p}}_1, \mathbf{q}_2) + E(\hat{\mathbf{p}}_2, \mathbf{q}_1)) / 2$，迫使网络在不同增强下保持一致的聚类分配。去掉此交换机制会导致性能显著退化（Table 3）。

**推理与评估映射**。推理时，网络执行标准 R-CNN 前向传播，将 $h^k$ 与 $h^n$ 的 logits 拼接后经 softmax 得到 $K+N$ 类的概率 $\hat{\mathbf{p}} = \mathrm{softmax}([h^k(\hat{\mathbf{f}}), h^n(\hat{\mathbf{f}})])$。由于聚类产生的簇 ID 与真实语义类别之间无直接对应关系，评估时采用匈牙利算法将预测簇映射到真实类别，未匹配的预测实例被忽略。这一映射机制是当前框架的一个结构性局限——它无法直接输出语义标签，且对聚类碎片化（如已知类被分裂为多个子簇）敏感。

**整体数据流**可概括为：无标注图像 → 冻结的 RPN 生成类不可知提议 → 冻结的 RoIAlign 提取特征 → 记忆模块增强 → 双头分类器输出 logits → Sinkhorn 在线聚类生成伪标签 → 交换多视图伪标签计算一致性损失 → 反向传播仅更新两个分类头。Figure 2 完整展示了从有监督引导到联合发现再到推理的全流程架构。

### 补充图表

![[assets/figures/papers/paper_list_l27_https_arxiv_org_abs_2210_10774/figures/014_Figure.jpg]]
*Figure: a) COCO → LVIS Figure H1: Visualization of predictions for validation images of the fully-supervised model and our RNCDL framework in \mathrm { C O C O } _ { h a l f } + LVIS setup. We color the discovered novel classes in red*

![[assets/figures/papers/paper_list_l27_https_arxiv_org_abs_2210_10774/figures/002_Figure_2.jpg]]
*Figure 2: A high-level overview of our network. (top) During the supervised training phase, we train our backbone and RPN networks using labeled data, together with classification head and a class agnostic localization head. During the discovery phase, we freeze all the layers of the network apart from classification head and attach and train a novel classification head using unlabeled data. During the inference (bottom), we perform a standard R-CNN pass, using classification heads of both known and novel categories to predict a class assignment for each proposal. This can be either one of K classes, that were presented a labeled samples during the model training, or any novel object class that appea...*



RNCDL 将新类别发现与定位任务分解为两个阶段：**有监督引导阶段**与**发现阶段**。在引导阶段，网络在已知类标注数据上学习类不可知的区域提议能力和可迁移的视觉特征；在发现阶段，网络冻结大部分参数，仅通过在线约束聚类生成伪标签来训练新颖类分类头。以下聚焦发现阶段的核心模块与关键公式。

### 双头分类架构

RNCDL 在标准 Faster/Mask R-CNN 的 RoI 框特征之上构建了两个并行的分类头：

- **已知类分类头** $h^k$：输出 $K$ 类 logits（无背景类），参数在发现阶段冻结。
- **新颖类分类头** $h^n$：由 MLP 投影层 $g^n$（带 ReLU 激活）和余弦分类层组成，在发现阶段训练。

新颖类 logits 的计算公式为：

$$\mathbf{l}^n = \frac{\mathbf{W}^n}{\|\mathbf{W}^n\|} \cdot \frac{\hat{\mathbf{f}}^n}{\|\hat{\mathbf{f}}^n\|}$$

其中 $\hat{\mathbf{f}}^n = g^n(\hat{\mathbf{f}})$ 为冻结的框特征 $\hat{\mathbf{f}}$ 经 MLP 投影后的特征，$\mathbf{W}^n$ 为可学习的分类权重矩阵。余弦相似度的归一化操作使 logits 对特征尺度不敏感，实验表明将其替换为全连接层会导致训练发散（Table E1）。

### 发现阶段联合损失

发现阶段的总损失为自监督聚类损失与缩放的有监督分类损失的加权和：

$$L_{disc} = L_{ss} + \alpha \cdot L_{cls}$$

- $L_{ss}$：基于在线聚类伪标签的交叉熵损失（见下文）。
- $L_{cls}$：标准有监督分类损失，仅在已知类标注样本上计算。
- $\alpha$：缩放系数，控制已知类分类信号的强度。消融实验（Table 1）表明 $\alpha=0.5$ 在 mAP_all 上达到最优（6.92），$\alpha=0$ 时已知类性能显著退化。

### 记忆增强的在线约束聚类

发现阶段的核心挑战是如何为无标注的 RoI 特征生成可靠的伪标签。RNCDL 采用 **Sinkhorn-Knopp 在线约束聚类**，并引入两个关键设计：

**记忆模块**：维护一个队列 $\mathbf{M}$，存储最近若干批次的 RoI 特征。在计算聚类 logits 时，将当前批次特征与记忆特征拼接，以扩大有效样本量、提升伪标签质量：

$$\hat{\mathbf{l}} = [\hat{\mathbf{l}}^k, \hat{\mathbf{l}}^n] = [h^k([\hat{\mathbf{f}}, \mathbf{M}]), h^n([\hat{\mathbf{f}}, \mathbf{M}])]$$

消融实验（Table 3）显示，移除记忆模块导致 mAP 下降 4.09，证明其对伪标签质量至关重要。

**长尾先验约束**：Sinkhorn 算法在求解最优传输时引入对数正态长尾先验，替代传统聚类中隐含的均匀类别分布假设。该先验更贴合自然场景中类别呈现长尾分布的现实，显著提升了新类别的发现性能（Section 4.2）。

聚类过程通过交替优化以下交叉熵能量函数实现：

$$E(\hat{\mathbf{p}}, \mathbf{q}) = \frac{1}{B} \sum_{i=1}^{B} \sum_{y}^{N+K} q(y|I_i) \log \hat{p}(y|I_i)$$

其中 $\hat{\mathbf{p}} = \mathrm{softmax}(\hat{\mathbf{l}})$ 为网络预测的类别概率，$\mathbf{q}$ 为 Sinkhorn 算法生成的软伪标签，$B$ 为批次大小，$N+K$ 为已知类与新颖类的总类别数。

### 多视图交换自监督

为增强特征对数据增强的不变性，RNCDL 对每张输入图像生成两个随机增强视图，分别计算其伪标签 $\mathbf{q}_1$、$\mathbf{q}_2$ 和预测 $\hat{\mathbf{p}}_1$、$\hat{\mathbf{p}}_2$，然后交换伪标签计算对称损失：

$$\hat{L}_{ss} = \frac{E(\hat{\mathbf{p}}_1, \mathbf{q}_2) + E(\hat{\mathbf{p}}_2, \mathbf{q}_1)}{2}$$

该设计迫使网络在不同视图下对同一 RoI 产生一致的类别分配。消融实验（Table 3）证实，移除此交换机制会导致性能显著降低。

### 推理阶段类别概率

推理时，将已知头和新颖头的 logits 拼接后经 softmax 归一化，得到全部 $K+N$ 类的概率分布：

$$\hat{\mathbf{p}} = \mathrm{softmax}([h^k(\hat{\mathbf{f}}), h^n(\hat{\mathbf{f}})]) \in \mathbb{R}^{K+N}$$

随后通过匈牙利算法将预测的簇 ID 映射到真实语义类别，计算 mAP 进行评估。



## 实验与关键发现

### 核心性能瓶颈与因果机制

RNCDL 要解决的核心瓶颈是：在无标注的真实图像中，标准检测器将未知物体区域的特征压缩为“背景”类，导致这些区域缺乏可判别的表示，且模型严重偏向已知类别。这使得传统离线聚类（如 k-means）难以有效发现新类别。RNCDL 的关键因果调节变量是在线约束聚类——通过引入基于长尾分布先验的 Sinkhorn-Knopp 算法生成伪标签，并配合记忆模块与多视图交换训练，迫使网络学习区分各种未知类别，同时保持已知类别分类能力。

### 主要结果：COCO_half + LVIS

**Table 4** 展示了 RNCDL 与现有方法的对比。在 COCO_half + LVIS 设定下，RNCDL 达到 **6.92 mAP_all**，比最强基线 **UNO**（2.18 mAP）高出 **4.74 点**。其中，已知类别 mAP 为 25.00，新颖类别 mAP 为 5.42——后者比 UNO（1.36）提升 4.06 点。相比之下，基于离线 k-means 的基线仅获得 0.93 mAP_known，说明端到端在线聚类对伪标签质量的提升至关重要。

### 关键消融实验

**Table 3** 的组件移除实验揭示了各模块的因果贡献：

- **移除记忆模块**：mAP 下降 **4.09**，这是所有单组件移除中降幅最大的，证实记忆模块对提升伪标签质量起决定性作用。
- **移除多视图交换**：性能显著降低，表明交换伪标签的一致性训练对学习鲁棒特征不可或缺。
- **随机初始化骨干网络**（替代 MoCo 预训练）：mAP 下降 2.15，说明自监督预训练为发现阶段提供了关键的特征基础。
- **将余弦分类器替换为全连接层**：训练发散，无法收敛（Section E），验证了归一化余弦分类器对稳定训练的必要性。

### 超参数敏感性

**Table 1** 考察有监督损失系数 α 的影响。α=0.5 时 mAP_all 达到最优 6.92；α=0 时已知类别性能严重受损，表明完全舍弃有监督信号会导致灾难性遗忘。

**Table 2** 考察预设新颖类别数 N 的敏感性。N=3000 时性能最佳；降至 1000 或升至 5000 分别导致 mAP 下降 1.50 和 0.68。这说明对类别数的事先估计偏差会显著影响聚类质量——N 过小会导致欠聚类（合并不同语义类），N 过大会导致过聚类（分裂同一语义类）。

**Table E1** 进一步显示：发现阶段使用无 NMS 的 50 个提议可获得最佳性能；更强的 NMS 会损害结果，因为可能过滤掉新颖类别的高质量提议。

### 跨数据集泛化：LVIS → VisualGenome

**Table 5** 展示了跨数据集迁移结果。RNCDL 在 LVIS → VG 设定下达到 4.46 mAP_all，其中新颖类别 mAP 为 2.56。作为参考，全监督已知类模型（无新颖类监督）在 VG 上达到 12.55 mAP。需注意，VG 标注不完整且包含大量抽象语义类，定量 mAP 可能不能完全反映真实性能，该结果需谨慎解读。

### 失败模式与局限性

1. **聚类碎片化**：当语义相近的类别（包括已知类）在特征空间中重叠时，Sinkhorn-Knopp 聚类可能将其分裂为多个子簇，导致匈牙利匹配后 mAP 下降。
2. **类别数依赖**：方法需要事先指定新颖类别数，错误的估计会直接损害性能（Table 2）。
3. **骨干网络冻结**：发现阶段冻结骨干网络虽稳定了训练，但也限制了特征对新颖类别的进一步自适应。
4. **语义映射不稳定**：依赖匈牙利算法将预测簇 ID 映射到真实语义类，无法直接提供语义标签，且匹配结果可能不稳定。

![[assets/figures/papers/paper_list_l27_https_arxiv_org_abs_2210_10774/figures/004_Table_2.jpg]]
*Table 2: Sensitivity to the number of classes. We vary the number of novel classes set during the discovery phase*

### 定性分析

**Figure 3** 展示了全监督模型与 RNCDL 在验证图像上的预测可视化对比（新颖类以红色标注）。RNCDL 成功发现了全监督模型完全忽略的多种新颖物体类别。**Figure 4** 进一步展示了在 LVIS 和 VisualGenome 两个数据集中共同发现的新颖类别，验证了方法跨数据集的语义发现一致性。**Figure H3** 对最大和最置信的发现簇进行了可视化分析，有助于理解聚类行为。

### 补充图表

![[assets/figures/papers/paper_list_l27_https_arxiv_org_abs_2210_10774/figures/007_Figure.jpg]]
*Figure: a) COCO → LVIS b) LVIS →VisualGenome*

![[assets/figures/papers/paper_list_l27_https_arxiv_org_abs_2210_10774/figures/013_Table.jpg]]
*Table: G1: Detailed results for the RCNDL model. (a) Detection scores for the RNCDL model in \mathrm { C O C O } _ { h a l f } + LVIS setup (b) Segmentation scores for the RNCDL model in \mathrm { C O C O } _ { h a l f } + LVIS setup (c) Detection scores for the RNCDL model in LVIS + VG setup*

![[assets/figures/papers/paper_list_l27_https_arxiv_org_abs_2210_10774/figures/016_Figure.jpg]]
*Figure: size: 48536,confidence: 0.27 size:l39228,confidence: 0.08*

![[assets/figures/papers/paper_list_l27_https_arxiv_org_abs_2210_10774/figures/017_Figure.jpg]]
*Figure: d) LVIS → VG unmatched clusters, ordered by size Figure H3: The largest and the most confident clusters discovered*

![[assets/figures/papers/paper_list_l27_https_arxiv_org_abs_2210_10774/figures/003_Table_1.jpg]]
*Table 1: Impact of supervised loss strength. We check the results of our method as a function of the strength of the supervised loss*

![[assets/figures/papers/paper_list_l27_https_arxiv_org_abs_2210_10774/figures/005_Table_3.jpg]]
*Table 3: Additional ablations. We experiment with removing individual components from the network and their impact on the overall performance*

![[assets/figures/papers/paper_list_l27_https_arxiv_org_abs_2210_10774/figures/006_Table_4.jpg]]
*Table 4: Comparison with state-of-the-art models. * as per open source code. † adapted to support known classes in the target dataset. ‡ randomly initialized novel head*

![[assets/figures/papers/paper_list_l27_https_arxiv_org_abs_2210_10774/figures/010_Table_5.jpg]]
*Table 5: LVIS → VisualGenome comparisons with a fully-supervised method*

![[assets/figures/papers/paper_list_l27_https_arxiv_org_abs_2210_10774/figures/011_Table.jpg]]
*Table: C1: Performance of fully-supervised models on \mathbf { C O C O } _ { h a l f } and LVIS datasets. In bold, we highlight the configuration used for the supervised training phase and the fully-supervised baseline*



## 定位与知识库关联

### 任务定位：新类别发现与定位（NCDL）

RNCDL 解决的是**新类别发现与定位**（Novel Class Discovery and Localization, NCDL）任务：给定带有已知类别标注的图像和可能包含新类别实例的无标注图像，网络需同时完成对已知类的识别与定位，以及对新类别的无监督聚类式发现。该任务将传统的新类别发现（NCD）从图像级分类拓展到目标检测领域，核心难点在于检测器天然将未知物体区域压缩为“背景”类，缺乏对新类别的判别表示。

### 与现有工作的关系

**1. 相对于图像级新类别发现方法的继承与拓展**

RNCDL 在自监督聚类范式上继承了图像级 NCD 方法的核心思想，但进行了关键的检测适配：

- **ORCA**（Cao et al., 2022）提出了同时利用已知和未知类别的对比学习框架，但仅适用于图像级分类。RNCDL 将其“已知类引导未知类聚类”的思想迁移到区域级检测场景，通过双分类头设计（已知头 $h^k$ 和新颖头 $h^n$）实现区域特征的联合判别。
- **UNO**（Fini et al., 2021）采用 SwAV 风格的等分约束聚类生成伪标签，但依赖均匀先验假设。RNCDL 将这一在线聚类范式引入检测管道，并用**对数正态长尾先验**替代均匀先验，更贴合真实场景中类别分布的长尾特性（消融实验证实该替换显著提升新类别发现性能，Section 4.2）。
- **Weng et al.** 的长尾分割方法采用了对比学习 + 离线 k-means 的两阶段方案。RNCDL 的实验表明，将离线 k-means 替换为端到端的 Sinkhorn-Knopp 在线聚类后，新类别 mAP 提升 4.86（Section 4.2），证实了离线聚类在检测场景中的表示偏差问题。

**2. 相对于目标检测基线的架构创新**

RNCDL 以标准的两阶段检测器（Faster/Mask R-CNN）为基础，进行了以下关键改造：

| 组件 | 标准检测器 | RNCDL | 改造动机 |
|------|-----------|-------|---------|
| 分类头 | 单头 $K+1$ 类（含背景） | 双头：已知头 $h^k$（$K$ 类，无背景）+ 新颖头 $h^n$（$N$ 类，余弦相似度） | 解耦已知类判别与新类别发现，避免背景类压缩未知物体特征 |
| 聚类机制 | 无 | 在线 Sinkhorn-Knopp 约束聚类 + 记忆模块 | 端到端生成高质量伪标签，消除离线聚类的表示偏差 |
| 训练增强 | 无额外增强 | 多视图（SimCLR 风格）交换伪标签一致性训练 | 强制特征对数据增强保持不变性，提升聚类稳定性 |
| 先验分布 | 均匀假设 | 对数正态长尾先验 | 建模真实场景的类别长尾分布 |

记忆模块的设计是 RNCDL 的核心工程贡献之一：通过队列存储最近批次的 RoI 特征，在 Sinkhorn 聚类时拼接当前特征与历史特征，有效缓解了小批次导致的伪标签噪声。消融实验表明，移除记忆模块导致 mAP 下降 4.09（Table 3），证实其对自监督伪标签质量的关键作用。

**3. 与通用目标检测知识库的关系**

RNCDL 的知识体系建立在以下基础之上：

- **两阶段检测范式**：继承 Faster R-CNN 的 RPN + RoIAlign 架构，RPN 提供类不可知的区域提议，在发现阶段冻结所有参数以保证训练稳定性。
- **自监督表示学习**：采用 MoCo 自监督预训练的 ResNet50-FPN 作为骨干网络，相比随机初始化提升 2.15 mAP（Table 3）。
- **最优传输理论**：Sinkhorn-Knopp 算法为在线聚类提供数学基础，将伪标签生成形式化为熵正则化的最优传输问题。
- **多视图一致性学习**：借鉴 SimCLR 和 SwAV 的多视图增强策略，通过交换伪标签实现跨视图一致性约束。

### 适用边界与关键局限

**适用场景：**
- 已知类别与未知类别共享相似的底层视觉特征（如均为自然场景中的常见物体）
- 可接受预先指定新类别数量（实验表明设为 3000 时最佳，Table 2）
- 无标注数据量充足，可支撑自监督聚类训练

**核心局限（基于论文自身分析）：**

1. **语义映射依赖事后匹配**：推理时需使用匈牙利算法将预测簇 ID 映射到真实语义类别，无法直接输出语义标签。这一映射过程不稳定且缺乏可解释性，在类别语义重叠时易出现碎片化（如将同一已知类分裂为多个子簇）。

2. **新类别数量需先验指定**：发现阶段要求预设 $N$ 值，设为 1000 或 5000 时性能分别下降 1.50 和 0.68 mAP（Table 2），表明方法对超参数敏感且无法自动估计真实类别数。

3. **骨干网络冻结限制特征自适应**：为稳定训练，发现阶段冻结 Backbone、RPN 和 Box Head 的所有参数，仅训练分类头。这虽避免了灾难性遗忘，但也阻止了特征表示向新类别的进一步自适应。

4. **跨数据集泛化的评估困境**：在 LVIS → VisualGenome 设置中，由于 VG 标注不完整且包含大量抽象/语义重叠类别，定量 mAP 可能无法完全反映真实发现能力（Table 5 中 RNCDL 的 mAP_all 为 4.46，而全监督已知类基线为 12.55，但后者无新类别发现能力）。

5. **计算与内存限制**：记忆模块的队列大小受限于 GPU 内存，论文未对超过 100 个批次的记忆规模进行实验，可能仍有性能提升空间。

6. **余弦分类器的必要性**：将新颖头的余弦分类器替换为全连接层会导致训练发散（Section E），表明归一化约束对于在线聚类稳定性至关重要，但这也可能限制了分类边界的表达能力。

### 开放问题

1. **骨干网络的安全更新**：如何在自监督训练阶段安全地更新骨干网络，以同时提升检测、定位和分割性能，而不引发灾难性遗忘或训练崩溃？

2. **新类别数量的自动估计**：能否通过非参数贝叶斯方法或聚类稳定性分析，在训练过程中自动推断新类别数量，消除对先验设置的依赖？

3. **语义映射的端到端学习**：如何建立更自然的语义映射机制（如通过跨模态对齐或弱监督语义锚点），避免事后匈牙利匹配的不稳定性和不可解释性？

4. **标注不完整数据集的评估协议**：在 VG 这类标注不全且含大量抽象类的数据集上，如何设计更合理的评估协议，使定量指标能真实反映新类别发现能力？

5. **人机协同的语义精化**：能否通过主动学习或人在回环的交互机制，在发现阶段引入少量人工反馈，改善新类别簇的语义一致性和可解释性？

6. **语义重叠的聚类解耦**：当前方法无法有效处理语义重叠导致的聚类碎片化问题，如何设计层次化或软分配聚类机制来建模类别间的包含与重叠关系？



## 原文 PDF

![[paperPDFs/NEURIPS_2022/Learning_to_Discover_and_Detect_Objects.pdf]]
