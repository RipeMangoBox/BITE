---
title: Learning Latent Concepts for Detecting Out-of-Distribution Objects
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/Learning_Latent_Concepts_for_Detecting_Out_of_Distribution_Objects.pdf
project_link: null
code_link: null
aliases:
- UA
- LLCDODO
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/generative_models_diffusion
- topic/representation_self_supervised_transfer
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: 通过无监督概念发现（UCD）从图像中提取稀疏、对象中心的槽表示并建模其关系，再通过神经概念绑定（NCB）将这些全局概念注入检测器的实例特征中，从而赋予检测器“未知”的概念，实现不修改检测器前提下的OOD检测能力提升。
primary_logic: 模仿人类视觉过程，在不改变检测器架构和权重的情况下，利用基于槽注意力的概念发现和关系推理，为检测器提供全局场景理解和“未知”概念，通过slot与实例特征的绑定以及图像引导的OOD评分，显著提高OOD目标检测性能。
claims:
- UNO-Adapter由无监督概念发现和神经概念绑定两个关键步骤组成。
- UCD模块利用信息瓶颈原理进行关系正则化和槽细化，增强槽间的交互并压缩冗余信息。
- 将槽与检测器的实例级特征基于相似度进行绑定，并结合图像引导的OOD评分以确保全局一致性。
- 在BDD-100K上，UNO-Adapter相较于之前的最佳方法WFS在FPR95指标上降低了11.96%（MS-COCO作为OOD）和4.03%（OpenImages作为OOD）。
---

# Learning Latent Concepts for Detecting Out-of-Distribution Objects

> [!tip] 核心洞察
> 模仿人类视觉过程，在不改变检测器架构和权重的情况下，利用基于槽注意力的概念发现和关系推理，为检测器提供全局场景理解和“未知”概念，通过slot与实例特征的绑定以及图像引导的OOD评分，显著提高OOD目标检测性能。

| 字段 | 内容 |
|------|------|
| 中文题名 | 学习潜在概念以检测分布外物体 |
| 英文题名 | Learning Latent Concepts for Detecting Out-of-Distribution Objects |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://openaccess.thecvf.com/content/CVPR2026/html/Peng_Learning_Latent_Concepts_for_Detecting_Out-of-Distribution_Objects_CVPR_2026_paper.html) |
| Topic | #topic/vision_multimodal_applications #topic/generative_models_diffusion #topic/representation_self_supervised_transfer #topic/vision_multimodal_applications/image_and_video_generation |
| Method | UNO-Adapter |
| Dataset | PASCAL-VOC, BDD-100K, ImageNet-200, OWOD Task 2 |

> [!tip] 效果简介
> - PASCAL-VOC (MS-COCO as OOD) 上，AUROC 91.68。
> - BDD-100K (OpenImages as OOD) 上，AUROC 99.04。
> - ImageNet-200 (Near OOD) 上，AUROC / FPR95 87.90 / 50.42。

## 概要

### 问题背景与瓶颈

分布外（OOD）目标检测旨在识别检测器在训练期间未见过的物体类别，是自动驾驶、机器人感知等安全关键应用的核心能力。现有方法的主流范式是在实例级别引入任务特定的正则化目标——例如虚拟异常合成（**VOS**; Du et al., ICLR 2022）、特征塑形（**SIREN**; Du et al., NeurIPS 2022）或敏感性感知特征（**SAFE**; Wilson et al., ICCV 2023）——以增强ID与OOD特征的可区分性。然而，这些方法存在一个根本性瓶颈：它们仅关注孤立的实例级特征，缺乏对场景中对象间全局概念和因果关系的建模，导致ID/OOD决策边界失真，定位不准确。

### 核心洞察

本文从一个关键问题出发：**能否设计一个统一框架，模仿人类视觉过程来检测OOD物体？** 人类在识别未知物体时，并非仅依赖于局部特征，而是结合了场景全局概念（如物体间的关系与上下文）进行推理。受此启发，本文提出 **UNO-Adapter**，在不修改检测器架构和权重的前提下，通过无监督概念发现与神经概念绑定，向检测器注入“未知”的全局概念，从而显著提升OOD检测性能。

### 方法定位

UNO-Adapter 由三个组件构成：**无监督概念发现（Unsupervised Concept Discovery, UCD）**、**神经概念绑定（Neural Concept Binder, NCB）** 以及 **推理时OOD评分（Inference-Time OOD Score）**。其方法谱系可定位于以下坐标系中：

