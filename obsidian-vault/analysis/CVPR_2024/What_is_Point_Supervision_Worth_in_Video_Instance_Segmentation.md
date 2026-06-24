---
title: "What is Point Supervision Worth in Video Instance Segmentation?"
type: paper
paper_level: A
venue: CVPR
year: 2024
pdf_ref: paperPDFs/CVPR_2024/What_is_Point_Supervision_Worth_in_Video_Instance_Segmentation.pdf
aliases:
- WIPSWVIS
tags:
- CVPR_2024
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: "通过类无关时空提案生成（利用COCO预训练编码形状先验）和点驱动的匹配器（引入交叉实例负样本和掩码置信度）构造高质量伪掩码，自训练进一步缩小图像到视频的域差。"
primary_logic: "仅需对每个视频对象标注一个正点，即可恢复全监督87%以上的性能，负点比正点对性能贡献更大，且负点位置比正点位置更重要。"
claims:
- "在YouTube-VIS 2019上，PointVIS (P1N1) 的AP达到59.6，相当于全监督MinVIS的96.7%"
- "交叉实例负样本损失和掩码度损失使mAP提升5.7点"
- "仅使用一个正点(P1)即可达到53.9 AP (87.5% of MinVIS)"
- "YouTube-VIS 2019 上 AP = 59.6"
---

# What is Point Supervision Worth in Video Instance Segmentation?