- **与OOD目标检测方法的关系**：不同于 VOS、SIREN、SAFE 和 **WFS**（Wu & Deng, CVPR 2025）等实例级正则化方法，UNO-Adapter 将“未知”概念的注入从实例空间上移至全局概念空间，利用基于槽注意力（Slot Attention）的表示学习，为检测器提供场景级理解。
- **与开放世界目标检测的关系**：与 **OW-DETR**（Gupta et al., CVPR 2022）等需要修改检测器训练范式的方法不同，UNO-Adapter 的训练仅作用于 UCD 模块，检测器权重完全冻结，推理时通过 NCB 实现特征融合，具有即插即用的适配器特性。
- **与经典OOD评分方法的关系**：不同于 **MSP**（Hendrycks & Gimpel, ICLR 2017）和 **Energy**（Liu et al., NeurIPS 2020）等仅依赖分类logits或能量的实例级评分，UNO-Adapter 的OOD评分融合了图像级余弦相似度与分位数策略，确保了全局一致性。

### 主要结果

UNO-Adapter 在多个基准上取得了显著提升：

- **OOD目标检测**：在 BDD-100K 上，当 MS-COCO 作为 OOD 时，FPR95 相较于此前最佳方法 WFS 降低了 **11.96%**；当 OpenImages 作为 OOD 时，FPR95 降低了 **4.03%**。在 PASCAL-VOC 上 AUROC 达到 **91.68**，在 BDD-100K 上 AUROC 达到 **99.04**。
- **开放世界目标检测（OWOD）**：在 Task 2 上，未知召回率（U-Recall）达到 **16.8**，整体 mAP 达到 **45.8**。
- **效率优势**：UNO-Adapter 的微调时间仅 **0.1 小时**，推理时间 **11.54 秒**，远低于 SIREN（36.31秒/2.2小时）和 SAFE（14.37秒/3.6小时），展现出优越的实用部署潜力。

### 局限性

性能对超参数（如槽数量 $S$ 和分位数阈值 $\tau$）存在一定敏感性，实际部署时需根据具体场景进行调优。



### 问题定义：分布外物体检测

在开放世界场景中，目标检测器不仅需要准确识别训练时见过的分布内（In-Distribution, ID）物体，还必须可靠地检测并拒绝分布外（Out-of-Distribution, OOD）物体——即那些不属于任何已知类别的未知物体。这一任务被称为**分布外目标检测**（OOD Object Detection, OOD-OD），其核心挑战在于：检测器天然缺乏对“未知”概念的建模能力，倾向于将OOD物体高置信度地误分类为某个ID类别。

形式上，给定测试输入 $\mathbf{x}^*$ 和预测边界框 $\mathbf{b}^*$，OOD检测的目标是估计该检测结果属于ID（$g=1$）或OOD（$g=0$）的后验概率 $p(g \mid \mathbf{x}^*, \mathbf{b}^*)$。

### 现有方法的瓶颈：实例级视角的局限

当前主流的OOD目标检测方法通常遵循一个共同的范式：在**实例级别**引入任务特定的正则化目标，以增强ID与OOD特征之间的可分性。例如：

- **VOS**（Du et al., ICLR 2022）通过虚拟异常合成生成伪OOD样本，在训练时对实例特征施加正则化；
- **SIREN**（Du et al., NeurIPS 2022）通过特征塑形（feature shaping）调整实例特征分布；
- **SAFE**（Wilson et al., ICCV 2023）引入敏感度感知特征以提升区分能力；
- **WFS**（Wu & Deng, CVPR 2025）通过模拟世界特征来增强OOD检测。

这些方法虽然取得了进展，但存在一个根本性的瓶颈：**它们仅关注孤立的实例级特征，缺乏对场景中物体间全局概念和因果关系的建模**。这导致两个直接后果：（1）定位不准确——缺乏场景上下文使得检测器难以判断一个边界框内的物体究竟是前景OOD还是背景噪声；（2）ID/OOD决策边界失真——仅凭局部特征难以捕捉“未知”这一概念所依赖的全局语义线索。

### 核心动机：模仿人类视觉中的概念推理

人类视觉系统在识别未知物体时，并非孤立地审视每个候选区域，而是综合运用场景中的全局概念和物体间关系进行推理。例如，当我们在驾驶场景中看到一个从未见过的异形车辆时，我们能够通过它与道路、交通标志等其他已知概念的空间和语义关系，推断出它“虽然未知但属于前景物体”这一结论。

这一观察直接引出了论文试图回答的核心问题：**如何设计一个统一的框架，模仿人类视觉过程来检测OOD物体？**

### 本文的切入点：不修改检测器的“未知”概念注入

基于上述动机，本文提出了一种全新的范式：**在不改变检测器架构和权重的前提下，通过外部模块向检测器注入“未知”概念**。具体而言，UNO-Adapter通过以下两个关键步骤实现这一目标：

1. **无监督概念发现（Unsupervised Concept Discovery, UCD）**：从图像的密集像素中提取一组稀疏的、以物体为中心的槽（slot）表示，这些槽捕捉了场景中的潜在概念，并通过关系建模和信息瓶颈原理增强槽之间的交互、压缩冗余信息。
2. **神经概念绑定（Neural Concept Binder, NCB）**：将UCD学习到的全局槽表示与检测器的实例级特征基于相似度进行自适应融合，使检测器获得场景级的“未知”感知能力，而无需修改检测器本身的任何参数。

这一范式的核心优势在于：检测器权重冻结，仅训练轻量的UCD模块；推理时通过绑定机制将全局概念注入实例特征，再结合图像引导的OOD评分确保全局一致性。这种“即插即用”的设计使得UNO-Adapter能够无缝适配任何预训练检测器，同时显著提升OOD检测性能——在BDD-100K上，UNO-Adapter相比之前的最佳方法WFS在FPR95指标上降低了11.96%（MS-COCO作为OOD）和4.03%（OpenImages作为OOD）。



## 核心方法与创新机理

UNO-Adapter 的核心创新在于：**在不修改检测器架构和权重的前提下，通过无监督概念发现与神经概念绑定，向实例级检测器注入全局场景中的“未知”概念**。这与现有方法形成根本性差异——**VOS**（Du et al., ICLR 2022）、**SIREN**（Du et al., NeurIPS 2022）、**SAFE**（Wilson et al., ICCV 2023）和 **WFS**（Wu & Deng, CVPR 2025）等方法均在实例层面引入任务特定的正则化目标来增强 ID/OOD 判别能力，而 UNO-Adapter 将 OOD 检测的核心问题从“特征塑形”转向“概念注入”。

### 从实例正则化到全局概念注入

现有方法的共性瓶颈在于：它们仅利用检测器提取的实例级特征进行 OOD 评分或正则化训练，缺乏对场景中对象间关系的全局理解。UNO-Adapter 通过三个关键设计突破这一限制：

**1. 未知概念注入方式：无监督槽注意力概念发现**

传统方法通过虚拟异常合成（VOS）、特征塑形（SIREN）或分类得分（MSP, Energy）来定义“未知”，本质上是在实例特征空间中构造决策边界。UNO-Adapter 转而采用基于槽注意力（Slot Attention）的无监督概念发现模块（UCD），从密集像素中提取一组稀疏的、以对象为中心的槽表示，这些槽自动捕捉场景中的潜在概念及其相互关系。这一设计使“未知”不再是被动构造的负样本，而是从场景结构中主动发现的全局概念。

**2. 特征融合：从实例特征到槽-实例自适应绑定**

基线方法仅使用检测器的实例级特征进行 OOD 判别，忽略了跨对象的全局上下文。UNO-Adapter 通过神经概念绑定（NCB）机制，将 UCD 学到的槽表示与检测器的实例查询基于相似度进行自适应融合。关键优势在于：槽表示在训练阶段独立于检测模型学习，推理时的绑定过程无需训练，且保留了原始特征空间。这使得 UNO-Adapter 可以即插即用地适配任何检测器，而无需修改其损失函数或进行微调。

**3. OOD 评分：从实例级得分到图像引导的全局一致性评分**

传统方法（MSP、Energy）仅基于单个实例的 logits 或能量值进行 OOD 判定。UNO-Adapter 提出图像引导的 OOD 评分策略，融合两个互补信号：图像级余弦相似度（衡量槽重构与原始图像特征的一致性）和分位数阈值策略（跨所有检测对象自适应校准）。这一设计强化了 ID/OOD 决策边界的全局一致性，避免了实例级评分在复杂场景中的局部失真。

### 关键因果机制