> [!tip] 核心洞察
> 仅需对每个视频对象标注一个正点，即可恢复全监督87%以上的性能，负点比正点对性能贡献更大，且负点位置比正点位置更重要。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 点监督在视频实例分割中的价值探究 |
| 英文题名 | What is Point Supervision Worth in Video Instance Segmentation? |
| 会议/期刊 | CVPR 2024 |
| Links | [paper](https://arxiv.org/abs/2404.01990v1) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/image_and_video_generation |
| Method | PointVIS |
| Dataset | YouTube-VIS 2019, YouTube-VIS 2021, OVIS |

> [!tip] 效果简介
> - YouTube-VIS 2019 上，AP 为 59.6，对比 61.7，变化 -2.1 (96.7%)。
> - YouTube-VIS 2021 上，AP 为 48.5，对比 55.3，变化 -6.8 (87.7%)。
> - OVIS 上，AP 为 28.6，对比 39.4，变化 -10.8 (72.6%)。

## 概述

**问题瓶颈**：视频实例分割（VIS）的密集掩码标注成本极高，而稀疏点监督下模型难以获取精确的目标边界和负样本，导致决策边界学习困难。

**核心思路**：PointVIS 通过类无关时空提案生成（利用 COCO 预训练编码形状先验）和点驱动的匹配器（引入交叉实例负样本与掩码置信度）构造高质量伪掩码，再以自训练缩小图像到视频的域差。

**关键发现**：仅需对每个视频对象标注一个正点，即可恢复全监督 87% 以上的性能；负点比正点对性能贡献更大，且负点位置比正点位置更重要。

**主要结果**：在 YouTube-VIS 2019 上，PointVIS（P1N1）达到 59.6 AP，相当于全监督 MinVIS 的 96.7%；在 YouTube-VIS 2021 上达到 48.5 AP（87.7%）；在严重遮挡的 OVIS 上达到 28.6 AP（72.6%），与全监督差距较大，暴露了伪掩码时域不一致和遗漏小/重叠对象的局限。

**方法定位**：PointVIS 属于弱监督 VIS，标注成本介于无监督方法（如 VIS-Unsup）和图像级弱监督方法（如 VISC，Liu et al., CVPR 2021）之间，但性能显著优于两者。其伪标签生成管线可嵌入现有基于查询的 VIS 框架（如 MinVIS，Huang et al., arXiv 2022），无需修改网络结构。

## 背景与动机

视频实例分割（VIS）要求同时检测、分割和跟踪视频中的对象实例，是视频理解的核心任务之一。近年来，全监督方法在该领域取得了显著进展，但其成功高度依赖密集的实例掩码标注——标注者需要为每一帧的每一个目标绘制精确的像素级轮廓。这种标注方式成本极高：一个短视频中仅标注单个对象实例就可能需要数十分钟，而完整标注一个标准VIS数据集所需的人力成本往往令人望而却步。标注瓶颈已成为制约VIS方法向更大规模、更多类别扩展的根本性障碍。

面对这一瓶颈，现有工作主要沿两个方向探索降低标注成本：**无监督方法**（如VIS-Unsup）完全放弃标注，但性能与全监督存在巨大鸿沟；**弱监督方法**（如VISC，Liu et al., CVPR 2021）使用图像级标签，但缺乏空间定位信息导致边界精度严重不足。一个关键但未被充分探索的问题是：**是否存在一种标注代价极低、却能保留密集掩码大部分性能的监督形式？**

点监督正是这样一种候选方案——标注者只需在每个视频对象上点击一个点，即可表达“这个位置属于该对象”的信息。相比密集掩码，点标注的时间成本可降低两个数量级以上。然而，点监督在VIS中面临独特的挑战：单个正点几乎不提供任何目标边界信息，也无法显式地告诉模型“哪里不是该对象”（负样本缺失）。这使得模型难以学习精确的决策边界，尤其是在多对象遮挡、外观相似的复杂视频场景中。

本文的核心动机正是系统性地探究点监督在VIS中的价值边界：**仅需极稀疏的点标注，究竟能恢复全监督性能的多大比例？正点和负点各自扮演什么角色？** 通过回答这些问题，我们希望为VIS社区提供一个标注效率与性能之间的量化参考，并揭示点监督中负样本的关键作用——这一发现可能改变人们对“标注什么最重要”的认知。

## 核心创新

PointVIS 的核心创新在于将视频实例分割的标注需求从**密集逐帧掩码**压缩为**每对象一个正点（及可选负点）**，并通过“提案-匹配-自训练”三阶段框架将稀疏点监督转化为高质量伪掩码，从而恢复全监督 87% 以上的性能。以下从三个 **changed slot** 展开其相对于全监督基线 **MinVIS**（Huang et al., arXiv 2022）的关键差异。

### 1. 标注范式：从密集掩码到稀疏点

全监督 VIS 需要为每个实例在每一帧提供精确的像素级掩码，标注成本极高。PointVIS 将标注量级压缩至极限：**每个视频对象仅需标注一个正点**（P1），即可在 YouTube-VIS 2019 上达到 53.9 AP，相当于 MinVIS 全监督性能的 87.5%（Table 1）。若额外引入一个负点（P1N1），性能进一步提升至 59.6 AP（96.7% of MinVIS）。这一标注效率的根本性突破构成了方法设计的出发点。

### 2. 伪标签生成：类无关时空提案 + 点驱动匹配器

全监督方法直接使用标注掩码作为训练目标，而 PointVIS 必须从稀疏点标注中构造伪掩码。其核心方案由两个模块构成：

**类无关时空提案生成**利用 COCO 预训练的图像实例分割模型对视频逐帧推理，再通过查询嵌入（query embeddings）的二部图匹配将逐帧提案关联为时空一致的视频级提案 $\hat{\mathbf{R}} = \mathbf{F}(\mathbf{V}; \theta_I) = \{\hat{\mathbf{M}}_r, \hat{c}_r\}_{r=1}^{R}$。COCO 预训练编码了丰富的形状先验，使提案天然具备合理的实例边界，无需任何视频掩码标注。

**点驱动匹配器**通过匈牙利算法将提案与点标注进行最优匹配，生成伪掩码。其关键创新在于匹配成本函数的设计：

$$\mathcal{L}_{\mathrm{match}} = \lambda_1 \mathcal{L}_{\mathrm{ann}} + \lambda_2 \mathcal{L}_{\mathrm{cineg}} + \lambda_3 \mathcal{L}_{\mathrm{maskness}}$$

- **标注一致性成本 $\mathcal{L}_{\mathrm{ann}}$**：统计提案掩码在标注点位置与标签不一致的帧数，确保正点落在掩码内、负点落在掩码外。
- **交叉实例负样本成本 $\mathcal{L}_{\mathrm{cineg}}$**：利用同一帧中其他实例的标注点作为当前对象的免费负样本，无需额外标注即可大幅增强决策边界的判别力。
- **掩码度成本 $\mathcal{L}_{\mathrm{maskness}}$**：以提案 logits 的时空均值 $c_r = \frac{1}{H \times W \times T} \sum_{x,y,z} \hat{\mathbf{M}}_r(x,y,z)$ 作为类无关置信度，抑制碎片化提案。

消融实验（Table 2）表明，仅使用 $\mathcal{L}_{\mathrm{ann}}$ 时 mAP 为 40.4；加入 $\mathcal{L}_{\mathrm{cineg}}$ 和 $\mathcal{L}_{\mathrm{maskness}}$ 后 mAP 跃升 5.7 点至 46.1，验证了交叉实例负样本和掩码度对伪掩码质量的决定性贡献。

### 3. 自训练：弥合图像到视频的域差

由于提案生成器基于 COCO 图像预训练，其产生的伪掩码在视频域中存在分布偏移。PointVIS 引入**自训练**：用微调后的视频模型重新生成伪标签，并将匹配成本中的掩码度分数替换为模型自身的置信度分数。Table 2 显示自训练将 mAP 从 46.1 进一步提升至 47.3，有效缩小了图像到视频的领域差距。

### 创新总结

PointVIS 的三处 changed slot——稀疏点标注、提案-匹配伪标签生成、自训练——形成了一条完整的低标注依赖 VIS 技术路径。其核心洞察在于：**负点比正点对性能贡献更大，且负点位置比正点位置更关键**（Table 4），这一发现为极低标注场景下的实例分割提供了重要的设计指引。

## 整体框架

PointVIS 的整体流程由三个核心模块串联构成：**类无关时空提案生成**、**基于点的时空匹配器**与**自训练**（Figure 2）。其设计逻辑是：利用 COCO 预训练的图像分割模型提供的丰富形状先验，在无需任何视频掩码标注的条件下生成密集的时空提案；再通过点标注驱动的匹配器为每个目标对象分配最优提案，从而构造高质量的伪掩码；最后借助自训练缩小图像预训练模型与视频域之间的分布差异。

### 输入与输出流

- **输入**：一段视频 $\mathbf{V}$ 与稀疏点标注集。每个视频对象仅需一个正点（及可选的负点），标注形式为 $\{(\mathbf{P}_j^t(k), \mathbf{L}_j^t(k))\}$，其中 $\mathbf{P}_j^t(k)$ 为第 $t$ 帧中第 $j$ 个对象的第 $k$ 个点的坐标，$\mathbf{L}_j^t(k) \in \{0, 1\}$ 表示该点为正或负。
- **输出**：视频实例分割结果，即每个实例在每一帧上的掩码预测。

### 模块关系与数据流

1. **类无关时空提案生成**
   将视频 $\mathbf{V}$ 送入基于 COCO 预训练的查询式图像实例分割模型 $\mathbf{F}(\cdot; \theta_I)$，逐帧生成实例提案，再通过查询嵌入的二部图匹配将其关联为时空提案：
   $$\hat{\mathbf{R}} = \mathbf{F}(\mathbf{V}; \theta_I) = \{\hat{\mathbf{M}}_r, \hat{c}_r\}_{r=1}^{R}$$
   其中 $\hat{\mathbf{M}}_r$ 为连续 logits 掩码，$\hat{c}_r$ 为由掩码度分数（maskness score）给出的类无关置信度：
   $$c_r = \frac{1}{H \times W \times T} \sum_{x,y,z} \hat{\mathbf{M}}_r(x,y,z)$$
   该模块的核心价值在于：无需任何视频掩码标注即可提供具有形状先验的时空提案，同时为后续匹配提供了丰富的负样本池。

2. **基于点的时空匹配器**
   将生成的提案与点标注进行匈牙利匹配，以构造伪掩码。匹配成本函数融合三项：
   $$\mathcal{L}_{\mathrm{match}} = \lambda_1 \mathcal{L}_{\mathrm{ann}} + \lambda_2 \mathcal{L}_{\mathrm{cineg}} + \lambda_3 \mathcal{L}_{\mathrm{maskness}}$$
   - **标注一致性成本** $\mathcal{L}_{\mathrm{ann}}$：统计提案掩码在标注点位置与点标签不一致的次数，惩罚未覆盖正点或错误覆盖负点的提案。
   - **交叉实例负样本成本** $\mathcal{L}_{\mathrm{cineg}}$：利用同一帧中其他实例的标注作为当前对象的负样本，强制提案不覆盖其他对象的正点区域，从而引入更清晰的决策边界。
   - **掩码度成本** $\mathcal{L}_{\mathrm{maskness}}$：引导匹配器偏好高置信度的提案。
   匹配完成后，每个对象获得一个最优提案作为伪掩码，用于后续视频模型的训练。

3. **自训练**
   用生成的伪掩码训练视频实例分割模型后，利用微调后的模型重新推理并生成新的伪标签，再次训练。该步骤的关键改动是：自训练阶段使用模型自身的置信度分数替代原始的掩码度分数进行匹配，因为此时模型已在视频数据上微调，置信度更可靠。自训练有效弥合了 COCO 图像域与目标视频域之间的分布差异。

### 关键设计决策

- **类无关设计**：提案生成与匹配器均不依赖类别信息，使得整个流程可泛化至新类别。
- **负点的核心地位**：消融实验表明，交叉实例负样本成本 $\mathcal{L}_{\mathrm{cineg}}$ 和掩码度成本 $\mathcal{L}_{\mathrm{maskness}}$ 共同带来 5.7 mAP 的提升（Table 2），且增加负点比增加正点对性能的贡献更为显著（Table 4）。
- **标注效率的极致压缩**：整个流程仅需每对象一个正点即可恢复全监督 87.5% 的性能（Table 1, P1），加入一个负点后进一步提升至 96.7%。

### 补充图表

![[assets/figures/papers/paper_list_l17_https_arxiv_org_abs_2404_01990v1/figures/001_Figure_1.jpg]]
*Figure 1: Point-supervised video instance segmentation in this work (YoutubeVIS-2021). Top: point-level annotations in the training set (pseudo masks generated from our method overlaid); Bottom: mask predictions in the validation set*

## 核心模块与公式推导

PointVIS 通过三个级联模块将稀疏点标注转化为稠密伪掩码，进而训练标准的视频实例分割模型。其核心逻辑是：先利用图像预训练模型生成类无关的时空提案以提供形状先验和负样本，再通过点驱动的匹配器将提案与点标注配对生成高质量伪掩码，最后以自训练弥合图像到视频的领域差距。

### 类无关时空提案生成

该模块利用在 COCO 上预训练的图像实例分割模型，对输入视频 $\mathbf{V}$ 逐帧生成实例提案，并通过查询嵌入的二部图匹配将逐帧提案关联为时空提案。形式上，给定视频 $\mathbf{V}$ 和预训练模型参数 $\theta_I$，生成 $R$ 个时空提案：

$$\hat{\mathbf{R}} = \mathbf{F}(\mathbf{V}; \theta_I) = \{\hat{\mathbf{M}}_r, \hat{c}_r\}_{r=1}^{R}$$

其中 $\hat{\mathbf{M}}_r$ 为连续 logits 掩码，$\hat{c}_r$ 为类无关置信度，由提案 logits 在时空维度上的均值计算得到：

$$c_r = \frac{1}{H \times W \times T} \sum_{x,y,z} \hat{\mathbf{M}}_r(x,y,z)$$

这一设计的关键在于：COCO 预训练模型编码了丰富的形状先验，使得提案即使在未见类别上也能提供合理的轮廓候选；同时，未被匹配的提案自然构成负样本池，为后续匹配器提供交叉实例负样本。

### 点驱动匹配器

匹配器通过匈牙利算法将时空提案与点标注进行最优配对，生成伪掩码。匹配总成本由三项加权组成：

$$\mathcal{L}_{\mathrm{match}} = \lambda_1 \mathcal{L}_{\mathrm{ann}} + \lambda_2 \mathcal{L}_{\mathrm{cineg}} + \lambda_3 \mathcal{L}_{\mathrm{maskness}}$$

**标注一致性成本** $\mathcal{L}_{\mathrm{ann}}$ 统计提案掩码在所有帧上与点标签的不一致次数。对于第 $j$ 个标注对象 $\mathbf{G}_j$ 和与其匹配的提案 $\mathbf{R}_{\sigma(j)}$：

$$\mathcal{L}_{\mathrm{ann}}(\mathbf{G}_j, \mathbf{R}_{\sigma(j)}) = \sum_{t=1}^{T} \sum_{k=1}^{N_j^t} \mathbb{1}[\mathbf{M}_{\sigma(j)}(\mathbf{P}_j^t(k), t) \neq \mathbf{L}_j^t(k)]$$

其中 $\mathbf{P}_j^t(k)$ 为第 $t$ 帧第 $k$ 个标注点的空间位置，$\mathbf{L}_j^t(k)$ 为该点的标签（正点为 1，负点为 0），$\mathbf{M}_{\sigma(j)}$ 为匹配提案的二值化掩码。该成本直接惩罚提案在标注点处与标签不一致的情况。

**交叉实例负样本成本** $\mathcal{L}_{\mathrm{cineg}}$ 利用同一帧中其他实例的标注点作为当前对象的负样本，强化了决策边界的判别性。这是本文的关键创新之一——无需额外标注即可获得高质量的实例间负样本。

**掩码度成本** $\mathcal{L}_{\mathrm{maskness}}$ 基于提案的类无关置信度 $c_r$ 进行加权，倾向于选择置信度高的提案，抑制碎片化或低质量的候选。

消融实验（Table 2）表明：仅使用 $\mathcal{L}_{\mathrm{ann}}$ 时 mAP 为 40.4；加入 $\mathcal{L}_{\mathrm{cineg}}$ 和 $\mathcal{L}_{\mathrm{maskness}}$ 后 mAP 提升 5.7 点至 46.1，验证了交叉实例负样本和掩码度成本的关键作用。

### 自训练

图像预训练模型与视频域之间存在分布差异。PointVIS 在首轮伪掩码生成后，用伪掩码微调视频实例分割模型，再以微调后模型重新生成伪标签。此轮自训练中，掩码度分数被替换为模型自身的置信度分数，因为微调后的模型已适应视频域。Table 2 显示自训练将 mAP 从 46.1 进一步提升至 47.3。

## 实验与分析

### 主实验结果

PointVIS在三个主流视频实例分割基准上验证了点监督的有效性。Table 1展示了基于Swin-L骨干网络的全掩码监督（M）与点监督（P）的性能对比。在YouTube-VIS 2019上，仅使用每对象一个正点和一个负点（P1N1）的PointVIS达到59.6 AP，相当于全监督MinVIS（61.7 AP）的96.7%。即使仅使用一个正点（P1），模型仍能达到53.9 AP，保留全监督性能的87.5%。在YouTube-VIS 2021上，P1N1达到48.5 AP，保留率为87.7%。然而，在包含严重遮挡场景的OVIS数据集上，性能退化较为明显，P1N1仅达到28.6 AP，保留率降至72.6%，揭示了方法在复杂场景下的局限性。

与无监督和弱监督基线的对比（Table 5）进一步验证了点监督的价值：PointVIS显著优于无监督方法VIS-Unsup和基于图像级标注的弱监督方法VISC（Liu et al., CVPR 2021），表明稀疏点标注在信息密度上远超图像级标签。

![[assets/figures/papers/paper_list_l17_https_arxiv_org_abs_2404_01990v1/figures/005_Table_5.jpg]]
*Table 5: Comparison with baselines on YouTube-VIS 2019 [58] validation set*

### 消融实验

Table 2系统拆解了各组件对YouTube-VIS 2019 val-dev性能的贡献。仅使用标注一致性损失（$\mathcal{L}_{\mathrm{ann}}$）生成伪掩码时，模型达到40.4 mAP。加入交叉实例负样本损失（$\mathcal{L}_{\mathrm{cineg}}$）和掩码度损失（$\mathcal{L}_{\mathrm{maskness}}$）后，性能显著提升5.7点至46.1 mAP，验证了负样本和置信度建模对伪掩码质量的关键作用。自训练进一步将mAP从46.1提升至47.3，表明微调后的视频模型能有效缩小图像到视频的领域差距。

关于点标注策略，Table 3分析了点选择偏差的影响。在框内随机采样、距离变换采样和图像内随机采样三种策略下，性能差距均不超过0.9 AP，说明方法对正点位置选择具有较好的鲁棒性。Table 4揭示了正负点的非对称重要性：增加负点比增加正点对性能提升更为显著，且负点位置比正点位置更关键——这一反直觉发现表明，决策边界的学习更依赖于高质量的负样本信号。

### 稀疏帧标注下的泛化性

Table 6展示了在视频帧二次采样场景下的性能。即使仅使用部分帧进行点标注，PointVIS（P1N1，无自训练）仍能保持较强的泛化能力，验证了时空提案生成模块对时序稀疏性的鲁棒性。

### 失败模式与局限性

Figure 4展示了OVIS数据集上的典型失败案例。伪掩码存在两类主要问题：一是时序不一致性（如左上角老虎的掩码在帧间抖动），二是实例遗漏（如白色衣服的行人被完全忽略）。这些问题在严重遮挡、小目标密集和长序列场景下尤为突出，与OVIS上72.6%的保留率下降相互印证。根本原因在于：COCO预训练的形状先验难以覆盖严重遮挡场景的视觉模式，且匈牙利匹配在实例高度重叠时容易产生歧义分配。此外，Figure 3的伪掩码可视化显示，在YouTube-VIS数据集上伪掩码质量较高，但在OVIS上边界精度明显下降，进一步支持了上述分析。

**需要手动验证**：Table 5中VIS-Unsup的具体数值和引用信息在给定材料中未明确提供，建议查阅原文确认。

### 补充图表

![[assets/figures/papers/paper_list_l17_https_arxiv_org_abs_2404_01990v1/figures/004_Table_1.jpg]]
*Table 1: Full mask (M) vs. our point supervision (P) on validation set of YouTube-VIS 2019 [58], YouTube-VIS 2021 [58], and OVIS [46]. All results below are based on Swin-L backbone. Our PointVIS results are with self-training*

![[assets/figures/papers/paper_list_l17_https_arxiv_org_abs_2404_01990v1/figures/006_Table_2.jpg]]
*Table 2: Effects of each component on YouTube-VIS 2019 [58] val-dev*

![[assets/figures/papers/paper_list_l17_https_arxiv_org_abs_2404_01990v1/figures/007_Table_3.jpg]]
*Table 3: Analysis of point selection bias on YouTube-VIS 2019 [58] val-dev. Table 4. Effects of additional points on YouTube-VIS 2019 [58] val-dev. “DPPointMatcher” means Dense Pseudo via Point Matcher. “CINeg” means enforcing additional negative point loss*

![[assets/figures/papers/paper_list_l17_https_arxiv_org_abs_2404_01990v1/figures/008_Table_6.jpg]]
*Table 6: PointVIS (P1N1) with subsampled video frames on YouTube-VIS 2019 validation set (w/o self-training)*

## 方法谱系与知识库定位

### 任务定位与核心差异

PointVIS 定位于视频实例分割（Video Instance Segmentation, VIS）的弱监督学习范式，其核心差异在于将标注成本从密集掩码降至每对象一个正点（及可选负点）。与全监督基线 **MinVIS**（Huang et al., arXiv 2022）相比，PointVIS 在 YouTube-VIS 2019 上仅用 P1N1（每对象一个正点一个负点）即达到 59.6 AP，保留全监督性能的 96.7%（Table 1）。与无监督基线 **VIS-Unsup** 和弱监督基线 **VISC**（Liu et al., CVPR 2021，使用图像级标注）相比，PointVIS 在相同基准上展现出显著优势（Table 5），表明点级时空监督在标注效率与性能之间取得了更优的平衡。

### 关键设计选择与知识来源

PointVIS 的性能高度依赖两个外部知识来源：**COCO 预训练的图像实例分割模型**提供的形状先验，以及**点标注中隐含的时空对应关系**。类无关时空提案生成模块（Class-Agnostic Spatio-Temporal Proposal Generation）利用 COCO 预训练模型对每帧生成实例提案，再通过查询嵌入的二部图匹配将其转化为时空一致的视频提案（Section 3.2, Equation 1）。这一设计将图像域的形状知识迁移至视频域，但同时也构成了方法的适用边界：若目标类别与 COCO 类别重叠度低，提案质量将显著下降。

点匹配器（Point-Based Matcher）的设计体现了对弱监督信号利用的深入思考。匹配成本函数（Equation 4）由三项加权组成：
$$\mathcal{L}_{\mathrm{match}} = \lambda_1 \mathcal{L}_{\mathrm{ann}} + \lambda_2 \mathcal{L}_{\mathrm{cineg}} + \lambda_3 \mathcal{L}_{\mathrm{maskness}}$$
其中标注一致性成本 $\mathcal{L}_{\mathrm{ann}}$ 统计提案掩码与点标签的时空不一致次数（Equation 3），交叉实例负样本成本 $\mathcal{L}_{\mathrm{cineg}}$ 引入同一帧内其他实例作为无需额外标注的负样本，掩码度成本 $\mathcal{L}_{\mathrm{maskness}}$ 则利用提案 logits 的时空均值作为类无关置信度。消融实验（Table 2）表明，仅使用 $\mathcal{L}_{\mathrm{ann}}$ 时 mAP 为 40.4，加入 $\mathcal{L}_{\mathrm{cineg}}$ 和 $\mathcal{L}_{\mathrm{maskness}}$ 后提升 5.7 点至 46.1，自训练进一步将 mAP 推至 47.3。

### 监督信号效率的核心发现

PointVIS 揭示了一个反直觉的规律：**负点比正点对性能贡献更大，且负点位置比正点位置更重要**。Table 1 显示仅用 P1（一个正点）即可达到 53.9 AP（全监督的 87.5%），而加入一个负点（P1N1）后提升至 59.6 AP（96.7%）。Table 4 进一步表明，增加负点比增加正点带来更显著的性能增益。然而，Table 3 显示不同负点采样策略（框内随机采样、距离变换采样、图像内随机采样）之间的性能差距不超过 0.9 AP，说明负点位置的选择对最终性能影响有限——这一结论需注意实验均在模拟点标注条件下得出，真实人工标注的偏差可能更大。

### 适用边界与退化条件

方法在三个基准上的性能保留率呈现明显梯度：YouTube-VIS 2019 上达 96.7%，YouTube-VIS 2021 上为 87.7%，OVIS 上仅 72.6%（Table 1）。OVIS 的严重遮挡和长序列特性暴露了 PointVIS 的核心脆弱性：伪掩码可能出现时域不一致（如目标身份在帧间漂移）和遗漏小/重叠对象（Figure 4）。这一退化源于提案生成模块在遮挡场景下难以维持时空一致性，且点匹配器缺乏显式的时序平滑机制。

Table 6 展示了帧二次采样下的性能变化，表明方法在更少标注帧条件下仍具一定泛化能力，但该实验未包含自训练，实际部署中的退化程度可能不同。

### 方法谱系中的位置与未覆盖方向

在 VIS 弱监督方法谱系中，PointVIS 填补了无监督（VIS-Unsup）与图像级弱监督（VISC）之间的空白，将监督信号精确到时空点级别。然而，当前方法仅探索了点击监督，未涉及更弱的监督形式如涂鸦或图像级标签。此外，方法对 COCO 预训练的依赖使其本质上属于迁移学习范式，而非全自监督设置。

### 开放问题

1. **时序一致性增强**：如何结合视频帧间对应关系（如光流或点跟踪）以进一步去噪伪掩码并提高时序一致性，尤其是在 OVIS 类严重遮挡场景下？
2. **超参数自适应**：匹配器中的超参数 $\lambda_1, \lambda_2, \lambda_3$ 目前为固定值，其最优自动调节策略尚待探索。
3. **极度稀疏标注**：在帧级标注比例降至 1% 以下的极端条件下，如何维持时序一致性和检测精度？
4. **任务扩展**：点监督范式能否扩展至 3D 视频实例分割或更复杂的时空任务？
5. **预训练依赖消除**：是否可以在无 COCO 预训练的全自监督设置下实现可比性能，从根本上降低对外部标注数据的依赖？

## 原文 PDF

![[paperPDFs/CVPR_2024/What_is_Point_Supervision_Worth_in_Video_Instance_Segmentation.pdf]]