UNO-Adapter 性能提升的因果链条可概括为：UCD 通过信息瓶颈原理对槽进行关系正则化和冗余压缩（式 $\mathcal{L}_{UCD} = \mathcal{L}_{recon} + \beta \mathcal{L}_{KL}$），使槽表示既保持对象中心的稀疏性，又捕捉对象间的全局交互；NCB 将这些富含全局概念的槽与检测器实例特征绑定，赋予每个检测对象“场景上下文”信息；最终，图像引导的 OOD 评分将槽重构质量与实例判别信号耦合，实现从全局到局部的 OOD 判定。消融实验（Table 3）证实，完整的 UCD+NCB+OOD Score 组合在 BDD-100K 上达到 97.61 AUROC 和 9.88 FPR95，显著优于仅使用 ID 特征或单独 UCD 的变体。

### 训练范式的根本转变

与需要修改检测器损失、进行任务特定微调的基线方法不同，UNO-Adapter 仅训练 UCD 模块（微调时间仅 0.1 小时），检测器权重完全冻结。推理时通过 NCB 进行零训练绑定，总推理时间 11.54 秒，显著低于 SIREN（36.31 秒/2.2 小时微调）和 SAFE（14.37 秒/3.6 小时微调）。这种“外挂式”设计使得 UNO-Adapter 具有极强的部署灵活性，可适配任意预训练检测器。



UNO-Adapter 的整体设计遵循“概念发现—概念绑定—评分决策”三阶段流水线，其核心思想是**在不修改检测器架构与权重的前提下，向检测器注入场景级的“未知”概念**，从而提升分布外（OOD）目标的判别能力。如图2所示，框架由三个关键模块串联构成：

1. **无监督概念发现（Unsupervised Concept Discovery, UCD）**：在训练阶段，从输入图像的密集像素特征中提取一组稀疏、对象中心化的槽（slot）表示。这些槽通过槽注意力机制捕获场景中的高层语义概念，并经由关系建模与信息瓶颈原理进行交互增强和冗余压缩，最终形成精炼的全局概念表征。
2. **神经概念绑定（Neural Concept Binder, NCB）**：在推理阶段，将UCD产出的槽表示与冻结检测器（Deformable DETR）输出的实例级特征基于相似度进行自适应融合。此过程无需训练，仅通过绑定操作将全局概念知识注入检测器的查询特征中，使每个检测到的目标同时携带局部实例信息和全局场景上下文。
3. **图像引导的OOD评分（Inference-Time OOD Score）**：结合图像级余弦相似度与分位数策略，为每个检测框计算最终的OOD分数 $\operatorname{score}(o_i, \pmb{b_i}) = \gamma \cdot \cos(\hat{\pmb{f_t}}, \pmb{f_t}) \cdot \Phi_{\tau}(z_i)$，以强化ID与OOD之间的决策边界一致性。

**输入输出流**：整个流程以单张RGB图像为输入。UCD模块从图像特征中输出 $S$ 个槽表示及对应的初始重要性分 $\pi_i^{\mathrm{init}}$；NCB模块接收槽表示与检测器输出的实例特征，输出绑定后的增强特征；最终OOD评分模块综合图像重建相似度和分位数阈值 $\tau$，为每个检测框输出一个标量OOD分数，分数越低表示越可能属于分布外目标。

**训练与推理分离的设计**：UCD模块独立于检测器进行训练，仅优化 $\mathcal{L}_{UCD} = \mathcal{L}_{recon} + \beta \mathcal{L}_{KL}$；检测器权重全程冻结。推理时，NCB绑定与OOD评分均为无参数的前向计算，使得UNO-Adapter在保持极低微调成本（0.1小时）的同时，实现了对多种检测器骨干的即插即用适配。

### 补充图表

![[assets/figures/papers/paper_list_l2052_https_openaccess_thecvf_com_content_CVPR2026_html_Peng_Learning_Latent_C/figures/002_Figure_2.jpg]]
*Figure 2: Overview of the proposed UNO-Adapter, which consists of three components: unsupervised concept discovery (UCD), neural concept binder (NCB), and an OOD object score. During training, UCD extracts sparse, high-level concepts from dense pixels, enhances the correlations among these concepts, and reduces redundant information. During inference, the refined slots are integrated with instance-level features via NCB. SA denotes “slot attention”, BG indicates “background”, and Obj is “object”*



### 3.1 问题形式化

给定测试图像 $\mathbf{x}^*$ 及检测器预测的边界框 $\mathbf{b}^*$，OOD 目标检测的目标是估计条件概率 $p(g \mid \mathbf{x}^*, \mathbf{b}^*)$，其中 $g=1$ 表示分布内（ID）目标，$g=0$ 表示分布外（OOD）目标。现有方法仅依赖检测器提取的实例级特征进行判别，缺乏对场景中对象间全局概念和因果关系的建模，导致 ID/OOD 决策边界失真。

UNO-Adapter 的核心洞察在于：**在不修改检测器架构和权重的前提下，通过无监督概念发现和神经概念绑定，为检测器注入全局“未知”概念**，从而提升 OOD 检测性能。

### 3.2 无监督概念发现（UCD）

UCD 模块基于槽注意力（Slot Attention）机制，从密集像素特征中提取一组稀疏的、以对象为中心的槽表示 $\{\mathbf{s}_i\}_{i=1}^S$，每个槽对应场景中的一个潜在概念。

**槽交叉注意力**：给定输入特征 $\mathbf{x}_j$，槽 $\mathbf{s}_i$ 与其之间的注意力权重通过缩放点积计算：

$$\alpha_{ij} = \mathrm{softmax}_i \left( \mathbf{s}_i^{\top} \mathbf{W}_Q \mathbf{x}_j / \sqrt{d_s} \right) \tag{1}$$

其中 $\mathbf{W}_Q$ 为可学习的查询投影矩阵，$d_s$ 为槽维度。注意力在槽维度上进行 softmax 归一化，使得每个输入特征被竞争性地分配给不同槽。

**槽更新**：通过加权聚合输入特征更新槽表示：

$$\hat{s}_i = \sum_{j=1}^{N} \alpha_{ij} \mathbf{W}_V \mathbf{x}_j \tag{2}$$

$\mathbf{W}_V$ 为值投影矩阵。更新后的槽 $\hat{s}_i$ 经过 GRU 进一步精炼，形成迭代式的槽注意力循环。

**关系建模与信息瓶颈**：为增强槽间的交互并压缩冗余信息，UCD 引入两个关键机制：

1. **槽重要性评分**：通过轻量 MLP $h_\theta$ 为每个槽预测初始重要性分：
   $$\pi_i^{\mathrm{init}} = \mathrm{sigmoid}(h_\theta(s_i)) \tag{3}$$

2. **关系矩阵**：建模槽之间的成对交互关系：
   $$W_{ij} = \mathrm{softmax}_j \left( (U v_i)^{\top} (V v_j) / \sqrt{d} \right) \tag{4}$$
   其中 $U$、$V$ 为可学习的全连接层（输入输出维度均为 256），$v_i$ 为槽的嵌入表示。

3. **加权 KL 散度正则化**：基于槽重要性对信息瓶颈施加压缩约束：
   $$\mathcal{L}_{KL} = \frac{1}{2} \pi_i \left( \mu_i + \sigma_i^{\prime 2} - 2 \log(\sigma_i^{\prime 2}) - 1 \right) \tag{8}$$
   其中 $\mu_i$、$\sigma_i^{\prime 2}$ 为信息瓶颈编码器输出的均值和方差。重要性分 $\pi_i$ 加权使得关键概念保留更多信息，冗余概念被更强压缩。

**UCD 总损失**：结合槽重构误差与 KL 正则化：
$$\mathcal{L}_{UCD} = \mathcal{L}_{recon} + \beta \mathcal{L}_{KL} \tag{9}$$

其中重构损失 $\mathcal{L}_{recon} = \| s_i^{\prime\prime} - \mathbf{s}_i^{\prime} \|^2$ 为精炼后槽 $s_i^{\prime\prime}$ 与原始槽 $\mathbf{s}_i^{\prime}$ 之间的均方误差，$\beta$ 为平衡系数。

### 3.3 神经概念绑定（NCB）

UCD 训练完成后，其学到的槽表示独立于检测模型。推理时，NCB 将槽表示与检测器的实例级特征基于相似度进行自适应融合，赋予检测器“未知”概念。该过程**无需训练**，保持原始特征空间不变。

### 3.4 图像引导的 OOD 评分

最终 OOD 评分融合图像级余弦相似度与分位数策略，确保全局一致性：

$$\operatorname{score}(o_i, \pmb{b_i}) = \gamma \cdot \cos(\hat{\pmb{f_t}}, \pmb{f_t}) \cdot \Phi_{\tau}(z_i) \tag{14}$$

其中：
- $\cos(\hat{\pmb{f_t}}, \pmb{f_t})$ 为重建图像特征与原始图像特征的余弦相似度，衡量图像级重建质量；
- $\Phi_{\tau}(z_i)$ 为分位数阈值函数，在 $N$ 个检测对象的 logits $\{z_i\}_{i=1}^N$ 中，取分位数 $\tau$ 对应的值作为判别阈值；
- $\gamma$ 为缩放因子。

该评分机制的核心逻辑：若图像整体重建质量差（低余弦相似度），且目标 logit 低于分位数阈值，则更可能为 OOD。图像级与实例级信息的协同有效强化了 ID/OOD 决策边界。



## 实验与关键发现

### 核心性能：OOD 目标检测

UNO-Adapter 在 OOD-OD 任务上展现出显著优势，尤其在更具挑战性的 BDD-100K 场景中，其性能大幅超越此前的最佳方法 **WFS**（Wu & Deng, CVPR 2025）。具体而言，在 BDD-100K 上以 MS-COCO 作为 OOD 时，FPR95 降低了 11.96%；以 OpenImages 作为 OOD 时，FPR95 降低了 4.03%。这验证了全局概念建模对复杂驾驶场景中“未知”物体判别的关键作用。在 PASCAL-VOC 基准上，UNO-Adapter 同样取得了 91.68 的 AUROC，表明该方法在不同数据域下均具有鲁棒性。

**Table 1** 中所有方法均基于相同的 Deformable DETR 骨干网络且未使用任何辅助数据，确保了公平对比。基线结果引用自原始论文或。

### 开放世界目标检测（OWOD）

在 OWOD 的 Task 2 设定下，UNO-Adapter 取得了 16.8 的 U-Recall 和 45.8 的整体 mAP（**Table 2**）。这表明通过槽注意力注入的全局“未知”概念，不仅有助于区分已知与未知类别，还能在增量学习场景中保持对已知类别的识别精度。

![[assets/figures/papers/paper_list_l2052_https_openaccess_thecvf_com_content_CVPR2026_html_Peng_Learning_Latent_C/figures/004_Table_2.jpg]]
*Table 2: The performance (%) of OWOD. The task definition strictly follows the setup of [26]. We mainly focus on the open-world setting, i.e., Task 2 and 3. For the closed-world setting (i.e., Task 1 and 4), we present only the more challenging task – Task 4. The results of all compared methods are cited from [65] as we follow their experimental setup, including dataset splits, model training, and evaluation*

### 消融实验：各模块的贡献

**Table 3** 的消融结果揭示了三个核心组件的因果效应：

- **仅使用 ID 特征**（即冻结检测器直接输出）时，BDD-100K 上的 AUROC 和 FPR95 表现较差，构成性能下界。
- **引入 UCD 模块**后，性能获得显著跃升，证明无监督概念发现所提取的稀疏、对象中心的槽表示能够有效捕获场景中与“未知”相关的全局结构。
- **完整的 UNO-Adapter**（UCD + NCB + OOD Score）达到最优：AUROC 97.61，FPR95 9.88。这确证了神经概念绑定（NCB）将槽表示与实例特征融合，以及图像引导的 OOD 评分策略，是两个不可或缺的性能倍增器。

### OOD 评分策略的拆解

**Table 5** 进一步剖析了 OOD 评分公式中各因子的作用。图像引导的余弦相似度与分位数阈值策略协同工作，将 PASCAL-VOC 上的 AUROC 推至 91.68，FPR95 降至 32.61。单独移除任一组分均会导致性能退化，说明图像级全局一致性约束与实例级自适应阈值的结合是决策边界清晰化的关键机制。

### 时间效率分析

**Table 6** 显示 UNO-Adapter 在推理效率上具有明显优势：推理时间仅 11.54 秒，微调时间仅 0.1 小时。相比之下，**SIREN**（Du et al., NeurIPS 2022）需要 36.31 秒推理和 2.2 小时微调，**SAFE**（Wilson et al., ICCV 2023）需要 14.37 秒推理和 3.6 小时微调。这一效率优势源于 UNO-Adapter 仅训练 UCD 模块而冻结检测器权重的设计选择。

### 可视化分析

**Figure 3** 展示了激活图与分割掩码的可视化对比。相比原始 Slot Attention（SA），UNO-Adapter 的 UCD 模块能够更精确地定位场景中的对象概念，且对背景噪声的抑制更为彻底。这归因于信息瓶颈原理对槽表示的冗余压缩和关系正则化对槽间交互的增强。

**Figure 4** 的定性检测结果显示，UNO-Adapter 在复杂场景中对 OOD 物体的定位精度和召回率均优于 SIREN 和 SAFE，尤其在物体重叠、遮挡和小目标场景下，全局概念建模的优势更加突出。

### 超参数敏感性

**Figure 5** 揭示了方法对两个关键超参数的敏感性：槽数量 $S$ 和分位数阈值 $\tau$。当 $S$ 过小时，槽表示不足以覆盖场景中的全部概念；当 $S$ 过大时，会引入冗余槽并稀释重要性分数。$\tau$ 则直接控制 OOD 评分的判定边界。实际部署时需根据目标场景对这两个参数进行仔细调优，这是该方法当前的一个已知局限。

### 近 OOD 与远 OOD 场景

在 ImageNet-200 基准上（**Table 4**），UNO-Adapter 在近 OOD（语义相近但类别不同的样本）上取得 87.90 AUROC / 50.42 FPR95，在远 OOD（语义差异大的样本）上取得 97.84 AUROC / 16.92 FPR95。近 OOD 场景下的性能降幅反映了基于槽的概念发现对细粒度语义差异的敏感性——当 ID 和 OOD 类别在视觉概念上高度重叠时，全局槽表示可能难以提供足够的判别信息，这是该方法的一个边界条件。

### 补充图表

![[assets/figures/papers/paper_list_l2052_https_openaccess_thecvf_com_content_CVPR2026_html_Peng_Learning_Latent_C/figures/003_Table_1.jpg]]
*Table 1: The performance (%) of OOD-OD. All methods are trained based on ID data and do not use any auxiliary data. Deformable DETR is used as the backbone detector*

![[assets/figures/papers/paper_list_l2052_https_openaccess_thecvf_com_content_CVPR2026_html_Peng_Learning_Latent_C/figures/005_Table_3.jpg]]
*Table 3: Ablation of UNO-Adapter*

![[assets/figures/papers/paper_list_l2052_https_openaccess_thecvf_com_content_CVPR2026_html_Peng_Learning_Latent_C/figures/007_Figure_3.jpg]]
*Figure 3: The visualization results of the activation map and segmentation mask. SA stands for original slot attention [35]*

![[assets/figures/papers/paper_list_l2052_https_openaccess_thecvf_com_content_CVPR2026_html_Peng_Learning_Latent_C/figures/008_Figure_4.jpg]]
*Figure 4: Qualitative visualization of detection results. We compared the proposed method with SIREN [10] and SAFE [48]*

![[assets/figures/papers/paper_list_l2052_https_openaccess_thecvf_com_content_CVPR2026_html_Peng_Learning_Latent_C/figures/009_Figure_5.jpg]]
*Figure 5: Analysis on hyperparameter sensitivity*

![[assets/figures/papers/paper_list_l2052_https_openaccess_thecvf_com_content_CVPR2026_html_Peng_Learning_Latent_C/figures/010_Table_5.jpg]]
*Table 5: The influence of OOD score*

![[assets/figures/papers/paper_list_l2052_https_openaccess_thecvf_com_content_CVPR2026_html_Peng_Learning_Latent_C/figures/011_Table_6.jpg]]
*Table 6: Analysis on time complexity*



## 定位与知识库关联

### 1. 方法角色：不修改检测器的“未知”概念注入适配器

UNO-Adapter 在 OOD 目标检测谱系中占据一个独特位置：它不修改检测器本身的架构或权重，而是通过一个可插拔的**无监督概念发现（UCD）**与**神经概念绑定（NCB）**模块，向冻结的检测器注入全局“未知”概念。这与主流范式形成鲜明对比：

- **实例级正则化范式**：**VOS**（Du et al., ICLR 2022）通过虚拟异常合成在实例特征上施加正则化；**SIREN**（Du et al., NeurIPS 2022）通过特征塑形增强 ID/OOD 区分性；**SAFE**（Wilson et al., ICCV 2023）引入敏感度感知的特征变换；**WFS**（Wu and Deng, CVPR 2025）模拟世界特征来扩展 ID 边界。这些方法均在检测器的实例级特征空间内操作，需要修改训练损失或进行特定任务的微调。
- **分类得分范式**：**MSP**（Hendrycks & Gimpel, ICLR 2017）和 **Energy**（Liu et al., NeurIPS 2020）等经典 OOD 评分方法直接利用检测器的 logits 或能量函数，缺乏对场景全局结构的建模。

UNO-Adapter 的核心区别在于：它通过槽注意力（slot attention）从像素级特征中无监督地发现对象中心的稀疏概念，并建模概念间的关系，再将这种全局理解绑定到检测器的实例特征上。这种“先理解场景，再判断异常”的流程模仿了人类视觉的认知过程，而无需改变检测器本身。

### 2. 方法谱系中的继承与突破

UNO-Adapter 的技术基因可追溯至两个关键来源：

**（1）槽注意力（Slot Attention）**：UCD 模块直接继承自 slot attention 机制（Locatello et al., NeurIPS 2020），通过迭代交叉注意力将密集特征压缩为一组对象中心的槽表示。但 UNO-Adapter 在此基础上引入了三项关键创新：
- **关系建模**：通过可学习矩阵 $U, V$ 计算槽间关系权重 $W_{ij} = \mathrm{softmax}_j \left( (U v_i)^{\top} (V v_j) / \sqrt{d} \right)$，增强槽之间的交互，使概念发现不再是孤立的。
- **信息瓶颈细化**：引入基于槽重要性的加权 KL 散度损失 $\mathcal{L}_{KL} = \frac{1}{2} \pi_i ( \mu_i + \sigma_i^{\prime 2} - 2 \log(\sigma_i^{\prime 2}) - 1 )$，压缩冗余信息，使槽表示更具判别性。
- **与检测器的绑定**：NCB 模块将槽表示与检测器查询基于相似度自适应融合，这是 slot attention 从未涉及的跨网络知识迁移。

**（2）开放世界目标检测（OWOD）**：**OW-DETR**（Gupta et al., CVPR 2022）等 OWOD 方法需要在检测器训练过程中显式建模未知类。UNO-Adapter 在 OWOD 基准上（Task 2）取得了 16.8 的 U-Recall 和 45.8 的 mAP，表明其概念发现机制同样适用于增量学习场景，但训练方式更轻量——仅需微调 UCD 模块（0.1h），远低于 SIREN（2.2h）和 SAFE（3.6h）。

### 3. 适用边界与局限

**适用场景**：
- 检测器架构为基于查询的 DETR 系列（如 Deformable DETR），因为 NCB 需要与检测器的查询特征进行绑定。
- ID 数据分布相对集中，OOD 对象在视觉概念上与 ID 存在可区分的差异。
- 对推理效率有一定容忍度（11.54s 总推理时间，含 UCD 前向传播）。

**已知局限**：
- **超参数敏感性**：槽数量 $S$ 和分位数阈值 $\tau$ 对性能存在明显影响（见图5），实际部署时需针对具体场景调优，缺乏自适应的参数选择机制。
- **检测器架构依赖**：NCB 的绑定机制假设检测器输出实例级查询特征，对于单阶段检测器（如 YOLO 系列）或基于锚框的方法，适配方案尚不明确。
- **极端场景未验证**：论文主要在 PASCAL-VOC、BDD-100K 和 ImageNet-200 上评估，对于密集遮挡、小目标密集分布或域偏移极大的场景（如医疗影像、遥感图像），UCD 的概念发现质量可能下降。

### 4. 开放问题

论文引言中提出的核心挑战——“如何设计一个模仿人类视觉过程的统一框架来检测 OOD 对象”——仍存在以下未解决问题：

1. **概念发现的语义可控性**：UCD 目前是完全无监督的，发现的槽概念缺乏语义标签，无法保证其与人类可理解的对象概念对齐。如何引入弱监督或语言引导，使概念发现更具可解释性和可控性？
2. **动态场景下的概念演化**：在 OWOD 场景中，ID 类别会逐步增加，当前 UCD 需要在新数据上重新训练。能否实现概念的增量学习，使槽表示随 ID 知识扩展而动态演化？
3. **与多模态模型的融合**：人类视觉过程融合了语言、先验知识等多模态信息。UNO-Adapter 目前仅依赖视觉信号，能否与视觉-语言模型（如 CLIP）结合，利用文本描述增强“未知”概念的建模？
4. **理论保证的缺失**：信息瓶颈原理在 UCD 中的应用缺乏严格的理论分析，例如 KL 散度正则化与 OOD 检测性能之间的定量关系、槽数量 $S$ 的下界等，均有待形式化研究。



## 原文 PDF

![[paperPDFs/CVPR_2026/Learning_Latent_Concepts_for_Detecting_Out_of_Distribution_Objects.pdf]]
